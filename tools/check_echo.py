# -*- coding: utf-8 -*-
"""図がナレーションの複写になっていないかを機械で見る。

■ なぜ要るか
  映像ルール6「**ナレーションで話していることを図内にそのまま書かない**」。
  これを破ると、同じ文が **音・字幕・図** の三重になって画面が読むものだらけになる。
  テスト映像（10カット）では c3 の1件を目視で見つけられたが、
  **本編は226カット・417行ある。目で追うのは無理**なので機械で測る。

■ 測り方
  カットごとに、そのカットの全レイヤーの `<text>` を集め、同じカットの
  ナレーション行と突き合わせ、**いちばん長い連続一致**が図の文字列の 0.72 倍以上なら複写。

  ⚠️ 最初は「共通部分列」（飛び飛びでよい）で測って**誤検出だらけになった**。
     日本語は助詞と常用漢字が共通なので、図のラベル「海面のボート」が
     「船の中にいた人も、海面の小さなボートにいた人も」と 100% 一致と出た。
     部位名は複写ではない。**連続一致で測るのが正しい。**

  次のものは対象外にする（図が持つべき情報そのもの、または意図した設計）：
    ・12字未満／数字と単位だけの文字列
    ・quote() の決め所（phrase）と出どころの札（who/to/when/doc・rows）… 引用を画面に留めるのが目的の型

■ 🔴 2026-09-06 に足した3つの規則（サーフサイド ⑤c の目視で素通りした 8件から）
  ⚠️ それまで「t と s しか集めていない」と引き継がれていたが**誤り**。全レイヤーの <text> を
     集めているので note・blocks・lead・注記の d も見ていた。素通りの真因は次の3つ：
     ① 図の文が**ナレーションの1文を丸ごと含んで、さらに語尾を足している**
        （c311 note「柱が床を突き抜けるようにして壊れる＝押し抜き（模式図）」＝1文16字＋8字。
        図の文を分母にすると 16/24＝67% で 0.72 に届かない）
        → **ナレーションの1文を分母にした比**も見る（**文で割る**。行でなく「。」で切った文）
     ② **語順が入れ替わっている／1語だけ違う**ので連続一致が2か所に割れる
        （c307 note「広い床が、柱の断面ぶんしか支えに触れていない」 対
        「広い床が、柱の太さのぶんしか、支えに触れていない」＝6字＋13字）
        → **いちばん長い一致と、それを除いた2番目の一致（5字以上）の合計**でも測る
     ③ 見出し（t）が字幕の1文と**句点・時制・助詞だけ違う同文**
        （c101「12階建て、高さは33.8メートル」／c217「…残っていた」対「…残っている」）。
        見出しは「話題を出す場所」として 0.90 未満を黙らせていたが、**同文は主張ではない**
        → 見出し・副題は字幕の**1文**と比べ、丸ごと同一／文字の近さ 0.80 以上／
          8字以上で文の頭か尻をそのまま切り取っている、のどれかで鳴らす
  ⚠️ 12字の閾値は据え置き（「柱と、床の板とのつなぎ目」11字は名前として通る）。

■ 出るもの
  🔴 … 直す。図の文を数値・関係・出どころに置き換える。見出しは主張に書き換える
  ・  … 参考（--all で出る）

使い方： python tools/check_echo.py [--only=c3] [--all] [--check]
         --check … 道具そのものの検算（作り物の例で、鳴るべきものが鳴り・黙るべきものが黙るか）
"""
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S

