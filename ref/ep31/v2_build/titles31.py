# -*- coding: utf-8 -*-
"""31本目④'：題の案の字数を数え、公開ずみの題（config/meta_*.json）と並べる（承認① の表の材料・ルール 4'-8＝型を全数照合・30本目 titles30.py を写した）。

  python -P ref/ep31/v2_build/titles31.py

字数＝len()（全角も半角も1字・【】も数える）。上限 100（YouTube）。
型の網＝死の語・「犯人」「加害者」・煽り語（衝撃・瞬間・闇・地獄）／札【事故検証】【ゆっくり解説】が末尾か／頭が「【映像あり】全日空機雫石衝突事故の真相。」か「全日空機雫石衝突事故の真相。」か。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAIL = '【事故検証】【ゆっくり解説】'
HEAD = '全日空機雫石衝突事故の真相。'
CANDS = [
    ('A（④の推奨）', '【映像あり】' + HEAD + 'その朝の訓練の空は、旅客機の道が載っていない地図の上で、幹部が指で示して決めていた。' + TAIL),
    ('A2', '【映像あり】' + HEAD + '訓練の空は、旅客機の道が載っていない地図の上で、指で示して決められた。' + TAIL),
    ('B（④の案）', '【映像あり】' + HEAD + '最高裁は、教官ひとりに責任を負わせるのは「酷に過ぎる」と書いた。' + TAIL),
    ("B'（④'＝対象を判決の文に）", '【映像あり】' + HEAD + '最高裁は、教官ひとりに刑事責任をすべて負わせ、4年の実刑にするのは「酷に過ぎる」と書いた。' + TAIL),
    ('C', '【映像あり】' + HEAD + '接触は14時2分39秒か、32秒か。報告書と防衛庁の7秒の食い違い。' + TAIL),
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
        flags = []
        for w in ('死亡', '犯人', '加害者', '衝撃', '瞬間', '闇', '地獄'):
            if w in t:
                flags.append('🔴「%s」' % w)
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
