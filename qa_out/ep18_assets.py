# -*- coding: utf-8 -*-
"""ep18_assets.py — 18本目（スレッシャー号のリメイク）の**写真の束**を作る（2026-10-04 ⑤b-7a 新設）。

`qa_out/ep16_assets.py`（16本目）の形を写した。ここでやるのは「名前を付ける・札と縁を切り落とす・幅3000px に縮める・
権利を表にする」だけ。報告書の頁（`pages`）と動く映像（`clips.json`）は ⑤b-7b で足す。

■ 素材（すべて米海軍の職務著作＝PD・17 U.S.C. §105）
  ① 旧版（3本目）の束 `ref/thresher/`（**読むだけ**＝旧版の記録を動かさない・materials.md §1）から写す点
     ＝NARA 289-T（RG 289・1963〜64年の捜索のアルバム・NARA の表示 Use: Unrestricted）・NARA 428-N-1057645・
       Commons の旧版4点（SHA-1 を Commons の原本と照らした＝2026-10-04 一致）・記録映画 85185 のコマ3枚
  ② Commons の新しい8点（`ref/ep18/img/`・**カズヤくんの了承のあとに `fetch` で取る**＝取るまで build は飛ばす）
■ 🔴 切り落とすもの（2026-10-04 ⑤b-7a に OCR〈`tools/ocr_win.ps1`〉と 640px のシートで見て決めた・元の画素の箱）
  ・289-T の英字の説明札（貼り札）＝OCR の文字の箱の外側に紙の縁が 20〜40px ある＝その外で切る
  ・艦首の正面（428-N）の台紙・上の手書きの番号・左下の札「24 July 1961 …」
  ・就役式（1961-08-03）の左の**座った観客（私人）**＝x 385 より左を切る（原寸で顔 約10px＝見分けられないが、寄りで大きくなる）
  ・t14 は1枚の頁に写真が2枚＝上の写真（セイルの593）だけ
  ・記録映画のコマは画素が縦長（SAR 10:11・NARA の 720×480）＝655×480 に直す（映像方針 §8）

    python qa_out/ep18_assets.py build [名…]   # ref/ep18/<名>.jpg ＋ assets.json
    python qa_out/ep18_assets.py check          # PICK・assets.json・ファイルが揃っているか
    python qa_out/ep18_assets.py panel          # 縦横比の並び（`cuts/ss.py` の PANEL_AR を決める材料）
    python qa_out/ep18_assets.py credits [--write]   # credits.json と ref/CREDITS.md の18本目の節
    python qa_out/ep18_assets.py fetch --yes    # Commons の新しい8点を取る（🔴 了承のあとだけ）
"""
from __future__ import annotations

import hashlib
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OLD = HERE / 'ref' / 'thresher'          # 旧版の束（読むだけ）
NEW = HERE / 'ref' / 'ep18' / 'img'      # Commons の新しい8点（git の外）
DEST = HERE / 'ref' / 'ep18'
DB = DEST / 'assets.json'
CREDITS_JSON = DEST / 'credits.json'
CREDITS_MD = HERE / 'ref' / 'CREDITS.md'
MAXW = 3000
UA = 'zukai-engine/1.0 (accident-documentary research; https://github.com/torotorotolo/zukai-engine)'
COMMONS = 'https://commons.wikimedia.org/wiki/'
NARA = 'https://catalog.archives.gov/id/'


def L(file, cuts, year, hold, url, ident, crop=None, sar=None, note='', who='米海軍'):
    """旧版の束 `ref/thresher/<file>` の1点。crop＝元の画素の箱 (x0, y0, x1, y1)。sar＝画素の縦横比（記録映画のコマ）。
    ident＝画面の出典に出す識別子（NARA の番号・USN の番号）。year＝撮影年（割れる・分からないなら None）"""
    return dict(src='old', file=file, cuts=cuts.split(), year=year, hold=hold, url=url, ident=ident,
                crop=crop, sar=sar, note=note, who=who)


def C(title, cuts, year, ident, note='', who='米海軍'):
    """Commons の新しい1点（`ref/ep18/img/` に取る）。title＝Commons の題名（File: を除く）"""
    return dict(src='commons', title=title, cuts=cuts.split(), year=year, ident=ident, note=note, who=who,
                hold=f'Wikimedia Commons「{title}」', url=COMMONS + 'File:' + urllib.parse.quote(title.replace(' ', '_')))


