# -*- coding: utf-8 -*-
"""本番1本目「潜水艇タイタン号」226カット・34分06秒のレイヤー書き出し。

■ 何がどこにあるか
  台本の文言   … `tools/narration.py` の SCRIPT（**正本はあちら**。ここには写さない）
  カットの尺   … `audio/narration.json`（合成後の実測秒）
  カットの「画」… `tools/cuts/*.py`（章ごと。この場所だけを直せば図が変わる）
  図の部品     … `tools/titan_fig.py`（型。226カットをこの部品で組む）

■ レイヤーの命名（build_jiko がこの名前で拾う）
  {cid}_base … 地＋見出し＋章マーカー。カット頭から出ている（動かない）
  {cid}_lab  … 図の骨格。**カット前半で左→右に描かれる**
  {cid}_aN   … 図の N 段目。**その段の持ち時間いっぱいをかけて左→右に描かれる**
  {cid}_hot  … 脈打つ強調（省略可）
  実写カットは {cid}_bg（地・写真に覆われる）と {cid}_lab（写真の上）＋{cid}_aN

■ 🔴 3秒以上の静止を禁止（映像ルール4）を**構造で満たす**
  段の持ち時間 ＝ その段が出てから次の段が出るまで（最後の段はカット終わりまで）。
  段はその持ち時間いっぱいをかけて描かれるので、**カットの頭から終わりまで常に何かが動く**。
  テスト映像のようにカットごとに MOTION を手で書く必要が無くなった
  （手書きだと図を動かすたびに直し忘れる。実際 c3 のワイプ範囲で1度やっている）。

■ 🔴 写真より上に出すものは `_lab` に置く
  build_jiko は bg の上に写真を貼るので、`_bg` に置いた文字は全画面写真に丸ごと覆われる
  （21巡目に見出しが完全に消えた）。
"""
import base64
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J
import titan_fig as F
import fontmetrics as fm
import render

W, H = 1920, 1080
HERE = Path(__file__).parent.parent
FONTS = Path(os.environ.get("ZUKAI_FONTS", HERE / "fonts"))
OUT = HERE / "out" / "jiko"
CSS = ""

# ── 章（章マーカーに出す名前） ────────────────────────────
CHAPTERS = {
    "c1": (1, "その日、10時47分"),
    "c2": (2, "炭素繊維という選択"),
    "c3": (3, "一度目の船体"),
    "c4": (4, "二度目の船体"),
    "c5": (5, "大きな音"),
    "c6": (6, "11か月の空白"),
}
NCH = 6


def chapter_of(cid):
    """プロローグ（pr*）とエピローグ（ep*）は章マーカー無し。"""
    return CHAPTERS.get(cid[:2])


# ── 出典表記（ref/CREDITS.md の台帳と1対1） ───────────────
CR_NTSB = "出典：NTSB（米国運輸安全委員会）／パブリックドメイン"
CR_USCG_ROV = "出典：アメリカ沿岸警備隊／ROV撮影／パブリックドメイン"
CR_USCG_L = "出典：アメリカ沿岸警備隊／撮影 M. Leake／パブリックドメイン"
CR_NOAA = "出典：NOAA／海洋探査研究所／ロードアイランド大学／パブリックドメイン"