TEXT = re.compile(r'<text\s[^>]*>([^<]*)</text>')
UNESC = {"&amp;": "&", "&lt;": "<", "&gt;": ">"}
HEAD_RATIO = 0.90        # 見出し・副題・引用の決め所はここまで許す（--all の参考表示）
BODY_RATIO = 0.72        # 図の中の文字はここを超えたら複写
MINLEN = 12
# 🔴 6字で切っていたら、図が**物の名前を書けなくなった**。
#    「この日の操縦士」「沿岸警備隊の輸送機」「カナダの救難調整本部」「声で話す装置」は
#    どれも図がラベルとして持つべき固有名詞で、ナレーションに出て当たり前。
#    ルールが禁じているのは**文（節）の複写**なので、節の長さで切る。
#    12字＝「〜は〜だった」が丸ごと入る長さ。ここより短いものは名前として扱う。
CHUNK = 5                # 2か所に割れた一致の、2番目の一致の最短（4字だと「ている」類の助詞が乗る）
HEAD_NEAR = 0.80         # 見出し・副題が字幕の1文と「ほぼ同文」と見なす近さ（SequenceMatcher）
HEAD_EDGE = 8            # 見出しが字幕の1文の頭か尻をそのまま切り取っている、と見なす最短の字数
#    ⚠️ 0.80 の根拠：⑤c の台帳で ⚠️（直す）とした c101 1.00・c217 0.92・c312 0.86・c232 0.83 が上、
#       ・（直さない）とした c215 0.72・c226・c317 が下に分かれる値。上げると c232 を落とす。

# 図が持ってよい語（数値・単位・部位名）。これだけで出来た文字列は複写と見なさない。
DATAISH = re.compile(r"^[0-9０-９,.，．%％\s"
                     r"a-zA-Zａ-ｚＡ-Ｚ"
                     r"年月日時分秒回本個名人隻機層枚倍度円"
                     r"午前後ごろ"
                     r"メートルインチフィートポンドマイルパーセントキロ"
                     r"／/・:：〜~\-−－(（)）]+$")


# 🔴 カタカナだけで出来た語は**固有名詞**。字数が伸びるだけで節ではない。
#    「ミッションスペシャリスト」は13字あるが、そのカットの主題そのもので、
#    図がこれを書けないと何の話か分からなくなる。
KATAKANA = re.compile(r"[ァ-ヶー・]+")

# 図の引数のうち、文字列でも「画面の文」ではないもの（色・種類・ファイル名・位置）
NOT_TEXT_KEYS = {"c", "vc", "dc", "tc", "kc", "kind", "mode", "photo", "at", "anchor", "fam",
                 "font", "img", "src", "side", "ref"}


def unesc(t):
    for k, v in UNESC.items():
        t = t.replace(k, v)
    return t


def norm(s):
    """比べるための正規化。読点・空白・かっこを落とす。"""
    if isinstance(s, (list, tuple)):
        s = "".join(str(x) for x in s)
    return re.sub(r"[、。，．\s「」『』（）()【】・…　]", "", str(s))


def sentences(rows):
    """字幕の行を「。」で文に切る。[(正規化した文, 元の文)]。"""
    out = []
    for r in rows:
        for part in re.split(r"[。]", str(r)):
            n = norm(part)
            if n:
                out.append((n, part.strip()))
    return out


def lcsub_pos(a, b):
    """いちばん長い**連続**一致（長さ, a の位置, b の位置）。

    🔴 部分列（飛び飛び）で測ると日本語では誤検出しかしない。助詞と常用漢字が
       どの文にも出るので、無関係なラベルが 100% 一致と判定される。
    """
    if not a or not b:
        return 0, -1, -1
    best = (0, -1, -1)
    prev = [0] * (len(b) + 1)
    for i, ca in enumerate(a):
        cur = [0] * (len(b) + 1)
        for j, cb in enumerate(b):
            if ca == cb:
                cur[j + 1] = prev[j] + 1
                if cur[j + 1] > best[0]:
                    best = (cur[j + 1], i - cur[j + 1] + 1, j - cur[j + 1] + 1)
        prev = cur
    return best


def lcsub(a, b):
    return lcsub_pos(a, b)[0]


