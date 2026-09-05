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

出力: 台本の数のうち、聞取の中に見つからないものを行ごとに出す。見つからない数があれば exit 1。
"""
import re
import sys
import unicodedata
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


def heard_numbers(h: str):
    """聞取の文から、出てくる数の集合を作る（アラビア数字と漢数字の両方）。"""
    h = unicodedata.normalize("NFKC", h)
    out = set()
    for m in re.findall(r"\d+(?:\.\d+)?", h):
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
]


def _selftest():
    bad = []
    for text, heard, want in _SELFTEST:
        got = heard_numbers(heard)
        miss = [m for m in re.findall(r"\d+(?:\.\d+)?", text)
                if not ({m, m.rstrip("0").rstrip(".") if "." in m else m} & got)]
        if miss != want:
            bad.append(f"  「{text[:24]}…」／聞取「{heard[:24]}…」→ {miss}／期待 {want}")
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
        got = heard_numbers(heard)
        miss = []
        # 「¾インチ」（c412 の決め所）は数字を含まないので、台本側だけ「4分の3」に開いて数を見る
        text = text.replace("¾", "4分の3")
        for m in re.findall(r"\d+(?:\.\d+)?", text):
            cand = {m, m.rstrip("0").rstrip(".") if "." in m else m}
            if not (cand & got):
                miss.append(m)
        if miss:
            ng += 1
            print(f"🔴 {sid} 一致率{float(r)*100:.1f}%  聞取に見当たらない数: {miss}")
            print(f"     台本: {text}")
            print(f"     聞取: {heard}")
    total_nums = sum(len(re.findall(r"\d+(?:\.\d+)?", t.replace("¾", "4分の3"))) for _, _, t, _ in rows)
    print(f"\n検査 {len(rows)}行／台本の数 {total_nums}個 → 聞取に見当たらない数がある行: {ng}行")
    print("⚠️ 0件でも『誤読なし』ではありません。この検査が見るのは**数だけ**です。")
    return 1 if ng else 0


if __name__ == "__main__":
    sys.exit(main())
