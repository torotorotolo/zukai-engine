# -*- coding: utf-8 -*-
"""17本目④'：第2版を機械で数える（読むだけ）。④の道具 ref/ep17/v1_build/m17.py（§1〜§8）をそのまま使い、
聞き役の役割表との1行ずつの突き合わせ（§6b）を足した。m17 の §6 の「役割」は文の形から推した値（？＝質問・「つまり」＝まとめ）で、
④'では人（直す係）が決めた役割表 roles.tsv の値を正とする。
    python ref/ep17/v2_build/mech17.py ref/ep17/daihon_v2.md [ref/ep17/v2_build/roles.tsv]
§6b で見るもの：
  E  台本の聞き役の行（`> Q: `）と roles.tsv の行が、順番・カット・文で1行ずつ一致しない
  E  役割が「質問／まとめ／反応」以外
  E  聞き役に数字（m17 と同じ正規表現）
  E  役割表で「まとめ」の行の次の語りが「そう。」で始まらない（ルール §4-15）
  W  聞き役の行が20字超／「質問」なのに？で終わらない／「まとめ」「反応」なのに？で終わる
  W  役割の割合が目安の外（質問5割〈40〜60%〉／まとめ2〜3割〈20〜30%〉／反応2割まで）
終了コード 0＝E 0件 / 1＝E あり
"""
import re, sys
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
sys.path.insert(0, str(S.parent / "v1_build"))
import m17  # noqa: E402

path = sys.argv[1]
roles_path = Path(sys.argv[2]) if len(sys.argv) > 2 else S / "roles.tsv"
cuts = m17.parse(open(path, encoding="utf-8").read())
print(m17.report(cuts))

print("## §6b 聞き役の役割表との突き合わせ（roles.tsv＝人が決めた役割）")
E, W = [], []
ids = list(cuts)
script_q = []   # (cid, 文, 次の語り)
for k, i in enumerate(ids):
    c = cuts[i]
    for j, b in enumerate(c["bare"]):
        if c["q"][j]:
            nxt = c["bare"][j + 1] if j + 1 < len(c["bare"]) else (cuts[ids[k + 1]]["bare"][0] if k + 1 < len(ids) else "")
            script_q.append((i, b.strip(), nxt))
rows = []
if roles_path.exists():
    for ln in roles_path.read_text(encoding="utf-8").splitlines():
        if not ln.strip() or ln.startswith("#") or ln.startswith("cid\t"):
            continue
        p = ln.split("\t")
        rows.append((p[0].strip(), p[1].strip() if len(p) > 1 else "", p[2].strip() if len(p) > 2 else ""))
else:
    E.append(f"役割表が無い: {roles_path}")
if len(rows) != len(script_q):
    E.append(f"行の数が違う：台本 {len(script_q)} ／ 役割表 {len(rows)}")
for n, (sq, rw) in enumerate(zip(script_q, rows)):
    if sq[0] != rw[0] or sq[1] != rw[2]:
        E.append(f"{n + 1}行目が一致しない：台本 {sq[0]}「{sq[1]}」／ 表 {rw[0]}「{rw[2]}」")
        break
# 役割は（カット・文）の組で引く＝1行ずれても、あとの行の判定が連鎖して崩れない
pool = {}
for cid, role, txt in rows:
    pool.setdefault((cid, txt), []).append(role)
used = Counter()
cnt = Counter()
for cid, txt, nxt in script_q:
    got = pool.get((cid, txt), [])
    if used[(cid, txt)] >= len(got):
        E.append(f"{cid} 台本の聞き役が役割表に無い「{txt}」")
        continue
    role = got[used[(cid, txt)]]
    used[(cid, txt)] += 1
    cnt[role] += 1
    if role not in ("質問", "まとめ", "反応"):
        E.append(f"{cid} 役割が読めない「{role}」")
    if m17.NUM_IN_Q.search(txt):
        E.append(f"{cid} 聞き役に数字「{txt}」")
    if role == "まとめ" and not nxt.startswith("そう。"):
        E.append(f"{cid} まとめの次の語りが「そう。」で始まらない：「{nxt[:16]}」")
    if len(txt) > 20:
        W.append(f"{cid} 聞き役が20字超（{len(txt)}字）「{txt}」")
    if role == "質問" and not txt.endswith("？"):
        W.append(f"{cid} 質問なのに？で終わらない「{txt}」")
    if role in ("まとめ", "反応") and txt.endswith("？"):
        W.append(f"{cid} {role}なのに？で終わる「{txt}」")
for k, v in pool.items():
    if used[k] < len(v):
        E.append(f"{k[0]} 役割表にあって台本に無い聞き役「{k[1]}」")
tot = sum(cnt.values()) or 1
pct = {k: round(100 * cnt[k] / tot) for k in ("質問", "まとめ", "反応")}
print(f"役割（表）{dict(cnt)}＝質問 {pct['質問']}%・まとめ {pct['まとめ']}%・反応 {pct['反応']}%（目安＝質問5割／まとめ2〜3割／反応2割まで）")
if not 40 <= pct["質問"] <= 60:
    W.append(f"質問 {pct['質問']}%＝目安（5割）の外")
if not 20 <= pct["まとめ"] <= 30:
    W.append(f"まとめ {pct['まとめ']}%＝目安（2〜3割）の外")
if pct["反応"] > 20:
    W.append(f"反応 {pct['反応']}%＝2割を超える")
for e in E:
    print("🔴 E", e)
for w in W:
    print("⚠️ W", w)
print(f"E {len(E)}件 / W {len(W)}件")
sys.exit(1 if E else 0)
