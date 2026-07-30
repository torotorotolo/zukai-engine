# -*- coding: utf-8 -*-
"""事故検証テストの合成。図解レイヤーとPD写真から30fpsのコマを作る。

■ 動きの設計（2026-07-30 指示：**3秒以上の静止禁止**）
  1 字幕が2〜3秒ごとに切り替わる  ← いちばん効くのはこれ
  2 注記が順に出る（フェード）
  3 破断部の縁・亀裂が脈打つ／左から進む
  4 数字が数え上がる
  5 図やグラフ自体が「描かれていく」（破断の弧・高度の折れ線・接着の剥離）
  6 実写カットはごくゆっくり寄る（ケンバーンズ）

🔴 **動きには必ず情報を運ばせる。装飾の動きは入れない。**
   4巡目に入れた「2%のゆっくりズーム」は何も説明していない装飾だったので5巡目で外した。
   スライドイン・回転・フラッシュはバラエティの文法なので使わない。
   `check_no_freeze()` で無変化区間を機械的に測っている。

■ 検品用の出力
  `out/jiko/qa/` に **クラウドで焼いた実物**の静止画と拡大図を書き出す。
  ローカルのWindowsフォントとクラウドのフォントで折返し位置が変わった実績があるので、
  検品はここに出たものだけを見る。
"""
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image, ImageChops

import scene_jiko as S
import jiko_style as J

FPS = 30
OUT = S.HERE / "out" / "jiko"
FR = OUT / "frames"
QA = OUT / "qa"

# 検品で必ず拡大して見る場所。(カット, 時刻の割合, 名前, 切り出し矩形)
# 🔴 15巡目でレイアウトを組み直したので、切り出し矩形も全部取り直した。
#    「余白を詰めた」ぶん要素が近づくので、**隣とぶつかっていないか**を見る箇所を増やした。
ZOOMS = [
    ("c2", 0.95, "機体-機首と操縦室", (60, 560, 580, 820)),
    ("c2", 0.95, "機体-主翼とエンジン", (470, 610, 900, 840)),
    ("c2", 0.95, "機体-尾翼", (880, 330, 1290, 690)),
    ("c2", 0.95, "機体-剥離範囲と5.5m", (200, 280, 720, 720)),
    ("c2", 0.95, "写真インセットと圧力差", (1250, 210, 1880, 890)),
    ("c4", 0.95, "重ね継手-段差", (260, 560, 1220, 700)),
    ("c4", 0.95, "重ね継手-亀裂", (260, 470, 1220, 620)),
    ("c4", 0.95, "情報柱-右", (1200, 300, 1880, 860)),
    ("c5", 0.95, "断面-接着層とリベット", (700, 400, 1260, 700)),
    ("c5", 0.95, "断面-外気側と客室側", (60, 210, 1880, 900)),
    ("p1", 0.95, "写真-出典を内側に入れた下端", (60, 790, 1200, 900)),
    ("p1", 0.95, "情報柱-右", (1180, 230, 1880, 900)),
    ("p2", 0.95, "情報柱-左", (60, 230, 760, 900)),
    ("p3", 0.95, "写真-調査員", (72, 240, 900, 880)),
    ("p4", 0.95, "情報柱-左", (60, 230, 760, 900)),
    ("c7", 0.99, "数字と棒-右", (930, 260, 1840, 810)),
    ("c7", 0.99, "数字と棒-左", (90, 260, 1000, 810)),
    ("c3", 0.40, "断面-裂けていく途中", (1030, 250, 1700, 900)),
    ("c3", 0.92, "断面-客室と座席", (200, 250, 860, 900)),
    ("c5", 0.45, "断面-接着が剥がれる途中", (700, 400, 1260, 700)),
    ("c6", 0.45, "高度-折れ線を描く途中", (220, 260, 1140, 900)),
    ("c6", 0.95, "高度-右端と13分", (900, 260, 1830, 900)),
    ("c2", 0.55, "字幕-図解の上", (300, 900, 1620, 1040)),
    ("p3", 0.55, "字幕-写真の上", (300, 900, 1620, 1040)),
]


