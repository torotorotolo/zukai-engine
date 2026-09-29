# -*- coding: utf-8 -*-
"""ep14_assets.py — 14本目（セウォル号）の**写真の束**・**判決と報告書の頁**・**動く映像の台帳**を作る（2026-09-29 ⑤b-7a 新設）。

`qa_out/ep13_assets.py`（13本目）の形を写した。写真は ⑤b-7a で Commons から取った23点
（`ref/ep14/probe/fetch14_img.py`・カズヤくん許可 09-29・控え＝`ref/ep14/img/meta.json`・`fetched.json`＝SHA-1 照合ずみ）。
ここでやるのは「名前を付ける・幅3000px に縮める・権利を表にする・頁を焼く・映像の台帳とひかえの静止画」だけ。

■ 素材（②の台帳 `ref/ep14/materials.md` §3 の記号・番号 → 名前 → 当てるカット＝章ファイルの PLAN）
  捜索（韓国国防部・CC BY-SA 2.0）11点＝**額装・無改変・1点1カット**（`cuts/ss.py` の `frame_only()` が権利から読む）
  船 3点（K1 仁川港 PD・J1 鹿児島港 BY-SA・M1 木浦 BY-SA）／当日 H1（**引用**＝額装・無改変＝`frame=True`）
  米海軍 1点（N28 PD）／追悼 6点（TW46・TW48 PD・P1 CC0・AN74 BY-SA・G2 Attribution・L1 CC BY）
■ 🔴 絵を見た記録（09-29 ⑤b-7a）：23点を 640px・2列×3行のシート4枚で全数、疑い4点を原寸で。
  ・G2（光化門 2018）：下の黄色い板に**見つかっていない5人の顔写真と名前**（私人）＝板より上だけに切る（`ss.TRIM`・y 0.76 まで）
  ・L1（救命胴衣の列）：奥の集会の人の**顔がはっきり写る**（私人）＝胴衣の列だけ（y 0.60 から下）に切る
  ・TW46：建物に「단원고」の文字＝学校で合っている・人なし／M1：どちらが船首か写真だけで決められない＝向きの札を付けない
  ・N34（クレーン船 04-20）は取ったが使わない（予備・束に入れない）
■ 頁（`ss.page(N)`）＝PLAN の頁。**切り出しは目印の語の行から機械で決める**（`ANCHOR`・行と行の間で切る＝行の途中で切らない）。
  結果は `pages.json` の `trim`（`cuts/ss.py` が `TRIM` に読む＝手で写さない）。図・写真の頁は画像の矩形（`FIGBOX`）。
■ 動く映像（DVIDS・米国の職務著作）＝`clips`：`ref/ep14/clips.json`・ひかえの静止画 `fb_<カット>.jpg`（`footage.USE` の欄ごと）

    python qa_out/ep14_assets.py build     # ref/ep14/<名>.jpg ＋ assets.json
    python qa_out/ep14_assets.py pages     # ref/ep14/pg<頁>.png ＋ pages.json（trim つき）
    python qa_out/ep14_assets.py clips     # ref/ep14/clips.json ＋ fb_<カット>.jpg（assets.json に登録）
    python qa_out/ep14_assets.py check     # PICK・assets.json・ファイルが揃っているか
    python qa_out/ep14_assets.py panel     # 縦横比の並び（`cuts/ss.py` の PANEL_AR を決める材料）
    python qa_out/ep14_assets.py credits [--write]   # credits.json と ref/CREDITS.md の表
"""
from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SRC = HERE / 'ref' / 'ep14' / 'img'
VID = HERE / 'ref' / 'ep14' / 'vid'
PDF = HERE / 'ref' / 'ep14' / 'src'
DEST = HERE / 'ref' / 'ep14'
DB = DEST / 'assets.json'
PAGES_JSON = DEST / 'pages.json'
CLIPS_JSON = DEST / 'clips.json'
CREDITS_JSON = DEST / 'credits.json'
CREDITS_MD = HERE / 'ref' / 'CREDITS.md'
MAXW = 3000


def C(key, slot, year, **kw):
    """Commons の1点。key＝`ref/ep14/img/meta.json` の鍵（materials.md の記号・番号）。"""
    return dict(src='commons', key=key, slot=slot, year=year, **kw)


