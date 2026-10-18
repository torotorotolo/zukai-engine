# -*- coding: utf-8 -*-
"""23本目 映像方針：素材の記号 → 出どころ・大きさ・権利の表 sources23.psv を組む（2026-10-18・映像方針チャット）。

  python ref/ep23/eizou_build/make_sources23.py

入力：assign23.psv（使う記号）・ref/ep10/src/commons_all.json（Commons の題・大きさ・作者の別・sha1）・ref/stock/stock.json（フリー素材の札）
出力：sources23.psv（区切り「|」・手で直さない＝直すのはこのファイルの表 RESERVE・SIRE・HIST・PENDING）
🔴 名前（撮影者・投稿者・公務員）はこの表に書かない＝作者が個人の点は「作者欄のとおり（src/credits_private.tsv）」
"""
import json
import os
import sys
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
ALL = os.path.join(REPO, 'ref', 'ep10', 'src', 'commons_all.json')
STOCK = os.path.join(REPO, 'ref', 'stock', 'stock.json')
OUT = os.path.join(HERE, 'sources23.psv')

# 控え（割り当ては無いが、差し替えに備えて取る点）＝了承②の一覧に載せる
RESERVE = ['C3', 'C9', 'C24', 'C65', 'C82', 'C119', 'C122', 'C76', 'C81', 'C68', 'C33', 'C140', 'S60606']   # 10-18：個人名義の控え（C236・C213・C218・C229）は Commons が 429 で取っていない＝手元の 960px だけ

# 研究院（data.si.re.kr「사진으로 본 서울」＝公共ヌリ第1類型＋CC BY 4.0）：node → (何・年)
SIRE = {
    '52399': ('三豊百貨店（崩壊前）', '1995-06', 'local'), '52400': ('三豊百貨店（崩壊前）', '1995-06', 'local'),
    '52394': ('瑞草洞の法院', '1995-09〜10', ''), '52395': ('瑞草洞の法院（歩く人）', '1995-09〜10', ''),
    '52396': ('瑞草洞の法院（正面と中央の門）', '1995-09〜10', ''), '52397': ('瑞草洞の法院（通りの奥）', '1995-09〜10', ''),
    '52398': ('瑞草洞の法院（工事中のビルの向こう）', '1995-09〜10', ''),
    '50279': ('瑞草洞の通り（동아극장 주변）', '1995-10', ''),
    '53849': ('国会議事堂（正面と芝生）', '1996-04〜07', ''), '53868': ('国会議事堂（広場からの遠景）', '1996-04〜07', ''),
    '53880': ('国会議事堂の前の大通り', '1996-04〜07', ''),
    '60606': ('大法院（いま）', '2020-06', ''), '60607': ('大法院（いま）', '2020-06', ''),
    '31733': ('三豊百貨店の跡地', '2000-02', ''), '31735': ('三豊百貨店の跡地（掘った土）', '2000-02', ''),
    '31737': ('三豊百貨店の跡地', '2000-02', ''), '31740': ('三豊百貨店の跡地（空き地と後ろの団地）', '2000-02', ''),
}
# 歴史編纂院（history.seoul.go.kr「사진으로 보는 서울」＝公共ヌリ第1類型・撮影者の欄なし）：記号 → (番号・何・年・手元の名)
HIST = {
    'H109': ('2301030109', '崩れた翌日の現場（縦）', '1995-06-30', 'ref/ep10/src/kogl/hs_2301030109_0.jpg'),
    'H108': ('2301030108', '1階の玄関の売り台（崩壊後）', '1995-06', 'ref/ep10/src/kogl/hs_2301030108_0.jpg'),
    'H107': ('2301030107', '現場の整理と救助（俯瞰）', '1995-06', 'ref/ep10/src/kogl/hs_2301030107_0.jpg'),
    'H102': ('2301030102', '区民会館の合同の焼香所', '1995-07', 'ref/ep10/src/kogl/hs_2301030102_0.jpg'),
    'H104m': ('2301030104', '行方を探す掲示板（顔と名前にモザイク＝隠した版）', '1995-06', 'ref/ep10/missing_board_01.jpg'),
    'H510': ('2301030510', '司法研修院で市長の仕事を引き継ぐ新しい市長', '1995-07-01', ''),
    'H077': ('2301030077', '安全を考える三豊の写真展（市庁の地下道）', '1996-06-24', ''),
    'H083': ('2301030083', '1周年の大都市の防災行政セミナー', '1996-06-25', ''),
    'H100': ('2301030100', '慰霊塔の除幕（_2）', '1998-06-29', ''),
    'H101': ('2301030101', '慰霊塔の除幕（_1）＝控え', '1998-06-29', ''),
}
# まだ決まっていない記号（研究院の遠景の候補から選ぶ・フリー素材の新しい候補から選ぶ）
PENDING = {}   # 10-18：cc02・cc10 は法院の写真（52396・52397）に決めた＝遠景の候補は取らない
THUMB = {'C211': 1280}   # 10-18：原本の GET が 429 で取れなかった点＝標準の縮小版で取った
STOCK_CODES = {'P7830155': 'px_7830155', 'P29880216': 'px_29880216', 'P5571839': 'px_5571839'}   # 10-18 にコマで確かめた（px_6028858・pb_52888 は使わない）


