# -*- coding: utf-8 -*-
"""15本目（リノ・エアレース2011）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-01（16本目 バイオントダム災害 ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `c646174` と同じ）
  ・`cuts/ss.py` の後半＝案C の出典の表・時計と秒の札・軸の型・地図5範囲・棒・書類の再現図・鎖と箱の値（15本目 ⑤b-2〜⑤b-7）
  ・`titan_fig.GEO` の15本目の7地点（`reno_` の頭＝⑤b-7）
  ・門番の記録の表（check_axis・check_qty・check_boxes・check_mech）
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を15本目の実物でも確かめている＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は16本目の空の器にした
  （fixture_ep14 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep15
      fixture_ep15.apply(sys.modules[__name__])   # その処理の中だけ ss・GEO・この門番の記録の表が15本目になる
      try: …（検算）
      finally: fixture_ep15.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14本目の見本と重ねるとき（check_mech は14本目の検算と15本目の検算を1つの処理で回す）は
      fixture_ep15.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss・GEO は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと16本目以降の画に15本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ 見本の頁の原文 `ref/ep15/src/ep15_pages.txt` は git の外（本線の作業ツリーにだけある）＝無いときは頁の照合を飛ばす
     （check_illu の `_pages()` が None を返す）。
"""
from __future__ import annotations

from pathlib import Path

import jiko_style as _J        # R_BASE（地図の線の色）が使う。ss も同じ理由で、章ファイルより先にここを読んでいた

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep15"


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）と軸の型（`tools/axis.py`・門番 `check_axis`）
#  ── 15本目 ⑤b-2〜⑤b-5
# ══════════════════════════════════════════════════════════
REC_PAGES = REF / "src" / "ep15_pages.txt"      # ④ の make_pages.py の出力（261頁・git の外＝手元だけ）
# 🔴 2026-09-30（15本目 ⑤b-2）：15本目の値を入れた。頁の番号は `ref/ep15/v1_build/make_pages.py` が振った通し番号
#    （AAB＝PDF の頁のまま p1〜p52・#40 p1001〜・#33 p2001〜・#14 p3001〜・#53 p4001〜・CAROL p5008〜p5017・勧告書 p6001〜・
#     #17 p7001〜）。画面の出典は「PDF N頁」（base を引く）。⚠️ 台本の出典欄の「#33 p9」は #33 の PDF の頁＝ここでは p2009
REC_DOCS = {
    "AAB": dict(range=(1, 52), name="NTSB 事故報告 AAB-12/01", page="pdf", base=0),
    "#40": dict(range=(1001, 1061), name="NTSB 資料 #40（材料の試験）", page="pdf", base=1000),
    "#33": dict(range=(2001, 2022), name="NTSB 資料 #33（生存と運営）", page="pdf", base=2000),
    "#14": dict(range=(3001, 3040), name="NTSB 資料 #14（データの記録）", page="pdf", base=3000),
    "#53": dict(range=(4001, 4029), name="NTSB 資料 #53（性能の解析）", page="pdf", base=4000),
    "CAROL": dict(range=(5008, 5017), name="NTSB 勧告の記録（CAROL）", page=None, base=0),
    "勧告書": dict(range=(6001, 6207), name="NTSB 勧告書（A-12-08〜17）", page=None, base=0),
    "#17": dict(range=(7001, 7029), name="NTSB 資料 #17（耐空性）", page="pdf", base=7000),
}
# 資料で割れる時刻（時計）＝15本目は無い（割れるのは秒の起点＝#42 の「5.3秒」と AAB の「4.6秒」＝台本 §1-5）。
#   秒の札は下の ILLU_SEC_OK（AAB p28 の表の値だけ）で止める＝5.3秒・写真の EXIF から推した時刻は札に出せない
ILLU_SPLIT_TIMES = ()
# 🆕 ⑤b-3（2026-09-30）：観客の群れ（置き場 RC）は**落ちる瞬間より前**だけ（映像方針 §10-1「ゆるめる」＝9秒のあいだも可）。
#   落ちる瞬間＝崩れ始め 16:24:28.9（AAB p28 の表の 0秒）＋約9.1秒＝16:24:38.0。場面の時刻 at は秒まで書く（秒の無い "16:24" は
#   その分の終わりとみなす＝遅い側に倒す＝群れを出せない）。c212・c726 は at="16:24:28"（0秒のころ＝観客はピットとボックス席にいた）
ILLU_CROWD_UNTIL = "16:24:38"
# 🆕 ⑤b-3：この回に置いてよい役割（門番 check_illu ②）＝型紙（1人ずつ数えられる影）は無し・群れは観客だけ
#   （パイロット・審判・救護・検査員・整備の仲間は描かない＝映像方針 §1 線2・§6②）
ILLU_ROLES = dict(sprite=(), crowd=("spectators",))
# 🆕 15本目：画面に出してよい秒（札の「N秒」「約N秒」）＝AAB p28 の経過の表の値だけ（映像方針 §6 ⑤）。門番 check_illu ⑤
ILLU_SEC_OK = {s: "AAB p28" for s in ("0", "0.27", "0.56", "0.83", "1.3", "1.44", "3.1", "4.6", "9.1")}
# 🆕 15本目：札に出してよい時計の時刻＝表の時刻（16時24分台）だけ（EXIF から推した時刻を出さない）
ILLU_CLOCK_OK = ("16:24",)
# 🆕 15本目：描いてよい数（部品の obj の合計＝その場面に描いた数）と記録（映像方針 §6 ③）。門番 check_illu ③
ILLU_COUNTS = dict(aircraft=(1, "AAB p10"), fuel_truck=(1, "AAB p19"), stands=(3, "AAB p20"), pylons=(12, "AAB p17"))

# 🔴 2026-09-30（15本目 ⑤b-5）：15本目の値を入れた（割れる時刻の印は使わない＝ILLU_SPLIT_TIMES が空）
AXIS_DOCS = {"AAB": "報告書", "CAROL": "勧告の記録"}

# 🆕 15本目 ⑤b-5（値と頁は ref/ep15/src/ep15_pages.txt で当てた）
#   HIST＝機体の歩み 1944→2011（c324・c404・c408・c410・c411・c412＝第3〜4章）
#   LATE＝その寄り 2006→2012（c607・c615＝第6章・改造のあとの初飛行と2010年の出場）
#   A08 ＝勧告 A-12-08 が閉じるまで（c913・c915・c916＝CAROL の記録 p5008）
#   DRILL＝2011年の訓練と事故（c809・c813＝AAB p21）／EMS＝事故と多数傷病者事故の宣言（c804＝AAB p20・p28）
#   UPSET＝横転の前の秒（c218＝負の秒・AAB p29）／NINE＝その9秒（c220＝AAB p28 の経過の表）
AX_HIST = dict(view="date", span=("1942", "2013"), ticks=("1950", "1960", "1970", "1980", "1990", "2000", "2010"))
AX_LATE = dict(view="date", span=("2006", "2012"), ticks=("2007", "2008", "2009", "2010", "2011", "2012"))
# ⚠️ ⑤b-5 の layout：左の端の点（事故）の札が右へ伸びると、すぐ右の点の縦の線が札を貫いた＝左に余白を取り、事故の札は左へ
AX_A08 = dict(view="date", span=("2010-01", "2022-03"), ticks=("2010", "2012", "2014", "2016", "2018", "2020", "2022"))
# ⚠️ ⑤b-5 の layout：5月25日の札（左へ）が枠の左の端を越えた＝4月1日から
AX_DRILL = dict(view="date", span=("2011-04-01", "2011-10-05"),
                ticks=("2011-04", "2011-05", "2011-06", "2011-07", "2011-08", "2011-09", "2011-10"))
