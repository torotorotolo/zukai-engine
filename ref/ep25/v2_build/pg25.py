# -*- coding: utf-8 -*-
"""25本目④'：一次資料の文字の層を引く道具（照合の係と G0 が同じ物差しで原文を引く・24本目 pg24.py の考え方を、
v1_build/quotes25.py の資料の表〈日本語の PDF の頁ごとの txt/*.json・HTML・国会会議録の JSON〉に替えた）。

  python ref/ep25/v2_build/pg25.py page R1 222            # R1 の印刷頁 222 をそのまま出す（PDF頁も添える）
  python ref/ep25/v2_build/pg25.py page R1 219 221        # 印刷頁 219〜221
  python ref/ep25/v2_build/pg25.py find R1 "低いものと考えられる"      # 空白・改行・引用符・ダッシュの揺れを無視して探す（頁の境もまたぐ）
  python ref/ep25/v2_build/pg25.py find R1 "焦って" --ctx 300 --max 30
  python ref/ep25/v2_build/pg25.py find all "後出しじゃんけん"          # 全部の資料（PDF・HTML・JR西日本・国会）
  python ref/ep25/v2_build/pg25.py re S3 "予見(可能性|でき)"           # 正規表現（NFKC・空白を消した字に当てる）
  python ref/ep25/v2_build/pg25.py find Kk "いずれも無罪"              # 国会会議録（発言ごと＝日付・院・会議・役職・URL）
  python ref/ep25/v2_build/pg25.py docs                    # 記号と資料の一覧
  python ref/ep25/v2_build/pg25.py --selftest

頁＝**印刷頁**（sources.md・台本の出典の欄と同じ。R1＝PDF−11・S1＝PDF−8・判決は PDF と同じ・付図と JR西日本の PDF は PDF頁）。
消防庁 F1・F2 は PDF頁（印刷頁の推定が負になる＝quotes25.PDF_PAGED）。HTML・国会・JR西日本は頁が無い（全文）。
出す字は NFKC で空白を消した字（頁の境は「⏎頁⏎」）。⚠️ 「0件」は「この綴りでは出ない」であって「無い」ではない
（言い換え・旧字・数字の書き方〈漢数字／算用数字〉・頁の境・脚注の番号〈「41号柱(副柱23)」〉でも探す）。
⚠️ 名前：git の外の src/names_private.txt の名前と、国会の発言の頭「○役職（名前君）」は［名前］に伏せて出す。
係の記録・リポのファイルには、乗客・遺族・負傷者・被告人・委員・社長の名前を写さない（役職で書く）。
"""
import glob
import html as H
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'v1_build'))
import quotes25 as Q  # noqa: E402  資料の表（PDFS・HTMLS・JRW_HTML・JRW_TXT・PDF_PAGED）を1か所にする

SRC = Q.SRC
NAMES = [ln.strip() for ln in open(os.path.join(SRC, 'names_private.txt'), encoding='utf-8')
         if ln.strip() and not ln.startswith('#')]
NAMES.sort(key=len, reverse=True)
SPK = re.compile(r'○([^○（(\s]{1,30})[（(][^）)]{1,12}[）)]')   # NFKC のあとは丸かっこが半角（10-25 に伏せ損ないを見つけて直した）


def nf(s):
    """NFKC・空白を消す（大文字小文字・引用符はそのまま＝表示用）。"""
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', s or ''))


NAME_RX = [re.compile(r'\s*'.join(re.escape(c) for c in n)) for n in NAMES]   # 行の切れ目で割れた名前（「山\n崎」）も伏せる


SHI = re.compile(r'[一-龥々]{2,5}(?=\s*氏)')   # 「〇〇氏」＝表に無い名前も伏せる（10-25 当て直しの係が S1 p.16 の伏せ漏れを知らせた）


def mask(s):
    s = SPK.sub(lambda m: '○%s（［名前］）' % m.group(1), s)
    for rx in NAME_RX:
        s = rx.sub('［名前］', s)
    s = SHI.sub('［名前］', s)
    return s


