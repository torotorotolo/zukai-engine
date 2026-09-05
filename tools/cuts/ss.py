# -*- coding: utf-8 -*-
"""4本目（サーフサイド）の章ファイルが共通で使う小道具。

■ 素材の名前（`ref/surfside/`。出どころは ref/CREDITS.md）
  技術的知見のスライドは **見出し帯（NIST ロゴ・英語の表題）を切り落として**ある。
  権利の無い部分（©2021 の写真・Google の画像・管財人の写真と原図）も**切ってから**置いてある。
  したがって章ファイルは「どこに寄るか」だけを書けばよい。

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  「画像のこの点を画面の中央に置きたい」と書けるように、点（0〜1）から xbias/bias を逆算する。
  🔴 画像の縦横比が要るので実物を開いて測る（推定で置かない）。
"""
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
W, H = 1920, 1080

# ── 技術的知見のスライド（ページ番号は動画のコマの右下） ──────────────
P003 = "surfside/tf_p003_model.jpg"      # 建物の3Dモデル＋寸法
P016_BODY = "surfside/tf_p016_body.jpg"  # 「余裕は決定的に小さかった」の箱＋赤黄の点の地図
P016_MAP = "surfside/tf_p016_map.jpg"    # 赤黄の点の地図だけ
P016_Q = "surfside/tf_p016_q.jpg"        # NIST の問い（横長の帯）
P029 = "surfside/tf_p029_model.jpg"      # 3D（西・中央・東、プールデッキ、街路駐車場）
P036 = "surfside/tf_p036_punch.jpg"      # パンチング・シアの線図（白地）
P048 = "surfside/tf_p048_deck.jpg"       # プールデッキの3D切り欠き（K/L/M・11.1/13.1）
P050_3D = "surfside/tf_p050_3d.jpg"      # 3週間前の3D
P050_GATE = "surfside/tf_p050_gate.jpg"  # 門の描き起こし（2段）
P052_3D = "surfside/tf_p052_3d.jpg"      # 1週間前の3D
P052_GATE = "surfside/tf_p052_gate.jpg"  # 門の描き起こし（3段）
P057_3D = "surfside/tf_p057_3d.jpg"      # 17時間前の3D
P057_MEMO = "surfside/tf_p057_memo.jpg"  # 手書きの目撃メモ
P058_3D = "surfside/tf_p058_3d.jpg"      # 9時間前の3D
P058_NOTE = "surfside/tf_p058_note.jpg"  # 付箋「Leak from the ceiling, not the pipe」
P062 = "surfside/tf_p062_summary.jpg"    # まとめ（3週間前・1週間前の吹き出し）
P065 = "surfside/tf_p065_garage.jpg"     # 9分前の駐車場3D
P067 = "surfside/tf_p067_deflect.jpg"    # 6〜7分前のたわみ（a/b/c）
P075 = "surfside/tf_p075_cover.jpg"      # かぶり ¾インチ／2インチ
P076 = "surfside/tf_p076_bars.jpg"       # 上端筋 4本→2本
P084 = "surfside/tf_p084_salt.jpg"       # 塩水浴と電極
P086 = "surfside/tf_p086_causes.jpg"     # 原因5点の箱と波括弧
P133 = "surfside/tf_p133_plan.jpg"       # 崩落範囲の平面図（左だけ）
P139 = "surfside/tf_p139_bars.jpg"       # 下端筋が抜ける線図（D E H I）
P174 = "surfside/tf_p174_corr.jpg"       # 鉄筋の腐食
P185 = "surfside/tf_p185_87park.jpg"     # 87パークの解析
P189 = "surfside/tf_p189_not.jpg"        # そうではなかったもの
P191 = "surfside/tf_p191_closing.jpg"    # Closing Remarks

# ── 記録映像から抜いた1コマ ───────────────────────────────
S_87PARK = "surfside/ss_b2_87park.jpg"
S_SIGN = "surfside/ss_b1_sign.jpg"

# ── p16 の地図の印の数（c407「印は1か所や2か所ではない」）───────────────
# 🔴 数えられる絵は数を合わせる（README §2）。目分量で置かず、`tf_p016_map.jpg` の赤と黄の
#    色の塊を機械で数えた（2026-09-05・連結成分 60px 以上・凡例の4つは除く）。
#      赤（severe）  … 点 8 ＋ 矢印 28 ＝ 36
#      黄（moderate）… 点 4 ＋ 矢印 15 ＝ 19
#    点＝柱とスラブのつなぎ目、矢印＝スラブの曲げ（凡例）。c407 は「印の多さ」を見せるので合算で出す。
#    ⚠️ 重なった印は1つに数えている。再計数は Vault の引き継ぎ 20260905d に手順。
P016_DOTS_RED = 36
P016_DOTS_YEL = 19


@lru_cache(maxsize=None)
def size_of(name):
    from PIL import Image
    with Image.open(HERE / "ref" / name) as im:
        return im.size


def focus(name, fx, fy, zoom=1.0, box=(W, H)):
    """画像の点 (fx, fy)（0〜1）が画面の中央に来る xbias / bias を返す。

    `fit()`：z = max(w/sw, h/sh)*zoom ／ 切り出し幅 cw = w/z ／ 左端 l = (sw-cw)*xbias。
    中央に置く → l = fx*sw - cw/2 → xbias = (fx*sw - cw/2) / (sw - cw)。0〜1 に丸める。
    """
    sw, sh = size_of(name)
    w, h = box
    z = max(w / sw, h / sh) * zoom
    cw, ch = min(sw, w / z), min(sh, h / z)
    xb = 0.5 if sw - cw < 1 else (fx * sw - cw / 2) / (sw - cw)
    yb = 0.5 if sh - ch < 1 else (fy * sh - ch / 2) / (sh - ch)
    return dict(xbias=round(min(1.0, max(0.0, xb)), 3),
                bias=round(min(1.0, max(0.0, yb)), 3), zoom=zoom)


def fb(cid):
    """動画を当てたカットの**ひかえの静止画**（footage が取れなかったときだけ画面に出る）。"""
    return f"surfside/fb_{cid}.jpg"
