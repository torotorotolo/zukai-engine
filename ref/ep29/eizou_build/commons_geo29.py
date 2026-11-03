# -*- coding: utf-8 -*-
"""29本目 映像方針（2026-11-03・チャット5）：Commons の候補の説明・撮影日・撮影地の座標・縮小版の URL を1点ずつ問い合わせる（文字だけ・画像は落とさない）。28本目の commons_geo28.py を写した。

  python -P ref/ep29/eizou_build/commons_geo29.py CM008 M005 P012 ...     → ref/ep29/src/commons/geo29.json に足す（取れた点は取り直さない）

番号＝目録の行（0行目は見出し）＝CMnnn は src/commons/commons_meta29_cats.tsv（台本の CMnnn と同じ）・Mnnn は commons_meta29_more.tsv・Pnnn は commons_meta29_public.tsv（映像方針で足した公的な機関の建物）・Tnnn は commons_meta29_terms.tsv（語の検索）。
🔴 出力に撮影者の名前が入る（Artist）＝git の外（src/）にだけ書く。多件まとめの問い合わせは 429 が続く（ルール §5b-55）＝1件ずつ・4秒あけ。
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
META = {'CM': 'commons_meta29_cats.tsv', 'M': 'commons_meta29_more.tsv', 'P': 'commons_meta29_public.tsv', 'T': 'commons_meta29_terms.tsv'}
OUT = os.path.join(EP, 'src', 'commons', 'geo29.json')
UA = {'User-Agent': 'zukai-engine-research/1.0 (GitHub torotorotolo)'}
KEYS = 'ImageDescription|DateTimeOriginal|GPSLatitude|GPSLongitude|LicenseShortName|Artist|ObjectName'


def rows(fn):
    with open(os.path.join(EP, 'src', 'commons', fn), encoding='utf-8') as f:
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
    tables = {k: rows(v) for k, v in META.items()}
    done = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    for code in sys.argv[1:]:
        if code in done:
            continue
        m = re.match(r'(CM|M|P|T)(\d+)$', code)
        r = tables[m.group(1)][int(m.group(2))]
        title = r[1]
        js = ask(title)
        if not js:
            print('NG', code)
            continue
        p = js['query']['pages'][0]
        ii = (p.get('imageinfo') or [{}])[0]
        em = {k: v.get('value') for k, v in (ii.get('extmetadata') or {}).items()}
        co = (p.get('coordinates') or [{}])[0]
        done[code] = dict(title=title, w=ii.get('width'), h=ii.get('height'), url=ii.get('url'),
                          thumb960=ii.get('thumburl'), lat=co.get('lat') or em.get('GPSLatitude'),
                          lon=co.get('lon') or em.get('GPSLongitude'), date=em.get('DateTimeOriginal'),
                          lic=em.get('LicenseShortName'), desc=em.get('ImageDescription'),
                          artist=em.get('Artist'), page=ii.get('descriptionurl'))
        print('ok', code, done[code]['w'], done[code]['h'], done[code]['lic'], flush=True)
        with open(OUT, 'w', encoding='utf-8') as f:
            json.dump(done, f, ensure_ascii=False, indent=1)
        time.sleep(4)
    print('done', len(done))


if __name__ == '__main__':
    main()