AX_EMS = dict(view="clock", span=("16:20", "16:32"), ticks=("16:20", "16:22", "16:24", "16:26", "16:28", "16:30", "16:32"))
AX_UPSET = dict(view="sec", span=("-10", "1"), ticks=("-10", "-8", "-6", "-4", "-2", "0"))
AX_NINE = dict(view="sec", span=("0", "10"), ticks=("0", "2", "4", "6", "8", "10"))

#   ⚠️ 年だけの値（"1983"）は年の真ん中に置く（span の両端も）＝1983〜1989 のレースは 1983.5〜1989.5 の帯
#   ⚠️ 事故の時刻は台本 c317 の「午後4時24分38秒ごろ」（AAB p28 の表）＝16:24。本文の要約の「about 1625」（p8・p10）は丸めた値
AXI = {
    # ── 機体の歩み（AAB p12「delivered to the Army Air Forces on December 23, 1944 … in July 1946, it was declared surplus
    #    and sold … acquired by the accident pilot in July 1983 … raced … from 1983 through 1989 before placing it in storage
    #    until 2007 … Between 2007 and 2009 … overhaul and further modifications」・p35「August 17, 1983 … special
    #    airworthiness certificate」・p36「completion of its major modifications occurred on September 21, 2009」「the 2010 NCAR」）
    "deliver": dict(k="pt", at="1944-12-23", t="軍へ引き渡し", rec="AAB p12"),
    "sold": dict(k="pt", at="1946-07", t="売却", rec="AAB p12"),
    "owner": dict(k="pt", at="1983-07", t="パイロットが取得", rec="AAB p12", anchor="end"),
    "exp": dict(k="pt", at="1983-08-17", t="FAAの許可", rec="AAB p35", anchor="start", fmt="ym"),
    "race8389": dict(k="span", a="1983", b="1989", t="リノのレース", rec="AAB p12", c="INST"),
    "store": dict(k="span", a="1989", b="2007", t="保管", rec="AAB p12", c="TICK"),
    "store_br": dict(k="br", a="1989", b="2007", rec="AAB p12"),
    # ⚠️ 2年の帯は札の幅が 164画素まで＝7字は小さくなる → 5字
    "rebuild": dict(k="span", a="2007", b="2009", t="分解と改造", rec="AAB p12", c="AMBER"),
    "first": dict(k="pt", at="2009-09-21", t="初飛行", rec="AAB p36"),
    "race10": dict(k="pt", at="2010", t="出場", rec="AAB p36"),
    "acc": dict(k="pt", at="2011-09-16", t="事故", rec="AAB p10", c="ALERT", fmt="y"),
    "life_br": dict(k="br", a="1944-12-23", b="2011-09-16", rec=["AAB p12", "AAB p10"]),
    # ── 勧告 A-12-08（CAROL p5008：NTSB の評価 2012-07-25・2016-11-30・2020-07-22＝OPEN—ACCEPTABLE RESPONSE／
    #    2020-02-27 命令 8900.1 を改めた・2020-11-03 通達 AC 91-45C を廃止（守らせる言い方が 49 CFR 5.25 で禁じられた）／
    #    2021-07-13 CLOSED—ACCEPTABLE ALTERNATE ACTION）
    "a08_acc": dict(k="pt", at="2011-09-16", t="事故", rec="CAROL p5008", c="ALERT", fmt="ym", anchor="end"),
    # ⚠️ ⑤b-5 の layout：「2020年7月」の札（右へ）が枠の右の端を越えた＝3回の評価は年だけ（語りも「3回」とだけ言う）
    "a08_1": dict(k="pt", at="2012-07-25", t="まだ閉じない", rec="CAROL p5008", fmt="y"),
    "a08_2": dict(k="pt", at="2016-11-30", t="まだ閉じない", rec="CAROL p5008", fmt="y"),
    "a08_3": dict(k="pt", at="2020-07-22", t="まだ閉じない", rec="CAROL p5008", fmt="y", anchor="start"),
    "a08_order": dict(k="pt", at="2020-02-27", t="命令を改めた", rec="CAROL p5008", c="INST", fmt="ym", anchor="end"),
    "a08_ac": dict(k="pt", at="2020-11-03", t="通達の廃止", rec="CAROL p5008", c="INST"),
    "a08_close": dict(k="pt", at="2021-07-13", t="閉じた", rec="CAROL p5008", c="OK", anchor="end"),
    "a08_br": dict(k="br", a="2011-09-16", b="2021-07-13", rec="CAROL p5008"),
    # ── 2011年の訓練（AAB p21「tabletop exercise had been conducted on June 2, 2011」「full-scale emergency exercise on
    #    May 25, 2011」）
    "d_acc": dict(k="pt", at="2011-09-16", t="事故", rec="AAB p10", c="ALERT"),
    "tabletop": dict(k="pt", at="2011-06-02", t="机上訓練", rec="AAB p21", anchor="start"),
    "fullscale": dict(k="pt", at="2011-05-25", t="総合訓練", rec="AAB p21", anchor="end"),
    "drill_br": dict(k="br", a="2011-06-02", b="2011-09-16", rec=["AAB p21", "AAB p10"]),
    # ── 事故と宣言（AAB p28 の表＝16:24:28.9 に崩れ始め・約9.1秒後に落ちた／p20「declared a mass-casualty incident at 1626」）
    "t1624": dict(k="pt", at="16:24", t="事故", rec="AAB p28", c="ALERT"),
    "t1626": dict(k="pt", at="16:26", t="多数傷病者事故の宣言", rec="AAB p20"),
    # ── 横転の前（AAB p29「About 8 seconds before the beginning of the upset, there was a noticeable reduction in engine
    #    manifold pressure and rpm」）・0秒＝横転の始まり（p28 の表の 0秒）
    "u0": dict(k="pt", at="0", t="横転の始まり", rec="AAB p28", c="ALERT"),
    "u8": dict(k="pt", at="約-8", t="圧力と回転が下がる", rec="AAB p29"),
    # ── その9秒（AAB p28 の経過の表の秒＝ILLU_SEC_OK と同じ9つ）。札を出さない点（lab=False）＝秒の単位で並んだことだけ
    **{f"s{s}": dict(k="pt", at=s, t="", lab=False, rec="AAB p28")
       for s in ("0", "0.27", "0.56", "0.83", "1.3", "1.44", "約3.1", "4.6", "約9.1")},
    "nine": dict(k="span", a="0", b="約9.1", t="崩れ始めから落ちるまで", rec="AAB p28", c="LINE"),
}
NINE_PTS = ("s0", "s0.27", "s0.56", "s0.83", "s1.3", "s1.44", "s約3.1", "s4.6", "s約9.1")


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：🆕 15本目 ⑤b-7（2026-09-30）：地図（drift）＝5つの範囲（映像方針 §4・09-30 カズヤくん「Googleアースは地図に替える」）
# ══════════════════════════════════════════════════════════
#   RAMP  … 駐機場（c213・c817・c819・c820）＝ショーライン・ピットとボックス席の端・許可と命令の152メートル・通達の305メートル
#   FIELD … 飛行場のまわり（c904 の2行目から）＝燃料車を約2.4キロ先へ・コースを北へ（矢印だけ）・より頑丈な柵
#   TOWN  … リノの町とステッド空港（c201・c811・c812）＝風の向き・州道395号（道の線は模式）
#   FLA   … フロリダ州オカラ（c602）＝基地から半径約161キロ
#   USA   … アメリカ（c413・c603・c917）＝アリゾナ→テキサス→ミンデン／オカラの円と機体の居場所／リノ→ロズウェル
#   地点＝`titan_fig.GEO`（Wikidata・`reno_` の頭）と、報告書の値で置く点（下の pts）。照合（rel）は範囲ごと：
#     空港の点＝NTSB 資料 #17 p7008 の座標（±2キロ）・駐機場＝AAB p19 と p17 の南北の距離・燃料車＝AAB p46・円＝AAB p35
#   🔴 駐機場と飛行場の線（ショーライン・ピット・ボックス席・燃料車・柵）の**長さと東西の並びは模式**＝報告書の値は
#      ショーラインからの南北の距離と、燃料車の距離だけ（注に書く）。コースを北へ移した距離は記録に無い＝矢印だけ（映像方針 §4）
#   ⚠️ 距離の札は語りと同じ「約228メートル」の形（門番 check_drift は⑤b-7 から「メートル」も読む＝描いた2点と ±5%）
#   ⚠️ 下の地図の関数は `src(...)` を呼ぶ（本体は ss.src＝台本の頁→画面の頁の出典の行）。ss から移したので、本体を変えないために
#      薄い橋を置いた（ss.src は apply() の対象でない＝本番の関数のまま）
def src(recs):
    """ss.src の橋（15本目の地図の関数が `src(...)` と書いてあるまま動くように）。"""
    from cuts import ss
    return ss.src(recs)


