# -*- coding: utf-8 -*-
"""33本目④'：題の案の字数を数え、公開ずみの題（config/meta_*.json）と並べる（承認① の表の材料・ルール 4'-8＝型を全数照合・32本目 titles32.py を写した）。

  python -P ref/ep33/v2_build/titles33.py

字数＝len()（全角も半角も1字・【】も数える）。上限 100（YouTube）。
型の網＝死の語（犠牲・死亡）・この回で言わない語（英国史上最悪・60時間・見捨て・生きたまま）・煽り語（衝撃・瞬間・闇・地獄・英雄・最悪）・
札【事故検証】【ゆっくり解説】が末尾か／頭が「グレンフェルタワー火災の真相。」か（【映像あり】は付けない＝② の決め）。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAIL = '【事故検証】【ゆっくり解説】'
HEAD = 'グレンフェルタワー火災の真相。'
NG = ('犠牲', '死亡', '英国史上最悪', '史上最悪', '60時間', '見捨て', '生きたまま', '衝撃', '瞬間', '闇', '地獄', '英雄', '犯人', '加害者', '最悪', '【映像あり】')
CANDS = [
    ('A（④の推奨）', HEAD + '外壁の板を選ぶ話し合いで、関わった人はみな見た目に集中し、火に強いかどうかを外していた。' + TAIL),
    ('B', HEAD + '台所のありふれた火は、3時間足らずで24階建ての塔を包んだ。' + TAIL),
    ('C', HEAD + '「部屋で待て」を改めるべき時から、1時間近くが失われた。' + TAIL),
]
EXTRA = os.path.join(HERE, 'titles33_extra.json')  # ④' で足す案（[["名", "題"], …]）


def published():
    out = []
    for p in sorted(glob.glob(os.path.join(REPO, 'config', 'meta_*.json'))):
        try:
            d = json.load(open(p, encoding='utf-8'))
        except (OSError, ValueError):
            continue
        t = d.get('title') if isinstance(d, dict) else None
        if t:
            out.append((os.path.split(p)[1], t))  # 名前の網の空鳴りを避ける書き方
    return out


def main():
    pub = published()
    ls = sorted(len(t) for _, t in pub)
    if ls:
        print('公開ずみの題 %d本・字数 %d〜%d（中央 %d）' % (len(ls), ls[0], ls[-1], ls[len(ls) // 2]))
    print('公開ずみの題（全数＝型の照合）:')
    for n, t in pub:
        tail = '札 末尾' if t.endswith(('【ゆっくり解説】', '【事故検証】', '【事件検証】')) else '札 ×'
        head = '頭＝【映像あり】' if t.startswith('【映像あり】') else ''
        shin = '「の真相。」' if 'の真相。' in t else ('「の真相」' if 'の真相' in t else '')
        print('  %s %d字 %s %s %s ／ %s' % (n[5:-5], len(t), tail, head, shin, t))
    cands = list(CANDS)
    if os.path.exists(EXTRA):
        cands += [tuple(x) for x in json.load(open(EXTRA, encoding='utf-8'))]
    for k, t in cands:
        flags = ['🔴「%s」' % w for w in NG if w in t]
        if not t.endswith(TAIL):
            flags.append('🔴 札が末尾に無い')
        if not t.startswith(HEAD):
            flags.append('🔴 頭の語の並びが型と違う')
        if len(t) > 100:
            flags.append('🔴 100字を超えた')
        print('%s %d字 %s\n    %s' % (k, len(t), '・'.join(flags) or '型の網 0', t))
    return 0


if __name__ == '__main__':
    sys.exit(main())
