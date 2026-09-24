# -*- coding: utf-8 -*-
"""15本目②：c15_pull.py の取りこぼし（続きの応答に分かれた imageinfo を読み捨てた）を題名で引き直し、
欄ごとの数と「場面を読むための一覧」を出す。"""
import json, re, sys, time, urllib.parse, urllib.request, urllib.error
from collections import Counter

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine-research/1.0 (ep15 materials survey)'
PATH = r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/commons_ep15.json'


def q(params):
    params = dict(params, format='json', formatversion='2', maxlag='5')
    req = urllib.request.Request(API, data=urllib.parse.urlencode(params).encode(), headers={'User-Agent': UA})
    for i in range(10):
        time.sleep(3)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if i == 9:
                raise
            wait = int(e.headers.get('Retry-After') or 60) + 5 if e.code == 429 else 10 * (i + 1)
            print('  HTTP', e.code, 'wait', wait, flush=True); time.sleep(wait)


def strip(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s or '')).strip()


DATE_RE = re.compile(r'(\d{4})[-:/](\d{2})(?:[-:/](\d{2}))?')
rows = json.load(open(PATH, encoding='utf-8'))
miss = [r for r in rows if not r.get('w') or not r.get('lic')]
print('欠け', len(miss), flush=True)
by = {r['title']: r for r in rows}
for i in range(0, len(miss), 40):
    ts = [r['title'] for r in miss[i:i + 40]]
    d = q({'action': 'query', 'titles': '|'.join(ts), 'prop': 'imageinfo|categories', 'clshow': 'hidden', 'cllimit': 'max',
           'iiprop': 'size|mime|extmetadata|url', 'iiurlwidth': '640',
           'iiextmetadatafilter': 'DateTimeOriginal|DateTime|LicenseShortName|UsageTerms|Artist|Credit|ImageDescription'})
    for p in d.get('query', {}).get('pages', []) or []:
        r = by.get(p.get('title'))
        if not r:
            continue
        ii = (p.get('imageinfo') or [{}])[0]
        em = ii.get('extmetadata') or {}
        raw = strip((em.get('DateTimeOriginal') or em.get('DateTime') or {}).get('value'))
        m = DATE_RE.search(raw)
        r.update({'w': ii.get('width'), 'h': ii.get('height'), 'mime': ii.get('mime', ''),
                  'lic': strip((em.get('LicenseShortName') or {}).get('value')),
                  'terms': strip((em.get('UsageTerms') or {}).get('value')),
                  'artist': strip((em.get('Artist') or {}).get('value'))[:120],
                  'credit': strip((em.get('Credit') or {}).get('value'))[:160],
                  'desc': strip((em.get('ImageDescription') or {}).get('value'))[:300],
                  'date': '-'.join(x for x in m.groups() if x) if m else '', 'date_raw': raw[:40],
                  'thumb': ii.get('thumburl', ''), 'url': ii.get('descriptionurl', '')})
        hid = [x['title'][9:] for x in (p.get('categories') or [])]
        if hid:
            r['hidden'] = sorted(set(r.get('hidden', []) + hid))
json.dump(rows, open(PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('still missing', sum(1 for r in rows if not r.get('w') or not r.get('lic')))


def cls(r):
    s = (r['lic'] + ' ' + r['terms']).lower()
    if 'by-sa' in s or 'gfdl' in s:
        return 'BY-SA'
    if 'public domain' in s or s.strip().startswith('pd') or 'cc0' in s:
        return 'PD'
    if 'cc by' in s or 'cc-by' in s:
        return 'BY'
    return 'other'


WIN = {'crash': '2011-09', 'race2011': '2011-09', 'strega': '2011', 'voodoo': '2011'}
print('\n欄 | 全点 | 権利 PD/BY/BY-SA/他 | 幅1280以上 | 窓の中（幅1280以上）')
for slot in ['crash', 'n79111', 'gg_misc', 'race2011', 'strega', 'voodoo', 'stead', 'stead_afb', 'reno_top', 'reno1969_75']:
    rs = [r for r in rows if slot in r['slots']]
    f = lambda xs: '%d/%d/%d/%d' % tuple(sum(1 for r in xs if cls(r) == k) for k in ('PD', 'BY', 'BY-SA', 'other'))
    big = [r for r in rs if (r['w'] or 0) >= 1280]
    win = WIN.get(slot)
    print('%-11s | %3d | %s | %s | %s' % (slot, len(rs), f(rs), f(big), f([r for r in big if win and r['date'].startswith(win)]) if win else '-'))


def line(r):
    return '  %s %4sx%-4s %-6s %-10s %s | %s' % (cls(r)[:5], r['w'], r['h'], r['date'][:10], (r['artist'] or '')[:18], r['title'][5:80], ','.join(h for h in r.get('hidden', []) if re.search('(?i)PD|public domain|NTSB|federal|USGov|CC-Zero|US Air Force|Navy', h))[:60])


print('\n=== 1件ずつ（race2011 以外は全部）')
for slot in ['crash', 'n79111', 'gg_misc', 'strega', 'voodoo', 'stead', 'stead_afb', 'reno_top', 'reno1969_75']:
    print('--', slot)
    for r in sorted([r for r in rows if slot in r['slots']], key=lambda r: r['date']):
        print(line(r))
KEY = re.compile(r'(?i)galloping|leeward|177|crash|grand ?stand|stands|crowd|spectat|box|pylon|voodoo|strega|unlimited|p-51|mustang|pit|ramp|race ?course|home')
rs = [r for r in rows if 'race2011' in r['slots']]
hit = [r for r in rs if KEY.search(r['title']) or KEY.search(r['desc'])]
print('\n=== race2011：語に当たった %d / %d 点（題名と説明の語）' % (len(hit), len(rs)))
for r in sorted(hit, key=lambda r: r['date']):
    print(line(r))
print('\nrace2011 の日付', Counter(r['date'][:10] for r in rs).most_common(8))
print('race2011 の作者', Counter((r['artist'] or '?')[:25] for r in rs).most_common(6))
print('race2011 の下位カテゴリ', Counter(r['cat'][9:] for r in rs).most_common(10))
