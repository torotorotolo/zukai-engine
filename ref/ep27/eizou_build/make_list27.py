# -*- coding: utf-8 -*-
"""27本目 映像方針：場面ごとの映像・写真の一覧を組む（2026-10-29・チャット5）。26本目の make_list26.py の型を27本目（事件の回）に替えた。

  python -P ref/ep27/eizou_build/make_list27.py
  python -P ref/ep27/eizou_build/make_list27.py --selftest     （陽性・陰性の対照＝門番が鳴ることを先に見る）

入力：台本 第2版 ref/ep27/daihon_v2.md §4（語りは字数・秒に使う）
      eizou_build/assign27.psv（当て方・11列）・eizou_build/sources27.psv（出どころ・12列）＝手で書く入力
出力：ref/ep27/eizou_list27.md（生成物＝手で直さない）・eizou_build/list27.tsv
門番（E があれば exit 1・⚠️ は止めない）：
  E 実写・引用・衛星・イメージに素材の記号が無い／記号が sources27.psv に無い／使わないと決めた点（NG）が sources27.psv にある
  E 🆕 県警・警察庁の素材（引用）＝額装（引用）でない・動き（寄る／流す）がある・地に使った・出典の行（機関・置き場・日付）が無い・副題に「警察」が無い
  E 🆕 県警の動画の区間が、「犯人」の字の映る秒（BAD）にかかる（10-29 に原寸と OCR で確かめた秒）／区間の長さ＋止めがカットの秒に足りない
  E 🆕 CC BY-SA の写真＝額装でない・動きがある・2カット以上・地に使った（BY-SA は無加工・1点1カット＝ルール §5b-52）
  E 🆕 説明カットの地＝CC BY・CC0・PD の Commons の写真でない（BY-SA・警察の素材・衛星写真・フリー素材は地にしない＝§5b-117）／図の型なのに地が無い（地図の略図は除く）
  E 🆕 SNS のカード（見た目 SNS）に、注釈の印・アカウント名なしの印が無い（§B2-9）
  E 🆕 副題・札に「犯人」「死亡」・「八田與一」の後ろに「容疑者」が無い（引用の字そのものは note に書く＝副題に書かない）
  E 冒頭（c101〜c107）にイメージ（冒頭は実写か実写を地にした画面）／イメージの副題が「イメージ」で始まらない
  E 同じ写真（全面・額装）を3回以上／同じ写真に別の副題／文字だけの画面がある／写真と映像が 20% 未満
  ⚠️ 同じ写真を2回（寄りの名が違えば ⚠️ のまま）・2回が8カットより近い／続く図で見た目の型が同じ／写真の無い画面が5つ以上続く／止めが区間の半分をこえる
  🆕 E（⑤b-1・10-30）県警の動画の区間＋止めが、カットの中身の秒（扉を除く＝実測）に足りない／区間の終わりが手元の素材の実の長さ（ffprobe）をこえる・
     ⚠️ 手元の素材の実の長さが VIDEO_LEN と 0.1秒より違う／素材が手元に無い（長さを測れない）
秒＝audio/narration.json が27本目の台本と合えば実測（⑤b-1 から＝26本目 make_list26.measured() の型・扉は check_script.door_key で数え、
    映像の区間と比べる秒は扉を除いた中身＝cont）・合わなければ台本の句読点なしの字数÷365 の見込み（出力に書く）。
"""
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
OUT_MD = os.path.join(EP, 'eizou_list27.md')
OUT_TSV = os.path.join(HERE, 'list27.tsv')
ASSIGN = os.path.join(HERE, 'assign27.psv')
SOURCES = os.path.join(HERE, 'sources27.psv')
PUNCT = re.compile(r'[、。，．,.「」『』（）()？！?!…・\s　〈〉：:"“”]')
CUT = re.compile(r'^\*\*(c\d{3})\*\*')
OPENING = ['c10%d' % i for i in range(1, 8)]
RATE = 365.0
PHOTO_LO = 0.20
GAP_MIN = 8
PICTURE = ('実写', '引用', '衛星', 'イメージ')
FIGS = ('模式', '流れ', '帯', '比べ', '棒', '年表', '線', '割合', '地図', '並べ', '箱', '札', '暦', '窓口', '対照', '数', 'SNS')
JI_OK_RIGHTS = ('CC BY 2.0', 'CC BY 2.5', 'CC BY 3.0', 'CC BY 4.0', 'CC0', 'PD')
# 県警の動画で「犯人」の字（重要指名手配のポスター）が映る秒＝使わない（10-29 原寸と OCR・境目は0.25秒きざみの画素の差）
BAD = {'YT-A': [(0.0, 20.0), (153.5, 159.25)], 'YT-C': []}
VIDEO_LEN = {'YT-A': 174.08, 'YT-C': 30.09}
KEYS = ['cid', 'kind', 'main', 'ji', 'frame', 'sub', 'motion', 'look', 'ga_new', 'note', 'mark']
SKEYS = ['code', 'type', 'title', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note']
# 使わないと決めた点（見て外した理由）＝ sources27.psv に載せたら E
NG = {'CM105': '別府観光港の交通センター（2022-09-11）＝銀色の車の運転席に人が写る・ヨットハーバーから2.3km',
      'CM131': '題名は「別府港」だが撮影地の座標が大分市の港（CM132〜134 も同じ）',
      'PX17605741': '店の名前（酒店）が読める', 'PX19286419': '外国の街・人が写る', 'PX30617584': '駅名の看板が読める（京都の駅＝場所を名指しすることになる）',
      'PX20193701': '特急の形で路線が分かる・人が写る', 'PX5951903': '前の車のナンバーが写る', 'PX4928592': '外国の交差点・ナンバーが読める',
      'PX4512439': '原寸（1920）で前のタクシーのナンバー「94-92」ほかが読め、横断歩道の歩行者が写る（10-29）＝c510 は PX7553959 に',
      'YT-A_poster': 'YT-A の重要指名手配のポスター（10〜19秒・154〜159秒）＝小さな字に「…死亡ひき逃げ事件の犯人です。」',
      'XPOST2': '県警 X の固定の投稿の2枚目のポスター＝縦書きで「…死傷させた犯人です。」'}
# 映像方針で決めたこと（台本 §0-5 の答え・一覧の §5 に出す）
DECIDED = [
    '✅ 了承②（2026-10-29 カズヤくん）＝①**地の暗さ＝B（字と地の比 8:1 を下限）**＝写真ごとに暗くする量を決める（明るい昼の写真は濃く・夜の写真は薄く）・⑤b の門番は字と図の線の周りの地で 8:1 を測る ②**SNS の注釈＝「※SNS の投稿。事実かは確かめられていません」**（文言を短く・置き場は見本どおり＝右下の字幕の帯の上・黒い帯に黄色い字）③**県警の動画の引用＝カットの秒で実時間で流す**（YT-A 5区間 計43秒・YT-C 1区間 7.5秒・速さは変えない）④そのほか推奨どおり（Commons 42点・Pexels 4点＋替えの候補1点・c603 の X のポスター・地図は衛星写真・人の写り・クレジット）',
    '🔴 県警の動画の「犯人」の字＝YT-A の重要指名手配のポスター（10〜19秒・154〜159秒）の小さな字「…死亡ひき逃げ事件の犯人です。犯人に関する情報を求めています。」（OCR 8コマ＋原寸）→ c309 は 30.3〜36.4秒の「警察庁指定 重要指名手配 被疑者」の大きな字に・c103 は大きな数の図に。境目は0.25秒きざみの画素の差（ポスターは19秒台まで・159.0秒まで）＝門番 BAD',
    'YT-C＝60コマ（0.5秒おき）の OCR で「犯」0・使う秒（1.5〜9.0秒）は原寸で見た。公開日 2025-12-11（yt-dlp の upload_date）＝c106 の副題〈2025年12月〉は正しい。c405 は c106 と同じ顔写真の構図＝図に・c417 は写真に（YT-C は1区間）',
    'c303 の防犯カメラ＝県警 X（2023-04-29 10:30・6.7万回再生）の「防犯カメラ映像」の頭の絵と同じカメラ・同じぼかしの形・同じ車の並び。2022-07-28 の公開と同じかは確かめられない＝副題の断り〈2024年8月の手配の動画から〉を残す',
    'c603＝元の 2026-06-15 の投稿はログインなしでは見つからない（X のプロフィールは最近の5件まで・県の頁にも無い）→ 固定の投稿（2026-06-29 10:33）の1枚目＝全身とサングラスの写真の入った手配のポスター（字は「…被疑者です。」＝OCR で「犯」0）を引用・c604 はその続き。2枚目は縦書きで「…死傷させた犯人です。」＝使わない',
    'c615＝固定の投稿の本文「あなたのそばに潜んでいるかも。」を原文で確かめた（2026-06-29 10:33）。県の頁「指名手配被疑者の検挙にご協力を！」（2026-10-01 更新）の本文は「…殺人等事件の犯人八田與一であり、現在も逃走中です」＝画面に出さない（c514 の語りの出典だけ）',
    '場所＝Commons の撮影地の座標（API の文字）と OpenStreetMap の別府北浜ヨットハーバー（33.27823,131.50798）で照らした：2022-09-10 の夜の連作は駅 → 駅の東の通り → 北浜の交差点（逃げた道すじに近い）・CM056／CM102／CM254 は北浜の海べり（約0.2km）・CM072 は CM056 と同じ山と建物の並び＝北浜のヨットハーバー。台本の港の写真（CM105〜CM112）は2km北の別府観光港＝ヨットハーバーの話には使わない。CM208・CM283 は駅から約3.5km（副題は「別府市の」）・CM239 は約4.8km＝使わない',
    'フリー素材＝Pexels 12点を見本帳で見た：c207 PX30037331（人のいない夜の商店街）・c509 PX7146298（駅名の看板なし）・c510 PX7553959（第1候補 PX4512439 は原寸でナンバーが読めた＝替えた）・c512 PX7508684。外した理由は NG。ライセンスは pexels.com/license と5点の頁で確かめた（10-29・Free to use・生成 AI の印なし）',
    '地図＝c504・c511 の「日本の略図」→ 日本全体の衛星写真（G9）＋地方の札（25本目からの地図の決まり・地方の境は描かない）。衛星写真は G1・G2・G3・G7・G9 の5つを ⑤b-1 で撮る（G4〈上田の湯町〉は G3 に入れる・G5・G6 は夜の写真に替えた）',
    '写真の使い回し＝衛星の3回使い3つを0に。⚠️ の2回使いはすべて寄りを変える（CM151・CM153・CM154・CM198・CM257）か、冒頭と結びで同じ景色に戻す（CM054・CM056）。BY-SA は1点1カット（15点）',
    'Commons の取り方の穴（10-29）＝API の原本の URL の後ろに「?utm_…」が付くようになり、縮小版の置き場も thumb.wikimedia.org に変わった＝原本の URL から組むと 400 → API が返した縮小版の URL を使う（fetch27.py）',
]


def nopunct(s):
    return PUNCT.sub('', s)


def read_psv(path, keys):
    rows = []
    with open(path, encoding='utf-8') as f:
        for n, ln in enumerate(f, 1):
            ln = ln.rstrip('\n')
            if not ln.strip() or ln.startswith('#') or ln.startswith(keys[0] + '|'):
                continue
            parts = ln.split('|')
            if len(parts) != len(keys):
                raise SystemExit('%s %d行目：列の数 %d（%d のはず）: %s' % (os.path.basename(path), n, len(parts), len(keys), ln[:80]))
            rows.append(dict(zip(keys, [p.strip() for p in parts])))
    return rows


def read_cuts(daihon=DAIHON):
    t = open(daihon, encoding='utf-8').read()
    body = t[t.index('## 4. 台本'):t.index('## 5. ')]
    rows, chap, cur = [], '', None
    for ln in body.split('\n'):
        if ln.startswith('### '):
            chap = ln[4:].strip()
            continue
        m = CUT.match(ln)
        if m:
            parts = ln.split(' ／ ')
            cur = dict(cid=m.group(1), chap=chap, ga=parts[1].strip() if len(parts) > 1 else '', n=0, first='')
            rows.append(cur)
            continue
        if cur and ln.startswith('>'):
            s = ln[1:].strip()
            s = s[2:].strip() if s.startswith('Q:') else s
            cur['first'] = cur['first'] or s
            cur['n'] += len(nopunct(s))
    sec = 0.0
    for r in rows:
        r['start'] = sec
        r['dur'] = r['n'] / RATE * 60
        r['cont'], r['card'] = r['dur'], 0.0
        sec += r['dur']
    return rows


def measured(rows):
    """🆕 ⑤b-1（10-30）：秒を audio/narration.json の実測に（26本目 make_list26.measured() の型）。27本目の台本と合わないときは ÷365 の見込みのまま。
    start＝扉こみの頭・dur＝扉＋中身・cont＝扉を除いた中身（声＋LEAD＋TAIL＝映像の区間と比べる秒）。扉は check_script.door_key（27本目は INNER_CARDS なし）"""
    if not os.path.exists(NARR):
        return '÷365 の見込み（narration.json が無い）'
    dur = json.load(open(NARR, encoding='utf-8')).get('durations', {})
    if [r['cid'] for r in rows] != [c for c in dur if c != 'ed01']:
        return '÷365 の見込み（narration.json は27本目の台本と合わない＝⑤a の前）'
    sys.path.insert(0, os.path.join(REPO, 'tools'))
    import check_script as CSC
    sec, prev = 0.0, None
    for r in rows:
        key = CSC.door_key(r['cid'], slug='ep27')
        r['card'] = CSC.CARD_SEC if (prev is not None and key != prev) else 0.0
        prev = key
        r['start'] = sec
        r['cont'] = dur[r['cid']] + CSC.LEAD + CSC.TAIL
        r['dur'] = r['cont'] + r['card']
        sec += r['dur']
    return 'audio/narration.json の実測'


def media_len(path):
    """手元の素材（ref/ep27 からの道）の実の長さ（ffprobe）。道が無い・読めないなら None。
    置き場の欄は「src/…/x.mp4（取得ずみ）」のように注が付く＝頭の道（拡張子まで）だけを使う"""
    m = re.match(r'[\w./\-]+\.(?:mp4|webm|mkv|mov)', path or '')
    path = m.group(0) if m else ''
    p = os.path.join(EP, path) if path else ''
    if not path or not os.path.exists(p):
        return None
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


def fmt_t(s):
    return '%d:%04.1f' % (s // 60, s % 60)


def base(main):
    return main.split(':')[0] if main else ''


def video_window(motion):
    """「映像 22.7〜29.9秒（＋止め 1.0秒）」→ (22.7, 29.9, 1.0)"""
    m = re.search(r'映像\s*([\d.]+)〜([\d.]+)秒(?:（＋止め\s*([\d.]+)秒）)?', motion)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2)), float(m.group(3) or 0)


