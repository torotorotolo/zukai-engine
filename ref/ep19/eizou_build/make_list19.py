# -*- coding: utf-8 -*-
"""19本目 映像方針（チャット4）：台本 第2版の237カット × 当て方の下書き → 場面ごとの映像の一覧・数・取得の一覧。

  python ref/ep19/eizou_build/make_list19.py              # 書いて数える（E があれば exit 1）
  python ref/ep19/eizou_build/make_list19.py --selftest   # 門番の見本（E を出すべき並び・出さない並び）

入力：ref/ep19/daihon_v2.md（§4 の237カット）・eizou_build/assign19.tsv（当て方の下書き＝無いカットは台本の画の欄のまま）・
      eizou_build/sources19.tsv（素材の記号 → 出どころ・大きさ・権利）
出力：ref/ep19/eizou_list19.md（人が読む一覧＝生成物・手で直さない）・eizou_build/list19.tsv（⑤b-1 の入口）・
      eizou_build/fetch19.tsv（取得の一覧＝使う素材だけ）

数え方（ルール統合版）：
  写真・実写＝カットの種類が「実写」（この事故の写真・記録映像）＝20%以上（§2-1）。フリー素材「イメージ」は別（§2-5c）
  差し込み（head<k>＝頭の k 行・tail<k>＝k 行目から終わり）は秒で別に数える＝カットの種類は変えない（check_text_screens と同じ）
  文字だけ＝パネル・決め所・文字の頁＝2割まで・3連続で E（§5b-79）
  同じ素材の2回＝写真は記号が同じなら E・映像は区間が重なれば E（区間が「⑤b-1」・備考に「別の秒」＝⑤b-1 で選ぶ印＝E にしない）
  伸ばし＝区間の秒より使う秒が長い＝2倍を超えたら ⚠️（⑤b-1 で長い区間を探す）
"""
import collections
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EP = HERE.parent
DAIHON = EP / 'daihon_v2.md'
ASSIGN = HERE / 'assign19.tsv'
SOURCES = HERE / 'sources19.tsv'
OUT_MD = EP / 'eizou_list19.md'
OUT_TSV = HERE / 'list19.tsv'
OUT_FETCH = HERE / 'fetch19.tsv'

PUNCT = set('、。？！「」（）・')
CPM = 365.0
CUT_RE = re.compile(r'^\*\*(c[0-9a-c][0-9]{2})\*\*(\s*🔧)?\s*／\s*(.*)$')
CH_RE = re.compile(r'^### (つかみ|第\d+章|終章)')
TEXT = ('panel', 'quote', '文字の頁')
NB = r'(?<![A-Za-z0-9_])'
CODE_RE = re.compile(NB + r'(TFV|TLS|TL(?![A-Za-z])|PC(?![A-Za-z])|GIF|W1|M[15](?![0-9])|B[1-8](?![0-9])|N#\d+|F:\d+|'
                     r'C\d{1,2}(?![0-9])|D(?:\d{1,2})?(?![A-Za-z0-9])|P[1-3](?![0-9])|A01|tf_p\d{3}_[a-z0-9]+|S#\d+)')
CLASSES = [(re.compile(r'^(B[1-8]|TLS|TL|W1|M[15])$'), 'film'),
           (re.compile(r'^(N#\d+|F:\d+|C\d{1,2}|D\d{0,2}|P[1-3])$'), 'photo'),
           (re.compile(r'^(TFV|GIF|PC)$'), 'anim'),
           (re.compile(r'^(tf_p\w+|A01|TF頁|資料の頁)$'), 'page'),
           (re.compile(r'^S#\d+$'), 'stock')]
KIND_JA = {'実写': '実写', '頁': '頁', '文字の頁': '文字の頁', '図動': 'NIST の動く図', 'フリー': 'フリー素材', '再現': '再現イラスト',
           '図': '図', 'panel': 'パネル', 'quote': '決め所'}