BOOST = {"p4"}          # 元が低コントラストで沈む写真（NASAの衛星画像）

# ワイプを進める x 範囲。**その図が実際に占めている幅**を渡す（全幅にすると空回りする）
# ⚠️ レイアウトを動かしたら**必ずここも直す**。図がずれた分だけワイプが空回りする。
_R3 = 200 * S.SEC_R
C3_ARC_SPAN = (S.SEC_RT - _R3 * 0.97, S.SEC_RT + _R3 * 0.97)   # 右の断面の破断の弧
LJ_X_SPAN = (S.LJ_X - 480 * S.LJ_S, S.LJ_X + 480 * S.LJ_S)     # 重ね継手の平面図
C5_BOND_SPAN = (S.SEC_X - S.SEC_HL - 30, S.SEC_X + S.SEC_HL + 30)  # A-A断面の接着層
C6_LINE_SPAN = (S.GX, S.GX + S.GW)                             # 高度グラフの枠


def L(name):
    return Image.open(OUT / f"{name}.png").convert("RGBA")


def duotone(im, dark, light, boost=False):
    """写真を配色に合わせる。生の白黒のまま置くと図解から浮く。

    boost=True で先にコントラストを立てる。衛星画像や航路図は元が低コントラストで、
    そのままデュオトーンにすると暗く沈んで島の形が読めなかった（6巡目の粗）。
    """
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


def load_photo(name, box):
    """写真は箱の2倍程度まで先に落としておく（4GBのPCでも開けるように）。"""
    src = Image.open(S.HERE / "ref" / name).convert("RGB")
    lim = box[2] * 2
    if src.width > lim:
        src = src.resize((lim, round(src.height * lim / src.width)), Image.LANCZOS)
    return src


def fit(src, box, k=0.0, bias=0.5):
    """箱を覆うように切り出す。k>0 でゆっくり寄る。bias は縦方向の寄せ。"""
    _, _, w, h = box
    sw, sh = src.size
    z = max(w / sw, h / sh) * (1.0 + 0.055 * k)
    cw, ch = min(sw, w / z), min(sh, h / z)
    l, t = (sw - cw) / 2, (sh - ch) * bias
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


def rev(t, dur, start_sec, span_frac):
    """0→1 の進み具合。**start_sec は秒、span_frac はカット尺に対する割合**。

    5巡目は span も秒で固定していたので、折れ線が最初の3.8秒で描き終わり、
    残り6秒は図が止まっていた（尺はナレーションから取るので毎回変わる）。
    尺に比例させれば、図の動きが常に喋りに付いていく。
    """
    return max(0.0, min(1.0, (t - start_sec) / max(0.2, span_frac * dur)))


