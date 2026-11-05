# -*- coding: utf-8 -*-
"""30本目④'：第2版を組んで、門番をまとめて回す（出力は v2_build/gates.md・各門番の終了コードつき・29本目 final29.py を写した）。

  python -P ref/ep30/v2_build/final30.py            # patches30.json で組み直す → 門番 → 対照表
  python -P ref/ep30/v2_build/final30.py --nobuild  # 組まずに門番だけ

回すもの（順番どおり）：
  1 build30_v2.py patches30.json          第2版（第1版の md5 を前後で比べる）
  2 roles30_v2.py daihon_v2.md roles.tsv  聞き役の役割表（roles_map.json から）
  3 m30v2.py --selftest                   m30 と足した網の陽性対照（自分の物差しを先に確かめる）
  4 m30v2.py daihon_v2.md --roles …       ④ の m30（字数・尺の3通り・冒頭の秒・行の形・聞き役＝check_listener.judge・写真の割合・図の型・線・名前・帰属）＋言い切り・帰属・カンマの網
  5 namecheck30.py                        書かない名前（src/names_private.txt）＝`git ls-files ref/ep30` の全部と v2_build の新しいファイルの全部
  6 linecheck30.py                        線の語（src/line_words.txt）＝同じファイル。§4 に当たれば E／ほかは人が見る行として出す
  7 tools/check_script.py daihon_v2.md    形の門番（E は既知の尺の件＝§5a-28b だけか）
  8 tools/check_script_diff.py v1 v2      🔧 の印と差分の一致・欠番
  9 quotes30.py v2                        出典の欄の原文の片を一次資料の文字に当てる（外れ 0）
 10 tags30.py v2                          出典の札の数え（置き場か台帳に無い札 0）
 11 sou                                   聞き役の「まとめ」のあとの語りが「そう。」で受けているか（roles.tsv × 台本）
 12 internal                              台本の頭と §0 に内部の数字の語が無いか（4'-17）
 13 band                                  字数の幅（13,140〜13,505）と冒頭の引き（c105 が46秒まで）＝m30 の出力から
 14 make_diff30.py                        第1版→第2版の対照表
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
LO, HI, OPEN_MAX = 13140, 13505, 46.0  # ③ の目標 36〜37分（kousei.md §0・m30.py）
A_LO, A_HI = 9855, 14600               # A の枠 27〜40分（÷365）
TARGET = 13320
HOOK = 'c105'                          # 冒頭の引き「同じ毒は、前の年に長野県の松本で使われていた」
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
    if not m or HOOK not in o:
        return 2, 'm30 の出力が読めない（字数か冒頭の秒が無い）'
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
    r = subprocess.run(['git', 'ls-files', 'ref/ep30'], cwd=REPO, capture_output=True, text=True, encoding='utf-8')
    return [os.path.join(REPO, x) for x in r.stdout.split('\n') if x.strip()]


def mine():
    fs = glob.glob(os.path.join(HERE, '*.md')) + glob.glob(os.path.join(HERE, '*.json')) + glob.glob(os.path.join(HERE, '*.tsv')) \
        + glob.glob(os.path.join(HERE, '*.py')) + glob.glob(os.path.join(HERE, '*.txt'))
    keep = [f for f in fs if os.path.basename(f) != 'gates.md']
    return sorted(set(keep + tracked() + [V2]))


def line_gate(r):
    """linecheck の当たりのうち、§4（台本の本文）に当たったものを E に。ほかは人が見る行。"""
    lines = open(V2, encoding='utf-8').read().split('\n')
    s4 = next(i for i, ln in enumerate(lines) if ln.startswith('## 4. 台本')) + 1
    s5 = next(i for i, ln in enumerate(lines) if ln.startswith('## 5. ')) + 1
    hit4 = []
    for m in re.finditer(r'^daihon_v2\.md:(\d+) に線の語', r, re.M):
        if s4 <= int(m.group(1)) < s5:
            hit4.append(m.group(1))
    return hit4


steps = []
if '--nobuild' not in sys.argv:
    steps.append(('build', [PY, '-P', os.path.join(HERE, 'build30_v2.py'), os.path.join(HERE, 'patches30.json')]))
steps += [
    ('roles', [PY, '-P', os.path.join(HERE, 'roles30_v2.py'), V2, ROLES]),
    ('m30v2_selftest', [PY, '-P', os.path.join(HERE, 'm30v2.py'), '--selftest']),
    ('m30v2', [PY, '-P', os.path.join(HERE, 'm30v2.py'), V2, '--roles', ROLES]),
    ('namecheck', 'names'),
    ('linecheck', 'line'),
    ('check_script', [PY, os.path.join(REPO, 'tools', 'check_script.py'), V2]),
    ('check_script_diff', [PY, os.path.join(REPO, 'tools', 'check_script_diff.py'), V1, V2]),
    ('quotes', [PY, '-P', os.path.join(EP, 'v1_build', 'quotes30.py'), V2, '--out', os.path.join(HERE, 'quotes30_v2.tsv')]),
    ('tags', [PY, '-P', os.path.join(HERE, 'tags30.py'), V2]),
    ('sou', None),
    ('internal', None),
    ('band', None),
    ('make_diff', [PY, '-P', os.path.join(HERE, 'make_diff30.py')]),
]
out = ['# 30本目 第2版の門番（final30.py の出力・手で直さない）', '']
summary = []
for name, cmd in steps:
    if cmd is None:
        rc, txt = {'sou': sou, 'internal': internal, 'band': band}[name]()
    else:
        if cmd == 'names':
            cmd = [PY, '-P', os.path.join(HERE, 'namecheck30.py')] + mine()
        elif cmd == 'line':
            cmd = [PY, '-P', os.path.join(HERE, 'linecheck30.py')] + mine()
        r = subprocess.run(cmd, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
        rc, txt = r.returncode, (r.stdout or '') + (r.stderr or '')
        if name == 'm30v2':
            M_OUT['txt'] = txt
        if name == 'linecheck':
            hit4 = line_gate(txt)
            txt += '\n§4 に当たった行: %s' % (hit4 or 'なし')
            rc = 1 if hit4 else 0
        if name == 'check_script':     # 既知の尺の E は 1件まで＝形の E が無いかを別に見る
            shape = [ln for ln in txt.split('\n') if ln.strip().startswith('🔴 E') and '尺 ' not in ln]
            txt += '\n形の E: %d件' % len(shape)
            rc = 1 if shape else 0
    out += ['## %s（exit=%d）' % (name, rc), '```', txt.rstrip(), '```', '']
    summary.append('%s=%d' % (name, rc))
    if name == 'build' and rc != 0:
        out.append('🔴 組めなかったので止めた')
        break
open(os.path.join(HERE, 'gates.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('  '.join(summary))
print('→', os.path.join(HERE, 'gates.md'))
