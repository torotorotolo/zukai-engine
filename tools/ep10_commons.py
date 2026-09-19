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


# 公共ヌリ第1類型の11点（②で取得ずみ。実体は ref/ep10/src/kogl/）。継承は無いが**実寸が小さい**
KOGL = {
    '2301030102': ('서초구민회관에 마련된 삼풍참사 사망자 합동분향소(1995.7)', 809, 534),
    '2301030104': ('삼풍백화점 사고 피해자를 찾는 벽보(1995.6)', 809, 534),
    '2301030105': ('붕괴현장에서 오열하는 유가족들(1995.6.29)', 809, 534),
    '2301030106': ('삼풍백화점 붕괴현장의 구조활동(1995.6)', 809, 534),
    '2301030107': ('삼풍백화점 붕괴현장 정리와 구조활동(1995.6)', 809, 534),
    '2301030108': ('건물 붕괴 충격으로 아수라장이 된 삼풍백화점 본관 1층 현관 가판대(1995.6)', 809, 534),
    '2301030109': ('처참한 모습을 드러낸 삼풍백화점 붕괴현장(1995.6.30)', 534, 809),
    '2301030481': ('4대 시의회 의장단 삼풍백화점 구조현장 방문(1995.7.12)', 1000, 657),
    '2301030508': ('시장 업무 인수 직후 삼풍백화점 현장을 찾은 조순 시장(1995.7.1)', 809, 534),
    '52399': ('삼풍백화점(붕괴전) 1995/6 · 01O01101Db8000', 1600, 1070),
    '52400': ('삼풍백화점(붕괴전) 1995/6 · 01O01102Db1000', 1600, 1070),
}
KOGL_SRC = {
    '5': dict(lic='KOGL Type 1', artist='서울역사편찬원',
              page='https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=%s&key=2211220005',
              credit='서울역사편찬원', file='ref/ep10/src/kogl/hs_%s_0.jpg'),
    '2': dict(lic='KOGL Type 1 + CC BY 4.0', artist='서울특별시／서울연구원',
              page='https://data.si.re.kr/node/%s',
              credit='서울 1995 도시형태와 경관, 서울특별시／서울연구데이터서비스(http://data.si.re.kr), 서울연구원',
              file='ref/ep10/src/kogl/sire_%s.jpg'),
}

