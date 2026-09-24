# -*- coding: utf-8 -*-
"""15本目②：Commons のカテゴリを語で探し、点数（categoryinfo）を出す。"""
import json, sys, time, urllib.parse, urllib.request

API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine-research/1.0 (ep15 materials survey)'


def q(params):
    params = dict(params, format='json', formatversion='2')
    req = urllib.request.Request(API, data=urllib.parse.urlencode(params).encode(),
                                 headers={'User-Agent': UA})
    for i in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if i == 4:
                raise
            time.sleep(5 * (i + 1))


TERMS = ['Reno Air Races', 'Reno air race 2011', 'Galloping Ghost', 'Reno Stead Airport',
         'Reno-Stead', 'National Championship Air Races', 'Air racing Reno', 'N79111',
         'Strega P-51', 'Voodoo P-51', 'Leeward']
found = {}
for t in TERMS:
    d = q({'action': 'query', 'list': 'search', 'srsearch': t, 'srnamespace': '14', 'srlimit': '50'})
    for m in d.get('query', {}).get('search', []):
        found.setdefault(m['title'], set()).add(t)
    time.sleep(1.5)
titles = sorted(found)
info = {}
for i in range(0, len(titles), 40):
    d = q({'action': 'query', 'prop': 'categoryinfo', 'titles': '|'.join(titles[i:i + 40])})
    for p in d.get('query', {}).get('pages', []):
        ci = p.get('categoryinfo') or {}
        info[p['title']] = (ci.get('files', 0), ci.get('subcats', 0))
    time.sleep(1.5)
for t in titles:
    f, s = info.get(t, (0, 0))
    print('%5d files %3d sub | %s | <- %s' % (f, s, t, ','.join(sorted(found[t]))))
