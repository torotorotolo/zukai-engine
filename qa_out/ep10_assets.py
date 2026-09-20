# -*- coding: utf-8 -*-
"""ep10_assets.py — 10本目（三豊百貨店）の**写真の束**を作る（2026-09-20 ⑤b-1 新設）。

`qa_out/ep9_assets.py`（9本目）を写して直した。**権利の形がまるで違うので、中身は別物**。

■ 9本目との違い（ここを取り違えると権利の事故になる）
  | | 9本目 テネリフェ | 10本目 三豊百貨店 |
  |---|---|---|
  | 継承（ShareAlike） | **1点も入れない**（見つけたら落とす） | **82点が CC BY-SA 4.0**。額装でだけ使う |
  | 置き場 | 全点 Commons | **82点 Commons ＋ 10点 公共ヌリ（手元に取得ずみ）** |
  | 切り出し | する（`TRIM` 6点） | **BY-SA は切らない**。公共ヌリの10点だけ切れる |

■ 🔴🔴 CC BY-SA を落とさない理由（9本目とは逆の判断）
  継承は「**自分が作った翻案物を共有するとき**」だけ掛かる。無加工・丸ごと・独立した要素として
  動画に入れるなら、動画を BY-SA にしなくてよい（許諾 3(b)・1(a)・2(a)(4)、CC 公式の
  ShareAlike_interpretation。原文は `ref/ep10/materials.md` §1）。
  → [[reference-cc-by-sa-unmodified-in-video]]（2026-09-20 カズヤくん決定＝額装で進める）
  🔴 **「額装でだけ使う」は約束ではなく `cuts/ss.py` の `FRAME_ONLY` が機械で止める。**

■ 🔴 守っていること
  1. **②が記録した権利と、いま Commons が返す権利が食い違ったら止める**（fail closed）。
     ②から⑤bまでに付け替えられている可能性を、引き写さずに毎回当て直す。
     → [[feedback-verify-inherited-claims]]／[[feedback-gates-go-stale-when-upstream-changes]]
  2. **Commons に無い題名は黙って飛ばさず止める**（fail closed）。
  3. 公共ヌリの10点は**手元のファイルから実寸を測る**（json の w/h を信じない）。
  4. 撮影年は出典に出す。作れないものは「不明」（年を作らない）
     → [[feedback-fallback-stills-must-match-the-era]]
  5. 出力はファイルへ。`| tail` でつながない（[[feedback-pipes-mask-exit-codes]]）。
  6. 画素は **幅3,000px まで**（額装なので 1080 あれば足りるが、⑤c の原寸目視のために残す）。
     ⚠️ 縮小は許諾 2(a)(4) が「翻案を生まない」と明記しているので BY-SA でも可。

    python qa_out/ep10_assets.py info     # 権利・寸法・撮影者を引き直して ref/ep10/assets.json へ
    python qa_out/ep10_assets.py fetch    # ref/ep10/<名>.jpg に落とす（公共ヌリは手元から写す）
    python qa_out/ep10_assets.py check    # PICK・assets.json・ファイルの3つが揃っているか
    python qa_out/ep10_assets.py panel    # 切り落とし率の並び（PANEL_AR を決める材料）
    python qa_out/ep10_assets.py sheet [名の頭 ...]   # 640px のシート（2列×3行）
    python qa_out/ep10_assets.py credits [--write]    # credits.json と ref/CREDITS.md の表
"""
from __future__ import annotations

import io
import json
import re
import shutil
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine/1.0 (accident-documentary research; contact: konariri8@gmail.com)'
DEST = HERE / 'ref' / 'ep10'
DB = DEST / 'assets.json'
SLOTS_JSON = DEST / 'slots_commons.json'
SHEET = HERE / 'out' / 'ep10_sheet'
MAXW = 3000
CREDITS = HERE / 'ref' / 'CREDITS.md'
# 🔴 `tools/check_credits.py` の `HEADER` と**1字も違わない**こと（違えば門番は表を読めずに止まる）。
#    ⚠️ 9本目（Commons の題名）と最後の列を変えてある＝前の回の表を読まない
TABLE_HEAD = '| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 素材の題名 |'
SECTION_HEAD = '## 三豊百貨店崩壊事故（1995-06-29・10本目）'

