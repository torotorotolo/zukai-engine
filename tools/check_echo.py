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
    ・6字未満／数字と単位だけの文字列
    ・見出し（t）と副題（s）… 話題を出す場所なので寄って当然。丸ごと同一のときだけ言う
    ・quote() の決め所（phrase）… 引用を画面に留めるのが目的の型なので意図的

■ 出るもの
  🔴 … 直す。図の文を数値・関係・出どころに置き換える
  ・  … 参考（--all で出る）

使い方： python tools/check_echo.py [--only=c3] [--all]
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S

TEXT = re.compile(r'<text\s[^>]*>([^<]*)</text>')
UNESC = {"&amp;": "&", "&lt;": "<", "&gt;": ">"}
HEAD_RATIO = 0.90        # 見出し・副題・引用の決め所はここまで許す
BODY_RATIO = 0.72        # 図の中の文字はここを超えたら複写
MINLEN = 12
# 🔴 6字で切っていたら、図が**物の名前を書けなくなった**。
#    「この日の操縦士」「沿岸警備隊の輸送機」「カナダの救難調整本部」「声で話す装置」は
#    どれも図がラベルとして持つべき固有名詞で、ナレーションに出て当たり前。
#    ルールが禁じているのは**文（節）の複写**なので、節の長さで切る。
#    12字＝「〜は〜だった」が丸ごと入る長さ。ここより短いものは名前として扱う。

# 図が持ってよい語（数値・単位・部位名）。これだけで出来た文字列は複写と見なさない。
DATAISH = re.compile(r"^[0-9０-９,.，．%％\s"
                     r"a-zA-Zａ-ｚＡ-Ｚ"
                     r"年月日時分秒回本個名人隻機層枚倍度円"
                     r"メートルインチフィートポンドマイルパーセントキロ"
                     r"／/・:：〜~\-−－(（)）]+$")


# 🔴 カタカナだけで出来た語は**固有名詞**。字数が伸びるだけで節ではない。
#    「ミッションスペシャリスト」は13字あるが、そのカットの主題そのもので、
#    図がこれを書けないと何の話か分からなくなる。
KATAKANA = re.compile(r"[ァ-ヶー・]+")


def unesc(t):
    for k, v in UNESC.items():
        t = t.replace(k, v)
    return t


def norm(s):
    """比べるための正規化。読点・空白・かっこを落とす。"""
    if isinstance(s, (list, tuple)):
        s = "".join(str(x) for x in s)
    return re.sub(r"[、。，．\s「」『』（）()【】・…]", "", str(s))


def lcsub(a, b):
    """いちばん長い**連続**一致の長さ。

    🔴 部分列（飛び飛び）で測ると日本語では誤検出しかしない。助詞と常用漢字が
       どの文にも出るので、無関係なラベルが 100% 一致と判定される。
    """
    if not a or not b:
        return 0
    best = 0
    prev = [0] * (len(b) + 1)
    for ca in a:
        cur = [0] * (len(b) + 1)
        for j, cb in enumerate(b):
            if ca == cb:
                cur[j + 1] = prev[j] + 1
                if cur[j + 1] > best:
                    best = cur[j + 1]
        prev = cur
    return best


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
    return {s for s in out if s}


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

    hard = soft = 0
    for cid in sorted(bycut):
        rows = [r["text"] for r in S.SUBS.get(cid, [])]
        if not rows:
            continue
        narr = [norm(r) for r in rows]
        ex = exempt.get(cid, set())
        for layer, t in bycut[cid]:
            n = norm(t)
            if len(n) < MINLEN or DATAISH.match(t) or KATAKANA.fullmatch(n):
                continue
            # 折り返された断片も見出し扱いにする（para が行を割るため）
            is_ex = any(n in h or h in n for h in ex)
            lim = HEAD_RATIO if is_ex else BODY_RATIO
            for src, nr in zip(rows, narr):
                r = 1.0 if n in nr else lcsub(n, nr) / len(n)
                if r < lim:
                    continue
                if is_ex:
                    if n == nr:
                        hard += 1
                        print(f"  🔴 {cid} [見出し/決め所]「{t}」\n"
                              f"      ナレーション1行と**丸ごと同一**")
                    else:
                        soft += 1
                        if show_all:
                            print(f"  ・ {cid} [見出し/決め所]「{t}」 ≒ {r:.0%}「{src}」")
                else:
                    hard += 1
                    print(f"  🔴 {cid} [{layer}]「{t}」\n"
                          f"      ナレーション「{src}」と {r:.0%} 一致"
                          f"{'（そのまま含まれる）' if n in nr else ''}")
                break
    print(f"\n{'🔴 図がナレーションの複写になっている箇所あり' if hard else '✓ 複写は無い'}"
          f"（複写 {hard}件・見出しの近さ {soft}件）")
    if soft and not show_all:
        print("   （見出しの近さは --all で出る。見出しは話題を出す場所なので既定では黙る）")
    return 1 if hard else 0


if __name__ == "__main__":
    only = next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")), None)
    sys.exit(main(only, "--all" in sys.argv))
