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

■ 🆕 2026-10-27（26本目 ⑤b-1）：**額装の写真は静止**（10-26 カズヤくん＝25本目の試写「ただ写真が揺れる演出は、ぶれているだけで見づらいので
   静止してください。次回から」・記憶 feedback-jiko-framed-photo-no-shake）。回の既定 `build_jiko.FRAME_STILL`（26本目から True）の回は、
    5. 🔴 SPEC に `fmove`（額ごと動かす）を書いたカットを止める（書き方の網）
    6. 🔴 **絵で測る**（記憶 feedback-settings-may-not-reach-the-picture＝SPEC の字面だけを見ない）＝額装・帯の写真のカット（写真だけ・図の地に敷かない・
       箱が全画面でない＝`build_jiko.framed`）ごとに、本物の `build_jiko.scene()` を尺の 25% と 95% の2つの時刻で回し、画面の画素が1つでも変われば止める
       （額ごと動く・額の中で寄る・cam で流す、のどれでも鳴る）。地（`{cid}_bg`）と文字の層（`{cid}_lab`）は空の層にする＝動くのは写真と額だけ
       （見出しのフェードを数えない）。映像を当てたカット（footage.USE）は映像そのものが動く＝測らない（名を出す）。
       全画面の写真のゆっくり寄る・流す（k・cam）は続ける（了承② 決め3）＝測らない。
       ⚠️ 尻の差し込み（tail）の額は selftest で型（`tail_frame` の k）を絵で測る。本番の差し込みは `layer_index` を組まないと箱が出ない＝件数だけ出す（本番の絵は測っていない）
   25本目までの回（FRAME_STILL＝False）は 5・6 を回さない（公開ずみ＝直さない）。

■ 使い方
    python tools/check_fmove.py             # 本番の SPEC
    python tools/check_fmove.py --selftest  # 陽性対照（見出し・出典と字幕の帯・画面の外・書き方・🆕 額装の静止）＋陰性対照
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


# ── 🆕 26本目 ⑤b-1：額装の写真は静止（絵で測る） ─────────────────
STILL_AT = (0.25, 0.95)          # 尺のこの2つの割合の時刻で scene() を回して比べる（頭の 0.15〜0.65秒の見出しのフェードは文字の層＝空にしてある）


def _blank_lay(S, cid, names=("bg", "lab")):
    from PIL import Image
    out = {}
    for n in names:
        out[f"{cid}_{n}"] = Image.new("RGBA", (S.W, S.H), (0, 0, 0, 255 if n in ("bg", "tbg") else 0))
    return out


def frame_diff(S, B, cid, meta_c, src, dur):
    """本物の `build_jiko.scene()` を2つの時刻で回した画面の差＝(変わった画素の数, 差の最大)。meta_c は build_jiko.meta_of の1カットぶんの形"""
    import numpy as np
    lay = _blank_lay(S, cid)
    miss = cid in B._FOOT_MISS
    B._FOOT_MISS.add(cid)        # 🔴 out/jiko/foot/<cid>/ に前の回のコマが残っていても読まない＝写真を測る（映像のカットは呼ぶ側で外す）
    try:
        fr = [np.asarray(B.scene(cid, a * dur, dur, lay, {cid: src}, {cid: meta_c}).convert("RGB"), dtype=np.int16) for a in STILL_AT]
    finally:
        if not miss:
            B._FOOT_MISS.discard(cid)
    d = np.abs(fr[0] - fr[1]).max(axis=2)
    return int((d > 0).sum()), int(d.max())


def tail_diff(S, B, cid, meta_c, dur):
    """尻の差し込みの1コマ（`build_jiko.tail_frame`）を差し込みの出た後の2つの時刻で回した差＝(変わった画素の数, 差の最大)"""
    import numpy as np
    lay = _blank_lay(S, cid, ("tbg", "tlab"))
    a = float(meta_c["tail"]["sec"])
    ts = [a + (dur - a) * u for u in STILL_AT]
    fr = [np.asarray(B.tail_frame(cid, t, dur, lay, {cid: meta_c}).convert("RGB"), dtype=np.int16) for t in ts]
    d = np.abs(fr[0] - fr[1]).max(axis=2)
    return int((d > 0).sum()), int(d.max())


