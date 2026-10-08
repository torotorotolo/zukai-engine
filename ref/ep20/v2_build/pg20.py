# -*- coding: utf-8 -*-
"""20本目④'：一次資料を引く小道具（係もG0も同じ物差しで原文を見る・2026-10-08）。

  python ref/ep20/v2_build/pg20.py page 報告書 98          # 報告書の印刷 p.98（文字の層・NFKC・行のまま）
  python ref/ep20/v2_build/pg20.py page 報告書 PDF3        # ja_01 の PDF p.3（前付け＝印刷の頁が無い所）
  python ref/ep20/v2_build/pg20.py page 解説 15            # 解説（2011）印字 p.15（i〜v も可）
  python ref/ep20/v2_build/pg20.py find 推定される [--in 報告書|解説|別添6|別添1|付録|sources|防衛庁|all] [--ctx 60] [--max 40]
  python ref/ep20/v2_build/pg20.py cvr 18:50               # 別添6（CVR）の OCR を、その分の列ごとに（原寸で見た字は sources.md §7-2 が正）
  python ref/ep20/v2_build/pg20.py sec 7-2                 # sources.md の節（### 7-2. …）をそのまま出す

揃え（find）＝NFKC・空白を消す・ダッシュ／波線／中黒の揺れを揃える（行をまたぐ語も当たる）。
⚠️ 「0件」は「無い」ではない（言い換え・OCR の誤り・頁の境目）。同義語を3つ以上当ててから「無い」と書く。
⚠️ 別添1 本文（ja_09）・付録（ja_huroku）・別添6（ja_11）は文字の層が無く OCR の写しだけ＝引く文は原寸で確かめる（係は「親へ（原寸）」と返す）。
"""
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\konar\Desktop\zukai-engine\ref\ep20'
SRC = os.path.join(ROOT, 'src')


def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'[‐‑‒–—―−－ｰ]', '-', s)
    s = s.replace('～', '〜').replace('~', '〜').replace('•', '・').replace('·', '・')
    s = s.replace('’', "'").replace('‘', "'").replace('”', '"').replace('“', '"')
    return s


def load_pages():
    out = []
    for line in open(os.path.join(SRC, 'pages.jsonl'), encoding='utf-8'):
        d = json.loads(line)
        out.append(d)
    return out


def label(d):
    f = d['file']
    pp = d.get('printed_page')
    if f == 'jtsb_kaisetsu.pdf':
        return '解説 p.%s' % pp
    if pp:
        return '報告書 p.%s（%s PDF%d）' % (pp, f, d['pdf_page'])
    return '報告書 %s PDF%d' % (f, d['pdf_page'])


def cmd_page(doc, p):
    pages = load_pages()
    hit = []
    for d in pages:
        if doc == '解説':
            if d['file'] == 'jtsb_kaisetsu.pdf' and str(d.get('printed_page')) == p:
                hit.append(d)
        else:
            if d['file'] == 'jtsb_kaisetsu.pdf':
                continue
            if p.upper().startswith('PDF'):
                if d['file'] == 'ja_01.pdf' and d['pdf_page'] == int(p[3:]):
                    hit.append(d)
            elif str(d.get('printed_page')) == p:
                hit.append(d)
    if not hit:
        print('（その頁は文字の層に無い：%s %s）' % (doc, p))
        return 1
    for d in hit:
        print('=== %s ===' % label(d))
        t = unicodedata.normalize('NFKC', d.get('text') or '')
        print(t if t.strip() else '（文字の層が空＝画像だけの頁。OCR の写しか原寸で）')
    return 0


