# -*- coding: utf-8 -*-
"""illu17.py — 案C の再現イラスト：17本目（中華航空140便・B-1816・1994-04-26・名古屋空港）の置き場 C1・C2・C3（⑤b-3・2026-10-20 新設）。

`tools/illu.py` の末尾で読み込み、型の表（FIELDS・CHOICES・VIEWS・REC_FIELDS・NOTE）と置き場の登録 `illu.EXTRA` へ足す（20本目 illu20 と同じ作り）。
🔴 §0b（題材を替えるとき）：このファイルは17本目の型の値そのもの＝次の回は読み込みを外すか、置き場の名がぶつからないか確かめる。

■ 置き場（映像方針 17本目 §4・§5・一覧 `ref/ep17/eizou_list17.md` の C1〜C3）
  C1 … 操縦士の前の画面の上の端（FMA＝いまの飛び方の表示）。形と字＝報告書の付図29「FMA表示の推定」（p135・8つの枠 14'00"〜15'13"＝
       なぞってよい＝PDL1.0 の「加工して作成」）。🔴 付図29 は「推定」＝出典の行に「付図29（推定）」（`cuts.ss.REC_DOCS` の名）。
       時刻＝付図29 の枠の時刻は世界共通の時刻（11時14分00秒）＝画面は日本の時刻（＋9時間＝20:14:00）。
       view＝all（画面ぜんたい＝上の端＋姿勢・速さ・方位・下り道のずれの目盛り＝形は模式）／band（上の端の寄り）／time（上の端＋時刻の帯）。
       欄＝c1f（枠 "1400"〜"1513"）・c1ring（輪 off／gsloc／ga／dual／thr／fd）・c1eye（目の印＝見た向き・人は描かない）・
       c1land（LAND のボタン off／on／press＝押しても GO AROUND は消えない）・c1cur（時刻の帯の線 off／"20:14:30" など）・
       c1att（姿勢 level／up＝15'13" の機首上げ 25度超・傾きは模式）・switch（頭だけ）
  C2 … 尾翼を横から見た図（機首が左）。水平安定板と昇降舵の2つの動く所（形は模式＝付図15 の位置と数だけ・角度は記録の値）。
       回る所＝昇降舵のちょうつがい（模式＝水平安定板の後ろの端で回すと、昇降舵がはなれない）。
       欄＝c2kind（rec＝記録の角度の場面／model＝しくみの説明＝角度も模式・頭だけ）・c2ths（水平安定板の角度・度・負＝機首上げ＝前の端が下がる）・
       c2elev（昇降舵の角度・度・水平安定板に対して・正＝機首下げ＝後ろの端が下がる）・c2ap（水平安定板を自動操縦の色＝水色）・
       c2hand（昇降舵を手の色＝橙）・c2hl（輪 off／both／ths／elev）・c2arrow（矢印 off／ap／hand）・c2ghost（−5.3度の形の点線＝頭だけ）・
       c2arc（−5.3度→−12.3度の弧）・c2lim（機首上げの限界の印）・switch
  C3 … 操縦室の中（後ろから前を向いて・夜）。人は影の手だけ（顔・体を描かない＝腕は画面の下の端から）。
       欄＝c3thr（副操縦士の手がスラスト・レバーに）・c3yoke（副操縦士の手が右の操縦輪に）・c3push（右の操縦輪を押す）・
       c3cap（機長の手が左の操縦輪に）・c3ap（自動操縦の灯 AP 1・AP 2）・c3ring（輪 off／go／at／lev）・switch
  🆕 ⑤b-4（2026-10-20）C4〜C7（C9 年表・C10 帯は軸の型 axis に替えた＝入力 assign17.psv・門番 check_axis）
  C4 … 進入の断面図（横から・滑走路は右）。線の形と時刻の位置＝付図4（p109 航跡概略図）を画素から読んだ `ref/ep17/c4_path.json`
       （`ref/ep17/make_c4path.py`）。高さは横より伸ばす（all 約7倍・near 約4倍＝見る向きの札に書く）。🔴 線は頂点（20:15:31）で止める。
       欄＝c4t（線の終わりの時刻＝C4_T）・c4mk（点）・c4gs（下り道＝3度の線・p54）・c4hl（lever＝ゴー・レバー〜頂点／flat＝約15秒の水平飛行）・
       c4go（ゴー・レバーの点）・c4dist（滑走路の末端からの物差し）・c4arrow（push 押す／back 戻ろうとした〈報告書の見方〉／dev 下り道からのずれ）・
       c4ring（on／ap＝自動操縦の水色）・switch。札の高さは本文の気圧高度（線は対地高度＝差は ±40m まで＝門番 ㉞）
  C5 … 相反の図＝C2 の尾翼（形と回し方をそのまま・縮めて上へ＝C5_T）＋押す手（橙）と自動操縦（水色）の矢印＋約30秒の時刻の帯（20:14:18〜49）。
       角度＝付図5（p110 拡大航跡図の THS・ELEVATOR の欄）。欄＝c5kind（rec／model）・c5ths・c5elev・c5ap・c5hand・c5band・c5snd（操作の音 0〜3＝p53）・
       c5cur（帯の時刻の線）・c5warn（警報の装置が無い＝×）・c5if（改修されていれば＝-5.3度の点線・想定の札と一緒に＝ca11）・c5lim・switch
  C6 … 夜の操縦室＝C3 の部屋＋①トリムの表示と②トリム・ホイール（p84＝センタペデスタルの上と両側・位置は模式）・視線（目の印）・
       ③警報音の印に ×（p84・p95）。人は描かない（手も無い）。欄＝c6ap・c6ring・c6eye・c6night（ペデスタルの下を暗く）・c6warn・switch
  C7 … 機体を横から（機首が右＝C4 の進む向き・形は模式）。機首の角度・水平安定板・昇降舵＝付図5 と本文（p49・p60）の値。
       欄＝c7kind・c7pitch・c7aoa（迎え角＝向かい風の矢印と弧・c7wind）・c7ths・c7elev・c7ap・c7push（fo＝副操縦士／cap＝機長＝20:15:03 から）・
       c7ring・c7thr（auto＝アルファ・フロア＝水色・p46／man＝手でいっぱい＝橙・p47）・c7rot（機首を上へ回す力）・c7warn（失速の警報）・switch。
       🔴 頂点（20:15:31）で止める＝機首が下がる絵・急降下は描かない
■ 守りの線（映像方針 17本目 §5-4・§5-8＝門番 check_illu ㉛〜㊲ が記録の値を門番の側に持つ＝ここの定数を読まない）
  ・乗員は影の手だけ（C3）・乗客は描かない・ぶつかる瞬間・炎・壊れた機体は描かない・CVR の言葉を絵の文字にしない
  ・時計の札は台本 §1-6 の1つに決まる時刻だけ（20:14:49＝付図29 の枠の 14'48" と割れる＝本文の 14分49秒・交替は 20:15:03）
  ・機長の手（左の席）は 20:15:03 の交替から（報告書 p73＝それまで手足を正常位置に保っていたかは明らかにできなかった）
  ・付図14・15・22 と写真51 の右上の線画はなぞらない（位置と数だけ）＝C2 の尾翼と C3 の操縦室は模式
"""
from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path

import fontmetrics as fm
import illu as IL
import titan_fig as F

W, H = IL.W, IL.H
KEY_DELAY = IL.KEY_DELAY
_part = IL._part

# ── 絵の色（全章で固定・章の色の置き換えが拾う値＝jiko_style の BG・BG2・GRID・LINE・LINE_DIM・TICK・INK_W を使わない）──
#   役の色＝映像方針 17本目 §8-4（人の操縦〈押す〉＝橙 jiko_style.COMPANY・自動の仕組み＝水色 jiko_style.SHIP と同じ値）
C17 = dict(
    # C1 画面
    room0="#121a21", room1="#1c262e", bez="#2b3238", bez_ln="#59646d", scr="#05090d",
    fma_ln="#c9d3d9", fw="#f3f6f8", fg="#58e27f", fb="#5aa9ff",
    sky="#3a74ad", gnd="#7a5433", hzn="#f3f6f8", sym="#11161b", sym_ln="#e9edf0",
    tape="#1b232a", tick="#a3afb7", ring="#f2c14e", ring_ol="#141a1f",
    eye="#e9edf0", btn="#3b444b", btn_ln="#aeb8bf", man="#f78b3e", ap="#7efcfa", red="#e0503c",
    bar="#e3e9ed", bar_txt="#11161b", axis="#aeb8bf", cur="#f2c14e",
    # C2 尾翼
    sky0="#132230", sky1="#1e3446", body="#a9b3ba", body_ln="#2a333a", fin="#97a2aa",
    ths="#d6dde2", elev="#c4cdd3", surf_ln="#20282e", ghost="#e9edf0",
    # C3 操縦室
    win0="#06090d", win1="#101a24", glare="#1f252a", panel="#2b3237", ped="#46505a", ped_ln="#6e7983",
    yoke="#7c868e", yoke_ln="#262d33", col="#4a545c", lever="#99a3ab", knob="#c2cad0", gol="#59626a", atb="#e6ebee",
    hand="#0a0e12", hand_ln="#5c6872", lamp_on="#9fe07e", lamp_off="#2f363c", lamp_txt="#0d1115", lamp_txt_off="#6b757d",
    # 🆕 ⑤b-4：C4 断面・C5 相反・C6 夜の操縦室・C7 機体
    gnd4="#1a1d1b", gnd4_ln="#59646d", tick4="#7d8a93", rwy="#8f989e", rwy_ln="#e9edf0", gs="#e9edf0", path4="#f3f6f8",
    band5="#1b232a", plane="#c9d1d7", plane_ln="#20282e", eng7="#9aa4ac", wind="#e9edf0", horizon="#59646d",
    trimw="#3d464d", trimw_ln="#a9b3ba", spk="#d6dde2", dark6="#020406",
)


def _d(pts, close=True):
    return "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")


def _path(pts, fill, stroke=None, sw=0.0, op=None, close=True, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<path d="{_d(pts, close)}" fill="{fill}"{st}{o}{extra}/>'


def _text(x, y, t, size=26, col=None, anchor="middle", ol=True):
    o = (' stroke="#10161b" stroke-width="5" stroke-linejoin="round" paint-order="stroke fill"' if ol else "")
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="Noto" font-size="{size:.0f}" fill="{col or C17["fw"]}" '
            f'text-anchor="{anchor}"{o}>{F.esc(t)}</text>')


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


def _switch_part(text):
    return dict(_part("switch", IL.va_switch_svg(text), "", keys=IL._switch_keys()), signal=True)


def _ring_rect(x0, y0, x1, y1, col=None, w=6):
    c = col or C17["ring"]
    return (f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" rx="12" fill="none" '
            f'stroke="{C17["ring_ol"]}" stroke-width="{w + 5}" opacity="0.6"/>'
            f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" rx="12" fill="none" '
            f'stroke="{c}" stroke-width="{w}"/>')


def _ring_circle(c, r, col=None, w=6):
    k = col or C17["ring"]
    return (f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" fill="none" stroke="{C17["ring_ol"]}" stroke-width="{w + 5}" '
            f'opacity="0.6"/><circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{r:.1f}" fill="none" stroke="{k}" stroke-width="{w}"/>')


