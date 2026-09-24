# -*- coding: utf-8 -*-
"""15本目②：ドケットの PDF の埋め込み画像（数・実寸）と、図・写真の説明文（Figure/Photo N）と出どころの語（courtesy 等）を出す。"""
import glob, os, re, sys
import fitz

SRC = r'C:/Users/konar/Desktop/zukai-engine/ref/ep15/src'
CAP = re.compile(r'^\s*(Figure|Fig\.|Photo(?:graph)?|Image)\s*([0-9]+[A-Za-z]?)[\.:\-–—\s]+(.{0,150})', re.I)
for f in sorted(glob.glob(SRC + '/ntsb_docket_*.pdf')):
    name = os.path.basename(f)
    try:
        d = fitz.open(f)
    except Exception as e:
        print('==', name, 'open error', e)
        continue
    sizes = []
    pages_with = 0
    for pno in range(d.page_count):
        imgs = d[pno].get_images(full=True)
        big = [(im[2], im[3]) for im in imgs if im[2] * im[3] >= 200 * 200]
        if big:
            pages_with += 1
        sizes += big
    ws = sorted((w for w, h in sizes), reverse=True)
    print('== %s  頁%d  画像(200px角以上)%d  画像のある頁%d  幅の最大%s 中央%s' % (name, d.page_count, len(sizes), pages_with, ws[0] if ws else '-', ws[len(ws) // 2] if ws else '-'))
    if not sizes:
        continue
    txt = os.path.splitext(f)[0] + '.txt'
    if not os.path.exists(txt):
        continue
    page = '?'
    caps = []
    credit = []
    for line in open(txt, encoding='utf-8', errors='replace'):
        m = re.match(r'=== p(\d+) ===', line)
        if m:
            page = m.group(1)
            continue
        c = CAP.match(line)
        if c:
            caps.append('p%s %s%s %s' % (page, c.group(1)[:3], c.group(2), c.group(3).strip()[:120]))
        if re.search(r'(?i)courtesy|©|copyright|photo by|provided by|photographer', line):
            credit.append('p%s %s' % (page, line.strip()[:120]))
    print('  説明文 %d 件' % len(caps))
    for c in caps[:200]:
        print('   ', c)
    if credit:
        print('  出どころの語 %d 件' % len(credit))
        for c in credit[:30]:
            print('   ', c)