def wipe(fr, layer, k, soft=90, span=None):
    """レイヤーを**左から右へ**現す。図が「引かれていく／裂けていく／剥がれていく」動きになる。

    🔴 動きの原則（2026-07-30 カズヤくんと確認）：
       **動きには必ず情報を運ばせる。装飾の動きは入れない。**
       4巡目に入れた「2%のゆっくりズーム」は何も説明していない装飾だったので外した。
       代わりに、破断の弧・高度の折れ線・接着の剥離を**左から描いていく**。
       これは「調査している」感触そのもので、検証番組の文法から外れない。
    """
    if k <= 0.0:
        return fr
    if k >= 1.0:
        return over(fr, layer)
    cr = layer.copy()
    # 🔴 11巡目まで画面全幅(0〜1920)を横断させていた。そのため、たとえば c3 の
    #    破断の弧は画面右側(1140〜1620)にしか無く、**ワイプの travel の6割が空白に費われて**
    #    弧が動き始めるのがカットの後半になっていた。図ごとの x 範囲で進める。
    x0, x1 = span or (0, S.W)
    x = int(x0 + (x1 - x0) * k)
    m = Image.new("L", cr.size, 0)
    m.paste(255, (0, 0, max(0, x - soft), S.H))
    if soft and x > 0:
        # 端をぼかす。硬い縁で切ると「シャッターが降りる」ように見える。
        # 🔴 9巡目まで `linear_gradient("L").rotate(90)` を使っていたが、これは
        #    **左が0・右が255**＝必要な向きの逆だった（実測で確認）。
        #    そのため reveal の縁の手前に「暗い帯」が出て、
        #    c3〜c6 の全ワイプに縦の筋が入っていた。明示的に作り直す。
        grad = Image.new("L", (soft, 1))
        grad.putdata([255 - round(255 * i / max(1, soft - 1)) for i in range(soft)])
        m.paste(grad.resize((soft, S.H)), (max(0, x - soft), 0))
    # 🔴 10巡目まで `Image.composite(alpha, m, m)` を使っていた。これは
    #    **マスクが中間値のとき、レイヤーの透明画素まで半不透明になる**
    #    （composite(0, 128, 128) = 64）。透明部分の下地は黒なので、
    #    ぼかし帯のところに**縦の暗い帯**が出ていた。正しくは不透明度の掛け算。
    cr.putalpha(ImageChops.multiply(cr.getchannel("A"), m))
    fr.alpha_composite(cr)
    return fr


def subtitle(fr, cut, t, subs):
    """その時刻に出ている字幕行を1枚だけ載せる。"""
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


def steps(fr, cut, t, lay):
    """図のラベルは頭から出し、注記は**ナレーションの行に同期して**順に出す。

    🔴 2026-07-30 カズヤくん指摘：
       「図内に文字が多いパートは、ナレーションに合わせて順番に表示した方が、
        視聴者も注視すべき場所が明らかになって見やすい」
       `{cut}_lab` = 図そのもののラベル（寸法・部位名）→ カット頭から
       `{cut}_aN`  = ナレーション N 行目に同期する注記 → その行が始まってから
    """
    if f"{cut}_lab" in lay:
        over(fr, lay[f"{cut}_lab"], min(1.0, max(0.0, (t - 0.15) / 0.5)))
    for i, r in enumerate(S.SUBS.get(cut, [])):
        key = f"{cut}_a{i + 1}"
        if key not in lay:
            continue
        start = r["t"] + S.LEAD
        over(fr, lay[key], max(0.0, min(1.0, (t - start) / 0.45)))
    return fr


def scene(cut, t, dur, lay, photos, numcells):
    """字幕を除いた画面。"""
    pulse = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * math.tau / 1.35))
    if cut in S.PHOTO_CUTS:
        box, _, bias = S.PHOTO_CUTS[cut]
        fr = lay[f"{cut}_bg"].copy()
        ph = fit(photos[cut], box, t / max(dur, 0.001), bias)
        fr.paste(duotone(ph, J.BG2, "#e6eef2", boost=cut in BOOST), (box[0], box[1]))
        return steps(fr, cut, t, lay)
    fr = lay[f"{cut}_base"].copy()
    if cut in S.INSETS:
        box, _ = S.INSETS[cut]
        fr.paste(duotone(fit(photos[cut], box), J.BG2, "#e6eef2"), (box[0], box[1]))
    if cut == "c2":
        # 穴は一度だけ開く。**縁だけを脈打たせる**（穴を明滅させると嘘に見える）
        over(fr, lay["c2_hole"], min(1.0, max(0.0, (t - 0.3) / 0.5)))
        over(fr, lay["c2_tearline"], min(1.0, max(0.0, (t - 0.3) / 0.5)) * pulse)
        return steps(fr, cut, t, lay)
    if cut == "c4":
        # 亀裂は左から順に現れる。「進行」に見せる
        wipe(fr, lay["c4_crack"], rev(t, dur, 0.4, 0.84), span=LJ_X_SPAN)
        return steps(fr, cut, t, lay)
    if cut == "c3":
        # 上部が「裂けて広がっていく」。円周55%という情報を運ぶ動き
        wipe(fr, lay["c3_arc"], rev(t, dur, 0.6, 0.82), span=C3_ARC_SPAN)
        steps(fr, cut, t, lay)
        # 「ここが消えた」の引き出し線は弧の右端を指すので、**弧が届いてから**出す。
        # 9巡目は注記が先に出て、線が何も無い所を指していた。
        return over(fr, lay["c3_call"], rev(t, dur, dur * 0.72, 0.10))
    if cut == "c5":
        # 接着が左から剥がれ、そのあと亀裂が出る。**因果の順に**動かす
        # 接着は全部は剥がさない。**緑を少し残す**と「接着層」のラベルが意味を保つ
        wipe(fr, lay["c5_bond"], rev(t, dur, 1.2, 0.50) * 0.78, soft=90,
             span=C5_BOND_SPAN)
        over(fr, lay["c5_crack"], rev(t, dur, dur * 0.62, 0.10) * pulse)
        return steps(fr, cut, t, lay)
    if cut == "c6":
        # 高度の折れ線を左から描く。離陸→巡航→剥離→緊急降下→着陸が時間軸で追える
        wipe(fr, lay["c6_line"], rev(t, dur, 0.4, 0.76), span=C6_LINE_SPAN)
        over(fr, lay["c6_mark"], rev(t, dur, dur * 0.34, 0.06) * pulse)
        return steps(fr, cut, t, lay)
    if cut == "c7":
        # 数え上がりはカット尺の7割。9割だと最終値が0.5秒しか出ず、読む間が無かった
        k = rev(t, dur, 0.3, 0.70)
        fr.alpha_composite(numcells[min(11, int(k * 11.999))])
        return fr
    return steps(fr, cut, t, lay)


