# -*- coding: utf-8 -*-
"""ep11_assets.py — 11本目（チャレンジャー号 STS-51-L）の**写真の束**を作る（2026-09-21 ⑤c-2 新設）。

`qa_out/ep10_assets.py`（10本目）を写して直した。**権利の形がまるで違うので、中身は別物**。

■ 10本目との違い
  | | 10本目 三豊百貨店 | 11本目 チャレンジャー号 |
  |---|---|---|
  | 権利 | CC BY-SA 4.0 が82点＋公共ヌリ10点 | **ほぼ全点が PD**（米連邦 §105／Commons の PD 札） |
  | 継承（ShareAlike） | 82点。額装でだけ使う | **0点。入れない**（見つけたら落とす） |
  | 置き場 | Commons ＋ 手元 | **Commons ＋ NASA画像庫 ＋ 動く映像からの抜き** |
  | 動く映像 | 0本 | **3本**（記録映画・USIA 公聴会・NARA 氷） |

■ 🔴 守っていること（ep10 から引き継ぐ）
  1. **②が記録した権利と、いま置き場が返す権利が食い違ったら止める**（fail closed）。
     → [[feedback-verify-inherited-claims]]／[[feedback-gates-go-stale-when-upstream-changes]]
  2. **題名が引けなければ黙って飛ばさず止める**（fail closed）→ [[feedback-parsers-fail-closed]]
  3. 撮影年は出典に出す。作れないものは「不明」（**年を作らない**）
     → [[feedback-fallback-stills-must-match-the-era]]
  4. 出力はファイルへ。`| tail` でつながない（[[feedback-pipes-mask-exit-codes]]）
  5. 画素は**幅3,000px まで**（⑤cの原寸目視のために残す）

■ 🔴🔴 ここに在るのは「候補の当たり」であって在庫ではない
  **`sheet` で絵を見てから採ること。**題名だけで採ると別物が来る
  （9本目は「KLMの747」がパンナム機だった）→ [[feedback-inventory-is-not-usable-material]]

    python qa_out/ep11_assets.py info      # 権利・寸法・撮影者を引き直して ref/ep11/assets.json へ
    python qa_out/ep11_assets.py fetch     # ref/ep11/<名>.jpg に落とす
    python qa_out/ep11_assets.py stills    # 🔴 動く映像から20点を抜く（ffmpeg・SAR を当てる）
    python qa_out/ep11_assets.py check     # PICK・assets.json・ファイルの3つが揃っているか
    python qa_out/ep11_assets.py panel     # 切り落とし率の並び（PANEL_AR を決める材料）
    python qa_out/ep11_assets.py sheet [名の頭 ...]   # 640px のシート（2列×3行）
    python qa_out/ep11_assets.py credits [--write]    # credits.json と ref/CREDITS.md の表
"""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

COMMONS = 'https://commons.wikimedia.org/w/api.php'
NASA_SEARCH = 'https://images-api.nasa.gov/search'
NASA_ASSET = 'https://images-api.nasa.gov/asset/'
UA = 'zukai-engine/1.0 (accident-documentary research; contact: konariri8@gmail.com)'
DEST = HERE / 'ref' / 'ep11'
DB = DEST / 'assets.json'
CLIPS_JSON = DEST / 'clips.json'
SHEET = HERE / 'out' / 'ep11_sheet'
MAXW = 3000

# 🔴 継承（ShareAlike）はこの回は1点も入れない。当たったら止める。
NG_LIC = ('SA',)


def C(title, **kw):
    return dict(src='commons', title=title, **kw)


def N(nasa_id, **kw):
    return dict(src='nasa', id=nasa_id, **kw)


def V(clip, t, **kw):
    """動く映像から抜く止め絵。`t` は**帯の中での秒**（`clips.json` の `at` からの相対）。"""
    return dict(src='clip', clip=clip, t=t, **kw)


