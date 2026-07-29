# -*- coding: utf-8 -*-
"""冒頭30秒の本編フレームを8枚出す（＝4カット × カット内2状態）。

設計の根拠は Vault `Resources/参考-HSS秒単位分解-20260728.md`（実測）。
  ・1カット 7.4秒 ＝ 台本の1文。4カットで29.6秒
  ・見出しは章単位でなく **毎カット** 替わる。名詞句で書く
  ・背景は7種で足りる。ここでは キッチン／ラボ／リビング の3種、ラボは2回使い回す
  ・「日常＝キッチン・リビング」「解説＝ラボ」の2チャンネルを行き来する
  ・字幕は黄（強調語）＋白。黒の太縁
  ・カット内は静止画でなく **部品差し替え**（表情・小道具・字幕が替わる。ズームはしない）

台本の構文もHSSの冒頭をそのまま移した：
  1〜3カット目で「常識の否定 → 意外な臓器 → 当事者の絵」を出し、
  4カット目で **答えを先送りして話題を横に飛ばす**（開いた輪を2つ作って閉じない）。
"""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import anatomy as A
import character as C
import render

W, H = 1920, 1080
HERE = Path(__file__).parent.parent
FONTS = Path(r"C:\Users\konar\Desktop\zankoku-sekkeizu\public\fonts")

INK = C.INK
CREAM = "#f7f0e0"
ACCENT = "#b5442c"
HORIZON = 700          # 壁と床の境。家具の足はここより下に接地させる


def face_css(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


# ── 背景 ──────────────────────────────────────────────────
# 「壁＋床＋家具3つ」では足りない（2026-07-28指摘）。
# 参考動画の背景は、家具のほかに**小物が10個前後**置いてあり、壁にも柄や額が入っている。
# 生活の場に見えるかどうかは小物の数で決まるので、1画面あたり小物を15点以上置く。

def _wall(top, bot, floor, floorline=True):
    g = (f'<rect width="{W}" height="{HORIZON}" fill="{top}"/>'
         f'<rect y="{HORIZON}" width="{W}" height="{H - HORIZON}" fill="{floor}"/>'
         f'<rect y="{HORIZON - 26}" width="{W}" height="26" fill="{bot}" '
         f'stroke="{INK}" stroke-width="5" opacity="0.85"/>')
    if floorline:      # 床板の目地。床がのっぺりした色面になるのを防ぐ
        g += "".join(f'<path d="M{-200 + i * 210} {H} L{100 + i * 150} {HORIZON}" '
                     f'stroke="{INK}" stroke-width="3" opacity="0.13"/>' for i in range(14))
    return g


# ── 使い回す小物 ──────────────────────────────────────────

def _books(x, y, n, h=76, seed=3):
    """棚に並べる本。厚みと高さと色をばらす。"""
    cols = ["#a4553f", "#5b7a86", "#8d7a4e", "#7b5f7d", "#5f7d5c", "#b08a4e"]
    out, cx, s = [], x, seed * 7919 + 13
    for i in range(n):
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        w = 16 + (s >> 9) % 16
        s = (s * 1103515245 + 12345) & 0x7FFFFFFF
        hh = h - (s >> 9) % 22
        lean = 0 if i != n - 1 else 10
        out.append(f'<g transform="translate({cx},{y}) rotate({lean})">'
                   f'<rect x="0" y="{-hh}" width="{w}" height="{hh}" rx="3" '
                   f'fill="{cols[(i + seed) % len(cols)]}" stroke="{INK}" stroke-width="4"/>'
                   f'<rect x="3" y="{-hh + 8}" width="{w - 6}" height="6" rx="2" '
                   f'fill="#fff" opacity="0.35"/></g>')
        cx += w + 2
    return "".join(out)


def _jar(x, y, s=1.0, col="#c9b06a", lid=True):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-26 -54 v44 q0 14 26 14 q26 0 26 -14 v-44 Z" fill="{col}" '
            f'fill-opacity="0.75" stroke="{INK}" stroke-width="5"/>'
            + (f'<rect x="-30" y="-64" width="60" height="14" rx="5" fill="#9a8a72" '
               f'stroke="{INK}" stroke-width="5"/>' if lid else "") + '</g>')


def _plant(x, y, s=1.0):
    leaves = "".join(
        f'<path d="M0 -20 Q{dx} {dy} {dx * 1.5:.0f} {dy - 24}" fill="none" stroke="#6f8f5c" '
        f'stroke-width="16" stroke-linecap="round"/>'
        for dx, dy in [(-42, -46), (-18, -70), (12, -74), (40, -50), (-30, -22), (34, -20)])
    return (f'<g transform="translate({x},{y}) scale({s})">{leaves}'
            f'<path d="M-38 -22 h76 l-10 60 q-2 12 -28 12 q-26 0 -28 -12 Z" fill="#b07a56" '
            f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
            f'<rect x="-42" y="-32" width="84" height="16" rx="5" fill="#c08a62" '
            f'stroke="{INK}" stroke-width="6"/></g>')


