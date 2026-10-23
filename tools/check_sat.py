# -*- coding: utf-8 -*-
"""check_sat.py — 地図のカット（衛星写真＋描き足し＝`tools/satmap.py`）の門番（2026-10-14 新設・22本目 ⑤b-3）。

  python tools/check_sat.py            # SPEC の地図のカットを照らす（qa_all）
  python tools/check_sat.py --selftest # 陽性対照（わざと壊した SPEC と表で鳴るか）

照らすこと（中身は `satmap.check`）：
  ① 額の書き方＝panel・pw・color 1.0・寄り／カメラ／注記／切り出しなし・副題に「現在の衛星写真」（Google の決まり＝色を変えない・動かさない）
  ② 衛星写真の md5＝表 `cuts/ss.SAT` と手元の絵（撮り直した絵に古い座標の描き足しを重ねない）・表の欄
  ③ 場所の表 `cuts/ss.GEO`＝出典（報告書で名が出る所）と座標の出どころ。🔴 確かめていない場所に点を置かない・×は報告書の座標だけ・
     一般の座標を使ったら額の下の断りに「一般の座標」
  ④ 描き足しの墨（描く関数と同じ箱）が額の内側・**ロゴと帰属の行の箱に入らない**（Google の決まり）・操作の部品の箱にも重ねない
  ⑤ 額の下の断り（左）と出典の行（右）が重ならない
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))

import satmap as M  # noqa: E402

# 🆕 2026-10-18（23本目 ⑤b-4）：囲み（area）の面積の記録＝{カット: (平方メートル, 出典)}。境の線が記録に無く「面積が同じ円」で描くカットだけ
#    （記録の値は門番の側＝§5b-88。描く側は `satmap.r_of_area` で半径を出す）。囲みの面積が記録から 1% より外れたら鳴る
# 🔴 2026-10-20（17本目 ⑤b-1・§0b）：23本目の記録（c511＝特別災害地域の範囲 67,100 平方メートル〈K6-市 p40〉）は見本 `tools/fixture_ep23.py`（GATES["check_sat"]・値は1つも変えていない＝
#    git の `b800dbdb`）へ移した＝空。17本目で「面積が同じ円」の囲み（area）を使うカットが出たら、その回の記録をここに入れる。
#    ⚠️ `area_check` は**表に載ったカットだけ**を見る（表が空なら何も照らさない＝止めない）。表に無いカットの囲み（area）は面積を照らされずに通る（`satmap.check` は area の面積の出どころを見ない）
#    ＝囲みを使うのに記録を入れ忘れると素通りする穴。17本目で囲みを使うときは必ず入れる（門番の側で「area があるのに表に無い」を止める直しは、この移し替えでは足していない）
#    🔴 2026-10-22（24本目 ⑤b-1）：17本目は囲み（area）を使わなかった＝空のまま（見本 `tools/fixture_ep17.py` の GATES["check_sat"] も REC_SAT_AREA は17本目の状態＝空として持つ）
REC_SAT_AREA = {}
# 🆕 2026-10-20（17本目 ⑤b-6）：**描き足しの札の数と時刻の記録**（§5b-88＝記録の値は門番の側）。{カット: {札の言葉: ((出典, 原文の句), …)}}。
#   数字を含む札は**全部**ここに載っていなければ鳴る（載っていない札＝出どころの無い数）・載っているのに描いていない札も鳴る（古い表）。
#   句は手元の原文（`ref/ep17/src/ep17_pages.txt`＝git の外）で照らす（`check_mech._m17_page`・Actions では句だけ飛ばす）
# 🔴 2026-10-22（24本目 ⑤b-1・§0b）：17本目の記録（REC_SAT_NUM＝空港の地図 c804〈化学消防車3台が出て着くまで・通報から3分以内〉・c812〈北門の鎖・着いた時刻・火が消えた時刻〉・c818〈病院へ運ばれた乗客〉の
#    描き足しの札 9つの数と時刻）は見本 `tools/fixture_ep17.py`（GATES["check_sat"]・値は1つも変えていない＝git の `2cc5e5ab`）へ移した＝空。selftest（`_selftest_ep17`）は見本と17本目の章ファイル
#    （`apply(gate)`＋`apply_cuts()`）を差して回す。24本目で地図の描き足しに数字を含む札を置くときは、その回の記録をここに入れる（空のあいだ、数字を含む札は「出どころの無い数」で鳴る＝fail closed）。
#    ⚠️ 句の照合 `num_check` が使う `check_mech._m17_page`（原文の道 `ref/ep17/src/ep17_pages.txt` を直書き）は型として残した（24本目で使うなら原文の道を替える）
REC_SAT_NUM = {}
_NUM = __import__("re").compile(r"[0-9０-９]")


def num_check(spec_all, rec=None):
    """地図のカットの描き足しの札（数字を含むもの）が、記録の表 REC_SAT_NUM に載っていて、句が原文の頁にあるか。"""
    from check_mech import _m17_page, _m17_q
    R = REC_SAT_NUM if rec is None else rec
    bad = []
    for cid, s in sorted(spec_all.items()):
        if not s.get("sat"):
            continue
        drawn = {el.get("t") for st in s["sat"]["steps"] for el in st if el.get("t") and _NUM.search(el["t"])}
        table = R.get(cid, {})
        for t in sorted(drawn - set(table)):
            bad.append(f"{cid}：札「{t}」の数が記録の表 REC_SAT_NUM に無い（出どころの無い数）")
        for t in sorted(set(table) - drawn):
            bad.append(f"{cid}：記録の表の札「{t}」が描かれていない（古い表）")
        for t in sorted(drawn & set(table)):
            for p, q in table[t]:
                src = _m17_page(p)
                if src is not None and _m17_q(q) not in src:
                    bad.append(f"{cid}：札「{t}」の句「{q[:14]}…」が {p} に無い")
    return bad


def area_check(spec_all, sat_tab, rec=None):
    """面積の記録のあるカットの囲み（area）が、記録と同じ面積か（撮った絵の画素×1画素のメートル）。"""
    import math
    bad = []
    for cid, (m2, _src) in (REC_SAT_AREA if rec is None else rec).items():
        s = spec_all.get(cid)
        if not s or not s.get("sat"):
            bad.append(f"{cid}：面積の記録があるのに地図のカットでない")
            continue
        sat = sat_tab[s["sat"]["code"]]
        areas = [el for st in s["sat"]["steps"] for el in st if el.get("k") == "area"]
        if len(areas) != 1:
            bad.append(f"{cid}：囲み（area）が {len(areas)} 個（面積の記録は1つ）")
            continue
        got = math.pi * (areas[0]["r"] * M.m_per_px(sat)) ** 2
        if abs(got - m2) / m2 > 0.01:
            bad.append(f"{cid}：囲みの面積 {got:,.0f} 平方メートルが記録 {m2:,} と 1% より違う")
    return bad


def main():
    import cuts
    import cuts.ss as ss
    bad, n, ne = M.check(cuts.SPEC)
    bad += area_check(cuts.SPEC, ss.SAT)
    bad += num_check(cuts.SPEC)
    print(f"■ 地図のカット（衛星写真）{n} カット・部品 {ne}")
    for code, s in sorted(__import__("cuts.ss", fromlist=["SAT"]).SAT.items()):
        print(f"  {code}：{s['file']}（{'手元に在る' if M.have(code) else '🔴 手元に無い'}）")
    for b in bad:
        print("  🔴 " + b)
    if not bad:
        print(f"  ✓ {n} カット・部品 {ne}：額の書き方・md5・場所の表・墨の位置（額の内側・ロゴと帰属の行の外）・断りと出典の行")
    # 🆕 2026-10-23（24本目 ⑤b-6）：この回は衛星写真の地図なし（ss.SAT_NONE＝理由の文）＝地図0を通す。地図が1つでもあれば言い分と食い違う＝鳴る
    rc0 = none_check(n, getattr(ss, "SAT_NONE", None))
    if rc0 is not None:
        return 1 if bad else rc0
    return 1 if bad else (1 if n == 0 else 0)


def none_check(n, why):
    """「この回は衛星写真の地図なし」の言い分（ss.SAT_NONE）。言い分が無ければ None（いつもどおり＝地図0は落ちる）。
    言い分があって地図0＝0（通す）・言い分があるのに地図がある＝1（食い違い）。"""
    if not why:
        return None
    if n == 0:
        print(f"  ✓ この回は衛星写真の地図なし（ss.SAT_NONE：{why}）")
        return 0
    print(f"  🔴 ss.SAT_NONE（衛星写真の地図なし）なのに地図のカットが {n} ある＝言い分と食い違う（§0b で戻し忘れ？）")
    return 1


def selftest():
    """🔴 2026-10-18（23本目 ⑤b-1・§0b）：22本目の実物（地図のカット9つ・衛星写真の表 `ss.SAT`・場所の表 `ss.GEO`）は本番から見本 `tools/fixture_ep22.py` へ移した
    ＝見本の ss の表（SAT・GEO ほか）と22本目の章ファイル（apply_cuts＝git の `adbe2d5`）を差して回し、最後に restore（LIFO）。
    この門番の照合（`satmap.check`）が読む ss の名は SAT・GEO だけ（`SAT[…]["file"]` は `ep22/…` の名を文字で持つ＝REF・EP の差し替えは要らない。
    写真の権利の台帳 `ss._assets()` も読まない）"""
    # 🆕 17本目 ⑤b-6：17本目の空港の地図の陽性対照を先に回す（下の22本目の見本の章ファイルは apply_cuts で止まることがある＝
    #    ⑤b-5 の qa_all でも sat は「落ちてよい3」だった＝22本目の c101 の CC BY-SA の決まり。17本目の対照がその陰で回らないのを防ぐ）
    #    （🔴 2026-10-22〜：17本目も見本 fixture_ep17 の表と章ファイルを差して回す＝`_selftest_ep17` が差し込んで・終わったら戻す）
    rc17 = _selftest_ep17()
    # 🆕 24本目 ⑤b-6：「衛星写真の地図なし」の言い分の陽性対照（言い分なし＝None・言い分あり地図0＝0・言い分ありで地図あり＝1）
    nc = [none_check(0, None), none_check(0, "見本の言い分"), none_check(3, "見本の言い分")]
    print(f"  {'✓' if nc == [None, 0, 1] else '🔴'} 陽性対照：衛星写真の地図なしの言い分 → {nc}（[None, 0, 1] のはず）")
    if nc != [None, 0, 1]:
        rc17 = rc17 or 1
    import fixture_ep22
    fixture_ep22.apply()
    fixture_ep22.apply_cuts()
    try:
        rc = _selftest()
    finally:
        fixture_ep22.restore()
    if rc or rc17:
        return rc or rc17
    # 🔴 2026-10-20（17本目 ⑤b-1・§0b）：23本目の実物（地図のカット c511・衛星写真の表 `ss.SAT`・場所の表 `ss.GEO`・面積の記録 `REC_SAT_AREA`）も本番から見本 `tools/fixture_ep23.py` へ移した
    #    ＝見本の ss の表と、この門番の表（`apply(gate)` が `REC_SAT_AREA` を差す）と、23本目の章ファイル（apply_cuts＝git の `b800dbdb`）を差して回し、最後に restore（LIFO）
    import fixture_ep23
    fixture_ep23.apply(sys.modules[__name__])
    fixture_ep23.apply_cuts()
    try:
        rc = _selftest_area()
    finally:
        fixture_ep23.restore()
    return rc


def _selftest_ep17():
    """🆕 17本目 ⑤b-6：17本目の空港の地図＝国土地理院の空中写真の行（gsi）が通り、壊すと狙った理由で鳴るか。
    🔴 2026-10-22（24本目 ⑤b-1・§0b）：17本目の実物（地図のカット c727・c804・c812・c818 ほか・衛星写真の表 `ss.SAT`・場所の表 `ss.GEO`・札の数と時刻の記録 `REC_SAT_NUM`）は本番から
    見本 `tools/fixture_ep17.py` へ移した＝見本の ss の表と、この門番の表（`apply(gate)` が `REC_SAT_AREA`・`REC_SAT_NUM` を差す）と、17本目の章ファイル（`apply_cuts`＝git の `2cc5e5ab`）を
    差して回し、最後に restore（LIFO・落ちても戻す）。本体は `_selftest_ep17_body`"""
    import fixture_ep17
    fixture_ep17.apply(sys.modules[__name__])
    try:
        fixture_ep17.apply_cuts()
        return _selftest_ep17_body()
    finally:
        fixture_ep17.restore()


def _selftest_ep17_body():
    """17本目の空港の地図の検算の本体（`fixture_ep17` の `apply(gate)`＋`apply_cuts()` を差し込んだ中で呼ぶ）。"""
    import cuts
    import cuts.ss as ss
    base = {c: s for c, s in cuts.SPEC.items() if s.get("sat")}
    if not base:
        print("  🔴 17本目の地図のカットが SPEC に無い＝陽性対照が作れない（見本 fixture_ep17 の apply_cuts が17本目の章ファイルを読めていない）")
        return 1
    ok = True
    b0 = M.check(base)[0] + num_check(base)
    print(f"  {'✓' if not b0 else '🔴'} 陰性：17本目の地図のカット {len(base)} は 0件（{len(b0)}件）" + (f"  ← {b0[0]}" if b0 else ""))
    ok &= not b0
    cases = []
    s = copy.deepcopy(base)
    s["c812"]["sat"]["steps"][1][0]["t"] = "20:45ごろ 名古屋市の消防"
    cases.append(("札の時刻を替える（表に無い札）", num_check(s), "REC_SAT_NUM に無い"))
    rec = copy.deepcopy(REC_SAT_NUM)
    rec["c804"]["20:19ごろ 着く"] = (("報告書 p27", "20時21分ごろ、消防小隊の化学消防車3台が第1陣"),)
    cases.append(("記録の句を替える（原文に無い）", num_check(base, rec) if __import__("check_mech")._m17_page("報告書 p27") is not None else ["（原文が手元に無い）が 報告書 p27 に無い"],
                  "報告書 p27 に無い"))
    s = copy.deepcopy(base)
    s["c727"]["s"] = "現在の衛星写真"
    cases.append(("副題から「1987〜1990年の空中写真」を消す", M.check(s)[0], "1987〜1990年の空中写真"))
    s = copy.deepcopy(base)
    s["c818"]["sat"]["steps"][0].append(dict(k="say", xy=(1900, 1060), t="額の外へ出る長い字の札", size=34))
    cases.append(("額の外へ出る字", M.check(s)[0], "額の内側"))
    for name, bad, want in cases:
        hit = [b for b in bad if want in b]
        print(f"  {'✓' if hit else '🔴'} 陽性対照（17本目）：{name} → {'鳴った：' + hit[0] if hit else '鳴らない'}")
        ok &= bool(hit)
    print(f"■ selftest（17本目の空港の地図）{'合格' if ok else '🔴 不合格'}")
    return 0 if ok else 1


def _selftest_area():
    """🆕 23本目 ⑤b-4：面積の照合（見本の c511＝陰性・半径を 5% 縮めた写し＝陽性）。
    🔴 2026-10-20（17本目 ⑤b-1）：表 REC_SAT_AREA・ss.SAT と SPEC の c511 は見本 `fixture_ep23`（`apply(gate)`＋`apply_cuts()`＝23本目の章ファイル）から（`selftest` が差し込んだ中で呼ぶ）"""
    import cuts
    import cuts.ss as ss
    ok = True
    b0 = area_check(cuts.SPEC, ss.SAT)
    print(f"  {'✓' if not b0 else '🔴'} 陰性：23本目 c511 の囲みの面積＝記録（{len(b0)}件）")
    ok &= not b0
    s = copy.deepcopy({c: cuts.SPEC[c] for c in REC_SAT_AREA})
    for st in s["c511"]["sat"]["steps"]:
        for el in st:
            if el.get("k") == "area":
                el["r"] *= 0.95
    b1 = area_check(s, ss.SAT)
    print(f"  {'✓' if b1 else '🔴'} 陽性対照：囲みの半径を 5% 縮める → {'鳴った：' + b1[0] if b1 else '鳴らない'}")
    ok &= bool(b1)
    print(f"■ selftest（面積）{'合格' if ok else '🔴 不合格'}")
    return 0 if ok else 1


def _selftest():
    import cuts
    import cuts.ss as ss
    base = {c: s for c, s in cuts.SPEC.items() if s.get("sat")}
    if not base:
        print("🔴 地図のカットが SPEC に無い＝陽性対照が作れない（見本 fixture_ep22 の apply_cuts が22本目の章ファイルを読めていない）")
        return 1
    cid = sorted(base)[0]
    ok = True

    def expect(name, spec, want, sat=None, geo=None):
        nonlocal ok
        s0, g0 = ss.SAT, ss.GEO
        try:
            if sat is not None:
                ss.SAT = sat
            if geo is not None:
                ss.GEO = geo
            bad, _, _ = M.check(spec)
        finally:
            ss.SAT, ss.GEO = s0, g0
        hit = [b for b in bad if want in b]
        print(f"  {'✓' if hit else '🔴'} 陽性対照：{name} → {'鳴った：' + hit[0] if hit else '鳴らない'}")
        ok &= bool(hit)

    clean, _, _ = M.check(base)
    print(f"  {'✓' if not clean else '🔴'} 陰性：22本目の見本の地図のカット {len(base)} は 0件（{len(clean)}件）")
    ok &= not clean
    s = copy.deepcopy(base)
    s[cid]["color"] = 0.5
    expect("色を変える（color 0.5）", s, "color=0.5")
    s = copy.deepcopy(base)
    s[cid]["zoom"] = 1.1
    expect("寄る（zoom）", s, "zoom は書けない")
    s = copy.deepcopy(base)
    s[cid]["s"] = "北アメリカ"
    expect("副題に「現在の衛星写真」が無い", s, "現在の衛星写真")
    s = copy.deepcopy(base)
    s[cid]["sat"]["steps"][0].append(dict(k="pt", at="nowhere", t="どこか"))
    expect("表に無い場所", s, "GEO に無い")
    s = copy.deepcopy(base)
    s[cid]["sat"]["steps"][0].append(dict(k="x", at="stjohns"))
    expect("一般の座標に×", s, "×は報告書の座標の場所だけ")
    # 帰属の行の箱（右下）に札を置く＝撮った絵の (1500, 1062) の場所を作って札を左下へ
    sat = ss.SAT[base[cid]["sat"]["code"]]
    geo = dict(ss.GEO, _attrib=dict(ll=M.igeo(sat, 1500, 1062), src="陽性対照", how="報告書の値"))
    s = copy.deepcopy(base)
    s[cid]["sat"]["steps"][0].append(dict(k="pt", at="_attrib", t="帰属の上"))
    expect("帰属の行に重なる点と札", s, "attrib の箱", geo=geo)
    geo = dict(ss.GEO, _logo=dict(ll=M.igeo(sat, 960, 1040), src="陽性対照", how="報告書の値"))
    s = copy.deepcopy(base)
    s[cid]["sat"]["steps"][0].append(dict(k="pt", at="_logo"))
    expect("ロゴに重なる点", s, "logo の箱", geo=geo)
    s = copy.deepcopy(base)
    s[cid]["sat"]["steps"][0].append(dict(k="pt", at="site", t="とても長い札がこの額の右の端をはみ出して外へ出る", lab=(18, -16, "start")))
    expect("額の外へ出る札", s, "額の内側")
    s = copy.deepcopy(base)
    s[cid]["sat"]["note"] = "断りを消した"
    expect("一般の座標の断りが無い", s, "一般の座標")
    sat2 = copy.deepcopy(ss.SAT)
    sat2[base[cid]["sat"]["code"]]["md5"] = "0" * 32
    if M.have(base[cid]["sat"]["code"]):
        expect("md5 が表と違う", base, "md5", sat=sat2)
    else:
        print("  ・md5 の陽性対照は手元に衛星写真が無いので飛ばした（Actions）")
    print(f"■ selftest {'合格' if ok else '🔴 不合格'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
