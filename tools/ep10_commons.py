# -*- coding: utf-8 -*-
"""ep10_commons.py — 10本目 三豊百貨店の Commons 写真（CC BY-SA 4.0）を②で選ぶ道具（2026-09-20）。

■ なぜ要るか
    ①で「事故の年 239点」まで絞った（ref/ep10/materials.md §2）。②では**写真の中身で**選ぶ。
    `commons_catlist.py` は BY-SA を「使わない」扱いにして上位40点しか出さないので、10本目には使えない。
    🔴 10本目は BY-SA を**額装**（無加工・丸ごと・色を変えない・何も重ねない）で使う（2026-09-20 カズヤくん決定）。
    → 継承の有無ではなく **額装で持つか（frame）／全画面・切り出しもできるか（free）** を欄ごとに持たせる。

■ サブコマンド
    list    分類を歩いて全点のメタデータを ref/ep10/src/commons_all.json へ（事故の年に印 y95）
    fetch   事故の年の点の 640px 版を ref/ep10/src/commons_640/NNN.jpg へ（NNN＝一覧の番号）
    dup     画素で近い組（dHash）を出す。同じ場面の連写を1組に畳むため
    sheet   2列×3行・1コマ幅640px のシートを out/ep10_sheets/ へ（事故検証chの例外＝640px 以上のシート）
    slots   SLOTS（②で目で選んだ結果）を ref/ep10/slots_commons.json に確定。許諾をもう一度取って検査する

■ 事故の年の決め方（①と同じ）
    DateTimeOriginal の年が 1995、または日付が無く題が `Sampungdept` で始まる（최광모の53点）。
    ⚠️ 「2000년대 초반 서울소방…삼풍」の10点は日付欄・EXIF が 2001年＝1995年と言えないので入れない。

■ 使い方
    PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python tools/ep10_commons.py list|fetch|dup|sheet|slots
"""
import io, json, os, re, sys, time, urllib.parse, urllib.request
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from commons_catlist import q, walk, files_of, UA  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'ref', 'ep10', 'src')
ALL = os.path.join(SRC, 'commons_all.json')
THUMBS = os.path.join(SRC, 'commons_640')
SHEETS = os.path.join(ROOT, 'out', 'ep10_sheets')
SLOTS_OUT = os.path.join(ROOT, 'ref', 'ep10', 'slots_commons.json')
CAT = 'Category:Sampoong Department Store collapse'
SA = re.compile(r'\bSA\b|share[- ]?alike|GFDL', re.I)


def _clean(s):
    s = re.sub('<[^>]+>', ' ', str(s or ''))
    return re.sub(r'\s+', ' ', s).strip()


def meta_full(titles):
    rows = []
    for i in range(0, len(titles), 40):
        d = q({'action': 'query', 'titles': '|'.join(titles[i:i + 40]), 'prop': 'imageinfo|categories',
               'iiprop': 'url|size|mime|sha1|extmetadata', 'iiurlwidth': '640', 'cllimit': '500',
               'iiextmetadatafilter': 'DateTimeOriginal|LicenseShortName|LicenseUrl|ImageDescription|Artist|Credit|ObjectName'})
        for p in d.get('query', {}).get('pages', []):
            ii = (p.get('imageinfo') or [{}])[0]
            em = ii.get('extmetadata', {}) or {}
            g = lambda k: str((em.get(k, {}) or {}).get('value', ''))
            date = _clean(g('DateTimeOriginal'))
            m = re.search(r'(1[89]\d\d|20\d\d)', date)
            rows.append({
                'title': p['title'].replace('File:', ''),
                'w': ii.get('width', 0), 'h': ii.get('height', 0), 'mime': ii.get('mime', ''),
                'sha1': ii.get('sha1', ''), 'date': date, 'year': m.group(1) if m else '',
                'lic': _clean(g('LicenseShortName')), 'lic_url': _clean(g('LicenseUrl')),
                'artist': _clean(g('Artist')), 'credit': _clean(g('Credit')),
                'desc': _clean(g('ImageDescription')),
                'cats': [c['title'].replace('Category:', '') for c in p.get('categories', [])],
                'url': ii.get('url', ''), 'thumb': ii.get('thumburl', ''),
                'page': ii.get('descriptionurl', ''),
            })
        time.sleep(0.5)
    return rows