def read_cand():
    p = os.path.join(HERE, 'stock23_cand.psv')
    rows = [ln.rstrip('\n') for ln in open(p, encoding='utf-8') if not ln.startswith('#') and ln.strip()]
    head = rows[0].split('|')
    return {r.split('|')[0]: dict(zip(head, r.split('|'))) for r in rows[1:]}


CAND = read_cand()


def used_codes():
    codes = []
    for ln in open(os.path.join(HERE, 'assign23.psv'), encoding='utf-8'):
        if ln.startswith('#') or not ln.strip():
            continue
        f = ln.rstrip('\n').split('|')
        m = f[2].split(':')[0]
        if m and m not in codes:
            codes.append(m)
    return codes


def commons_rows(codes):
    d = json.load(open(ALL, encoding='utf-8'))
    y95 = {r['no']: r for r in d['files'] if r.get('y95')}
    by_title = {r['title']: r for r in d['files']}
    rows = []
    for c in codes:
        if c == 'C2K001':
            r = by_title['2000년대 초반 서울소방 소방공무원(소방관) 활동 사진 삼풍001.jpg']
            no = None
        else:
            no = int(c[1:])
            r = y95[no]
        own = r['title'].startswith('Sampungdept')
        w, h = r['w'], r['h']
        if max(w, h) > 3840:
            get, dims = 'commons:3840', '%dx%d（原本）→ 幅3840 の標準の縮小版' % (w, h)
            fn = 'ref/ep23/src/commons/%s_3840.jpg' % c.lower()
        elif own and c in THUMB:
            get, dims = 'commons:%d' % THUMB[c], '%dx%d（原本）→ 幅%d の標準の縮小版（原本は 429）' % (w, h, THUMB[c])
            fn = 'ref/ep23/src/commons/%s_%d.jpg' % (c.lower(), THUMB[c])
        elif own:
            get, dims = 'commons:orig', '%dx%d' % (w, h)
            fn = 'ref/ep23/src/commons/%s.jpg' % c.lower()
        else:
            get, dims = 'local:960', '%dx%d（原本）→ 手元の Commons 標準の縮小版 960px（ref/ep10/src/commons_640/%03d.jpg を写す）' % (w, h, no)
            fn = 'ref/ep23/src/commons/%s_960.jpg' % c.lower()
        page = 'https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(r['title'].replace(' ', '_'))
        media = (r.get('url') or '').split('?')[0]
        rights = 'BY-SA 4.0（own＝作者は個人）' if own else 'BY-SA 4.0（本部）'
        credit = ('写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0' if own
                  else '写真：ソウル特別市 消防災難本部（CC BY-SA 4.0）')
        note = 'sha1 %s' % r.get('sha1', '')[:12]
        if c == 'C182':
            note += '・本部の但し書き（識別できる人は承認）の4点の1つ＝人物は豆粒'
        rows.append([c, 'photo', fn, page, media, get, dims, '', rights, credit, note])
    return rows


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    codes = used_codes()
    allc = codes + [c for c in RESERVE if c not in codes]
    rows = []
    rows += commons_rows([c for c in allc if c.startswith('C')])
    for c in allc:
        if c.startswith('S') and c[1:] in SIRE or c[1:] in SIRE and c.startswith('S'):
            n = c[1:]
            what, yr, loc = SIRE[n]
            fn = ('ref/ep10/src/kogl/sire_%s.jpg' % n) if loc == 'local' else ('ref/ep23/src/sire/sire_%s.jpg' % n)
            rows.append([c, 'photo', fn, 'https://data.si.re.kr/node/%s' % n, '頁のフォーム（이용목적 선택＝상업적 활용 →「사진 다운로드(1600px)」）',
                         'local' if loc == 'local' else 'sire:1600', '1600px 版', '', 'A（公共ヌリ第1類型＋CC BY 4.0）',
                         '写真：ソウル特別市／ソウル研究院（서울연구데이터서비스）（公共ヌリ第1類型・CC BY 4.0）', '%s・%s' % (what, yr)])
    for c in [x for x in SIRE if 'S' + x not in allc]:
        if SIRE[c][0].endswith('（候補）'):
            what, yr, loc = SIRE[c]
            rows.append(['S' + c, 'photo', 'ref/ep23/src/sire/sire_%s.jpg' % c, 'https://data.si.re.kr/node/%s' % c,
                         '頁のフォーム（同上）', 'sire:1600', '1600px 版', '', 'A（公共ヌリ第1類型＋CC BY 4.0）',
                         '写真：ソウル特別市／ソウル研究院（서울연구데이터서비스）（公共ヌリ第1類型・CC BY 4.0）', '%s・%s＝cc02・cc10 の候補' % (what, yr)])
    for c in allc + ['H101']:
        if c in HIST and not any(r[0] == c for r in rows):
            num, what, yr, loc = HIST[c]
            page = 'https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=%s&key=2211220005' % num
            fn = loc or 'ref/ep23/src/hist/hs_%s_0.jpg' % num
            rows.append([c, 'photo', fn, page, '頁のフォーム（자료 이용 조건 동의서）' if not loc else '手元（旧版の取得）',
                         'local' if loc else 'hist:form', '809×534 前後（CMYK）', '', 'A（公共ヌリ第1類型）',
                         '写真：ソウル歴史編纂院（公共ヌリ第1類型）' + ('・改変：顔と名前にモザイク' if c == 'H104m' else ''), '%s・%s・%s' % (num, what, yr)])
    st = json.load(open(STOCK, encoding='utf-8'))
    for c in allc:
        if c in STOCK_CODES:
            v = st[STOCK_CODES[c]]
            rows.append([c, 'stock', 'ref/stock/media/%s.mp4' % STOCK_CODES[c], v['page'], v['media'], 'local(ref/stock)',
                         '%s・%s秒' % (v['rendition'], v['sec']), str(v['size']), 'フリー素材（%s）' % v['license'], 'イメージ（%s）' % v['site'],
                         '%s（ref/stock の共用＝読むだけ・19本目で使用）' % v['what']])
        elif c.startswith('X') and c[1:] in CAND:
            v = CAND[c[1:]]
            ext = '.mp4' if v['kind'] == 'video' else '.jpg'
            lic = 'Pexels License' if v['site'] == 'Pexels' else 'Pixabay Content License'
            rows.append([c, 'stock', 'ref/ep23/src/stock/%s%s' % (c[1:], ext), v['page'], v['media'], 'stock',
                         '1920×1080 の版' if v['kind'] == 'video' else '幅1920 の版', v['bytes_head'], 'フリー素材（%s）' % lic, 'イメージ（%s）' % v['site'],
                         '%s（10-18 にコマで見て選んだ）' % v['title']])
        elif c.startswith('X'):
            rows.append([c, 'stock', '', '', '', 'pending', '', '', 'フリー素材（Pexels License／Pixabay Content License）', 'イメージ（サイト名）',
                         'フリー素材の候補から選ぶ（人なし・字なし・生成AIなし）'])
        elif c in PENDING:
            rows.append([c, 'photo', '', '', '', 'pending', '', '', 'A（公共ヌリ第1類型＋CC BY 4.0）',
                         '写真：ソウル特別市／ソウル研究院（서울연구데이터서비스）（公共ヌリ第1類型・CC BY 4.0）', PENDING[c]])
    head = ['# 23本目 映像方針（2026-10-18）素材の記号 → 出どころ・大きさ・権利（make_sources23.py が書く＝手で直さない）',
            '# 区切り「|」。get＝local（手元）／local:960（手元の Commons 標準の縮小版を写す）／commons:orig（原本・sha1 照合）／commons:3840（標準の縮小版）／sire:1600（研究院の頁のフォーム）／hist:form（歴史編纂院の頁のフォーム）／local(ref/stock)／pending（これから決める）',
            '# 🔴 名前は書かない（作者が個人の点は src/credits_private.tsv＝git の外）',
            'code|class|file|page|media|get|dims|bytes|rights|credit|note']
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(head) + '\n')
        for r in rows:
            f.write('|'.join(x.replace('|', '／') for x in r) + '\n')
    from collections import Counter
    print('記号 %d（割り当て %d・控え %d）' % (len(rows), len(codes), len([c for c in RESERVE if c not in codes])))
    print(dict(Counter(r[5] for r in rows)))
    print('→', OUT)


if __name__ == '__main__':
    main()
