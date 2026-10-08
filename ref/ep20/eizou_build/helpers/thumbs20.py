# -*- coding: utf-8 -*-
"""Commons の候補を「見るため」だけに縮小版で取る（20本目 映像方針・scratchpad）。

  python -I thumbs20.py <出力フォルダ> <幅px> <記号>=<File:名前> …

API で thumburl（iiurlwidth）を引き、1点ずつ1秒あけて落とす。原本の取得は了承②のあと（ここでは取らない）。
出力＝<記号>.jpg と thumbs.tsv（記号・File名・縮小の幅高さ・バイト数・URL）。
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
UA = 'zukai-engine-research/1.0 (personal non-commercial research; github torotorotolo)'
API = 'https://commons.wikimedia.org/w/api.php'


def api(params):
    params = dict(params, format='json', formatversion='2')
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(params), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode('utf-8'))


def main():
    out, width = sys.argv[1], int(sys.argv[2])
    os.makedirs(out, exist_ok=True)
    pairs = [a.split('=', 1) for a in sys.argv[3:]]
    d = api({'action': 'query', 'titles': '|'.join(t for _, t in pairs), 'prop': 'imageinfo',
             'iiprop': 'url|size', 'iiurlwidth': str(width)})
    info = {p['title']: p['imageinfo'][0] for p in d['query']['pages'] if 'imageinfo' in p}
    norm = {n['from']: n['to'] for n in d['query'].get('normalized', [])}
    rows = []
    for code, title in pairs:
        ii = info.get(norm.get(title, title))
        if not ii:
            print('🔴 見つからない', code, title)
            continue
        url = ii.get('thumburl') or ii['url']
        dst = os.path.join(out, code + '.jpg')
        for k in range(3):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': UA})
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
                break
            except Exception as e:
                print('  再試行', code, e)
                time.sleep(10 * (k + 1))
        else:
            print('🔴 取れない', code)
            continue
        open(dst, 'wb').write(data)
        rows.append((code, title, ii.get('thumbwidth'), ii.get('thumbheight'), len(data), url))
        print('%s %s %sx%s %d bytes' % (code, title, ii.get('thumbwidth'), ii.get('thumbheight'), len(data)))
        time.sleep(1.0)
    with open(os.path.join(out, 'thumbs.tsv'), 'a', encoding='utf-8') as f:
        for r in rows:
            f.write('\t'.join(str(x) for x in r) + '\n')


if __name__ == '__main__':
    main()
