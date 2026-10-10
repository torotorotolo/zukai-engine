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
#    頁＝`ref/ep20/src/ep20_pages.txt`（報告書＝印刷の頁・別添6 は p310〜343・解説＝1000＋頁）で当てた。
#    🔴 §0b（題材を替えるとき）：21本目に入るときは、この表を見本 fixture へ移して空にする（m19 と同じ）
FT = 0.3048
REC_M20 = dict(
    # 操縦室の席（p6「副操縦士の機長昇格訓練のため、機長が右操縦士席、副操縦士が左操縦士席に位置し」・p148 付図-12＝P4 機関士計器は右の壁）
    seats=dict(day=("副操縦士", "機長"), usual_left="機長", src="報告書 p6・p148"),
    xpdr_digits=(4, "報告書 p6（緊急コード番号7700）"),
    # エンジンの横の位置（付図-4「有効エンジン・モーメントアーム」内側 Y_EI 12.07m・外側 Y_EO 21.15m）・左の2基＝No.1・No.2（p82）
    eng_y=((12.07, 21.15), "報告書 p140（付図-4）"),
    left_engines=({1, 2}, "報告書 p82（左側第1、第2エンジン・右側第3、第4エンジン）"),
    hyd_n=(4, "報告書 p112（配管を4系統）"),
    # 管が切れる所＝垂直尾翼の中（p113「垂直尾翼の損壊に伴う操縦系統油圧配管の切断」）＝後部圧力隔壁 BS2360（p29＝57.66m）より後ろ・
    #   垂直尾翼の後縁の根元（付図-4 の横の図＝71.2m）より前
    hyd_cut=((57.66, 71.2), "報告書 p113・p29・p140"),
    cg_x=(31.75, "報告書 p140（付図-4「104 FT 2 IN」＝機首から 0.25 MAC まで）"),
    # 高さの記録の点（時刻, フィート）＝cruise は付図-1 の時刻と高度の札（p137）・final は p82（18:55:57ごろ 約10,000フィート・
    #   18:56:17ごろ 約5,500フィート）と付図-1（18:56:03 8,400）
    alt=dict(cruise=[("18:24:12", 23400), ("18:24:35", 23900), ("18:25:18", 23900), ("18:27:07", 24400), ("18:28:36", 22100),
                     ("18:31:08", 24900), ("18:34:53", 21400), ("18:38:06", 22400), ("18:40:30", 22400), ("18:41:59", 20900),
                     ("18:43:05", 18600), ("18:44:09", 17000), ("18:45:48", 13500), ("18:47:17", 9000), ("18:48:03", 6800)],
             final=[("18:55:57", 10000), ("18:56:03", 8400), ("18:56:17", 5500)]),
    alt_src="報告書 p137（付図-1）・p82",
    # 印の時刻＝18:25:21（p6・p115 降下の要求）・18:40（p115「実際に降下を始めたのは18時40分以降」）・18:56:07（p82 頭下げ約36度）・
    #   18:56:17（p82 地上接近警報）
    alt_marks=dict(cruise=dict(m1="18:25:21", m2="18:40:00"), final=dict(m1="18:56:07", m2="18:56:17")),
    alt_rate=(15000.0, "報告書 p82（降下率は平均15,000フィート/分）"),
    gear=(25.59, "報告書 p140（付図-4「83 FT 11.5 IN」＝前の脚から主脚まで）・p117（18時38分以降脚下げ・18時44分以降フラップ下げ）"),
    radio=dict(names=dict(left="東京コントロール", right="羽田"), src="報告書 p6（東京管制区管制所＝東京コントロール）・p333（羽田にコンタクトしますか？）"),
    fix=dict(plane=(5.0, 1.0), heli=(1.0, 0.1), ray=(305.0, 35.0), src="解説 p1018（方位は5度、距離は1マイル／方位1度、距離0.1マイル）・p1019（①）"),
    bulk_x=(57.66, "報告書 p29（BS2360）"),
    # 3つの空港（p117「目的地の大阪国際空港や予定飛行経路から比較的近い名古屋空港ではなく東京国際空港を選んだことは、空港の規模、
    #   滑走路長及びその他の施設環境からみて妥当な選択」）・経度は一般の地図の値（東西の順を照らすだけ）
    apt=dict(lons={"大阪国際空港": 135.44, "名古屋空港": 136.92, "東京国際空港": 139.78}, picked="東京国際空港",
             why=("空港の規模", "滑走路長", "その他の施設環境"), src="報告書 p117"),
    clock={"18:25:21", "18:50:50", "18:42:53", "18:44:43", "18:56:07", "18:56:17", "18:55:57", "18:46:09"},
    # 🆕 ⑤b-6（第6〜8章）：p44「上側ウエブの下端から2列目のリベット孔を縫って破断…付図―38(a)」・p45「第1から第3ストラップの間の、
    #   ダブラ・プレートにより補強された部分の断面構造は、付図-38(b)」（上側ウエブの下端から1列目）・p102「この部分の強度は本来の強度の
    #   70パーセント程度に低下」・p124（同）・p65「1列リベットの場合の疲労亀裂は2列リベットの場合と比較すると、2倍強の速さで進展する」・
    #   別添1 p248「左側の第一ストラップと第3ストラップ間の2べイ分の結合が1列リベット結合」・p110「1ベイ・フェール・セーフ」・
    #   別添1 p246「後部圧力隔壁については、下半部（コレクタ・リングを含む。）の交換」・p103「当該接続部分の縁がフィレット・シールで覆われている」・
    #   p104「後部圧力隔壁後面全体の目視検査（G2レベル相当）」・p100「リベット孔両側平均で10ミリメートル（可視亀裂長さ8ミリメートル）」・
    #   「1つの疲労亀裂の発見確率は、10パーセント程度」・「少なくとも1つを発見できる確率は14～60パーセント程度」・p105（コ）・p103（ウ）
    #   「客室最後部位置の化粧室」「客室後部コートルーム」
    fatigue=dict(src="報告書 p65（多数のリベット孔縁より疲労亀裂が発生）"),
    rows=dict(n=dict(a=2, b=1), ratio=0.70, src="報告書 p44・p45（付図-38(a)(b)）・p102・p124（70パーセント程度に低下）"),
    grow=dict(ratio=(2.0, 2.5), src="報告書 p65（2倍強の速さで進展）"),
    fs=dict(one=(1, 3), src="報告書 p248（左側の第1ストラップと第3ストラップ間の2ベイ分）・p110（1ベイ・フェール・セーフ）"),
    half=dict(new="lo", src="報告書 p246（後部圧力隔壁については、下半部…の交換）"),
    edge=dict(src="報告書 p248（エッジ・マージンが構造修理マニュアルに記載された値より不足）"),
    seal=dict(ends=("upper", "splice", "lower"), src="報告書 p103（接続部分の縁がフィレット・シールで覆われている）・p174（付図-38）"),
    rear=dict(src="報告書 p104（後部圧力隔壁後面全体の目視検査）"),
    clen=dict(ratio=0.8, src="報告書 p100（リベット孔両側平均で10ミリメートル（可視亀裂長さ8ミリメートル））"),
    prob=dict(one=10.0, many=(14.0, 60.0), src="報告書 p100（10パーセント程度・14～60パーセント程度）"),
    two=dict(src="報告書 p105（隔壁が正規に製作されている場合、またその修理が適正に行われている場合には…妥当な点検方法）"),
    lav=dict(src="報告書 p103（客室最後部位置の化粧室・客室後部コートルーム）"),
    assume=dict(hyd=("cut", "on"), thrust=("nose", "up"), rows=("bars", "on"), clen=("len", "on")))


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
        lav=dict(view="lav", steps=[dict(state=dict(lav="on")), dict(state=dict(coat="on", bend="on"))], note=N))
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
            ("化粧室を隔壁の後ろに描く", "LV", dict(M.LV, lav=(58.0, 60.5)), "化粧室", "lav")):
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
            ("強さの棒に推定の札が無い", dict(view="rows", steps=[dict(state=dict(bars="on"), tag=dict(t="強さ", at="str"))], note=N), "推定")):
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


def judge(kind, kw):
    f = getattr(F, kind)(**kw)
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
    fixture_ep19.restore()       # 🔴 20本目 ⑤b-1：selftest で足した19本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep18.restore()       # 🔴 19本目 ⑤b-1：selftest で足した18本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep16.restore()       # 🔴 18本目 ⑤b-1：selftest で足した16本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep15.restore()       # 🔴 16本目 ⑤b-1：selftest で足した15本目の見本の表を戻す（あとに差し込んだ側から＝LIFO）
    fixture_ep14.restore()       # 🔴 15本目 ⑤b-2：selftest で差し込んだ14本目の見本を本番の表に戻す（戻さないと14本目の表で本番を測る）
    import cuts
    targets = {c: s["fig"] for c, s in sorted(cuts.SPEC.items())
               if s.get("fig") and s["fig"][0] in ("latch", "section", "hull", "lash", "tail", "mod", "bolt", "vsec", "lv", "m18",
                                                   "m19", "m20")}
    if not targets:
        print("⚠️ latch・section・hull・lash・tail・mod・bolt のカットが0件（この回に仕組みの模式図が無いなら正しい。"
              "**0件を調べて合格**にしていないか確かめる）")
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