def is_fig(c):
    return c['kind'] in FIGS


def build(assign_path=ASSIGN, sources_path=SOURCES, daihon=DAIHON):
    cuts = read_cuts(daihon)
    tnote = measured(cuts)
    A = read_psv(assign_path, KEYS)
    S = {s['code']: s for s in read_psv(sources_path, SKEYS)}
    amap = {a['cid']: a for a in A}
    E, W = [], []
    ids = [c['cid'] for c in cuts]
    if [a['cid'] for a in A] != ids:
        miss = sorted(set(ids) - set(amap))
        extra = sorted(set(amap) - set(ids))
        E.append('当て方の表のカットが台本と合わない（無い %s・余り %s・順番も見る）' % (miss[:8], extra[:8]))
    rows = []
    for c in cuts:
        a = amap.get(c['cid'])
        if not a:
            continue
        r = dict(c, **a)
        rows.append(r)
    for code in S:
        if code in NG:
            E.append('使わないと決めた点 %s が sources27.psv にある（%s）' % (code, NG[code]))
    uses = defaultdict(list)          # 全面・額装で見せた回数（地は数えない）
    subs = defaultdict(set)
    ji_uses = defaultdict(list)
    for r in rows:
        cid, kind, code = r['cid'], r['kind'], base(r['main'])
        s = S.get(code) if code else None
        text = r['sub'] + ' ' + r['look']
        if re.search(r'犯人|死亡', text):
            E.append('%s 副題・札に「犯人」か「死亡」: %s' % (cid, text[:60]))
        # 「」の中＝引用の原文（県警の動画の字・SNS の原文）は網の外（台本 §1-4＝「八田與一」とだけ言うのは引用の中だけ）
        if re.search(r'八田與一(?!容疑者)', re.sub(r'「[^」]*」', '', r['sub'])):
            E.append('%s 副題の「八田與一」の後ろに「容疑者」が無い' % cid)
        if kind in PICTURE:
            if not code:
                E.append('%s %s に素材の記号が無い' % (cid, kind))
                continue
            if not s:
                E.append('%s 素材 %s が sources27.psv に無い' % (cid, code))
                continue
            uses[code].append(cid)
            subs[code].add(r['sub'])
            if kind == 'イメージ' and not r['sub'].startswith('イメージ'):
                E.append('%s イメージの副題が「イメージ」で始まらない' % cid)
            if kind == '引用':
                if not r['frame'].startswith('額装（引用）'):
                    E.append('%s 引用なのに額装（引用）でない: %s' % (cid, r['frame']))
                if not (r['motion'].startswith('映像') or r['motion'] == '静止'):
                    E.append('%s 引用に動き（寄る・流す）: %s' % (cid, r['motion']))
                if not re.search(r'出典：(大分県警察|警察庁).*', s['credit']) or not re.search(r'\d{4}年|頁', s['credit']):
                    E.append('%s 引用の出典の行に機関・置き場・日付が無い: %s' % (cid, s['credit']))
                if '警察' not in r['sub']:
                    E.append('%s 引用の副題に「警察」が無い（誰が公開したかを副題で言う）' % cid)
                vw = video_window(r['motion'])
                if s['type'] == 'police-video':
                    vid = code
                    if not vw:
                        E.append('%s 県警の動画なのに区間（映像 a〜b秒）が無い' % cid)
                    else:
                        lo, hi, hold = vw
                        for blo, bhi in BAD.get(vid, []):
                            if lo < bhi and hi > blo:
                                E.append('%s %s %.2f〜%.2f秒が「犯人」の字の映る %.2f〜%.2f秒にかかる' % (cid, vid, lo, hi, blo, bhi))
                        if hi > VIDEO_LEN[vid]:
                            E.append('%s %s の区間の終わり %.2f秒が動画の長さ %.2f秒をこえる' % (cid, vid, hi, VIDEO_LEN[vid]))
                        have = media_len(s['file'])
                        if have is None:
                            W.append('%s %s の素材が手元に無い（置き場の欄＝%s）＝実の長さを測れない（取ってから回し直す）' % (cid, vid, s['file'][:30] or '空'))
                        else:
                            if abs(have - VIDEO_LEN[vid]) > 0.1:
                                W.append('%s %s の手元の素材 %.2f秒が VIDEO_LEN %.2f秒と違う' % (cid, vid, have, VIDEO_LEN[vid]))
                            if hi > have + 0.01:
                                E.append('%s %s の区間の終わり %.2f秒が手元の素材の実の長さ %.2f秒をこえる' % (cid, vid, hi, have))
                        if hi - lo + hold + 0.05 < r['cont']:
                            E.append('%s 区間 %.2f秒＋止め %.2f秒がカットの中身 %.2f秒（扉を除く）に足りない（尻が %.2f秒 欠ける）' % (
                                cid, hi - lo, hold, r['cont'], r['cont'] - (hi - lo + hold)))
                        if hold > (hi - lo) * 0.5:
                            W.append('%s 止め %.1f秒が区間 %.1f秒の半分をこえる' % (cid, hold, hi - lo))
            if 'BY-SA' in s['rights']:
                if not r['frame'].startswith('額装'):
                    E.append('%s BY-SA %s が額装でない: %s' % (cid, code, r['frame']))
                if r['motion'] != '静止':
                    E.append('%s BY-SA %s に動き: %s' % (cid, code, r['motion']))
            if r['frame'].startswith('額装') and r['motion'] not in ('静止',) and not r['motion'].startswith('映像'):
                E.append('%s 額装に動き（10-26 額装は静止）: %s' % (cid, r['motion']))
        elif is_fig(r):
            if r['kind'] != '地図':
                if not r['ji']:
                    E.append('%s 図（%s）なのに地の写真が無い（§5b-117）' % (cid, kind))
                else:
                    sj = S.get(r['ji'])
                    if not sj:
                        E.append('%s 地 %s が sources27.psv に無い' % (cid, r['ji']))
                    elif sj['type'] != 'commons-photo' or not any(sj['rights'].startswith(x) for x in JI_OK_RIGHTS) or 'BY-SA' in sj['rights']:
                        E.append('%s 地 %s は %s・%s＝地にできない（CC BY・CC0・PD の Commons だけ）' % (cid, r['ji'], sj['type'], sj['rights']))
                    else:
                        ji_uses[r['ji']].append(cid)
            if kind == 'SNS' and not ('注釈' in r['note'] and 'アカウント名なし' in r['note'] and r['mark'] == 'SNS'):
                E.append('%s SNS のカードに注釈・アカウント名なしの印が無い（§B2-9）' % cid)
        elif kind == '文字だけ':
            E.append('%s 文字だけの画面' % cid)
        else:
            E.append('%s 種類「%s」が分からない' % (cid, kind))
        if cid in OPENING and kind == 'イメージ':
            E.append('%s 冒頭にイメージ（冒頭は実写か実写を地にした画面）' % cid)
    # 県警の動画は同じ動画の別の区間を使う＝回数でなく「区間が重ならないか」で見る
    wins = defaultdict(list)
    for r in rows:
        if r['kind'] == '引用' and S.get(base(r['main']), {}).get('type') == 'police-video':
            vw = video_window(r['motion'])
            if vw:
                wins[base(r['main'])].append((vw[0], vw[1], r['cid']))
    for vid, ws in wins.items():
        ws.sort()
        for (a0, a1, ca), (b0, b1, cb) in zip(ws, ws[1:]):
            if b0 < a1:
                E.append('%s の区間が重なる: %s %.2f〜%.2f と %s %.2f〜%.2f' % (vid, ca, a0, a1, cb, b0, b1))
    for code, cs in uses.items():
        s = S[code]
        if s['type'] == 'police-video':
            continue
        if 'BY-SA' in s['rights'] and len(cs) > 1:
            E.append('BY-SA %s を %d カット: %s（1点1カット）' % (code, len(cs), ' '.join(cs)))
        elif len(cs) >= 3:
            E.append('同じ写真 %s を %d 回: %s' % (code, len(cs), ' '.join(cs)))
        elif len(cs) == 2 and S[code]['type'] not in ('police-video',):
            i0, i1 = ids.index(cs[0]), ids.index(cs[1])
            W.append('同じ写真 %s を2回: %s %s%s' % (code, cs[0], cs[1], '（%dカットしか離れていない）' % (i1 - i0) if i1 - i0 < GAP_MIN else ''))
        if len(subs[code]) > 1 and S[code]['type'] not in ('police-video', 'satellite'):
            E.append('同じ写真 %s に別の副題: %s' % (code, ' ／ '.join(sorted(subs[code]))))
    for code in ji_uses:
        if 'BY-SA' in S[code]['rights']:
            E.append('BY-SA %s を地に使った' % code)
    # 続く図の見た目・写真の無い画面の続き
    prev_look, run = None, 0
    for r in rows:
        if is_fig(r):
            if r['look'] and r['look'] == prev_look:
                W.append('%s 続く図の見た目が同じ（%s）' % (r['cid'], r['look']))
            prev_look = r['look']
            run += 1
            if run == 5:
                W.append('%s 写真の無い画面が5つ続く' % r['cid'])
        else:
            prev_look, run = None, 0
    n = len(rows)
    photo = [r for r in rows if r['kind'] in ('実写', '引用', '衛星')]
    real = [r for r in rows if r['kind'] in ('実写', '引用')]
    if len(real) < PHOTO_LO * n:
        E.append('写真と映像（この事件の実写＋引用）%d/%d が 20%% 未満' % (len(real), n))
    return dict(rows=rows, S=S, E=E, W=W, uses=uses, ji_uses=ji_uses, n=n, photo=photo, real=real, tnote=tnote)