def _frame(x, y, w=140, h=110, inner="#cbd8dd", art=""):
    return (f'<g transform="translate({x},{y})">'
            f'<rect width="{w}" height="{h}" rx="6" fill="#8d7250" stroke="{INK}" '
            f'stroke-width="6"/>'
            f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" fill="{inner}" '
            f'stroke="{INK}" stroke-width="4"/>{art}</g>')


def _clock(x, y, r=44):
    return (f'<g transform="translate({x},{y})">'
            f'<circle r="{r}" fill="#f6efe0" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M0 0 V{-r * 0.6:.0f} M0 0 L{r * 0.42:.0f} {r * 0.22:.0f}" '
            f'stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
            f'<circle r="4" fill="{INK}"/></g>')


def bg_kitchen():
    """キッチン。上の吊り戸棚・カウンター・コンロ・冷蔵庫。"""
    counter = (f'<g><rect x="0" y="{HORIZON - 130}" width="1180" height="34" rx="8" '
               f'fill="#cdb894" stroke="{INK}" stroke-width="6"/>'
               f'<rect x="0" y="{HORIZON - 96}" width="1180" height="{96}" fill="#e4d7bd" '
               f'stroke="{INK}" stroke-width="5"/>'
               f'<path d="M300 {HORIZON - 96} V{HORIZON} M760 {HORIZON - 96} V{HORIZON}" '
               f'stroke="{INK}" stroke-width="5" opacity="0.45"/></g>')
    cabinet = (f'<g><rect x="60" y="150" width="900" height="230" rx="10" fill="#d7c3a0" '
               f'stroke="{INK}" stroke-width="6"/>'
               f'<path d="M360 150 V380 M660 150 V380" stroke="{INK}" stroke-width="5" '
               f'opacity="0.5"/>'
               f'<rect x="330" y="250" width="60" height="12" rx="6" fill="{INK}" opacity="0.6"/>'
               f'<rect x="630" y="250" width="60" height="12" rx="6" fill="{INK}" opacity="0.6"/></g>')
    stove = (f'<g transform="translate(430,{HORIZON - 150})">'
             f'<rect width="230" height="22" rx="7" fill="#8f857a" stroke="{INK}" stroke-width="6"/>'
             f'<circle cx="66" cy="11" r="26" fill="#5f574d" stroke="{INK}" stroke-width="5"/>'
             f'<circle cx="164" cy="11" r="26" fill="#5f574d" stroke="{INK}" stroke-width="5"/></g>')
    fridge = (f'<g transform="translate(1580,196)">'
              f'<rect width="300" height="{HORIZON + 40 - 196}" rx="16" fill="#e8e2d6" '
              f'stroke="{INK}" stroke-width="7"/>'
              f'<path d="M0 190 h330" stroke="{INK}" stroke-width="6"/>'
              f'<rect x="256" y="118" width="14" height="56" rx="7" fill="{INK}" opacity="0.65"/>'
              f'<rect x="256" y="212" width="14" height="76" rx="7" fill="{INK}" opacity="0.65"/></g>')
    return _wall("#efe6d2", "#ded0b3", "#c9b492") + cabinet + counter + stove + fridge


