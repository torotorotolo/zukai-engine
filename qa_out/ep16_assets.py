# -*- coding: utf-8 -*-
"""ep16_assets.py — 16本目（バイオントダム災害）の**写真の束**・**議会の報告書の頁**を作る（2026-10-02 ⑤b-7 新設）。

`qa_out/ep15_assets.py`（15本目）の形を写した。写真は ⑤b-7 で Commons から取った48点のうち当てる46点＋⑤b-1 に取った
地形図 #100（`ref/ep16/probe/fetch16_img.py`・カズヤくん許可 10-02・控え＝`ref/ep16/img/meta.json`・`fetched.json`＝SHA-1 照合ずみ）。
ここでやるのは「名前を付ける・幅3000px に縮める・権利を表にする・頁を焼く・切り口を決める」だけ。動く映像は無い（【映像あり】なし）。

■ 素材（②の台帳 `ref/ep16/photos_commons.tsv` の番号 → 名前 → 当てるカット＝章ファイルの PLAN）
  事故の直後（1963年10月）＝イタリア消防・米陸軍・撮影者不明の PD／事故の前（1955〜63年）＝絵はがきと記録の PD・BY-SA 2点／
  現在（2003〜2023年）＝CC BY 5点・PD 3点。**BY-SA の2点は額装・無改変・1点1カット**（`cuts/ss.py` の `frame_only()`）
■ 🔴 PLAN から替えた点（⑤b-7・原寸で見て決めた＝映像方針 §17）
  ・c208：#075（1958年の管の橋＝ダムが写っていない）→ **#080（1960年・下流から見た工事中のダム・BY-SA）**
  ・c714：#029（道のトンネル＝イタリア消防の1963年10月の記録＝**事故のあと**）→ **#082（事故の前の絵はがき・左岸の道）**
    ＝語りは「20時」＝事故の前（記憶 feedback-fallback-stills-must-match-the-era）
  ・c206 は #073 のまま（1956年の峡谷の橋の工事＝副題は「橋の工事」まで・ダムとは書かない）
  ・使わない（取ったが当てない）：#029（事故のあと）・#074（作業員の顔＝BY-SA はモザイク不可）・#075（橋だけ）
■ 頁（`ss.page(N)`＝台本の頁番号＝S1 の PDF の頁）。議会の報告書は**2段組みのスキャン＋OCR の文字の層**
  ＝目印の語は文字の層で探し（段ごと・行末のハイフンをつなぐ）、**切る線は同じ段の画像の行（インクの帯）の空きの真ん中**
  （文字の層の行と画像の行の差＝中央 0.4〜1.0‰・最大 7.3‰＝⑤b-7 に p171・p207・p225・p226 で測った）。表紙 p1 は文字の層が
  化けている＝画像の行だけで切る

    python qa_out/ep16_assets.py build     # ref/ep16/<名>.jpg ＋ assets.json
    python qa_out/ep16_assets.py pages     # ref/ep16/pg<頁>.png ＋ pages.json（cuts つき）
    python qa_out/ep16_assets.py check     # PICK・assets.json・ファイルが揃っているか
    python qa_out/ep16_assets.py panel     # 縦横比の並び（`cuts/ss.py` の PANEL_AR を決める材料）
    python qa_out/ep16_assets.py credits [--write]   # credits.json と ref/CREDITS.md の表
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

SRC = HERE / 'ref' / 'ep16' / 'img'
PDF = HERE / 'ref' / 'ep16' / 'src'
DEST = HERE / 'ref' / 'ep16'
DB = DEST / 'assets.json'
PAGES_JSON = DEST / 'pages.json'
CREDITS_JSON = DEST / 'credits.json'
CREDITS_MD = HERE / 'ref' / 'CREDITS.md'
MAXW = 3000
# 手元にある原本（Commons から取り直さない＝SHA-1 を照らすだけ）
LOCAL = {'#100': PDF / 'igm1934.jpg'}


def _ledger():
    """②の台帳 `photos_commons.tsv`（1点1行の正本）＝{番号: 行}。PD の根拠（ground）は**ここから引く**（手で写さない）"""
    import csv
    with open(DEST / 'photos_commons.tsv', encoding='utf-8') as f:
        return {r['id']: r for r in csv.DictReader(f, delimiter='\t')}


LEDGER = _ledger()


def C(key, cuts, year, ground=None, **kw):
    """Commons の1点。key＝台帳の番号（`photos_commons.tsv`・`meta.json` の鍵）。cuts＝当てるカット（PLAN）。
    year＝撮影年（分からない・割れるなら None＝副題に年を書かない＝門番 credits）。
    ground＝PD の根拠＝**台帳の値**（引数は照合用。台帳と違えば止める＝⑤b-7 に #079 を手で D' と書き違えた）"""
    g = LEDGER[key]['ground']
    if ground is not None and ground != g:
        raise SystemExit(f"🔴 {key}：根拠を {ground} と書いたが台帳は {g}")
    return dict(src='commons', key=key, cuts=cuts.split(), year=year, ground=g, **kw)