# 名前 → 素材。cut＝当てるカット（PLAN の画の欄）。**BY-SA は1点1カット**（`ss.check_frame_only` が止める）
PICK = {
    # ── 当日・船そのもの ───────────────────────────────────────
    # H1：Commons の表示「South Korea-Gov」は根拠が無い（削除依頼中）＝**引用**（額装・無改変・出典＝海洋警察）
    'sinking_0416': C('H1', 'accident', 2014, cut='c107', frame=True,
                      lic='引用（Commons の表示 South Korea-Gov は根拠なし）',
                      note='4月16日・船首と船底だけが出た船・浮かぶコンテナと救命いかだ（韓国海洋警察の撮影）'),
    'sewol_incheon': C('K1', 'ship', 2014, cut='c202・c306・c501',
                       note='2014年3月27日・仁川港のセウォル号。船首に「SEWOL 세월」・船首の甲板にコンテナ（900px＝額装）'),
    'naminoue_2010': C('J1', 'ship', 2010, cut='c301',
                       note='2010年2月14日・鹿児島港の「フェリーなみのうえ」（日本時代の唯一の写真・BY-SA）'),
    'mokpo_2017': C('M1', 'ship', 2017, cut='c412',
                    note='2017年8月2日・木浦新港の横倒しの船体と足場（BY-SA）。⚠️ 船首の向きは写真だけで決められない'),
    # ── 米海軍（PD）───────────────────────────────────────────
    'site_0418': C('N28', 'navy', 2014, cut='c918',
                   note='2014年4月18日・沈んだ場所のまわりのクレーン船と海洋警察の船（MH-60S から）'),
    # ── 捜索（韓国国防部・CC BY-SA 2.0＝額装・1点1カット・「当日の救助」と名乗らない）──────
    'search_tent_0418': C('F15', 'search', 2014, cut='ca02', note='4月18日・テントの前で簡易ベッドを組む兵士'),
    'search_ssu_0419': C('F12', 'search', 2014, cut='ca03', note='4月19日・SSU のゴムボートと潜水員'),
    'search_ship21_0419': C('F6', 'search', 2014, cut='ca04', note='4月19日・艦番号21の艦の舷側とゴムボート'),
    'search_waves_0420': C('F8', 'search', 2014, cut='ca05', note='4月20日・荒れた海の SSU のゴムボートと潜水員'),
    'search_night_0420': C('F11', 'search', 2014, cut='ca06', note='4月20日の夜・クレーン・大きな浮き・ボート'),
    'search_flare_0420': C('F13', 'search', 2014, cut='ca07', note='4月20日の夜・照明弾・SSU のボート'),
    'search_diver_0504': C('F17', 'search', 2014, cut='ca09', note='5月4日・はしけから海へ入る送気式の潜水員'),
    'search_fleet_0506': C('F4', 'search', 2014, cut='ca10', note='5月・島を背に海を埋める捜索の船（横長）'),
    'search_banner_0504': C('F2', 'search', 2014, cut='ca12',
                            note='5月4日・米海軍の艇と、奥のはしけの幕「당신은 우리 아이들의 마지막 희망입니다」'),
    'search_divers_0504': C('F19', 'search', 2014, cut='ca13', note='5月4日・水中の潜水員2人とボートの兵士'),
    'search_flare_0501': C('F20', 'search', 2014, cut='ca14', note='5月1日の夜・照明弾と明かりのはしけ'),
    # ── 追悼・その後（副題に年＝事故の当時ではない）──────────────────
    'danwon_school': C('TW46', 'memorial', 2014, cut='cd01', note='4月22日・ダンウォン高校（建物に「단원고」）・人なし'),
    'danwon_banner': C('TW48', 'memorial', 2014, cut='cd02',
                       note='4月22日・学校のそばの幕「단원고 학생들이 무사히 집으로 돌아오길 간절히 기원합니다」'),
    'seoul_plaza_2014': C('P1', 'memorial', 2014, cut='cd03', note='6月22日・ソウル市庁の「미안합니다」の幕と黄色いテント'),
    'ansan_street_2014': C('AN74', 'memorial', 2014, cut='cd04', note='5月1日・アンサンの通りの横断幕（BY-SA）'),
    'gwanghwamun_2018': C('G2', 'memorial', 2018, cut='cd05',
                          note='2018年3月31日・光化門広場の追悼の場所。🔴 下の板に5人の顔写真と名前＝`ss.TRIM` で板より上だけ'),
    'lifejackets_2017': C('L1', 'memorial', 2017, cut='cd07',
                          note='2017年1月7日・ソウルの集会の救命胴衣の列。🔴 奥の人の顔＝`ss.TRIM` で胴衣の列だけ'),
}
# 画面の出典の「誰が」（撮影者の欄が長い・機関名で名乗る点）
WHO = {
    'sinking_0416': '韓国 海洋警察',
    'sewol_incheon': 'jinjoo2713',
    'naminoue_2010': 'tsuda',
    'mokpo_2017': 'Trainholic',
    'site_0418': '米海軍',
    'danwon_school': 'Fyodor Tertitskiy', 'danwon_banner': 'Fyodor Tertitskiy',
    'seoul_plaza_2014': 'PuzzletChung',
    'ansan_street_2014': 'Piotrus',
    'gwanghwamun_2018': 'Garam',
    'lifejackets_2017': 'Mathew Schwartz',
}
for _n, _r in PICK.items():
    if _r['slot'] == 'search':
        WHO[_n] = '韓国 国防部'