PHOTO_CREDIT = {
    "titan_hull_edge.jpg": CR_NTSB,
    "titan_hull_pair.jpg": CR_NTSB,
    "titan_ntsb14_endface.jpg": CR_NTSB,
    "titan_ntsb15_endpiece.jpg": CR_NTSB,
    "titan_ntsb16_wrinkle.jpg": CR_NTSB,
    "titan_ntsb16_grind.jpg": CR_NTSB,
    "titan_ntsb17_layers.jpg": CR_NTSB,
    "titan_ntsb17_voids.jpg": CR_NTSB,
    "titan_hull_inner.jpg": CR_NTSB,
    "titan_delam_ruler.jpg": CR_NTSB,
    "titan_rov_aft.jpg": CR_USCG_ROV,
    "titan_rov_tailcone.jpg": CR_USCG_ROV,
    "titan_cf_evidence.jpg": CR_USCG_L,
    "titan_titanic_bow.jpg": CR_NOAA,
    # ── 2026-08-02 追加。**PD限定をやめた**ので報告書の図を戻した ─────────
    #    方針変更は 2026-08-01（[[引き継ぎ-事故検証-タイタン号-r13試写指摘-20260801]] §5）。
    #    ⚠️ ところが**解禁したまま、捨てた素材を戻していなかった**ので、
    #      実写の比率は 12.0% → 12.7% までしか動いていなかった。
    #    ⚠️ うち図18は**出所の記載が無い＝NTSB作成＝PD**で、従来の縛りでも
    #      使えたはずの取りこぼし（図13〜18をPDと判定したとき18だけ拾い忘れた）。
    "titan_f18_delam.png": CR_NTSB,
    "titan_f01_descend.jpg": "出典：NTSB 報告書 図1（撮影：オーシャンゲート）",
    "titan_f04_lars.png": "出典：NTSB 報告書 図4（撮影：G. Comber）",
    "titan_f08_launch.png": "出典：NTSB 報告書 図8（撮影：G. Comber）",
    "titan_f09_parking.png": "出典：NTSB 報告書 図9（撮影：A. Harvey）",
    "titan_f10_mishap.png": "出典：NTSB 報告書 図10（撮影：S. Taragel）",
    "titan_f11_wreck.png":
        "出典：NTSB 報告書 図11（ROV撮影：Pelagic Research Services）",
    "titan_f12_wreck.png":
        "出典：NTSB 報告書 図12（ROV撮影：Pelagic Research Services）",
}
# 2026-07-31：titan_hull_pair.jpg は **NTSB 図13**（外面と内面の2枚組）と確認できたので
# 解禁した。報告書の画素サイズ（1609×1490）と完全一致し、図13〜18は出所表記が無い
# ＝NTSB自身の研究室撮影＝PD。使えない写真はいまは無い。
BANNED_PHOTOS = set()


def credit_of(cid, spec):
    """そのカットに出す出典。**動画を当てたカットは動画の出典を出す。**

    🔴 2026-08-01：動画を差し込むとき、静止画の出典（NTSB／PD）をそのまま
       出してしまうと**出所を偽ることになる**。ROV映像は沿岸警備隊の公開資料だが
       撮影は Pelagic Research Services で、パブリックドメインではない。
       検証番組で出所を偽ると、内容そのものの信用が落ちる。
    """
    try:
        import footage as FO
        c = FO.credit_of(cid)
        if c and FO.have(cid):
            return c
    except Exception:                                    # noqa: BLE001
        pass
    return PHOTO_CREDIT[spec["photo"]]


def face_css(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


def page(inner, w=W, h=H):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}">{inner}</svg>')
    return (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{CSS}'
            f'body{{width:{w}px;height:{h}px;overflow:hidden}}</style></head>'
            f'<body>{svg}</body></html>')


# ── 字幕 ─────────────────────────────────────────────────
# 黒帯の上・38px・NotoSansJP-Bold・全カット統一（映像ルール1）。帯は y=900〜1080。
SUB_Y, SUB_H = 900, 180
SUB_SIZE = 38
SUB_MAXW = 1560          # 字幕1行に許す最大の幅（px）。**実測で折る**
XML = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def esc(t):
    return "".join(XML.get(c, c) for c in t)


def wrap2(text):
    """字幕は**2行まで**。折る位置は読点。無ければ幅の中央に近い文字境界。

    🔴 「26字」で折っていたのを**実測幅（px）**に変えた。
       字幕は漢字・かな・数字が混ざるので、字数で折ると1行の長さが 1.6 倍ぶれる
       （「2023年6月18日、午前10時47分。」は16字だが数字が多く、
         「潜水艇は、原型をとどめていなかった。」の18字より狭い）。
    """
    if fm.width(text, SUB_SIZE, "Noto") <= SUB_MAXW:
        return [text]
    half = fm.width(text, SUB_SIZE, "Noto") / 2
    best, acc = None, 0.0
    cands = []
    for i, ch in enumerate(text):
        acc += fm.adv(ch, "Noto") * SUB_SIZE
        if ch in "、。":
            cands.append((abs(acc - half), i + 1))
        if best is None or abs(acc - half) < best[0]:
            best = (abs(acc - half), i + 1)
    cut = min(cands)[1] if cands else best[1]
    return [text[:cut], text[cut:]]


