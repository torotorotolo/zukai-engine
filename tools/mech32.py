# -*- coding: utf-8 -*-
"""mech32.py — 32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03）「札の型」と「見え方の表」
（2026-11-11 新設・⑤b-5＝模式 前半〈第1〜5章の34カット〉）。

■ 型を決めた理由（⑤b-1 の割り振り「mech31 を写すか新しい型か」）
  31本目の型（`tools/mech31.py`＝札1〜4枚＋矢印0〜2本＋誰の記録かの色・見え方の表＝札と部品を座標で置く）をそのまま使う。
  🔴 **式は写さない＝import する**（格子 `layout`・札の大きさ `_size`・札と部品の作り `_c`・`_x`・`_f`・`_z`・`_at`・`_p`・`_zbox`・線と印 `_lead`・`_tie`・
     `_plane`・`_blip`・`_dbl` は mech31 の関数＝回をまたいで同じ式）。写したのは**表の値を引く関数だけ**（誰の記録かの色 `sc`・印の表 `ICONS`・
     描き手 `_draw_card`・`_draw_arrow`・配線 `fu`・`zu`・`stage_art`・`m32`・`geo_of`）＝mech31 の関数はその回の表（31本目の SRC・FU・VIEWS）を引くため。
  31本目の表（FU・VIEWS・SRC）は mech31 に残したまま＝selftest の見本（`fixture_ep31`）が引く。32本目の章ファイルは m32 だけを引く。

■ 何か（31本目と同じ）
  札の型＝表 `FU` の1行が1カット（格子に並べる）。見え方の表＝表 `VIEWS` の1行が1カット（札と部品を座標で置く＝模式の絵・時間の線・棒）。
  段の層（その行から出て残る）・動く部品は使わない。再現イラストではない。
  🔴 **地は写真**（`cuts.ss.gr`＝暗くするだけ・静止・原色）＝字は暗い縁取り（OL）・札の地は半ば透ける紺（`_panel`）。8:1 は check_ground。
  🔴🔴 **この回の線＝名前を出すのは機長と副操縦士だけ**（c203・c205＝姓だけ）・客室乗務員・管制官・救助の人は立場だけ・乗客は名前なし・
     「犠牲」「死亡」は言わない・「208秒」は使わず「約3分半」。**人の形・顔を描かない**（席は丸の印・機体は上か横から見た形だけ）。
     名前の網＝`ref/ep32/v2_build/namecheck32.py`。
  🔴 図の中身は台本 §4 の画の欄と出典の欄（PLAN の plan・src）の字の範囲だけ＝言い切らない。数は報告書の字のとおり。
     ⚠️ c617 の「約150メートルで衝撃に備える合図」は画の欄にあるが、報告書の字の層（`ref/ep32/src/ntsb/AAR1003.txt`）に字が無い＝図に入れない
     （付録C の頁の絵で当たるまで）。機首約11度は報告書 p73 の字（Touchdown with approximately 11 degrees of pitch）。
  🔴 **色は「誰の記録か」**（SRC）：報告書＝緑／公開ドケット（聴取の記録）＝紫／AP 通信＝橙。意味の色＝黄 AMBER（数・時刻）。
  🔴 札の中の数字と原文どおりの字（`q=True`＝「」が付く）は門番の側 `check_mech.REC_M32` が別に持つ＝描く側の表を書き換えると鳴る。
     字数と字の大きさは `tools/check_fuda.py`。

■ 表の書き方（31本目と同じ）
  `FU["c203"] = _f(2, "見出し", "副題", [_c(at=0, who=R, head="…", big="…", lines=("…",), cell=(0, 0)), …], [_x(1, "a", "b", t="…")], src=S_R)`
  `VIEWS["c207"] = _z(2, "見出し", "副題", [_at(_c(…), x, y), …], [_p(0, fn), …], src=…, note="模式・…", schem=True, tl=…)`
  SPEC は `"c203": M.fu_spec("c203", ss.gr("c50"))`／`"c207": M.zu_spec("c207", ss.gr("c50"))`。
"""
from __future__ import annotations

import math
import re

import jiko_style as J
import mech31 as _M31
import titan_fig as F
from mech21 import _arrow, _on, _qmark, _xmark
from mech24 import rc
from mech27 import INK, OL, ONOFF, _panel, _t, svg_texts
# 🔴 mech31 の式（表を引かない関数だけ）＝回をまたいで同じ式
from mech31 import (AREA_H, AREA_W, ICON_H, ICON_W, LH, PX, _arrow_xy, _at, _blip, _c, _dbl, _f, _lead, _p, _plane, _rows, _size,  # noqa: F401
                    _tie, _x, _z, _zbox, GRAY_FILL, GRAY_INK, GRAY_LINE, layout)
from mech31 import _qwrap  # noqa: F401

# 誰の記録か（名・ROLE か J の名）。同じ色の鍵は同じ画面に出さない（門番が見る）
SRC = dict(
    hokoku=("NTSB の報告書", "ntsb"),
    docket=("NTSB の公開ドケット", "tsb"),
    ap=("AP 通信", "company"),
)
R, D, A = "hokoku", "docket", "ap"
S_R = "NTSB「NTSB/AAR-10/03」（2010）"
S_D = "NTSB 公開ドケット DCA09MA026（聴取の記録）"
S_AP = "AP 通信（PBS NewsHour の転載・2016年9月）"


def sc(key):
    return rc(SRC[key][1]) if key else J.LINE


# ══════════════════════════════════════════════════════════
#  印（人の形・顔は描かない＝線と四角だけ。ICON_W×ICON_H に収まる）。mech31 の形＋32本目の形
# ══════════════════════════════════════════════════════════
def _i_screen(cx, cy, col):
    """操縦室の画面（四角と、字の代わりの横線）。"""
    g = F.rect(cx - 66, cy - 50, 132, 92, J.BG2, col, 6, rx=8)
    for i, w in enumerate((84, 64, 74)):
        g += F.line(cx - 46, cy - 24 + 24 * i, cx - 46 + w, cy - 24 + 24 * i, col, 5)
    return g + F.line(cx - 26, cy + 42, cx - 34, cy + 60, col, 5) + F.line(cx + 26, cy + 42, cx + 34, cy + 60, col, 5)


ICONS = dict(_M31.ICONS, screen=_i_screen)


# ══════════════════════════════════════════════════════════
#  描き手（mech31 と同じ式＝表 SRC・ICONS だけ32本目の物を引く）
# ══════════════════════════════════════════════════════════
def _icon(c, cx, cy, col, k):
    """印の座標は等倍で書いた＝拡大率を座標の値に掛ける（mech31._icon と同じ式）。"""
    g = ICONS[c["icon"]](cx, cy, col)
    if c["cross"]:
        g += _xmark(cx, cy, 50, J.ALERT, 10)

    def xv(v):
        return cx + (float(v) - cx) * k

    def yv(v):
        return cy + (float(v) - cy) * k

    g = re.sub(r'(?<![-\w])(x|x1|x2|cx)="([-\d.]+)"', lambda m: f'{m[1]}="{xv(m[2]):.1f}"', g)
    g = re.sub(r'(?<![-\w])(y|y1|y2|cy)="([-\d.]+)"', lambda m: f'{m[1]}="{yv(m[2]):.1f}"', g)
    g = re.sub(r'(?<![-\w])(width|height|r|rx|stroke-width)="([-\d.]+)"', lambda m: f'{m[1]}="{float(m[2]) * k:.1f}"', g)
    return re.sub(r' d="M([^"]+)"', lambda m: ' d="M' + re.sub(r"([-\d.]+) ([-\d.]+)", lambda p: f"{xv(p[1]):.1f} {yv(p[2]):.1f}", m[1]) + '"', g)


def _draw_card(c, box, k=1.0):
    """mech31._draw_card と同じ式（色だけ32本目の SRC）。"""
    x, y, w, h = box
    col = sc(c["who"])
    ink, big = INK, J.AMBER
    head = col
    fill = None
    op = None
    if c["gray"]:
        col, ink, big, head, fill = GRAY_LINE, GRAY_INK, GRAY_INK, GRAY_INK, GRAY_FILL
    if c["dim"]:
        ink, big, head = J.TICK, J.TICK, J.TICK
        col = J.TICK
        op = 0.55
    g = _panel(x, y, w, h, col, op=op if op is not None else 0.84, sw=3 if c["dim"] else 5, fill=fill)
    rows = _rows(c, k)
    ch = sum(cap * LH[kd] for kd, _t2, cap in rows)
    tx0, tw = x, w
    if c["icon"]:
        g += _icon(c, x + (PX + ICON_W / 2) * k, y + h / 2, col, k)
        tx0, tw = x + (ICON_W + 22) * k, w - (ICON_W + 22) * k
    tx = tx0 + tw / 2
    yy = y + (h - ch) / 2
    for kd, t, cap in rows:
        lh = cap * LH[kd]
        base = yy + lh / 2 + cap * 0.36
        colr = head if kd == "head" else big if kd == "big" else (J.TICK if c["dim"] else ink)
        g += _t(tx, base, t, cap, colr, "middle", tw - 2 * PX * k + 8)
        yy += lh
    return g


def _draw_arrow(a, boxes, k=1.0):
    """mech31._draw_arrow と同じ式（色だけ32本目の SRC）。"""
    x1, y1, x2, y2 = _arrow_xy(boxes[a["a"]], boxes[a["b"]])
    col = sc(a["who"])
    g = _arrow(x1, y1, x2, y2, col, 8, 30, "16 12" if a["dash"] else None) if a["head"] else F.line(x1, y1, x2, y2, col, 7, dash="16 12" if a["dash"] else None)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    if a["q"]:
        g += _qmark(mx, my - 8 * k, 76 * k, J.AMBER)
    if a["ng"]:
        g += _xmark(mx, my, 26 * k, J.ALERT, 9)
    if a["t"]:
        if abs(y1 - y2) < 2:
            g += _t(mx, my - 26 * k, a["t"], 34 * k, col, "middle", max(abs(x2 - x1), 130.0))
        else:
            g += _t(mx + 26 * k, my + 12 * k, a["t"], 34 * k, col, "start", 420.0)
    return g


# ══════════════════════════════════════════════════════════
#  札の型の表（1行が1カット）。カットの順＝一覧 `ref/ep32/eizou_list32.md`。字は語りと同じ字面を避ける（門番 echo）・見出しと重ねない（門番 dup）
# ══════════════════════════════════════════════════════════
FU = {}
# ── 第1章
FU["c203"] = _f(2, "操縦室の1人目", "経歴の記録", [
    _c(0, R, head="機長", big="57歳", lines="サレンバーガー", cell=(0, 0)),
    _c(1, R, head="飛んだ時間", big="1万9,663時間", sub=("うち A320", "4,765時間"), cell=(1, 0))], src=S_R)
FU["c205"] = _f(2, "操縦室の2人目", "経歴の記録", [
    _c(0, R, head="副操縦士", big="49歳", lines="スカイルズ", cell=(0, 0)),
    _c(0, R, head="飛んだ時間", big="1万5,643時間", cell=(1, 0)),
    # 🔧 slide G-14：右に並べると地 c50 の焼き込みの字（格納庫の札）の上に載った＝下の段へ
    _c(1, R, head="うち A320", big="37時間", sub="資格は2008年12月31日", cell=(0, 1), span=(2, 1))], src=S_R)
FU["c213"] = _f(2, "操縦の役目", "離陸のとき", [
    _c(0, R, head="操縦する人", lines="副操縦士", cell=(0, 0)),
    _c(0, R, head="見守る人", lines="機長", cell=(1, 0))],
    [_x(1, "a", "b", t="このあと入れ替わる", head=False)], src=S_R)
# ── 第2章
FU["c311"] = _f(3, "機体の後ろの装置", "報告書の注", [
    _c(1, R, head="APU", lines="後ろの小さなエンジン", icon="plane", cell=(0, 0)),
    _c(2, R, lines="電気をつくる", sub="もう1つの電気の源", cell=(1, 0))],
    [_x(2, "a", "b")], src=S_R)
FU["c313"] = _f(2, "操縦の交代", "鳥とぶつかったあと", [
    _c(0, R, head="機長", lines="操縦・交信", sub="降りる場所を決める", cell=(0, 0)),
    _c(1, R, head="副操縦士", lines="手順書", cell=(1, 0)),
    _c(1, R, big="約12秒", sub="ぶつかってから", cell=(0, 1), span=(2, 1))], src=S_R)
FU["c319"] = _f(2, "届かなかった声", "無線の重なり", [
    _c(0, R, head="1549便", lines="機長の声の一部", icon="plane", cell=(0, 0)),
    _c(0, R, head="ほかの機", lines="同じ周波数で交信", cell=(0, 1)),
    _c(0, R, head="管制", lines="届かず", icon="radio", cell=(1, 0), span=(1, 2)),
    _c(1, R, head="便名", big="1539", sub="正しくは1549", cell=(2, 0), span=(1, 2))],
    [_x(0, "a", "c", ng=True), _x(0, "b", "c")], src=S_R)
# ── 第3章
FU["c402"] = _f(2, "交信の相手", "離陸のあと", [
    _c(0, R, lines="1549便", icon="plane", cap=56, cell=(0, 0), span=(1, 3)),
    _c(0, R, head="レーダー", lines="出発の管制", cell=(1, 0)),
    _c(0, R, lines="ラガーディアの管制塔", dim=True, cell=(1, 1)),
    _c(0, R, lines="テターボロの管制", dim=True, cell=(1, 2))],
    [_x(0, "a", "b", t="交信")], src=S_R)
FU["c405"] = _f(3, "戻った推力", "15時28分の操縦室", [
    _c(0, R, head="機長", big="15:28:25", lines="左のエンジンが少し戻ってきた", q=True, cell=(0, 0)),
    _c(2, R, head="報告書", lines=("どちらのエンジンも", "飛び続ける力は出せず"), cell=(1, 0))], src=S_R, mute=(0,))
FU["c410"] = _f(2, "3つの道", "降りる場所の案", [
    _c(0, R, lines="ラガーディア", cell=(0, 0)),
    _c(0, R, head="右手の空港", lines="テターボロ", cell=(1, 0)),
    _c(0, R, lines="ハドソン川", cell=(2, 0)),
    _c(1, R, head="機長", lines="そうする", q=True, cell=(1, 1))], src=S_R, mute=(1,))
FU["c417"] = _f(3, "聞き返し", "管制の録音", [
    _c(0, R, head="管制", lines="すまない、もう一度", q=True, icon="radio", cell=(0, 0))], src=S_R, mute=(0,))
