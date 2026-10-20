# -*- coding: utf-8 -*-
"""mech17.py — 17本目（中華航空140便墜落事故）「図解」（2026-10-20 新設・⑤b-5）。

■ 何か
  23本目 `mech23` と同じ作り＝「基図＋段の層（その行から出て残る）＋動く部品（段の鍵で動く）」。再現イラストではない＝「再現」の札は出さない。
  左上に見る向き（ある見え方だけ＝門番 check_mech が PLAN の「見る向き：」と照らす）・左下に「模式」（原文の写しの見え方は付けない）と出典。
  🔴 人の形・顔・乗員の実名は描かない（席は席の形と役の札だけ）。🔴 CVR の言葉を絵の文字にしない（「解除して」は「機長の指示」と書く）。
  🔴 **色は役の色**（`jiko_style.ROLE`＝映像方針 17本目 §8-4）：人の操縦（押す）＝橙 company・自動の仕組み＝水色 ship・報告書＝青 state・
     エアバス社＝緑 airbus・当局と会社＝中立の線 LINE（だれかは札の言葉）。意味の色＝赤 ALERT（危ない・壊れ）・黄 AMBER（数・注意）

■ 見え方（view）＝映像方針の一覧 `ref/ep17/eizou_list17.md` の「見た目の型」（第1〜7章の図解 25カット）
  factors … 報告書の12の要因の並べ図（p95〜96）。札の形と大きさは全部同じ・番号は報告書の順          c110・c726（⑤b-6 の ca14・cb02 も）
  clock2  … 2つの時計（世界共通の時刻 11:14:05 ＋9時間＝日本の時刻 20:14:05）と単位の札                 c114
  seats   … 正面から見た操縦席の2つの席（左＝機長・右＝副操縦士・人は描かない）                         c205・c210
  hours   … 機長の飛行時間の棒（この型・全部＝p17・p38）と経歴の札                                    c206
  train   … 副操縦士の訓練の順の帯（地上の学科 → シミュレーター → 実際の機体で3時間＝p38）               c208
  area    … 面積のマス目（昇降舵：昇降舵を含めた水平安定板＝1：約3＝p55）と同じ角度の板                  c304
  afs     … 自動飛行システムの3つの箱（自動操縦・自動推力・飛行の指示）                                   c307
  band    … 横から見た進入の道と高さの帯（対地 約120m〈400ft〉以下のランドとゴー・アラウンドが対象外＝p78）  c317
  modes   … ゴー・アラウンドの抜け方の流れ（縦と横の両方＝抜ける／縦だけ＝表示は消え働きは残る／ランドのボタン＝抜けられない＝p54・p81〜82）
                                                                                                c321・c516
  fcom    … 表示（FMA）と操縦の手引き書（FCOM）の欄・書かれていない所・勧告（p81〜82・p103）            c322
  who3    … 自動操縦を入れた人の3つの可能性の札（p52〜53・p89＝並べるだけ）                             c504
  ths     … 水平安定板の角度の帯（時刻×角度＝付図5 の表と本文の値の点・点のあいだは直線）              c517・c603
  warn    … 警報音（THS モーション・ウォーニング）の設計の流れ（開発のとき・変更後・報告書の見方＝p84〜85）  c612・c615
  eu      … 上から見たイギリスとフランス（陸＝Natural Earth・国境なし）・イギリスの当局 → エアバス社      c613
  cards3  … 機長の考えの3つの可能性の札（番号と「？」だけ＝中身は次の3カットの語り）                     c616
  assist  … もう1つの押し方（電波の道を捕まえるとき＝自動操縦と同じ向き／この夜＝逆向き＝p57・p90）       c619
  afloor  … アルファ・フロアの流れ（迎え角が大きすぎる → 推力を自動で最大 → 失速を防ぐ＝p83）            c704
  pitch   … 分度器（機首の角度 最大 52.6度＝p49）＝針と機の形が段の鍵で回る                                c719
  pbars   … 機首の角度の棒（着陸の進入 約4度・表示が消える 25度・最大 52.6度・25度の2倍の線）              c720

■ SPEC の書き方（mech23 と同じ）
  fig=("m17", dict(view=…, start=dict(…), steps=[dict(state=dict(…)), …], rel=[dict(t="52.6", src="報告書 p49")], note="…", src=ss.src([…])))
  状態は前の段から引き継ぐ（書いた欄だけ変わる）。🔴 画面の字の数（時刻・数・角度）は全部 `rel=` に同じ文字列で宣言する
  （門番 check_mech の judge_m17 が**基図と段の層の全部の字**から数を拾って照らす＝札だけでなく描いた字も）。
  🔴 記録の値（要因の言葉と順・時刻・飛行時間・角度・面積の比・抜け方・手引き書の欄・可能性の札・点の時刻と角度）は門番の側
     REC_M17 が別に持つ（§5b-88）。描く側の表（FACTORS・CK2_T・HR_V・TH_PTS・PB_V・PT_DEG …）を書き換えると鳴る。
"""
from __future__ import annotations

import datetime
import json
import math
import re
from pathlib import Path

import jiko_style as J
import titan_fig as F
from mech21 import _P, _arrow, _box, _check, _on, _qmark, _xmark

HERE = Path(__file__).resolve().parent.parent
ONOFF = ("off", "on")
INK = J.INK_W
L_X = F.BX0 + 40.0
HAND = J.ROLE["company"]          # 人の操縦（押す）＝橙
AUTO = J.ROLE["ship"]             # 自動の仕組み＝水色
REP = J.ROLE["state"]             # 報告書＝青
AB = J.ROLE["airbus"]             # エアバス社＝緑
DIM = J.LINE_DIM
FMA_G = "#58e27f"                 # 表示（FMA）の緑の字＝再現イラスト C1 の色（illu17.C17["fg"]）


def rc(r):
    """役の名（ROLE）か意味の色の名（ALERT・LINE…）か #色 → 色の値。"""
    if not r:
        return INK
    if str(r).startswith("#"):
        return r
    return J.ROLE.get(r) or getattr(J, r)


def _tline(x, y, t, cap=30, col=None, anchor="start", mw=600, fam="Noto", ol=0):
    return F.txtfit(x, y, t, mw, cap=cap, col=col or INK, anchor=anchor, fam=fam, ol=ol)


def _card(cx, cy, w, h, col, fill=None, sw=4, dash=None):
    return F.rect(cx - w / 2, cy - h / 2, w, h, fill or J.BG2, col, sw, rx=10, dash=dash)


def _bracket(xa, xb, y, col=None, down=True, d=22):
    k = d if down else -d
    return F.poly([(xa, y + k), (xa, y), (xb, y), (xb, y + k)], "none", col or J.TICK, 4)


def _speaker(cx, cy, s=34.0, col=None):
    c = col or INK
    body = [(cx - s, cy - s * 0.45), (cx - s * 0.35, cy - s * 0.45), (cx + s * 0.25, cy - s), (cx + s * 0.25, cy + s),
            (cx - s * 0.35, cy + s * 0.45), (cx - s, cy + s * 0.45)]
    return F.poly(body, J.BG2, c, 5, close=True)


def _waves(cx, cy, n=3, r0=30, col=None):
    g = []
    for i in range(n):
        r = r0 + i * 18
        pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(-40, 41, 8)]
        g.append(F.poly(pts, "none", col or J.AMBER, 5))
    return "".join(g)