# 名前 → 素材。**BY-SA は1点1カット**（`ss.check_frame_only` が止める）
PICK = {
    # ── 冒頭と第1章 ─────────────────────────────────────────
    'dam_us_1963': C('#002', 'c103 c820', 1963, 'A', note='事故のあとも立つダム（下流の峡谷から・谷底にがれき・管）'),
    'toc_now': C('#120', 'c105 cb05', 2016, 'BY', note='トック山の崩れた跡（いま・2016年8月）・手前に送電線'),
    'dam_houses_now': C('#119', 'c107 cb02', 2005, 'B', note='ロンガローネの家並みの上に見えるダム（2005年8月18日＝題名）'),
    'dam_gorge_now': C('#118', 'c111 ca27 cb03', 2003, 'BY', note='ロンガローネから峡谷ごしに見るダム（2003年4月）'),
    'longarone_before': C('#091', 'c117', None, "D", note='建設前のロンガローネと峡谷の出口（絵はがき・1959年より前）'),
    # ── 第2章 谷とダム（事故の前）───────────────────────────────
    'gorge_1956': C('#087', 'c201', 1956, "D'", note='1956年の峡谷と橋と道'),
    'igm_1934': C('#100', 'c202', 1934, 'E', note='イタリア軍地理院 1934年の地形図（谷・峡谷・ロンガローネ）'),
    'gorge_1955': C('#033', 'c203', 1955, "D", note='1955年の峡谷・アーチの橋・上の小屋（『Il grande Vajont』2012 所収）'),
    'bridge_works_1956': C('#073', 'c206', 1956, 'BY-SA',
                           note='1956年 峡谷にかかるアーチの橋の工事（題名「Ponte SACAIM」・透かし入り）＝ダムは写っていない'),
    'dam_works_1960': C('#080', 'c208', 1960, 'BY-SA', note='1960年 下流から見た工事中のダム（ケーブルの箱・透かし入り）'),
    'crest_cabin': C('#078', 'c212 c519 c622 c704 c709', None, "D",
                     note='天端と操作の建物（1963年より前）・天端の右に人影（動いてぼけている・顔は見えない）'),
    'crest_lake_1960': C('#089', 'c213 c317 c423 c610 c623', 1960, "D'",
                         note='天端の道と湖・左岸の建物（1960年）・天端の人と荷車（背丈 約25px・顔は見えない）'),
    'postcard_280_1961': C('#076', 'c214', 1961, "D'", note='1961年の絵はがき「Diga Del Vajont (altezza m. 280)」＝刷られた「280」'),
    'erto_1960': C('#079', 'c215 c420 c702', 1960, note='絵はがき「Erto m. 775 - Lago del Vaiont」＝湖とエルト村'),
    'color_postcard': C('#082', 'c216 c521 c605 c714', None, "D",
                        note='カラーの絵はがき：左岸の道とトンネルの口・赤い車・ダム・奥にトックの斜面（事故の前）'),
    'crest_full_lake': C('#084', 'c219 c520 c615', None, "D",
                         note='天端と満水に近い湖・トックの斜面（撮影年が割れる＝#088 の1960年の絵はがきと同じ写真）'),
    'aerial_1960': C('#090', 'c220', 1960, "D'", note='1960年の空撮：湖とダム・雪の山'),
    # ── 第3〜5章 1960年の崩落・模型 ─────────────────────────────
    'crack_1960': C('#050', 'c307', 1960, "D'", note='1960年秋 草地を横切る長い亀裂と遠くの人（背丈 約20px）'),
    'slide_19601104': C('#083', 'c309 c323 c415 c501', 1960, "D'",
                        note='1960年11月4日の崩落：ダムの上から見た湖と右（南の岸）の崩れた跡・雪'),
    'slide_1960_small': C('#051', 'c321', 1960, "D'", note='1960年の崩落の跡（360px・ぼやける）'),
    'model_nove': C('#109', 'c503 c505 c506', None, "D'",
                    note='ノーヴェの水理模型（1961〜63年・出どころ＝Augusto Ghetti）・模型の上の4人は背中か上から（顔は見えない）'),
    # ── 第7章・第10章 法廷 ──────────────────────────────────────
    'trial_1968': C('#108', 'c719 ca01 ca12', 1968, "D'",
                    note='1968年11月 ラクイラの法廷（一審）。🔴 座っている人の横顔8人＝顔だけモザイク（MASK）・奥の判事席・憲兵はそのまま'),
    # ── 第8章 22時39分 ─────────────────────────────────────────
    'dam_slide_1963': C('#023', 'c804 cb18', 1963, 'A', note='ダムとその奥で谷を埋めた崩れた山・残った湖（米陸軍）'),
    'aerial_slide_1963': C('#007', 'c818', 1963, "D'", note='上空から：峡谷のダム・谷を埋めた崩れた山・残った湖'),
    'dam_from_debris_1963': C('#021', 'c821', 1963, "D'", note='崩れた土砂の上からダムを見る・残った水'),
    'gorge_exit_1963': C('#031', 'c822', 1963, "D",
                         note='峡谷の出口と水たまり・倒れた電柱・水辺の2人（背丈 約25px）・切れ目の奥にダムの天端'),
    # ── 第9章 夜が明けて（1963年10月）───────────────────────────────
    'longarone_before_after': C('#019', 'c901', 1963, "A+D'", note='同じ構図の前後（左1960年・右1963年・米陸軍）＝合成'),
    'rubble_tower_1963': C('#028', 'c902', 1963, "D",
                           note='がれきの原・ピラーゴの鐘楼・奥に峡谷の出口・作業する兵士（背丈 10〜20px）＝遺体は写っていない（原寸）'),
    'longarone_above_1963': C('#018', 'c903', 1963, 'A', note='上から見たロンガローネ一帯（削られた地面と残った家並み）'),
    'pirago_tower_1963': C('#001', 'c904', 1963, "D'", note='ピラーゴの鐘楼とがれき（人なし）'),
    'rail_bridge_1963': C('#004', 'c905', 1963, "D", note='空撮：鉄道の石のアーチ橋と道路・奥に削られた平地'),
    'piave_valley_1963': C('#006', 'c909', 1963, "D", note='ピアーヴェ川の谷の広い眺め・遠くに町（左端にスキャンの黒い影）'),
    'temp_bridge_1963': C('#013', 'c911', 1963, "D", note='仮の橋を架ける兵士たち（公的な任務）'),
    'army_trucks_1963': C('#025', 'c912', 1963, "D", note='軍のトラックの列と整列した兵士'),
    'tent_camp_1963': C('#024', 'c913', 1963, "D", note='テントの村とトラック'),
    'tents_above_1963': C('#003', 'c914', 1963, "D", note='上から：削られた地面・軍のテント・道路'),
    'bulldozer_1963': C('#027', 'c915', 1963, "D", note='兵士の運転するブルドーザーと流木（後ろ姿）'),
    'valley_above_1963': C('#032', 'c916', 1963, 'A', note='上から：削られたピアーヴェの谷と残った家並み'),
    'ruined_house_1963': C('#009', 'c917', 1963, "D", note='壊れた建物とがれき・遠くに小さな人影'),
    'pirago_tower2_1963': C('#020', 'c920', 1963, "D'", note='ピラーゴの鐘楼（別の向き）・根こそぎの木'),
    # ── 第10・11章 いま ────────────────────────────────────────
    'dam_now_downstream': C('#116', 'ca03 cb04', 2008, 'B', note='下流の峡谷から見たダム（2008年2月）'),
    'dam_now_below': C('#117', 'ca07 cb17', 2003, 'BY', note='真下から見たダム（2003年4月・縦）・手前にねじれた鉄筋'),
    'lake_now': C('#122', 'ca23 cb07', 2015, 'BY', note='残った湖と崩れた山（2015年5月）'),
    'slide_surface_now': C('#121', 'ca24 cb06', 2005, 'BY', note='トック山のすべり面の近景（2005年7月）'),
    'sign_2023': C('#115', 'cb09', 2023, 'A', note='「Viale Soccorritori del Vajont」の標識（米陸軍 2023年10月8日）'),
    'memorial_cross_1963': C('#014', 'cb10', 1963, "D", note='慰霊の大きな木の十字架と花輪（318px）'),
}
UNUSED = {'#029': '道のトンネル＝イタリア消防の1963年10月の記録＝事故のあと（c714 の語りは事故の前の20時）',
          '#074': '1957年のケーブルクレーンの小屋と作業員（顔＝BY-SA はモザイク不可）',
          '#075': '1958年の管の橋だけ（ダムが写っていない＝c208 は #080）'}

