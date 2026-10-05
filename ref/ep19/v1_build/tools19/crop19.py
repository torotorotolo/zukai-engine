# -*- coding: utf-8 -*-
"""19本目④：決め所・数字の頁の画像を、OCR／文字の層の座標で「その段だけ」切り出す。
原寸の頁を丸ごと読まない（鉄則1）。見た枚は seen19.tsv に1行ずつ記録する（記録は見たあとに手で足す）。
  python crop19.py
"""
import os
import re

import fitz
from PIL import Image

S1 = ('C:/Users/konar/AppData/Local/Temp/claude/C--Users-konar-Documents-Obsidian-Vault/'
      '4cbe5283-d9a0-4fd2-8ebc-1295638da157/scratchpad')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'crops')
SRC = 'C:/Users/konar/Desktop/zukai-engine/ref/ep19/src'
SURF = 'C:/Users/konar/Desktop/zukai-engine/ref/surfside'
os.makedirs(OUT, exist_ok=True)

# 大陪審の OCR（[x1,y1-x2,y2] 文）を頁ごとに
pages, cur = {}, None
for ln in open(S1 + '/ep19_view/gj_ocr.txt', encoding='utf-8'):
    m = re.match(r'^##\s.*?(gj_p\d+)\.png', ln)
    if m:
        cur = m.group(1)
        pages[cur] = []
        continue
    m = re.match(r'^\[(\d+),(\d+)-(\d+),(\d+)\]\s?(.*)$', ln.rstrip('\n'))
    if m and cur:
        pages[cur].append(tuple(int(m.group(i)) for i in range(1, 5)) + (m.group(5),))


def gj(name, pg, first, last, extra=0):
    """first に当たる行から last に当たる行までの帯を切る（extra 行ぶん下へ足す）。"""
    ls = sorted(pages[pg], key=lambda r: r[1])
    i0 = next(i for i, r in enumerate(ls) if re.search(first, r[4], re.I))
    i1 = max(i for i, r in enumerate(ls) if re.search(last, r[4], re.I) and i >= i0)
    i1 = min(len(ls) - 1, i1 + extra)
    band = ls[i0:i1 + 1]
    x0 = min(r[0] for r in band) - 20
    y0 = band[0][1] - 14
    x1 = max(r[2] for r in band) + 20
    y1 = band[-1][3] + 14
    im = Image.open(S1 + '/ep19_view/gj/%s.png' % pg).crop((max(0, x0), max(0, y0), x1, y1))
    p = os.path.join(OUT, name + '.png')
    im.save(p)
    print(name, pg, '行', i0, '〜', i1, im.size)


def pdfcrop(name, path, pno, needles, pad=(40, 60)):
    """文字の層で needles を探し、当たった所の上下を切る（2倍で描く）。"""
    doc = fitz.open(path)
    page = doc[pno - 1]
    hits = []
    for nd in needles:
        hits += page.search_for(nd)
    if not hits:
        print(name, '🔴 文字の層に無い:', needles)
        return
    r = fitz.Rect(page.rect.x0 + 20, min(h.y0 for h in hits) - pad[0],
                  page.rect.x1 - 20, max(h.y1 for h in hits) + pad[1])
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2), clip=r)
    p = os.path.join(OUT, name + '.png')
    pix.save(p)
    print(name, os.path.basename(path), 'p%d' % pno, '当たり', len(hits), (pix.width, pix.height))


def shrink(name, src, width):
    im = Image.open(src)
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    p = os.path.join(OUT, name + '.png')
    im.convert('RGB').save(p)
    print(name, os.path.basename(src), im.size)


# 組1：GJ p.1（c706・cc02・cc04）／GJ p.18（c414・c416・cc03・cc04）／MC18 p.7（c311）／MIN18 p.7（c404）
gj('a1_gj_p1', 'gj_p04', r'Except for a 14', r'participants\.?$|^participants')
gj('a2_gj_p18', 'gj_p21', r'accelerat', r'quickly', extra=0)
pdfcrop('a3_mc18_p7', SRC + '/surfside_morabito_2018-10-08_structural_field_survey.pdf', 7,
        ['major structural damage', 'failed'])
pdfcrop('a4_min18_p7', SRC + '/surfside_cts_board_minutes_2018-11-15.pdf', 7, ['very good shape'])
# 組2：TF p50 の門（c505）／TF p57 の注記（c517）／TF p185（cb07）／GJ p.20（cc07〜cc10）
shrink('b1_tf_p50_gate', SURF + '/tf_p050_gate.jpg', 1100)
shrink('b2_tf_p57_memo', SURF + '/tf_p057_memo.jpg', 1100)
shrink('b3_tf_p185', SURF + '/tf_p185_87park.jpg', 1500)
gj('b4_gj_p20', 'gj_p23', r'Crestview Towers is a', r'evacuate the', extra=1)
# 組3：GJ p.3（cc06 の「もっと早く」）
gj('c1_gj_p3', 'gj_p06', r'host|reasons', r'earlier', extra=0)
