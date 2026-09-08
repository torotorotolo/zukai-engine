# -*- coding: utf-8 -*-
"""台本の「画面に出す言葉と数字」を、一次資料の原文に機械で当てる門番。

    python tools/check_facts.py <台本.md> <原文.txt>      # 決め所と数字の両方
    python tools/check_facts.py --selftest

なぜ要るか
----------
`check_script.py` は**形**（字数・行数・割合・尺）しか見ない。
「決め所の原文が本当に在るか」「画面に出す数字が原文に在るか」は**1件も見ていない**。
2026-08-04 に123便の決め所12件を手で当てたら **2件（16.7%）が誤り**だった。
手でやるかぎり必ず抜けるので、機械に落とす。
→ [[feedback-verify-every-onscreen-quote]] / [[feedback-rules-need-gates]]

何を見るか
----------
1. **決め所**：台本の `## 2.` の表から、4列目の `` ` `` で囲った原文と、
   5列目の頁（`p177` / `p38〜39`）を取り出し、**その頁に、その文字列が在るか**を見る。
   ⚠️ 報告書の1文は**頁をまたぐ**ことがある（キー橋 c404 で実際に踏んだ）。
   　 だから「全頁のどこかに在る」ではなく「**書いた頁に在る**」で判定し、
   　 見つからないときは**全頁を探して、実際に在る頁を出す**（直す先が分かるように）。
2. **数字**：`## 4. 台本` の字幕行から数字を全部拾い、原文に素の形で在るかを見る。
   3桁未満は時刻や個数で当たりすぎるので除く。
   ⚠️ **「無い」＝誤りではない。**こちらが換算した値（フィート→メートル等）は必ず「無い」側に出る。
   　 出たものが**全部、台本の §9-2 に申告してある**ことを人が確かめるための一覧である。

⚠️ **この道具が0件でも「照合した」ことにはならない。**
　 語句が在ることと、意味が同じことは別（逆接を切った引用は素通りする）。
　 → [[feedback-absence-of-a-word-is-not-absence]]

終了コード: 0=決め所が全件当たった / 1=当たらないものがある / 2=道具の異常
"""
import io
import os
import re
import sys

if hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PAGE_RE = re.compile(r'=== p(\d+) ===')
# 台本の §2 の表の行： | 5 | **c404** | **決め所**（10字） | `原文` ／ `原文` | p38〜39 |
ROW_RE = re.compile(r'^\|\s*\d+\s*\|\s*\*\*([a-z]{1,2}\d{2,3})\*\*\s*\|(.*)$')
QUOTE_RE = re.compile(r'`([^`]+)`')
# 頁の欄： p177 / p38〜39 / p38-39 / p26 注115
PAGE_COL_RE = re.compile(r'p\.?\s*(\d+)(?:\s*[〜~\-–]\s*(\d+))?')
CUT_RE = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*(?:🔧\s*)?／\s*([^／]*)／')
SUB_RE = re.compile(r'^>\s?(.*)$')
NUM_RE = re.compile(r'\d[\d,\.]*')
MIN_DIGITS = 3          # これ未満の数字は見ない（時刻・個数で当たりすぎる）

# 🔴 報告書は PDF の頁と印字の頁がずれる（キー橋は前付 xxii ぶんで +2）。
#    ⚠️ ずれは題材ごとに違う。**推定で置かない**＝台本に書いてある頁が印字の頁なら、
#    　 ここで足す数を題材ごとに渡す。既定 0（ずれの無い資料）。
DEFAULT_OFFSET = 0


def norm(s):
    """引用符とダッシュと空白の揺れを吸う（PDFの組版と手打ちの差）。"""
    for a, b in (('’', "'"), ('‘', "'"), ('“', '"'), ('”', '"'),
                 ('—', '-'), ('–', '-'), ('−', '-'), (' ', ' ')):
        s = s.replace(a, b)
    return re.sub(r'\s+', ' ', s).strip()


def load_pages(path):
    """`=== p<N> ===` で割られた原文を {頁: 正規化ずみ本文} にする。"""
    t = open(path, encoding='utf-8', errors='replace').read()
    parts = PAGE_RE.split(t)
    if len(parts) < 3:
        raise SystemExit('E 原文に `=== p<N> ===` の区切りがない: %s' % path)
    return {int(parts[i]): norm(parts[i + 1]) for i in range(1, len(parts), 2)}


def parse_quotes(text):
    """§2 の表から (カット, [原文…], [頁…]) を取り出す。§2 以外の表は読まない。"""
    out, on = [], False
    for line in text.split('\n'):
        if re.match(r'^## 2[.\s]', line):
            on = True
            continue
        if on and re.match(r'^## (?!2)', line):
            break
        if not on:
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        # ⚠️ 表の行は `|` で終わるので、素で split すると**最後の欄が空文字**になる。
        #    そのまま cols[-1] を頁の欄として読むと、全件「頁が読めない」になる
        #    （2026-09-08、この道具の selftest が最初に捕まえた穴）。
        cols = [c.strip() for c in m.group(2).split('|')]
        while cols and not cols[-1]:
            cols.pop()
        quotes, pages = [], []
        for c in cols:
            quotes += QUOTE_RE.findall(c)
        if cols:
            for a, b in PAGE_COL_RE.findall(cols[-1]):
                pages.append(int(a))
                if b:
                    pages.append(int(b))
        out.append((m.group(1), quotes, pages))
    return out


def parse_subs(text):
    """§4 台本 の字幕行だけを返す（見出し行と §5 以降は読まない）。"""
    lines, on, cur = [], False, False
    for raw in text.split('\n'):
        line = raw.rstrip()
        if line.startswith('## 4. 台本'):
            on = True
            continue
        if on and re.match(r'^## \d', line):
            break
        if not on:
            continue
        if CUT_RE.match(line):
            cur = True
            continue
        m = SUB_RE.match(line)
        if m and cur and m.group(1).strip():
            lines.append(re.sub(r'^★', '', m.group(1)).replace('**', '').strip())
    return lines