def raw_pages(name):
    """[(頁の札, 印刷頁, PDF頁, 字)]。"""
    out = []
    for d in json.load(open(os.path.join(SRC, 'txt', name + '.json'), encoding='utf-8')):
        pr = d['printed'] if d.get('printed') is not None and name not in Q.PDF_PAGED else d['pdf']
        lab = 'p.%s（PDF%s）' % (pr, d['pdf']) if pr != d['pdf'] else 'PDF p.%s' % d['pdf']
        if d.get('garble'):
            lab += '［字化け %s］' % d['garble']
        out.append((lab, int(pr), int(d['pdf']), d.get('raw') or ''))
    return out


def html_raw(rel):
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
    return H.unescape(t)


def load(doc):
    """[(頁の札, 印刷頁 or None, 字)]。"""
    if doc == 'Kk':
        seen, out = set(), []
        for fn in sorted(glob.glob(os.path.join(SRC, 'kokkai', 'kokkai_*.json'))):
            d = json.load(open(fn, encoding='utf-8'))
            for r in (d.get('speechRecord', []) if isinstance(d, dict) else d):
                if not isinstance(r, dict) or r.get('speechID') in seen:
                    continue
                seen.add(r.get('speechID'))
                lab = '%s %s %s 発言%s（%s）%s' % (r.get('date'), r.get('nameOfHouse', ''), r.get('nameOfMeeting', ''),
                                              r.get('speechOrder'), r.get('speakerPosition') or r.get('speakerRole') or '',
                                              r.get('speechURL', ''))
                out.append((lab, None, r.get('speech', '')))
        out.sort(key=lambda x: x[0])
        return out
    if doc == 'J':
        out = [('jrw/' + os.path.basename(r), None, html_raw(r)) for r in Q.JRW_HTML if os.path.exists(os.path.join(SRC, r))]
        for nm in Q.JRW_TXT:
            out += [('%s %s' % (nm, lab), pr, t) for lab, pr, _p, t in raw_pages(nm)]
        return out
    if doc in Q.HTMLS:
        return [(r, None, html_raw(r)) for r in Q.HTMLS[doc]]
    if doc in Q.PDFS:
        return [(lab, pr, t) for lab, pr, _p, t in raw_pages(Q.PDFS[doc])]
    raise SystemExit('記号が無い: %s（docs で一覧）' % doc)


def alldocs():
    return list(Q.PDFS) + list(Q.HTMLS) + ['J', 'Kk']


def loose(q):
    """探す句 → 空白・引用符・かぎかっこ・中黒・波線・ダッシュの揺れを許す正規表現（NFKC・空白を消した字に当てる）。"""
    q = nf(q)
    parts = []
    for c in q:
        if c in '‘’“”\'"`´「」『』':
            parts.append(r'[‘’“”\'"`´「」『』]?')
        elif c in '-‐‑‒–—―−－ｰ':
            parts.append(r'[-‐‑‒–—―−－ｰ]')
        elif c in '~～∼〜':
            parts.append(r'[~～∼〜]')
        elif c in '·・ㆍ･':
            parts.append(r'[·・ㆍ･]')
        else:
            parts.append(re.escape(c))
    return re.compile(r'[「」『』‘’“”]?'.join(parts), re.I)


def show_hits(doc, rx, ctx, mx, rng=None, out=print):
    pages = load(doc)
    if rng:
        pages = [p for p in pages if p[1] is not None and rng[0] <= p[1] <= rng[1]]
    starts, buf, pos = [], [], 0
    for lab, pr, t in pages:
        t = nf(t)
        starts.append((pos, lab))
        buf.append(t)
        pos += len(t)
    whole = ''.join(buf)
    bounds = [p for p, _ in starts]
    n = 0
    for m in rx.finditer(whole):
        n += 1
        if n > mx:
            continue
        i = max(k for k, p in enumerate(bounds) if p <= m.start())
        j = max(k for k, p in enumerate(bounds) if p <= max(m.start(), m.end() - 1))
        cross = '（頁の境をまたぐ→%s）' % starts[j][1] if j != i else ''
        a, b = max(0, m.start() - ctx), min(len(whole), m.end() + ctx)
        seg = ''
        for k in range(a, b):
            if k in bounds and k != a:
                seg += '⏎頁⏎'
            if k == m.start():
                seg += '【'
            seg += whole[k]
            if k == m.end() - 1:
                seg += '】'
        out('- %s %s%s: …%s…' % (doc, starts[i][1], cross, mask(seg)))
    if n > mx:
        out('  （%s: %d件中 %d件だけ表示）' % (doc, n, mx))
    return n