def bg_kitchen2():
    """キッチン（作り込み版）。タイル壁・吊り戸棚・調理台・シンク・冷蔵庫＋小物15点。

    ■ 置き場所の決め方（初稿で全部やらかした）
      ・キャラの立ち位置（x≈470）の前後 ±150 には背の高い物を置かない。コンロが頭に隠れた
      ・画面上端 y<160 は見出しの帯。時計を置くと切られる
      ・主役の図（腎臓）を置く区画は、あらかじめ**無地のタイル壁だけ**にして空けておく
      ・鉢植えは床に接地させる。宙に浮くと何なのか分からなくなる
    """
    top = HORIZON - 130
    # タイルの目地。壁を無地にしないだけで「台所」に見える
    CAB_R, CNT_R = 1150, 1180        # 吊り戸棚と調理台の右端
    tiles = "".join(f'<path d="M0 {y} H1712" stroke="{INK}" stroke-width="3" opacity="0.12"/>'
                    for y in range(400, top, 46))
    tiles += "".join(f'<path d="M{x} 400 V{top}" stroke="{INK}" stroke-width="3" '
                     f'opacity="0.12"/>' for x in range(0, 1712, 62))
    cabinet = (f'<g><rect x="20" y="150" width="{CAB_R - 20}" height="238" rx="10" '
               f'fill="#d7c3a0" stroke="{INK}" stroke-width="6"/>'
               + "".join(f'<path d="M{x} 150 V388" stroke="{INK}" stroke-width="5" '
                         f'opacity="0.45"/>' for x in (300, 580, 860))
               + "".join(f'<rect x="{x}" y="256" width="54" height="12" rx="6" fill="{INK}" '
                         f'opacity="0.55"/>' for x in (266, 546, 826, 1076))
               # 右端はガラス扉にして中の食器を見せる
               + f'<rect x="880" y="168" width="250" height="202" rx="6" fill="#cfe0e2" '
                 f'fill-opacity="0.5" stroke="{INK}" stroke-width="5"/>'
               + "".join(f'<rect x="{906 + i * 44}" y="{202 + (i % 2) * 74}" width="34" '
                         f'height="46" rx="4" fill="#f2ece0" stroke="{INK}" stroke-width="4"/>'
                         for i in range(5))
               + f'<path d="M880 282 h250" stroke="{INK}" stroke-width="4" opacity="0.45"/></g>')
    counter = (f'<g><rect x="0" y="{top}" width="{CNT_R}" height="34" rx="8" '
               f'fill="#cdb894" stroke="{INK}" stroke-width="6"/>'
               f'<rect x="0" y="{top + 34}" width="{CNT_R}" height="{HORIZON - top + 6}" '
               f'fill="#e4d7bd" stroke="{INK}" stroke-width="5"/>'
               + "".join(f'<path d="M{x} {top + 34} V{HORIZON + 40}" stroke="{INK}" '
                         f'stroke-width="5" opacity="0.35"/>' for x in (290, 600, 900))
               + "".join(f'<rect x="{x}" y="{top + 74}" width="52" height="11" rx="5" '
                         f'fill="{INK}" opacity="0.45"/>' for x in (110, 420, 730, 1030)) + '</g>')
    # コンロは左端へ。キャラ(x≈470)の後ろに置くと鍋が頭で隠れる
    stove = (f'<g transform="translate(60,{top - 18})">'
             f'<rect width="220" height="22" rx="7" fill="#8f857a" stroke="{INK}" stroke-width="6"/>'
             f'<circle cx="62" cy="11" r="25" fill="#5f574d" stroke="{INK}" stroke-width="5"/>'
             f'<circle cx="158" cy="11" r="25" fill="#5f574d" stroke="{INK}" stroke-width="5"/>'
             f'<g transform="translate(62,-32)"><path d="M-34 0 h68 q8 0 6 14 '
             f'q-4 26 -40 26 q-36 0 -40 -26 q-2 -14 6 -14 Z" fill="#9db3bb" stroke="{INK}" '
             f'stroke-width="5"/><path d="M34 6 q22 4 20 22" fill="none" stroke="{INK}" '
             f'stroke-width="5"/><path d="M-16 0 q16 -16 32 0" fill="none" stroke="{INK}" '
             f'stroke-width="5"/></g></g>')
    sink = (f'<g transform="translate(640,{top})">'
            f'<rect x="0" y="-2" width="240" height="32" rx="8" fill="#b9c3c4" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="M118 -2 v-64 q0 -22 34 -22 q34 0 34 22 v16" fill="none" '
            f'stroke="#9aa4a6" stroke-width="12" stroke-linecap="round"/></g>')
    board = (f'<g transform="translate(920,{top - 10})"><rect width="118" height="12" rx="5" '
             f'fill="#c39a63" stroke="{INK}" stroke-width="5"/></g>')
    knives = (f'<g transform="translate(1064,{top - 64})">'
              f'<path d="M0 64 v-50 q0 -14 16 -14 h34 q16 0 16 14 v50 Z" fill="#9a7a56" '
              f'stroke="{INK}" stroke-width="5"/>'
              + "".join(f'<path d="M{14 + i * 16} 0 v-30" stroke="{INK}" stroke-width="7" '
                        f'stroke-linecap="round"/>' for i in range(3)) + '</g>')
    fridge = (f'<g transform="translate(1706,172)">'
              f'<rect width="268" height="{HORIZON + 62 - 172}" rx="16" fill="#e8e2d6" '
              f'stroke="{INK}" stroke-width="7"/>'
              f'<path d="M0 202 h268" stroke="{INK}" stroke-width="6"/>'
              f'<rect x="226" y="128" width="14" height="56" rx="7" fill="{INK}" opacity="0.6"/>'
              f'<rect x="226" y="226" width="14" height="76" rx="7" fill="{INK}" opacity="0.6"/>'
              f'<rect x="38" y="70" width="74" height="54" rx="4" fill="#e8cf7a" '
              f'stroke="{INK}" stroke-width="4"/></g>')
    jars = (_jar(830, top - 4, 0.58, "#c9b06a") + _jar(880, top - 4, 0.5, "#a4553f"))
    # x 1180〜1690 は主役の図（腎臓）を置く区画。無地のタイル壁のままにしておく
    return (_wall("#efe6d2", "#ded0b3", "#c9b492") + tiles + cabinet + counter
            + stove + sink + board + knives + jars + fridge
            + _plant(1250, HORIZON + 118, 0.82))


