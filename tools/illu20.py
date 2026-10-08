# -*- coding: utf-8 -*-
"""illu20.py — 案C の再現イラスト：20本目（日本航空123便・JA8119・1985-08-12）の置き場 S1・S2・S3（⑤b-3・2026-10-08 新設）・
S4・S5・S6・S7（⑤b-4・同日。欄と記録は各節の頭の注・門番 check_illu ㉗㉘㉙㉚）。

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
    name="#e8eef1", hl="#f2c14e", line2="#f6d77a",
    # 🆕 ⑤b-4（S4〜S7）
    night0="#0d1626", night1="#1a2a40", ngrid="#9fb4c8", peak="#cfd6dc", morn="#8fd3e8", glow="#fff3d6", smoke="#d9dee3",
    dawn0="#6b8db3", dawn1="#2f4766", air="#e9f6ff", crack="#e4572e", hyd="#c9a0ff", act="#8a96a0", web_up="#c8cfd6",
    web_lo="#a9c4d9", splice="#f2c14e", filler="#e58f5a", rivet="#56616b", drop="#e4572e", cur="#7fd0f0", deb="#f2c14e",
    area="#f6d77a", panel="#101820")
LAB = dict(S1="横から見た図", S2="上から見た図（北が上）", S3=dict(side="横から見た模式", front="正面から見た模式",
                                                                both="2つの揺れの模式（横から・正面から）"),
           S4="上から見た図（北が上）", S5=dict(tail="横から見た図（尾部を拡大）", all="横から見た図"),
           S6=dict(front="正面から見た図（後ろから隔壁を見る）", side="横から見た継ぎ目の断面", both="横から見た継ぎ目の断面（左右に並べる）"),
           S7="上から見た図（北が上）")


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
#  S4 夜の地図（上から・北が上）＝墜落地点のまわり 🆕 ⑤b-4
# ══════════════════════════════════════════════════════════
# 点と山の位置＝解説 図13（p.20）を墜落地点からの東西・南北（km）で読んだ `ref/ep20/night20.json`（`night20.py`）。
# ⚠️ 図13 の下の地形図は今の地図（2005 年の奥三川湖が写る）＝地形・川・湖は描かない（夜の地の色と 1km の方眼だけ）
# ⑤b-4 に決めた：S2 の地図の型（P2・海岸線）は使い回さない＝点のずれは 0.7〜6km（S2 の 1画素≒217m では 3〜28画素）・
#   この範囲に海岸は無い。平らにし方（東西＝cos(緯度)）だけ同じ
S4_K = 80.0                       # 1km＝80画素（1画素＝12.5m）
S4_C = (900.0, 430.0)             # 墜落地点の画面の位置
S4_WIT = (202.5, 3.0, 4.0)        # 目撃者の位置＝墜落地点から南南西・3〜4km（報告書 p.7）
S4_YOK = (139.348, 35.749)        # 横田飛行場（S2 と同じ点）
S4_RINGS = (2.0, 4.0, 6.0)        # ずれの輪（km）＝表3 の誤差 2〜6km の目盛り
S4_SCALE_KM = 2.0
S4_T = dict(show=0.6, glow=1.0, dawn=2.4)
S4_REC = dict(
    map="解説 p1020（図13 航空機による墜落場所の特定図）",
    crash="報告書 p8（北緯35度59分54秒、東経138度41分49秒）",
    peaks="解説 p1020（図13 の三国山・三国峠・扇平山）",
    wit="報告書 p7（墜落地点の南南西3〜4キロメートルの地点での目撃者（4名））",
    glow="報告書 p8（同機が隠れた山陰から白煙と閃光が見えた）",
    pts="解説 p1019（表3 各航空機の測位結果）・p1020（図13）",
    yok="報告書 p25（横田TACANから305度、35海里の地点に火災を発見）",
    ring="解説 p1019（表3 の誤差＝3km・6km・4km・2km）",
    dawn="解説 p1019（表3 日出 13日04:55）")


@lru_cache(maxsize=1)
def s4_data():
    return json.loads((REF / "night20.json").read_text(encoding="utf-8"))


def P4(e, n):
    """墜落地点からの東（km）・北（km）→ 画面"""
    return (S4_C[0] + e * S4_K, S4_C[1] - n * S4_K)


def s4_pt(n):
    return P4(*next(p for p in s4_data()["points"] if p["n"] == n)["km"])


def s4_peak(k):
    return P4(*s4_data()["peaks"][k]["km"])


def s4_wit():
    b, r0, r1 = S4_WIT
    s, c = math.sin(math.radians(b)), math.cos(math.radians(b))
    return P4(r0 * s, r0 * c), P4(r1 * s, r1 * c)


def s4_yok_dir():
    """① の点から横田飛行場への向き（画面の単位ベクトル）と距離（km）"""
    d = s4_data()
    cx, cy = d["crash"]
    e = (S4_YOK[0] - cx) * math.cos(math.radians(cy)) * 111.32
    n = (S4_YOK[1] - cy) * 110.57
    p1 = next(p for p in d["points"] if p["n"] == 1)["km"]
    de, dn = e - p1[0], n - p1[1]
    L = math.hypot(de, dn)
    return (de / L, -dn / L), L


def s4_yok_end():
    (ux, uy), _L = s4_yok_dir()
    x, y = s4_pt(1)
    t = (1830.0 - x) / ux
    return (x + ux * t, y + uy * t)


def s4_base_svg():
    g = [f'<defs><linearGradient id="s4N" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C20["night0"]}"/>'
         f'<stop offset="1" stop-color="{C20["night1"]}"/></linearGradient></defs>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#s4N)"/>']
    for k in range(-13, 14):
        x = S4_C[0] + k * S4_K
        if 0 <= x <= W:
            g.append(f'<path d="M {x:.1f} 0 L {x:.1f} {H}" stroke="{C20["ngrid"]}" stroke-width="1.2" opacity="0.10"/>')
    for k in range(-8, 9):
        y = S4_C[1] + k * S4_K
        if 0 <= y <= H:
            g.append(f'<path d="M 0 {y:.1f} L {W} {y:.1f}" stroke="{C20["ngrid"]}" stroke-width="1.2" opacity="0.10"/>')
    return "".join(g)


def s4_peaks_svg():
    g = []
    for k, filled, (dx, dy, anc) in (("mikuni", True, (22, 9, "start")), ("touge", False, (22, 9, "start")),
                                     ("ougi", True, (-20, 40, "end"))):
        x, y = s4_peak(k)
        tri = [(x, y - 13), (x + 12, y + 8), (x - 12, y + 8)]
        g.append(_path(tri, C20["peak"] if filled else "none", "#10161b" if filled else C20["peak"], 2.5 if filled else 3.0))
        g.append(_text(x + dx, y + dy, s4_data()["peaks"][k]["name"], 24, anchor=anc))
    return "".join(g)


def s4_crash_svg():
    x, y = S4_C
    d = f"M {x - 13:.1f} {y - 13:.1f} L {x + 13:.1f} {y + 13:.1f} M {x + 13:.1f} {y - 13:.1f} L {x - 13:.1f} {y + 13:.1f}"
    return (f'<path d="{d}" stroke="#10161b" stroke-width="11" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{C20["crack"]}" stroke-width="5.5" stroke-linecap="round"/>'
            + _text(x - 24, y + 9, "墜落地点", 26, anchor="end"))


def s4_wit_svg():
    a, b = s4_wit()
    return (f'<path d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}" stroke="#10161b" stroke-width="30" stroke-linecap="round" '
            f'opacity="0.55"/><path d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}" stroke="{C20["morn"]}" stroke-width="22" '
            f'stroke-linecap="round" opacity="0.55"/>' + _text(b[0] + 30, b[1] + 14, "目撃した4人", 26, anchor="start"))


def s4_glow_svg():
    x, y = S4_C
    return (f'<defs><radialGradient id="s4G"><stop offset="0" stop-color="{C20["glow"]}" stop-opacity="0.95"/>'
            f'<stop offset="1" stop-color="{C20["glow"]}" stop-opacity="0"/></radialGradient></defs>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="70" fill="url(#s4G)"/>'
            + "".join(f'<ellipse cx="{x + dx:.1f}" cy="{y + dy:.1f}" rx="{rx}" ry="{ry}" fill="{C20["smoke"]}" opacity="0.30"/>'
                      for dx, dy, rx, ry in ((-8, -62, 30, 18), (10, -98, 38, 20), (-4, -138, 46, 22))))


def s4_point_svg(n, night):
    x, y = s4_pt(n)
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{C20["hl"] if night else C20["morn"]}" stroke="#10161b" '
            'stroke-width="3"/>')


def s4_rings_svg():
    g = []
    x, y = S4_C
    for km in S4_RINGS:
        r = km * S4_K
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="#10161b" stroke-width="7" opacity="0.5"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{C20["line2"]}" stroke-width="3" '
                 'stroke-dasharray="14 10" opacity="0.9"/>')
        a = math.radians(20.0)
        g.append(_text(x + r * math.cos(a) + 8, y - r * math.sin(a) - 6, f"{km:.0f}キロ", 24, col=C20["line2"], anchor="start"))
    return "".join(g)


def s4_yok_svg():
    x0, y0 = s4_pt(1)
    x1, y1 = s4_yok_end()
    (ux, uy), _L = s4_yok_dir()
    hx, hy = x1 - 26 * ux, y1 - 26 * uy
    px, py = -uy * 13, ux * 13
    return (f'<path d="M {x0:.1f} {y0:.1f} L {hx:.1f} {hy:.1f}" stroke="#10161b" stroke-width="9" opacity="0.6"/>'
            f'<path d="M {x0:.1f} {y0:.1f} L {hx:.1f} {hy:.1f}" stroke="{C20["line2"]}" stroke-width="4" stroke-dasharray="16 10"/>'
            f'<path d="M {x1:.1f} {y1:.1f} L {hx + px:.1f} {hy + py:.1f} L {hx - px:.1f} {hy - py:.1f} Z" fill="{C20["line2"]}" '
            'stroke="#10161b" stroke-width="2"/>' + _text(x1 - 6, y1 + 46, "横田へ", 26, anchor="end"))


def s4_dawn_svg():
    return (f'<defs><linearGradient id="s4D" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C20["dawn0"]}"/>'
            f'<stop offset="1" stop-color="{C20["dawn1"]}"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#s4D)" opacity="0.55"/>')


def s4_scale_svg():
    L = S4_SCALE_KM * S4_K
    x1, y = 1790.0, 846.0
    x0 = x1 - L
    d = f"M {x0:.1f} {y - 8:.1f} L {x0:.1f} {y:.1f} L {x1:.1f} {y:.1f} L {x1:.1f} {y - 8:.1f}"
    return (f'<path d="{d}" fill="none" stroke="#10161b" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{C20["name"]}" stroke-width="3" stroke-linejoin="round"/>'
            + _text((x0 + x1) / 2, y - 16, f"{S4_SCALE_KM:.0f}キロ", 24))


def _scene_S4(start, states, steps):
    allst = [start] + states
    _head_only("S4", start, states, ("view", "switch"))
    R = S4_REC
    for a, b in zip(allst, allst[1:]):
        if int(b["s4n"]) < int(a["s4n"]) or int(b["s4m"]) < int(a["s4m"]):
            raise ValueError("illu S4：点の数（s4n・s4m）は増えるだけ（時刻の順に出す）")
    parts = [_part("base", s4_base_svg(), R["map"])]
    if any(st["s4dawn"] == "on" for st in allst):
        parts.append(_part("dawn", s4_dawn_svg(), R["dawn"], keys=_akeys(start, states, steps, lambda st: st["s4dawn"] == "on",
                                                                          S4_T["dawn"])))
    parts.append(dict(_part("scale", s4_scale_svg(), R["map"]), geo=dict(kind="scale", km=S4_SCALE_KM, px=S4_SCALE_KM * S4_K)))
    parts.append(dict(_part("peaks", s4_peaks_svg(), R["peaks"]),
                      geo=dict(kind="s4peaks", c=list(S4_C), k=S4_K, xy={k: list(s4_peak(k)) for k in ("mikuni", "touge", "ougi")})))
    if any(st["s4ring"] == "on" for st in allst):
        parts.append(dict(_part("rings", s4_rings_svg(), R["ring"], keys=_akeys(start, states, steps, lambda st: st["s4ring"] == "on")),
                          geo=dict(kind="s4ring", c=list(S4_C), km=list(S4_RINGS), r=[km * S4_K for km in S4_RINGS])))
    if any(st["s4glow"] == "on" for st in allst):
        parts.append(_part("glow", s4_glow_svg(), R["glow"], keys=_akeys(start, states, steps, lambda st: st["s4glow"] == "on",
                                                                          S4_T["glow"])))
    parts.append(dict(_part("crash", s4_crash_svg(), R["crash"]), geo=dict(kind="s4crash", xy=list(S4_C), k=S4_K)))
    if any(st["s4wit"] == "on" for st in allst):
        a, b = s4_wit()
        parts.append(dict(_part("wit", s4_wit_svg(), R["wit"], keys=_akeys(start, states, steps, lambda st: st["s4wit"] == "on")),
                          geo=dict(kind="s4wit", a=list(a), b=list(b))))
    if any(st["s4yok"] == "on" for st in allst):
        parts.append(dict(_part("yok", s4_yok_svg(), R["yok"], keys=_akeys(start, states, steps, lambda st: st["s4yok"] == "on")),
                          geo=dict(kind="s4yok", frm=list(s4_pt(1)), to=list(s4_yok_end()))))
    for p in s4_data()["points"]:
        n, night = p["n"], p["night"]
        f, m = ("s4n", n) if night else ("s4m", n - 4)
        if any(int(st[f]) >= m for st in allst):
            parts.append(dict(_part(f"pt{n}", s4_point_svg(n, night), R["pts"],
                                    keys=_akeys(start, states, steps, lambda st, f=f, m=m: int(st[f]) >= m, S4_T["show"])),
                              geo=dict(kind="s4pt", n=n, t=p["t"], xy=list(s4_pt(n)))))
    if start["switch"] == "on":
        parts.append(_switch_part("上から見ると"))
    return parts


def _s4_anchors(st):
    a, b = s4_wit()
    an = dict(crash=S4_C, wit=((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), mikuni=s4_peak("mikuni"), ougi=s4_peak("ougi"),
              touge=s4_peak("touge"), yok=s4_yok_end())
    for p in s4_data()["points"]:
        an[f"p{p['n']}"] = s4_pt(p["n"])
    x0, y0 = s4_pt(1)
    (ux, uy), _L = s4_yok_dir()
    an["yok_mid"] = (x0 + ux * 420, y0 + uy * 420)
    return an


def _s4_note(st0, states):
    return "点と山の位置は解説の図13 から・地形は描かない・人は描かない"


# ══════════════════════════════════════════════════════════
#  S5 尾部が壊れていく推定（横から・機首が左）🆕 ⑤b-4
# ══════════════════════════════════════════════════════════
# 形は S1 と同じ（付図-4 の三面図・胴体の番地 BS）。frame＝tail（尾部を拡大＝1m 38画素・x 46m が 480画素）／all（機全体＝S1 と同じ）。
#   後部圧力隔壁＝BS2360（p.29）・APU 防火壁＝BS2658（p.9・p.29「BS2658（APU防火壁の取付部）」）・方向舵＝上と下の2枚（表5・付図-7）・
#   油圧の配管＝4系統（p.112・p.126）。🔴 起きた順と形は報告書 4.1.6 の「推定」＝全部の段に「推定」の札（ss.ILLU_ASSUME）。
#   配管の道すじ・空気の流れの矢印・亀裂の形は模式（断りに書く）
S5_K = 38.0
S5_X0M, S5_X0P, S5_Y0 = 46.0, 480.0, 705.0
S5_XL = 39.0                       # 尾部の絵の左の端（m）＝ここで胴体を切る（折れ線の印）
S5_XFW = s1_x(2658.0)              # APU 防火壁（65.22m）
S5_ZJ = 0.15                       # 隔壁の継ぎ目（L18）の高さ（隔壁の上下の真ん中＝付図-32 の L18 は円の真ん中の高さ）
S5_APU = (66.2, 68.1, -0.55, 0.85)  # APU の箱（x0, x1, z0, z1）＝長さ 1.9・高さ 1.4（解説 表5）・位置は模式
S5_RUD_SPLIT = 8.6                 # 上の方向舵と下の方向舵の境（S1 の線と同じ高さ・模式）
S5_SPAR = dict(front=((61.3, 3.0), (68.0, 14.6)), rear=((65.4, 2.7), (69.5, 14.6)))   # 前と後ろの桁（模式）
S5_ACT = ((66.4, 4.4), (68.3, 10.6))   # 方向舵を動かす装置2つ（下・上）の位置（模式）
S5_T = dict(show=0.6, tear=0.8, open=0.9, air=0.7, cone=1.6, rud=1.6, fin=1.0, press=3.0)
S5_OPEN = 55.0                     # 開いた上の半分の回り（度・模式）
S5_REC = dict(
    sky="報告書 p6（巡航高度24,000フィートに到達する直前）",
    body="報告書 p140（付図-4 三面図）・p9（セクション48＝BS2360〜2792・BS2658 以降のテールコーン）",
    bulk="報告書 p29（BS2360＝後部圧力隔壁の取付部）",
    tear="報告書 p125（L18接続部は一気に全面破断したものと推定される）",
    open="報告書 p125（開口面積は2~3平方メートル程度と推定される）",
    air="報告書 p125（客室与圧空気が後部胴体内に流出）",
    fw="報告書 p29（BS2658（APU防火壁の取付部））",
    cone="報告書 p125（APU防火壁が破壊されその後方に位置するAPU本体を含む胴体尾部構造の一部の破壊・脱落が生じたものと推定される）",
    fin="報告書 p125（垂直尾翼内に流れ込み、垂直尾翼の内部圧力が上昇し）",
    rud="報告書 p126（方向舵は脱落し、また4系統の方向舵操縦系統油圧配管もすべて破断したものと推定される）",
    hyd="報告書 p112（配管を4系統とするような冗長性を考慮した設計）",
    press="報告書 p126（操縦室を含む客室与圧は数秒間で大気圧まで減圧したものと推定される）",
    tail="報告書 p143（付図-7 尾翼ステーション図）")


def P5(x, z):
    return (S5_X0P + (x - S5_X0M) * S5_K, S5_Y0 - z * S5_K)


def _s5_P(frame):
    return P5 if frame == "tail" else P1


def _s5_k(frame):
    return S5_K if frame == "tail" else S1_K


def _clip_x(pts, lo=None, hi=None):
    """折れ線（x 増える順）を x の範囲で切る（端は線の上の点を足す）"""
    out = []
    for a, b in zip(pts, pts[1:]):
        for p in (a,):
            if (lo is None or p[0] >= lo) and (hi is None or p[0] <= hi):
                out.append(p)
        for edge in (lo, hi):
            if edge is not None and (a[0] - edge) * (b[0] - edge) < 0:
                t = (edge - a[0]) / (b[0] - a[0])
                out.append((edge, a[1] + (b[1] - a[1]) * t))
    last = pts[-1]
    if (lo is None or last[0] >= lo) and (hi is None or last[0] <= hi):
        out.append(last)
    return sorted(out, key=lambda p: p[0])


def _s5_outline(P, lo=None, hi=None, jag_lo=False, jag_hi=False):
    up = _clip_x(IL._smooth(S1_UP, per=6), lo, hi)
    dn = _clip_x(IL._smooth(S1_LO, per=6), lo, hi)
    pts = [P(*p) for p in up]
    if jag_hi:
        zt, zb = up[-1][1], dn[-1][1]
        pts += [P(up[-1][0] + (0.35 if k % 2 else -0.3), zt + (zb - zt) * k / 7.0) for k in range(1, 7)]
    pts += [P(*p) for p in reversed(dn)]
    if jag_lo:
        zt, zb = up[0][1], dn[0][1]
        pts += [P(up[0][0] + (0.3 if k % 2 else -0.3), zb + (zt - zb) * k / 7.0) for k in range(1, 7)]
    return pts


def s5_body_svg(frame):
    P = _s5_P(frame)
    if frame == "all":
        return s1_body_svg()
    out = _s5_outline(P, lo=S5_XL, hi=S5_XFW, jag_lo=True)
    g = [_path(out, C20["body"], C20["body_ln"], 3.0)]
    xa, xb, y = P(S5_XL + 1.0, 0)[0], P(55.0, 0)[0], P(0, 1.25)[1]
    g.append(f'<path d="M {xa:.1f} {y:.1f} L {xb:.1f} {y:.1f}" stroke="{C20["win"]}" stroke-width="12" stroke-dasharray="9 11"/>')
    return "".join(g)


def s5_cone_svg(frame):
    """テールコーン（BS2658 から後ろ）と APU の箱"""
    P = _s5_P(frame)
    out = _s5_outline(P, lo=S5_XFW)
    x0, x1, z0, z1 = S5_APU
    a, b = P(x0, z1), P(x1, z0)
    g = [_path(out, C20["body"], C20["body_ln"], 3.0),
         f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" rx="8" fill="{C20["eng"]}" '
         f'stroke="{C20["body_ln"]}" stroke-width="2.5"/>']
    if frame == "tail":
        g.append(f'<text x="{(a[0] + b[0]) / 2:.1f}" y="{(a[1] + b[1]) / 2 + 9:.1f}" font-family="Noto" font-size="24" '
                 f'fill="{C20["body_ln"]}" text-anchor="middle">APU</text>')
    return "".join(g)


def s5_fw_svg(frame):
    P = _s5_P(frame)
    up = _clip_x(IL._smooth(S1_UP, per=6), S5_XFW - 0.01, S5_XFW + 0.01)[0][1]
    dn = _clip_x(IL._smooth(S1_LO, per=6), S5_XFW - 0.01, S5_XFW + 0.01)[0][1]
    (x, y0), (_x, y1) = P(S5_XFW, up - 0.1), P(S5_XFW, dn + 0.1)
    return (f'<path d="M {x:.1f} {y0:.1f} L {x:.1f} {y1:.1f}" stroke="{C20["dark"]}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M {x:.1f} {y0:.1f} L {x:.1f} {y1:.1f}" stroke="{C20["eng_dk"]}" stroke-width="4" stroke-linecap="round"/>')


def s5_region_svg(frame, lo, hi, col, op):
    P = _s5_P(frame)
    return _path(_s5_outline(P, lo=lo, hi=hi), col, None, 0, op=op)


def _s5_bulk_pts(frame, upper):
    P = _s5_P(frame)
    zt, zb = 3.05, -2.75
    zc, rz = (zt + zb) / 2, (zt - zb) / 2
    a0 = math.degrees(math.asin((S5_ZJ - zc) / rz))
    rng = range(int(math.ceil(a0)), 91, 5) if upper else range(-90, int(math.floor(a0)) + 1, 5)
    pts = [(S1_XB + 1.25 * math.cos(math.radians(a)), zc + rz * math.sin(math.radians(a))) for a in rng]
    if upper:
        pts = [(S1_XB + 1.25 * math.cos(math.radians(a0)), S5_ZJ)] + pts
    else:
        pts = pts + [(S1_XB + 1.25 * math.cos(math.radians(a0)), S5_ZJ)]
    return [P(*p) for p in pts]


def s5_bulk_svg(frame, upper):
    q = _s5_bulk_pts(frame, upper)
    w = 11 if frame == "tail" else 9
    return (f'<path d="{_d(q, False)}" fill="none" stroke="{C20["dark"]}" stroke-width="{w + 5}" stroke-linecap="round"/>'
            f'<path d="{_d(q, False)}" fill="none" stroke="{C20["bulk"]}" stroke-width="{w}" stroke-linecap="round"/>')


def s5_joint(frame):
    """継ぎ目（L18）の画面の点＝上の半分が開くときの回る中心"""
    return _s5_bulk_pts(frame, True)[0]


def s5_tear_svg(frame):
    x, y = s5_joint(frame)
    k = _s5_k(frame) / S5_K
    pts = [(x - 26 * k, y - 3 * k), (x - 14 * k, y + 6 * k), (x - 4 * k, y - 6 * k), (x + 6 * k, y + 5 * k), (x + 16 * k, y - 4 * k),
           (x + 26 * k, y + 3 * k)]
    return (f'<path d="{_d(pts, False)}" fill="none" stroke="#10161b" stroke-width="{9 * k:.1f}" stroke-linejoin="round"/>'
            f'<path d="{_d(pts, False)}" fill="none" stroke="{C20["crack"]}" stroke-width="{4.5 * k:.1f}" stroke-linejoin="round"/>')


def _arrow_svg(pts, col, w=10.0, head=22.0, op=0.95):
    """太い矢印（折れ線の最後が頭）"""
    (ax, ay), (bx, by) = pts[-2], pts[-1]
    L = math.hypot(bx - ax, by - ay) or 1.0
    ux, uy = (bx - ax) / L, (by - ay) / L
    hx, hy = bx - head * ux, by - head * uy
    px, py = -uy * head * 0.6, ux * head * 0.6
    body = pts[:-1] + [(hx, hy)]
    return (f'<g opacity="{op}"><path d="{_d(body, False)}" fill="none" stroke="#10161b" stroke-width="{w + 6:.1f}" '
            f'stroke-linecap="round" stroke-linejoin="round"/><path d="{_d(body, False)}" fill="none" stroke="{col}" '
            f'stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M {bx:.1f} {by:.1f} L {hx + px:.1f} {hy + py:.1f} L {hx - px:.1f} {hy - py:.1f} Z" fill="{col}" '
            'stroke="#10161b" stroke-width="2.5"/></g>')


S5_AIR = [[(51.0, 2.3), (54.5, 2.4), (57.4, 2.4), (60.6, 2.0)], [(51.0, 1.0), (54.8, 1.3), (57.6, 2.0), (61.4, 0.9)],
          [(51.0, -0.3), (54.5, 0.4), (57.3, 1.7), (60.8, -0.4)]]
S5_FINAIR = [[(60.4, 1.6), (62.0, 3.2), (63.7, 6.6), (65.3, 10.0)], [(61.6, 0.6), (64.0, 2.6), (66.1, 5.8)]]


def s5_air_svg(frame, which):
    P = _s5_P(frame)
    k = _s5_k(frame) / S5_K
    paths = S5_AIR if which == "aft" else S5_FINAIR
    return "".join(_arrow_svg([P(*p) for p in IL._smooth(pl, per=6)], C20["air"], 10 * k, 24 * k) for pl in paths)


def s5_fin_svg(frame):
    P = _s5_P(frame)
    g = [_path([P(*p) for p in S1_STAB], C20["stab"], C20["body_ln"], 2.0),
         _path([P(*p) for p in S1_FIN], C20["fin"], C20["body_ln"], 3.0)]
    if frame == "tail":
        for nm in ("front", "rear"):
            (x0, z0), (x1, z1) = S5_SPAR[nm]
            a, b = P(x0, z0), P(x1, z1)
            g.append(f'<path d="M {a[0]:.1f} {a[1]:.1f} L {b[0]:.1f} {b[1]:.1f}" stroke="{C20["body_ln"]}" stroke-width="2" '
                     'stroke-dasharray="7 6" opacity="0.6"/>')
    return "".join(g)


def _rud_pts(upper):
    (x0, z0), (x1, z1), (x2, z2), (x3, z3) = S1_RUD     # 前の根元・前の先・後ろの先・後ろの根元
    def at(pa, pb, z):
        return (pa[0] + (pb[0] - pa[0]) * (z - pa[1]) / (pb[1] - pa[1]), z)
    f0, f1 = (x0, z0), (x1, z1)
    r0, r1 = (x3, z3), (x2, z2)
    if upper:
        return [at(f0, f1, S5_RUD_SPLIT), f1, r1, at(r0, r1, S5_RUD_SPLIT)]
    return [f0, at(f0, f1, S5_RUD_SPLIT), at(r0, r1, S5_RUD_SPLIT), r0]


def s5_rud_svg(frame, upper):
    P = _s5_P(frame)
    return _path([P(*p) for p in _rud_pts(upper)], C20["rud"], C20["body_ln"], 2.2)


def s5_fin_lost_svg(frame):
    P = _s5_P(frame)
    return (_path([P(*p) for p in S1_STAB], C20["stab"], C20["body_ln"], 2.0)
            + _path([P(*p) for p in S1_LOST_FIN], C20["fin"], C20["body_ln"], 3.0))


S5_CRACKS = [[(62.6, 4.2), (63.4, 5.1), (63.1, 6.0), (64.0, 7.0)], [(64.6, 6.4), (65.6, 7.6), (65.2, 8.6), (66.2, 9.8)],
             [(63.4, 9.2), (64.5, 10.4), (64.2, 11.3)]]


def s5_crack_svg(frame):
    P = _s5_P(frame)
    g = []
    for pl in S5_CRACKS:
        q = [P(*p) for p in pl]
        g.append(f'<path d="{_d(q, False)}" fill="none" stroke="#10161b" stroke-width="8" stroke-linejoin="round"/>'
                 f'<path d="{_d(q, False)}" fill="none" stroke="{C20["crack"]}" stroke-width="4" stroke-linejoin="round"/>')
    return "".join(g)


S5_HYD_Z = (2.85, 2.65, 2.45, 2.25)       # 4本の配管の高さ（胴体の中の上・模式）
S5_HYD_ROOT = 3.4                          # 尾翼の根元（ここで切れる＝模式）


def _hyd_lines():
    """4本の配管（胴体の中を後ろへ → 後ろの桁に沿って上へ）。返り値＝[(根元より下の折れ線, 上の折れ線)]"""
    (rx0, rz0), (rx1, rz1) = S5_SPAR["rear"]
    out = []
    for i, z in enumerate(S5_HYD_Z):
        dx = (i - 1.5) * 0.18
        xr = rx0 + (rx1 - rx0) * (z - rz0) / (rz1 - rz0) + dx
        lo = [(S5_XL + 0.6, z), (xr - 0.6, z), (xr, z + 0.3)]
        xroot = rx0 + (rx1 - rx0) * (S5_HYD_ROOT - rz0) / (rz1 - rz0) + dx
        lo.append((xroot, S5_HYD_ROOT))
        ztop = S5_ACT[1][1] + 0.4
        up = [(xroot, S5_HYD_ROOT), (rx0 + (rx1 - rx0) * (ztop - rz0) / (rz1 - rz0) + dx, ztop)]
        out.append((lo, up))
    return out


def s5_hyd_svg(frame, upper):
    P = _s5_P(frame)
    g = []
    for lo, up in _hyd_lines():
        q = [P(*p) for p in (up if upper else lo)]
        g.append(f'<path d="{_d(q, False)}" fill="none" stroke="#10161b" stroke-width="7" stroke-linejoin="round"/>'
                 f'<path d="{_d(q, False)}" fill="none" stroke="{C20["hyd"]}" stroke-width="3.5" stroke-linejoin="round"/>')
    if upper:
        for x, z in S5_ACT:
            a, b = P(x - 0.45, z + 0.22), P(x + 0.45, z - 0.22)
            g.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" rx="6" '
                     f'fill="{C20["act"]}" stroke="#10161b" stroke-width="2.5"/>')
    return "".join(g)


def s5_cut_svg(frame):
    """配管が切れた所（根元の上の切れ目と、こぼれる油の点＝模式）"""
    P = _s5_P(frame)
    g = []
    for lo, _up in _hyd_lines():
        x, z = lo[-1]
        cx, cy = P(x, z)
        g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{C20["crack"]}" stroke="#10161b" stroke-width="2"/>')
        for j, (dx, dy) in enumerate(((10, 14), (18, 30), (8, 40))):
            g.append(f'<circle cx="{cx + dx:.1f}" cy="{cy + dy:.1f}" r="{3.5 - j * 0.6:.1f}" fill="{C20["hyd"]}" opacity="0.85"/>')
    return "".join(g)


def _s5_move(start, states, steps, f, gone, dx, dy, rot, dur):
    """detach（f の値が gone になる段で、dx・dy・rot だけ動きながら消える）"""
    ks = [dict(stage=0, delay=0.0, a=0.0 if start[f] == gone else 1.0, dx=0.0, dy=0.0, rot=0.0)]
    cur = start[f]
    for i, (st, sp) in enumerate(zip(states, steps)):
        if st[f] != cur:
            d = float(sp.get("delay", KEY_DELAY))
            if st[f] == gone:
                ks.append(dict(stage=i, delay=d, dur=float(sp.get("dur", dur)) * 0.55, a=1.0, dx=dx * 0.5, dy=dy * 0.4, rot=rot * 0.5))
                ks.append(dict(stage=i, delay=d + float(sp.get("dur", dur)) * 0.55, dur=float(sp.get("dur", dur)) * 0.45, a=0.0,
                               dx=dx, dy=dy, rot=rot))
            cur = st[f]
    return ks


def _scene_S5(start, states, steps):
    allst = [start] + states
    _head_only("S5", start, states, ("view", "s5frame", "switch"))
    fr = start["s5frame"]
    R = S5_REC
    on = (lambda f, v="on": (lambda st: st[f] == v))
    if fr == "all" and any(st["s5cone"] == "off" or st["s5rud"] == "off" or st["s5fin"] != "on" or st["s5hyd"] != "off"
                           for st in allst):
        raise ValueError("illu S5：機全体（s5frame＝all）は隔壁の穴と気圧だけ（尾部の壊れ方は tail で）")
    P = _s5_P(fr)
    k = _s5_k(fr)
    parts = [_part("sky", _sky_svg("s5Sky") + _clouds_svg(), R["sky"])]
    lo_body = S5_XL if fr == "tail" else 0.0
    if any(st["s5press"] == "on" for st in allst):
        parts.append(_part("press", s5_region_svg(fr, lo_body, S1_XB, C20["press"], 0.5) if fr == "tail" else
                           _path(_s1_outline(S1_XB, jag=False), C20["press"], None, 0, op=0.5), R["press"],
                           keys=_akeys(start, states, steps, on("s5press"), S5_T["press"])))
    body = dict(_part("body", s5_body_svg(fr), R["body"]),
                geo=dict(kind="s5body", frame=fr, k=k, x0m=S5_X0M if fr == "tail" else 0.0,
                         x0p=S5_X0P if fr == "tail" else S1_X0))
    # 下の順で重ねる：胴体 → 与圧の色 → 尾部の圧力の色 → 隔壁 → 防火壁 → テールコーン → 主翼（all）→ 尾翼 → 方向舵 → 配管 → 空気の矢印
    parts.insert(1, body)
    if fr == "all":
        parts.append(_part("wing", s1_wing_svg(), R["body"]))
    if any(st["s5tailp"] == "on" for st in allst):
        parts.append(_part("tailp", s5_region_svg(fr, S1_XB, S5_XFW, C20["press"], 0.38), R["air"],
                           keys=_akeys(start, states, steps, on("s5tailp"), S5_T["air"])))
    parts.append(dict(_part("bulk_lo", s5_bulk_svg(fr, False), R["bulk"]), geo=dict(kind="s5bulk", x=P(S1_XB, 0)[0])))
    # 上の半分は継ぎ目（隔壁のいちばん後ろの点）を中心に後ろへ回って開く（SVG の角は時計回りが正＝上の端が後ろ〈右〉へ）
    jx, jy = s5_joint(fr)
    ks = [dict(stage=0, delay=0.0, rot=S5_OPEN if start["s5bulk"] == "open" else 0.0)]
    cur = start["s5bulk"]
    for i, (st, sp) in enumerate(zip(states, steps)):
        if st["s5bulk"] != cur:
            if st["s5bulk"] == "open":
                ks.append(dict(stage=i, delay=float(sp.get("delay", KEY_DELAY)), dur=float(sp.get("dur", S5_T["open"])), rot=S5_OPEN))
            cur = st["s5bulk"]
    opened = any(st["s5bulk"] == "open" for st in allst)
    parts.append(dict(_part("bulk_up", s5_bulk_svg(fr, True), R["open"] if opened else R["bulk"], (jx, jy), ks),
                      destroy=opened, geo=dict(kind="s5hole", open=opened)))
    if any(st["s5bulk"] in ("tear", "open") for st in allst):
        parts.append(dict(_part("tear", s5_tear_svg(fr), R["tear"],
                                keys=_akeys(start, states, steps, lambda st: st["s5bulk"] in ("tear", "open"), S5_T["tear"])),
                          destroy=True))
    if fr == "tail":
        parts.append(dict(_part("fw", s5_fw_svg(fr), R["fw"]), geo=dict(kind="s5fw", x=P(S5_XFW, 0)[0])))
        cone_off = any(st["s5cone"] == "off" for st in allst)
        parts.append(dict(_part("cone", s5_cone_svg(fr), R["cone"] if cone_off else R["body"], P(S5_XFW, 0.0),
                                _s5_move(start, states, steps, "s5cone", "off", 150.0, 260.0, 28.0, S5_T["cone"])),
                          destroy=cone_off, geo=dict(kind="s5cone", cut_x=P(S5_XFW, 0)[0])))
    lost = any(st["s5fin"] == "lost" for st in allst)
    parts.append(dict(_part("fin", s5_fin_svg(fr), R["tail"],
                            keys=_akeys(start, states, steps, lambda st: st["s5fin"] != "lost", S5_T["fin"])),
                      geo=dict(kind="fin", lost=False)))
    if lost:
        parts.append(dict(_part("fin_lost", s5_fin_lost_svg(fr), R["rud"], keys=_akeys(start, states, steps, on("s5fin", "lost"),
                                                                                       S5_T["fin"])),
                          destroy=True, geo=dict(kind="fin", lost=True)))
    if any(st["s5fin"] == "crack" for st in allst):
        parts.append(dict(_part("cracks", s5_crack_svg(fr), R["fin"],
                                keys=_akeys(start, states, steps, on("s5fin", "crack"), S5_T["tear"])), destroy=True))
    rud_off = any(st["s5rud"] == "off" for st in allst)
    for up, (dx, dy, rot) in ((True, (180.0, 140.0, 35.0)), (False, (150.0, 220.0, 22.0))):
        nm = "rud_up" if up else "rud_lo"
        parts.append(dict(_part(nm, s5_rud_svg(fr, up), R["rud"] if rud_off else R["tail"], P(*_rud_pts(up)[0]),
                                _s5_move(start, states, steps, "s5rud", "off", dx, dy, rot, S5_T["rud"])),
                          destroy=rud_off, geo=dict(kind="s5rud", upper=up)))
    if any(st["s5hyd"] != "off" for st in allst):
        parts.append(dict(_part("hyd_lo", s5_hyd_svg(fr, False), R["hyd"],
                                keys=_akeys(start, states, steps, lambda st: st["s5hyd"] != "off")),
                          geo=dict(kind="s5hyd", n=len(S5_HYD_Z))))
        # 尾翼の中の配管と装置は、尾翼が欠けたら一緒に消える（宙に残さない）
        parts.append(_part("hyd_up", s5_hyd_svg(fr, True), R["hyd"],
                           keys=_akeys(start, states, steps, lambda st: st["s5hyd"] == "on" and st["s5fin"] != "lost", S5_T["fin"])))
        if any(st["s5hyd"] == "cut" for st in allst):
            parts.append(dict(_part("cut", s5_cut_svg(fr), R["rud"], keys=_akeys(start, states, steps, on("s5hyd", "cut"))),
                              destroy=True))
    if any(st["s5air"] == "on" for st in allst):
        parts.append(_part("air", s5_air_svg(fr, "aft"), R["air"], keys=_akeys(start, states, steps, on("s5air"), S5_T["air"])))
    if any(st["s5finair"] == "on" for st in allst):
        parts.append(_part("finair", s5_air_svg(fr, "fin"), R["fin"],
                           keys=_akeys(start, states, steps, on("s5finair"), S5_T["air"])))
    if start["switch"] == "on":
        parts.append(_switch_part("横から見ると"))
    return parts


def _s5_anchors(st):
    fr = st["s5frame"]
    P = _s5_P(fr)
    x0, x1, z0, z1 = S5_APU
    lo, up = _hyd_lines()[0]
    return dict(joint=s5_joint(fr), hole=P(S1_XB + 1.0, 2.6), bulk=P(S1_XB + 1.2, 0.6), tailsec=P(61.5, 0.6),
                fw=P(S5_XFW, -1.4), apu=P((x0 + x1) / 2, z0), cone=P(68.5, 0.0), fin=P(64.6, 8.0), rud=P(69.6, 6.0),
                rud_up=P(70.0, 11.5), hyd=P(*up[0]), cut=P(*lo[-1]), cabin=P(50.0 if fr == "tail" else 31.0, 0.4),
                cockpit=P(4.2, 4.0))


def _s5_note(st0, states):
    if st0["s5frame"] == "all":
        return "形は付図-4 の三面図から・大きさと配置は模式・人は描かない"
    return "形は付図-4・付図-7 から・桁と配管の道すじ・空気の矢印・亀裂の形は模式・人は描かない"


# ══════════════════════════════════════════════════════════
#  S6 後部圧力隔壁の継ぎ目（正面から＝隔壁の円・横から＝継ぎ目の断面）🆕 ⑤b-4
# ══════════════════════════════════════════════════════════
# 正面（front）＝付図-32（後部圧力隔壁損壊図・後ろから見る）・付図-36（L18接続部の略図）：円・36本の横の補強材（L1〜L36）の真ん中が L18
#   ＝上半分と下半分のウエブの合わせ面（p.101「隔壁の上半部と下半部のウェブ合わせ面（L18接続部）」）。1978年の修理で下半分を取り替えた（p.101）
# 横（side・both）＝別添1 付図-3（p.252「修正指示と実際の継ぎ方」）の断面をそのまま：前（左）から 下の板・継ぎ板・上の板の3枚、リベット3列
#   （上から 既存の位置2列＋新しい列＝1インチ下）。🔴 付図に無い線は描き足さない（映像方針 §2）。補強材の点線・シールは省いた（足していない）
#   板の重なり（インチ・下が正）＝付図-3 を ⑤b-4 に2倍の切り出しで測った値（列の間＝1インチ＝約155画素）
S6_ROWS = (-1.0, 0.0, 1.0)
S6_EDGE = 2.6                      # 絵の上と下の端（インチ）＝板はここまで続く
S6_LAYERS = dict(
    plan=dict(lower=(-0.50, S6_EDGE), splice=(-1.34, 1.32), upper=(-S6_EDGE, 0.34), filler=None),
    real=dict(lower=(-0.58, S6_EDGE), splice=(-0.55, 1.32), upper=(-S6_EDGE, 0.39), filler=(-1.32, -0.61)))
S6_ORDER = ("lower", "splice", "upper")      # 前（左）から
S6_T = 0.18                         # 板の厚さ（インチ・付図-3 の見え方より厚く＝模式）
# ⑤b-4 の門番 layout：上の題（「指示された継ぎ方」）が合図の札（y 40〜106）と重なった＝絵を下げて少し小さく
S6_VIEW = dict(side=dict(k=130.0, cx=dict(plan=960.0, real=960.0), cy=500.0),
               both=dict(k=125.0, cx=dict(plan=600.0, real=1320.0), cy=500.0))
S6F_C, S6F_R = (960.0, 470.0), 330.0
S6F_STRAPS = (0.93, 0.75, 0.56, 0.36)       # 第1〜第4ストラップの半径（円の半径に対する比・付図-32 の目読み）
S6_TIT = dict(plan="指示された継ぎ方", real="実際の継ぎ方")
S6_REC = dict(
    front="報告書 p168（付図-32 後部圧力隔壁損壊図）・p172（付図-36 後部圧力隔壁L18接続部（略図））",
    l18="報告書 p101（隔壁の上半部と下半部のウェブ合わせ面（L18接続部））",
    side="報告書 p252（別添1 付図-3 修正指示と実際の継ぎ方）",
    plan="報告書 p252（付図-3 左＝修正措置で指示された継ぎ方）",
    real="報告書 p252（付図-3 右＝実際の継ぎ方）・p248（2列リベットで結合されるべきものが…1列リベット結合）",
    made="報告書 p248（スプライス・プレート及びフィラは、取り外した旧隔壁から製作された）")


def _s6_geo(view, kind):
    v = S6_VIEW[view]
    k, cx, cy = v["k"], v["cx"][kind], v["cy"]
    xs = {nm: cx + (i - 1) * S6_T * k for i, nm in enumerate(S6_ORDER)}       # 板の真ん中の x
    return k, cx, cy, xs


def _s6_y(view, kind, inch):
    k, _cx, cy, _xs = _s6_geo(view, kind)
    return cy + inch * k


def s6_stack_svg(view, kind):
    """断面（板とリベット）＋名前"""
    k, cx, cy, xs = _s6_geo(view, kind)
    L = S6_LAYERS[kind]
    w = S6_T * k
    col = dict(lower=C20["web_lo"], splice=C20["splice"], upper=C20["web_up"], filler=C20["filler"])
    g = []
    for nm in ("lower", "upper", "splice", "filler"):
        rng = L[nm]
        if not rng:
            continue
        x = xs["splice" if nm == "filler" else nm]
        y0, y1 = cy + rng[0] * k, cy + rng[1] * k
        g.append(f'<rect x="{x - w / 2:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{y1 - y0:.1f}" fill="{col[nm]}" '
                 f'stroke="#10161b" stroke-width="2.5"/>')
    xl, xr = xs["lower"] - w / 2, xs["upper"] + w / 2
    for r in S6_ROWS:
        y = cy + r * k
        hw, hh = 0.20 * k, 0.40 * k
        g.append(f'<rect x="{xl - hw:.1f}" y="{y - hh / 2:.1f}" width="{hw:.1f}" height="{hh:.1f}" rx="4" fill="{C20["rivet"]}" '
                 f'stroke="#10161b" stroke-width="2.5"/>'
                 f'<rect x="{xl:.1f}" y="{y - 0.07 * k:.1f}" width="{xr - xl:.1f}" height="{0.14 * k:.1f}" fill="{C20["rivet"]}" '
                 f'stroke="#10161b" stroke-width="1.5"/>'
                 f'<path d="M {xr:.1f} {y - 0.19 * k:.1f} A {0.19 * k:.1f} {0.19 * k:.1f} 0 0 1 {xr:.1f} {y + 0.19 * k:.1f} Z" '
                 f'fill="{C20["rivet"]}" stroke="#10161b" stroke-width="2.5"/>')
    big = view == "side"
    fs = 28 if big else 24
    g.append(_text(cx, cy - S6_EDGE * k - 18, S6_TIT[kind], 32 if big else 28))
    # 名前（引き出し線つき）：上の板は右上・下の板は右下・継ぎ板は左・フィラは左上
    def lab(x0, y0, x1, y1, t, anc):
        return (f'<path d="M {x0:.1f} {y0:.1f} L {x1:.1f} {y1:.1f}" stroke="{C20["name"]}" stroke-width="2.2"/>'
                f'<circle cx="{x0:.1f}" cy="{y0:.1f}" r="4" fill="{C20["name"]}"/>'
                + _text(x1 + (8 if anc == "start" else -8), y1 + fs * 0.35, t, fs, anchor=anc))
    xu = xs["upper"] + w / 2
    g.append(lab(xu, cy - 1.9 * k, xu + 0.9 * k, cy - 2.05 * k, "上の板（上半分）", "start"))
    g.append(lab(xs["lower"] - w / 2, cy + 2.0 * k, xs["lower"] - w / 2 - 0.9 * k, cy + 2.15 * k, "下の板（下半分）", "end"))
    g.append(lab(xs["splice"], cy + 1.15 * k, xs["lower"] - w / 2 - 0.9 * k, cy + 1.2 * k, "継ぎ板", "end"))
    if L["filler"]:
        g.append(lab(xs["splice"] - w / 2, cy - 1.25 * k, xs["lower"] - w / 2 - 0.9 * k, cy - 1.55 * k, "フィラ（詰め物）", "end"))
    return "".join(g)


def _s6_join_rows(kind):
    """上の板と、継ぎ板か下の板を一緒に留める列（門番と同じ考え＝列の高さに上の板と、継ぎ板か下の板がある）"""
    L = S6_LAYERS[kind]
    def has(nm, r):
        return bool(L[nm]) and L[nm][0] <= r <= L[nm][1]
    return [r for r in S6_ROWS if has("upper", r) and (has("splice", r) or has("lower", r))]


def s6_rows_svg(view, kind):
    k, cx, cy, xs = _s6_geo(view, kind)
    g = []
    for r in _s6_join_rows(kind):
        y = cy + r * k
        g.append(f'<ellipse cx="{cx:.1f}" cy="{y:.1f}" rx="{0.62 * k:.1f}" ry="{0.30 * k:.1f}" fill="none" stroke="#10161b" '
                 f'stroke-width="10" opacity="0.6"/><ellipse cx="{cx:.1f}" cy="{y:.1f}" rx="{0.62 * k:.1f}" ry="{0.30 * k:.1f}" '
                 f'fill="none" stroke="{C20["hl"]}" stroke-width="5"/>')
    return "".join(g)


def s6_glow_svg(view, kind, nm):
    k, cx, cy, xs = _s6_geo(view, kind)
    rng = S6_LAYERS[kind][nm]
    w = S6_T * k
    x = xs["splice"]
    y0, y1 = cy + rng[0] * k, cy + rng[1] * k
    return (f'<rect x="{x - w / 2 - 7:.1f}" y="{y0 - 7:.1f}" width="{w + 14:.1f}" height="{y1 - y0 + 14:.1f}" rx="6" fill="none" '
            f'stroke="#10161b" stroke-width="10" opacity="0.6"/><rect x="{x - w / 2 - 7:.1f}" y="{y0 - 7:.1f}" width="{w + 14:.1f}" '
            f'height="{y1 - y0 + 14:.1f}" rx="6" fill="none" stroke="{C20["hl"]}" stroke-width="5"/>')


def s6_front_svg():
    cx, cy = S6F_C
    R = S6F_R
    g = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{C20["sky0"]}"/>',
         f'<path d="M {cx - R:.1f} {cy:.1f} A {R:.1f} {R:.1f} 0 0 1 {cx + R:.1f} {cy:.1f} Z" fill="{C20["web_up"]}"/>',
         f'<path d="M {cx - R:.1f} {cy:.1f} A {R:.1f} {R:.1f} 0 0 0 {cx + R:.1f} {cy:.1f} Z" fill="{C20["web_lo"]}"/>']
    for i in range(1, 36):
        y = cy - R + i * 2 * R / 36.0
        hw = math.sqrt(max(0.0, R * R - (y - cy) ** 2))
        g.append(f'<path d="M {cx - hw:.1f} {y:.1f} L {cx + hw:.1f} {y:.1f}" stroke="{C20["body_ln"]}" stroke-width="1.2" opacity="0.35"/>')
    for f in S6F_STRAPS:
        g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R * f:.1f}" fill="none" stroke="{C20["body_ln"]}" stroke-width="1.5" '
                 'stroke-dasharray="6 7" opacity="0.45"/>')
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R:.1f}" fill="none" stroke="#10161b" stroke-width="5"/>')
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="18" fill="{C20["eng"]}" stroke="#10161b" stroke-width="2.5"/>')
    g.append(_text(cx, cy - R * 0.52, "上半分", 30, col=C20["dark"]).replace('stroke="#10161b"', f'stroke="{C20["web_up"]}"'))
    g.append(_text(cx, cy + R * 0.62, "下半分（1978年に取り替え）", 28, col=C20["dark"]).replace('stroke="#10161b"',
                                                                                                  f'stroke="{C20["web_lo"]}"'))
    g.append(_text(cx - R - 14, cy + 9, "L18", 26, anchor="end"))
    return "".join(g)


def s6_l18_svg():
    cx, cy = S6F_C
    R = S6F_R
    return (f'<path d="M {cx - R:.1f} {cy:.1f} L {cx + R:.1f} {cy:.1f}" stroke="#10161b" stroke-width="15" opacity="0.6"/>'
            f'<path d="M {cx - R:.1f} {cy:.1f} L {cx + R:.1f} {cy:.1f}" stroke="{C20["hl"]}" stroke-width="8"/>')


def _scene_S6(start, states, steps):
    allst = [start] + states
    _head_only("S6", start, states, ("view", "s6kind", "switch"))
    v = start["view"]
    R = S6_REC
    on = (lambda f, v="on": (lambda st: st[f] == v))
    if v == "front":
        if any(st[f] == "on" for st in allst for f in ("s6spl", "s6row", "s6fil")):
            raise ValueError("illu S6：正面（front）は L18 の印だけ（板とリベットの印は断面で）")
        parts = [dict(_part("disk", s6_front_svg(), R["front"]),
                      geo=dict(kind="s6front", c=list(S6F_C), r=S6F_R, l18_y=S6F_C[1], n_stiff=36))]
        if any(st["s6l18"] == "on" for st in allst):
            parts.append(_part("l18", s6_l18_svg(), R["l18"], keys=_akeys(start, states, steps, on("s6l18"))))
        if start["switch"] == "on":
            parts.append(_switch_part("正面から見ると"))
        return parts
    if any(st["s6l18"] == "on" for st in allst):
        raise ValueError("illu S6：L18 の印（s6l18）は正面（front）だけ")
    kinds = ("plan", "real") if v == "both" else (start["s6kind"],)
    parts = [_part("bg", f'<rect x="0" y="0" width="{W}" height="{H}" fill="{C20["sky0"]}"/>', R["side"])]
    for kd in kinds:
        k, cx, cy, xs = _s6_geo(v, kd)
        parts.append(dict(_part(f"stack_{kd}", s6_stack_svg(v, kd), R[kd]),
                          geo=dict(kind="s6joint", which=kd, k=k, cy=cy, rows=list(S6_ROWS),
                                   layers={nm: (list(r) if r else None) for nm, r in S6_LAYERS[kd].items()})))
        # 並べた絵（both）の継ぎ板の印は実際の側だけ（c812「その継ぎ板とフィラは、取り外した古い隔壁から」）
        if any(st["s6spl"] == "on" for st in allst) and (v != "both" or kd == "real"):
            parts.append(_part(f"spl_{kd}", s6_glow_svg(v, kd, "splice"), R["made"] if kd == "real" else R[kd],
                               keys=_akeys(start, states, steps, on("s6spl"))))
        if kd == "real" and any(st["s6fil"] == "on" for st in allst):
            parts.append(_part(f"fil_{kd}", s6_glow_svg(v, kd, "filler"), R["made"], keys=_akeys(start, states, steps, on("s6fil"))))
        if any(st["s6row"] == "on" for st in allst):
            parts.append(dict(_part(f"rows_{kd}", s6_rows_svg(v, kd), R[kd], keys=_akeys(start, states, steps, on("s6row"))),
                              geo=dict(kind="s6rows", which=kd, rows=_s6_join_rows(kd))))
    if v == "both":
        parts.append(_part("sep", f'<path d="M 960 150 L 960 820" stroke="{C20["route"]}" stroke-width="2" opacity="0.3"/>', R["side"]))
    if start["switch"] == "on":
        parts.append(_switch_part("横から見ると"))
    return parts


def _s6_anchors(st):
    v = st["view"]
    if v == "front":
        cx, cy = S6F_C
        return dict(l18=(cx - S6F_R * 0.55, cy), l18r=(cx + S6F_R * 0.55, cy), upper=(cx, cy - S6F_R * 0.35),
                    lower=(cx, cy + S6F_R * 0.35))
    an = {}
    for kd in (("plan", "real") if v == "both" else (st["s6kind"],)):
        k, cx, cy, xs = _s6_geo(v, kd)
        pre = "" if v == "side" else kd[0] + "_"
        rows = _s6_join_rows(kd)
        w = S6_T * k
        an[pre + "rows"] = (xs["upper"] + w / 2 + 0.25 * k, cy + (sum(rows) / len(rows)) * k)
        an[pre + "splice"] = (xs["splice"], cy + 0.6 * k)
        an[pre + "upper"] = (xs["upper"] + w / 2, cy - 1.6 * k)
        an[pre + "lower"] = (xs["lower"] - w / 2, cy + 1.6 * k)
        if S6_LAYERS[kd]["filler"]:
            an[pre + "filler"] = (xs["splice"] + w / 2, cy - 1.0 * k)
        an[pre + "row1"] = (xs["upper"] + w / 2 + 0.2 * k, cy - 1.0 * k)
        an[pre + "row2"] = (xs["upper"] + w / 2 + 0.2 * k, cy)
    return an


def _s6_note(st0, states):
    if st0["view"] == "front":
        return "形は付図-32・付図-36 から・補強材の数と間隔は模式・人は描かない"
    return "形は付図-3 から（板の厚さは強調・補強材とシールは省いた）・人は描かない"


# ══════════════════════════════════════════════════════════
#  S7 相模湾の地図（上から・北が上）🆕 ⑤b-4
# ══════════════════════════════════════════════════════════
# 点と線＝`ref/ep20/sagami20.json`（`sagami20.py`）：付図-20（浮遊残骸の揚収場所 1〜28＝図の海岸線を Natural Earth に重ねて読んだ）・
#   付図-21（調査区域の枠・調査地点 ①〜⑰・推定飛行経路 244度・推定異常音発生点・海岸線＝緯度経度の目盛りから読んだ）・
#   解説 図15（推定落下区域の楕円・海流の矢印＝経緯線から読んだ・形は目安）
# frame＝bay（相模湾の全体・1km 7.6画素＝Natural Earth の陸）／area（付図-21 の範囲だけの窓・1km 60画素＝図の海岸線）
S7_VIEW = dict(bay=dict(k=7.6, c=(139.47, 34.97), px=(960.0, 480.0), lat0=35.0),
               area=dict(k=60.0, c=(139.071, 34.763), px=(760.0, 470.0), lat0=34.77))
S7_SCALE = dict(bay=10.0, area=1.0)
S7_PATH_KM = (50.0, 14.0)          # 推定飛行経路の線＝推定異常音発生点から東北東へ 50km・西南西へ 14km（図15 の線と同じく湾を横切る）
S7_NAMES = dict(bay=(("相模湾", (139.40, 35.12)), ("伊豆半島", (138.98, 34.88)), ("大島", (139.53, 34.72)),
                     ("三浦半島", (139.66, 35.29)), ("房総半島", (139.98, 35.10))),
                area=(("伊豆半島", (139.025, 34.795)), ("稲取", (139.052, 34.775))))
S7_T = dict(show=0.6, cur=1.2)
S7_REC = dict(
    map="報告書 p157（付図-21 相模湾海底調査区域）",
    deb="報告書 p156（付図-20 相模湾等の浮遊残骸揚収場所図）・p13（総数53個の浮遊残骸が揚収された）",
    area="報告書 p157（付図-21 の調査区域）・p13（相模湾の海底に沈んだ可能性のある残骸の調査）",
    pts="報告書 p157（付図-21 ①〜⑰ えい航式深海カメラによる調査地点）",
    none="報告書 p13（同機の残骸の一部とみられるものは発見されなかった）",
    drop="解説 p1022（図15 推定落下区域）",
    cur="解説 p1022（図15 海流概況）",
    path="報告書 p157（付図-21 推定飛行経路244度（レーダ航跡）・推定異常音発生点）",
    obj="解説 p1025（表5 推定される落下物）",
    sink="解説 p1025（APUとアクチュエータは…沈んでいる可能性は大きい・両方向舵は…漂流した部分がある可能性が大きい）")
# 推定される落下物の6つ（解説 表5 の並び・名前は台本の言い方）。形は模式（表5 の寸法では描かない）
S7_OBJ = (("apu", "APU"), ("act", "方向舵を動かす装置×2"), ("cone", "胴体の最後部"), ("box", "垂直尾翼の中央の箱"),
          ("rud_up", "上の方向舵"), ("rud_lo", "下の方向舵"))
S7_PANEL = (1250.0, 150.0, 1890.0, 800.0)


@lru_cache(maxsize=1)
def s7_data():
    return json.loads((REF / "sagami20.json").read_text(encoding="utf-8"))


def P7(frame, lon, lat):
    v = S7_VIEW[frame]
    kx = math.cos(math.radians(v["lat0"])) * 111.32
    return (v["px"][0] + (lon - v["c"][0]) * kx * v["k"], v["px"][1] - (lat - v["c"][1]) * 110.57 * v["k"])


def _s7_proj(frame):
    v = S7_VIEW[frame]
    return dict(c=list(v["c"]), px=list(v["px"]), k=v["k"], lat0=v["lat0"])


def s7_base_svg(frame):
    g = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{C20["sea"] if frame == "bay" else C20["panel"]}"/>']
    if frame == "bay":
        d = json.loads((REF / "coast_ne10m.json").read_text(encoding="utf-8"))
        for poly in d["polys"]:
            g.append(_path([P7(frame, lon, lat) for lon, lat in poly], C20["land"], C20["land_ln"], 1.8))
    else:
        nr = s7_data()["near"]
        (lo0, la0), (lo1, la1) = nr["bbox"]
        a, b = P7(frame, lo0, la1), P7(frame, lo1, la0)
        g.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="{C20["sea"]}"/>')
        coast = nr["coast"]
        land = [(lo0, la1), (coast[0][0], la1)] + [tuple(p) for p in coast] + [(lo0, coast[-1][1])]
        g.append(_path([P7(frame, *p) for p in land], C20["land"], None, 0))
        g.append(_path([P7(frame, *p) for p in coast], "none", C20["land_ln"], 2.4, close=False))
        g.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="none" '
                 f'stroke="{C20["name"]}" stroke-width="3" opacity="0.8"/>')
    for t, (lon, lat) in S7_NAMES[frame]:
        x, y = P7(frame, lon, lat)
        g.append(_text(x, y, t, 26 if frame == "bay" else 28))
    return "".join(g)


def s7_scale_svg(frame):
    km = S7_SCALE[frame]
    L = km * S7_VIEW[frame]["k"]
    if frame == "bay":
        x1, y = 1790.0, 846.0
    else:
        nr = s7_data()["near"]
        b = P7(frame, nr["bbox"][1][0], nr["bbox"][0][1])
        x1, y = b[0] - 24.0, b[1] - 24.0
    x0 = x1 - L
    d = f"M {x0:.1f} {y - 8:.1f} L {x0:.1f} {y:.1f} L {x1:.1f} {y:.1f} L {x1:.1f} {y - 8:.1f}"
    return (f'<path d="{d}" fill="none" stroke="#10161b" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{C20["name"]}" stroke-width="3" stroke-linejoin="round"/>'
            + _text((x0 + x1) / 2, y - 16, f"{km:.0f}キロ", 24))


def s7_deb_svg(frame):
    g = []
    for _k, (lon, lat, _d) in s7_data()["bay"]["pts"].items():
        x, y = P7(frame, lon, lat)
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{C20["deb"]}" stroke="#10161b" stroke-width="2.2"/>')
    return "".join(g)


def s7_area_svg(frame):
    pts = [P7(frame, *p) for p in s7_data()["near"]["area"]]
    w = 4.0 if frame == "bay" else 5.0
    return (_path(pts, C20["area"], None, 0, op=0.16) + _path(pts, "none", "#10161b", w + 4, op=0.6)
            + _path(pts, "none", C20["area"], w))


def s7_drop_svg(frame):
    pts = [P7(frame, *p) for p in s7_data()["fig15"]["ellipse"]["ll"]]
    return _path(pts, C20["drop"], "#10161b", 2.5, op=0.55)


def s7_cur_svg(frame):
    g = []
    for ar in s7_data()["fig15"]["arrows"]:
        pts = [P7(frame, *p) for p in ar["ll"]]
        pts = IL._smooth(pts, per=4) if len(pts) > 2 else pts
        g.append(_arrow_svg(pts, C20["cur"], 5.0, 16.0, 0.9))
    return "".join(g)


def s7_path_pts(frame):
    nr = s7_data()["near"]
    (a0, b0), (a1, b1) = nr["flight"]
    lat0 = S7_VIEW[frame]["lat0"]
    kx = math.cos(math.radians(lat0)) * 111.32
    de, dn = (a1 - a0) * kx, (b1 - b0) * 110.57
    L = math.hypot(de, dn)
    ue, un = de / L, dn / L                       # 西南西（飛んだ向き）
    bx, by = nr["boom"]
    back, fwd = S7_PATH_KM
    p0 = (bx - ue * back / kx, by - un * back / 110.57)
    p1 = (bx + ue * fwd / kx, by + un * fwd / 110.57)
    a, b = P7(frame, *p0), P7(frame, *p1)
    if frame == "area":
        # ⑤b-4 の下見：付図-21 の窓の外（落下物の絵の上）まで線が出た＝窓の枠で切る
        (lo0, la0), (lo1, la1) = nr["bbox"]
        (x0, y0), (x1, y1) = P7(frame, lo0, la1), P7(frame, lo1, la0)
        t0, t1 = 0.0, 1.0
        dx, dy = b[0] - a[0], b[1] - a[1]
        for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if abs(p) < 1e-12:
                continue
            r = q / p
            if p < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
        a, b = (a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)
    return a, b


def s7_path_svg(frame):
    p0, p1 = s7_path_pts(frame)
    return _arrow_svg([p0, p1], C20["route"], 4.0, 18.0, 0.95)


def s7_boom_svg(frame):
    x, y = P7(frame, *s7_data()["near"]["boom"])
    r = 13.0 if frame == "bay" else 18.0
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="#10161b" stroke-width="9" opacity="0.6"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{C20["hl"]}" stroke-width="4.5"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{C20["hl"]}"/>')


def s7_pts_svg(frame, none):
    g = []
    for _k, (lon, lat) in s7_data()["near"]["pts"].items():
        x, y = P7(frame, lon, lat)
        if none:
            d = f"M {x - 10:.1f} {y - 10:.1f} L {x + 10:.1f} {y + 10:.1f} M {x + 10:.1f} {y - 10:.1f} L {x - 10:.1f} {y + 10:.1f}"
            g.append(f'<path d="{d}" stroke="#10161b" stroke-width="9" stroke-linecap="round"/>'
                     f'<path d="{d}" stroke="{C20["crack"]}" stroke-width="4.5" stroke-linecap="round"/>')
        else:
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{C20["morn"]}" stroke="#10161b" stroke-width="2.5"/>')
    return "".join(g)


def _s7_obj_cells():
    x0, y0, x1, y1 = S7_PANEL
    cw, ch = (x1 - x0) / 2, (y1 - y0 - 70) / 3
    return {k: (x0 + cw * (i % 2) + cw / 2, y0 + 70 + ch * (i // 2) + ch * 0.42) for i, (k, _n) in enumerate(S7_OBJ)}


def _obj_shape(k, cx, cy):
    """推定される落下物の形（模式）"""
    s = 1.0
    if k == "apu":
        return (f'<rect x="{cx - 46:.1f}" y="{cy - 30:.1f}" width="80" height="60" rx="10" fill="{C20["eng"]}" stroke="#10161b" stroke-width="2.5"/>'
                + _path([(cx + 34, cy - 18), (cx + 56, cy - 10), (cx + 56, cy + 10), (cx + 34, cy + 18)], C20["eng_dk"], "#10161b", 2.2))
    if k == "act":
        g = ""
        for dy in (-18, 18):
            g += (f'<rect x="{cx - 50:.1f}" y="{cy + dy - 10:.1f}" width="60" height="20" rx="8" fill="{C20["act"]}" stroke="#10161b" stroke-width="2.2"/>'
                  f'<path d="M {cx + 10:.1f} {cy + dy:.1f} L {cx + 48:.1f} {cy + dy:.1f}" stroke="#10161b" stroke-width="8" stroke-linecap="round"/>'
                  f'<path d="M {cx + 10:.1f} {cy + dy:.1f} L {cx + 48:.1f} {cy + dy:.1f}" stroke="{C20["eng"]}" stroke-width="4" stroke-linecap="round"/>')
        return g
    if k == "cone":
        return _path([(cx - 50, cy - 34), (cx + 40, cy - 14), (cx + 52, cy - 4), (cx + 52, cy + 6), (cx + 40, cy + 14), (cx - 50, cy + 34)],
                     C20["body"], "#10161b", 2.5)
    if k == "box":
        return (_path([(cx - 30, cy + 46), (cx - 6, cy - 50), (cx + 26, cy - 50), (cx + 34, cy + 46)], C20["fin"], "#10161b", 2.5)
                + "".join(f'<path d="M {cx - 26 + 6 * j:.1f} {cy + 30 - 22 * j:.1f} L {cx + 33 - 1.4 * j:.1f} {cy + 30 - 22 * j:.1f}" '
                          f'stroke="{C20["body_ln"]}" stroke-width="1.8" opacity="0.7"/>' for j in range(4)))
    h = 46 if k == "rud_up" else 40
    return _path([(cx - 16, cy + h), (cx + 6 * s, cy - h), (cx + 26, cy - h), (cx + 22, cy + h)], C20["rud"], "#10161b", 2.5)


def s7_obj_svg():
    x0, y0, x1, y1 = S7_PANEL
    g = [f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" rx="18" fill="{C20["panel"]}" '
         f'stroke="{C20["name"]}" stroke-width="2.5" opacity="0.94"/>',
         _text((x0 + x1) / 2, y0 + 46, "推定される落下物（形は模式）", 28)]
    for k, name in S7_OBJ:
        cx, cy = _s7_obj_cells()[k]
        g.append(_obj_shape(k, cx, cy))
        g.append(_text(cx, cy + 86, name, 22))
    return "".join(g)


def s7_sink_svg(which):
    """heavy＝APU と方向舵を動かす装置の下向きの矢印（沈む）／light＝上下の方向舵の波の矢印（流される）"""
    g = []
    cells = _s7_obj_cells()
    if which == "heavy":
        for k in ("apu", "act"):
            cx, cy = cells[k]
            g.append(_arrow_svg([(cx + 74, cy - 30), (cx + 74, cy + 40)], C20["cur"], 6.0, 16.0))
    else:
        for k in ("rud_up", "rud_lo"):
            cx, cy = cells[k]
            pts = [(cx + 40, cy + 8), (cx + 52, cy - 2), (cx + 64, cy + 8), (cx + 76, cy - 2), (cx + 92, cy + 4)]
            g.append(_arrow_svg(pts, C20["cur"], 5.0, 14.0))
    return "".join(g)


def _scene_S7(start, states, steps):
    allst = [start] + states
    _head_only("S7", start, states, ("view", "s7frame", "switch"))
    fr = start["s7frame"]
    R = S7_REC
    on = (lambda f, v="on": (lambda st: st[f] == v))
    if fr == "bay" and any(st["s7pts"] != "off" or st["s7obj"] == "on" for st in allst):
        raise ValueError("illu S7：調査地点 ①〜⑰ と落下物の絵は付図-21 の窓（s7frame＝area）だけ")
    if fr == "area" and any(st["s7deb"] == "on" or st["s7drop"] == "on" or st["s7cur"] == "on" for st in allst):
        raise ValueError("illu S7：揚収場所・推定落下区域・海流は湾の全体（s7frame＝bay）だけ")
    if any(st["s7sink"] != "off" and st["s7obj"] != "on" for st in allst):
        raise ValueError("illu S7：沈む・流れる矢印（s7sink）は落下物の絵（s7obj）と一緒に")
    parts = [dict(_part("map", s7_base_svg(fr), R["map"] if fr == "area" else R["deb"]), geo=dict(kind="s7map", frame=fr, proj=_s7_proj(fr))),
             dict(_part("scale", s7_scale_svg(fr), R["map"]), geo=dict(kind="scale", km=S7_SCALE[fr], px=S7_SCALE[fr] * S7_VIEW[fr]["k"]))]
    if any(st["s7drop"] == "on" for st in allst):
        parts.append(_part("drop", s7_drop_svg(fr), R["drop"], keys=_akeys(start, states, steps, on("s7drop"))))
    if any(st["s7cur"] == "on" for st in allst):
        parts.append(_part("cur", s7_cur_svg(fr), R["cur"], keys=_akeys(start, states, steps, on("s7cur"), S7_T["cur"])))
    if any(st["s7area"] == "on" for st in allst):
        parts.append(dict(_part("area", s7_area_svg(fr), R["area"], keys=_akeys(start, states, steps, on("s7area"))),
                          geo=dict(kind="s7area", px=[list(P7(fr, *p)) for p in s7_data()["near"]["area"]])))
    if any(st["s7deb"] == "on" for st in allst):
        parts.append(dict(_part("deb", s7_deb_svg(fr), R["deb"], keys=_akeys(start, states, steps, on("s7deb"))),
                          geo=dict(kind="s7deb", n=len(s7_data()["bay"]["pts"]))))
    if any(st["s7path"] == "on" for st in allst):
        p0, p1 = s7_path_pts(fr)
        parts.append(dict(_part("path", s7_path_svg(fr), R["path"], keys=_akeys(start, states, steps, on("s7path"), S7_T["cur"])),
                          geo=dict(kind="s7path", frm=list(p0), to=list(p1))))
    if any(st["s7boom"] == "on" for st in allst):
        parts.append(dict(_part("boom", s7_boom_svg(fr), R["path"], keys=_akeys(start, states, steps, on("s7boom"))),
                          geo=dict(kind="s7boom", xy=list(P7(fr, *s7_data()["near"]["boom"])))))
    if any(st["s7pts"] != "off" for st in allst):
        parts.append(dict(_part("pts", s7_pts_svg(fr, False), R["pts"], keys=_akeys(start, states, steps, on("s7pts"))),
                          geo=dict(kind="s7pts", n=len(s7_data()["near"]["pts"]))))
        if any(st["s7pts"] == "none" for st in allst):
            parts.append(dict(_part("none", s7_pts_svg(fr, True), R["none"], keys=_akeys(start, states, steps, on("s7pts", "none"))),
                              geo=dict(kind="s7pts", n=len(s7_data()["near"]["pts"]))))
    if any(st["s7obj"] == "on" for st in allst):
        parts.append(dict(_part("obj", s7_obj_svg(), R["obj"], keys=_akeys(start, states, steps, on("s7obj"))),
                          geo=dict(kind="s7obj", n=len(S7_OBJ))))
    if any(st["s7sink"] != "off" for st in allst):
        parts.append(_part("sink_heavy", s7_sink_svg("heavy"), R["sink"],
                           keys=_akeys(start, states, steps, lambda st: st["s7sink"] in ("heavy", "all"))))
    if any(st["s7sink"] == "all" for st in allst):
        parts.append(_part("sink_light", s7_sink_svg("light"), R["sink"], keys=_akeys(start, states, steps, on("s7sink", "all"))))
    if start["switch"] == "on":
        parts.append(_switch_part("上から見ると"))
    return parts


def _s7_anchors(st):
    fr = st["s7frame"]
    d = s7_data()
    area = [P7(fr, *p) for p in d["near"]["area"]]
    an = dict(area=(sum(p[0] for p in area) / len(area), sum(p[1] for p in area) / len(area)),
              area_e=max(area, key=lambda p: p[0]), area_n=min(area, key=lambda p: p[1]),
              boom=P7(fr, *d["near"]["boom"]), drop=P7(fr, *d["fig15"]["ellipse"]["c"]))
    p0, p1 = s7_path_pts(fr)
    an["path"] = ((p0[0] * 2 + p1[0]) / 3, (p0[1] * 2 + p1[1]) / 3)
    pts = [P7(fr, *p) for p in d["near"]["pts"].values()]
    an["pts"] = max(pts, key=lambda p: p[0] - p[1])
    an["deb"] = P7(fr, *d["bay"]["pts"]["16"][:2])
    cur = d["fig15"]["arrows"][0]["ll"]
    an["cur"] = P7(fr, *cur[len(cur) // 2])
    for k, (cx, cy) in _s7_obj_cells().items():
        an[k] = (cx, cy)
    return an


def _s7_note(st0, states):
    if st0["s7frame"] == "area":
        return "海岸線と点は付図-21 から・人は描かない"
    return "海岸線は Natural Earth・点と線は付図-20・付図-21・解説の図15 から（位置は目安）"


# ══════════════════════════════════════════════════════════
#  型の表へ登録（illu.py の末尾から読まれる）
# ══════════════════════════════════════════════════════════
def register():
    IL.FIELDS.update(
        S1=dict(view="side", s1cab="off", s1ck="off", s1mask="off", s1press="off", s1bulk="off", s1ring="off", s1fin="on",
                switch="off", cam=1.0),
        S2=dict(view="top", s2t=S2_T0, s2plane="on", s2yok="off", s2kum="off", s2lines="off", s2ngo="off", s2ring="off",
                s2crash="off", switch="off", cam=1.0),
        S3=dict(view="side", s3wave="off", s3amp="off", s3pitch="off", s3roll="off", switch="off", cam=1.0),
        # 🆕 ⑤b-4
        S4=dict(view="top", s4wit="off", s4glow="off", s4n="0", s4m="0", s4yok="off", s4ring="off", s4dawn="off", switch="off",
                cam=1.0),
        S5=dict(view="side", s5frame="tail", s5press="off", s5tailp="off", s5bulk="on", s5air="off", s5finair="off", s5cone="on",
                s5fin="on", s5rud="on", s5hyd="off", switch="off", cam=1.0),
        S6=dict(view="side", s6kind="real", s6l18="off", s6spl="off", s6row="off", s6fil="off", switch="off", cam=1.0),
        S7=dict(view="top", s7frame="bay", s7deb="off", s7area="off", s7drop="off", s7cur="off", s7path="off", s7boom="off",
                s7pts="off", s7obj="off", s7sink="off", switch="off", cam=1.0))
    IL.CHOICES.update(s1cab=IL.ONOFF, s1ck=IL.ONOFF, s1mask=("off", "drop"), s1press=IL.ONOFF, s1bulk=IL.ONOFF,
                      s1ring=("off", "cockpit", "tail"), s1fin=("on", "lost"),
                      s2plane=IL.ONOFF, s2yok=IL.ONOFF, s2kum=IL.ONOFF, s2lines=IL.ONOFF, s2ngo=IL.ONOFF,
                      s2ring=("off", "haneda", "yokota", "both", "sagami"), s2crash=IL.ONOFF,
                      s3wave=IL.ONOFF, s3amp=IL.ONOFF, s3pitch=IL.ONOFF, s3roll=IL.ONOFF,
                      s4wit=IL.ONOFF, s4glow=IL.ONOFF, s4n=("0", "1", "2", "3", "4"), s4m=("0", "1", "2", "3"), s4yok=IL.ONOFF,
                      s4ring=IL.ONOFF, s4dawn=IL.ONOFF,
                      s5frame=("tail", "all"), s5press=IL.ONOFF, s5tailp=IL.ONOFF, s5bulk=("on", "tear", "open"), s5air=IL.ONOFF,
                      s5finair=IL.ONOFF, s5cone=IL.ONOFF, s5fin=("on", "crack", "lost"), s5rud=IL.ONOFF, s5hyd=("off", "on", "cut"),
                      s6kind=("plan", "real"), s6l18=IL.ONOFF, s6spl=IL.ONOFF, s6row=IL.ONOFF, s6fil=IL.ONOFF,
                      s7frame=("bay", "area"), s7deb=IL.ONOFF, s7area=IL.ONOFF, s7drop=IL.ONOFF, s7cur=IL.ONOFF, s7path=IL.ONOFF,
                      s7boom=IL.ONOFF, s7pts=("off", "on", "none"), s7obj=IL.ONOFF, s7sink=("off", "heavy", "all"))
    IL.VIEWS.update(S1=("side",), S2=("top",), S3=("side", "front", "both"), S4=("top",), S5=("side",), S6=("front", "side", "both"),
                    S7=("top",))
    IL.REC_FIELDS = IL.REC_FIELDS + ("s1mask", "s1press", "s1bulk", "s1fin", "s2t", "s2yok", "s2kum", "s2lines", "s2ngo", "s2crash",
                                     "s3wave", "s3amp", "s3pitch", "s3roll",
                                     "s4wit", "s4glow", "s4n", "s4m", "s4yok", "s4ring", "s4dawn",
                                     "s5press", "s5tailp", "s5bulk", "s5air", "s5finair", "s5cone", "s5fin", "s5rud", "s5hyd",
                                     "s6l18", "s6spl", "s6row", "s6fil",
                                     "s7deb", "s7area", "s7drop", "s7cur", "s7path", "s7boom", "s7pts", "s7obj", "s7sink")
    IL.NOTE.update(S1=_s1_note, S2=_s2_note, S3=_s3_note, S4=_s4_note, S5=_s5_note, S6=_s6_note, S7=_s7_note)
    IL.EXTRA.update(
        S1=dict(scene=_scene_S1, anchors=_s1_anchors, camc=lambda st0, states: (960.0, 540.0), label=lambda st0, states: LAB["S1"]),
        S2=dict(scene=_scene_S2, anchors=_s2_anchors, camc=lambda st0, states: (960.0, 500.0), label=lambda st0, states: LAB["S2"],
                mpp=1000.0 / S2_S, mend=_s2_mend),
        S3=dict(scene=_scene_S3, anchors=_s3_anchors, camc=lambda st0, states: (960.0, 520.0),
                label=lambda st0, states: LAB["S3"][st0["view"]]),
        S4=dict(scene=_scene_S4, anchors=_s4_anchors, camc=lambda st0, states: S4_C, label=lambda st0, states: LAB["S4"],
                mpp=1000.0 / S4_K),
        S5=dict(scene=_scene_S5, anchors=_s5_anchors, camc=lambda st0, states: P5(60.0, 4.0) if st0["s5frame"] == "tail" else (960.0, 540.0),
                label=lambda st0, states: LAB["S5"][st0["s5frame"]]),
        S6=dict(scene=_scene_S6, anchors=_s6_anchors, camc=lambda st0, states: (960.0, 480.0),
                label=lambda st0, states: LAB["S6"][st0["view"]]),
        S7=dict(scene=_scene_S7, anchors=_s7_anchors, camc=lambda st0, states: S7_VIEW[st0["s7frame"]]["px"],
                label=lambda st0, states: LAB["S7"], mpp=1000.0 / S7_VIEW["area"]["k"]))


register()