def run_still(S):
    """26本目からの回：SPEC の fmove を止める（5）・額装・帯の写真を本物の scene() で2つの時刻に回して画素が変われば止める（6）。(🔴 の数, 測ったカットの数)"""
    import build_jiko as B
    import footage as FO
    import el_script
    if not B.FRAME_STILL:
        print(f"■ 額装の静止：この回（{el_script.SLUG}）は FRAME_STILL＝False（25本目までの回）＝測らない")
        return 0, 0
    bad = [(cid, "SPEC に fmove（額ごと動かす）＝26本目からは額装は静止（fmove を消す）") for cid, s in sorted(S.SPEC.items()) if s.get("fmove")]
    items, vids = [], []
    for cid, (box, photo, bias) in sorted(S.PHOTO_CUTS.items()):
        s = S.SPEC.get(cid) or {}
        if s.get("fig") or s.get("illu") or not B.framed(box):
            continue
        (vids if cid in FO.USE else items).append(cid)
    tails = sorted(c for c, s in S.SPEC.items() if s.get("tail") and not (s["tail"] or {}).get("full"))
    print(f"■ 額装の静止（{el_script.SLUG}・FRAME_STILL）：SPEC の fmove {len(bad)} 欄・額装と帯の写真 {len(items)} カットを本物の scene() で"
          f"{STILL_AT[0]:.0%} と {STILL_AT[1]:.0%} の時刻に回して比べる（映像を当てた額 {len(vids)}＝測らない{'：' + '・'.join(vids) if vids else ''}）")
    if tails:
        print(f"  ⚠️ 尻の差し込みの額 {len(tails)} 欄（{'・'.join(tails[:12])}）＝本番の絵は測っていない（型は selftest で測った）")
    if items:
        idx = {cid: dict(photo=True, back=False, veil=None, pveil=None, span=None, stages=0, holds=[]) for cid in items}
        meta = B.meta_of(idx)
        secs = dict(S.CUTS)
        for cid in items:
            box, photo, _ = S.PHOTO_CUTS[cid]
            src = B.load_photo(photo, box, S.PHOTO_TRIM.get(cid), S.PHOTO_LEVELS.get(cid))
            dur = max(1.0, secs.get(cid, 8.0) - S.card_of(cid))
            n, mx = frame_diff(S, B, cid, meta[cid], src, dur)
            if n:
                why = [k for k in ("fmove", "cam") if meta[cid].get(k)] or ["額の中の寄り（k）"]
                bad.append((cid, f"額装の写真が動く＝{dur * STILL_AT[0]:.1f}秒と {dur * STILL_AT[1]:.1f}秒で {n:,} 画素が変わる（差の最大 {mx}・"
                                 f"見込みの元＝{'・'.join(why)}）"))
            else:
                print(f"  ✓ {cid}  静止（変わった画素 0）")
    for cid, why in bad:
        print(f"  🔴 {cid}：{why}")
    if bad:
        print(f"🔴 額装の静止を外れる所 {len(bad)} か所（exit 1）")
    elif not items:
        print("⚠️ 額装の静止：額装と帯の写真が0カット＝測っていない（章ファイルに写真をまだ書いていない回なら正しい・"
              "書いたのに0なら PHOTO_CUTS を読めていない＝0件を調べて合格にしない）")
    else:
        print(f"✓ 額装の静止：fmove 0・額装と帯の写真 {len(items)} カットとも画素が変わらない")
    return len(bad), len(items)


def run():
    import scene_jiko as S
    import check_layout as L
    nstill, _ = run_still(S)
    items = [(cid, s) for cid, s in sorted(S.SPEC.items()) if s.get("fmove")]
    print(f"■ 額ごと動かすカット {len(items)} 欄（SPEC の fmove）を、頭・真ん中・終わりの額の箱で測る")
    if not items:
        print("⚠️ 0欄＝この回は額ごと動かすカットが無い（あるはずの回なら章ファイルを読めていない）")
        return 1 if nstill else 0
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
    return 1 if nstill else 0


