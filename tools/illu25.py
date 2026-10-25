# -*- coding: utf-8 -*-
"""illu25.py — 案C の再現イラスト：25本目（JR福知山線脱線事故・2005-04-25・上り快速 5418M）の置き場 F1〜F6（⑤b-4・2026-10-25 新設）。

`tools/illu.py` の末尾で読み込み、型の表（FIELDS・CHOICES・VIEWS・REC_FIELDS・NOTE）と置き場の登録 `illu.EXTRA` へ足す（illu17・illu20・illu24 と同じ作り）。
🔴 置き場の名は **F1〜F6**（illu17＝C1〜C7・illu20＝S1〜S7・illu24＝N1〜N4・illu19 の型＝A1〜A5 と重ねない＝同じ名で足すと黙ってぶつかる）。
🔴 §0b（題材を替えるとき）：このファイルは25本目の型の値そのもの＝次の回は読み込みを外すか、置き場の名がぶつからないか確かめる。

■ 置き場（台本 §7 の案C・映像方針 25本目 §2 了承② 決め4・一覧 `ref/ep25/eizou_list25.md`）
  F1 … 曲線と速度（c301＝view all 伊丹駅〜曲線／c317＝view near 塚口駅〜曲線）。上から見た線路の略図＝駅・信号・曲線の入口の間の距離の比は
       付図27 のキロ程（尼崎駅起点の実測）。線路はまっすぐに伸ばした模式（実際の線路の曲がりは描かない）・曲線の形だけ記録の値
       （付図73＝入口の緩和曲線 60m・円曲線 半径304m 長さ188m・出口の緩和曲線 60m）。欄＝f1at（列車の印の位置）・f1hl（曲線を赤く）
  F2 … ブレーキの段（c304＝view early／c318＝view late）。取っ手を正面から（形のもと＝国交省「207系運転台のブレーキ、力行ハンドル位置図」の
       ユルメ・1〜8・非常の並び・角度は模式）。手は描かない。右に使った段の秒の帯（R1 p.13 の秒＝帯の幅・0.0〜約0.2秒の段は細い帯で秒の字なし）
  F3 … 交信の流れ（c306＝view start／c314＝view later）。3つの欄（総合指令所の指令員・7両目の車掌・1両目の運転士＝役職だけ）・吹き出しは
       誰が何をしたかの短い言い方（字句は語りが読む＝複写にしない・要の語は R1 p.77 の記録の語）・運転士の欄は空白。
       下に秒の帯（9:17:50〜9:19:00＝点の位置は時刻の比）
  F4 … ATS の照査（c703＝view basic／c719＝view if）。速さと距離の図（形のもと＝検証報告書の付録の解説 図-5 の ATS-P 曲線速照機能・数は描かない）。
       if＝もし照らしがあったら（想定の札）・実際の速さの線は曲線の入口で止める（脱線は描かない）
  F5 … 付け替えの前後（c603）。上から見た曲線の重ね＝前（半径600m・R1 p.72）といま（付図73 の形）。半径と長さの比は記録の値・
       前の曲線が手前で分かれて緩い形は国土地理院の空中写真（1974〜78年・1984〜86年の層）・位置の関係は模式
  F6 … 宝塚の分岐器（c207）。上から見た宝塚駅の略図（付図28 その1）＝ATS の地上子 下り17k981m・「40」の標識 下り18k008m・ホームの端
       下り18k149m の間の距離の比はキロ程。分岐器（31号イ）の位置と長さ・線の間隔は模式
■ 守りの線（台本 §1-4・§1-5・映像方針 25本目＝門番 check_illu ㊷〜㊼ が記録の値を門番の側に持つ＝ここの定数を読まない）
  ・人は描かない（運転士・車掌・指令員は役職の欄だけ・手も描かない）・事故の瞬間（脱線・転覆）は描かない
  ・時計の札は台本 §1-5 で1つに決めた時刻だけ（`cuts.ss.ILLU_CLOCK_OK`＋門番の側の秒まで）・数の札は記録の値だけ
"""
from __future__ import annotations

import math

import illu as IL
import titan_fig as F

W, H = IL.W, IL.H
KEY_DELAY = IL.KEY_DELAY
_part = IL._part

# ── 絵の色（全章で固定・章の色の置き換えが拾う値＝jiko_style の BG・BG2・GRID・LINE・LINE_DIM・TICK・INK_W を使わない）──
C25 = dict(
    bg0="#0e161d", bg1="#18232c", ink="#eef3f5", dim="#a9b8c2", ol="#0a0f14",
    rail="#c9d2d8", rail_ol="#0b1015", rail_dk="#6f7b84", sleeper="#3b4650",
    stn="#eef3f5", sig_pole="#8996a0", sig_head="#1d262e", sig_lamp="#5cc98a",
    train="#dfe6ea", train_ln="#2a333b", amber="#f2c14e", red="#e0503c", green="#5cc98a", blue="#5aa7e8",
    card="#1a2630", card_ln="#5d6d79", time="#f2c14e",
    dial="#26323c", dial_ln="#8494a0", knob="#c9d2d8", shaft="#9aa7b1",
    band_bg="#24313b", band_ln="#6d7d89", seg="#5aa7e8", seg_thin="#a9d2f3", coast="#6b7a86",
    col_bg="#16222c", col_ln="#5d6d79", bubble="#eef3f5", bubble_ln="#0a0f14", bubble_ink="#10181f", radio="#5aa7e8",
    axis="#cdd6dc", pat="#5aa7e8", speed="#eef3f5", real="#8c99a3", brake="#e0503c",
    old="#8c99a3", new="#e0503c", trans="#f2c14e", plat="#3c4954", plat_ln="#7f8e9a", coil="#e0503c", sign="#eef3f5",
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
    o = (f' stroke="{C25["ol"]}" stroke-width="6" stroke-linejoin="round" paint-order="stroke fill"' if ol else "")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Noto" font-size="{size:.0f}" fill="{col or C25["ink"]}" '
            f'text-anchor="{anchor}"{o}{extra}>{F.esc(t)}</text>')


def _arrow(p, q, col, w=8.0, head=22.0):
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    b = (q[0] - head * math.cos(ang), q[1] - head * math.sin(ang))
    l = (b[0] + head * 0.55 * math.sin(ang), b[1] - head * 0.55 * math.cos(ang))
    r = (b[0] - head * 0.55 * math.sin(ang), b[1] + head * 0.55 * math.cos(ang))
    return (_line(p[0], p[1], b[0], b[1], C25["ol"], w + 5, ' opacity="0.55"') + _line(p[0], p[1], b[0], b[1], col, w)
            + _path([q, l, r], col, C25["ol"], 2.0))


def _tw(t, size):
    """字の幅の見積もり（全角＝字の大きさ・半角＝0.56倍）"""
    return sum(size if ord(ch) > 255 else 0.56 * size for ch in t)


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


def _at_keys(stage, delay, dur=0.5):
    """決まった段の決まった秒に出す鍵（型の表の順番＝段の行頭からの秒）"""
    return [dict(stage=0, delay=0.0, a=0.0), dict(stage=int(stage), delay=float(delay), dur=float(dur), a=1.0)]


def _head_only(place, start, states, fields):
    for f in fields:
        if any(st[f] != start[f] for st in states):
            raise ValueError(f"illu {place}：{f} は場面の頭（start）で1つだけ")


def _switch_part(text):
    return dict(_part("switch", IL.va_switch_svg(text), "", keys=IL._switch_keys()), signal=True)


def _bg_svg(gid="f25bg"):
    return (f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C25["bg0"]}"/>'
            f'<stop offset="1" stop-color="{C25["bg1"]}"/></linearGradient></defs>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#{gid})"/>')