CLASS_JA = {'film': '映像', 'photo': '写真', 'anim': 'NIST の動く図', 'page': '頁', 'stock': 'フリー素材', None: '—'}


def nopunct(s):
    return sum(1 for ch in s if ch not in PUNCT)


def clean(line):
    s = line[1:].strip() if line.startswith('>') else line
    s = re.sub(r'^Q:\s*', '', s)
    return s.replace('★', '').replace('**', '').strip()


def kind_of(pic):
    p = pic.strip()
    if p.startswith('実写'):
        return '実写'
    if p.startswith('フリー素材'):
        return 'フリー'
    if p.startswith('図 再現イラスト'):
        return '再現'
    if re.match(r'^図 p\d', p) or p.startswith('図 TF') or p.startswith('図 頁'):
        return '文字の頁' if '文字の頁' in p else '頁'
    if p.startswith('図'):
        return '図'
    for k in ('panel', 'quote'):
        if p.startswith(k):
            return k
    return '?'


def parse_daihon(path):
    body = Path(path).read_text(encoding='utf-8').split('## 4. 台本', 1)[1].split('## 5. 使わなかったもの', 1)[0]
    cuts, ch, cur = [], None, None
    for ln in body.splitlines():
        if CH_RE.match(ln):
            ch = ln[4:].split('（')[0].strip()
            continue
        m = CUT_RE.match(ln)
        if m:
            parts = [x.strip() for x in m.group(3).split(' ／ ')]
            cur = dict(cid=m.group(1), ch=ch, pic=parts[0], src=' ／ '.join(parts[1:]), lines=[])
            cuts.append(cur)
        elif cur is not None and ln.startswith('>'):
            cur['lines'].append(clean(ln))
    t = 0.0
    for c in cuts:
        c['start'] = t
        c['line_secs'] = [nopunct(s) / CPM * 60 for s in c['lines']]
        c['dur'] = sum(c['line_secs'])
        t += c['dur']
        c['kind'] = kind_of(c['pic'])
    return cuts


def read_tsv(path):
    rows = []
    head = None
    for ln in Path(path).read_text(encoding='utf-8').splitlines():
        if not ln.strip() or ln.startswith('#'):
            continue
        f = ln.split('\t')
        if head is None:
            head = f
            continue
        rows.append(dict(zip(head, f + [''] * (len(head) - len(f)))))
    return rows


def class_of(code):
    for rx, k in CLASSES:
        if code and rx.match(code):
            return k
    return None


def code_of(text):
    t = text.split('→')[-1] if '→' in text else text
    m = CODE_RE.search(t)
    if not m:
        return None, ''
    rest = t[m.end():]
    mm = re.match(r'@([^（(\s]+)', rest)
    return m.group(1), (mm.group(1) if mm else '')


def num_range(rng):
    m = re.match(r'^(\d+(?:\.\d+)?)[–〜\-](\d+(?:\.\d+)?)$', rng or '')
    return (float(m.group(1)), float(m.group(2))) if m else None


def parse_ins(s):
    s = (s or '').strip()
    if not s or s == '—':
        return None
    m = re.match(r'^(head|tail)(\d+):(.*)$', s)
    if not m:
        return dict(pos='?', k=0, text=s, code=None, rng='')
    code, rng = code_of(m.group(3))
    return dict(pos=m.group(1), k=int(m.group(2)), text=m.group(3), code=code, rng=rng)


