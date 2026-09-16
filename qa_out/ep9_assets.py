# -*- coding: utf-8 -*-
"""ep9_assets.py — 9本目（テネリフェ）の**写真の束**を作る（2026-09-16 ⑤b-1 新設）。

■ なぜ要るか
  ②は `ref/ep9/slots_commons.json` に73点の**一覧**を作っただけで、束は1点も作っていない。
  しかも台本第2版 §5 のとおり **`losrodeos_now` 8点に38カット**など、欄ごとに足りない。
  ⑤b-1 で候補を足し、「選ぶ・落とす・出典を作る・シートで見る」を1本にまとめる。

■ 🔴 守っていること
  1. **継承（CC BY-SA・GFDL）は1点も入れない**。取得した権利表示で**もう一度**検査して止める
     （②の `ep9_slots.py` と同じ網を、落とす直前にもう一度かける）。
  2. **Commons に無い題名は黙って飛ばさず止める**（fail closed）。
  3. **撮影年は出典に出す**。`DateTimeOriginal` が無いものは「不明」（年を作らない）
     → [[feedback-fallback-stills-must-match-the-era]]
  4. 出力はファイルへ。`| tail` でつながない（[[feedback-pipes-mask-exit-codes]]）。
  5. 画素は **幅3,000px まで**（8本目の `ref/ep8/` と同じ扱い＝最大3,032）。
     それより大きい原本は Commons の縮小版を落とす。

    python qa_out/ep9_assets.py info       # 寸法・権利・撮影者・日付を引いて ref/ep9/assets.json へ
    python qa_out/ep9_assets.py fetch      # ref/ep9/<名>.jpg に落とす
    python qa_out/ep9_assets.py check      # PICK・assets.json・ファイルの3つが揃っているか
    python qa_out/ep9_assets.py panel      # 切り落とし率の並び（PANEL_AR を決める材料）
    python qa_out/ep9_assets.py sheet [名の頭 ...]   # 640px のシート（2列×3行）
    python qa_out/ep9_assets.py credits    # scene_jiko.EP9_PHOTO と ref/CREDITS.md の表
"""
from __future__ import annotations

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

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine/1.0 (accident-documentary research; contact: konariri8@gmail.com)'
SA = re.compile(r'\bSA\b|share[- ]?alike|GFDL|GPL', re.I)
DEST = HERE / 'ref' / 'ep9'
DB = DEST / 'assets.json'
SLOTS_JSON = DEST / 'slots_commons.json'
SHEET = HERE / 'out' / 'ep9_sheet'
MAXW = 3000
CREDITS = HERE / 'ref' / 'CREDITS.md'
# 🔴 `tools/check_credits.py` の `HEADER` と**1字も違わない**こと（違えば門番は表を読めずに止まる）。
#    ⚠️ 7本目（元の題名）・8本目（NASA の識別子）と最後の列を変えてある＝前の回の表を読まない
TABLE_HEAD = '| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | Commons の題名 |'
# ⚠️ この節は `ref/CREDITS.md` の**末尾**に置く（書き出すたびに、ここから下を差し替える）
SECTION_HEAD = '## テネリフェ空港衝突事故（1977-03-27・9本目）'

