# -*- coding: utf-8 -*-
"""ep8_assets.py — 8本目（コロンビア号）の**写真の束**を作る（2026-09-14 ⑤b-1 新設）。

■ なぜ要るか
  ②は「2003年・幅1280以上 1,006点」まで**数えた**だけで、束は1点も作っていない。
  `ref/ep8/` には画像が1枚も無く、台本の**実写103カット**が全部空のまま。
  ここで「選ぶ・落とす・出典を作る」を1本にまとめる。

■ ⚠️ 7本目（`ep7_assets.py`）とは出どころが違う
  7本目は Commons（CC BY が混ざるので撮影者名が要る）。
  8本目は **NASA 画像庫と archive.org の NASA 束だけ**＝米連邦職員の職務著作で
  原則パブリックドメイン。⚠️ ただし例外があるので `center`/`creator` を出典に出す
  （→ [[feedback-pd-label-hides-two-different-grounds]]：PD の根拠は1種類ではない）。

■ 🔴 守っていること
  1. **台帳に無い nasa_id は黙って飛ばさず止める**（fail closed）。
     「落ちていない写真を当てたカット」は焼くまで気づけない。
  2. **`date_created` を必ず出典に出す**＝[[feedback-fallback-stills-must-match-the-era]]。
     事故の前後・別ミッションの写真を「その場面」として出さないため。
     ⚠️ **門番は1件も鳴らない。**副題を書く人間が見るしかない。
  3. 出力はファイルへ。`| tail` でつながない（[[feedback-pipes-mask-exit-codes]]）。

    python qa_out/ep8_assets.py check     # PICK が台帳と合っているか（落とさない）
    python qa_out/ep8_assets.py fetch     # ref/ep8/ に落とす
    python qa_out/ep8_assets.py fetch --only=orb   # 名前の頭で絞る
    python qa_out/ep8_assets.py credits   # scene_jiko.EP8_PHOTO と CREDITS.md の行
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from ep8_pick import load, caption                       # noqa: E402

DEST = HERE / 'ref' / 'ep8'
UA = 'Mozilla/5.0 (zukai-engine ep8 assets)'

# ══════════════════════════════════════════════════════════
#  🔴 PICK ── 欄の名前 → nasa_id
# ══════════════════════════════════════════════════════════
# ここに書いた名前が `ref/ep8/<名>.jpg`・`cuts/ss.py` の定数・
# `scene_jiko.EP8_PHOTO` の鍵の3つを兼ねる。**食い違うと写真が出ないか出典が出ない。**
# 検算＝`python qa_out/ep8_assets.py check`。
#
# ⚠️ 「同型」「前の飛行」の写真（別ミッション・別の年）には名前の末尾に理由を書いた。
#    副題で必ずその年を名乗ること。
PICK = {
    # ── 射点と打ち上げ（KSC・2003-01-15/16）──────────────
    'pad_rss': 'KSC-03pd0070',          # 回転式整備構台を開いた射点（1/15）
    'pad_stack': 'KSC-03pd0076',        # 3つの部品が見える全景（1/15）
    'et_orange': 'KSC-03pd0071',        # オレンジ色の外部タンク（1/15）
    'et_surface': 'KSC-03pd0074',       # タンクと固体ロケットの表面（1/15）
    'et_top': 'KSC-03pd0075',           # タンクの頂部（1/15）
    'launch_wide': 'KSC-03pd0134',      # 木立の上へ（1/16）
    'launch_flames': 'KSC-03pd0135',    # 炎と煙（1/16・縦 1968x3000）
    'launch_sky': '0300307',            # 快晴の空へ（MSFC・1/16）
    # ── 衝突のコマ（NASA 公式の追跡カメラ）──────────────
    'strike_wide': 'KSC-03pd0242',      # 「T-0 から約80〜84秒」
    'strike_near': 'KSC-03pd0243',      # 「約81〜82秒・バイポッド付近から」
    # ── 乗員（地上）────────────────────────────────
    'crew_portrait': 'HSF-photo-jsc2002e30459',   # 7人の記念写真（2002-07-25）
    'crew_arrival': 'KSC-03pd0058',     # KSC 到着後（1/12）
    'crew_astrovan': 'KSC-03pd0110',    # 射点へ向かう（1/16）
    'suit_chawla': 'KSC-03pp0144',      # ホワイトルームでの着装（1/16）
    'suit_clark': 'KSC-03pp0145',       # 同上（1/16）
    # ── 軌道上（乗員が撮った電子スチル・3032x2064）──────
    'orb_chawla': 'S107E05001',
    'orb_husband': 'S107E05002',
    'orb_husband_seat': 'S107E05003',
    'orb_clark_arms': 'S107E05006',
    'orb_chawla_hab': 'S107E05010',
    'orb_mccool': 'S107E05014',
    'orb_chawla_clark': 'S107E05018',
    'orb_clark_husband': 'S107E05020',
    'orb_clark_window': 'S107E05021',
    'orb_brown': 'S107E05025',
    'orb_mccool_afd': 'S107E05026',
    'orb_ramon': 'S107E05029A',
    'orb_anderson': 'S107E05033',
    'orb_crew7': 'HSF-photo-sts107-735-032',      # 7人が浮く恒例の記念写真
    'orb_anderson_read': 'HSF-photo-sts107-301-025',
    'orb_earth': '0301002',             # 機内から撮った日の出（1/22）
    'columbia_orbit': 'HSF-photo-jsc2003e13222',  # 軌道のコロンビア号（地上望遠・1/28）
    # ── 管制室 ─────────────────────────────────────
    'mcc_launch': 'HSF-photo-jsc2003e02609',      # 打ち上げ当日の管制室（1/16）
    'mcc_feb1': 'HSF-photo-jsc2003e03368',        # 🔴 2月1日の管制室
    'fd_cain': 'HSF-photo-jsc2003e02610',         # 飛行主任 LeRoy Cain（1/16）
    'capcom': 'HSF-photo-jsc2003e02600',          # 乗員と話す席（CAPCOM・1/16）
    'fd_engelauf': 'HSF-photo-jsc2003e02611',
    # ── 東テキサスの捜索（archive.org にしか無い）─────────
    'search_line': 'HSF-photo-jsc2003-00151',     # 列を組んで野を歩く
    'search_brief': 'HSF-photo-jsc2003-00119',    # 出発前の説明
    'search_forest': 'HSF-photo-jsc2003-00127',   # 森林局の捜索者
    'search_queue': 'HSF-photo-jsc2003e29065',    # 食事の列
    'search_map': 'HSF-photo-jsc2003e28823',      # 地図を見る
    'search_howell': 'HSF-photo-jsc2003e26420',   # JSC所長も捜索に加わる
    'evidence_corsicana': 'HSF-photo-jsc2003e28846',   # 証拠置き場のタイル
    'engine_dig': 'HSF-photo-jsc2003e28147',      # 掘る前の記録
    'engine_found': 'HSF-photo-jsc2003e28148',    # 掘り出した主エンジン
    'barksdale': 'HSF-photo-jsc2003e14383',       # バークスデール基地の格納庫
    # ── 格納庫での再構成（KSC・RLV Hangar）──────────────
    'hangar_floor': 'KSC-03pd1070',     # 床一面の破片（4/14）
    'hangar_grid': 'KSC-03pd0875',      # 床の格子が埋まっていく（3/27）
    'hangar_caib': 'KSC-03pd0403',      # 委員が破片を見る（2/13）
    'hangar_exam': 'KSC-03pd0407',      # 破片を調べる（2/14）
    'le_fixture': 'KSC-03pd1157',       # 前のふちを並べる治具（4/17・縦）
    'le_fixture2': 'KSC-03pd1156',      # 同（4/17・横）
    'debris_truck': 'KSC-03pd1401',     # 最後の輸送（5/6）
    # ── 衝突試験（SwRI・2003-06-06）──────────────────
    'test_panel': 'HSF-photo-jsc2003e40558',
    'test_panel2': 'HSF-photo-jsc2003e40593',
    'test_hole': 'HSF-photo-jsc2003e40715_nr',
    # ── 委員会と報告書 ─────────────────────────────
    'caib_hearing': 'KSC-03pd0831',     # 第3回公聴会（3/25）
    'caib_gehman': 'KSC-03pd0836',      # 委員長（3/25）
    'report_copy': 'HSF-photo-jsc2003e55050',     # 出たばかりの報告書（8/26）
    'report_copy2': 'HSF-photo-jsc2003e55049',
    'report_gehman': 'HSF-photo-jsc2003e55047',
    'report_mail': 'KSC-03pd3115',      # 配るために積まれた報告書（11/6）
    'ham_caib': 'HSF-photo-jsc2003e09152',        # ミッション運営チーム議長が委員会で話す
    'dittemore': 'HSF-photo-jsc2003e31694',       # シャトル計画責任者（4/23）
    # ── 記録装置 ────────────────────────────────
    'oex_recorder': 'HSF-photo-s88-44993',        # ⚠️ 1988年の**同型**の記録装置
    # ── 別の年のコロンビア号（⚠️ 副題で必ず年を名乗る）─────
    'slf_landing': 'HSF-photo-sts109-s-013',      # 滑走路33に降りる（2002-03-12）
    'slf_approach': 'HSF-photo-sts109-s-016',     # 接地直前（2002-03-12）
    'columbia_middeck': 'HSF-photo-s109e6032',    # コロンビア号の中デッキ（2002-03-11）
    'cargo_tool': 'HSF-photo-s109e5386',          # 貨物室で工具を確かめる（2002-03-05）
    # ── アトランティス号（救出案の相手）───────────────
    'atlantis_nose': 'KSC-03pd0369',    # 組立棟のアトランティス号の機首（2/12）
    'atlantis_stack': 'KSC-03pd0372',   # 固体ロケットと外部タンクを結合（2/13・縦）
    # ── そのほか ───────────────────────────────
    'recovery_team': 'KSC-03pd0270',    # 回収管理チームの作業（2/5）
    'news_center': 'KSC-03pd0252',      # 2月1日、報道各社（2/1）
}


def ledger():
    return {it['nasa_id']: it for it in load()}


def cmd_check():
    """🔴 PICK と台帳の突き合わせ。**無いIDがあれば exit 1。**"""
    led = ledger()
    bad, small = [], []
    print(f'PICK {len(PICK)} 件 ／ 台帳 {len(led)} 件\n')
    for name, nid in PICK.items():
        it = led.get(nid)
        if it is None:
            bad.append((name, nid))
            print(f'🔴 {name:<20} {nid:<30} 台帳に無い')
            continue
        w, h = it.get('w') or 0, it.get('h') or 0
        flag = ''
        if w < 1280 and h < 1280:
            small.append(name)
            flag = '  ⚠️ 幅も高さも1280未満'
        print(f'   {name:<20} {nid:<30} {w}x{h} {it.get("date_created","")[:10]}{flag}')
    dup = [n for n in set(PICK.values()) if list(PICK.values()).count(n) > 1]
    if dup:
        print(f'\n⚠️ 同じ nasa_id を2つの名前で採っている: {dup}')
    print(f'\n無いID {len(bad)} 件 ／ 小さすぎ {len(small)} 件')
    return 1 if bad else 0


def _get(url, dest, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            dest.write_bytes(data)
            return len(data)
        except Exception as e:                          # noqa: BLE001
            if i == tries - 1:
                raise
            print(f'   再試行 {i + 1}/{tries}: {e}')
            time.sleep(2 + i * 2)
    return 0


def cmd_fetch(only=None):
    led = ledger()
    DEST.mkdir(parents=True, exist_ok=True)
    n_ok = n_skip = n_err = 0
    for name, nid in PICK.items():
        if only and not name.startswith(only):
            continue
        it = led.get(nid)
        if it is None:
            print(f'🔴 {name}: 台帳に {nid} が無い（check を先に通す）')
            n_err += 1
            continue
        out = DEST / f'{name}.jpg'
        if out.exists() and out.stat().st_size > 10000:
            n_skip += 1
            continue
        url = it.get('orig')
        if not url:
            print(f'🔴 {name}: 原本のURLが台帳に無い')
            n_err += 1
            continue
        try:
            sz = _get(url, out)
            print(f'✓ {name:<20} {sz / 1024:8.0f} KB  {nid}')
            n_ok += 1
        except Exception as e:                          # noqa: BLE001
            print(f'🔴 {name}: {e}')
            n_err += 1
    print(f'\n落とした {n_ok} ／ すでに在る {n_skip} ／ 失敗 {n_err}')
    return 1 if n_err else 0


_MON = dict(january=1, february=2, march=3, april=4, may=5, june=6, july=7,
            august=8, september=9, october=10, november=11, december=12,
            jan=1, feb=2, mar=3, apr=4, jun=6, jul=7, aug=8, sep=9, oct=10,
            nov=11, dec=12)


def _date_of(it):
    """撮影日。**`date_created` をそのまま信じない。**

    🔴 archive.org 側（`HSF-photo-*`）の `date_created` は**年しか持っていない**ので
       「2002-01-01」と出る。そのまま出典に書くと**撮影日を偽ることになる**
       （`crew_portrait` は実際には 2002年7月25日）。
       説明文の頭に「(25 July 2002)」の形で本当の日付が入っているので、そこから採る。
    ⚠️ 採れなければ**年だけを名乗る**。日を捏造しない。
    """
    cap = caption(it)
    m = re.search(r'\((?:For Release,?\s*)?(\d{1,2})\s+([A-Za-z]+)\.?,?\s+(\d{4})\)', cap)
    if m and m.group(2).lower().rstrip('.') in _MON:
        return int(m.group(3)), _MON[m.group(2).lower().rstrip('.')], int(m.group(1))
    m = re.search(r'\(([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})\)', cap)
    if m and m.group(1).lower().rstrip('.') in _MON:
        return int(m.group(3)), _MON[m.group(1).lower().rstrip('.')], int(m.group(2))
    # 「(April 2003)」＝月まで
    m = re.search(r'\(([A-Za-z]+)\.?\s+(\d{4})\)', cap)
    if m and m.group(1).lower().rstrip('.') in _MON:
        return int(m.group(2)), _MON[m.group(1).lower().rstrip('.')], None
    # 🔴 「(1988)」＝年だけ。**ここが効かないと `oex_recorder`（1988年の同型の記録装置）が
    #    archive.org の登録年を拾って「2003年」と名乗る**＝撮影年を偽る。
    m = re.search(r'\((\d{4})\)', cap)
    if m:
        return int(m.group(1)), None, None
    d = (it.get('date_created') or '')[:10]
    if len(d) == 10 and d[5:] != '01-01':
        return int(d[:4]), int(d[5:7]), int(d[8:10])
    if len(d) >= 4:
        return int(d[:4]), None, None
    return None, None, None


def _credit(it):
    """PD の根拠は1種類ではない（→ [[feedback-pd-label-hides-two-different-grounds]]）。
    NASA の職務著作として出すが、**撮影機関（center）は必ず出す。**"""
    who = (it.get('creator') or '').strip()
    center = (it.get('center') or '').strip()
    org = 'NASA'
    if center and center not in ('IA',):
        org = f'NASA {center}'
    y, mo, dd = _date_of(it)
    if y and mo and dd:
        when = f'（{y}年{mo}月{dd}日）'
    elif y and mo:
        when = f'（{y}年{mo}月）'
    elif y:
        when = f'（{y}年）'
    else:
        when = ''
    src = f'出典：{org}{when}／パブリックドメイン'
    if who:
        src = f'出典：{org}／撮影 {who}{when}／パブリックドメイン'
    return src


def cmd_credits():
    led = ledger()
    print('# tools/scene_jiko.py の EP8_PHOTO に貼る（手で書き換えない）\n')
    print('EP8_PHOTO = {')
    for name, nid in PICK.items():
        it = led.get(nid)
        if it is None:
            print(f'    # 🔴 {name}: {nid} が台帳に無い')
            continue
        print(f'    "ep8/{name}.jpg": "{_credit(it)}",')
    print('}')
    print('\n\n# ref/CREDITS.md §コロンビア号 の表\n')
    print('| 欄 | nasa_id | 実寸 | 撮影日 | 何が写っているか |')
    print('|---|---|---|---|---|')
    for name, nid in PICK.items():
        it = led.get(nid)
        if it is None:
            continue
        cap = caption(it).replace('|', '／')
        cap = cap.split('---')[-1].strip()[:90]
        print(f'| `{name}` | {nid} | {it.get("w")}×{it.get("h")} | '
              f'{(it.get("date_created") or "")[:10]} | {cap} |')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=('check', 'fetch', 'credits'))
    ap.add_argument('--only', default=None)
    a = ap.parse_args()
    if a.cmd == 'check':
        sys.exit(cmd_check())
    if a.cmd == 'fetch':
        sys.exit(cmd_fetch(a.only))
    sys.exit(cmd_credits())


if __name__ == '__main__':
    main()
