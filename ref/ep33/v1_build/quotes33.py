# -*- coding: utf-8 -*-
"""33本目 出典の欄の原文の片（バッククォートの中）を、一次資料の文字に機械で当てる（④・2026-11-12・32本目の quotes32.py を写して資料の記号を替えた）。

  python -P ref/ep33/v1_build/quotes33.py ref/ep33/daihon_v1.md [--out 結果.tsv]
  python -P ref/ep33/v1_build/quotes33.py --selftest

なぜ要るか：決め所（★）が0＝tools/check_facts.py の照合が働かない（ルール 4-2 の「多文書の回」）。§4 の全カットの「出典の欄」のバッククォートを、書いた資料に当てる。
書き方＝`記号（`原文の片`…`原文の片`）`。記号：
  〈巻〉¶〈段落〉（調査の報告＝P1ES・P1V1〜P1V4・P2V1〜P2V7。src/inquiry_txt/〈巻〉.txt の全頁から探す＝報告の頁は PDF の頁と印刷の頁がずれる巻があるので段落で引く。
      片が見つかった頁か、その2頁前までに段落の札（「28.6」「2. 11」）があれば OK・札が見えなければ「OK(¶?)」・ほかの巻にしか無ければ「巻違い」。脚注は「¶28.81注72」）
  首（首相の議会での声明 2024-09-04）・警1（警視庁 2026-09-30）・警2（2026-05-19）・警3（2024-05-22／09-04）・
  応（政府の応答 CP 1248・2025-02-26）・年（年次報告 CP 1512・2026-02-25）・進（進捗報告 第6回・2026-09-10）・
  中（独立レビューの中間 2017-12）・終（最終 2018-05）・法（建築安全法 2022）・塔（塔の将来・取り壊し・住民向けお知らせ）・市（ロンドン市長の発表 2017-06-15）・
  香（香港の警察・独立委員会・政府）・国（国交省 2017-10-06 の資料6・F11 の報告）・消（消防庁の通知 2026-03-30）
  計（こちらの計算＝当てない）・画（画面の表示＝当てない）
揃え＝NFKC・小文字・曲がった引用符を直す・英数字とかなと漢字のほかを全部消す（空白・句読点・ハイフン・括弧）。「…」で区切った片を全部探す。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属・条件節）は人と係が見る（ルール 4'-12）。
"""
import glob
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')
VOLS = ['P1ES', 'P1V1', 'P1V2', 'P1V3', 'P1V4', 'P2V1', 'P2V2', 'P2V3', 'P2V4', 'P2V5', 'P2V6', 'P2V7']
WEB = {'首': ['web/avoid/pm.html.txt'],
       '警1': ['web/met/m1.html.txt'], '警2': ['web/met/m2.html.txt'], '警3': ['web/met/m3.html.txt', 'web/met/m4.html.txt'],
       '応': ['web/govuk/resp.html.txt', 'web/govuk/resp_pub.html.txt'],
       '年': ['web/govuk/annual_main.html.txt', 'web/govuk/annual-report-february-2026-summary-update.html.txt',
             'web/govuk/grenfell-tower-inquiry-government-annual-report-february-2026.html.txt'],
       '進': ['web/govuk/prog_pub.html.txt', 'web/govuk/progress-report-september-2026-summary-update.html.txt',
             'web/govuk/grenfell-tower-inquiry-government-progress-report-september-2026.html.txt'],
       '中': ['web/review/interim_web.pdf.txt',
             'web/review/independent-review-of-building-regulations-and-fire-safety-interim-report.html.txt'],
       '終': ['web/review/final_web.pdf.txt',
             'web/review/independent-review-of-building-regulations-and-fire-safety-final-report.html.txt'],
       '法': ['web/leg/*.txt'],
       '塔': ['web/tower/*.txt', 'inquiry_txt/GOV_Sept2026_community_update.txt'],
       '市': ['web/lfb/gla39157.html.txt'],
       '香': ['web/hk/*.txt'],
       '国': ['web/jp/*.txt', 'inquiry_txt/MLIT_001205300.txt'],
       '消': ['inquiry_txt/FDMA_20260330yo120.txt']}
NOCHECK = {'計', '画'}
CUT_RE = re.compile(r'^\*\*([a-z][0-9a-z]\d{2})\*\*\s*(?:🔧\s*)?／\s*.*?\s*／\s*(.*)$', re.M)
TOK = re.compile(r'(?P<rep>P[12](?:V\d|ES)¶\d+\.\d+(?:注\d+)?)（|(?P<doc>首|警1|警2|警3|応|年|進|中|終|法|塔|市|香|国|消|計|画)（'
                 r'|`(?P<q>[^`]+)`')
KEEP = re.compile(r'[0-9a-z぀-ヿ㐀-鿿]')
_vol = {}
_web = {}


def norm(s):
    s = unicodedata.normalize('NFKC', s or '').lower()
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    return ''.join(KEEP.findall(s))


def vol_pages(v):
    """巻 → {頁: (生の文字, 揃えた文字)}。無ければ None。"""
    if v not in _vol:
        p = os.path.join(SRC, 'inquiry_txt', v + '.txt')
        if not os.path.exists(p):
            _vol[v] = None
        else:
            t = open(p, encoding='utf-8').read()
            parts = re.split(r'=====\[p(\d+)\]=====', t)
            _vol[v] = {int(parts[i]): (parts[i + 1], norm(parts[i + 1])) for i in range(1, len(parts), 2)}
    return _vol[v]