# ══════════════════════════════════════════════════════════
#  🔴 PICK ── 名前 → Commons の題名
# ══════════════════════════════════════════════════════════
# 名前が `ref/ep9/<名>.jpg`・`cuts/ss.py` の定数・`scene_jiko.EP9_PHOTO` の鍵の3つを兼ねる。
# ②の73点は `slots_commons.json` の並びから `<欄>_<NN>` で自動に名付ける（手で写さない）。
# ⑤b-1 で足した候補は下の ADD。値は題名そのもの、または
# （題名の頭, 何番目）＝ Commons の題名が長くて一覧で切れているものを頭で引く。
ADD = {
    # ── いまのテネリフェ北空港（②の8点の外。分類を深さ3まで歩き、全文検索でも当てた）──
    #    ⚠️ 大半は機体が主役。**写っているのは現在の空港**＝副題で「現在の」と名乗る
    'losrodeos_now_09': 'A340-tenerifenorth.JPG',
    'losrodeos_now_10': 'Tenerife North Airport.jpg',
    'losrodeos_now_11': 'Tenerife North Airport (2).jpg',
    'losrodeos_now_12': 'Airbus 340-600 EC-IZX de Iberia landing in Los Rodeos airport.jpg',
    'losrodeos_now_13': 'EC-JBJ (8663466023).jpg',
    'losrodeos_now_14': 'EC-LKH (8667167560).jpg',
    'losrodeos_now_15': 'EC-LKH (8666109731).jpg',
    'losrodeos_now_16': 'EC-IDA (8663483661).jpg',
    'losrodeos_now_17': 'EI-EBW (8667219504).jpg',
    'losrodeos_now_18': 'Luke SkyVueling.jpg',
    # ── 空港の北東、ラ・ラグーナの山地に降りた雲（2025年）──────────────
    #    ⚠️ **空港そのものは写っていない**。c5 の「地面につく雲」の見本として使うなら、
    #       副題で場所と年を名乗る（ハルディーナ展望台・2025年）
    'fog_laguna_01': '20250702 Mirador de Jardina 01.jpg',
    'fog_laguna_02': '20250702 Mirador de Jardina 02.jpg',
    'fog_laguna_03': '20250702 Mirador de Jardina 03.jpg',
    'fog_laguna_04': '20250702 Mirador de Jardina 04.jpg',
    'fog_laguna_05': '20250702 Mirador de Jardina 05.jpg',
    'fog_laguna_06': 'Mountains Tenerife north.jpg',
    # ── 747 の操縦室（年代の合うものを先に）───────────────────────
    'cockpit_747_02': 'Vlucht met Boeing 747 naar Rome van Schiphol cockpit, Bestanddeelnr 924-3165.jpg',
    'cockpit_747_03': 'Vlucht met Boeing 747 naar Rome van Schiphol cockpit, Bestanddeelnr 924-3166.jpg',
    'cockpit_747_04': 'Vlucht met Boeing 747 naar Rome van Schiphol, Bestanddeelnr 924-3167.jpg',
    'cockpit_747_05': ('Vliegtrainingsgebouw KLM op Schiphol-Oost geopend interieur van cockpit Boeing', 0),
    # ⚠️ 頭で引くと**600×400 の GIF の複製**に当たった（並べ替えで先に来る）。原本の題名を書く
    'cockpit_747_06': 'Mrs. Nixon visits the cockpit of the first commercial Boeing 747 jet in conjunction with the christening ceremony for... - NARA - 194665.tif',
    'cockpit_747_07': 'Boeing 747-206SUD flightdeck (9649946519).jpg',
    'cockpit_747_08': 'F-BPVJ cockpit, Air France Boeing 747-128.jpg',
    'cockpit_747_09': 'B747-cockpit.jpg',
    'cockpit_747_10': 'B747-200SF FE Panel.JPG',
    'cockpit_747_11': ('Cockpit of Boeing 747-136, serial 20269', 0),
    'cockpit_747_12': ('Cockpit of Boeing 747-136, serial 20269', 1),
    'cockpit_747_13': ('Cockpit of Boeing 747-136, serial 20269', 2),
    'cockpit_747_14': 'E-4B cockpit.jpg',
    'cockpit_747_15': 'Cockpit of Shuttle Carrier Aircraft 905 (KSC-2012-2185).jpg',
    'cockpit_747_16': ('Frankfurt- Flughafen; Jumbo-Jet; Cockpit', 0),
    'cockpit_747_17': '1989 05 11 B747 121 LX FCV LO AF flt deck mid atlantic.jpg',
    # ── 747 のエンジン（JT9D）──────────────────────────────────
    'engine_747_02': ('Pratt & Whitney JT9D-7 turbofan engine, 1970', 0),
    'engine_747_03': ('Pratt & Whitney JT9D (1969) used in Boeing 747 at Flugausstellung Hermeskeil', 0),
    'engine_747_04': ('Pratt & Whitney JT9D (1969) used in Boeing 747 at Flugausstellung Hermeskeil', 1),
    'engine_747_05': 'Cityofeverett-engine.jpg',
    # ❌ 'Boeing 747 rollout (6).jpg' / '(7).jpg'（1968年・ファンの大きさを人で見せる写真）は**外した**。
    #    PD の根拠が `PD-Sweden-photo`（スウェーデンの「単なる写真」50年）で、Commons 自身が
    #    `PD-old-warning-text` を付けている＝**米国では保護が残っている恐れ**がある
    #    （URAA：1996年時点でスウェーデンで保護期間内だった写真は米国で復活する）。
    #    → [[feedback-pd-label-hides-two-different-grounds]]。絵は惜しいが、権利で落とす。
    # ── KLM の 747（1970〜73年・スキポール空港・Anefo CC0）──────────────
    'klm_747_same_type_04': 'De Boeing 747 wordt door een batsman naar een juiste positie op het platform van, Bestanddeelnr 923-6393.jpg',
    'klm_747_same_type_05': 'Onder een Hollandse wolkenlucht is de Boeing 747 Jumbo-jet op het platform Schip, Bestanddeelnr 923-6389.jpg',
    'klm_747_same_type_06': 'Op het platform van Schiphol kan de Boeing 747 tijdens het uitladen op grote bel, Bestanddeelnr 923-6388.jpg',
    'klm_747_same_type_07': 'De Boeing 747 aan de pier op het platform, Bestanddeelnr 923-6395.jpg',
    'klm_747_same_type_08': 'De Boeing 747 aan de pier op het platform, Bestanddeelnr 923-6396.jpg',
    'klm_747_same_type_09': 'De Boeing 747 net voor de landing op Schiphol, Bestanddeelnr 923-6399.jpg',
    'klm_747_same_type_10': 'De Boeing 747 landt op Schiphol, Bestanddeelnr 923-6392.jpg',
    'klm_747_same_type_11': ('Eerste Jumbo-Jet Boeing 747 B , van KLM arriveert op Schiphol', 0),
    'klm_747_same_type_12': ('Eerste Jumbo-Jet Boeing 747 B , van KLM arriveert op Schiphol', 1),
    'klm_747_same_type_13': ('KLM bouwt geluidsmuur rond platform', 0),
    'klm_747_same_type_14': 'De gekaapte Jumbo is terugekeerd op Schiphol, Bestanddeelnr 926-8612.jpg',
    # ── パンナムの 747（年代の合うもの）──────────────────────────────
    'panam_747_same_type_04': 'Amerikaanse Luchtvaartmij Pan Am gaat 27 op Amsterdam vliegen met een 747 voo, Bestanddeelnr 923-5862.jpg',
    'panam_747_same_type_05': 'Pan American World Airways Boeing 747 N750PA 01.jpg',
    'panam_747_same_type_06': 'AT THE JOHN F. KENNEDY AIRPORT - NARA - 547951.jpg',
    'panam_747_same_type_07': 'Pan American World Airways - Pan Am Boeing 747-121 N732PA "Clipper Ocean Telegraph" (29935660081).jpg',
    'panam_747_same_type_08': 'Pan American World Airways - Pan Am Boeing 747-121 N754PA "Clipper Ocean Rover" (24059638596).jpg',
    # ── カナリア諸島（宇宙から・地図の地に敷く候補）──────────────────────
    'canary_iss_01': 'ISS020-E-21144 - View of the Canary Islands.jpg',
}


