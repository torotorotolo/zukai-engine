# -*- coding: utf-8 -*-
"""30本目④'：手記の「行の継ぎ目の読み違い」を全数で当てる（c807・c808 の型＝文字の層の行が逆順に出て、問いと答えの向きを取り違えた）。

  python -I -X utf8 ref/ep30/v2_build/seam30.py [台本]     # 既定＝第1版

すること：
 1. src/shuki/*.pdf の文字を、頁の座標（上から下・左から右）で並べ直して src/shuki/shuki_sorted.txt に書く（git の外）。
    頁の見出しは shuki_ocr.txt と同じ形にしないので、読むときは skipgrep.py か ctx30.py を通す（線の文は丸ごと伏せる）。
 2. 台本の出典の欄の手記の片（手助役・手運転士・手警部補・手機関員・手院長）を、並べ直した写しの字に当てる。
    「OCR の写しには当たるが、正しい順の写しには当たらない片」＝継ぎ目をまたいだ片の疑い、として出す。
 3. 語りの字は出さない。片（台本の出典の欄にある字）とカット番号だけを出す。資料の本文は出さない。
"""
import glob
import os
import re
import sys

import fitz

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
SH = os.path.join(EP, 'src', 'shuki')
OUT = os.path.join(SH, 'shuki_sorted.txt')
TAGS = {'手助役': 'joyaku', '手運転士': 'unten', '手警部補': 'keibuho', '手機関員': 'shobo', '手院長': 'innchou'}
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
SPACE = re.compile(r'\s+')


def squeeze(s):
    return SPACE.sub('', s)


def page_lines(page):
    """頁の文字を行ごとに、上から下・左から右へ。"""
    rows = []
    for b in page.get_text('dict')['blocks']:
        for ln in b.get('lines', []):
            t = ''.join(sp['text'] for sp in ln['spans']).strip()
            if t:
                rows.append((round(ln['bbox'][1] / 3), ln['bbox'][0], t))
    rows.sort()
    return [r[2] for r in rows]


def build():
    out = {}
    for f in sorted(glob.glob(os.path.join(SH, '*.pdf'))):
        name = os.path.splitext(os.path.basename(f))[0]
        d = fitz.open(f)
        out[name] = [page_lines(p) for p in d]
    with open(OUT, 'w', encoding='utf-8', newline='\n') as w:
        for name, pages in out.items():
            for i, lines in enumerate(pages, 1):
                w.write('=== %s_p%d ===\n' % (name, i))
                w.write('\n'.join(lines) + '\n')
    return out


def frags(path):
    """出典の欄の手記の片を（カット, 札, 片）で。"""
    rows = []
    for ln in open(path, encoding='utf-8'):
        m = CUT.match(ln)
        if not m:     # 出典の欄は見出しの行の末尾（`**c101** ／ 画 ／ 出典`）
            continue
        cur = m.group(1)
        for tag, frag in re.findall(r'(手助役|手運転士|手警部補|手機関員|手院長)（`([^`]+)`', ln):
            rows.append((cur, tag, frag))
    return rows


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(EP, 'daihon_v1.md')
    pages = build()
    joined = {k: squeeze(''.join(''.join(p) for p in v)) for k, v in pages.items()}
    ocr = squeeze(open(os.path.join(SH, 'shuki_ocr.txt'), encoding='utf-8').read())
    rows = frags(path)
    bad, both = [], 0
    for cut, tag, frag in rows:
        z = squeeze(frag)
        in_sorted = z in joined.get(TAGS[tag], '')
        in_ocr = z in ocr
        if in_sorted:
            both += 1
        else:
            bad.append((cut, tag, frag, in_ocr))
    print('手記の片 %d・正しい順の写しに当たる %d・当たらない %d' % (len(rows), both, len(bad)))
    for cut, tag, frag, in_ocr in bad:
        print('  %s %s 「%s」 OCR の写し=%s' % (cut, tag, frag, '当たる（継ぎ目の疑い）' if in_ocr else '当たらない'))
    print('→ 写し', OUT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