T289 = 'NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」'
U289 = NARA + '138924735'
F85185 = 'NARA 85185（RG 428）「USS THRESHER (SSN-593)」記録映画 1963年3月'

# 名前 → 素材。当てるカット（cuts）は章ファイルの PLAN と照らす（台本の画の欄）
PICK = {
    # ── 事故の前（1960〜62年）────────────────────────────────────
    'bow_1961': L('nara_428-N-1057645.jpg', 'c114 c709', 1961, 'NARA 175539769（428-N-1057645）', NARA + '175539769',
                  'NARA 428-N-1057645', crop=(90, 200, 2230, 2590),
                  note='1961年7月24日 真正面から見た艦首（札「DIRECT BOW VIEW」と台紙・手書きの番号は切った）'),
    'commission_1961': L('cm_SSN593_service_entering.jpg', 'c116 c215', 1961, 'Wikimedia Commons「SSN593 service entering.jpg」',
                         COMMONS + 'File:SSN593_service_entering.jpg', None, crop=(385, 0, 1750, 1211),
                         note='1961年8月3日 就役の直前・岸壁に式台を組む造船所の人と、甲板の白服の乗員（左の座った観客＝私人は切った）'),
    'launch_1960': L('cm_USN_1048964_USS_Thresher__SSN-593_.jpg', 'c201', 1960,
                     'Wikimedia Commons「USN 1048964 USS Thresher (SSN-593).jpg」',
                     COMMONS + 'File:USN_1048964_USS_Thresher_(SSN-593).jpg', 'USN 1048964',
                     note='1960年7月9日 進水（建屋から水へ出る艦首）・岸の人は全員が後ろ姿か横向き（原寸）'),
    'underway_1961': L('cm_USS_Thresher__SSN-593_.jpg', 'cb23', 1961, 'Wikimedia Commons「USS Thresher (SSN-593).jpg」',
                       COMMONS + 'File:USS_Thresher_(SSN-593).jpg', None,
                       note='1961年7月24日 海上を行くスレッシャー（右舷の前から・海軍歴史センター）'),
    'running_t2': L('thr_t2.jpg', 'c220 c423 c627', None, T289 + ' 289-T-2', U289, 'NARA 289-T-2',
                    crop=(0, 240, 2400, 1400),
                    note='浮上して走るスレッシャー（網点の印刷）＝アルバムの謝辞の頁の写真（右下の札「ACKNOWLEDGMENT …」と上の白い余白は切った）。撮影年は書かれていない'),
    'shipyard_sail_t14': L('thr_t14.jpg', 'c203', None, T289 + ' 289-T-14', U289, 'NARA 289-T-14', crop=(0, 0, 1555, 752),
                           note='造船所の写真：セイルの「593」と潜舵（頁の上の写真だけ・札「Shipyard photograph.」は切った）'),
    'shipyard_stern_t22': L('thr_t22.jpg', 'c208 c611', None, T289 + ' 289-T-22', U289, 'NARA 289-T-22',
                            note='造船所の写真：ドックの艦尾（上の舵・推進器の軸・横舵・足場）'),
    # ── 事故のあと（1963〜64年の海の底）───────────────────────────────
    # ⚠️ 試し焼き 37206148473：上の縁に白い細い帯が残った（y 10 から切った）＝y 30 から
    'bottle_t37': L('thr_t37.jpg', 'c722', 1964, T289 + ' 289-T-37', U289, 'NARA 289-T-37', crop=(90, 30, 1790, 1592),
                    note='1964年 海の底の空気のボンベ（上にカメラのそりの羅針・NRL/MIZAR）'),
    'hull_aft_t33': L('thr_t33.jpg', 'c805', 1964, T289 + ' 289-T-33', U289, 'NARA 289-T-33', crop=(0, 250, 1800, 1720),
                      note='1964年 艦の後ろ寄りの外殻の継ぎ写真（モザイク・NRL/MIZAR）'),
    'break78_t29': L('thr_t29.jpg', 'c812', 1964, T289 + ' 289-T-29', U289, 'NARA 289-T-29', crop=(0, 0, 1650, 1340),
                     note='1964年 78番目の骨組みで切れた所を真上から（TRIESTE II）'),
    'tail_t23': L('thr_t23.jpg', 'c819', 1964, T289 + ' 289-T-23', U289, 'NARA 289-T-23', crop=(0, 0, 1790, 1174),
                  note='1964年 艦尾の継ぎ写真（103番目の骨組みのあたりがつぶれた所・NRL/MIZAR）'),
    'break78_top_t30': L('thr_t30.jpg', 'c822', 1964, T289 + ' 289-T-30', U289, 'NARA 289-T-30', crop=(0, 0, 1430, 1351),
                         note='1964年 78番目の骨組みで切れた所の前の上甲板（TRIESTE II）'),
    'sail_t16': L('thr_t16.jpg', 'c906', 1964, T289 + ' 289-T-16', U289, 'NARA 289-T-16', crop=(0, 0, 1850, 1334),
                  note='1964年 海の底のセイルの右の側面（NRL/MIZAR）。札は「593 の最初の2桁」と書くが、絵では数字は読めない'),
    'page24': L('thr_page24.jpg', 'c911', 1964, T289 + ' 289-T-24（頁全体）', U289, 'NARA 289-T-24',
                note='289-T-24 のアルバムの頁全体（上と下の角に黒い塗り＝機密の印を消した跡・右下に説明札）'),
    'stern_plane_t26': L('thr_t26.jpg', 'c914', 1964, T289 + ' 289-T-26', U289, 'NARA 289-T-26', crop=(330, 0, 2400, 1665),
                         note='1964年 海の底の右の横舵と聴音器（左の札は切った）'),
    'rudder_t24': L('thr_t24.jpg', 'c920', 1964, T289 + ' 289-T-24', U289, 'NARA 289-T-24', crop=(1000, 0, 2340, 690),
                    note='1964年 海の底の上の舵の喫水の数字（4〜9・30〜34＝札の上まで・NRL/MIZAR）'),
    'plating_t39': L('thr_t39.jpg', 'ca05', 1963, T289 + ' 289-T-39', U289, 'NARA 289-T-39', crop=(190, 0, 1760, 1530),
                     note='1963年 外殻の板（約3m 四方・ラモント地質観測所の調査船コンラッドの写真）'),
    'debris_711302': L('cm_330-PSA-110-63__USN_711302___22171571340_.jpg', 'ca06', 1963,
                       'Wikimedia Commons「330-PSA-110-63 (USN 711302) (22171571340).jpg」',
                       COMMONS + 'File:330-PSA-110-63_(USN_711302)_(22171571340).jpg', 'USN 711302',
                       note='1963年 調査船の水中カメラが撮った海の底の破片（国防総省の発表の写真・セピア）'),
    'bow_plating_t5': L('thr_t5.jpg', 'ca13', 1963, T289 + ' 289-T-5', U289, 'NARA 289-T-5', crop=(0, 0, 1760, 990),
                        note='1963年 艦首の外板（初代トリエステの写真）。札の喫水の数字は絵では読めない'),
    'tracks_t41': L('thr_t41.jpg', 'ca20', 1964, T289 + ' 289-T-41', U289, 'NARA 289-T-41', crop=(190, 60, 1790, 960),
                    note='1964年 トリエステ2世が海の底に残した跡（捨てたおもりの黒い点・引きずった跡）'),
    # ── 記録映画 85185 のコマ（静止画。⑤b-7b で動く映像に替える案＝カズヤくんの返事しだい）─────────────
    'film_a': L('thr_film593_a.jpg', 'c301 c601', 1963, F85185, NARA + '85185', 'NARA 85185', sar=10 / 11,
                note='記録映画のコマ（622秒）：浮上して走るスレッシャー・セイルの593（カラー）', who='米海軍の記録映画'),
    'film_b': L('thr_film593_b.jpg', 'cb01', 1963, F85185, NARA + '85185', 'NARA 85185', sar=10 / 11,
                note='記録映画のコマ（628秒）：セイルの上の乗員（公務）', who='米海軍の記録映画'),
    'film_c': L('thr_film593_c.jpg', 'c212', 1963, F85185, NARA + '85185', 'NARA 85185', sar=10 / 11,
                note='記録映画のコマ（631秒）：セイルの593', who='米海軍の記録映画'),
    # ── Commons の新しい8点（🔴 カズヤくんの了承のあとに fetch で取る）────────────────────
    'skylark_front': C('USS Skylark (ASR-20).jpg', 'c304 c523', None, None,
                       note='救難艦スカイラークの正面（網点の印刷・1950年代後半〜60年代＝撮影年は割れる）'),
    'skylark_side': C('USS Skylark (ASR-20) underway c1950.jpg', 'c306 c511 c415', None, None,
                      note='海上のスカイラーク（横から・1951年ごろ＝撮影年は「ごろ」）'),
    'door_711348': C('330-PSA-191-63 (USN 711348) (22171493730).jpg', 'ca10', 1963, 'USN 711348',
                     note='1963年8月24日 トリエステの2回目の潜航で撮った艦の中の水密扉'),
    'pipe_711350': C('330-PSA-191-63 (USN 711350) (22172651149).jpg', 'ca11', 1963, 'USN 711350',
                     note='1963年 トリエステが回収した真鍮の管（刻印「593 Boat」）'),
    'trieste2_sea': C('330-PSA-309-64 (KN-9302C) (22766865552).jpg', 'ca14', 1964, 'KN-9302C',
                      note='1964年 海上のトリエステ2世（説明文の「ボストンの造船所」と絵〈海の上〉が合わない＝場所は名乗らない）'),
    'trieste2_drawing': C('330-PSA-276-63 (USN 711389) (22517726786).jpg', 'ca17', 1963, 'USN 711389',
                          note='1963年 海軍が描いたトリエステ2世の想像図'),
    'fish_1104636': C('330-PSA-309-64 (USN 1104636-D) (22592418930).jpg', 'ca18', 1964, 'USN 1104636-D',
                      note='1964年 ミザーから降ろされる曳航カメラ「The Fish」'),
    'search_ships_1963': C('Ships searching for USS Thresher (SSN-593), 15 April 1963 (NH 97555).jpg', 'cb09', 1963, 'NH 97555',
                           note='1963年4月15日 スレッシャーの沈んだあたりを回る海軍の艦'),
}
GROUND = 'PD（米連邦の職務著作 17 U.S.C. §105）'


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def _db():
    return json.loads(DB.read_text(encoding='utf-8')) if DB.exists() else {}