# ══════════════════════════════════════════════════════════
#  PICK ── 台本の欄の名前 → 1点
# ══════════════════════════════════════════════════════════
# 🔴 鍵は**台本 §4 が書いている欄の名前そのまま**（`ref/ep11/parse_script.py --slots` で出る90件）。
#    `cuts/ss.py` の `P(名)` が `ep11/<名>.jpg` を指す。3つが食い違うと写真が出ない。
# ⚠️ 当てた根拠は `ref/ep11/photo_picks.md`。**採否は sheet を見てから。**
PICK: dict[str, dict] = {

    # ── 動く映像から抜く止め絵（12点）。秒は `ref/ep11/photo_picks.md` §2-2 ──────────
    'ice_icicle':           V('t_ice', 14, note='氷に覆われた配管（元1119）'),
    'ice_trough':           V('t_ice', 9,  note='🔴 水受けの厚い氷（元1114）。額入り 470x479'),
    'ice_icicle_2':         V('t_ice', 23, note='霜の付いた梁（元1128）'),
    'ice_box':              V('t_ice', 18, note='🔴 氷でふさがった通信箱（元1123）'),
    'ssme_ignition':        V('launch', 9, note='主エンジンの点火（元607）'),
    'srb_stack':            V('srb', 48,   note='積み上げ（元1041）'),
    'oring_physical':       V('joint', 2,  note='ゴムの輪の現物（元1540）'),
    'oring_channel':        V('joint', 8,  note='溝（元1546）'),
    'commission_hearing':   V('commission', 2, note='机の上のシャトル模型（元57）'),
    'commission_room':      V('commission', 12, note='青い幕の公聴会場（元67）'),
    'commission_members':   V('commission', 14, note='🔴 壇上に並ぶ委員（元69）'),
    'commission_hearing_2': V('commission', 19, note='公聴会の席（元74）'),
    # 🔴 2026-09-21 ⑤c-2 で動画から止め絵に変えた。使えるのは 元59〜64 の5秒だけで
    #    （64〜66秒に `ROBERT R…` の名札）、c709 の尺 9.92秒だと **0.50倍速**＝
    #    自分で決めた「0.6 を下回るものは動画にしない」に当たる。
    'commission_testimony': V('commission', 6, note='木の壁の委員会室（元61）'),

    # ── 動画にする8点の「ひかえの静止画」（`ss.fb(cid)` が指す名前）─────────────────
    'fb_c307': V('smoke', 11,      note='🔴 黒い煙（元1459）'),
    'fb_c413': V('accident', 49,   note='破壊されたあとの筋（元711）'),
    'fb_pr02': V('launch', 19,     note='打ち上げ（元617）'),
    'fb_c603': V('srb', 36,        note='積み上げ工程（元1029）'),
    'fb_pr07': V('joint', 30,      note='継ぎ目とゴムの輪（元1568）'),
    'fb_c503': V('joint', 42,      note='現地で組んだ継ぎ目（元1580）'),
    'fb_c101': V('pad', 44,        note='射点39Bの機体（元1188）'),

    # ── 乗員（11点）────────────────────────────────────────────────
    'crew_portrait':   C('Challenger flight 51-l crew.jpg'),
    'crew_portrait_2': N('S85-44253', note='Official Portrait - STS-51L Crewmembers'),
    'crew_portrait_3': C('722342main challenger full full.jpg'),
    'crew_scobee':     C('Francis Richard Scobee.jpg'),
    'crew_smith':      C('Michael Smith (NASA).jpg'),
    'crew_onizuka':    N('S86-25964', note='Portrait - Astronaut Onizuka, Ellison S.（1986）'),
    'crew_resnik':     C('Judith A. Resnik, official portrait.jpg'),
    'crew_mcnair':     N('S85-36539', note='Portrait - Astronaut McNair, Ronald E.（1985）'),
    'crew_jarvis':     N('S85-25624', note='Official portrait Gregory Jarvis（1985）'),
    'crew_breakfast':  C('STS-51-L preflight breakfast.jpg'),
    'crew_whiteroom':  C('51-L Challenger Crew in White Room - GPN-2000-001867.jpg'),

    # ── マコーリフ・訓練（4点）──────────────────────────────────────
    'mcauliffe_class':    N('S85-41239', note='Official portrait Sharon Christa McAuliffe'),
    'mcauliffe_training': C('Christa McAuliffe in Training (28698549073).jpg'),
    'mcauliffe_morgan':   C('Christa McAuliffe and Barbara Morgan - GPN-2002-000004.jpg'),
    'training_zero_g':    C('Zero-G training for crew of 1985 and 1986 space shuttle missions.jpg'),

    # ── 氷・射点（5点）─────────────────────────────────────────────
    'ice_pad':          C("Ice on the Pad on the Day of STS-51-L's Launch - GPN-2004-00011.jpg"),
    'ice_egress':       N('51L-10147', note='View of ice on the launch complex'),
    'ice_team':         C('Photograph of Space Shuttle Ice and Frost Inspection - NARA - 593693.gif',
                          note='🔴 481x600。氷の点検班はこの1点だけ'),
    'rockwell_orbiter': C('Space Shuttle Columbia receives her thermal tiles at KSC (KSC-79P-119).jpg',
                          note='⚠️ 1979年・コロンビア（チャレンジャーではない）。⑤bの当て。'
                               '副題で機体名と年を名乗る＝[[feedback-subtitle-must-match-what-is-visible]]'),

    # ── 打ち上げ・上昇（4点）───────────────────────────────────────
    'launch_pad_morning': C('STS-51-L.jpg'),
    # 🔴 2026-09-21 ⑤c-2 で直した。はじめ `51l-s-155`（＝51-L 自身の打ち上げ）を当てていたが、
    #    `c313` は「**それまでの**打ち上げの映像も調べ直された」と言うカット。
    #    51-L の絵を出すと**言っていることと違う絵**になる（門番は1本も鳴らない）
    #    → [[feedback-subtitle-must-match-what-is-visible]]
    #    ⚠️ 1984年の点は「別の飛行」なので②の網では捨てる決まりだが、
    #       **ここは「別の飛行」であることが要る**カット。機体は同じチャレンジャー号。
    'past_launch':        N('41c-3029', note='1984年4月 41-C の打ち上げ（チャレンジャー号の別の飛行）'),
    'ascent_1':           C('70mm frame of Challenger during ascent.png'),
    'ascent_2':           C('Challenger - GPN-2000-001347.jpg'),

    # ── 煙・炎・破壊（10点）────────────────────────────────────────
    'smoke_puffs':      C('STS51L-10144 black smoke.jpg', note='⚠️ 751x523'),
    'flame_plume':      C('Booster Rocket Breach - GPN-2000-001425.jpg', note='58.778秒の炎'),
    'flame_plume_2':    C('Challenger 58 sec.jpg', note='⚠️ 477x621'),
    'et_breach':        C('LOX Tank Rupture - GPN-2000-001426.jpg'),
    'breakup_moment':   C('Challenger breakup.jpg'),
    'accident_breakup': C('Challenger explosion.jpg'),
    'fireball_wide':    C('SPACE SHUTTLE CHALLENGER DISASTER 1986 UNCORRECTED COLOR '
                          '20211117142954!Challenger explosion.jpg'),
    'fireball':         C('Challenger explosion (cropped).jpg'),
    'hydrogen_burn':    C('Challenger explosion (cropped).jpg',
                          note='⚠️ fireball と同じ点。寄りを変えて使う（専用の絵が無い）'),
    'breakup_sections': C('Shuttle Destruction - GPN-2000-001423.jpg'),
    'srb_trails':       C('Challenger Rocket Booster - GPN-2000-001422.jpg'),

    # ── 残骸・回収（10点）──────────────────────────────────────────
    'recovery_ship':       C('STS-51-L Debris Aboard the USGS Cutter Dallas - GPN-2004-00013.jpg'),
    'debris_hangar':       C('ChallengerRemains.jpg'),
    'debris_et':           C('STS-51-L Recovered Debris (ET and SRBs) - GPN-2004-00003.jpg'),
    'srb_burn_hole':       C('STS-51-L Recovered Debris (Left Solid Rocket Booster) - GPN-2004-00009.jpg'),
    'srb_burn_hole_2':     N('51L-10162', note='View of left SRB first piece retrieval'),
    'srb_inside':          C('STS-51-L Recovered Debris (O-Ring Tracks on Right SRB Joint) - GPN-2004-00010.jpg',
                             note='⚠️ oring_erosion_photo と同じ点。寄りを変える'),
    'rudder_burn':         C('STS-51-L Recovered Debris (Lower Right Vertical Stabilizer) - GPN-2004-00005.jpg'),
    'frustum_compare':     C('STS-51-L Recovered Debris (Forward Skirt) - GPN-2004-00006.jpg'),
    'ssme_salvage':        C('STS-51-L Recovered Debris (SSME Close Up) - GPN-2004-00008.jpg'),
    'oring_erosion':       C('STS-51-L Recovered Debris (Burn Marks on the SRM) - GPN-2004-00004.jpg'),
    'oring_erosion_photo': C('STS-51-L Recovered Debris (O-Ring Tracks on Right SRB Joint) - GPN-2004-00010.jpg'),

    # ── 委員会・組織（7点）─────────────────────────────────────────
    # 🔴🔴 `commission_report` は**落とした**（下の MISSING）。
    #    Commons の `Rogers-report-front-page.png` は題も説明も
    #    「Cover of final report for the Rogers Commission」だが、**絵は別物**だった＝
    #    米上院の公聴会記録の表紙（SPACE SHUTTLE ACCIDENT / HEARINGS BEFORE THE
    #    SUBCOMMITTEE ON SCIENCE, TECHNOLOGY, AND SPACE / FEBRUARY 18, JUNE 10 AND 17, 1986）。
    #    → [[feedback-inventory-is-not-usable-material]]（題名だけで採ると別物が来る）
    'commission_oversight':  N('S86-28889', note='PRESIDENTIAL COMMISSION - STS-33/51L - KSC'),
    'mulloy_testimony':      N('S86-28750'),
    'astronaut_manager':     N('51L-10166', note='委員がKSCに着く'),
    'safety_panel':          C('Rogers Commission members arrive at Kennedy Space Center.jpg'),
    'mmt_meeting':           C('STS-51L riadiace stredisko.jpg', note='管制室。⑤bの当て'),
    'telecon_room':          C('STS-51-L mcc 01.jpg', note='⚠️ 630x450'),

    # ── 追悼（4点）─────────────────────────────────────────────────
    'memorial_service': N('51l-s-127', note='STS 51-L Memorial service on JSC main mall'),
    'memorial_wreath':  N('51l-s-108', note='Barbara Morgan at Memorial service'),
    'flag_half_mast':   N('S86-26436', note='Flags at half-staff in memorial of STS 51-L crewmembers'),
    'reagan_address':   C('Presidents Speech to The Nation on The Space Shuttle Challenger in '
                          'Oval Office - DPLA - 24415e25cef1697901176efda1f71503.jpg'),
}

