# -*- coding: utf-8 -*-
"""17本目の台本を数える（④・④' 用。tools/ は触らない）。

    python ref/ep17/v1_build/m17.py ref/ep17/daihon_v1.md [--roles ref/ep17/v1_build/roles.tsv]
    python ref/ep17/v1_build/m17.py --selftest

数えるもの
  §1 カット・行・字（句読点こみ／句読点なし）・章ごと（kousei.md §3 の計画と並べる）
  §2 3通りの尺：① カット×9.0秒 ② 句読点なし字数÷380字/分（ルール §5a-28）③ 章ごとの ② の合計と計画の差
  §3 1行の字数（41字まで）・1カット1〜3行・決め所の字数（20字まで）・決め所の位置と最大の空白
  §4 写真・実写（check_script と同じ分け方＝`実写` と `図 pN`）・章ごと
  §5 文字だけの画面（Vault の count_text_screens.py と同じ分け方）・続く最長・3カット以上続く所
  §6 聞き役（割合・1分あたり・最初の1回・空き・役割・数字・キャラ語尾・まとめの次の「そう。」）
  §7 冒頭の秒（② の式を1カットずつ足す／決め所の余白 2.0秒を足した式）
  §8 使わない語（死亡・煽り語・波ダッシュ・ch 名）
句読点なし＝ 、。？！「」（）・ に加えて 『』・空白・★ を除く（ルール §5a-28 の数え方＋記号）。聞き役の印 `Q: ` は数えない。
"""
import os
import re
import sys
from collections import OrderedDict, Counter

CPM = 380.0
SEC_PER_CUT = 9.0
PUNCT = set('、。？！「」（）・『』 　★')
CUT_RE = re.compile(r'^\*\*(c[0-9a-z]\d{2})\*\*\s*(?:🔧\s*)?／\s*([^／]*)／\s*(.*)$')
Q_RE = re.compile(r'^Q:\s')
PLAN = OrderedDict([  # kousei.md §3（章・カット・句読点なし字・決め所・写真）
    ('c1', (17, 950, 1, 5)), ('c2', (20, 1140, 1, 7)), ('c3', (23, 1330, 1, 3)), ('c4', (20, 1140, 2, 6)),
    ('c5', (23, 1330, 2, 5)), ('c6', (20, 1140, 2, 4)), ('c7', (27, 1520, 1, 7)), ('c8', (20, 1140, 2, 8)),
    ('c9', (23, 1330, 2, 3)), ('ca', (20, 1140, 1, 3)), ('cb', (30, 1710, 2, 5))])
FIG = re.compile(r'図\s?[0-9０-９]|写真|地図|断面|配置|グラフ|航跡|映像|切出|画像|空撮|courtesy')
HYPE = ['即死', '絶命', '闇', '隠蔽', '悲劇', '戦慄', '驚愕', '恐怖の', '衝撃', '地獄']
NUM_IN_Q = re.compile(r'[0-9０-９一二三四五六七八九十百千万]')


def nopunct(s):
    return ''.join(ch for ch in s if ch not in PUNCT)


def parse(text):
    cuts, cur, on = OrderedDict(), None, False
    for raw in text.split('\n'):
        ln = raw.rstrip()
        if ln.startswith('## 4. 台本'):
            on = True
            continue
        if on and re.match(r'^## \d', ln):
            break
        if not on:
            continue
        m = CUT_RE.match(ln)
        if m:
            cur = m.group(1)
            cuts[cur] = {'pic': m.group(2).strip(), 'src': m.group(3).strip(), 'lines': []}
            continue
        if ln.startswith('### '):
            cur = None
            continue
        if cur and ln.startswith('>'):
            body = re.sub(r'^>\s?', '', ln)
            if body.strip():
                cuts[cur]['lines'].append(body)
    for c in cuts.values():
        c['q'] = [bool(Q_RE.match(l)) for l in c['lines']]
        c['bare'] = [Q_RE.sub('', l).replace('★', '') for l in c['lines']]
        c['star'] = [l.startswith('★') for l in c['lines']]
        c['np'] = sum(len(nopunct(b)) for b in c['bare'])
        c['wp'] = sum(len(b) for b in c['bare'])
        c['sec'] = c['np'] / CPM * 60
    return cuts