def sub_band(w=W, h=SUB_H):
    """★字幕の黒帯だけ。**文字とは別の1枚**にして、常時貼りっぱなしにする。

    🔴 2026-07-31（試写の指摘③）：それまで帯と文字を1枚のPNGに焼いていたので、
       字幕が変わるたびに**帯までいっしょにフェードして画面がちらついた**。
       帯を分けて常時表示にすれば、消えるのは文字だけになる。
    ⚠️ 帯は**全カット共通**なので焼くのは1枚（`_subband`）。226枚焼かない。
    ⚠️ 図の本体は y=210〜892（jiko_style の BAND_T / BAND_B）に収まっていて、
       帯は y=900 から下。**常時出しても図に一切かからない**（確認済み）。
    """
    return (f'<linearGradient id="subbg" x1="0" y1="1" x2="0" y2="0">'
            f'<stop offset="0" stop-color="#000" stop-opacity="0.78"/>'
            f'<stop offset="0.62" stop-color="#000" stop-opacity="0.70"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#subbg)"/>')


def sub_row(text, w=W, h=SUB_H):
    """字幕1枚ぶんの**文字だけ**。1行なら下寄せ、2行なら上下に振り分ける。

    ⚠️ 帯はここに含めない（`sub_band()` が別に持つ）。太いフチは残す
       ── 帯があっても、明るい写真の上では文字がフチで持っている。
    """
    lines = wrap2(text)
    ys = [h * 0.64] if len(lines) == 1 else [h * 0.42, h * 0.78]
    g = []
    for t, y in zip(lines, ys):
        g.append(f'<text x="{w / 2:.0f}" y="{y:.0f}" font-family="Noto" '
                 f'font-size="{SUB_SIZE}" fill="{J.INK_W}" text-anchor="middle" '
                 f'stroke="#000" stroke-width="7" stroke-linejoin="round" '
                 f'paint-order="stroke fill">{esc(t)}</text>')
    return "".join(g)


def sub_strip(lines):
    return "".join(f'<g transform="translate(0,{i * SUB_H})">{sub_row(t)}</g>'
                   for i, t in enumerate(lines))


# ── 実写カットの型：全画面 ────────────────────────────────
PHOTO_FULL = (0, 0, W, H)
SCRIM_TOP = 300
CRED_Y = 872
CRED_BACK_Y = 196       # 写真を地に敷くカットの出典（右上・本体枠の上）
BAND_CY = 560           # 帯写真の縦中心


def photo_box(spec):
    """写真の置き場所。全画面か、**帯**か。

    🔴 NTSB の標本写真は 1431×325 のように細長いものが多い。
       全画面（1920×1080）に覆わせると **3.3倍に引き伸ばして左右を切り落とす**ことになり、
       ぼやけたうえに写真の意味（層が並んでいる様子）が消える。
       帯なら原寸に近い倍率で、横方向の情報を全部見せられる。
    """
    if not spec.get("band"):
        return PHOTO_FULL
    from PIL import Image
    with Image.open(HERE / "ref" / spec["photo"]) as im:
        sw, sh = im.size
    h = min(int(W * sh / sw), 720)
    return (0, int(BAND_CY - h / 2), W, h)


def full_bg():
    """全画面写真カットの地。**ここには何も置けない**（写真が全面で乗る）。"""
    return J.frame(W, H)


