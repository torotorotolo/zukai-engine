# -*- coding: utf-8 -*-
"""14本目（セウォル号）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-09-30（15本目 リノ ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `dc6ecf4` と同じ・注は一部短くした）
  ・`cuts/ss.py` の後半＝案C の出典の表・割れる時刻・軸の型・地図・量の型・箱の型の値（14本目 ⑤b-2〜⑤b-7b）
  ・`titan_fig.GEO` の14本目の地点（韓国の港と島 13点＝⑤b-4・⑤b-7a）
  ・門番の記録の表（check_axis・check_qty・check_boxes・check_mech）
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を14本目の実物で確かめている＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は15本目の空の器にした。
■ 使い方（selftest の中だけ）:
      import fixture_ep14
      fixture_ep14.apply(sys.modules[__name__])   # その処理の中だけ ss・GEO・この門番の記録の表が14本目になる
  🔴 本番の門番・合成からは呼ばない（呼ぶと15本目以降の画に14本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ 見本の頁の原文 `ref/ep14/src/sewol_pages.txt` は git の外（手元だけ）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep14"


# ══════════════════════════════════════════════════════════
#  cuts/ss.py から：案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）── 14本目 ⑤b-2
# ══════════════════════════════════════════════════════════
REC_PAGES = REF / "src" / "sewol_pages.txt"
REC_DOCS = {
    "判決": dict(range=(1, 81), name="大法院 判決（2015年）", page="print", base=0),
    "海審": dict(range=(1001, 1138), name="海洋安全審判院 特別調査報告（2014年）", page="pdf", base=1000),
    "裁決": dict(range=(2001, 2174), name="中央海洋安全審判院 裁決（2026年）", page="pdf", base=2000),
    "特調委": dict(range=(3001, 3330), name="社会的惨事特別調査委員会 報告（2022年）", page="pdf", base=3000),
    "特調委小": dict(range=(4001, 4486), name="社会的惨事特別調査委員会 小委員会報告（2022年）", page="pdf", base=4000),
    "艇長の判決": dict(range=(5001, 5002), name="123艇の艇長の判決", page=None, base=0),
    "幹部の判決": dict(range=(5003, 5004), name="海洋警察の幹部の判決", page=None, base=0),
    "会社の判決": dict(range=(5005, 5005), name="清海鎮海運の判決", page=None, base=0),
    "船員の1審": dict(range=(5006, 5006), name="船員の1審判決（光州地裁）", page=None, base=0),
    "船員の2審": dict(range=(5007, 5007), name="船員の2審判決（光州高裁）", page=None, base=0),
}
ILLU_SPLIT_TIMES = ("8:48", "8:49", "8:52", "8:54", "8:56", "8:58", "9:30", "9:32", "9:33", "9:35", "9:46", "9:48")
ILLU_CROWD_UNTIL = "9:47"

# 軸の型（`tools/axis.py`・14本目 ⑤b-5）
AXIS_DOCS = {"判決": "判決", "海審": "報告書", "艇長の判決": "艇長の判決", "特調委": "特別調査委",
             "幹部の判決": "幹部の判決", "裁決": "裁決", "船員の2審": "2審の判決"}
AX_SHIP = dict(view="date", span=("1993", "2015"), ticks=("1994", "1998", "2002", "2006", "2010", "2014"))
AX_BUILD = dict(view="date", span=("1993-12", "1994-06"),
                ticks=("1994-01", "1994-02", "1994-03", "1994-04", "1994-05", "1994-06"))
AX_KAIZO = dict(view="date", span=("2012-09", "2013-05"),
                ticks=("2012-09", "2012-10", "2012-11", "2012-12", "2013-01", "2013-02", "2013-03", "2013-04", "2013-05"))
AX_CAUSE = dict(view="date", span=("2012-07", "2027"), ticks=("2014", "2016", "2018", "2020", "2022", "2024", "2026"))
AX_NIGHT = dict(view="clock", span=("18:00", "翌10:00"),
                ticks=("18:00", "20:00", "22:00", "翌0:00", "翌2:00", "翌4:00", "翌6:00", "翌8:00", "翌10:00"))
AX_0850 = dict(view="clock", span=("8:48", "9:02"), ticks=("8:50", "8:55", "9:00"))
AX_TALK = dict(view="lanes", span=("9:04", "9:40"), ticks=("9:05", "9:10", "9:15", "9:20", "9:25", "9:30", "9:35", "9:40"),
               lanes=("管制", "近くの船", "セウォル号"))
AXI = {
    "accident": dict(k="pt", at="2014-04-16", t="事故", rec="海審 p1008", c="ALERT"),
    "keel": dict(k="pt", at="1994-01-25", t="工事の始まり", rec="海審 p1013"),
    "launch": dict(k="pt", at="1994-04-01", t="進水", rec="海審 p1013"),
    "japan": dict(k="span", a="1994-04-01", b="2012-10-08", t="日本", rec=["海審 p1013", "海審 p1016"], c="INST"),
    "naminoue": dict(k="span", a="1994-04-01", b="2012-10-08", t="なみのうえ", rec=["海審 p1013", "海審 p1016"], c="INST"),
    "import": dict(k="pt", at="2012-10-08", t="導入", rec="海審 p1016"),
    "kaizo": dict(k="span", a="2012-10-12", b="2013-02-12", t="改造", rec="海審 p1016", c="AMBER"),
    "first": dict(k="pt", at="2013-03-16", t="初めての運航", rec="海審 p1026"),
    "incline": dict(k="pt", at="2013-01-24", t="傾斜試験", rec="海審 p1022"),
    "kmst": dict(k="pt", at="2014-12-29", t="海洋安全審判院", rec="海審 p1001", c="INST", anchor="end", fmt="ym"),
    "court": dict(k="pt", at="2015", t="裁判所", rec="船員の2審 p5007", c="INST", anchor="start"),
    "raise": dict(k="pt", at="2017-03-23", t="引き揚げ", rec="特調委 p3061", c="INST", anchor="end", fmt="ym"),
    "hull18": dict(k="pt", at="2018-08", t="船体調査委員会", rec="特調委 p3073", c="INST", anchor="start"),
    "sccc": dict(k="pt", at="2022-09", t="特別調査委員会", rec="特調委 p3006", c="INST"),
    "kmst26": dict(k="pt", at="2026-01-28", t="中央海洋安全審判院", rec="裁決 p2001", c="INST", fmt="ym"),
    "dep_plan": dict(k="pt", at="18:30", t="出港の予定", rec="海審 p1026"),
    "arr_plan": dict(k="pt", at="翌9:10", t="着く予定", rec="海審 p1026"),
    "plan": dict(k="span", a="18:30", b="翌9:10", t="予定の航海", rec="海審 p1026"),
    "t0906": dict(k="link", at="9:06", fr="管制", to="セウォル号", rec="海審 p1059"),
    "t0913": dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="判決 p13"),
    "t0914": dict(k="link", at="9:14", fr="管制", to="セウォル号", rec="海審 p1059"),
    "t0924": dict(k="link", at="9:24", fr="近くの船", to="セウォル号", rec="判決 p14"),
    "t0937": dict(k="link", at="9:37", fr="セウォル号", to="管制", rec="海審 p1061"),
}
CAUSE_NOTE = "年表：機関の名と、その機関が挙げた原因の項目だけ（原因は今も1つに決まっていない）"

# 断面F（`tools/hull.py`）と地図（drift）── 14本目 ⑤b-4
HULL_NOTE = "模式図：形は報告書の要目と構造の文から（部屋の前後の位置・通路の幅は模式）"
MAP_PTS = {
    "acc": dict(lat=34 + 9 / 60 + 34 / 3600, lon=125 + 57 / 60 + 56 / 3600),     # 海審 p1065
    "ch": dict(mid=["maenggoldo", "seogeochado"]),                              # 海審 p1046
    "appr": dict(of="ch", km=7.0, deg=340),                                      # 位置は模式
    "t0846": dict(of="byeongpungdo", km=1.667, deg=46),                          # 海審 p1046
}
MAP_REL_ACC = dict(a="acc", lat=MAP_PTS["acc"]["lat"], lon=MAP_PTS["acc"]["lon"], tol_km=0.3, src="海審 p1065")
MAP_REL_NE = dict(a="byeongpungdo", b="acc", km=2.41, dir="北東", sector=8, src="海審 p1065")
MAP_REL_0846 = dict(a="t0846", b="byeongpungdo", km=1.667, src="海審 p1046")
ROUTE = ["incheon", "palmido", "ongdo", "eocheongdo", "heuksando", "ch", "t0846", "acc"]
ROUTE_PLAN = ["acc", "chujado", "jeju"]
MAP_VIEWS = {
    "wide": dict(view=dict(lon=(125.2, 126.9), lat=(33.40, 37.66)), scale_km=100, grid=1.0,
                 places=[dict(k="incheon", dx=130), dict(k="jeju", dx=60), dict(k="jindo", side="above", dx=40)],
                 rel=[MAP_REL_ACC], note="模式図：航路は報告書の通った島を直線で結んだもの（実際の線ではない）。港と島は中心の1点"),
    "local": dict(view=dict(lon=(125.62, 126.28), lat=(34.10, 34.30)), scale_km=5, grid=0.1,
                  places=["maenggoldo", dict(k="seogeochado", side="above"), "byeongpungdo"],
                  rel=[MAP_REL_ACC, MAP_REL_NE], note="模式図：島は中心の1点（形は描いていない）。船の位置は報告書の値から"),
    "near": dict(view=dict(lon=(125.86, 126.06), lat=(34.125, 34.195)), scale_km=1, grid=0.05,
                 places=["byeongpungdo"], rel=[MAP_REL_ACC, MAP_REL_NE, MAP_REL_0846],
                 note="模式図：島は中心の1点（形は描いていない）。船の位置は報告書の値から"),
}
MAP_LAB = {"wide": dict(_l1=dict(lat=36.9, lon=125.35), _r1=dict(lat=35.2, lon=126.75)),
           "local": dict(_l1=dict(lat=34.285, lon=125.66), _r1=dict(lat=34.285, lon=126.12)),
           "near": dict(_l1=dict(lat=34.19, lon=125.875), _r1=dict(lat=34.137, lon=126.035))}


def sewol_map(which, steps, rel=None, note=None, recs=None, dial=None, places=None, drop=()):
    """14本目の地図（drift）。which＝wide／local／near。places＝足す地点・drop＝外す地点の名。"""
    from cuts import ss
    m = MAP_VIEWS[which]
    pts = dict(MAP_PTS, **MAP_LAB[which])
    base = [p for p in m["places"] if (p if isinstance(p, str) else p["k"]) not in set(drop)]
    return ("drift", dict(view=m["view"], places=base + list(places or []), pts=pts,
                          rel=list(m["rel"]) + list(rel or []),
                          steps=steps, note=note or m["note"], src=ss.src(recs or ["海審 p1065"]), scale_km=m["scale_km"],
                          grid=m["grid"], dial=dial))


# 2つの問い（c105 の型）を戻すカット ── 14本目 ⑤b-7b
Q1_TILT = dict(state=dict(heel=30.0), rec="判決 p12・海審 p1056（約30度）", delay=0.6, dur=1.5)
Q2_BOARD = dict(board=8, gap=0.3, rec="判決 p18（123艇に乗った）")


def q_pair(n, left, right, lv="", rv=""):
    """n＝台本の行の数。left／right＝(出る段, 絵の段の list＝n 個)。lv／rv＝問いの下の小さな字。"""
    (ls, lsteps), (rs, rsteps) = left, right
    lstart = {} if any(st.get("state", {}).get("heel") for st in lsteps) else dict(heel=30.0)
    lrec = {} if lstart == {} else dict(rec="判決 p12・海審 p1056（約30度）")
    ppl = (dict(people=dict(crew=(8, "判決 p11（操舵室に集まった甲板部の8人）")))
           if any(st.get("board") for st in rsteps) else {})
    return ("illu_pair", dict(blocks=[
        dict(k="問い1", t="なぜ傾いたか", v=lv, stage=ls, stages=n,
             scene=dict(place="A", at="8:50", start=lstart, steps=lsteps, **lrec)),
        dict(k="問い2", t="なぜ助からなかったか", v=rv, stage=rs, stages=n,
             scene=dict(place="D", at="9:46", start=dict(heel=61.2), rec="判決 p18・海審 p1057", steps=rsteps, **ppl))]))


# 量の型（`tools/qty.py`）と箱の型（`tools/boxes.py`）── 14本目 ⑤b-6
QG = {
    "cargo": dict(id="cargo", t="積める貨物の上限（トン）", ticks=(0, 500, 1000, 1500, 2000, 2500)),
    "pax": dict(id="pax", t="乗せられる人の数（人）", ticks=(0, 200, 400, 600, 800, 1000)),
    "load": dict(id="load", t="貨物の重さ（トン）", ticks=(0, 500, 1000, 1500, 2000, 2500), rows=("上限", "積み荷")),
    "pair": dict(id="pair", t="重さ（トン）", ticks=(0, 500, 1000, 1500, 2000, 2500)),
}
QB = {
    "cargo_before": dict(k="bar", g="cargo", t="改造の前", v=2437, rec="海審 p1018"),
    "cargo_after": dict(k="bar", g="cargo", t="改造の後", v=987, rec="海審 p1018", c="AMBER"),
    "pax_before": dict(k="bar", g="pax", t="改造の前", v=840, rec="海審 p1018"),
    "pax_after": dict(k="bar", g="pax", t="改造の後", v=956, rec="海審 p1018", c="AMBER"),
    "load_limit": dict(k="bar", g="load", t="上限", v=987, rec="海審 p1041", c="AMBER"),
    "load_real": dict(k="bar", g="load", t="積み荷", v=2142.7, rec="海審 p1041", c="ALERT"),
    "pair_cargo": dict(k="bar", g="pair", t="貨物", v=987, rec="海審 p1043", c="AMBER"),
    "pair_water": dict(k="bar", g="pair", t="バラスト", v=1703, rec="海審 p1043"),
}
PEOPLE_ORDER = (("生徒", 325), ("先生", 14), ("一般の乗客", 104), ("船員", 15), ("調理・事務の係", 8),
                ("ほか（アルバイトなど）", 10))
PEOPLE_SETS = {"乗客": ("生徒", "先生", "一般の乗客"), "船で働く人": ("船員", "調理・事務の係", "ほか（アルバイトなど）")}
PEOPLE_REC = {"乗客": "海審 p1038", "生徒": "海審 p1038", "先生": "海審 p1038", "一般の乗客": "海審 p1038",
              "船で働く人": "海審 p1038", "船員": "海審 p1038", "調理・事務の係": "海審 p1038",
              "ほか（アルバイトなど）": "海審 p1038・p1039"}
PEOPLE_CUTS = ("c204", "c205", "c206")

CT = dict(
    cols=dict(who=(84, 304), crime=(364, 604), c1=(680, 960), c2=(1040, 1320), c3=(1400, 1760)),
    heads=[dict(id="c1", t="1審", col="c1", rec="船員の1審 p5006"), dict(id="c2", t="2審", col="c2", rec="船員の2審 p5007"),
           dict(id="c3", t="大法院", col="c3", rec="判決 p1")],
    head_y=(232, 292), chain=True,
    seats=dict(col="c3", n=13, y=306, t="裁判官", rec=["判決 p79", "判決 p80", "判決 p81"]),
    bounds=(642, 1000, 1360), guide_y=(346, 850),
    rows={"船長": 392, "1等航海士": 444, "2等航海士": 496, "機関長": 548, "3等航海士": 600, "操舵手（当直）": 652,
          "会社の代表": 744, "123艇の艇長": 796},
)


def _cr(i, t, row, rec="判決 p2"):
    return dict(k="role", id=i, t=t, row=row, rec=rec)


def _ce(fr, to, **kw):
    return dict(k="edge", fr=fr, to=to, **kw)       # ＝ss.ce（CREW15 を組むために写した）


CTP = {
    "r_captain": _cr("r_captain", "船長", "船長"),
    "r_mate1": _cr("r_mate1", "1等航海士", "1等航海士"),
    "r_mate2": _cr("r_mate2", "2等航海士", "2等航海士"),
    "r_chief": _cr("r_chief", "機関長", "機関長"),
    "r_mate3": _cr("r_mate3", "3等航海士", "3等航海士"),
    "r_helm": _cr("r_helm", "操舵手（当直）", "操舵手（当直）", ["判決 p2", "判決 p33"]),
    "r_ceo": _cr("r_ceo", "会社の代表", "会社の代表", ["会社の判決 p5005", "民事の判決 N"]),
    "r_123": _cr("r_123", "123艇の艇長", "123艇の艇長", ["艇長の判決 p5001", "艇長の判決 p5002"]),
    "x_cap": dict(k="crime", id="x_cap", t="殺人・殺人未遂", row="船長", rec=["判決 p18", "判決 p21"]),
    "x_murder": dict(k="crime", id="x_murder", t="殺人", y=470, rec="判決 p24"),
    "x_aband": dict(k="crime", id="x_aband", t="遺棄致死など", y=522, rec="判決 p1"),
    "x_rudder": dict(k="crime", id="x_rudder", t="舵の過失", rows=("3等航海士", "操舵手（当直）"), rec="判決 p33"),
    "o_cap": dict(k="res", id="o_cap", t="有罪", col="c3", row="船長", rec="判決 p39"),
    "o_murder": dict(k="res", id="o_murder", t="無罪", col="c3", y=470, rec="判決 p24"),
    "o_aband": dict(k="res", id="o_aband", t="有罪", col="c3", y=522, rec="判決 p1"),
    "o_rud2": dict(k="res", id="o_rud2", t="無罪", col="c2", rows=("3等航海士", "操舵手（当直）"), rec="判決 p34"),
    "o_rud3": dict(k="res", id="o_rud3", t="無罪", col="c3", rows=("3等航海士", "操舵手（当直）"), rec="判決 p34"),
    "s_captain": dict(k="res", id="s_captain", t="無期懲役", col="c3", row="船長", rec="船員の2審 p5007"),
    "s_mate1": dict(k="res", id="s_mate1", t="懲役12年", col="c3", row="1等航海士", rec="船員の2審 p5007"),
    "s_mate2": dict(k="res", id="s_mate2", t="懲役7年", col="c3", row="2等航海士", rec="船員の2審 p5007"),
    "s_chief": dict(k="res", id="s_chief", t="懲役10年", col="c3", row="機関長", rec="船員の2審 p5007"),
    "s_mate3": dict(k="res", id="s_mate3", t="懲役5年", col="c3", row="3等航海士", rec="船員の2審 p5007"),
    "s_helm": dict(k="res", id="s_helm", t="懲役5年", col="c3", row="操舵手（当直）", rec="船員の2審 p5007"),
    "s_ceo": dict(k="res", id="s_ceo", t="懲役7年", col="c3", row="会社の代表", rec="民事の判決 N"),
    "s_123": dict(k="res", id="s_123", t="懲役3年", col="c3", row="123艇の艇長", rec="艇長の判決 p5002"),
}

CREW15 = [dict(k="grp", t="甲板部", x=84, y=372)]
for _i, (_t, _y, _c) in enumerate([("船長", 412, "who"), ("1等航海士", 412, "crime"), ("2等航海士", 460, "who"),
                                   ("3等航海士", 460, "crime"), ("操舵手（当直）", 508, "who"), ("航海士", 508, "crime"),
                                   ("操舵手", 556, "who"), ("操舵手", 556, "crime")]):
    CREW15.append(dict(k="role", id=f"d{_i + 1}", t=_t, y=_y, pos=CT["cols"][_c], grp="甲板部",
                       rec=["判決 p2", "判決 p33"] if _t == "操舵手（当直）" else "判決 p2"))
CREW15.append(dict(k="grp", t="機関部", x=84, y=626))
for _i, (_t, _y, _c) in enumerate([("機関長", 666, "who"), ("1等機関士", 666, "crime"), ("3等機関士", 714, "who"),
                                   ("操機長", 714, "crime"), ("操機手", 762, "who"), ("操機手", 762, "crime"),
                                   ("操機手", 810, "who")]):
    CREW15.append(dict(k="role", id=f"e{_i + 1}", t=_t, y=_y, pos=CT["cols"][_c], grp="機関部",
                       rec="判決 p2" if _i < 3 else "判決 p3"))
CREW15.append(dict(k="bracket", id="br15", over=[f"d{i}" for i in range(1, 9)] + [f"e{i}" for i in range(1, 8)]))
CREW15.append(_ce("br15", "c1"))

RUD = dict(kind="模式図",
           heads=[dict(id="helm", t="操舵台", kind="node", x=(150, 470), y=(470, 570), rec="海審 p1118"),
                  dict(id="valve", t="ソレノイド弁", kind="node", x=(760, 1160), y=(470, 570), rec="海審 p1118"),
                  dict(id="rudder", t="舵", kind="node", x=(1450, 1770), y=(470, 570), rec="海審 p1118")])
RUDP = {
    "q_valve": dict(k="mark", at="valve", t="？"),
    "e_elec": dict(k="edge", fr="helm", to="valve", lab="電気の信号", rec="海審 p1118"),
    "e_oil": dict(k="edge", fr="valve", to="rudder", lab="油の流れ", rec="海審 p1118"),
    "c_kmst": dict(k="chip", id="c_kmst", at="valve", t="報告書：退けた", dy=60, rec="海審 p1118"),
    "c_sccc": dict(k="chip", id="c_sccc", at="valve", t="特別調査委：可能性は非常に低い", dy=130, rec="特調委 p3013"),
}
FORM_PRE = dict(title="出港前安全点検報告書", rec="海審 p1037",
                fields=[dict(t="乗船人員", rec="海審 p1037"), dict(t="貨物量", rec="海審 p1037")],
                ends=dict(ship=dict(t="セウォル号", rec="海審 p1037"), office=dict(t="運航管理室", rec="海審 p1037")))
CAUSE = {
    "rudder": dict(k="item", t="舵の使い方？", rec=["海審 p1091", "裁決 p2087"]),
    "fault": dict(k="item", t="装置の故障？", rec=["判決 p33", "特調委 p3073"]),
    "outer": dict(k="item", t="外からの力？", rec=["特調委 p3013", "特調委小 p4161"]),
}

# 🆕 2026-09-30（15本目 ⑤b-2）：15本目で足した表（秒の札・時計の札・描いてよい数）＝14本目には無かった＝空（門番はその回の表が
#    空なら測らない）。apply() が本番の15本目の値を消して14本目の見本だけで回す
ILLU_SEC_OK = {}
ILLU_CLOCK_OK = ()
ILLU_COUNTS = {}
# 🆕 2026-09-30（15本目 ⑤b-3）：置いてよい役割は回ごとの表（ss.ILLU_ROLES）になった＝14本目の値（船員・海洋警察・管制の型紙と
#    乗客の群れ＝illu.ROLES と check_illu.CROWD_ROLES の既定と同じ）
ILLU_ROLES = dict(sprite=("crew", "coast_guard", "control"), crowd=("passengers",))

SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ROLES",
            "AXIS_DOCS",
            "AX_SHIP", "AX_BUILD", "AX_KAIZO", "AX_CAUSE", "AX_NIGHT", "AX_0850", "AX_TALK", "AXI", "CAUSE_NOTE",
            "HULL_NOTE", "MAP_PTS", "MAP_REL_ACC", "MAP_REL_NE", "MAP_REL_0846", "ROUTE", "ROUTE_PLAN", "MAP_VIEWS",
            "MAP_LAB", "sewol_map", "Q1_TILT", "Q2_BOARD", "q_pair", "QG", "QB", "PEOPLE_ORDER", "PEOPLE_SETS",
            "PEOPLE_REC", "PEOPLE_CUTS", "CT", "CTP", "CREW15", "RUD", "RUDP", "FORM_PRE", "CAUSE")


# ══════════════════════════════════════════════════════════
#  titan_fig.GEO から：14本目の地点（Wikidata P625・2026-09-29 取得）
# ══════════════════════════════════════════════════════════
GEO = {
    "incheon": (37.460105, 126.624899, "インチョン港"),
    "jeju": (33.52239444, 126.54078611, "チェジュ港"),
    "palmido": (37.358070721, 126.511861096, "パルミド"),
    "ongdo": (36.6475, 126.008333333, "オンド"),
    "eocheongdo": (36.11667, 125.97972, "オチョンド"),
    "heuksando": (34.666666666, 125.416666666, "フクサンド"),
    "maenggoldo": (34.211388888, 125.856666666, "メンゴルド"),
    "seogeochado": (34.2514, 125.908, "ソゴチャド"),
    "donggeochado": (34.23639, 125.93861, "トンゴチャド"),
    "byeongpungdo": (34.1489, 125.944, "ピョンプンド"),
    "chujado": (33.96111, 126.29167, "チュジャド"),
    "jindo": (34.4575, 126.253333333, "チンド"),
    "mokpo": (34.793611111, 126.388611111, "モッポ"),
}


# ══════════════════════════════════════════════════════════
#  門番の記録の表（14本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════════
GATES = {
    "check_axis": dict(
        REC_AXIS={
            "1994-01-25": {"海審 p1013"}, "1994-04-01": {"海審 p1013"}, "2012-10-08": {"海審 p1016"},
            "2012-10-12": {"海審 p1016"}, "2013-02-12": {"海審 p1016"}, "2013-01-24": {"海審 p1022"},
            "2013-03-16": {"海審 p1026"}, "2014-04-16": {"海審 p1001", "海審 p1008"},
            "2014-12-29": {"海審 p1001"}, "2015": {"船員の2審 p5007"}, "2017-03-23": {"特調委 p3061"},
            "2018-08": {"特調委 p3073"}, "2022-09": {"特調委 p3006"}, "2026-01-28": {"裁決 p2001"},
            "18:30": {"海審 p1026"}, "翌9:10": {"海審 p1026"}, "21:05": {"海審 p1038"},
            "8:52": {"海審 p1059", "艇長の判決 p5002"}, "8:54": {"艇長の判決 p5002"}, "8:56": {"海審 p1053"},
            "8:58": {"判決 p12", "艇長の判決 p5002"}, "9:10": {"海審 p1054"}, "9:50": {"海審 p1055"},
            "9:06": {"海審 p1059"}, "9:13": {"判決 p13"}, "9:14": {"海審 p1059"}, "9:24": {"判決 p14"}, "9:37": {"海審 p1061"},
            "9:30": {"艇長の判決 p5002", "海審 p1054", "海審 p1060"}, "9:32": {"特調委 p3098"}, "9:33": {"幹部の判決 p5003"},
            "9:35": {"判決 p17"}, "9:46": {"判決 p18"}, "9:48": {"海審 p1055"},
            "10:31": {"海審 p1049", "海審 p1057"}, "11:28": {"海審 p1061"}, "12:19": {"海審 p1060"},
        },
        LANES_OK={"管制", "近くの船", "セウォル号"},
    ),
    "check_qty": dict(
        REC_QTY={
            ("積める貨物の上限（トン）", "改造の前"): (2437, {"海審 p1018"}),
            ("積める貨物の上限（トン）", "改造の後"): (987, {"海審 p1018"}),
            ("乗せられる人の数（人）", "改造の前"): (840, {"海審 p1018"}),
            ("乗せられる人の数（人）", "改造の後"): (956, {"海審 p1018"}),
            ("貨物の重さ（トン）", "上限"): (987, {"海審 p1041"}),
            ("貨物の重さ（トン）", "積み荷"): (2142.7, {"海審 p1041"}),
            ("重さ（トン）", "貨物"): (987, {"海審 p1043"}),
            ("重さ（トン）", "バラスト"): (1703, {"海審 p1043"}),
        },
        REC_GHOST={("積める貨物の上限（トン）", "改造の後"): (2437, {"海審 p1018"})},
        REC_GRID={"判定の項目": dict(n=9, ok=5, ng=4, rec={"海審 p1080"})},
        REC_PEOPLE={"乗っていた人": 476, "乗客": 443, "生徒": 325, "先生": 14, "一般の乗客": 104,
                    "船で働く人": 33, "船員": 15, "調理・事務の係": 8, "ほか（アルバイトなど）": 10},
        REC_PEOPLE_PAGES={"海審 p1038", "海審 p1039", "海審 p1038・p1039", "海審 p1062"},
        PEOPLE_CUTS={"c204", "c205", "c206"},
    ),
    "check_boxes": dict(
        REC_CREW={"甲板部": ["船長", "1等航海士", "2等航海士", "3等航海士", "操舵手（当直）", "航海士", "操舵手", "操舵手"],
                  "機関部": ["機関長", "1等機関士", "3等機関士", "操機長", "操機手", "操機手", "操機手"]},
        REC_ROLE_PAGES={"判決 p2", "判決 p3", "判決 p33"},
        REC_OTHER_ROLE={"会社の代表": {"会社の判決 p5005", "民事の判決 N"},
                        "123艇の艇長": {"艇長の判決 p5001", "艇長の判決 p5002"}},
        REC_CRIME={"殺人・殺人未遂": {"判決 p18", "判決 p21"}, "殺人": {"判決 p24"}, "遺棄致死など": {"判決 p1"},
                   "舵の過失": {"判決 p33"}},
        REC_VERDICT={
            ("船長", "殺人・殺人未遂", "c3"): ("有罪", {"判決 p39"}),
            **{(r, "殺人", "c3"): ("無罪", {"判決 p24"}) for r in ("1等航海士", "2等航海士", "機関長")},
            **{(r, "遺棄致死など", "c3"): ("有罪", {"判決 p1"}) for r in ("1等航海士", "2等航海士", "機関長")},
            **{(r, "舵の過失", c): ("無罪", {"判決 p34"}) for r in ("3等航海士", "操舵手（当直）") for c in ("c2", "c3")},
        },
        REC_SENT={
            "船長": ("無期懲役", {"船員の2審 p5007"}), "1等航海士": ("懲役12年", {"船員の2審 p5007"}),
            "2等航海士": ("懲役7年", {"船員の2審 p5007"}), "機関長": ("懲役10年", {"船員の2審 p5007"}),
            "3等航海士": ("懲役5年", {"船員の2審 p5007"}), "操舵手（当直）": ("懲役5年", {"船員の2審 p5007"}),
            "会社の代表": ("懲役7年", {"民事の判決 N"}), "123艇の艇長": ("懲役3年", {"艇長の判決 p5002"}),
        },
        REC_SEATS=13,
        REC_UNANIMOUS={("船長", "殺人・殺人未遂")},
        HEADS={"1審", "2審", "大法院"},
        REC_MECH={"操舵台", "ソレノイド弁", "舵", "電気の信号", "油の流れ"},
        REC_CHIP={"報告書：退けた": {"海審 p1118"}, "特別調査委：可能性は非常に低い": {"特調委 p3013"}},
        REC_FORM={"出港前安全点検報告書": dict(fields={"乗船人員", "貨物量"}, ends={"セウォル号", "運航管理室"},
                                              values={}, rec={"海審 p1037"})},
        REC_CAUSE={"舵の使い方？": {"海審 p1091", "裁決 p2087"}, "装置の故障？": {"判決 p33", "特調委 p3073"},
                   "外からの力？": {"特調委 p3013", "特調委小 p4161"}},
        EXTRA={"甲板部", "機関部", "裁判官", "模式図"},
    ),
    "check_mech": dict(
        REC_HULL=dict(a_ext=5.6, br_ext=2.6, roof0=3.5, rise=1.7,
                      cargo_less=987.0 / 2437.0,
                      bw=dict(before=370.0 / 2501.826, req=1703.0 / 2501.826, low=761.272 / 2501.826),
                      draft_seen=6.20, draft_full=6.26),
        REC_LASH=dict(car_req=dict(front=2, rear=2), car_act=dict(front=1, rear=1),
                      truck_req=10, truck_act=4, zone_belts=0, lock_used=0),
    ),
}


_SAVED = []


def apply(gate=None):
    """selftest の処理の中だけ、ss・titan_fig.GEO・（gate を渡せば）その門番の記録の表を14本目の値にする。
    🔴 2026-09-30（15本目 ⑤b-2）：差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す
       （戻さないと、selftest のあとの本番の照合が14本目の表で15本目の画を測る＝⑤b-1〜⑤b-2 に在った穴。
        本番に15本目の案C・軸のカットが無かったあいだは表に出なかった）"""
    import titan_fig as F
    from cuts import ss
    g = globals()
    saved = dict(ss={n: getattr(ss, n) for n in SS_NAMES if hasattr(ss, n)}, geo=dict(F.GEO), gate=gate, tables={})
    for n in SS_NAMES:
        setattr(ss, n, g[n])
    F.GEO.update(GEO)
    if gate is not None:
        name = Path(getattr(gate, "__file__", "") or "").stem
        for k, v in GATES.get(name, {}).items():
            if hasattr(gate, k):
                saved["tables"][k] = getattr(gate, k)
            setattr(gate, k, v)
    _SAVED.append(saved)


def restore():
    """apply() の前の本番の値に戻す（selftest のあと・本番の照合の前に呼ぶ）。apply を呼んでいなければ何もしない。"""
    import titan_fig as F
    from cuts import ss
    while _SAVED:
        s = _SAVED.pop()
        for n, v in s["ss"].items():
            setattr(ss, n, v)
        F.GEO.clear()
        F.GEO.update(s["geo"])
        for k, v in s["tables"].items():
            setattr(s["gate"], k, v)
