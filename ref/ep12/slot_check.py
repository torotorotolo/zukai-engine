# -*- coding: utf-8 -*-
"""台本が要求している「実写の欄」を数え、②の在庫と突き合わせる（12本目）。

`ref/ep11/slot_check.py` を写して直した（2026-09-23 ⑤b-2）。**台本の書き方が違う**：
  11本目 `**c101** ／ 実写 ice_icicle ／ …`（欄の名が 実写 のすぐ後ろ）
  12本目 `**c104** 🔧 ／ 実写 NARA きのこ雲の空撮（fireball） ／ …`（欄は**説明の末尾の括弧**）
         欄の括弧が無い行は、置き場（DOE映像／4K切り出し／記録映画）を欄にする。

🔴 記憶 feedback-inventory-is-not-usable-material＝候補N点は在庫ではない。
🔴 **PATH は台本の版を指す**（11本目は第1版を読んだまま⑤bまで来た＝§0b）。
"""
import collections
import re
import sys

PATH = ("C:/Users/konar/Documents/Obsidian Vault/Projects/"
        "事故検証-キャッスルブラボー-台本第2版-20260923.md")

# ②の実測（`ref/ep12/materials.md` §7・台本第2版 §7）。欄名 → 候補点数
#   ⚠️ NARA の51点は**題名で**仕分けた数（絵はまだ見ていない＝⑤b-2 でシートを見て直す）
STOCK = {
    "fireball": 9, "device": 4, "decon": 13, "fallout": 10, "base": 6,
    "rongelap": 5, "suits": 3, "damage": 2, "other_shots": 8, "japan": 2,
    "official": 1,
    # 動く映像は「点」ではなく秒で足りるかを見る（`footage.py --check`）。ここは欄の数だけ
    "DOE映像": 8, "4K切り出し": 6, "記録映画": 3,
}

CUT = re.compile(r'^\*\*(c\d{3})\*\*[^／]*／\s*実写\s+(.*?)\s*／')
# 欄は括弧の中の英小文字の語（`（艦上から・fireball）`・`（base・副題は…）` のように他の語と同居する）
PAREN = re.compile(r'（([^（）]*)）')
WORD = re.compile(r'[a-z_]{3,}')


def main():
    on = False
    used = collections.Counter()
    where = collections.defaultdict(list)
    unknown = []
    # 🔴 どの版を読んだかを必ず出す＝記憶 feedback-check-version-before-inspecting
    print("読んだ台本: %s" % PATH.rsplit("/", 1)[1])
    for raw in open(PATH, encoding="utf-8"):
        line = raw.rstrip()
        if line.startswith("## 4. 台本"):
            on = True
            continue
        if on and re.match(r'^## \d', line):
            break
        if not on:
            continue
        m = CUT.match(line)
        if not m:
            continue
        cid, rest = m.groups()
        src = re.match(r'[^\s（]+', rest).group(0)         # NARA／Commons／DOE映像／4K切り出し／記録映画
        words = [w for g in PAREN.findall(rest) for w in WORD.findall(g) if w in STOCK]
        col = words[-1] if words else src
        if col not in STOCK:
            unknown.append((cid, col))
            continue
        used[col] += 1
        where[col].append(cid)

    print("== 台本が要求する枚数 vs ②の候補（同じ欄から引くもの）")
    print("  %-12s %5s %5s  %s" % ("欄", "要求", "候補", "判定"))
    short = 0
    for col in sorted(STOCK, key=lambda k: -used[k]):
        need, have = used[col], STOCK[col]
        if need == 0:
            continue
        ok = "OK" if need <= have else "🔴 不足 %d" % (need - have)
        short += max(0, need - have)
        print("  %-12s %5d %5d  %s  %s" % (col, need, have, ok, " ".join(where[col])))
    print("\n  合計 要求 %d / 🔴 不足の合計 %d" % (sum(used.values()), short))
    if unknown:
        # 🔴 数えられないスロットは「不足0」に見える＝黙った合格。ここで止める。
        print("\n== 🔴 E ②の欄に無いスロット（STOCK に足すまで枚数を数えられていない）")
        for cid, s in unknown:
            print("  %s %s" % (cid, s))
        return 1
    return 1 if short else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