# 欄 → [(出どころ, 番号/ID, 見せ方[, 注記])]。②で目で見て選んだ結果（→ ref/ep10/src/seen.tsv）。
#   'C'＝Commons（全部 CC BY-SA 4.0）→ 見せ方は **frame（額装）だけ**
#   'K'＝公共ヌリ第1類型（継承なし）→ 'free'（切り出しも**ぼかし**もできる）。⚠️ ただし 809px＝実際は額装向き
#
# 🔴🔴 判定の線（2026-09-20 カズヤくん決定。①の「見分けられる人物は使わない」を引き直した）:
#   ① 血・傷が見える負傷者／損傷のある遺体 → **使わない**（YouTube の広告ガイドラインで「広告収入が制限される」に明記）
#   ② 覆われた遺体・担架の搬送 → **遠景だけ**（YouTube 上は収益化できるが、遺族感情と ch の品位で絞る）
#   ③ 救助隊・軍・警察など**公的な任務の人の顔は使ってよい**（YouTube の規約には無い。ch の実名の線引きと同じ考え）
#   ④ 私人（遺族の顔）→ 使わない。行方不明者の掲示板は**ぼかして**使う（公共ヌリ第1類型＝手直しが許される）
#   ⚠️ 消防本部の但し書き「구별 가능한 특정 인물…승인」が説明欄にあるのは **239点中4点**（#178/#179/#181/#182）。
#      この4点だけは、人が識別できるかを1点ずつ見て決める（#182 は人物が極小なので可）
SLOTS = {
    # ── 崩壊前の建物（この2点しか無い）────────────────────────────
    'sampoong_before': [('K', '52399', 'free'), ('K', '52400', 'free')],
    # ── 「三豊百貨店」の看板が読める、残った建物 ───────────────────
    'sign_sampoong': [('C', 211, 'frame'), ('C', 227, 'frame')],
    # ── 俯瞰＝崩れた穴と残ったピンクの壁（崩壊の規模が分かる）─────────
    'wreck_aerial': [('C', 182, 'frame'), ('C', 212, 'frame'), ('C', 215, 'frame'),
                     ('C', 228, 'frame'), ('C', 236, 'frame'), ('C', 193, 'frame'),
                     ('C', 230, 'frame'), ('C', 239, 'frame')],
    # ── 地上から見た瓦礫と、崩れた建物の断面 ─────────────────────
    'wreck_ground': [('C', 189, 'frame'), ('C', 221, 'frame'), ('C', 224, 'frame'),
                     ('K', '2301030109', 'free')],
    # ── 折れた柱・むき出しの鉄筋（c5「柱は図面より細かった」の実物）──────
    'column_broken': [('C', 207, 'frame'), ('C', 219, 'frame')],
    # ── 瓦礫の上の捜索・作業（救助隊・軍・警察＝公的な任務の人）─────────
    'rescue_work': [('C', 187, 'frame'), ('C', 188, 'frame'), ('C', 192, 'frame'),
                    ('C', 194, 'frame'), ('C', 195, 'frame'), ('C', 196, 'frame'),
                    ('C', 198, 'frame'), ('C', 208, 'frame'), ('C', 213, 'frame'),
                    ('C', 216, 'frame'), ('C', 218, 'frame'), ('C', 220, 'frame'),
                    ('C', 225, 'frame'), ('C', 229, 'frame'), ('C', 231, 'frame'),
                    ('C', 233, 'frame'), ('C', 234, 'frame'), ('C', 235, 'frame'),
                    ('K', '2301030106', 'free')],
    # ── 救急車が列になって待っている（夜・昼）─────────────────────
    'ambulance_line': [('C', 203, 'frame'), ('C', 214, 'frame'), ('C', 201, 'frame'),
                       ('C', 209, 'frame'), ('C', 199, 'frame')],
    # ── 封鎖された道路と、遠くから見ている人たち ──────────────────
    'street_cordon': [('C', 210, 'frame')],
    # ── 炊き出し・物資を運ぶボランティア ───────────────────────
    'volunteers': [('C', 217, 'frame')],
    # ── 崩壊の衝撃で散乱した、1階の売り場 ───────────────────────
    'inside_store': [('K', '2301030108', 'free')],
    # ── 重機が並ぶ現場整理・回収した物の袋 ──────────────────────
    'site_cleanup': [('K', '2301030107', 'free'),
                     ('C', 222, 'frame', '⚠️ 大袋の中身は原本に書かれていない。副題で中身を断定しない')],
    # ── 合同焼香所（白菊と位牌の列）──────────────────────────
    'mourning': [('K', '2301030102', 'free')],
    # ── 行方不明者を探す掲示板（壁一面の張り紙）───────────────────
    'missing_board': [('K', '2301030104', 'free',
                       '🔴 顔写真と名前を**ぼかしてから**使う（私人。公共ヌリ第1類型は手直し可）')],
    # ── 現場に入った市長・市議会（行政の対応）────────────────────
    'officials_visit': [('K', '2301030508', 'free'), ('K', '2301030481', 'free')],
}


def cmd_slots():
    if not SLOTS:
        sys.exit('SLOTS が空')
    rows = {r['no']: r for r in _load()}
    # ⚠️ API は名前空間つきの題でないと imageinfo を返さない（付け忘れると w=0・sha1 空で
    #    「画素が差し替わっている」と全点で鳴る＝2026-09-20 に踏んだ）
    titles = sorted({'File:' + rows[i[1]]['title'] for v in SLOTS.values() for i in v if i[0] == 'C'})
    fresh = {r['title']: r for r in meta_full(titles)}
    out, bad = {}, []
    for slot, items in SLOTS.items():
        out[slot] = []
        for item in items:
            src, n, mode = item[:3]
            note = item[3] if len(item) > 3 else ''
            if src == 'K':
                t, w, h = KOGL[n]
                meta = KOGL_SRC['2' if len(n) < 8 else '5']
                f = meta['file'] % n
                if not os.path.exists(os.path.join(ROOT, f)):
                    bad.append(f'{slot} {n} の実体が無い（{f}）')
                out[slot].append(dict(no=n, mode=mode, note=note, share_alike=False, title=t, w=w, h=h,
                                      lic=meta['lic'], lic_url='https://www.kogl.or.kr/info/licenseType1.do',
                                      artist=meta['artist'], date='1995', url=f,
                                      page=meta['page'] % n, credit=meta['credit']))
                continue
            r = fresh[rows[n]['title']]
            if r['sha1'] != rows[n]['sha1']:
                bad.append(f'{slot} #{n} 画素が差し替わっている（sha1 が一覧と違う）')
            sa = bool(SA.search(r['lic']))
            if sa and mode != 'frame':
                bad.append(f'{slot} #{n} BY-SA なのに見せ方が {mode}（額装だけ）')
            out[slot].append(dict(no=n, mode=mode, note=note, share_alike=sa, **{k: r[k] for k in (
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
