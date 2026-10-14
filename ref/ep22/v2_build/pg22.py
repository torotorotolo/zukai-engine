# -*- coding: utf-8 -*-
"""22本目④'：3冊の原文を引く小道具（照合の係も G0 も同じ物差しで原文を見る・2026-10-14・21本目 pg21.py の考え方を写した）。

  python ref/ep22/v2_build/pg22.py page USCG 35        # USCG の PDF の頁 35（印字＝PDF−8 を名乗りに添える）
  python ref/ep22/v2_build/pg22.py page NTSB 44        # NTSB MIR-25-36 の PDF の頁
  python ref/ep22/v2_build/pg22.py sec 1.3.2           # TSB の節（見出しの行から次の見出しの行まで）。付録は A／B／C
  python ref/ep22/v2_build/pg22.py fn 45               # TSB の脚注
  python ref/ep22/v2_build/pg22.py find "loud bang" [--in USCG|NTSB|TSB|TSB_A|TSB_B|LAB|kousei|sources|legend|cards|all] [--ctx 300] [--max 30]

find の揃え＝NFKC・小文字・空白を消す・ダッシュと引用符の揺れを揃える・行末のハイフンを消した形でも探す。
当たった所は「元の字（改行は ⏎）」で前後 ctx 字を出し、USCG は「p.PDF〈印字〉」、TSB は節・脚注の番号で名乗る。
⚠️ 「0件」は「無い」ではない（言い換え・頁の境目・表のセル）。同じ意味の語を3つ以上当ててから「無い」と書く。
⚠️ 頁の境目で文が割れる＝前後の頁の終わりと始まりも読む。
⚠️ LAB（NTSB 研究所 24-011）は3冊の外＝画の出どころだけ。語りの事実は3冊の字で引く。
⚠️ --in の既定は 3冊（USCG・NTSB・TSB・TSB_A・TSB_B）。設計図とカードは名指しで。
"""
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\konar\Desktop\zukai-engine'
EP = os.path.join(ROOT, 'ref', 'ep22')
SRC = os.path.join(EP, 'src')
PAGE = re.compile(r'^=== PDF p\.(\d+) ｜ 印字 p\.\S+ ===\s*$', re.M)
HEAD = re.compile(r'^(\d+(?:\.\d+)*)[ \u00a0]+([A-Z][^\n]{0,150})$')
BOOKS = ['USCG', 'NTSB', 'TSB', 'TSB_A', 'TSB_B']


def nchar(ch):
    s = unicodedata.normalize('NFKC', ch).lower()
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'[‐‑‒–—―−－ｰ]', '-', s)
    return s.replace('’', "'").replace('‘', "'").replace('”', '"').replace('“', '"').replace('\u00ad', '')


def norm_map(raw):
    out, idx = [], []
    for i, ch in enumerate(raw):
        for c in nchar(ch):
            out.append(c)
            idx.append(i)
    return ''.join(out), idx


def txt(path):
    return open(path, encoding='utf-8', errors='replace').read() if os.path.exists(path) else ''


def pages(path):
    raw = txt(path)
    out = []
    ms = list(PAGE.finditer(raw))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(raw)
        out.append((int(m.group(1)), raw[m.end():end]))
    return out


def tsb_parts():
    """[(名乗り, 元の字)]＝本文の節・付録・脚注。"""
    lines = txt(os.path.join(SRC, 'tsb_m23a0169_html.txt')).split('\n')
    out, cur, buf = [], '前', []
    fn_start = None
    for i, ln in enumerate(lines):
        if ln.strip() == 'Footnotes':
            fn_start = i
            break
        s = ln.strip()
        m = HEAD.match(s)
        app = re.match(r'^Appendix[ \u00a0]+([A-C])\b', s)
        if (m and not s.endswith('.')) or app:
            out.append((cur, '\n'.join(buf)))
            cur = ('付録' + app.group(1)) if app else ('§' + m.group(1))
            buf = [ln]
        else:
            buf.append(ln)
    out.append((cur, '\n'.join(buf)))
    if fn_start is not None:
        # 形＝「45」⏎ 空行 ⏎ 本文 ⏎ 空行 ⏎「Return to footnote」⏎「45」⏎「referrer」（戻りの番号は読み飛ばす）
        rest = lines[fn_start + 1:]
        num, body, back = None, [], False
        for ln in rest:
            s = ln.strip()
            if s == 'referrer':
                continue
            if re.fullmatch(r'\d+', s) and num is None:
                if back:
                    back = False
                    continue
                num, body = s, []
            elif s.startswith('Return to footnote'):
                if num is not None:
                    out.append(('脚注' + num, '\n'.join(body).strip()))
                num, back = None, True
            elif num is not None:
                body.append(ln)
    return out