def is_y95(r):
    return r['year'] == '1995' or (r['year'] == '' and r['title'].startswith('Sampungdept'))


def cmd_list():
    cats = walk(CAT, 1)
    titles = files_of(cats)
    rows = meta_full(titles)
    rows.sort(key=lambda r: r['title'])
    y95 = [r for r in rows if is_y95(r)]
    for n, r in enumerate(y95, 1):
        r['no'] = n
    for r in rows:
        r['y95'] = is_y95(r)
    os.makedirs(SRC, exist_ok=True)
    json.dump({'measured': time.strftime('%Y-%m-%d'), 'cats': cats, 'files': rows},
              open(ALL, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'分類 {len(cats)} / ファイル {len(rows)} / 事故の年 {len(y95)}')
    print('許諾', dict(Counter(r['lic'] for r in rows)))
    print('事故の年の許諾', dict(Counter(r['lic'] for r in y95)))
    print('年', dict(Counter(r['year'] or '-' for r in rows)))
    print('撮影者', dict(Counter(r['artist'][:30] for r in y95).most_common(6)))
    ws = [r['w'] for r in y95]
    print('幅 1920以上', sum(w >= 1920 for w in ws), '/ 1280以上', sum(w >= 1280 for w in ws),
          '/ 1000〜1279', sum(1000 <= w < 1280 for w in ws), '/ 800〜999', sum(800 <= w < 1000 for w in ws),
          '/ 800未満', sum(w < 800 for w in ws))
    print('高さ870以上', sum(r['h'] >= 870 for r in y95), '/ 縦長', sum(r['h'] > r['w'] for r in y95))
    print('SA でない（継承なし）', [r['title'] for r in y95 if not SA.search(r['lic'])])


def _load():
    d = json.load(open(ALL, encoding='utf-8'))
    return [r for r in d['files'] if r.get('y95')]


def cmd_fetch():
    os.makedirs(THUMBS, exist_ok=True)
    rows, got, skip, bad = _load(), 0, 0, []
    for r in rows:
        fn = os.path.join(THUMBS, f"{r['no']:03d}.jpg")
        if os.path.exists(fn) and os.path.getsize(fn) > 1000:
            skip += 1
            continue
        for i in range(4):
            try:
                req = urllib.request.Request(r['thumb'], headers={'User-Agent': UA})
                data = urllib.request.urlopen(req, timeout=90).read()
                open(fn, 'wb').write(data)
                got += 1
                break
            except Exception as e:
                if i == 3:
                    bad.append((r['no'], str(e)[:80]))
                time.sleep(3 * (i + 1))
        time.sleep(0.3)
    print(f'取得 {got} / 既存 {skip} / 失敗 {len(bad)}  → {THUMBS}')
    for b in bad:
        print('  失敗', b)
    if bad:
        sys.exit(1)


def _dhash(fn, size=8):
    from PIL import Image
    im = Image.open(fn).convert('L').resize((size + 1, size), Image.LANCZOS)
    px = list(im.getdata())
    bits = 0
    for y in range(size):
        for x in range(size):
            bits = (bits << 1) | (px[y * (size + 1) + x] > px[y * (size + 1) + x + 1])
    return bits


def groups(th=10):
    rows = _load()
    hs = {r['no']: _dhash(os.path.join(THUMBS, f"{r['no']:03d}.jpg")) for r in rows}
    parent = {n: n for n in hs}

    def f(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    ns = sorted(hs)
    for i, a in enumerate(ns):
        for b in ns[i + 1:]:
            if bin(hs[a] ^ hs[b]).count('1') <= th:
                parent[f(b)] = f(a)
    g = {}
    for n in ns:
        g.setdefault(f(n), []).append(n)
    return [v for v in g.values() if len(v) > 1]


def cmd_dup():
    th = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    gs = groups(th)
    print(f'dHash のハミング距離 {th} 以下で組になったもの {len(gs)}組 / {sum(len(x) for x in gs)}点')
    for x in gs:
        print('  ', x)


def cmd_sheet():
    """引数＝番号の並び（例 1-6,9,12）。省略＝事故の年の全点。6点ずつ1枚。"""
    from PIL import Image, ImageDraw, ImageFont
    rows = {r['no']: r for r in _load()}
    if len(sys.argv) > 2:
        want = []
        for part in sys.argv[2].split(','):
            a, _, b = part.partition('-')
            want += list(range(int(a), int(b) + 1)) if b else [int(a)]
    else:
        want = sorted(rows)
    tag = sys.argv[3] if len(sys.argv) > 3 else 'all'
    os.makedirs(SHEETS, exist_ok=True)
    CW, CH, LH = 640, 480, 34
    font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 20)
    outs = []
    for s in range(0, len(want), 6):
        chunk = want[s:s + 6]
        sheet = Image.new('RGB', (CW * 2 + 12, (CH + LH) * 3 + 8), (40, 40, 40))
        dr = ImageDraw.Draw(sheet)
        for k, n in enumerate(chunk):
            r = rows[n]
            im = Image.open(os.path.join(THUMBS, f'{n:03d}.jpg')).convert('RGB')
            sc = min(CW / im.width, CH / im.height)  # 640 版を縮めない（640 の枠に収まる向きだけ縮む）
            im = im.resize((max(1, round(im.width * sc)), max(1, round(im.height * sc))), Image.LANCZOS)
            x0 = (k % 2) * (CW + 12)
            y0 = (k // 2) * (CH + LH) + 4
            sheet.paste(im, (x0 + (CW - im.width) // 2, y0 + (CH - im.height) // 2))
            lab = f"#{n:03d}  {r['w']}x{r['h']}  {r['title'][:40]}"
            dr.text((x0 + 6, y0 + CH + 4), lab, fill=(255, 255, 0), font=font)
        fn = os.path.join(SHEETS, f'{tag}_{s // 6 + 1:02d}.jpg')
        sheet.save(fn, quality=92)
        outs.append(fn)
    print(f'シート {len(outs)}枚 → {SHEETS}')
    for o in outs:
        print('  ', os.path.basename(o))


# 欄 → [(番号, 見せ方)]。②で目で選んだ結果を入れる（'frame'＝額装だけ）。空のうちは slots を呼ばない
SLOTS = {}


def cmd_slots():
    if not SLOTS:
        sys.exit('SLOTS が空')
    rows = {r['no']: r for r in _load()}
    titles = sorted({rows[n]['title'] for v in SLOTS.values() for n, _ in v})
    fresh = {r['title']: r for r in meta_full(titles)}
    out, bad = {}, []
    for slot, items in SLOTS.items():
        out[slot] = []
        for n, mode in items:
            r = fresh[rows[n]['title']]
            if r['sha1'] != rows[n]['sha1']:
                bad.append(f'{slot} #{n} 画素が差し替わっている（sha1 が一覧と違う）')
            sa = bool(SA.search(r['lic']))
            if sa and mode != 'frame':
                bad.append(f'{slot} #{n} BY-SA なのに見せ方が {mode}（額装だけ）')
            out[slot].append(dict(no=n, mode=mode, share_alike=sa, **{k: r[k] for k in (
                'title', 'w', 'h', 'lic', 'lic_url', 'artist', 'date', 'url', 'page')}))
    n_all = sum(len(v) for v in out.values())
    json.dump({'measured': time.strftime('%Y-%m-%d'), 'episode': 10, 'theme': '三豊百貨店崩壊事故',
               'note': 'CC BY-SA 4.0 は額装（無加工・丸ごと・色を変えない・何も重ねない）でだけ使う（2026-09-20 カズヤくん決定）。'
                       'mode=frame の点を切る・寄せる・暗くする・上に札を置く型に渡したら⑤bの門番で止める。',
               'total': n_all, 'slots': out, 'problems': bad},
              open(SLOTS_OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'欄 {len(out)} / 点 {n_all} → {SLOTS_OUT}')
    for b in bad:
        print('  🔴', b)
    if bad:
        sys.exit(1)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    {'list': cmd_list, 'fetch': cmd_fetch, 'dup': cmd_dup, 'sheet': cmd_sheet, 'slots': cmd_slots}.get(
        cmd, lambda: sys.exit(__doc__))()