def _arrow(p, q, col, w=9, head=26):
    """まっすぐな矢印（p→q）。縁取りつき"""
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    b = (q[0] - head * 0.9 * math.cos(ang), q[1] - head * 0.9 * math.sin(ang))
    l = (q[0] - head * math.cos(ang - 0.45), q[1] - head * math.sin(ang - 0.45))
    r = (q[0] - head * math.cos(ang + 0.45), q[1] - head * math.sin(ang + 0.45))
    line = f'M {p[0]:.1f} {p[1]:.1f} L {b[0]:.1f} {b[1]:.1f}'
    return (f'<path d="{line}" stroke="{C17["ring_ol"]}" stroke-width="{w + 6}" stroke-linecap="round" opacity="0.7"/>'
            f'<path d="{line}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            + _path([q, l, r], col, C17["ring_ol"], 3))


# ══════════════════════════════════════════════════════════
#  C1 操縦士の前の画面の上の端（FMA）＝付図29 の8つの枠
# ══════════════════════════════════════════════════════════
C1_T0 = 20 * 3600 + 14 * 60          # 20:14:00＝付図29 の 14'00"（世界共通の時刻 11:14:00 ＋9時間）
# 付図29 の枠（p135）。cells＝(欄, 段, 字, 色)。欄＝5つ割り "0"〜"4"／3つ割り "t"（推力）・"m"（飛び方）・"r"（指示と自動操縦）。
#   段 0／1＝上の行／下の行（付図29 の字の高さ）。色 w＝注記なし（白）・g＝注記 (green)・b＝注記 (blue)。s＝20:14:00 からの秒
C1_FRAMES = {
    "1400": dict(s=0, split=5, cells=(("0", 0, "SPD", "w"), ("1", 0, "GS", "g"), ("2", 0, "LOC", "g"), ("3", 0, "CAT1", "w"),
                                      ("4", 0, "FD1", "w"))),
    "1406": dict(s=6, split=3, cells=(("t", 0, "THR", "w"), ("m", 0, "GO AROUND", "w"), ("m", 1, "ALT", "b"), ("r", 0, "FD1", "w"))),
    "1412": dict(s=12, split=3, cells=(("t", 1, "MAN THR", "w"), ("m", 0, "GO AROUND", "w"), ("m", 1, "ALT", "b"),
                                       ("r", 0, "FD1", "w"))),
    "1418": dict(s=18, split=3, cells=(("t", 1, "MAN THR", "w"), ("m", 0, "GO AROUND", "w"), ("m", 1, "ALT", "b"),
                                       ("r", 0, "FD1", "w"), ("r", 1, "DUAL", "w"))),
    "1448": dict(s=48, split=3, cells=(("t", 1, "MAN THR", "w"), ("m", 0, "GO AROUND", "w"), ("m", 1, "ALT", "b"),
                                       ("r", 0, "FD1", "w"))),
    "1502": dict(s=62, split=3, cells=(("t", 0, "THR L", "g"), ("m", 0, "GO AROUND", "w"), ("m", 1, "ALT", "b"), ("r", 0, "FD1", "w"))),
    "1511": dict(s=71, split=3, cells=(("t", 1, "MAN THR", "w"), ("m", 0, "GO AROUND", "w"), ("m", 1, "ALT", "b"),
                                       ("r", 0, "FD1", "w"))),
    "1513": dict(s=73, split=0, cells=()),
}
C1_U5 = (0.0, 0.199, 0.399, 0.600, 0.796, 1.0)      # 付図29 の 14'00" の欄の区切り（内側の幅の割合＝頁の画素から）
C1_U3 = (0.0, 0.227, 0.799, 1.0)                     # 14'06" から（推力・飛び方・指示と自動操縦）
C1_ROW = (0.41, 0.64)                                # 字の段の下の線（枠の高さの割合）
C1_FS = 0.24                                         # 字の大きさ（枠の高さの割合）
C1_MLEFT = 0.33                                      # 真ん中の欄の字は左寄せ（付図29 の GO AROUND・ALT）
C1_COL = dict(w="fw", g="fg", b="fb")
# 見え方ごとの枠（x0・w＝内側の左と幅・y0＝外の上の線・h＝外の線の長さ）
# 🔴 ⑤b-3 の試し焼き 39366522160：time の枠の上の線（y150）が右上の章の札の字を横切った＝枠を下げた（y192）／
#    all の画面の縁（y132〜846）が上は章の札・下は出典の行に触れた＝画面ぜんたいを小さく（y150〜822）
C1_GEO = dict(all=dict(x0=548.0, y0=180.0, w=824.0, h=160.0),
              band=dict(x0=190.0, y0=200.0, w=1540.0, h=400.0),
              time=dict(x0=360.0, y0=192.0, w=1200.0, h=268.0))
# 画面ぜんたい（all）の部品の置き場（形は模式）
C1_ALL = dict(bez=(500.0, 150.0, 920.0, 672.0), scr=(518.0, 166.0, 884.0, 640.0), att=(796.0, 372.0, 328.0, 328.0),
              spd=(594.0, 372.0, 116.0, 328.0), hdg=(812.0, 734.0, 296.0, 46.0), gs=(1166.0, 392.0, 30.0, 288.0))
C1_HZN = dict(level=14.0, high=88.0, up=136.0)   # 姿勢の水平線の下がり（画素）＝ピッチ約4°（p54）／約18°（p83）／25度超（付図29 の 15'13"）＝模式
# 時刻の帯（time）
C1_TB = dict(x0=360.0, x1=1560.0, t1=75.0, y_mid=568.0, y_r=652.0, bh=50.0, y_axis=732.0)
C1_LAB = dict(all="操縦士の前の画面（正面から）", band="画面の上の端（拡大）", time="画面の上の端と時刻")
C1_SWITCH = "操縦士の前の画面では"
C1_REC = dict(
    f29="付図29 p1（FMA表示の推定＝14'00\"〜15'13\" の8つの枠）",
    screen="報告書 p52（機長の指示はFMAの表示を見て言った）",
    pfd="付図29 p1（注＝PITCH 角が25°を越えると Attitude・Speed・Heading 以外の PFD の表示は消える）",
    att_level="報告書 p54（ピッチ角約4°で降下を継続）",
    att_high="報告書 p83（ピッチ角は約9.5度増加し、約18°に達した）",
    att_up="付図29 p1（15'13\"：PITCH 角が25.84°）",
    gs="報告書 p5（正規の降下経路の上方1.2ドットの位置付近）",
    tband="付図29 p1（枠の時刻）・報告書 p5（APは約30秒間使用）・p46（14分49秒 両APを解除）",
    eye="報告書 p45（FMAの表示がGOAROUNDのまま変わっていないのを見て）・p52（FMAの表示を見て言った）",
    land="報告書 p54（直接LANDモードのボタンを押すことによって解除することはできない）",
    cur="報告書 p45（14分30秒）・p46（14分45秒）・p52（14分12秒）",
)


def c1_cells(view, k):
    """枠 k の字の置き場＝[(字, 色, x, 基線 y, 寄せ, 字の大きさ)]"""
    G = C1_GEO[view]
    x0, y0, w, h = G["x0"], G["y0"], G["w"], G["h"]
    fs = C1_FS * h
    fr = C1_FRAMES[k]
    out = []

    def fit(t, colw):
        # ⑤b-3 の下見：band で「MAN THR」（96px）が推力の欄（幅 350px）から枠の外へはみ出した＝欄の幅の 88% に収める（付図29 も欄に収まる）
        return min(fs, 0.88 * colw / (fm.width(t, 1.0) + 0.04 * len(t)))
    for col, row, t, c in fr["cells"]:
        y = y0 + C1_ROW[row] * h
        if fr["split"] == 5:
            i = int(col)
            out.append((t, c, x0 + w * (C1_U5[i] + C1_U5[i + 1]) / 2, y, "middle", fit(t, w * (C1_U5[i + 1] - C1_U5[i]))))
        elif col == "t":
            out.append((t, c, x0 + w * (C1_U3[0] + C1_U3[1]) / 2, y, "middle", fit(t, w * (C1_U3[1] - C1_U3[0]))))
        elif col == "m":
            out.append((t, c, x0 + w * C1_MLEFT, y, "start", fit(t, w * (C1_U3[2] - C1_MLEFT))))
        else:
            out.append((t, c, x0 + w * (C1_U3[2] + C1_U3[3]) / 2, y, "middle", fit(t, w * (C1_U3[3] - C1_U3[2]))))
    return out


def c1_box(cell, pad=0.22):
    """字の外の箱（輪・札の指し先）。🔴 ⑤b-3 の試し焼き 39366522160：縦の余白が字の大きさに比例して大きく、GO AROUND の輪の下の辺が
    すぐ下の段の「ALT」の頭に・DUAL の輪の上の辺が「FD1」にかかった＝付図29 の字は大文字だけ（下へ出る字が無い）＝縦は字の高さ＋0.08 だけ。
    横は字の間隔（letter-spacing＝0.04×大きさ×字数）も足す"""
    t, _c, x, y, anchor, fs = cell
    tw = fm.width(t, fs) + 0.04 * fs * len(t)
    xa = x - tw / 2 if anchor == "middle" else x
    p = pad * fs
    return (xa - p, y - 0.86 * fs, xa + tw + p, y + 0.12 * fs)


def c1_lines_svg(view, split):
    G = C1_GEO[view]
    x0, y0, w, h = G["x0"], G["y0"], G["w"], G["h"]
    om = 0.026 * w
    ln, sw = C17["fma_ln"], max(2.0, h * 0.012)
    g = [f'<path d="M {x0 - om:.1f} {y0 + h:.1f} L {x0 - om:.1f} {y0:.1f} L {x0 + w + om:.1f} {y0:.1f} L {x0 + w + om:.1f} {y0 + h:.1f}" '
         f'fill="none" stroke="{ln}" stroke-width="{sw:.1f}"/>',
         f'<path d="M {x0:.1f} {y0 + h:.1f} L {x0:.1f} {y0 + 0.34 * h:.1f} L {x0 + 0.052 * w:.1f} {y0 + 0.11 * h:.1f} '
         f'L {x0 + w - 0.065 * w:.1f} {y0 + 0.11 * h:.1f} L {x0 + w:.1f} {y0 + 0.34 * h:.1f} L {x0 + w:.1f} {y0 + h:.1f}" '
         f'fill="none" stroke="{ln}" stroke-width="{sw:.1f}"/>']
    us = C1_U5[1:-1] if split == 5 else C1_U3[1:-1] if split == 3 else ()
    for u in us:
        x = x0 + u * w
        g.append(f'<path d="M {x:.1f} {y0 + 0.11 * h:.1f} L {x:.1f} {y0 + 0.77 * h:.1f}" stroke="{ln}" stroke-width="{sw * 0.8:.1f}"/>')
    return "".join(g)


def c1_frame_svg(k, view):
    fr = C1_FRAMES[k]
    g = [c1_lines_svg(view, fr["split"])]
    for t, c, x, y, anchor, fs in c1_cells(view, k):
        g.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Noto" font-size="{fs:.0f}" fill="{C17[C1_COL[c]]}" '
                 f'text-anchor="{anchor}" letter-spacing="{fs * 0.04:.1f}">{F.esc(t)}</text>')
    return "".join(g)


def c1_bg_svg(view):
    if view == "all":
        g = [f'<defs><linearGradient id="c1room" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C17["room0"]}"/>'
             f'<stop offset="1" stop-color="{C17["room1"]}"/></linearGradient></defs>',
             f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#c1room)"/>']
        bx, by, bw, bh = C1_ALL["bez"]
        sx, sy, sw, sh = C1_ALL["scr"]
        g.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="34" fill="{C17["bez"]}" stroke="{C17["bez_ln"]}" stroke-width="4"/>')
        g.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="18" fill="{C17["scr"]}"/>')
        return "".join(g)
    return (f'<rect x="0" y="0" width="{W}" height="{H}" fill="{C17["scr"]}"/>'
            f'<rect x="0" y="0" width="{W}" height="{H}" fill="none" stroke="{C17["bez"]}" stroke-width="56"/>')


def c1_att_svg(kind):
    x, y, w, h = C1_ALL["att"]
    hy = y + h / 2 + C1_HZN[kind]
    cx = x + w / 2
    cid = f"c1clip_{kind}"
    g = [f'<defs><clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="40"/></clipPath></defs>',
         f'<g clip-path="url(#{cid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{C17["sky"]}"/>'
         f'<rect x="{x}" y="{hy:.1f}" width="{w}" height="{y + h - hy + 2:.1f}" fill="{C17["gnd"]}"/>'
         f'<path d="M {x} {hy:.1f} L {x + w} {hy:.1f}" stroke="{C17["hzn"]}" stroke-width="5"/>']
    for k in (-2, -1, 1, 2):          # 目盛りの線（数は書かない＝模式）
        yy = hy - k * 46
        ww = 70 if k % 2 == 0 else 40
        g.append(f'<path d="M {cx - ww:.1f} {yy:.1f} L {cx + ww:.1f} {yy:.1f}" stroke="{C17["hzn"]}" stroke-width="3" opacity="0.85"/>')
    g.append("</g>")
    cy = y + h / 2
    # 機の印（固定）
    for s in (-1, 1):
        g.append(_path([(cx + s * 150, cy - 6), (cx + s * 62, cy - 6), (cx + s * 62, cy + 22), (cx + s * 48, cy + 22),
                        (cx + s * 48, cy + 8), (cx + s * 150, cy + 8)], C17["sym"], C17["sym_ln"], 3))
    g.append(f'<rect x="{cx - 8:.1f}" y="{cy - 8:.1f}" width="16" height="16" fill="{C17["sym"]}" stroke="{C17["sym_ln"]}" stroke-width="3"/>')
    return "".join(g)


def c1_pfd_svg():
    """速さの帯（左）・方位の帯（下）＝目盛りだけ（数は書かない＝模式）"""
    g = []
    x, y, w, h = C1_ALL["spd"]
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{C17["tape"]}" stroke="{C17["bez_ln"]}" stroke-width="2"/>')
    for k in range(1, 12):
        yy = y + k * h / 12
        ln = 34 if k % 2 == 0 else 18
        g.append(f'<path d="M {x + w - ln:.1f} {yy:.1f} L {x + w - 4:.1f} {yy:.1f}" stroke="{C17["tick"]}" stroke-width="3"/>')
    g.append(_path([(x + w - 2, y + h / 2), (x + w + 18, y + h / 2 - 12), (x + w + 18, y + h / 2 + 12)], C17["fw"]))
    x, y, w, h = C1_ALL["hdg"]
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{C17["tape"]}" stroke="{C17["bez_ln"]}" stroke-width="2"/>')
    for k in range(1, 14):
        xx = x + k * w / 14
        ln = 22 if k % 2 == 0 else 12
        g.append(f'<path d="M {xx:.1f} {y + 4:.1f} L {xx:.1f} {y + 4 + ln:.1f}" stroke="{C17["tick"]}" stroke-width="3"/>')
    g.append(_path([(x + w / 2, y - 2), (x + w / 2 - 12, y - 20), (x + w / 2 + 12, y - 20)], C17["fw"]))
    return "".join(g)


def c1_gs_svg():
    """下り道のずれの目盛り（点＝ドット・p5 の「1.2ドット」）。指す印は描かない（位置は記録に無い）"""
    x, y, w, h = C1_ALL["gs"]
    cx, cy = x + w / 2, y + h / 2
    g = [f'<path d="M {cx - 16:.1f} {cy:.1f} L {cx + 16:.1f} {cy:.1f}" stroke="{C17["fw"]}" stroke-width="4"/>']
    for k in (-2, -1, 1, 2):
        g.append(f'<circle cx="{cx:.1f}" cy="{cy + k * 62:.1f}" r="9" fill="none" stroke="{C17["fw"]}" stroke-width="3.5"/>')
    return "".join(g)


def c1_tx(s):
    T = C1_TB
    return T["x0"] + float(s) / T["t1"] * (T["x1"] - T["x0"])


def c1_hms(s):
    t = C1_T0 + int(round(float(s)))
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}"


def c1_tband_svg():
    """時刻の帯：飛び方の欄（GS・LOC → GO AROUND → 消える）と右の欄（DUAL＝2つの自動操縦）。数は時刻の目盛りだけ"""
    T = C1_TB
    g = []
    bh = T["bh"]

    def bar(s0, s1, y, fill, txt, tcol, op=0.92, tx=None):
        x0, x1 = c1_tx(s0), c1_tx(s1)
        out = [f'<rect x="{x0:.1f}" y="{y - bh / 2:.1f}" width="{x1 - x0:.1f}" height="{bh:.1f}" rx="8" fill="{fill}" opacity="{op}"/>']
        # 🆕 ⑤c'：幅で縮む帯（GS LOC＝96px）は字と隣の帯の縁が 5.1px＝余白を 12→16px（6px 以上・geom_gap）
        fs = min(34.0, (x1 - x0 - 16) / max(1.0, fm.width(txt, 1.0)))
        out.append(f'<text x="{(x0 + x1) / 2 if tx is None else tx:.1f}" y="{y + fs * 0.36:.1f}" font-family="Noto" font-size="{fs:.0f}" fill="{tcol}" '
                   f'text-anchor="middle">{F.esc(txt)}</text>')
        return "".join(out)
    g.append(bar(0, 6, T["y_mid"], C17["fg"], "GS LOC", C17["bar_txt"]))
    # 🆕 ⑤c'（2026-10-21・c520）：帯の真ん中（x 992）だと 20:14:45 の時刻の線（x 1080）が字の N と D の間を貫いた（geom_gap 0px）
    #    ＝字を 14分30秒（c514）と 14分45秒（c520）の線のちょうど間（37.5秒）へ＝どちらの線とも約13px あく
    g.append(bar(6, 73, T["y_mid"], C17["bar"], "GO AROUND", C17["bar_txt"], tx=c1_tx(37.5)))
    g.append(bar(18, 49, T["y_r"], C17["bar"], "DUAL", C17["bar_txt"]))
    g.append(_text(T["x0"] - 18, T["y_mid"] + 10, "飛び方の欄", 28, C17["fw"], "end"))
    g.append(_text(T["x0"] - 18, T["y_r"] + 10, "右の欄", 28, C17["fw"], "end"))
    ya = T["y_axis"]
    g.append(f'<path d="M {T["x0"]:.1f} {ya:.1f} L {T["x1"]:.1f} {ya:.1f}" stroke="{C17["axis"]}" stroke-width="3"/>')
    for s in range(0, 76, 10):
        x = c1_tx(s)
        g.append(f'<path d="M {x:.1f} {ya:.1f} L {x:.1f} {ya + (14 if s % 30 == 0 else 8):.1f}" stroke="{C17["axis"]}" stroke-width="3"/>')
    # ⑤b-3 の下見：20:14:30 の目盛りの字が c514 の時刻の線の字（20:14:30）と縦に2つ並んだ＝目盛りの字は分の頭だけ
    for s in (0, 60):
        g.append(_text(c1_tx(s), ya + 44, c1_hms(s), 26, C17["axis"], "middle"))
    return "".join(g)


def c1_cursor_svg(hms):
    s = _sec_of(hms) - C1_T0
    x = c1_tx(s)
    T = C1_TB
    return (f'<path d="M {x:.1f} {T["y_mid"] - T["bh"] / 2 - 26:.1f} L {x:.1f} {T["y_axis"] + 10:.1f}" stroke="{C17["ring_ol"]}" '
            f'stroke-width="10" opacity="0.6"/><path d="M {x:.1f} {T["y_mid"] - T["bh"] / 2 - 26:.1f} L {x:.1f} {T["y_axis"] + 10:.1f}" '
            f'stroke="{C17["cur"]}" stroke-width="5"/>'
            + _text(x, T["y_axis"] + 84, hms, 34, C17["cur"], "middle"))


def _sec_of(hms):
    h, m, s = (int(v) for v in str(hms).split(":"))
    return h * 3600 + m * 60 + s


C1_EYE = dict(time=(205.0, 250.0), band=(180.0, 690.0), all=(390.0, 250.0))   # ⑤b-3 の下見：time の点線が MAN THR の字をかすめた＝上へ（枠を下げた分も）


def c1_eye_svg(view, frame):
    """目の印（見た向き＝人は描かない）と、GO AROUND の字への点線の矢印"""
    ex, ey = C1_EYE[view]
    tgt = next((c for c in c1_cells(view, frame) if c[0] == "GO AROUND"), None)
    if tgt is None:
        raise ValueError(f"illu C1：目の印の先（GO AROUND）が枠 {frame} に無い")
    g = [f'<path d="M {ex - 58:.1f} {ey:.1f} Q {ex:.1f} {ey - 46:.1f} {ex + 58:.1f} {ey:.1f} Q {ex:.1f} {ey + 46:.1f} {ex - 58:.1f} {ey:.1f} Z" '
         f'fill="{C17["eye"]}" stroke="{C17["ring_ol"]}" stroke-width="4"/>',
         f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="19" fill="{C17["sym"]}"/><circle cx="{ex + 6:.1f}" cy="{ey - 6:.1f}" r="5" fill="{C17["eye"]}"/>']
    if tgt:
        b = c1_box(tgt)
        q = (b[0] - 6, (b[1] + b[3]) / 2)
        p = (ex + 66, ey)
        g.append(f'<path d="M {p[0]:.1f} {p[1]:.1f} L {q[0] - 26:.1f} {q[1]:.1f}" stroke="{C17["eye"]}" stroke-width="5" '
                 f'stroke-dasharray="14 10"/>')
        g.append(_arrow((q[0] - 40, q[1]), q, C17["eye"], w=5, head=22))
    return "".join(g)


C1_LAND = dict(c=(960.0, 742.0), w=200.0, h=76.0)


def c1_land_svg(press=False):
    cx, cy = C1_LAND["c"]
    w, h = C1_LAND["w"], C1_LAND["h"]
    d = 6.0 if press else 0.0
    g = [f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2 + d:.1f}" width="{w:.1f}" height="{h:.1f}" rx="10" fill="{C17["btn"]}" '
         f'stroke="{C17["man"] if press else C17["btn_ln"]}" stroke-width="{6 if press else 3}"/>',
         f'<text x="{cx:.1f}" y="{cy + 15 + d:.1f}" font-family="Noto" font-size="42" fill="{C17["fw"]}" text-anchor="middle" '
         f'letter-spacing="2">LAND</text>']
    return "".join(g)