# ══════════════════════════════════════════════════════════
#  🔴🔴 2026-09-16（⑤b-1）640px のシートで見て分かった直し
# ══════════════════════════════════════════════════════════
# ① **②の `klm_747_same_type` は KLM ではなかった。**Anefo の1970年の連作「スキポールに初めて来た
#    ジャンボ機」（923-63xx）は、胴に **PAN AM**・尾翼にパンナムの地球の印が写っている
#    （KLM が747を受け取ったのは1971年）。名前のまま副題を書くと**写っていない航空会社を名乗る**。
#    → 名前ごと付け直す（`ref/ep9/photos.md` §1）。本物の KLM の747 は 924-2251/2252（1971）と 926-8612（1973）だけ。
RENAME = {
    'klm_747_same_type_01': 'panam_ams1970_01', 'klm_747_same_type_02': 'panam_ams1970_02',
    'klm_747_same_type_03': 'panam_ams1970_03', 'klm_747_same_type_04': 'panam_ams1970_04',
    'klm_747_same_type_05': 'panam_ams1970_05', 'klm_747_same_type_06': 'panam_ams1970_06',
    'klm_747_same_type_07': 'panam_ams1970_07', 'klm_747_same_type_08': 'panam_ams1970_08',
    'klm_747_same_type_09': 'panam_ams1970_09', 'klm_747_same_type_10': 'panam_ams1970_10',
    'klm_747_same_type_11': 'klm_747_1971_01', 'klm_747_same_type_12': 'klm_747_1971_02',
    'klm_747_same_type_13': 'wing_747_1972_01', 'klm_747_same_type_14': 'klm_747_1973_01',
}
# ② 撮影年の直し。`DateTimeOriginal` が**写真の年ではなく取り込みの年**を持っていたもの。
#    ⚠️ 年は `check_credits.py` が副題の主張と突き合わせる根拠そのもの（黙って間違えると誤報か見逃し）。
YEAR_FIX = {
    'losrodeos_1930_01': 1930,      # 題「Primer vuelo Península - Canarias (1930)」。台帳は 2011（取り込み）
    'panam_n736pa_01': None,        # 台帳は 2006（取り込み）。出どころの番号「76_837」は1976年の見込みだが**未確認**
    'panam_747_same_type_02': 1970,  # `_01`（1970）を切り抜いた派生物。台帳は 2009（派生の年）
}
# ③ 事故現場の6点は**写真の焼き付けを器具に挟んで撮った複写**（黒い台紙・留め具・角の番号札・
#    左に縦書きの「PATERSON」＝器具の商標）。絵は中央の6割ほどなので、切り出す前提で**原寸で持つ**
#    （幅3000に縮めると、切り出したあとの絵が約1950pxしか残らない）。
FULLRES = {'wreck_klm_01', 'wreck_klm_02', 'wreck_klm_03',
           'wreck_both_01', 'wreck_both_02', 'wreck_engine_01'}


