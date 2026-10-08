# -*- coding: utf-8 -*-
"""Wikimedia Commons の API を引く小道具（20本目 映像方針・scratchpad）。

  python -I commons20.py search "<語>" [件数]          ファイル名前空間を検索
  python -I commons20.py info "<File:名前>" ["<File:…>" …]  大きさ・権利・URL・作者
  python -I commons20.py cat "<Category:名前>" [件数]    カテゴリの中のファイル

Git Bash から curl に日本語を渡すと文字化けするので、Python で URL を組む。
道具の名乗りにメールや @ を入れない。
"""
import json
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine-research/1.0 (personal non-commercial research; github torotorotolo)'


def get(params):
    params = dict(params, format='json', formatversion='2')
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode('utf-8'))


def strip(s):
    import re
    return re.sub(r'<[^>]+>', '', s or '').strip()


def info(titles):
    out = []
    for i in range(0, len(titles), 40):
        d = get({'action': 'query', 'titles': '|'.join(titles[i:i + 40]), 'prop': 'imageinfo',
                 'iiprop': 'url|size|mime|extmetadata|sha1',
                 'iiextmetadatafilter': 'LicenseShortName|Artist|DateTimeOriginal|ImageDescription|Credit|UsageTerms|Categories'})
        for p in d['query']['pages']:
            if p.get('missing'):
                out.append({'title': p['title'], 'missing': True})
                continue
            ii = p['imageinfo'][0]
            em = ii.get('extmetadata', {})
            out.append({'title': p['title'], 'w': ii.get('width'), 'h': ii.get('height'),
                        'bytes': ii.get('size'), 'mime': ii.get('mime'), 'dur': ii.get('duration'),
                        'sha1': ii.get('sha1'),
                        'license': strip(em.get('LicenseShortName', {}).get('value')),
                        'artist': strip(em.get('Artist', {}).get('value'))[:120],
                        'date': strip(em.get('DateTimeOriginal', {}).get('value'))[:60],
                        'credit': strip(em.get('Credit', {}).get('value'))[:160],
                        'desc': strip(em.get('ImageDescription', {}).get('value'))[:300],
                        'cats': strip(em.get('Categories', {}).get('value'))[:400],
                        'url': ii.get('url'), 'page': ii.get('descriptionurl')})
    return out


def main():
    cmd = sys.argv[1]
    if cmd == 'search':
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        d = get({'action': 'query', 'list': 'search', 'srsearch': sys.argv[2], 'srnamespace': '6', 'srlimit': str(n)})
        print('hits', d['query']['searchinfo']['totalhits'])
        for r in d['query']['search']:
            print(r['title'])
    elif cmd == 'info':
        for r in info(sys.argv[2:]):
            print(json.dumps(r, ensure_ascii=False))
    elif cmd == 'cat':
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        d = get({'action': 'query', 'list': 'categorymembers', 'cmtitle': sys.argv[2], 'cmlimit': str(n), 'cmtype': 'file|subcat'})
        for r in d['query']['categorymembers']:
            print(r['title'])


if __name__ == '__main__':
    main()
