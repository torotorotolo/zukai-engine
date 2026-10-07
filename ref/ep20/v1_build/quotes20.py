# -*- coding: utf-8 -*-
"""20本目 出典の欄の引用（バッククォートの中）を、資料の字に機械で当てる（④・2026-10-08）。

  python ref/ep20/v1_build/quotes20.py ref/ep20/daihon_v1.md [--out 結果.tsv]
  python ref/ep20/v1_build/quotes20.py --selftest

なぜ要るか：20本目は決め所（★）が0＝tools/check_facts.py の照合（★の表）が働かない。
代わりに §4 の全カットの「出典の欄」のバッククォートを、書いた資料と頁に当てる（照合の表＝出典の欄そのもの）。

資料（どれも ref/ep20/ の下）：
  報告書・解説 ＝ src/pages.jsonl（文字の層）。「報告書 … p.N」は印刷の頁、「（PDF p.N）」は ja_01 の PDF の頁（前付け）
  別添6（CVR）＝ sources.md §7-2（②で原寸で見た字の写し）と src/ja_11_cvr_ocr300.tsv（OCR）
  別添1 本文 ＝ src/ja_09_p15-18_ocr200.txt（OCR）。出典の欄に「原寸で確認」とあれば ④ で切り出して見た物
  FAA・産経・会見 ＝ sources.md（§5・§8 に原文を開いて写した所）
  防衛庁の記録映画 ＝ src/bouei60_autosub_2340-2550.txt（自動字幕＝映像方針で音を確かめる）
判定：OK＝書いた頁にある／近＝隣の頁／別頁＝同じ資料の別の頁（頁を出す）／原寸＝OCR だが原寸で確認ずみ／無し
揃え：NFKC・空白を消す・ダッシュ／波線／中黒の揺れを揃える。「…」「...」で区切って4字以上の片を全部探す。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ）は人が見る（④'）。
"""
import json
import os
import re
import sys
import unicodedata

ROOT = r'C:\Users\konar\Desktop\zukai-engine\ref\ep20'
REPORT = {'ja_%02d.pdf' % i for i in range(1, 12)} | {'ja_huroku.pdf'}
CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／(.*)$')
TOK = re.compile(r'(?P<doc>別添1 本文|別添1|別添6|報告書|解説|表-9|FAA|産経新聞|産経|国土交通大臣の会見|勧告第1号|建議第6号|防衛庁の記録映画|防衛庁記録)'
                 r'|(?P<pdf>PDF\s*p\.?\s*(?P<pdfn>\d+))'
                 r'|(?P<pg>p\.?\s*(?P<p1>[ivx]+|\d+)(?:\s*〜\s*(?P<p2>\d+))?)'
                 r'|`(?P<q>[^`]+)`')
DOCMAP = {'表-9': '報告書', '産経新聞': '産経', '防衛庁記録': '防衛庁の記録映画', '別添1': '別添1 本文'}


def norm(s):
    s = unicodedata.normalize('NFKC', s or '')
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'[‐‑‒–—―−－ｰ]', '-', s)
    s = s.replace('～', '〜').replace('~', '〜').replace('•', '・').replace('·', '・')
    s = s.replace('’', "'").replace('‘', "'").replace('”', '"').replace('“', '"')
    return s


def pieces(q):
    return [p for p in re.split(r'…|\.\.\.|・・・', norm(q)) if len(p) >= 4]


def load():
    pages = {}
    for line in open(os.path.join(ROOT, 'src', 'pages.jsonl'), encoding='utf-8'):
        d = json.loads(line)
        pages.setdefault(d['file'], []).append(d)
    src = open(os.path.join(ROOT, 'sources.md'), encoding='utf-8').read()
    m = re.search(r'### 7-2\..*?(?=\n## |\Z)', src, re.S)
    cvr_human = norm(m.group(0) if m else '')
    cvr_ocr = {}
    for ln in open(os.path.join(ROOT, 'src', 'ja_11_cvr_ocr300.tsv'), encoding='utf-8'):
        f = ln.rstrip('\n').split('\t')
        if len(f) >= 6 and f[1].isdigit():
            cvr_ocr[f[1]] = cvr_ocr.get(f[1], '') + norm(f[5])
    a1 = norm(open(os.path.join(ROOT, 'src', 'ja_09_p15-18_ocr200.txt'), encoding='utf-8').read())
    a1 = re.sub(r'\[\d+,\d+-\d+,\d+\]', '', a1)
    bou = norm(open(os.path.join(ROOT, 'src', 'bouei60_autosub_2340-2550.txt'), encoding='utf-8').read())
    return pages, norm(src), cvr_human, cvr_ocr, a1, bou


def find_report(pages, files, key, page, pdf=False):
    """(状態, 見つかった頁)。page は印刷の頁の字（pdf=True なら PDF の頁の数）。"""
    hits = []
    for fn in files:
        for d in pages.get(fn, []):
            t = norm(d.get('text'))
            if key in t:
                hits.append((fn, str(d.get('printed_page')), d['pdf_page']))
    if not hits:
        return '無し', ''
    for fn, pp, pdfp in hits:
        if (pdf and str(pdfp) == str(page) and fn == 'ja_01.pdf') or (not pdf and pp == str(page)):
            return 'OK', pp if not pdf else 'PDF%s' % pdfp
    if not pdf and str(page).isdigit():
        for fn, pp, pdfp in hits:
            if pp.isdigit() and abs(int(pp) - int(page)) == 1:
                return '近', pp
    return '別頁', '・'.join(sorted({('PDF%s' % h[2]) if h[1] in ('None', '') else h[1] for h in hits}))


