# -*- coding: utf-8 -*-
"""切り方（`xbias` / `bias` / `zoom`）を**総当たりで探す**道具（2026-09-07 に tools/ へ移した）。

■ なぜ要るか
    台帳の「直しの当たり」は式で書いてあるが、**2026-09-04 に2件・09-06 に3件外れている**
    （[[feedback-verify-the-ledgers-suggested-fix]]）。「どこが変か」は目で正しく言えても、
    「いくつにするか」は式と実測で決めないと当たらない。
    門番 `check_slide` が「行頭が切れる／帯に入る／注記が焼き込みに載る／名指しが窓に無い」を
    **数で**言えるので、**その数がいちばん少ない切り方を機械で探す**。

■ 🔴 守っていること（過去に踏んだ罠）
    1. **判定は本番の `check_slide.scan()` を呼ぶ。**判定を2か所に書かない
       （`check_dup.selfcheck()` が別実装を持っていて、本番を直しても検算が緑のままだった）
    2. **`--keep` を必ず1つ以上。**残したい物を言わずに探すと
       「**何も写らない切り方**」が満点になる（0件だから）
    3. **元の切り方の近くだけを探す。**全域を探すと「粗は0件だが構図が別物」が満点になる
       （ep05 で bias 0.72→0.2 が出た）。⑤c の目視で構図は承認ずみなので、
       大きく動かしてよいのは主に `xbias`（左右）
    4. 出した答えは**そのままコミットしない**。`check_slide.py --draw <cid>` で
       k=0/k=1 を描いて見てから直す

■ 使い方
    python tools/fitcrop.py show  c423
    python tools/fitcrop.py solve c423 --keep "column specimen" --keep "slab top"
    python tools/fitcrop.py solve c423 --keepvisible        # いま丸ごと写っている行を全部残す
    python tools/fitcrop.py solve c423 --keepbox 120,340,880,410   # 文字でない決め所
    python tools/fitcrop.py --selftest

■ 出力
    show  … 原画の寸法／k=0 と k=1 の切り出し窓／画面に入る行（画面座標 x0）／いまの 🔴 と ・
    solve … `cid  → xbias=… , bias=… , zoom=…   🔴n件 ・m件 （もと …）` の1行
            見つからなければ「条件を満たす切り方が見つかりません」（**勝手に緩めない**）
    exit  … 0＝答えが出た／1＝見つからない・引数が足りない
"""
from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

import check_slide as CS      # noqa: E402  🔴 判定も幾何も本番のここ1本から借りる

W, H = CS.W, CS.H


def load():
    spec_map, photo_of, box_of, skip = CS.production_inputs()
    return spec_map, CS.load_ocr(), photo_of, box_of, skip


def geom(cid, spec_map, ocr, photo_of, box_of, skip, override=None):
    spec = dict(spec_map[cid])
    if override:
        spec.update(override)
    return CS.cut_geom(cid, spec, ocr, photo_of, box_of, skip)


def one(cid, spec_map, ocr, photo_of, box_of, skip, override=None, jobs=None):
    """そのカット1つだけを **本番の scan()** に通し、(🔴, ・) を返す。"""
    sm = {cid: dict(spec_map[cid])}
    if override:
        sm[cid].update(override)
    return CS.scan(sm, ocr, photo_of, box_of, skip, jobs=jobs)


def show(cid):
    spec_map, ocr, photo_of, box_of, skip = load()
    if cid not in spec_map:
        raise SystemExit(f"🔴 {cid} は SPEC に無い")
    g = geom(cid, spec_map, ocr, photo_of, box_of, skip)
    if not g:
        print(f"{cid}: 見ないカット（動画を当てた／写真の割り当てが無い）")
        return 1
    s = spec_map[cid]
    print(f"■ {cid}  {g['name']}  原画 {g['sw']}x{g['sh']}  "
          f"xbias={s.get('xbias', 0.5)} bias={s.get('bias', 0.5)} zoom={s.get('zoom', 1.0)}")
    for k in (0.0, 1.0):
        r = g["rects"][k]
        print(f"   k={k:.0f}  切り出し 原画 x {r['left']:.0f}〜{r['left'] + r['cw']:.0f}"
              f" / y {r['top']:.0f}〜{r['top'] + r['ch']:.0f}  （幅 {r['cw']:.0f}px）")
    print("   ── 画面に入る行（画面座標 x0）")
    for ln in g["lines"]:
        scr = {k: CS.to_screen(ln["box"], g["rects"][k]) for k in (0.0, 1.0)}
        if not any(v[2] > 0 and v[0] < W and v[3] > 0 and v[1] < H for v in scr.values()):
            continue
        f0, f1 = scr[0.0], scr[1.0]
        print(f"     x0 k0={f0[0]:7.0f} k1={f1[0]:7.0f}  y k0={f0[1]:6.0f} "
              f"k1={f1[1]:6.0f}  「{ln['text'][:56]}」")
    hits, softs = one(cid, spec_map, ocr, photo_of, box_of, skip,
                      jobs=CS.jobs_for({cid: spec_map[cid]}))
    print(f"   ── 🔴 {len(hits)}件 ／ ・{len(softs)}件")
    for h in hits:
        print("      🔴", " ".join(str(x)[:58] for x in h[1:4]))
    return 0