# ══════════════════════════════════════════════════════════
#  頁（台本の頁番号＝判決 p1〜81〈印字の頁〉・海審 p1001〜〈PDF の頁＋1000〉・裁決 p2001〜〈PDF の頁＋2000〉）
# ══════════════════════════════════════════════════════════
PAGES_PICK = (1, 12, 18, 20, 33, 1001, 1015, 1016, 1060, 1083, 1091, 1113, 1136, 2003, 2089)
# (通し番号の頭, ファイル, 資料の鍵＝`cuts/ss.REC_DOCS`, dpi)。**頭の大きい順**（`next()` で最初に当たる）
DOCS = ((2001, 'later/kmst_2026_001_central_verdict.pdf', '裁決', 200),
        (1001, 'kmst_sewol.pdf', '海審', 200),
        (1, 'sewol_scourt.pdf', '判決', 200))
# 画面の出典の頁の書き方（`illu.rec_line` と同じ名前）。範囲を持つ頁だけここに（語りの中身が隣の頁にある）
PAGE_CITE = {1083: '海審 p1083・p1091〜1092', 2089: '裁決 p2088〜2089'}
# 文字の頁：目印の語（空白を除いた原文）→ その行を真ん中に、額の縦横比になるまで上下の行を足して切る
ANCHOR = {
    1: '2015도6809',                       # cb01 判決の1頁（事件番号の見出し）
    12: '대기하라',                         # c707 8時58分の指示
    18: '선내대기중인사실등을',             # c913 乗客が船内で待っていることを伝えなかった
    20: '익사시키는행위',                   # cb07「積極的に水に落として溺死させる行為と変わらない」
    33: '조타기나프로펠러가정상적으로',     # cb10 舵の部品に不具合が起きた可能性を打ち消せない
    1016: '나미노우에호',                   # c308「なみのうえ」の記述
    1060: '30)이당시까지선내비상전원',      # c808 注30
    1091: '확인할수있는자료는없지만',       # cc03 舵角を確かめる資料は無い
    1136: '7.9구명동의를퇴선장소',          # cd06 改善事項 7.9
    # cc14 2026年の裁決の主文＝目印の行から**下へだけ**足す（上は伏せ字の行と調査官の名の行＝要らない・インク率が下がる）
    2003: ('주문이전복사건은', 'down'),
}
PANEL_AR_T = 1120 / 648      # 額の最大の箱（`scene_jiko.PANEL_MAXW × PANEL_MAXH`）の縦横比＝切り出しの目標
# 図・写真の頁：画像（写真）の矩形を PDF から読む頁。値＝その頁の何番目の画像か（大きい順）
#   p1015〔그림1〕2014-04-15 仁川港のセウォル号＝c201（写真だけ＝見出し・頁番号を落とす）
FIGIMG = {1015: 0}
# 見出し・説明の行ごと切る図の頁（頁の割合 x0,y0,x1,y1）。⑤b-7a（09-29）に PDF の行・画像・線の位置を測って
#   **上下の要素のあいだの真ん中**で決めた（行の途中で切らない＝門番 edges）。左右は図の枠の線を両方入れる
FIGVEC = {
    # c109 表紙＝題の3行（「여객선 세월호 전복사고 / 특별조사보고서 / <Safety Investigation Report>」y 0.263〜0.378・x 0.21〜0.79）。
    #   上下の行（柱 0.059・「사고일자」0.574）は遠い＝題の周りに余白 0.028。頁全体だとインク率 3.9%（門番 blank の下限 4% 未満）→ 15.0%
    1001: [0.17, 0.235, 0.83, 0.405],
    # 見出し〔그림4〕(y 0.085〜0.103)＋上のグラフの画像(0.118〜0.479)。上＝柱の罫(0.065)との間・
    #   下＝画像と説明「CASE 1에 따른」(0.490〜0.505) の間（説明の下は次のグラフまで 0.003 しか無い＝説明の上で切る）
    1083: [0.085, 0.075, 0.905, 0.4845],
    # 見出し[그림8](0.094〜0.111)＋図2枚(0.119〜0.387・枠の線〜0.390)。下＝次の行「5.1.1.4」(0.446) との間
    1113: [0.085, 0.08, 0.915, 0.418],
    # 写真の枠(0.142〜0.433)＋説明[사진5](0.436〜0.453)。上＝前の行(〜0.116)との間・下＝次の行(0.482)との間
    #   ⚠️ 画像の下の端に元の報告の小さな字（〔그림2-9〕…）がある＝画像の端で切らず説明の行の下で切る
    2089: [0.085, 0.129, 0.915, 0.4675],
}


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def _meta():
    return json.loads((SRC / 'meta.json').read_text(encoding='utf-8'))


