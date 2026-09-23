# -*- coding: utf-8 -*-
"""check_drift.py — 動く模式図（drift）の**位置・向き・距離**を報告書の値と突き合わせる（2026-09-23 新設・12本目 ⑤b-2）。

■ なぜ要るか（葦の分析を受けた決定・記憶 project-jiko-visual-variety-from-ep12）
    drift は1枚の地図の上で物を動かす型。**地図が報告書と食い違うと、動きがそのまま嘘になる**
    （事故検証chの値打ちは正確さ）。「規則を書いたら門番も」＝[[feedback-rules-need-gates]]。

■ 測るもの（**本番の関数 `titan_fig.drift()` が描いた画素**から逆算する＝SPEC の数字を読み比べない）
    1. 🔴 `rel=`（報告書の値の宣言）ごとに、描いた2点の画素 → 緯度経度 → 距離と方位
       距離は宣言の ±5%（`tol` で変えられる）／方位は宣言の16方位の扇（±11.25度）＋1度
    2. 🔴 寸法線の札（`dim` の「157キロ」）が、描いた2点の距離と ±5% で合うか
    3. ⚠️ 宣言（`rel`）が1件も無い drift は E（**照合できない模式図を出さない**）
    → [[feedback-gates-must-share-the-production-geometry]]（対照は本番の関数そのものを呼ぶ）

■ 使い方
    python tools/check_drift.py              # 全カット
    python tools/check_drift.py --selftest   # 物差しの検算（陽性対照＝わざと食い違わせた宣言が落ちること）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import titan_fig as F  # noqa: E402

SLACK_DEG = 1.0


def _adiff(a, b):
    return abs((a - b + 180) % 360 - 180)


def judge(kw):
    """1つの drift の引数 → 所見のリスト（空なら合格）と、照合した件数。"""
    f = F.drift(**kw)
    V, P = f.view, f.geo_px
    bad, n = [], 0

    def measured(a, b):
        return F.geo_between(V.geo(*P[a]), V.geo(*P[b]))

    for r in f.rel:
        n += 1
        if "lat" in r:
            # 🔴 緯度経度で書かれた値（日本政府の文書など）＝描いた点がその位置から ±2キロ
            off, _ = F.geo_between(V.geo(*P[r["a"]]), (float(r["lat"]), float(r["lon"])))
            tk = float(r.get("tol_km", 2.0))
            if off > tk:
                bad.append(f"{r['a']}: 図の点は宣言の緯度経度から {off:.1f}キロずれている（＞{tk:g}キロ）"
                           f"［{r.get('src', '')}］")
            continue
        km, deg = measured(r["a"], r["b"])
        tol = float(r.get("tol", 0.05))
        if abs(km - r["km"]) / r["km"] > tol:
            bad.append(f"{r['a']}→{r['b']}: 図は {km:.0f}キロ／報告書 {r['km']}キロ"
                       f"（差 {abs(km - r['km']) / r['km']:.1%}＞{tol:.0%}）［{r.get('src', '')}］")
        if r.get("dir") and _adiff(deg, F.dir_deg(r["dir"])) > 11.25 + SLACK_DEG:
            bad.append(f"{r['a']}→{r['b']}: 図の方位 {deg:.0f}度（{F.dir_name(deg)}）／報告書「{r['dir']}」"
                       f"［{r.get('src', '')}］")
        # 🔴 方位角（度）で書かれた値（DNA p209「230° bearing」）は16方位の扇より細かく ±2度
        if r.get("deg") is not None and _adiff(deg, float(r["deg"])) > float(r.get("tol_deg", 2.0)):
            bad.append(f"{r['a']}→{r['b']}: 図の方位 {deg:.1f}度／報告書 {float(r['deg']):g}度"
                       f"［{r.get('src', '')}］")
    for st in kw.get("steps", []):
        for d in F._many(st.get("dim")):
            m = re.search(r"(\d[\d,]*)キロ", d.get("t", ""))
            if not m:
                continue
            n += 1
            km, _ = measured(d["a"], d["b"])
            say = float(m.group(1).replace(",", ""))
            if abs(km - say) / say > 0.05:
                bad.append(f"寸法線 {d['a']}→{d['b']}「{d['t']}」: 図は {km:.0f}キロ（差 {abs(km - say) / say:.1%}）")
    if not f.rel:
        bad.append("rel（報告書の値の宣言）が1件も無い＝照合できない模式図")
    return bad, n


def selftest():
    base = dict(view=dict(lon=(164.3, 168.9), lat=(10.7, 12.8)), places=["bikini", "rongerik"],
                pts=dict(ship=dict(of="gz", km=157, dir="東北東")), note="模式図",
                steps=[dict(dim=dict(a="gz", b="ship", t="157キロ"))])
    ok = True
    cases = [
        ("正しい宣言（157キロ・東北東）", dict(base, rel=[dict(a="gz", b="ship", km=157, dir="東北東")]), True),
        ("🔴 陽性対照：距離を300キロと宣言", dict(base, rel=[dict(a="gz", b="ship", km=300, dir="東北東")]), False),
        ("🔴 陽性対照：方角を東南東と宣言", dict(base, rel=[dict(a="gz", b="ship", km=157, dir="東南東")]), False),
        ("正しい宣言（ロンゲリックは東へ250キロ＝135海里・DNA p212）",
         dict(base, rel=[dict(a="gz", b="rongerik", km=250, dir="東")]), True),
        ("🔴 陽性対照：寸法線の札を200キロと書く",
         dict(base, steps=[dict(dim=dict(a="gz", b="ship", t="200キロ"))],
              rel=[dict(a="gz", b="ship", km=157, dir="東北東")]), False),
        ("🔴 陽性対照：宣言が無い", dict(base), False),
        # ⑤b-3（2026-09-23）で足した口：方位角（度）と緯度経度
        ("正しい宣言（駆逐艦＝ビキニから230度・167キロ・DNA p209）",
         dict(base, pts=dict(base["pts"], dd=dict(of="bikini", km=167, deg=230)),
              rel=[dict(a="bikini", b="dd", km=167, deg=230)]), True),
        ("🔴 陽性対照：方位角を270度と宣言（図は230度）",
         dict(base, pts=dict(base["pts"], dd=dict(of="bikini", km=167, deg=230)),
              rel=[dict(a="bikini", b="dd", km=167, deg=270)]), False),
        ("正しい宣言（日本政府の文書の位置 北緯11度52分半・東経166度35分）",
         dict(base, pts=dict(base["pts"], jp=dict(lat=11.875, lon=166.58333)),
              rel=[dict(a="jp", lat=11.875, lon=166.58333)]), True),
        ("🔴 陽性対照：緯度経度を 0.1度ずらして宣言",
         dict(base, pts=dict(base["pts"], jp=dict(lat=11.875, lon=166.58333)),
              rel=[dict(a="jp", lat=11.975, lon=166.58333)]), False),
        ("🔴 陽性対照：寸法線が2本の段で、2本目の札が違う",
         dict(base, steps=[dict(dim=[dict(a="gz", b="ship", t="157キロ"),
                                     dict(a="gz", b="rongerik", t="300キロ")])],
              rel=[dict(a="gz", b="ship", km=157, dir="東北東")]), False),
    ]
    for name, kw, want in cases:
        bad, _ = judge(kw)
        got = not bad
        mark = "OK" if got == want else "🔴 NG"
        ok &= got == want
        print(f"  {mark} {name}: {'合格' if got else '不合格'}（{'合格' if want else '不合格'}のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import cuts
    targets = {c: s["fig"][1] for c, s in sorted(cuts.SPEC.items())
               if s.get("fig") and s["fig"][0] == "drift"}
    if not targets:
        print("⚠️ drift のカットが0件（この回に動く模式図が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
        return 0
    bad_all, n_all = 0, 0
    for cid, kw in targets.items():
        bad, n = judge(kw)
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {cid}: {b}")
        else:
            print(f"✓ {cid}: 宣言と寸法線 {n}件が図の座標と合う")
    print(f"\n{'✓' if not bad_all else '🔴'} drift {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
