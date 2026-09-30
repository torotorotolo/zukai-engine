# -*- coding: utf-8 -*-
"""check_drift.py — 動く模式図（drift）の**位置・向き・距離**を報告書の値と突き合わせる（2026-09-23 新設・12本目 ⑤b-2）。

■ なぜ要るか（葦の分析を受けた決定・記憶 project-jiko-visual-variety-from-ep12）
    drift は1枚の地図の上で物を動かす型。**地図が報告書と食い違うと、動きがそのまま嘘になる**
    （事故検証chの値打ちは正確さ）。「規則を書いたら門番も」＝[[feedback-rules-need-gates]]。

■ 測るもの（**本番の関数 `titan_fig.drift()` が描いた画素**から逆算する＝SPEC の数字を読み比べない）
    1. 🔴 `rel=`（報告書の値の宣言）ごとに、描いた2点の画素 → 緯度経度 → 距離と方位
       距離は宣言の ±5%（`tol` で変えられる）／方位は宣言の16方位の扇（±11.25度）＋1度
       🔴 13本目（09-24）：報告書が**8方位の言い方**で書いた値は `sector=8`（扇 ±22.5度＋1度）。
          仏 p12「à 37 km dans le nord-est de Paris」＝緯度経度から測ると 32.8度（16方位なら北北東の端）。
          16方位の扇で照合すると差 12.2度が許し 12.25度に**0.05度差で通る**だけ＝物差しとして意味が無い。
          NTSB §1.10「17 statute miles southwest of Detroit」も測ると 242度（16方位なら西南西）。
          ⚠️ 報告書が16方位（east-northeast など）で書いた値に `sector=8` を付けない（許しを広げる口にしない）
    2. 🔴 寸法線の札（`dim` の「157キロ」）が、描いた2点の距離と ±5% で合うか
    3. ⚠️ 宣言（`rel`）が1件も無い drift は E（**照合できない模式図を出さない**）
    4. 半径の円は、中心と半径の点の距離が rel に宣言されていること（15本目 ⑤b-7）
    5. 🆕 🔴 **動く道（stream の点・path の線と点・sight の線）が札の字を通らない**（2026-09-30・15本目 ⑤c'）
       動く部品は札より上に描かれる（`build_jiko.draw_moves`）＝点や線が字に乗る。14本目 c812（gather の点が「セヴォル号」に
       乗った＝avoid で薄める）、15本目 c201（風の点が「ステッド空港」の「港」に乗った）・c904（燃料車の道が「観客席」を
       斜めに通った）＝**どれも門番0件で、原寸の目視で見つけた**。道（本番の関数が返す `f.moves`）と札の字の箱（字幅と
       字面は fontmetrics の実測＝check_layout と同じ）の最短の距離が、点の半径（stream 6・path 9・sight 2）より近ければ止める
    → [[feedback-gates-must-share-the-production-geometry]]（対照は本番の関数そのものを呼ぶ）

■ 使い方
    python tools/check_drift.py              # 全カット
    python tools/check_drift.py --selftest   # 物差しの検算（陽性対照＝わざと食い違わせた宣言が落ちること）
"""
from __future__ import annotations

import math
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


def _km(v):
    """所見の距離の書き方（15本目 ⑤b-7：駐機場の数百メートルが「0キロ」と出ていた）。"""
    return f"{v * 1000:.0f}メートル" if v < 1 else f"{v:.1f}キロ" if v < 10 else f"{v:.0f}キロ"


# ── ⑤ 動く道と札の字（15本目 ⑤c'）────────────────────────
TEXT = re.compile(r'<text\s([^>]*)>([^<]*)</text>')
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
MOVE_R = dict(stream=6.0, path=9.0, sight=2.0)     # build_jiko.draw_moves の点の半径（sight は線の太さの半分）
_FM = []


def _text_boxes(svg):
    """字の箱 (x0, y0, x1, y1, 字)＝check_layout.boxes と同じ実測（字幅＝送り幅・上下＝字面）。"""
    import fontmetrics as fm
    if not _FM:
        fm.measured()          # 先に読む（check_layout の注＝後だとこの PC は MemoryError で粗いキャッシュへ落ちる）
        _FM.append(fm)
    out = []
    for m in TEXT.finditer(svg):
        a, t = dict(ATTR.findall(m.group(1))), m.group(2).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        if not t.strip():
            continue
        x, y, size, fam = float(a["x"]), float(a["y"]), float(a["font-size"]), a.get("font-family", "Noto")
        w = fm.width(t, size, fam)
        up, dn = fm.ink(t, size, fam)
        anc = a.get("text-anchor", "start")
        x0 = x - w / 2 if anc == "middle" else (x - w if anc == "end" else x)
        out.append((x0, y - up, x0 + w, y + dn, t))
    return out