def full_top(cid, spec):
    """写真の上に載せる一式（暗幕・見出し・章マーカー・出典）。`_lab` に入れる。"""
    side = spec.get("side", "right")
    if spec.get("band"):
        # 帯のときは見出しも注記も**写真の外**に置けるので、暗幕は要らない
        g = []
    else:
        g = [J.scrim(0, 0, W, SCRIM_TOP, "top", 0.80)]
        if side == "right":
            g.append(J.scrim(1150, 0, W - 1150, H, "right", 0.62))
        else:
            g.append(J.scrim(0, 0, 770, H, "left", 0.62))
    g.append(J.title(spec["t"], spec.get("s", "")))
    ch = chapter_of(cid)
    if ch:
        g.append(J.chapter(ch[0], NCH, ch[1]))
    g.append(J.outlined(J.MG, CRED_Y, credit_of(cid, spec), J.LINE, 24, sw=5))
    return "".join(g)


def photo_ann(spec):
    """実写カットの注記。**4〜6ブロックまで**（全画面では多いと邪魔になる）。

    ann … [dict(t="巡航高度", v="7,300 m", c=J.AMBER)] を上から積む。
    """
    side = spec.get("side", "right")
    x = J.RIGHT if side == "right" else J.MG
    anchor = "end" if side == "right" else "start"
    maxw = 700
    if spec.get("band"):
        # 帯写真の注記は写真の下に横並びで置く（写真の上に載せない）
        x = J.MG if side != "right" else J.RIGHT
        maxw = 1500
    y = spec.get("ann_y", 340)
    out = []
    for a in spec.get("ann", []):
        s = []
        if a.get("t"):
            size = fm.fit(a["t"], maxw, "Noto", cap=a.get("ts", 46), floor=24)
            s.append(J.outlined(x, y, a["t"], a.get("c", J.INK_W), size, anchor,
                                sw=max(6, size * 0.17)))
            y += size + 18
        if a.get("v"):
            size = fm.fit(a["v"], maxw, "Dela", cap=a.get("vs", 96), floor=30)
            s.append(J.outlined(x, y + size * 0.20, a["v"], a.get("vc", J.AMBER),
                                size, anchor, sw=max(7, size * 0.15), family="Dela"))
            y += size + 26
        if a.get("d"):
            size = fm.fit(a["d"], maxw, "Noto", cap=a.get("ds", 34), floor=22)
            s.append(J.outlined(x, y, a["d"], a.get("dc", J.LINE), size, anchor,
                                sw=max(5, size * 0.17)))
            y += size + 16
        y += 22
        out.append("".join(s))
    return out


# ── 図解カットの地 ────────────────────────────────────────
# ★写真を地に敷くときの暗幕の濃さ（2026-07-31 試写の指摘④）。
#   ⚠️ **推定で置かない。** `tools/check_veil.py` が、写真ごとに
#      「図のいちばん細い色と地とのコントラスト比」を測って必要な濃さを出す。
#      ここは既定値で、カットごとに `veil=` で上書きできる。
# 2026-08-01 カズヤくんが見比べ画像の**5段目**を指定 → **0.76**。
# 実測では 0.76 で「図の読みやすさ 0.37／写真の見え L*20」。
# ⚠️ 机上の基準（0.50）は下回るが、**実物を見たうえでの判断**なのでこちらを採る。
#    机上の基準は「焼く前に候補を絞る」ための道具であって、目より上位ではない。
VEIL = float(os.environ.get("ZUKAI_VEIL", 0.76))


def fig_base(cid, spec, ground=True):
    """図解カットの地。

    ground=False … 写真を地に敷くカット。**不透明な地を置かない**（写真が隠れる）。
                   代わりに方眼だけ薄く残し、出典表記を必ず出す。
    """
    if ground:
        g = [J.frame(W, H)]
    else:
        # 🔴 出典は**右上**（見出しの罫の下・本体枠の上）に置く。
        #    実写カットと同じ y=872 に置いたら、本体（BAND_T 210〜BAND_B 892）の
        #    中に入って図の文字と重なった（check_layout が c115a と c628 で検出）。
        #    ここは章マーカー（y=56〜158）の下、本体の上で、どの型も使わない帯。
        g = [J.grid_only(W, H),
             J.outlined(J.RIGHT, CRED_BACK_Y, credit_of(cid, spec),
                        J.LINE, 24, anchor="end", sw=5)]
    g.append(J.title(spec["t"], spec.get("s", "")))
    ch = chapter_of(cid)
    if ch:
        g.append(J.chapter(ch[0], NCH, ch[1]))
    return "".join(g)