def q(params):
    params = dict(params, format='json', formatversion='2')
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(API, data=data, headers={'User-Agent': UA})
    for i in range(5):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception:                                   # noqa: BLE001
            if i == 4:
                raise
            time.sleep(2 * (i + 1))


def base_pick():
    d = json.loads(SLOTS_JSON.read_text(encoding='utf-8'))
    out = {}
    for slot, items in d['slots'].items():
        for i, it in enumerate(items, 1):
            out[f'{slot}_{i:02d}'] = it['title']
    return out


def resolve_prefix(prefix, k):
    """題名の頭から k 番目の題名を引く。**当たらなければ止める。**"""
    key = prefix.replace(' ', '_')
    d = q({'action': 'query', 'list': 'allimages', 'aiprefix': key, 'ailimit': '20'})
    names = sorted(m['name'].replace('_', ' ') for m in d.get('query', {}).get('allimages', []))
    if len(names) <= k:
        raise SystemExit(f'🔴 題名の頭「{prefix}」の {k} 番目が無い（当たり {len(names)}件）')
    return names[k]


def pick():
    out = base_pick()
    for name, v in ADD.items():
        if name in out:
            raise SystemExit(f'🔴 名前 {name} が②の73点と重なる')
        out[name] = v
    out = {RENAME.get(k, k): v for k, v in out.items()}
    if len(out) != len(base_pick()) + len(ADD):
        raise SystemExit('🔴 付け直した名前が既存の名前とぶつかった')
    return out


