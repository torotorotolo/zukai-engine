# -*- coding: utf-8 -*-
"""15本目④：門番をまとめて回す（tools/ は1文字も変えない）。
    python ref/ep15/v1_build/gates15.py [台本.md]      （既定 ref/ep15/daihon_v1.md）
出力＝ref/ep15/v1_build/out/*.txt。最後に終了コードの一覧を出す。
聞き役を知る実行は、14本目④'（ref/ep14/v2_build/final.sh）と同じ2点だけを読み込んだ中で差し替える：
  ① `Q: ` を字数から外す ②「？」「！」で終わる聞き役の行を文の終わりと見る（行末に「、」を足して読ませる）
"""
import subprocess, sys
from pathlib import Path
ROOT = Path("C:/Users/konar/Desktop/zukai-engine")
B = ROOT / "ref/ep15/v1_build"
O = B / "out"
O.mkdir(exist_ok=True)
MD = sys.argv[1] if len(sys.argv) > 1 else "ref/ep15/daihon_v1.md"
ENV = {"PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
QAWARE = r'''
import sys, re
sys.path.insert(0, 'tools'); import check_script as cs
_c = cs.clean
cs.clean = lambda l: re.sub(r'^Q:\s', '', _c(l))
src = open(sys.argv[1], encoding='utf-8').read()
src = re.sub(r'^(> Q: .*[？！])$', r'\1、', src, flags=re.M)
sys.exit(1 if cs.report(cs.parse(src)) else 0)
'''
RUNS = [
    ("pages", [sys.executable, str(B / "make_pages.py")]),
    ("refcheck", [sys.executable, "tools/check_script.py", "--refcheck"]),
    ("cs", [sys.executable, "tools/check_script.py", MD]),
    ("csq", [sys.executable, "-c", QAWARE, MD]),
    ("cf", [sys.executable, "tools/check_facts.py", MD, "ref/ep15/src/ep15_pages.txt"]),
    ("mech", [sys.executable, str(B / "mech15.py"), MD, "ref/ep14/v2_build/titles.json"]),
]
import os
env = dict(os.environ, **ENV)
rc = []
for name, cmd in RUNS:
    p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    (O / f"{name}.txt").write_text(p.stdout + ("\n[stderr]\n" + p.stderr if p.stderr.strip() else ""), encoding="utf-8")
    rc.append(f"{name} exit={p.returncode}")
(O / "rc.txt").write_text("\n".join(rc) + "\n", encoding="utf-8")
print("\n".join(rc))