def compose(cut, t, dur, lay, photos, numcells, subs=None):
    fr = scene(cut, t, dur, lay, photos, numcells)
    return subtitle(fr, cut, t, subs or {})


# カットごとの「図が動いている区間」。(開始秒, 終わりの割合) で表す。
# 🔴 2026-07-30：静止禁止は**図とグラフの動きだけ**で満たす（字幕には適用しない）。
#    字幕を3秒以下に細切れにするのは「見にくい」と判定されて撤回した。
MOTION = {
    "c2": (0.3, 1.00),   # 破断の縁が常に脈打つ
    "c3": (0.6, 0.82),   # 破断の弧を描く
    "c4": (0.4, 0.84),   # 亀裂が左から進む
    "c5": (1.2, 1.00),   # 接着が剥がれ → 亀裂が脈打つ
    "c6": (0.4, 1.00),   # 折れ線を描く → 剥離点が脈打つ
    "c7": (0.3, 0.70),   # 数字が数え上がる
}


def check_motion(limit=3.0):
    """**3秒以上、図がまったく動かない区間**が無いかを機械的に確認する。

    実写カットはケンバーンズで常に動いているので対象外。
    図解カットは MOTION の区間だけ動くので、その前後の空白を測る。
    """
    bad, worst = [], 0.0
    for cut, sec in S.CUTS:
        if cut in S.PHOTO_CUTS:
            continue
        st, frac = MOTION.get(cut, (0.0, 0.0))
        end = st + frac * sec
        gaps = [("頭", st), ("尻", max(0.0, sec - end))]
        for where, g in gaps:
            worst = max(worst, g)
            if g > limit:
                bad.append((cut, where, round(g, 2), round(sec, 2)))
    print(f"図が動かない最長区間 = {worst:.2f}秒")
    for cut, where, g, sec in bad:
        print(f"  🔴 {cut}（尺{sec}秒）の{where}が {g}秒 動かない")
    if not bad:
        print(f"✓ 図が {limit}秒以上止まるカットは無い")
    # 字幕は参考情報として長さだけ出す
    longest = max(((r["d"], r["text"]) for rows in S.SUBS.values() for r in rows),
                  default=(0, ""))
    print(f"（参考）最長の字幕 = {longest[0]:.2f}秒「{longest[1][:26]}」"
          f" ／ 字幕の枚数 {sum(len(r) for r in S.SUBS.values())}")
    return bad