def _src_path(m):
    p = SRC / f"{m['title'].rsplit('.', 1)[0]}.jpg"
    if not p.exists():
        raise SystemExit(f"🔴 {p.name} が無い（`ref/ep14/probe/fetch14_img.py use` で取る）")
    return p


def cmd_build(only=None):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    meta = _meta()
    fx = json.loads((SRC / 'fetched.json').read_text(encoding='utf-8'))
    db = json.loads(DB.read_text(encoding='utf-8')) if DB.exists() else {}
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
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        out = DEST / f'{name}.jpg'
        im.save(out, quality=92)
        db[name] = dict(src='commons', id=m['title'], key=r['key'], slot=r['slot'], cut=r.get('cut', ''),
                        note=r.get('note', ''), box=[0.0, 0.0, 1.0, 1.0], w=im.width, h=im.height, md5=_md5(out),
                        lic=r.get('lic') or m['lic'], frame=bool(r.get('frame')), author=m['artist'],
                        year=r['year'], title=m['title'], hold=f"Wikimedia Commons「{m['title']}」",
                        url=m['page'], sha1=m['sha1'], fetched=fx.get(m['title'], {}).get('fetched', ''))
        print(f"✓ {name:20} {im.width}x{im.height}  {db[name]['lic']}{'（額装だけ＝引用）' if r.get('frame') else ''}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'→ {DB}（{len(db)}点）')
    return 0


# ── 頁の切り出し（行と行の間で切る）─────────────────────────────
def _rows(page):
    """頁の字の行（同じ高さに並ぶ span をまとめた1行）＝[dict(t=空白なしの字, box=(x0,y0,x1,y1))]（上から）。"""
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
    """頁番号・柱（「-12-」「SafetyInvestigationReport해양안전심판원-9-」・下の柱「해양안전심판원」）＝切り出しに入れない行。
    ⚠️ 09-29：下の柱「해양안전심판원」を中身と数えて窓を広げ、その下の頁番号を半分切った（c808）"""
    return bool(re.fullmatch(r'-\d+-', t) or re.search(r'SafetyInvestigationReport', t)
                or re.fullmatch(r'해양안전심판원(-\d+-)?', t))


def text_trim(page, anchor):
    """目印の語を含む行を真ん中に、額の縦横比になるまで上下へ行を足した矩形（頁の割合）。
    anchor が (語, 'down') なら目印の行から下へだけ足す（下が尽きたら上へ）。
    🔴 境目（行間の真ん中）は**頁番号・柱の行も含めた全部の行**で測る（09-29：柱を外して測ったら c808 で頁番号「- 53 -」を
       半分切った＝門番 edges が拾った）。切り出しの中身には柱を入れない。"""
    anchor, mode = (anchor, 'mid') if isinstance(anchor, str) else anchor
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
    x0 = min(r['box'][0] for r in rows)
    x1 = max(r['box'][2] for r in rows)
    want = (x1 - x0 + 24) / PANEL_AR_T
    i0, i1 = a0, a1
    height = lambda: rows[i1]['box'][3] - rows[i0]['box'][1]
    up = mode != 'down'
    while height() < want and (i0 > 0 or i1 < len(rows) - 1):
        if mode == 'down':
            if i1 < len(rows) - 1:
                i1 += 1
            else:
                i0 -= 1
            continue
        if up and i0 > 0:
            i0 -= 1
        elif i1 < len(rows) - 1:
            i1 += 1
        else:
            i0 -= 1
        up = not up
    y_top, y_bot = rows[i0]['box'][1], rows[i1]['box'][3]
    above = [r['box'][3] for r in every if r['box'][3] <= y_top + 0.5]
    below = [r['box'][1] for r in every if r['box'][1] >= y_bot - 0.5]
    top = (max(above) + y_top) / 2 if above else y_top - 8
    bot = (y_bot + min(below)) / 2 if below else y_bot + 8
    W, H = page.rect.width, page.rect.height
    box = (max(0.0, (x0 - 12) / W), max(0.0, top / H), min(1.0, (x1 + 12) / W), min(1.0, bot / H))
    return [round(v, 4) for v in box], dict(rows=[i0, i1], anchor_rows=[a0, a1], n_rows=len(rows))


def image_trim(page, idx):
    """その頁の画像（大きい順の idx 番目）の矩形（頁の割合）。"""
    infos = sorted(page.get_image_info(), key=lambda i: -(i['bbox'][2] - i['bbox'][0]) * (i['bbox'][3] - i['bbox'][1]))
    if len(infos) <= idx:
        raise SystemExit(f'🔴 頁 {page.number + 1} に画像が {len(infos)} 個しか無い')
    x0, y0, x1, y1 = infos[idx]['bbox']
    W, H = page.rect.width, page.rect.height
    return [round(max(0.0, x0 / W), 4), round(max(0.0, y0 / H), 4), round(min(1.0, x1 / W), 4),
            round(min(1.0, y1 / H), 4)], dict(images=len(infos))


def cmd_pages(only=None):
    """`pages` は全頁。`pages 12` のように頁を書けばその頁だけ焼き直す（ほかの頁の md5 を動かさない）。"""
    import fitz
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    for pr in PAGES_PICK:
        if only and pr not in only:
            continue
        base, fn, doc, dpi = next(d for d in DOCS if pr >= d[0])
        pno = pr - base + 1
        with fitz.open(PDF / fn) as d:
            if pno > d.page_count:
                raise SystemExit(f'🔴 p{pr}＝{doc} の PDF {pno}頁は無い（全{d.page_count}頁）')
            pg = d[pno - 1]
            pix = pg.get_pixmap(dpi=dpi)          # 色のまま（裁決 p2089 の写真は色＝引用は色を変えない）
            out = DEST / f'pg{pr}.png'
            pix.save(out)
            trim, how = (None, {})
            if pr in ANCHOR:
                trim, how = text_trim(pg, ANCHOR[pr])
            elif pr in FIGIMG:
                trim, how = image_trim(pg, FIGIMG[pr])
            elif pr in FIGVEC:
                trim, how = FIGVEC[pr], dict(by='FIGVEC')
        old = pj.get(f'pg{pr}', {})
        rec = dict(old, doc=doc, pdf=fn, pdf_page=pno, w=pix.width, h=pix.height, dpi=dpi, md5=_md5(out), how=how)
        rec.pop('trim', None)
        if trim:
            rec['trim'] = trim
        pj[f'pg{pr}'] = rec
        print(f'✓ pg{pr}  {doc} PDF {pno}頁  {pix.width}x{pix.height}  trim={trim}  {how}')
    PAGES_JSON.write_text(json.dumps(pj, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0


# ══════════════════════════════════════════════════════════
#  動く映像（DVIDS・米国の職務著作＝PD）。手元＝`ref/ep14/vid/`（git 管理外）・Actions と Modal は `media` から読む
# ══════════════════════════════════════════════════════════
#   🔴 DVIDS 本体の窓口（download/videofile）は curl に 403（検問）＝配信の置き場 CloudFront の原本を読む（HEAD で 200 を確かめた）
#   ⚠️ 米国防総省の映像・写真＝概要欄に「推奨を意味しない」断り書き（⑥へ申し送り・`ref/CREDITS.md`）
CLIPS = {
    "e1": dict(
        file="ep14/vid/e1.mp4",
        url="https://www.dvidshub.net/video/330919/",
        media="https://d34w7g4gy10iej.cloudfront.net/video/1404/DOD_101385880/DOD_101385880.mp4",
        credit="出典：米海軍（DVIDS）（記録映像より）",
        src="dvids", at=0.0, date="2014-04-18",
        what="USS ボノム・リシャールの見張り・艦橋・MH-60S の発艦（1分30秒・スレートなし）"),
    "e2": dict(
        file="ep14/vid/e2.mp4",
        url="https://www.dvidshub.net/video/332722/sewol-ferry-sar-efforts-31st-meu",
        media="https://d34w7g4gy10iej.cloudfront.net/video/1404/DOD_101470723/DOD_101470723.mp4",
        credit="出典：米海兵隊（DVIDS）（記録映像より）",
        src="dvids", at=0.0, date="2014-04-19",
        what="第31海兵遠征部隊のヘリから見た捜索の海（2分02秒・0〜2秒は英字のスレート＝NOGO）"),
}
# ひかえの静止画を抜く秒（そのカットの中身が分かる秒・ショットの中）
FB_T = {"ca01": 80.0, "ca11": 9.5}


def _probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,sample_aspect_ratio",
                        "-show_entries", "format=duration", "-of", "json", str(p)],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    s = j["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return dict(w=s["width"], h=s["height"], fps=round(int(num) / int(den), 3),
                sar=s.get("sample_aspect_ratio", "1:1"), sec=round(float(j["format"]["duration"]), 3))


def _decoded_size(p, t=1.0):
    """1コマを実際に取り出した寸法。🔴 器の札（ffprobe の width）を信じない：E-2 は 1280×720 の器に
    切り取りの指定（左右16・上下9画素）があり、出てくる絵は 1248×702（→ [[feedback-container-labels-lie-about-the-picture]]）"""
    from PIL import Image
    tmp = VID / f"_probe_{p.stem}.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(p), "-frames:v", "1", str(tmp)], check=True)
    with Image.open(tmp) as im:
        size = im.size
    tmp.unlink()
    return size


def cmd_clips():
    sys.path.insert(0, str(HERE / 'tools'))
    import footage as FO
    clips = {}
    for k, c in CLIPS.items():
        p = VID / Path(c["file"]).name
        m = _probe(p)
        if m["sar"] not in ("1:1", "N/A", None):
            raise SystemExit(f"🔴 {k}: SAR {m['sar']}（正方形でない画素＝dispw を測り直す）")
        dw, dh = _decoded_size(p)
        if abs(dw / dh - 16 / 9) > 0.01:
            raise SystemExit(f"🔴 {k}: 取り出した絵 {dw}x{dh} が 16:9 でない（切り方を決め直す）")
        clips[k] = dict(c, **dict(m, sar="1:1"), dar="16:9", square_w=dw, dispw=dw, decoded=[dw, dh])
        print(f"✓ {k}: {m}  取り出した絵 {dw}x{dh}")
    CLIPS_JSON.write_text(json.dumps(clips, ensure_ascii=False, indent=1), encoding="utf-8")
    db = json.loads(DB.read_text(encoding='utf-8'))
    miss = sorted(set(FO.USE) - set(FB_T))
    if miss:
        raise SystemExit(f"🔴 FB_T に秒が無い欄: {miss}（ひかえの静止画を作れない）")
    from PIL import Image
    for cid, u in FO.USE.items():
        clip, t = u["clip"], FB_T[cid]
        out = DEST / f"fb_{cid}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(VID / f"{clip}.mp4"),
                        "-frames:v", "1", "-q:v", "2", str(out)], check=True)
        with Image.open(out) as im:
            w, h = im.size
        db[f"fb_{cid}"] = dict(src="clip", clip=clip, t=t, slot="video", cut=cid, note=f"{cid} のひかえ（{clip} {t}秒）",
                               box=[0, 0, 1, 1], w=w, h=h, md5=_md5(out), lic="Public domain（米国の職務著作）",
                               author=CLIPS[clip]["credit"].split("：", 1)[1].split("（")[0], year=2014,
                               title=CLIPS[clip]["url"], hold=CLIPS[clip]["url"], url=CLIPS[clip]["url"], frame=False)
        print(f"✓ fb_{cid}.jpg  {w}x{h}  ← {clip} {t}秒")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0


