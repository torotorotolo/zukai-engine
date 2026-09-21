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
    "bottom quarter — an empty overcast sky above, deep shadow and dust below — so that "
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

SCENES = {
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


def build(v):
    s = SCENES[v]
    return (f"{LOOK}{s['scene']}{FRAME}{BAN}"
            "The result must look like a genuine, sombre, respectful news photograph "
            "of the aftermath of a building collapse — not a render, not an "
            "illustration, not a movie still, no motion blur, no dramatic lighting.")


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
