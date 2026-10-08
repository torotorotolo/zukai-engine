# -*- coding: utf-8 -*-
"""illu20.py — 案C の再現イラスト：20本目（日本航空123便・JA8119・1985-08-12）の置き場 S1・S2・S3（⑤b-3・2026-10-08 新設）。

`tools/illu.py` の末尾で読み込み、型の表（FIELDS・CHOICES・VIEWS・REC_FIELDS・NOTE）と置き場の登録 `illu.EXTRA` へ足す
（illu.py に1つずつ書き足すと 7,500 行の中で回の境が見えなくなる＝回の置き場は回のファイルに）。
🔴 §0b（題材を替えるとき）：このファイルは20本目の型の値そのもの＝次の回は読み込みを外すか、置き場の名がぶつからないか確かめる。

■ 置き場（台本 第2版 §4 の画の欄・映像方針 20本目・一覧 `ref/ep20/eizou_list20.md` の S1〜S3）
  S1 … 横から見た機体（ボーイング式747SR-100型・機首が左）。形のもと＝報告書 付図-4（三面図＝全長 231 FT 4 IN・高さ 63 FT 5 IN・
       エンジンの位置）・胴体の番地（BS）＝2.4.2.1 p.9（機首 BS90・セクション46＝BS1480〜2360・セクション48＝BS2360〜2792・
       BS2658 から後ろのテールコーン）・後部圧力隔壁＝BS2360（p.29）。
       欄＝s1cab（客室を明るく）・s1ck（操縦室を明るく）・s1mask（酸素マスク off／drop）・s1press（与圧の範囲の色）・s1bulk（後部圧力隔壁の形）・
       s1ring（黄色の輪 off／cockpit／tail）・s1fin（on／lost＝垂直尾翼と尾部胴体が欠けた形＝頭だけ・推定の札と一緒に）・switch（頭だけ）
  S2 … 上から見た経路の地図（北が上）。経路と時刻の点＝付図-1 を Natural Earth の海岸線に重ねて読んだ `ref/ep20/route20.json`
       （`ref/ep20/route20.py`）・陸と海＝`ref/ep20/coast_ne10m.json`（Natural Earth 1:10m・PD）。
       欄＝s2t（その段の時刻 "18:24:35"＝経路をそこまで描き、機の印を置く。"end"＝墜落地点まで描いて印を消す）・s2plane・s2yok（横田）・
       s2kum（熊谷）・s2lines（羽田と熊谷から機へ結ぶ線）・s2ngo（名古屋の向きの矢印）・s2ring（強める輪 off／haneda／yokota／both／sagami）・
       s2crash（墜落地点の印）・switch。出来事 rings（その段の機の位置に音の輪＝c209 の「ドーン」）
  S3 … 2つの揺れの模式（記録のグラフではない）。view＝side（横から＝フゴイド）／front（正面から＝ダッチロール）／both（並べる＝c410）。
       欄＝s3wave（波の道を進む）・s3amp（高さの差のかっこ）・s3pitch（機首の上げの角の印）・s3roll（左右に傾く＝頭だけ）・switch
■ 守りの線（ルール §5b-74・映像方針 20本目・台本 第2版の画の欄「人は描かない」）
  ・人は描かない（S1〜S3）＝`ss.ILLU_ROLES` は空のまま。部品は数（obj）を持たない（マスクの数・窓の数は模式＝断りに書く）
  ・欠けた機体（S1 の s1fin＝lost）は表のカット（`ss.ILLU_DESTROY_CUTS`）だけ・「推定」の札（欠けた範囲の形は報告書も特定できない＝p.107）
  ・墜落の時刻は札に出さない（付図-1「18:56'30」と 2.1 p.8「18時56分ごろ」＝割れる＝`ss.ILLU_SPLIT_TIMES`）
  ・S3 の数は 3.2.6.2 p.113（縦揺れ角±約15度・速度変化約100ノット・高度変化約4,000フィート）・p.114（横揺れ角±約40度）だけ。
    角の印は本当の角度（15度・40度）で描く（模式でも角だけは記録の値＝門番 ㉖）
  ・門番 `check_illu` の ㉔（S1）・㉕（S2）・㉖（S3）は記録の値を門番の側に持つ（§5b-88＝ここの定数を読まない）
"""
from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path

import illu as IL
import titan_fig as F

W, H = IL.W, IL.H
REF = Path(__file__).resolve().parent.parent / "ref" / "ep20"
KEY_DELAY = IL.KEY_DELAY
_part = IL._part

# ── 絵の色（全章で固定・章の色の置き換えが拾う値＝jiko_style の BG・BG2・GRID・LINE・LINE_DIM・TICK・INK_W を使わない）──
C20 = dict(
    sky0="#17263a", sky1="#46617e", sky2="#b88d6e", cloud="#8597a8",
    body="#e3e7eb", body_ln="#26313b", win="#3b5064", wing="#a9b3bc", eng="#bcc5cc", eng_dk="#5a6670",
    fin="#d7dce1", rud="#c9d0d6", stab="#b5bec6", cabin="#f4e4bd", press="#79c2d6", bulk="#f2c14e",
    mask="#f2d24a", mask_ln="#5b4c17", ring="#f2c14e", tear="#59646d", dark="#141c24",
    sea="#1d3a55", land="#596855", land_ln="#a7b8b1", route="#f4efe6", route_ln="#16202a", plane="#f2c14e",
    name="#e8eef1", hl="#f2c14e", line2="#f6d77a")
LAB = dict(S1="横から見た図", S2="上から見た図（北が上）", S3=dict(side="横から見た模式", front="正面から見た模式",
                                                                both="2つの揺れの模式（横から・正面から）"))


def _d(pts, close=True):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")


def _path(pts, fill, stroke=None, sw=0.0, op=None, close=True, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<path d="{_d(pts, close)}" fill="{fill}"{st}{o}{extra}/>'


def _text(x, y, t, size=26, col=None, anchor="middle"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Noto" font-size="{size}" fill="{col or C20["name"]}" '
            f'text-anchor="{anchor}" stroke="#10161b" stroke-width="5" stroke-linejoin="round" paint-order="stroke fill">'
            f'{F.esc(t)}</text>')


def _sky_svg(gid):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C20["sky0"]}"/>'
            f'<stop offset="0.7" stop-color="{C20["sky1"]}"/><stop offset="1" stop-color="{C20["sky2"]}"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{gid})"/>')


def _clouds_svg(y0=830.0, seed=3):
    """下の雲の帯（形は模式＝記録に無い）。"""
    g = []
    for k in range(9):
        cx = 120.0 + k * 215.0 + 40.0 * math.sin(k * 1.7 + seed)
        ry = 26.0 + 10.0 * math.sin(k * 2.3 + seed)
        g.append(f'<ellipse cx="{cx:.0f}" cy="{y0 + 30 * math.sin(k * 0.9 + seed):.0f}" rx="{170 + 30 * math.sin(k):.0f}" '
                 f'ry="{ry:.0f}" fill="{C20["cloud"]}" opacity="0.30"/>')
    g.append(f'<rect x="0" y="{y0 + 40:.0f}" width="{W}" height="{H - y0 - 40:.0f}" fill="{C20["cloud"]}" opacity="0.22"/>')
    return "".join(g)


def _switch_part(text):
    return dict(_part("switch", IL.va_switch_svg(text), "", keys=IL._switch_keys()), signal=True)


def _akeys(start, states, steps, on, dur=0.6, extra=0.0):
    """濃さだけの鍵（on＝状態 → 見せるか）。段の行頭＋delay から dur 秒で"""
    ks = [dict(stage=0, delay=0.0, a=float(on(start)))]
    cur = on(start)
    for i, (st, sp) in enumerate(zip(states, steps)):
        v = on(st)
        if v != cur:
            ks.append(dict(stage=i, delay=float(sp.get("delay", KEY_DELAY)) + extra, dur=float(sp.get("dur", dur)), a=float(v)))
            cur = v
    return ks


def _head_only(place, start, states, fields):
    for f in fields:
        if any(st[f] != start[f] for st in states):
            raise ValueError(f"illu {place}：{f} は場面の頭（start）で1つだけ")


