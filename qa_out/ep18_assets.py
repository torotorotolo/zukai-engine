# -*- coding: utf-8 -*-
"""ep18_assets.py — 18本目（スレッシャー号のリメイク）の**写真の束**を作る（2026-10-04 ⑤b-7a 新設）。

`qa_out/ep16_assets.py`（16本目）の形を写した。ここでやるのは「名前を付ける・札と縁を切り落とす・幅3000px に縮める・
権利を表にする」だけ。🆕 ⑤b-7b（10-05）：報告書・議会の本・発表の紙の**頁**（`pages`）を足した。動く映像（`clips.json`）は ⑤b-7c。

■ 素材（すべて米海軍の職務著作＝PD・17 U.S.C. §105）
  ① 旧版（3本目）の束 `ref/thresher/`（**読むだけ**＝旧版の記録を動かさない・materials.md §1）から写す点
     ＝NARA 289-T（RG 289・1963〜64年の捜索のアルバム・NARA の表示 Use: Unrestricted）・NARA 428-N-1057645・
       Commons の旧版4点（SHA-1 を Commons の原本と照らした＝2026-10-04 一致）・記録映画 85185 のコマ3枚
  ② Commons の新しい8点（`ref/ep18/img/`・**カズヤくんの了承のあとに `fetch` で取る**＝取るまで build は飛ばす）
■ 🔴 切り落とすもの（2026-10-04 ⑤b-7a に OCR〈`tools/ocr_win.ps1`〉と 640px のシートで見て決めた・元の画素の箱）
  ・289-T の英字の説明札（貼り札）＝OCR の文字の箱の外側に紙の縁が 20〜40px ある＝その外で切る
  ・艦首の正面（428-N）の台紙・上の手書きの番号・左下の札「24 July 1961 …」
  ・就役式（1961-08-03）の左の**座った観客（私人）**＝x 385 より左を切る（原寸で顔 約10px＝見分けられないが、寄りで大きくなる）
  ・t14 は1枚の頁に写真が2枚＝上の写真（セイルの593）だけ
  ・記録映画のコマは画素が縦長（SAR 10:11・NARA の 720×480）＝655×480 に直す（映像方針 §8）

    python qa_out/ep18_assets.py build [名…]   # ref/ep18/<名>.jpg ＋ assets.json
    python qa_out/ep18_assets.py check          # PICK・assets.json・ファイルが揃っているか
    python qa_out/ep18_assets.py panel          # 縦横比の並び（`cuts/ss.py` の PANEL_AR を決める材料）
    python qa_out/ep18_assets.py credits [--write]   # credits.json と ref/CREDITS.md の18本目の節
    python qa_out/ep18_assets.py fetch --yes    # Commons の新しい8点を取る（🔴 了承のあとだけ）
    python qa_out/ep18_assets.py pages [頁…]    # 🆕 ⑤b-7b：ref/ep18/pg<通し頁>.png ＋ pages.json（カットごとの切り口 cuts）
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = HERE / 'ref' / 'thresher'          # 旧版の束（読むだけ）
NEW = HERE / 'ref' / 'ep18' / 'img'      # Commons の新しい8点（git の外）
DEST = HERE / 'ref' / 'ep18'
DB = DEST / 'assets.json'
CREDITS_JSON = DEST / 'credits.json'
CREDITS_MD = HERE / 'ref' / 'CREDITS.md'
MAXW = 3000
UA = 'zukai-engine/1.0 (accident-documentary research; https://github.com/torotorotolo/zukai-engine)'
COMMONS = 'https://commons.wikimedia.org/wiki/'
NARA = 'https://catalog.archives.gov/id/'


def L(file, cuts, year, hold, url, ident, crop=None, sar=None, note='', who='米海軍'):
    """旧版の束 `ref/thresher/<file>` の1点。crop＝元の画素の箱 (x0, y0, x1, y1)。sar＝画素の縦横比（記録映画のコマ）。
    ident＝画面の出典に出す識別子（NARA の番号・USN の番号）。year＝撮影年（割れる・分からないなら None）"""
    return dict(src='old', file=file, cuts=cuts.split(), year=year, hold=hold, url=url, ident=ident,
                crop=crop, sar=sar, note=note, who=who)


def C(title, cuts, year, ident, note='', who='米海軍'):
    """Commons の新しい1点（`ref/ep18/img/` に取る）。title＝Commons の題名（File: を除く）"""
    return dict(src='commons', title=title, cuts=cuts.split(), year=year, ident=ident, note=note, who=who,
                hold=f'Wikimedia Commons「{title}」', url=COMMONS + 'File:' + urllib.parse.quote(title.replace(' ', '_')))


T289 = 'NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」'
U289 = NARA + '138924735'
F85185 = 'NARA 85185（RG 428）「USS THRESHER (SSN-593)」記録映画 1963年3月'

# 名前 → 素材。当てるカット（cuts）は章ファイルの PLAN と照らす（台本の画の欄）
PICK = {
    # ── 事故の前（1960〜62年）────────────────────────────────────
    'bow_1961': L('nara_428-N-1057645.jpg', 'c114 c709', 1961, 'NARA 175539769（428-N-1057645）', NARA + '175539769',
                  'NARA 428-N-1057645', crop=(90, 200, 2230, 2590),
                  note='1961年7月24日 真正面から見た艦首（札「DIRECT BOW VIEW」と台紙・手書きの番号は切った）'),
    'commission_1961': L('cm_SSN593_service_entering.jpg', 'c116 c215', 1961, 'Wikimedia Commons「SSN593 service entering.jpg」',
                         COMMONS + 'File:SSN593_service_entering.jpg', None, crop=(385, 0, 1750, 1211),
                         note='1961年8月3日 就役の直前・岸壁に式台を組む造船所の人と、甲板の白服の乗員（左の座った観客＝私人は切った）'),
    'launch_1960': L('cm_USN_1048964_USS_Thresher__SSN-593_.jpg', 'c201', 1960,
                     'Wikimedia Commons「USN 1048964 USS Thresher (SSN-593).jpg」',
                     COMMONS + 'File:USN_1048964_USS_Thresher_(SSN-593).jpg', 'USN 1048964',
                     note='1960年7月9日 進水（建屋から水へ出る艦首）・岸の人は全員が後ろ姿か横向き（原寸）'),
    'underway_1961': L('cm_USS_Thresher__SSN-593_.jpg', 'cb23', 1961, 'Wikimedia Commons「USS Thresher (SSN-593).jpg」',
                       COMMONS + 'File:USS_Thresher_(SSN-593).jpg', None,
                       note='1961年7月24日 海上を行くスレッシャー（右舷の前から・海軍歴史センター）'),
    'running_t2': L('thr_t2.jpg', 'c220 c423 c627', None, T289 + ' 289-T-2', U289, 'NARA 289-T-2',
                    crop=(0, 240, 2400, 1400),
                    note='浮上して走るスレッシャー（網点の印刷）＝アルバムの謝辞の頁の写真（右下の札「ACKNOWLEDGMENT …」と上の白い余白は切った）。撮影年は書かれていない'),
    'shipyard_sail_t14': L('thr_t14.jpg', 'c203', None, T289 + ' 289-T-14', U289, 'NARA 289-T-14', crop=(0, 0, 1555, 752),
                           note='造船所の写真：セイルの「593」と潜舵（頁の上の写真だけ・札「Shipyard photograph.」は切った）'),
    'shipyard_stern_t22': L('thr_t22.jpg', 'c208 c611', None, T289 + ' 289-T-22', U289, 'NARA 289-T-22',
                            note='造船所の写真：ドックの艦尾（上の舵・推進器の軸・横舵・足場）'),
    # ── 事故のあと（1963〜64年の海の底）───────────────────────────────
    # ⚠️ 試し焼き 37206148473：上の縁に白い細い帯が残った（y 10 から切った）＝y 30 から
    'bottle_t37': L('thr_t37.jpg', 'c722', 1964, T289 + ' 289-T-37', U289, 'NARA 289-T-37', crop=(90, 30, 1790, 1592),
                    note='1964年 海の底の空気のボンベ（上にカメラのそりの羅針・NRL/MIZAR）'),
    'hull_aft_t33': L('thr_t33.jpg', 'c805', 1964, T289 + ' 289-T-33', U289, 'NARA 289-T-33', crop=(0, 250, 1800, 1720),
                      note='1964年 艦の後ろ寄りの外殻の継ぎ写真（モザイク・NRL/MIZAR）'),
    'break78_t29': L('thr_t29.jpg', 'c812', 1964, T289 + ' 289-T-29', U289, 'NARA 289-T-29', crop=(0, 0, 1650, 1340),
                     note='1964年 78番目の骨組みで切れた所を真上から（TRIESTE II）'),
    'tail_t23': L('thr_t23.jpg', 'c819', 1964, T289 + ' 289-T-23', U289, 'NARA 289-T-23', crop=(0, 0, 1790, 1174),
                  note='1964年 艦尾の継ぎ写真（103番目の骨組みのあたりがつぶれた所・NRL/MIZAR）'),
    'break78_top_t30': L('thr_t30.jpg', 'c822', 1964, T289 + ' 289-T-30', U289, 'NARA 289-T-30', crop=(0, 0, 1430, 1351),
                         note='1964年 78番目の骨組みで切れた所の前の上甲板（TRIESTE II）'),
    'sail_t16': L('thr_t16.jpg', 'c906', 1964, T289 + ' 289-T-16', U289, 'NARA 289-T-16', crop=(0, 0, 1850, 1334),
                  note='1964年 海の底のセイルの右の側面（NRL/MIZAR）。札は「593 の最初の2桁」と書くが、絵では数字は読めない'),
    'page24': L('thr_page24.jpg', 'c911', 1964, T289 + ' 289-T-24（頁全体）', U289, 'NARA 289-T-24',
                note='289-T-24 のアルバムの頁全体（上と下の角に黒い塗り＝機密の印を消した跡・右下に説明札）'),
    'stern_plane_t26': L('thr_t26.jpg', 'c914', 1964, T289 + ' 289-T-26', U289, 'NARA 289-T-26', crop=(330, 0, 2400, 1665),
                         note='1964年 海の底の右の横舵と聴音器（左の札は切った）'),
    'rudder_t24': L('thr_t24.jpg', 'c920', 1964, T289 + ' 289-T-24', U289, 'NARA 289-T-24', crop=(1000, 0, 2340, 690),
                    note='1964年 海の底の上の舵の喫水の数字（4〜9・30〜34＝札の上まで・NRL/MIZAR）'),
    'plating_t39': L('thr_t39.jpg', 'ca05', 1963, T289 + ' 289-T-39', U289, 'NARA 289-T-39', crop=(190, 0, 1760, 1530),
                     note='1963年 外殻の板（約3m 四方・ラモント地質観測所の調査船コンラッドの写真）'),
    'debris_711302': L('cm_330-PSA-110-63__USN_711302___22171571340_.jpg', 'ca06', 1963,
                       'Wikimedia Commons「330-PSA-110-63 (USN 711302) (22171571340).jpg」',
                       COMMONS + 'File:330-PSA-110-63_(USN_711302)_(22171571340).jpg', 'USN 711302',
                       note='1963年 調査船の水中カメラが撮った海の底の破片（国防総省の発表の写真・セピア）'),
    'bow_plating_t5': L('thr_t5.jpg', 'ca13', 1963, T289 + ' 289-T-5', U289, 'NARA 289-T-5', crop=(0, 0, 1760, 990),
                        note='1963年 艦首の外板（初代トリエステの写真）。札の喫水の数字は絵では読めない'),
    'tracks_t41': L('thr_t41.jpg', 'ca20', 1964, T289 + ' 289-T-41', U289, 'NARA 289-T-41', crop=(190, 60, 1790, 960),
                    note='1964年 トリエステ2世が海の底に残した跡（捨てたおもりの黒い点・引きずった跡）'),
    # ── 記録映画 85185 のコマ（静止画）＝✅ ⑤b-7c（10-05）に (b) の承認どおり c212 c301 c601 cb01 を同じ映画の動く映像に替えた
    #    ＝いまはどのカットも使っていない（束には残す＝旧版から写した記録）。動く映像は §4（clips.json）・ひかえは fb_<カット>
    'film_a': L('thr_film593_a.jpg', '', 1963, F85185, NARA + '85185', 'NARA 85185', sar=10 / 11,
                note='記録映画のコマ（622秒）：浮上して走るスレッシャー・セイルの593（カラー）＝⑤b-7c で動く映像に替えた（使っていない）',
                who='米海軍の記録映画'),
    'film_b': L('thr_film593_b.jpg', '', 1963, F85185, NARA + '85185', 'NARA 85185', sar=10 / 11,
                note='記録映画のコマ（628秒）：セイルの上の乗員（公務）＝⑤b-7c で動く映像に替えた（使っていない）', who='米海軍の記録映画'),
    'film_c': L('thr_film593_c.jpg', '', 1963, F85185, NARA + '85185', 'NARA 85185', sar=10 / 11,
                note='記録映画のコマ（631秒）：セイルの593＝⑤b-7c で動く映像に替えた（使っていない）', who='米海軍の記録映画'),
    # ── Commons の新しい8点（🔴 カズヤくんの了承のあとに fetch で取る）────────────────────
    'skylark_front': C('USS Skylark (ASR-20).jpg', 'c304 c523', None, None,
                       note='救難艦スカイラークの正面（網点の印刷・1950年代後半〜60年代＝撮影年は割れる）'),
    'skylark_side': C('USS Skylark (ASR-20) underway c1950.jpg', 'c306 c511 c415', None, None,
                      note='海上のスカイラーク（横から・1951年ごろ＝撮影年は「ごろ」）'),
    'door_711348': C('330-PSA-191-63 (USN 711348) (22171493730).jpg', 'ca10', 1963, 'USN 711348',
                     note='1963年8月24日 トリエステの2回目の潜航で撮った艦の中の水密扉'),
    'pipe_711350': C('330-PSA-191-63 (USN 711350) (22172651149).jpg', 'ca11', 1963, 'USN 711350',
                     note='1963年 トリエステが回収した真鍮の管（刻印「593 Boat」）'),
    'trieste2_sea': C('330-PSA-309-64 (KN-9302C) (22766865552).jpg', 'ca14', 1964, 'KN-9302C',
                      note='1964年 海上のトリエステ2世（説明文の「ボストンの造船所」と絵〈海の上〉が合わない＝場所は名乗らない）'),
    'trieste2_drawing': C('330-PSA-276-63 (USN 711389) (22517726786).jpg', 'ca17', 1963, 'USN 711389',
                          note='1963年 海軍が描いたトリエステ2世の想像図'),
    'fish_1104636': C('330-PSA-309-64 (USN 1104636-D) (22592418930).jpg', 'ca18', 1964, 'USN 1104636-D',
                      note='1964年 ミザーから降ろされる曳航カメラ「The Fish」'),
    'search_ships_1963': C('Ships searching for USS Thresher (SSN-593), 15 April 1963 (NH 97555).jpg', 'cb09', 1963, 'NH 97555',
                           note='1963年4月15日 スレッシャーの沈んだあたりを回る海軍の艦'),
}
GROUND = 'PD（米連邦の職務著作 17 U.S.C. §105）'

# ══════════════════════════════════════════════════════════
#  頁（🆕 ⑤b-7b・2026-10-05）＝台本の通し頁（`cuts/ss.REC_DOCS` と同じ番号）
# ══════════════════════════════════════════════════════════
# 16本目（2段組みの議会の報告書）の `col_trim` を**1段組み**に写した。18本目の資料はほぼ全部が1段組み
# （タイプ打ちの査問会の記録・証拠・意見書／議会の本〈活字〉）＝段を探さず、**同じ高さの語を1行にまとめてから**目印を探す
# （文字の層が語ごとに割れている頁がある＝IR18 p.1）。目印は文字の層の字（OCR の誤りもそのまま）から a〜z と 0〜9 だけを残した字。
RAW = HERE / 'ref' / '_thresher_raw'     # 旧版の写し（V1・X）＝読むだけ
SRC = DEST / 'src'                       # ④ で取った資料（IR18・R08・J）
PAGES_JSON = DEST / 'pages.json'
# (通し頁の下限, 上限, PDF, 資料, base＝通し頁 − PDF の頁, dpi)
PAGE_DOCS = (
    (1, 300, RAW / 'inquiry_vol1_p1-300.pdf', 'V1', 0, 200),
    (1001, 1600, RAW / 'inquiry_9_10.pdf', 'X', 1000, 200),
    (2001, 2203, SRC / 'navy_IR18.pdf', 'IR18', 2000, 200),
    (4001, 4300, SRC / 'navy_IR08.pdf', 'R08', 4000, 200),
    # J＝議会の本（Stanford の PDF・頁が小さい 383×638pt＝300dpi）。通し頁＝印刷頁＋8000・**PDF の頁＝印刷頁＋14**
    #   （⑤b-7b に7頁〈13・38・79・89・112・122・160〉を文字の層で ep18_pages.txt と照らした＝7頁とも同じずれ）
    (8001, 8192, SRC / 'jcae1965_stanford.pdf', 'J', 8000 - 14, 300),
)
# 画像の頁＝国防総省の発表 No.710-64 の紙（旧版の束の Commons「330-PSA-309-64a (22791587391).jpg」・NARA RG 330）
PAGE_IMG = {9801: (OLD / 'cm_330-PSA-309-64a__22791587391_.jpg', 'No.710-64')}
PAGE_DPI_OF = {1131: 100, 1135: 100}     # 海図（1868×1343pt・1914×1343pt）＝100dpi でも切り口の幅が 1,500px を超える
PANEL_AR_T = 1120 / 648                  # 額の最大の箱（`scene_jiko.PANEL_MAXW × PANEL_MAXH`）の縦横比＝文字の頁の切り出しの目標
COLS = (0.08, 0.92)                      # 字を探す横の範囲（頁の幅の割合）＝余白の汚れ・穴・綴じの跡（x 0.94〜0.97）を拾わない
END_PAD = 0.012
# 切り口（カット → (頁, 切り方)）：
#   ('rows', 始めの目印, 終わりの目印[, dict(lo=目印, hi=目印)])
#        … 始め〜終わりの行を入れ、額の縦横比になるまで上下に行を足す。lo＝この目印の行より上は入れない／hi＝この目印の行から下は入れない
#   ('imgbox', 上, 下)  … 文字の層が使えない頁（表・画像の頁）：頁の割合の上下の範囲に中心がある字の帯をまとめる
#   ('box', x0, y0, x1, y1) … 海図（字の行が無い）＝頁の割合をそのまま（⑤b-7b に縮めた頁を見て決めた）
# ⚠️ 目印は ⑤b-7b（10-05）に `scratchpad/probe_anchor.py` で文字の層を引いて、台本の語りと照らして決めた
PAGE_CUTS = {
    # 冒頭：前の艦長の評価書（証拠111）の1頁目＝艦名・Ser 086・1962年11月16日・差出人と宛先
    #   ⚠️ 1回目（lo なし）は上の余白の頁番号とスキャンの汚れまで足して縦横比 1.18＝艦名の行から下へだけ広げる
    'c105': (1531, ('rows', 'thresherssn593', 'chiefbureauofships', dict(lo='thresherssn593'))),
    # 🔴 c105 の3行目（X p.533 第5段落）と印（映像方針 §1-3）は ⑤b-7c の「尻の差し込み」・⑤b-8 の trace で＝切り口だけ先に作る
    #   ⚠️ 試し焼き 37217579198：第5段落の上下に手書きの書き込みがあり、右の端で切れた＝第5段落だけ（lo＝段落の頭・hi＝0.852
    #      ＝「essential.」の下・手書きは文字の層に無い＝頁の割合で止める）・横の範囲を広げる
    'c105t': (1533, ('rows', 'inmyopinionthemostdangerous', 'totalisolationis',
                     dict(lo='inmyopinionthemostdangerous', hi=0.852, cols=(0.05, 0.97)))),
    # 海軍長官の第7 endorsement の1頁目（1965-03-19・第18回公開）＝題と差出人・宛先・件名
    'c109': (2001, ('rows', 'seventhendorsement', 'lossatseaofussthresher')),
    # 認定5・6（R08 p.184）＝「乗っていた全員は公務を果たすために乗っていた」＝c303 の語り（PLAN は p.181＝cb22 と同じ頁だった）
    'c303': (4184, ('rows', 'thatthepersonslistedasbeing', 'executingofficialduties')),
    # 証拠50 の海図（線画）＝海岸線・捜索の区域・EXHIBIT 50 の札
    'c307': (1131, ('box', 0.05, 0.24, 0.66, 0.82)),
    # ヘッカー少佐への問い「SKYLARK に何ができるか」「None, sir.」（下の「8400 feet of water」の行は入れない＝深さの数は「約2,600メートル」で言う）
    #   ⚠️「None, sir.」は頁に2回ある＝終わりの目印は問いの行・hi で答えの行まで入る
    #   ⚠️ 試し焼き 37217579198：1行目「…approximate time by 'pho」が右の端で切れた＝横の範囲を広げる
    'c316': (183, ('rows', 'questionsbythepresident', 'assistingasubmarineoutofcontrol',
                   dict(hi='ifthatsubmarineisin', cols=(0.08, 0.97)))),
    # 認定19＝9時18分ごろ全員とともに失われた・北緯41度45分 西経65度
    'c414': (38, ('rows', 'thresherwaslostatsea', 'longitude6500')),
    # スカイラークの無線の記録（電文 101604Z〜17:45Z に陸の局が受け取った行）＝表＝文字の層が崩れる
    #   ⚠️ 試し焼き 37217579198：17:45Z の行「R 101604Z AR」（語りの「3時間半」）が切り口の下に外れた＝下を 0.49 → 0.50
    'c508': (1061, ('imgbox', 0.225, 0.50)),
    # 潜水艦シーウルフの報告（証拠49）の題と General の段落（文字の層が崩れる＝見た目の字はくっきり）
    'c516': (1120, ('imgbox', 0.215, 0.365)),
    # 議員「残りの2,855の継手は、なぜ一度も試されなかったのか」→ オースティン中将「査問会も同じ思いだった」
    'c623': (8013, ('rows', 'thisstilldoesntanswer', 'evidencedonthispoint')),
    # 議員「その深さで吹き切れるか……一度も行われていないと理解している」→ モーラー少将「そのとおり」
    #   ⚠️ 頁の最後の行（議員の次の発言「100 or 200 feet」＝深さの数）は入れない
    'c712': (8038, ('rows', 'myquestionisthatwearegoing', 'admiralmaurerthatisright', dict(hi='itwouldseemtomeyou'))),
    # 議員「岸壁ででも目いっぱい吹いたか」→ カーツ少将「分からない。していないと思う」
    'c721': (8112, ('rows', 'didyoueverblowatall', 'idontthinkso')),
    # リッコーヴァー中将の声明の結び「本当に何が起きたかを突き止めるには情報が足りない」
    'c814': (8089, ('rows', 'thereisinsufficientinformation', 'everythingthatmayhave')),
    # 小委員長の書簡（1963-08-19）「国民を真実から守るために機密を使うことは望まないはずだ」「どこが機密かを示せ」
    'c903': (8160, ('rows', 'dearmrkorth', 'properlyclassified')),
    # ［classified matter deleted］が並ぶ所＝見出し「REASSESSMENT OF NEED FOR DEEP OPERATING DEPTH」の下の段（運用の深さの数が
    #   5か所削られている＝語りの「証言の中の深さの数字も、削られている」）。⚠️ 最初は「魔法の数」の段（頁の中ほど）にしたが、
    #   行間の詰まった頁の中ほどは寄りの縮みを受けるすき間が無い（門番 edges）＝見出しの上の余白を上の辺にした
    'c905': (8122, ('rows', 'reassessmentofneedfordeep', 'safetyfactorhere')),
    # 認定15＝「この潜航の深さは……に決められていた」の後ろの b(1) の塗り
    'c909': (38, ('rows', 'thatat0747r', 'skylarkdidnotplot')),
    # 第9・10回の捜索の海図（灰色の地）の白い四角の塗り「(b)(1)」とまわり
    'c910': (1135, ('box', 0.55, 0.50, 0.97, 0.93)),
    # 国防総省の発表 No.710-64（1964-10-01）＝日付・番号・題・第1〜2段落（6月・7月・8月）
    'ca15': (9801, ('imgbox', 0.19, 0.545)),
    # リッコーヴァー中将の声明（1963-07）「特定のろう付け・溶接・系統・部品の故障だけを原因と見るべきでない」
    'cb12': (8079, ('rows', 'nowiwillconcludeibelieve', 'navalshipbuildingprograms')),
    # 証拠111 の第5段落（c105 の3行目と同じ所＝物証を終章で回収）
    'cb21': (1533, ('rows', 'inmyopinionthemostdangerous', 'totalisolationis',
                    dict(lo='inmyopinionthemostdangerous', hi=0.852, cols=(0.05, 0.97)))),
    # 🔴 cb21 の2行目＝勧告20（R08 p.220）は ⑤b-7c の「尻の差し込み」で＝切り口だけ先に作る
    'cb21t': (4220, ('rows', 'thatearlyconsideration', 'timelydisseminationofsuchinformation')),
    # 認定4 の書き出しと名簿の頭（R08 p.181）
    #   ⚠️ 試し焼き 37217579198：右の列「STAFF, DEPUTY COMMANDER SUBMARINE FORCE, U.S.」が右の端で切れた＝横の範囲を広げる
    'cb22': (4181, ('rows', 'thatthefollowingpersons', 'smarzjohn', dict(cols=(0.08, 0.97)))),
}
# 切り口を持たずに焼く頁＝c104（決め所＝⑤b-8 の trace が頁と行の箱を自分で切る）：意見1（V1 p.57）・IR18 p.1（c109 と同じ）・p.5 段落11
#   ⚠️ 意見1 は V1 p.57 と R08 p.204 で同じ文・どちらも意見1 の段落に塗りの印が無い（⑤b-7b に文字の層で確かめた）
#      ＝見た目の字が濃い方を ⑤b-8 で選べるよう両方焼く（§9 の測り 0.052／0.058）
EXTRA_PAGES = (57, 4204, 2005)


def pages_pick():
    return sorted({pr for pr, _ in PAGE_CUTS.values()} | set(EXTRA_PAGES))


def _page_doc(pr):
    if pr in PAGE_IMG:
        return None
    for d in PAGE_DOCS:
        if d[0] <= pr <= d[1]:
            return d
    raise SystemExit(f'🔴 p{pr} の資料が PAGE_DOCS に無い')


def _doc_code(pr):
    return PAGE_IMG[pr][1] if pr in PAGE_IMG else _page_doc(pr)[3]


def _gray(page, dpi):
    import fitz
    import numpy as np
    pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)


def _bands(a, c0, c1):
    """横の範囲 c0〜c1（頁の幅の割合）の字の帯＝[(上, 下)]（頁の高さの割合）。インクの横の投影で、帯は高さ4画素以上
    （16本目と同じ。⚠️ 帯を「インクが1画素でもある行」まで広げない＝スキャンの汚れで行間が埋まる）"""
    sub = a[:, int(c0 * a.shape[1]):int(c1 * a.shape[1])]
    ink = (sub < 140).sum(axis=1)
    on = ink > max(3, 0.01 * sub.shape[1])
    spans, y, H = [], 0, a.shape[0]
    while y < len(on):
        if on[y]:
            y0 = y
            while y < len(on) and on[y]:
                y += 1
            if y - y0 >= 4:
                spans.append([y0, y])
        y += 1
    return [(s[0] / H, s[1] / H) for s in spans]


def _ocr_rows(key, c0, c1):
    """門番 edges が使う OCR の読み置き（`check_slide.py --ocr`＝ref/ep18/ocr_slides.json）の、横 c0〜c1 の行の箱（頁の高さの割合）。
    読み置きが無ければ []（初回・頁を足した直後）＝インクの帯だけで切る→ OCR を取ってから `pages` をもう一度（§5b-115）"""
    p = DEST / 'ocr_slides.json'
    if not p.exists():
        return []
    v = json.loads(p.read_text(encoding='utf-8')).get(f'{key}.png')
    if not v:
        return []
    W, H = v['size']
    # 🔴 ⑤b-7b：箱そのものでなく**上下を 7% ずつ縮めた芯**を返す。議会の本（行間の詰まった活字・300dpi）は Windows の OCR の
    #    行の箱が上下の行と高さの 0.1〜0.2（誤読の行で 0.37〜0.72）重なり、箱のまままとめると頁が数本の塊になった
    #    （c623 が縦横比 0.66・c712 は止まった）。門番 edges は「見えている割合が 8〜92% の行」だけを鳴らす＝箱の上下 8% までは
    #    切り線がかかってよい＝芯（7%＝少し内側）と芯のすき間で切れば門番と同じ物差しのまま。タイプ打ちの頁は重なり 0〜0.04
    return [(ln['box'][1] / H + 0.07 * (ln['box'][3] - ln['box'][1]) / H,
             ln['box'][3] / H - 0.07 * (ln['box'][3] - ln['box'][1]) / H) for ln in v['lines']
            if c0 <= (ln['box'][0] + ln['box'][2]) / 2 / W < c1 and ln['box'][3] - ln['box'][1] >= 10]


def _occupied(bands, rows):
    """インクの帯と OCR の行の箱を合わせた「字のある範囲」（重なる・触れる範囲はまとめる）"""
    out = []
    for a, b in sorted(list(bands) + list(rows)):
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [tuple(x) for x in out]


def _ink_x(a, y0, y1, c0, c1):
    """y0〜y1（頁の高さの割合）・横 c0〜c1 の中で、インクのある左端と右端（頁の幅の割合）。
    縦の列のインクが帯の高さの 2% を超える列だけ数える（汚れの点を拾わない）"""
    import numpy as np
    H, Wp = a.shape
    sub = a[int(y0 * H):int(y1 * H), int(c0 * Wp):int(c1 * Wp)]
    cols = np.where((sub < 140).sum(axis=0) > max(1, 0.02 * sub.shape[0]))[0]
    if not len(cols):
        raise SystemExit('🔴 範囲の中にインクが無い')
    return (int(cols[0]) + int(c0 * Wp)) / Wp, (int(cols[-1]) + int(c0 * Wp)) / Wp


ZOOM_D = 1 - 1 / (1 + 0.055 * 0.35)      # 額装の寄りが尺の終わりまでに縮める窓の高さ（切り口の高さの割合）＝`check_slide.crop_rect`
SEARCH = 12                              # 切り口の上下の行を探す幅（行）


def _fit_cut(occ, j0, j1, lo, hi, px, want=None):
    """🔴 ⑤b-7b：字のある範囲 j0〜j1 の上下の切り線と、寄りの縦の寄せ bias を決める（頁の高さの割合）。
    寄りは尺の終わりまでに窓の高さを Δ＝ZOOM_D×切り口の高さ だけ縮める＝bias の割合が上の辺、残りが下の辺の動き
    （`check_slide.crop_rect`：top＝(sh−ch)×bias）。行間の詰まった頁（議会の本）は上下どちらのすき間も Δ/2 に足りない
    （16本目の `_cut_lines`＝bias 0.5 の前提で、6カットが門番 edges で端の行 72〜87%）→ **上下のすき間の和が Δ を超える行の組**を
    j0・j1 の±SEARCH 行から探し（足す行の少ない組）、縮みをすき間の広さに比例して上下に配る。足りる組が無ければ止める。
    ⚠️ 議会の本は行と行のすき間が 0〜6px（Δ は約 10〜21px）＝成り立つのは片方の辺が**見出しの前後・手紙の書き出しと署名・
    頁の上下の余白**にある組だけ（bias が 0 か 1 に寄る＝その辺だけが動く）。
    want＝欲しい高さ（頁の高さの割合・額の縦横比から）＝成り立つ組のうち高さがいちばん近い組（無ければ足す行の少ない組）。
    ⚠️ 先に縦横比まで行を足してから探すと、足した先に見出しの余白が入らず（c712）、上下に広がりすぎた（c623 縦横比 0.9）"""
    best = None
    for a in range(j0, max(lo, j0 - SEARCH) - 1, -1):
        for b in range(j1, min(hi, j1 + SEARCH) + 1):
            gt = occ[a][0] - occ[a - 1][1] if a > 0 else 1.0
            gb = occ[b + 1][0] - occ[b][1] if b < len(occ) - 1 else 1.0
            t_out = occ[a - 1][1] + px if a > 0 else occ[a][0] - END_PAD
            b_out = occ[b + 1][0] - px if b < len(occ) - 1 else occ[b][1] + END_PAD
            d = ZOOM_D * (b_out - t_out)
            room_t, room_b = occ[a][0] - px - t_out, b_out - (occ[b][1] + px)   # 辺が動いてよい幅
            if room_t < 0 or room_b < 0 or room_t + room_b < d:
                continue
            added = (j0 - a) + (b - j1)
            cost = (abs((b_out - t_out) - want), added) if want else (added,)
            if best is None or cost < best[0]:
                best = (cost, a, b, t_out, b_out, room_t, room_b, d)
    if best is None:
        raise SystemExit(f'🔴 上下のすき間の和が寄りの縮みに足りる行の組が無い（行 {j0}〜{j1}・±{SEARCH}行）')
    _, a, b, t_out, b_out, room_t, room_b, d = best
    bias = min(1.0, max(0.0, room_t / (room_t + room_b))) if room_t + room_b > 0 else 0.5
    # 辺は「動ききった所」がちょうど内側の行の手前に来るよう、余る幅を上下に半分ずつ残す
    spare = room_t + room_b - d
    top = t_out + spare / 2 * (room_t / (room_t + room_b) if room_t + room_b > 0 else 0.5)
    bot = b_out - spare / 2 * (room_b / (room_t + room_b) if room_t + room_b > 0 else 0.5)
    return a, b, top, bot, round(bias, 3)


def _text_rows(page):
    """文字の層の行＝[dict(t, y0, y1)]（頁の割合・上から）。**同じ高さの語を1行にまとめる**（語ごとに割れた文字の層）。
    t＝左から並べた字の a〜z・0〜9 だけ（行末のハイフンは落ちる＝次の行とつながる）"""
    H, W = page.rect.height, page.rect.width
    segs = []
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for ln in b['lines']:
            t = re.sub(r'[^a-z0-9]', '', ''.join(s['text'] for s in ln['spans']).lower())
            if t:
                x0, y0, x1, y1 = ln['bbox']
                segs.append((y0 / H, y1 / H, x0 / W, t))
    segs.sort(key=lambda s: (s[0] + s[1]) / 2)
    rows = []
    for s in segs:
        c = (s[0] + s[1]) / 2
        if rows and abs(c - rows[-1]['c']) < 0.45 * (s[1] - s[0]):
            r = rows[-1]
            r['segs'].append(s)
            r['y0'], r['y1'] = min(r['y0'], s[0]), max(r['y1'], s[1])
        else:
            rows.append(dict(c=c, y0=s[0], y1=s[1], segs=[s]))
    for r in rows:
        r['t'] = ''.join(x[3] for x in sorted(r['segs'], key=lambda x: x[2]))
    return rows


def _find(rows, anchor, pr):
    """目印の最初と最後の字が載る行の番号。1か所でなければ止める（黙って別の所を切らない）"""
    joined, owner = '', []
    for i, r in enumerate(rows):
        joined += r['t']
        owner += [i] * len(r['t'])
    ks = [m.start() for m in re.finditer(re.escape(anchor), joined)]
    if len(ks) != 1:
        raise SystemExit(f'🔴 p{pr}：目印「{anchor}」が {len(ks)} か所＝1か所でないと切らない')
    return owner[ks[0]], owner[ks[0] + len(anchor) - 1]


def row_trim(page, a, pr, a_from, a_to, opt=None):
    """1段組みの頁の切り口：始め〜終わりの目印の行を入れ、額の縦横比になるまで上下に字の帯を足す（頁の割合）"""
    opt = opt or {}
    rows = _text_rows(page)
    r0, _ = _find(rows, a_from, pr)
    _, r1 = _find(rows, a_to, pr)
    if r1 < r0:
        raise SystemExit(f'🔴 p{pr}：終わりの目印が始めより上')
    bands = _occupied(_bands(a, *COLS), _ocr_rows(f'pg{pr}', *COLS))

    def band_of(r):
        # ⚠️ 文字の層の行の箱は上下が隣の行と重なるほど高い（議会の本 p.38＝0.918〜0.943 の次の行が 0.934〜）＝箱の端で
        #    比べると外れる。行の**中心**にいちばん近いインクの帯を当てる（帯は行間の詰まった頁で2〜3行が1本につながる）
        c = (rows[r]['y0'] + rows[r]['y1']) / 2
        k = min(range(len(bands)), key=lambda i: abs((bands[i][0] + bands[i][1]) / 2 - c))
        if not bands[k][0] - 0.012 <= c <= bands[k][1] + 0.012:
            raise SystemExit(f'🔴 p{pr}：文字の層の行（y {c:.4f}）に近い字の帯が無い')
        return k
    j0, j1 = band_of(r0), band_of(r1)
    lo, hi = 0, len(bands) - 1
    if opt.get('lo') is not None:
        # lo＝この目印の行から上は入れない（頁の上の余白のごみ・頁番号まで足して縦長になるのを止める＝c105）。
        #   数なら頁の割合＝帯の上の端がそれより上の帯は入れない
        lo = (band_of(_find(rows, opt['lo'], pr)[0]) if isinstance(opt['lo'], str)
              else min(i for i, b in enumerate(bands) if b[0] >= opt['lo']))
        if lo > j0:
            raise SystemExit(f'🔴 p{pr}：lo の目印が始めの目印より下')
    if opt.get('hi') is not None:
        # hi＝この目印の行から下は入れない。数なら頁の割合＝帯の真ん中がそれより下の帯は入れない（文字の層に無い手書き＝cb21）
        hb = (band_of(_find(rows, opt['hi'], pr)[0]) if isinstance(opt['hi'], str)
              else min(i for i, b in enumerate(bands) if (b[0] + b[1]) / 2 > opt['hi']))
        hi = hb - 1
        if hi < j1:
            raise SystemExit(f'🔴 p{pr}：hi の目印の帯が終わりの目印の帯と同じか上（帯がつながっている）')
    # 左右の端＝画像のインク（目印の行の上下 4本ぶんの帯で測る）＋10pt
    x0, x1 = _ink_x(a, bands[max(lo, j0 - 4)][0], bands[min(hi, j1 + 4)][1], *opt.get('cols', COLS))
    W, H = page.rect.width, page.rect.height
    x0, x1 = max(0.0, x0 - 10 / W), min(1.0, x1 + 10 / W)
    want = (x1 - x0) * W / PANEL_AR_T / H
    # lo・hi は _fit_cut の探す範囲（lo の帯より上・hi の帯から下の行は入れない＝切り線は lo の上の帯・hi の帯の手前まで）
    j0, j1, top, bot, bias = _fit_cut(bands, j0, j1, lo, hi, 1 / a.shape[0], want)
    # 🔴 左右の端は**最後に決まった切り口の中の行全部**で測り直す（試し焼き 37217579198：目印のまわりの行だけで測ったので、
    #    切り口に入った長い行・右の列・手書きが右の端で切れた＝c316「by 'pho」・cb22「DEPUTY COMM」・cb21 の手書き）。
    #    横の範囲は既定 COLS（余白の汚れを拾わない）・長い行や手書きのある頁は opt の cols で広げる
    x0, x1 = _ink_x(a, top, bot, *opt.get('cols', COLS))
    x0, x1 = max(0.0, x0 - 10 / W), min(1.0, x1 + 10 / W)
    box = (x0, max(0.0, top), x1, min(1.0, bot))
    return [round(float(v), 4) for v in box], dict(by='rows', rows=[j0, j1], n_rows=j1 - j0 + 1, bias=bias,
                                                    ar=round((x1 - x0) * W / ((box[3] - box[1]) * H), 2))


def imgbox_trim(a, pr, ya, yb, wpt):
    """文字の層が使えない頁（表・画像の頁）：頁の割合 ya〜yb に中心がある字の帯をまとめて切る。左右はインクの端＋12pt。
    wpt＝頁の幅（pt・画像の頁は画素）"""
    import numpy as np
    bands = _occupied(_bands(a, 0.04, 0.96), _ocr_rows(f'pg{pr}', 0.04, 0.96))
    idx = [i for i, b in enumerate(bands) if ya <= (b[0] + b[1]) / 2 <= yb]
    if not idx:
        raise SystemExit(f'🔴 p{pr}：y {ya}〜{yb} に字の帯が無い')
    j0, j1, top, bot, bias = _fit_cut(bands, idx[0], idx[-1], 0, len(bands) - 1, 1 / a.shape[0])
    sub = a[int(bands[j0][0] * a.shape[0]):int(bands[j1][1] * a.shape[0]), int(0.04 * a.shape[1]):int(0.96 * a.shape[1])]
    cols = np.where((sub < 140).sum(axis=0) > 1)[0] + int(0.04 * a.shape[1])
    pad = 12 / wpt
    x0, x1 = cols[0] / a.shape[1] - pad, cols[-1] / a.shape[1] + pad
    box = (max(0.0, x0), max(0.0, top), min(1.0, x1), min(1.0, bot))
    return [round(float(v), 4) for v in box], dict(by='imgbox', rows=[j0, j1], n_rows=j1 - j0 + 1, bias=bias)


def cmd_pages(only=None):
    """`pages` は全頁。`pages 38` のように頁を書けばその頁だけ焼き直す（ほかの頁の md5 を動かさない）。頁は灰色の PNG"""
    import fitz
    import numpy as np
    from PIL import Image
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    for pr in pages_pick():
        if only and pr not in only:
            continue
        out = DEST / f'pg{pr}.png'
        cuts, biases = {}, {}      # biases＝寄りの縦の寄せ（`ss.pbias`＝SPEC の bias）
        if pr in PAGE_IMG:
            src, doc = PAGE_IMG[pr]
            with Image.open(src) as im0:
                im = im0.convert('L')
            im.save(out)
            a = np.asarray(im)
            for cid, (p2, how) in PAGE_CUTS.items():
                if p2 == pr:
                    trim, info = imgbox_trim(a, pr, how[1], how[2], im.width)
                    cuts[cid], biases[cid] = trim, info['bias']
                    print(f'✓ pg{pr} {cid}  trim={trim}  {info}')
            pj[f'pg{pr}'] = dict(doc=doc, img=src.name, src_md5=_md5(src), w=im.width, h=im.height, dpi=None,
                                 md5=_md5(out), cuts=cuts, bias=biases)
            print(f'  pg{pr}  {doc} 画像 {src.name}  {im.width}x{im.height}')
            continue
        lo_, hi_, fn, doc, base, dpi = _page_doc(pr)
        dpi = PAGE_DPI_OF.get(pr, dpi)
        pno = pr - base
        with fitz.open(fn) as d:
            if not 1 <= pno <= d.page_count:
                raise SystemExit(f'🔴 p{pr}＝{doc} の PDF {pno}頁は無い（全{d.page_count}頁）')
            pg = d[pno - 1]
            pix = pg.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
            pix.save(out)
            a = _gray(pg, dpi)
            for cid, (p2, how) in PAGE_CUTS.items():
                if p2 != pr:
                    continue
                if how[0] == 'rows':
                    trim, info = row_trim(pg, a, pr, how[1], how[2], how[3] if len(how) > 3 else None)
                elif how[0] == 'imgbox':
                    trim, info = imgbox_trim(a, pr, how[1], how[2], pg.rect.width)
                elif how[0] == 'box':
                    trim, info = [float(v) for v in how[1:5]], dict(by='box')
                else:
                    raise SystemExit(f'🔴 {cid}：知らない切り方 {how[0]}')
                cuts[cid], biases[cid] = trim, info.get('bias', 0.5)
                print(f'✓ pg{pr} {cid}  trim={trim}  {info}')
        pj[f'pg{pr}'] = dict(doc=doc, pdf=fn.name, pdf_page=pno, w=pix.width, h=pix.height, dpi=dpi, md5=_md5(out),
                             cuts=cuts, bias=biases)
        print(f'  pg{pr}  {doc} PDF {pno}頁  {pix.width}x{pix.height}')
    PAGES_JSON.write_text(json.dumps(pj, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def _db():
    return json.loads(DB.read_text(encoding='utf-8')) if DB.exists() else {}


def _src_path(r):
    if r['src'] == 'old':
        return OLD / r['file']
    return NEW / r['title']


def cmd_build(only=None):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    db = _db()
    skip = []
    fetched = json.loads((NEW / 'fetched.json').read_text(encoding='utf-8')) if (NEW / 'fetched.json').exists() else {}
    for name, r in PICK.items():
        if only and name not in only:
            continue
        sp = _src_path(r)
        if not sp.exists():
            skip.append(name)
            continue
        if r['src'] == 'commons':
            f = fetched.get(r['title'])
            if not f or hashlib.sha1(sp.read_bytes()).hexdigest() != f['sha1']:
                raise SystemExit(f"🔴 {name}: {sp.name} の SHA-1 が Commons の原本と違う（取り直す）")
        with Image.open(sp) as im0:
            im = im0.convert('RGB')
        w0, h0 = im.size
        box = r.get('crop') or (0, 0, w0, h0)
        im = im.crop(box)
        if r.get('sar'):
            im = im.resize((round(im.width * r['sar']), im.height), Image.LANCZOS)
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        out = DEST / f'{name}.jpg'
        im.save(out, quality=92)
        db[name] = dict(src=r['src'], file=sp.name, cut=' '.join(r['cuts']), note=r['note'],
                        box=[round(box[0] / w0, 4), round(box[1] / h0, 4), round(box[2] / w0, 4), round(box[3] / h0, 4)],
                        crop_px=list(box), sar=r.get('sar'), w=im.width, h=im.height, md5=_md5(out), src_md5=_md5(sp),
                        lic='Public domain', frame=False, author=r['who'], ground='A', year=r['year'],
                        hold=r['hold'], url=r['url'], ident=r.get('ident'))
        print(f"✓ {name:20} {im.width}x{im.height}  ← {sp.name}  切り={box}{'・SAR を直した' if r.get('sar') else ''}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'→ {DB}（{len(db)}点）')
    if skip:
        print(f"⚠️ 元のファイルが無いので飛ばした {len(skip)}点（Commons の新しい点＝了承のあとに fetch）: {' '.join(skip)}")
    return 0


def cmd_check():
    if not DB.exists():
        raise SystemExit('🔴 assets.json が無い（build を先に）')
    db = _db()
    bad = 0
    for name in PICK:
        p = DEST / f'{name}.jpg'
        if name not in db or not p.exists():
            print(f'🔴 {name}: 束に無い')
            bad += 1
            continue
        if _md5(p) != db[name]['md5']:
            print(f'🔴 {name}: md5 が assets.json と違う（手で差し替えた？）')
            bad += 1
    for e in sorted(set(db) - set(PICK)):
        print(f'⚠️ assets.json に PICK に無い名前: {e}')
    # 当てるカットが PLAN の写真のカットと1対1か（台本の画の欄＝PLAN が正本）
    sys.path.insert(0, str(HERE / 'tools'))
    import cuts
    want = {c for c, p in cuts.PLAN.items() if p['kind'] == '写真'}
    have = {c for r in PICK.values() for c in r['cuts']}
    # 🆕 ⑤b-7c：記録映画（カットまるごと＝footage.USE・head でない）のカットは動く映像が当たっている
    import footage as FO
    vids = {c for c, u in FO.USE.items() if not u.get('head')}
    print(f'PLAN の写真 {len(want)}カット・PICK が当てる {len(have)}カット・記録映画（footage.USE）{len(want & vids)}カット・'
          f"まだ当てていない {len(want - have - vids)}: {' '.join(sorted(want - have - vids))}")
    if have - want:
        print(f"🔴 PLAN で写真でないカットに当てている: {' '.join(sorted(have - want))}")
        bad += 1
    # 🆕 ⑤b-7b：頁＝焼いた頁が揃っているか・md5・切り口・PLAN の頁のカットと1対1か
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    miss = [pr for pr in pages_pick() if f'pg{pr}' not in pj or not (DEST / f'pg{pr}.png').exists()]
    if miss:
        print(f'🔴 焼いていない頁: {miss}')
        bad += 1
    for k, v in pj.items():
        if (DEST / f'{k}.png').exists() and _md5(DEST / f'{k}.png') != v['md5']:
            print(f'🔴 {k}: md5 が pages.json と違う')
            bad += 1
    hav = {cid for v in pj.values() for cid in v.get('cuts', {})}
    if set(PAGE_CUTS) - hav:
        print(f'🔴 切り口の無いカット: {sorted(set(PAGE_CUTS) - hav)}')
        bad += 1
    pwant = {c for c, p in cuts.PLAN.items() if p['kind'] in ('文字の頁', '図・写真の頁')}
    pgot = {c for c in PAGE_CUTS if not c.endswith('t')}      # 〜t＝尻の差し込みの切り口（⑤b-7c）
    print(f'PLAN の頁 {len(pwant)}カット・PAGE_CUTS {len(pgot)}カット（＋尻の差し込み {len(PAGE_CUTS) - len(pgot)}）'
          f"・まだ切っていない {len(pwant - pgot)}: {' '.join(sorted(pwant - pgot))}")
    if pgot - pwant:
        print(f"🔴 PLAN で頁でないカットに切り口: {' '.join(sorted(pgot - pwant))}")
        bad += 1
    print('✓ 揃っている' if not bad else f'🔴 {bad}件')
    return 1 if bad else 0


def cmd_panel():
    db = _db()
    for n, r in sorted(db.items(), key=lambda kv: kv[1]['w'] / kv[1]['h']):
        ar = r['w'] / r['h']
        loss = 1 - (ar / (16 / 9) if ar < 16 / 9 else (16 / 9) / ar)
        print(f"AR {ar:.3f}  {n:20} {r['w']}x{r['h']}  全画面で {loss:.1%} 切れる  {r['lic']}")
    return 0


def credit_line(name, r):
    """画面の出典＝「誰が（識別子）・パブリックドメイン」。PD の根拠は ref/CREDITS.md の権利の欄に書く（画面は短く）"""
    ident = r.get('ident')
    return f"出典：{r['author']}（{ident}・パブリックドメイン）" if ident else f"出典：{r['author']}（パブリックドメイン）"


# 頁の資料の年と「誰が」・権利（②の台帳 sources.md）
PAGE_DOC = {
    'V1': (1963, '米海軍 スレッシャー号の査問会', 'PD（米連邦の職務著作 17 U.S.C. §105）／海軍が FOIA の訴えで公開（第1回・2020-09-23）'),
    'X': (1963, '米海軍 スレッシャー号の査問会（証拠）', 'PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第9・10回・2021-05）'),
    'IR18': (1965, '米海軍長官（上級の意見書）', 'PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第18回）'),
    'R08': (1963, '米海軍 スレッシャー号の査問会', 'PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第8回）'),
    'J': (1965, '米議会 両院原子力合同委員会', 'PD（米議会の刊行物）／Stanford Digital Repository の PDF（印刷頁＋14＝PDF の頁）'),
    'No.710-64': (1964, '米国防総省', 'PD（米連邦の職務著作）／Wikimedia Commons「330-PSA-309-64a (22791587391).jpg」（NARA RG 330）'),
}


def page_credit(pr):
    sys.path.insert(0, str(HERE / 'tools'))
    import illu
    line = illu.rec_line([f'{_doc_code(pr)} p{pr}'])
    if not line:
        raise SystemExit(f'🔴 p{pr} の出典の行が作れない（`cuts/ss.REC_DOCS` に資料が無い）')
    return line


def cmd_credits(write=False):
    db = _db()
    pages = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    cj = {f'ep18/{n}.jpg': credit_line(n, r) for n, r in db.items()}
    cj.update({f'ep18/{k}.png': page_credit(int(k[2:])) for k in pages})
    # 🆕 ⑤b-7c：記録映画のひかえの静止画（fb_<カット>）＝その映画の出典（コマが切り出せなかったときだけ出る）
    sys.path.insert(0, str(HERE / 'tools'))
    import footage as FO
    cj.update({f'ep18/fb_{c}.jpg': FO.CLIPS[u['clip']]['credit'] for c, u in FO.USE.items()
               if not FO.CLIPS[u['clip']].get('stock')})
    rows = [f"| `{n}` | {r.get('cut') or '（章ファイル）'} | {r['year'] or '不明'} | {GROUND} | {r['author']} | "
            f"{r['hold']}　{r.get('url', '')} |" for n, r in db.items()]
    rows += [f"| `{k}` | {' '.join(sorted(p.get('cuts', {}))) or '（c104＝⑤b-8）'} | {PAGE_DOC[p['doc']][0]} | "
             f"{PAGE_DOC[p['doc']][2]} | {PAGE_DOC[p['doc']][1]} | "
             f"{(p['pdf'] + ' PDF ' + str(p['pdf_page']) + '頁') if p.get('pdf') else p['img']} |"
             for k, p in sorted(pages.items(), key=lambda kv: int(kv[0][2:]))]
    for k, v in cj.items():
        print(k, '|', v)
    print(f'… 写真 {len(db)}点・頁 {len(pages)}枚')
    if write:
        CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding='utf-8')
        md = CREDITS_MD.read_text(encoding='utf-8')
        # 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②）
        head = '## スレッシャー号のリメイク（1963-04-10・18本目）'
        hdr = '| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |'
        block = '\n'.join([
            head, '',
            '※2026-10-04（⑤b-7a）。`qa_out/ep18_assets.py credits --write` が書く（手で直さない）。旧版（3本目）の節は上の'
            '「USS Thresher (SSN-593)（1963-04-10・3本目）」＝旧版の誤り（Anefo の1点を「米海軍」・シーウルフの記録を「スカイラーク」）は'
            '直さない（公開ずみ・⑥で非公開にするだけ）。18本目は Anefo の1点（写っているのはノーチラス）とシーウルフの記録の頁を使わない。',
            '',
            '### 1. 写真（すべて米海軍の職務著作＝PD）',
            '- 出どころは3つ：NARA 289-T（RG 289・1963〜64年の捜索のアルバム・NARA の表示 Use: Unrestricted）／NARA 428-N（RG 428）・'
            '記録映画 85185 のコマ（RG 428・作り手は海軍写真センター）／Wikimedia Commons（隠しカテゴリ `PD US Navy`＋`CC-PD-Mark`）',
            '- 🔴 289-T の英字の説明札・428-N の台紙と札は**切り落とした**（`qa_out/ep18_assets.py` の crop＝OCR の文字の箱の外で切る）。'
            '頁全体を見せる `page24`（c911＝角の黒い塗り）だけ札が残る',
            '- 🔴 人が写る写真（§B2-2）：就役式（1961-08-03）の左の座った観客（私人）は**切り落とした**（x 385 より左）。甲板の乗員と'
            '式台の造船所の人（公的な任務）は残る（原寸で顔 約10px）。進水（1960）の岸の人は全員が後ろ姿か横向き',
            '- 撮影年が書かれていない・割れる点（289-T の造船所の写真2点と謝辞の頁の航走写真・スカイラークの2点）は撮影年を「不明」にし、'
            '**副題に年を書かない**（門番 credits）',
            '- 記録映画のコマは画素が縦長（SAR 10:11）＝655×480 に直した。動く映像（記録映画）は §4（⑤b-7c で `clips.json`）',
            '- Commons の新しい8点は、落とす前に一覧（名前・大きさ）でカズヤくんの了承を取った（2026-10-04）＝取ったファイルは'
            ' Commons の原本と SHA-1 が一致（`ref/ep18/img/fetched.json`＝git の外）',
            '',
            '### 2. 頁（査問会の記録・証拠・上級の意見書・議会の本・国防総省の発表の紙）＝⑤b-7b（2026-10-05）',
            '- 欄 `pg<通し頁>`＝台本の通し頁（V1＝p1〜300・X＝p1001〜・IR18＝p2001〜・R08＝p4001〜・J＝印刷頁＋8000・'
            'No.710-64＝p9801）。画面の出典は資料の名と頁（`illu.rec_line`）',
            '- 🔴 画面に映す頁は**見た目の字がある版だけ**（V1 の見えない43頁は使わない＝映像方針 §9）。塗り（b(1)・(b)(6)・'
            '［classified matter deleted］）は公開の版のまま',
            '- 頁は灰色の PNG（PDF を 200dpi・議会の本は 300dpi・海図は 100dpi で描いた）。薄い海図（c910）は SPEC の `levels` で'
            '濃淡だけ強める＝出典の行に「濃淡補正」',
            '- 名簿（認定4・R08 p.181）と名簿の終わり（p.184）の名前＝公務の乗員と、公務を果たすために乗っていた造船所・会社の人'
            '（認定6）＝実名の線（§B2-1）の内',
            '', hdr, '|---|---|---|---|---|---|', *rows, '', *stock_md(), *films_md()])
        if head in md:
            pre, rest = md.split(head, 1)
            nxt = rest.find('\n## ')
            md = pre + block + (rest[nxt:] if nxt >= 0 else '')
        else:
            md = md.rstrip('\n') + '\n\n' + block
        CREDITS_MD.write_text(md, encoding='utf-8')
        print(f'→ {CREDITS_JSON} ／ {CREDITS_MD}')
    return 0


def _get(url, timeout=60):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def cmd_fetch(yes=False):
    """Commons の新しい点を原寸で取り、SHA-1 を Commons の値と照らす（🔴 了承のあとだけ `--yes`）。"""
    want = {r['title']: n for n, r in PICK.items() if r['src'] == 'commons'}
    q = urllib.parse.urlencode(dict(action='query', format='json', prop='imageinfo', iiprop='size|sha1|url',
                                    titles='|'.join('File:' + t for t in want)))
    info = json.loads(_get('https://commons.wikimedia.org/w/api.php?' + q))
    rows = []
    for p in info['query']['pages'].values():
        ii = p['imageinfo'][0]
        rows.append((p['title'][5:], ii['size'], ii['width'], ii['height'], ii['sha1'], ii['url']))
    for t, sz, w, h, _, _ in rows:
        print(f'{want[t]:20} {w}x{h} {sz / 1e6:.2f}MB  {t}')
    print(f'計 {sum(r[1] for r in rows) / 1e6:.2f}MB・{len(rows)}点')
    if not yes:
        print('（取っていない＝了承のあとに --yes）')
        return 0
    NEW.mkdir(parents=True, exist_ok=True)
    fx = json.loads((NEW / 'fetched.json').read_text(encoding='utf-8')) if (NEW / 'fetched.json').exists() else {}
    bad = 0
    for t, sz, w, h, sha1, url in rows:
        out = NEW / t
        for k in range(4):
            try:
                b = _get(url)
                break
            except Exception as e:  # noqa: BLE001
                print(f'  … {t}: {e}（{5 * (k + 1)}秒待って取り直す）')
                time.sleep(5 * (k + 1))
        else:
            print(f'🔴 {t}: 取れなかった')
            bad += 1
            continue
        got = hashlib.sha1(b).hexdigest()
        if got != sha1 or len(b) != sz:
            print(f'🔴 {t}: SHA-1・大きさが Commons の原本と違う（{len(b)} / {sz}）')
            bad += 1
            continue
        out.write_bytes(b)
        # 落としかけを測らない＝ディスクから2回 md5（記憶 feedback-download-size-is-not-completion）
        m1, m2 = _md5(out), _md5(out)
        fx[t] = dict(sha1=sha1, size=sz, w=w, h=h, url=url, md5=m1, fetched=time.strftime('%Y-%m-%d'))
        print(f"✓ {t}  SHA-1 一致・md5 {m1}{'' if m1 == m2 else '（2回目が違う🔴）'}")
        time.sleep(1.0)
    (NEW / 'fetched.json').write_text(json.dumps(fx, ensure_ascii=False, indent=1), encoding='utf-8')
    return 1 if bad else 0


# ══════════════════════════════════════════════════════════
#  フリー素材の映像（🆕 ⑤b-7b・2026-10-05）＝映像方針 §22-3 (a) の「頭の1行の差し込み」11カット
# ══════════════════════════════════════════════════════════
# ルール §2-5c：テーマに関連した映像・画面に「イメージ」と出典（サイト名・撮影者名）・ライセンスは1本ずつサイトの頁で・
#   生成AIの素材は使わない（Pexels は規約で生成AIの投稿を認めない〈Terms & Policy Update 2024〉・Pixabay は生成AIに印を付ける＝
#   選んだ点には印が無い）・顔の分かる人と現代の艦を出さない・**落とす前に一覧でカズヤくんの了承**・【映像あり】と20%に数えない。
# 動画はリポに入れない（`ref/*` は git の外）＝本番は Actions が URL から取る（⑤b-7c で clips.json に URL と "stock": true）。
# 頁の情報は 2026-10-05 に内蔵ブラウザで各頁の VideoObject（JSON-LD）と本文から読み、大きさは HEAD（中身は落とさない）で測った
STOCK_DIR = DEST / 'stock'
STOCK_LIC = {'Pexels': ('Pexels License', 'https://www.pexels.com/license/'),
             'Pixabay': ('Pixabay Content License', 'https://pixabay.com/service/license-summary/')}


def S(cut, site, page, url, author, up, sec, size, what):
    return dict(cut=cut, site=site, page=page, url=url, author=author, up=up, sec=sec, size=size, what=what)


STOCK = {
    'docs_binders_7710340': S('c109', 'Pexels', 'https://www.pexels.com/video/documents-on-the-table-7710340/',
                              'https://videos.pexels.com/video-files/7710340/7710340-hd_2048_1080_25fps.mp4',
                              'Kaboompics', '2021-04-29', 13, 3008016, '机の上に積んだ書類の綴じ込み（人は写らない）'),
    'deep_rays_63427': S('c114', 'Pixabay', 'https://pixabay.com/videos/waves-ocean-sea-underwater-water-63427/',
                         'https://cdn.pixabay.com/video/2021/01/29/63427-506377691_medium.mp4',
                         'Jackdrafahl', '2021-01-30', 23, 19299854, '水の中から見上げた水面と光の筋'),
    'pier_blue_10354787': S('c215', 'Pexels', 'https://www.pexels.com/video/ripples-in-water-surface-under-a-pier-10354787/',
                            'https://videos.pexels.com/video-files/10354787/10354787-hd_2048_1080_30fps.mp4',
                            'Engin Akyurt', '2021-11-26', 60, 41749090, '桟橋の杭と海面のさざ波（人・船なし）'),
    'pier_dark_11812247': S('c220', 'Pexels', 'https://www.pexels.com/video/ripples-on-seawater-under-a-pier-11812247/',
                            'https://videos.pexels.com/video-files/11812247/11812247-hd_2048_1080_30fps.mp4',
                            'Engin Akyurt', '2022-04-14', 60, 41979822, '桟橋の下の暗い海面（人・船なし）'),
    'sea_dark_5668613': S('c511', 'Pexels', 'https://www.pexels.com/video/dark-surface-of-the-deep-water-5668613/',
                          'https://videos.pexels.com/video-files/5668613/5668613-hd_2048_1080_30fps.mp4',
                          'ROMAN ODINTSOV', '2020-10-22', 8, 4868884, '暗い沖の海面'),
    'deep_sun_48596': S('c805', 'Pixabay', 'https://pixabay.com/videos/underwater-rays-light-sun-48596/',
                        'https://cdn.pixabay.com/video/2020/08/30/48596-454825141_medium.mp4',
                        'ChristianBodhi', '2020-09-04', 20, 15731713, '水の中から見上げた太陽（暗い青）'),
    'deep_blue_32790667': S('c812', 'Pexels', 'https://www.pexels.com/video/underwater-ocean-view-with-sunlight-rays-32790667/',
                            'https://videos.pexels.com/video-files/32790667/13977645_1920_1080_60fps.mp4',
                            'JUN HO LEE', '2025-06-30', 14, 15176855, '青い水の中に差す光の筋'),
    'typewriter_33068304': S('c903', 'Pexels', 'https://www.pexels.com/video/vintage-typewriter-typing-close-up-33068304/',
                             'https://videos.pexels.com/video-files/33068304/14094862_1920_1080_20fps.mp4',
                             'Stefan', '2025-07-18', 48, 36589965, '古いタイプライターの活字の寄り'),
    'files_hands_6549976': S('c906', 'Pexels', 'https://www.pexels.com/video/looking-among-files-6549976/',
                             'https://videos.pexels.com/video-files/6549976/6549976-hd_1920_1080_25fps.mp4',
                             'Tima Miroshnichenko', '2021-01-20', 22, 9644835, '引き出しの記録のカードを手で繰る（顔は写らない）'),
    'seabed_sand_11781634': S('ca05', 'Pexels', 'https://www.pexels.com/video/time-lapse-of-a-sandy-seabed-11781634/',
                              'https://videos.pexels.com/video-files/11781634/11781634-hd_1920_1080_60fps.mp4',
                              'Markus Winkler', '2022-04-11', 46, 33825641, '光のゆらぐ砂の海底（タイムラプス）'),
    'seabed_murky_33896777': S('ca06', 'Pexels', 'https://www.pexels.com/video/underwater-ocean-floor-with-sand-movement-33896777/',
                               'https://videos.pexels.com/video-files/33896777/14385381_1920_1080_60fps.mp4',
                               'JUN HO LEE', '2025-09-14', 15, 15639270, '砂の動く海の底（濁った青緑）'),
}


def stock_md():
    """ref/CREDITS.md の18本目の節の「3. フリー素材の映像」（stock.json＝取った点だけ）。表にしない＝門番 credits の写真の表と混ぜない"""
    p = DEST / 'stock.json'
    if not p.exists():
        return []
    led = json.loads(p.read_text(encoding='utf-8'))
    out = ['### 3. フリー素材の映像（イメージ）＝⑤b-7b（2026-10-05 カズヤくん了承・頭の1行の差し込み11カット＝差し込みは ⑤b-7c）',
           '- ルール §2-5c：画面に「イメージ（フリー素材）：サイト名／撮影者」を出す・【映像あり】と20%に数えない・動画はリポに入れない'
           '（`ref/ep18/stock/`＝git の外・本番は Actions が URL から取る）',
           '- ライセンス：Pexels License（https://www.pexels.com/license/）／Pixabay Content License'
           '（https://pixabay.com/service/license-summary/）＝商用可・クレジット不要・改変可。生成AI＝Pexels は規約で投稿を認めない・'
           'Pixabay は印を付ける（選んだ点に印なし）', '']
    for n, r in led.items():
        out.append(f"- `{n}`（{r['cut']}）{r['what']}＝{r['site']}・{r['author']}・投稿 {r['up']}・{r['w']}×{r['h']}・{r['dur']}秒・"
                   f"{r['license']}・取った日 {r['fetched']}　{r['page']}")
    return out + ['']


def stock_credit(name):
    """画面の出典の行（フリー素材）＝「イメージ」と出典（サイト名・撮影者名）。⑤b-7c で差し込みの層に出す"""
    r = STOCK[name]
    return f"イメージ（フリー素材）：{r['site']}／{r['author']}"


def cmd_stock(yes=False):
    """フリー素材の一覧（了承の表）。`--yes`＝了承のあとに落とす（ref/ep18/stock/＝git の外）→ 大きさ・md5 2回・ffprobe → stock.json"""
    import subprocess
    tot = 0
    for n, r in STOCK.items():
        tot += r['size']
        print(f"{r['cut']:5} {n:24} {r['site']:7} {r['author']:20} {r['up']}  {r['sec']:>3}秒  {r['size'] / 1e6:6.1f}MB  {r['what']}")
    print(f'計 {len(STOCK)}本・{tot / 1e6:.1f}MB')
    if not yes:
        print('（落としていない＝了承のあとに --yes）')
        return 0
    STOCK_DIR.mkdir(parents=True, exist_ok=True)
    led = json.loads((DEST / 'stock.json').read_text(encoding='utf-8')) if (DEST / 'stock.json').exists() else {}
    bad = 0
    for n, r in STOCK.items():
        out = STOCK_DIR / f'{n}.mp4'
        req = urllib.request.Request(r['url'], headers={'User-Agent': 'Mozilla/5.0', 'Referer': r['page']})
        for k in range(4):
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    b = resp.read()
                break
            except Exception as e:  # noqa: BLE001
                print(f'  … {n}: {e}（{5 * (k + 1)}秒待って取り直す）')
                time.sleep(5 * (k + 1))
        else:
            print(f'🔴 {n}: 取れなかった')
            bad += 1
            continue
        if len(b) != r['size']:
            print(f"🔴 {n}: 大きさが HEAD と違う（{len(b)} / {r['size']}）")
            bad += 1
            continue
        out.write_bytes(b)
        # 落としかけを測らない＝ディスクから2回 md5（記憶 feedback-download-size-is-not-completion）
        m1, m2 = _md5(out), _md5(out)
        pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                             'stream=width,height,r_frame_rate:format=duration', '-of', 'json', str(out)],
                            capture_output=True, text=True)
        info = json.loads(pr.stdout or '{}')
        st = (info.get('streams') or [{}])[0]
        lic = STOCK_LIC[r['site']]
        led[n] = dict(r, file=f'stock/{n}.mp4', md5=m1, w=st.get('width'), h=st.get('height'), fps=st.get('r_frame_rate'),
                      dur=round(float((info.get('format') or {}).get('duration') or 0), 2), license=lic[0], license_url=lic[1],
                      credit=stock_credit(n), fetched=time.strftime('%Y-%m-%d'), approved='2026-10-05 カズヤくん（一覧で了承）')
        print(f"✓ {n}  {st.get('width')}x{st.get('height')}  {led[n]['dur']}秒  md5 {m1}{'' if m1 == m2 else '（2回目が違う🔴）'}")
        time.sleep(1.0)
    (DEST / 'stock.json').write_text(json.dumps(led, ensure_ascii=False, indent=1), encoding='utf-8')
    return 1 if bad else 0


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7c（2026-10-05）：動く映像＝記録映画12本（NARA RG 428）とフリー素材11本の台帳
# ══════════════════════════════════════════════════════════
# 記録映画は (c) の了承（10-04）＝**丸ごとは保存しない**：ショットの境目は1本につき網から1回だけ読み流して測り（1秒1コマ）、
#   本番（Actions）は `footage.py` が URL から区間だけ切り出す（`"range": true`＝落とさない）。
# 値は 2026-10-05 に NARA のカタログ API（`/proxy/records/search?naId=`）の objectUrl・HEAD（大きさ）・ffprobe（720×480・
#   SAR 10:11・DAR 15:11・60p・progressive）で測った。権利＝米海軍の職務著作（海軍写真センター 428-NPC）＝PD。
#   NARA の表示は Use: Undetermined（NARA が未判定という意味＝制限ではない・materials.md §1）
MOPIX = 'https://catalog.archives.gov/medialz/mopix/428/NPC/'


def Fm(npc, sec, size, title, what, year=None):
    return dict(npc=npc, sec=sec, size=size, title=title, what=what, year=year)


FILMS = {
    '85185': Fm('36843', 789.38, 215134981, 'USS THRESHER (SSN-593)', 'カラーの航走（セイルの593・艦橋の乗員）'),
    '83213': Fm('28682', 189.68, 51561325, 'LAUNCHING OF USS THRESHER (SSN-593) Naval Shipyard, Portsmouth',
                '1960年の進水（空から見た造船所と艦）', 1960),
    '83750': Fm('32793', 281.55, 76909073, 'SEARCH FOR USS THRESHER (SSN-593)', '捜索の海の艦（空から）', 1963),
    '83751': Fm('32794', 310.72, 84771038, 'SEARCH FOR USS THRESHER (SSN-593)', '捜索の艦（空から・艦番号179 ほか）', 1963),
    '83746': Fm('32786', 505.03, 137578490, 'SEARCH FOR USS THRESHER (SSN-593) On Board USS ALLEGHENY (ATA-179)',
                'アレゲニーの艦上の乗員と機器（乗用車の場面は使わない）', 1963),
    '83737': Fm('32762', 515.32, 140627185, 'SEARCH FOR USS THRESHER (SSN-593) 250 Miles East of Cape Cod over Atlantic',
                '哨戒機から見た捜索の海', 1963),
    '83759': Fm('32824', 178.08, 48405035, 'SEARCH FOR USS THRESHER (SSN-593) Naval Shipyard, Boston, Mass',
                'ボストンの造船所・艦番号422 の潜水艦（トロ）', 1963),
    '83795': Fm('32987', 248.48, 67851947, 'THRESHER SEARCH 220 Miles East of Cape Cod at Sea', '海の上の初代トリエステ', 1963),
    '83766': Fm('32855', 194.0, 52555357, 'SEARCH FOR USS THRESHER (SSN-593) Boston Naval Shipyard', 'ボストンの造船所', 1963),
    '83757': Fm('32803', 642.98, 175367398, 'SEARCH FOR USS THRESHER (SSN-593) TRIESTE Test Dive Boston, Mass. & at Sea',
                '初代トリエステの試験潜航（1963-05-03・ボストンの東 約60マイル）', 1963),
    '83741': Fm('32767', 574.73, 156798136, 'USS THRESHER (SSN-593) MEMORIALS', '追悼（参列者の顔のショットは使わない）', 1963),
    '83740': Fm('32766', 327.67, 89347981, 'THRESHER MEMORIAL SERVICE Portsmouth, N. H',
                'ポーツマスの追悼の式（頭2秒は NARA のロゴ・顔の分かるショットは使わない）', 1963),
}
FILM_CREDIT = '出典：米海軍の記録映画（NARA {na}・パブリックドメイン）'


def cmd_clips():
    """ref/ep18/clips.json（footage.CLIPS）＝記録映画12本（nara<naId>）＋フリー素材11本（stock.json の実測）"""
    out = {}
    for na, f in FILMS.items():
        out[f'nara{na}'] = dict(url=NARA + na, media=MOPIX + f"428-npc-{f['npc']}.mp4", range=True,
                                credit=FILM_CREDIT.format(na=na), src='nara', at=0.0, date=f['year'],
                                what=f['what'], title=f['title'], w=720, h=480, fps=60.0, sar='10:11', dar='15:11',
                                sec=f['sec'], size=f['size'], dispw=655, decoded=[655, 480])
    led = json.loads((DEST / 'stock.json').read_text(encoding='utf-8'))
    for n, r in led.items():
        num, den = (int(x) for x in str(r['fps']).split('/'))
        out[n] = dict(url=r['page'], media=r['url'], stock=True, file=f"ep18/{r['file']}", credit=r['credit'], src='stock',
                      at=0.0, date=r['up'], what=r['what'], w=r['w'], h=r['h'], fps=round(num / den, 3), sar='1:1',
                      sec=r['dur'], size=r['size'], md5=r['md5'], dispw=r['w'], decoded=[r['w'], r['h']],
                      license=r['license'], license_url=r['license_url'], author=r['author'], site=r['site'])
    p = DEST / 'clips.json'
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'→ {p}（記録映画 {len(FILMS)}本・フリー素材 {len(led)}本）')
    return 0


# 🔴 境目の物差し（隣の1秒の見た目の差 ＞ 14）が動きの速い水面で「全部の秒が境目」になる素材＝1ショットに直す（根拠と目で確かめた事）。
#    ⚠️ 表に足すのは、差が**全部**しきい値を超える（静かな秒が1つも無い＝切り替わりと見分けられない）うえ、境目の前後を目で見た素材だけ
SHOT_ONE = {
    'sea_dark_5668613': '1秒ごとの差が全部 24.8〜29.2＝波の速い動き・4秒の「境目」の前後 1.0／3.5／4.5／7.0秒を並べて同じ水面の続き'
                        '（2026-10-05 ⑤b-7c に目で確かめた）',
}


# 🔴 境目の物差しが**短いショットをまとめてしまった**所＝割る（秒・根拠と目で確かめた事）。
#    物差しは「続けて差が大きい秒」を1つの境目に畳む（ディゾルブ用）＝3秒の短いショットが前後の切り替わりと一緒に畳まれる
SHOT_SPLIT = {
    'nara85185': {465.0: '#62（462〜469秒）の中で切り替わる＝462〜464秒は遠くの艦・465秒から「593」のセイルの寄り（1秒1コマを並べて'
                         '2026-10-05 ⑤b-7c に目で確かめた・試し焼き 37246867517 の c102 の頭が遠くの艦だった）'},
}


def _split(shots, cuts):
    out = []
    for s in shots:
        inner = sorted(t for t in cuts if s['start'] < t < s['until'])
        a = s['start']
        for t in inner + [s['until']]:
            out.append(dict(start=a, until=t, motion=s['motion']))
            a = t
    return out


def cmd_shots(probe):
    """ref/ep18/shots.json（footage.SHOTS）。記録映画＝⑤b-7c に1本につき網から1回だけ読み流した1秒1コマから
    `tools/shots.boundaries()`（同じ物差し）で出した境目（probe＝scratchpad の films/probe.json）・フリー素材＝手元の mp4 を
    `tools/shots.shots_of()` で"""
    sys.path.insert(0, str(HERE / 'tools'))
    import shots
    pr = json.loads(Path(probe).read_text(encoding='utf-8'))
    out = {}
    for na in FILMS:
        v = pr[na]
        how = '1秒1コマを読み流して tools/shots.boundaries（2026-10-05・丸ごとは保存しない）'
        sh = v['shots']
        if f'nara{na}' in SHOT_SPLIT:
            sp = SHOT_SPLIT[f'nara{na}']
            sh = _split(sh, sp)
            how += '＋割った境目 ' + '・'.join(f'{t:.0f}秒（{w}）' for t, w in sp.items())
        out[f'nara{na}'] = dict(src=MOPIX + f"428-npc-{FILMS[na]['npc']}.mp4", dur=float(v['nframes']), how=how, shots=sh)
    led = json.loads((DEST / 'stock.json').read_text(encoding='utf-8'))
    for n, r in led.items():
        sh, dur = shots.shots_of(str(DEST / r['file']))
        how = ' 手元の mp4 を tools/shots.shots_of'
        if n in SHOT_ONE:
            sh = [dict(start=0.0, until=float(int(dur)), motion=max(s['motion'] for s in sh))]
            how += f'＋1ショットに直した（{SHOT_ONE[n]}）'
        out[n] = dict(src=r['file'], dur=round(dur, 2), how=how.strip(), shots=sh)
        print(f'  {n}: {dur:.0f}秒・ショット {len(sh)}')
    p = DEST / 'shots.json'
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f"→ {p}（{len(out)}本・ショット {sum(len(v['shots']) for v in out.values())}）")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（コマが切り出せなかったときだけ出る絵）＝footage.USE の start の1コマ。
    記録映画＝ref/ep18/fb_<カット>.jpg（URL から1コマ・SAR を直して 655×480）／フリー素材の頭＝ref/ep18/stock/fb_<カット>.jpg
    （手元の mp4 から・幅1280）。🔴 名前に fb_ を付ける＝門番 credits は「動画の出典を借りる」として表と照らさない"""
    import subprocess
    sys.path.insert(0, str(HERE / 'tools'))
    import footage as FO
    bad = 0
    for cid, u in FO.USE.items():
        if only and cid not in only:        # `fb c102` のようにカットを書けばそのカットだけ（ほかの md5 を動かさない）
            continue
        c = FO.CLIPS[u['clip']]
        t = float(u['start'])
        if c.get('stock'):
            src, dst, vf, net = str(HERE / 'ref' / c['file']), DEST / 'stock' / f'fb_{cid}.jpg', 'scale=1280:-2', []
        else:
            src, dst, vf = c['media'], DEST / f'fb_{cid}.jpg', 'scale=iw*sar:ih,setsar=1'
            net = ['-user_agent', UA, '-rw_timeout', '60000000']
        for k in range(3):
            r = subprocess.run(['ffmpeg', '-y', '-nostdin', '-v', 'error', *net, '-ss', f'{t:.2f}', '-i', src,
                                '-frames:v', '1', '-vf', vf, '-q:v', '3', str(dst)], capture_output=True, text=True, timeout=600)
            if r.returncode == 0 and dst.exists():
                break
            time.sleep(5 * (k + 1))
        else:
            print(f'🔴 {cid}: ひかえの静止画が作れない（{r.stderr[-160:]}）')
            bad += 1
            continue
        print(f"✓ {cid:5} {u['clip']:22} {t:7.1f}秒 → {dst.relative_to(HERE).as_posix()}")
    return 1 if bad else 0


