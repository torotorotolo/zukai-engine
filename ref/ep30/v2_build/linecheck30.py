# -*- coding: utf-8 -*-
"""30本目：線の語の網（git の外の src/line_words.txt の語）を、台本と道具のファイルに全部当てる（namecheck30.py と同じ形）。
語そのものは出さない（当たった番号とファイルと行の番号だけ）。リポは公開＝commit の前に回す。
⚠️ 台本の頭の注と kousei・materials・sources の「線の説明」の行（語らない語を一般の語で挙げた所）にも当たる＝人が1行ずつ見る。

  python -P ref/ep30/v2_build/linecheck30.py ref/ep30/daihon_v1.md ...
終了コード 0=0件 / 1=当たった / 2=網のファイルが無い（fail closed）
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = os.path.join(os.path.dirname(HERE), 'src', 'line_words.txt')


def main(files):
    if not os.path.exists(WORDS):
        print('🔴 網のファイルが無い＝止める:', WORDS)
        return 2
    words = [ln.strip() for ln in open(WORDS, encoding='utf-8') if ln.strip() and not ln.startswith('#')]
    hits = 0
    for f in files:
        try:
            lines = open(f, encoding='utf-8').read().split('\n')
        except (OSError, UnicodeDecodeError) as e:
            print('⚠️ 読めない:', f, e)
            continue
        for i, ln in enumerate(lines, 1):
            for k, w in enumerate(words):
                if w and w in ln:
                    hits += 1
                    head = ln[:14].replace('`', '')
                    if any(x in head for x in words):     # 出力は gates.md としてリポへ入る＝行の頭に線の語があれば伏せる
                        head = '伏せた'
                    print('%s:%d に線の語 #%d（行の頭 %s）' % (os.path.basename(f), i, k + 1, head))
    print('線の語の網 %d語 × %dファイル → %d件' % (len(words), len(files), hits))
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