# ── 第4章
FU["c503"] = _f(2, "試しの条件", "シミュレーター", [
    _c(0, R, head="事故の日に合わせた", lines=("風・気温", "機体の重さ"), cell=(0, 0)),
    # 🔧 slide G-14：右に並べると地 gm1 の焼き込みの字（シミュレーターの画面）の上に載った＝下の段へ
    _c(1, R, head="始まり", lines="鳥とぶつかる少し前", cell=(0, 1))], src=S_R)
FU["c513"] = _f(3, "機長の聴取", "戻らなかった理由", [
    _c(1, R, head="ラガーディアへ戻るのは", lines="現実的な選択ではなかった", q=True, cell=(0, 0)),
    _c(2, R, head="いったん曲がれば", lines=("ほかの道をすべて消す", "取り消せない選択"), q=True, cell=(0, 1))], src=S_R, mute=(1, 2))
FU["c518"] = _f(2, "調査の側の話", "映画のあとの記事", [
    _c(0, A, head="AP 通信の記事", lines="調査を率いた元の責任者", cell=(0, 0)),
    _c(1, A, lines=("誰にも恥をかかせる", "つもりはまったくなかった"), q=True, cell=(0, 1))], src=S_AP, mute=(1,))
# ── 第5章
FU["c601"] = _f(3, "画面と冊子", "故障のときの決まり", [
    _c(1, R, head="ふだん", lines="操縦室の画面", sub="故障とやることが出る", icon="screen", cell=(0, 0)),
    _c(2, R, head="両方のエンジンの故障", lines="紙の冊子を開く", icon="book", cell=(1, 0))],
    [_x(2, "a", "b", t="例外")], src=S_R)
FU["c605"] = _f(3, "エアバスの考え", "高い空と低い所", [
    _c(0, R, lines="飛ぶ時間の多くは高い空", cell=(0, 0)),
    _c(1, R, lines="故障の見込みも高い空", cell=(1, 0)),
    _c(2, R, head="低い所の故障の手順書", lines="検討していなかった", cell=(0, 1), span=(2, 1))],
    [_x(1, "a", "b", t="だから")], src=S_R)
FU["c608"] = _f(3, "手順書の改訂", "エアバスの直し", [
    _c(0, R, head="2005年", lines=("燃料が残る場合", "残らない場合"), sub="2本立てに", cell=(0, 0)),
    _c(1, R, head="別の手順書から", lines="着水の手順", cell=(1, 0)),
    _c(2, R, lines="長い手順書に", icon="book", cell=(0, 1), span=(2, 1))],
    [_x(1, "b", "a", t="入れる")], src=S_R)
FU["c610"] = _f(2, "たどった手順", "手順書の1つ目の部分", [
    _c(0, R, lines="a 点火 … 入れる", cell=(0, 0)),
    _c(1, R, lines=("b 推力のレバー … 確かめる", "c 速さ 300ノットを保つ", "d 降りる場所 … 決める"), cell=(0, 1))], src=S_R)
FU["c617"] = _f(2, "着水の段取り", "手順書の3ページ目", [
    _c(0, R, head="地上から", big="約910メートル", lines="までに翼を降りる形に", cell=(0, 0)),
    _c(1, R, big="約610メートル", lines="着水のボタン", cell=(1, 0)),
    _c(1, R, head="水面に着くとき", lines="機首 約11度", cell=(0, 1), span=(2, 1))],
    [_x(1, "a", "b"), _x(1, "b", "c")], src=S_R)
FU["c621"] = _f(2, "訓練の中身", "副操縦士の話", [
    _c(0, D, lines="地上の座学だけ", cell=(0, 0)),
    _c(0, D, head="シミュレーター", lines="着水の訓練なし", cell=(1, 0)),
    _c(1, D, head="教わった着水", lines="時間がある前提", cell=(0, 1), span=(2, 1))], src=S_D)
FU["c626"] = _f(2, "報告書の見方", "もしあれば", [
    _c(0, R, lines="低い所の故障用の手順書", cell=(0, 0)),
    _c(1, R, head="最後まで終えられた", lines="見込みはより高い", cell=(1, 0))],
    [_x(1, "a", "b", t="あれば")], src=S_R)
FU["c628"] = _f(2, "手順書の勧告", "報告書の勧告", [
    _c(0, R, head="勧告", lines="手順書の作り方の指針", sub="大事な項目の順番・長さ・時間", cell=(0, 0)),
    _c(1, R, head="勧告", lines="低い所の故障を訓練に", sub="座学とシミュレーター", cell=(1, 0))], src=S_R)
FU["c630"] = _f(2, "勧告のその後", "この章の勧告", [
    _c(0, R, lines="勧告", dim=True, cell=(0, 0)),
    _c(0, R, lines="勧告", dim=True, cell=(1, 0)),
    _c(0, R, lines="勧告", dim=True, cell=(2, 0)),
    _c(0, R, lines="勧告", dim=True, cell=(3, 0)),
    _c(0, R, big="第10章", lines="で見る", cell=(0, 1), span=(4, 1))], src=S_R)


# ══════════════════════════════════════════════════════════
#  見え方の表 VIEWS（札と部品を座標で置く＝模式の絵・時間の線・棒）。札は札の型と同じ部品＝門番が測る形も同じ
# ══════════════════════════════════════════════════════════
VIEWS = {}


def _ring(c, col=None, pad=14.0):
    return _M31._ring(c, col, pad)


# ── 機体を上から（第1章 c207・c209）＝丸い筒（前＝左）。人の形は描かない
BODY = (360.0, 1560.0, 500.0, 660.0)


def _body(lab=True):
    x0, x1, y0, y1 = BODY
    g = F.rect(x0, y0, x1 - x0, y1 - y0, J.BG2, INK, 6, rx=(y1 - y0) / 2, op=0.55)
    if lab:
        g += _t(x0 - 26, (y0 + y1) / 2 + 14, "前", 42, INK, "end", 100) + _t(x1 + 26, (y0 + y1) / 2 + 14, "後ろ", 42, INK, "start", 140)
    return g


def _seat(x, y, col=J.AMBER):
    return F.circ(x, y, 22, col) + F.circ(x, y, 34, "none", col, 4, op=0.6)


C207 = [
    _at(_c(0, R, head="前の席", big="2人", sub="51歳・57歳", bcap=64), 560, 355),
    _at(_c(0, R, head="後ろの席", big="1人", sub="58歳", bcap=64), 1360, 355),
    _at(_c(1, R, big="26年以上", lines="初めの訓練から", bcap=64, cap=46), 960, 765),
]
VIEWS["c207"] = _z(2, "客室乗務員", "座る位置と年齢", C207, [
    _p(0, _body), _p(0, lambda: _seat(470.0, 550.0) + _seat(470.0, 610.0) + _seat(1450.0, 580.0)),
    _p(0, lambda: _lead(C207[0], 470.0, 528.0) + _lead(C207[1], 1450.0, 558.0))],
    src=S_R, note="模式・席の位置は描いた形でない", schem=True)


def _doors():
    x0, x1, y0, y1 = BODY
    g = ""
    for x in (470.0, 1450.0):
        for y in (y0, y1):
            g += F.rect(x - 34, y - 14, 68, 28, J.AMBER, None, None, rx=6)
    return g


def _rows_of_seats():
    x0, x1, y0, y1 = BODY
    g = ""
    for i in range(18):
        x = 580.0 + 44.0 * i
        for y in (528.0, 560.0, 600.0, 632.0):
            g += F.rect(x - 12, y - 10, 24, 20, "none", J.TICK, 3, rx=4)
    return g


C209 = [
    _at(_c(0, R, head="前と後ろの扉", big="4つ", lines="すべり台", sub="救命いかだを兼ねる", bcap=64, cap=46), 960, 350),
    _at(_c(1, R, head="座席の下", lines="救命胴衣", sub="人数分", cap=46), 960, 760),
]
VIEWS["c209"] = _z(2, "この機体の装備", "海の上を長く飛ぶ備え", C209, [
    _p(0, _body), _p(0, _doors), _p(1, _rows_of_seats)],
    src=S_R, note="模式・扉と席の位置は描いた形でない", schem=True)

# ── 第2章 c315 推力（エンジンが機体を前へ押す＝矢印）。機体は上から・機首が右
C315 = [
    _at(_c(0, R, head="QRH", lines=("緊急のときの手順を", "まとめた冊子"), icon="book", cap=46), 470, 420),
    _at(_c(1, R, head="推力とは", lines="機体を前へ押す力", cap=46), 1250, 775),
]
VIEWS["c315"] = _z(2, "冊子と推力", "機長の指示", C315, [
    _p(0, lambda: _plane(1250.0, 560.0, INK, k=1.7, ang=90.0)),
    _p(1, lambda: _arrow(860.0, 560.0, 1110.0, 560.0, J.AMBER, 9, 30) + _t(985.0, 520.0, "推力", 48, J.AMBER, "middle", 200), arrow=True)],
    src=S_R, note="模式・機体の形は描いた形でない", schem=True)

# ── c321 速さの棒（時速＝比例・門番 ⑤ num が字の数を棒の端で測る）
SX0, SK = 300.0, 2.0          # 時速 0 の x・1キロ毎時＝2px
SY = (490.0, 800.0)


def _sx(v):
    return SX0 + v * SK


def _sbar(i, v, col):
    y = SY[i]
    return F.rect(SX0, y - 22, _sx(v) - SX0, 44, col, None, None, rx=6, op=0.85)


C321 = [
    _at(_c(0, R, head="かけ直しに向く速さ", big="時速約560キロ", sub="300ノット", bcap=64), 700, 340),
    _at(_c(1, R, head="ぶつかったあとの最高", big="時速約400キロ", sub="214ノット", bcap=64), 700, 650),
]
VIEWS["c321"] = _z(2, "足りない速さ", "エンジンをかけ直す", C321, [
    _p(0, lambda: F.line(SX0, 430.0, SX0, 860.0, J.TICK, 5)),
    _p(0, lambda: _sbar(0, 560.0, J.AMBER)), _p(1, lambda: _sbar(1, 400.0, J.LINE))],
    src=S_R, note="計器の速さの目安・棒の長さは時速の比例",
    tl=dict(kind="num", ax=((0.0, SX0), (600.0, _sx(600.0))), pts=(("時速約560キロ", _sx(560.0)), ("時速約400キロ", _sx(400.0)))))


# ── 第3章 c419 レーダーの電波が建物にさえぎられる（横から見た模式）
def _c419_ground():
    g = F.line(120.0, 780.0, 1800.0, 780.0, J.TICK, 5)
    g += _M31._i_ndb(260.0, 700.0, INK) + _t(260.0, 830.0, "レーダー", 40, INK, "middle", 240)
    for x, w, h in ((760.0, 100.0, 260.0), (880.0, 80.0, 200.0), (980.0, 110.0, 300.0)):
        g += F.rect(x, 780.0 - h, w, h, J.BG2, J.TICK, 4, op=0.9)
    g += _t(925.0, 830.0, "建物", 40, J.TICK, "middle", 200)
    return g + _blip(1500.0, 700.0, J.AMBER) + _t(1500.0, 650.0, "機体", 40, J.AMBER, "middle", 200)


def _c419_sight():
    # 電波の筋（アンテナの先から機体へ）＝建物の面で止まる（×）
    x0, y0, x1, y1 = 290.0, 660.0, 1500.0, 700.0
    xb = 760.0
    yb = y0 + (y1 - y0) * (xb - x0) / (x1 - x0)
    g = F.line(x0, y0, xb - 6, yb, J.AMBER, 6, dash="18 12")
    g += F.line(xb, yb, x1 - 40, y1 - 1, J.TICK, 3, dash="6 14", op=0.6)
    return g + _xmark(xb - 30, yb - 2, 26, J.ALERT, 9)


C419 = [
    _at(_c(0, R, head="出発の管制", big="15:29:53", lines="レーダーで見失う", bcap=64, cap=46), 1300, 330),
]
VIEWS["c419"] = _z(2, "見えなくなった機体", "低く降りたとき", C419, [
    _p(0, _c419_ground), _p(1, _c419_sight)],
    src=S_R, note="模式・高さと距離は描いた形でない", schem=True)

# ── 第4章 c507 15回の試し（降りられた8回＝黄・残る7回＝印）。並びは試しの順でない
BX, BW_, BG_ = 281.0, 70.0, 22.0


def _box(i, ok):
    x = BX + i * (BW_ + BG_)
    if ok:
        return F.rect(x, 560.0, BW_, BW_, J.AMBER, None, None, rx=8, op=0.9)
    return F.rect(x, 560.0, BW_, BW_, "none", J.TICK, 4, rx=8) + _xmark(x + BW_ / 2, 595.0, 18, J.TICK, 6)


C507 = [
    _at(_c(0, R, big="8回", lines="降りられた", sub="どれも直後に曲がった", bcap=64, cap=46), 638, 390),
    _at(_c(1, R, big="7回", lines="うまく降りられず", bcap=64, cap=46), 1328, 390),
]
VIEWS["c507"] = _z(3, "試しの結果", "シミュレーター", C507, [
    _p(0, lambda: "".join(_box(i, True) for i in range(8)) + _t(960.0, 720.0, "15回の試し", 42, J.TICK, "middle", 400)),
    _p(1, lambda: "".join(_box(i, False) for i in range(8, 15)))],
    src=S_R, note="模式・並びは試しの順でない", schem=True)


# ── c510 1549便の実際（秒の線＝門番 ⑤ hms）。目盛りは10秒ごと・字は札の時刻だけ
def _hs(h, m, s=0):
    return h * 3600.0 + m * 60.0 + s


TX = dict(x0=240.0, x1=1680.0, y=600.0, v0=_hs(15, 27, 0), v1=_hs(15, 28, 0))


def _tx(v):
    return TX["x0"] + (v - TX["v0"]) * (TX["x1"] - TX["x0"]) / (TX["v1"] - TX["v0"])


V510 = (_hs(15, 27, 11), _hs(15, 27, 33), _hs(15, 27, 50))


def _c510_axis():
    g = F.line(TX["x0"], TX["y"], TX["x1"], TX["y"], J.TICK, 5)
    for s in range(0, 61, 10):
        x = _tx(TX["v0"] + s)
        g += F.line(x, TX["y"] - 14, x, TX["y"] + 14, J.TICK, 4)
    return g


def _span(v_a, v_b, y, lab):
    xa, xb = _tx(v_a), _tx(v_b)
    g = F.line(xa, y, xb, y, J.AMBER, 6) + F.line(xa, y - 14, xa, y + 14, J.AMBER, 5) + F.line(xb, y - 14, xb, y + 14, J.AMBER, 5)
    return g + _t((xa + xb) / 2, y + 56, lab, 44, J.AMBER, "middle", 300)


