# -*- coding: utf-8 -*-
"""話者の印（聞き役 `Q: `）を1か所で扱う（2026-09-25・14本目⑤a 新設）。

なぜ要るか
  14本目から「最小限の聞き役」を入れた（ルール §4-15）。台本では聞き役の行の頭に `Q: `
  （半角 Q＋半角コロン＋半角空白1つ）を付ける＝md は `> Q: 船長たちは？`。
  **印は音にも字幕にも出さない**。ところが台本の文は何本もの道具を通る
  （check_script の字数・行末の規則／el_script.md_vs_script／check_subwrap の突き合わせ／
  fontmetrics の字幅／aq_build の合成）。道具ごとに正規表現を書くと、どれか1本が
  外し忘れて**字幕に `Q:` が出る・字数に3字足される**。だから外し方はここ1か所に置く。

決まり
  - 印は `narration.SCRIPT` の文にも**付けたまま**持つ（話者の正本）。外すのは使う側がここを通して
  - `narration.json` の字幕は外した文（text）と話者（who＝"q"。語りは欄を書かない）を持つ
  - 13本目までの台本には印が無い＝どの関数も素通し（結果は1字も変わらない）
"""
import re

Q_MARK = "Q: "
Q_RE = re.compile(r"^Q:\s")          # `> ` を外したあとの行頭（ルール §4-15 の `^>\s?Q:\s(.+)$` と同じ）
WHO_Q = "q"                          # narration.json の字幕の who（聞き役）


def is_q(line):
    """聞き役の行か（`> ` を外したあとの文で判定）。"""
    return bool(Q_RE.match(line.strip()))


def bare(line):
    """印を外した文（音と字幕になる文）。印が無ければそのまま。"""
    return Q_RE.sub("", line.strip(), count=1)


def split(line):
    """(who, 文)。who は聞き役なら "q"・語りなら None。"""
    return (WHO_Q if is_q(line) else None), bare(line)


def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %s %-24s 期待 %-16r 実際 %r" % ("OK " if good else "🔴NG", name, want, got))

    chk("聞き役を拾う", is_q("Q: 船長たちは？"), True)
    chk("前後の空白があっても拾う", is_q("  Q: 船長たちは？"), True)
    chk("語りは拾わない", is_q("船長たちは、先に船を離れた。"), False)
    chk("文中の Q: は拾わない", is_q("記号 Q: は印"), False)
    chk("全角のＱは印でない", is_q("Ｑ： 船長たちは？"), False)
    chk("印を外す", bare("Q: 船長たちは？"), "船長たちは？")
    chk("語りはそのまま", bare("9時50分の放送。"), "9時50分の放送。")
    chk("外すのは頭の1つだけ", bare("Q: Q: 二重"), "Q: 二重")
    chk("split 聞き役", split("Q: つまり？"), ("q", "つまり？"))
    chk("split 語り", split("そう。"), (None, "そう。"))
    print("speaker selftest:", "PASS" if ok else "🔴FAIL")
    return ok


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(0 if selftest() else 1)