def _move_segs(m):
    """動く部品 → [(点a, 点b, 半径)]（道のない動き＝輪・降る点・集まる点・図の動きは見ない）。"""
    r = MOVE_R.get(m.get("kind"))
    if r is None:
        return []
    if m["kind"] == "path":
        return [(p, q, r) for p, q in zip(m["pts"], m["pts"][1:])]
    return [(m["a"], m["b"], r)]


def _seg_box_dist(a, b, box):
    """線分 a→b と字の箱の最短の距離（2画素ごとに当てる＝誤差1画素）。"""
    (ax, ay), (bx, by) = a, b
    x0, y0, x1, y1 = box
    k = max(1, int(math.hypot(bx - ax, by - ay) / 2))
    best = 1e9
    for i in range(k + 1):
        px, py = ax + (bx - ax) * i / k, ay + (by - ay) * i / k
        best = min(best, math.hypot(max(x0 - px, 0.0, px - x1), max(y0 - py, 0.0, py - y1)))
    return best


def judge_moves(f):
    """⑤ 動く道が札の字を通るか → 所見のリスト（空なら合格）と照合した件数。"""
    bad, n = [], 0
    boxes = _text_boxes(f.lab + "".join(f.stages))
    for m in getattr(f, "moves", None) or []:
        for a, b, r in _move_segs(m):
            n += 1
            for x0, y0, x1, y1, t in boxes:
                d = _seg_box_dist(a, b, (x0, y0, x1, y1))
                if d < r:
                    bad.append(f"動く道（{m['kind']}）が札「{t}」の字を通る（最短 {d:.1f}画素＜点の半径 {r:g}）")
    return bad, n


