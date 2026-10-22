# -*- coding: utf-8 -*-
"""illu24.py — 案C の再現イラスト：24本目（チェルノブイリ原発事故・1986-04-26・4号炉 RBMK-1000）の置き場 N1〜N4（⑤b-3・2026-10-22 新設）。

`tools/illu.py` の末尾で読み込み、型の表（FIELDS・CHOICES・VIEWS・REC_FIELDS・NOTE）と置き場の登録 `illu.EXTRA` へ足す（17本目 illu17・20本目 illu20 と同じ作り）。
🔴 置き場の名は **N1〜N4**（illu17 が C1〜C7・illu20 が S1〜S3 を登録している＝同じ名で足すと黙ってぶつかる）。
🔴 §0b（題材を替えるとき）：このファイルは24本目の型の値そのもの＝次の回は読み込みを外すか、置き場の名がぶつからないか確かめる。

■ 置き場（台本 第2版 §4 の案C・映像方針 24本目 §1 決め7・一覧 `ref/ep24/eizou_list24.md`）
  N1 … 炉の断面（c208・横から）。黒鉛の塊に縦の管（燃料と水）・上から入る棒・蒸気ドラム・ポンプ（人は描かない）。
       炉の高さと直径の比＝記録の値（S1 p16「height 7 m, diameter 11.8 m」＝1m 60画素）。管・棒・ドラム・ポンプ・配管の数と形は模式
       （S1 p113「1660 fuel channels」＝札の数・2つのループ・ドラム・ポンプの台数は描かない）。タービンは描かない（蒸気の管が画面の右の外へ）。
       欄＝n1flow（下から入る水の矢印）・n1boil（燃料の熱で沸いて蒸気）・n1rise（蒸気と水がドラムへ）・n1steam（蒸気がタービンへ＝画面の外）・switch
  N2 … 止める棒（c615＝前触れ・view top／c905＝本番・view cut）。形のもと＝Commons の CC0「RBMK positive scram.svg」（表示は任意＝書かない）、
       寸法＝INSAG-7 図1 (a) の数（吸う棒の先は炉の上の端の 20cm 上・水 125cm・押しのけ棒 450cm・水 125cm＝炉の高さ 700cm）。1cm 0.8画素。
       🔴 図1 そのものは写さない（© IAEA＝c901 で頁の引用）。(b)（事故のあとの改良）は描かない。
       欄＝n2dy（棒の下がった長さ cm＝段で増えるだけ）・n2arrow（下向きの矢印）・n2red（炉の下の方 125cm を赤く＝c905 の最後の段だけ）・switch
       top＝炉の上の方を横から（炉は不透明＝下の水と押しのけ棒は見せない）。下がった長さは記録の速さ（S1 p113「0.4 m/s」）×3秒
       （表I-I p65「01:23:40」→「01:23:43」）＝120cm まで。cut＝棒を縦に切った図（管の中が見える）。下がった長さ 125cm で押しのけ棒の下の端が炉の下の端
  N3 … 出力の時刻表（c303＝前半 view am＝4月25日 0:00〜24:00／c403＝後半 view night＝4月26日 0:00〜1:10）。時刻の軸と、時刻ごとの札（時刻と記録の値）。
       🔴 割れる時刻（200MW で止まった 1:00＝ソ連の報告／1:03＝表I-I）は札に出さない＝同じ形の目盛り2本に出典の名だけ（どちらが正しいとは描かない）。
       軸の目盛りに 1:00 を置かない（割れる時刻の字になる）。欄＝n3a（前半＝5つの札／後半＝0:05 と 200MW の割れ）・n3b（前半＝決まりの札と色／
       後半＝0:28 の急落）・n3c（後半＝試験の予定の札）
  N4 … 避難のバス（c707）。町の通りを横から（夜→27日の昼）。バスの列は画面の両端の外まで続く（数は描かない＝札「約1,200台」）。
       住民は顔の無い群れ（`illu.crowd_layout`＝門番 ② が数えられない形か見る）＝避難の時刻（14:00〜17:00＝L2 p24）の場面だけ。
       知らせの輪は模式（「broadcast」＝何で流したかは描かない）。欄＝n4bus・n4day・n4call・n4crowd
■ 守りの線（台本 §1-4・§1-5・映像方針 24本目＝門番 check_illu ㊳〜㊶ が記録の値を門番の側に持つ＝ここの定数を読まない）
  ・人は N4 の住民の顔の無い群れだけ（運転員・消防士・ボタンを押す1人は描かない）・爆発・火・煙・壊れた炉は描かない
  ・時計の札は台本 §1-5 で1つに決めた時刻だけ（`cuts.ss.ILLU_CLOCK_OK`）・数の札は記録の値だけ
"""
from __future__ import annotations

import math

import illu as IL
import titan_fig as F

W, H = IL.W, IL.H
KEY_DELAY = IL.KEY_DELAY
_part = IL._part

# ── 絵の色（全章で固定・章の色の置き換えが拾う値＝jiko_style の BG・BG2・GRID・LINE・LINE_DIM・TICK・INK_W を使わない）──
C24 = dict(
    bg0="#0d151c", bg1="#17222b", ink="#eef3f5", dim="#a7b6c0", ol="#0a0f14",
    gra="#555c63", gra_ln="#6e767e", gra_dk="#41474d",
    water="#3a8bcf", water_lo="#2f78b6", water_ln="#1c4b72", steam="#eaf0f3", bub="#f4f8fa",
    rod="#121618", rod_ln="#7f8a92", disp="#d7dbde", disp_ln="#4f575d", tele="#c0c8ce",
    lid="#20282f", lid_ln="#39434c",
    drum="#98a4ad", drum_ln="#44505a", pump="#8996a0", pump_ln="#3f4a53",
    amber="#f2c14e", red="#e0503c", green="#5cc98a", arrow="#eef3f5",
    axis="#cdd6dc", tick="#93a1ab", card="#1a2630", card_ln="#5d6d79", time="#f2c14e", doc="#9cc7ee",
    sky_n0="#060b15", sky_n1="#15223a", sky_d0="#6ea4d4", sky_d1="#c1d9ec",
    bld_n="#18232e", bld_n_win="#22303d", bld_d="#7f8d9a", bld_d_win="#687683",
    road="#384047", road_ln="#c9cfd4", gnd_n="#10171d", gnd_d="#55606a",
    bus="#c2cad0", bus_ln="#262d34", bus_win="#25303a", bus_dk="#8c969e", wheel="#141819",
    # ⑤b-3 の下見：後ろの列 #3a4651 が道 #384047 とほぼ同じ＝群れが帯に見えた → 3列とも道より暗く
    crowd0="#141b21", crowd1="#1b242c", crowd2="#232d36", ring="#f2c14e",
    # ⑤b-3 の下見：棒 #121618 が暗い地に沈み、長い一様な棒で下がる動きも見えなかった → 鋼の灰色＋継ぎ目
    steel="#64717a", steel_ln="#b1bcc3", joint="#2c343a",
)


def _d(pts, close=True):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")


