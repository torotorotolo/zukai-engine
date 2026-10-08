# -*- coding: utf-8 -*-
"""20本目④'：第2版を組んで、門番をまとめて回す（出力は v2_build/gates.md・各門番の終了コードつき）。

  python ref/ep20/v2_build/final20.py            # patches20.json で組み直す → 門番 → 対照表
  python ref/ep20/v2_build/final20.py --nobuild  # 組まずに門番だけ

回すもの（順番どおり）：
  1 build20_v2.py patches20.json         第2版（第1版の md5 を前後で比べる）
  2 roles20_v2.py daihon_v2.md roles.tsv 聞き役の役割表（roles_map.json から）
  3 m20.py daihon_v2.md --roles …        字数・尺の3通り・冒頭の秒・行の形・聞き役（check_listener.judge）・写真の割合
  4 quotes20.py daihon_v2.md             出典の欄の引用を資料の字に
  5 tools/check_script.py daihon_v2.md   形の門番（E は既知の件だけか）
  6 tools/check_script_diff.py v1 v2     🔧 の印と差分の一致・欠番
  7 count_text_screens.py --gate --ids   文字だけの画面
  8 make_diff20.py                       第1版→第2版の対照表
"""
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
PY = sys.executable
V1 = os.path.join(EP, 'daihon_v1.md')
V2 = os.path.join(EP, 'daihon_v2.md')
ROLES = os.path.join(HERE, 'roles.tsv')
CTS = r'C:/Users/konar/Documents/Obsidian Vault/Resources/事故検証ch-案C見本/count_text_screens.py'
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')

steps = []
if '--nobuild' not in sys.argv:
    steps.append(('build', [PY, os.path.join(HERE, 'build20_v2.py'), os.path.join(HERE, 'patches20.json')]))
steps += [
    ('roles', [PY, os.path.join(HERE, 'roles20_v2.py'), V2, ROLES]),
    ('m20', [PY, os.path.join(EP, 'v1_build', 'm20.py'), V2, '--roles', ROLES]),
    ('quotes20', [PY, os.path.join(EP, 'v1_build', 'quotes20.py'), V2, '--out', os.path.join(HERE, 'quotes20_v2.tsv')]),
    ('check_script', [PY, os.path.join(REPO, 'tools', 'check_script.py'), V2]),
    ('check_script_diff', [PY, os.path.join(REPO, 'tools', 'check_script_diff.py'), V1, V2]),
    ('count_text_screens', [PY, CTS, V2, '--gate', '--ids']),
    ('make_diff', [PY, os.path.join(HERE, 'make_diff20.py')]),
]
out = ['# 20本目 第2版の門番（final20.py の出力・手で直さない）', '']
summary = []
for name, cmd in steps:
    r = subprocess.run(cmd, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    txt = (r.stdout or '') + (r.stderr or '')
    out += ['## %s（exit=%d）' % (name, r.returncode), '```', txt.rstrip(), '```', '']
    summary.append('%s=%d' % (name, r.returncode))
    if name == 'build' and r.returncode != 0:
        out.append('🔴 組めなかったので止めた')
        break
open(os.path.join(HERE, 'gates.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('  '.join(summary))
print('→', os.path.join(HERE, 'gates.md'))