# 🔴 顔だけモザイク（ルール §B2-2b・2026-09-30 カズヤくん「顔面のみのモザイク加工」）。**PD・CC BY の点だけ**。
#    範囲＝原寸の画素 (x0, y0, x1, y1, 誰)。⑤b-7 に**4倍の拡大と10px の目盛り**で読んだ（scratchpad `zoom16.py`）。
#    #108＝座っている人の横顔（誰が私人か写真では決められない＝全員）。奥の判事席の3人（顔 約12〜15px＝法廷の公務）と
#    憲兵（背中）はかけない。元画像そのものを直す＝`cuts/ss.py` の NEEDS_MASK・`masked.json`（check_photo_mask --record）
MOSAIC_PX = {'trial_1968': 6}      # 升の大きさ（原寸の画素）。顔の幅 25〜45px ＝ 4〜7升＝見分けられない
MASK = {
    'trial_1968': [(0, 200, 34, 250, '左端の横顔の人'),
                   (8, 175, 42, 210, '左奥の人'),
                   (46, 176, 78, 226, '白髪の人'),
                   (70, 175, 100, 210, 'うつむく白髪の人'),
                   (98, 182, 130, 226, '右を向く横顔の人'),
                   (128, 207, 170, 256, '明るい髪の人'),
                   (156, 188, 194, 236, '白い襟の人'),
                   (196, 183, 240, 234, '右の横顔の人')],
}


def mosaic(im, boxes, n0, scale=1.0):
    """顔の範囲だけを升目にする（縮めて NEAREST で戻す）。scale＝原寸からの縮尺（束は幅3000px まで）。"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        b = tuple(round(v * scale) for v in (x0, y0, x1, y1))
        reg = im.crop(b)
        n = max(1, round(n0 * scale))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), b[:2])
    return im


# 画面の出典の「誰が」。PD の根拠（台帳の記号）は ref/CREDITS.md の権利の欄に書く（画面は短く）
WHO = {
    'dam_us_1963': 'U.S. Army', 'dam_slide_1963': 'U.S. Army', 'longarone_above_1963': 'U.S. Army',
    'valley_above_1963': 'U.S. Army', 'longarone_before_after': '撮影者不明・U.S. Army',
    'sign_2023': 'U.S. Army・Sgt. Bobbi-Jo McGinley',
    'gorge_1955': 'M. Reberschak 編『Il grande Vajont』',
    'igm_1934': 'イタリア軍地理院 IGM',
    'bridge_works_1956': 'Enel・Archivio Enel', 'dam_works_1960': 'Torno S.p.A.・Archivio Torno',
    'dam_now_downstream': 'Riccardo Sartor', 'dam_houses_now': 'Emanuele Paolini',
    'dam_gorge_now': 'Stefano Petri', 'dam_now_below': 'Stefano Petri', 'toc_now': 'Davide Cavalli',
    'slide_surface_now': 'Christian Thiergan', 'lake_now': 'Gianmarco139',
}

def who_of(name, artist):
    """画面の「誰が」。上の表に無い点は **Commons の撮影者の欄から**決める（台帳の根拠の記号からは決めない＝
    根拠 D でも撮影者不明の絵はがきがある）：Vigili del Fuoco＝イタリア消防／US Army＝U.S. Army／それ以外＝撮影者不明
    （#050 の「Leopold Muller (?)」も不明＝c307 の語り「撮った人ははっきりしていない」・#078 の VENET01 はスキャンした人）"""
    if name in WHO:
        return WHO[name]
    a = artist.lower()
    if 'vigili del fuoco' in a:
        return 'イタリア消防'
    if 'us army' in a or 'u.s. army' in a:
        return 'U.S. Army'
    return '撮影者不明'