def _plain(s):
    s = re.sub(r'<[^>]+>', ' ', str(s or ''))
    s = s.replace('&amp;', '&').replace('&quot;', '"').replace('&#039;', "'")
    return re.sub(r'\s+', ' ', s).strip()


def _year(date, desc, title):
    m = re.search(r'(1[89]\d\d|20\d\d)', date or '')
    if m:
        return int(m.group(1))
    return None


def cmd_info():
    pk = pick()
    titles = {}
    for name, v in pk.items():
        titles[name] = resolve_prefix(*v) if isinstance(v, tuple) else v
    rows, bad = {}, []
    names = list(titles)
    for i in range(0, len(names), 40):
        chunk = names[i:i + 40]
        d = q({'action': 'query', 'titles': '|'.join('File:' + titles[n] for n in chunk),
               'prop': 'imageinfo', 'iiprop': 'url|size|mime|extmetadata',
               'iiurlwidth': str(MAXW),
               'iiextmetadatafilter': 'DateTimeOriginal|LicenseShortName|ImageDescription|Artist|Credit'})
        norm = {x['from']: x['to'] for x in d['query'].get('normalized', [])}
        pages = {p['title']: p for p in d['query']['pages']}
        for n in chunk:
            t = 'File:' + titles[n]
            p = pages.get(norm.get(t, t))
            if not p or p.get('missing') or not p.get('imageinfo'):
                bad.append((n, titles[n], 'Commons に無い'))
                continue
            ii = p['imageinfo'][0]
            em = ii.get('extmetadata', {}) or {}
            g = lambda k: _plain((em.get(k, {}) or {}).get('value', ''))    # noqa: E731
            lic = g('LicenseShortName')
            if SA.search(lic):
                bad.append((n, titles[n], f'継承あり（{lic}）'))
                continue
            date = g('DateTimeOriginal')
            desc = g('ImageDescription')
            rows[n] = dict(title=titles[n], w=ii['width'], h=ii['height'], mime=ii['mime'],
                           url=ii['url'], thumb=ii.get('thumburl'), page=ii.get('descriptionurl'),
                           lic=lic, artist=g('Artist'), credit=g('Credit'), date=date,
                           year=(YEAR_FIX[n] if n in YEAR_FIX else _year(date, desc, titles[n])),
                           desc=desc[:400])
        time.sleep(0.5)
    DB.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'PICK {len(pk)} ／ 引けた {len(rows)} ／ 止めた {len(bad)}')
    for n, t, why in bad:
        print(f'🔴 {n}: {why} … {t}')
    return 1 if bad else 0


def _db():
    if not DB.exists():
        raise SystemExit('🔴 ref/ep9/assets.json が無い。まず info')
    return json.loads(DB.read_text(encoding='utf-8'))


