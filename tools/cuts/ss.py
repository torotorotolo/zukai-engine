# -*- coding: utf-8 -*-
"""6本目（フランシス・スコット・キー橋 崩落）の章ファイルが共通で使う小道具。

■ 素材の名前（`ref/keybridge/`。出どころは `ref/CREDITS.md`・取り出しは `tools/keybridge_assets.py`）
  `kb_p<印字>_fig<図番>.png` … NTSB **MIR-25-40** のページを PNG に焼いたもの（32枚）
  `kb_pre_*` / `kb_bld_*.jpg` … Commons の写真（11点。**PD と CC BY だけ**）
  `fb_<cid>.jpg`              … 動画のひかえの静止画（動画のコマが取れたら動画が勝つ）

■ 🔴 名前の数字は「印字ページ」。PDF ページではない
  MIR-25-40 は **PDF ＝ 印字 ＋ 2**（前付が i〜xxii）。`kb_p114_fig50` は**印字 p.114**で、
  画面と出典に出るのも p.114。ここを混ぜると出典が2ページずれる。

■ 🔴 報告書のページは「紙いちめん」ではなく**図の矩形だけ**が出る
  `scene_jiko.TRIM_BY_PHOTO` に、`keybridge_assets.py bands` が測った箱が
  **32枚ぶん自動で入る**（`ref/keybridge/textbands.json`）。章ファイルで切り方を書かない。
  ⚠️ 箱は PDF の埋め込み画像の矩形（`page.get_image_bbox()`）＝**画素で探していない**ので、
     本文の段落を図と読み違える余地が無い。1ページに図が2つ在る p62 は
     「題のすぐ上の画像」を採ってある。

■ 🔴 全画面にするか額装パネルにするかは**縦横比で決める**（`kind()`）
  画面は 16:9（1.778）。図がそれより縦長だと、全画面は左右を切り落とす
  ＝ 図の端の凡例や寸法が消える。**1.55 未満は `panel=True`**。
  → 4本目で「切り出しを勘定に入れていなかった」ために尾部が枠外に出た件と同じ穴。
     `scene_jiko.photo_box` の注記を参照。

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  「画像のこの点を画面の中央に置きたい」と書けるように、点（0〜1）から xbias/bias を逆算する。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。

■ 5本目（SL-1）の中身は git の `778e514` にある（`git show 778e514:tools/cuts/ss.py`）。
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "keybridge"
W, H = 1920, 1080

# 画面の縦横比。これより縦長の図は額装パネルに回す（下限は 1.55＝12%の余裕）
SCREEN_AR = W / H
PANEL_AR = 1.55

_BANDS_FILE = REF / "textbands.json"
BANDS = (json.loads(_BANDS_FILE.read_text(encoding="utf-8"))
         if _BANDS_FILE.exists() else {})


def page(pr):
    """印字ページ番号から、そのページの PNG の名前を返す。

    🔴 章ファイルは**印字ページの数字だけ**を書く（`ss.page(114)`）。
       図番はここで台帳から引く。＝ 図番を手で書き写して取り違える余地を無くす。
    ⚠️ 台帳に無いページを呼んだら止まる（黙って別のページを出さない）。
    """
    for name, b in BANDS.items():
        if b["printed"] == pr:
            return f"keybridge/{name}.png"
    raise KeyError(f"印字 p{pr} は焼いていない"
                   f"（`tools/keybridge_assets.py` の PAGES に足して figs → bands）")


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
       （2026-09-08 に実際に起きた。`check_layout` は空の SPEC を調べて「✓ 全部おさまっている」
       を出した）。→ [[feedback-gates-blind-to-the-new-material]]
       切り出しの正本は `textbands.json` のほうなので、こちらを直接読む。
    """
    sw, sh = size_of(name)
    b = BANDS.get(name.split("/", 1)[-1].rsplit(".", 1)[0])
    if not b or not b.get("fig_box"):
        return sw, sh
    x0, y0, x1, y1 = b["fig_box"]
    return max(1, int(sw * (x1 - x0))), max(1, int(sh * (y1 - y0)))


def aspect(name):
    """切ったあとの縦横比（横÷縦）。"""
    w, h = trimmed_size(name)
    return w / h


def kind(name):
    """`dict(panel=True)` か `dict()` を返す。**縦横比で決める。目で決めない。**"""
    return dict(panel=True) if aspect(name) < PANEL_AR else dict()


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


def fb(cid):
    """動画を当てたカットの**ひかえの静止画**（footage が取れなかったときだけ画面に出る）。"""
    return f"keybridge/fb_{cid}.jpg"


# ── Commons の写真（`ref/CREDITS.md` の表と1対1）────────────────
# 🔴 **事故前**の橋。②の「事故前の写真は在庫に1点も無い」は誤りだった（⑤bで測り直した）。
PRE_1976 = "keybridge/kb_pre_1976.jpg"          # 1976-08-11 開通前の橋（The Evening Sun）
PRE_HARBOR07 = "keybridge/kb_pre_harbor07.jpg"  # 2007 内港から見た全景
PRE_NAVY12 = "keybridge/kb_pre_navy12.jpg"      # 2012 橋の下をくぐる艦（航路の上）
PRE_OAKHILL14 = "keybridge/kb_pre_oakhill14.jpg"  # 2014 橋に近づく艦
PRE_CATLETT22 = "keybridge/kb_pre_catlett22.jpg"  # 2022 橋の下を通る測量艇
PRE_DECK05 = "keybridge/kb_pre_deck05.jpg"      # 2005 橋の路面（車内から・4車線）
PRE_2019 = "keybridge/kb_pre_2019.jpg"          # 2019 全景 5416×3610
# ── 建設中（第1章）
BLD_HARBOR = "keybridge/kb_bld_harbor.jpg"      # 建設中の橋（NARA 546833）
BLD_PIERS = "keybridge/kb_bld_piers.jpg"        # 橋脚の工事（NARA 546837）
BLD_SUPPORTS = "keybridge/kb_bld_supports.jpg"  # 橋脚の支持部（NARA 546929）
BLD_CURTIS = "keybridge/kb_bld_curtis.jpg"      # カーティス湾の取付部（NARA 546911）


def report():
    """台帳の中身を1枚ずつ出す。

        python -c "import sys;sys.path.insert(0,'tools');import cuts.ss as ss;ss.report()"
    """
    for name, b in sorted(BANDS.items(), key=lambda kv: kv[1]["printed"]):
        n = f"keybridge/{name}.png"
        w, h = trimmed_size(n)
        print(f"  p{b['printed']:<4} 図{b['figure']:<3} {w:>5}x{h:<5} "
              f"縦横比 {aspect(n):.2f}  {'額装' if aspect(n) < PANEL_AR else '全画面'}"
              f"  {b['note']}")
