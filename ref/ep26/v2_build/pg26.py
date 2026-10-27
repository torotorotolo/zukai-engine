# -*- coding: utf-8 -*-
"""26本目④'：一次資料の文字の層を引く道具（照合の係と G0 が同じ物差しで原文を引く・25本目 pg25.py の考え方を、
v1_build/quotes26.py の資料の表〈英国の報告 S. Doc. 933・MAIB 1992＋OCR・米国の法3本・米国の公聴会 S. Doc. 726〉に替えた）。

  python -P ref/ep26/v2_build/pg26.py page G1 60            # G1 の印刷頁 60 をそのまま出す
  python -P ref/ep26/v2_build/pg26.py page G1 56 58         # 印刷頁 56〜58
  python -P ref/ep26/v2_build/pg26.py page G2 15            # MAIB の印刷頁 15（＝PDF 19）。送り状は「page G2 cover」
  python -P ref/ep26/v2_build/pg26.py page G2 11 --ocr      # MAIB は文字の層に緯度経度・色の語が無い＝OCR の行で読む
  python -P ref/ep26/v2_build/pg26.py page G7 740           # 米国の公聴会（PDF の頁＝台本の出典の欄と同じ）
  python -P ref/ep26/v2_build/pg26.py page G4               # 米国の法（G4〜G6）は全文
  python -P ref/ep26/v2_build/pg26.py find G1 "might have saved many"     # 大文字小文字・記号・改行・行末の分かち書きを無視（頁の境もまたぐ）
  python -P ref/ep26/v2_build/pg26.py find all "no villains" --ctx 400  # 全部の資料（G7 は全1,170頁）
  python -P ref/ep26/v2_build/pg26.py find G7 "New York time" --from 700 --to 760
  python -P ref/ep26/v2_build/pg26.py re G2 "abnormal\\s+refraction"      # 正規表現（空白をつめた原文に・大文字小文字を無視）
  python -P ref/ep26/v2_build/pg26.py docs
  python -P ref/ep26/v2_build/pg26.py --selftest

頁＝**印刷頁**（sources.md §1・台本の出典の欄と同じ。G1＝PDF と同じ・G2＝PDF−4〈送り状＝PDF 3〉・G7＝PDF の頁）。
⚠️ OCR の崩れ（「Tutanic」「itis」「deck ights」「1s」「57° 7」）がある＝見つからないときは綴りを変える・短くする・数字を外す。
⚠️ 「0件」は「この綴りでは出ない」であって「無い」ではない。
⚠️ 名前：git の外の src/names_private.txt の名前は［名前］に伏せて出す。係の記録・リポのファイルに、乗客・会社の人・
カリフォルニアン号の機関部の乗組員の名前を写さない（役職で書く）。
G7 の頁は、初めて引いたときに F:\\jiko_src\\ep26\\ の PDF から取り出して src/sd726_pages/（git の外）に置く（quotes26 と同じ置き場）。
"""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
SRC = r'C:\Users\konar\Desktop\zukai-engine\ref\ep26\src'
G7_PDF = r'F:\jiko_src\ep26\SERIALSET-06167_00_00-002-0726-0000.pdf'
G7_CACHE = os.path.join(SRC, 'sd726_pages')
G7_N = 1170
WHOLE = {'G4': 'txt/stat37_199.txt', 'G5': 'txt/stat37_302.txt', 'G6': 'txt/stat36_629.txt'}
DOCS = {
    'G1': '英国の審問の報告（S. Doc. 933・印刷頁＝PDF）',
    'G2': 'MAIB 1992 再評価（印刷頁＝PDF−4・送り状＝cover＝PDF 3）＋OCR（--ocr）',
    'G4': '米国の法 37 Stat. 199（全文・欄外の注が混ざる）',
    'G5': '米国の法 37 Stat. 302 Radio Act（全文）',
    'G6': '米国の法 36 Stat. 629（全文）',
    'G7': '米国上院の公聴会 S. Doc. 726（PDF の頁・1〜1170）',
}

NAMES = [ln.strip() for ln in open(os.path.join(SRC, 'names_private.txt'), encoding='utf-8')
         if ln.strip() and not ln.startswith('#')]
NAMES.sort(key=len, reverse=True)
NAME_RX = [re.compile(r'\s*'.join(re.escape(c) for c in n if not c.isspace()), re.I) for n in NAMES]


def mask(s):
    for rx in NAME_RX:
        s = rx.sub('［名前］', s)
    return s


def squash(s):
    return re.sub(r'\s+', ' ', (s or '').replace('\u00ad', '')).strip()