def build(cuts, assign):
    """カットごとに台本と下書きを合わせる。返す行＝一覧の1行（秒・種類・素材・差し込み・副題・権利・札）"""
    a = {r['cid']: r for r in assign}
    rows = []
    for c in cuts:
        r = a.get(c['cid'])
        kind = r['kind'] if r else c['kind']
        main = r['main'] if r else c['pic']
        ins = parse_ins(r['ins']) if r else None
        ins_secs = 0.0
        if ins and ins['pos'] in ('head', 'tail') and 1 <= ins['k'] <= len(c['line_secs']):
            ls = c['line_secs']
            ins_secs = sum(ls[:ins['k']]) if ins['pos'] == 'head' else sum(ls[ins['k'] - 1:])
        if kind in ('実写', '頁', 'フリー', '図動'):
            code, rng = code_of(main)
            if code is None and kind == '頁':
                code = 'TF頁' if 'TF のスライド' in main else '資料の頁'
        elif kind == '文字の頁':
            code, rng = '資料の頁', ''
        else:
            code, rng = None, ''
        note = r['note'] if r else ''
        label = []
        if kind == 'フリー':
            label.append('イメージ')
        if ins and class_of(ins['code']) == 'stock':
            label.append('イメージ（差し込み）')
        if '推定' in main + note:
            label.append('推定')
        rows.append(dict(cid=c['cid'], ch=c['ch'], start=c['start'], dur=c['dur'], lines=len(c['line_secs']),
                         kind=kind, script_kind=c['kind'], main=main, code=code, rng=rng, cls=class_of(code),
                         main_secs=c['dur'] - ins_secs, ins=ins, ins_secs=ins_secs,
                         sub=(r['sub'] if r else ''), rights=(r['rights'] if r else ('自作' if kind not in ('頁', '文字の頁') else '')),
                         label='・'.join(label), note=note, assigned=bool(r), narr=''.join(c['lines'])[:24]))
    missing = sorted(set(a) - {c['cid'] for c in cuts})
    return rows, missing


def uses_of(rows):
    out = []
    for r in rows:
        if r['code']:
            out.append(dict(cid=r['cid'], role='main', code=r['code'], rng=r['rng'], secs=r['main_secs'],
                            text=r['main'] + ' ' + r['note']))
        if r['ins'] and r['ins']['code']:
            out.append(dict(cid=r['cid'], role=r['ins']['pos'], code=r['ins']['code'], rng=r['ins']['rng'],
                            secs=r['ins_secs'], text=r['ins']['text'] + ' ' + r['note']))
    return out


