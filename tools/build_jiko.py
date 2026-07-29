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

from PIL import Image

import scene_jiko as S
import jiko_style as J

FPS = 30
OUT = S.HERE / "out" / "jiko"
FR = OUT / "frames"
QA = OUT / "qa"

# 検品で必ず拡大して見る場所。(カット, 時刻の割合, 名前, 切り出し矩形)
ZOOMS = [
    ("c2", 0.95, "機体-機首と操縦室", (150, 480, 640, 760)),
    ("c2", 0.95, "機体-主翼とエンジン", (460, 540, 1010, 800)),
    ("c2", 0.95, "機体-尾翼", (880, 320, 1300, 660)),
    ("c2", 0.95, "機体-剥離範囲", (300, 480, 800, 720)),
    ("c2", 0.95, "写真インセット", (1300, 270, 1880, 700)),
    ("c4", 0.95, "重ね継手-段差", (240, 560, 1220, 800)),
    ("c4", 0.95, "重ね継手-亀裂", (240, 500, 1220, 660)),
    ("c5", 0.95, "断面-接着層とリベット", (420, 400, 1340, 720)),
    ("p1", 0.95, "写真-枠と出典", (120, 780, 1250, 900)),
    ("p3", 0.95, "写真-調査員", (140, 250, 960, 880)),
    ("c7", 0.99, "数字", (300, 400, 1620, 800)),
    ("c3", 0.40, "断面-裂けていく途中", (900, 240, 1900, 700)),
    ("c5", 0.45, "断面-接着が剥がれる途中", (420, 400, 1340, 720)),
    ("c6", 0.45, "高度-折れ線を描く途中", (200, 300, 1720, 900)),
    ("c3", 0.92, "断面-完成", (240, 200, 1900, 900)),
    ("c2", 0.55, "字幕-図解の上", (300, 900, 1620, 1040)),
    ("p3", 0.55, "字幕-写真の上", (300, 900, 1620, 1040)),
]


BOOST = {"p4"}          # 元が低コントラストで沈む写真（NASAの衛星画像）


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


def wipe(fr, layer, k, soft=90):
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
    x = int(S.W * k)
    m = Image.new("L", cr.size, 0)
    m.paste(255, (0, 0, max(0, x - soft), S.H))
    if soft and x > 0:
        # 端をぼかす。硬い縁で切ると「シャッターが降りる」ように見える
        grad = Image.linear_gradient("L").rotate(90, expand=True).resize((soft, S.H))
        m.paste(grad, (max(0, x - soft), 0))
    cr.putalpha(Image.composite(cr.getchannel("A"), m, m))
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


def scene(cut, t, dur, lay, photos, numcells):
    """字幕を除いた画面。"""
    av = max(0.0, min(1.0, (t - 0.5) / 1.1))          # 注記は0.5秒後から1.1秒かけて
    pulse = 0.55 + 0.45 * (0.5 + 0.5 * math.sin(t * math.tau / 1.35))
    if cut in S.PHOTO_CUTS:
        box, _, bias = S.PHOTO_CUTS[cut]
        fr = lay[f"{cut}_bg"].copy()
        ph = fit(photos[cut], box, t / max(dur, 0.001), bias)
        fr.paste(duotone(ph, J.BG2, "#e6eef2", boost=cut in BOOST), (box[0], box[1]))
        return over(fr, lay[f"{cut}_over"], min(1.0, t / 0.4))
    fr = lay[f"{cut}_base"].copy()
    if cut in S.INSETS:
        box, _ = S.INSETS[cut]
        fr.paste(duotone(fit(photos[cut], box), J.BG2, "#e6eef2"), (box[0], box[1]))
    if cut == "c2":
        # 穴は一度だけ開く。**縁だけを脈打たせる**（穴を明滅させると嘘に見える）
        over(fr, lay["c2_hole"], min(1.0, max(0.0, (t - 0.3) / 0.5)))
        over(fr, lay["c2_tearline"], min(1.0, max(0.0, (t - 0.3) / 0.5)) * pulse)
        return over(fr, lay["c2_anno"], av)
    if cut == "c4":
        # 亀裂は左から順に現れる。「進行」に見せる
        wipe(fr, lay["c4_crack"], rev(t, dur, 0.4, 0.66))
        return over(fr, lay["c4_anno"], max(0.0, min(1.0, (t - 1.8) / 1.1)))
    if cut == "c3":
        # 上部が「裂けて広がっていく」。円周55%という情報を運ぶ動き
        wipe(fr, lay["c3_arc"], rev(t, dur, 0.6, 0.62))
        return over(fr, lay["c3_anno"], av)
    if cut == "c5":
        # 接着が左から剥がれ、そのあと亀裂が出る。**因果の順に**動かす
        # 接着は全部は剥がさない。**緑を少し残す**と「接着層」のラベルが意味を保つ
        wipe(fr, lay["c5_bond"], rev(t, dur, 1.2, 0.50) * 0.78, soft=140)
        over(fr, lay["c5_crack"], rev(t, dur, dur * 0.62, 0.10) * pulse)
        return over(fr, lay["c5_anno"], av)
    if cut == "c6":
        # 高度の折れ線を左から描く。離陸→巡航→剥離→緊急降下→着陸が時間軸で追える
        wipe(fr, lay["c6_line"], rev(t, dur, 0.4, 0.76))
        over(fr, lay["c6_mark"], rev(t, dur, dur * 0.34, 0.06) * pulse)
        return over(fr, lay["c6_anno"], max(0.0, min(1.0, (t - 2.2) / 1.1)))
    if cut == "c7":
        k = max(0.0, min(1.0, (t - 0.3) / 2.6))
        fr.alpha_composite(numcells[min(11, int(k * 11.999))])
        return fr
    return over(fr, lay[f"{cut}_anno"], av)