def normmap(s):
    """英小文字と数字だけの字（間は空白1つ）と、その字の元の位置。行末の分かち書き（-＋改行）はつなぐ。"""
    out, idx, sp = [], [], True
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == '-' and i + 1 < n and s[i + 1] in '\r\n':
            j = i + 1
            while j < n and s[j] in ' \t\r\n':
                j += 1
            i = j
            continue
        c = c.lower().replace('’', "'")
        if c.isascii() and c.isalnum():
            out.append(c)
            idx.append(i)
            sp = False
        elif not sp:
            out.append(' ')
            idx.append(i)
            sp = True
        i += 1
    return ''.join(out), idx


def norm(s):
    return normmap(s)[0].strip()


def _read(fn):
    return open(fn, encoding='utf-8', errors='replace').read()


def _maib_ocr():
    out, cur, buf = {}, None, []
    fn = os.path.join(SRC, 'maib_ocr.txt')
    for ln in open(fn, encoding='utf-8', errors='replace'):
        m = re.match(r'^## .*p(\d+)\.png', ln)
        if m:
            if cur is not None:
                out[cur - 4] = '\n'.join(buf)
            cur, buf = int(m.group(1)), []
            continue
        buf.append(re.sub(r'^\[[^\]]*\]\s*', '', ln.rstrip('\n')))
    if cur is not None:
        out[cur - 4] = '\n'.join(buf)
    return out


def _g7(pgs):
    out, need = {}, []
    for p in pgs:
        fn = os.path.join(G7_CACHE, 'p%04d.txt' % p)
        if os.path.exists(fn):
            out[p] = _read(fn)
        elif 1 <= p <= G7_N:
            need.append(p)
    if need:
        import fitz
        os.makedirs(G7_CACHE, exist_ok=True)
        doc = fitz.open(G7_PDF)
        for p in need:
            t = doc[p - 1].get_text()
            with open(os.path.join(G7_CACHE, 'p%04d.txt' % p), 'w', encoding='utf-8') as f:
                f.write(t)
            out[p] = t
        doc.close()
    return out


def pages(doc, lo=None, hi=None, ocr=False):
    """{印刷頁: 原文}。"""
    pno = lambda f: int(re.match(r'p(\d+)\.txt$', os.path.basename(f)).group(1))   # noqa: E731  道の「ep26」を拾わない
    if doc == 'G1':
        d = {pno(f): _read(f) for f in glob.glob(os.path.join(SRC, 'sd933_pages', 'p*.txt'))}
    elif doc == 'G2':
        if ocr:
            d = _maib_ocr()
        else:
            d = {pno(f) - 4: _read(f) for f in glob.glob(os.path.join(SRC, 'maib_pages', 'p*.txt'))}
    elif doc in WHOLE:
        d = {0: _read(os.path.join(SRC, WHOLE[doc]))}
    elif doc == 'G7':
        a = lo if lo is not None else 1
        b = hi if hi is not None else G7_N
        return _g7(range(max(1, a), min(G7_N, b) + 1))
    else:
        raise SystemExit(f'資料の記号が無い: {doc}（docs で一覧）')
    if lo is not None:
        d = {k: v for k, v in d.items() if (hi is None and k == lo) or (hi is not None and lo <= k <= hi)}
    return d


def label(doc, k):
    if doc in WHOLE:
        return f'{doc} 全文'
    if doc == 'G2':
        return f'G2 p.{k}（PDF {k + 4}）' if k > 0 else f'G2 {"送り状" if k == -1 else "表紙側"}（PDF {k + 4}）'
    return f'{doc} p.{k}'


def find(doc, q, ctx=250, mx=20, lo=None, hi=None, ocr=False):
    nq = norm(q)
    if len(nq) < 3:
        raise SystemExit('探す字が短すぎる')
    docs = list(DOCS) if doc == 'all' else [doc]
    hits = 0
    for d in docs:
        # G2 は文字の層を先に・当たらなければ OCR（文字の層に緯度経度と色の語が無い）
        variants = [False, True] if (d == 'G2' and not ocr) else [ocr]
        for use_ocr in variants:
            got = 0
            pg = pages(d, lo, hi, use_ocr)
            for k in sorted(pg):
                txt = pg[k]
                joined = txt + '\n⏎頁⏎\n' + pg.get(k + 1, '')[:600]
                ns, idx = normmap(joined)
                start = 0
                while True:
                    j = ns.find(nq, start)
                    if j < 0 or idx[j] >= len(txt):   # 次の頁の頭だけで当たった＝次の頁で拾う
                        break
                    a = idx[j]
                    b = idx[min(j + len(nq) - 1, len(idx) - 1)] + 1
                    hits += 1
                    got += 1
                    tag = '（OCR）' if use_ocr else ''
                    seam = '（頁の境をまたぐ）' if b > len(txt) else ''
                    print(f'■ {label(d, k)}{tag}{seam}')
                    print('  ' + mask(squash(joined[max(0, a - ctx):b + ctx])))
                    if hits >= mx:
                        print(f'…（{mx}件で止めた＝--max で増やす）')
                        return hits
                    start = j + 1
            if got:
                break
    if not hits:
        print('0件（この綴りでは出ない＝無いとは限らない。綴り・短さ・数字の書き方を変えて探す）')
    return hits