def _plane(cx, cy, L=180.0, deg=0.0, col=None, ln=None):
    """横から見た旅客機の形（機首が右・deg＝機首上げの角度・模式）。"""
    c, k = col or "#c9d1d7", ln or "#20282e"
    h = L * 0.10
    pts = [(0.50, 0.0), (0.46, -0.45), (0.38, -0.58), (-0.36, -0.58), (-0.47, -1.9), (-0.52, -1.9), (-0.50, -0.30),
           (-0.44, 0.40), (0.38, 0.45), (0.47, 0.30)]
    wing = [(0.06, 0.10), (-0.10, 0.85), (-0.16, 0.85), (-0.06, 0.10)]
    a = math.radians(-deg)

    def tr(u, v):
        x, y = u * L, v * h
        return (cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
    return (F.poly([tr(u, v) for u, v in pts], c, k, 3, close=True) + F.poly([tr(u, v) for u, v in wing], "#9aa4ac", k, 2, close=True))


def _num(t):
    """数の文字列（"1,350"・"52.6"）→ 数。"""
    return float(str(t).replace(",", ""))


# ══════════════════════════════════════════════════════════
#  factors（c110・c726）＝報告書の12の要因（p95〜96）。札は全部同じ形と大きさ・番号は報告書の順。
#  言葉は要約（原文の要点＝門番 REC_M17 の原文の句と照らす）。役＝だれの要因か（札の縁の色と下の行）
# ══════════════════════════════════════════════════════════
FACTORS = (
    ("誤ってゴー・レバー", "crew"), ("解除しないまま自動操縦", "crew"), ("重い操縦輪を押し続けた", "crew"),
    ("板と昇降舵が食い違った", "plane"), ("知らせる警報が無かった", "plane"), ("仕組みの理解に欠けた", "crew"),
    ("交替の時機が遅れた", "crew"), ("アルファ・フロアの作動", "plane"), ("立て直しが適切さを欠く", "crew"),
    ("2人の連携が不適切", "crew"), ("改修されていなかった", "airline"), ("推奨のまま・命令なし", "maker"),
)
FAC_WHO = dict(crew=("操縦の2人", "company"), plane=("機体の作り", "ship"), airline=("航空会社", "LINE"), maker=("メーカーと当局", "airbus"))
FG = dict(xs=(260.0, 580.0, 900.0, 1220.0), ys=(395.0, 545.0, 695.0), w=280.0, h=104.0, acc=(1620.0, 545.0, 250.0, 130.0), br=1400.0)
FAC_MK = dict(design=((1, "レバーの作り"), (5, "警報の無さ"), (6, "手引き書")), crew=((7, "交替の時機"), (9, "立て直し"), (10, "連携")))


def fac_xy(i):
    """要因 i（1〜12）の札の中心。"""
    k = i - 1
    return FG["xs"][k % 4], FG["ys"][k // 4]


def _fac_card(i):
    """札（中立の縁・番号・言葉）。言葉は上寄せ＝下の行（だれの要因か）の場所を空けておく。"""
    t, _who = FACTORS[i - 1]
    cx, cy = fac_xy(i)
    w, h = FG["w"], FG["h"]
    g = [_card(cx, cy, w, h, J.LINE)]
    g.append(F.txt(cx - w / 2 + 14, cy - h / 2 + 30, str(i), 26, J.AMBER, "Dela", "start"))
    g.append(_tline(cx + 10, cy + 4, t, 26, INK, "middle", w - 56))
    return "".join(g)


def _fac_role(i):
    """役の色の縁と下の行（だれの要因か）だけ＝札の字は描き直さない（🔧 門番 layout：同じ字を2つの層に描くと重なりで鳴る）。"""
    _t, who = FACTORS[i - 1]
    cx, cy = fac_xy(i)
    w, h = FG["w"], FG["h"]
    wt, wr = FAC_WHO[who]
    return (F.rect(cx - w / 2, cy - h / 2, w, h, "none", rc(wr), 5, rx=10)
            + _tline(cx, cy + 40, wt, 21, rc(wr), "middle", w - 40))


def factors_base(st0):
    return []


def factors_stage(prev, st):
    s = []
    if _on(prev, st, "cards"):
        for i in range(1, 13):
            s.append(_fac_card(i))
    if _on(prev, st, "roles"):
        for i in range(1, 13):
            s.append(_fac_role(i))
    if _on(prev, st, "chain"):
        w, h = FG["w"], FG["h"]
        for i in range(1, 13):
            cx, cy = fac_xy(i)
            if i % 4:
                s.append(F.line(cx + w / 2, cy, cx + w / 2 + (FG["xs"][1] - FG["xs"][0] - w), cy, J.LINE, 5))
            if i <= 8:
                s.append(F.line(cx, cy + h / 2, cx, cy + h / 2 + (FG["ys"][1] - FG["ys"][0] - h), J.LINE, 5))
    if _on(prev, st, "acc"):
        x, y, w, h = FG["acc"]
        s.append(_bracket(FG["br"], FG["br"], FG["ys"][0] - FG["h"] / 2, J.TICK))
        s.append(F.poly([(FG["br"] - 22, FG["ys"][0] - FG["h"] / 2), (FG["br"], FG["ys"][0] - FG["h"] / 2),
                         (FG["br"], FG["ys"][2] + FG["h"] / 2), (FG["br"] - 22, FG["ys"][2] + FG["h"] / 2)], "none", J.TICK, 4))
        s.append(_arrow(FG["br"], y, x - w / 2 - 6, y, J.ALERT, 6, 24))
        s.append(_card(x, y, w, h, J.ALERT, sw=6))
        s.append(_tline(x, y + 16, "事故", 44, J.ALERT, "middle", w - 30))
    for key, col in (("mk_design", J.AMBER), ("mk_crew", HAND)):
        if _on(prev, st, key):
            for i, t in FAC_MK[key[3:]]:
                cx, cy = fac_xy(i)
                w, h = FG["w"], FG["h"]
                s.append(F.rect(cx - w / 2 - 9, cy - h / 2 - 9, w + 18, h + 18, "none", col, 7, rx=14))
                s.append(_tline(cx + w / 2 + 6, cy - h / 2 - 14, t, 24, col, "end", w))
    return s


# ══════════════════════════════════════════════════════════
#  clock2（c114）＝報告書の時刻は世界共通の時刻（p4「時刻は協定世界時で記す」）。この動画は＋9時間（日本標準時）
# ══════════════════════════════════════════════════════════
CK2_T = "11:14:05"                # ゴー・レバー（p51「11時14分05秒に副操縦士がゴー・レバーを作動させた」）
CK2_ADD = 9                       # 日本標準時＝協定世界時＋9時間（p4「08時53分協定世界時(日本標準時17時53分)」）
CK2 = dict(xs=(560.0, 1360.0), y=450.0, r=120.0, ty=650.0, sy=700.0, uy=790.0)
CK2_CAP = ("世界共通の時刻（報告書）", "日本の時刻（日本標準時）")      # 🔧 門番 wording：「この動画」は楽屋の言葉
CK2_UNITS = (("フィート", "メートル"), ("ノット", "時速（キロ）"))


def ck2_times():
    t = datetime.datetime.strptime(CK2_T, "%H:%M:%S")
    return CK2_T, (t + datetime.timedelta(hours=CK2_ADD)).strftime("%H:%M:%S")


def ck2_angles(t):
    """時刻 → (短針, 長針, 秒針) の角度（度・12時から時計回り）。"""
    h, m, s = (int(x) for x in t.split(":"))
    return ((h % 12) * 30.0 + m * 0.5 + s / 120.0, m * 6.0 + s * 0.1, s * 6.0)


def _hand(cx, cy, ang, L, w, col):
    a = math.radians(ang)
    return F.line(cx, cy, cx + L * math.sin(a), cy - L * math.cos(a), col, w)


def _clock2(i, t, col):
    cx, cy, R = CK2["xs"][i], CK2["y"], CK2["r"]
    g = [F.circ(cx, cy, R, J.BG2, col, 6)]
    for k in range(12):
        a = math.radians(k * 30)
        g.append(F.line(cx + R * 0.80 * math.sin(a), cy - R * 0.80 * math.cos(a), cx + R * 0.92 * math.sin(a), cy - R * 0.92 * math.cos(a),
                        J.TICK, 4 if k % 3 == 0 else 2))
    ha, ma, sa = ck2_angles(t)
    g.append(_hand(cx, cy, ha, R * 0.52, 10, INK))
    g.append(_hand(cx, cy, ma, R * 0.80, 6, INK))
    g.append(_hand(cx, cy, sa, R * 0.86, 2, J.AMBER))
    g.append(F.circ(cx, cy, 9, INK, None))
    g.append(_tline(cx, CK2["ty"], t, 48, J.AMBER, "middle", 340, fam="Dela"))
    g.append(_tline(cx, CK2["sy"], CK2_CAP[i], 28, col if col != DIM else J.TICK, "middle", 420))
    return "".join(g)


def clock2_base(st0):
    return []


def clock2_stage(prev, st):
    s = []
    utc, jst = ck2_times()
    if _on(prev, st, "utc"):
        s.append(_clock2(0, utc, REP))
    if _on(prev, st, "jst"):
        s.append(_arrow(CK2["xs"][0] + CK2["r"] + 30, CK2["y"], CK2["xs"][1] - CK2["r"] - 30, CK2["y"], J.AMBER, 6, 26))
        s.append(_tline(960.0, CK2["y"] - 26, f"＋{CK2_ADD}時間", 40, J.AMBER, "middle", 300))
        s.append(_clock2(1, jst, INK))
    if _on(prev, st, "units"):
        for k, (a, b) in enumerate(CK2_UNITS):
            cx = (620.0, 1300.0)[k]
            s.append(_card(cx, CK2["uy"], 520.0, 70.0, J.LINE))
            s.append(_tline(cx, CK2["uy"] + 10, f"{a} → {b}", 30, INK, "middle", 480))
    return s


# ══════════════════════════════════════════════════════════
#  seats（c205・c210）＝正面から見た操縦席の2つの席（左＝機長・右＝副操縦士＝p17・p42）。人は描かない
# ══════════════════════════════════════════════════════════
ST = dict(xs=(700.0, 1220.0), top=470.0, bot=760.0, w=260.0, ped=(925.0, 995.0, 560.0, 760.0), win=(380.0, 1540.0, 300.0, 420.0),
          name_y=548.0, sub_y=630.0, role_y=690.0, arr_y=520.0)
ST_NAME = ("機長", "副操縦士")
ST_AGE = "42"                     # p17「機長 男性 42歳」
ST_AF = ("1970-09", "1989-01")    # p38「台湾空軍のパイロットとして1970年9月から1989年1月まで勤務」
ST_ROLE = ("見守り・確かめる役", "操縦する役")    # p42「機長(PNF)」「副操縦士(PF)」・p57「副操縦士にPF業務を実施させていた」
ST_ORDER = "20:00"                # p42「00分11秒 機長(PNF)は、副操縦士(PF)に対し、自分で判断して自分で操縦するように指示」（11時00分11秒＝20時00分11秒）


def st_years():
    a, b = (datetime.date(int(s[:4]), int(s[5:]), 1) for s in ST_AF)
    return (b - a).days / 365.25


def seats_base(st0):
    x0, x1, y0, y1 = ST["win"]
    g = []
    n = 4
    for k in range(n):
        a, b = x0 + (x1 - x0) * k / n + 8, x0 + (x1 - x0) * (k + 1) / n - 8
        g.append(F.poly([(a + 18, y0), (b - 18, y0), (b, y1), (a, y1)], "#101a24", J.LINE_DIM, 3, close=True))
    g.append(F.rect(x0 - 40, y1 + 10, x1 - x0 + 80, 40, "#2b3237", J.LINE_DIM, 3, rx=6))
    p0, p1, q0, q1 = ST["ped"]
    g.append(F.rect(p0, q0, p1 - p0, q1 - q0, "#46505a", J.LINE_DIM, 3, rx=6))
    for cx in ST["xs"]:
        w = ST["w"]
        g.append(F.rect(cx - 70, ST["top"] - 40, 140, 64, "#2b3237", J.LINE_DIM, 3, rx=18))
        g.append(F.rect(cx - w / 2, ST["top"], w, ST["bot"] - ST["top"], "#1c262e", J.LINE_DIM, 4, rx=26))
    g.append(F.line(220.0, ST["bot"] + 14, 1700.0, ST["bot"] + 14, J.LINE_DIM, 3))
    return g


def _seat_card(i, t, col):
    cx = ST["xs"][i]
    return _card(cx, ST["name_y"], 230.0, 64.0, col) + _tline(cx, ST["name_y"] + 11, t, 30, INK, "middle", 210)


def seats_stage(prev, st):
    s = []
    if _on(prev, st, "cap"):
        s.append(_seat_card(0, f"{ST_NAME[0]}（{ST_AGE}歳）" if st["age"] == "on" else ST_NAME[0], HAND))
    if _on(prev, st, "fo"):
        s.append(_seat_card(1, ST_NAME[1], HAND))
    if _on(prev, st, "af"):
        s.append(_tline(ST["xs"][0], ST["sub_y"], "前は台湾空軍", 26, J.TICK, "middle", 240))
        s.append(_tline(ST["xs"][0], ST["sub_y"] + 40, f"（約{round(st_years())}年）", 26, J.AMBER, "middle", 240))
    if _on(prev, st, "roles"):
        for i in (0, 1):
            s.append(_tline(ST["xs"][i], ST["role_y"], ST_ROLE[i], 26, HAND, "middle", 240))
    if _on(prev, st, "order"):
        a, b = ST["xs"][0] + 120.0, ST["xs"][1] - 120.0
        s.append(_arrow(a, ST["arr_y"], b, ST["arr_y"], J.AMBER, 6, 22))
        s.append(_tline(960.0, ST["arr_y"] - 22, f"指示（{ST_ORDER}ごろ）", 26, J.AMBER, "middle", 300))
    return s


# ══════════════════════════════════════════════════════════
#  hours（c206）＝機長の飛行時間（p17・p38）。棒の長さ＝時間（同じ縮尺）・数は目盛りだけ（棒に数を書かない＝字幕）
# ══════════════════════════════════════════════════════════
HR_V = (("この型（A300-600R）", 1350 + 27 / 60, "company"), ("空軍のころから全部", 8340 + 19 / 60, "LINE"))
HR = dict(x0=560.0, x1=1660.0, vmax=9000.0, ys=(560.0, 690.0), h=60.0, ty=790.0, cy=380.0)
HR_TICKS = (0, 2000, 4000, 6000, 8000)
HR_CAREER = ("1989年 入社", "747の副操縦士", "1992年12月 この型の機長")    # p38「1989年2月1日、同公司に入社」「B747-200、-400の副操縦士を経て」「同年12月1日に…機長に昇格」


def hr_x(v):
    return HR["x0"] + (HR["x1"] - HR["x0"]) * v / HR["vmax"]


def hours_base(st0):
    g = [F.line(HR["x0"], HR["ys"][0] - 50, HR["x0"], HR["ty"] - 34, J.LINE, 3)]
    for v in HR_TICKS:
        x = hr_x(v)
        g.append(F.line(x, HR["ty"] - 34, x, HR["ty"] - 22, J.TICK, 3))
        g.append(_tline(x, HR["ty"], f"{v:,}", 24, J.TICK, "middle", 120))
    g.append(_tline(HR["x1"] + 30, HR["ty"], "時間", 24, J.TICK, "start", 120))
    for k, (t, _v, _r) in enumerate(HR_V):
        g.append(_tline(HR["x0"] - 24, HR["ys"][k] + 10, t, 28, J.TICK, "end", 440))
    return g


def hours_stage(prev, st):
    s = []
    if _on(prev, st, "career"):
        xs = (420.0, 960.0, 1500.0)
        for k, t in enumerate(HR_CAREER):
            s.append(_card(xs[k], HR["cy"], 440.0, 72.0, J.LINE))
            s.append(_tline(xs[k], HR["cy"] + 10, t, 28, INK, "middle", 410))
            if k:
                s.append(_arrow(xs[k - 1] + 226, HR["cy"], xs[k] - 228, HR["cy"], J.TICK, 4, 16))
    for k, f_ in enumerate(("b0", "b1")):
        if _on(prev, st, f_):
            _t, v, r = HR_V[k]
            y = HR["ys"][k]
            s.append(F.rect(HR["x0"], y - HR["h"] / 2, hr_x(v) - HR["x0"], HR["h"], rc(r), None, op=0.92))
    return s


# ══════════════════════════════════════════════════════════
#  train（c208）＝副操縦士の訓練の順（p38「仏国のアエロフォーメーション社において地上学科、シミュレータによる訓練及び実飛行時間3時間の訓練」）。
#  順だけ＝帯の長さは時間に比例しない（模式）
# ══════════════════════════════════════════════════════════
TR_STEPS = ("地上の学科（教室）", "シミュレーター", "実際の機体")
TR_HOURS = "3"
TR = dict(x0=240.0, x1=1680.0, y=560.0, h=120.0, hy=380.0, gap=24.0)


def tr_seg(k):
    w = (TR["x1"] - TR["x0"] - 2 * TR["gap"]) / 3
    a = TR["x0"] + k * (w + TR["gap"])
    return a, a + w


def _chev(a, b, y, h, col):
    t = 34.0
    return F.poly([(a, y - h / 2), (b - t, y - h / 2), (b, y), (b - t, y + h / 2), (a, y + h / 2), (a + t, y)], J.BG2, col, 5, close=True)


def train_base(st0):
    return []


def train_stage(prev, st):
    s = []
    if _on(prev, st, "head"):
        s.append(_tline(960.0, TR["hy"], "副操縦士の訓練（フランスの訓練会社）", 32, INK, "middle", 1000))
        s.append(_bracket(TR["x0"], TR["x1"], TR["hy"] + 30, J.TICK))
    for k, f_ in ((0, "s1"), (1, "s23"), (2, "s23")):
        if _on(prev, st, f_):
            a, b = tr_seg(k)
            col = AUTO if k == 1 else (HAND if k == 2 else J.LINE)
            s.append(_chev(a, b, TR["y"], TR["h"], col))
            s.append(_tline((a + b) / 2 + 10, TR["y"] + 11, TR_STEPS[k], 30, INK, "middle", b - a - 90))
            if k == 2:
                s.append(_tline((a + b) / 2, TR["y"] + TR["h"] / 2 + 70, f"{TR_HOURS}時間", 44, J.AMBER, "middle", 300, fam="Dela"))
    return s


# ══════════════════════════════════════════════════════════
#  area（c304）＝面積のマス目（p55「THS(エレベータを含む。)の面積は、エレベータの面積のおよそ3倍」）。マス目の数の比＝記録の比・形は模式
# ══════════════════════════════════════════════════════════
AR = dict(cell=64.0, el=(300.0, 470.0), th=(1060.0, 360.0), cols=4, rows=3, py=730.0)
AR_EL_N = 4                        # 昇降舵のマス
AR_TH_N = 12                       # 昇降舵を含めた水平安定板のマス（後ろの1列＝昇降舵）
AR_RATIO = "3"
AR_DEG = 12.0                      # 「同じ角度」の板の傾き（模式＝記録の値ではない）


def ar_cells():
    """(昇降舵のマスの左上の list, 水平安定板のマスの左上と、昇降舵の部分か の list)"""
    c = AR["cell"]
    el = [(AR["el"][0] + k * c, AR["el"][1]) for k in range(AR_EL_N)]
    th = [(AR["th"][0] + i * c, AR["th"][1] + j * c, j == AR["rows"] - 1) for j in range(AR["rows"]) for i in range(AR["cols"])][:AR_TH_N]
    return el, th


def _plate(x, y, L, deg, col):
    a = math.radians(-deg)
    t = 14.0
    pts = [(0, -t / 2), (L, -t / 4), (L, t / 4), (0, t / 2)]
    return F.poly([(x + u * math.cos(a) - v * math.sin(a), y + u * math.sin(a) + v * math.cos(a)) for u, v in pts], col, J.BG, 2, close=True)


def area_base(st0):
    return []


def area_stage(prev, st):
    s = []
    c = AR["cell"]
    el, th = ar_cells()
    if _on(prev, st, "elev"):
        for x, y in el:
            s.append(F.rect(x, y, c, c, "#3a3220", J.AMBER, 3))
        s.append(_tline(AR["el"][0] + c * AR_EL_N / 2, AR["el"][1] - 24, "昇降舵", 30, J.AMBER, "middle", 300))
    if _on(prev, st, "ths"):
        for x, y, is_el in th:
            s.append(F.rect(x, y, c, c, "#3a3220" if is_el else "#22333f", J.AMBER if is_el else INK, 3))
        s.append(_tline(AR["th"][0] + c * AR["cols"] / 2, AR["th"][1] - 24, "水平安定板（昇降舵を含む）", 30, INK, "middle", 560))
        s.append(_tline(800.0, 486.0, f"約{AR_RATIO}倍", 52, J.AMBER, "middle", 260))
        s.append(_tline(800.0, 530.0, "面積", 24, J.TICK, "middle", 200))
    if _on(prev, st, "same"):
        xa, xb = 330.0, 1060.0
        y = AR["py"]
        for x, L in ((xa, 150.0), (xb, 300.0)):
            s.append(F.line(x - 20, y, x + L + 40, y, DIM, 3, dash="8 8"))
            s.append(_plate(x, y, L, AR_DEG, "#c9d1d7"))
            arc = F._arc(x, y, L * 0.7, -AR_DEG, 0.0, 12)
            s.append(F.poly(arc, "none", J.AMBER, 3))
        s.append(_tline(810.0, y - 6, "同じ角度", 28, J.AMBER, "middle", 260))
        # ⚠️ 下見（座標の読み直し）：大きい矢印を y 560 まで伸ばすと上のマス目（下の端 y 552）に触れる＝y 580 まで
        s.append(_arrow(xa + 75, y - 40, xa + 75, y - 85, J.LINE, 5, 16))
        s.append(_arrow(xb + 150, y - 40, xb + 150, y - 150, J.LINE, 8, 24))
        s.append(_tline(xb + 180, y - 100, "効き", 28, J.LINE, "start", 160))
    return s


# ══════════════════════════════════════════════════════════
#  afs（c307）＝自動飛行システム（AFS）の主な中身3つ（略語の頁 p-14＝AP・ATS・FD／p51「FDはGOAROUNDモードになり、ATSはTHRモード」）
# ══════════════════════════════════════════════════════════
AFS3 = (("自動操縦（AP）", "舵を動かす"), ("自動推力（ATS）", "推力を整える"), ("飛行の指示（FD）", "画面の印で示す"))
AF = dict(xs=(420.0, 960.0, 1500.0), y=590.0, w=460.0, h=260.0, hy=360.0)


def _af_icon(k, cx, cy):
    if k == 0:      # 尾の板と回る向き
        return (F.poly([(cx - 70, cy + 10), (cx + 40, cy), (cx + 40, cy + 12), (cx - 70, cy + 22)], "#c9d1d7", J.BG, 2, close=True)
                + F.poly(F._arc(cx + 40, cy + 6, 46, -50, 50, 10), "none", AUTO, 5))
    if k == 1:      # 推力のレバー
        return (F.rect(cx - 60, cy + 20, 120, 18, "#46505a", J.LINE_DIM, 2, rx=4) + F.line(cx, cy + 20, cx + 30, cy - 34, "#99a3ab", 10)
                + F.circ(cx + 32, cy - 38, 14, "#c2cad0", J.BG, 2) + _arrow(cx + 70, cy + 10, cx + 70, cy - 40, AUTO, 5, 16))
    return (F.rect(cx - 70, cy - 40, 140, 90, "#05090d", J.LINE_DIM, 3, rx=6) + F.line(cx - 50, cy + 5, cx + 50, cy + 5, FMA_G, 5)
            + F.line(cx, cy - 30, cx, cy + 40, FMA_G, 5))


def afs_base(st0):
    return []


def afs_stage(prev, st):
    s = []
    if _on(prev, st, "head"):
        s.append(_card(960.0, AF["hy"], 560.0, 70.0, AUTO))
        s.append(_tline(960.0, AF["hy"] + 11, "自動飛行システム（AFS）", 32, AUTO, "middle", 520))
    for k, f_ in ((0, "ap"), (1, "at"), (2, "fd")):
        if _on(prev, st, f_):
            cx, cy = AF["xs"][k], AF["y"]
            s.append(F.line(cx, AF["hy"] + 35, cx, cy - AF["h"] / 2, AUTO, 3, dash="6 6"))
            s.append(_card(cx, cy, AF["w"], AF["h"], AUTO))
            s.append(_af_icon(k, cx, cy - 50))
            t, d = AFS3[k]
            s.append(_tline(cx, cy + 60, t, 32, INK, "middle", AF["w"] - 40))
            s.append(_tline(cx, cy + 104, d, 26, J.TICK, "middle", AF["w"] - 40))
    return s


# ══════════════════════════════════════════════════════════
#  band（c317）＝横から見た進入の道（模式＝傾きは誇張）。改修 MOD.7187 の対象外（p78「LANDTrack(対地高度400ft以下)及びGOAROUNDモード以外の
#  モードでは…15kg以上の力を加えるとAPがディスエンゲージ」）＝対地 約120m（400ft）以下のランドとゴー・アラウンド
# ══════════════════════════════════════════════════════════
BD = dict(g=780.0, a=(200.0, 330.0), td=(1300.0, 780.0), rw=(1250.0, 1700.0), y_low=670.0, ga=((1180.0, 732.0), (1500.0, 560.0), (1790.0, 330.0)))
BD_FT, BD_M = "400", "120"
BD_OUT = ("ランド", "ゴー・アラウンド")


def bd_y(x):
    (x0, y0), (x1, y1) = BD["a"], BD["td"]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def bd_x(y):
    (x0, y0), (x1, y1) = BD["a"], BD["td"]
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)


def band_base(st0):
    g = [F.line(100.0, BD["g"], 1820.0, BD["g"], J.LINE, 4)]
    a, b = BD["rw"]
    g.append(F.rect(a, BD["g"] - 8, b - a, 16, "#8f989e", None))
    g.append(_tline((a + b) / 2, BD["g"] + 42, "滑走路", 24, J.TICK, "middle", 300))
    g.append(F.line(*BD["a"], *BD["td"], J.LINE, 5))
    g.append(_plane(BD["a"][0] + 40, bd_y(BD["a"][0] + 40) - 22, 140.0, -math.degrees(math.atan2(BD["td"][1] - BD["a"][1], BD["td"][0] - BD["a"][0]))))
    # ⚠️ 下見（座標の読み直し）：(560, 640) だと札の右の端が下り道の線（x 900 で y 616）にかかる＝線の下の左へ
    g.append(_tline(240.0, 560.0, "ほかのモード：押すと切れる", 28, J.LINE, "start", 520))
    return g


def band_stage(prev, st):
    s = []
    if _on(prev, st, "land"):
        x = bd_x(BD["y_low"])
        s.append(F.line(100.0, BD["y_low"], 1820.0, BD["y_low"], J.TICK, 3, dash="10 10"))
        s.append(_tline(110.0, BD["y_low"] - 14, f"対地 約{BD_M}m（{BD_FT}ft）", 26, J.TICK, "start", 360))
        s.append(F.line(x, BD["y_low"], *BD["td"], J.AMBER, 12))
        s.append(F.line(x - 40, 760.0, x - 6, 712.0, J.AMBER, 2))
        s.append(_tline(x - 50, 770.0, f"{BD_OUT[0]}（約{BD_M}m以下）", 28, J.AMBER, "end", 420))
        s.append(_tline(x - 50, 808.0, "対象外", 28, J.ALERT, "end", 200))
    if _on(prev, st, "ga"):
        p = BD["ga"]
        s.append(F.poly([p[0], p[1], p[2]], "none", J.AMBER, 10, dash="22 12"))
        s.append(_arrow(p[1][0] + (p[2][0] - p[1][0]) * 0.9, p[1][1] + (p[2][1] - p[1][1]) * 0.9, p[2][0], p[2][1], J.AMBER, 10, 30))
        s.append(_tline(1520.0, 420.0, BD_OUT[1], 30, J.AMBER, "end", 420))
        s.append(_tline(1520.0, 460.0, "（やり直しの上昇）", 24, J.AMBER, "end", 420))
        s.append(_tline(1520.0, 500.0, "対象外", 28, J.ALERT, "end", 200))
    return s


# ══════════════════════════════════════════════════════════
#  modes（c321・c516）＝ゴー・アラウンドの抜け方（p54「ラテラル及びロンジチュヂィナルの双方にそれぞれLANDモード以外のモードを選択しなければならず、
#  直接LANDモードのボタンを押すことによって解除することはできない」・p81「…V/Sモードを選択すると…GOAROUNDの表示が消え…実際にはGOAROUNDの機能が
#  完全にディスエンゲージされたことにはならない」）
# ══════════════════════════════════════════════════════════
MD = dict(sx=320.0, sy=580.0, sw=340.0, sh=120.0, mx=860.0, mw=420.0, rx=1440.0, rw=380.0, ya=400.0, yb=580.0, yc=760.0, h=88.0)
MD_ROWS = dict(a=("縦と横の両方で選び直す", (("抜ける", "OK"),)),
               b=("縦だけ選び直す", (("画面の文字は消える", "AMBER"), ("働きは残る", "ALERT"))),
               c=("ランドのボタンを押す", (("抜けられない", "ALERT"),)))
MD_START = "ゴー・アラウンド・モード"


def _md_row(key, dim=False, results=True, upto=None):
    t, res = MD_ROWS[key]
    y = MD[f"y{key}"]
    col = DIM if dim else (HAND if key == "c" else J.LINE)
    ink = J.TICK if dim else INK
    g = [_arrow(MD["sx"] + MD["sw"] / 2, MD["sy"] + (y - MD["sy"]) * 0.3, MD["mx"] - MD["mw"] / 2 - 8, y, DIM if dim else J.LINE, 4, 18)]
    g.append(_box(MD["mx"], y, MD["mw"], MD["h"], t, col, ink, 28))
    if results:
        n = len(res) if upto is None else upto
        for j, (rt, rcol) in enumerate(res[:n]):
            ry = y if len(res) == 1 else y + (j - 0.5) * 96
            c = DIM if dim else rc(rcol)
            g.append(_arrow(MD["mx"] + MD["mw"] / 2 + 6, y, MD["rx"] - MD["rw"] / 2 - 8, ry, DIM if dim else J.LINE, 4, 18))
            g.append(_box(MD["rx"], ry, MD["rw"], 80.0, rt, c, ink if dim else c, 28))
            if not dim and rcol == "OK":
                g.append(_check(MD["rx"] + MD["rw"] / 2 + 46, ry, 22, J.OK))
            if not dim and rcol == "ALERT" and key == "c":
                g.append(_xmark(MD["rx"] + MD["rw"] / 2 + 46, ry, 22))
    return "".join(g)


def modes_base(st0):
    g = [_box(MD["sx"], MD["sy"], MD["sw"], MD["sh"], MD_START, AUTO, INK, 28)]
    if st0["dim"] == "on":
        g.append(_md_row("a", dim=True))
        g.append(_md_row("b", dim=True))
    return g


def modes_stage(prev, st):
    s = []
    if _on(prev, st, "a") and st["dim"] != "on":
        s.append(_md_row("a"))
    if _on(prev, st, "b") and st["dim"] != "on":
        s.append(_md_row("b", upto=1))
    if _on(prev, st, "b2") and st["dim"] != "on":
        _t, res = MD_ROWS["b"]
        y = MD["yb"]
        ry = y + 0.5 * 96
        s.append(_arrow(MD["mx"] + MD["mw"] / 2 + 6, y, MD["rx"] - MD["rw"] / 2 - 8, ry, J.LINE, 4, 18))
        s.append(_box(MD["rx"], ry, MD["rw"], 80.0, res[1][0], J.ALERT, J.ALERT, 28))
    if _on(prev, st, "c"):
        s.append(_md_row("c", results=False))
    if _on(prev, st, "cx"):
        t, res = MD_ROWS["c"]
        y = MD["yc"]
        s.append(_arrow(MD["mx"] + MD["mw"] / 2 + 6, y, MD["rx"] - MD["rw"] / 2 - 8, y, J.LINE, 4, 18))
        s.append(_box(MD["rx"], y, MD["rw"], 80.0, res[0][0], J.ALERT, J.ALERT, 28))
        s.append(_xmark(MD["rx"] + MD["rw"] / 2 + 46, y, 22))
    if _on(prev, st, "stay"):
        s.append(F.rect(MD["sx"] - MD["sw"] / 2 - 10, MD["sy"] - MD["sh"] / 2 - 10, MD["sw"] + 20, MD["sh"] + 20, "none", J.AMBER, 6, rx=14))
        s.append(_tline(MD["sx"], MD["sy"] - MD["sh"] / 2 - 34, "モードはそのまま", 28, J.AMBER, "middle", 340))
    return s


# ══════════════════════════════════════════════════════════
#  fcom（c322）＝表示（FMA）と操縦の手引き書（FCOM 1.03.67 P-8 REV17＝p81）。手引き書の欄の言葉は報告書の要約（p81 の「次の趣旨の内容」）・
#  書かれていない所（p82）・勧告（p103 の 2c「FMA上の表示の変更と実質的機能の変更の対比」）
# ══════════════════════════════════════════════════════════
FC_FMA = ("V/S", "HDG")           # p81「FMAに表示されたコモン・モードであるGOAROUNDの表示が消え、V/SとラテラルのモードであるHDGが表示」
FC_ROWS = ("縦のモードを選ぶ → 解ける", "横のモードを選ぶ → 解ける")
FC_MISS = "縦だけでは働きが残る"
FC_REC = ("勧告（報告書）", "表示の変化と働きの変化の対比")
FC = dict(fma=(200.0, 380.0, 560.0, 90.0), doc=(980.0, 320.0, 740.0, 500.0), rec=(200.0, 650.0, 640.0, 140.0))


def fcom_base(st0):
    x, y, w, h = FC["doc"]
    g = [F.rect(x, y, w, h, "#1b1812", J.DOC, 4, rx=8)]
    g.append(F.rect(x, y, w, 64, "#2a2418", J.DOC, 4, rx=8))
    g.append(_tline(x + w / 2, y + 44, "操縦の手引き書（FCOM）", 30, J.DOC, "middle", w - 40))
    g.append(_tline(x + 30, y + 120, "ゴー・アラウンドを解く手順", 28, INK, "start", w - 60))
    for k, t in enumerate(FC_ROWS):
        yy = y + 190 + k * 80
        g.append(F.rect(x + 30, yy - 36, w - 60, 56, "#221e16", J.DOC_DIM, 3, rx=6))
        g.append(_tline(x + 50, yy + 2, t, 26, INK, "start", w - 100))
    # ⚠️ 下見（座標の読み直し）：y+360 からだと灰の行が「書かれていない」の破線の枠（y 724〜）に重なる＝上へ
    for k in range(3):
        g.append(F.line(x + 30, y + 300 + k * 20, x + w - 30 - (k % 2) * 160, y + 300 + k * 20, J.DOC_DIM, 6))
    return g


def fcom_stage(prev, st):
    s = []
    if _on(prev, st, "fma"):
        x, y, w, h = FC["fma"]
        s.append(F.rect(x, y, w, h, "#05090d", J.LINE_DIM, 4, rx=6))
        n = 3
        for k in range(1, n):
            s.append(F.line(x + w * k / n, y + 10, x + w * k / n, y + h - 10, J.LINE_DIM, 2))
        for k, t in enumerate(FC_FMA):
            s.append(_tline(x + w * (k + 0.5) / n, y + h / 2 + 14, t, 36, FMA_G, "middle", w / n - 20))
        s.append(_tline(x + w / 2, y - 18, "表示（FMA）", 24, J.TICK, "middle", w))
        s.append(_tline(x + w / 2, y + h + 56, "「あたかも」", 40, J.AMBER, "middle", w))
        s.append(_tline(x + w / 2, y + h + 98, "解除されたように見える", 26, J.AMBER, "middle", w))
    if _on(prev, st, "gap"):
        x, y, w, h = FC["doc"]
        yy = y + 190 + 2 * 80
        s.append(F.rect(x + 30, yy - 36 + 90, w - 60, 64, "none", J.ALERT, 4, rx=6, dash="12 8"))
        s.append(_tline(x + 50, yy + 96, FC_MISS, 26, J.ALERT, "start", w - 300))
        s.append(_tline(x + w - 50, yy + 96, "書かれていない", 26, J.ALERT, "end", 240))
    if _on(prev, st, "rec"):
        x, y, w, h = FC["rec"]
        s.append(F.rect(x, y, w, h, J.BG2, REP, 5, rx=10))
        s.append(_tline(x + 24, y + 46, FC_REC[0], 28, REP, "start", w - 40))
        s.append(_tline(x + 24, y + 100, FC_REC[1], 28, INK, "start", w - 40))
    return s


# ══════════════════════════════════════════════════════════
#  who3（c504）＝自動操縦を入れた人の3つの可能性（p52〜53・p89(4)）。並べるだけ（どれも同じ形・同じ色＝どれかを目立たせない）
# ══════════════════════════════════════════════════════════
WHO3 = (("機長が", "自分で"), ("副操縦士が", "機長の指示で"), ("副操縦士が", "断りなく"))
WH = dict(xs=(420.0, 960.0, 1500.0), y=570.0, w=460.0, h=160.0, hy=370.0, by=690.0)


def who3_base(st0):
    return [_tline(960.0, WH["hy"], "自動操縦を入れた人", 34, INK, "middle", 800)]


def who3_stage(prev, st):
    s = []
    for k, f_ in ((0, "c01"), (1, "c01"), (2, "c2")):
        if _on(prev, st, f_):
            a, b = WHO3[k]
            s.append(_box(WH["xs"][k], WH["y"], WH["w"], WH["h"], a, J.LINE, INK, 32, t2=b))
    if _on(prev, st, "br"):
        xa, xb = WH["xs"][0] - WH["w"] / 2, WH["xs"][2] + WH["w"] / 2
        s.append(_bracket(xa, xb, WH["by"] + 20, J.TICK, down=False))
        s.append(_tline(960.0, WH["by"] + 70, "報告書が並べた可能性", 28, REP, "middle", 600))
    return s


# ══════════════════════════════════════════════════════════
#  ths（c517・c603）＝水平安定板の角度の帯（横＝時刻 20:14:00〜20:15:20・縦＝角度〈上ほど機首上げ＝マイナスが大きい〉）。
#  点＝付図5 の表と本文の値（時刻は20時14分＋秒）・点のあいだは直線（模式）
# ══════════════════════════════════════════════════════════
TH_PTS = ((5, -5.3), (18, -5.3), (25, -6.7), (31, -9.5), (37, -12.3), (49, -12.3), (57, -12.3), (71, -12.3))
TH = dict(x0=320.0, x1=1720.0, t1=80.0, y0=760.0, k=36.0, amin=-13.0)
TH_TICKS = (0, 20, 40, 60, 80)
TH_GRID = (0, -4, -8, -12)
TH_LINE = dict(none=0, t25=25, t49=49)
TH_DESC = 26                       # p55「同26秒ごろから降下に移っている」
TH_OFF = 49                        # p56「11時14分49秒…APはディスエンゲージされたがTHSは-12.3°のまま」


def th_x(t):
    return TH["x0"] + (TH["x1"] - TH["x0"]) * t / TH["t1"]


def th_y(a):
    return TH["y0"] + a * TH["k"]


def th_clock(t):
    m, s = divmod(14 * 60 + int(t), 60)
    return f"20:{m:02d}:{s:02d}"


def _th_seg_col(t0):
    return INK if t0 < 18 else (AUTO if t0 < TH_OFF else J.ALERT)


def _th_line(upto, t_from=0, width=6, dim=False):
    g = []
    pts = [p for p in TH_PTS if t_from <= p[0] <= upto]
    for (t0, a0), (t1, a1) in zip(pts, pts[1:]):
        g.append(F.line(th_x(t0), th_y(a0), th_x(t1), th_y(a1), DIM if dim else _th_seg_col(t0), width))
    for t, a in pts:
        g.append(F.circ(th_x(t), th_y(a), 8, DIM if dim else J.AMBER, J.BG, 3))
    return "".join(g)


def ths_base(st0):
    g = [F.line(TH["x0"], th_y(TH["amin"]) - 10, TH["x0"], TH["y0"] + 10, J.LINE, 3),
         F.line(TH["x0"], TH["y0"] + 10, TH["x1"] + 20, TH["y0"] + 10, J.LINE, 3)]
    for a in TH_GRID:
        y = th_y(a)
        if a:
            g.append(F.line(TH["x0"], y, TH["x1"], y, J.GRID, 2, dash="8 10"))
        g.append(_tline(TH["x0"] - 14, y + 9, ("0度" if a == 0 else f"−{-a}"), 24, J.TICK, "end", 100))
    for t in TH_TICKS:
        x = th_x(t)
        g.append(F.line(x, TH["y0"] + 10, x, TH["y0"] + 22, J.TICK, 3))
        g.append(_tline(x, TH["y0"] + 50, th_clock(t), 24, J.TICK, "middle", 160))
    g.append(_tline(TH["x0"] + 12, th_y(TH["amin"]) - 2, "角度（上ほど機首上げ）", 24, J.TICK, "start", 520))
    up = TH_LINE[st0["line"]]
    if up:
        g.append(_th_line(up))
    return g


def ths_stage(prev, st):
    s = []
    if st["line"] != prev.get("line"):
        a = TH_LINE[prev.get("line", "none")]
        b = TH_LINE[st["line"]]
        if b > a:
            s.append(_th_line(b, t_from=max(0, [t for t, _a in TH_PTS if t <= a][-1] if a else 0)))
    if _on(prev, st, "lab53"):
        t, a = TH_PTS[0]
        s.append(_tline(th_x(t) - 6, th_y(a) - 26, "−5.3度", 34, J.AMBER, "start", 200, fam="Dela"))
        s.append(_tline(th_x(t) + 170, th_y(a) - 28, "ゴー・レバーの前", 24, J.AMBER, "start", 260))
    if _on(prev, st, "desc"):
        x = th_x(TH_DESC)
        s.append(F.line(x, th_y(TH["amin"]) + 40, x, TH["y0"], J.LINE, 3, dash="10 8"))
        s.append(_tline(x + 12, th_y(-10.5), "機体が下り始める", 26, J.LINE, "start", 300))
        s.append(_tline(x + 12, th_y(-10.5) + 36, f"（{th_clock(TH_DESC)}ごろ）", 24, J.LINE, "start", 300))
    if _on(prev, st, "flat"):
        t0, t1 = TH_OFF, TH_PTS[-1][0]
        s.append(F.line(th_x(t0), th_y(-12.3), th_x(t1), th_y(-12.3), J.ALERT, 12))
        for t in (t0, TH_PTS[-2][0], t1):
            s.append(F.circ(th_x(t), th_y(-12.3), 8, J.AMBER, J.BG, 3))
        s.append(F.line(th_x(t0), th_y(-12.3) + 14, th_x(t0), TH["y0"], J.TICK, 3, dash="6 8"))
        s.append(_tline(th_x(t0) + 10, th_y(-8.6), "自動操縦を切った", 26, J.TICK, "start", 300))
        s.append(_tline(th_x(t0) + 10, th_y(-8.6) + 34, f"（{th_clock(t0)}）", 24, J.TICK, "start", 300))
        s.append(_tline((th_x(t0) + th_x(t1)) / 2, th_y(-12.3) - 22, "−12.3度のまま", 30, J.ALERT, "middle", 380))
        s.append(_tline(th_x(t1) + 14, th_y(-12.3) + 10, th_clock(t1), 24, J.AMBER, "start", 160))
    if _on(prev, st, "oot"):
        cx, cy = (th_x(TH_OFF) + th_x(TH_PTS[-1][0])) / 2 + 40, th_y(-4.6)
        s.append(_card(cx, cy, 420.0, 76.0, J.ALERT))
        s.append(_tline(cx, cy + 11, "アウト・オブ・トリム", 30, J.ALERT, "middle", 380))
    return s


# ══════════════════════════════════════════════════════════
#  warn（c612・c615）＝警報音（THS モーション・ウォーニング＝ウーラー音）の設計（p84「A300-600型機開発時においては…手動、自動操縦共THSが作動した時には
#  ウーラー音が鳴るように設計」「その後、自動操縦時においては当該ウーラー音は鳴らないように設計変更」・p85 報告書の見方）
# ══════════════════════════════════════════════════════════
WN_IN = (("手の操縦", "company"), ("自動操縦", "ship"))
WN_OPTS = ("警報音を残す", "別の仕組みで知らせる")
WN_WHY = "押し続けるとアウト・オブ・トリムになる作り"
# ⚠️ 下見（座標の読み直し）：「〜のとき」の札を x 1180 に置くと × が右の報告書の見方の札（x 1370〜）に入る＝左へ
WN = dict(hx=260.0, ay=(450.0, 650.0), bw=300.0, bh=96.0, tx=700.0, ty=550.0, tw=320.0, th=110.0, sx=1010.0, sy=550.0, cx=1120.0,
          px=1580.0, pw=420.0)


def warn_base(st0):
    return []


def warn_stage(prev, st):
    s = []
    if _on(prev, st, "dev"):
        s.append(_tline(F.BX0 + 40, 330.0, "開発のときの設計", 30, J.TICK, "start", 600))
        for k, (t, r) in enumerate(WN_IN):
            y = WN["ay"][k]
            s.append(_box(WN["hx"], y, WN["bw"], WN["bh"], t, rc(r), INK, 30))
            s.append(_arrow(WN["hx"] + WN["bw"] / 2 + 6, y, WN["tx"] - WN["tw"] / 2 - 8, WN["ty"] + (y - WN["ty"]) * 0.3, rc(r), 5, 20))
        s.append(_box(WN["tx"], WN["ty"], WN["tw"], WN["th"], "水平安定板が動く", J.LINE, INK, 28))
    if _on(prev, st, "ring"):
        s.append(_arrow(WN["tx"] + WN["tw"] / 2 + 6, WN["ty"], WN["sx"] - 48, WN["sy"], J.LINE, 5, 20))
        s.append(_speaker(WN["sx"], WN["sy"], 34.0))
        s.append(_waves(WN["sx"] + 10, WN["sy"], 3, 40))
        s.append(_tline(WN["sx"] + 20, WN["sy"] + 110, "警報音が鳴る", 28, J.AMBER, "middle", 300))
        for k, (t, r) in enumerate(WN_IN):
            y = WN["sy"] - 60 + k * 120
            s.append(_tline(WN["cx"], y, f"{t}のとき", 24, rc(r), "start", 200))
    if _on(prev, st, "cut"):
        y = WN["sy"] + 60
        s.append(_xmark(WN["cx"] + 190, y - 9, 18))
        s.append(_tline(WN["cx"], y + 40, "変更後：鳴らない", 24, J.ALERT, "start", 240))
    if _on(prev, st, "why"):
        x = WN["px"]
        s.append(F.rect(x - WN["pw"] / 2, 330.0, WN["pw"], 170.0, J.BG2, REP, 5, rx=10))
        s.append(_tline(x, 376.0, "報告書の見方", 28, REP, "middle", WN["pw"] - 40))
        s.append(_tline(x, 426.0, "押し続けると", 26, INK, "middle", WN["pw"] - 40))
        s.append(_tline(x, 466.0, "アウト・オブ・トリムになる作り", 26, INK, "middle", WN["pw"] - 30))
    if _on(prev, st, "opts"):
        x = WN["px"]
        for k, t in enumerate(WN_OPTS):
            y = (590.0, 750.0)[k]
            s.append(_box(x, y, WN["pw"], 84.0, t, REP, INK, 28))
        s.append(_tline(x, 680.0, "または", 26, J.TICK, "middle", 200))
    return s


# ══════════════════════════════════════════════════════════
#  eu（c613）＝上から見たイギリスとフランス（陸＝Natural Earth 1:50m・国境なし＝`ref/ep17/coast_eu_ne50m.json`）。
#  イギリスの航空の当局 → エアバス社（p84「英国CAAは同型式機の評価時に…エアバス社に対して要求した」）。トゥールーズは一般の座標（報告書に地名は無い）
# ══════════════════════════════════════════════════════════
COAST_EU = HERE / "ref" / "ep17" / "coast_eu_ne50m.json"
EU_VIEW = dict(lon=(-11.0, 9.0), lat=(42.0, 59.0))
EU_BOX = (740.0, 290.0, 440.0, 550.0)
EU_PTS = dict(gb=(53.0, -1.6), tls=(43.6047, 1.4442))          # gb＝グレートブリテン島の真ん中あたり（模式）・tls＝トゥールーズ（一般の座標）
EU_GB = (-6.5, 2.0, 49.8, 59.0)                                # グレートブリテン島を選ぶ範囲（経度・緯度）
EU_REQ = ("自動着陸の最後の場面", "警報を減らす")


class Geo:
    def __init__(self):
        v = EU_VIEW
        self.latc, self.lonc = (v["lat"][0] + v["lat"][1]) / 2, (v["lon"][0] + v["lon"][1]) / 2
        self.kx = 111.32 * math.cos(math.radians(self.latc))
        self.ky = 110.57
        x0, y0, w, h = EU_BOX
        self.s = min(w / ((v["lon"][1] - v["lon"][0]) * self.kx), h / ((v["lat"][1] - v["lat"][0]) * self.ky))
        self.cx, self.cy = x0 + w / 2, y0 + h / 2

    def px(self, lat, lon):
        return (self.cx + (lon - self.lonc) * self.kx * self.s, self.cy - (lat - self.latc) * self.ky * self.s)


_COAST = []


def coast_eu():
    if not _COAST:
        _COAST.extend(json.loads(COAST_EU.read_text(encoding="utf-8"))["polys"])
    return _COAST


def eu_gb_poly():
    """グレートブリテン島の多角形（範囲の中に点の多い最大の輪）。"""
    a, b, c, d = EU_GB
    best = None
    for p in coast_eu():
        lo = sum(x for x, _y in p) / len(p)
        la = sum(y for _x, y in p) / len(p)
        if a <= lo <= b and c <= la <= d and (best is None or len(p) > len(best)):
            best = p
    return best


def _eu_clip(G, p):
    x0, y0, w, h = EU_BOX
    return [(min(max(x, x0), x0 + w), min(max(y, y0), y0 + h)) for x, y in (G.px(la, lo) for lo, la in p)]


def eu_base(st0):
    G = Geo()
    x0, y0, w, h = EU_BOX
    g = [F.rect(x0, y0, w, h, J.BG, J.LINE_DIM, 3)]
    for p in coast_eu():
        q = [G.px(la, lo) for lo, la in p]
        if max(x for x, _ in q) < x0 or min(x for x, _ in q) > x0 + w or max(y for _, y in q) < y0 or min(y for _, y in q) > y0 + h:
            continue
        g.append(F.poly(_eu_clip(G, p), "#22333f", "#41606f", 2, close=True))
    # ⚠️ 下見（座標の読み直し）：枠の下（y 868）は出典の行（y 866〜884）＝枠の左下の外へ
    g.append(_tline(x0 - 20, y0 + h - 10, "陸の形（国境なし）", 22, J.TICK, "end", 300))
    return g


def eu_stage(prev, st):
    G = Geo()
    s = []
    if _on(prev, st, "src"):
        s.append(F.poly(_eu_clip(G, eu_gb_poly()), "#2b3a46", J.LINE, 4, close=True))
        s.append(_tline(F.BX0 + 50, 340.0, "出どころ：英国の事故調査当局", 26, J.TICK, "start", 600))
    if _on(prev, st, "req"):
        gx, gy = G.px(*EU_PTS["gb"])
        tx, ty = G.px(*EU_PTS["tls"])
        s.append(F.circ(gx, gy, 9, J.LINE, J.BG, 3))
        s.append(F.line(gx - 12, gy, 640.0, 470.0, J.LINE, 2))
        s.append(_tline(630.0, 462.0, "イギリスの航空の当局", 30, J.LINE, "end", 520))
        s.append(_arrow(gx + 6, gy + 14, tx - 6, ty - 16, J.AMBER, 6, 24))
        s.append(F.circ(tx, ty, 11, AB, J.BG, 3))
        s.append(F.line(tx + 14, ty, 1250.0, ty, AB, 2))
        s.append(_tline(1262.0, ty + 10, "エアバス社（トゥールーズ）", 30, AB, "start", 560))
        s.append(_tline((gx + tx) / 2 + 26, (gy + ty) / 2, "求めた", 26, J.AMBER, "start", 200, ol=6))
    if _on(prev, st, "what"):
        x, y = 1500.0, 410.0
        s.append(F.rect(x - 280, y - 70, 560, 150, J.BG2, J.AMBER, 4, rx=10))
        s.append(_tline(x, y - 18, EU_REQ[0], 28, INK, "middle", 520))
        s.append(_tline(x, y + 34, EU_REQ[1], 30, J.AMBER, "middle", 520))
    return s


# ══════════════════════════════════════════════════════════
#  cards3（c616）＝機長の考えの3つの可能性（p57 (10)）。札は番号と「？」だけ（中身は c617〜c619 の語り＝次のカットの語りを先に書かない）
# ══════════════════════════════════════════════════════════
CD3_N = 3
CD3 = dict(xs=(500.0, 960.0, 1420.0), y=600.0, w=380.0, h=260.0, hy=370.0)


def cards3_base(st0):
    return []


def cards3_stage(prev, st):
    s = []
    if _on(prev, st, "q"):
        s.append(_tline(960.0, CD3["hy"], "可能性は3つ", 34, INK, "middle", 600))
    if _on(prev, st, "cards"):
        for k in range(CD3_N):
            cx = CD3["xs"][k]
            s.append(_card(cx, CD3["y"], CD3["w"], CD3["h"], J.LINE))
            s.append(_tline(cx, CD3["y"] - 20, str(k + 1), 72, J.AMBER, "middle", 200, fam="Dela"))
            s.append(_qmark(cx, CD3["y"] + 70, 56, J.TICK))
    return s


# ══════════════════════════════════════════════════════════
#  assist（c619）＝もう1つの押し方（p57「グライド・スロープやローカライザー又はVORコースをキャプチャーする際に、操縦士が操縦輪に力を加えて、APを
#  アシストすることができるスーパーバイザリー・オーバーライドと呼ばれる機能」・p90「スーパーバイザリー・オーバーライド機能との混同」）。形と向きは模式
# ══════════════════════════════════════════════════════════
AS = dict(l=(140.0, 920.0), r=(1000.0, 1780.0), y0=310.0, y1=820.0)
AS_VEC = dict(l=((0, 1), (0, 1)), r=((0, -1), (0, 1)))     # （自動操縦の向き, 操縦士が押す向き）＝画面の向き（下＝機首下げ）
AS_NAME = "スーパーバイザリー・オーバーライド"


def _as_panel(side, title, cap, capcol):
    a, b = AS[side]
    cx = (a + b) / 2
    g = [F.rect(a, AS["y0"], b - a, AS["y1"] - AS["y0"], "none", J.LINE_DIM, 3, rx=10)]
    g.append(_tline(cx, AS["y0"] + 46, title, 28, INK, "middle", b - a - 40))
    # ⚠️ 下見（座標の読み直し）：機の形を y 500・矢印 110 にすると、右の上向きの「自動操縦」の札が見出し（y 356）に重なる＝機を下げ矢印を短く
    if side == "l":
        g.append(F.line(a + 40, 520.0, b - 40, 740.0, J.TICK, 4, dash="14 10"))
        g.append(_tline(b - 50, 700.0, "電波の道", 24, J.TICK, "end", 300))
    px, py = cx - 60, 560.0
    g.append(_plane(px, py, 200.0, 0.0))
    (ax, ay), (hx, hy) = AS_VEC[side]
    L = 90.0
    g.append(_arrow(px + 120, py + ay * 30, px + 120 + ax * L, py + ay * (30 + L), AUTO, 8, 24))
    g.append(_tline(px + 150, py + ay * (30 + L) + (10 if ay > 0 else -4), "自動操縦", 24, AUTO, "start", 160))
    g.append(_arrow(px - 60, py + hy * 30, px - 60 + hx * L, py + hy * (30 + L), HAND, 8, 24))
    g.append(_tline(px - 90, py + hy * (30 + L) + 10, "操縦士が押す", 24, HAND, "end", 200))
    g.append(_tline(cx, AS["y1"] - 30, cap, 26, capcol, "middle", b - a - 40))
    return "".join(g)


def assist_base(st0):
    return []


def assist_stage(prev, st):
    s = []
    if _on(prev, st, "l"):
        s.append(_as_panel("l", "電波の道を捕まえるとき", "同じ向き＝手伝える", J.OK))
    if _on(prev, st, "name"):
        a, b = AS["l"]
        s.append(_tline((a + b) / 2, AS["y1"] - 70, AS_NAME, 24, J.TICK, "middle", b - a - 40))
    if _on(prev, st, "r"):
        s.append(_as_panel("r", "この夜（ゴー・アラウンドのまま）", "逆の向き", J.ALERT))
        a, b = AS["r"]
        s.append(_qmark(b - 90, 420.0, 72))
        s.append(_tline(b - 90, 480.0, "取り違え？", 26, J.AMBER, "middle", 220))
    return s


# ══════════════════════════════════════════════════════════
#  afloor（c704）＝アルファ・フロア（p83「AOAが…検知角11.5°を越えたため、アルファ・フロア機能が作動し出力が増加」「本来失速を防止しフライト・エンベロープを
#  保護するための安全装置」）。形は模式
# ══════════════════════════════════════════════════════════
AFL_STEPS = ("迎え角が大きすぎる", "推力を自動で最大に", "失速を防ぐ")
AFL = dict(xs=(380.0, 960.0, 1540.0), y=600.0, w=440.0, h=260.0, hy=370.0)


def _afl_icon(k, cx, cy):
    if k == 0:
        g = [_plane(cx + 20, cy + 10, 180.0, 22.0)]
        g.append(_arrow(cx - 150, cy + 40, cx - 60, cy + 40, J.TICK, 4, 14))
        g.append(_arrow(cx - 150, cy + 70, cx - 60, cy + 70, J.TICK, 4, 14))
        g.append(F.poly(F._arc(cx - 70, cy + 34, 80, -22, 0, 8), "none", J.AMBER, 4))
        return "".join(g)
    if k == 1:
        return (F.rect(cx - 90, cy - 20, 120, 60, "#9aa4ac", J.BG, 2, rx=24) + _arrow(cx + 40, cy + 10, cx + 150, cy + 10, AUTO, 12, 32))
    return (F.poly([(cx, cy - 60), (cx + 56, cy - 36), (cx + 46, cy + 30), (cx, cy + 62), (cx - 46, cy + 30), (cx - 56, cy - 36)], J.BG2, J.OK, 6,
                   close=True) + _check(cx, cy, 22, J.OK))


def afloor_base(st0):
    return []


def afloor_stage(prev, st):
    s = []
    if _on(prev, st, "name"):
        s.append(_card(960.0, AFL["hy"], 420.0, 70.0, AUTO))
        s.append(_tline(960.0, AFL["hy"] + 11, "アルファ・フロア", 34, AUTO, "middle", 380))
    if _on(prev, st, "flow"):
        for k, t in enumerate(AFL_STEPS):
            cx = AFL["xs"][k]
            col = AUTO if k == 1 else (J.AMBER if k == 0 else J.OK)
            s.append(_card(cx, AFL["y"], AFL["w"], AFL["h"], col))
            s.append(_afl_icon(k, cx, AFL["y"] - 40))
            s.append(_tline(cx, AFL["y"] + 90, t, 30, INK, "middle", AFL["w"] - 40))
            if k:
                s.append(_arrow(AFL["xs"][k - 1] + AFL["w"] / 2 + 8, AFL["y"], cx - AFL["w"] / 2 - 10, AFL["y"], J.LINE, 5, 20))
    if _on(prev, st, "safe"):
        s.append(_tline(960.0, 790.0, "機体を守る安全装置", 30, AUTO, "middle", 600))
    return s


# ══════════════════════════════════════════════════════════
#  pitch（c719）＝分度器（p49「15分26秒 同機のピッチ角は、最大の52.6°となっている」）。針と機の形が段の鍵で回る（動く部品）・機の形は模式
# ══════════════════════════════════════════════════════════
PT_DEG = 52.6
PT = dict(cx=640.0, cy=780.0, r=430.0)
PT_LAB = (1180.0, 470.0)


def _pt_xy(deg, r):
    a = math.radians(deg)
    return PT["cx"] + r * math.cos(a), PT["cy"] - r * math.sin(a)


def pitch_base(st0):
    g = [F.line(PT["cx"] - 80, PT["cy"], PT["cx"] + PT["r"] + 80, PT["cy"], J.LINE, 3)]
    # ⚠️ 下見（座標の読み直し）：右の端に置くと目盛りの「0」（x 1110）と並んで読める＝左の端へ
    g.append(_tline(PT["cx"] - 90, PT["cy"] + 9, "水平", 24, J.TICK, "end", 120))
    arc = [_pt_xy(d, PT["r"]) for d in range(0, 91, 3)]
    g.append(F.poly(arc, "none", J.LINE, 4))
    for d in range(0, 91, 10):
        x0, y0 = _pt_xy(d, PT["r"])
        x1, y1 = _pt_xy(d, PT["r"] - (34 if d % 30 == 0 else 18))
        g.append(F.line(x0, y0, x1, y1, J.TICK, 4 if d % 30 == 0 else 2))
        if d % 30 == 0:
            lx, ly = _pt_xy(d, PT["r"] + 40)
            g.append(_tline(lx, ly + 9, f"{d}度" if d == 90 else str(d), 24, J.TICK, "middle", 100))
    return g


def pitch_parts(st):
    on = st["needle"] == "on"
    rot = -PT_DEG if on else 0.0
    cx, cy = PT["cx"], PT["cy"]
    L = PT["r"] - 40
    needle = _P("needle", "poly", [(cx, cy - 4), (cx + L, cy - 2), (cx + L, cy + 2), (cx, cy + 4)], pivot=[cx, cy], rot=rot,
                fill=J.AMBER, stroke=J.AMBER, w=3, alpha=1.0 if st["dial"] == "on" else 0.0)
    h = 14.0
    body = [(cx - 40, cy - h), (cx + 150, cy - h), (cx + 180, cy), (cx + 150, cy + h), (cx - 30, cy + h), (cx - 60, cy - 2 * h), (cx - 40, cy - 2 * h)]
    plane = _P("plane", "poly", body, pivot=[cx, cy], rot=rot, fill="#c9d1d7", stroke="#20282e", w=3, alpha=1.0 if st["dial"] == "on" else 0.0)
    return [plane, needle]


def pitch_stage(prev, st):
    s = []
    if _on(prev, st, "needle"):
        wedge = [(PT["cx"], PT["cy"])] + [_pt_xy(PT_DEG * i / 20, PT["r"] - 50) for i in range(21)]
        s.append(F.poly(wedge, J.AMBER, None, close=True, op=0.18))
        s.append(_tline(PT_LAB[0], PT_LAB[1], f"{PT_DEG}度", 80, J.AMBER, "start", 420, fam="Dela"))
        s.append(_tline(PT_LAB[0], PT_LAB[1] + 56, "機首の角度（最大）", 28, J.AMBER, "start", 420))
    return s


# ══════════════════════════════════════════════════════════
#  pbars（c720）＝機首の角度の棒（同じ縮尺）。着陸の進入 約4度（p54「ピッチ角約4°」）・画面の表示が消える 25度（付図29 の注）・最大 52.6度（p49）
# ══════════════════════════════════════════════════════════
PB_V = (("着陸の進入", 4.0, "LINE"), ("画面の表示が消える", 25.0, "AMBER"), ("この夜の最大", 52.6, "ALERT"))
PB = dict(x0=660.0, x1=1660.0, vmax=60.0, ys=(430.0, 570.0, 710.0), h=64.0, ty=790.0)
PB_TICKS = (0, 10, 20, 30, 40, 50, 60)
PB_TWICE = 2


def pb_x(v):
    return PB["x0"] + (PB["x1"] - PB["x0"]) * v / PB["vmax"]


def pbars_base(st0):
    g = [F.line(PB["x0"], PB["ys"][0] - 60, PB["x0"], PB["ty"] - 34, J.LINE, 3)]
    for v in PB_TICKS:
        x = pb_x(v)
        g.append(F.line(x, PB["ty"] - 34, x, PB["ty"] - 22, J.TICK, 3))
        g.append(_tline(x, PB["ty"], str(v), 24, J.TICK, "middle", 80))
    g.append(_tline(PB["x1"] + 40, PB["ty"], "度", 24, J.TICK, "start", 80))
    for k, (t, _v, _r) in enumerate(PB_V):
        g.append(_tline(PB["x0"] - 24, PB["ys"][k] + 10, t, 28, J.TICK, "end", 520))
    return g


def pbars_stage(prev, st):
    s = []
    for k, f_ in ((0, "b0"), (1, "b0"), (2, "b1")):
        if _on(prev, st, f_):
            _t, v, r = PB_V[k]
            y = PB["ys"][k]
            s.append(F.rect(PB["x0"], y - PB["h"] / 2, pb_x(v) - PB["x0"], PB["h"], rc(r), None, op=0.92))
    if _on(prev, st, "twice"):
        x = pb_x(PB_V[1][1] * PB_TWICE)
        s.append(F.line(x, PB["ys"][0] - 50, x, PB["ty"] - 40, J.AMBER, 4, dash="12 8"))
        s.append(_tline(x - 12, PB["ys"][0] - 26, f"25度の{PB_TWICE}倍", 26, J.AMBER, "end", 300))
    return s


# ══════════════════════════════════════════════════════════
#  見え方の表（mech23 と同じ作り）
# ══════════════════════════════════════════════════════════
VIEWS = dict(
    # 🔧 門番 dup：左上の札が見出しを覆うと「図の写し」＝見出しと別の言い方に（c110・c206・c321・c517・c612・c616・c720）
    factors=dict(lab="要因の並べ図（報告書の認定）", fields=dict(cards=ONOFF, chain=ONOFF, acc=ONOFF, roles=ONOFF, mk_design=ONOFF, mk_crew=ONOFF),
                 base=factors_base, stage=factors_stage),
    clock2=dict(lab="時刻の書き方", fields=dict(utc=ONOFF, jst=ONOFF, units=ONOFF), base=clock2_base, stage=clock2_stage),
    seats=dict(lab="正面から見た操縦席の2つの席（人は描かない）", fields=dict(cap=ONOFF, age=ONOFF, fo=ONOFF, af=ONOFF, roles=ONOFF, order=ONOFF),
               base=seats_base, stage=seats_stage),
    hours=dict(lab="飛行時間の棒（同じ縮尺）", fields=dict(career=ONOFF, b0=ONOFF, b1=ONOFF), base=hours_base, stage=hours_stage),
    train=dict(lab="訓練の順", fields=dict(head=ONOFF, s1=ONOFF, s23=ONOFF), base=train_base, stage=train_stage),
    area=dict(lab="面積の比べ（マス目）", fields=dict(elev=ONOFF, ths=ONOFF, same=ONOFF), base=area_base, stage=area_stage),
    afs=dict(lab="自動飛行システムの主な中身", fields=dict(head=ONOFF, ap=ONOFF, at=ONOFF, fd=ONOFF), base=afs_base, stage=afs_stage),
    band=dict(lab="横から見た進入の道", fields=dict(land=ONOFF, ga=ONOFF), base=band_base, stage=band_stage),
    modes=dict(lab="モードの抜け方の流れ", fields=dict(dim=ONOFF, a=ONOFF, b=ONOFF, b2=ONOFF, c=ONOFF, cx=ONOFF, stay=ONOFF),
               base=modes_base, stage=modes_stage),
    fcom=dict(lab="表示と操縦の手引き書", fields=dict(fma=ONOFF, gap=ONOFF, rec=ONOFF), base=fcom_base, stage=fcom_stage),
    who3=dict(lab="可能性の札（並べるだけ）", fields=dict(c01=ONOFF, c2=ONOFF, br=ONOFF), base=who3_base, stage=who3_stage),
    ths=dict(lab="角度の帯（時刻と角度）", fields=dict(line=tuple(TH_LINE), lab53=ONOFF, desc=ONOFF, flat=ONOFF, oot=ONOFF),
             base=ths_base, stage=ths_stage),
    warn=dict(lab="鳴る・鳴らないの流れ", fields=dict(dev=ONOFF, ring=ONOFF, cut=ONOFF, why=ONOFF, opts=ONOFF), base=warn_base, stage=warn_stage),
    eu=dict(lab="上から見たイギリスとフランス", fields=dict(src=ONOFF, req=ONOFF, what=ONOFF), base=eu_base, stage=eu_stage),
    cards3=dict(lab="可能性の札", fields=dict(q=ONOFF, cards=ONOFF), base=cards3_base, stage=cards3_stage),
    assist=dict(lab="横から見た押す向き", fields=dict(l=ONOFF, name=ONOFF, r=ONOFF), base=assist_base, stage=assist_stage),
    afloor=dict(lab="アルファ・フロアの働き", fields=dict(name=ONOFF, flow=ONOFF, safe=ONOFF), base=afloor_base, stage=afloor_stage),
    pitch=dict(lab="横から見た機首の角度", fields=dict(dial=ONOFF, needle=ONOFF), base=pitch_base, stage=pitch_stage, parts=pitch_parts),
    pbars=dict(lab="機首の角度の棒", fields=dict(b0=ONOFF, b1=ONOFF, twice=ONOFF), base=pbars_base, stage=pbars_stage),
)
START = {v: {f: d["fields"][f][0] for f in d["fields"]} for v, d in VIEWS.items()}
HEAD_ONLY = dict(modes=("dim",))
ORDER = dict(ths=dict(line=tuple(TH_LINE)))
# 原文の値・欄・項目の写し（左上に「模式」を付けない）
NOT_SCHEMATIC = ("factors", "clock2", "hours", "who3", "ths", "cards3", "pitch", "pbars")
VIEW_DIR = ("横から", "上から", "斜めから", "正面")


def lab_of(view, st0):
    lab = VIEWS[view]["lab"]
    return lab(st0) if callable(lab) else lab


TAG_AT = {v: {} for v in VIEWS}


def anchors(view, st):
    return {}


def parts_of(view, st):
    fn = VIEWS[view].get("parts")
    return fn(st) if fn else []


def _states(view, start, steps):
    fields = VIEWS[view]["fields"]
    cur = dict(START[view], **(start or {}))
    out = []
    for i, st in enumerate([dict(state={})] + list(steps)):
        new = st.get("state") or {}
        for f_ in HEAD_ONLY.get(view, ()):
            if i > 0 and f_ in new:
                raise ValueError(f"m17：{f_} は頭（start）だけで決める")
        cur = dict(cur, **new)
        for f_, v in cur.items():
            if f_ not in fields:
                raise ValueError(f"m17：知らない欄 {f_!r}（{view} で使えるのは {tuple(fields)}）")
            if v not in fields[f_]:
                raise ValueError(f"m17：{f_}={v!r} は知らない値（{fields[f_]}）")
        out.append(dict(cur))
    for f_, seq in ORDER.get(view, {}).items():
        idx = [seq.index(s[f_]) for s in out]
        if any(b < a for a, b in zip(idx, idx[1:])):
            raise ValueError(f"m17：{f_} は戻さない（{' → '.join(seq)}）")
    return out[0], out[1:]


def stage_art(view, prev, st):
    return VIEWS[view]["stage"](prev, st)


def _base(view, st0):
    """基図＋頭の状態の層（頭で on にした欄は基図に描く＝前のカットの続き）"""
    pre = dict(START[view], **{k: st0[k] for k in HEAD_ONLY.get(view, ())})
    if view == "ths":
        pre["line"] = st0["line"]          # 頭の線は基図（ths_base）が描く
    return VIEWS[view]["base"](st0) + stage_art(view, pre, st0)


def _stage_svgs(view, steps, start, states, cap=32):
    pre = TAG_AT[view]
    stages, texts = [], []
    prev = start
    for st, stt in zip(steps, states):
        s = stage_art(view, prev, stt)
        an = anchors(view, stt)
        for tg in F._many(st.get("tag")):
            at = tg.get("at", next(iter(pre)) if pre else (L_X, 330.0))
            x, y, anchor, mw = pre[at] if isinstance(at, str) else (tuple(at) if len(at) == 4 else (at[0], at[1], "start", 420))
            c = tg.get("cap", cap)
            col = tg.get("col", INK)
            if tg.get("to"):
                tx, ty = an[tg["to"]] if isinstance(tg["to"], str) else tg["to"]
                s.append(F.line(x, y + 8, tx, ty, col, 2))
            s.append(F.txtfit(x, y, tg["t"], mw, cap=c, col=col, anchor=anchor))
            texts.append(tg["t"])
        stages.append("".join(s) or " ")
        prev = stt
    return stages, texts


def _static_part(sh):
    a = float(sh["keys"][0].get("alpha", 1.0))
    if a <= 0.01:
        return ""
    k0 = sh["keys"][0]
    pts = F.mech_pts(sh, k0)
    return F.poly(pts, k0.get("fill", sh.get("fill")) or "none", k0.get("stroke", sh.get("stroke")), sh.get("w") or None, close=True,
                  op=(round(a, 2) if a < 0.99 else None))


KEY_FIELDS = ("pts", "rot", "alpha", "fill", "stroke", "glow", "dx", "dy")
_TEXT = re.compile(r"<text\s[^>]*>([^<]*)</text>")


def svg_texts(svg):
    """SVG の <text> の中身（門番が全部の字から数を拾う）。"""
    return [t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">") for t in _TEXT.findall(svg)]


