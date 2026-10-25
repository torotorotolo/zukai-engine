# -*- coding: utf-8 -*-
"""25本目 映像方針：報告書の付図の頁で、写真ごとに「説明の文字（キャプション）」と「写真の上に重ねた文字（注記）」を機械で当てる。
画像は開かない（PDF の画像の矩形と文字の行の矩形の位置だけ）。

  python ref/ep25/eizou_build/figcap25.py <出力.tsv> RA07-3-1-3:9 RA07-3-1-4:5 ...
  python ref/ep25/eizou_build/figcap25.py --selftest

出力の列：pdf・頁・番号（頁の上の並び＝上から下・左から右）・xref・埋め込みの実寸・頁の上の矩形（pt）・
         注記（写真の矩形の内側にある文字の行＝PDF の文字＝写真の画素ではない＝埋め込みの原画には載っていない）・
         説明（写真の下 40pt 以内で横が重なる行。無ければ上 40pt 以内）
⚠️ 当て方は位置だけ＝⑤b で焼いた絵を原寸で見て最終にする（記憶 feedback-subtitle-must-match-what-is-visible）。
"""
import os
import sys
import unicodedata

import fitz

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
JTSB = os.path.join(os.path.dirname(HERE), 'src', 'jtsb')
MIN_PT = 60          # 頁の上でこれより小さい画像（印・矢印）は飛ばす（probe/figs25.py と同じ）
NEAR = 40            # 説明を探す上下の幅（pt）


def norm(s):
    return unicodedata.normalize('NFKC', s).strip()


def lines_of(page):
    """文字の行の矩形を「見たままの向き」に直す（頁が90度回っている付図26 などは、回す前の座標だと説明が写真の右に来る＝下と読めない）"""
    out = []
    m = page.rotation_matrix
    d = page.get_text('dict')
    for b in d['blocks']:
        for ln in b.get('lines', []):
            t = norm(''.join(sp['text'] for sp in ln['spans']))
            if t:
                out.append((fitz.Rect(ln['bbox']) * m, t))
    return out


def overlap_x(a, b):
    return max(0, min(a.x1, b.x1) - max(a.x0, b.x0))


def scan(name, pno):
    doc = fitz.open(os.path.join(JTSB, name + '.pdf'))
    pg = doc[pno - 1]
    lines = lines_of(pg)
    ims = []
    for im in pg.get_images(full=True):
        xref = im[0]
        for r in pg.get_image_rects(xref):
            r = r * pg.rotation_matrix
            if r.width < MIN_PT or r.height < MIN_PT:
                continue
            info = doc.extract_image(xref)
            ims.append((r, xref, '%dx%d' % (info['width'], info['height'])))
    ims.sort(key=lambda x: (round(x[0].y0 / 20), x[0].x0))
    rows = []
    for k, (r, xref, nat) in enumerate(ims, 1):
        inner = [t for (lr, t) in lines if r.contains(fitz.Point((lr.x0 + lr.x1) / 2, (lr.y0 + lr.y1) / 2))]
        below = sorted([(lr.y0 - r.y1, t) for (lr, t) in lines
                        if 0 <= lr.y0 - r.y1 <= NEAR and overlap_x(lr, r) > 0.3 * min(lr.width, r.width)])
        above = sorted([(r.y0 - lr.y1, t) for (lr, t) in lines
                        if 0 <= r.y0 - lr.y1 <= NEAR and overlap_x(lr, r) > 0.3 * min(lr.width, r.width)])
        cap = ' '.join(t for _, t in below[:2]) if below else (('↑' + ' '.join(t for _, t in above[-2:])) if above else '')
        rows.append([name, 'PDF%d' % pno, str(k), str(xref), nat, '%.0f,%.0f,%.0f,%.0f' % tuple(r), ' / '.join(inner)[:160], cap[:120]])
    return rows


def selftest():
    # 付図26（R5 PDF28）＝写真6コマ。頁の文字の層に「1 名神高速道路跨線橋地点(1k992m)付近」ほか6つの説明がある
    rows = scan('RA07-3-1-5', 28)
    ok = len(rows) == 6
    caps = ' '.join(r[7] for r in rows)
    ok &= all(('%d ' % i) in caps or ('%d' % i) in caps for i in range(1, 7))
    ok &= any('1k992m' in r[7] for r in rows)
    print('付図26 の写真', len(rows), '点・説明に 1k992m', any('1k992m' in r[7] for r in rows), '→', 'selftest OK' if ok else 'selftest ✗')
    for r in rows:
        print('  ', r[2], r[4], r[7][:60])
    return 0 if ok else 1


def main(a):
    if a and a[0] == '--selftest':
        return selftest()
    out = a[0]
    rows = [['pdf', 'page', 'no', 'xref', 'native', 'rect_pt', 'overlay_text', 'caption']]
    for spec in a[1:]:
        name, pno = spec.split(':')
        rows += scan(name, int(pno))
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        for r in rows:
            f.write('\t'.join(x.replace('\t', ' ') for x in r) + '\n')
    print('rows', len(rows) - 1, '→', out)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