def _path(pts, fill, stroke=None, sw=0.0, op=None, close=True, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<path d="{_d(pts, close)}" fill="{fill}"{st}{o}{extra}/>'


def _rect(x, y, w, h, fill, stroke=None, sw=0.0, rx=0.0, op=None, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    r = f' rx="{rx}"' if rx else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"{r} fill="{fill}"{st}{o}{extra}/>'


def _line(x1, y1, x2, y2, col, w=3.0, extra=""):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" '
            f'stroke-linecap="round"{extra}/>')


def _text(x, y, t, size=30, col=None, anchor="middle", ol=True, extra=""):
    o = (f' stroke="{C24["ol"]}" stroke-width="6" stroke-linejoin="round" paint-order="stroke fill"' if ol else "")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Noto" font-size="{size:.0f}" fill="{col or C24["ink"]}" '
            f'text-anchor="{anchor}"{o}{extra}>{F.esc(t)}</text>')


def _arrow(p, q, col, w=8.0, head=22.0):
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    b = (q[0] - head * math.cos(ang), q[1] - head * math.sin(ang))
    l = (b[0] + head * 0.55 * math.sin(ang), b[1] - head * 0.55 * math.cos(ang))
    r = (b[0] - head * 0.55 * math.sin(ang), b[1] + head * 0.55 * math.cos(ang))
    return (_line(p[0], p[1], b[0], b[1], C24["ol"], w + 5, ' opacity="0.55"') + _line(p[0], p[1], b[0], b[1], col, w)
            + _path([q, l, r], col, C24["ol"], 2.0))


def _akeys(start, states, steps, on, dur=0.6, extra=0.0):
    """濃さだけの鍵（on＝状態 → 見せるか）。段の行頭＋delay＋extra から dur 秒で"""
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


def _grow_only(place, start, states, field):
    v = float(start[field])
    for st in states:
        if float(st[field]) < v - 1e-9:
            raise ValueError(f"illu {place}：{field} は段で増えるだけ（戻さない＝棒は下がるだけ）")
        v = float(st[field])


def _switch_part(text):
    return dict(_part("switch", IL.va_switch_svg(text), "", keys=IL._switch_keys()), signal=True)


def _bg_svg(c0=None, c1=None, gid="n24bg"):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c0 or C24["bg0"]}"/>'
            f'<stop offset="1" stop-color="{c1 or C24["bg1"]}"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{gid})"/>')


def _blocks_svg(x0, y0, x1, y1, bw, bh, col, w=1.6, op=0.55):
    """黒鉛の積み木の目地（模式）"""
    g = []
    y, r = y0 + bh, 0
    while y < y1 - 2:
        g.append(_line(x0, y, x1, y, col, w, f' opacity="{op}"'))
        y += bh
    y, r = y0, 0
    while y < y1 - 2:
        x = x0 + (bw / 2 if r % 2 else 0.0)
        while x < x1:
            if x > x0 + 1:
                g.append(_line(x, y, x, min(y1, y + bh), col, w, f' opacity="{op}"'))
            x += bw
        y += bh
        r += 1
    return "".join(g)


# ══════════════════════════════════════════════════════════
#  N1 炉の断面（c208・横から）
# ══════════════════════════════════════════════════════════
N1_MPX = 60.0                                     # 1m＝60画素（S1 p16 の高さ 7m・直径 11.8m の比を保つ）
N1_CORE = dict(x0=960.0 - 5.9 * N1_MPX, x1=960.0 + 5.9 * N1_MPX, y0=330.0, y1=330.0 + 7.0 * N1_MPX)
N1_PITCH = 34.0                                   # 管の間隔（模式＝本数は 1,660 本でない）
N1_TW = 12.0                                      # 管の太さ（模式）
N1_CH = tuple(N1_CORE["x0"] + 17.0 + N1_PITCH * k for k in range(21))
N1_ROD = tuple(N1_CH[k] + N1_PITCH / 2 for k in (1, 5, 9, 13, 17))      # 棒の通り道（管と管のあいだ・模式）
N1_ROD_TOP = 206.0
N1_COLLECT_Y = 306.0                              # 管の上の集め管（模式）
N1_HEADER_Y = 795.0                               # 管の下の配り管（模式）
N1_DRUM = (140.0, 198.0, 520.0, 262.0)            # 蒸気ドラム（横置き＝S1 p113「horizontal steam separator drums」・数は模式）
N1_PUMP = (300.0, N1_HEADER_Y, 38.0)              # ポンプ（中心・半径＝模式）
N1_STEAM_Y = 174.0                                # 蒸気の管（ドラム → 画面の右の外＝タービンは描かない）
N1_LAB = "炉を横から切った図"
N1_SWITCH = "横から見ると"
N1_REC = dict(
    core="S1 p113（There were 1660 fuel channels in the vertical ducts of the graphite columns）・S1 p16（height 7 m, diameter 11.8 m）",
    ch="S1 p113（There were 1660 fuel channels in the vertical ducts of the graphite columns）",
    rod="S1 p14（The control rods and the safety rods of an RBMK reactor are inserted into the reactor core from above）",
    loop="S1 p113（The coolant is circulated by the main circulating pumps (MCPs)・The steam and water are separated in the horizontal steam separator drums）",
    flow="S1 p113（Individual pipes supply subcooled water to each channel and remove the steam-water mixture）",
    boil="S1 p113（with a graphite moderator and a boiling light water coolant）",
    steam="S1 p113（The saturated steam is sent to two turbines）",
)


def n1_core_svg():
    c = N1_CORE
    g = [_rect(c["x0"], c["y0"], c["x1"] - c["x0"], c["y1"] - c["y0"], C24["gra"], C24["gra_ln"], 3.0),
         _blocks_svg(c["x0"], c["y0"], c["x1"], c["y1"], N1_PITCH * 2, 42.0, C24["gra_dk"])]
    return "".join(g)


def n1_channels_svg():
    c = N1_CORE
    g = []
    for x in N1_CH:
        g.append(_rect(x - N1_TW / 2, c["y0"], N1_TW, c["y1"] - c["y0"], C24["water"], C24["water_ln"], 1.5))
        g.append(_line(x, c["y1"], x, N1_HEADER_Y, C24["water_lo"], 5.0))          # 下の配り管から
        g.append(_line(x, c["y0"], x, N1_COLLECT_Y, C24["water_lo"], 5.0))         # 上の集め管へ
    return "".join(g)


def n1_rods_svg():
    """上から入る棒（N2 と同じ鋼の色・⑤b-3 の試し焼き：暗い色では空の枠に見えた）"""
    g = []
    for x in N1_ROD:
        g.append(_rect(x - 6, N1_ROD_TOP, 12, N1_CORE["y0"] - N1_ROD_TOP, C24["steel"], C24["steel_ln"], 2.0))
    return "".join(g)