def two_chunks(a, b):
    """いちばん長い一致＋それを除いた2番目の一致（CHUNK 字以上）の合計。

    語順の入れ替え・1語の置き換えで一致が2か所に割れる複写（c307 の形）を拾う。
    2つまでしか足さない（3つ以上足すと「部分列」に近づいて誤検出が戻る）。
    """
    n1, ia, ib = lcsub_pos(a, b)
    if n1 == 0:
        return 0
    a2 = a[:ia] + "\x00" * n1 + a[ia + n1:]
    b2 = b[:ib] + "\x01" * n1 + b[ib + n1:]
    n2 = lcsub(a2, b2)
    return n1 + (n2 if n2 >= CHUNK else 0)


def exempt_strings(spec):
    """そのカットで「ナレーションに寄ってよい」文字列（見出し・副題・引用の札）。"""
    out = {norm(spec.get("t", "")), norm(spec.get("s", ""))}
    fig = spec.get("fig")
    if fig and fig[0] == "quote":
        # 🔴 2026-08-01 追加：**出どころの札（誰が・誰に・いつ・どこに）も免除する。**
        #    `tools/cuts/README.md` の規則2は「引用カットは言葉でなく出どころを図にする。
        #    誰が・誰に・いつ・どこに書かれていたかを左の札に置く」と定めている。
        #    ＝この4つは**図が持つべき情報そのもの**であって、複写ではない。
        #    ⚠️ 決め所（phrase）しか免除していなかったため、副題を減量した c227 で
        #      「沿岸警備隊にいた元技術者」（誰が）が複写と誤検出された。
        #      それまでは副題が同じ語を含んでいて、たまたま免除に引っかかっていただけ。
        for k in ("phrase", "who", "to", "when", "doc"):
            out.add(norm(fig[1].get(k, "")))
        # 4本目からは rows=[("誰が", "…", 色)] の形。値（2番目）は同じ役目なので同じく免除
        for row in fig[1].get("rows", []) or []:
            if isinstance(row, (list, tuple)) and len(row) >= 2:
                out.add(norm(row[1]))
    return {s for s in out if s}


def spec_strings(spec):
    """カット表から**画面に出る文字列を丸ごと**集める。[(どこ, 文字列)]。

    レイヤーの <text> は para で折り返されて断片になることがあるので、
    引数の文字列そのものを1本として比べる（規則①②はこちらで測る）。
    """
    out = []

    def walk(v, where):
        if isinstance(v, str):
            if v.strip():
                out.append((where, v))
        elif isinstance(v, dict):
            for k, x in v.items():
                if k in NOT_TEXT_KEYS:
                    continue
                walk(x, f"{where}.{k}" if where else k)
        elif isinstance(v, (list, tuple)):
            for x in v:
                walk(x, where)

    fig = spec.get("fig")
    if fig:
        walk(fig[1], fig[0])
    walk(spec.get("ann", []), "ann")
    return out


def judge_body(n, sents):
    """図の文 n（正規化ずみ）が字幕のどの文の複写か。(比, 規則, 元の文) か None。"""
    for sn, raw in sents:
        if n in sn:
            return 1.0, "そのまま含まれる", raw
        a = lcsub(n, sn)
        r1 = a / len(n)
        r2 = a / len(sn) if a >= MINLEN else 0.0
        c = two_chunks(n, sn)
        r3 = c / len(n) if c >= MINLEN else 0.0
        r4 = c / len(sn) if c >= MINLEN else 0.0
        r = max(r1, r2, r3, r4)
        if r >= BODY_RATIO:
            rule = ("連続一致" if r == r1 else
                    "字幕の1文をほぼ丸ごと含む" if r == r2 else
                    "2か所に割れた一致の合計" if r == r3 else
                    "2か所に割れた一致が字幕の1文をほぼ覆う")
            return r, rule, raw
    return None


def judge_head(n, sents):
    """見出し・副題 n（正規化ずみ）が字幕の1文と同文か。(近さ, 規則, 元の文) か None。"""
    if len(n) < HEAD_EDGE or DATAISH.match(n):
        return None
    for sn, raw in sents:
        if n == sn:
            return 1.0, "句点を除いて丸ごと同一", raw
        r = SequenceMatcher(None, n, sn).ratio()
        if r >= HEAD_NEAR:
            return r, "ほぼ同文（時制・助詞・1語だけ違う）", raw
        if sn.startswith(n) or sn.endswith(n):
            return len(n) / len(sn), "字幕の1文の頭か尻を、そのまま切り取っている", raw
    return None