_FT = 0.0003048            # 1フィート（キロ）
RENO_TAB = (39 + 39 / 60 + 50 / 3600, -(119 + 52 / 60 + 36 / 3600))
RENO_REL = [dict(a="reno_stead", lat=RENO_TAB[0], lon=RENO_TAB[1], tol_km=2.0,
                 src="NTSB 資料 #17 p7008（左の板の一片が見つかった所＝滑走路8-26 の北側・ホームパイロンの近く）")]
_SLAT, _SLON = 39.667222, -119.876111          # ステッド空港（Wikidata）＝駐機場と飛行場の模式の原点

# 駐機場（1キロ＝約993画素）。ショーライン＝滑走路8/26 の南の縁（AAB p17）・ピットの端は南へ748フィート・
#   ボックス席の端は874フィート（AAB p19）・許可の条件と命令＝500フィート（p17）・通達＝1,000フィート（p17・勧告書 A-12-08 p3）
RAMP_VIEW = dict(lon=(_SLON - 0.00997, _SLON + 0.00997), lat=(_SLAT - 0.0040, _SLAT + 0.0013))
RAMP_PTS = dict(
    sl_w=dict(of="reno_stead", km=0.40, deg=270), sl_e=dict(of="reno_stead", km=0.40, deg=90),
    sl_pit=dict(of="reno_stead", km=0.25, deg=270), sl_box=dict(of="reno_stead", km=0.05, deg=90),
    pit=dict(of="sl_pit", km=748 * _FT, deg=180), box=dict(of="sl_box", km=874 * _FT, deg=180),
    pit_w=dict(of="pit", km=0.10, deg=270), pit_e=dict(of="pit", km=0.10, deg=90),
    box_w=dict(of="box", km=0.13, deg=270), box_e=dict(of="box", km=0.13, deg=90),
    o_w=dict(of="sl_w", km=500 * _FT, deg=180), o_e=dict(of="sl_e", km=500 * _FT, deg=180),
    a_w=dict(of="sl_w", km=1000 * _FT, deg=180), a_e=dict(of="sl_e", km=1000 * _FT, deg=180),
    rn=dict(of="sl_e", km=0.06, deg=0),
)
RAMP_REL = [
    # ⚠️ 注の字にもメートル法の換算を添える（門番 wording＝§B1：フィート・マイルだけの字を置かない）
    dict(a="sl_pit", b="pit", km=748 * _FT, dir="南", src="AAB p19（ピットの端はショーラインの南 748フィート＝約228メートル）"),
    dict(a="sl_box", b="box", km=874 * _FT, dir="南", src="AAB p19（ボックス席の端は南 874フィート＝約266メートル）"),
    dict(a="sl_w", b="o_w", km=500 * _FT, dir="南", src="AAB p17（許可の条件・命令＝500フィート＝約152メートル）"),
    dict(a="sl_w", b="a_w", km=1000 * _FT, dir="南", src="AAB p17（通達＝1,000フィート＝約305メートル）"),
]
RAMP_NOTE = "模式図：線の長さと東西の並びは模式。ショーラインから南への距離は報告書の値"
# 段の部品（語りの行に合わせて `_merge` で足す）
R_BASE = dict(route=[dict(via=["sl_w", "sl_e"], col=_J.INK_W, sw=5, dash=None),
                     dict(via=["pit_w", "pit_e"], col=_J.LINE, sw=7, dash=None),
                     dict(via=["box_w", "box_e"], col=_J.LINE, sw=7, dash=None)],
              # ⚠️ 下見（09-30）：ボックス席の札を線の左に置くとピットの線の真下に来て、どちらの線の札か紛らわしかった＝右へ
              tag=[dict(at="sl_e", t="ショーライン", side="right"), dict(at="rn", t="滑走路8/26", side="right"),
                   dict(at="pit_w", t="ピットの端", side="left"), dict(at="box_e", t="ボックス席の端", side="right")])
R_DIMS = dict(dim=[dict(a="pit", b="sl_pit", t="約228メートル"), dict(a="sl_box", b="box", t="約266メートル")])
# 許可の条件・命令（152メートル）の線の札は右の端・通達（305メートル）は左の端（右はボックス席の札に近い＝下見）


def ramp_map(steps, note=RAMP_NOTE, recs=("AAB p17", "AAB p19")):
    """駐機場の地図（c213・c817・c819・c820）。steps は段の list（`merge` で部品を足して作る）。"""
    return ("drift", dict(view=RAMP_VIEW, places=[], pts=RAMP_PTS, rel=list(RAMP_REL), steps=steps, note=note,
                          src=src(list(recs)), scale_km=0.1, grid=0.002))