def n1_loop_svg():
    """配管（模式）：集め管 → ドラム／ドラム → 下り管 → ポンプ → 配り管"""
    c, (dx0, dy0, dx1, dy1), (px, py, pr) = N1_CORE, N1_DRUM, N1_PUMP
    g = [_line(N1_CH[0], N1_COLLECT_Y, N1_CH[-1], N1_COLLECT_Y, C24["water_lo"], 9.0),
         _path([(N1_CH[0], N1_COLLECT_Y), (560.0, N1_COLLECT_Y), (560.0, (dy0 + dy1) / 2), (dx1, (dy0 + dy1) / 2)], "none",
               C24["water_lo"], 9.0, close=False),
         _path([(dx0 + 70, dy1), (dx0 + 70, py), (px - pr, py)], "none", C24["water_lo"], 11.0, close=False),
         _line(px + pr, py, N1_CH[-1], py, C24["water_lo"], 11.0)]
    return "".join(g)


def n1_drum_svg():
    x0, y0, x1, y1 = N1_DRUM
    h = y1 - y0
    g = [_rect(x0, y0, x1 - x0, h, C24["drum"], C24["drum_ln"], 3.0, rx=h / 2),
         f'<clipPath id="n1dc"><rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{h:.1f}" rx="{h / 2:.1f}"/></clipPath>',
         _rect(x0, y0 + h * 0.55, x1 - x0, h * 0.45, C24["water"], extra=' clip-path="url(#n1dc)" opacity="0.9"'),
         _rect(x0, y0, x1 - x0, h, "none", C24["drum_ln"], 3.0, rx=h / 2)]
    return "".join(g)