def compose(cut, t, dur, lay, photos, numcells, subs=None):
    fr = scene(cut, t, dur, lay, photos, numcells)
    return subtitle(fr, cut, t, subs or {})


def check_no_freeze(limit=3.0):
    """**3秒以上、画面に何の変化も無い区間**が無いかを機械的に確認する。
    ゆっくりズームは常に動いているので厳密には静止しないが、
    「読むものが変わらない時間」が長いと離脱するので、字幕と注記の切り替わりで測る。"""
    events, t = [], 0.0
    for cut, sec in S.CUTS:
        events.append((t, f"{cut} 開始"))
        for r in S.SUBS.get(cut, []):
            events.append((t + S.LEAD + r["t"], f"{cut} 字幕「{r['text'][:14]}」"))
        t += sec
    events.append((t, "終端"))
    events.sort()
    worst, bad = 0.0, []
    for (a, na), (b, _) in zip(events, events[1:]):
        if b - a > worst:
            worst = b - a
        if b - a > limit:
            bad.append((round(a, 2), round(b - a, 2), na))
    print(f"最長の無変化区間 = {worst:.2f}秒")
    for at, d, na in bad:
        print(f"  🔴 {at}秒から {d}秒 変化なし（直前: {na}）")
    if not bad:
        print(f"✓ {limit}秒以上の静止なし")
    return bad


def build():
    FR.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    names = ["p1_bg", "p1_over", "p2_bg", "p2_over", "p3_bg", "p3_over",
             "p4_bg", "p4_over",
             "c2_base", "c2_hole", "c2_tearline", "c2_anno", "c3_base", "c3_anno",
             "c3_arc", "c4_base", "c4_crack", "c4_anno",
             "c5_base", "c5_crack", "c5_bond", "c5_anno",
             "c6_base", "c6_line", "c6_mark", "c6_anno", "c7_base"]
    lay = {k: L(k) for k in names}
    photos = {c: load_photo(f, b) for c, (b, f, _) in S.PHOTO_CUTS.items()}
    photos.update({c: load_photo(f, b) for c, (b, f) in S.INSETS.items()})
    subs = {c: L(f"sub_{c}") for c in S.SUBS if (OUT / f"sub_{c}.png").exists()}
    print(f"字幕帯 {len(subs)}カット", flush=True)
    check_no_freeze()
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
        qa = compose(cut, sec * 0.60, sec, lay, photos, numcells, subs).convert("RGB")
        qa.save(QA / f"cut_{cut}.png")
        sheet.append(qa.copy())
        print(f"cut {cut}: {total}", flush=True)
    for cut, k, name, box in ZOOMS:
        sec = dict(S.CUTS)[cut]
        im = compose(cut, sec * k, sec, lay, photos, numcells, subs).convert("RGB")
        c = im.crop(box)
        c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
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