# 飛行場のまわり（c904 の2行目から・1キロ＝約173画素）。燃料車は「ピットの近くの駐機場」（AAB p19）→ 2012年から
#   「飛行場の南東の側・主な観客席から約1.5マイル」（AAB p46）。柵は「ピットの西の端からボックス席を通って一般の観客席まで」
#   （p46）。コースと選手を「北へ移した」（p46・CAROL A-12-14＝距離の記録は無い）。燃料車の距離だけ宣言（向きは模式）
FIELD_VIEW = dict(lon=(_SLON - 0.0523, _SLON + 0.0623), lat=(_SLAT - 0.0215, _SLAT + 0.0090))
FIELD_PTS = dict(RAMP_PTS,
                 fuel0=dict(of="pit", km=0.25, deg=270),
                 fuelm=dict(of="fuel0", km=0.60, deg=180),   # ⑤c'：燃料車の道の曲がり角（模式）＝札「観客席」の下を通す
                 fuel1=dict(of="box", km=1.5 * 1.609344, deg=135),
                 pbw=dict(of="pit", km=0.10, deg=270), grand=dict(of="box", km=0.40, deg=90),
                 cn1=dict(of="reno_stead", km=0.80, deg=0))
FIELD_REL = [dict(a="box", b="fuel1", km=1.5 * 1.609344, src="AAB p46（主な観客席から約1.5マイル＝約2.4キロ）")]
FIELD_NOTE = "模式図：場所の並びと線の長さは模式（燃料車の距離だけ報告書の値）。コースを動かした距離は記録に無い"


def field_map(steps):
    return ("drift", dict(view=FIELD_VIEW, places=[], pts=FIELD_PTS, rel=list(FIELD_REL), steps=steps,
                          note=FIELD_NOTE, src=src(["AAB p19", "AAB p46"]), scale_km=0.5, grid=0.01))


# リノの町とステッド空港（1キロ＝約24画素）。州道395号の線は町と空港を直線で結んだ模式（道の形は記録に無い）
TOWN_VIEW = dict(lon=(-120.257, -119.432), lat=(39.49, 39.71))
TOWN_PTS = dict(hw_mid=dict(mid=["reno_stead", "reno_city"]),
                wind0=dict(of="reno_stead", km=5.0, deg=240))   # 風上（AAB p16「wind was from 240°」）＝流れの起点（模式）
TOWN_PLACES = [dict(k="reno_stead", side="above"), "reno_city"]


def town_map(steps, note="模式図：地点は緯度経度から（リノは町の中心）", recs=("#17 p7008",)):
    return ("drift", dict(view=TOWN_VIEW, places=TOWN_PLACES, pts=TOWN_PTS, rel=list(RENO_REL), steps=steps,
                          note=note, src=src(list(recs)), scale_km=5, grid=0.1))


# フロリダ州オカラ（1キロ＝約1.39画素）。運用の制限＝基地（オカラの飛行場）から半径100マイル（AAB p35）。
#   円の中心はオカラの町の中心（基地の飛行場の位置は報告書に無い）。外へ出る矢印＝レースへ向かう途中（向きはリノの方角 298.9度）
FLA_VIEW = dict(lon=(-88.44, -75.84), lat=(27.3, 31.1))
FLA_PTS = dict(ocala_r=dict(of="reno_ocala", km=100 * 1.609344, deg=90),
               fl_out=dict(of="reno_ocala", km=300, deg=298.9))
FLA_REL = [dict(a="reno_ocala", b="ocala_r", km=100 * 1.609344, src="AAB p35（半径100マイル＝約161キロ）")]
CIRCLE = dict(circle=dict(at="reno_ocala", through="ocala_r"))


def fla_map(steps):
    return ("drift", dict(view=FLA_VIEW, places=["reno_ocala"], pts=FLA_PTS, rel=list(FLA_REL), steps=steps,
                          note="模式図：円の中心はオカラの町の中心（基地の飛行場の位置ではない）",
                          src=src(["AAB p35"]), scale_km=100, grid=1.0))


# アメリカ（1キロ＝約0.28画素）。ミンデンと空港は約80キロ＝約23画素（輪が重なる＝札は空港を上・ミンデンを下）
USA_VIEW = dict(lon=(-133.1, -67.9), lat=(25.5, 44.0))


def usa_map(steps, places, note, recs, rel=(), extra=""):
    """extra＝出典の行に足す字（`REC_DOCS` に無い資料＝主催の団体の発表など）。"""
    return ("drift", dict(view=USA_VIEW, places=places, pts=dict(FLA_PTS), rel=list(RENO_REL) + list(rel),
                          steps=steps, note=note, src=src(list(recs)) + extra, scale_km=500, grid=5.0))


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：量の型（`tools/qty.py`・門番 check_qty）の棒 ── 15本目 ⑤b-5
# ══════════════════════════════════════════════════════════
# 🔴 2026-09-30（15本目 ⑤b-5）：15本目の値を入れた（値と頁は ref/ep15/src/ep15_pages.txt で当てた）
#   speed＝c206（AAB p10「about 445 knots as it passed pylon 8」＝時速約824キロ／新幹線の営業の最高 時速320キロ＝一般の事実）
#   lap  ＝c217（AAB p29「maximum 458-knot GPS ground speed between pylons 6 and 7 … the fastest that the airplane had flown
#          on the course by about 35 knots」＝848 と、そこから約65キロ〈35ノット〉を引いた 783＝🔴 783 は報告書の差から引いた値
#          ＝注で言う。⚠️ #14 p3008 の「記録した GPS の最高 431ノット（2010-09-14）」は9回の飛行の全体＝物差しが違う）
#   test ＝c606・c609・c612（AAB p36「3 hours of flight time」・p50「all five flights … 20 minutes … only 1 hour 40 minutes」・
#          p36／p49「about 23 minutes」）
#   hours＝c620（AAB p12「“2,700±” hours」＝2011年の参加の書類・p15 注15／p16「1,453.6 hours」）
#   recent＝c622（AAB p51「about 25 total hours between its assembly in 2009 and its July 2011 inspection … about 200 flight
#          hours in it since the previous year」）
#   g    ＝c907（CAROL p5011・p5012「normally between 3 and 4 g」＝棒は上の端 4／AAB p28 の表 17.3G）
#   ⚠️ c616（2010年の速さ＝公式の平均の速さ 325ノット未満＝AAB p36 注41）は棒にしない：同じ物差し（周の平均）の2011年の値が
#      記録に無い＝「その瞬間の速さ」と並べると物差しが違う → 箱の型（2010年の成績の流れ）にした
QG = {
    "speed": dict(id="speed", t="速さ（時速・キロ）", ticks=(0, 200, 400, 600, 800, 1000)),
    "lap": dict(id="lap", t="コースでの速さ（時速・キロ）", ticks=(0, 200, 400, 600, 800, 1000),
                rows=("それまでの最高", "事故の周")),
    "test": dict(id="test", t="試験の飛行の時間（分）", ticks=(0, 30, 60, 90, 120, 150, 180),
                 rows=("求められた", "多く見積もっても", "テレメトリーの記録")),
    "hours": dict(id="hours", t="この機体での時間（時間）", ticks=(0, 500, 1000, 1500, 2000, 2500, 3000),
                  rows=("参加の書類", "記録簿の総時間")),
    "recent": dict(id="recent", t="この機体での時間（時間）", ticks=(0, 50, 100, 150, 200),
                   rows=("書類：前の年から", "記録簿：組み立てから")),
    "g": dict(id="g", t="かかったG（重さの何倍か）", ticks=(0, 5, 10, 15, 20), rows=("ふつうのコース", "事故の最大")),
}
QB = {
    "shinkansen": dict(k="bar", g="speed", t="新幹線（営業の最高）", v=320, rec="一般の事実"),
    "plane824": dict(k="bar", g="speed", t="事故機", v=824, rec="AAB p10", c="AMBER"),
    "lap_prev": dict(k="bar", g="lap", t="それまでの最高", v=783, rec="AAB p29"),
    "lap_acc": dict(k="bar", g="lap", t="事故の周", v=848, rec="AAB p29", c="AMBER"),
    "test_req": dict(k="bar", g="test", t="求められた", v=180, rec="AAB p36"),
    "test_max": dict(k="bar", g="test", t="多く見積もっても", v=100, rec="AAB p50", c="AMBER"),
    "test_tele": dict(k="bar", g="test", t="テレメトリーの記録", v=23, rec="AAB p36", c="ALERT"),
    "hours_form": dict(k="bar", g="hours", t="参加の書類", v=2700, rec="AAB p12", c="AMBER"),
    "hours_log": dict(k="bar", g="hours", t="記録簿の総時間", v=1453.6, rec="AAB p16"),
    "recent_form": dict(k="bar", g="recent", t="書類：前の年から", v=200, rec="AAB p51", c="AMBER"),
    "recent_log": dict(k="bar", g="recent", t="記録簿：組み立てから", v=25, rec="AAB p51"),
    "g_course": dict(k="bar", g="g", t="ふつうのコース", v=4, rec="CAROL p5011"),
    "g_acc": dict(k="bar", g="g", t="事故の最大", v=17.3, rec="AAB p28", c="ALERT"),
}


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：🆕 15本目 ⑤b-5（2026-09-30）：箱の型の15本目の表（門番 check_boxes の REC_MECH・REC_OTHER_ROLE・REC_CHIP・REC_FORM と照らす）
# ══════════════════════════════════════════════════════════
# 報告書の鎖（c106・c723・c725）＝AAB p52 の推定原因「deteriorated locknut inserts → screws to become loose → reduced
#   stiffness → flutter at racing speeds → failure of the left trim tab link assembly → elevator movement, high flight loads」。
#   箱は動かない（基図）＝段で矢印（つなぎ）が出る。c106 は第1章＝「リンク」の語がまだ出ていない＝「棒が折れる」（台本 c106 の画）
_CX = ((85, 335), (385, 635), (685, 935), (985, 1235), (1285, 1535), (1585, 1835))
CHAIN_Y = (400, 500)


