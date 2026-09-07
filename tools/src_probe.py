# -*- coding: utf-8 -*-
"""素材の**中身**を画素で測る（工程の新設計 §6 の②）。

■ なぜ要るか
    ②で素材を選ぶとき、これまでは**題名と点数**で判断していた。
    5本目 SL-1 の引き継ぎは Commons を「全画面8点・残り45点は2値スキャンの図面」と書いていたが、
    実測すると**幅1280以上が52点**あり、5000px超の大半は図面ではなく**写真**だった。
    ＝ 題名（"floor plan" / "Interior view"）で連続階調か2値かは決まらない。
    → [[feedback-dont-state-inferences-as-findings]] / [[feedback-measure-the-source-before-choosing-the-crop]]

■ 何を測るか
    | 量 | 意味 | 使いどころ |
    |---|---|---|
    | 🔴 `ink` **インク率** | 明度 200 未満の画素の割合 | **全画面（full）か額装パネル（panel）か**を分ける |
    | `band` 空白帯 | 四辺から続く無インクの帯の最大割合 | 余白が広い＝切らないと使えない |
    | `bbox` `fx` `fy` | インクのある範囲とその中心（原画の比） | 🔴 `focus(fx,fy)` の当たりを式で出すため |
    | `w x h` | **原本**の寸法（配信物ではない） | 全画面に耐えるか（幅1280以上） |
    | `mid` `levels` | 中間調率・使われている階調の段数 | 診断用。判定には使わない（下の理由） |

■ ⚠️ この道具が見ていないもの
    - 何が写っているか（意味）。⇒ 目で1回見る。ただし**選別のあとに、絞った点数だけ**
    - 権利。⇒ `commons_probe.py` / `nara_probe.py` の担当
    - 引き伸ばし（配信 CDN が小さい原本を拡大して返す）。⇒ `dvids_probe.py` の担当。
      ここでは Commons の imageinfo が返す**原本の寸法**を使うので問題は起きない

■ しきい値の根拠（このファイルの `--hist` で取り直せる）
    `INK_FULL = 0.42` … SL-1 の59点で測った分布の切れ目（図面 最大 0.35／写真 最小 0.49）。
    間に**1点も無く**、59点すべてで題名（"floor plan" / "Interior view"）と一致した。
    → [[feedback-gate-threshold-from-ledger-split]]（⚠️ 別の題材で使うときは必ず取り直す）

■ 使い方
    python tools/src_probe.py --commons "Category:SL-1 Reactor" --out analytics/materials/sl1_src.json
    python tools/src_probe.py --files ref/surfside/*.jpg
    python tools/src_probe.py --hist analytics/materials/sl1_src.json   # 分布（しきい値の決め直し）
    python tools/src_probe.py --selftest                                # 陽性対照
"""
from __future__ import annotations

import argparse
import io
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
Image.MAX_IMAGE_PIXELS = None

UA = "jiko-kensho/1.0 (research; konariri8@gmail.com)"
API = "https://commons.wikimedia.org/w/api.php"

INK_DARK = 200      # check_blank.py と同じ（明度がこれ未満なら「インク」）
MID_LO, MID_HI = 40, 215
THUMB_W = 1600      # 測るときの幅。⚠️ これ以上小さくすると図面の細線が中間調に化ける

LEVELS_MIN = 0.0005     # 全画素の 0.05% 以上を持つ明度の段だけ「使われている」と数える（診断用）

