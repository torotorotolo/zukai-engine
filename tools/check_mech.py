# -*- coding: utf-8 -*-
"""check_mech.py — 仕組みの動く模式図（latch・section）の**状態の筋・描いた部品・札の数**を照合する
（2026-09-24 新設・13本目 ⑤b-2）。

■ なぜ要るか（⑤b-1 の相談で決めた「新しい型」＝記憶 project-jiko-visual-variety-from-ep12）
    模式図は形を省くかわりに**仕組みの順番**を見せる型。状態の並びが報告書の筋と食い違うと、
    動きがそのまま嘘になる（例：フックが回りきっていないのにピンが入る絵）。「規則を書いたら門番も」
    ＝[[feedback-rules-need-gates]]。drift の門番（check_drift）と同じ形。

■ 測るもの（**本番の関数 `titan_fig.latch()`／`section()` が置いた部品の画素**から＝SPEC の文字を読み比べない）
  latch（ドアの錠）
    1. 筋（報告書）：
       ピン in ⇒ フック closed（フックが閉まりきって初めてピンが入る・上院 p2017）
       ピン butt ⇒ フック ≠ closed（切り欠きが揃っていればピンは入る）
       通気扉 closed ⇔ ハンドル down（ハンドルが通気扉を閉める・上院 p2017〜p2018）
       ハンドル down かつ ピン ≠ in ⇔ 軸 bent（無理に閉めると軸がたわむ・仏 p88 図7・p80）
       ハンドル part ⇒ ピン ≠ in（途中で止まるのはピンが入れないから）
       灯り off ⇒ ハンドル down（灯りはハンドルの仕組みで消える）／空気 leak ⇒ 通気扉 open
    2. 画素：ピン in＝先が切り欠きの口より奥・切り欠きの上下がピンの上下を覆う
             ピン butt＝先が円板の縁の手前 0〜3画素・切り欠きがピンの行く手からずれている
             フック closed＝顎の中心が受けの中心 ±2画素／open・short＝15画素以上ずれる
             ハンドル・通気扉 down/closed＝水平 ±0.5度／軸 bent＝真ん中が20画素以上下がり赤
             灯り on＝赤／off＝赤でない
  section（胴体の断面）
    1. 筋：空気 out ⇒ ドア gone／床 push・down ⇒ ドア gone かつ 逃げ道 none／ケーブル hurt ⇒ 床 down／
          与圧 push ⇒ ドア on
    2. 画素：ドア gone＝重心が胴体の円の外（半径＋30画素より外）で見えない／床 down＝左端が元の床より60画素以上下／
             ケーブル hurt＝赤
  hull（14本目 ⑤b-4・断面F＝船の断面・`tools/hull.py`）
    1. 筋（記録）：延ばした ⇒ 天井を上げたあと（海審 p1016「천정을 약1.7미터 높인 후 … 연장」）／
          大理石 ⇒ 展示室（延ばした上の階）がある（p1024）／片寄った荷に固縛の帯が付いたまま、は無い／
          重心 high ⇒ 足した重さがある／元へ戻ろうとする力 ⇒ 傾いている／
          水は下がらない・3階の出入口が閉じる ⇒ 3階の手すりの上まで水・4階の出入口 ⇒ 4階の手すりの上まで（判決 p18）
    2. 画素：底のタンクの水の高さ＝表1・表7 の割合（±1%）／延ばした長さ 約5.6・約2.6・上げた天井 約1.7（±0.05メートル）／
             荷を減らした長さ＝987／2437／52.2度で3階（B甲板）の左舷の端が水面（±0.3メートル＝海審 p1057「닿을 정도」）／
             足したあとの重心が上・力の矢印が短い／水面が手すりの上下のどちらか
    ⚠️ 傾き heel の0でない値は `rel=[dict(heel=…, src=…)]` に宣言しないと型が止まる（記録に無い傾きは src="模式"）
  共通 3. 札の数（キロ・ミリ・メートル・ポンド・㎡・人・秒・分・時・度）は `rel=` の宣言に同じ文字列があること

■ 使い方
    python tools/check_mech.py              # 全カット
    python tools/check_mech.py --selftest   # 物差しの検算（陽性対照＝わざと食い違わせた筋・画素・数が落ちること）
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

# 🆕 ⑤b-7b：固縛の札の単位（トン・本・台・個・センチ）を足した（「約30本」が素通りした＝陽性対照で見つけた）
# 🆕 15本目 ⑤b-4：倍・回・ノット・G を足した（改造の比べ「約2倍」・締め直しのあとの「3回」・「17.3G」）
NUM = re.compile(r"約?[0-9０-９][0-9０-９,.．]*\s*(キロ|ミリ|メートル|ポンド|㎡|平方メートル|人|秒|分|時|度|トン|本|台|個|センチ|倍|回|ノット|G)")


def _shape(f, ident):
    return next(s for s in f.mech["shapes"] if s["id"] == ident)


def _at(sh, i):
    """段 i の鍵（鍵0＝頭・鍵 i+1＝段 i）。"""
    return sh["keys"][i + 1]


def _angle(p, q):
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))


def _numbers(f):
    bad = []
    said = [r.get("t", "") for r in f.mech["rel"]]
    for t in f.mech["tags"]:
        for m in NUM.finditer(t):
            if not any(m.group(0) in s for s in said):
                bad.append(f"札「{t}」の数「{m.group(0)}」が rel（報告書の値の宣言）に無い")
    for r in f.mech["rel"]:
        if not r.get("src"):
            bad.append(f"rel「{r.get('t')}」に出どころ（src）が無い")
    return bad


def judge_latch(f):
    bad, n = [], 0
    hx, hy = F.LT["hub"]
    sx, sy = F.LT["spool"]
    py, ph = F.LT["pin_y"], F.LT["pin_h"] / 2
    disc, pin, jaw = _shape(f, "disc"), _shape(f, "pin"), _shape(f, "jaw")
    handle, vent, tube, lamp = _shape(f, "handle"), _shape(f, "vent"), _shape(f, "tube"), _shape(f, "lamp")
    nd = 48                                             # 円板の弧の分け数（titan_fig.latch と同じ）
    for i, st in enumerate(f.mech["states"]):
        tag = f"段{i + 1}"
        # ── 1. 筋 ──
        rules = [
            (st["pin"] == "in" and st["hook"] != "closed", "ピンが入っているのにフックが閉まりきっていない"),
            (st["pin"] == "butt" and st["hook"] == "closed", "フックが閉まりきっているのにピンが縁で止まっている"),
            ((st["vent"] == "closed") != (st["handle"] == "down"), "通気扉とハンドルが食い違う（通気扉はハンドルが閉める）"),
            ((st["handle"] == "down" and st["pin"] != "in") != (st["tube"] == "bent"),
             "ハンドルが倒れているのにピンが入っていない＝軸がたわむはず（またはその逆）"),
            (st["handle"] == "part" and st["pin"] == "in", "ハンドルが途中で止まっているのにピンが入っている"),
            (st["lamp"] == "off" and st["handle"] != "down", "ハンドルが倒れていないのに灯りが消えている"),
            (st["air"] == "leak" and st["vent"] != "open", "通気扉が閉まっているのに空気が逃げている"),
        ]
        for hit, why in rules:
            n += 1
            if hit:
                bad.append(f"{tag}: {why}（{st}）")
        # ── 2. 画素（本番の関数が置いた部品）──
        dq = F.mech_pts(disc, _at(disc, i))
        mouth = (dq[0], dq[nd])                         # 切り欠きの口の上下の角
        inner = (dq[nd + 1], dq[nd + 2])                # 切り欠きの奥の角
        y_lo, y_hi = min(p[1] for p in mouth), max(p[1] for p in mouth)
        aligned = y_lo <= py - ph + 0.5 and y_hi >= py + ph - 0.5 and abs(mouth[0][0] - mouth[1][0]) < 3
        tip = max(p[0] for p in F.mech_pts(pin, _at(pin, i)))
        edge = hx - F.LT["R"]
        n += 1
        if st["pin"] == "in":
            deep = min(p[0] for p in inner)
            if not (aligned and min(p[0] for p in mouth) + 10 <= tip <= deep + 1):
                bad.append(f"{tag}: ピン in なのに、ピンの先 x={tip:.0f} が切り欠き（口 {min(p[0] for p in mouth):.0f}〜"
                           f"奥 {deep:.0f}・揃い {aligned}）に入っていない")
        elif st["pin"] == "butt":
            if aligned or not (edge - 3 <= tip <= edge):
                bad.append(f"{tag}: ピン butt なのに、先 x={tip:.0f}（縁 {edge}）・切り欠きが揃っている={aligned}")
        else:
            if tip > edge - 40:
                bad.append(f"{tag}: ピン out なのに、先 x={tip:.0f} が縁 {edge} に近すぎる")
        # 顎の中心（受けの中心を、フックと同じだけ回した点）
        rot = float(_at(jaw, i).get("rot", 0.0))
        jc = F.mech_pts(dict(pts=[[sx, sy]], pivot=[hx, hy]), dict(rot=rot))[0]
        off = math.hypot(jc[0] - sx, jc[1] - sy)
        n += 1
        if (st["hook"] == "closed") != (off <= 2.0) or (st["hook"] != "closed" and off < 15.0):
            bad.append(f"{tag}: フック {st['hook']} なのに、顎の中心が受けから {off:.1f}画素")
        hq = F.mech_pts(handle, _at(handle, i))
        vq = F.mech_pts(vent, _at(vent, i))
        n += 2
        if (st["handle"] == "down") != (abs(_angle(hq[0], hq[1])) <= 0.5):
            bad.append(f"{tag}: ハンドル {st['handle']} なのに、レバーの角度 {_angle(hq[0], hq[1]):.1f}度")
        if (st["vent"] == "closed") != (abs(_angle(vq[0], vq[1])) <= 0.5):
            bad.append(f"{tag}: 通気扉 {st['vent']} なのに、扉の角度 {_angle(vq[0], vq[1]):.1f}度")
        tk = _at(tube, i)
        sag = max(p[1] for p in tk["pts"]) - tk["pts"][0][1]          # 弓なりのいちばん下と端の差
        n += 1
        if (st["tube"] == "bent") != (sag >= 20 and tk.get("stroke") == "ALERT"):
            bad.append(f"{tag}: 軸 {st['tube']} なのに、真ん中の下がり {sag:.0f}画素・色 {tk.get('stroke')}")
        n += 1
        if (st["lamp"] == "on") != (_at(lamp, i).get("fill") == "ALERT"):
            bad.append(f"{tag}: 灯り {st['lamp']} なのに、色 {_at(lamp, i).get('fill')}")
    bad += _numbers(f)
    return bad, n


def judge_section(f):
    bad, n = [], 0
    cx, cy = F.SC["c"]
    R, fy = F.SC["R"], F.SC["floor_y"]
    door, floor = _shape(f, "door"), _shape(f, "floorL")
    cables = [s for s in f.mech["shapes"] if s["id"].startswith("cable")]
    for i, st in enumerate(f.mech["states"]):
        tag = f"段{i + 1}"
        rules = [
            (st["air"] == "out" and st["door"] != "gone", "ドアが付いているのに貨物室の空気が抜けている"),
            (st["floor"] in ("push", "down") and st["door"] != "gone", "ドアが付いているのに床に圧力の差がかかる"),
            (st["floor"] in ("push", "down") and st["vent"] == "open", "床に逃げ道があるのに床が押される・落ちる"),
            (st["cable"] == "hurt" and st["floor"] != "down", "床が落ちていないのにケーブルが傷む"),
            (st["press"] == "push" and st["door"] != "on", "ドアが無いのにドアを押す力を描いている"),
        ]
        for hit, why in rules:
            n += 1
            if hit:
                bad.append(f"{tag}: {why}（{st}）")
        dk = _at(door, i)
        dq = F.mech_pts(door, dk)
        gx, gy = sum(p[0] for p in dq) / len(dq), sum(p[1] for p in dq) / len(dq)
        out = math.hypot(gx - cx, gy - cy) > R + 30 and float(dk.get("alpha", 1.0)) <= 0.05
        n += 1
        if (st["door"] == "gone") != out:
            bad.append(f"{tag}: ドア {st['door']} なのに、重心は中心から {math.hypot(gx - cx, gy - cy):.0f}画素"
                       f"・見え {dk.get('alpha')}")
        fq = F.mech_pts(floor, _at(floor, i))
        n += 1
        if (st["floor"] == "down") != (fq[0][1] - fy >= 60):
            bad.append(f"{tag}: 床 {st['floor']} なのに、左端の下がり {fq[0][1] - fy:.0f}画素")
        n += 1
        red = all(_at(c, i).get("fill") == "ALERT" for c in cables)
        if (st["cable"] == "hurt") != red:
            bad.append(f"{tag}: ケーブル {st['cable']} なのに、色 {[ _at(c, i).get('fill') for c in cables]}")
    bad += _numbers(f)
    return bad, n


# 🔴 断面F の記録の値は**門番の側にも別に持つ**（型の定数と比べると、型を壊しても「型どおり」で通る＝物差しにならない）
# 🔴 2026-09-30（15本目 リノ ⑤b-1・§0b）：14本目（セウォル号）の REC_HULL・REC_LASH は selftest の見本 `tools/fixture_ep14.py`
#    （GATES["check_mech"]・値は1つも変えていない）へ移した＝空。断面F（hull）と固縛（lash）は14本目の船の型＝15本目は使わない。
#    15本目の尾翼の板の模式図（映像方針 §4）で記録の値が要る型を足すときは、その型の記録の表をここに別に持つ（§5b-88）
REC_HULL = {}
REC_LASH = {}


def judge_hull(f):
    """断面F（`tools/hull.py`）。部品の形は `hull.parts_of`＝描く側と同じ関数が組んだもの。"""
    import hull as H
    R = REC_HULL
    m = f.mech
    bad, n = [], 0
    view = m["view"]
    kind = H.kind_of(view)
    v = H.VIEWS[view]
    seq = [m["start"]] + m["states"]
    shp = {s["id"]: s for s in m["shapes"]}

    def pts(ident, i):
        return F.mech_pts(shp[ident], shp[ident]["keys"][i])

    def alpha(ident, i):
        a = shp[ident]["keys"][i].get("alpha", 1.0)
        return 1.0 if a is None else float(a)

    def span(q, ax):
        return max(p[ax] for p in q) - min(p[ax] for p in q)
    for i, st in enumerate(seq):
        tag = "頭" if i == 0 else f"段{i}"
        if kind == "side":
            s = v["s"]
            rules = [(st["aext"] == "on" and st["aroof"] != "high", "後ろへ延ばしたのに天井が上がっていない（海審 p1016＝上げてから延ばした）"),
                     (st["marble"] == "on" and st["aext"] != "on", "展示室（延ばした上の階）が無いのに大理石（海審 p1024）"),
                     (i == 0 and st["ramp"] == "gone", "頭の状態で渡し板が「外した」（外す動きは段で見せる）")]
            if st["ballast"] != "none":
                frac = span(pts("bw", i), 1) / (H.E_Y * s)
                want = R["bw"][st["ballast"]]
                rules.append((abs(frac - want) > 0.01 or alpha("bw", i) < 0.5,
                              f"底のタンクの水の高さ {frac:.3f}＝宣言 {want:.3f}（表1・表7）と違う・または見えない"))
            if st["aext"] == "on":
                wa, wb = span(pts("aext_f", i), 0) / s, span(pts("brext_f", i), 0) / s
                roof = span(pts("comp_f", i), 1) / s
                rules += [(abs(wa - R["a_ext"]) > 0.05, f"A甲板の延ばした長さ {wa:.2f}＝記録 約{R['a_ext']}（p1016）と違う"),
                          (abs(wb - R["br_ext"]) > 0.05, f"船橋甲板の延ばした長さ {wb:.2f}＝記録 約{R['br_ext']}（p1016）と違う"),
                          (abs(roof - (R["roof0"] + R["rise"])) > 0.05,
                           f"部屋の天井の高さ {roof:.2f}＝記録 約{R['roof0']}＋約{R['rise']}（p1016）と違う")]
            if st["cargo"] == "less":
                r = span(pts("cg_d_f", i), 0) / ((118.0 - 8.0) * s)
                rules.append((abs(r - R["cargo_less"]) > 0.01, f"減らした荷の長さの比 {r:.3f}＝987／2437（表1）と違う"))
        elif kind == "front":
            rules = [(st["cargo"] == "port" and st["lash"] == "on", "片寄った荷に固縛の帯が付いたまま")]
            if abs(st["heel"] - 52.2) < 0.01:
                q = pts("dkB", i)
                dm = (q[1][1] - v["piv"][0][1]) / v["s"]
                rules.append((abs(dm) > 0.3, f"52.2度で3階の左舷の端が水面から {dm:+.2f} メートル（記録＝届くほど＝海審 p1057）"))
        elif kind == "pair":
            rules = [(st["g"] == "high" and st["add"] != "on", "足した重さが無いのに重心が上がっている"),
                     (st["force"] == "on" and abs(st["heel"]) < 0.01, "傾いていないのに元へ戻ろうとする力を描いている")]
            yl = sum(p[1] for p in pts("L_g", i)) / 12
            yr = sum(p[1] for p in pts("R_g", i)) / 12
            if st["g"] == "high":
                rules.append((not yr < yl - 8, f"足したあとの重心が上に描かれていない（左 {yl:.0f}・右 {yr:.0f}画素）"))
            if st["force"] == "on":
                la = sum(math.dist(a, b) for a, b in zip(pts("L_force", i), pts("L_force", i)[1:]))
                ra = sum(math.dist(a, b) for a, b in zip(pts("R_force", i), pts("R_force", i)[1:]))
                rules.append((st["g"] == "high" and not ra < la,
                              f"重心が高い船の力の矢印が短くない（左 {la:.0f}・右 {ra:.0f}画素）"))
        elif kind == "mark":
            # 🆕 ⑤b-7b（c211）：水面と限りの線の画素を目盛りの式で喫水へ戻す＝記録（海審 p1038）
            V = H._MarkV(v)
            rules = []
            yw = min(p[1] for p in pts("water", i))
            yf = pts("full", i)[0][1]
            if st["water"] == "seen":
                dw = (V.p(0, R["draft_seen"])[1] - yw) / v["s"]
                rules.append((abs(dw) > 0.005 or alpha("water", i) < 0.2,
                              f"水面が記録の約{R['draft_seen']}メートルから {dw:+.3f} メートル（海審 p1038）・または見えない"))
            if st["full"] == "on":
                df = (V.p(0, R["draft_full"])[1] - yf) / v["s"]
                rules.append((abs(df) > 0.005 or alpha("full", i) < 0.5,
                              f"限りの線が記録の {R['draft_full']}メートルから {df:+.3f} メートル（海審 p1038）・または見えない"))
                rules.append((st["water"] == "seen" and not yf < yw, "限りの線が水面より下（記録＝確かめた値は限りの内）"))
        else:
            V = H._PortV(v)
            top = min(p[1] for p in pts("water", i))
            f3, r3, r4 = V.p(0, H.B_Y)[1], V.p(0, H.B_Y + H.RAIL_H)[1], V.p(0, H.A_Y + H.RAIL_H)[1]
            order = {"low": 0, "b": 1, "a": 2}
            rules = [(i > 0 and order[st["water"]] < order[seq[i - 1]["water"]], "水が下がる（記録＝3階→4階の順＝判決 p18）"),
                     (st["water"] == "low" and not top > f3, "まだ水の前なのに3階の床より上に水"),
                     (st["water"] == "b" and not (r4 < top < r3), "3階の手すりの上・4階の手すりの下に水の面が無い"),
                     (st["water"] == "a" and not top < r4, "4階の手すりが水の上に出ている"),
                     (st["exits"] in ("shut3", "shut") and st["water"] == "low", "水の前に出入口が閉じている"),
                     (st["exits"] == "shut" and st["water"] != "a", "4階の手すりがつかる前に4階の出入口が閉じている")]
        for hit, why in rules:
            n += 1
            if hit:
                bad.append(f"{tag}: {why}")
    bad += _numbers(f)
    return bad, n


def judge_lash(f):
    """🆕 ⑤b-7b：固縛（`tools/lash.py`）。**描いた SVG の印 data-l を数える**＝本数・木の止め・面・留め金。"""
    import lash as Lh
    R = REC_LASH
    m = f.mech
    svg = f.lab + "".join(f.stages)
    c = Lh.count(svg)
    bad, n = [], 0
    final = (m["states"] or [m["start"]])[-1]

    def got(key):
        return c.get(key, 0)
    for who in ("car", "truck"):
        lv = final.get(who, "off")
        if lv == "off":
            continue
        n += 1
        wheels, chocks = got(f"{who}|wheel"), got(f"{who}|chock")
        if lv == "all" and chocks != wheels:
            bad.append(f"{who}: 木の止め {chocks} 個・タイヤ {wheels} 個（記録＝各タイヤに＝海審 p1042 3.1.4.3・p1093）")
        if lv != "all" and chocks:
            bad.append(f"{who}: 実際の固縛の前に木の止めが {chocks} 個")
        req = {e: got(f"{who}|req|{e}") for e in ("front", "rear", "side")}
        act = {e: got(f"{who}|act|{e}") for e in ("front", "rear", "side")}
        if lv in ("req", "all"):
            n += 1
            if who == "car" and (req["front"], req["rear"], req["side"]) != (R["car_req"]["front"], R["car_req"]["rear"], 0):
                bad.append(f"乗用車の基準の帯 前{req['front']}・後ろ{req['rear']}・横{req['side']}（記録＝前・後ろ2本ずつ＝p1093 4.4.1）")
            if who == "truck" and sum(req.values()) != R["truck_req"]:
                bad.append(f"25トン車の基準の帯 {sum(req.values())} 本（記録＝10本＝p1093 4.4.2）")
        if lv == "all":
            n += 1
            if who == "car" and (act["front"], act["rear"], act["side"]) != (R["car_act"]["front"], R["car_act"]["rear"], 0):
                bad.append(f"乗用車の実際の帯 前{act['front']}・後ろ{act['rear']}・横{act['side']}（記録＝前・後ろ1本ずつ＝p1093 4.4.1）")
            if who == "truck" and sum(act.values()) != R["truck_act"]:
                bad.append(f"25トン車の鎖 {sum(act.values())} 本（記録＝4本＝p1093 4.4.2）")
        elif sum(act.values()):
            bad.append(f"{who}: 状態 {lv} なのに実際の帯が {sum(act.values())} 本")
    if final.get("zone") == "on":
        n += 1
        zb = got("zone|belt")
        if zb != R["zone_belts"] or not got("zone|area"):
            bad.append(f"仮ナンバーの乗用車の面：帯 {zb} 本・面 {got('zone|area')}（記録＝帯なし＝p1042 3.1.4.4・p1093 4.4.5）")
    if m["view"] == "box":
        n += 1
        if got("box|lock|used") != R["lock_used"]:
            bad.append(f"留め金を使った絵が {got('box|lock|used')} か所（記録＝使っていない＝p1042 3.1.4.5・p1093 4.4.3）")
        if final.get("rope") == "on" and not got("box|rope"):
            bad.append("ロープの状態 on なのに、ロープの絵が無い")
        if final.get("lock") == "on" and not got("box|lock|empty"):
            bad.append("留め金の場所の状態 on なのに、点線の枠が無い")
        if got("box|casting") != 8:
            bad.append(f"隅の金具 {got('box|casting')} 個（横から見た2段の箱は 4×2＝8）")
    bad += _numbers(f)
    return bad, n


def judge_tail(f):
    """15本目 ⑤b-3：尾翼の板の模式図（`tools/tail15.py`）。①筋（AAB）②本番の関数が置いた部品の画素 ③札の数。"""
    import tail15 as T
    bad, n = [], 0
    view = f.mech["view"]
    sh = {s["id"]: s for s in f.mech["shapes"]}

    def pts(ident, i):
        return F.mech_pts(sh[ident], _at(sh[ident], i))

    def alpha(ident, i):
        a = _at(sh[ident], i).get("alpha", 1.0)
        return 1.0 if a is None else float(a)

    def gap(a, b):
        return math.hypot(b[0][0] - a[-1][0], b[0][1] - a[-1][1])

    for i, st in enumerate(f.mech["states"]):
        tag = f"段{i + 1}"
        if view == "side":
            rules = [
                (st["tab"] == "free" and st["link"] != "broken", "板が限り（約13度＝p23）を越えたのにリンクが折れていない（p28 0.56秒）"),
                (st["link"] == "broken" and st["force"] == "on", "リンクが折れたのに板が昇降舵を押す力が残っている（p41〜p42）"),
                (st["elev"] == "up" and (st["link"] != "broken" or st["force"] != "off"),
                 "昇降舵がはね上がるのは、板の押す力が消えた（リンクが折れた）あと（c322・p41〜p42）"),
                (st["nose"] == "on" and st["elev"] != "up", "機首が上がるのは昇降舵がはね上がってから"),
                (st["force"] == "on" and st["tab"] != "up", "押す力は後ろの縁が上の板（機首下げの調整＝p22・p42）から"),
                (st["elev"] == "down" and st["force"] != "on", "昇降舵の後ろの縁が下がるのは板の押す力で"),
                (st["ghost"] == "on" and st["tab"] == "zero", "0度の点線（整備の仲間の見方＝p15）は板が0度でないときだけ"),
                # 🆕 ⑤b-4（c511）：材料を塗って板が重くなり重心が後ろへ（p40）
                (st["cg"] == "aft" and st["fill"] != "on", "板の重心が後ろへ動くのは、表面に材料を塗ったから（p14・p40）"),
            ]
        else:
            rules = [
                (st["rlink"] == "broken" and st["llink"] != "broken", "右のリンクが先に折れた（記録は左→右＝p40）"),
                (st["shake"] == "both" and st["llink"] != "broken", "右の板の震えは左のリンクの震えと破断のあと（p40）"),
                (st["spread"] == "on" and st["shake"] != "both", "左から右への広がりの矢印なのに右が震えていない"),
                (st["mode"] == "stock" and (st["llink"] != "ok" or st["rlink"] != "ok" or st["shake"] != "none"),
                 "ふつうの P-51D（stock）の絵に事故の壊れ方を描いた"),
                (st["rod"] == "on" and st["mode"] != "mod", "鉄の棒（p14）は改造後の右の板だけ"),
            ]
        for hit, why in rules:
            n += 1
            if hit:
                bad.append(f"{tag}: {why}（{st}）")
        # ── 画素 ──
        if view == "side":
            eq = pts("elev", i)
            te = [(eq[T.E_TE[0]][0] + eq[T.E_TE[1]][0]) / 2, (eq[T.E_TE[0]][1] + eq[T.E_TE[1]][1]) / 2]
            ea = math.degrees(math.atan2(te[1] - T.E_H[1], te[0] - T.E_H[0]))
            e_deg = ((ea - 180.0 + 180.0) % 360.0) - 180.0
            tq = pts("tab", i)
            th = T._elev_pt(T.T_H, st)
            tt = [(tq[T.T_TE[0]][0] + tq[T.T_TE[1]][0]) / 2, (tq[T.T_TE[0]][1] + tq[T.T_TE[1]][1]) / 2]
            ta = math.degrees(math.atan2(tt[1] - th[1], tt[0] - th[0]))
            t_deg = ((ta - ea + 180.0) % 360.0) - 180.0
            n += 2
            want_e = dict(trim=(-0.5, 0.5), down=(-12.0, -2.0), up=(8.0, 25.0))[st["elev"]]
            if not want_e[0] <= e_deg <= want_e[1]:
                bad.append(f"{tag}: 昇降舵 {st['elev']} なのに、描いた角度 {e_deg:+.1f}度（{want_e}）")
            # 板の角度：zero＝0度／up＝後ろの縁が上へ 5〜13度（p22 の写真 5・8度・p23 の限り）／free＝21度以上（p28）
            want_t = dict(zero=(-0.5, 0.5), up=(5.0, 13.0), free=(21.0, 60.0))[st["tab"]]
            if not want_t[0] <= t_deg <= want_t[1]:
                bad.append(f"{tag}: 板 {st['tab']} なのに、昇降舵に対する角度 {t_deg:+.1f}度（記録の幅 {want_t}）")
            g_ = gap(pts("link_a", i), pts("link_b", i))
            red = _at(sh["link_a"], i).get("stroke") == "ALERT"
            n += 1
            if (st["link"] == "broken") != (g_ >= 20.0 and red):
                bad.append(f"{tag}: リンク {st['link']} なのに、すき間 {g_:.0f}画素・赤 {red}")
            for ident, on in (("force", st["force"] == "on"), ("nose", st["nose"] == "on"), ("ghost", st["ghost"] == "on"),
                              ("fill_stab0", st["fill"] == "on"), ("fill_tab1", st["fill"] == "on"), ("cg", st["cg"] != "off"),
                              ("cg_wt", st["cg"] == "aft")):
                n += 1
                if (alpha(ident, i) > 0.5) != on:
                    bad.append(f"{tag}: {ident} の濃さ {alpha(ident, i)} が状態と違う")
            # 🆕 ⑤b-4：塗った材料の帯は面の外（上の縁の帯は面より上・下の縁の帯は面より下）・重心 aft は元の重心より後ろ（左）
            if st["fill"] == "on":
                n += 1
                mean_y = lambda ps: sum(p[1] for p in ps) / len(ps)  # noqa: E731
                up, dn = mean_y(pts("fill_tab0", i)), mean_y(pts("fill_tab1", i))
                up_edge, dn_edge = mean_y(tq[0:3]), mean_y(tq[3:6])
                if not (up < up_edge - 2.0 and dn > dn_edge + 2.0):
                    bad.append(f"{tag}: 塗った材料の帯が板の外に出ていない（帯 上 {up:.0f}・下 {dn:.0f}／板の縁 上 {up_edge:.0f}・"
                               f"下 {dn_edge:.0f}）")
            if st["cg"] == "aft":
                n += 1
                c_now = [sum(v) / len(v) for v in zip(*pts("cg", i))]
                c_old = [sum(v) / len(v) for v in zip(*pts("cg_old", i))]
                if not c_old[0] - c_now[0] >= 20.0:
                    bad.append(f"{tag}: 重心 aft なのに、元の重心より後ろ（左）へ {c_old[0] - c_now[0]:.0f}画素（20以上のはず）")
        else:
            mod = st["mode"] == "mod"
            for ident, on in (("rod", mod), ("act_r", not mod), ("link_rs", not mod), ("bolt", mod),
                              ("shake_l", st["shake"] in ("left", "both")), ("shake_r", st["shake"] == "both"),
                              ("spread", st["spread"] == "on")):
                n += 1
                if (alpha(ident, i) > 0.5) != on:
                    bad.append(f"{tag}: {ident} の濃さ {alpha(ident, i)} が状態 {st} と違う")
            for side in ("l", "r"):
                g_ = gap(pts(f"link_{side}a", i), pts(f"link_{side}b", i))
                red = _at(sh[f"link_{side}a"], i).get("stroke") == "ALERT"
                brk = st[f"{side}link"] == "broken"
                n += 1
                if brk != (g_ >= 20.0 and red):
                    bad.append(f"{tag}: {'左' if side == 'l' else '右'}のリンク {st[side + 'link']} なのに、すき間 {g_:.0f}画素・赤 {red}")
    bad += _numbers(f)
    return bad, n


# ── 15本目 ⑤b-4：改造の比べ（mod）・ねじとナットとフラッター（bolt）の記録の値＝門番の側に独立して持つ
#    （型の定数を読まない＝型の定数を壊す陽性対照が捕まえられる）──
# 🔴 2026-10-01（16本目 バイオントダム災害 ⑤b-1・§0b）：15本目の REC_MOD・REC_BOLT は selftest の見本 `tools/fixture_ep15.py`
#    （GATES["check_mech"]・値は1つも変えていない＝git の `c646174`）へ移した＝空。selftest は見本の表だけ差し込む
#    （`fixture_ep15.apply(gate, tables_only=True)`）。16本目で改造の比べ（mod）・ねじ（bolt）の型を使うときは、
#    その回の記録の値をここに別に持つ（§5b-88）。`_FT, _LB`＝メートル・キロの換算（見本の表の式も同じ値）
_FT, _LB = 0.3048, 0.45359237
REC_MOD = {}
REC_BOLT = {}


def _in_poly(p, poly):
    x, y = p
    inside = False
    n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            inside = not inside
    return inside


def _mid(ps):
    return [sum(p[0] for p in ps) / len(ps), sum(p[1] for p in ps) / len(ps)]


def judge_mod(f):
    """15本目 ⑤b-4：改造の比べ（`tools/mod15.py`）。①筋（AAB p13・p14・p42・p43）②本番の関数が置いた部品の画素 ③札の数。"""
    import mod15 as Mo
    bad, n = [], 0
    view = f.mech["view"]
    sh = {s["id"]: s for s in f.mech["shapes"]}

    def pts(ident, i):
        return F.mech_pts(sh[ident], _at(sh[ident], i) if i >= 0 else sh[ident]["keys"][0])

    def alpha(ident, i):
        a = _at(sh[ident], i).get("alpha", 1.0)
        return 1.0 if a is None else float(a)

    # ── 形（段によらない）──
    if view == "plan":
        mod_ = pts("mod", -1)
        span_m = (max(p[1] for p in mod_) - min(p[1] for p in mod_)) / Mo.K_P
        top = min(p[1] for p in pts("stk_wing_l", -1))
        bot = max(p[1] for p in pts("stk_wing_r", -1))
        span_s = (bot - top) / Mo.K_P
        n += 2
        for nm, got, rec in (("事故機の翼の幅", span_m, REC_MOD["span_mod"]), ("ふつうの翼の幅", span_s, REC_MOD["span_stock"])):
            if abs(got / rec - 1.0) > 0.015:
                bad.append(f"{nm}：描いた {got:.2f}メートル ≠ 記録 {rec:.3f}（±1.5%＝AAB p13）")
        # 寸法の線の端＝翼端（±3画素）
        for nm, (y0, y1) in (("dim_s", (top, bot)), ("dim_m", (min(p[1] for p in mod_), max(p[1] for p in mod_)))):
            n += 1
            a_, b_ = pts(nm + "_a", -1)[-1], pts(nm + "_b", -1)[-1]
            if abs(a_[1] - y0) > 3.0 or abs(b_[1] - y1) > 3.0:
                bad.append(f"寸法の線 {nm} の端 {a_[1]:.0f}・{b_[1]:.0f} が翼端 {y0:.0f}・{y1:.0f} と違う")
        # おもりの印は水平尾翼の中（事故機の輪郭の内）・補助翼は翼の後ろの縁
        for s in ("l", "r"):
            n += 1
            if not _in_poly(_mid(pts(f"cw_{s}", -1)), mod_):
                bad.append(f"昇降舵のおもりの印（{s}）が機体の形の外")
            n += 1
            aq = pts(f"ail_{s}", -1)
            if not all(_in_poly(_mid([p, _mid(aq)]), mod_) for p in aq):
                bad.append(f"補助翼（{s}）が翼の形の外にはみ出す")
        # 補助翼の断面：後ろの縁が少し下（p43）＝基準の線より 8画素以上下
        n += 1
        ail_te = max(pts("ins_ail", -1), key=lambda p: -p[0])
        ref_te = min(pts("ins_ref", -1), key=lambda p: p[0])
        if not ail_te[1] - ref_te[1] >= 8.0:
            bad.append(f"補助翼の断面：後ろの縁が基準より {ail_te[1] - ref_te[1]:.0f}画素下（8以上のはず＝p43 後ろの縁が少し下）")
    elif view == "side":
        body = pts("mod", -1)
        n += 2
        if not all(_in_poly(p, body) for p in pts("box", -1)):
            bad.append("沸かして冷やす箱が胴の形の外（p13＝操縦席の後ろの胴の中）")
        if _in_poly(pts("vent", -1)[-1], body):
            bad.append("湯気の矢印の先が胴の中（外へ逃がす＝p13 注11）")
    else:
        h = {k: (lambda ps: max(p[1] for p in ps) - min(p[1] for p in ps))(pts(k, -1)) for k in ("cw_stock", "cw_acc", "bw_stock", "bw_acc")}
        n += 3
        if abs((h["cw_acc"] / h["cw_stock"]) / REC_MOD["cw_ratio"] - 1.0) > 0.02:
            bad.append(f"おもりの高さの比 {h['cw_acc'] / h['cw_stock']:.3f} ≠ 記録 {REC_MOD['cw_ratio']:.3f}（26／13.75ポンド＝AAB p14）")
        if abs(h["cw_acc"] / Mo.K_W / REC_MOD["cw_kg"] - 1.0) > 0.02:
            bad.append(f"左のおもりの高さ {h['cw_acc'] / Mo.K_W:.2f}キロ ≠ 記録 {REC_MOD['cw_kg']:.2f}")
        r = h["bw_acc"] / h["bw_stock"]
        if abs(r / REC_MOD["bw_ratio"] - 1.0) > 0.02 or not r < 0.5:
            bad.append(f"動きを安定させるおもりの比 {r:.3f} ≠ 記録 {REC_MOD['bw_ratio']:.3f}（半分未満＝AAB p43・#53 p10）")
    for i, st in enumerate(f.mech["states"]):
        tag = f"段{i + 1}"
        if view == "plan":
            rules = [
                (st["span"] == "on" and st["stock"] != "on", "翼の幅の寸法は、ふつうの P-51D の形（緑）と並べて出す"),
                (st["wing"] == "on" and st["stock"] != "on", "「短い翼」の印は、ふつうの翼（緑）と並べて出す（p42）"),
            ]
            ons = [("stk_wing_l", st["stock"] == "on"), ("stk_wing_l_ln", st["stock"] == "on"), ("dim_s_a", st["span"] == "on"),
                   ("dim_m_b", st["span"] == "on"), ("tailring", st["tailring"] == "on"), ("cw_l", st["cw"] == "on"),
                   ("wing_l", st["wing"] == "on"), ("shake0", st["shake"] == "on"), ("ail_l", st["ail"] == "on"),
                   ("ins_ail", st["ail"] == "on")]
        elif view == "side":
            rules = [
                (st["boil"] == "on" and st["boiler"] != "on", "沸く印は、沸かして冷やす箱があるときだけ"),
                (st["vent"] == "on" and st["boil"] != "on", "湯気で外へ逃がすのは、液が沸いてから（p13 注11）"),
            ]
            ons = [("box", st["boiler"] == "on"), ("bub0", st["boil"] == "on"), ("vent", st["vent"] == "on"),
                   ("scoop_ln", True)]
        else:
            rules = [
                (st["cwx2"] == "on" and st["cw"] != "both", "「約2倍」の線は、ふつうの最大と事故機の両方を出してから"),
                (st["sens"] == "on" and st["cw"] != "both", "機首の上げ下げが敏感に＝おもりの比べ（p43）を出してから"),
            ]
            ons = [("cw_acc", st["cw"] in ("acc", "both")), ("cw_stock", st["cw"] == "both"), ("cw_line", st["cwx2"] == "on"),
                   ("bw_acc", st["bw"] == "on"), ("sens", st["sens"] == "on")]
        for hit, why in rules:
            n += 1
            if hit:
                bad.append(f"{tag}: {why}（{st}）")
        for ident, on in ons:
            n += 1
            if (alpha(ident, i) > 0.05) != on:
                bad.append(f"{tag}: {ident} の濃さ {alpha(ident, i)} が状態と違う")
    bad += _numbers(f)
    return bad, n


def judge_bolt(f):
    """15本目 ⑤b-4：ねじ・ナット・フラッター（`tools/bolt15.py`）。①筋（AAB p31・p40・p41・#40）②画素 ③札の数。"""
    import bolt15 as B
    bad, n = [], 0
    view = f.mech["view"]
    sh = {s["id"]: s for s in f.mech["shapes"]}

    def pts(ident, i):
        return F.mech_pts(sh[ident], _at(sh[ident], i) if i >= 0 else sh[ident]["keys"][0])

    def alpha(ident, i):
        a = _at(sh[ident], i).get("alpha", 1.0)
        return 1.0 if a is None else float(a)

    seq = [f.mech["start"]] + list(f.mech["states"])
    if view == "nut":
        # 決まりの長さと実際の長さ（頭の下）の比＝#40 の実測
        n += 1
        l_spec = B.TIP["spec"] - B.HEAD_B
        l_short = B.TIP["short"] - B.HEAD_B
        if abs((l_short / l_spec) / REC_BOLT["len_ratio"] - 1.0) > 0.02:
            bad.append(f"ねじの長さの比 {l_short / l_spec:.3f} ≠ 記録 {REC_BOLT['len_ratio']:.3f}（0.96／1.219インチ＝#40 p2・p6）")
    tightened = seq[0].get("tight") == "on"
    for i, st in enumerate(f.mech["states"]):
        tag = f"段{i + 1}"
        prev = seq[i]
        if view == "nut":
            nf, pf = int(st["flights"]), int(prev["flights"])
            rules = [
                (st["ghost"] == "on" and st["screw"] != "short", "決まりの長さの影は、実際のねじが短いときだけ（p31）"),
                (st["tip"] == "on" and st["screw"] != "short", "先の輪（ナットの端とそろう）は短いねじのとき（p31）"),
                (st["clamp"] == "on" and st["insert"] != "new", "古い詰め物はねじ山をほとんど締めつけない（p31）"),
                (st["loose"] == "on" and st["insert"] != "old", "ねじのゆるみは古いナット（詰め物）から（p40）"),
                (st["paint"] == "on" and st["loose"] != "on", "塗装のはげ＝ゆるんだねじでこすれ合った跡（p31）"),
                (st["tight"] == "on" and st["loose"] == "on", "締め直した段でゆるんでいる"),
                (nf < pf, "飛行の数が減った"),
                (nf > 0 and not (tightened or st["tight"] == "on"), "飛行の数は締め直しのあとから数える（p41）"),
                (st["loose"] == "on" and tightened and nf == 0, "締め直したあと、飛ばずにゆるんだ（p41＝そのあと3回飛んだ）"),
                (nf > REC_BOLT["flights"], f"締め直しのあとの飛行は {REC_BOLT['flights']}回（p41）"),
            ]
            tightened = tightened or st["tight"] == "on"
            # 画素：ねじの先とナットの端・詰め物のすき間・印の濃さ
            sq = pts("shank", i)
            tip = max(p[1] for p in sq)
            n += 2
            if st["screw"] == "short" and abs(tip - B.NUT_END) > 2.0:
                bad.append(f"{tag}: 短いねじの先 {tip:.0f} がナットの端 {B.NUT_END:.0f} とそろわない（p31）")
            if st["screw"] == "spec" and not tip - B.NUT_END >= 20.0:
                bad.append(f"{tag}: 決まりのねじの先 {tip:.0f} がナットの端 {B.NUT_END:.0f} から出ていない")
            gap = min(p[0] for p in sq) - max(p[0] for p in pts("ins_l", i))
            if (st["insert"] == "old") != (gap >= 4.0) or (st["insert"] == "new" and gap > 1.0):
                bad.append(f"{tag}: 詰め物 {st['insert']} なのに、ねじとのすき間 {gap:.1f}画素")
            ons = [("ghost", st["ghost"] == "on"), ("tipring", st["tip"] == "on"), ("clamp0", st["clamp"] == "on"),
                   ("turn", st["loose"] == "on"), ("slip_a", st["loose"] == "on"), ("paint0", st["paint"] == "on"),
                   ("tight", st["tight"] == "on")] + [(f"fly{j}", nf > j) for j in range(3)]
        elif view == "spring":
            rules = [
                (st["stiff"] == "low" and st["screw"] != "loose", "支えのかたさが落ちるのは、ねじのゆるみから（p40）"),
                (st["wobble"] == "on" and st["screw"] != "loose", "板がぐらつくのは、ねじがゆるんでから（p40）"),
                (st["shake"] == "on" and st["stiff"] != "low", "フラッターは、支えのかたさが落ちてから（p40）"),
                (st["air"] == "on" and st["shake"] != "on", "空気の力がかみ合う矢印は、震えているとき"),
                (st["graph"] == "on" and st["shake"] != "on", "震えの続き方は、震えが起きてから"),
            ]
            # 画素：揺れの幅（板の後ろの縁の角度）
            th = abs(_at(sh["tab_up"], i).get("rot", 0.0) or 0.0)
            n += 1
            want = REC_BOLT["shake_deg"] if st["shake"] == "on" else REC_BOLT["wobble_deg"] if st["wobble"] == "on" else None
            if want and not (want[0] <= th <= want[1] and alpha("tab_up", i) > 0.2):
                bad.append(f"{tag}: 板の揺れの幅 {th:.1f}度（{want}）")
            if want is None and alpha("tab_up", i) > 0.05:
                bad.append(f"{tag}: 揺れていないのに揺れの影が出ている")
            if st["air"] == "on":
                n += 2
                au, ad = pts("air_up", i), pts("air_dn", i)
                te_up = max(pts("tab_up", i), key=lambda p: -p[0])
                if not (au[-1][1] < au[0][1] and au[0][1] < te_up[1]):
                    bad.append(f"{tag}: 上へ揺れた板の後ろの縁の上で、空気の力が上を向いていない（かみ合う＝向きがそろう）")
                te_dn = max(pts("tab_dn", i), key=lambda p: -p[0])
                if not (ad[-1][1] > ad[0][1] and ad[0][1] > te_dn[1]):
                    bad.append(f"{tag}: 下へ揺れた板の後ろの縁の下で、空気の力が下を向いていない")
            if st["graph"] == "on":
                n += 2
                for ident, lo, hi in (("g_steady", 0.85, 1.15), ("g_grow", 4.0, 99.0)):
                    q = pts(ident, i)
                    cy = sum(p[1] for p in q) / len(q)
                    k = len(q) // 4
                    a0 = max(abs(p[1] - cy) for p in q[:k])
                    a1 = max(abs(p[1] - cy) for p in q[-k:])
                    if not lo <= a1 / max(a0, 1e-6) <= hi:
                        bad.append(f"{tag}: {ident} の幅の比（終わり／始め）{a1 / max(a0, 1e-6):.2f}（{lo}〜{hi}）")
            ons = [("spr_lo", st["stiff"] == "low"), ("spr_hi", st["stiff"] == "high"), ("scr_gap", st["screw"] == "loose"),
                   ("zz", st["shake"] == "on"), ("air_up", st["air"] == "on"), ("g_grow", st["graph"] == "on")]
        else:
            rules = [
                (st["ring"] == "on" and st["acc"] != "on", "輪は事故機の点に付ける"),
                (st["acc"] == "on" and st["region"] != "on", "事故機の点は、起きやすい所と一緒に出す"),
                (st["arrows"] == "on" and st["region"] != "on", "向きの矢印は、起きやすい所と一緒に出す"),
            ]
            region = pts("region", i)
            if st["acc"] == "on":
                n += 1
                if not _in_poly(_mid(pts("acc", i)), region):
                    bad.append(f"{tag}: 事故機の点が「起きやすい所」の外（p40＝ゆるみとレースの速さ）")
            if st["arrows"] == "on":
                for ident in ("ar_speed", "ar_stiff"):
                    n += 1
                    q = pts(ident, i)
                    if _in_poly(q[0], region) or not _in_poly(q[-1], region):
                        bad.append(f"{tag}: 矢印 {ident} が「起きにくい所 → 起きやすい所」へ向いていない（p40）")
            ons = [("region", st["region"] == "on"), ("ar_speed", st["arrows"] == "on"), ("acc", st["acc"] == "on"),
                   ("ring", st["ring"] == "on")]
        for hit, why in rules:
            n += 1
            if hit:
                bad.append(f"{tag}: {why}（{st}）")
        for ident, on in ons:
            n += 1
            if (alpha(ident, i) > 0.05) != on:
                bad.append(f"{tag}: {ident} の濃さ {alpha(ident, i)} が状態と違う")
    if view == "chart":
        # 起きやすい所の境＝速いほど高いかたさが要る（右へ行くほど上＝画面の y が小さく）＝p40
        n += 1
        edge = pts("edge", 0)
        if any(b[1] >= a[1] for a, b in zip(edge, edge[1:])):
            bad.append("起きやすい所の境が、速さとともに上がっていない（p40＝速いほど起きやすい）")
    bad += _numbers(f)
    return bad, n


# 🆕 16本目 ⑤b-4：断面の図解（vsec）の記録＝門番の側（§5b-88＝型の定数〈vsec16・illu〉を読まない）
# 🔴 2026-10-04（18本目 スレッシャー号 ⑤b-1・§0b）：16本目の値（ダムの断面・上から見た弓・湖の水位・調べた土の厚さ・試し掘りと横穴）は
#    selftest の見本 `tools/fixture_ep16.py`（GATES["check_mech"]・値は1つも変えていない＝git の `b044b56`）へ移した＝空。
#    selftest は見本の表だけ差し込む（`fixture_ep16.apply(gate, tables_only=True)`）。18本目で断面の図解（vsec）の型を使うときは、
#    その回の記録の値をここに別に持つ（§5b-88）。空のあいだ、断面の図解は止まる（fail closed）
REC_VSEC = {}
NUM_VSEC = re.compile(r"[0-9０-９][0-9０-９,.．]*(?:\s*〜\s*[0-9０-９][0-9０-９,.．]*)?\s*(?:m|メートル|本|分の1)")


def judge_vsec(f):
    """16本目 断面の図解：①状態の筋 ②形（f.mech["geo"] の画素を写しの目盛りで読む）③札の数（rel）。"""
    bad, n = [], 0
    m = f.mech
    g = m["geo"]
    mp = g["map"]
    k = mp["k"]

    def z(y):
        return mp["z0"] - (y - mp["y0"]) / k
    view = m["view"]
    seq = [m["start"]] + list(m["states"])
    # ① 筋：すべり面が出る前に「また動き出す」矢印を出さない・塊の無いすべり面を出さない・目印が動く前に向きを出さない
    for s in seq:
        n += 1
        if view == "two" and ((s["move"] == "on" and s["slip"] != "on") or (s["slip"] == "on" and s["block"] != "on")):
            bad.append(f"① 筋：2人の見立ては 塊 → すべり面 → 動き出す の順（{s}）")
        if view == "marks" and s["dir"] == "on" and s["marks"] != "moved":
            bad.append(f"① 筋：目印のずれ（moved）より前に動く向きを出した（{s}）")
    # ② 形
    if view == "arch":
        # 🆕 ⑤b-6a：上から見た弓（画素を上から見た図の写しの縮尺で m に戻す）＝弦・弓の長さ・頂きの厚さ
        A = REC_VSEC["arch"]
        kp = g["plan"]["k"]
        arc = g["arc"]
        chord = math.dist(arc[0], arc[-1]) / kp
        length = sum(math.dist(a, b) for a, b in zip(arc, arc[1:])) / kp
        th = math.dist(*g["apex"]) / kp
        n += 3
        if abs(chord - A["chord"]) > 0.5:
            bad.append(f"② 上から見た弓の弦 {chord:.2f}m（記録 {A['chord']}m＝{A['src']}）")
        if abs(length - A["length"]) > 0.6:
            bad.append(f"② 上から見た弓の長さ {length:.2f}m（記録 天端の長さ {A['length']}m＝{A['src']}）")
        if abs(th - A["top"]) > 0.3:
            bad.append(f"② 上から見た弓の厚さ {th:.2f}m（記録 上の厚さ {A['top']}m＝{A['src']}）")
    if view in ("dam", "arch") and "dam" in g:
        # ダムの断面（c211 と、c209 の右の小さな断面＝同じ形）
        R = REC_VSEC["dam"]
        d = g["dam"]
        ymin, ymax = min(p[1] for p in d), max(p[1] for p in d)
        n += 3
        if abs(z(ymin) - R["crest"]) > 0.6 or abs((ymax - ymin) / k - R["height"]) > 0.6:
            bad.append(f"② ダムの天端 {z(ymin):.1f}m・高さ {(ymax - ymin) / k:.1f}m（記録 {R['crest']}m・{R['height']}m＝{R['src']}）")
        wb = (max(p[0] for p in d if abs(p[1] - ymax) < 0.5) - min(p[0] for p in d if abs(p[1] - ymax) < 0.5)) / k
        wt = (max(p[0] for p in d if abs(p[1] - ymin) < 0.5) - min(p[0] for p in d if abs(p[1] - ymin) < 0.5)) / k
        if abs(wb - R["base"]) > 0.6 or abs(wt - R["top"]) > 0.3:
            bad.append(f"② ダムの厚さ 底{wb:.2f}m・上{wt:.2f}m（記録 底{R['base']}m・上{R['top']}m＝{R['src']}）")
        if abs(z(g["lake_y"]) - R["lake"]) > 0.5:
            bad.append(f"② ダムの断面の湖 {z(g['lake_y']):.1f}m（記録 最も高い水位 {R['lake']}m＝{R['src']}）")
    elif view not in ("dam", "arch"):
        n += 1
        want = REC_VSEC["lake"][view]
        if abs(z(g["lake_y"]) - want) > 0.5:
            bad.append(f"② 湖の水位 {z(g['lake_y']):.1f}m（記録 {want}m）")
    if "cover" in g:
        c = g["cover"]
        h = len(c) // 2
        th = [(b[1] - a[1]) / k for a, b in zip(c[:h], reversed(c[h:]))]
        lo, hi, rec = REC_VSEC["cover"]
        n += 1
        if min(th) < lo - 0.3 or max(th) > hi + 0.3:
            bad.append(f"② 調べた線の上の土の厚さ {min(th):.1f}〜{max(th):.1f}m（記録 {lo:g}〜{hi:g}m＝{rec}）")
    for key in ("borings", "tunnels"):
        if key in g:
            n += 1
            want, rec = REC_VSEC[key]
            if len(g[key]) != want:
                bad.append(f"② {key} の数 {len(g[key])}（記録 {want}＝{rec}）")
    # ③ 札の数（m・本・分の1）＝rel の宣言
    said = [r.get("t", "") for r in m["rel"]]
    for t in m["tags"]:
        for mm in NUM_VSEC.finditer(t):
            n += 1
            if not any(mm.group(0) in s for s in said):
                bad.append(f"③ 札「{t}」の数「{mm.group(0)}」が rel（記録の値の宣言）に無い")
    for r in m["rel"]:
        if not r.get("src"):
            bad.append(f"③ rel「{r.get('t')}」に出どころ（src）が無い")
    return bad, n


def _selftest_vsec(ok):
    """16本目 ⑤b-4：断面の図解の検算（正しい7つ・陽性対照＝型の定数を壊す形）。"""
    import vsec16 as V
    import illu as IL
    N = "模式"
    good_cases = [
        ("dam", dict(steps=[dict(state=dict(base="on"), tag=dict(t="約22m", at="base")),
                            dict(state=dict(top="on"), tag=dict(t="3.4m", at="top")), dict(state=dict(force="on"))],
                     rel=[dict(t="約22m", src="S9 p2006"), dict(t="3.4m", src="S9 p2006")], note=N)),
        ("marks", dict(steps=[dict(state=dict(marks="on")), dict(state=dict(marks="moved")), dict(state=dict(dir="on"))], note=N)),
        ("two", dict(steps=[dict(state=dict(block="on")), dict(), dict(state=dict(slip="on", move="on"))], note=N)),
        ("pair", dict(steps=[dict(), dict(state=dict(right="on")), dict()], note=N)),
        ("probe", dict(steps=[dict(state=dict(survey="on"), tag=dict(t="土10〜20m", at="t1")),
                              dict(state=dict(holes="on"), tag=dict(t="試し掘り3本・横穴2本", at="t2"))],
                       rel=[dict(t="10〜20m", src="S1 p74"), dict(t="3本・横穴2本", src="S1 p148")], note=N)),
        ("model", dict(steps=[dict(state=dict(copy="on")), dict(state=dict(scale="on"), tag=dict(t="200分の1", at="scale"))],
                       rel=[dict(t="200分の1", src="S1 p89")], note=N)),
        ("seep", dict(steps=[dict(state=dict(inner="on", push="on"), tag=dict(t="702.5m", at="r1"))],
                      rel=[dict(t="702.5m", src="S1 p96")], note=N)),
        # 🆕 ⑤b-6a：c209（上から見た弓 → 横から切った断面）
        ("arch", dict(steps=[dict(state=dict(force="on"), tag=dict(t="上から見ると", at="plan")),
                             dict(state=dict(sec="on"), tag=dict(t="横から切ると", at="sec"))], note=N)),
    ]
    for view, kw in good_cases:
        bad, _ = judge("vsec", dict(view=view, **kw))
        ok &= not bad
        print(f"  {'OK' if not bad else '🔴 NG'} 16本目 正しい断面の図解（{view}）: {'合格' if not bad else '不合格'}"
              + (f"  ← {bad[0]}" if bad else ""))
    probe = dict(view="probe", steps=[dict(state=dict(survey="on")), dict(state=dict(holes="on"))], note=N)
    for name, mod_, attr, val, kw, key in (
            ("ダムの底の厚さを 30m で描く型（illu.VC_DAM）", IL, "VC_DAM", dict(IL.VC_DAM, base=30.0), dict(good_cases[0][1], view="dam"),
             "ダムの厚さ"),
            ("ダムの断面の湖を 740m まで描く型（DAM_LAKE）", V, "DAM_LAKE", 740.0, dict(good_cases[0][1], view="dam"), "ダムの断面の湖"),
            ("調べた線の上の土を 30m で描く型（COVER）", V, "COVER", 30.0, probe, "土の厚さ"),
            ("試し掘りを4本描く型（BORINGS）", V, "BORINGS", (300.0, 420.0, 760.0, 1050.0), probe, "borings の数"),
            ("10月8日の水位を 710m で描く型（LAKE）", V, "LAKE", dict(V.LAKE, seep=710.0), dict(good_cases[6][1], view="seep"),
             "湖の水位"),
            # 🆕 ⑤b-6a：上から見た弓の型の値を壊す（弦・長さ・厚さ）・右の断面のダムを c211 と違う厚さで描く
            ("上から見た弓の弦を 180m で描く型（ARCH）", V, "ARCH", dict(V.ARCH, chord=180.0), dict(good_cases[7][1], view="arch"),
             "弓の弦"),
            ("上から見た弓の長さを 200m で描く型（ARCH）", V, "ARCH", dict(V.ARCH, length=200.0),
             dict(good_cases[7][1], view="arch"), "弓の長さ"),
            ("上から見た弓の厚さを 6m で描く型（ARCH）", V, "ARCH", dict(V.ARCH, top=6.0), dict(good_cases[7][1], view="arch"),
             "弓の厚さ"),
            ("c209 の右の断面のダムの底を 30m で描く型（illu.VC_DAM）", IL, "VC_DAM", dict(IL.VC_DAM, base=30.0),
             dict(good_cases[7][1], view="arch"), "ダムの厚さ")):
        keep = getattr(mod_, attr)
        setattr(mod_, attr, val)
        try:
            bad, _ = judge("vsec", kw)
        finally:
            setattr(mod_, attr, keep)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 16本目 陽性対照（型）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    for name, kw, key in (
            ("札「約25m」が rel に無い", dict(view="dam", steps=[dict(state=dict(base="on"), tag=dict(t="約25m", at="base"))], note=N),
             "rel"),
            ("すべり面より先に「動き出す」矢印", dict(view="two", steps=[dict(state=dict(block="on", move="on"))], note=N), "筋"),
            ("目印が動く前に向き", dict(view="marks", steps=[dict(state=dict(marks="on", dir="on"))], note=N), "筋")):
        bad, _ = judge("vsec", kw)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 16本目 陽性対照：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    try:
        V.vsec("marks", [dict(state=dict(marks="moved")), dict(state=dict(marks="on"))], note=N)
        g_ = False
    except ValueError:
        g_ = True
    ok &= g_
    print(f"  {'OK' if g_ else '🔴 NG'} 16本目 型の見張り：動いた目印を戻す: {'組めない（止まった）' if g_ else '🔴 組めた'}")
    return ok


# ══════════════════════════════════════════════════════════
#  🆕 16本目 ⑤b-5（2026-10-01）：水位と斜面の速さの線（lv＝`tools/lv16.py`）
# ══════════════════════════════════════════════════════════
# 🔴 記録＝門番の側（§5b-88＝型〈lv16〉も ss の点の表〈LVP〉も読まない）。原文 ref/ep16/src/ep16_pages.txt で当てた
#    （S1＝議会の調査委員会の最終報告 PDF の頁 p1〜p248・S8＝学術の総説の冊子の頁 p1041〜・S9＝財団の年表 PDF p2001〜）。
#    行＝((日付の窓の頭, 尻), (値の下限, 上限), {頁})。月だけの記録（「nel marzo 1960」）は窓をその月まるごと・
#    「primi di ottobre」＝1〜10日・「metà」＝11〜20日・「fine」＝21〜末日。値の「circa」は書いた値のまま（幅は丸めの外に広げない）
#    🔴 §0b（題材を替えるとき空にする場所）：次の回は見本 fixture へ移して空にする（16本目の型＝lv16 を使う回だけの表）
#    🔴 2026-10-04（18本目 スレッシャー号 ⑤b-1・§0b）：16本目の値（湖の水位・斜面の速さの記録の表 REC_LV／横の線 REC_LV_REF／縦の線と帯の日
#       REC_LV_DATE／線を切ってよい区間 REC_LV_BRK）は selftest の見本 `tools/fixture_ep16.py`（GATES["check_mech"]・値は1つも
#       変えていない＝git の `b044b56`）へ移した＝空。selftest は見本の表だけ差し込む（`fixture_ep16.apply(gate, tables_only=True)`）。
#       18本目で線の図（lv）の型を使うときは、その回の記録の値をここに別に持つ（§5b-88）。空のあいだ、線の図は止まる（fail closed）
#       ⚠️ 記録の表の読み方（行＝((日付の窓の頭, 尻), (値の下限, 上限), {頁})・月だけの記録は窓をその月まるごと・「primi」＝1〜10日・
#          「metà」＝11〜20日・「fine」＝21〜末日・「circa」は書いた値のまま）は移した注の側にある＝fixture_ep16 の GATES["check_mech"]
REC_LV = dict(z=[], v=[])     # 湖の水位（z）・斜面の速さ（v）の段ごとの行＝空でも段の名は持つ（KeyError でなく「記録の表に無い」と止める）
REC_LV_REF = []       # 横の線＝(段, 下限, 上限, 引き始めてよい日〈None＝軸の端から〉, {頁})
REC_LV_DATE = []      # 縦の線（ev）と帯（band）の日＝(窓, {頁})
REC_LV_BRK = []       # 線を切ってよい区間＝(段, 頭の窓, 尻の窓, {頁})＝数の記録が無い区間だけ
NUM_LV = re.compile(r"[0-9０-９][0-9０-９,.．]*\s*(?:m|メートル|ミリ|センチ)")


def _lv_yr(d):
    """門番の日付の読み方（型〈axis.val〉とは別に書く＝§5b-93）：日付 → 年（小数・その年の日数で割る）。"""
    import datetime
    j = datetime.date(d.year, 1, 1)
    return d.year + (d - j).days / (datetime.date(d.year + 1, 1, 1) - j).days


def _lv_date(s):
    """"1960"／"1963-03"／"1960-11-04" → その期間の頭（年・小数）。"""
    import datetime
    p = [int(x) for x in str(s).split("-")]
    return _lv_yr(datetime.date(p[0], p[1] if len(p) > 1 else 1, p[2] if len(p) > 2 else 1))


def _lv_win(a, b):
    """日付の窓（両端の日を含む）→ 年の範囲。"""
    import datetime
    da = datetime.date(*[int(x) for x in a.split("-")])
    db = datetime.date(*[int(x) for x in b.split("-")]) + datetime.timedelta(days=1)
    return _lv_yr(da), _lv_yr(db)


def _lv_fit(pairs):
    """[(値, 画素)] → (傾き, 切片)＝画素 = 傾き×値 + 切片（最小二乗）。"""
    k = len(pairs)
    mv = sum(v for v, _ in pairs) / k
    mx = sum(x for _, x in pairs) / k
    sxx = sum((v - mv) ** 2 for v, _ in pairs)
    p = sum((v - mv) * (x - mx) for v, x in pairs) / sxx
    return p, mx - p * mv


def _lv_recs(r):
    return set(r if isinstance(r, (list, tuple)) else [r])


def judge_lv(f):
    """16本目 水位と斜面の速さの線：①目盛り ②点（画素→日付と値→記録の表）③線（隣どうしだけ・切ってよい区間）④横の線
    ⑤縦の線と帯 ⑥寸法の線と囲み ⑦札の日付と数（rel）。"""
    bad, n = [], 0
    m = f.mech
    day = 1.0 / 365.25
    xt = m["xt"]
    if len(xt) < 2:
        return ["① 横の目盛りが2本未満（画素から日付へ戻せない）"], 1
    px_, qx = _lv_fit([(_lv_date(t["at"]), t["x"]) for t in xt])
    for t in xt:
        n += 2
        if abs(px_ * _lv_date(t["at"]) + qx - t["x"]) > 1.0:
            bad.append(f"① 横の目盛り {t['at']} が一直線に並ばない（{t['x']}）")
        p = str(t["at"]).split("-")
        want = f"{p[0]}年" if len(p) == 1 else f"{int(p[1])}月"
        if t["lab"] != want:
            bad.append(f"① 目盛り {t['at']} の字が「{t['lab']}」（{want} のはず）")
    fy = {}
    for s, ys in m["yt"].items():
        n += 1
        if len(ys) < 2:
            bad.append(f"① 縦の目盛り（{s}）が2本未満")
            continue
        fy[s] = _lv_fit([(t["v"], t["y"]) for t in ys])
        for t in ys:
            if abs(fy[s][0] * t["v"] + fy[s][1] - t["y"]) > 1.0:
                bad.append(f"① 縦の目盛り（{s}）{t['v']} が一直線に並ばない")

    def bx(x):
        return (x - qx) / px_

    def by(s, y):
        return (y - fy[s][1]) / fy[s][0]

    def ymd(yr):
        import datetime
        y = int(yr)
        d0 = datetime.date(y, 1, 1)
        return (d0 + datetime.timedelta(days=(yr - y) * (datetime.date(y + 1, 1, 1) - d0).days)).isoformat()

    def hit_date(rows, yr):
        return [r for r in rows if _lv_win(*r[0])[0] - 0.6 * day <= yr <= _lv_win(*r[0])[1] + 0.6 * day]

    # ② 点
    pts = m["pts"]
    for p in pts:
        n += 2
        if p["s"] not in fy:
            bad.append(f"② 点 {p['s']} {p['at']} の段に縦の目盛りが無い")
            continue
        yr, val = bx(p["x"]), by(p["s"], p["y"])
        rows = [r for r in hit_date(REC_LV[p["s"]], yr) if r[1][0] - 0.3 <= val <= r[1][1] + 0.3]
        if not rows:
            bad.append(f"② 点 {p['s']} {p['at']}（画素から {ymd(yr)}・{val:.2f}）が記録の表 REC_LV に無い")
        elif not any(_lv_recs(p["rec"]) & r[2] for r in rows):
            bad.append(f"② 点 {p['s']} {p['at']} の rec {sorted(_lv_recs(p['rec']))} が記録の頁 {sorted(rows[0][2])} と合わない")
    # ③ 線＝同じ段の点を日付の順に隣どうしだけ（飛ばさない・延ばさない）。切ってよいのは REC_LV_BRK の区間だけ
    for s in ("z", "v"):
        ps = sorted([p for p in pts if p["s"] == s], key=lambda p: p["x"])
        pairs = [(a["at"], b["at"]) for a, b in zip(ps, ps[1:])]
        sg = {(g["a"], g["b"]): g for g in m["segs"] if g["s"] == s}
        brk = {(b["a"], b["b"]) for b in m["brks"] if b["s"] == s}
        at_px = {p["at"]: p for p in ps}
        for a, b in pairs:
            n += 1
            if (a, b) in brk:
                ok_ = any(r[0] == s and _lv_win(*r[1])[0] <= _lv_date(a) < _lv_win(*r[1])[1]
                          and _lv_win(*r[2])[0] <= _lv_date(b) < _lv_win(*r[2])[1] for r in REC_LV_BRK)
                if not ok_:
                    bad.append(f"③ 線を切った区間 {s} {a}〜{b} が記録の表 REC_LV_BRK に無い（数の記録が無い区間だけ切ってよい）")
                if (a, b) in sg:
                    bad.append(f"③ 切った区間 {s} {a}〜{b} に線がある")
            elif (a, b) not in sg:
                bad.append(f"③ 隣どうしの点 {s} {a}〜{b} が結ばれていない")
        for (a, b), g in sg.items():
            n += 1
            if (a, b) not in pairs:
                bad.append(f"③ 線 {s} {a}〜{b} が隣どうしの点を結んでいない（飛ばした・延ばした）")
                continue
            pa, pb = at_px[a], at_px[b]
            if max(abs(pa["x"] - g["xa"]), abs(pa["y"] - g["ya"]), abs(pb["x"] - g["xb"]), abs(pb["y"] - g["yb"])) > 0.6:
                bad.append(f"③ 線 {s} {a}〜{b} の端が点の画素と違う（延ばした線）")
    # ④ 横の線
    for r in m["refs"]:
        n += 2
        if r["s"] not in fy:
            continue
        val = by(r["s"], r["y"])
        rows = [q for q in REC_LV_REF if q[0] == r["s"] and q[1] - 0.3 <= val <= q[2] + 0.3]
        if not rows:
            bad.append(f"④ 横の線 {val:.2f}（{r['s']}）が記録の表 REC_LV_REF に無い")
            continue
        if not any(_lv_recs(r["rec"]) & q[4] for q in rows):
            bad.append(f"④ 横の線 {val:.2f} の rec {sorted(_lv_recs(r['rec']))} が記録の頁と合わない")
        q = rows[0]
        if q[3] and r["xa"] < px_ * _lv_date(q[3]) + qx - 0.6:
            bad.append(f"④ 横の線 {val:g}（{r['s']}）が記録の日 {q[3]} より前から引いてある（x={r['xa']}）")
    # ⑤ 縦の線と帯の日
    for e in m["evs"]:
        n += 1
        rows = hit_date(REC_LV_DATE, bx(e["x"]))
        if not rows or not any(_lv_recs(e["rec"]) & r[1] for r in rows):
            bad.append(f"⑤ 縦の線 {e['at']}（画素から {ymd(bx(e['x']))}）が記録の表 REC_LV_DATE（頁）に無い")
    for bd in m["bands"]:
        for key in ("xa", "xb"):
            n += 1
            rows = hit_date(REC_LV_DATE, bx(bd[key])) + [(r[0], r[2]) for s in ("z", "v") for r in hit_date(REC_LV[s], bx(bd[key]))]
            if not any(_lv_recs(bd["rec"]) & r[1] for r in rows):
                bad.append(f"⑤ 帯 {bd['a']}〜{bd['b']} の端（{ymd(bx(bd[key]))}）が記録の日（頁）に無い")
    # ⑥ 寸法の線（両端が記録の値）と囲み（描いた点）
    vals = {s: [(r[1], r[2]) for r in REC_LV[s]] + [((q[1], q[2]), q[4]) for q in REC_LV_REF if q[0] == s] for s in ("z", "v")}
    for gp in m["gaps"]:
        for key in ("ya", "yb"):
            n += 1
            val = by(gp["s"], gp[key])
            if not any(lo - 0.3 <= val <= hi + 0.3 and _lv_recs(gp["rec"]) & rr for (lo, hi), rr in vals[gp["s"]]):
                bad.append(f"⑥ 寸法の線の端 {val:.2f}（{gp['s']}）が記録の値（頁）に無い")
    for rg in m["rings"]:
        n += 1
        if not any(p["s"] == rg["s"] and p["at"] == rg["at"] and abs(p["x"] - rg["x"]) < 0.6 and abs(p["y"] - rg["y"]) < 0.6
                   for p in pts):
            bad.append(f"⑥ 囲み {rg['s']} {rg['at']} が描いた点に無い")
    # ⑦ 札の日付（点・縦の線・囲みの日と合う）と数（rel）
    said = [r.get("t", "") for r in m["rel"]]
    for tx in m["texts"]:
        t = tx["t"]
        if tx.get("at"):
            p = [int(x) for x in str(tx["at"]).split("-")]
            # 日は「10月8日」の形だけ日付と読む（「1日1m」＝1日あたり1m を日付と読まない）
            for rx, i in ((r"(\d{4})年", 0), (r"(\d{1,2})月", 1), (r"(?<=月)(\d{1,2})日", 2)):
                for mm in re.finditer(rx, t):
                    n += 1
                    if len(p) <= i or int(mm.group(1)) != p[i]:
                        bad.append(f"⑦ 札「{t}」の日付「{mm.group(0)}」が {tx['at']} と合わない")
        for mm in NUM_LV.finditer(t):
            n += 1
            if not any(mm.group(0) in s for s in said):
                bad.append(f"⑦ 札「{t}」の数「{mm.group(0)}」が rel（記録の値の宣言）に無い")
    for r in m["rel"]:
        if not r.get("src"):
            bad.append(f"⑦ rel「{r.get('t')}」に出どころ（src）が無い")
    n += 1
    if "模式" not in m["note"]:
        bad.append("⑦ note に「模式」が無い（点と点のあいだは直線でつないだ模式）")
    return bad, n


def _selftest_lv(ok):
    """16本目 ⑤b-5：水位と斜面の速さの線の検算（正しい2つ・陽性対照＝記録・頁・札・rel・切る区間＋型を壊す3つ）。"""
    import axis as AX
    import lv16 as L
    N = "点＝記録の値・あいだは直線でつないだ模式"

    def P(s, at, v, rec, **kw):
        return dict(k="pt", s=s, at=at, v=v, rec=rec, **kw)
    allv = dict(span=("1960-01-01", "1963-11-01"), ticks=("1960", "1961", "1962", "1963"), zr=(560, 740),
                zt=(600, 650, 700), vr=(0, 50), vt=(0, 10, 20, 30, 40, 50), src="s", note=N)
    good = dict(allv, steps=[dict(add=[P("z", "1960-03-15", 580, "S1 p72", t="1960年3月"), P("v", "1960-03-15", 0, "S1 p72"),
                                       dict(k="ref", s="z", v=725.5, t="天端725.5m", rec="S9 p2006", c="LINE"),
                                       dict(k="gap", s="z", at="1960-03-15", a=580, b=725.5, rec=["S1 p72", "S9 p2006"], dx=-30)]),
                             dict(add=[P("z", "1960-11-04", 650, "S1 p72"), P("v", "1960-11-04", 40, "S1 p73"),
                                       dict(k="ev", at="1960-11-04", t="崩落", rec="S1 p72", c="ALERT")]),
                             dict(add=[P("z", "1961-01-08", 600, "S8 p1046"), P("v", "1961-01-08", 0, "S1 p85"),
                                       dict(k="ring", s="v", at="1961-01-08"),
                                       dict(k="ref", s="z", v=700, t="700m（模型）", rec="S1 p89")])],
                rel=[dict(t="天端725.5m", src="S9 p2006"), dict(t="700m（模型）", src="S1 p89")])
    y63 = dict(span=("1963-03-01", "1963-10-20"),
               ticks=("1963-03", "1963-04", "1963-05", "1963-06", "1963-07", "1963-08", "1963-09", "1963-10"),
               zr=(640, 730), zt=(650, 700), vr=(0, 50), vt=(0, 25, 50), src="s", note=N)
    good63 = dict(y63, past=[P("z", "1963-03-15", 650, "S1 p93"), P("v", "1963-03-15", 0, "S1 p93")],
                  steps=[dict(add=[P("z", "1963-04-10", 647.5, "S1 p226"), P("v", "1963-09-02", 6.5, "S9 p2014"),
                                   dict(k="brk", s="v", a="1963-03-15", b="1963-09-02", rec="S1 p93"),
                                   dict(k="ref", s="z", v=715, a="1963-05-04", t="715mの許可", rec="S1 p92", c="INST"),
                                   dict(k="band", s="v", a="1963-05-01", b="1963-08-31", t="大きな速まりなし", rec="S1 p93")])],
                  rel=[dict(t="715m", src="S1 p92")])

    def add(kw, j, *its):
        st = [dict(s) for s in kw["steps"]]
        st[j] = dict(st[j], add=list(F._many(st[j].get("add"))) + list(its))
        return dict(kw, steps=st)
    cases = [("正しい線の図（1960年の水ためと崩落・700m・天端）", good, True),
             ("正しい線の図（1963年・715m の許可は5月4日から・速さは3月〜9月2日を切る）", good63, True),
             ("🔴 陽性対照：記録に無い速さ（1962年12月を30ミリ）", add(good, 2, P("v", "1962-12-15", 30, "S8 p1046")), False),
             ("🔴 陽性対照：頁が違う（580m を S1 p91）",
              dict(good, steps=[dict(add=P("z", "1960-03-15", 580, "S1 p91"))]), False),
             ("🔴 陽性対照：札の日付が点と違う（1960年3月の点に「1960年4月」）",
              dict(good, steps=[dict(add=P("z", "1960-03-15", 580, "S1 p72", t="1960年4月"))]), False),
             ("🔴 陽性対照：札の数が rel に無い（700m（模型））", dict(good, rel=[dict(t="天端725.5m", src="S9 p2006")]), False),
             ("🔴 陽性対照：数の記録がある区間で線を切る（1960年11月4日〜1961年1月）",
              add(good, 2, dict(k="brk", s="z", a="1960-11-04", b="1961-01-08", rec="S1 p72")), False)]
    for name, kw, want in cases:
        bad, _ = judge("lv", kw)
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} 16本目 {name}: {'合格' if got else '不合格'}（{'合格' if want else '不合格'}のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    # 型を壊す陽性対照（§5b-88）：①日まである日付だけ20日ずらして描く型（目盛りは年・月＝ずれない）②最後の点の先へ線を延ばす型
    #   ③715m の許可を左の端から引く型
    keep_val, keep_segs, keep_ref = AX.val, L._segs_of, L._ref_span
    # ⚠️ 軸の端（"1960-01-01"）までずらすと型が先に止まる（範囲の外）＝門番の検算にならない → 月の1日は外す（点の日だけずらす）
    AX.val = lambda view, s: ((keep_val(view, s)[0] + (20 / 365.25 if view == "date" and str(s).count("-") == 2
                                                        and not str(s).endswith("-01") else 0.0)), keep_val(view, s)[1])

    def ext(pts_, brks_):
        out = keep_segs(pts_, brks_)
        for s, lst in pts_.items():
            if lst:
                j, last = lst[-1]
                out.append(dict(s=s, a=last["at"], b="1963-10-31", stage=j, pa=last, pb=dict(last, at="1963-10-31")))
        return out
    for name, patch, kw, key in (("日まである日付を20日ずらして描く型（axis.val）", ("val",), good, "記録の表"),
                                 ("最後の点の先へ線を延ばす型（lv16._segs_of）", ("segs",), good, "隣どうし"),
                                 ("715m の許可を左の端から引く型（lv16._ref_span）", ("ref",), good63, "より前")):
        if "val" not in patch:
            AX.val = keep_val
        if "segs" in patch:
            L._segs_of = ext
        if "ref" in patch:
            L._ref_span = lambda V, it: (L.X0, L.X1)
        try:
            bad, _ = judge("lv", kw)
        except ValueError as e:
            bad = [f"型が止まった：{e}"]
        finally:
            AX.val, L._segs_of, L._ref_span = keep_val, keep_segs, keep_ref
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 16本目 陽性対照（型）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    return ok


# ══════════════════════════════════════════════════════════
#  🆕 18本目 ⑤b-4（2026-10-04）：仕組みの模式図（m18＝`tools/mech18.py`）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-06（19本目 ⑤b-1・§0b）：18本目の記録（合格の割合・面の数・ボンベの数・円すい・時刻・札に出さない語）は selftest の見本
#    `tools/fixture_ep18.py`（GATES["check_mech"]・値は1つも変えていない＝git の `2d627a2`）へ移した＝空。selftest は見本の表だけ差し込む
#    （`fixture_ep18.apply(gate, tables_only=True)`）。19本目で仕組みの模式図 mech18 の型を使うときは、その回の記録の値をここに別に持つ（§5b-88）
REC_M18 = dict(lands=(0, "記録の表が空（REC_M18）"), avg=(0.0, "記録の表が空（REC_M18）"), land=(0.0, "記録の表が空（REC_M18）"),
                banks=(0, "記録の表が空（REC_M18）"), cone=(0.0, "記録の表が空（REC_M18）"), clock={}, pct={}, ng={})    # 空でも鍵は持つ（KeyError でなく「記録の表が空」と止める）
NUM_M18 = re.compile(r"[0-9０-９]{1,2}[:：][0-9０-９]{2}|[0-9０-９][0-9０-９,.．]*\s*(?:%|％|m|メートル|フィート|トン|ポンド|秒|分|本|個|"
                     r"年|月|倍|キロ)?")


def _seg_dist(p, a, b):
    ax_, ay = a
    bx, by = b
    dx, dy = bx - ax_, by - ay
    L2 = dx * dx + dy * dy or 1.0
    t = max(0.0, min(1.0, ((p[0] - ax_) * dx + (p[1] - ay) * dy) / L2))
    return math.hypot(p[0] - (ax_ + t * dx), p[1] - (ay + t * dy))


def _box(pts):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def _conical(cone):
    """円すい形か（先の高さ÷底の高さ）＝cone_pts の4点（底の上・先の上・先の下・底の下）。"""
    (_bx, y0), (_ax, ya), (_ax2, yb), (_bx2, y1) = cone
    base = abs(y1 - y0) or 1.0
    return abs(yb - ya) / base


def judge_m18(f):
    """18本目 仕組みの模式図：①状態の筋 ②形（f.mech["geo"] の画素）を記録（REC_M18）で ③札の数・時刻・語りに無い語。"""
    bad, n = [], 0
    m = f.mech
    g = m["geo"]
    view = m["view"]
    seq = [m["start"]] + list(m["states"])
    steps = m["steps"]

    def tags_upto(i):                     # 段 i（0＝頭・i≥1＝steps[i-1]）までに出た札
        out = []
        for st in steps[:i]:
            out += [t.get("t", "") + t.get("d", "") for t in F._many(st.get("tag"))]
        return out
    # ① 筋
    for i, s in enumerate(seq):
        n += 1
        if view == "loop":
            if s["reactor"] == "scram" and s["pump"] != "stop":
                bad.append(f"① 筋：原子炉が自動で止まるのはポンプが止まった場合だけ（意見45）＝{s}")
            if s["pump"] == "stop" and not any("仮定" in t for t in tags_upto(max(i, 1))):
                bad.append("① 筋：ポンプが止まった場合は査問会の仮定（意見45）＝その段までに「仮定」の札が要る")
        if view == "braze" and s["alloy"] == "flow" and s["heat"] != "on":
            bad.append("① 筋：合金は溶かしてから流れる（熱の印より先に流した）")
        if view == "ut" and s["sound"] == "on" and s["probe"] != "on":
            bad.append("① 筋：音は外から当てる道具から（道具より先に音）")
        if view == "cold" and s["ice"] == "on" and s["expand"] != "on":
            bad.append("① 筋：氷は空気が一気に広がって冷えてから（J p32・意見8c）")
        if view == "ice" and s["flow"] == "stop" and s["ice"] != "on":
            bad.append("① 筋：タンクへの空気が止まるのは網に氷がついてから（J p32 の注）")
        if view == "shock" and s["blast"] == "on" and s["sub"] != "on":
            bad.append("① 筋：爆薬より先に艦（揺れに耐えるかを試すのは艦）")
    if view == "loop" and any(s["pump"] != "fast" for s in seq):
        n += 1
        if not any(t in REC_M18["clock"] for t in m["tags"]):
            bad.append(f"① 筋：ポンプの速い回し方が止んだ時刻の札が無い（記録 {list(REC_M18['clock'])}）")
    # ② 形（記録の値で照らす）
    if view == "shock":
        n += 2
        if g["obj"]["sub"] != 1 or g["obj"]["charge"] > 1:
            bad.append(f"② 艦 {g['obj']['sub']}・爆薬の印 {g['obj']['charge']}（艦は1・爆薬の印は1つまで＝試験は何回かを note で断る）")
        hx0, hy0, hx1, hy1 = _box(g["hull"])
        cx, cy = g["charge"]
        if hx0 - 2 <= cx <= hx1 + 2 and hy0 - 2 <= cy <= hy1 + 2:
            bad.append("② 爆薬の印が艦の上にある（近くで爆発させる＝艦から離す）")
    if view == "loop":
        n += 2
        path = g["path"]
        d = min(_seg_dist(g["pump"], a, b) for a, b in zip(path, path[1:]))
        if d > 2.0:
            bad.append(f"② ポンプが熱を運ぶ水の回り道の上に無い（管から {d:.1f}画素）")
        v = g["vessel"]
        if abs(path[0][0] - v[2]) > 2.0 or abs(path[-1][0] - v[2]) > 2.0:
            bad.append("② 回り道の両端が原子炉につながっていない")
        # 🆕 ⑤b-4 の試し焼き（Actions 37185142461）：止まった印を段の層に描いたら、動く部品のポンプの円に隠れた
        #   ＝止まった場合は、印が動く部品として**ポンプより後（上）**に描かれ、その段で見えていること
        if any(s["pump"] == "stop" for s in seq):
            n += 1
            ids = [sh["id"] for sh in m["shapes"]]
            mk = next((sh for sh in m["shapes"] if sh["id"] == "stopmark"), None)
            if mk is None or "pump" not in ids or ids.index("stopmark") < ids.index("pump") \
                    or float(mk["keys"][-1].get("alpha", 0.0)) < 0.99:
                bad.append("② 止まった印がポンプの円に隠れる（印は動く部品としてポンプより後に描き、止まった段で見えること）")
    if view in ("braze", "ut", "crit"):
        want, rec = REC_M18["lands"]
        lands, gr, so = g["lands"], g["groove"], g["socket"]
        n += 2
        if len(lands) != want:
            bad.append(f"② 面の数 {len(lands)}（記録 {want}＝{rec}）")
        elif not (so[0] - 0.5 <= lands[0][0] < lands[0][1] <= gr[0] + 0.5 and gr[1] - 0.5 <= lands[1][0] < lands[1][1] <= so[1] + 0.5):
            bad.append(f"② 輪の溝が2つの面のあいだ（受け口の中）に無い（面 {lands}・溝 {gr}・受け口 {so}）")
        ylo, yhi = min(g["gap"]), max(g["gap"])
        ax = g["ax"]
        if view == "braze" and g.get("alloy"):
            cover = {}
            for pts in g["alloy"]:
                x0, y0, x1, y1 = _box(pts)
                top = y1 <= ax
                lo, hi = (ylo, yhi) if top else (2 * ax - yhi, 2 * ax - ylo)
                n += 1
                if x1 - x0 > 0.5 and (y0 < lo - 0.5 or y1 > hi + 0.5 or x0 < so[0] - 0.5 or x1 > so[1] + 0.5):
                    bad.append(f"② 合金がすき間の外（x {x0:.0f}〜{x1:.0f}・y {y0:.0f}〜{y1:.0f}／すき間 y {lo:.0f}〜{hi:.0f}）")
                for k, (a0, a1) in enumerate(lands):
                    ov = max(0.0, min(x1, a1) - max(x0, a0))
                    cover[(k, top)] = cover.get((k, top), 0.0) + ov
            if any(s["alloy"] == "flow" for s in seq):
                for k, (a0, a1) in enumerate(lands):
                    for top in (True, False):
                        n += 1
                        if cover.get((k, top), 0.0) < 0.98 * (a1 - a0):
                            bad.append(f"② 溶けた合金が{'左' if k == 0 else '右'}の面（{'上' if top else '下'}）に届いていない"
                                       f"（輪は2つの面のあいだ＝両方へ流れる）")
        if view == "ut" and "probe" in g:
            n += 1
            yb = g["probe"][3]
            if yb > g["outer"] + 0.5 or yb < g["outer"] - 3.0:
                bad.append(f"② 音を当てる道具が継手の外の面に当たっていない（下の端 y{yb:.0f}・外の面 y{g['outer']:.0f}＝外から当てる）")
        if view == "crit" and g.get("bars"):
            B = g["bars"]
            if B.get("avg"):
                x0, x1, _y, _h, fr = B["avg"]
                n += 1
                if abs(fr - REC_M18["avg"][0] / 100.0) > 0.003:
                    bad.append(f"② 平均の合格の線 {fr * 100:.1f}%（記録 {REC_M18['avg'][0]:g}%＝{REC_M18['avg'][1]}）")
            if B.get("lands") is not None and any(s["land"] == "on" for s in seq):
                n += 1
                if len(B["lands"]) != REC_M18["lands"][0]:
                    bad.append(f"② 面の棒の数 {len(B['lands'])}（記録 {REC_M18['lands'][0]}）")
                for b in B["lands"]:
                    n += 1
                    if abs(b[4] - REC_M18["land"][0] / 100.0) > 0.003:
                        bad.append(f"② 面の合格の線 {b[4] * 100:.1f}%（記録 {REC_M18['land'][0]:g}%＝{REC_M18['land'][1]}）")
    if view == "blow":
        want, rec = REC_M18["banks"]
        n += 3
        if len(g["banks"]) != want:
            bad.append(f"② 空気のボンベの数 {len(g['banks'])}（記録 {want}＝{rec}）")
        if not (max(b[2] for b in g["banks"]) < g["valve"][0] < g["valve"][2] < g["tank"][0]):
            bad.append("② 空気の通り道の順番（ボンベ → 減圧弁 → 主タンク）が違う")
        for i, s in enumerate(seq):
            if s["flow"] == "on" and not g["water"][i] > g["water"][0]:
                bad.append("② 空気を送ってもタンクの海水が下がっていない")
            if s["flow"] != "on" and abs(g["water"][i] - g["water"][0]) > 0.5:
                bad.append("② 空気を送る前にタンクの海水が下がった")
    if view in ("blow", "cold", "ice") and g.get("cone"):
        n += 1
        r = _conical(g["cone"])
        if r > REC_M18["cone"][0]:
            bad.append(f"② こし器が円すい形でない（先の高さ÷底の高さ {r:.2f}＞{REC_M18['cone'][0]}＝{REC_M18['cone'][1]}）")
    if view == "cold":
        n += 1
        if any(s != "none" for s in g["dry"]):
            bad.append("② 水分を取る装置を描いた（認定48：Dehydrators were not installed）")
        if g.get("ice"):
            x0, y0, x1, y1 = _box(g["cone"])
            for p in g["ice"]:
                n += 1
                if not (x0 - 12 <= p[0] <= x1 + 12 and y0 - 12 <= p[1] <= y1 + 12):
                    bad.append(f"② 氷がこし器の網の上に無い（{p[0]:.0f}, {p[1]:.0f}）")
                    break
    if view == "ice":
        x0, y0, x1, y1 = _box(g["cone"])
        for pts in g["ice"]:
            n += 1
            cx_, cy_ = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
            if not (x0 - 30 <= cx_ <= x1 + 30 and y0 - 30 <= cy_ <= y1 + 30):
                bad.append(f"② 氷がこし器の網の上に無い（{cx_:.0f}, {cy_:.0f}）")
        if any(s["flow"] == "stop" for s in seq):
            n += 1
            if any(a > 0.01 for a in g["down"]):
                bad.append("② 空気が止まったのに網のあとの空気の矢印が残っている")
    if view == "tinosa":
        n += 1
        top, bot, _xl, _xr = g["hull"]
        if not (top < g["water_y"] < bot):
            bad.append(f"② 岸壁の艦が水面にいない（船体 y{top:.0f}〜{bot:.0f}・水面 y{g['water_y']:.0f}＝岸壁での試験）")
    # ③ 札の数・時刻・語りに無い語
    said = [r.get("t", "") for r in m["rel"]]
    for t in m["tags"]:
        for mm in NUM_M18.finditer(t):
            tok = mm.group(0).strip()
            if not tok:
                continue
            n += 1
            if view == "shock":
                bad.append(f"③ 札「{t}」に数「{tok}」＝距離と重さは次の c207（数の比べ）の語り")
                continue
            if not any(tok in s or s in tok for s in said):
                bad.append(f"③ 札「{t}」の数「{tok}」が rel（記録の値の宣言）に無い")
            if ":" in tok or "：" in tok:
                if tok.replace("：", ":") not in REC_M18["clock"]:
                    bad.append(f"③ 札「{t}」の時刻「{tok}」が記録の時刻（{list(REC_M18['clock'])}）に無い")
            elif "%" in tok or "％" in tok:
                if tok.replace("％", "%") not in REC_M18["pct"]:
                    bad.append(f"③ 札「{t}」の割合「{tok}」が記録の割合（{list(REC_M18['pct'])}）に無い")
        for w in REC_M18["ng"].get(view, ()):
            n += 1
            if w in t:
                bad.append(f"③ 札「{t}」の「{w}」は語りに無い出来事（次のカットの語り）")
    for r in m["rel"]:
        if not r.get("src"):
            bad.append(f"③ rel「{r.get('t')}」に出どころ（src）が無い")
    return bad, n


def _selftest_m18(ok):
    """18本目 ⑤b-4：仕組みの模式図の検算（正しい10・陽性対照＝型の定数を壊す10＋筋と札10・型の見張り2）。"""
    import mech18 as M
    N = "模式"
    R911 = [dict(t="9:11", src="R08 p4185")]
    good = dict(
        shock=dict(view="shock", steps=[dict(state=dict(sub="on"), tag=dict(t="スレッシャー", at="sub")),
                                        dict(state=dict(blast="on"), tag=dict(t="爆薬", at="charge"))], note=N),
        loop=dict(view="loop", steps=[dict(state=dict(pump="quit"), tag=dict(t="9:11", at="clock")),
                                      dict(state=dict(pump="ask"), tag=dict(t="止まった？", at="q1"))], rel=R911, note=N),
        loop2=dict(view="loop", start=dict(pump="ask"),
                   steps=[dict(tag=dict(t="9:11", at="clock")),
                          dict(state=dict(pump="stop", reactor="scram"), tag=dict(t="止まった（仮定）", at="q2"))], rel=R911, note=N),
        braze=dict(view="braze", steps=[dict(), dict(state=dict(alloy="flow", heat="on"))], note=N),
        ut=dict(view="ut", steps=[dict(state=dict(probe="on")), dict(state=dict(sound="on"))], note=N),
        crit=dict(view="crit", steps=[dict(state=dict(avg="on"), tag=dict(t="40%以上", at="avg")),
                                      dict(state=dict(land="on"), tag=dict(t="25%以上", at="l1"))],
                  rel=[dict(t="40%", src="R08 p4197"), dict(t="25%", src="R08 p4197")], note=N),
        blow=dict(view="blow", steps=[dict(), dict(state=dict(flow="on")), dict(state=dict(strainer="on"))], note=N),
        cold=dict(view="cold", steps=[dict(state=dict(expand="on")), dict(state=dict(ice="on"))], note=N),
        tinosa=dict(view="tinosa", steps=[dict(), dict(state=dict(sys="on"))], note=N),
        ice=dict(view="ice", steps=[dict(state=dict(ice="on", flow="stop")), dict(), dict()], note=N),
    )
    for name, kw in good.items():
        bad, _ = judge("m18", kw)
        ok &= not bad
        print(f"  {'OK' if not bad else '🔴 NG'} 18本目 正しい仕組みの模式図（{name}）: {'合格' if not bad else '不合格'}"
              + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 型の定数を壊す（筋は正しいのに絵が記録と食い違う＝§5b-88 の陽性対照）
    for nm, attr, val, kw, key in (
            ("平均の合格の線を 45% で描く型（CRIT_AVG）", "CRIT_AVG", 0.45, good["crit"], "平均の合格の線"),
            ("面の合格の線を 30% で描く型（CRIT_LAND）", "CRIT_LAND", 0.30, good["crit"], "面の合格の線"),
            ("空気のボンベを3つで描く型（BANKS_N）", "BANKS_N", 3, good["blow"], "ボンベの数"),
            ("溶けた合金が右の面にだけ流れる型（FLOW_BOTH）", "FLOW_BOTH", False, good["braze"], "左の面"),
            ("合金の帯をすき間より太く描く型（ALLOY_PAD）", "ALLOY_PAD", 6.0, good["braze"], "すき間の外"),
            ("輪の溝を受け口の口の外に描く型（JT）", "JT", dict(M.JT, gx=1300.0), good["braze"], "輪の溝"),
            ("こし器を筒の形で描く型（CONE_APEX）", "CONE_APEX", 0.8, good["blow"], "円すい形でない"),
            ("超音波の道具を金属の中に描く型（PROBE_GAP）", "PROBE_GAP", -12.0, good["ut"], "外の面に当たっていない"),
            ("ポンプを管から外して描く型（LOOP）", "LOOP", dict(M.LOOP, pump=(1000.0, 690.0)), good["loop"], "回り道の上に無い"),
            ("岸壁の艦を水の中に沈めて描く型（TIN）", "TIN", dict(M.TIN, cy=650.0), good["tinosa"], "水面にいない")):
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            bad, _ = judge("m18", kw)
        finally:
            setattr(M, attr, keep)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 18本目 陽性対照（型）：{nm}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    for nm, kw, key in (
            ("ポンプが止まっていないのに原子炉が止まる",
             dict(view="loop", steps=[dict(state=dict(pump="quit", reactor="scram"), tag=dict(t="9:11", at="clock"))], rel=R911,
                  note=N), "筋"),
            ("止まった場合に「仮定」の札が無い",
             dict(view="loop", steps=[dict(state=dict(pump="stop"), tag=dict(t="9:11", at="clock"))], rel=R911, note=N), "仮定"),
            ("時刻の札が 9:13（記録は 9:11）",
             dict(view="loop", steps=[dict(state=dict(pump="quit"), tag=dict(t="9:13", at="clock"))],
                  rel=[dict(t="9:13", src="R08 p4185")], note=N), "記録の時刻"),
            ("7.1分の札（次の c720 の語り）",
             dict(view="loop", steps=[dict(state=dict(pump="quit"), tag=[dict(t="9:11", at="clock"), dict(t="7.1分", at="r1")])],
                  rel=R911 + [dict(t="7.1分", src="R08 p4212")], note=N), "語りに無い"),
            ("合格の札が 50%（記録は 40%）",
             dict(view="crit", steps=[dict(state=dict(avg="on"), tag=dict(t="50%以上", at="avg"))],
                  rel=[dict(t="50%", src="R08 p4197")], note=N), "記録の割合"),
            ("衝撃試験に距離の札",
             dict(view="shock", steps=[dict(state=dict(sub="on", blast="on"), tag=dict(t="約110m", at="charge"))],
                  rel=[dict(t="約110m", src="R08 p4194")], note=N), "c207"),
            ("広がる前に氷", dict(view="cold", steps=[dict(state=dict(ice="on"))], note=N), "筋"),
            ("氷の前に空気が止まる", dict(view="ice", steps=[dict(state=dict(flow="stop"))], note=N), "筋"),
            ("網が破れる札（c715 の決め所の語り）",
             dict(view="ice", steps=[dict(state=dict(ice="on", flow="stop"), tag=dict(t="網が破れる", at="stop"))], note=N),
             "語りに無い"),
            ("熱の前に合金が流れる", dict(view="braze", steps=[dict(state=dict(alloy="flow"))], note=N), "筋")):
        bad, _ = judge("m18", kw)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 18本目 陽性対照：{nm}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    # 🆕 ⑤b-4 の試し焼き：止まった印が動く部品のポンプの円に隠れる型（印を部品から外す＝段の層に描いていた前の形）
    keep = M._loop_parts
    M._loop_parts = lambda st: [p for p in keep(st) if p["id"] != "stopmark"]
    try:
        bad, _ = judge("m18", good["loop2"])
    finally:
        M._loop_parts = keep
    g_ = any("隠れる" in b for b in bad)
    ok &= g_
    print(f"  {'OK' if g_ else '🔴 NG'} 🔴 18本目 陽性対照（型）：止まった印をポンプの円の下に描く型: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    for nm, fn in (("溶けた合金を輪に戻す", lambda: M.m18("braze", [dict(state=dict(alloy="flow", heat="on")),
                                                                     dict(state=dict(alloy="ring"))], note=N)),
                   ("水分を取る装置を付ける", lambda: M.m18("cold", [dict(state=dict(dry="on"))], note=N))):
        try:
            fn()
            g_ = False
        except ValueError:
            g_ = True
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 18本目 型の見張り：{nm}: {'組めない（止まった）' if g_ else '🔴 組めた'}")
    return ok


# ══════════════════════════════════════════════════════════
#  🆕 19本目 ⑤b-4（2026-10-06）：模式図（m19＝`tools/mech19.py`・29の見え方）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-08（20本目 ⑤b-1・§0b）：19本目の記録（候補の柱・まわりの柱・継ぎ目の不足の位置・漏れの楕円・柱の動き・重ねの厚さ・鉄筋の本数と間隔・
#    強さ・札に出してよい時刻・余裕・赤い線の型・推定で描く段ほか）は selftest の見本 `tools/fixture_ep19.py`（GATES["check_mech"]・値は1つも
#    変えていない＝git の `70c7e51`）へ移した＝空。selftest は見本の表だけ差し込む（`fixture_ep19.apply(gate, tables_only=True)`）。
#    20本目で仕組みの模式図 mech19 の型を使うときは、その回の記録の値をここに別に持つ（§5b-88＝描く側の表 mech19.CAND・AROUND・CODE_DOTS・CORE・CV・RB_C・
#    JO_TIES…を書き換えると鳴る）。空のあいだ、m19 のカットは `judge_m19` が「記録の表が空」で止める（fail closed＝KeyError にしない）。
#    形の定数（`NUM_M19`＝札の数を拾う式・`_m19_order_ok`・`judge_m19` の筋の規則）は型の側＝残す
REC_M19 = {}
NUM_M19 = re.compile(r"[0-9０-９]{1,2}[:：][0-9０-９]{2}(?:[:：][0-9０-９]{2})?|[0-9０-９][0-9０-９,.．]*")


def _m19_order_ok(seq, need, have):
    """need の欄が on になる段では、have の欄がすでに on（同じ段も可）。"""
    return all(not (s.get(need[0]) == need[1]) or all(s.get(k) == v for k, v in have) for s in seq)


def judge_m19(f):
    """19本目 模式図：①状態の筋 ②形（f.mech["geo"]）を記録（REC_M19）で ③札の数・時刻・推定の札。"""
    import mech19 as M
    bad, n = [], 0
    m = f.mech
    g, view = m["geo"], m["view"]
    seq = [m["start"]] + list(m["states"])
    R = REC_M19
    if not R:       # 🆕 20本目 ⑤b-1：記録の表が空のあいだは止める（KeyError で理由が見えなくならない＝fail closed）
        return ["記録の表 REC_M19 が空（20本目の値を入れるまで、m19 のカットは止まる）"], 1
    texts = list(m["tags"])
    # ① 筋（先に起きることが先）
    rules = dict(
        punch=[(("drop", "on"), (("crack", "wide"),), "床が落ちるのは、ひびが開いて継ぎ目が強さを失ってから（TR0066）"),
               (("hook", "on"), (("drop", "on"),), "フックの形の鉄筋が残るのは、落ちきってから（TR0072）"),
               (("shear", "on"), (("drop", "on"),), "押し抜きの矢印は、床がずれたあと")],
        water=[(("slope", "on"), (("strip", "on"),), "傾けたコンクリートは、全部はがしてから（MC18 p.7）"),
               (("memb2", "on"), (("slope", "on"),), "防水を敷き直すのは、傾けたコンクリートの上"),
               (("fix", "on"), (("strip", "on"),), "床を直すのは、はがしてから")],
        edge=[(("pull", "on"), (("fall", "full"),), "継ぎ目を引きはがすのは、デッキが塔の南の面まで崩れてから（TR0330）"),
              (("joint", "hurt"), (("pull", "on"),), "継ぎ目が傷むのは、梁と床が外れてから（TR0292）"),
              (("joint", "crush"), (("pull", "on"),), "押しつぶれは、引きはがされて傷んだあと（TR0332）"),
              (("drop", "on"), (("joint", "crush"),), "上の柱が下がるのは、継ぎ目が押しつぶされてから（TR0313）")],
        joint=[(("buckle", "on"), (("bars", "on"), ("ties", "on")), "曲がる縦の鉄筋と、輪の形の鉄筋の無い高さを先に見せる"),
               (("dense", "on"), (("bars", "on"),), "詰め込みは縦の鉄筋を見せてから")],
        zoneb=[(("brk", "on"), (("mark", "on"),), "折れる所（①）と保つ所（②）の印を先に")],
        excav=[(("drive", "on"), (("pit", "on"),), "鋼の板は掘る所の壁を支えるため"),
               (("wave", "on"), (("drive", "on"),), "揺れは鋼の板を打ち込むときに出る（TR0456）"),
               (("damp", "on"), (("wave", "on"),), "弱まるのは揺れが出てから"), (("dist", "on"), (("pit", "on"),), "距離は掘った所から")],
        drip=[(("flow", "tap"), (("band", "on"),), "蛇口のような漏れ（約3時間前）は、しずく（約9時間前）の帯を見せてから")],
        cover=[(("weak", "on"), (("dwg", "on"), ("real", "on")), "強さの比べは、図面と実際の両方を見せてから")],
        rebar=[(("space", "on"), (("real", "on"),), "間隔の比べは、実際の鉄筋を見せてから")],
        ruler=[(("short", "on"), (("rul", "on"),), "足りない量は物差しを見せてから"), (("gap", "on"), (("short", "on"),), ""),
               (("limit", "on"), (("rul", "on"),), "")],
        seq=[(("around", "on"), (("first", "on"), ("second", "on")), "まわりの柱へ重さが回るのは、2か所が壊れてから（TR0140）")],
        cand=[(("red", "on"), (("cand", "on"),), "赤い枠は候補の中の2か所（TR0106）")],
        # 🆕 ⑤b-6
        margin=[(("gap", "on"), (("cap", "on"), ("load", "on")), "余裕は、耐えられる重さとふだんの重さの差（TR0470）＝2本を見せてから")],
        drop=[(("now", "on"), (("ref", "on"),), "下がりは前日のコマ（基準の床）と比べた量（TR0340・TR0345）")],
        curve=[(("cross", "on"), (("blue", "on"),), "交わる所は、かかる力の線を見せてから"),
               (("gap", "on"), (("blue", "on"),), "余裕は、かかる力の線を見せてから")],
        ground=[(("none", "on"), (("cave", "on"),), "「空洞の跡なし」は、空洞の例を見せてから")])
    for need, have, why in rules.get(view, []):
        n += 1
        if not _m19_order_ok(seq, need, have):
            bad.append(f"① 筋：{need[0]}={need[1]} の段で {dict(have)} になっていない（{why}）")
    # ② 形（記録で照らす）
    if view == "cand":
        n += 2
        if g["cand"] and set(g["cand"]) != R["cand"][0]:
            bad.append(f"② 候補の位置 {sorted(g['cand'])}（記録 {sorted(R['cand'][0])}＝{R['cand'][1]}）")
        if g["red"] and set(g["red"]) != R["first2"][0]:
            bad.append(f"② 赤い枠 {sorted(g['red'])}（記録 {sorted(R['first2'][0])}＝{R['first2'][1]}）")
    if view == "seq":
        n += 2
        if not set(g["punched"]) <= R["first2"][0]:
            bad.append(f"② 壊れた継ぎ目の印 {g['punched']}（記録 {sorted(R['first2'][0])}）")
        if g["around"] and set(g["around"]) != R["around"][0]:
            bad.append(f"② まわりの柱 {sorted(g['around'])}（記録 {sorted(R['around'][0])}＝{R['around'][1]}）")
    if view == "code" and g["red"]:
        n += 2
        if set(g["red"]) != R["code_red"][0]:
            bad.append(f"② ひどい不足の継ぎ目 {sorted(g['red'])}（記録 {sorted(R['code_red'][0])}＝{R['code_red'][1]}）")
        if set(g["yel"]) != R["code_yel"][0]:
            bad.append(f"② 中くらいの不足の継ぎ目 {sorted(g['yel'])}（記録 {sorted(R['code_yel'][0])}＝{R['code_yel'][1]}）")
    if view == "dmg":
        n += 3
        (c0, c1), (r0, r1), why = R["leak"]
        x, y = g["leak"]
        if not (M.COLX[c0] < x < M.COLX[c1] and M.ROWY[r0] < y < M.ROWY[r1]):
            bad.append(f"② 漏れの楕円が {c0} と {c1} のあいだ・{r0} と {r1} のあいだに無い（{x:.0f}, {y:.0f}＝{why}）")
        wx, wy = g["water"]
        c, r = R["water"][0].split("-")
        if abs(wx - M.COLX[c]) > 1 or abs(wy - M.ROWY[r]) > 1:
            bad.append(f"② 柱を伝う水の点が {R['water'][0]} に無い（{R['water'][1]}）")
        if abs(g["gate"][0] - M.COLX[R["gate_col"][0]]) > 1:
            bad.append(f"② 門の点が {R['gate_col'][0]} の線に無い（{R['gate_col'][1]}）")
        bx = g["planter_box"]
        px, py = g["planter"]
        n += 1
        if not (bx[0] - 2 <= px <= bx[2] + 2 and bx[1] - 2 <= py <= bx[3] + 2):
            bad.append("② プランターの点がプランターの箱の上に無い")
    if view == "sight" and g["vis"]:
        n += 2
        dx = [p[0] for p in g["deck"]]
        dy = [p[1] for p in g["deck"]]
        if any(not (min(dx) - 1 <= p[0] <= max(dx) + 1 and min(dy) - 1 <= p[1] <= max(dy) + 1) for p in g["vis"]):
            bad.append("② 見えた範囲がプールデッキの外へ出ている（TF p9069＝デッキの上だけ）")

        def area(P):
            return abs(sum(P[i][0] * P[i - 1][1] - P[i - 1][0] * P[i][1] for i in range(len(P)))) / 2.0
        fr = area(g["vis"]) / area(g["deck"])
        if not 0.70 <= fr <= 0.97:
            bad.append(f"② 見えた範囲がデッキの {fr * 100:.0f}%（TF p9069＝デッキのほとんど・北西の角は見えない＝70〜97%）")
    if view == "planter" and g["boxes"]:
        n += 2
        y0, y1 = g["band"]
        x0, x1 = g["deck_x"]
        if any(not (y0 <= b[1] and b[3] <= y1 and x0 <= b[0] and b[2] <= x1) for b in g["boxes"]):
            bad.append("② プランターの列がデッキの北の縁（塔の南の面と 11.1 のあいだ）に無い（TF p9088 の赤い点線）")
        if m["states"] and m["states"][-1]["palm"] == "gone" and any(a > 0.01 for a in g["palm_after"]):
            bad.append("② 抜いたヤシの木が残っている（TR0235＝2017年のハリケーンのあとに抜いた）")
    if view == "cam" and g["move"]:
        n += 3
        gr = R["cam_grid"][0]
        if abs(g["grid"]["L"] - gr["L"]) > 0.5 or abs(g["grid"]["M"] - gr["M"]) > 0.5:
            bad.append(f"② 平面の L・M の線が NIST の図と違う（{g['grid']}＝{R['cam_grid'][1]}）")
        if set(g["move"]) != R["cam_move"][0] or set(g["still"]) != R["cam_still"][0]:
            bad.append(f"② 下がった柱 {g['move']}・動かない柱 {g['still']}（記録 {sorted(R['cam_move'][0])}／{sorted(R['cam_still'][0])}）")
        if not (g["unit"][0] == gr["L"] and g["unit"][1] == gr["M"]):
            bad.append("② 11 の列の部屋が L と M のあいだに無い（TR0336）")
    if view == "hall":
        mv, still, why = R["hall"]
        n += 2
        if any(abs(g["dy"][c]) > 0.01 for c in still):
            bad.append(f"② 動かない所（{sorted(still)}）の床が下がっている（{why}）")
        if any(s["sag"] == "on" for s in seq) and any(g["dy"][c] <= 0 for c in mv):
            bad.append(f"② たわむ所（{sorted(mv)}）の床が下がっていない（{why}）")
    if view == "flat" and g["joints"]:
        n += 2
        if g["beams"]:
            bad.append("② フラットプレートに梁を描いた（TR0055＝床の板が柱に直に載る）")
        if g["joints"] != g["n"]:
            bad.append(f"② 継ぎ目の印 {g['joints']}／柱と床の交わり {g['n']}")
    if view == "punch":
        (tx, ty), (bx_, by_) = g["crack"]
        n += 1
        if not (abs(tx - g["col_face"]) > abs(bx_ - g["col_face"]) + 20 and ty < by_):
            bad.append("② ひびが柱のまわりの斜めのひび（上の面で柱から離れ、下の面で柱に近い）になっていない（TR0065）")
        if g["react"]:
            n += 1
            if not g["react"][0] > g["react"][1]:
                bad.append("② 柱の矢印が上を向いていない（TR0064＝柱は上へ押し返す）")
        if g["shear"]:
            n += 1
            if not g["shear"]["slab"][1] > g["shear"]["slab"][0]:
                bad.append("② 床の矢印が下を向いていない（押し抜き＝柱は上・床は下へずれる）")
    if view == "gspan":
        n += 2
        if any(abs(d) > 0.01 for r, d in g["dy"].items() if r != "13.1"):
            bad.append(f"② 下がったのが K-13.1 の柱の所だけでない（{g['dy']}＝TR0139）")
        if g["share_to"] and set(g["share_to"]) != {"15", "11.1"}:
            bad.append(f"② 重さを渡す先が隣の柱でない（{g['share_to']}）")
    if view == "core":
        want, why = R["core"]
        th = g["thick"]
        n += 1
        if th["top"]:
            got = (th["topping"], th["tile"], th["top"])
            k = got[0] / want[0]
            if any(abs(gv / (wv * k) - 1.0) > 0.03 for gv, wv in zip(got, want)):
                bad.append(f"② 重ねの厚さの比 {tuple(round(v / k, 3) for v in got)}（記録 {want}＝{why}）")
    if view == "water":
        n += 2
        if abs(g["slab_y"][0] - g["slab_y"][1]) > 0.5:
            bad.append("② 床の板が平らでない（MC18 p.7＝平らな床）")
        if g["pond_with_slope"]:
            bad.append("② 傾けたあとも水がたまっている")
    if view == "edge":
        n += 2
        if abs(g["joint_x"] - g["row91"]) > 0.5:
            bad.append("② 傷む継ぎ目が 9.1 の線の柱に無い（TR0292）")
        if not (g["beam_x"][0] < g["beam_x"][1] <= g["row91"]):
            bad.append("② 梁が 9.1 の線（塔の南の面）の南に無い（TR0288）")
    if view == "joint":
        f0, f1 = g["floor"]
        n += 1
        if any(f0 < y < f1 for y in g["ties"]):
            bad.append(f"② 床の高さ（継ぎ目）に輪の形の鉄筋を描いた（{[y for y in g['ties'] if f0 < y < f1]}＝TR0297・AC p.71）")
        if g["bar2"] is not None:
            n += 1
            want = R["strength"][0][1] / R["strength"][0][0]
            if abs(g["bar2"] - want) > 0.01:
                bad.append(f"② 床と柱の強さの棒の比 {g['bar2']:.3f}（記録 {want:.3f}＝{R['strength'][1]}）")

        def rgb(h):
            return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
        c, fl = rgb(g["colors"]["col"]), rgb(g["colors"]["floor"])
        n += 1
        if not (c[1] > c[0] + 20 and c[1] > c[2] + 20 and max(fl) - min(fl) < 20):
            bad.append("② 柱は緑・床は灰色（NIST の図＝TF p9112）になっていない")
    if view == "front" and g["heads_shown"]:
        n += 1
        if not g["head_top"] < g["roof_top"] - 10:
            bad.append("② 柱の頭が屋根より上に突き出していない（TR0366）")
    if view == "zoneb":
        n += 2
        if not (g["topbar_end"] - 5 <= g["brk"] <= g["topbar_end"] + 80 and g["brk"] > g["E"]):
            bad.append(f"② 折れる所（①）が E の柱の東・上の鉄筋の途切れる辺りに無い（{g['brk']:.0f}・鉄筋の端 {g['topbar_end']:.0f}＝TR0384・TF p9144）")
        if any(abs(r) > 0.01 for r in g["rot"]) and abs(g["pivot_x"] - g["brk"]) > 0.5:
            bad.append("② 傾く床が ① で折れていない")
    if view == "excav":
        a = g["amps"]
        n += 2
        if not all(p[1] > q[1] for p, q in zip(a, a[1:])) or not all(p[0] < q[0] for p, q in zip(a, a[1:])):
            bad.append(f"② 揺れが遠くへ行くほど小さくなっていない（{a}＝TR0461）")
        if not (g["pile"] < min(g["walls"]) and max(g["walls"]) < a[1][0] and a[-1][0] < g["joint"]):
            bad.append("② 壁が鋼の板と建物の中の揺れのあいだに無い・継ぎ目の手前で測っていない（TR0461）")
    if view == "ground" and g["cave"]:
        n += 1
        x0, x1 = g["bld"]
        if any(x0 <= p[0] <= x1 for p in g["cave"]):
            bad.append("② 空洞の例を建物の下に描いた（A06＝建物の下に空洞の跡は無い）")
    if view == "cover":
        want, why = R["cover"]
        n += 1
        r = g["cover"]["real"] / g["cover"]["dwg"]
        if abs(r / (want[1] / want[0]) - 1.0) > 0.03:
            bad.append(f"② 鉄筋の上の厚さの比 {r:.2f}（記録 {want[1] / want[0]:.2f}＝{why}）")
    if view == "ruler" and g["have"]:
        n += 1
        if any(h >= nd for h, nd in zip(g["have"], g["need"])):
            bad.append("② 強さの棒が物差しの求める所に届いている（TR0214＝どちらにも足りない）")
    if view == "rebar":
        (wd, wr), why = R["over"]
        lo, hi = R["space"][0]
        n += 2
        if g["over"]["dwg"] != wd or g["over"]["real"] != wr:
            bad.append(f"② 柱の真上の鉄筋 図面 {g['over']['dwg']}本・実際 {g['over']['real']}本（記録 {wd}・{wr}＝{why}）")
        k = g["space"]["real"] / g["space"]["dwg"]
        if not lo <= k <= hi:
            bad.append(f"② 間隔の比 {k:.2f}（記録 {lo}〜{hi}＝{R['space'][1]}）")
    if view == "sat" and g["cells"]:
        n += 1
        if any(c.lower() != R["neutral"][0] for c in g["cells"]):
            bad.append(f"② 沈みの色を付けた区画がある（{R['neutral'][1]}）")
    # 🆕 ⑤b-6（2026-10-06）
    if view == "margin":
        if g["cap"] is not None and g["load"] is not None:
            n += 1
            if not g["load"] < g["cap"]:
                bad.append(f"② ふだんの重さの棒 {g['load']:.0f} が耐えられる重さの棒 {g['cap']:.0f} 以上（{R['margin']}）")
        if g["gap"] is not None:
            n += 1
            if [round(v) for v in g["gap"]] != [round(g["load"] or -1), round(g["cap"] or -1)]:
                bad.append(f"② 余裕の枠 {g['gap']} が2本の棒の端（{g['load']}〜{g['cap']}）と合わない（余裕＝差・{R['margin']}）")
    if view == "drop" and g["drop"]:
        (a, b), why = R["drop_more"]
        n += 3
        if not g["drop"][a][0] > g["drop"][b][0] > 0:
            bad.append(f"② L の側の下がり {a}＝{g['drop'][a][0]:.0f}・{b}＝{g['drop'][b][0]:.0f}（記録＝{a} がより大きい・どちらも下がる＝{why}）")
        if any(abs(v[1]) > 0.5 for v in g["drop"].values()):
            bad.append(f"② M の側も下がっている（{R['drop_still']}）")
    if view == "curve":
        for s in g["st"]:
            want, why = R["curve"][s["red"]]
            n += 1
            if (s["cross"] is not None) != want:
                bad.append(f"② 赤い線（{s['red']}）が青い線と{'交わらない' if want else '交わる'}（記録＝{'交わる' if want else '交わらない'}・{why}）")
            if s["red"] == "high":
                n += 1
                if s["gmin"] < R["curve_gap"]:
                    bad.append(f"② 決まりどおりの継ぎ目なのに2本の線の差が小さい（最小 {s['gmin']}・{R['curve_gap']} 以上＝{why}）")
            if s["ring"]:
                n += 1
                if s["cross"] is None:
                    bad.append("② 交わる所の輪を、交わらない線に描いた")
            if s["gap"]:
                n += 1
                if s["cross"] is not None:
                    bad.append(f"② 余裕の矢印を、交わる線（{s['red']}）に描いた＝余裕は無い（{R['curve']['touch'][1]}）")
    # ③ 札の数・時刻・推定
    said = [r.get("t", "") for r in m["rel"]]
    for t in texts:
        for mm in NUM_M19.finditer(t):
            tok = mm.group(0)
            n += 1
            if not any(tok in s for s in said):
                bad.append(f"③ 札「{t}」の数「{tok}」が rel（記録の値の宣言）に無い")
            if (":" in tok or "：" in tok) and tok.replace("：", ":").count(":") >= 1:
                full = tok.replace("：", ":")
                if full.count(":") == 2 and full not in R["clock"]:
                    bad.append(f"③ 札「{t}」の時刻「{tok}」が記録の時刻（{sorted(R['clock'])}）に無い")
    fa, va = R["assume"].get(view, (None, None))
    if fa and any(s.get(fa) == va for s in seq):
        n += 1
        if not any("推定" in t for t in texts):
            bad.append("③ 推定で描いた段に「推定」の札が無い（NIST の見立て＝ルール §5b-10）")
    for r in m["rel"]:
        n += 1
        if not r.get("src"):
            bad.append(f"③ rel「{r.get('t')}」に出どころ（src）が無い")
    return bad, n


def _selftest_m19(ok):
    """19本目 ⑤b-4：模式図の検算（正しい12・陽性対照＝描く側の表を壊す12＋筋と札6・型の見張り2）。"""
    import mech19 as M
    N = "模式"
    good = dict(
        cand=dict(view="cand", steps=[dict(state=dict(cand="on"), tag=dict(t="候補（6か所）", at="cand")),
                                      dict(state=dict(red="on"), tag=dict(t="門とプランターのそば", at="k131"))],
                  rel=[dict(t="6か所", src="TR p1105")], note=N),
        seq=dict(view="seq", start=dict(first="on", second="on"), steps=[dict(state=dict(around="on"), tag=dict(t="まわり", at="around"))],
                 note=N),
        code=dict(view="code", steps=[dict(state=dict(dots="on", flex="on"), tag=dict(t="赤", at="red"))], note=N),
        dmg=dict(view="dmg", steps=[dict(state=dict(leak="on", pts="on"), tag=dict(t="9時間前", at="leak"))],
                 rel=[dict(t="9時間前", src="TR p1159")], note=N),
        sight=dict(view="sight", steps=[dict(state=dict(vis="on"), tag=dict(t="見えた範囲", at="vis"))], note=N),
        cam=dict(view="cam", steps=[dict(state=dict(unit="on", move="on"), tag=dict(t="1:22:04〜1:22:15", at="clock"))],
                 rel=[dict(t="1:22:04・1:22:15", src="TR p1345")], note=N),
        hall=dict(view="hall", steps=[dict(state=dict(ref="on", sag="on"), tag=dict(t="1:21:55", at="ref"))],
                  rel=[dict(t="1:21:55", src="TR p1353")], note=N),
        core=dict(view="core", steps=[dict(state=dict(new="on"), tag=dict(t="敷石", at="new"))], note=N),
        cover=dict(view="cover", steps=[dict(state=dict(dwg="on", real="on"), tag=dict(t="図面", at="dwg"))], note=N),
        rebar=dict(view="rebar", steps=[dict(state=dict(real="on", space="on"), tag=dict(t="間隔", at="space"))], note=N),
        joint=dict(view="joint", start=dict(color="on", bars="on", ties="on"),
                   steps=[dict(state=dict(crush="on", bar2="on"), tag=dict(t="押しつぶされた（推定）", at="crush"))], note=N),
        excav=dict(view="excav", steps=[dict(state=dict(pit="on", drive="on", wave="on", damp="more"), tag=dict(t="揺れ", at="damp"))],
                   note=N),
        zoneb=dict(view="zoneb", steps=[dict(state=dict(mark="on", brk="on"), tag=dict(t="①", at="one"))], note=N),
        ground=dict(view="ground", steps=[dict(state=dict(lime="on", cave="on", none="on"), tag=dict(t="例", at="cave"))], note=N),
        front=dict(view="front", steps=[dict(state=dict(roof="down"), tag=dict(t="柱の頭（推定の模式）", at="heads"))], note=N),
        # 🆕 ⑤b-6（2026-10-06）
        margin=dict(view="margin", steps=[dict(state=dict(cap="on", load="on"), tag=dict(t="耐えられる重さ", at="cap")),
                                          dict(state=dict(gap="on"), tag=dict(t="余裕", at="gap", to="gap"))], note=N),
        drop=dict(view="drop", steps=[dict(state=dict(ref="on"), tag=dict(t="前日のコマ", at="ref")),
                                      dict(state=dict(now="on"), tag=dict(t="1:22:14 ごろ", at="l91"))],
                  rel=[dict(t="1:22:14", src="TR p1348")], note=N),
        curve_high=dict(view="curve", steps=[dict(state=dict(blue="on", red="high"), tag=dict(t="決まりどおり", at="red")),
                                             dict(state=dict(gap="on"), tag=dict(t="余裕", at="gap"))], note=N),
        curve_mid=dict(view="curve", steps=[dict(state=dict(blue="on", red="mid")), dict(state=dict(cross="on"), tag=dict(t="交わる", at="cross"))],
                       note=N),
        curve_touch=dict(view="curve", steps=[dict(state=dict(blue="on", red="touch", cross="on"), tag=dict(t="余裕ゼロ", at="cross"))],
                         note=N))
    for nm, kw in good.items():
        bad, n = judge("m19", kw)
        ok &= not bad
        print(f"  {'OK' if not bad else '🔴 NG'} 19本目 正しい模式図（{nm}）: {'合格' if not bad else '🔴 ' + bad[0]}（{n}件）")
    # 陽性対照（描く側の表を壊す＝筋は正しいのに絵が記録と食い違う）
    for name, attr, val, key, kwk in (
            ("候補の1つを N-13.1 に描く", "CAND", [("N", "13.1")] + M.CAND[1:], "候補の位置", "cand"),
            ("まわりの柱を1つ M-11.1 に描く", "AROUND", M.AROUND[:-1] + [("M", "11.1")], "まわりの柱", "seq"),
            ("ひどい不足の継ぎ目を1つ落とす", "CODE_DOTS", dict(M.CODE_DOTS, red=M.CODE_DOTS["red"][1:]), "ひどい不足", "code"),
            ("漏れを K と L のあいだに描く", "LEAK", (970.0, 478.0, 55.0, 35.0), "漏れの楕円", "dmg"),
            ("見えた範囲をデッキ全体にする", "VISIBLE", [(930.0, 350.0), (1460.0, 350.0), (1460.0, 800.0), (930.0, 800.0)], "見えた範囲が", "sight"),
            ("11 の列を K と L のあいだに描く", "CAM_X", dict(M.CAM_X, L=580.0), "L・M の線", "cam"),
            ("廊下の I の辺りもたわませる", "HA_SAG", (0.0, 8.0) + M.HA_SAG[2:], "動かない所", "hall"),
            ("タイルの層を厚く描く", "CORE", dict(M.CORE, tile=2.0), "重ねの厚さ", "core"),
            ("実際の厚さを 1.5インチで描く", "CV", dict(M.CV, real=1.5), "厚さの比", "cover"),
            ("実際の間隔を 1.6倍で描く", "RB_C", dict(M.RB_C, k=1.6), "間隔の比", "rebar"),
            ("継ぎ目の高さに輪の鉄筋を描く", "JO_TIES", M.JO_TIES + (555.0,), "床の高さ（継ぎ目）に輪", "joint"),
            ("床の強さを 5000 で描く", "JO_STRENGTH", (6000.0, 5000.0), "強さの棒の比", "joint"),
            ("揺れを壁の内で大きく描く", "EX_AMP", ((630.0, 10.0), (800.0, 26.0), (1300.0, 4.0)), "小さくなっていない", "excav"),
            ("折れる所を E の柱の西に描く", "ZB", dict(M.ZB, brk=480.0), "折れる所（①）", "zoneb"),
            ("空洞の例を建物の下に描く", "GR_CAVE", [(x - 700.0, y) for x, y in M.GR_CAVE], "建物の下", "ground"),
            ("屋根を上へ動かす", "FR", dict(M.FR, drop=-60.0), "突き出していない", "front"),
            # 🆕 ⑤b-6
            ("ふだんの重さの棒を長く描く", "MG", dict(M.MG, load=1600.0), "以上", "margin"),
            ("L-8 の側を L-9.1 より下げる", "DP", dict(M.DP, drop={"9.1": 30.0, "8": 38.0}), "L の側の下がり", "drop"),
            ("決まりどおりの赤い線を低く描く", "CURVE_RED", dict(M.CURVE_RED, high=(0.66, 0.12)), "交わる", "curve_high"),
            ("余裕ゼロの赤い線を高く描く", "CURVE_RED", dict(M.CURVE_RED, touch=(0.95, 0.10)), "交わらない", "curve_touch")):
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            bad, _ = judge("m19", good[kwk])
        except Exception as e:                 # 壊した値で組めない＝その旨を出して落とす
            bad = [f"組めない {e!r}"]
        finally:
            setattr(M, attr, keep)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 19本目 陽性対照（画素）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    # 陽性対照（筋と札）
    for name, kw, key in (
            ("落ちる前にフックの鉄筋", dict(view="punch", steps=[dict(state=dict(hook="on"), tag=dict(t="x", at="hook"))], note=N), "① 筋"),
            ("はがす前に傾けたコンクリート", dict(view="water", steps=[dict(state=dict(slope="on"), tag=dict(t="x", at="slope"))], note=N), "① 筋"),
            ("打ち込む前に揺れ", dict(view="excav", steps=[dict(state=dict(pit="on", wave="on"), tag=dict(t="x", at="wave"))], note=N), "① 筋"),
            ("押しつぶしに推定の札が無い", dict(view="joint", start=dict(color="on", bars="on", ties="on"),
                                         steps=[dict(state=dict(crush="on"), tag=dict(t="押しつぶされた", at="crush"))], note=N), "推定"),
            ("札の時刻が記録に無い（1:22:05）", dict(view="cam", steps=[dict(state=dict(unit="on"), tag=dict(t="1:22:05", at="clock"))],
                                                 rel=[dict(t="1:22:05", src="x")], note=N), "記録の時刻"),
            ("札の数が rel に無い", dict(view="cover", steps=[dict(state=dict(dwg="on"), tag=dict(t="約3センチ", at="dwg"))], note=N), "rel"),
            # 🆕 ⑤b-6
            ("基準の床の前に下がり", dict(view="drop", steps=[dict(state=dict(now="on"), tag=dict(t="x", at="l91"))], note=N), "① 筋"),
            ("交わる線に余裕の矢印", dict(view="curve", steps=[dict(state=dict(blue="on", red="touch", gap="on"), tag=dict(t="x", at="gap"))],
                                       note=N), "余裕の矢印")):
        bad, _ = judge("m19", kw)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 19本目 陽性対照（筋と札）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    for nm, fn in (("押しつぶれを戻す", lambda: M.m19("edge", [dict(state=dict(fall="full", pull="on", joint="crush")),
                                                             dict(state=dict(joint="hurt"))], note=N)),
                   ("知らない欄", lambda: M.m19("site", [dict(state=dict(sea="on"))], note=N))):
        try:
            fn()
            g_ = False
        except ValueError:
            g_ = True
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 19本目 型の見張り：{nm}: {'組めない（止まった）' if g_ else '🔴 組めた'}")
    return ok


# ══════════════════════════════════════════════════════════
#  🆕 20本目 ⑤b-5（2026-10-10）：模式図（m20＝`tools/mech20.py`・11の見え方）
# ══════════════════════════════════════════════════════════
# 🔴 記録の値は門番の側に持つ（§5b-88＝描く側の表 mech20.TOP_ENG_Y・HY_CUT・AL_PTS・FX_PLANE・PR_BULK…を書き換えると鳴る）。
# 🔴 2026-10-12（21本目 ⑤b-1・§0b）：20本目の記録 REC_M20 の全項目（操縦室の席・番号の枠・エンジンの横の位置・管が切れる所・高さの記録の点と印の時刻・
#    降下率・脚とフラップ・無線の相手・夜の測位と読み取りの幅・3つの空港・札に出してよい時刻・疲労亀裂とリベットの列・速さの比・ベイ・下半分の交換・
#    エッジ・シール・目視の範囲・亀裂の長さ・発見確率・化粧室・天井の穴と風・走路・温度・減圧の幅・穴の面積・探索のカメラと広さ・点検口・言葉の使い分け・
#    FAA の英文・3つの答え・フューズ・20,000フィートの帯・推定で描く段・「考えられる」の段）は selftest の見本 `tools/fixture_ep20.py`
#    （GATES["check_mech"]・値は1つも変えていない＝git の `cbf40ec`）へ移した＝空。selftest は見本の表だけ差し込む
#    （`fixture_ep20.apply(gate, tables_only=True)`）。21本目で模式図 mech20 の型を使うときは、その回の記録の値をここに別に持つ（§5b-88＝描く側の表
#    mech20.TOP_ENG_Y・HY_CUT・AL_PTS・FX_PLANE・PR_BULK…を書き換えると鳴る）。頁の番号の書き方（報告書＝印刷の頁・別添6 は p310〜343・解説＝1000＋頁）と
#    引いた原文は移した注の側にある＝fixture_ep20 の REC_M20 の注。空のあいだ、m20 のカットは `judge_m20` が「記録の表が空」で止める（fail closed＝KeyError にしない）。
#    `FT`（フィート→メートル）は単位の型＝残す
FT = 0.3048
REC_M20 = {}


def _hms(s):
    p = [int(v) for v in s.split(":")] + [0, 0]
    return p[0] * 3600 + p[1] * 60 + p[2]


def _fit(pairs):
    """[(値, 画素)] から 画素→値 の一次式"""
    (v0, p0), (v1, p1) = pairs[0], pairs[-1]
    return lambda p: v0 + (p - p0) * (v1 - v0) / (p1 - p0)


def judge_m20(f):
    """20本目 模式図：①状態の筋 ②形（f.mech["geo"]）を記録（REC_M20）で ③札の数・時刻・推定の札。"""
    bad, n = [], 0
    m = f.mech
    g, view = m["geo"], m["view"]
    seq = [m["start"]] + list(m["states"])
    R = REC_M20
    if not R:       # 🆕 21本目 ⑤b-1：記録の表が空のあいだは止める（KeyError で理由が見えなくならない＝fail closed。judge_m19 と同じ）
        return ["記録の表 REC_M20 が空（21本目の値を入れるまで、m20 のカットは止まる）"], 1
    texts = list(m["tags"])

    def need(cond, msg):
        nonlocal n
        n += 1
        if not cond:
            bad.append(msg)
    # ① 筋（先に起きることが先）
    for s in seq:
        if view == "seats":
            need(not (s["left"] == "cop") or s["right"] == "cap", "① 筋：左に副操縦士なら右に機長（同じ段で）＝報告書 p6")
            need(s["cert"] != "on" or s["right"] == "cap", "① 筋：認定の印は、右の席の機長を見せてから（p14）")
        if view == "xpdr":
            need(s["reply"] == "off" or s["ask"] == "on", "① 筋：番号を返すのは、レーダーが問うてから")
        if view == "hyd":
            need(s["cut"] != "on" or s["pipes"] == "on", "① 筋：切れる管は、管を見せてから")
            need(s["num"] != "on" or s["pipes"] == "on", "① 筋：系統の番号は、管を見せてから")
        if view == "thrust":
            need(s["nose"] != "up" or s["pwr"] == "up", "① 筋：機首が上がるのは、推力を上げてから（p117 の推定）")
            need(s["yaw"] != "on" or s["diff"] in ("ask", "on"), "① 筋：向きが変わるのは、左右の推力に差をつけてから（p114）")
        if view == "alt":
            need(s["rate"] != "on" or s["pts"] != "off", "① 筋：降下率の線は、記録の点を見せてから")
            need(s["stop"] != "on" or s["pts"] == "all", "① 筋：降下が止まる印は、最後の点を見せてから")
        if view == "gear":
            need(s["flap"] != "down" or s["gear"] == "down", "① 筋：フラップは脚のあと（18時38分以降脚・18時44分以降フラップ＝p117）")
        if view == "radio":
            need(s["ask"] != "on" or s["link"] == "on", "① 筋：切り替えの問いは、いまの相手を見せてから")
            need(s["stay"] != "on" or s["ask"] == "on", "① 筋：「切り替えない」は、問いのあと（p333）")
        if view == "fix":
            need(s["zoom"] != "on" or s["ray"] == "on", "① 筋：寄りの窓は、方角と距離の線を見せてから")
            need(all(s[k] != "on" for k in ("pa", "pd", "heli")) or s["zoom"] == "on", "① 筋：読み取りの幅は寄りの窓の中")
            need(s["pd"] != "on" or s["pa"] == "on", "① 筋：距離の幅は、方位の幅を見せてから")
        if view == "press":
            need(s["push"] != "on" or s["press"] == "on", "① 筋：押す力は、客室の与圧を見せてから（p125）")
        if view == "bag":
            need(s["swell"] != "on" or s["bags"] == "on", "① 筋：ふくらむのは、袋を見せてから")
        if view == "apt":
            need(all(s[k] != "on" for k in ("why", "ok")) or s["pick"] == "on", "① 筋：理由と見立ては、選んだ空港を見せてから")
        # 🆕 ⑤b-6
        if view == "fatigue":
            need(s["crack"] != "on" or s["load"] == "rep", "① 筋：ひびが伸びるのは、くり返しの力のあと")
        if view == "grow":
            need(s["one"] != "on" or s["two"] == "on", "① 筋：1列の線は、比べる元の2列の線を見せてから")
            need(s["same"] != "on" or s["one"] == "on", "① 筋：同じ長さの印は、2本の線を見せてから")
        if view == "half":
            need(s["join"] != "on" or s["half"] == "on", "① 筋：継ぎ目の印は、上と下を分けてから")
        if view == "edge":
            need(s["req"] != "on" or s["bad"] == "on", "① 筋：決まりの長さは、近すぎる穴を見せてから")
        if view == "seal":
            need(s["eye"] != "on" or s["seal"] == "on", "① 筋：目で見る印は、シール材を見せてから（p103）")
        if view == "clen":
            need(s["len"] != "on" or s["crack"] == "on", "① 筋：長さの括弧は、亀裂を見せてから")
        if view == "prob":
            need(s["q"] != "on" or s["many"] == "on", "① 筋：「？」は、確率の幅を見せてから")
        if view == "two":
            need(s["ok"] != "on" or s["pick"] == "on", "① 筋：妥当の印は、正しい作りの壁を示してから")
        # 🆕 ⑤b-6b
        if view == "cab":
            need(s["flow"] == "off" or s["hole"] == "on", "① 筋：流れの矢印は、天井の穴を見せてから")
            need(s["half"] != "on" or s["hole"] == "on", "① 筋：半球は、天井の穴を見せてから")
            need(s["gauge"] != "lo" or s["hole"] == "on", "① 筋：気圧の針が下がるのは、穴が開いてから")
            need(s["gauge"] == "off" or seq[0]["gauge"] != "off", "① 筋：気圧の計は頭（start）から出す（目盛りは基図）")
        if view == "flow":
            need(s["seat"] != "on" or s["air"] == "on", "① 筋：座席のあたりの弱い風は、客室の平均の風を見せてから")
        if view == "sonar":
            need(s["echo"] != "on" or s["beam"] == "on", "① 筋：跳ね返りは、扇の音を出してから")
        if view == "res":
            need(s["need"] != "on" or s["cell"] == "on", "① 筋：見分けられる大きさは、1つの点を見せてから")
        if view == "area":
            need(s["rep"] != "on" or s["day"] == "on", "① 筋：くり返しは、1日に写せる広さを見せてから")
        if view == "word":
            need(s["mean"] != "on" or s["pick"] == "on", "① 筋：言葉の意味は、原因の言葉を示してから")
        if view == "faa":
            need(s["hl"] != "on" or s["body"] == "on", "① 筋：句の印は、英文を見せてから")
        if view == "ans":
            need(s["q3b"] != "on" or s["q3a"] == "on", "① 筋：3つ目の残りは、答えのある方を見せてから")
        if view == "hyd":
            need(s["fuse"] == "off" or s["pipes"] == "on", "① 筋：フューズは、管を見せてから")
    # ② 形（記録で照らす）
    if view == "seats":
        names = g["names"]
        if any(s["left"] == "cop" for s in seq):
            need(names["left"] == [R["seats"]["day"][0]] and names["right"] == [R["seats"]["day"][1]],
                 f"② この日の席の名 左 {names['left']}・右 {names['right']}（記録＝左 {R['seats']['day'][0]}・右 {R['seats']['day'][1]}＝{R['seats']['src']}）")
        if any(s["left"] == "usual" for s in seq):
            need(names["left"] == [R["seats"]["usual_left"]], f"② ふつうの並びの左の席 {names['left']}（記録＝{R['seats']['usual_left']}）")
        (lx, ly), (rx, ry) = g["pilots"]
        fx, fy = g["fe"]
        need(fx > (lx + rx) / 2 and fy > max(ly, ry) + 80 and g["p4_x"] > rx,
             f"② 航空機関士の席が右の席の後ろ・計器が右の壁に無い（{fx:.0f}, {fy:.0f}＝付図-12 の P4）")
    if view == "xpdr" and g["boxes"]:
        need(g["boxes"] == R["xpdr_digits"][0], f"② 番号の枠 {g['boxes']} 桁（記録＝{R['xpdr_digits'][0]} 桁＝{R['xpdr_digits'][1]}）")
    if view == "hyd":
        (yi, yo), src = R["eng_y"]
        for no, (px, py) in g["eng"].items():
            y = (px - g["cx"]) / g["k"]
            want = yi if no in (2, 3) else yo
            need(abs(abs(y) - want) < 0.05, f"② エンジン No.{no} の横の位置 {abs(y):.2f}m（記録 {want}m＝{src}）")
            need((y < 0) == (no in R["left_engines"][0]), f"② エンジン No.{no} の左右（記録＝左は {sorted(R['left_engines'][0])}＝{R['left_engines'][1]}）")
        if g["pipes"]:
            need(g["pipes"] == R["hyd_n"][0], f"② 管の数 {g['pipes']}（記録 {R['hyd_n'][0]}＝{R['hyd_n'][1]}）")
            for no, (x, y) in g["starts"].items():
                need(abs(abs(y) - (yi if no in (2, 3) else yo)) < 0.05, f"② 系統 {no} の管がエンジン No.{no} から出ていない（ポンプ＝p51）")
        (a, b), why = R["hyd_cut"]
        need(a < g["tail_x"] <= b, f"② 管の先 {g['tail_x']:.1f}m が尾翼の中に無い（{a}〜{b}m＝{why}）")
        if g["cut_x"] is not None:
            need(a < g["cut_x"] < b, f"② 管が切れる所 {g['cut_x']:.1f}m が垂直尾翼の中（{a}〜{b}m）に無い＝{why}")
        if g["nums"]:
            xs = [g["num_x"][no] for no in (1, 2, 3, 4)]
            need(xs == sorted(xs), "② 系統の番号の並びが左から 1・2・3・4 でない")
    if view == "thrust":
        cg, why = R["cg_x"]
        need(abs(g["cg_x"] - cg) < 0.05, f"② 回す中心 {g['cg_x']:.2f}m（記録 {cg}m＝{why}）")
        if any(s["nose"] == "up" for s in seq):
            need(g["nose_dy"] > 20, f"② 機首を上げた段の機首が上がっていない（機首の先と中心の高さの差 {g['nose_dy']:.0f} 画素）")
        for s, (diff, yaw, L, ang) in zip(seq, g["yaw"]):
            if diff != "off":
                need(L[1] > L[4] and L[2] > L[3], f"② 左右の推力の差の矢印（左 {L[1]}・{L[2]}／右 {L[3]}・{L[4]}）＝左を強く")
        if "nose_dx" in g and any(s["yaw"] == "on" for s in seq):
            need(g["nose_dx"] > 10, f"② 左が強いのに機首が右へ向いていない（{g['nose_dx']:.0f} 画素）")
        for no, y in g["top_eng_y"].items():
            want = R["eng_y"][0][0] if no in (2, 3) else R["eng_y"][0][1]
            need(abs(abs(y) - want) < 0.05 and (y < 0) == (no in R["left_engines"][0]), f"② 上から見たエンジン No.{no} の位置 {y}m")
    if view == "alt":
        span = g["span"]
        tx, ya = _fit([( _hms(t), x) for t, x in g["xt"]]), _fit(g["yt"])
        rec = R["alt"][span]
        got = []
        for x, y in g["dots"]:
            t, mm = tx(x), ya(y)
            hit = [r for r in rec if abs(_hms(r[0]) - t) < 1.0 and abs(r[1] * FT - mm) < 15.0]
            need(bool(hit), f"② 点（{x:.0f}, {y:.0f}）＝{t:.0f}秒・{mm:.0f}m が記録の点に無い（{R['alt_src']}）")
            got += hit
        if seq[-1]["pts"] == "all":
            need(len(set(got)) == len(rec), f"② 記録の点 {len(rec)} のうち {len(set(got))} しか描いていない（{R['alt_src']}）")
        for k_, x in g["marks"].items():
            want = _hms(R["alt_marks"][span][k_])
            need(abs(tx(x) - want) < 1.0, f"② 印 {k_} の時刻 {tx(x):.0f}秒（記録 {R['alt_marks'][span][k_]}）")
        if g.get("rate"):
            (x0, y0), (x1, y1) = g["rate"]
            rate = (ya(y0) - ya(y1)) / FT / ((tx(x1) - tx(x0)) / 60.0)
            need(abs(rate - R["alt_rate"][0]) / R["alt_rate"][0] < 0.02, f"② 降下率の線 {rate:.0f} フィート/分（記録 {R['alt_rate']}）")
    if view == "gear":
        d, why = R["gear"]
        need(abs(sum(g["main_x"]) / 2 - g["nose_x"] - d) < 0.6, f"② 前の脚と主脚の間 {sum(g['main_x']) / 2 - g['nose_x']:.2f}m（記録 {d}m＝{why}）")
        need(g["lag"] > 0, "② フラップが脚と同時に動く（記録＝脚のあと＝p117）")
    if view == "radio":
        need(g["names"] == R["radio"]["names"], f"② 無線の相手の名 {g['names']}（記録 {R['radio']['names']}＝{R['radio']['src']}）")
    if view == "fix":
        F_ = R["fix"]
        need(abs(g["brg"] - F_["ray"][0]) < 0.5 and abs(g["nm"] - F_["ray"][1]) < 0.3,
             f"② 方角と距離の線 {g['brg']:.1f}°・{g['nm']:.1f}マイル（記録 {F_['ray']}＝{F_['src']}）")
        for k_ in ("plane", "heli"):
            if g[k_]:
                w, dpt = F_[k_]
                need(abs(g[k_]["width"] - w) < 0.05 * w and abs(g[k_]["depth"] - dpt) < 0.05 * dpt,
                     f"② {k_} の扇 {g[k_]['width']:.2f}度・{g[k_]['depth']:.3f}マイル（記録 {w}度・{dpt}マイル＝{F_['src']}）")
    if view == "hoist":
        need(g["people"] == 0, "② 人を描いた（台本の画の欄＝人は描かない）")
    if view == "press":
        bx, why = R["bulk_x"]
        need(abs(g["bulk_x"] - bx) < 0.05, f"② 隔壁の位置 {g['bulk_x']:.2f}m（記録 {bx}m＝{why}）")
        for (a, b) in g["arrows"]:
            need(a[0] < b[0] <= g["bulk_x"], "② 押す矢印が客室の側から後ろ（隔壁）へ向いていない")
    if view == "bag" and g["ratio"] is not None:
        need(g["ratio"] > 1.1, f"② 山の上の袋が海の近くの袋よりふくらんでいない（面積の比 {g['ratio']:.2f}＝解説 p1017）")
    if view == "apt":
        A = R["apt"]
        want = sorted(A["lons"], key=lambda k: A["lons"][k])
        need(g["order"] == want, f"② 空港の並び {g['order']}（記録＝西から {want}）")
        if g["why"]:
            need(tuple(g["why"]) == A["why"], f"② 理由の言葉 {g['why']}（記録＝{A['why']}＝{A['src']}・言い換えない）")
        if g["picked"]:
            need(g["picked"] == A["picked"], f"② 選んだ空港 {g['picked']}（記録＝{A['picked']}＝{A['src']}）")
    # 🆕 ⑤b-6
    if view == "fatigue" and g["cracks"]:
        hx, hy, hr = g["hole"]
        for side, ((x0, y0), (x1, y1)) in g["cracks"].items():
            need(abs(math.hypot(x0 - hx, y0 - hy) - hr) < 2.0, f"② ひび（{side}）の根元が穴の縁に無い（{R['fatigue']['src']}）")
            ang = math.degrees(math.atan2(-(y1 - y0), x1 - x0)) % 180.0
            need(abs(((ang - g["load_deg"]) % 180.0) - 90.0) < 5.0,
                 f"② ひび（{side}）の向き {ang:.0f}度が引く力（{g['load_deg']:.0f}度）に直角でない")
    if view == "rows":
        W = R["rows"]
        for k, want in W["n"].items():
            need(g["rows"][k] == want, f"② {k} の列の数 {g['rows'][k]}（記録 {want}＝{W['src']}）")
            a, b = g["lap"][k]
            need(all(a < y < b for y in g["row_y"][k]), f"② {k} の列が板の重なりの外にある")
        if g["bars"]:
            r_ = g["bars"]["b"] / g["bars"]["a"]
            need(abs(r_ - W["ratio"]) < 0.01, f"② 強さの棒の比 {r_:.2f}（記録 約{W['ratio']}＝{W['src']}）")
    if view == "grow" and len(g["lines"]) == 2:
        def _slope(ln):
            (x0, y0), (x1, y1) = ln
            return (y0 - y1) / (x1 - x0)
        r_ = _slope(g["lines"]["one"]) / _slope(g["lines"]["two"])
        lo_, hi_ = R["grow"]["ratio"]
        need(lo_ < r_ <= hi_, f"② 1列と2列の速さの比 {r_:.2f}（記録＝2倍強＝{R['grow']['src']}）")
        if g["hits"]:
            q = (g["hits"]["one"] - g["x0"]) / (g["hits"]["two"] - g["x0"])
            need(abs(q - 1 / r_) < 0.02, f"② 同じ長さに届くまでの比 {q:.2f} が速さの比の逆数 {1 / r_:.2f} と合わない")
    if view == "fs":
        cx, cy = g["c"]
        S_ = g["straps"]
        if g["one"]:
            idx = []
            for (x, y) in g["one"]:
                rr = math.hypot(x - cx, y - cy) / g["R"]
                j = min(range(len(S_)), key=lambda i: abs(S_[i] - rr))
                need(abs(S_[j] - rr) < 0.005, f"② 1列の所の端（半径の比 {rr:.3f}）がストラップの上に無い")
                need(x < cx, "② 1列の所が左側に無い（記録＝左側の L18）")
                idx.append(j + 1)
            need(sorted(idx) == sorted(R["fs"]["one"]), f"② 1列の所＝第{sorted(idx)}ストラップの間（記録＝第1と第3＝{R['fs']['src']}）")
        if g["bay"]:
            a, b = sorted(g["bay"])
            edges = sorted([0.0] + S_ + [1.0])
            need(any(e0 <= a and b <= e1 for e0, e1 in zip(edges, edges[1:])),
                 f"② 1ベイの亀裂（{a}〜{b}）がストラップをまたいでいる（p110＝1ベイの中）")
    if view == "half" and g["new"]:
        z = g["lens_z"]
        other = "up" if g["new"] == "lo" else "lo"
        need(g["new"] == R["half"]["new"] and z[g["new"]][1] <= z[other][0] + 1e-6,
             f"② 取り替えた側（{g['new']}）が下半分でない（{R['half']['src']}）")
    if view == "edge" and any(s[2] == "on" for s in g["seq"]):
        m_ = g["m"]
        need(m_["bad"] < m_["req"] < m_["good"],
             f"② 余白の長さ：近すぎる {m_['bad']:.0f}・決まり {m_['req']:.0f}・足りている {m_['good']:.0f}（近すぎる＜決まり＜足りている）")
    if view == "seal":
        for nm, (x, y) in g["beads"]:
            need(abs(y - g["ends"][nm]) < 1.0, f"② シール材（{nm}）が板の端の縁に無い（{R['seal']['src']}）")
        if g["beads"]:
            need({nm for nm, _ in g["beads"]} == set(R["seal"]["ends"]), "② シール材の数が板の端と合わない")
        if g["eye_x"] is not None:
            need(g["eye_x"] > g["stack_x1"], "② 目が後ろの側（点検する後面）に無い（p104）")
    if view == "rear" and g["all_r"] is not None:
        need(abs(g["all_r"] - g["R"]) < 1.0, f"② 目で見る範囲が後面全体でない（半径 {g['all_r']:.0f}／{g['R']:.0f}＝{R['rear']['src']}）")
    if view == "clen" and g["sides"]:
        rs = [d["vis"] / d["total"] for d in g["sides"].values()]
        for r_ in rs:
            need(abs(r_ - R["clen"]["ratio"]) < 0.01, f"② 見える長さの比 {r_:.2f}（記録 {R['clen']['ratio']}＝{R['clen']['src']}）")
        need(max(rs) - min(rs) < 1e-6, "② 穴の両側で長さが違う（記録＝両側の平均）")
    if view == "prob":
        fx = _fit(g["xt"])
        if g["one"] is not None:
            need(abs(fx(g["one"]) - R["prob"]["one"]) < 0.3,
                 f"② 1つの亀裂の確率 {fx(g['one']):.1f}%（記録 {R['prob']['one']}%程度＝{R['prob']['src']}）")
        if g["many"]:
            got = tuple(round(fx(x), 1) for x in g["many"])
            need(all(abs(a - b) < 0.3 for a, b in zip(got, R["prob"]["many"])),
                 f"② 少なくとも1つの確率の幅 {got}（記録 {R['prob']['many']}＝{R['prob']['src']}）")
    if view == "two":
        need(g["cracks"]["a"] == 0 and g["cracks"]["b"] > 0,
             f"② 亀裂の印：正しい作り {g['cracks']['a']}・事故機 {g['cracks']['b']}（{R['two']['src']}）")
    if view == "lav":
        (la, lb), (ca, cb) = g["lav"], g["coat"]
        need(lb < g["bulk"] and lb >= cb and la >= ca, f"② 化粧室が客室のいちばん後ろ（隔壁の前）に無い（{R['lav']['src']}）")
    # 🆕 ⑤b-6b
    if view == "cab":
        C_ = R["cab"]
        if g["hole_area"] is not None:
            need(abs(g["hole_area"] - C_["area"]) / C_["area"] < 0.02, f"② 穴の面積 {g['hole_area']:.3f}m2（記録 約{C_['area']}m2＝{C_['src']}）")
        if g["half"]:
            need(abs(g["half"]["R"] - C_["R"]) < 0.01, f"② 半球の半径 {g['half']['R']:.2f}m（記録 {C_['R']}m＝{C_['src']}）")
            need(abs(g["half"]["d"] - C_["R"]) < 0.05, f"② 印の席と穴の間 {g['half']['d']:.2f}m（記録 {C_['R']}m）")
        if g["flow"] and g["flow"]["far"] is not None:
            need(g["flow"]["near"] >= 3.0 * g["flow"]["far"],
                 f"② 矢印の長さ：穴の近く {g['flow']['near']:.0f}・離れた所 {g['flow']['far']:.0f}（離れると弱い＝解説 p1003）")
        if any(s["gauge"] == "lo" for s in seq):
            need(g["needle"]["lo"] < g["needle"]["hi"], "② 気圧の針が下がる向きに動かない")
    if view == "flow":
        for nm, arr in (("up", g["up"]), ("seat", g["seat"])):
            for a, b in arr:
                need(b > a and b < g["bulk_x"], f"② 客室の風の矢印（{nm}）が後ろの壁へ向いていない・壁を越える（{R['flow']['src']}）")
        if g["up"] and g["seat"]:
            lu = sum(b - a for a, b in g["up"]) / len(g["up"])
            ls = sum(b - a for a, b in g["seat"]) / len(g["seat"])
            need(lu >= 2.0 * ls, f"② 座席のあたりの矢印 {ls:.1f}m が天井の近く {lu:.1f}m と比べて弱くない（{R['flow']['src']}）")
    if view == "run":
        need(abs(g["m"] - R["run"]["m"]) < 0.5, f"② 走路の長さ {g['m']:.1f}m（記録 {R['run']['m']}m＝{R['run']['src']}）")
        need(all(d < 0 for d in g["wind_dx"]), "② 風の向きが走る向きの逆（顔に当たる向き）でない")
    if view == "temp" and g["dots"]:
        fx, fy = _fit(g["xt"]), _fit(g["yt"])
        got = [(round(fx(x), 2), round(fy(y), 2)) for x, y in g["dots"]]
        want = list(R["temp"]["pts"])
        need(len(got) == len(want) and all(abs(a - c) < 0.05 and abs(b - d) < 0.3 for (a, b), (c, d) in zip(got, want)),
             f"② 温度の点 {got}（記録 {want}＝{R['temp']['src']}）")
    if view == "dect":
        fx = _fit(g["xt"])
        if g["j123"]:
            got = tuple(round(fx(x), 2) for x in g["j123"])
            need(all(abs(a - b) < 0.03 for a, b in zip(got, R["dect"]["j123"])),
                 f"② 123便の幅 {got}秒（記録 {R['dect']['j123']}＝{R['dect']['src']}）")
        if g["b737"] is not None:
            need(abs(fx(g["b737"]) - R["dect"]["b737"]) < 0.03, f"② 2009年の例 {fx(g['b737']):.2f}秒（記録 約{R['dect']['b737']}＝{R['dect']['src']}）")
    if view == "holes":
        for nm, a in g["areas"].items():
            need(abs(a - R["holes"][nm]) / R["holes"][nm] < 0.02, f"② 穴の面積（{nm}）{a:.3f}m2（記録 {R['holes'][nm]}＝{R['holes']['src']}）")
    if view == "sonar" and g["fans"]:
        (l0, l1), (r0, r1) = g["fans"]["l"], g["fans"]["r"]
        need(abs(l0 - r0) < 0.5 and abs(l1 - r1) < 0.5, f"② 扇が左右で対称でない（左 {l0:.0f}〜{l1:.0f}度・右 {r0:.0f}〜{r1:.0f}度＝解説 p1023 図17）")
    if view == "dcam":
        if g["h"] is not None:
            need(abs(g["h"] - R["dcam"]["h"]) < 0.02, f"② カメラの高さ {g['h']:.2f}m（記録 約{R['dcam']['h']}m＝{R['dcam']['src']}）")
        if g["w"] is not None:
            need(abs(g["w"] - R["dcam"]["w"]) < 0.02, f"② 写る幅 {g['w']:.2f}m（記録 約{R['dcam']['w']}m＝{R['dcam']['src']}）")
    if view == "res":
        need(all(abs(a - b) < 0.01 for a, b in zip(g["cell"], R["res"]["cell"])),
             f"② 1つの点 {g['cell']}m（記録 {R['res']['cell']}＝{R['res']['src']}）")
        if g["need"]:
            need(all(abs(a - b) < 0.05 for a, b in zip(g["need"], R["res"]["need"])),
                 f"② 見分けられる大きさ {tuple(round(v, 2) for v in g['need'])}m（記録 {R['res']['need']}＝{R['res']['src']}）")
    if view == "area":
        need(abs(g["km2"] - R["area"]["km2"]) < 0.1, f"② 区域の広さ {g['km2']:.1f}km2（記録 約{R['area']['km2']}＝{R['area']['src']}）")
        if g["day_km2"]:
            d_ = g["km2"] / g["day_km2"]
            need(abs(d_ - R["area"]["days"]) / R["area"]["days"] < 0.01, f"② 区域÷1日の広さ＝{d_:.0f}日（記録 {R['area']['days']:.0f}日）")
    if view == "cover":
        a, b = g["fin"]
        need(a <= g["hole_x"] <= b, f"② 点検口 {g['hole_x']}m が垂直尾翼の根元（{a}〜{b}m）に無い（{R['cover']['src']}）")
        if g["air0"] is not None:
            need(g["air0"] > g["bulk_x"], "② 尾翼へ向かう空気が隔壁の後ろから出ていない")
    if view == "word":
        need(tuple(g["rows"]) == R["word"]["rows"], f"② 言葉の使い分けが記録と違う（{R['word']['src']}・言い換えない・順も）")
        if g["pick"]:
            need(g["pick"] == R["word"]["pick"], f"② 原因の言葉 {g['pick']}（記録＝{R['word']['pick']}＝{R['word']['src']}）")
    if view == "faa" and g["lines"]:
        body = " ".join(g["lines"]).replace(" …", "").strip()
        need(R["faa"]["sentence"].startswith(body), f"② 英文が FAA の頁の一文と違う（原文のまま＝{R['faa']['src']}）")
        if g["hl"]:
            need(" ".join(g["hl"]) == R["faa"]["hl"], f"② 印を付けた句 {g['hl']} が記録の句と違う")
        # 🆕 試し焼き ep20_b6b：英文の1行目が頁の枠からはみ出した（layout は頁の枠を見ない）
        need(g["line_w"] <= g["page_w"], f"② 英文の行の幅 {g['line_w']:.0f} が頁の字の幅 {g['page_w']:.0f} からはみ出す")
    if view == "ans":
        need(len(g["q"]) == R["ans"]["n"], f"② 問いの数 {len(g['q'])}（冒頭の問いは {R['ans']['n']} つ）")
        if g["wait"]:
            need(g["wait"] == R["ans"]["wait"], f"② 3つ目の残りの札「{g['wait']}」（記録＝{R['ans']['wait']}）")
    if view == "hyd" and g.get("fuse"):
        no, x = g["fuse"]
        want_no, fin0, why = R["hyd_fuse"]
        need(no == want_no and x < fin0 and x < g["fin_x0"], f"② フューズ No.{no}・{x}m（記録＝No.{want_no} が垂直安定板の手前＝{why}）")
    if view == "alt" and g.get("band") is not None:
        need(abs(g["band"] - R["alt_band"][0]) < 1.0, f"② 帯の高さ {g['band']:.0f}フィート（記録 {R['alt_band'][0]:.0f}＝{R['alt_band'][1]}）")
    # ③ 札の数・時刻・推定
    said = [r.get("t", "") for r in m["rel"]]
    for t in texts:
        for mm in NUM_M19.finditer(t):
            tok = mm.group(0)
            need(any(tok in s for s in said), f"③ 札「{t}」の数「{tok}」が rel（記録の値の宣言）に無い")
            full = tok.replace("：", ":")
            if full.count(":") == 2:
                need(full in R["clock"], f"③ 札「{t}」の時刻「{tok}」が記録の時刻（{sorted(R['clock'])}）に無い")
    if view == "xpdr":
        need(not any(re.search(r"7700|77", t) for t in texts), "③ 番号（7700）を画面に書いた（台本の画の欄＝番号は書かず「緊急」の札）")
    fa, va = R["assume"].get(view, (None, None))
    if fa and any(s.get(fa) == va for s in seq):
        need(any("推定" in t for t in texts), "③ 推定で描いた段に「推定」の札が無い（報告書の推定＝ルール §5b-10）")
    fa, va = R["think"].get(view, (None, None))          # 🆕 ⑤b-6b：「考えられる」の段
    if fa and any(s.get(fa) == va for s in seq):
        need(any("考え" in t for t in texts), "③ 報告書が「考えられる」と書く段に「考え」の札が無い（言い切らない）")
    for r in m["rel"]:
        need(bool(r.get("src")), f"③ rel「{r.get('t')}」に出どころ（src）が無い")
    return bad, n


def _selftest_m20(ok):
    """20本目 ⑤b-5：模式図の検算（正しい場面・陽性対照＝描く側の表を壊す・筋と札）。"""
    import mech20 as M
    N = "模式"
    good = dict(
        seats=dict(view="seats", steps=[dict(state=dict(fe="on")), dict(state=dict(left="usual"))], note=N),
        seats_day=dict(view="seats", steps=[dict(state=dict(left="cop", right="cap")), dict(state=dict(cert="on"))], note=N),
        xpdr=dict(view="xpdr", steps=[dict(state=dict(ask="on", reply="on"), tag=dict(t="4桁の番号", at="code")),
                                      dict(state=dict(reply="emg"), tag=dict(t="緊急", at="emg"))],
                  rel=[dict(t="4桁", src="報告書 p6")], note=N),
        hyd=dict(view="hyd", start=dict(pipes="on", num="on"), steps=[dict(state=dict(cut="on"), tag=dict(t="4系統とも切れる（推定）", at="cut"))],
                 rel=[dict(t="4系統", src="報告書 p112")], note=N),
        thrust=dict(view="thrust", steps=[dict(state=dict(pwr="up", nose="up"), tag=dict(t="機首の上げ下げ（推定）", at="pwr")),
                                          dict(state=dict(top="on", diff="on", yaw="on"))], note=N),
        alt=dict(view="alt", steps=[dict(state=dict(pts="early", m1="on")), dict(state=dict(pts="all", m2="on"))], note=N),
        alt_final=dict(view="alt", start=dict(span="final"),
                       steps=[dict(state=dict(pts="all", m1="on", rate="on"), tag=dict(t="18:56:07", at="m1"))],
                       rel=[dict(t="18:56:07", src="報告書 p82")], note=N),
        gear=dict(view="gear", steps=[dict(state=dict(gear="down", flap="down"))], note=N),
        radio=dict(view="radio", steps=[dict(state=dict(link="on", ask="on")), dict(state=dict(stay="on"))], note=N),
        fix=dict(view="fix", start=dict(ray="on"), steps=[dict(state=dict(zoom="on", pa="on", pd="on", heli="on"))], note=N),
        press=dict(view="press", steps=[dict(state=dict(press="on", push="on"))], note=N),
        bag=dict(view="bag", steps=[dict(state=dict(bags="on", swell="on"))], note=N),
        apt=dict(view="apt", steps=[dict(state=dict(pick="on")), dict(state=dict(why="on")), dict(state=dict(ok="on"))], note=N),
        # 🆕 ⑤b-6
        fatigue=dict(view="fatigue", steps=[dict(state=dict(load="once")), dict(state=dict(load="rep", crack="on"))], note=N),
        rows=dict(view="rows", steps=[dict(state=dict(bars="on"), tag=dict(t="強さ（推定）", at="str"))], note=N),
        grow=dict(view="grow", steps=[dict(state=dict(two="on")), dict(state=dict(one="on")), dict(state=dict(same="on"))], note=N),
        fs=dict(view="fs", steps=[dict(state=dict(bay="on")), dict(state=dict(one="on"))], note=N),
        half=dict(view="half", steps=[dict(state=dict(half="on")), dict(state=dict(join="on"))], note=N),
        edge=dict(view="edge", steps=[dict(state=dict(good="on")), dict(state=dict(bad="on")), dict(state=dict(req="on"))], note=N),
        seal=dict(view="seal", steps=[dict(state=dict(seal="on")), dict(state=dict(eye="on"))], note=N),
        rear=dict(view="rear", steps=[dict(state=dict(l18="on")), dict(state=dict(all="on"))], note=N),
        clen=dict(view="clen", steps=[dict(state=dict(crack="on")), dict(state=dict(len="on"), tag=dict(t="亀裂の長さ（推定）", at="len"))],
                  note=N),
        prob=dict(view="prob", steps=[dict(state=dict(one="on")), dict(state=dict(many="on", q="on"))], note=N),
        two=dict(view="two", steps=[dict(state=dict(pick="on")), dict(state=dict(ok="on"))], note=N),
        lav=dict(view="lav", steps=[dict(state=dict(lav="on")), dict(state=dict(coat="on", bend="on"))], note=N),
        # 🆕 ⑤b-6b
        cab_half=dict(view="cab", start=dict(gauge="hi"), steps=[dict(state=dict(hole="on", gauge="lo")), dict(state=dict(half="on"))],
                      note=N),
        cab_flow=dict(view="cab", steps=[dict(state=dict(hole="on")), dict(state=dict(flow="near")), dict(state=dict(flow="all"))], note=N),
        cab_warm=dict(view="cab", steps=[dict(state=dict(warm="on", mask="on")), dict(state=dict(fog="on"))], note=N),
        flow=dict(view="flow", steps=[dict(state=dict(air="on")), dict(state=dict(seat="on"))], note=N),
        run=dict(view="run", steps=[dict(state=dict(wind="on")), dict(state=dict(eye="on"))], note=N),
        temp=dict(view="temp", steps=[dict(state=dict(drop="on")), dict(state=dict(pts="on"))], note=N),
        dect=dict(view="dect", steps=[dict(state=dict(j123="on")), dict(state=dict(b737="on"))], note=N),
        holes=dict(view="holes", steps=[dict(state=dict(j123="on", b737="on"))], note=N),
        sonar=dict(view="sonar", steps=[dict(state=dict(beam="on")), dict(state=dict(echo="on"))], note=N),
        dcam=dict(view="dcam", steps=[dict(state=dict(h="on")), dict(state=dict(w="on"))], note=N),
        rov=dict(view="rov", steps=[dict(state=dict(ask="on")), dict(state=dict(rov="on"))], note=N),
        res=dict(view="res", steps=[dict(state=dict(cell="on")), dict(state=dict(need="on"))], note=N),
        area=dict(view="area", steps=[dict(state=dict(day="on")), dict(state=dict(rep="on", nog="on", end="on"))], note=N),
        cover=dict(view="cover", steps=[dict(state=dict(cover="on")), dict(state=dict(strong="on"))], note=N),
        word=dict(view="word", steps=[dict(state=dict(pick="on")), dict(state=dict(mean="on"))], note=N),
        faa=dict(view="faa", steps=[dict(state=dict(body="on")), dict(state=dict(hl="on"))], note=N),
        ans=dict(view="ans", steps=[dict(state=dict(q3a="on")), dict(state=dict(q3b="on"))], note=N),
        hyd_fuse=dict(view="hyd", start=dict(pipes="on"), steps=[dict(state=dict(fuse="on")),
                                                                 dict(state=dict(fuse="stop"), tag=dict(t="働きを残せる（考えられている）", at="stop"))],
                      note=N),
        alt_band=dict(view="alt", start=dict(pts="all"), steps=[dict(state=dict(band="on"))], note=N),
        seats_hyp=dict(view="seats", start=dict(left="cop", right="cap"),
                       steps=[dict(state=dict(hyp="on"), tag=dict(t="判断力などがある程度低下", d="報告書の考え", at="judge"))], note=N))
    for nm, kw in good.items():
        bad, n = judge("m20", kw)
        ok &= not bad
        print(f"  {'OK' if not bad else '🔴 NG'} 20本目 正しい模式図（{nm}）: {'合格' if not bad else '🔴 ' + bad[0]}（{n}件）")
    # 陽性対照（描く側の表を壊す＝筋は正しいのに絵が記録と食い違う）
    for name, attr, val, key, kwk in (
            ("内側のエンジンを 13m に描く", "ENG_NO", {1: -21.15, 2: -13.0, 3: 12.07, 4: 21.15}, "横の位置", "hyd"),
            ("エンジンの番号を右から振る", "ENG_NO", {1: 21.15, 2: 12.07, 3: -12.07, 4: -21.15}, "左右", "hyd"),
            ("管を隔壁の前で切る", "HY_CUT", 50.0, "切れる所", "hyd"),
            ("この日の席を逆に書く", "SE_NAMES", dict(left=dict(usual="機長", cop="機長"), right=dict(cap="副操縦士")), "この日の席の名", "seats_day"),
            ("機関士の席を左に描く", "SE_FE", (840.0, 705.0), "航空機関士の席", "seats"),
            ("番号の枠を3桁に描く", "XP_DIGITS", 3, "番号の枠", "xpdr"),
            ("機首を下げる向きに回す", "TH_PITCH", -7.0, "機首が上がっていない", "thrust"),
            ("回す中心を機首から 40m に置く", "CG_X", 40.0, "回す中心", "thrust"),
            ("右が強い差で描く", "TH_DIFF", dict(strong=2.0, weak=9.0), "左を強く", "thrust"),
            ("付図-1 の点を1つ 1,000フィート高く描く", "AL_PTS",
             dict(M.AL_PTS, cruise=[(t, ft + (1000 if t == "18:31:08" else 0)) for t, ft in M.AL_PTS["cruise"]]), "記録の点に無い", "alt"),
            ("付図-1 の点を1つ落とす", "AL_PTS", dict(M.AL_PTS, cruise=M.AL_PTS["cruise"][:-1]), "しか描いていない", "alt"),
            ("18:40 の印を 18:38 に描く", "AL_MARK", dict(M.AL_MARK, cruise=dict(m1="18:25:21", m2="18:38:00")), "印 m2", "alt"),
            ("降下率の線を 12,000 で描く", "AL_RATE", 12000.0, "降下率の線", "alt_final"),
            ("主脚を前の脚の 20m 後ろに描く", "GE_MAIN_X", (26.4, 27.9), "前の脚と主脚", "gear"),
            ("フラップを脚と同時に動かす", "GE_FLAP_LAG", 0.0, "同時", "gear"),
            ("相手の名を取り違える", "RA_NAMES", dict(left="東京アプローチ", right="羽田"), "無線の相手の名", "radio"),
            ("方角を 300° で描く", "FX", dict(M.FX, brg=300.0), "方角と距離の線", "fix"),
            ("飛行機の扇を 4度で描く", "FX_PLANE", (4.0, 1.0), "plane の扇", "fix"),
            ("ヘリの扇を 0.2マイルで描く", "FX_HELI", (1.0, 0.2), "heli の扇", "fix"),
            ("隔壁を 55m に描く", "PR_BULK", 55.0, "隔壁の位置", "press"),
            ("山の上の袋をふくらませない", "BG_SWELL", 1.0001, "ふくらんでいない", "bag"),
            ("理由を「滑走路の長さ」と言い換える", "AP_WHY", ("空港の規模", "滑走路の長さ", "その他の施設環境"), "理由の言葉", "apt"),
            ("名古屋を大阪の西に置く", "AP_PTS", dict(M.AP_PTS, nagoya=(300.0, "名古屋空港", 136.924)), "空港の並び", "apt"),
            # 🆕 ⑤b-6（描く側が実際に使う表を壊す）
            ("ひびを穴の縁から離して描く", "FA_GAP", 30.0, "穴の縁", "fatigue"),
            ("ひびを引く力と同じ向きに描く", "FA_DIR", 90.0, "直角でない", "fatigue"),
            ("1列の所を2列で描く", "RW_ROWS", dict(a=(465.0, 525.0), b=(480.0, 510.0)), "列の数", "rows"),
            ("1列の所の強さを 0.8 で描く", "RW_STR", dict(a=1.0, b=0.8), "強さの棒の比", "rows"),
            ("速さの比を 1.6 で描く", "GR_RATIO", 1.6, "速さの比", "grow"),
            ("1列の所を第1〜第4ストラップに描く", "FS_ONE", (0, 3), "1列の所", "fs"),
            ("1ベイの亀裂がストラップをまたぐ", "FS_BAY_R", (0.70, 0.80), "1ベイの亀裂", "fs"),
            ("上半分を新しい物の色で描く", "HF_NEW", "up", "下半分でない", "half"),
            ("決まりを近すぎる穴より短く描く", "ED_REQ", 10.0, "余白の長さ", "edge"),
            ("シール材を板の端から離して描く", "SL_BEAD_DY", 30.0, "シール材", "seal"),
            ("目を客室の側に置く", "SL_EYE", (300.0, 610.0), "後ろの側", "seal"),
            ("目で見る範囲を円の6割に描く", "RE_ALL", 0.6, "後面全体", "rear"),
            ("見える長さを 7 にして描く", "CL_VIS", 7.0, "見える長さの比", "clen"),
            ("少なくとも1つの幅を 14〜50 で描く", "PB_MANY", (14.0, 50.0), "幅", "prob"),
            ("1つの亀裂を 20 で描く", "PB_ONE", 20.0, "1つの亀裂の確率", "prob"),
            ("正しい作りの壁に亀裂を描く", "TW_CRACKS", dict(a=3, b=9), "亀裂の印", "two"),
            ("化粧室を隔壁の後ろに描く", "LV", dict(M.LV, lav=(58.0, 60.5)), "化粧室", "lav"),
            # 🆕 ⑤b-6b（描く側が実際に使う表を壊す）
            ("天井の穴を 0.4m2 で描く", "CB_HOLE_A", 0.4, "穴の面積", "cab_half"),
            ("半球を半径1mで描く", "CB_R", 1.0, "半球の半径", "cab_half"),
            ("離れた所の矢印を穴の近くと同じ長さに描く", "CB_FAR", 150.0, "矢印の長さ", "cab_flow"),
            ("座席のあたりの矢印を天井の近くと同じ長さに描く", "FLW_SEAT", dict(M.FLW_SEAT, L=5.2), "座席のあたり", "flow"),
            ("走路を 80m で描く", "RN_M", 80.0, "走路の長さ", "run"),
            ("風を走る向きに描く", "RN_WIND_DX", 1.0, "風の向き", "run"),
            ("3分後の点を 15度に描く", "TP_PTS", ((2.0, 0.0), (3.0, 15.0), (5.0, 20.0)), "温度の点", "temp"),
            ("123便の幅を 1.7〜4秒で描く", "DT_J123", (1.7, 4.0), "123便の幅", "dect"),
            ("2009年の例を 3.5秒で描く", "DT_B737", 3.5, "2009年の例", "dect"),
            ("123便の穴を 1m2 で描く", "HL_A", dict(j123=1.0, b737=0.135), "穴の面積", "holes"),
            ("右の扇だけ広く描く", "SN_ANG", (28.0, 80.0), "対称", "sonar"),
            ("カメラを 3m の高さに描く", "DC_H", 3.0, "カメラの高さ", "dcam"),
            ("写る幅を 3m で描く", "DC_W", 3.0, "写る幅", "dcam"),
            ("1つの点を 1.5m で描く", "RS_CELL", (1.5, 1.3), "1つの点", "res"),
            ("見分けられる大きさを4点で描く", "RS_N", 4, "見分けられる大きさ", "res"),
            ("区域を 36km2 で描く", "AR_KM2", 36.0, "区域の広さ", "area"),
            ("1日の広さを 500日ぶんで描く", "AR_DAYS", 500.0, "日", "area"),
            ("点検口を隔壁の前に描く", "CV_HOLE", (55.0, 3.2), "点検口", "cover"),
            ("言葉の順を入れ替える", "WD_ROWS", (M.WD_ROWS[1], M.WD_ROWS[0]) + tuple(M.WD_ROWS[2:]), "言葉の使い分け", "word"),
            ("原因の言葉を「考えられる」の段にする", "WD_PICK", 2, "原因の言葉", "word"),
            ("英文を言い換える", "FA_LINES", ("During the bulkhead repair, the splice plate was cut and",
                                             "of a splice plate resulted in the Boeing repair crew",
                                             "dividing the plate and installing it in two pieces …"), "英文", "faa"),
            ("英文の1行目を長くして頁からはみ出す", "FA_LINES",
             ("During the bulkhead repair, difficulty in installation of a splice plate resulted in", "the Boeing repair crew",
              "dividing the plate and installing it in two pieces …"), "はみ出す", "faa"),
            ("3つ目を「分かった」と書く", "AN_WAIT", "分かった", "残りの札", "ans"),
            ("フューズを No.3 に描く", "HY_FUSE", (3, 56.0), "フューズ", "hyd_fuse"),
            ("フューズを垂直尾翼の中に描く", "HY_FUSE", (4, 62.0), "フューズ", "hyd_fuse"),
            ("帯を 18,000 フィートで描く", "AL_BAND", 18000.0, "帯の高さ", "alt_band")):
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            bad, _ = judge("m20", good[kwk])
        except Exception as e:                 # 壊した値で組めない＝その旨を出して落とす
            bad = [f"組めない {e!r}"]
        finally:
            setattr(M, attr, keep)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 20本目 陽性対照（画素）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    # 陽性対照（筋と札）
    for name, kw, key in (
            ("脚の前にフラップ", dict(view="gear", steps=[dict(state=dict(flap="down"))], note=N), "① 筋"),
            ("与圧の前に押す力", dict(view="press", steps=[dict(state=dict(push="on"))], note=N), "① 筋"),
            ("問いの前に「切り替えない」", dict(view="radio", steps=[dict(state=dict(link="on", stay="on"))], note=N), "① 筋"),
            ("推力を上げずに機首が上がる", dict(view="thrust", steps=[dict(state=dict(nose="up"))], note=N), "① 筋"),
            ("管が切れたのに推定の札が無い", dict(view="hyd", start=dict(pipes="on"), steps=[dict(state=dict(cut="on"), tag=dict(t="切れる", at="cut"))],
                                              note=N), "推定"),
            ("番号 7700 を画面に書く", dict(view="xpdr", steps=[dict(state=dict(ask="on", reply="emg"), tag=dict(t="7700", at="emg"))],
                                          rel=[dict(t="7700", src="報告書 p6")], note=N), "番号（7700）"),
            ("札の時刻が記録に無い（18:56:09）", dict(view="alt", start=dict(span="final"),
                                                  steps=[dict(state=dict(pts="all"), tag=dict(t="18:56:09", at="why"))],
                                                  rel=[dict(t="18:56:09", src="x")], note=N), "記録の時刻"),
            ("札の数が rel に無い", dict(view="press", steps=[dict(state=dict(press="on"), tag=dict(t="約7,300メートル", at="alt"))], note=N),
             "rel"),
            # 🆕 ⑤b-6
            ("くり返しの前にひびが伸びる", dict(view="fatigue", steps=[dict(state=dict(load="once", crack="on"))], note=N), "① 筋"),
            ("シール材の前に目", dict(view="seal", steps=[dict(state=dict(eye="on"))], note=N), "① 筋"),
            ("正しい壁を示す前に妥当の印", dict(view="two", steps=[dict(state=dict(ok="on"))], note=N), "① 筋"),
            ("強さの棒に推定の札が無い", dict(view="rows", steps=[dict(state=dict(bars="on"), tag=dict(t="強さ", at="str"))], note=N), "推定"),
            # 🆕 ⑤b-6b
            ("穴の前に流れの矢印", dict(view="cab", steps=[dict(state=dict(flow="near"))], note=N), "① 筋"),
            ("扇の前に跳ね返り", dict(view="sonar", steps=[dict(state=dict(echo="on"))], note=N), "① 筋"),
            ("判断力の霞に「考え」の札が無い", dict(view="seats", steps=[dict(state=dict(hyp="on"), tag=dict(t="判断力が低下", at="judge"))],
                                                note=N), "考え"),
            ("フューズが流れを止める段に「考え」の札が無い",
             dict(view="hyd", start=dict(pipes="on"), steps=[dict(state=dict(fuse="stop"), tag=dict(t="働きを残す", at="stop"))], note=N),
             "考え")):
        bad, _ = judge("m20", kw)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 20本目 陽性対照（筋と札）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    for nm, fn in (("切れた管を戻す", lambda: M.m20("hyd", [dict(state=dict(pipes="on", cut="on")), dict(state=dict(cut="off"))], note=N)),
                   ("段で高さの線の範囲を変える", lambda: M.m20("alt", [dict(state=dict(span="final"))], note=N)),
                   ("知らない欄", lambda: M.m20("seats", [dict(state=dict(door="on"))], note=N))):
        try:
            fn()
            g_ = False
        except ValueError:
            g_ = True
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 20本目 型の見張り：{nm}: {'組めない（止まった）' if g_ else '🔴 組めた'}")
    return ok


# ══════════════════════════════════════════════════════════
#  🆕 21本目 ⑤b-3（2026-10-12）：模式図（m21＝`tools/mech21.py`・15の見え方）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-14（22本目 ⑤b-1・§0b）：21本目の記録 REC_M21 の全項目（空港・基地・街の緯度経度 pts〈ボストン・ニューアーク・ダレス・ロサンゼルス・サンフランシスコ・ローム・オーティス・
#    ラングレー・ニューヨーク・首都・ハーンドン・ボルチモア・ホワイトハウス・ペンタゴン・レーガン・シャンクスビル・議事堂・アンドルーズ〉・正体不明の機の距離と方位・
#    シャンクスビルと首都の距離・受け持つ便の数・許可の連絡の順・撃ち落とすのに要ること・後ろの列・4便の出発と行き先と便の名・待機の2か所と NEADS・鳴った探知機の門・
#    4インチ・手順の段の順・間隔・前提の数・札に出してよい時刻・序文の調べの数・引き継いだ監察総監・記録装置の表・犠牲者の数と時点）は selftest の見本 `tools/fixture_ep21.py`
#    （GATES["check_mech"]・値は1つも変えていない＝git の `35fab37`）へ移した＝空。selftest は見本の表だけ差し込む（`fixture_ep21.apply(gate, tables_only=True)`）。
#    22本目で模式図 mech21 の型を使うときは、その回の記録の値をここに別に持つ（§5b-88＝描く側の表 mech21.MAP_PTS・ROUTES・NE_BASES・GT・BL_LIMIT_IN・CH_ORDER・ES_MILES・PM_T…を
#    書き換えると鳴る）。頁の番号の書き方（委員会報告＝印字の頁〈GPO の PDF＝印字＋18〉・序文は PDF の頁）と引いた原文は移した注の側にある＝fixture_ep21 の REC_M21 の注。
#    空のあいだ、m21 のカットは `judge_m21` が「記録の表が空」で止まる（fail closed＝KeyError にしない）。
#    ⚠️ **本番に残したもの（見本に入れていない）＝`_M21_NEED`（「先に起きることが先」の筋の表）と `NUM_M21`（札の数と時刻を拾う正規表現）**。判断の理由：
#       `_M21_NEED` は mech21 の見え方〈view〉と欄の名の約束（扉が開くのは鍵が外れてから・返信は届いてから・揺さぶりが止まるのは水平に戻ってから…）を並べた表で、
#       記録の値（時刻・数・座標・頁の照合）を1つも持たない＝型の側の規則。20本目の `judge_m20` の ① 筋が本番のコードにそのまま残っているのと同じ扱い
#       （筋は図の型の規則＝22本目も同じ見え方を使えば同じ約束が要る）。メッセージに入っている頁（p3・p13・p25 など）は理由の注で、照合には使っていない。
#       値を持つ表になったら（例：筋の中に時刻や数を並べ始めたら）、その行は見本へ移す。22本目で見え方を足すときは、その見え方の筋をこの表に足す
REC_M21 = {}
# 筋（先に起きることが先）＝(見え方, 欄, 値, 前に要る欄, 前に要る値の集合, 言葉)
_M21_NEED = (
    ("us", "routes", "on", "east", {"on"}, "4便の線は、出発の空港を見せてから"),
    ("us", "routes", "on", "west", {"on"}, "4便の線は、行き先の街を見せてから"),
    ("gate", "wand", "on", "ring", {"on"}, "手持ちの探知機は、門が鳴ってから（p3）"),
    ("gate", "pass_", "on", "wand", {"on"}, "通過は、手持ちの探知機のあと（p3）"),
    ("blade", "ok", "on", "limit", {"on"}, "持ち込めた印は、4インチの線を見せてから"),
    ("blade", "r2", "on", "r1", {"on"}, "理由の2つ目は1つ目のあと"),
    ("blade", "r3", "on", "r2", {"on"}, "理由の3つ目は2つ目のあと"),
    ("tools", "fake", "on", "bomb", {"on"}, "「おそらく偽物」は「爆弾」を見せてから（p13）"),
    ("door", "door", "open", "lock", {"open"}, "扉が開くのは、鍵が外れてから"),
    ("door", "comply", "on", "door", {"open"}, "「要求に従う」の矢印は、扉が開いてから"),
    ("door", "loose", "on", "lock", {"on", "open"}, "「守られていない」は、鍵の決まりを見せてから"),
    ("old", "b2", "on", "b1", {"on"}, "着陸の箱は、要求の箱のあと"),
    ("old", "b3", "on", "b2", {"on"}, "警察や軍の箱は、着陸の箱のあと"),
    ("old", "chips", "on", "b1", {"on"}, "要求の中身は、要求の箱を見せてから"),
    ("old", "long", "on", "b3", {"on"}, "「長引くほど」は、3つの箱を見せてから"),
    ("chain", "cape", "on", "short", {"on"}, "ケープコッドの施設は、近道の線の上"),
    ("escort", "dim", "on", "fighter", {"on"}, "間隔の線は、戦闘機を見せてから"),
    ("escort", "near", "on", "fighter", {"on"}, "「そばに寄せない」は、後ろの戦闘機を見せてから"),
    ("premise", "x1", "on", "p1", {"on"}, "1つ目の×は、1つ目を見せてから"),
    ("phone", "dur", "on", "call", {"on"}, "約25分は、電話の線を見せてから"),
    ("phone", "train", "on", "call", {"on"}, "訓練の線は、電話の線を見せてから"),
    ("radio", "garble", "on", "v1", {"on"}, "聞き取れないのは、声のあと"),
    ("radio", "v2", "on", "v1", {"on"}, "2つ目の声は、1つ目のあと"),
    ("radio", "know", "on", "v2", {"on"}, "乗っ取りと分かるのは、2つ目の声のあと（p19）"),
    ("call", "talk", "ask", "link", {"on"}, "行き来は、電話の線がつながってから"),
    ("call", "drill", "on", "link", {"on"}, "演習の札は、電話の線を見せてから"),
    ("scope", "search", "s1", "dots", {"on"}, "探す輪は、札の無い点を見せてから"),
    # 🆕 ⑤b-4
    ("scope", "code", "on", "block", {"on"}, "番号の変化は、札を見せてから"),
    ("scope", "ghost", "on", "blip", {"off"}, "記録に残っていた点は、画面の点が消えてから（p25）"),
    ("us", "stop", "on", "air", {"on"}, "離陸の停止は、空港の点を見せてから"),
    ("us", "aa", "ne", "air", {"on"}, "北東部の停止は、空港の点を見せてから"),
    ("us", "aa", "all", "air", {"on"}, "全米の停止は、空港の点を見せてから"),
    ("us", "land", "arrow", "fly", {"on"}, "降りる矢印は、空の機を見せてから"),
    ("us", "land", "down", "fly", {"on"}, "降りきるのは、空の機を見せてから"),
    ("ne", "mnh", "on", "f15", {"on"}, "マンハッタンへの矢印は、F-15 と沖の空域を見せてから"),
    ("ne", "look", "on", "r77", {"west", "east"}, "管制官が探した向きは、77便の線を見せてから"),
    ("ne", "reapp", "on", "r77", {"east"}, "東で戻る点は、東への線を見せてから（p25）"),
    ("ne", "turn", "on", "r77", {"east"}, "向きを変えた所は、東への線を見せてから"),
    ("dc", "follow", "on", "c130", {"on"}, "追う矢印は、輸送機を見せてから"),
    ("dc", "follow", "on", "t77", {"on"}, "追う矢印は、77便の線を見せてから"),
    ("soft", "cut", "on", "rec", {"on"}, "画面に出ないのは、レーダーが捉えてから（p25）"),
    # 🆕 ⑤b-5
    ("acars", "recv93", "on", "send", {"on"}, "93便に届くのは、警告を送り始めてから（p11 9:19→9:24）"),
    ("acars", "reply", "on", "recv93", {"on"}, "返信は、93便に届いてから（p11 9:24→9:26）"),
    ("ground", "back", "on", "calls", {"on"}, "機内に伝わるのは、電話の線を見せてから"),
    ("cvr", "v2", "on", "v1", {"on"}, "2つ目の叫びは、1つ目の声のあと（p14）"),
    ("cvr", "hl2", "on", "v2", {"on"}, "書き起こしの印は、2つ目の叫びを見せてから"),
    ("cmd", "plt", "on", "cap", {"on"}, "操縦士の側の札は、首都の側の札と並べて"),
    ("cmd", "neq", "on", "plt", {"on"}, "食い違いの印は、2つの札を見せてから"),
    ("need", "x", "on", "hl", {"on"}, "×は、3つを見せてから"),
    ("ne", "proj", "on", "r93", {"on"}, "首都への予測の線は、実際の93便の線を見せてから（p41）"),
    ("ne", "proj", "on", "shk", {"on"}, "首都への予測の線は、墜ちた所を見せてから（p41）"),
    ("sky", "adw", "on", "o2", {"on"}, "アンドルーズ基地は、2組目の戦闘機を見せてから"),
    ("sky", "o2", "on", "o1", {"on"}, "2組目の戦闘機は、ラングレーの戦闘機を見せてから（p44「another set」）"),
    ("cabin", "rear9", "on", "fones", {"on"}, "後ろの9列の枠は、座席の背の電話を見せてから"),
    ("cabin", "rush", "on", "vote", {"on"}, "前へ向かうのは、決をとってから（p13）"),
    ("roll", "calm", "on", "tilt", {"level"}, "揺さぶりが止まった印は、機が水平に戻ってから（p14）"),
    # 🆕 ⑤b-6
    ("us", "reopen", "on", "stop", {"on"}, "空がふたたび開くのは、離陸を止めたあと（p327）"),
    ("us", "reopen", "on", "air", {"on"}, "開いた空港は、空港の点を見せてから"),
    ("ig", "r1", "on", "dot", {"on"}, "運輸省の監察総監の答えは、運輸省の箱を見せてから"),
    ("ig", "r2", "on", "r1", {"on"}, "幹部2人の処分は、1つ目の答えのあと（CC-2006-085 p2→p3）"),
    ("fdr", "hl93", "on", "st", {"ok", "all"}, "93便の音声の印は、読めた記録装置を見せてから"),
    ("fdr", "okhl", "on", "st", {"ok", "all"}, "読めた所の印は、読めた記録装置を見せてから"),
    ("fdr", "use", "on", "st", {"ok", "all"}, "報告書への線は、読めた記録装置を見せてから"),
    ("fdr", "court", "on", "st", {"ok", "all"}, "裁判の証拠は、読めた記録装置を見せてから"),
    ("recom", "hl2", "on", "c2", {"on"}, "爆発物の勧告の印は、その箱を見せてから"),
    ("two", "k", "on", "hl", {"on"}, "「何を知ったか」は、空の側に印を付けてから"),
    ("toll", "diff", "on", "old", {"on"}, "数の差は、委員会の数を見せてから"),
    ("toll", "diff", "on", "now", {"on"}, "数の差は、いまの数を見せてから"),
)
NUM_M21 = re.compile(r"[0-9０-９]{1,2}[:：][0-9０-９]{2}(?:[:：][0-9０-９]{2})?|[0-9０-９][0-9０-９,.．]*")


def judge_m21(f):
    """21本目 模式図：①状態の筋 ②形（f.mech["geo"]）を記録（REC_M21）で ③札の数・時刻。"""
    bad, n = [], 0
    m = f.mech
    g, view = m["geo"], m["view"]
    seq = [m["start"]] + list(m["states"])
    R = REC_M21
    if not R:       # 🆕 22本目 ⑤b-1：記録の表が空のあいだは止める（KeyError で理由が見えなくならない＝fail closed。judge_m20 と同じ）
        return ["記録の表 REC_M21 が空（22本目の値を入れるまで、m21 のカットは止まる）"], 1
    texts = list(m["tags"])

    def need(cond, msg):
        nonlocal n
        n += 1
        if not cond:
            bad.append(msg)
    # ① 筋
    for v, fl, val, pre, ok_vals, msg in _M21_NEED:
        if v != view:
            continue
        for s in seq:
            if fl == "talk":
                hit = s.get(fl) in ("ask", "back")
            elif fl == "search":
                hit = s.get(fl) not in (None, "off")
            else:
                hit = s.get(fl) == val
            if hit:
                need(s.get(pre) in ok_vals, f"① 筋：{msg}")
    if view == "chain":
        for s in seq:
            need(s["hqx"] != "on" or int(s["lit"]) >= 3, "① 筋：本部の×は、本部まで灯してから")
    if view == "chain":
        for s in seq:
            need(s.get("reg", "off") == "off" or int(s["lit"]) >= 2, "① 筋：地域の管理職への矢印は、上司まで灯してから（p22）")
            need(s.get("hqq", "off") == "off" or int(s["lit"]) >= 3, "① 筋：本部の「？」は、本部まで灯してから（p29）")
    if view == "cmd":       # 🆕 ⑤b-5
        for s in seq:
            need(s["msg"] == "off" or int(s["lit"]) >= 3, "① 筋：文字の連絡は、NEADS まで灯してから（p42）")
            need(s["x"] == "off" or int(s["lit"]) >= 3, "① 筋：NEADS から先の×は、NEADS まで灯してから（p43）")
            need(s["x"] == "off" or int(s["lit"]) <= 3, "① 筋：戦闘機まで灯したのに×がある（p43＝NEADS は下へ流していない）")
    if view == "scope":
        for s in seq:
            need(s["who"] == "faa" or s["block"] == "off", "① 筋：便名と高度の札は管制の画面だけ（NEADS の画面は札の無い点）")
            need(s["who"] == "neads" or (s["dots"] == "off" and s["search"] == "off"), "① 筋：札の無い点を探すのは NEADS の画面")
            need(s["who"] == "faa" or (s["code"] == "off" and s["two"] == "off" and s["ghost"] == "off"),
                 "① 筋：番号の変化・2機・記録に残った点は管制（航空路）の画面")
            need(s["who"] == "app" or s["fast"] == "off", "① 筋：東へ速く動く札の無い点は空港の管制の画面（ダレス・p25）")
            need(s["who"] != "faa" or s["blip"] == "on" or s["block"] == "off", "① 筋：点が消えたのに札が残っている")
    # ② 形（記録）
    if view in ("us", "ne", "dc"):
        need(g["coast"] > 0, "② 陸の輪郭が無い（Natural Earth の切り出し ref/ep21/coast_ne50m.json）")
        for k, (la, lo) in g["back"].items():
            want = R["pts"].get(k)
            need(want is not None and abs(la - want[0]) < 0.05 and abs(lo - want[1]) < 0.05,
                 f"② 地点 {k} の位置（画素から {la:.3f}, {lo:.3f}）が記録の座標 {want} と違う")
        px_lon, px_lat, latc = g["k"]
        kx, ky = px_lon / (111.32 * math.cos(math.radians(latc))), px_lat / 110.57      # 1km あたりの画素（門番の側の式）
        need(abs(kx - ky) / ky < 0.02, f"② 東西と南北の縮尺がそろっていない（1km＝{kx:.4f}／{ky:.4f} 画素）")
    if view == "us":
        need(set(g["routes"]) == R["routes"], f"② 4便の出発と行き先 {sorted(g['routes'])} が記録（{R['src']} p4・p7・p8・p10）と違う")
        for k, want in R["flights"].items():
            got = set(re.split(r"[・、]", g["flights"].get(k, "")))
            need(got == want, f"② {k} の便 {sorted(got)} が記録 {sorted(want)} と違う")
        xs = g["pts"]
        need(min(xs[k][0] for k in ("bos", "ewr", "iad")) > max(xs[k][0] for k in ("lax", "sfo")), "② 出発の空港が行き先の街より東に無い")
    if view == "us":
        air = g["air"]
        for i, (pl, tg, k) in enumerate(g["fly"]):
            near = min(range(len(air)), key=lambda j: math.hypot(air[j][0] - pl[0], air[j][1] - pl[1]))
            need(near == k and math.hypot(tg[0] - air[k][0], tg[1] - air[k][1]) < 0.5,
                 f"② 空の機 {i} の降りる先（空港 {k}）が、いちばん近い空港（{near}）でない（{R['src']} p29「the nearest airport」）")
    if view == "ne":
        need(set(g["bases"]) == R["bases"], f"② 待機の2か所 {g['bases']} が記録（{R['src']} p17＝オーティス・ラングレー）と違う")
        need(g["neads"] == R["neads"], f"② NEADS の場所 {g['neads']}（記録＝ローム＝{R['src']} p17）")
        r7, P = g["r77"], g["pts"]
        need(r7["reapp"][0] > r7["lost"][0] + 10, f"② 77便の点が戻る所（x {r7['reapp'][0]:.0f}）が消えた所（x {r7['lost'][0]:.0f}）より東に無い（{R['src']} p25）")
        need(r7["turn"][0] < P["iad"][0] - 100, "② 77便が向きを変えた所が、ダレスより西に無い（p24・p25）")
        (lx, ly), (ex, ey), (bx, by) = P["langley"], g["lang_e"], P["bal"]
        need(ex > lx + 100 and abs(ey - ly) < 0.2 * (ex - lx), f"② ラングレーの戦闘機の線が東の海へ向いていない（{R['src']} p27「east over the ocean」）")
        need(by < ly - 50, "② 命令の向き（ボルチモア）がラングレーの北に無い（p27「north toward the Baltimore area」）")
        need(g["w105"][0] > P["nyc"][0] and g["w105"][1] > P["nyc"][1], "② 軍の空域がニューヨークの南東（ロングアイランドの沖）に無い（p20）")
        # 🆕 ⑤b-5：シャンクスビルと首都の距離（p30「125 miles」）・93便が向きを変えた所はシャンクスビルより西（p12「turn the aircraft around
        #   and head east」）・ニューアークより西
        px_lon, px_lat, latc = g["k"]
        (sx, sy), (dx_, dy_) = P["shk"], P["dc"]
        mi = math.hypot((sx - dx_) / px_lon * 111.32 * math.cos(math.radians(latc)), (sy - dy_) / px_lat * 110.57) / 1.609344
        need(abs(mi - R["shk_mi"]) < 10, f"② シャンクスビルと首都の距離 {mi:.0f}マイル（記録 {R['shk_mi']:g}マイル＝{R['src']} p30）")
        r9 = g["r93"]
        need(r9["turn"][0] < sx - 100 and r9["turn"][0] < P["ewr"][0] - 100,
             "② 93便が向きを変えた所が、シャンクスビルとニューアークより西に無い（p12「head east」）")
    if view == "dc":
        (wx, wy), (ux, uy) = g["pts"]["wh"], g["unk"]
        px_lon, px_lat, latc = g["k"]
        ekm = (ux - wx) / px_lon * 111.32 * math.cos(math.radians(latc))
        nkm = -(uy - wy) / px_lat * 110.57
        mi = math.hypot(ekm, nkm) / 1.609344
        brg = math.degrees(math.atan2(ekm, nkm)) % 360
        need(abs(mi - R["unk_mi"]) < 0.3, f"② 正体不明の機がホワイトハウスから {mi:.2f}マイル（記録 {R['unk_mi']:g}マイル＝{R['src']} p34）")
        need(R["unk_brg"][0] <= brg <= R["unk_brg"][1], f"② 正体不明の機の方位 {brg:.0f}度が南西でない（{R['src']} p34）")
    if view == "gate":
        need(g["arches"] == R["arches"], f"② 鳴った探知機の門 {g['arches']}台（記録 {R['arches']}台＝{R['src']} p3）")
    if view == "blade":
        cm = (g["limit_x"] - g["zero_x"]) / g["px_cm"]
        need(abs(cm - R["limit_in"] * 2.54) < 0.02, f"② 4インチの線 {cm:.2f}センチ（記録 {R['limit_in']}インチ＝{R['limit_in'] * 2.54:.2f}センチ＝{R['src']} p84）")
        need(g["blade_end_x"] < g["limit_x"], "② 刃物の刃が4インチの線を越えている（持ち込めた＝4インチ未満）")
    if view == "chain":
        need(tuple(g["order"]) == R["chain"], f"② 手順の段の順 {g['order']}（記録＝{R['src']} p17・p18）")
        ys = [y for _, y in g["xy"]]
        top = ys.index(min(ys))
        need(g["order"][top] == "国防長官の許し" and all(a > b for a, b in zip(ys[:top], ys[1:top + 1]))
             and all(a < b for a, b in zip(ys[top:], ys[top + 1:])), "② 段が「国防長官の許し」まで上がって NORAD から下りる形になっていない")
    if view == "escort":
        need((g["miles"], g["km"]) == R["escort"], f"② 間隔 {g['miles']}マイル・{g['km']}キロ（記録 {R['escort']}＝{R['src']} p18）")
        need(g["fighter_x"] < g["plane_x"], "② 戦闘機が乗っ取られた機の後ろ（進む向きの反対＝左）に無い")
    if view == "premise":
        need(len(g["boxes"]) == R["premise"], f"② 前提の数 {len(g['boxes'])}（記録 {R['premise']}＝{R['src']} p18）")
    # 🆕 ⑤b-5
    if view == "acars":
        need(g["planes"] == R["acars"], f"② 受け持つ便の数 {g['planes']}機（記録 {R['acars']}機＝{R['src']} p11）")
    if view == "cmd":
        need(tuple(g["order"]) == R["cmd"], f"② 許可の連絡の順 {g['order']}（記録＝{R['src']} p42）")
        need(all(a < b for a, b in zip(g["xs"], g["xs"][1:])), "② 許可の連絡の箱が左から右へ並んでいない")
    if view == "need":
        need(len(g["boxes"]) == R["need"], f"② 撃ち落とすのに要ることの数 {len(g['boxes'])}（記録 {R['need']}＝{R['src']} p45）")
    if view == "cabin" and g.get("plane") == "757":
        need(g["rear"] == R["rear"], f"② 座席の背の電話の列 {g['rear']}列（記録＝後ろの{R['rear']}列＝国立公園局）")
        need(tuple(g["seats"]) == (3, 3), f"② ボーイング757 の横の並び {g['seats']}（3-3）")
    # 🆕 ⑤b-6
    if view == "us" and any(s.get("reopen") == "on" for s in seq):
        need(0 < len(g["open"]) < g["n_air"], f"② 9月13日に開いた空港 {len(g['open'])}／{g['n_air']}（記録＝基準を満たした空港から＝全部ではない・p327）")
    if view == "probe":
        P_ = R["probe"]
        need(g["law"].startswith(P_["law"]), f"② 委員会をつくった法律の月「{g['law']}」（記録 {P_['law']}＝序文）")
        c = g["cards"]
        need(len(c) == 3 and c[0].startswith(P_["pages"]) and c[1].startswith(P_["people"]) and c[2].startswith(P_["countries"]),
             f"② 調べの数 {c}（記録＝文書 {P_['pages']}頁・{P_['people']}人・{P_['countries']}か国＝序文）")
        need(all("超える" in t for t in c[:2]), "② 文書と人の数に「超える」が無い（記録＝more than）")
    if view == "ig":
        need(tuple(g["igs"]) == R["igs"], f"② 引き継いだ先 {g['igs']}（記録＝国防総省と運輸省の監察総監＝CC-2006-085 p1）")
        m_ = re.search(r"幹部(\d+)人", g["r2"])
        need(bool(m_) and int(m_.group(1)) == R["ig_execs"], f"② 処分を求めた幹部の数「{g['r2']}」（記録 {R['ig_execs']}人＝CC-2006-085 p3）")
    if view == "fdr":
        need(g["table"] == R["fdr"], f"② 記録装置の表 {g['table']} が記録（{R['src']} p456）と違う")
        need(tuple(g["rows"]) == tuple(R["fdr"]), f"② 便の並び {g['rows']}")
    if view == "toll":
        nums = [int(re.sub(r"\D", "", t)) for t in g["nums"]]
        need(tuple(nums) == R["toll"], f"② 犠牲者の数 {nums}（記録＝委員会 {R['toll'][0]}＝p311・いま {R['toll'][1]}＝記念館）")
        need(R["toll_when"][0] in g["when"][0] and R["toll_when"][1] in g["when"][1], f"② 数の時点と出どころ {g['when']}")
        d_ = re.search(r"(\d+)人", g["diff"])
        need(bool(d_) and int(d_.group(1)) == R["toll"][1] - R["toll"][0], f"② 差の札「{g['diff']}」（記録の差 {R['toll'][1] - R['toll'][0]}人）")
    # ③ 札の数・時刻
    said = [r.get("t", "") for r in m["rel"]]
    for t in texts:
        for mm in NUM_M21.finditer(t):
            tok = mm.group(0)
            need(any(tok in s for s in said), f"③ 札「{t}」の数「{tok}」が rel（記録の値の宣言）に無い")
            full = tok.replace("：", ":")
            if ":" in full:
                need(full in R["clock"], f"③ 札「{t}」の時刻「{tok}」が記録の時刻（{sorted(R['clock'])}）に無い")
    for r in m["rel"]:
        need(bool(r.get("src")), f"③ rel「{r.get('t')}」に出どころ（src）が無い")
    return bad, n


def _selftest_m21(ok):
    """21本目 ⑤b-3：模式図の検算（正しい場面・陽性対照＝描く側の表を壊す・筋と札）。"""
    import mech21 as M
    N = "模式"
    good = dict(
        us=dict(view="us", steps=[dict(state=dict(east="on")), dict(state=dict(west="on", routes="on"))], note=N),
        ne=dict(view="ne", steps=[dict(state=dict(neads="on", bases="on"))], note=N),
        gate=dict(view="gate", steps=[dict(state=dict(ring="on")), dict(state=dict(wand="on", pass_="on"))], note=N),
        blade=dict(view="blade", steps=[dict(state=dict(limit="on", ok="on"), tag=dict(t="4インチ未満", at="ok"))],
                   rel=[dict(t="4インチ", src="委員会報告 p84")], note=N),
        chain=dict(view="chain", steps=[dict(state=dict(lit="3")), dict(state=dict(lit="7", hqx="on"))], note=N),
        escort=dict(view="escort", steps=[dict(state=dict(fighter="on", dim="on"), tag=dict(t="約8キロ（5マイル）", at="dim"))],
                    rel=[dict(t="約8キロ（5マイル）", src="委員会報告 p18")], note=N),
        premise=dict(view="premise", steps=[dict(state=dict(p1="on")), dict(state=dict(x1="on"))], note=N),
        scope=dict(view="scope", start=dict(block="on"), steps=[dict(tag=dict(t="8:21", at="time"))], rel=[dict(t="8:21", src="委員会報告 p18")],
                   note=N),
        # 🆕 ⑤b-4
        us2=dict(view="us", steps=[dict(state=dict(air="on", fly="on")), dict(state=dict(land="arrow")), dict(state=dict(land="down"))], note=N),
        ne2=dict(view="ne", steps=[dict(state=dict(r77="west", lang="on", f15="on")), dict(state=dict(r77="east", reapp="on"))], note=N),
        dc=dict(view="dc", steps=[dict(state=dict(unk="on"), tag=dict(t="約10キロ（6マイル）", at="unk", to="unk"))],
                rel=[dict(t="約10キロ（6マイル）", src="委員会報告 p34")], note=N),
        # 🆕 ⑤b-5
        acars=dict(view="acars", steps=[dict(state=dict(send="on"), tag=dict(t="9:19", at="time")), dict(state=dict(recv93="on")),
                                        dict(state=dict(reply="on"))], rel=[dict(t="9:19", src="委員会報告 p11")], note=N),
        cmd=dict(view="cmd", steps=[dict(state=dict(lit="3", msg="on")), dict(state=dict(x="on", cap="on", plt="on", neq="on"))], note=N),
        need=dict(view="need", steps=[dict(state=dict(hl="on")), dict(state=dict(x="on"))], note=N),
        cab757=dict(view="cabin", start=dict(plane="757"), steps=[dict(state=dict(fones="on", rear9="on", vote="on", rush="on"))], note=N),
        ne3=dict(view="ne", steps=[dict(state=dict(r93="on", shk="on")), dict(state=dict(proj="on", hits="on"))], note=N),
        dc2=dict(view="dc", steps=[dict(state=dict(tgt="on"))], note=N),
        sky=dict(view="sky", steps=[dict(state=dict(o1="on")), dict(state=dict(o2="on", adw="on"))], note=N),
        cvr=dict(view="cvr", steps=[dict(state=dict(v1="on")), dict(state=dict(v2="on", hl2="on", ap="on", phone="on"))], note=N),
        roll=dict(view="roll", steps=[dict(state=dict(tilt="left", rock="on")), dict(state=dict(tilt="level", calm="on"))], note=N),
        wall=dict(view="wall", steps=[dict(state=dict(block="on", rec="on", noise="on", q="on", down="on"))], note=N),
        ground=dict(view="ground", steps=[dict(state=dict(calls="on")), dict(state=dict(back="on"))], note=N),
        # 🆕 ⑤b-6
        us3=dict(view="us", start=dict(air="on", stop="on"), steps=[dict(state=dict(reopen="on"))], note=N),
        probe=dict(view="probe", steps=[dict(state=dict(law="on")), dict(state=dict(n="on"))], note=N),
        ig=dict(view="ig", steps=[dict(state=dict(dot="on")), dict(state=dict(r1="on")), dict(state=dict(r2="on"))], note=N),
        fdr=dict(view="fdr", steps=[dict(state=dict(st="ok")), dict(state=dict(st="all", hl93="on", okhl="on", use="on", court="on"))],
                 note=N),
        recom=dict(view="recom", steps=[dict(state=dict(c1="on")), dict(state=dict(c2="on", hl2="on"))], note=N),
        two=dict(view="two", steps=[dict(state=dict(hl="on")), dict(state=dict(k="on"))], note=N),
        toll=dict(view="toll", start=dict(now="on"), steps=[dict(state=dict(old="on")), dict(state=dict(diff="on", me="full"))], note=N),
        cover=dict(view="cover", steps=[dict(state=dict(web="on"))], note=N),
    )
    for nm, kw in good.items():
        bad, n = judge("m21", kw)
        g_ = not bad
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 21本目 正しい場面：{nm}（{n}件）" + (f"  ← {bad[0]}" if bad else ""))
    for name, attr, val, key, kwk in (
            ("ボストンの空港を2度北に描く", "MAP_PTS", dict(M.MAP_PTS, bos=(44.3656, -71.0096)), "地点 bos", "us"),
            ("93便をロサンゼルスへ結ぶ", "ROUTES", (("11便・175便", "bos", "lax"), ("77便", "iad", "lax"), ("93便", "ewr", "lax")),
             "出発と行き先", "us"),
            ("待機の基地をニューヨークにする", "NE_BASES", ("otis", "nyc"), "待機の2か所", "ne"),
            ("探知機の門を1台にする", "GT", dict(M.GT, arch=(560.0,)), "探知機の門", "gate"),
            ("4インチを4.5インチで描く", "BL_LIMIT_IN", 4.5, "4インチの線", "blade"),
            ("段の順を入れ替える", "CH_ORDER", ("ctl", "hq", "sup", "nmcc", "osd", "norad", "ftr"), "段の順", "chain"),
            ("間隔を4マイルにする", "ES_MILES", 4, "間隔", "escort"),
            ("前提を2つにする", "PM_T", M.PM_T[:2], "前提の数", "premise"),
            # 🆕 ⑤b-4
            ("77便の点を西で戻す", "R77", dict(M.R77, reapp=(38.5, -83.6)), "東に無い", "ne2"),
            ("ラングレーの線を北へ向ける", "NE_LANG_E", (39.9, -76.3), "東の海", "ne2"),
            ("軍の空域をニューヨークの北に置く", "NE_W105", (41.6, -73.0), "軍の空域", "ne2"),
            ("正体不明の機を5マイルに描く", "DC_UNK_MI", 5.0, "マイル", "dc"),
            ("正体不明の機を南東に描く", "DC_UNK_BRG", 135.0, "方位", "dc"),
            ("空の機を、近い空港でない方へ降ろす", "FLY", ((0, -1.6, 0.0),) + M.FLY[1:], "いちばん近い空港", "us2"),
            # 🆕 ⑤b-5
            ("受け持つ便を15機にする", "AC_N", 15, "受け持つ便の数", "acars"),
            ("許可の流れの NORAD と NEADS を入れ替える", "CM_T", (M.CM_T[0], M.CM_T[2], M.CM_T[1], M.CM_T[3]), "許可の連絡の順", "cmd"),
            ("要ることを2つにする", "ND_T", M.ND_T[:2], "要ることの数", "need"),
            ("電話の列を8列で描く", "CB_REAR", 8, "座席の背の電話の列", "cab757"),
            ("シャンクスビルを1.5度西に描く", "MAP_PTS", dict(M.MAP_PTS, shk=(40.0514, -80.4044)), "マイル", "ne3"),
            ("93便が向きを変えた所を東に描く", "R93", dict(M.R93, turn=(40.6, -76.0)), "向きを変えた所", "ne3"),
            # 🆕 ⑤b-6
            ("9月13日に全部の空港を開く", "AIR_OPEN", tuple(range(len(M.AIR_PTS))), "開いた空港", "us3"),
            ("文書を25万頁と書く", "PB_CARDS", (("読んだ文書", "25万頁を超える"),) + M.PB_CARDS[1:], "調べの数", "probe"),
            ("話を聞いた人の「超える」を落とす", "PB_CARDS", (M.PB_CARDS[0], ("話を聞いた人", "1,200人")) + M.PB_CARDS[2:], "超える", "probe"),
            ("処分を求めた幹部を3人と書く", "IG_T", dict(M.IG_T, r2=("正さなかった幹部3人", "処分の検討を求める")), "幹部の数", "ig"),
            ("77便の音声を「読めた」にする", "FD_ST", dict(M.FD_ST, **{"77便": ("ok", "ok")}), "記録装置の表", "fdr"),
            ("委員会の数を2,977人と書く", "TO_T", (("委員会の数", "（2004年7月）", "2,977人"),) + M.TO_T[1:], "犠牲者の数", "toll"),
            ("差を3人と書く", "TO_DIFF", "3人の差", "差の札", "toll")):
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            bad, _ = judge("m21", good[kwk])
        except Exception as e:                 # 壊した値で組めない＝その旨を出して落とす
            bad = [f"組めない {e!r}"]
        finally:
            setattr(M, attr, keep)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 21本目 陽性対照（画素）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    for name, kw, key in (
            ("近道の線の前にケープコッド", dict(view="chain", steps=[dict(state=dict(cape="on"))], note=N), "① 筋"),
            ("爆弾の前に「偽物」", dict(view="tools", steps=[dict(state=dict(fake="on"))], note=N), "① 筋"),
            ("1つ目の声の前に「聞き取れない」", dict(view="radio", steps=[dict(state=dict(garble="on"))], note=N), "① 筋"),
            ("NEADS の画面に便名の札", dict(view="scope", start=dict(who="neads", block="on"), steps=[dict()], note=N), "① 筋"),
            ("札の時刻が記録に無い（8:22）", dict(view="scope", steps=[dict(tag=dict(t="8:22", at="time"))], rel=[dict(t="8:22", src="x")], note=N),
             "記録の時刻"),
            ("札の数が rel に無い", dict(view="cabin", steps=[dict(tag=dict(t="全米で33人", at="n33"))], note=N), "rel"),
            # 🆕 ⑤b-4
            ("札の無い画面で番号が変わる", dict(view="scope", steps=[dict(state=dict(code="on"))], note=N), "① 筋"),
            ("東へ速く動く点を航空路の画面に", dict(view="scope", steps=[dict(state=dict(fast="on"))], note=N), "① 筋"),
            ("東への線の前に戻る点", dict(view="ne", steps=[dict(state=dict(r77="west", reapp="on"))], note=N), "① 筋"),
            ("空の機を見せずに降りる矢印", dict(view="us", steps=[dict(state=dict(air="on", land="arrow"))], note=N), "① 筋"),
            ("点が消えたのに札が残る", dict(view="scope", start=dict(block="on"), steps=[dict(state=dict(blip="off"))], note=N), "① 筋"),
            # 🆕 ⑤b-5
            ("警告を送る前に93便に届く", dict(view="acars", steps=[dict(state=dict(recv93="on"))], note=N), "① 筋"),
            ("灯す前に NEADS から先へ×", dict(view="cmd", steps=[dict(state=dict(x="on"))], note=N), "① 筋"),
            ("実際の93便の線の前に予測の線", dict(view="ne", steps=[dict(state=dict(shk="on", proj="on"))], note=N), "① 筋"),
            ("1つ目の声の前に2つ目の叫び", dict(view="cvr", steps=[dict(state=dict(v2="on"))], note=N), "① 筋"),
            ("傾いたまま「止まった」印", dict(view="roll", steps=[dict(state=dict(tilt="right", calm="on"))], note=N), "① 筋"),
            ("札の時刻が記録に無い（9:27）", dict(view="acars", steps=[dict(tag=dict(t="9:27", at="time"))], rel=[dict(t="9:27", src="x")],
                                         note=N), "記録の時刻"),
            # 🆕 ⑤b-6
            ("離陸を止めずに空港が開く", dict(view="us", start=dict(air="on"), steps=[dict(state=dict(reopen="on"))], note=N), "① 筋"),
            ("運輸省の箱の前に答え", dict(view="ig", steps=[dict(state=dict(r1="on"))], note=N), "① 筋"),
            ("読めた装置を見せずに裁判の証拠", dict(view="fdr", steps=[dict(state=dict(court="on"))], note=N), "① 筋"),
            ("委員会の数を見せずに差", dict(view="toll", start=dict(now="on"), steps=[dict(state=dict(diff="on"))], note=N), "① 筋")):
        bad, _ = judge("m21", kw)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 21本目 陽性対照（筋と札）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    for nm, fn in (("開いた扉を閉じる", lambda: M.m21("door", [dict(state=dict(lock="open", door="open")), dict(state=dict(door="closed"))], note=N)),
                   ("段で画面の持ち主を変える", lambda: M.m21("scope", [dict(state=dict(who="neads"))], note=N)),
                   ("知らない欄", lambda: M.m21("gate", [dict(state=dict(door="on"))], note=N)),
                   ("消えた点を戻す", lambda: M.m21("scope", [dict(state=dict(blip="off")), dict(state=dict(blip="on"))], note=N)),
                   ("降りた機を空へ戻す", lambda: M.m21("us", [dict(state=dict(fly="on", land="down")), dict(state=dict(land="arrow"))], note=N)),
                   ("段で電話の相手を変える", lambda: M.m21("phone", [dict(state=dict(to="family"))], note=N)),
                   # 🆕 ⑤b-5
                   ("段で機の型を変える", lambda: M.m21("cabin", [dict(state=dict(plane="757"))], note=N)),
                   ("段で首都の札の位置を変える", lambda: M.m21("ne", [dict(state=dict(dclab="se"))], note=N)),
                   ("灯した許可の流れを戻す", lambda: M.m21("cmd", [dict(state=dict(lit="3")), dict(state=dict(lit="1"))], note=N)),
                   # 🆕 ⑤b-6
                   ("記録装置の表を戻す", lambda: M.m21("fdr", [dict(state=dict(st="all")), dict(state=dict(st="ok"))], note=N)),
                   ("検視局の箱を戻す", lambda: M.m21("toll", [dict(state=dict(me="full")), dict(state=dict(me="on"))], note=N))):
        try:
            fn()
            g_ = False
        except ValueError:
            g_ = True
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 21本目 型の見張り：{nm}: {'組めない（止まった）' if g_ else '🔴 組めた'}")
    return ok


# ══════════════════════════════════════════════════════════
#  🆕 22本目 ⑤b-3b（2026-10-14）：模式図（m22＝`tools/mech22.py`・17の見え方）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-18（23本目 ⑤b-1・§0b）：22本目の記録 REC_M22 の全項目（富士山とタイタニックの深さ・3つの報告書の名と年月・横から見たタイタン〈全長・席・ボルト〉・職の席8・書類の英文〈免責・計画・
#    船級・点検・手紙・ブログほか〉・付録B の表27行〈元表 `_TW_ROWS`〉と深さの回数・付録A の吹き出し〈潜航・復旧・ニスキン・最後〉・深さの点・船首のまわりの向き・2つの装置・札に出してよい時刻・
#    第4〜7章〈送る間隔・手順・救助の手段・話した言葉・層・座屈・物差し・模型・船級・会議・亀裂・殻・矢印〉・第8〜9章〈カード・溝・クーポン・棚・80回目・監視のセンサー・音・研ぎ・2022年・画面の色の決まり〉・
#    第10〜11章・終章〈ターフ・要因8つ・所見・勧告6つ・温度・ストライク・列 cols・比べ cmp〉）と、その元表 `_TW_ROWS`（付録B の27行）は selftest の見本 `tools/fixture_ep22.py`
#    （GATES["check_mech"]・値は1つも変えていない＝git の `adbe2d5`）へ移した＝空。selftest は見本の表だけ差し込む（`fixture_ep22.apply(gate, tables_only=True)`）。
#    23本目で模式図 mech22 の型を使うときは、その回の記録の値をここに別に持つ（§5b-88＝描く側の表 mech22.FUJI_M・RP_T・SD_BOLTS・ORG・PP_DOC・APPB・APPA・DEPTH・BW_DIR・TW_SEABED…を
#    書き換えると鳴る）。頁の番号の書き方（USCG＝PDF の頁・NTSB＝1000＋PDF の頁・TSB＝節〈§1.3.1・§付録B〉）と引いた原文は移した注の側にある＝fixture_ep22 の REC_M22 の注。
#    空のあいだ、m22 のカットは `judge_m22` が「記録の表が空」で止まる（fail closed＝KeyError にしない。judge_m21 と同じ）。
#    ⚠️ **本番に残したもの（見本に入れていない）＝`_M22_NEED`（「先に起きることが先」の筋の表）と `NUM_M22`（札の数と時刻を拾う正規表現）・`_m22_min`・`cols_note_clash`**。判断の理由（`_M21_NEED` と同じ）：
#       `_M22_NEED` は mech22 の見え方〈view〉と欄の名の約束（水の重さを見せてから1円玉・外から締めるボルトを見せてから「出入りはここだけ」・浮きのタンクに水を入れてから台が沈む…）を並べた表で、
#       記録の値（時刻・数・座標・頁の照合）を持たない＝型の側の規則（メッセージの括弧の時刻〈9:04→9:05 など〉は理由の注で、照合には使っていない）。値を持つ表になったら、その行は見本へ移す。
#       23本目で見え方を足すときは、その見え方の筋をこの表に足す
REC_M22 = {}
_M22_NEED = (
    ("fuji", "coin", "on", "press", {"on"}, "1円玉と乗用車は、水の重さを見せてから"),
    ("side", "only", "on", "bolts", {"on"}, "「出入りはここだけ」は、外から締めるボルトを見せてから"),
    ("org", "ceo", "on", "seats", {"on"}, "CEO の席は、席を見せてから"),
    ("org", "all", "on", "ceo", {"on"}, "CEO から全部への線は、CEO の席を明るくしてから"),
    ("paper", "uscg", "on", "name", {"on"}, "米沿岸警備隊の見立ては、呼び名を見せてから"),
    ("dives", "dome", "on", "reach", {"on"}, "不具合の輪は、届いた回を見せてから"),
    ("lars_side", "lvl", "under", "fill", {"on"}, "台が沈むのは、浮きのタンクに水を入れてから（9:04→9:05）"),
    ("lars_side", "det", "on", "lvl", {"under"}, "切り離すのは、台が水面の下に沈んでから（9:05→9:14）"),
    ("comms", "dead", "on", "dead", {"on"}, ""),
    ("depth", "left", "on", "sea", {"on"}, "海の底までの括弧は、海の底を見せてから"),
    ("depth", "stop", "on", "upto", {"c"}, "止まった印は、最後の点まで描いてから"),
    ("bow", "jump", "on", "ese", {"on"}, "跳ぶ点は、潜水艇の知らせの点を見せてから"),
    ("two", "why", "on", "ca", {"on"}, "「理由は分からない」は、カナダの段を見せてから"),
    # 🆕 ⑤b-4（2026-10-15）
    ("send", "none", "on", "send", {"on"}, "「返事なし」は、母船の文を見せてから"),
    ("proto", "search", "on", "wait", {"on"}, "海面を探すのは、浮き上がるのを待ってから"),
    ("proto", "out", "on", "search", {"on"}, "外に知らせるのは、海面を探してから"),
    ("proto", "best", "on", "out", {"on"}, "海の上のならいは、会社の手順を見せてから"),
    ("layers", "rub", "on", "sep", {"on"}, "こすれた跡は、剥離の面を見せてから"),
    ("layers", "void", "on", "sep", {"on"}, "空隙は、剥離の面を見せてから"),
    ("buckle", "press", "on", "split", {"on"}, "押されて曲がるのは、薄い2枚に分かれてから"),
    ("ruler", "ratio", "on", "fail", {"on"}, "何倍かの箱は、壊れる深さを見せてから"),
    ("sf", "ratio", "on", "bars", {"on"}, "何倍かは、棒を見せてから"),
    ("sf", "spare", "on", "ratio", {"on"}, "余裕は、何倍かを見せてから"),
    ("model", "fail", "on", "press", {"on"}, "ドームが壊れるのは、圧をかけてから"),
    ("klass", "design", "on", "soc", {"on"}, "確かめる中身は、船級協会を見せてから"),
    ("klass", "cert", "on", "test", {"on"}, "証明書は、試験に立ち会ってから"),
    # 🆕 ⑤b-5（2026-10-15）
    ("cards", "loop", "on", "n", {"4"}, "くり返しの矢印は、4つの箱を明るくしてから"),
    ("groove", "cut", "on", "thick", {"on"}, "外側を削るのは、厚い端を見せてから"),
    ("shelf", "tube", "on", "std", {"on"}, "この筒の線は、基準の線を見せてから"),
    ("shelf", "spare", "on", "tube", {"on"}, "余裕は、この筒の線を見せてから"),
    ("d80", "bang", "on", "line", {"on"}, "音の印は、深さの線を描いてから"),
    ("d80", "who", "on", "bang", {"on"}, "聞いた人は、音の印を見せてから"),
    ("rtm", "dead", "on", "ae", {"on"}, "拾わなかったセンサーは、センサーを見せてから"),
    ("rtm", "squeeze", "on", "sg", {"on"}, "縮む矢印は、ひずみ計を見せてから"),
    ("ae", "jump", "on", "peak", {"on"}, "ひずみの跳びは、音の山を見せてから"),
    ("ae", "up", "on", "peak", {"on"}, "増え始めは、音の山を見せてから"),
    ("stime", "hard", "on", "on", {"on"}, "比べにくい印は、線を描いてから"),
    ("nonlin", "zones", "on", "bend", {"on"}, "浅い所と深い所の帯は、曲がった線を描いてから"),
    ("screen", "reset", "on", "lv", {"on"}, "ゼロへ戻る矢印は、色の決まりを見せてから"),
    # 🆕 ⑤b-6（2026-10-15）
    ("cols", "u8", "on", "u0", {"on"}, "主な要因8つは、主な原因を見せてから"),
    ("cols", "u7", "on", "u8", {"on"}, "7つ目の下線は、主な要因8つを見せてから"),
    ("cols", "ux", "on", "u8", {"on"}, "その他の要因は、主な要因8つを見せてから"),
    ("cols", "n2", "on", "n1", {"on"}, "寄与は、推定原因を見せてから"),
    ("cols", "n3", "on", "n2", {"on"}, "2つ目の寄与は、1つ目の寄与を見せてから"),
    ("cols", "t2", "on", "t1", {"on"}, "傷が積もったのは、強さを確かめなかったことを見せてから"),
    ("cols", "gap", "on", "ux", {"on"}, "監督の穴の枠は、米沿岸警備隊のその他の要因を見せてから"),
    ("cols", "gap", "on", "n2", {"on"}, "監督の穴の枠は、米運輸安全委員会の寄与を見せてから"),
    ("cols", "gap", "on", "tx", {"on"}, "監督の穴の枠は、カナダの危険の所見を見せてから"),
    ("risk", "three", "on", "line", {"on"}, "3つで中止は、ストライクの線を見せてから"),
    ("org", "vac", "on", "seats", {"on"}, "空いた席の枠は、席を見せてから"),
)
NUM_M22 = re.compile(r"[0-9０-９]{1,2}[:：][0-9０-９]{2}(?:[:：][0-9０-９]{2})?|[0-9０-９][0-9０-９,.．]*")


def _m22_min(t):
    p = [float(x) for x in t.split(":")]
    return p[0] * 60 + p[1] + (p[2] / 60 if len(p) > 2 else 0)


def judge_m22(f):
    """22本目 模式図：①状態の筋 ②形・表・色（f.mech["geo"]）を記録（REC_M22）で ③札の数・時刻。"""
    import jiko_style as J
    bad, n = [], 0
    m = f.mech
    g, view = m["geo"], m["view"]
    seq = [m["start"]] + list(m["states"])
    R = REC_M22
    if not R:       # 🆕 23本目 ⑤b-1：記録の表が空のあいだは止める（KeyError で理由が見えなくならない＝fail closed。judge_m21・judge_m20 と同じ）
        return ["記録の表 REC_M22 が空（23本目の値を入れるまで、m22 のカットは止まる）"], 1
    texts = list(m["tags"])

    def need(cond, msg):
        nonlocal n
        n += 1
        if not cond:
            bad.append(msg)
    for v, fl, val, pre, ok_vals, msg in _M22_NEED:
        if v != view or not msg:
            continue
        for s in seq:
            if s.get(fl) == val:
                need(s.get(pre) in ok_vals, f"① 筋：{msg}")
    if view == "fuji":
        Rf = R["fuji"]
        need(abs((g["fuji_y"] - g["y0"]) / g["px_m"] - Rf["fuji_m"]) < 3, f"② 富士山の頂の深さが記録 {Rf['fuji_m']:g}m（国土地理院）と違う")
        need(abs((g["titanic_y"] - g["y0"]) / g["px_m"] - Rf["depth_m"]) < 3, f"② タイタニックの深さが記録 {Rf['depth_m']:g}m（TSB §1.3）と違う")
        need(Rf["fuji_m"] < Rf["depth_m"] and g["fuji_y"] < g["titanic_y"], "② 富士山の頂がタイタニックの深さより深い")
        kgf = Rf["psi"] * 0.45359237 / (2.54 ** 2)                  # kgf／平方センチ
        ton = kgf * math.pi * (Rf["coin_mm"] / 20.0) ** 2 / 1000.0     # 1円玉（半径 1センチ）の面積にかかる力
        if any(s.get("coin") == "on" for s in seq):
            need(any(f"約{ton:.1f}トン" in t for t in texts), f"② 1円玉の札が記録の計算（約{ton:.1f}トン＝NTSB p10 の 5,554.5 psi）と合わない")
    if view == "reports":
        got = [(w, ym, c.lower()) for w, ym, c in g["order"]]
        want = [(w, ym, J.ROLE[r].lower()) for w, ym, r in R["reports"]]
        need(got == want, f"② 3つの報告書の名・年月・色 {got} が記録 {want} と違う")
    if view == "side":
        Rs = R["side"]
        need(abs(Rs["len_ft"] * 0.3048 - g["len_m"]) < 0.05 and abs(g["len_m"] - Rs["len_m"]) < 1e-6,
             f"② 全長 {g['len_m']}m が記録（{Rs['len_ft']:g}フィート＝NTSB p10）と違う")
        need(g["seats"] == Rs["seats"], f"② 乗れる人 {g['seats']}人（記録 {Rs['seats']}人＝TSB §1.2.1）")
        if any(s.get("bolts") == "on" for s in seq):
            need(g["bolts"] == Rs["bolts"], f"② ボルトの数 {g['bolts']}本（記録 {Rs['bolts']}本＝TSB 脚注39）")
        if any(s.get("dim") == "on" for s in seq):
            need(abs((g["xt"] - g["x0"]) - g["L"]) < 0.5, "② 全長の寸法が機首から尾部の先までになっていない")
    if view == "org":
        Ro = R["org"]
        need(len(g["seats"]) == Ro["n"], f"② 職の席 {len(g['seats'])}（記録 {Ro['n']}＝TSB §1.23 表4）")
        need({nm for nm, s in g["seats"] if s == "vacant"} == Ro["vacant"], f"② 空席 {[nm for nm, s in g['seats'] if s == 'vacant']}（記録＝技術部長だけ）")
        need(g["seats"][0][0] == Ro["first"], "② いちばん上の席が CEO でない")
        need(g["staff"] == Ro["staff"], f"② 社員の印 {g['staff']}（記録 {Ro['staff']}人＝TSB §1.23）")
        need(g["col"].lower() == J.ROLE["company"].lower(), "② 席の色が会社の役の色でない")
    if view == "paper":
        need(list(g["lines"]) == list(R["paper"][g["doc"]]), f"② 書類の句 {g['lines']} が記録と違う")
        need(g["death"] == R["paper"]["death"], f"② 「death」の数 {g['death']}（記録 {R['paper']['death']}＝USCG p71）")
    if view == "table":
        need(tuple(tuple(r) for r in g["rows"]) == R["appb"], "② 付録Bの表の行が記録（TSB 付録B 表B1）と違う")
    if view == "dives":
        rows = [r[:2] + (r[6],) for r in R["appb"]]
        need(list(g["rows"]) == rows, "② 点の並びの元の行が記録（付録B）と違う")
        yrs = {}
        for _, yr, _, _ in g["pts"]:
            yrs[yr] = yrs.get(yr, 0) + 1
        need(yrs == R["years"], f"② 年ごとの点の数 {yrs}（記録 {R['years']}）")
        deep = {R["appb"][i][0] for i in g["deep"]}
        need(deep == {r[0] for r in R["appb"] if r[1] == R["deep"]} and len(deep) == R["n_deep"],
             f"② 届いた回 {len(deep)}（記録 {R['n_deep']}回＝NTSB p14）")
        for k, dates in R["marks"].items():
            if any(s.get(k) == "on" for s in seq):
                got = {R["appb"][i][0] for i in g["marks"][k]}
                need(got == dates, f"② 不具合の輪 {k} の回 {sorted(got)}（記録 {sorted(dates)}）")
        need(g["lit"].lower() == J.ROLE["sub"].lower(), "② 届いた回の色が潜水艇の役の色でない")
    if view == "chat":
        need(tuple(tuple(r) for r in g["rows"]) == R["appa"][g["set"]], f"② 吹き出しの文 {g['set']} が記録（TSB 付録A）と違う")
        need(g["cols"]["T"].lower() == J.ROLE["sub"].lower() and g["cols"]["SST"].lower() == J.ROLE["ship"].lower(),
             "② 吹き出しの色が役の色（潜水艇＝白・母船＝水色）でない")
    if view == "depth":
        D = g["D"]
        for (t, mm, (x, y)), (tw, mw) in zip(g["pts"], R["depth"]):
            tt = D["t0"] + (x - D["x0"]) / (D["x1"] - D["x0"]) * (D["t1"] - D["t0"])
            dd = D["d0"] + (y - D["y0"]) / (D["y1"] - D["y0"]) * (D["d1"] - D["d0"])
            need(abs(tt - _m22_min(tw)) < 0.05 and abs(dd - mw) < 1.0, f"② 深さの点 {tw} {mw:g}m が画素から {tt:.2f}分・{dd:.0f}m（記録と違う）")
        need(len(g["pts"]) == len(R["depth"]), "② 深さの点の数が記録と違う")
        need(abs(g["seabed"] - R["seabed"]) < 1e-6 and tuple(g["gap"]) == R["gap"], "② 海の底・返事の無い間が記録と違う")
    if view == "bow":
        tx, ty = g["tip"]
        for k in ("ese", "ene"):
            x, y = g[k]
            brg = math.degrees(math.atan2(x - tx, -(y - ty))) % 360
            need(abs(brg - R["bow"][k]) <= 11.25, f"② {k} の方位 {brg:.1f}度が記録（{R['bow'][k]}度±11.25＝付録A）の外")
    if view == "two":
        need(g["seabed"] == R["two"]["seabed"] and f"約{R['two']['seabed']}メートル" in g["ca"][0],
             f"② 海の底までの残り「{g['ca'][0]}」（記録 約{R['two']['seabed']}メートル＝TSB §1.3.2）")
    if view == "lars_side":
        need(g["top"] + g["under"] > g["sea"], "② 沈んだ台が水面の下に無い")
    # 🆕 ⑤b-4（2026-10-15）：第4〜7章
    def rc(r):
        return J.ROLE[r] if r in J.ROLE else getattr(J, r)
    if view == "side" and any(s.get("crack") == "on" for s in seq):
        need(len(g["cracks"]) == R["crack"], f"② 亀裂の数 {len(g['cracks'])}（記録 {R['crack']}＝TSB §1.12.1）")
        need(all(g["cyl"][0] <= x <= (g["cyl"][0] + g["cyl"][1]) / 2 for x, _ in g["cracks"]), "② 亀裂が筒の前の半分に無い（記録＝forward）")
    if view == "send":
        rate = g["n"] / g["minutes"]
        need(R["send"]["lo"] <= rate <= R["send"]["hi"], f"② 文の印 1分に{rate:.1f}回（記録 1分に2〜3回＝NTSB p17）")
        d = [b - a for a, b in zip(g["xs"], g["xs"][1:])]
        need(max(d) - min(d) < 0.5, "② 文の印の間隔がそろっていない（模式＝同じ間隔）")
    if view == "proto":
        need(tuple(t for t, _ in g["boxes"]) == R["proto"], f"② 手順の箱 {[t for t, _ in g['boxes']]} が記録（USCG p39）と違う")
        need(all(c.lower() == rc(r).lower() for (_, c), r in zip(g["boxes"], R["proto_role"])), "② 手順の箱の色が役の色（会社＝橙）でない")
    if view == "none":
        need(tuple(g["items"]) == R["none"][g["set"]], f"② 欄 {g['items']} が記録と違う")
    if view == "say":
        role, bub = R["say"][g["set"]]
        need(tuple(tuple(b) for b in g["bubbles"]) == bub, f"② 吹き出しの英字 {g['set']} が記録（報告書が引く言葉）と違う")
        need(g["col"].lower() == rc(role).lower(), f"② 人の形の色が役の色（{role}）でない")
    if view == "layers":
        Rl = R["layers"]
        need(g["n"] == Rl["n"], f"② 層の数 {g['n']}（記録 {Rl['n']}枚＝NTSB p59）")
        need(set(g["sep"]) == Rl["sep"], f"② 剥離の面 {g['sep']}（記録 1と2・3と4＝NTSB p40）")
        need(set(g["void"]) == Rl["void"], f"② 空隙の面 {g['void']}（記録＝NTSB p59）")
        need(g["inner_y"] > g["outer_y"], "② 層1（いちばん内側＝NTSB p41）が下（内側）に無い")
        for t in texts:
            mm = re.search(r"約([0-9.]+)センチ", t)
            if mm:
                need(abs(float(mm.group(1)) - Rl["inch"] * 2.54) <= 0.05, f"② 札「{t}」が記録（1インチ＝2.54センチ）と違う")
    if view == "buckle":
        for r in g["rows"]:
            if r["split"] == "on":
                need(abs(r["th_out"] - g["th"] / 2) < 0.5 and r["gap"] > 0, "② 分かれた板が厚い1枚の半分の厚さになっていない（NTSB p61）")
            if r["press"] == "on":
                need(r["bow"] > 0 and g["inner_down"], "② 押された板が内側へ曲がっていない")
    if view == "tc":
        for side, (head, outward, (cx, cy), arrows) in g["sides"].items():
            want = R["tc"].get(head)
            for x1, y1, x2, y2 in arrows:
                need(want is not None and (math.hypot(x2 - cx, y2 - cy) > math.hypot(x1 - cx, y1 - cy)) == want,
                     f"② {head} の矢印の向きが記録と逆（引っ張りは中から外・深い海の殻は外から中＝USCG p274）")
    if view == "shell":
        need(g["left"][1] == R["shell"]["left"] and g["right"][1] == R["shell"]["right"], "② 殻の材料と形が記録（TSB §1.13）と違う")
    if view == "ruler":
        Rr = R["ruler"]
        px_m = (g["y1"] - g["y0"]) / g["dmax"]
        need(abs((g["titanic"][1] - g["y0"]) / px_m - Rr["titanic"]) < 1, f"② タイタニックの深さが記録 {Rr['titanic']:g}m と違う")
        for k, (mv, y) in g["marks"].items():
            if any(s.get(k) == "on" for s in seq):
                got = (y - g["y0"]) / px_m
                need(abs(got - Rr[k]) < 1, f"② 物差しの {k} が画素から {got:.0f}m（記録 {Rr[k]:g}m）")
                # 🆕 ⑤b-5：線の色＝その値を書いた調べの役（REC の ruler_role）。⑤b-4 の3本は会社
                need(g["cols"][k].lower() == rc(R["ruler_role"][k]).lower(), f"② 物差しの {k} の色が役の色（{R['ruler_role'][k]}）でない")
                # 🆕 ⑤b-5：線の札に書いた数＝記録の値（数は線の札そのものに書く＝別の深さの高さに数を並べない）
                mm = re.search(r"([0-9][0-9,]*)メートル", g["labs"][k])
                if mm:
                    need(abs(float(mm.group(1).replace(",", "")) - Rr[k]) < 1e-6, f"② 物差しの {k} の札「{g['labs'][k]}」の数が記録 {Rr[k]:g}m と違う")
        if any(s.get("ratio") == "on" for s in seq):
            need(g["ratio_n"] * Rr["titanic"] <= Rr["fail"] < (g["ratio_n"] + 1) * Rr["titanic"], "② 「何倍」の箱の数が記録の比と合わない")
            for t in texts:
                mm = re.search(r"([0-9]+)倍", t)
                if mm:
                    need(int(mm.group(1)) == g["ratio_n"], f"② 札「{t}」が箱の数と違う")
        for t in texts:
            if "安全率" in t:
                mm = re.search(r"([0-9]+\.[0-9]+)", t)
                need(bool(mm) and abs(float(mm.group(1)) - Rr["sf"]) < 1e-9, f"② 札「{t}」が安全率の目標（記録 {Rr['sf']}）と違う")
    if view == "sf":
        need(g["k"] > 1, "② 壊れる深さが潜ってよい深さより浅い（安全率は1より大きい）")
    if view == "model":
        need(abs(g["dome_m"] - R["model"]["dome_m"]) < 1e-6, "② ドームが壊れた深さが記録と違う")
        for t in texts:
            mm = re.search(r"約([0-9,]+)メートル", t)
            if mm:
                need(abs(float(mm.group(1).replace(",", "")) - R["model"]["dome_m"]) < 1e-6, f"② 札「{t}」が記録（約3,000メートル＝TSB §1.12.1）と違う")
    if view == "klass":
        need(tuple(g["chk"]) == R["klass"], f"② 船級の確かめの中身 {g['chk']} が記録（NTSB p22）と違う")
    if view == "meet":
        need(tuple(g["seats"]) == R["meet"], f"② 会合の席 {g['seats']}（記録＝CEO・運航部長・社員3人＝TSB §1.12.1）")
    # 🆕 ⑤b-5（2026-10-15）：第8〜9章
    if view == "cards":
        want = R["cards"].get(g["set"])
        need(want is not None and tuple(g["cards"]) == want, f"② 要点の箱 {g['set']} {g['cards']} が記録と違う")
        need(all(c.lower() == rc(r).lower() for c, (_, _, r) in zip(g["cols"], g["cards"])), "② 要点の箱の色が役の色でない")
        if g["set"] == "life":
            need(abs(g["life"] - R["life"]) < 1e-9 and any(f"{round(R['life'] * 100)}%" in b for _, b, _ in g["cards"]),
                 f"② 疲れの寿命の塗り {g['life']}（記録 {R['life']}＝TSB §1.16）")
    if view == "groove":
        Rg = R["groove"]
        need(abs(g["groove_px"] / g["px_cm"] - Rg["groove_in"] * 2.54) < 0.01, f"② 溝の幅が記録（{Rg['groove_in']}インチ＝NTSB p1043）と違う")
        need(abs(g["end_px"] / g["px_cm"] - Rg["end_in"] * 2.54) < 0.01, f"② 端の厚さが記録（{Rg['end_in']}インチ＝NTSB p1043）と違う")
        need(g["end_px"] > g["groove_px"], "② 端が溝より薄い（記録＝厚すぎて外側を削った）")
        for t in texts:
            mm = re.search(r"約([0-9.]+)センチ", t)
            if mm:
                need(abs(float(mm.group(1)) - Rg["end_in"] * 2.54) < 0.05, f"② 札「{t}」が端の厚さの記録（{Rg['end_in']}インチ）と違う")
    if view == "coupons":
        got = (sum(1 for k, _, _ in g["rects"] if k == "axial"), sum(1 for k, _, _ in g["rects"] if k == "circ"))
        need(got == R["coupons"], f"② 試料の数 {got}（記録 {R['coupons']}＝TSB §1.15）")
        need(all((h > w) == (k == "axial") for k, w, h in g["rects"]), "② 試料の向き（長さ＝縦長・周り＝横長）が逆")
        for t in texts:
            mm = re.search(r"(長さ|周り)の向き\s*([0-9]+)", t)
            if mm:
                need(int(mm.group(2)) == R["coupons"][0 if mm.group(1) == "長さ" else 1], f"② 札「{t}」が試料の数の記録と違う")
    if view == "shelf":
        Rs = R["shelf"]
        need(abs(g["req"] - Rs["req"]) < 1e-9 and abs(g["circ"] - Rs["circ"]) < 1e-9, f"② 安全率（基準 {g['req']}・周りの向き {g['circ']}）が記録と違う")
        need(tuple(g["labs"]) == (f"{round(g['load'] * Rs['req'])}キロまで", f"{round(g['load'] * Rs['circ'])}キロまで"),
             f"② 棚の札 {g['labs']} が安全率の比と合わない")
        need(abs((g["gy0"] - g["y_req"]) / g["px_kg"] - g["load"] * Rs["req"]) < 0.5
             and abs((g["gy0"] - g["y_circ"]) / g["px_kg"] - g["load"] * Rs["circ"]) < 0.5, "② 棚の線の高さが安全率の比と合わない")
    if view == "d80":
        D = g["D"]

        def _tm(x):
            return D["t0"] + (x - D["x0"]) / (D["x1"] - D["x0"]) * (D["t1"] - D["t0"])
        for (t, _m, (x, y)), (tw, mw) in zip(g["pts"], R["d80"]):
            dd = (y - D["y0"]) / (D["y1"] - D["y0"]) * D["d1"]
            need(abs(_tm(x) - _m22_min(tw)) < 0.05 and abs(dd - mw) < 1.0, f"② 80回目の深さの点 {tw} {mw:g}m が画素から {_tm(x):.2f}分・{dd:.0f}m")
        need(len(g["pts"]) == len(R["d80"]), "② 80回目の深さの点の数が記録と違う")
        bt, (bx, by) = g["bang"]
        need(bt == R["d80_bang"] and abs(_tm(bx) - _m22_min(bt)) < 0.05 and abs(by - D["y0"]) < 0.5,
             f"② 大きな音の印が記録の時刻（{R['d80_bang']}＝USCG p283）か海面の線に無い")
    if view == "rtm":
        Rr = R["rtm"]
        need(len(g["ae"]) == Rr["ae"] and sum(1 for d in g["ae"] if d) == Rr["dead"] and g["sg"] == Rr["sg"],
             f"② 監視装置の数（センサー {len(g['ae'])}・拾わず {sum(1 for d in g['ae'] if d)}・ひずみ計の場所 {g['sg']}）が記録（NTSB p1031・p1051）と違う")
    if view == "ae":
        Ra = R["ae"]
        need((g["up"], g["esc"], g["peak"], tuple(g["band"])) == (Ra["up"], Ra["esc"], Ra["peak"], Ra["band"]),
             "② 音の記録の時刻が記録（USCG p283・NTSB p1052）と違う")
        need(abs(g["jump_x"] - g["peak_x"]) < 0.5, "② ひずみの跳びが音の山と同じ時刻に無い（USCG p286「coincided」）")
        D = g["D"]
        for t, x in g["x_of"].items():
            tt = D["t0"] + (x - D["x0"]) / (D["x1"] - D["x0"]) * (D["t1"] - D["t0"])
            need(abs(tt - _m22_min(t)) < 0.02, f"② 音の記録の {t} が画素から {tt:.2f}分")
    if view == "ctrl":
        need(g["plain"][0] != g["plain"][1] and g["flip"][0] == g["flip"][1], "② そのまま＝向きが逆・逆さに持つ＝そろう、になっていない（USCG p235）")
    if view == "stime":
        d = g["dives"]
        need(len(d) >= 2 and all(a[1] < b[0] for a, b in zip(d, d[1:])), "② 潜航ごとの線が横に並んでいない（NTSB p1051）")
    if view == "nonlin":
        st_, bent = g["straight"], g["bent"]
        k0 = (st_[1][0] - st_[0][0]) / (st_[1][1] - st_[0][1])
        k1 = (bent[-1][0] - bent[-2][0]) / (bent[-1][1] - bent[-2][1])
        need(abs(k0 - k1) < 1e-6, "② 深い所の線がまっすぐな線と平行でない（NTSB p1059＝深い所はまとまって動く）")
        need(any(abs(x - (st_[0][0] + k0 * (y - st_[0][1]))) > 5 for x, y in bent if y <= g["gy0"] + g["sh"]),
             "② 浅い所で線が曲がっていない（NTSB p1059）")
        need(g["gauge_x"] < g["cyl"][0] + (g["cyl"][1] - g["cyl"][0]) * 0.1, "② ひずみ計が筒の前の端に無い（NTSB p1059）")
    if view == "screen":
        need((g["y"], g["r"]) == (R["screen"]["y"], R["screen"]["r"]), f"② 画面の決まり（黄 {g['y']}・赤 {g['r']}）が記録（NTSB p1031）と違う")
    if view == "layers" and any(s.get("grind") == "on" for s in seq):
        need(g["grind"] == R["grind"], f"② 削ったしわの数 {g['grind']}（記録 {R['grind']}＝USCG 図143）")
    if view == "dives" and any(s.get("y22") == "on" for s in seq):
        Ry = R["year22"]
        rows = [r for r in R["appb"] if r[0].startswith(g["year"])]
        need(g["year"] == Ry["year"] and len(rows) == Ry["n"] and sum(1 for r in rows if r[1] == R["deep"]) == Ry["deep"],
             f"② 残した年 {g['year']}（記録 {Ry['year']}年＝{Ry['n']}回のうち{Ry['deep']}回）")
        for t in texts:
            mm = re.search(r"([0-9]+)回のうち([0-9]+)回", t)
            if mm:
                need((int(mm.group(1)), int(mm.group(2))) == (Ry["n"], Ry["deep"]), f"② 札「{t}」が記録（USCG p235）と違う")
    if view == "bow" and any(s.get("hit") == "on" for s in seq):
        tx, ty = g["tip"]
        hx, hy = g["hit"]
        need(hx < tx - g["w"] * 0.8 and ty < hy < ty + 400, "② ぶつかった印が左舷の船首（北が上の左の縁）に無い（TSB 付録B「port bow」）")
    # 🆕 ⑤b-6（2026-10-15）：第10〜11章・終章
    if view == "temp":
        Rt = R["temp"]
        need((g["hi"], g["lo"]) == (Rt["hi"], Rt["lo"]), f"② 気温の平均（最高 {g['hi']}・最低 {g['lo']}）が記録（TSB §1.22）と違う")
        for k in ("hi", "lo"):
            got = (g["y0"] - g[f"y_{k}"]) / g["px_deg"]
            need(abs(got - Rt[k]) < 0.01, f"② 気温の印 {k} が画素から {got:.2f}°（記録 {Rt[k]}°）")
        for t in texts:
            need("℃" not in t, f"② 札「{t}」に ℃（記録は「°」だけ＝摂氏は推測）")
            mm = re.search(r"([−-]?)([0-9.]+)°", t)
            if mm:
                v = float(mm.group(2)) * (-1 if mm.group(1) else 1)
                need(v in (Rt["hi"], Rt["lo"]), f"② 札「{t}」の気温が記録（{Rt['hi']}°・{Rt['lo']}°）に無い（符号を含めて）")
    if view == "risk":
        Rk = R["risk"]
        need((g["day"], g["strike"], g["n"]) == (Rk["day"], Rk["strike"], Rk["n"]),
             f"② 危険度（この日 {g['day']}・線 {g['strike']}・{g['n']}つで中止）が記録（TSB §1.17.12.1・USCG p78）と違う")
        for k, v in (("x_day", Rk["day"]), ("x_line", Rk["strike"])):
            got = (g[k] - g["x0"]) / g["px"]
            need(abs(got - v) < 0.01, f"② 危険度の {k} が画素から {got:.2f}（記録 {v}）")
    if view == "cols":
        Rc = R["cols"]
        need([(nm, c.lower()) for nm, c in g["heads"]] == [(nm, rc(r).lower()) for nm, r in Rc["heads"]], f"② 列の名と色 {g['heads']} が記録と違う")
        need(tuple(g["tiers"]) == Rc["tiers"], f"② 段の名 {g['tiers']} が記録と違う")
        need(g["items"] == Rc["items"], "② 3列の札（字・列・段・役）が記録（USCG p5・p7・p8・NTSB p1074・TSB §3.1・§3.2）と違う")
        for f_, (_c, _tier, items) in Rc["items"].items():
            need([c.lower() for c in g["cols"].get(f_, [])] == [rc(r).lower() for _t, r in items], f"② 札 {f_} の色が主語の役の色でない")
        need(tuple(g["gap"]) == Rc["gap"] and tuple(g["u7"]) == Rc["u7"], "② 監督の穴の札か7つ目の下線の場所が記録と違う")
        need(not any(re.search(r"[0-9０-９]", t) for _c, _tier, items in g["items"].values() for t, _r in items), "② 3列の札に数字がある（数は字幕）")
        bad_bot = cols_note_clash(g["bot"], g["note_y"])
        need(not bad_bot, bad_bot)
    if view == "cmp":
        Rv = R["cmp"]
        need([(nm, c.lower()) for nm, c in g["heads"]] == [(nm, rc(r).lower()) for nm, r in Rv["heads"]], f"② 列の名と色 {g['heads']} が記録と違う")
        need(tuple(g["rows"]) == Rv["rows"], "② 並べの行が記録と違う")
    if view == "layers" and any(s.get("ice") == "on" for s in seq):
        need(abs(g["ice"]["top"] - g["ice"]["outer"]) < 0.5, "② 凍る水のすき間が外側（海の側）の面から始まっていない")
    if view == "org" and any(s.get("vac") == "on" for s in seq):
        vx, _vy = g["vac_xy"]
        need(abs(g["eng"][0] - vx) < 0.5, "② 「未定」の線の先が空いた席に無い")
    said = [r.get("t", "") for r in m["rel"]]
    for t in texts:
        for mm in NUM_M22.finditer(t):
            tok = mm.group(0)
            need(any(tok in s for s in said), f"③ 札「{t}」の数「{tok}」が rel（記録の値の宣言）に無い")
            full = tok.replace("：", ":")
            if ":" in full:
                need(full in R["clock"], f"③ 札「{t}」の時刻「{tok}」が記録の時刻（{sorted(R['clock'])}）に無い")
    for r in m["rel"]:
        need(bool(r.get("src")), f"③ rel「{r.get('t')}」に出どころ（src）が無い")
    return bad, n


def cols_note_clash(bot, note_y, cap=26, margin=8):
    """🆕 2026-10-15（22本目 ⑤c'）：cols の列の箱の下の端が、下の注の行（基準 note_y・字 cap）の字の上の端より margin 以上離れているか。
    重なれば理由の文字列・離れていれば空。22本目 ⑤c' で米沿岸警備隊の列に1行足したら箱が 42px 伸び（下の端 886）、注の行に重なった
    ＝周2 の 640px で見つけた（layout・geom_gap は鳴らなかった＝箱の線と注の字を比べていない）"""
    top = note_y - round(cap * 0.9)
    worst = max(bot)
    return "" if worst + margin <= top else f"② 列の箱の下の端 {worst:.0f} が注の行の字の上の端 {top}（−{margin}px）に届く＝箱が注に重なる"


def _selftest_m22(ok):
    """22本目 ⑤b-3b：模式図の検算（正しい場面・陽性対照＝描く側の表を壊す・筋と札）。"""
    import mech22 as M
    N = "模式"
    # 🆕 ⑤c'（10-15）：列の箱と注の行（陰性＝今の列・陽性＝直す前に1行足した 886）
    for nm, b, want_bad in (("陰性対照：今の3列の箱（下の端 844）", [844.0, 684.0, 642.0], False),
                            ("🔴 陽性対照：米沿岸警備隊の列に1行足して下の端 886", [886.0, 684.0, 642.0], True)):
        got_bad = bool(cols_note_clash(b, M.F.BY1 - 6))
        ok &= got_bad == want_bad
        print(f"  {'OK' if got_bad == want_bad else '🔴 NG'} 22本目 {nm}: {'不合格' if got_bad else '合格'}（{'不合格' if want_bad else '合格'}のはず）")
    good = dict(
        fuji=dict(view="fuji", steps=[dict(state=dict(press="on")), dict(state=dict(coin="on"), tag=dict(t="約1.2トン", at="t"))],
                  rel=[dict(t="約1.2トン", src="NTSB p1010")], note=N),
        reports=dict(view="reports", steps=[dict(state=dict(r1="on", r2="on", r3="on"))], note=N),
        side=dict(view="side", steps=[dict(state=dict(dim="on")), dict(state=dict(bolts="on", only="on"))], note=N),
        org=dict(view="org", steps=[dict(state=dict(seats="on")), dict(state=dict(ceo="on", all="on", staff="on"))], note=N),
        paper=dict(view="paper", start=dict(doc="waiver"), steps=[dict(state=dict(hl1="on", n9="on"))], note=N),
        table=dict(view="table", steps=[dict(state=dict(yr="on"))], note=N),
        dives=dict(view="dives", steps=[dict(state=dict(reach="on")), dict(state=dict(dome="on", batt="on", thr="on", wt="on", com="on"))], note=N),
        chat=dict(view="chat", start=dict(set="niskin"), steps=[dict(state=dict(n="8"))], note=N),
        depth=dict(view="depth", steps=[dict(state=dict(upto="c", sea="on", left="on", stop="on"))], note=N),
        depth_end=dict(view="depth", start=dict(z="end", upto="c"), steps=[dict(state=dict(stop="on"))], note=N),
        bow=dict(view="bow", steps=[dict(state=dict(ese="on", ene="on")), dict(state=dict(jump="on"))], note=N),
        two=dict(view="two", steps=[dict(state=dict(us="on", ca="on")), dict(state=dict(why="on"))], note=N),
        lars=dict(view="lars_side", steps=[dict(state=dict(fill="on", lvl="under")), dict(state=dict(det="on"))], note=N),
        # 🆕 ⑤b-4（2026-10-15）
        crack=dict(view="side", steps=[dict(state=dict(crack="on"))], note=N),
        send=dict(view="send", steps=[dict(state=dict(send="on")), dict(state=dict(none="on"))], note=N),
        proto=dict(view="proto", steps=[dict(state=dict(wait="on")), dict(state=dict(search="on", out="on")), dict(state=dict(best="on"))], note=N),
        none=dict(view="none", start=dict(set="told"), steps=[dict(state=dict(n="3"))], note=N),
        say=dict(view="say", start=dict(set="tv"), steps=[dict(state=dict(n="1")), dict(state=dict(n="2"))], note=N),
        layers=dict(view="layers", steps=[dict(state=dict(sep="on"), tag=dict(t="約2.5センチ", at="th")), dict(state=dict(void="on", rub="on"))],
                    rel=[dict(t="約2.5センチ", src="NTSB p1059")], note=N),
        buckle=dict(view="buckle", steps=[dict(state=dict(split="on")), dict(state=dict(press="on"))], note=N),
        tc=dict(view="tc", steps=[dict(state=dict(air="on", sea="on"))], note=N),
        shell=dict(view="shell", steps=[dict(state=dict(left="on", right="on"))], note=N),
        ruler=dict(view="ruler", start=dict(z="far", goal="on"),
                   steps=[dict(state=dict(fail="on")), dict(state=dict(ratio="on"), tag=dict(t="3倍あまり", at="dl"))],
                   rel=[dict(t="3倍あまり", src="NTSB p1025")], note=N),
        ruler_sf=dict(view="ruler", steps=[dict(state=dict(goal="on"), tag=dict(t="安全率の目標 2.25", at="sf"))],
                      rel=[dict(t="2.25", src="TSB §1.12.1")], note=N),
        model=dict(view="model", steps=[dict(state=dict(press="on")), dict(state=dict(fail="on"), tag=dict(t="ドーム", d="約3,000メートル相当", at="r2"))],
                   rel=[dict(t="約3,000メートル", src="TSB §1.12.1")], note=N),
        klass=dict(view="klass", steps=[dict(state=dict(soc="on", design="on")), dict(state=dict(test="on", cert="on"))], note=N),
        meet=dict(view="meet", steps=[dict(state=dict(rec="on"))], note=N),
        paper_mts=dict(view="paper", start=dict(doc="mts"), steps=[dict(state=dict(hl1="on", hl5="on"))], note=N),
        # 🆕 ⑤b-5（2026-10-15）
        cards=dict(view="cards", start=dict(set="views"), steps=[dict(state=dict(n="2")), dict(state=dict(n="3"))], note=N),
        cure=dict(view="cards", start=dict(set="cure"), steps=[dict(state=dict(n="4", loop="on"))], note=N),
        life=dict(view="cards", start=dict(set="life"), steps=[dict(state=dict(n="2"))], note=N),
        groove=dict(view="groove", steps=[dict(state=dict(thick="on"), tag=dict(t="端材 約13.1センチ", at="w")), dict(state=dict(cut="on"))],
                    rel=[dict(t="約13.1センチ", src="NTSB p1043")], note=N),
        coupons=dict(view="coupons", steps=[dict(state=dict(cut="on"), tag=[dict(t="長さの向き 9", at="a"), dict(t="周りの向き 9", at="c")])],
                     rel=[dict(t="9", src="TSB §1.15")], note=N),
        shelf=dict(view="shelf", steps=[dict(state=dict(load="on", std="on")), dict(state=dict(tube="on", spare="on"))], note=N),
        d80=dict(view="d80", steps=[dict(state=dict(line="on", bang="on")), dict(state=dict(who="on"))], note=N),
        rtm=dict(view="rtm", steps=[dict(state=dict(ae="on", sg="on")), dict(state=dict(squeeze="on", dead="on"))], note=N),
        ae=dict(view="ae", steps=[dict(state=dict(peak="on")), dict(state=dict(jump="on", up="on", band="on"), tag=dict(t="15:15〜15:30ごろ", at="band"))],
                rel=[dict(t="15:15〜15:30", src="NTSB p1052")], note=N),
        ctrl=dict(view="ctrl", steps=[dict(state=dict(flip="on"))], note=N),
        stime=dict(view="stime", steps=[dict(state=dict(on="on")), dict(state=dict(hard="on"))], note=N),
        nonlin=dict(view="nonlin", steps=[dict(state=dict(bend="on", zones="on")), dict(state=dict(fwd="on"))], note=N),
        screen=dict(view="screen", steps=[dict(state=dict(lv="on")), dict(state=dict(mute="on", reset="on"))], note=N),
        grind=dict(view="layers", steps=[dict(state=dict(grind="on"))], note=N),
        dives22=dict(view="dives", steps=[dict(state=dict(y22="on")), dict(state=dict(reach="on"), tag=dict(t="13回のうち7回", at="t"))],
                     rel=[dict(t="13回のうち7回", src="USCG p235")], note=N),
        bowhit=dict(view="bow", steps=[dict(state=dict(hit="on"))], note=N),
        ruler_mid=dict(view="ruler", start=dict(z="mid"), steps=[dict(state=dict(test="on", w650="on", w1k="on"))], note=N),
        paper_u80=dict(view="paper", start=dict(doc="u80"), steps=[dict(state=dict(hl1="on", hl3="on"))], note=N),
        say_again=dict(view="say", start=dict(set="again"), steps=[dict(state=dict(n="1"))], note=N),
        # 🆕 ⑤b-6（2026-10-15）
        temp=dict(view="temp", steps=[dict(state=dict(avg="on"), tag=[dict(t="−0.5°", d="最高気温の平均", at="hi"), dict(t="−5.5°", d="最低気温の平均", at="lo")]),
                                      dict(state=dict(wx="on"))],
                  rel=[dict(t="−0.5°", src="TSB §1.22"), dict(t="−5.5°", src="TSB §1.22")], note=N),
        risk=dict(view="risk", steps=[dict(state=dict(day="on"), tag=dict(t="この日 35", at="day")),
                                      dict(state=dict(line="on", three="on"), tag=dict(t="3つで中止", at="three"))],
                  rel=[dict(t="この日 35", src="TSB §1.17.12.1"), dict(t="3つ", src="USCG p78")], note=N),
        cols=dict(view="cols", steps=[dict(state=dict(u0="on")), dict(state=dict(u8="on")), dict(state=dict(u7="on", ux="on", n1="on")),
                                      dict(state=dict(n2="on", n3="on", t1="on", t2="on")), dict(state=dict(tx="on", gap="on"))], note=N),
        cmp=dict(view="cmp", steps=[dict(state=dict(n="3")), dict(state=dict(n="5"))], note=N),
        rec6=dict(view="cards", start=dict(set="rec6"), steps=[dict(state=dict(n="6"))], note=N),
        q3=dict(view="cards", start=dict(set="q3"), steps=[dict(state=dict(n="1")), dict(state=dict(n="3"))], note=N),
        ice=dict(view="layers", steps=[dict(state=dict(ice="on"))], note=N),
        vac=dict(view="org", start=dict(seats="on"), steps=[dict(tag=dict(t="未定（TBD）", at="eng", to="eng")), dict(state=dict(vac="on"))], note=N),
        paper_drift=dict(view="paper", start=dict(doc="drift"), steps=[dict(state=dict(hl1="on")), dict(state=dict(hl2="on", hl3="on", hl4="on"))], note=N),
    )
    for nm, kw in good.items():
        bad, n = judge("m22", kw)
        g_ = not bad
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 22本目 正しい場面：{nm}（{n}件）" + (f"  ← {bad[0]}" if bad else ""))
    rows = list(M.APPB)
    for name, attr, val, key, kwk in (
            ("富士山を3,700メートルで描く", "FUJI_M", 3700.0, "富士山", "fuji"),
            ("報告書の順を入れ替える", "RP_T", (M.RP_T[1], M.RP_T[0], M.RP_T[2]), "3つの報告書", "reports"),
            ("ボルトを17本で描く", "SD_BOLTS", 17, "ボルトの数", "side"),
            ("全長を7.0メートルにする", "SD_LEN_M", 7.0, "全長", "side"),
            ("空席を総務部長にする", "ORG", M.ORG[:2] + (("技術部長", "filled"),) + M.ORG[3:7] + (("総務部長", "vacant"),), "空席", "org"),
            ("社員を14人にする", "ORG_STAFF", 14, "社員の印", "org"),
            ("「death」を8回にする", "PP_DEATH", 8, "death", "paper"),
            ("付録Bの1行の深さを変える", "APPB", tuple(rows[:2] + [rows[2][:1] + ("3800",) + rows[2][2:]] + rows[3:]), "付録B", "table"),
            ("届いた深さの値を3800にする", "DV_DEEP", "3800", "届いた回", "dives"),
            ("付録Aの文を直して書く", "APPA", dict(M.APPA, niskin=((M.APPA["niskin"][0][0], "SST", "remember to write down"),) + M.APPA["niskin"][1:]),
             "吹き出しの文", "chat"),
            ("436メートルを463メートルで描く", "DEPTH", M.DEPTH[:1] + (("9:23", 463.0, "a"),) + M.DEPTH[2:], "深さの点", "depth"),
            ("東南東を南東にする", "BW_DIR", dict(M.BW_DIR, ese=135.0), "方位", "bow"),
            ("海の底まで600メートルと書く", "TW_CA", ("海の底まで約600メートル",) + M.TW_CA[1:], "海の底までの残り", "two"),
            # 🆕 ⑤b-4（2026-10-15）
            ("亀裂を2つで描く", "SD_CRACK", 2, "亀裂の数", "crack"),
            ("文の印を1分に4回にする", "SE_N", 40, "文の印", "send"),
            ("手順の箱の順を入れ替える", "PR_T", (M.PR_T[0], M.PR_T[2], M.PR_T[1], M.PR_T[3]), "手順の箱", "proto"),
            ("知らせた先に「家族」を足す", "NO", dict(M.NO, told=dict(M.NO["told"], items=("客", "当局", "船級協会", "家族"))), "欄", "none"),
            ("吹き出しの英字を言い換える", "SAY", dict(M.SAY, tv=dict(M.SAY["tv"], bubbles=(("I want to be remembered as an innovator.",),) + M.SAY["tv"]["bubbles"][1:])),
             "吹き出しの英字", "say"),
            ("剥離を2と3のあいだにする", "LY_SEP", ((1, 2), (2, 3)), "剥離の面", "layers"),
            ("壊れる深さの計算を12,000メートルにする", "RL_M", dict(M.RL_M, fail=(12000.0,) + M.RL_M["fail"][1:]), "物差しの fail", "ruler"),
            ("ドームの壊れた深さを3,500メートルにする", "MD_DOME_M", 3500.0, "ドームが壊れた", "model"),
            ("船級の確かめに「検査」を足す", "KL_CHK", M.KL_CHK + ("検査をする",), "船級", "klass"),
            ("会合を社員4人にする", "MT_SEATS", M.MT_SEATS + (("社員", 1300.0, 440.0),), "会合の席", "meet"),
            ("押しつぶしの矢印を外向きにする", "TC_SIDE", (M.TC_SIDE[0], M.TC_SIDE[1][:4] + (True,)), "矢印の向き", "tc"),
            # 🆕 ⑤b-5（2026-10-15）
            ("カナダの見方を「示す」と書く", "CD", dict(M.CD, views=dict(M.CD["views"], cards=M.CD["views"]["cards"][:2] + (("カナダの調べ", "示す", "tsb", None, None),))),
             "要点の箱", "cards"),
            ("疲れの寿命の塗りを0.9にする", "CD_LIFE", 0.9, "疲れの寿命", "life"),
            ("溝を5.2インチで描く", "GV_IN", 5.2, "溝の幅", "groove"),
            ("試料を長さの向き8つにする", "CP_N", (8, 9), "試料の数", "coupons"),
            ("周りの向きを1.21にする", "SV_CIRC", 1.21, "安全率", "shelf"),
            ("10:05 を10:15 で描く", "D80_PTS", (M.D80_PTS[0], ("10:15", 3840.0)) + M.D80_PTS[2:], "80回目の深さの点", "d80"),
            ("拾わなかったセンサーを2つにする", "RT_AE", M.RT_AE[:4] + ((0.80, 0.58, False),) + M.RT_AE[5:], "監視装置の数", "rtm"),
            ("音の山を15:27:45 にする", "AE_PEAK", "15:27:45", "音の記録", "ae"),
            ("逆さに持っても向きが逆のまま", "ctrl_dirs", lambda flip: (1, -1), "そのまま", "ctrl"),
            ("黄の決まりを40にする", "SC_Y", 40, "画面の決まり", "screen"),
            ("4枚目のしわを20にする", "LY_GRIND", {1: 1, 2: 8, 3: 14, 4: 20}, "削ったしわ", "grind"),
            ("残す年を2021年にする", "DV_YEAR", "2021", "残した年", "dives22"),
            ("ぶつかった印を右舷に置く", "bw_hit", lambda: (M.BW_["tip"][0] + M.BW_["w"] + 4, M.BW_["tip"][1] + 170.0), "左舷", "bowhit"),
            ("試験の最も深い所を4,000メートルにする", "RL_M", dict(M.RL_M, test=(4000.0,) + M.RL_M["test"][1:]), "物差しの test", "ruler_mid"),
            ("窓の1,000メートルを会社の色にする", "RL_M", dict(M.RL_M, w1k=M.RL_M["w1k"][:2] + ("company",)), "物差しの w1k", "ruler_mid"),
            ("試験の線の札を4,000メートルと書く", "RL_M", dict(M.RL_M, test=(4200.0, "試験で最も深い 4,000メートル", "company")), "物差しの test の札", "ruler_mid"),
            ("80回目の句を言い換える", "PP_DOC", dict(M.PP_DOC, u80=dict(M.PP_DOC["u80"], lines=("the TITAN got stuck",) + M.PP_DOC["u80"]["lines"][1:])),
             "書類の句", "paper_u80"),
            # 🆕 ⑤b-6（2026-10-15）
            ("最低気温を−5.0°にする", "TP_LO", -5.0, "気温の平均", "temp"),
            ("この日の点数を38にする", "RK_DAY", 38, "危険度", "risk"),
            ("ストライクを2つで中止にする", "RK", dict(M.RK, bx=M.RK["bx"][:2]), "危険度", "risk"),
            ("主な要因を7つにする", "CL_ITEM", dict(M.CL_ITEM, u8=(0, 1, M.CL_ITEM["u8"][2][:7])), "3列の札", "cols"),
            ("船体の作りの欠陥を会社の色にする", "CL_ITEM", dict(M.CL_ITEM, u8=(0, 1, M.CL_ITEM["u8"][2][:4] + (("船体の作りの欠陥", "company"),) + M.CL_ITEM["u8"][2][5:])),
             "3列の札", "cols"),
            ("7つ目の下線を6つ目に引く", "CL_U7", ("u8", 5), "7つ目の下線", "cols"),
            ("列の順を入れ替える", "CL_COL", (M.CL_COL[1], M.CL_COL[0], M.CL_COL[2]), "列の名と色", "cols"),
            ("2022年の音のカナダを「示す」と書く", "VS_ROWS", M.VS_ROWS[:3] + (("cells", "2022年の音の重み", ("強く示す", "可能性が高い", "示す")),) + M.VS_ROWS[4:],
             "並べの行", "cmp"),
            ("勧告の番号を M26-08 まで書く", "CD", dict(M.CD, rec6=dict(M.CD["rec6"], cards=M.CD["rec6"]["cards"][1:] + (("M26-08", "運輸省へ", "tsb", None, None),))),
             "要点の箱", "rec6"),
            ("問いの言葉を言い換える", "CD", dict(M.CD, q3=dict(M.CD["q3"], cards=(("何が壊れた？",) + M.CD["q3"]["cards"][0][1:],) + M.CD["q3"]["cards"][1:])),
             "要点の箱", "q3"),
            ("凍る水を内側から描く", "ice_top", lambda: M.LY["y_in"], "凍る水", "ice"),
            ("ずれの句を言い換える", "PP_DOC", dict(M.PP_DOC, drift=dict(M.PP_DOC["drift"], lines=("past success is no guarantee of future success,",) + M.PP_DOC["drift"]["lines"][1:])),
             "書類の句", "paper_drift")):
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            bad, _ = judge("m22", good[kwk])
        except Exception as e:                 # 壊した値で組めない＝その旨を出して落とす
            bad = [f"組めない {e!r}"]
        finally:
            setattr(M, attr, keep)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 22本目 陽性対照（表）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    for name, kw, key in (
            ("水を入れずに台が沈む", dict(view="lars_side", steps=[dict(state=dict(lvl="under"))], note=N), "① 筋"),
            ("沈む前に切り離す", dict(view="lars_side", steps=[dict(state=dict(fill="on", det="on"))], note=N), "① 筋"),
            ("ボルトの前に「出入りはここだけ」", dict(view="side", steps=[dict(state=dict(only="on"))], note=N), "① 筋"),
            ("最後の点の前に止まった印", dict(view="depth", steps=[dict(state=dict(upto="b", stop="on"))], note=N), "① 筋"),
            ("札の時刻が記録に無い（8:25）", dict(view="lars_top", steps=[dict(tag=dict(t="8:25 閉める", at="t1"))], rel=[dict(t="8:25", src="x")],
                                          note=N), "記録の時刻"),
            ("札の数が rel に無い", dict(view="dives", steps=[dict(tag=dict(t="13回", at="t"))], note=N), "rel"),
            # 🆕 ⑤b-4（2026-10-15）
            ("分かれる前に押されて曲がる", dict(view="buckle", steps=[dict(state=dict(press="on"))], note=N), "① 筋"),
            ("海面を探す前に外に知らせる", dict(view="proto", steps=[dict(state=dict(wait="on", out="on"))], note=N), "① 筋"),
            ("層の厚さを約3センチと書く", dict(view="layers", steps=[dict(tag=dict(t="約3センチ", at="th"))], rel=[dict(t="約3センチ", src="x")], note=N),
             "1インチ"),
            # 🆕 ⑤b-5（2026-10-15）
            ("深さの線の前に音の印", dict(view="d80", steps=[dict(state=dict(bang="on"))], note=N), "① 筋"),
            ("音の山の前にひずみの跳び", dict(view="ae", steps=[dict(state=dict(jump="on"))], note=N), "① 筋"),
            ("端材の厚さを約13.5センチと書く", dict(view="groove", steps=[dict(state=dict(thick="on"), tag=dict(t="約13.5センチ", at="w"))],
                                             rel=[dict(t="約13.5センチ", src="x")], note=N), "端の厚さ"),
            ("札の時刻が記録に無い（15:20）", dict(view="ae", steps=[dict(state=dict(peak="on"), tag=dict(t="15:20", at="peak"))],
                                           rel=[dict(t="15:20", src="x")], note=N), "記録の時刻"),
            ("13回のうち6回と書く", dict(view="dives", steps=[dict(state=dict(y22="on"), tag=dict(t="13回のうち6回", at="t"))],
                                      rel=[dict(t="13回のうち6回", src="x")], note=N), "USCG p235"),
            # 🆕 ⑤b-6（2026-10-15）
            ("気温の札の符号を落とす（0.5°）", dict(view="temp", steps=[dict(state=dict(avg="on"), tag=dict(t="0.5°", at="hi"))], rel=[dict(t="0.5°", src="x")], note=N),
             "符号を含めて"),
            ("気温の札を ℃ で書く", dict(view="temp", steps=[dict(state=dict(avg="on"), tag=dict(t="−0.5℃", at="hi"))], rel=[dict(t="−0.5℃", src="x")], note=N), "℃"),
            ("線の前に3つで中止", dict(view="risk", steps=[dict(state=dict(three="on"))], note=N), "① 筋"),
            ("主な原因の前に8つ", dict(view="cols", steps=[dict(state=dict(u8="on"))], note=N), "① 筋"),
            ("カナダの危険の所見の前に監督の穴の枠", dict(view="cols", start=dict(u0="on", u8="on", ux="on", n1="on", n2="on"),
                                                  steps=[dict(state=dict(gap="on"))], note=N), "① 筋"),
            ("席の前に空いた席の枠", dict(view="org", steps=[dict(state=dict(vac="on"))], note=N), "① 筋")):
        bad, _ = judge("m22", kw)
        g_ = any(key in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 22本目 陽性対照（筋と札）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    for nm, fn in (("増えた吹き出しを減らす", lambda: M.m22("chat", [dict(state=dict(n="3")), dict(state=dict(n="2"))], start=dict(set="descent"), note=N)),
                   ("吹き出しを付録Aの行より多く", lambda: M.m22("chat", [dict(state=dict(n="5"))], start=dict(set="descent"), note=N)),
                   ("沈んだ台を浮かせる", lambda: M.m22("lars_side", [dict(state=dict(fill="on", lvl="under")), dict(state=dict(lvl="up"))], note=N)),
                   ("段で書類を替える", lambda: M.m22("paper", [dict(state=dict(doc="plan"))], note=N)),
                   ("note に模式が無い", lambda: M.m22("side", [dict()], note="形"))):
        try:
            fn()
            g_ = False
        except ValueError:
            g_ = True
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 22本目 型の見張り：{nm}: {'組めない（止まった）' if g_ else '🔴 組めた'}")
    return ok


# ══════════════════════════════════════════════════════════
#  🆕 23本目 ⑤b-3（2026-10-18）：模式図（m23＝`tools/mech23.py`・章をまたぐ型4つ＋第1〜3章の10の見え方）
# ══════════════════════════════════════════════════════════
#   🔴 2026-10-20（17本目 ⑤b-1・§0b）：23本目の記録 REC_M23 の全項目（67キー＝建物の階と使い道・先に落ちる床・閉めた所・柱の格子・文庫本・会議・別紙2 の欄・判断の流れ・点検の表・時計〈第1〜3章〉／
#    H形鋼・暦・札の数・センターの数・継ぎ足した紙・順位・柱の直径と鉄筋・柱のあいだ・1人の重さ・台数・5階の使い道・仮の使用の階・床の広さ・板の無い所・冷却塔〈第4〜7章〉／
#    箱の物・余計な重さ・ダクトの穴・つなぎ目・フック・積み木・4階の帯・決まりの線・点検の項目〈第8〜9章〉／窓口・届けと確かめ・10月の数・戸籍・最終の数・年代の表・最多の比べ・罰の札・瓦礫・補償・3つの問い・別紙3つ・
#    1つ目の表・会長の欄・賄賂の額・図面の棚・判決の段階・切れた線・原因の札・積み木の札・止められた所・開いたままの店〈第10〜11章・終章〉）は selftest の見本 `tools/fixture_ep23.py`
#    （GATES["check_mech"]・値は1つも変えていない＝git の `b800dbdb`）へ移した＝空。selftest は見本の表だけ差し込む（`fixture_ep23.apply(gate, tables_only=True)`）。
#    17本目で模式図 mech23 の型を使うときは、その回の記録の値をここに別に持つ（§5b-88＝描く側の表 mech23.SC_USE・CLOSED・SINK_PTS・GRID・CK_SET・FORM・FLOW・TB_ROWS・BK_*・WL・CAL_SET・CARDS・NUMS・SH・RANK・
#    CX_COLS・SP_LONG_M・PQ・VS_SET・USE5・HI・AREA・DP_MISS・CT・TW3・LD・LISTS・OVER_KG・DU_CUT・JT_CM・HK_CM・SK_ITEMS・SK_COL_MM・P3・RL_LINE・RL_PT・ITEMS・TG・DESK・TALLY・TOLL・KOSEKI・FINAL・AGES・MOST・
#    PEN・HAUL・PAY・Q3・FORMS3・ACTS・CHAIR・FAKE・BRIBE・CARD_SETS・SHELF・STAGES・CHAIN・GAP・CAUSES・OPEN・BLOCKS・STOP を書き換えると鳴る）。引いた原文（ソウル市・国会の報告・検察の報告・瑞草区の報告・
#    判決 大96・大99・高96・白書の頁）と頁の番号の書き方〈会議録の PDF の頁＝印刷の頁・頁の無い資料は「名 p1」〉は移した注の側にある＝fixture_ep23 の REC_M23 の注。
#    空のあいだ、m23 のカットは `judge_m23` が「記録の表が空」で止まる（fail closed＝KeyError にしない。judge_m22・judge_m21 と同じ）。
#    ⚠️ **本番に残したもの（見本に入れていない）＝`_M23_NEED`・`_M23_NEED_B4`・`_M23_NEED_B5`・`_M23_NEED_B6`（「先に起きることが先」の筋の表）・`NUM_M23`（札の数と時刻を拾う正規表現）・`VIEW_HEADS`・
#       `view_dir_check`（見る向きの合図）・`_m23_src_page`・`_judge_m23_b4`〜`_judge_m23_b6`（記録 R の値を引いて形 g と照らす関数）**。判断の理由（`_M22_NEED`・`_M21_NEED` と同じ）：
#       `_M23_NEED*` は mech23 の見え方〈view〉と欄の名の約束（崩れたあとに重さが増えた階の印・たわみはうろこを見せてから・水を抜くのは冷却塔を止めてから・…）を並べた表で、
#       記録の値（時刻・数・座標・頁の照合）を持たない＝型の側の規則。判定の関数は値を `R`（＝この表）から引くだけで、値そのものを持たない。
#       ⚠️ 例外として、判定の中に23本目の言い回しが残る所がある：`_m23_src_page` は原文の道（`ref/ep10/src/assembly_sampoong_tokui_no6_19950912_id19114.txt`＝10本目から引いた会議録）を直書きしている・
#       `_judge_m23_b6` は「502−30−471＝1」「額の幅と合計」のように R の値どうしの足し算を確かめる（R が空なら judge_m23 が先に止まる＝本番では働かない）。
#       値を持つ表になったら、その行は見本へ移す。17本目で見え方を足すときは、その見え方の筋をこの表に足す
REC_M23 = {}
_M23_NEED_B6 = (                    # 🆕 ⑤b-6 の筋（下の _M23_NEED に足す）
    ("desk", "one", "on", "two", {"on"}, "まとめる矢印は、2つの窓口を見せてから"),
    ("desk", "fix", "on", "one", {"on"}, "直した数は、まとめる途中（まとめる矢印と同じ段かあと）"),
    ("tally", "done", "on", "total", {"on"}, "確かめた数は、届けの数の棒の中に"),
    ("tally", "left", "on", "done", {"on"}, "残りの数は、確かめた数のあとに"),
    ("toll", "parts", "on", "total", {"on"}, "内訳は、合計を見せてから"),
    ("koseki", "done", "on", "n", {"on"}, "確定の印は、30人の札のあとに"),
    ("final", "calc", "on", "cards", {"on"}, "引き算は、最終の数を見せてから"),
    ("ages", "top", "on", "bars", {"on"}, "いちばん多い年代は、棒を全部見せてから"),
    ("most", "r1", "on", "r0", {"on"}, "それまでの最多の棒は、三豊の棒のあとに"),
    ("pen", "b0", "on", "q", {"on"}, "罰の棒は、罪の札のあとに"),
    ("pen", "b1", "on", "b0", {"on"}, "重くなった罰は、事故の前の罰と並べて"),
    ("pen", "b1", "on", "law", {"on"}, "重くなった罰は、改めた法律の札のあとに"),
    ("haul", "found", "on", "truck", {"on"}, "見つかった数は、瓦礫を運んだあとに"),
    ("pay", "sub", "on", "r0", {"on"}, "円と平均は、亡くなった人の額のあとに"),
    ("acts", "seen", "on", "c1", {"on"}, "見てきた印は、4つの札を見せてから"),
    ("chair", "c3", "on", "c12", {"on"}, "過失の札は、知っていた札のあとに"),
    ("fake", "doc", "on", "site", {"on"}, "見たことにした書類は、見ていない現場のあとに"),
    ("bribe", "ward", "on", "rumor", {"on"}, "記録の棒は、語られる話のあとに"),
    ("bribe", "city", "on", "ward", {"on"}, "市の3人は、区の12人に足す"),
    ("stages", "fault", "on", "cards", {"on"}, "過失は、4つの段階を見せてから"),
    ("chain", "one", "on", "link", {"on"}, "1か所だけの×は、鎖を見せてから"),
    ("gap", "cut", "on", "line", {"on"}, "切れた線は、つないだ線を見せてから"),
    ("causes", "gov", "on", "four", {"on"}, "役所の監督は、4つの欠陥のあとに"),
    ("open", "sign", "on", "sig", {"on"}, "営業のあとに直す札は、朝の合図のあとに"),
    ("blocks", "up", "on", "low", {"on"}, "載った重さは、弱い作りの上に"),
    ("stop", "mk", "on", "cards", {"on"}, "欠陥の印は、札を見せてから"),
    ("stop", "one", "on", "mk", {"on"}, "1人ではない括弧は、印を見せてから"),
)
_M23_NEED_B5 = (                    # 🆕 ⑤b-5 の筋（下の _M23_NEED に足す）
    ("lists", "diff", "on", "w", {"on"}, "違いの印は、2つ目の箱を見せてから"),
    ("over", "add", "on", "pre", {"on"}, "余計な重さの矢印は、前提の重さの上に"),
    ("cover", "cover", "on", "q", {"on"}, "押えコンクリートは、重さを増やす物の問いのあと"),
    ("duct", "cut", "on", "duct", {"on"}, "切った穴は、ダクトを見せてから"),
    ("joint", "ruler", "on", "bar", {"lit"}, "長さの物差しは、上の鉄筋を見せてから"),
    ("joint", "wall", "on", "fall", {"on"}, "立ったままの壁の印は、床が落ちてから"),
    ("hook", "r", "on", "l", {"on"}, "まっすぐ短い形は、本来の形を見せてから"),
    ("section", "joints", "on", "walls", {"on"}, "つなぎ目の印は、残った壁を見せてから"),
    ("section", "walls", "on", "fall", {"all"}, "残った壁は、崩れたあとに"),
    ("stack", "noreinf", "on", "items", {"on"}, "補強なしの印は、積み重なった重さを見せてから"),
    ("plan", "up", "on", "marks", {"on"}, "上の階の括弧は、前触れの印を見せてから"),
    ("rule", "pt", "on", "zone", {"on"}, "三豊の点は、決まりの線を見せてから"),
    ("items", "no", "on", "c1", {"on"}, "無い項目は、項目を全部見せてから"),
    ("slab", "leak", "on", "dpm", {"on"}, "水漏れは、板の無い所を見せてから"),
)
_M23_NEED_B4 = (                    # 🆕 ⑤b-4 の筋（下の _M23_NEED に足す）
    ("road", "amb", "blocked", "jam", {"on"}, "救助の車が止まる印は、道がふさがってから"),
    ("cal", "d1", "on", "d0", {"on"}, "救出の日の印は、崩れた日を見せてから"),
    ("plan", "add", "on", "aplan", {"on"}, "増えた床の色は、工事の図面の床を見せてから"),
    ("plan", "miss_lit", "on", "dp", {"miss"}, "板の無い所の輪は、板の無い所を見せてから"),
    ("hoop", "cut", "on", "r", {"on"}, "切った帯筋は、内側の帯筋を見せてから"),
    ("load", "brit", "on", "cap", {"less"}, "粘りの話は、支えられる重さが減ってから"),
    ("vs", "lit", "on", "c1", {"on"}, "片方を明るくするのは、2つの札を見せてから"),
    ("beam", "lit", "on", "l", {"on"}, "梁を明るくするのは、梁のある作りを見せてから"),
    ("drop", "up", "on", "dp", {"on"}, "支える矢印は、板を見せてから"),
    ("redo", "x", "on", "loop", {"on"}, "怠った印は、やり直す手順を見せてから"),
    ("slab", "box", "on", "bar", {"sunk"}, "重い箱は、上の鉄筋が沈んだ床に"),
    ("bldg", "chk", "on", "hi", {"temp"}, "途中の検査なしの印は、仮の使用の階を見せてから"),
    ("tower", "roof", "on", "load", {"on"}, "屋上の床を明るくするのは、重さの矢印のあと"),
)
_M23_NEED = (
    ("section", "load", "on", "fall", {"all"}, "重さが増えた階の印は、崩れたあとの元の場所に"),
    ("bldg", "bulge", "on", "cell", {"on"}, "床の盛り上がりの矢印は、食堂の印を見せてから"),
    ("bldg", "x", "on", "spk", {"on"}, "怠った印は、放送の印を見せてから"),
    ("plan", "sag", "on", "scale", {"on"}, "たわみは、うろこを見せてから"),
    ("plan", "crack", "on", "north", {"on"}, "ひびは、北側の食堂を見せてから"),
    ("plan", "start", "on", "crack", {"on"}, "崩れはじめる側は、ひびを見せてから"),
    ("plan", "hit", "on", "nums", {"on"}, "2本の柱の印は、列と行の番号を見せてから"),
    ("plan", "rubble", "on", "walls", {"on"}, "落ちた床は、残った壁を見せてから"),
    ("slab", "sink", "on", "crack", {"on"}, "柱の近くの沈みは、ひびを見せてから"),
    ("slab", "beam", "plan", "sag", {"on"}, "鉄の梁の補強は、沈んだ床に"),
    ("tower", "drain", "on", "run", {"off"}, "水を抜くのは、冷却塔を止めてから"),
    ("table", "why", "on", "r2", {"on"}, "点検の目的は、2回目の行を見せてから"),
) + _M23_NEED_B4 + _M23_NEED_B5 + _M23_NEED_B6
NUM_M23 = re.compile(r"[0-9０-９]{1,2}[:：][0-9０-９]{2}|[0-9０-９][0-9０-９,.．]*")
VIEW_HEADS = ("横から", "上から", "斜めから")


def _m23_src_page(p):
    """原文の頁の文字（空白を除く）。手元に原文が無ければ None（Actions など＝表の写しだけで照らす）。"""
    from pathlib import Path
    t = Path(__file__).resolve().parent.parent / "ref" / "ep10" / "src" / "assembly_sampoong_tokui_no6_19950912_id19114.txt"
    if not t.exists():
        return None
    parts = re.split(r"=== \[PDF p\.(\d+)\] ===", t.read_text(encoding="utf-8"))
    pages = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}
    return re.sub(r"\s+", "", pages.get(p, ""))


def view_dir_check(plan_text, lab):
    """PLAN の「見る向き：」の頭の語と、図の左上の札の頭の語が同じか（空＝合う）。🆕 23本目 ⑤b-3＝見る向きの合図の門番"""
    m_ = re.search(r"見る向き：(横から|上から|斜めから)", plan_text or "")
    if not m_:
        return ""
    return "" if str(lab).startswith(m_.group(1)) else f"左上の札「{lab}」が PLAN の見る向き「{m_.group(1)}」で始まらない（見る向きの合図）"


def judge_m23(f):
    """23本目 模式図：①状態の筋 ②形・表・色（f.mech["geo"]）を記録（REC_M23）で ③札の数・時刻。"""
    import jiko_style as J
    bad, n = [], 0
    m = f.mech
    g, view = m["geo"], m["view"]
    seq = [m["start"]] + list(m["states"])
    R = REC_M23
    if not R:
        return ["記録の表 REC_M23 が空（その回の値を入れるまで、m23 のカットは止まる）"], 1
    texts = list(m["tags"])

    def need(cond, msg):
        nonlocal n
        n += 1
        if not cond:
            bad.append(msg)
    for v, fl, val, pre, ok_vals, msg in _M23_NEED:
        if v != view:
            continue
        for s in seq:
            if s.get(fl) == val:
                need(s.get(pre) in ok_vals, f"① 筋：{msg}")
    if view == "section":
        need((g["above"], g["below"]) == (R["floors"]["above"], R["floors"]["below"]), f"② 階の数（地上{g['above']}・地下{g['below']}）が記録（地上5・地下4）と違う")
        need(g["use"] == {w: [(tuple(r), t) for r, t in v] for w, v in R["use"].items()}, "② 各階の使い道が記録（ソウル市の報告 p.34 の断面図）と違う")
        need(g["a_left"], "② A棟（北）が左にない（ソウル市の報告の図の向き＝A棟が北）")
        need(g["a_col"].lower() == J.ROLE["bldg_a"].lower() and g["b_col"].lower() == J.INK_W.lower(), "② 棟の色が役の色（A棟＝ピンク・B棟＝白）でない")
        base_y = g["rows"][0]["slab_y"] if g["rows"][0]["fall"] == "none" else None
        for r in g["rows"]:
            if r["fall"] == "none" or base_y is None:
                continue
            moved = [abs(a - b) > 0.5 for a, b in zip(r["slab_y"], base_y)]
            if r["fall"] == "top":
                need(all(moved[i] for i in R["first_fall"]) and not any(moved[i] for i in range(len(moved)) if i not in R["first_fall"]),
                     "② 先に落ちる床の板が記録（屋上と5階＝国会の報告 p.28）と違う")
            if r["fall"] == "all":
                need(all(moved) and all(y > g["ground"] for y in r["slab_y"]) and all(y < g["b3_floor"] for y in r["slab_y"]),
                     "② 崩れたあとの床の板が地下3階の床の上に積もっていない（5階から地下まで＝検察の報告 p.47）")
                need(r["conn"] <= 0.01, "② 崩れたあとに真ん中の通路が残っている（崩れた所＝A棟と中央の連結通路＝検察の報告 p.45）")
    if view == "bldg":
        need(g["n"] == R["floors"]["above"], f"② 地上の階の数 {g['n']}（記録 5）")
        need(set(g["closed"]) == set(R["closed"]), f"② 閉めた所 {sorted(g['closed'])} が記録（5階の食堂・4階の貴金属）と違う")
        for k, (f0, f1) in g["closed"].items():
            if k in R["closed"]:
                _w, lo, hi = R["closed"][k]
                need(lo < (f1 - f0) <= hi, f"② 閉めた所 {k} の幅 {f1 - f0:.2f} が記録の言い方（{_w}）と合わない")
        need(tuple(g["hi"]["a5"]) == R["hi_a5"], "② 朝の記録の階が A棟5階でない（国会の報告 p.30）")
        need(g["a_left"] and g["a_col"].lower() == J.ROLE["bldg_a"].lower(), "② A棟（ピンク）が左にない")
    if view == "plan":
        need(g["a_left"], "② A棟（北）が左にない")
        if any(s.get("sink") == "on" for s in seq):
            need(g["sink"] == R["sink"], f"② 屋上の沈んだ所 {g['sink']}（記録 {R['sink']}か所＝検察の報告 p.47）")
        if any(s.get("chk") == "on" for s in seq):
            need(tuple(g["chk"]) == R["b1_chk"], f"② 区が確かめた受け持ち {g['chk']} が記録（区の報告 p.45）と違う")
        if g["floor"] == "grid":
            need(set(g["cols"]) <= R["grid"]["cols"] and set(g["rows"]) <= R["grid"]["rows"], "② 柱の列と行の番号に判決に無い番号がある")
            need(set(g["hit"]) == R["grid"]["hit"], f"② 印の柱 {g['hit']} が記録（5列E行・5列F行＝判決 理由1）と違う")
            for c_, r_ in g["hit"]:
                need((c_, r_) in g["grid_px"], f"② 印の柱 {c_}列{r_}行が柱の並びの上に無い")
    if view == "slab":
        rows = g["rows"]
        if g["z"] == "span":
            for s, r in zip(seq, rows):
                pts = r["slab"]
                n_ = len(pts) // 2
                mid = pts[n_ // 2][1]
                if s.get("sag") == "on":
                    need(mid > g["top"] + 1, "② 沈んだはずの床の板が下がっていない")
        else:
            c = g["cols"][0]
            for s, r in zip(seq, rows):
                L_ = r["slabL"]
                if s.get("sink") == "on" and s.get("punch") != "on":
                    need(L_[1][1] > L_[0][1] + 1, "② 柱の近くの床が沈んでいない（柱の側が下がる＝国会の報告 p.30）")
                if s.get("punch") == "on":
                    need(min(y for _x, y in L_) > g["top"] + 40 and max(x for x, _y in L_) < c, "② 押し抜きのあとに床が柱から離れて落ちていない")
    if view == "bunko":
        Rb = R["bunko"]
        need(abs(g["sink_px"] / g["px_cm"] - Rb["sink_cm"]) < 1e-6 and abs(g["sink_cm"] - Rb["sink_cm"]) < 1e-9,
             f"② 沈みの括弧が記録（{Rb['sink_cm']:g}センチ＝国会の報告 p.30）と違う")
        need(tuple(g["book_mm"]) == Rb["book_mm"] and all(abs(p / g["px_cm"] * 10 - mm) < 1e-6 for p, mm in zip(g["book_px"], Rb["book_mm"])),
             "② 文庫本の大きさが A6判（105×148ミリ）と違うか、縮尺が括弧と違う")
    if view == "meeting":
        need(tuple(g["cards"]) == R["meeting"] and g["col"].lower() == J.COMPANY.lower(), f"② 会議の札 {g['cards']} が記録（社長・会長・役員たち）と違うか、会社の色でない")
    if view == "form":
        Rf = R["form"]
        fm_ = g["form"]
        need((fm_["title"], fm_["head"], tuple(fm_["cols"])) == (Rf["title"], Rf["head"], Rf["cols"]), "② 別紙2 の題と欄の名が記録と違う")
        joined = " ".join(fm_["cell"]).replace(" …", "").strip()
        need(joined == Rf["quote"], f"② 欄の句「{joined}」が記録（検察の報告 p.52 の原文）と違う")
        src_ = _m23_src_page(Rf["page"])
        if src_ is not None:
            need(re.sub(r"\s+", "", Rf["quote"]).replace("‘", "'").replace("’", "'") in src_.replace("‘", "'").replace("’", "'"),
                 "② 記録の句が原文の頁（p.52）に無い")
        for t_, i in g["hl"]:
            need(t_ in fm_["cell"][i], f"② 印の句「{t_}」が欄の行に無い")
    if view == "flow":
        Rw = R["flow"]
        need(tuple(g["head"]) == Rw["head"] and tuple(g["boxes"]) == Rw["boxes"], "② 判断の流れの札が記録（国会の報告 p.32 の要約）と違う")
        need(not any(w in t for w in Rw["ng"] for t, _r in g["boxes"]), "② 次のカットの語り（大きな惨事）を札にしている")
    if view == "table":
        Rt = R["table"]
        need(tuple((r[1], r[2]) for r in g["rows"]) == Rt["rows"] and g["rows"][1][3] == Rt["why"], "② 点検の期間と目的が記録（区の報告 p.45）と違う")
        (m0, d0), (m1, d1) = Rt["rows"][1]
        need(m0 * 31 + d0 <= Rt["day"][0] * 31 + Rt["day"][1] <= m1 * 31 + d1 and g["bar"][0] <= g["day_x"] <= g["bar"][1],
             "② 事故の日（6月29日）の印が2回目の期間の帯の中に無い")
    if view == "clocks":
        want = R["clocks"][g["set"]]
        got = tuple((t, a, r) for t, a, _w, r in g["items"])
        need(got == want, f"② 時計の時刻と役 {got} が記録 {want} と違う")
        for (t, _a, _r), (ha, ma) in zip(want, g["angles"]):
            h, mi = (int(x) for x in t.split(":"))
            need(abs(ha - ((h % 12) * 30 + mi * 0.5)) < 1e-6 and abs(ma - mi * 6) < 1e-6, f"② 時計 {t} の針の角度が時刻と合わない")
    bad_, n_ = _judge_m23_b4(g, view, seq, R)
    bad += bad_
    n += n_
    bad_, n_ = _judge_m23_b5(g, view, seq, R)
    bad += bad_
    n += n_
    bad_, n_ = _judge_m23_b6(g, view, seq, R, texts)
    bad += bad_
    n += n_
    said = [r.get("t", "") for r in m["rel"]]
    for t in texts:
        for mm in NUM_M23.finditer(t):
            tok = mm.group(0)
            need(any(tok in s for s in said), f"③ 札「{t}」の数「{tok}」が rel（記録の値の宣言）に無い")
            full = tok.replace("：", ":")
            if ":" in full:
                need(full in R["clock"], f"③ 札「{t}」の時刻「{tok}」が記録の時刻（{sorted(R['clock'])}）に無い")
    for r in m["rel"]:
        need(bool(r.get("src")), f"③ rel「{r.get('t')}」に出どころ（src）が無い")
    return bad, n


def _judge_m23_b4(g, view, seq, R):
    """🆕 23本目 ⑤b-4：第4〜7章の見え方と、足した欄の照合（記録＝R・形＝g）。"""
    import datetime as dt
    bad, n = [], 0

    def need(cond, msg):
        nonlocal n
        n += 1
        if not cond:
            bad.append(msg)
    any_ = lambda f, v: any(s.get(f) == v for s in seq)   # noqa: E731
    if view == "wall":
        need(g["hbeam"] == R["wall"]["hbeam"], f"② H形鋼 {g['hbeam']} か所（記録 {R['wall']['hbeam']}か所＝ソウル市の報告 p.37）")
    if view == "cal":
        if g["set"] == "rescue":
            Rc = R["cal"]["rescue"]
            for (y, mo, d), col, row in g["cells"]:
                need(col == (dt.date(y, mo, d).weekday() + 1) % 7, f"② 暦の {mo}月{d}日 が {col}列（実際の曜日と違う）")
            need(tuple(g["fall"]) == Rc["fall"] and tuple(g["mark"]) == Rc["mark"], f"② 暦の印 {g['fall']}・{g['mark']} が記録（6月29日・7月9日＝白書 p.643）と違う")
            need(tuple(g["cells"][-1][0]) == Rc["last"], f"② 暦の終わり {g['cells'][-1][0]} が7月15日（17日目）でない")
            cell = {tuple(c[0]): (c[1], c[2]) for c in g["cells"]}
            need(cell.get(tuple(g["fall"])) == tuple(g["fall_cell"]) and cell.get(tuple(g["mark"])) == tuple(g["mark_cell"]), "② 印の升目が日付の升目と違う")
        else:
            Rc = R["cal"]["move89"]
            need(tuple(g["band"]) == Rc["band"] and tuple(g["open"]) == Rc["open"], f"② 移した時期 {g['band']}・開店 {g['open']} が記録（1989年7〜12月・12月1日）と違う")
            need((g["open"][0], g["open"][1]) in [tuple(m_) for m_ in g["months"]], "② 開店の日が暦の月に無い")
    if view == "cards" and g.get("set", "rescue") == "rescue":      # 🆕 ⑤b-6：組（bribe・art）は _judge_m23_b6
        need((g["cards"]["head"][0], tuple(g["cards"]["rows"])) == (R["cards"]["head"], R["cards"]["rows"]), "② 札の数が記録（ソウル市の報告 p.37・p.39＝7月19日）と違う")
    if view == "nums":
        need(g["nums"]["place"][0] == R["nums"]["place"] and tuple(g["nums"]["boxes"]) == R["nums"]["boxes"], "② センターの数が記録（ソウル市の報告 p.39）と違う")
    if view == "sheets":
        lo, hi = R["sheets"]
        need(lo < g["sheets"] < hi + 1, f"② 継ぎ足した紙 {g['sheets']} 枚が「20回あまり」（判決）と合わない")
    if view == "rank":
        need(tuple(g["rank"]) == R["rank"], f"② 順位 {g['rank']} が記録（白書 p.69＝売り上げ7位・売り場2位）と違う")
    if view == "colx":
        need(tuple((t, d, k) for t, d, k, _r in g["colx"]) == R["colx"], f"② 柱の直径と鉄筋の数が記録（国会の報告 p.29）と違う")
        need(abs(g["cover_cm"] - R["colx_cover_cm"]) < 1e-9, "② 鉄筋の輪が表面から5センチでない")
    if view == "spans":
        need(abs(g["long_m"] - R["spans_m"]) < 1e-9, f"② 柱のあいだ {g['long_m']} メートル（記録 10.8＝判決）")
        need(g["sag"][1] > g["sag"][0], "② 長い柱のあいだの床が、短いほうより垂れていない")
    if view == "persq":
        Rp = R["persq"]
        need(tuple(g["n"]) == Rp["n"] and abs(g["per"] - Rp["per"]) < 1e-9, f"② 人の数 {g['n']}・1人の重さ {g['per']}（記録の計算＝6人・4人・65キロ）")
        for k, kg in zip(g["n"], Rp["kg"]):
            need(abs(k * Rp["per"] - kg) / kg <= Rp["tol"], f"② {k}人×{Rp['per']:g}キロが {kg:g}キロから1割より外れる")
    if view == "vs":
        if g["set"] == "count":
            need(tuple((c[0][0], c[0][1]) for c in g["cards"]) == R["vs"]["count"], "② 台数の札が記録（判決 3基・白書 4台）と違う")
        else:
            need(tuple((h, v) for h, v, _r in g["cards"][1]) == R["vs"]["rumor_rec"], "② 記録の札が判決（1基28.7トン）・検察（1989年）と違う")
    if view == "bldg":
        need(g["use5"] == R["use5"], f"② 5階の使い道 {g['use5']} が記録（許可＝運動の施設・実際＝食堂街）と違う")
        if any_("hi", "temp"):
            need(frozenset(g["temp"]) == R["temp"], f"② 仮の使用の階 {g['temp']} が記録（地下1階〜地上3階＝区の報告 p.43）と違う")
            need(g.get("under") == "on", "② 仮の使用に地下1階の帯が無い")
    if view == "plan" and g.get("area"):
        a = g["area"]
        need((a["permit"], a["plan"], a["add"]) == (R["area"]["permit"], R["area"]["plan"], R["area"]["add"]) and a["permit"] + a["add"] == a["plan"],
             "② 床の広さが記録（許可 71,136・図面 73,205・増えた 2,069）と違う")
        x0, x1 = a["x"]
        need(abs((g["split_px"] - x0) / (x1 - x0) - R["area"]["permit"] / R["area"]["plan"]) < 1e-6, "② 増えた床の幅が広さの割合と違う")
    if view == "plan" and any_("dp", "miss"):
        need(set(g["dp_miss"]) == R["dp_miss"], f"② 板の無い所 {g['dp_miss']} が記録（5階 4列E行＝判決）と違う")
    if view == "plan" and g.get("ct_rows"):
        need(g["ct_n"] == R["towers"], f"② 冷却塔 {g['ct_n']} 基（判決 3基）")
        for s, row in zip(seq, g["ct_rows"]):
            if s.get("ct") == "moved":
                need(all(b[1] > a[1] + 50 for a, b in zip(g["ct_rows"][0], row)), "② 移したあとの冷却塔が前の側（下）に動いていない")
    if view == "slab" and g.get("bars"):
        oks = [o for b, o in g["bars"] if b == "ok"]
        for b, o in g["bars"]:
            if b == "sunk":
                need(o > g["bar_off"]["ok"] + 5 and all(o > x for x in oks), "② 沈んだ鉄筋が正しい位置より深くない")
    if view == "tower" and g["set"] == "three":
        need(g["n"] == R["towers"], f"② 冷却塔 {g['n']} 基（判決 3基）")
    if view == "load" and g["set"] == "sum":
        need(g["towers"] == R["towers"], f"② 屋上の冷却塔 {g['towers']} 基（判決 3基）")
    if view == "drag":
        rows = g["drag"]
        for r in rows:
            need(abs(r["sag_x"] - r["box_x"]) < 30, "② たわみが重い箱の下に無い")
        if any(r["pos"] == "moved" for r in rows):
            need(rows[-1]["box_x"] > rows[0]["box_x"] + 100, "② 引きずった箱が動いていない")
    if view == "crack" and any_("crack", "long"):
        need(g["branch"] > 0, "② ひびが育っていない（枝のひびが無い）")
    return bad, n


def _judge_m23_b5(g, view, seq, R):
    """🆕 23本目 ⑤b-5：第8〜9章の見え方と、足した欄の照合（記録＝R・形＝g）。"""
    import jiko_style as J
    bad, n = [], 0

    def need(cond, msg):
        nonlocal n
        n += 1
        if not cond:
            bad.append(msg)
    any_ = lambda f, v: any(s.get(f) == v for s in seq)   # noqa: E731
    if view == "lists":
        got = tuple((h, r, tuple(it)) for h, r, it in g["lists"])
        need(got == R["lists"], f"② 箱の物 {got} が記録（国会の報告 p.29・白書 p.89）と違う")
    if view == "over":
        need(abs(g["over_kg"] - R["over_kg"]) < 1e-9, f"② 余計な重さ {g['over_kg']:g} キロ（記録 360＝判決）")
        need(g["add"][1] < g["pre"][0] and g["pre"][1] < g["top"], "② 足された重さの矢印が前提の重さの上に無い（床の上に前提・その上に足された重さ）")
    if view == "cover":
        c = g["cover"]
        need(c["cc"] < c["wp"] <= c["top"], "② 押えコンクリートが防水の層の上・屋上の床の上の順に無い（国会の報告 p.29）")
    if view == "duct":
        d = g["duct"]
        need(tuple(d["cut"]) == R["duct"] and abs(d["frac"] - R["duct"][0] / R["duct"][1]) < 1e-6,
             f"② 穴の長さの割合 {d['frac']:.3f} が記録（壁の長さ160センチのうち98センチ＝国会の報告 p.29）と違う")
        need(d["wall"][0] <= d["slot"][0] < d["slot"][1] <= d["wall"][1], "② 穴が壁の外にはみ出す")
    if view == "joint":
        j = g["joint"]
        need(abs(j["need_cm"] - R["joint"]["need"]) < 1e-6 and all(abs(a - b) < 1e-6 for a, b in zip(j["got_cm"], R["joint"]["got"])),
             f"② 物差しの長さ {j['need_cm']:g}・{j['got_cm']} センチが記録（64センチ・15〜18センチ＝判決）と違う")
        for r in j["rows"]:
            if r["fall"] == "on":
                need(r["slab_y"] > j["top"] + 100, "② 落ちたはずの床が壁から離れて下がっていない（壁は立ったまま床だけ＝国会の報告 p.29）")
    if view == "hook":
        h = g["hook"]
        need(len(h["bent"]) == 2 and abs(h["bent"][0] / h["bent"][1] - R["hook"][0] / R["hook"][1]) < 1e-6,
             f"② 曲げる形の2本の鉄筋の長さの比 {h['bent']} が記録（64：40＝国会の報告 p.29）と違う")
        need(all(h["hooks"]) and not any(h["straight_hooks"]), "② 曲げる形に引っかけ（先）が無いか、まっすぐの形に引っかけがある")
        need(max(h["straight"]) < min(h["bent"]), "② まっすぐの形の鉄筋が、曲げる形より短くない")
    if view == "section" and g.get("walls"):
        (n0, n1), (s0, s1) = g["walls"]
        a0, a1 = g["a_x"]
        need(len(g["walls"]) == 2 and abs(n0 - a0) < 1e-6 and abs(s1 - a1) < 1e-6 and n1 < s0,
             "② 残った壁が A棟の北と南の端に無い（ソウル市の報告 p.37「A동 북측 잔여벽체」「A동 남측 벽체」）")
    if view == "stack":
        need(frozenset(g["stack"]) == R["stack"], f"② 積み木の物 {g['stack']} が記録（国会・白書・判決が挙げる物）と違う")
        calc, plan = dict((t, d) for t, d, _n in R["colx"])["計算書"], dict((t, d) for t, d, _n in R["colx"])["図面"]
        w_plan, w_calc = g["col_w"]
        need(abs(w_plan / w_calc - plan / calc) < 1e-6, f"② 柱の太さの比 {w_plan:g}：{w_calc:g} が記録（図面60：計算書80＝国会の報告 p.29）と違う")
    if view == "bldg" and (any_("hi", "f4") or any_("hi", "f4a5")):
        need(frozenset(g["f4"]) == R["f4"], f"② 4階の帯 {g['f4']} が両方の棟でない（売り場の棟は記録に無い＝国会の報告 p.30）")
        need(frozenset(g["f4a5"]) == R["f4"] | {("a", 5)}, "② 4階の帯と食堂街（A棟5階）の帯が記録と違う")
    if view == "plan" and g.get("floor") == "three":
        need(tuple(g["labs"]) == R["three"], f"② 床の名 {g['labs']} が記録に残る場所（4階・5階・屋上）と違う")
    if view == "tower" and g.get("gauge"):
        lv = {k: y for k, y in g["gauge"]}
        if "low" in lv and "on" in lv:
            need(lv["low"] > lv["on"], "② 調節したあとの水の高さが下がっていない")
    if view == "rule":
        r = g["rule"]
        ax = r["ax"]
        X = lambda m: ax["x0"] + m / ax["mx"] * (ax["x1"] - ax["x0"])   # noqa: E731
        Y = lambda f: ax["y0"] - f / ax["my"] * (ax["y0"] - ax["y1"])   # noqa: E731
        Rr = R["rule"]
        need((r["line"]["floors"], r["line"]["span"]) == (Rr["floors"], Rr["span"]), f"② 決まりの線 {r['line']} が記録（16階以上か30メートル以上＝検察の報告 p.50）と違う")
        need(abs(r["zone"][0][0] - X(Rr["span"])) < 1e-6 and abs(r["zone"][1][1] - Y(Rr["floors"])) < 1e-6,
             "② 決まりの線の画素が軸の目盛りと合わない（縮尺どおりでない）")
        need(tuple(r["pt"]) == Rr["pt"] and abs(r["pt_px"][0] - X(Rr["pt"][0])) < 1e-6 and abs(r["pt_px"][1] - Y(Rr["pt"][1])) < 1e-6,
             f"② 三豊の点 {r['pt']} が記録（地上5階・柱のあいだ10.8メートル）の位置に無い")
        need(r["pt_px"][0] < r["zone"][0][0] and r["pt_px"][1] > r["zone"][1][1], "② 三豊の点が決まりの線の外に無い")
    if view == "items":
        it = g["items"]
        need(tuple(it["cards"]) == R["items"] and it["head"][1] == "ward", f"② 点検の項目 {it['cards']} が記録（瑞草区の報告 p.45）と違うか、区の色でない")
    return bad, n


def _judge_m23_b6(g, view, seq, R, texts=()):
    """🆕 23本目 ⑤b-6：第10〜11章・終章の見え方と、足した組の照合（記録＝R・形＝g）。"""
    bad, n = [], 0

    def need(cond, msg):
        nonlocal n
        n += 1
        if not cond:
            bad.append(msg)

    def close(a, b, tol=1e-6):
        return abs(a - b) <= tol
    if view == "cards" and g.get("set") == "bribe":
        need(tuple(g["cards"]["rows"]) == R["cards_bribe"] and g["cards"]["head"][1] == "state",
             f"② 受け取ったとされる額の札 {g['cards']['rows']} が記録（検察の報告 p.53）と違うか、国の色でない")
        lo, hi = min(R["bribe"]["amounts"]), max(R["bribe"]["amounts"])
        need(R["cards_bribe"][0][1] == f"{lo:,}万〜{hi:,}万ウォン" and R["cards_bribe"][1][1] == f"{sum(R['bribe']['amounts']):,}万ウォン",
             "② 額の幅と合計が15人の額（検察の報告 p.53）の最小・最大・合計と合わない")
    if view == "cards" and g.get("set") == "art":
        need((tuple(g["cards"]["head"]), tuple(g["cards"]["rows"])) == (R["cards_art"]["head"], R["cards_art"]["rows"]), "② 2026年の計画の札が記録（ソウル市の公告）と違う")
    if view == "desk":
        d = g["desk"]
        need(tuple(d["two"]) == R["desk"]["two"] and tuple(d["fix"]) == R["desk"]["fix"], f"② 窓口と直した数 {d} が記録（国会の報告 p.32＝207人→410人）と違う")
    if view == "tally":
        t = g["tally"]
        Rt = R["tally"]
        need((t["head"][0], t["total"], t["done"], t["left"]) == (Rt["head"], Rt["total"], Rt["done"], Rt["left"]),
             f"② 届けと確かめの数 {t['total']}・{t['done']}・{t['left']} が記録（ソウル市の報告 p.53＝1,566・1,485・81）と違う")
        need(Rt["total"] == Rt["done"] + Rt["left"], "② 記録の数が足し算で合わない（届け＝確かめた＋残り）")
        x0, x1 = t["x"]
        need(close((t["done_x"] - x0) / (x1 - x0), Rt["done"] / Rt["total"]), "② 確かめた数の棒の長さが件数の比と違う")
    if view == "toll":
        t = g["toll"]
        need((t["total"], tuple(t["parts"]), t["head"][1]) == (R["toll"]["total"], R["toll"]["parts"], R["toll"]["role"]),
             f"② 10月の数 {t['total']}＝{t['parts']} が記録（国政監査 p.24＝501＝471＋30）と違うか、市の色でない")
        need(sum(R["toll"]["parts"]) == R["toll"]["total"], "② 内訳の足し算が合計と合わない")
    if view == "koseki":
        need(g["koseki"] == R["koseki"], f"② 戸籍の整理 {g['koseki']} が記録（白書 p.92＝30人・11月29日）と違う")
    if view == "final":
        f = g["final"]
        need((tuple(f["cards"]), f["koseki"], f["oct"]) == (R["final"]["cards"], R["final"]["koseki"], R["final"]["oct"]),
             f"② 最終の数 {f} が記録（白書 p.92＝502・937・戸籍30／10月471）と違う")
        need(R["final"]["cards"][0] - R["final"]["koseki"] - R["final"]["oct"] == 1, "② 502−30 と 10月の471 の差が1人でない（語り）")
    if view == "ages":
        a = g["ages"]
        need(tuple(a["rows"]) == R["ages"] and sum(v for _t, v in R["ages"]) == R["ages_sum"],
             f"② 年代の表 {a['rows']} が記録（白書 p.93＝計502）と違う")
        vmax = max(v for _t, v in a["rows"])
        hmax = max(a["h"])
        need(all(close(h / hmax, v / vmax) for h, (_t, v) in zip(a["h"], a["rows"])), "② 棒の高さが人数の比と違う")
        need(a["rows"][a["top"]][1] == vmax, "② 明るくする棒がいちばん多い年代でない")
    if view == "most":
        mo = g["most"]
        need(tuple(mo["rows"]) == R["most"], f"② 比べる数 {mo['rows']} が記録（白書 p.92＝502・1970年の326）と違う")
        need(all(close((x - mo["x0"]) / mo["unit"], v) for x, (_t, _y, v) in zip(mo["x1"], mo["rows"])), "② 棒の長さが人数の比と違う")
    if view == "pen":
        p = g["pen"]
        need(tuple(p["rows"]) == R["pen"], f"② 罰の札 {p['rows']} が記録（検察の報告 p.50＝5年以下／法令＝無期または3年以上）と違う")
        yr = lambda x: (x - p["x0"]) / (p["x1"] - p["x0"]) * p["ymax"]   # noqa: E731
        for (xa, xb), (_t, a, b, _l) in zip(p["x"], R["pen"]):
            need(close(yr(xa), a) and (b is None and xb is None or b is not None and close(yr(xb), b)), "② 罰の棒の端が年の目盛りと合わない")
        need(p["inf"] > p["x1"], "② 無期の矢じりが目盛りの右の端の外に無い")
    if view == "haul":
        h = g["haul"]
        need(tuple(h["found"]) == R["haul"]["found"] and tuple(h["day"]) == R["haul"]["day"], f"② 見つかった数 {h['found']} が記録（国政監査 p.24＝142点・3,419点・8月14日）と違う")
        allt = list(h["texts"]) + list(texts)
        need(not any(w in t for w in R["haul"]["ng"] for t in allt), "② 瓦礫を運んだ場所の名が画面にある（名は出さない）")
    if view == "pay":
        p = g["pay"]
        need((p["head"], tuple(p["rows"]), p["avg"], p["yen"]) == (R["pay"]["head"], R["pay"]["rows"], R["pay"]["avg"], R["pay"]["yen"]),
             "② 補償の数が記録（白書 p.93＝1996年6月14日・464人分 1,758億・709人 1,003億・平均3億8千万）と違う")
    if view == "q3":
        need(tuple(g["q3"]) == R["q3"], f"② 問い {g['q3']} が冒頭の語り（c107）と違う")
    if view == "forms3":
        f = g["forms3"]
        Rf = R["forms3"]
        need(f["add"].replace("※", "").rstrip(" :") == Rf["add"] and tuple(f["roles"]) == Rf["roles"], "② 追加の罪名の行が記録（検察の報告 p.48）と違う")
        need(tuple((nm, " ".join(h)) for nm, h in f["sheets"]) == tuple((nm, t) for nm, t, _p in Rf["sheets"]), "② 別紙の題が記録（検察の報告 p.51〜53）と違う")
        for nm, t, pg in Rf["sheets"] + (("add", Rf["add"], Rf["add_page"]),):
            src_ = _m23_src_page(pg)
            if src_ is not None:
                need(re.sub(r"\s+", "", t) in src_, f"② 記録の題「{t}」が原文の頁（p.{pg}）に無い")
    if view == "acts":
        need((tuple(g["acts"]["cards"]), tuple(g["acts"]["ch"])) == (R["acts"]["cards"], R["acts"]["ch"]) and g["acts"]["head"][1] == "state",
             f"② 1つ目の表の札 {g['acts']['cards']} が記録（検察の報告 p.51＝語りの4つ）と違うか、章の印が違う")
    if view == "chair":
        c = g["chair"]
        need((tuple(c["head"]), tuple(c["cards"])) == (R["chair"]["head"], R["chair"]["cards"]), "② 会長の欄の札が記録の要約と違うか、会社の色でない")
        need(not any(w in t for w in R["chair"]["ng"] for t in list(c["cards"]) + list(texts)), "② 語りに無い時刻（14:30）を札にしている")
    if view == "fake":
        need(g["fake"]["head"][1] in R["fake"], "② 書類を作った人の色が市の色でない（検察の報告 p.53＝市の職員）")
    if view == "bribe":
        b = g["bribe"]
        Rb = R["bribe"]
        am = Rb["amounts"]
        city = sum(am[i] for i in Rb["city_rows"])
        need(len(am) == Rb["ward"][0] + Rb["city"][0] and (Rb["ward"][1], Rb["city"][1]) == (sum(am) - city, city),
             "② 区と市の額が15人の額（検察の報告 p.53）の足し算と合わない")
        need((b["rumor"], tuple(b["ward"]), tuple(b["city"])) == (Rb["rumor"], Rb["ward"], Rb["city"]), f"② 語られる額と記録の額 {b} が記録と違う")
        for x, v in zip(b["xs"], (Rb["rumor"], Rb["ward"][1], Rb["ward"][1] + Rb["city"][1])):
            need(close((x - b["x0"]) / b["unit"], v), "② 額の棒の長さが額の比と違う")
    if view == "shelf":
        need(g["shelf"]["years"] == R["shelf"]["years"] and g["shelf"]["r"][1] == R["shelf"]["r_role"], "② 図面を残す年と区の棚が記録（検察の報告 p.49＝5年・区にだけ）と違う")
    if view == "stages":
        need(tuple(g["stages"]["cards"]) == R["stages"] and g["stages"]["head"][1] == "state", f"② 判決の段階 {g['stages']['cards']} が判決の要旨（大96）と違う")
    if view == "chain":
        need(tuple(g["chain"]["cards"]) == R["stages"], f"② 鎖でつなぐ段階 {g['chain']['cards']} が判決の要旨（大96）と違う")
    if view == "gap":
        need((tuple(g["gap"]["l"]), tuple(g["gap"]["r"])) == (R["gap"]["l"], R["gap"]["r"]), "② 切れた線の両端の札が記録（大99）と違うか、区の色でない")
    if view == "causes":
        c = g["causes"]
        need((tuple(c["cards"]), c["gov"], tuple(c["marks"]), c["head"][1]) == (R["causes"]["cards"], R["causes"]["gov"], R["causes"]["marks"], "state"),
             "② 国会の報告の原因の札が記録（p.28＝設計・施工・監理・維持管理の欠陥と監督の不備）と違う")
    if view == "blocks":
        bl = g["blocks"]
        need((tuple(bl["low"]), tuple(bl["up"]), bl["wall"]) == (R["blocks"]["low"], R["blocks"]["up"], R["blocks"]["wall"]), "② 積み木の札が終章の語りと違う")
    if view == "stop":
        s = g["stop"]
        need((tuple(s["cards"]), tuple(s["marks"]), s["head"][1]) == (R["stop"]["cards"], R["stop"]["marks"], "state"), "② 止められた所の札が記録（国会の報告 p.28）と違う")
    if view == "open":
        need(g["open"] == R["open"], "② 開いたままの店の札が記録（国会の報告 p.32）と違う")
    return bad, n


def _selftest_m23(ok):
    """23本目 ⑤b-3：模式図の検算（正しい場面・陽性対照＝描く側の表を壊す・筋・見る向きの合図）。
    🔴 2026-10-20（17本目 ⑤b-1）：記録の表 REC_M23 は見本 `fixture_ep23` から（`selftest` が `apply(gate, tables_only=True)` で差し込んだ中で呼ぶ）"""
    import mech23 as M
    N = "模式"
    good = dict(
        sec=dict(view="section", start=dict(a="on"), steps=[dict(state=dict(fall="top")), dict(state=dict(fall="all")), dict(state=dict(load="on"))], note=N),
        bl=dict(view="bldg", steps=[dict(state=dict(hi="a5", cell="on")), dict(state=dict(bulge="on")), dict(state=dict(closed="on"))], note=N),
        pl=dict(view="plan", start=dict(floor="roof"), steps=[dict(state=dict(sink="on"))], note=N),
        gr=dict(view="plan", start=dict(floor="grid"), steps=[dict(state=dict(nums="on")), dict(state=dict(hit="on"), tag=dict(t="5列E行", at="g"))],
                rel=[dict(t="5列E行", src="大96 p1")], note=N),
        ck=dict(view="clocks", start=dict(set="fall"), steps=[dict(state=dict(k0="on", k1="on", k2="on"))], note=N),
        fo=dict(view="form", steps=[dict(state=dict(h0="on"))], note=""),
        tb=dict(view="table", steps=[dict(state=dict(r2="on")), dict(state=dict(why="on"))], note=N),
        bk=dict(view="bunko", steps=[dict(state=dict(br="on"))], note=N),
        sl=dict(view="slab", start=dict(z="col", fl="5"), steps=[dict(state=dict(crack="on")), dict(state=dict(sink="on")), dict(state=dict(punch="on"))], note=N),
    )
    for k, kw in good.items():
        bad, nn = judge("m23", kw)
        g_ = not bad
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 23本目 正しい場面 {k}: {'合格' if not bad else bad[0]}（{nn}件）")
    pos = [
        ("屋上の沈みを3か所に", "SINK_PTS", M.SINK_PTS[:3], "pl", "沈んだ所"),
        ("5階の食堂の閉めた所を一部だけに", "CLOSED", dict(a5=(0.10, 0.30), a4=(0.55, 0.72)), "bl", "閉めた所 a5"),
        ("印の柱を4列E行に", "GRID_HIT", (("4", "E"), ("5", "F")), "gr", "印の柱"),
        ("時計の時刻を17:50に", "CK_SET", dict(M.CK_SET, fall=(("17:50", "", "国会の報告", "state"),) + M.CK_SET["fall"][1:]), "ck", "時計の時刻"),
        ("別紙2 の句を言い換え", "FORM", dict(M.FORM, cell=("삼풍백화점의 무량판공법으로", "계산 설계한 건축구조기술사로서 …")), "fo", "欄の句"),
        ("点検の2回目を6月10日からに", "TB_ROWS", (M.TB_ROWS[0], ("2回目", (6, 10), (6, 30), M.TB_ROWS[1][3])), "tb", "点検の期間"),
        ("文庫本を縦15センチに", "BK_BOOK_MM", (105.0, 150.0), "bk", "文庫本"),
        ("各階の使い道を取り替え", "SC_USE", dict(M.SC_USE, a=(((5, 5), "売り場"), ((1, 4), "食堂街"))), "sec", "使い道"),
    ]
    for name, attr, val, key, frag in pos:
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            bad, _ = judge("m23", good[key])
        finally:
            setattr(M, attr, keep)
        g_ = any(frag in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 陽性対照：{name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 筋：うろこの前にたわみ・止める前に水を抜く
    for name, kw in (("うろこの前にたわみ", dict(view="plan", start=dict(floor="roof"), steps=[dict(state=dict(sag="on"))], note=N)),
                     ("止める前に水を抜く", dict(view="tower", start=dict(run="on"), steps=[dict(state=dict(drain="on"))], note=N)),
                     ("札の時刻が記録に無い", dict(view="crack", steps=[dict(tag=dict(t="13:00", at="t"))], rel=[dict(t="13:00", src="x")], note=N))):
        bad, _ = judge("m23", kw)
        g_ = bool(bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 陽性対照（筋・札）：{name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 見る向きの合図（PLAN の見る向き × 左上の札）
    for name, plan_t, lab, want_bad in (("横からの PLAN に横からの札", "見る向き：横から（断面）", "横から見た建物（断面）", False),
                                         ("上からの PLAN に斜めからの札", "見る向き：上から", "斜めから見た建物", True),
                                         ("見る向きの無い PLAN", "見た目の型：時計", "記録ごとの時刻", False)):
        b_ = bool(view_dir_check(plan_t, lab))
        g_ = b_ == want_bad
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 23本目 見る向きの合図：{name}: {'鳴る' if b_ else '鳴らない'}")
    for nm, fn in (("崩れた床を戻す", lambda: M.m23("section", [dict(state=dict(fall="all")), dict(state=dict(fall="top"))], note=N)),
                   ("段で床を替える", lambda: M.m23("plan", [dict(state=dict(floor="f5"))], start=dict(floor="roof"), note=N)),
                   ("note に模式が無い", lambda: M.m23("bldg", [dict()], note="形"))):
        try:
            fn()
            g_ = False
        except ValueError:
            g_ = True
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 23本目 型の見張り：{nm}: {'組めない（止まった）' if g_ else '🔴 組めた'}")
    return _selftest_m23_b4(ok)


def _selftest_m23_b4(ok):
    """🆕 23本目 ⑤b-4：第4〜7章の見え方の検算（正しい場面・陽性対照＝描く側の表を壊す・筋）。"""
    import mech23 as M
    N = "模式"
    good = dict(
        wall=dict(view="wall", steps=[dict(state=dict(rubble="clear"))], note=N),
        cal=dict(view="cal", start=dict(set="rescue", d0="on"), steps=[dict(state=dict(d1="on"))], note=""),
        cal89=dict(view="cal", start=dict(set="move89"), steps=[dict(state=dict(band="on", open="on"))], note=""),
        cards=dict(view="cards", steps=[dict(state=dict(r0="on", r1="on", r2="on"))], note=""),
        nums=dict(view="nums", steps=[dict(state=dict(place="on", n="on"))], note=N),
        sheets=dict(view="sheets", steps=[dict(state=dict(add="on"))], note=N),
        rank=dict(view="rank", steps=[dict(state=dict(r0="on", r1="on"))], note=N),
        colx=dict(view="colx", steps=[dict(state=dict(both="on"))], note=N),
        spans=dict(view="spans", steps=[dict(state=dict(sag="on"))], note=N),
        persq=dict(view="persq", steps=[dict(state=dict(l="on", r="on"))], note=N),
        vs=dict(view="vs", start=dict(set="count"), steps=[dict(state=dict(c0="on", c1="on")), dict(state=dict(lit="on"))], note=""),
        rumor=dict(view="vs", start=dict(set="rumor"), steps=[dict(state=dict(c0="on")), dict(state=dict(c1="on"))], note=""),
        temp=dict(view="bldg", start=dict(under="on"), steps=[dict(state=dict(hi="temp")), dict(state=dict(chk="on"))], note=N),
        area=dict(view="plan", start=dict(floor="area"), steps=[dict(state=dict(aplan="on")), dict(state=dict(add="on"))], note=N),
        dp=dict(view="plan", start=dict(floor="grid", dp="thin"), steps=[dict(state=dict(dp="miss")), dict(state=dict(miss_lit="on"))], note=N),
        ct=dict(view="plan", start=dict(floor="ct"), steps=[dict(state=dict(ct="back")), dict(state=dict(ct="moved"))], note=N),
        bar=dict(view="slab", start=dict(z="span", fl="5", bar="ok"), steps=[dict(state=dict(bar="sunk"))], note=N),
        tw3=dict(view="tower", start=dict(set="three"), steps=[dict(state=dict(load="on")), dict(state=dict(roof="on"))], note=N),
        drag=dict(view="drag", steps=[dict(state=dict(split="on")), dict(state=dict(pos="moved"))], note=N),
        crack=dict(view="crack", start=dict(fl="roof", crack="on"), steps=[dict(state=dict(crack="long"))], note=N),
    )
    for k, kw in good.items():
        bad, nn = judge("m23", kw)
        g_ = not bad
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 23本目 ⑤b-4 正しい場面 {k}: {'合格' if not bad else bad[0]}（{nn}件）")
    pos = [
        ("H形鋼を1か所に", "WL", dict(M.WL, hb=M.WL["hb"][:1]), "wall", "H形鋼"),
        ("救出の日を7月10日に", "CAL_SET", dict(M.CAL_SET, rescue=dict(M.CAL_SET["rescue"], mark=(1995, 7, 10))), "cal", "暦の印"),
        ("開店を12月2日に", "CAL_SET", dict(M.CAL_SET, move89=dict(M.CAL_SET["move89"], open=(1989, 12, 2))), "cal89", "開店"),
        ("救助の数を933人に", "CARDS", dict(M.CARDS, rows=(("救助された人", "933人"),) + M.CARDS["rows"][1:]), "cards", "札の数"),
        ("引き渡しを310件に", "NUMS", dict(M.NUMS, boxes=(M.NUMS["boxes"][0], ("確かめて引き渡し", "310件"))), "nums", "センターの数"),
        ("継ぎ足す紙を15枚に", "SH", dict(M.SH, n=15), "sheets", "継ぎ足した紙"),
        ("売り上げを6位に", "RANK", dict(M.RANK, rows=(("売り上げ", 6), ("売り場の大きさ", 2))), "rank", "順位"),
        ("図面の鉄筋を10本に", "CX_COLS", (M.CX_COLS[0], ("図面", 60.0, 10, "ALERT")), "colx", "柱の直径"),
        ("柱のあいだを10.5メートルに", "SP_LONG_M", 10.5, "spans", "柱のあいだ"),
        ("大人を5人に", "PQ", dict(M.PQ, n=(5, 4)), "persq", "人の数"),
        ("白書の台数を3台に", "VS_SET", dict(M.VS_SET, count=(M.VS_SET["count"][0], (("白書", "3台", "city"),))), "vs", "台数の札"),
        ("判決の重さを12トンに", "VS_SET", dict(M.VS_SET, rumor=(M.VS_SET["rumor"][0], (("判決", "1基12トン", "state"), M.VS_SET["rumor"][1][1]))), "rumor", "記録の札"),
        ("仮の使用を4階まで", "HI", dict(M.HI, temp=M.HI["temp"] + (("a", 4),)), "temp", "仮の使用の階"),
        ("増えた床を2,000に", "AREA", dict(M.AREA, add=2000), "area", "床の広さ"),
        ("板の無い所を5列E行に", "DP_MISS", (("5", "E"),), "dp", "板の無い所"),
        ("冷却塔を4基に", "CT", dict(M.CT, back=M.CT["back"] + ((1200.0, 470.0),), front=M.CT["front"] + ((1250.0, 690.0),)), "ct", "冷却塔"),
        ("沈んだ鉄筋を正しい位置に", "SLB", dict(M.SLB, sunk=M.SLB["ok"]), "bar", "沈んだ鉄筋"),
        ("屋上の冷却塔を4基に", "TW3", dict(M.TW3, n=4), "tw3", "冷却塔"),
        ("ひびの枝を消す", "CR_BRANCH", (), "crack", "ひびが育って"),
    ]
    for name, attr, val, key, frag in pos:
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            try:
                bad, _ = judge("m23", good[key])
            except Exception as e:    # noqa: BLE001
                bad = [f"組めない：{e}"]
        finally:
            setattr(M, attr, keep)
        g_ = any(frag in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 ⑤b-4 陽性対照：{name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 暦の曜日（描く側の升目の計算を壊す＝1列ずらす）
    keep = M.cal_cells
    M.cal_cells = lambda: [(d, (c + 1) % 7, r) for d, c, r in keep()]
    try:
        bad, _ = judge("m23", good["cal"])
    finally:
        M.cal_cells = keep
    g_ = any("曜日" in b for b in bad)
    ok &= g_
    print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 ⑤b-4 陽性対照：暦の曜日を1列ずらす: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    for name, kw in (("道がふさがる前に車が止まる", dict(view="road", start=dict(amb="on"), steps=[dict(state=dict(amb="blocked"))], note=N)),
                     ("内側の帯筋の前に切る", dict(view="hoop", steps=[dict(state=dict(l="on")), dict(state=dict(cut="on"))], note=N)),
                     ("仮の使用の前に検査なし", dict(view="bldg", start=dict(under="on"), steps=[dict(state=dict(chk="on"))], note=N))):
        bad, _ = judge("m23", kw)
        g_ = bool(bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 ⑤b-4 陽性対照（筋）：{name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    return _selftest_m23_b5(ok)


def _selftest_m23_b5(ok):
    """🆕 23本目 ⑤b-5：第8〜9章の見え方の検算（正しい場面・陽性対照＝描く側の表を壊す・筋）。"""
    import mech23 as M
    N = "模式"
    good = dict(
        use=dict(view="load", start=dict(set="use"), steps=[dict(state=dict(sk="on")), dict(state=dict(food="on"))], note=N),
        lists=dict(view="lists", start=dict(k="on"), steps=[dict(state=dict(w="on")), dict(state=dict(diff="on"))], note=""),
        over=dict(view="over", steps=[dict(state=dict(pre="on")), dict(state=dict(add="on"))], note=N),
        cover=dict(view="cover", steps=[dict(state=dict(q="on")), dict(state=dict(cover="on"))], note=N),
        duct=dict(view="duct", steps=[dict(state=dict(duct="on")), dict(state=dict(cut="on")), dict(state=dict(load="on"))], note=N),
        opening=dict(view="opening", steps=[dict(state=dict(none="on")), dict(state=dict(weak="on"))], note=N),
        joint=dict(view="joint", start=dict(fl="5"), steps=[dict(state=dict(bar="lit")), dict(state=dict(ruler="on"))], note=N),
        fall=dict(view="joint", steps=[dict(state=dict(fall="on")), dict(state=dict(wall="on"))], note=N),
        hook=dict(view="hook", steps=[dict(state=dict(l="on")), dict(state=dict(r="on"))], note=N),
        walls=dict(view="section", start=dict(fall="all"), steps=[dict(state=dict(walls="on")), dict(state=dict(joints="on"))], note=N),
        stack=dict(view="stack", steps=[dict(state=dict(items="on")), dict(state=dict(col="on")), dict(state=dict(noreinf="on"))], note=N),
        f4=dict(view="bldg", steps=[dict(state=dict(hi="f4", lamp="on")), dict(state=dict(shake="on")), dict(state=dict(hi="f4a5"))], note=N),
        two=dict(view="plan", start=dict(floor="two"), steps=[dict(state=dict(kit="on")), dict(state=dict(path="on"))], note=N),
        three=dict(view="plan", start=dict(floor="three"), steps=[dict(state=dict(marks="on")), dict(state=dict(up="on"))], note=N),
        roof=dict(view="slab", start=dict(z="col", fl="roof"), steps=[dict(state=dict(dpm="on", leak="on", crack="on"))], note=N),
        gauge=dict(view="tower", start=dict(gauge="on"), steps=[dict(state=dict(gauge="low"))], note=N),
        insp=dict(view="insp", steps=[dict(state=dict(eye="on")), dict(state=dict(doc="on"))], note=N),
        rule=dict(view="rule", start=dict(zone="on"), steps=[dict(state=dict(pt="on"))], note=N),
        items=dict(view="items", steps=[dict(state=dict(c0="on")), dict(state=dict(c1="on", no="on"))], note=""),
    )
    for k, kw in good.items():
        bad, nn = judge("m23", kw)
        g_ = not bad
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 23本目 ⑤b-5 正しい場面 {k}: {'合格' if not bad else bad[0]}（{nn}件）")
    pos = [
        ("国会の箱から花壇を抜く", "LISTS", ((M.LISTS[0][0], M.LISTS[0][1], M.LISTS[0][2][:3]), M.LISTS[1]), "lists", "箱の物"),
        ("余計な重さを300キロに", "OVER_KG", 300.0, "over", "余計な重さ"),
        ("穴を壁の長さの半分に", "DU_CUT", (80.0, 160.0), "duct", "穴の長さの割合"),
        ("入れるべき長さを60センチに", "JT_CM", dict(M.JT_CM, need=60.0), "joint", "物差しの長さ"),
        ("曲げる形の2本を同じ長さに", "HK_CM", (64.0, 64.0), "hook", "長さの比"),
        ("積み木から石の庭を抜く", "SK_ITEMS", M.SK_ITEMS[:5], "stack", "積み木の物"),
        ("柱の太さの比を 600：700 に", "SK_COL_MM", (600.0, 700.0), "stack", "柱の太さの比"),
        ("4階の帯を A棟だけに", "HI", dict(M.HI, f4=(("a", 4),), f4a5=(("a", 4), ("a", 5))), "f4", "4階の帯"),
        ("床の名を3階からに", "P3", dict(M.P3, lab=("3階", "4階", "5階")), "three", "床の名"),
        ("決まりの線を15階に", "RL_LINE", dict(M.RL_LINE, floors=15), "rule", "決まりの線"),
        ("三豊の点を地上6階に", "RL_PT", (10.8, 6), "rule", "三豊の点"),
        ("点検の項目から看板を抜く", "ITEMS", dict(M.ITEMS, cards=M.ITEMS["cards"][:4]), "items", "点検の項目"),
        ("調節で水を増やす", "TG", dict(M.TG, lv=dict(M.TG["lv"], low=500.0)), "gauge", "水の高さ"),
    ]
    for name, attr, val, key, frag in pos:
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            try:
                bad, _ = judge("m23", good[key])
            except Exception as e:    # noqa: BLE001
                bad = [f"組めない：{e}"]
        finally:
            setattr(M, attr, keep)
        g_ = any(frag in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 ⑤b-5 陽性対照：{name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 残った壁（描く側の位置の計算を壊す＝B棟へずらす）
    keep = M.sc_walls
    M.sc_walls = lambda: tuple((x0 + 650.0, x1 + 650.0) for x0, x1 in keep())
    try:
        bad, _ = judge("m23", good["walls"])
    finally:
        M.sc_walls = keep
    g_ = any("残った壁" in b for b in bad)
    ok &= g_
    print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 ⑤b-5 陽性対照：残った壁を B棟へずらす: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    for name, kw in (("決まりの線の前に三豊の点", dict(view="rule", steps=[dict(state=dict(pt="on"))], note=N)),
                     ("鉄筋を見せる前に物差し", dict(view="joint", steps=[dict(state=dict(ruler="on"))], note=N)),
                     ("床が落ちる前に立ったままの壁", dict(view="joint", steps=[dict(state=dict(wall="on"))], note=N)),
                     ("崩れる前に残った壁", dict(view="section", steps=[dict(state=dict(walls="on"))], note=N)),
                     ("積み木の前に補強なし", dict(view="stack", steps=[dict(state=dict(noreinf="on"))], note=N))):
        bad, _ = judge("m23", kw)
        g_ = bool(bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 ⑤b-5 陽性対照（筋）：{name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    return _selftest_m23_b6(ok)


def _selftest_m23_b6(ok):
    """🆕 23本目 ⑤b-6：第10〜11章・終章の見え方の検算（正しい場面・陽性対照＝描く側の表を壊す・筋）。"""
    import mech23 as M
    N = "模式"
    good = dict(
        desk=dict(view="desk", steps=[dict(state=dict(two="on")), dict(state=dict(one="on", fix="on"))], note=N),
        tally=dict(view="tally", steps=[dict(state=dict(total="on", done="on")), dict(state=dict(left="on"))], note=""),
        toll=dict(view="toll", steps=[dict(), dict(state=dict(total="on")), dict(state=dict(parts="on"))], note=""),
        koseki=dict(view="koseki", steps=[dict(state=dict(n="on")), dict(state=dict(done="on"))], note=N),
        final=dict(view="final", steps=[dict(state=dict(cards="on")), dict(state=dict(calc="on"))], note=""),
        ages=dict(view="ages", steps=[dict(state=dict(bars="on")), dict(state=dict(top="on"))], note=""),
        most=dict(view="most", steps=[dict(state=dict(r0="on")), dict(state=dict(r1="on"))], note=""),
        pen0=dict(view="pen", steps=[dict(state=dict(q="on")), dict(state=dict(b0="on"))], note=""),
        pen1=dict(view="pen", start=dict(q="on", b0="on"), steps=[dict(state=dict(law="on")), dict(state=dict(b1="on"))], note=""),
        haul=dict(view="haul", steps=[dict(), dict(state=dict(truck="on")), dict(state=dict(found="on"))], note=N),
        pay=dict(view="pay", steps=[dict(state=dict(r0="on")), dict(state=dict(sub="on")), dict(state=dict(r1="on"))], note=""),
        q3=dict(view="q3", steps=[dict(state=dict(lit="on"))], note=""),
        forms3=dict(view="forms3", steps=[dict(state=dict(add="on")), dict(state=dict(sheets="on"))], note=""),
        acts=dict(view="acts", steps=[dict(state=dict(c0="on")), dict(state=dict(c1="on")), dict(state=dict(seen="on"))], note=""),
        chair=dict(view="chair", steps=[dict(state=dict(c12="on")), dict(state=dict(c3="on"))], note=N),
        fake=dict(view="fake", steps=[dict(state=dict(site="on")), dict(state=dict(doc="on"))], note=N),
        bribe=dict(view="bribe", steps=[dict(state=dict(rumor="on")), dict(state=dict(ward="on")), dict(state=dict(city="on"))], note=""),
        cbribe=dict(view="cards", start=dict(set="bribe"), steps=[dict(state=dict(r0="on")), dict(state=dict(r1="on", r2="on"))], note=""),
        cart=dict(view="cards", start=dict(set="art"), steps=[dict(state=dict(r0="on"))], note=""),
        crescue=dict(view="cards", steps=[dict(state=dict(r0="on")), dict(state=dict(r1="on", r2="on"))], note=""),
        shelf=dict(view="shelf", steps=[dict(state=dict(rule="on"))], note=N),
        stages=dict(view="stages", steps=[dict(state=dict(cards="on")), dict(state=dict(fault="on"))], note=N),
        chain=dict(view="chain", steps=[dict(state=dict(link="on")), dict(state=dict(one="on"))], note=N),
        gap=dict(view="gap", steps=[dict(state=dict(line="on")), dict(state=dict(cut="on"))], note=N),
        causes=dict(view="causes", steps=[dict(state=dict(four="on")), dict(state=dict(gov="on"))], note=N),
        open=dict(view="open", steps=[dict(state=dict(sig="on")), dict(state=dict(sign="on"))], note=N),
        blocks=dict(view="blocks", steps=[dict(state=dict(low="on")), dict(state=dict(up="on"))], note=N),
        stop=dict(view="stop", steps=[dict(state=dict(cards="on")), dict(state=dict(mk="on")), dict(state=dict(one="on"))], note=""),
    )
    for k, kw in good.items():
        bad, nn = judge("m23", kw)
        g_ = not bad
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 23本目 ⑤b-6 正しい場面 {k}: {'合格' if not bad else bad[0]}（{nn}件）")
    pos = [
        ("直した数を207→401に", "DESK", dict(M.DESK, fix=(207, 401)), "desk", "直した数"),
        ("確かめた数を1,458に", "TALLY", dict(M.TALLY, done=("確かめが済んだ", 1458)), "tally", "届けと確かめの数"),
        ("10月の内訳を470＋31に", "TOLL", dict(M.TOLL, parts=(("遺体で確かめた", 470), ("亡くなったと認めた", 31))), "toll", "10月の数"),
        ("戸籍の日を11月30日に", "KOSEKI", dict(M.KOSEKI, day=(11, 30)), "koseki", "戸籍の整理"),
        ("けがをした人を933人に", "FINAL", dict(M.FINAL, cards=(("亡くなった人", 502), ("けがをした人", 933))), "final", "最終の数"),
        ("年代の51〜60歳を20人に（割合の欄の値）", "AGES", M.AGES[:5] + (("51〜60歳", 20),) + M.AGES[6:], "ages", "年代の表"),
        ("1970年の沈没を292人に", "MOST", dict(M.MOST, rows=(M.MOST["rows"][0], ("船の沈没", "1970年", 292, "LINE"))), "most", "比べる数"),
        ("事故の前の罰を3年以下に", "PEN", dict(M.PEN, rows=(("事故の前", "手抜き工事で壊れたとき", 0.0, 3.0, "LINE", "5年以下の懲役"), M.PEN["rows"][1])), "pen0", "罰の"),
        ("集める場所に地名を書く", "HAUL", dict(M.HAUL, labels=("崩れた百貨店の跡", "난지도の集める場所")), "haul", "場所の名"),
        ("平均を3億7千万に", "PAY", dict(M.PAY, avg="3億7千万ウォン"), "pay", "補償の数"),
        ("2つ目の問いを言い換える", "Q3", (M.Q3[0], "なぜビルは崩れたのか", M.Q3[2]), "q3", "問い"),
        ("別紙3 の題を別の言葉に", "FORMS3", dict(M.FORMS3, sheets=M.FORMS3["sheets"][:2] + (("별지 3", ("공무원", "범죄사실 요지")),)), "forms3", "別紙の題"),
        ("1つ目の表の札から耐力壁を抜く", "ACTS", dict(M.ACTS, cards=M.ACTS["cards"][:3] + ("柱を細くした",)), "acts", "1つ目の表の札"),
        ("会長の欄に時刻を足す", "CHAIR", dict(M.CHAIR, cards=M.CHAIR["cards"][:1] + ("14:30にひびの報告",) + M.CHAIR["cards"][2:]), "chair", "会長の欄"),
        ("区の額を8,000万に", "BRIBE", dict(M.BRIBE, ward=(12, 8000)), "bribe", "語られる額と記録の額"),
        ("額の幅の上を1,300万に", "CARD_SETS", dict(M.CARD_SETS, bribe=dict(M.CARD_SETS["bribe"], rows=(("1人あたり", "100万〜1,300万ウォン"),) + M.CARD_SETS["bribe"]["rows"][1:])),
         "cbribe", "受け取ったとされる額"),
        ("図面を残す決まりを10年に", "SHELF", dict(M.SHELF, years=10), "shelf", "図面を残す年"),
        ("判決の段階から計画を抜く", "STAGES", dict(M.STAGES, cards=M.STAGES["cards"][1:]), "stages", "判決の段階"),
        ("区の札を市の色に", "GAP", dict(M.GAP, l=("区の職員の違反", "city")), "gap", "切れた線"),
        ("国会の原因から監理を抜く", "CAUSES", dict(M.CAUSES, cards=("設計", "工事", "建ったあとの管理")), "causes", "原因の札"),
        ("止められた所の印を全部欠陥に", "STOP", dict(M.STOP, marks=("欠陥",) * 5), "stop", "止められた所"),
    ]
    for name, attr, val, key, frag in pos:
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            try:
                bad, _ = judge("m23", good[key])
            except Exception as e:    # noqa: BLE001
                bad = [f"組めない：{e}"]
        finally:
            setattr(M, attr, keep)
        g_ = any(frag in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 ⑤b-6 陽性対照：{name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 棒の長さ（描く側の位置の計算を壊す＝確かめた数の棒を1割長く・罰の棒の端を1年ずらす）
    for name, attr, fn, key, frag in (("確かめた数の棒を1割長く", "tl_x", lambda keep: (lambda v: keep(v * 1.1)), "tally", "棒の長さ"),
                                      ("罰の目盛りを1年ずらす", "pn_x", lambda keep: (lambda y: keep(y + (1.0 if y else 0.0))), "pen0", "罰の棒の端"),
                                      ("額の棒を1割長く", "br_x", lambda keep: (lambda v: keep(v * 1.1)), "bribe", "額の棒の長さ")):
        keep = getattr(M, attr)
        setattr(M, attr, fn(keep))
        try:
            bad, _ = judge("m23", good[key])
        finally:
            setattr(M, attr, keep)
        g_ = any(frag in b for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 ⑤b-6 陽性対照：{name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    for name, kw in (("合計の前に内訳", dict(view="toll", steps=[dict(state=dict(parts="on"))], note="")),
                     ("2つの窓口の前にまとめる", dict(view="desk", steps=[dict(state=dict(one="on"))], note=N)),
                     ("事故の前の罰の前に重くなった罰", dict(view="pen", start=dict(q="on"), steps=[dict(state=dict(law="on", b1="on"))], note="")),
                     ("区の12人の前に市の3人", dict(view="bribe", steps=[dict(state=dict(rumor="on")), dict(state=dict(city="on"))], note="")),
                     ("札の前に1人ではない", dict(view="stop", steps=[dict(state=dict(cards="on")), dict(state=dict(one="on"))], note=""))):
        bad, _ = judge("m23", kw)
        g_ = bool(bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 23本目 ⑤b-6 陽性対照（筋）：{name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    return ok


# ══════════════════════════════════════════════════════════
#  🆕 17本目 ⑤b-5（2026-10-20）：図解（m17＝`tools/mech17.py`・第1〜7章の25カット）
#   記録の値は門番の側（§5b-88）＝描く側の表（FACTORS・CK2_T・HR_V・TH_PTS・PT_DEG …）と別に持ち、
#   ①形・表・色（f.mech["geo"]）を記録で ②**基図と段の層の全部の字**の数を rel で（札だけでなく描いた字も）③句を原文の頁で（手元に原文があるとき）照らす。
#   原文＝報告書 96-5 の通し頁（`ref/ep17/src/ep17_pages.txt`＝git の外。Actions では句の照合だけ飛ばす）。頁の無い資料（付図5・付図29）は句を持たない
# ══════════════════════════════════════════════════════════
REC_M17 = dict(
    factors=dict(
        items=(("誤ってゴー・レバー", "crew", "報告書 p95", "副操縦士が誤ってゴー・レバーを作動させたこと"),
               ("解除しないまま自動操縦", "crew", "報告書 p95", "ゴー・アラウンド・モードが解除されていない状態で、APをエンゲージし進入を継続したこと"),
               ("重い操縦輪を押し続けた", "crew", "報告書 p95", "操縦輪の操舵が重い状態であるにもかかわらず、機長の指示の下で副操縦士が操縦輪の押し下げ操作を続けたこと"),
               ("板と昇降舵が食い違った", "plane", "報告書 p95", "THSとエレベータが整合することなく作動し、異常なアウト・オブ・トリム状態になったこと"),
               ("知らせる警報が無かった", "plane", "報告書 p95", "直接的かつ積極的に操縦士に知らせる警報・認識機能がなかったこと"),
               ("仕組みの理解に欠けた", "crew", "報告書 p96", "理解に欠ける点があったこと"),
               ("交替の時機が遅れた", "crew", "報告書 p96", "操縦の交替の時機が遅れ"),
               ("アルファ・フロアの作動", "plane", "報告書 p96", "アルファ・フロア機能が、異常なアウト・オブ・トリム状態と適切に整合することなく作動し"),
               ("立て直しが適切さを欠く", "crew", "報告書 p96", "異常な飛行状態からの回復操作に適切さを欠いたこと"),
               ("2人の連携が不適切", "crew", "報告書 p96", "クルー・コーディネーションが適切に行われなかったこと"),
               ("改修されていなかった", "airline", "報告書 p96", "技術通報SBA300-22-6021による改修が行われていなかったこと"),
               ("推奨のまま・命令なし", "maker", "報告書 p96", "最も優先度の高いMandatoryとして発行しなかったこと")),
        who=dict(crew=("操縦の2人", "company"), plane=("機体の作り", "ship"), airline=("航空会社", "LINE"), maker=("メーカーと当局", "airbus")),
        # 🆕 ⑤b-6b：k11・k12＝ca14（要因11＝航空会社・12＝メーカーと設計・製造国の当局）・cmd＝cb02（改修の区分と命令＝要因12）
        mk=dict(design=(1, 5, 6), crew=(7, 9, 10), k11=(11,), k12=(12,), cmd=(12,)),
        mk_quote=(("報告書 p95", "スラスト・レバーの通常の操作中に誤って作動させ得る可能性のある機構であったことが寄与"),
                  ("報告書 p96", "AFS(AutomaticFlightSystem)に関する記述が分かりにくいことが寄与"),
                  ("報告書 p96", "操縦交替後の飛行状況の把握及び異常な飛行状態からの回復操作に適切さを欠いたこと"),
                  ("報告書 p96", "設計、製造国の耐空性管理当局が、速やかに上述のSBの実施に係る耐空性改善命令を発行"))),
    clock2=dict(utc="11:14:05", jst="20:14:05", add=9, units=(("フィート", "メートル"), ("ノット", "時速（キロ）")),
                quote=(("報告書 p4", "時刻は協定世界時で記す"), ("報告書 p4", "08時53分協定世界時(日本標準時17時53分)"),
                       ("報告書 p51", "11時14分05秒に副操縦士がゴー・レバーを作動させた"), ("報告書 p44", "気圧高度約1,070ft"), ("報告書 p56", "速度127kt"))),
    seats=dict(names=("機長", "副操縦士"), age="42", af=("1970-09", "1989-01"), years=18, roles=("見守り・確かめる役", "操縦する役"), order="20:00",
               quote=(("報告書 p17", "機長男性42歳"), ("報告書 p38", "台湾空軍のパイロットとして1970年9月から1989年1月まで勤務"),
                      ("報告書 p42", "00分11秒機長(PNF)は、副操縦士(PF)に対し、自分で判断して自分で操縦するように指示"),
                      ("報告書 p57", "機長は、ILS進入時に副操縦士にPF業務を実施させていた"))),
    hours=dict(rows=(("この型（A300-600R）", 1350 + 27 / 60), ("空軍のころから全部", 8340 + 19 / 60)),
               career=("1989年 入社", "747の副操縦士", "1992年12月 この型の機長"),
               quote=(("報告書 p17", "総飛行時間8,340時間19分同型式機飛行時間1,350時間27分"), ("報告書 p38", "1989年2月1日、同公司に入社"),
                      ("報告書 p38", "B747-200、-400の副操縦士を経て"), ("報告書 p38", "同年12月1日に同公司のA300-600Rの機長に昇格"))),
    train=dict(steps=("地上の学科（教室）", "シミュレーター", "実際の機体"), hours="3",
               quote=(("報告書 p38", "仏国のアエロフォーメーション社において地上学科、シミュレータによる訓練及び実飛行時間3時間の訓練を受けた"),
                      ("報告書 p38", "副操縦士は、1990年4月16日"))),
    area=dict(ratio=3, quote=(("報告書 p55", "THS(エレベータを含む。)の面積は、エレベータの面積のおよそ3倍"),)),
    afs=dict(items=(("自動操縦（AP）", "舵を動かす"), ("自動推力（ATS）", "推力を整える"), ("飛行の指示（FD）", "画面の印で示す")),
             quote=(("報告書 p51", "FDはGOAROUNDモードになり、ATSはTHRモードにエンゲージした"), ("報告書 p95", "AP(AutoPilot)"))),
    band=dict(ft="400", m="120", out=("ランド", "ゴー・アラウンド"),
              quote=(("報告書 p78", "LANDTrack(対地高度400ft以下)及びGOAROUNDモード以外のモードでは操縦輪にピッチ方向に15kg以上の力を加えるとAPがディスエンゲージ"),)),
    modes=dict(start="ゴー・アラウンド・モード",
               rows=dict(a=("縦と横の両方で選び直す", ("抜ける",)), b=("縦だけ選び直す", ("画面の文字は消える", "働きは残る")),
                         c=("ランドのボタンを押す", ("抜けられない",))),
               cols=dict(a=("OK",), b=("AMBER", "ALERT"), c=("ALERT",)),
               quote=(("報告書 p54", "ラテラル及びロンジチュヂィナルの双方にそれぞれLANDモード以外のモードを選択しなければならず"),
                      ("報告書 p54", "直接LANDモードのボタンを押すことによって解除することはできない"),
                      ("報告書 p54", "いずれかのモードを選択すれば、FMAのGOAROUND表示は消える"),
                      ("報告書 p81", "実際にはGOAROUNDの機能が完全にディスエンゲージされたことにはならない"),
                      ("報告書 p54", "LANDモードのスイッチを押すことのみであったと推定"))),
    fcom=dict(fma=("V/S", "HDG"), rows=("縦のモードを選ぶ → 解ける", "横のモードを選ぶ → 解ける"), miss="縦だけでは働きが残る",
              rec=("勧告（報告書）", "表示の変化と働きの変化の対比"),
              quote=(("報告書 p81", "V/SとラテラルのモードであるHDGが表示"), ("報告書 p81", "あたかもGOAROUNDモードがディスエンゲージされたかのように見える"),
                     ("報告書 p81", "GOAROUNDモードはディスエンゲージし、横方向(ラテラル)のモードであるHDGモードがエンゲージされる"),
                     ("報告書 p82", "ロンジチュジナルのモードのみを選択した場合、GOAROUNDの機能は完全にディスエンゲージされないことが記載されていない"),
                     ("報告書 p103", "FMA上の表示の変更と実質的機能の変更の対比"))),
    who3=dict(items=(("機長が", "自分で"), ("副操縦士が", "機長の指示で"), ("副操縦士が", "断りなく")),
              quote=(("報告書 p89", "機長が自らエンゲージしたか、副操縦士が機長の指示によりエンゲージしたか、あるいは、副操縦士が機長に断りなく"),)),
    ths=dict(pts=((5, -5.3, "報告書 p54", "THS機首上げ-5.3°"), (18, -5.3, "報告書 p55", "THSは-5.3°からなお機首上げ方向に動き始めた"),
                  (25, -6.7, "付図5 p1", ""), (31, -9.5, "付図5 p1", ""), (37, -12.3, "報告書 p56", "THSは機首上げ一杯の-12.3°に達しており"),
                  (49, -12.3, "報告書 p56", "APはディスエンゲージされたがTHSは-12.3°のままであり"), (57, -12.3, "報告書 p56", "THS-12.3°及びエレベータ角9.9°"),
                  (71, -12.3, "報告書 p49", "THSは15分11秒の-12.3°から")),
             line=dict(none=0, t25=25, t49=49), desc=26, off=49, limit=-12.3,
             quote=(("報告書 p55", "同26秒ごろから降下に移っている"),)),
    warn=dict(inputs=("手の操縦", "自動操縦"), cols=("company", "ship"), opts=("警報音を残す", "別の仕組みで知らせる"),
              quote=(("報告書 p84", "手動、自動操縦共THSが作動した時にはウーラー音が鳴るように設計"),
                     ("報告書 p84", "自動操縦時においては当該ウーラー音は鳴らないように設計変更"),
                     ("報告書 p85", "操縦輪を操作し続けるとアウト・オブ・トリムに至る特性"),
                     ("報告書 p85", "THSモーション・ウォーニング(ウーラー音)を残すか、または、削除するのであればTHSモーション・ウォーニングに替わる"))),
    eu=dict(tls=(43.6047, 1.4442), gb=(49.8, 59.0, -6.5, 2.0), req=("自動着陸の最後の場面", "警報を減らす"),
            quote=(("報告書 p84", "英国CAAは同型式機の評価時に"),
                   ("報告書 p84", "オートランド・フレア中のTHSモーション・ウォーニング(ウーラー音)は減少されるべきであるとエアバス社に対して要求"))),
    cards3=dict(n=3, quote=(("報告書 p57", "繰り返し操縦輪を押すように指示している。このことについては、次の可能性が考えられる。1"),)),
    assist=dict(name="スーパーバイザリー・オーバーライド",
                quote=(("報告書 p57", "操縦士が操縦輪に力を加えて、APをアシストすることができるスーパーバイザリー・オーバーライドと呼ばれる機能"),
                       ("報告書 p90", "スーパーバイザリー・オーバーライド機能との混同"))),
    afloor=dict(steps=("迎え角が大きすぎる", "推力を自動で最大に", "失速を防ぐ"),
                quote=(("報告書 p83", "アルファ・フロア機能が作動し出力が増加した"), ("報告書 p83", "本来失速を防止しフライト・エンベロープを保護するための安全装置"))),
    # 🆕 ⑤b-6：分度器を前例の値にも（set＝c719・hel・mos）＝(角度, 速さ〈時速約○キロ・○ノット〉)
    pitch=dict(sets=dict(c719=(52.6, None), hel=(35.5, ("170", "94")), mos=(88.0, ("56", "30"))),
               caps=dict(c719="機首の角度（最大）", hel="機首の角度（やり直しの上昇）", mos="機首の角度（ほとんど真上）"),
               quote=(("報告書 p49", "ピッチ角は、最大の52.6°となっている"), ("報告書 p184", "機体姿勢は機首上げ35.5。に増加し、速度は94ktに減じた"),
                      ("報告書 p185", "機首上げは88。に増加し、速度は30ktに低下し"))),
    # 🆕 ⑤b-6（第8〜9章）
    bars=dict(sets=dict(fire=(("国際的な基準（望ましい）", 9000.0, "LINE"), ("基地の化学消防車5台", 7500.0, "AMBER")),
                        trim=(("ふだんのやり直し", (1.0, 2.0), "LINE"), ("ヘルシンキの出来事", 8.0, "ship")),
                        # 🆕 ⑤b-6b：fcc＝ca09（p77）・force＝cb19（判決 p2088〜2090）
                        fcc=(("1991年", 4.0, "LINE"), ("1992年", 8.0, "LINE"), ("通報のあと事故まで", 0.0, "ALERT")),
                        force=(("ふだんの上り下り", (4.0, 5.0), "LINE"), ("この夜", 20.0, "company"))),
              labs=dict(fire=("9,000", "7,500"), trim=("−1〜−2度", "−8度"), fcc=("4台", "8台", "0台"), force=("4〜5kg", "20kg以上")),
              chips=dict(force=(("自分で入れた", "city"), ("画面の表示", "city"), ("機長の指摘 3回", "city"))),
              msg=dict(fcc="改修の機会が来ない", force="約30秒 押し続けた"),
              quote=(("報告書 p86", "ICAO水準では、放射率は9,000l/minとされている"), ("報告書 p86", "化学消防車5台の放射率は7,500l/min"),
                     ("報告書 p184", "すでに一8。機首上げ側に作動しており"), ("報告書 p184", "通常のGO-AROUNDでは一1。ー2。機首上げ"),
                     ("報告書 p184", "オートトリムを働かせTHSをエレベータの動きと相反する機首上げ側に作動させた"),
                     ("報告書 p77", "1991年は4台、1992年は8台"),
                     ("報告書 p77", "1993年6月24日から1994年4月26日の名古屋空港での事故発生までの間に、中華航空公司において、故障により機体から取り下ろされ、"
                                   "修理のためSEXTANTシンガポールに送られたFCCはなかった"),
                     ("報告書 p77", "故障して取り下ろされたFCCの修理を実施する際,同時にSBによる改修を行うものとして計画された"),
                     ("判決 p2088", "4から5kgの力を超えることがない"), ("判決 p2088", "最低限20kgの力が必要"),
                     ("判決 p2088", "通常の4倍から5倍の力である20kgもの力を,約30秒間継続"),
                     ("判決 p2089", "自らオートパイロットを接続したのであるし"),
                     ("判決 p2089", "フライトモード表示器上にはゴーアラウンドモードでオートパイロットが接続されていることが表示されていた"),
                     ("判決 p2089", "3度にわたって機長からゴーアラウンドモードであることを指摘された"),
                     ("判決 p2090", "約30秒間にもわたって20kg以上の非常に強い力を操縦輪に加え続けても押し下げられない"))),
    flow=dict(sets=dict(gov=dict(boxes=(("rep", "航空事故調査委員会", "（報告書）", "state"), ("min", "運輸大臣", "", "LINE"),
                                        ("what", "全国の飛行場", "消火と救難を強める", "AMBER")),
                                 arrows=(("rep", "min", "建議"), ("min", "what", "")), marks=()),
                        edu=dict(boxes=(("cal", "中華航空", "", "LINE"), ("crew", "事故機と同じ型の乗員", "", "LINE"),
                                        ("two", "この機長と副操縦士", "（当時はその型に乗っていない）", "company")),
                                 arrows=(("cal", "crew", "モスクワの出来事の教育"), ("cal", "two", "")),
                                 marks=(("ok", "crew", ""), ("x", "two", "教わっていない"))),
                        # 🆕 ⑤b-6b（ca04・ca07・ca12・cb04・cb10）
                        own=dict(boxes=(("cls", "必須以外の区分", "（推奨・望ましい・任意）", "LINE"), ("cal", "航空会社", "", "LINE"),
                                        ("exp", "運航の経験", "", "LINE"), ("plan", "整備の計画", "", "LINE"),
                                        ("do", "行うかどうか", "", "AMBER"), ("how", "そのやり方", "", "AMBER")),
                                 arrows=(("cls", "cal", ""), ("exp", "cal", ""), ("plan", "cal", ""), ("cal", "do", ""), ("cal", "how", "")),
                                 marks=(("q", "cls", "この改修は"),)),
                        cal=dict(boxes=(("sb", "推奨の改修", "（技術通報）", "airbus"), ("cal", "中華航空", "", "LINE"),
                                        ("judge", "緊急性は無い", "（判断）", "AMBER"), ("plan", "故障して修理に出すとき", "合わせて改修する", "LINE")),
                                 arrows=(("sb", "cal", ""), ("cal", "judge", ""), ("judge", "plan", "")), marks=()),
                        tell=dict(boxes=(("judge", "中華航空の判断", "（緊急性は無い）", "LINE"), ("rec", "「推奨」として出た", "", "airbus"),
                                         ("why", "理由と背景の説明", "（足りなかった）", "airbus")),
                                  arrows=(("hub", "judge", "大きく影響"), ("rec", "hub", ""), ("why", "hub", "")), marks=()),
                        rec=dict(boxes=(("rep", "航空事故調査委員会", "（報告書）", "state"), ("sr", "安全勧告", "こう変えてほしい", "state"),
                                        ("tw", "台湾の当局", "", "LINE"), ("fr", "フランスの当局", "", "LINE")),
                                 arrows=(("rep", "sr", ""), ("sr", "tw", ""), ("sr", "fr", "")), marks=()),
                        cog=dict(boxes=(("see", "見る", "", "LINE"), ("note", "気づく", "", "LINE"), ("judge", "判断する", "", "LINE")),
                                 arrows=(("see", "note", ""), ("note", "judge", "")), marks=())),
              quote=(("報告書 p105", "本事故に鑑み以下のとおり運輸大臣に建議する"), ("報告書 p105", "全国の飛行場における民間航空機に係る今後の消火救難体制"),
                     ("報告書 p74", "モスクワで発生したA310型のインシデント事例については、該当乗務員に対して教育を行った"),
                     ("報告書 p74", "当該機長及び副操縦士は、当時、A300-600R型機に乗務していなかったため、当該教育を受けていなかった"),
                     ("報告書 p76", "Recommended及びその他の場合は、各オペレータの運航経験、運航形態及び整備計画等を加味して適用の可否、実施する場合の方法が決定される"),
                     ("報告書 p76", "緊急性が認められないとの判断により、当該改修はFCCの修理を行う際に合わせて改修することとした"),
                     ("報告書 p92", "当該SBの適用区分がRecommendedであったことから、緊急性が認められないとの判断により"),
                     ("報告書 p80", "当該SBがMandatoryとしてではなく、Recommendedとして発行されたこと"),
                     ("報告書 p80", "当該SBの発行された理由及び技術的背景についての説明が詳細、かつ、明確に述べられていなかったこと等が大きく影響していたものと考えられる"),
                     ("報告書 p101", "本事故に鑑み以下のとおり関係当局に勧告する。1台湾民用航空当局は"),
                     ("報告書 p102", "2仏国耐空性管理当局は"),
                     ("報告書 p104", "人間の認知過程を考慮したAFS"))),
    prec=dict(sets=dict(hel="ヘルシンキの出来事（1989年）", mos="モスクワの出来事（1991年）"),
              why=dict(hel="乗客の乗り心地のため", mos="機体が軽く・上昇が急"),
              quote=(("報告書 p184", "乗客の快適性のためAPによる機首上げを避けようと、機首上げモーメントに抗して手動で操縦輪を押しつづけた"),
                     ("報告書 p184", "オートトリムを働かせTHSをエレベータの動きと相反する機首上げ側に作動させた"),
                     ("報告書 p184", "マニュアルトリムを使用し、副操縦士にこの操作を続けさせた"), ("報告書 p184", "正常な飛行に戻った"),
                     ("報告書 p80", "1991年1月にFCOM1.03.64P3/4及び同2.02.03P1が改訂され"),
                     ("報告書 p184", "機体重量が軽く、上昇率が高かったため"), ("報告書 p184", "手動で操縦輪を押しエレベータを機首下げとした"),
                     ("報告書 p185", "この間乗員はAPはまだ解除されていないものと思っており"))),
    hold=dict(ft=750, m=230, quote=(("報告書 p184", "対地高度750ftで水平飛行をしばらく維持した"),
                                    ("報告書 p184", "この間、機長及び副操縦士はAPはまだ解除されていないものと思っていた"))),
    keep=dict(quote=(("報告書 p185", "THSの作動角度はそのままの状態が残ることとなった"), ("報告書 p184", "APは解除されることとなった"))),
    updown=dict(pts=(("ga", 1275), ("p1", 4327), ("l1", 1487), ("p4", 11755), ("rec", 8715)),
                m=(("p1", "1,320"), ("p4", "3,580"), ("rec", "2,660")),
                quote=(("報告書 p184", "対地高度1,275ftでG0AROUNDモードにした"), ("報告書 p185", "高度は、4,327ftに達した後、失速状態となり、高度1,487ftまで降下"),
                       ("報告書 p185", "4回目の上昇時には高度11,755ftに達した"), ("報告書 p185", "高度8,715ftで異常な飛行から回復することができた"),
                       ("報告書 p185", "4回目の降下時に、乗員によりエンジン出力が減じられたこと"), ("報告書 p185", "THSが機首下げ方向にトリムされた"))),
    doc=dict(modes=("LAND", "GO AROUND"), flow=("操縦輪で逆らう", "釣り合いがずれる", "危険な状態のおそれ"),
             # 🆕 ⑤b-6b：書類の set（ca02・ca03・ca16）＝(欄の名, 値, 役)。cls の区分の順は報告書の順（Mandatory が最も優先）
             sets=dict(sb=dict(head=("SERVICE BULLETIN", "A300-22-6021"),
                               rows=(("出す側", "AIRBUS INDUSTRIE（メーカー）", "airbus"), ("受ける側", "航空会社", "LINE"),
                                     ("高さ", "対地 400 ft 以上（約120メートル）", "AMBER"), ("操縦輪", "15 kg 以上の力 → AP が切れる", "AMBER"))),
                       cls=dict(head=("SERVICE BULLETIN", ""),
                                rows=(("1", "Mandatory（必須）", "AMBER"), ("2", "Recommended（推奨）", "LINE"),
                                      ("3", "Desirable（望ましい）", "LINE"), ("4", "Optional（任意）", "LINE")), top="最も優先"),
                       ad=dict(head=("耐空性改善命令", ""),
                               rows=(("出す側", "国の当局", "LINE"), ("受ける側", "航空会社", "LINE"), ("目的", "安全に飛べる状態を保つ", "LINE"),
                                     ("中身", "改修など", "LINE")), stamp="義務")),
             quote=(("報告書 p80", "LAND及びGOAROUNDモード時にピッチ方向にAPをオーバーライドするとアウト・オブ・トリムとなり危険な状態に至る"),
                    ("報告書 p80", "1991年1月にFCOM1.03.64P3/4及び同2.02.03P1が改訂され"),
                    ("報告書 p76", "製造者から各オペレータに対して、航空機及び装備品の点検及び改修に関して発行される技術通報としてServiceBulletin"),
                    ("報告書 p76", "GOAROUNDモードにおいて、対地高度400ft以上で操縦輪にピッチ方向へ15kg以上の力を加えた場合、APが解除されるAFSの改修"),
                    ("報告書 p76", "エアバス社から1993年6月24日に、Recommendedとして発行されたSBA300-22-6021"),
                    ("報告書 p76", "大別してMandatory、Recommended、Desirable、Optional、の4つに分けられ"),
                    ("報告書 p76", "Mandatoryの場合、最優先にて実施されることとなる"),
                    ("報告書 p93", "(1)のSBの実施に係る耐空性改善命令を発行する処置を速やかに講じなかった"),
                    ("報告書 p80", "SBを速やかに導入できるよう耐空性改善命令としての処置を講ずる必要があった"))),
    cards2=dict(sets=dict(fcom2=dict(cards=(("勧める", "異常な自動操縦から守る", "OK"), ("禁じる", "正常なときに逆らう", "ALERT")),
                                     foot=("報告書", "混同するおそれ", "state")),
                          # 🆕 ⑤b-6b（ca05・cb20・cb25）
                          rec2=dict(cards=(("推奨", "Recommended", "airbus"), ("2台", "1機あたりの飛行制御コンピュータ", "LINE")), foot=None),
                          train2=dict(cards=(("判決", "受けていた", "city"), ("報告書", "教官の記録に実施の印", "state")),
                                      foot=("報告書", "方法は明らかにできない", "state"),
                                      top=("訓練の項目", "GO-AROUND DEMONSTRATE AP MISUSE IN GO-AROUND")),
                          q2=dict(cards=(("報告書の問い", "同じ事故を防ぐ", "state"), ("判決の問い", ("賠償の上限を外せるか", "（国際条約の決まり）"), "city")),
                                  foot=None)),
                quote=(("報告書 p81", "APオーバーライドの目的は、APの異常な作動から操縦士を保護するものである"),
                       ("報告書 p81", "CAUTIONに記述されている内容は、APが正常に機能している場合のオーバーライドを禁止するものである"),
                       ("報告書 p81", "推奨と禁止の相矛盾する内容を混同して理解する可能性がある"),
                       ("報告書 p76", "このSBの実施には、一機当たり2台のFCCを改修する必要があった"),
                       ("判決 p2090", "GO-AROUNDDEMONSTRATEAPMISUSEINGO-AROUND"),
                       ("判決 p2090", "という項目のシミュレーター訓練を受けていた"),
                       ("報告書 p75", "「GO-AROUNDDEMONSTRATEAPMISUSEINGO-AROUND」の項目が設けられ、実施欄に+マークが記入されていた"),
                       ("報告書 p75", "事前に手渡されたチェック・シートは同項目が追加されていない改訂前のものであった"),
                       ("報告書 p75", "どのような方法で本項目の訓練を行ったかについては明らかにできなかった"),
                       ("判決 p2081", "責任制限規定の適用排除を定める改正ワルソー条約25条"),
                       ("報告書 p103", "再発防止のための技術改修の開発"))),
    # 🆕 ⑤b-6b：asia（ca08）＝シンガポールは一般の座標（報告書に座標は無い）・明るくする島は台湾
    asia=dict(sg=(1.29, 103.85), tw=(21.8, 25.4, 119.8, 122.2),
              quote=(("報告書 p77", "中華航空公司の整備施設ではFCCの改修が実施できないため、この改修作業が可能なSEXTANTシンガポールに送らねばならず"),
                     ("報告書 p77", "運航を維持するための予備品を確保しつつ"))),
    # 🆕 ⑤b-6b：cmp（cb16・cb24・cb26）＝並べ図の行（番号・問い・報告書の欄・判決の欄）・欄の色（報告書＝青 state・判決＝紫 city）・欄の下の札
    cmp=dict(rows=(("1", "入れたのは誰か", "特定できない", "副操縦士と認める"), ("2", "気づいていたか", "認識することなく", "認識していた"),
                   ("3", "警報", "知らせる警報が無い", "操縦輪の重さが警告"), ("4", "手引き書", "分かりにくい（要因）", "分かりにくいとはいえない"),
                   ("5", "設計", "ずれの要因の1つ", "直ちに欠陥とはいえない")),
             cols=(("報告書", "state"), ("判決", "city")), foot=("同じ事故を防ぐ", "責任を決める"),
             quote=(("報告書 p89", "副操縦士が機長に断りなく、又は通知することなくエンゲージしたか、いずれかの可能性がある"),
                    ("判決 p2088", "14分18秒にオートパイロットを接続した者は,副操縦士であると認めるのが相当である"),
                    ("報告書 p95", "当該状況を認識することなく更に進入を継続し"),
                    ("判決 p2090", "アウトオブトリムの状態を認識していたというべきであり"),
                    ("報告書 p95", "直接的かつ積極的に操縦士に知らせる警報・認識機能がなかったこと"),
                    ("判決 p2098", "操縦輪の重さがアウトオブトリムの状態を操縦士に知らせる最も直接的で有効な警告である"),
                    ("報告書 p96", "AFS(AutomaticFlightSystem)に関する記述が分かりにくいことが寄与"),
                    ("判決 p2091", "運航マニュアルの記載が分かりにくいとはいえない"),
                    ("報告書 p78", "このような設計になっていたことが、本事故における異常なアウト・オブ・トリムの要因の1つとなった"),
                    ("判決 p2094", "これをもって直ちに欠陥であるということはできない"),
                    ("報告書 p103", "再発防止のための技術改修の開発"),
                    ("判決 p2081", "損害賠償責任を負うこととなる"))),
    pbars=dict(rows=(("着陸の進入", 4.0), ("画面の表示が消える", 25.0), ("この夜の最大", 52.6)), twice=2,
               quote=(("報告書 p54", "ピッチ角約4°"), ("報告書 p49", "最大の52.6°"))),
    clock={"11:14", "20:14", "20:15", "20:00"},
)
NUM_M17 = re.compile(r"[0-9０-９]{1,2}[:：][0-9０-９]{2}|[0-9０-９][0-9０-９,.．]*")
VIEW_HEADS17 = ("横から", "上から", "斜めから", "正面")
_M17_PAGES = {}


def _m17_page(rec):
    """「報告書 pN」「判決 pN」の頁の文字（NFKC・空白なし）。原文が手元に無い（Actions）・頁の無い資料は None。
    🆕 ⑤b-6b：判決も同じ通し頁（ep17_pages.txt の p2001〜p2152＝2000＋PDF の頁＝cuts/ss.REC_DOCS の「判決」）"""
    import unicodedata
    from pathlib import Path
    m_ = re.fullmatch(r"(?:報告書|判決) p(-?\d+)", rec)
    if not m_:
        return None
    if not _M17_PAGES:
        t = Path(__file__).resolve().parent.parent / "ref" / "ep17" / "src" / "ep17_pages.txt"
        if not t.exists():
            _M17_PAGES[None] = True
            return None
        for mm in re.finditer(r"^=== p(-?\d+) ===\n(.*?)(?=^=== p|\Z)", t.read_text(encoding="utf-8"), re.M | re.S):
            _M17_PAGES[int(mm.group(1))] = re.sub(r"\s+", "", unicodedata.normalize("NFKC", mm.group(2)))
    return _M17_PAGES.get(int(m_.group(1)))


def _m17_q(q):
    import unicodedata
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", q))


def view_dir_check17(plan_text, lab):
    """PLAN の「見る向き：」の頭の語と、図の左上の札の頭の語が同じか（17本目は「正面」も）。"""
    m_ = re.search(r"見る向き：(横から|上から|斜めから|正面)", plan_text or "")
    if not m_:
        return ""
    return "" if str(lab).startswith(m_.group(1)) else f"左上の札「{lab}」が PLAN の見る向き「{m_.group(1)}」で始まらない（見る向きの合図）"


def judge_m17(f):
    """17本目 図解：①形・表・色（f.mech["geo"]）を記録（REC_M17）で ②全部の字の数を rel で ③句を原文の頁で。"""
    import jiko_style as J
    bad, n = [], 0
    m = f.mech
    g, view = m["geo"], m["view"]
    seq = [m["start"]] + list(m["states"])
    R = REC_M17
    if not R:
        return ["記録の表 REC_M17 が空（その回の値を入れるまで、m17 のカットは止まる）"], 1

    def need(cond, msg):
        nonlocal n
        n += 1
        if not cond:
            bad.append(msg)

    def col(name):
        return (J.ROLE.get(name) or getattr(J, name)).lower()
    Rv = R.get(view) or {}
    if view == "factors":
        it = Rv["items"]
        need(tuple((t, w) for t, w in g["factors"]) == tuple((t, w) for t, w, _p, _q in it), f"② 要因の札 {g['factors']} が記録（p95〜96 の12の要因の順と言葉）と違う")
        need(len(g["factors"]) == 12, f"② 要因の数 {len(g['factors'])}（記録 12）")
        need({k: (t, col(r)) for k, (t, r) in g["who"].items()} == {k: (t, col(r)) for k, (t, r) in Rv["who"].items()},
             "② 要因の役（だれの要因か）の名か色が記録と違う")
        xy = g["xy"]
        need(all((xy[i][1], xy[i][0]) < (xy[i + 1][1], xy[i + 1][0]) for i in range(11)), "② 札の並びが番号の順（左から右・上から下）でない")
        need({k: tuple(v) for k, v in g["mk"].items()} == {k: tuple(v) for k, v in Rv["mk"].items()}, f"② 印の要因 {g['mk']} が記録（機体の作りと手引き書＝1・5・6／乗員＝7・9・10）と違う")
        for t, _w, p, q in it:
            src_ = _m17_page(p)
            if src_ is not None:
                need(_m17_q(q) in src_, f"② 要因「{t}」の原文の句が {p} に無い")
        for p, q in Rv["mk_quote"]:
            src_ = _m17_page(p)
            if src_ is not None:
                need(_m17_q(q) in src_, f"② 印の句が {p} に無い")
    if view == "clock2":
        import datetime as dt
        need((g["utc"], g["jst"], g["add"]) == (Rv["utc"], Rv["jst"], Rv["add"]), f"② 時計の時刻 {g['utc']}→{g['jst']}（＋{g['add']}）が記録（11:14:05＋9時間＝20:14:05）と違う")
        u = dt.datetime.strptime(g["utc"], "%H:%M:%S")
        need((u + dt.timedelta(hours=Rv["add"])).strftime("%H:%M:%S") == g["jst"], "② 時計：日本の時刻が世界共通の時刻の＋9時間でない")
        for t, (ha, ma, sa) in zip((g["utc"], g["jst"]), g["angles"]):
            h, mi, s = (int(x) for x in t.split(":"))
            need(abs(ha - ((h % 12) * 30 + mi * 0.5 + s / 120)) < 1e-6 and abs(ma - (mi * 6 + s * 0.1)) < 1e-6 and abs(sa - s * 6) < 1e-6,
                 f"② 時計 {t} の針の角度が時刻と合わない")
        need(tuple(g["units"]) == Rv["units"], "② 単位の札が記録（フィート→メートル・ノット→時速）と違う")
    if view == "seats":
        need(tuple(g["names"]) == Rv["names"] and g["left_x"] < g["right_x"], "② 席の名（左＝機長・右＝副操縦士）が記録と違う")
        need(g["age"] == Rv["age"] and tuple(g["af"]) == Rv["af"] and round(g["years"]) == Rv["years"], f"② 機長の年齢と空軍の年（{g['age']}歳・約{round(g['years'])}年）が記録と違う")
        need(tuple(g["roles"]) == Rv["roles"] and g["order"] == Rv["order"], "② 役の札か指示の時刻が記録（p42・p57）と違う")
        need(g["arrow"][0] < g["arrow"][1], "② 指示の矢印が左の席（機長）から右の席（副操縦士）へ向いていない")
    if view == "hours":
        need(tuple(t for t, _v in g["rows"]) == tuple(t for t, _v in Rv["rows"])
             and all(abs(a - b) < 1e-6 for (_t, a), (_u, b) in zip(g["rows"], Rv["rows"])), f"② 飛行時間 {g['rows']} が記録（p17・p38）と違う")
        need(all(abs(e - (g["x0"] + v * g["unit"])) < 0.5 for e, (_t, v) in zip(g["ends"], Rv["rows"])), "② 飛行時間の棒の長さが記録の時間と合わない（同じ縮尺）")
        need(all(abs(x - (g["x0"] + v * g["unit"])) < 0.5 for v, x in g["ticks"]), "② 目盛りの位置が値と合わない")
        need(tuple(g["career"]) == Rv["career"], "② 経歴の札が記録（p38）と違う")
    if view == "train":
        need(tuple(g["steps"]) == Rv["steps"] and g["hours"] == Rv["hours"], "② 訓練の順か時間が記録（p38）と違う")
        need(all(a[1] < b[0] for a, b in zip(g["segs"], g["segs"][1:])), "② 訓練の帯が左から右への順になっていない")
    if view == "area":
        need(g["th_n"] == Rv["ratio"] * g["el_n"], f"② 面積のマス目（昇降舵 {g['el_n']}・水平安定板 {g['th_n']}）が記録（約3倍＝p55）と違う")
        need(g["th_el"] == g["el_n"] and str(Rv["ratio"]) == str(g["ratio"]), "② 水平安定板の中の昇降舵のマスが昇降舵だけのマスと違うか、札の倍が記録と違う")
    if view == "afs":
        need(tuple(g["afs"]) == Rv["items"], "② 3つの仕組みの札が記録と違う")
    if view == "band":
        need((g["ft"], g["m"], tuple(g["out"])) == (Rv["ft"], Rv["m"], Rv["out"]), "② 対象外の高さかモードが記録（p78＝対地400ft以下のランド・ゴー・アラウンド）と違う")
        need(abs(int(Rv["ft"]) * 0.3048 - int(g["m"])) < 5, "② メートルの札がフィートの値の換算と合わない")
        need(g["y_low"] < g["g"] and g["land_x0"] < g["td"][0], "② 約120m の線が地面より上にないか、ランドの区間が接地の手前から始まらない")
        need(g["ga"][0][1] > g["ga"][-1][1], "② ゴー・アラウンドの線が上っていない")
    if view == "modes":
        need(g["start"] == Rv["start"] and {k: (t, tuple(r)) for k, (t, r) in g["rows"].items()} == Rv["rows"], f"② 抜け方の札 {g['rows']} が記録（p54・p81）と違う")
        need({k: tuple(v) for k, v in g["cols"].items()} == Rv["cols"], "② 抜け方の結果の色（抜ける＝緑・消える＝黄・残る／抜けられない＝赤）が記録と違う")
    if view == "fcom":
        need((tuple(g["fma"]), tuple(g["rows"]), g["miss"], tuple(g["rec"])) == (Rv["fma"], Rv["rows"], Rv["miss"], Rv["rec"]),
             "② 表示・手引き書の欄・書かれていない所・勧告の札が記録（p81〜82・p103）と違う")
    if view == "who3":
        need(tuple(g["who3"]) == Rv["items"], "② 3つの可能性の札が記録（p89）と違う")
    if view == "ths":
        need(tuple((t, a) for t, a in g["pts"]) == tuple((t, a) for t, a, _p, _q in Rv["pts"]), f"② 角度の点 {g['pts']} が記録（付図5 の表と本文）と違う")
        need(all(abs(x - (g["x0"] + t * g["sec"])) < 0.5 and abs(y - (g["y0"] + a * g["k"])) < 0.5 for (x, y), (t, a, _p, _q) in zip(g["px"], Rv["pts"])),
             "② 角度の点の画素が値（時刻・角度）と合わない")
        need(min(a for _t, a in g["pts"]) == Rv["limit"], "② 角度の点が機首上げ一杯（−12.3度＝p56）を超えている")
        need(set(g["upto"]) <= set(Rv["line"].values()) and g["desc"] == Rv["desc"] and g["off"] == Rv["off"],
             "② 線の終わり・下り始め・自動操縦を切った時刻が記録（14:25・14:49・14:26・14:49）と違う")
        for _t, _a, p, q in Rv["pts"]:
            src_ = _m17_page(p)
            if q and src_ is not None:
                need(_m17_q(q) in src_, f"② 角度の点の句が {p} に無い")
    if view == "warn":
        need(tuple(g["inputs"]) == Rv["inputs"] and tuple(col(c) for c in g["in_cols"]) == tuple(col(c) for c in Rv["cols"]),
             "② 警報音の入り口（手の操縦＝橙・自動操縦＝水色）が記録と違う")
        need(tuple(g["opts"]) == Rv["opts"], "② 報告書の見方の2つの札が記録（p85）と違う")
    if view == "eu":
        la, lo = g["pts"]["tls"]
        need(abs(la - Rv["tls"][0]) < 0.05 and abs(lo - Rv["tls"][1]) < 0.05, f"② トゥールーズの点（{la}, {lo}）が一般の座標と違う")
        a, b, c, d = Rv["gb"]
        gc = g["gb_c"]
        need(gc is not None and a <= gc[0] <= b and c <= gc[1] <= d and g["gb_n"] > 50, "② 明るくした島がグレートブリテン島でない")
        (gx, gy), (tx, ty) = g["px"]["gb"], g["px"]["tls"]
        need(ty > gy and tx > gx, "② トゥールーズがイギリスの南東に描かれていない（向き）")
        need(tuple(g["req"]) == Rv["req"], "② 要求の札が記録（p84）と違う")
        need("一般の座標" in m.get("note", ""), "② 注に「一般の座標」が無い（トゥールーズは報告書の値ではない）")
    if view == "cards3":
        need(g["n"] == Rv["n"], f"② 可能性の札の数 {g['n']}（記録 3）")
    if view == "assist":
        (la_, lh_), (ra_, rh_) = g["vec"]["l"], g["vec"]["r"]
        need(la_[0] * lh_[0] + la_[1] * lh_[1] > 0, "② 電波の道を捕まえるときの押す向きが自動操縦と同じでない（手伝う）")
        need(ra_[0] * rh_[0] + ra_[1] * rh_[1] < 0 and ra_[1] < 0, "② この夜の押す向きが自動操縦（機首上げ）と逆でない")
        need(g["name"] == Rv["name"], "② 機能の名が記録（p57）と違う")
    if view == "afloor":
        need(tuple(g["steps"]) == Rv["steps"], "② アルファ・フロアの流れの札が記録（p83）と違う")
    if view == "pitch":
        deg, spd = Rv["sets"][g["set"]]
        need(abs(g["deg"] - deg) < 1e-9, f"② 機首の角度 {g['deg']}（記録 {deg}度）")
        last = g["rows"][-1]
        need(abs(last["rot"] + deg) < 1e-9 and abs(last["plane"] - last["rot"]) < 1e-9, "② 針と機の形が記録の角度まで回っていない")
        need(all(r["rot"] <= 0 for r in g["rows"]), "② 針が下（機首下げ）へ回っている")
        need(g["cap"] == Rv["caps"][g["set"]], f"② 角度の札「{g['cap']}」が記録と違う")
        need(tuple(g["spd"] or ()) == tuple(spd or ()), f"② 速さ {g['spd']} が記録 {spd} と違う")
        if spd:
            need(abs(int(spd[1]) * 1.852 - int(spd[0])) <= 5, f"② 時速 {spd[0]} キロが {spd[1]} ノットの換算と合わない")
    if view == "bars":
        rows = Rv["sets"][g["set"]]
        need(tuple((t, v) for t, v, _r in g["rows"]) == tuple((t, v) for t, v, _r in rows), f"② 棒 {g['rows']} が記録と違う")
        need(tuple(col(r) for _t, _v, r in g["rows"]) == tuple(col(r) for _t, _v, r in rows), "② 棒の色（役）が記録と違う")
        need(tuple(g["labs"]) == Rv["labs"][g["set"]], f"② 棒の値の札 {g['labs']} が記録と違う")
        for e, (_t, v, _r) in zip(g["ends"], rows):
            vv = v if isinstance(v, tuple) else (v,)
            ee = e if isinstance(e, tuple) else (e,)
            need(all(abs(a - (g["x0"] + b * g["unit"])) < 0.5 for a, b in zip(ee, vv)), "② 棒の長さが値と合わない（同じ縮尺）")
        need(all(abs(x - (g["x0"] + v * g["unit"])) < 0.5 for v, x in g["ticks"]), "② 目盛りの位置が値と合わない")
        # 🆕 ⑤b-6b：理由の札（判決の色）・下の札
        ch = Rv.get("chips", {}).get(g["set"], ())
        need(tuple(t for t, _r in g["chips"]) == tuple(t for t, _r in ch)
             and tuple(col(r) for _t, r in g["chips"]) == tuple(col(r) for _t, r in ch), f"② 棒の理由の札 {g['chips']} が記録と違う")
        need(g["msg"] == Rv.get("msg", {}).get(g["set"]), f"② 棒の下の札「{g['msg']}」が記録と違う")
        need(all(not g["on"][f_] for f_ in ("b0", "b1", "b2")[len(rows):]), "② 記録に無い棒（行）を出している")
    if view == "flow":
        S = Rv["sets"][g["set"]]
        need(tuple(g["boxes"]) == S["boxes"], f"② 流れの箱 {g['boxes']} が記録と違う")
        need(tuple(g["arrows"]) == S["arrows"] and tuple(g["marks"]) == S["marks"], "② 流れの矢印か印（✓・×・？）が記録と違う")
        need(all(col(r) for _n, _t, _t2, r in g["boxes"]), "② 箱の役の色が引けない")
        need(all((dx, dy) != (0, 0) for _a, _b, dx, dy in g["vec"]), "② 矢印の元と先が同じ点")
    if view == "prec":
        need(g["name"] == Rv["sets"][g["set"]] and g["why"] == Rv["why"][g["set"]], f"② 前例の名か理由の札（{g['name']}・{g['why']}）が記録と違う")
        need(not (g["on"]["fcom"] and g["set"] != "hel"), "② 注意書きの札（1991年1月）はヘルシンキの出来事のあと（p80）＝モスクワの絵に出さない")
    if view == "hold":
        need((g["ft"], g["m"]) == (Rv["ft"], Rv["m"]) and abs(Rv["ft"] * 0.3048 - Rv["m"]) < 5, f"② 高さ {g['m']}m（{g['ft']}ft）が記録と違う")
        need(g["y"] < g["g"], "② 水平飛行の線が地面より上にない")
    if view == "keep":
        need(g["xoff"] < g["x1"] and g["y_flat"] < g["y0"], "② 切れたあとの角度の線が切れた所から先に無いか、上がっていない")
    if view == "updown":
        need(tuple(g["pts"]) == Rv["pts"], f"② 高さの点 {g['pts']} が記録（p184〜185）と違う")
        need(all(abs(y - (g["g"] - f * 0.3048 * g["k"])) < 0.5 for (x, y), (_n, f) in zip(g["px"], Rv["pts"])), "② 高さの点の画素が値に比例していない")
        need(all(a[0] < b[0] for a, b in zip(g["px"], g["px"][1:])), "② 点が順番（左から右）に並んでいない")
        fts = dict(Rv["pts"])
        for nm_, m_ in Rv["m"]:
            need(abs(fts[nm_] * 0.3048 - float(m_.replace(",", ""))) <= 10, f"② 札の {m_}メートルが {fts[nm_]}フィートの換算と合わない")
            fld = dict(p1="first", p4="fourth", rec="rec")[nm_]
            if any(s.get(fld) == "on" for s in seq):
                need(any(m_ in t for t in m["texts_all"]), f"② 札に {m_}メートルが描かれていない")
    if view == "doc":
        if g["set"] == "fcom":
            need(tuple(g["modes"]) == Rv["modes"] and tuple(g["flow"]) == Rv["flow"], "② 注意書きの語か流れが記録（p80）と違う")
        else:
            D = Rv["sets"][g["set"]]
            need(tuple(g["head"] or ()) == D["head"], f"② 書類の表題 {g['head']} が記録と違う")
            need(tuple(g["rows"]) == D["rows"], f"② 書類の欄 {g['rows']} が記録と違う")
            need(len(g["rows"]) <= 4, "② 書類の欄が4つを超える（§5b-114）")
            need(g["top"] == D.get("top") and g["stamp"] == D.get("stamp"), "② 書類の印（最も優先・義務）が記録と違う")
    if view == "cards2":
        S = Rv["sets"][g["set"]]
        need(tuple(g["cards"]) == S["cards"] and (tuple(g["foot"]) if g["foot"] else None) == S["foot"], f"② 2つの札 {g['cards']} が記録と違う")
        need((tuple(g["top"]) if g["top"] else None) == S.get("top"), f"② 上の札 {g['top']} が記録と違う")
        need(all(col(r) for _h, _t, r in g["cards"]), "② 札の役の色が引けない")
    if view == "asia":
        la, lo = g["pts"]["sg"]
        need(abs(la - Rv["sg"][0]) < 0.05 and abs(lo - Rv["sg"][1]) < 0.05, f"② シンガポールの点（{la}, {lo}）が一般の座標と違う")
        a, b, c, d = Rv["tw"]
        tc = g["tw_c"]
        need(tc is not None and a <= tc[0] <= b and c <= tc[1] <= d and g["tw_n"] > 10, "② 明るくした島が台湾でない")
        (tx, ty), (sx, sy) = g["px"]["tw"], g["px"]["sg"]
        need(sy > ty and sx < tx, "② シンガポールが台湾の南西に描かれていない（向き）")
        need("一般の座標" in m.get("note", ""), "② 注に「一般の座標」が無い（シンガポールは報告書の値ではない）")
    if view == "cmp":
        need(tuple(g["rows"]) == Rv["rows"], f"② 並べ図の行 {g['rows']} が記録と違う")
        need(tuple(t for t, _r in g["cols"]) == tuple(t for t, _r in Rv["cols"])
             and tuple(col(r) for _t, r in g["cols"]) == tuple(col(r) for _t, r in Rv["cols"]), "② 並べ図の欄の名か色（報告書＝青・判決＝紫）が記録と違う")
        need(g["xp"] < g["xj"], "② 報告書の欄が判決の欄の左にない")
        need(tuple(g["foot"]) == Rv["foot"], "② 欄の下の札が記録と違う")
        need(all(a < b for a, b in zip(g["ys"], g["ys"][1:])), "② 行が語りの順（上から下）に並んでいない")
    if view == "pbars":
        need(tuple(t for t, _v in g["rows"]) == tuple(t for t, _v in Rv["rows"])
             and all(abs(a - b) < 1e-9 for (_t, a), (_u, b) in zip(g["rows"], Rv["rows"])), f"② 角度の棒 {g['rows']} が記録（約4・25・52.6度）と違う")
        need(all(abs(e - (g["x0"] + v * g["unit"])) < 0.5 for e, (_t, v) in zip(g["ends"], Rv["rows"])), "② 角度の棒の長さが値と合わない（同じ縮尺）")
        need(g["twice"] == Rv["twice"] and abs(g["twice_x"] - (g["x0"] + Rv["rows"][1][1] * Rv["twice"] * g["unit"])) < 0.5
             and Rv["rows"][2][1] > Rv["rows"][1][1] * Rv["twice"], "② 「25度の2倍」の線が値と合わないか、最大が2倍を超えていない")
    for p, q in Rv.get("quote", ()):
        src_ = _m17_page(p)
        if src_ is not None:
            need(_m17_q(q) in src_, f"② 句「{q[:16]}…」が {p} に無い")
    said = [r.get("t", "") for r in m["rel"]]
    for t in list(m["texts_all"]) + list(m["tags"]):
        for mm in NUM_M17.finditer(t):
            tok = mm.group(0)
            need(any(tok in s for s in said), f"③ 画面の字「{t}」の数「{tok}」が rel（記録の値の宣言）に無い")
            full = tok.replace("：", ":")
            if ":" in full:
                need(full in R["clock"], f"③ 画面の字「{t}」の時刻「{tok}」が記録の時刻（{sorted(R['clock'])}）に無い")
    for r in m["rel"]:
        need(bool(r.get("src")), f"③ rel「{r.get('t')}」に出どころ（src）が無い")
    return bad, n


def _selftest_m17(ok):
    """🆕 17本目 ⑤b-5：本番の SPEC の m17 が全部通り、描く側の定数を壊すと**狙った理由で**鳴るか（陽性対照）。"""
    import mech17 as M
    import cuts
    good = {c: s["fig"][1] for c, s in cuts.SPEC.items() if s.get("fig") and s["fig"][0] == "m17"}
    if not good:
        print("  ⚠️ 17本目 m17 のカットが0件（selftest の陽性対照を飛ばした）")
        return ok
    for cid, kw in sorted(good.items()):
        bad, _ = judge("m17", kw)
        g_ = not bad
        ok &= g_
        if not g_:
            print(f"  🔴 NG 17本目 m17 の本番 {cid} が落ちた: {bad[0]}")
    by_view = {}
    for cid, kw in sorted(good.items()):
        by_view.setdefault(kw["view"], kw)

    def facs():
        x = list(M.FACTORS)
        x[2] = ("重い操縦輪を引き続けた", "crew")
        return tuple(x)
    cases = (("要因の言葉を替える", "factors", "FACTORS", facs(), "② 要因の札"),
             ("時計の差を8時間に", "clock2", "CK2_ADD", 8, "② 時計の時刻"),
             ("この型の時間を替える", "hours", "HR_V", (("この型（A300-600R）", 1530.0, "company"), M.HR_V[1]), "② 飛行時間"),
             ("角度の点を替える", "ths", "TH_PTS", ((5, -5.3), (18, -4.0)) + tuple(M.TH_PTS[2:]), "② 角度の点"),
             ("機首の角度を替える", "pitch", "PT_SET", dict(M.PT_SET, c719=50.0), "② 機首の角度"),
             ("この夜の押す向きを自動操縦と同じに", "assist", "AS_VEC", dict(l=((0, 1), (0, 1)), r=((0, -1), (0, -1))), "② この夜の押す向き"),
             ("トゥールーズを北へ", "eu", "EU_PTS", dict(gb=(53.0, -1.6), tls=(55.6047, 1.4442)), "② トゥールーズ"),
             ("面積のマスを9つに", "area", "AR_TH_N", 9, "② 面積のマス目"),
             ("ランドのボタンの結果を替える", "modes", "MD_ROWS", dict(M.MD_ROWS, c=("ランドのボタンを押す", (("抜ける", "OK"),))), "② 抜け方の札"),
             ("角度の棒の25度を替える", "pbars", "PB_V", (M.PB_V[0], ("画面の表示が消える", 30.0, "AMBER"), M.PB_V[2]), "② 角度の棒"),
             ("警報音の入り口の色を替える", "warn", "WN_IN", (("手の操縦", "ship"), ("自動操縦", "ship")), "② 警報音の入り口"),
             ("席を左右逆に", "seats", "ST_NAME", ("副操縦士", "機長"), "② 席の名"),
             # 🆕 ⑤b-6（第8〜9章）
             ("基地の5台の消火剤を 8,000 に", "bars", "BR_SETS",
              dict(M.BR_SETS, fire=dict(M.BR_SETS["fire"], rows=(M.BR_SETS["fire"]["rows"][0], ("基地の化学消防車5台", 8000.0, "AMBER", "7,500")))), "② 棒"),
             ("4回目の頂点の高さを替える", "updown", "UD_PTS", M.UD_PTS[:3] + (("p4", 1180.0, 12755),) + M.UD_PTS[4:], "② 高さの点"),
             ("建議の向きを逆に（運輸大臣 → 委員会）", "flow", "FL_SETS",
              dict(M.FL_SETS, gov=dict(M.FL_SETS["gov"], arrows=(("min", "rep", "a", "建議"),) + M.FL_SETS["gov"]["arrows"][1:])), "② 流れの矢印か印"),
             ("水平飛行の高さを替える", "hold", "HD_M", 300, "② 高さ"),
             ("押した理由を替える", "prec", "PR_WHY", dict(M.PR_WHY, hel="急いでいたため"), "② 前例の名か理由"),
             ("注意書きのモードを替える", "doc", "DC_MODES", ("LAND", "ALT"), "② 注意書き"),
             ("2つの札を入れ替える", "cards2", "CD2_SETS",
              dict(M.CD2_SETS, fcom2=dict(M.CD2_SETS["fcom2"], cards=tuple(reversed(M.CD2_SETS["fcom2"]["cards"])))), "② 2つの札"),
             # 🆕 ⑤b-6b（第10〜11章）＝新しい set は「その見え方の最初のカット」で回らない（by_view＝カットの名の順）→ カットを名指し（6つ目）
             ("1992年の台数を 6 に", "bars", "BR_SETS",
              dict(M.BR_SETS, fcc=dict(M.BR_SETS["fcc"], rows=(M.BR_SETS["fcc"]["rows"][0], ("1992年", 6.0, "LINE", "8台"), M.BR_SETS["fcc"]["rows"][2]))),
              "② 棒", "ca09"),
             ("理由の札を2つに", "bars", "BR_SETS", dict(M.BR_SETS, force=dict(M.BR_SETS["force"], chips=M.BR_SETS["force"]["chips"][:2])),
              "② 棒の理由の札", "cb19"),
             ("勧告の宛先の矢印を逆に（台湾の当局 → 安全勧告）", "flow", "FL_SETS",
              dict(M.FL_SETS, rec=dict(M.FL_SETS["rec"], arrows=(M.FL_SETS["rec"]["arrows"][0], ("tw", "sr", "b", ""), M.FL_SETS["rec"]["arrows"][2]))),
              "② 流れの矢印か印", "cb04"),
             ("区分の順を入れ替える", "doc", "DC_SETS",
              dict(M.DC_SETS, cls=dict(M.DC_SETS["cls"], rows=(M.DC_SETS["cls"]["rows"][1], M.DC_SETS["cls"]["rows"][0]) + M.DC_SETS["cls"]["rows"][2:])),
              "② 書類の欄", "ca03"),
             ("2台を3台に", "cards2", "CD2_SETS",
              dict(M.CD2_SETS, rec2=dict(M.CD2_SETS["rec2"], cards=(M.CD2_SETS["rec2"]["cards"][0], ("3台",) + M.CD2_SETS["rec2"]["cards"][1][1:]))),
              "② 2つの札", "ca05"),
             ("要因12の印を11に", "factors", "FAC_MK", dict(M.FAC_MK, k12=((11, "メーカーとフランスの当局"),)), "② 印の要因", "ca14"),
             ("シンガポールを北へ", "asia", "ASIA_PTS", dict(M.ASIA_PTS, sg=(30.0, 103.85)), "② シンガポール"),
             ("1行目の報告書と判決の欄を入れ替える", "cmp", "CMP_ROWS", (("1", "入れたのは誰か", "副操縦士と認める", "特定できない"),) + M.CMP_ROWS[1:],
              "② 並べ図の行"),
             ("判決の欄を青に", "cmp", "CMP_COLS", (("報告書", "state"), ("判決", "state")), "② 並べ図の欄の名か色"))
    good_all = dict(good)
    for name, view, attr, val, why, *cid in cases:
        if cid and cid[0] not in good_all:
            print(f"  ⚠️ 17本目 陽性対照「{name}」：{cid[0]} のカットが無い（飛ばした）")
            continue
        if not cid and view not in by_view:
            print(f"  ⚠️ 17本目 陽性対照「{name}」：{view} のカットが無い（飛ばした）")
            continue
        keep = getattr(M, attr)
        setattr(M, attr, val)
        try:
            bad, _ = judge("m17", good_all[cid[0]] if cid else by_view[view])
        except Exception as e:      # 組めない＝止まる（fail closed）も鳴ったに数える
            bad = [f"{why}（例外：{e}）"]
        finally:
            setattr(M, attr, keep)
        g_ = any(b.startswith(why) for b in bad)
        ok &= g_
        print(f"  {'OK' if g_ else '🔴 NG'} 🔴 17本目 ⑤b-5 陽性対照：{name}: {'不合格' if bad else '合格'}（不合格のはず・理由「{why}」）"
              + (f"  ← {bad[0]}" if bad else ""))
    # rel から数を抜く（③＝画面の字の数の宣言）
    kw = dict(by_view["pitch"], rel=[r for r in by_view["pitch"]["rel"] if "52.6" not in r.get("t", "")])
    bad, _ = judge("m17", kw)
    g_ = any(b.startswith("③") and "52.6" in b for b in bad)
    ok &= g_
    print(f"  {'OK' if g_ else '🔴 NG'} 🔴 17本目 ⑤b-5 陽性対照：rel から 52.6 を抜く: {'不合格' if bad else '合格'}（不合格のはず・理由「③」）")
    return ok


def judge(kind, kw):
    f = getattr(F, kind)(**kw)
    if kind == "m17":
        return judge_m17(f)
    if kind == "m23":
        return judge_m23(f)
    if kind == "m22":
        return judge_m22(f)
    if kind == "m21":
        return judge_m21(f)
    if kind == "m20":
        return judge_m20(f)
    if kind == "m19":
        return judge_m19(f)
    return (judge_latch(f) if kind == "latch" else judge_section(f) if kind == "section"
            else judge_lash(f) if kind == "lash" else judge_tail(f) if kind == "tail"
            else judge_mod(f) if kind == "mod" else judge_bolt(f) if kind == "bolt"
            else judge_vsec(f) if kind == "vsec" else judge_lv(f) if kind == "lv"
            else judge_m18(f) if kind == "m18" else judge_hull(f))


def selftest():
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（本番の表は回ごとに空にする＝§0b）＝この処理の中だけ14本目にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    # 🔴 2026-10-01（16本目 ⑤b-1）：下の15本目の尾翼・改造・ねじの検算は REC_MOD・REC_BOLT を使う＝本番の表は16本目の空の器なので、
    #    見本 fixture_ep15 の表だけ差し込む（ss・GEO は触らない＝14本目の見本を壊さない）。main() が restore で戻す（LIFO）
    import fixture_ep15
    fixture_ep15.apply(sys.modules[__name__], tables_only=True)
    # 🔴 2026-10-04（18本目 ⑤b-1）：下の16本目の断面（vsec）・線の図（lv）の検算は REC_VSEC・REC_LV＊を使う＝本番の表は18本目の空の器なので、
    #    見本 fixture_ep16 の表だけ差し込む（ss・GEO は触らない＝14本目の見本を壊さない）。main() が restore で戻す（LIFO＝16→15→14）
    import fixture_ep16
    fixture_ep16.apply(sys.modules[__name__], tables_only=True)
    # 🔴 2026-10-06（19本目 ⑤b-1）：下の18本目の模式図（m18）の検算 `_selftest_m18` は REC_M18 を使う＝本番の表は19本目の空の器なので、
    #    見本 fixture_ep18 の表だけ差し込む（ss・GEO は触らない＝14本目の見本を壊さない）。main() が restore で戻す（LIFO＝18→16→15→14）
    import fixture_ep18
    fixture_ep18.apply(sys.modules[__name__], tables_only=True)
    # 🔴 2026-10-08（20本目 ⑤b-1）：下の19本目の模式図（m19）の検算 `_selftest_m19` は REC_M19 を使う＝本番の表は20本目の空の器なので、
    #    見本 fixture_ep19 の表だけ差し込む（ss・GEO は触らない＝14本目の見本を壊さない）。main() が restore で戻す（LIFO＝19→18→16→15→14）
    import fixture_ep19
    fixture_ep19.apply(sys.modules[__name__], tables_only=True)
    # 🔴 2026-10-12（21本目 ⑤b-1）：下の20本目の模式図（m20）の検算 `_selftest_m20` は REC_M20 を使う＝本番の表は21本目の空の器なので、
    #    見本 fixture_ep20 の表だけ差し込む（ss・GEO は触らない＝14本目の見本を壊さない）。main() が restore で戻す（LIFO＝20→19→18→16→15→14）
    import fixture_ep20
    fixture_ep20.apply(sys.modules[__name__], tables_only=True)
    # 🔴 2026-10-14（22本目 ⑤b-1）：下の21本目の模式図（m21）の検算 `_selftest_m21` は REC_M21 を使う＝本番の表は22本目の空の器なので、
    #    見本 fixture_ep21 の表だけ差し込む（ss・GEO は触らない＝14本目の見本を壊さない）。main() が restore で戻す（LIFO＝21→20→19→18→16→15→14）
    import fixture_ep21
    fixture_ep21.apply(sys.modules[__name__], tables_only=True)
    # 🔴 2026-10-18（23本目 ⑤b-1）：下の22本目の模式図（m22）の検算 `_selftest_m22` は REC_M22 を使う＝本番の表は23本目の空の器なので、
    #    見本 fixture_ep22 の表だけ差し込む（ss・GEO は触らない＝14本目の見本を壊さない）。main() が restore で戻す（LIFO＝22→21→20→19→18→16→15→14）
    import fixture_ep22
    fixture_ep22.apply(sys.modules[__name__], tables_only=True)
    # 🔴 2026-10-20（17本目 ⑤b-1）：下の23本目の模式図（m23）の検算 `_selftest_m23` は REC_M23 を使う＝本番の表は17本目の空の器なので、
    #    見本 fixture_ep23 の表だけ差し込む（ss・GEO は触らない＝14本目の見本を壊さない）。main() が restore で戻す（LIFO＝23→22→21→20→19→18→16→15→14）
    import fixture_ep23
    fixture_ep23.apply(sys.modules[__name__], tables_only=True)
    N = "模式図：テスト"
    ok = True
    closing = [dict(state=dict(hook="closed", motor="run"), tag=dict(t="フックが回る")),
               dict(state=dict(handle="down", pin="in", vent="closed", lamp="off", motor="idle"),
                    tag=dict(t="ピンが入る", at="pin"))]
    forced = [dict(state=dict(hook="short"), tag=dict(t="回りきらない")),
              dict(state=dict(handle="down", pin="butt", tube="bent", vent="closed", lamp="off"),
                   tag=dict(t="約22キロで閉まる", at="handle"))]
    sec_ok = [dict(state=dict(press="push"), tag=dict(t="空の上")),
              dict(state=dict(door="gone", press="none", air="out"), tag=dict(t="ドアが外れる")),
              dict(state=dict(floor="push"), tag=dict(t="床の上と下で差")),
              dict(state=dict(floor="down", cable="hurt"), tag=dict(t="床が落ちる"))]
    cases = [
        ("正しい閉め方（フック→ハンドル・ピン・通気扉・灯り）", "latch", dict(steps=closing, note=N), True),
        ("正しい無理な閉め方（約22キロ・仏 p80）", "latch",
         dict(steps=forced, note=N, rel=[dict(t="約22キロ", src="仏 p80")]), True),
        ("🔴 陽性対照：フック short のままピン in", "latch",
         dict(steps=[dict(state=dict(hook="short", handle="down", pin="in", vent="closed", lamp="off"),
                          tag=dict(t="x"))], note=N), False),
        ("🔴 陽性対照：ピンが入らないのにハンドル down・軸がたわまない", "latch",
         dict(steps=[dict(state=dict(hook="short", handle="down", pin="butt", vent="closed", lamp="off"),
                          tag=dict(t="x"))], note=N), False),
        ("🔴 陽性対照：ハンドル up のまま通気扉 closed", "latch",
         dict(steps=[dict(state=dict(hook="closed", vent="closed"), tag=dict(t="x"))], note=N), False),
        ("🔴 陽性対照：札の数「約30キロ」が宣言（約22キロ）と違う", "latch",
         dict(steps=[dict(forced[0]), dict(forced[1], tag=dict(t="約30キロで閉まる"))], note=N,
              rel=[dict(t="約22キロ", src="仏 p80")]), False),
        ("正しい断面（与圧→ドア→空気→床→ケーブル）", "section", dict(steps=sec_ok, note=N), True),
        ("🔴 陽性対照：ドアが付いたまま床が落ちる", "section",
         dict(steps=[dict(state=dict(floor="down"), tag=dict(t="x"))], note=N), False),
        ("🔴 陽性対照：床が落ちないのにケーブルが傷む", "section",
         dict(steps=[dict(state=dict(door="gone", air="out", cable="hurt"), tag=dict(t="x"))], note=N), False),
        ("🔴 陽性対照：逃げ道があるのに床が落ちる", "section",
         dict(steps=[dict(state=dict(door="gone", air="out", vent="open", floor="down", cable="hurt"),
                          tag=dict(t="x"))], note=N), False),
        # 14本目 ⑤b-4：断面F（hull）
        ("正しい改造（天井を上げる→延ばす・約5.6メートル＝海審 p1016）", "hull",
         dict(view="stern", start=dict(aroof="low", aext="off", bcab="off"),
              steps=[dict(state=dict(aroof="high"), tag=dict(t="天井を上げる")),
                     dict(state=dict(aext="on"), tag=dict(t="約5.6メートル延ばす"))],
              note=N, rel=[dict(t="約5.6メートル", src="海審 p1016")]), True),
        ("正しい水の順（3階→4階＝判決 p18）", "hull",
         dict(view="port", steps=[dict(state=dict(water="b", exits="shut3")), dict(state=dict(water="a", exits="shut"))],
              note=N), True),
        ("正しい重心と力（足す→上がる→傾くと力が小さい）", "hull",
         dict(view="pair", steps=[dict(), dict(state=dict(add="on", g="high", up="on")),
                                  dict(state=dict(heel=15.0, up="off", force="on"))],
              note=N, rel=[dict(heel=15.0, src="模式")]), True),
        ("正しい52.2度（3階の左舷の端が水面＝海審 p1057）", "hull",
         dict(view="front", start=dict(heel=52.2), steps=[dict(state=dict(paths="on"))], note=N,
              rel=[dict(heel=52.2, src="判決 p16")]), True),
        ("正しいタンクの水（表7＝約3割）", "hull",
         dict(view="hold", steps=[dict(state=dict(ballast="low"))], note=N), True),
        ("🔴 陽性対照：天井を上げないまま延ばす", "hull",
         dict(view="stern", start=dict(aroof="low", aext="off"), steps=[dict(state=dict(aext="on"))], note=N), False),
        ("🔴 陽性対照：4階の手すりのあとに3階（水が下がる）", "hull",
         dict(view="port", steps=[dict(state=dict(water="a")), dict(state=dict(water="b"))], note=N), False),
        ("🔴 陽性対照：水の前に出入口が閉じる", "hull",
         dict(view="port", steps=[dict(state=dict(exits="shut3"))], note=N), False),
        ("🔴 陽性対照：足さないのに重心が上がる", "hull",
         dict(view="pair", steps=[dict(state=dict(g="high"))], note=N), False),
        ("🔴 陽性対照：札の数「約9.9メートル」が宣言に無い", "hull",
         dict(view="side", steps=[dict(tag=dict(t="約9.9メートル"))], note=N,
              rel=[dict(t="約5.6メートル", src="海審 p1016")]), False),
        # 🆕 ⑤b-7b：喫水の寄り（hull の mark）と固縛（lash）
        ("正しい喫水の寄り（水面 約6.20・限りの線 6.26＝海審 p1038）", "hull",
         dict(view="mark", steps=[dict(state=dict(water="seen")), dict(state=dict(full="on"))], note=N), True),
        ("正しい乗用車（前・後ろ2本ずつ → 1本ずつ・各タイヤに木の止め）", "lash",
         dict(view="car", steps=[dict(state=dict(car="req")), dict(state=dict(car="all"))], note=N, src="s"), True),
        ("正しい乗用車と25トン車（10本 → 鎖4本）", "lash",
         dict(view="both", steps=[dict(state=dict(car="all")), dict(state=dict(truck="all"),
                                                                    tag=dict(t="25トン車の鎖", xy=(1200, 300)))],
              note=N, src="s", rel=[dict(t="25トン", src="海審 p1093")]), True),
        ("正しい仮ナンバーの車の面（帯なし）", "lash",
         dict(view="loose", steps=[dict(state=dict(zone="on"))], note=N, src="s"), True),
        ("正しい2段の箱（留め金の場所・ロープ）", "lash",
         dict(view="box", steps=[dict(state=dict(lock="on")), dict(state=dict(rope="on"))], note=N, src="s"), True),
        ("🔴 陽性対照：固縛の札の数「約30本」が宣言に無い", "lash",
         dict(view="car", steps=[dict(state=dict(car="all"), tag=dict(t="約30本", xy=(100, 300)))], note=N, src="s"), False),
    ]
    # 🆕 15本目 ⑤b-3：尾翼の板の模式図（tail）＝筋（AAB p14・p22・p23・p28・p40〜p42）・画素・札の数
    trim = [dict(tag=dict(t="トリムタブ")),
            dict(state=dict(tab="up", force="on", elev="down"), tag=dict(t="後ろの縁が上へ 8度", at="b1", to="tab"))]
    pop = [dict(state=dict(link="broken", tab="free", force="off", elev="up"), tag=dict(t="リンクが折れる", at="b1", to="link")),
           dict(state=dict(nose="on"), tag=dict(t="機首が上がる", at="nose", to="nose"))]
    spread = [dict(state=dict(llink="broken", shake="left")), dict(state=dict(rlink="broken", shake="both", spread="on"))]
    cases += [
        ("15本目 正しい尾翼（横から：0度→後ろの縁が上へ8度・押す力・昇降舵が下がる）", "tail",
         dict(view="side", steps=trim, note=N, rel=[dict(t="8度", src="AAB p22")]), True),
        ("15本目 正しい尾翼（横から：リンクが折れ→力が消え→昇降舵がはね上がり機首が上がる）", "tail",
         dict(view="side", start=dict(tab="up", force="on", elev="down"), steps=pop, note=N), True),
        ("15本目 正しい尾翼（上から：左のリンク→右の震え・右のリンク・広がり）", "tail", dict(view="plan", steps=spread, note=N), True),
        ("15本目 正しい尾翼（上から：ふつうの P-51D＝2枚とも動く）", "tail",
         dict(view="plan", steps=[dict(state=dict(mode="stock"))], note=N), True),
        ("🔴 15本目 陽性対照：板が限りを越えたのにリンクが折れていない", "tail",
         dict(view="side", steps=[dict(state=dict(tab="free"))], note=N), False),
        ("🔴 15本目 陽性対照：昇降舵が下がったまま機首が上がる", "tail",
         dict(view="side", steps=[dict(state=dict(nose="on"))], note=N), False),
        ("🔴 15本目 陽性対照：リンクが折れたのに押す力が残る", "tail",
         dict(view="side", start=dict(tab="up", force="on", elev="down"), steps=[dict(state=dict(link="broken"))], note=N), False),
        ("🔴 15本目 陽性対照：右のリンクが先に折れる（記録は左→右）", "tail",
         dict(view="plan", steps=[dict(state=dict(rlink="broken"))], note=N), False),
        ("🔴 15本目 陽性対照：ふつうの P-51D に鉄の棒の印", "tail",
         dict(view="plan", steps=[dict(state=dict(mode="stock", rod="on"))], note=N), False),
        ("🔴 15本目 陽性対照：札の角度「約10度」が宣言（8度）に無い", "tail",
         dict(view="side", steps=[dict(state=dict(tab="up", force="on", elev="down"), tag=dict(t="約10度"))], note=N,
              rel=[dict(t="8度", src="AAB p22")]), False),
        # 🆕 ⑤b-4：尾翼の断面に塗った材料と板の重心（c511）
        ("15本目 正しい尾翼（材料を塗る → 板の重心が後ろへ）", "tail",
         dict(view="side", steps=[dict(state=dict(fill="on"), tag=dict(t="最大約3ミリ", at="stab")),
                                  dict(state=dict(cg="aft"), tag=dict(t="重心が後ろへ", at="b1", to="cg"))],
              note=N, rel=[dict(t="約3ミリ", src="AAB p14")]), True),
        ("🔴 15本目 陽性対照：材料を塗らずに板の重心が後ろへ", "tail",
         dict(view="side", steps=[dict(state=dict(cg="aft"))], note=N), False),
        # 🆕 ⑤b-4：改造の比べ（mod）
        ("15本目 正しい改造の比べ（上から：ふつうの形 → 翼の幅の寸法）", "mod",
         dict(view="plan", steps=[dict(state=dict(stock="on")),
                                  dict(state=dict(span="on"), tag=dict(t="約11.3メートル"))], note=N,
              rel=[dict(t="約11.3メートル", src="AAB p13")]), True),
        ("15本目 正しい改造の比べ（横から：箱 → 沸く → 湯気で外へ）", "mod",
         dict(view="side", steps=[dict(state=dict(scoop="dim", boiler="on", boil="on", vent="on"))], note=N), True),
        ("15本目 正しいおもりの比べ（事故機 → ふつうの最大 → 約2倍 → 敏感に → 動きを安定させるおもり）", "mod",
         dict(view="weights", steps=[dict(state=dict(cw="acc")), dict(state=dict(cw="both", cwx2="on"), tag=dict(t="約2倍")),
                                     dict(state=dict(sens="on")), dict(state=dict(bw="on"))], note=N,
              rel=[dict(t="約2倍", src="AAB p43")]), True),
        ("🔴 15本目 陽性対照：ふつうの形なしに翼の幅の寸法", "mod",
         dict(view="plan", steps=[dict(state=dict(span="on"))], note=N), False),
        ("🔴 15本目 陽性対照：沸く前に湯気で外へ", "mod", dict(view="side", steps=[dict(state=dict(boiler="on", vent="on"))], note=N),
         False),
        ("🔴 15本目 陽性対照：ふつうの最大を出さずに「約2倍」の線", "mod",
         dict(view="weights", steps=[dict(state=dict(cw="acc", cwx2="on"))], note=N), False),
        ("🔴 15本目 陽性対照：札「約3倍」が宣言（約2倍）に無い", "mod",
         dict(view="weights", steps=[dict(state=dict(cw="both", cwx2="on"), tag=dict(t="約3倍"))], note=N,
              rel=[dict(t="約2倍", src="AAB p43")]), False),
        # 🆕 ⑤b-4：ねじとナットとフラッター（bolt）
        ("15本目 正しいねじ（短いねじ＝決まりの影・先がナットの端）", "bolt",
         dict(view="nut", start=dict(insert="old"), steps=[dict(state=dict(screw="short", ghost="on")), dict(state=dict(tip="on"))],
              note=N), True),
        ("15本目 正しいねじ（締め直し → 3回 → ゆるんでいた）", "bolt",
         dict(view="nut", start=dict(insert="old"), steps=[dict(state=dict(tight="on")),
                                                           dict(state=dict(tight="off", flights="3", loose="on"),
                                                                tag=dict(t="3回"))],
              note=N, rel=[dict(t="3回", src="AAB p41")]), True),
        ("15本目 正しい支え（ゆるむ → かたさが落ちてぐらつく → 震え → かみ合う → 続き方）", "bolt",
         dict(view="spring", steps=[dict(state=dict(screw="loose")), dict(state=dict(stiff="low", wobble="on")),
                                    dict(state=dict(shake="on")), dict(state=dict(air="on")), dict(state=dict(graph="on"))],
              note=N), True),
        ("15本目 正しい速さとかたさ（起きやすい所・向き → 事故機 → 輪）", "bolt",
         dict(view="chart", steps=[dict(state=dict(region="on", arrows="on")), dict(state=dict(acc="on")),
                                   dict(state=dict(ring="on"))], note=N), True),
        ("🔴 15本目 陽性対照：決まりの長さのねじに「決まりの影」", "bolt",
         dict(view="nut", steps=[dict(state=dict(ghost="on"))], note=N), False),
        ("🔴 15本目 陽性対照：古い詰め物がねじ山を締めつける", "bolt",
         dict(view="nut", start=dict(insert="old"), steps=[dict(state=dict(clamp="on"))], note=N), False),
        ("🔴 15本目 陽性対照：ゆるまずに塗装がはげる", "bolt",
         dict(view="nut", start=dict(insert="old"), steps=[dict(state=dict(paint="on"))], note=N), False),
        ("🔴 15本目 陽性対照：締め直したあと飛ばずにゆるむ", "bolt",
         dict(view="nut", start=dict(insert="old"), steps=[dict(state=dict(tight="on")), dict(state=dict(tight="off", loose="on"))],
              note=N), False),
        ("🔴 15本目 陽性対照：かたさが落ちないまま震える（フラッター）", "bolt",
         dict(view="spring", steps=[dict(state=dict(screw="loose", shake="on"))], note=N), False),
        ("🔴 15本目 陽性対照：起きやすい所なしに事故機の点", "bolt", dict(view="chart", steps=[dict(state=dict(acc="on"))], note=N),
         False),
    ]
    for name, kind, kw, want in cases:
        bad, _ = judge(kind, kw)
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 画素の陽性対照：型の定数をわざと壊して、筋は正しいのに**絵が状態と食い違う**ことを捕まえるか
    keep = dict(F.LATCH_ROT["hook"])
    F.LATCH_ROT["hook"]["short"] = 0.0          # 回りきらないフックを「閉まりきった角度」で描く
    bad, _ = judge("latch", dict(steps=forced, note=N, rel=[dict(t="約22キロ", src="仏 p80")]))
    F.LATCH_ROT["hook"].update(keep)
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照（画素）：short を0度で描く型＝ピン butt の絵が嘘: "
          f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    keep_drop = F.SC["drop"]
    F.SC["drop"] = 0.0                            # 床を落とさない型
    bad, _ = judge("section", dict(steps=sec_ok, note=N))
    F.SC["drop"] = keep_drop
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照（画素）：床を落とさない型＝床 down の絵が嘘: "
          f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 断面F の画素の陽性対照：型の定数をわざと壊す（延ばした長さ・タンクの水・52.2度の甲板の高さ）
    import hull as H
    for name, attr, val, kw in (
            ("延ばした長さを 6.6 で描く型", "A_EXT", 6.6,
             dict(view="stern", start=dict(aroof="high", aext="on"), steps=[dict()], note=N)),
            ("タンクの水を半分で描く型", "BW_FRAC", dict(H.BW_FRAC, low=0.5),
             dict(view="hold", steps=[dict(state=dict(ballast="low"))], note=N)),
            ("3階の床を3メートル高く描く型", "B_Y", H.B_Y + 3.0,
             dict(view="front", start=dict(heel=52.2), steps=[dict()], note=N, rel=[dict(heel=52.2, src="判決 p16")]))):
        keep = getattr(H, attr)
        setattr(H, attr, val)
        try:
            if attr == "A_EXT":
                keep_x = H.X_AEXT
                H.X_AEXT = H.X_COMP[0] - val
            bad, _ = judge("hull", kw)
        finally:
            setattr(H, attr, keep)
            if attr == "A_EXT":
                H.X_AEXT = keep_x
        good = bool(bad)
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照（画素）：{name}: "
              f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    try:
        judge("hull", dict(view="front", start=dict(heel=40.0), steps=[dict()], note=N))
        good = False
    except ValueError:
        good = True
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照：宣言の無い傾き 40度で型が止まる: {'止まった' if good else '通った'}（止まるはず）")
    # 🆕 ⑤b-7b：喫水の寄りと固縛の画素の陽性対照（型の表・定数をわざと壊す＝描いた絵が記録と食い違う）
    import lash as Lh
    mark_kw = dict(view="mark", steps=[dict(state=dict(water="seen", full="on"))], note=N)
    car_kw = dict(view="car", steps=[dict(state=dict(car="req")), dict(state=dict(car="all"))], note=N, src="s")
    both_kw = dict(view="both", steps=[dict(state=dict(car="all")), dict(state=dict(truck="all"))], note=N, src="s")
    box_kw = dict(view="box", steps=[dict(state=dict(lock="on")), dict(state=dict(rope="on"))], note=N, src="s")
    zone_kw = dict(view="loose", steps=[dict(state=dict(zone="on"))], note=N, src="s")
    keep_zone, keep_box = Lh._zone_svg, Lh._box_layer
    for name, mod, attr, val, kind, kw in (
            ("限りの線を 6.20 に描く型", H, "FULL_DRAFT", 6.20, "hull", mark_kw),
            ("水面を 6.30 に描く型", H, "DRAFT", 6.30, "hull", mark_kw),
            ("乗用車の実際の帯を前2本で描く型", Lh, "CAR_ACT", (("front", -1), ("front", +1), ("rear", +1)), "lash", car_kw),
            ("25トン車の基準の帯を9本で描く型", Lh, "TRUCK_REQ", Lh.TRUCK_REQ[:9], "lash", both_kw),
            ("25トン車の鎖を5本で描く型", Lh, "TRUCK_ACT", Lh.TRUCK_ACT + (("side", -1, 0.12),), "lash", both_kw),
            ("仮ナンバーの車の面に帯を描く型", Lh, "_zone_svg",
             lambda: keep_zone() + Lh._g("zone|belt", F.line(0, 0, 9, 9, "#fff", 2)), "lash", zone_kw),
            ("留め金を使った絵を描く型", Lh, "_box_layer",
             lambda what: keep_box(what) + Lh._g("box|lock|used", F.rect(0, 0, 9, 9, "#fff")), "lash", box_kw)):
        keep = getattr(mod, attr)
        setattr(mod, attr, val)
        try:
            bad, _ = judge(kind, kw)
        finally:
            setattr(mod, attr, keep)
        good = bool(bad)
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照（画素）：{name}: "
              f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    try:
        judge("lash", dict(view="car", steps=[dict(state=dict(car="all")), dict(state=dict(car="req"))], note=N, src="s"))
        good = False
    except ValueError:
        good = True
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照：固縛の段が戻る（all → req）で型が止まる: {'止まった' if good else '通った'}（止まるはず）")
    # 🔴 15本目 ⑤b-3 画素の陽性対照（描く側の定数を壊す）：①限りを越えた板を 15度で描く（21度以上＝p28 に届かない）
    #    ②折れたリンクのすき間を0に（折れて見えない）
    import tail15 as T
    keep = dict(T.TAB_DEG)
    T.TAB_DEG["free"] = 15.0
    try:
        bad, _ = judge("tail", dict(view="side", start=dict(tab="up", force="on", elev="down"), steps=pop, note=N))
    finally:
        T.TAB_DEG.update(keep)
    good = any("板 free" in b for b in bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 15本目 陽性対照（画素）：限りを越えた板を15度で描く型: "
          f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    keep = T.GAP
    T.GAP = 0.0
    try:
        bad, _ = judge("tail", dict(view="plan", steps=spread, note=N))
    finally:
        T.GAP = keep
    good = any("リンク broken" in b for b in bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 15本目 陽性対照（画素）：折れたリンクのすき間0の型: "
          f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 15本目 ⑤b-4 画素の陽性対照（描く側の定数を壊す＝筋は正しいのに絵が記録と食い違う）
    import mod15 as Mo
    import bolt15 as Bo
    cg_kw = dict(view="side", steps=[dict(state=dict(fill="on")), dict(state=dict(cg="aft"))], note=N)
    w_kw = dict(view="weights", steps=[dict(state=dict(cw="both", bw="on"))], note=N)
    for name, mod_, attr, val, kind, kw, key in (
            ("板の重心 aft を元より前に描く型", T, "CG_AT", dict(T.CG_AT, aft=0.30), "tail", cg_kw, "重心 aft"),
            ("左のおもりを 20ポンドで描く型", Mo, "W_KG", dict(Mo.W_KG, cw_acc=20.0 * 0.45359237), "mod", w_kw, "おもりの高さの比"),
            ("動きを安定させるおもりを 0.6倍で描く型", Mo, "W_KG", dict(Mo.W_KG, bw_acc=Mo.BW_STOCK * 0.6), "mod", w_kw,
             "動きを安定させる"),
            ("事故機の形を縦に 1.1倍で描く型", Mo, "MOD", [[x, Mo.Y_C + (y - Mo.Y_C) * 1.1] for x, y in Mo.MOD], "mod",
             dict(view="plan", steps=[dict(state=dict(stock="on"))], note=N), "事故機の翼の幅"),
            ("沸かして冷やす箱を胴の上に描く型", Mo, "BOX", (-5.75, 0.9, -4.85, 1.5), "mod",
             dict(view="side", steps=[dict(state=dict(boiler="on"))], note=N), "胴の形の外"),
            ("短いねじの先をナットの端の 30画素上に描く型", Bo, "TIP", dict(Bo.TIP, short=Bo.NUT_END - 30.0), "bolt",
             dict(view="nut", start=dict(insert="old"), steps=[dict(state=dict(screw="short"))], note=N), "そろわない"),
            ("古い詰め物のすき間を0に描く型", Bo, "INS_GAP", dict(Bo.INS_GAP, old=0.0), "bolt",
             dict(view="nut", steps=[dict(state=dict(insert="old"))], note=N), "詰め物 old"),
            ("フラッターの揺れを 0度で描く型", Bo, "GHOST_DEG", dict(Bo.GHOST_DEG, shake=0.0), "bolt",
             dict(view="spring", steps=[dict(state=dict(screw="loose", stiff="low", shake="on"))], note=N), "揺れの幅"),
            ("事故機の点を起きにくい所に描く型", Bo, "ACC_UV", (0.3, 0.8), "bolt",
             dict(view="chart", steps=[dict(state=dict(region="on", acc="on"))], note=N), "起きやすい所」の外")):
        keep = getattr(mod_, attr)
        setattr(mod_, attr, val)
        try:
            bad, _ = judge(kind, kw)
        finally:
            setattr(mod_, attr, keep)
        good = any(key in b for b in bad)
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} 🔴 15本目 陽性対照（画素）：{name}: "
              f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    ok = _selftest_vsec(ok)
    ok = _selftest_lv(ok)
    ok = _selftest_m18(ok)
    ok = _selftest_m19(ok)
    ok = _selftest_m20(ok)
    ok = _selftest_m21(ok)
    ok = _selftest_m22(ok)
    ok = _selftest_m23(ok)
    ok = _selftest_m17(ok)       # 🆕 17本目 ⑤b-5：本番の m17 が通り・壊した定数が狙った理由で鳴る
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import fixture_ep14
    import fixture_ep15
    import fixture_ep16
    import fixture_ep18
    import fixture_ep19
    import fixture_ep20
    import fixture_ep21
    import fixture_ep22
    import fixture_ep23
    fixture_ep23.restore()       # 🔴 17本目 ⑤b-1：selftest で足した23本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep22.restore()       # 🔴 23本目 ⑤b-1：selftest で足した22本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep21.restore()       # 🔴 22本目 ⑤b-1：selftest で足した21本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep20.restore()       # 🔴 21本目 ⑤b-1：selftest で足した20本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep19.restore()       # 🔴 20本目 ⑤b-1：selftest で足した19本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep18.restore()       # 🔴 19本目 ⑤b-1：selftest で足した18本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep16.restore()       # 🔴 18本目 ⑤b-1：selftest で足した16本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep15.restore()       # 🔴 16本目 ⑤b-1：selftest で足した15本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep14.restore()       # 🔴 15本目 ⑤b-2：selftest で差し込んだ14本目の見本を本番の表に戻す（戻さないと14本目の表で本番を測る）
    import cuts
    targets = {c: s["fig"] for c, s in sorted(cuts.SPEC.items())
               if s.get("fig") and s["fig"][0] in ("latch", "section", "hull", "lash", "tail", "mod", "bolt", "vsec", "lv", "m18",
                                                   "m19", "m20", "m21", "m22", "m23", "m17")}
    if not targets:
        print("⚠️ latch・section・hull・lash・tail・mod・bolt のカットが0件（この回に仕組みの模式図が無いなら正しい。"
              "**0件を調べて合格**にしていないか確かめる）")
        return 0
    bad_all, n_all = 0, 0
    for cid, (kind, kw) in targets.items():
        bad, n = judge(kind, kw)
        if kind == "m23":         # 🆕 23本目 ⑤b-3：見る向きの合図（PLAN の「見る向き：」× 左上の札）
            n += 1
            vb = view_dir_check(cuts.PLAN.get(cid, {}).get("plan", ""), F.m23(**kw).mech["lab"])
            bad = list(bad) + ([f"② {vb}"] if vb else [])
        if kind == "m17":         # 🆕 17本目 ⑤b-5：見る向きの合図（「正面」も）
            n += 1
            vb = view_dir_check17(cuts.PLAN.get(cid, {}).get("plan", ""), F.m17(**kw).mech["lab"])
            bad = list(bad) + ([f"② {vb}"] if vb else [])
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {cid}（{kind}）: {b}")
        else:
            print(f"✓ {cid}（{kind}）: 筋と部品の画素・札の数 {n}件が合う")
    print(f"\n{'✓' if not bad_all else '🔴'} 仕組みの模式図 {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
