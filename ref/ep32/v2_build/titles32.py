# -*- coding: utf-8 -*-
"""32本目④'：題の案の字数を数え、公開ずみの題（config/meta_*.json）と並べる（承認① の表の材料・ルール 4'-8＝型を全数照合・31本目 titles31.py を写した）。

  python -P ref/ep32/v2_build/titles32.py

字数＝len()（全角も半角も1字・【】も数える）。上限 100（YouTube）。
型の網＝死の語（犠牲・死亡）・この回で言わない語（208・奇跡的・墜落・拒否）・煽り語（衝撃・瞬間・闇・地獄・英雄）／
札【事故検証】【ゆっくり解説】が末尾か／頭が「【映像あり】ハドソン川の奇跡の真相。」か「ハドソン川の奇跡の真相。」か。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAIL = '【事故検証】【ゆっくり解説】'
HEAD = 'ハドソン川の奇跡の真相。'
NG = ('犠牲', '死亡', '208', '奇跡的', '墜落', '拒否', '衝撃', '瞬間', '闇', '地獄', '英雄', '犯人', '加害者')
CANDS = [
    ('A（④の推奨）', '【映像あり】' + HEAD + '判断の35秒を足して空港へ戻るシミュレーターの試しは、届かなかった。' + TAIL),
    ("A'（④' の推奨＝A に「滑走路に」）", '【映像あり】' + HEAD + '判断の35秒を足して空港へ戻るシミュレーターの試しは、滑走路に届かなかった。' + TAIL),
    ("A'（【映像あり】なし）", HEAD + '判断の35秒を足して空港へ戻るシミュレーターの試しは、滑走路に届かなかった。' + TAIL),
    ('A2', '【映像あり】' + HEAD + '空港に降りられた試しは、どれも、鳥とぶつかった直後に曲がった回だった。' + TAIL),
    ('B', '【映像あり】' + HEAD + '両方のエンジンが故障したときの手順書は3ページ。乗員がたどれたのは約3分の1だった。' + TAIL),
    ('C', '【映像あり】' + HEAD + '報告書は「奇跡」と書かず、成功の多くは「一連の偶然」によると書いた。' + TAIL),
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
    if ls:
        print('公開ずみの題 %d本・字数 %d〜%d（中央 %d）' % (len(ls), ls[0], ls[-1], ls[len(ls) // 2]))
    print('公開ずみの題（全数＝型の照合）:')
    for n, t in pub:
        tail = '札 末尾' if t.endswith(('【ゆっくり解説】', '【事故検証】', '【事件検証】')) else '札 ×'
        head = '頭＝【映像あり】' if t.startswith('【映像あり】') else ''
        shin = '「の真相。」' if 'の真相。' in t else ('「の真相」' if 'の真相' in t else '')
        print('  %s %d字 %s %s %s ／ %s' % (n[5:-5], len(t), tail, head, shin, t))
    for k, t in CANDS:
        flags = ['🔴「%s」' % w for w in NG if w in t]
        if not t.endswith(TAIL):
            flags.append('🔴 札が末尾に無い')
        if not (t.startswith(HEAD) or t.startswith('【映像あり】' + HEAD)):
            flags.append('🔴 頭の語の並びが型と違う')
        if len(t) > 100:
            flags.append('🔴 100字を超えた')
        print('%s %d字 %s\n    %s' % (k, len(t), '・'.join(flags) or '型の網 0', t))
    return 0


if __name__ == '__main__':
    sys.exit(main())
