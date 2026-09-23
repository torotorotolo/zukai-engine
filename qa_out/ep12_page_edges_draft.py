# -*- coding: utf-8 -*-
"""【下書き】頁・写真の切り方（trim）と寄りの窓の辺が、字の行を横／縦に切っていないか（12本目 ⑤c 原寸・2026-09-23）。

⚠️ 2026-09-23（⑤c'）に門番 `tools/check_page_edges.py`（qa_all の `edges`・窓の辺だけを測る・対照は合成）へ移した。
   これは記録として残す。直したので c719・c517 の陽性対照はもう出ない＝回すと exit 2 で止まる（正しい）。

🔴 ⑤c' で `tools/check_page_edges.py`（または check_slide の G-17）の門番へ移して `qa_all` に載せること（ルール §5c-5）。
   ここに置いたのは**チャットをまたいで渡すため**だけ（scratchpad は次のチャットから見えない）。

■ なぜ要るか（台帳 `qa_out/ep12_qa_look1.md` §7-4）
  原寸で c719（表22 の最下行 Utirik が上半分だけ）・c517（図の注 "Figure 65…" が上半分だけ）を見つけた。
  `check_slide.apply_trim()` は窓に半分かかる行を「かかっている分だけ」に**詰めて**残す（本番も半分しか出ないので正しい）。
  ＝「行が切られた」という事実が門番の手前で消える。G-10 は**左端**の語の欠けしか見ない。→ 上下の辺は誰も見ていなかった。

■ 測るもの
  OCR の読み置き（`check_slide.load_ocr()`＝**切る前**の行の箱）を
  ① trim の4辺（`check_slide.trim_of`＝本番の `PHOTO_TRIM` と同じ引き方）
  ② 寄りの窓の4辺（`check_slide.cam_rects`＝build_jiko.fit と同じ式。k=0/1、cam= のカットは頭・中・尻の3点）
  と比べ、行の見えている割合が LO〜HI（8〜92%）なら「切られている」。
  ⚠️ 左右の辺は、地図を横に流すカメラの途中で地名が出入りするのが自然（c519 c520 c710 c814 c815）＝既定では出さない（--sides で出す）

■ 陽性対照（原寸で見たもの）… c719「Utirik」の行（見えている 18〜81%）・c517「Figure 65」の行（60〜80%）が出ること。出なければ物差しが死んでいる
  🔴 ⑤c' で c719・c517 を直すと、この2件は**出なくなるのが正しい**＝この対照は直す前の版でしか使えない。
     門番にするときは、SPEC を細工して行を切らせた**合成の対照**（例：c719 の trim の下端を Utirik の行の中ほどへ）に替える
■ 2026-09-23 の結果（r02 の SPEC）… 上下の辺で 15カット：c321 c403 c418 c517 c519 c520 c615 c706 c710 c719 c720 c721 c722 c814 c815

使い方:
    python qa_out/ep12_page_edges_draft.py            # 上下の辺（trim と寄りの窓）
    python qa_out/ep12_page_edges_draft.py --sides    # 左右の辺も
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import check_slide as CS  # noqa: E402
import scene_jiko as S  # noqa: E402

LO, HI = 0.08, 0.92
POSITIVE = {"c719": "Utirik", "c517": "24 hours after"}


def frac_in(a0, a1, e, inside_is_high):
    """[a0,a1] を位置 e で切ったとき、窓の内側に残る割合。"""
    f = (a1 - e) / max(a1 - a0, 1e-6)
    return f if inside_is_high else 1 - f


def scan(sides=False):
    ocr = CS.load_ocr()
    spec_map, photo_of, box_of, skip = CS.production_inputs()
    rows = []
    for cid in S.ORDER:
        if cid in skip or cid not in photo_of:
            continue
        spec = spec_map.get(cid) or {}
        o = ocr.get(Path(photo_of[cid]).name)
        if not o:
            continue
        sw, sh = o["size"]
        raw = o["lines"]
        tr = CS.trim_of(spec)
        X0, Y0, X1, Y1 = 0, 0, sw, sh
        if tr:
            X0, Y0, X1, Y1 = round(tr[0] * sw), round(tr[1] * sh), round(tr[2] * sw), round(tr[3] * sh)
        live = [ln for ln in raw if not (ln["box"][2] <= X0 or ln["box"][0] >= X1
                                         or ln["box"][3] <= Y0 or ln["box"][1] >= Y1)]
        if tr:
            for ln in live:
                b = ln["box"]
                edges = [("trim上", frac_in(b[1], b[3], Y0, True)), ("trim下", frac_in(b[1], b[3], Y1, False))]
                if sides:
                    edges += [("trim左", frac_in(b[0], b[2], X0, True)), ("trim右", frac_in(b[0], b[2], X1, False))]
                for edge, f in edges:
                    if LO < f < HI:
                        rows.append((cid, edge, f, ln["text"], b[3] - b[1]))
        # 寄りの窓は trim のあとの座標で（apply_trim は詰めるので使わず、切る前の箱をずらす）
        tw, th = X1 - X0, Y1 - Y0
        moved = [dict(ln, box=[ln["box"][0] - X0, ln["box"][1] - Y0, ln["box"][2] - X0, ln["box"][3] - Y0])
                 for ln in live]
        for k, r in CS.cam_rects(tw, th, box_of[cid], spec).items():
            L, T, R, B = r["left"], r["top"], r["left"] + r["cw"], r["top"] + r["ch"]
            sy = r["h"] / r["ch"]
            for ln in moved:
                b = ln["box"]
                if b[2] <= L or b[0] >= R or b[3] <= T or b[1] >= B:
                    continue
                edges = [(f"窓上 k{k:g}", frac_in(b[1], b[3], T, True)), (f"窓下 k{k:g}", frac_in(b[1], b[3], B, False))]
                if sides:
                    edges += [(f"窓左 k{k:g}", frac_in(b[0], b[2], L, True)), (f"窓右 k{k:g}", frac_in(b[0], b[2], R, False))]
                for edge, f in edges:
                    if LO < f < HI:
                        rows.append((cid, edge, f, ln["text"], round((b[3] - b[1]) * sy)))
    return rows


def main():
    sides = "--sides" in sys.argv
    rows = scan(sides)
    cuts = sorted({r[0] for r in rows}, key=S.ORDER.index)
    print(f"■ 字の行が辺で切られている（見えている {LO:.0%}〜{HI:.0%}）… {len(rows)} 行 ／ {len(cuts)} カット")
    for cid in cuts:
        rs = sorted((r for r in rows if r[0] == cid), key=lambda r: r[2])
        worst = rs[0]
        print(f"  {cid} 最悪 {worst[2]:.0%}（{worst[1]}・高さ {worst[4]}px）「{worst[3][:40]}」 ほか {len(rs) - 1} 行")
    ok = True
    for cid, word in POSITIVE.items():
        hit = any(r[0] == cid and word in r[3] for r in rows)
        print(f"  {'✓' if hit else '🔴'} 陽性対照 {cid}「{word}」")
        ok &= hit
    print("✓ 物差しは生きている" if ok else "🔴 陽性対照が出ない＝物差しか OCR の読み置きが変わった。本番に当てるな")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
