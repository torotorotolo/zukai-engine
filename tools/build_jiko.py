# -*- coding: utf-8 -*-
"""226カットの合成。図解レイヤーとPD写真から30fpsのコマを作る。

■ 動きの設計（映像ルール4：**3秒以上の静止を禁止**）
  段（`{cid}_aN`）は**その段の持ち時間いっぱいをかけて左→右に描かれる**。
  持ち時間 ＝ その段が出てから次の段が出るまで（最後の段はカット終わりまで）。
  → カットのどの瞬間にも「描いている途中の段」が必ず1つある＝**静止区間が構造的に無い**。
  テスト映像のようにカットごとに MOTION を手で書く必要がなくなった
  （手書きは図を動かすたびに直し忘れる。実際 c3 のワイプ範囲で1度やっている）。

  🔴 **動きには必ず情報を運ばせる。装飾の動きは入れない。**
     スライドイン・回転・弾む出方・意味のない拡大はバラエティの文法なので使わない。
  🔴 2026-09-23（12本目から・カズヤくん決定＝ルール統合版 §5b-17）：次の3つだけ解禁した。
     ① 転換＝章の変わり目の暗転（scene_jiko.chapter_tail）→ 章の扉（scene_jiko.CARD_SEC）
        ／同じ章の写真どうしのディゾルブ（DISSOLVE）＝「場面が変わった」を運ぶ
     ② カメラの型＝パン・引き・2点移動（SPEC の cam=）＋緩急（ease()）＝「どこを見るか」を運ぶ
     ③ 閃光＝**爆発の瞬間だけ**（SPEC の flash=）＝乗組員が見た「空が光る」そのもの
     どれも SPEC に書いたカットにしか効かない（書かなければ11本目までと同じ絵）。

■ 2つのモード（34分＝61,300コマあるので分ける）
  qa   … カットごとの検品用の静止画と拡大図だけを作る。**5巡以上の精査はこちらで回す**
  full … mp4 まで作る。カット単位で並列に焼き、最後に連結する

■ 検品用の出力
  `out/jiko/qa/` に**クラウドで焼いた実物**を書き出す。
  ローカルのフォントとクラウドのフォントで折返し位置が変わった実績があるので、
  検品はここに出たものだけを見る。
"""
import math
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageChops, ImageDraw

import scene_jiko as S
import jiko_style as J

FPS = 30
OUT = S.HERE / "out" / "jiko"
SEG = OUT / "seg"
QA = OUT / "qa"

# 🔴 r8 の目視：NTSB が研究室で撮った標本写真は元が低コントラストで、
#    デュオトーンにすると灰色の塊になって形が読めない。
#    r9 の目視：報告書から取り出した標本写真も、青背景＋緑の接着剤という配色なので
#    デュオトーンにすると全体が同じ灰色に寄る。空隙の黒がいちばん見せたいところなので立てる。
# 🔴 2026-08-04：**1本目のカットID直書き13件を空にした。**
#    `--report` にも出てこない**隠れた題材依存**で、残すと123便の関係ない
#    カットで勝手にコントラストが持ち上がる。中身は git の `57e6c16` にある。
# ⚠️ 123便の報告書スキャンは取り出しの時点で
#    「長辺1200pxへ縮小＋ぼかし0.7」でディザをほどいてあるので、
#    autocontrast をかけると**ほどいた中間調がまた2値に寄る**。既定では使わない。
# 🔴 2026-09-20（10本目 ⑤c'）：`c810`（行方不明者の掲示板）だけ持ち上げる。
#    私人の顔と名前を隠すためにモザイクを掛けてあり（`qa_out/ep10_remask.py`）、
#    枡の中が平らになるぶん**デュオトーンで全体が同じ明るさに寄る**。
#    実測（デュオトーンに落として1920幅）：貼り紙の輪郭 36.14 →（boost）**41.57**。
#    ⚠️ 題材依存なので、次の回に移るときは**ここを空にする**
#      （`project-jiko-rules-index` §0b の「題材を替えるとき空にする場所」）。
# 🔴 2026-09-21（11本目 ⑤c-2）：**空にした**（§0b の10か所目）。10本目の `{"c810"}` は
#    掲示板のモザイクを持ち上げるためのもので、11本目の c810 は別の絵。
BOOST = set()
# 段を「描き終える」までにかける時間。
# 🔴 割合で決めると長いカットで破綻する。0.70 にしたら尺12秒のカットで
#    3.8秒止まって「3秒以上の静止禁止」を割った（実測7カット）。
#    **止まる時間の側を 2.2 秒で頭打ちにする**のが正しい。
STILL_MAX = 2.2        # 段が出そろってから次の段までに許す静止（秒）
# 骨格（lab）を描くのにカットの何割を使うか。型が labk を返せば、そちらが優先。
LAB_K = 0.30


def draw_span(w):
    """持ち時間 w のうち、描画にかける秒。読む間を残しつつ静止を作らない。"""
    # 割合を混ぜると長い段でまた破綻する（0.75 だと尺12.9秒で3.15秒止まった）。
    # **止まる時間そのもの**を STILL_MAX で固定するのが正しい。
    return min(w * 0.9, max(0.6, w - STILL_MAX))


def L(name):
    return Image.open(OUT / f"{name}.png").convert("RGBA")


def duotone(im, dark, light, boost=False):
    """写真を配色に合わせる。生の白黒のまま置くと図解から浮く。"""
    g = im.convert("L")
    if boost:
        from PIL import ImageOps
        g = ImageOps.autocontrast(g, cutoff=(1, 6))
    d = tuple(int(dark[i:i + 2], 16) for i in (1, 3, 5))
    l = tuple(int(light[i:i + 2], 16) for i in (1, 3, 5))
    lut = []
    for c in range(3):
        lut += [int(d[c] + (l[c] - d[c]) * (v / 255.0)) for v in range(256)]
    return g.convert("RGB").point(lut).convert("RGBA")


def tone(ph, cut, meta):
    """写真の色の扱い。既定はデュオトーン（図解から浮かせない）。

    🔴 2026-09-05（4本目）：**NIST のスライドは色に意味がある**
       （p16 の赤＝重い不足・黄＝中くらい／p75 の黄色い線＝鉄筋の深さ／p133 の青＝崩れた範囲／
        p65 の柱の緑・黄・赤）。デュオトーンにすると「黄色い線が2本」と言う声の下で
       灰色の線が出て、**図が声と食い違う**。
       → カット側が `color=0.0〜1.0` を書くと、そのぶん原色を残す（残りはデュオトーン）。
       ⚠️ 全カットに色を残さない。実写と、色が意味を持たないスライドは今までどおり沈める。
    """
    keep = float((meta.get(cut) or {}).get("color", 0.0) or 0.0)
    # 🔴 12本目から：デュオトーンの2色は**その章の色**（jiko_style.PALETTES。navy＝今までと同じ2色）
    pal = J.palette((meta.get(cut) or {}).get("pal"))
    duo = duotone(ph, pal["BG2"], pal["DUO_L"], boost=cut in BOOST)
    if keep <= 0.001:
        return duo
    raw = ph.convert("RGBA")
    return Image.blend(duo, raw, min(1.0, keep))


# ── ★実写「動画」を差し込む（2026-08-01 追加） ─────────────────
# 🔴 コマは `python tools/footage.py fetch` が out/jiko/foot/<cid>/ に切り出しておく。
#    **無ければ静止画に落ちる**ので、切り出さないまま焼いてもパイプラインは壊れない。
FOOT = OUT / "foot"
_FOOT_MISS = set()
try:
    import footage as _FO
    _FOOT_USE = _FO.USE
except Exception:                                        # noqa: BLE001
    _FO = None
    _FOOT_USE = {}