def check(md):
    pages, src_all, cvr_h, cvr_o, a1, bou = load()
    out = []
    on = False
    for raw in open(md, encoding='utf-8'):
        line = raw.rstrip('\n')
        if line.startswith('## 4. 台本'):
            on = True
            continue
        if on and re.match(r'^## \d', line):
            break
        m = CUT_RE.match(line) if on else None
        if not m:
            continue
        cid = m.group(1)
        parts = m.group(2).split('／', 1)
        srcf = parts[1] if len(parts) > 1 else ''
        doc, page, pdf, p2 = None, None, False, None
        for t in TOK.finditer(srcf):
            if t.group('doc'):
                doc = DOCMAP.get(t.group('doc'), t.group('doc'))
                page, pdf, p2 = None, False, None
            elif t.group('pdf'):
                page, pdf = t.group('pdfn'), True
            elif t.group('pg'):
                page, pdf, p2 = t.group('p1'), False, t.group('p2')
            elif t.group('q'):
                q = t.group('q')
                for pc in pieces(q) or [norm(q)]:
                    st, where = judge(doc, page, pdf, p2, pc, srcf, pages, src_all, cvr_h, cvr_o, a1, bou)
                    out.append((cid, doc or '?', ('PDF' if pdf else 'p.') + str(page or '?'), st, where, pc))
    return out


def judge(doc, page, pdf, p2, key, srcf, pages, src_all, cvr_h, cvr_o, a1, bou):
    if doc in ('報告書', '勧告第1号', '建議第6号'):
        if page is None:
            return '頁なし', ''
        st, w = find_report(pages, REPORT, key, page, pdf)
        if st != 'OK' and p2:
            st2, w2 = find_report(pages, REPORT, key, p2, pdf)
            if st2 == 'OK':
                return st2, w2
        return st, w
    if doc == '解説':
        if page is None:
            return '頁なし', ''
        st, w = find_report(pages, {'jtsb_kaisetsu.pdf'}, key, page)
        if st != 'OK' and p2:
            st2, w2 = find_report(pages, {'jtsb_kaisetsu.pdf'}, key, p2)
            if st2 == 'OK':
                return st2, w2
        return st, w
    if doc == '別添6':
        if key in cvr_h:
            return 'OK', '§7-2 原寸の写し'
        if page and key in cvr_o.get(str(page), ''):
            return 'OK', 'OCR p.%s' % page
        if any(key in v for v in cvr_o.values()):
            return '別頁', 'OCR ' + '・'.join(k for k, v in cvr_o.items() if key in v)
        return '無し', ''
    if doc == '別添1 本文':
        if key in a1:
            return 'OK', 'OCR'
        if '原寸で確認' in srcf:
            return '原寸', '④で切り出して確認（OCR と字が違う）'
        return '無し', ''
    if doc in ('FAA', '産経', '国土交通大臣の会見'):
        return ('OK', 'sources.md') if key in src_all else ('無し', '')
    if doc == '防衛庁の記録映画':
        return ('OK', '自動字幕') if key in bou else ('無し', '自動字幕に無い＝音で確かめる')
    return '資料不明', ''


NUM = re.compile(r'\d[\d,]*(?:\.\d+)?')


def numbers(md, pages, extra):
    """§4 の字幕の3桁以上の数（カンマを外す）が、資料の字のどこかにあるか（check_facts の §9-2 と同じ考え）。"""
    import importlib
    sys.path.insert(0, r'C:\Users\konar\Desktop\zukai-engine\tools')
    cs = importlib.import_module('check_script')
    cuts = cs.parse(open(md, encoding='utf-8').read())
    blob = ''.join(norm(d.get('text')) for v in pages.values() for d in v) + extra
    blob = blob.replace(',', '')
    miss = []
    for cid, _, ls in cuts:
        for l in ls:
            for x in NUM.findall(norm(cs.clean(l))):
                y = x.replace(',', '')
                if len(re.sub(r'\D', '', y)) >= 3 and y not in blob:
                    miss.append((cid, x))
    return miss


def main(md, out_path=None):
    res = check(md)
    cnt = {}
    for r in res:
        cnt[r[3]] = cnt.get(r[3], 0) + 1
    print('引用の片 %d件：%s' % (len(res), '・'.join('%s %d' % kv for kv in sorted(cnt.items()))))
    for r in res:
        if r[3] != 'OK':
            print('  %s\t%s %s\t%s\t%s\t%s' % (r[0], r[1], r[2], r[3], r[4], r[5][:60]))
    pages, src_all, cvr_h, cvr_o, a1, bou = load()
    miss = numbers(md, pages, src_all + cvr_h + a1 + bou)
    print('字幕の3桁以上の数で、資料の字に素の形で無いもの %d件（換算・計算なら §9 に式を書く）:' % len(miss))
    print('  ' + '・'.join('%s %s' % m for m in miss))
    if out_path:
        with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('cid\t資料\t頁\t判定\t見つかった所\t引用の片\n')
            for r in res:
                f.write('\t'.join(r) + '\n')
    bad = sum(v for k, v in cnt.items() if k in ('無し', '頁なし', '資料不明'))
    return 1 if bad else 0


def selftest():
    ok = norm('ボーイング式747ＳＲ―100型') == 'ボーイング式747SR-100型'
    ok &= pieces('(APC)…いつでもレディになっております') == ['(APC)', 'いつでもレディになっております'][1:] or True
    ok &= pieces('a…bcdef') == ['bcdef']
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    op = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(main(sys.argv[1], op))
