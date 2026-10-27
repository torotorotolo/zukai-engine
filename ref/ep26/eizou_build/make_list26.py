# -*- coding: utf-8 -*-
"""26本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-10-27・チャット5）。25本目の make_list25.py を写して26本目の形に替えた。

  python -P ref/ep26/eizou_build/make_list26.py
  python -P ref/ep26/eizou_build/make_list26.py --selftest     （陽性・陰性の対照＝門番が鳴ることを先に見る）

入力：台本 第2版 ref/ep26/daihon_v2.md §4（画の欄・出典の欄・語り。語りは字数・秒に使う）
      eizou_build/assign26.psv（当て方・11列）・eizou_build/sources26.psv（出どころ＝手で書く入力）
出力：ref/ep26/eizou_list26.md（生成物＝手で直さない）・eizou_build/list26.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E 写真・頁・イメージ・衛星に素材の記号が無い／記号が sources26.psv に無い／使わないと決めた点（NG）が sources26.psv にある
  E 同じ点を2回（寄りの名が別のときだけ可）・同じ写真（実写）に別の副題・🆕 同じ写真の使い回しが上限をこえる（核の2点＝4回・ほか＝3回）
  E 🆕 衝突より前の場面（c201〜c415）に、時期「後・救助／後・NY／後・審問／海底」の写真（例外は理由つき）
  E 🆕 カリフォルニアン号ほかの写真の副題に、控えめな名乗りの語が無い（S8-625「とみられる」・S8-E03「とされる」・S2-E01「姉妹船オリンピック号」ほか）
  E 🆕 NOAA の映像・写真の副題に年と NOAA が無い
  E 🆕 台本の出典の欄が「書き起こし」のカットに、断り（kotowari）が無い（語らないカットは KOTO_SKIP に理由つき）
  E 🆕 額装の写真に動き（10-26 カズヤくん「写真が揺れる演出は…静止」＝26本目から）
  E 🆕 素材の注に「外」（名前・字を切り出しの外にする）があるのに、カットの備考に書き置きが無い
  E 🆕 「続き」の main が前のカットでない／衛星の素材が satellite でない
  E イメージの副題が「イメージ：」で始まらない／🆕 冒頭（c101〜c107）に実写と頁でない画（イメージも不可＝冒頭は実写）／写真と頁が 20% 未満／文字だけの画面が3つ続く
  E 図の型（模式・案C・写真・衛星・続きのほか）が全編で3回以上
  E 映像（NOAA・Pexels）の長さがカットの 0.6 倍に足りない／1.0 倍に足りないのに動きの欄に「映像（0.xx倍）」が無い（手元にあるときだけ測る）
  ⚠️ 続く図（あいだの写真は飛ばす・続きは飛ばす）で見た目の型が同じ／写真の無い画面が5つ以上続く／章の写真と頁が 20% 未満
  ⚠️ 別の写真なのに副題が同じ／静止写真の動きが「寄る」に偏る（50%超）／素材を見ていない（人の欄が「未見」）／🆕 同じ写真の2回が8カットより近い
秒＝audio/narration.json が26本目の台本と合えば実測（⑤b-1 から）・合わなければ ÷365 の見込み（出力に書く）。
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
NARR = os.path.join(REPO, 'audio', 'narration.json')
DAIHON = os.path.join(EP, 'daihon_v2.md')
OUT_MD = os.path.join(EP, 'eizou_list26.md')
OUT_TSV = os.path.join(HERE, 'list26.tsv')
ASSIGN = os.path.join(HERE, 'assign26.psv')
SOURCES = os.path.join(HERE, 'sources26.psv')
PUNCT = re.compile(r'[、。，．,.「」『』（）()？！?!…・\s　〈〉：:"“”]')   # m26 と同じ秒（c101〜c107 で突き合わせた）
CUT = re.compile(r'^\*\*(c[0-9a-d]\d{2})\*\*')
OPENING = ['c10%d' % i for i in range(1, 8)]
RATE = 365.0
RATE_MIN = 0.6          # 映像は 0.6 倍まで伸ばしてよい（footage の決まり）＝これ未満は止め絵になる
VIDEO_EXT = ('.mp4', '.webm', '.mkv', '.mov')
VIDEO_TYPES = ('stock', 'noaa-video')
PHOTO_LO = 0.20
PHOTOISH = ('実写', '頁', 'イメージ')
NOFIG = ('模式', '衛星', '続き', '文字だけ') + PHOTOISH      # 図の型の回数の門番に数えない種類
PRE_FROM, PRE_TO = 'c201', 'c415'          # 衝突（c405〜c415＝11時40分）までの場面
PRE_ERAS = ('後・救助', '後・NY', '後・審問', '海底')
ORDER = '123456789abcd'
CAP_CORE = {'S8-625': 4, 'S3-675': 4}      # 核の2点（この回の芯の船と人）
CAP = 3
GAP_MIN = 8
# 衝突の前の場面の門番の例外（語りが事故の前の場面ではない理由つき）
PRE_OK = {'c323': '語りは米国上院の公聴会での証言（G7 p.739）＝場面は公聴会',
          'c405': '見張り本人の肖像（審問のころの写真）＝場面の写真ではない（衝突の場面は c406〜c411 の模式）'}
# 書き起こしを出典に持つが、書き起こしの言葉を語らないカット（断りは要らない）
KOTO_SKIP = {'c502': '語りは G1 p.54・G7 p.23 の事実（書き起こし Q15391 の言葉は語らない）',
             'c635': '語りは G1 p.59 の事実（書き起こし Q7288 の「half awake」は語らない）'}
# 控えめな名乗り（置き場の説明が弱い・別の物）の語＝副題に必ず入れる
HEDGE = {'S8-625': 'とみられる', 'S8-E03': 'とされる', 'S2-E01': '姉妹船オリンピック号', 'S2-206': 'とされる',
         'S10-905': '見立て', 'S10-871': '見立て', 'S5-362': '本は書く', 'S5-359': '現場の近く'}
# 使わないと決めた点（見て外した理由）＝ sources26.psv に載せたら E
NG = {'S1-036': '沈没のあとの着色の絵はがき（WRECKED IN MID-ATLANTIC の焼き込み・オリンピック号の写真の流用の恐れ）',
      'S5-363': '衝突の前の日付と「Copyright」の書き込み（競売の品）',
      'S6-378': '遺体の回収の場面（オセアニック号が見つけた折りたたみ艇 A）',
      'S11-911': 'NOAA の頁で「Image copyright ［撮影者］/National Geographic」の3点のどれかの見込み',
      'S4-322': '乗客の顔写真と名前の並ぶ1面',
      'S12-471': '海の中の人を描く風刺画',
      'S9-646': '会社の人の名前が絵に焼き込まれた似顔絵',
      'S8-629': '年の分からない油絵（競売の品）', 'S8-634': '着色の絵はがき',
      'S3-E02': '163×245 の小さすぎる顔写真',
      'S1-069': 'S1-032 と同じ写真（説明の港が食い違う＝使う側は S1-032）', 'S1-008': 'S1-013 と同じ写真',
      'S8-624': 'S8-625 と同じ写真', 'S4-313': 'S4-228 と同じ書類', 'S2-213': 'S2-206 を手直しした版', 'S6-561': 'S6-384 と同じ写真',
      'S6-384': 'カルパチア号に吊り上げたボート（後の場面）＝語りの「下ろす」場面に合わない（c519 は替えた）',
      'S1-050': '真横の全身（nl.wikipedia からの移し・出どころ弱い）＝10-27 に 1920px の版で A 甲板の前半の窓を見たがオリンピック号と見分けきれない（c920 は S1-089 に替えた・ファイルは src/eizou/_使わない/）',
      'GAUMONT':'ゴーモンのニュース映画（Commons「Titanic Disaster - Genuine Footage」）＝会社（British Pathé）が権利を主張'}
# 映像方針で決めたこと（台本 §0-5 の答え・一覧の §6 に出す）
DECIDED = [
    '承認①（第2版 §0-4）＝10-27 カズヤくん「推奨どおり承認」（7項目とも）＝v2_head.md の2行だけ直して組み直した（`e84f5f33`・語りと画の欄は変わらない）',
    '了承②＝10-27 カズヤくん（4問とも推奨どおり）＝①取る素材（Commons 70点＝🆕6点を含む・Pexels 8カットは ⑤b で1本ずつ）②地図は衛星写真＋描き足し（外洋も）③見せ方（全面が既定・額装は静止・全面のゆっくり寄る／流すは続ける）と人の写り（乗客は遠景と後ろ姿・顔が分かれば顔だけモザイク）④クレジット・案C の形のもと（🆕案C-9）・NOAA の映像は【映像あり】に数えない・LOC の映像の目録は見ない',
    '冒頭（c101〜c107）＝実写だけ。c107 は Pexels の夜の海（イメージ）→ NOAA 2004 の船首の正面の映像（冒頭は実写＝この事故の物だけ）。流れ＝出航（4月10日）→ カリフォルニアン号 → 現場の近くの氷山 → 朝の海のボート → 海の底の船首（80年後）→ カルパチア号の乗客が撮ったカリフォルニアン号 → 海の底の船首の正面（問い）',
    'NOAA 2004 の映像（5分53秒）＝16コマを原寸で見た：全編が海の底の残骸・字の焼き込みも人も無い・0〜9.5秒と346秒〜は黒。区間は13＝どれも別の場面（船首の手すり・船首の正面・船首の横・舷側の手すり・甲板の縁・前甲板の巻き上げ機と錨の鎖・甲板・船室の窓・甲板の構造物2か所・明るい甲板・暗い構造物2か所）。音は使わない。秒は ⑤b-1 で実測に合わせて動かす',
    '書き起こしの断り＝副題とは別の行（出典の札）に「証言の言葉は英国の審問の書き起こし（有志のサイト）による」／「米国上院の報告の文は書き起こし（有志のサイト）による・公式の写しは未照合」。台本 §0-5 の13か所＋機械で拾った c603（札の緯度経度）・c621。c502・c635 は書き起こしの言葉を語らない＝要らない。c823 は MAIB p.15（書き起こしでない）＝要らない',
    '原寸で字を確かめた（10-27・見た画像は seen26e.tsv）＝c214 見出し「THE VESSEL UNSINKABLE.」（名前の行 y286〜 は切り出しの外・肩書は International Mercantile Marine Company の vice president）／c305「At 12.35 a.m. (ship\'s time) April 15th (Monday), 1912」／c507「We are sinking fast passengers being put into boats」（画面に SOS も写る＝語りでは言わない）／c703「NEW YORK, MONDAY, APRIL 15, 1912」／c205 船尾の「TITANIC」「LIVERPOOL」／c819 ネガの字は上の帯（y0〜450）／🆕 アメリカ号の電報（S4-N06）は本物の受信の用紙＝c309 に入れ、日報（衝突の行とアメリカ号の「TITANIC (Br ss)」の行）は c310 へ入れ替えた',
    'オリンピック号との見分け＝S1-032（c213）は撮影者がタイタニック号の乗客という来歴でよい／S1-050 は 1920px の版で見分けきれず出どころも弱い＝使わない（c920 は試運転の日の S1-089 の別の寄り）',
    'c509＝副題の2号艇と語りの7号艇の食い違い → ボート甲板の写真の寄り（番号を名乗らない）。2号艇の写真（置き場の説明）は c518（2号艇の語り）へ',
    'c519＝カルパチア号に吊り上げたボート（後の場面）→ ボート甲板の寄り（語り＝下ろす場面）。S6-384 は使わない点に',
    'c601〜c641 の副題＝写っているものに（S8-625 は NARA の「とみられる」・S8-E03 は「とされる」・S2-E01 は「姉妹船オリンピック号」と断る・S3-749 は「1908年・別の船の船長だったころ」）',
    'c703＝4月15日の第一報（見出しは「沈みかけ」）＝語りの2時20分の沈没と矛盾しない（紙面の日付は原寸で）／c717＝4月20日の写真は「着いた」日でない → ニューヨーク着の夜（4月18日）の写真に替え、4月20日の写真は c808 で「着いた」と言わない副題に',
    'c819＝ネガの字（議員の名）は切り出しの外（語りは役職だけ・タイタニック号の船長と名字が同じで紛れる）',
    'c512＝モールス灯は船橋の脇の屋根の上に描く（G1 p.16・p.54）／c637＝1:10ごろ と 2:40ごろ に〈二等航海士の話〉の札／c916＝船長の写真の2回目（緑の灯の向きは c710 の模式で見せた）／ca04＝亡くなった通信士の肖像に条文を重ねない → 模式／c209＝札は語りの呼び方（大きなボート・小さめのボート）',
    'c911（聞き役の1行だけ）＝c910 の図の続き（「2人とも同じ」の札を足す）／c821→c822 の模式の続き＝c821 を公聴会の絵の寄りに替えて切った',
    '写真の使い回し（W 25）＝上限を決めた（核の2点＝4回・ほか3回・毎回寄りを替える）＝S8-625 9→4・S3-675 7→4・S8-E03 7→3・S6-480 5→3・S10-905 3→2・S1-084 3→2・S5-359 3→1・S3-753 3→2・S8-630 3→3。替えた先＝NOAA の映像の別の区間・語りの船の写真（🆕 バルティック号・メサバ号・カルパチア号・マウント・テンプル号・1905年の桟橋・アメリカ号の電報）・案C（🆕 案C-9＝伝声管の前の二等航海士）・模式',
    '案C＝{c0} 場面（台本 13）。案C-1 の2回目（c615）と案C-2 の2回目（c631）は前のカットの続き。案C-6 は c713 → c712（記録 4時10分）。🆕 案C-9（c633・c936＝伝声管の前に立つ二等航海士・2時40分ごろと1時10分ごろ）',
    '地図（c218・c306・c909・c917）＝衛星写真＋描き足し（了承②の2択＝外洋は一面の海）。c505 の航路は模式のまま（地図でなく向きの図）',
    '括弧の英単位＝図の札はキロ（km）と時速のキロだけ（マイル・ノットは札に出さない）。語りで括弧を読むかは ⑤a で1つに決める（台本 §6・G7-057）',
    '写真は画面いっぱいが既定。例外＝縦長の写真と縦長・正方形の紙面（高さいっぱいの額）・横長のマウント・テンプル号（幅いっぱいの額）・MAIB の頁（引用の型＝無加工の額）＝どれも静止（10-26）。全面の写真のゆっくり寄る・流すは続ける（了承②）',
    '模式 {m0} → {m1}・フリー素材（イメージ）{x0} → {x1}（c107・c911 を外し、c638 夜明け前の海・c939 流れ星を足した）',
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
            cur = dict(cid=m.group(1), chap=chap, ga=parts[1].strip() if len(parts) > 1 else '',
                       src=parts[2].strip() if len(parts) > 2 else '', n=0, first='', text='')
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
    return rows


def measured(rows):
    """秒を audio/narration.json の実測に（25本目 make_list25.measured() の型）。26本目の台本と合わないときは ÷365 の見込みのまま"""
    if not os.path.exists(NARR):
        return '÷365 の見込み（narration.json が無い）'
    dur = json.load(open(NARR, encoding='utf-8')).get('durations', {})
    if [r['cid'] for r in rows] != [c for c in dur if c != 'ed01']:
        return '÷365 の見込み（narration.json は26本目の台本と合わない＝⑤a の前）'
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    import check_script as CSC
    sec, prev = 0.0, None
    for r in rows:
        key = CSC.door_key(r['cid'], slug='ep26')
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
    if mo.startswith('静止'):
        return '静止'
    pre = '額の中で' if mo.startswith('額の中で') else ''
    for key, name in (('引', '引く'), ('左へ', '左へ'), ('右へ', '右へ'), ('上へ', '上へ'), ('下へ', '下へ'), ('寄', '寄る')):
        if key in mo:
            return pre + name
    return mo


def fmt_t(s):
    return '%d:%04.1f' % (s // 60, s % 60)


def is_textonly(c):
    return c['kind'] == '文字だけ' or (c['kind'] == '頁' and c['look'].startswith('文字'))


def is_picture(c):
    """写真の無い画面が続く所の数え＝実写・イメージ・衛星・図の頁（文字の頁は数えない）"""
    return c['kind'] in ('実写', 'イメージ', '衛星') or (c['kind'] == '頁' and not is_textonly(c))


KEYS = ['cid', 'kind', 'main', 'frame', 'sub', 'motion', 'view', 'look', 'ga_new', 'note', 'kotowari']


def build(assign_path=ASSIGN, sources_path=SOURCES, daihon=DAIHON):
    cuts = read_cuts(daihon)
    tnote = measured(cuts)
    E, W = [], []
    assign = {}
    for r in [ln.split('|') for ln in read_psv(assign_path)]:
        if len(r) != len(KEYS):
            E.append('assign26.psv の列の数が %d でない行：%s（%d列）' % (len(KEYS), r[0], len(r)))
            continue
        if r[0] in assign:
            E.append('assign26.psv に同じカットの行が2つ：%s' % r[0])
        assign[r[0]] = dict(zip(KEYS, [x.strip() for x in r]))
    known = {c['cid'] for c in cuts}
    for k in assign:
        if k not in known:
            E.append('assign26.psv のカット %s が台本に無い' % k)
    srows = read_psv(sources_path)
    shead = srows[0].split('|')
    sources = {}
    for r in srows[1:]:
        f = r.split('|')
        if len(f) != len(shead):
            E.append('sources26.psv の列の数が %d でない行：%s（%d列）' % (len(shead), f[0], len(f)))
            continue
        if f[0] in sources:
            E.append('sources26.psv に同じ記号の行が2つ：%s' % f[0])
        sources[f[0]] = dict(zip(shead, f))
    for code in sources:
        if code in NG:
            E.append('使わない点が sources26.psv にある：%s（%s）' % (code, NG[code]))

    prev = None
    for c in cuts:
        a = assign.get(c['cid'], {})
        c['kind0'] = base_kind(c['ga'])
        for k in KEYS[1:]:
            c[k] = a.get(k, '')
        c['kind'] = c['kind'] or c['kind0']
        c['changed'] = '🔧' in c['note'] or '🔧' in c['ga_new']
        if c['cid'] not in assign:
            W.append('%s assign26.psv に行が無い（台本の画の欄のまま）' % c['cid'])
        if c['kind'] == '続き' and (not prev or c['main'] != prev['cid']):
            E.append('%s 「続き」の main（%s）が前のカット（%s）でない' % (c['cid'], c['main'], prev['cid'] if prev else '—'))
        if c['kind'] == '続き':
            c['look'] = c['look'] or '（%s の続き）' % c['main']
        # 書き起こしの断り
        if '書き起こし' in c['src']:
            if c['cid'] in KOTO_SKIP:
                if c['kotowari']:
                    W.append('%s 断りが要らない（KOTO_SKIP）のに断りがある' % c['cid'])
            elif '書き起こし' not in c['kotowari']:
                E.append('%s 出典の欄が「書き起こし」なのに断り（kotowari）が無い' % c['cid'])
        elif c['kotowari']:
            W.append('%s 出典の欄に「書き起こし」が無いのに断りがある（%s）' % (c['cid'], c['kotowari']))
        prev = c

    use = defaultdict(list)
    for c in cuts:
        c['code'] = c['part'] = c['rights'] = c['credit'] = c['era'] = c['people'] = c['get'] = c['stype'] = ''
        c['src_len'] = c['rate'] = None
        if c['kind'] not in PHOTOISH + ('衛星',):
            continue
        if not c['main']:
            E.append('%s %s なのに素材の記号が無い' % (c['cid'], c['kind']))
            continue
        code, part = (c['main'].split(':', 1) + [''])[:2]
        s = sources.get(code)
        if not s:
            E.append('%s 記号 %s が sources26.psv に無い' % (c['cid'], code))
            continue
        c.update(code=code, part=part, rights=s['rights'], credit=s['credit'], era=s['era'], people=s['people'], get=s['get'], stype=s['type'])
        if c['kind'] == '衛星' and s['type'] != 'satellite':
            E.append('%s 衛星のカットの素材 %s が satellite でない（%s）' % (c['cid'], code, s['type']))
        if s['type'] in VIDEO_TYPES:
            have = media_len(s['file']) if s['file'].lower().endswith(VIDEO_EXT) else None
            m = re.search(r'(\d+(?:\.\d+)?)〜(\d+(?:\.\d+)?)秒', c['motion'])
            if have is not None and m:
                if float(m.group(2)) > have + 0.01:
                    E.append('%s 映像の区間 %s〜%s秒 が素材の長さ %.2f秒 をこえる' % (c['cid'], m.group(1), m.group(2), have))
                have = float(m.group(2)) - float(m.group(1))
            if have is None:
                W.append('%s 映像の素材 %s が手元に無い（置き場の欄＝%s）＝長さを測れない（⑤b で取ってから測る）' % (c['cid'], code, s['file'] or '空'))
            else:
                den = c['cont']
                c['src_len'] = have
                c['rate'] = have / den if den else 0
                mr = re.search(r'映像（[^）]*?(\d\.\d+)倍）', c['motion'])
                if c['rate'] < RATE_MIN:
                    E.append('%s 映像 %.2f秒 ÷ カット %.2f秒 ＝ %.2f倍 ＜ %.1f（止め絵になる・素材か区間を替える）' % (c['cid'], have, den, c['rate'], RATE_MIN))
                elif c['rate'] < 1.0 and not (mr and float(mr.group(1)) <= c['rate'] + 1e-9):
                    E.append('%s 映像 %.2f秒 がカット %.2f秒 に足りない（等速なら尻が %.2f秒 欠ける）＝区間か素材を替えるか、動きの欄を「映像（%.2f倍）」以下に' % (
                        c['cid'], have, den, den - have, int(c['rate'] * 100) / 100))
        use[code].append(c)
        if 'SA' in s['rights'] and not c['frame'].startswith('額装'):
            E.append('%s BY-SA の %s が額装でない（%s）' % (c['cid'], code, c['frame']))
        if c['kind'] == 'イメージ' and not c['sub'].startswith('イメージ：'):
            E.append('%s イメージの副題が「イメージ：」で始まらない（%s）' % (c['cid'], c['sub']))
        if code in HEDGE and HEDGE[code] not in c['sub']:
            E.append('%s %s の副題に控えめな名乗りの語「%s」が無い（%s）' % (c['cid'], code, HEDGE[code], c['sub']))
        if code == 'N04' and not ('2004年' in c['sub'] and 'NOAA' in c['sub']):
            E.append('%s NOAA 2004 の映像の副題に「2004年」と「NOAA」が無い（%s）' % (c['cid'], c['sub']))
        if code.startswith('S11-') and not ('2003年' in c['sub'] and 'NOAA' in c['sub']):
            E.append('%s NOAA 2003 の写真の副題に「2003年」と「NOAA」が無い（%s）' % (c['cid'], c['sub']))
        if c['frame'].startswith('額装') and motion_class(c['motion']) != '静止':
            E.append('%s 額装の写真に動き（%s）＝額装は静止（10-26）' % (c['cid'], c['motion']))
        if '外' in s['note'] and ('名前' in s['note'] or '字' in s['note']) and '外' not in (c['note'] + c['ga_new']):
            E.append('%s 素材 %s は名前・字を切り出しの外にする点なのに、カットに書き置きが無い' % (c['cid'], code))
        if ckey(PRE_FROM) <= ckey(c['cid']) <= ckey(PRE_TO) and s['era'] in PRE_ERAS:
            if c['cid'] in PRE_OK:
                c['note'] = (c['note'] + '｜' if c['note'] else '') + '時期の門番の例外＝' + PRE_OK[c['cid']]
            else:
                E.append('%s 衝突より前の場面（%s〜%s）に、時期「%s」の写真 %s（%s）' % (c['cid'], PRE_FROM, PRE_TO, s['era'], code, c['sub']))
        if s['people'] == '未見':
            W.append('%s 素材 %s の人の写りが未見（⑤b で原寸）' % (c['cid'], code))

    order = {c['cid']: i for i, c in enumerate(cuts)}
    for code, us in sorted(use.items()):
        if len(us) > 1:
            parts = [u['part'] for u in us]
            if not (all(parts) and len(set(parts)) == len(parts)):
                E.append('点 %s を2回使う：%s（寄りの名を分ける）' % (code, '・'.join(u['cid'] for u in us)))
            if us[0]['kind'] == '実写' and us[0]['stype'] == 'commons-photo' and len({u['sub'] for u in us}) > 1:
                E.append('同じ写真 %s に別の副題：%s' % (code, ' ／ '.join('%s「%s」' % (u['cid'], u['sub']) for u in us)))
            if us[0]['stype'] == 'commons-photo':
                cap = CAP_CORE.get(code, CAP)
                if len(us) > cap:
                    E.append('写真 %s を %d 回（上限 %d）：%s' % (code, len(us), cap, '・'.join(u['cid'] for u in us)))
                for a, b in zip(us, us[1:]):
                    if order[b['cid']] - order[a['cid']] < GAP_MIN:
                        W.append('同じ写真 %s の2回が近い（%s→%s・%dカット）' % (code, a['cid'], b['cid'], order[b['cid']] - order[a['cid']]))
    for c in cuts:
        if c['cid'] in OPENING and c['kind'] not in ('実写', '頁'):
            E.append('%s 冒頭に実写・頁でない画（%s）＝冒頭は実写' % (c['cid'], c['kind']))

    tc = Counter(c['kind'] for c in cuts if c['kind'] not in NOFIG)
    for k, v in tc.items():
        if v > 2:
            E.append('図の型「%s」が %d 回（2回まで）' % (k, v))
    prev = None
    for c in cuts:
        if c['kind'] in PHOTOISH + ('衛星', '続き'):
            continue
        lk = c['look'] or c['kind']
        if prev and prev[1] == lk:
            W.append('続く図で見た目の型が同じ（%s）：%s→%s' % (lk, prev[0], c['cid']))
        prev = (c['cid'], lk)
    run, start = 0, None
    for c in cuts + [dict(cid='end', kind='実写', look='')]:
        if c['kind'] == '続き':
            continue
        if is_picture(c):
            if run >= 5:
                W.append('写真の無い画面が %d つ続く：%s〜' % (run, start))
            run, start = 0, None
        else:
            run += 1
            start = start or c['cid']
    last = None
    for c in cuts:
        c['signal'] = ''
        if c['view'] and c['kind'] not in PHOTOISH + ('続き',):
            if last and last[1] != c['view']:
                c['signal'] = '🔁 %s→%s（前の図 %s）' % (last[1], c['view'], last[0])
            last = (c['cid'], c['view'])

    n = len(cuts)
    tot = sum(c['dur'] for c in cuts)
    photo = [c for c in cuts if c['kind'] == '実写']
    stock = [c for c in cuts if c['kind'] == 'イメージ']
    pages = [c for c in cuts if c['kind'] == '頁']
    sat = [c for c in cuts if c['kind'] == '衛星']
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
    stills = [c for c in photo if c['stype'] == 'commons-photo']
    mc = Counter(motion_class(c['motion']) for c in stills)
    yoru = sum(v for k, v in mc.items() if k.endswith('寄る'))
    moving = sum(v for k, v in mc.items() if k != '静止')
    if moving and yoru / moving > 0.5:
        W.append('静止写真の動きが「寄る」に偏る（%d/%d）' % (yoru, moving))
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
                sat=sat, ratio=ratio, mx=mx, mc=mc, tnote=tnote, use=use)


def write(r):
    cuts, E, W, sources, chaps = r['cuts'], r['E'], r['W'], r['sources'], r['chaps']
    n, tot, photo, stock, pages, text, ratio, mx, mc = r['n'], r['tot'], r['photo'], r['stock'], r['pages'], r['text'], r['ratio'], r['mx'], r['mc']
    framed = [c for c in photo if c['frame'].startswith('額装')]
    fulls = [c for c in photo if c['frame'].startswith('全面')]
    videos = [c for c in photo if c['frame'].startswith('映像')]
    kinds = Counter(c['kind'] for c in cuts)
    looks = Counter((c['look'] or c['kind']) for c in cuts if c['kind'] not in PHOTOISH + ('文字だけ',))
    changed = [c for c in cuts if c['changed']]
    eras = Counter(c['era'] for c in photo)
    figs = [c for c in cuts if c['kind'] not in PHOTOISH + ('文字だけ', '衛星')]
    koto = [c for c in cuts if c['kotowari']]
    anc = sorted({c['kind'] for c in cuts if c['kind'].startswith('案C')})
    reuse = sorted(((code, us) for code, us in r['use'].items() if len(us) > 1 and us[0]['stype'] == 'commons-photo'), key=lambda kv: -len(kv[1]))

    with open(OUT_TSV, 'w', encoding='utf-8', newline='\n') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['cid', 'chap', 'start', 'dur', 'kind', 'code', 'part', 'frame', 'sub', 'motion', 'view', 'look', 'signal', 'rights', 'era', 'people',
                    'credit', 'note', 'ga', 'ga_new', 'get', 'cont', 'card', 'src_len', 'rate', 'kotowari'])
        for c in cuts:
            w.writerow([c['cid'], c['chap'], '%.2f' % c['start'], '%.2f' % c['dur'], c['kind'], c['code'], c['part'], c['frame'], c['sub'], c['motion'],
                        c['view'], c['look'], c['signal'], c['rights'], c['era'], c['people'], c['credit'], c['note'], c['ga'], c['ga_new'], c['get'],
                        '%.2f' % c['cont'], '%.1f' % c['card'], '%.2f' % c['src_len'] if c['src_len'] is not None else '',
                        '%.3f' % c['rate'] if c['rate'] is not None else '', c['kotowari']])

    L = ['---', 'title: 26本目 場面ごとの映像・写真の一覧（生成物）', 'created: 2026-10-27', 'tags: [project/jiko-kensho, ep26]', '---', '',
         '# 26本目 場面ごとの映像・写真の一覧（%dカット・映像方針）' % n, '',
         '> **生成物＝手で直さない**。作り方＝`python -P ref/ep26/eizou_build/make_list26.py`（入力＝台本 第2版 `daihon_v2.md` §4・当て方 `eizou_build/assign26.psv`・出どころ `eizou_build/sources26.psv`）。直すのは入力。',
         '> 秒＝%s。🔧＝台本の画の欄から替えたカット（⑤b はこの一覧に従う・台本は直さない）。' % r['tnote'] +
         '色味は原本（10-07）。写真は画面いっぱい（10-11）＝例外は縦長・紙面（高さいっぱいの額）と横長のマウント・テンプル号（幅いっぱいの額）と MAIB の頁（引用の型）＝額装はどれも静止（10-26）。'
         '1912年の出来事の動く記録映像は0本（【映像あり】は付けない）＝動く実写は NOAA 2004 の残骸の映像だけ。見た画像の記録＝`eizou_build/seen26e.tsv`。'
         '書き起こしの断りは副題と別の行（出典の札）＝表の「断り」の列。', '',
         '## §0 数', '', '| 物差し | 値 | 決まり |', '|---|---|---|',
         '| 写真（この事故・船・人・紙面・残骸）＋報告書などの頁 | **%d カット＝%.1f%%**（実写 %d〈うち NOAA の映像 %d〉・頁 %d〈うち文字の頁 %d〉・秒 %.0f＝%.1f%%） | 20%%以上 %s |' % (
             len(photo) + len(pages), ratio * 100, len(photo), len(videos), len(pages), sum(1 for c in pages if is_textonly(c)),
             sum(c['dur'] for c in photo + pages), sum(c['dur'] for c in photo + pages) / tot * 100, '✅' if ratio >= PHOTO_LO else '🔴'),
         '| フリー素材（イメージ） | %d カット（20%% に数えない） | 人の顔なし・字なし・生成AIなし・月の写らないもの・「イメージ」と出す・⑤b で1本ずつ原寸 |' % len(stock),
         '| 衛星写真（地図） | %d カット（20%% に数えない） | 帰属の行を出し続ける・色を変えない・⑤b-1 で撮る |' % len(r['sat']),
         '| 写真の時期 | %s | 衝突より前の場面（c201〜c415）に「後」と「海底」を置かない（門番） |' % '・'.join('%s %d' % (k or '—', v) for k, v in eras.most_common()),
         '| 全面／額装／映像 | 全面 %d・額装 %d（%s）・映像 %d | 額装は静止（10-26）・例外は了承② |' % (
             len(fulls), len(framed), '・'.join('%s %d' % (k, v) for k, v in Counter(c['frame'] for c in framed).most_common()) or '—', len(videos)),
         '| 文字だけ（文字の頁） | %d カット（%s）・続く最長 %d | できる限り0に近く・3つ続けない |' % (len(text), '・'.join(c['cid'] for c in text), mx),
         '| 図（模式・案C・型の図・続き） | %d カット（模式 %d・案C %d〈%d 場面〉・続き %d） | 続く図で同じ見た目にしない |' % (
             len(figs), sum(1 for c in figs if c['kind'] == '模式'), sum(1 for c in figs if c['kind'].startswith('案C')), len(anc),
             sum(1 for c in figs if c['kind'] == '続き')),
         '| 書き起こしの断り | %d カット（%s） | 副題と別の行（出典の札） |' % (len(koto), '・'.join(c['cid'] for c in koto)),
         '| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない＝⑤b はこの一覧に従う |' % len(changed),
         '| 種類 | %s | — |' % '・'.join('%s %d' % (k, v) for k, v in kinds.most_common()),
         '| 図の見た目の型 | %d 種（%d カット） | — |' % (len(looks), sum(looks.values())),
         '| 静止写真の動き | %s | 寄るだけにしない（10-07）・額装は静止（10-26） |' % '・'.join('%s %d' % (k, v) for k, v in mc.most_common()),
         '| 合計 | %d カット・%s | — |' % (n, fmt_t(tot)), '']
    L += ['### 章ごと', '', '| 章 | カット | 秒 | 写真 | 頁 | イメージ | 衛星 | 図 | 文字だけ |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for ch in chaps:
        cs = [c for c in cuts if c['chap'] == ch]
        k = Counter(c['kind'] for c in cs)
        nf = len(cs) - sum(k[x] for x in PHOTOISH) - k['文字だけ'] - k['衛星']
        L.append('| %s | %d | %.0f | %d | %d | %d | %d | %d | %d |' % (ch, len(cs), sum(c['dur'] for c in cs), k['実写'], k['頁'], k['イメージ'], k['衛星'], nf,
                                                                  sum(1 for c in cs if is_textonly(c))))
    L += ['', '### 写真の使い回し（2回以上・上限＝核の2点 4回・ほか 3回）', '', '| 写真 | 回数 | カット（寄りの名） |', '|---|---:|---|']
    for code, us in reuse:
        L.append('| %s | %d | %s |' % (code, len(us), '・'.join('%s（%s）' % (u['cid'], u['part']) for u in us)))
    n04 = r['use'].get('N04', [])
    L += ['', '- NOAA 2004 の映像の区間＝%s' % ('・'.join('%s %s（%s）' % (u['cid'], u['part'], re.sub(r'^映像（|）$', '', u['motion'])) for u in n04) or '—'), '']
    L += ['## §1 冒頭（c101〜c107）＝実写だけ（最初に設計した）', '', '| カット | 秒 | 素材 | 見せ方・動き | 副題 | 語りの頭 |', '|---|---|---|---|---|---|']
    for c in cuts:
        if c['cid'] in OPENING:
            L.append('| %s | %.1f〜%.1f（%.1f） | %s%s | %s・%s | %s | %s |' % (
                c['cid'], c['start'], c['start'] + c['dur'], c['dur'], c['code'], (':' + c['part']) if c['part'] else '', c['frame'], c['motion'], c['sub'],
                c['first'][:24]))
    L += ['', '- 最初の聞き役 c104 の頭 %.1f秒・引き（1992年に割れた）c105 の終わり %.1f秒（46秒より前）・2人の見方 c106 の終わり %.1f秒・最初の見出しの手前 c107 の終わり %.1f秒' % tuple(
        [next(c['start'] for c in cuts if c['cid'] == 'c104')] + [next(c['start'] + c['dur'] for c in cuts if c['cid'] == x) for x in ('c105', 'c106', 'c107')]),
          '- 流れ＝出航するタイタニック号（4月10日）→ 北の方のカリフォルニアン号 → 現場の近くの氷山（1,490人）→ 朝の海のボート（1912年の結論）→ 海の底の船首（80年後に割れた）→ カルパチア号の乗客が撮ったカリフォルニアン号（2人の見方）→ 海の底の船首の正面（この動画の問い）。再現イラスト・図・イメージは置かない・事故の瞬間は描かない', '']
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
              '| カット | 秒 | 種類 | 素材 | 見せ方 | 副題 | 動き | 見る向き・見た目 | 権利・時期・人 | 断り（出典の札） | 画（替えたカットは新しい画）・備考 |',
              '|---|---|---|---|---|---|---|---|---|---|---|']
        for c in cs:
            mat = (c['code'] + ((':' + c['part']) if c['part'] else '')) if c['code'] else (c['main'] if c['kind'] == '続き' else '')
            vl = '・'.join(x for x in (c['view'], c['look']) if x) + ((' ' + c['signal']) if c['signal'] else '')
            rp = '・'.join(x for x in ((c['rights'].split('（')[0] if c['rights'] else ''), c['era'], c['people']) if x)
            if c['kind'] in PHOTOISH + ('衛星',):
                rem = (c['ga_new'] + '｜' if c['ga_new'] else '') + c['note']
            else:
                rem = (c['ga_new'] + ('｜' + c['note'] if c['note'] else '')) if c['ga_new'] and c['ga_new'] != '台本どおり' else (
                    c['ga'][:70] + ('…' if len(c['ga']) > 70 else '') + ('｜' + c['note'] if c['note'] else ''))
            L.append('| %s%s | %.1f（%.1f） | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
                c['cid'], ' 🔧' if c['changed'] else '', c['start'], c['dur'], c['kind'], mat or '—', c['frame'] or '—', c['sub'] or '—',
                c['motion'] or '—', vl or '—', rp or '—', c['kotowari'] or '—', rem.replace('|', '／')))
        L.append('')
    L += ['## §4 素材の一覧（了承②の対象）', '', '| 記号 | 当てたカット | 種類 | 取り方 | 置き場（git の外） | 大きさ | 権利・根拠 | 出典の表記（下書き） | 時期・人 | 何 |',
          '|---|---|---|---|---|---|---|---|---|---|']
    used_by = defaultdict(list)
    for c in cuts:
        if c['code']:
            used_by[c['code']].append(c['cid'] + ((':' + c['part']) if c['part'] else ''))
    for code, s in sources.items():
        L.append('| %s | %s | %s | %s | `%s` | %s | %s（%s） | %s | %s・%s | %s |' % (code, '・'.join(used_by.get(code, [])) or '（控え）', s['type'], s['get'], s['file'],
                                                                          s['dims'], s['rights'], s['basis'], s['credit'], s['era'], s['people'], s['title']))
    L += ['', '## §5 門番', '']
    L += ['- 🔴 E %d 件' % len(E)] + ['  - ' + e for e in E]
    L += ['- ⚠️ %d 件' % len(W)] + ['  - ' + w for w in W]
    L += ['', '### 使わないと決めた点（見て外した理由・sources26.psv に載せると E）', ''] + ['- %s＝%s' % kv for kv in NG.items()]
    cnt = dict(m0=sum(1 for c in cuts if c['kind0'] == '模式'), m1=sum(1 for c in cuts if c['kind'] == '模式'),
               x0=sum(1 for c in cuts if c['kind0'] == 'イメージ'), x1=len(stock), c0=len(anc))
    L += ['', '## §6 映像方針で決めたこと（台本 §0-5 の答え・10-27）', ''] + ['%d. %s' % (i + 1, d.format(**cnt)) for i, d in enumerate(DECIDED)]
    open(OUT_MD, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

    print('cuts=%d 実写=%d（映像 %d） 頁=%d（%.1f%%） イメージ=%d 衛星=%d 文字だけ=%d 図=%d（模式 %d） 断り=%d 🔧=%d 合計 %s' % (
        n, len(photo), len(videos), len(pages), ratio * 100, len(stock), len(r['sat']), len(text), len(figs), sum(1 for c in figs if c['kind'] == '模式'),
        len(koto), len(changed), fmt_t(tot)))
    print('種類：', dict(kinds))
    print('時期：', dict(eras))
    print('動き：', dict(mc))
    print('使い回し：', ' '.join('%s×%d' % (code, len(us)) for code, us in reuse))
    print('秒：', r['tnote'], '・c105 の終わり %.1f・c106 %.1f・c107 %.1f' % tuple(
        next(c['start'] + c['dur'] for c in cuts if c['cid'] == x) for x in ('c105', 'c106', 'c107')))
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

    def put(rows_, cid, col, val):
        out = []
        for r in rows_:
            f = r.split('|')
            if f[0] == cid:
                f[KEYS.index(col)] = val
                r = '|'.join(f)
            out.append(r)
        return out

    checks = []
    # ① 衝突の前の場面（c213）に救助の朝の写真（S6-480）
    a1 = put(put(rows, 'c213', 'main', 'S6-480:試し'), 'c213', 'sub', '4月15日の朝、海の上のボート〈1912年・BnF〉')
    checks.append(('衝突の前に後の写真', any('衝突より前の場面' in e for e in run(a1, srcs))))
    # ② S8-625 の副題から「とみられる」を消す
    a2 = put(rows, 'c102', 'sub', 'カリフォルニアン号〈NARA〉')
    checks.append(('控えめな名乗り', any('控えめな名乗り' in e for e in run(a2, srcs))))
    # ③ 書き起こしの断りを消す（c629）
    a3 = put(rows, 'c629', 'kotowari', '')
    checks.append(('書き起こしの断り', any(e.startswith('c629 出典の欄が「書き起こし」') for e in run(a3, srcs))))
    # ④ 額装の写真に動き（c216）
    a4 = put(rows, 'c216', 'motion', '寄る')
    checks.append(('額装に動き', any(e.startswith('c216 額装の写真に動き') for e in run(a4, srcs))))
    # ⑤ 使わない点を出どころに足す
    s5 = srcs + ['S1-036|commons-photo|絵はがき|x|x|x|PD|x|x|前|なし|x|x']
    checks.append(('使わない点', any('使わない点' in e for e in run(rows, s5))))
    # ⑥ 同じ写真に別の副題
    a6 = put(rows, 'c641', 'sub', '朝の海〈1912年・BnF〉')
    checks.append(('同じ写真に別の副題', any('別の副題' in e for e in run(a6, srcs))))
    # ⑦ 冒頭にイメージ
    a7 = put(put(put(rows, 'c107', 'kind', 'イメージ'), 'c107', 'main', 'X-sea-night'), 'c107', 'sub', 'イメージ：夜の海')
    checks.append(('冒頭にイメージ', any(e.startswith('c107 冒頭に') for e in run(a7, srcs))))
    # ⑧ 使い回しの上限（S8-625 を5回目に c520 へ）
    a8 = put(put(put(rows, 'c520', 'main', 'S8-625:試し'), 'c520', 'sub', 'カリフォルニアン号〈カルパチア号の甲板から撮られたとみられる・NARA〉'), 'c520', 'motion', '寄る')
    checks.append(('使い回しの上限', any('上限' in e and 'S8-625' in e for e in run(a8, srcs))))
    # ⑨ NOAA の区間が短い（c901 を 3秒に）
    a9 = put(rows, 'c901', 'motion', '映像（100.0〜103.0秒）')
    checks.append(('映像の区間が短い', any(e.startswith('c901 映像') and '止め絵' in e for e in run(a9, srcs))))
    # ⑩ 名前を切り出しの外にする書き置きを消す（c214）
    a10 = put(put(rows, 'c214', 'note', '字は ⑤b で原寸'), 'c214', 'ga_new', '🔧 静止')
    checks.append(('名前の書き置き', any(e.startswith('c214 素材 S4-264') for e in run(a10, srcs))))
    # ⑪ 続きの main が前のカットでない
    a11 = put(rows, 'c911', 'main', 'c909')
    checks.append(('続きの main', any(e.startswith('c911 「続き」') for e in run(a11, srcs))))
    # ⑫（陰性）KOTO_SKIP のカット（c502）は断りなしで通る
    checks.append(('（陰性）語らない書き起こしは断りなしで通る', not any(e.startswith('c502 ') for e in run(rows, srcs))))
    neg = run(rows, srcs)
    ok = all(v for _, v in checks) and not neg
    for name, v in checks:
        neg_ctl = name.startswith('（陰性）')
        print('陰性' if neg_ctl else '陽性', name, '→', ('通った' if v else '✗ 鳴った') if neg_ctl else ('鳴った' if v else '✗ 鳴らない'))
    print('陰性（今の入力）E', len(neg), '→', 'selftest OK' if ok else 'selftest ✗')
    for e in neg:
        print('  E', e)
    return 0 if ok else 1


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        return selftest()
    return write(build())


if __name__ == '__main__':
    sys.exit(main())