def cmd_check():
    if not DB.exists():
        raise SystemExit('🔴 assets.json が無い（build を先に）')
    db = json.loads(DB.read_text(encoding='utf-8'))
    bad = 0
    for name in PICK:
        p = DEST / f'{name}.jpg'
        if name not in db or not p.exists():
            print(f'🔴 {name}: 束に無い'); bad += 1; continue
        if _md5(p) != db[name]['md5']:
            print(f'🔴 {name}: md5 が assets.json と違う（手で差し替えた？）'); bad += 1
    for name, r in db.items():
        if r.get('src') == 'clip' and not (DEST / f'{name}.jpg').exists():
            print(f'🔴 {name}: ひかえの静止画が無い'); bad += 1
    extra = sorted(n for n in set(db) - set(PICK) if db[n].get('src') != 'clip')
    for e in extra:
        print(f'⚠️ assets.json に PICK に無い名前: {e}')
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    miss = [pr for pr in PAGES_PICK if f'pg{pr}' not in pj or not (DEST / f'pg{pr}.png').exists()]
    if miss:
        print(f'🔴 焼いていない頁: {miss}'); bad += 1
    for k, v in pj.items():
        if (DEST / f'{k}.png').exists() and _md5(DEST / f'{k}.png') != v['md5']:
            print(f'🔴 {k}: md5 が pages.json と違う'); bad += 1
    print('✓ 揃っている' if not bad else f'🔴 {bad}件')
    return 1 if bad else 0


