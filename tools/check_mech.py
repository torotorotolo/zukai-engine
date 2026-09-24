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

NUM = re.compile(r"約?[0-9０-９][0-9０-９,.．]*\s*(キロ|ミリ|メートル|ポンド|㎡|平方メートル|人|秒|分|時|度)")


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
        sag = tk["pts"][1][1] - tk["pts"][0][1]
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


def judge(kind, kw):
    f = getattr(F, kind)(**kw)
    return judge_latch(f) if kind == "latch" else judge_section(f)


def selftest():
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
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import cuts
    targets = {c: s["fig"] for c, s in sorted(cuts.SPEC.items())
               if s.get("fig") and s["fig"][0] in ("latch", "section")}
    if not targets:
        print("⚠️ latch・section のカットが0件（この回に仕組みの模式図が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
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