def m17(view, steps, start=None, rel=(), note="", src=""):
    """17本目の図解。view は VIEWS の見え方。steps＝ナレーションの行ごとの段。"""
    if view not in VIEWS:
        raise ValueError(f"m17：知らない見え方 {view!r}（{tuple(VIEWS)}）")
    if view not in NOT_SCHEMATIC and "模式" not in note:
        raise ValueError("m17：note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    st0, states = _states(view, start, steps)
    seq = [st0] + states
    per = [parts_of(view, s) for s in seq]
    shapes, anim = [], []
    for j, p0 in enumerate(per[0]):
        keys = []
        for i, ps in enumerate(per):
            pj = ps[j]
            kk = {f_: pj[f_] for f_ in KEY_FIELDS if f_ in pj and pj[f_] is not None}
            kk.setdefault("alpha", 1.0)
            dl = 0.0 if i == 0 else float(steps[i - 1].get("delay", 1.0 if i == 1 else F.MECH_DELAY)) + float(p0.get("lag", 0.0))
            keys.append(dict(stage=max(0, i - 1), delay=dl, **kk))
        sh = {f_: p0[f_] for f_ in p0 if f_ not in ("alpha", "dx", "dy", "rot", "lag")}
        sh["keys"] = keys
        moving = any({f_: kk.get(f_) for f_ in KEY_FIELDS} != {f_: keys[0].get(f_) for f_ in KEY_FIELDS} for kk in keys[1:])
        sh["anim"] = bool(moving)
        shapes.append(sh)
        if moving:
            anim.append(sh)
    g = _base(view, st0)
    for sh in shapes:
        if not sh["anim"]:
            g.append(_static_part(sh))
    lab = lab_of(view, st0)
    g.append(F.txtfit(F.BX0 + 8, F.BY0 + 36, lab + ("" if view in NOT_SCHEMATIC else "・模式"), 1000, cap=30, col=J.TICK))
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK))
    stages, texts = _stage_svgs(view, steps, st0, states)
    base_svg = "".join(g)
    f = F.Fig(base_svg, stages, "", (F.BX0, F.BX1))
    f.moves = ([dict(kind="anim", stage=0, shapes=anim, box=F._mech_box(anim), delay=F.MECH_DELAY, dur=F.MECH_DUR)]
               if anim else [])
    # 門番が数を拾う字＝基図（左上の札と出典の行を除く）と段の層の全部
    body = "".join(g[:-2]) + "".join(stages)
    f.mech = dict(kind="m17", view=view, start=st0, states=states, rel=list(rel), tags=texts, shapes=shapes, lab=lab, note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view, st0, states), texts_all=svg_texts(body))
    return f