C510 = [
    _at(_c(1, R, big="15:27:11", lines="鳥とぶつかる", bcap=64, cap=46), 420, 380),
    _at(_c(1, R, big="15:27:33", lines="管制へ第一報", bcap=64, cap=46), 960, 380),
    _at(_c(2, R, big="15:27:50", lines="手順書を読み始める", bcap=64, cap=46), 1520, 380),
]
VIEWS["c510"] = _z(3, "1549便の実際", "ぶつかってから", C510, [
    _p(0, _c510_axis),
    _p(1, lambda: _lead(C510[0], _tx(V510[0]), TX["y"]) + _lead(C510[1], _tx(V510[1]), TX["y"]) + _span(V510[0], V510[1], 670.0, "22秒")),
    _p(2, lambda: _lead(C510[2], _tx(V510[2]), TX["y"]) + _span(V510[0], V510[2], 760.0, "39秒"))],
    src=S_R, note="目盛りは10秒ごと",
    tl=dict(kind="hms", ax=((TX["v0"], TX["x0"]), (TX["v1"], TX["x1"])),
            pts=(("15:27:11", _tx(V510[0])), ("15:27:33", _tx(V510[1])), ("15:27:50", _tx(V510[2])))))


# ── c522 判断の35秒を足した1回（滑走路の手前で止まる矢印）
def _c522_runway():
    g = F.rect(1450.0, 556.0, 330.0, 44.0, J.BG2, INK, 5, rx=6)
    return g + _t(1615.0, 650.0, "滑走路", 40, INK, "middle", 240)


def _c522_path():
    pts = [(300.0 + 20.0 * i, 500.0 + 75.0 * math.sin(i / 52.0 * math.pi * 0.5)) for i in range(53)]
    g = F.poly(pts, "none", J.AMBER, 7, dash="18 12")
    x, y = pts[-1]
    g += _arrow(x, y, x + 60.0, y + 2.0, J.AMBER, 7, 26)
    return g + F.line(1450.0, 520.0, 1450.0, 640.0, J.TICK, 4, dash="8 8") + _t(1395.0, 640.0, "届かず", 40, J.ALERT, "end", 200)


C522 = [
    _at(_c(0, R, head="判断の時間", big="35秒", sub="つかんで決めるまで", bcap=72), 420, 320),
    _at(_c(0, R, head="それを足した1回", lines="滑走路の手前", cap=46), 1560, 330),
    _at(_c(1, R, head="報告書の結論", lines="川が、生き残れる見込みのいちばん高い道", cap=46), 960, 770),
]
VIEWS["c522"] = _z(2, "届かなかった1回", "シミュレーターの答え", C522, [
    _p(0, _c522_runway), _p(0, _c522_path, arrow=True)],
    src=S_R + "・NTSB 公開ドケット DCA09MA026", note="模式・道の形と長さは描いた形でない", schem=True)

# ── 第5章 c603・c614・c623 手順書の3ページ（ページの中の区切りは模式）
PG = ((250.0, 300.0), (560.0, 300.0), (870.0, 300.0))
PW, PH = 230.0, 380.0
P1Y = 470.0            # 2ページ目の 1つ目の部分の下の端（模式）


def _pages():
    g = ""
    for i, (x, y) in enumerate(PG):
        g += F.rect(x, y, PW, PH, J.BG2, INK, 5, rx=8, op=0.8)
        for r in range(10):
            yy = y + 34.0 + 33.0 * r
            g += F.line(x + 26, yy, x + PW - 26 - (40 if r % 3 == 2 else 0), yy, J.TICK, 3, op=0.7)
        g += _t(x + PW / 2, y + PH + 50, f"{i + 1}ページ目", 38, INK, "middle", 260)
    return g


def _part(i, fill=False, dash=None, col=J.AMBER, op=0.16):
    (x1, y1), (x2, y2), (x3, y3) = PG
    rs = {1: [(x1, y1, PH), (x2, y2, P1Y - y2)], 2: [(x2, P1Y, y2 + PH - P1Y)], 3: [(x3, y3, PH)]}[i]
    g = ""
    for x, y, h in rs:
        g += F.rect(x + 6, y + 6, PW - 12, h - 12, col if fill else "none", None if fill else col, None if fill else 5, rx=6,
                    op=op if fill else None, dash=dash)
    return g


def _pnum(i):
    (x1, y1), (x2, y2), (x3, y3) = PG
    x, y = {1: (x1 + PW / 2, y1 + PH / 2 + 26), 2: (x2 + PW / 2, (P1Y + y2 + PH) / 2 + 26), 3: (x3 + PW / 2, y3 + PH / 2 + 26)}[i]
    g = _t(x, y, str(i), 72, J.AMBER, "middle", 120)
    if i == 1:
        # 🔧 試し焼き（11-11）：2ページ目の上の枠（1つ目の部分）に番号が無く「1」の続きと読みにくかった＝小さな「1」
        x2, y2 = PG[1]
        g += _t(x2 + PW / 2, (y2 + P1Y) / 2 + 16, "1", 44, J.AMBER, "middle", 80)
    return g


C603 = [
    _at(_c(0, R, head="1つ目", lines="エンジンをかけ直す", cap=46), 1480, 300),
    _at(_c(1, R, head="2つ目", lines=("かかったとき", "かからないとき"), cap=46), 1480, 520),
    _at(_c(2, R, head="3つ目", lines="不時着と着水", cap=46), 1480, 750),
]
VIEWS["c603"] = _z(3, "手順書の作り", "3つの部分", C603, [
    _p(0, _pages), _p(0, lambda: _part(1) + _pnum(1)), _p(1, lambda: _part(2) + _pnum(2)), _p(2, lambda: _part(3) + _pnum(3))],
    src=S_R, note="模式・ページの中の区切りは描いた形でない", schem=True)


def _c614_paint():
    (x1, y1), _p2, _p3 = PG
    return F.rect(x1 + 6, y1 + 6, PW - 12, PH - 12, J.AMBER, None, None, rx=6, op=0.42)


def _c614_done():
    # 🔧 ⑤b-6（11-11）：すぐ次の c615「全体の約3分の1」（報p105）と同じ塗り＝1ページ目だけ（3ページの3分の1）。
    #    1つ目の部分（1ページ目と2ページ目の上＝枠）の大半を塗る形のまま＝c614 の札「1つ目の大半まで」（報p104）とも合う
    return _c614_paint() + _part(1)


C614 = [
    _at(_c(0, R, head="報告書", lines="1つ目の大半まで", cap=46), 1480, 330),
    _at(_c(1, R, head="2つ目と3つ目", lines="入れなかった", sub="高さも時間も足りず", cap=46), 1480, 640),
]
VIEWS["c614"] = _z(2, "進んだ所", "手順書の3ページ", C614, [
    _p(0, _pages), _p(0, _c614_done), _p(1, lambda: _part(2, dash="12 10", col=J.TICK) + _part(3, dash="12 10", col=J.TICK))],
    src=S_R, note="模式・ページの区切りと塗った長さは描いた形でない", schem=True)

KY = 300.0 + 34.0 + 33.0 * 3          # 2ページ目の k の行（模式＝1つ目の部分の中）


def _c623_k():
    x, _y = PG[1]
    g = F.rect(x + 12, KY - 18, PW - 24, 36, "none", J.AMBER, 6, rx=8)
    return g + _t(x - 14, KY + 14, "k", 44, J.AMBER, "end", 60)


C623 = [
    _at(_c(1, R, head="2ページ目の k", lines="APU を始動する", sub="前に a〜j の10項目", cap=46), 1480, 330),
    _at(_c(1, R, head="報告書", lines="順番どおりなら行われず", cap=46), 1480, 640),
]
VIEWS["c623"] = _z(2, "大事な一手", "項目の順番", C623, [
    _p(0, _pages), _p(0, lambda: _part(1, dash="12 10", col=J.TICK)), _p(1, _c623_k)],
    src=S_R, note="模式・行の位置は描いた形でない", schem=True)


# ── c619 着水のボタン（横から見た機体と水面・水面より下の弁を閉じる）
WY = 560.0


def _c619_body():
    g = F.rect(300.0, 470.0, 1200.0, 140.0, J.BG2, INK, 6, rx=70, op=0.6)
    g += F.line(160.0, WY, 1700.0, WY, J.LINE, 5, dash="20 12") + _t(160.0, WY - 22, "水面", 40, J.LINE, "start", 160)
    for x in (520.0, 780.0, 1040.0, 1300.0):
        g += F.circ(x, 588.0, 14, "none", J.TICK, 4)
    return g


def _c619_shut():
    g = ""
    for x in (520.0, 780.0, 1040.0, 1300.0):
        g += F.circ(x, 588.0, 16, J.AMBER) + F.line(x - 12, 588.0, x + 12, 588.0, J.BG2, 5)
    return g


C619 = [
    _at(_c(1, R, head="着水のボタン", lines="水面より下の弁を閉じる", cap=46), 900, 320),
    _at(_c(2, R, lines="長く浮くのを助ける", cap=46), 900, 760),
]
VIEWS["c619"] = _z(3, "押すと起きること", "機体の下の弁", C619, [
    _p(0, _c619_body), _p(1, _c619_shut), _p(1, lambda: _lead(C619[0], 780.0, 572.0))],
    src=S_R, note="模式・弁の数と位置は描いた形でない", schem=True)


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-11-11）：第6〜10章の地を使う模式5カット（地 gf1・gk2・gl1・gr2 の明るさを `--suggest` で測るため ⑤b-6 から前倒し）
# ══════════════════════════════════════════════════════════
def _wing(cx, cy, chord, ang=0.0, flap=False):
    """翼の断面（前＝左）。ang＝前を上げる角度（度）。flap＝うしろの板を下へ出す（形と角度は模式）。
    🔧 試し焼き（11-11）：前の端がとがって見えた＝NACA の4桁の厚みの式（厚み15%・反り4%）で丸い前の端に"""
    a = math.radians(ang)
    ca, sa = math.cos(a), math.sin(a)

    def rot(x, y):
        return cx + x * ca - y * sa, cy + x * sa + y * ca

    def cam(u):
        m, p = 0.04, 0.4
        return m / p ** 2 * (2 * p * u - u * u) if u < p else m / (1 - p) ** 2 * ((1 - 2 * p) + 2 * p * u - u * u)

    def th(u):
        return 5 * 0.15 * (0.2969 * math.sqrt(u) - 0.1260 * u - 0.3516 * u ** 2 + 0.2843 * u ** 3 - 0.1036 * u ** 4)

    n = 40
    us = [(1 - math.cos(math.pi * i / n)) / 2 for i in range(n + 1)]
    up = [(-chord / 2 + chord * u, -chord * (cam(u) + th(u))) for u in us]
    lo = [(-chord / 2 + chord * u, -chord * (cam(u) - th(u))) for u in reversed(us)]
    g = F.poly([rot(x, y) for x, y in up + lo], J.BG2, INK, 6, close=True)
    if flap:
        fx = chord / 2
        pts = [(fx - 10, 4), (fx + 0.28 * chord, 0.12 * chord), (fx + 0.27 * chord, 0.15 * chord), (fx - 14, 18)]
        g += F.poly([rot(x, y) for x, y in pts], J.AMBER, J.AMBER, 4, close=True)
    return g


# ── 第6章 c703 フラップ（翼のうしろから出す板）
C703 = [
    _at(_c(0, R, head="フラップ", lines="翼のうしろから出す板", sub="ゆっくり飛べるように", cap=46), 1480, 330),
    _at(_c(1, R, head="高さ", big="約80メートル", lines="レバーを「2」に", bcap=64, cap=46), 1480, 680),
]
VIEWS["c703"] = _z(2, "着水の前の操作", "機長の指示", C703, [
    _p(0, lambda: _wing(600.0, 560.0, 700.0, 0.0, flap=True) + _t(1000.0, 740.0, "出した板", 40, J.AMBER, "middle", 240))],
    src=S_R, note="模式・板の形と角度は描いた形でない", schem=True)


# ── c705 速さの線（いちばん遠くまで滑れる速さ・機体が示す下限の速さ・実際の速さ＝高さの差は模式）
def _c705_lines():
    g = F.line(300.0, 430.0, 1560.0, 430.0, J.LINE, 5, dash="18 12") + _t(300.0, 405.0, "遠くまで滑る速さ", 38, J.LINE, "start", 700)
    return g + F.line(300.0, 560.0, 1560.0, 560.0, J.TICK, 5, dash="18 12") + _t(300.0, 530.0, "機体が示す下限の速さ", 38, J.TICK, "start", 600)


def _c705_pts(i):
    # 🔧 試し焼き（11-11）：黄の線が「機体が示す下限の速さ」の字の下の端を横切った＝下限の線（y 560）の上か少し下（報告書 at VLS or slightly less）
    return 300.0 + 12.0 * i, 566.0 + 8.0 * math.sin(i / 6.0) + (max(0, i - 87) * 3.4)


def _c705_speed(last=False):
    rng = range(87, 106) if last else range(0, 88)
    pts = [_c705_pts(i) for i in rng]
    g = F.poly(pts, "none", J.AMBER, 7)
    if last:
        g += _t(pts[-1][0] + 16, pts[-1][1] + 14, "実際の速さ", 38, J.AMBER, "start", 260)
    return g


C705 = [
    _at(_c(0, R, head="降りるあいだの大部分", lines="滑れる速さより遅い", cap=46), 560, 760),
    _at(_c(1, R, head="最後の約60メートル", lines="下限より時速約30キロ遅い", cap=46), 1340, 760),
]
VIEWS["c705"] = _z(2, "足りなかった速さ", "降りていくあいだ", C705, [
    _p(0, _c705_lines), _p(0, _c705_speed), _p(1, lambda: _c705_speed(True))],
    src=S_R, note="模式・線の高さと速さの差は描いた形でない", schem=True)

# ── c711 迎え角（翼が空気に当たる角度）と迎え角の守り
# 🔧 試し焼き（11-11）：「迎え角」の字と水平の破線が空気の流れの矢印に重なった・弧が小さかった＝翼を右へ・角度 20度・弧を大きく・矢印は下へ
AOA = (900.0, 580.0, 700.0, 20.0)       # 翼の真ん中・弦の長さ・角度（模式）


def _c711_le():
    cx, cy, ch, ang = AOA
    a = math.radians(ang)
    return cx - ch / 2 * math.cos(a), cy - ch / 2 * math.sin(a)