def foot_frame(cut, t):
    """そのカットに動画が当ててあれば、その時刻のコマを返す。無ければ None。"""
    if cut in _FOOT_MISS:
        return None
    d = FOOT / cut
    p = d / f"{int(round(t * FPS)):05d}.jpg"
    if not p.exists():
        # 尺の端でコマが足りないときは最後のコマで持たせる
        got = sorted(d.glob("*.jpg")) if d.is_dir() else []
        if not got:
            _FOOT_MISS.add(cut)
            # 🔴 2026-08-02：動画を当てているのにコマが無いと**黙って静止画に落ちる**。
            #    r16 で archive.org が 500 を返したとき、失敗したのに ✓ に見えた。
            #    動画のカットが 3 → 10 に増えたので、落ちたことが必ずログに出るようにする。
            if cut in _FOOT_USE:
                print(f"  ⚠️ {cut}: 動画のコマが無いので**静止画に落ちた**"
                      f"（tools/footage.py が取れていない）", flush=True)
            return None
        p = got[-1]
    return Image.open(p).convert("RGB")


def stretch(src, levels):
    """階調を伸ばす。**中身は足さない・消さない。濃淡だけを強める。**

    🔴 2026-08-09（カズヤくん承認）：捜索海図は**線と紙の明るさの差が
       255階調中わずか12〜16**（実測：紙の中央部 median 182〜185 / p5 166〜172）。
       素のまま出すと、鉛筆の航跡も書き込まれた船名も画面でまったく見えない。
       第5章はその海図が主役なので、**読めないままでは章が成立しない。**
    ⚠️ 引用の要件④「改変しない」は**中身を変えないこと**であって、
       すでに `trim`（切り抜き）を掛けているのと同じ範囲の処理として扱う。
       出典の行に「濃淡補正」と出す（`scene_jiko.credit_of`）。
    """
    lo, hi = levels
    if not 0 <= lo < hi <= 255:
        raise ValueError(f"levels が不正です: {levels}")
    lut = [max(0, min(255, round((v - lo) * 255 / (hi - lo)))) for v in range(256)]
    return src.point(lut * len(src.getbands()))


def load_photo(name, box, trim=None, levels=None):
    """写真は箱の2倍程度まで先に落としておく（4GBのPCでも開けるように）。

    trim   … (x0, y0, x1, y1) を**元画像に対する割合**で渡すと、先に切り落とす。
             報告書の英字ラベルを画面に出さないために使う（`S.PHOTO_TRIM`）。
    levels … (lo, hi) を渡すと**階調を伸ばす**（`S.PHOTO_LEVELS`）。
             ⚠️ 切る前・縮める前に掛ける。あとから掛けると、縮小で平均化された
               画素に対して伸ばすことになり、測った値と合わなくなる。
    """
    src = Image.open(S.HERE / "ref" / name).convert("RGB")
    if levels:
        src = stretch(src, levels)
    if trim:
        w, h = src.size
        x0, y0, x1, y1 = trim
        src = src.crop((round(x0 * w), round(y0 * h),
                        round(x1 * w), round(y1 * h)))
    lim = box[2] * 2
    if src.width > lim:
        src = src.resize((lim, round(src.height * lim / src.width)), Image.LANCZOS)
    return src


def fit(src, box, k=0.0, bias=0.5, xbias=0.5, zoom=1.0):
    """箱を覆うように切り出す。k>0 でゆっくり寄る。bias は縦方向の寄せ。

    xbias / zoom … 地に敷くとき、写真の焼き込み（ROV の深度表示など）を
    画面外へ追い出すために使う。既定（0.5 / 1.0）は今までと同じ動き。
    """
    _, _, w, h = box
    sw, sh = src.size
    z = max(w / sw, h / sh) * zoom * (1.0 + 0.055 * k)
    cw, ch = min(sw, w / z), min(sh, h / z)
    l, t = (sw - cw) * xbias, (sh - ch) * bias
    crop = src.crop((round(l), round(t), round(l + cw), round(t + ch)))
    return crop.resize((w, h), Image.LANCZOS)


def fade(layer, a):
    if a <= 0.001:
        return None
    if a >= 0.999:
        return layer
    o = layer.copy()
    o.putalpha(o.getchannel("A").point(lambda v: int(v * a)))
    return o


def over(fr, layer, a=1.0):
    p = fade(layer, a)
    if p:
        fr.alpha_composite(p)
    return fr


_GRAD = {}


def _grad(soft):
    if soft not in _GRAD:
        g = Image.new("L", (soft, 1))
        g.putdata([255 - round(255 * i / max(1, soft - 1)) for i in range(soft)])
        _GRAD[soft] = g.resize((soft, S.H))
    return _GRAD[soft]


def wipe(fr, layer, k, soft=90, span=None):
    """レイヤーを**左から右へ**現す。図が「描かれていく」動きになる。

    🔴 ワイプは**図が実際に占める x 範囲**で進める。画面全幅を横断させると
       travel の大半が空白に費やされ、図が動き出すのがカットの後半になる
       （テスト映像11巡目に c3 で実際に起きた）。
    """
    if k <= 0.0:
        return fr
    if k >= 1.0:
        return over(fr, layer)
    cr = layer.copy()
    x0, x1 = span or (0, S.W)
    x = int(x0 + (x1 - x0) * k)
    m = Image.new("L", cr.size, 0)
    m.paste(255, (0, 0, max(0, x - soft), S.H))
    if soft and x > 0:
        # 🔴 端のぼかしは明示的に作る。`linear_gradient("L").rotate(90)` は
        #    左が0・右が255＝必要な向きの逆で、reveal の手前に暗い帯が出た。
        m.paste(_grad(soft), (max(0, x - soft), 0))
    # 🔴 `Image.composite` ではなく**不透明度の掛け算**。composite だとマスクが
    #    中間値のとき透明画素まで半不透明になり、ぼかし帯に縦の暗い帯が出る。
    cr.putalpha(ImageChops.multiply(cr.getchannel("A"), m))
    fr.alpha_composite(cr)
    return fr


def subtitle(fr, cut, t, subs, band=None, mute=()):
    """黒帯を**常時**貼り、その時刻に出ている字幕行の**文字だけ**を載せる。

    🔴 2026-07-31（試写の指摘③）：帯と文字を1枚のPNGに焼いていたので、
       字幕が切り替わるたびに帯までフェードして**画面がちらついた**。
       帯は全カット共通の1枚（`_subband`）にして貼りっぱなしにする。
       ⚠️ 図の本体は y=892 までなので、帯を常時出しても図には一切かからない。

    mute … 出さない行の番号。**呼び出し側が `meta` から渡す**（下記）。
    """
    if band is not None:
        fr.alpha_composite(band, (0, S.SUB_Y))
    rows = S.SUBS.get(cut)
    if not rows or cut not in subs:
        return fr
    strip = subs[cut]
    for i, r in enumerate(rows):
        if i in mute:
            continue
        a, b = r["t"] + S.LEAD, r["t"] + r["d"] + S.LEAD + 0.12
        if a - 0.10 <= t <= b:
            row = strip.crop((0, i * S.SUB_H, S.W, (i + 1) * S.SUB_H))
            k = min(1.0, (t - (a - 0.10)) / 0.14, max(0.0, (b - t) / 0.14))
            p = fade(row, k)
            if p:
                fr.alpha_composite(p, (0, S.SUB_Y))
            break
    return fr


_VEIL = {}


