# -*- coding: utf-8 -*-
"""27本目 映像方針（2026-10-29・チャット5）：Commons の候補の説明・撮影日・撮影地の座標・縮小版の URL を1点ずつ問い合わせる（文字だけ・画像は落とさない）。

  python -P ref/ep27/eizou_build/commons_geo27.py CM044 CM045 ...     → ref/ep27/src/commons/geo27.json に足す（取れた点は取り直さない）

番号＝src/commons/commons_meta.tsv を0から数えた行（台本の CMnnn と同じ）。
🔴 出力に撮影者の名前が入る（Artist）＝git の外（src/）にだけ書く。多件まとめの問い合わせは 429 が続く（ルール §5b-55）＝1件ずつ・4秒あけ。
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
META = os.path.join(EP, 'src', 'commons', 'commons_meta.tsv')
OUT = os.path.join(EP, 'src', 'commons', 'geo27.json')
UA = {'User-Agent': 'zukai-engine-research/1.0 (GitHub torotorotolo)'}
KEYS = 'ImageDescription|DateTimeOriginal|GPSLatitude|GPSLongitude|LicenseShortName|Artist|ObjectName'


def rows():
    with open(META, encoding='utf-8') as f:
        return [ln.rstrip('\n').split('\t') for ln in f if ln.strip()]


def ask(title):
    kw = dict(action='query', titles=title, prop='imageinfo|coordinates', iiprop='url|size|extmetadata',
              iiurlwidth=960, iiextmetadatafilter=KEYS, format='json', formatversion=2)
    url = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(kw)
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception as e:      # 429 など＝待って取り直す（回避はしない）
            print('  ERR', title, e, file=sys.stderr)
            time.sleep(30 * (i + 1))
    return None


def main():
    meta = rows()
    done = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    for cm in sys.argv[1:]:
        if cm in done:
            continue
        r = meta[int(cm[2:])]
        title = r[1]
        js = ask(title)
        if not js:
            print('NG', cm, title)
            continue
        p = js['query']['pages'][0]
        ii = (p.get('imageinfo') or [{}])[0]
        em = {k: v.get('value') for k, v in (ii.get('extmetadata') or {}).items()}
        co = (p.get('coordinates') or [{}])[0]
        done[cm] = dict(title=title, w=ii.get('width'), h=ii.get('height'), url=ii.get('url'),
                        thumb960=ii.get('thumburl'), lat=co.get('lat') or em.get('GPSLatitude'),
                        lon=co.get('lon') or em.get('GPSLongitude'), date=em.get('DateTimeOriginal'),
                        lic=em.get('LicenseShortName'), desc=em.get('ImageDescription'),
                        artist=em.get('Artist'), page=ii.get('descriptionurl'))
        print('ok', cm, done[cm]['lat'], done[cm]['lon'], title[:60])
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(done, f, ensure_ascii=False, indent=1)
        time.sleep(4)
    print('done', len(done))


if __name__ == '__main__':
    main()
