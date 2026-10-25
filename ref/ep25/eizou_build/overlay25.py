# -*- coding: utf-8 -*-
"""25本目 映像方針：付図の写真の上の注記（矢印・札・字）が「原画に焼き込み」か「PDF の上に重ねた図形（原画には無い）」かを画素で測る。
画像は開かない（機械で比べるだけ）。入力＝figcap25.tsv（写真ごとの xref と頁の上の矩形）。

  python ref/ep25/eizou_build/overlay25.py <figcap25.tsv> <出力.tsv>
  python ref/ep25/eizou_build/overlay25.py --selftest

やり方：頁を描いて写真の矩形で切った絵（注記こみ）と、PDF に埋め込まれた原画（extract_image）を同じ大きさにそろえ、
        画素の差が大きい（>60）点の割合を測る。原画は頁の上で回して置かれていることがある＝4つの向きで最小の差を採る。
読み方：diff_px が 1% 以上＝頁の上に重ねた注記がある（原画を使えば消える）／ほぼ0＝注記は無いか、原画に焼き込み
⚠️ 目安の数字＝⑤b で原画を原寸で見て決める。
"""
import io
import os
import sys

import fitz
from PIL import Image, ImageChops

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
JTSB = os.path.join(os.path.dirname(HERE), 'src', 'jtsb')
TH = 60


def measure(doc, pg, xref, rect, cache):
    key = (doc.name, pg.number)
    if key not in cache:
        z = 3.0
        pix = pg.get_pixmap(matrix=fitz.Matrix(z, z))
        cache[key] = (Image.open(io.BytesIO(pix.tobytes('png'))).convert('L'), z)
    page_img, z = cache[key]
    x0, y0, x1, y1 = [float(v) for v in rect.split(',')]
    crop = page_img.crop((int(x0 * z), int(y0 * z), int(x1 * z), int(y1 * z)))
    raw = Image.open(io.BytesIO(doc.extract_image(xref)['image'])).convert('L')
    best = None
    for rot in (0, 90, 180, 270):
        r = raw.rotate(rot, expand=True)
        a = r.resize((160, int(160 * r.height / r.width)) if r.width >= r.height else (int(160 * r.width / r.height), 160))
        b = crop.resize(a.size)
        d = ImageChops.difference(a, b)
        hist = d.histogram()
        big = sum(hist[TH + 1:]) / (a.size[0] * a.size[1])
        mean = sum(i * n for i, n in enumerate(hist)) / (a.size[0] * a.size[1])
        if best is None or mean < best[1]:
            best = (rot, mean, big)
    return best


def run(tsv, out):
    rows = [ln.rstrip('\n').split('\t') for ln in open(tsv, encoding='utf-8')]
    head, rows = rows[0], rows[1:]
    docs, cache, res = {}, {}, []
    for r in rows:
        name, page, no, xref, nat, rect = r[0], r[1], r[2], int(r[3]), r[4], r[5]
        if name not in docs:
            docs[name] = fitz.open(os.path.join(JTSB, name + '.pdf'))
        doc = docs[name]
        pg = doc[int(page[3:]) - 1]
        rot, mean, big = measure(doc, pg, xref, rect, cache)
        res.append([name, page, no, str(xref), nat, str(rot), '%.1f' % mean, '%.2f' % (big * 100), r[7][:60]])
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['pdf', 'page', 'no', 'xref', 'native', 'raw_rot', 'mean_diff', 'diff_px_%', 'caption']) + '\n')
        for x in res:
            f.write('\t'.join(x) + '\n')
    print('rows', len(res), '→', out)
    return res


def selftest():
    """陽性＝付図16 その3 の車内電話の写真（頁の上に「列車無線マイク」「車内電話」の札と線が重なる）と、
    付図26 の6コマのうち文字の層に札（42号柱・41号柱・上り第3閉そく信号機）があるコマ／陰性＝付図26 の札の無い5コマ"""
    import tempfile
    t = os.path.join(tempfile.gettempdir(), 'ov25_st.tsv')
    src = os.path.join(HERE, 'figcap25.tsv')
    rows = [ln.rstrip('\n').split('\t') for ln in open(src, encoding='utf-8')]
    pick = [rows[0]] + [r for r in rows[1:] if (r[0], r[1]) in (('RA07-3-1-4', 'PDF7'), ('RA07-3-1-5', 'PDF28'))]
    open(t, 'w', encoding='utf-8').write('\n'.join('\t'.join(r) for r in pick) + '\n')
    res = run(t, t + '.out')
    labeled = {r[2] for r in pick[1:] if r[1] == 'PDF28' and r[6].strip()}
    pos = [x for x in res if (x[1] == 'PDF7' and x[4] == '215x470') or (x[1] == 'PDF28' and x[2] in labeled)]
    neg = [x for x in res if x[1] == 'PDF28' and x[2] not in labeled]
    ok = len(pos) == 2 and all(float(x[7]) >= 1.0 for x in pos) and len(neg) == 5 and all(float(x[7]) < 1.0 for x in neg)
    print('陽性', [x[7] for x in pos], '％／陰性（付図26 の札なし）', [x[7] for x in neg], '→', 'selftest OK' if ok else 'selftest ✗')
    return 0 if ok else 1


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--selftest':
        sys.exit(selftest())
    run(a[0], a[1])