def _chain(words):
    return dict(heads=[dict(id=f"n{i + 1}", t=w, kind="node", x=_CX[i], y=CHAIN_Y, rec="AAB p52")
                       for i, w in enumerate(words)])


CHAIN1 = _chain(("ナットの劣化", "ねじのゆるみ", "かたさが落ちる", "板の震え", "棒が折れる", "機首上げ"))
CHAIN2 = _chain(("ナットの劣化", "ねじのゆるみ", "かたさが落ちる", "板の震え", "リンクが折れる", "機首上げ"))


def chain_links(**kw):
    """鎖の5本の矢印（n1→n2 … n5→n6）。"""
    return [dict(k="edge", fr=f"n{i}", to=f"n{i + 1}", rec="AAB p52", **kw) for i in range(1, 6)]


# 重なった要因（c725）＝AAB p52「Contributing to the accident were the undocumented and untested major modifications … and
#   the pilot's operation of the airplane in the unique air racing environment without adequate flight testing」＝鎖の下に
#   区切りの線を引いて並べるだけ（鎖のどの輪につながるかは報告書が言っていない＝矢印でつながない）
FACTORS = {
    "f_mod": dict(k="role", id="f_mod", t="記録も試験も無い改造", y=700, pos=(160, 860), rec="AAB p52"),
    "f_ops": dict(k="role", id="f_ops", t="十分な試験なしのレース", y=700, pos=(1060, 1760), rec="AAB p52"),
}
# 🆕 ⑤b-7（2026-09-30）：3つの問いの答え（c918）＝台本 c918「先に折れたリンク、ゆるんだねじ、食い違った2つの資料」
#   （AAB p52 の推定原因＝リンクの破損とねじのゆるみ・p17 の2つの手引きの食い違い）と、事故の前にあった手がかり
#   （26年以上のナット＝p41・「ねじが短すぎる」＝p37 の検査の用紙・記録簿の「終えた」＝p15）。上の段＝c109 の問いの名
#   （台本 c109 の画）。🔴 答えと手がかりを矢印でつながない（台本は組にしていない）＝区切りの線の下に並べるだけ
#   ⚠️ 下見（09-30）：問いの箱を node（38px）にすると答えの箱（28px）より目立った＝問いは head（34px・低い箱）に
ANS = dict(heads=[dict(id="q1", t="9秒に何が起きたか", kind="head", x=(110, 650), y=(320, 380), rec="AAB p28"),
                  dict(id="q2", t="なぜ板は震えたか", kind="head", x=(690, 1230), y=(320, 380), rec="AAB p41"),
                  dict(id="q3", t="観客席との距離", kind="head", x=(1270, 1810), y=(320, 380), rec="AAB p19")])
ANSP = {
    "a1": dict(k="role", id="a1", t="先に折れたリンク", y=480, pos=(160, 600), rec="AAB p52"),
    "a2": dict(k="role", id="a2", t="ゆるんだねじ", y=480, pos=(740, 1180), rec="AAB p52"),
    "a3": dict(k="role", id="a3", t="食い違った2つの資料", y=480, pos=(1320, 1760), rec="AAB p17"),
    "k1": dict(k="role", id="k1", t="26年以上のナット", y=690, pos=(160, 600), rec="AAB p41"),
    "k2": dict(k="role", id="k2", t="「ねじが短すぎる」", y=690, pos=(740, 1180), rec="AAB p37"),
    "k3": dict(k="role", id="k3", t="記録簿の「終えた」", y=690, pos=(1320, 1760), rec="AAB p15"),
}


def ans_links():
    """問い → 答え の3本の矢印。"""
    return [dict(k="edge", fr=f"q{i}", to=f"a{i}", rec=ANSP[f"a{i}"]["rec"]) for i in (1, 2, 3)]


