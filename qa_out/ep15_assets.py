# -*- coding: utf-8 -*-
"""ep15_assets.py — 15本目（リノ・エアレース2011）の**写真の束**・**報告書と資料の頁**を作る（2026-09-30 ⑤b-6 新設）。

`qa_out/ep14_assets.py`（14本目）の形を写した。写真は ⑤b-6 で Commons から取った19点
（`ref/ep15/probe/fetch15_img.py`・カズヤくん許可 09-30・控え＝`ref/ep15/img/meta.json`・`fetched.json`＝SHA-1 照合ずみ）。
ここでやるのは「名前を付ける・幅3000px に縮める・権利を表にする・頁を焼く・切り口を決める」だけ。動く映像は無い（【映像あり】なし＝09-25）。

■ 素材（②の台帳 `ref/ep15/materials.md` §3 の記号 → 名前 → 当てるカット＝章ファイルの PLAN）
  事故の週の事故機・同じレースの機・会場（tataquax・CC BY-SA 2.0）12点＝**額装・無改変・1点1カット**（`cuts/ss.py` の `frame_only()`）
  来歴（Bill Larkins・BY-SA 2.0）3点／会場の空撮 D4（BY-SA 2.0）／2010年の事故機（jeggernot・CC BY 2.0）2点／2016年の講習会 D5（CC BY 4.0）
■ 🔴 **報告書の courtesy の写真（図5〜10・15・17）＝紙面の引用**（ルール §2-6c・09-25 カズヤくん）：
  写真だけを切り出さない＝**図・説明の行・撮影者の行まで**を紙面のまま切った画像（`pg<頁>_fig<NN>.jpg`）にし、
  `assets.json` に `frame=True`（引用）で入れる＝BY-SA と同じ網（額装・寄り0・色を変えない・1点1カット）
■ 頁（`ss.page(N)`＝台本の頁番号・`ref/ep15/v1_build/make_pages.py` の通し番号）。**同じ頁を2カットで別の所を切る**
  （p15・p32・p35・p37）＝切り口は**カットごと**（`pages.json` の `cuts`＝`ss.ptrim(cid)`）。文字の頁は目印の語の行から、
  図の頁は PDF の行・画像の位置から**行間の真ん中で**機械で決める（門番 edges＝行の途中で切らない）

    python qa_out/ep15_assets.py build     # ref/ep15/<名>.jpg ＋ assets.json
    python qa_out/ep15_assets.py pages     # ref/ep15/pg<頁>.png ＋ pg<頁>_fig<NN>.jpg ＋ pages.json（cuts つき）
    python qa_out/ep15_assets.py check     # PICK・assets.json・ファイルが揃っているか
    python qa_out/ep15_assets.py panel     # 縦横比の並び（`cuts/ss.py` の PANEL_AR を決める材料）
    python qa_out/ep15_assets.py credits [--write]   # credits.json と ref/CREDITS.md の表
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SRC = HERE / 'ref' / 'ep15' / 'img'
PDF = HERE / 'ref' / 'ep15' / 'src'
DEST = HERE / 'ref' / 'ep15'
DB = DEST / 'assets.json'
PAGES_JSON = DEST / 'pages.json'
CREDITS_JSON = DEST / 'credits.json'
CREDITS_MD = HERE / 'ref' / 'CREDITS.md'
MAXW = 3000


def C(key, slot, year, **kw):
    """Commons の1点。key＝`ref/ep15/img/meta.json` の鍵（materials.md の記号）。"""
    return dict(src='commons', key=key, slot=slot, year=year, **kw)


# 名前 → 素材。cut＝当てるカット（PLAN の画の欄）。**BY-SA は1点1カット**（`ss.check_frame_only` が止める）
#   🔴 tataquax の撮影時刻（EXIF）は日本時間のまま＝現地は −16時間（materials.md §3-0・推定）。副題は「事故のレースの離陸／周回中」まで
PICK = {
    # ── 事故の週の事故機（§3-1）────────────────────────────────
    'gg_below_race': C('B4', 'crash', 2011, cut='c205',
                       note='飛んでいる事故機を真下から（尾翼の「177」・右翼の「NX79111」）。事故のレースの周回中（推定）'),
    'gg_takeoff_race': C('A5', 'crash', 2011, cut='c208',
                         note='事故機の最後の離陸の滑走（「177」「THE GALLOPING GHOST」）。事故のレースの離陸（推定）'),
    'gg_taxi_0915': C('A6', 'n79111', 2011, cut='c401', note='前日（9/15 現地）・地上を走る事故機。人物は操縦席だけ'),
    'gg_nose_0916': C('B5', 'n79111', 2011, cut='c419', note='事故の日の朝（9/16 現地）・ピットの機首「THE GALLOPING GHOST」'),
    'gg_pit_0914': C('B6', 'n79111', 2011, cut='c504', note='事故の週（9/14 現地）・ピットの全身'),
    # ── 事故の日の会場と同じレースの機（§3-2）──────────────────────
    'strega_taxi': C('A1', 'race2011', 2011, cut='c207', note='ストレガ（1位の機・赤白「7」）のタキシング＝事故のレースの前'),
    'voodoo_taxi': C('A3', 'race2011', 2011, cut='c203', note='ヴードゥー（2位の機・紫と黄「5」）のタキシング'),
    'strega_takeoff': C('A4', 'race2011', 2011, cut='c202', note='ストレガの離陸の滑走'),
    'strega_below': C('B2', 'race2011', 2011, cut='c219', note='ストレガを真下から（事故のレースの周回中＝推定）'),
    'voodoo_below': C('B3', 'race2011', 2011, cut='c318', note='ヴードゥーを真下から（事故のレースの周回中＝推定）'),
    'stands_0916': C('E70', 'race2011', 2011, cut='c801', note='ピットの機体の奥に満員の観客席（遠景）・事故の日の昼'),
    'pylon_0916': C('E85', 'race2011', 2011, cut='c204', note='レースのパイロン（鉄塔）と上に立つ審判2人・事故の日'),
    # ── 来歴（Bill Larkins・§3-3）＝撮影年は題名の「69」「70」（Commons の日付 2011 は取り込みの年）──────────
    'candace_1969': C('C1', 'n79111', 1969, cut='c405', note='白黒・「Miss Candace」「69」「N79111」'),
    'taxi_1970': C('C2', 'n79111', 1970, cut='c406', note='白黒・タキシング・「69」'),
    'damage_1970': C('C3', 'n79111', 1970, cut='c407', note='白黒・格納庫の中・胴体の下が壊れた状態（題名「after damage」）'),
    # ── 2010年の事故機（jeggernot・CC BY 2.0）§3-4 ─────────────────────
    'gg_nose_2010': C('C4', 'n79111', 2010, cut='c417', note='ピットの機首・プロペラ。🔴 整備の人と周りの人の顔＝顔だけモザイク（MASK）'),
    'gg_pit_2010': C('C5', 'n79111', 2010, cut='c416', note='ピットの全身・「177」。🔴 手前の人とテントの人の顔＝顔だけモザイク（MASK）'),
    # ── 会場（§3-5）──────────────────────────────────────────
    'stead_2009': C('D4', 'stead', 2009, cut='c112', note='高空から見たステッド空港と周りの町・湖・雪の山（2009-03-28）'),
    'seminar_2016': C('D5', 'stead', 2016, cut='c906', note='2016年の講習会（Pylon Racing Seminar）の駐機場'),
}
# 🔴 顔だけモザイク（2026-09-30 カズヤくん「顔写りについては、モザイク処理でも構いません」「顔面のみのモザイク加工」）。
#    **CC BY の点だけ**（許諾が手直しを許す）。⚠️ BY-SA はモザイク自体が翻案＝かけない（ルール §5b-52・§B2-2）
#    範囲＝原寸（1280×853）の画素 (x0, y0, x1, y1, 誰)。⑤b-6 に2倍の拡大と10px の目盛りで読んだ（scratchpad `grid15.py`）。
#    元画像そのものを直す＝`cuts/ss.py` の NEEDS_MASK に載せ、`python tools/check_photo_mask.py --record` で md5 を記録
MOSAIC_PX = 8          # モザイクの升の大きさ（原寸の画素）。顔の幅 40〜70px ＝ 5〜9升＝見分けられない
MASK = {
    'gg_nose_2010': [(312, 478, 356, 520, '翼の下に座る人'),
                     (748, 520, 815, 585, '緑の服の整備の人'),
                     (860, 495, 935, 580, '青い服の整備の人'),
                     (1228, 465, 1280, 565, '右端の人')],
    'gg_pit_2010': [(18, 432, 62, 478, '左端のサングラスの人'),
                    (52, 470, 118, 515, '帽子の人'),
                    (238, 422, 292, 478, '黒い帽子の人'),
                    (138, 478, 185, 512, '赤いジープの人（確かめの切り出しで見つけて足した）'),
                    (888, 395, 935, 440, 'テントの人1'),
                    (938, 368, 978, 405, 'テントの人2'),
                    (980, 405, 1020, 445, 'テントの人3'),
                    (1038, 350, 1080, 392, 'テントの人4'),
                    (1082, 352, 1120, 395, 'テントの人5'),
                    (1125, 340, 1165, 380, 'テントの人6'),
                    (1228, 438, 1275, 485, '右端の白い帽子の人')],
}


def mosaic(im, boxes, scale=1.0):
    """顔の範囲だけを升目にする（縮めて NEAREST で戻す）。scale＝原寸からの縮尺（束は幅3000px まで）。"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        b = tuple(round(v * scale) for v in (x0, y0, x1, y1))
        reg = im.crop(b)
        n = max(1, round(MOSAIC_PX * scale))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), b[:2])
    return im


