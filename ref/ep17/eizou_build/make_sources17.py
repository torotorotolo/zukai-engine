# -*- coding: utf-8 -*-
"""17本目 映像方針：素材の記号 → 出どころ・権利・大きさの表 sources17.psv を書く（2026-10-19）。手で sources17.psv を直さない＝ここを直して回す。

  python ref/ep17/eizou_build/make_sources17.py

- 報告書（S1）の写真・付図・頁＝手元の PDF（ref/ep17/src/jtsb_96-5_ja_0N.pdf・印刷頁は probe/pagemap.json）＝⑤b で頁から切り出す
- Commons＝②の台帳 ref/ep17/commons_cal_a300.tsv・commons_accident.tsv から題で引く（題・大きさ・権利・頁の URL を手で写さない）
- 新しい候補（Commons の係・フリー素材の係が頁の文字で探した物）＝cand17.psv（記号|class|page|media|dims|bytes|rights|note）
- 決まっていない記号は get=pending（make_list17.py が ⚠️ にする）
🔴 作者の名前はここに書かない（公開リポ）＝作者が個人の点は src/credits_private.tsv（git の外）
"""
import csv
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'sources17.psv')
CAND = os.path.join(HERE, 'cand17.psv')
S1 = '運輸省 航空事故調査委員会『航空事故調査報告書 96-5』%s（加工して作成）'
HEAD = ['code', 'class', 'file', 'page', 'media', 'get', 'dims', 'bytes', 'rights', 'credit', 'note']

