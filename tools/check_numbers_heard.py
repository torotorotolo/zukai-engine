# -*- coding: utf-8 -*-
r"""check_numbers_heard.py — 台本の数字が、文字起こしの中に**数として**現れているか検査する。

  python tools\check_numbers_heard.py ep008

なぜ要るか（2026-08-31）:
  ep008 は178行中101行が数字を含む「数字だらけの回」で、数字の誤読が最大の地雷でした。
  ところが一致率（difflib）は表記のゆれに引きずられて役に立ちません
  （「三千四周」と「3.4周」が、正規化で"千"を落とした結果**偶然一致**していた実例あり）。
  そこで **漢数字を本当に数へ直してから**、台本の数と突き合わせます。

⚠️ これは門番ではありません。文字起こし自体が誤るので、出た行は人が中身を見ます。
⚠️ 逆に **0件でも「誤読が無い」ことにはなりません**（同音の別語・助詞の崩れは拾えません）。
    この検査が見るのは**数だけ**です。

🔴 2026-09-23（12本目⑤a）: 鳴った16行のうち **15行が「1500万トン」型の空振り**だった（本物は c512-1 の1行だけ）。
    台本側が「1500万」を **1500** と拾い、聞取『千五百万』（＝15000000）と当たらなかった。
    同じ穴は 10本目に el_ledger.numbers_missing だけ塞いで、**こちらには効いていなかった**
    （[[feedback-gates-blind-spot-is-the-scan-direction]]）。
    → 数の物差しは**ここ1か所**に置く（script_numbers／heard_numbers／numbers_missing／numbers_extra）。
       el_ledger・el_retake・el_ab_verdict はここを import する。

出力: 台本の数のうち、聞取の中に見つからないものを行ごとに出す。見つからない数があれば exit 1。
"""
import re
import sys
import unicodedata
from decimal import Decimal
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
DIG = {"〇": 0, "零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
       "六": 6, "七": 7, "八": 8, "九": 9}
UNIT = {"十": 10, "百": 100, "千": 1000}
BIG = {"万": 10000, "億": 100000000}


def kan2int(s: str):
    """「百七十七」→177 ／「二〇〇九」→2009。読めなければ None（fail closed 側）。"""
    if not s:
        return None
    if all(c in DIG for c in s):                     # 桁を並べた書き方（二〇〇九）
        return int("".join(str(DIG[c]) for c in s))
    total = cur = 0
    num = None
    for c in s:
        if c in DIG:
            num = DIG[c]
        elif c in UNIT:
            cur += (num if num is not None else 1) * UNIT[c]
            num = None
        elif c in BIG:
            cur += num or 0
            total += (cur or 1) * BIG[c]
            cur = 0
            num = None
        else:
            return None
    return total + cur + (num or 0)


KANNUM = "〇零一二三四五六七八九十百千万億"
# 「十四点二」のような小数も拾う
PAT = re.compile(f"[{KANNUM}]+(?:点[{KANNUM}]+)?")
NUM = r"\d+(?:\.\d+)?"
# 算用数字に 千・万・億 が付いた「合成の数」（1500万／7億2千万／1万4000／2万5千／7万1136）。
# 台本・聞取の両側で**かたまりごと1つの数**に直す。直さないと:
#   台本側 …「1500万」を 1500 と拾い、聞取『千五百万』（15000000）と当たらない（12本目⑤a の15行）
#   聞取側 …『3200万』を 3200 と「万」だけの 10000 に割る（el_retake が「数の余り:10000」を出す）
# 🔴 2026-09-20（10本目）にも同じ型: 台本の「7万1,136」を 7 と 1136 に割り、N万M,MMM の10行・N億ウォンの6行が
#    **全部鳴りっぱなし**だった。`c306-1` は 71,136 を 71,336 と読んでいた**本物**なのに、同じ見え方をしていた。
# 先頭の単位は 千・万・億 だけ（「5百」「3十」は語の一部のことがある）。聞取は数字と単位の間に空白が入ることがある。
MIX = re.compile(rf"{NUM} ?[千万億](?:[千百十万億]|{NUM})*")


