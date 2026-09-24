# -*- coding: utf-8 -*-
"""15本目②：Commons の欄ごとに網の段1〜3を数える（tataquax の撮影時刻は日本時間のまま＝現地は −16時間）。"""
import collections, datetime, json, re

rows = json.load(open(r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/commons_ep15.json', encoding='utf-8'))


def cls(r):
    s = (r['lic'] + ' ' + r['terms']).lower()
    if 'by-sa' in s or 'gfdl' in s:
        return 'BY-SA'
    if 'public domain' in s or s.strip().startswith('pd') or 'cc0' in s:
        return 'PD'
    if 'cc by' in s or 'cc-by' in s:
        return 'BY'
    return 'other'


def local(r):
    raw = r.get('date_raw', '')
    m = re.match(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})', raw)
    if (r.get('artist') or '').startswith('tataquax') and m:
        t = datetime.datetime(*map(int, m.groups())) - datetime.timedelta(hours=16)
        return t.strftime('%Y-%m-%d %H:%M')
    return r.get('date', '')


WIN = {'crash': ('2011-09-14', '2011-09-17'), 'race2011': ('2011-09-14', '2011-09-17'), 'n79111': ('2011-09-14', '2011-09-17'),
       'strega': ('2011-09-14', '2011-09-17'), 'voodoo': ('2011-09-14', '2011-09-17'), 'reno1969_75': ('1969', '1976')}
f = lambda xs: '%d/%d/%d' % tuple(sum(1 for r in xs if cls(r) == k) for k in ('PD', 'BY', 'BY-SA'))
print('欄 | 全点 | 段1 PD・CC0/BY/BY-SA | 段2 幅1280以上 | 段3 窓（現地） | 窓')
for slot in ['crash', 'n79111', 'gg_misc', 'race2011', 'strega', 'voodoo', 'stead', 'stead_afb', 'reno_top', 'reno1969_75']:
    rs = [r for r in rows if slot in r['slots']]
    big = [r for r in rs if (r['w'] or 0) >= 1280]
    w = WIN.get(slot)
    inw = [r for r in big if w and w[0] <= local(r)[:10] < w[1]] if w else []
    print('%-11s | %3d | %s | %s | %s | %s' % (slot, len(rs), f(rs), f(big), f(inw) if w else '-', '%s〜%s' % w if w else '-'))
t = [r for r in rows if (r.get('artist') or '').startswith('tataquax')]
print('\ntataquax 現地の日ごと', sorted(collections.Counter(local(r)[:10] for r in t).items()))
print('tataquax 現地の最後', max(local(r) for r in t))
n = [r for r in rows if 'n79111' in r['slots']]
print('\nn79111 の年', sorted(collections.Counter(local(r)[:4] + (' (' + r['title'][5:30] + ')' if not local(r) else '') for r in n).items()))
for r in sorted(n, key=local):
    print('  ', local(r), cls(r), r['w'], 'x', r['h'], r['title'][5:75])