def veil_layer(a, bg=None):
    """図を読ませるために写真の上に敷く暗幕。**全面 J.BG の一様な板。**

    🔴 2026-07-31（試写の指摘④）。図解は細い線と小さい文字なので、
       写真がそのまま出ていると読めない。濃さは `tools/check_veil.py` が
       「いちばん暗いインクと地とのコントラスト比」を測って決めている。
       ⚠️ グラデーションにしない。薄いところに図が来ると読めなくなるので、
          **どこに図が来ても同じ濃さ**であることのほうが大事。
    """
    # 🔴 12本目から：板の色は**その章の地の色**（bg。省略は J.BG＝今までどおり）
    bg = bg or J.BG
    k = (round(a, 3), bg)
    if k not in _VEIL:
        c = tuple(int(bg[i:i + 2], 16) for i in (1, 3, 5))
        _VEIL[k] = Image.new("RGBA", (S.W, S.H), c + (int(255 * k[0]),))
    return _VEIL[k]


def _bg_of(meta, cut):
    return J.palette((meta.get(cut) or {}).get("pal"))["BG"]


# ── 12本目からの転換・カメラ・閃光（§5b-17）────────────────────────
FADE_BLACK = 0.40     # 章の終わりの暗転／扉の出だしの暗転明け（秒）
CARD_X = 0.40         # 扉 → 中身へ重ねて入れ替える秒
DISSOLVE = 0.50       # 同じ章の写真どうしのディゾルブ（秒）
CARD_PHOTO = 0.36     # 扉の地に写真を混ぜる割合（方眼を残す）


def ease(u):
    """緩急（イージング）。0→1 を、動き始めと終わりをなめらかにして返す（余弦の半周）。"""
    u = min(1.0, max(0.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u)


# カメラの型。SPEC の cam= に書く。**写真だけのカット（動く映像でない）**にだけ効く。
# 書かなければ今までどおりのゆっくり寄る動き（k）。
#   "pan_r" / "pan_l"   … 左→右／右→左に横へなぞる（CAM_Z 倍に寄って動く余地を作る）
#   "tilt_d" / "tilt_u" … 上→下／下→上になぞる
#   "pull"              … 1.5倍に寄った所から引いて、全体を明かす
#   {"from": (xbias, bias, zoom), "to": (xbias, bias, zoom)} … 2点移動（cuts/ss.focus() の値を書ける）
# ⚠️ 切り方が動くので、check_slide（焼き込み文字）・check_blank（空の窓）は cam_samples() の
#    3点（頭・中・尻）で測る。
CAM_Z = 1.22


def cam_ends(cam, bias=0.5, xb=0.5, zm=1.0):
    """カメラの経路の両端 ((xbias, bias, zoom), (xbias, bias, zoom))。"""
    if isinstance(cam, str):
        z = max(zm, 1.0) * CAM_Z
        return {"pan_r": ((0.0, bias, z), (1.0, bias, z)),
                "pan_l": ((1.0, bias, z), (0.0, bias, z)),
                "tilt_d": ((xb, 0.0, z), (xb, 1.0, z)),
                "tilt_u": ((xb, 1.0, z), (xb, 0.0, z)),
                "pull": ((xb, bias, zm * 1.5), (xb, bias, zm))}[cam]
    return tuple(cam["from"]), tuple(cam["to"])


def cam_state(cam, u, bias=0.5, xb=0.5, zm=1.0):
    """時刻 u（0→1）のカメラ＝(xbias, bias, zoom)。緩急を掛け、寄せは 0〜1 に収める。"""
    a, b = cam_ends(cam, bias, xb, zm)
    e = ease(u)
    x, y, z = (p + (q - p) * e for p, q in zip(a, b))
    return min(1.0, max(0.0, x)), min(1.0, max(0.0, y)), z


def cam_samples(cam, bias=0.5, xb=0.5, zm=1.0):
    """門番が測る3点（頭・中・尻）。"""
    return [cam_state(cam, u, bias, xb, zm) for u in (0.0, 0.5, 1.0)]


# 閃光＝**爆発の瞬間だけ**。SPEC の flash=（中身の頭からの秒）が光のいちばん強い時刻。
# 2コマで立ち上がり、τ=0.28秒で消える（1回きり。点滅はさせない）。
FLASH_PEAK, FLASH_TAU = 0.85, 0.28


def flash_alpha(dt):
    rise = 2 / FPS
    if dt < -rise:
        return 0.0
    if dt < 0:
        return FLASH_PEAK * (1 + dt / rise)
    return FLASH_PEAK * math.exp(-dt / FLASH_TAU)


_SOLID = {}


def _solid(rgb):
    if rgb not in _SOLID:
        _SOLID[rgb] = Image.new("RGBA", (S.W, S.H), rgb + (255,))
    return _SOLID[rgb]


def _empty_name(pal):
    return "_empty" if (pal or "navy") == "navy" else f"_empty_{pal}"


def card_frame(cut, t, off, lay, photos, meta):
    """章の扉。その章の色の方眼に、頭のカットの写真を薄く混ぜ、章番号と章名を載せる。"""
    m = meta.get(cut) or {}
    fr = lay[_empty_name(m.get("pal"))].copy()
    if cut in photos:
        ph = fit(photos[cut], (0, 0, S.W, S.H), 0.3 * t / max(off, 0.001),
                 S.PHOTO_CUTS[cut][2], *S.PHOTO_CROP[cut])
        fr = Image.blend(fr, tone(ph, cut, meta), CARD_PHOTO)
    over(fr, lay[f"card_{cut}"], min(1.0, max(0.0, (t - 0.20) / 0.45)))
    if t < FADE_BLACK:
        fr = Image.blend(_solid((0, 0, 0)), fr, ease(t / FADE_BLACK))
    return fr


def scene(cut, t, dur, lay, photos, meta):
    """字幕を除いた画面。"""
    span = meta[cut]["span"]
    times = meta[cut]["times"]
    if meta[cut]["back"]:
        # ★写真を地にして、暗幕を挟み、その上に図解を重ねる
        k = t / max(dur, 0.001)
        xb, zm = S.PHOTO_CROP[cut]
        # 🔴 2026-08-02：地に敷くカットも**動画にできる**ようにした。
        #    それまでは実写カット（写真だけ）しか動画に差し替えられず、
        #    地に敷く9カットは静止画のまま寄るだけだった。
        #    ⚠️ 動くコマに寄り（ケンバーンズ）を重ねると手ブレに見えるので k=0。
        #    ⚠️ 切り方は**動画側の実測値**を使う（写真用の寄せでは焼き込みが残る）。
        src = foot_frame(cut, t)
        if src is not None:
            ph = fit(src, S.PHOTO_FULL, 0.0, meta[cut].get("fbias", 0.5),
                     meta[cut].get("fxb", xb), meta[cut].get("fzm", zm))
        else:
            ph = fit(photos[cut], S.PHOTO_FULL, k, S.PHOTO_CUTS[cut][2], xb, zm)
        fr = tone(ph, cut, meta)
        fr.alpha_composite(veil_layer(meta[cut]["veil"], _bg_of(meta, cut)))
        fr.alpha_composite(lay[f"{cut}_base"])
    elif meta[cut]["photo"]:
        box, _, bias = S.PHOTO_CUTS[cut]
        xb, zm = S.PHOTO_CROP[cut]
        fr = lay[f"{cut}_bg"].copy()
        # 帯写真はケンバーンズを弱くする（原寸に近いので寄ると粗が出る）
        k = t / max(dur, 0.001)
        # ★動画を当てたカットは、そのコマを写真の代わりに使う
        #   ⚠️ 映像そのものが動いているので、寄り（ケンバーンズ）は**かけない**。
        #     動く絵に寄りを重ねると手ブレのように見える。
        src = foot_frame(cut, t)
        if src is not None:
            xb, zm = meta[cut].get("fxb", xb), meta[cut].get("fzm", zm)
            ph = fit(src, box, 0.0, meta[cut].get("fbias", bias), xb, zm)
        else:
            src = photos[cut]
            cam = meta[cut].get("cam")
            if cam:
                # 🔴 12本目から：カメラの型（パン・引き・2点移動）。寄り（k）は重ねない
                cxb, cb, czm = cam_state(cam, k, bias, xb, zm)
                ph = fit(src, box, 0.0, cb, cxb, czm)
            else:
                # 実写カットでも `xbias` / `zoom` を書けば焼き込みを外せる（既定は今までと同じ）
                ph = fit(src, box, k * (0.35 if box[3] < S.H else 1.0), bias, xb, zm)
        fr.paste(tone(ph, cut, meta), (box[0], box[1]))
        # 🔴 2026-09-07（5本目 SL-1）：**実写カットにも暗幕をかけられるようにした。**
        #    それまで暗幕は「写真を地にして図を重ねるカット」だけだった。
        #    5本目は**報告書の本文ページ**を写真として出すカットが 26 あり、
        #    紙いちめんの英字の上に日本語の注記が載っていた
        #    （`check_slide` G-13 108件・G-14 61件）。暗幕を敷くと英字は 16〜22% に沈み、
        #    こちらの文字だけが残る。⚠️ **spec に `veil=` を書いたカットだけ**（既定は今までどおり無し）。
        vp = meta[cut].get("pveil")
        if vp:
            fr.alpha_composite(veil_layer(vp, _bg_of(meta, cut)))
        over(fr, lay[f"{cut}_lab"], min(1.0, max(0.0, (t - 0.15) / 0.5)))
        # 実写の注記は**フェード**で出す。写真の上を横切るワイプは汚れに見える
        for i, (a, b) in enumerate(times):
            k = f"{cut}_a{i + 1}"
            if k in lay:
                over(fr, lay[k], max(0.0, min(1.0, (t - a) / 0.45)))
        return fr
    else:
        fr = lay[f"{cut}_base"].copy()
    # 図の骨格は前半で手早く描く（骨格が未完成のまま段が乗ると図が壊れて見える）
    if f"{cut}_lab" in lay:
        wipe(fr, lay[f"{cut}_lab"],
             min(1.0, max(0.0, (t - 0.15) / (dur * meta[cut]["labk"]))), span=span)
    # 段は draw_span() の秒で描き終え、残りは出そろった状態で見せる。
    # 🔴 r6 の目視で分かった：持ち時間いっぱい使うと、引用の2行目が
    #    カットの終わりでやっと出そろい、**読み終わる前に切り替わる**（c518 は尺3.7秒）。
    for i, (a, b) in enumerate(times):
        k = f"{cut}_a{i + 1}"
        if k not in lay:
            continue
        wipe(fr, lay[k], max(0.0, min(1.0, (t - a) / draw_span(b - a))),
             soft=70, span=span)
    if f"{cut}_hot" in lay:
        pulse = 0.42 + 0.58 * (0.5 + 0.5 * math.sin(t * math.tau / 1.6))
        over(fr, lay[f"{cut}_hot"], pulse)
    if meta[cut].get("moves"):
        fr = draw_moves(fr, cut, t, meta)
    return fr


# ══════════════════════════════════════════════════════════
#  12本目から：動く部品（drift・trace）と冒頭の写真（intro）── ⑤b-2 新設（2026-09-23）
# ══════════════════════════════════════════════════════════
# 型が `Fig.moves` に**画素の座標**で渡したものを、1コマずつ PIL で描く（Chrome を毎コマ呼ばない）。
# 動き出す時刻＝その段の行頭（`times`）。冒頭の写真があるカットは、写真が図へ入れ替わってから。
# 小さな点のギザギザを消すため、動く部品の**外接の矩形だけ**を2倍で描いて縮める。
INTRO_X = 0.6          # 冒頭の写真から図へ入れ替える秒
_SS = 2


def _rgb(hx):
    return tuple(int(hx[i:i + 2], 16) for i in (1, 3, 5))


def _move_box(mv):
    """その動きが描く範囲（画面の画素）。"""
    if mv["kind"] == "hl":
        xs = [v for r in mv["rects"] for v in (r[0], r[2])]
        ys = [v for r in mv["rects"] for v in (r[1], r[3])]
        return min(xs) - 8, min(ys) - 8, max(xs) + 8, max(ys) + 8
    if mv["kind"] == "fall":
        x, y = mv["at"]
        return x - 110, y - 260, x + 110, y + 30
    pts = mv.get("pts") or [mv[k] for k in ("a", "b") if k in mv]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs) - 60, min(ys) - 60, max(xs) + 60, max(ys) + 60