def build():
    FR.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    names = ["p1_bg", "p1_lab", "p1_a1", "p1_a2",
             "p2_bg", "p2_lab", "p2_a1",
             "c2_base", "c2_hole", "c2_tearline", "c2_lab", "c2_a1", "c2_a2",
             "p3_bg", "p3_lab", "p3_a1", "p3_a2",
             "c3_base", "c3_arc", "c3_lab", "c3_call",
             "c4_base", "c4_crack", "c4_lab", "c4_a1", "c4_a2", "c4_a3",
             "c5_base", "c5_crack", "c5_bond", "c5_lab", "c5_a1", "c5_a3",
             "p4_bg", "p4_lab", "p4_a1",
             "c6_base", "c6_line", "c6_mark", "c6_lab", "c6_a1", "c6_a2",
             "c7_base"]
    lay = {k: L(k) for k in names}
    photos = {c: load_photo(f, b) for c, (b, f, _) in S.PHOTO_CUTS.items()}
    photos.update({c: load_photo(f, b) for c, (b, f) in S.INSETS.items()})
    subs = {c: L(f"sub_{c}") for c in S.SUBS if (OUT / f"sub_{c}.png").exists()}
    print(f"字幕帯 {len(subs)}カット", flush=True)
    check_motion()
    nums = L("c7_num")
    cw, ch = S.W // 2, S.H // 2
    numcells = [nums.crop(((i % 4) * cw, (i // 4) * ch, (i % 4) * cw + cw,
                           (i // 4) * ch + ch)).resize((S.W, S.H), Image.LANCZOS)
                for i in range(12)]
    n = 0
    sheet = []
    for cut, sec in S.CUTS:
        total = int(round(sec * FPS))
        for f in range(total):
            fr = compose(cut, f / FPS, sec, lay, photos, numcells, subs)
            fr.convert("RGB").save(FR / f"{n:05d}.jpg", quality=93)
            n += 1
        # 検品用：そのカットの終盤（注記が出そろった状態）を実寸で残す
        qa = compose(cut, sec * 0.88, sec, lay, photos, numcells, subs).convert("RGB")
        qa.save(QA / f"cut_{cut}.png")
        sheet.append(qa.copy())
        print(f"cut {cut}: {total}", flush=True)
    # 地の基準画像。`tools/check_space.py` が余白を測るのに使う（差分で「地のまま」を判定）
    if (OUT / "_empty.png").exists():
        L("_empty").convert("RGB").save(QA / "_empty.png")
    for cut, k, name, box in ZOOMS:
        sec = dict(S.CUTS)[cut]
        im = compose(cut, sec * k, sec, lay, photos, numcells, subs).convert("RGB")
        c = im.crop(box)
        # 2倍が既定。ただし画面をまたぐ広い切り出しは 1920×1080 に収まる倍率まで落とす
        z = min(2.0, S.W / c.width, S.H / c.height)
        if z > 1.02:
            c = c.resize((round(c.width * z), round(c.height * z)), Image.LANCZOS)
        c.save(QA / f"zoom_{cut}_{name}.png")
    tw = 640
    th = round(tw * S.H / S.W)
    sh = Image.new("RGB", (tw * 2, th * ((len(sheet) + 1) // 2)), "#000")
    for i, im in enumerate(sheet):
        sh.paste(im.resize((tw, th), Image.LANCZOS), ((i % 2) * tw, (i // 2) * th))
    sh.save(QA / "contact.jpg", quality=90)
    print("total", n, flush=True)
    return n


if __name__ == "__main__":
    n = build()
    mp4 = OUT / "jiko_test.mp4"
    subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                    "-framerate", str(FPS), "-i", str(FR / "%05d.jpg"),
                    "-vf", "format=yuv420p", "-c:v", "libx264", "-preset", "medium",
                    "-crf", "19", "-movflags", "+faststart", str(mp4)], check=True)
    print("wrote", mp4, round(n / FPS, 1), "sec")
