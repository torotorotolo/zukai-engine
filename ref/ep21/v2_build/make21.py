# -*- coding: utf-8 -*-
"""21本目④'：第2版を一気に組み直す（扱いの表 → G0 の直し → 差し替え表 → 試し組み → 「報せ」の行ごとの直し → 本組みと門番 → 台帳）。

  python ref/ep21/v2_build/make21.py

第2版を直すときは decide21.py（係の所見の扱い）か gen_g0.py（G0 の直し）を書き足して、これを回す（daihon_v2.md を手で直さない）。
"""
import os
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
PY = sys.executable
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
TMP = os.path.join(tempfile.gettempdir(), 'ep21_v2pre.md')


def run(args):
    r = subprocess.run([PY] + args, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('$', ' '.join(os.path.basename(a) if a.endswith('.py') else a for a in args), '→ exit', r.returncode)
    print((r.stdout or '').rstrip()[-1500:])
    if r.stderr.strip():
        print(r.stderr.rstrip()[-1500:])
    if r.returncode != 0:
        sys.exit(r.returncode)


j = lambda *p: os.path.join(HERE, *p)  # noqa: E731
run([j('decide21.py')])
run([j('gen_g0.py')])
run([j('ledger21.py'), 'patches', '--nomech'])
run([j('build21_v2.py'), j('patches21.json'), '--out', TMP])
run([j('gen_g0.py'), '--mech', TMP])
run([j('ledger21.py'), 'patches'])
r = subprocess.run([PY, j('final21.py')], cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
print((r.stdout or '') + (r.stderr or ''))
run([j('ledger21.py'), 'ledger'])
