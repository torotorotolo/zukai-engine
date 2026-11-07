# -*- coding: utf-8 -*-
"""31本目④'：第2版を組んで、門番をまとめて回す（出力は v2_build/gates.md・各門番の終了コードつき・30本目 final30.py を写した）。

  python -P ref/ep31/v2_build/final31.py            # patches31.json で組み直す → 門番 → 対照表 → 消えた語
  python -P ref/ep31/v2_build/final31.py --nobuild  # 組まずに門番だけ

回すもの（順番どおり）：
  1 build31_v2.py patches31.json          第2版（第1版の md5 を前後で比べる）
  2 v1_build/roles31.py daihon_v2.md v2_build/roles.tsv   聞き役の役割表（役割は行の終わりで決まる）
  3 v1_build/m31.py --selftest            m31 の陽性対照（自分の物差しを先に確かめる）
  4 v1_build/m31.py daihon_v2.md --roles  字数・尺の3通り・冒頭の秒・行の形・聞き役＝check_listener.judge・写真の割合・図の型・線・名前・帰属・時点
  5 namecheck31.py                        書かない名前（src/names_private.txt＋names_commons.txt）＝`git ls-files ref/ep31` の全部と v2_build の新しいファイルの全部
  6 tools/check_script.py daihon_v2.md    形の門番（E は既知の尺の件＝§5a-28b だけか）
  7 tools/check_script_diff.py v1 v2      🔧 の印と差分の一致・欠番
  8 v1_build/quotes31.py v2               出典の欄の原文の片を一次資料の文字に当てる（外れ 0）
  9 tags31.py v2                          出典の札の数え（置き場に無い国会の発言 0）
 10 sou                                   聞き役の「まとめ」のあとの語りが「そう。」で受けているか（roles.tsv × 台本）
 11 internal                              台本の頭と §0 に内部の数字の語が無いか（4'-17）
 12 band                                  字数の幅（13,140〜13,505）と冒頭の引き（c105 が46秒まで）＝m31 の出力から
 13 make_diff31.py                        第1版→第2版の対照表
 14 lost31.py                             第1版の語りにあって第2版に無い語（git の外へ）
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
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
LO, HI, OPEN_MAX = 13140, 13505, 46.0  # ③ の目標 36〜37分（kousei.md §0・m31.py）
A_LO, A_HI = 9855, 14600               # A の枠 27〜40分（÷365）
TARGET = 13140
HOOK = 'c105'                          # 冒頭の引き「旅客機の通り道が載っていない地図の上で…指で示して決めていた」
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
    head = s[:s.find('## 4. 台本')]
    hit = [w for w in ('維持率', 'CTR', 'インプレ', '再生回数', '再生数', '流入', '視聴維持', '平均視聴', 'クリック率') if w in head]
    return (1 if hit else 0), '頭と §0〜§3 の内部の数字の語: %s' % (hit or 'なし')


def band():
    out = M_OUT.get('txt', '')
    m = re.search(r'＝(\d+)字（目標', out)
    o = dict(re.findall(r'(c10[1-7])=([\d.]+)s', out))
    if not m or HOOK not in o:
        return 2, 'm31 の出力が読めない（字数か冒頭の秒が無い）'
    n = int(m.group(1))
    hook, c107 = float(o[HOOK]), float(o.get('c107', 0))
    bad = []
    if not A_LO <= n <= A_HI:
        bad.append('字数 %d が A の枠 %d〜%d（27〜40分）の外' % (n, A_LO, A_HI))
    if not LO <= n <= HI:
        bad.append('字数 %d が ③ の目標の幅 %d〜%d の外（%+d字＝約%+.0f秒）' % (n, LO, HI, n - TARGET, (n - TARGET) * 60 / 365.0))
    if hook > OPEN_MAX:
        bad.append('冒頭の引き %s の終わり %.1f秒が %d秒を越えた' % (HOOK, hook, OPEN_MAX))
    txt = '句読点なし %d字（幅 %d〜%d・A の枠 %d〜%d・%d分%02d秒）／冒頭の引き %s=%.1f秒（%d秒まで）・最初の見出しの前 c107 の終わり=%.1f秒／%s' % (
        n, LO, HI, A_LO, A_HI, n // 365, int(n * 60 / 365.0) % 60, HOOK, hook, OPEN_MAX, c107, '・'.join(bad) or 'OK')
    return (1 if bad else 0), txt


def tracked():
    r = subprocess.run(['git', 'ls-files', 'ref/ep31'], cwd=REPO, capture_output=True, text=True, encoding='utf-8')
    return [os.path.join(REPO, x) for x in r.stdout.split('\n') if x.strip()]


def mine():
    fs = []
    for ext in ('*.md', '*.json', '*.tsv', '*.py', '*.txt'):
        fs += glob.glob(os.path.join(HERE, ext))
    keep = [f for f in fs if os.path.basename(f) != 'gates.md']
    return sorted(set(keep + tracked() + [V2]))


steps = []
if '--nobuild' not in sys.argv:
    steps.append(('build', [PY, '-P', os.path.join(HERE, 'build31_v2.py'), os.path.join(HERE, 'patches31.json')]))
steps += [
    ('roles', [PY, '-P', os.path.join(EP, 'v1_build', 'roles31.py'), V2, ROLES]),
    ('m31_selftest', [PY, '-P', os.path.join(EP, 'v1_build', 'm31.py'), '--selftest']),
    ('m31', [PY, '-P', os.path.join(EP, 'v1_build', 'm31.py'), V2, '--roles', ROLES]),
    ('namecheck', 'names'),
    ('check_script', [PY, os.path.join(REPO, 'tools', 'check_script.py'), V2]),
    ('check_script_diff', [PY, os.path.join(REPO, 'tools', 'check_script_diff.py'), V1, V2]),
    ('quotes', [PY, '-P', os.path.join(EP, 'v1_build', 'quotes31.py'), V2, '--out', os.path.join(HERE, 'quotes31_v2.tsv')]),
    ('tags', [PY, '-P', os.path.join(HERE, 'tags31.py'), V2]),
    ('sou', None),
    ('internal', None),
    ('band', None),
    ('make_diff', [PY, '-P', os.path.join(HERE, 'make_diff31.py')]),
    ('lost', [PY, '-P', os.path.join(HERE, 'lost31.py')]),
]
out = ['# 31本目 第2版の門番（final31.py の出力・手で直さない）', '']
summary = []
for name, cmd in steps:
    if cmd is None:
        rc, txt = {'sou': sou, 'internal': internal, 'band': band}[name]()
    else:
        if cmd == 'names':
            cmd = [PY, '-P', os.path.join(HERE, 'namecheck31.py')] + mine()
        r = subprocess.run(cmd, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
        rc, txt = r.returncode, (r.stdout or '') + (r.stderr or '')
        if name == 'm31':
            M_OUT['txt'] = txt
            em = re.search(r'E (\d+)件（形）・聞き役 E (\d+)件', txt)
            if not em or em.group(1) != '0' or em.group(2) != '0':
                rc = rc or 1
        if name == 'check_script':     # 既知の尺の E は 1件まで＝形の E が無いかを別に見る
            shape = [ln for ln in txt.split('\n') if ln.strip().startswith('🔴 E') and '尺 ' not in ln]
            txt += '\n形の E: %d件' % len(shape)
            rc = 1 if shape else 0
        if name == 'm31':              # W の「模式が続く」は数だけ（行は gates.md を太らせる）
            keep = [ln for ln in txt.split('\n') if '図の型「模式」が続く' not in ln]
            nmod = len(txt.split('\n')) - len(keep)
            txt = '\n'.join(keep) + '\n（W「図の型『模式』が続く」%d行は数だけ）' % nmod
    out += ['## %s（exit=%d）' % (name, rc), '```', txt.rstrip(), '```', '']
    summary.append('%s=%d' % (name, rc))
    if name == 'build' and rc != 0:
        out.append('🔴 組めなかったので止めた')
        break
open(os.path.join(HERE, 'gates.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('  '.join(summary))
print('→', os.path.join(HERE, 'gates.md'))