def cmd_panel():
    db = json.loads(DB.read_text(encoding='utf-8'))
    for n, r in sorted(db.items(), key=lambda kv: kv[1]['w'] / kv[1]['h']):
        ar = r['w'] / r['h']
        loss = 1 - (ar / (16 / 9) if ar < 16 / 9 else (16 / 9) / ar)
        print(f"AR {ar:.3f}  {n:22} {r['w']}x{r['h']}  全画面で {loss:.1%} 切れる  {r['lic']}")
    return 0


# 元画像そのものに手を入れた点（`cuts/ss.py` の NEEDS_MASK・`ref/ep14/masked.json`）。14本目は無い
#   ⚠️ 私人の顔と名前は切り出し（`ss.TRIM`）で外した＝G2・L1（改変の旨は `scene_jiko.credit_of` が足す）
MASKED: dict[str, str] = {}


def credit_line(name, r):
    """画面の出典。BY-SA は「（無改変）」まで書く。引用も無改変。PD・CC0 は義務は無いが出どころは名乗る。
    CC BY・Attribution の切り出しの断り（改変）は `scene_jiko.credit_of` が足す（「改変」の字が無ければ）。"""
    lic = r['lic']
    who = WHO.get(name) or r['author']
    if r.get('src') == 'clip':
        return CLIPS[r['clip']]['credit'] + '（静止画）'
    if r.get('frame') and lic.startswith('引用'):
        return f"出典：{who}の撮影（引用・無改変）"
    if 'SA' in lic.upper().replace('-', ' ').split():
        return f"出典：{who}／{lic}（無改変）"
    if lic.upper().startswith('CC BY'):
        return f"出典：{who}／{lic}"
    if lic == 'Attribution':
        # ⚠️ `scene_jiko.credit_of` が改変の旨を足すのは「CC BY」の字があるときだけ＝ここで書く（全画面は色を置き換える＝既定 color 0.0）
        return f"出典：{who}（Wikimedia Commons・帰属表示）／改変：色調変更・切出"
    if lic.upper() == 'CC0':
        return f"出典：{who}／CC0"
    return f"出典：{who}（パブリックドメイン）"


