# -*- coding: utf-8 -*-
"""27本目④'：題の案の字数を数え、公開ずみの題（config/meta_*.json）の字数の幅と並べる（承認① の表の材料）。

  python -P ref/ep27/v2_build/titles27b.py

字数＝len()（全角も半角も1字・【】も数える＝④ の titles27.py と同じ数え方）。上限 100（YouTube）。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAIL = '【事件検証】【ゆっくり解説】'
HEAD = '別府ひき逃げ殺傷事件、八田與一容疑者の4年。'
CANDS = [
    ('A（④の推奨・いま）', HEAD + '寄せられた情報は1万3978件、本人と確かめられた目撃は、まだ報じられていない。' + TAIL),
    ('A2（④\'の推奨）', HEAD + '寄せられた情報は1万3978件、逮捕につながる有力な手がかりは、まだ得られていない。' + TAIL),
    ('B', HEAD + '足取りが途絶えた港の海を、警察は2日間調べた。' + TAIL),
    ('C', HEAD + '道路交通法違反で全国初の重要指名手配は、殺人の疑いに変わった。' + TAIL),
]


def published():
    out = []
    for p in sorted(glob.glob(os.path.join(REPO, 'config', 'meta_*.json'))):
        try:
            d = json.load(open(p, encoding='utf-8'))
        except (OSError, ValueError):
            continue
        t = d.get('title') if isinstance(d, dict) else None
        if t:
            out.append((os.path.basename(p), t))
    return out


def main():
    pub = published()
    ls = sorted(len(t) for _, t in pub)
    rec = [(n, t) for n, t in pub if n in ('meta_ep21.json', 'meta_ep22.json', 'meta_ep23.json', 'meta_ep24.json',
                                            'meta_ep25.json', 'meta_ep26.json')]
    print('公開ずみの題 %d本・字数 %d〜%d（中央 %d）' % (len(ls), ls[0], ls[-1], ls[len(ls) // 2]))
    print('直近6本（21〜26本目）: ' + '・'.join('%s %d字' % (n[5:-5], len(t)) for n, t in rec))
    for k, t in CANDS:
        flags = []
        if '真相' in t:
            flags.append('🔴「真相」')
        for w in ('死亡', '犯人', '殺人犯'):
            if w in t:
                flags.append('🔴「%s」' % w)
        if '八田與一' in t and '八田與一容疑者' not in t:
            flags.append('🔴 容疑者が無い')
        if not t.endswith(TAIL):
            flags.append('🔴 札が末尾に無い')
        print('%s %d字 %s\n    %s' % (k, len(t), '・'.join(flags) or '型の網 0', t))
    return 0


if __name__ == '__main__':
    sys.exit(main())