def c1_land_x_svg(view, frame):
    """LAND のボタン → GO AROUND の字へ：押しても消えない（×）"""
    tgt = next((c for c in c1_cells(view, frame) if c[0] == "ALT"), None)
    if tgt is None:
        raise ValueError(f"illu C1：LAND のボタンの矢印の先（ALT）が枠 {frame} に無い")
    b = c1_box(tgt)
    cx, cy = C1_LAND["c"]
    p, q = (cx, cy - C1_LAND["h"] / 2 - 8), (cx, b[3] + 14)
    mx, my = cx, (p[1] + q[1]) / 2
    r = 24
    return (f'<path d="M {p[0]:.1f} {p[1]:.1f} L {q[0]:.1f} {q[1] + 20:.1f}" stroke="{C17["fw"]}" stroke-width="5" stroke-dasharray="12 9"/>'
            + _path([q, (q[0] - 14, q[1] + 24), (q[0] + 14, q[1] + 24)], C17["fw"])
            + f'<path d="M {mx - r:.1f} {my - r:.1f} L {mx + r:.1f} {my + r:.1f} M {mx + r:.1f} {my - r:.1f} L {mx - r:.1f} {my + r:.1f}" '
              f'stroke="{C17["ring_ol"]}" stroke-width="17" stroke-linecap="round"/>'
            + f'<path d="M {mx - r:.1f} {my - r:.1f} L {mx + r:.1f} {my + r:.1f} M {mx + r:.1f} {my - r:.1f} L {mx - r:.1f} {my + r:.1f}" '
              f'stroke="{C17["red"]}" stroke-width="10" stroke-linecap="round"/>')


C1_RING_TXT = dict(ga=("GO AROUND",), dual=("DUAL",), fd=("FD1",), gsloc=("GS", "LOC"), thr=("THR", "MAN THR", "THR L", "SPD"))


def c1_ring_box(view, frame, tgt):
    cells = [c for c in c1_cells(view, frame) if c[0] in C1_RING_TXT[tgt]]
    if not cells:
        raise ValueError(f"illu C1：輪 {tgt} の字が枠 {frame} に無い")
    bs = [c1_box(c, 0.35) for c in cells]
    return (min(b[0] for b in bs), min(b[1] for b in bs), max(b[2] for b in bs), max(b[3] for b in bs))


def _scene_C1(start, states, steps):
    allst = [start] + states
    _head_only("C1", start, states, ("view", "switch"))
    v = start["view"]
    R = C1_REC
    parts = [_part("bg", c1_bg_svg(v), R["screen"])]
    if v == "all":
        parts.append(_part("pfd", c1_pfd_svg(), R["pfd"]))
        for a in ("level", "high", "up"):
            if any(st["c1att"] == a for st in allst):
                parts.append(dict(_part("att_" + a, c1_att_svg(a), R["att_" + a],
                                        keys=_akeys(start, states, steps, lambda st, a=a: st["c1att"] == a, 0.9)),
                                  geo=dict(kind="c1att", att=a)))
        parts.append(dict(_part("gsscale", c1_gs_svg(), R["gs"], keys=_akeys(start, states, steps, lambda st: st["c1f"] != "1513")),
                          geo=dict(kind="c1other")))
    elif any(st["c1att"] != "level" for st in allst):
        raise ValueError("illu C1：姿勢（c1att）は画面ぜんたい（view＝all）だけ")
    if v == "time":
        parts.append(dict(_part("tband", c1_tband_svg(), R["tband"]), geo=dict(kind="c1tband")))
    elif any(st["c1cur"] != "off" for st in allst):
        raise ValueError("illu C1：時刻の帯の線（c1cur）は view＝time だけ")
    for k in C1_FRAMES:
        if not any(st["c1f"] == k for st in allst) or (v == "all" and k == "1513"):
            continue
        parts.append(dict(_part("f" + k, c1_frame_svg(k, v), R["f29"], keys=_akeys(start, states, steps, lambda st, k=k: st["c1f"] == k)),
                          geo=dict(kind="fma", frame=k, view=v, cells=[list(c) for c in C1_FRAMES[k]["cells"]])))
    for tgt, k in sorted({(st["c1ring"], st["c1f"]) for st in allst if st["c1ring"] != "off"}):
        x0, y0, x1, y1 = c1_ring_box(v, k, tgt)
        parts.append(_part(f"ring_{tgt}_{k}", _ring_rect(x0, y0, x1, y1), R["f29"],
                           keys=_akeys(start, states, steps, lambda st, tgt=tgt, k=k: st["c1ring"] == tgt and st["c1f"] == k, 0.5)))
    for k in sorted({st["c1f"] for st in allst if st["c1eye"] == "on"}):
        parts.append(_part("eye_" + k, c1_eye_svg(v, k), R["eye"],
                           keys=_akeys(start, states, steps, lambda st, k=k: st["c1eye"] == "on" and st["c1f"] == k)))
    if any(st["c1land"] != "off" for st in allst):
        if v != "band":
            raise ValueError("illu C1：LAND のボタン（c1land）は view＝band だけ")
        parts.append(_part("land", c1_land_svg(False), R["land"], keys=_akeys(start, states, steps, lambda st: st["c1land"] == "on")))
        parts.append(_part("land_p", c1_land_svg(True), R["land"], keys=_akeys(start, states, steps, lambda st: st["c1land"] == "press", 0.3)))
        for k in sorted({st["c1f"] for st in allst if st["c1land"] == "press"}):
            parts.append(_part("land_x_" + k, c1_land_x_svg(v, k), R["land"],
                               keys=_akeys(start, states, steps, lambda st, k=k: st["c1land"] == "press" and st["c1f"] == k, 0.5, 0.5)))
    for hms in sorted({st["c1cur"] for st in allst if st["c1cur"] != "off"}):
        parts.append(dict(_part("cur_" + hms.replace(":", ""), c1_cursor_svg(hms), R["cur"],
                                keys=_akeys(start, states, steps, lambda st, h=hms: st["c1cur"] == h)), geo=dict(kind="c1cur", hms=hms)))
    if start["switch"] == "on":
        parts.append(_switch_part(C1_SWITCH))
    return parts


def _c1_anchors(st):
    v, k = st["view"], st["c1f"]
    G = C1_GEO[v]
    a = {}
    for c in c1_cells(v, k):
        b = c1_box(c)
        a[c[0].lower().replace(" ", "_")] = ((b[0] + b[2]) / 2, b[1] - 6)
        a[c[0].lower().replace(" ", "_") + "_low"] = ((b[0] + b[2]) / 2, b[3] + 6)
    if "go_around" in a:
        a["ga"], a["ga_low"] = a["go_around"], a["go_around_low"]
    for nm in ("thr", "man_thr", "thr_l"):
        if nm in a:
            a["thrcol"], a["thrcol_low"] = a[nm], a[nm + "_low"]
    x0, y0, w, h = G["x0"], G["y0"], G["w"], G["h"]
    a["col_thr"] = (x0 + w * (C1_U5[0] + C1_U5[1]) / 2, y0 + 0.11 * h)
    a["col_fly"] = (x0 + w * C1_U5[2], y0 + 0.11 * h)
    a["col_fd"] = (x0 + w * (C1_U5[4] + C1_U5[5]) / 2, y0 + 0.11 * h)
    a["strip"] = (x0 + w / 2, y0 + h * 0.5)
    if v == "all":
        x, y, w2, h2 = C1_ALL["att"]
        a["att"] = (x + w2 * 0.94, y + h2 * 0.24)
        x, y, w2, h2 = C1_ALL["spd"]
        a["spd_tape"] = (x + w2 * 0.3, y + h2 * 0.22)
        x, y, w2, h2 = C1_ALL["hdg"]
        a["hdg"] = (x + w2 * 0.75, y + h2)
    if v == "time":
        a["bar_ga"] = (c1_tx(40), C1_TB["y_mid"] - C1_TB["bh"] / 2)
        a["bar_dual"] = (c1_tx(33), C1_TB["y_r"] + C1_TB["bh"] / 2)
        if st["c1cur"] != "off":
            a["cursor"] = (c1_tx(_sec_of(st["c1cur"]) - C1_T0), C1_TB["y_mid"] - C1_TB["bh"] / 2 - 26)
    if v == "band":
        a["land"] = (C1_LAND["c"][0] + C1_LAND["w"] / 2, C1_LAND["c"][1])
    return a


def _c1_note(st0, states):
    note = ["報告書を加工して作成・画面の形は模式・字の色は付図29 の注記どおり（注記の無い字は白）"]
    if any(st["c1att"] != "level" for st in [st0] + list(states)):
        note.append("姿勢の傾きは模式")
    return "・".join(note)


# ══════════════════════════════════════════════════════════
#  C2 尾翼を横から見た図（機首が左）＝水平安定板と昇降舵
# ══════════════════════════════════════════════════════════
C2_LE, C2_TE, C2_Y = 920.0, 1700.0, 590.0       # 翼弦の前の端・後ろの端・翼弦の線（画素）
C2_HX = 1405.0                                   # ちょうつがい（水平安定板の後ろの端＝昇降舵の前の端・回る所＝模式）
C2_TH = 0.09                                     # 厚み（翼弦の割合・模式）
C2_GHOST = -5.3                                  # 点線の形＝進入の釣り合いの角度（報告書 p54「THS機首上げ-5.3°」）
C2_LIM = -12.3                                   # 機首上げの限界の印（報告書 p56「機首上げ一杯の-12.3°」）
C2_LAB = "尾翼を横から見た図（機首が左）"
C2_SWITCH = "尾翼を横から見ると"
C2_REC = dict(
    body="報告書 p55（THS（エレベータを含む。）の面積は、エレベータの面積のおよそ3倍）",
    ths="報告書 p78（APがTHSを、操縦士がエレベータをそれぞれ制御）",
    elev="報告書 p82（操縦輪…を一定以上の力で操作すると…マニュアル操作となる）",
    ap="報告書 p82（THSについては、その機構上オーバーライド中もAPがエンゲージされたままとなり、APに従った作動を続ける）",
    hand="報告書 p82（APアクチュエータはメカニカルに舵面の操作から切り離され、マニュアル操作となる）",
    ghost="報告書 p54（THS機首上げ-5.3°）",
    arc="報告書 p5（約18秒の間に、THSの角度は-5.3°から、機首上げ方向の限界に近い-12.3°まで）",
    lim="報告書 p56（THSは機首上げ一杯の-12.3°に達しており）",
    arrow_ap="報告書 p55（APはエレベータ及びTHSを機首上げ方向に作動させようとした）",
    arrow_hand="報告書 p44（操縦輪を押して機首下げ操作）",
)


def _naca(xc):
    return 5 * C2_TH * (0.2969 * math.sqrt(max(0.0, xc)) - 0.1260 * xc - 0.3516 * xc ** 2 + 0.2843 * xc ** 3 - 0.1015 * xc ** 4)


def _c2_half(x):
    c = C2_TE - C2_LE
    return _naca((x - C2_LE) / c) * c


def c2_rot(p, deg, about=None):
    ax, ay = about or (C2_HX, C2_Y)
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    x, y = p[0] - ax, p[1] - ay
    return (ax + c * x - s * y, ay + s * x + c * y)


def c2_ths_pts(deg=0.0):
    xs = [C2_LE + (C2_HX - 6 - C2_LE) * (1 - math.cos(math.pi * k / 40)) / 2 for k in range(41)]
    up = [(x, C2_Y - _c2_half(x)) for x in xs]
    lo = [(x, C2_Y + _c2_half(x)) for x in reversed(xs)]
    return [c2_rot(p, deg) for p in up + lo]          # 後ろの端はまっすぐ（昇降舵の丸い前の端が上に重なる＝ちょうつがい）


def c2_elev_pts(deg=0.0):
    """昇降舵（前の端はちょうつがいを真ん中にした丸＝回しても水平安定板からはなれない）"""
    hr = _c2_half(C2_HX)
    nose = [(C2_HX - hr * 0.9 * math.cos(math.radians(a)), C2_Y - hr * math.sin(math.radians(a))) for a in range(90, -91, -15)]
    xs = [C2_HX + (C2_TE - C2_HX) * k / 24 for k in range(1, 25)]
    lo = [(x, C2_Y + max(1.5, _c2_half(x))) for x in xs]
    up = [(x, C2_Y - max(1.5, _c2_half(x))) for x in reversed(xs)]
    return [c2_rot(p, deg) for p in nose + lo + up]


def c2_bg_svg():
    g = [f'<defs><linearGradient id="c2sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C17["sky0"]}"/>'
         f'<stop offset="1" stop-color="{C17["sky1"]}"/></linearGradient></defs>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#c2sky)"/>']
    return "".join(g)


def c2_body_svg():
    """胴体の後ろ（テールコーン）と垂直尾翼（形は模式）"""
    top = [(-20.0, 440.0), (860.0, 440.0)] + [(860.0 + 700 * u, 440.0 + 128 * u ** 1.6) for u in (0.2, 0.4, 0.6, 0.8, 1.0)]
    bot = [(1560.0, 604.0), (1300.0, 660.0), (1050.0, 730.0), (820.0, 770.0), (-20.0, 770.0)]
    # ⑤b-4 の試し焼き 39377897273：上の端 y 130 は右上の章の札（y 約66〜150・x 1380〜）の下に入った＝y 175 に下げた（形は模式）
    g = [_path([(1010.0, 444.0), (1290.0, 175.0), (1458.0, 175.0), (1548.0, 552.0)], C17["fin"], C17["body_ln"], 3.0),
         _path(top + bot, C17["body"], C17["body_ln"], 3.5)]
    return "".join(g)


def c2_surface_svg(pts, fill, op=None):
    return _path(pts, fill, C17["surf_ln"], 3.5, op=op)


def c2_ghost_svg():
    return _path(c2_ths_pts(C2_GHOST), "none", C17["ghost"], 3.0, extra=' stroke-dasharray="12 9" opacity="0.85"')


def c2_arc_svg(a0=C2_GHOST, a1=C2_LIM):
    r = C2_HX - C2_LE + 26
    pts = [c2_rot((C2_HX - r, C2_Y), a0 + (a1 - a0) * k / 20) for k in range(21)]
    q = pts[-1]
    ang = math.atan2(q[1] - pts[-3][1], q[0] - pts[-3][0])
    l = (q[0] - 24 * math.cos(ang - 0.5), q[1] - 24 * math.sin(ang - 0.5))
    rr = (q[0] - 24 * math.cos(ang + 0.5), q[1] - 24 * math.sin(ang + 0.5))
    return (f'<path d="{_d(pts, False)}" fill="none" stroke="{C17["ring_ol"]}" stroke-width="11" opacity="0.6"/>'
            f'<path d="{_d(pts, False)}" fill="none" stroke="{C17["ap"]}" stroke-width="6"/>' + _path([q, l, rr], C17["ap"]))


def c2_lim_svg():
    r0, r1 = C2_HX - C2_LE + 8, C2_HX - C2_LE + 62
    p, q = c2_rot((C2_HX - r0, C2_Y), C2_LIM), c2_rot((C2_HX - r1, C2_Y), C2_LIM)
    return (f'<path d="M {p[0]:.1f} {p[1]:.1f} L {q[0]:.1f} {q[1]:.1f}" stroke="{C17["ring_ol"]}" stroke-width="14" stroke-linecap="round"/>'
            f'<path d="M {p[0]:.1f} {p[1]:.1f} L {q[0]:.1f} {q[1]:.1f}" stroke="{C17["red"]}" stroke-width="8" stroke-linecap="round"/>')


def c2_arrows_svg(kind):
    if kind == "ap":          # 自動操縦が機首上げへ動かそうとする向き（昇降舵の後ろの端は上へ・水平安定板の前の端は下へ）
        return (_arrow((C2_TE + 60, C2_Y - 6), (C2_TE + 60, C2_Y - 112), C17["ap"])
                + _arrow((C2_LE - 58, C2_Y - 20), (C2_LE - 58, C2_Y + 96), C17["ap"]))
    return _arrow((C2_TE + 60, C2_Y + 8), (C2_TE + 60, C2_Y + 116), C17["man"])          # 押す＝昇降舵の後ろの端は下へ


def c2_hinge_svg():
    return f'<circle cx="{C2_HX:.1f}" cy="{C2_Y:.1f}" r="7" fill="{C17["surf_ln"]}" stroke="{C17["ghost"]}" stroke-width="2"/>'


