# -*- coding: utf-8 -*-
"""24本目 出典の欄の原文の片（バッククォートの中）を、一次資料の文字の層に機械で当てる（④・2026-10-22・23本目の quotes23.py を写し、英語の PDF と国会会議録に替えた）。

  python ref/ep24/v1_build/quotes24.py ref/ep24/daihon_v1.md [--out 結果.tsv]
  python ref/ep24/v1_build/quotes24.py --selftest

なぜ要るか：決め所（★）が0＝tools/check_facts.py の照合が働かない。代わりに §4 の全カットの「出典の欄」のバッククォートを、
書いた資料と頁に当てる（照合の表＝出典の欄そのもの）。

資料（ref/ep24/src/＝git の外・頁ごとの文字＝*.pages.tsv の1列目＝PDF頁）：
  S1＝insag7_pub913e（INSAG-7・付属書I・II）／S2＝gc_spl1_3_insag1text（INSAG-1 の本文＝OCR）／S3＝ussr_report_part1／
  L1＝forum_legacy_2006／L2＝unscear2000_annexJ／L3＝unscear2008_annexD_corr／L4＝unscear_wp2018_thyroid／L7＝unscear1988_annexG／
  L8＝iarc2006_briefing／L10＝ines_manual2008／K1＝国会会議録の JSON（発言の全文に当てる＝頁なし）
出典の欄の書き方＝「S1 p.21／11（`…`）」＝p の後の最初の数＝PDF頁（sources.md と同じ「PDF頁／印刷頁」）。範囲「p.26〜27／22〜23」も可。
L9（WHO の頁）・U（USGS）・R（権利の頁）・WEB・報道は文字の層が手元に無い＝当てない（「」の要約は人が見る）
判定：OK＝書いた PDF頁にある（K1 は発言の全文にある）／近＝隣の頁／別頁＝同じ資料の別の頁（どこかを出す）／無し／資料なし／短い
揃え：NFKC・行末のハイフン（「experi- mentally」）をつなぐ・空白（改行を含む）を消す・引用符を消す・小文字にそろえる・中黒と波線とダッシュの揺れを揃える。
「…」で区切った4字以上の片を全部探す。⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属）は人が見る（④'）。
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
    'L4': 'unscear_wp2018_thyroid', 'L7': 'unscear1988_annexG', 'L8': 'iarc2006_briefing', 'L10': 'ines_manual2008',
}
KOKKAI = 'K1'
CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／\s*[^／]*／(.*)$')
TOK = re.compile(r'(?<![A-Za-z0-9])(?P<doc>L10|L[1-9]|S[1-3]|K1|U[1-4]|R[1-4]|N[12])(?![0-9])'
                 r'|(?P<pg>p\.?\s*(?P<p1>\d+)(?:\s*〜\s*(?P<p2>\d+))?(?:／~?\d+(?:\s*〜\s*~?\d+)?)?)'
                 r'|`(?P<q>[^`]+)`')


def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    s = re.sub(r'(\w)-\s+(\w)', r'\1\2', s)          # 行末のハイフンでの切れ目をつなぐ
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'[‘’“”\'"`´]', '', s)
    s = re.sub(r'[·・ㆍ･]', '·', s)
    s = re.sub(r'[～∼〜~]', '~', s)
    s = re.sub(r'[‐‑‒–—―−－ｰ]', '-', s)
    return s.lower()


def pieces(q):
    return [p for p in re.split(r'…|\.\.\.', norm(q)) if len(p) >= 4]


def load(doc):
    if doc == KOKKAI:
        texts = []
        for fn in glob.glob(os.path.join(SRC, 'kokkai_*.json')):
            d = json.load(open(fn, encoding='utf-8'))
            recs = d if isinstance(d, list) else d.get('speechRecord', [])
            texts += [r.get('speech', '') for r in recs if isinstance(r, dict)]
        return {0: norm('\n'.join(texts))}
    out = {}
    for ln in open(os.path.join(SRC, FILES[doc] + '.pages.tsv'), encoding='utf-8'):
        pdf, _n, text = ln.rstrip('\n').split('\t', 2)
        out[int(pdf)] = norm(text)
    return out


_CACHE = {}


def pages_of(doc):
    if doc not in _CACHE:
        _CACHE[doc] = load(doc)
    return _CACHE[doc]


def judge(doc, pgs, q):
    if doc not in FILES and doc != KOKKAI:
        return '資料なし', ''
    pages = pages_of(doc)
    ps = pieces(q)
    if not ps:
        return '短い', ''
    worst, where = 'OK', []
    order = ['OK', '近', '別頁', '無し']
    for p in ps:
        if doc == KOKKAI:
            v = 'OK' if p in pages[0] else '無し'
        else:
            hit = [k for k, txt in pages.items() if p in txt]
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
        if r[3] != 'OK':
            print('  %s %s p.%s → %s %s ｜ %s' % r)
    if out_path:
        with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('cut\tdoc\tpages\tverdict\twhere\tquote\n')
            for r in rows:
                f.write('\t'.join(r) + '\n')
    return sum(1 for r in rows if r[3] not in ('OK',))


def selftest():
    ok = norm('was discovered experi- mentally in  November') == 'wasdiscoveredexperimentallyinnovember'
    ok &= norm('“entirely plausible”') == 'entirelyplausible'
    ok &= norm('五月三日に至り、東京都') == '五月三日に至り、東京都'
    ok &= pieces('not proscribed…in operating instructions') == ['notproscribed', 'inoperatinginstructions']
    toks = [(m.group('doc'), m.group('p1'), m.group('p2')) for m in TOK.finditer('S1 p.21／11（`a`）・L10 p.13／2・S3 p.26〜27／22〜23')
            if m.group('doc') or m.group('pg')]
    ok &= toks == [('S1', None, None), (None, '21', None), ('L10', None, None), (None, '13', None),
                   ('S3', None, None), (None, '26', '27')]
    # 本物の資料で陽性対照（sources.md §2 で照合ずみの句）と陰性対照
    ok &= judge('S1', [21], 'no operator error as such')[0] == 'OK'
    ok &= judge('S1', [33], 'no operator error as such')[0] == '別頁'
    ok &= judge('S1', [21], 'the operators were entirely innocent of')[0] == '無し'
    ok &= judge('K1', [], '五月三日に至り')[0] == 'OK'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    op = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], op) else 0)