GROUND = {
    'A': 'PD（米連邦の職務著作 17 U.S.C. §105）',
    "A+D'": 'PD（米連邦 §105＋伊の単純写真＝撮影から20年）',
    'B': 'PD（撮影者本人の宣言）',
    'D': 'PD（伊の単純写真＝撮影から20年・米国も PD-1996）',
    "D'": 'PD（伊の単純写真＝撮影から20年）',
    'E': 'PD（1934年の地形図＝PD-old）',
}

# ══════════════════════════════════════════════════════════
#  頁（台本の頁番号＝S1 の PDF の頁 p1〜p248）
# ══════════════════════════════════════════════════════════
DOCS = ((1, 'senato_doc76bis_285307.pdf', 'S1', 200),)
PANEL_AR_T = 1120 / 648      # 額の最大の箱（`scene_jiko.PANEL_MAXW × PANEL_MAXH`）の縦横比＝文字の頁の切り出しの目標
COLS = ((0.08, 0.50), (0.50, 0.92))   # 2段組み（左の段・右の段）の範囲（頁の幅の割合）
RULE_FRAC = 0.60             # 縦の罫線とみなす列（窓の高さのこの割合以上にインク）＝字の列は4割台まで
SHRINK = 0.0095              # 額装の頁の寄りが尺の終わりに縮める窓（片側・切り口の高さの割合）＝(1−1/1.01925)/2 ＋丸め
END_PAD = 0.012              # 頁の最初・最後の行の外の余白（頁の高さの割合）
# 切り口（カット → (頁, 切り方)）：
#   ('col', 目印)      … 文字の頁：目印（空白なし・小文字・行末のハイフンをつないだ原文）を含む段の行を真ん中に、額の縦横比に
#                        なるまで同じ段の行を上下に足す。切る線は画像の行の空きの真ん中
#   ('imgbox', 上, 下) … 文字の層が使えない頁（表紙）：頁の割合の上下の範囲に入る画像の行をまとめ、空きの真ん中で切る
# ⚠️ 目印は ⑤b-7（10-02）に `scratchpad/probe_pages16.py` で文字の層を引いて決めた（台本 §G の照合表の原文）
PAGE_CUTS = {
    'c112': (1, ('imgbox', 0.665, 0.920)),          # 表紙の下＝RELAZIONE FINALE・1965年7月15日・ALLEGATI（少数派の報告2本）
    'c412': (217, ('col', 'mediantemisureartificiali')),   # 少数派の報告がミュラーの報告を引く段（人工的な手段で止められるか）
    'c416': (179, ('col', 'conosciutiallapub')),            # 多数派「ミュラーの報告と模型の実験は行政に知られていた」
    'c516': (225, ('col', 'questiulterioriaccertamenti')),  # 少数派「これらの追加の調べは行われなかった」
    'c606': (226, ('col', 'deliberatoproposito')),          # 少数派「15メートル越える、はっきりした意図」（p166 は出さない＝§17）
    'c819': (171, ('col', 'qualeresistette')),              # 多数派「ダムも助かった…3,000万立方メートルの水の圧力に耐えた」
    'c910': (207, ('col', 'cinquecentobambini')),           # 少数派「2,000人の市民、うち子ども500人」
    'ca06': (178, ('col', 'peggiorecombinazione')),         # 多数派「最悪の組み合わせでも危険を否定」
    'ca08': (207, ('col', 'equindievitabile')),             # 少数派「予見でき、起こる見込みも高く、だから避けられた」
}
PAGE_DPI = 200


def pages_pick():
    return sorted({pr for pr, _ in PAGE_CUTS.values()})


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def _meta():
    return json.loads((SRC / 'meta.json').read_text(encoding='utf-8'))


