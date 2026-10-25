# -*- coding: utf-8 -*-
"""25本目 出典の欄の原文の片（バッククォートの中）を、一次資料の文字の層に機械で当てる（④・2026-10-25・24本目の quotes24.py を写し、
日本語の PDF（頁ごとの txt/*.json）・HTML・国会会議録の JSON に替えた）。

  python ref/ep25/v1_build/quotes25.py ref/ep25/daihon_v1.md [--out 結果.tsv]
  python ref/ep25/v1_build/quotes25.py --selftest

なぜ要るか：決め所（★）が0＝tools/check_facts.py の照合が働かない。代わりに §4 の全カットの「出典の欄」のバッククォートを、
書いた資料と頁に当てる（照合の表＝出典の欄そのもの）。

資料（ref/ep25/src/＝git の外）：頁ごとの文字＝txt/<名前>.json（{pdf, printed, raw, norm, …}）。記号は sources.md §1 の表。
出典の欄の書き方＝「R1 p.222（`…`）」＝p の後の数＝**印刷頁**（sources.md と同じ。R1＝PDF−11・S1＝PDF−8・判決＝PDF と同じ）。
範囲「p.219〜221」も可。印刷頁の無い資料（付図・JR西日本の PDF など）は PDF の頁。
HTML の資料（M1・M2・J0・J1・J2 ほか）と国会会議録（Kk）は頁を見ない＝全文に当てる。JR西日本（J0〜J7）は JR西日本の全ファイルの和に当てる。
判定：OK＝書いた頁にある（頁の無い資料は全文にある）／近＝隣の頁／別頁＝同じ資料の別の頁（どこかを出す）／無し／資料なし／短い
揃え：NFKC・空白（改行を含む）を消す・引用符とかぎかっこを消す・中黒と波線とダッシュの揺れを揃える・小文字にそろえる。
「…」で区切った4字以上の片を全部探す。⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属）は人が見る（④'）。
"""
import glob
import html as H
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
SRC = r'C:\Users\konar\Desktop\zukai-engine\ref\ep25\src'
PDFS = {
    'R0': 'RA2007-3-1_cover', 'R1': 'RA07-3-1-1', 'R2': 'RA07-3-1-2', 'R3': 'RA07-3-1-3', 'R4': 'RA07-3-1-4',
    'R5': 'RA07-3-1-5', 'R6': 'RA07-3-1-6', 'R7': 'RA07-3-1-7', 'K05': 'kengi_170906k', 'K07': 'kengi_190628k',
    'P1': 'keika2', 'S1': 'fu04-finalreport', 'S1k': 'fu04-finalreport-annex-2-2', 'T1': 'annual2010-fukuchiyama',
    'I01': 'iken20070201-an01-honbun', 'I06': 'iken20070201-giji01-gaiyou', 'S2': 'hanrei-pdf-86834', 'S3': 'hanrei-pdf-82178',
    'M1q': 'mlit_pubcom5_01', 'F1': 'fdma_post364', 'F2': 'fdma_170523_1', 'C1': 'bousai_fukuchiyama_07',
    'HY1': 'hyogo_kensho_000007823', 'HY2': 'hyogo_kensho_gaiyou_000007665',
}
HTMLS = {
    'M1': ['gov/mlit_kisha_080324_.html'], 'M1p': ['gov/mlit_pubcomk5_.html'], 'M2': ['gov/mlit_fukuchiyama_index.html'],
    'M3': ['gov/mlit_hakusho_h18_H1012210.html'], 'M4': ['gov/cao_koutu_h29_h1b2s2_1.html'],
    'C2': ['gov/bousai_hakusho_h17_hm120503.htm'], 'C3': ['gov/bousai_hakusho_h18_hm01020503.htm'],
}
JRW_HTML = ['jrw/' + x for x in ('action.html', 'fukuchiyama_top.html', 'inorinomori.html', 'outline.html', 'plan_improvement.html',
                                  'report_railroad.html', 'safety_top.html', 'support_01.html', 'support_02.html')]
JRW_TXT = ['j_inorinomori', 'keikaku_00', 'shourainiwataru', 'support_houkoku', 'report_railroad_houkoku_01', 'report_railroad_houkoku_02']
CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／\s*[^／]*／(.*)$')
TOK = re.compile(r'(?<![A-Za-z0-9])(?P<doc>S1k|K0[57]|HY[12]|M1[pq]|M[1-4]|J[0-7]|Kk|R[0-7]|P1|S[1-3]|T1|I0[16]|F[12]|C[1-3])'
                 r'(?![0-9A-Za-z])'
                 r'|(?P<pg>p\.?\s*(?P<p1>\d+)(?:\s*[〜～~-]\s*(?P<p2>\d+))?)'
                 r'|`(?P<q>[^`]+)`')


