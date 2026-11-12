# -*- coding: utf-8 -*-
"""33本目④'：Commons の候補（git の外 src/commons/cand33.json の通し番号 #1〜#130）を番号で引く（読むだけ・係と親が使う）。

  python -P ref/ep33/v2_build/cand33.py 7 12 8 3

出すもの＝#番号・ファイル名・権利・撮影日・大きさ・説明の頭（200字）。撮影者の欄は出さない。
名前の網（src/names_private.txt・names_commons.txt の語）に当たる字は〈名〉に伏せる。番号が無ければ何も出さずに終了コード 2。
⚠️ 伏せる網にも穴がありうる＝人の名前らしい字が見えたら、写さずに親へ申告する。
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')


def net():
    words = []
    for p in ('names_private.txt', 'names_commons.txt'):
        fp = os.path.join(SRC, p)
        if os.path.exists(fp):
            words += [w.strip() for w in open(fp, encoding='utf-8') if w.strip() and not w.startswith('#') and len(w.strip()) >= 4]
    if not words:
        return None
    words.sort(key=len, reverse=True)
    return re.compile('|'.join(re.escape(w) for w in words), re.I)


def main(argv):
    nums = [int(a.lstrip('#')) for a in argv[1:] if a.lstrip('#').isdigit()]
    if not nums:
        print('番号が要る（例：7 12 8）＝何も出さない')
        return 2
    rx = net()
    if rx is None:
        print('🔴 名前の網が無い＝止める')
        return 2
    files = json.load(open(os.path.join(SRC, 'commons', 'cand33.json'), encoding='utf-8'))['files']
    for n in nums:
        if not 1 <= n <= len(files):
            print('#%d は無い（1〜%d）' % (n, len(files)))
            continue
        e = files[n - 1]
        def m(s):
            return rx.sub('〈名〉', str(s or ''))
        print('#%d ｜ %s ｜ 権利 %s ｜ 撮影 %s ｜ %s×%s ｜ 分類 %s' % (
            n, m(e.get('title')), m(e.get('lic')), m(e.get('date')), e.get('w'), e.get('h'), m(e.get('cat'))))
        print('   説明: %s' % m(e.get('desc'))[:200].replace('\n', ' '))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