def _c711_wing():
    cx, cy, ch, ang = AOA
    g = _wing(cx, cy, ch, ang)
    lx, ly = _c711_le()
    for y in (ly + 150.0, ly + 220.0):
        g += _arrow(120.0, y, 330.0, y, J.TICK, 5, 18)
    return g + _t(225.0, ly + 290.0, "空気の流れ", 38, J.TICK, "middle", 260)


def _c711_angle():
    cx, cy, ch, ang = AOA
    a = math.radians(ang)
    lx, ly = _c711_le()
    g = F.line(lx - 300.0 * math.cos(a), ly - 300.0 * math.sin(a), lx, ly, J.AMBER, 4, dash="10 10")
    g += F.line(lx - 300.0, ly, lx, ly, J.TICK, 4, dash="10 10")
    arc = [(lx - 260.0 * math.cos(math.radians(t)), ly - 260.0 * math.sin(math.radians(t))) for t in range(0, int(ang) + 1, 2)]
    return g + F.poly(arc, "none", J.AMBER, 6) + _t(lx - 285.0, ly - 30.0, "迎え角", 40, J.AMBER, "end", 200)


C711 = [
    _at(_c(1, R, head="迎え角", lines="翼が空気に当たる角度", cap=46), 1480, 300),
    _at(_c(2, R, head="迎え角の守り", lines="大きくなりすぎないよう", sub="操縦をおさえる", cap=46), 1480, 520),
]
VIEWS["c711"] = _z(3, "操縦の制限", "翼と空気の角度", C711, [
    _p(0, _c711_wing), _p(1, _c711_angle)],
    src=S_R, note="模式・角度は描いた形でない", schem=True)

# ── 第9章 ca04 偶然の1つ目と2つ目（1つ目は前のカットのおさらい＝影の札）
FU["ca04"] = _f(2, "報告書が挙げたこと", "重なった偶然", [
    _c(0, R, head="1つ目", lines="よい見通しと穏やかな水面", dim=True, cell=(0, 0)),
    _c(0, R, head="2つ目", lines="とても経験のある乗員", cell=(1, 0))], src=S_R)
# ── 第10章 cb13 救命胴衣の勧告（A-10-085）
FU["cb13"] = _f(2, "着けやすさの見直し", "閉じるまで", [
    _c(0, R, head="勧告", lines="救命胴衣の決まり", sub="すばやく正しく着ける", cell=(0, 0)),
    _c(1, R, head="2018年", lines="受け入れられる対応", sub="勧告は閉じた", cell=(1, 0))],
    src=S_R + "・NTSB の勧告の記録（CAROL）")


# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-11-11）：模式 後半28＋型の図23（第1〜11章の残り＝51カット）。
#  🔴 言い切らない線＝台本の画の欄と出典の欄の字の範囲だけ。数と原文は報告書の字の層（`ref/ep32/src/ntsb/AAR1003.txt`）・
#     書き起こしの付録（p189〜p196）・勧告の控え（`src/carol/carol_dca09ma026.json`＝2026-11-09）・連邦官報（`src/web/fr2023_06413.txt`）に
#     11-11 に当てた（記録は check_mech.REC_M32）。換算＝1フィート 0.3048メートル・1ノット 1.852キロ毎時・1ポンド 0.4536キロ・華氏は (F−32)÷1.8。
#  型の図（帯・時計・比べ・並べ・線・年表・表・棒・割合・箱）は 31本目の型の図（c205 帯・c216 年表・c702 表）の形＝見え方の表に札と部品を座標で置く。
#     比例の図は門番 ⑤ が字の数から位置を自分で測る（tl＝num・hms・ym）。比例でない絵だけ「模式」の札（schem）
# ══════════════════════════════════════════════════════════
S_CAROL = "NTSB の勧告の記録（CAROL・2026年11月に取り込み）"
S_FR = "連邦官報 2023-06413（2023年4月4日）"


def _lx(ax, v):
    """値 v を線の x へ（ax＝((v0, x0), (v1, x1))＝門番 ⑤ の tl と同じ形・描く側はこの直線の式だけ）。"""
    (v0, x0), (v1, x1) = ax
    return x0 + (v - v0) * (x1 - x0) / (v1 - v0)


def _hline(ax, y, step, x_from=None, x_to=None):
    """目盛りの線（字なし）。"""
    (v0, x0), (v1, x1) = ax
    g = F.line(x0 if x_from is None else x_from, y, x1 if x_to is None else x_to, y, J.TICK, 5)
    lo, hi = min(v0, v1), max(v0, v1)
    v = lo
    while v <= hi + 1e-9:
        x = _lx(ax, v)
        g += F.line(x, y - 14, x, y + 14, J.TICK, 4)
        v += step
    return g


def _ev(x, axy, tm, words, up=True, lx=None, gap=58.0):
    """年表の出来事（点・細い線・時刻＝黄・語＝白）。up＝線の上に字・lx＝字の真ん中の x（点と違うときは斜めの線）。"""
    lx = x if lx is None else lx
    rows = ([(tm, 34, J.AMBER)] if tm else []) + [(w, 38, INK) for w in words]
    hh = 46.0 * len(rows)
    y_top = axy - gap - hh if up else axy + gap
    y_bot = y_top + hh
    g = F.line(x, axy, lx, (y_bot + 4) if up else (y_top - 4), J.TICK, 3) + F.circ(x, axy, 10, INK)
    yy = y_top
    for t, cap, col in rows:
        g += _t(lx, yy + 36, t, cap, col, "middle", 440)
        yy += 46.0
    return g


def _sq(x, y, w, fill=None, stroke=None, op=None, dash=None):
    """箱の図の四角（1つが1つ＝数え切れる）。"""
    if fill:
        return F.rect(x, y, w, w, fill, None, None, rx=8, op=op)
    return F.rect(x, y, w, w, "none", stroke or J.TICK, 4, rx=8, dash=dash)


def _hbar(ax, v, y, col, h=44.0, op=0.85, v0=0.0):
    """横の棒（v0 から v まで）。"""
    xa, xb = _lx(ax, v0), _lx(ax, v)
    return F.rect(min(xa, xb), y - h / 2, abs(xb - xa), h, col, None, None, rx=6, op=op)


def _obar(ax, v, y, h=44.0):
    """横の棒の外枠（全体の数）。"""
    xa, xb = _lx(ax, 0.0), _lx(ax, v)
    return F.rect(xa, y - h / 2, xb - xa, h, "none", J.TICK, 4, rx=6, dash="12 8")


# ── 第1章 c210 75機のうち20機（1つの四角が1機＝数え切れる）
SQ210 = (800.0, 330.0, 52.0, 12.0)        # 左上の x・y・四角の辺・すき間（15列×5行）