# 報告書の写真（S1 写真N・印刷頁・PDF の分冊）＝PDL1.0
PHOTOS = [  # 記号, 写真の番号, 印刷頁, 分冊, 題（報告書）
    ('R01', 1, 136, 5, '事故現場（滑走路34の南側上空から）'), ('R02', 2, 137, 5, '事故現場（滑走路34末端付近上空から）'),
    ('R03', 3, 138, 5, '事故現場全景'), ('R04', 4, 139, 5, '救難作業状況（夜）'), ('R05', 5, 140, 5, '左エルロン'),
    ('R08', 8, 141, 5, 'バーチカル・スタビライザ及びラダー'), ('R09', 9, 142, 6, '左エレベータ'), ('R10', 10, 142, 6, '右エレベータ'),
    ('R11', 11, 143, 6, 'THS'), ('R12', 12, 143, 6, 'THS ジャッキ・スクリュウ'), ('R13', 13, 144, 6, 'フラップ・スラット'),
    ('R27', 27, 151, 6, '操縦室前方窓及び上部外板'), ('R29', 29, 152, 7, '胴体前方部外板'), ('R31', 31, 153, 7, 'No.1エンジン'),
    ('R35', 35, 155, 7, 'センタ・ペデスタル1'), ('R36', 36, 155, 7, 'センタ・ペデスタル2'), ('R37', 37, 156, 7, 'スラスト・レバー及びゴー・レバー'),
    ('R38', 38, 156, 7, 'SLATS/FLAPS レバー'), ('R39', 39, 157, 7, 'THS マニュアル・トリム・ホイール'), ('R40', 40, 157, 7, 'L/G レバー'),
    ('R41', 41, 158, 7, '計器盤及び破損した計器'), ('R42', 42, 158, 7, 'キャプテン・アンド・センタ・ライトパネル'), ('R43', 43, 159, 7, 'DFDR'),
    ('R44', 44, 159, 7, 'CVR'), ('R49', 49, 162, 8, '左主脚の接地痕'),
]
# 報告書の付図・頁（S1）＝PDL1.0
PAGES = [  # 記号, 印刷頁, 分冊, 何
    ('F01', 106, 4, '付図1 飛行計画経路図'), ('F03', 108, 4, '付図3 計器進入方式図（名古屋 ILS RWY34）'),
    ('F04', 109, 4, '付図4 航跡概略図（🔴 頁の中で横倒し＝起こして切り出す・時刻は世界共通の時刻）'),
    ('F05', 110, 4, '付図5 拡大航跡図（時刻ごとの角度と速さの表・時刻は世界共通の時刻）'), ('F08', 113, 4, '付図8 名古屋空港見取図'),
    ('F09', 114, 4, '付図9 事故現場地上痕跡図'), ('F11', 116, 5, '付図11 主要残骸散乱図'), ('F12', 117, 5, '付図12 火災痕跡図'),
    ('F28', 134, 5, '付図28 THS の動作（DFDR の記録）'), ('F29', 135, 5, '付図29 FMA 表示の推定（🔴 題に「推定」）'),
    ('P51', 163, 8, '写真51 分割したスラスト・レバー及びゴー・レバーとの位置関係（右上の線画は製造者由来の可能性＝頁ごと・なぞらない）'),
    ('P95', 95, 3, '本文 p.95「4 原因」（文字の頁）'),
]
# Commons（②の台帳から題で引く）：記号 → 題の頭・取り方・何
COMMONS = [
    ('E1', 'Photo of China Airlines Airbus A300B4-622R B-1816 at Nagoya', 'commons:orig', '事故機 B-1816（1993-04-13・名古屋空港）＝額装・無加工'),
    ('E2', 'CI A300 B-1816.jpg', 'commons:3840', '事故機 B-1816（撮影日不明・香港の啓徳）＝額装・無加工'),
    ('E3', 'China Airlines B-1816 Airbus A300 at HK Airport.jpg', 'commons:orig', '事故機 B-1816（1991-09-30・香港・脚を出した進入）＝額装・無加工（GFDL は BY-SA と同じ扱い）'),
    ('T1', 'HONG KONG KAI TAK 19 OCT 1993 CHINA AIRLINES AIRBUS A300 B-1814.jpg', 'commons:orig', '同じ型の姉妹機 B-1814（1993-10-19・香港の着陸進入）＝切り出し可（改変の旨）'),
    ('K05', 'ChinaAirlines A300 fukuoka 20050925102120.jpg', 'commons:orig', '中華航空の同じ系列の A300-600R（2005-09-25・福岡）＝前例の機体ではない'),
    ('K04', 'ChinaAirlines A300 fukuoka 20041023102346.jpg', 'commons:orig', '中華航空の同じ系列の A300-600R（2004-10-23・福岡）'),
    ('K05b', 'ChinaAirlines A300 fukuoka 20050429102946.jpg', 'commons:orig', '中華航空の同じ系列の A300-600R の別の機体（2005-04-29・福岡）'),
    ('B192', 'HONG KONG KAI TAK FEB 1998 CHINA AIRLINES AIRBUS A300 B-192', 'commons:orig', '中華航空の A300（1998-02・香港）＝事故の4年後・別の機体'),
    ('B194', 'HONG KONG KAI TAK FEB 1998 CHINA AIRLINES AIRBUS A300 B-194', 'commons:orig', '中華航空の A300（1998-02・香港）＝別の機体'),
    ('N1810', 'China Airlines Airbus A300B4-220 (B-1810-179).jpg', 'commons:3840', '中華航空の A300B4-220（1992年ごろ・名古屋空港）＝別の機体・額装・無加工'),
]
# そのほかの決まった素材
STATIC = [
    ['V1', 'video', 'ref/ep17/src/v1/heisei6_bouei_kiroku.mp4', 'https://www.youtube.com/watch?v=WQTZQU1VOC4', '（yt-dlp・形式 399＝1080p）', 'yt-dlp（了承②のあと）',
     '1920x1080（中身は4:3・実効は標準画質）', '—', 'CC BY 3.0', '防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0・改変：切り出し）',
     '12:37〜13:12「中華航空機墜落事故への対応」。使う秒＝12:37〜12:44・12:51〜12:56・12:57〜13:05／使わない＝12:45〜12:50（覆われたものの近景）・13:06〜13:12'],
    ['L64', 'page', 'ref/ep17/src/faa_hf_team_1996.pdf', 'L1 PDF p.64（図4）', '—', 'local:pdf', '頁', '—', 'PD（米連邦政府）', 'FAA Human Factors Team (1996) Figure 4', 'ゴー・アラウンドのスイッチと自動推力を切るスイッチの位置（機種ごと）'],
    ['L80', 'page', 'ref/ep17/src/faa_hf_team_1996.pdf', 'L1 PDF p.80', '—', 'local:pdf', '頁', '—', 'PD（米連邦政府）', 'FAA Human Factors Team (1996) p.80', '前触れの例（A310・文字の頁）'],
    ['L03', 'page', 'ref/ep17/src/faa_hf_team_1996.pdf', 'L1 PDF p.3（序文）', '—', 'local:pdf', '頁', '—', 'PD（米連邦政府）', 'FAA Human Factors Team (1996) 序文', '名古屋の事故から始まる段（文字の頁）'],
    ['J1', 'page', 'ref/ep17/src/court_2003-12-26_H7wa4179.pdf', 'S2 PDF p.1（主文）', '—', 'local:pdf', '頁', '—', '判決（著作権の目的とならない・著作権法13条）', '名古屋地方裁判所 2003年12月26日判決（平成7(ワ)4179）', '主文（文字の頁）'],
    ['J98', 'page', 'ref/ep17/src/court_2003-12-26_H7wa4179.pdf', 'S2 PDF p.98', '—', 'local:pdf', '頁', '—', '判決（著作権の目的とならない・著作権法13条）', '名古屋地方裁判所 2003年12月26日判決（平成7(ワ)4179）', '警告の判断の段（文字の頁）'],
]
for i, what in enumerate(['現在の県営名古屋空港と航空自衛隊小牧基地（上から）', '滑走路の南の端と着陸帯（斜めから）', '南から滑走路へ向かう進入の道すじ（斜めから）',
                          '滑走路の東側・当時の消防の待機所があった辺り', '空港の北の端・北門の辺り', '県営名古屋空港の全体（上から）'], 1):
    STATIC.append(['G%d' % i, 'google', 'ref/ep17/photo/g%d.png（⑤b で撮る）' % i, 'Google Earth', '—', 'capture:⑤b（gshot の型）', '1920x1080', '—',
                   'Google（Geo Guidelines）', 'Google Earth（画面の表記を絵の近くに）', what])