# 実況の担当（c806）＝AAB p20「The NCAR announcing team … remained calm and provided clear evacuation procedures guidance to the
#   crowd, assisted first responders, and requested additional help from medical staff on scene」。人の形は描かない（文字の箱だけ）
MC = dict(heads=[dict(id="mc", t="実況の担当", kind="node", x=(150, 560), y=(470, 570), rec="AAB p20")])
MCP = {
    "a_evac": dict(k="role", id="a_evac", t="観客へ避難の案内", y=380, pos=(900, 1500), rec="AAB p20"),
    "a_help": dict(k="role", id="a_help", t="救護の人を手伝う", y=520, pos=(900, 1500), rec="AAB p20"),
    "a_med": dict(k="role", id="a_med", t="医療の応援を頼む", y=660, pos=(900, 1500), rec="AAB p20"),
}
# 2010年の成績（c616）＝AAB p38「started in the last place in the lowest heat in the class. The airplane won a series of races
#   and qualified to run the unlimited class gold race in 2010, but that race was cancelled due to wind」
HEAT = dict(heads=[dict(id="h1", t="いちばん下の組", kind="node", x=(150, 610), y=(430, 530), rec="AAB p38"),
                   dict(id="h2", t="勝ち上がる", kind="node", x=(730, 1190), y=(430, 530), rec="AAB p38"),
                   dict(id="h3", t="ゴールドのレース", kind="node", x=(1310, 1770), y=(430, 530), rec="AAB p38")])

# 書類の再現図（c415・c524・c617・c621・c704・c705・c905）。🔴 本物の書類の写しではない＝「再現」の札と出典・書いてある字は
#   報告書に引かれた文だけ（様式は抽象）。欄の値は記録の値だけ（門番 REC_FORM の values）
#   c415＝AAB p15 注15・p16（2011-07-29 のエンジンの記録簿の総時間 1,453.6＝機体の記録簿の 1,447.2 は 6.4時間の書き違い）
#   c524＝AAB p15（2009-09-22・本人の署名「The prescribed flight test hours have been completed」）
#   c617＝AAB p37（2009年の参加の書類の問い〈前に出たあとの大きな改造〉に「yes」の丸）
#   c621＝AAB p12 注7（2009年と2010年の書類の年齢「59」）
#   c704＝AAB p37（「Remarks」の欄「elev trim tab screws too short …」・2011-09-12 に承認・書面で確かめる手順は無かった）
#   c705＝AAB p37（付録E：技術委員会の承認は「機体の状態や耐空性を表すものではない」＝規則の文を1行に＝様式は抽象）
#   c905＝CAROL p5010（A-12-10：用紙に「指摘」と「直した中身」の書面・再検査まで出さない）
FORM_LOG11 = dict(title="記録簿（2011年7月29日）", rec="AAB p15",
                  fields=[dict(t="機体の総時間", v="1,453.6時間", rec="AAB p16")],
                  paper=(560, 1360, 330, 690), lw=260)
FORM_LOG09 = dict(title="記録簿（2009年9月22日）", rec="AAB p15",
                  fields=[dict(t="試験飛行の時間", v="終えた", rec="AAB p15"),
                          dict(t="署名", v="パイロット本人", rec="AAB p15")],
                  paper=(560, 1360, 300, 740), lw=260)
FORM_ENTRY09 = dict(title="参加の書類（2009年）", rec="AAB p37",
                    fields=[dict(t="大きな改造をしたか", v="はい", rec="AAB p37", late=True)],
                    paper=(460, 1460, 330, 690), lw=340)
FORM_AGE = dict(title="参加の書類（2009年・2010年）", rec="AAB p12",
                fields=[dict(t="年齢", v="59", rec="AAB p12")],
                paper=(560, 1360, 330, 690), lw=200)
FORM_TECH = dict(title="技術検査の用紙", rec="AAB p37",
                 fields=[dict(t="備考", v="トリムタブのねじが短すぎる", rec="AAB p37"),
                         dict(t="承認の日付", v="2011年9月12日", rec="AAB p37")],
                 ends=dict(office=dict(t="レースのコース", rec="AAB p37")),
                 paper=(520, 1300, 300, 740), lw=200)
FORM_RULE = dict(title="技術検査の決まり（付録E）", rec="AAB p37",
                 fields=[dict(t="技術委員会の承認", v="機体の状態や、飛べるかを表さない", rec="AAB p37")],
                 paper=(360, 1560, 330, 690), lw=300)
FORM_NEW = dict(title="技術検査の用紙（事故のあと）", rec="CAROL p5010",
                fields=[dict(t="指摘", rec="CAROL p5010"), dict(t="直した中身", rec="CAROL p5010"),
                        dict(t="再検査", rec="CAROL p5010")],
                ends=dict(office=dict(t="レースのコース", rec="CAROL p5010")),
                paper=(520, 1300, 280, 800), lw=220)

# `apply()` が cuts.ss に差し込む名の全部（上の値と関数＝ss から移したもの）。ここに無い名は ss に置かない
SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK",
            "ILLU_COUNTS",
            "AXIS_DOCS",
            "AX_HIST", "AX_LATE", "AX_A08", "AX_DRILL", "AX_EMS", "AX_UPSET", "AX_NINE", "AXI", "NINE_PTS",
            "_FT", "RENO_TAB", "RENO_REL", "_SLAT", "_SLON", "RAMP_VIEW", "RAMP_PTS", "RAMP_REL", "RAMP_NOTE", "R_BASE", "R_DIMS",
            "ramp_map", "FIELD_VIEW", "FIELD_PTS", "FIELD_REL", "FIELD_NOTE", "field_map", "TOWN_VIEW", "TOWN_PTS",
            "TOWN_PLACES", "town_map", "FLA_VIEW", "FLA_PTS", "FLA_REL", "CIRCLE", "fla_map", "USA_VIEW", "usa_map",
            "QG", "QB",
            "_CX", "CHAIN_Y", "_chain", "CHAIN1", "CHAIN2", "chain_links", "FACTORS", "ANS", "ANSP", "ans_links", "MC", "MCP",
            "HEAT", "FORM_LOG11", "FORM_LOG09", "FORM_ENTRY09", "FORM_AGE", "FORM_TECH", "FORM_RULE", "FORM_NEW")


# ══════════════════════════════════════════════════════════
#  titan_fig.GEO から：15本目の地点（Wikidata P625・2026-09-30 取得）
# ══════════════════════════════════════════════════════════
GEO = {
    # 🆕 15本目（リノ・エアレース2011）⑤b-7（2026-09-30）：Wikidata P625（query.wikidata.org の SPARQL・2026-09-30）
    #   Reno Q49225（市の中心）・Reno Stead Airport Q5796729・Ocala Q918195・Minden, Nevada Q680911・McKinney, Texas Q51697・
    #   Roswell, New Mexico Q33561・Arizona Q816（州の代表点＝札だけに使う）。都市の位置は報告書に無い＝照合の宣言に入れない。
    #   照合は NTSB 資料 #17 p7008 の座標（板の一片が見つかった所＝滑走路8-26 の北側）で空港の点を当てる（`cuts/ss.py` の RENO_REL）
    #   ⚠️ 同じ名の町が多い（Minden は NE・LA・IA ほか・Roswell は GA ほか）＝説明（郡）で選んだ
    "reno_city": (39.526111, -119.8125, "リノの町"),
    "reno_stead": (39.667222, -119.876111, "ステッド空港"),
    "reno_ocala": (29.1875, -82.141389, "オカラ"),
    "reno_minden": (38.955833, -119.769167, "ミンデン"),
    "reno_mckinney": (33.2, -96.633333, "マッキニー"),
    "reno_roswell": (33.394167, -104.522778, "ロズウェル"),
    "reno_az": (34.286667, -111.656944, "アリゾナ州"),
}


