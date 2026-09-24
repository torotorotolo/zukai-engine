# -*- coding: utf-8 -*-
"""13本目 ⑤a：tools/el_script.py の EL_YOMI（12本目の216件）を**空の13本目の枠**に差し替える（2026-09-24・1回だけ使う）。

  python qa_out/ep13_yomi_reset.py

旧版は git 履歴（`git show d95efed:tools/el_script.py`）に全部残る。
切る範囲＝「# ── EL_YOMI（9本目 テネリフェ）」の行から、EL_YOMI の閉じ括弧 `}` の行まで。
差し替えたあと el_script を import し直して、門番（_gate）が通ることまで見る。
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
F = ROOT / "tools" / "el_script.py"

NEW = '''# ── EL_YOMI（13本目 トルコ航空981便）───────────────────────────────
# 🔴🔴 **12本目（キャッスル・ブラボー）の216件を空にした**（2026-09-24・⑤a）。旧版＝`git show d95efed:tools/el_script.py`。
# 🔴🔴 **数は焼く前にかなで固定する**（ルール統合版 5a-6）。聞取（Scribe）は数の誤読を正しい字で書き戻すので、
#    数は「焼いて崩れてから直す」道が最初から無い。⭐ かなで送ると Scribe は聞こえた音を書く＝読みが測れる。
#    書き方＝12本目の試写を通った形（ひらがな・数と助数詞をまとめて1語）。読みの出典＝台本第2版 §6-1〜§6-3。
# 🔴 助詞の「に」「は」の直後に、に・は で始まる数を置かない。**空白で切っても化けた**（12本目「住民 にひゃく…」
#    →『住民に百三十九人』）＝その所は**漢数字**で送る（ルール 5a-20）。
# ⚠️ 数以外の語（固有名詞など）は**焼く前に埋めない**。焼いて聞取で当たってから、A/B で確かめて入れる。
EL_YOMI = {
}
'''


def main():
    src = F.read_text(encoding="utf-8")
    a = src.index("# ── EL_YOMI（9本目 テネリフェ）")
    s = src.index("\nEL_YOMI = {\n", a)
    b = src.index("\n}\n", s) + 3
    tail = src[b:]
    assert tail.lstrip().startswith("# 🔴 「三豊」"), f"閉じ括弧の直後が想定と違う: {tail[:40]!r}"
    old_n = src[s:b].count('": "')
    F.write_text(src[:a] + NEW + tail, encoding="utf-8")
    print(f"差し替えた: EL_YOMI {old_n}件（12本目）→ 0件（13本目の枠）")
    sys.path.insert(0, str(ROOT / "tools"))
    import el_script as ES
    print(f"import ✓ SLUG={ES.SLUG} EL_YOMI={len(ES.EL_YOMI)}件 CRITICAL_EP={ES.CRITICAL_EP} 行={len(ES.lines())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