# 決まっていない記号（係の候補が届いたら cand17.psv に入れる＝そこにあれば上書き）
PENDING = []   # 10-19：係の候補はすべて cand17.psv に入れた（Q1〜Q4 → QA〜QD など）


def commons_rows():
    by_title = {}
    for fn in ('commons_cal_a300.tsv', 'commons_accident.tsv'):
        for r in csv.DictReader(open(os.path.join(EP, fn), encoding='utf-8'), delimiter='\t'):
            by_title.setdefault(r['title'][5:], r)
    out = []
    for code, head, get, what in COMMONS:
        hits = [t for t in by_title if t.startswith(head)]
        if len(hits) != 1:
            raise SystemExit('Commons の題が1つに決まらない：%s → %s' % (code, hits))
        r = by_title[hits[0]]
        lic = r['lic'].replace('CC BY-SA', 'BY-SA')
        media = r['url'].split('?')[0]
        name = 'ref/ep17/src/commons/%s.jpg' % code.lower()
        out.append([code, 'photo', name, r['page'], media, get, '%sx%s' % (r['w'], r['h']), '—', lic,
                    'Wikimedia Commons「%s」（%s）＝作者は src/credits_private.tsv' % (hits[0], r['lic']), what])
    return out


def main():
    rows = []
    for code, no, pg, vol, title in PHOTOS:
        rows.append([code, 'photo', 'ref/ep17/src/jtsb_96-5_ja_%02d.pdf' % vol, 'S1 p.%d 写真%d' % (pg, no), '—', 'local:pdf（⑤b で頁から切り出す）',
                     '頁 400dpi から', '—', 'PDL1.0', S1 % ('写真%d' % no), title])
    for code, pg, vol, what in PAGES:
        rows.append([code, 'page', 'ref/ep17/src/jtsb_96-5_ja_%02d.pdf' % vol, 'S1 p.%d' % pg, '—', 'local:pdf（⑤b で頁を書き出す）', '頁', '—', 'PDL1.0',
                     S1 % what.split('（')[0].split(' ')[0], what])
    rows += commons_rows()
    rows += STATIC
    cand = {}
    if os.path.exists(CAND):
        for ln in open(CAND, encoding='utf-8'):
            if ln.startswith('#') or not ln.strip():
                continue
            v = ln.rstrip('\n').split('|')
            if v[0] == 'code':
                continue
            cand[v[0]] = v
    def from_cand(c):   # code|class|page|media|dims|bytes|rights|get|file|credit|note
        return [c[0], c[1], c[8], c[2], c[3], c[7], c[4], c[5], c[6], c[9], c[10]]
    for code, cls, what in PENDING:
        if code in cand:
            rows.append(from_cand(cand[code]))
        else:
            rows.append([code, cls, '—', '—', '—', 'pending', '—', '—', '—', '—', what])
    done = {r[0] for r in rows}
    for code, c in cand.items():   # 控えの候補（取って見て1本に決める）も表に入れる
        if code not in done:
            rows.append(from_cand(c))
    for r in rows:
        for x in r:
            if '|' in x:
                raise SystemExit('「|」を含む値：%s' % r)
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 17本目 映像方針（2026-10-19）素材の記号 → 出どころ・大きさ・権利（make_sources17.py が書く＝手で直さない）\n')
        f.write('# 区切り「|」。get＝local:pdf（手元の報告書の PDF から ⑤b で切り出す）／commons:orig（原本・sha1 照合）／commons:3840（標準の縮小版）／yt-dlp／capture:⑤b／stock（Pexels・Pixabay の直リンク）／pending（未定）\n')
        f.write('# 🔴 作者の名前は書かない（作者が個人の点は src/credits_private.tsv＝git の外）\n')
        f.write('|'.join(HEAD) + '\n')
        for r in rows:
            f.write('|'.join(r) + '\n')
    print('rows=%d pending=%d → %s' % (len(rows), sum(1 for r in rows if r[5] == 'pending'), OUT))


if __name__ == '__main__':
    main()
