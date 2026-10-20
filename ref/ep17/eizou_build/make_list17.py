# -*- coding: utf-8 -*-
"""17本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-10-19・映像方針チャット）。23本目の make_list23.py を写して17本目の型に替えた。

  python ref/ep17/eizou_build/make_list17.py

入力：台本 第2版 ref/ep17/daihon_v2.md §4 の見出し行（画の欄。語りは字数と秒を数えるだけ）・§2 の決め所★の表
      eizou_build/assign17.psv（当て方＝全カット・区切りは「|」）・sources17.psv（素材の記号 → 出どころ・権利・大きさ）
出力：ref/ep17/eizou_list17.md（生成物＝手で直さない）・eizou_build/list17.tsv

17本目の型（23本目と違う所）
  - 種類＝実写（この事故の写真・事故機・姉妹機・同型機・記録映像 V1・Googleアース）／頁（報告書の付図・写真51 の頁・文字の頁・FAA・判決）
          ／関連（事故そのものではない実物の写真＝同じ型の操縦室・機関の建物・空港など）／イメージ（フリー素材）／案C（再現イラスト）／図／文字だけ
  - 「写真・実写」の割合（20%以上）は ④' の数え方（mech17）と同じく 実写＋頁 で数える。関連とイメージは別に数える
  - つかみ＝c101〜c109（最初の見出し＝章の扉は c109 のあと＝⑤b-1 で scene_jiko に「c1 の中の扉」を足す）
  - 決め所★17行の画面は作らない（10-07）＝★のカットに quote・文字だけを置かない

門番（E があれば exit 1・⚠️ は止めない）：
  E 実写・頁・関連・イメージに素材の記号が無い／記号が sources17.psv に無い／同じ記号を同じ寄りの名で2回（寄りの名を分ける）
  E BY-SA・GFDL が「額装（BY-SA）」でない・動きが「額ごと」でない・2回使う（1点1カット）
  E つかみ（c101〜c109）に案C・図・文字だけ／頁は「実写の地」の額装だけ
  E ★のカットが文字だけ／写真・実写（実写＋頁）が 20% 未満／文字だけが3つ続く
  E フリー素材・記録映像の長さがカットの 0.6 倍に足りない（手元にあるときだけ測る）
  ⚠️ 続く図（あいだの実写・頁・関連・イメージは飛ばす）で見た目の型が同じ／同じ見た目の型が4回以上（案C は場面ごとの数を表に）
  ⚠️ 静止写真の動きが「寄る」に偏る（50%超）／章の写真・実写が 20% 未満／別の写真なのに副題が同じ／素材が決まっていない（pending）
秒＝句読点なし÷365字/分の見込み（ゆっくりの話速・⑤a の実測で取り直す）。
"""
import csv
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
DAIHON = os.path.join(EP, 'daihon_v2.md')
OUT_MD = os.path.join(EP, 'eizou_list17.md')
OUT_TSV = os.path.join(HERE, 'list17.tsv')
NARR = os.path.join(REPO, 'audio', 'narration.json')
PUNCT = '、。？！「」（）・'
CUT = re.compile(r'^\*\*(c[1-9ab]\d{2})\*\*')
OPENING = ['c10%d' % i for i in range(1, 10)]
FIRST_HEAD_AFTER = 'c109'
RATE = 365.0
RATE_MIN = 0.6
PHOTO_LO = 0.20
LOOK_MAX = 3
PHOTO_KINDS = ('実写', '頁')
PIC_KINDS = ('実写', '頁', '関連', 'イメージ')
KEYS = ['cid', 'kind', 'main', 'frame', 'sub', 'motion', 'view', 'look', 'ga_new', 'note']


def nopunct(s):
    return ''.join(ch for ch in s if ch not in PUNCT and not ch.isspace())


def read_psv(path):
    with open(path, encoding='utf-8') as f:
        return [ln.rstrip('\n') for ln in f if not ln.startswith('#') and ln.strip()]


def heading(t, head, start=0):
    """見出しの行（行の頭の `head`）の位置。🔴 2026-10-20（⑤b-1）：`str.index` は最初の1つを取る＝台本 §3 の注（842行目）に
    「`## 4. 台本`」の字があり、§2 の切り出し `t[§2:最初の「## 4. 台本」]` が空＝★0件のまま「★のカットに決め所の画面」の E が
    対象0件で通っていた（⑤a-2 で見つけた）。行の頭だけを見て、`start` より後ろから探す"""
    m = re.compile('^' + re.escape(head), re.M).search(t, start)
    if not m:
        raise SystemExit('台本に見出し「%s」が無い（%d字目より後ろ）' % (head, start))
    return m.start()


