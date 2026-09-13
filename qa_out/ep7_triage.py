# -*- coding: utf-8 -*-
"""ep7_triage.py — 79件の「読みが違う」を **①文頭の崩れ ②語の読み ③その他** に機械で仕分ける（この回かぎり）。

■ なぜ要るか
    直し方が型ごとに違う（[[reference-elevenlabs-tts]]）:
      ① **文頭の崩れ** … 書き方では直らない。`el_retake`（頭に「　、」を足して振り直す）
      ② **語の読み**   … 行の途中でも崩れる＝本文が誘発。`EL_YOMI` に入れて A/B（`el_ab_yomi`）
      ③ **Scribe の字の当て違い** … 読みは同じ。**直さない**（交信→更新／責める→攻める）
    仕分けずに全部 retake すると 79行×4テイク＝約4,900クレジットを捨てる。

■ 仕分けの規則（機械）
    - 台本の**先頭2字**が聞取の**先頭6字**のどこにも無い → ①文頭の崩れ
    - その語が**行の途中**でも崩れている行が別にある → ②語の読み
    - どちらでもない → ③（人が見る）
    ⚠️ 陽性対照＝c417-1（A/B で頭欠けを実測ずみ）が①に入ること。
    ⚠️ 陰性対照＝c304-1「交信→更新」（読みは こうしん で同じ）が①にも②にも入らないこと。

  python qa_out/ep7_triage.py
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import el_script as ES  # noqa: E402

Q = ROOT / "audio" / "el_qa"
diff = list(csv.DictReader((Q / "ep7_reading_diff.tsv").read_text(encoding="utf-8").splitlines(),
                           delimiter="\t"))
heard = {r["場面"]: r["聞こえた文"] for r in
         csv.DictReader((Q / "ep7_el_yomi.tsv").read_text(encoding="utf-8").splitlines(),
                        delimiter="\t")}
lines = {l.lid: l.text for l in ES.lines()}

# ③ 読みが同じで字だけ違うと**人が確かめた**もの（1件ずつ理由つき。ここに入れたら直さない）
SAME_READING = {
    "c304-1": "交信→更新（こうしん）",
    "c403-1": "交信→更新（こうしん）",
    "c104-1": "4便→ヨンビン（よんびん・カタカナ表記）",
    "c606-2": "便→瓶（びん）",
    "c311-2": "あいだ→間（janome が カン と読んだだけ）",
    "c314-2": "街じゅう→町中（じゅう。janome が ナカ と読んだだけ）",
    "c910-1": "国じゅう→国中（じゅう。同上）",
    "c319-3": "跡→後（あと）",
    "c903-1": "あと→その後（あと）",
    "c302-1": "あと→後（あと）",
    "c718-1": "4機→四基・1機→一基（き）",
    "c902-1": "行って→やって（おこなって／やって。どちらでも意味は同じ）",
    "c124-2": "は→が（助詞。Scribe の揺れ）",
    "c209-2": "のが→のね（Scribe の揺れ）",
    "c708-2": "減った→欠いた（Scribe の当て違い）",
}
FRONT_LOOK = 6


def front_broken(lid):
    t, h = lines[lid], heard.get(lid, "")
    return t[:2] not in h[:FRONT_LOOK]


rows = [r for r in diff if r["判定"] == "読みが違う"]
front, other = [], []
for r in rows:
    lid = r["行"]
    if lid in SAME_READING:
        continue
    (front if front_broken(lid) else other).append(lid)

print(f"「読みが違う」{len(rows)}行 → ③読みが同じ（人が確認）{len([r for r in rows if r['行'] in SAME_READING])}"
      f"／①文頭の崩れ {len(front)}／②行の途中 {len(other)}")
print(f"\n── ① 文頭の崩れ（el_retake で振り直す）{len(front)}行 ──")
for lid in front:
    print(f"  {lid:<9} 台本: {lines[lid]}")
    print(f"  {'':<9} 聞取: {heard.get(lid,'')}")
print(f"\n── ② 行の途中の崩れ（EL_YOMI の候補・A/B へ）{len(other)}行 ──")
for lid in other:
    print(f"  {lid:<9} 台本: {lines[lid]}")
    print(f"  {'':<9} 聞取: {heard.get(lid,'')}")

# 対照
ok = []
ok.append(("陽性対照 c417-1 が①に入る", "c417-1" in front))
ok.append(("陰性対照 c304-1（交信→更新）が①②に入らない",
           "c304-1" not in front and "c304-1" not in other))
print("\n── 対照 ──")
for name, v in ok:
    print(f"  {'✓' if v else '🔴'} {name}")
(Q / "ep7_triage_front.txt").write_text("\n".join(front), encoding="utf-8")
(Q / "ep7_triage_mid.txt").write_text("\n".join(other), encoding="utf-8")
print(f"\n→ {Q/'ep7_triage_front.txt'}（{len(front)}行）／{Q/'ep7_triage_mid.txt'}（{len(other)}行）")