# ══════════════════════════════════════════════════════════
#  S1 横から見た機体（747SR-100・機首が左）
# ══════════════════════════════════════════════════════════
S1_K = 21.5                       # 1メートル＝21.5画素（全長 70.5m＝1,516画素）
S1_X0, S1_Y0 = 212.0, 600.0       # 機首の先の x・胴体の真ん中の y
S1_LEN = 231 * 0.3048 + 4 * 0.0254          # 付図-4「231 FT 4 IN」＝70.51m
S1_BS_NOSE, S1_BS_BULK, S1_BS_CONE = 90.0, 2360.0, 2658.0   # p.9・p.29（インチ）


def s1_x(bs):
    """胴体の番地（BS・インチ）→ 機首からのメートル"""
    return (bs - S1_BS_NOSE) * 0.0254


def P1(x, z):
    return (S1_X0 + x * S1_K, S1_Y0 - z * S1_K)


S1_XB, S1_XC = s1_x(S1_BS_BULK), s1_x(S1_BS_CONE)        # 57.66m・65.22m
# 胴体の輪郭（メートル・機首からの x・真ん中からの z）。付図-4 の横の図の見え方（2階の膨らみは SR の短い2階）＝形は模式
S1_UP = [(0.0, -0.35), (0.6, 0.7), (1.6, 1.75), (2.9, 2.75), (4.4, 3.75), (6.2, 4.6), (8.5, 5.15), (11.0, 5.3), (16.5, 5.3),
         (19.0, 5.0), (21.5, 4.2), (24.0, 3.55), (27.0, 3.35), (52.0, 3.35), (57.0, 3.25), (61.0, 3.0), (65.0, 2.55),
         (68.5, 2.05), (S1_LEN, 1.75)]
S1_LO = [(0.0, -0.35), (0.5, -1.3), (1.5, -2.2), (3.2, -2.85), (6.0, -3.25), (10.0, -3.35), (48.0, -3.35), (52.0, -3.2),
         (56.0, -2.7), (60.0, -1.85), (64.0, -0.85), (67.5, 0.15), (S1_LEN, 1.05)]
S1_FIN = [(58.8, 3.1), (67.3, 14.6), (71.2, 14.6), (69.9, 2.1)]          # 前縁の根元・前縁の先・後縁の先・後縁の根元
S1_RUD = [(66.2, 2.6), (69.9, 14.6), (71.2, 14.6), (69.9, 2.1)]          # 方向舵（後ろ約3割＝付図-4・付図-7 の見え方）
S1_STAB = [(61.0, 1.85), (63.5, 2.45), (70.3, 2.75), (70.6, 2.35), (66.5, 1.9)]
S1_WING = [(22.5, -1.5), (26.0, -1.15), (46.5, 0.15), (47.4, -0.2), (36.0, -2.35), (33.0, -2.65)]
S1_ENG = [(21.4, 29.6, -3.55, 1.35), (31.9, 39.4, -2.45, 1.3)]           # 内側・外側の手前のエンジン（付図-4 の横の図の位置）
S1_CABIN = (6.2, 56.6, -2.25, 2.55)                                       # 客室（明るくする範囲＝模式）
# 操縦室（2階の前＝付図-12 の席の並び）。⑤b-3 の試し焼き：細いくさび形に黄色の縁で機首の上の「帽子」に見えた＝胴体の上の線に
#   沿って内側へ寄せた形を滑らかにし、縁は細く
S1_COCK = [(2.2, 1.95), (3.3, 2.75), (4.6, 3.6), (6.3, 4.3), (7.8, 4.5), (7.8, 1.95)]
S1_CEIL = 2.35                                                             # マスクが下がる天井の高さ（模式）
# ⑤b-3 の試し焼き（c216）：0.9m 上から下ろすと、下りる途中の管と玉が胴体の上の線より外へはみ出した＝0.6m だけ下ろす
#   （始め＝玉が天井・管の上の端 z 2.95 は胴体の上の線 3.35 の内側）
S1_MASK_DROP = 0.6 * S1_K
S1_LOST_FIN = [(58.8, 3.1), (61.4, 6.9), (62.2, 6.3), (62.9, 7.2), (63.6, 6.1), (64.3, 6.6), (64.8, 5.1), (64.4, 4.2),
               (64.9, 3.3), (64.6, 2.7)]                                   # 残った前の下の部分（模式＝範囲は特定できない）
S1_T = dict(drop=1.4, show=0.6, ring=0.5, press=0.9)
S1_REC = dict(
    sky="報告書 p6（巡航高度24,000フィートに到達する直前）",
    body="報告書 p140（付図-4 三面図＝全長 231 FT 4 IN・高さ 63 FT 5 IN・エンジンの位置）・p9（BS90〜・セクション48＝BS2360〜2792）",
    cabin="報告書 p141（付図-5 胴体ステーション及び座席配置図）",
    cockpit="報告書 p6（機長が右操縦士席、副操縦士が左操縦士席）・p148（付図-12 操縦室パネル配置図）",
    masks="報告書 p91（客室内の酸素マスクが落下するとともにPRAが開始された）",
    press="報告書 p106（客室与圧空気は、後部圧力隔壁の…部分から後部胴体内に流出）",
    bulk="報告書 p29（BS2360＝後部圧力隔壁の取付部）・p35（18枚のウエブをドーム状に並べ）",
    tail="報告書 p143（付図-7 尾翼ステーション図）・p9（BS2658 以降のテールコーン）",
    lost="報告書 p106（APU 防火壁が後方の構造とともに脱落したと推定）・p107（アフト・トルクボックスの倒壊・方向舵の脱落＝詳細は特定できない）")


def _s1_outline(cut=None, jag=True):
    """胴体の輪郭の画素（cut＝その x〈メートル〉より後ろを切った形・jag＝切り口をぎざぎざに〈壊れた所〉／まっすぐ〈色の範囲〉）。"""
    up = IL._smooth(S1_UP, per=6)
    lo = IL._smooth(S1_LO, per=6)
    if cut is not None:
        def clip(pts):
            out = [p for p in pts if p[0] < cut]
            for a, b in zip(pts, pts[1:]):
                if a[0] < cut <= b[0]:
                    out.append((cut, a[1] + (b[1] - a[1]) * (cut - a[0]) / (b[0] - a[0])))
                    break
            return out
        up, lo = clip(up), clip(lo)
        zt, zb = up[-1][1], lo[-1][1]
        mid = [(cut + (0.45 if k % 2 else -0.35), zt + (zb - zt) * k / 7.0) for k in range(1, 7)] if jag else []
        return [P1(*p) for p in up] + [P1(*p) for p in mid] + [P1(*p) for p in reversed(lo)]
    return [P1(*p) for p in up] + [P1(*p) for p in reversed(lo)]


def s1_body_svg(cut=None):
    out = _s1_outline(cut)
    g = [_path(out, C20["body"], C20["body_ln"], 3.0)]
    # 窓の帯（客室・2階）＝数は模式
    xa, xb = P1(7.0, 0)[0], P1(min(55.0, (cut or 99) - 1.0), 0)[0]
    y = P1(0, 1.25)[1]
    g.append(f'<path d="M {xa:.1f} {y:.1f} L {xb:.1f} {y:.1f}" stroke="{C20["win"]}" stroke-width="7" stroke-dasharray="5 6"/>')
    xa2, xb2, y2 = P1(10.5, 0)[0], P1(17.5, 0)[0], P1(0, 4.15)[1]
    g.append(f'<path d="M {xa2:.1f} {y2:.1f} L {xb2:.1f} {y2:.1f}" stroke="{C20["win"]}" stroke-width="6" stroke-dasharray="5 7"/>')
    g.append(_path([P1(2.3, 2.45), P1(3.6, 3.2), P1(4.5, 3.3), P1(4.3, 2.75), P1(2.9, 2.2)], C20["win"]))
    if cut is None:
        g.append(f'<circle cx="{P1(S1_LEN - 0.15, 1.4)[0]:.1f}" cy="{P1(0, 1.4)[1]:.1f}" r="6" fill="{C20["eng_dk"]}"/>')
    return "".join(g)