def _scene_C2(start, states, steps):
    allst = [start] + states
    _head_only("C2", start, states, ("view", "c2kind", "c2ghost", "switch"))
    R = C2_REC
    piv = (C2_HX, C2_Y)
    rot_t = (lambda st: dict(rot=float(st["c2ths"])))                       # noqa: E731
    rot_e = (lambda st: dict(rot=float(st["c2ths"]) + float(st["c2elev"])))  # noqa: E731
    parts = [_part("bg", c2_bg_svg(), R["body"]), _part("body", c2_body_svg(), R["body"])]
    if start["c2ghost"] == "on":
        parts.append(dict(_part("ghost", c2_ghost_svg(), R["ghost"]), geo=dict(kind="c2ghost", deg=C2_GHOST)))
    if any(st["c2arc"] == "on" for st in allst):
        parts.append(dict(_part("arc", c2_arc_svg(), R["arc"], keys=_akeys(start, states, steps, lambda st: st["c2arc"] == "on", 1.6)),
                          geo=dict(kind="c2arc", a0=C2_GHOST, a1=C2_LIM)))
    if any(st["c2lim"] == "on" for st in allst):
        parts.append(dict(_part("lim", c2_lim_svg(), R["lim"], keys=_akeys(start, states, steps, lambda st: st["c2lim"] == "on")),
                          geo=dict(kind="c2lim", deg=C2_LIM)))
    parts.append(dict(_part("ths", c2_surface_svg(c2_ths_pts(), C17["ths"]), R["ths"], piv, IL._keys(start, states, steps, rot_t)),
                      geo=dict(kind="c2ths")))
    if any(st["c2ap"] == "on" for st in allst):
        parts.append(dict(_part("ths_ap", c2_surface_svg(c2_ths_pts(), C17["ap"], 0.92), R["ap"], piv,
                                IL._keys(start, states, steps, rot_t)),
                          akeys=_akeys(start, states, steps, lambda st: st["c2ap"] == "on"), geo=dict(kind="c2ap")))
    parts.append(dict(_part("elev", c2_surface_svg(c2_elev_pts(), C17["elev"]), R["elev"], piv, IL._keys(start, states, steps, rot_e)),
                      geo=dict(kind="c2elev")))
    if any(st["c2hand"] == "on" for st in allst):
        parts.append(dict(_part("elev_hand", c2_surface_svg(c2_elev_pts(), C17["man"], 0.95), R["hand"], piv,
                                IL._keys(start, states, steps, rot_e)),
                          akeys=_akeys(start, states, steps, lambda st: st["c2hand"] == "on"), geo=dict(kind="c2hand")))
    for nm, which, fn in (("ring_ths", ("both", "ths"), rot_t), ("ring_elev", ("both", "elev"), rot_e)):
        if any(st["c2hl"] in which for st in allst):
            pts = c2_ths_pts() if nm == "ring_ths" else c2_elev_pts()
            svg = (_path(pts, "none", C17["ring_ol"], 15.0, op=0.6) + _path(pts, "none", C17["ring"], 8.0))
            parts.append(dict(_part(nm, svg, R["ths" if nm == "ring_ths" else "elev"], piv, IL._keys(start, states, steps, fn)),
                              akeys=_akeys(start, states, steps, lambda st, w=which: st["c2hl"] in w)))
    for kind in ("ap", "hand"):
        if any(st["c2arrow"] == kind for st in allst):
            parts.append(_part("arrow_" + kind, c2_arrows_svg(kind), R["arrow_" + kind],
                               keys=_akeys(start, states, steps, lambda st, k=kind: st["c2arrow"] == k)))
    parts.append(_part("hinge", c2_hinge_svg(), R["ths"]))
    if start["switch"] == "on":
        parts.append(_switch_part(C2_SWITCH))
    return parts


def _c2_anchors(st):
    t, e = float(st["c2ths"]), float(st["c2elev"])
    xs = C2_LE + 0.30 * (C2_TE - C2_LE)
    xe = C2_HX + 0.55 * (C2_TE - C2_HX)
    return dict(ths=c2_rot((xs, C2_Y - _c2_half(xs)), t), ths_low=c2_rot((xs, C2_Y + _c2_half(xs)), t),
                le=c2_rot((C2_LE, C2_Y), t), elev=c2_rot((xe, C2_Y - _c2_half(xe)), t + e),
                elev_low=c2_rot((xe, C2_Y + _c2_half(xe)), t + e), te=c2_rot((C2_TE, C2_Y), t + e), hinge=(C2_HX, C2_Y),
                ghost=c2_rot((C2_LE, C2_Y), C2_GHOST), lim=c2_rot((C2_LE - 62, C2_Y), C2_LIM), fin=(1390.0, 260.0), body=(520.0, 600.0))


C2_REC_THS = (C2_GHOST, C2_LIM)                 # 🆕 ⑤c'：水平安定板の記録の点（p54・p44 の -5.3°／p56 の -12.3°）


def _c2_note(st0, states):
    if st0["c2kind"] == "model":
        return "報告書を加工して作成・形と角度の動きは模式（付図15 の位置と数だけ）"
    # 🆕 17本目 ⑤c'（2026-10-21・c509）：記録の点の間の水平安定板（c509 の −6.0度＝p45「-5.3°の位置からなお機首上げ方向へ動き始めている」）は
    #    記録の値でない＝「角度は記録の値」と言い切らない（門番 ㉜ が同じ断りを見る）
    mid = any(all(abs(float(st["c2ths"]) - v) > 0.05 for v in C2_REC_THS) for st in [st0] + list(states))
    return "報告書を加工して作成・形は模式（付図15 の位置と数だけ）・角度は記録の値" + ("（途中の角度は模式）" if mid else "")


# ══════════════════════════════════════════════════════════
#  C3 操縦室の中（後ろから前を向いて・夜）＝人は影の手だけ
# ══════════════════════════════════════════════════════════
# ⑤b-3 の下見：窓が上半分を占めて操縦輪・レバー・手が下に小さく寄った＝窓を縮め（y 0〜170）、操縦輪とレバーを大きく上へ
C3_LEV = ((905.0, 560.0), (1015.0, 560.0))     # スラスト・レバーのノブ（左・右）＝2本（報告書 p51「両スラスト・レバー」）
C3_KNOB = (100.0, 42.0)
C3_GO = (905.0, 597.0)                          # ゴー・レバー＝左のスラスト・レバーのノブの下（報告書 p51・写真51「左スラスト・レバー」）
C3_AT = (849.0, 560.0)                          # 自動推力を切るボタン＝ノブの端（写真51 の位置だけ）
C3_YOKE = dict(L=(390.0, 650.0), R=(1530.0, 650.0))
C3_HORN = 1.35                                  # 操縦輪の大きさ（模式）
C3_LAMPS = ((915.0, 202.0), (1005.0, 202.0))    # 自動操縦の灯（AP 1・AP 2＝報告書 p5「No.2そしてNo.1」）
C3_PIV_R = (1530.0, 1080.0)                     # 右の操縦輪を押す（前へ＝上へ小さく）の回る所
C3_PUSH = dict(dy=-30.0, sc=0.93)
C3_SLIDE = 470.0                                # 手が画面の下から入る・出る量（画素）
C3_LAB = "操縦室の中（後ろから前を向いて）"
C3_SWITCH = "操縦室の中では"
C3_REC = dict(
    room="報告書 p73（副操縦士が路線において操縦する場合は、右席で実施）",
    lever="報告書 p51（両スラスト・レバー・ゴー・レバーはスラスト・レバーのノブの下方に位置）",
    yoke="報告書 p44（副操縦士は…操縦輪を押して機首下げ操作）・p47（機長は…操縦輪を限界まで一杯に押し続けた）",
    lamps="報告書 p5（APがNo.2そしてNo.1とほぼ同時にエンゲージ）",
    lamps_off="報告書 p46（14分49秒 両APを解除）",
    hand_thr="報告書 p51（副操縦士は、ATSを使用しスラスト・レバーに手を添えていた）",
    hand_yoke="報告書 p55（副操縦士が操縦輪を押し続けていた）",
    hand_cap="報告書 p47（15分03秒、機長は副操縦士に操縦を交替する旨を告げ、操縦を交替し、操縦輪を限界まで一杯に押し続けた）・p73（我來と呼唱して操縦を交替）",
    push="報告書 p45（14分23秒「押して」＝操縦輪の押し下げ操作を指示）",
    at="報告書 p51（ATディスコネクト・プッシュ・ボタンとを間違えたためか）",
)


def c3_room_svg():
    g = [f'<defs><linearGradient id="c3win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C17["win0"]}"/>'
         f'<stop offset="1" stop-color="{C17["win1"]}"/></linearGradient></defs>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#c3win)"/>',
         # 窓の下の覆い（グレアシールド）と計器の板（模式）
         _path([(0, 166), (W, 166), (W, 232), (1500, 240), (960, 246), (420, 240), (0, 232)], C17["glare"], C17["ped_ln"], 2.0),
         _path([(0, 232), (420, 240), (960, 246), (1500, 240), (W, 232), (W, 470), (0, 470)], C17["panel"]),
         # 真ん中の台（ペデスタル）
         _path([(790, 470), (1130, 470), (1290, H + 4), (630, H + 4)], C17["ped"], C17["ped_ln"], 3.0),
         # FCU（モードを選ぶ板・模式）
         f'<rect x="740" y="178" width="440" height="48" rx="6" fill="{C17["panel"]}" stroke="{C17["ped_ln"]}" stroke-width="2"/>']
    return "".join(g)


def c3_lamps_svg(on):
    g = []
    for (x, y), t in zip(C3_LAMPS, ("AP 1", "AP 2")):
        g.append(f'<rect x="{x - 40:.1f}" y="{y - 17:.1f}" width="80" height="34" rx="5" '
                 f'fill="{C17["lamp_on"] if on else C17["lamp_off"]}" stroke="{C17["ped_ln"]}" stroke-width="2"/>')
        g.append(f'<text x="{x:.1f}" y="{y + 9:.1f}" font-family="Noto" font-size="24" '
                 f'fill="{C17["lamp_txt"] if on else C17["lamp_txt_off"]}" text-anchor="middle">{t}</text>')
    return "".join(g)


def c3_levers_svg():
    g = []
    for x, y in C3_LEV:
        g.append(f'<rect x="{x - 11:.1f}" y="{y:.1f}" width="22" height="180" fill="{C17["lever"]}" stroke="{C17["yoke_ln"]}" stroke-width="2"/>')
        g.append(f'<rect x="{x - 36:.1f}" y="{y + 176:.1f}" width="72" height="16" rx="4" fill="{C17["col"]}"/>')
    for x, y in C3_LEV:
        kw, kh = C3_KNOB
        g.append(f'<rect x="{x - kw / 2:.1f}" y="{y - kh / 2:.1f}" width="{kw:.1f}" height="{kh:.1f}" rx="{kh / 2:.1f}" '
                 f'fill="{C17["knob"]}" stroke="{C17["yoke_ln"]}" stroke-width="3"/>')
    gx, gy = C3_GO
    g.append(_path([(gx - 26, gy - 7), (gx + 22, gy - 7), (gx + 17, gy + 9), (gx - 21, gy + 9)], C17["gol"], C17["knob"], 2.0))
    ax, ay = C3_AT
    g.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="11" fill="{C17["atb"]}" stroke="{C17["yoke_ln"]}" stroke-width="3"/>')
    return "".join(g)


def c3_yoke_svg(side):
    cx, cy = C3_YOKE[side]
    k = C3_HORN
    g = [f'<rect x="{cx - 30:.1f}" y="{cy + 26:.1f}" width="60" height="{H - cy:.1f}" fill="{C17["col"]}" stroke="{C17["yoke_ln"]}" stroke-width="3"/>']
    horn = [(-150, -70), (-132, -86), (-112, -70), (-104, -2), (104, -2), (112, -70), (132, -86), (150, -70), (140, 26), (60, 40),
            (-60, 40), (-140, 26)]
    g.append(_path(IL._smooth([(cx + x * k, cy + y * k) for x, y in horn], closed=True, per=4), C17["yoke"], C17["yoke_ln"], 4.0))
    g.append(f'<circle cx="{cx:.1f}" cy="{cy + 22:.1f}" r="30" fill="{C17["col"]}" stroke="{C17["yoke_ln"]}" stroke-width="3"/>')
    return "".join(g)


def _ellipse(c, rx, ry, rot=0.0, n=24):
    r = math.radians(rot)
    return [(c[0] + rx * math.cos(t) * math.cos(r) - ry * math.sin(t) * math.sin(r),
             c[1] + rx * math.cos(t) * math.sin(r) + ry * math.sin(t) * math.cos(r))
            for t in (2 * math.pi * k / n for k in range(n))]


def _hand_shape(base, wrist, fist, r, kind="grip", side=1):
    """影の手（腕は画面の下の端から＝顔・体を描かない）。base＝画面の下の端の腕の真ん中・wrist＝手首・fist＝手の真ん中・r＝手の大きさ。
    kind＝grip（操縦輪の角を握る＝指の節4つと親指）／palm（ノブの上に添える＝前へ伸びた指4本と親指）。side＝親指の向き（1＝左・-1＝右）
    ⑤b-3 の下見：楕円1つと小さな丸の手は「黒い丸」に見えて手と分からなかった＝指の節・指・親指を形にした"""
    bx, by = base
    wx, wy = wrist
    ang = math.atan2(wy - by, wx - bx)
    nx, ny = -math.sin(ang), math.cos(ang)
    arm = [(bx + nx * 72, by + ny * 72), (wx + nx * 0.62 * r, wy + ny * 0.62 * r), (wx - nx * 0.62 * r, wy - ny * 0.62 * r),
           (bx - nx * 72, by - ny * 72)]
    fx, fy = fist
    out = [arm]
    if kind == "grip":
        out.append(_ellipse((fx, fy), r * 0.95, r * 0.82))
        for k in range(4):                                       # 指の節（上の縁に4つ）
            a = math.radians(-150 + k * 36)
            out.append(_ellipse((fx + r * 0.78 * math.cos(a), fy + r * 0.70 * math.sin(a)), r * 0.28, r * 0.26, n=16))
        out.append(_ellipse((fx - side * r * 0.86, fy + r * 0.05), r * 0.24, r * 0.52, rot=side * 24, n=16))   # 親指
    else:
        out.append(_ellipse((fx, fy), r * 1.02, r * 0.74))
        for k in range(4):                                       # 前へ伸びた指（上へ）
            x = fx + (k - 1.5) * r * 0.40
            out.append(_ellipse((x, fy - r * 0.86), r * 0.17, r * 0.46, n=16))
        out.append(_ellipse((fx - side * r * 0.98, fy + r * 0.12), r * 0.42, r * 0.20, rot=side * -28, n=16))  # 親指
    return out


C3_HANDS = dict(
    thr=dict(seat="R", shapes=[_hand_shape((1340.0, H + 40), (1112.0, 640.0), (1030.0, 576.0), 66.0, "palm")]),
    yoke=dict(seat="R", shapes=[_hand_shape((1770.0, H + 40), (1748.0, 690.0), (1722.0, 586.0), 56.0, "grip", -1)]),
    cap=dict(seat="L", shapes=[_hand_shape((140.0, H + 40), (174.0, 690.0), (198.0, 586.0), 56.0, "grip", 1),
                               _hand_shape((640.0, H + 40), (606.0, 690.0), (582.0, 586.0), 56.0, "grip", -1)]),
)


def c3_hand_svg(name):
    g = []
    for sh in C3_HANDS[name]["shapes"]:
        for poly in sh:
            g.append(_path(poly, C17["hand"], C17["hand_ln"], 2.5))
    return "".join(g)


