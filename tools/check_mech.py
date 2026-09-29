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
NUM = re.compile(r"約?[0-9０-９][0-9０-９,.．]*\s*(キロ|ミリ|メートル|ポンド|㎡|平方メートル|人|秒|分|時|度|トン|本|台|個|センチ)")


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


def judge(kind, kw):
    f = getattr(F, kind)(**kw)
    return (judge_latch(f) if kind == "latch" else judge_section(f) if kind == "section"
            else judge_lash(f) if kind == "lash" else judge_hull(f))


def selftest():
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（本番の表は回ごとに空にする＝§0b）＝この処理の中だけ14本目にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
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
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import cuts
    targets = {c: s["fig"] for c, s in sorted(cuts.SPEC.items())
               if s.get("fig") and s["fig"][0] in ("latch", "section", "hull", "lash")}
    if not targets:
        print("⚠️ latch・section・hull・lash のカットが0件（この回に仕組みの模式図が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
        return 0
    bad_all, n_all = 0, 0
    for cid, (kind, kw) in targets.items():
        bad, n = judge(kind, kw)
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
