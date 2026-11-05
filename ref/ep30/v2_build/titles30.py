# -*- coding: utf-8 -*-
"""30本目④'：題の案の字数を数え、公開ずみの題（config/meta_*.json）と並べる（承認① の表の材料・ルール 4'-8＝型を全数照合・29本目 titles29.py を写した）。

  python -P ref/ep30/v2_build/titles30.py

字数＝len()（全角も半角も1字・【】も数える）。上限 100（YouTube）。
型の網＝死の語・「犯人」・煽り語（衝撃・瞬間・闇・地獄）／札【事件検証】【ゆっくり解説】が末尾か／頭が「【映像あり】地下鉄サリン事件の真相。」か「地下鉄サリン事件の真相。」か。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAIL = '【事件検証】【ゆっくり解説】'
HEAD = '地下鉄サリン事件の真相。'
CANDS = [
    ('A（④の推奨）', '【映像あり】' + HEAD + '前の年に松本で同じ毒が使われ、4か月前には土から手がかりが出ていた。' + TAIL),
    ('B', '【映像あり】' + HEAD + '最初の知らせは「病人2名」と「ガソリンの匂い」。サリンと伝わるまで約3時間半。' + TAIL),
    ('C', '【映像あり】' + HEAD + '助けに入った消防職員135人も負傷した。現場は何を知らされていなかったのか。' + TAIL),
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
    print('公開ずみの題 %d本・字数 %d〜%d（中央 %d）' % (len(ls), ls[0], ls[-1], ls[len(ls) // 2]))
    print('公開ずみの題（全数＝型の照合）:')
    for n, t in pub:
        tail = '札 末尾' if t.endswith(('【ゆっくり解説】', '【事故検証】', '【事件検証】')) else '札 ×'
        print('  %s %d字 %s ／ %s' % (n[5:-5], len(t), tail, t))
    for k, t in CANDS:
        flags = []
        for w in ('死亡', '犯人', '衝撃', '瞬間', '闇', '地獄'):
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