def main(only=None, show_all=False):
    jobs, _ = S.build_layers(allow_missing=True)
    bycut = defaultdict(list)
    for k, svg in jobs.items():
        cid = k.rsplit("_", 1)[0]
        if only and not cid.startswith(only):
            continue
        for m in TEXT.finditer(svg):
            t = unesc(m.group(1)).strip()
            if t:
                bycut[cid].append((k, t))

    # ⚠️ レイヤー名では見分けられない。実写カットは見出しが `_lab` に入るので、
    #    **カット表の中身**（t / s / quote の phrase）と突き合わせて判定する。
    exempt = {cid: exempt_strings(sp) for cid, sp in S.SPEC.items()}

    hard = soft = heads = 0
    for cid in sorted(bycut):
        rows = [r["text"] for r in S.SUBS.get(cid, [])]
        if not rows:
            continue
        narr = [norm(r) for r in rows]
        sents = sentences(rows)
        ex = exempt.get(cid, set())
        spec = S.SPEC.get(cid, {})
        said = set()

        # ── 規則③ 見出し・副題 対 字幕の1文 ──
        for key, name in (("t", "見出し"), ("s", "副題")):
            n = norm(spec.get(key, ""))
            if not n:
                continue
            j = judge_head(n, sents)
            if j:
                heads += 1
                said.add(n)
                print(f"  🔴 {cid} [{name}]「{spec[key]}」\n"
                      f"      字幕の1文「{j[2]}」と {j[0]:.0%}＝{j[1]}")

        # ── 規則①② 図の文字列を丸ごと 対 字幕の1文 ──
        for where, t in spec_strings(spec):
            n = norm(t)
            if n in said or len(n) < MINLEN or DATAISH.match(t) or KATAKANA.fullmatch(n):
                continue
            if any(n in h or h in n for h in ex):
                continue
            j = judge_body(n, sents)
            if j:
                hard += 1
                said.add(n)
                print(f"  🔴 {cid} [{where}]「{t}」\n"
                      f"      字幕「{j[2]}」と {j[0]:.0%}（{j[1]}）")

        # ── 従来：レイヤーの <text>（折り返しの断片も含む） 対 字幕の行 ──
        for layer, t in bycut[cid]:
            n = norm(t)
            if n in said or len(n) < MINLEN or DATAISH.match(t) or KATAKANA.fullmatch(n):
                continue
            # 折り返された断片も見出し扱いにする（para が行を割るため）
            is_ex = any(n in h or h in n for h in ex)
            lim = HEAD_RATIO if is_ex else BODY_RATIO
            for src, nr in zip(rows, narr):
                r = 1.0 if n in nr else lcsub(n, nr) / len(n)
                if r < lim:
                    continue
                if is_ex:
                    # 見出し・副題の同文は規則③が言う。ここは参考表示だけ
                    soft += 1
                    if show_all:
                        print(f"  ・ {cid} [見出し/決め所]「{t}」 ≒ {r:.0%}「{src}」")
                else:
                    hard += 1
                    said.add(n)
                    print(f"  🔴 {cid} [{layer}]「{t}」\n"
                          f"      ナレーション「{src}」と {r:.0%} 一致"
                          f"{'（そのまま含まれる）' if n in nr else ''}")
                break
    bad = hard + heads
    print(f"\n{'🔴 図がナレーションの複写になっている箇所あり' if bad else '✓ 複写は無い'}"
          f"（複写 {hard}件・見出し/副題の同文 {heads}件・見出しの近さ {soft}件）")
    if soft and not show_all:
        print("   （見出しの近さは --all で出る。0.80 未満は「話題を出す場所」として黙る）")
    return 1 if bad else 0