def bg_lab():
    """ラボ。棚のガラス器具・カウンター・顕微鏡。解説モードはここへ飛ぶ。"""
    shelf = [f'<rect x="90" y="{y}" width="1080" height="16" rx="6" fill="#bfae90" '
             f'stroke="{INK}" stroke-width="5"/>' for y in (250, 430)]
    glass = []
    for i, (x, kind, col) in enumerate([
            (150, "flask", "#8fb0a4"), (270, "beaker", "#c9b06a"), (380, "tube", "#b98c92"),
            (500, "flask", "#8aa3bd"), (640, "beaker", "#9db684"), (760, "tube", "#c2a06c"),
            (890, "flask", "#a894bb"), (1030, "beaker", "#8fb0a4")]):
        y = 250 if i % 2 == 0 else 430
        if kind == "flask":
            g = (f'<path d="M-13 -74 h26 v30 l30 62 q6 16 -12 16 h-62 q-18 0 -12 -16 l30 -62 Z" '
                 f'fill="{col}" fill-opacity="0.55" stroke="{INK}" stroke-width="5"/>')
        elif kind == "beaker":
            g = (f'<path d="M-28 -66 v52 q0 16 28 16 q28 0 28 -16 v-52 Z" fill="{col}" '
                 f'fill-opacity="0.55" stroke="{INK}" stroke-width="5"/>')
        else:
            g = (f'<path d="M-13 -78 v54 q0 14 13 14 q13 0 13 -14 v-54 Z" fill="{col}" '
                 f'fill-opacity="0.55" stroke="{INK}" stroke-width="5"/>')
        glass.append(f'<g transform="translate({x},{y})">{g}</g>')
    # カウンターは低く置く。高くするとキャラの首を横切って「カウンターの向こうの人」に見える
    top = HORIZON - 46
    counter = (f'<rect x="0" y="{top}" width="{W}" height="26" rx="8" fill="#a9bcc0" '
               f'stroke="{INK}" stroke-width="6"/>'
               f'<rect x="0" y="{top + 26}" width="{W}" height="120" fill="#cfdcdd" '
               f'stroke="{INK}" stroke-width="5"/>'
               f'<path d="M420 {top + 26} V{top + 146} M1120 {top + 26} V{top + 146}" '
               f'stroke="{INK}" stroke-width="5" opacity="0.4"/>')
    # 顕微鏡。台・アーム・鏡筒・ステージの4つが無いと顕微鏡に見えない
    scope = (f'<g transform="translate(1680,{top})">'
             f'<path d="M-62 0 h124 q8 0 8 -10 q0 -12 -16 -14 h-108 q-16 2 -16 14 q0 10 8 10 Z" '
             f'fill="#78848a" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<path d="M28 -24 q34 -20 34 -70 q0 -46 -34 -62" fill="none" stroke="#78848a" '
             f'stroke-width="20" stroke-linecap="round"/>'
             f'<rect x="-56" y="-84" width="86" height="16" rx="5" fill="#8f9ba1" '
             f'stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-30 -180 h44 v66 l-16 26 h-12 l-16 -26 Z" fill="#8f9ba1" '
             f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<rect x="-34" y="-206" width="52" height="30" rx="8" fill="#6f7b81" '
             f'stroke="{INK}" stroke-width="6"/></g>')
    return (_wall("#e6ecea", "#cfdad7", "#bcc9c6") + "".join(shelf) + "".join(glass)
            + counter + scope)


