# -*- coding: utf-8 -*-
"""22本目 出典の欄の引用（バッククォートの中）を、3冊の文字の層に機械で当てる（④・2026-10-14・21本目の quotes21.py の考え方を写した）。

  python ref/ep22/v1_build/quotes22.py ref/ep22/daihon_v1.md [--out 結果.tsv]
  python ref/ep22/v1_build/quotes22.py --selftest

なぜ要るか：22本目も決め所（★）が0＝tools/check_facts.py の照合（★の表）が働かない。
代わりに §4 の全カットの「出典の欄」のバッククォートを、書いた資料と頁・節に当てる（照合の表＝出典の欄そのもの）。

資料（どれも ref/ep22/src/ の下＝git の外）：
  USCG ＝ uscg_mbi_pages.txt（「USCG p.35〈27〉」＝PDF の頁 35・〈〉は印字＝PDF−8。頁の印「=== PDF p.N ｜ 印字 p.X ===」）
  NTSB ＝ ntsb_mir2536_pages.txt（「NTSB p.44」＝PDF の頁）
  TSB  ＝ tsb_m23a0169_html.txt（「TSB §1.3.1」＝節の番号。節は見出しの行から次の見出しの行まで。NBSP は空白として揃える）
         「TSB 付録A」「TSB 付録B」＝本文の Appendix A／B と core_raw/tsb_appxA.tsv・tsb_appxB.tsv
判定：OK＝書いた頁・節にある／近＝隣の頁／別頁・別節＝同じ資料の別の所（どこかを出す）／無し／資料なし
揃え：NFKC・小文字・空白を消す・ダッシュと引用符の揺れを揃える（行末ハイフンは「消した版」でも探す）。「…」「...」で区切って4字以上の片を全部探す。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属）は人が見る（④'）。
"""
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'C:\Users\konar\Desktop\zukai-engine'
EP = os.path.join(ROOT, 'ref', 'ep22')
SRC = os.path.join(EP, 'src')
CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／(.*)$')
TOK = re.compile(r'(?P<doc>USCG|NTSB|TSB)'
                 r'|(?P<pg>p\.?\s*(?P<p1>\d+)(?:〈[^〉]*〉)?(?:\s*〜\s*p?\.?\s*(?P<p2>\d+)(?:〈[^〉]*〉)?)?)'
                 r'|(?P<sec>§\s*(?P<s>\d+(?:\.\d+)*))'
                 r'|(?P<app>付録\s*(?P<a>[A-C]))'
                 r'|`(?P<q>[^`]+)`')
PAGE = re.compile(r'^=== PDF p\.(\d+) ｜ 印字 p\.\S+ ===\s*$', re.M)
HEAD = re.compile(r'^(\d+(?:\.\d+)*)[ \u00a0]+([A-Z][^\n]{0,150})$')


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


def _pages(path):
    raw = open(path, encoding='utf-8', errors='replace').read()
    out = {}
    ms = list(PAGE.finditer(raw))
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(raw)
        out[int(m.group(1))] = norm(raw[m.end():end])
    return out


def _tsb(path):
    """節ごとの文字（節の番号 → 揃えた字）。付録は 'A'・'B'・'C'。"""
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    secs, cur, buf = {}, '前', []
    for ln in lines:
        s = ln.strip()
        m = HEAD.match(s)
        app = re.match(r'^Appendix[  ]+([A-C])\b', s)
        if (m and not s.endswith('.')) or app:
            secs[cur] = secs.get(cur, '') + norm('\n'.join(buf))
            cur, buf = (app.group(1) if app else m.group(1)), [ln]
        else:
            buf.append(ln)
    secs[cur] = secs.get(cur, '') + norm('\n'.join(buf))
    return secs


def _txt(path):
    return norm(open(path, encoding='utf-8', errors='replace').read()) if os.path.exists(path) else ''


def load():
    return {'USCG': _pages(os.path.join(SRC, 'uscg_mbi_pages.txt')),
            'NTSB': _pages(os.path.join(SRC, 'ntsb_mir2536_pages.txt')),
            'TSB': _tsb(os.path.join(SRC, 'tsb_m23a0169_html.txt')),
            'TSB_A': _txt(os.path.join(SRC, 'core_raw', 'tsb_appxA.tsv')),
            'TSB_B': _txt(os.path.join(SRC, 'core_raw', 'tsb_appxB.tsv'))}


def _in(piece, text):
    return piece in text or nohy(piece) in nohy(text)