# ── カット表を読み込む ────────────────────────────────────
def _load_spec():
    """`tools/cuts/*.py` の SPEC を1つに束ねる。章ごとにファイルを分けてある。"""
    import cuts
    return cuts.SPEC


SPEC = _load_spec()

# ── 尺と字幕（audio/narration.json の実測） ───────────────
LEAD, TAIL = 0.35, 0.50


# 🔴 2026-08-01：カットごとに**末尾の間**を足せるようにした（カズヤくん判断）。
#    r13 の試写で quote に「決め所は前振りを読み終えてから出す」と指摘が出たが、
#    実測すると**どの quote カットも末尾は きっかり 0.50 秒（TAIL）しか無い**。
#    読み終えてから決め所を出す余地が、構造的に無かった。
#    ⚠️ ナレーションの文言も話速も変えていない。**読み終わったあとに間を足すだけ。**
#    16カット × 2.0 秒 ＝ 全体で +32 秒。
TAIL_EXTRA = {"quote": 2.0}


def _tail_extra(cid):
    fig = (SPEC.get(cid) or {}).get("fig")
    return TAIL_EXTRA.get(fig[0], 0.0) if fig else 0.0


def _narration():
    p = HERE / "audio" / "narration.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    dur = d["durations"]
    cuts = [(c, round(dur[c] + LEAD + TAIL + _tail_extra(c), 2)) for c in dur]
    return cuts, d.get("subtitles", {})


CUTS, SUBS = _narration()
ORDER = [c for c, _ in CUTS]

# 全画面の実写カット。(枠, ファイル名, 縦方向の寄せ)
PHOTO_CUTS = {cid: (photo_box(s), s["photo"], s.get("bias", 0.5))
              for cid, s in SPEC.items() if s.get("photo")}
INSETS = {}

# ★写真を地に敷くときの切り方 (横方向の寄せ, 拡大率)。
# 🔴 USCG の ROV 画像には **左端と下端に焼き込み**がある
#    （"OceanGate / Dive: 01 / Depth (m): 3774.9" と日付・HDG・Alt）。
#    実写カットではこれは**出所の証拠**なので残す。だが地に敷くと話が変わる。
#    c115a は「水深3,346メートル」を図で出しているカットで、
#    その真上に **3774.9 という別の数字**が焼き込みで出てしまった（実際に焼いて発見）。
#    → 地に敷くときだけ、焼き込みが画面外に出るところまで寄せて切る。
PHOTO_CROP = {cid: (s.get("xbias", 0.5), s.get("zoom", 1.0))
              for cid, s in SPEC.items() if s.get("photo")}


# ── 段の持ち時間 ─────────────────────────────────────────
# 段が描き終わるのに最低限これだけは残す（秒）。
# 🔴 2026-08-01：r13 の試写で「右端の枠が描き終わる前にカットが切り替わる」（process 17枚）。
#    実測すると、**行より段が多いカット**では余った段を「いちばん広い隙間の真ん中」に
#    挟んでいたので、最後の段の開始が尺の終わりぎりぎりに寄っていた
#    （c414：尺4.86秒に対し最後の段が 4.30秒から。描画0.60秒で 4.90秒＝尺を超える）。
#    → **最後の段は必ず尺の RESERVE 秒前までに出はじめる**ように押し戻す。
RESERVE = 1.0

# build_layers が段の時間割（holds / labk）を書き出す場所。layer_index が直後に読む。
STAGE_META = {}