def _src_path(r):
    if r['src'] == 'old':
        return OLD / r['file']
    return NEW / r['title']


def cmd_build(only=None):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    db = _db()
    skip = []
    fetched = json.loads((NEW / 'fetched.json').read_text(encoding='utf-8')) if (NEW / 'fetched.json').exists() else {}
    for name, r in PICK.items():
        if only and name not in only:
            continue
        sp = _src_path(r)
        if not sp.exists():
            skip.append(name)
            continue
        if r['src'] == 'commons':
            f = fetched.get(r['title'])
            if not f or hashlib.sha1(sp.read_bytes()).hexdigest() != f['sha1']:
                raise SystemExit(f"🔴 {name}: {sp.name} の SHA-1 が Commons の原本と違う（取り直す）")
        with Image.open(sp) as im0:
            im = im0.convert('RGB')
        w0, h0 = im.size
        box = r.get('crop') or (0, 0, w0, h0)
        im = im.crop(box)
        if r.get('sar'):
            im = im.resize((round(im.width * r['sar']), im.height), Image.LANCZOS)
        if im.width > MAXW:
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
        out = DEST / f'{name}.jpg'
        im.save(out, quality=92)
        db[name] = dict(src=r['src'], file=sp.name, cut=' '.join(r['cuts']), note=r['note'],
                        box=[round(box[0] / w0, 4), round(box[1] / h0, 4), round(box[2] / w0, 4), round(box[3] / h0, 4)],
                        crop_px=list(box), sar=r.get('sar'), w=im.width, h=im.height, md5=_md5(out), src_md5=_md5(sp),
                        lic='Public domain', frame=False, author=r['who'], ground='A', year=r['year'],
                        hold=r['hold'], url=r['url'], ident=r.get('ident'))
        print(f"✓ {name:20} {im.width}x{im.height}  ← {sp.name}  切り={box}{'・SAR を直した' if r.get('sar') else ''}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'→ {DB}（{len(db)}点）')
    if skip:
        print(f"⚠️ 元のファイルが無いので飛ばした {len(skip)}点（Commons の新しい点＝了承のあとに fetch）: {' '.join(skip)}")
    return 0


def cmd_check():
    if not DB.exists():
        raise SystemExit('🔴 assets.json が無い（build を先に）')
    db = _db()
    bad = 0
    for name in PICK:
        p = DEST / f'{name}.jpg'
        if name not in db or not p.exists():
            print(f'🔴 {name}: 束に無い')
            bad += 1
            continue
        if _md5(p) != db[name]['md5']:
            print(f'🔴 {name}: md5 が assets.json と違う（手で差し替えた？）')
            bad += 1
    for e in sorted(set(db) - set(PICK)):
        print(f'⚠️ assets.json に PICK に無い名前: {e}')
    # 当てるカットが PLAN の写真のカットと1対1か（台本の画の欄＝PLAN が正本）
    sys.path.insert(0, str(HERE / 'tools'))
    import cuts
    want = {c for c, p in cuts.PLAN.items() if p['kind'] == '写真'}
    have = {c for r in PICK.values() for c in r['cuts']}
    print(f'PLAN の写真 {len(want)}カット・PICK が当てる {len(have)}カット・まだ当てていない {len(want - have)}: '
          f"{' '.join(sorted(want - have))}")
    if have - want:
        print(f"🔴 PLAN で写真でないカットに当てている: {' '.join(sorted(have - want))}")
        bad += 1
    print('✓ 揃っている' if not bad else f'🔴 {bad}件')
    return 1 if bad else 0


def cmd_panel():
    db = _db()
    for n, r in sorted(db.items(), key=lambda kv: kv[1]['w'] / kv[1]['h']):
        ar = r['w'] / r['h']
        loss = 1 - (ar / (16 / 9) if ar < 16 / 9 else (16 / 9) / ar)
        print(f"AR {ar:.3f}  {n:20} {r['w']}x{r['h']}  全画面で {loss:.1%} 切れる  {r['lic']}")
    return 0


def credit_line(name, r):
    """画面の出典＝「誰が（識別子）・パブリックドメイン」。PD の根拠は ref/CREDITS.md の権利の欄に書く（画面は短く）"""
    ident = r.get('ident')
    return f"出典：{r['author']}（{ident}・パブリックドメイン）" if ident else f"出典：{r['author']}（パブリックドメイン）"


def cmd_credits(write=False):
    db = _db()
    cj = {f'ep18/{n}.jpg': credit_line(n, r) for n, r in db.items()}
    rows = [f"| `{n}` | {r.get('cut') or '（章ファイル）'} | {r['year'] or '不明'} | {GROUND} | {r['author']} | "
            f"{r['hold']}　{r.get('url', '')} |" for n, r in db.items()]
    for k, v in cj.items():
        print(k, '|', v)
    print(f'… 写真 {len(db)}点')
    if write:
        CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding='utf-8')
        md = CREDITS_MD.read_text(encoding='utf-8')
        # 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②）
        head = '## スレッシャー号のリメイク（1963-04-10・18本目）'
        hdr = '| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |'
        block = '\n'.join([
            head, '',
            '※2026-10-04（⑤b-7a）。`qa_out/ep18_assets.py credits --write` が書く（手で直さない）。旧版（3本目）の節は上の'
            '「USS Thresher (SSN-593)（1963-04-10・3本目）」＝旧版の誤り（Anefo の1点を「米海軍」・シーウルフの記録を「スカイラーク」）は'
            '直さない（公開ずみ・⑥で非公開にするだけ）。18本目は Anefo の1点（写っているのはノーチラス）とシーウルフの記録の頁を使わない。',
            '',
            '### 1. 写真（すべて米海軍の職務著作＝PD）',
            '- 出どころは3つ：NARA 289-T（RG 289・1963〜64年の捜索のアルバム・NARA の表示 Use: Unrestricted）／NARA 428-N（RG 428）・'
            '記録映画 85185 のコマ（RG 428・作り手は海軍写真センター）／Wikimedia Commons（隠しカテゴリ `PD US Navy`＋`CC-PD-Mark`）',
            '- 🔴 289-T の英字の説明札・428-N の台紙と札は**切り落とした**（`qa_out/ep18_assets.py` の crop＝OCR の文字の箱の外で切る）。'
            '頁全体を見せる `page24`（c911＝角の黒い塗り）だけ札が残る',
            '- 🔴 人が写る写真（§B2-2）：就役式（1961-08-03）の左の座った観客（私人）は**切り落とした**（x 385 より左）。甲板の乗員と'
            '式台の造船所の人（公的な任務）は残る（原寸で顔 約10px）。進水（1960）の岸の人は全員が後ろ姿か横向き',
            '- 撮影年が書かれていない・割れる点（289-T の造船所の写真2点と謝辞の頁の航走写真・スカイラークの2点）は撮影年を「不明」にし、'
            '**副題に年を書かない**（門番 credits）',
            '- 記録映画のコマは画素が縦長（SAR 10:11）＝655×480 に直した。動く映像（記録映画）は ⑤b-7b で `clips.json` に足す',
            '- Commons の新しい8点は、落とす前に一覧（名前・大きさ）でカズヤくんの了承を取った（2026-10-04）＝取ったファイルは'
            ' Commons の原本と SHA-1 が一致（`ref/ep18/img/fetched.json`＝git の外）',
            '', hdr, '|---|---|---|---|---|---|', *rows, ''])
        if head in md:
            pre, rest = md.split(head, 1)
            nxt = rest.find('\n## ')
            md = pre + block + (rest[nxt:] if nxt >= 0 else '')
        else:
            md = md.rstrip('\n') + '\n\n' + block
        CREDITS_MD.write_text(md, encoding='utf-8')
        print(f'→ {CREDITS_JSON} ／ {CREDITS_MD}')
    return 0


