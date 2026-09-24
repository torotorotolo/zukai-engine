# -*- coding: utf-8 -*-
"""15本目②：Commons を欄ごとに歩き、1点ずつの台帳を JSON に落とす。
出力: ref/ep15/commons_ep15.json（1点1行ぶんの辞書のリスト）
網の4段＝権利 → 大きさ → 撮影年 → 場面（場面は題名を人が読む）。ここでは1〜3段の数だけ出す。
"""
import json, re, sys, time, urllib.parse, urllib.request
from collections import Counter

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine-research/1.0 (ep15 materials survey)'
OUT = r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/commons_ep15.json'

# 欄 → (カテゴリ, 深さ, 撮影年の窓)
SLOTS = [
    ('crash', 'Category:2011 Reno Air Races crash', 0, '2011-09'),
    ('n79111', 'Category:N79111 (aircraft)', 1, ''),
    ('gg_misc', 'Category:The Galloping Ghost', 0, ''),
    ('race2011', 'Category:Reno Air Races 2011', 1, '2011-09'),
    ('strega', 'Category:Strega (aircraft)', 0, '2011'),
    ('voodoo', 'Category:Voodoo (aircraft)', 0, '2011'),
    ('stead', 'Category:Reno Stead Airport', 1, ''),
    ('stead_afb', 'Category:Stead Air Force Base', 1, ''),
    ('reno_top', 'Category:Reno Air Races', 0, ''),
    ('reno1969_75', 'Category:Reno Air Races 1969|Category:Reno Air Races 1973|Category:Reno Air Races 1974|Category:Reno Air Races 1975', 0, '19'),
]


def q(params):
    # 🔴 09-24 に HTTP 429 で落ちた＝毎回3秒あけ、429 は Retry-After（無ければ60秒）待って聞き直す
    params = dict(params, format='json', formatversion='2', maxlag='5')
    req = urllib.request.Request(API, data=urllib.parse.urlencode(params).encode(),
                                 headers={'User-Agent': UA})
    for i in range(10):
        time.sleep(3)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if i == 9:
                raise
            wait = int(e.headers.get('Retry-After') or 60) + 5 if e.code == 429 else 10 * (i + 1)
            print('  HTTP', e.code, 'wait', wait, flush=True)
            time.sleep(wait)
        except Exception as e:
            if i == 9:
                raise
            time.sleep(10 * (i + 1))


def subcats(cat, depth):
    out, frontier = [cat], [cat]
    for _ in range(depth):
        nxt = []
        for c in frontier:
            d = q({'action': 'query', 'list': 'categorymembers', 'cmtitle': c, 'cmtype': 'subcat', 'cmlimit': '500'})
            for m in d.get('query', {}).get('categorymembers', []):
                if m['title'] not in out:
                    out.append(m['title']); nxt.append(m['title'])
            time.sleep(1)
        frontier = nxt
    return out


def strip(s):
    s = re.sub(r'<[^>]+>', ' ', s or '')
    return re.sub(r'\s+', ' ', s).strip()


DATE_RE = re.compile(r'(\d{4})[-:/](\d{2})(?:[-:/](\d{2}))?')

rows, seen = [], {}
for slot, cats, depth, win in SLOTS:
    allc = []
    for c in cats.split('|'):
        allc += subcats(c, depth)
    for c in allc:
        cont = {}
        while True:
            d = q(dict({'action': 'query', 'generator': 'categorymembers', 'gcmtitle': c,
                        'gcmtype': 'file', 'gcmlimit': '100',
                        'prop': 'imageinfo|categories', 'clshow': 'hidden', 'cllimit': 'max',
                        'iiprop': 'size|mime|extmetadata|url', 'iiurlwidth': '640',
                        'iiextmetadatafilter': 'DateTimeOriginal|DateTime|LicenseShortName|UsageTerms|Artist|Credit|ImageDescription'},
                       **cont))
            for p in d.get('query', {}).get('pages', []) or []:
                t = p.get('title')
                if t in seen:
                    seen[t]['slots'].append(slot) if slot not in seen[t]['slots'] else None
                    continue
                ii = (p.get('imageinfo') or [{}])[0]
                em = ii.get('extmetadata') or {}
                raw = strip((em.get('DateTimeOriginal') or em.get('DateTime') or {}).get('value'))
                m = DATE_RE.search(raw)
                ymd = '-'.join(x for x in m.groups() if x) if m else ''
                r = {
                    'title': t, 'pageid': p.get('pageid'), 'slots': [slot], 'cat': c,
                    'w': ii.get('width'), 'h': ii.get('height'), 'mime': ii.get('mime', ''),
                    'lic': strip((em.get('LicenseShortName') or {}).get('value')),
                    'terms': strip((em.get('UsageTerms') or {}).get('value')),
                    'artist': strip((em.get('Artist') or {}).get('value'))[:120],
                    'credit': strip((em.get('Credit') or {}).get('value'))[:160],
                    'desc': strip((em.get('ImageDescription') or {}).get('value'))[:300],
                    'date': ymd, 'date_raw': raw[:40],
                    'hidden': [x['title'][9:] for x in (p.get('categories') or [])],
                    'thumb': ii.get('thumburl', ''), 'url': ii.get('descriptionurl', ''),
                }
                rows.append(r); seen[t] = r
            if 'continue' in d:
                cont = d['continue']
            else:
                break
            time.sleep(1)
        time.sleep(1)
    print('slot', slot, 'cats', len(allc), 'rows so far', len(rows), flush=True)

json.dump(rows, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote', OUT, len(rows))


def cls(r):
    s = (r['lic'] + ' ' + r['terms']).lower()
    if 'by-sa' in s or 'gfdl' in s:
        return 'BY-SA'
    if 'public domain' in s or s.strip().startswith('pd') or 'cc0' in s:
        return 'PD/CC0'
    if 'cc by' in s or 'cc-by' in s:
        return 'BY'
    return 'other:' + r['lic'][:20]


print('\n欄 | 全点 | 段1 権利(PD/CC0・BY・BY-SA・他) | 段2 幅1280以上(同) | 撮影年の窓 | 動画')
for slot, cats, depth, win in SLOTS:
    rs = [r for r in rows if slot in r['slots']]
    c1 = Counter(cls(r) for r in rs)
    big = [r for r in rs if (r['w'] or 0) >= 1280 and str(r['mime']).startswith('image')]
    c2 = Counter(cls(r) for r in big)
    inwin = [r for r in big if win and r['date'].startswith(win)]
    c3 = Counter(cls(r) for r in inwin)
    vids = [r for r in rs if str(r['mime']).startswith('video')]
    f = lambda c: '%d/%d/%d/%d' % (c.get('PD/CC0', 0), c.get('BY', 0), c.get('BY-SA', 0), sum(v for k, v in c.items() if k.startswith('other')))
    print('%-11s | %4d | %s | %s | %s %s | %d' % (slot, len(rs), f(c1), f(c2), win or '-', f(c3) if win else '-', len(vids)))
print('\nother licenses:', Counter(r['lic'] for r in rows if cls(r).startswith('other')).most_common(10))