def _scene_C3(start, states, steps):
    allst = [start] + states
    _head_only("C3", start, states, ("view", "switch"))
    R = C3_REC
    piv = C3_PIV_R

    def push(st):
        return dict(dy=C3_PUSH["dy"] if st["c3push"] == "on" else 0.0, sc=C3_PUSH["sc"] if st["c3push"] == "on" else 1.0)
    # 灯の消えた形と点いた形は入れ替える（同じ位置の字が重ならない＝check_layout の「同時に見えない絵の層」）
    parts = [_part("room", c3_room_svg(), R["room"]),
             dict(_part("lamps", c3_lamps_svg(False), R["lamps"],
                        keys=_akeys(start, states, steps, lambda st: st["c3ap"] != "on", 0.35)), obj=dict(autopilot=2))]
    if any(st["c3ap"] == "on" for st in allst):
        parts.append(_part("lamps_on", c3_lamps_svg(True), R["lamps"],
                           keys=_akeys(start, states, steps, lambda st: st["c3ap"] == "on", 0.35)))
    parts.append(_part("yoke_L", c3_yoke_svg("L"), R["yoke"]))
    parts.append(_part("yoke_R", c3_yoke_svg("R"), R["yoke"], piv, IL._keys(start, states, steps, push)))
    parts.append(dict(_part("levers", c3_levers_svg(), R["lever"]), obj=dict(thrust_lever=2),
                      geo=dict(kind="c3levers", knobs=[list(p) for p in C3_LEV], go=list(C3_GO), at=list(C3_AT))))
    for nm, fld, rec, mv in (("hand_thr", "c3thr", R["hand_thr"], None), ("hand_yoke", "c3yoke", R["hand_yoke"], push),
                             ("hand_cap", "c3cap", R["hand_cap"], None)):
        if not any(st[fld] == "on" for st in allst):
            continue

        def fn(st, fld=fld, mv=mv):
            on = st[fld] == "on"
            d = dict(dy=0.0 if on else C3_SLIDE, a=1.0 if on else 0.0)
            if mv:
                m = mv(st)
                d = dict(dy=d["dy"] + m["dy"], sc=m["sc"], a=d["a"])
            return d
        ks = IL._keys(start, states, steps, fn)
        polys = [list(map(list, poly)) for sh in C3_HANDS[nm[5:]]["shapes"] for poly in sh]
        parts.append(dict(_part(nm, c3_hand_svg(nm[5:]), rec, piv if mv else (0.0, 0.0), ks),
                          geo=dict(kind="hand", seat=C3_HANDS[nm[5:]]["seat"], polys=polys)))
    if any(st["c3push"] == "on" for st in allst):
        x, y = C3_YOKE["R"]
        parts.append(_part("push", _arrow((x, y - 120), (x, y - 236), C17["man"]), R["push"],
                           keys=_akeys(start, states, steps, lambda st: st["c3push"] == "on")))
    for tgt, svg in (("go", _ring_circle(C3_GO, 34)), ("at", _ring_circle(C3_AT, 26)),
                     ("lev", _ring_rect(C3_LEV[0][0] - 52, C3_LEV[0][1] - 34, C3_LEV[1][0] + 52, C3_LEV[1][1] + 34))):
        if any(st["c3ring"] == tgt for st in allst):
            parts.append(_part("ring_" + tgt, svg, R["at"] if tgt == "at" else R["lever"],
                               keys=_akeys(start, states, steps, lambda st, t=tgt: st["c3ring"] == t, 0.5)))
    if start["switch"] == "on":
        parts.append(_switch_part(C3_SWITCH))
    return parts


def _c3_anchors(st):
    lx = (C3_LEV[0][0] + C3_LEV[1][0]) / 2
    return dict(go=(C3_GO[0] - 10, C3_GO[1] + 10), at=(C3_AT[0] - 12, C3_AT[1]), lev=(lx, C3_LEV[0][1] - 26),
                lev_r=(C3_LEV[1][0] + 52, C3_LEV[1][1]), yoke_R=(C3_YOKE["R"][0] - 150, C3_YOKE["R"][1] - 70),
                yoke_L=(C3_YOKE["L"][0] + 120, C3_YOKE["L"][1] - 40),
                lamps=((C3_LAMPS[0][0] + C3_LAMPS[1][0]) / 2, C3_LAMPS[0][1] + 18),
                hand_thr=(1112.0, 640.0), push=(C3_YOKE["R"][0], C3_YOKE["R"][1] - 236), top=(960.0, 120.0))


def _c3_note(st0, states):
    return "報告書を加工して作成・操縦室の形と並びは模式（付図22・写真51 の位置と数だけ）・人は影の手だけ"


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-20）C4 進入の断面図（横から・滑走路は右）＝付図4 の線（`ref/ep17/c4_path.json`＝make_c4path.py）
# ══════════════════════════════════════════════════════════
C4_JSON = Path(__file__).resolve().parent.parent / "ref" / "ep17" / "c4_path.json"
# 見え方＝k0（左の端の km＝滑走路から）・k1（右の端の km＝負は滑走路の上）・x0／x1（画素）・mtop（ytop の高さ m）・yg（0m の画素）
#   高さは横より伸ばしてある（all 約8倍・near 約4倍）＝左上の見る向きの札に「高さを約N倍に」（門番 ㉞ が目盛りから倍率を数え直す）
#   🔴 地面（0m）は y 760＝出典の行（y 約866〜884・左下から右へ長く伸びる）と字幕に札・線を近づけない（C1 の all と同じ考え）
C4_VIEW = dict(all=dict(k0=17.6, k1=-0.6, x0=110.0, x1=1810.0, mtop=820.0, yg=760.0, ytop=190.0),
               near=dict(k0=6.6, k1=-0.6, x0=110.0, x1=1810.0, mtop=620.0, yg=760.0, ytop=180.0))
# 場面の時刻（c4t）に使ってよい時刻＝付図4 の矢印の時刻と頂点（json の times）・本文の時刻（内挿＝14:00・14:10 p44・14:25〈14:10＋約15秒 p5〉・
#   14:57 p46・15:02 p5）。🔴 時刻の札に出すかは門番の表（REC_C17_CLOCK）が決める＝ここは線の長さだけ
C4_T = ("20:11:35", "20:14:00", "20:14:05", "20:14:10", "20:14:18", "20:14:25", "20:14:37", "20:14:49", "20:14:57", "20:15:02",
        "20:15:03", "20:15:11", "20:15:25", "20:15:31")
C4_FLAT = ("20:14:10", "20:14:25")              # 約15秒の水平飛行（p44「14分10秒ごろから…水平飛行」・p5「約15秒間水平飛行」）
C4_LEVER = ("20:14:05", "20:15:31")             # ゴー・レバー（p5）から頂点（p6・p49）まで＝線はここで止める
C4_SWITCH = "進入の道を横から見ると"
C4_REC = dict(
    path="付図4 p1（航跡概略図＝横軸は距離・縦軸は補正計算した対地高度）",
    gs="報告書 p54（3°のILS進入経路に乗って）",
    rwy="報告書 p6（滑走路34末端中心から東北東約110m）・付図4 p1（RWY）",
    mk="付図4 p1（時刻の矢印）",
    lever="報告書 p5（11時14分05秒…ゴー・レバーを作動）・p6（11時15分31秒…最高点）",
    flat="報告書 p44（14分10秒ごろから気圧高度約1,040ftで水平飛行状態）・p5（約15秒間水平飛行）",
    dist5="報告書 p5（滑走路から約5.5kmの地点付近）",
    dist18="報告書 p5（11時15分02秒、気圧高度約510ft（滑走路から約1.8kmの地点付近））",
    push="報告書 p44（操縦輪を押して機首下げ操作を行っているが…降下することなく）",
    back="報告書 p90（APの補助を得て正規の降下経路に戻ろうとして行った可能性）",
    dev="報告書 p44（やや機首上げ傾向となりILS降下経路から上方に外れ）",
    ap="報告書 p5（APがNo.2そしてNo.1とほぼ同時にエンゲージ）",
)


@lru_cache(maxsize=1)
def c4_data():
    d = json.loads(C4_JSON.read_text(encoding="utf-8"))
    d["pts"] = sorted((float(k), float(m)) for k, m in d["pts"])[::-1]          # 遠い → 近い
    return d


def c4_sec(hms):
    return _sec_of(hms)


def c4_km(t):
    """時刻 → 滑走路からの km（付図4 の矢印の時刻のあいだは時刻で内挿）"""
    tt = sorted((c4_sec(k), float(v)) for k, v in c4_data()["times"].items())
    s = c4_sec(t)
    for (s0, k0), (s1, k1) in zip(tt, tt[1:]):
        if s0 <= s <= s1:
            return k0 + (k1 - k0) * (s - s0) / (s1 - s0)
    raise ValueError(f"illu C4：時刻 {t} は付図4 の時刻の範囲の外")


def c4_h(km):
    """km → 付図4 の対地高度（m）"""
    pts = c4_data()["pts"]
    for (ka, ma), (kb, mb) in zip(pts, pts[1:]):
        if kb <= km <= ka:
            return ma + (mb - ma) * (ka - km) / (ka - kb)
    raise ValueError(f"illu C4：{km:.3f}km は付図4 の線の外（頂点より滑走路の側は描かない）")


def c4_x(view, km):
    V = C4_VIEW[view]
    return V["x0"] + (V["k0"] - km) / (V["k0"] - V["k1"]) * (V["x1"] - V["x0"])


def c4_y(view, m):
    V = C4_VIEW[view]
    return V["yg"] - m * (V["yg"] - V["ytop"]) / V["mtop"]


def c4_xy(view, km, m=None):
    return (c4_x(view, km), c4_y(view, c4_h(km) if m is None else m))


def c4_ruler(view):
    """門番 ㉞ が画素を km・m に読み直す目盛り（描く側と同じ式）"""
    V = C4_VIEW[view]
    pxkm = (V["x1"] - V["x0"]) / (V["k0"] - V["k1"])
    pxm = (V["yg"] - V["ytop"]) / V["mtop"]
    return dict(x0=V["x0"], k0=V["k0"], pxkm=pxkm, yg=V["yg"], pxm=pxm)


def c4_exag(view):
    r = c4_ruler(view)
    return r["pxm"] / (r["pxkm"] / 1000.0)


def c4_label(view):
    return f"進入の道を横から見た図（高さを約{round(c4_exag(view))}倍に）"


def c4_seg(view, ka, kb):
    """km ka → kb（ka>kb）の線の点"""
    pts = [(ka, c4_h(ka))] + [(k, m) for k, m in c4_data()["pts"] if kb < k < ka] + [(kb, c4_h(kb))]
    V = C4_VIEW[view]
    return [(c4_x(view, k), c4_y(view, m)) for k, m in pts if k <= V["k0"] + 1e-9] or []


def c4_bg_svg(view):
    V = C4_VIEW[view]
    yg = V["yg"]
    x0r, x1r = c4_x(view, 0.0), W + 4
    g = [f'<defs><linearGradient id="c4sky_{view}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C17["sky0"]}"/>'
         f'<stop offset="1" stop-color="{C17["sky1"]}"/></linearGradient></defs>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#c4sky_{view})"/>',
         f'<rect x="-4" y="{yg:.1f}" width="{W + 8}" height="{H - yg + 4:.1f}" fill="{C17["gnd4"]}"/>',
         f'<path d="M -4 {yg:.1f} L {W + 4} {yg:.1f}" stroke="{C17["gnd4_ln"]}" stroke-width="3"/>']
    # 距離の目盛り（1km ごと・字は無い）＝地面の線の下
    step = 1.0
    k = math.floor(V["k0"])
    while k >= 0:
        x = c4_x(view, k)
        g.append(f'<path d="M {x:.1f} {yg + 4:.1f} L {x:.1f} {yg + (22 if k % 5 == 0 else 12):.1f}" stroke="{C17["tick4"]}" stroke-width="3"/>')
        k -= step
    # 滑走路（末端＝0km から右へ）
    g.append(f'<rect x="{x0r:.1f}" y="{yg - 7:.1f}" width="{x1r - x0r:.1f}" height="14" fill="{C17["rwy"]}"/>')
    g.append(f'<path d="M {x0r + 10:.1f} {yg:.1f} L {x1r:.1f} {yg:.1f}" stroke="{C17["rwy_ln"]}" stroke-width="3" stroke-dasharray="16 12"/>')
    # ⑤b-4 の門番 layout：全体（all）は末端が x 1754＝真ん中に置くと字の右が 1872（上限 1848）＝真ん中は 1790 まで
    g.append(_text(min((x0r + min(x1r, W - 20)) / 2, 1790.0), yg + 46, "滑走路", 30, C17["fw"], "middle"))
    # 1km の物差し。⑤b-4 の下見：全体（all）で左上に置くと c214 の点（17km・約760m）の輪に触れた＝全体は左下の地面のすぐ上／
    #   試し焼き 39377897273：寄り（near）で左下に置くと c412 の滑走路からの物差しの点線（5.5km）が字「1km（横）」を横切った＝寄りは左上
    xa = 96.0
    xb = xa + c4_ruler(view)["pxkm"]
    ys = yg - 40.0 if view == "all" else 178.0
    g.append(f'<path d="M {xa:.1f} {ys - 10:.1f} L {xa:.1f} {ys:.1f} L {xb:.1f} {ys:.1f} L {xb:.1f} {ys - 10:.1f}" fill="none" '
             f'stroke="{C17["fw"]}" stroke-width="3"/>')
    g.append(_text(xb + 14, ys + 9, "1km（横）", 26, C17["fw"], "start"))
    return "".join(g)


def c4_gs_svg(view):
    d = c4_data()["glide"]
    t = math.tan(math.radians(float(d["deg"])))
    V = C4_VIEW[view]
    k_hi = min(V["k0"], V["mtop"] * 1.02 / 1000.0 / t - float(d["d0"]))
    p = (c4_x(view, k_hi), c4_y(view, t * (k_hi + float(d["d0"])) * 1000.0))
    q = (c4_x(view, -float(d["d0"])), c4_y(view, 0.0))
    return (f'<path d="M {p[0]:.1f} {p[1]:.1f} L {q[0]:.1f} {q[1]:.1f}" stroke="{C17["gs"]}" stroke-width="4" '
            f'stroke-dasharray="18 12" opacity="0.85"/>')


def c4_gs_pt(view, km):
    d = c4_data()["glide"]
    return (c4_x(view, km), c4_y(view, math.tan(math.radians(float(d["deg"]))) * (km + float(d["d0"])) * 1000.0))


def c4_path_svg(view, t):
    pts = c4_seg(view, C4_VIEW[view]["k0"], c4_km(t))
    return (_path(pts, "none", C17["ring_ol"], 13.0, op=0.7, close=False)
            + _path(pts, "none", C17["path4"], 6.0, close=False))


def c4_hl_svg(view, a, b, col=None):
    pts = c4_seg(view, c4_km(a), c4_km(b))
    return _path(pts, "none", col or C17["ring"], 18.0, op=0.55, close=False)


def c4_mk_svg(view, t):
    x, y = c4_xy(view, c4_km(t))
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{C17["ring"]}" stroke="{C17["ring_ol"]}" stroke-width="5"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{C17["ring_ol"]}"/>')


def c4_dot_svg(view, t, col=None):
    x, y = c4_xy(view, c4_km(t))
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{col or C17["fw"]}" stroke="{C17["ring_ol"]}" stroke-width="4"/>'


def c4_dist_svg(view, t):
    """滑走路の末端（0km）から、その時刻の点の真下までの物差し（地面の下）"""
    xa, xb = c4_x(view, 0.0), c4_x(view, c4_km(t))
    y = C4_VIEW[view]["yg"] + 34
    x_pt, y_pt = c4_xy(view, c4_km(t))
    return (f'<path d="M {xb:.1f} {y_pt + 18:.1f} L {xb:.1f} {y:.1f}" stroke="{C17["fw"]}" stroke-width="2.5" stroke-dasharray="8 8" opacity="0.8"/>'
            f'<path d="M {xa:.1f} {y - 14:.1f} L {xa:.1f} {y + 14:.1f} M {xa:.1f} {y:.1f} L {xb:.1f} {y:.1f} M {xb:.1f} {y - 14:.1f} '
            f'L {xb:.1f} {y + 14:.1f}" stroke="{C17["ring"]}" stroke-width="5" stroke-linecap="round"/>')


def c4_arrow_svg(view, t, kind):
    x, y = c4_xy(view, c4_km(t))
    if kind == "push":                      # 操縦輪を押す（機首下げ）＝手の色
        return _arrow((x, y + 26), (x, y + 150), C17["man"])
    if kind == "back":                      # 下り道へ戻ろうとする（向き＝点線の矢印）
        q = c4_gs_pt(view, c4_km(t) - 0.55)
        return (f'<path d="M {x + 18:.1f} {y + 14:.1f} Q {(x + q[0]) / 2 + 10:.1f} {y + 6:.1f} {q[0] - 16:.1f} {q[1] - 22:.1f}" fill="none" '
                f'stroke="{C17["fw"]}" stroke-width="5" stroke-dasharray="12 9"/>'
                + _path([(q[0] - 4, q[1] - 6), (q[0] - 28, q[1] - 16), (q[0] - 14, q[1] - 34)], C17["fw"]))
    # dev＝下り道からの上へのずれ（下り道の点からその時刻の点までの縦の括弧）
    g = c4_gs_pt(view, c4_km(t))
    return (f'<path d="M {x - 26:.1f} {g[1]:.1f} L {x - 38:.1f} {g[1]:.1f} L {x - 38:.1f} {y + 4:.1f} L {x - 26:.1f} {y + 4:.1f}" fill="none" '
            f'stroke="{C17["ring"]}" stroke-width="5"/>')


