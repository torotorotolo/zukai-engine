# -*- coding: utf-8 -*-
"""25本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-10-25・チャット5）。24本目の make_list24.py を写して25本目の形に替えた。

  python ref/ep25/eizou_build/make_list25.py
  python ref/ep25/eizou_build/make_list25.py --selftest     （陽性・陰性の対照＝門番が鳴ることを先に見る）

入力：台本 第2版 ref/ep25/daihon_v2.md §4（画の欄と語り。語りは字数・秒に使う）
      eizou_build/assign25.psv（当て方）・eizou_build/sources25.psv（出どころ＝手で書く入力）
出力：ref/ep25/eizou_list25.md（生成物＝手で直さない）・eizou_build/list25.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E 写真・頁・イメージに素材の記号が無い／記号が sources25.psv に無い／使わないと決めた点（NG）が sources25.psv にある
  E 同じ点を2回（寄りの名が別のときだけ可）・同じ写真（実写）に別の副題
  E 🆕 脱線の前の場面（c201〜c319）に、時期「後・損傷」（壊れた車両や設備）の写真（記憶 feedback-fallback-stills-must-match-the-era・例外は理由つき）
  E 🆕 同じ形式の車両（事故列車でない）の写真の副題に「同じ形」が無い／付図26 の副題に「後日撮影・事故列車ではない」が無い
  E 🆕 名前の載る頁（出どころの備考に「名前」）を使うカットの備考に、名前を切り出しの外にする書き置きが無い
  E イメージの副題が「イメージ：」で始まらない
  E 冒頭（c101〜c107）に写真・頁でない画／写真と頁が 20% 未満／文字だけの画面（文字の頁）が3つ続く
  E 図の型（模式・案C・写真のほか）が全編で3回以上
  ⚠️ 続く図（あいだの写真は飛ばす）で見た目の型が同じ／写真の無い画面が5つ以上続く／章の写真と頁が 20% 未満
  ⚠️ 別の写真なのに副題が同じ／静止写真の動きが「寄る」に偏る（50%超）／素材を見ていない（人の欄が「未見」）
秒＝句読点なし÷365 の見込み（25本目の音はまだ無い＝⑤a のあと ⑤b-1 で実測に替える。🔴 audio/narration.json は別の回の音なので読まない）。
"""
import csv
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
DAIHON = os.path.join(EP, 'daihon_v2.md')
OUT_MD = os.path.join(EP, 'eizou_list25.md')
OUT_TSV = os.path.join(HERE, 'list25.tsv')
ASSIGN = os.path.join(HERE, 'assign25.psv')
SOURCES = os.path.join(HERE, 'sources25.psv')
PUNCT = re.compile(r'[、。，．,.「」『』（）()？！?!…・\s　〈〉：:"“”]')   # m25 と同じ秒（c101〜c107 で突き合わせた）
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
OPENING = ['c10%d' % i for i in range(1, 8)]
RATE = 365.0
PHOTO_LO = 0.20
PHOTOISH = ('実写', '頁', 'イメージ')
PRE_FROM, PRE_TO = 'c201', 'c319'          # 脱線（c320＝9時18分54秒ごろ）より前の場面
ORDER = '123456789abcd'
# 脱線の前の場面の門番の例外（語りが事故の前の場面ではない理由つき）
PRE_OK = {'c203': '語りは調べた委員会の紹介（事故を調べたのは…）＝事故の前の場面ではない'}
# 使わないと決めた点（見て外した理由・10-25）＝ sources25.psv に載せたら E
NG = {'M050501': '国交省 2005-05-01「事故現場概略図」＝マンションの名前が字で入っている（集合住宅は「マンション」とだけ）',
      'F11-外観': '付図11「マンション北側の損傷状況」＝建物の外観（住まいの近景）',
      'M050507': '国交省「一両目先頭のスカート」＝赤い跡（②③）＝原寸で確かめるまで使わない',
      'M050507_2': '国交省「二両目の状況」＝床に紫の布（私物かもしれない）',
      'M050429p': '国交省 2005-04-29「同型式の先頭車両【写真】」＝網点の刷り物を取り込んだ白黒写真＝撮った人が事故調でない恐れ（第三者）',
      'G2004': '国土地理院「2004年〜」の層＝この範囲は最新の層と画素の平均差9＝同じ写真の別の処理',
      'F56': '付図56「乗客の乗車位置」＝亡くなった人・けがをした人の位置の印（人の数を形で見せない）',
      'Mnikkin': '国交省「日勤教育関連調査」の頁＝台本が避けた「除草」などの話が載る（台本の範囲の外）',
      'F13-台車': '付図13 その6〜9（台車を上下反転させた写真）＝語りの対象でない（3両目台車は見た）',
      'F13-1L': '付図13 その1 の説明「車体中間部の状況（左に横転した状態を撮影）」の1点＝原画を見たら車内（室内・座席と扉）＝亡くなった人の多かった車両の中は使わない（10-25 チャット5）',
      'COURTS-photo': '裁判所の頁の庁舎の写真＝「写真・イラスト…を除き」著作権法上認められている利用（10-25 原文）＝使えない'}