def judge(rows, sources, missing=()):
    """数と門番。返す＝(stats, probs)。probs＝[(印, 文)]・印 E＝止める／⚠️＝⑤b-1 で見る／・＝⑤b-1 で選ぶ"""
    probs = []
    n = len(rows)
    T = sum(r['dur'] for r in rows)
    st = collections.OrderedDict()
    st['cuts'] = n
    st['secs'] = T
    st['kinds'] = collections.Counter(r['kind'] for r in rows)
    st['script_kinds'] = collections.Counter(r['script_kind'] for r in rows)
    real = [r for r in rows if r['kind'] == '実写']
    st['real'] = (len(real), len(real) / n if n else 0, sum(r['dur'] for r in real), sum(r['dur'] for r in real) / T if T else 0)
    st['real_by_class'] = collections.Counter(r['cls'] for r in real)
    if n and len(real) / n < 0.20:
        probs.append(('E', '写真・実写 %d/%d＝%.1f%%＜20%%（§2-1）' % (len(real), n, 100 * len(real) / n)))
    film_main = [r for r in rows if r['cls'] == 'film']
    film_ins = [r for r in rows if r['ins'] and class_of(r['ins']['code']) == 'film']
    st['film'] = (len({r['cid'] for r in film_main + film_ins}),
                  sum(r['main_secs'] for r in film_main) + sum(r['ins_secs'] for r in film_ins))
    st['film_codes'] = sorted({r['code'] for r in film_main} | {r['ins']['code'] for r in film_ins})
    anim_main = [r for r in rows if r['kind'] == '図動']
    anim_ins = [r for r in rows if r['ins'] and class_of(r['ins']['code']) == 'anim']
    st['anim'] = (len(anim_main), sum(r['main_secs'] for r in anim_main), len(anim_ins), sum(r['ins_secs'] for r in anim_ins))
    stock_main = [r for r in rows if r['kind'] == 'フリー']
    stock_ins = [r for r in rows if r['ins'] and class_of(r['ins']['code']) == 'stock']
    st['stock'] = (len(stock_main), sum(r['main_secs'] for r in stock_main), len(stock_ins), sum(r['ins_secs'] for r in stock_ins))
    real_ins = [r for r in rows if r['ins'] and class_of(r['ins']['code']) in ('film', 'photo')]
    st['real_ins'] = (len(real_ins), sum(r['ins_secs'] for r in real_ins))
    text = [r for r in rows if r['kind'] in TEXT]
    run, best, best_at = 0, 0, ''
    for r in rows:
        run = run + 1 if r['kind'] in TEXT else 0
        if run > best:
            best, best_at = run, r['cid']
        if run == 3:
            probs.append(('E', '文字だけが3連続（%s まで・§5b-79）' % r['cid']))
    st['text'] = (len(text), len(text) / n if n else 0, sum(r['dur'] for r in text), best, best_at)
    if n and len(text) / n > 0.20:
        probs.append(('E', '文字だけ %d/%d＝%.1f%%＞20%%' % (len(text), n, 100 * len(text) / n)))
    for c in missing:
        probs.append(('E', '下書きに台本に無いカット %s' % c))
    for r in rows:
        if r['kind'] in ('実写', 'フリー', '図動') and not r['code']:
            probs.append(('E', '%s：素材の記号が読めない（%s）' % (r['cid'], r['main'][:30])))
        if r['ins'] and (r['ins']['pos'] == '?' or not (1 <= r['ins']['k'] <= r['lines'])):
            probs.append(('E', '%s：差し込みの行 %s%s がカットの行数 %d の外' % (r['cid'], r['ins']['pos'], r['ins']['k'], r['lines'])))
        if r['ins'] and not r['ins']['code']:
            probs.append(('E', '%s：差し込みの素材の記号が読めない（%s）' % (r['cid'], r['ins']['text'][:30])))
    us = uses_of(rows)
    for u in us:
        if u['code'] not in sources:
            probs.append(('E', '%s：素材 %s が sources19.tsv に無い' % (u['cid'], u['code'])))
    by = collections.defaultdict(list)
    for u in us:
        by[u['code']].append(u)
    pick = []
    for code, lst in by.items():
        k = class_of(code)
        if len(lst) < 2 or k in ('page', None):
            continue
        cids = ' '.join('%s(%s)' % (u['cid'], u['rng'] or '—') for u in lst)
        if k == 'photo' and code != 'D':
            probs.append(('E', '同じ写真 %s を2回以上：%s' % (code, cids)))
        elif code == 'D':
            pick.append(('・', 'D（DHS 15点）を %d カット：%s＝⑤b-1 で別のコマ' % (len(lst), cids)))
        elif k == 'stock':
            probs.append(('⚠️', '同じフリー素材 %s を2回以上：%s' % (code, cids)))
        else:
            for i in range(len(lst)):
                for j in range(i + 1, len(lst)):
                    p, q = lst[i], lst[j]
                    a, b = num_range(p['rng']), num_range(q['rng'])
                    if a and b and a[0] < b[1] and b[0] < a[1]:
                        if '別の秒' in p['text'] + q['text']:
                            pick.append(('・', '%s %s と %s が同じ区間 %s/%s＝備考どおり⑤b-1 で別の秒' % (code, p['cid'], q['cid'], p['rng'], q['rng'])))
                        else:
                            probs.append(('E', '%s：%s と %s の区間が重なる（%s／%s）' % (code, p['cid'], q['cid'], p['rng'], q['rng'])))
            loose = [u for u in lst if not num_range(u['rng'])]
            if loose:
                pick.append(('・', '%s を %d カット（うち区間が決まっていない %d：%s）＝⑤b-1 の走査で別の秒' %
                             (code, len(lst), len(loose), ' '.join(u['cid'] for u in loose))))
    for u in us:
        rg = num_range(u['rng'])
        if rg and class_of(u['code']) in ('film', 'anim'):
            avail = rg[1] - rg[0]
            f = u['secs'] / avail if avail > 0 else 99
            if f > 2.0 and '静止画で受ける' not in u['text']:
                probs.append(('⚠️', '%s %s@%s：%.1f秒に %.1f秒を伸ばす（×%.1f）＝⑤b-1 で長い区間を探す' % (u['cid'], u['code'], u['rng'], u['secs'], avail, f)))
            elif f > 1.0:
                pick.append(('・', '%s %s@%s：%.1f秒に %.1f秒（×%.2f＝%s）' % (u['cid'], u['code'], u['rng'], u['secs'], avail, f,
                                                                       '伸ばしすぎ＝備考どおり長い区間か静止画で受ける' if f > 2.0 else 'ゆっくり')))
    perch = collections.OrderedDict()
    for r in rows:
        d = perch.setdefault(r['ch'], collections.Counter())
        d['cuts'] += 1
        d['secs'] += r['dur']
        d[r['kind']] += 1
        if r['ins'] and class_of(r['ins']['code']) in ('film', 'photo'):
            d['ins_real'] += 1
    for ch, d in perch.items():
        if d['実写'] == 0:
            probs.append(('⚠️', '%s：実写が0カット' % ch))
    st['perch'] = perch
    st['pick'] = pick
    return st, probs