def _scene_C4(start, states, steps):
    allst = [start] + states
    _head_only("C4", start, states, ("view", "switch"))
    v = start["view"]
    R = C4_REC
    rul = c4_ruler(v)
    parts = [dict(_part("bg", c4_bg_svg(v), R["rwy"]), geo=dict(kind="c4ruler", view=v, **rul, label=c4_label(v)))]
    if any(st["c4gs"] == "on" for st in allst):
        d = c4_data()["glide"]
        parts.append(dict(_part("gs", c4_gs_svg(v), R["gs"], keys=_akeys(start, states, steps, lambda st: st["c4gs"] == "on")),
                          geo=dict(kind="c4gs", deg=float(d["deg"]), d0=float(d["d0"]), a=list(c4_gs_pt(v, 3.0)), b=list(c4_gs_pt(v, 1.0)))))
    for nm, (a, b), fld in (("hl_lever", C4_LEVER, "lever"), ("hl_flat", C4_FLAT, "flat")):
        if any(st["c4hl"] == fld for st in allst):
            parts.append(dict(_part(nm, c4_hl_svg(v, a, b), R[fld], keys=_akeys(start, states, steps, lambda st, f=fld: st["c4hl"] == f, 0.8)),
                              geo=dict(kind="c4hl", hl=fld, a=a, b=b)))
    # 線＝時刻ごとに1本（段で長くなる＝入れ替える）。🔴 頂点（15:31）より先は描かない
    for t in sorted({st["c4t"] for st in allst}, key=c4_sec):
        pts = c4_seg(v, C4_VIEW[v]["k0"], c4_km(t))
        parts.append(dict(_part("path_" + t.replace(":", ""), c4_path_svg(v, t), R["path"],
                                keys=_akeys(start, states, steps, lambda st, t=t: st["c4t"] == t, 0.9)),
                          geo=dict(kind="c4path", t=t, pts=[list(p) for p in pts])))
    if any(st["c4go"] == "on" for st in allst):
        x, y = c4_xy(v, c4_km(C4_LEVER[0]))
        parts.append(dict(_part("go", c4_dot_svg(v, C4_LEVER[0], C17["ring"]), R["lever"],
                                keys=_akeys(start, states, steps, lambda st: st["c4go"] == "on")),
                          geo=dict(kind="c4pt", t=C4_LEVER[0], xy=[x, y])))
    for t in sorted({st["c4t"] for st in allst if st["c4mk"] == "on"}, key=c4_sec):
        x, y = c4_xy(v, c4_km(t))
        parts.append(dict(_part("mk_" + t.replace(":", ""), c4_mk_svg(v, t), R["mk"],
                                keys=_akeys(start, states, steps, lambda st, t=t: st["c4mk"] == "on" and st["c4t"] == t, 0.9)),
                          geo=dict(kind="c4pt", t=t, xy=[x, y])))
    for t in sorted({st["c4t"] for st in allst if st["c4dist"] == "on"}, key=c4_sec):
        parts.append(dict(_part("dist_" + t.replace(":", ""), c4_dist_svg(v, t), R["dist18" if c4_km(t) < 3.0 else "dist5"],
                                keys=_akeys(start, states, steps, lambda st, t=t: st["c4dist"] == "on" and st["c4t"] == t)),
                          geo=dict(kind="c4dist", t=t, a=c4_x(v, 0.0), b=c4_x(v, c4_km(t)))))
    for kind in ("push", "back", "dev"):
        for t in sorted({st["c4t"] for st in allst if st["c4arrow"] == kind}, key=c4_sec):
            parts.append(dict(_part(f"arrow_{kind}_" + t.replace(":", ""), c4_arrow_svg(v, t, kind), R[kind],
                                    keys=_akeys(start, states, steps, lambda st, k=kind, t=t: st["c4arrow"] == k and st["c4t"] == t)),
                              geo=dict(kind="c4arrow", arrow=kind, t=t)))
    for ring, col in (("on", C17["ring"]), ("ap", C17["ap"])):
        for t in sorted({st["c4t"] for st in allst if st["c4ring"] == ring}, key=c4_sec):
            parts.append(dict(_part(f"ring_{ring}_" + t.replace(":", ""), _ring_circle(c4_xy(v, c4_km(t)), 38, col), R["ap" if ring == "ap" else "mk"],
                                    keys=_akeys(start, states, steps, lambda st, r=ring, t=t: st["c4ring"] == r and st["c4t"] == t, 0.5)),
                              geo=dict(kind="c4ring", ring=ring, t=t)))
    if start["switch"] == "on":
        parts.append(_switch_part(C4_SWITCH))
    return parts


def _c4_anchors(st):
    v, t = st["view"], st["c4t"]
    k = c4_km(t)
    x, y = c4_xy(v, k)
    a = dict(pt=(x, y - 30), pt_low=(x, y + 30), pt_l=(x - 30, y), pt_r=(x + 30, y))
    gx, gy = c4_xy(v, c4_km(C4_LEVER[0]))
    a.update(go=(gx, gy - 24), go_low=(gx, gy + 24))
    ax, ay = c4_xy(v, c4_km(C4_LEVER[1]))
    a.update(apex=(ax, ay - 24))
    fk = (c4_km(C4_FLAT[0]) + c4_km(C4_FLAT[1])) / 2
    fx, fy = c4_xy(v, fk)
    a.update(flat=(fx, fy - 18))
    lk = (c4_km(C4_LEVER[0]) + c4_km(C4_LEVER[1])) / 2
    a.update(lever=c4_xy(v, lk))
    a.update(gs=c4_gs_pt(v, max(k - 0.9, 0.3)), gs_far=c4_gs_pt(v, min(C4_VIEW[v]["k0"] - 1.2, k + 2.0)))
    yd = C4_VIEW[v]["yg"] + 34
    a.update(dist=((c4_x(v, 0.0) + c4_x(v, k)) / 2, yd - 8), push=(x, y + 150), rwy=(c4_x(v, -0.3), C4_VIEW[v]["yg"]))
    return a


def _c4_note(st0, states):
    return ("報告書を加工して作成・線の形は付図4（対地高度）・札の高さは本文の気圧高度・下り道の3度の線は付図4 の線に合わせた・"
            "点の時刻は付図4 の矢印から内挿")


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4 C5 相反の図＝C2 の尾翼（形と回し方をそのまま・縮めて上へ）＋押す手と自動操縦の矢印＋約30秒の時刻の帯
# ══════════════════════════════════════════════════════════
C5_T = dict(s=0.78, tx=-86.0, ty=-30.0)        # C2 の座標 → C5 の画面（ちょうつがい 1405,590 → 1010,430）
C5_TB = dict(t0=20 * 3600 + 14 * 60 + 8, t1=20 * 3600 + 14 * 60 + 58, x0=330.0, x1=1590.0, y=700.0, bh=46.0)   # 帯は y 608〜798（出典の行の上）
C5_AP = ("20:14:18", "20:14:49")                # 自動操縦が入っていた約30秒（p5「約30秒間使用」・p44・p46）
C5_SND = ("20:14:20", "20:14:34", "20:14:39")    # トリムのスイッチを操作したと思われる音（p45・p46・p53）
C5_LAB = "相反の図（尾翼を横から・機首が左）"
C5_SWITCH = "尾翼を横から見ると"
C5_REC = dict(
    ths="付図5 p1（THS の欄）・報告書 p78（APがTHSを、操縦士がエレベータをそれぞれ制御）",
    elev="付図5 p1（ELEVATOR の欄）",
    ap="報告書 p82（THSについては…オーバーライド中もAPがエンゲージされたままとなり、APに従った作動を続ける）",
    hand="報告書 p44（操縦輪を押して機首下げ操作）",
    band="報告書 p5（APがNo.2そしてNo.1とほぼ同時にエンゲージされ、その後、約30秒間使用された）・p46（14分49秒…両APを解除）",
    snd="報告書 p53（14分20秒、同34秒及び同39秒に、ピッチ・トリム・コントロール・スイッチの操作音）",
    warn="報告書 p78（2つの制御が同時に入力されていることを操縦士に知らせるための警報装置は装備されていなかった）",
    iff="報告書 p79（もしSBA300-22-6021による改修が実施されていれば、APは…15kg以上の力を加えることによりディスエンゲージされ）",
    lim="報告書 p56（THSは機首上げ一杯の-12.3°に達しており）",
)


def _c5g(svg):
    return f'<g transform="translate({C5_T["tx"]:.1f} {C5_T["ty"]:.1f}) scale({C5_T["s"]})">{svg}</g>'


def c5_pt(p):
    return (C5_T["s"] * p[0] + C5_T["tx"], C5_T["s"] * p[1] + C5_T["ty"])


def c5_tx(hms):
    T = C5_TB
    return T["x0"] + (_sec_of(hms) - T["t0"]) / (T["t1"] - T["t0"]) * (T["x1"] - T["x0"])


def c5_band_svg():
    T = C5_TB
    y, bh = T["y"], T["bh"]
    xa, xb = c5_tx(C5_AP[0]), c5_tx(C5_AP[1])
    g = [f'<rect x="{T["x0"] - 30:.1f}" y="{y - 92:.1f}" width="{T["x1"] - T["x0"] + 60:.1f}" height="190" rx="14" fill="{C17["band5"]}" opacity="0.92"/>',
         f'<path d="M {T["x0"]:.1f} {y + bh / 2 + 8:.1f} L {T["x1"]:.1f} {y + bh / 2 + 8:.1f}" stroke="{C17["axis"]}" stroke-width="3"/>',
         f'<rect x="{xa:.1f}" y="{y - bh / 2:.1f}" width="{xb - xa:.1f}" height="{bh:.1f}" rx="8" fill="{C17["ap"]}" opacity="0.9"/>',
         # 試し焼き 39377897273：真ん中寄せだと c519 の時刻の線（20:14:37）が字の「）」を貫いた＝左寄せ（帯の頭から）
         f'<text x="{xa + 18:.1f}" y="{y + 11:.1f}" font-family="Noto" font-size="30" fill="{C17["bar_txt"]}" text-anchor="start">自動操縦（2つ）</text>']
    for t in C5_AP:
        x = c5_tx(t)
        g.append(f'<path d="M {x:.1f} {y + bh / 2 + 8:.1f} L {x:.1f} {y + bh / 2 + 22:.1f}" stroke="{C17["axis"]}" stroke-width="3"/>')
        g.append(_text(x, y + bh / 2 + 56, t, 26, C17["axis"], "middle"))
    return "".join(g)


def c5_snd_svg(n):
    """操作の音の印（トリムのスイッチ）＝時刻の帯の上の小さな印 n 個（時刻の字つき）"""
    T = C5_TB
    g = []
    for t in C5_SND[:n]:
        x = c5_tx(t)
        y = T["y"] - T["bh"] / 2 - 14
        g.append(_path([(x, y), (x - 13, y - 22), (x + 13, y - 22)], C17["ring"], C17["ring_ol"], 3))
        g.append(_text(x, y - 34, t, 22, C17["ring"], "middle"))   # 時刻は「時:分:秒」の形（「14:20」だと門番 ⑤ が14時20分と読む）
    return "".join(g)


def c5_cur_svg(hms):
    T = C5_TB
    x = c5_tx(hms)
    return (f'<path d="M {x:.1f} {T["y"] - T["bh"] / 2 - 8:.1f} L {x:.1f} {T["y"] + T["bh"] / 2 + 8:.1f}" stroke="{C17["ring_ol"]}" '
            f'stroke-width="11" opacity="0.6"/><path d="M {x:.1f} {T["y"] - T["bh"] / 2 - 8:.1f} L {x:.1f} {T["y"] + T["bh"] / 2 + 8:.1f}" '
            f'stroke="{C17["cur"]}" stroke-width="6"/>')


