# -*- coding: utf-8 -*-
"""33本目④'：一次資料の文字（git の外 src/inquiry_txt/ と src/web/）を、段落の札か語で引く（読むだけ・係と親が使う）。

  python -P ref/ep33/v2_build/src33.py P1V4 28.6            # 段落 28.6 を頭から（次の段落の札まで・最大 3,000字）
  python -P ref/ep33/v2_build/src33.py P1V4 28.81 --n 6000  # 長い段落・脚注を見るとき（頁の終わりの脚注も窓に入る）
  python -P ref/ep33/v2_build/src33.py P1V4 --kw "best part of an hour" [--w 400] [--max 5]
  python -P ref/ep33/v2_build/src33.py 警1 --kw "54 individuals"      # web の写し（記号は台本の出典の欄と同じ）
  python -P ref/ep33/v2_build/src33.py ALL --kw "stay put" --max 3   # 報告の12冊すべて（巻ごとに数と最初の窓）
  python -P ref/ep33/v2_build/src33.py P1V2 --fig 10.14             # 図の題の行（"Figure 10.14" の窓）

・語の照らし方＝NFKC・小文字・曲がった引用符を直したうえで、空白とハイフンの違いを無視して探す（quotes33.py と同じ考え）
・窓の頭に「巻 p頁 ¶直前の段落の札」を付ける（段落の札＝「28.6」「2. 11」の形で、次の字が大文字か引用符のもの）
・名前は伏せない（原文のまま出る）＝🔴 返事やファイルに人の名前を写さない（〈名〉と書く）
・語も段落も無ければ何も出さずに終了コード 2（全文を出さない）
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
       '消': ['inquiry_txt/FDMA_20260330yo120.txt'],
       '換': ['web/boe/*.html']}
LABEL = re.compile(r'(?<![\d.£$€,])([1-9]\d{0,2})\.\s?(\d{1,3})(?![\d.,%])\s+(?=[A-Z‘“"\'(\[])')  # 頭が0の「01.50」は時刻＝札にしない


def fold(s):
    s = unicodedata.normalize('NFKC', s or '').lower()
    return s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')


def squash(s):
    """照らす用：空白・ハイフン・ダッシュを消し、元の位置への対応表も返す。"""
    out, pos = [], []
    for i, ch in enumerate(fold(s)):
        if ch.isspace() or ch in '-‐‑‒–—―':
            continue
        out.append(ch)
        pos.append(i)
    return ''.join(out), pos


def vol_pages(v):
    p = os.path.join(SRC, 'inquiry_txt', v + '.txt')
    if not os.path.exists(p):
        return None
    t = open(p, encoding='utf-8').read()
    parts = re.split(r'=====\[p(\d+)\]=====', t)
    return [(int(parts[i]), parts[i + 1]) for i in range(1, len(parts), 2)]


def joined(v):
    """巻の全文を1本に（頁の頭の位置の表つき）。"""
    pages = vol_pages(v)
    if pages is None:
        return None, None
    buf, starts = [], []
    n = 0
    for pg, tx in pages:
        starts.append((n, pg))
        buf.append(tx)
        n += len(tx) + 1
    return '\n'.join(buf), starts


def page_at(starts, i):
    pg = starts[0][1]
    for s, p in starts:
        if s <= i:
            pg = p
        else:
            break
    return pg


def last_label(text, i):
    best = None
    for m in LABEL.finditer(text, max(0, i - 6000), i + 1):
        best = '%s.%s' % (m.group(1), m.group(2))
    return best or '?'


def web_docs(code):
    out = []
    for pat in WEB[code]:
        for f in sorted(glob.glob(os.path.join(SRC, pat))):
            out.append((os.path.relpath(f, SRC).replace('\\', '/'), open(f, encoding='utf-8', errors='replace').read()))
    return out


def kwic(text, kw, w, mx, head):
    sq, pos = squash(text)
    k, _ = squash(kw)
    if not k:
        return 0
    hits, start = [], 0
    while True:
        j = sq.find(k, start)
        if j < 0:
            break
        hits.append(j)
        start = j + 1
    for j in hits[:mx]:
        a, b = pos[j], pos[min(j + len(k) - 1, len(pos) - 1)]
        print('—— %s' % head(a))
        print(text[max(0, a - w):a].replace('\n', ' ') + '【' + text[a:b + 1].replace('\n', ' ') + '】' + text[b + 1:b + 1 + w].replace('\n', ' '))
    return len(hits)


def main(argv):
    args = argv[1:]
    if not args:
        print(__doc__)
        return 2
    doc = args[0]
    kw = args[args.index('--kw') + 1] if '--kw' in args else None
    fig = args[args.index('--fig') + 1] if '--fig' in args else None
    w = int(args[args.index('--w') + 1]) if '--w' in args else 350
    mx = int(args[args.index('--max') + 1]) if '--max' in args else 5
    nmax = int(args[args.index('--n') + 1]) if '--n' in args else 3000
    para = args[1] if len(args) > 1 and re.fullmatch(r'\d{1,3}\.\d{1,3}', args[1]) else None
    if fig:
        kw = 'Figure %s' % fig
    if not kw and not para:
        print('語（--kw）か段落（例 28.6）か図（--fig）が要る＝何も出さない')
        return 2
    vols = VOLS if doc == 'ALL' else ([doc] if doc in VOLS else [])
    if vols:
        total = 0
        for v in vols:
            text, starts = joined(v)
            if text is None:
                print('資料が無い:', v)
                continue
            if para:
                a, b = para.split('.')
                rx = re.compile(r'(?<![\d.£$€,])%s\.\s?%s(?![\d.,%%])\s+(?=[A-Z‘“"\'(\[])' % (a, b))
                nb = '%s.%d' % (a, int(b) + 1)
                rxn = re.compile(r'(?<![\d.£$€,])%s\.\s?%s(?![\d.,%%])\s+(?=[A-Z‘“"\'(\[])' % tuple(nb.split('.')))
                ms = list(rx.finditer(text))
                if not ms:
                    print('段落の札が見つからない: %s ¶%s（札が文字の層に無い巻がある＝--kw で語から引く）' % (v, para))
                    return 2
                for m in ms[:3]:
                    s = m.start()
                    mn = rxn.search(text, m.end())
                    e = min(mn.start() if mn else s + nmax, s + nmax)
                    print('—— %s p%s ¶%s（候補 %d のうち）' % (v, page_at(starts, s), para, len(ms)))
                    print(text[s:e].replace('\n', ' '))
                total += len(ms)
            else:
                n = kwic(text, kw, w, mx if doc != 'ALL' else min(mx, 1),
                         lambda a, v=v, text=text, starts=starts: '%s p%s ¶%s' % (v, page_at(starts, a), last_label(text, a)))
                if doc == 'ALL' and n:
                    print('   %s：%d件' % (v, n))
                total += n
        if not total:
            print('当たり 0')
            return 2
        print('当たり %d' % total)
        return 0
    if doc in WEB:
        if not kw:
            print('web の写しは --kw で引く')
            return 2
        total = 0
        for name, text in web_docs(doc):
            total += kwic(text, kw, w, mx, lambda a, name=name: '%s %s' % (doc, name))
        print('当たり %d' % total)
        return 0 if total else 2
    print('記号が分からない:', doc, '（巻＝%s・ALL・web＝%s）' % (' '.join(VOLS), ' '.join(WEB)))
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