def _t0(mv, times, meta_c):
    a = times[mv["stage"]][0] if mv["stage"] < len(times) else 0.0
    it = meta_c.get("intro")
    return max(a, float(it["sec"]) + INTRO_X * 0.5) if it else a


def draw_moves(fr, cut, t, meta):
    import random
    mc = meta[cut]
    moves, times = mc["moves"], mc["times"]
    pal = J.palette(mc.get("pal"))
    ink, amber = _rgb(pal["INK_W"]), _rgb(J.AMBER)
    boxes = [_move_box(m) for m in moves]
    X0 = max(0, int(min(b[0] for b in boxes)))
    Y0 = max(0, int(min(b[1] for b in boxes)))
    X1 = min(S.W, int(max(b[2] for b in boxes)))
    Y1 = min(S.H, int(max(b[3] for b in boxes)))
    if X1 <= X0 or Y1 <= Y0:
        return fr
    ov = Image.new("RGBA", ((X1 - X0) * _SS, (Y1 - Y0) * _SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)

    def P(x, y):
        return (x - X0) * _SS, (y - Y0) * _SS

    def dot(x, y, r, col, a):
        cx, cy = P(x, y)
        d.ellipse((cx - r * _SS, cy - r * _SS, cx + r * _SS, cy + r * _SS),
                  fill=col + (max(0, min(255, int(255 * a))),))
    drew = False
    for mv in moves:
        t0 = _t0(mv, times, mc)
        if t < t0:
            continue
        dt = t - t0
        drew = True
        if mv["kind"] == "stream":
            # 灰の**向き**だけ（広がりの形は描かない）。頭が 2.4秒で伸びきり、点が流れつづける
            (ax, ay), (bx, by) = mv["a"], mv["b"]
            head = min(1.0, dt / 2.4)
            n = int(mv.get("n", 16))
            d.line((*P(ax, ay), *P(ax + (bx - ax) * head, ay + (by - ay) * head)),
                   fill=ink + (60,), width=3 * _SS)
            for j in range(n):
                u = (dt / 3.2 + j / n) % 1.0
                if u > head:
                    continue
                a = min(1.0, u / 0.08) * min(1.0, (1.0 - u) / 0.12) * 0.9
                dot(ax + (bx - ax) * u, ay + (by - ay) * u, 6, ink, a)
        elif mv["kind"] == "sight":
            # 視線の線（1.0秒で伸びる）→ その先が光る（人は描かない）
            (ax, ay), (bx, by) = mv["a"], mv["b"]
            k = min(1.0, dt / 1.0)
            L = math.hypot(bx - ax, by - ay)
            seg, gap = 18.0, 12.0
            s0 = 0.0
            while s0 < L * k:
                s1 = min(s0 + seg, L * k)
                d.line((*P(ax + (bx - ax) * s0 / L, ay + (by - ay) * s0 / L),
                        *P(ax + (bx - ax) * s1 / L, ay + (by - ay) * s1 / L)),
                       fill=ink + (200,), width=3 * _SS)
                s0 = s1 + gap
            if k >= 1.0:
                g = 0.5 + 0.5 * math.sin((dt - 1.0) * math.tau / 1.2)
                for r, a in ((46 + 10 * g, 0.18), (30 + 6 * g, 0.35), (16, 0.9)):
                    dot(bx, by, r, amber, a)
        elif mv["kind"] == "fall":
            # 白い点が降りはじめ、船の上に積もる（決まった乱数＝何度焼いても同じ絵）
            x, y = mv["at"]
            rnd = random.Random(f"{cut}-fall")
            for j in range(int(mv.get("n", 26))):
                t_j = j * 0.32 + rnd.random() * 0.2
                if dt < t_j:
                    continue
                # 船の輪郭（幅20・長さ52px）の上とそのすぐ周り。広く散らすと「船の上」に見えない
                dx, land = rnd.uniform(-18, 18), rnd.uniform(-24, 18)
                sway = rnd.uniform(0, math.tau)
                yy = max(float(mv.get("top", y - 230)), y - 230) + (dt - t_j) * 95
                xx = x + dx + 6 * math.sin((dt - t_j) * 2.2 + sway)
                if yy >= y + land:
                    yy, xx = y + land, x + dx
                dot(xx, yy, 4, (255, 255, 255), 0.95)
        elif mv["kind"] == "path":
            # 点がその順に進み、通ったあとに線を残す（船の航路など）
            pts = mv["pts"]
            segs = [math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts, pts[1:])]
            tot = sum(segs) or 1.0
            gone = ease(min(1.0, dt / float(mv.get("sec", 3.0)))) * tot
            px_, py_ = pts[0]
            for (p, q), sl in zip(zip(pts, pts[1:]), segs):
                f = min(1.0, gone / sl) if sl else 1.0
                ex, ey = p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f
                d.line((*P(*p), *P(ex, ey)), fill=ink + (190,), width=4 * _SS)
                px_, py_ = ex, ey
                gone -= sl
                if gone <= 0:
                    break
            dot(px_, py_, 9, ink, 1.0)
        elif mv["kind"] == "hl":
            # 蛍光ペン：**読む順に**行ごとに左→右へ塗る（1行 0.7秒）。頁が出そろってから（delay）
            rest = dt - float(mv.get("delay", 0.4))
            for r in mv["rects"]:
                if rest <= 0:
                    break
                k = min(1.0, rest / 0.7)
                x0, y0, x1, y1 = r
                d.rectangle((*P(x0 - 4, y0 - 2), *P(x0 - 4 + (x1 - x0 + 8) * k, y1 + 2)),
                            fill=amber + (105,))
                rest -= 0.7
    if not drew:
        return fr
    ov = ov.resize((X1 - X0, Y1 - Y0), Image.LANCZOS)
    fr = fr.convert("RGBA") if fr.mode != "RGBA" else fr
    fr.alpha_composite(ov, (X0, Y0))
    return fr