# 映像方針で決めたこと（§0-5 の答え・一覧の §6 に出す）
DECIDED = [
    'c517 の地図＝R1 p.7「加島駅直前より始まる半径250mの左曲線手前約99mの位置において8時23分46秒ごろP最大Bが作動」＝JR東西線の御幣島駅〜加島駅（台本の画の欄も G0-101 で直した）',
    'c305・c607 の「直線」＝付図5（R2・事故現場略図）に「直線」の語は無い。シミュレーションの軌道の模型（付図73「直線 長さ300m」・付図74）にだけある＝副題・札に使わない（両カットとも画を替えた）',
    'cb05 Commons #12＝看板の字「迂回にご協力を／4月25日午前中は、この先の踏切で渋滞が予想されます。迂回をお願いします」（西日本旅客鉄道株式会社・尼崎東警察署）＝語り「その日の回り道を知らせる看板」と合う。撮影日は日付の欄 2025-04-30・分類 2025-04-25＝副題は「2025年4月撮影」',
    'cb01 Commons #3＝1280の版で見た：覆われた建物・クレーン・建物の前の線路を通る電車・自転車の人1（後ろ姿）＝語りと合う',
    'c703 の解説の図-5＝見た（ATS-P の曲線速照＝P地上子・パターン・常用最大ブレーキ／ATS-SW の曲線速照＝照査速度の2点・非常ブレーキ）＝案C-D の形のもと',
    'c303 付図17＝B8 と非常のあいだの「常用Bも非常Bも作動しない範囲」の図＝B1〜B8 の段は描いていない → 国交省 2005-05-01 の「ブレーキ、力行ハンドル位置図」（ユルメ・1〜8・非常）に替えた',
    'c409 ほか「列車全体の人数」＝報告書の付図55（車両ごとの死傷）・付図56（乗車位置）とも「現場を立ち去った乗客は含まれていない」＝列車全体の人数は無い＝語りどおり',
    'cb10 の札＝画の欄は「4段」と書いて3つ並べていた → 原因の3つの文の言い方（c502 の4段のうち3つ）に（台本の画の欄も G0-102 で直した）',
    'c922 と ca03（どちらも2009年9月25日）＝c922 は「調べる側から調べられる側へ漏れた矢印」（日付なし）・ca03 は「日付の札と役職の線」に分けた',
    '報告書の小さい写真（250〜650px）＝全面を既定（ぼけは差し替えの理由にしない）・縦長は高さいっぱいの額（左右は写真のぼかし）・説明の字が要る所は頁の切り出し',
    '注記の焼き込み＝付図の写真の上の矢印・札は、ほぼ全部が PDF の上に重ねた図形＝原画（埋め込みの画像）には無い（overlay25.tsv：差 1〜15%・付図26 の札の無い5コマは0%）＝全面は原画を使う（注記を消す加工は要らない）',
    '空中写真（付け替えの前後）＝1974〜78・1984〜86 は曲線が北で分かれて緩い・今は南まで来て急に曲がる（原寸560px×4 で見た）。「2004年〜」の層は最新と同じ写真＝使わない。線の重ねの描き足しは ⑤b で線の位置を当ててから',
    '章名「5両の脱線と107人」の札＝そのまま（台本の章名・サムネの「犠牲107人」と同じ数・死の語は無い）',
    '国交省の頁の規約＝「特記されていない限り国土交通省に帰属し、権利表記の記載がない限り PDL1.0」（10-25 原文・別紙の例外に事故の頁は無い）',
    '模式 {m0} → {m1}（実写・頁に替えた所と、写真が語りの対象でなく模式にした所を差し引き）・見た目の型は続く所で同じにしない',
    'フリー素材 {x0} → {x1}（事故の写真・報告書の頁・模式に替えた）＝残りは会議・裁判所・書類・ふだんの電車など、この事故の写真が無い場面',
]


