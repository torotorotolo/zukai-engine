# -*- coding: utf-8 -*-
"""22本目④'：書かない名前の網（リポは公開＝私人の名前と CEO の名前をリポに入るファイルに書かない）。

  python ref/ep22/v2_build/namecheck22.py <ファイル> [<ファイル> …]

名前の一覧は git の外の ref/ep22/src/names_private.txt（1行1語・末尾の ! は大文字小文字を区別）。
当たった所は名前を伏せて「ファイル:行・語の頭1字＋○」だけ出す（この出力も gates.md に入る＝リポに名前を写さない）。
あわせて、バッククォートの中の英字の「Aaa Bbb」形（人名らしい2語）を数だけ出す（中身は人が見る＝--show で出す）。
終了コード 0=名前0 / 1=名前あり / 2=一覧が読めない（fail closed）
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
LIST = os.path.join(os.path.dirname(HERE), 'src', 'names_private.txt')
PAIR = re.compile(r'\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b')


def load():
    if not os.path.exists(LIST):
        return None
    out = []
    for ln in open(LIST, encoding='utf-8'):
        w = ln.strip()
        if not w or w.startswith('#'):
            continue
        cs = w.endswith('!')
        w = w.rstrip('!')
        if re.fullmatch(r'[A-Za-z\-]+', w):
            out.append((w, re.compile(r'\b%s\b' % re.escape(w), 0 if cs else re.I)))
        else:
            out.append((w, re.compile(re.escape(w))))
    return out


def main(files, show):
    pats = load()
    if not pats:
        print('🔴 名前の一覧が読めない（%s）＝測れていない' % LIST)
        return 2
    hits, pairs = [], 0
    for f in files:
        if os.path.abspath(f) == os.path.abspath(__file__):
            continue
        for i, ln in enumerate(open(f, encoding='utf-8', errors='replace'), 1):
            for w, rx in pats:
                if rx.search(ln):
                    hits.append('%s:%d  %s○' % (os.path.basename(f), i, w[0]))
            for q in re.findall(r'`([^`]+)`', ln):
                for m in PAIR.finditer(q):
                    pairs += 1
                    if show:
                        print('  人名らしい2語？ %s:%d  %s' % (os.path.basename(f), i, m.group(0)))
    print('書かない名前 %d件（%dファイル・一覧 %d語）／引用の中の「Aaa Bbb」形 %d件（--show で中身）' % (len(hits), len(files), len(pats), pairs))
    for h in hits:
        print('  ✗', h)
    return 1 if hits else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    sys.exit(main([x for x in a if not x.startswith('--')], '--show' in a))