_INTRO_SRC = {}


def intro_frame(cut, t, lay, meta):
    """冒頭の写真のコマ（全画面・ゆっくり寄る）。見出しと出典は `{cut}_ilab`。"""
    it = meta[cut]["intro"]
    if it["photo"] not in _INTRO_SRC:
        _INTRO_SRC[it["photo"]] = load_photo(it["photo"], (0, 0, S.W, S.H))
    k = t / max(float(it["sec"]) + INTRO_X, 0.001)
    ph = fit(_INTRO_SRC[it["photo"]], (0, 0, S.W, S.H), k * 0.6,
             it.get("bias", 0.5), it.get("xbias", 0.5), it.get("zoom", 1.0))
    keep = float(it.get("color", 0.0))
    pal = J.palette(meta[cut].get("pal"))
    fr = duotone(ph, pal["BG2"], pal["DUO_L"])
    if keep > 0.001:
        fr = Image.blend(fr, ph.convert("RGBA"), min(1.0, keep))
    fr = fr.convert("RGBA")
    if f"{cut}_ilab" in lay:
        over(fr, lay[f"{cut}_ilab"], min(1.0, max(0.0, (t - 0.15) / 0.5)))
    return fr


def compose(cut, t, dur, lay, photos, meta, subs=None, band=None):
    """1コマ。t と dur は**扉込み**のカットの時刻と尺（CUTS のまま渡す）。

    🔴 12本目から：扉（meta の card 秒）があるカットは、頭の card 秒が章の扉。
       中身（scene・字幕）には**扉を引いた時刻**を渡す（scene_jiko.stage_times も同じ尺で組む）。
    """
    m = meta.get(cut) or {}
    off = float(m.get("card") or 0.0)
    if off and t < off:
        fr = card_frame(cut, t, off, lay, photos, meta)
        if t > off - CARD_X:
            # 扉の終わりは、中身の最初のコマへ重ねて入れ替える
            first = scene(cut, 0.0, dur - off, lay, photos, meta)
            fr = Image.blend(fr, first, ease((t - (off - CARD_X)) / CARD_X))
        return fr
    t2, dur2 = t - off, dur - off
    fr = scene(cut, t2, dur2, lay, photos, meta)
    it = m.get("intro")
    if it and t2 < float(it["sec"]) + INTRO_X:
        # 🔴 12本目から：冒頭の写真（c104＝空撮を約3秒→地図）。写真のあいだ図は見せず、重ねて入れ替える
        pf = intro_frame(cut, t2, lay, meta)
        u = (t2 - float(it["sec"])) / INTRO_X
        fr = pf if u <= 0 else Image.blend(pf, fr, ease(u))
    if m.get("flash") is not None:
        a = flash_alpha(t2 - float(m["flash"]))
        if a > 0.004:
            fr = Image.blend(fr, _solid((255, 255, 255)), a)
    prev = m.get("_prev_img")
    if prev is not None and t2 < DISSOLVE:
        # 同じ章の写真どうし：前のカットの最後のコマから重ねて入れ替える
        fr = Image.blend(prev, fr, ease(t2 / DISSOLVE))
    # 🔴 決め所（quote）と同じ行は字幕に出さない。図が同じ言葉を大きく出しているので、
    #    そのまま出すと二重表示になる（2026-08-03。"with_last" で声と同時に出すようにした）。
    #    ★どの行を消すかは **meta から取る**。`S.SUB_MUTE` を直接見てはいけない
    #      （理由は meta_of() の "mute" を見よ）。
    fr = subtitle(fr, cut, t2, subs or {}, band, m.get("mute") or ())
    if m.get("tail_black") and t > dur - FADE_BLACK:
        # 章の終わり：声が止んだあとの尻（TAIL 0.50秒）で暗転し、次の章の扉へ
        fr = Image.blend(fr, _solid((0, 0, 0)), ease((t - (dur - FADE_BLACK)) / FADE_BLACK))
    return fr


def load_band():
    """字幕の黒帯。**全カット共通の1枚**なので1回だけ読む。"""
    p = OUT / "_subband.png"
    return Image.open(p).convert("RGBA") if p.exists() else None


