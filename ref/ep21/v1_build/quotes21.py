# -*- coding: utf-8 -*-
"""21本目 出典の欄の引用（バッククォートの中）を、資料の字に機械で当てる（④・2026-10-11・20本目の quotes20.py の考え方を写した）。

  python ref/ep21/v1_build/quotes21.py ref/ep21/daihon_v1.md [--out 結果.tsv]
  python ref/ep21/v1_build/quotes21.py --selftest

なぜ要るか：21本目も決め所（★）が0＝tools/check_facts.py の照合（★の表）が働かない。
代わりに §4 の全カットの「出典の欄」のバッククォートを、書いた資料と頁に当てる（照合の表＝出典の欄そのもの）。

資料（どれも ref/ep21/ の下。src/ は git の外）：
  委員会報告 ＝ src/core_raw/GPO-911REPORT.pages.jsonl（文字の層・生まれつき）。「p21」は印字の頁＝PDF＝印字＋18。前付けは p.xv（PDF＝ローマ数字の値）
  図表（委員会報告 p32〜33）＝ sources.md §11-1 #9（②で原寸で見た字の写し）
  スタッフ声明 ＝ src/core_raw/staff17.pages.jsonl（PDF の頁）
  NTSB 11便／175便／77便／93便 ＝ sources.md §11-1 #1〜#5（②で原寸）と analytics/materials/ep7/s2/ocr/*.ocr.txt（OCR）
  CVR（93便の逐語 P200056T）＝ sources.md §11-1 #11（②で原寸）と src/core_raw/P200056T.ocr.txt（OCR）
  国立公園局・AP・法律（Public Law 107-71）・検視局・記念館・監察総監（Air Force Magazine の報道）＝ src/new/web4/*.txt（④で開いた写し）
  NIST ＝ sources.md §11-1（②で原寸）と src/core_raw/ncstar1.pages.jsonl（NCSTAR 1 の文字の層＝OCR 並み＝全頁から探す）
  運輸長官の証言（2003-05-23）＝ src/new/hearing2/transcript_0523.txt
判定：OK＝書いた頁にある／近＝隣の頁／別頁＝同じ資料の別の頁（頁を出す）／原寸＝OCR の資料で、②が原寸で見た写しにある／OCR＝OCR の字にだけある／無し
揃え：NFKC・小文字・空白を消す・ダッシュと引用符の揺れを揃える（行末ハイフンは「消した版」でも探す）。「…」「...」で区切って4字以上の片を全部探す。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ）は人が見る（④'）。
"""
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\konar\Desktop\zukai-engine'
EP = os.path.join(ROOT, 'ref', 'ep21')
CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／(.*)$')
TOK = re.compile(r'(?P<doc>委員会報告|図表|スタッフ声明|NTSB\s*(?:11|175|77|93)便|CVR|国立公園局|AP|法律|検視局|記念館'
                 r'|監察総監|運輸長官の証言|NIST)'
                 r'|(?P<pg>p\.?\s*(?P<p1>[ivx]+|\d+)(?:\s*〜\s*p?\.?\s*(?P<p2>\d+))?)'
                 r'|`(?P<q>[^`]+)`')
FLAT = {'国立公園局': 'nps', 'AP': 'ap_seattletimes', '法律': 'pl107_71', '検視局': 'ocme',
        '記念館': 'memorial_faq', '監察総監': 'afmag_dot'}
NTSB = {'11': 'AA11', '175': 'UA175', '77': 'AA77', '93': 'UA93'}
ROMAN = {'i': 1, 'v': 5, 'x': 10}


def roman(s):
    v, prev = 0, 0
    for ch in reversed(s):
        n = ROMAN[ch]
        v = v - n if n < prev else v + n
        prev = max(prev, n)
    return v


def norm(s):
    s = unicodedata.normalize('NFKC', s or '').lower()
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'[‐‑‒–—―−－ｰ]', '-', s)
    s = s.replace('’', "'").replace('‘', "'").replace('”', '"').replace('“', '"').replace('\u00ad', '')
    return s


def nohy(s):
    return s.replace('-', '')


def pieces(q):
    return [p for p in re.split(r'…|\.\.\.|・・・', norm(q)) if len(p) >= 4]


def _jsonl(path):
    out = {}
    for line in open(path, encoding='utf-8'):
        d = json.loads(line)
        out[d['pdf_page']] = norm(d.get('raw') or '')
    return out


def _txt(path):
    return norm(open(path, encoding='utf-8', errors='replace').read()) if os.path.exists(path) else ''


def load():
    src = open(os.path.join(EP, 'sources.md'), encoding='utf-8').read()
    m = re.search(r'### 11-1\..*?(?=\n### 11-2|\Z)', src, re.S)
    human = norm(m.group(0) if m else '')
    D = {'cr': _jsonl(os.path.join(EP, 'src', 'core_raw', 'GPO-911REPORT.pages.jsonl')),
         'staff': _jsonl(os.path.join(EP, 'src', 'core_raw', 'staff17.pages.jsonl')),
         'human': human,
         'cvr': _txt(os.path.join(EP, 'src', 'core_raw', 'P200056T.ocr.txt')),
         'nist': ''.join(_jsonl(os.path.join(EP, 'src', 'core_raw', 'ncstar1.pages.jsonl')).values()),
         'hearing': _txt(os.path.join(EP, 'src', 'new', 'hearing2', 'transcript_0523.txt'))}
    for k, f in NTSB.items():
        D['ntsb' + k] = _txt(os.path.join(ROOT, 'analytics', 'materials', 'ep7', 's2', 'ocr', f + '.ocr.txt'))
    for k, f in FLAT.items():
        D[k] = _txt(os.path.join(EP, 'src', 'new', 'web4', f + '.txt'))
    return D