def c5_spk_svg(c, cross=True, s=1.0):
    """警報の音の印（スピーカー）。cross＝赤の ×（鳴らない・無い）"""
    x, y = c
    k = s
    g = [_path([(x - 34 * k, y - 16 * k), (x - 14 * k, y - 16 * k), (x + 10 * k, y - 38 * k), (x + 10 * k, y + 38 * k), (x - 14 * k, y + 16 * k),
                (x - 34 * k, y + 16 * k)], C17["spk"], C17["ring_ol"], 3)]
    for r in (26, 44):
        g.append(f'<path d="M {x + 18 * k:.1f} {y - r * k * 0.8:.1f} Q {x + (18 + r) * k:.1f} {y:.1f} {x + 18 * k:.1f} {y + r * k * 0.8:.1f}" '
                 f'fill="none" stroke="{C17["spk"]}" stroke-width="5" stroke-linecap="round"/>')
    if cross:
        r = 46 * k
        for w, col in ((17, C17["ring_ol"]), (10, C17["red"])):
            g.append(f'<path d="M {x - r:.1f} {y - r:.1f} L {x + r + 20 * k:.1f} {y + r:.1f} M {x + r + 20 * k:.1f} {y - r:.1f} L {x - r:.1f} {y + r:.1f}" '
                     f'stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
    return "".join(g)


C5_SPK = (1660.0, 560.0)       # ⑤b-4 の下見：(1700, 300) だと札「知らせる警報は無かった」が自動操縦の矢印（x 1287）に接した＝右下へ


def _scene_C5(start, states, steps):
    allst = [start] + states
    _head_only("C5", start, states, ("view", "c5kind", "switch"))
    R = C5_REC
    piv = c5_pt((C2_HX, C2_Y))
    rot_t = (lambda st: dict(rot=float(st["c5ths"])))                       # noqa: E731
    rot_e = (lambda st: dict(rot=float(st["c5ths"]) + float(st["c5elev"])))  # noqa: E731
    parts = [_part("bg", c2_bg_svg(), C2_REC["body"]), _part("body", _c5g(c2_body_svg()), C2_REC["body"])]
    if any(st["c5if"] == "on" for st in allst):
        parts.append(dict(_part("if_ghost", _c5g(_path(c2_ths_pts(C2_GHOST), "none", C17["ring"], 4.0, extra=' stroke-dasharray="14 10"')),
                                R["iff"], keys=_akeys(start, states, steps, lambda st: st["c5if"] == "on", 0.8)),
                          geo=dict(kind="c5if", deg=C2_GHOST)))
    if any(st["c5lim"] == "on" for st in allst):
        parts.append(dict(_part("lim", _c5g(c2_lim_svg()), R["lim"], keys=_akeys(start, states, steps, lambda st: st["c5lim"] == "on")),
                          geo=dict(kind="c5lim", deg=C2_LIM)))
    parts.append(dict(_part("ths", _c5g(c2_surface_svg(c2_ths_pts(), C17["ths"])), R["ths"], piv, IL._keys(start, states, steps, rot_t)),
                      geo=dict(kind="c5ths")))
    if any(st["c5ap"] == "on" for st in allst):
        parts.append(dict(_part("ths_ap", _c5g(c2_surface_svg(c2_ths_pts(), C17["ap"], 0.92)), R["ap"], piv, IL._keys(start, states, steps, rot_t)),
                          akeys=_akeys(start, states, steps, lambda st: st["c5ap"] == "on"), geo=dict(kind="c5ap")))
    parts.append(dict(_part("elev", _c5g(c2_surface_svg(c2_elev_pts(), C17["elev"])), R["elev"], piv, IL._keys(start, states, steps, rot_e)),
                      geo=dict(kind="c5elev")))
    if any(st["c5hand"] == "on" for st in allst):
        parts.append(dict(_part("elev_hand", _c5g(c2_surface_svg(c2_elev_pts(), C17["man"], 0.95)), R["hand"], piv,
                                IL._keys(start, states, steps, rot_e)),
                          akeys=_akeys(start, states, steps, lambda st: st["c5hand"] == "on"), geo=dict(kind="c5hand")))
    parts.append(_part("hinge", _c5g(c2_hinge_svg()), C2_REC["ths"]))
    for kind, fld in (("ap", "c5ap"), ("hand", "c5hand")):
        if any(st[fld] == "on" for st in allst):
            parts.append(dict(_part("arrow_" + kind, _c5g(c2_arrows_svg(kind)), R[kind],
                                    keys=_akeys(start, states, steps, lambda st, f=fld: st[f] == "on")), geo=dict(kind="c5arrow", arrow=kind)))
    if any(st["c5band"] == "on" for st in allst):
        parts.append(dict(_part("band", c5_band_svg(), R["band"], keys=_akeys(start, states, steps, lambda st: st["c5band"] == "on")),
                          geo=dict(kind="c5band", a=C5_AP[0], b=C5_AP[1])))
    for n in sorted({int(st["c5snd"]) for st in allst if int(st["c5snd"]) > 0}):
        if any(st["c5band"] != "on" and int(st["c5snd"]) > 0 for st in allst):
            raise ValueError("illu C5：操作の音の印（c5snd）は時刻の帯（c5band）と一緒に")
        parts.append(dict(_part(f"snd{n}", c5_snd_svg(n), R["snd"], keys=_akeys(start, states, steps, lambda st, n=n: int(st["c5snd"]) == n, 0.4)),
                          geo=dict(kind="c5snd", times=list(C5_SND[:n]))))
    for hms in sorted({st["c5cur"] for st in allst if st["c5cur"] != "off"}):
        parts.append(dict(_part("cur_" + hms.replace(":", ""), c5_cur_svg(hms), R["band"],
                                keys=_akeys(start, states, steps, lambda st, h=hms: st["c5cur"] == h)), geo=dict(kind="c5cur", hms=hms)))
    if any(st["c5warn"] == "on" for st in allst):
        parts.append(dict(_part("warn", c5_spk_svg(C5_SPK), R["warn"], keys=_akeys(start, states, steps, lambda st: st["c5warn"] == "on")),
                          geo=dict(kind="c5warn")))
    if start["switch"] == "on":
        parts.append(_switch_part(C5_SWITCH))
    return parts


def _c5_anchors(st):
    t, e = float(st["c5ths"]), float(st["c5elev"])
    xs = C2_LE + 0.30 * (C2_TE - C2_LE)
    xe = C2_HX + 0.55 * (C2_TE - C2_HX)
    T = C5_TB
    a = dict(ths=c5_pt(c2_rot((xs, C2_Y - _c2_half(xs)), t)), ths_low=c5_pt(c2_rot((xs, C2_Y + _c2_half(xs)), t)),
             le=c5_pt(c2_rot((C2_LE, C2_Y), t)), elev=c5_pt(c2_rot((xe, C2_Y - _c2_half(xe)), t + e)),
             elev_low=c5_pt(c2_rot((xe, C2_Y + _c2_half(xe)), t + e)), te=c5_pt(c2_rot((C2_TE, C2_Y), t + e)),
             ap_up=c5_pt((C2_TE + 60, C2_Y - 112)), hand_dn=c5_pt((C2_TE + 60, C2_Y + 116)), ap_le=c5_pt((C2_LE - 58, C2_Y + 96)),
             fin=c5_pt((1390.0, 260.0)), body=c5_pt((520.0, 600.0)), lim=c5_pt(c2_rot((C2_LE - 62, C2_Y), C2_LIM)),
             ghost=c5_pt(c2_rot((C2_LE, C2_Y), C2_GHOST)),
             band=((c5_tx(C5_AP[0]) + c5_tx(C5_AP[1])) / 2, T["y"] - T["bh"] / 2 - 4), band_top=((T["x0"] + T["x1"]) / 2, T["y"] - 92.0),
             spk=(C5_SPK[0], C5_SPK[1] + 60))
    if st["c5cur"] != "off":
        a["cur"] = (c5_tx(st["c5cur"]), T["y"] - T["bh"] / 2 - 8)
    return a


def _c5_note(st0, states):
    if st0["c5kind"] == "model":
        return "報告書を加工して作成・形と角度の動きは模式（付図15 の位置と数だけ）"
    return "報告書を加工して作成・形は模式（付図15 の位置と数だけ）・角度は付図5 の値"


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4 C6 夜の操縦室（後ろから前を向いて）＝C3 の部屋＋トリムの表示とトリム・ホイール（p84 の①②）・視線・警報の印（③）
# ══════════════════════════════════════════════════════════
# 🔴 出典の行（2行のとき y 約834〜884・左から x 1100 あたりまで）より上に収める＝ホイールは y 590〜790・表示は y 660〜720
#    （試し焼き 39377897273：表示を y 805 に置くと輪が出典の行の1行目と x 1030〜1140 で重なった＝右のレバーとホイールのあいだへ上げた）
C6_WHEEL = ((706.0, 690.0), (1214.0, 690.0))     # トリム・ホイール＝センタペデスタルの両側（p84②・位置は模式）
C6_IND = (822.0, 660.0)                           # ビジュアル・トリム・インジケータ＝センタペデスタルの上（p84①・模式）＝左のレバーと左のホイールのあいだ
C6_INDS = 0.75                                    # 表示の大きさ（90×60）
C6_EYE = (1500.0, 360.0)                         # 右の席（副操縦士・p73）の目の高さ（見た向き＝人は描かない）
C6_SPK = (300.0, 360.0)
C6_LAB = "夜の操縦室（後ろから前を向いて）"
C6_SWITCH = "操縦室の中では"
C6_REC = dict(
    room="報告書 p84（本事故の場合は夜間であった）・p73（副操縦士が路線において操縦する場合は、右席で実施）",
    wheel="報告書 p84（②トリム・ホイール：センタペデスタルの両側にあり…縞模様のマーキング）",
    ind="報告書 p84（①ビジュアル・トリム・インジケータ：センタペデスタル上にあり、THSの位置を表示する）",
    eye="報告書 p84（1及び2は、パイロットの視野の中に常時あるものではなく）",
    night="報告書 p84（夜間であったことから、THSの作動認識装置としては、有効に機能し得なかった）",
    warn="報告書 p84（③THSモーション・ウォーニング…APはCMDにエンゲージされていたため、3は作動しなかった）",
    warn2="報告書 p95（アウト・オブ・トリム状態を…直接的かつ積極的に認識させる警報・認識機能が無かった）",
)


def c6_wheel_svg(c):
    x, y = c
    rx, ry = 28.0, 100.0
    g = [f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" fill="{C17["trimw"]}" stroke="{C17["trimw_ln"]}" stroke-width="4"/>']
    for k in range(-4, 5):                                            # 縞模様（p84）
        yy = y + k * 21
        w = rx * math.sqrt(max(0.0, 1 - ((yy - y) / ry) ** 2))
        g.append(f'<path d="M {x - w + 4:.1f} {yy + 6:.1f} L {x + w - 4:.1f} {yy - 6:.1f}" stroke="{C17["trimw_ln"]}" stroke-width="5"/>')
    return "".join(g)


def c6_ind_svg():
    x, y = C6_IND
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({C6_INDS}) translate({-x:.1f} {-y:.1f})">' + _c6_ind_body() + "</g>")


def _c6_ind_body():
    x, y = C6_IND
    g = [f'<rect x="{x - 60:.1f}" y="{y - 40:.1f}" width="120" height="80" rx="8" fill="{C17["scr"]}" stroke="{C17["ped_ln"]}" stroke-width="3"/>',
         f'<path d="M {x - 40:.1f} {y + 22:.1f} A 46 46 0 0 1 {x + 40:.1f} {y + 22:.1f}" fill="none" stroke="{C17["tick"]}" stroke-width="4"/>']
    for k in range(5):
        a = math.radians(-150 + k * 30)
        g.append(f'<path d="M {x + 40 * math.cos(a):.1f} {y + 44 + 40 * math.sin(a) - 22:.1f} L {x + 50 * math.cos(a):.1f} '
                 f'{y + 44 + 50 * math.sin(a) - 22:.1f}" stroke="{C17["tick"]}" stroke-width="3"/>')
    g.append(f'<path d="M {x:.1f} {y + 22:.1f} L {x - 22:.1f} {y - 8:.1f}" stroke="{C17["fw"]}" stroke-width="5" stroke-linecap="round"/>')
    return "".join(g)


def c6_eye_svg():
    ex, ey = C6_EYE
    g = [f'<path d="M {ex - 58:.1f} {ey:.1f} Q {ex:.1f} {ey - 46:.1f} {ex + 58:.1f} {ey:.1f} Q {ex:.1f} {ey + 46:.1f} {ex - 58:.1f} {ey:.1f} Z" '
         f'fill="{C17["eye"]}" stroke="{C17["ring_ol"]}" stroke-width="4"/>',
         f'<circle cx="{ex:.1f}" cy="{ey - 6:.1f}" r="19" fill="{C17["sym"]}"/>']
    for q in ((1500.0, 120.0), (1200.0, 130.0)):                    # 前の窓と画面の上の端へ（視線）
        g.append(f'<path d="M {ex:.1f} {ey - 50:.1f} L {q[0]:.1f} {q[1] + 26:.1f}" stroke="{C17["eye"]}" stroke-width="5" stroke-dasharray="14 10"/>')
        g.append(_arrow((q[0] + (ex - q[0]) * 0.12, q[1] + 26 + (ey - 50 - q[1] - 26) * 0.12), (q[0], q[1] + 20), C17["eye"], w=5, head=22))
    return "".join(g)


def c6_night_svg():
    """夜で見えにくい＝ペデスタルの下の部分を暗く（p84）"""
    return (f'<path d="M 600 560 L 1320 560 L 1420 {H + 4} L 500 {H + 4} Z" fill="{C17["dark6"]}" opacity="0.62"/>')


def _scene_C6(start, states, steps):
    allst = [start] + states
    _head_only("C6", start, states, ("view", "switch"))
    R = C6_REC
    parts = [_part("room", c3_room_svg(), R["room"]),
             dict(_part("lamps", c3_lamps_svg(False), C3_REC["lamps"],
                        keys=_akeys(start, states, steps, lambda st: st["c6ap"] != "on", 0.35)), obj=dict(autopilot=2))]
    if any(st["c6ap"] == "on" for st in allst):
        parts.append(_part("lamps_on", c3_lamps_svg(True), C3_REC["lamps"], keys=_akeys(start, states, steps, lambda st: st["c6ap"] == "on", 0.35)))
    parts.append(_part("yoke_L", c3_yoke_svg("L"), C3_REC["yoke"]))
    parts.append(_part("yoke_R", c3_yoke_svg("R"), C3_REC["yoke"]))
    parts.append(dict(_part("levers", c3_levers_svg(), C3_REC["lever"]), obj=dict(thrust_lever=2),
                      geo=dict(kind="c3levers", knobs=[list(p) for p in C3_LEV], go=list(C3_GO), at=list(C3_AT))))
    parts.append(dict(_part("wheels", "".join(c6_wheel_svg(c) for c in C6_WHEEL), R["wheel"]), obj=dict(trim_wheel=2),
                      geo=dict(kind="c6wheel", xy=[list(c) for c in C6_WHEEL])))
    parts.append(dict(_part("ind", c6_ind_svg(), R["ind"]), obj=dict(trim_indicator=1), geo=dict(kind="c6ind", xy=list(C6_IND))))
    if any(st["c6night"] == "on" for st in allst):
        parts.append(_part("night", c6_night_svg(), R["night"], keys=_akeys(start, states, steps, lambda st: st["c6night"] == "on", 1.0)))
    if any(st["c6ring"] == "on" for st in allst):
        svg = "".join(_ring_rect(c[0] - 40, c[1] - 118, c[0] + 40, c[1] + 118) for c in C6_WHEEL) + _ring_rect(
            C6_IND[0] - 60, C6_IND[1] - 44, C6_IND[0] + 60, C6_IND[1] + 40)
        parts.append(_part("ring", svg, R["wheel"], keys=_akeys(start, states, steps, lambda st: st["c6ring"] == "on", 0.5)))
    if any(st["c6eye"] == "on" for st in allst):
        parts.append(dict(_part("eye", c6_eye_svg(), R["eye"], keys=_akeys(start, states, steps, lambda st: st["c6eye"] == "on")),
                          geo=dict(kind="c6eye")))
    if any(st["c6warn"] == "on" for st in allst):
        parts.append(dict(_part("warn", c5_spk_svg(C6_SPK), R["warn"], keys=_akeys(start, states, steps, lambda st: st["c6warn"] == "on")),
                          geo=dict(kind="c6warn")))
    if start["switch"] == "on":
        parts.append(_switch_part(C6_SWITCH))
    return parts


def _c6_anchors(st):
    return dict(wheel_L=(C6_WHEEL[0][0] - 40, C6_WHEEL[0][1] - 120), wheel_R=(C6_WHEEL[1][0] + 40, C6_WHEEL[1][1] - 120),
                ind=(C6_IND[0] - 20, C6_IND[1] + 44), eye=(C6_EYE[0], C6_EYE[1] + 50), spk=(C6_SPK[0], C6_SPK[1] + 60),
                lamps=((C3_LAMPS[0][0] + C3_LAMPS[1][0]) / 2, C3_LAMPS[0][1] + 18), ped=(960.0, 760.0))


def _c6_note(st0, states):
    return "報告書を加工して作成・操縦室の形と並びは模式（付図22・写真51 の位置と数だけ）・トリムの装置の位置は p84 の言葉から（模式）"


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4 C7 機体を横から（機首が右＝C4 の進む向き）＝機首の角度・迎え角・推力・水平安定板。🔴 頂点（20:15:31）で止める
# ══════════════════════════════════════════════════════════
C7_K = 15.0                                     # 1メートル＝15画素（全長 約54m＝810画素・形は模式）
C7_CG = (1000.0, 480.0)                         # 機首の角度で回す中心（画面）＝52度でも尾が出典の行（y 約866）に届かない（尾 y 約800）
C7_XC = 27.0                                    # 胴体の座標で CG に置く点（尾の端から m）
C7_UP = [(0.0, 1.4), (4.0, 2.4), (8.0, 2.8), (46.0, 2.8), (49.0, 2.5), (51.5, 1.8), (53.2, 0.6), (54.0, -0.4)]
C7_LO = [(53.6, -1.4), (52.0, -2.3), (49.0, -2.8), (14.0, -2.8), (8.0, -1.6), (3.0, -0.2), (0.0, 0.6)]
C7_FIN = [(11.0, 2.7), (4.2, 11.6), (1.2, 11.6), (0.3, 1.5)]
C7_WING = [(20.0, -1.9), (31.0, -1.5), (31.6, -2.0), (20.6, -2.7)]
C7_ENG = (27.0, 34.6, -3.75, 1.25)              # 手前のエンジン（前後の m・中心の高さ・半径）
C7_THS = [(0.9, 1.75), (2.6, 2.05), (6.4, 2.0), (6.9, 1.75), (6.4, 1.5), (2.6, 1.45)]   # 水平安定板（前の端＝右）
C7_THS_P = (3.0, 1.75)                          # 水平安定板の回る所（模式＝後ろ寄り）
C7_ELEV = [(-0.6, 1.72), (0.9, 1.95), (0.9, 1.55)]                                    # 昇降舵（後ろの端＝左）
C7_ELEV_P = (0.9, 1.75)
C7_LAB = "機体を横から見た図（機首が右）"
C7_SWITCH = "機体を横から見ると"
C7_REC = dict(
    body="報告書 p6（同機は急上昇を始めるとともにAOAが急激に増加し）・付図5 p1（PITCH の欄）",
    pitch="付図5 p1（PITCH の欄）・報告書 p60（ピッチ角21.5°・40.3°）・p49（52.6°・43.8°）",
    ths="付図5 p1（THS の欄）・報告書 p5（同15分11秒まで引き続き-12.3°のまま）",
    elev="付図5 p1（ELEVATOR の欄）",
    wind="報告書 p83（迎え角が増加し）・付図5 p1（AOA c の欄）",
    thr_auto="報告書 p46（アルファ・フロア機能が作動したことによるものと考えられる）・p47（増加した出力により…上昇に移った）",
    thr_man="報告書 p47（15分11秒機長(PF)は、一旦絞ったスラストをフル・スラストまで増加させ）",
    push="報告書 p47（15分03秒…操縦輪を限界まで一杯に押し続けたが、なおも機首上げの傾向が続いた）",
    push_fo="報告書 p55（副操縦士が操縦輪を押し続けていた）",
    rot="報告書 p56（アウト・オブ・トリム状態とアルファ・フロア機能の作動による出力の急激な増加がピッチ・アップ・モーメントの発生を生じさせた）",
    warn="報告書 p6（同25秒、失速警報音が約2秒間作動した）",
    hzn="報告書 p6（気圧高度約1,730ft…に達した後）",
)


def P7(x, y):
    """胴体の座標（尾の端から m・上が正）→ 画面（機首の角度 0）"""
    return (C7_CG[0] + (x - C7_XC) * C7_K, C7_CG[1] - y * C7_K)


def _rotp(p, deg, about):
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    x, y = p[0] - about[0], p[1] - about[1]
    return (about[0] + c * x - s * y, about[1] + s * x + c * y)


def c7_body_svg():
    g = [_path([P7(*p) for p in C7_FIN], C17["plane"], C17["plane_ln"], 3.0),
         _path(IL._smooth([P7(*p) for p in C7_UP + C7_LO], closed=True, per=3), C17["plane"], C17["plane_ln"], 3.5),
         _path([P7(*p) for p in [(50.6, 0.7), (52.6, 0.8), (51.6, 1.6), (50.4, 1.5)]], C17["win1"], C17["plane_ln"], 2.0),
         _path([P7(*p) for p in C7_WING], C17["eng7"], C17["plane_ln"], 3.0)]
    x0, x1, yc, r = C7_ENG
    g.append(_path([P7(*p) for p in [(29.0, -2.4), (32.6, -2.2), (32.0, yc + r * 0.6), (29.4, yc + r * 0.6)]], C17["eng7"], C17["plane_ln"], 2.5))
    g.append(_path(IL._smooth([P7(*p) for p in [(x0, yc - r * 0.8), (x0 + 0.6, yc - r), (x1 - 0.4, yc - r), (x1, yc - r * 0.7),
                                                  (x1, yc + r * 0.7), (x1 - 0.4, yc + r), (x0 + 0.6, yc + r), (x0, yc + r * 0.8)]],
                               closed=True, per=3), C17["eng7"], C17["plane_ln"], 3.0))
    return "".join(g)


def c7_ths_svg(col=None, op=None):
    return _path([P7(*p) for p in C7_THS], col or C17["ths"], C17["plane_ln"], 2.5, op=op)


def c7_elev_svg(col=None, op=None):
    return _path([P7(*p) for p in C7_ELEV], col or C17["elev"], C17["plane_ln"], 2.5, op=op)


def c7_key(st, part):
    """部品の鍵（pivot＝CG）：機首の角度（反時計回り＝機首上げ）→ 水平安定板（前の端が下がる＝負）→ 昇降舵（後ろの端が下がる＝正）を、
    1つの回転（CG のまわり）＋ずらし（dx・dy）にまとめる（build_jiko は pivot のまわりに回してからずらす）"""
    a = -float(st["c7pitch"])
    b = -float(st["c7ths"]) if part in ("ths", "elev") else 0.0
    c = -float(st["c7elev"]) if part == "elev" else 0.0
    p = C7_CG
    if part == "elev":
        p = _rotp(p, c, P7(*C7_ELEV_P))
    if part in ("ths", "elev"):
        p = _rotp(p, b, P7(*C7_THS_P))
    p = _rotp(p, a, C7_CG)
    return dict(rot=a + b + c, dx=p[0] - C7_CG[0], dy=p[1] - C7_CG[1])


def c7_thr_svg(kind):
    x0, x1, yc, r = C7_ENG
    p, q = P7(x1 + 0.6, yc), P7(x1 + 11.0, yc)
    return _arrow(p, q, C17["ap"] if kind == "auto" else C17["man"], w=12, head=34)


def c7_rot_svg():
    """機首を上へ回す力（ピッチ・アップ・モーメント）＝機首のまわりの弧の矢印"""
    cx, cy = C7_CG
    r = 470.0
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(18, -36, -3)]
    q = pts[-1]
    ang = math.atan2(q[1] - pts[-3][1], q[0] - pts[-3][0])
    l = (q[0] - 30 * math.cos(ang - 0.5), q[1] - 30 * math.sin(ang - 0.5))
    rr = (q[0] - 30 * math.cos(ang + 0.5), q[1] - 30 * math.sin(ang + 0.5))
    return (f'<path d="{_d(pts, False)}" fill="none" stroke="{C17["ring_ol"]}" stroke-width="15" opacity="0.6"/>'
            f'<path d="{_d(pts, False)}" fill="none" stroke="{C17["ring"]}" stroke-width="9"/>' + _path([q, l, rr], C17["ring"], C17["ring_ol"], 3))


def c7_wind_svg(pitch, aoa):
    """向かってくる風（進む向きの逆）と迎え角の弧。進む向き＝機首の角度−迎え角（上が正）"""
    gam = float(pitch) - float(aoa)
    vx, vy = math.cos(math.radians(gam)), -math.sin(math.radians(gam))      # 画面の進む向き
    nose = _rotp(P7(54.0, -0.4), -float(pitch), C7_CG)
    g = []
    for k in (-1, 0, 1):
        ox, oy = -vy * 70 * k, vx * 70 * k
        s = (nose[0] + vx * 330 + ox, nose[1] + vy * 330 + oy)
        e = (nose[0] + vx * 120 + ox, nose[1] + vy * 120 + oy)
        g.append(_arrow(s, e, C17["wind"], w=6, head=24))
    # 迎え角の弧（翼の線＝機首の向き と 進む向き のあいだ）
    cx, cy = C7_CG
    r = 300.0
    a0, a1 = -float(pitch), -gam
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / 16)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / 16))) for k in range(17)]
    ax = (cx + r * 1.25 * math.cos(math.radians(-float(pitch))), cy + r * 1.25 * math.sin(math.radians(-float(pitch))))
    bx = (cx + r * 1.25 * math.cos(math.radians(-gam)), cy + r * 1.25 * math.sin(math.radians(-gam)))
    g.append(f'<path d="M {cx:.1f} {cy:.1f} L {ax[0]:.1f} {ax[1]:.1f} M {cx:.1f} {cy:.1f} L {bx[0]:.1f} {bx[1]:.1f}" stroke="{C17["ring"]}" '
             f'stroke-width="3" stroke-dasharray="10 8"/>')
    g.append(f'<path d="{_d(pts, False)}" fill="none" stroke="{C17["ring"]}" stroke-width="7"/>')
    return "".join(g)


