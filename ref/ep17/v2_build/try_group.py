# -*- coding: utf-8 -*-
"""17本目④'：直す係が自分の差し替え表だけで第2版を試しに組み、門番を回す（daihon_v2.md は書かない・読むだけ）。
    python ref/ep17/v2_build/try_group.py G3 <置き場のフォルダ>
やること：
  1. build_v2.py --only G3 --out <置き場>/try_G3.md（ほかの係の書きかけで止まらない）
  2. 役割表＝自分の章は roles_G3.tsv・ほかの章は第1版の表（v1_build/roles.tsv）をつないで <置き場>/roles_try_G3.tsv
  3. mech17.py（§6b の突き合わせ・20字・まとめの次の「そう。」）と tools/check_script.py（形の E）を回す
  4. 自分の章の「句読点なし字」の増減（第1版との差）と、決めごと §1 の上限を並べて出す
終了コード 0＝E なし・上限の内 / 1＝E あり・上限の外（尺の E は既知の誤りとして数えない）
"""
import os, re, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
ROOT = S.parents[2]
sys.path.insert(0, str(S.parent / "v1_build"))
import m17  # noqa: E402

G = sys.argv[1]
OUTD = Path(sys.argv[2]); OUTD.mkdir(parents=True, exist_ok=True)
CH = {"G1": ("c1", "c2"), "G2": ("c3", "c4"), "G3": ("c5", "c6"), "G4": ("c7", "c8"), "G5": ("c9", "ca"), "G6": ("cb",)}[G]
LIMIT = {"G1": 60, "G2": -10, "G3": -10, "G4": 10, "G5": -30, "G6": 50}[G]   # decisions.md §1 と同じ（句読点なし字の正味の増減の上限）
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
bad = 0

try_md = OUTD / f"try_{G}.md"
p = subprocess.run([sys.executable, str(S / "build_v2.py"), "--only", G, "--out", str(try_md)], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
print("== build_v2 --only", G, "exit", p.returncode); print(p.stdout.strip())
if p.returncode:
    sys.exit(1)

# 役割表をつなぐ
v1rows = [l.split("\t") for l in (S.parent / "v1_build/roles.tsv").read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
mine = S / f"roles_{G}.tsv"
myrows = [l.split("\t") for l in mine.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#") and not l.startswith("cid\t")] if mine.exists() else []
if not mine.exists():
    print(f"⚠️ {mine.name} が無い＝自分の章の聞き役の行を全部書く（cid<TAB>役割<TAB>文）"); bad = 1
rows = [r for r in v1rows if r[0][:2] not in CH] + myrows
order = {c: k for k, c in enumerate(m17.parse(try_md.read_text(encoding="utf-8")))}
rows.sort(key=lambda r: order.get(r[0], 10 ** 6))   # 台本の順（同じカットの中は書いた順のまま＝sort は安定）
rt = OUTD / f"roles_try_{G}.tsv"
rt.write_text("\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")

p = subprocess.run([sys.executable, str(S / "mech17.py"), str(try_md), str(rt)], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
(OUTD / f"mech_try_{G}.txt").write_text(p.stdout + p.stderr, encoding="utf-8")
out = p.stdout
print("== mech17（全体。聞き役の割合はほかの章が第1版のままの値）exit", p.returncode)
for ln in out.splitlines():
    if ln.startswith(("🔴", "⚠️", "E ", "役割（表）", "聞き役の行", "最初の1回", "1行41字超", "1カット1〜3行の外", "   20字超", "   ★が最後の行でない", "## §5", "① カット")) or ln.startswith("| `" + CH[0]) or (len(CH) > 1 and ln.startswith("| `" + CH[1])):
        print(ln)
if p.returncode:
    bad = 1

p = subprocess.run([sys.executable, "tools/check_script.py", str(try_md)], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8")
(OUTD / f"cs_try_{G}.txt").write_text(p.stdout + p.stderr, encoding="utf-8")
es = [l for l in p.stdout.splitlines() if l.startswith("🔴 E") and "尺" not in l]
print("== check_script の E（尺の既知の E を除く）", len(es))
for l in es:
    print(l)
if es:
    bad = 1

a = m17.parse((S.parent / "daihon_v1.md").read_text(encoding="utf-8"))
b = m17.parse(try_md.read_text(encoding="utf-8"))
d = sum(b[c]["np"] for c in b if c[:2] in CH) - sum(a[c]["np"] for c in a if c[:2] in CH)
d_open = sum(b[c]["np"] for c in list(b)[:6]) - sum(a[c]["np"] for c in list(a)[:6])
print(f"== 句読点なし字の正味の増減（{'・'.join(CH)}）：{d:+d}（上限 {LIMIT:+d}）" + (f"／冒頭 c101〜c106：{d_open:+d}（上限 +35）" if G == "G1" else ""))
if d > LIMIT or (G == "G1" and d_open > 35):
    print("🔴 上限の外"); bad = 1
t = 0.0
for c in list(b)[:6]:
    t += b[c]["np"] / m17.CPM * 60
    if c == "c105":
        print(f"== 物証 c105 の終わり（② の式）{t:.1f}秒（46秒より前）")
sys.exit(bad)
