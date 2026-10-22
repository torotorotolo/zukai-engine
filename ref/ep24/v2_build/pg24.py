# -*- coding: utf-8 -*-
"""24本目④'：一次資料の文字の層を引く道具（照合の係と G0 が同じ物差しで原文を引く・23本目 pg23.py の考え方を英語の PDF と国会会議録に替えた）。

  python ref/ep24/v2_build/pg24.py page S1 21            # S1 の PDF頁 21 をそのまま出す（印刷頁も添える）
  python ref/ep24/v2_build/pg24.py page S1 63 65         # PDF頁 63〜65
  python ref/ep24/v2_build/pg24.py find S1 "might well have caused"      # 空白・行末のハイフン・大文字小文字を無視して探す（頁の境もまたぐ）
  python ref/ep24/v2_build/pg24.py find all "Ignalina" --ctx 300 --max 30
  python ref/ep24/v2_build/pg24.py re S2 "violat\\w+ of (the )?rules"     # 正規表現（文字の層の字そのまま・大文字小文字は無視）
  python ref/ep24/v2_build/pg24.py find K1 "五月三日に至り"              # 国会会議録（発言ごと＝日付・会議・役職・URL を添える）
  python ref/ep24/v2_build/pg24.py --selftest

資料（ref/ep24/src/＝git の外・読むだけ。頁＝「PDF頁／印刷頁」＝sources.md と同じ）：
  S1＝INSAG-7（1992・付属書I＝ソ連の規制側の委員会 1991・付属書II＝ソ連専門家作業部会）印刷＝PDF−10
  S2＝GC(SPL.I)/3＝INSAG-1 の本文（1986・OCR）印刷＝頁頭の「- N -」（途中でずれが変わる）
  S3＝ソ連の報告 Part I（1986年8月・IAEA 専門家会議向け）印刷＝PDF−4
  L1＝チェルノブイリ・フォーラム 2006 印刷＝PDF＋2（⚠️ probe/grep24.py の OFF −2 は誤り）／L2＝UNSCEAR 2000 Annex J 印刷＝PDF＋448／
  L3＝UNSCEAR 2008 Annex D 印刷＝PDF＋40／L4＝UNSCEAR 白書 2018（甲状腺）／L5＝UNSCEAR 1988 本文／L6＝1988 Annex D／L7＝1988 Annex G／
  L8＝IARC 2006／L10＝INES の手引き 2008／K1＝国会会議録（1986-04-26〜1987-05-31 の発言の JSON）
  ⚠️ L9（WHO 2005 の頁）・WEB（事業者・EBRD・内閣府・WNN）は文字の層が手元に無い＝係は開けない（親へ）
⚠️ 「0件」は「この綴りでは出ない」であって「無い」ではない（OCR の崩れ・別の言い回し）。言い換えでも探す・頁の境で文が割れる（前の頁の終わりも読む）。
⚠️ 国会会議録・付属書の出力には人の名前が出てくる＝リポのファイル・係の記録には、記録にある5人（レガソフ・ジャトロフ・ヴォルコフ・ブリクス・ルイシコフ）のほかの名前を写さない（役職で書く）。
"""
import glob
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
SRC = r'C:\Users\konar\Desktop\zukai-engine\ref\ep24\src'
FILES = {
    'S1': 'insag7_pub913e', 'S2': 'gc_spl1_3_insag1text', 'S3': 'ussr_report_part1',
    'L1': 'forum_legacy_2006', 'L2': 'unscear2000_annexJ', 'L3': 'unscear2008_annexD_corr',
    'L4': 'unscear_wp2018_thyroid', 'L5': 'unscear1988_report', 'L6': 'unscear1988_annexD', 'L7': 'unscear1988_annexG',
    'L8': 'iarc2006_briefing', 'L10': 'ines_manual2008',
}
OFF = {'S1': -10, 'S3': -4, 'L1': 2, 'L2': 448, 'L3': 40}
S2_HEAD = re.compile(r'^\s*-\s*(\d{1,3})\s*-')


def nf(s):
    return unicodedata.normalize('NFKC', s or '')


def load(doc):
    """[(頁の札, 文字)]。S・L＝PDF頁ごと。K1＝発言ごと。"""
    if doc == 'K1':
        seen, out = set(), []
        for fn in sorted(glob.glob(os.path.join(SRC, 'kokkai_*.json'))):
            d = json.load(open(fn, encoding='utf-8'))
            recs = d if isinstance(d, list) else d.get('speechRecord', [])
            if isinstance(d, dict) and 'meetingRecord' in d:
                for m in d['meetingRecord']:
                    for sp in m.get('speechRecord', []):
                        sp = dict(sp, nameOfMeeting=m.get('nameOfMeeting'), date=m.get('date'), nameOfHouse=m.get('nameOfHouse'))
                        recs.append(sp)
            for r in recs:
                if not isinstance(r, dict) or r.get('speechID') in seen:
                    continue
                seen.add(r.get('speechID'))
                lab = '%s %s %s 発言%s（%s）%s' % (r.get('date'), r.get('nameOfHouse', ''), r.get('nameOfMeeting', ''),
                                              r.get('speechOrder'), r.get('speakerPosition') or r.get('speakerRole') or '',
                                              r.get('speechURL', ''))
                out.append((lab, nf(r.get('speech', ''))))
        return out
    out = []
    for ln in open(os.path.join(SRC, FILES[doc] + '.pages.tsv'), encoding='utf-8'):
        pdf, _n, text = ln.rstrip('\n').split('\t', 2)
        out.append((int(pdf), nf(text)))
    return out


