# -*- coding: utf-8 -*-
"""23本目 映像方針：研究院の写真を、頁のフォーム（利用目的＝상업적 활용）が返したダウンロード先から取る（了承② 2026-10-18）。

  python ref/ep23/eizou_build/helpers/sire_get23.py <nid=/photo/download/...?t=...> [...]

置き場＝ref/ep23/src/sire/sire_<nid>.jpg（git の外）。HEAD を見ずに GET 1回（頁の作りが HEAD を受けないため）→ 型が image/ でなければ捨てる → 長さ（Content-Length）と照合 → 名前を付け替える。
道具の名乗りにメールや @ を入れない。
"""
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DST = os.path.join(REPO, 'ref', 'ep23', 'src', 'sire')
UA = 'zukai-engine-research/1.0 (personal non-commercial research; github torotorotolo)'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(DST, exist_ok=True)
    bad = 0
    for arg in sys.argv[1:]:
        nid, path = arg.split('=', 1)
        dst = os.path.join(DST, 'sire_%s.jpg' % nid)
        if os.path.exists(dst):
            print(nid, '済み')
            continue
        url = 'https://data.si.re.kr' + path
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://data.si.re.kr/node/%s' % nid})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                ct = r.headers.get('Content-Type', '')
                ln = int(r.headers.get('Content-Length') or -1)
                data = r.read()
        except Exception as e:
            print(nid, '🔴 取れない：', e)
            bad += 1
            continue
        if not (ct.startswith('image/') or data[:3] == b'\xff\xd8\xff'):   # 10-18：研究院は application/octet-stream で返す＝先頭の印（JPEG）で見る
            print(nid, '🔴 画像でない（%s・%d bytes・先頭 %r）＝捨てる' % (ct, len(data), data[:4]))
            bad += 1
            continue
        if ln > 0 and ln != len(data):
            print(nid, '🔴 長さ %d ≠ %d＝落としかけ' % (len(data), ln))
            bad += 1
            continue
        part = dst + '.part'
        with open(part, 'wb') as f:
            f.write(data)
        os.replace(part, dst)
        print(nid, '→', os.path.relpath(dst, REPO), ct, len(data))
        time.sleep(1.5)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