def meta_of(idx):
    """カットごとの合成に必要な情報をまとめる。"""
    m = {}
    for cid, v in idx.items():
        m[cid] = {"photo": v["photo"], "back": v["back"], "veil": v["veil"],
                  # 🔴🔴 2026-09-07（5本目 SL-1 ⑤c'）：**この1行が抜けていた。**
                  #    scene_jiko.layer_index() は `pveil` を正しく作っていたのに
                  #    ここで写していなかったので、build_jiko.py:346 の
                  #    `meta[cut].get("pveil")` が**常に None**。
                  #    ＝ spec に veil=0.84 と書いた **26カットすべてで暗幕が1枚も
                  #    かかっていなかった**（実効 0.08＝tone() の写りだけ）。
                  #    門番 check_slide は「絵」でなく SPEC を読んでいたので黙っていた。
                  #    → [[feedback-settings-may-not-reach-the-picture]]
                  "pveil": v.get("pveil"),
                  "span": v["span"],
                  # labk … 骨格を描くのにカットの何割を使うか（既定 LAB_K）。
                  #   段が1つしかない型（作り直した quote）は、既定だと前半で
                  #   描き終わってそのあと画が止まるので、型の側から長めに指定できる。
                  "labk": v.get("labk") or LAB_K,
                  # ★「最後の行を読み終えてから出す」段（quote の決め所）の番号。
                  #   検品画像をこの段より**あと**で撮るために要る（qa_shots を見よ）。
                  "held": [i for i, h in enumerate(v.get("holds") or [])
                           if h == "after_last"],
                  # 🔴 字幕に出さない行（決め所と同じ行）。**必ずここに入れて持ち回る。**
                  #    `S.SUB_MUTE` は build_layers が埋めるモジュール変数で、
                  #    build_full は ProcessPoolExecutor で焼く。子プロセスは
                  #    `import scene_jiko` をやり直すだけで build_layers を呼ばないので、
                  #    **子の SUB_MUTE は空のまま**になる。
                  #    Linux(fork)の Modal では親の記憶を受け継ぐので今は効くが、
                  #    Windows(spawn) で full を回すと決め所が字幕と二重表示になる。
                  #    しかも検品(qa)は同一プロセスなので**画像だけ正しく見えて気づけない**。
                  #    → meta に入れて `_seg_worker` へ引数として渡す（2026-08-03）。
                  "mute": sorted(S.SUB_MUTE.get(cid) or []),
                  # ★色を残す割合（0＝デュオトーン／1＝原色）。`tone()` を見よ
                  "color": float((S.SPEC.get(cid) or {}).get("color", 0.0)),
                  "times": S.stage_times(cid, v["stages"], v.get("holds")),
                  # 🔴 12本目から（§5b-17・§5b-33b）。子プロセスは親の変数を見ないので必ず meta で運ぶ
                  "pal": S.palette_of(cid),                 # 章の色
                  "card": S.card_of(cid),                   # 頭の扉の秒（0＝無し）
                  "tail_black": S.chapter_tail(cid),        # 尻で暗転（次が扉）
                  "flash": (S.SPEC.get(cid) or {}).get("flash"),   # 閃光の秒（爆発の瞬間だけ）
                  "cam": (S.SPEC.get(cid) or {}).get("cam"),       # カメラの型
                  "moves": v.get("moves") or [],            # 動く部品（drift・trace）
                  "intro": v.get("intro")}                  # 冒頭の写真（c104）
        # ディゾルブ：**同じ章の、写真だけのカットどうし**（図解・扉つきのカットには掛けない）
        i = S.ORDER.index(cid)
        prev = S.ORDER[i - 1] if i > 0 else None
        solo = v["photo"] and not v["back"]
        if (prev and solo and prev in idx and idx[prev]["photo"] and not idx[prev]["back"]
                and prev[:2] == cid[:2] and not S.card_of(cid)):
            m[cid]["dissolve"] = prev
        # ★動画を当てたカットの切り方（焼き込みを画面外へ追い出すための寄せ・拡大）
        u = _FOOT_USE.get(cid)
        if u:
            # 🔴 2026-09-07（K-12）：寄りは **footage.zoom_of()** から取る。
            #    素材（NARA MoPix）は 1920 の箱に 1440 の絵で、左右 240px が黒。
            #    `u["zoom"]` をそのまま使うと帯が画面に残る。1か所で効かせる
            m[cid].update(fxb=u.get("xbias", 0.5),
                          fzm=(_FO.zoom_of(cid, u) if _FO else u.get("zoom", 1.0)),
                          fbias=u.get("bias", 0.5))
    return m


def check_motion(meta, limit=5.0):
    """**limit 秒以上、図がまったく動かない区間**が無いかを機械的に確認する。

    🔴 2026-08-01：上限を **3.0 → 5.0 秒**にした（カズヤくん指示）。
       3秒は厳しすぎて、**引用の決め所を「読み終えてから出す」ことができなかった**
       （読み終わりを待つあいだは、当然どこも動かない）。
       ⚠️ 「動かなくてよい」ではなく「5秒までなら止まってよい」。
          STILL_MAX（2.2秒）は**変えていない**ので、ふつうの段の見え方は今までどおり。

    実写はケンバーンズで常に動いているので対象外。
    図解は「骨格を描く区間」と「各段を描く区間」の合併が尺を覆っているかを見る。
    """
    bad, worst = [], 0.0
    for cid, sec in S.CUTS:
        if cid not in meta:
            continue
        sec = sec - S.card_of(cid)      # 扉の秒は中身に含めない（扉は扉で動いている）
        # 写真だけのカットはケンバーンズで常に動いている。
        # ⚠️ **写真を地に敷いた図解カットは対象に残す**（図が止まったら止まって見える）。
        if meta[cid]["photo"] and not meta[cid]["back"]:
            continue
        iv = [(0.15, 0.15 + sec * meta[cid]["labk"])] + [(a, a + draw_span(b - a))
                                                        for a, b in meta[cid]["times"]]
        iv.sort()
        cur = 0.0
        gaps = []
        for a, b in iv:
            if a - cur > 0:
                gaps.append((cur, a))
            cur = max(cur, b)
        if sec - cur > 0:
            gaps.append((cur, sec))
        for a, b in gaps:
            worst = max(worst, b - a)
            if b - a > limit:
                bad.append((cid, round(a, 2), round(b - a, 2), round(sec, 2)))
    print(f"図が動かない最長区間 = {worst:.2f}秒")
    for cid, a, g, sec in bad:
        print(f"  🔴 {cid}（尺{sec}秒）の {a}秒から {g}秒 動かない")
    if not bad:
        print(f"✓ 図が {limit}秒以上止まるカットは無い")
    longest = max(((r["d"], r["text"]) for rows in S.SUBS.values() for r in rows),
                  default=(0, ""))
    print(f"（参考）最長の字幕 = {longest[0]:.2f}秒「{longest[1][:26]}」"
          f" ／ 字幕の枚数 {sum(len(r) for r in S.SUBS.values())}")
    return bad


# ── 検品で必ず拡大して見る場所 ────────────────────────────
# 🔴 226カットあるので**全カットを同じ4か所で機械的に切り出す**。
#    「見出しの行末」「本体の左」「本体の右」「字幕帯」。
#    ここに載せたカットだけ、さらに実寸の全体像も出す。
ZOOM_BOXES = [
    ("見出しと章", (0, 20, 1900, 300)),
    ("本体-左", (40, 200, 990, 900)),
    ("本体-右", (950, 200, 1900, 900)),
    ("字幕帯", (180, 860, 1740, 1080)),
]


def _load_layers(cids, idx):
    lay = {}
    for cid in cids:
        for n in idx[cid]["layers"]:
            lay[n] = L(n)
        if S.card_of(cid) and (OUT / f"card_{cid}.png").exists():
            lay[f"card_{cid}"] = L(f"card_{cid}")
    # 章の色ごとの地（章の扉の地・check_space の基準）
    for pal in set(S.CHAPTER_PALETTE.values()) | {"navy"}:
        n = _empty_name(pal)
        if (OUT / f"{n}.png").exists():
            lay[n] = L(n)
    return lay