def s1_wing_svg():
    g = [_path([P1(*p) for p in S1_WING], C20["wing"], C20["body_ln"], 2.5)]
    for x0, x1, zc, r in S1_ENG:
        g.append(_path([P1(x0 + 2.5, zc + r * 0.6), P1(x0 + 4.2, -1.0 if zc < -3 else -0.2),
                        P1(x0 + 5.6, -1.2 if zc < -3 else -0.5), P1(x0 + 5.2, zc + r * 0.6)], C20["wing"], C20["body_ln"], 2.0))
        pts = [P1(x0, zc + r), P1(x1 - 1.2, zc + r * 0.95), P1(x1, zc + r * 0.45), P1(x1, zc - r * 0.45),
               P1(x1 - 1.2, zc - r * 0.95), P1(x0, zc - r)]
        g.append(_path(pts, C20["eng"], C20["body_ln"], 2.5))
        g.append(f'<ellipse cx="{P1(x0, 0)[0]:.1f}" cy="{P1(0, zc)[1]:.1f}" rx="5" ry="{r * S1_K:.1f}" fill="{C20["eng_dk"]}"/>')
    return "".join(g)


def s1_fin_svg():
    return (_path([P1(*p) for p in S1_STAB], C20["stab"], C20["body_ln"], 2.0)
            + _path([P1(*p) for p in S1_FIN], C20["fin"], C20["body_ln"], 3.0)
            + _path([P1(*p) for p in S1_RUD], C20["rud"], C20["body_ln"], 2.0)
            + f'<path d="M {P1(68.0, 8.6)[0]:.1f} {P1(0, 8.6)[1]:.1f} L {P1(70.55, 8.6)[0]:.1f} {P1(0, 8.6)[1]:.1f}" '
              f'stroke="{C20["body_ln"]}" stroke-width="1.6"/>')


def s1_fin_lost_svg():
    """欠けた垂直尾翼（前の下の部分だけ＝模式）と水平尾翼"""
    return (_path([P1(*p) for p in S1_STAB], C20["stab"], C20["body_ln"], 2.0)
            + _path([P1(*p) for p in S1_LOST_FIN], C20["fin"], C20["body_ln"], 3.0))


def s1_cabin_svg():
    x0, x1, z0, z1 = S1_CABIN
    a, b = P1(x0, z1), P1(x1, z0)
    return (f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" rx="26" '
            f'fill="{C20["cabin"]}" opacity="0.62" stroke="{C20["bulk"]}" stroke-width="3"/>')


def s1_cockpit_svg():
    pts = [P1(*p) for p in IL._smooth(S1_COCK, closed=True, per=5)]
    return _path(pts, C20["cabin"], C20["bulk"], 2.0, op=0.75)


def s1_masks_svg():
    """天井から下がった酸素マスク（下がりきった形＝鍵で天井から下ろす）。数と並びは模式"""
    g = []
    x = 7.6
    yc = P1(0, S1_CEIL)[1]
    while x < 55.6:
        px = P1(x, 0)[0]
        g.append(f'<path d="M {px:.1f} {yc:.1f} L {px:.1f} {yc + S1_MASK_DROP - 4:.1f}" stroke="{C20["mask_ln"]}" stroke-width="2"/>'
                 f'<ellipse cx="{px:.1f}" cy="{yc + S1_MASK_DROP + 1:.1f}" rx="6.5" ry="5.5" fill="{C20["mask"]}" '
                 f'stroke="{C20["mask_ln"]}" stroke-width="1.6"/>')
        x += 1.05
    return "".join(g)


def s1_press_svg():
    """与圧の範囲（機首から後部圧力隔壁 BS2360 まで）の色"""
    return _path(_s1_outline(S1_XB, jag=False), C20["press"], None, 0, op=0.5)


def s1_bulk_svg():
    """後部圧力隔壁（お椀の形＝後ろへふくらむ。横から見ると弧）"""
    zt, zb = 3.05, -2.75
    pts = [(S1_XB + 1.25 * math.cos(math.radians(a)), (zt + zb) / 2 + (zt - zb) / 2 * math.sin(math.radians(a)))
           for a in range(-90, 91, 10)]
    q = [P1(*p) for p in pts]
    return (f'<path d="{_d(q, False)}" fill="none" stroke="{C20["dark"]}" stroke-width="11" stroke-linecap="round"/>'
            f'<path d="{_d(q, False)}" fill="none" stroke="{C20["bulk"]}" stroke-width="6" stroke-linecap="round"/>')