def mmss(t):
    return '%d:%04.1f' % (int(t) // 60, t - 60 * (int(t) // 60))


def md_cell(s):
    return (s or '').replace('|', '｜').replace('\n', ' ')


def opening(rows):
    seg = []
    for r in rows:
        if r['cid'] > 'c105' or not r['cid'].startswith('c1'):
            break
        t0, t1 = r['start'], r['start'] + r['dur']
        ins = r['ins']
        if ins and ins['pos'] == 'tail':
            seg.append((r['cid'], t0, t1 - r['ins_secs'], r['kind'], r['cls'], r['main']))
            seg.append((r['cid'] + ' 尻', t1 - r['ins_secs'], t1, '差し込み', class_of(ins['code']), ins['text']))
        elif ins and ins['pos'] == 'head':
            seg.append((r['cid'] + ' 頭', t0, t0 + r['ins_secs'], '差し込み', class_of(ins['code']), ins['text']))
            seg.append((r['cid'], t0 + r['ins_secs'], t1, r['kind'], r['cls'], r['main']))
        else:
            seg.append((r['cid'], t0, t1, r['kind'], r['cls'], r['main']))
    return seg


def write_outputs(rows, st, probs, sources):
    us = uses_of(rows)
    used = collections.OrderedDict()
    for u in us:
        used.setdefault(u['code'], []).append(u['cid'])
    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        f.write('cid\tch\tstart\tdur\tkind\tcode\trng\tclass\tmain\tins_pos\tins_k\tins_code\tins_rng\tins_secs\tins_text\tsub\trights\tlabel\tnote\tnarr\n')
        for r in rows:
            i = r['ins'] or {}
            f.write('\t'.join(str(x) for x in [r['cid'], r['ch'], '%.1f' % r['start'], '%.1f' % r['dur'], r['kind'], r['code'] or '', r['rng'],
                                               r['cls'] or '', r['main'], i.get('pos', ''), i.get('k', ''), i.get('code') or '', i.get('rng', ''),
                                               '%.1f' % r['ins_secs'] if i else '', i.get('text', ''), r['sub'], r['rights'], r['label'],
                                               r['note'], r['narr']]) + '\n')
    alts = [(c, s) for c, s in sources.items() if c not in used and s.get('note', '').startswith('【代わり】')]
    fetch = [(c, ' '.join(cids), sources.get(c, {})) for c, cids in used.items()] + [(c, '（代わり）', s) for c, s in alts]
    with open(OUT_FETCH, 'w', encoding='utf-8', newline='\n') as f:
        f.write('code\tclass\tused_in\tfile\turl\tdims\tdur\tmb\trights\tcredit\tnote\n')
        for code, used_in, s in fetch:
            f.write('\t'.join([code, s.get('class', ''), used_in, s.get('file', ''), s.get('url', ''), s.get('dims', ''), s.get('dur', ''),
                               s.get('mb', ''), s.get('rights', ''), s.get('credit', ''), s.get('note', '')]) + '\n')
    n, T = st['cuts'], st['secs']
    L = ['---', 'title: 19本目 場面ごとの映像の一覧（生成物）', 'created: 2026-10-06', 'tags: [project/jiko-kensho, ep19]', '---', '',
         '# 19本目 場面ごとの映像の一覧（237カット・映像方針 チャット4）', '',
         '> **生成物＝手で直さない**。作り方＝`python ref/ep19/eizou_build/make_list19.py`（入力＝台本 第2版 `daihon_v2.md` §4・'
         '当て方の下書き `eizou_build/assign19.tsv`・素材の出どころ `eizou_build/sources19.tsv`）。直すのは assign19.tsv。'
         '秒＝句読点なし÷365字/分（行の間は入れない）。素材の記号の意味＝`eizou19_memo.md` §2。', '',
         '> ✅ **決め①〜⑨＝推奨どおり**（2026-10-06 カズヤくん）＝Vault `Projects/事故検証-19本目-映像方針-20261006.md`。素材の取得（決め⑧）は ⑤b-1 で。', '',
         '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|']
    rn, rp, rs, rsp = st['real']
    L.append('| 写真・実写（この事故） | **%d カット＝%.1f%%**（秒 %.0f＝%.1f%%）＝映像 %d・写真 %d・TF のコマ %d | 20%%以上 ✅ |' %
             (rn, 100 * rp, rs, 100 * rsp, st['real_by_class']['film'], st['real_by_class']['photo'], st['real_by_class']['anim']))
    L.append('| 本物の差し込み（頭・尻） | %d カット・%.1f秒（カットの種類は図・再現のまま＝20%%には数えない） | — |' % st['real_ins'])
    L.append('| この事故の動く映像（【映像あり】の材料） | %d カット・%.0f秒（%s） | 幅1280以上は⑤b-1 で使うコマごとに測る |' %
             (st['film'][0], st['film'][1], '・'.join(st['film_codes'])))
    L.append('| NIST の動く図 | 本体 %d カット・%.1f秒／差し込み %d カット・%.1f秒 | — |' % st['anim'])
    L.append('| フリー素材「イメージ」 | 本体 %d カット・%.1f秒／差し込み %d カット・%.1f秒 | 20%%に数えない・「イメージ」と出典 |' % st['stock'])
    tn, tp, ts, tb, tbat = st['text']
    L.append('| 文字だけ（パネル・決め所・文字の頁） | %d カット＝%.1f%%（秒 %.0f）・続く最長 %d（%s まで） | 2割まで・3連続で E |' % (tn, 100 * tp, ts, tb, tbat))
    L.append('| 種類（台本のまま→いま） | %s | — |' % '・'.join('%s %d→%d' % (KIND_JA.get(k, k), st['script_kinds'][k], st['kinds'][k])
                                                       for k in KIND_JA if st['script_kinds'][k] or st['kinds'][k]))
    L.append('| 合計 | %d カット・%s | — |' % (n, mmss(T)))
    L += ['', '### 章ごと', '', '| 章 | カット | 秒 | 実写 | 本物の差し込み | フリー | NIST の動く図 | 頁 | 文字だけ | 再現 | 図 |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for ch, d in st['perch'].items():
        L.append('| %s | %d | %.0f | %d | %d | %d | %d | %d | %d | %d | %d |' % (ch, d['cuts'], d['secs'], d['実写'], d['ins_real'], d['フリー'], d['図動'], d['頁'],
                                                                            d['panel'] + d['quote'] + d['文字の頁'], d['再現'], d['図']))
    L += ['', '## §1 冒頭（c101〜c105）の秒', '', '| 区間 | 秒 | 画 | 素材 |', '|---|---|---|---|']
    for cid, t0, t1, kind, cls, txt in opening(rows):
        L.append('| %s | %.1f〜%.1f（%.1f） | %s／%s | %s |' % (cid, t0, t1, t1 - t0, KIND_JA.get(kind, kind), CLASS_JA.get(cls, '—'), md_cell(txt[:70])))
    L += ['', '## §2 章ごと・カットごと', '']
    cur = None
    for r in rows:
        if r['ch'] != cur:
            cur = r['ch']
            d = st['perch'][cur]
            L += ['', '### %s（%d カット・%s から）' % (cur, d['cuts'], mmss(r['start'])), '',
                  '| カット | 秒 | 画の種類 | 素材（記号@区間） | 差し込み | 副題 | 権利 | 札 | 備考・語りの頭 |', '|---|---|---|---|---|---|---|---|---|']
        i = r['ins']
        ins = '%s%d：%s' % ('頭' if i['pos'] == 'head' else '尻', i['k'], i['text'][:60]) + '（%.1f秒）' % r['ins_secs'] if i else ''
        kind = KIND_JA.get(r['kind'], r['kind']) + ('・' + CLASS_JA[r['cls']] if r['kind'] == '実写' and r['cls'] else '')
        mark = '🔁' if r['assigned'] and r['kind'] != r['script_kind'] else ''
        L.append('| %s | %s +%.1f | %s%s | %s | %s | %s | %s | %s | %s |' % (
            r['cid'], mmss(r['start']), r['dur'], mark, kind, md_cell(r['main'][:90]), md_cell(ins), md_cell(r['sub']), md_cell(r['rights']),
            md_cell(r['label']), md_cell((r['note'][:80] + '／' if r['note'] and r['note'] != '—' else '') + '「' + r['narr'] + '…」')))
    L += ['', '## §3 門番の所見と ⑤b-1 で選ぶ所', '']
    for mark, s in probs:
        L.append('- %s %s' % (mark, s))
    if not probs:
        L.append('- E・⚠️ なし')
    for mark, s in st['pick']:
        L.append('- %s %s' % (mark, s))
    L += ['', '## §4 取得の一覧（使う素材と代わりの候補・⑤b-1 でまとめて落とす＝決め⑧で了承ずみ〈軽い道〉・YouTube は別に聞く）', '',
          '| 記号 | 種類 | 使うカット | ファイル名 | 出どころ | 大きさ | 秒 | MB | 権利 |', '|---|---|---|---|---|---|---|---:|---|']
    tot, alt_mb = collections.Counter(), 0.0
    for code, used_in, s in fetch:
        try:
            mb = float(s.get('mb') or 'x')
            if used_in == '（代わり）':
                alt_mb += mb
            else:
                tot[s.get('class', '')] += mb
        except ValueError:
            pass
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (code, CLASS_JA.get(s.get('class'), s.get('class', '')), used_in, md_cell(s.get('file', '')),
                                                                md_cell(s.get('url', '')), s.get('dims', ''), s.get('dur', ''), s.get('mb', ''), md_cell(s.get('rights', ''))))
    L += ['', '- MB の合計（測れた物だけ・元の画質）：' + '・'.join('%s %.0f' % (CLASS_JA.get(k, k), v) for k, v in tot.items()) +
          '／代わり %.1f（%d 点）' % (alt_mb, len(alts)),
          '- 軽い道（決め⑧）：1秒1コマの走査は幅1920前後の版（NIST の記録映像と点群 計 約625MB＋技術的知見の動画 796MB）・使う秒だけ元の画質から切り出す・'
          '写真とフリー素材（幅1920の版）を足して 約2GB', '']
    OUT_MD.write_text('\n'.join(L) + '\n', encoding='utf-8')


def selftest():
    srcs = {k: {} for k in ('B1', 'N#1', 'S#1', 'TFV')}

    def row(cid, kind, code=None, rng='', note='', ins=None, ch='第1章', dur=5.0, lines=2):
        return dict(cid=cid, ch=ch, start=0.0, dur=dur, lines=lines, kind=kind, script_kind=kind, main=(code or '') + ('@' + rng if rng else ''),
                    code=code, rng=rng, cls=class_of(code), main_secs=dur - (ins or {}).get('secs', 0), ins=ins,
                    ins_secs=(ins or {}).get('secs', 0.0), sub='', rights='', label='', note=note, assigned=True, narr='')
    base = [row('c%03d' % i, '実写', 'N#1' if i == 0 else 'B1', '%d–%d' % (10 * i, 10 * i + 6)) for i in range(3)] + [row('c1%02d' % i, '図') for i in range(7)]
    ok = True

    def run(name, rows, want):
        nonlocal ok
        st, probs = judge(rows, srcs)
        got = [s for m, s in probs if m == 'E']
        hit = bool(got) == want
        ok &= hit
        print('  %s %s（E %d 件%s）' % ('✓' if hit else '✗', name, len(got), '：' + got[0] if got else ''))
    run('① 正しい並び（実写30%・文字0）＝E なし', base, False)
    run('② 実写が20%を割る', [row('c%03d' % i, '図') for i in range(5)] + base[3:], True)
    run('③ 文字だけ3連続', base[:7] + [row('c2%02d' % i, 'quote') for i in range(3)], True)
    run('④ 同じ写真を2回', base + [row('c300', '実写', 'N#1')], True)
    run('⑤ 映像の区間が重なる（備考なし）', base + [row('c301', '実写', 'B1', '12–15')], True)
    run('⑥ 区間が重なるが備考に「別の秒」＝E なし', base + [row('c302', '実写', 'B1', '12–15', note='c001 と別の秒')], False)
    run('⑦ 出どころの表に無い記号', base + [row('c303', '実写', 'B9x')], True)
    run('⑧ 差し込みの行がカットの外', base + [row('c304', '図', ins=dict(pos='tail', k=3, code='TFV', rng='', text='TFV', secs=1.0))], True)
    return 0 if ok else 1


def main(argv):
    if '--selftest' in argv:
        return selftest()
    cuts = parse_daihon(DAIHON)
    rows, missing = build(cuts, read_tsv(ASSIGN))
    sources = {r['code']: r for r in read_tsv(SOURCES)}
    st, probs = judge(rows, sources, missing)
    write_outputs(rows, st, probs, sources)
    rn, rp, rs, rsp = st['real']
    tn, tp, ts, tb, tbat = st['text']
    print('cuts=%d secs=%.1f（%s）' % (st['cuts'], st['secs'], mmss(st['secs'])))
    print('実写 %d＝%.1f%%（映像 %d・写真 %d・TFのコマ %d）／本物の差し込み %d・%.1f秒／動く映像 %dカット・%.0f秒' %
          (rn, 100 * rp, st['real_by_class']['film'], st['real_by_class']['photo'], st['real_by_class']['anim'], st['real_ins'][0], st['real_ins'][1],
           st['film'][0], st['film'][1]))
    print('NIST の動く図 本体 %d・%.1f秒／差し込み %d・%.1f秒' % st['anim'])
    print('フリー 本体 %d・%.1f秒／差し込み %d・%.1f秒' % st['stock'])
    print('文字だけ %d＝%.1f%%・最長 %d（%s）' % (tn, 100 * tp, tb, tbat))
    print('種類 %s' % dict(st['kinds']))
    for m, s in probs:
        print(m, s)
    for m, s in st['pick']:
        print(m, s)
    print('→ %s・%s・%s' % (OUT_MD.name, OUT_TSV.name, OUT_FETCH.name))
    return 1 if any(m == 'E' for m, _ in probs) else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