def read_cuts():
    t = open(DAIHON, encoding='utf-8').read()
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
        if r['cid'] in OPENING:
            r['chap'] = 'つかみ（c101〜c109・最初の見出しは c109 のあと）'
        elif r['cid'].startswith('c1'):
            r['chap'] = '第1章　画面に出ていた文字（c110〜c117）'
        r['start'] = sec
        r['dur'] = r['cont'] = r['n'] / RATE * 60
        r['card'] = 0.0
        sec += r['dur']
    note = measured(rows)
    a2 = heading(t, '## 2. 原文に当てた決め所')
    sec2 = t[a2:heading(t, '## ', a2 + 1)]          # §2 の次の見出しまで（§4 を探さない＝並びに頼らない）
    star = set(re.findall(r'^\| *\d+ *\| *\*\*(c[1-9ab]\d{2})\*\* *\|', sec2, re.M))
    m = re.match(r'## 2\. 原文に当てた決め所 (\d+)件', sec2)
    want = int(m.group(1)) if m else None             # 陽性対照＝見出しの「17件」と読めた★の数
    return rows, star, want, note


def measured(rows):
    """🆕 2026-10-20（⑤b-1）：秒を **audio/narration.json の実測**に（23本目 make_list23・20本目 make_list20.measured() の型）。
    カット＝前 LEAD＋声（行間こみ）＋後 TAIL（決め所の余白は0＝⑤a-2 で★を外した）・扉 CARD_SEC はそのカットの頭（start は扉の前）。
    🔴 扉の位置は check_script.door_key（音の側〈aq_build.timeline・check_script ③・check_listener〉と scene_jiko._card_heads と同じ1つの規則）＝
       17本目は c110 の前（c1 の中の扉＝INNER_CARDS）と第2〜11章の頭の11枚。倍率の分母（cont）は扉を除く。
    narration.json のカットが台本と合わないときだけ ÷365 の見込みのまま（出力に書く）"""
    if not os.path.exists(NARR):
        return '÷365 の見込み（narration.json が無い）'
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    import check_script as CSC
    dur = json.load(open(NARR, encoding='utf-8')).get('durations', {})
    if [r['cid'] for r in rows] != [c for c in dur if c != 'ed01']:
        return '÷365 の見込み（narration.json が台本と合わない）'
    sec, prev = 0.0, None
    for r in rows:
        key = CSC.door_key(r['cid'])
        r['card'] = CSC.CARD_SEC if (prev is not None and key != prev) else 0.0
        prev = key
        r['start'] = sec
        r['cont'] = dur[r['cid']] + CSC.LEAD + CSC.TAIL
        r['dur'] = r['cont'] + r['card']
        sec += r['dur']
    return 'audio/narration.json の実測'


def star_screen(c):
    """★のカットに決め所の画面（文字だけ・quote）を置いたか。🔴 2026-10-20（⑤b-1）：当て方の欄 ga_new は「quote → 写真1」
    （決め所の画面**から**替えた）の形＝矢印の前の「quote」に当たって★17カットが全部鳴った（★0件のあいだは隠れていた）。
    見るのは**替えた先**（最後の「→」のあと・矢印が無ければ欄の全部）"""
    return bool(c['star']) and (c['kind'] == '文字だけ' or 'quote' in c['ga_new'].rsplit('→', 1)[-1])


def media_len(path):
    p = os.path.join(REPO, path)
    if not path or not os.path.exists(p):
        return None
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def motion_class(mo):
    if not mo:
        return ''
    if mo.startswith('映像'):
        return '映像'
    pre = '額ごと' if mo.startswith('額ごと') else ('額の中で' if mo.startswith('額の中で') else '')
    for key, name in (('2点', '2点'), ('引', '引く'), ('左へ', '左へ'), ('右へ', '右へ'), ('上へ', '上へ'), ('下へ', '下へ'), ('寄', '寄る')):
        if key in mo:
            return pre + name
    return mo