def n1_pump_svg():
    px, py, r = N1_PUMP
    g = [f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="{C24["pump"]}" stroke="{C24["pump_ln"]}" stroke-width="3"/>']
    for k in range(4):
        a = math.radians(45 + 90 * k)
        g.append(_line(px, py, px + 0.78 * r * math.cos(a), py + 0.78 * r * math.sin(a), C24["pump_ln"], 5.0))
    g.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="7" fill="{C24["pump_ln"]}"/>')
    return "".join(g)


def n1_flow_svg():
    """下から入る水（管の下の方に上向きの矢じり・配り管の向き）"""
    c = N1_CORE
    g = []
    for x in N1_CH:
        for y in (c["y1"] - 40.0, c["y1"] - 120.0):
            g.append(_path([(x - 9, y + 7), (x, y - 5), (x + 9, y + 7)], "none", C24["water_lo"], 3.0, close=False))
            g.append(_path([(x - 6, y + 5), (x, y - 3), (x + 6, y + 5)], "none", "#cfe7fa", 2.6, close=False))
    px, py, pr = N1_PUMP
    for xa in (520.0, 1000.0):
        g.append(_arrow((xa, py), (xa + 90, py), "#cfe7fa", 5.0, 16.0))
    return "".join(g)


def n1_boil_svg():
    """燃料の熱で沸いて蒸気（管の上の方を白く・泡＝模式）"""
    c = N1_CORE
    top, mid = c["y0"], c["y0"] + 0.55 * (c["y1"] - c["y0"])
    g = [f'<defs><linearGradient id="n1bo" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{C24["water"]}" stop-opacity="0"/>'
         f'<stop offset="1" stop-color="{C24["steam"]}" stop-opacity="1"/></linearGradient></defs>']
    for k, x in enumerate(N1_CH):
        g.append(_rect(x - N1_TW / 2 + 1, top, N1_TW - 2, mid - top, "url(#n1bo)"))
        for j, y in enumerate((top + 26, top + 70, top + 120, top + 168)):
            g.append(f'<circle cx="{x + (2.5 if (j + k) % 2 else -2.5):.1f}" cy="{y + (k % 3) * 6:.1f}" r="{3.4 - 0.5 * (j % 3):.1f}" '
                     f'fill="{C24["bub"]}" stroke="{C24["water_ln"]}" stroke-width="0.8"/>')
    return "".join(g)


def n1_rise_svg():
    """蒸気と水がドラムへ（集め管と上の管を白く・矢印）"""
    (dx0, dy0, dx1, dy1) = N1_DRUM
    ym = (dy0 + dy1) / 2
    g = [_line(N1_CH[0], N1_COLLECT_Y, N1_CH[-1], N1_COLLECT_Y, C24["steam"], 6.0),
         _path([(N1_CH[0], N1_COLLECT_Y), (560.0, N1_COLLECT_Y), (560.0, ym), (dx1, ym)], "none", C24["steam"], 6.0, close=False)]
    for x in N1_CH:
        g.append(_line(x, N1_CORE["y0"], x, N1_COLLECT_Y, C24["steam"], 3.0))
    g.append(_arrow((560.0, N1_COLLECT_Y - 10), (560.0, ym + 18), C24["arrow"], 5.0, 16.0))
    return "".join(g)


N1_STEAM_PATH = ((330.0, N1_DRUM[1]), (330.0, N1_STEAM_Y), (1905.0, N1_STEAM_Y))


def n1_steam_svg():
    pts = N1_STEAM_PATH
    g = [_path(list(pts), "none", C24["ol"], 20.0, op=0.6, close=False),
         _path(list(pts), "none", C24["steam"], 12.0, close=False)]
    for x in (900.0, 1500.0):
        g.append(_path([(x - 14, N1_STEAM_Y - 12), (x + 6, N1_STEAM_Y), (x - 14, N1_STEAM_Y + 12)], "none", C24["drum_ln"], 4.0, close=False))
    return "".join(g)


def _scene_N1(start, states, steps):
    allst = [start] + states
    _head_only("N1", start, states, ("view", "switch"))
    R = N1_REC
    c = N1_CORE
    parts = [_part("bg", _bg_svg(), R["core"]),
             dict(_part("loop", n1_loop_svg(), R["loop"]), geo=dict(kind="n1loop")),
             dict(_part("core", n1_core_svg(), R["core"]), geo=dict(kind="n1core", x0=c["x0"], x1=c["x1"], y0=c["y0"], y1=c["y1"])),
             dict(_part("channels", n1_channels_svg(), R["ch"]), geo=dict(kind="n1ch", xs=list(N1_CH), y0=c["y0"], y1=c["y1"])),
             dict(_part("rods", n1_rods_svg(), R["rod"]), geo=dict(kind="n1rod", xs=list(N1_ROD), top=N1_ROD_TOP, tip=c["y0"])),
             dict(_part("drum", n1_drum_svg(), R["loop"]), geo=dict(kind="n1drum")),
             dict(_part("pump", n1_pump_svg(), R["loop"]), geo=dict(kind="n1pump"))]
    if any(st["n1flow"] == "on" for st in allst):
        parts.append(_part("flow", n1_flow_svg(), R["flow"], keys=_akeys(start, states, steps, lambda st: st["n1flow"] == "on", 0.8)))
    if any(st["n1boil"] == "on" for st in allst):
        parts.append(dict(_part("boil", n1_boil_svg(), R["boil"],
                                keys=_akeys(start, states, steps, lambda st: st["n1boil"] == "on", 1.2, extra=1.6)), geo=dict(kind="n1boil")))
    if any(st["n1rise"] == "on" for st in allst):
        parts.append(_part("rise", n1_rise_svg(), R["flow"],
                           keys=_akeys(start, states, steps, lambda st: st["n1rise"] == "on", 0.8, extra=3.0)))
    if any(st["n1steam"] == "on" for st in allst):
        go = [dict(stage=0, delay=0.0, u=float(start["n1steam"] == "on"))]
        for i, (st, sp) in enumerate(zip(states, steps)):
            if st["n1steam"] == "on" and (go[-1]["u"] < 1.0):
                go.append(dict(stage=i, delay=float(sp.get("delay", KEY_DELAY)), dur=1.5, u=1.0))   # 試し焼き：2.2秒では段の終わりのコマで右の端に届かなかった
        parts.append(dict(_part("steam", n1_steam_svg(), R["steam"], keys=[dict(stage=0, delay=0.0, a=1.0)]), kind="draw",
                          path=[list(q) for q in N1_STEAM_PATH], go=go, reveal=40, geo=dict(kind="n1steam", end=N1_STEAM_PATH[-1][0])))
    if start["switch"] == "on":
        parts.append(_switch_part(N1_SWITCH))
    return parts


def _n1_anchors(st):
    c = N1_CORE
    return dict(ch=(N1_CH[-3] + N1_TW / 2, c["y0"] + 0.62 * (c["y1"] - c["y0"])), core=(c["x0"] + 40, c["y1"] - 60),
                pump=(N1_PUMP[0], N1_PUMP[1] - N1_PUMP[2]), drum=((N1_DRUM[0] + N1_DRUM[2]) / 2, N1_DRUM[3] + 2),
                steam=(1880.0, N1_STEAM_Y + 8), rod=(N1_ROD[-1] + 5, N1_ROD_TOP + 40),
                boil=(N1_CH[-1] + N1_TW / 2, c["y0"] + 60))


def _n1_note(st0, states):
    return "管・棒・ドラム・ポンプ・配管の数と形は模式・炉の高さと直径の比は記録の値"


# ══════════════════════════════════════════════════════════
#  N2 止める棒（c615 top・c905 cut）＝形のもと CC0 の図・寸法 INSAG-7 図1 (a)
# ══════════════════════════════════════════════════════════
N2_S = 0.8                                        # 1cm＝0.8画素
N2_FIG1 = dict(gap=20.0, water=125.0, disp=450.0)   # 図1 (a) の寸法（cm）＝描く側の値（門番は自分の側に REC_N2 を持つ）
N2_CORE_CM = N2_FIG1["water"] * 2 + N2_FIG1["disp"]
# 棒の列は画面の両端で切る（RBMK の棒は 211本＝S1 p113・数えられる形にしない＝門番 ㊴）。試し焼き 39791009342：top の細い棒（56）は
#   「暗い板と灰色の柱」に見えた＝太く（76）・間を詰め・丸い棒の光の筋
N2_CUT = dict(yt=258.0, lid=230.0, xs=(20.0, 490.0, 960.0, 1430.0, 1900.0), cw=96.0, rw=64.0)
N2_TOP = dict(yt=600.0, lid=150.0, xs=tuple(192.0 * k for k in range(11)), rw=76.0)
N2_LAB = dict(cut="止める棒を縦に切った図（横から）", top="炉の上の方（横から）")
N2_REC = dict(
    fig1="S1 p14（with a water filled space of 1.25 m separating the displacer and the absorbing rod・with 1.25 m of water at either end）・S1 p15（図1 (a)＝寸法 cm）",
    core="S1 p16（height 7 m）・S1 p15（図1 (a)）",
    rods="S1 p14（The control rods and the safety rods of an RBMK reactor are inserted into the reactor core from above）",
    move="S1 p113（The independent control rods are inserted into the core at a speed of 0.4 m/s when the EPS is triggered）・S1 p65（01:23:40 EPS-S button was pressed）",
    red="S1 p14（caused a local insertion of positive reactivity in the lower part of the core）",
)


def n2_geo(view):
    """描いた幾何（画素）：炉の上の端・下の端・吸う棒の先・押しのけ棒の上と下（棒が下がる前）"""
    if view == "cut":
        yt = N2_CUT["yt"]
    else:
        yt = N2_TOP["yt"]
    s = N2_S
    return dict(yt=yt, yb=yt + N2_CORE_CM * s, tip=yt - N2_FIG1["gap"] * s, d0=yt + N2_FIG1["water"] * s,
                d1=yt + (N2_FIG1["water"] + N2_FIG1["disp"]) * s, s=s)


def n2_moderator_svg(view):
    g = n2_geo(view)
    if view == "cut":
        out = [_rect(0, g["yt"], W, g["yb"] - g["yt"], C24["gra"]),
               _blocks_svg(0, g["yt"], W, g["yb"], 110.0, 56.0, C24["gra_dk"])]
        for x in N2_CUT["xs"]:
            cw = N2_CUT["cw"]
            out.append(_rect(x - cw / 2, N2_CUT["lid"], cw, g["yb"] - N2_CUT["lid"], C24["water"], C24["water_ln"], 2.0))
        return "".join(out)
    out = [_rect(0, g["yt"], W, H - g["yt"], C24["gra"]), _blocks_svg(0, g["yt"], W, H, 120.0, 60.0, C24["gra_dk"]),
           _line(0, g["yt"], W, g["yt"], C24["gra_ln"], 4.0)]
    return "".join(out)


def n2_rods_svg(view):
    """棒（吸う棒・つなぎ・押しのけ棒）を下がる前の位置で。cut は管の中まで見える・top は吸う棒だけ（炉の中は不透明の塊の後ろ）"""
    g = n2_geo(view)
    out = []

    def absorber(x, rw):
        a = [_rect(x - rw / 2, -400.0, rw, g["tip"] + 400.0, C24["steel"], C24["steel_ln"], 2.5),
             _rect(x - rw / 2 + rw * 0.2, -400.0, rw * 0.16, g["tip"] + 396.0, C24["steel_ln"], op=0.45)]   # 丸い棒の光の筋
        y = g["tip"] - 18.0
        while y > -400.0:                       # 継ぎ目（模式）＝下がる動きが見える
            a.append(_line(x - rw / 2 + 3, y, x + rw / 2 - 3, y, C24["joint"], 4.0))
            y -= 64.0
        return "".join(a)
    if view == "cut":
        rw = N2_CUT["rw"]
        for x in N2_CUT["xs"]:
            out.append(absorber(x, rw))
            for dx in (-7.0, 7.0):
                out.append(_line(x + dx, g["tip"], x + dx, g["d0"], C24["tele"], 3.0))
            out.append(_rect(x - rw / 2, g["d0"], rw, g["d1"] - g["d0"], C24["disp"], C24["disp_ln"], 2.5))
        return "".join(out)
    for x in N2_TOP["xs"]:
        out.append(absorber(x, N2_TOP["rw"]))
    return "".join(out)


def n2_lid_svg(view):
    g = n2_geo(view)
    if view == "cut":
        lid = N2_CUT["lid"]
        return (_rect(0, 0, W, lid, C24["lid"], C24["lid_ln"], 2.0) + _line(0, lid, W, lid, C24["lid_ln"], 3.0)
                + _rect(0, g["yb"], W, H - g["yb"], C24["lid"]) + _line(0, g["yt"], W, g["yt"], C24["ink"], 2.0, ' opacity="0.55"')
                + _line(0, g["yb"], W, g["yb"], C24["ink"], 2.0, ' opacity="0.55"'))
    lid = N2_TOP["lid"]
    return _rect(0, 0, W, lid, C24["lid"], C24["lid_ln"], 2.0) + _line(0, lid, W, lid, C24["lid_ln"], 3.0)


def n2_arrows_svg(view):
    g = n2_geo(view)
    out = []
    if view == "cut":
        for x in N2_CUT["xs"][1:4]:
            xa = x + N2_CUT["cw"] / 2 + 40
            out.append(_arrow((xa, g["yt"] + 30), (xa, g["yt"] + 150), C24["arrow"], 6.0, 20.0))
        return "".join(out)
    xs = N2_TOP["xs"]
    for a, b in zip(xs, xs[1:]):
        xa = (a + b) / 2
        out.append(_arrow((xa, 300.0), (xa, 430.0), C24["arrow"], 6.0, 20.0))
    return "".join(out)


def n2_red_svg():
    g = n2_geo("cut")
    y0 = g["yb"] - N2_FIG1["water"] * N2_S
    out = []
    for x in N2_CUT["xs"]:
        cw = N2_CUT["cw"]
        out.append(_rect(x - cw / 2 - 6, y0, cw + 12, g["yb"] - y0, C24["red"], op=0.55))
        out.append(_rect(x - cw / 2 - 6, y0, cw + 12, g["yb"] - y0, "none", C24["red"], 5.0))
    return "".join(out)


def _scene_N2(start, states, steps):
    allst = [start] + states
    _head_only("N2", start, states, ("view", "switch"))
    _grow_only("N2", start, states, "n2dy")
    view = start["view"]
    R = N2_REC
    g = n2_geo(view)
    if view == "top" and any(st["n2red"] != "off" for st in allst):
        raise ValueError("illu N2：top（炉の上の方）は炉の中を見せない＝n2red は cut だけ")
    mv = lambda st: dict(dy=float(st["n2dy"]) * N2_S, a=1.0)      # noqa: E731
    xs = list(N2_CUT["xs"] if view == "cut" else N2_TOP["xs"])
    core = dict(_part("moderator", n2_moderator_svg(view), R["core"]),
                geo=dict(kind="n2core", view=view, yt=g["yt"], yb=g["yb"], xs=xs,
                         w=N2_CUT["cw"] if view == "cut" else N2_TOP["rw"], opaque=view == "top"))
    rods = dict(_part("rods", n2_rods_svg(view), R["fig1"] if view == "cut" else R["rods"], keys=IL._keys(start, states, steps, mv)),
                geo=dict(kind="n2rods", view=view, tip=g["tip"], d0=g["d0"] if view == "cut" else None,
                         d1=g["d1"] if view == "cut" else None, s=N2_S, xs=xs,
                         w=N2_CUT["rw"] if view == "cut" else N2_TOP["rw"]))
    lid = dict(_part("lid", n2_lid_svg(view), R["core"]), geo=dict(kind="n2lid", view=view))
    # cut＝管の中（水）の上に棒・その上にふた／top＝炉は不透明の塊＝棒は塊の後ろへ入る（下の水と押しのけ棒は見せない）
    parts = [_part("bg", _bg_svg(), R["core"])] + ([core, rods, lid] if view == "cut" else [rods, core, lid])
    if any(st["n2arrow"] == "on" for st in allst):
        parts.append(_part("arrow", n2_arrows_svg(view), R["move"],
                           keys=_akeys(start, states, steps, lambda st: st["n2arrow"] == "on", 0.5)))
    if any(st["n2red"] == "on" for st in allst):
        y0 = g["yb"] - N2_FIG1["water"] * N2_S
        parts.append(dict(_part("red", n2_red_svg(), R["red"],
                                keys=_akeys(start, states, steps, lambda st: st["n2red"] == "on", 0.8, extra=2.0)),   # 下がり終わってから
                          geo=dict(kind="n2red", y0=y0, y1=g["yb"])))
    if start["switch"] == "on":
        parts.append(_switch_part("棒を縦に切ると" if view == "cut" else "炉の上の方では"))
    return parts


def _n2_anchors(st):
    view = st["view"]
    g = n2_geo(view)
    dy = float(st["n2dy"]) * N2_S
    if view == "cut":
        x = N2_CUT["xs"][2]
        cw = N2_CUT["cw"]
        return dict(rod=(x + N2_CUT["rw"] / 2, N2_CUT["lid"] + 4 + dy * 0.0), tip=(x + N2_CUT["rw"] / 2, g["tip"] + dy),
                    disp=(x + N2_CUT["rw"] / 2, (g["d0"] + g["d1"]) / 2 + dy),
                    lo=(N2_CUT["xs"][3] + cw / 2 + 6, g["yb"] - N2_FIG1["water"] * N2_S / 2),
                    top=(x + cw / 2, g["yt"] + 20))
    x = N2_TOP["xs"][min(6, len(N2_TOP["xs"]) - 1)]
    return dict(rod=(x + N2_TOP["rw"] / 2, 300.0 + dy), tip=(x + N2_TOP["rw"] / 2, g["tip"] + dy), top=(x, g["yt"]))


def _n2_note(st0, states):
    if st0["view"] == "cut":
        return "INSAG-7 図1 の寸法（押しのけ棒 4.5m・上下の水 1.25m）で描いた模式・棒の本数は模式"
    return "棒の本数と形は模式・下がる長さは記録の速さ（毎秒0.4m）の内"


# ══════════════════════════════════════════════════════════
#  N3 出力の時刻表（c303 am・c403 night）
# ══════════════════════════════════════════════════════════
N3_AX = dict(x0=210.0, x1=1710.0, y=720.0)
N3_SPAN = dict(am=(0, 24 * 60), night=(0, 70))
N3_TICKS = dict(am=(0, 360, 720, 1080, 1440), night=(0, 30))      # ⚠️ 後半に 1:00 の目盛りを置かない（割れる時刻の字になる）
N3_DAY = dict(am="4月25日", night="4月26日")
N3_LAB = dict(am="4月25日の時刻表（前半）", night="4月26日の時刻表（後半）")
# 札＝(時刻, 段〈0 上・1 下〉, 字の行, 出典)。値は台本 §1-5 で1つに決めた値（表I-I p63・ソ連の報告 p20）
N3_CARDS = dict(
    am=(("1:06", 1, ("出力を下げ始める", "残した棒 31本"), "S1 p63（01:06 Start of reactor power reduction; ORM equals 31 manual control rods）"),
        ("3:47", 0, ("出力 1,600MW",), "S1 p63（03:47 Reactor thermal power is 1600 MW）"),
        ("7:10", 1, ("残した棒 13.2本",), "S1 p63（07:10 ORM equals 13.2 manual control rods）"),
        ("14:00", 0, ("非常用の冷却を切る", "試験の延期"),
         "S1 p63（14:00 Disconnection of the ECCS・14:00 Postponement of testing programme requested by Kiev power grid controller）"),
        ("23:10", 1, ("下げる作業の再開", "残した棒 26本"), "S1 p63（23:10 Power reduction continued, ORM equals 26 manual control rods）")),
    night=(("0:05", 1, ("出力 720MW",), "S1 p63（00:05 Reactor thermal power was 720 MW）"),
           ("0:28", 0, ("約500MW", "30MW 未満"), "S1 p63（00:28 At reactor thermal power of about 500 MW transfer made）・S3 p2020（the power fell below 30 MW(th)）")),
)
N3_ROW_Y = (330.0, 520.0)                          # 札の上の端（段0・段1）
N3_RULE = dict(t="決まり：ふだん 26〜30本以上・15本で すぐ止める", rec="S1 p89（not less than 26-30 rods・When the ORM falls to 15 rods, the reactor should be shut down immediately）")
N3_RULE_COL = {"31本": "green", "13.2本": "red", "26本": "green"}     # 札の行の終わりの値 → 決まりとの比べの色（15本を下回る＝赤）


def n3_rule_hit(t):
    """札の行が残した棒の値で終わるなら、その値（「残した棒 31本」→「31本」）"""
    return next((k for k in N3_RULE_COL if t.endswith(" " + k)), None)
N3_SPLIT = (("1:00", "ソ連の報告", "S3 p2020（Only at 1:00 on 26 April did the operator succeed in stabilizing it at 200 MW(th)）"),
            ("1:03", "INSAG-7 の表", "S1 p64（01.03 Reactor thermal power increased to 200 MW and stabilized）"))
N3_SPLIT_T = "200MW で止まる"
N3_PLAN = dict(t="試験の予定 700〜1,000MW の 20分の1 より低い",
               rec="S3 p2020（was to be carried out at a reactor power of 700-1000 MW(th)・the power fell below 30 MW(th)）")
N3_ECCS = "14:00"                                  # 非常用の冷却を切った札の印（台本 §1-4 の②＝時刻表の印・琥珀＝違反かは割れる）


def n3_min(hm):
    h, m = hm.split(":")
    return int(h) * 60 + int(m)


def n3_x(view, hm):
    a, b = N3_SPAN[view]
    return N3_AX["x0"] + (n3_min(hm) - a) / (b - a) * (N3_AX["x1"] - N3_AX["x0"])


def _hm(m):
    return f"{m // 60}:{m % 60:02d}"


def n3_axis_svg(view):
    ax = N3_AX
    g = [_line(ax["x0"] - 30, ax["y"], ax["x1"] + 30, ax["y"], C24["axis"], 5.0)]
    for m in N3_TICKS[view]:
        x = n3_x(view, _hm(m))
        g.append(_line(x, ax["y"] - 12, x, ax["y"] + 12, C24["tick"], 3.0))
        g.append(_text(x, ax["y"] + 54, _hm(m), 30, C24["tick"], extra=' data-k="tick"'))
    g.append(_text(ax["x0"] - 30, ax["y"] + 104, N3_DAY[view], 32, C24["dim"], anchor="start"))
    return "".join(g)


def _tw(t, size):
    """字の幅の見積もり（全角＝字の大きさ・半角＝0.56倍）"""
    return sum(size if ord(ch) > 255 else 0.56 * size for ch in t)


def _card_box(view, hm, row, lines):
    x = n3_x(view, hm)
    # 試し焼き 39791009342：幅 330 の固定では 3:47 の線が 1:06 の札の右の辺に約4px まで寄った＝幅を字の長さで決める
    w = max(220.0, max([_tw(hm, 48)] + [_tw(t, 34) for t in lines]) + 48.0)
    cx = min(max(x, 96.0 + w / 2), W - 96.0 - w / 2)
    y0 = N3_ROW_Y[row]
    h = 70.0 + 46.0 * len(lines)
    return cx, y0, w, h, x


def n3_card_svg(view, hm, row, lines, accent=None):
    cx, y0, w, h, x = _card_box(view, hm, row, lines)
    ln = accent or C24["card_ln"]
    g = [_line(x, y0 + h, x, N3_AX["y"] - 10, ln, 4.0, f' data-k="stem" data-t="{hm}"'),
         f'<circle cx="{x:.1f}" cy="{N3_AX["y"]:.1f}" r="11" fill="{C24["time"]}" stroke="{C24["ol"]}" stroke-width="3"/>',
         _rect(cx - w / 2, y0, w, h, C24["card"], ln, 4.0 if accent else 3.0, rx=10),
         _text(cx, y0 + 54, hm, 48, C24["time"], extra=' data-k="time"')]
    for k, t in enumerate(lines):
        g.append(_text(cx, y0 + 104 + 46 * k, t, 34, C24["ink"], extra=' data-k="val"'))
    return "".join(g)


def n3_mark_svg(view, hm, row, lines):
    """決まりとの比べの色の枠（残した棒の値の行を緑／赤で囲む）。
    ⚠️ ⑤b-3 の qa_all：同じ札を色違いで上に重ねる形は、同じ字が2枚重なる（門番 layout）＝字を持たない枠にした"""
    cx, y0, w, h, x = _card_box(view, hm, row, lines)
    g = []
    for k, t in enumerate(lines):
        hit = n3_rule_hit(t)
        if hit:
            yb = y0 + 104 + 46 * k
            g.append(_rect(cx - w / 2 + 10, yb - 36, w - 20, 48, "none", C24[N3_RULE_COL[hit]], 5.0, rx=8,
                           extra=f' data-k="mark" data-v="{hit}"'))
    return "".join(g)


def n3_rule_svg():
    w, h, cx, y = 1180.0, 66.0, 960.0, 196.0
    return (_rect(cx - w / 2, y, w, h, C24["card"], C24["amber"], 3.0, rx=10)
            + _text(cx, y + 46, N3_RULE["t"], 34, C24["amber"], extra=' data-k="rule"'))


def n3_drop_svg():
    cx, y0, w, h, x = _card_box("night", "0:28", 0, N3_CARDS["night"][1][2])
    xa = cx + w / 2 + 40
    return _arrow((xa, y0 + 70), (xa, y0 + h + 40), C24["red"], 9.0, 26.0)


def n3_split_svg():
    """割れる時刻＝同じ形の目盛り2本と出典の名（時刻の字は出さない）・200MW の札は2本のあいだ（時刻なし）"""
    ax = N3_AX
    g = []
    xs = []
    for k, (hm, name, _rec) in enumerate(N3_SPLIT):
        x = n3_x("night", hm)
        xs.append(x)
        g.append(_line(x, ax["y"] - 26, x, ax["y"] + 26, C24["doc"], 5.0, f' data-k="split" data-t="{hm}"'))
        g.append(_text(x + (-14 if k == 0 else 14), ax["y"] + 62 + 40 * k, name, 28, C24["doc"],
                       anchor="end" if k == 0 else "start", extra=' data-k="splitname"'))
    cx = (xs[0] + xs[1]) / 2
    w, y0 = 300.0, N3_ROW_Y[1] + 20
    g += [_line(cx, y0 + 76, cx, ax["y"] - 30, C24["card_ln"], 4.0),
          _rect(min(cx - w / 2, W - 96 - w), y0, w, 76, C24["card"], C24["card_ln"], 3.0, rx=10),
          _text(min(cx, W - 96 - w / 2), y0 + 50, N3_SPLIT_T, 34, C24["ink"], extra=' data-k="val"')]
    return "".join(g)


def n3_plan_svg():
    w, h, cx, y = 1060.0, 66.0, 960.0, 196.0
    return (_rect(cx - w / 2, y, w, h, C24["card"], C24["red"], 3.0, rx=10)
            + _text(cx, y + 46, N3_PLAN["t"], 34, C24["ink"], extra=' data-k="plan"'))


def _scene_N3(start, states, steps):
    allst = [start] + states
    _head_only("N3", start, states, ("view",))
    view = start["view"]
    rec_all = "・".join(c[3] for c in N3_CARDS[view])
    parts = [_part("bg", _bg_svg(), rec_all),
             dict(_part("axis", n3_axis_svg(view), rec_all), geo=dict(kind="n3axis", view=view))]
    on_a = lambda st: st["n3a"] == "on"      # noqa: E731
    on_b = lambda st: st["n3b"] == "on"      # noqa: E731
    cards = N3_CARDS[view]
    if view == "am":
        for k, (hm, row, lines, rec) in enumerate(cards):
            acc = C24["amber"] if hm == N3_ECCS else None
            parts.append(dict(_part(f"card{k}", n3_card_svg(view, hm, row, lines, accent=acc), rec,
                                    keys=_akeys(start, states, steps, on_a, 0.5, extra=0.55 * k)), geo=dict(kind="n3card", t=hm)))
        if any(on_b(st) for st in allst):
            parts.append(dict(_part("rule", n3_rule_svg(), N3_RULE["rec"], keys=_akeys(start, states, steps, on_b, 0.6)),
                              geo=dict(kind="n3rule")))
            for k, (hm, row, lines, rec) in enumerate(cards):
                if any(n3_rule_hit(t) for t in lines):
                    parts.append(dict(_part(f"mark{k}", n3_mark_svg(view, hm, row, lines), rec + "・" + N3_RULE["rec"],
                                            keys=_akeys(start, states, steps, on_b, 0.6, extra=0.8)),
                                      geo=dict(kind="n3mark", t=hm)))
    else:
        hm, row, lines, rec = cards[0]
        parts.append(dict(_part("card0", n3_card_svg(view, hm, row, lines), rec, keys=_akeys(start, states, steps, on_a, 0.5)),
                          geo=dict(kind="n3card", t=hm)))
        parts.append(dict(_part("split", n3_split_svg(), "・".join(s[2] for s in N3_SPLIT),
                                keys=_akeys(start, states, steps, on_a, 0.5, extra=0.4)), geo=dict(kind="n3split")))
        hm, row, lines, rec = cards[1]
        if any(on_b(st) for st in allst):
            parts.append(dict(_part("card1", n3_card_svg(view, hm, row, lines, accent=C24["red"]), rec,
                                    keys=_akeys(start, states, steps, on_b, 0.5)), geo=dict(kind="n3card", t=hm)))
            parts.append(_part("drop", n3_drop_svg(), rec, keys=_akeys(start, states, steps, on_b, 0.6, extra=1.2)))
        if any(st["n3c"] == "on" for st in allst):
            parts.append(dict(_part("plan", n3_plan_svg(), N3_PLAN["rec"],
                                    keys=_akeys(start, states, steps, lambda st: st["n3c"] == "on", 0.6)), geo=dict(kind="n3plan")))
    return parts


def _n3_anchors(st):
    return dict(axis=(N3_AX["x0"], N3_AX["y"]))


def _n3_note(st0, states):
    if st0["view"] == "night":
        return "200MW で止まった時刻は資料で割れる（1つに決めない）"
    return "残した棒＝標準の棒に直した本数"


# ══════════════════════════════════════════════════════════
#  N4 避難のバス（c707・町の通りを横から）
# ══════════════════════════════════════════════════════════
N4_HZ = 600.0                                      # 地平線（建物の足もと）
N4_ROAD = (628.0, 724.0)                           # 道（上の端・下の端）
N4_BUS = dict(len=236.0, h=94.0, gap=28.0, y=716.0, x0=-150.0)    # バス（横から・模式）＝画面の両端の外まで続く
N4_BUS_XS = tuple(N4_BUS["x0"] + (N4_BUS["len"] + N4_BUS["gap"]) * k for k in range(9))
N4_IN = 1980.0                                     # 夜のうちに着く＝右の外からずれて来る量（画素）
N4_CROWD = dict(base=832.0, w=72.0, rows=2)       # ⑤b-3 の下見：46画素では帯・試し焼き：56画素3列でも暗い玉の帯＝大きく2列（肩の形が見える）
N4_TOWN = (960.0, 380.0)                           # 知らせの輪の真ん中（模式）
N4_LAB = "町の通りを横から見た図"
N4_REC = dict(
    town="L2 p3024（the town of Pripyat, located just 3 km from the damaged reactor）",
    bus="L2 p3024（During the night, arrangements were made for nearly 1,200 buses that would be needed totransport the residents）",
    call="L2 p3024（Around noon on 27 April the evacuation order was broadcast to the people）",
    crowd="L2 p3024（the evacuation began at 14:00 and finished at 17:00）",
)
N4_BLDG = ((60, 250, 13), (330, 200, 9), (560, 300, 16), (900, 240, 12), (1180, 210, 9), (1420, 300, 16), (1760, 220, 12))


def n4_sky_svg(day):
    c0, c1 = (C24["sky_d0"], C24["sky_d1"]) if day else (C24["sky_n0"], C24["sky_n1"])
    gid = "n4d" if day else "n4n"
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c0}"/>'
            f'<stop offset="1" stop-color="{c1}"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="{N4_HZ + 2:.0f}" fill="url(#{gid})"/>')


