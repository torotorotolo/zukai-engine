# -*- coding: utf-8 -*-
"""11本目（1986年1月28日 チャレンジャー号 STS-51-L）の
章ファイルが共通で使う小道具。

**10本目（三豊百貨店）の中身は git の `46f11b3` にある**（`git show 46f11b3:tools/cuts/ss.py`）。
9本目（テネリフェ）は `e18b8f1`、8本目（コロンビア号）は `4c71bf0`、7本目（9.11）は `ae30d49`。

■ 素材の名前（`ref/ep11/`。選び方と出どころは `qa_out/ep11_assets.py` の `PICK`）
  `ep11/<欄の名>.jpg` … **76点**。台本 §4 が書いている欄の名前そのままが鍵。
  内わけ＝**写真 56点**（Commons の PD ＋ NASA画像庫 §105）
        ＋ **動く映像からの止め絵 20点**（うち8点は `fb_<カットID>` ＝動画のひかえ）
  🔴 台本の欄は90件。**14件はまだ当てが無い**（`ref/ep11/photo_picks.md` §3）。

■ ✅ この回は継承（ShareAlike）が**1点も無い**
  10本目は82点が CC BY-SA で「額装だけ」という縛りが要ったが、**11本目は0点**。
  🔴 **それは約束ではなく、`qa_out/ep11_assets.py` の `NG_LIC` が取り込みで止めている。**
  下の `check_share_alike()` が**焼く側でももう一度**照合する（二重の網）。
  → [[feedback-rules-need-gates]]／[[reference-cc-by-sa-unmodified-in-video]]

■ 🔴🔴 この回も**報告書から取り出した図を画面に出さない**（`BANDS` が空）
  ロジャース委員会報告書の図版は**英字がビットマップに焼き込まれている**
  （→ [[reference-report-figures-have-burned-in-english]]）。
  下敷きは寸法と位置を取るためだけに使い、**`titan_fig` の型で描き直して日本語にする**。
  ⚠️ だから `page()` は呼べない。呼んだら止まる。

■ 🔴🔴 動く映像は**額装パネルで置く。全画面にしない**
  配布されているのは 720x480（SAR 8:9 ＝正方画素 640x480）で、1920 幅に伸ばすと 3倍になる。
  `vid()` は必ず `panel=True` を付ける。
  🔴 さらに**額入り（ピラーボックス）のコマがある**＝器は 720x480 のままなのに
     実効の絵が 470x479（幅65%）しかない。**器を見る門番は1本も鳴らない。**
     → `box_trim()` が `ref/ep11/boxes.json`（1秒おきに全数測った地図）から切り出しを出す。
     ⚠️ **帯ごとではなくコマごとに変わる**（同じ帯で58%と97.9%が隣り合う）。
     → [[feedback-container-labels-lie-about-the-picture]]

■ 🔴 人が写る点の扱い（この回）
  乗員7人・委員・NASAの管理職は**公的な任務の人**＝顔を出してよい。
  私人（遺族・見物人）は写っていない＝`NEEDS_MASK` は空。
  ⚠️ **遺体・負傷は1点も採っていない。**→ [[feedback-jiko-photo-people-policy]]

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep11"
W, H = 1920, 1080

# 画面の縦横比。これより縦長／横長の図は額装パネルに回す。
# 🔴 上限と下限は対。片側だけにすると粗が反対側へ移る（[[feedback-kinsoku-needs-both-ends]]）。
SCREEN_AR = W / H
# 🔴 2026-09-21（11本目 ⑤c-2）：**この回の76点で取り直した**
#    （→ [[feedback-per-episode-constants-go-stale]]。10本目の 4/3 を写さない）。
#    `python qa_out/ep11_assets.py panel` の実測に**はっきりした切れ目**があった：
#      … AR 1.250 crew_portrait（29.7%切れる）／AR 1.238 past_launch／AR 1.235 accident_breakup（30.6%）
#      ── ここで 12.5ポイント飛ぶ ──
#      AR 1.011 oring_erosion（43.1%切れる）／AR 1.006 ssme_salvage／frustum_compare …
#    ＝ 2つの族の境目（4:3〜5:4 の普通の写真 と、GPN-2004 の**ほぼ正方形**の残骸写真）。
#    その中点を採る。⚠️ 10本目の 1.3333 をここに置くと、**普通の4:3写真まで額装に回る**。
PANEL_AR = 1.12                      # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝2.82。これ超＝横長すぎ

# 🔴 報告書の図版は使わない（上の■）。空のまま。`page()` を呼ぶと止まる。
BANDS: dict[str, dict] = {}

# 画素で測った切り出し。⚠️ **⑤cで原寸を見てから足す**（推定で置かない）。
TRIM: dict[str, tuple] = {}


def page(pr):
    """報告書の頁から図を切り出す（この回は使わない）。"""
    raise RuntimeError(
        "11本目は報告書の図版を画面に出さない（英字が焼き込まれている）。"
        "titan_fig の型で描き直すこと → reference-report-figures-have-burned-in-english")


def P(name):
    """欄の名前 → `ref/` から見た写真のパス。"""
    return f"ep11/{name}.jpg"


def fb(cid):
    """動く映像を当てたカットの**ひかえの静止画**（`footage.USE` が取れなかったとき）。

    ⚠️ 取れなかったことは**黙って静止画に落ちる**＝⑥で `✓ 切り出し完了 N/N` を数える
    → [[feedback-fetch-failure-falls-back-to-a-still]]
    """
    return f"ep11/fb_{cid}.jpg"


# ══════════════════════════════════════════════════════════
#  ✅ 継承（ShareAlike）は1点も入れない ── 焼く側でももう一度照合する
# ══════════════════════════════════════════════════════════
#   取り込み側（`qa_out/ep11_assets.py` の `NG_LIC`）で止めてあるが、
#   **あとから手で1点足したときに素通りする**ので、ここでも当てる（二重の網）。
#   ⚠️ `assets.json` が読めなければ**止める**（0点にして素通りさせない）
#   → [[feedback-parsers-fail-closed]]
@lru_cache(maxsize=None)
def _assets():
    p = REF / "assets.json"
    if not p.exists():
        raise RuntimeError(
            "ref/ep11/assets.json が無い（`python qa_out/ep11_assets.py info`）。"
            "権利を確かめずに焼かない → feedback-parsers-fail-closed")
    return json.loads(p.read_text(encoding="utf-8"))


def check_share_alike(spec):
    """継承つきの点を当てているカットを挙げる（空なら合格）。"""
    db = _assets()
    bad = []
    for cid, s in sorted(spec.items()):
        ph = s.get("photo")
        if not ph or not ph.startswith("ep11/"):
            continue
        r = db.get(Path(ph).stem)
        lic = str((r or {}).get("lic", "")).upper().replace("-", " ")
        if "SA" in lic.split():
            bad.append(f"{cid}＝{ph}（{r['lic']}）: この回は継承つきを入れない")
    return bad


# ══════════════════════════════════════════════════════════
#  🔴🔴 使わない写真（シートで見て落とした。**使うと `cuts` の読み込みで止まる**）
# ══════════════════════════════════════════════════════════
#   `cuts/__init__.py` が SPEC を組んだあとに照合し、当たれば RuntimeError にする
#   ＝ 門番を1本足す代わりに、**全部の門番が落ちる**形で止める（黙って焼けない）。
NG_PHOTOS: dict[str, str] = {
    # 🔴 まだ空です。⑤c-3 のシートで落とした点をここに足します。
    #    ⚠️ 「まだ見ていない」だけで、「危険が無い」ではありません。
}

# 🔴 元画像そのものを直してから焼く点。この回は**空**。
#    乗員・委員・管理職は公的な任務の人＝顔を出してよい。私人は1点も写っていない。
#    ⚠️ **`blur=` は書けるように見えて誰も読まない**（10本目で私人の顔が素のまま焼けた）。
#       隠すなら元画像を直し、`ref/ep11/masked.json` に md5 を記録する。
#    → [[feedback-settings-may-not-reach-the-picture]]／[[feedback-jiko-photo-people-policy]]
NEEDS_MASK: dict[str, str] = {}


@lru_cache(maxsize=None)
def size_of(name):
    from PIL import Image
    with Image.open(HERE / "ref" / name) as im:
        return im.size


@lru_cache(maxsize=None)
def trimmed_size(name):
    """切り出しを当てたあとの寸法（画素）。切っていなければ原寸。

    ⚠️ **`scene_jiko` を import しない。** `scene_jiko` は起動時に `cuts` を読むので、
       ここから import すると循環参照になり、章ファイルが**丸ごと黙って読めなくなる**
       （2026-09-08 に実際に起きた。`check_layout` は空の SPEC を調べて
       「✓ 全部おさまっている」を出した）→ [[feedback-gates-blind-to-the-new-material]]
    """
    sw, sh = size_of(name)
    t = TRIM.get(name)
    if t:
        x0, y0, x1, y1 = t
        return max(1, int(sw * (x1 - x0))), max(1, int(sh * (y1 - y0)))
    b = BANDS.get(name.split("/", 1)[-1].rsplit(".", 1)[0])
    if not b or not b.get("fig_box"):
        return sw, sh
    x0, y0, x1, y1 = b["fig_box"]
    return max(1, int(sw * (x1 - x0))), max(1, int(sh * (y1 - y0)))


def aspect(name):
    """切ったあとの縦横比（横÷縦）。"""
    w, h = trimmed_size(name)
    return w / h


def crop_loss(name):
    """全画面にしたとき、絵の**何割が枠の外へ出るか**（0〜1）。額装なら 0。"""
    a = aspect(name)
    return 1 - (a / SCREEN_AR if a < SCREEN_AR else SCREEN_AR / a)


# 🔴 2026-09-21（⑤c-2）：**画素が足りない点も額装に回す。**
#    `PANEL_AR` は縦横比しか見ないので、`smoke_puffs`（751×523・AR 1.436）のような
#    **横長だが小さい**点が全画面に回り、1920 幅へ 2.6倍に伸びていた。
#    制作ルールの「1ビットのスキャンは額装パネル（横1200px上限）」と同じ筋＝
#    **伸ばせないものを伸ばさない。**
#    ⚠️ 上限と下限は対（[[feedback-kinsoku-needs-both-ends]]）＝縦横比と画素の両方で見る。
MIN_FULL_W = 1280        # 全画面にしてよい最小の幅（②の網の敷居と同じ値）


def kind(name):
    """`dict(panel=True)` か `dict()` を返す。**縦横比と画素で決める。目で決めない。**

    ⚠️ 縦長すぎ（< PANEL_AR）だけでなく**横長すぎ（> WIDE_AR）も額装**に回す。
    ⚠️ さらに**幅が足りない点も額装**（上の MIN_FULL_W）。
    """
    a = aspect(name)
    w, _ = trimmed_size(name)
    return (dict(panel=True)
            if (a < PANEL_AR or a > WIDE_AR or w < MIN_FULL_W) else dict())


def focus(name, fx, fy, zoom=1.0, box=(W, H)):
    """画像の点 (fx, fy)（0〜1・**切ったあとの絵の中での位置**）を画面中央に置く寄せ。

    `fit()`：z = max(w/sw, h/sh)*zoom ／ 切り出し幅 cw = w/z ／ 左端 l = (sw-cw)*xbias。
    中央に置く → l = fx*sw - cw/2 → xbias = (fx*sw - cw/2) / (sw - cw)。0〜1 に丸める。
    """
    sw, sh = trimmed_size(name)
    w, h = box
    z = max(w / sw, h / sh) * zoom
    cw, ch = min(sw, w / z), min(sh, h / z)
    xb = 0.5 if sw - cw < 1 else (fx * sw - cw / 2) / (sw - cw)
    yb = 0.5 if sh - ch < 1 else (fy * sh - ch / 2) / (sh - ch)
    return dict(xbias=round(min(1.0, max(0.0, xb)), 3),
                bias=round(min(1.0, max(0.0, yb)), 3), zoom=zoom)


# ══════════════════════════════════════════════════════════
#  動く映像
# ══════════════════════════════════════════════════════════
@lru_cache(maxsize=None)
def _clips():
    p = REF / "clips.json"
    if not p.exists():
        raise RuntimeError("ref/ep11/clips.json が無い（`python ref/ep11/make_clips.py`）")
    return json.loads(p.read_text(encoding="utf-8"))


@lru_cache(maxsize=None)
def _boxes():
    p = REF / "boxes.json"
    if not p.exists():
        raise RuntimeError("ref/ep11/boxes.json が無い（`python ref/ep11/sweep_box.py`）")
    return json.loads(p.read_text(encoding="utf-8"))


def box_trim(clip, t, tol=2):
    """🔴🔴 **そのコマの**額（ピラーボックス）を追い出す `trim`。無ければ None。

    器は 720x480 のままでも、実効の絵は 470x479 しかないコマがある。
    **帯ごとではなくコマごとに変わる**（同じ帯で58%と97.9%が隣り合う実測）。
    だから `bars_trim(clip)` のような**帯に1つの値**では足りない。
    → `ref/ep11/boxes.json`（1秒おきに全数測った地図）からそのコマの値を引く。

    🔴 **`zoom` で追い出してはいけない。**`fit()` の zoom は縦横を同じ率で切るので、
       額装で 1/PILLAR を掛けると**上下も同じ率だけ落ちる**。
    """
    e = _boxes().get(clip)
    if not e:
        raise RuntimeError(f"boxes.json に帯 {clip!r} が無い（fail closed）")
    step = e.get("step") or 1.0
    row = min(e["frames"], key=lambda r: abs(r["t"] - t))
    if abs(row["t"] - t) > step:
        raise RuntimeError(f"{clip} の {t}秒を測った行が無い（fail closed）")
    W0 = _clips()[clip]["w"]
    H0 = _clips()[clip]["h"]
    if row["w"] >= W0 - tol and row["h"] >= H0 - tol:
        return None
    x0, y0 = row["x"] / W0, row["y"] / H0
    return (round(x0, 4), round(y0, 4),
            round((row["x"] + row["w"]) / W0, 4), round((row["y"] + row["h"]) / H0, 4))


def vid(cid, pw, clip=None, t=None, **kw):
    """動く映像のカット（額装パネル＋ひかえの静止画）を1行で書く。

    🔴 **必ず額装パネル**（`panel=True`）。640x480 を 1920 幅に伸ばすと3倍になる。
    🔴 `clip` と `t` を渡すと、**そのコマの額**を `boxes.json` から引いて `trim` にする。
    """
    t_ = kw.pop("trim", None)
    if t_ is None and clip is not None and t is not None:
        t_ = box_trim(clip, t)
    d = dict(photo=fb(cid), panel=True, pw=pw, **kw)
    if t_:
        d["trim"] = t_
    return d


def still(name, clip, t, **kw):
    """動く映像から抜いた**止め絵**（`footage.USE` に入れないカット）。

    動画にすると 0.25〜0.45倍速＝ほぼ静止になる欄を、素直に止め絵で置く。
    **実写の数は変わらない。**→ `ref/ep11/photo_picks.md` §2-2
    """
    t_ = kw.pop("trim", None) or box_trim(clip, t)
    d = dict(photo=P(name), panel=True, **kw)
    if t_:
        d["trim"] = t_
    return d
