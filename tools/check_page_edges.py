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
# 🔴🔴 2026-09-25（13本目 ⑤c'）：**寄りの両端（k=0/1）だけ測っていたので、途中で辺が行を横切るのを見なかった。**
#    c520 の最下行「SAFETY RECOMMENDATIONS…」は k=0 で 97% 見え・k=1 で 6%（ほぼ外）＝両端ではどちらも
#    「切れていない」なのに、**尺の途中はずっと半分に切れて見える**（⑤c-2 の原寸で🔴＝検品画像は途中の瞬間）。
#    → `cam=` の無いカットは寄りの間を K_STEPS 点に刻んで測る（辺は1コマに高さの 0.26% しか動かない＝
#       高さ 10px 以上の行を刻みの間で飛ばさない）。`cam=` のカットは今までどおり経路の3点。
K_STEPS = 21
# 画面での高さがこれ未満の「行」は字として読めない＝測らない（参考に出す）。OCR が模様を字と読んだ幻を含む
#   （13本目 c102 の森の破片「ゞ ツ レ」＝画面 8px）。本物の頁の行は画面 19〜39px（⑤c' の実測）
MIN_H_PX = 10


def rects_of(sw, sh, box, spec):
    """測る窓 {k: 窓}。`cam=` のカットは経路の3点（check_slide.cam_rects）、それ以外は寄りを K_STEPS 点に刻む。"""
    if spec.get("cam") or spec.get("fmove"):
        # 🆕 20本目 ⑤c'：額ごと動かす（fmove）も check_slide.cam_rects へ＝絵を切らない（本番 build_jiko と同じ）
        return CS.cam_rects(sw, sh, box, spec)
    b, xb, zm = (float(spec.get("bias", 0.5)), float(spec.get("xbias", 0.5)), float(spec.get("zoom", 1.0)))
    import build_jiko as B
    # 🆕 2026-10-28（26本目 ⑤b-7）：回の既定 FRAME_STILL（26本目から）の**額装・帯の写真は寄らない**（本番 build_jiko の kb＝0・`framed(box)`）
    #    ＝寄りの始めの1点だけ。寄る前提で21点に刻むと、静止の頁の切り口の辺が k＝1 の窓で隣の行を切ると鳴った（c809 ほか＝本番の絵では切れない）
    # 🆕 27本目 ⑤b-4：説明カットの地の写真（dim）も動かさない（build_jiko.scene の dim の枝＝fit の k=0）＝1点だけ
    if spec.get("still") or spec.get("sat") or (B.FRAME_STILL and B.framed(box)) or (spec.get("dim") and spec.get("fig")):
        # 🆕 19本目 ⑤b-7c：寄らない尻の頁（`still=True`＝build_jiko.tail_frame の k＝0・c618 の引用の頁）＝寄りの始めの1点だけ
        # 🆕 22本目 ⑤b-7：地図のカット（衛星写真＝`sat`）も寄らない（build_jiko の meta で still＝True）＝本番と同じ1点だけ。
        #    寄る前提で測ると、衛星写真の上の端の地名（c812・c813 の「Orlando」）が寄りの終わりに半分切れると鳴った（本番では切れない）
        return {0.0: CS.crop_rect(sw, sh, box, 0.0, b, xb, zm)}
    return {i / (K_STEPS - 1): CS.crop_rect(sw, sh, box, i / (K_STEPS - 1), b, xb, zm) for i in range(K_STEPS)}


def frac_in(a0, a1, e, inside_is_high):
    """[a0,a1] を位置 e で切ったとき、窓の内側に残る割合。"""
    f = (a1 - e) / max(a1 - a0, 1e-6)
    return f if inside_is_high else 1 - f