# 🔴 動画にする8カットの欄（`footage.USE` に入る）。**欄の名前では写真を採らない**
#    ＝ `cuts/README.md` §0-8「動画は写真より優先」。`ss.vid(cid, ...)` が `fb_<cid>.jpg` を指す。
#    その `fb_*` は上の PICK に在り、**動画が取れなかったときのひかえ**になる。
VIDEO_SLOTS = ('smoke_liftoff', 'srb_destruct', 'launch_liftoff', 'thiokol_plant',
               'srb_oring', 'srb_field_joint', 'pad_39b')

# 🔴🔴 **まだ当てが無い14件**（`photo_picks.md` §3）。
#    ほとんどが**報告書の図でしか見たことのない主題**（`slot_fill.md` §7＝報告書の図版は使えない）。
#    🔴 `burn.mpg`（元2494〜2626。**全画面が83秒つづく**）から止め絵で抜けるものを先に当てること。
#    ⚠️ ここに名前が在るだけでは合格にしない。`check` が「PICK にも MISSING にも無い」を止める。
MISSING = ('joint_test', 'oring_resilience_test', 'srb_sun_shade', 'joint_qual_test',
           'srm_horizontal', 'srm_nozzle_51b', 'joint_redesign', 'joint_test_new',
           'srm_vertical_test', 'oring_soot', 'oring_data_chart',
           'thiokol_telefax', 'marshall_center', 'launch_51c',
           # 🔴 2026-09-21 ⑤c-2 で落とした。Commons の題と説明が嘘で、絵は上院の公聴会記録
           #    の表紙だった（上の注）。**本物のロジャース委員会報告書の表紙は Commons に無い**
           #    （3通りの語で探して0件）。⑤c-3 で別の置き場を当たること。
           'commission_report')