def _get(url, timeout=60):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def cmd_fetch(yes=False):
    """Commons の新しい点を原寸で取り、SHA-1 を Commons の値と照らす（🔴 了承のあとだけ `--yes`）。"""
    want = {r['title']: n for n, r in PICK.items() if r['src'] == 'commons'}
    q = urllib.parse.urlencode(dict(action='query', format='json', prop='imageinfo', iiprop='size|sha1|url',
                                    titles='|'.join('File:' + t for t in want)))
    info = json.loads(_get('https://commons.wikimedia.org/w/api.php?' + q))
    rows = []
    for p in info['query']['pages'].values():
        ii = p['imageinfo'][0]
        rows.append((p['title'][5:], ii['size'], ii['width'], ii['height'], ii['sha1'], ii['url']))
    for t, sz, w, h, _, _ in rows:
        print(f'{want[t]:20} {w}x{h} {sz / 1e6:.2f}MB  {t}')
    print(f'計 {sum(r[1] for r in rows) / 1e6:.2f}MB・{len(rows)}点')
    if not yes:
        print('（取っていない＝了承のあとに --yes）')
        return 0
    NEW.mkdir(parents=True, exist_ok=True)
    fx = json.loads((NEW / 'fetched.json').read_text(encoding='utf-8')) if (NEW / 'fetched.json').exists() else {}
    bad = 0
    for t, sz, w, h, sha1, url in rows:
        out = NEW / t
        for k in range(4):
            try:
                b = _get(url)
                break
            except Exception as e:  # noqa: BLE001
                print(f'  … {t}: {e}（{5 * (k + 1)}秒待って取り直す）')
                time.sleep(5 * (k + 1))
        else:
            print(f'🔴 {t}: 取れなかった')
            bad += 1
            continue
        got = hashlib.sha1(b).hexdigest()
        if got != sha1 or len(b) != sz:
            print(f'🔴 {t}: SHA-1・大きさが Commons の原本と違う（{len(b)} / {sz}）')
            bad += 1
            continue
        out.write_bytes(b)
        # 落としかけを測らない＝ディスクから2回 md5（記憶 feedback-download-size-is-not-completion）
        m1, m2 = _md5(out), _md5(out)
        fx[t] = dict(sha1=sha1, size=sz, w=w, h=h, url=url, md5=m1, fetched=time.strftime('%Y-%m-%d'))
        print(f"✓ {t}  SHA-1 一致・md5 {m1}{'' if m1 == m2 else '（2回目が違う🔴）'}")
        time.sleep(1.0)
    (NEW / 'fetched.json').write_text(json.dumps(fx, ensure_ascii=False, indent=1), encoding='utf-8')
    return 1 if bad else 0


def main():
    a = sys.argv[1:] or ['check']
    cmd = a[0]
    if cmd == 'build':
        return cmd_build(set(a[1:]) or None)
    if cmd == 'check':
        return cmd_check()
    if cmd == 'panel':
        return cmd_panel()
    if cmd == 'credits':
        return cmd_credits('--write' in a)
    if cmd == 'fetch':
        return cmd_fetch('--yes' in a)
    raise SystemExit(f'知らない命令: {cmd}')


if __name__ == '__main__':
    sys.exit(main())