def cut_rows(cid, spec, ocr, photo_of, box_of, sides=False, rects=None):
    """1カットぶん (cid, 辺, 見えている割合, 行の字, 画面での高さpx, 切る前の箱)。🔴 本番も対照もここを通る。

    同じ行・同じ辺は、刻みのうち**いちばん欠けた1点**だけ返す（刻みの数だけ行が水増しされないように）。
    `rects` … 窓の出し方（既定＝`rects_of`）。対照で「両端だけ」の旧い測り方と比べるときに渡す。
    """
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
    worst = {}
    for k, r in (rects or rects_of)(X1 - X0, Y1 - Y0, box_of[cid], spec).items():
        L, T, R, B = r["left"], r["top"], r["left"] + r["cw"], r["top"] + r["ch"]
        sy = r["h"] / r["ch"]
        # 🆕 2026-10-25（25本目 ⑤b-2）：**全面の絵は字幕の帯（y SUB_Y〜1080・真っ黒）が下を覆う＝帯の上の辺も画面に出る辺**。
        #    窓の下の辺だけ測っていたので、c107（付図24 の頁を全面で下へ流す）の「速度制限（曲線半径304m）」の行が帯の上の辺で半分に
        #    切れていても鳴らなかった（試し焼き 40182234709 を原寸で見て分かった）。額装（箱の下が帯より上）は帯がかからない＝測らない
        oy = r["box"][1]
        eb = T + (S.SUB_Y - oy) / sy if oy + r["h"] > S.SUB_Y else None
        for li, (ln, b) in enumerate(moved):
            if b[2] <= L or b[0] >= R or b[3] <= T or b[1] >= B:
                continue
            edges = [("窓上", frac_in(b[1], b[3], T, True)),
                     ("窓下", frac_in(b[1], b[3], B, False))]
            if eb is not None and T < eb < B:
                edges.append(("帯上", frac_in(b[1], b[3], eb, False)))
            if sides:
                edges += [("窓左", frac_in(b[0], b[2], L, True)),
                          ("窓右", frac_in(b[0], b[2], R, False))]
            for side, f in edges:
                if LO < f < HI and ((li, side) not in worst or f < worst[(li, side)][2]):
                    worst[(li, side)] = (cid, f"{side} k{k:.2f}", f, ln["text"], round((b[3] - b[1]) * sy),
                                         ln["box"])
    return list(worst.values())


def scan(spec_map, ocr, photo_of, box_of, skip, sides=False):
    rows = []
    # 🆕 18本目 ⑤b-7c：台本の順＋写真・頁の差し込み（尻）の仮の鍵 `<cid>~t`（CS.keys_of）＝差し込んだ頁も測る
    for cid in CS.keys_of(photo_of):
        if cid in skip or cid not in photo_of:
            continue
        rows += cut_rows(cid, spec_map.get(cid) or {}, ocr, photo_of, box_of, sides)
    return rows


def pick_control(spec_map, ocr, photo_of, box_of, skip):
    """合成の対照に使う (カット, SPEC, 行)。本番の頁のカットのうち、trim の内側でいちばん幅の広い字の行。"""
    best = None
    for cid in S.ORDER:
        spec = spec_map.get(cid) or {}
        # 🆕 2026-10-27（26本目 ⑤b-3）：地図のカット（衛星写真＝`sat`）は対照に使わない。頁のカットがまだ無い回で、Google の地名の行
        #    （c218「オランダ ベルリン ポーランド」）がいちばん幅の広い行として選ばれ、陽性①②が「出ない」で止まった＝trim を行の真ん中へ動かすと
        #    額（16:9）に合わせて横が切られ、右寄りの地名の行が窓の外へ出る（地図は本番で trim も寄りも無い＝rects_of の1点だけ）
        if cid in skip or cid not in photo_of or not spec.get("panel") or spec.get("sat"):
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


def synth_control():
    """🆕 2026-10-18（23本目 ⑤b-2）：本番に対照の行が無い回（頁のカット0・額装の写真に字の行が無い）の**合成の頁**＝額装の箱と字の行1本。
    23本目は報告書の頁を写すカットが0で、OCR が拾ったのは写真の模様の幻の行だけ＝pick_control が何も返さず、物差しを確かめられずに止まっていた。
    下の3つの対照（陽性①②・陰性）は本番と同じ `cut_rows` を通す＝物差しの検算として同じ（sweep_control と同じ合成の作法）"""
    size, box = [1120, 641], (72, 213, 1120, 641)
    ln = dict(box=[100, 300, 1000, 330], text="SYNTH LINE")
    ocr = {"synth_page.png": dict(size=size, lines=[ln])}
    return ("cP", dict(panel=True), ln, 900, (0.0, 0.0, 1.0, 1.0), size[1]), ocr, {"cP": "x/synth_page.png"}, {"cP": box}


