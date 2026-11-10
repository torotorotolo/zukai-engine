# -*- coding: utf-8 -*-
"""32本目④'：第1版→第2版の対照表（変わったカットだけ・語りと見出しの行を並べる）を作る（31本目 make_diff31.py の考えを写した）。

  python -P ref/ep32/v2_build/make_diff32.py [--only c4,c5] [--out 置き場]

別の目（ルール 4'-18）に渡す。差し替え表（patches32.json）の id と why と from も添える。
既定の出力＝v2_build/diff_v1_v2.md。--only は章の頭2字（c4,c5 や cb,cc）で絞る。§ の差し替えは末尾にまとめる。
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
CUT = re.compile(r'^\*\*(c[0-9a-c]\d{2})\*\*')


def blocks(path):
    out, cur, order = {}, None, []
    text = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    s4 = text[text.index('## 4. 台本'):text.index('\n## 5.')]
    for l in s4.split('\n'):
        m = CUT.match(l)
        if m:
            cur = m.group(1)
            out[cur] = [re.sub(r'^(\*\*c[0-9a-c]\d{2}\*\*)\s*🔧', r'\1', l)]
            order.append(cur)
            continue
        if l.startswith('#') or l.strip() == '---':
            cur = None
            continue
        if cur and l.startswith('>'):
            out[cur].append(l)
    return out, order


def main():
    out = os.path.join(HERE, 'diff_v1_v2.md')
    if '--out' in sys.argv:
        out = sys.argv[sys.argv.index('--out') + 1]
    only = None
    if '--only' in sys.argv:
        only = set(sys.argv[sys.argv.index('--only') + 1].split(','))
    b1, o1 = blocks(os.path.join(EP, 'daihon_v1.md'))
    b2, o2 = blocks(os.path.join(EP, 'daihon_v2.md'))
    pt = os.path.join(HERE, 'patches32.json')
    patches = json.load(open(pt, encoding='utf-8')) if os.path.exists(pt) else []
    by_cut = {}
    for p in patches:
        by_cut.setdefault(p['cut'], []).append(p)
    lines = ['# 32本目 台本 第1版 → 第2版の対照（変わったカットだけ・make_diff32.py が組む・手で直さない）', '',
             '- 形＝カットごとに「第1版」と「第2版」の見出しの行（画・出典）と語り・聞き役の行。差し替えの id・理由・もとの所見の番号を添える。',
             '- 消えたカット・新しいカットがあれば見出しに書く。', '']
    n = 0
    for c in o2:
        if only and c[:2] not in only:
            continue
        if c in b1 and b1[c] == b2[c]:
            continue
        n += 1
        lines.append('## %s%s' % (c, '' if c in b1 else '（新しいカット）'))
        for p in by_cut.get(c, []):
            lines.append('- 差し替え %s：%s（もと %s）' % (p['id'], p.get('why', ''), '・'.join(p.get('from') or [])))
        if c in b1:
            lines.append('**第1版**')
            lines += ['    ' + l for l in b1[c]]
        lines.append('**第2版**')
        lines += ['    ' + l for l in b2[c]]
        lines.append('')
    gone = [c for c in o1 if c not in b2 and (not only or c[:2] in only)]
    if gone:
        lines.append('## 消えたカット：' + ' '.join(gone))
        lines.append('')
    sec = [p for p in patches if p['cut'] in ('§', '*')]
    if sec and not only:
        lines.append('## § と見出しの差し替え（%d件）' % len(sec))
        for p in sec:
            lines.append('- %s：%s' % (p['id'], p.get('why', '')))
            lines.append('    − ' + p['old'].replace('\n', '⏎'))
            lines.append('    ＋ ' + p['new'].replace('\n', '⏎'))
        lines.append('')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))
    print('対照 %d カット・消えた %d・§ %d → %s' % (n, len(gone), len(sec), out))
    return 0


if __name__ == '__main__':
    sys.exit(main())