def track_pts(x0, y0, ppm, shape, head=0.0, tail=0.0, step=1.0):
    """曲線の点（上から見た・右へ進んで右へ曲がる）。shape＝(入口の緩和曲線 m, 半径 m, 円曲線 m, 出口の緩和曲線 m)。
    曲がり（1／半径）を緩和曲線で 0 から直線的に上げ下げして、向きを足し上げる（クロソイドの近似）。返り値＝(点, 区切りの距離 m)"""
    l1, r, lc, l2 = shape
    marks = (l1, l1 + lc, l1 + lc + l2)
    total = marks[-1] + tail
    pts, x, y, th, s = [(x0 - head * ppm, y0), (x0, y0)], x0, y0, 0.0, 0.0
    while s < total - 1e-9:
        ds = min(step, total - s)
        sm = s + ds / 2
        if sm < l1:
            k = sm / (l1 * r) if l1 else 1.0 / r
        elif sm < l1 + lc:
            k = 1.0 / r
        elif sm < marks[-1]:
            k = (marks[-1] - sm) / (l2 * r) if l2 else 0.0
        else:
            k = 0.0
        th += k * ds
        x += math.cos(th - k * ds / 2) * ds * ppm
        y += math.sin(th - k * ds / 2) * ds * ppm
        s += ds
        pts.append((x, y))
    return pts, marks


def _sub(pts, ppm, x0, a, b, head):
    """track_pts の点から、曲線の入口からの距離 a〜b（m）の部分（head＝入口の手前の直線の長さ m＝点の頭の2つ）"""
    out = [pts[1]] if a <= 0 else []
    for k, p in enumerate(pts[2:], start=1):
        if a - 1e-9 <= k <= b + 1e-9:
            out.append(p)
    return out


# ══════════════════════════════════════════════════════════
#  F1 曲線と速度（c301 all・c317 near）＝上から見た線路の略図
# ══════════════════════════════════════════════════════════
F1_KM = dict(itami=6.200, inadera=4.312, tsukaguchi=2.872, sig6l=2.690, sig4=2.207, curve=1.949)   # 付図27（尼崎駅起点の実測キロ程）
F1_SHAPE = (60.0, 304.0, 188.0, 60.0)              # 付図73＝入口の緩和曲線 60m・円曲線 半径304m 長さ188m・出口の緩和曲線 60m
F1_Y = 540.0
F1_VIEW = dict(all=dict(k0=6.200, x0=250.0, ppk=290.0, show=("itami", "inadera", "tsukaguchi", "curve")),
               near=dict(k0=2.872, x0=250.0, ppk=1000.0, show=("tsukaguchi", "sig6l", "sig4", "curve")))
F1_NAME = dict(itami="伊丹駅", inadera="猪名寺駅", tsukaguchi="塚口駅", sig6l="塚口駅の先の信号", sig4="次の信号", curve="曲線の入口")
F1_TAIL = 240.0                                    # 曲線の先の直線（m・模式＝画面の下の端の手前まで）
F1_LAB = dict(all="上から見た線路の略図（伊丹駅〜曲線）", near="上から見た線路の略図（塚口駅〜曲線）")
F1_REC = dict(
    km="付図27 p5030（塚口駅上り2k872m・上り出発信号機(6L,7L)上り2k690m・上り第4閉そく信号機上り2k207m）・"
       "付図27 p5031（猪名寺駅上り4k312m）・付図27 p5032（伊丹駅上り6k200m）",
    curve="R1 p72（上り1k949mから上り1k889mまでの60mが緩和曲線、その前方上り1k702mまでが半径304mの円曲線）・"
          "付図73 p7005（緩和曲線長さ60m・円曲線半径304m長さ188m）",
    run="R1 p12（伊丹駅を定刻より約1分20秒遅れて9時16分10秒ごろ出発した後力行を続け）",
)


def f1_x(view, km):
    v = F1_VIEW[view]
    return v["x0"] + (v["k0"] - km) * v["ppk"]


def f1_track(view):
    v = F1_VIEW[view]
    ppm = v["ppk"] / 1000.0
    xc = f1_x(view, F1_KM["curve"])
    head = (xc + 60.0) / ppm                       # 画面の左の外から
    return track_pts(xc, F1_Y, ppm, F1_SHAPE, head=head, tail=F1_TAIL)


def f1_track_svg(view):
    pts, _m = f1_track(view)
    return (_path(pts, "none", C25["rail_ol"], 22.0, close=False) + _path(pts, "none", C25["rail_dk"], 14.0, close=False)
            + _path(pts, "none", C25["rail"], 6.0, close=False))


def f1_marks_svg(view):
    g = []
    for nm in F1_VIEW[view]["show"]:
        x = f1_x(view, F1_KM[nm])
        if nm in ("itami", "inadera", "tsukaguchi"):
            g.append(_rect(x - 34, F1_Y - 30, 68, 12, C25["stn"], C25["ol"], 2.0, rx=3))
            g.append(_rect(x - 34, F1_Y + 18, 68, 12, C25["stn"], C25["ol"], 2.0, rx=3))
            # 🔧 ⑤b-4 の qa_all：駅の名を線の上に置くと、駅を指す札（上へ出る）の線が名を縦に貫いた＝名は線の下・札は上
            g.append(_text(x, F1_Y + 72, F1_NAME[nm], 34, C25["ink"]))
        elif nm in ("sig6l", "sig4"):
            g.append(_line(x, F1_Y + 16, x, F1_Y + 70, C25["sig_pole"], 5.0))
            g.append(f'<circle cx="{x:.1f}" cy="{F1_Y + 82:.1f}" r="15" fill="{C25["sig_head"]}" stroke="{C25["sig_pole"]}" stroke-width="3"/>')
            g.append(_text(x, F1_Y + 140, F1_NAME[nm], 30, C25["dim"]))
        else:
            g.append(_path([(x, F1_Y - 30), (x + 14, F1_Y - 16), (x, F1_Y - 2), (x - 14, F1_Y - 16)], C25["amber"], C25["ol"], 2.0))
            g.append(_text(x - 20, F1_Y - 52, F1_NAME[nm], 32, C25["amber"], anchor="end"))
    return "".join(g)