def keeps_ok(g, keeps, keepboxes):
    """残したい語・箱が k=0 と k=1 の**両方で丸ごと画面に入って**いるか。"""
    got = {w: False for w in keeps}
    for ln in g["lines"]:
        t = ln["text"].lower()
        for w in keeps:
            if w.lower() not in t:
                continue
            if all(inside(CS.to_screen(ln["box"], g["rects"][k])) for k in (0.0, 1.0)):
                got[w] = True
    for i, b in enumerate(keepboxes):
        got[f"箱{i + 1}"] = all(inside(CS.to_screen(b, g["rects"][k])) for k in (0.0, 1.0))
    return all(got.values()), got


def inside(s):
    return s[0] >= 0 and s[1] >= 0 and s[2] <= W and s[3] <= H


def frange(a, b, step):
    v = a
    while v <= b + 1e-9:
        yield v
        v += step


def solve(cid, keeps, keepboxes, keepvisible, top=1):
    spec_map, ocr, photo_of, box_of, skip = load()
    if cid not in spec_map:
        raise SystemExit(f"🔴 {cid} は SPEC に無い")
    g0 = geom(cid, spec_map, ocr, photo_of, box_of, skip)
    if not g0:
        raise SystemExit(f"🔴 {cid} はスライドが映るカットではない")
    keeps = list(keeps)
    if keepvisible:
        # いま**丸ごと**写っている行を全部残す＝見せている物を落とさずに粗だけ減らす
        for ln in g0["lines"]:
            if len(ln["text"].strip()) < CS.CLIP_CHARS:
                continue
            if all(inside(CS.to_screen(ln["box"], g0["rects"][k])) for k in (0.0, 1.0)):
                keeps.append(ln["text"].strip())
        print(f"   いま丸ごと写っている行 {len(keeps)}本 を残す")
    if not keeps and not keepboxes:
        # 🔴 fail closed：残したい物を言わずに探すと「何も写らない切り方」が満点になる
        raise SystemExit("🔴 --keep か --keepbox か --keepvisible を必ず1つ以上。"
                         "残したい物を言わずに探すと『何も写らない切り方』が満点になる")
    for w in keeps:
        if not any(w.lower() in l["text"].lower() for l in g0["lines"]):
            raise SystemExit(f"🔴 --keep「{w}」に当たる焼き込み行が無い。"
                             f"`show {cid}` で行を見て書き直すか --keepbox で箱を直に指定する")

    jobs = CS.jobs_for(spec_map)
    bx, bb, bz = (spec_map[cid].get("xbias", .5), spec_map[cid].get("bias", .5),
                  spec_map[cid].get("zoom", 1.0))
    best, tried = None, 0
    stages = [([round(v, 3) for v in frange(0, 1, .05)],
               [round(min(1, max(0, bb + d)), 3) for d in frange(-.12, .12, .03)],
               [round(max(1.0, bz + d), 3) for d in frange(-.45, .15, .05)])]
    for stage in range(2):
        if stage == 1:
            if not best:
                break
            cx, cb, cz = best[1]
            stages.append(
                ([round(min(1, max(0, cx + d)), 3) for d in frange(-.09, .09, .015)],
                 [round(min(1, max(0, cb + d)), 3) for d in frange(-.09, .09, .015)],
                 [round(max(1.0, cz + d), 3) for d in frange(-.08, .08, .02)]))
        xs, bs, zs = stages[stage]
        for x, b, z in itertools.product(sorted(set(xs)), sorted(set(bs)), sorted(set(zs))):
            if z < 1.0:
                continue
            ov = dict(xbias=x, bias=b, zoom=z)
            g = geom(cid, spec_map, ocr, photo_of, box_of, skip, ov)
            ok, _ = keeps_ok(g, keeps, keepboxes)
            if not ok:
                continue
            tried += 1
            hits, softs = one(cid, spec_map, ocr, photo_of, box_of, skip, ov, jobs)
            # 粗の数 → 参考の数 → **元からの動きの小ささ**（構図を変えないほうを採る）
            score = (len(hits), len(softs),
                     round(abs(z - bz) * 2 + abs(b - bb) * 3 + abs(x - bx), 4))
            if best is None or score < best[0]:
                best = (score, (x, b, z))
    if not best:
        print(f"{cid}: 条件を満たす切り方が見つかりません"
              f"（--keep が厳しすぎるかも。{tried}通りを試した）")
        return 1
    (nh, ns, _), (x, b, z) = best
    now_h, now_s = one(cid, spec_map, ocr, photo_of, box_of, skip, jobs=jobs)
    print(f"{cid}  → xbias={x}, bias={b}, zoom={z}   🔴{nh}件 ・{ns}件"
          f"   （もと xbias={bx} bias={bb} zoom={bz}＝🔴{len(now_h)}件 ・{len(now_s)}件"
          f"／{tried}通りを試した）")
    print(f"⚠️ このままコミットしない。`python tools/check_slide.py --draw {cid} --boxes` で"
          f" k=0/k=1 を描いて見てから直す")
    return 0


