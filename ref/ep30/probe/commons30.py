# -*- coding: utf-8 -*-
"""30本目 ②：Wikimedia Commons の目録だけを取る（画像は落とさない・作者名を含むので出力は git の外の src/ へ）。
  python -I -X utf8 commons30.py <出力tsv> <カテゴリ名...>
列＝ファイル名・幅・高さ・ライセンス・撮影日の札・提供の欄（先頭だけ）
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
API = 'https://commons.wikimedia.org/w/api.php'
UA = 'zukai-engine-ep30-probe/1.0 (research for a documentary; no bulk download)'


def get(params):
    params.update(format='json', formatversion='2')
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(params), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def main(out, cats):
    rows = []
    for cat in cats:
        cont = {}
        while True:
            p = dict(action='query', generator='categorymembers', gcmtitle='Category:' + cat, gcmtype='file', gcmlimit='50',
                     prop='imageinfo', iiprop='size|extmetadata|mime', iiextmetadatafilter='LicenseShortName|Artist|DateTimeOriginal|Credit')
            p.update(cont)
            d = get(p)
            for pg in d.get('query', {}).get('pages', []):
                ii = (pg.get('imageinfo') or [{}])[0]
                m = ii.get('extmetadata', {})
                g = lambda k: re.sub(r'<[^>]+>', '', (m.get(k) or {}).get('value', '')).strip()[:80]
                rows.append([cat, pg['title'].replace('File:', ''), ii.get('width'), ii.get('height'), g('LicenseShortName'), g('DateTimeOriginal'), g('Credit'), g('Artist')])
            if 'continue' in d:
                cont = d['continue']
                time.sleep(2)
            else:
                break
        time.sleep(2)
        print(cat, len([r for r in rows if r[0] == cat]))
    with open(out, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write('\t'.join(str(x) for x in r) + '\n')
    print('計', len(rows), out)


main(sys.argv[1], sys.argv[2:])
