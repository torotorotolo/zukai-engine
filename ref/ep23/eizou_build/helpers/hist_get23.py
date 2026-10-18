# -*- coding: utf-8 -*-
"""23本目 映像方針：歴史編纂院の写真を取る（「자료 이용 조건 동의서」＝目的 상업 출판・出典を書くことに同意を内蔵ブラウザで出したあと・了承② 2026-10-18）。

  python ref/ep23/eizou_build/helpers/hist_get23.py 2301030510 2301030077 ...

取り先＝https://history.seoul.go.kr/common/file/fileDown.do?accSn=<番号>&accTy=bbsctt&ordr=0（頁の goDownload と同じ）。置き場＝ref/ep23/src/hist/hs_<番号>_0.jpg（git の外）。
型の札は application/octet-stream＝先頭の印（JPEG）で見る。長さは Content-Length と照合。道具の名乗りにメールや @ を入れない。
"""
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DST = os.path.join(REPO, 'ref', 'ep23', 'src', 'hist')
UA = 'zukai-engine-research/1.0 (personal non-commercial research; github torotorotolo)'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    os.makedirs(DST, exist_ok=True)
    bad = 0
    for sn in sys.argv[1:]:
        dst = os.path.join(DST, 'hs_%s_0.jpg' % sn)
        if os.path.exists(dst):
            print(sn, '済み')
            continue
        url = 'https://history.seoul.go.kr/common/file/fileDown.do?accSn=%s&accTy=bbsctt&ordr=0' % sn
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': 'https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=%s&key=2211220005' % sn})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                ln = int(r.headers.get('Content-Length') or -1)
                data = r.read()
        except Exception as e:
            print(sn, '🔴 取れない：', e)
            bad += 1
            continue
        if data[:3] != b'\xff\xd8\xff':
            print(sn, '🔴 JPEG でない（%d bytes・先頭 %r）＝置かない' % (len(data), data[:8]))
            bad += 1
            continue
        if ln > 0 and ln != len(data):
            print(sn, '🔴 長さ %d ≠ %d＝落としかけ' % (len(data), ln))
            bad += 1
            continue
        with open(dst + '.part', 'wb') as f:
            f.write(data)
        os.replace(dst + '.part', dst)
        print(sn, '→', os.path.relpath(dst, REPO), len(data))
        time.sleep(1.5)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
