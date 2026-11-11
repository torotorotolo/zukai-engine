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


def _c614_done():
    (x1, y1), (x2, y2), _p3 = PG
    g = F.rect(x1 + 6, y1 + 6, PW - 12, PH - 12, J.AMBER, None, None, rx=6, op=0.42)
    return g + F.rect(x2 + 6, y2 + 6, PW - 12, P1Y - y2 - 46, J.AMBER, None, None, rx=6, op=0.42) + _part(1)


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