def _mixed_value(s: str):
    """「1500万」→'15000000'／「7億2千万」→'720000000'／「1万4000」→'14000'。読めなければ None。
    数え方は kan2int と同じ（算用数字のかたまりを、漢数字1字と同じく「その桁の値」として扱う）。
    ⚠️ 昔の el_ledger._expand_kanji_units（正規表現の置き換え）は「万のあとに千」を読み違えていた:
       8本目 c729-3「1万9千」→ 10009000・c807-1「2万5千」→ 20005000（正しい読みの2行を鳴らしていた）、
       「1億2000万」→ 1000020000000。"""
    total = cur = Decimal(0)
    num = None
    for t in re.findall(rf"{NUM}|[千百十万億]", s):
        if t[0].isdigit():
            if num is not None:                      # 数が2つ続く＝読めない（fail closed 側）
                return None
            num = Decimal(t)
        elif t in UNIT:
            cur += (num if num is not None else 1) * UNIT[t]
            num = None
        else:
            cur += num or 0
            total += (cur or 1) * BIG[t]
            cur = 0
            num = None
    v = total + cur + (num or 0)
    return str(int(v)) if v == v.to_integral_value() else format(v.normalize(), "f")


def _kan_decimal(m):
    """『二七．六』→ '27.6'。小数部は桁の並び（〇五 → .05）。"""
    a, b = kan2int(m[1]), m[2]
    b = "".join(str(DIG[c]) for c in b) if all(c in DIG for c in b) else kan2int(b)
    return f"{a}.{b}" if a is not None and b is not None else m.group()


def heard_numbers(h: str):
    """聞取の文から、出てくる数の集合を作る（アラビア数字と漢数字の両方）。"""
    h = unicodedata.normalize("NFKC", h)
    # 🔴 2026-09-16（9本目）: 桁区切りのカンマを外す（外さないと『3,400』を 3 と 400 に割る）
    h = re.sub(r"(?<=\d),(?=\d{3})", "", h)
    # 🔴 2026-09-20（10本目）: 漢数字＋全角の点で書いた小数（`pr06-1`『二七．六メートル』）は 27 と 6 に割れる。
    #    NFKC で点を半角にしたうえで、点をはさむ漢数字を先に算用数字へ直す（もとは el_ledger だけにあった）
    h = re.sub(rf"([{KANNUM}]+)\.([〇零一二三四五六七八九十]+)", _kan_decimal, h)
    out = set()

    def _mix(m):
        v = _mixed_value(m.group())
        if v is None:
            return m.group()
        out.add(v)
        return " "          # 拾ったかたまりは消す（下で 3200 と 万=10000 に割って数え直さない）

    h = MIX.sub(_mix, h)
    for m in re.findall(NUM, h):
        out.add(m.rstrip("0").rstrip(".") if "." in m else m)
        out.add(m)
    for m in PAT.finditer(h):
        s = m.group()
        if "点" in s:
            a, b = s.split("点", 1)
            ia, ib = kan2int(a), None
            # 小数部は桁の並び（点四 → .4／点六 → .6）
            if all(c in DIG for c in b):
                ib = "".join(str(DIG[c]) for c in b)
            if ia is not None and ib is not None:
                out.add(f"{ia}.{ib}")
        else:
            v = kan2int(s)
            if v is not None:
                out.add(str(v))
    return out