def bg_lab2():
    """ラボ（作り込み版）。棚2段・ガラス器具・本・箱・人体図の掲示・作業台・顕微鏡。

    理科室らしさはガラス器具の数より**掲示物と本**で出る。器具だけ並べると看板に見える。
    キャラは cut2 が x≈1370、cut4 が x≈430。図解ボード(x 200〜760)と脳(x 1100〜1480)も
    重なるので、棚の小物は隠れても成立する配置にする。
    """
    top = HORIZON - 46
    wall = _wall("#e6ecea", "#cfdad7", "#bcc9c6")
    panel = (f'<rect y="470" width="{W}" height="10" fill="{INK}" opacity="0.10"/>'
             + "".join(f'<path d="M{x} 470 V{HORIZON - 26}" stroke="{INK}" stroke-width="3" '
                       f'opacity="0.07"/>' for x in range(0, W, 96)))
    shelves, items = [], []
    for sy in (214, 372):
        shelves.append(f'<rect x="50" y="{sy}" width="1420" height="15" rx="6" '
                       f'fill="#bfae90" stroke="{INK}" stroke-width="5"/>')
        for bx in (150, 780, 1450):
            shelves.append(f'<path d="M{bx} {sy + 15} v26 h-18 z" fill="#a8987c" '
                           f'stroke="{INK}" stroke-width="4"/>')
    kit = [(110, "flask", "#8fb0a4"), (196, "beaker", "#c9b06a"), (268, "tube", "#b98c92"),
           (330, "tube", "#8aa3bd"), (610, "flask", "#8aa3bd"), (700, "beaker", "#9db684"),
           (1024, "tube", "#c2a06c"), (1086, "tube", "#a894bb"), (1156, "flask", "#a894bb"),
           (1440, "beaker", "#8fb0a4"), (1520, "flask", "#c2a06c"), (1300, "tube", "#9db684"),
           (1396, "beaker", "#b98c92")]
    for i, (x, kind, col) in enumerate(kit):
        sy = 214 if i % 2 == 0 else 372
        if kind == "flask":
            g = (f'<path d="M-12 -70 h24 v28 l28 58 q6 15 -11 15 h-58 q-17 0 -11 -15 l28 -58 Z" '
                 f'fill="{col}" fill-opacity="0.6" stroke="{INK}" stroke-width="5"/>'
                 f'<path d="M-24 -4 h48" stroke="{col}" stroke-width="10" opacity="0.8"/>')
        elif kind == "beaker":
            g = (f'<path d="M-26 -62 v48 q0 15 26 15 q26 0 26 -15 v-48 Z" fill="{col}" '
                 f'fill-opacity="0.6" stroke="{INK}" stroke-width="5"/>'
                 f'<path d="M-22 -26 h44" stroke="{col}" stroke-width="10" opacity="0.8"/>')
        else:
            g = (f'<path d="M-12 -74 v52 q0 13 12 13 q12 0 12 -13 v-52 Z" fill="{col}" '
                 f'fill-opacity="0.6" stroke="{INK}" stroke-width="5"/>')
        items.append(f'<g transform="translate({x},{sy})">{g}</g>')
    items.append(_books(410, 214, 6, 74, 2))
    items.append(_books(776, 372, 5, 68, 5))
    items.append(_books(1216, 214, 5, 70, 9))
    items.append(_jar(1348, 214, 0.5, "#9db684"))
    items.append(_jar(896, 214, 0.5, "#b98c92"))
    for bx, by in ((530, 372), (1180, 372)):
        items.append(f'<g transform="translate({bx},{by})"><rect x="-42" y="-58" width="84" '
                     f'height="58" rx="6" fill="#c0ab86" stroke="{INK}" stroke-width="5"/>'
                     f'<path d="M-42 -34 h84" stroke="{INK}" stroke-width="4" opacity="0.5"/></g>')
    chart = _frame(1544, 176, 330, 264, "#eef0e6",
                   f'<g transform="translate(165,140)">'
                   f'<ellipse cy="-50" rx="19" ry="23" fill="none" stroke="{INK}" '
                   f'stroke-width="5"/>'
                   f'<path d="M0 -27 V32 M0 -13 l-34 28 M0 -13 l34 28 M0 32 l-24 40 '
                   f'M0 32 l24 40" fill="none" stroke="{INK}" stroke-width="5" '
                   f'stroke-linecap="round"/></g>')
    counter = (f'<rect x="0" y="{top}" width="{W}" height="26" rx="8" fill="#a9bcc0" '
               f'stroke="{INK}" stroke-width="6"/>'
               f'<rect x="0" y="{top + 26}" width="{W}" height="150" fill="#cfdcdd" '
               f'stroke="{INK}" stroke-width="5"/>'
               + "".join(f'<path d="M{x} {top + 26} V{top + 176}" stroke="{INK}" '
                         f'stroke-width="5" opacity="0.35"/>' for x in (400, 800, 1200, 1600))
               + "".join(f'<rect x="{x}" y="{top + 76}" width="50" height="11" rx="5" '
                         f'fill="{INK}" opacity="0.4"/>' for x in (170, 570, 970, 1370, 1770)))
    scope = (f'<g transform="translate(1706,{top})">'
             f'<path d="M-60 0 h120 q8 0 8 -10 q0 -12 -16 -14 h-104 q-16 2 -16 14 q0 10 8 10 Z" '
             f'fill="#78848a" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<path d="M28 -24 q34 -20 34 -70 q0 -46 -34 -62" fill="none" stroke="#78848a" '
             f'stroke-width="20" stroke-linecap="round"/>'
             f'<rect x="-56" y="-84" width="86" height="16" rx="5" fill="#8f9ba1" '
             f'stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-30 -180 h44 v66 l-16 26 h-12 l-16 -26 Z" fill="#8f9ba1" '
             f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
             f'<rect x="-34" y="-206" width="52" height="30" rx="8" fill="#6f7b81" '
             f'stroke="{INK}" stroke-width="6"/></g>')
    rack = (f'<g transform="translate(1150,{top - 56})">'
            f'<rect y="34" width="130" height="22" rx="6" fill="#9a8a72" stroke="{INK}" '
            f'stroke-width="5"/>'
            + "".join(f'<path d="M{18 + i * 32} 34 v-40 q0 -10 12 -10 q12 0 12 10 v40 Z" '
                      f'fill="#b98c92" fill-opacity="0.65" stroke="{INK}" stroke-width="4"/>'
                      for i in range(3)) + '</g>')
    papers = (f'<g transform="translate(886,{top - 2})">'
              f'<rect x="0" y="-16" width="126" height="16" rx="3" fill="#f4efe2" '
              f'stroke="{INK}" stroke-width="5"/>'
              f'<rect x="-8" y="-26" width="126" height="14" rx="3" fill="#fbf7ec" '
              f'stroke="{INK}" stroke-width="5"/></g>')
    return (wall + panel + chart + "".join(shelves) + "".join(items)
            + counter + scope + rack + papers)


