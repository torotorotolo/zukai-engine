# -*- coding: utf-8 -*-
"""28本目④'：題の案の字数を数え、公開ずみの題（config/meta_*.json）と並べる（承認① の表の材料・ルール 4'-8＝型を全数照合・27本目 titles27b.py を写した）。

  python -P ref/ep28/v2_build/titles28.py

字数＝len()（全角も半角も1字・【】も数える＝27本目と同じ数え方）。上限 100（YouTube）。
型の網＝「真相」・死の語・犯人・加害者・流出（題に使わない）／札【事件検証】【ゆっくり解説】が末尾か／頭の語が「タイムズカー」か。
"""
import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
TAIL = '【事件検証】【ゆっくり解説】'
HEAD_A = 'タイムズカー情報漏洩事件 まとめ完全版（2026年10月時点）'
CANDS = [
    ('A（④の推奨）', HEAD_A + '退会した人の免許証の画像まで、7年間残されていた。' + TAIL),
    ('B', 'タイムズカー情報漏洩、いま分かっていること。会員は400万人あまり、漏えいは662万件あまり。' + TAIL),
    ('C', HEAD_A + '見舞金は3000円、訴えに加わりたい人は10万人を超えた。' + TAIL),
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
        if not t.startswith('タイムズカー'):
            flags.append('🔴 頭の語がタイムズカーでない')
        if len(t) > 100:
            flags.append('🔴 100字を超えた')
        print('%s %d字 %s\n    %s' % (k, len(t), '・'.join(flags) or '型の網 0', t))
    return 0


if __name__ == '__main__':
    sys.exit(main())