def main(a):
    if not a or a[0] == '--selftest':
        return selftest()
    cmd = a[0]
    if cmd == 'docs':
        for k, v in Q.PDFS.items():
            print(k, v)
        for k, v in Q.HTMLS.items():
            print(k, v)
        print('J', 'JR西日本の HTML と PDF の和（J0〜J7）')
        print('Kk', '国会会議録（kokkai/*.json）')
        return 0
    ctx = int(a[a.index('--ctx') + 1]) if '--ctx' in a else 120
    mx = int(a[a.index('--max') + 1]) if '--max' in a else 12
    rng = None
    if '--pages' in a:
        x = a[a.index('--pages') + 1]
        rng = tuple(int(v) for v in x.split('-')) if '-' in x else (int(x), int(x))
    opt = ('--ctx', '--max', '--pages')
    pos = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in opt)]
    doc = pos[1]
    if doc.startswith('J') and doc not in Q.PDFS:
        doc = 'J'
    if cmd == 'page':
        p1 = int(pos[2])
        p2 = int(pos[3]) if len(pos) > 3 else p1
        for lab, pr, t in load(doc):
            if pr is not None and p1 <= pr <= p2:
                t = unicodedata.normalize('NFKC', t)
                t = re.sub(r'[ \t　]+', ' ', t)
                t = re.sub(r'\n\s*\n+', '\n', t)
                print('=== %s %s ===' % (doc, lab))
                print(mask(t.strip()))
        return 0
    docs = alldocs() if doc == 'all' else [doc]
    q = pos[2]
    rx = loose(q) if cmd == 'find' else re.compile(nf(q), re.I)
    print('### %s %s「%s」' % (cmd, doc, q))
    tot = 0
    for d in docs:
        tot += show_hits(d, rx, ctx, mx, rng)
    if not tot:
        print('  0件（⚠️ この綴りでは出ない＝無いとは限らない。言い換え・漢数字・頁の境・脚注の番号でも探す）')
    return 0


def selftest():
    import io
    ok = True
    cases = [('R1', '低いものと考えられる', True, '222'),
             ('R1', 'どのように急いでいても', True, '194'),
             ('R1', '焦っていた可能性も考えられる', True, '220'),
             ('R1', '平成17年4月以降にずれ込んだ', True, '230'),
             ('S1', '後出しじゃんけん的ですね', True, '51'),
             ('S2', '認識できたとは認められない', True, '5'),
             ('Kk', 'いずれも無罪', True, None),
             ('J', '106名のお客様', True, None),
             ('M1', '省令', True, None),
             ('R1', '遅れを取り戻そうとわざと速度を出した', False, None)]   # 作った句＝無し
    for d, q, want, pg in cases:
        buf = []
        n = show_hits(d, loose(q), 30, 20, out=buf.append)
        got = n > 0
        pg_ok = (pg is None) or any(('p.%s（' % pg) in x or ('PDF p.%s:' % pg) in x for x in buf)
        good = got == want and (not want or pg_ok)
        print('%s %s「%s」→ %d件 %s' % ('OK' if good else '✗', d, q, n, buf[0][:90] if buf else ''))
        ok &= good
    # 頁の境（④で割れた片：p.12 の終わり「124ないし」→ 脚注と頁の数字 → p.13「125km/h」＝続けては当たらない。境の印が出るか）
    buf = []
    n = show_hits('R1', loose('125km/hに達した9時18分09秒'), 80, 3, out=buf.append)
    mark = any('⏎頁⏎' in x for x in buf)
    print('%s 頁の境の印 R1「125km/hに達した」→ %d件 %s' % ('OK' if n and mark else '✗', n, buf[0][:120] if buf else ''))
    ok &= bool(n and mark)
    # 名前を伏せる（国会の発言の頭）
    buf = []
    show_hits('Kk', loose('いずれも無罪'), 200, 1, out=buf.append)
    masked = bool(buf) and '君）' not in buf[0].replace('［名前］）', '')
    print('%s 国会の発言の頭を伏せる' % ('OK' if masked else '✗'))
    ok &= masked
    print('selftest', 'OK' if ok else '✗')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