# ══════════════════════════════════════════════════════════
#  門番の記録の表（15本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════════
# check_mech の `_FT, _LB = 0.3048, 0.45359237`（メートル・キロ）と同じ値。上の地図の `_FT`（キロ）とは別の物なので名を分けた
#   （REC_MOD の式の中の `_FT`・`_LB` だけ、この2つの名に替えた＝値は同じ）
_MECH_FT, _MECH_LB = 0.3048, 0.45359237

GATES = {
    "check_axis": dict(
        # 🔴 2026-09-30（15本目 ⑤b-2）：15本目の値＝秒の帯（崩れ始めからの秒＝AAB p28 の経過の表・c312）。
        #    0.56秒＝左の板の後ろの縁が21度以上上がった（p28）＝リンクがこのときまでに折れていた（p24・p39）／4.6秒＝一片が離れた（p28）・
        #    本部のパイロンの近くで見つかった（p18）。年表・時間の帯（分・日）の値は ⑤b-5 で足す
        REC_AXIS={
            "0": {"AAB p28"}, "0.27": {"AAB p28"}, "0.56": {"AAB p24", "AAB p28", "AAB p39"}, "0.83": {"AAB p28"},
            "1.3": {"AAB p28"}, "1.44": {"AAB p28"}, "約3.1": {"AAB p28"}, "4.6": {"AAB p18", "AAB p28"}, "約9.1": {"AAB p28"},
            # 🆕 2026-09-30（15本目 ⑤b-5）：年表・時刻の帯・横転の前の秒（原文 ref/ep15/src/ep15_pages.txt で当てた）
            #   p12「delivered … on December 23, 1944 … in July 1946 … surplus and sold … acquired by the accident pilot in July 1983
            #        … raced … from 1983 through 1989 before placing it in storage until 2007 … Between 2007 and 2009 … overhaul」
            "1944-12-23": {"AAB p12"}, "1946-07": {"AAB p12"}, "1983-07": {"AAB p12"},
            "1983": {"AAB p12"}, "1989": {"AAB p12"}, "2007": {"AAB p12"}, "2009": {"AAB p12"},
            "1983-08-17": {"AAB p35"},                              # p35「on August 17, 1983 … special airworthiness certificate」
            "2009-09-21": {"AAB p36"},                              # p36「completion of its major modifications occurred on September 21, 2009」
            "2010": {"AAB p36", "AAB p38"},                         # p36「entered into the 2010 NCAR」・p38
            "2011-09-16": {"AAB p8", "AAB p10", "CAROL p5008"},     # p10「On September 16, 2011」
            #   CAROL p5008（A-12-08）：NTSB の評価（OPEN—ACCEPTABLE RESPONSE）3回・命令の改め・通達の廃止・閉じた日
            "2012-07-25": {"CAROL p5008"}, "2016-11-30": {"CAROL p5008"}, "2020-07-22": {"CAROL p5008"},
            "2020-02-27": {"CAROL p5008"}, "2020-11-03": {"CAROL p5008"}, "2021-07-13": {"CAROL p5008"},
            #   p21「tabletop exercise … on June 2, 2011」「full-scale emergency exercise on May 25, 2011」
            "2011-06-02": {"AAB p21"}, "2011-05-25": {"AAB p21"},
            #   p28 の表（16:24:28.9 に崩れ始め・約9.1秒後に落ちた＝台本 c317「午後4時24分38秒ごろ」）・p20「declared a mass-casualty
            #   incident at 1626」
            "16:24": {"AAB p28"}, "16:26": {"AAB p20"},
            #   p29「About 8 seconds before the beginning of the upset, there was a noticeable reduction in engine manifold pressure and rpm」
            "約-8": {"AAB p29"},
        },
    ),
    "check_qty": dict(
        # 🆕 2026-09-30（15本目 ⑤b-5）：原文 ref/ep15/src/ep15_pages.txt で当てた（型の側 ss.QB とは別に持つ＝§5b-88）
        REC_QTY={          # (群の項目名＝画面の文字, 行の名＝画面の文字) → (値, 頁)
            ("速さ（時速・キロ）", "新幹線（営業の最高）"): (320, {"一般の事実"}),          # 台本 c206 の出典欄
            ("速さ（時速・キロ）", "事故機"): (824, {"AAB p10"}),                          # 445ノット×1.852＝824.1
            ("コースでの速さ（時速・キロ）", "事故の周"): (848, {"AAB p29"}),              # 458ノット＝848.2
            ("コースでの速さ（時速・キロ）", "それまでの最高"): (783, {"AAB p29"}),        # 🔴 848.2−64.8（35ノット）＝報告書の差から引いた値
            ("試験の飛行の時間（分）", "求められた"): (180, {"AAB p36", "AAB p49"}),      # 3 hours of flight time
            ("試験の飛行の時間（分）", "多く見積もっても"): (100, {"AAB p50"}),           # five flights × 20 minutes＝1 hour 40 minutes
            ("試験の飛行の時間（分）", "テレメトリーの記録"): (23, {"AAB p36", "AAB p49"}),  # about 23 minutes
            ("この機体での時間（時間）", "参加の書類"): (2700, {"AAB p12"}),               # 2011年の書類「2,700±」
            ("この機体での時間（時間）", "記録簿の総時間"): (1453.6, {"AAB p15", "AAB p16"}),
            ("この機体での時間（時間）", "書類：前の年から"): (200, {"AAB p51"}),
            ("この機体での時間（時間）", "記録簿：組み立てから"): (25, {"AAB p51"}),
            ("かかったG（重さの何倍か）", "ふつうのコース"): (4, {"CAROL p5011", "CAROL p5012"}),  # normally between 3 and 4 g＝上の端
            ("かかったG（重さの何倍か）", "事故の最大"): (17.3, {"AAB p28"}),
        },
    ),
    "check_boxes": dict(
        # 🆕 2026-09-30（15本目 ⑤b-5）：原文 ref/ep15/src/ep15_pages.txt で当てた（型の側 ss.FACTORS・MCP・FORM_* とは別に持つ）。
        #   流れ図の「role」の箱＝15本目は役職でなく、報告書の文の言葉（重なった要因＝AAB p52・実況の担当がしたこと＝AAB p20）
        REC_OTHER_ROLE={
            "記録も試験も無い改造": {"AAB p52"},        # the undocumented and untested major modifications
            "十分な試験なしのレース": {"AAB p52"},      # operation … in the unique air racing environment without adequate flight testing
            "観客へ避難の案内": {"AAB p20"},            # provided clear evacuation procedures guidance to the crowd
            "救護の人を手伝う": {"AAB p20"},            # assisted first responders
            "医療の応援を頼む": {"AAB p20"},            # requested additional help from medical staff on scene
            # 🆕 ⑤b-7（2026-09-30）：3つの問いの答え（c918）と、事故の前にあった手がかり
            "先に折れたリンク": {"AAB p52"},            # failure of the left trim tab link assembly（p28 の表＝0.56秒に板が21度以上）
            "ゆるんだねじ": {"AAB p52"},                # allowed the trim tab attachment screws to become loose
            "食い違った2つの資料": {"AAB p17"},         # A comparison of the two FAA guidance documents revealed …
            "26年以上のナット": {"AAB p41"},            # the locknuts had likely been installed for at least 26 years
            "「ねじが短すぎる」": {"AAB p37"},          # "elev trim tab screws too short"（技術検査の用紙の備考）
            "記録簿の「終えた」": {"AAB p15"},          # The prescribed flight test hours have been completed
        },
        # 🆕 15本目：報告書の鎖（AAB p52 の推定原因）・実況の担当（p20）・2010年の成績（p38）の箱の言葉
        REC_MECH={"ナットの劣化", "ねじのゆるみ", "かたさが落ちる", "板の震え", "棒が折れる", "リンクが折れる", "機首上げ",
                  "実況の担当", "いちばん下の組", "勝ち上がる", "ゴールドのレース",
                  # 🆕 ⑤b-7：c918 の上の段＝c109 の3つの問いの名（台本 c109 の画）と、手がかりの見出し（台本 c918 の3行目）
                  "9秒に何が起きたか", "なぜ板は震えたか", "観客席との距離", "事故の前の手がかり"},
        REC_CHIP={"風で中止": {"AAB p38"}},           # that race was cancelled due to wind
        # 🆕 15本目：書類の再現図（表題 → 欄の名・行き来の箱・欄の値＝記録の文にある値だけ・頁）
        REC_FORM={
            "記録簿（2011年7月29日）": dict(fields={"機体の総時間"}, ends=set(), values={"機体の総時間": "1,453.6時間"},
                                          rec={"AAB p15", "AAB p16"}),
            "記録簿（2009年9月22日）": dict(fields={"試験飛行の時間", "署名"}, ends=set(),
                                          values={"試験飛行の時間": "終えた", "署名": "パイロット本人"}, rec={"AAB p15"}),
            "参加の書類（2009年）": dict(fields={"大きな改造をしたか"}, ends=set(), values={"大きな改造をしたか": "はい"},
                                     rec={"AAB p37"}),
            "参加の書類（2009年・2010年）": dict(fields={"年齢"}, ends=set(), values={"年齢": "59"}, rec={"AAB p12"}),
            "技術検査の用紙": dict(fields={"備考", "承認の日付"}, ends={"レースのコース"},
                                values={"備考": "トリムタブのねじが短すぎる", "承認の日付": "2011年9月12日"}, rec={"AAB p37"}),
            "技術検査の決まり（付録E）": dict(fields={"技術委員会の承認"}, ends=set(),
                                         values={"技術委員会の承認": "機体の状態や、飛べるかを表さない"}, rec={"AAB p37"}),
            "技術検査の用紙（事故のあと）": dict(fields={"指摘", "直した中身", "再検査"}, ends={"レースのコース"}, values={},
                                          rec={"CAROL p5010"}),
        },
    ),
    "check_mech": dict(
        # ── 15本目 ⑤b-4：改造の比べ（mod）・ねじとナットとフラッター（bolt）の記録の値＝門番の側に独立して持つ
        #    （型の定数を読まない＝型の定数を壊す陽性対照が捕まえられる）──
        REC_MOD=dict(span_stock=(37 + (5 / 16) / 12) * _MECH_FT,    # 11.286 メートル（AAB p13）
                     span_mod=(28 + 10 / 12) * _MECH_FT,            # 8.788
                     cw_ratio=26.0 / 13.75,                    # 左の昇降舵のおもり／資料のふつうの最大（AAB p14）
                     cw_kg=26.0 * _MECH_LB,                         # 11.79 キロ（AAB p14）
                     bw_ratio=(8 + 2 / 3) / 20.0),             # 動きを安定させるおもり（#53 p10＝推定）＜ 0.5（AAB p43「半分未満」）
        REC_BOLT=dict(len_ratio=0.96 / 1.219,                  # 実際のねじ／決まりのねじ（#40 p2・p6＝頭の下の長さ）
                      flights=3,                               # 締め直しのあとの飛行（AAB p41）
                      shake_deg=(10.0, 20.0), wobble_deg=(3.0, 8.0)),   # 板の揺れの幅（模式＝震えはぐらつきより大きい）
    ),
}


