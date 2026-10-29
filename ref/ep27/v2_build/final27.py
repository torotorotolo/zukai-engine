# -*- coding: utf-8 -*-
"""27本目④'：第2版を組んで、門番をまとめて回す（出力は v2_build/gates.md・各門番の終了コードつき・26本目 final26.py を写した）。

  python -P ref/ep27/v2_build/final27.py            # patches27.json で組み直す → 門番 → 対照表
  python -P ref/ep27/v2_build/final27.py --nobuild  # 組まずに門番だけ

回すもの（順番どおり）：
  1 build27_v2.py patches27.json          第2版（第1版の md5 を前後で比べる）
  2 roles27_v2.py daihon_v2.md roles.tsv  聞き役の役割表（ROLE から）
  3 m27v2.py daihon_v2.md --roles …       ④ の m27（字数・尺の3通り・冒頭の秒・行の形・聞き役＝check_listener.judge・写真の割合・
                                          事件の回の網・名前・Commons の番号と題名・図の型）＋確かめようのない否定・SNS の字
  4 namecheck27.py                        書かない名前（src/names_private.txt）＝台本と v2_build の md・json・tsv・py・txt の全部
  5 tools/check_script.py daihon_v2.md    形の門番（E は既知の尺の件＝ElevenLabs の定数と A の枠＝§5a-28b だけか）
  6 tools/check_script_diff.py v1 v2      🔧 の印と差分の一致・欠番
  7 tools/check_facts.py v2 news_frag     3桁以上の数が原文の片にあるか（git の外の src/news_frag_v2.txt＝④ の片＋④' の係の片）
  8 sou                                   聞き役の「まとめ」のあとの語りが「そう。」で受けているか（roles.tsv × 台本）
  9 internal                              台本の頭と §0 に内部の数字の語（維持率・CTR・インプレ・再生回数・流入）が無いか（4'-17）
 10 band                                  字数の幅（5,690〜5,990）と冒頭の引き（c103 が46秒まで）＝m27 の出力から
 11 make_diff27.py                        第1版→第2版の対照表
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
FRAG = os.path.join(EP, 'src', 'news_frag_v2.txt')
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
LO, HI, OPEN_MAX = 5690, 5990, 46.0   # ③ の目標16分±25秒（参考＝外でも止めない）
B_LO, B_HI = 2920, 7300                # B の枠 8〜20分（÷365）＝外なら止める（10-29 カズヤくんの指示で補足を外し、16分から15分台に下がった）
HOOK = 'c103'                      # 冒頭の引き「1万3978件・逮捕につながる有力な手がかりは、まだ得られていない」
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
        return 2, 'm27 の出力が読めない（字数か冒頭の秒が無い）'
    n = int(m.group(1))
    hook, c107 = float(o[HOOK]), float(o.get('c107', 0))
    bad, note = [], []
    if not B_LO <= n <= B_HI:
        bad.append('字数 %d が B の枠 %d〜%d（8〜20分）の外' % (n, B_LO, B_HI))
    if not LO <= n <= HI:
        note.append('参考：③ の目標16分の幅 %d〜%d の外（%+d字＝約%+.0f秒・10-29 カズヤくんの指示で一般の語の補足を外したため）' % (
            LO, HI, n - 5840, (n - 5840) * 60 / 365.0))
    if hook > OPEN_MAX:
        bad.append('冒頭の引き %s の終わり %.1f秒が %d秒を越えた' % (HOOK, hook, OPEN_MAX))
    txt = '句読点なし %d字（B の枠 %d〜%d の内か・%.0f分%02.0f秒）／冒頭の引き %s=%.1f秒（%d秒まで）・最初の見出しの前 c107 の終わり=%.1f秒／%s%s' % (
        n, B_LO, B_HI, n // 365, (n * 60 / 365.0) % 60, HOOK, hook, OPEN_MAX, c107, '・'.join(bad) or 'OK',
        ('／' + '・'.join(note)) if note else '')
    return (1 if bad else 0), txt


steps = []
if '--nobuild' not in sys.argv:
    steps.append(('build', [PY, '-P', os.path.join(HERE, 'build27_v2.py'), os.path.join(HERE, 'patches27.json')]))
mine = sorted(f for f in glob.glob(os.path.join(HERE, '*.md')) + glob.glob(os.path.join(HERE, '*.json'))
              + glob.glob(os.path.join(HERE, '*.tsv')) + glob.glob(os.path.join(HERE, '*.py')) + glob.glob(os.path.join(HERE, '*.txt'))
              if os.path.basename(f) != 'gates.md')
steps += [
    ('roles', [PY, '-P', os.path.join(HERE, 'roles27_v2.py'), V2, ROLES]),
    ('m27v2', [PY, '-P', os.path.join(HERE, 'm27v2.py'), V2, '--roles', ROLES]),
    ('namecheck', [PY, '-P', os.path.join(HERE, 'namecheck27.py'), V2] + mine),
    ('check_script', [PY, os.path.join(REPO, 'tools', 'check_script.py'), V2]),
    ('check_script_diff', [PY, os.path.join(REPO, 'tools', 'check_script_diff.py'), V1, V2]),
    ('check_facts', [PY, os.path.join(REPO, 'tools', 'check_facts.py'), V2, FRAG]),
    ('sou', None),
    ('internal', None),
    ('band', None),
    ('make_diff', [PY, '-P', os.path.join(HERE, 'make_diff27.py')]),
]
out = ['# 27本目 第2版の門番（final27.py の出力・手で直さない）', '']
summary = []
for name, cmd in steps:
    if cmd is None:
        rc, txt = {'sou': sou, 'internal': internal, 'band': band}[name]()
    else:
        r = subprocess.run(cmd, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
        rc, txt = r.returncode, (r.stdout or '') + (r.stderr or '')
        if name == 'm27v2':
            M_OUT['txt'] = txt
    out += ['## %s（exit=%d）' % (name, rc), '```', txt.rstrip(), '```', '']
    summary.append('%s=%d' % (name, rc))
    if name == 'build' and rc != 0:
        out.append('🔴 組めなかったので止めた')
        break
open(os.path.join(HERE, 'gates.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('  '.join(summary))
print('→', os.path.join(HERE, 'gates.md'))
