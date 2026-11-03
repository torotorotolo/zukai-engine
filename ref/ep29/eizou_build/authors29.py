# -*- coding: utf-8 -*-
"""29本目 映像方針（2026-11-03・チャット5）：Commons の撮影者の表と、名前の網を git の外に作る（名前は画面に出さない＝数だけ出す）。28本目の authors28.py を写した。

  python -I ref/ep29/eizou_build/authors29.py
入力：src/commons/commons_meta29_{cats,more,public,terms}.tsv（目録・8列目＝作者）・src/commons/geo29.json（API の Artist）・eizou_build/sources29.psv（使う点）
出力（どれも git の外）：src/credits_private.tsv（記号→作者＝⑤b で画面の「{作者}」に差し込む）・src/names_commons.txt（名前の網＝v2_build/namecheck29.py が読む）
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')
META = {'CM': 'commons_meta29_cats.tsv', 'M': 'commons_meta29_more.tsv', 'P': 'commons_meta29_public.tsv', 'T': 'commons_meta29_terms.tsv'}
SKIP = {'own work', 'flickr', 'commons', 'wikimedia', 'user', 'unknown', 'japan', 'sweden', 'stockholm', 'from', 'the', 'and',
        # 目録の作者の欄に入っている機関名と一般の語＝名前でない（28本目 11-01・29本目で足した）
        'tokyo', 'artist', '投稿者', 'panoramio', 'kyoto', 'yokohama', 'wikipedia', 'self', 'photo', 'shibuya',
        '内閣官房内閣広報室', '首相官邸ホームページ', 'gmo registry', '国土交通省', '警察庁', '財務省', '総務省', '金融庁', 'デジタル庁', '内閣府'}


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


def load(fn):
    with open(os.path.join(SRC, 'commons', fn), encoding='utf-8') as f:
        return [ln.rstrip('\n').split('\t') for ln in f if ln.strip()]


def main():
    tables = {k: load(v) for k, v in META.items()}
    geo = json.load(open(os.path.join(SRC, 'commons', 'geo29.json'), encoding='utf-8'))
    used = []
    with open(os.path.join(HERE, 'sources29.psv'), encoding='utf-8') as f:
        for ln in f:
            code = ln.split('|')[0]
            if re.match(r'(CM|M|P|T)\d+$', code) and '|commons-photo|' in ln:
                used.append(code)
    names = set()
    # 網は「使う点と見本帳で見た点」の撮影者＝目録まるごとだと一般の語が混ざる（機関の写真の目録が大きい）
    for g in geo.values():
        if g.get('artist'):
            names |= parts(plain(g['artist']))
    for code in list(geo) + used:
        m = re.match(r'(CM|M|P|T)(\d+)$', code)
        r = tables[m.group(1)][int(m.group(2))]
        if len(r) > 7 and r[7].strip():
            names |= parts(plain(r[7]))
    rows = []
    for code in used:
        m = re.match(r'(CM|M|P|T)(\d+)$', code)
        r = tables[m.group(1)][int(m.group(2))]
        a = plain(geo.get(code, {}).get('artist')) or (r[7] if len(r) > 7 else '')
        rows.append((code, a))
    with open(os.path.join(SRC, 'credits_private.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 29本目 Commons の撮影者（git の外・⑤b で画面の「{作者}」に差し込む）\ncode\tauthor\n')
        for code, a in rows:
            f.write('%s\t%s\n' % (code, a))
    with open(os.path.join(SRC, 'names_commons.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# Commons の撮影者（29本目 映像方針・見本帳で見た点と使う点から）＝リポに書かない\n')
        for n in sorted(names):
            f.write(n + '\n')
    empty = [c for c, a in rows if not a]
    print('作者の表 %d 点（空 %d：%s）・名前の網 %d 語 → src/credits_private.tsv・src/names_commons.txt' % (len(rows), len(empty), ' '.join(empty), len(names)))


if __name__ == '__main__':
    main()