# 画面の出典の「誰が」（Commons の撮影者の欄が長い点・Flickr の名前で名乗る点）
WHO = {
    'stead_2009': 'Shawn from Airdrie',
    'gg_nose_2010': 'jeggernot', 'gg_pit_2010': 'jeggernot',
    'seminar_2016': 'Don Ramey Logan',
}
for _n, _r in PICK.items():
    if _r['key'][0] in 'ABE':
        WHO[_n] = 'tataquax'           # 私人（日本の観客）＝Flickr の名前だけ（materials.md §3-0）
    elif _r['key'] in ('C1', 'C2', 'C3'):
        WHO[_n] = 'Bill Larkins'

# ══════════════════════════════════════════════════════════
#  頁（台本の頁番号＝`ref/ep15/v1_build/make_pages.py` の通し番号。AAB＝p1〜52・#40＝p1001〜・#33＝p2001〜・
#      #14＝p3001〜・#53＝p4001〜・勧告書 A-12-08＝p6001〜）
# ══════════════════════════════════════════════════════════
# (通し番号の頭, ファイル, 資料の鍵＝`cuts/ss.REC_DOCS`, dpi)。**頭の大きい順**（`next()` で最初に当たる）
DOCS = ((6001, 'ntsb_recletter_A-12-008.pdf', '勧告書', 200),
        (4001, 'ntsb_docket_53_aircraft_performance_study.pdf', '#53', 200),
        (3001, 'ntsb_docket_14_data_recorders_factual.pdf', '#14', 200),
        (2001, 'ntsb_docket_33_survival_factors_operations_factual.pdf', '#33', 200),
        (1001, 'ntsb_docket_40_materials_lab_12-029.pdf', '#40', 200),
        (1, 'AAB1201.pdf', 'AAB', 200))