def pic_photo(pic):
    return ('実写' in pic) or bool(re.search(r'図\s*p\d', pic))


def pic_text(pic):
    if pic.startswith('quote'):
        return '決め所'
    if pic.startswith('panel'):
        return 'パネル'
    if re.match(r'図\s*p\d', pic) and not FIG.search(pic):
        return '文字の頁'
    return None


def role(q):
    t = q.strip()
    if t.endswith('？'):
        return '質問'
    if t.startswith('つまり'):
        return 'まとめ'
    return '反応'


def fmt(s):
    return '%d分%02d秒' % (int(s) // 60, int(round(s)) % 60 if int(round(s)) % 60 != 60 else 0)


def report(cuts, roles_out=None):
    ids = list(cuts)
    n = len(ids)
    out = []
    P = out.append
    allbare = [b for c in cuts.values() for b in c['bare']]
    np_total = sum(c['np'] for c in cuts.values())
    wp_total = sum(c['wp'] for c in cuts.values())
    nlines = sum(len(c['lines']) for c in cuts.values())
    nq = sum(any(c['star']) for c in cuts.values())
    P('## §1 数')
    P('カット %d / 行 %d（1カット %.2f行）/ 字 句読点こみ %d・句読点なし %d（比 %.3f）/ 決め所 %d'
      % (n, nlines, nlines / n, wp_total, np_total, np_total / wp_total, nq))
    # §2 尺
    d1 = n * SEC_PER_CUT
    d2 = np_total / CPM * 60
    P('## §2 尺')
    P('① カット×%.1f秒 = %s   ② 句読点なし÷%d字/分 = %s   開き %s'
      % (SEC_PER_CUT, fmt(d1), CPM, fmt(d2), fmt(abs(d1 - d2))))
    P('   ②の範囲（話速 ±7%%）＝ %s〜%s／27〜40分の内か: %s' % (fmt(d2 / 1.07), fmt(d2 / 0.93), 27 * 60 <= d2 <= 40 * 60))
    P('   計画 13,870字（±2%%＝13,593〜14,147）との差 %+d字' % (np_total - 13870))
    # 章ごと
    P('## §3 章ごと（計画＝kousei.md §3）')
    P('| 章 | カット（計画） | 行 | 句読点なし字（計画・差） | ③ 分（計画） | 決め所（計画） | 写真・実写（計画） | 聞き役 |')
    P('|---|---:|---:|---:|---:|---:|---:|---:|')
    tot = Counter()
    for ch, (pc, pch, pq, pp) in PLAN.items():
        cs = [cuts[i] for i in ids if i[:2] == ch]
        k = len(cs)
        ln = sum(len(c['lines']) for c in cs)
        chars = sum(c['np'] for c in cs)
        q = sum(any(c['star']) for c in cs)
        ph = sum(pic_photo(c['pic']) for c in cs)
        lq = sum(sum(c['q']) for c in cs)
        tot.update(dict(k=k, ln=ln, chars=chars, q=q, ph=ph, lq=lq))
        P('| `%s` | %d（%d） | %d | %d（%d・%+d） | %.2f（%.1f） | %d（%d） | %d（%d） | %d |'
          % (ch, k, pc, ln, chars, pch, chars - pch, chars / CPM, pch / CPM, q, pq, ph, pp, lq))
    P('| 計 | %d（243） | %d | %d（13,870・%+d） | %.2f（36.5） | %d（17） | %d（56） | %d |'
      % (tot['k'], tot['ln'], tot['chars'], tot['chars'] - 13870, tot['chars'] / CPM, tot['q'], tot['ph'], tot['lq']))
    # §3 形
    P('## §3b 形')
    long_lines = [(i, b, len(b)) for i in ids for b in cuts[i]['bare'] if len(b) > 41]
    P('1行41字超: %d %s' % (len(long_lines), long_lines[:10]))
    P('1行の字数: 中央値 %d・最長 %d' % (sorted(len(b) for b in allbare)[len(allbare) // 2], max(len(b) for b in allbare)))
    badn = [(i, len(cuts[i]['lines'])) for i in ids if not 1 <= len(cuts[i]['lines']) <= 3]
    P('1カット1〜3行の外: %s' % badn)
    stars = [(i, cuts[i]['bare'][k]) for i in ids for k, s in enumerate(cuts[i]['star']) if s]
    P('決め所の字数（20字まで）: ' + ' '.join('%s=%d' % (i, len(t)) for i, t in stars))
    over = [(i, t, len(t)) for i, t in stars if len(t) > 20]
    P('   20字超: %s' % over)
    notlast = [i for i in ids if any(cuts[i]['star']) and not cuts[i]['star'][-1]]
    P('   ★が最後の行でない: %s' % notlast)
    qi = [k for k, i in enumerate(ids) if any(cuts[i]['star'])]
    gaps = [qi[0]] + [qi[k] - qi[k - 1] for k in range(1, len(qi))] + [n - 1 - qi[-1]]
    P('決め所の位置: %s   最大の空白 %dカット（check_script の W は 26カット以上）' % (qi, max(gaps)))
    # §4 写真
    ph = [i for i in ids if pic_photo(cuts[i]['pic'])]
    P('## §4 写真・実写（check_script と同じ分け方）: %d / %d = %.1f%%（下限20%%）' % (len(ph), n, 100 * len(ph) / n))
    P('   うち実写 %d・報告書などの頁 %d' % (sum('実写' in cuts[i]['pic'] for i in ph), sum('実写' not in cuts[i]['pic'] for i in ph)))
    # §5 文字だけ
    kinds = {i: pic_text(cuts[i]['pic']) for i in ids}
    tx = [i for i in ids if kinds[i]]
    run = best = runs = 0
    span = ''
    for k, i in enumerate(ids):
        if kinds[i]:
            run += 1
            if run > best:
                best, span = run, ids[k - run + 1] + '〜' + i
        else:
            runs += run >= 3
            run = 0
    runs += run >= 3
    c_kind = Counter(kinds[i] for i in tx)
    P('## §5 文字だけの画面: %d / %d = %.1f%%（2割まで）・続く最長 %d（%s）・3カット以上続く所 %d'
      % (len(tx), n, 100 * len(tx) / n, best, span, runs))
    P('   内訳 %s' % dict(c_kind))
    P('   ' + ' '.join('%s:%s' % (i, kinds[i]) for i in tx))
    # §6 聞き役
    t = 0.0
    qtimes, rows = [], []
    ends = []
    for i in ids:
        c = cuts[i]
        for k, b in enumerate(c['bare']):
            if c['q'][k]:
                qtimes.append((t, i))
                rows.append((i, role(b), b.strip()))
            t += len(nopunct(b)) / CPM * 60
        ends.append((i, t))
    total = t
    nqline = len(rows)
    P('## §6 聞き役')
    P('聞き役の行 %d / %d = %.1f%%（10〜15%%）・1分あたり %.2f回（1.5〜2）・字 %d'
      % (nqline, nlines, 100 * nqline / nlines, nqline / (total / 60),
         sum(len(nopunct(r[2])) for r in rows)))
    if qtimes:
        gl = [qtimes[0][0]] + [qtimes[k][0] - qtimes[k - 1][0] for k in range(1, len(qtimes))] + [total - qtimes[-1][0]]
        top = sorted([(round(qtimes[k][0] - qtimes[k - 1][0]), qtimes[k - 1][1], qtimes[k][1]) for k in range(1, len(qtimes))], reverse=True)[:5]
        P('最初の1回 %.1f秒・最長の空き %.0f秒（90秒まで）・90秒超 %d・長い空きの上位 %s'
          % (qtimes[0][0], max(gl[1:-1] or [0]), sum(g > 90 for g in gl[1:-1]), top))
    rc = Counter(r[1] for r in rows)
    P('役割 %s（質問 %.0f%%・まとめ %.0f%%・反応 %.0f%%）'
      % (dict(rc), 100 * rc['質問'] / nqline, 100 * rc['まとめ'] / nqline, 100 * rc['反応'] / nqline))
    P('数字を含む聞き役の行: %s' % [r for r in rows if NUM_IN_Q.search(r[2])])
    P('キャラ語尾: %s' % [r for r in rows if re.search(r'(ぜ|わ|かしら)[。！？]?$', r[2])])
    bad_sou = []
    for k, i in enumerate(ids):
        c = cuts[i]
        for j, b in enumerate(c['bare']):
            if c['q'][j] and role(b) == 'まとめ':
                nxt = c['bare'][j + 1] if j + 1 < len(c['bare']) else (cuts[ids[k + 1]]['bare'][0] if k + 1 < n else '')
                if not nxt.startswith('そう。'):
                    bad_sou.append((i, nxt[:12]))
    P('まとめの次の語りが「そう。」で始まらない: %s' % bad_sou)
    if roles_out:
        with open(roles_out, 'w', encoding='utf-8') as f:
            f.write('cid\t役割\t文\n')
            for r in rows:
                f.write('%s\t%s\t%s\n' % r)
        P('roles.tsv を書いた: %s（%d行）' % (roles_out, len(rows)))
    # §7 冒頭
    P('## §7 冒頭の秒（② の式・カットの終わり）')
    t1 = t2 = 0.0
    s = []
    for i in ids[:8]:
        c = cuts[i]
        t1 += c['np'] / CPM * 60
        t2 += c['np'] / CPM * 60 + (2.0 if any(c['star']) else 0.0)
        s.append('%s=%.1f/%.1fs' % (i, t1, t2))
    P('   ' + ' '.join(s) + '   （左＝字数÷380・右＝決め所の余白2.0秒を足す）')
    # §8 語
    P('## §8 使わない語')
    body = '\n'.join(allbare)
    P('死亡: %d・煽り語: %s・波ダッシュ〜: %d・ch名: %d'
      % (body.count('死亡'), [w for w in HYPE if w in body], body.count('〜'),
         sum(body.count(w) for w in ('仕事帰り', '事故調査ノート', 'shigotogaeri'))))
    return '\n'.join(out)


SAMPLE = '''## 4. 台本
### 第1章　a（2カット）
**c101** ／ 実写 写真1 ／ S1
> 一二三、四五。
> Q: 何？
**c102** ／ quote（決め所） ／ S1
> そう。あいう
> ★かきくけこ
### 第2章　b（1カット）
**c201** ／ panel x ／ —
> Q: つまり、そう。
## 5. x
'''


def selftest():
    cs = parse(SAMPLE)
    ok = True
    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(('✓' if good else 'E'), name, got, want)
    chk('カット数', len(cs), 3)
    chk('c101 句読点なし（一二三四五＋何）', cs['c101']['np'], 6)
    chk('c102 ★は最後', cs['c102']['star'], [False, True])
    chk('c102 句読点なし（そうあいう＋かきくけこ）', cs['c102']['np'], 10)
    chk('聞き役の印を数えない', cs['c201']['np'], 5)
    chk('写真', pic_photo(cs['c101']['pic']), True)
    chk('文字だけ（quote）', pic_text(cs['c102']['pic']), '決め所')
    chk('文字だけ（図 p の文字の頁）', pic_text('図 p95（S1 原因の頁）'), '文字の頁')
    chk('図の頁は文字だけでない', pic_text('図 p135（S1 付図29）'), None)
    chk('役割', [role('何？'), role('つまり、そう。'), role('へえ。')], ['質問', 'まとめ', '反応'])
    return 0 if ok else 1


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        sys.exit(selftest())
    path = sys.argv[1]
    ro = sys.argv[sys.argv.index('--roles') + 1] if '--roles' in sys.argv else None
    print(report(parse(open(path, encoding='utf-8').read()), ro))
