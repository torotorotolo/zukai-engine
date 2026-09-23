# -*- coding: utf-8 -*-
"""ep12_assets.py — 12本目（キャッスル・ブラボー）の**写真の束**と**報告書の頁**を作る（2026-09-23 ⑤b-2 新設）。

`qa_out/ep11_assets.py`（11本目）の形を写した。**素材はもう手元にある**（②で落とした）ので、
置き場へ取りに行く部分は無い。ここでやるのは「名前を付ける・縁を切る・権利を表にする」だけ。

■ 素材（②の台帳 `ref/ep12/materials.md` §7）
  NARA RG 678 の51点（`ref/ep12/img/nara/<naId>.jpg`・米連邦 §105・全点 Unrestricted）
  Commons の20点（`ref/ep12/img/<題名>`・米国の職務著作 PD ／ 日本の1954年の報道写真 PD-Japan-oldphoto）
  報告書3冊（`ref/ep12/src/*.pdf`。頁の番号は台本と同じ通し番号＝DNA p1〜・WT p1001〜・DASA p2001〜）

■ 🔴 絵は⑤b-2 で全点を見た（NARA＝`ref/ep12/nara_seen.tsv`・640px シート9枚／Commons＝②のシート4枚）
  落とした点は PICK に入れていない：
    NARA #17 クェゼリンで診察される島の子ども（私人の子どもの顔＋皮膚の傷）
    NARA #30 ロンゲリックのネズミ（＝第68図。頁 p241 で出すので写真は要らない）
    Commons 久保山さんの病床・増田三次郎さんの病室（私人の顔の近景）／装置の restoration1（002 と同じ写真）
    Commons Castle Romeo 001（別の実験）／AW 2〜6（どの装置か決められない＝台本 §1-4）
    Commons の F4U の除染（NARA #47 と同じ写真）

■ 🔴 縁と焼き込みの番号（後から載せた文字＝粗。§5b-5）
  ほぼ全点に**フィルムの黒い縁・焼き付けの白い余白**と、そこに**手書きの整理番号**（`22-2500`・`65%`・`Fig 28`・`CROP`）がある。
  → `box()` が端から内へ画素で測って切る（黒＝色の最大値の中央値が暗い行／白＝明るく平らな行）。
  さらに**絵の内側に焼き込まれた番号**（`ENI-455-54`・`D-205-5` ほか）は `cut=` で下端を追加で切る。
  ⚠️ `cut` の値は `strips` で切った下端の帯を並べて**目で確かめてから**決める（推定で置かない）。

    python qa_out/ep12_assets.py build     # ref/ep12/<名>.jpg ＋ assets.json
    python qa_out/ep12_assets.py pages     # ref/ep12/pg<頁>.png ＋ pages.json（200dpi）
    python qa_out/ep12_assets.py check     # PICK・assets.json・ファイルが揃っているか／縁が残っていないか
    python qa_out/ep12_assets.py sheet <出力>   # 切った枠を赤で描いた一覧（枠が絵に沿っているかを見る用）
    python qa_out/ep12_assets.py strips <出力>  # 番号を切った下端の帯を並べる（目で確かめる用）
    python qa_out/ep12_assets.py panel     # 縦横比の並び（`cuts/ss.py` の PANEL_AR を決める材料）
    python qa_out/ep12_assets.py credits [--write]   # credits.json と ref/CREDITS.md の表
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SRC = HERE / 'ref' / 'ep12' / 'img'
NARA = SRC / 'nara'
PDF = HERE / 'ref' / 'ep12' / 'src'
DEST = HERE / 'ref' / 'ep12'
DB = DEST / 'assets.json'
PAGES_JSON = DEST / 'pages.json'
CREDITS_JSON = DEST / 'credits.json'
CREDITS_MD = HERE / 'ref' / 'CREDITS.md'
MAXW = 3000
DPI = 200

NARA_LIC = 'Public domain (17 U.S.C. §105)'


def N(na_id, slot, **kw):
    return dict(src='nara', id=str(na_id), slot=slot, **kw)


def C(prefix, slot, **kw):
    # 🔴 Commons の点は**縁の測定をしない**（もともと縁が無い）。測らせると暗い雲・暗い背景・
    #    暗いスーツを縁と取り違えて**中身を2割まで切った**（⑤b-2 の枠の一覧で実測・6点）。
    kw.setdefault('frame', False)
    return dict(src='commons', id=prefix, slot=slot, **kw)


# 名前 → 素材。**欄（slot）は台本 §7 の欄**。`cut`＝下端を追加で切る割合（絵の内側の焼き込み番号）
PICK = {
    # ── fireball（ブラボーの火球）NARA 4・Commons 5 ─────────────────
    'fb_aerial_a': N(146763394, 'fireball', note='空撮・輪の雲を重ねたきのこ雲（#07）'),
    'fb_aerial_b': N(146763404, 'fireball', note='空撮・雲の上の火球（#01）'),
    'fb_estes_a': N(146763408, 'fireball', note='エステスから・海の上のきのこ雲（#04・明るい）'),
    'fb_estes_b': N(146763406, 'fireball', note='エステスから・雲の塊と水平線（#03・暗い）'),
    'fb_color_a': C('Castle Bravo Blast', 'fireball'),
    'fb_color_b': C('Castle Bravo nuclear test', 'fireball'),
    'fb_bw': C('Castle Bravo (black and white)', 'fireball'),
    'fb_close_a': C('Castle Bravo 005', 'fireball'),
    'fb_close_b': C('HD.10.290', 'fireball'),
    # ── other_shots（キャッスル作戦の別の爆発）─────────────────────
    'romeo_cloud': N(146763402, 'other_shots', note='ロメオ（#05）'),
    'union_cloud': N(146763398, 'other_shots', note='ユニオン（#09）'),
    'nectar_cloud': N(146763396, 'other_shots', note='ネクター（#11）'),
    'yankee_fb_1': N(146763410, 'other_shots', note='ヤンキー 1/3（#02）'),
    'yankee_fb_2': N(146763412, 'other_shots', note='ヤンキー 2/3（#06）'),
    'yankee_fb_3': N(146763414, 'other_shots', note='ヤンキー 3/3（#08）'),
    'yankee_cloud': N(146763400, 'other_shots', note='ヤンキーの雲（#10）'),
    'mine_recovery': N(146763464, 'other_shots', note='ユニオンのあとの機雷の回収（#20）', cut=0.07),
    # ── device（Commons だけ。装置の写真は4点＝全部別の写真）──────────
    'dev_shrimp': C('Castle Bravo Shrimp Device 002.jpg', 'device', note='射点の小屋の中の装置（白黒）'),
    'dev_shrimp_men': C('BravoSHRIMPShotCab', 'device', note='装置と作業の人たち（色）'),
    'dev_shotcab': C('BravoShotCab', 'device', note='射点の小屋の外観'),
    'dev_truck': C('Operation Castle AW 1', 'device', note='トラックに積まれた装置（元の説明）'),
    # ── base（パリー島・エニウェトク・エネマン）────────────────────
    'base_parry_aerial': N(146763422, 'base', note='パリー島の施設の空撮（#18）', cut=0.05),
    'base_airfield': N(146763494, 'base', note='エニウェトクの飛行場（#15）', cut=0.07),
    'base_metal': N(146763454, 'base', note='エニウェトクの金属の建物（#22）'),
    # ⚠️ 下の5点は box() の測りが「白い台紙の細い帯→黒い縁→絵」の並びで迷う＝**実測した枠を手で指定**
    #    （行ごとの明るさの中央値を端から並べて、暗い帯の終わりを読んだ。⑤b-2）
    'base_tents': N(146763452, 'base', note='パリー島の天幕（#13）',
                    box=(0.0723, 0.0673, 0.949, 0.9251)),
    'base_dock': N(146763420, 'base', note='パリー島の桟橋（#50）', cut=0.05),
    'base_eneman': N(146763428, 'base', note='エネマン島のキャンプ（#39）'),
    # ── rongelap（ロンゲラップ・ロンゲリック）────────────────────
    'rongelap_landing': N(146763432, 'rongelap', note='調査の一行が浜に上がる（#49・原寸で私人なし）'),
    # ⚠️ ⑤b-3 で頁を見て直した：#29 は第67図と**別の写真**（小屋のそばで靴に覆いを付けた1人）。
    #    第67図（p240）は **#49＝c108 と同じ場面の別のコマ**（ボート DDE449・3月9日）＝c903 に第67図を出さない
    'rongelap_booties': N(146763434, 'rongelap', note='靴の覆い（#29・第67図とは別の写真）'),
    'rongerik_station': N(146763424, 'rongelap', note='ロンゲリックの気象観測所（#40）'),
    # ── damage ─────────────────────────────────────────
    'dmg_eneman': N(146763468, 'damage', note='エネマン島の建物の被害（#43）',
                    box=(0.106, 0.069, 0.9453, 0.9215)),
    'dmg_mine': N(146763466, 'damage', note='Project 3.4 機雷の被害（#16）', cut=0.07),
    # ── suits（防護服）─────────────────────────────────────
    'suits_three': N(146763470, 'suits', note='防護服3種（#27）'),
    'suits_scrub': N(146763472, 'suits', note='脱ぐ前にこすって洗う（#42）', cut=0.07),
    # ⚠️ 暗い写真が黒い台紙の中にある＋絵の内側に手書き 22-2225＝枠は**手で指定**（box() は中の暗さで迷う）
    'suits_adrikan': N(146763450, 'suits', note='アドリカン島で器材を回収（#45）',
                       box=(0.2252, 0.0628, 0.735, 0.72)),
    # ── decon（除染）13 ────────────────────────────────────
    'dc_f84g': N(146763492, 'decon', note='F-84G（#12）', cut=0.07),
    # 上端の暗さは縁ではなく艦内の中身。手書き 22-1287 は上 4.6% まで＝そこだけ落とす
    'dc_curtis': N(146763430, 'decon', note='USS Curtis 服を脱いだあとの測定（#14）',
                   box=(0.1038, 0.05, 0.9006, 0.97)),
    'dc_yag40_deck': N(146763438, 'decon', note='YAG-40 の甲板を洗う（#23）'),
    'dc_b36_tail': N(146763486, 'decon', note='B-36 の尾翼を洗う（#24）', cut=0.07),
    'dc_ship_scrub': N(146763474, 'decon', note='艦の除染 高圧の海水とブラシ（#26）', cut=0.07),
    'dc_parry_equip': N(146763440, 'decon', note='パリー島の除染器材（#28）',
                        box=(0.0886, 0.061, 0.852, 0.869)),
    'dc_b36_under': N(146763490, 'decon', note='B-36 の下で洗う（#32）', cut=0.07),
    'dc_b36_wing': N(146763488, 'decon', note='B-36 の主翼を洗う（#33）'),
    'dc_tent': N(146763446, 'decon', note='汚れた服を着替える天幕（#37）'),
    'dc_yag40_spray': N(146763436, 'decon', note='YAG-40 の放水（#38）'),
    'dc_molala': N(146763456, 'decon', note='USS Molala が YAG-40 を洗う（#44）'),
    'dc_f4u_test': N(146763444, 'decon', note='F4U を測る（#47）'),
    'dc_f4u_wash': N(146763442, 'decon', note='F4U を洗う（#48）'),
    # ── fallout（灰を集める）10 ────────────────────────────────
    'fo_roll_prep': N(146763478, 'fallout', note='濾紙を巻く準備（#19）', cut=0.07),
    'fo_cave': N(146763460, 'fallout', note='濾紙を遮へいの箱へ（#21）', cut=0.07),
    'fo_f84g': N(146763476, 'fallout', note='F-84G 採取機の駐機・真上から（#25）', cut=0.12),
    'fo_tank': N(146763416, 'fallout', note='翼端の筒から濾紙を出す（#31）'),
    'fo_pig_lift': N(146763484, 'fallout', note='ピッグを持ち上げる（#34）', cut=0.07),
    'fo_pig_place': N(146763482, 'fallout', note='濾紙をピッグへ（#35）', cut=0.07),
    'fo_wire': N(146763458, 'fallout', note='採取器の針金を切る（#36）', cut=0.07),
    'fo_rolled': N(146763480, 'fallout', note='濾紙を巻く（#41）', cut=0.07),
    'fo_tray': N(146763448, 'fallout', note='灰を受けるトレイ（#46）'),
    'fo_buoy': N(146763418, 'fallout', note='浮かべる採集ブイ（#51）', cut=0.05),
    # ── japan・official・doc（Commons）──────────────────────────
    'jp_tuna_check': C('Technical experts checking contamination', 'japan',
                       note='魚市場でマグロを調べる技術者（公的な任務）'),
    # 🔴 店の女性2人（私人）の顔が右 0.65〜0.89 に写る＝看板の側だけを切り出す（§B2-2）
    'jp_fish_sign': C('A signboard appealing shoppers', 'japan', note='魚屋の看板（女性の顔は切り落とす）',
                      trim=(0.0, 0.0, 0.60, 1.0)),
    'eisenhower_strauss': C('Eisenhower and Strauss', 'official'),
    # ── mike（1952年のマイク＝第2章 c205・c206）⑤b-3 でカズヤくん許可のうえ追加 ─────
    #    🔴 **年は1952**（この束の既定の1954ではない）＝`year=` を持たせ、出典の行と表もそれを読む
    'mike_cloud': C('IvyMike2 HR', 'mike', year=1952, note='マイクのきのこ雲（1952年11月1日・NARA 由来）'),
    'mike_device': C('Ivy Mike Sausage device', 'mike', year=1952, note='マイクの装置（ソーセージ）と人'),
    'doc_aec_letter': C('AEC Authorization for Operation Castle', 'doc', frame=False),
    # 🔴 海図は米海軍水路部 H.O. 6032「3rd Ed., Dec. 1954 ; Revised 6/30/58」＋1958年7月の訂正印＝**この写しは1958年**
    #    （⑤b-3 で余白を原寸で読んだ）。既定の1954と書くと、画面の出典が嘘の年を名乗る
    'doc_bikini_chart': C('Bikini Atoll - NARA', 'doc', frame=False, year=1958,
                          note='ビキニ環礁の海図（米海軍水路部 H.O. 6032・1954年第3版の1958年改訂）'),
}
# 画面の出典の「誰が」を名乗り直す点（`credit_line` の既定＝撮影者の欄から推すのでは足りないもの）
WHO = {'doc_bikini_chart': '米海軍水路部'}

# 報告書の頁（台本 §4 の画の欄に出てくる頁＋報告書をなぞる型の頁）。名前は `pg<頁>`
PAGES_PICK = (1, 30, 114, 118, 211, 212, 213, 214, 215, 216, 218, 219, 221, 223, 226, 229,
              230, 232, 238, 240, 241, 243, 1015, 1082, 2069, 2074,
              # ⑤b-3：報告書の実物をなぞる型（trace）の頁＝c207 p31・c414 p209・c515 p217
              31, 209, 217,
              # ⑤b-4：c711 のなぞる型（DNA p227「…Hq JTF 7 did not know where the cloud was, nor where it had been.」）
              227)
DOCS = ((2001, 'dasa1251_v2.pdf', 'DASA 1251'), (1001, 'project41_wt923.pdf', 'WT-923'),
        (1, 'dna6035f.pdf', 'DNA 6035F'))


# ══════════════════════════════════════════════════════════
def _src_path(r):
    if r['src'] == 'nara':
        return NARA / f"{r['id']}.jpg"
    hits = [p for p in SRC.iterdir() if p.is_file() and p.name.startswith(r['id'])]
    if len(hits) != 1:
        raise SystemExit(f"🔴 Commons の {r['id']!r} が {len(hits)} 件に当たる（1件でなければ止める）")
    return hits[0]


def box(im):
    """フィルムの黒い縁・焼き付けの白い余白を、端から内へ画素で測って切る矩形（0〜1）。

    行（列）を「縁」とみなす条件：
      黒＝その行の**色の最大値**の中央値が 60 未満（赤い火球の写真は R が高いので縁にならない）
      白＝中央値 228 以上・25 パーセンタイル 190 以上・ばらつき 14 未満（明るく平らな余白。空は雲や粒でばらつく）
    3行続けて縁でない行が来たら、そこを絵の端とする。最後に 0.6% 内へ寄せる（縁のにじみ）。
    """
    import numpy as np
    s = 800 / max(im.size)
    sm = im.convert('RGB').resize((max(1, int(im.width * s)), max(1, int(im.height * s))))
    a = np.asarray(sm).astype(np.int16)
    v = a.max(axis=2)
    g = a.mean(axis=2)

    def border(lv, lg):
        if np.median(lv) < 60:
            return True
        return (np.median(lg) >= 228 and np.percentile(lg, 25) >= 190 and lg.std() < 14)

    def walk(n, get):
        run = 0
        for i in range(n // 2):
            lv, lg = get(i)
            if border(lv, lg):
                run = 0
                continue
            run += 1
            if run == 3:
                return i - 2
        return 0

    h, w = v.shape
    top = walk(h, lambda i: (v[i], g[i]))
    bot = walk(h, lambda i: (v[h - 1 - i], g[h - 1 - i]))
    lef = walk(w, lambda i: (v[:, i], g[:, i]))
    rig = walk(w, lambda i: (v[:, w - 1 - i], g[:, w - 1 - i]))

    # 2段目：止まった所の**切り口の行**がまだ暗ければ内へ進む（縁の内側のにじみ＝暗い灰色）。
    #   ⚠️ 1段目だけだと 天幕・USS Curtis・エネマン島・パリー島の器材で1%ほど黒が残った（check で実測）。
    #   ⚠️ 進むのは**切り口の行そのもの**が暗いときだけ・最大4%（暗い写真の中身まで食わない）。
    #   🔴 白い台紙の細い線も同じ（右端に約1%残る点が5つあった＝strips で実測）。白は最大1.5%まで。
    def creep(pos, n, line):
        lim, wlim = pos + int(n * 0.04), pos + int(n * 0.015)
        while pos < lim:
            ln = line(pos)
            if np.median(ln) < 50 or (pos < wlim and np.median(ln) > 236 and np.percentile(ln, 25) > 200):
                pos += 1
                continue
            break
        return pos
    top = creep(top, h, lambda i: v[i, lef:w - rig])
    bot = creep(bot, h, lambda i: v[h - 1 - i, lef:w - rig])
    lef = creep(lef, w, lambda i: v[top:h - bot, i])
    rig = creep(rig, w, lambda i: v[top:h - bot, w - 1 - i])
    pad = 0.006
    return (round(lef / w + pad, 4), round(top / h + pad, 4),
            round(1 - rig / w - pad, 4), round(1 - bot / h - pad, 4))


def _md5(p):
    return hashlib.md5(p.read_bytes()).hexdigest()


def _nara_meta():
    rows = csv.DictReader(open(NARA / 'index.tsv', encoding='utf-8'), delimiter='\t')
    return {r['naId']: r for r in rows}


def _commons_meta():
    import re
    L = json.loads((DEST / 'commons_ep12.json').read_text(encoding='utf-8'))
    H = json.loads((DEST / 'commons_hidden.json').read_text(encoding='utf-8'))

    def strip(s):
        return re.sub(r'<[^>]+>', '', s or '').strip()
    # ⑤b-3（2026-09-23）：②の検索の外から足した点（マイクの2点）は `commons_extra.json`。
    #    隠しカテゴリ（PD の根拠）も同じ行に持つ（②の束は `commons_hidden.json`）
    X = DEST / 'commons_extra.json'
    E = json.loads(X.read_text(encoding='utf-8')) if X.exists() else []
    out = {}
    for x in L + E:
        t = x['title'][5:]
        out[t] = dict(lic=x.get('license_short') or '', author=strip(x.get('artist')),
                      date=strip(x.get('date_original')), cats=H.get(x['title'], x.get('hidden', [])),
                      title=t)
    return out


def cmd_build(only=None):
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    nm, cm = _nara_meta(), _commons_meta()
    db = json.loads(DB.read_text(encoding='utf-8')) if DB.exists() else {}
    for name, r in PICK.items():
        if only and name not in only:
            continue
        sp = _src_path(r)
        with Image.open(sp) as im0:
            # ⚠️ 海図は 12624x9024（RGB で 342MB）。コミットの空きが足りないので JPEG の縮小読みで開く
            if im0.format == 'JPEG' and im0.width > 2 * MAXW:
                im0.draft('RGB', (im0.width // 4, im0.height // 4))
            im = im0.convert('RGB')
        b = (r['box'] if r.get('box')
             else box(im) if r.get('frame', True) else (0.0, 0.0, 1.0, 1.0))
        x0, y0, x1, y1 = b
        if r.get('cut'):
            y1 = round(y1 - (y1 - y0) * r['cut'], 4)
        if r.get('trim'):                         # 素材の中での追加の切り出し（顔を外すなど）
            tx0, ty0, tx1, ty1 = r['trim']
            x0, x1 = x0 + (x1 - x0) * tx0, x0 + (x1 - x0) * tx1
            y0, y1 = y0 + (y1 - y0) * ty0, y0 + (y1 - y0) * ty1
        W0, H0 = im.size
        crop = im.crop((int(W0 * x0), int(H0 * y0), int(W0 * x1), int(H0 * y1)))
        if crop.width > MAXW:
            crop = crop.resize((MAXW, round(crop.height * MAXW / crop.width)), Image.LANCZOS)
        out = DEST / f'{name}.jpg'
        crop.save(out, quality=92)
        if r['src'] == 'nara':
            m = nm[r['id']]
            meta = dict(lic=NARA_LIC, author='米国立公文書館', year=1954,
                        title=m['scope'], hold=f"NARA {r['id']}（RG 678）")
        else:
            m = cm[sp.name]
            jp = any('Japan' in c for c in m['cats'])
            meta = dict(lic=('Public domain（日本・1957年より前に公表の写真）' if jp
                             else 'Public domain（米国の職務著作）'),
                        author=m['author'], year=r.get('year', 1954), title=m['title'],
                        hold=f"Wikimedia Commons「{m['title']}」")
        db[name] = dict(src=r['src'], id=r['id'], slot=r['slot'], note=r.get('note', ''),
                        box=[round(x0, 4), round(y0, 4), round(x1, 4), round(y1, 4)],
                        w=crop.width, h=crop.height, md5=_md5(out), **meta)
        print(f'✓ {name:20} {crop.width}x{crop.height}  枠 {db[name]["box"]}')
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'→ {DB}（{len(db)}点）')
    return 0


def cmd_pages():
    import fitz
    pj = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    for pr in PAGES_PICK:
        base, fn, doc = next(d for d in DOCS if pr >= d[0])
        pno = pr - base + 1 if base > 1 else pr          # DNA は +0・WT は +1000・DASA は +2000
        with fitz.open(PDF / fn) as d:
            pg = d[pno - 1]
            pix = pg.get_pixmap(dpi=DPI, colorspace=fitz.csGRAY)
            out = DEST / f'pg{pr}.png'
            pix.save(out)
        old = pj.get(f'pg{pr}', {})
        pj[f'pg{pr}'] = dict(old, doc=doc, pdf=fn, pdf_page=pno, w=pix.width, h=pix.height, md5=_md5(out))
        print(f'✓ pg{pr}  {doc} の PDF {pno}頁  {pix.width}x{pix.height}')
    PAGES_JSON.write_text(json.dumps(pj, ensure_ascii=False, indent=1), encoding='utf-8')
    return 0


def cmd_check():
    import numpy as np
    from PIL import Image
    if not DB.exists():
        raise SystemExit('🔴 assets.json が無い（build を先に）')
    db = json.loads(DB.read_text(encoding='utf-8'))
    bad = 0
    for name in PICK:
        p = DEST / f'{name}.jpg'
        if name not in db or not p.exists():
            print(f'🔴 {name}: 束に無い'); bad += 1; continue
        if _md5(p) != db[name]['md5']:
            print(f'🔴 {name}: md5 が assets.json と違う（手で差し替えた？）'); bad += 1
        a = np.asarray(Image.open(p).convert('RGB').resize((400, 300))).astype(np.int16)
        v = a.max(axis=2)
        for side, band in (('上', v[:4]), ('下', v[-4:]), ('左', v[:, :4]), ('右', v[:, -4:])):
            if np.median(band) < 45:
                print(f'⚠️ {name}: {side}の端が黒い（縁が残っている疑い・中央値 {np.median(band):.0f}）')
            # 台紙＝**粒の無い真っ平らな白**。空・砂浜・船体は明るくても粒がある
            #   ⚠️ 「明るい」だけで鳴らすと 40件鳴った（空と砂浜）＝鳴りすぎる門番は本物を埋もれさせる
            if PICK[name].get('frame', True) and np.median(band) > 247 and band.std() < 5:
                print(f'⚠️ {name}: {side}の端が白い（台紙が残っている疑い）')
    extra = sorted(n for n in set(db) - set(PICK) if db[n].get('src') != 'clip')
    for e in extra:
        print(f'⚠️ assets.json に PICK に無い名前: {e}')
    print('✓ 揃っている' if not bad else f'🔴 {bad}件')
    return 1 if bad else 0


def cmd_sheet(out):
    """切った枠を赤で描いた一覧（4列×4行・1コマ 320x240）。**枠が絵に沿っているか**を見る用。"""
    from PIL import Image, ImageDraw
    Image.MAX_IMAGE_PIXELS = None
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    db = json.loads(DB.read_text(encoding='utf-8'))
    names = list(PICK)
    CW, CH, COLS, ROWS = 320, 240, 4, 4
    per = COLS * ROWS
    for i in range(0, len(names), per):
        sh = Image.new('RGB', (CW * COLS, (CH + 18) * ROWS), (40, 40, 44))
        d = ImageDraw.Draw(sh)
        for k, name in enumerate(names[i:i + per]):
            with Image.open(_src_path(PICK[name])) as im0:
                im = im0.convert('RGB')
            im.thumbnail((CW - 6, CH - 6))
            x, y = (k % COLS) * CW + (CW - im.width) // 2, (k // COLS) * (CH + 18) + (CH - im.height) // 2
            sh.paste(im, (x, y))
            x0, y0, x1, y1 = db[name]['box']
            d.rectangle((x + x0 * im.width, y + y0 * im.height, x + x1 * im.width, y + y1 * im.height),
                        outline=(255, 40, 40), width=2)
            d.text(((k % COLS) * CW + 4, (k // COLS) * (CH + 18) + CH + 3), name, fill=(240, 240, 240))
        p = out / f'box_{i // per + 1:02}.jpg'
        sh.save(p, quality=88)
        print(f'✓ {p.name}')
    return 0


def cmd_strips(out):
    """焼き込み番号を `cut` で切った点の**下端の帯**を並べる（切ったあとの絵の下 12%）。"""
    from PIL import Image, ImageDraw
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    names = [n for n, r in PICK.items() if r.get('cut')]
    rows = []
    for n in names:
        im = Image.open(DEST / f'{n}.jpg').convert('RGB')
        band = im.crop((0, int(im.height * 0.88), im.width, im.height))
        band = band.resize((1240, max(1, int(band.height * 1240 / band.width))))
        rows.append((n, band))
    H = sum(b.height + 22 for _, b in rows)
    sh = Image.new('RGB', (1260, H), (40, 40, 44))
    d = ImageDraw.Draw(sh)
    y = 0
    for n, b in rows:
        d.text((8, y + 4), f'{n}  cut={PICK[n]["cut"]}', fill=(255, 220, 90))
        sh.paste(b, (10, y + 20))
        y += b.height + 22
    p = out / 'strips.jpg'
    sh.save(p, quality=88)
    print(f'✓ {p}  {len(rows)}点')
    return 0


def cmd_panel():
    db = json.loads(DB.read_text(encoding='utf-8'))
    for n, r in sorted(db.items(), key=lambda kv: kv[1]['w'] / kv[1]['h']):
        ar = r['w'] / r['h']
        loss = 1 - (ar / (16 / 9) if ar < 16 / 9 else (16 / 9) / ar)
        print(f"AR {ar:.3f}  {n:20} {r['w']}x{r['h']}  全画面で {loss:.1%} 切れる")
    return 0


def credit_line(name, r):
    if r['src'] == 'clip':                        # 映像から抜いた静止画（`ref/ep12/make_clips.py` が登録）
        c = json.loads((DEST / 'clips.json').read_text(encoding='utf-8'))[r['clip']]['credit']
        return c + ('（静止画）' if name.startswith('fb_') else '')
    if r['src'] == 'nara':
        return f"出典：米国立公文書館（NARA {r['id']}）（1954年）"
    a = r['author']
    if name in WHO:
        return f"出典：{WHO[name]}（{r.get('year', 1954)}年）"
    if 'Asahi' in a:
        who = '朝日グラフ'
    elif 'Yomiuri' in a:
        who = '読売新聞'
    elif 'Energy' in a or 'ENERGY' in a or a == 'USDE':
        who = '米エネルギー省'
    elif 'NARA' in a:
        who = '米国立公文書館'
    elif 'Atomic Energy' in a:
        who = '米原子力委員会'
    elif 'Defense' in a:
        who = '米国防総省'
    else:
        who = '米国政府'
    return f"出典：{who}（{r.get('year', 1954)}年）"


def cmd_credits(write=False):
    db = json.loads(DB.read_text(encoding='utf-8'))
    cj = {f'ep12/{n}.jpg': credit_line(n, r) for n, r in db.items()}
    rows = [f"| `{n}` | （章ファイル） | {r.get('year', 1954)} | {r['lic']} | {r['author']} | {r['hold']} |"
            for n, r in db.items()]
    # 🔴 報告書の頁も表に載せる（`check_credits` は ep12/ の絵を全部この表で引く＝載せないと fail closed）。
    #    年は**頁の文書の年**（表紙・DTIC の記録で確かめた値＝scene_jiko.EP12_DOC と同じ）
    pages = json.loads(PAGES_JSON.read_text(encoding='utf-8')) if PAGES_JSON.exists() else {}
    who = {'DNA 6035F': (1982, '国防原子力局'), 'WT-923': (1954, '医師団（Project 4.1）'),
           'DASA 1251': (1979, '国防原子力局（GE-TEMPO の抜粋版）')}
    rows += [f"| `{k}` | （章ファイル） | {who[p['doc']][0]} | Public domain（米国の職務著作） | "
             f"{who[p['doc']][1]} | {p['doc']} PDF {p['pdf_page']}頁 |" for k, p in pages.items()]
    for k, v in list(cj.items())[:4]:
        print(k, '|', v)
    print(f'… {len(cj)}点')
    if write:
        CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding='utf-8')
        md = CREDITS_MD.read_text(encoding='utf-8')
        head = '## キャッスル・ブラボー水爆実験（1954-03-01・12本目）　※2026-09-23（⑤b-2）'
        hdr = '| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 所蔵と識別子 |'
        block = '\n'.join([head, '', '### 1. 写真（NARA RG 678 ＝ 米連邦 §105 ／ Commons ＝ 米国の職務著作 PD・日本の1954年の報道写真 PD）',
                           '`qa_out/ep12_assets.py credits --write` が書く（手で直さない）。', '',
                           hdr, '|---|---|---|---|---|---|', *rows, ''])
        if head in md:
            pre, rest = md.split(head, 1)
            nxt = rest.find('\n## ')
            md = pre + block + (rest[nxt:] if nxt >= 0 else '')
        else:
            md = md.rstrip('\n') + '\n\n' + block
        CREDITS_MD.write_text(md, encoding='utf-8')
        print(f'→ {CREDITS_JSON} ／ {CREDITS_MD}')
    return 0


def main():
    a = sys.argv[1:] or ['check']
    cmd = a[0]
    if cmd == 'build':
        return cmd_build(set(a[1:]) or None)
    if cmd == 'pages':
        return cmd_pages()
    if cmd == 'check':
        return cmd_check()
    if cmd == 'sheet':
        return cmd_sheet(a[1])
    if cmd == 'strips':
        return cmd_strips(a[1])
    if cmd == 'panel':
        return cmd_panel()
    if cmd == 'credits':
        return cmd_credits('--write' in a)
    raise SystemExit(f'知らない命令: {cmd}')


if __name__ == '__main__':
    sys.exit(main())
