# -*- coding: utf-8 -*-
"""29本目④'：題の案の字数を数え、公開ずみの題（config/meta_*.json）と並べる（承認① の表の材料・ルール 4'-8＝型を全数照合・28本目 titles28.py を写した）。

  python -P ref/ep29/v2_build/titles29.py

字数＝len()（全角も半角も1字・【】も数える＝27本目と同じ数え方）。上限 100（YouTube）。
型の網＝「真相」・死の語・犯人・加害者・流出（題に使わない）／札【事件検証】【ゆっくり解説】が末尾か／頭の語が「GMO」か。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAIL = '【事件検証】【ゆっくり解説】'
HEAD_A = 'GMO不正アクセス事件 まとめ完全版（2026年11月時点）'
CANDS = [
    ('A（④の推奨）', HEAD_A + '侵入から76日。調べ始めたきっかけは、利用者の問い合わせだった。' + TAIL),
    ('B', HEAD_A + 'なぜ2カ月半、気づけなかったのか。答えは、まだ出ていない。' + TAIL),
    ('C', HEAD_A + '2年前に指摘、8月に侵入、確かめたのは10月。' + TAIL),
    ('A2（④\' の推奨の1句・呼び名はそのまま）', HEAD_A + '侵入から76日、会社は気づけなかった。きっかけは利用者の問い合わせ。' + TAIL),
    ('A2＋呼び名「GMOへの」（④\' の推奨）', 'GMOへの不正アクセス事件 まとめ完全版（2026年11月時点）侵入から76日、会社は気づけなかった。きっかけは利用者の問い合わせ。' + TAIL),
    ('A＋呼び名「問題」', 'GMO不正アクセス問題 まとめ完全版（2026年11月時点）侵入から76日。調べ始めたきっかけは、利用者の問い合わせだった。' + TAIL),
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
        if '真相' in t:
            flags.append('🔴「真相」')
        for w in ('死亡', '犯人', '加害者', '流出'):
            if w in t:
                flags.append('🔴「%s」' % w)
        if not t.endswith(TAIL):
            flags.append('🔴 札が末尾に無い')
        if not t.startswith('GMO'):
            flags.append('🔴 頭の語が GMO でない')
        if len(t) > 100:
            flags.append('🔴 100字を超えた')
        print('%s %d字 %s\n    %s' % (k, len(t), '・'.join(flags) or '型の網 0', t))
    return 0


if __name__ == '__main__':
    sys.exit(main())
