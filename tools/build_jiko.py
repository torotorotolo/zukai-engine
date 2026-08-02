# -*- coding: utf-8 -*-
"""226カットの合成。図解レイヤーとPD写真から30fpsのコマを作る。

■ 動きの設計（映像ルール4：**3秒以上の静止を禁止**）
  段（`{cid}_aN`）は**その段の持ち時間いっぱいをかけて左→右に描かれる**。
  持ち時間 ＝ その段が出てから次の段が出るまで（最後の段はカット終わりまで）。
  → カットのどの瞬間にも「描いている途中の段」が必ず1つある＝**静止区間が構造的に無い**。
  テスト映像のようにカットごとに MOTION を手で書く必要がなくなった
  （手書きは図を動かすたびに直し忘れる。実際 c3 のワイプ範囲で1度やっている）。

  🔴 **動きには必ず情報を運ばせる。装飾の動きは入れない。**
     スライドイン・回転・フラッシュはバラエティの文法なので使わない。

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

from PIL import Image, ImageChops

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
BOOST = {"pr03", "pr09", "c135", "c307", "c308", "c411", "c416",
         "c422", "c424", "c427", "c429", "c624", "c627"}
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


# ── ★実写「動画」を差し込む（2026-08-01 追加） ─────────────────
# 🔴 コマは `python tools/footage.py fetch` が out/jiko/foot/<cid>/ に切り出しておく。
#    **無ければ静止画に落ちる**ので、切り出さないまま焼いてもパイプラインは壊れない。
FOOT = OUT / "foot"
_FOOT_MISS = set()
try:
    import footage as _FO
    _FOOT_USE = _FO.USE
except Exception:                                        # noqa: BLE001
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
            return None
        p = got[-1]
    return Image.open(p).convert("RGB")


def load_photo(name, box):
    """写真は箱の2倍程度まで先に落としておく（4GBのPCでも開けるように）。"""
    src = Image.open(S.HERE / "ref" / name).convert("RGB")
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


def subtitle(fr, cut, t, subs, band=None):
    """黒帯を**常時**貼り、その時刻に出ている字幕行の**文字だけ**を載せる。

    🔴 2026-07-31（試写の指摘③）：帯と文字を1枚のPNGに焼いていたので、
       字幕が切り替わるたびに帯までフェードして**画面がちらついた**。
       帯は全カット共通の1枚（`_subband`）にして貼りっぱなしにする。
       ⚠️ 図の本体は y=892 までなので、帯を常時出しても図には一切かからない。
    """
    if band is not None:
        fr.alpha_composite(band, (0, S.SUB_Y))
    rows = S.SUBS.get(cut)
    if not rows or cut not in subs:
        return fr
    strip = subs[cut]
    for i, r in enumerate(rows):
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


def veil_layer(a):
    """図を読ませるために写真の上に敷く暗幕。**全面 J.BG の一様な板。**

    🔴 2026-07-31（試写の指摘④）。図解は細い線と小さい文字なので、
       写真がそのまま出ていると読めない。濃さは `tools/check_veil.py` が
       「いちばん暗いインクと地とのコントラスト比」を測って決めている。
       ⚠️ グラデーションにしない。薄いところに図が来ると読めなくなるので、
          **どこに図が来ても同じ濃さ**であることのほうが大事。
    """
    k = round(a, 3)
    if k not in _VEIL:
        c = tuple(int(J.BG[i:i + 2], 16) for i in (1, 3, 5))
        _VEIL[k] = Image.new("RGBA", (S.W, S.H), c + (int(255 * k),))
    return _VEIL[k]


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
        fr = duotone(ph, J.BG2, "#e6eef2", boost=cut in BOOST)
        fr.alpha_composite(veil_layer(meta[cut]["veil"]))
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
            # 実写カットでも `xbias` / `zoom` を書けば焼き込みを外せる（既定は今までと同じ）
            ph = fit(src, box, k * (0.35 if box[3] < S.H else 1.0), bias, xb, zm)
        fr.paste(duotone(ph, J.BG2, "#e6eef2", boost=cut in BOOST), (box[0], box[1]))
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
    return fr


def compose(cut, t, dur, lay, photos, meta, subs=None, band=None):
    fr = scene(cut, t, dur, lay, photos, meta)
    return subtitle(fr, cut, t, subs or {}, band)


def load_band():
    """字幕の黒帯。**全カット共通の1枚**なので1回だけ読む。"""
    p = OUT / "_subband.png"
    return Image.open(p).convert("RGBA") if p.exists() else None


def meta_of(idx):
    """カットごとの合成に必要な情報をまとめる。"""
    m = {}
    for cid, v in idx.items():
        m[cid] = {"photo": v["photo"], "back": v["back"], "veil": v["veil"],
                  "span": v["span"],
                  # labk … 骨格を描くのにカットの何割を使うか（既定 LAB_K）。
                  #   段が1つしかない型（作り直した quote）は、既定だと前半で
                  #   描き終わってそのあと画が止まるので、型の側から長めに指定できる。
                  "labk": v.get("labk") or LAB_K,
                  "times": S.stage_times(cid, v["stages"], v.get("holds"))}
        # ★動画を当てたカットの切り方（焼き込みを画面外へ追い出すための寄せ・拡大）
        u = _FOOT_USE.get(cid)
        if u:
            m[cid].update(fxb=u.get("xbias", 0.5), fzm=u.get("zoom", 1.0),
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
    return lay


def qa_shots(cids, idx, meta, at=0.92):
    """カットごとの検品画像。段が出そろった状態を実寸で残す。

    🔴 撮る時刻の選び方で2回まちがえた。
       0.88 … ワイプの途中が写り、図が切れているのか描いている最中か区別がつかない
       0.97 … **字幕が消えたあと**を撮ってしまう（カット尻の TAIL=0.5秒は無音なので
               字幕が出ていない）。占有率が 52.5% → 42.3% と10ポイント落ちた
       0.92 … 段は出そろい、字幕はまだ出ている。**ここが実際の見え方に近い**
    """
    QA.mkdir(parents=True, exist_ok=True)
    secs = dict(S.CUTS)
    subs = {c: L(f"sub_{c}") for c in cids if (OUT / f"sub_{c}.png").exists()}
    lay = _load_layers(cids, idx)
    band = load_band()
    photos = {c: load_photo(S.PHOTO_CUTS[c][1], S.PHOTO_CUTS[c][0])
              for c in cids if idx[c]["photo"]}
    out = []
    for cid in cids:
        sec = secs[cid]
        im = compose(cid, sec * at, sec, lay, photos, meta, subs, band).convert("RGB")
        im.save(QA / f"cut_{cid}.png")
        out.append((cid, im))
    return out


def _seg_worker(args):
    """1カットぶんを mp4 に焼く。**プロセスを分けて並列に回す**。

    🔴 `nframes` は呼び出し側が**通し時刻から**計算して渡す。
       カットごとに round(sec*30) すると丸め誤差が積み上がり、34分の終わりでは
       音と数秒ずれる（226カット × 最大0.5コマ）。音声側は正確な秒で置いているので、
       映像の側を通し時刻に合わせる。
    """
    cid, sec, nframes, idxv, metav = args
    import scene_jiko as S2
    lay = {n: Image.open(OUT / f"{n}.png").convert("RGBA") for n in idxv["layers"]}
    subs = {}
    if (OUT / f"sub_{cid}.png").exists():
        subs[cid] = Image.open(OUT / f"sub_{cid}.png").convert("RGBA")
    photos = {}
    if idxv["photo"]:
        photos[cid] = load_photo(S2.PHOTO_CUTS[cid][1], S2.PHOTO_CUTS[cid][0])
    band = load_band()
    meta = {cid: metav}
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
        args.append((cid, secs[cid], b - a, idx[cid], meta[cid]))
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
    for pre in ("pr", "c1", "c2", "c3", "c4", "c5", "c6", "ep"):
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
    if (OUT / "_empty.png").exists():
        L("_empty").convert("RGB").save(QA / "_empty.png")
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
    for pre, label in (("pr", "プロローグ"), ("c1", "1章"), ("c2", "2章"), ("c3", "3章"),
                       ("c4", "4章"), ("c5", "5章"), ("c6", "6章"), ("ep", "エピローグ")):
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
    photos = {c: load_photo(S.PHOTO_CUTS[c][1], S.PHOTO_CUTS[c][0]) for c in cids}
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
