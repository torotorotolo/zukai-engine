# -*- coding: utf-8 -*-
"""commons_year_probe.py — ①題材用の網：Commons を歩いて **撮影年で割る**（2026-09-16）。

■ なぜ要るか
    `commons_probe.py` は「幅1280以上・PD が何点か」までは出すが、**撮影年を見ない**。
    カテゴリの点数は **在庫であって素材ではない**（→[[feedback-inventory-is-not-usable-material]]）。
    9本目の①で、年で割ったら見立てが3件とも動いた：
        TWA800             84点 → **1996年は13点**（下方修正・却下へ）
        テネリフェ         75点 → **1977年に33点**（上方修正・最大 5052x4360）
        ディープウォーター 614点 → **2010年4月は17点**（残りは流出後の清掃）

■ 🔴 道具の検算（陽性対照）
    帳簿に記録のある TWA800 を測り、**「動く映像1本・654x480・幅1280以上0本」**を
    再現できることを見る。再現しなければ道具を疑う（→[[feedback-verify-your-own-instrument]]）。
        python tools/commons_year_probe.py qa_out/ctrl_twa800.txt 2 1996 "Category:TWA Flight 800 (1996)"

■ 数え方
    - **CC0 は継承が無いので PD と同じ枠で数える**（UsageTerms に "public domain" が入る）。
      ⚠️ **CC BY-SA だけが危険**（継承が動画全体に波及する）
    - 動く映像（mime が video/*）は写真と別の軸で数える
      （【映像あり】が名乗れるかは**幅1280以上の動く映像が何本あるか**で決まる）
    - 窓は**前方一致**。"2010" は 2010-04 も 2010-?? も拾う

■ 使い方
    python tools/commons_year_probe.py <出力ファイル> <深さ> <窓> <カテゴリ...>
    例) python tools/commons_year_probe.py qa_out/tnf.txt 1 1977 "Category:Tenerife airport disaster"
    ⚠️ 出力先は**呼ぶ側が必ず明示する**（→[[feedback-external-tools-wipe-their-output-dir]]）
"""
import json, sys, re, time, urllib.parse, urllib.request
from collections import Counter, defaultdict

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine/1.0 (theme research; contact: konariri8@gmail.com)'


def q(params):
    params = dict(params, format='json', formatversion='2')
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(API, data=data, headers={'User-Agent': UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if i == 3:
                raise
            time.sleep(2 * (i + 1))


def subcats(cat, depth):
    seen, out, frontier = {cat}, [cat], [cat]
    for _ in range(depth):
        nxt = []
        for c in frontier:
            cont = {}
            while True:
                d = q(dict({'action': 'query', 'list': 'categorymembers', 'cmtitle': c,
                            'cmtype': 'subcat', 'cmlimit': '500'}, **cont))
                for m in d.get('query', {}).get('categorymembers', []):
                    if m['title'] not in seen:
                        seen.add(m['title']); out.append(m['title']); nxt.append(m['title'])
                if 'continue' in d:
                    cont = d['continue']
                else:
                    break
        frontier = nxt
        if not frontier:
            break
    return out


DATE_RE = re.compile(r'(\d{4})[-:/]?(\d{2})?')


def walk(cats, cap=4000):
    rows, seen = [], set()
    for c in cats:
        cont = {}
        while True:
            d = q(dict({'action': 'query', 'generator': 'categorymembers', 'gcmtitle': c,
                        'gcmtype': 'file', 'gcmlimit': '200', 'prop': 'imageinfo',
                        'iiprop': 'size|mime|extmetadata',
                        'iiextmetadatafilter': 'DateTimeOriginal|DateTime|LicenseShortName|UsageTerms'}, **cont))
            for p in d.get('query', {}).get('pages', []) or []:
                t = p.get('title')
                if t in seen:
                    continue
                seen.add(t)
                ii = (p.get('imageinfo') or [{}])[0]
                em = ii.get('extmetadata') or {}
                raw = (em.get('DateTimeOriginal') or em.get('DateTime') or {}).get('value') or ''
                raw = re.sub(r'<[^>]+>', ' ', raw)
                m = DATE_RE.search(raw)
                ym = (m.group(1) + '-' + (m.group(2) or '??')) if m else '????-??'
                rows.append({
                    'title': t, 'w': ii.get('width'), 'h': ii.get('height'),
                    'mime': ii.get('mime', ''),
                    'lic': (em.get('LicenseShortName') or {}).get('value', ''),
                    'terms': (em.get('UsageTerms') or {}).get('value', ''),
                    'ym': ym, 'raw': raw.strip()[:40],
                })
                if len(rows) >= cap:
                    return rows
            if 'continue' in d:
                cont = d['continue']
            else:
                break
    return rows


def is_pd(r):
    s = (r['lic'] + ' ' + r['terms']).lower()
    return ('public domain' in s) or s.strip() in ('pd', 'pd-usgov')


def main():
    outpath = sys.argv[1]
    depth = int(sys.argv[2])
    window = sys.argv[3]          # 例 2010-04,2010-05  ＝ 事故の窓
    cats_in = sys.argv[4:]
    win = tuple(window.split(','))   # 前方一致（"2010" は 2010-04 も 2010-?? も拾う）

    def inwindow(r):
        return r['ym'].startswith(win)

    lines = []
    allcats = []
    for c in cats_in:
        allcats += subcats(c, depth)
    allcats = list(dict.fromkeys(allcats))
    lines.append('カテゴリ %d 個' % len(allcats))
    rows = walk(allcats)
    lines.append('ファイル %d 点' % len(rows))

    vids = [r for r in rows if str(r['mime']).startswith('video')]
    photos = [r for r in rows if str(r['mime']).startswith('image')]

    def big(r):
        return (r['w'] or 0) >= 1280

    lines.append('')
    lines.append('== 動く映像 %d 本（うち幅1280以上 %d 本）==' % (len(vids), len([v for v in vids if big(v)])))
    for v in sorted(vids, key=lambda r: -(r['w'] or 0)):
        lines.append('  %sx%s %-28s %s | %s | %s' % (v['w'], v['h'], (v['lic'] or '?')[:28], v['ym'], v['title'][5:85], 'PD' if is_pd(v) else '--'))

    lines.append('')
    lines.append('== 写真：年月ごと（幅1280以上・PD だけ）==')
    cnt = Counter(r['ym'] for r in photos if big(r) and is_pd(r))
    for ym, n in sorted(cnt.items()):
        mark = ' ★事故の窓' if ym.startswith(win) else ''
        lines.append('  %-9s %4d%s' % (ym, n, mark))

    inwin = [r for r in photos if big(r) and is_pd(r) and inwindow(r)]
    lines.append('')
    lines.append('🔴 事故の窓（%s）の 幅1280以上・PD 写真 = %d 点' % (window, len(inwin)))
    lines.append('   ライセンス内訳(全体) %s' % dict(Counter((r['lic'] or '?')[:24] for r in photos).most_common(8)))
    lines.append('')
    lines.append('== 事故の窓の一覧（最大120件・題を1行ずつ読む用）==')
    for r in sorted(inwin, key=lambda r: -(r['w'] or 0))[:120]:
        lines.append('  %5sx%-5s %s | %s' % (r['w'], r['h'], r['ym'], r['title'][5:100]))

    open(outpath, 'w', encoding='utf-8').write('\n'.join(lines))
    print('ok rows=%d' % len(rows))


main()