# 🔴 「全画面に出せる（full）」か「額装パネルにする（panel）」かの判定＝**インク率**。
#    2026-09-07 に3つ試して、割れたのは ink だけだった（→ `--hist` で取り直せる）：
#      ・`mid`（中間調率）    … ❌ **暗い写真**5点を図面と誤判定（Ten-ton crane・Steel shell ほか）
#      ・`levels`（階調の段数）… ❌ HAER の図面は**2値でなくグレースケール走査**なので段数が多い（68〜235）
#      ・`flat`（平坦な画素の割合）… ❌ 図面 0.14〜0.83／写真 0.01〜0.38 で重なる
#      ・🔴 `ink`             … ✅ **図面 0.12〜0.35／写真 0.49〜1.00。間に1点も無い**（59点全部が題名と一致）
#    ⚠️ この量が効くのは、判断そのものが「画面のどれだけがインクで埋まるか」だから。
#       白い紙の図面を全画面に出すと**まぶしくて細線が消える**ので額装パネルにする、という規則の言い換え。
#    ⚠️⚠️ **題材ごとに取り直す。** 雪原・砂漠・霧など**地が白い写真**は ink が低く出て panel 側に落ちる。
#       落ちた点は捨てずに、`--hist` の切れ目を見て手で拾い直すこと。
#    🔴🔴 **`ink` は「白い紙に刷った物」用の量。動画のコマに当ててはいけない**（2026-09-07 実測）。
#       SL-1 の記録映画（1961年の白黒フィルム）410ショットの中央のコマを測ったら
#       **ink の中央値が 1.00**（＝全面が明度200未満）。フィルムには白い地が無いので当たり前で、
#       `ink>0.985` を表題カードの条件にしたら **410/410 が該当**した。
#       → 動画のコマは**明るさに依らない `levels`（階調の段数）**で見る。ただし SL-1 では
#         分布が単峰で切れ目が無く（4〜163・中央135）、**門番にはできなかった**。
#         `levels<60` は「表題カード・ほぼ真っ黒の**候補**」までで、合否は目で決める。
#       → [[feedback-verify-your-own-instrument]]（全部OK／全部NGと出たら道具を疑う）
INK_FULL = 0.42         # 実測の切れ目（0.35 → 0.49）の真ん中


# ────────────────────────────────────────── 測る
def measure(im: Image.Image) -> dict:
    """PIL 画像 1 枚から 5 つの量を出す。返り値は原画に対する**比**で持つ。"""
    g = np.asarray(im.convert("L"), dtype=np.uint8)
    h, w = g.shape
    total = float(h * w)

    ink = g < INK_DARK
    mid = (g >= MID_LO) & (g <= MID_HI)

    # インクのある範囲（行・列ごとに 1 画素でもインクがあるか）
    rows = np.flatnonzero(ink.any(axis=1))
    cols = np.flatnonzero(ink.any(axis=0))
    if len(rows) and len(cols):
        y0, y1 = int(rows[0]), int(rows[-1]) + 1
        x0, x1 = int(cols[0]), int(cols[-1]) + 1
    else:
        y0 = x0 = 0
        y1, x1 = h, w

    # 四辺から続く無インクの帯（check_blank.edge_band と同じ考え方）
    rp = ink.any(axis=1)
    cp = ink.any(axis=0)

    def lead(v):
        nz = np.flatnonzero(v)
        return (int(nz[0]), len(v) - 1 - int(nz[-1])) if len(nz) else (len(v), 0)

    top, bot = lead(rp)
    left, right = lead(cp)
    band = max(top / h, bot / h, left / w, right / w)

    # 使われている階調の段の数（明るさの水準に依らない）
    hist256 = np.bincount(g.ravel(), minlength=256) / total
    levels = int((hist256 >= LEVELS_MIN).sum())

    return dict(
        ink=round(float(ink.sum()) / total, 4),
        mid=round(float(mid.sum()) / total, 4),
        levels=levels,
        band=round(float(band), 4),
        bbox=[round(x0 / w, 3), round(y0 / h, 3), round(x1 / w, 3), round(y1 / h, 3)],
        # 🔴 focus(fx,fy) の当たり＝インクのある範囲の中心（原画の比）
        fx=round((x0 + x1) / 2 / w, 3),
        fy=round((y0 + y1) / 2 / h, 3),
    )


def kind(m: dict) -> str:
    """full＝全画面に出せる（連続階調の写真）／panel＝額装パネル・暗幕の地にする（線図・図面）。"""
    return "full" if m["ink"] >= INK_FULL else "panel"


# ────────────────────────────────────────── 取ってくる
def _get_json(params):
    u = API + "?" + urllib.parse.urlencode(dict(params, format="json", formatversion="2"))
    r = urllib.request.Request(u, headers={"User-Agent": UA})
    return json.load(urllib.request.urlopen(r, timeout=60))


CACHE = Path(__file__).resolve().parent.parent / "analytics" / "materials" / "_thumbs"