def write(r, out_md=OUT_MD, out_tsv=OUT_TSV):
    rows, S = r['rows'], r['S']
    total = sum(x['dur'] for x in rows)
    kinds = Counter(x['kind'] for x in rows)
    motions = Counter(x['motion'].split('（')[0].split(' ')[0] for x in rows if x['kind'] in PICTURE)
    frames = Counter(x['frame'] for x in rows if x['kind'] in PICTURE)
    sec_real = sum(x['dur'] for x in r['real'])
    L = []
    L.append('---\ntitle: 27本目 場面ごとの映像・写真の一覧（生成物）\ncreated: 2026-10-29\ntags: [project/jiko-kensho, ep27]\n---\n')
    L.append('# 27本目 場面ごとの映像・写真の一覧（107カット・映像方針）\n')
    L.append('> **生成物＝手で直さない**。作り方＝`python -P ref/ep27/eizou_build/make_list27.py`（入力＝台本 第2版 `daihon_v2.md` §4・当て方 `eizou_build/assign27.psv`・出どころ `eizou_build/sources27.psv`）。直すのは入力。')
    L.append('> 秒＝' + r['tnote'] + '（扉こみの頭と長さ・映像の区間と比べるのは扉を除いた中身＝list27.tsv の cont）。🔧＝台本の画の欄から替えたカット（⑤b はこの一覧に従う・台本は直さない）。色味は原本（10-07）・写真は画面いっぱい（10-11）＝例外は BY-SA（額装・無加工・1点1カット）と警察の素材（引用＝額装・無加工）と衛星写真（額装）＝額装はどれも静止（10-26）。説明カットの地＝CC BY・CC0 の写真を暗くするだけ（27本目〜）。見た画像の記録＝`src/seen_log.tsv`（映像方針の印）。\n')
    L.append('## §0 数\n')
    L.append('| 物差し | 値 | 決まり |\n|---|---|---|')
    L.append('| この事件の写真・映像（Commons の実写＋警察の素材の引用） | **%d カット＝%.1f%%**（実写 %d・引用 %d・秒 %.0f＝%.1f%%） | 20%%以上 %s |' % (
        len(r['real']), 100.0 * len(r['real']) / r['n'], kinds['実写'], kinds['引用'], sec_real, 100.0 * sec_real / total, '✅' if len(r['real']) >= PHOTO_LO * r['n'] else '🔴'))
    L.append('| 衛星写真（地図） | %d カット（20%% に数えない） | 帰属の行を出し続ける・色を変えない・額装・⑤b-1 で撮る |' % kinds['衛星'])
    L.append('| フリー素材（イメージ） | %d カット（20%% に数えない） | 人の顔・ナンバー・店の名前なし・生成 AI なし・「イメージ」と出す |' % kinds['イメージ'])
    figs = sum(v for k, v in kinds.items() if k in FIGS)
    L.append('| 図（模式・型の図・SNS のカード） | %d カット（地＝写真 %d・略図 %d） | 地は CC BY・CC0 の写真を暗くするだけ・動かさない |' % (figs, figs - kinds['地図'], kinds['地図']))
    L.append('| 文字だけ | %d カット | 0 |' % kinds['文字だけ'])
    L.append('| 全面／額装 | %s | 額装は静止 |' % '・'.join('%s %d' % kv for kv in frames.most_common()))
    L.append('| 写真の動き | %s | 額装と引用は動かさない・全面は寄る／流す |' % '・'.join('%s %d' % kv for kv in motions.most_common()))
    L.append('| 🔧 台本の画の欄から替えたカット | %d | 台本は直さない＝⑤b はこの一覧に従う |' % sum(1 for x in rows if x['ga_new'] not in ('', '台本どおり')))
    L.append('| 種類 | %s | — |' % '・'.join('%s %d' % kv for kv in kinds.most_common()))
    L.append('| 合計 | %d カット・%s | — |\n' % (r['n'], fmt_t(total)))
    L.append('### 写真の使い回し（全面・額装で2回以上＝地は数えない）\n')
    for code, cs in sorted(r['uses'].items()):
        if len(cs) > 1:
            L.append('- %s（%s）＝%s' % (code, S[code]['title'], ' '.join(cs)))
    L.append('\n### 地に使った写真（説明カットの背景＝暗くするだけ）\n')
    for code, cs in sorted(r['ji_uses'].items()):
        L.append('- %s（%s・%s）＝%d カット：%s' % (code, S[code]['title'], S[code]['rights'], len(cs), ' '.join(cs)))
    L.append('\n## §1 冒頭（c101〜c107）＝実写と実写を地にした画面だけ（最初に設計した）\n')
    L.append('| カット | 秒 | 語りの頭 | 画 |\n|---|---|---|---|')
    for x in rows:
        if x['cid'] in OPENING:
            L.append('| %s | %s〜%s | %s | %s %s（%s） |' % (x['cid'], fmt_t(x['start']), fmt_t(x['start'] + x['dur']), x['first'][:24], x['kind'], x['main'], x['sub'] or x['look']))
    L.append('\n## §2 章ごと・カットごと\n')
    chap = None
    for x in rows:
        if x['chap'] != chap:
            chap = x['chap']
            L.append('\n### %s\n' % chap)
            L.append('| カット | 秒 | 語りの頭 | 種類 | 素材 | 地 | 見せ方 | 副題・札 | 動き | 🔧 | 備考 |\n|---|---|---|---|---|---|---|---|---|---|---|')
        mark = '🔧' if x['ga_new'] not in ('', '台本どおり') else ''
        L.append('| %s | %s（%.1f） | %s | %s | %s | %s | %s | %s | %s | %s %s | %s |' % (
            x['cid'], fmt_t(x['start']), x['dur'], x['first'][:20], x['kind'], x['main'] or '—', x['ji'] or '—', x['frame'] or '—',
            x['sub'] or x['look'], x['motion'] or '—', mark, x['ga_new'] if mark else '', x['note']))
    L.append('\n## §3 素材の一覧（出どころ・権利・取得＝了承②の対象）\n')
    L.append('| 記号 | 種類 | 中身（見て確かめた） | 大きさ | 権利 | 根拠 | 画面の出典 | 時期 | 人の写り | 使うカット |\n|---|---|---|---|---|---|---|---|---|---|')
    for code, s in S.items():
        cs = r['uses'].get(code, []) + ['地 ' + c for c in r['ji_uses'].get(code, [])]
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (code, s['type'], s['title'], s['dims'], s['rights'], s['basis'], s['credit'], s['era'], s['people'], ' '.join(cs) or '（使わない）'))
    L.append('\n## §4 門番\n')
    L.append('- E %d 件・⚠️ %d 件' % (len(r['E']), len(r['W'])))
    for e in r['E']:
        L.append('- 🔴 E ' + e)
    for w in r['W']:
        L.append('- ⚠️ ' + w)
    if DECIDED:
        L.append('\n## §5 映像方針で決めたこと（台本 §0-5 の答え・10-29）\n')
        for d in DECIDED:
            L.append('- ' + d)
    with open(out_md, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    with open(out_tsv, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['cid', 'start', 'dur'] + KEYS[1:] + ['card', 'cont']) + '\n')
        for x in rows:
            f.write('\t'.join([x['cid'], '%.2f' % x['start'], '%.2f' % x['dur']] + [x[k] for k in KEYS[1:]]
                              + ['%.1f' % x['card'], '%.2f' % x['cont']]) + '\n')