def selfcheck():
    """★道具そのものを検算する（作り物の例。実データを直しても結果が変わらない）。"""
    print("── 道具の検算 ──")
    ok = True
    subs = ["柱が床を突き抜けるようにして壊れる。だから、押し抜き、という名前が付いている。",
            "広い床が、柱の太さのぶんしか、支えに触れていない。",
            "鉄筋を入れて固めた、コンクリートの平らな板のことである。",
            "スラブは、柱の上に置かれているのではない。",
            "そのスラブの上に、重さが載る。歩く人、停まっている車、敷かれた土、舗装、植木。",
            "手のひらを縦にして、そのまま差し込める幅にあたる。",
            "まる一日近くが、残っている。",
            "聞き取りの図に描き込まれるくらい、水は話に出ていた。",
            "2021年6月24日、午前1時22分ごろ。"]
    sents = sentences(subs)
    body = [
        ("①1文を丸ごと含んで語尾を足す（c311 の形）",
         "柱が床を突き抜けるようにして壊れる＝押し抜き（模式図）", True),
        ("①1文の大半を含む（c304 の形）",
         "柱の上に置かれているのではなく、つながっている（模式図）", True),
        ("②語が1つ違って一致が2か所に割れる（c307 の形）",
         "広い床が、柱の断面ぶんしか支えに触れていない（模式図）", True),
        ("②語順が入れ替わる（c303 の形）",
         "鉄筋を入れて固めた、平らなコンクリートの板", True),
        ("②並べた語が同じ（c305 の形）",
         "載るもの＝歩く人、停まっている車、土、舗装、植木（模式図）", True),
        ("部位名・関係だけ（**直さない**）", "白い帯＝柱の断面（模式図）", False),
        ("数を宣言する注記（**直さない**）", "矢印は向きだけ。本数に意味はない（模式図）", False),
        ("12字未満は名前（**直さない**）", "柱と、床の板とのつなぎ目", False),
    ]
    for name, s, should in body:
        n = norm(s)
        hit = (len(n) >= MINLEN and not DATAISH.match(s) and not KATAKANA.fullmatch(n)
               and judge_body(n, sents) is not None)
        mark = "✓" if hit == should else "✗"
        ok &= hit == should
        print(f"  {mark} {name}\n      「{s}」→ {'言う' if hit else '黙る'}"
              f"（そうあるべき: {'言う' if should else '黙る'}）")
    head = [
        ("③句点を除いて同一（c101 の形）", "12階建て、高さは33.8メートル",
         ["寸法が書き込まれている。12階建て、高さは33.8メートル。"], True),
        ("③時制だけ違う（c217 の形）", "まる一日近くが、残っていた", subs, True),
        ("③1語が挟まる（c312 の形）", "壊れる前に、前ぶれが出ない",
         ["壊れる前に、ほとんど前ぶれが出ない。"], True),
        ("③助詞だけ違う（c232 の形）", "その映像は、ここでは出さない",
         ["ただし、その映像を、ここでは出さない。"], True),
        ("③文の尻をそのまま（c210 の形）", "水は、話に出ていた", subs, True),
        ("主張として言い換えている（c215＝**直さない**）", "手のひらを縦に差し込める幅", subs, False),
        ("日付・時刻だけの見出し（pr01＝**直さない**）", "2021年6月24日、午前1時22分", subs, False),
        ("字幕の一部の語を使うだけ（**直さない**）", "支えに触れているのは、柱の太さだけ", subs, False),
    ]
    for name, t, rows, should in head:
        hit = judge_head(norm(t), sentences(rows)) is not None
        mark = "✓" if hit == should else "✗"
        ok &= hit == should
        print(f"  {mark} {name}\n      「{t}」→ {'言う' if hit else '黙る'}"
              f"（そうあるべき: {'言う' if should else '黙る'}）")
    print(f"── {'✓ 道具は使える' if ok else '🔴 道具が壊れている。直してから使う'} ──\n")
    return ok


if __name__ == "__main__":
    only = next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")), None)
    if "--check" in sys.argv and not selfcheck():
        sys.exit(1)
    sys.exit(main(only, "--all" in sys.argv))