def _plain(s):
    s = re.sub(r'<[^>]+>', ' ', str(s or ''))
    s = s.replace('&amp;', '&').replace('&quot;', '"').replace('&#039;', "'")
    return re.sub(r'\s+', ' ', s).strip()


def _year(s):
    m = re.search(r'(1[89]\d\d|20\d\d)', str(s or ''))
    return int(m.group(1)) if m else None


def _get(url, tries=5, timeout=120):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as e:                              # noqa: BLE001
            if i == tries - 1:
                raise
            print(f'   再試行 {i + 1}/{tries}: {e}')
            time.sleep(3 + 3 * i)
    return b''


def _json(url):
    return json.loads(_get(url, timeout=60).decode('utf-8'))


def commons_info(titles):
    """題名（File: なし）の束 → imageinfo。🔴 引けない題名は呼び元で止める。"""
    out = {}
    titles = list(titles)
    for i in range(0, len(titles), 25):
        chunk = titles[i:i + 25]
        p = dict(action='query', format='json', formatversion='2',
                 titles='|'.join('File:' + t for t in chunk),
                 prop='imageinfo', iiprop='url|size|extmetadata')
        j = _json(COMMONS + '?' + urllib.parse.urlencode(p))
        norm = {n['from']: n['to'] for n in j.get('query', {}).get('normalized', [])}
        back = {}
        for t in chunk:
            back[norm.get('File:' + t, 'File:' + t)] = t
        for pg in j.get('query', {}).get('pages', []):
            key = back.get(pg['title'], pg['title'][5:])
            if pg.get('missing') or not pg.get('imageinfo'):
                continue
            ii = pg['imageinfo'][0]
            em = ii.get('extmetadata', {})
            out[key] = dict(
                w=ii['width'], h=ii['height'], url=ii['url'],
                lic=_plain(em.get('LicenseShortName', {}).get('value')),
                author=_plain(em.get('Artist', {}).get('value')) or 'NASA',
                date=_plain(em.get('DateTimeOriginal', {}).get('value')),
                page=f'https://commons.wikimedia.org/wiki/File:{urllib.parse.quote(key)}')
        time.sleep(0.4)
    return out