def n4_bldg_svg(day):
    """団地の影（模式・窓の明かりは描かない＝人の様子を描かない）"""
    fill, win = (C24["bld_d"], C24["bld_d_win"]) if day else (C24["bld_n"], C24["bld_n_win"])
    g = []
    for x0, w, fl in N4_BLDG:
        h = fl * 22.0
        y0 = N4_HZ - h
        g.append(_rect(x0, y0, w, h, fill))
        for r in range(fl):
            y = y0 + 8 + 22 * r
            xx = x0 + 12
            while xx + 16 < x0 + w - 8:
                g.append(_rect(xx, y, 16, 9, win))
                xx += 30
    return "".join(g)


def n4_ground_svg(day):
    gnd = C24["gnd_d"] if day else C24["gnd_n"]
    y0, y1 = N4_ROAD
    return (_rect(0, N4_HZ, W, H - N4_HZ, gnd) + _rect(0, y0, W, y1 - y0, C24["road"])
            + _line(0, y0, W, y0, C24["road_ln"], 2.0, ' opacity="0.5"'))


def n4_bus_svg():
    L, h, yb = N4_BUS["len"], N4_BUS["h"], N4_BUS["y"]
    g = []
    for x in N4_BUS_XS:
        y0 = yb - h
        g.append(_rect(x, y0, L, h - 10, C24["bus"], C24["bus_ln"], 3.0, rx=14))
        g.append(_rect(x + 14, y0 + 14, L - 40, 30, C24["bus_win"], rx=4))
        for k in range(1, 5):
            xx = x + 14 + (L - 40) * k / 5
            g.append(_line(xx, y0 + 14, xx, y0 + 44, C24["bus_dk"], 3.0))
        g.append(_rect(x + L - 22, y0 + 14, 12, h - 32, C24["bus_win"], rx=3))
        g.append(_rect(x, yb - 34, L, 8, C24["bus_dk"]))
        for wx in (x + 46, x + L - 54):
            g.append(f'<circle cx="{wx:.1f}" cy="{yb - 10:.1f}" r="18" fill="{C24["wheel"]}" stroke="{C24["bus_dk"]}" stroke-width="4"/>')
    return "".join(g)