def label(doc, pdf, text):
    if doc == 'K1':
        return pdf
    if doc in OFF:
        return 'p.%d／%d' % (pdf, pdf + OFF[doc])
    if doc == 'S2':
        m = S2_HEAD.match(text)
        return 'p.%d／~%s' % (pdf, m.group(1) if m else '?')
    return 'p.%d／?' % pdf


def loose(q):
    """探す句 → 空白・改行・行末のハイフン・引用符の揺れを許す正規表現。"""
    q = nf(q)
    q = re.sub(r'\s+', '', q)
    parts = []
    for c in q:
        if c in '‘’“”\'"`´':
            parts.append(r'[‘’“”\'"`´]?')
            continue
        if c in '-‐‑‒–—―−－':
            parts.append(r'[-‐‑‒–—―−－]?')
            continue
        parts.append(re.escape(c))
    return re.compile(r'(?:[\s\-‐]*)'.join(parts), re.I)


def show_hits(doc, rx, ctx, mx):
    pages = load(doc)
    # 頁の境をまたいで当たるように、全体をつないで探す（頁の頭の位置を覚える）
    starts, buf, pos = [], [], 0
    for pdf, text in pages:
        starts.append((pos, pdf, text))
        buf.append(text)
        pos += len(text) + 1
    whole = '\n'.join(buf)
    n = 0
    for m in rx.finditer(whole):
        n += 1
        if n > mx:
            continue
        i = max(k for k, (p, _, _) in enumerate(starts) if p <= m.start())
        p0, pdf, text = starts[i]
        cross = '（頁の境をまたぐ）' if '\n' in m.group(0) else ''
        a, b = max(0, m.start() - ctx), min(len(whole), m.end() + ctx)
        snippet = whole[a:b].replace('\n', ' ⏎頁⏎ ')
        print('- %s %s%s: …%s…' % (doc, label(doc, pdf, text), cross, snippet))
    if n > mx:
        print('  （%s: %d件中 %d件だけ表示）' % (doc, n, mx))
    return n


def main(a):
    if not a or a[0] == '--selftest':
        return selftest()
    cmd = a[0]
    ctx = int(a[a.index('--ctx') + 1]) if '--ctx' in a else 160
    mx = int(a[a.index('--max') + 1]) if '--max' in a else 12
    pos = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--ctx', '--max'))]
    doc = pos[1]
    if cmd == 'page':
        p1 = int(pos[2])
        p2 = int(pos[3]) if len(pos) > 3 else p1
        for pdf, text in load(doc):
            if p1 <= pdf <= p2:
                print('=== %s %s ===' % (doc, label(doc, pdf, text)))
                print(text)
        return 0
    docs = (list(FILES) + ['K1']) if doc == 'all' else [doc]
    q = pos[2]
    rx = loose(q) if cmd == 'find' else re.compile(nf(q), re.I)
    print('### %s %s「%s」' % (cmd, doc, q))
    tot = 0
    for d in docs:
        tot += show_hits(d, rx, ctx, mx)
    if not tot:
        print('  0件（⚠️ この綴りでは出ない＝無いとは限らない。言い換え・OCR の崩れでも探す）')
    return 0


def selftest():
    import io
    import contextlib
    ok = True
    cases = [('S1', 'might well have caused the destruction', True),    # 5.2.1（PDF 28）
             ('S1', 'were in fact not violations', True),
             ('S2', 'compounded and amplified', True),
             ('S1', 'the operators were completely innocent', False),  # 作った句＝無し
             ('K1', '五月三日に至り', True)]
    for d, q, want in cases:
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            n = show_hits(d, loose(q), 40, 3)
        got = n > 0
        print('%s %s「%s」→ %d件 %s' % ('OK' if got == want else '✗', d, q, n, '' if got == want else '（期待と違う）'))
        ok &= got == want
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        show_hits('S1', loose('might well have caused'), 10, 3)
    ok &= 'p.28／18' in f.getvalue()
    print('頁の札 S1 might well →', 'p.28／18' if 'p.28／18' in f.getvalue() else '✗ ' + f.getvalue()[:120])
    print('selftest', 'OK' if ok else '✗')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
