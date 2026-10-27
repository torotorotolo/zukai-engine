# -*- coding: utf-8 -*-
"""26本目 出典の欄の原文の片（バッククォートの中）を、一次資料の文字の層に機械で当てる（④・2026-10-27・25本目の quotes25.py を写し、
英語の資料＝英国の報告 S. Doc. 933・MAIB 1992・米国の法3本・米国の公聴会 S. Doc. 726 に替えた）。

  python ref/ep26/v1_build/quotes26.py ref/ep26/daihon_v1.md [--out 結果.tsv]
  python ref/ep26/v1_build/quotes26.py --selftest

なぜ要るか：決め所（★）が0＝tools/check_facts.py の照合が働かない（ルール 4-2 の「多文書の回」）。代わりに §4 の全カットの
「出典の欄」のバッククォートを、書いた資料と頁に当てる（照合の表＝出典の欄そのもの）。

資料（ref/ep26/src/＝git の外。記号は sources.md §1）：
  G1＝sd933_pages/pNNN.txt（PDF の頁＝印刷の頁）／G2＝maib_pages/pNNN.txt（印刷＝PDF−4・送り状＝PDF 3）＋OCR（maib_ocr.txt＝
  文字の層に緯度経度が無いため・OCR だけで当たったら「OK(OCR)」）／G4・G5・G6＝txt/stat*.txt（全文）／
  G7＝F:\\jiko_src\\ep26\\ の PDF（頁＝PDF の頁・当てる頁だけ fitz で取り出して src/sd726_pages/ に置く）。
  T1・T2・T3（有志の書き起こし＝保存していない）・N・U・A（web）は機械で当てない＝「書き起こし」「web」と出す。
揃え：英小文字と数字だけ（記号・引用符・改行の行末の - は消す）＝OCR の句読点の崩れに強くする（probe/sd726grep26.py と同じ）。
「…」で区切った6字以上の片を全部探す。頁またぎは前後の頁の端とつないでも探す。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属・条件節）は人が見る（④'）。
"""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
SRC = r'C:\Users\konar\Desktop\zukai-engine\ref\ep26\src'
G7_PDF = r'F:\jiko_src\ep26\SERIALSET-06167_00_00-002-0726-0000.pdf'
G7_CACHE = os.path.join(SRC, 'sd726_pages')
WHOLE = {'G4': 'txt/stat37_199.txt', 'G5': 'txt/stat37_302.txt', 'G6': 'txt/stat36_629.txt'}
NOCHECK = {'T1': '書き起こし', 'T2': '書き起こし', 'T3': '書き起こし', 'N1': 'web', 'N2': 'web', 'N3': 'web',
           'U1': 'web', 'A1': 'web'}
CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／\s*[^／]*／(.*)$')
TOK = re.compile(r'(?<![A-Za-z0-9])(?P<doc>G[1-7]|T[1-3]|N[1-3]|U1|A1)(?![0-9A-Za-z])'
                 r'|(?P<cover>送り状)'
                 r'|(?P<pg>p\.?\s*(?P<p1>\d+)(?:\s*[〜～~-]\s*(?P<p2>\d+))?)'
                 r'|`(?P<q>[^`]+)`')


