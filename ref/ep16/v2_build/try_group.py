# -*- coding: utf-8 -*-
"""16本目④'：直す係が自分の差し替え表だけで試しに組み、門番まで回す（読むだけ・daihon_v2.md は書かない）。
    python ref/ep16/v2_build/try_group.py G3
  1 build_v2.py --only G3 --out out/try_G3.md（自分の v2_cuts_G3.txt だけ当てる）
  2 役割表＝自分の roles_G3.tsv＋ほかの章は第1版の表（v1_build/roles.tsv）→ out/roles_try_G3.tsv
  3 check_script（形の検査。🔴 尺の E は既知の誤り＝無視してよい）・check_facts・mech16・count_text_screens --gate
  4 章ごとの句読点なし字数を第1版と比べる（自分の章の増減）
出力は out/try_G3_*.txt に全部落とし、画面には要点だけ出す。
"""
import os, re, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[3]
B = ROOT / "ref/ep16/v2_build"
O = B / "out"
O.mkdir(exist_ok=True)
G = sys.argv[1]
CH = {"G1": ("c1", "c2"), "G2": ("c3", "c4"), "G3": ("c5", "c6"), "G4": ("c7", "c8"), "G5": ("c9", "ca"), "G6": ("cb",)}[G]
env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
CTS = "C:/Users/konar/Documents/Obsidian Vault/Resources/事故検証ch-案C見本/count_text_screens.py"


def run(cmd, tag):
    p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = p.stdout + ("\n[stderr]\n" + p.stderr if p.stderr.strip() else "")
    (O / f"try_{G}_{tag}.txt").write_text(out, encoding="utf-8")
    return p.returncode, out


md = O / f"try_{G}.md"
rc, out = run([sys.executable, str(B / "build_v2.py"), "--only", G, "--out", str(md)], "build")
print("build exit=%d" % rc)
print(out.strip())
if rc:
    sys.exit(2)
v1rows = [l for l in (ROOT / "ref/ep16/v1_build/roles.tsv").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
mine = B / f"roles_{G}.tsv"
my = [l for l in mine.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")] if mine.exists() else []
if not my:
    print("⚠️ roles_%s.tsv が無い＝自分の章も第1版の表で数える" % G)
    my = [l for l in v1rows if l.split("\t")[0][:2] in CH]
rows = [l for l in v1rows if l.split("\t")[0][:2] not in CH] + [l for l in my if l.split("\t")[0][:2] in CH]
rp = O / f"roles_try_{G}.tsv"
rp.write_text("\n".join(rows) + "\n", encoding="utf-8")

rc, out = run([sys.executable, "tools/check_script.py", str(md)], "cs")
print("\n[check_script exit=%d]（尺の E は既知の誤り）" % rc)
print("\n".join(l for l in out.splitlines() if l.startswith(("🔴", "⚠️", "E ")) or " E " in l[:6]))
rc, out = run([sys.executable, "tools/check_facts.py", str(md), "ref/ep16/src/ep16_pages.txt"], "cf")
print("\n[check_facts exit=%d]" % rc)
print("\n".join(l for l in out.splitlines() if l.startswith(("NG", "決め所", "数字", "   ")) or "当たらない" in l))
rc, out = run([sys.executable, str(B / "mech16.py"), str(md), "--roles", str(rp)], "mech")
print("\n[mech16 exit=%d]" % rc)
keep = False
for l in out.splitlines():
    if l.startswith("## "):
        keep = l.split()[1] in ("3", "6", "7", "10", "11")
        if keep:
            print(l)
        continue
    if keep or "ゆっくりの式" in l:
        print(l)
rc, out = run([sys.executable, CTS, str(md), "--gate"], "cts")
print("\n[count_text_screens exit=%d]" % rc)
print(out.strip()[-400:])

# 章ごとの字（第1版と比べる）
sys.path.insert(0, str(ROOT / "tools"))
os.chdir(ROOT)
import check_script as cs  # noqa: E402
NP = set("、。？！「」（）・")
npl = lambda s: sum(1 for ch in s if ch not in NP)  # noqa: E731


def per_ch(path):
    d = {}
    for cid, _, ls in cs.parse(Path(path).read_text(encoding="utf-8")):
        d[cid[:2]] = d.get(cid[:2], 0) + sum(npl(cs.clean(l)) for l in ls)
    return d


a, b = per_ch(ROOT / "ref/ep16/daihon_v1.md"), per_ch(md)
print("\n[句読点なしの字・第1版→試し組み]")
for k in CH:
    print(f"  {k}: {a.get(k, 0)} → {b.get(k, 0)}（{b.get(k, 0) - a.get(k, 0):+d}）")
print("  全体: %d → %d（%+d）" % (sum(a.values()), sum(b.values()), sum(b.values()) - sum(a.values())))
