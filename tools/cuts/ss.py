# -*- coding: utf-8 -*-
"""5本目（SL-1）の章ファイルが共通で使う小道具。

■ 素材の名前（`ref/sl1/`。出どころは `ref/CREDITS.md`・取り出しは `tools/sl1_assets.py`）
  報告書のページは **PDF を丸ごと PNG に焼いたもの**（切っていない）。
  焼き込みの英字を逃がすのは `scene_jiko.TRIM_BY_PHOTO`（切る場所はカットでなく**ファイル**に紐づける）。
  → [[reference-report-figures-have-burned-in-english]]

■ 🔴 名前の数字は「印字ページ」。PDF ページではない
  IDO-19302 は **PDF ＝ 印字 ＋ 11**。`ido_p016_fig14` は**印字 p.16**（PDF 27）で、
  画面と出典に出るのも p.16。ここを混ぜると出典が11ページずれる。

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  「画像のこの点を画面の中央に置きたい」と書けるように、点（0〜1）から xbias/bias を逆算する。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ 余りが小さいと 0/1 に丸まって端に寄る（4本目 PR-07 の実例）。`check_layout` では見えない。

■ 4本目（サーフサイド）の中身は git の `4e4c1fb` にある。
"""
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
W, H = 1920, 1080

# ── IDO-19302（アイダホ支所の報告書・208ページ）──────────────────
IDO_VII = "sl1/ido_pvii_foreword.png"    # 前書き。「原因は扱わない」と断る段落
IDO_P4 = "sl1/ido_p004_night.png"        # 夜間指示書の9項目
IDO_P13 = "sl1/ido_p013_fig11.png"       # Fig 1.1 試験場の全体図
IDO_P14 = "sl1/ido_p014_fig12.png"       # Fig 1.2 SL-1 区域の配置図
IDO_P15 = "sl1/ido_p015_fig13.png"       # Fig 1.3 炉建屋の断面
IDO_P16 = "sl1/ido_p016_fig14.png"       # Fig 1.4 炉の縦断面
IDO_P17 = "sl1/ido_p017_fig15.png"       # Fig 1.5 位置の番号と炉心の配置
IDO_P18 = "sl1/ido_p018_fig16.png"       # Fig 1.6 十字型の制御棒
IDO_P19 = "sl1/ido_p019_fig17.png"       # Fig 1.7 燃料要素
IDO_P20 = "sl1/ido_p020_fig18.png"       # Fig 1.8 制御棒の駆動
IDO_P21 = "sl1/ido_p021_log.png"         # 運転日誌／時系列の最初のページ
# 🔴 下の5枚は⑤bで足した。**記録映画に無い主題の欄**を、そのカットの出典が指す
#    報告書のページに落とすため（代用ではなく根拠を出す）。→ `ref/sl1/SHOTS_INDEX.md`
IDO_P22 = "sl1/ido_p022_fire.png"        # 消防の到着・空気呼吸器の受け渡し
IDO_P23 = "sl1/ido_p023_ctrl.png"        # 制御室で見たもの・階段の線量
IDO_P90 = "sl1/ido_p090_found.png"       # 2人を見つけた／3人目の記述
IDO_P91 = "sl1/ido_p091_rescue.png"      # 救助の8分・救急車と落ち合う
IDO_P96 = "sl1/ido_p096_ship.png"        # 棺の札と輸送
IDO_P35 = "sl1/ido_p035_fig21.png"       # Fig 2.1 事故後の運転室
IDO_P36 = "sl1/ido_p036_fig22.png"       # Fig 2.2 事故後の運転室
IDO_P95 = "sl1/ido_p095_lead.png"        # 鉛で包み金属の帯で締めた記述
IDO_P100 = "sl1/ido_p100_kingston.png"   # キングストンでの記述
IDO_P101 = "sl1/ido_p101_deleted.png"    # 🔴 本文が2行だけの白紙ページ
IDO_P103 = "sl1/ido_p103_fig51.png"      # Fig 5.1 運転階の床

# ── IDO-19311（回収作業の最終報告・GE）─────────────────────
I11_ABST = "sl1/i11_p004_abstract.png"   # 要旨 ii（20インチ引き抜き）
I11_S41 = "sl1/i11_p019_sec41.png"       # I-5 §4.1「はっきりした証明は無い」

