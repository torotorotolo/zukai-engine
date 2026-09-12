# -*- coding: utf-8 -*-
"""check_script_units_test.py — 単位の門番（`check_script.py` の「原単位のまま」）の陽性対照。

    python tools/check_script_units_test.py

🔴 なぜ別ファイルか
   `check_script.py --selftest` は尺と cps の検算で、**単位の網を1件も通していない**。
   ＝「selftest が通っても本番の経路は別」 → [[feedback-selftest-must-not-reach-real-side-effects]]

🔴 2026-09-13（7本目②）に直した3つの穴。**全部この対照が見つけた。**

  (a) **「華氏」「°F」が網に無かった。**9.11 は鉄と火災＝温度の話をする回。
  (b) **`met.search(body)` がカット全体を免除していた。**
      「全長1,200メートルの橋で、船は毎時8ノット」が素通りする（t03）。
      → 原単位1つずつに、対応する換算語が**前後60字**にあるかを見る形に変えた。
  (c) 🔴🔴 **「華氏1,000度」が2回続けて鳴らなかった。**原因が2つ重なっていた:
      ・日本語は**単位が数の前**に来る（`[0-9]…(華氏)` の形では当たらない）
      ・換算語に「度」を入れていたので、**「華氏1,000度」の「度」が自分に当たって免除**された
      → [[feedback-verify-your-own-instrument]]（道具が全部0件のときは道具を疑う）
"""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_script as C                                       # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

# (ID, 説明, 本文, 鳴るべきか)
CASES = [
    ("t01", "華氏だけ", "鋼材は華氏1,000度まで上がりました。", True),
    ("t02", "華氏＋摂氏", "鋼材は摂氏538度、華氏1,000度まで上がりました。", False),
    ("t03", "離れたメートルで免除される穴",
     "全長1,200メートルの橋です。" + "あ" * 90 + "船は毎時8ノットで進みました。", True),
    ("t04", "近くに換算あり", "船は毎時8ノット、時速約15キロで進みました。", False),
    ("t05", "フィート単独", "高さは1,368フィートありました。", True),
    ("t06", "フィート＋メートル", "高さは417メートル、1,368フィートありました。", False),
    ("t07", "陰性：単位が無い", "その日の空はよく晴れていました。", False),
    ("t08", "°F（数が前）", "炉内は1832°Fに達しました。", True),
    ("t09", "ガロン単独", "燃料は10,000ガロン積んでいました。", True),
    ("t10", "ガロン＋リットル", "燃料は約43,150リットル、10,000ガロン積んでいました。", False),
    ("t11", "℃で受ける", "鋼材は538℃、華氏1,000度まで上がりました。", False),
    ("t12", "刃渡り4インチ単独", "刃渡り4インチ未満なら通せました。", True),
    ("t13", "刃渡り4インチ＋センチ", "刃渡り10.2センチ、4インチ未満なら通せました。", False),
]


def main():
    lines = ["## 4. 台本", ""]
    for cid, _, body, _ in CASES:
        lines += [f"**{cid}**／p01／図", "> " + body, ""]
    lines += ["## 5. おわり"]
    cuts = C.parse("\n".join(lines))
    if len(cuts) != len(CASES):
        print(f"🔴 台本を読めていない（{len(cuts)}/{len(CASES)}カット）。CUT_RE が変わった？")
        return 1

    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        C.report(cuts)
    finally:
        sys.stdout = old
    errs = [l for l in buf.getvalue().splitlines() if "単位が原文のまま" in l]

    ok = True
    for cid, lab, _, want in CASES:
        got = any(f" {cid} " in l for l in errs)
        if got != want:
            ok = False
        print(f"  {'✅' if got == want else '🔴ちがう'} {cid} {lab:<26} "
              f"期待={'鳴る' if want else '鳴らない'} 実際={'鳴った' if got else '鳴らない'}")
    want_n = sum(1 for c in CASES if c[3])
    print(f"\n鳴った件数 {len(errs)} ／ 鳴るはず {want_n}")
    print("陽性対照:", "PASS" if ok else "🔴FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