def nasa_info(nasa_id):
    """NASA 画像庫の1点 → 原寸の URL と説明。🔴 引けなければ None（呼び元で止める）。"""
    j = _json(NASA_SEARCH + '?' + urllib.parse.urlencode(dict(q=nasa_id, media_type='image')))
    hit = None
    for it in j['collection']['items']:
        d = it['data'][0]
        if str(d.get('nasa_id', '')).lower() == nasa_id.lower():
            hit = d
            break
    if hit is None:
        return None
    # 🔴 資産の窓口は**大文字小文字を見る**。②の欄は小文字で持っているものがあるので、
    #    検索が返した本物の `nasa_id` を使う（`41c-3029` で引くと 404）。
    real = str(hit.get('nasa_id') or nasa_id)
    a = _json(NASA_ASSET + urllib.parse.quote(real))
    hrefs = [x['href'] for x in a['collection']['items']]
    orig = ([h for h in hrefs if h.lower().endswith(('~orig.jpg', '~orig.png', '~orig.tif'))]
            or [h for h in hrefs if h.lower().endswith(('~large.jpg', '.jpg'))])
    if not orig:
        return None
    return dict(url=orig[0].replace('http://', 'https://'),
                lic='Public domain (17 U.S.C. §105)',
                author=_plain(hit.get('photographer') or hit.get('center') or 'NASA'),
                date=str(hit.get('date_created', ''))[:10],
                title=_plain(hit.get('title')),
                page=f'https://images.nasa.gov/details/{urllib.parse.quote(nasa_id)}')