def script_numbers(text: str):
    """台本の数を [(見出し, 当たりとする値, 聞取に出てよい値)] の並びで返す。

    - 「1500万」「7億2千万」は **全体の値だけ**を当たりにする（15000000／720000000）。
      ⚠️ 素の 1500 でも当たりにすると、万の落ちた『千五百トン』（1万分の1の誤読）が素通りする。
         聞取が『3200万』と数字で書いた行（12本目 c820-2）は、聞取側も 32000000 に直すので素の桁は要らない。
    - 「聞取に出てよい値」（el_retake の「数の余り」用）には素の桁も入れる（聞取に 1500 があっても余りとは言わない）。
    - 「¾インチ」（c412 の決め所）は数字を含まないので「4分の3」に開く。
    - 🔴 2026-09-16（9本目）: 桁区切りのカンマは外す。外さないと「3,400」を 3 と 400 に割り、
      『三千四百』と正しく読んだテイクまで不合格にしていた（el_retake が c303-1 の数の合ったテイクを落とした）。
    """
    t = re.sub(r"(?<=\d)[,，](?=\d{3})", "", text.replace("¾", "4分の3"))
    out = []
    for m in re.finditer(rf"{MIX.pattern}|{NUM}", t):
        g = m.group()
        v = _mixed_value(g) if MIX.fullmatch(g) else None
        if v is not None:
            out.append((g.replace(" ", ""), {v}, {v} | set(re.findall(NUM, g))))
            continue
        for n in re.findall(NUM, g):
            c = {n, n.rstrip("0").rstrip(".") if "." in n else n}
            out.append((n, c, c))
    return out


def numbers_missing(text: str, heard: str):
    """台本の数のうち、聞取に**数として**見当たらないもの（見出しの並び。空＝全部ある）。"""
    got = heard_numbers(heard)
    return [lab for lab, need, _ in script_numbers(text) if not (need & got)]


def numbers_extra(text: str, heard: str):
    """台本に無い数が、聞取に**増えている**もの（el_retake の「数の余り」）。数字を含まない行は見ない。
    1〜3 は「ひとつ／ふたつ／みっつ」を Scribe が 一つ／二つ／三つ と書くので除く。"""
    if not re.search(r"\d", text):
        return []
    have = set().union(*(ok for _, _, ok in script_numbers(text)))
    return sorted(n for n in heard_numbers(heard)
                  if n not in have and n not in {"1", "2", "3"}
                  and not any(n == m.rstrip("0").rstrip(".") for m in have))


# ---- 門番: この検査そのものの検算（実行のたびに必ず走る）----------------------------
# ⚠️ 「0件でした」と出たときは**まず道具を疑う**（[[feedback-verify-your-own-instrument]]）。
#    ここには 2026-08-31 に実際に壊れていた聞取をそのまま固定してある。
#    ここが通らなければ、検査の結果は信用できないので **答えを出さずに止める**。
_SELFTEST = [
    # (台本, 聞取, 見つからないはずの数)  ← 直す前に実測した壊れた側
    ("2006年、アメリカのワシントン大学で、1つの実験が行われました。",
     "2004年、アメリカのワシントン大学で一つの実験が行われました。", ["2006"]),
    ("3.4周というのは、つまり、14.2周のおよそ4分の1です。",
     "三千四周というのは、つまり十四点二周のおよそ四分の一です。", ["3.4"]),
    ("61点と40点の差は21点、100問なら21問ぶんです。",
     "授業一点と四十点の差は二十一点、百問なら二十一問分です。", ["61"]),
    # 正しく読めている側は素通りしなければならない（＝全部NGと言う壊れ方も捕まえる）
    ("19人。全体の10.7パーセントです。", "十九人、全体の十点七パーセントです。", []),
    ("これを挙げた人は177人中148人で、割合にすると83.6パーセントにあたります。",
     "これを挙げた人は百七十七人中百四十八人で、割合にすると八十三点六パーセントにあたります。", []),
    ("2つ目の質問は選ぶ形式で、こちらは、177人のうち101人が答えています。",
     "二つ目の質問は選ぶ形式で、こちらは百七十七人のうち百一人が答えています。", []),
    # ── 2026-09-23（12本目⑤a）: 算用数字＋千・万・億。正しく読めた行は素通り（直す前は全部鳴っていた）──
    ("TNT火薬に直して1500万トンぶん。", "TNT火薬に直して千五百万トン分。", []),               # c102-1・c504-1（「1500万」は6行）
    ("当時のお金で7億2千万円。", "当時のお金で七億二千万円。", []),                           # c819-3
    ("配られた人だけで、1万人を超えていた。", "配られた人だけで一万人を超えていた。", []),     # c211-2
    ("威力は、TNT火薬に直して1040万トンぶん。", "威力はTNT火薬に直して千四十万トン分", []),     # c205-2
    ("署名は、1955年の秋までに3200万を超えた。", "署名は1955年の秋までに3200万を超えた。", []),  # c820-2 聞取も数字
    ("高さは、およそ1万4000メートルだ。", "高さはおよそ1万4000mだ。", []),                    # 11本目 c406-2
    ("許可のときは71,136平方メートルだった", "許可の時は七万千百三十六平方メートルだった", []),  # 10本目 c306-1 取り直し後
    ("いちばん高いところで27.6メートル。", "一番高いところで二七．六メートル。", []),          # 10本目 pr06-1 の古い聞取の書き方
    # ── 本物の誤読は、万・億を足しても鳴り続けなければならない ──
    ("住民239人", "住民に百三十九人", ["239"]),
    ("許可のときは71,136平方メートルだった", "許可の時は七万一千三百三十六平方メートルだった", ["71136"]),  # 10本目 c306-1 の本物
    ("TNT火薬に直して1500万トンぶん。", "TNT火薬に直して千五百トン分。", ["1500万"]),        # 万が落ちた（素の桁で当てると素通り）
    ("署名は、1955年の秋までに3200万を超えた。", "署名は1955年の秋までに3200を超えた。", ["3200万"]),
    ("当時のお金で7億2千万円。", "当時のお金で七億二千円。", ["7億2千万"]),
    ("乗っていたのは3200人。", "乗っていたのは3200万人。", ["3200"]),     # 万が増えた（直す前の聞取側は 3200 も拾って素通り）
]

