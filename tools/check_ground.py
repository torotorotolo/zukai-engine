# -*- coding: utf-8 -*-
"""check_ground.py — 説明カットの地の写真（暗くするだけ）と SNS の注釈の門番（2026-10-30 新設・27本目 ⑤b-4）。

■ 何を見るか
  ① 8:1 … 地の写真のカット（SPEC の `dim`＝`cuts.ss.gr`）ごとに、**字と図の線の周りの地**（写真が見えている所だけ）で、
     字の白（J.INK_W）と地のコントラスト比が 8:1 以上か（了承② 決め1＝見本B・CM254 に ×0.32 で 8.2:1）。
     インク＝scene_jiko が Chrome で焼いた層（`out/jiko/<cid>_*.png`）のα・地＝本番と同じ式（`build_jiko.fit`＋`build_jiko.ground_dim`）。
     周り＝インクから 10px の帯のうち、どの層も覆っていない画素（不透明な札の中は札の地＝写真ではない）・字幕の帯（y≥900）は除く。
     48px 四方の升ごとに、帯の画素の明るい上位10%の平均（mock27.py の box_lum と同じ＝字にいちばん厳しい所）で比を出し、いちばん悪い升で決める。
  ② SNS … 映像方針の一覧（`ref/<回>/eizou_build/list<回>.tsv`）で印が SNS のカットに、注釈の字（`cuts.ss.SNS_NOTE`）が
     図の層の SVG にあり、焼いた層に黄色い字の画素がある・その画素が置き場（`cuts.ss.SNS_NOTE_BOX`）の中で、右下の透かし（x≥1768・y≥905）・
     字幕の帯（y≥900）・左下の出典の行（y≥858）・右上の章の印（y<100）に入らない。印の無いカットに注釈を出していないか（⚠️）
  ③ 台帳 … dim のカットの写真は CC BY・CC0（`ss.GROUND_LIC`）・dim は `ss.GROUND` の写真の値と同じ（写真ごとに1つ＝続くカットで跳ねない）
     ・静止（cam・fmove を書かない）・暗幕（veil）を書かない
  🔴 層が無い（焼く前）・写真が読めない・測れる升が0 は**落とす**（fail closed＝測っていないのに通さない）。

■ 使い方
    python -P tools/check_ground.py              … ①②③（層は `python tools/scene_jiko.py --only=<頭>` か Actions の層の段で焼いたもの）
    python -P tools/check_ground.py --suggest    … 写真ごとに 8:1 を満たす**いちばん明るい**掛け算（0.01 刻み・切り捨て）＝`ss.GROUND` に写す値
    python -P tools/check_ground.py --selftest   … 陽性（鳴るべき所で鳴る）・陰性（通るべき所で通る）
  終了コード＝0 通った／1 落ちた／2 道具の誤り
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

TARGET = 8.0           # 了承② 決め1（見本B）
RING = 10              # インクの周りの帯の幅（px）
TILE = 48              # 升の一辺（px）
MIN_PX = 40            # 升で測るのに要る帯の画素の数
TOP = 0.10             # 升の帯の画素の明るい上位の割合
SUB_Y = 900            # 字幕の帯（ここから下は測らない）
INK_A = 128            # インクとみなすα（0〜255）
COVER_A = 20           # 地が見えているとみなすα の上限
# SNS の注釈の避ける所（1920×1080）
WM = (1768, 905)       # 右下の透かし（x≥・y≥）
CRED_Y = 858           # 左下の出典の行の上
CHAP_Y = 100           # 右上の章の印の下
YELLOW_TOL = 40        # 黄色い字の色の許し（各色 ±）
YELLOW_MIN = 0.012     # 注釈の箱の中の黄色い画素の割合の下限（字が描けている）


def _lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lum(rgb):
    """相対輝度（WCAG）。rgb＝(…, 3) の配列 0〜255。"""
    rgb = np.asarray(rgb, dtype=np.float64)
    return 0.2126 * _lin(rgb[..., 0]) + 0.7152 * _lin(rgb[..., 1]) + 0.0722 * _lin(rgb[..., 2])


def _hex(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def ink_lum():
    import jiko_style as J
    return float(lum(np.array(_hex(J.INK_W))))


def ring_of(alpha):
    """インク（α≥INK_A）の周り RING px の帯のうち、地が見えている所（α≤COVER_A）・字幕の帯より上。"""
    from scipy import ndimage
    ink = alpha >= INK_A
    grown = ndimage.binary_dilation(ink, structure=np.ones((3, 3), bool), iterations=RING)
    ring = grown & (alpha <= COVER_A)
    ring[SUB_Y:, :] = False
    return ring


def worst(L, ring, Lw=None):
    """升ごとの比。(いちばん悪い比, (x, y), 測った升の数, 比の中央値)。L＝地の相対輝度の配列。"""
    Lw = ink_lum() if Lw is None else Lw
    h, w = ring.shape
    best = (float("inf"), None)
    ratios = []
    for y0 in range(0, h, TILE):
        for x0 in range(0, w, TILE):
            m = ring[y0:y0 + TILE, x0:x0 + TILE]
            n = int(m.sum())
            if n < MIN_PX:
                continue
            v = np.sort(L[y0:y0 + TILE, x0:x0 + TILE][m])
            top = v[int(len(v) * (1 - TOP)):]
            r = (Lw + 0.05) / (float(top.mean()) + 0.05)
            ratios.append(r)
            if r < best[0]:
                best = (r, (x0 + TILE // 2, y0 + TILE // 2))
    if not ratios:
        return 0.0, None, 0, 0.0
    return best[0], best[1], len(ratios), float(np.median(ratios))


def dimmed(ph_rgb, k):
    """build_jiko.ground_dim と同じ式（画素の値に k を掛けて丸める）。ph_rgb＝(H, W, 3) uint8。"""
    return np.rint(ph_rgb.astype(np.float64) * round(float(k), 3)).clip(0, 255)


# ══════════════════════════════════════════════════════════
#  本番の絵（層と写真）を読む
# ══════════════════════════════════════════════════════════
def _cut_inputs(cid, idx, B, S):
    """(写真を画面いっぱいに切った RGB の配列・層のαの和・dim)。層が無ければ RuntimeError。"""
    from PIL import Image
    names = [n for n in idx[cid]["layers"]]
    if not names:
        raise RuntimeError(f"{cid}: 層の名前が無い")
    miss = [n for n in names if not (B.OUT / f"{n}.png").exists()]
    if miss:
        raise RuntimeError(f"{cid}: 焼いた層が無い {miss[:3]}（`python tools/scene_jiko.py --only={cid}` か Actions の層の段）")
    a = None
    for n in names:
        al = np.asarray(Image.open(B.OUT / f"{n}.png").convert("RGBA"))[..., 3]
        a = al if a is None else np.maximum(a, al)
    ph = B.load_photo(S.PHOTO_CUTS[cid][1], S.PHOTO_CUTS[cid][0], S.PHOTO_TRIM.get(cid), S.PHOTO_LEVELS.get(cid))
    xb, zm = S.PHOTO_CROP[cid]
    full = B.fit(ph, S.PHOTO_FULL, 0.0, S.PHOTO_CUTS[cid][2], xb, zm).convert("RGB")
    return np.asarray(full), a, idx[cid].get("dim")


def _load():
    import scene_jiko as S
    import build_jiko as B
    idx, jobs = S.layer_index(allow_missing=True)      # 画の無いカット（衛星写真は ⑤b-5）は飛ばす＝地の写真のカットは全部ある
    return S, B, idx, jobs


def _dim_cuts(S, idx):
    return [c for c in S.ORDER if c in idx and idx[c].get("dim")]


def check_ledger(S, idx):
    """③ 台帳。"""
    import cuts.ss as ss
    bad = []
    for c in _dim_cuts(S, idx):
        sp = S.SPEC[c]
        name = sp["photo"][len(ss.EP):-len(".jpg")] if sp["photo"].startswith(ss.EP) else sp["photo"]
        lic = (ss._assets().get(name) or {}).get("lic")
        if lic not in ss.GROUND_LIC:
            bad.append(f"{c}: 地の写真 {name} の権利 {lic}＝CC BY・CC0 だけ（§5b-117）")
        if name not in ss.GROUND:
            bad.append(f"{c}: 地の写真 {name} が ss.GROUND に無い")
        elif abs(float(ss.GROUND[name]) - float(sp["dim"])) > 1e-9:
            bad.append(f"{c}: dim {sp['dim']} が ss.GROUND[{name}]={ss.GROUND[name]} と違う（写真ごとに1つ）")
        for k in ("cam", "fmove", "veil"):
            if sp.get(k) is not None:
                bad.append(f"{c}: 地の写真のカットに {k} を書いた（動かさない・暗幕を敷かない）")
    return bad


def check_contrast(S, B, idx, cids=None):
    """① 8:1。[(cid, 比, 位置, 升の数, 中央値, 誤り)]"""
    out = []
    for c in (cids or _dim_cuts(S, idx)):
        try:
            ph, a, k = _cut_inputs(c, idx, B, S)
        except Exception as e:                       # noqa: BLE001
            out.append((c, 0.0, None, 0, 0.0, str(e)))
            continue
        r, at, n, med = worst(lum(dimmed(ph, k)), ring_of(a))
        out.append((c, r, at, n, med, "" if n else "測れる升が0（層のαが無い？）"))
    return out


def suggest(S, B, idx):
    """写真ごとに、その写真を地にする全カットで 8:1 を満たすいちばん明るい k（0.01 刻み・切り捨て）。"""
    import cuts.ss as ss
    by = {}
    for c in _dim_cuts(S, idx):
        name = S.SPEC[c]["photo"][len(ss.EP):-len(".jpg")]
        by.setdefault(name, []).append(c)
    res = {}
    for name, cs in sorted(by.items()):
        ins = [_cut_inputs(c, idx, B, S) for c in cs]
        rings = [ring_of(a) for _ph, a, _k in ins]
        ks = []
        for (ph, _a, _k), rg in zip(ins, rings):
            lo, hi = 0.05, 1.0
            if worst(lum(dimmed(ph, hi)), rg)[0] >= TARGET:
                ks.append(1.0)
                continue
            if worst(lum(dimmed(ph, lo)), rg)[0] < TARGET:
                ks.append(0.0)
                continue
            for _ in range(14):
                mid = (lo + hi) / 2
                if worst(lum(dimmed(ph, mid)), rg)[0] >= TARGET:
                    lo = mid
                else:
                    hi = mid
            ks.append(int(lo * 100) / 100.0)
        res[name] = (min(ks), cs, ks)
    return res


def _sns_cuts(S):
    """映像方針の一覧の印 SNS のカット。一覧が無ければ None（＝SNS の画面が無い回）。"""
    import csv
    import cuts.ss as ss
    n = ss.EP.strip("/")[2:]
    p = ss.REF / "eizou_build" / f"list{n}.tsv"
    if not p.exists():
        return None
    rows = list(csv.reader(p.open(encoding="utf-8"), delimiter="\t"))
    h = rows[0]
    if "mark" not in h:
        raise RuntimeError(f"{p.name} に mark の列が無い")
    return [dict(zip(h, r))["cid"] for r in rows[1:] if dict(zip(h, r)).get("mark") == "SNS"]


def check_sns(S, B, jobs, want=None):
    """② SNS の注釈。want＝印 SNS のカット（selftest が差し込む・既定は映像方針の一覧から）。"""
    from PIL import Image
    import cuts.ss as ss
    bad, warn = [], []
    want = _sns_cuts(S) if want is None else want
    if want is None:
        return bad, warn, []
    note = ss.SNS_NOTE
    yel = np.array(_hex(ss.SNS_NOTE_INK))
    y0, x1, y1 = ss.SNS_NOTE_BOX
    for c in S.ORDER:
        svg = "".join(v for k, v in jobs.items() if k.startswith(c + "_"))
        has = note in svg
        if c not in want:
            if has:
                warn.append(f"{c}: 印の無いカットに SNS の注釈がある")
            continue
        if not has:
            bad.append(f"{c}: 印 SNS のカットの層に注釈「{note}」の字が無い")
            continue
        pngs = [B.OUT / f"{k}.png" for k in jobs if k.startswith(c + "_")]
        if not pngs or not all(p.exists() for p in pngs):
            bad.append(f"{c}: 焼いた層が無い（注釈の画素を測れない）")
            continue
        hit = None
        for p in pngs:
            im = np.asarray(Image.open(p).convert("RGBA")).astype(int)
            m = (np.abs(im[..., :3] - yel).max(axis=2) <= YELLOW_TOL) & (im[..., 3] >= 200)
            if m.sum() > 50:
                hit = m if hit is None else (hit | m)
        if hit is None:
            bad.append(f"{c}: 焼いた層に注釈の黄色い字の画素が無い")
            continue
        ys, xs = np.nonzero(hit)
        bx0, by0, bx1, by1 = int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())
        frac = float(hit[y0:y1, :x1].sum()) / max(1, (y1 - y0) * (x1 - bx0))
        if by0 < y0 or by1 > y1 or bx1 > x1:
            bad.append(f"{c}: 注釈の字（x{bx0}〜{bx1}・y{by0}〜{by1}）が置き場（y{y0}〜{y1}・右端 x{x1}）の外")
        if by1 >= SUB_Y or (bx1 >= WM[0] and by1 >= WM[1]) or by1 >= CRED_Y or by0 < CHAP_Y:
            bad.append(f"{c}: 注釈の字（y{by0}〜{by1}）が字幕の帯・透かし・左下の出典の行・章の印にかかる")
        if frac < YELLOW_MIN:
            bad.append(f"{c}: 注釈の箱の黄色い画素 {frac:.3f}＜{YELLOW_MIN}（字が描けていない）")
    return bad, warn, want


# ══════════════════════════════════════════════════════════
#  selftest（陽性＝鳴るべき所で鳴る・陰性＝通るべき所で通る）
# ══════════════════════════════════════════════════════════
def selftest():
    ok = True
    H_, W_ = 1080, 1920

    def say(cond, msg):
        nonlocal ok
        print(("  ✓ " if cond else "  🔴 NG ") + msg)
        ok &= bool(cond)

    def blob(x0, y0, x1, y1):
        a = np.zeros((H_, W_), np.uint8)
        a[y0:y1, x0:x1] = 255
        return a

    txt = blob(400, 400, 700, 460)
    # 陰性：暗い地（30）＝通る
    r, _at, n, _m = worst(lum(np.full((H_, W_, 3), 30.0)), ring_of(txt))
    say(n > 0 and r >= TARGET, f"陰性 暗い地（30）で通る（{r:.1f}:1・升 {n}）")
    # 陽性：明るい地（200）＝鳴る
    r, _at, n, _m = worst(lum(np.full((H_, W_, 3), 200.0)), ring_of(txt))
    say(n > 0 and r < TARGET, f"陽性 明るい地（200）で鳴る（{r:.1f}:1）")
    # 位置を測る：左半分だけ明るい地＝字が右（暗い所）なら通り、左（明るい所）なら鳴る
    half = np.full((H_, W_, 3), 25.0)
    half[:, :W_ // 2] = 210.0
    r_r = worst(lum(half), ring_of(blob(1300, 400, 1600, 460)))[0]
    r_l = worst(lum(half), ring_of(blob(300, 400, 600, 460)))[0]
    say(r_r >= TARGET and r_l < TARGET, f"位置 暗い側の字は通る（{r_r:.1f}）・明るい側の字は鳴る（{r_l:.1f}）")
    # 小さな明るい点（街の灯）が字のすぐ横にある＝上位10%で鳴る（平均では通ってしまう所）
    spot = np.full((H_, W_, 3), 20.0)
    spot[395:410, 640:700] = 255.0
    r_s = worst(lum(spot), ring_of(txt))[0]
    say(r_s < TARGET, f"陽性 字の横の明るい点で鳴る（{r_s:.1f}:1・平均では見えない所）")
    # 不透明な札の中は地ではない＝札の下だけ明るい写真でも、札の中の字の周りは測らない（札の外の暗い地で決まる）
    card = np.zeros((H_, W_), np.uint8)
    card[300:560, 300:800] = 200
    under = np.full((H_, W_, 3), 20.0)
    under[300:560, 300:800] = 240.0
    r_c = worst(lum(under), ring_of(np.maximum(card, txt)))[0]
    say(r_c >= TARGET, f"陰性 札に覆われた所（下が明るい）は測らない（{r_c:.1f}:1）")
    # 測れる升が0 は 0.0（落とす側）を返す
    r_z, _at, n_z, _m = worst(lum(np.full((H_, W_, 3), 230.0)), np.zeros((H_, W_), bool))
    say(n_z == 0 and r_z == 0.0, "測れる升が0 は 0.0（落とす側）を返す")
    # 字幕の帯の中は測らない
    rg = ring_of(blob(400, 950, 700, 1000))
    say(int(rg.sum()) == 0, "字幕の帯（y≥900）の字の周りは測らない")
    # dimmed は build_jiko.ground_dim と同じ値
    try:
        from PIL import Image
        import build_jiko as B
        rnd = (np.random.default_rng(7).random((40, 60, 3)) * 255).astype(np.uint8)
        a = np.asarray(B.ground_dim(Image.fromarray(rnd), 0.37).convert("RGB")).astype(int)
        b = dimmed(rnd, 0.37).astype(int)
        say(int(np.abs(a - b).max()) == 0, "dimmed＝build_jiko.ground_dim と同じ画素（本番と同じ式）")
        g = np.asarray(B.ground_dim(Image.fromarray(np.array([[[200, 100, 50]]], np.uint8)), 0.5).convert("RGB"))[0, 0]
        say(tuple(int(v) for v in g) == (100, 50, 25), "ground_dim は色相を変えない（各色に同じ掛け算）")
    except Exception as e:                           # noqa: BLE001
        say(False, f"build_jiko.ground_dim を呼べない: {e}")
    # suggest の二分探索：一様な地 v で 8:1 の境の k
    v = 180.0
    lo, hi = 0.05, 1.0
    rg = ring_of(txt)
    for _ in range(14):
        mid = (lo + hi) / 2
        if worst(lum(np.full((H_, W_, 3), v * mid)), rg)[0] >= TARGET:
            lo = mid
        else:
            hi = mid
    k = int(lo * 100) / 100.0
    ra = worst(lum(np.rint(np.full((H_, W_, 3), v * k))), rg)[0]
    rb = worst(lum(np.rint(np.full((H_, W_, 3), v * (k + 0.02)))), rg)[0]
    say(ra >= TARGET and rb < TARGET, f"suggest の境（地 180 で k={k}: {ra:.2f}:1・k+0.02: {rb:.2f}:1）")
    # mock27 の見本B（CM254 ×0.32＝8.2:1）と同じ物差しか（INK_W の輝度）
    say(abs(ink_lum() - 0.8737) < 0.01, f"字の白 J.INK_W の輝度 {ink_lum():.4f}（mock27 と同じ色）")
    # ② SNS の注釈：作り物の層（黄色い字の帯）で、ある・無い・置き場の外を見分けるか
    import tempfile
    import types
    from PIL import Image, ImageDraw
    import cuts.ss as ss
    y0, x1, y1 = ss.SNS_NOTE_BOX
    with tempfile.TemporaryDirectory() as td:
        out = Path(td)

        def layer(name, box):
            im = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
            if box:
                d = ImageDraw.Draw(im)
                d.rectangle(box, fill=(0, 0, 0, 255))
                bx0, by0, bx1, by1 = box
                for x in range(bx0 + 10, bx1 - 10, 14):         # 字の代わりの黄色い縦の棒
                    d.rectangle((x, by0 + 8, x + 6, by1 - 8), fill=_hex(ss.SNS_NOTE_INK) + (255,))
            im.save(out / f"{name}.png")
        layer("x1_base", (1300, y0, x1, y1))                    # 正しい置き場
        layer("x2_base", None)                                  # 字の画素が無い
        layer("x3_base", (1500, 950, 1900, 1000))               # 字幕の帯と透かしの中
        fS = types.SimpleNamespace(ORDER=["x1", "x2", "x3", "x4"])
        fB = types.SimpleNamespace(OUT=out)
        jobs_ = {"x1_base": ss.SNS_NOTE, "x2_base": ss.SNS_NOTE, "x3_base": ss.SNS_NOTE, "x4_base": "（注釈なし）"}
        bad_, _w, _ = check_sns(fS, fB, jobs_, want=["x1", "x2", "x3", "x4"])
        say(not any(b.startswith("x1:") for b in bad_), "陰性 正しい置き場の注釈は通る")
        say(any(b.startswith("x2:") and "黄色い字の画素が無い" in b for b in bad_), "陽性 字の画素が無いと鳴る")
        say(any(b.startswith("x3:") and "字幕の帯" in b for b in bad_), "陽性 字幕の帯・透かしに入ると鳴る")
        say(any(b.startswith("x4:") and "注釈" in b for b in bad_), "陽性 印 SNS のカットの層に注釈の字が無いと鳴る")
    return ok


def main():
    if "--selftest" in sys.argv:
        ok = selftest()
        print("selftest:", "通った" if ok else "🔴 落ちた")
        return 0 if ok else 1
    S, B, idx, jobs = _load()
    if "--suggest" in sys.argv:
        res = suggest(S, B, idx)
        print(f"■ 写真ごとの明るさ（8:1 を満たすいちばん明るい掛け算・0.01 刻み）{len(res)}点")
        for name, (k, cs, ks) in res.items():
            flag = "🔴 " if k < 0.15 else ""
            print(f"  {flag}{name}: {k:.2f}  ← " + "・".join(f"{c} {x:.2f}" for c, x in zip(cs, ks)))
        print("  （🔴＝0.15 未満＝ほとんど黒＝何の写真か分からない見込み＝地の写真を替える候補）")
        print("GROUND = {" + ", ".join(f'"{n}": {k:.2f}' for n, (k, _c, _x) in res.items()) + "}")
        return 0
    bad = []
    bad += [f"③ {b}" for b in check_ledger(S, idx)]
    rows = check_contrast(S, B, idx)
    print(f"■ ① 字と図の線の周りの地（地の写真 {len(rows)}カット・下限 {TARGET:.0f}:1）")
    for c, r, at, n, med, err in rows:
        if err:
            bad.append(f"① {c}: {err}")
            print(f"  🔴 {c}: {err}")
            continue
        mark = "✓" if r >= TARGET else "🔴"
        print(f"  {mark} {c}: いちばん悪い升 {r:.1f}:1（{at}）・中央値 {med:.1f}:1・升 {n}")
        if r < TARGET:
            bad.append(f"① {c}: {r:.1f}:1＜{TARGET:.0f}:1（{at} の升）")
    sb, sw, want = check_sns(S, B, jobs)
    print(f"■ ② SNS の注釈（印 SNS {len(want)}カット：{'・'.join(want) or 'なし'}）")
    bad += [f"② {b}" for b in sb]
    for w in sw:
        print(f"  ⚠️ {w}")
    for b in bad:
        print(f"  🔴 {b}")
    if not rows and not want:
        print("（地の写真のカットも SNS の画面も無い＝測る物が無い）")
    print("✓ 通った" if not bad else f"🔴 {len(bad)}件")
    return 0 if not bad else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:                           # noqa: BLE001
        import traceback
        traceback.print_exc()
        print(f"🔴 道具の誤り: {e}")
        sys.exit(2)
