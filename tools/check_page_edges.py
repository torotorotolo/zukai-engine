# -*- coding: utf-8 -*-
"""頁・写真の**画面に出る辺**（寄りの窓の上下）が、焼き込みの字の行を横に切っていないか（qa_all の `edges`）。

2026-09-23（12本目 ⑤c'）に `qa_out/ep12_page_edges_draft.py`（⑤c 原寸で書いた下書き）から門番にした（ルール §5c-20）。

■ なぜ要るか（台帳 `qa_out/ep12_qa_look1.md` §7-4・§8）
  原寸で c719（表22 の最下行 Utirik が上半分だけ）・c517（図の注 "Figure 65…" が上半分だけ）を見つけ、
  式にして全数へ当てたら **15カット**あった。どの門番も鳴っていなかった：
  `check_slide.apply_trim()` は窓に半分かかる行を「かかっている分だけ」に**詰めて**残す（本番も半分しか
  出ないので、それ自体は正しい）＝「行が切られた」という事実が門番の手前で消える。G-10 は**左端**の語の欠けだけ。

■ 測るもの
  OCR の読み置き（`check_slide.load_ocr()`＝**切る前**の行の箱）を trim のあとの座標へずらし、
  寄りの窓（`check_slide.cam_rects`＝build_jiko.fit と同じ式。k=0/1、`cam=` のカットは頭・中・尻の3点）の
  **上下の辺**と比べる。行の見えている割合が LO〜HI（8〜92%）なら「切られている」。
  ⚠️ **trim の辺そのものは測らない**＝画面に出るのは窓の辺だけ（窓の辺が trim の辺に重なるときは窓の側で拾う）。
     下書きは trim の辺も測って **c519 で空振り**した（trim の下の辺が図の注を切るが、窓は y0.497 までしか下りない）。
  ⚠️ 左右の辺は既定で見ない（地図を横に流すカメラの途中で地名が出入りするのは自然）＝ `--sides` で出す。

■ 陽性対照は**合成**（題材が替わっても当たる）
  原寸で見つけた c719・c517 は直したので、もう出ない（出ないのが正しい）。カット番号を対照に書くと、
  次の題材では別のカットになって門番が必ず止まる（[[feedback-per-episode-constants-go-stale]]）。
  → 本番の頁のカット（`panel`）から**いちばん幅の広い字の行**を選び、SPEC を細工してその場で作る：
     陽性① trim の下の辺をその行の真ん中へ（bias 1.0＝窓の下の辺＝trim の下の辺）→ 窓下で出る
     陽性② trim の上の辺をその行の真ん中へ（bias 0.0）→ 窓上で出る
     陰性  trim の下の辺をその行の下端の 2px 下へ → その行は出ない（境目の式が逆向きでないこと）
  対照が1つでも外れたら、本番に当てずに止まる（exit 2）。

■ 12本目の実績：直す前 15カット → 直したあと 0。c719 は頁の走査の傾き（1.106°）を直してから切った
  （`qa_out/ep12_assets.py` の DESKEW）。**傾いた表は、行間が横に通らない＝どの高さで切っても升目が欠ける。**

使い方:
    python tools/check_page_edges.py             # 本番（qa_all の edges）
    python tools/check_page_edges.py --sides     # 左右の辺も（参考・exit は上下だけで決める）
    python tools/check_page_edges.py --selftest  # 合成の対照だけ
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import check_slide as CS  # noqa: E402
import scene_jiko as S  # noqa: E402

LO, HI = 0.08, 0.92


def frac_in(a0, a1, e, inside_is_high):
    """[a0,a1] を位置 e で切ったとき、窓の内側に残る割合。"""
    f = (a1 - e) / max(a1 - a0, 1e-6)
    return f if inside_is_high else 1 - f


def cut_rows(cid, spec, ocr, photo_of, box_of, sides=False):
    """1カットぶん (cid, 辺, 見えている割合, 行の字, 画面での高さpx, 切る前の箱)。🔴 本番も対照もここを通る。"""
    o = ocr.get(Path(photo_of[cid]).name)
    if not o:
        return []
    sw, sh = o["size"]
    tr = CS.trim_of(spec)
    X0, Y0, X1, Y1 = 0, 0, sw, sh
    if tr:
        X0, Y0, X1, Y1 = round(tr[0] * sw), round(tr[1] * sh), round(tr[2] * sw), round(tr[3] * sh)
    # 切る前の箱を trim のあとの座標へずらす（apply_trim は半分かかる行を詰めてしまうので使わない）
    moved = [(ln, [ln["box"][0] - X0, ln["box"][1] - Y0, ln["box"][2] - X0, ln["box"][3] - Y0])
             for ln in o["lines"]
             if not (ln["box"][2] <= X0 or ln["box"][0] >= X1 or ln["box"][3] <= Y0 or ln["box"][1] >= Y1)]
    rows = []
    for k, r in CS.cam_rects(X1 - X0, Y1 - Y0, box_of[cid], spec).items():
        L, T, R, B = r["left"], r["top"], r["left"] + r["cw"], r["top"] + r["ch"]
        sy = r["h"] / r["ch"]
        for ln, b in moved:
            if b[2] <= L or b[0] >= R or b[3] <= T or b[1] >= B:
                continue
            edges = [(f"窓上 k{k:g}", frac_in(b[1], b[3], T, True)),
                     (f"窓下 k{k:g}", frac_in(b[1], b[3], B, False))]
            if sides:
                edges += [(f"窓左 k{k:g}", frac_in(b[0], b[2], L, True)),
                          (f"窓右 k{k:g}", frac_in(b[0], b[2], R, False))]
            for edge, f in edges:
                if LO < f < HI:
                    rows.append((cid, edge, f, ln["text"], round((b[3] - b[1]) * sy), ln["box"]))
    return rows


def scan(spec_map, ocr, photo_of, box_of, skip, sides=False):
    rows = []
    for cid in S.ORDER:
        if cid in skip or cid not in photo_of:
            continue
        rows += cut_rows(cid, spec_map.get(cid) or {}, ocr, photo_of, box_of, sides)
    return rows


def pick_control(spec_map, ocr, photo_of, box_of, skip):
    """合成の対照に使う (カット, SPEC, 行)。本番の頁のカットのうち、trim の内側でいちばん幅の広い字の行。"""
    best = None
    for cid in S.ORDER:
        spec = spec_map.get(cid) or {}
        if cid in skip or cid not in photo_of or not spec.get("panel"):
            continue
        o = ocr.get(Path(photo_of[cid]).name)
        if not o:
            continue
        sw, sh = o["size"]
        tr = CS.trim_of(spec) or (0.0, 0.0, 1.0, 1.0)
        for ln in o["lines"]:
            b = ln["box"]
            if (b[0] >= tr[0] * sw and b[2] <= tr[2] * sw and b[1] > tr[1] * sh + 4 and b[3] < tr[3] * sh - 4
                    and b[3] - b[1] >= 8 and (best is None or b[2] - b[0] > best[3])):
                best = (cid, spec, ln, b[2] - b[0], tr, sh)
    return best


def selftest(spec_map, ocr, photo_of, box_of, skip):
    got = pick_control(spec_map, ocr, photo_of, box_of, skip)
    if not got:
        print("  🔴 対照に使える頁のカットが無い（panel の頁に OCR の行が1つも無い）＝物差しを確かめられない")
        return False
    cid, spec, ln, _w, tr, sh = got
    b = ln["box"]
    mid = (b[1] + b[3]) / 2 / sh
    base = dict(spec, cam=None)
    cases = [("陽性① 下の辺を行の真ん中へ", dict(base, trim=(tr[0], tr[1], tr[2], mid), bias=1.0), "窓下", True),
             ("陽性② 上の辺を行の真ん中へ", dict(base, trim=(tr[0], mid, tr[2], tr[3]), bias=0.0), "窓上", True),
             ("陰性  下の辺を行の2px下へ", dict(base, trim=(tr[0], tr[1], tr[2], (b[3] + 2) / sh), bias=1.0), "窓下",
              False)]
    ok = True
    print(f"  対照の行：{cid}「{ln['text'][:40]}」（箱 {b}）")
    for name, sp, edge, want in cases:
        hit = [r for r in cut_rows(cid, sp, ocr, photo_of, box_of) if r[5] is b and r[1].startswith(edge)]
        good = bool(hit) == want
        seen = f"{hit[0][2]:.0%} で出た" if hit else "出ない"
        print(f"  {'✓' if good else '🔴'} {name} → {seen}（{'出るはず' if want else '出ないはず'}）")
        ok &= good
    return ok


def main():
    sides = "--sides" in sys.argv
    ocr = CS.load_ocr()
    spec_map, photo_of, box_of, skip = CS.production_inputs()
    print("■ 物差しの検算（合成の対照）")
    if not selftest(spec_map, ocr, photo_of, box_of, skip):
        print("🔴 対照が外れた＝物差しか OCR の読み置きが変わった。本番に当てずに止める")
        return 2
    if "--selftest" in sys.argv:
        print("✓ 物差しは正しい")
        return 0
    rows = scan(spec_map, ocr, photo_of, box_of, skip, sides)
    hard = [r for r in rows if r[1][:2] in ("窓上", "窓下")]
    cuts = sorted({r[0] for r in rows}, key=S.ORDER.index)
    print(f"■ 画面に出る辺が字の行を切っている（見えている {LO:.0%}〜{HI:.0%}）… {len(rows)} 行 ／ {len(cuts)} カット"
          f"{'（左右の辺も）' if sides else ''}")
    for cid in cuts:
        rs = sorted((r for r in rows if r[0] == cid), key=lambda r: r[2])
        w = rs[0]
        mark = "🔴" if any(r[0] == cid for r in hard) else "  ・"
        print(f"{mark} {cid} 最悪 {w[2]:.0%}（{w[1]}・高さ {w[4]}px）「{w[3][:40]}」 ほか {len(rs) - 1} 行")
    if hard:
        print("   → trim の上下を行間へ寄せる／図の注・題は副題が名乗るので外す／寄りの終わりで出ていく行は bias で残すか外す"
              "（台帳の例＝`qa_out/ep12_qa_look1.md` §8）。傾いた走査は先に傾きを直す")
        return 1
    print("✓ 画面に出る上下の辺で切られている字の行は 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
