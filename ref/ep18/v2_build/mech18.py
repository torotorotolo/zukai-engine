# -*- coding: utf-8 -*-
"""18本目④'：台本を機械で数える（読むだけ）。④の数え m18.py（尺・章ごと・形・冒頭の秒・聞き役〈tools/check_listener.judge〉・
文字だけの画面）をそのまま回し、17本目 mech17.py の §6b（人が決めた役割表と本文を1行ずつ突き合わせる）を足した。
    python ref/ep18/v2_build/mech18.py ref/ep18/daihon_v2.md [ref/ep18/v2_build/roles.tsv]
§6b で見るもの：
  E  台本の聞き役の行（`> Q: `）と roles.tsv の行が、順番・カット・文で1行ずつ一致しない
  E  役割が「質問／まとめ／反応」以外
  E  役割表で「まとめ」の行の次の語りが「そう。」で始まらない（ルール §4-15）
  W  聞き役の行が20字超／「質問」なのに？で終わらない／「まとめ」「反応」なのに？で終わる
終了コード 0＝E 0件 / 1＝E あり
"""
import sys
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
sys.path.insert(0, str(S))
import m18  # noqa: E402
CS, speaker = m18.CS, m18.speaker

path = sys.argv[1]
roles_path = Path(sys.argv[2]) if len(sys.argv) > 2 else S / "roles.tsv"
print("## §1〜§5 m18.py（④の数え・聞き役は tools/check_listener.judge）")
n_e = m18.main(path, str(roles_path))

print("## §6b 聞き役の役割表との突き合わせ（roles.tsv＝人が決めた役割）")
E, W = [], []
flat = []
for cid, _, ls in CS.parse(open(path, encoding="utf-8").read()):
    for raw in ls:
        who = speaker.split(raw)[0]
        flat.append((cid, who, speaker.bare(CS.STAR_RE.sub("", raw).replace("**", "").strip())))
script_q = []
for k, (cid, who, b) in enumerate(flat):
    if who == speaker.WHO_Q:
        nxt = next((x[2] for x in flat[k + 1:] if x[1] != speaker.WHO_Q), "")
        script_q.append((cid, b, nxt))
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
# 役割は（カット・文）の組で引く＝1行ずれても、あとの行の判定が連鎖して崩れない（17本目 mech17.py と同じ）
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
print(f"役割（表）{dict(cnt)}")
for e in E:
    print("🔴 E", e)
for w in W:
    print("⚠️ W", w)
print(f"§6b E {len(E)}件 / W {len(W)}件")
sys.exit(1 if (E or n_e) else 0)
