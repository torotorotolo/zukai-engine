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
REC_SAT_AREA = {"c511": (67100, "K6-市 p40（`부지와 그 주변지역을 포함한 67,100㎡`）")}


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
    print(f"■ 地図のカット（衛星写真）{n} カット・部品 {ne}")
    for code, s in sorted(__import__("cuts.ss", fromlist=["SAT"]).SAT.items()):
        print(f"  {code}：{s['file']}（{'手元に在る' if M.have(code) else '🔴 手元に無い'}）")
    for b in bad:
        print("  🔴 " + b)
    if not bad:
        print(f"  ✓ {n} カット・部品 {ne}：額の書き方・md5・場所の表・墨の位置（額の内側・ロゴと帰属の行の外）・断りと出典の行")
    return 1 if bad else (1 if n == 0 else 0)


def selftest():
    """🔴 2026-10-18（23本目 ⑤b-1・§0b）：22本目の実物（地図のカット9つ・衛星写真の表 `ss.SAT`・場所の表 `ss.GEO`）は本番から見本 `tools/fixture_ep22.py` へ移した
    ＝見本の ss の表（SAT・GEO ほか）と22本目の章ファイル（apply_cuts＝git の `adbe2d5`）を差して回し、最後に restore（LIFO）。
    この門番の照合（`satmap.check`）が読む ss の名は SAT・GEO だけ（`SAT[…]["file"]` は `ep22/…` の名を文字で持つ＝REF・EP の差し替えは要らない。
    写真の権利の台帳 `ss._assets()` も読まない）"""
    import fixture_ep22
    fixture_ep22.apply()
    fixture_ep22.apply_cuts()
    try:
        rc = _selftest()
    finally:
        fixture_ep22.restore()
    return rc or _selftest_area()


def _selftest_area():
    """🆕 23本目 ⑤b-4：面積の照合（本番の c511＝陰性・半径を 5% 縮めた写し＝陽性）。"""
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