def bg_living():
    """リビング。ソファ・低いテーブル・スタンド。家具は必ず床に接地させる。"""
    sofa = (f'<g transform="translate(96,{HORIZON - 230})">'
            f'<path d="M0 290 V96 q0 -34 36 -34 h392 q36 0 36 34 V290 Z" fill="#a98d6d" '
            f'stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M16 290 V152 q0 -26 30 -26 h380 q30 0 30 26 V290 Z" fill="#c0a483" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="M54 152 h372" fill="none" stroke="{INK}" stroke-width="5" opacity="0.4"/></g>')
    table = (f'<g transform="translate(1230,{HORIZON + 96})">'
             f'<rect x="0" y="0" width="330" height="24" rx="9" fill="#b98d5c" '
             f'stroke="{INK}" stroke-width="6"/>'
             f'<rect x="28" y="24" width="18" height="96" rx="7" fill="#a67d4e" '
             f'stroke="{INK}" stroke-width="6"/>'
             f'<rect x="284" y="24" width="18" height="96" rx="7" fill="#a67d4e" '
             f'stroke="{INK}" stroke-width="6"/></g>')
    lamp = (f'<g transform="translate(1760,0)">'
            f'<rect x="-9" y="360" width="18" height="{HORIZON + 34 - 360}" fill="#8d7a5e" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="0" cy="{HORIZON + 36}" rx="62" ry="16" fill="#8d7a5e" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-78 366 L-50 258 h100 l28 108 Z" fill="#e3d3ae" stroke="{INK}" '
            f'stroke-width="7" stroke-linejoin="round"/></g>')
    window = (f'<g transform="translate(1180,170)">'
              f'<rect width="380" height="300" rx="10" fill="#bcd2d8" stroke="{INK}" '
              f'stroke-width="7"/><path d="M190 0 V300 M0 150 h380" stroke="{INK}" '
              f'stroke-width="6" opacity="0.7"/></g>')
    return _wall("#e7dcc6", "#d8c9ad", "#c2a179") + window + lamp + sofa + table


def bg_living2():
    """リビング（作り込み版）。ソファ・ラグ・低いテーブル・スタンド・額2枚・窓とカーテン・観葉植物。

    キャラは cut3 が x≈820（拡大1.28）で、頭の左右 x 656/1036・y 420 に痛みの記号が出る。
    その帯には壁の物を置かない。家具はすべて床に接地させる。
    """
    wall = _wall("#e7dcc6", "#d8c9ad", "#c2a179")
    # 腰壁。上下で壁紙を変えるだけで部屋の奥行きが出る
    rail = (f'<rect y="472" width="{W}" height="{HORIZON - 26 - 472}" fill="#dfd0b2"/>'
            f'<rect y="464" width="{W}" height="14" rx="5" fill="#c6b18c" '
            f'stroke="{INK}" stroke-width="5"/>')
    stripe = "".join(f'<path d="M{x} 0 V464" stroke="{INK}" stroke-width="3" opacity="0.06"/>'
                     for x in range(0, W, 74))
    # ラグは楕円でなく台形にする。楕円だと床にできた茶色い水たまりに見えた
    rug = (f'<g><path d="M320 872 H960 L1090 1046 H182 Z" fill="#b08a72" '
           f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
           f'<path d="M368 900 H912 L1016 1018 H262 Z" fill="none" '
           f'stroke="{INK}" stroke-width="5" opacity="0.32"/></g>')
    sofa = (f'<g transform="translate(70,{HORIZON - 236})">'
            f'<path d="M0 292 V-6 q0 -34 36 -34 h432 q36 0 36 34 V292 Z" fill="#a98d6d" '
            f'stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M16 292 V152 q0 -26 30 -26 h420 q30 0 30 26 V292 Z" fill="#c0a483" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="M256 152 V292" stroke="{INK}" stroke-width="5" opacity="0.35"/>'
            # クッション2つ。これがあるだけで「使っているソファ」に見える
            f'<g transform="translate(96,196) rotate(-8)"><rect x="-46" y="-46" width="92" '
            f'height="92" rx="14" fill="#cf9f72" stroke="{INK}" stroke-width="6"/></g>'
            f'<g transform="translate(388,196) rotate(7)"><rect x="-46" y="-46" width="92" '
            f'height="92" rx="14" fill="#8fa587" stroke="{INK}" stroke-width="6"/></g>'
            f'<path d="M40 292 v40 M464 292 v40" stroke="{INK}" stroke-width="14" '
            f'stroke-linecap="round"/></g>')
    frames = (_frame(150, 196, 156, 124, "#cbd8dd",
                     f'<path d="M22 96 q34 -46 62 -20 q30 26 50 -30" fill="none" '
                     f'stroke="{INK}" stroke-width="5"/>')
              + _frame(346, 232, 128, 100, "#e0d0b8",
                       f'<circle cx="64" cy="50" r="26" fill="none" stroke="{INK}" '
                       f'stroke-width="5"/>'))
    table = (f'<g transform="translate(1210,{HORIZON + 96})">'
             f'<rect x="0" y="0" width="340" height="24" rx="9" fill="#b98d5c" '
             f'stroke="{INK}" stroke-width="6"/>'
             f'<rect x="28" y="24" width="18" height="98" rx="7" fill="#a67d4e" '
             f'stroke="{INK}" stroke-width="6"/>'
             f'<rect x="294" y="24" width="18" height="98" rx="7" fill="#a67d4e" '
             f'stroke="{INK}" stroke-width="6"/>'
             # マグと本
             f'<g transform="translate(72,-40)"><path d="M-26 0 h52 v34 q0 12 -26 12 '
             f'q-26 0 -26 -12 Z" fill="#e2e0d4" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M26 8 q20 4 18 16 q-2 12 -18 12" fill="none" stroke="{INK}" '
             f'stroke-width="5"/></g>'
             f'<g transform="translate(230,-18)"><rect x="-46" y="-14" width="92" height="14" '
             f'rx="3" fill="#8d6a86" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="-40" y="-26" width="92" height="14" rx="3" fill="#6f8a94" '
             f'stroke="{INK}" stroke-width="5"/></g></g>')
    lamp = (f'<g transform="translate(1806,0)">'
            f'<rect x="-9" y="348" width="18" height="{HORIZON + 34 - 348}" fill="#8d7a5e" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="0" cy="{HORIZON + 36}" rx="62" ry="16" fill="#8d7a5e" '
            f'stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-78 354 L-50 246 h100 l28 108 Z" fill="#e3d3ae" stroke="{INK}" '
            f'stroke-width="7" stroke-linejoin="round"/></g>')
    window = (f'<g transform="translate(1216,168)">'
              f'<rect width="360" height="286" rx="10" fill="#bcd2d8" stroke="{INK}" '
              f'stroke-width="7"/>'
              f'<path d="M0 196 q84 -52 178 -24 q92 28 182 -14 V286 H0 Z" fill="#9dbb92"/>'
              f'<path d="M180 0 V286 M0 143 h360" stroke="{INK}" stroke-width="6" '
              f'opacity="0.7"/>'
              # カーテン
              f'<path d="M-34 -16 q26 150 0 306 h-46 V-16 Z" fill="#c98f7c" '
              f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
              f'<path d="M394 -16 q-26 150 0 306 h46 V-16 Z" fill="#c98f7c" '
              f'stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>'
              f'<rect x="-92" y="-30" width="544" height="16" rx="7" fill="#8d7250" '
              f'stroke="{INK}" stroke-width="5"/></g>')
    return (wall + stripe + rail + window + frames + rug + sofa + table + lamp
            + _plant(1660, HORIZON + 132, 0.92) + _clock(1000, 250, 46))


