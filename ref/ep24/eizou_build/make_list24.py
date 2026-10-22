# -*- coding: utf-8 -*-
"""24本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-10-22・チャット5）。23本目の make_list23.py を写して24本目の形に替えた。

  python ref/ep24/eizou_build/make_list24.py

入力：台本 第2版 ref/ep24/daihon_v2.md §4（画の欄と語り。語りは字数・秒と「責める行」の判定に使う）
      eizou_build/assign24.psv（当て方）・eizou_build/sources24.psv（出どころ＝make_sources24.py が書く）
出力：ref/ep24/eizou_list24.md（生成物＝手で直さない）・eizou_build/list24.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E 写真・頁・イメージに素材の記号が無い／記号が sources24.psv に無い／同じ点を2回（PD・CC0・CC BY で寄りの名が別のときだけ可）
  E BY-SA が「額装（BY-SA）」でない・動きが「額ごと」でない／BY-SA を全面にする
  E 🆕 爆発の前（第1章〜第5章の c617 まで）に、時期が「後」か「今・跡」の写真（記憶 feedback-fallback-stills-must-match-the-era・§0-5）
  E 🆕 責める・評価する行（語りに 運転員・職員・当直長・責め・誤り・違反・わざと・知らなかった）に、顔の判る人の写真（§0-5）
  E 冒頭（c101〜c107）に写真・頁・イメージでない画／写真と頁が 20% 未満／文字だけの画面（パネルと文字の頁）が3つ続く
  E 図の型（模式のほか）が全編で3回以上（同じ図を何度も使わない＝台本の設計で2回まで）
  ⚠️ 続く図（あいだの写真は飛ばす）で見た目の型が同じ／写真の無い画面が5つ以上続く／章の写真と頁が 20% 未満
  ⚠️ 別の写真なのに副題が同じ／静止写真の動きが「寄る」に偏る（50%超）
  🆕 E フリー素材の映像の長さがカットの 0.6 倍に足りない／1.0 倍に足りないのに動きの欄に「映像（0.xx倍）」が無い（手元にあるときだけ測る・
     ⑤b-1＝23本目 make_list23・17本目 make_list17 の型）
秒＝🆕 2026-10-22（⑤b-1）から **audio/narration.json の実測**（前 0.35＋声＋後 0.50・章の扉 2.0＝c2〜cc の頭の11枚＝check_script.door_key と同じ規則）。
   narration.json が無い・台本と合わないときだけ ÷365 の見込み（出力に書く）。
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
OUT_MD = os.path.join(EP, 'eizou_list24.md')
OUT_TSV = os.path.join(HERE, 'list24.tsv')
NARR = os.path.join(REPO, 'audio', 'narration.json')
PUNCT = '、。？！「」（）・'
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
OPENING = ['c10%d' % i for i in range(1, 8)]
RATE = 365.0
RATE_MIN = 0.6          # 映像は 0.6 倍まで伸ばしてよい（footage の決まり）＝これ未満は止め絵になる
PHOTO_LO = 0.20
BLAME = re.compile(r'運転員|職員|当直長|責め|誤り|違反|わざと|知らなかった|規則に反')
PRE_ERA_BAD = ('後', '今・跡', 'イメージ')  # §0-5＝夜と4月25日の場面に今の跡の写真・フリー素材を置かない
PHOTOISH = ('実写', '参考', 'イメージ', '頁')
# 責める行の門番の例外（人を見て決めた理由つき・10-22）＝写っているのは説明した側で、責められた職員ではない
PEOPLE_OK = {'c807': '会議のソ連側の席（ソ連の専門家団の長の名札）＝語りはソ連の報告が「職員の動機」をどう説明したか＝説明した側の写真',
             'c811': '記者会見の壇上＝語りは「主語は職員」というソ連の説明の書き方＝説明した側の写真'}
# 使わない点（見て外した理由・10-22）＝ sources24.psv に載せない。載せたら E
NG = {'CR4B:全体': '2025年の4号機の制御室＝学生が真ん中に立つ（運転員に見える）＝左の盤だけ切り出す',
      'TH2013': '2013年のタービン建屋＝2013年2月の屋根の崩れ（1986年の跡と取り違える）',
      'V4CR': '4号機の制御室の動画（2016）＝ほとんど真っ暗・見学の人の列',
      'M4_14': '2014年の4号機の模型＝反原発の張り紙が貼ってある（BY-SA で切れない）',
      'IGN05': 'イグナリナ1号機（2005）＝駐車場と食堂',
      'X12160809': 'Pexels「錆びた制御盤」＝炭酸水の自動販売機',
      'X32034022': 'Pexels「冷却塔」＝4号炉の物でない見込み',
      'CZ1': '1号機の炉の建屋（2007）＝画質が低い（緑がかった動画のコマ）',
      'G2022': '2022年4月の IAEA 訪問＝人と報道陣が主役・アーチが写らない',
      'KURSK2024': 'クルスク原発の IAEA 訪問＝顔が主役'}


def nopunct(s):
    return ''.join(ch for ch in s if ch not in PUNCT and not ch.isspace())


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
    """見出しの行（行の頭の `head`）の位置。🆕 2026-10-22（⑤b-1）：`str.index` は最初の1つを取る＝本文の注に同じ字があると
    切り出しが空になる（17本目 ⑤b-1 の落とし穴）。行の頭だけを見て、`start` より後ろから探す"""
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
        r['start'] = sec
        r['dur'] = r['cont'] = r['n'] / RATE * 60
        r['card'] = 0.0
        sec += r['dur']
    return rows, measured(rows)


def measured(rows):
    """🆕 2026-10-22（⑤b-1）：秒を **audio/narration.json の実測**に（17本目 make_list17・23本目 make_list23・20本目 make_list20.measured() の型）。
    カット＝前 LEAD＋声（行間こみ）＋後 TAIL・扉 CARD_SEC はそのカットの頭（start は扉の前）。
    🔴 扉の位置は check_script.door_key（音の側〈aq_build.timeline・check_script ③・check_listener〉と scene_jiko._card_heads と同じ1つの規則）＝
       24本目は c2〜cc の頭の11枚（つかみ c101〜c107 が c1 の記号を使い切る＝INNER_CARDS は要らない）。倍率の分母（cont）は扉を除く。
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
        key = CSC.door_key(r['cid'], slug='ep24')
        r['card'] = CSC.CARD_SEC if (prev is not None and key != prev) else 0.0
        prev = key
        r['start'] = sec
        r['cont'] = dur[r['cid']] + CSC.LEAD + CSC.TAIL
        r['dur'] = r['cont'] + r['card']
        sec += r['dur']
    return 'audio/narration.json の実測'


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
    for key, name in (('引', '引く'), ('左へ', '左へ'), ('右へ', '右へ'), ('上へ', '上へ'), ('下へ', '下へ'), ('寄', '寄る')):
        if key in mo:
            return pre + name
    return mo