def selftest():
    """物差しの検算。**本番の scan() と本番の SPEC** を通す（作り物を作らない）。"""
    ok = True

    def say(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '🔴'} {msg}")

    spec_map, ocr, photo_of, box_of, skip = load()
    cid = next((c for c in sorted(spec_map)
                if geom(c, spec_map, ocr, photo_of, box_of, skip)), None)
    say(cid is not None, f"試験台にできるカットがある（{cid}）")
    if cid is None:
        return False
    g = geom(cid, spec_map, ocr, photo_of, box_of, skip)

    # 🔴 残したい物を言わないと止まる（何も写らない切り方が満点になるのを防ぐ）
    try:
        solve(cid, [], [], False)
        say(False, "--keep 無しで走ってしまった")
    except SystemExit:
        say(True, "--keep も --keepbox も無ければ止まる")
    # 🔴 素材に無い語を --keep に書いたら止まる（黙って緩めない）
    try:
        solve(cid, ["Xyzzy Plugh"], [], False)
        say(False, "素材に無い --keep で走ってしまった")
    except SystemExit:
        say(True, "素材に無い --keep は止まる")

    # keeps_ok：いまの切り方で丸ごと写っている行は「残っている」と答える
    vis = [l["text"].strip() for l in g["lines"]
           if all(inside(CS.to_screen(l["box"], g["rects"][k])) for k in (0.0, 1.0))]
    if vis:
        say(keeps_ok(g, [vis[0]], [])[0], f"丸ごと写っている行「{vis[0][:22]}」は残ると答える")
    # keeps_ok：原画の外の箱は「残らない」と答える（鳴りすぎの検算）
    far = [g["sw"] + 100, g["sh"] + 100, g["sw"] + 300, g["sh"] + 200]
    say(not keeps_ok(g, [], [far])[0], "原画の外の箱は『残らない』と答える")

    # 🔴 判定が本番と同じ1本を通っているか（scan を直接呼んだ結果と一致するか）
    a = one(cid, spec_map, ocr, photo_of, box_of, skip,
            jobs=CS.jobs_for({cid: spec_map[cid]}))
    b = CS.scan({cid: spec_map[cid]}, ocr, photo_of, box_of, skip,
                jobs=CS.jobs_for({cid: spec_map[cid]}))
    say(a == b, "判定は本番の check_slide.scan() そのもの（別実装を持っていない）")
    print("  " + ("✓ 物差しは正しい" if ok else "🔴 物差しに落ちた"))
    return ok


def main():
    if "--selftest" in sys.argv:
        return 0 if selftest() else 1
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["show", "solve"])
    ap.add_argument("cid")
    ap.add_argument("--keep", action="append", default=[],
                    help="残したい焼き込みの語（何度でも）")
    ap.add_argument("--keepbox", action="append", default=[],
                    help="残したい原画の箱 x0,y0,x1,y1（写真・印など文字でない決め所）")
    ap.add_argument("--keepvisible", action="store_true",
                    help="いま丸ごと写っている行を全部残す")
    a = ap.parse_args()
    if a.cmd == "show":
        return show(a.cid)
    boxes = [[float(v) for v in b.split(",")] for b in a.keepbox]
    return solve(a.cid, a.keep, boxes, a.keepvisible)


if __name__ == "__main__":
    sys.exit(main())