def stage_times(cid, nstage, holds=None):
    """段 i が「出はじめる秒」と「描き終える秒」を返す。

    段はナレーションの行に合わせて出す。行より段が多ければ余った段を等間隔で挟む。
    **描き終える秒 ＝ 次の段が出る秒**（最後の段はカット終わりまで）。
    こうすると、カットのどの瞬間にも必ず「描いている途中の段」が1つある。

    holds … 段ごとの指定（`titan_fig.Fig.holds`）。**"after_last"** の段は
            **最後の行を読み終えてから**出す（引用の決め所など）。
    """
    sec = dict(CUTS)[cid]
    rows = SUBS.get(cid, [])
    starts = [r["t"] + LEAD for r in rows]
    if not starts:
        starts = [0.25]
    if nstage <= len(starts):
        st = starts[:nstage]
    else:
        # 行の切れ目を優先しつつ、足りないぶんは行の間に等間隔で挟む
        st = list(starts)
        bounds = starts + [sec]
        while len(st) < nstage:
            widest = max(range(len(bounds) - 1), key=lambda i: bounds[i + 1] - bounds[i])
            mid = (bounds[widest] + bounds[widest + 1]) / 2
            st.append(mid)
            bounds = sorted(bounds + [mid])
        st = sorted(st)[:nstage]
    # 🔴 最後の段が尺の終わりに寄りすぎていたら押し戻す（上の RESERVE を参照）
    if st and st[-1] > sec - RESERVE:
        st[-1] = max(st[0], sec - RESERVE)
        st = sorted(st)
    # ★「最後の行を読み終えてから出す」段
    if holds:
        last_end = (rows[-1]["t"] + rows[-1]["d"] + LEAD) if rows else 0.25
        for i, h in enumerate(holds[:len(st)]):
            if h == "after_last":
                # 字幕は行末 +0.12 秒までフェードで残る。そのあとに出す
                st[i] = min(max(last_end + 0.25, st[i]), max(0.25, sec - RESERVE))
    ends = st[1:] + [sec]
    # 描き終わりが早すぎると止まって見える。最低でも 1.1 秒はかける
    return [(a, max(b, a + 1.1)) for a, b in zip(st, ends)]


# ── レイヤーの組み立て ────────────────────────────────────
def build_layers(allow_missing=False):
    """cid → {レイヤー名: SVG} と、ワイプの x 範囲を返す。

    allow_missing … 章を1つずつ作っている途中は True で回す（未定義カットを飛ばす）。
    """
    jobs, spans, holds, labks = {}, {}, {}, {}
    for cid in ORDER:
        spec = SPEC.get(cid)
        if spec is None:
            if allow_missing:
                continue
            raise SystemExit(f"カット {cid} の画が定義されていません（tools/cuts/）")
        if spec.get("photo") and spec["photo"] in BANNED_PHOTOS:
            raise SystemExit(f"{cid}: {spec['photo']} は出所が無いので使えません")
        if spec.get("photo") and not spec.get("fig"):
            # 実写カット（写真だけ。注記は暗幕とフチで写真の上に載せる）
            jobs[f"{cid}_bg"] = full_bg()
            jobs[f"{cid}_lab"] = full_top(cid, spec)
            for i, a in enumerate(photo_ann(spec)):
                jobs[f"{cid}_a{i + 1}"] = a
            spans[cid] = (0, W)
            continue
        # ★写真を地に敷いたうえに図を重ねるカット（photo と fig を両方持つ）
        back = bool(spec.get("photo"))
        kind, kw = spec["fig"]
        fig = getattr(F, kind)(**kw)
        jobs[f"{cid}_base"] = fig_base(cid, spec, ground=not back)
        lab, stages = fig.lab, list(fig.stages)
        holds[cid], labks[cid] = list(fig.holds), fig.labk
        if not stages:
            # 段が無いと「描いている途中」が作れず、カットが丸ごと静止する。
            # 骨格を段に格上げして、カット全体をかけて描かせる。
            lab, stages = "", [lab]
            holds[cid] = [None]
        if lab:
            jobs[f"{cid}_lab"] = lab
        for i, s in enumerate(stages):
            jobs[f"{cid}_a{i + 1}"] = s
        if fig.hot:
            jobs[f"{cid}_hot"] = fig.hot
        # 🔴 ワイプ範囲は**必ず本体枠を含める**。
        #    型が返す span は「図の実体」しか指していないことがあり
        #    （例：icons は絵の並びだけで 640〜1280）、そのままだと枠の左右に置いた
        #    見出し・注記・出典が**ワイプの外に出て永久に現れない**。
        spans[cid] = (min(fig.span[0], F.BX0), max(fig.span[1], F.BX1))
    # ⚠️ 戻り値は (jobs, spans) のまま。`jobs, _ = build_layers()` と受けている
    #    呼び出しが4か所（check_layout / check_box / peek / layer_index）あるので、
    #    段の時間割はここに置いて layer_index が直後に読む。
    STAGE_META.clear()
    STAGE_META.update({c: {"holds": holds.get(c) or [], "labk": labks.get(c)}
                       for c in spans})
    return jobs, spans