def f1_curve_svg(view):
    pts, (m1, m2, m3) = f1_track(view)
    ppm = F1_VIEW[view]["ppk"] / 1000.0
    cv = _sub(pts, ppm, 0, 0.0, m3, 0)
    xm, ym = cv[len(cv) // 2]
    return (_path(cv, "none", C25["ol"], 24.0, op=0.6, close=False) + _path(cv, "none", C25["red"], 14.0, close=False)
            + _text(xm - 60, ym + 70, "半径304m", 38, C25["red"], anchor="end", extra=' data-k="r"'))


def f1_train_svg(view):
    x = f1_x(view, F1_KM[F1_VIEW[view]["show"][0]])
    return (_rect(x - 40, F1_Y - 15, 80, 30, C25["train"], C25["train_ln"], 3.0, rx=8)
            + _path([(x + 40, F1_Y - 11), (x + 56, F1_Y), (x + 40, F1_Y + 11)], C25["train"], C25["train_ln"], 3.0))


def _scene_F1(start, states, steps):
    allst = [start] + states
    _head_only("F1", start, states, ("view", "switch"))
    view = start["view"]
    show = F1_VIEW[view]["show"]
    for st in allst:
        if st["f1at"] not in show:
            raise ValueError(f"illu F1：列車の印の位置 {st['f1at']} はこの見え方（{view}）に無い（{show}）")
    R = F1_REC
    pts, marks = f1_track(view)
    ppm = F1_VIEW[view]["ppk"] / 1000.0
    xs = {nm: f1_x(view, F1_KM[nm]) for nm in show}
    parts = [_part("bg", _bg_svg(), R["km"]),
             dict(_part("track", f1_track_svg(view), R["km"]),
                  geo=dict(kind="f1track", view=view, ppk=F1_VIEW[view]["ppk"], y=F1_Y, x_curve=xs["curve"],
                           shape=_shape_geo(pts, marks, ppm))),
             dict(_part("marks", f1_marks_svg(view), R["km"]), geo=dict(kind="f1marks", view=view, xs=xs))]
    if any(st["f1hl"] == "on" for st in allst):
        parts.append(dict(_part("curve", f1_curve_svg(view), R["curve"],
                                keys=_akeys(start, states, steps, lambda st: st["f1hl"] == "on", 0.8)), geo=dict(kind="f1curve")))
    x_first = xs[show[0]]
    mv = lambda st: dict(dx=xs[st["f1at"]] - x_first, a=1.0)      # noqa: E731
    parts.append(dict(_part("train", f1_train_svg(view), R["run"], keys=IL._keys(start, states, steps, mv)),
                      geo=dict(kind="f1train", at=[st["f1at"] for st in allst])))
    if start["switch"] == "on":
        parts.append(_switch_part("上から見ると"))
    return parts


def _shape_geo(pts, marks, ppm):
    """描いた曲線の幾何（画素）：曲線の長さ・入口の緩和曲線の長さ・円曲線の曲がり（3点の外接円の半径）"""
    def plen(a, b):
        return sum(math.dist(pts[k], pts[k + 1]) for k in range(a, b))
    i0 = 1
    i1 = i0 + int(round(marks[0]))
    i2 = i0 + int(round(marks[1]))
    i3 = i0 + int(round(marks[2]))
    p, q, r = pts[i1 + 10], pts[(i1 + i2) // 2], pts[i2 - 10]
    a, b, c = math.dist(q, r), math.dist(p, r), math.dist(p, q)
    area = abs((q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])) / 2
    return dict(len=plen(i0, i3), trans=plen(i0, i1), circ=plen(i1, i2), radius=a * b * c / (4 * area), ppm=ppm)


def _f1_anchors(st):
    view = st["view"]
    out = {nm: (f1_x(view, F1_KM[nm]), F1_Y - 16) for nm in F1_VIEW[view]["show"]}
    return out


def _f1_note(st0, states):
    return "線路はまっすぐに伸ばした模式（駅・信号・曲線の入口の間の距離の比はキロ程・曲線の形は記録の値）"


# ══════════════════════════════════════════════════════════
#  F2 ブレーキの段（c304 early・c318 late）＝取っ手を正面から
# ══════════════════════════════════════════════════════════
F2_PIV = (700.0, 560.0)
F2_RAD = 290.0
F2_POS = ("ユルメ", "1", "2", "3", "4", "5", "6", "7", "8", "非常")
F2_ANG0 = 150.0                                     # ユルメの角度（度・画面の x 軸から時計回り＝左下）
F2_DANG = 10.0                                      # 段の間の角度（模式）
F2_PPS = 150.0                                      # 秒の帯の 1秒の幅（画素）
F2_BAND = dict(x0=1100.0, y=640.0, h=50.0)
F2_SEQ = dict(early=((0, 0.35, "1"), (0, 2.30, "ユルメ")),
              late=((0, 0.45, "1"), (0, 1.25, "3か4"), (1, 0.30, "5"), (1, 1.35, "6"), (1, 1.75, "7")))
# 帯の切れ＝(名, 秒〈None＝帯の右の端まで〉, 字, 段, 秒〈段の行頭から〉)。0.0〜約0.2秒の段は 0.2秒の細い帯＝秒の字は出さない
F2_SEG = dict(early=(("B1", 2.0, "B1 約2.0秒", 0, 0.35), ("惰行", None, "その先は 惰行", 0, 2.30)),
              late=(("B1・B3かB4", 0.2, "B1・B3かB4", 0, 0.45), ("B5", 0.8, "B5 約0.8秒", 1, 0.30),
                    ("B6", 0.2, "B6", 1, 1.35), ("B7", 2.4, "B7 約2.4秒", 1, 1.75)))
F2_T0 = dict(early="9:18:09ごろ", late="9:18:50ごろ")
F2_LAB = "ブレーキの取っ手を正面から見た図"
F2_REC = dict(
    pos="国交省 p1（207系運転台のブレーキ、力行ハンドル位置図＝ユルメ・1〜8・非常）・R1 p13（B1・B3又はB4・B5・B6・B7）",
    early="R1 p13（力行を止めるとほぼ同時にB1が約2.0秒間使用され・125km/hに達した9時18分09秒ごろ）",
    late="R1 p13（9時18分50秒ごろB1続いてB3又はB4が合わせて0.0~約0.2秒間、B5が約0.8秒間、B6が0.0~約0.2秒間、B7が約2.4秒間）",
)


def f2_ang(name):
    if name == "3か4":
        return F2_ANG0 + F2_DANG * 3.5
    return F2_ANG0 + F2_DANG * F2_POS.index(name)


def _polar(a, r):
    t = math.radians(a)
    return F2_PIV[0] + r * math.cos(t), F2_PIV[1] + r * math.sin(t)


def f2_dial_svg():
    cx, cy = F2_PIV
    a0, a1 = f2_ang("ユルメ") - 6, f2_ang("非常") + 6
    p0, p1 = _polar(a0, F2_RAD + 26), _polar(a1, F2_RAD + 26)
    q0, q1 = _polar(a1, F2_RAD - 26), _polar(a0, F2_RAD - 26)
    g = [f'<path d="M {p0[0]:.1f} {p0[1]:.1f} A {F2_RAD + 26:.1f} {F2_RAD + 26:.1f} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} '
         f'L {q0[0]:.1f} {q0[1]:.1f} A {F2_RAD - 26:.1f} {F2_RAD - 26:.1f} 0 0 0 {q1[0]:.1f} {q1[1]:.1f} Z" '
         f'fill="{C25["dial"]}" stroke="{C25["dial_ln"]}" stroke-width="3"/>']
    for nm in F2_POS:
        a = f2_ang(nm)
        p, q = _polar(a, F2_RAD - 22), _polar(a, F2_RAD + 22)
        g.append(_line(p[0], p[1], q[0], q[1], C25["red"] if nm == "非常" else C25["ink"], 5.0))
        tx, ty = _polar(a, F2_RAD + 70)
        g.append(_text(tx, ty + 12, nm, 36 if len(nm) == 1 else 32, C25["red"] if nm == "非常" else C25["ink"],
                       extra=f' data-k="pos" data-a="{a:.1f}"'))
    g.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="34" fill="{C25["dial"]}" stroke="{C25["dial_ln"]}" stroke-width="4"/>')
    return "".join(g)


def f2_handle_svg():
    """取っ手（ユルメの角度で描く＝鍵の rot で回す）。手は描かない"""
    cx, cy = F2_PIV
    tip = _polar(F2_ANG0, F2_RAD - 30)
    return (_line(cx, cy, tip[0], tip[1], C25["ol"], 30.0, ' opacity="0.6"') + _line(cx, cy, tip[0], tip[1], C25["shaft"], 20.0)
            + f'<circle cx="{tip[0]:.1f}" cy="{tip[1]:.1f}" r="30" fill="{C25["knob"]}" stroke="{C25["ol"]}" stroke-width="4"/>'
            + f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="16" fill="{C25["shaft"]}" stroke="{C25["ol"]}" stroke-width="3"/>')


def f2_band_bg_svg(view):
    b = F2_BAND
    return (_rect(b["x0"] - 20, b["y"] - 20, W - 72 - b["x0"] + 20, b["h"] + 40, C25["band_bg"], C25["band_ln"], 2.0, rx=10)
            + _text(b["x0"], b["y"] - 80, F2_T0[view], 40, C25["time"], anchor="start", extra=' data-k="t0"')
            # 🔧 ⑤b-4 の qa_all：帯の下（y 840）では左下の出典の行に 8px 重なった＝帯の上の右へ
            + _text(W - 92.0, b["y"] - 80, "帯の幅＝使った秒", 28, C25["dim"], anchor="end"))


def f2_segs(view):
    """帯の切れの幾何（画素）＝(名, x0, x1, 字, 段, 秒, 字の行)。細い帯の字は帯の上・ほかは帯の下に互い違い（B5 と B7 の字が重ならない）"""
    out, x, j = [], F2_BAND["x0"], 0
    for nm, sec, t, stg, dl in F2_SEG[view]:
        x1 = (W - 92.0) if sec is None else x + sec * F2_PPS
        thin = (x1 - x) < 60
        out.append((nm, x, x1, t, stg, dl, -1 if thin else j % 2))
        j += 0 if thin else 1
        x = x1
    return out


def f2_seg_svg(nm, x0, x1, t, row):
    b = F2_BAND
    thin = row < 0
    col = C25["coast"] if nm == "惰行" else (C25["seg_thin"] if thin else C25["seg"])
    g = [_rect(x0, b["y"], x1 - x0, b["h"], col, C25["ol"], 2.0, extra=f' data-k="seg" data-n="{nm}"')]
    if thin:
        g.append(_text(x0 + (x1 - x0) / 2, b["y"] - 34, t, 28, C25["seg_thin"], extra=' data-k="segt"'))
    else:
        g.append(_text(x0 + 6, b["y"] + b["h"] + 48 + 44 * row, t, 34, C25["ink"], anchor="start", extra=' data-k="segt"'))
    return "".join(g)


def _scene_F2(start, states, steps):
    _head_only("F2", start, states, ("view", "switch"))
    view = start["view"]
    seq = F2_SEQ[view]
    if any(s >= len(steps) for s, _d0, _p in seq) or any(s >= len(steps) for _n, _s, _t, s, _d0 in F2_SEG[view]):
        raise ValueError(f"illu F2：{view} の段の並びが行の数 {len(steps)} を越える")
    R = F2_REC
    parts = [_part("bg", _bg_svg(), R["pos"]),
             dict(_part("dial", f2_dial_svg(), R["pos"]),
                  geo=dict(kind="f2dial", ang={nm: f2_ang(nm) for nm in F2_POS}, piv=list(F2_PIV)))]
    ks = [dict(stage=0, delay=0.0, rot=0.0)]
    for stg, dl, pos in seq:
        ks.append(dict(stage=stg, delay=dl, dur=0.3, rot=f2_ang(pos) - F2_ANG0))
    parts.append(dict(_part("handle", f2_handle_svg(), R["pos"], pivot=F2_PIV, keys=ks),
                      geo=dict(kind="f2handle", seq=[[s, d, p] for s, d, p in seq])))
    parts.append(dict(_part("band", f2_band_bg_svg(view), R[view], keys=_at_keys(0, 0.0, 0.4)), geo=dict(kind="f2band", view=view)))
    for k, (nm, x0, x1, t, stg, dl, row) in enumerate(f2_segs(view)):
        parts.append(dict(_part(f"seg{k}", f2_seg_svg(nm, x0, x1, t, row), R[view], keys=_at_keys(stg, dl, 0.3)),
                          geo=dict(kind="f2seg", n=nm, x0=x0, x1=x1, pps=F2_PPS, t=t, stage=stg, delay=dl)))
    if start["switch"] == "on":
        parts.append(_switch_part("正面から見ると"))
    return parts


def _f2_anchors(st):
    return dict(dial=_polar(f2_ang("非常"), F2_RAD + 30), band=(F2_BAND["x0"], F2_BAND["y"]))


def _f2_note(st0, states):
    return "段の並びは国交省の位置図・角度は模式・帯の幅は記録の秒（ごく短い段は細い帯）"


# ══════════════════════════════════════════════════════════
#  F3 交信の流れ（c306 start・c314 later）
# ══════════════════════════════════════════════════════════
F3_COL = dict(disp=(420.0, "総合指令所の指令員"), cond=(960.0, "7両目の車掌"), drv=(1500.0, "1両目の運転士"))
F3_HEAD_Y = 196.0
F3_LIFE = (262.0, 700.0)
F3_AX = dict(x0=300.0, x1=1620.0, y=790.0, t0=(9, 17, 50), t1=(9, 19, 0))
F3_DOT = dict(start=(9, 17, 57), ans=(9, 18, 40))
# 吹き出し＝(言う側, 聞く側, 字, 出典)。🔧 ⑤b-4 の qa_all：交信記録の字句をそのまま出すと語り（同じ言葉を読む）の複写（門番 echo）
#   ＝誰が何をしたかの短い言い方（「」を付けない＝引用に見せない）。要の語（遅れ・1分半）は R1 p.77 の記録の語（門番 ㊹）
F3_SAY = dict(ask=("disp", "cond", "遅れの時間を問う", "R1 p77（えー、遅れにつきましては、何分でしょうか。どうぞ）"),
              ans=("cond", "disp", "1分半と答える", "R1 p77（あ、1分半です。どうぞ）"))
F3_LAB = "交信の流れ（列車無線）"
F3_REC = dict(
    who="R1 p13（交信記録ファイル「204T091757a」は、本件列車が猪名寺駅~塚口駅間上り第1閉そく信号機付近を走行しているときから）・"
        "R1 p77（本件車掌と総合指令所の輸送指令員Aとの列車無線による交信の記録ファイル）",
    start="R1 p77（01時23分45秒から開始された交信記録であれば「204T012345a」とされている）",
    ans="付図24 p5023（交信の時刻＝9時18分40秒ごろ）",
)


def f3_sec(hms):
    return hms[0] * 3600 + hms[1] * 60 + hms[2]


def f3_x(hms):
    a = F3_AX
    return a["x0"] + (f3_sec(hms) - f3_sec(a["t0"])) / (f3_sec(a["t1"]) - f3_sec(a["t0"])) * (a["x1"] - a["x0"])


def f3_cols_svg():
    g = []
    for key, (x, name) in F3_COL.items():
        w = _tw(name, 34) + 56
        g.append(_rect(x - w / 2, F3_HEAD_Y - 48, w, 70, C25["col_bg"], C25["col_ln"], 3.0, rx=12, extra=f' data-k="col" data-c="{key}"'))
        g.append(_text(x, F3_HEAD_Y, name, 34, C25["ink"], extra=' data-k="role"'))
        g.append(_line(x, F3_LIFE[0], x, F3_LIFE[1], C25["col_ln"], 3.0, ' stroke-dasharray="10 12"'))
    return "".join(g)


def f3_axis_svg():
    a = F3_AX
    return (_line(a["x0"] - 20, a["y"], a["x1"] + 20, a["y"], C25["axis"], 5.0)
            + _text(a["x0"] - 30, a["y"] + 48, "秒の帯（点の位置は時刻の比）", 26, C25["dim"], anchor="start"))


def f3_dot_svg(key):
    x = f3_x(F3_DOT[key])
    return f'<circle cx="{x:.1f}" cy="{F3_AX["y"]:.1f}" r="13" fill="{C25["time"]}" stroke="{C25["ol"]}" stroke-width="3" data-k="dot" data-d="{key}"/>'


def f3_call_svg():
    """車掌が列車無線で指令所を呼ぶ（矢印と電波の印）＝言葉は出さない"""
    xc, xd = F3_COL["cond"][0], F3_COL["disp"][0]
    y = 400.0
    g = [_arrow((xc - 20, y), (xd + 24, y), C25["radio"], 8.0, 26.0),
         _text((xc + xd) / 2, y - 30, "列車無線で呼ぶ", 34, C25["radio"])]
    for r in (18, 32, 46):
        g.append(f'<path d="M {xc + 10:.1f} {y - r:.1f} A {r} {r} 0 0 1 {xc + 10:.1f} {y + r:.1f}" fill="none" stroke="{C25["radio"]}" stroke-width="4"/>')
    return "".join(g)


def f3_bubble_svg(key, y):
    who, to, t, _rec = F3_SAY[key]
    x, xt = F3_COL[who][0], F3_COL[to][0]
    s = 38
    w, h = _tw(t, s) + 60, 84.0
    bx = x - w / 2 if who != "disp" else x - 70
    bx = min(max(bx, 96.0), W - 96.0 - w)
    tip_x = x + (40 if xt > x else -40)
    g = [_path([(tip_x - 18, y + h - 2), (x, y + h + 40), (tip_x + 18, y + h - 2)], C25["bubble"], C25["bubble_ln"], 3.0),
         _rect(bx, y, w, h, C25["bubble"], C25["bubble_ln"], 3.0, rx=22, extra=f' data-k="bubble" data-w="{who}"'),
         _text(bx + w / 2, y + 56, t, s, C25["bubble_ink"], ol=False, extra=f' data-k="say" data-w="{who}"')]
    return "".join(g)


def _scene_F3(start, states, steps):
    allst = [start] + states
    _head_only("F3", start, states, ("view", "switch"))
    view = start["view"]
    R = F3_REC
    parts = [_part("bg", _bg_svg(), R["who"]),
             dict(_part("cols", f3_cols_svg(), R["who"]), geo=dict(kind="f3cols", cols={k: v[0] for k, v in F3_COL.items()})),
             dict(_part("axis", f3_axis_svg(), R["start"]),
                  geo=dict(kind="f3axis", x0=F3_AX["x0"], x1=F3_AX["x1"], t0=list(F3_AX["t0"]), t1=list(F3_AX["t1"])))]
    on = lambda f: (lambda st: st[f] == "on")       # noqa: E731
    if any(st["f3call"] == "on" for st in allst):
        parts.append(dict(_part("call", f3_call_svg(), R["who"], keys=_akeys(start, states, steps, on("f3call"), 0.6)),
                          geo=dict(kind="f3call")))
    # 交信の始まりの点：start は2行目（録音のファイル名の時刻）から・later は頭から（前のカットの続き）
    parts.append(dict(_part("dot_start", f3_dot_svg("start"), R["start"], keys=_akeys(start, states, steps, on("f3t0"), 0.4)),
                      geo=dict(kind="f3dot", d="start", x=f3_x(F3_DOT["start"]), t=list(F3_DOT["start"]))))
    if any(st["f3ask"] == "on" for st in allst):
        parts.append(dict(_part("ask", f3_bubble_svg("ask", 300.0), F3_SAY["ask"][3], keys=_akeys(start, states, steps, on("f3ask"), 0.5)),
                          geo=dict(kind="f3say", key="ask", who=F3_SAY["ask"][0], t=F3_SAY["ask"][2])))
    if any(st["f3ans"] == "on" for st in allst):
        parts.append(dict(_part("ans", f3_bubble_svg("ans", 470.0), F3_SAY["ans"][3], keys=_akeys(start, states, steps, on("f3ans"), 0.5)),
                          geo=dict(kind="f3say", key="ans", who=F3_SAY["ans"][0], t=F3_SAY["ans"][2])))
        parts.append(dict(_part("dot_ans", f3_dot_svg("ans"), R["ans"], keys=_akeys(start, states, steps, on("f3ans"), 0.4)),
                          geo=dict(kind="f3dot", d="ans", x=f3_x(F3_DOT["ans"]), t=list(F3_DOT["ans"]))))
    if start["switch"] == "on":
        parts.append(_switch_part("交信を並べると"))
    return parts


def _f3_anchors(st):
    y = F3_AX["y"] - 14
    return dict(t_start=(f3_x(F3_DOT["start"]), y), t_ans=(f3_x(F3_DOT["ans"]), y),
                cond=(F3_COL["cond"][0], F3_HEAD_Y + 30), disp=(F3_COL["disp"][0], F3_HEAD_Y + 30))


def _f3_note(st0, states):
    return "吹き出しは交信記録の要約・人は役職だけ"


# ══════════════════════════════════════════════════════════
#  F4 ATS の照査（c703 basic・c719 if）＝速さと距離の図（解説 図-5 の形・数は描かない）
# ══════════════════════════════════════════════════════════
F4_AX = dict(x0=240.0, x1=1680.0, y0=660.0, ytop=230.0)
F4_CURVE_X = 1300.0                                 # 曲線の入口（模式）
F4_LIMIT_Y = 540.0                                  # 曲線の制限速度の高さ（模式）
F4_PAT = dict(flat_y=300.0, bend_x=800.0)           # 照らす速度の線＝高い所から曲線の入口で制限の高さへ
F4_TRAIN = dict(y=450.0, slope=0.26)                # 列車の速さ（加速して照らす速度の線にぶつかる＝模式）
F4_REAL = dict(y=360.0, end=F4_CURVE_X + 70.0)      # 実際の速さ（照らしなし＝高いまま曲線へ・その先は描かない）
F4_COIL_X = 420.0                                   # 線路の装置（P地上子・模式の位置）
F4_LAB = dict(basic="速さと進んだ距離の図（ATS が速さを照らす）", **{"if": "速さと進んだ距離の図（もし曲線の照らしがあったら）"})
F4_REC = dict(
    fig="S1k p10039（図-5 曲線速照機能のイメージ＝照査速度・制限速度・曲線部・常用最大ブレーキ）",
    basic="S1k p10039（図-5 曲線速照機能のイメージ）",
    real="R1 p13（塚口駅上り出発信号機6Lを速度約122km/hで通過し・上り第4閉そく信号機を速度約118km/hで通過した）",
    max="R1 p230（もしP曲線速照機能が使用開始されていれば・本件曲線の手前で最大Bが作動し、本事故の発生は回避できたものと推定される）",
)


def f4_pat_y(x):
    p = F4_PAT
    if x <= p["bend_x"]:
        return p["flat_y"]
    if x >= F4_CURVE_X:
        return F4_LIMIT_Y
    u = (x - p["bend_x"]) / (F4_CURVE_X - p["bend_x"])
    return p["flat_y"] + (F4_LIMIT_Y - p["flat_y"]) * u * u


def f4_train_y(x):
    return F4_TRAIN["y"] - (x - F4_AX["x0"]) * F4_TRAIN["slope"]


def f4_real_y(x):
    x1 = F4_AX["x0"] + 300.0
    return F4_REAL["y"] + 40.0 * max(0.0, (x1 - x) / 300.0)


def f4_meet(view="basic"):
    """速さの線（basic＝列車の速さ・if＝実際の速さ）が照らす速度の線にぶつかる x（二分法）＝そこからブレーキ"""
    fn = f4_train_y if view == "basic" else f4_real_y
    a, b = F4_AX["x0"], F4_CURVE_X
    for _ in range(60):
        m = (a + b) / 2
        if fn(m) > f4_pat_y(m):
            a = m
        else:
            b = m
    return (a + b) / 2


def _f4_pts(fn, x0, x1, n=80):
    return [(x0 + (x1 - x0) * k / n, fn(x0 + (x1 - x0) * k / n)) for k in range(n + 1)]


def f4_axes_svg():
    a = F4_AX
    g = [_line(a["x0"], a["y0"], a["x1"] + 30, a["y0"], C25["axis"], 4.0), _line(a["x0"], a["y0"], a["x0"], a["ytop"] - 20, C25["axis"], 4.0),
         _path([(a["x0"] - 12, a["ytop"] - 10), (a["x0"], a["ytop"] - 34), (a["x0"] + 12, a["ytop"] - 10)], C25["axis"]),
         _text(a["x0"] + 22, a["ytop"] - 4, "速さ", 32, C25["dim"], anchor="start"),
         _text(a["x1"] + 30, a["y0"] + 50, "進む向き →", 30, C25["dim"], anchor="end")]
    # 線路の帯・装置・曲線の範囲
    ty = a["y0"] + 100
    g += [_line(a["x0"], ty, a["x1"], ty, C25["rail"], 6.0),
          _path([(F4_COIL_X - 18, ty - 4), (F4_COIL_X, ty - 34), (F4_COIL_X + 18, ty - 4)], C25["blue"], C25["ol"], 2.0),
          _text(F4_COIL_X, ty + 46, "線路の装置", 28, C25["dim"]),
          _line(F4_CURVE_X, ty - 26, F4_CURVE_X, ty + 26, C25["amber"], 5.0), _line(a["x1"], ty - 26, a["x1"], ty + 26, C25["amber"], 5.0),
          _line(F4_CURVE_X, ty, a["x1"], ty, C25["amber"], 10.0),
          _text((F4_CURVE_X + a["x1"]) / 2, ty + 50, "曲線", 30, C25["amber"]),
          _line(F4_CURVE_X, a["ytop"], F4_CURVE_X, ty - 30, C25["amber"], 2.0, ' stroke-dasharray="8 10" opacity="0.6"')]
    return "".join(g)


def f4_pat_svg():
    pts = _f4_pts(f4_pat_y, F4_AX["x0"], F4_AX["x1"], 140)
    xl = F4_AX["x0"] + 40
    return (_path(pts, "none", C25["ol"], 12.0, op=0.5, close=False)
            + _path(pts, "none", C25["pat"], 6.0, close=False, extra=' stroke-dasharray="16 10"')
            + _text(xl, F4_PAT["flat_y"] - 24, "照らす速度（決まりの線）", 32, C25["pat"], anchor="start")
            + _text(F4_AX["x1"], F4_LIMIT_Y + 52, "曲線の制限速度", 28, C25["pat"], anchor="end"))


def f4_train_svg():
    xm = f4_meet()
    pts = _f4_pts(f4_train_y, F4_AX["x0"], xm, 40)
    return (_path(pts, "none", C25["ol"], 12.0, op=0.5, close=False) + _path(pts, "none", C25["speed"], 6.0, close=False)
            + _text(F4_AX["x0"] + 40, F4_TRAIN["y"] + 46, "列車の速さ", 32, C25["speed"], anchor="start"))


def f4_brake_svg(label, view):
    xm = f4_meet(view)
    pts = _f4_pts(f4_pat_y, xm, F4_CURVE_X, 60)
    after = [(F4_CURVE_X, F4_LIMIT_Y), (F4_AX["x1"], F4_LIMIT_Y)]
    xl = (xm + F4_CURVE_X) / 2
    return (_path(pts, "none", C25["ol"], 14.0, op=0.5, close=False) + _path(pts, "none", C25["brake"], 8.0, close=False)
            + _path(after, "none", C25["speed"], 6.0, close=False)
            + _text(xl - 30, f4_pat_y(xl) + 64, label, 34, C25["brake"], anchor="end"))


def f4_real_svg():
    pts = [(F4_AX["x0"], f4_real_y(F4_AX["x0"])), (F4_AX["x0"] + 300, F4_REAL["y"]), (F4_REAL["end"], F4_REAL["y"])]
    return (_path(pts, "none", C25["ol"], 12.0, op=0.5, close=False) + _path(pts, "none", C25["real"], 6.0, close=False)
            + f'<circle cx="{F4_REAL["end"]:.1f}" cy="{F4_REAL["y"]:.1f}" r="9" fill="{C25["real"]}"/>'
            + _text(F4_AX["x0"] + 40, F4_REAL["y"] - 22, "実際の速さ（照らしなし）", 30, C25["real"], anchor="start"))


def f4_say_svg():
    # 🔧 ⑤b-4 の qa_all：「事故の発生は回避できたものと推定される（報告書）」は語りの3行目の複写（門番 echo 86%）＝短い結びに
    t = "報告書の推定＝事故は回避できた"
    w = _tw(t, 34) + 60
    x, y = 960.0 - w / 2, 150.0
    return (_rect(x, y, w, 68, C25["card"], C25["amber"], 3.0, rx=12) + _text(960.0, y + 47, t, 34, C25["amber"], extra=' data-k="say"'))


def _scene_F4(start, states, steps):
    allst = [start] + states
    _head_only("F4", start, states, ("view", "switch"))
    view = start["view"]
    R = F4_REC
    on = lambda f: (lambda st: st[f] == "on")       # noqa: E731
    xm = f4_meet(view)
    parts = [_part("bg", _bg_svg(), R["fig"]),
             dict(_part("axes", f4_axes_svg(), R["fig"]), geo=dict(kind="f4axes", curve_x=F4_CURVE_X, x1=F4_AX["x1"], coil_x=F4_COIL_X)),
             dict(_part("pat", f4_pat_svg(), R["fig"]),
                  geo=dict(kind="f4pat", y_at_curve=f4_pat_y(F4_CURVE_X), limit_y=F4_LIMIT_Y, y_flat=F4_PAT["flat_y"]))]
    if view == "if":
        parts.append(dict(_part("real", f4_real_svg(), R["real"]), geo=dict(kind="f4real", end=F4_REAL["end"])))
    else:
        parts.append(dict(_part("speed", f4_train_svg(), R["basic"]), geo=dict(kind="f4speed", meet=xm)))
    if any(st["f4brake"] == "on" for st in allst):
        lab = "自動でブレーキ" if view == "basic" else "最大のブレーキ"
        parts.append(dict(_part("brake", f4_brake_svg(lab, view), R["basic"] if view == "basic" else R["max"],
                                keys=_akeys(start, states, steps, on("f4brake"), 0.9)),
                          geo=dict(kind="f4brake", x0=xm, x_end=F4_CURVE_X, y_end=f4_pat_y(F4_CURVE_X), label=lab)))
    if any(st["f4say"] == "on" for st in allst):
        parts.append(dict(_part("say", f4_say_svg(), R["max"], keys=_akeys(start, states, steps, on("f4say"), 0.6)),
                          geo=dict(kind="f4say")))
    if start["switch"] == "on":
        parts.append(_switch_part("速さで見ると"))
    return parts


def _f4_anchors(st):
    xm = f4_meet(st["view"])
    return dict(meet=(xm, f4_pat_y(xm)), curve=(F4_CURVE_X, F4_LIMIT_Y), coil=(F4_COIL_X, F4_AX["y0"] + 70))


def _f4_note(st0, states):
    return "模式（解説の図-5 の形・速さの数は描かない）"


# ══════════════════════════════════════════════════════════
#  F5 付け替えの前後（c603）＝上から見た曲線の重ね
# ══════════════════════════════════════════════════════════
F5_PPM = 0.9                                        # 1m＝0.9画素（前といまで同じ目盛り）
F5_Y0 = 290.0
F5_X_OLD = 330.0                                    # 前の曲線の入口（模式＝手前で分かれる・空中写真の形）
F5_X_NEW = 700.0                                    # いまの曲線の入口（模式＝先まで来て急に曲がる）
F5_NEW = (60.0, 304.0, 188.0, 60.0)                 # 付図73
F5_OLD_R = 600.0                                    # R1 p.72（それまで半径600mの右曲線であった区間）
F5_TAIL = 520.0
F5_LAB = "上から見た曲線（付け替えの前といま）"
F5_REC = dict(
    new="付図73 p7005（緩和曲線長さ60m・円曲線半径304m長さ188m）・R1 p72（半径304m、曲線長308m・60mが緩和曲線）",
    old="R1 p72（それまで半径600mの右曲線であった区間が、平成8年12月20日に）・空中写真 p1（1974〜78年・1984〜86年の層＝曲線は手前で分かれて緩い）",
    len="R1 p72（半径304m、曲線長308mの右曲線となっており、そのうち上り1k949mから上り1k889mまでの60mが緩和曲線）",
)


def f5_new():
    return track_pts(F5_X_NEW, F5_Y0, F5_PPM, F5_NEW, tail=F5_TAIL)


def f5_old_pts():
    """前の曲線＝半径600m の円弧（いまの曲線と同じ向きまで曲がる＝模式）"""
    _pts, (m1, m2, m3) = f5_new()
    l1, r, lc, l2 = F5_NEW
    th = (l1 / 2 + lc + l2 / 2) / r                 # いまの曲線の曲がりの角度（緩和曲線は半分ずつ）
    R = F5_OLD_R * F5_PPM
    cx, cy = F5_X_OLD, F5_Y0 + R
    pts = [(F5_X_OLD - 260.0, F5_Y0)] + [(cx + R * math.sin(th * k / 80), cy - R * math.cos(th * k / 80)) for k in range(81)]
    ex, ey = pts[-1]
    pts.append((ex + math.cos(th) * F5_TAIL * F5_PPM, ey + math.sin(th) * F5_TAIL * F5_PPM))
    return pts, R, th


def f5_old_svg():
    pts, R, th = f5_old_pts()
    xm, ym = pts[1 + 40]
    return (_path(pts, "none", C25["ol"], 18.0, op=0.5, close=False)
            + _path(pts, "none", C25["old"], 9.0, close=False, extra=' stroke-dasharray="22 14"')
            + _text(xm - 40, ym + 80, "付け替えの前（半径600m）", 34, C25["old"], anchor="end", extra=' data-k="old"'))


def f5_new_svg():
    pts, (m1, m2, m3) = f5_new()
    head = [(80.0, F5_Y0), (F5_X_NEW, F5_Y0)]
    cv = _sub(pts, F5_PPM, 0, 0.0, m3, 0)
    xm, ym = cv[len(cv) // 2]
    return (_path(head + pts[2:], "none", C25["ol"], 20.0, op=0.55, close=False)
            + _path(head + pts[2:], "none", C25["rail"], 8.0, close=False)
            + _path(cv, "none", C25["new"], 12.0, close=False)
            + _text(xm + 40, ym - 20, "いま（半径304m）", 36, C25["new"], anchor="start", extra=' data-k="new"'))


def f5_len_svg():
    pts, (m1, m2, m3) = f5_new()
    tr = _sub(pts, F5_PPM, 0, 0.0, m1, 0)
    cv = _sub(pts, F5_PPM, 0, 0.0, m3, 0)
    x0, y0 = tr[0]
    xe, ye = cv[-1]
    return (_path(cv, "none", C25["ink"], 4.0, close=False, extra=' stroke-dasharray="4 8"')
            + _path(tr, "none", C25["ol"], 22.0, op=0.5, close=False) + _path(tr, "none", C25["trans"], 14.0, close=False)
            + _text(x0 + 10, y0 - 60, "入口の60m（ゆるやかに曲がり始める）", 32, C25["trans"], anchor="start", extra=' data-k="trans"')
            + _text(xe + 40, ye + 10, "曲線の長さ 308m", 36, C25["ink"], anchor="start", extra=' data-k="len"'))


def _scene_F5(start, states, steps):
    allst = [start] + states
    _head_only("F5", start, states, ("view", "switch"))
    R = F5_REC
    on = lambda f: (lambda st: st[f] == "on")       # noqa: E731
    pts, marks = f5_new()
    opts, oR, th = f5_old_pts()
    parts = [_part("bg", _bg_svg(), R["new"])]
    parts.append(dict(_part("old", f5_old_svg(), R["old"], keys=_akeys(start, states, steps, on("f5old"), 0.8)),
                      geo=dict(kind="f5old", radius=oR, ppm=F5_PPM, x_in=F5_X_OLD)))
    parts.append(dict(_part("new", f5_new_svg(), R["new"], keys=_akeys(start, states, steps, on("f5new"), 0.8, extra=1.4)),
                      geo=dict(kind="f5new", x_in=F5_X_NEW, **_shape_geo(pts, marks, F5_PPM))))
    if any(st["f5len"] == "on" for st in allst):
        parts.append(dict(_part("len", f5_len_svg(), R["len"], keys=_akeys(start, states, steps, on("f5len"), 0.8)),
                          geo=dict(kind="f5len")))
    if start["switch"] == "on":
        parts.append(_switch_part("上から見ると"))
    return parts


def _f5_anchors(st):
    return dict(new_in=(F5_X_NEW, F5_Y0), old_in=(F5_X_OLD, F5_Y0))


def _f5_note(st0, states):
    return "曲線の位置の関係は模式（半径と長さの比は記録の値）"


# ══════════════════════════════════════════════════════════
#  F6 宝塚の分岐器（c207）＝上から見た宝塚駅の略図（付図28 その1）
# ══════════════════════════════════════════════════════════
F6_KM0, F6_X0, F6_PPM = 17.930, 150.0, 5.9         # 下り17k930m を x 150 に・1m＝5.9画素（下りは右へ＝キロ程が増える）
F6_KM = dict(coil=17.981, sign40=18.008, home=18.149)   # 付図28 その1（ATS-SW形地上子(ロング)・速度制限標識(40)・ホーム端位置）
F6_TURN = (18.012, 18.085)                          # 31号イ分岐器の始めと終わり（模式＝「40」の標識の先・ホームの手前）
F6_Y = dict(main=430.0, home2=580.0, up=740.0)
F6_TIME = "8:54:43ごろ"
F6_LAB = "上から見た宝塚駅の略図（尼崎から来て2番線へ）"
F6_REC = dict(
    km="付図28 p5037（ATS-SW形地上子(ロング)5・6RQ1 下り17k981m・速度制限標識(分岐側を2番線に走行する場合、40km/h)下り18k008m・"
       "ホーム端位置 下り18k149m・31号イ分岐器）",
    ats="R1 p9（8時54分43秒ごろ2.13.2に記述するSWロング機能による非常Bが作動した）",
    turn="R1 p9（31号イ分岐器の箇所に・制限速度である40km/hを超えた約65km/hで進入した）",
)


def f6_x(km):
    return F6_X0 + (km - F6_KM0) * 1000.0 * F6_PPM


def f6_turn_pts():
    x0, x1 = f6_x(F6_TURN[0]), f6_x(F6_TURN[1])
    y0, y1 = F6_Y["main"], F6_Y["home2"]
    pts = []
    for k in range(41):
        u = k / 40
        pts.append((x0 + (x1 - x0) * u, y0 + (y1 - y0) * (3 * u * u - 2 * u * u * u)))
    return pts


def f6_base_svg():
    ym, y2, yu = F6_Y["main"], F6_Y["home2"], F6_Y["up"]
    xh = f6_x(F6_KM["home"])
    g = [_rect(xh, y2 + 34, W - 40 - xh, yu - y2 - 70, C25["plat"], C25["plat_ln"], 3.0, rx=6),
         _text(xh + 24, y2 + 104, "2番線のホーム（宝塚駅）", 30, C25["ink"], anchor="start"),
         _rect(xh, ym - 104, W - 40 - xh, 64, C25["plat"], C25["plat_ln"], 3.0, rx=6),
         _text(xh + 30, ym - 60, "1番線のホーム", 28, C25["dim"], anchor="start")]
    for y, dash in ((ym, ""), (y2, ""), (yu, ' stroke-dasharray="18 12"')):
        x_start = 40.0 if y != y2 else f6_x(F6_TURN[1])
        g.append(_line(x_start, y, W - 40, y, C25["rail_ol"], 18.0, dash))
        g.append(_line(x_start, y, W - 40, y, C25["rail"], 7.0, dash))
    tp = f6_turn_pts()
    g.append(_path(tp, "none", C25["rail_ol"], 18.0, close=False) + _path(tp, "none", C25["rail"], 7.0, close=False))
    g.append(_text(84.0, yu - 22, "上り線", 28, C25["dim"], anchor="start"))
    g.append(_arrow((70.0, ym + 100), (250.0, ym + 100), C25["dim"], 5.0, 18.0))
    g.append(_text(70.0, ym + 76, "尼崎から（下り）", 28, C25["dim"], anchor="start"))
    # ATS の地上子・「40」の標識・分岐器の名
    xc, xs = f6_x(F6_KM["coil"]), f6_x(F6_KM["sign40"])
    g += [_rect(xc - 12, ym - 12, 24, 24, C25["coil"], C25["ol"], 2.0, extra=' data-k="coil"'),
          _text(xc, ym + 66, "ATS の地上子", 30, C25["ink"]),
          _line(xs, ym - 26, xs, ym - 96, C25["sig_pole"], 5.0),
          _rect(xs - 34, ym - 160, 68, 64, C25["sign"], C25["ol"], 3.0, rx=6, extra=' data-k="sign"'),
          _text(xs, ym - 114, "40", 40, C25["ol"], ol=False, extra=' data-k="sign40"'),
          _text((f6_x(F6_TURN[0]) + f6_x(F6_TURN[1])) / 2 + 40, (ym + y2) / 2 - 20, "分岐器", 30, C25["dim"], anchor="start")]
    return "".join(g)


def f6_time_svg():
    w = _tw(F6_TIME, 44) + 60
    return (_rect(960.0 - w / 2, 150.0, w, 72, C25["card"], C25["time"], 3.0, rx=12)
            + _text(960.0, 202.0, F6_TIME, 44, C25["time"], extra=' data-k="time"'))


def f6_turn_hl_svg():
    tp = f6_turn_pts()
    return (_path(tp, "none", C25["ol"], 30.0, op=0.5, close=False) + _path(tp, "none", C25["amber"], 18.0, close=False)
            + _path(tp, "none", C25["rail"], 5.0, close=False))


def f6_ring_svg():
    x = f6_x(F6_KM["coil"])
    return (f'<circle cx="{x:.1f}" cy="{F6_Y["main"]:.1f}" r="60" fill="none" stroke="{C25["ol"]}" stroke-opacity="0.5" stroke-width="12"/>'
            f'<circle cx="{x:.1f}" cy="{F6_Y["main"]:.1f}" r="60" fill="none" stroke="{C25["red"]}" stroke-width="6"/>')


def _scene_F6(start, states, steps):
    allst = [start] + states
    _head_only("F6", start, states, ("view", "switch"))
    R = F6_REC
    on = lambda f: (lambda st: st[f] == "on")       # noqa: E731
    xs = {k: f6_x(v) for k, v in F6_KM.items()}
    parts = [_part("bg", _bg_svg(), R["km"]),
             dict(_part("base", f6_base_svg(), R["km"]),
                  geo=dict(kind="f6base", x0=F6_X0, km0=F6_KM0, ppm=F6_PPM, xs=xs, turn=[f6_x(F6_TURN[0]), f6_x(F6_TURN[1])]))]
    if any(st["f6time"] == "on" for st in allst):
        parts.append(dict(_part("time", f6_time_svg(), R["ats"], keys=_akeys(start, states, steps, on("f6time"), 0.5)),
                          geo=dict(kind="f6time", t=F6_TIME)))
    if any(st["f6ats"] == "on" for st in allst):
        pulse = [dict(stage=i, delay=float(sp.get("ring_delay", 0.4)), n=2, **IL.RING_KIND["out"])
                 for i, (st, sp) in enumerate(zip(states, steps)) if st["f6ats"] == "on" and allst[i]["f6ats"] != "on"]
        parts.append(dict(_part("ats", f6_ring_svg(), R["ats"], (xs["coil"], F6_Y["main"])), kind="ring", pulse=pulse,
                          geo=dict(kind="f6ats", x=xs["coil"])))
    if any(st["f6turn"] == "on" for st in allst):
        parts.append(dict(_part("turn", f6_turn_hl_svg(), R["turn"], keys=_akeys(start, states, steps, on("f6turn"), 0.8)),
                          geo=dict(kind="f6turn")))
    if start["switch"] == "on":
        parts.append(_switch_part("上から見ると"))
    return parts


def _f6_anchors(st):
    ym = F6_Y["main"]
    tp = f6_turn_pts()
    return dict(coil=(f6_x(F6_KM["coil"]), ym - 14), sign40=(f6_x(F6_KM["sign40"]) + 34, ym - 128), turn=tp[len(tp) // 2])


def _f6_note(st0, states):
    return "地上子・標識・ホームの端の間の距離の比はキロ程・分岐器の位置と長さ・線の間隔は模式"


# ══════════════════════════════════════════════════════════
#  登録
# ══════════════════════════════════════════════════════════
F1_AT = tuple(F1_KM)


def register():
    IL.FIELDS.update(
        F1=dict(view="all", f1at="itami", f1hl="off", switch="off", cam=1.0),
        F2=dict(view="early", switch="off", cam=1.0),
        F3=dict(view="start", f3call="off", f3t0="off", f3ask="off", f3ans="off", switch="off", cam=1.0),
        F4=dict(view="basic", f4brake="off", f4say="off", switch="off", cam=1.0),
        F5=dict(view="plan", f5old="off", f5new="off", f5len="off", switch="off", cam=1.0),
        F6=dict(view="plan", f6time="off", f6ats="off", f6turn="off", switch="off", cam=1.0))
    IL.CHOICES.update(f1at=F1_AT, f1hl=IL.ONOFF, f3call=IL.ONOFF, f3t0=IL.ONOFF, f3ask=IL.ONOFF, f3ans=IL.ONOFF,
                      f4brake=IL.ONOFF, f4say=IL.ONOFF, f5old=IL.ONOFF, f5new=IL.ONOFF, f5len=IL.ONOFF,
                      f6time=IL.ONOFF, f6ats=IL.ONOFF, f6turn=IL.ONOFF)
    IL.VIEWS.update(F1=("all", "near"), F2=("early", "late"), F3=("start", "later"), F4=("basic", "if"), F5=("plan",), F6=("plan",))
    IL.REC_FIELDS = IL.REC_FIELDS + ("f1at", "f1hl", "f3call", "f3t0", "f3ask", "f3ans", "f4brake", "f4say", "f5old", "f5new", "f5len",
                                     "f6time", "f6ats", "f6turn")
    IL.NOTE.update(F1=_f1_note, F2=_f2_note, F3=_f3_note, F4=_f4_note, F5=_f5_note, F6=_f6_note)
    IL.EXTRA.update(
        F1=dict(scene=_scene_F1, anchors=_f1_anchors, camc=lambda st0, states: (960.0, 540.0),
                label=lambda st0, states: F1_LAB[st0["view"]]),
        F2=dict(scene=_scene_F2, anchors=_f2_anchors, camc=lambda st0, states: (960.0, 540.0), label=lambda st0, states: F2_LAB),
        F3=dict(scene=_scene_F3, anchors=_f3_anchors, camc=lambda st0, states: (960.0, 540.0), label=lambda st0, states: F3_LAB),
        F4=dict(scene=_scene_F4, anchors=_f4_anchors, camc=lambda st0, states: (960.0, 540.0),
                label=lambda st0, states: F4_LAB[st0["view"]]),
        F5=dict(scene=_scene_F5, anchors=_f5_anchors, camc=lambda st0, states: (960.0, 540.0), label=lambda st0, states: F5_LAB),
        F6=dict(scene=_scene_F6, anchors=_f6_anchors, camc=lambda st0, states: (960.0, 540.0), label=lambda st0, states: F6_LAB))


register()