C7_SPK = (300.0, 330.0)


def _scene_C7(start, states, steps):
    allst = [start] + states
    _head_only("C7", start, states, ("view", "c7kind", "switch"))
    R = C7_REC
    g0 = [f'<defs><linearGradient id="c7sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C17["sky0"]}"/>'
          f'<stop offset="1" stop-color="{C17["sky1"]}"/></linearGradient></defs>',
          f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#c7sky)"/>',
          # 試し焼き 39377897273：y 836 は出典の行（2行のとき y 約834〜）の上の端に接した＝y 812（機首 52.6度でも尾の先は y 約790）
          f'<path d="M -4 812 L {W + 4} 812" stroke="{C17["horizon"]}" stroke-width="3" stroke-dasharray="22 14"/>']
    parts = [dict(_part("bg", "".join(g0), R["hzn"]), geo=dict(kind="c7bg"))]
    piv = C7_CG

    def key(part):
        return IL._keys(start, states, steps, lambda st: c7_key(st, part))
    parts.append(dict(_part("body", c7_body_svg(), R["body"], piv, key("body")), obj=dict(aircraft=1), geo=dict(kind="c7body")))
    parts.append(dict(_part("ths", c7_ths_svg(), R["ths"], piv, key("ths")), geo=dict(kind="c7ths")))
    if any(st["c7ap"] == "on" for st in allst):
        parts.append(dict(_part("ths_ap", c7_ths_svg(C17["ap"], 0.92), C5_REC["ap"], piv, key("ths")),
                          akeys=_akeys(start, states, steps, lambda st: st["c7ap"] == "on"), geo=dict(kind="c7ap")))
    parts.append(dict(_part("elev", c7_elev_svg(), R["elev"], piv, key("elev")), geo=dict(kind="c7elev")))
    if any(st["c7push"] != "off" for st in allst):
        parts.append(dict(_part("elev_hand", c7_elev_svg(C17["man"], 0.95), R["push"], piv, key("elev")),
                          akeys=_akeys(start, states, steps, lambda st: st["c7push"] != "off"), geo=dict(kind="c7push")))
    if any(st["c7ring"] == "on" for st in allst):
        c = P7(3.6, 1.75)
        parts.append(dict(_part("ring_ths", _ring_circle(c, 92.0), R["ths"], piv, key("body")),
                          akeys=_akeys(start, states, steps, lambda st: st["c7ring"] == "on", 0.5)))
    for kind in ("auto", "man"):
        if any(st["c7thr"] == kind for st in allst):
            parts.append(dict(_part("thr_" + kind, c7_thr_svg(kind), R["thr_" + kind], piv, key("body")),
                              akeys=_akeys(start, states, steps, lambda st, k=kind: st["c7thr"] == k), geo=dict(kind="c7thr", thr=kind)))
    if any(st["c7rot"] == "on" for st in allst):
        parts.append(dict(_part("rot", c7_rot_svg(), R["rot"], keys=_akeys(start, states, steps, lambda st: st["c7rot"] == "on")),
                          geo=dict(kind="c7rot")))
    for pa in sorted({(float(st["c7pitch"]), float(st["c7aoa"])) for st in allst if st["c7wind"] == "on"}):
        parts.append(dict(_part("wind_%g_%g" % pa, c7_wind_svg(*pa), R["wind"],
                                keys=_akeys(start, states, steps, lambda st, pa=pa: st["c7wind"] == "on" and
                                            (float(st["c7pitch"]), float(st["c7aoa"])) == pa, 0.8)),
                          geo=dict(kind="c7wind", pitch=pa[0], aoa=pa[1])))
    if any(st["c7warn"] == "on" for st in allst):
        parts.append(dict(_part("warn", c5_spk_svg(C7_SPK, cross=False), R["warn"], keys=_akeys(start, states, steps, lambda st: st["c7warn"] == "on")),
                          geo=dict(kind="c7warn")))
    if start["switch"] == "on":
        parts.append(_switch_part(C7_SWITCH))
    return parts


def _c7_anchors(st):
    a = -float(st["c7pitch"])

    def R(p):
        return _rotp(p, a, C7_CG)
    nose = R(P7(54.0, 1.0))
    k = c7_key(st, "ths")
    ths = _rotp(P7(5.0, 2.1), k["rot"], C7_CG)
    ths = (ths[0] + k["dx"], ths[1] + k["dy"])
    ke = c7_key(st, "elev")
    el = _rotp(P7(-0.2, 1.6), ke["rot"], C7_CG)
    el = (el[0] + ke["dx"], el[1] + ke["dy"])
    x0, x1, yc, r = C7_ENG
    return dict(nose=nose, tail=R(P7(2.0, 11.0)), ths=(ths[0], ths[1] - 30), ths_low=(ths[0], ths[1] + 30), elev=el, eng=R(P7(x1 + 6.0, yc - 1.0)),
                body=R(P7(30.0, 3.0)), wing=R(P7(26.0, -2.6)), rot=(C7_CG[0] + 470 * math.cos(math.radians(-36)), C7_CG[1] + 470 * math.sin(math.radians(-36))),
                cg=C7_CG, spk=(C7_SPK[0], C7_SPK[1] + 60), aoa=(C7_CG[0] + 330, C7_CG[1] - 20))


def _c7_note(st0, states):
    if st0["c7kind"] == "model":
        return "報告書を加工して作成・機体の形と角度は模式"
    return "報告書を加工して作成・機体の形は模式・角度は付図5 と本文の値・水平安定板と昇降舵の動きは見やすく小さな部品で"


# ══════════════════════════════════════════════════════════
#  型の表へ登録（illu.py の末尾から読まれる）
# ══════════════════════════════════════════════════════════
def register():
    IL.FIELDS.update(
        C1=dict(view="all", c1f="1400", c1ring="off", c1eye="off", c1land="off", c1cur="off", c1att="level", switch="off", cam=1.0),
        C2=dict(view="side", c2kind="rec", c2ths=0.0, c2elev=0.0, c2ap="off", c2hand="off", c2hl="off", c2arrow="off", c2ghost="off",
                c2arc="off", c2lim="off", switch="off", cam=1.0),
        C3=dict(view="front", c3thr="off", c3yoke="off", c3push="off", c3cap="off", c3ap="off", c3ring="off", switch="off", cam=1.0),
        # 🆕 ⑤b-4
        C4=dict(view="near", c4t="20:14:05", c4mk="on", c4gs="off", c4hl="off", c4go="off", c4dist="off", c4arrow="off", c4ring="off",
                switch="off", cam=1.0),
        C5=dict(view="side", c5kind="rec", c5ths=-5.3, c5elev=3.5, c5ap="off", c5hand="off", c5band="off", c5snd=0, c5cur="off",
                c5warn="off", c5if="off", c5lim="off", switch="off", cam=1.0),
        C6=dict(view="front", c6ap="off", c6ring="off", c6eye="off", c6night="off", c6warn="off", switch="off", cam=1.0),
        C7=dict(view="side", c7kind="rec", c7pitch=0.0, c7aoa=0.0, c7ths=-12.3, c7elev=0.0, c7ap="off", c7push="off", c7ring="off",
                c7thr="off", c7rot="off", c7wind="off", c7warn="off", switch="off", cam=1.0))
    IL.CHOICES.update(c1f=tuple(C1_FRAMES), c1ring=("off", "gsloc", "ga", "dual", "thr", "fd"), c1eye=IL.ONOFF,
                      c1land=("off", "on", "press"), c1att=("level", "high", "up"),
                      c2kind=("rec", "model"), c2ap=IL.ONOFF, c2hand=IL.ONOFF, c2hl=("off", "both", "ths", "elev"),
                      c2arrow=("off", "ap", "hand"), c2ghost=IL.ONOFF, c2arc=IL.ONOFF, c2lim=IL.ONOFF,
                      c3thr=IL.ONOFF, c3yoke=IL.ONOFF, c3push=IL.ONOFF, c3cap=IL.ONOFF, c3ap=IL.ONOFF, c3ring=("off", "go", "at", "lev"),
                      c4t=C4_T, c4mk=IL.ONOFF, c4gs=IL.ONOFF, c4hl=("off", "lever", "flat"), c4go=IL.ONOFF, c4dist=IL.ONOFF,
                      c4arrow=("off", "push", "back", "dev"), c4ring=("off", "on", "ap"),
                      c5kind=("rec", "model"), c5ap=IL.ONOFF, c5hand=IL.ONOFF, c5band=IL.ONOFF, c5snd=(0, 1, 2, 3), c5warn=IL.ONOFF,
                      c5if=IL.ONOFF, c5lim=IL.ONOFF,
                      c6ap=IL.ONOFF, c6ring=IL.ONOFF, c6eye=IL.ONOFF, c6night=IL.ONOFF, c6warn=IL.ONOFF,
                      c7kind=("rec", "model"), c7ap=IL.ONOFF, c7push=("off", "fo", "cap"), c7ring=IL.ONOFF, c7thr=("off", "auto", "man"),
                      c7rot=IL.ONOFF, c7wind=IL.ONOFF, c7warn=IL.ONOFF)
    IL.VIEWS.update(C1=("all", "band", "time"), C2=("side",), C3=("front",), C4=tuple(C4_VIEW), C5=("side",), C6=("front",), C7=("side",))
    IL.REC_FIELDS = IL.REC_FIELDS + ("c1f", "c1eye", "c1land", "c1cur", "c1att",
                                     "c2ths", "c2elev", "c2ap", "c2hand", "c2arrow", "c2ghost", "c2arc", "c2lim",
                                     "c3thr", "c3yoke", "c3push", "c3cap", "c3ap",
                                     "c4t", "c4hl", "c4dist", "c4arrow", "c4go",
                                     "c5ths", "c5elev", "c5ap", "c5hand", "c5snd", "c5if", "c5lim", "c5warn",
                                     "c6ap", "c6warn", "c6night",
                                     "c7pitch", "c7ths", "c7elev", "c7thr", "c7push", "c7warn", "c7ap", "c7aoa")
    IL.NOTE.update(C1=_c1_note, C2=_c2_note, C3=_c3_note, C4=_c4_note, C5=_c5_note, C6=_c6_note, C7=_c7_note)
    IL.EXTRA.update(
        C1=dict(scene=_scene_C1, anchors=_c1_anchors, camc=lambda st0, states: (960.0, 480.0),
                label=lambda st0, states: C1_LAB[st0["view"]]),
        C2=dict(scene=_scene_C2, anchors=_c2_anchors, camc=lambda st0, states: (C2_HX - 200.0, C2_Y),
                label=lambda st0, states: C2_LAB),
        C3=dict(scene=_scene_C3, anchors=_c3_anchors, camc=lambda st0, states: (960.0, 640.0),
                label=lambda st0, states: C3_LAB),
        C4=dict(scene=_scene_C4, anchors=_c4_anchors, camc=lambda st0, states: (960.0, 560.0),
                label=lambda st0, states: c4_label(st0["view"])),
        C5=dict(scene=_scene_C5, anchors=_c5_anchors, camc=lambda st0, states: (960.0, 480.0),
                label=lambda st0, states: C5_LAB),
        C6=dict(scene=_scene_C6, anchors=_c6_anchors, camc=lambda st0, states: (960.0, 640.0),
                label=lambda st0, states: C6_LAB),
        C7=dict(scene=_scene_C7, anchors=_c7_anchors, camc=lambda st0, states: C7_CG,
                label=lambda st0, states: C7_LAB))


register()