def corpora(which):
    """(名前, 平らにした本文) の並び。"""
    out = []
    if which in ('報告書', '解説', 'all'):
        for d in load_pages():
            isk = d['file'] == 'jtsb_kaisetsu.pdf'
            if which == '報告書' and isk:
                continue
            if which == '解説' and not isk:
                continue
            out.append((label(d), norm(d.get('text'))))
    if which in ('別添6', 'all'):
        cols = {}
        for ln in open(os.path.join(SRC, 'ja_11_cvr_ocr300.tsv'), encoding='utf-8'):
            f = ln.rstrip('\n').split('\t')
            if len(f) >= 6 and f[1].isdigit():
                cols.setdefault(f[1], []).append(f[5])
        for p, chs in cols.items():
            out.append(('別添6 OCR p.%s' % p, norm(''.join(chs))))
    if which in ('別添1', 'all'):
        out += ocr_pages('ja_09_p15-18_ocr200.txt', '別添1 OCR', 230 - 1 + 15 - 15)
    if which in ('付録', 'all'):
        out += ocr_pages('ja_huroku_p1-8_ocr200.txt', '付録 OCR', 0)
    if which in ('sources', 'all'):
        for name in ('sources.md', 'kousei.md', 'materials.md', 'claims_check_2026-10-07.md', 'legend_2026-10-07.md'):
            t = open(os.path.join(ROOT, name), encoding='utf-8').read()
            for i, ln in enumerate(t.split('\n'), 1):
                out.append(('%s:%d' % (name, i), norm(ln)))
    if which in ('防衛庁', 'all'):
        t = open(os.path.join(SRC, 'bouei60_autosub_2340-2550.txt'), encoding='utf-8').read()
        out.append(('防衛庁の記録映画 自動字幕 23:40〜25:50', norm(t)))
    return out


def ocr_pages(fn, name, _):
    t = open(os.path.join(SRC, fn), encoding='utf-8').read()
    out = []
    for blk in re.split(r'^## ', t, flags=re.M)[1:]:
        head, body = blk.split('\n', 1) if '\n' in blk else (blk, '')
        m = re.search(r'_p(\d+)_\d+\.png', head)
        body = re.sub(r'\[\d+,\d+-\d+,\d+\]', '', body)
        out.append(('%s（PDF p.%s）' % (name, m.group(1) if m else '?'), norm(body)))
    return out


def cmd_find(q, which='all', ctx=60, mx=40):
    key = norm(q)
    n = 0
    for name, t in corpora(which):
        for m in re.finditer(re.escape(key), t):
            n += 1
            if n <= mx:
                a, b = max(0, m.start() - ctx), min(len(t), m.end() + ctx)
                print('%s ｜ …%s【%s】%s…' % (name, t[a:m.start()], t[m.start():m.end()], t[m.end():b]))
    print('== %d件（%s・揃えた語＝%s）' % (n, which, key))
    return 0


def cmd_cvr(hm):
    h, m = hm.split(':')
    rows = {}
    for ln in open(os.path.join(SRC, 'ja_11_cvr_ocr300.tsv'), encoding='utf-8'):
        f = ln.rstrip('\n').split('\t')
        if len(f) < 6 or not f[1].isdigit():
            continue
        if f[2] != str(int(m)):
            continue
        rows.setdefault((int(f[1]), int(f[4])), []).append((f[3], f[5]))
    if not rows:
        print('（%s の行が OCR に無い）' % hm)
        return 1
    print('⚠️ OCR の写し（縦書きの列ごと・右から）。原寸で見た字は `pg20.py sec 7-2`')
    for (p, x) in sorted(rows, key=lambda k: (k[0], -k[1])):
        chs = rows[(p, x)]
        print('p.%d %s:%s 秒≈%s x=%d ｜ %s' % (p, h, m, chs[0][0], x, ''.join(c for _, c in chs)))
    return 0


def cmd_sec(num):
    t = open(os.path.join(ROOT, 'sources.md'), encoding='utf-8').read()
    m = re.search(r'^#{2,3} %s[\. ].*?(?=^#{2,3} |\Z)' % re.escape(num), t, re.S | re.M)
    print(m.group(0) if m else '（sources.md に節 %s が無い）' % num)
    return 0 if m else 1


def main(a):
    if not a:
        print(__doc__)
        return 2
    if a[0] == 'page':
        return cmd_page(a[1], a[2])
    if a[0] == 'find':
        which = a[a.index('--in') + 1] if '--in' in a else 'all'
        ctx = int(a[a.index('--ctx') + 1]) if '--ctx' in a else 60
        mx = int(a[a.index('--max') + 1]) if '--max' in a else 40
        return cmd_find(a[1], which, ctx, mx)
    if a[0] == 'cvr':
        return cmd_cvr(a[1])
    if a[0] == 'sec':
        return cmd_sec(a[1])
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
