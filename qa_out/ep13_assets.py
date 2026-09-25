# -*- coding: utf-8 -*-
"""ep13_assets.py — 13本目（トルコ航空981便）の**写真の束**と**報告書の頁**を作る（2026-09-24 ⑤b-2 新設）。

`qa_out/ep12_assets.py`（12本目）の形を写した。写真は ⑤b-2 で Commons から取った22点
（`ref/ep13/probe/fetch13_img.py`・カズヤくん許可 09-24・控え＝`ref/ep13/img/fetched.json`）。
ここでやるのは「名前を付ける・幅3000pxに縮める・権利を表にする・頁を焼く」だけ。

■ 素材（②の台帳 `ref/ep13/materials.md` §3・台本 `daihon_v2.md` §7 の欄と当てたカット）
  事故機 TC-JAV 4点（A1〜A4）＝ 🔴 **CC BY-SA＝額装だけ・1点1カット**（`cuts/ss.py` の `FRAME_ONLY` が止める）
  予兆の機体 2点（A5 N103AA・A6 AA96便のドアの跡）／現場のその後 4点（B1〜B4）
  同型機 11点（C1〜C6・D1〜D3・D5・D6）／1970年ごろのオルリー 1点（O1＝BY-SA・⑤b-2 で見本を見て採った）
  ✗ D4（NARA の刷り）は使わない（PD の根拠が要確認＝台本 §7）
■ 🔴 絵を見た記録：21点は②の 640px シート（`sheet13_index.tsv`）。O1 と C4 の確かめは ⑤b-2 の見本シート2枚。
  C4 は**題名が「操縦室と操縦士」なのに、絵はニースでタラップを上る乗客**（題名と絵が逆＝絵が正本）。
■ 報告書の頁（`ss.page(N)`）＝台本 §7 の頁＋決め所をなぞる型（trace）の候補の頁。
  🔴 p144〜p149（地上係員の供述・署名・氏名）は**焼かない**（台本 §1-2 実名の線）。

    python qa_out/ep13_assets.py build     # ref/ep13/<名>.jpg ＋ assets.json
    python qa_out/ep13_assets.py pages     # ref/ep13/pg<頁>.png ＋ pages.json
    python qa_out/ep13_assets.py check     # PICK・assets.json・ファイルが揃っているか
    python qa_out/ep13_assets.py panel     # 縦横比の並び（`cuts/ss.py` の PANEL_AR を決める材料）
    python qa_out/ep13_assets.py credits [--write]   # credits.json と ref/CREDITS.md の表
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

SRC = HERE / 'ref' / 'ep13' / 'img'
PDF = HERE / 'ref' / 'ep13' / 'src'
DEST = HERE / 'ref' / 'ep13'
DB = DEST / 'assets.json'
PAGES_JSON = DEST / 'pages.json'
CREDITS_JSON = DEST / 'credits.json'
CREDITS_MD = HERE / 'ref' / 'CREDITS.md'
MAXW = 3000


def C(stem, slot, year, **kw):
    """Commons の1点。stem＝`ref/ep13/img/` のファイル名（拡張子なし）。**縁は測らない**（Commons に縁は無い）。"""
    return dict(src='commons', id=stem, slot=slot, year=year, **kw)


# 名前 → 素材。**欄（slot）は台本 §7 の欄**。cut＝台本 §7 で当てたカット（1点1カットの照合に使う）
PICK = {
    # ── 事故機 TC-JAV（CC BY-SA＝額装だけ・1点1カット）──────────────
    'tcjav_taxi': C('TC-JAV (5920254289) (2)', 'tcjav', 1973, cut='c202',
                    note='1973年夏・ヒースロー。地上走行・胴に THY の文字（A1）'),
    'tcjav_takeoff': C('TC-JAV (6004629408)', 'tcjav', 1973, cut='c104',
                       note='1973年夏・ヒースロー。離陸の瞬間（A2）'),
    # ⚠️ 撮影年が決まらない点は None（表では「不明」）。⑤b-2 で一度「推測の年」を入れて直した（D6 に 1975）
    'tcjav_tail': C('TC-JAV, Turkish DC-10 (6060110163)', 'tcjav', None, cut='c606',
                    note='尾部のエンジンと登録記号 TC-JAV（A3・縦長）。⚠️ Commons の日付は「1974年3月3日より前」だけ'),
    'tcjav_landing': C('THY Türk Hava Yolları - Turkish Airlines McDonnell Douglas DC-10-10 London - Heathrow 1973',
                       'tcjav', 1973, cut='c701', note='1973年・ヒースロー。着陸（白黒・A4）'),
    # ── 予兆の機体 ─────────────────────────────────────────
    'n103aa_1977': C('N103AA American DC-10-10 at KSFO', 'n103aa', 1977, cut='c401',
                     note='1977年3月・サンフランシスコの N103AA（ドアが外れた機体そのもの・修理後・A5）'),
    'aa96_door': C('Photo of American Airlines Flight 96 cargo door', 'n103aa', 1972, cut='c421',
                   note='AA96便のドアの外れた跡を後ろから見る人（顔は見えない・A6）'),
    # ── 現場のその後・慰霊（事故の当時ではない＝副題に年）────────────
    'wreck_1997': C('Paris DC-10 Crash- March 3, 1974', 'after', 1997, cut='c102',
                    note='1997年5月・現場に残っていた機体の破片（B1）。題名の日付は事故の日＝撮影は1997年'),
    'names_wall': C('Paris DC-10 Crash, Names', 'after', 1997, cut='c814',
                    note='慰霊の名前の壁（1997年・B2）。⚠️ 原寸で私人の名前が読める＝読めない大きさで（⑤b-3 で決める）'),
    'stele_2010': C('Stèle du crash aérien de 1974 (parcelle 144)', 'after', 2010, cut='c801',
                    note='森の中の石碑（2010年・B3・BY-SA＝額装）'),
    'monument_2010': C('Monument DC10 Ermenonville-1', 'after', 2010, cut='c915',
                       note='石碑（2010年・B4・729px＝額装パネル）'),
    # ── 同型機（副題は「同型機（航空会社・年）」。TC-JAV と名乗らない）──────
    'klm_landing_1972': C('Eerste DC 10 voor KLM landt op Schiphol, Bestanddeelnr 926-1070', 'dc10', 1972,
                          cut='c506', note='1972年12月・KLM の初号機がアムステルダムに着陸（白黒・C1）'),
    'klm_apron_1972': C('Eerste DC 10 voor KLM landt op Schiphol, DC 10 op platform, Bestanddeelnr 926-1071',
                        'dc10', 1972, cut='c207', note='駐機場で荷物車・作業員に囲まれる DC-10（地上作業・C2）'),
    'klm_cockpit_1972': C('Eerste DC 10 voor KLM landt op Schiphol, cockpit en interieur, Bestanddeelnr 926-1073',
                          'dc10', 1972, cut='c704', note='操縦室と2人（乗員＝公的な任務・C3）'),
    'klm_nice_1973': C('Vlucht met DC-10 naar Nice, cockpit DC-10 met piloten, Bestanddeelnr 926-2653', 'dc10',
                       1973, cut='c804',
                       note='1973年3月・ニースで乗客がタラップを上る（C4）。⚠️ 題名は「操縦室と操縦士」だが絵はタラップ'),
    'aa_dc10_1974': C('American Airlines McDonnell Douglas DC-10 01', 'dc10', 1974, cut='c424',
                      note='1974年8月・AA の DC-10（カラー・C5）'),
    'kal_longbeach_1974': C('Korean Air Lines McDonnell Douglas DC-10 N198 01', 'dc10', 1974, cut='c605',
                            note='1974年8月・ダグラスのロングビーチ工場で引き渡し前の DC-10（C6）'),
    'ua_longbeach_1974': C('United Airlines DC-10 N1826U', 'dc10', 1974, cut='c617',
                           note='1974年8月・ロングビーチ空港のユナイテッド機（D1）'),
    'dc10_flight_1971': C('McDonnell Douglas DC-10 N1803U (C15-10)', 'dc10', 1971, cut='c713',
                          note='飛行中の DC-10（白黒・ダグラスの広報写真・D2）'),
    'dc10_cabin': C('McDonnell Douglas DC-10 interior (CJ406257)', 'dc10', None, cut='c802',
                    note='客室と客室乗務員（広報写真・D3）。⚠️ Commons の日付は「1974年より前」＝年は副題に書かない'),
    'tcjau_fra_1974': C('Douglas DC-10-10 TC-JAU THY FRA 28.07.74 edited-2', 'dc10', 1974, cut='c203',
                        note='姉妹機 TC-JAU・1974年7月28日・フランクフルト（カラー・1054px＝額装パネル・D5）'),
    'finnair_dc10': C('Finnairin DC-10 lentokone lentokentällä 1970 (HK7137-875)', 'dc10', None, cut='c206',
                      note='フィンエアーの DC-10 と乗客（D6）。⚠️ Commons の日付欄は空・題の「1970」は年代の可能性＝年は副題に書かない'),
    # ── 1970年代のオルリー（BY-SA＝額装）─────────────────────────
    'orly_hall_1970': C('Departure hall at Paris-Orly airport (LBS SR04-038169)', 'orly', 1970, cut='c209',
                        note='1970年ごろのオルリーの出発ロビー（スイス航空の写真・ETH 図書館・O1）'),
}
# 画面の出典の「誰が」（撮影者の欄が長い・機関名で名乗る点）
WHO = {
    'aa96_door': '米連邦航空局（FAA）',
    'klm_landing_1972': 'オランダ国立公文書館（Anefo）', 'klm_apron_1972': 'オランダ国立公文書館（Anefo）',
    'klm_cockpit_1972': 'オランダ国立公文書館（Anefo）', 'klm_nice_1973': 'オランダ国立公文書館（Anefo）',
    'dc10_flight_1971': 'マクドネル・ダグラス社の広報写真', 'dc10_cabin': 'マクドネル・ダグラス社の広報写真',
    'finnair_dc10': 'Volker von Bonin／フィンランド文化遺産庁',
    'orly_hall_1970': 'スイス航空／ETH 図書館',
}

# 報告書の頁（台本 §7 の画の欄に出てくる頁＋決め所をなぞる型の候補）。名前は `pg<頁>`
# 🔴 p144〜p149 は入れない（地上係員の供述・署名＝台本 §1-2）
PAGES_PICK = (
    # 仏 最終報告（S1）：§7 の11頁
    15, 16, 17, 63, 88, 90, 91, 92, 94, 95, 109,
    # 仏：決め所の原文（なぞる型の候補）＝#1 p105・#11 p80・#12 p53・#13 p11/p141・#15 p104・#16 p107
    11, 53, 80, 104, 105, 107, 141,
    # 英訳 AIB 8/76（S2）：表紙 p1001・#13 p1010・#15 p1052・#1 p1053
    1001, 1010, 1052, 1053,
    # 米上院（S6）：§7 の10頁＋#9 p2034（電報の表示板）
    2005, 2014, 2017, 2030, 2032, 2033, 2034, 2046, 2051, 2055,
    # AD・官報・SB（S7〜S13）
    4001, 4101, 4201, 4301, 5002, 5003)
# (通し番号の頭, ファイル, 資料の名, dpi)。**頭の大きい順**（`next()` で最初に当たる）
DOCS = ((5101, 'faa_SB52-38.pdf', 'SB 52-38', 200), (5001, 'faa_SB52-37.pdf', 'SB 52-37', 200),
        (4301, 'fr_1974-04-02_11992.pdf', '官報 1974-04-02', 200),
        (4201, 'faa_AD75-15-05.pdf', 'AD 75-15-05', 200), (4101, 'faa_AD74-12-07.pdf', 'AD 74-12-07', 200),
        (4001, 'faa_AD74-08-04.pdf', 'AD 74-08-04', 200),
        (3001, 'ntsb_AAR73-02_N103AA_erau.pdf', 'NTSB AAR-73-02', 200),
        # ⚠️ 上院の資料は頁が 1227x1830pt（ほかの約2倍）＝200dpi だと 3400x5100px になる＝100dpi
        (2001, 'senate_cprt93_dc10.pdf', '米上院 報告', 100),
        (1001, 'aib_8-76_TC-JAV.pdf', 'AIB 8/76', 200),
        (1, 'faa_FinalAccidentReportinFrench.pdf', '仏 最終報告', 200))


# ══════════════════════════════════════════════════════════
def _fetched():
    return {v['file'].rsplit('.', 1)[0]: dict(v, title=t)
            for t, v in json.loads((SRC / 'fetched.json').read_text(encoding='utf-8')).items()}


def _src_path(r):
    p = SRC / f"{r['id']}.jpg"
    if not p.exists():
        raise SystemExit(f"🔴 {p.name} が無い（`ref/ep13/probe/fetch13_img.py use` で取る）")
    return p


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def _plain(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', str(s or ''))).strip()


def cmd_build(only=None):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    fx = _fetched()
    db = json.loads(DB.read_text(encoding='utf-8')) if DB.exists() else {}
    for name, r in PICK.items():
        if only and name not in only:
            continue
        sp = _src_path(r)
        m = fx[r['id']]
        with Image.open(sp) as im0:
            im = im0.convert('RGB')
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        out = DEST / f'{name}.jpg'
        im.save(out, quality=92)
        db[name] = dict(src='commons', id=r['id'], slot=r['slot'], cut=r.get('cut', ''), note=r.get('note', ''),
                        box=[0.0, 0.0, 1.0, 1.0], w=im.width, h=im.height, md5=_md5(out),
                        lic=m['lic'], author=_plain(m['artist']), year=r['year'], title=m['title'],
                        hold=f"Wikimedia Commons「{m['title']}」", url=m['orig_url'] if 'orig_url' in m else
                        'https://commons.wikimedia.org/wiki/File:' + m['title'].replace(' ', '_'))
        print(f'✓ {name:20} {im.width}x{im.height}  {m["lic"]}')
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'→ {DB}（{len(db)}点）')
    return 0


def cmd_pages(only=None):
    """`pages` は全頁。`pages 105` のように頁を書けばその頁だけ焼き直す（ほかの頁の md5 を動かさない）。"""
    import fitz
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    for pr in PAGES_PICK:
        if only and pr not in only:
            continue
        if 144 <= pr <= 149:
            raise SystemExit(f'🔴 p{pr} は焼かない（地上係員の供述・署名＝台本 §1-2）')
        base, fn, doc, dpi = next(d for d in DOCS if pr >= d[0])
        pno = pr - base + 1
        with fitz.open(PDF / fn) as d:
            if pno > d.page_count:
                raise SystemExit(f'🔴 p{pr}＝{doc} の PDF {pno}頁は無い（全{d.page_count}頁）')
            pix = d[pno - 1].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
            out = DEST / f'pg{pr}.png'
            pix.save(out)
        old = pj.get(f'pg{pr}', {})
        pj[f'pg{pr}'] = dict(old, doc=doc, pdf=fn, pdf_page=pno, w=pix.width, h=pix.height, dpi=dpi, md5=_md5(out))
        print(f'✓ pg{pr}  {doc} の PDF {pno}頁  {pix.width}x{pix.height}（{dpi}dpi）')
    PAGES_JSON.write_text(json.dumps(pj, ensure_ascii=False, indent=1), encoding='utf-8')
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
    cuts = {}
    for name, r in PICK.items():
        cuts.setdefault(r.get('cut'), []).append(name)
    for c, ns in cuts.items():
        if c and len(ns) > 1:
            print(f'🔴 {c} に2点を当てている: {ns}'); bad += 1
    extra = sorted(set(db) - set(PICK))
    for e in extra:
        print(f'⚠️ assets.json に PICK に無い名前: {e}')
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    miss = [pr for pr in PAGES_PICK if f'pg{pr}' not in pj or not (DEST / f'pg{pr}.png').exists()]
    if miss:
        print(f'🔴 焼いていない頁: {miss}'); bad += 1
    print('✓ 揃っている' if not bad else f'🔴 {bad}件')
    return 1 if bad else 0


def cmd_panel():
    db = json.loads(DB.read_text(encoding='utf-8'))
    for n, r in sorted(db.items(), key=lambda kv: kv[1]['w'] / kv[1]['h']):
        ar = r['w'] / r['h']
        loss = 1 - (ar / (16 / 9) if ar < 16 / 9 else (16 / 9) / ar)
        print(f"AR {ar:.3f}  {n:20} {r['w']}x{r['h']}  全画面で {loss:.1%} 切れる  {r['lic']}")
    return 0


# 元画像そのものに手を入れた点（`cuts/ss.py` の NEEDS_MASK・`ref/ep13/masked.json`）。CC BY は改変の旨を出典に書く
#   ⚠️ `build` で取り直すとモザイクが消える＝`check_photo_mask` が md5 で止める（⑤b-4・09-25）
MASKED = {'names_wall': '名前にモザイク'}


def credit_line(name, r):
    """画面の出典。BY-SA は「（無改変）」まで書く（10本目と同じ形。`scene_jiko.credit_of` は
    「改変」の字があれば「改変：色調変更・切出」を足さない）。PD・CC0 は義務は無いが出どころは名乗る。"""
    lic = r['lic']
    who = WHO.get(name) or r['author']
    if 'SA' in lic.upper().replace('-', ' ').split():
        return f"出典：{who}／{lic}（無改変）"
    if lic.upper().startswith('CC BY') and name in MASKED:
        return f"出典：{who}／{lic}（改変：{MASKED[name]}・色調変更・切出）"
    if lic.upper().startswith('CC BY'):
        return f"出典：{who}／{lic}"
    if lic.upper() == 'CC0':
        return f"出典：{who}／CC0"
    return f"出典：{who}（パブリックドメイン）"


# 頁の文書の年と「誰が」（台本 §10 の出典一覧・表紙で確かめた値）
PAGE_DOC = {
    '仏 最終報告': (1976, 'フランス事故調査委員会', '仏国の公文書＝引用（改変しない）'),
    'AIB 8/76': (1976, '英国事故調査局（仏報告の英訳）', '英国の公文書＝引用（改変しない）'),
    '米上院 報告': (1974, '米上院 商業委員会 航空小委員会', 'Public domain（米国の職務著作）'),
    'NTSB AAR-73-02': (1973, '米国家運輸安全委員会（NTSB）', 'Public domain（米国の職務著作）'),
    'AD 74-08-04': (1974, '米連邦航空局（FAA）', 'Public domain（米国の職務著作）'),
    'AD 74-12-07': (1974, '米連邦航空局（FAA）', 'Public domain（米国の職務著作）'),
    'AD 75-15-05': (1975, '米連邦航空局（FAA）', 'Public domain（米国の職務著作）'),
    '官報 1974-04-02': (1974, '米官報（Federal Register）', 'Public domain（米国の職務著作）'),
    'SB 52-37': (1972, 'マクドネル・ダグラス社', '企業の技術文書＝引用（改変しない）'),
    'SB 52-38': (1972, 'マクドネル・ダグラス社', '企業の技術文書＝引用（改変しない）'),
}


def cmd_credits(write=False):
    db = json.loads(DB.read_text(encoding='utf-8'))
    cj = {f'ep13/{n}.jpg': credit_line(n, r) for n, r in db.items()}
    rows = [f"| `{n}` | {r.get('cut') or '（章ファイル）'} | {r['year'] or '不明'} | {r['lic']} | "
            f"{WHO.get(n) or r['author']} | {r['hold']}　{r.get('url', '')} |" for n, r in db.items()]
    pages = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    rows += [f"| `{k}` | （章ファイル） | {PAGE_DOC[p['doc']][0]} | {PAGE_DOC[p['doc']][2]} | "
             f"{PAGE_DOC[p['doc']][1]} | {p['doc']} PDF {p['pdf_page']}頁 |" for k, p in sorted(
                 pages.items(), key=lambda kv: int(kv[0][2:]))]
    for k, v in list(cj.items())[:5]:
        print(k, '|', v)
    print(f'… 写真 {len(cj)}点・頁 {len(pages)}枚')
    if write:
        CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding='utf-8')
        md = CREDITS_MD.read_text(encoding='utf-8')
        head = '## トルコ航空981便（1974-03-03・13本目）　※2026-09-24（⑤b-2）'
        # 🔴 見出しの最後の列は**12本目（所蔵と識別子）と別の文字列**にする。`check_credits.load_table()` は
        #    `lines.index(HEADER)` で最初に当たった表を読む＝同じ見出しだと12本目の表を黙って読み続ける（09-24 に実測）
        hdr = '| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |'
        block = '\n'.join([
            head, '',
            '### 1. 写真（Wikimedia Commons ＝ CC BY-SA は**額装・無改変・1点1カット**／CC BY／CC0／PD）と報告書の頁',
            '`qa_out/ep13_assets.py credits --write` が書く（手で直さない）。'
            'BY-SA の表示＝撮影者・許諾名と URL・素材の URL・無改変（許諾の URL は概要欄で）。', '',
            hdr, '|---|---|---|---|---|---|', *rows, ''])
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
