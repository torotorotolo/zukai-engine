# -*- coding: utf-8 -*-
"""23本目④'：韓国語の一次資料の文字の層を引く道具（照合の係と G0 が同じ物差しで原文を引く・22本目 pg22.py の考え方）。

  python ref/ep23/v2_build/pg23.py page K6 47            # K6 の印刷の頁 p.47 をそのまま出す（K6-R／市／区／検／市b／区b は同じ K6）
  python ref/ep23/v2_build/pg23.py page K6 51 53         # p.51〜p.53
  python ref/ep23/v2_build/pg23.py find K6 당장붕괴위험     # 空白を除いて探す（頁の境をまたいでも当たる）・前後の原文を出す
  python ref/ep23/v2_build/pg23.py find all 냉각탑 --ctx 200 --max 30
  python ref/ep23/v2_build/pg23.py find 大96 보강조치
  python ref/ep23/v2_build/pg23.py --selftest

資料（どれも ref/ep10/src/ の下＝git の外・読むだけ）：
  K6＝国会 三豊特委 第6号会議録（1995-09-12）。頁の印「=== [PDF p.N] ===」＝印刷の頁。
      R＝報告書の本文 pp.28〜34／市＝ソウル市 95.7.20 pp.34〜42／区＝瑞草区 95.7.20 pp.42〜45／
      検＝ソウル地検 95.7.28 pp.45〜53（別紙1〜3＝pp.51〜53）／市b＝ソウル市 95.8.9 pp.53〜58／区b＝瑞草区 95.8.9 pp.58〜59／
      問＝委員の質問の要旨 pp.9〜27＝🔴 認定ではない
  国監内＝1995年国政監査 内務委 ソウル市（10-10）／国監建＝建設交通委 ソウル市（10-11）＝同じ頁の印
  大96＝大法院 96도1231（刑事・全文）／大99＝大法院 98다29797（民事）／高96＝ソウル高法 96노118（主文など公開部分）＝頁なし
⚠️ 文字の層の癖：K6-検 p.52 は表の欄が文に割り込む／p.47 の「대책회의 중이던」のあとは名前／韓国語は空白を除いて当てる（この道具は空白を除いて探す）。
⚠️ 出力には名前が出てくる＝リポのファイル・係の記録には名前を写さない（役職で書く）。
"""
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
SRC = r'C:\Users\konar\Desktop\zukai-engine\ref\ep10\src'
FILES = {
    'K6': 'assembly_sampoong_tokui_no6_19950912_id19114.txt',
    '国監内': 'assembly_audit1995_naemu_seoul_19951010_id19476.txt',
    '国監建': 'assembly_audit1995_geonseol_seoul_19951011_id19502.txt',
    '大96': 'lawgokr_prec114109_96do1231.txt',
    '大99': 'lawgokr_prec79152_98da29797.txt',
    '高96': 'casenote_seoulhigh_96no118_visible.txt',
}
PAGED = {'K6', '国監内', '国監建'}
PAGE = re.compile(r'^=== \[PDF p\.(\d+)\] ===\s*$', re.M)
ALIAS = {'K6-R': 'K6', 'K6-市': 'K6', 'K6-区': 'K6', 'K6-検': 'K6', 'K6-市b': 'K6', 'K6-区b': 'K6', 'K6-問': 'K6',
         'R': 'K6', '検': 'K6', '市': 'K6', '区': 'K6', '内': '国監内', '建': '国監建'}


def doc_name(d):
    d = ALIAS.get(d, d)
    if d not in FILES:
        sys.exit('資料の名が違う: %s（%s）' % (d, '・'.join(FILES)))
    return d


def raw(doc):
    return open(os.path.join(SRC, FILES[doc]), encoding='utf-8', errors='replace').read()