def _in(piece, text):
    return piece in text or nohy(piece) in nohy(text)


def find(D, doc, p1, p2, piece):
    """戻り値＝(判定, 見つかった所)"""
    if doc in ('委員会報告', '図表'):
        pages = D['cr']
        if doc == '図表' and _in(piece, D['human']):
            return '原寸', 'sources §11-1'
        if p1 is not None:
            want = list(range(p1, (p2 or p1) + 1))
            for p in want:
                if _in(piece, pages.get(p + 18, '')):
                    return 'OK', 'p%d' % p
            for p in (want[0] - 1, want[-1] + 1):
                if _in(piece, pages.get(p + 18, '')):
                    return '近', 'p%d' % p
        hit = [pp - 18 for pp, t in sorted(pages.items()) if _in(piece, t)]
        if hit:
            return '別頁', ','.join('p%d' % h for h in hit[:6])
        return '無し', '-'
    if doc == 'スタッフ声明':
        hit = [pp for pp, t in sorted(D['staff'].items()) if _in(piece, t)]
        if hit and p1 in hit:
            return 'OK', 'p%d' % p1
        return ('別頁', ','.join('p%d' % h for h in hit[:6])) if hit else ('無し', '-')
    if doc.startswith('NTSB'):
        k = re.sub(r'\D', '', doc)
        if _in(piece, D['human']):
            return '原寸', 'sources §11-1'
        return ('OCR', 'NTSB %s OCR' % NTSB[k]) if _in(piece, D['ntsb' + k]) else ('無し', '-')
    if doc == 'CVR':
        if _in(piece, D['human']):
            return '原寸', 'sources §11-1'
        return ('OCR', 'P200056T OCR') if _in(piece, D['cvr']) else ('無し', '-')
    if doc == 'NIST':
        if _in(piece, D['human']):
            return '原寸', 'sources §11-1'
        return ('OCR', 'NCSTAR 1 の文字の層') if _in(piece, D['nist']) else ('無し', '-')
    if doc == '運輸長官の証言':
        return ('OK', 'transcript_0523') if _in(piece, D['hearing']) else ('無し', '-')
    if doc in FLAT:
        return ('OK', FLAT[doc]) if _in(piece, D[doc]) else ('無し', '-')
    return '資料なし', '-'


def scan(text, D):
    rows = []
    on = False
    for line in text.splitlines():
        if line.startswith('## 4.'):
            on = True
            continue
        if on and re.match(r'^## \d', line):
            break
        m = CUT_RE.match(line) if on else None
        if not m:
            continue
        cid, rest = m.group(1), m.group(2)
        cols = rest.split('／')
        srccol = '／'.join(cols[1:]) if len(cols) > 1 else ''
        doc, p1, p2 = None, None, None
        for t in TOK.finditer(srccol):
            if t.group('doc'):
                doc, p1, p2 = t.group('doc'), None, None
            elif t.group('pg'):
                a = t.group('p1')
                p1 = roman(a) - 18 if a.isalpha() else int(a)
                p2 = int(t.group('p2')) if t.group('p2') else None
            elif t.group('q'):
                for pc in pieces(t.group('q')):
                    v, where = find(D, doc, p1, p2, pc) if doc else ('資料なし', '-')
                    rows.append((cid, doc or '-', ('p%d' % p1) if p1 is not None else '-', v, where, pc))
    return rows


def main(path, out=None):
    D = load()
    rows = scan(open(path, encoding='utf-8').read(), D)
    out = out or os.path.join(EP, 'v1_build', 'quotes21_result.tsv')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('cid\t資料\t頁\t判定\t見つかった所\t引用の片\n')
        for r in rows:
            f.write('\t'.join(r) + '\n')
    cnt = {}
    for r in rows:
        cnt[r[3]] = cnt.get(r[3], 0) + 1
    print('片 %d → %s  %s' % (len(rows), out, cnt))
    for r in rows:
        if r[3] not in ('OK', '原寸'):
            print('  %s %s %s %s %s  %s' % r)
    return sum(1 for r in rows if r[3] in ('無し', '資料なし'))


def selftest():
    D = {'cr': {39: norm('In summary, NEADS received notice of the hijacking nine minutes before it struck the North Tower.'),
                40: norm('han- dled it')},
         'staff': {}, 'human': norm('10:00:42 Roll it.'), 'cvr': '', 'hearing': '', 'nist': ''}
    for k in NTSB:
        D['ntsb' + k] = ''
    for k in FLAT:
        D[k] = ''
    md = ('## 4. 台本\n**c101** ／ 実写 x ／ 委員会報告 p21（`nine minutes before it struck`）・p22（`handled it`）'
          '・CVR p7（`Roll it.`）・p21（`no such words`）\n## 5. x\n')
    got = [(r[0], r[3]) for r in scan(md, D)]
    ok = got == [('c101', 'OK'), ('c101', 'OK'), ('c101', '原寸'), ('c101', '無し')]
    ok &= roman('xv') == 15
    print('selftest', 'ok' if ok else 'NG', got)
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    o = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], o) else 0)