PANEL_AR_T = 1120 / 648      # 額の最大の箱（`scene_jiko.PANEL_MAXW × PANEL_MAXH`）の縦横比＝文字の頁の切り出しの目標
# 切り口（カット → (頁, 切り方)）。切り方：
#   ('anchor', 目印)       … 文字の頁：目印の語（空白を除いた原文）の行を真ん中に、額の縦横比になるまで上下の行を足す
#   ('box', 上, 下[, dict]) … 図の頁：中身の上の端と下の端（頁の割合）を渡すと、**上下の要素とのあいだの真ん中**で切る。
#                            左右は中身の要素の端＋12pt。dict の cap＝真ん中が遠いときの余白の上限（頁の割合）
#   ('img', 番号)          … 図の頁：その頁の画像（大きい順の番号）の矩形だけ（NTSB の写真＝PD。courtesy には使わない）
# ⚠️ 値（上の端・下の端）は ⑤b-6（09-30）に PDF の行・画像の位置を測った（scratchpad `probe_pages.py`）
PAGE_CUTS = {
    # ── 文字の頁（16）────────────────────────────────────────────
    'c110': (1, ('box', 0.053, 0.181, dict(cap=0.03))),   # 表紙の右上の題の4行（下の表紙の画像〈中身を見ていない〉は入れない）
    'c304': (28, ('box', 0.193, 0.620)),                  # 経過の表（題「Table. Summary of events.」〜下の罫）
    'c402': (12, ('anchor', 'TheP-51Dvariantenteredproduction')),
    'c409': (35, ('anchor', 'receivedaspecialairworthinesscertificate')),
    'c503': (13, ('anchor', 'Eachaileronwasshortenedtoabout3feet')),
    'c507': (15, ('anchor', 'groundcrewwereawareofanydetaileddrawings')),
    'c601': (35, ('anchor', 'basedandmaintainedatLeewardAirRanchAirport')),
    'c608': (36, ('anchor', 'Telemetrydatashowedthatabout23minutes')),
    'c611': (15, ('anchor', 'controllablethroughoutitsnormalrangeofspeeds')),
    'c618': (37, ('anchor', 'Onthe2010and2011entrydocuments')),
    'c624': (51, ('anchor', 'submittedsuchinaccurateinformation')),
    'c703': (37, ('anchor', 'nothavingenoughthreadsprotrudingfromthenut')),
    'c724': (52, ('box', 0.091, 0.280)),                  # 「3. PROBABLE CAUSE」と推定原因の段落だけ（下の委員の名は入れない）
    'c818': (17, ('anchor', 'requireadistanceof500feet')),
    'c901': (43, ('anchor', 'January10,2012,investigative')),
    'c902': (6001, ('box', 0.107, 0.370)),                # 勧告書の上だけ＝紋章・宛名・日付の欄（460ノットと人数の段落は映さない）
    # ── 図・写真の頁（NTSB の図＝PD）────────────────────────────────
    'c105': (32, ('img', 0)),                             # 図14 の写真だけ（冒頭の物証）
    'c708': (32, ('box', 0.091, 0.383)),                  # 図14＋説明の行（新品と事故機の詰め物の比べ）
    'c211': (20, ('box', 0.091, 0.485)),                  # 図3 駐機場の配置
    'c308': (29, ('box', 0.173, 0.538)),                  # 図11 縦の加速度
    'c501': (14, ('box', 0.091, 0.486)),                  # 図2 事故機の図
    'c707': (31, ('box', 0.176, 0.606)),                  # 図13 右の板のちょうつがい（説明の行と Note まで）
    'c209': (2009, ('box', 0.300, 0.663)),                # #33 図7 コースを航空写真に重ねた図
    'c805': (2019, ('box', 0.098, 0.582)),                # #33 図14 救護の配置
    'c814': (2015, ('box', 0.098, 0.477)),                # #33 図13 駐機場の斜めの空撮
    'c317': (3014, ('box', 0.0, 1.0, dict(rot=True))),    # #14 図12 航跡（横向きの頁＝回転を直して図と説明の行）
    'c319': (4021, ('box', 0.091, 0.366)),                # #53 図18 ストレガの後方乱気流
    # ── #40 材料の試験の図（PD・札は英字のまま＝紙面）──────────────────────
    'c706': (1034, ('box', 0.117, 0.454)),                # 図1 左の昇降舵と板の破片・ちょうつがいの札
    # 図7 ねじの出っ張り＝写真だけ（黒い矢印の先の黄色の線を大きく＝09-30 に 300dpi で見て、題ごとだと画面で数画素だった）
    'c710': (1036, ('img', 3)),
    'c713': (1037, ('box', 0.356, 0.677)),                # 図11 内側のねじの折れ口と横から
    'c714': (1038, ('box', 0.390, 0.643)),                # 図14 疲労の筋＋右の題
    'c718': (1041, ('box', 0.117, 0.334)),                # 図22 曲がって折れたリンクの管＋右の題
}
# 🔴 courtesy の写真（紙面の引用）＝図・説明の行・撮影者の行まで（写真だけにしない）。名前 → (頁, 図, 上, 下, 撮影者, カット)
#    名前は `pg<頁>_fig<NN>`＝頁の切り出し（門番 textscreens は名前の `/pg` で「頁の画像」と数える＝PLAN の「図・写真の頁」と合う）。
#    ⚠️ 09-30：最初 `pg<頁>_fig<NN>` と名付けて textscreens が「写真」と数え、PLAN と8件食い違った
QUOTE_FIGS = {
    'pg23_fig05': (23, 5, 0.091, 0.505, 'Jonathan Apfelbaum', 'c301'),
    'pg24_fig06': (24, 6, 0.141, 0.587, 'Jonathan Apfelbaum', 'c306'),
    'pg25_fig07': (25, 7, 0.091, 0.521, 'Jonathan Apfelbaum', 'c309'),
    'pg26_fig08': (26, 8, 0.091, 0.521, 'Jonathan Apfelbaum', 'c310'),
    'pg27_fig09': (27, 9, 0.091, 0.505, 'Frank Ranney', 'c311'),
    'pg27_fig10': (27, 10, 0.520, 0.898, 'Julia Kirchenbauer', 'c103'),
    'pg33_fig15': (33, 15, 0.245, 0.659, 'Florian Schmehl', 'c520'),
    'pg34_fig17': (34, 17, 0.502, 0.897, 'Florian Schmehl', 'c521'),
}
QUOTE_DPI = 300
# 画面の出典に添える図の番号（図の頁だけ）
PAGE_FIG = {14: '図2', 20: '図3', 29: '図11', 31: '図13', 32: '図14', 1034: '図1', 1036: '図7', 1037: '図11',
            1038: '図14', 1041: '図22', 2009: '図7', 2015: '図13', 2019: '図14', 3014: '図12', 4021: '図18'}
