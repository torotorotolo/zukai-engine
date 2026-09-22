#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""事故検証ch のサムネの「地の絵」を OpenAI 画像APIで作る（A/Bテスト用）。

🔴 2026-09-21 カズヤくん指示で全面改訂：
   「できるだけ写真に近い質感で、事件の悲劇が伝わるデザイン」「背景も含め実際の写真のように」
   「既存の OpenAI API を使ったサムネ生成ルールは**別チャンネルのものなので完全に無視**」
   → 心理ch のクレイ調・色の役割分担（赤と白は絵に使わない等）は**一切引き継がない**。
     ここは事故検証ch 専用の、実写の報道写真を作る道具。

🔴 文字は作らせない。**地だけ**を作り、赤1行・黄1行は `thumb_jiko.py` で焼く
   （日本語の字形が崩れる／型の画素指定を守れないため）。

⚠️ 人は描かせない。実在の被害者を捏造しないため（火・煙・血・遺体も描かせない）。

⚠️ 焼き込み側（fx_type の "e_veil"）があとから絵の上に足すもの:
     ・上 230px に暗幕（0.42→0）・四隅にビネット（0→0.55）・下 260px に影（0.46→0）
   ＝ 絵が主役として効くのは **y175〜510（全体の47%）**。

使い方:
  python tools/gen_thumb_ai.py c --dry     # 文面だけ（無料）
  python tools/gen_thumb_ai.py c           # ★課金 約$0.2