def find_pages(pages, n):
    """片がある頁（頁の境をまたぐ片は前の頁）。"""
    hit = []
    ks = sorted(pages)
    for i, k in enumerate(ks):
        cur = pages[k][1]
        nxt = pages[ks[i + 1]][1] if i + 1 < len(ks) else ''
        if n in cur or (n in cur + nxt and n not in nxt):
            hit.append(k)
    return hit


def para_re(para):
    a, b = para.split('.')
    return re.compile(r'(?<![\d.])%s\.\s?%s(?![\d])' % (a, b))


def check_report(ref, part):
    m = re.match(r'(P[12](?:V\d|ES))¶(\d+\.\d+)(?:注(\d+))?$', ref)
    vol, para = m.group(1), m.group(2)
    n = norm(part)
    if len(n) < 6:
        return '短い'
    pages = vol_pages(vol)
    if pages is None:
        return '資料が無い'
    hit = find_pages(pages, n)
    if not hit:
        other = [v for v in VOLS if v != vol and vol_pages(v) and find_pages(vol_pages(v), n)]
        return ('巻違い:' + ','.join(other)) if other else '無し'
    rx = para_re(para)
    for p in hit:
        for q in (p, p - 1, p - 2):
            if q in pages and rx.search(pages[q][0]):
                return 'OK'
    return 'OK(¶?):p%s' % ','.join(map(str, hit[:3]))


def web_texts(code):
    if code not in _web:
        out = []
        for pat in WEB[code]:
            for f in sorted(glob.glob(os.path.join(SRC, pat))):
                out.append(norm(open(f, encoding='utf-8', errors='replace').read()))
        _web[code] = out
    return _web[code]


def check_fragment(doc, q):
    """(判定, 片) の列を返す。"""
    out = []
    for part in re.split(r'…|\.\.\.', q):
        part = part.strip()
        if not part:
            continue
        if doc in NOCHECK:
            out.append((doc, part))
        elif doc and doc.startswith('P'):
            out.append((check_report(doc, part), part))
        elif doc in WEB:
            n = norm(part)
            if len(n) < 6:
                out.append(('短い', part))
                continue
            texts = web_texts(doc)
            out.append((('OK' if any(n in t for t in texts) else '無し') if texts else '資料が無い', part))
        else:
            out.append(('記号が無い:%s' % doc, part))
    return out


def run(md, outp=None):
    text = open(md, encoding='utf-8').read()
    res = []
    empty = []
    for m in CUT_RE.finditer(text):
        cid, src = m.group(1), m.group(2)
        doc = None
        nq = 0
        for t in TOK.finditer(src):
            if t.group('rep'):
                doc = t.group('rep')
            elif t.group('doc'):
                doc = t.group('doc')
            else:
                nq += 1
                for verdict, part in check_fragment(doc, t.group('q')):
                    res.append((cid, doc or '?', verdict, part))
        if nq == 0 and '計' not in src and '画' not in src and '―' not in src:
            empty.append(cid)
    cnt = {}
    for _, _, v, _ in res:
        k = v.split(':')[0]
        cnt[k] = cnt.get(k, 0) + 1
    bad = [r for r in res if not (r[2] == 'OK' or r[2] in NOCHECK)]
    print('片 %d：%s' % (len(res), '・'.join('%s %d' % kv for kv in sorted(cnt.items(), key=lambda kv: -kv[1]))))
    for cid, doc, v, part in bad:
        print('  %s %s %s %s' % ('⚠️' if v.startswith('OK(') else '🔴', cid, doc, v), '｜', part[:90])
    if empty:
        print('片の無いカット（計・画・― のほか）%d: %s' % (len(empty), ' '.join(empty)))
    if outp:
        with open(outp, 'w', encoding='utf-8', newline='\n') as f:
            f.write('# quotes33.py の結果（片＝台本の出典の欄のバッククォート）\n')
            for r in res:
                f.write('\t'.join(r) + '\n')
        print('→', outp)
    return sum(1 for r in bad if not r[2].startswith('OK('))


def selftest():
    ok = norm('“Bears  No-Blame”') == 'bearsnoblame'
    ok &= bool(para_re('2.11').search('2. 11 The following')) and not para_re('2.11').search('12.11')
    ok &= check_report('P1ES¶2.12', 'bears no blame') == 'OK'
    ok &= check_report('P1V4¶28.6', 'by 01.30 at the earliest and by 01.50 at the latest') == 'OK'
    ok &= check_report('P1V4¶28.6', 'this sentence is not in the report at all') == '無し'
    ok &= check_report('P1V1¶3.9', 'just over 67 metres tall') == 'OK'
    ok &= check_report('P1V2¶3.9', 'just over 67 metres tall').startswith('巻違い')
    ok &= check_fragment('首', 'the simple truth is that the deaths that occurred were all avoidable')[0][0] == 'OK'
    ok &= check_fragment('警1', 'The 20 files relate to 20 companies and organisations and 54 individuals')[0][0] == 'OK'
    ok &= check_fragment('国', 'ロンドン火災との比較において極めて危険という状況は認められない')[0][0] == 'OK'
    ok &= check_fragment('消', '工事用シートは、消防法令に基づき、防炎物品を使用すること')[0][0] == 'OK'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    op = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(1 if run(sys.argv[1], op) else 0)
