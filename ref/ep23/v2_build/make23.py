# -*- coding: utf-8 -*-
"""23本目④'：第2版を一気に組み直す（扱いの表 → 差し替え表 → 本組みと門番 → 台帳）＝22本目 make22.py を写した。

  python ref/ep23/v2_build/make23.py

第2版を直すときは decide23.py（係の所見の扱い・G0 の直し）を書き足して、これを回す（daihon_v2.md を手で直さない）。
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
PY = sys.executable
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')


def run(args):
    r = subprocess.run([PY] + args, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('$', ' '.join(os.path.basename(a) if a.endswith('.py') else a for a in args), '→ exit', r.returncode)
    print((r.stdout or '').rstrip()[-1500:])
    if r.stderr.strip():
        print(r.stderr.rstrip()[-1500:])
    if r.returncode != 0:
        sys.exit(r.returncode)


j = lambda *p: os.path.join(HERE, *p)  # noqa: E731
run([j('decide23.py')])
run([j('ledger23.py'), 'patches'])
r = subprocess.run([PY, j('final23.py')], cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
print((r.stdout or '') + (r.stderr or ''))
run([j('ledger23.py'), 'ledger'])