def fmt_t(s):
    return '%d:%04.1f' % (s // 60, s % 60)


def chap_no(cid):
    return cid[1]  # '1'〜'9','a','b','c'


def is_pre_explosion(cid):
    """爆発の前の章＝第1章〜第5章の c617 まで（c2xx〜c6xx・c618 から後は爆発のあと）"""
    return cid[1] in '23456' and not (cid[1] == '6' and int(cid[2:]) >= 18)


def is_textonly(c):
    return c['kind'] == '文字だけ' or (c['kind'] == '頁' and c['look'].startswith('文字'))


def main():
    cuts, tnote = read_cuts()
    E, W = [], []
    arows = [ln.split('|') for ln in read_psv(os.path.join(HERE, 'assign24.psv'))]
    keys = ['cid', 'kind', 'main', 'frame', 'sub', 'motion', 'view', 'look', 'ga_new', 'note']
    assign = {}
    for r in arows:
        if len(r) != 10:
            E.append('assign24.psv の列の数が10でない行：%s（%d列）' % (r[0], len(r)))
            continue
        if r[0] in assign:
            E.append('assign24.psv に同じカットの行が2つ：%s' % r[0])
        assign[r[0]] = dict(zip(keys, [x.strip() for x in r]))
    known = {c['cid'] for c in cuts}
    for k in assign:
        if k not in known:
            E.append('assign24.psv のカット %s が台本に無い' % k)
    srows = read_psv(os.path.join(HERE, 'sources24.psv'))
    shead = srows[0].split('|')
    sources = {r.split('|')[0]: dict(zip(shead, r.split('|'))) for r in srows[1:]}
    for code in sources:
        if code in NG:
            E.append('使わない点が sources24.psv にある：%s（%s）' % (code, NG[code]))

    for c in cuts:
        a = assign.get(c['cid'], {})
        c['kind0'] = base_kind(c['ga'])
        for k in keys[1:]:
            c[k] = a.get(k, '')
        c['kind'] = c['kind'] or c['kind0']
        if c['kind'] in ('実写', '参考') and not c['sub']:
            m = re.search(r'副題「(.+?)」', c['ga'])
            c['sub'] = m.group(1) if m else ''
        c['changed'] = '🔧' in c['note'] or '🔧' in c['ga_new']
        if c['cid'] not in assign:
            W.append('%s assign24.psv に行が無い（台本の画の欄のまま）' % c['cid'])

    use = defaultdict(list)
    for c in cuts:
        c['code'] = c['part'] = c['rights'] = c['credit'] = c['era'] = c['people'] = c['get'] = ''
        c['src_len'] = c['rate'] = None
        if c['kind'] not in PHOTOISH:
            continue
        if not c['main']:
            E.append('%s %s なのに素材の記号が無い' % (c['cid'], c['kind']))
            continue
        code, part = (c['main'].split(':', 1) + [''])[:2]
        s = sources.get(code)
        if not s:
            E.append('%s 記号 %s が sources24.psv に無い' % (c['cid'], code))
            continue
        c.update(code=code, part=part, rights=s['rights'], credit=s['credit'], era=s['era'], people=s['people'], get=s['get'])
        if s['type'] == 'stock' and s['file'].endswith(('.mp4', '.webm', '.mkv')):
            # 🆕 ⑤b-1（10-22）：映像の長さの門番（23本目 make_list23・17本目 make_list17 の型）。分母は扉を除いた中身の秒（cont＝実測）。
            #    区間「a〜b秒」が動きの欄にあればその長さ。等速＝伸ばさない／1.0 未満は動きの欄に「映像（0.xx倍）」（0.6 未満は E）
            have = media_len(s['file'])
            m = re.search(r'(\d+(?:\.\d+)?)〜(\d+(?:\.\d+)?)秒', c['motion'])
            if m:
                have = float(m.group(2)) - float(m.group(1))
            if have is None:
                W.append('%s 映像の素材 %s が手元に無い＝長さを測れない' % (c['cid'], s['file']))
            else:
                den = c['cont']
                c['src_len'] = have
                c['rate'] = have / den if den else 0
                mr = re.search(r'映像（[^）]*?(\d\.\d+)倍）', c['motion'])     # 「映像（0.83倍）」「映像（0〜5.8秒＝…・0.83倍）」
                if c['rate'] < RATE_MIN:
                    E.append('%s 映像 %.2f秒 ÷ カット %.2f秒 ＝ %.2f倍 ＜ %.1f（止め絵になる・素材か区間を替える）' % (c['cid'], have, den, c['rate'], RATE_MIN))
                elif c['rate'] < 1.0 and not (mr and float(mr.group(1)) <= c['rate'] + 1e-9):
                    E.append('%s 映像 %.2f秒 がカット %.2f秒 に足りない（等速なら尻が %.2f秒 欠ける）＝区間か素材を替えるか、動きの欄を「映像（%.2f倍）」以下に' % (
                        c['cid'], have, den, den - have, int(c['rate'] * 100) / 100))
        use[code].append((c['cid'], part))
        r = s['rights']
        if 'SA' in r:
            if c['frame'] != '額装（BY-SA）':
                E.append('%s BY-SA の %s が額装（BY-SA）でない（%s）' % (c['cid'], code, c['frame']))
            if not c['motion'].startswith('額ごと'):
                E.append('%s BY-SA の %s の動きが「額ごと」でない（%s）＝写真は常に全部見える動きだけ' % (c['cid'], code, c['motion']))
        if c['frame'] == '額装（小さい）' and c['motion'] and not c['motion'].startswith('額'):
            E.append('%s 小さい写真の動き（%s）＝額の中で' % (c['cid'], c['motion']))
        if c['kind'] in ('実写', '参考') and c['frame'].startswith('全面') and 'SA' in r:
            E.append('%s BY-SA を全面にしている（%s）' % (c['cid'], r))
        if is_pre_explosion(c['cid']) and c['era'] in PRE_ERA_BAD:
            E.append('%s 爆発の前の章に、時期が「%s」の写真 %s（%s）' % (c['cid'], c['era'], code, c['sub']))
        if c['people'] == '顔' and BLAME.search(c['text']):
            if c['cid'] in PEOPLE_OK:
                c['note'] = (c['note'] + '｜' if c['note'] else '') + '責める行の門番の例外＝' + PEOPLE_OK[c['cid']]
            else:
                E.append('%s 責める・評価する行（「%s」）に顔の判る人の写真 %s' % (c['cid'], BLAME.search(c['text']).group(0), code))

    for code, us in sorted(use.items()):
        if len(us) > 1:
            parts = [p for _, p in us]
            rights = sources[code]['rights']
            ok = (('SA' not in rights) and all(parts) and len(set(parts)) == len(parts))
            if not ok:
                E.append('点 %s を2回使う：%s（1点1カット・PD/CC0/CC BY は寄りの名を分ける）' % (code, '・'.join(x for x, _ in us)))
    for c in cuts:
        if c['cid'] in OPENING and c['kind'] not in PHOTOISH:
            E.append('%s 冒頭に写真・頁・イメージでない画（%s）' % (c['cid'], c['kind']))

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
    for c in cuts + [dict(cid='end', kind='実写')]:
        if c['kind'] in ('実写', '参考', 'イメージ') or (c['kind'] == '頁' and not is_textonly(c)):
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
    ref_ = [c for c in cuts if c['kind'] == '参考']
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
    stills = photo + ref_
    mc = Counter(motion_class(c['motion']) for c in stills)
    if stills and sum(v for k, v in mc.items() if k.endswith('寄る')) / len(stills) > 0.5:
        W.append('静止写真の動きが「寄る」に偏る（%d/%d）' % (sum(v for k, v in mc.items() if k.endswith('寄る')), len(stills)))
    chaps = []
    for c in cuts:
        if not chaps or chaps[-1] != c['chap']:
            chaps.append(c['chap'])
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = sum(1 for c in cs if c['kind'] in ('実写', '頁'))
        if k / len(cs) < PHOTO_LO:
            W.append('章「%s」の写真と頁 %d/%d（%.0f%%）＜ 20%%（参考 %d・イメージ %d は別）' % (
                ch.split('（')[0], k, len(cs), k / len(cs) * 100, sum(1 for c in cs if c['kind'] == '参考'), sum(1 for c in cs if c['kind'] == 'イメージ')))
    subs = defaultdict(set)
    for c in stills:
        subs[c['sub']].add(c['code'])
    for s, cs in subs.items():
        if len(cs) > 1:
            W.append('別の写真なのに副題が同じ「%s」：%s' % (s, '・'.join(sorted(cs))))
    framed = [c for c in stills if c['frame'].startswith('額装')]
    fulls = [c for c in stills if c['frame'].startswith('全面')]
    kinds = Counter(c['kind'] for c in cuts)
    looks = Counter((c['look'] or c['kind']) for c in cuts if c['kind'] not in PHOTOISH + ('文字だけ',))
    changed = [c for c in cuts if c['changed']]
    heads = {}
    for c in cuts:
        heads.setdefault(c['chap'], c)
    card0 = [h['cid'] for ch, h in heads.items() if not ch.startswith('つかみ') and h['kind'] in ('実写', '参考') and 'SA' in h['rights']]
    eras = Counter(c['era'] for c in stills)

    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        # 🆕 ⑤b-1：末尾に cont（扉を除いた中身の秒）・card（頭の扉の秒）・src_len／rate（映像の素材の秒と倍率）＝前の列の並びは変えない
        w.writerow(['cid', 'chap', 'start', 'dur', 'kind', 'code', 'part', 'frame', 'sub', 'motion', 'view', 'look', 'signal', 'rights', 'era', 'people', 'credit', 'note', 'ga', 'ga_new',
                    'cont', 'card', 'src_len', 'rate'])
        for c in cuts:
            w.writerow([c['cid'], c['chap'], '%.2f' % c['start'], '%.2f' % c['dur'], c['kind'], c['code'], c['part'], c['frame'], c['sub'], c['motion'],
                        c['view'], c['look'], c['signal'], c['rights'], c['era'], c['people'], c['credit'], c['note'], c['ga'], c['ga_new'],
                        '%.2f' % c['cont'], '%.1f' % c['card'], '%.2f' % c['src_len'] if c['src_len'] is not None else '',
                        '%.3f' % c['rate'] if c['rate'] is not None else ''])

    L = ['---', 'title: 24本目 場面ごとの映像・写真の一覧（生成物）', 'created: 2026-10-22', 'tags: [project/jiko-kensho, ep24]', '---', '',
         '# 24本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % n, '',
         '> **生成物＝手で直さない**。作り方＝`python ref/ep24/eizou_build/make_list24.py`（入力＝台本 第2版 `daihon_v2.md` §4・当て方 `eizou_build/assign24.psv`・出どころ `eizou_build/sources24.psv`〈`make_sources24.py` が書く〉）。直すのは入力。',
         '> 秒＝%s（⑤b-1 から＝前 0.35＋声＋後 0.50・章の扉 2.0＝c2〜cc の頭の11枚）。🔧＝台本の画の欄から替えたカット。' % tnote + '色味は原本（10-07）。写真は画面いっぱい（10-11）＝例外は BY-SA（高さいっぱいの額装・切らない・色を変えない・寄らない＝額ごと動かす）と小さい写真（額装）。'
         '1986年の事故の動く記録映像は0本（【映像あり】は付けない）。見た画像の記録＝`eizou_build/seen24.tsv`。決めと確かめの正本＝Vault `Projects/事故検証-24本目-映像方針-20261022.md`。', '',
         '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真（この発電所・この事故）＋報告書の頁 | **%d カット＝%.1f%%**（写真 %d・頁 %d〈うち文字の頁 %d〉・秒 %.0f＝%.1f%%） | 20%%以上 %s |' % (
             len(photo) + len(pages), ratio * 100, len(photo), len(pages), sum(1 for c in pages if is_textonly(c)),
             sum(c['dur'] for c in photo + pages), sum(c['dur'] for c in photo + pages) / tot * 100, '✅' if ratio >= PHOTO_LO else '🔴'),
         '| 参考（同じ型のほかの発電所） | %d カット（20%% に数えない） | 副題で「同じ型の炉（〇〇原発）」と名乗る |' % len(ref_),
         '| フリー素材（イメージ） | %d カット（20%% に数えない） | 人なし・字なし・生成AIなし・「イメージ」と出す |' % len(stock),
         '| 写真の時期 | %s | 爆発の前の章に「後・今・跡」を置かない（門番） |' % '・'.join('%s %d' % (k or '—', v) for k, v in eras.most_common()),
         '| 全面／額装 | 全面 %d・額装 %d（%s） | 例外は了承② |' % (len(fulls), len(framed), '・'.join('%s %d' % (k, v) for k, v in Counter(c['frame'] for c in framed).most_common())),
         '| 文字だけ（パネル・文字の頁） | %d カット（%s）・続く最長 %d | できる限り0に近く |' % (len(text), '・'.join(c['cid'] for c in text), mx),
         '| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない＝⑤b はこの一覧に従う |' % len(changed),
         '| 種類 | %s | — |' % '・'.join('%s %d' % (k, v) for k, v in kinds.most_common()),
         '| 図の見た目の型 | %d 種（模式ほか %d カット） | 続く図で同じ型を続けない |' % (len(looks), sum(looks.values())),
         '| 静止写真の動き | %s | 寄るだけにしない（10-07） |' % '・'.join('%s %d' % (k, v) for k, v in mc.most_common()),
         '| 扉の地を方眼だけにする章（頭のカットが BY-SA） | %s | card_mix=0（⑤b） |' % ('・'.join(card0) or '—'),
         '| 合計 | %d カット・%s | — |' % (n, fmt_t(tot)), '']
    L += ['### 章ごと', '', '| 章 | カット | 秒 | 写真 | 頁 | 参考 | イメージ | 図 | 文字だけ |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = Counter(c['kind'] for c in cs)
        figs = len(cs) - sum(k[x] for x in PHOTOISH) - k['文字だけ']
        L.append('| %s | %d | %.0f | %d | %d | %d | %d | %d | %d |' % (ch, len(cs), sum(c['dur'] for c in cs), k['実写'], k['頁'], k['参考'], k['イメージ'], figs,
                                                               sum(1 for c in cs if is_textonly(c))))
    L += ['', '## §1 冒頭（c101〜c107）＝実写だけ（写真の動き・頁・今の映像）', '', '| カット | 秒 | 素材 | 見せ方・動き | 副題 | 語りの頭 |', '|---|---|---|---|---|---|']
    for c in cuts:
        if c['cid'] in OPENING:
            L.append('| %s | %.1f〜%.1f（%.1f） | %s%s | %s・%s | %s | %s |' % (
                c['cid'], c['start'], c['start'] + c['dur'], c['dur'], c['code'], (':' + c['part']) if c['part'] else '', c['frame'], c['motion'], c['sub'], c['first'][:24]))
    L += ['', '- 引き＝c104 の終わり %.1f秒（ひっくり返し）・c105 の終わり %.1f秒（46秒より前）・最初の見出しの手前 c107 の終わり %.1f秒' % tuple(
        next(c['start'] + c['dur'] for c in cuts if c['cid'] == x) for x in ('c104', 'c105', 'c107')), '']
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
                rem = (c['ga_new'] + ('｜' + c['note'] if c['note'] else '')) if c['ga_new'] else (c['ga'][:70] + ('…' if len(c['ga']) > 70 else '') + ('｜' + c['note'] if c['note'] else ''))
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
                                                                     s['rights'], s['basis'], s['credit'], s['era'], s['people'], s['note']))
    L += ['', '## §5 門番', '']
    L += ['- 🔴 E %d 件' % len(E)] + ['  - ' + e for e in E]
    L += ['- ⚠️ %d 件' % len(W)] + ['  - ' + w for w in W]
    L += ['', '### 使わないと決めた点（見て外した理由・sources24.psv に載せると E）', ''] + ['- %s＝%s' % kv for kv in NG.items()]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

    print('cuts=%d 写真=%d 頁=%d（%.1f%%） 参考=%d イメージ=%d 文字だけ=%d 🔧=%d 合計 %s' % (
        n, len(photo), len(pages), ratio * 100, len(ref_), len(stock), len(text), len(changed), fmt_t(tot)))
    print('種類：', dict(kinds))
    print('時期：', dict(eras))
    print('動き：', dict(mc))
    print('扉を方眼だけ：', card0)
    print('E %d・⚠️ %d' % (len(E), len(W)))
    for e in E:
        print('  E', e)
    for w in W:
        print('  ⚠️', w)
    print('→', OUT_MD)
    return 1 if E else 0


if __name__ == '__main__':
    sys.exit(main())