def n4_ring_svg():
    x, y = N4_TOWN
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="64" fill="none" stroke="{C24["ol"]}" stroke-opacity="0.5" stroke-width="12"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="64" fill="none" stroke="{C24["ring"]}" stroke-width="6"/>')


def n4_crowd_layout():
    c = N4_CROWD
    return IL.crowd_layout(0.0, float(W), c["base"], c["w"], rows=c["rows"])


def _scene_N4(start, states, steps):
    allst = [start] + states
    R = N4_REC
    day = lambda st: st["n4day"] == "on"      # noqa: E731
    parts = [_part("sky_n", n4_sky_svg(False), R["town"]),
             _part("sky_d", n4_sky_svg(True), R["call"], keys=_akeys(start, states, steps, day, 1.6)),
             _part("bldg_n", n4_bldg_svg(False), R["town"]),
             _part("bldg_d", n4_bldg_svg(True), R["town"], keys=_akeys(start, states, steps, day, 1.6)),
             _part("gnd_n", n4_ground_svg(False), R["town"]),
             _part("gnd_d", n4_ground_svg(True), R["town"], keys=_akeys(start, states, steps, day, 1.6))]
    bus_dx = lambda st: dict(dx=0.0 if st["n4bus"] == "on" else N4_IN, a=1.0)     # noqa: E731
    ks = [dict(stage=0, delay=0.0, **bus_dx(start))]
    for i, (st, sp) in enumerate(zip(states, steps)):
        if st["n4bus"] != (allst[i]["n4bus"]):
            ks.append(dict(stage=i, delay=float(sp.get("delay", KEY_DELAY)), dur=2.6, **bus_dx(st)))
    parts.append(dict(_part("buses", n4_bus_svg(), R["bus"], keys=ks),
                      geo=dict(kind="n4bus", xs=list(N4_BUS_XS), len=N4_BUS["len"], dx_off=N4_IN)))
    pulse = [dict(stage=i, delay=float(sp.get("ring_delay", 0.6)), n=3, **IL.RING_KIND["out"])
             for i, (st, sp) in enumerate(zip(states, steps)) if st["n4call"] == "on" and allst[i]["n4call"] != "on"]
    if pulse:
        parts.append(dict(_part("call", n4_ring_svg(), R["call"], N4_TOWN), kind="ring", pulse=pulse, geo=dict(kind="n4call")))
    if any(st["n4crowd"] == "on" for st in allst):
        lay = n4_crowd_layout()
        cols = (C24["crowd0"], C24["crowd1"], C24["crowd2"])
        parts.append(dict(_part("crowd", IL.crowd_svg(lay, cols), R["crowd"],
                                keys=_akeys(start, states, steps, lambda st: st["n4crowd"] == "on", 1.0, extra=2.0)),
                          role="residents", crowd=[dict(layout=lay, x0=0.0, x1=float(W))], geo=dict(kind="n4crowd")))
    return parts