def selftest_still(S, L, base):
    """🆕 26本目 ⑤b-1：額装の静止の門番（6）が**絵で**鳴るか。本物の scene()・tail_frame() に、本物の写真（base の photo）と1カットぶんの meta を渡す。
    FRAME_STILL を True／False に差し替えて回し、終わったら必ず戻す（try/finally）。"""
    import build_jiko as B
    import importlib
    ss = importlib.import_module("cuts.ss")
    ok = True

    def chk(what, cond):
        nonlocal ok
        print(f"  {'✓' if cond else '🔴'} {what}")
        ok &= bool(cond)

    cid = "cz91"                 # どの回にも無いカットID（out/jiko/foot に前の回のコマが残っていても当たらない）
    box = S.photo_box(base)
    full = S.PHOTO_FULL
    keep = (B.FRAME_STILL, S.PHOTO_CUTS.get(cid), S.PHOTO_CROP.get(cid))

    def meta(**kw):
        m = dict(photo=True, back=False, veil=None, pveil=None, span=None, labk=0.3, held=[], mute=[], color=1.0, times=[], pal="navy",
                 card=0, tail_black=False, flash=None, cam=None, fmove=None, ground=None, moves=[], intro=None, hl=None, illu=None, tail=None,
                 frame_only=False, still=False)
        m.update(kw)
        return m

    def case(b, **kw):
        S.PHOTO_CUTS[cid] = (b, base["photo"], 0.5)
        S.PHOTO_CROP[cid] = (0.5, 1.0)
        src = B.load_photo(base["photo"], b)
        return frame_diff(S, B, cid, meta(**kw), src, 8.0)

    try:
        chk(f"額装の箱は全画面でない（{box}）＝framed", B.framed(box) and not B.framed(full))
        B.FRAME_STILL = True
        n, mx = case(box)
        chk(f"陰性対照：FRAME_STILL・額装・書きなし → 静止（変わった画素 {n}）", n == 0)
        n, mx = case(box, fmove=ss.fm("in"))
        chk(f"陽性：額装に fmove=ss.fm('in')（額ごと寄る）→ 動く（{n:,} 画素・差の最大 {mx}）", n > 0)
        n, mx = case(box, fmove=ss.fm("r"))
        chk(f"陽性：額装に fmove=ss.fm('r')（額ごと右へ流す）→ 動く（{n:,} 画素）", n > 0)
        n, mx = case(box, cam="pan_r")
        chk(f"陽性：額装に cam='pan_r'（額の中を流す）→ 動く（{n:,} 画素）", n > 0)
        n, mx = case(full)
        chk(f"陰性の確かめ：全画面の写真は FRAME_STILL でも寄る（{n:,} 画素＝全画面のゆっくり寄るは続ける・門番は測らない）", n > 0)
        B.FRAME_STILL = False
        n, mx = case(box)
        chk(f"陽性：25本目までの回（FRAME_STILL＝False）の額装・書きなし → 額の中で寄る（{n:,} 画素＝物差しは既定の寄りも拾う）", n > 0)
        # 尻の差し込みの額（tail_frame の k）
        tl = dict(photo=base["photo"], box=list(box), sec=2.0, full=False)
        B.FRAME_STILL = True
        nt, _ = tail_diff(S, B, cid, meta(tail=tl), 8.0)
        chk(f"陰性対照：FRAME_STILL・尻の差し込みの額 → 静止（変わった画素 {nt}）", nt == 0)
        B.FRAME_STILL = False
        nt, _ = tail_diff(S, B, cid, meta(tail=tl), 8.0)
        chk(f"陽性：FRAME_STILL＝False の尻の差し込みの額 → 寄る（{nt:,} 画素）", nt > 0)
        B.FRAME_STILL = True
        nt, _ = tail_diff(S, B, cid, meta(tail=dict(tl, still=True)), 8.0)
        chk(f"陰性対照：尻の差し込みに still=True → 静止（{nt}）", nt == 0)
    finally:
        B.FRAME_STILL = keep[0]
        for d, v in ((S.PHOTO_CUTS, keep[1]), (S.PHOTO_CROP, keep[2])):
            if v is None:
                d.pop(cid, None)
            else:
                d[cid] = v
    return ok


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
    # 🆕 26本目 ⑤b-1：額装の静止（絵で測る）
    print("■ 額装の静止（本物の scene()・tail_frame() で2つの時刻を比べる）")
    ok &= selftest_still(S, L, base)
    print("✓ selftest 合格" if ok else "🔴 selftest 不合格")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv[1:] else run())
