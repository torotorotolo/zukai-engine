# -*- coding: utf-8 -*-
"""21本目④'：一次資料を引く小道具（照合の係も G0 も同じ物差しで原文を見る・2026-10-11・20本目 pg20.py の考え方を写した）。

  python ref/ep21/v2_build/pg21.py page 委員会報告 21        # 委員会報告の印字 p21（PDF＝印字＋18・文字の層のまま）
  python ref/ep21/v2_build/pg21.py page 委員会報告 xv        # 前付け（ローマ数字）
  python ref/ep21/v2_build/pg21.py page スタッフ声明 15      # スタッフ声明 No.17 の PDF の頁
  python ref/ep21/v2_build/pg21.py page NIST 83              # NIST NCSTAR 1 の PDF の頁（文字の層＝OCR 並み）
  python ref/ep21/v2_build/pg21.py find "nine minutes" [--in 委員会報告|スタッフ声明|NIST|NIST1A|CVR|NTSB11|NTSB175|NTSB77|NTSB93|運輸長官の証言|国立公園局|AP|法律|検視局|記念館|監察総監|sources|all] [--ctx 300] [--max 30]
  python ref/ep21/v2_build/pg21.py sec 11-1                  # sources.md の節（### 11-1. …）をそのまま出す

find の揃え＝NFKC・小文字・空白を消す・ダッシュと引用符の揺れを揃える・行末のハイフンを消した形でも探す。
当たった所は「元の字（改行こみ）」で前後 ctx 字を出す。委員会報告は「印字の頁」で名乗る。
⚠️ 「0件」は「無い」ではない（言い換え・OCR の誤り・頁の境目）。同じ意味の語を3つ以上当ててから「無い」と書く。
⚠️ NTSB の4本・CVR（P200056T）・NIST は OCR の字＝引く文は sources.md §11-1（②が原寸で見た写し）を正とする。
⚠️ 頁の境目で文が割れる＝前後の頁の終わりと始まりも読む。
"""
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\konar\Desktop\zukai-engine'
EP = os.path.join(ROOT, 'ref', 'ep21')
CORE = os.path.join(EP, 'src', 'core_raw')
WEB4 = os.path.join(EP, 'src', 'new', 'web4')
NTSB = {'NTSB11': 'AA11', 'NTSB175': 'UA175', 'NTSB77': 'AA77', 'NTSB93': 'UA93'}
FLAT = {'国立公園局': 'nps', 'AP': 'ap_seattletimes', '法律': 'pl107_71', '検視局': 'ocme',
        '記念館': 'memorial_faq', '監察総監': 'afmag_dot'}
ROMAN = {'i': 1, 'v': 5, 'x': 10, 'l': 50}


def roman(s):
    v, prev = 0, 0
    for ch in reversed(s.lower()):
        n = ROMAN[ch]
        v = v - n if n < prev else v + n
        prev = max(prev, n)
    return v


def nchar(ch):
    s = unicodedata.normalize('NFKC', ch).lower()
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'[‐‑‒–—―−－ｰ]', '-', s)
    return s.replace('’', "'").replace('‘', "'").replace('”', '"').replace('“', '"').replace('\u00ad', '')


def norm_map(raw):
    """揃えた字列と、揃えた字ごとの元の位置。"""
    out, idx = [], []
    for i, ch in enumerate(raw):
        for c in nchar(ch):
            out.append(c)
            idx.append(i)
    return ''.join(out), idx


def jsonl(path):
    out = []
    for line in open(path, encoding='utf-8'):
        d = json.loads(line)
        out.append((d['pdf_page'], d.get('raw') or ''))
    return out


def txt(path):
    return open(path, encoding='utf-8', errors='replace').read() if os.path.exists(path) else ''


def docs():
    """名前 → [(頁の名乗り, 元の字)]"""
    D = {}
    D['委員会報告'] = [(cr_label(p), t) for p, t in jsonl(os.path.join(CORE, 'GPO-911REPORT.pages.jsonl'))]
    D['スタッフ声明'] = [('スタッフ声明 PDF p%d' % p, t) for p, t in jsonl(os.path.join(CORE, 'staff17.pages.jsonl'))]
    D['NIST'] = [('NCSTAR 1 PDF p%d' % p, t) for p, t in jsonl(os.path.join(CORE, 'ncstar1.pages.jsonl'))]
    D['NIST1A'] = [('NCSTAR 1A PDF p%d' % p, t) for p, t in jsonl(os.path.join(CORE, 'ncstar1a.pages.jsonl'))]
    D['CVR'] = [('P200056T OCR', txt(os.path.join(CORE, 'P200056T.ocr.txt')))]
    for k, f in NTSB.items():
        D[k] = [('%s OCR' % k, txt(os.path.join(ROOT, 'analytics', 'materials', 'ep7', 's2', 'ocr', f + '.ocr.txt')))]
    D['運輸長官の証言'] = [('transcript_0523', txt(os.path.join(EP, 'src', 'new', 'hearing2', 'transcript_0523.txt')))]
    for k, f in FLAT.items():
        D[k] = [(f + '.txt', txt(os.path.join(WEB4, f + '.txt')))]
    D['sources'] = [('sources.md', txt(os.path.join(EP, 'sources.md')))]
    return D