def _n4_anchors(st):
    x = N4_BUS_XS[min(5, len(N4_BUS_XS) - 1)]
    return dict(bus=(x + N4_BUS["len"] / 2, N4_BUS["y"] - N4_BUS["h"]), town=(N4_TOWN[0] + 70, N4_TOWN[1] - 40),
                crowd=(1320.0, N4_CROWD["base"] - 60))


def _n4_note(st0, states):
    return "バス・建物・群れの形は模式（数は描かない）・知らせの輪は模式"


# ══════════════════════════════════════════════════════════
#  登録
# ══════════════════════════════════════════════════════════
def register():
    IL.FIELDS.update(
        N1=dict(view="side", n1flow="off", n1boil="off", n1rise="off", n1steam="off", switch="off", cam=1.0),
        N2=dict(view="cut", n2dy=0.0, n2arrow="off", n2red="off", switch="off", cam=1.0),
        N3=dict(view="am", n3a="off", n3b="off", n3c="off", cam=1.0),
        N4=dict(view="street", n4bus="off", n4day="off", n4call="off", n4crowd="off", cam=1.0))
    IL.CHOICES.update(n1flow=IL.ONOFF, n1boil=IL.ONOFF, n1rise=IL.ONOFF, n1steam=IL.ONOFF,
                      n2arrow=IL.ONOFF, n2red=IL.ONOFF,
                      n3a=IL.ONOFF, n3b=IL.ONOFF, n3c=IL.ONOFF,
                      n4bus=IL.ONOFF, n4day=IL.ONOFF, n4call=IL.ONOFF, n4crowd=IL.ONOFF)
    IL.VIEWS.update(N1=("side",), N2=("cut", "top"), N3=("am", "night"), N4=("street",))
    IL.REC_FIELDS = IL.REC_FIELDS + ("n1flow", "n1boil", "n1rise", "n1steam", "n2dy", "n2red", "n3a", "n3b", "n3c",
                                     "n4bus", "n4day", "n4call", "n4crowd")
    IL.NOTE.update(N1=_n1_note, N2=_n2_note, N3=_n3_note, N4=_n4_note)
    IL.EXTRA.update(
        N1=dict(scene=_scene_N1, anchors=_n1_anchors, camc=lambda st0, states: (960.0, 520.0), label=lambda st0, states: N1_LAB),
        N2=dict(scene=_scene_N2, anchors=_n2_anchors, camc=lambda st0, states: (960.0, 540.0),
                label=lambda st0, states: N2_LAB[st0["view"]]),
        N3=dict(scene=_scene_N3, anchors=_n3_anchors, camc=lambda st0, states: (960.0, 540.0),
                label=lambda st0, states: N3_LAB[st0["view"]]),
        N4=dict(scene=_scene_N4, anchors=_n4_anchors, camc=lambda st0, states: (960.0, 560.0), label=lambda st0, states: N4_LAB))


register()