# 「数の余り」（el_retake）: (台本, 聞取, 余るはずの数)
_SELFTEST_EXTRA = [
    ("6回のうち3回は、TNT火薬に直して1000万トンを超えた。",
     "六回のうち三回はTNT火薬に直して一千万トンを超えた。", []),                 # c210-1（直す前は 10000000 が余り）
    ("署名は、1955年の秋までに3200万を超えた。", "署名は1955年の秋までに3200万を超えた。", []),  # 直す前は「万」だけの 10000 が余り
    ("1982年の報告書も、7、8分と書いている。", "1982年の報告書も七、八十分と書いている。", ["80"]),
    ("乗っていたのは23人。", "乗っていたのは二十三万人。", ["230000"]),
]


def _selftest():
    bad = []
    for text, heard, want in _SELFTEST:
        miss = numbers_missing(text, heard)
        if miss != want:
            bad.append(f"  「{text[:24]}…」／聞取「{heard[:24]}…」→ {miss}／期待 {want}")
    for text, heard, want in _SELFTEST_EXTRA:
        extra = numbers_extra(text, heard)
        if extra != want:
            bad.append(f"  （数の余り）「{text[:24]}…」／聞取「{heard[:24]}…」→ {extra}／期待 {want}")
    if bad:
        raise RuntimeError("★検査そのものが壊れています（判定を出しません）:\n" + "\n".join(bad))


def main(slug=None):
    _selftest()
    import el_script as ES     # 事故検証ch：tsv は audio/el_qa/<SLUG>_el_yomi.tsv
    p = ES.qa_path("el_yomi.tsv")
    if not p.exists():                                # fail closed
        print(f"[FATAL] 文字起こしがありません: {p}", file=sys.stderr)
        print("        先に el_check_yomi.py を回してください。", file=sys.stderr)
        return 1
    rows = [l.split("\t")[:4] for l in p.read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    ng = 0
    for sid, r, text, heard in rows:
        miss = numbers_missing(text, heard)
        if miss:
            ng += 1
            print(f"🔴 {sid} 一致率{float(r)*100:.1f}%  聞取に見当たらない数: {miss}")
            print(f"     台本: {text}")
            print(f"     聞取: {heard}")
    total_nums = sum(len(script_numbers(t)) for _, _, t, _ in rows)
    print(f"\n検査 {len(rows)}行／台本の数 {total_nums}個 → 聞取に見当たらない数がある行: {ng}行")
    print("⚠️ 0件でも『誤読なし』ではありません。この検査が見るのは**数だけ**です。")
    return 1 if ng else 0


if __name__ == "__main__":
    sys.exit(main())