def s1_ring_svg(c, r):
    return (f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" fill="none" stroke="{C20["dark"]}" stroke-width="11" opacity="0.6"/>'
            f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" fill="none" stroke="{C20["ring"]}" stroke-width="6"/>')


S1_RINGS = dict(cockpit=(P1(4.0, 3.3), 3.4 * S1_K), tail=(P1(59.6, 0.6), 4.9 * S1_K))


def _scene_S1(start, states, steps):
    allst = [start] + states
    _head_only("S1", start, states, ("view", "s1fin", "switch"))
    lost = start["s1fin"] == "lost"
    if lost and any(st["s1mask"] != "off" or st["s1press"] != "off" for st in allst):
        raise ValueError("illu S1：欠けた機体（s1fin＝lost）の場面にマスク・与圧の色を重ねない（場面を分ける）")
    R = S1_REC
    on = (lambda f, v="on": (lambda st: st[f] == v))
    parts = [_part("sky", _sky_svg("s1Sky") + _clouds_svg(), R["sky"])]
    if lost:
        parts.append(dict(_part("body_lost", s1_body_svg(cut=S1_XC), R["lost"]), destroy=True,
                          geo=dict(kind="body", nose_x=P1(0, 0)[0], tail_x=P1(S1_LEN, 0)[0], len_m=S1_LEN,
                                   cut_x=P1(S1_XC, 0)[0])))
    else:
        parts.append(dict(_part("body", s1_body_svg(), R["body"]),
                          geo=dict(kind="body", nose_x=P1(0, 0)[0], tail_x=P1(S1_LEN, 0)[0], len_m=S1_LEN, cut_x=None)))
    if any(st["s1press"] == "on" for st in allst):
        parts.append(_part("press", s1_press_svg(), R["press"], keys=_akeys(start, states, steps, on("s1press"), S1_T["press"])))
    if any(st["s1cab"] == "on" or st["s1mask"] != "off" for st in allst):
        parts.append(_part("cabin", s1_cabin_svg(), R["cabin"],
                           keys=_akeys(start, states, steps, lambda st: st["s1cab"] == "on" or st["s1mask"] != "off")))
    if any(st["s1mask"] != "off" for st in allst):
        ks = [dict(stage=0, delay=0.0, a=float(start["s1mask"] == "drop"), dy=0.0 if start["s1mask"] == "drop" else -S1_MASK_DROP)]
        cur = start["s1mask"]
        for i, (st, sp) in enumerate(zip(states, steps)):
            if st["s1mask"] != cur:
                d = float(sp.get("delay", KEY_DELAY))
                ks.append(dict(stage=i, delay=d, dur=0.2, a=1.0, dy=-S1_MASK_DROP))
                ks.append(dict(stage=i, delay=d + 0.2, dur=float(sp.get("dur", S1_T["drop"])), a=1.0, dy=0.0))
                cur = st["s1mask"]
        parts.append(dict(_part("masks", s1_masks_svg(), R["masks"], keys=ks), geo=dict(kind="masks")))
    if any(st["s1ck"] == "on" for st in allst):
        parts.append(_part("cockpit", s1_cockpit_svg(), R["cockpit"], keys=_akeys(start, states, steps, on("s1ck"))))
    parts.append(_part("wing", s1_wing_svg(), R["body"]))
    if lost:
        parts.append(dict(_part("fin_lost", s1_fin_lost_svg(), R["lost"]), destroy=True, geo=dict(kind="fin", lost=True)))
    else:
        parts.append(dict(_part("fin", s1_fin_svg(), R["tail"]), geo=dict(kind="fin", lost=False)))
    if any(st["s1bulk"] == "on" for st in allst):
        parts.append(dict(_part("bulk", s1_bulk_svg(), R["bulk"], keys=_akeys(start, states, steps, on("s1bulk"))),
                          geo=dict(kind="bulk", x=P1(S1_XB, 0)[0])))
    for nm in ("cockpit", "tail"):
        if any(st["s1ring"] == nm for st in allst):
            c, r = S1_RINGS[nm]
            parts.append(_part("ring_" + nm, s1_ring_svg(c, r), R["cockpit" if nm == "cockpit" else "bulk"],
                               keys=_akeys(start, states, steps, on("s1ring", nm), S1_T["ring"])))
    if start["switch"] == "on":
        parts.append(_switch_part("横から見ると"))
    return parts


def _s1_anchors(st):
    lost = st["s1fin"] == "lost"
    return dict(cabin=P1(31.0, 0.6), cockpit=P1(4.2, 4.0), bulk=P1(S1_XB + 1.0, 0.4), tail=P1(61.5, 3.4),
                fin=P1(62.4, 6.6) if lost else P1(66.0, 10.5), masks=P1(31.0, 1.2), nose=P1(1.0, 0.0),
                cone=P1(S1_XC, 2.0), wing=P1(36.0, -1.4))


def _s1_note(st0, states):
    allst = [st0] + list(states)
    note = ["形は付図-4 の三面図から・大きさと配置は模式・人は描かない"]
    if any(st["s1mask"] != "off" for st in allst):
        note.append("マスクの数と並びは模式")
    if st0["s1fin"] == "lost":
        note.append("欠けた範囲は模式（報告書も詳しい形は特定できない）")
    return "・".join(note)


# ══════════════════════════════════════════════════════════
#  S2 上から見た経路の地図（北が上）
# ══════════════════════════════════════════════════════════
S2_LAT0 = 35.4                              # route20.py と同じ平らにし方（正距円筒）
S2_KX = math.cos(math.radians(S2_LAT0)) * 111.32
S2_KY = 110.57
S2_S = 4.6                                  # 1km＝4.6画素（1画素≒217m）
S2_C = (139.055, 35.378)                    # 画面の真ん中（東経・北緯）
S2_PX = (960.0, 500.0)
S2_T0 = "18:12:00"                          # 経路の頭＝離陸（2.1 p.6「18時12分滑走路15Lから離陸」）
# 地点（経度・緯度）。地名の位置は一般の地図の値（付図-1 の地名の点と重ねて 1〜2km 以内＝route20.py の重ね）
S2_PTS = dict(haneda=(139.780, 35.549), fuji=(138.727, 35.361), yokota=(139.348, 35.749), kumagaya=(139.388, 36.147),
              yaizu=(138.324, 34.867), otsuki=(138.94, 35.575), oshima=(139.40, 34.74), nagoya=(136.924, 35.255),
              # 三国山＝墜落地点（2.1 p.8）の「南南東 約2.5km」（「三国山の北北西約2.5キロメートル」の逆）
              mikuni=(138.6969 + 2.5 * math.sin(math.radians(22.5)) / (111.32 * math.cos(math.radians(36.0))),
                      35.9983 - 2.5 * math.cos(math.radians(22.5)) / 110.57),
              sagami=(139.35, 35.12))
# ⑤b-3 の門番 layout：「駿河湾」を湾の真ん中（東経138.63度）に置くと、駿河湾の上の機の印から出す札の線が貫いた＝湾の西へ寄せた
# ⑤b-3 の試し焼き：「大島」を島の南に置くと左下の出典の行のすぐ上に来た＝島の東へ
S2_NAMES = (("伊豆半島", (138.96, 34.93)), ("駿河湾", (138.47, 34.94)), ("相模湾", (139.37, 35.12)), ("大島", (139.53, 34.765)))
S2_SCALE_KM = 20.0
S2_T = dict(trace=2.6, show=0.6, ring=0.5)
S2_REC = dict(
    map="報告書 p137（付図-1 JA8119飛行経路略図）",
    names="報告書 p137（付図-1 の地名＝東京国際空港（羽田）・富士山・伊豆半島・大島）",
    trace="報告書 p137（付図-1 の経路と時刻の点）・p6（18時12分滑走路15Lから離陸）",
    plane="報告書 p137（付図-1 の経路）",
    yokota="報告書 p7（羽田も横田も受け入れ可能）・p137（付図-1 の横田飛行場）",
    kumagaya="報告書 p7（羽田の北西55海里、熊谷の西25海里の地点）",
    nagoya="報告書 p7（名古屋空港から72海里の地点）",
    crash="報告書 p8（北緯35度59分54秒、東経138度41分49秒）",
    sagami="報告書 p13（相模湾等から…浮遊残骸が揚収された）",
    boom="報告書 p6（18時24分35秒…「ドーン」というような音とともに）")


def P2(lon, lat):
    return (S2_PX[0] + (lon - S2_C[0]) * S2_KX * S2_S, S2_PX[1] - (lat - S2_C[1]) * S2_KY * S2_S)


def _sec(t):
    h, m, s = (int(v) for v in t.split(":"))
    return h * 3600 + m * 60 + s


@lru_cache(maxsize=1)
def s2_route():
    """経路の画素の折れ線・長さの累積・時刻の点（秒 → 長さ）。"""
    d = json.loads((REF / "route20.json").read_text(encoding="utf-8"))
    pts = [P2(lon, lat) for lon, lat in d["route"]]
    crash = P2(d["crash"]["lon"], d["crash"]["lat"])
    pts.append(crash)
    cum = [0.0]
    for p, q in zip(pts, pts[1:]):
        cum.append(cum[-1] + math.hypot(q[0] - p[0], q[1] - p[1]))

    def proj(p, i0):
        """経路の上の一番近い点の長さ。🔴 大月の上の1回転で経路が自分と交わる＝前の時刻の点の区間 i0 から先の 30 区間だけを探す
        （全部を探すと、入る所の点が出る所の線に当たって長さが先へ飛ぶ）"""
        best = None
        for i in range(i0, min(len(pts) - 2, i0 + 30)):
            a, b = pts[i], pts[i + 1]
            vx, vy = b[0] - a[0], b[1] - a[1]
            L2 = vx * vx + vy * vy or 1e-9
            u = max(0.0, min(1.0, ((p[0] - a[0]) * vx + (p[1] - a[1]) * vy) / L2))
            q = (a[0] + vx * u, a[1] + vy * u)
            dd = math.hypot(p[0] - q[0], p[1] - q[1])
            if best is None or dd < best[0]:
                best = (dd, cum[i] + math.sqrt(L2) * u, i)
        if best[0] > 4.0:
            raise ValueError(f"illu S2：時刻の点が経路から {best[0]:.1f} 画素離れた（route20.json を確かめる）")
        return best[1], best[2]
    ticks = [(_sec(S2_T0), 0.0, S2_T0)]
    i0 = 0
    for tk in d["ticks"]:
        s, i0 = proj(P2(tk["lon"], tk["lat"]), i0)
        ticks.append((_sec(tk["t"]), s, tk["t"]))
    for a, b in zip(ticks, ticks[1:]):
        if not (b[0] > a[0] and b[1] > a[1]):
            raise ValueError(f"illu S2：時刻の点の並びが経路の上で戻る（{a[2]}→{b[2]}）")
    return dict(pts=pts, cum=cum, ticks=ticks, crash=crash, total=cum[-1])


def s2_len(t):
    """時刻 t（"18:24:35"・"end"）の経路の上の長さ（画素）。時刻の点のあいだは時間に比例（目安）"""
    R = s2_route()
    if t == "end":
        return R["total"]
    s = _sec(t)
    tk = R["ticks"]
    if not tk[0][0] <= s <= tk[-1][0]:
        raise ValueError(f"illu S2：時刻 {t} は付図-1 の点の範囲（{tk[0][2]}〜{tk[-1][2]}）の外")
    for a, b in zip(tk, tk[1:]):
        if a[0] <= s <= b[0]:
            return a[1] + (b[1] - a[1]) * (s - a[0]) / (b[0] - a[0])
    return tk[-1][1]


def s2_pos(t):
    R = s2_route()
    s = s2_len(t)
    for (p, q), c0, c1 in zip(zip(R["pts"], R["pts"][1:]), R["cum"], R["cum"][1:]):
        if s <= c1 + 1e-9:
            f = (s - c0) / (c1 - c0) if c1 > c0 else 0.0
            return (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)
    return R["pts"][-1]


def s2_base_svg():
    g = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{C20["sea"]}"/>']
    d = json.loads((REF / "coast_ne10m.json").read_text(encoding="utf-8"))
    for poly in d["polys"]:
        g.append(_path([P2(lon, lat) for lon, lat in poly], C20["land"], C20["land_ln"], 1.8))
    return "".join(g)


def s2_names_svg():
    g = []
    hx, hy = P2(*S2_PTS["haneda"])
    g.append(f'<rect x="{hx - 7:.1f}" y="{hy - 7:.1f}" width="14" height="14" fill="{C20["name"]}" stroke="#10161b" stroke-width="2.5"/>')
    g.append(_text(hx + 16, hy + 9, "羽田", 28, anchor="start"))
    fx, fy = P2(*S2_PTS["fuji"])
    g.append(_path([(fx, fy - 11), (fx + 10, fy + 7), (fx - 10, fy + 7)], C20["name"], "#10161b", 2.0))
    g.append(_text(fx, fy + 36, "富士山", 24))
    for t, (lon, lat) in S2_NAMES:
        x, y = P2(lon, lat)
        g.append(_text(x, y, t, 26 if t != "大島" else 24))
    return "".join(g)


def s2_scale_svg():
    L = S2_SCALE_KM * S2_S
    x1, y = 1790.0, 846.0
    x0 = x1 - L
    return (f'<path d="M {x0:.1f} {y - 8:.1f} L {x0:.1f} {y:.1f} L {x1:.1f} {y:.1f} L {x1:.1f} {y - 8:.1f}" fill="none" '
            f'stroke="#10161b" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M {x0:.1f} {y - 8:.1f} L {x0:.1f} {y:.1f} L {x1:.1f} {y:.1f} L {x1:.1f} {y - 8:.1f}" fill="none" '
            f'stroke="{C20["name"]}" stroke-width="3" stroke-linejoin="round"/>'
            + _text((x0 + x1) / 2, y - 16, f"{S2_SCALE_KM:.0f}キロ", 24))


def s2_trail_svg():
    pts = s2_route()["pts"]
    d = _d(pts, False)
    return (f'<path d="{d}" fill="none" stroke="{C20["route_ln"]}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round" '
            f'opacity="0.75"/><path d="{d}" fill="none" stroke="{C20["route"]}" stroke-width="4.5" stroke-linejoin="round" '
            'stroke-linecap="round"/>')


S2_MK = (960.0, 540.0)


def s2_plane_svg():
    """機の印（上から・機首が +x・拡大＝断り「機の印は拡大」）"""
    cx, cy = S2_MK
    k = 0.62

    def P(x, y):
        return (cx + x * k, cy + y * k)
    body = [P(30, 0), P(24, -4), P(-22, -4), P(-30, -2), P(-30, 2), P(-22, 4), P(24, 4)]
    wing = [P(8, -4), P(-6, -30), P(-12, -30), P(-6, -4), P(-6, 4), P(-12, 30), P(-6, 30), P(8, 4)]
    stab = [P(-20, -3), P(-27, -12), P(-30, -12), P(-28, -3), P(-28, 3), P(-30, 12), P(-27, 12), P(-20, 3)]
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="27" fill="{C20["plane"]}" opacity="0.22"/>'
            + _path(wing, C20["plane"], "#10161b", 2.2) + _path(stab, C20["plane"], "#10161b", 2.0)
            + _path(body, C20["plane"], "#10161b", 2.2))