_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・titan_fig.GEO・（gate を渡せば）その門番の記録の表を15本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss と GEO は触らない）＝14本目の見本 `fixture_ep14` と重ねるとき
    （check_mech の selftest は14本目と15本目の検算を1つの処理で回す＝先に14本目を全部差し込み、15本目は表だけ足す）。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が15本目の表で
       16本目の画を測る）。apply の前に**無かった名**（ss の RAMP_VIEW・FORM_LOG11 …／門番の表）も覚えて、restore で**消す**
       ＝selftest のあとに15本目の名が本番へ残らない（fixture_ep14 は上書きした名を戻すだけだった）"""
    saved = dict(ss={}, ss_new=[], geo=None, gate=gate, tables={}, tables_new=[])
    if not tables_only:
        import titan_fig as F
        from cuts import ss
        saved["ss"] = {n: getattr(ss, n) for n in SS_NAMES if hasattr(ss, n)}
        saved["ss_new"] = [n for n in SS_NAMES if not hasattr(ss, n)]
        saved["geo"] = dict(F.GEO)
    tabs = {}
    if gate is not None:
        name = Path(getattr(gate, "__file__", "") or "").stem
        tabs = GATES.get(name, {})
        for k in tabs:
            if hasattr(gate, k):
                saved["tables"][k] = getattr(gate, k)
            else:
                saved["tables_new"].append(k)
    _SAVED.append(saved)         # 覚えてから差し込む＝途中で落ちても restore() が戻せる
    if not tables_only:
        g = globals()
        for n in SS_NAMES:
            setattr(ss, n, g[n])
        F.GEO.update(GEO)
    for k, v in tabs.items():
        setattr(gate, k, v)


def restore():
    """apply() の前の本番の値に戻す（selftest のあと・本番の照合の前に呼ぶ）。apply を呼んでいなければ何もしない。
    ss と門番の表は、apply の前に無かった名を消す。GEO は fixture_ep14 と同じに、覚えた写しで入れ替える（clear → update）。
    tables_only で差し込んだ分は ss・GEO を覚えていない＝戻さない（先に差し込んだ別の見本を壊さない）。LIFO（あとに apply した順）"""
    while _SAVED:
        s = _SAVED.pop()
        if s["geo"] is not None:
            import titan_fig as F
            from cuts import ss
            for n, v in s["ss"].items():
                setattr(ss, n, v)
            for n in s["ss_new"]:
                if hasattr(ss, n):
                    delattr(ss, n)
            F.GEO.clear()
            F.GEO.update(s["geo"])
        gate = s["gate"]
        for k, v in s["tables"].items():
            setattr(gate, k, v)
        for k in s["tables_new"]:
            if hasattr(gate, k):
                delattr(gate, k)