def _get_bytes(url, cache_key=None):
    """⚠️ しきい値を決め直すたびに 59 点を落とし直さないよう、縮小版だけ手元に残す。"""
    if cache_key:
        CACHE.mkdir(parents=True, exist_ok=True)
        import hashlib
        p = CACHE / (hashlib.sha1(cache_key.encode()).hexdigest()[:16] + ".bin")
        if p.exists():
            return p.read_bytes()
    r = urllib.request.Request(url, headers={"User-Agent": UA})
    b = urllib.request.urlopen(r, timeout=120).read()
    if cache_key:
        p.write_bytes(b)
    return b


def commons_files(cat: str):
    """カテゴリのファイルを imageinfo つきで全部。⚠️ 直列＋待ち（並列だと 429）。"""
    titles, cont = [], None
    while True:
        p = dict(action="query", list="categorymembers", cmtitle=cat, cmtype="file", cmlimit="500")
        if cont:
            p["cmcontinue"] = cont
        d = _get_json(p)
        titles += [m["title"] for m in d["query"]["categorymembers"]]
        cont = d.get("continue", {}).get("cmcontinue")
        if not cont:
            break
        time.sleep(0.5)

    out = []
    for i in range(0, len(titles), 25):
        d = _get_json(dict(
            action="query", titles="|".join(titles[i:i + 25]), prop="imageinfo",
            iiprop="url|size|mime|extmetadata", iiurlwidth=str(THUMB_W),
            iiextmetadatafilter="LicenseShortName|Artist|Credit|ImageDescription|DateTimeOriginal",
        ))
        for pg in d["query"]["pages"]:
            ii = (pg.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})

            def g(k):
                return (em.get(k, {}) or {}).get("value", "")

            out.append(dict(
                title=pg["title"], w=ii.get("width", 0), h=ii.get("height", 0),
                mime=ii.get("mime", ""), lic=g("LicenseShortName"),
                artist=g("Artist"), desc=g("ImageDescription"), date=g("DateTimeOriginal"),
                url=ii.get("url", ""), thumb=ii.get("thumburl", ""),
            ))
        time.sleep(0.6)
    return out


def probe_commons(cat: str, min_w: int = 0):
    rows = commons_files(cat)
    for r in rows:
        if r["w"] < min_w or not r["thumb"]:
            r["skip"] = "too small" if r["w"] < min_w else "no thumb"
            continue
        try:
            im = Image.open(io.BytesIO(_get_bytes(r["thumb"], cache_key=r["title"])))
            r.update(measure(im))
            r["kind"] = kind(r)
        except Exception as e:                                    # noqa: BLE001
            r["skip"] = f"{type(e).__name__}: {e}"
        time.sleep(0.4)
    return rows


def probe_files(paths):
    rows = []
    for p in paths:
        p = Path(p)
        try:
            im = Image.open(p)
            w, h = im.size
            if w > THUMB_W:
                im = im.resize((THUMB_W, round(h * THUMB_W / w)), Image.LANCZOS)
            r = dict(title=p.name, w=w, h=h, url=str(p))
            r.update(measure(im))
            r["kind"] = kind(r)
        except Exception as e:                                    # noqa: BLE001
            r = dict(title=p.name, skip=f"{type(e).__name__}: {e}")
        rows.append(r)
    return rows


# ────────────────────────────────────────── 出す
def report(rows, min_w=1280):
    ok = [r for r in rows if "mid" in r]
    print(f"測れた {len(ok)} / {len(rows)} 点")
    photo = [r for r in ok if r["kind"] == "full"]
    line = [r for r in ok if r["kind"] == "panel"]
    big = [r for r in photo if r["w"] >= min_w]
    print(f"  全画面に出せる（full） {len(photo)}   うち幅{min_w}以上 **{len(big)}**")
    print(f"  額装パネル（panel）    {len(line)}")
    print()
    print(f"{'幅x高':>12}  {'種':<6} {'段':>4} {'mid':>5} {'ink':>5} {'band':>5}  題")
    for r in sorted(ok, key=lambda r: (r["kind"] != "full", -r["w"])):
        t = r["title"].replace("File:", "")[:66]
        print(f'{r["w"]}x{r["h"]:>5}  {r["kind"]:<6} {r["levels"]:>4} {r["mid"]:>5.2f} '
              f'{r["ink"]:>5.2f} {r["band"]:>5.2f}  {t}')
    for r in rows:
        if "skip" in r:
            print(f'  – 除外 {r["title"][:60]}: {r["skip"]}')