def find(D, doc, p1, p2, sec, piece):
    """戻り値＝(判定, 見つかった所)"""
    if doc in ('USCG', 'NTSB'):
        pages = D[doc]
        if p1 is not None:
            want = list(range(p1, (p2 or p1) + 1))
            for p in want:
                if _in(piece, pages.get(p, '')):
                    return 'OK', 'p.%d' % p
            for p in (want[0] - 1, want[-1] + 1):
                if _in(piece, pages.get(p, '')):
                    return '近', 'p.%d' % p
        hit = [p for p, t in sorted(pages.items()) if _in(piece, t)]
        if hit:
            return '別頁', ','.join('p.%d' % h for h in hit[:6])
        return '無し', '-'
    if doc == 'TSB':
        secs = D['TSB']
        if sec in ('A', 'B') and _in(piece, D['TSB_' + sec]):
            return 'OK', '付録%s（表）' % sec
        if sec is not None:
            for k, t in secs.items():
                if (k == sec or k.startswith(sec + '.')) and _in(piece, t):
                    return 'OK', ('付録' + k) if k in 'ABC' else '§' + k
        hit = [k for k, t in secs.items() if _in(piece, t)]
        if not hit:
            hit = ['付録%s（表）' % a for a in 'AB' if _in(piece, D['TSB_' + a])]
        if hit:
            # 節を書かずに引いた片（脚注など）は、TSB のどこかにあれば OK（どこにあったかを出す）
            return ('OK' if sec is None else '別節'), ','.join(
                ('付録' + h) if h in 'ABC' else ('§' + h if h[0].isdigit() else h) for h in hit[:6])
        return '無し', '-'
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
        doc, p1, p2, sec = None, None, None, None
        for t in TOK.finditer(srccol):
            if t.group('doc'):
                doc, p1, p2, sec = t.group('doc'), None, None, None
            elif t.group('pg'):
                p1 = int(t.group('p1'))
                p2 = int(t.group('p2')) if t.group('p2') else None
            elif t.group('sec'):
                sec = t.group('s')
            elif t.group('app'):
                sec = t.group('a')
            elif t.group('q'):
                where_cited = ('p.%d' % p1) if p1 is not None else (('§' + sec) if sec and sec[0].isdigit()
                                                                    else ('付録' + sec) if sec else '-')
                for pc in pieces(t.group('q')):
                    v, where = find(D, doc, p1, p2, sec, pc) if doc else ('資料なし', '-')
                    rows.append((cid, doc or '-', where_cited, v, where, pc))
    return rows


def main(path, out=None):
    D = load()
    rows = scan(open(path, encoding='utf-8').read(), D)
    out = out or os.path.join(EP, 'v1_build', 'quotes22_result.tsv')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('cid\t資料\t頁・節\t判定\t見つかった所\t引用の片\n')
        for r in rows:
            f.write('\t'.join(r) + '\n')
    cnt = {}
    for r in rows:
        cnt[r[3]] = cnt.get(r[3], 0) + 1
    print('片 %d → %s  %s' % (len(rows), out, cnt))
    for r in rows:
        if r[3] != 'OK':
            print('  %s %s %s %s %s  %s' % r)
    return sum(1 for r in rows if r[3] in ('無し', '資料なし'))


def selftest():
    D = {'USCG': {35: norm('TITAN sent a text message "dropped two wts" at 10:47:02'), 36: norm('han- dled it')},
         'NTSB': {44: norm('the scraping marks')},
         'TSB': {'1.3.2': norm('was displayed at 10:47:26.903'), '2.1': norm('The reason is unknown'),
                 'A': norm('10:47:26.9 T dropped two wts')},
         'TSB_A': norm('10:47:26.9\tT\tdropped two wts'), 'TSB_B': ''}
    md = ('## 4. 台本\n**c101** ／ 実写 x ／ USCG p.35〈27〉（`"dropped two wts" at 10:47:02`）・p.35（`handled it`）'
          '・NTSB p.43（`scraping marks`）・TSB §1.3.2（`displayed at 10:47:26.903`）・§1.3（`reason is unknown`）'
          '・付録A（`dropped two wts`）・USCG p.35（`no such words`）\n## 5. x\n')
    got = [(r[0], r[3]) for r in scan(md, D)]
    want = [('c101', 'OK'), ('c101', '近'), ('c101', '近'), ('c101', 'OK'), ('c101', '別節'), ('c101', 'OK'),
            ('c101', '無し')]
    ok = got == want
    ok &= _tsb.__doc__ is not None and bool(HEAD.match('1.3.2\u00a0Descent of the\u00a0Titan'))
    print('selftest', 'ok' if ok else 'NG', got)
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    o = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(1 if main(sys.argv[1], o) else 0)