def selftest(spec_map, ocr, photo_of, box_of, skip):
    got = pick_control(spec_map, ocr, photo_of, box_of, skip)
    if not got:
        # 🆕 23本目 ⑤b-2：本番に対照の行が無い＝合成の頁で回す（黙って飛ばさない・何で確かめたかを出す）
        print("  ・本番に対照に使える頁の行が無い（panel の頁・写真に OCR の字の行が無い）＝合成の頁で物差しを確かめる")
        got, ocr, photo_of, box_of = synth_control()
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
    return ok and sweep_control() and band_control()


def band_control():
    """陽性④・陰性（合成・2026-10-25 25本目 ⑤b-2）：全面の絵（箱 1920×1080）で、字幕の帯の上の辺（y SUB_Y）が行を横切ると「帯上」で出る・
    帯より上の行は出ない・額装（箱の下が帯より上）は帯を測らない"""
    size = [1920, 1080]
    mid = S.SUB_Y
    lines = [dict(box=[100, mid - 15, 1000, mid + 15], text="SYNTH ACROSS"), dict(box=[100, mid - 60, 1000, mid - 30], text="SYNTH ABOVE")]
    ocr = {"synth_full.png": dict(size=size, lines=lines)}
    full = cut_rows("cF", dict(bias=0.5), ocr, {"cF": "x/synth_full.png"}, {"cF": (0, 0, 1920, 1080)})
    band = {r[3] for r in full if r[1].startswith("帯上")}
    panel = cut_rows("cF", dict(bias=0.5, panel=True), ocr, {"cF": "x/synth_full.png"}, {"cF": (384, 216, 1152, 648)})
    good = band == {"SYNTH ACROSS"} and not [r for r in panel if r[1].startswith("帯上")]
    print(f"  {'✓' if good else '🔴'} 陽性④ 全面の絵で帯の上の辺が行を横切る → 帯上で {sorted(band) or '出ない'}"
          f"（ACROSS だけ出て ABOVE は出ないはず）・額装は帯を測らない")
    return good


def sweep_control():
    """陽性③（合成・2026-09-25）：寄りの**途中だけ**で下の辺が行を横切る（c520 の型）。
    両端（k=0/1）だけの旧い測り方では出ず、刻み（`rects_of`）で出ること。"""
    size, box = [1120, 641], (72, 213, 1120, 641)       # 額装＝窓が絵の縦横比と同じ
    spec = dict(bias=0.0)                               # 上の辺を留める＝下の辺だけが上がる
    e0, e1 = (CS.crop_rect(size[0], size[1], box, k, 0.0, 0.5, 1.0) for k in (0.0, 1.0))
    b0, b1 = e0["top"] + e0["ch"], e1["top"] + e1["ch"]
    h, mid = (b0 - b1) / 3, (b0 + b1) / 2               # k=0 では全部内・k=1 では全部外の行
    ocr = {"synth.png": dict(size=size, lines=[dict(box=[100, mid - h / 2, 1000, mid + h / 2], text="SYNTH")])}
    args = ("cS", spec, ocr, {"cS": "x/synth.png"}, {"cS": box})
    # 🆕 2026-10-28（26本目 ⑤b-7）：額装を寄る回（FRAME_STILL＝False＝25本目まで）の型として回し、終わったら必ず戻す。
    #    FRAME_STILL＝True（26本目から）の額装は寄らない＝同じ行は出ないのが正しい（陰性⑤）
    import build_jiko as B
    keep = B.FRAME_STILL
    try:
        B.FRAME_STILL = False
        old = cut_rows(*args, rects=lambda sw, sh, bx, sp: {k: CS.crop_rect(sw, sh, bx, k, 0.0, 0.5, 1.0)
                                                            for k in (0.0, 1.0)})
        new = cut_rows(*args)
        B.FRAME_STILL = True
        still = cut_rows(*args)
    finally:
        B.FRAME_STILL = keep
    good = not old and bool(new) and not still
    print(f"  {'✓' if good else '🔴'} 陽性③ 寄りの途中だけで下の辺が行を横切る → 両端だけ {'出る' if old else '出ない'}"
          f"／刻み {f'{new[0][2]:.0%}（{new[0][1]}）で出た' if new else '出ない'}（両端では出ず、刻みで出るはず）")
    print(f"  {'✓' if not still else '🔴'} 陰性⑤ FRAME_STILL の額装（寄らない）では同じ行は {'出た' if still else '出ない'}（出ないはず＝本番の絵は k＝0 だけ）")
    return good