def nchar(c):
    c = unicodedata.normalize('NFKC', c)
    c = re.sub(r'\s+', '', c)
    c = re.sub(r'[‘’“”\'"`]', '', c)
    c = re.sub(r'[·・ㆍ･]', '·', c)
    c = re.sub(r'[～∼〜~]', '~', c)
    c = re.sub(r'[‐‑‒–—―−－ｰ]', '-', c)
    return c


def norm_map(s):
    """揃えた字の並びと、その1字ずつの元の位置。"""
    out, pos = [], []
    for i, ch in enumerate(s):
        n = nchar(ch)
        for x in n:
            out.append(x)
            pos.append(i)
    return ''.join(out), pos


def pages(s):
    ms = list(PAGE.finditer(s))
    return [(int(m.group(1)), m.start(), ms[k + 1].start() if k + 1 < len(ms) else len(s)) for k, m in enumerate(ms)]


def page_of(pgs, i):
    p = None
    for n, a, _ in pgs:
        if a <= i:
            p = n
    return p


def cmd_page(doc, p1, p2):
    doc = doc_name(doc)
    if doc not in PAGED:
        sys.exit('%s は頁が無い＝find か、ファイルを Read で読む' % doc)
    s = raw(doc)
    hit = 0
    for n, a, b in pages(s):
        if p1 <= n <= p2:
            print(s[a:b].rstrip())
            hit += 1
    if not hit:
        sys.exit('頁が無い: %s p.%d〜%d' % (doc, p1, p2))


def cmd_find(doc, q, ctx, mx):
    docs = list(FILES) if doc == 'all' else [doc_name(doc)]
    qn = ''.join(nchar(c) for c in q)
    if len(qn) < 2:
        sys.exit('探す語が短すぎる')
    total = 0
    for d in docs:
        s = raw(d)
        ns, pos = norm_map(s)
        pgs = pages(s) if d in PAGED else []
        k = ns.find(qn)
        while k >= 0:
            total += 1
            a = pos[k]
            b = pos[k + len(qn) - 1] + 1
            pre = s[max(0, a - ctx):a].replace('\n', '⏎')
            mid = s[a:b].replace('\n', '⏎')
            post = s[b:b + ctx].replace('\n', '⏎')
            pg = ('p.%s' % page_of(pgs, a)) if pgs else '頁なし@%d字' % a
            print('[%s %s] …%s【%s】%s…' % (d, pg, pre, mid, post))
            if total >= mx:
                print('（%d 件で止めた＝--max を上げる）' % mx)
                return
            k = ns.find(qn, k + 1)
    print('== 当たり %d 件（%s・「%s」）' % (total, '・'.join(docs), q))


def selftest():
    ok = True
    s = raw('K6')
    n47 = [x for x in pages(s) if x[0] == 47]
    ok &= bool(n47)
    ns, pos = norm_map('가 나\n다')
    ok &= ns == '가나다' and pos == [0, 2, 4]
    import io
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cmd_find('K6', '당장 붕괴위험', 20, 5)
    ok &= '当たり' in buf.getvalue() and 'p.47' in buf.getvalue()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        cmd_find('大96', '아무런보강조치', 20, 5)
    ok &= '当たり 1' in buf.getvalue() or '当たり 2' in buf.getvalue()
    print('selftest', 'OK' if ok else '🔴 NG')
    return 0 if ok else 1


def main():
    a = sys.argv[1:]
    if not a or a[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    if a[0] == '--selftest':
        return selftest()
    ctx = int(a[a.index('--ctx') + 1]) if '--ctx' in a else 120
    mx = int(a[a.index('--max') + 1]) if '--max' in a else 20
    rest = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--ctx', '--max'))]
    if rest[0] == 'page':
        p1 = int(rest[2])
        p2 = int(rest[3]) if len(rest) > 3 else p1
        cmd_page(rest[1], p1, p2)
    elif rest[0] == 'find':
        cmd_find(rest[1], ' '.join(rest[2:]), ctx, mx)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