def hist(rows):
    """3つの候補の分布を並べて、いちばん広い切れ目を持つ量を選ぶ（しきい値はその真ん中）。"""
    for key, fmt, gapmin in (("levels", "{:.0f}", 20), ("ink", "{:.3f}", 0.05), ("mid", "{:.3f}", 0.05)):
        v = sorted(r[key] for r in rows if key in r)
        gaps = [(v[i + 1] - v[i], v[i], v[i + 1]) for i in range(len(v) - 1)]
        gaps.sort(reverse=True)
        print(f"\n== {key} ==  n={len(v)}  最小 {fmt.format(v[0])} 最大 {fmt.format(v[-1])}")
        for g, a, b in gaps[:3]:
            mark = " 🔴" if g >= gapmin else ""
            print(f"   切れ目 {fmt.format(g)}: {fmt.format(a)} → {fmt.format(b)}"
                  f"（真ん中 {fmt.format((a + b) / 2)}）{mark}")


def selftest():
    """陽性対照＝作った絵で「写真」と「図面」を必ず分ける。"""
    rng = np.random.default_rng(0)
    yy, xx = np.mgrid[0:400, 0:400]
    cases = []
    # ① ふつうの写真＝なだらかな階調＋粒子
    cases.append(("写真", np.clip(yy * 0.5 + xx * 0.1 + rng.normal(0, 8, (400, 400)), 0, 255)
                  .astype(np.uint8), "full"))
    # ② 🔴 暗い写真（Ten-ton crane 型）＝中間調は少ないがインクは多い。`mid` では図面と誤判定した
    cases.append(("暗い写真", np.clip(rng.normal(45, 22, (400, 400)), 0, 255).astype(np.uint8), "full"))
    # ③ 白地の図面＝線だけ。全画面に出すとまぶしくて線が消える
    ln = np.full((400, 400), 255, np.uint8)
    ln[::40, :] = 0
    ln[:, ::40] = 0
    cases.append(("図面", ln, "panel"))
    # ④ ⚠️ **既知の取りこぼし**＝雪原・砂漠のような地が白い写真は panel 側に落ちる。
    #    これは誤りではなく仕様（全画面に出すと白飛びする）だが、**捨てずに手で拾い直す**。
    #    ここで固定しておくのは、次に誰かが「写真なのに panel になる」と驚かないため。
    cases.append(("雪景色の写真（既知の取りこぼし）",
                  np.clip(rng.normal(228, 12, (400, 400)), 0, 255).astype(np.uint8), "panel"))

    ok = True
    for name, arr, want in cases:
        m = measure(Image.fromarray(arr))
        got = kind(m)
        flag = "OK" if got == want else "🔴 NG"
        ok &= got == want
        print(f'  {flag} {name}: 段={m["levels"]:>3} mid={m["mid"]:.2f} ink={m["ink"]:.2f} '
              f'→ {got}（期待 {want}）')
    # 空白帯：右半分が白紙の絵（4本目 tf_p076_bars.jpg の再現）
    hb = np.full((400, 400), 255, np.uint8)
    hb[100:300, 20:180] = 90
    m = measure(Image.fromarray(hb))
    flag = "OK" if m["band"] >= 0.45 and m["fx"] < 0.4 else "NG"
    ok &= flag == "OK"
    print(f'  {flag} 右半分が白紙: band={m["band"]:.2f} fx={m["fx"]:.2f}（期待 band>=0.45・fx<0.4）')
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commons")
    ap.add_argument("--files", nargs="*")
    ap.add_argument("--out")
    ap.add_argument("--min-w", type=int, default=1280)
    ap.add_argument("--hist")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest()
    if a.hist:
        return hist(json.load(open(a.hist, encoding="utf-8"))) or 0

    if a.commons:
        rows = probe_commons(a.commons, min_w=0)
    elif a.files:
        rows = probe_files(a.files)
    else:
        ap.error("--commons か --files か --hist か --selftest")

    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        json.dump(rows, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"→ {a.out}")
    report(rows, min_w=a.min_w)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