"""
import base64
import io
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "ref" / "ep10" / "ai"
API = "https://api.openai.com/v1/images/generations"
MODEL = "gpt-image-2.5-flare"       # 2026-09-21 に GET /v1/models で在庫を確認ずみ
SIZE = "1792x1008"                  # 16:9。1280x720 へ縮めるだけで切り取りが出ない
QUALITY = "high"                    # ⚠️ xhigh/max は出力トークンが増えて高くなる

KEY_CANDIDATES = [
    Path(r"C:\Users\konar\Desktop\psych-channel\pipeline\config\openai_key.txt"),
    Path(r"C:\Users\konar\Desktop\zankoku-sekkeizu\config\openai_key.txt"),
    Path(r"C:\Users\konar\Desktop\data-geo-channel\config\openai_key.txt"),
    Path(r"F:\00_C退避_20260807\撤退チャンネル\data-geo-channel\config\openai_key.txt"),
]

# ── 質感：実写の報道写真 ─────────────────────────────────────────────────────
LOOK = (
    "A real PHOTOGRAPH, indistinguishable from documentary press photography. "
    "Shot on a full-frame 35mm camera, natural flat overcast daylight, no sunshine, "
    "no artificial lighting, slightly desaturated, fine natural film grain, true "
    "photographic depth of field and lens falloff. Physically accurate materials: "
    "rough fractured concrete, powdered dust, dull steel, weathered paint. "
    "The mood is sombre, still and heavy — the quiet after a catastrophe. "
)

# ── 構図：焼き込む文字の帯に合わせる ─────────────────────────────────────────
FRAME = (
    "COMPOSITION, critical: 16:9 frame. The TOP 25% and the BOTTOM 26% will later be "
    "covered by two lines of very large text, and the corners will be darkened. So the "
    "subject and every important detail must sit in the MIDDLE HORIZONTAL BAND, across "
    "the full width. Put plain, quiet, low-detail areas in the top quarter and the "
    # ⚠️ 2026-09-22：ここは "an empty overcast sky" と天気まで決め打ちだった。
    #    `build()` は FRAME を**場面より後ろ**に置くので、場面が「夏の晴れた強い光」を
    #    指定しても**曇りが勝つ**（＝場面ごとの指定が黙って無効になる）。天気は場面に任せる。
    "bottom quarter — an empty plain sky above, deep shadow and dust below — so that "
    "large lettering will read cleanly over them. Keep the bottom-right corner dark. "
)

# ── 描かせないもの ──────────────────────────────────────────────────────────
BAN = (
    "There must be NO people anywhere — no victims, no rescue workers, no bystanders, "
    "no bodies, no body parts, no blood, no injuries, no clothing or shoes on the "
    "ground. No fire, no flames, no explosion, no smoke (settling grey concrete DUST "
    "is wanted and is not smoke). "
    "No text, letters, numbers, words, signage, logos, labels or watermarks of any "
    "kind, in any language. No modern cars, no smartphones, no modern signage. "
)

PINK = (
    "One detail matters: the building's painted outer wall is a distinctive dusty "
    "PINK, and it must stay clearly pink — never drifting into red, crimson, brick "
    "or terracotta. "
)

# ── 質感：崩れている「最中」を撮ってしまった1枚（2026-09-22 カズヤくん指示）────────
#    「とにかく派手で目を引くように。しかし現実感のある、実際の事件を再現するような程度で」
#    ⚠️ 上の LOOK（曇り・静けさ・崩れたあと）とは**両立しない**ので、丸ごと差し替える。
#    ⚠️ 「派手」を色や演出で作らない。**粉じんの量と、落ちている途中という事実**で作る。
LOOK_MOMENT = (
    "A real PHOTOGRAPH, indistinguishable from a press photographer's grab shot. "
    "Caught hand-held at the very instant it happened, on a full-frame 35mm camera "
    "loaded with 1995 colour negative film. Bright hazy late-afternoon summer "
    "sunlight from the side, strong directional light, deep shadows, high contrast, "
    "fine natural film grain, slight hand-shake, imperfect focus at the edges. "
    "Physically accurate materials: fractured concrete, powdered grey dust, bent "
    "steel, painted render. The image is violent and overwhelming, but it is a "
    "photograph of a real event, not a spectacle. "
)
TAIL_MOMENT = (
    "The result must look like a genuine news photograph taken at the exact second "
    "a building came down — chaotic, dusty and real. It must NOT look like a render, "
    "a video game, a disaster movie poster, a 3D visualisation or an illustration. "
    "No lens flare, no colour grading, no cinematic teal-and-orange, no debris "
    "frozen in an unnatural fan shape. Gravity must read correctly: everything is "
    "falling straight DOWN."
)

SCENES = {
    # ── ★2026-09-22 カズヤくん指示＝「今まさに崩壊している」実写風 ────────────
    "e": {
        "name": "崩落の瞬間（真下に落ちていく北側と、噴き上がる粉じん）",
        "hypothesis": "「崩れたあと」は8本目までに出し尽くした。**落ちている途中**は"
                      "この事故の写真が1枚も存在しない絵なので、一覧の中で必ず止まる",
        "look": LOOK_MOMENT,
        "tail": TAIL_MOMENT,
        "scene": (
            "June 1995, Seoul. A large five-storey 1990s department store is collapsing "
            "RIGHT NOW, photographed from across a wide open car park. "
            "THE BUILDING IS FALLING STRAIGHT DOWN INTO ITSELF — it is not toppling "
            "sideways. The LEFT portion has already dropped: its floor slabs have "
            "pancaked one onto the next and disappeared below the ground line. The "
            "floors immediately to the right of that are caught mid-fall, still roughly "
            "flat but sagging and tilting inward, their edges snapping, the painted "
            "facade splitting into a long jagged vertical tear. The RIGHT portion is "
            "still standing, upright and ordinary and completely intact — that contrast "
            "is the point. "
            "An enormous billowing cloud of pale grey concrete DUST is erupting from the "
            "base and rolling outward low across the car park and upward behind the "
            "building, already swallowing the lower floors. Slabs of the pink painted "
            "wall and broken concrete are falling through the dust, all of them moving "
            "straight down. "
            "Architecture: a long horizontal five-storey block, a dark navy-blue band "
            "running along the very top of the parapet with small evenly spaced white "
            "squares set into it, tall narrow vertical banner panels in dark navy on "
            "the facade, a tall arched glass atrium at the centre, stepped setbacks at "
            "the corner, cooling towers on the roof. " + PINK +
            "Foreground: a broad empty asphalt car park with painted lines, a low "
            "concrete retaining wall, clipped hedges and a few conical evergreen shrubs, "
            "utility poles and slack overhead wires. Behind, ordinary 1990s Seoul "
            "mid-rise concrete apartment blocks under a bright hazy summer sky. "
        ),
    },
    "c": {
        "name": "崩落の断面（立っている壁と、消えた半分）",
        "hypothesis": "無傷の壁と、その隣の空白の対比が、いちばん惨さを伝える",
        "scene": (
            "The aftermath of the collapse of a large 1990s five-storey department "
            "store in Seoul, photographed from across the street a few hours after it "
            "fell. "
            "On the RIGHT half of the frame the building still stands and looks "
            "completely ordinary and undamaged — a flat painted facade, neat rows of "
            "windows, not a scratch on it. "
            "On the LEFT half, directly against it, the entire building is simply GONE. "
            "It has been sheared off along a clean vertical line and has pancaked "
            "straight down into a vast pit filled with stacked concrete floor slabs, "
            "snapped columns and bent reinforcing bars, several storeys deep. "
            "THE SUBJECT OF THE PHOTOGRAPH IS THAT CONTRAST: an untouched wall standing "
            "right beside a void where five floors of a crowded shop used to be. "
            "The scale is overwhelming — the standing wall towers over the mound. " +
            PINK +
            "Behind and above, a real 1990s Seoul cityscape: ordinary mid-rise concrete "
            "apartment blocks and office buildings under a flat, heavy, featureless "
            "overcast sky. Grey dust still hangs in the air and softens the distance. "
        ),
    },
    "d": {
        "name": "重なった床（床が床の上に落ちた形）",
        "hypothesis": "床が重なった形そのものが、被害の大きさを一目で伝える",
        "scene": (
            "A closer photograph, taken from the edge of the same collapse site, "
            "looking down and across the ruin. "
            "Enormous reinforced-concrete FLOOR SLABS have fallen flat on top of one "
            "another like a dropped stack of cards — five thick slabs compressed almost "
            "solid, with only a narrow crushed gap left between each one. Snapped "
            "reinforcing bars bend and protrude from the broken edges. Pulverised "
            "concrete and thick grey dust cover everything. "
            "THE SUBJECT IS THE STACK ITSELF and how terrifyingly little space is left "
            "between the layers. It fills the middle of the frame and runs off both "
            "edges so the viewer cannot see where it ends. "
            "Among the grey, one large fragment of smooth painted shop wall is still "
            "recognisable, lying tilted in the rubble. " + PINK +
            "At the top of the frame, beyond the ruin, ordinary 1990s Seoul buildings "
            "stand untouched under a flat overcast sky — normal life continuing right "
            "at the edge of the destruction. "
        ),
    },
}


TAIL = ("The result must look like a genuine, sombre, respectful news photograph "
        "of the aftermath of a building collapse — not a render, not an "
        "illustration, not a movie still, no motion blur, no dramatic lighting.")


def build(v):
    """🔴 質感（look）と締め（tail）は**場面ごとに差し替えられる**（2026-09-22 追加）。

    それまではここが「崩れた**あと**」「動きのブレなし」で決め打ちだった。
    「崩れている**最中**」を作るには、静けさを求める `LOOK` と
    「no motion blur / no dramatic lighting」で終わる締めが**真正面からぶつかる**。
    ⚠️ `FRAME`（文字の帯）・`BAN`（人・炎・文字）・`PINK` は**どの場面でも外さない**。
    """
    s = SCENES[v]
    return f"{s.get('look', LOOK)}{s['scene']}{FRAME}{BAN}{s.get('tail', TAIL)}"


def key():
    for p in KEY_CANDIDATES:
        try:
            if p.exists() and p.read_text(encoding="utf-8").strip():
                return p.read_text(encoding="utf-8").strip()
        except OSError:
            continue
    sys.exit("🔴 openai_key.txt が1つも読めません")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args or args[0] not in SCENES:
        sys.exit(f"使い方: python tools/gen_thumb_ai.py [{'|'.join(SCENES)}] [--dry]")
    v = args[0]
    prompt = build(v)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"ep10_{v}_prompt.txt").write_text(prompt, encoding="utf-8")

    if "--dry" in sys.argv:
        print(f"== 案{v.upper()}：{SCENES[v]['name']} ==")
        print(f"仮説: {SCENES[v]['hypothesis']}")
        print(f"model={MODEL} size={SIZE} quality={QUALITY}／文字数 {len(prompt)}\n")
        print(prompt)
        return 0

    print(f"★課金API: {MODEL} {QUALITY} 1枚（概算 $0.2前後）。案{v.upper()}＝{SCENES[v]['name']}")
    body = json.dumps({"model": MODEL, "prompt": prompt, "size": SIZE,
                       "quality": QUALITY, "n": 1}).encode()
    req = urllib.request.Request(
        API, data=body,
        headers={"Authorization": f"Bearer {key()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)

    from PIL import Image
    im = Image.open(io.BytesIO(base64.b64decode(data["data"][0]["b64_json"]))).convert("RGB")
    w, h = im.size
    target = w * 9 / 16
    if h > target:
        t = int((h - target) / 2)
        im = im.crop((0, t, w, int(t + target)))
    im = im.resize((1280, 720), Image.LANCZOS)
    dst = OUT / f"ep10_{v}.jpg"
    im.save(dst, "JPEG", quality=94)
    im.resize((246, 138), Image.LANCZOS).save(OUT / f"ep10_{v}_246.jpg", "JPEG", quality=92)
    print(f"OK -> {dst}（246px版も出力）")
    print("🔴 次＝thumb_jiko.py で赤・黄を焼いてから検品する（地だけで判断しない）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