def cr_label(pdf):
    if pdf <= 18:
        return '委員会報告 PDF p%d（前付け）' % pdf
    return '委員会報告 p%d（PDF %d）' % (pdf - 18, pdf)


def cmd_page(doc, p):
    if doc == '委員会報告':
        pdf = roman(p) if re.fullmatch(r'[ivxl]+', p.lower()) else int(p) + 18
        rows = jsonl(os.path.join(CORE, 'GPO-911REPORT.pages.jsonl'))
    elif doc == 'スタッフ声明':
        pdf, rows = int(p), jsonl(os.path.join(CORE, 'staff17.pages.jsonl'))
    elif doc in ('NIST', 'NIST1A'):
        pdf = int(p)
        rows = jsonl(os.path.join(CORE, 'ncstar1.pages.jsonl' if doc == 'NIST' else 'ncstar1a.pages.jsonl'))
    else:
        print('page は 委員会報告・スタッフ声明・NIST・NIST1A だけ（ほかは find を使う）')
        return 2
    for pp, t in rows:
        if pp == pdf:
            print('=== %s ===' % (cr_label(pp) if doc == '委員会報告' else '%s PDF p%d' % (doc, pp)))
            print(t)
            return 0
    print('その頁は無い')
    return 1


def cmd_find(q, where, ctx, mx):
    D = docs()
    keys = list(D) if where == 'all' else [where]
    nq = ''.join(nchar(c) for c in q)
    nq2 = nq.replace('-', '')
    n = 0
    for k in keys:
        for lab, raw in D.get(k, []):
            s, idx = norm_map(raw)
            # 1回目＝そのまま／2回目＝資料と問いの両方からハイフンを消した形（行末で割れた語 `cov- erage` を拾う）。
            # ⚠️ 2026-10-12 直した：もとは問いにハイフンが無いと2回目を飛ばしていた＝行末で割れた語が0件になった
            pairs = [(c, i) for c, i in zip(s, idx) if c != '-']
            s2, idx2 = ''.join(c for c, _ in pairs), [i for _, i in pairs]
            for target, ss, ii in ((nq, s, idx), (nq2, s2, idx2)):
                start = 0
                hit_any = False
                while True:
                    j = ss.find(target, start)
                    if j < 0 or not target:
                        break
                    hit_any = True
                    a, b = ii[j], ii[min(j + len(target) - 1, len(ii) - 1)]
                    lo, hi = max(0, a - ctx), min(len(raw), b + 1 + ctx)
                    print('--- [%s] %s ---' % (k, lab))
                    print(raw[lo:hi].replace('\n', ' ⏎ '))
                    n += 1
                    if n >= mx:
                        print('（%d件で打ち切り）' % mx)
                        return 0
                    start = j + 1
                if hit_any:
                    break
    print('== %d件 ==' % n)
    return 0 if n else 1


def cmd_sec(name):
    s = txt(os.path.join(EP, 'sources.md'))
    m = re.search(r'^### %s\..*?(?=^### |\Z)' % re.escape(name), s, re.S | re.M)
    print(m.group(0) if m else 'その節は無い')
    return 0 if m else 1


def main(a):
    if len(a) >= 3 and a[0] == 'page':
        return cmd_page(a[1], a[2])
    if len(a) >= 2 and a[0] == 'find':
        where, ctx, mx = 'all', 300, 30
        rest = a[2:]
        for i, x in enumerate(rest):
            if x == '--in':
                where = rest[i + 1]
            elif x == '--ctx':
                ctx = int(rest[i + 1])
            elif x == '--max':
                mx = int(rest[i + 1])
        return cmd_find(a[1], where, ctx, mx)
    if len(a) >= 2 and a[0] == 'sec':
        return cmd_sec(a[1])
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