# ── 画面の部品 ────────────────────────────────────────────

def headline(text):
    """毎カット替わる大見出し。名詞句で書く（動詞で終わる文にしない）。"""
    return (f'<text x="{W // 2}" y="132" font-family="Dela" font-size="88" fill="{INK}" '
            f'text-anchor="middle" stroke="{CREAM}" stroke-width="18" '
            f'stroke-linejoin="round" paint-order="stroke fill">{text}</text>')


def subtitle(lines):
    """字幕。(強調語, 残り) の組を1〜2行。強調語だけ黄、残りは白。黒の太縁。"""
    out, y0 = [], 966 if len(lines) > 1 else 1006
    common = ('font-family="Noto" font-size="54" text-anchor="middle" '
              f'stroke="{INK}" stroke-width="14" stroke-linejoin="round" '
              'paint-order="stroke fill"')
    for i, (hi, rest) in enumerate(lines):
        out.append(f'<text x="{W // 2}" y="{y0 + i * 70}" {common}>'
                   f'<tspan fill="#ffd83d">{hi}</tspan><tspan fill="#fffdf6">{rest}</tspan></text>')
    return "".join(out)


def board(x, y, title, rows, w=560, h=380):
    """画面の中にボードを置いて、そこに図を描く。
    実測でいちばん多かった「絵にしにくい話の逃げ方」（分類1・約30カット/本）。"""
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#fbf6ea" '
         f'stroke="{INK}" stroke-width="8"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="92" rx="16" fill="{ACCENT}" '
         f'opacity="0.9"/>'
         f'<text x="{x + w // 2}" y="{y + 66}" font-family="Dela" font-size="52" '
         f'fill="#fffdf6" text-anchor="middle">{title}</text>']
    for i, (lab, pct, col) in enumerate(rows):
        by = y + 136 + i * 104
        g.append(f'<text x="{x + 28}" y="{by + 46}" font-family="Noto" font-size="40" '
                 f'fill="{INK}">{lab}</text>'
                 f'<rect x="{x + 216}" y="{by + 8}" width="{int(pct * (w - 256) / 100)}" '
                 f'height="54" rx="12" fill="{col}" stroke="{INK}" stroke-width="5"/>')
    return "".join(g)


def pain_mark(x, y, s=1.0):
    """痛みの記号。頭の横に置く。"""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            + "".join(f'<path d="M0 0 L{28 * dx} {28 * dy} " stroke="{ACCENT}" '
                      f'stroke-width="11" stroke-linecap="round"/>'
                      for dx, dy in [(-1.7, -0.9), (-1.1, -1.7), (0, -2.0),
                                     (1.1, -1.7), (1.7, -0.9)]) + '</g>')