def docs():
    D = {}
    D['USCG'] = [('USCG p.%d〈%d〉' % (p, p - 8), t) for p, t in pages(os.path.join(SRC, 'uscg_mbi_pages.txt'))]
    D['NTSB'] = [('NTSB p.%d' % p, t) for p, t in pages(os.path.join(SRC, 'ntsb_mir2536_pages.txt'))]
    D['TSB'] = [('TSB ' + k, t) for k, t in tsb_parts()]
    D['TSB_A'] = [('TSB 付録A（tsv）', txt(os.path.join(SRC, 'core_raw', 'tsb_appxA.tsv')))]
    D['TSB_B'] = [('TSB 付録B（tsv）', txt(os.path.join(SRC, 'core_raw', 'tsb_appxB.tsv')))]
    D['LAB'] = [('24-011（3冊の外）', txt(os.path.join(SRC, 'materials_raw', 'ntsb_docket_pdf', 'lab24011.txt')))]
    for k, f in (('kousei', 'kousei.md'), ('sources', 'sources.md'), ('legend', 'legend_2026-10-13.md')):
        D[k] = [(f, txt(os.path.join(EP, f)))]
    cd = os.path.join(SRC, 'cards')
    D['cards'] = [(f, txt(os.path.join(cd, f))) for f in sorted(os.listdir(cd))] if os.path.isdir(cd) else []
    return D


def cmd_page(doc, p):
    p = int(p)
    for pp, t in pages(os.path.join(SRC, 'uscg_mbi_pages.txt' if doc == 'USCG' else 'ntsb_mir2536_pages.txt')):
        if pp == p:
            print('=== %s p.%d%s ===' % (doc, pp, '〈%d〉' % (pp - 8) if doc == 'USCG' else ''))
            print(t)
            return 0
    print('その頁は無い')
    return 1


def cmd_sec(name):
    want = name if name.startswith(('§', '付録', '脚注')) else (('付録' + name) if name in 'ABC' else '§' + name)
    n = 0
    for k, t in tsb_parts():
        if k == want:
            print('=== TSB %s ===' % k)
            print(t)
            n += 1
    if not n:
        print('その節は無い（見出しの番号を確かめる）')
    return 0 if n else 1


def cmd_find(q, where, ctx, mx):
    D = docs()
    keys = BOOKS if where == 'books' else (list(D) if where == 'all' else [where])
    nq = ''.join(nchar(c) for c in q)
    nq2 = nq.replace('-', '')
    n = 0
    for k in keys:
        for lab, raw in D.get(k, []):
            s, idx = norm_map(raw)
            pairs = [(c, i) for c, i in zip(s, idx) if c != '-']
            s2, idx2 = ''.join(c for c, _ in pairs), [i for _, i in pairs]
            for target, ss, ii in ((nq, s, idx), (nq2, s2, idx2)):
                start, hit_any = 0, False
                while target:
                    j = ss.find(target, start)
                    if j < 0:
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


def main(a):
    if len(a) >= 3 and a[0] == 'page' and a[1] in ('USCG', 'NTSB'):
        return cmd_page(a[1], a[2])
    if len(a) >= 2 and a[0] == 'sec':
        return cmd_sec(a[1])
    if len(a) >= 2 and a[0] == 'fn':
        return cmd_sec('脚注' + a[1])
    if len(a) >= 2 and a[0] == 'find':
        where, ctx, mx = 'books', 300, 30
        rest = a[2:]
        for i, x in enumerate(rest):
            if x == '--in':
                where = rest[i + 1]
            elif x == '--ctx':
                ctx = int(rest[i + 1])
            elif x == '--max':
                mx = int(rest[i + 1])
        return cmd_find(a[1], where, ctx, mx)
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