def _get(url, tries=5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:                              # noqa: BLE001
            if i == tries - 1:
                raise
            print(f'   再試行 {i + 1}/{tries}: {e}')
            time.sleep(3 + 3 * i)
    return b''


def cmd_fetch(only=None):
    from PIL import Image
    db = _db()
    DEST.mkdir(parents=True, exist_ok=True)
    ok = skip = err = 0
    for n, r in db.items():
        if only and not any(n.startswith(o) for o in only):
            continue
        out = DEST / f'{n}.jpg'
        if out.exists() and out.stat().st_size > 10000:
            skip += 1
            continue
        full = n in FULLRES
        url = r['thumb'] if (r['w'] > MAXW and r.get('thumb') and not full) else r['url']
        try:
            data = _get(url)
            im = Image.open(io.BytesIO(data))
            im.load()
            if im.mode != 'RGB':
                im = im.convert('RGB')
            if im.width > MAXW and not full:
                im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
            im.save(out, quality=92)
            print(f'✓ {n:<24} {im.width}x{im.height}  {out.stat().st_size / 1024:7.0f} KB')
            ok += 1
        except Exception as e:                              # noqa: BLE001
            print(f'🔴 {n}: {e}')
            err += 1
        time.sleep(0.6)
    print(f'\n落とした {ok} ／ すでに在る {skip} ／ 失敗 {err}')
    return 1 if err else 0


def cmd_check():
    from PIL import Image
    pk, db = pick(), _db()
    bad = 0
    for n in pk:
        f = DEST / f'{n}.jpg'
        if n not in db:
            print(f'🔴 {n}: assets.json に無い'); bad += 1; continue
        if not f.exists():
            print(f'🔴 {n}: ファイルが無い'); bad += 1; continue
        w, h = Image.open(f).size
        if max(w, h) < 1280:
            print(f'⚠️ {n}: {w}x{h}（長い辺も1280未満）')
    extra = sorted(p.stem for p in DEST.glob('*.jpg') if p.stem not in pk)
    if extra:
        print(f'⚠️ PICK に無いファイル: {extra}')
    print(f'PICK {len(pk)} ／ 台帳 {len(db)} ／ 欠け {bad}')
    return 1 if bad else 0


def cmd_panel():
    from PIL import Image
    W, H = 1920, 1080
    rows = []
    for f in sorted(DEST.glob('*.jpg')):
        w, h = Image.open(f).size
        a = w / h
        loss = 1 - (a / (W / H) if a < W / H else (W / H) / a)
        rows.append((loss, f.stem, w, h, a))
    rows.sort()
    for loss, n, w, h, a in rows:
        print(f'{loss * 100:5.1f}%  AR {a:5.3f}  {w:>4}x{h:<4}  {n}')
    return 0


def cmd_sheet(pats):
    from PIL import Image, ImageDraw
    db = _db()
    names = [n for n in pick() if (DEST / f'{n}.jpg').exists()]
    if pats:
        names = [n for n in names if any(n.startswith(p) for p in pats)]
    SHEET.mkdir(parents=True, exist_ok=True)
    TW, TH, BAR, COLS, ROWS = 640, 360, 22, 2, 3
    per = COLS * ROWS
    index = []
    for page in range((len(names) + per - 1) // per):
        chunk = names[page * per:(page + 1) * per]
        sh = Image.new('RGB', (TW * COLS, (TH + BAR) * ROWS), (20, 20, 20))
        dd = ImageDraw.Draw(sh)
        for i, n in enumerate(chunk):
            with Image.open(DEST / f'{n}.jpg') as im:
                im = im.convert('RGB')
                sw, shh = im.size
                z = min(TW / sw, TH / shh)
                im = im.resize((max(1, round(sw * z)), max(1, round(shh * z))), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            for k in range(1, 4):                        # 0.25 刻みの格子（主題の位置を言うため）
                x, y = im.width * k / 4, im.height * k / 4
                d.line([(x, 0), (x, im.height)], fill=(255, 60, 60), width=1)
                d.line([(0, y), (im.width, y)], fill=(255, 60, 60), width=1)
            x0, y0 = (i % COLS) * TW, (i // COLS) * (TH + BAR)
            sh.paste(im, (x0 + (TW - im.width) // 2, y0 + BAR + (TH - im.height) // 2))
            r = db.get(n, {})
            dd.text((x0 + 6, y0 + 5), f"{n}  {sw}x{shh}  {r.get('year') or '?'}  {r.get('lic', '')}",
                    fill=(255, 220, 120))
        tag = (pats[0].rstrip('_') if pats else 'all')
        p = SHEET / f'{tag}_{page + 1:02d}.jpg'
        sh.save(p, quality=88)
        index.append(f'{p.name}: ' + ' / '.join(chunk))
        print(f'  ✓ {p.relative_to(HERE)}  {" / ".join(chunk)}')
    with open(SHEET / 'index.txt', 'a', encoding='utf-8') as fh:
        fh.write('\n'.join(index) + '\n')
    return 0


# 🔴 機械で整えきれない撮影者名だけの例外表（短く保つ）
WHO_FIX = {
    'canary_iss_01': 'NASA ジョンソン宇宙センター',
}


def _who(r, name=None):
    """撮影者の表記を1行にする。

    🔴 2026-09-16（⑤b-1）**Commons の `Artist` はそのまま画面に出せない。**128点で7型あった：
       「No machine-readable author provided. 〇〇 assumed (based on copyright claims).」／
       「元の名.jpg : 〇〇 (1923-1990), uploaded by: 〇〇 derivative work: …」／
       「〇〇 from Malmö, Sweden」（Flickr の町と国）／「Unknown author Unknown author or not provided」／
       「User:〇〇」／生没年／URL。7本目は画面に「出典：Work of the United States Federal
       Government under the terms」と**権利の文の断片**が出ていた（⑤c'）。
    ⚠️ 「George from Spain」は Flickr の表示名そのものなので落とさない（町と国の**2語**のときだけ落とす）。
    """
    if name in WHO_FIX:
        return WHO_FIX[name]
    s = _plain(r.get('artist'))
    s = re.sub(r'https?://\S+', ' ', s)
    s = re.sub(r'^No machine-readable author provided\.\s*', '', s)
    s = re.sub(r'\s*assumed \(based on copyright claims\)\.?', '', s)
    s = re.sub(r'^[^:]+\.(?:jpe?g|png|tiff?)\s*:\s*', '', s, flags=re.I)
    s = re.sub(r',?\s*uploaded by:.*$', '', s)
    s = re.sub(r'\s*\(\d{4}\s*-\s*\d{4}\)', '', s)
    s = re.sub(r'\s+from\s+[^,]+,\s*[^,]+$', '', s)
    s = re.sub(r'^User:', '', s)
    s = re.sub(r'\s+', ' ', s).strip().strip('"“”').rstrip('。.').replace('"', '”')
    s = re.sub(r'^(.*?)\s+\1$', r'\1', s)
    if s.lower().startswith('unknown author') or s.lower() in ('', '[onbekend]', 'unknown', 'onbekend'):
        s = ''
    if not s and 'National Archives' in r.get('credit', ''):
        s = '米国国立公文書館'
    return s[:48]


def _kind(r):
    lic = r.get('lic', '')
    if lic.upper().startswith('CC0'):
        return 'CC0'
    if lic.lower().startswith('public domain') or lic.lower() in ('pd', 'no restrictions'):
        return 'PD'
    if lic.upper().startswith('CC BY'):
        return 'CC BY'
    return '?'


def _anefo(r):
    return 'anefo' in (r.get('desc', '') + r.get('title', '')).lower() or \
        '10648' in r.get('credit', '')


def credit_line(r, name=None):
    k, who = _kind(r), _who(r, name)
    if k == 'CC0' and _anefo(r):
        return '出典：オランダ国立公文書館（Anefo）／CC0'
    if k == 'CC0':
        return f"出典：ウィキメディア・コモンズ／撮影 {who or '不明'}／CC0"
    if k == 'PD':
        return f"出典：{who or 'ウィキメディア・コモンズ'}／パブリックドメイン"
    if k == 'CC BY':
        return f"出典：ウィキメディア・コモンズ／撮影 {who}／{r['lic']}"
    raise SystemExit(f"🔴 権利が読めない（fail closed）：{r.get('title')} … {r.get('lic')}")


def cmd_credits():
    db = _db()
    used = {}
    try:
        sys.path.insert(0, str(HERE / 'tools'))
        import cuts                                          # noqa: PLC0415
        for cid, s in sorted(cuts.SPEC.items()):
            p = s.get('photo') or ''
            if p.startswith('ep9/'):
                used.setdefault(Path(p).stem, []).append(cid)
    except Exception as e:                                   # noqa: BLE001
        print(f'⚠️ cuts を読めなかった（使うカットの欄は空になる）: {e}')
    ng = 0
    cred = {}
    for n in pick():
        r = db.get(n)
        if not r:
            print(f'🔴 {n}: 台帳に無い'); ng += 1; continue
        if _kind(r) == 'CC BY' and not _who(r, n):
            print(f'🔴 {n}: CC BY なのに撮影者が空'); ng += 1; continue
        cred[f'ep9/{n}.jpg'] = credit_line(r, n)
    rows = [TABLE_HEAD, '|---|---|---:|---|---|---|']
    for n in pick():
        r = db.get(n)
        if not r:
            rows.append(f'| `{n}` | 🔴 台帳に無い（黙って落とさずここで止める） |'); ng += 1; continue
        k = _kind(r)
        right = {'CC0': 'CC0', 'PD': 'PD（Public domain）'}.get(k, f"CC BY（{r['lic']}）")
        title = r['title'].replace('|', '／')
        rows.append(f"| `{n}` | {' '.join(used.get(n, []))} | {r.get('year') or '不明'} | {right} | "
                    f"{_who(r, n).replace('|', '／')} | {title} |")
    print('\n'.join(f'{k} … {v}' for k, v in cred.items()))
    print('\n' + '\n'.join(rows))
    if '--write' in sys.argv and not ng:
        (DEST / 'credits.json').write_text(json.dumps(cred, ensure_ascii=False, indent=1),
                                           encoding='utf-8')
        n_used = sum(1 for n in pick() if used.get(n))
        sec = [SECTION_HEAD, '',
               '**2026-09-16（⑤b-1）に実測した。**写真は `qa_out/ep9_assets.py` の `PICK` が正本で、'
               'この節は `python qa_out/ep9_assets.py credits --write` が**機械で書き出している**（手で書かない）。',
               '',
               f'### 1. 写真 {len(cred)}点 ── ウィキメディア・コモンズ（継承なし：CC0／PD／CC BY）',
               '',
               '⚠️ **CC BY は撮影者名が使用条件**。⑥の概要欄には、この表の「撮影者」をそのまま載せる。',
               '⚠️ **CC BY-SA・GFDL は1点も入れていない**（継承が動画全体に伝染する）。取得した権利表示で2回検査した。',
               '⚠️ `losrodeos_now_*` `laspalmas_now_*` は**現在の空港**、`fog_laguna_*` は**2025年のラ・ラグーナの山地**、'
               '`cockpit_747_*` `engine_747_*` の多くは**博物館の保存機**。副題で必ず名乗る'
               '（[[feedback-fallback-stills-must-match-the-era]]）。**門番は年の食い違いだけを見ていて、被写体の食い違いは見ない。**',
               f'⚠️ いま画面に出しているのは **{n_used}点**（`使うカット` が空の欄は候補として落としただけ。捨てていない）。',
               '', *rows, '']
        text = CREDITS.read_text(encoding='utf-8')
        i = text.find(SECTION_HEAD)
        text = (text[:i].rstrip('\n') if i >= 0 else text.rstrip('\n')) + '\n\n' + '\n'.join(sec)
        CREDITS.write_text(text, encoding='utf-8')
        print(f'\n✓ ref/ep9/credits.json {len(cred)}行 と ref/CREDITS.md の §テネリフェ（{len(rows) - 2}行）を書いた')
    return 1 if ng else 0


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    cmd, rest = sys.argv[1], sys.argv[2:]
    return dict(info=cmd_info, fetch=lambda: cmd_fetch(rest or None), check=cmd_check,
                panel=cmd_panel, sheet=lambda: cmd_sheet(rest), credits=cmd_credits)[cmd]()


if __name__ == '__main__':
    sys.exit(main())