def layer_index(allow_missing=False):
    """build_jiko が読む索引。{cid: dict(photo, layers, span, stages)}"""
    jobs, spans = build_layers(allow_missing=allow_missing)
    idx = {}
    for cid in [c for c in ORDER if c in spans]:
        s = SPEC[cid]
        names = [k for k in jobs if k.startswith(cid + "_")]
        ns = len([k for k in names if re.fullmatch(rf"{cid}_a\d+", k)])
        # photo … 写真を読む必要があるか（実写カットと、地に敷くカットの両方で True）
        # back  … **地に敷く**カットか（写真だけの実写カットと区別する）
        m = STAGE_META.get(cid, {})
        idx[cid] = {"photo": bool(s.get("photo")), "back": bool(s.get("photo") and s.get("fig")),
                    "veil": float(s.get("veil", VEIL)), "span": spans[cid],
                    "stages": ns, "layers": sorted(names),
                    "holds": m.get("holds") or [], "labk": m.get("labk")}
    return idx, jobs


def render_all(force=False, only=None, jobs_workers=4):
    """SVG → PNG。**Chrome を1レイヤーにつき1回起動する**ので並列で回す。

    226カット × 平均5レイヤー ＋ 字幕226枚 ＝ 約1,350回。直列だと20分近い。
    """
    from concurrent.futures import ThreadPoolExecutor
    OUT.mkdir(parents=True, exist_ok=True)
    ensure_css()
    jobs, _ = build_layers(allow_missing=True)
    jobs["_empty"] = J.frame(W, H)        # 余白測定の基準（check_space.py が使う）
    todo = []
    for k, svg in jobs.items():
        if only and not k.startswith(only):
            continue
        p = OUT / f"{k}.png"
        if p.exists() and not force:
            continue
        todo.append((k, svg, p, W, H))
    # ★字幕の黒帯。全カット共通の1枚。**常時貼るので必ず焼く**
    if not (only and not "_subband".startswith(only)):
        p = OUT / "_subband.png"
        if force or not p.exists():
            todo.append(("_subband", sub_band(), p, W, SUB_H))
    for cid, rows in SUBS.items():
        if only and not cid.startswith(only):
            continue
        p = OUT / f"sub_{cid}.png"
        if p.exists() and not force:
            continue
        h = SUB_H * len(rows)
        todo.append((f"sub_{cid}", sub_strip([r["text"] for r in rows]), p, W, h))
    print(f"書き出すレイヤー {len(todo)} 枚（並列 {jobs_workers}）", flush=True)
    done = [0]

    def one(t):
        k, svg, p, w, h = t
        render.png(page(svg, w, h), p, w, h)
        done[0] += 1
        if done[0] % 50 == 0:
            print(f"  {done[0]}/{len(todo)}", flush=True)

    with ThreadPoolExecutor(max_workers=jobs_workers) as ex:
        list(ex.map(one, todo))
    print(f"done {len(todo)}", flush=True)


def ensure_css():
    """フォントの base64 は4MB超。合成側では要らないので遅延で読む。"""
    global CSS
    if not CSS:
        CSS = (face_css("Dela", "DelaGothicOne.woff2")
               + face_css("Noto", "NotoSansJP-Bold.woff2")
               + face_css("NotoM", "NotoSansJP-Medium.woff2"))