def qa_shots(cids, idx, meta, at=0.92):
    """カットごとの検品画像。段が出そろった状態を実寸で残す。

    🔴 撮る時刻の選び方で2回まちがえた。
       0.88 … ワイプの途中が写り、図が切れているのか描いている最中か区別がつかない
       0.97 … **字幕が消えたあと**を撮ってしまう（カット尻の TAIL=0.5秒は無音なので
               字幕が出ていない）。占有率が 52.5% → 42.3% と10ポイント落ちた
       0.92 … 段は出そろい、字幕はまだ出ている。**ここが実際の見え方に近い**

    🔴 2026-08-02（r21 の目視）：**0.92 でもまだ足りていなかった。**
       尺の短いカットでは 0.92 が字幕のフェードアウトの最中に当たる。
       実測すると **229 カット中 36 カット**で字幕が薄い／消えていた
       （c107 は 5.0 秒で不透明度 0.13、c414 は 0.04、c124 など9カットは 0）。
       ⚠️ これは映像の粗ではなく**検品画像の撮り方の穴**だが、
         そのせいで「字幕が読めるか」をこの36カットで**判定できなかった**。
         実際 r21 の目視で「c107 の字幕だけ色が壊れている」と誤って上がっている。
       → カットごとに「**最後の字幕がまだ完全に出ている**いちばん遅い時刻」を選ぶ。
         段が出そろうのを待ちたいので、その範囲で**できるだけ遅く**撮る。
    """
    QA.mkdir(parents=True, exist_ok=True)
    secs = dict(S.CUTS)

    def shot_at(cid, sec):
        """字幕が完全に出ている範囲で、いちばん遅い時刻。"""
        rows = S.SUBS.get(cid)
        if not rows:
            return sec * at
        last = rows[-1]
        # subtitle() のフェード：b = t + d + LEAD + 0.12、最後の 0.14 秒で消える
        full_until = last["t"] + last["d"] + S.LEAD + 0.12 - 0.14
        # 段が出そろう時刻（既定 0.92）より前には戻さない範囲で、遅いほうを採る
        t = max(min(sec * at, full_until), min(sec * 0.70, full_until))
        # 🔴 2026-08-02（r25 の目視）：**引用16カットの決め所が1枚も写っていなかった。**
        #    `quote` の決め所は `holds="after_last"`＝最後の行を読み終えてから出る段で、
        #    上の式は「最後の字幕がまだ完全に出ている」時刻を選ぶので、
        #    **必ず決め所が出る直前**を撮ってしまう。
        #    そのため検品画像はどれも右2/3が空で、掛け値なしに「画が空」と読めた
        #    （実際には決め所が 2.25秒ぶん出る。尺と段の時刻で実測した）。
        #    → 保持段があるカットは、**その段が出たあと**を撮る。
        #      字幕はそのとき消えているが、それはこの型の設計そのもの
        #      （画面に出す言葉を字幕に出さない）。
        held = (meta.get(cid) or {}).get("held") or []
        if held:
            times = meta[cid]["times"]
            start = max(times[i][0] for i in held if i < len(times))
            t = max(t, min(start + 0.6, sec - 0.10))
        return t
    subs = {c: L(f"sub_{c}") for c in cids if (OUT / f"sub_{c}.png").exists()}
    lay = _load_layers(cids, idx)
    band = load_band()
    photos = {c: load_photo(S.PHOTO_CUTS[c][1], S.PHOTO_CUTS[c][0],
                            S.PHOTO_TRIM.get(c), S.PHOTO_LEVELS.get(c))
              for c in cids if idx[c]["photo"]}
    out = []
    for cid in cids:
        sec = secs[cid]
        # 🔴 12本目から：撮る時刻は**中身の時刻**で選び、扉の秒を足して compose へ渡す
        off = S.card_of(cid)
        im = compose(cid, off + shot_at(cid, sec - off), sec, lay, photos, meta, subs,
                     band).convert("RGB")
        im.save(QA / f"cut_{cid}.png")
        if off and f"card_{cid}" in lay:
            # 章の扉も1枚（文字が出そろい、中身へ重なり始める前）
            compose(cid, off * 0.6, sec, lay, photos, meta, subs, band).convert("RGB").save(
                QA / f"card_{cid}.png")
        out.append((cid, im))
    return out


def _seg_worker(args):
    """1カットぶんを mp4 に焼く。**プロセスを分けて並列に回す**。

    🔴 `nframes` は呼び出し側が**通し時刻から**計算して渡す。
       カットごとに round(sec*30) すると丸め誤差が積み上がり、34分の終わりでは
       音と数秒ずれる（226カット × 最大0.5コマ）。音声側は正確な秒で置いているので、
       映像の側を通し時刻に合わせる。
    """
    cid, sec, nframes, idxv, metav, prevpack = args
    import scene_jiko as S2
    lay = {n: Image.open(OUT / f"{n}.png").convert("RGBA") for n in idxv["layers"]}
    if metav.get("card"):
        # 章の扉の文字と、その章の色の地
        for n in (f"card_{cid}", _empty_name(metav.get("pal"))):
            lay[n] = Image.open(OUT / f"{n}.png").convert("RGBA")
    subs = {}
    if (OUT / f"sub_{cid}.png").exists():
        subs[cid] = Image.open(OUT / f"sub_{cid}.png").convert("RGBA")
    photos = {}
    if idxv["photo"]:
        photos[cid] = load_photo(S2.PHOTO_CUTS[cid][1], S2.PHOTO_CUTS[cid][0],
                                 S2.PHOTO_TRIM.get(cid), S2.PHOTO_LEVELS.get(cid))
    band = load_band()
    meta = {cid: dict(metav)}
    if prevpack:
        # ディゾルブの元＝前のカットの**最後のコマ**（各コマは「カットと時刻」だけで決まる作りなので、
        #   前のカットの素材を読めばこのプロセスの中で同じ絵を作れる）
        pcid, psec, pidxv, pmetav = prevpack
        play = {n: Image.open(OUT / f"{n}.png").convert("RGBA") for n in pidxv["layers"]}
        pph = {}
        if pidxv["photo"]:
            pph[pcid] = load_photo(S2.PHOTO_CUTS[pcid][1], S2.PHOTO_CUTS[pcid][0],
                                   S2.PHOTO_TRIM.get(pcid), S2.PHOTO_LEVELS.get(pcid))
        meta[cid]["_prev_img"] = scene(pcid, max(0.0, psec - 1.0 / FPS), psec, play, pph,
                                       {pcid: pmetav})
    n = nframes
    dst = SEG / f"{cid}.mp4"
    p = subprocess.Popen(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-s", f"{S.W}x{S.H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
         "-pix_fmt", "yuv420p", str(dst)], stdin=subprocess.PIPE)
    for f in range(n):
        fr = compose(cid, f / FPS, sec, lay, photos, meta, subs, band)
        p.stdin.write(fr.convert("RGB").tobytes())
    p.stdin.close()
    p.wait()
    return cid, n


def build_full(idx, meta, workers=None):
    """全カットを mp4 にして連結する。カット単位で並列。

    🔴 並列数は `ZUKAI_WORKERS` で外から決められる（2026-07-31）。
       本編の製造を Modal へ移したため（`modal_app.py` 参照）、
       `os.cpu_count()` はホストのコア数を返して**確保したコア数と一致しない**。
       確保したぶんだけ使うよう、実行側から渡す。
    """
    SEG.mkdir(parents=True, exist_ok=True)
    secs = dict(S.CUTS)
    workers = (workers or int(os.environ.get("ZUKAI_WORKERS", 0))
               or max(1, min(8, (os.cpu_count() or 2))))
    order = [c for c in S.ORDER if c in idx]
    # 通し時刻からコマの境目を出す（丸め誤差を積み上げない）
    args, cum = [], 0.0
    for cid in order:
        a = int(round(cum * FPS))
        cum += secs[cid]
        b = int(round(cum * FPS))
        pc = meta[cid].get("dissolve")
        prevpack = ((pc, S.content_sec(pc), idx[pc], meta[pc])
                    if pc and pc in idx and pc in meta else None)
        args.append((cid, secs[cid], b - a, idx[cid], meta[cid], prevpack))
    total = 0
    print(f"mp4 を {workers} 並列で焼く（{len(args)}カット）", flush=True)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for i, (cid, n) in enumerate(ex.map(_seg_worker, args), 1):
            total += n
            if i % 20 == 0 or i == len(args):
                print(f"  {i}/{len(args)}  {total}コマ", flush=True)
    lst = SEG / "list.txt"
    lst.write_text("".join(f"file '{cid}.mp4'\n" for cid in S.ORDER), encoding="utf-8")
    mp4 = OUT / "titan.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", "-movflags", "+faststart", str(mp4)], check=True)
    print(f"wrote {mp4} {total / FPS:.1f} sec", flush=True)
    return total


