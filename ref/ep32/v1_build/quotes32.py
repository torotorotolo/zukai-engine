# -*- coding: utf-8 -*-
"""32本目 出典の欄の原文の片（バッククォートの中）を、一次資料の文字に機械で当てる（④・2026-11-09・31本目の quotes31.py を写した）。

  python -P ref/ep32/v1_build/quotes32.py ref/ep32/daihon_v1.md [--out 結果.tsv]
  python -P ref/ep32/v1_build/quotes32.py --selftest

なぜ要るか：決め所（★）が0＝tools/check_facts.py の照合が働かない（ルール 4-2 の「多文書の回」）。§4 の全カットの「出典の欄」のバッククォートを、書いた資料に当てる。
書き方＝`記号（`原文の片`…`原文の片`）`。記号：
  報p〈N〉（報告書 NTSB/AAR-10/03 の PDF の頁 N。N と N+1 の頁をつないだ中を探す＝頁の境で割れた文も拾う。ほかの頁にしか無ければ「頁違い」）
  ド#〈品目〉p〈N〉（公開ドケットの品目＝src/ntsb/docket/〈3桁〉_*.txt の頁 N と N+1。公聴会の速記〈#109〜#111〉は行番号を消してから照らす）
  官（連邦官報 2023-06413 の窓＝src/web/fr2023_06413.txt）・通（AP の記事の転載〈PBS〉の窓＝src/web/ap_sully_pbs.txt）・観（ノースカロライナ州の観光の案内の窓＝src/web/visitnc_museum.txt）
  勧（NTSB の勧告のデータベース CAROL の控え＝src/carol/carol_dca09ma026.json。片＝「A-10-067 受け入れられない対応 2014-07-23」の形＝番号・状態・閉じた日を照らす）
  業（業界紙＝控えなし＝当てない）・聞（報道＝控えなし＝当てない）・画（画面の表示＝当てない）・計（こちらの計算＝当てない）
揃え＝NFKC・小文字・曲がった引用符を直す・英数字とかなと漢字のほかを全部消す（空白・句読点・ハイフン・括弧）。「…」で区切った片を全部探す。
⚠️ 判定は「その字が資料にあるか」まで。意味が合っているか（言い換えの強さ・帰属・条件節）は人と係が見る（ルール 4'-12）。
"""
import glob
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'src')
WEB = {'官': 'web/fr2023_06413.txt', '通': 'web/ap_sully_pbs.txt', '観': 'web/visitnc_museum.txt'}
NOCHECK = {'業': '業', '聞': '聞', '画': '画', '計': '計'}
STATUS = {'受け入れられる対応': '2', 'それに代わる対応': '3', '受け入れられない対応': '4', '見直し': '5',
          '開いている': '8'}
TRANSCRIPT = {109, 110, 111}
CUT_RE = re.compile(r'^\*\*([a-z][0-9a-z]\d{2})\*\*\s*(?:🔧\s*)?／\s*.*?\s*／\s*(.*)$', re.M)
TOK = re.compile(r'(?P<aar>報p\d+)（|(?P<dk>ド#\d+p\d+)（|(?P<doc>[官通観勧業聞画計])（|`(?P<q>[^`]+)`')
KEEP = re.compile(r'[0-9a-z぀-ヿ㐀-鿿]')
_pages = {}
_carol = None


def norm(s, transcript=False):
    s = unicodedata.normalize('NFKC', s or '').lower()
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    if transcript:
        s = re.sub(r'(?<![0-9a-z])\d{1,2}(?![0-9a-z])', ' ', s)     # 速記の行番号（文の途中に入る）を消す＝片の側も同じに
    return ''.join(KEEP.findall(s))


def pages_of(path, transcript=False):
    key = (path, transcript)
    if key not in _pages:
        if not os.path.exists(path):
            _pages[key] = None
        else:
            t = open(path, encoding='utf-8', errors='replace').read()
            parts = re.split(r'=====\[p(\d+)\]=====', t)
            if len(parts) > 1:
                _pages[key] = {int(parts[i]): norm(parts[i + 1], transcript) for i in range(1, len(parts), 2)}
            else:
                _pages[key] = {1: norm(t, transcript)}
    return _pages[key]


def find_in_pages(pages, n, page):
    if page is None:
        return 'OK' if any(n in v for v in pages.values()) else '無し'
    near = pages.get(page, '') + pages.get(page + 1, '')
    if n in near:
        return 'OK'
    other = [p for p, v in sorted(pages.items()) if n in v]
    return ('頁違い:p%s' % ','.join(map(str, other[:3]))) if other else '無し'