# 頁の文書の年と「誰が」・権利（台本 §10 の出典一覧・②の台帳 §5）
PAGE_DOC = {
    '判決': (2015, '大韓民国 大法院', '判決＝韓国著作権法7条・日本の著作権法13条で権利の目的とならない'),
    '海審': (2014, '海洋安全審判院', '公共ヌリの表示なし＝引用（紙面をそのまま・出典）'),
    '裁決': (2026, '中央海洋安全審判院', '一覧の頁の表示は公共ヌリ第4類型（改変禁止）＝引用（紙面をそのまま・出典）'),
}


def page_credit(pr):
    sys.path.insert(0, str(HERE / 'tools'))
    import illu
    cite = PAGE_CITE.get(pr) or f"{next(d for d in DOCS if pr >= d[0])[2]} p{pr}"
    line = illu.rec_line([cite])
    # ⚠️ `illu.rec_line` は範囲（p1091〜1092）を頭の頁だけにする＝範囲を持つ頁はここで書き直す
    if pr in PAGE_CITE:
        doc = cite.split(' ', 1)[0]
        base = next(d for d in DOCS if d[2] == doc)[0] - 1
        pages = []
        for part in cite.split(' ', 1)[1].split('・'):
            a, _, b = part.lstrip('p').partition('〜')
            a = int(a) - base
            pages.append(f"{a}〜{int(b) - base}" if b else f"{a}")
        line = re.sub(r'PDF [0-9・〜]+頁$', f"PDF {'・'.join(pages)}頁", line)
    return line