def drops(x, y, n=5):
    """水滴。腎臓が塩分と水分を手放す絵。"""
    out = []
    for i in range(n):
        dx = x + (i - n // 2) * 46
        dy = y + (i % 2) * 34
        out.append(f'<path d="M{dx} {dy} c-22 30 -22 52 0 52 c22 0 22 -22 0 -52 Z" '
                   f'fill="#7fa8c4" stroke="{INK}" stroke-width="5"/>')
    return "".join(out)


def qmark(x, y):
    return (f'<text x="{x}" y="{y}" font-family="Dela" font-size="112" fill="{ACCENT}" '
            f'stroke="{CREAM}" stroke-width="14" paint-order="stroke fill" '
            f'text-anchor="middle">？</text>')


def vignette():
    return f'<rect width="{W}" height="{H}" fill="url(#vig2)"/>'


DEFS = f'''{C.defs()}{A.defs()}
  <radialGradient id="vig2" cx="50%" cy="45%" r="78%">
    <stop offset="60%" stop-color="#3a2c18" stop-opacity="0"/>
    <stop offset="100%" stop-color="#3a2c18" stop-opacity="0.16"/></radialGradient>'''


# ── 4カット × 2状態 ────────────────────────────────────────
# 見出しはカット単位、字幕とキャラの部品はカット内で替わる（＝HSSのカット内の動き）

def cut1(state):
    """キッチン。常識の否定 → 意外な臓器名。"""
    face = "normal" if state == 0 else "surprise"
    man = C.character("stand", face, costume="casual", at=(470, 1000), scale=1.12)
    # bg_kitchen2 が空けてある無地タイルの区画（x 1180〜1690）に置く
    k = (f'<g transform="translate(1306,338) scale(0.72)">{A.kidney(flip=True)}</g>'
         f'<g transform="translate(1550,338) scale(0.72)">{A.kidney()}</g>')
    glow = f'<g filter="url(#glow)" opacity="{0.0 if state == 0 else 0.95}">{k}</g>'
    sub = ([("", "砂糖をやめると、まず体重が減ると思われがちです")] if state == 0
           else [("", "ですが、最初に反応するのは"), ("腎臓", "なのです")])
    return (bg_kitchen2() + man + glow + k + (qmark(686, 470) if state == 0 else "")
            + vignette() + headline("最初に反応するのは腎臓") + subtitle(sub))


def cut2(state):
    """ラボ。解説モードへ切り替え。ボードに図を出す＝逃げ方の分類1。"""
    # 指差しの手は x+204 まで伸びる。1480 に置くと顕微鏡(1680)に指先が重なった
    man = C.character("point", "convinced" if state == 0 else "smile",
                      costume="coat", at=(1370, 1000), scale=1.05)
    rows = ([("血糖値", 88, "#c9bda4"), ("インスリン", 74, ACCENT)] if state == 0
            else [("血糖値", 38, "#c9bda4"), ("インスリン", 22, ACCENT)])
    sub = ([("", "血糖値が下がると、インスリンも下がります")] if state == 0
           else [("", "腎臓はためこんでいた"), ("塩分と水分", "を、手放しはじめます")])
    return (bg_lab2() + board(200, 250, "砂糖をやめた直後", rows)
            + (drops(880, 640, 5) if state == 1 else "") + man
            + vignette() + headline("インスリンが下がる") + subtitle(sub))


def cut3(state):
    """リビング。当事者の絵。表情と痛みの記号だけで持たせる＝逃げ方の分類6。"""
    man = C.character("stand", "pain", costume="casual", at=(820, 1010), scale=1.28)
    hx, hy = man.anchors["head"]
    sub = ([("", "この、わずかな水分の不足が")] if state == 0
           else [("", "一日目の頭痛を、"), ("いつもより重く", "感じさせています")])
    marks = "" if state == 0 else (pain_mark(hx - 190, hy - 40, 1.15)
                                   + pain_mark(hx + 190, hy - 40, 1.15))
    return (bg_living2() + man + marks
            + vignette() + headline("一日目の頭痛") + subtitle(sub))


def cut4(state):
    """ラボ（2回目・使い回し）。答えを先送りして話題を横に飛ばす。"""
    man = C.character("point", "convinced" if state == 0 else "surprise",
                      costume="coat", at=(430, 1000), scale=1.05)
    b = f'<g transform="translate(1290,530) scale(0.92)">{A.brain()}</g>'
    glow = f'<g filter="url(#glow)" opacity="{0.0 if state == 0 else 0.95}">{b}</g>'
    sub = ([("", "腎臓の話は、"), ("あとの章で", "くわしくお伝えします")] if state == 0
           else [("", "ですがその前に、もっと早く"), ("脳", "で起きることがあります")])
    return (bg_lab2() + man + glow + b
            + vignette() + headline("まず、脳で起きること") + subtitle(sub))


CUTS = [cut1, cut2, cut3, cut4]
SEC = 7.4          # 実測値。1カット＝台本の1文

if __name__ == "__main__":
    css = face_css("Dela", "DelaGothicOne.woff2") + face_css("Noto", "NotoSansJP-Bold.woff2")
    out = HERE / "out" / "open30"
    out.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:] or None
    plan = []
    for i, fn in enumerate(CUTS, 1):
        for s in (0, 1):
            name = f"c{i}{'ab'[s]}"
            plan.append({"file": f"{name}.png", "sec": SEC / 2})
            if only and name not in only:
                continue
            svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                   f'viewBox="0 0 {W} {H}"><defs>{DEFS}</defs>{fn(s)}</svg>')
            html = (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{css}'
                    f'body{{width:{W}px;height:{H}px;overflow:hidden}}</style></head>'
                    f'<body>{svg}</body></html>')
            render.png(html, out / f"{name}.png", W, H)
            print("wrote", name)
    (out / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    print("total", sum(p["sec"] for p in plan), "sec")