def carol(q):
    global _carol
    if _carol is None:
        p = os.path.join(SRC, 'carol', 'carol_dca09ma026.json')
        _carol = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    m = re.match(r'\s*(A-\d{2}-\d{3})\s+(\S+)(?:\s+(\d{4}-\d{2}-\d{2}))?\s*$', q)
    if not m:
        return '勧の形が違う'
    rec = _carol.get(m.group(1))
    if rec is None:
        return '勧の番号が無い'
    if STATUS.get(m.group(2)) != str(rec.get('Status')):
        return '勧の状態が違う（控え=%s）' % rec.get('Status')
    if m.group(3) and not str(rec.get('DateClosed') or '').startswith(m.group(3)):
        return '勧の日が違う（控え=%s）' % rec.get('DateClosed')
    return 'OK'


def check_fragment(doc, q):
    """(判定, 片) の列を返す。"""
    if doc == '勧':
        return [(carol(q), q)]
    out = []
    for part in re.split(r'…|\.\.\.', q):
        part = part.strip()
        if not part:
            continue
        if doc in NOCHECK:
            out.append((NOCHECK[doc], part))
            continue
        m_aar = re.match(r'報p(\d+)$', doc)
        m_dk = re.match(r'ド#(\d+)p(\d+)$', doc)
        if m_aar:
            n = norm(part)
            if len(n) < 6:
                out.append(('短い', part))
                continue
            pages = pages_of(os.path.join(SRC, 'ntsb', 'AAR1003.txt'))
            out.append((find_in_pages(pages, n, int(m_aar.group(1))) if pages else '資料が無い', part))
        elif m_dk:
            item, page = int(m_dk.group(1)), int(m_dk.group(2))
            tr = item in TRANSCRIPT
            n = norm(part, tr)
            if len(n) < 6:
                out.append(('短い', part))
                continue
            fs = glob.glob(os.path.join(SRC, 'ntsb', 'docket', '%03d_*.txt' % item))
            pages = pages_of(fs[0], tr) if fs else None
            out.append((find_in_pages(pages, n, page) if pages else '資料が無い', part))
        elif doc in WEB:
            n = norm(part)
            if len(n) < 6:
                out.append(('短い', part))
                continue
            pages = pages_of(os.path.join(SRC, WEB[doc]))
            out.append((find_in_pages(pages, n, None) if pages else '資料が無い', part))
        else:
            out.append(('記号が無い:' + doc, part))
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
            if t.group('aar') or t.group('dk') or t.group('doc'):
                doc = t.group('aar') or t.group('dk') or t.group('doc')
            elif t.group('q'):
                nq += 1
                if doc is None:
                    res.append((cid, '記号なし', t.group('q')))
                    continue
                for verdict, part in check_fragment(doc, t.group('q')):
                    res.append((cid, verdict, doc + ' ' + part))
        if nq == 0:
            empty.append(cid)
    cnt = {}
    for _, v, _ in res:
        cnt[v] = cnt.get(v, 0) + 1
    print('片 %d: %s' % (len(res), ' '.join('%s=%d' % kv for kv in sorted(cnt.items()))))
    print('片の無いカット %d: %s' % (len(empty), ' '.join(empty)))
    bad = [r for r in res if r[1] not in ('OK',) + tuple(NOCHECK)]
    for cid, v, s in bad:
        print('🔴 %s %s: %s' % (cid, v, s[:100]))
    if outp:
        with open(outp, 'w', encoding='utf-8', newline='\n') as f:
            for cid, v, s in res:
                f.write('%s\t%s\t%s\n' % (cid, v, s))
    return 1 if bad else 0


def selftest():
    ok = norm('Cactus fifteen-thirty nine, “hit birds.”') == 'cactusfifteenthirtyninehitbirds'
    r = check_fragment('報p19', "we're unable. we may end up in the Hudson")
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('報p67', 'In eight of the 15 runs (53 percent), the pilot successfully landed after making an immediate turn')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('報p67', 'the pilot successfully landed after a 35-second delay')                 # 陰性（崩れた言い方）
    ok &= bool(r) and r[0][0] == '無し'
    r = check_fragment('報p19', 'In eight of the 15 runs (53 percent)')                                  # 陰性（頁違い）
    ok &= bool(r) and r[0][0].startswith('頁違い')
    r = check_fragment('ド#7p5', 'The Airbus had a ditching button, but he did not push it')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('ド#109p18', 'a successful return to LaGuardia or a diversion to Teterboro Airport was not assured')
    ok &= bool(r) and r[0][0] == 'OK'                                                                   # 速記の行番号をまたぐ
    r = check_fragment('勧', 'A-10-067 受け入れられない対応 2014-07-23')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('勧', 'A-10-072 受け入れられない対応')                                              # 陰性（状態が違う）
    ok &= bool(r) and r[0][0].startswith('勧の状態')
    r = check_fragment('官', 'As a result of the Flight 1549 accident, the FAA began studying')
    ok &= bool(r) and r[0][0] == 'OK'
    r = check_fragment('画', 'ENG DUAL FAILURE')
    ok &= bool(r) and r[0][0] == '画'
    print('selftest', 'ok' if ok else 'NG')
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    op = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
    sys.exit(run(sys.argv[1], op))
