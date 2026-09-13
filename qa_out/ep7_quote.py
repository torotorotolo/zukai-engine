# -*- coding: utf-8 -*-
"""9/11委員会報告の原文に当てる小道具。パターンごとに前後の文脈を出す。"""
import re, sys, io
sys.stdout.reconfigure(encoding='utf-8')
P = r"C:/Users/konar/Desktop/zukai-engine/analytics/materials/ep7/GPO-911REPORT.pdf.txt"
T = open(P, encoding='utf-8', errors='replace').read()
# OCR/抽出の癖：改行と連続空白を詰めた版でも探す
FLAT = re.sub(r'\s+', ' ', T)
def show(pat, win=240, limit=6, flat=True):
    src = FLAT if flat else T
    hits = list(re.finditer(pat, src, re.I))
    print('=== %s  → %d件' % (pat, len(hits)))
    for m in hits[:limit]:
        a = max(0, m.start()-win); b = min(len(src), m.end()+win)
        print('  …' + src[a:b].replace('\n', ' ') + '…')
        print('  ---')
if __name__ == '__main__':
    for pat in sys.argv[1:]:
        show(pat)
