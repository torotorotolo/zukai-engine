# -*- coding: utf-8 -*-
"""事故検証テストの合成。図解レイヤーとPD写真から30fpsのコマを作る。

■ 図解様式で「意図に見える」動きは4つだけ
  1 注記が順に出る（フェード）
  2 破断部・亀裂が脈打つ／左から進む
  3 数字が数え上がる
  4 写真だけ、ごくゆっくり寄る
人が動く必要が無いので、カメラは固定でよい。図解カットはズームもしない。

■ 検品用の出力
  `out/jiko/qa/` に **クラウドで焼いた実物**の静止画と拡大図を書き出す。
  ローカルのフォントとクラウドのフォントで折返し位置が変わった実績があるので、
  検品はここに出たものだけを見る。
"""
import math
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image

import scene_jiko as S
import jiko_style as J

FPS = 30
OUT = S.HERE / "out" / "jiko"
FR = OUT / "frames"
QA = OUT / "qa"

# 検品で必ず拡大して見る場所。(カット, 時刻の割合, 名前, 切り出し矩形)
ZOOMS = [
    ("c2", 0.95, "機体-機首と操縦室", (150, 470, 620, 740)),
    ("c2", 0.95, "機体-主翼とエンジン", (480, 540, 1010, 790)),
    ("c2", 0.95, "機体-尾翼", (900, 300, 1300, 640)),
    ("c2", 0.95, "機体-剥離範囲", (300, 430, 780, 700)),
    ("c4", 0.95, "重ね継手-段差", (240, 620, 1200, 860)),
    ("c5", 0.95, "断面-接着層とリベット", (560, 440, 1360, 700)),
    ("p1", 0.95, "写真-枠と出典", (120, 760, 1240, 900)),
    ("c7", 0.99, "数字", (300, 400, 1620, 800)),
]


def L(name):
    return Image.open(OUT / f"{name}.png").convert("RGBA")


def duotone(im, dark, light):
    """写真を配色に合わせる。生の白黒のまま置くと図解から浮く。"""
    g = im.convert("L")
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


def ken_burns(src, box, k):
    """ごくゆっくり寄る。図解カットは動かさないので、ここだけが息をする。"""
    _, _, w, h = box
    sw, sh = src.size
    z = max(w / sw, h / sh) * (1.0 + 0.055 * k)
    cw, ch = min(sw, w / z), min(sh, h / z)
    l, t = (sw - cw) / 2, (sh - ch) / 2
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


def compose(cut, t, dur, lay, photos, numcells):
    """1コマぶんを合成して返す。"""
    av = max(0.0, min(1.0, (t - 0.5) / 1.1))          # 注記は0.5秒後から1.1秒かけて
    pulse = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * math.tau / 1.35))
    if cut in S.PHOTO_CUTS:
        box, _ = S.PHOTO_CUTS[cut]
        fr = lay[f"{cut}_bg"].copy()
        ph = ken_burns(photos[cut], box, t / max(dur, 0.001))
        fr.paste(duotone(ph, J.BG2, "#e6eef2"), (box[0], box[1]))
        fr.alpha_composite(fade(lay[f"{cut}_over"], min(1.0, t / 0.4)) or lay[f"{cut}_over"])
        return fr
    if cut == "c2":
        fr = lay["c2_base"].copy()
        p = fade(lay["c2_tear"], min(1.0, max(0.0, (t - 0.3) / 0.6)) * pulse)
        if p:
            fr.alpha_composite(p)
        p = fade(lay["c2_anno"], av)
        if p:
            fr.alpha_composite(p)
        return fr
    if cut == "c4":
        fr = lay["c4_base"].copy()
        # 亀裂は左から順に現れる。ワイプで出すと「進行」に見える
        k = max(0.0, min(1.0, (t - 0.4) / 2.2))
        if k > 0:
            cr = lay["c4_crack"].copy()
            m = Image.new("L", cr.size, 0)
            m.paste(255, (0, 0, int(S.W * k), S.H))
            cr.putalpha(Image.composite(cr.getchannel("A"), m, m))
            fr.alpha_composite(cr)
        p = fade(lay["c4_anno"], max(0.0, min(1.0, (t - 1.8) / 1.1)))
        if p:
            fr.alpha_composite(p)
        return fr
    if cut == "c5":
        fr = lay["c5_base"].copy()
        p = fade(lay["c5_crack"], max(0.0, min(1.0, (t - 2.4) / 0.8)) * pulse)
        if p:
            fr.alpha_composite(p)
        p = fade(lay["c5_anno"], av)
        if p:
            fr.alpha_composite(p)
        return fr
    if cut == "c7":
        fr = lay["c7_base"].copy()
        k = max(0.0, min(1.0, (t - 0.3) / 2.6))
        fr.alpha_composite(numcells[min(11, int(k * 11.999))])
        return fr
    fr = lay[f"{cut}_base"].copy()
    p = fade(lay[f"{cut}_anno"], av)
    if p:
        fr.alpha_composite(p)
    return fr


def build():
    FR.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    names = ["p1_bg", "p1_over", "p2_bg", "p2_over",
             "c2_base", "c2_tear", "c2_anno", "c3_base", "c3_anno",
             "c4_base", "c4_crack", "c4_anno", "c5_base", "c5_crack", "c5_anno",
             "c6_base", "c6_anno", "c7_base"]
    lay = {k: L(k) for k in names}
    photos = {c: load_photo(f, b) for c, (b, f) in S.PHOTO_CUTS.items()}
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
            fr = compose(cut, f / FPS, sec, lay, photos, numcells)
            fr.convert("RGB").save(FR / f"{n:05d}.jpg", quality=93)
            n += 1
        # 検品用：そのカットの終盤（注記が出そろった状態）を実寸で残す
        qa = compose(cut, sec * 0.95, sec, lay, photos, numcells).convert("RGB")
        qa.save(QA / f"cut_{cut}.png")
        sheet.append((cut, qa.copy()))
        print(f"cut {cut}: {total}", flush=True)
    # 拡大図
    for cut, k, name, box in ZOOMS:
        sec = dict(S.CUTS)[cut]
        im = compose(cut, sec * k, sec, lay, photos, numcells).convert("RGB")
        c = im.crop(box)
        c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
        c.save(QA / f"zoom_{cut}_{name}.png")
    # 一覧
    tw = 640
    th = round(tw * S.H / S.W)
    sh = Image.new("RGB", (tw * 2, th * ((len(sheet) + 1) // 2)), "#000")
    for i, (_, im) in enumerate(sheet):
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