def _src_path(key, m):
    if key in LOCAL:
        return LOCAL[key]
    p = SRC / f"{m['title'].rsplit('.', 1)[0]}.jpg"
    if not p.exists():
        raise SystemExit(f"🔴 {p.name} が無い（`ref/ep16/probe/fetch16_img.py use` で取る）")
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
        sp = _src_path(r['key'], m)
        # 🔴 取ったファイルが Commons の原本そのものか（SHA-1）を束に入れる前にもう一度
        if hashlib.sha1(sp.read_bytes()).hexdigest() != m['sha1']:
            raise SystemExit(f"🔴 {name}: {sp.name} の SHA-1 が Commons の原本と違う")
        with Image.open(sp) as im0:
            im = im0.convert('RGB')
        w0 = im.width
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        lic = m['lic']
        if name in MASK:
            if 'SA' in lic.upper().replace('-', ' ').split():
                raise SystemExit(f'🔴 {name}：BY-SA にモザイクはかけない（翻案＝§5b-52）')
            im = mosaic(im, MASK[name], MOSAIC_PX[name], im.width / w0)
        out = DEST / f'{name}.jpg'
        im.save(out, quality=92)
        db[name] = dict(src='commons', id=m['title'], key=r['key'], slot=r['ground'], cut=' '.join(r['cuts']),
                        note=r.get('note', ''), box=[0.0, 0.0, 1.0, 1.0], w=im.width, h=im.height, md5=_md5(out),
                        lic=lic, frame=False, author=m['artist'], ground=r['ground'],
                        year=r['year'], title=m['title'], hold=f"Wikimedia Commons「{m['title']}」",
                        url=m['page'], sha1=m['sha1'],
                        fetched=('2026-10-01（⑤b-1）' if r['key'] in LOCAL
                                 else fx.get(m['title'], {}).get('fetched', '')))
        if name in MASK:
            db[name]['mosaic'] = [list(b) for b in MASK[name]]
        print(f"✓ {name:24} {im.width}x{im.height}  {lic}"
              f"{f'（顔のモザイク {len(MASK[name])}か所）' if name in MASK else ''}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'→ {DB}（{len(db)}点）')
    return 0


# ── 頁の切り出し（2段組みのスキャン＝画像の行の空きで切る）─────────────────────
def _gray(page, dpi):
    import fitz
    import numpy as np
    pix = page.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
    return np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)


def _bands(a, c0, c1):
    """画像の段（頁の幅の割合 c0〜c1）の字の帯＝[(上, 下)]（頁の高さの割合）。インクの横の投影で、帯は高さ4画素以上"""
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
    # ⚠️ 帯を「インクが1画素でもある行」まで広げてはいけない（⑤b-7 に試した＝スキャンの薄い汚れが行間を埋め、帯どうしが
    #    くっついて切る線が次の行の中に入った）。薄い部分は門番と同じ OCR の行の箱で補う（`_occupied`）
    return [(s[0] / H, s[1] / H) for s in spans]