def nopunct(s):
    return PUNCT.sub('', s)


def read_psv(path):
    with open(path, encoding='utf-8') as f:
        return [ln.rstrip('\n') for ln in f if not ln.startswith('#') and ln.strip()]


def base_kind(ga):
    if ga.startswith('実写'):
        return '実写'
    if ga.startswith('イメージ'):
        return 'イメージ'
    if ga.startswith('panel'):
        return '文字だけ'
    if ga.startswith('図 '):
        k = ga.split()[1].split('（')[0]
        return '頁' if re.match(r'^p\d+$', k) else k
    return '?'


def heading(t, head, start=0):
    m = re.compile('^' + re.escape(head), re.M).search(t, start)
    if not m:
        raise SystemExit('台本に見出し「%s」が無い（%d字目より後ろ）' % (head, start))
    return m.start()


def ckey(cid):
    return (ORDER.index(cid[1]), int(cid[2:]))


def read_cuts(daihon=DAIHON):
    t = open(daihon, encoding='utf-8').read()
    a4 = heading(t, '## 4. 台本')
    body = t[a4:heading(t, '## 5. ', a4)]
    rows, chap, cur = [], '', None
    for ln in body.split('\n'):
        if ln.startswith('### '):
            chap = ln[4:].strip()
            continue
        m = CUT.match(ln)
        if m:
            parts = ln.split(' ／ ')
            cur = dict(cid=m.group(1), chap=chap, ga=parts[1].strip() if len(parts) > 1 else '', n=0, first='', text='')
            rows.append(cur)
            continue
        if cur and ln.startswith('>'):
            s = ln[1:].strip()
            if s.startswith('Q:'):
                s = s[2:].strip()
            if not cur['first']:
                cur['first'] = s
            cur['text'] += s
            cur['n'] += len(nopunct(s))
    sec = 0.0
    for r in rows:
        r['start'] = sec
        r['dur'] = r['n'] / RATE * 60
        sec += r['dur']
    return rows


def motion_class(mo):
    if not mo:
        return ''
    if mo.startswith('映像'):
        return '映像'
    pre = '額の中で' if mo.startswith('額の中で') else ''
    for key, name in (('引', '引く'), ('左へ', '左へ'), ('右へ', '右へ'), ('上へ', '上へ'), ('下へ', '下へ'), ('寄', '寄る')):
        if key in mo:
            return pre + name
    return mo