def cmd_info():
    """置き場に引き直して `ref/ep11/assets.json` を作る。🔴 引けない点があれば止める。"""
    db, bad = {}, []
    ctitles = [v['title'] for v in PICK.values() if v['src'] == 'commons']
    print(f'Commons を引く: {len(set(ctitles))} 題名')
    ci = commons_info(sorted(set(ctitles)))

    clips = json.loads(CLIPS_JSON.read_text(encoding='utf-8'))
    for name, p in PICK.items():
        if p['src'] == 'clip':
            # 🔴 止め絵にも**撮影年**を持たせる。無いと副題が「1986年1月28日」と名乗るのに
            #    表が「不明」になり、`check_credits` が食い違いとして止める（実測5件）。
            #    年は `clips.json` の `date`（記録映画＝当日／USIA＝1986年）から引く。
            db[name] = dict(src='clip', clip=p['clip'], t=p['t'], note=p.get('note', ''),
                            year=_year(clips[p['clip']]['date']),
                            lic='Public domain (17 U.S.C. §105)',
                            author=clips[p['clip']]['credit'])
            continue
        if p['src'] == 'commons':
            r = ci.get(p['title'])
            if not r:
                bad.append(f'{name}: Commons に「{p["title"]}」が無い')
                continue
            if any(x in _plain(r['lic']).upper().replace('-', ' ').split() for x in NG_LIC):
                bad.append(f'🔴 {name}: 継承つき（{r["lic"]}）。この回は入れない')
                continue
            # 🔴 `year=` を書いた欄は、置き場の日付欄より**そちらを採る**。
            #    置き場が撮影日を持っていない点で、**別の根拠で年が分かっている**ときだけ使う。
            #    ⚠️ 年を作らないこと＝根拠を `note` に書く → [[feedback-fallback-stills-must-match-the-era]]
            db[name] = dict(src='commons', title=p['title'],
                            year=p.get('year') or _year(r['date']),
                            note=p.get('note', ''), **r)
        else:
            # 🔴 1点の失敗で全部の引き直しを落とさない（落とすと**直した点まで消える**）。
            #    落ちた点は下で一覧にして 🔴 を返す＝黙って合格にはしない。
            try:
                r = nasa_info(p['id'])
            except Exception as e:                          # noqa: BLE001
                bad.append(f'{name}: NASA画像庫で落ちた（{type(e).__name__}: {e}）')
                continue
            if not r:
                bad.append(f'{name}: NASA画像庫に「{p["id"]}」の原寸が無い')
                continue
            db[name] = dict(src='nasa', id=p['id'], year=_year(r['date']),
                            note=p.get('note', ''), **r)
            time.sleep(0.4)
        print(f"  {name:22} {db[name].get('w', '?')}x{db[name].get('h', '?')} "
              f"{db[name]['year']} {db[name]['lic'][:26]}")

    if bad:
        print('\n🔴 引けなかった点（fail closed）:')
        for b in bad:
            print('   ' + b)
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'\n✓ {DB} に {len(db)} 点／🔴 {len(bad)} 点')
    return 1 if bad else 0


def _db():
    if not DB.exists():
        raise SystemExit('🔴 ref/ep11/assets.json が無い。まず info')
    return json.loads(DB.read_text(encoding='utf-8'))