def selftest():
    import tempfile
    cuts = read_cuts()
    good = []
    for c in cuts:
        good.append('|'.join([c['cid'], '実写', 'CMT', '', '全面', '別府市の夜〈2022年9月〉', '寄る', '', '台本どおり', '', '']))
    src = ['code|type|title|get|dims|rights|basis|credit|era|people|file|note',
           'CMT|commons-photo|テスト|commons:CMT|4032x3024|CC BY 2.0|Flickr|Wikimedia Commons（CC BY 2.0）|後|なし|x|',
           'CMSA|commons-photo|テスト|commons:CMSA|3264x2448|CC BY-SA 4.0|-|Wikimedia Commons（CC BY-SA 4.0）|後|なし|x|',
           'CMU|commons-photo|テスト2|commons:CMU|4032x3024|CC BY 2.0|Flickr|Wikimedia Commons（CC BY 2.0）|後|なし|x|',
           'YT-A|police-video|手配の動画|yt|1920x1080|引用|県の頁|出典：大分県警察 公式YouTube（2024年8月1日）|後|容疑者（引用）|x|',
           'YT-C|police-video|手配の動画|yt|854x476|引用|県の頁|出典：大分県警察 公式YouTube（2025年12月11日）|後|容疑者（引用）|x|']
    cases = [
        ('陰性', None, 0),
        ('陽性 BY-SA を全面で', ('c201', '実写|CMSA||全面|別府の港〈2024年5月〉|静止'), 1),
        ('陽性 引用が「犯人」の秒', ('c201', '引用|YT-A:x||額装（引用）|警察が公開した手配の動画〈2024年8月〉|映像 12.0〜21.0秒'), 1),
        ('陽性 地が BY-SA', ('c201', '模式||CMSA|—||'), 1),
        ('陽性 副題に犯人', ('c201', '実写|CMT||全面|犯人の通った道|寄る'), 1),
        ('陽性 八田與一だけ', ('c201', '実写|CMT||全面|八田與一の写真|寄る'), 1),
        ('陽性 冒頭にイメージ', ('c101', 'イメージ|CMT||全面|イメージ：夜|寄る'), 1),
        ('陽性 SNS の印なし', ('c201', 'SNS||CMT|—|カード|'), 1),
        ('陽性 額装に動き', ('c201', '実写|CMT||額装（高さいっぱい）|別府市の夜〈2022年9月〉|寄る'), 1),
        ('陰性 SNS の原文の中の八田與一', ('c201', '実写|CMU||全面|SNS の声「なんか八田與一に似てる」|寄る'), 0),
        ('陽性 区間＋止めがカットの中身に足りない（⑤b-1）', ('c201', '引用|YT-A||額装（引用）|警察が公開した手配の動画〈2024年8月〉|映像 22.0〜23.0秒'), 1),
        ('陽性 区間の終わりが動画の長さをこえる', ('c201', '引用|YT-C||額装（引用）|警察が公開した手配の動画〈2025年12月〉|映像 25.0〜31.0秒'), 1),
        ('陽性 県警の動画の区間が重なる', [('c201', '引用|YT-A||額装（引用）|警察が公開した手配の動画〈2024年8月〉|映像 22.0〜32.0秒'),
                                       ('c202', '引用|YT-A||額装（引用）|警察が公開した手配の動画〈2024年8月〉|映像 30.0〜40.0秒')], 1),
    ]
    ok = True
    for name, mod, want_e in cases:
        lines = list(good)
        for m in ([mod] if isinstance(mod, tuple) else (mod or [])):
            i = [l.split('|')[0] for l in lines].index(m[0])
            parts = m[1].split('|')
            row = [m[0]] + parts[:6] + ['', '🔧 テスト', '', '']
            lines[i] = '|'.join(row[:11])
        with tempfile.TemporaryDirectory() as d:
            pa, ps = os.path.join(d, 'a.psv'), os.path.join(d, 's.psv')
            open(pa, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
            open(ps, 'w', encoding='utf-8').write('\n'.join(src) + '\n')
            res = build(pa, ps)
        # 陰性は同じ写真を107回使うので「3回以上」の E だけが出る＝それを除いて数える
        es = [e for e in res['E'] if not e.startswith('同じ写真 CMT を')]
        got = 1 if es else 0
        flag = '✓' if got == want_e else '✗'
        ok &= got == want_e
        print('%s %s：E %d 件 %s' % (flag, name, len(es), es[:1]))
    print('selftest', 'OK' if ok else 'NG')
    return 0 if ok else 1


def main():
    if '--selftest' in sys.argv:
        return selftest()
    r = build()
    write(r)
    rows = {x['cid']: x for x in r['rows']}
    print('秒：', r['tnote'], '・c103 の終わり %.1f・c107 %.1f・合計 %s' % (
        rows['c103']['start'] + rows['c103']['dur'], rows['c107']['start'] + rows['c107']['dur'], fmt_t(sum(x['dur'] for x in r['rows']))))
    print('カット %d・写真と映像（実写＋引用）%d＝%.1f%%・E %d・⚠️ %d → %s' % (r['n'], len(r['real']), 100.0 * len(r['real']) / r['n'], len(r['E']), len(r['W']), OUT_MD))
    for e in r['E']:
        print('E', e)
    for w in r['W']:
        print('W', w)
    return 1 if r['E'] else 0


if __name__ == '__main__':
    sys.exit(main())