def report():
    """焼く前に机上で見る要約。カット数・尺・図の種類の分布。"""
    from collections import Counter
    total = sum(s for _, s in CUTS)

    def kind_of(c):
        s = SPEC[c]
        if s.get("photo") and not s.get("fig"):
            return "photo"
        # ★写真を地に敷いた図解カットは、型の名前に「+写真」を付けて数える
        return s["fig"][0] + ("+写真" if s.get("photo") else "")

    kinds = Counter(kind_of(c) for c in ORDER if c in SPEC)
    nback = sum(1 for c in ORDER if c in SPEC
                and SPEC[c].get("photo") and SPEC[c].get("fig"))
    print(f"カット {len(ORDER)} ／ 完成尺 {total:.1f}秒 = "
          f"{int(total // 60)}分{total % 60:04.1f}秒")
    print(f"字幕 {sum(len(v) for v in SUBS.values())} 枚")
    print(f"実写 {kinds.get('photo', 0)} ／ ★写真を地に敷いた図解 {nback}")
    print("図の種類:")
    for k, v in kinds.most_common():
        print(f"   {k:<12} {v:>3}")
    miss = [c for c in ORDER if c not in SPEC]
    if miss:
        print(f"🔴 画が未定義: {miss}")
    extra = [c for c in SPEC if c not in ORDER]
    if extra:
        print(f"🔴 台本に無いカット: {extra}")

    # 🔴 2026-08-02：**写真が git に入っていなくて r24 が失敗した。**
    #    `.gitignore` が `ref/*` を除外して許可制（`!ref/…` を1行ずつ）にしているので、
    #    新しい写真を置いても `git add -A` が**黙って落とす**。
    #    ローカルにはファイルがあるから机上検査は全部通り、写真を実際に開くのは
    #    クラウドの `build_jiko` だけなので、**40分焼いた最後に FileNotFoundError**
    #    になる。押す前にここで気づけるようにする。
    #
    # ⚠️ **この検査は最初に作ったとき間違っていた**（2026-08-02・作り直し）。
    #    `git ls-files` は**索引（add した状態）**を答えるので、
    #    `git add` して**commit していない**ファイルを「入っている」と言う。
    #    r24 が落ちたときのリポジトリがまさにその状態で、
    #    **この検査は 0件と答えていた**。クラウドが checkout するのは索引ではなく
    #    **push 済みのコミット**なので、そこを見なければ意味が無い。
    #    → HEAD のツリー（`ls-tree`）を見る。さらに push 済みかも見る。
    used = sorted({v[1] for v in PHOTO_CUTS.values()})
    nofile = [n for n in used if not (HERE / "ref" / n).exists()]
    if nofile:
        print(f"🔴 ref に実体が無い写真: {nofile}")

    def _git(*a):
        import subprocess
        r = subprocess.run(["git", *a], cwd=HERE, capture_output=True,
                           text=True, timeout=20)
        return r.stdout if r.returncode == 0 else None

    uncommitted = []
    head = _git("ls-tree", "-r", "--name-only", "HEAD", "ref/")
    if head is None:                            # git が無い環境（クラウド）では黙る
        print("   （git を確認できないので追跡の検査は飛ばす）")
    else:
        intree = set(head.split())
        uncommitted = [n for n in used if f"ref/{n}" not in intree]
        if uncommitted:
            print(f"🔴 **コミットされていない写真** {len(uncommitted)}件: {uncommitted}")
            print("   → `.gitignore` の許可制リストに `!ref/<名前>` を1行ずつ足して"
                  "**commit する**。add しただけではクラウドに届かない。")
        # コミット済みでも push していなければクラウドは古い版を焼く
        ahead = _git("rev-list", "--count", "@{u}..HEAD")
        if ahead is None:
            print("   （上流が無いので push の検査は飛ばす）")
        elif int(ahead.strip() or 0):
            # 押せば直る（写真そのものは在る）ので、戻り値は落とさず警告だけ出す
            print(f"🔴 **push していないコミットが {ahead.strip()} 個ある。**"
                  "クラウドは古い版を焼く → `git push` してから回すこと")
    return not (miss or extra or nofile or uncommitted)


if __name__ == "__main__":
    if "--report" in sys.argv:
        sys.exit(0 if report() else 1)
    render_all(force="--force" in sys.argv,
               only=next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")),
                         None))
