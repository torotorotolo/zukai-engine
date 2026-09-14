# -*- coding: utf-8 -*-
"""④' の通し読みの当たりを付ける道具。
   ・カットを全部拾えているか（216になるか）を先に検算する＝道具のほうが先に間違えるため
   ・専門語の初出カットと、そのカット内に噛み砕きがあるか
   ・主語なしで始まる指示語・代名詞
"""
import re, io

P = r"C:\Users\konar\Documents\Obsidian Vault\Projects\事故検証-コロンビア号-台本第1版-20260914.md"
src = io.open(P, encoding="utf-8").read()
body = src.split("## 4. 台本", 1)[1].split("\n## 5. ", 1)[0]

cuts = []
cur = None
HDR = re.compile(r"^\*\*([a-z]{1,2}\d{2,3})\*\*\s*／\s*(.*?)\s*／\s*(.*)$")
for ln in body.splitlines():
    s = ln.strip()
    m = HDR.match(s)
    if m:
        cur = {"id": m.group(1), "pic": m.group(2), "src": m.group(3), "lines": []}
        cuts.append(cur)
        continue
    if cur is not None and s.startswith(">"):
        cur["lines"].append(s.lstrip("> ").strip())

print("カット数 %d （216なら道具は正しい）" % len(cuts))
print("字幕行 %d" % sum(len(c["lines"]) for c in cuts))

TERMS = [
    "オービタ", "外部タンク", "固体ロケットブースタ", "断熱材", "バイポッド", "RCC",
    "耐熱タイル", "再突入", "マッハ", "デブリ評価チーム", "ミッション運営チーム",
    "クレーター", "船外活動", "飛行主任", "記録装置", "逸脱の常態化",
    "逸した機会", "スペースハブ", "桁", "前のふち", "大気圏", "軌道",
    "ケネディ宇宙センター", "マーシャル宇宙飛行センター", "米戦略軍", "FREESTAR",
    "国際宇宙ステーション", "画像解析", "ロボットアーム", "耐熱", "指揮系統",
]
# 噛み砕きの合図＝「という」「とは」「＝」「呼ぶ」「である。…のこと」など
KUDAKI = re.compile(r"という|とは|と呼ぶ|のことである|＝|でできて|の略")

print("\n=== 専門語の初出 ===")
print("%-22s %-7s %-5s %s" % ("語", "初出", "回数", "初出カットに噛み砕きがあるか"))
for t in TERMS:
    hits = [c for c in cuts if any(t in l for l in c["lines"])]
    if not hits:
        print("%-22s %-7s %-5d %s" % (t, "-", 0, "（本文に出ない）"))
        continue
    first = hits[0]
    txt = "／".join(first["lines"])
    ok = "○" if KUDAKI.search(txt) else "⚠️ 無し"
    print("%-22s %-7s %-5d %s" % (t, first["id"], len(hits), ok))

print("\n=== 主語なしで始まる行（指示語が先頭）===")
DEMO = re.compile(r"^(それ|これ|そこ|ここ|その|この|あの|そう|こう|どちら|そちら|彼ら|両方)")
for c in cuts:
    for i, l in enumerate(c["lines"]):
        if i == 0 and DEMO.match(l):
            print("  %s 1行目: %s" % (c["id"], l))

print("\n=== 章の切れ目（前の章の最終カット → 次の章の先頭カット）===")
prev = None
for c in cuts:
    ch = re.match(r"^([a-z]{1,2})", c["id"]).group(1)
    if prev and prev[0] != ch:
        print("  %s 末: %s" % (prev[1]["id"], prev[1]["lines"][-1]))
        print("  %s 頭: %s" % (c["id"], c["lines"][0]))
        print("  ---")
    prev = (ch, c)