def main():
    sides = "--sides" in sys.argv
    ocr = CS.load_ocr()
    spec_map, photo_of, box_of, skip = CS.production_inputs()
    print("■ 物差しの検算（合成の対照）")
    if not selftest(spec_map, ocr, photo_of, box_of, skip):
        print("🔴 対照が外れた＝物差しか OCR の読み置きが変わった。本番に当てずに止める")
        return 2
    # 🆕 2026-10-13（21本目 ⑤b-7）：「字でない」と決めた範囲（cuts/ss.OCR_NOT_TEXT＝check_slide.drop_not_text）の対照＝合成の読み置きで
    #    範囲の中の行だけを外し、外の行は残し、何にも当たらない宣言は「古い」として返すこと
    _fake = {"z.jpg": {"size": [100, 100], "lines": [dict(box=[10, 10, 30, 14], text="a"), dict(box=[60, 60, 90, 64], text="b")]}}
    _stale = CS.drop_not_text(_fake, {"z.jpg": [((0, 0, 50, 50), "対照"), ((0, 80, 10, 90), "当たらない宣言")]})
    CS._DROPPED[:] = [d for d in CS._DROPPED if d[0] != "z.jpg"]      # 対照の行を外した行の表に残さない
    if [ln["text"] for ln in _fake["z.jpg"]["lines"]] != ["b"] or len(_stale) != 1:
        print(f"🔴 「字でない」範囲の対照が外れた（残った行 {_fake['z.jpg']['lines']}・古い宣言 {_stale}）")
        return 2
    print("  ✓ 「字でない」範囲（ss.OCR_NOT_TEXT）は範囲の中の行だけを外し、当たらない宣言を古いとして返す")
    if "--selftest" in sys.argv:
        print("✓ 物差しは正しい")
        return 0
    # 🔴🔴 2026-09-25（13本目 ⑤c'）：**読み置きの無いカットを黙って飛ばしていた**（`cut_rows` が [] を返す）。
    #    13本目の `ocr_slides.json` は ⑤b-1 の3点だけ＝写真・頁45カットのうち **42カットを測らずに ✓** だった
    #    （c520 の頁 pg2046 も c311 の pg95 も）。→ 読み置きが無ければ止める（[[feedback-parsers-fail-closed]]）
    missing = [cid for cid in CS.keys_of(photo_of) if cid in photo_of and cid not in skip
               and not ocr.get(Path(photo_of[cid]).name)]
    if missing:
        print(f"🔴 OCR の読み置きが無い写真・頁のカット {len(missing)} 件＝**測っていない**："
              f"{' '.join(missing[:15])}{' …' if len(missing) > 15 else ''}\n"
              f"   → `python tools/check_slide.py --ocr` で読み置きを作り直す（0件を合格にしない）")
        return 1
    rows = scan(spec_map, ocr, photo_of, box_of, skip, sides)
    small = [r for r in rows if r[4] < MIN_H_PX]
    for r in small:
        print(f"  ・ 参考（画面 {r[4]}px＜{MIN_H_PX}px＝字として読めない・測らない）{r[0]}「{r[3][:30]}」{r[1]}")
    rows = [r for r in rows if r[4] >= MIN_H_PX]
    # 🆕 2026-10-06（19本目 ⑤b-7b）：**縦長の箱（幅が高さの半分未満）は横書きの行ではない**＝OCR が写真の模様を字と読んだ幻
    #    （c701＝N#18 の建物の縦の筋「に 」 、 い」＝箱 11×39px）。本物の行は1字でも幅≒高さ（英字の行は幅が高さの数倍）。
    #    黙って捨てず、上の「画面で小さい行」と同じく参考に出す（ON_PURPOSE の作法）
    tall = [r for r in rows if (r[5][2] - r[5][0]) < 0.5 * (r[5][3] - r[5][1])]
    for r in tall:
        print(f"  ・ 参考（箱が縦長 {r[5][2] - r[5][0]}×{r[5][3] - r[5][1]}px＝横書きの行ではない・測らない）{r[0]}「{r[3][:30]}」{r[1]}")
    rows = [r for r in rows if r not in tall]
    hard = [r for r in rows if r[1][:2] in ("窓上", "窓下", "帯上")]      # 🆕 25本目 ⑤b-2：帯の上の辺も止める（左右は参考のまま）
    cuts = sorted({r[0] for r in rows}, key=CS.keys_of(photo_of).index)
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