def fmt_t(s):
    return '%d:%04.1f' % (s // 60, s % 60)


def scene_of(c):
    if c['kind'] != '案C':
        return ''
    m = re.match(r'(C\d+)', c['look'])
    return m.group(1) if m else '?'


def main():
    cuts, star, want, tnote = read_cuts()
    E, W = [], []
    if want is None or len(star) != want:
        E.append('§2 の表から読めた★ %d ≠ 見出しの %s件（切り出しか表の形が崩れた＝★の門番が対象を失う）' % (len(star), want))
    arows = [ln.split('|') for ln in read_psv(os.path.join(HERE, 'assign17.psv'))]
    bad = [r[0] for r in arows if len(r) != len(KEYS)]
    if bad:
        E.append('assign17.psv の列の数が%dでない行：%s' % (len(KEYS), '・'.join(bad)))
    assign = {}
    for r in arows:
        if len(r) == len(KEYS):
            if r[0] in assign:
                E.append('assign17.psv に同じカットの行が2つ：%s' % r[0])
            assign[r[0]] = dict(zip(KEYS, [x.strip() for x in r]))
    known = {c['cid'] for c in cuts}
    for k in assign:
        if k not in known:
            E.append('assign17.psv のカット %s が台本に無い' % k)
    missing = [c['cid'] for c in cuts if c['cid'] not in assign]
    if missing:
        E.append('assign17.psv に無いカット %d：%s' % (len(missing), '・'.join(missing)))
    srows = read_psv(os.path.join(HERE, 'sources17.psv'))
    shead = srows[0].split('|')
    sources = {}
    for r in srows[1:]:
        v = r.split('|')
        if len(v) != len(shead):
            E.append('sources17.psv の列の数が%dでない：%s' % (len(shead), v[0]))
            continue
        if v[0] in sources:
            E.append('sources17.psv に同じ記号が2つ：%s' % v[0])
        sources[v[0]] = dict(zip(shead, v))

    for c in cuts:
        a = assign.get(c['cid'], {})
        for k in KEYS[1:]:
            c[k] = a.get(k, '')
        c['changed'] = '🔧' in c['note']
        c['star'] = c['cid'] in star

    use = defaultdict(list)
    for c in cuts:
        c['code'] = c['part'] = c['rights'] = c['credit'] = c['get'] = ''
        c['src_len'] = c['rate'] = None
        if c['kind'] not in PIC_KINDS:
            continue
        if not c['main']:
            E.append('%s %s なのに素材の記号が無い' % (c['cid'], c['kind']))
            continue
        code, part = (c['main'].split(':', 1) + [''])[:2]
        s = sources.get(code)
        if not s:
            E.append('%s 記号 %s が sources17.psv に無い' % (c['cid'], code))
            continue
        c['code'], c['part'], c['rights'], c['credit'], c['get'] = code, part, s['rights'], s['credit'], s['get']
        if s['get'].startswith('pending'):
            W.append('%s 素材が決まっていない（%s＝%s）' % (c['cid'], code, s['note'][:40]))
        if s['class'] in ('video', 'stock') and s['file'].endswith(('.mp4', '.webm', '.mkv')):
            have = media_len(s['file'])
            m = re.search(r'(\d+(?:\.\d+)?)〜(\d+(?:\.\d+)?)秒', c['motion'])
            if m:
                have = float(m.group(2)) - float(m.group(1))
            if have is None:
                W.append('%s 映像の素材 %s が手元に無い＝長さを測れない' % (c['cid'], s['file']))
            else:
                # 🆕 ⑤b-1：分母は扉を除いた中身の秒（cont＝narration.json の実測）。等速＝伸ばさない／1.0 未満は動きの欄に倍率（make_list23 の型）
                # 🆕 ⑤b-1（10-20 カズヤくん＝c101 は推奨 A）：動きの欄に「頭の差し込み＝k行目まで」＝映像はカットの頭の k 行だけ（あとは写真）＝
                #    分母は scene_jiko.head_secs と同じ式（k 行目を読み始める少し前＋入れ替え INTRO_X）＝式は scene_jiko の関数を呼ぶ（2か所に書かない）
                den, what = c['cont'], 'カット'
                mh = re.search(r'頭の差し込み＝(\d+)行目まで', c['motion'])
                if mh:
                    import scene_jiko as S
                    den, what = S.ins_sec(c['cid'], int(mh.group(1))) + S.INTRO_X, '頭の差し込み（%s行目まで）' % mh.group(1)
                c['src_len'] = have
                c['rate'] = have / den if den else 0
                mr = re.search(r'映像（[^）]*?(\d\.\d+)倍）', c['motion'])     # 「映像（0.74倍）」「映像（757〜762.5秒＝…・0.61倍）」
                if c['rate'] < RATE_MIN:
                    E.append('%s 映像 %.2f秒 ÷ %s %.2f秒 ＝ %.2f倍 ＜ %.1f（止め絵になる・素材か区間を替える）' % (c['cid'], have, what, den, c['rate'], RATE_MIN))
                elif c['rate'] < 1.0 and not (mr and float(mr.group(1)) <= c['rate'] + 1e-9):
                    E.append('%s 映像 %.2f秒 が%s %.2f秒 に足りない（等速なら尻が %.2f秒 欠ける）＝区間か素材を替えるか、動きの欄を「映像（%.2f倍）」以下に' % (
                        c['cid'], have, what, den, den - have, int(c['rate'] * 100) / 100))
        use[code].append((c['cid'], part))
        r = s['rights']
        if r.startswith(('BY-SA', 'GFDL')):
            if c['frame'] != '額装（BY-SA）':
                E.append('%s %s の %s が額装（BY-SA）でない（%s）' % (c['cid'], r, code, c['frame']))
            if not c['motion'].startswith('額ごと'):
                E.append('%s %s の %s の動きが「額ごと」でない（%s）＝写真は常に全部見える動きだけ' % (c['cid'], r, code, c['motion']))
    for code, us in sorted(use.items()):
        if len(us) > 1:
            parts = [p for _, p in us]
            r = sources[code]['rights']
            if r.startswith(('BY-SA', 'GFDL')):
                E.append('BY-SA・GFDL の %s を2回使う：%s（1点1カット）' % (code, '・'.join(x for x, _ in us)))
            elif len(set(parts)) < len(parts):
                E.append('%s を同じ寄りの名で2回：%s（寄りの名を分ける）' % (code, '・'.join('%s:%s' % (x, p or '—') for x, p in us)))
    for c in cuts:
        if c['cid'] in OPENING:
            if c['kind'] not in PIC_KINDS:
                E.append('%s つかみに実写でない画（%s）' % (c['cid'], c['kind']))
            elif c['kind'] == '頁' and '実写の地' not in c['frame']:
                E.append('%s つかみの頁は「実写の地」の額装だけ（%s）' % (c['cid'], c['frame']))
        if star_screen(c):
            E.append('%s ★のカットに決め所の画面（%s・%s）' % (c['cid'], c['kind'], c['ga_new']))

    # 図の見た目の型
    prev = None
    for c in cuts:
        if c['kind'] in PIC_KINDS:
            continue
        lk = c['look'] or c['kind']
        if prev and prev[1] == lk:
            W.append('続く図で見た目の型が同じ（%s）：%s→%s' % (lk, prev[0], c['cid']))
        prev = (c['cid'], lk)
    last = None   # 見る向きの合図（5b-80）＝横から見た断面 ⇄ 上から見た地図の切り替えだけ（正面の画面・手の絵は数えない）
    for c in cuts:
        c['signal'] = ''
        if c['view'] in ('横から', '上から') and c['kind'] not in PIC_KINDS:
            if last and last[1] != c['view']:
                c['signal'] = '🔁 %s→%s（前の図 %s）' % (last[1], c['view'], last[0])
            last = (c['cid'], c['view'])

    n = len(cuts)
    tot = sum(c['dur'] for c in cuts)
    photo = [c for c in cuts if c['kind'] in PHOTO_KINDS]
    real = [c for c in cuts if c['kind'] == '実写']
    pages = [c for c in cuts if c['kind'] == '頁']
    rel = [c for c in cuts if c['kind'] == '関連']
    stock = [c for c in cuts if c['kind'] == 'イメージ']
    for c in cuts:   # 文字の頁（写真・図の無い頁）は「文字だけの画面」に数える（mech17 と同じ）＝出どころの表の何の欄に「文字の頁」
        c['textpage'] = c['kind'] == '頁' and '文字の頁' in sources.get(c['code'], {}).get('note', '') + c['note']
    text = [c for c in cuts if c['kind'] == '文字だけ' or c['textpage']]
    illu = [c for c in cuts if c['kind'] == '案C']
    figs = [c for c in cuts if c['kind'] == '図']
    ratio = len(photo) / n
    if ratio < PHOTO_LO:
        E.append('写真・実写（実写＋頁） %.1f%% ＜ 20%%' % (ratio * 100))
    run = mx = 0
    for c in cuts:
        run = run + 1 if (c['kind'] == '文字だけ' or c['textpage']) else 0
        mx = max(mx, run)
    if mx >= 3:
        E.append('文字だけの画面が %d つ続く' % mx)
    still = [c for c in cuts if c['kind'] in PIC_KINDS and not c['motion'].startswith('映像')]
    mc = Counter(motion_class(c['motion']) for c in still)
    nz = sum(v for k, v in mc.items() if k.endswith('寄る'))
    if still and nz / len(still) > 0.5:
        W.append('静止写真の動きが「寄る」に偏る（%d/%d）' % (nz, len(still)))
    chaps = []
    for c in cuts:
        if not chaps or chaps[-1] != c['chap']:
            chaps.append(c['chap'])
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = sum(1 for c in cs if c['kind'] in PHOTO_KINDS)
        if k / len(cs) < PHOTO_LO:
            W.append('章「%s」の写真・実写 %d/%d（%.0f%%）＜ 20%%' % (ch.split('（')[0], k, len(cs), k / len(cs) * 100))
    subs = defaultdict(set)
    for c in cuts:
        if c['kind'] in ('実写', '頁', '関連') and c['sub']:   # イメージ（フリー素材）は同じ副題でよい
            subs[c['sub']].add(c['code'])
    for s, cs in subs.items():
        if len(cs) > 1:
            W.append('別の写真なのに副題が同じ「%s」：%s' % (s, '・'.join(sorted(cs))))
    looks = Counter((c['look'] or c['kind']) for c in figs)
    for k, v in looks.items():
        if v > LOOK_MAX:
            W.append('図の見た目の型「%s」が %d 回（%d回まで）' % (k, v, LOOK_MAX))
    scenes = Counter(scene_of(c) for c in illu)
    illu_looks = Counter(c['look'] for c in illu)
    changed = [c for c in cuts if c['changed']]
    kinds = Counter(c['kind'] for c in cuts)
    framed = Counter(c['frame'] for c in cuts if c['kind'] in PIC_KINDS)

    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        # 台本の画の欄（ga）は写さない＝撮影者の名前が入っている（新しいファイルに作者の名前を書かない＝src/credits_private.tsv だけ）。元の画は台本 §4 を読む
        # 🆕 ⑤b-1：cont（扉を除いた中身の秒）・card（頭の扉の秒）・src_len／rate（映像の素材の秒と倍率）・credit（出典の行の下書き）・
        #    textpage（文字の頁＝文字だけの画面に数える）＝make_plan17 が読む
        w.writerow(['cid', 'chap', 'start', 'dur', 'kind', 'code', 'part', 'frame', 'sub', 'motion', 'view', 'look', 'signal', 'rights', 'note', 'ga_new', 'star',
                    'cont', 'card', 'src_len', 'rate', 'credit', 'textpage'])
        for c in cuts:
            w.writerow([c['cid'], c['chap'], '%.2f' % c['start'], '%.2f' % c['dur'], c['kind'], c['code'], c['part'], c['frame'], c['sub'], c['motion'],
                        c['view'], c['look'], c['signal'], c['rights'], c['note'], c['ga_new'], '★' if c['star'] else '',
                        '%.2f' % c['cont'], '%.1f' % c['card'], '%.2f' % c['src_len'] if c['src_len'] is not None else '',
                        '%.3f' % c['rate'] if c['rate'] is not None else '', c['credit'], '1' if c['textpage'] else ''])

    head_t = next(c['start'] + c['dur'] for c in cuts if c['cid'] == FIRST_HEAD_AFTER)
    L = ['---', 'title: 17本目 場面ごとの映像・写真の一覧（生成物）', 'created: 2026-10-19', 'tags: [project/jiko-kensho, ep17]', '---', '',
         '# 17本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % n, '',
         '> **生成物＝手で直さない**。作り方＝`python ref/ep17/eizou_build/make_list17.py`（入力＝台本 第2版 `daihon_v2.md` §4 の画の欄と §2 の★・当て方 `eizou_build/assign17.psv`・出どころ `eizou_build/sources17.psv`）。直すのは入力（台本の画の欄は直さない＝⑤b はこの一覧に従う）。',
         '> 秒＝%s（⑤b-1 から＝前 0.35＋声＋後 0.50・章の扉 2.0＝c110 の前と第2〜11章の頭）。🔧＝台本の画の欄から替えたカット。' % tnote + '★＝決め所だった行（画面は作らない＝10-07）。色味は原本（10-07）。写真は画面いっぱい（10-11）＝例外は了承②の表。見た画像＝`eizou_build/seen17.tsv`。決めと確かめの正本＝Vault `Projects/事故検証-17本目-映像方針-20261019.md`。', '',
         '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真・実写（実写＋頁） | **%d カット＝%.1f%%**（実写 %d・頁 %d／秒 %.0f＝%.1f%%） | 20%%以上 %s（台本 第2版は66＝27.2%%） |' % (
             len(photo), ratio * 100, len(real), len(pages), sum(c['dur'] for c in photo), sum(c['dur'] for c in photo) / tot * 100, '✅' if ratio >= PHOTO_LO else '🔴'),
         '| 関連の写真（事故そのものではない実物） | %d カット | 「イメージ」か「現在の〜」と副題で断る |' % len(rel),
         '| フリー素材（イメージ） | %d カット（20%% に数えない） | 人の顔なし・字なし・生成AIなし |' % len(stock),
         '| 実写・頁・関連・イメージの計 | **%d カット＝%.1f%%** | 10-15「実写をもっと増やす」 |' % (len(photo) + len(rel) + len(stock), (len(photo) + len(rel) + len(stock)) / n * 100),
         '| 案C（再現イラスト） | %d カット（%s） | 台本 第2版は85 |' % (len(illu), '・'.join('%s %d' % (k, v) for k, v in sorted(scenes.items(), key=lambda kv: int(kv[0][1:]) if kv[0][1:].isdigit() else 99))),
         '| 図（案C の外） | %d カット | 続く図で同じ型を続けない |' % len(figs),
         '| 文字だけ（パネル・文字の頁） | %d カット（%s）・続く最長 %d | できる限り0に近く（台本 第2版は24＝決め所17・パネル2・文字の頁5） |' % (len(text), '・'.join(c['cid'] for c in text), mx),
         '| ★の行（決め所の画面はやめた） | %d（%s） | 画は写真・映像・図 |' % (len(star), '・'.join(sorted(star))),
         '| 見せ方（実写・頁・関連・イメージ） | %s | 全面が既定（10-11）・例外は了承② |' % '・'.join('%s %d' % (k, v) for k, v in framed.most_common()),
         '| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない＝⑤b はこの一覧に従う |' % len(changed),
         '| 静止の動き | %s | 寄るだけにしない（10-07） |' % '・'.join('%s %d' % (k, v) for k, v in mc.most_common()),
         '| 最初の見出し（章の扉） | %s のあと＝%.1f秒（%s） | 競合の型＝1分前後 |' % (FIRST_HEAD_AFTER, head_t, tnote),
         '| 合計 | %d カット・%s | — |' % (n, fmt_t(tot)), '']
    L += ['### 章ごと', '', '| 章 | カット | 秒 | 実写 | 頁 | 関連 | イメージ | 案C | 図 | 文字だけ |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = Counter(c['kind'] for c in cs)
        L.append('| %s | %d | %.0f | %d | %d | %d | %d | %d | %d | %d |' % (ch, len(cs), sum(c['dur'] for c in cs), k['実写'], k['頁'], k['関連'], k['イメージ'], k['案C'], k['図'], k['文字だけ']))
    L += ['', '## §1 つかみ（c101〜c109）＝実写か実写を地にした画面だけ（10-06）', '', '| カット | 秒 | 種類 | 素材 | 見せ方・動き | 副題 | 語りの頭 |', '|---|---|---|---|---|---|---|']
    for c in cuts:
        if c['cid'] in OPENING:
            L.append('| %s%s | %.1f〜%.1f（%.1f） | %s | %s%s | %s・%s | %s | %s |' % (
                c['cid'], ' ★' if c['star'] else '', c['start'], c['start'] + c['dur'], c['dur'], c['kind'], c['code'], (':' + c['part']) if c['part'] else '',
                c['frame'], c['motion'], c['sub'], c['first'][:26]))
    L += ['', '- 引き＝c105 の終わり %.1f秒（46秒より前）・最初の見出し（扉）＝c109 のあと %.1f秒' % (
        next(c['start'] + c['dur'] for c in cuts if c['cid'] == 'c105'), head_t), '']
    L += ['## §2 図と案C の見た目の型（続く所の見張り）', '', '| 見た目の型 | 回数 | カット |', '|---|---:|---|']
    by_look = defaultdict(list)
    for c in cuts:
        if c['kind'] in ('図', '案C', '文字だけ'):
            by_look[c['look'] or c['kind']].append(c['cid'])
    for k, v in sorted(by_look.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        L.append('| %s | %d | %s |' % (k, len(v), '・'.join(v)))
    L += ['', '- 見る向きの合図（🔁）＝%s' % ('・'.join('%s（%s）' % (c['cid'], c['signal'].split('（')[0]) for c in cuts if c['signal']) or '—'), '']
    L += ['## §3 章ごと・カットごと', '']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        L += ['### %s（%d カット・%s から）' % (ch, len(cs), fmt_t(cs[0]['start'])), '',
              '| カット | 秒 | 種類 | 素材 | 見せ方 | 副題 | 動き | 見る向き・見た目 | 権利 | 画（替えたカットは新しい画）・備考 |', '|---|---|---|---|---|---|---|---|---|---|']
        for c in cs:
            mat = c['code'] + ((':' + c['part']) if c['part'] else '')
            vl = '・'.join(x for x in (c['view'], c['look']) if x) + ((' ' + c['signal']) if c['signal'] else '')
            if c['kind'] in PIC_KINDS:
                rem = c['ga_new'] + (('｜' if c['ga_new'] else '') + c['note'] if c['note'] else '')
            else:
                rem = (c['ga_new'] if c['ga_new'] else (c['ga'][:60] + ('…' if len(c['ga']) > 60 else ''))) + ('｜' + c['note'] if c['note'] else '')
            L.append('| %s%s%s | %.1f（%.1f） | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                c['cid'], ' ★' if c['star'] else '', ' 🔧' if c['changed'] else '', c['start'], c['dur'], c['kind'], mat or '—', c['frame'] or '—', c['sub'] or '—',
                c['motion'] or '—', vl or '—', (c['rights'].split('（')[0] if c['rights'] else '—'), rem.replace('|', '／')))
        L.append('')
    L += ['## §4 素材の一覧（了承②の対象）', '', '| 記号 | 当てたカット | 取り方 | 置き場（git の外） | 大きさ | 権利 | 出典の表記（下書き） | 何 |', '|---|---|---|---|---|---|---|---|']
    used_by = defaultdict(list)
    for c in cuts:
        if c['code']:
            used_by[c['code']].append(c['cid'] + ((':' + c['part']) if c['part'] else ''))
    for code, s in sources.items():
        L.append('| %s | %s | %s | `%s` | %s | %s | %s | %s |' % (code, '・'.join(used_by.get(code, [])) or '（控え）', s['get'], s['file'], s['dims'], s['rights'], s['credit'], s['note']))
    L += ['', '## §5 門番', '']
    L += ['- 🔴 E %d 件' % len(E)] + ['  - ' + e for e in E]
    L += ['- ⚠️ %d 件' % len(W)] + ['  - ' + w for w in W]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

    print('cuts=%d 写真・実写=%d（%.1f%%＝実写 %d・頁 %d） 関連=%d イメージ=%d 案C=%d 図=%d 文字だけ=%d 🔧=%d 合計 %s' % (
        n, len(photo), ratio * 100, len(real), len(pages), len(rel), len(stock), len(illu), len(figs), len(text), len(changed), fmt_t(tot)))
    print('案C：', dict(scenes))
    print('案C の見た目：', dict(illu_looks))
    print('図の見た目（多い順）：', looks.most_common(12))
    print('見せ方：', dict(framed))
    print('動き：', dict(mc))
    print('扉：%s のあと %.1f秒' % (FIRST_HEAD_AFTER, head_t))
    print('E %d・⚠️ %d' % (len(E), len(W)))
    for e in E:
        print('  E', e)
    for w in W:
        print('  ⚠️', w)
    print('→', OUT_MD)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
