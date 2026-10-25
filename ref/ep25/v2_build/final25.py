# -*- coding: utf-8 -*-
"""25本目④'：第2版を組んで、門番をまとめて回す（出力は v2_build/gates.md・各門番の終了コードつき・24本目 final24.py を写した）。

  python ref/ep25/v2_build/final25.py            # patches25.json で組み直す → 門番 → 対照表
  python ref/ep25/v2_build/final25.py --nobuild  # 組まずに門番だけ

回すもの（順番どおり）：
  1 build25_v2.py patches25.json          第2版（第1版の md5 を前後で比べる）
  2 roles25_v2.py daihon_v2.md roles.tsv  聞き役の役割表（roles_map.json から）
  3 m25.py daihon_v2.md --roles …         字数・尺の3通り・冒頭の秒・行の形・聞き役（check_listener.judge）・写真の割合・言わない語・名前・図の型
  4 quotes25.py daihon_v2.md --out …      出典の欄の原文の片を文字の層に（第1版の記録 v1_build/quotes25_result.tsv を上書きしない）
  5 namecheck25.py                        書かない名前（src/names_private.txt・撮影者の個人名）＝台本と v2_build の md・json・tsv・py の全部
  6 tools/check_script.py daihon_v2.md    形の門番（E は既知の尺の件だけか）
  7 tools/check_script_diff.py v1 v2      🔧 の印と差分の一致・欠番
  8 count_text_screens.py --gate --ids    文字だけの画面
  9 sou                                   聞き役の「まとめ」のあとの語りが「そう。」で受けているか（roles.tsv × 台本）
 10 internal                              台本の頭と §0 に内部の数字の語（維持率・CTR・インプレ・再生回数・流入）が無いか（4'-17）
 11 band                                  字数の幅（13,140〜13,505）と冒頭の秒（ひっくり返し c106 が46秒まで）＝m25 の出力から
 12 make_diff25.py                        第1版→第2版の対照表
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
LO, HI, OPEN_MAX = 13140, 13505, 46.0
M_OUT = {}


def narr_after(path):
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
    hit = [w for w in ('維持率', 'CTR', 'インプレ', '再生回数', '流入', '視聴維持', '平均視聴') if w in head]
    return (1 if hit else 0), '頭と §0 の内部の数字の語: %s' % (hit or 'なし')


def band():
    out = M_OUT.get('txt', '')
    m = re.search(r'＝(\d+)字（目標', out)
    o = dict(re.findall(r'(c10[1-7])=([\d.]+)s', out))
    if not m or 'c106' not in o:
        return 2, 'm25 の出力が読めない（字数か冒頭の秒が無い）'
    n = int(m.group(1))
    c106, c107 = float(o['c106']), float(o.get('c107', 0))
    bad = []
    if not LO <= n <= HI:
        bad.append('字数 %d が幅 %d〜%d の外' % (n, LO, HI))
    if c106 > OPEN_MAX:
        bad.append('ひっくり返し c106 の終わり %.1f秒が %d秒を越えた' % (c106, OPEN_MAX))
    txt = '句読点なし %d字（幅 %d〜%d・上限まで %d字）／冒頭 c106=%.1f秒（%d秒まで）・最初の見出し c107 の終わり=%.1f秒／%s' % (
        n, LO, HI, HI - n, c106, OPEN_MAX, c107, '・'.join(bad) or 'OK')
    return (1 if bad else 0), txt


steps = []
if '--nobuild' not in sys.argv:
    steps.append(('build', [PY, os.path.join(HERE, 'build25_v2.py'), os.path.join(HERE, 'patches25.json')]))
mine = sorted(f for f in glob.glob(os.path.join(HERE, '*.md')) + glob.glob(os.path.join(HERE, '*.json'))
              + glob.glob(os.path.join(HERE, '*.tsv')) + glob.glob(os.path.join(HERE, '*.py')) + glob.glob(os.path.join(HERE, '*.txt'))
              if os.path.basename(f) != 'gates.md')
steps += [
    ('roles', [PY, os.path.join(HERE, 'roles25_v2.py'), V2, ROLES]),
    ('m25', [PY, os.path.join(EP, 'v1_build', 'm25.py'), V2, '--roles', ROLES]),
    ('quotes25', [PY, os.path.join(EP, 'v1_build', 'quotes25.py'), V2, '--out', os.path.join(HERE, 'quotes25_v2.tsv')]),
    ('namecheck', [PY, os.path.join(HERE, 'namecheck25.py'), V2] + mine),
    ('check_script', [PY, os.path.join(REPO, 'tools', 'check_script.py'), V2]),
    ('check_script_diff', [PY, os.path.join(REPO, 'tools', 'check_script_diff.py'), V1, V2]),
    ('count_text_screens', [PY, CTS, V2, '--gate', '--ids']),
    ('sou', None),
    ('internal', None),
    ('band', None),
    ('make_diff', [PY, os.path.join(HERE, 'make_diff25.py')]),
]
out = ['# 25本目 第2版の門番（final25.py の出力・手で直さない）', '']
summary = []
for name, cmd in steps:
    if cmd is None:
        rc, txt = {'sou': sou, 'internal': internal, 'band': band}[name]()
    else:
        r = subprocess.run(cmd, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
        rc, txt = r.returncode, (r.stdout or '') + (r.stderr or '')
        if name == 'm25':
            M_OUT['txt'] = txt
    out += ['## %s（exit=%d）' % (name, rc), '```', txt.rstrip(), '```', '']
    summary.append('%s=%d' % (name, rc))
    if name == 'build' and rc != 0:
        out.append('🔴 組めなかったので止めた')
        break
open(os.path.join(HERE, 'gates.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('  '.join(summary))
print('→', os.path.join(HERE, 'gates.md'))