def s2_mark_svg(p, kind="sq"):
    x, y = P2(*p)
    if kind == "sq":
        return (f'<rect x="{x - 8:.1f}" y="{y - 8:.1f}" width="16" height="16" fill="{C20["hl"]}" stroke="#10161b" stroke-width="2.5"/>')
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{C20["hl"]}" stroke="#10161b" stroke-width="2.5"/>'


def s2_ring_svg(p, r=36.0):
    """強める輪（p＝画面の点）"""
    x, y = p
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="#10161b" stroke-width="10" opacity="0.6"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{C20["hl"]}" stroke-width="5"/>')


def s2_lines_svg(at):
    g = []
    for nm in ("haneda", "kumagaya"):
        x, y = P2(*S2_PTS[nm])
        g.append(f'<path d="M {x:.1f} {y:.1f} L {at[0]:.1f} {at[1]:.1f}" stroke="#10161b" stroke-width="8" opacity="0.6"/>'
                 f'<path d="M {x:.1f} {y:.1f} L {at[0]:.1f} {at[1]:.1f}" stroke="{C20["line2"]}" stroke-width="4" '
                 'stroke-dasharray="14 9"/>')
    return "".join(g)


def s2_nagoya_svg(at):
    nx, ny = P2(*S2_PTS["nagoya"])
    a = math.atan2(ny - at[1], nx - at[0])
    ex, ey = nx - 14 * math.cos(a), ny - 14 * math.sin(a)
    hx, hy = ex - 26 * math.cos(a), ey - 26 * math.sin(a)
    px, py = -math.sin(a) * 14, math.cos(a) * 14
    return (f'<path d="M {at[0]:.1f} {at[1]:.1f} L {hx:.1f} {hy:.1f}" stroke="#10161b" stroke-width="10" stroke-linecap="round" opacity="0.6"/>'
            f'<path d="M {at[0]:.1f} {at[1]:.1f} L {hx:.1f} {hy:.1f}" stroke="{C20["line2"]}" stroke-width="5" stroke-dasharray="16 10"/>'
            f'<path d="M {ex:.1f} {ey:.1f} L {hx + px:.1f} {hy + py:.1f} L {hx - px:.1f} {hy - py:.1f} Z" fill="{C20["line2"]}" '
            'stroke="#10161b" stroke-width="2"/>'
            f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="8" fill="{C20["hl"]}" stroke="#10161b" stroke-width="2.5"/>')


def s2_crash_svg():
    x, y = s2_route()["crash"]
    d = f"M {x - 12:.1f} {y - 12:.1f} L {x + 12:.1f} {y + 12:.1f} M {x + 12:.1f} {y - 12:.1f} L {x - 12:.1f} {y + 12:.1f}"
    return (f'<path d="{d}" stroke="#10161b" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{C20["hl"]}" stroke-width="5" stroke-linecap="round"/>')


def s2_boom_svg(c):
    return (f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="22" fill="none" stroke="#10161b" stroke-width="8" opacity="0.5"/>'
            f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="22" fill="none" stroke="{C20["hl"]}" stroke-width="4"/>')


def _first_on(start, states, f, v=None):
    for st in [start] + list(states):
        if (st[f] == v) if v else (st[f] != "off"):
            return st
    return None


def _scene_S2(start, states, steps):
    allst = [start] + states
    _head_only("S2", start, states, ("view", "switch"))
    R = S2_REC
    prev_s = -1.0
    for st in allst:
        s = s2_len(st["s2t"])
        if s < prev_s - 1e-6:
            raise ValueError("illu S2：時刻 s2t は進むだけ（戻さない）")
        prev_s = s
        if st["s2crash"] == "on" and st["s2t"] != "end":
            raise ValueError("illu S2：墜落地点の印（s2crash）は s2t＝\"end\"（墜落地点まで描いた段）だけ")
        if st["s2t"] == "end" and st["s2plane"] == "on":
            raise ValueError("illu S2：s2t＝\"end\" の段に機の印を置かない（墜落の瞬間を描かない）")
    total = s2_route()["total"]
    u = [s2_len(st["s2t"]) / total for st in allst]
    go = [dict(stage=0, delay=0.0, u=u[0])]
    for i, sp in enumerate(steps):
        if abs(u[i + 1] - u[i]) > 1e-9:
            go.append(dict(stage=i, delay=float(sp.get("delay", KEY_DELAY)), dur=float(sp.get("dur", S2_T["trace"])), u=u[i + 1]))
    A1 = [dict(stage=0, delay=0.0, a=1.0)]
    pts = [list(p) for p in s2_route()["pts"]]
    parts = [_part("map", s2_base_svg(), R["map"]), _part("names", s2_names_svg(), R["names"]),
             dict(_part("scale", s2_scale_svg(), R["map"]), geo=dict(kind="scale", km=S2_SCALE_KM, px=S2_SCALE_KM * S2_S))]
    if any(st["s2ring"] == "sagami" for st in allst):
        parts.append(_part("ring_sagami", s2_ring_svg(P2(*S2_PTS["sagami"]), 70.0), R["sagami"],
                           keys=_akeys(start, states, steps, lambda st: st["s2ring"] == "sagami", S2_T["ring"])))
    parts.append(dict(_part("trail", s2_trail_svg(), R["trace"]), kind="draw", path=pts, go=go, keys=A1, reveal=16,
                      geo=dict(kind="trail", proj=dict(px=list(S2_PX), c=list(S2_C), kx=S2_KX, ky=S2_KY, s=S2_S, lat0=S2_LAT0))))
    for nm, kind in (("yokota", "sq"), ("kumagaya", "dot")):
        f = "s2yok" if nm == "yokota" else "s2kum"
        if any(st[f] == "on" for st in allst):
            parts.append(dict(_part(nm, s2_mark_svg(S2_PTS[nm], kind), R[nm], keys=_akeys(start, states, steps, lambda st, f=f: st[f] == "on")),
                              geo=dict(kind="pt", name=nm, xy=list(P2(*S2_PTS[nm])))))
    st_l = _first_on(start, states, "s2lines", "on")
    if st_l:
        at = s2_pos(st_l["s2t"])
        parts.append(dict(_part("lines", s2_lines_svg(at), R["kumagaya"],
                                keys=_akeys(start, states, steps, lambda st: st["s2lines"] == "on", S2_T["show"])),
                          geo=dict(kind="lines", at=list(at), t=st_l["s2t"],
                                   frm=[list(P2(*S2_PTS["haneda"])), list(P2(*S2_PTS["kumagaya"]))])))
    st_n = _first_on(start, states, "s2ngo", "on")
    if st_n:
        at = s2_pos(st_n["s2t"])
        parts.append(dict(_part("nagoya", s2_nagoya_svg(at), R["nagoya"],
                                keys=_akeys(start, states, steps, lambda st: st["s2ngo"] == "on", S2_T["show"])),
                          geo=dict(kind="nagoya", at=list(at), to=list(P2(*S2_PTS["nagoya"])), t=st_n["s2t"])))
    for nm in ("haneda", "yokota"):
        if any(st["s2ring"] in (nm, "both") for st in allst):
            parts.append(_part("ring_" + nm, s2_ring_svg(P2(*S2_PTS[nm])), R["yokota"],
                               keys=_akeys(start, states, steps, lambda st, nm=nm: st["s2ring"] in (nm, "both"), S2_T["ring"])))
    if any(st["s2crash"] == "on" for st in allst):
        parts.append(dict(_part("crash", s2_crash_svg(), R["crash"], keys=_akeys(start, states, steps, lambda st: st["s2crash"] == "on")),
                          geo=dict(kind="crash", xy=list(s2_route()["crash"]))))
    # 出来事 rings＝その段の機の位置の音の輪（c209 の「ドーン」）
    for i, (st, sp) in enumerate(zip(states, steps)):
        if sp.get("rings"):
            c = s2_pos(st["s2t"])
            parts += IL._pulse_part(f"boom{i}", s2_boom_svg(c), R["boom"], c, states, [s if j == i else {} for j, s in enumerate(steps)],
                                    "rings", "out")
    if any(st["s2plane"] == "on" for st in allst):
        parts.append(dict(_part("plane", s2_plane_svg(), R["plane"]), kind="mover", path=pts, go=go,
                          keys=_akeys(start, states, steps, lambda st: st["s2plane"] == "on", 0.4), anchor=list(S2_MK),
                          geo=dict(kind="plane", t=[st["s2t"] for st in allst])))
    if start["switch"] == "on":
        parts.append(_switch_part("上から見ると"))
    return parts


def _s2_anchors(st):
    a = {k: P2(*v) for k, v in S2_PTS.items()}
    a["plane"] = s2_pos(st["s2t"]) if st["s2t"] != "end" else s2_route()["crash"]
    a["crash"] = s2_route()["crash"]
    a["boom"] = s2_pos("18:24:35")
    a["okutama"] = s2_pos("18:48:03")
    nx, ny = P2(*S2_PTS["nagoya"])
    if st["s2ngo"] == "on":
        p = s2_pos(st["s2t"])
        a["nagoya_mid"] = ((p[0] + nx) / 2, (p[1] + ny) / 2)
    return a


def _s2_mend(st0, states, steps):
    """⑤b-3 の試し焼き（c209）：時計の札が段の頭（0.35秒）から出て、機の印がまだ進んでいるうちに先の点を指した＝時刻が進む段は
    動きが終わってから札を出す（illu.scene の札の出る秒＝15本目 RB と同じ仕組み）"""
    out, prev = {}, st0
    for i, (st, sp) in enumerate(zip(states, steps)):
        if st["s2t"] != prev["s2t"]:
            out[i] = float(sp.get("delay", KEY_DELAY)) + float(sp.get("dur", S2_T["trace"]))
        prev = st
    return out


def _s2_note(st0, states):
    return "海岸線は Natural Earth・経路と時刻の点は付図-1 から（位置は目安）・機の印は拡大"


# ══════════════════════════════════════════════════════════
#  S3 2つの揺れの模式（記録のグラフではない）
# ══════════════════════════════════════════════════════════
S3_PITCH, S3_ROLL = 15.0, 40.0              # 3.2.6.2 p.113（縦揺れ角±約15度）・p.114（横揺れ角±約40度）
S3_WAVE = dict(side=dict(x0=1790.0, x1=150.0, yc=500.0, lam=1400.0, ph=0.25),
               both=dict(x0=900.0, x1=110.0, yc=520.0, lam=700.0, ph=0.25))
# ⑤b-3 の試し焼き（c305）：k 8.5 では翼・尾翼・水平尾翼が細い線ばかりで機に見えにくかった＝大きく（翼の幅 約660画素）・翼と尾翼を厚く
S3_FRONT = dict(front=dict(c=(960.0, 520.0), k=11.0), both=dict(c=(1420.0, 500.0), k=7.0))
S3_T = dict(go=3.4, show=0.6, swing=1.55)
S3_REC = dict(
    sky="報告書 p6（顕著なフゴイド及びダッチロール運動が励起され）",
    wave="報告書 p113（フゴイド運動が縦揺れ角±約15度、垂直加速度±約0.3G、速度変化約100ノット、高度変化約4,000フィートにも及んだ場合もあった）",
    roll="報告書 p114（ダッチロール運動は…横揺れ角±約40度、横方向加速度±約0.5Gという激しい場合もあった）",
    body="報告書 p140（付図-4 三面図）")


def s3_amp(lam):
    """機首の上げの最大＝道の傾きの最大が 15度 になる波の高さ（道の傾き＝本当の角度のまま）"""
    return math.tan(math.radians(S3_PITCH)) * lam / (2.0 * math.pi)


def s3_wave_pts(view):
    w = S3_WAVE[view]
    A = s3_amp(w["lam"])
    n = int(abs(w["x1"] - w["x0"]) / 6)
    return [(w["x0"] + (w["x1"] - w["x0"]) * i / n,
             w["yc"] - A * math.sin(2 * math.pi * ((w["x0"] + (w["x1"] - w["x0"]) * i / n - w["x0"]) / w["lam"] + w["ph"])))
            for i in range(n + 1)]


def _side_icon(c, k, nose_left=True):
    """横から見た機の小さな形（S1 の輪郭を縮めたもの・機首が左）。c＝真ん中・k＝1メートルの画素"""
    s = -1.0 if not nose_left else 1.0

    def Q(x, z):
        return (c[0] + s * (x - S1_LEN / 2) * k, c[1] - z * k)
    up = IL._smooth(S1_UP, per=4)
    lo = IL._smooth(S1_LO, per=4)
    body = [Q(*p) for p in up] + [Q(*p) for p in reversed(lo)]
    return (_path([Q(*p) for p in S1_FIN], C20["fin"], C20["body_ln"], 1.6) + _path(body, C20["body"], C20["body_ln"], 1.8)
            + _path([Q(*p) for p in S1_WING], C20["wing"], C20["body_ln"], 1.4))


def _front_icon(c, k):
    """正面から見た機（付図-4 の正面の図＝翼の幅 195 FT 8 IN・エンジン 内側 12.07m・外側 21.15m の見え方）＝回す中心 c"""
    cx, cy = c
    span = 59.64 / 2
    dih = math.tan(math.radians(7.0))

    def Q(y, z):
        return (cx + y * k, cy - z * k)
    g = [_path([Q(-11.1, 3.5), Q(-0.6, 3.1), Q(-0.6, 4.0), Q(-11.1, 4.3)], C20["stab"], C20["body_ln"], 2.0, op=0.85),
         _path([Q(11.1, 3.5), Q(0.6, 3.1), Q(0.6, 4.0), Q(11.1, 4.3)], C20["stab"], C20["body_ln"], 2.0, op=0.85),
         _path([Q(-0.75, 2.8), Q(-0.35, 14.6), Q(0.35, 14.6), Q(0.75, 2.8)], C20["fin"], C20["body_ln"], 2.2)]
    for sg in (-1, 1):
        g.append(_path([Q(sg * 2.6, -1.3), Q(sg * span, -1.6 + span * dih + 0.45), Q(sg * span, -1.6 + span * dih - 0.25),
                        Q(sg * 2.6, -2.8)], C20["wing"], C20["body_ln"], 2.2))
        for y, dz in ((12.07, 2.53), (21.15, 0.94)):
            zc = -1.6 + y * dih - dz
            g.append(f'<circle cx="{Q(sg * y, 0)[0]:.1f}" cy="{Q(0, zc)[1]:.1f}" r="{1.3 * k:.1f}" fill="{C20["eng"]}" '
                     f'stroke="{C20["body_ln"]}" stroke-width="1.6"/><circle cx="{Q(sg * y, 0)[0]:.1f}" cy="{Q(0, zc)[1]:.1f}" '
                     f'r="{0.75 * k:.1f}" fill="{C20["eng_dk"]}"/>')
    g.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{3.25 * k:.1f}" ry="{3.4 * k:.1f}" fill="{C20["body"]}" '
             f'stroke="{C20["body_ln"]}" stroke-width="2"/>')
    g.append(f'<ellipse cx="{cx:.1f}" cy="{cy - 1.4 * k:.1f}" rx="{1.6 * k:.1f}" ry="{0.55 * k:.1f}" fill="{C20["win"]}"/>')
    return "".join(g)


def s3_wave_svg(view):
    d = _d(s3_wave_pts(view), False)
    return (f'<path d="{d}" fill="none" stroke="#10161b" stroke-width="7" opacity="0.45"/>'
            f'<path d="{d}" fill="none" stroke="{C20["route"]}" stroke-width="3" stroke-dasharray="12 10"/>')


def _s3_peak(view, which):
    """波の頂（which＝top）・谷（bottom）・上りの傾きが一番の所（climb＝左へ進みながら上がる）の x, y"""
    w = S3_WAVE[view]
    A = s3_amp(w["lam"])
    phase = {"top": 0.25, "bottom": 0.75, "climb": 0.5}[which]
    # y＝yc − A·sin(2πφ)・φ＝(x−x0)/λ＋ph。頂＝φ 1/4・谷＝3/4。左へ進む（x が減る）＝φ が減る＝上り（y が減る）は cos(2πφ)＜0 の所・
    #   傾きが一番の所は φ＝1/2。候補 x＝x0＋(φ−ph＋m)·λ のうち、道の端から 60画素より内で、進む向きに最初に来るもの
    lo, hi = min(w["x0"], w["x1"]) + 60, max(w["x0"], w["x1"]) - 60
    xs = [w["x0"] + (phase - w["ph"] + m) * w["lam"] for m in range(-8, 9)]
    xs = [x for x in xs if lo <= x <= hi]
    if not xs:
        raise ValueError("illu S3：波の中に頂・谷が無い")
    x = max(xs) if w["x1"] < w["x0"] else min(xs)
    return x, w["yc"] - A * math.sin(2 * math.pi * ((x - w["x0"]) / w["lam"] + w["ph"]))


def s3_amp_svg(view):
    """高さの差のかっこ（頂と谷の高さ＝波の本当の高さ）"""
    w = S3_WAVE[view]
    A = s3_amp(w["lam"])
    yt, yb = w["yc"] - A, w["yc"] + A
    # ⑤b-3 の組み立て：頂と谷は半波長（700画素）離れる＝引き出し線が長く波を横切った＝頂と谷の高さに横の点線を引き、かっこは右の端へ
    xl, xr = min(w["x0"], w["x1"]), max(w["x0"], w["x1"])
    bx = xr + 12
    g = []
    for y in (yt, yb):
        g.append(f'<path d="M {xl:.1f} {y:.1f} L {bx:.1f} {y:.1f}" stroke="{C20["line2"]}" stroke-width="2.5" stroke-dasharray="6 7" '
                 'opacity="0.8"/>')
    g.append(f'<path d="M {bx - 12:.1f} {yt:.1f} L {bx:.1f} {yt:.1f} L {bx:.1f} {yb:.1f} L {bx - 12:.1f} {yb:.1f}" fill="none" '
             f'stroke="#10161b" stroke-width="8"/><path d="M {bx - 12:.1f} {yt:.1f} L {bx:.1f} {yt:.1f} L {bx:.1f} {yb:.1f} '
             f'L {bx - 12:.1f} {yb:.1f}" fill="none" stroke="{C20["hl"]}" stroke-width="4"/>')
    return "".join(g), (bx, yt, yb)


def s3_pitch_svg(view):
    """機首の上げの角の印（上りの傾きが一番の所に、15度 上げた機の影と水平の線と弧）"""
    x, y = _s3_peak(view, "climb")
    k = 2.6 if view == "side" else 1.6
    r = 120.0 if view == "side" else 70.0
    a = math.radians(S3_PITCH)
    ghost = (f'<g transform="rotate({S3_PITCH:.1f} {x:.1f} {y:.1f})" opacity="0.55">{_side_icon((x, y), k)}</g>')
    return (ghost
            + f'<path d="M {x:.1f} {y:.1f} L {x - r - 40:.1f} {y:.1f}" stroke="{C20["line2"]}" stroke-width="2.5" stroke-dasharray="8 6"/>'
            + f'<path d="M {x:.1f} {y:.1f} L {x - (r + 40) * math.cos(a):.1f} {y - (r + 40) * math.sin(a):.1f}" '
              f'stroke="{C20["line2"]}" stroke-width="2.5"/>'
            + f'<path d="M {x - r:.1f} {y:.1f} A {r:.1f} {r:.1f} 0 0 1 {x - r * math.cos(a):.1f} {y - r * math.sin(a):.1f}" '
              f'fill="none" stroke="{C20["hl"]}" stroke-width="5"/>'), (x, y)


def s3_roll_arc_svg(view):
    c, k = S3_FRONT[view]["c"], S3_FRONT[view]["k"]
    r = 14.6 * k + 26
    g = []
    for sg in (-1, 1):
        a = math.radians(90 + sg * S3_ROLL)
        x, y = c[0] + r * math.cos(a), c[1] - r * math.sin(a)
        g.append(f'<path d="M {c[0]:.1f} {c[1]:.1f} L {x:.1f} {y:.1f}" stroke="{C20["line2"]}" stroke-width="2.5" stroke-dasharray="8 6"/>')
    a0, a1 = math.radians(90 - S3_ROLL), math.radians(90 + S3_ROLL)
    g.append(f'<path d="M {c[0] + r * math.cos(a0):.1f} {c[1] - r * math.sin(a0):.1f} A {r:.1f} {r:.1f} 0 0 0 '
             f'{c[0] + r * math.cos(a1):.1f} {c[1] - r * math.sin(a1):.1f}" fill="none" stroke="{C20["hl"]}" stroke-width="5"/>')
    g.append(f'<path d="M {c[0]:.1f} {c[1]:.1f} L {c[0]:.1f} {c[1] - r - 20:.1f}" stroke="{C20["line2"]}" stroke-width="2" opacity="0.7"/>')
    return "".join(g)


def _roll_keys(n_sec):
    """左右に約40度＝鍵はカットの頭（段0）から時間の順に（段をまたいでも戻らない）"""
    ks = [dict(stage=0, delay=0.0, rot=0.0)]
    t, sg = 0.35, -1.0
    while t < n_sec:
        ks.append(dict(stage=0, delay=t, dur=S3_T["swing"], rot=sg * S3_ROLL))
        t += S3_T["swing"]
        sg = -sg
    return ks


def _scene_S3(start, states, steps):
    allst = [start] + states
    _head_only("S3", start, states, ("view", "s3roll", "switch"))
    v = start["view"]
    R = S3_REC
    parts = [_part("sky", _sky_svg("s3Sky") + _clouds_svg(860.0, 5), R["sky"])]
    if v == "both":
        # ⑤b-3 の試し焼き（c410）：名札を y 860 に置くと左下の出典の行（y 876）と重なった＝上へ
        parts.append(_part("labels", _text(505, 760, "フゴイド（横から）", 30) + _text(1420, 760, "ダッチロール（正面から）", 30)
                           + f'<path d="M 960 240 L 960 720" stroke="{C20["route"]}" stroke-width="2" opacity="0.35"/>', R["sky"]))
    if v in ("side", "both"):
        wv = s3_wave_pts(v)
        parts.append(dict(_part("wave", s3_wave_svg(v), R["wave"], keys=_akeys(start, states, steps, lambda st: st["s3wave"] == "on")),
                          geo=dict(kind="wave", lam=S3_WAVE[v]["lam"], amp=s3_amp(S3_WAVE[v]["lam"]))))
        if any(st["s3amp"] == "on" for st in allst):
            svg, (bx, yt, yb) = s3_amp_svg(v)
            parts.append(dict(_part("amp", svg, R["wave"], keys=_akeys(start, states, steps, lambda st: st["s3amp"] == "on")),
                              geo=dict(kind="amp", px=yb - yt, wave_px=2 * s3_amp(S3_WAVE[v]["lam"]))))
        if any(st["s3pitch"] == "on" for st in allst):
            svg, _xy = s3_pitch_svg(v)
            parts.append(dict(_part("pitch", svg, R["wave"], keys=_akeys(start, states, steps, lambda st: st["s3pitch"] == "on")),
                              geo=dict(kind="pitch", deg=S3_PITCH)))
        # 機の印＝波の道を進む（左へ）。道の傾き＝機首の上げ下げ（mover が道の向きに回す・機首が左の形に 180度を足す）
        n = max(1, len(steps))
        go = [dict(stage=0, delay=0.0, u=0.0)]
        for i, (st, sp) in enumerate(zip(states, steps)):
            if st["s3wave"] == "on":
                go.append(dict(stage=i, delay=float(sp.get("delay", KEY_DELAY)), dur=float(sp.get("dur", S3_T["go"])), u=(i + 1) / n))
        k = 2.6 if v == "side" else 1.6
        parts.append(dict(_part("craft", _side_icon((960.0, 540.0), k), R["body"]), kind="mover", path=[list(p) for p in wv], go=go,
                          keys=_akeys(start, states, steps, lambda st: st["s3wave"] == "on", 0.4), anchor=[960.0, 540.0], rot0=180.0,
                          geo=dict(kind="craft")))
    if v in ("front", "both"):
        c, k = S3_FRONT[v]["c"], S3_FRONT[v]["k"]
        parts.append(dict(_part("arc", s3_roll_arc_svg(v), R["roll"]), geo=dict(kind="arc", deg=S3_ROLL)))
        keys = _roll_keys(30.0) if start["s3roll"] == "on" else [dict(stage=0, delay=0.0, rot=0.0)]
        parts.append(dict(_part("front", _front_icon(c, k), R["body"], c, keys), geo=dict(kind="front")))
    if start["switch"] == "on":
        parts.append(_switch_part("横から見ると" if v == "side" else "正面から見ると"))
    return parts


def _s3_anchors(st):
    v = st["view"]
    a = {}
    if v in ("side", "both"):
        a["top"] = _s3_peak(v, "top")
        a["bottom"] = _s3_peak(v, "bottom")
        a["climb"] = _s3_peak(v, "climb")
        a["amp"] = (max(S3_WAVE[v]["x0"], S3_WAVE[v]["x1"]) + 12, S3_WAVE[v]["yc"])
        a["wave"] = (S3_WAVE[v]["x0"] - 200, S3_WAVE[v]["yc"])
    if v in ("front", "both"):
        c, k = S3_FRONT[v]["c"], S3_FRONT[v]["k"]
        r = 14.6 * k + 26
        a["arc"] = (c[0] + r * math.cos(math.radians(90 - S3_ROLL)), c[1] - r * math.sin(math.radians(90 - S3_ROLL)))
        a["front"] = c
    return a


def _s3_note(st0, states):
    return "形と動きは模式（記録のグラフではない）・角の大きさは報告書の値"


# ══════════════════════════════════════════════════════════
#  型の表へ登録（illu.py の末尾から読まれる）
# ══════════════════════════════════════════════════════════
def register():
    IL.FIELDS.update(
        S1=dict(view="side", s1cab="off", s1ck="off", s1mask="off", s1press="off", s1bulk="off", s1ring="off", s1fin="on",
                switch="off", cam=1.0),
        S2=dict(view="top", s2t=S2_T0, s2plane="on", s2yok="off", s2kum="off", s2lines="off", s2ngo="off", s2ring="off",
                s2crash="off", switch="off", cam=1.0),
        S3=dict(view="side", s3wave="off", s3amp="off", s3pitch="off", s3roll="off", switch="off", cam=1.0))
    IL.CHOICES.update(s1cab=IL.ONOFF, s1ck=IL.ONOFF, s1mask=("off", "drop"), s1press=IL.ONOFF, s1bulk=IL.ONOFF,
                      s1ring=("off", "cockpit", "tail"), s1fin=("on", "lost"),
                      s2plane=IL.ONOFF, s2yok=IL.ONOFF, s2kum=IL.ONOFF, s2lines=IL.ONOFF, s2ngo=IL.ONOFF,
                      s2ring=("off", "haneda", "yokota", "both", "sagami"), s2crash=IL.ONOFF,
                      s3wave=IL.ONOFF, s3amp=IL.ONOFF, s3pitch=IL.ONOFF, s3roll=IL.ONOFF)
    IL.VIEWS.update(S1=("side",), S2=("top",), S3=("side", "front", "both"))
    IL.REC_FIELDS = IL.REC_FIELDS + ("s1mask", "s1press", "s1bulk", "s1fin", "s2t", "s2yok", "s2kum", "s2lines", "s2ngo", "s2crash",
                                     "s3wave", "s3amp", "s3pitch", "s3roll")
    IL.NOTE.update(S1=_s1_note, S2=_s2_note, S3=_s3_note)
    IL.EXTRA.update(
        S1=dict(scene=_scene_S1, anchors=_s1_anchors, camc=lambda st0, states: (960.0, 540.0), label=lambda st0, states: LAB["S1"]),
        S2=dict(scene=_scene_S2, anchors=_s2_anchors, camc=lambda st0, states: (960.0, 500.0), label=lambda st0, states: LAB["S2"],
                mpp=1000.0 / S2_S, mend=_s2_mend),
        S3=dict(scene=_scene_S3, anchors=_s3_anchors, camc=lambda st0, states: (960.0, 520.0),
                label=lambda st0, states: LAB["S3"][st0["view"]]))


register()