def films_md():
    """ref/CREDITS.md の18本目の節の「4. 記録映画（動く映像）」（表にしない＝門番 credits の写真の表と混ぜない）"""
    out = ['### 4. 記録映画（動く映像）＝⑤b-7c（2026-10-05・取得は 10-04 カズヤくん了承＝丸ごとは保存しない）',
           '- NARA RG 428（海軍写真センター 428-NPC）の記録映画＝米海軍の職務著作＝PD（17 U.S.C. §105）。NARA の表示 Use: '
           'Undetermined（未判定＝制限ではない）。画面の出典＝「出典：米海軍の記録映画（NARA <naId>・パブリックドメイン）」',
           '- すべて 720×480・画素が縦長（SAR 10:11）＝655×480 に直して額装＋地のぼかし（映像方針 §8）。【映像あり】は付けない',
           '- 本番（Actions・Modal）は `tools/footage.py` が URL から使う区間だけ切り出す（落とさない＝`"range": true`）。'
           'ショットの境目は `ref/ep18/shots.json`（1秒刻み）・使う区間は `footage.USE`', '']
    for na, f in FILMS.items():
        out.append(f"- NARA {na}「{f['title']}」{f['what']}・{f['sec']:.0f}秒　{NARA + na}")
    return out + ['']


def main():
    a = sys.argv[1:] or ['check']
    cmd = a[0]
    if cmd == 'clips':
        return cmd_clips()
    if cmd == 'shots':
        return cmd_shots(a[1])
    if cmd == 'fb':
        return cmd_fb(set(a[1:]) or None)
    if cmd == 'build':
        return cmd_build(set(a[1:]) or None)
    if cmd == 'check':
        return cmd_check()
    if cmd == 'panel':
        return cmd_panel()
    if cmd == 'credits':
        return cmd_credits('--write' in a)
    if cmd == 'fetch':
        return cmd_fetch('--yes' in a)
    if cmd == 'pages':
        return cmd_pages({int(x) for x in a[1:]} or None)
    if cmd == 'stock':
        return cmd_stock('--yes' in a)
    raise SystemExit(f'知らない命令: {cmd}')


if __name__ == '__main__':
    sys.exit(main())