def forms(n):
    """3桁区切りの有無どちらでも当たるように、探す形を増やす。"""
    v = n.replace(',', '')
    out = {v}
    if v.isdigit() and len(v) > 3:
        out.add('{:,}'.format(int(v)))
    return out


def check_quotes(rows, pages, offset):
    """🔴 判定は「書いた頁に在るか」。全頁のどこかに在るだけでは通さない。"""
    ng = 0
    for cid, quotes, ps in rows:
        if not quotes:
            print('⚠️  %-6s 原文の欄が空（表の書き方を見る）' % cid)
            continue
        if not ps:
            print('🔴 %-6s 頁の欄が読めない' % cid)
            ng += 1
            continue
        want = {p + offset for p in ps}
        for q in quotes:
            nq = norm(q)
            here = sorted(p for p in want if nq in pages.get(p, ''))
            if here:
                print('OK  %-6s p%-8s %s' % (cid, '/'.join(str(p - offset) for p in here), q[:52]))
            else:
                where = sorted(p - offset for p in pages if nq in pages[p])
                ng += 1
                print('🔴 %-6s 書いた頁 %s に無い。実際に在る頁=%s : %s'
                      % (cid, sorted(p - offset for p in want), where or '（どこにも無い）', q[:52]))
    return ng


def check_numbers(subs, whole):
    """⚠️ ここは落とさない（換算値は必ず「無い」側に出る）。一覧を出すだけ。"""
    found = {}
    for l in subs:
        for m in NUM_RE.finditer(l):
            found.setdefault(m.group(0).rstrip('.'), 0)
            found[m.group(0).rstrip('.')] += 1
    miss = []
    for n in sorted(found):
        if len(n.replace(',', '').replace('.', '')) < MIN_DIGITS:
            continue
        if not any(re.search(r'(?<![\d,.])%s(?![\d])' % re.escape(f), whole) for f in forms(n)):
            miss.append(n)
    print('\n数字: %d種を拾い、%d桁以上を照合 → 原文に素の形で無いもの %d件'
          % (len(found), MIN_DIGITS, len(miss)))
    if miss:
        print('   ' + ' '.join(miss))
        print('   ⚠️ これは誤りの一覧ではない。**台本の §9-2 に全部申告してあるか**を人が見る。')
    return miss


SAMPLE_SRC = '''=== p10 ===
The quick brown fox jumps over the lazy dog. There were 9,086 feet between the abutments.
=== p11 ===
and the rudder could not be moved. About 50,000 tons were removed.
'''
SAMPLE_MD = '''## 2. 決め所

| # | カット | 決め所 | 原文 | 頁 |
|---|---|---|---|---|
| 1 | **c101** | **とんだ**（4字） | `The quick brown fox jumps` | p10 |
| 2 | **c102** | **動かせない**（5字） | `rudder could not be moved` | p11 |
| 3 | **c103** | **まちがい**（5字） | `the rudder could not be moved` | p10 |

## 4. 台本

**c101** ／ 図 p10（きつね）／ src p10
> 9086フィートあった。
> 換算すると2769メートルになる。

## 5. つぎ
> これは数えない9999。
'''


def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print('  %s %-26s 期待 %-10s 実際 %s' % ('OK ' if good else '🔴NG', name, want, got))

    import tempfile
    d = tempfile.mkdtemp()
    src = os.path.join(d, 's.txt')
    open(src, 'w', encoding='utf-8').write(SAMPLE_SRC)
    pages = load_pages(src)
    chk('頁を割れる', sorted(pages), [10, 11])
    rows = parse_quotes(SAMPLE_MD)
    chk('§2の表を読む', [c for c, _, _ in rows], ['c101', 'c102', 'c103'])
    chk('原文の欄を取る', rows[0][1], ['The quick brown fox jumps'])
    chk('頁の欄を取る', rows[1][2], [11])
    subs = parse_subs(SAMPLE_MD)
    chk('§4の字幕だけ拾う', len(subs), 2)
    chk('§5を読まない', any('9999' in s for s in subs), False)
    print('  ── 陽性対照（わざと外した1件だけが落ちること）')
    ng = check_quotes(rows, pages, 0)
    chk('落ちるのは1件だけ', ng, 1)
    whole = ' '.join(pages.values())
    miss = check_numbers(subs, whole)
    chk('原文に在る9086は出ない', '9086' in miss, False)
    chk('換算した2769は出る', '2769' in miss, True)
    print('selftest:', 'PASS' if ok else '🔴FAIL')
    return 0 if ok else 2


def main(argv):
    if '--selftest' in argv:
        return selftest()
    if len(argv) < 3:
        print(__doc__)
        return 2
    md, src = argv[1], argv[2]
    offset = DEFAULT_OFFSET
    for a in argv[3:]:
        if a.startswith('--offset='):
            offset = int(a.split('=', 1)[1])
    text = open(md, encoding='utf-8').read()
    pages = load_pages(src)
    print('原文 %d頁 / 頁のずれ +%d（台本の頁 ＋%d ＝ 原文の頁）' % (len(pages), offset, offset))
    rows = parse_quotes(text)
    print('決め所 %d件\n' % len(rows))
    ng = check_quotes(rows, pages, offset)
    check_numbers(parse_subs(text), ' '.join(pages.values()))
    print('\n決め所 %d件中 %d件が当たらない' % (sum(len(q) for _, q, _ in rows), ng))
    return 1 if ng else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