# ══════════════════════════════════════════════════════════
#  門番が測る形（描く関数と同じ式・記録の値は門番の側 REC_M17）
# ══════════════════════════════════════════════════════════
def geo_of(view, start, states):
    allst = [start] + list(states)
    out = dict(view=view, seq=[dict(s) for s in allst])
    if view == "factors":
        xy = [fac_xy(i) for i in range(1, 13)]
        out.update(factors=tuple(FACTORS), who={k: (t, r) for k, (t, r) in FAC_WHO.items()}, xy=xy, size=(FG["w"], FG["h"]),
                   mk={k: tuple(i for i, _t in v) for k, v in FAC_MK.items()})
    elif view == "clock2":
        utc, jst = ck2_times()
        out.update(utc=utc, jst=jst, add=CK2_ADD, angles=(ck2_angles(utc), ck2_angles(jst)), units=tuple(CK2_UNITS))
    elif view == "seats":
        out.update(names=ST_NAME, left_x=ST["xs"][0], right_x=ST["xs"][1], age=ST_AGE, af=ST_AF, years=st_years(), roles=ST_ROLE,
                   order=ST_ORDER, arrow=(ST["xs"][0] + 120.0, ST["xs"][1] - 120.0))
    elif view == "hours":
        out.update(rows=tuple((t, v) for t, v, _r in HR_V), x0=HR["x0"], unit=(HR["x1"] - HR["x0"]) / HR["vmax"],
                   ends=tuple(hr_x(v) for _t, v, _r in HR_V), career=HR_CAREER, ticks=tuple((v, hr_x(v)) for v in HR_TICKS))
    elif view == "train":
        out.update(steps=TR_STEPS, hours=TR_HOURS, segs=[tr_seg(k) for k in range(3)])
    elif view == "area":
        el, th = ar_cells()
        out.update(el_n=len(el), th_n=len(th), th_el=sum(1 for *_xy, e in th if e), ratio=AR_RATIO)
    elif view == "afs":
        out.update(afs=tuple(AFS3))
    elif view == "band":
        out.update(ft=BD_FT, m=BD_M, out=BD_OUT, y_low=BD["y_low"], g=BD["g"], td=BD["td"], land_x0=bd_x(BD["y_low"]), ga=tuple(BD["ga"]))
    elif view == "modes":
        out.update(rows={k: (t, tuple(r for r, _c in res)) for k, (t, res) in MD_ROWS.items()}, start=MD_START,
                   cols={k: tuple(c for _r, c in res) for k, (_t, res) in MD_ROWS.items()})
    elif view == "fcom":
        out.update(fma=FC_FMA, rows=FC_ROWS, miss=FC_MISS, rec=FC_REC)
    elif view == "who3":
        out.update(who3=tuple(WHO3))
    elif view == "ths":
        out.update(pts=tuple(TH_PTS), px=[(th_x(t), th_y(a)) for t, a in TH_PTS], x0=TH["x0"], y0=TH["y0"], k=TH["k"],
                   sec=(TH["x1"] - TH["x0"]) / TH["t1"], upto=[TH_LINE[s["line"]] for s in allst], desc=TH_DESC, off=TH_OFF,
                   clock0="20:14:00")
    elif view == "warn":
        out.update(inputs=tuple(t for t, _r in WN_IN), in_cols=tuple(r for _t, r in WN_IN), opts=WN_OPTS, why=WN_WHY)
    elif view == "eu":
        G = Geo()
        gb = eu_gb_poly()
        out.update(pts=dict(EU_PTS), px={k: G.px(*v) for k, v in EU_PTS.items()}, req=EU_REQ,
                   gb_n=len(gb or []), gb_c=((sum(y for _x, y in gb) / len(gb), sum(x for x, _y in gb) / len(gb)) if gb else None))
    elif view == "cards3":
        out.update(n=CD3_N)
    elif view == "assist":
        out.update(vec={k: tuple(v) for k, v in AS_VEC.items()}, name=AS_NAME)
    elif view == "afloor":
        out.update(steps=AFL_STEPS)
    elif view == "pitch":
        rows = []
        for s in allst:
            ps = {p["id"]: p for p in pitch_parts(s)}
            rows.append(dict(rot=ps["needle"]["rot"], plane=ps["plane"]["rot"], alpha=ps["needle"]["alpha"]))
        out.update(deg=PT_DEG, rows=rows)
    elif view == "pbars":
        out.update(rows=tuple((t, v) for t, v, _r in PB_V), x0=PB["x0"], unit=(PB["x1"] - PB["x0"]) / PB["vmax"],
                   ends=tuple(pb_x(v) for _t, v, _r in PB_V), twice=PB_TWICE, twice_x=pb_x(PB_V[1][1] * PB_TWICE))
    return out
