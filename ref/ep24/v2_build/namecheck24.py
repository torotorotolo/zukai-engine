# -*- coding: utf-8 -*-
"""24本目④'：書かない名前の網（リポは公開＝撮影者の個人名・二次資料にしか無い人の名前を、リポに入るファイルに書かない）。

  python ref/ep24/v2_build/namecheck24.py <ファイル> [<ファイル> …]

網は2つ：
 1. 出さない名前＝v1_build/m24.py の NAMES_NG（カタカナ）＋そのラテン文字の綴り＝当たれば E。
    （台本に出してよいのは記録にある5人＝レガソフ・ジャトロフ・ヴォルコフ・ブリクス・ルイシコフ＝10-22 カズヤくんの決め）
 2. 撮影者の個人名＝src/credits_private.tsv（git の外）の**作者の列だけ**（注の行と見出しは飛ばす・機関名は除く）＝当たれば E。
当たった所は名前を伏せて「ファイル:行・語の頭1字＋○」だけ出す（この出力も gates.md に入る＝リポに名前を写さない）。
終了コード 0=0件 / 1=当たりあり / 2=作者の表が読めない（fail closed）
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(EP, 'v1_build'))
import m24                          # noqa: E402  NAMES_NG を使う

CRED = os.path.join(EP, 'src', 'credits_private.tsv')
LATIN_NG = ['Akimov', 'Toptunov', 'Bryukhanov', 'Brukhanov', 'Fomin', 'Pravik', 'Kibenok', 'Khodemchuk', 'Shashenok',
            'Telyatnikov', 'Ignatenko', 'Shcherbina', 'Kobzon', 'Perevozchenko', 'Lelechenko', 'Ananenko', 'Bezpalov', 'Baranov']
# 作者の列に入る機関名・許諾名（名前でない）＝網から除く語
ORG = {'iaea', 'imagebank', 'nasa', 'usgs', 'government', 'ministry', 'agency', 'commons', 'wikimedia', 'flickr', 'unknown',
       'author', 'the', 'of', 'and', 'photo', 'photographer', 'by', 'own', 'work', 'archive', 'archives', 'national', 'office',
       'press', 'service', 'ukraine', 'ukrainian', 'chernobyl', 'chornobyl', 'zone', 'state', 'http', 'https', 'www', 'com', 'org',
       # 10-22 ④'：作者の列の機関名の一部（衛星の会社・世界遺産の写真の名義）＝台本の英語の題と当たる一般語
       'heritage', 'spot', 'world', 'new', 'news', 'nuclear', 'safe', 'level'}


def author_tokens():
    if not os.path.exists(CRED):
        return None
    toks = set()
    for ln in open(CRED, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip():
            continue
        cols = ln.rstrip('\n').split('\t')
        if cols[0] == 'row' or len(cols) < 4:
            continue
        # 名前は大文字で始まる語だけ（作者の列には「from」「for」などの小文字の語も入る＝名前でない）
        for t in re.findall(r'[A-ZÀ-ÞА-Я][a-zà-ÿа-я]{2,}', cols[3]):
            if t.lower() not in ORG:
                toks.add(t)
    return toks


def mask(w):
    return w[0] + '○' * (len(w) - 1)


def main(files):
    toks = author_tokens()
    if toks is None:
        print('🔴 作者の表が読めない:', CRED)
        return 2
    nets = [(n, re.compile(re.escape(n))) for n in m24.NAMES_NG]
    nets += [(n, re.compile(r'\b' + re.escape(n) + r'\b', re.I)) for n in LATIN_NG]
    auth = [(n, re.compile(r'\b' + re.escape(n) + r'\b')) for n in sorted(toks)]
    hits = 0
    for f in files:
        try:
            lines = open(f, encoding='utf-8').read().split('\n')
        except Exception as e:
            print('🔴 読めない:', f, e)
            return 2
        for i, ln in enumerate(lines, 1):
            for kind, net in (('出さない名前', nets), ('撮影者の名前', auth)):
                for n, rx in net:
                    if rx.search(ln):
                        hits += 1
                        print('E %s:%d %s「%s」' % (os.path.basename(f), i, kind, mask(n)))
    print('名前の網：出さない名前 %d 語＋撮影者の語 %d（作者の列だけ）／ファイル %d／当たり %d' % (len(nets), len(auth), len(files), hits))
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