def rex(doc, pat, ctx=200, mx=20, lo=None, hi=None, ocr=False):
    rx = re.compile(pat, re.I)
    docs = list(DOCS) if doc == 'all' else [doc]
    hits = 0
    for d in docs:
        pg = pages(d, lo, hi, ocr)
        for k in sorted(pg):
            s = squash(pg[k])
            for m in rx.finditer(s):
                hits += 1
                print(f'■ {label(d, k)}{"（OCR）" if ocr else ""}')
                print('  ' + mask(s[max(0, m.start() - ctx):m.end() + ctx]))
                if hits >= mx:
                    print(f'…（{mx}件で止めた）')
                    return hits
    if not hits:
        print('0件（この綴りでは出ない＝無いとは限らない）')
    return hits


def page(doc, lo, hi, ocr=False):
    pg = pages(doc, lo, hi, ocr)
    if not pg:
        print('その頁は無い')
        return
    for k in sorted(pg):
        print(f'===== {label(doc, k)}{"（OCR）" if ocr else ""} =====')
        print(mask(pg[k]))


def _opt(args, name, cast=int, default=None):
    if name in args:
        i = args.index(name)
        v = cast(args[i + 1])
        del args[i:i + 2]
        return v
    return default


def selftest():
    import io
    import contextlib
    ok = True

    def hit(*a, **k):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            n = find(*a, **k)
        return n, buf.getvalue()

    cases = [
        ('G1', 'might have saved many if not all of the lives', 60, None),
        ('G1', 'She made no attempt', 85, None),
        ('G2', 'there are no villains in this story', 19, None),
        ('G2', 'more likely that she was not seen', 3, None),     # 結論の要約（p.3）
        ('G7', 'New York time', None, (735, 745)),
        ('G4', 'one or the other of whom shall be', 0, None),
    ]
    for d, q, want, rng in cases:
        lo, hi = rng if rng else (None, None)
        n, out = hit(d, q, lo=lo, hi=hi)
        good = n >= 1 and (want is None or f'p.{want}' in out or (want == 0 and '全文' in out))
        print(('✓' if good else '✗'), '陽性', d, q[:40], '→', n, '件')
        ok &= good
    n, _ = hit('G1', 'the Californian could not have saved anyone')
    print(('✓' if n == 0 else '✗'), '陰性 G1 作った句 →', n, '件')
    ok &= n == 0
    if NAMES:
        nm = NAMES[0]
        good = mask('x ' + nm + ' y') == 'x ［名前］ y' and mask('x ' + nm.upper() + ' y') == 'x ［名前］ y'
        print(('✓' if good else '✗'), '名前を伏せる（表の1件目・大文字も）')
        ok &= good
    good = norm('deck-\nlights “Keep out.”') == 'decklights keep out'
    print(('✓' if good else '✗'), '揃え（行末の分かち書き・引用符）')
    ok &= good
    print('selftest', 'OK' if ok else 'NG')
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        return 0
    if args[0] == '--selftest':
        return selftest()
    ocr = '--ocr' in args
    args = [a for a in args if a != '--ocr']
    ctx = _opt(args, '--ctx', int, 250)
    mx = _opt(args, '--max', int, 20)
    lo = _opt(args, '--from', int)
    hi = _opt(args, '--to', int)
    cmd = args[0]
    if cmd == 'docs':
        for k, v in DOCS.items():
            print(k, v)
        return 0
    doc = args[1]
    if cmd == 'page':
        if doc in WHOLE:
            page(doc, None, None)
            return 0
        a = -1 if args[2] == 'cover' else int(args[2])
        b = int(args[3]) if len(args) > 3 else a      # 1頁だけ（G7 で「その頁から最後まで」を出していた＝10-27 に直した）
        page(doc, a, b, ocr)
        return 0
    if cmd == 'find':
        return 0 if find(doc, args[2], ctx, mx, lo, hi, ocr) else 2
    if cmd == 're':
        return 0 if rex(doc, args[2], ctx, mx, lo, hi, ocr) else 2
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