def default_zooms(order=None):
    """既定で拡大図を出すカット。**全226カット×4か所を出すと数百MBになる**ので絞る。

    章の頭・章の締め・実写カットを必ず入れ、あとは章ごとに等間隔で拾う。
    ここに無いカットを拡大したいときは `--zoom=c114,c529` のように名指しする。
    """
    order = order or S.ORDER
    want = set()
    # 🔴 2026-09-23：接頭辞を並びから取る。以前は ("pr","c1"〜"c6","ep") の決め打ちで、
    #    **第7〜9章と ed01 が拡大図にも一覧にも出なかった**（11本目・12本目は9章）
    for pre in dict.fromkeys(c[:2] for c in order):
        ids = [c for c in order if c.startswith(pre)]
        if not ids:
            continue
        want |= {ids[0], ids[-1]}
        for k in range(1, 3):
            want.add(ids[len(ids) * k // 3])
    want |= {c for c in order if S.SPEC.get(c, {}).get("photo")}
    return want


def build_qa(idx, meta, zoom_cuts=None):
    """検品用の静止画・拡大図・一覧を作る。**5巡以上の精査はこれを見る。**"""
    QA.mkdir(parents=True, exist_ok=True)
    order = [c for c in S.ORDER if c in idx]     # 章を作っている途中でも回せるように
    shots = qa_shots(order, idx, meta)
    # 余白の基準（check_space）。12本目から章の色ごとに1枚
    for pal in set(S.CHAPTER_PALETTE.values()) | {"navy"}:
        n = _empty_name(pal)
        if (OUT / f"{n}.png").exists():
            L(n).convert("RGB").save(QA / f"{n}.png")
    zoom_cuts = zoom_cuts if zoom_cuts is not None else default_zooms(order)
    for cid, im in shots:
        if cid not in zoom_cuts:
            continue
        for name, box in ZOOM_BOXES:
            c = im.crop(box)
            z = min(2.0, S.W / c.width, S.H / c.height)
            if z > 1.02:
                c = c.resize((round(c.width * z), round(c.height * z)), Image.LANCZOS)
            c.save(QA / f"zoom_{cid}_{name}.jpg", quality=92)
    # 一覧（章ごとに1枚）。34分を通しで俯瞰できるようにする
    names = {"pr": "プロローグ", "ep": "エピローグ", "ed": "エンディング"}
    for pre, label in ((p, names.get(p) or (f"{S.CHAPTERS[p][0]}章" if p in S.CHAPTERS else p))
                       for p in dict.fromkeys(c[:2] for c in order)):
        sel = [im for cid, im in shots if cid.startswith(pre)]
        if not sel:
            continue
        tw = 480
        th = round(tw * S.H / S.W)
        cols = 4
        rows = (len(sel) + cols - 1) // cols
        sh = Image.new("RGB", (tw * cols, th * rows), "#000")
        for i, im in enumerate(sel):
            sh.paste(im.resize((tw, th), Image.LANCZOS), ((i % cols) * tw,
                                                          (i // cols) * th))
        sh.save(QA / f"contact_{pre}.jpg", quality=88)
    print(f"検品画像 {len(shots)} カット", flush=True)


def veil_ladder(idx, meta, cids=None, alphas=(0.76, 0.80, 0.84, 0.88, 0.92)):
    """★同じカットを暗幕の濃さ違いで焼き並べる（2026-07-31 試写の指摘④）。

    カズヤくん指示「暗幕の濃さは焼いて目視で決めてください」。
    `tools/check_veil.py` が机上で 0.80〜0.88 まで絞ってあるので、その前後を焼く。
    ⚠️ **1回のクラウド実行で全部の濃さを出す**（濃さごとに回すと成果物枠を食う）。
    """
    QA.mkdir(parents=True, exist_ok=True)
    back = [c for c in S.ORDER if c in idx and idx[c]["back"]]
    cids = [c for c in (cids or back) if c in idx and idx[c]["back"]]
    if not cids:
        print("🔴 写真を地に敷いたカットが無い（cuts/__init__.py の BACKDROP）")
        return
    secs = dict(S.CUTS)
    subs = {c: L(f"sub_{c}") for c in cids if (OUT / f"sub_{c}.png").exists()}
    lay = _load_layers(cids, idx)
    band = load_band()
    photos = {c: load_photo(S.PHOTO_CUTS[c][1], S.PHOTO_CUTS[c][0],
                            S.PHOTO_TRIM.get(c), S.PHOTO_LEVELS.get(c))
              for c in cids}
    for cid in cids:
        sec = secs[cid]
        strip = []
        for a in alphas:
            m = {cid: dict(meta[cid], veil=a)}
            strip.append(compose(cid, sec * 0.92, sec, lay, photos, m,
                                 subs, band).convert("RGB"))
        # 濃さを縦に積んで1枚にする。**並べないと差が判断できない**
        tw = 960
        th = round(tw * S.H / S.W)
        sheet = Image.new("RGB", (tw, th * len(strip)), "#000")
        for i, im in enumerate(strip):
            sheet.paste(im.resize((tw, th), Image.LANCZOS), (0, i * th))
        sheet.save(QA / f"veil_{cid}.jpg", quality=90)
        # 拡大して線の読みやすさを見るぶんも出す（縮小版では判断できない）
        for a, im in zip(alphas, strip):
            im.crop((40, 200, 990, 900)).save(
                QA / f"veilzoom_{cid}_{int(a * 100)}.jpg", quality=92)
        print(f"  veil_{cid}.jpg  濃さ {'/'.join(str(a) for a in alphas)}", flush=True)
    print(f"暗幕の見比べ {len(cids)} カット（上から {alphas[0]} → {alphas[-1]}）", flush=True)


def shrink_stills(q=88):
    """check_space が読んだあとの `cut_*.png` を JPEG に詰め直す。

    226カットを PNG のまま成果物に載せると 300MB を超えてダウンロードが実用的でない。
    ⚠️ **check_space より先にやってはいけない。** JPEG のノイズは地との差として出るので、
       占有率と空き矩形の判定が壊れる（地の判定は画素差でやっている）。
    """
    n = 0
    for p in sorted(QA.glob("cut_*.png")):
        Image.open(p).convert("RGB").save(p.with_suffix(".jpg"), quality=q)
        p.unlink()
        n += 1
    (QA / "_empty.png").exists() and (QA / "_empty.png").unlink()
    print(f"検品画像 {n} 枚を JPEG に詰め直した", flush=True)


if __name__ == "__main__":
    mode = "qa"
    zooms = None
    ladder = None
    for a in sys.argv[1:]:
        if a in ("qa", "full", "shrink", "veil"):
            mode = a
        elif a.startswith("--zoom="):
            zooms = set(a.split("=", 1)[1].split(","))
        elif a.startswith("--cuts="):
            ladder = a.split("=", 1)[1].split(",")
    if mode == "shrink":
        shrink_stills()
        sys.exit(0)
    idx, _ = S.layer_index(allow_missing="--partial" in sys.argv)
    meta = meta_of(idx)
    if mode == "veil":
        veil_ladder(idx, meta, ladder)
        sys.exit(0)
    check_motion(meta)
    build_qa(idx, meta, zooms)
    if mode == "full":
        build_full(idx, meta)