def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'[‘’“”\'"`´「」『』]', '', s)
    s = re.sub(r'[·・ㆍ･]', '·', s)
    s = re.sub(r'[～∼〜~]', '~', s)
    s = re.sub(r'[‐‑‒–—―−－ｰ]', '-', s)
    return s.lower()


def pieces(q):
    return [p for p in re.split(r'…|\.\.\.', norm(q)) if len(p) >= 4]


def html_text(rel):
    b = open(os.path.join(SRC, rel), 'rb').read()
    for enc in ('utf-8', 'cp932', 'euc-jp'):
        try:
            t = b.decode(enc)
            break
        except Exception:
            continue
    else:
        t = b.decode('utf-8', 'replace')
    t = re.sub(r'(?is)<(script|style).*?</\1>', '', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return norm(H.unescape(t))


# 印刷頁の推定（printed）が当てにならない資料＝PDF の頁で書く（消防庁 F1・F2 は printed＝PDF−4 の推定値が負になる）
PDF_PAGED = {'fdma_post364', 'fdma_170523_1'}


def txt_pages(name):
    out = {}
    for d in json.load(open(os.path.join(SRC, 'txt', name + '.json'), encoding='utf-8')):
        pg = d['printed'] if d.get('printed') is not None and name not in PDF_PAGED else d['pdf']
        out[int(pg)] = norm(d.get('raw') or d.get('norm') or '')
    return out


def load(doc):
    if doc == 'Kk':
        texts = []
        for fn in glob.glob(os.path.join(SRC, 'kokkai', 'kokkai_*.json')):
            d = json.load(open(fn, encoding='utf-8'))
            recs = d if isinstance(d, list) else d.get('speechRecord', [])
            texts += [r.get('speech', '') for r in recs if isinstance(r, dict)]
        return {0: norm('\n'.join(texts))}
    if doc.startswith('J'):
        texts = [html_text(r) for r in JRW_HTML if os.path.exists(os.path.join(SRC, r))]
        for nm in JRW_TXT:
            texts += list(txt_pages(nm).values())
        return {0: ''.join(texts)}
    if doc in HTMLS:
        return {0: ''.join(html_text(r) for r in HTMLS[doc])}
    return txt_pages(PDFS[doc])


_CACHE = {}


def pages_of(doc):
    if doc not in _CACHE:
        _CACHE[doc] = load(doc)
    return _CACHE[doc]


def judge(doc, pgs, q):
    if doc not in PDFS and doc not in HTMLS and doc != 'Kk' and not doc.startswith('J'):
        return '資料なし', ''
    pages = pages_of(doc)
    ps = pieces(q)
    if not ps:
        return '短い', ''
    worst, where = 'OK', []
    order = ['OK', '近', '別頁', '無し']
    whole = list(pages.keys()) == [0]
    for p in ps:
        if whole:
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
    ok = norm('「回復運転のため 意識的に」') == '回復運転のため意識的に'
    ok &= norm('平成15年10月~平成17年5月') == norm('平成15年10月～平成17年5月')
    ok &= pieces('回復運転のため意識的に…低いものと考えられる') == ['回復運転のため意識的に', '低いものと考えられる']
    toks = [(m.group('doc'), m.group('p1'), m.group('p2')) for m in TOK.finditer('R1 p.222（`a`）・S1 p.13〜14・Kk・S1k p.5・HY1 p.3')
            if m.group('doc') or m.group('pg')]
    ok &= toks == [('R1', None, None), (None, '222', None), ('S1', None, None), (None, '13', '14'), ('Kk', None, None),
                   ('S1k', None, None), (None, '5', None), ('HY1', None, None), (None, '3', None)]
    # 本物の資料で陽性対照（sources.md §2・§5 で照合ずみの句）・別の頁・陰性対照・国会・JR西日本
    ok &= judge('R1', [222], '回復運転のため意識的に')[0] == 'OK'
    ok &= judge('R1', [221], '回復運転のため意識的に')[0] in ('近', 'OK')
    ok &= judge('R1', [100], '回復運転のため意識的に')[0] == '別頁'
    ok &= judge('R1', [222], '遅れを取り戻そうとわざと速度を出した')[0] == '無し'
    ok &= judge('R1', [138], 'P信号速照機能を使用')[0] == 'OK'
    ok &= judge('S1', [14], '後出しじゃんけん')[0] == 'OK'
    ok &= judge('S2', [5], '認識できたとは認められない')[0] == 'OK'
    ok &= judge('Kk', [], 'いずれも無罪')[0] == 'OK'
    ok &= judge('J1', [], '106名のお客様')[0] == 'OK'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    op = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], op) else 0)