def cmd_stills(only=None):
    """🔴 動く映像から止め絵を抜く。**SAR を当ててから**（1:1 のままだと横に12.5%太る）。"""
    clips = json.loads(CLIPS_JSON.read_text(encoding='utf-8'))
    DEST.mkdir(parents=True, exist_ok=True)
    ok = err = 0
    for name, p in PICK.items():
        if p['src'] != 'clip':
            continue
        if only and not any(name.startswith(o) for o in only):
            continue
        c = clips[p['clip']]
        src = HERE / 'ref' / c['file']
        out = DEST / f'{name}.jpg'
        cmd = ['ffmpeg', '-nostdin', '-v', 'error', '-ss', str(p['t']), '-i', str(src),
               '-frames:v', '1', '-vf', 'scale=iw*sar:ih,setsar=1', '-q:v', '2',
               '-y', str(out)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not out.exists():
            print(f'🔴 {name}: {r.stderr[:160]}')
            err += 1
            continue
        from PIL import Image
        w, h = Image.open(out).size
        print(f"✓ {name:22} {w}x{h}  元{c['at'] + p['t']}秒  {p.get('note', '')}")
        ok += 1
    print(f'\n抜いた {ok} ／ 失敗 {err}')
    return 1 if err else 0


def cmd_fetch(only=None):
    from PIL import Image
    db = _db()
    DEST.mkdir(parents=True, exist_ok=True)
    ok = skip = err = 0
    for n, r in db.items():
        if r['src'] == 'clip':
            continue
        if only and not any(n.startswith(o) for o in only):
            continue
        out = DEST / f'{n}.jpg'
        if out.exists() and out.stat().st_size > 10000:
            skip += 1
            continue
        try:
            im = Image.open(io.BytesIO(_get(r['url'])))
            im.load()
            if im.mode != 'RGB':
                im = im.convert('RGB')
            if im.width > MAXW:
                im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
            im.save(out, quality=92)
            print(f'✓ {n:<24} {im.width}x{im.height}  {out.stat().st_size / 1024:7.0f} KB')
            ok += 1
        except Exception as e:                              # noqa: BLE001
            print(f'🔴 {n}: {e}')
            err += 1
        time.sleep(0.5)
    print(f'\n落とした {ok} ／ すでに在る {skip} ／ 失敗 {err}')
    return 1 if err else 0


def cmd_check():
    """🔴 PICK・台帳・ファイル・**台本の欄**の4つが揃っているか。揃わなければ止める。"""
    from PIL import Image
    sys.path.insert(0, str(HERE / 'ref' / 'ep11'))
    import parse_script as ps                               # noqa: PLC0415
    want = {c['slot'] for c in ps.parse() if c['slot']}
    have = set(PICK) | set(MISSING) | set(VIDEO_SLOTS)
    lack = sorted(want - have)
    extra = sorted(n for n in PICK if not n.startswith('fb_') and n not in want)

    db = _db()
    bad = small = 0
    for n in PICK:
        f = DEST / f'{n}.jpg'
        if n not in db:
            print(f'🔴 {n}: assets.json に無い')
            bad += 1
            continue
        if not f.exists():
            print(f'🔴 {n}: ファイルが無い')
            bad += 1
            continue
        w, h = Image.open(f).size
        if max(w, h) < 1280:
            print(f'⚠️ {n}: {w}x{h}（長い辺も1280未満＝額装でも小さい）')
            small += 1
    if lack:
        print(f'\n🔴 台本が要求しているのに PICK にも MISSING にも無い欄 {len(lack)}: {lack}')
    if extra:
        print(f'⚠️ 台本に無い名前 {len(extra)}: {extra}')
    nslot = len([n for n in PICK if not n.startswith('fb_')])
    print(f'\n台本の欄 {len(want)} ＝ 写真 {nslot} ＋ 動画 {len(VIDEO_SLOTS)} '
          f'＋ まだ当てが無い {len(MISSING)}（計 {nslot + len(VIDEO_SLOTS) + len(MISSING)}）')
    print(f'PICK {len(PICK)}（うち ひかえ fb_* {len(PICK) - nslot}）／ 台帳 {len(db)} '
          f'／ 欠け {bad} ／ 小さい {small}')
    return 1 if (bad or lack) else 0


def cmd_sheet(pats):
    """640px・2列×3行のシート。⚠️ **シートで決めてよくない型が3つある**
    （図の比例・小さな点・札の切れ）→ [[feedback-sheet-cannot-judge-three-types]]。"""
    from PIL import Image, ImageDraw
    SHEET.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in DEST.glob('*.jpg')
                   if not pats or any(p.stem.startswith(x) for x in pats))
    if not files:
        raise SystemExit('🔴 シートにする絵が無い')
    CW, CH, COLS, ROWS = 640, 400, 2, 3
    per = COLS * ROWS
    for i in range(0, len(files), per):
        chunk = files[i:i + per]
        sh = Image.new('RGB', (CW * COLS, (CH + 26) * ROWS), (16, 16, 18))
        d = ImageDraw.Draw(sh)
        for k, f in enumerate(chunk):
            im = Image.open(f)
            im.thumbnail((CW - 8, CH - 8), Image.LANCZOS)
            x, y = (k % COLS) * CW, (k // COLS) * (CH + 26)
            sh.paste(im, (x + (CW - im.width) // 2, y + (CH - im.height) // 2))
            w, h = Image.open(f).size
            d.text((x + 6, y + CH + 6), f'{f.stem}  {w}x{h}', fill=(235, 235, 235))
        out = SHEET / f'sheet_{i // per + 1:02}.jpg'
        sh.save(out, quality=90)
        print(f'✓ {out}  {len(chunk)}点')
    return 0


def cmd_panel():
    """切り落とし率の並び。`PANEL_AR` は**この回の素材から取り直す**
    → [[feedback-per-episode-constants-go-stale]]。"""
    from PIL import Image
    W, H = 1920, 1080
    rows = []
    for f in sorted(DEST.glob('*.jpg')):
        w, h = Image.open(f).size
        a = w / h
        loss = 1 - (a / (W / H) if a < W / H else (W / H) / a)
        rows.append((loss, a, f.stem, w, h))
    rows.sort()
    for loss, a, n, w, h in rows:
        print(f'  {loss * 100:5.1f}%切れる  AR {a:5.3f}  {n:24} {w}x{h}')
    print(f'\n{len(rows)}点。**はっきりした切れ目**を探して PANEL_AR を決める')
    return 0


def credit_line(name, r):
    """画面の右上に出す1行。🔴 **この回は実名を出す回なので、出典も画面に出す**
    （記憶 `project-jiko-rules-index` §5）。

    ⚠️ **動く映像から抜いた止め絵は、写真の出典を名乗らない。**映像の出典を出す
    （出所を偽ることになる → `scene_jiko.credit_of` の 2026-08-01 の注）。
    """
    if r['src'] == 'clip':
        c = json.loads(CLIPS_JSON.read_text(encoding='utf-8'))[r['clip']]
        return c['credit'] + '（記録映像より）'
    who = re.sub(r'\s*\(.*?\)\s*', '', _plain(r.get('author') or 'NASA')).strip() or 'NASA'
    # Commons の Artist 欄は人名でなく機関名のことが多い。NASA の各センターは NASA と名乗る
    # （JSC＝ジョンソン宇宙センター、KSC＝ケネディ宇宙センターはどちらも NASA の施設）。
    if re.search(r'NASA|National Aeronautics|Johnson Space|Kennedy Space|\bJSC\b|\bKSC\b',
                 who, re.I):
        who = 'NASA'
    # ⚠️ 「撮影者不明」を NASA と名乗らない（出所を作らない）
    #    → [[feedback-fallback-stills-must-match-the-era]] と同じ筋で、**分かっていないことは書く**
    elif re.search(r'unknown|not provided', who, re.I):
        who = ORIGIN.get(name) or '撮影者不明'
    elif re.search(r'White House', who, re.I):
        who = 'ホワイトハウス写真室'
    y = r.get('year')
    return f"出典：{who}{f'（{y}年）' if y else ''}"


# 🔴 Commons の Artist 欄が「不明」の点は、**その点の本当の出どころ**を手で当てる。
#    ⚠️ NASA と名乗らせない（§105 を名乗るなら根拠が要る）。値は `assets.json` の `page` を見て決めた。
ORIGIN = {
    'ascent_1': 'NASA（70mm 追尾カメラ）',
    'ice_team': '米国立公文書館（NARA 593693）',
}


def cmd_credits(write=False):
    db = _db()
    out = {f'ep11/{n}.jpg': credit_line(n, r) for n, r in db.items()}
    p = DEST / 'credits.json'
    if write:
        p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'✓ {p} に {len(out)} 行')
    # 🔴 「使うカット」は `cuts.SPEC` から機械で引く（手で書かない＝写し間違いが起きない）
    sys.path.insert(0, str(HERE / 'tools'))
    import cuts                                            # noqa: PLC0415
    used: dict[str, list[str]] = {}
    for cid, sp in cuts.SPEC.items():
        ph = sp.get('photo')
        if ph and ph.startswith('ep11/'):
            used.setdefault(Path(ph).stem, []).append(cid)

    print('| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころ |')
    print('|---|---|---:|---|---|---|')
    for n, r in sorted(db.items()):
        src = (r.get('title') or r.get('id')
               or (f"記録映像 {r.get('clip')} +{r.get('t')}秒" if r['src'] == 'clip' else ''))
        who = re.sub(r'^出典：', '', credit_line(n, r)).split('（')[0]
        print(f"| `{n}` | {' '.join(sorted(used.get(n, []))) or '🔴未使用'} | "
              f"{r.get('year') or '不明'} | {r.get('lic', '')} | {who} | {src} |")
    return 0


def main():
    a = sys.argv[1:] or ['check']
    cmd, rest = a[0], a[1:]
    if cmd == 'info':
        return cmd_info()
    if cmd == 'fetch':
        return cmd_fetch(rest or None)
    if cmd == 'stills':
        return cmd_stills(rest or None)
    if cmd == 'check':
        return cmd_check()
    if cmd == 'sheet':
        return cmd_sheet(rest)
    if cmd == 'panel':
        return cmd_panel()
    if cmd == 'credits':
        return cmd_credits('--write' in rest)
    raise SystemExit(f'🔴 知らない命令: {cmd}')


if __name__ == '__main__':
    sys.exit(main())
