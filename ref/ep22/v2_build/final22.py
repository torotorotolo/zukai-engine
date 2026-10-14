# -*- coding: utf-8 -*-
"""22本目④'：第2版を組んで、門番をまとめて回す（出力は v2_build/gates.md・各門番の終了コードつき・21本目 final21.py を写した）。

  python ref/ep22/v2_build/final22.py            # patches22.json で組み直す → 門番 → 対照表
  python ref/ep22/v2_build/final22.py --nobuild  # 組まずに門番だけ

回すもの（順番どおり）：
  1 build22_v2.py patches22.json         第2版（第1版の md5 を前後で比べる）
  2 roles22_v2.py daihon_v2.md roles.tsv 聞き役の役割表（roles_map.json から）
  3 m22.py daihon_v2.md --roles …        字数・尺の3通り・冒頭の秒・行の形・聞き役（check_listener.judge）・写真の割合・言わない語・CEO の置き場
  4 quotes22.py daihon_v2.md --out …     出典の欄の引用を3冊の字に（第1版の記録 v1_build/quotes22_result.tsv を上書きしない）
  5 namecheck22.py                       書かない名前（git の外の一覧）＝台本と v2_build の md・json・tsv の全部
  6 tools/check_script.py daihon_v2.md   形の門番（E は既知の尺の件だけか）
  7 tools/check_script_diff.py v1 v2     🔧 の印と差分の一致・欠番
  8 count_text_screens.py --gate --ids   文字だけの画面
  9 sou                                  聞き役の「まとめ」のあとの語りが「そう。」で受けているか（roles.tsv × 台本）
 10 internal                             台本の頭と §0 に内部の数字の語（維持率・CTR・インプレ・再生回数・流入）が無いか（4'-17）
 11 make_diff22.py                       第1版→第2版の対照表
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
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')


def narr_after(path):
    """カット番号 → そのカットの語りの行（聞き役でない `> ` の行）の並び。台本の順。"""
    order, lines, cur, on = [], {}, None, False
    for ln in open(path, encoding='utf-8'):
        if ln.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        m = CUT.match(ln) if on else None
        if m:
            cur = m.group(1)
            order.append(cur)
            lines[cur] = []
        elif cur and ln.startswith('> '):
            lines[cur].append(ln[2:].strip())
    return order, lines


def sou():
    """roles.tsv の「まとめ」の行のすぐ後の語りの行が「そう。」で始まるか。まとめでない聞き役の後の「そう。」も数える。"""
    roles = {}
    for ln in open(ROLES, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip():
            continue
        c, r, _ = ln.rstrip('\n').split('\t', 2)
        roles[c] = r
    order, lines = narr_after(V2)
    flat = [(c, x) for c in order for x in lines[c]]
    bad, odd = [], []
    for i, (c, x) in enumerate(flat):
        if not x.startswith('Q:'):
            continue
        nxt = next(((cc, y) for cc, y in flat[i + 1:] if not y.startswith('Q:')), None)
        if not nxt:
            continue
        starts = nxt[1].startswith('そう。')
        if roles.get(c) == 'まとめ' and not starts:
            bad.append('%s のまとめ → %s「%s」' % (c, nxt[0], nxt[1][:20]))
        if roles.get(c) != 'まとめ' and starts:
            odd.append('%s（%s）→ %s「%s」' % (c, roles.get(c, '質問'), nxt[0], nxt[1][:20]))
    nq = sum(1 for _, x in flat if x.startswith('Q:'))
    ns = sum(1 for _, x in flat if x.startswith('そう。'))
    nm = sum(1 for r in roles.values() if r == 'まとめ')
    txt = '聞き役の行 %d・そのうち役割表のまとめ %d・語りの「そう。」 %d（0 なら数え損ない）\nまとめの後が「そう。」でない: %d\n%s\n参考＝まとめでない聞き役の後の「そう。」: %d\n%s' % (
        nq, nm, ns, len(bad), '\n'.join(bad) or '—', len(odd), '\n'.join(odd) or '—')
    if not nq or not ns:
        return 2, txt
    return (1 if bad else 0), txt


def internal():
    s = open(V2, encoding='utf-8').read()
    head = s[:s.find('## 1. ')]
    hit = [w for w in ('維持率', 'CTR', 'インプレ', '再生回数', '流入', '視聴維持') if w in head]
    return (1 if hit else 0), '頭と §0 の内部の数字の語: %s' % (hit or 'なし')


steps = []
if '--nobuild' not in sys.argv:
    steps.append(('build', [PY, os.path.join(HERE, 'build22_v2.py'), os.path.join(HERE, 'patches22.json')]))
mine = sorted(glob.glob(os.path.join(HERE, '*.md')) + glob.glob(os.path.join(HERE, '*.json')) + glob.glob(os.path.join(HERE, '*.tsv')))
steps += [
    ('roles', [PY, os.path.join(HERE, 'roles22_v2.py'), V2, ROLES]),
    ('m22', [PY, os.path.join(EP, 'v1_build', 'm22.py'), V2, '--roles', ROLES]),
    ('quotes22', [PY, os.path.join(EP, 'v1_build', 'quotes22.py'), V2, '--out', os.path.join(HERE, 'quotes22_v2.tsv')]),
    ('namecheck', [PY, os.path.join(HERE, 'namecheck22.py'), V2] + mine),
    ('check_script', [PY, os.path.join(REPO, 'tools', 'check_script.py'), V2]),
    ('check_script_diff', [PY, os.path.join(REPO, 'tools', 'check_script_diff.py'), V1, V2]),
    ('count_text_screens', [PY, CTS, V2, '--gate', '--ids']),
    ('sou', None),
    ('internal', None),
    ('make_diff', [PY, os.path.join(HERE, 'make_diff22.py')]),
]
out = ['# 22本目 第2版の門番（final22.py の出力・手で直さない）', '']
summary = []
for name, cmd in steps:
    if cmd is None:
        rc, txt = {'sou': sou, 'internal': internal}[name]()
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