def norm(s):
    s = (s or '').replace('\u00ad', '')
    s = re.sub(r'-\s*\n\s*', '', s)                  # 行末の分かち書き
    s = s.lower().replace('’', "'").replace('‘', "'")
    s = re.sub(r"[^a-z0-9]+", ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def pieces(q):
    return [p for p in (norm(x) for x in re.split(r'…|\.\.\.', q)) if len(p) >= 6]


def _pages_from_files(pattern, offset):
    out = {}
    for fn in glob.glob(pattern):
        m = re.search(r'p(\d+)\.txt$', fn)
        if m:
            out[int(m.group(1)) + offset] = norm(open(fn, encoding='utf-8', errors='replace').read())
    return out


def _maib_ocr():
    out, cur, buf = {}, None, []
    fn = os.path.join(SRC, 'maib_ocr.txt')
    if not os.path.exists(fn):
        return out
    for ln in open(fn, encoding='utf-8', errors='replace'):
        m = re.match(r'^## .*p(\d+)\.png', ln)
        if m:
            if cur is not None:
                out[cur - 4] = norm(' '.join(buf))
            cur, buf = int(m.group(1)), []
            continue
        buf.append(re.sub(r'^\[[^\]]*\]\s*', '', ln.strip()))
    if cur is not None:
        out[cur - 4] = norm(' '.join(buf))
    return out


def _g7_pages(pgs):
    os.makedirs(G7_CACHE, exist_ok=True)
    out, need = {}, []
    for p in pgs:
        fn = os.path.join(G7_CACHE, 'p%04d.txt' % p)
        if os.path.exists(fn):
            out[p] = norm(open(fn, encoding='utf-8').read())
        else:
            need.append(p)
    if need:
        import fitz
        doc = fitz.open(G7_PDF)
        for p in need:
            if 1 <= p <= doc.page_count:
                t = doc[p - 1].get_text()
                with open(os.path.join(G7_CACHE, 'p%04d.txt' % p), 'w', encoding='utf-8') as f:
                    f.write(t)
                out[p] = norm(t)
        doc.close()
    return out


_CACHE = {}


def pages_of(doc, pgs=()):
    if doc == 'G7':
        want = set()
        for p in pgs:
            want |= {p - 1, p, p + 1}
        got = _CACHE.setdefault('G7', {})
        miss = [p for p in sorted(want) if p not in got and p >= 1]
        if miss:
            got.update(_g7_pages(miss))
        return got
    if doc not in _CACHE:
        if doc == 'G1':
            _CACHE[doc] = _pages_from_files(os.path.join(SRC, 'sd933_pages', 'p*.txt'), 0)
        elif doc == 'G2':
            _CACHE[doc] = _pages_from_files(os.path.join(SRC, 'maib_pages', 'p*.txt'), -4)
            _CACHE['G2ocr'] = _maib_ocr()
        elif doc in WHOLE:
            _CACHE[doc] = {0: norm(open(os.path.join(SRC, WHOLE[doc]), encoding='utf-8', errors='replace').read())}
    return _CACHE[doc]


def _find(pages, p, pgs):
    hit = [k for k, txt in pages.items() if p in txt]
    for k in sorted(pages):                           # 頁またぎ（k の終わり＋k+1 の始まり）
        if k + 1 in pages:
            seam = pages[k][-300:] + ' ' + pages[k + 1][:300]
            if p in seam and k not in hit and k + 1 not in hit:
                hit.append(k)
    return hit


def judge(doc, pgs, q):
    if doc in NOCHECK:
        return NOCHECK[doc], ''
    if doc not in ('G1', 'G2', 'G7') and doc not in WHOLE:
        return '資料なし', ''
    pages = pages_of(doc, pgs)
    ps = pieces(q)
    if not ps:
        return '短い', ''
    worst, where = 'OK', []
    order = ['OK', 'OK(OCR)', '近', '別頁', '無し']
    for p in ps:
        if doc in WHOLE:
            v = 'OK' if p in pages[0] else '無し'
        else:
            hit = _find(pages, p, pgs)
            if pgs and any(k in pgs for k in hit):
                v = 'OK'
            elif pgs and any(abs(k - g) == 1 for k in hit for g in pgs):
                v = '近'
                where.append('p.%s' % ','.join(str(k) for k in hit[:3]))
            elif hit:
                v = '別頁' if pgs else 'OK'
                where.append('p.%s' % ','.join(str(k) for k in hit[:3]))
            else:
                v = '無し'
            if v != 'OK' and doc == 'G2':
                ocr = _CACHE.get('G2ocr', {})
                oh = [k for k, txt in ocr.items() if p in txt]
                if pgs and any(k in pgs for k in oh):
                    v = 'OK(OCR)'
        if order.index(v) > order.index(worst):
            worst = v
    return worst, ' '.join(where)


def scan(md):
    text = open(md, encoding='utf-8').read()
    on, out = False, []
    for ln in text.split('\n'):
        if ln.startswith('## 4. 台本'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        m = CUT_RE.match(ln) if on else None
        if not m:
            continue
        cid, src = m.group(1), m.group(2)
        doc, pgs = None, []
        for t in TOK.finditer(src):
            if t.group('doc'):
                doc, pgs = t.group('doc'), []
            elif t.group('cover'):
                pgs = [-1]
            elif t.group('pg'):
                a = int(t.group('p1'))
                b = int(t.group('p2')) if t.group('p2') else a
                pgs = list(range(a, b + 1))
            elif t.group('q') is not None and doc:
                v, where = judge(doc, pgs, t.group('q'))
                out.append((cid, doc, ','.join(map(str, pgs)), v, where, t.group('q')))
    return out


def main(md, out_path=None):
    rows = scan(md)
    cnt = {}
    for r in rows:
        cnt[r[3]] = cnt.get(r[3], 0) + 1
    print('片 %d ＝ %s' % (len(rows), '・'.join('%s %d' % kv for kv in sorted(cnt.items()))))
    for r in rows:
        if r[3] not in ('OK', 'OK(OCR)', '書き起こし', 'web'):
            print('  %s %s p.%s → %s %s ｜ %s' % r)
    if out_path:
        with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('cut\tdoc\tpages\tverdict\twhere\tquote\n')
            for r in rows:
                f.write('\t'.join(r) + '\n')
    return sum(1 for r in rows if r[3] not in ('OK', 'OK(OCR)', '書き起こし', 'web'))


def selftest():
    ok = norm('“Keep out.”') == 'keep out'
    ok &= pieces('might have saved many…lives that were lost') == ['might have saved many', 'lives that were lost']
    toks = [(m.group('doc'), m.group('p1'), m.group('cover')) for m in
            TOK.finditer('G1 p.60（`a`）・G2 p.18・G2 送り状・T1 Day 7 Q7921・G7 p.739')
            if m.group('doc') or m.group('pg') or m.group('cover')]
    ok &= toks == [('G1', None, None), (None, '60', None), ('G2', None, None), (None, '18', None), ('G2', None, None),
                   (None, None, '送り状'), ('T1', None, None), ('G7', None, None), (None, '739', None)]
    # 本物の資料で陽性対照（sources.md §2・§3・§4-3 で照合ずみの句）・別の頁・陰性対照
    ok &= judge('G1', [60], 'might have saved many if not all of the lives')[0] == 'OK'
    ok &= judge('G1', [59], 'might have saved many if not all of the lives')[0] == '近'
    ok &= judge('G1', [30], 'might have saved many if not all of the lives')[0] == '別頁'
    ok &= judge('G1', [60], 'the Californian could not have saved anyone')[0] == '無し'
    ok &= judge('G1', [85], 'She made no attempt')[0] == 'OK'
    ok &= judge('G2', [19], 'there are no villains in this story')[0] == 'OK'
    ok &= judge('G2', [-1], 'full endorse the Deputy Chief Inspector')[0] == 'OK'
    ok &= judge('G2', [18], 'attempt should have been made')[0] == 'OK'
    ok &= judge('G4', [], 'one or the other of whom shall be')[0] == 'OK'
    ok &= judge('T1', [], 'Keep out')[0] == '書き起こし'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    op = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], op) else 0)
