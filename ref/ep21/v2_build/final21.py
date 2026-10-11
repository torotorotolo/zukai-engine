# -*- coding: utf-8 -*-
"""21本目④'：第2版を組んで、門番をまとめて回す（出力は v2_build/gates.md・各門番の終了コードつき・20本目 final20.py を写した）。

  python ref/ep21/v2_build/final21.py            # patches21.json で組み直す → 門番 → 対照表
  python ref/ep21/v2_build/final21.py --nobuild  # 組まずに門番だけ

回すもの（順番どおり）：
  1 build21_v2.py patches21.json         第2版（第1版の md5 を前後で比べる）
  2 roles21_v2.py daihon_v2.md roles.tsv 聞き役の役割表（roles_map.json から）
  3 m21.py daihon_v2.md --roles …        字数・尺の3通り・冒頭の秒・行の形・聞き役（check_listener.judge）・写真の割合
  4 quotes21.py daihon_v2.md             出典の欄の引用を資料の字に（--out で第1版の記録を上書きしない）
  5 namecheck.py（git の外）             書かない名前＝台本と v2_build の md・json の全部
  6 tools/check_script.py daihon_v2.md   形の門番（E は既知の尺の件だけか）
  7 tools/check_script_diff.py v1 v2     🔧 の印と差分の一致・欠番
  8 count_text_screens.py --gate --ids   文字だけの画面
  9 romanpage                            🆕 `図 p.xv` のようにローマ数字・点つきの頁＝count_text_screens が「図解」と数える穴（④' で見つけた）
 10 make_diff21.py                       第1版→第2版の対照表
"""
import glob
import os
import re
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
NAMECHECK = os.path.join(EP, 'src', 'core_raw', 'namecheck.py')
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')


def romanpage():
    """画の欄が `図 p.` か `図 p` ＋ローマ数字のカット＝文字の頁なのに count_text_screens が「図解」と数える。"""
    hdr = re.compile(r'^\*\*(c[0-9a-c]\d{2})\*\*\s*(?:🔧)?\s*／\s*(.*?)\s*／')
    hit = []
    on = False
    for ln in open(V2, encoding='utf-8'):
        if ln.startswith('## 4.'):
            on = True
        elif on and re.match(r'^## \d', ln):
            break
        m = hdr.match(ln) if on else None
        if m and re.match(r'図\s*p\s*(\.|[ivxl]+\b)', m.group(2)) and not re.match(r'図\s*p\d', m.group(2)):
            hit.append('%s ／ %s' % (m.group(1), m.group(2)[:60]))
    txt = '\n'.join(hit) if hit else '該当なし'
    return (1 if hit else 0), 'ローマ数字・点つきの頁（文字だけに数え足す）: %d\n%s' % (len(hit), txt)


steps = []
if '--nobuild' not in sys.argv:
    steps.append(('build', [PY, os.path.join(HERE, 'build21_v2.py'), os.path.join(HERE, 'patches21.json')]))
mine = sorted(glob.glob(os.path.join(HERE, '*.md')) + glob.glob(os.path.join(HERE, '*.json')) + glob.glob(os.path.join(HERE, '*.tsv')))
steps += [
    ('roles', [PY, os.path.join(HERE, 'roles21_v2.py'), V2, ROLES]),
    ('m21', [PY, os.path.join(EP, 'v1_build', 'm21.py'), V2, '--roles', ROLES]),
    ('quotes21v2', [PY, os.path.join(HERE, 'quotes21v2.py'), V2, '--out', os.path.join(HERE, 'quotes21_v2.tsv')]),
    ('namecheck', [PY, NAMECHECK, V2] + mine),
    ('check_script', [PY, os.path.join(REPO, 'tools', 'check_script.py'), V2]),
    ('check_script_diff', [PY, os.path.join(REPO, 'tools', 'check_script_diff.py'), V1, V2]),
    ('count_text_screens', [PY, CTS, V2, '--gate', '--ids']),
    ('romanpage', None),
    ('make_diff', [PY, os.path.join(HERE, 'make_diff21.py')]),
]
out = ['# 21本目 第2版の門番（final21.py の出力・手で直さない）', '']
summary = []
for name, cmd in steps:
    if cmd is None:
        rc, txt = romanpage()
    else:
        r = subprocess.run(cmd, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
        rc, txt = r.returncode, (r.stdout or '') + (r.stderr or '')
    out += ['## %s（exit=%d）' % (name, rc), '```', txt.rstrip(), '```', '']
    summary.append('%s=%d' % (name, rc))
    if name == 'build' and rc != 0:
        out.append('🔴 組めなかったので止めた')
        break
open(os.path.join(HERE, 'gates.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('  '.join(summary))
print('→', os.path.join(HERE, 'gates.md'))