# ── ANL-6692（ALPR 設計の回顧的検討）／AEC 調査委員会報告／官報 ──────
ANL_COVER = "sl1/anl_p001_cover.png"     # 表紙
ANL_VF = "sl1/anl_p038_vf.png"           # 印字 p.36 §VIII-F
AEC_COVER = "sl1/aec_p001_cover.png"     # AEC 調査委員会報告の表紙（43ページ）
FR_GDC = "sl1/fr_p3258_gdc.png"          # 官報 3258ページ 一般設計基準 25・26

# ── HAER No. ID-33-D（米議会図書館の記録写真・5200px 超）────────────
# 🔴 **年代で仕分ける**（台本 §5-1 の5）。1957〜1961年を第1・2章に、1968年以降を第8・9章に。
HAER_52 = "sl1/haer_52.jpg"    # 1957-09-05 炉建屋の支柱
HAER_53 = "sl1/haer_53.jpg"    # 1957-09-20 鋼の外殻が支柱の上に立ち上がる
HAER_70 = "sl1/haer_70.jpg"    # 1957-10-31 支援棟 ARA-602 が建つ
HAER_56 = "sl1/haer_56.jpg"    # 1957-11-19 建屋の内側・炉容器を見る
HAER_65 = "sl1/haer_65.jpg"    # 1958-03-21 運転階の水浄化系の配管
HAER_64 = "sl1/haer_64.jpg"    # 1958 運転階（INEEL 58-1360）
HAER_67 = "sl1/haer_67.jpg"    # 1958-04-23 支援棟から運転階へ続く覆いのある階段（外観）
HAER_73 = "sl1/haer_73.jpg"    # 1958-05-22 完成間近の空撮
HAER_69 = "sl1/haer_69.jpg"    # 1958-06-24 運転階でタービン発電機を据える
HAER_74 = "sl1/haer_74.jpg"    # 1959-08-08 制御盤の前に立つ人たち
HAER_76 = "sl1/haer_76.jpg"    # 🔴 1961-01-06 爆発後・遮蔽した運転席のクレーンで扉を開けようとする
HAER_78 = "sl1/haer_78.jpg"    # 1982 空撮（守衛所が手前）
HAER_15 = "sl1/haer_15.jpg"    # 跡地・管理棟 ARA-613（解体準備中）
HAER_14 = "sl1/haer_14.jpg"    # 跡地・遠景（管理棟とクレーン）


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


# 報告書の本文ページで、文字が入っている横の帯（実測。左右の余白を除いた割合）
TEXT_X0, TEXT_X1 = 0.13, 0.87


def text_focus(name, fy, zoom=1.35):
    """報告書の**本文ページ**に寄る（縦だけ動かし、横は必ず全幅を入れる）。

    🔴 4本目の⑤cで5件出た「行が左端で語の途中から始まる」を、式で止める。
       切り出し幅 cw = sw/zoom。本文は x {TEXT_X0}〜{TEXT_X1} にあるので、
       **1/zoom ≥ TEXT_X1 − TEXT_X0** でなければ、どこに寄せても行が切れる。
       → [[feedback-gates-dont-see-text-burned-into-the-picture]] の3
    ⚠️ これを守ると zoom は 1.35 が上限（0.74 ≧ 0.74）。もっと寄りたいときは
       **ファイルを切る**（`scene_jiko.TRIM_BY_PHOTO`）。寄せでは逃げられない。
    """
    need = TEXT_X1 - TEXT_X0
    if 1.0 / zoom < need - 1e-9:
        raise ValueError(
            f"{name}: zoom={zoom} だと切り出し幅が本文の {need:.2f} に足りない"
            f"（1/zoom={1 / zoom:.3f}）。行頭が切れる。zoom ≦ {1 / need:.2f} にする")
    return focus(name, 0.5, fy, zoom)


def fb(cid):
    """動画を当てたカットの**ひかえの静止画**（footage が取れなかったときだけ画面に出る）。"""
    return f"sl1/fb_{cid}.jpg"