def _ocr_rows(key, c0, c1):
    """門番 edges が使う OCR の読み置き（`check_slide.py --ocr`＝ref/ep16/ocr_slides.json）の、段 c0〜c1 の行の箱（頁の高さの割合）。
    読み置きが無ければ []（初回・頁を足した直後）＝インクの帯だけで切る→ OCR を取ってから `pages` をもう一度"""
    p = DEST / 'ocr_slides.json'
    if not p.exists():
        return []
    v = json.loads(p.read_text(encoding='utf-8')).get(f'{key}.png')
    if not v:
        return []
    W, H = v['size']
    return [(ln['box'][1] / H, ln['box'][3] / H) for ln in v['lines']
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
    """画像の y0〜y1（頁の高さの割合）・段 c0〜c1（頁の幅の割合）の中で、インクのある左端と右端（頁の幅の割合）。
    縦の列のインクが帯の高さの 2% を超える列だけ数える（汚れの点を拾わない）"""
    import numpy as np
    H, Wp = a.shape
    sub = a[int(y0 * H):int(y1 * H), int(c0 * Wp):int(c1 * Wp)]
    cnt = (sub < 140).sum(axis=0)
    # 🔴 ⑤b-7：段のあいだの**縦の罫線**（帯の高さの 60% 以上にインクがある列）は字ではない＝数えない
    #    （数えると左の段の切り口の右端に罫線が入り、額の縁に見えた＝c412・c416・c910）。罫線は所々で途切れる
    #    ＝85% では拾えなかった。字の列は縦に4割台まで（左端の縦画がそろう列でも）＝6割で分かれる
    cols = np.where((cnt > max(1, 0.02 * sub.shape[0])) & (cnt < RULE_FRAC * sub.shape[0]))[0]
    if not len(cols):
        raise SystemExit('🔴 段の中にインクが無い')
    return (int(cols[0]) + int(c0 * Wp)) / Wp, (int(cols[-1]) + int(c0 * Wp)) / Wp


def _rules_x(a, y0, y1, c0, c1):
    """縦の罫線の位置（頁の幅の割合）＝帯の高さの RULE_FRAC 以上にインクがある列"""
    import numpy as np
    H, Wp = a.shape
    sub = a[int(y0 * H):int(y1 * H), int(c0 * Wp):int(c1 * Wp)]
    cnt = (sub < 140).sum(axis=0)
    return [(int(x) + int(c0 * Wp)) / Wp for x in np.where(cnt >= RULE_FRAC * sub.shape[0])[0]]


def _body(bands):
    """柱（頁の上の「Atti Parlamentari — N — Senato della Repubblica」と「LEGISLATURA IV …」）を外した本文の帯。
    上の 15% の中でいちばん大きな空きより上を柱とみなす"""
    top = [i for i in range(len(bands) - 1) if bands[i + 1][0] < 0.15]
    if not top:
        return bands
    k = max(top, key=lambda i: bands[i + 1][0] - bands[i][1])
    return bands[k + 1:]


def _col_rows(page, ci):
    """文字の層の行（その段だけ）＝[dict(t=空白なし・小文字・行末のハイフンを外した字, box)]（上から）"""
    W = page.rect.width
    c0, c1 = COLS[ci]
    rows = []
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for ln in b['lines']:
            x0, y0, x1, y1 = ln['bbox']
            if not c0 <= (x0 + x1) / 2 / W < c1:
                continue
            t = re.sub(r'\s+', '', ''.join(s['text'] for s in ln['spans'])).lower()
            if t:
                rows.append(dict(t=t[:-1] if t.endswith('-') else t, box=(x0, y0, x1, y1)))
    rows.sort(key=lambda r: (r['box'][1] + r['box'][3]) / 2)
    return rows


def _cut_lines(occ, j0, j1, lo, hi, px):
    """字のある範囲 j0〜j1 の上下を切る（頁の高さの割合）。lo・hi＝使える範囲の端。px＝1画素（頁の高さの割合）。
    🔴 2026-10-02（⑤b-7）：門番 edges（＝本番の寄り）に合わせて決める。額装の頁は尺の終わりに窓が高さの 1.89% 縮む
       （`build_jiko.fit`：1＋0.055×0.35）＝上下に 0.94% ずつ。→ 内側の行にその分＋1px を残し、外側の行は最初から写さない
       （門番の「見えている 8〜92%」の外）。空きが足りなければ1行ずつ足す（最大3行）＝それでも足りなければいちばん広い空きで。
       ⚠️ 空きの真ん中で切ったら3カット（c112・c412・ca08）で端の行が9割しか見えなかった（行間 2〜8px＜縮み＋余白）"""
    def need(a, b):
        return SHRINK * (occ[b][1] - occ[a][0]) + px

    def ok_top(a, b):
        return a == 0 or occ[a][0] - occ[a - 1][1] >= need(a, b) + px

    def ok_bot(a, b):
        return b == len(occ) - 1 or occ[b + 1][0] - occ[b][1] >= need(a, b) + px

    for _ in range(3):
        if not ok_top(j0, j1) and j0 > lo:
            j0 -= 1
            continue
        if not ok_bot(j0, j1) and j1 < hi:
            j1 += 1
            continue
        break
    m = need(j0, j1)
    top = (max(occ[j0 - 1][1] + px, occ[j0][0] - m - px) if j0 > 0 else occ[j0][0] - END_PAD)
    bot = (min(occ[j1 + 1][0] - px, occ[j1][1] + m + px) if j1 < len(occ) - 1 else occ[j1][1] + END_PAD)
    return j0, j1, top, bot


def col_trim(page, anchor):
    """文字の頁の切り口（2段組み）：目印を含む段の行を真ん中に、額の縦横比になるまで同じ段の行を上下に足す（頁の割合）。"""
    hits = []
    for ci in (0, 1):
        rows = _col_rows(page, ci)
        joined, owner = '', []
        for i, r in enumerate(rows):
            joined += r['t']
            owner += [i] * len(r['t'])
        k = joined.find(anchor)
        while k >= 0:
            hits.append((ci, rows, owner[k], owner[k + len(anchor) - 1]))
            k = joined.find(anchor, k + 1)
    if len(hits) != 1:
        raise SystemExit(f'🔴 目印「{anchor}」が {len(hits)} か所（頁 {page.number + 1}）＝1か所でないと切らない')
    ci, rows, a0, a1 = hits[0]
    W, H = page.rect.width, page.rect.height
    cy = ((rows[a0]['box'][1] + rows[a1]['box'][3]) / 2) / H
    a = _gray(page, PAGE_DPI)
    ink_b = _body(_bands(a, *COLS[ci]))
    if not ink_b:
        raise SystemExit(f'🔴 頁 {page.number + 1}：段 {ci} に字の帯が無い')
    # 字のある範囲＝インクの帯＋門番の OCR の行の箱（柱より下だけ）
    bands = _occupied(ink_b, [r for r in _ocr_rows(f'pg{page.number + 1}', *COLS[ci]) if r[0] >= ink_b[0][0] - 0.004])
    j = min(range(len(bands)), key=lambda i: abs((bands[i][0] + bands[i][1]) / 2 - cy))
    near = abs((bands[j][0] + bands[j][1]) / 2 - cy)
    if near > 0.012:
        raise SystemExit(f'🔴 頁 {page.number + 1}：目印の行（y {cy:.4f}）に近い画像の行が無い（差 {near:.4f}）')
    # 🔴 左右の端は**画像のインク**で、その段の中だけから測る（⑤b-7：文字の層に2段にまたがる行があり、p178 の右の段の
    #    切り口が左端 0.24 まで広がって左の段に食い込んだ）。目印の行の上下 6行ぶんの帯で測る
    ya, yb = bands[max(0, j - 6)][0], bands[min(len(bands) - 1, j + 6)][1]
    x0, x1 = _ink_x(a, ya, yb, *COLS[ci])
    # 余白 10pt は**2つの段のあいだの溝の真ん中**で止める（溝は約 0.017＝余白 10pt と同じ幅＝隣の段の字の頭が入る）
    lr, rl = _ink_x(a, ya, yb, *COLS[0])[1], _ink_x(a, ya, yb, *COLS[1])[0]
    gut = (lr + rl) / 2
    rules = [r for r in _rules_x(a, ya, yb, lr, rl)]       # 2つの段のあいだの罫線
    tl, tr = x0, x1                                          # 字の左端・右端（頁の幅の割合）
    x0, x1 = x0 * W - 10, x1 * W + 10
    if ci == 0:
        x1 = min([x1, gut * W] + [r * W - 2 for r in rules if r > tr])
    else:
        x0 = max([x0, gut * W] + [r * W + 2 for r in rules if r < tl])
    want = (x1 - x0) / PANEL_AR_T / H          # 欲しい高さ（頁の高さの割合）
    j0 = j1 = j
    up = True
    while bands[j1][1] - bands[j0][0] < want:
        if up and j0 > 0:
            j0 -= 1
        elif j1 < len(bands) - 1:
            j1 += 1
        elif j0 > 0:
            j0 -= 1
        else:
            break
        up = not up
    j0, j1, top, bot = _cut_lines(bands, j0, j1, 0, len(bands) - 1, 1 / a.shape[0])
    # 🔴 罫線は**最後の切り口の窓の中で**もう一度探す（罫線は所々で途切れる＝窓が違うと拾い損ねる＝⑤b-7 の ca06・c416・c606）
    #    ⚠️ 上の窓で罫線を「字の端」と数えていることがある（罫線＝字の右端）＝「段の真ん中より外側の罫線」で外す
    fin = _rules_x(a, top, bot, min(lr, rl) - 0.01, max(lr, rl) + 0.01)
    mid = (tl + tr) / 2
    if ci == 0:
        x1 = min([x1] + [r * W - 2 for r in fin if r > mid])
    else:
        x0 = max([x0] + [r * W + 2 for r in fin if r < mid])
    box = (max(0.0, x0 / W), max(0.0, top), min(1.0, x1 / W), min(1.0, bot))
    return [round(float(v), 4) for v in box], dict(by='col', col='左右'[ci], rows=[j0, j1], anchor_row=j,
                                            n_rows=j1 - j0 + 1, ar=round((x1 - x0) / ((bot - top) * H), 2))


def imgbox_trim(page, ya, yb):
    """文字の層の無い・化けた頁（表紙）：頁の割合 ya〜yb に中心がある画像の行をまとめ、空きの真ん中で切る。左右はインクの端＋12pt"""
    import numpy as np
    a = _gray(page, PAGE_DPI)
    bands = _occupied(_bands(a, 0.04, 0.96), _ocr_rows(f'pg{page.number + 1}', 0.04, 0.96))
    idx = [i for i, b in enumerate(bands) if ya <= (b[0] + b[1]) / 2 <= yb]
    if not idx:
        raise SystemExit(f'🔴 頁 {page.number + 1}：y {ya}〜{yb} に字の帯が無い')
    j0, j1, top, bot = _cut_lines(bands, idx[0], idx[-1], 0, len(bands) - 1, 1 / a.shape[0])
    sub = a[int(bands[j0][0] * a.shape[0]):int(bands[j1][1] * a.shape[0]), :]
    cols = np.where((sub < 140).sum(axis=0) > 1)[0]
    W = page.rect.width
    pad = 12 / W
    x0, x1 = cols[0] / a.shape[1] - pad, cols[-1] / a.shape[1] + pad
    box = (max(0.0, x0), max(0.0, top), min(1.0, x1), min(1.0, bot))
    return [round(float(v), 4) for v in box], dict(by='imgbox', rows=[j0, j1], n_rows=j1 - j0 + 1)


def _doc_of(pr):
    return next(d for d in DOCS if pr >= d[0])


def cmd_pages(only=None):
    """`pages` は全頁。`pages 171` のように頁を書けばその頁だけ焼き直す（ほかの頁の md5 を動かさない）。
    頁は灰色（スキャンの白黒＝色の情報が無い）の PNG"""
    import fitz
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
            pix = pg.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
            out = DEST / f'pg{pr}.png'
            pix.save(out)
            cuts = {}
            for cid, (p2, how) in PAGE_CUTS.items():
                if p2 != pr:
                    continue
                trim, info = col_trim(pg, how[1]) if how[0] == 'col' else imgbox_trim(pg, how[1], how[2])
                cuts[cid] = trim
                print(f'✓ pg{pr} {cid}  trim={trim}  {info}')
        pj[f'pg{pr}'] = dict(doc=doc, pdf=fn, pdf_page=pno, w=pix.width, h=pix.height, dpi=dpi, md5=_md5(out),
                             cuts=cuts)
        print(f'  pg{pr}  {doc} PDF {pno}頁  {pix.width}x{pix.height}')
    PAGES_JSON.write_text(json.dumps(pj, ensure_ascii=False, indent=1), encoding='utf-8')
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
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    miss = [pr for pr in pages_pick() if f'pg{pr}' not in pj or not (DEST / f'pg{pr}.png').exists()]
    if miss:
        print(f'🔴 焼いていない頁: {miss}')
        bad += 1
    for k, v in pj.items():
        if (DEST / f'{k}.png').exists() and _md5(DEST / f'{k}.png') != v['md5']:
            print(f'🔴 {k}: md5 が pages.json と違う')
            bad += 1
    have = {cid for v in pj.values() for cid in v.get('cuts', {})}
    if set(PAGE_CUTS) - have:
        print(f'🔴 切り口の無いカット: {sorted(set(PAGE_CUTS) - have)}')
        bad += 1
    print('✓ 揃っている' if not bad else f'🔴 {bad}件')
    return 1 if bad else 0


def cmd_panel():
    db = _db()
    for n, r in sorted(db.items(), key=lambda kv: kv[1]['w'] / kv[1]['h']):
        ar = r['w'] / r['h']
        loss = 1 - (ar / (16 / 9) if ar < 16 / 9 else (16 / 9) / ar)
        print(f"AR {ar:.3f}  {n:24} {r['w']}x{r['h']}  全画面で {loss:.1%} 切れる  {r['lic']}"
              f"{'（額装だけ）' if r.get('frame') or 'SA' in r['lic'].upper().replace('-', ' ').split() else ''}")
    return 0


def credit_line(name, r):
    """画面の出典。BY-SA は「（無改変）」まで書く。モザイクをかけた点は「改変：顔にモザイク」を書く。
    CC BY の切り出し・色の断り（改変）は `scene_jiko.credit_of` が足す（「改変」の字が無ければ）。"""
    lic = r['lic']
    who = who_of(name, r['author'])
    if 'SA' in lic.upper().replace('-', ' ').split():
        return f"出典：{who}／{lic}（無改変）"
    if lic.upper().startswith('CC BY') and r.get('mosaic'):
        return f"出典：{who}／{lic}／改変：顔にモザイク・色調変更"
    if lic.upper().startswith('CC BY'):
        return f"出典：{who}／{lic}"
    if r.get('mosaic'):
        return f"出典：{who}（パブリックドメイン・顔にモザイク）"
    return f"出典：{who}（パブリックドメイン）"


# 頁の文書の年と「誰が」・権利（②の台帳 materials.md §9）
PAGE_DOC = {
    'S1': (1965, 'イタリア議会 ヴァイオント災害調査委員会',
           '保護の外（伊著作権法 第5条＝国の公文書）／Senato della Repubblica の公開版'),
}


def page_credit(pr):
    sys.path.insert(0, str(HERE / 'tools'))
    import illu
    line = illu.rec_line([f"{_doc_of(pr)[2]} p{pr}"])
    if not line:
        raise SystemExit(f'🔴 p{pr} の出典の行が作れない（`cuts/ss.REC_DOCS` に資料が無い）')
    return line


def cmd_credits(write=False):
    db = _db()
    pages = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    cj = {f'ep16/{n}.jpg': credit_line(n, r) for n, r in db.items()}
    cj.update({f'ep16/{k}.png': page_credit(int(k[2:])) for k in pages})
    rows = [f"| `{n}` | {r.get('cut') or '（章ファイル）'} | {r['year'] or '不明'} | "
            f"{r['lic'] if r['lic'] != 'Public domain' else GROUND[r['ground']]} | "
            f"{who_of(n, r['author'])} | {r['hold']}　{r.get('url', '')} |" for n, r in db.items()]
    rows += [f"| `{k}` | {' '.join(sorted(p.get('cuts', {})))} | {PAGE_DOC[p['doc']][0]} | "
             f"{PAGE_DOC[p['doc']][2]} | {PAGE_DOC[p['doc']][1]} | {p['pdf']} PDF {p['pdf_page']}頁 |"
             for k, p in sorted(pages.items(), key=lambda kv: int(kv[0][2:]))]
    for k, v in list(cj.items()):
        print(k, '|', v)
    print(f'… 写真 {len(db)}点・頁 {len(pages)}枚')
    if write:
        CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding='utf-8')
        md = CREDITS_MD.read_text(encoding='utf-8')
        # 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②）
        head = '## バイオントダム災害（1963-10-09・16本目）'
        hdr = '| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |'
        block = '\n'.join([
            head, '',
            '※2026-10-02（⑤b-7）。`qa_out/ep16_assets.py credits --write` が書く（手で直さない）。',
            '',
            '### 1. 写真（Wikimedia Commons ＝ PD・CC BY・CC BY-SA は**額装・無改変・1点1カット**）・地形図・議会の報告書の頁',
            'BY-SA の表示＝撮影者・許諾名と URL・素材の URL・無改変（許諾の URL は概要欄で）。', '',
            '- 🔴 **PD の根拠は点ごとに違う**（記憶 feedback-pd-label-hides-two-different-grounds）＝米連邦 §105（米陸軍）／'
            '撮影者本人の宣言／伊の単純写真（撮影から20年＝1963年の写真は1983年に保護が切れた。米国でも PD-1996 の点がある）／'
            '1934年の地形図（PD-old）。権利の欄に1点ずつ書いた（「PD」と1行にまとめない）',
            '- 🔴 **米陸軍の写真（1963年の4点・2023年の標識）＝⑥の概要欄に「米陸軍の写真の使用は推奨を意味しない」の断り書き**'
            '（ルール §5b-98⑧）',
            '- 🔴 人が写る写真（§B2-2）：1968年の法廷（`trial_1968`）の座っている人の横顔8人は**顔だけモザイク**'
            '（2026-09-30 カズヤくん「顔面のみのモザイク加工」＝PD は手直しを許す＝元画像を直す・`cuts/ss.py` の `NEEDS_MASK`・'
            '`ref/ep16/masked.json`）。奥の判事席・憲兵（法廷の公務）・救援の兵士と消防（公的な任務）はそのまま。'
            'ほかの点の人（がれきの原の兵士・水辺の2人・天端の人影）は原寸で背丈 10〜25px＝顔は見分けられない',
            '- 撮影年が割れる・分からない点（天端と満水の湖＝#084／#088 と同じ写真・操作の建物・カラーの絵はがき・建設前の'
            '絵はがき・水理模型）は撮影年を「不明」にし、**副題に年を書かない**（門番 credits）',
            '- 取ったが当てない点：#029（道のトンネル＝事故のあとの記録）・#074（作業員の顔＝BY-SA）・#075（橋だけ）',
            '- 動く映像は使わない（【映像あり】なし）。Google Earth は使わない（2026-10-02 カズヤくん＝7カットは地図〈VA〉に替えた）',
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
