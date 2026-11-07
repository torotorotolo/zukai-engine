# -*- coding: utf-8 -*-
"""31本目④'：親の差し替え（patches_base.json）・直す係（src/agents/wf31b/fix_F*.json）・当て直しと点検の直し（patches_r.json）・§ の直し（patches_sec.json）を
1本の差し替え表 patches31.json へまとめる（数を必ず突き合わせる・30本目 merge30.py を写した）。

  python -P ref/ep31/v2_build/merge31.py

- 順番＝base → F1〜F6 → r → sec（後ろの差し替えの old は前の差し替えのあとの字）。id の重なりは止める。
- 聞き役の役割は行の終わりで決まる（roles31.py）＝役割の表は持たない（「？」質問・「ね。」まとめ・ほか反応）。
- 読み＝fix_F*.json の yomi と yomi_extra.json を、§6 の表の末尾（「| 上役 | うわやく | |」の次）に足す差し替えを1本作る（同じ語は1行に）。
- 出すのは数だけ。終了コード 0＝組めた／1＝id の重なりか形の誤り。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
AG = os.path.join(EP, 'src', 'agents', 'wf31b')
ANCHOR = '| 上役 | うわやく | |'


def load(name):
    p = os.path.join(HERE, name)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else []


def main():
    base = load('patches_base.json')
    fixes = []
    yomi = {}
    per = {}
    for p in sorted(glob.glob(os.path.join(AG, 'fix_F*.json'))):
        d = json.load(open(p, encoding='utf-8'))
        ps = d.get('patches') or []
        per[os.path.basename(p)[4:6]] = len(ps)
        fixes += ps
        for y in d.get('yomi') or []:
            w = y['word'].strip()
            if w in yomi:
                yomi[w]['cuts'] = yomi[w]['cuts'] + '・' + y['cuts']
            else:
                yomi[w] = dict(y)
    rs = load('patches_r.json')
    sec = load('patches_sec.json') + load('patches_sec_num.json')
    yfrom = []
    for y in load('yomi_extra.json'):
        yomi[y['word'].strip()] = y
        yfrom += y.get('from') or []
    for w in load('yomi_drop.json'):
        yomi.pop(w, None)
    ypatch = []
    if yomi:
        rows = '\n'.join('| %s | %s | %s |' % (y['word'], y['reading'], y.get('cuts', '')) for y in yomi.values())
        ypatch = [{'id': 'S-YOMI', 'cut': '§', 'old': ANCHOR, 'new': ANCHOR + '\n' + rows,
                   'why': "④' の係と親の読みの所見をまとめて足した", 'from': yfrom}]
    all_p = base + fixes + rs + sec + ypatch
    ids = [p.get('id') for p in all_p]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        print('🔴 id の重なり', dup)
        return 1
    for p in all_p:
        if not p.get('move_after') and ('old' not in p or 'new' not in p or 'cut' not in p):
            print('🔴 形の誤り', p.get('id'))
            return 1
    json.dump(all_p, open(os.path.join(HERE, 'patches31.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print('差し替え %d＝親 %d・直す係 %s=%d・当て直しと点検 %d・§ %d・読み %d行（%d本）' % (
        len(all_p), len(base), per, len(fixes), len(rs), len(sec), len(yomi), len(ypatch)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
