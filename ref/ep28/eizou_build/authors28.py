# -*- coding: utf-8 -*-
"""28本目 映像方針（2026-11-01・チャット5）：Commons の撮影者の表と、名前の網を git の外に作る（名前は画面に出さない＝数だけ出す）。27本目の authors27.py を写した。

  python -I ref/ep28/eizou_build/authors28.py
入力：src/commons/commons_meta28_cats.tsv（130点の目録・8列目＝作者）・src/commons/geo28.json（API の Artist）・eizou_build/sources28.psv（使う点）
出力（どれも git の外）：src/credits_private.tsv（記号→作者＝⑤b で画面の「{作者}」に差し込む）・src/names_commons.txt（名前の網＝v2_build/namecheck28.py が読む）
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')
SKIP = {'own work', 'flickr', 'commons', 'wikimedia', 'user', 'unknown', 'japan', 'sweden', 'stockholm', 'from', 'the', 'and',
        # 28本目（11-01）：目録の作者の欄に入っていた機関名と一般の語＝名前でない（台本・sources・materials に当たって分かった）
        'park24', 'tokyo', 'artist', '国土交通省', '投稿者', '警察庁', 'times', 'panoramio', 'kyoto', 'yokohama', 'mazda', 'wikipedia', 'self', 'photo'}


def plain(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    return re.sub(r'\s+', ' ', s).strip()


def parts(name):
    out = {name}
    for p in re.split(r'[()（）,、/／]| from ', name):
        p = p.strip()
        if len(p) >= 3 and p.lower() not in SKIP:
            out.add(p)
    return {p for p in out if len(p) >= 3 and p.lower() not in SKIP}


def main():
    meta = [ln.rstrip('\n').split('\t') for ln in open(os.path.join(SRC, 'commons', 'commons_meta28_cats.tsv'), encoding='utf-8') if ln.strip()]
    geo = json.load(open(os.path.join(SRC, 'commons', 'geo28.json'), encoding='utf-8'))
    used = [ln.split('|')[0] for ln in open(os.path.join(HERE, 'sources28.psv'), encoding='utf-8')
            if ln.startswith('CM')]
    names = set()
    for r in meta:
        if len(r) > 7 and r[7].strip():
            names |= parts(plain(r[7]))
    for g in geo.values():
        if g.get('artist'):
            names |= parts(plain(g['artist']))
    rows = []
    for code in used:
        a = plain(geo.get(code, {}).get('artist')) or (meta[int(code[2:])][7] if len(meta[int(code[2:])]) > 7 else '')
        rows.append((code, a))
    with open(os.path.join(SRC, 'credits_private.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 28本目 Commons の撮影者（git の外・⑤b で画面の「{作者}」に差し込む）\ncode\tauthor\n')
        for code, a in rows:
            f.write('%s\t%s\n' % (code, a))
    with open(os.path.join(SRC, 'names_commons.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Commons の撮影者（28本目 映像方針・目録130点と API の Artist から）＝リポに書かない\n')
        for n in sorted(names):
            f.write(n + '\n')
    empty = [c for c, a in rows if not a]
    print('作者の表 %d 点（空 %d：%s）・名前の網 %d 語 → src/credits_private.tsv・src/names_commons.txt' % (len(rows), len(empty), ' '.join(empty), len(names)))


if __name__ == '__main__':
    main()