def cmd_credits(write=False):
    db = json.loads(DB.read_text(encoding='utf-8'))
    pages = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    cj = {f'ep14/{n}.jpg': credit_line(n, r) for n, r in db.items()}
    cj.update({f'ep14/{k}.png': page_credit(int(k[2:])) for k in pages})
    rows = [f"| `{n}` | {r.get('cut') or '（章ファイル）'} | {r['year'] or '不明'} | {r['lic']} | "
            f"{WHO.get(n) or r['author']} | {r['hold']}　{r.get('url', '')} |" for n, r in db.items()]
    rows += [f"| `{k}` | （章ファイル） | {PAGE_DOC[p['doc']][0]} | {PAGE_DOC[p['doc']][2]} | "
             f"{PAGE_DOC[p['doc']][1]} | {p['pdf']} PDF {p['pdf_page']}頁 |" for k, p in sorted(
                 pages.items(), key=lambda kv: int(kv[0][2:]))]
    for k, v in list(cj.items()):
        print(k, '|', v)
    print(f'… 写真と静止画 {len(db)}点・頁 {len(pages)}枚')
    if write:
        CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding='utf-8')
        md = CREDITS_MD.read_text(encoding='utf-8')
        head = '## セウォル号沈没事故（2014-04-16・14本目）　※2026-09-29（⑤b-7a）'
        # 🔴 見出しは `check_credits.HEADER` と同じ文字列（09-28 から門番は**この回の節 `SECTION` の中だけ**で表を探す＝
        #    13本目と同じ見出しでも前の回の表を読まない＝§5b-82②）。09-29 に別の文字列にして門番が fail closed で止めた
        hdr = '| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |'
        block = '\n'.join([
            head, '',
            '### 1. 写真（Wikimedia Commons ＝ CC BY-SA は**額装・無改変・1点1カット**／CC BY／Attribution／CC0／PD／引用）・映像・判決と報告書の頁',
            '`qa_out/ep14_assets.py credits --write` が書く（手で直さない）。'
            'BY-SA の表示＝撮影者・許諾名と URL・素材の URL・無改変（許諾の URL は概要欄で）。', '',
            '- 🔴 **私人の顔と名前は出さない**：G2（光化門 2018）の下の板＝見つかっていない5人の顔写真と名前／L1（救命胴衣の列）の奥の集会の人＝どちらも切り出し（`cuts/ss.py` の `TRIM`）で外した（改変の旨は画面の出典に出る）',
            '- 🔴 H1（当日の沈む船）＝Commons の表示「South Korea-Gov」に根拠が無い（削除依頼中）＝**引用**（額装・無改変・出典＝韓国 海洋警察）。サムネに使わない',
            '- 🔴 **米国防総省（米海軍・米海兵隊）の写真と映像**（`site_0418`・`e1`・`e2`）＝DVIDS の条件「The appearance of U.S. Department of Defense (DoD) visual information does not imply or constitute DoD endorsement.」＝**概要欄に「米国防総省の画像の使用は、同省の推奨を意味しません」**（⑥の申し送り）',
            '- 映像＝DVIDS 330919（USS Bonhomme Richard・2014-04-18・1920×1080）・332722（31st MEU・2014-04-19・1280×720）。原本は CloudFront の `DOD_<番号>.mp4`（`ref/ep14/clips.json` の `media`）',
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
    if cmd == 'clips':
        return cmd_clips()
    if cmd == 'check':
        return cmd_check()
    if cmd == 'panel':
        return cmd_panel()
    if cmd == 'credits':
        return cmd_credits('--write' in a)
    raise SystemExit(f'知らない命令: {cmd}')


if __name__ == '__main__':
    sys.exit(main())