def fmt_t(s):
    return '%d:%04.1f' % (s // 60, s % 60)


def is_textonly(c):
    return c['kind'] == '文字だけ' or (c['kind'] == '頁' and c['look'].startswith('文字'))


def build(assign_path=ASSIGN, sources_path=SOURCES, daihon=DAIHON):
    cuts = read_cuts(daihon)
    E, W = [], []
    keys = ['cid', 'kind', 'main', 'frame', 'sub', 'motion', 'view', 'look', 'ga_new', 'note']
    assign = {}
    for r in [ln.split('|') for ln in read_psv(assign_path)]:
        if len(r) != 10:
            E.append('assign25.psv の列の数が10でない行：%s（%d列）' % (r[0], len(r)))
            continue
        if r[0] in assign:
            E.append('assign25.psv に同じカットの行が2つ：%s' % r[0])
        assign[r[0]] = dict(zip(keys, [x.strip() for x in r]))
    known = {c['cid'] for c in cuts}
    for k in assign:
        if k not in known:
            E.append('assign25.psv のカット %s が台本に無い' % k)
    srows = read_psv(sources_path)
    shead = srows[0].split('|')
    sources = {}
    for r in srows[1:]:
        f = r.split('|')
        if len(f) != len(shead):
            E.append('sources25.psv の列の数が %d でない行：%s（%d列）' % (len(shead), f[0], len(f)))
            continue
        sources[f[0]] = dict(zip(shead, f))
    for code in sources:
        if code in NG:
            E.append('使わない点が sources25.psv にある：%s（%s）' % (code, NG[code]))

    for c in cuts:
        a = assign.get(c['cid'], {})
        c['kind0'] = base_kind(c['ga'])
        for k in keys[1:]:
            c[k] = a.get(k, '')
        c['kind'] = c['kind'] or c['kind0']
        c['changed'] = '🔧' in c['note'] or '🔧' in c['ga_new']
        if c['cid'] not in assign:
            W.append('%s assign25.psv に行が無い（台本の画の欄のまま）' % c['cid'])

    use = defaultdict(list)
    for c in cuts:
        c['code'] = c['part'] = c['rights'] = c['credit'] = c['era'] = c['people'] = c['get'] = ''
        if c['kind'] not in PHOTOISH + ('地図',):
            continue
        if not c['main']:
            if c['kind'] in PHOTOISH:
                E.append('%s %s なのに素材の記号が無い' % (c['cid'], c['kind']))
            continue
        code, part = (c['main'].split(':', 1) + [''])[:2]
        s = sources.get(code)
        if not s:
            E.append('%s 記号 %s が sources25.psv に無い' % (c['cid'], code))
            continue
        c.update(code=code, part=part, rights=s['rights'], credit=s['credit'], era=s['era'], people=s['people'], get=s['get'])
        use[code].append(c)
        if 'SA' in s['rights'] and not c['frame'].startswith('額装'):
            E.append('%s BY-SA の %s が額装でない（%s）' % (c['cid'], code, c['frame']))
        if c['kind'] == 'イメージ' and not c['sub'].startswith('イメージ：'):
            E.append('%s イメージの副題が「イメージ：」で始まらない（%s）' % (c['cid'], c['sub']))
        if s['era'] == '同型' and '同じ形' not in c['sub']:
            E.append('%s 事故列車でない同じ形式の車両の写真 %s の副題に「同じ形」が無い（%s）' % (c['cid'], code, c['sub']))
        if code.startswith('F26-') and '後日撮影・事故列車ではない' not in c['sub']:
            E.append('%s 付図26 の副題に報告書の断り「後日撮影・事故列車ではない」が無い（%s）' % (c['cid'], c['sub']))
        if '⚠️' in s['note'] and '名前' in s['note'] and '名前' not in c['note']:
            E.append('%s 名前の載る頁 %s を使うのに、名前を切り出しの外にする書き置きが備考に無い' % (c['cid'], code))
        if ckey(PRE_FROM) <= ckey(c['cid']) <= ckey(PRE_TO) and s['era'] == '後・損傷':
            if c['cid'] in PRE_OK:
                c['note'] = (c['note'] + '｜' if c['note'] else '') + '時期の門番の例外＝' + PRE_OK[c['cid']]
            else:
                E.append('%s 脱線の前の場面（%s〜%s）に、壊れた車両や設備の写真 %s（%s）' % (c['cid'], PRE_FROM, PRE_TO, code, c['sub']))
        if s['people'] == '未見':
            W.append('%s 素材 %s の人の写りが未見（⑤b で原寸）' % (c['cid'], code))

    for code, us in sorted(use.items()):
        if len(us) > 1:
            parts = [u['part'] for u in us]
            if not (all(parts) and len(set(parts)) == len(parts)):
                E.append('点 %s を2回使う：%s（寄りの名を分ける）' % (code, '・'.join(u['cid'] for u in us)))
            if us[0]['kind'] == '実写' and len({u['sub'] for u in us}) > 1:
                E.append('同じ写真 %s に別の副題：%s' % (code, ' ／ '.join('%s「%s」' % (u['cid'], u['sub']) for u in us)))
    for c in cuts:
        if c['cid'] in OPENING and c['kind'] not in PHOTOISH:
            E.append('%s 冒頭に写真・頁でない画（%s）' % (c['cid'], c['kind']))

    tc = Counter(c['kind'] for c in cuts if c['kind'] not in ('模式',) + PHOTOISH + ('文字だけ',))
    for k, v in tc.items():
        if v > 2:
            E.append('図の型「%s」が %d 回（2回まで）' % (k, v))
    prev = None
    for c in cuts:
        if c['kind'] in PHOTOISH:
            continue
        lk = c['look'] or c['kind']
        if prev and prev[1] == lk:
            W.append('続く図で見た目の型が同じ（%s）：%s→%s' % (lk, prev[0], c['cid']))
        prev = (c['cid'], lk)
    run, start = 0, None
    for c in cuts + [dict(cid='end', kind='実写', look='')]:
        if c['kind'] in ('実写', 'イメージ') or (c['kind'] == '頁' and not is_textonly(c)):
            if run >= 5:
                W.append('写真の無い画面が %d つ続く：%s〜' % (run, start))
            run, start = 0, None
        else:
            run += 1
            start = start or c['cid']
    last = None
    for c in cuts:
        c['signal'] = ''
        if c['view'] and c['kind'] not in PHOTOISH:
            if last and last[1] != c['view']:
                c['signal'] = '🔁 %s→%s（前の図 %s）' % (last[1], c['view'], last[0])
            last = (c['cid'], c['view'])

    n = len(cuts)
    tot = sum(c['dur'] for c in cuts)
    photo = [c for c in cuts if c['kind'] == '実写']
    stock = [c for c in cuts if c['kind'] == 'イメージ']
    pages = [c for c in cuts if c['kind'] == '頁']
    text = [c for c in cuts if is_textonly(c)]
    ratio = (len(photo) + len(pages)) / n
    if ratio < PHOTO_LO:
        E.append('写真と頁 %.1f%% ＜ 20%%' % (ratio * 100))
    run = mx = 0
    for c in cuts:
        run = run + 1 if is_textonly(c) else 0
        mx = max(mx, run)
    if mx >= 3:
        E.append('文字だけの画面が %d つ続く' % mx)
    stills = photo
    mc = Counter(motion_class(c['motion']) for c in stills)
    yoru = sum(v for k, v in mc.items() if k.endswith('寄る'))
    if stills and yoru / len(stills) > 0.5:
        W.append('静止写真の動きが「寄る」に偏る（%d/%d）' % (yoru, len(stills)))
    chaps = []
    for c in cuts:
        if not chaps or chaps[-1] != c['chap']:
            chaps.append(c['chap'])
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = sum(1 for c in cs if c['kind'] in ('実写', '頁'))
        if k / len(cs) < PHOTO_LO:
            W.append('章「%s」の写真と頁 %d/%d（%.0f%%）＜ 20%%' % (ch.split('（')[0], k, len(cs), k / len(cs) * 100))
    subs = defaultdict(set)
    for c in stills:
        subs[c['sub']].add(c['code'])
    for s, cs in subs.items():
        if len(cs) > 1:
            W.append('別の写真なのに副題が同じ「%s」：%s' % (s, '・'.join(sorted(cs))))
    return dict(cuts=cuts, E=E, W=W, sources=sources, chaps=chaps, n=n, tot=tot, photo=photo, stock=stock, pages=pages, text=text,
                ratio=ratio, mx=mx, mc=mc)


def write(r):
    cuts, E, W, sources, chaps = r['cuts'], r['E'], r['W'], r['sources'], r['chaps']
    n, tot, photo, stock, pages, text, ratio, mx, mc = r['n'], r['tot'], r['photo'], r['stock'], r['pages'], r['text'], r['ratio'], r['mx'], r['mc']
    framed = [c for c in photo if c['frame'].startswith('額装')]
    fulls = [c for c in photo if c['frame'].startswith('全面')]
    kinds = Counter(c['kind'] for c in cuts)
    looks = Counter((c['look'] or c['kind']) for c in cuts if c['kind'] not in PHOTOISH + ('文字だけ',))
    changed = [c for c in cuts if c['changed']]
    eras = Counter(c['era'] for c in photo)
    figs = [c for c in cuts if c['kind'] not in PHOTOISH + ('文字だけ',)]

    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['cid', 'chap', 'start', 'dur', 'kind', 'code', 'part', 'frame', 'sub', 'motion', 'view', 'look', 'signal', 'rights', 'era', 'people',
                    'credit', 'note', 'ga', 'ga_new', 'get'])
        for c in cuts:
            w.writerow([c['cid'], c['chap'], '%.2f' % c['start'], '%.2f' % c['dur'], c['kind'], c['code'], c['part'], c['frame'], c['sub'], c['motion'],
                        c['view'], c['look'], c['signal'], c['rights'], c['era'], c['people'], c['credit'], c['note'], c['ga'], c['ga_new'], c['get']])

    L = ['---', 'title: 25本目 場面ごとの映像・写真の一覧（生成物）', 'created: 2026-10-25', 'tags: [project/jiko-kensho, ep25]', '---', '',
         '# 25本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % n, '',
         '> **生成物＝手で直さない**。作り方＝`python ref/ep25/eizou_build/make_list25.py`（入力＝台本 第2版 `daihon_v2.md` §4・当て方 `eizou_build/assign25.psv`・出どころ `eizou_build/sources25.psv`）。直すのは入力。',
         '> 秒＝句読点なし÷365 の見込み（25本目の音はまだ無い＝⑤b-1 で実測に替える）。🔧＝台本の画の欄から替えたカット（⑤b はこの一覧に従う）。'
         '色味は原本（10-07）。写真は画面いっぱい（10-11）＝例外は縦長（高さいっぱいの額・左右は写真のぼかし）と説明の字が要る所（頁の切り出し）。'
         'この事故の動く記録映像は0本（【映像あり】は付けない）。見た画像の記録＝`eizou_build/seen25.tsv`。写真ごとの説明と注記＝`eizou_build/figcap25.tsv`・`overlay25.tsv`。'
         '決めと確かめの正本＝Vault `Projects/事故検証-25本目-映像方針-20261025.md`。', '',
         '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真（この事故・現場）＋報告書などの頁 | **%d カット＝%.1f%%**（写真 %d・頁 %d〈うち文字の頁 %d〉・秒 %.0f＝%.1f%%） | 20%%以上 %s |' % (
             len(photo) + len(pages), ratio * 100, len(photo), len(pages), sum(1 for c in pages if is_textonly(c)),
             sum(c['dur'] for c in photo + pages), sum(c['dur'] for c in photo + pages) / tot * 100, '✅' if ratio >= PHOTO_LO else '🔴'),
         '| フリー素材（イメージ） | %d カット（20%% に数えない） | 人の顔なし・字なし・生成AIなし・「イメージ」と出す・⑤b で1本ずつ原寸 |' % len(stock),
         '| 写真の時期 | %s | 脱線の前の場面（c201〜c319）に「後・損傷」を置かない（門番） |' % '・'.join('%s %d' % (k or '—', v) for k, v in eras.most_common()),
         '| 全面／額装 | 全面 %d・額装 %d（%s） | 例外は了承② |' % (len(fulls), len(framed), '・'.join('%s %d' % (k, v) for k, v in Counter(c['frame'] for c in framed).most_common()) or '—'),
         '| 文字だけ（文字の頁） | %d カット（%s）・続く最長 %d | できる限り0に近く・3つ続けない |' % (len(text), '・'.join(c['cid'] for c in text), mx),
         '| 図（模式・案C・型の図） | %d カット（模式 %d） | 続く図で同じ見た目にしない |' % (len(figs), sum(1 for c in figs if c['kind'] == '模式')),
         '| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない（G0-101・G0-102 の2つだけ直した）＝⑤b はこの一覧に従う |' % len(changed),
         '| 種類 | %s | — |' % '・'.join('%s %d' % (k, v) for k, v in kinds.most_common()),
         '| 図の見た目の型 | %d 種（%d カット） | — |' % (len(looks), sum(looks.values())),
         '| 静止写真の動き | %s | 寄るだけにしない（10-07） |' % '・'.join('%s %d' % (k, v) for k, v in mc.most_common()),
         '| 合計 | %d カット・%s | — |' % (n, fmt_t(tot)), '']
    L += ['### 章ごと', '', '| 章 | カット | 秒 | 写真 | 頁 | イメージ | 図 | 文字だけ |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = Counter(c['kind'] for c in cs)
        nf = len(cs) - sum(k[x] for x in PHOTOISH) - k['文字だけ']
        L.append('| %s | %d | %.0f | %d | %d | %d | %d | %d |' % (ch, len(cs), sum(c['dur'] for c in cs), k['実写'], k['頁'], k['イメージ'], nf,
                                                             sum(1 for c in cs if is_textonly(c))))
    L += ['', '## §1 冒頭（c101〜c107）＝実写と頁だけ（最初に設計した）', '', '| カット | 秒 | 素材 | 見せ方・動き | 副題 | 語りの頭 |', '|---|---|---|---|---|---|']
    for c in cuts:
        if c['cid'] in OPENING:
            L.append('| %s | %.1f〜%.1f（%.1f） | %s%s | %s・%s | %s | %s |' % (
                c['cid'], c['start'], c['start'] + c['dur'], c['dur'], c['code'], (':' + c['part']) if c['part'] else '', c['frame'], c['motion'], c['sub'],
                c['first'][:24]))
    L += ['', '- 引き＝c105 の終わり %.1f秒（よく語られる話）・ひっくり返し c106 の終わり %.1f秒（46秒より前）・最初の見出しの手前 c107 の終わり %.1f秒' % tuple(
        next(c['start'] + c['dur'] for c in cuts if c['cid'] == x) for x in ('c105', 'c106', 'c107')),
          '- 流れ＝衛星写真で場所（今）→ 運転室からの視界（後日撮影）→ 現場の空撮（脱線）→ 1両目（107人）→ 曲線の「70」の標識（よく語られる話）→ 報告書 p.222（★）→ 付図24（記録の秒）。再現イラストは置かない・事故の瞬間は描かない', '']
    L += ['## §2 図の見た目の型（続く所の見張り）', '', '| 見た目の型 | 回数 | カット |', '|---|---:|---|']
    by_look = defaultdict(list)
    for c in cuts:
        if c['kind'] not in PHOTOISH + ('文字だけ',):
            by_look[c['look'] or c['kind']].append(c['cid'])
    for k, v in sorted(by_look.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        L.append('| %s | %d | %s |' % (k, len(v), '・'.join(v)))
    L += ['', '- 見る向きの合図（🔁）＝%s' % ('・'.join('%s（%s）' % (c['cid'], c['signal'].split('（')[0]) for c in cuts if c['signal']) or '—'), '']
    L += ['## §3 章ごと・カットごと', '']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        L += ['### %s（%d カット・%s から）' % (ch, len(cs), fmt_t(cs[0]['start'])), '',
              '| カット | 秒 | 種類 | 素材 | 見せ方 | 副題 | 動き | 見る向き・見た目 | 権利・時期・人 | 画（替えたカットは新しい画）・備考 |', '|---|---|---|---|---|---|---|---|---|---|']
        for c in cs:
            mat = c['code'] + ((':' + c['part']) if c['part'] else '')
            vl = '・'.join(x for x in (c['view'], c['look']) if x) + ((' ' + c['signal']) if c['signal'] else '')
            rp = '・'.join(x for x in ((c['rights'].split('（')[0] if c['rights'] else ''), c['era'], c['people']) if x)
            if c['kind'] in PHOTOISH:
                rem = (c['ga_new'] + '｜' if c['ga_new'] else '') + c['note']
            else:
                rem = (c['ga_new'] + ('｜' + c['note'] if c['note'] else '')) if c['ga_new'] and c['ga_new'] != '台本どおり' else (
                    c['ga'][:70] + ('…' if len(c['ga']) > 70 else '') + ('｜' + c['note'] if c['note'] else ''))
            L.append('| %s%s | %.1f（%.1f） | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                c['cid'], ' 🔧' if c['changed'] else '', c['start'], c['dur'], c['kind'], mat or '—', c['frame'] or '—', c['sub'] or '—',
                c['motion'] or '—', vl or '—', rp or '—', rem.replace('|', '／')))
        L.append('')
    L += ['## §4 素材の一覧（了承②の対象）', '', '| 記号 | 当てたカット | 取り方 | 置き場（git の外） | 大きさ | 権利・根拠 | 出典の表記（下書き） | 時期・人 | 何 |', '|---|---|---|---|---|---|---|---|---|']
    used_by = defaultdict(list)
    for c in cuts:
        if c['code']:
            used_by[c['code']].append(c['cid'] + ((':' + c['part']) if c['part'] else ''))
    for code, s in sources.items():
        L.append('| %s | %s | %s | `%s` | %s | %s（%s） | %s | %s・%s | %s |' % (code, '・'.join(used_by.get(code, [])) or '（控え）', s['get'], s['file'], s['dims'],
                                                                     s['rights'], s['basis'], s['credit'], s['era'], s['people'], s['title']))
    L += ['', '## §5 門番', '']
    L += ['- 🔴 E %d 件' % len(E)] + ['  - ' + e for e in E]
    L += ['- ⚠️ %d 件' % len(W)] + ['  - ' + w for w in W]
    L += ['', '### 使わないと決めた点（見て外した理由・sources25.psv に載せると E）', ''] + ['- %s＝%s' % kv for kv in NG.items()]
    cnt = dict(m0=sum(1 for c in cuts if c['kind0'] == '模式'), m1=sum(1 for c in cuts if c['kind'] == '模式'),
               x0=sum(1 for c in cuts if c['kind0'] == 'イメージ'), x1=len(stock))
    L += ['', '## §6 映像方針で決めたこと（台本 §0-5 の答え・10-25）', ''] + ['%d. %s' % (i + 1, d.format(**cnt)) for i, d in enumerate(DECIDED)]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

    print('cuts=%d 写真=%d 頁=%d（%.1f%%） イメージ=%d 文字だけ=%d 図=%d（模式 %d） 🔧=%d 合計 %s' % (
        n, len(photo), len(pages), ratio * 100, len(stock), len(text), len(figs), sum(1 for c in figs if c['kind'] == '模式'), len(changed), fmt_t(tot)))
    print('種類：', dict(kinds))
    print('時期：', dict(eras))
    print('動き：', dict(mc))
    print('E %d・⚠️ %d' % (len(E), len(W)))
    for e in E:
        print('  E', e)
    for w in W:
        print('  ⚠️', w)
    print('→', OUT_MD)
    return 1 if E else 0


def selftest():
    """陽性＝門番が鳴る入力を作って E を数える／陰性＝今の入力で E 0（main で見る）"""
    import tempfile
    rows = read_psv(ASSIGN)
    srcs = read_psv(SOURCES)
    tmp = tempfile.mkdtemp()

    def run(arows, srows):
        a = os.path.join(tmp, 'a.psv')
        s = os.path.join(tmp, 's.psv')
        open(a, 'w', encoding='utf-8').write('\n'.join(arows) + '\n')
        open(s, 'w', encoding='utf-8').write('\n'.join(srows) + '\n')
        return build(a, s)['E']

    checks = []
    # ① 脱線の前の場面（c213）に壊れた車両の写真（F13-1F）
    a1 = [('c213|実写|F13-1F|全面|1両目の前部の正面の損傷〈報告書の付図13〉|寄る|||試し|' if r.startswith('c213|') else r) for r in rows]
    checks.append(('脱線の前に壊れた車両', any('脱線の前の場面' in e for e in run(a1, srcs))))
    # ② 付図26 の副題から断りを消す
    a2 = [r.replace('（名神高速の跨線橋のあたり）〈後日撮影・事故列車ではない〉', '（名神高速の跨線橋のあたり）') if r.startswith('c102|') else r for r in rows]
    checks.append(('付図26 の断り', any('付図26 の副題' in e for e in run(a2, srcs))))
    # ③ 同じ形式の車両の副題から「同じ形」を消す
    a3 = [r.replace('（同じ形式の車両）', '') if r.startswith('c704|') else r for r in rows]
    checks.append(('同じ形式の断り', any('同じ形式の車両' in e for e in run(a3, srcs))))
    # ④ 名前の載る頁の書き置きを消す
    a4 = [r.replace('⚠️ 頁の頭の宛先の大臣と委員長の名前＝切り出しの外', '') if r.startswith('c805|') else r for r in rows]
    checks.append(('名前の頁の書き置き', any('名前の載る頁' in e for e in run(a4, srcs))))
    # ⑤ 使わない点を出どころに足す
    s5 = srcs + ['M050501|mlit-page|事故現場概略図|x|x|x|PDL1.0|x|x|文書|なし|x|x']
    checks.append(('使わない点', any('使わない点' in e for e in run(rows, s5))))
    # ⑥ 同じ写真に別の副題
    a6 = [r.replace('|事故の現場〈報告書の付図12〉|寄る（建物と1両目へ）', '|空から見た現場〈報告書の付図12〉|寄る（建物と1両目へ）') if r.startswith('c401|') else r for r in rows]
    checks.append(('同じ写真に別の副題', any('別の副題' in e for e in run(a6, srcs))))
    # ⑦ 冒頭に図
    a7 = [('c103|模式||||||試しの模式|試し|' if r.startswith('c103|') else r) for r in rows]
    checks.append(('冒頭に図', any('冒頭に写真・頁でない画' in e for e in run(a7, srcs))))
    # 陰性＝今の入力
    neg = run(rows, srcs)
    ok = all(v for _, v in checks) and not neg
    for name, v in checks:
        print('陽性', name, '→', '鳴った' if v else '✗ 鳴らない')
    print('陰性（今の入力）E', len(neg), '→', 'selftest OK' if ok else 'selftest ✗')
    return 0 if ok else 1


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        return selftest()
    return write(build())


if __name__ == '__main__':
    sys.exit(main())