# 出典の行を手で書く頁（`illu.rec_line` が頁を出さない資料）
PAGE_LINE = {6001: '出典：NTSB 勧告書 A-12-08（2012年4月10日）1頁'}


def pages_pick():
    return sorted({pr for pr, _ in PAGE_CUTS.values()})


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def _meta():
    return json.loads((SRC / 'meta.json').read_text(encoding='utf-8'))


def _src_path(m):
    p = SRC / f"{m['title'].rsplit('.', 1)[0]}.jpg"
    if not p.exists():
        raise SystemExit(f"🔴 {p.name} が無い（`ref/ep15/probe/fetch15_img.py use` で取る）")
    return p


def _db():
    return json.loads(DB.read_text(encoding='utf-8')) if DB.exists() else {}


def cmd_build(only=None):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    meta = _meta()
    fx = json.loads((SRC / 'fetched.json').read_text(encoding='utf-8'))
    db = _db()
    for name, r in PICK.items():
        if only and name not in only:
            continue
        m = meta[r['key']]
        sp = _src_path(m)
        # 🔴 取ったファイルが Commons の原本そのものか（SHA-1）を束に入れる前にもう一度
        if hashlib.sha1(sp.read_bytes()).hexdigest() != m['sha1']:
            raise SystemExit(f"🔴 {name}: {sp.name} の SHA-1 が Commons の原本と違う")
        with Image.open(sp) as im0:
            im = im0.convert('RGB')
        w0 = im.width
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        if name in MASK:
            if 'SA' in (r.get('lic') or m['lic']).upper().replace('-', ' ').split():
                raise SystemExit(f'🔴 {name}：BY-SA にモザイクはかけない（翻案＝§5b-52）')
            im = mosaic(im, MASK[name], im.width / w0)
        out = DEST / f'{name}.jpg'
        im.save(out, quality=92)
        db[name] = dict(src='commons', id=m['title'], key=r['key'], slot=r['slot'], cut=r.get('cut', ''),
                        note=r.get('note', ''), box=[0.0, 0.0, 1.0, 1.0], w=im.width, h=im.height, md5=_md5(out),
                        lic=r.get('lic') or m['lic'], frame=bool(r.get('frame')), author=m['artist'],
                        year=r['year'], title=m['title'], hold=f"Wikimedia Commons「{m['title']}」",
                        url=m['page'], sha1=m['sha1'], fetched=fx.get(m['title'], {}).get('fetched', ''))
        if name in MASK:
            db[name]['mosaic'] = [list(b) for b in MASK[name]]
        print(f"✓ {name:18} {im.width}x{im.height}  {db[name]['lic']}"
              f"{f'（顔のモザイク {len(MASK[name])}か所）' if name in MASK else ''}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'→ {DB}（{len(db)}点）')
    return 0


# ── 頁の切り出し（行と行の間で切る）─────────────────────────────
def _rows(page):
    """頁の字の行（同じ高さに並ぶ span をまとめた1行）＝[dict(t=空白なしの字, box=(x0,y0,x1,y1))]（上から）。
    ⚠️ 箱は**回転を直す前**の座標（回転した頁は `_els` で直す）"""
    items = []
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for ln in b['lines']:
            t = re.sub(r'\s+', '', ''.join(s['text'] for s in ln['spans']))
            if t:
                items.append((ln['bbox'], t))
    items.sort(key=lambda it: ((it[0][1] + it[0][3]) / 2, it[0][0]))
    rows = []
    for (x0, y0, x1, y1), t in items:
        cy = (y0 + y1) / 2
        if rows and abs(cy - rows[-1]['cy']) < 3.0:
            r = rows[-1]
            r['parts'].append((x0, t))
            r['box'] = (min(r['box'][0], x0), min(r['box'][1], y0), max(r['box'][2], x1), max(r['box'][3], y1))
        else:
            rows.append(dict(cy=cy, box=(x0, y0, x1, y1), parts=[(x0, t)]))
    for r in rows:
        r['t'] = ''.join(t for _, t in sorted(r['parts']))
    return rows


def _is_folio(t):
    """頁番号・柱（AAB の下の「3」「NTSB/AAB-12/01」・#40 の上の「NTSB No. WPR11MA454 Report No. 12-029」「Page No. 34」・
    #33 の下の「FACTUAL REPORT 8 WPR11MA454」・勧告書の下の番号「8349B」）＝切り出しの中身に入れない行"""
    return bool(re.fullmatch(r'\d{1,3}', t) or t == 'NTSB/AAB-12/01' or t.startswith('NTSBNo.WPR11MA454')
                or re.fullmatch(r'PageNo\.\d+', t) or re.fullmatch(r'FACTUALREPORT\d+WPR11MA454', t)
                or re.fullmatch(r'\d{4}[A-Z]', t))


def _els(page):
    """頁の要素（字の行・画像・線や面）の箱を**画面の向き**（回転を直した座標）で。[(種類, fitz.Rect, 字)]"""
    import fitz
    M = page.rotation_matrix
    out = []
    for r in _rows(page):
        out.append(('row', fitz.Rect(r['box']) * M, r['t']))
    for im in page.get_image_info():
        out.append(('img', fitz.Rect(im['bbox']) * M, ''))
    for d in page.get_drawings():
        out.append(('draw', fitz.Rect(d['rect']) * M, ''))
    return [(k, fitz.Rect(min(r.x0, r.x1), min(r.y0, r.y1), max(r.x0, r.x1), max(r.y0, r.y1)), t) for k, r, t in out]


def box_trim(page, ya, yb, cap=0.025, rot=False):
    """図の頁の切り口：中身（上の端 ya〜下の端 yb）の上下を、**外の要素とのあいだの真ん中**で切る（頁の割合）。
    左右は中身の要素（行・画像）の端＋12pt。rot＝回転した頁（中身＝画像と、画像の外の行のうち柱でないもの）。
    cap＝真ん中が遠いときの余白の上限（頁の割合）。⚠️ 09-30：下に何も無い図（#33 図7・AAB 図15）は真ん中で切ると
    余白が頁の1割を超えた＝既定で 0.025 に抑える"""
    W, H = page.rect.width, page.rect.height          # 画面の向きの大きさ
    els = _els(page)
    if rot:
        body = [e for e in els if e[0] in ('img', 'row') and not (e[0] == 'row' and _is_head(e[2]))]
        y0, y1 = min(e[1].y0 for e in body), max(e[1].y1 for e in body)
    else:
        y0, y1 = ya * H, yb * H
    inside = [e for e in els if e[0] != 'draw' and e[1].y0 >= y0 - 0.5 and e[1].y1 <= y1 + 0.5 and e[1].width > 0
              and not (e[0] == 'row' and _is_folio(e[2]))]
    if not inside:
        raise SystemExit(f'🔴 頁 {page.number + 1}：y {ya}〜{yb} に中身が無い')
    above = [e[1].y1 for e in els if e[1].y1 <= y0 + 0.5]
    below = [e[1].y0 for e in els if e[1].y0 >= y1 - 0.5]
    top = (max(above) + y0) / 2 if above else y0 - 8
    bot = (y1 + min(below)) / 2 if below else y1 + 8
    if cap is not None:
        top, bot = max(top, y0 - cap * H), min(bot, y1 + cap * H)
    x0 = min(e[1].x0 for e in inside) - 12
    x1 = max(e[1].x1 for e in inside) + 12
    box = (max(0.0, x0 / W), max(0.0, top / H), min(1.0, x1 / W), min(1.0, bot / H))
    return [round(v, 4) for v in box], dict(by='box', n_inside=len(inside))


def _is_head(t):
    """#14 の横向きの頁の柱（「WPR11MA454」「Data Recorders Factual Report, page 14」）"""
    return t == 'WPR11MA454' or t.startswith('DataRecordersFactualReport')


def _foot_rule(page):
    """脚注の区切りの短い横線の y（頁の下 45% にある、いちばん上の横線）。無ければ None。"""
    H = page.rect.height
    ys = [d['rect'].y0 for d in page.get_drawings()
          if d['rect'].height < 2 and d['rect'].width > 20 and d['rect'].y0 > 0.55 * H]
    return min(ys) if ys else None


def _paras(rows, rule):
    """行を段落に分ける（[[行の番号…]…]）。前の行の下とこの行の上の空きが、行の高さの中央値の 0.35 倍を超えたら新しい段落。
    脚注の区切り線より下は別の段落（区切り線をまたいでつなげない）"""
    hs = sorted(r['box'][3] - r['box'][1] for r in rows)
    med = hs[len(hs) // 2] if hs else 12
    out = []
    for i, r in enumerate(rows):
        if i and (r['box'][1] - rows[i - 1]['box'][3] <= 0.35 * med
                  and not (rule and rows[i - 1]['box'][3] <= rule <= r['box'][1])):
            out[-1].append(i)
        else:
            out.append([i])
    return out


def text_trim(page, anchor):
    """文字の頁の切り口：目印の語を含む**段落**から始め、額の縦横比に近づくまで上下へ**段落ごと**足した矩形（頁の割合）。
    🔴 2026-09-30（⑤b-6）：14本目の「行ごとに足して行間の真ん中で切る」は、AAB（行間が狭い＝字の箱が触れ合う）では
       寄り（尺の終わりで窓が約1.9%縮む＝上下 約8画素）が端の行に届き、門番 edges が9カットで「下の行が7割しか見えない」と
       鳴った → 切り口は**段落の切れ目**（1行ぶんの空き）の真ん中に置く＝寄りが届かない。脚注は目印が脚注にあるときだけ。
    🔴 境目（空きの真ん中）は**頁番号・柱の行も含めた全部の行**で測る（14本目 09-29：柱を外して測ったら頁番号を半分切った）。"""
    every = _rows(page)
    rows = [r for r in every if not _is_folio(r['t'])]
    joined, owner = '', []
    for i, r in enumerate(rows):
        joined += r['t']
        owner += [i] * len(r['t'])
    k = joined.find(anchor)
    if k < 0 or joined.find(anchor, k + 1) >= 0:
        raise SystemExit(f'🔴 目印「{anchor}」が {"無い" if k < 0 else "2か所ある"}（頁 {page.number + 1}）')
    a0, a1 = owner[k], owner[k + len(anchor) - 1]
    rule = _foot_rule(page)
    paras = _paras(rows, rule)
    pid = {i: n for n, p in enumerate(paras) for i in p}
    foot = lambda n: rule is not None and rows[paras[n][0]]['box'][1] >= rule
    body = [r for r in rows if rule is None or r['box'][1] < rule]
    x0 = min(r['box'][0] for r in (body or rows))
    x1 = max(r['box'][2] for r in (body or rows))
    want = (x1 - x0 + 24) / PANEL_AR_T
    j0, j1 = pid[a0], pid[a1]
    zone = foot(j0)
    top_of = lambda n: rows[paras[n][0]]['box'][1]
    bot_of = lambda n: rows[paras[n][-1]]['box'][3]
    up = True
    for _ in range(len(paras) * 2):
        if bot_of(j1) - top_of(j0) >= want:
            break
        cand = []
        if j0 > 0 and foot(j0 - 1) == zone:
            cand.append(('up', bot_of(j1) - top_of(j0 - 1)))
        if j1 < len(paras) - 1 and foot(j1 + 1) == zone:
            cand.append(('down', bot_of(j1 + 1) - top_of(j0)))
        cand = [c for c in cand if c[1] <= want * 1.3]
        if not cand:
            break
        pick = next((c for c in cand if c[0] == ('up' if up else 'down')), cand[0])
        j0, j1 = (j0 - 1, j1) if pick[0] == 'up' else (j0, j1 + 1)
        up = not up
    y_top, y_bot = top_of(j0), bot_of(j1)
    lines = [d['rect'] for d in page.get_drawings() if d['rect'].height < 2]
    above = [r['box'][3] for r in every if r['box'][3] <= y_top + 0.5] + [ln.y1 for ln in lines if ln.y1 <= y_top]
    below = [r['box'][1] for r in every if r['box'][1] >= y_bot - 0.5] + [ln.y0 for ln in lines if ln.y0 >= y_bot]
    top = (max(above) + y_top) / 2 if above else y_top - 8
    bot = (y_bot + min(below)) / 2 if below else y_bot + 8
    W, H = page.rect.width, page.rect.height
    box = (max(0.0, (x0 - 12) / W), max(0.0, top / H), min(1.0, (x1 + 12) / W), min(1.0, bot / H))
    return [round(v, 4) for v in box], dict(by='anchor', paras=[j0, j1], rows=[paras[j0][0], paras[j1][-1]],
                                            anchor_rows=[a0, a1], ar=round((x1 - x0 + 24) / (y_bot - y_top), 2))


def image_trim(page, idx):
    """その頁の画像（大きい順の idx 番目）の矩形（頁の割合・回転を直した向き）。"""
    import fitz
    infos = sorted(page.get_image_info(), key=lambda i: -(i['bbox'][2] - i['bbox'][0]) * (i['bbox'][3] - i['bbox'][1]))
    if len(infos) <= idx:
        raise SystemExit(f'🔴 頁 {page.number + 1} に画像が {len(infos)} 個しか無い')
    r = fitz.Rect(infos[idx]['bbox']) * page.rotation_matrix
    W, H = page.rect.width, page.rect.height
    return [round(max(0.0, min(r.x0, r.x1) / W), 4), round(max(0.0, min(r.y0, r.y1) / H), 4),
            round(min(1.0, max(r.x0, r.x1) / W), 4), round(min(1.0, max(r.y0, r.y1) / H), 4)], dict(by='img',
                                                                                                    images=len(infos))


def _doc_of(pr):
    return next(d for d in DOCS if pr >= d[0])


def cmd_pages(only=None):
    """`pages` は全頁。`pages 15` のように頁を書けばその頁だけ焼き直す（ほかの頁の md5 を動かさない）。
    courtesy の図（QUOTE_FIGS）は `pg<頁>_fig<NN>.jpg` に切って assets.json に入れる（only を書いたときは焼かない）。"""
    import fitz
    from PIL import Image
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    for pr in pages_pick():
        if only and pr not in only:
            continue
        base, fn, doc, dpi = _doc_of(pr)
        pno = pr - base + 1
        with fitz.open(PDF / fn) as d:
            if pno > d.page_count:
                raise SystemExit(f'🔴 p{pr}＝{doc} の PDF {pno}頁は無い（全{d.page_count}頁）')
            pg = d[pno - 1]
            pix = pg.get_pixmap(dpi=dpi)          # 色のまま（#40 の黄色の塗装＝色が証拠）
            out = DEST / f'pg{pr}.png'
            pix.save(out)
            cuts = {}
            for cid, (p2, how) in PAGE_CUTS.items():
                if p2 != pr:
                    continue
                if how[0] == 'anchor':
                    trim, info = text_trim(pg, how[1])
                elif how[0] == 'img':
                    trim, info = image_trim(pg, how[1])
                else:
                    opt = how[3] if len(how) > 3 else {}
                    trim, info = box_trim(pg, how[1], how[2], cap=opt.get('cap', 0.025), rot=opt.get('rot', False))
                cuts[cid] = trim
                print(f'✓ pg{pr} {cid}  trim={trim}  {info}')
        rec = dict(doc=doc, pdf=fn, pdf_page=pno, w=pix.width, h=pix.height, dpi=dpi, md5=_md5(out), cuts=cuts)
        pj[f'pg{pr}'] = rec
        print(f'  pg{pr}  {doc} PDF {pno}頁  {pix.width}x{pix.height}')
    PAGES_JSON.write_text(json.dumps(pj, ensure_ascii=False, indent=1), encoding='utf-8')
    if only:
        return 0
    # ── courtesy の図＝紙面の引用（図・説明の行・撮影者の行まで）─────────────
    db = _db()
    for k in [k for k, v in db.items() if v.get('src') == 'aab' and k not in QUOTE_FIGS]:
        del db[k]                             # 名前を替えた前の欄（09-30 の pg<頁>_fig<NN>）を台帳から外す
    with fitz.open(PDF / 'AAB1201.pdf') as d:
        for name, (pr, fig, ya, yb, who, cid) in QUOTE_FIGS.items():
            pg = d[pr - 1]
            trim, info = box_trim(pg, ya, yb)
            W, H = pg.rect.width, pg.rect.height
            clip = fitz.Rect(trim[0] * W, trim[1] * H, trim[2] * W, trim[3] * H)
            pix = pg.get_pixmap(dpi=QUOTE_DPI, clip=clip)
            im = Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')
            out = DEST / f'{name}.jpg'
            im.save(out, quality=94)
            # 🔴 撮影者の行（「Photograph courtesy of …」）が切り口の中にあることを字で確かめる（写真だけにしない）
            txt = re.sub(r'\s+', '', pg.get_textbox(clip))
            if f'Photographcourtesyof{who.replace(" ", "")}' not in txt or f'Figure{fig}.' not in txt:
                raise SystemExit(f'🔴 {name}：切り口に「Figure {fig}.」と「Photograph courtesy of {who}」の行が無い')
            db[name] = dict(src='aab', page=pr, fig=fig, trim=trim, slot='quote', cut=cid,
                            note=f'AAB 図{fig}（写真：{who}）＝紙面の引用（図・説明の行・撮影者の行まで）',
                            box=[0.0, 0.0, 1.0, 1.0], w=im.width, h=im.height, md5=_md5(out),
                            lic='引用（NTSB 報告書の紙面に載った courtesy の写真）', frame=True, author=who, year=2011,
                            title=f'NTSB AAB-12/01 Figure {fig}', hold=f'NTSB AAB-12/01（2012年）PDF {pr}頁 図{fig}',
                            url='https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf')
            print(f'✓ {name}  p{pr} 図{fig}  {im.width}x{im.height}  trim={trim}  撮影者の行を確かめた')
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0


def cmd_check():
    if not DB.exists():
        raise SystemExit('🔴 assets.json が無い（build を先に）')
    db = _db()
    bad = 0
    for name in list(PICK) + list(QUOTE_FIGS):
        p = DEST / f'{name}.jpg'
        if name not in db or not p.exists():
            print(f'🔴 {name}: 束に無い'); bad += 1; continue
        if _md5(p) != db[name]['md5']:
            print(f'🔴 {name}: md5 が assets.json と違う（手で差し替えた？）'); bad += 1
    extra = sorted(set(db) - set(PICK) - set(QUOTE_FIGS))
    for e in extra:
        print(f'⚠️ assets.json に PICK に無い名前: {e}')
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    miss = [pr for pr in pages_pick() if f'pg{pr}' not in pj or not (DEST / f'pg{pr}.png').exists()]
    if miss:
        print(f'🔴 焼いていない頁: {miss}'); bad += 1
    for k, v in pj.items():
        if (DEST / f'{k}.png').exists() and _md5(DEST / f'{k}.png') != v['md5']:
            print(f'🔴 {k}: md5 が pages.json と違う'); bad += 1
    have = {cid for v in pj.values() for cid in v.get('cuts', {})}
    if set(PAGE_CUTS) - have:
        print(f'🔴 切り口の無いカット: {sorted(set(PAGE_CUTS) - have)}'); bad += 1
    print('✓ 揃っている' if not bad else f'🔴 {bad}件')
    return 1 if bad else 0


def cmd_panel():
    db = _db()
    for n, r in sorted(db.items(), key=lambda kv: kv[1]['w'] / kv[1]['h']):
        ar = r['w'] / r['h']
        loss = 1 - (ar / (16 / 9) if ar < 16 / 9 else (16 / 9) / ar)
        print(f"AR {ar:.3f}  {n:18} {r['w']}x{r['h']}  全画面で {loss:.1%} 切れる  {r['lic']}"
              f"{'（額装だけ）' if r.get('frame') or 'SA' in r['lic'].upper().replace('-', ' ').split() else ''}")
    return 0


def credit_line(name, r):
    """画面の出典。BY-SA は「（無改変）」まで書く。引用（courtesy の紙面）は図の番号と撮影者と「引用・無改変」。
    CC BY の切り出し・色の断り（改変）は `scene_jiko.credit_of` が足す（「改変」の字が無ければ）。"""
    lic = r['lic']
    who = WHO.get(name) or r['author']
    if r.get('src') == 'aab':
        return f"出典：NTSB 事故報告 AAB-12/01 PDF {r['page']}頁・図{r['fig']}（写真：{who}・引用・無改変）"
    if 'SA' in lic.upper().replace('-', ' ').split():
        return f"出典：{who}／{lic}（無改変）"
    if lic.upper().startswith('CC BY') and r.get('mosaic'):
        # ⚠️ `scene_jiko.credit_of` は「改変」の字があれば足さない＝ここで全部書く（額装・章の色＝色調の変更）
        return f"出典：{who}／{lic}／改変：顔にモザイク・色調変更"
    if lic.upper().startswith('CC BY'):
        return f"出典：{who}／{lic}"
    return f"出典：{who}（パブリックドメイン）"


# 頁の文書の年と「誰が」・権利（台本 §10 の出典一覧・②の台帳 sources.md）
PAGE_DOC = {
    'AAB': (2012, 'NTSB', 'PD（米連邦の職務著作）'),
    '#40': (2012, 'NTSB', 'PD（米連邦の職務著作）'),
    '#33': (2012, 'NTSB', 'PD（米連邦の職務著作・図の下地の空撮は出どころ未記載＝頁ごとの引用）'),
    '#14': (2012, 'NTSB', 'PD（米連邦の職務著作・図の下地は Google Earth＝頁ごとの引用）'),
    '#53': (2012, 'NTSB', 'PD（米連邦の職務著作）'),
    '勧告書': (2012, 'NTSB', 'PD（米連邦の職務著作）'),
}


def page_credit(pr):
    if pr in PAGE_LINE:
        return PAGE_LINE[pr]
    sys.path.insert(0, str(HERE / 'tools'))
    import illu
    line = illu.rec_line([f"{_doc_of(pr)[2]} p{pr}"])
    if not line:
        raise SystemExit(f'🔴 p{pr} の出典の行が作れない（`cuts/ss.REC_DOCS` に資料が無い）')
    return line + (f"・{PAGE_FIG[pr]}" if pr in PAGE_FIG else '')


def cmd_credits(write=False):
    db = _db()
    pages = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    cj = {f'ep15/{n}.jpg': credit_line(n, r) for n, r in db.items()}
    cj.update({f'ep15/{k}.png': page_credit(int(k[2:])) for k in pages})
    rows = [f"| `{n}` | {r.get('cut') or '（章ファイル）'} | {r['year'] or '不明'} | {r['lic']} | "
            f"{WHO.get(n) or r['author']} | {r['hold']}　{r.get('url', '')} |" for n, r in db.items()]
    rows += [f"| `{k}` | {' '.join(sorted(p.get('cuts', {})))} | {PAGE_DOC[p['doc']][0]} | {PAGE_DOC[p['doc']][2]} | "
             f"{PAGE_DOC[p['doc']][1]} | {p['pdf']} PDF {p['pdf_page']}頁 |" for k, p in sorted(
                 pages.items(), key=lambda kv: int(kv[0][2:]))]
    for k, v in list(cj.items()):
        print(k, '|', v)
    print(f'… 写真と紙面の引用 {len(db)}点・頁 {len(pages)}枚')
    if write:
        CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding='utf-8')
        md = CREDITS_MD.read_text(encoding='utf-8')
        # 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②）
        head = '## リノ・エアレース墜落事故（2011-09-16・15本目）'
        hdr = '| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |'
        block = '\n'.join([
            head, '',
            '※2026-09-30（⑤b-6）。`qa_out/ep15_assets.py credits --write` が書く（手で直さない）。',
            '',
            '### 1. 写真（Wikimedia Commons ＝ CC BY-SA は**額装・無改変・1点1カット**／CC BY）・報告書の courtesy の写真（紙面の引用）・報告書と資料の頁',
            'BY-SA の表示＝撮影者・許諾名と URL・素材の URL・無改変（許諾の URL は概要欄で）。', '',
            '- 🔴 **報告書の courtesy の写真（図5〜10・15・17）＝紙面の引用**（ルール §2-6c・09-25 カズヤくん）：写真だけを切り出さず、'
            '**図・説明の行・撮影者の行まで**を紙面のまま（`pg<頁>_fig<NN>`）。額装・寄り0・色を変えない・1点1カット。'
            '画面の出典＝撮影者名と NTSB（「引用・無改変」）',
            '- 🔴 **tataquax（日本の観客＝私人）の撮影時刻は EXIF が日本時間のまま＝現地は −16時間**（推定・materials.md §3-0）。'
            '副題は「事故のレースの離陸／周回中」まで（「事故の◯秒前」と書かない）。撮影者名は Flickr の名前だけ',
            '- 🔴 観客・整備の人は私人＝顔と名前は出さない。CC BY の2010年の2点（`gg_nose_2010`・`gg_pit_2010`）は**顔だけモザイク**'
            '（09-30 カズヤくん「顔面のみのモザイク加工」＝元画像を直す・`cuts/ss.py` の `NEEDS_MASK`・`masked.json` に md5）。'
            'BY-SA はモザイク自体が翻案＝かけない（近景の私人の顔が写る点は使わない・中景の小さな人は §B2-2 のとおり使う）',
            '- 来歴の3点（Bill Larkins）の撮影年は題名の「69」「70」（Commons の日付 2011 は取り込みの年）',
            '- 動く映像は使わない（【映像あり】なし＝09-25 カズヤくん）。Googleアースは使わない（09-30 カズヤくん＝地図に替えた）',
            '', hdr, '|---|---|---|---|---|---|', *rows, ''])
        if head in md:
            pre, rest = md.split(head, 1)
            nxt = rest.find('\n## ')
            md = pre + block + (rest[nxt:] if nxt >= 0 else '')
        else:
            md = md.rstrip('\n') + '\n\n' + block
        CREDITS_MD.write_text(md, encoding='utf-8')
        print(f'→ {CREDITS_JSON} ／ {CREDITS_MD}')
    return 0


def main():
    a = sys.argv[1:] or ['check']
    cmd = a[0]
    if cmd == 'build':
        return cmd_build(set(a[1:]) or None)
    if cmd == 'pages':
        return cmd_pages({int(x) for x in a[1:]} or None)
    if cmd == 'check':
        return cmd_check()
    if cmd == 'panel':
        return cmd_panel()
    if cmd == 'credits':
        return cmd_credits('--write' in a)
    raise SystemExit(f'知らない命令: {cmd}')


if __name__ == '__main__':
    sys.exit(main())