# 撮影者の表記（画面に出す形）。🔴 **原語はハングル。画面は片仮名・表には原語も残す。**
#   個人名の読みは機械的な転写（최＝チェ／광＝グァン／모＝モ）。⚠️ 当人の名乗りではない。
WHO_JA = {
    '서울특별시 소방재난본부': 'ソウル特別市 消防災難本部',
    '서울역사편찬원': 'ソウル歴史編纂院',
    '서울특별시／서울연구원': 'ソウル特別市／ソウル研究院',
    '최광모': 'チェ・グァンモ',
}


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
    return {}


def _slots():
    return json.loads(SLOTS_JSON.read_text(encoding='utf-8'))['slots']


def pick():
    """名前 → ②の1点（`<欄>_<NN>`。②の並びのまま。手で付け直さない）。"""
    out = {}
    for slot, items in _slots().items():
        for i, it in enumerate(items, 1):
            out[f'{slot}_{i:02d}'] = it
    return out


def _plain(s):
    s = re.sub(r'<[^>]+>', ' ', str(s or ''))
    s = s.replace('&amp;', '&').replace('&quot;', '"').replace('&#039;', "'")
    return re.sub(r'\s+', ' ', s).strip()


def _year(date):
    m = re.search(r'(1[89]\d\d|20\d\d)', str(date or ''))
    return int(m.group(1)) if m else None


# 🔴🔴 2026-09-20（⑤b-1）**日付の欄は撮影時刻ではない。**
#    消防災難本部の32点は `DateTimeOriginal` が**全部おなじ「1995-06-29 15:09:25」**だった。
#    崩壊は **17時55分ごろ**なので、崩れたあとの写真がこの時刻に撮れるはずがない
#    ＝まとめて入れられた値（事故の日そのもの）で、**その写真が撮られた時刻ではない**。
#    しかも②の目視では `rescue_work_05` に「'95 7 3」が焼き込まれている＝**7月の写真**がある。
#    → [[feedback-inventory-is-not-usable-material]]（取り込みの年が混じる型の、時刻版）
#    ⚠️ **年（1995）は正しい**（題名 `19950629…`・分類・被写体が一致）。**日は名乗らない。**
BULK_STAMP = '1995-06-29 15:09:25'
# 최광모 の40点は `DateTimeOriginal` も題名も日付を持たない（題名は `SampungdeptNN.jpg`、
# 説明は "Sampoong Department Store Collapse" だけ）。**被写体がこの事故そのもの**なので
# 年は 1995 と書けるが、**根拠は日付欄ではない**。どちらの根拠かを `year_src` に残す。
EVENT_YEAR = 1995