def judge(kw):
    """1つの drift の引数 → 所見のリスト（空なら合格）と、照合した件数。"""
    f = F.drift(**kw)
    V, P = f.view, f.geo_px
    bad, n = [], 0

    def measured(a, b):
        return F.geo_between(V.geo(*P[a]), V.geo(*P[b]))

    for r in f.rel:
        n += 1
        if "course" in r:
            # 14本目 ⑤b-4：方位盤の針路の宣言（値の照合は drift() が型の中で止める＝宣言の無い針路は描けない）
            if not r.get("src"):
                bad.append(f"針路 {r['course']} 度の宣言に出どころ（src）が無い")
            continue
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
            bad.append(f"{r['a']}→{r['b']}: 図は {_km(km)}／報告書 {_km(r['km'])}"
                       f"（差 {abs(km - r['km']) / r['km']:.1%}＞{tol:.0%}）［{r.get('src', '')}］")
        half = {16: 11.25, 8: 22.5}[int(r.get("sector", 16))]
        if r.get("dir") and int(r.get("sector", 16)) == 8 and F.dir_deg(r["dir"]) % 45:
            bad.append(f"{r['a']}→{r['b']}: sector=8 なのに「{r['dir']}」は8方位の名ではない［{r.get('src', '')}］")
        elif r.get("dir") and _adiff(deg, F.dir_deg(r["dir"])) > half + SLACK_DEG:
            bad.append(f"{r['a']}→{r['b']}: 図の方位 {deg:.0f}度（{F.dir_name(deg)}）／報告書「{r['dir']}」"
                       f"（{int(r.get('sector', 16))}方位の扇）［{r.get('src', '')}］")
        # 🔴 方位角（度）で書かれた値（DNA p209「230° bearing」）は16方位の扇より細かく ±2度
        if r.get("deg") is not None and _adiff(deg, float(r["deg"])) > float(r.get("tol_deg", 2.0)):
            bad.append(f"{r['a']}→{r['b']}: 図の方位 {deg:.1f}度／報告書 {float(r['deg']):g}度"
                       f"［{r.get('src', '')}］")
    declared = {frozenset((r["a"], r["b"])) for r in f.rel if "b" in r and "km" in r}
    for st in kw.get("steps", []):
        for d in F._many(st.get("dim")):
            # 🔴 14本目 ⑤b-4：小数を読む（「約1.7キロ」を「7キロ」と読んでいた＝12・13本目は整数だけだった）
            # 🔴 15本目 ⑤b-7：「メートル」も読む（駐機場の地図の「約228メートル」はキロの札でないので**黙って素通り**していた）
            m = re.search(r"(\d[\d,]*(?:\.\d+)?)(キロ|メートル)", d.get("t", ""))
            if not m:
                continue
            n += 1
            km, _ = measured(d["a"], d["b"])
            say = float(m.group(1).replace(",", "")) / (1000.0 if m.group(2) == "メートル" else 1.0)
            if abs(km - say) / say > 0.05:
                bad.append(f"寸法線 {d['a']}→{d['b']}「{d['t']}」: 図は {_km(km)}（差 {abs(km - say) / say:.1%}）")
        for ci in F._many(st.get("circle")):
            # 🆕 15本目 ⑤b-7：半径の円は、中心と半径の点の距離が**報告書の値として宣言**されていること
            n += 1
            if frozenset((ci["at"], ci["through"])) not in declared:
                bad.append(f"円 {ci['at']}（半径の点 {ci['through']}）: 半径の距離が rel に宣言されていない")
    if not f.rel:
        bad.append("rel（報告書の値の宣言）が1件も無い＝照合できない模式図")
    mb, mn = judge_moves(f)
    return bad + mb, n + mn


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
        # 13本目 ⑤b-2（2026-09-24）で足した口：8方位の言い方（sector=8）
        ("正しい宣言（8方位：32.8度の点を「北東」・仏 p12 と同じ形）",
         dict(base, pts=dict(base["pts"], n8=dict(of="gz", km=38, deg=32.8)),
              rel=[dict(a="gz", b="n8", km=38, dir="北東", sector=8)]), True),
        ("🔴 陽性対照：8方位で「東」と宣言（図は32.8度＝差57度）",
         dict(base, pts=dict(base["pts"], n8=dict(of="gz", km=38, deg=32.8)),
              rel=[dict(a="gz", b="n8", km=38, dir="東", sector=8)]), False),
        ("🔴 陽性対照：8方位なのに16方位の名「北北東」を書く",
         dict(base, pts=dict(base["pts"], n8=dict(of="gz", km=38, deg=32.8)),
              rel=[dict(a="gz", b="n8", km=38, dir="北北東", sector=8)]), False),
        ("🔴 陽性対照：16方位（既定）で25度ずれた点を「北東」",
         dict(base, pts=dict(base["pts"], n8=dict(of="gz", km=38, deg=20.0)),
              rel=[dict(a="gz", b="n8", km=38, dir="北東")]), False),
        # 15本目 ⑤b-7（2026-09-30）で足した口：メートルの寸法線（駐機場）と半径の円（オカラから約161キロ）
        ("正しい寸法線（約228メートル・南）",
         dict(base, pts=dict(base["pts"], pit=dict(of="gz", km=0.228, deg=180)),
              steps=[dict(dim=dict(a="gz", b="pit", t="約228メートル"))],
              rel=[dict(a="gz", b="pit", km=0.228, dir="南")]), True),
        ("🔴 陽性対照：メートルの札を約400メートルと書く（図は228メートル）",
         dict(base, pts=dict(base["pts"], pit=dict(of="gz", km=0.228, deg=180)),
              steps=[dict(dim=dict(a="gz", b="pit", t="約400メートル"))],
              rel=[dict(a="gz", b="pit", km=0.228, dir="南")]), False),
        ("正しい半径の円（半径161キロを宣言）",
         dict(base, pts=dict(base["pts"], r161=dict(of="gz", km=161, deg=90)),
              steps=[dict(circle=dict(at="gz", through="r161"), dim=dict(a="gz", b="r161", t="約161キロ"))],
              rel=[dict(a="gz", b="r161", km=161)]), True),
        ("🔴 陽性対照：円の半径を宣言していない",
         dict(base, pts=dict(base["pts"], r161=dict(of="gz", km=161, deg=90)),
              steps=[dict(circle=dict(at="gz", through="r161"))],
              rel=[dict(a="gz", b="ship", km=157, dir="東北東")]), False),
        # 15本目 ⑤c'（2026-09-30）で足した口 ⑤：動く道と札の字（c201 の風の点・c904 の燃料車の道と同じ形）
        ("正しい流れの点（札の右から離れて北へ）",
         dict(base, steps=[dict(tag=dict(at="ship", t="船の位置", side="right"),
                                move=[dict(kind="stream", a="ship", deg=0, km=100, n=8)])],
              rel=[dict(a="gz", b="ship", km=157, dir="東北東")]), True),
        ("🔴 陽性対照：流れの点が札の字の真ん中を東へ通る",
         dict(base, steps=[dict(tag=dict(at="ship", t="船の位置", side="right"),
                                move=[dict(kind="stream", a="ship", deg=90, km=100, n=8)])],
              rel=[dict(a="gz", b="ship", km=157, dir="東北東")]), False),
        ("🔴 陽性対照：動く道（path）の線が札の字を通る",
         dict(base, steps=[dict(tag=dict(at="gz", t="出発した所", side="right"),
                                move=[dict(kind="path", via=["gz", "ship"], sec=2.0)])],
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
