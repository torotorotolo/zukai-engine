# -*- coding: utf-8 -*-
"""23本目 出典の欄の原文の片（バッククォートの中）を、韓国語の一次資料の文字の層に機械で当てる（④・2026-10-18・22本目の quotes22.py の考え方を写した）。

  python ref/ep23/v1_build/quotes23.py ref/ep23/daihon_v1.md [--out 結果.tsv]
  python ref/ep23/v1_build/quotes23.py --selftest

なぜ要るか：決め所（★）が0＝tools/check_facts.py の照合が働かない。代わりに §4 の全カットの「出典の欄」のバッククォートを、
書いた資料と頁に当てる（照合の表＝出典の欄そのもの）。

資料（どれも ref/ep10/src/ の下＝git の外）：
  K6-R／K6-市／K6-区／K6-検／K6-市b／K6-区b ＝ assembly_sampoong_tokui_no6_19950912_id19114.txt（頁の印「=== [PDF p.N] ===」＝印刷の頁）
  国監内 ＝ assembly_audit1995_naemu_seoul_19951010_id19476.txt／国監建 ＝ assembly_audit1995_geonseol_seoul_19951011_id19502.txt（同じ頁の印）
  大96 ＝ lawgokr_prec114109_96do1231.txt／大99 ＝ lawgokr_prec79152_98da29797.txt／高96 ＝ casenote_seoulhigh_96no118_visible.txt（頁なし＝全文に当てる）
  白書（頁の画像だけ）・法・記主・記テ・報道は文字の層が手元に無い＝当てない（「」の要約は人が見る）
判定：OK＝書いた頁にある（頁の無い資料は全文にある）／近＝隣の頁／別頁＝同じ資料の別の頁（どこかを出す）／無し／資料なし
揃え：NFKC・空白（改行を含む）を消す・引用符を消す・中黒（· ・ ㆍ）と波線（～ ∼ 〜 ~）とダッシュの揺れを揃える。「…」で区切って4字以上の片を全部探す。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属）は人が見る（④'）。
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
CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／\s*[^／]*／(.*)$')
TOK = re.compile(r'(?P<doc>K6-(?:R|市b|区b|市|区|検)|国監内|国監建|大96|大99|高96|白書|記主|記テ|大統記|KOGL|歴史編纂院|報道|法)'
                 r'|(?P<pg>p\.?\s*(?P<p1>\d+)(?:\s*〜\s*p?\.?\s*(?P<p2>\d+))?)'
                 r'|`(?P<q>[^`]+)`')
PAGE = re.compile(r'^=== \[PDF p\.(\d+)\] ===\s*$', re.M)


def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'[‘’“”\'"`]', '', s)
    s = re.sub(r'[·・ㆍ･]', '·', s)
    s = re.sub(r'[～∼〜~]', '~', s)
    s = re.sub(r'[‐‑‒–—―−－ｰ]', '-', s)
    return s


def pieces(q):
    return [p for p in re.split(r'…|\.\.\.', norm(q)) if len(p) >= 4]


def load(doc):
    raw = open(os.path.join(SRC, FILES[doc]), encoding='utf-8', errors='replace').read()
    if doc not in PAGED:
        return {0: norm(raw)}
    out = {}
    ms = list(PAGE.finditer(raw))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(raw)
        out[int(m.group(1))] = norm(raw[m.end():end])
    return out


_CACHE = {}


def pages_of(doc):
    if doc not in _CACHE:
        _CACHE[doc] = load(doc)
    return _CACHE[doc]


def judge(doc, pgs, q):
    key = 'K6' if doc.startswith('K6') else doc
    if key not in FILES:
        return '資料なし', ''
    pages = pages_of(key)
    ps = pieces(q)
    if not ps:
        return '短い', ''
    worst, where = 'OK', []
    for p in ps:
        if key not in PAGED:
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
        order = ['OK', '近', '別頁', '無し']
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
    ok = norm('5층 식당가  북동쪽부터\n붕괴') == '5층식당가북동쪽부터붕괴'
    ok &= norm('17:52∼17:57') == norm('17:52～17:57') == '17:52~17:57'
    ok &= norm('15㎝') == '15cm'
    ok &= pieces('무량판공법…으로 계산 설계한') == ['무량판공법', '으로계산설계한']
    ok &= [m.group('doc') for m in TOK.finditer('K6-市b p.53（`1,566`）・K6-検 p.47') if m.group('doc')] == ['K6-市b', 'K6-検']
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    op = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], op) else 0)