def _norm_lic(s):
    """許諾名を突き合わせ用にそろえる（`CC BY-SA 4.0` と `CC BY-SA 4.0 International`）。"""
    s = _plain(s).upper().replace('-', ' ').replace('_', ' ')
    s = re.sub(r'\bINTERNATIONAL\b|\bDEED\b', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def cmd_info():
    """Commons の82点を引き直し、公共ヌリの10点は手元のファイルを測る。"""
    from PIL import Image
    pk = pick()
    rows, bad = {}, []
    commons = {n: it for n, it in pk.items() if it.get('mode') == 'frame'}
    local = {n: it for n, it in pk.items() if it.get('mode') != 'frame'}

    names = list(commons)
    for i in range(0, len(names), 40):
        chunk = names[i:i + 40]
        d = q({'action': 'query',
               'titles': '|'.join('File:' + commons[n]['title'] for n in chunk),
               'prop': 'imageinfo', 'iiprop': 'url|size|mime|extmetadata',
               'iiurlwidth': str(MAXW),
               'iiextmetadatafilter': 'DateTimeOriginal|LicenseShortName|LicenseUrl|'
                                      'ImageDescription|Artist|Credit'})
        norm = {x['from']: x['to'] for x in d['query'].get('normalized', [])}
        pages = {p['title']: p for p in d['query']['pages']}
        for n in chunk:
            it = commons[n]
            t = 'File:' + it['title']
            p = pages.get(norm.get(t, t))
            if not p or p.get('missing') or not p.get('imageinfo'):
                bad.append((n, it['title'], 'Commons に無い（fail closed）'))
                continue
            ii = p['imageinfo'][0]
            em = ii.get('extmetadata', {}) or {}
            g = lambda k: _plain((em.get(k, {}) or {}).get('value', ''))    # noqa: E731
            lic = g('LicenseShortName')
            # 🔴 ②が記録した権利と食い違ったら止める（引き写さない）
            if _norm_lic(lic) != _norm_lic(it['lic']):
                bad.append((n, it['title'], f"権利が②と違う：② {it['lic']} → いま {lic}"))
                continue
            rows[n] = dict(src='commons', title=it['title'], slot=n.rsplit('_', 1)[0],
                           mode=it.get('mode'), share_alike=bool(it.get('share_alike')),
                           w=ii['width'], h=ii['height'], mime=ii['mime'],
                           url=ii['url'], thumb=ii.get('thumburl'), page=ii.get('descriptionurl'),
                           lic=lic, lic_url=g('LicenseUrl') or it.get('lic_url', ''),
                           artist=_plain(g('Artist')) or _plain(it.get('artist')),
                           credit=g('Credit'), date=g('DateTimeOriginal') or it.get('date'),
                           year=_year(g('DateTimeOriginal') or it.get('date')) or EVENT_YEAR,
                           year_src=('日付欄' if _year(g('DateTimeOriginal') or it.get('date'))
                                     else '被写体（この事故の記録）'),
                           date_ok=(g('DateTimeOriginal') or '').strip() != BULK_STAMP,
                           desc=g('ImageDescription')[:400], note=it.get('note', ''))
        time.sleep(0.5)

    for n, it in local.items():
        f = HERE / it['url'] if not Path(it['url']).is_absolute() else Path(it['url'])
        if not f.exists():
            bad.append((n, it['title'], f'手元のファイルが無い（fail closed）: {it["url"]}'))
            continue
        with Image.open(f) as im:
            w, h = im.size                      # 🔴 json の w/h ではなく実物を測る
        rows[n] = dict(src='kogl', title=it['title'], slot=n.rsplit('_', 1)[0],
                       mode=it.get('mode'), share_alike=bool(it.get('share_alike')),
                       w=w, h=h, mime='image/jpeg', url=it['url'], thumb=None,
                       page=it.get('page', ''), lic=it['lic'], lic_url=it.get('lic_url', ''),
                       artist=_plain(it.get('artist')), credit=_plain(it.get('credit')),
                       date=it.get('date'), year=_year(it.get('date')) or EVENT_YEAR,
                       year_src=('日付欄' if _year(it.get('date')) else '被写体（この事故の記録）'),
                       date_ok=True,
                       desc='', note=it.get('note', ''))
        if (w, h) != (it['w'], it['h']):
            print(f'⚠️ {n}: ②の寸法 {it["w"]}x{it["h"]} と実物 {w}x{h} が違う（実物を採った）')

    DB.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    sa = sum(1 for r in rows.values() if r['share_alike'])
    print(f'PICK {len(pk)} ／ 引けた {len(rows)}（Commons {len(commons)} ＋ 公共ヌリ {len(local)}）'
          f' ／ 止めた {len(bad)}')
    print(f'  うち継承あり（額装だけ） {sa}点 ／ 手直し可 {len(rows) - sa}点')
    bulk = [n for n, r in rows.items() if not r.get('date_ok')]
    ev = [n for n, r in rows.items() if r.get('year_src') != '日付欄']
    print(f'🔴 日付欄が一括の値（{BULK_STAMP}）＝撮影時刻ではない: {len(bulk)}点')
    print(f'🔴 年の根拠が日付欄でなく被写体: {len(ev)}点（年は {EVENT_YEAR} でよいが**日は名乗らない**）')
    for n, t, why in bad:
        print(f'🔴 {n}: {why} … {t}')
    return 1 if bad else 0


def _db():
    if not DB.exists():
        raise SystemExit('🔴 ref/ep10/assets.json が無い。まず info')
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
        try:
            if r['src'] == 'kogl':
                src = HERE / r['url'] if not Path(r['url']).is_absolute() else Path(r['url'])
                data = src.read_bytes()
            else:
                url = r['thumb'] if (r['w'] > MAXW and r.get('thumb')) else r['url']
                data = _get(url)
            im = Image.open(io.BytesIO(data))
            im.load()
            if im.mode != 'RGB':
                im = im.convert('RGB')
            if im.width > MAXW:
                im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
            im.save(out, quality=92)
            print(f'✓ {n:<24} {im.width}x{im.height}  {out.stat().st_size / 1024:7.0f} KB')
            ok += 1
        except Exception as e:                              # noqa: BLE001
            print(f'🔴 {n}: {e}')
            err += 1
        if r['src'] != 'kogl':
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
            print(f'⚠️ {n}: {w}x{h}（長い辺も1280未満＝額装でも小さい）')
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
            for k in range(1, 4):                # 0.25 刻みの格子（主題の位置を言うため）
                x, y = im.width * k / 4, im.height * k / 4
                d.line([(x, 0), (x, im.height)], fill=(255, 60, 60), width=1)
                d.line([(0, y), (im.width, y)], fill=(255, 60, 60), width=1)
            x0, y0 = (i % COLS) * TW, (i // COLS) * (TH + BAR)
            sh.paste(im, (x0 + (TW - im.width) // 2, y0 + BAR + (TH - im.height) // 2))
            r = db.get(n, {})
            tag = 'SA' if r.get('share_alike') else 'free'
            dd.text((x0 + 6, y0 + 5), f"{n}  {sw}x{shh}  {r.get('year') or '?'}  {tag}",
                    fill=(255, 220, 120))
        tag = (pats[0].rstrip('_') if pats else 'all')
        p = SHEET / f'{tag}_{page + 1:02d}.jpg'
        sh.save(p, quality=88)
        index.append(f'{p.name}: ' + ' / '.join(chunk))
        print(f'  ✓ {p.relative_to(HERE)}  {" / ".join(chunk)}')
    with open(SHEET / 'index.txt', 'a', encoding='utf-8') as fh:
        fh.write('\n'.join(index) + '\n')
    return 0


def _who(r):
    """撮影者の表記（画面に出す形）。読めなければ**止める**（CC BY-SA は氏名表示が条件）。"""
    s = _plain(r.get('artist'))
    s = re.sub(r'https?://\S+', ' ', s)
    s = re.sub(r'^No machine-readable author provided\.\s*', '', s)
    s = re.sub(r'\s*assumed \(based on copyright claims\)\.?', '', s)
    s = re.sub(r'^User:', '', s).strip()
    # 括弧つきの英語併記（「…본부(Seoul Metropolitan Fire & Disaster Headquarters)」）を落とす
    s = re.sub(r'\s*\([A-Za-z][^)]*\)\s*$', '', s).strip()
    return WHO_JA.get(s, s)


def credit_line(r):
    """画面の隅に出す1行。⚠️ **許諾のURL・素材のURLは概要欄の表で出す**（画面には入らない）。"""
    who = _who(r)
    if not who:
        raise SystemExit(f"🔴 撮影者が読めない（fail closed）：{r.get('title')}")
    if r['share_alike']:
        # 🔴 BY-SA は「改変していないこと」の表示も条件。だから「無改変」を入れる
        return f'出典：{who}／CC BY-SA 4.0（無改変）'
    if 'KOGL' in r['lic'].upper() or '공공누리' in r['lic']:
        # ⚠️ `sampoong_before_01` `_02` は **公共ヌリ第1類型 ＋ CC BY 4.0 の二重表示**。
        #    CC BY も氏名表示が条件なので、**許諾名を両方出す**（片方に丸めない）。
        if 'CC BY' in r['lic'].upper():
            return f'出典：{who}／公共ヌリ 第1類型・CC BY 4.0'
        return f'出典：{who}／公共ヌリ 第1類型'
    raise SystemExit(f"🔴 権利が読めない（fail closed）：{r.get('title')} … {r.get('lic')}")


def cmd_credits():
    db = _db()
    used = {}
    try:
        sys.path.insert(0, str(HERE / 'tools'))
        import cuts                                          # noqa: PLC0415
        for cid, s in sorted(cuts.SPEC.items()):
            p = s.get('photo') or ''
            if p.startswith('ep10/'):
                used.setdefault(Path(p).stem, []).append(cid)
    except Exception as e:                                   # noqa: BLE001
        print(f'⚠️ cuts を読めなかった（使うカットの欄は空になる）: {e}')
    ng = 0
    cred = {}
    for n in pick():
        r = db.get(n)
        if not r:
            print(f'🔴 {n}: 台帳に無い'); ng += 1; continue
        cred[f'ep10/{n}.jpg'] = credit_line(r)
    rows = [TABLE_HEAD, '|---|---|---:|---|---|---|']
    for n in pick():
        r = db.get(n)
        if not r:
            rows.append(f'| `{n}` | 🔴 台帳に無い（黙って落とさずここで止める） |'); ng += 1; continue
        right = (f"CC BY-SA 4.0（額装のみ・無改変）" if r['share_alike']
                 else f"{r['lic']}（手直し可）")
        title = r['title'].replace('|', '／')
        rows.append(f"| `{n}` | {' '.join(used.get(n, []))} | {r.get('year') or '不明'} | {right} | "
                    f"{_who(r).replace('|', '／')} | {title} |")
    print('\n'.join(f'{k} … {v}' for k, v in cred.items()))
    print('\n' + '\n'.join(rows))
    if '--write' in sys.argv and not ng:
        (DEST / 'credits.json').write_text(json.dumps(cred, ensure_ascii=False, indent=1),
                                           encoding='utf-8')
        n_used = sum(1 for n in pick() if used.get(n))
        sa = sum(1 for r in db.values() if r['share_alike'])
        sec = [SECTION_HEAD, '',
               '**2026-09-20（⑤b-1）に実測した。**写真は `qa_out/ep10_assets.py` が正本で、'
               'この節は `python qa_out/ep10_assets.py credits --write` が**機械で書き出している**（手で書かない）。',
               '',
               f'### 1. 写真 {len(cred)}点（CC BY-SA 4.0 {sa}点 ／ 公共ヌリ第1類型 {len(cred) - sa}点）',
               '',
               '🔴🔴 **CC BY-SA の点は額装でだけ使っている**（無加工・丸ごと・色を変えない・何も重ねない）。',
               '　　継承は翻案物を共有するときだけ掛かるので、**動画を BY-SA にする必要はない**',
               '　　（許諾 3(b)・1(a)・2(a)(4)／CC 公式 ShareAlike_interpretation。'
               '`ref/ep10/materials.md` §1 に原文）。',
               '　　⚠️ 切る・色を変える・上に重ねると翻案になる。**止める仕掛け＝`cuts/ss.py` の `FRAME_ONLY`**。',
               '⚠️ **BY-SA の表示に要るのは4つ**＝撮影者・許諾名と URL・素材の URL・**改変していないこと**。',
               '　　画面の隅には「出典：撮影者／CC BY-SA 4.0（無改変）」だけを出し、'
               'URL はこの表と⑥の概要欄で出す。',
               '⚠️ 撮影者名の原語はハングル。画面は片仮名にしている（`WHO_JA`）。'
               '個人名の読みは機械的な転写で、当人の名乗りではない。',
               f'⚠️ いま画面に出しているのは **{n_used}点**（`使うカット` が空の欄は候補として落としただけ。捨てていない）。',
               '', *rows, '']
        text = CREDITS.read_text(encoding='utf-8')
        i = text.find(SECTION_HEAD)
        text = (text[:i].rstrip('\n') if i >= 0 else text.rstrip('\n')) + '\n\n' + '\n'.join(sec)
        CREDITS.write_text(text, encoding='utf-8')
        print(f'\n✓ ref/ep10/credits.json {len(cred)}行 と '
              f'ref/CREDITS.md の §三豊百貨店（{len(rows) - 2}行）を書いた')
    return 1 if ng else 0


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    cmd, rest = sys.argv[1], sys.argv[2:]
    rest = [a for a in rest if not a.startswith('--')]
    try:
        fn = dict(info=cmd_info, fetch=lambda: cmd_fetch(rest or None), check=cmd_check,
                  panel=cmd_panel, sheet=lambda: cmd_sheet(rest), credits=cmd_credits)[cmd]
    except KeyError:
        print(f'🔴 知らない指図です: {cmd}'); return 2
    return fn()


if __name__ == '__main__':
    sys.exit(main())
