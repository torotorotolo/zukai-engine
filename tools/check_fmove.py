# -*- coding: utf-8 -*-
"""check_fmove.py — **額ごと動かす**カット（SPEC の `fmove`）の額の箱が、尺の頭・真ん中・終わりで
画面の外・見出し・章の札・出典・注記・字幕の帯にかからないか（2026-10-08・20本目 ⑤b-2 新設）。

■ なぜ要るか
    額装の写真は額の箱が動かない前提で、見出し・出典・字幕の帯との重なりを門番 layout が**止まった箱**で測っていた。
    `fmove`（`scene_jiko.fmove_at`）は額の箱そのものを動かす＝止まった箱で測る門番は、動いた先の重なりを見ない
    （測る線の向きの穴＝記憶 feedback-gates-blind-spot-is-the-scan-direction）。
    箱の各辺は緩急をかけた u の1次式＝いちばん外へ出るのは頭か終わり（真ん中も念のため測る）。

■ 測るもの（文字の箱は `check_layout.boxes`＝書体の実測・額の箱は縁の太さ 3px の外まで）
    1. 画面の外（0〜1920 × 0〜1080）
    2. 字幕の帯（y ≥ scene_jiko.SUB_Y）
    3. そのカットの `_lab` の文字（見出し・副題・章の札・出典・注記）と GAP px 未満に近づく
    4. 書き方：額装（panel=True）でない・額の中の寄せ／カメラ／頁の印／差し込みと一緒に書いた（cam・hl・zoom≠1・intro・tail・band）

■ 使い方
    python tools/check_fmove.py             # 本番の SPEC
    python tools/check_fmove.py --selftest  # 陽性対照（見出し・出典と字幕の帯・画面の外・書き方）＋陰性対照
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

GAP = 4          # 額の縁の外と文字の箱のあいだに残す px（縁の外の 1.5px は箱に含める）
US = (0.0, 0.5, 1.0)
BAD_WITH = ("cam", "hl", "intro", "tail", "band")


def frame_rects(S, spec):
    base = S.photo_box(spec)
    out = []
    for u in US:
        x, y, w, h = S.fmove_at(base, spec["fmove"], u)
        e = S.FRAME_SW * 1.5
        out.append((u, (x - e, y - e, x + w + e, y + h + e)))
    return out


def judge(S, L, cid, spec):
    """(🔴の理由の並び, 測った額の箱の数)"""
    bad = []
    if not spec.get("panel"):
        bad.append("panel=True が無い（全画面の写真は額が無い＝額ごと動かせない）")
        return bad, 0
    for k in BAD_WITH:
        if spec.get(k):
            bad.append(f"{k} と一緒に書いている（額ごと動かすカットは額の中を動かさない・差し込みと混ぜない）")
    if float(spec.get("zoom") or 1.0) != 1.0:
        bad.append(f"zoom={spec.get('zoom')}（額の中の寄せ＝絵を切る）")
    svg = S.full_top(cid, spec) + "".join(S.photo_ann(spec, cid)) if spec.get("ann") else S.full_top(cid, spec)
    texts = [b for b in L.boxes(svg, f"{cid}_lab")]
    n = 0
    for u, (x0, y0, x1, y1) in frame_rects(S, spec):
        n += 1
        if x0 < 0 or y0 < 0 or x1 > S.W or y1 > S.H:
            bad.append(f"u={u}：額の箱 ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) が画面の外へ出る")
        if y1 > S.SUB_Y - GAP:
            bad.append(f"u={u}：額の下の辺 y{y1:.0f} が字幕の帯（y{S.SUB_Y}〜）に {y1 - (S.SUB_Y - GAP):.0f}px かかる")
        for tx0, ty0, tx1, ty1, t, *_ in texts:
            if x0 < tx1 + GAP and tx0 < x1 + GAP and y0 < ty1 + GAP and ty0 < y1 + GAP:
                bad.append(f"u={u}：額の箱 ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) が文字「{t[:24]}」"
                           f"({tx0:.0f},{ty0:.0f})-({tx1:.0f},{ty1:.0f}) に {GAP}px より近い")
    return bad, n


def run():
    import scene_jiko as S
    import check_layout as L
    items = [(cid, s) for cid, s in sorted(S.SPEC.items()) if s.get("fmove")]
    print(f"■ 額ごと動かすカット {len(items)} 欄（SPEC の fmove）を、頭・真ん中・終わりの額の箱で測る")
    if not items:
        print("⚠️ 0欄＝この回は額ごと動かすカットが無い（あるはずの回なら章ファイルを読めていない）")
        return 0
    hits, n = [], 0
    for cid, s in items:
        b, k = judge(S, L, cid, s)
        n += k
        hits += [(cid, x) for x in b]
        if not b:
            (x0, y0, x1, y1) = frame_rects(S, s)[0][1]
            (a0, b0, a1, b1) = frame_rects(S, s)[-1][1]
            print(f"  ✓ {cid}  頭 ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) → 終わり ({a0:.0f},{b0:.0f})-({a1:.0f},{b1:.0f})")
    for cid, why in hits:
        print(f"  🔴 {cid}：{why}")
    if hits:
        print(f"🔴 額ごと動かす額が {len(hits)} か所でかかる（exit 1）")
        return 1
    print(f"✓ {len(items)} 欄・額の箱 {n} 個とも、画面の内・字幕の帯の上・文字から {GAP}px 以上")
    return 0


def selftest():
    import scene_jiko as S
    import check_layout as L
    import json
    ok = True

    def chk(what, cond):
        nonlocal ok
        print(f"  {'✓' if cond else '🔴'} {what}")
        ok &= bool(cond)

    # 束の写真を1点借りる（credits.json に出典がある点）＝実物の箱の大きさで測る
    cj = json.loads((S.HERE / "ref" / "ep20" / "credits.json").read_text(encoding="utf-8"))
    photo = next(k for k in cj if k.endswith("p015.jpg"))
    base = dict(photo=photo, panel=True, t="回収された垂直尾翼の一部", s="相模湾（事故のあと）")
    cases = [
        ("陰性対照：寄る（0.90→1.00）", dict(base, fmove=dict(frm=(0, 0, 0.9), to=(0, 0, 1.0))), False),
        ("陰性対照：右へ流す ±80px", dict(base, fmove=dict(frm=(-80, 0, 1.0), to=(80, 0, 1.0))), False),
        ("陽性：上へ 150px＝見出しの副題にかかる", dict(base, fmove=dict(frm=(0, 0, 1.0), to=(0, -150, 1.0))), True),
        ("陽性：下へ 40px＝出典の行にかかる", dict(base, fmove=dict(frm=(0, 0, 1.0), to=(0, 40, 1.0))), True),
        ("陽性：下へ 90px＝字幕の帯にかかる", dict(base, fmove=dict(frm=(0, 0, 1.0), to=(0, 90, 1.0))), True),
        ("陽性：右へ 700px＝画面の外", dict(base, fmove=dict(frm=(0, 0, 1.0), to=(700, 0, 1.0))), True),
        ("陽性：大きさ 1.25＝上下にはみ出す", dict(base, fmove=dict(frm=(0, 0, 1.0), to=(0, 0, 1.25))), True),
        ("陽性：panel なし", {k: v for k, v in dict(base, fmove=dict(frm=(0, 0, 0.9), to=(0, 0, 1.0))).items()
                            if k != "panel"}, True),
        ("陽性：cam と一緒", dict(base, cam="pan_r", fmove=dict(frm=(0, 0, 0.9), to=(0, 0, 1.0))), True),
    ]
    for what, spec, want in cases:
        b, _ = judge(S, L, "c102", spec)
        chk(f"{what} → {'鳴る' if want else '鳴らない'}（{len(b)}件{'：' + b[0][:60] if b else ''}）", bool(b) == want)
    # 見出しの副題の箱が本当に拾えているか（物差しの確かめ＝文字の箱が0なら 3 は空の合格）
    tb = L.boxes(S.full_top("c102", base), "c102_lab")
    chk(f"文字の箱を拾えている（{len(tb)}個＝見出し・副題・出典・章の札）", len(tb) >= 3)
    # ss.fm の6つの型が本物の箱で通る（書き方の見本が門番に止められない）
    import importlib
    ss = importlib.import_module("cuts.ss")
    for k in ("in", "out", "r", "l", "u", "d"):
        b, _ = judge(S, L, "c102", dict(base, fmove=ss.fm(k)))
        chk(f"ss.fm('{k}') は通る（{len(b)}件）", not b)
    print("✓ selftest 合格" if ok else "🔴 selftest 不合格")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else run())