def _c210_sq(fill=False):
    x0, y0, w, gp = SQ210
    g = ""
    for i in range(75):
        x, y = x0 + (i % 15) * (w + gp), y0 + (i // 15) * (w + gp)
        if fill and i < 20:
            g += _sq(x, y, w, fill=J.AMBER, op=0.92)
        elif not fill:
            g += _sq(x, y, w, stroke=J.TICK)
    return g


C210 = [
    _at(_c(1, R, head="この便", lines="積む決まりなし", cap=46), 420, 400),
    _at(_c(2, R, big="20機", lines="装備のある機", sub="A320 75機のうち", bcap=72, cap=46), 420, 650),
]
VIEWS["c210"] = _z(3, "海の上の備え", "会社の中で", C210, [
    _p(1, _c210_sq), _p(2, lambda: _c210_sq(True) + _tie(C210[1], SQ210[0] - 12, 362.0))],
    src=S_R, note="1つの四角が1機（会社の A320）")

# ── c214 上昇の帯（高さの比例＝門番 ⑤ num）。左が地上
AX214 = ((0.0, 300.0), (5000.0, 1650.0))
Y214 = 640.0
C214 = [
    _at(_c(0, R, head="出発の管制へ", big="15:25:51", lines="約210メートル", bcap=64, cap=46), 520, 380),
    _at(_c(1, R, head="管制の指示", big="約4,600メートル", lines="まで上がる", bcap=64, cap=46), 1460, 380),
]
VIEWS["c214"] = _z(2, "上昇の指示", "離陸して", C214, [
    _p(0, lambda: _hline(AX214, Y214, 1000.0) + _t(300.0, Y214 + 66, "地上", 38, J.TICK, "middle", 160)
       + _t(1650.0, Y214 + 66, "高さ", 38, J.TICK, "middle", 160) + _lead(C214[0], _lx(AX214, 210.0), Y214)),
    _p(1, lambda: _arrow(_lx(AX214, 210.0), Y214 - 40, _lx(AX214, 4600.0), Y214 - 40, J.AMBER, 8, 28, "18 12")
       + _lead(C214[1], _lx(AX214, 4600.0), Y214), arrow=True)],
    src=S_R, note="高さは比例・目盛りは1,000メートルごと",
    tl=dict(kind="num", ax=AX214, pts=(("約210メートル", _lx(AX214, 210.0)), ("約4,600メートル", _lx(AX214, 4600.0)))))


# ── 第2章 c301 時計（針は 15:27:10 の位置＝式で置く・文字盤の数は 12・3・6・9 だけ）
def _clock(cx, cy, r, h, m, s):
    g = F.circ(cx, cy, r, J.BG2, None, None, op=0.6) + F.circ(cx, cy, r, "none", INK, 6)
    for i in range(60):
        a = math.radians(i * 6)
        big = i % 5 == 0
        r0 = r - (34 if big else 16)
        g += F.line(cx + r0 * math.sin(a), cy - r0 * math.cos(a), cx + (r - 8) * math.sin(a), cy - (r - 8) * math.cos(a),
                    J.AMBER if i == 0 else (INK if big else J.TICK), 6 if big else 3)
    for n, deg in (("12", 0), ("3", 90), ("6", 180), ("9", 270)):
        a = math.radians(deg)
        g += _t(cx + (r - 70) * math.sin(a), cy - (r - 70) * math.cos(a) + 16, n, 44, INK, "middle", 100)
    ah = math.radians(((h % 12) + m / 60.0 + s / 3600.0) * 30.0)
    am = math.radians((m + s / 60.0) * 6.0)
    asec = math.radians(s * 6.0)
    g += F.line(cx, cy, cx + r * 0.5 * math.sin(ah), cy - r * 0.5 * math.cos(ah), INK, 14)
    g += F.line(cx, cy, cx + r * 0.78 * math.sin(am), cy - r * 0.78 * math.cos(am), INK, 9)
    g += F.line(cx, cy, cx + r * 0.84 * math.sin(asec), cy - r * 0.84 * math.cos(asec), J.AMBER, 4)
    return g + F.circ(cx, cy, 12, J.AMBER)


C301 = [_at(_c(0, R, head="機長", big="15:27:10", lines="鳥だ", q=True, bcap=72, cap=56), 1350, 540)]
VIEWS["c301"] = _z(2, "最初の一言", "操縦室の録音", C301, [_p(0, lambda: _clock(700.0, 545.0, 270.0, 15, 27, 10.4))],
                   src=S_R, note="針は15時27分10秒の位置")

# ── c306 ガンの重さ（キロの比例＝門番 ⑤ num・2本の線＝幅の頭と尻）
AX306 = ((0.0, 300.0), (5.0, 1600.0))
YR306 = (520.0, 680.0)


def _c306_row(i, lo, hi, lab, txt):
    y = YR306[i]
    g = F.line(_lx(AX306, 0.0), y, _lx(AX306, lo), y, J.TICK, 3, dash="6 10")
    g += _hbar(AX306, hi, y, J.AMBER, v0=lo) + _t(280.0, y + 14, lab, 40, INK, "end", 160)
    # 字は 3.6キロの印の線（x 1236）を避ける＝オスは棒の右・メスは棒の左
    if i == 0:
        return g + _t(_lx(AX306, hi) + 20, y + 16, txt, 44, J.AMBER, "start", 420)
    return g + _t(_lx(AX306, lo) - 20, y + 16, txt, 44, J.AMBER, "end", 420)


def _c306_mark():
    x = _lx(AX306, 3.6)
    return F.line(x, 470.0, x, 730.0, J.LINE, 5, dash="14 10")


C306 = [_at(_c(1, R, head="報告書の見立て", lines="約3.6キロのガン", sub="少なくとも2羽ずつ", cap=46), 600, 330)]
VIEWS["c306"] = _z(2, "ガンの重さ", "オスとメス", C306, [
    _p(0, lambda: _hline(AX306, 780.0, 1.0) + _c306_row(0, 3.8, 4.2, "オス", "約3.8〜4.2キロ") + _c306_row(1, 3.3, 3.5, "メス", "約3.3〜3.5キロ")),
    _p(1, lambda: _c306_mark() + _lead(C306[0], _lx(AX306, 3.6), 470.0))],
    src=S_R, note="重さは比例・目盛りは1キロごと・ポンドをキロに換算",
    tl=(dict(kind="num", ax=AX306, pts=(("約3.8〜4.2キロ", _lx(AX306, 3.8)), ("約3.3〜3.5キロ", _lx(AX306, 3.3)), ("約3.6キロ", _lx(AX306, 3.6)))),
        dict(kind="num", ax=AX306, pts=(("4.2キロ", _lx(AX306, 4.2)), ("3.5キロ", _lx(AX306, 3.5))))))

# ── c307 試験の鳥と当たったガン（キロの比例＝門番 ⑤ num）
AX307 = ((0.0, 300.0), (4.0, 1380.0))
YR307 = (500.0, 690.0)
C307 = [
    _at(_c(0, R, head="認められたときの試験", big="約1.8キロ", lines="1羽", bcap=64, cap=46), 1150, 380),
    _at(_c(1, R, head="吸い込んだガン", big="約3.6キロ", lines="約2倍の重さ", bcap=64, cap=46), 1580, 690),
]
VIEWS["c307"] = _z(2, "試験と実際", "大きな鳥の基準", C307, [
    _p(0, lambda: _hline(AX307, 820.0, 1.0) + _hbar(AX307, 1.8, YR307[0], J.LINE) + _t(300.0, YR307[0] - 40, "試験の鳥", 40, INK, "start", 300)
       + _tie(C307[0], _lx(AX307, 1.8), YR307[0])),
    _p(1, lambda: _hbar(AX307, 3.6, YR307[1], J.AMBER) + _t(300.0, YR307[1] - 40, "ガン", 40, INK, "start", 200))],
    src=S_R, note="棒の長さは重さの比例・目盛りは1キロごと",
    tl=dict(kind="num", ax=AX307, pts=(("約1.8キロ", _lx(AX307, 1.8)), ("約3.6キロ", _lx(AX307, 3.6)))))

# ── c308 回る速さ（%の比例＝門番 ⑤ num）。82% の外枠から 35%・15% へ
AX308 = ((0.0, 440.0), (100.0, 1640.0))
YR308 = (420.0, 590.0)


def _c308_row(i, to, lab):
    y = YR308[i]
    x82, xt = _lx(AX308, 82.0), _lx(AX308, to)
    g = _obar(AX308, 82.0, y) + _hbar(AX308, to, y, J.AMBER) + _t(420.0, y + 14, lab, 40, INK, "end", 340)
    g += _t(x82 + 18, y + 14, "82%", 40, J.TICK, "start", 160) + _t(xt + 18, y + 14, f"{to:.0f}%", 44, J.AMBER, "start", 160)
    return g + _arrow(x82 - 10, y - 46, xt + 90, y - 46, J.AMBER, 6, 22)


C308 = [_at(_c(1, R, head="どちらも", lines="押す力はほぼ残らない", cap=46), 1080, 770)]
VIEWS["c308"] = _z(3, "落ちた回転", "ぶつかった直後", C308, [
    _p(0, lambda: _hline(AX308, 660.0, 25.0) + _t(440.0, 320.0, "エンジンの回る速さ", 38, J.TICK, "start", 500) + _c308_row(0, 35.0, "左のエンジン"), arrow=True),
    _p(1, lambda: _c308_row(1, 15.0, "右のエンジン"), arrow=True)],
    src=S_R, note="棒の長さは比例・目盛りは25%ごと",
    tl=dict(kind="num", ax=AX308, pts=(("82%", _lx(AX308, 82.0)), ("35%", _lx(AX308, 35.0)), ("15%", _lx(AX308, 15.0)))))

# ── c323 約2分の帯（秒の比例＝門番 ⑤ hms）
AX323 = ((_hs(15, 27, 0), 240.0), (_hs(15, 30, 0), 1680.0))
Y323 = 600.0
C323 = [
    _at(_c(0, R, big="15:27:33", lines="管制へ第一報", bcap=64, cap=46), 504, 380),
    _at(_c(1, R, big="15:29:28", lines="ハドソン川に降りる", q=True, bcap=64, cap=46), 1424, 380),
]


def _c323_span():
    xa, xb = _lx(AX323, _hs(15, 27, 33)), _lx(AX323, _hs(15, 29, 28))
    g = F.line(xa, Y323 + 60, xb, Y323 + 60, J.AMBER, 7) + F.line(xa, Y323 + 44, xa, Y323 + 76, J.AMBER, 5) + F.line(xb, Y323 + 44, xb, Y323 + 76, J.AMBER, 5)
    return g + _t((xa + xb) / 2, Y323 + 130, "約2分", 52, J.AMBER, "middle", 300)


VIEWS["c323"] = _z(2, "管制とのやりとり", "手順書と並んで", C323, [
    _p(0, lambda: _hline(AX323, Y323, 30.0) + _lead(C323[0], _lx(AX323, _hs(15, 27, 33)), Y323)),
    _p(1, lambda: _lead(C323[1], _lx(AX323, _hs(15, 29, 28)), Y323) + _c323_span())],
    src=S_R, note="目盛りは30秒ごと",
    tl=dict(kind="hms", ax=AX323, pts=(("15:27:33", _lx(AX323, _hs(15, 27, 33))), ("15:29:28", _lx(AX323, _hs(15, 29, 28))))))

# ── 第3章 c407 よく言われる話と記録の言葉（灰色の噂の札は使わない＝画の欄）
FU["c407"] = _f(3, "断ったのか", "記録の言葉", [
    _c(0, None, head="よく言われる話", lines="管制の指示を断った", cell=(0, 0)),
    _c(1, R, lines="unable", q=True, sub="できない", cell=(1, 0)),
    _c(1, R, lines="we can't do it", q=True, sub="無理だ", cell=(1, 1)),
    _c(2, R, head="滑走路13のとき", lines="降りるかの問い", cell=(0, 1))],
    [_x(1, "a", "b", t="記録では")], src=S_R)

# ── c422 交信の並び（秒の比例＝門番 ⑤ hms）。字は話した人の行の時刻（書き起こし p189〜p196・15:28:11 は本文 p105 の字）
AX422 = ((_hs(15, 27, 0), 240.0), (_hs(15, 30, 0), 1680.0))
Y422 = 560.0
EV422 = (  # 時刻・語・上か・字の x のずれ
    ((15, 27, 33), "15:27:33", ("ラガーディアへ", "戻る"), True, 0.0),
    ((15, 28, 11), "15:28:11", ("滑走路13は", "できない"), False, 0.0),
    ((15, 28, 35), "15:28:35", ("滑走路31も", "できない"), True, 0.0),
    ((15, 28, 50), "15:28:50", ("滑走路4も", "届くか分からない"), False, 0.0),
    ((15, 29, 25), "15:29:25", ("テターボロも", "無理だ"), True, -40.0),
    ((15, 29, 28), "15:29:28", ("ハドソン川に", "降りる"), False, 90.0),
)


def _c422_ev(*ii):
    g = ""
    for i in ii:
        hms, tm, ws, up, dx = EV422[i]
        x = _lx(AX422, _hs(*hms))
        g += _ev(x, Y422, tm, ws, up=up, lx=x + dx)
    return g


C422 = [_at(_c(2, R, head="鳥とぶつかってから", big="2分17秒", bcap=64), 420, 720)]
VIEWS["c422"] = _z(3, "消えていった案", "交信の並び", C422, [
    _p(0, lambda: _hline(AX422, Y422, 30.0) + F.circ(_lx(AX422, _hs(15, 27, 11)), Y422, 10, J.TICK)
       + _t(_lx(AX422, _hs(15, 27, 11)), Y422 - 34, "鳥", 36, J.TICK, "middle", 80) + _c422_ev(0)),
    _p(1, lambda: _c422_ev(1, 2, 3)), _p(2, lambda: _c422_ev(4, 5))],
    src=S_R, note="目盛りは30秒ごと・時刻は話した人の行",
    tl=dict(kind="hms", ax=AX422, pts=tuple((e[1], _lx(AX422, _hs(*e[0]))) for e in EV422)))

# ── 第4章 c505 試しの数（20回 → 5回を外す → 15回＝行き先ごとの表）
C505 = [
    _at(_c(0, R, head="試し", big="20回", bcap=72), 360, 330),
    _at(_c(0, R, head="残り", big="15回", bcap=72), 1560, 330),
]
TY505 = (560.0, 650.0, 740.0)
R505 = (("ラガーディア", "滑走路22", "6回"), ("ラガーディア", "滑走路13", "7回"), ("テターボロ", "滑走路19", "2回"))


def _c505_flow():
    a, b = _zbox(C505[0]), _zbox(C505[1])
    g = _arrow(a[0] + a[2] + 16, 330.0, b[0] - 16, 330.0, J.LINE, 8, 28)
    # 🔧 check_echo：「記録の不具合などで5回を外す」は語りと 93% 一致＝報告書の poor data or simulator malfunctions の訳に
    mx = (a[0] + a[2] + b[0]) / 2
    return g + _t(mx, 300.0, "5回を外す", 40, J.LINE, "middle", 400) + _t(mx, 386.0, "データや装置の不具合", 32, J.TICK, "middle", 500)


def _c505_table():
    # 🔧 check_slide G-14：地 gm1 の画面の焼き込みの字（画面 x 992〜1106・y 566〜620）に「滑走路22」が載った＝列を右へ（x 1000 → 1220）
    g = _t(560.0, 492.0, "行き先", 36, J.TICK, "middle", 300) + _t(1220.0, 492.0, "滑走路", 36, J.TICK, "middle", 300) + _t(1480.0, 492.0, "回数", 36, J.TICK, "middle", 200)
    g += "".join(F.line(360.0, y + 45, 1600.0, y + 45, J.TICK, 3, op=0.7) for y in TY505[:2])
    for y, (a, b, n) in zip(TY505, R505):
        g += _t(560.0, y + 16, a, 44, INK, "middle", 380) + _t(1220.0, y + 16, b, 44, INK, "middle", 300) + _t(1480.0, y + 20, n, 52, J.AMBER, "middle", 200)
    return g


VIEWS["c505"] = _z(2, "試しの数", "行き先ごと", C505, [_p(0, _c505_flow, arrow=True), _p(1, _c505_table)],
                   src=S_R, note="エンジニアのシミュレーターの試し")

# ── c506 降りられた回数（回数の比例＝門番 ⑤ num・2本の線＝全体の回数と降りられた回数）
AX506 = ((0.0, 640.0), (8.0, 1600.0))
R506 = ((330.0, "滑走路22", 6, 2), (440.0, "滑走路13", 7, 5), (550.0, "テターボロ", 2, 1))


def _c506_bars():
    g = _hline(AX506, 620.0, 1.0)
    for y, lab, n, ok in R506:
        g += _obar(AX506, float(n), y) + _hbar(AX506, float(ok), y, J.AMBER) + _t(610.0, y + 14, lab, 40, INK, "end", 340)
        g += _t(_lx(AX506, float(n)) + 18, y + 14, f"{n}回中{ok}回", 40, INK, "start", 260)
    return g


C506 = [
    _at(_c(0, R, big="8回・53%", lines="15回のうち降りられた", bcap=64, cap=46), 760, 760),
    _at(_c(1, R, head="いちばん多い", lines="滑走路13", cap=46), 1420, 760),
]
VIEWS["c506"] = _z(2, "結果の内訳", "滑走路ごと", C506, [
    _p(0, _c506_bars), _p(1, lambda: F.rect(390.0, 440.0 - 40, 230.0, 80.0, "none", J.AMBER, 6, rx=14))],
    src=S_R, note="棒の長さは回数の比例・枠は試しの回数",
    tl=(dict(kind="num", ax=AX506, pts=tuple((f"{n}回中{ok}回", _lx(AX506, float(n))) for _y, _l, n, ok in R506)),
        dict(kind="num", ax=AX506, pts=tuple((f"中{ok}回", _lx(AX506, float(ok))) for _y, _l, n, ok in R506))))

# ── 第5章 c607 前提の高さ（メートルの比例＝門番 ⑤ num）
AX607 = ((0.0, 360.0), (7000.0, 1660.0))
YR607 = (420.0, 590.0)
C607 = [_at(_c(1, R, head="前提の高さの", big="約7分の1", bcap=72), 1320, 770)]


def _c607_row(i):
    y = YR607[i]
    if i == 0:
        x = _lx(AX607, 6100.0)
        g = _hbar(AX607, 6100.0, y, J.LINE) + _arrow(x + 6, y, 1700.0, y, J.LINE, 6, 22, "12 10")
        g += _t(360.0, y - 40, "手順書の前提", 40, INK, "start", 400) + _t(x, y - 40, "約6,100メートル", 44, J.LINE, "middle", 400)
        return g + _t(1700.0, y + 64, "より上", 40, J.LINE, "end", 200)
    x = _lx(AX607, 860.0)
    return _hbar(AX607, 860.0, y, J.AMBER) + _t(360.0, y - 40, "1549便", 40, INK, "start", 300) + _t(x + 20, y + 16, "約860メートル", 44, J.AMBER, "start", 400)


VIEWS["c607"] = _z(2, "想定した高さ", "鳥とぶつかった所", C607, [
    _p(0, lambda: _hline(AX607, 650.0, 1000.0) + _c607_row(1)), _p(1, lambda: _c607_row(0))],
    src=S_R, note="棒の長さは高さの比例・目盛りは1,000メートルごと",
    tl=dict(kind="num", ax=AX607, pts=(("約6,100メートル", _lx(AX607, 6100.0)), ("約860メートル", _lx(AX607, 860.0)))))


# ── c615 たどれた所（c603・c614 と同じ3ページの絵・1ページ目を塗る＝全体の3分の1）
def _c615_all():
    x0, x1 = PG[0][0], PG[2][0] + PW
    g = F.line(x0, 266.0, x1, 266.0, J.TICK, 5) + F.line(x0, 266.0, x0, 286.0, J.TICK, 5) + F.line(x1, 266.0, x1, 286.0, J.TICK, 5)
    return g + _t((x0 + x1) / 2, 250.0, "全体", 38, J.TICK, "middle", 200)


C615 = [_at(_c(0, R, head="手順書の全体のうち", big="約3分の1", bcap=72), 1480, 480)]
VIEWS["c615"] = _z(2, "たどれた所", "報告書の見方", C615, [_p(0, _pages), _p(0, _c614_paint), _p(0, _c615_all)],
                   src=S_R, note="模式・ページの区切りは描いた形でない・塗りは全体の3分の1", schem=True)

# ── c624 APU の効き目（流れ）
FU["c624"] = _f(3, "APU の効き目", "電気と守り", [
    _c(0, R, head="APU", lines="電気をつくる", cell=(0, 0)),
    _c(0, R, head="ふだんの制御の形", lines="ノーマル・ロー", cell=(1, 0)),
    _c(1, R, head="失速を防ぐ守り", lines="働き続ける", cell=(2, 0)),
    _c(2, R, head="失速とは", lines="翼が空気の力を失う", cell=(0, 1), span=(3, 1))],
    [_x(0, "a", "b"), _x(1, "b", "c")], src=S_R)

# ── 第6章 c707 鳴らなかった警報
FU["c707"] = _f(2, "消えた知らせ", "警報の順番", [
    _c(0, R, head="速さが遅すぎる警報", lines="鳴らなかった", cell=(0, 0)),
    _c(0, R, head="地面に近い警報", lines="優先された", cell=(1, 0)),
    _c(1, R, big="15回", lines="約85秒で", cell=(1, 1))],
    [_x(0, "b", "a", t="優先")], src=S_R)
# ── c709 地面の警報（原文どおり＝字幕を消す）
FU["c709"] = _f(2, "地面の警報", "最後の録音", [
    _c(0, R, big="15:30:24", lines="地面、地面、機首を上げろ", q=True, cell=(0, 0)),
    _c(1, R, head="機首を上げろ", lines="録音が終わるまで", sub="くり返された", cell=(1, 0))], src=S_R, mute=(0,))
# ── c712 守りが働いた高さ（高さの比例＝門番 ⑤ num・左が高い・右が水面）
AX712 = ((60.0, 300.0), (0.0, 1620.0))
C712 = [
    _at(_c(0, R, head="迎え角の守り", lines="約45メートルから下", cap=46), 560, 300),
    _at(_c(1, R, head="エアバスの再現", lines="約30メートルから下", cap=46), 1250, 300),
]


def _c712_band(v, y, col, txt):
    xa, xb = _lx(AX712, v), _lx(AX712, 0.0)
    g = F.rect(xa, y - 30, xb - xa, 60, col, None, None, rx=10, op=0.28) + F.rect(xa, y - 30, xb - xa, 60, "none", col, 5, rx=10)
    return g + _t(xa + 24, y + 14, txt, 38, INK, "start", xb - xa - 40) + F.line(xa, y + 30, xa, 660.0, col, 3, dash="8 8")


VIEWS["c712"] = _z(2, "守りが働いた高さ", "水面に近づいて", C712, [
    _p(0, lambda: _hline(AX712, 660.0, 10.0) + _t(1620.0, 726.0, "水面", 38, J.TICK, "middle", 160) + _t(300.0, 726.0, "高さ", 38, J.TICK, "middle", 160)
       + _c712_band(45.0, 550.0, J.AMBER, "守りが働く") + _lead(C712[0], _lx(AX712, 45.0), 520.0)),
    _p(1, lambda: _c712_band(30.0, 440.0, J.LINE, "機首上げが効きにくい") + _lead(C712[1], _lx(AX712, 30.0), 410.0))],
    src=S_R, note="高さは比例・目盛りは10メートルごと",
    tl=dict(kind="num", ax=AX712, pts=(("約45メートル", _lx(AX712, 45.0)), ("約30メートル", _lx(AX712, 30.0)))))
# ── c713 守りのよい面（前の c712 の弱める面は影の札）
FU["c713"] = _f(3, "守りのよい面", "報告書の分析", [
    _c(0, R, head="守りの別の面", lines="機首上げの効きを弱めた", dim=True, cell=(0, 0), span=(2, 1)),
    _c(0, R, head="その重さと形で", lines="いちばんの性能", cell=(0, 1)),
    _c(1, R, head="守りのおかげ", lines="失速の心配なく引けた", cell=(1, 1))], src=S_R)
# ── c715 着水の姿（横から見た機体＝機首の角度は比例・ほかは模式）
WY715 = 640.0
T715 = (520.0, 980.0, 120.0, 9.5)          # 尾が水面に着く点の x・長さ・高さ・機首の上げ（度）


def _r715(x, y):
    tx, _L, _H, ang = T715
    a = math.radians(ang)
    return tx + x * math.cos(a) + y * math.sin(a), WY715 - x * math.sin(a) + y * math.cos(a)


def _c715_body():
    _tx, L, H, _a = T715
    nose = [(L - 60 + 60 * math.cos(math.radians(t)), -H / 2 + (H / 2) * math.sin(math.radians(t))) for t in range(90, -91, -10)]
    body = [(0.0, 0.0)] + nose + [(40.0, -H), (0.0, -H + 24)]
    fin = [(10.0, -H), (170.0, -H), (60.0, -H - 130), (14.0, -H - 130)]
    g = F.line(160.0, WY715, 1760.0, WY715, J.LINE, 5, dash="20 12") + _t(1760.0, WY715 + 50, "水面", 38, J.LINE, "end", 160)
    g += F.poly([_r715(x, y) for x, y in body], J.BG2, INK, 6, close=True) + F.poly([_r715(x, y) for x, y in fin], J.BG2, INK, 5, close=True)
    arc = [(T715[0] + 380 * math.cos(math.radians(t / 10)), WY715 - 380 * math.sin(math.radians(t / 10))) for t in range(0, 96, 5)]
    return g + F.poly(arc, "none", J.AMBER, 6)


def _c715_moves():
    _tx, L, H, _a = T715
    (x1, y1), (x2, y2) = _r715(L + 40, -H / 2), _r715(L + 260, -H / 2)
    return _arrow(x1, y1, x2, y2, J.AMBER, 8, 28) + _arrow(430.0, 470.0, 430.0, 610.0, J.AMBER, 8, 28)


C715 = [
    _at(_c(0, R, head="着水", big="15:30:43", bcap=64), 300, 300),
    _at(_c(0, R, head="機首の上げ", big="9.5度", bcap=64), 1150, 770),
    _at(_c(0, R, head="速さ", big="時速約230キロ", bcap=64), 1560, 770),
    _at(_c(1, R, head="沈む速さ", big="毎秒約3.8メートル", bcap=64), 420, 770),
]
VIEWS["c715"] = _z(2, "着水の姿", "水面に着いたとき", C715, [
    _p(0, _c715_body), _p(0, _c715_moves, arrow=True),
    _p(0, lambda: _lead(C715[1], T715[0] + 380 * math.cos(math.radians(4.75)), WY715 - 380 * math.sin(math.radians(4.75)))
       + _lead(C715[2], _r715(T715[1] + 150, -T715[2] / 2)[0], _r715(T715[1] + 150, -T715[2] / 2)[1] + 4)),
    _p(1, lambda: _lead(C715[3], 430.0, 612.0))],
    src=S_R, note="模式・機体の形と矢印の長さは描いた形でない・機首の角度は比例", schem=True)
# ── c719 客室乗務員のけが
FU["c719"] = _f(2, "客室乗務員のけが", "後ろの席", [
    _c(0, R, head="傷", lines="左のすね", cell=(0, 0)),
    _c(0, R, head="長さ", big="12センチ", cell=(1, 0)),
    _c(0, R, head="深さ", big="5センチ", cell=(2, 0)),
    _c(1, R, lines="手術で閉じた", cell=(0, 1), span=(3, 1))], src=S_R)
# ── c721 前提の難しさ（所見）
FU["c721"] = _f(3, "前提の難しさ", "報告書の所見", [
    _c(0, R, head="エンジンの力なしで", lines="着水の前提をすべて", cell=(0, 0)),
    _c(1, R, lines=("ありえなくはないが", "見込みは低い"), cell=(1, 0)),
    _c(2, R, head="その難しさ", lines="胴体の損傷の一因", cell=(0, 1), span=(2, 1))],
    [_x(1, "a", "b")], src=S_R)
# ── c716 沈む速さ（毎秒メートルの比例＝門番 ⑤ num）
AX716 = ((0.0, 440.0), (4.0, 1640.0))
YR716 = (420.0, 590.0)
C716 = [
    _at(_c(1, R, big="3倍をこえる", bcap=72), 1340, 770),
    _at(_c(2, R, head="後ろの胴体に", lines="大きな水の力", cap=46), 620, 770),
]
VIEWS["c716"] = _z(3, "沈む速さ", "水に当たったとき", C716, [
    _p(0, lambda: _hline(AX716, 664.0, 1.0) + _hbar(AX716, 1.1, YR716[0], J.LINE) + _t(420.0, YR716[0] + 14, "認証の前提", 40, INK, "end", 340)
       + _t(_lx(AX716, 1.1) + 20, YR716[0] + 16, "毎秒約1.1メートル", 44, J.LINE, "start", 500)),
    _p(1, lambda: _hbar(AX716, 3.8, YR716[1], J.AMBER) + _t(420.0, YR716[1] + 14, "1549便", 40, INK, "end", 300)
       + _t(_lx(AX716, 3.8), YR716[1] - 40, "毎秒約3.8メートル", 44, J.AMBER, "end", 500))],
    src=S_R, note="棒の長さは比例・目盛りは毎秒1メートルごと・フィートをメートルに換算",
    tl=dict(kind="num", ax=AX716, pts=(("毎秒約1.1メートル", _lx(AX716, 1.1)), ("毎秒約3.8メートル", _lx(AX716, 3.8)))))
# ── c723 損傷に関わった3つ（並べ）
FU["c723"] = _f(3, "損傷に関わった3つ", "報告書の結論", [
    _c(0, R, head="FAA の認証", lines="推力なしで届くか確かめず", cell=(0, 0)),
    _c(1, R, head="訓練と指針", lines="着水の降り方", sub="業界に足りず", cell=(1, 0)),
    _c(2, R, head="最後の進入", lines="思う速さを保ちにくい", sub="緊急で手いっぱい", cell=(0, 1), span=(2, 1))], src=S_R)

# ── 第7章 c802 開いた順（秒の比例＝門番 ⑤ hms・NTSB が映像から読んだ時刻）
AX802 = ((_hs(15, 30, 40), 240.0), (_hs(15, 31, 30), 1680.0))
Y802 = 560.0
EV802 = (
    ((15, 30, 58), "15:30:58", ("左の翼の非常口",), True),
    ((15, 31, 6), "15:31:06", ("前の左の扉",), False),
    ((15, 31, 11), "15:31:11", ("前の右の扉",), True),
    ((15, 31, 16), "15:31:16", ("前の右のすべり台", "ふくらむ"), False),
    ((15, 31, 26), "15:31:26", ("前の左のすべり台", "ふくらみ始める"), True),
)


def _c802_ev(*ii):
    return "".join(_ev(_lx(AX802, _hs(*EV802[i][0])), Y802, EV802[i][1], EV802[i][2], up=EV802[i][3]) for i in ii)


C802 = [_at(_c(0, R, head="着水", big="15:30:43", bcap=64), 360, 380)]
VIEWS["c802"] = _z(2, "開いた順", "NTSB の映像の読み", C802, [
    _p(0, lambda: _hline(AX802, Y802, 10.0) + _lead(C802[0], _lx(AX802, _hs(15, 30, 43)), Y802) + _c802_ev(0)),
    _p(1, lambda: _c802_ev(1, 2, 3, 4))],
    src=S_R, note="目盛りは10秒ごと",
    tl=dict(kind="hms", ax=AX802, pts=(("15:30:43", _lx(AX802, _hs(15, 30, 43))),) + tuple((e[1], _lx(AX802, _hs(*e[0]))) for e in EV802)))


# ── c804 閉まりかけた扉（前から見た扉の口・扉・すべり台＝模式）
def _c804_door():
    g = F.poly([(760.0, 700.0), (1060.0, 700.0), (1170.0, 850.0), (650.0, 850.0)], J.AMBER, None, close=True, op=0.22)
    g += F.poly([(760.0, 700.0), (1060.0, 700.0), (1170.0, 850.0), (650.0, 850.0)], "none", J.AMBER, 5, close=True)
    g += _t(910.0, 800.0, "すべり台", 40, INK, "middle", 300)
    # 🔧 check_box（空き矩形 47%）：扉の口は「中が空いた枠」でなく、暗い穴（塗った形）として描く
    g += F.rect(760.0, 300.0, 300.0, 400.0, J.BG2, INK, 6, rx=10) + _t(910.0, 282.0, "扉の口", 38, INK, "middle", 260)
    return g + F.rect(766.0, 306.0, 104.0, 388.0, J.TICK, J.TICK, 5, rx=6, op=0.55) + _t(818.0, 520.0, "扉", 40, INK, "middle", 80)


C804 = [
    _at(_c(0, R, head="前の右の扉", lines="途中で閉まりかけた", sub="約30センチ入り込む", cap=46), 1450, 380),
    _at(_c(1, R, head="客室乗務員の頼み", lines="力のありそうな男性", sub="扉を押さえる", cap=46), 1450, 680),
]
VIEWS["c804"] = _z(2, "扉の異変", "脱出のさなか", C804, [
    _p(0, _c804_door), _p(0, lambda: _arrow(880.0, 600.0, 990.0, 600.0, J.AMBER, 8, 28) + _tie(C804[0], 1066.0, 420.0), arrow=True)],
    src=S_R, note="模式・扉とすべり台の形は描いた形でない", schem=True)


# ── c807・c809 機体を上から（c207 と同じ筒・前＝左・上が右側）
def _sides():
    return _t(430.0, 470.0, "右", 34, J.TICK, "middle", 60) + _t(430.0, 712.0, "左", 34, J.TICK, "middle", 60)


def _exits807():
    g = ""
    for x in (930.0, 1000.0):
        for y in (BODY[2], BODY[3]):
            g += F.rect(x - 22, y - 12, 44, 24, J.TICK, None, None, rx=5)
    for y in (BODY[2], BODY[3]):
        g += F.rect(470.0 - 34, y - 14, 68, 28, J.AMBER, None, None, rx=6)
    return g


def _c807_flow():
    pts = [(965.0 + 120.0 * math.cos(math.radians(t)), 580.0 + 70.0 * math.sin(math.radians(t))) for t in range(0, 361, 15)]
    g = F.poly(pts, J.AMBER, None, close=True, op=0.22) + F.poly(pts, "none", J.AMBER, 4, close=True, dash="10 8")
    return g + _arrow(830.0, 580.0, 560.0, 580.0, J.AMBER, 10, 32)


def _c807_aft():
    return F.line(1450.0, 545.0, 540.0, 545.0, J.LINE, 5, dash="16 12") + _arrow(540.0, 545.0, 478.0, 516.0, J.LINE, 5, 22)


C807 = [
    _at(_c(0, R, head="翼の非常口", lines="混み合った", cap=46), 965, 330),
    _at(_c(0, R, head="前の扉へ", lines="呼び寄せた", cap=46), 720, 770),
    _at(_c(1, R, head="後ろの客室乗務員", lines="前の右の扉から出た", cap=46), 1300, 770),
]
VIEWS["c807"] = _z(2, "前へ呼ぶ", "人の向き", C807, [
    _p(0, lambda: _body() + _exits807() + _sides()), _p(0, _c807_flow, arrow=True),
    _p(0, lambda: _lead(C807[0], 965.0, BODY[2] - 14) + _lead(C807[1], 470.0, BODY[3] + 16)),
    _p(1, _c807_aft, arrow=True), _p(1, lambda: _lead(C807[2], 1450.0, 560.0))],
    src=S_R, note="模式・人の流れの形は描いた形でない（人は数えない）", schem=True)


def _c809_loop():
    return _arrow(560.0, 565.0, 1430.0, 565.0, J.AMBER, 6, 24, "16 12") + _arrow(1430.0, 605.0, 560.0, 605.0, J.AMBER, 6, 24, "16 12")


C809 = [
    _at(_c(0, R, head="機長と副操縦士", lines="残る人がいないか", cap=46), 960, 330),
    _at(_c(1, R, lines="前の左のすべり台へ", cap=46), 860, 790),
]
VIEWS["c809"] = _z(2, "最後の見回り", "機長の話", C809, [
    _p(0, lambda: _body() + _exits807() + _sides()), _p(0, _c809_loop, arrow=True), _p(0, lambda: _lead(C809[0], 960.0, 555.0)),
    _p(1, lambda: _arrow(470.0, 640.0, 470.0, 770.0, J.AMBER, 8, 28) + _tie(C809[1], 486.0, 760.0), arrow=True)],
    src=S_R, note="模式・見回った道の形は描いた形でない", schem=True)
# ── c813 その日の寒さ
FU["c813"] = _f(3, "その日の寒さ", "気温と水温", [
    _c(1, R, head="気温", big="マイナス7度", sub="セントラルパーク 15:51", cell=(0, 0), bcap=72),
    _c(2, R, head="川の水", big="5.2度", cell=(1, 0), bcap=72),
    _c(2, R, head="風を受けた体", big="約マイナス17度", cell=(2, 0), bcap=72)], src=S_R)


# ── c820 いかだになるすべり台（横から見た機体の前・すべり台・いかだ＝模式）
def _c820_slide():
    g = F.line(160.0, 600.0, 1760.0, 600.0, J.LINE, 5, dash="20 12") + _t(1760.0, 650.0, "水面", 38, J.LINE, "end", 160)
    g += F.rect(200.0, 380.0, 560.0, 140.0, J.BG2, INK, 6, rx=70, op=0.6) + F.rect(560.0, 400.0, 60.0, 100.0, "none", J.AMBER, 5, rx=6)
    g += F.poly([(560.0, 500.0), (620.0, 500.0), (900.0, 600.0), (820.0, 600.0)], J.AMBER, None, close=True, op=0.35)
    return g + F.line(566.0, 514.0, 626.0, 514.0, J.ALERT, 5, dash="8 6")


def _c820_raft():
    g = _arrow(930.0, 575.0, 1160.0, 585.0, J.AMBER, 8, 28)
    g += F.rect(1180.0, 560.0, 380.0, 60.0, J.AMBER, None, None, rx=30, op=0.30) + F.rect(1180.0, 560.0, 380.0, 60.0, "none", J.AMBER, 5, rx=30)
    return g + _t(1370.0, 690.0, "いかだ", 40, INK, "middle", 200)


C820 = [
    _at(_c(0, R, head="前のすべり台", lines="切り離すといかだに", cap=46), 520, 290),
    _at(_c(0, R, head="いかだ1つ", big="44人用", bcap=64), 1370, 330),
    _at(_c(1, R, head="報告書", lines="この装備が無ければ", sub="約64人のいかだは無かった", cap=46), 1000, 760),
]
VIEWS["c820"] = _z(2, "もう1つの使い道", "海の上の装備", C820, [
    _p(0, _c820_slide), _p(0, _c820_raft, arrow=True), _p(0, lambda: _lead(C820[1], 1370.0, 552.0))],
    src=S_R, note="模式・機体とすべり台といかだの形は描いた形でない", schem=True)


# ── c822 救助を待つ（川の上の機体と、近づく船の影＝数えない形）
def _c822_river():
    g = F.rect(F.BX0, 440.0, F.BW, 260.0, J.LINE, None, None, op=0.12) + F.line(F.BX0, 440.0, F.BX1, 440.0, J.TICK, 4) + F.line(F.BX0, 700.0, F.BX1, 700.0, J.TICK, 4)
    return g + _plane(820.0, 570.0, INK, k=1.5, ang=-90.0)


def _c822_ship():
    pts = [(1330.0, 575.0), (1520.0, 575.0), (1570.0, 600.0), (1520.0, 628.0), (1330.0, 628.0)]
    g = F.poly(pts, "none", J.TICK, 5, close=True, dash="12 8")
    return g + _arrow(1310.0, 600.0, 1010.0, 585.0, J.TICK, 5, 22, "14 10") + _qmark(1450.0, 540.0, 64, J.AMBER)


C822 = [_at(_c(1, R, head="最初の船", lines="何分後に着いたか", cap=46), 1420, 320)]
VIEWS["c822"] = _z(2, "救助を待つ", "川の上の機体", C822, [_p(0, _c822_river), _p(1, _c822_ship, arrow=True)],
                   src=S_R, note="模式・船の形と数は描いた形でない", schem=True)

# ── 第8章 c909 救助の時間（分の比例＝門番 ⑤ num・着水から）
AX909 = ((0.0, 300.0), (25.0, 1600.0))
Y909 = 560.0
C909 = [
    _at(_c(0, R, big="約4分", lines="最初のフェリー", bcap=64, cap=46), 520, 360),
    _at(_c(1, R, big="約20分", lines="全員が救われる", bcap=64, cap=46), 1340, 760),
    _at(_c(0, R, big="24分", lines="最後の船が離れる", sub="15:54:43", bcap=64, cap=46), 1560, 350),
]
VIEWS["c909"] = _z(2, "救助の時間", "着水から", C909, [
    _p(0, lambda: _hline(AX909, Y909, 5.0) + _t(300.0, Y909 + 66, "着水", 40, J.TICK, "middle", 160)
       + _lead(C909[0], _lx(AX909, 4.0), Y909) + _lead(C909[2], _lx(AX909, 24.0), Y909)),
    _p(1, lambda: _lead(C909[1], _lx(AX909, 20.0), Y909))],
    src=S_R, note="分は比例・目盛りは5分ごと",
    tl=dict(kind="num", ax=AX909, pts=(("約4分", _lx(AX909, 4.0)), ("約20分", _lx(AX909, 20.0)), ("24分", _lx(AX909, 24.0)))))
# ── c913 重いけが
FU["c913"] = _f(2, "重いけが", "5人の内訳", [
    _c(0, R, head="客室乗務員", lines="足の傷", cell=(0, 0)),
    _c(0, R, head="乗客", lines="胸の骨の端の骨折", cell=(1, 0)),
    _c(0, R, head="乗客", lines="低体温症", sub="2日後の夕方まで入院", cell=(0, 1)),
    _c(1, R, head="あとで申し出た乗客", big="2人", lines="肩の骨折", cell=(1, 1))], src=S_R)


# ── c918 両岸へ（救助の3つ・川・両岸＝模式）。北が上＝西がニュージャージー側
def _c918_river():
    g = F.rect(820.0, 430.0, 280.0, 428.0, J.LINE, None, None, op=0.12) + F.line(820.0, 430.0, 820.0, 858.0, J.TICK, 4) + F.line(1100.0, 430.0, 1100.0, 858.0, J.TICK, 4)
    return g + _plane(960.0, 600.0, INK, k=0.9, ang=200.0) + _t(1500.0, 684.0, "ニューヨーク側", 42, INK, "middle", 400)


C918 = [
    _at(_c(0, R, lines="フェリー", cap=46), 560, 300),
    _at(_c(0, R, lines="消防", cap=46), 960, 300),
    _at(_c(0, R, lines="沿岸警備隊", cap=46), 1360, 300),
    _at(_c(0, R, head="ニュージャージー側", lines="救助の指揮所", cap=46), 420, 670),
]
VIEWS["c918"] = _z(2, "両岸へ", "救助の動き", C918, [
    _p(0, _c918_river), _p(0, lambda: _lead(C918[0], 900.0, 548.0) + _lead(C918[1], 960.0, 540.0) + _lead(C918[2], 1020.0, 548.0)),
    _p(1, lambda: _arrow(900.0, 650.0, 640.0, 680.0, J.AMBER, 8, 28) + _arrow(1020.0, 650.0, 1330.0, 680.0, J.AMBER, 8, 28), arrow=True)],
    src=S_R, note="模式・位置と大きさは描いた形でない", schem=True)

# ── 第9章 ca08 生き残れた理由（結論の4つ）
FU["ca08"] = _f(2, "生き残れた理由", "報告書の結論", [
    _c(0, R, head="乗員", lines="判断と連携", cell=(0, 0)),
    _c(1, R, head="海の上の装備", lines="偶然あった", cell=(1, 0)),
    _c(1, R, head="客室乗務員", lines="速い誘導", cell=(0, 1)),
    _c(1, R, head="救助の人たち", lines="近さと早さ", cell=(1, 1))], src=S_R)
# ── ca10 認められた判断（所見の番号＝報告書の結論の並び）
FU["ca10"] = _f(3, "認められた判断", "報告書の所見", [
    _c(0, R, head="所見15", lines="川を選んだ判断", cell=(0, 0)),
    _c(1, R, head="所見14", lines="APU を先に回した", cell=(1, 0)),
    _c(1, R, head="所見18", lines="フラップ2は妥当", cell=(2, 0)),
    _c(2, R, lines="どれも機長がしたこと", cell=(0, 1), span=(3, 1))], src=S_R)
# ── ca12 時間はあったか（委員の意見＝原文どおり・字幕を消す）
FU["ca12"] = _f(3, "時間はあったか", "委員の意見", [
    _c(0, R, head="NTSB の以前の研究", lines="着水には準備の時間", cell=(0, 0)),
    _c(2, R, lines=("1549便には、ほとんど", "何をする時間もなかった"), q=True, cell=(1, 0))],
    [_x(2, "a", "b", t="ところが")], src=S_R, mute=(2,))
# ── ca14 4つの偶然（重なった偶然＝ca04 と同じ語・下に「次も重なるとは限らない」）
C14A = [
    _at(_c(1, R, lines="よい見通しと静かな水面", cap=46), 560, 400),
    _at(_c(1, R, lines="経験のある乗員", cap=46), 1360, 400),
    _at(_c(2, R, lines="積む決まりのない装備", cap=46), 560, 560),
    _at(_c(2, R, lines="近くの船", cap=46), 1360, 560),
]
VIEWS["ca14"] = _z(3, "4つの偶然", "3つ目の問い", C14A, [
    _p(0, lambda: _t(960.0, 300.0, "重なった偶然", 46, J.TICK, "middle", 600)),
    _p(2, lambda: F.line(560.0, 680.0, 1360.0, 680.0, J.TICK, 3) + _t(960.0, 760.0, "次も重なるとは限らない", 52, J.AMBER, "middle", 900))],
    src=S_R, note="偶然の語は報告書の結論と分析の字")

# ── 第10章 cb01 勧告の数（1つの札が1本）
GX01 = dict(faa=(300.0, 470.0, 13, 2), easa=(1080.0, 501.0, 8, 1), usda=(1600.0, 501.0, 1, 1))


def _cb01_cards(col=None):
    g = ""
    cols = dict(faa=J.LINE, easa=J.AMBER, usda=INK)
    for key, (x0, y0, nc, nr) in GX01.items():
        for i in range(nc * nr):
            x, y = x0 + (i % nc) * 48.0, y0 + (i // nc) * 62.0
            if col:
                g += F.rect(x - 18, y - 25, 36, 50, cols[key], None, None, rx=5, op=0.85)
            else:
                g += F.rect(x - 18, y - 25, 36, 50, "none", J.TICK, 3, rx=5)
    return g


C01 = [
    _at(_c(1, R, head="勧告", big="35本", sub="報告書の34本＋先の1本", bcap=64), 960, 318),
    _at(_c(2, R, head="FAA", big="26本", bcap=64), 588, 720),
    _at(_c(2, R, head="ヨーロッパの当局", big="8本", bcap=64), 1248, 720),
    _at(_c(2, R, head="アメリカの農務省", big="1本", bcap=64), 1640, 720),
]
VIEWS["cb01"] = _z(3, "勧告の数", "あて先", C01, [_p(1, _cb01_cards), _p(2, lambda: _cb01_cards(True))],
                   src=S_CAROL, note="1つの札が1本の勧告")
# ── cb03 評価のしくみ
FU["cb03"] = _f(3, "評価のしくみ", "閉じ方", [
    _c(0, R, head="勧告の相手", lines="対応する", cell=(0, 0)),
    _c(2, R, head="NTSB", lines="対応を見て評価", cell=(1, 0)),
    _c(2, R, lines="記録を閉じる", cell=(2, 0)),
    _c(1, R, head="受け入れられない対応", lines="求めに届かない", cell=(0, 1), span=(3, 1))],
    [_x(2, "a", "b"), _x(2, "b", "c")], src=S_CAROL)
# ── cb05 閉じた評価（A-10-068）
FU["cb05"] = _f(2, "閉じた評価", "CAROL の記録", [
    _c(0, R, head="勧告", lines="手順書の作り方の指針", cell=(0, 0)),
    _c(1, R, big="2012年", lines="受け入れられない対応", cell=(1, 0))], src=S_CAROL)
# ── cb07 閉じるまでの年月（年の比例＝門番 ⑤ ym）
AX07 = ((2009.0, 300.0), (2026.0, 1660.0))
Y07 = 560.0
V07 = (2009 + 0.5 / 12, 2025 + 11.5 / 12)
C07 = [
    _at(_c(0, R, head="事故", big="2009年1月", bcap=64), 360, 360),
    _at(_c(0, R, head="勧告が閉じる", big="2025年12月", bcap=64), 1520, 360),
    _at(_c(1, R, big="17年近く", bcap=72), 960, 760),
]
VIEWS["cb07"] = _z(2, "閉じるまでの年月", "事故から", C07, [
    _p(0, lambda: _hline(AX07, Y07, 1.0) + _lead(C07[0], _lx(AX07, V07[0]), Y07) + _lead(C07[1], _lx(AX07, V07[1]), Y07)),
    _p(1, lambda: F.line(_lx(AX07, V07[0]), Y07 + 50, _lx(AX07, V07[1]), Y07 + 50, J.AMBER, 10))],
    src=S_CAROL, note="年は比例・目盛りは1年ごと",
    tl=dict(kind="ym", ax=AX07, pts=(("2009年1月", _lx(AX07, V07[0])), ("2025年12月", _lx(AX07, V07[1])))))
# ── cb10 エンジンの規則（FAA の規則の説明＝連邦官報・低い回転の試験の勧告＝A-10-064）
# 🔧 門番 credits：副題「2023年の規則」が地 c61（2009年の撮影）の年と食い違う＝副題に年を書かない
FU["cb10"] = _f(2, "エンジンの規則", "鳥とエンジン", [
    _c(0, None, head="FAA の規則の説明", lines="1549便がきっかけ", sub="鳥の吸い込みの研究", cell=(0, 0), span=(1, 2)),
    _c(1, R, head="勧告", lines="低い回転での鳥の試験", cell=(1, 0)),
    _c(1, R, big="2024年4月", lines="受け入れられる別の対応", cell=(1, 1))], src=S_FR + "・" + S_CAROL)
# ── cb15 残った評価（A-10-067・A-10-069＝受け入れられない対応の印）
C15 = [
    _at(_c(0, R, head="勧告", lines="低い所の手順書を使う", cap=46), 560, 470),
    _at(_c(1, R, head="勧告", lines="その手順の訓練", cap=46), 1360, 470),
    _at(_c(2, R, lines="受け入れられない対応", sub="2026年11月の時点", cap=46), 960, 730),
    _at(_c(1, R, head="報告書の求め", lines="偶然に頼らない備え", cap=46), 960, 290),
]


def _cb15_stamp():
    g = ""
    for c in C15[:2]:
        x, y, w, h = _zbox(c)
        g += F.rect(x - 14, y - 14, w + 28, h + 28, "none", J.ALERT, 7, rx=22)
    return g


VIEWS["cb15"] = _z(3, "残った評価", "手順書と訓練", C15, [_p(2, _cb15_stamp)], src=S_CAROL)
# ── cb02 勧告の状態（1つの四角が1本）
SQ02 = (300.0, 430.0, 56.0, 12.0)            # 左上・辺・すき間（17列×2行＝閉じた34）
ST02 = ((10, J.LINE, 0.85), (7, J.LINE, 0.40), (16, J.AMBER, 0.92), (1, J.TICK, 0.85))


def _cb02_sq(hi=False):
    x0, y0, w, gp = SQ02
    g, i = "", 0
    for n, col, op in ST02:
        for _k in range(n):
            x, y = x0 + (i % 17) * (w + gp), y0 + (i // 17) * (w + gp)
            if (col == J.AMBER) == hi:
                g += _sq(x, y, w, fill=col, op=op)
            i += 1
    if not hi:
        g += _sq(1560.0, 464.0, w, stroke=J.AMBER, dash="10 8")
        g += _t(300.0, 610.0, "受け入れられる対応 10本", 34, J.LINE, "start", 500) + _t(820.0, 610.0, "別の対応 7本", 34, J.LINE, "start", 300)
        g += _t(1120.0, 610.0, "考え直して閉じた 1本", 34, J.TICK, "start", 400)
    return g


C02 = [
    _at(_c(0, R, head="閉じた", big="34本", bcap=64), 870, 320),
    _at(_c(0, R, head="開いている", big="1本", bcap=64), 1588, 320),
    _at(_c(1, R, head="受け入れられない対応", big="16本", bcap=64), 960, 750),
]
VIEWS["cb02"] = _z(2, "勧告の状態", "いまの内訳", C02, [_p(0, _cb02_sq), _p(1, lambda: _cb02_sq(True))],
                   src=S_CAROL, note="1つの四角が1本の勧告")
# ── cb14 ヨーロッパあての勧告（1つの四角が1本）
SQ14 = (436.0, 420.0, 110.0, 24.0)
ST14 = ((3, J.LINE, 0.85), (1, J.LINE, 0.40), (4, J.AMBER, 0.92))


def _cb14_sq():
    x0, y0, w, gp = SQ14
    g, i = "", 0
    for n, col, op in ST14:
        for _k in range(n):
            g += _sq(x0 + i * (w + gp), y0, w, fill=col, op=op)
            i += 1
    return g


def _sq14_mid(i0, n):
    x0, y0, w, gp = SQ14
    return x0 + i0 * (w + gp) + (n * (w + gp) - gp) / 2, y0 + w


C14 = [
    _at(_c(0, R, head="ヨーロッパの当局あて", big="8本", bcap=64), 960, 300),
    _at(_c(0, R, head="受け入れられる対応", big="3本", bcap=64), 470, 720),
    _at(_c(1, R, head="受け入れられる別の対応", big="1本", bcap=64), 960, 720),
    _at(_c(1, R, head="受け入れられない対応", big="4本", bcap=64), 1460, 720),
]
VIEWS["cb14"] = _z(2, "ヨーロッパあての勧告", "すべて閉じた", C14, [
    _p(0, _cb14_sq), _p(0, lambda: _lead(C14[1], *_sq14_mid(0, 3))), _p(1, lambda: _lead(C14[2], *_sq14_mid(3, 1)) + _lead(C14[3], *_sq14_mid(4, 4)))],
    src=S_CAROL, note="1つの四角が1本の勧告")

# ── 第11章 cc05・cc07・cc09 答えと結び
FU["cc05"] = _f(2, "1つ目の答え", "戻れたのか", [
    # 🔧 check_box（空き矩形 35%）：同じ列に縦に並べると細い札 a が b の幅に引き伸ばされた＝横に並べる
    _c(0, R, head="判断の35秒を足すと", lines="届かなかった", cell=(0, 0)),
    _c(1, R, head="報告書の結論", lines=("川が、生き残れる見込みの", "いちばん高い道"), cell=(1, 0))], src=S_R + "・NTSB 公開ドケット DCA09MA026")
FU["cc07"] = _f(2, "3つ目の答え", "報告書の言う偶然", [
    _c(0, R, lines="よい見通しと静かな水面", cell=(0, 0)),
    _c(1, R, lines="経験のある乗員", cell=(1, 0)),
    _c(1, R, lines="積む決まりのない装備", cell=(0, 1)),
    _c(1, R, lines="近くの船", cell=(1, 1))], src=S_R)
FU["cc09"] = _f(2, "残された記録", "報告書が書いたこと", [
    _c(0, R, head="報告書に残る", lines="助かった理由", cell=(0, 0)),
    _c(0, R, lines="足りなかった所", cell=(1, 0)),
    _c(1, R, lines="成功の中の偶然まで", cell=(0, 1), span=(2, 1))], src=S_R)
# ── 第7章 c810 いた場所（人数の比例＝門番 ⑤ num）
AX810 = ((0.0, 560.0), (100.0, 1560.0))
YR810 = (440.0, 600.0)
C810 = [_at(_c(2, R, head="翼の上", lines="立つ場所はほぼ残らず", cap=46), 1200, 775)]
VIEWS["c810"] = _z(3, "いた場所", "助けられた人の数", C810, [
    _p(0, lambda: _hline(AX810, 676.0, 10.0) + _t(540.0, YR810[0] + 14, "前の2つのすべり台", 38, INK, "end", 440)
       + _t(540.0, YR810[1] + 14, "翼の上と翼のすべり台", 38, INK, "end", 460)),
    _p(1, lambda: _hbar(AX810, 64.0, YR810[0], J.LINE) + _t(_lx(AX810, 64.0) + 20, YR810[0] + 16, "約64人", 48, J.LINE, "start", 300)
       + _hbar(AX810, 87.0, YR810[1], J.AMBER) + _t(_lx(AX810, 87.0) + 20, YR810[1] + 16, "約87人", 48, J.AMBER, "start", 300))],
    src=S_R, note="棒の長さは人数の比例・目盛りは10人ごと",
    tl=dict(kind="num", ax=AX810, pts=(("約64人", _lx(AX810, 64.0)), ("約87人", _lx(AX810, 87.0)))))
# ── c816 浮くための物（聞き取りの表）
TY816 = (390.0, 480.0, 570.0)
R816 = (("着水の前に着けた", "2人"), ("着水のあと座席の下から", "10人"), ("人から渡された", "21人"))


def _c816_table():
    g = _t(420.0, 320.0, "救命胴衣", 40, J.TICK, "start", 300)
    g += "".join(F.line(400.0, y + 45, 1520.0, y + 45, J.TICK, 3, op=0.7) for y in TY816[:2])
    for y, (a, n) in zip(TY816, R816):
        g += _t(420.0, y + 16, a, 44, INK, "start", 760) + _t(1500.0, y + 20, n, 56, J.AMBER, "end", 240)
    return g


C816 = [_at(_c(1, R, head="浮く座席のクッション", big="77人", lines="持って出た", bcap=64, cap=46), 960, 740)]
VIEWS["c816"] = _z(2, "浮くための物", "手に取った物", C816, [_p(0, _c816_table)], src=S_R, note="乗客の聞き取りの答え")
# ── c819 説明としおり（聞き取りの札）
FU["c819"] = _f(2, "説明としおり", "乗客の聞き取り", [
    _c(0, R, head="答えた乗客", big="146人", sub="150人のうち", cell=(0, 0)),
    _c(0, R, head="安全の説明の実演", big="25人", lines="ほとんど見た", sub="一部を見た 19人", cell=(1, 0)),
    _c(1, R, head="安全のしおり", big="12人", lines="読んだ", cell=(2, 0))], src=S_R)


# ══════════════════════════════════════════════════════════
#  配線（SPEC の fig・段・門番が測る形）＝mech31 と同じ形・型の名は m32
# ══════════════════════════════════════════════════════════
def _cid(view):
    return "c" + view[3:] if view.startswith(("fu_", "zu_")) else view


def _ids(fu):
    return [c["id"] for c in fu["cards"]] + [a["id"] for a in fu.get("arrows", ())] + [p["id"] for p in fu.get("parts", ())]


def fu(cid):
    """SPEC の fig＝("m32", …)。段は札の at から組む。"""
    d = FU[cid]
    steps = []
    for i in range(d["n"]):
        on = {c["id"]: "on" for c in d["cards"] if c["at"] == i}
        on.update({a["id"]: "on" for a in d["arrows"] if a["at"] == i})
        steps.append(dict(state=on))
    return ("m32", dict(view="fu_" + cid[1:], steps=steps, note=d["note"], src=d["src"], mute=list(d["mute"])))


def fu_spec(cid, ground, **kw):
    """章ファイルの SPEC の1行＝`"c203": M.fu_spec("c203", ss.gr("c50"))`。"""
    d = FU[cid]
    return dict(ground, t=d["t"], s=d["s"], fig=fu(cid), **kw)


def zu(cid):
    d = VIEWS[cid]
    steps = [dict(state={x["id"]: "on" for x in d["cards"] + d["parts"] if x["at"] == i}) for i in range(d["n"])]
    return ("m32", dict(view="zu_" + cid[1:], steps=steps, note=d["note"], src=d["src"], mute=list(d["mute"])))


def zu_spec(cid, ground, **kw):
    d = VIEWS[cid]
    return dict(ground, t=d["t"], s=d["s"], fig=zu(cid), **kw)


def stage_art(view, prev, st):
    if view in VIEWS:
        d = VIEWS[view]
        s = [p["fn"]() for p in d["parts"] if _on(prev, st, p["id"])]
        return s + [_draw_card(c, _zbox(c)) for c in d["cards"] if _on(prev, st, c["id"])]
    d = FU[view]
    boxes, _bb, k = layout(d)
    s = []
    for c in d["cards"]:
        if _on(prev, st, c["id"]):
            s.append(_draw_card(c, boxes[c["id"]], k))
    for a in d["arrows"]:
        if _on(prev, st, a["id"]):
            s.append(_draw_arrow(a, boxes, k))
    return s


def quote_lines(view):
    """原文どおりに出す字（門番 echo の例外＝mute のあるカットだけ＝その行の字幕は消える）。"""
    d = FU.get(_cid(view)) or VIEWS.get(_cid(view))
    if not d or not d["mute"]:
        return []
    return [ln for c in d["cards"] if c["q"] for ln in _qwrap(c["lines"])]


def m32(view, steps, start=None, rel=(), note="", src="", mute=()):
    """32本目 札の型と見え方の表。view は `fu()` の「fu_203」か `zu()` の「zu_207」の形。steps＝語りの行ごとの段。"""
    view = _cid(view)
    if view not in FU and view not in VIEWS:
        raise ValueError(f"m32：表 FU にも見え方の表 VIEWS にも無い {view!r}")
    d = FU.get(view) or VIEWS[view]
    zv = view in VIEWS
    if zv and d["schem"] and "模式" not in note:
        raise ValueError(f"m32：{view} は模式＝note に「模式」を書くこと（§5b-10 模式であることを札で断る）")
    ids = _ids(d)
    cur = {k: "off" for k in ids}
    st0 = dict(cur, **(start or {}))
    states, c2 = [], dict(st0)
    for st in steps:
        c2 = dict(c2, **(st.get("state") or {}))
        for k, v in c2.items():
            if k not in ids or v not in ONOFF:
                raise ValueError(f"m32：{view} の欄 {k}={v!r} は知らない")
        states.append(dict(c2))
    g = []
    if zv:
        for c in d["cards"]:
            x, y, w, h = _zbox(c)
            if x < F.BX0 or x + w > F.BX1 or y < F.BY0 or y + h > F.BY1 - 34:
                raise ValueError(f"m32：{view} の札 {c['id']} が本体の外（{x:.0f},{y:.0f}〜{x + w:.0f},{y + h:.0f}）")
        if d["schem"]:
            g.append(F.txtfit(F.BX0 + 8, F.BY0 + 36, "模式", 1000, cap=30, col=J.TICK, ol=OL))
    else:
        _boxes, bb, _k = layout(d)
        if bb[2] > AREA_W or bb[3] > AREA_H:
            raise ValueError(f"m32：{view} の札が広すぎる（幅 {bb[2]:.0f}／{AREA_W:.0f}・高さ {bb[3]:.0f}／{AREA_H:.0f}）")
    g.append(F.txtfit(F.BX0, F.BY1 - 6, note + (f"　出典：{src}" if src else ""), F.BW, cap=26, col=J.TICK, ol=OL))
    stages, prev = [], st0
    for stt in states:
        stages.append("".join(stage_art(view, prev, stt)) or " ")
        prev = stt
    f = F.Fig("".join(g), stages, "", (F.BX0, F.BX1))
    f.moves = []
    f.mech = dict(kind="m32", view=view, start=st0, states=states, rel=list(rel), tags=[], shapes=[], lab="", note=note,
                  steps=[dict(s) for s in steps], geo=geo_of(view), texts_all=svg_texts("".join(stages)), sns=False)
    return f


def geo_of(view):
    if view in VIEWS:
        d = VIEWS[view]
        boxes = {c["id"]: _zbox(c) for c in d["cards"]}
        x0 = min(b[0] for b in boxes.values())
        y0 = min(b[1] for b in boxes.values())
        bb = (x0, y0, max(b[0] + b[2] for b in boxes.values()) - x0, max(b[1] + b[3] for b in boxes.values()) - y0)
        return dict(view=view, src={key: tuple(v) for key, v in SRC.items()}, vsrc=tuple(sorted({c["who"] for c in d["cards"] if c["who"]})),
                    quotes=tuple("".join(c["lines"]) for c in d["cards"] if c["q"]), mute=d["mute"], n=d["n"],
                    cards=tuple(dict(id=c["id"], who=c["who"], q=c["q"], dim=c["dim"], rows=tuple(_rows(c))) for c in d["cards"]),
                    narrows=sum(1 for p in d["parts"] if p["arrow"]), bbox=bb, boxes=boxes, k=1.0, band=d["band"], tl=d["tl"], schem=d["schem"])
    d = FU[view]
    boxes, bb, k = layout(d)
    return dict(view=view, src={key: tuple(v) for key, v in SRC.items()}, vsrc=tuple(sorted({c["who"] for c in d["cards"] if c["who"]})),
                quotes=tuple("".join(c["lines"]) for c in d["cards"] if c["q"]), mute=d["mute"], n=d["n"],
                cards=tuple(dict(id=c["id"], who=c["who"], q=c["q"], dim=c["dim"], rows=tuple(_rows(c, k))) for c in d["cards"]),
                narrows=len(d["arrows"]), bbox=bb, boxes=boxes, k=k)
