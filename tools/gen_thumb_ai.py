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


# ══ 14本目・セウォル号（2026-09-29・⑥）══════════════════════════════════════════
# カズヤくん指示「もっと事件の凄惨さが伝わるような刺激的な写真。なければ OpenAI API で生成も可。生成前に相談」。
# 🔴 文字を重ねられる実写が無い（Commons 68点・DVIDS 30点・韓国政府の頁＝傾いた船／沈む船の写真は
#    海洋警察の1点〈権利の根拠なし〉と報道機関の写真〈非自由〉だけ）→ 地だけを生成する。
# 🔴 札は3枚とも**新規**（記憶 feedback-prompt-cards-must-not-be-reused）＝10本目の LOOK・FRAME・BAN は
#    建物の崩落向け（コンクリート・粉じん・地面の靴・車）で、海の場面に混ぜると絵が崩れる。
# ⚠️ 本編の守りの線（映像方針 09-26）どおり、**人は描かせない**（乗客・救助隊・遺体・血・火・煙）。
#    船の名前・文字も描かせない（`thumb_jiko.py` が赤・黄を焼く）。この絵は**サムネだけ**・本編に入れない。
LOOK_SEA = (
    "A real PHOTOGRAPH, indistinguishable from documentary press photography, taken in "
    "2014 with a digital SLR and a long telephoto lens from a helicopter flying low over "
    "the sea. Flat, hazy, overcast spring morning light, muted natural colours, fine "
    "sensor grain, slight atmospheric haze that softens the distance, true photographic "
    "depth of field. Physically accurate materials: painted steel hull plating streaked "
    "with rust and salt, glass windows, calm grey-green sea water with small wavelets. "
    "The mood is heavy, silent and grave — a disaster unfolding in plain daylight. "
)
FRAME_SEA = (
    "COMPOSITION, critical: 16:9 frame. The TOP 25% and the BOTTOM 26% will later be "
    "covered by two lines of very large text, and the corners will be darkened. So the "
    "ship and every important detail must sit in the MIDDLE HORIZONTAL BAND, stretched "
    "across most of the width. Keep the top quarter as plain hazy sky or distant sea, "
    "and the bottom quarter as plain, darker open water with no important detail, so "
    "that large lettering will read cleanly over them. Keep the bottom-right corner dark. "
)
BAN_SEA = (
    "There must be NO people anywhere — no passengers, no crew, no rescuers, no divers, "
    "no figures on decks, in boats or in the water, no bodies, no blood, no injuries. "
    "No fire, no flames, no explosion, no smoke. "
    "No text, letters, numbers, ship names, words, flags with writing, logos, labels or "
    "watermarks of any kind, in any language — the hull and superstructure carry no "
    "lettering at all. "
)
TAIL_SEA = (
    "The result must look like a genuine, sombre news photograph of a real maritime "
    "disaster — not a render, not an illustration, not a disaster-movie still, not a "
    "3D visualisation. No lens flare, no colour grading, no cinematic teal-and-orange, "
    "no dramatic storm, no giant waves: the sea is calm, which is what makes it terrible."
)
SEWOL_SHIP = (
    "The ship: a large Korean passenger car-ferry, about 146 metres long, with a long "
    "white hull and a tall white superstructure of several passenger decks lined with "
    "rows of small square windows, the navigation bridge near the bow, and a single "
    "funnel toward the stern. The underwater part of the hull is painted dark red. "
)
SCENES.update({
    "sewol_a": {
        "ep": "ep14",
        "name": "大きく左へ傾いた船（浮かぶコンテナと救命いかだ・遠巻きの救助の船）",
        "hypothesis": "「助けを待つあいだに傾いていく」という、この回の芯そのもの。"
                      "穏やかな海で巨大な船だけが横倒しになっていく異様さが、一覧で止める",
        "look": LOOK_SEA, "frame": FRAME_SEA, "ban": BAN_SEA, "tail": TAIL_SEA,
        "scene": (
            "April 2014, the calm sea off the south-western coast of Korea, mid-morning. "
            + SEWOL_SHIP +
            "It is CAPSIZING RIGHT NOW: the whole ship is heeled over onto its LEFT (port) "
            "side at about sixty degrees, the port side of the superstructure already "
            "under the sea up to the upper decks, the long flat starboard side and the "
            "rounded hull turned up toward the sky, a broad band of the dark red hull "
            "bottom lifted clear of the water. Loose cargo containers and white "
            "capsule-shaped life-raft canisters float in the water beside the hull. "
            "At a distance, a few small orange rescue boats and a grey coast-guard patrol "
            "boat wait, tiny against the ship; a helicopter hangs in the haze above. "
            "Seen from a low oblique angle from the air, the leaning ship fills the middle "
            "band of the frame from left to right. Faint low islands on the horizon. "
        ),
    },
    "sewol_b": {
        "ep": "ep14",
        "name": "船首の先だけが残った海（まわりに群がる救助の船）",
        "hypothesis": "10時31分の「船首の先だけを水面に残して沈んだ」（c107）。"
                      "船がほぼ見えないこと自体が、中に残された人の数を想像させる",
        "look": LOOK_SEA, "frame": FRAME_SEA, "ban": BAN_SEA, "tail": TAIL_SEA,
        "scene": (
            "April 2014, the calm sea off the south-western coast of Korea, late morning. "
            "A large passenger car-ferry, about 146 metres long, has turned completely "
            "upside down and sunk. Only the very tip of its BOW still breaks the surface: "
            "the upturned, rounded bulbous bow and a short length of the keel, painted "
            "dark red, sticking up out of the grey-green water like a small island. "
            "Everything else of the ship is already under the sea. "
            "Around it, spread across the whole width of the frame, dozens of small "
            "boats — grey coast-guard patrol boats, fishing boats, orange rescue "
            "boats — hold position in a loose ring, all of them far too small to help. "
            "A helicopter hovers in the haze. Seen from the air at a low oblique angle, "
            "the red bow sits in the centre of the middle band of the frame. "
        ),
    },
})


# ══ 15本目・リノ・エアレース2011（2026-09-30・⑥）════════════════════════════════════
# カズヤくん指示「もっとショッキングで目をひくものに。なければ事故の瞬間を再現したようなイラストを OpenAI API で生成。
#   生成する場合は具体案を出して、私の承認後 GO」。赤は c「犠牲11人 改造機が観客席へ」で決定（09-30）。
# 🔴 文字を重ねられる写真が無い（09-30 に探し直した）：Commons の分類「2011 Reno Air Races crash」＝NTSB の部品の図（PD）と
#    tataquax の BY-SA だけ／Openverse（CC BY・CC0・PD）＝2010年の jeggernot 1点だけ／NTSB 資料 #20（付録A 写真と図）は
#    サーバーの写しが途中で切れ、写真の中身は暗号化（鍵は切れた側）＝取り出せない／#42 は観客の写真（撮影者の著作物）・
#    #40 は部品／DVIDS は2018〜2023年の大会だけ。
# 🔴 札は4枚とも**新規**（記憶 feedback-prompt-cards-must-not-be-reused）＝10本目は建物の崩落・14本目は海。
# 🔴 事実に合わせる（報告書 AAB-12/01）：快晴・22℃・西南西の風（p16）／16時24分（p28）／降下は「らせん状の飛び方で地上へ」
#    （p10・p39）／駐機場に衝突して機体がばらばらになった＝**火が出たという記述は無い**（p10）→ 火・爆発は描かせない／
#    ボックス席の幕は青と赤（p21 脚注26）。
# ⚠️ 本編の守りの線（映像方針 09-26）どおり、**人は描かせない**（パイロット＝風防は光る面・観客・救助の人・遺体・血）。
#    機体の番号「177」・文字も描かせない（崩れた字を防ぐ・`thumb_jiko.py` が赤・黄を焼く）。この絵は**サムネだけ**・本編に入れない。
# ⚠️ 通説（「尾翼の板が外れて機首が上がった」）の絵にしない＝板の破片を機首上げと同じ瞬間に描かない（一片が離れたのは最大Gの約3秒後）。
LOOK_RENO = (
    "A real PHOTOGRAPH, indistinguishable from a press photographer's grab shot, taken at an "
    "air race in September 2011 on a digital SLR with a long telephoto lens, panning with the "
    "airplane so that the airplane is sharp and only the propeller disc is blurred. Bright, "
    "clear late-afternoon high-desert light from the west, a cloudless deep-blue sky, hard "
    "shadows, crisp dry air, the bare brown sagebrush hills and mountains of northern Nevada "
    "low on the horizon. Physically accurate materials: polished bare aluminium skin that "
    "reflects the sun, painted steel grandstand framing, sun-bleached asphalt, fabric bunting. "
    "Fine natural sensor grain. The image is shocking and immediate, but it is a photograph of "
    "a real event, not a spectacle. "
)
FRAME_RENO = (
    "COMPOSITION, critical: 16:9 frame. The TOP 25% and the BOTTOM 26% will later be covered by "
    "two lines of very large text, and the corners will be darkened. So the airplane's nose, "
    "canopy and wings, and the edge of the spectator seating it is heading into, must all sit "
    "in the MIDDLE HORIZONTAL BAND; only the airplane's tail may reach up into the top quarter. "
    "Keep the top quarter as plain, empty, cloudless deep-blue sky, and the bottom quarter as "
    "plain, shadowed, featureless asphalt in the foreground, so that large lettering will read "
    "cleanly over them. Keep the bottom-right corner dark. "
)
BAN_RENO = (
    "There must be NO people anywhere — no spectators, no pilot visible in the cockpit (the "
    "canopy is only a bright sun glare), no crew, no rescuers, no figures in the seats or on "
    "the grandstand, no bodies, no body parts, no blood, no injuries. The chairs and stands "
    "are simply empty. No fire, no flames, no explosion, no smoke, no fireball. "
    "No text, letters, numbers, race numbers, words, sponsor decals, logos, flags with writing, "
    "labels or watermarks of any kind, in any language — the airplane carries no markings at "
    "all, just bare polished metal. "
)
TAIL_RENO = (
    "The result must look like a genuine news photograph taken a split second before a real "
    "air-race crash — sharp, bright, sudden and real. It must NOT look like a render, a video "
    "game, a movie poster, a 3D visualisation or an illustration. No lens flare, no colour "
    "grading, no cinematic teal-and-orange, no speed lines, no debris frozen in the air. "
    "Gravity and perspective must read correctly: the airplane is falling steeply toward the "
    "ground."
)
RENO_PLANE = (
    "The airplane: a single, heavily modified World War II P-51D Mustang racing airplane — a "
    "long, slim, gleaming polished bare-metal silver fuselage, a low teardrop bubble canopy, "
    "short clipped wings, a large four-blade propeller, and a big air-scoop under the belly. "
)
SCENES.update({
    "reno_a": {
        "ep": "ep15",
        "name": "落ちる直前の1秒（らせんを描いて観客のボックス席へ突っ込んでくる機体）",
        "hypothesis": "サムネの赤「改造機が観客席へ」をそのまま絵にする。空から突っ込む機体と、"
                      "その真下の観客席が同じ画面にある＝一覧で「何が起きたか」が一目で分かり、止める",
        "look": LOOK_RENO, "frame": FRAME_RENO, "ban": BAN_RENO, "tail": TAIL_RENO,
        "scene": (
            "September 16, 2011, about 4:24 in the afternoon, the Reno air races at Stead "
            "airfield, Nevada. " + RENO_PLANE +
            "It is plunging almost straight DOWN toward the ground, nose first, in a steep, "
            "twisting corkscrew dive, rolled partly onto its back, only a second or two from "
            "impact. It is seen from the side and slightly below, from the edge of the "
            "spectator area, large in the frame, in the centre-right of the middle band. "
            "Directly below it, along the lower middle of the frame, is the front of the "
            "spectator area on the flat asphalt ramp: a long row of boxed seating areas "
            "separated by low metal railings and hung with BLUE and RED fabric bunting, rows "
            "of empty folding chairs inside them, and behind them the steel frame and roof of "
            "a large covered grandstand. The airplane is unmistakably diving into the seating "
            "area. "
        ),
    },
    "reno_b": {
        "ep": "ep15",
        "name": "横転と機首上げの瞬間（コースの上空で、急に機首を上げて裏返りかける機体）",
        "hypothesis": "事故の始まりの0〜1.3秒（横転→17.3G）。空の中の異様な姿勢で止める。"
                      "観客席は遠く小さい＝Aより穏やか",
        "look": LOOK_RENO, "frame": FRAME_RENO, "ban": BAN_RENO, "tail": TAIL_RENO,
        "scene": (
            "September 16, 2011, about 4:24 in the afternoon, the Reno air races at Stead "
            "airfield, Nevada. " + RENO_PLANE +
            "At racing speed, low over the desert race course, it has suddenly rolled far to "
            "the left, past vertical, and at the same instant pitched violently NOSE-UP, its "
            "tail-wheel hanging down — the whole airplane twisted into a wrong, uncontrolled "
            "attitude against the deep-blue sky. Nothing has broken off it; it is intact. "
            "It fills the centre of the middle band, seen from the ground with a telephoto "
            "lens. Far below and behind it, small and distant along the lower middle of the "
            "frame, a tall race-course pylon marker and the long covered grandstands of the "
            "airfield. "
        ),
    },
})

# ── 16本目 バイオントダム災害（1963-10-09 22:39・イタリア北東部）──────────────────────
# 🆕 2026-10-02 ⑥ の試写のあと、カズヤくん「写真はインパクトが弱いので変更。OpenAI API で生成。生成の前に具体案を出して、
#    承認後生成。とにかく目を引くような、事件の瞬間を象徴するような写真。サムネイルなので、ある程度の誇張表現は許容」。
#    札は4枚とも新規（ep15 の飛行機・観客席・砂漠の語を流用しない＝`--dry` で数える）。ブレ止めの1文だけ ep15 から1字も変えずに写した。
# 🔴 事実の芯（本編の語り）：夜の22時39分／ダムは壊れず立ったまま（c104）／湖の水がダムの上を越えた（c815）・
#    天端より100メートル以上の高さで越えた（学術の総説＝c817）／峡谷の出口でも約70メートル（c904）。
#    誇張してよいのは光と迫力（月・投光・しぶき）。ダムは壊さない（本編の芯＝ダムは耐えた）。
# 🆕🔴 2026-10-02 カズヤくん（案A の承認と同時に）「人（ダムや岸の人・救助の人も）・遺体・血・家や窓の灯り・車・火・煙を
#    描かないというルールは今後撤廃します」＝ルール §6-55⑤ のうち**文字以外の禁止を外した**（BAN_VAJ は文字だけ）。
#    ⚠️ 文字は引き続き描かせない（赤・黄は thumb_jiko.py が焼く＝絵の字は崩れて二重になる）。
#    ⚠️ YouTube のサムネの決まり（暴力的・生々しい画像）は別に残る＝こちらから遺体・血を足しはしない（言われたら相談）
LOOK_VAJ = (
    "A real PHOTOGRAPH, indistinguishable from documentary press photography, taken at night "
    "in October 1963 in a deep alpine gorge in north-eastern Italy, on a large-format press "
    "camera. The only light comes from a bright moon behind thin high cloud and from a short "
    "row of lamps along the top of the dam: cold blue-white light on the water, deep "
    "blue-black shadow in the gorge. Physically accurate materials: smooth pale concrete, wet "
    "grey limestone cliffs, churning white water, fine drifting spray and mist. Fine natural "
    "film grain. The image is shocking and immediate, but it is a photograph of a real "
    "event, not a spectacle. "
)
FRAME_VAJ = (
    "COMPOSITION, critical: 16:9 frame. The TOP 25% and the BOTTOM 26% will later be covered by "
    "two lines of very large text, and the corners will be darkened. So the main subject — "
    "described above — must sit in the MIDDLE HORIZONTAL BAND, across most of the width; only "
    "the highest spray may reach up into the top quarter. Keep the top quarter as plain, dark "
    "night sky with faint mountain silhouettes, and the bottom quarter as plain, black, "
    "featureless shadow deep in the valley, so that large lettering will read cleanly over "
    "them. Keep the bottom-right corner dark. "
)
BAN_VAJ = (
    "No text, letters, numbers, words, signs, logos, labels or watermarks of any kind, in any "
    "language. "
)
TAIL_VAJ = (
    "The result must look like a genuine photograph of the real disaster at that very "
    "instant — dark, violent, sudden and real. It must NOT look like a render, a video game, "
    "a movie poster, a 3D visualisation or an illustration. No lens flare, no colour grading, "
    "no cinematic teal-and-orange, no lightning, no rain. Gravity and scale must read "
    "correctly: the dam is enormous and the water falls a very long way."
)
VAJ_DAM = (
    "The dam: a very tall, thin, double-curvature concrete arch dam, about 260 metres high, "
    "its gently curved top about 190 metres long, wedged into a narrow, sheer-walled limestone "
    "gorge. The dam itself is intact and standing — it does NOT break, crack or collapse. "
)
SCENES.update({
    "vaj_a": {
        "ep": "ep16",
        "name": "ダムを越える波（夜・ダムは立ったまま、天端の上を白い水の壁が越えて峡谷へ落ちる）",
        "hypothesis": "本編の芯「ダムは耐えた。水がその上を越えた」を1枚に。赤の「予兆は3年前」と組で"
                      "「分かっていたのに」を引く。白い水と黒い谷の明暗＝210px でも何が起きたかが読める",
        "look": LOOK_VAJ, "frame": FRAME_VAJ, "ban": BAN_VAJ, "tail": TAIL_VAJ,
        "scene": (
            "October 9, 1963, 10:39 at night, the Vajont dam in the Italian Alps. " + VAJ_DAM +
            "At this instant a colossal wave from the reservoir behind it is pouring over the "
            "ENTIRE length of its top: a towering wall of white, foaming water bursting more "
            "than a hundred metres up above the top of the dam and then plunging down its "
            "downstream face into the black gorge below, throwing up enormous clouds of white "
            "spray. Seen from high on the downstream side of the gorge, a little above the "
            "height of the dam's top, so that the curved top of the dam runs horizontally "
            "across the middle band of the frame, the white water exploding over it, and the "
            "dark cliffs of the gorge close in on both sides. "
        ),
    },
    "vaj_b": {
        "ep": "ep16",
        "name": "山が湖へ滑り込む瞬間（夜・南の岸の山の斜面が1つの塊のまま湖へ、押し出された水が北の岸を駆け上がる）",
        "hypothesis": "事故の始まり（c101・c811）。山と波の大きさで止める。ダムは右の奥に小さい＝A より何の事故かが伝わりにくい",
        "look": LOOK_VAJ, "frame": FRAME_VAJ, "ban": BAN_VAJ, "tail": TAIL_VAJ,
        "scene": (
            "October 9, 1963, 10:39 at night, the long, narrow reservoir behind the Vajont dam "
            "in the Italian Alps. The whole forested lower face of the mountain on the south "
            "shore — a slope about two kilometres long — is sliding as ONE single solid block "
            "down into the reservoir, trees still standing on it, pushing the water ahead of "
            "it. The displaced water rises as a gigantic white wave that races up the steep "
            "opposite (north) shore of the valley, far higher than the lake. Far to the right, "
            "at the end of the lake, the thin curved concrete arch dam stands intact, the "
            "first water just reaching its top. Seen from high on the valley side, looking "
            "along the lake, so that the sliding mountainside, the rising wave and the lake "
            "run horizontally across the middle band of the frame. "
        ),
    },
})


# ── 🆕 20本目 日本航空123便のリメイク（2026-10-11・⑥）＝カズヤくん「サムネAの写真がイマイチ。事故の瞬間を象徴するような
#    実写写真を OpenAI API で生成。生成前に案を出し、承認してから生成」。🔴 札は新規（ほかの回の札を流用しない＝ルール 6-55④）
#    事実の芯（報告書）：18:24:35 ごろ・巡航高度 24,000 フィート（約7,300メートル）に達する直前・相模湾の上空・夕方（日没は約18:40）。
#    垂直尾翼の大部分（上の部分と方向舵）と尾部の円すい（APU）が失われた＝火も煙も出ていない（構造の破壊）。機体は 747SR-100
#    （短い2階・4発）・白い胴体の上・窓の帯の赤い線＝**文字・ロゴ・登録記号は描かせない**（字形が崩れる・鶴丸は尾翼ごと壊れる）
LOOK_JAL = (
    "A real PHOTOGRAPH, indistinguishable from documentary press photography, taken with a very long telephoto lens "
    "from very far away. Natural evening daylight in August: a low sun from the side, warm but soft, slight "
    "atmospheric haze, slightly desaturated colours, the fine natural grain of 1980s colour negative film, true "
    "photographic depth of field. Physically accurate materials: painted aluminium skin, torn sheet metal, rivets. "
)
FRAME_JAL = (
    "COMPOSITION, critical: 16:9 frame. The TOP 25% and the BOTTOM 26% will later be covered by two lines of very large "
    "text, and the corners will be darkened. So the aircraft — described above — must sit in the MIDDLE HORIZONTAL "
    "BAND, across most of the width, its nose pointing to the LEFT. Keep the top quarter as plain, empty, pale evening "
    "sky, and the bottom quarter as plain, hazy, featureless sea far below, so that large lettering will read cleanly "
    "over them. Keep the bottom-right corner dark. "
)
BAN_JAL = (
    "No text, letters, numbers, words, signs, logos, airline names, registration markings, emblems, labels or "
    "watermarks of any kind, in any language. No other aircraft. "
)
TAIL_JAL = (
    "The result must look like a genuine photograph of the real event at that very instant — sudden, shocking and "
    "real. It must NOT look like a render, a video game, a movie poster, a 3D visualisation or an illustration. No "
    "lens flare, no cinematic colour grading, no fire, no smoke trail, no explosion fireball — the damage is purely "
    "structural: metal tearing apart and pieces flying off. Scale must read correctly: a huge four-engine jumbo jet "
    "seen from far away."
)
JAL_PLANE = (
    "The aircraft: a Boeing 747 jumbo jet of the early 1980s — the 747SR version with the SHORT upper-deck hump "
    "right behind the cockpit — four engines hanging under the swept wings, white upper fuselage, a thin red stripe "
    "along the row of cabin windows, metal-grey lower fuselage, and no lettering or logos anywhere. "
)
SCENES.update({
    "jal_a": {
        "ep": "ep20",
        "name": "尾翼がはじける瞬間（夕方・相模湾の上空・高い空で垂直尾翼の上の部分がちぎれて破片が後ろへ飛ぶ・機体はまっすぐ飛んでいる）",
        "hypothesis": "事故の瞬間そのもの（c102「ドーン」）。何が壊れたか（尾翼）が 210px でも形で分かる。"
                      "赤「生存者4人 全員が後ろの席」の「後ろ」と、壊れた後ろ（尾部）が絵の上で結びつく",
        "look": LOOK_JAL, "frame": FRAME_JAL, "ban": BAN_JAL, "tail": TAIL_JAL,
        "scene": (
            "August 12, 1985, about 6:24 in the evening, high above the sea south-west of Tokyo (Sagami Bay), at "
            "about 7,000 metres. " + JAL_PLANE +
            "At this very instant the upper part of its tall vertical tail fin is breaking apart, torn away by air "
            "pressure from inside the tail: large sheets of white-painted metal skin and pieces of the fin structure "
            "are blasting off and tumbling away behind the aircraft, with a scatter of small debris, and the cone at "
            "the very end of the fuselage is torn open. The rest of the aircraft is still intact and flying straight "
            "and level. Seen exactly side-on from far away and slightly below, so that the whole aircraft runs "
            "horizontally across the middle band of the frame and the breaking tail stands out clearly against the "
            "sky. "
        ),
    },
    "jal_b": {
        "ep": "ep20",
        "name": "尾翼を失って山の上を飛ぶ機体（夕暮れ・群馬の山並み・尾翼はぎざぎざの根元だけ）",
        "hypothesis": "約30分の操縦できない飛行（c104）。尾翼の無い機影は旧版の写真-124 と同じ芯＝この事故だと分かる。"
                      "ただし「瞬間」ではない＝A のほうが依頼に近い",
        # 🆕 カズヤくん（10-11・案A の生成のあと）「案Bの画像も生成。当時の写真の質感を再現するような粗さで」＝質感だけ 1985年の写真に
        "look": (
            "A real PHOTOGRAPH taken in August 1985 from the ground, from very far away, with a long telephoto lens on "
            "fast ISO 400 colour negative film, and scanned from the original print. It has the rough, imperfect look "
            "of a real photograph of that time: heavy, coarse film grain everywhere, slightly soft focus and a little "
            "haze from the great distance, low contrast, muted and slightly faded colours with a warm cast, faint dust "
            "specks and slight unevenness in the print. Nothing is crisp or digital. "),
        "frame": FRAME_JAL.replace("plain, hazy, featureless sea far below",
                                                     "dark, featureless forested mountain ridges far below"),
        "ban": BAN_JAL, "tail": TAIL_JAL,
        "scene": (
            "August 12, 1985, about 6:45 in the evening, over the steep, dark green forested mountains of Gunma, "
            "Japan. " + JAL_PLANE +
            "The aircraft has lost almost all of its vertical tail fin: only a short, jagged, torn stump of metal "
            "remains above the rear fuselage, and the very end of the fuselage behind it is ragged and open. It is "
            "flying low and slightly banked under a pale evening sky. Seen side-on from far away and slightly below, "
            "so that the whole aircraft runs horizontally across the middle band of the frame. "
        ),
    },
})


# ── 🆕 22本目 タイタン号のリメイク（2026-10-15・⑥）＝カズヤくん「サムネはどれもイマイチ。OpenAI API で海底のタイタン号を再現した
#    実写イラストを作成して使用」（国の写真の候補は見たうえで・ROV の映像＝Pelagic＝第三者はサムネに使わない＝10-14 の決め）。
#    🔴 札は新規（ほかの回の札を流用しない＝ルール 6-55④。流用はブレ止めの1文「It must NOT look like a render, …」だけ）
#    事実の芯（3冊・台本 c101・c5）：2023-06-22・北大西洋・深さ約3,800メートル・タイタニックの船首から約500メートル。無人の探査機（ROV）の
#    ライトの中で、海底に尾部（白い円すいの覆い）が見つかり、まわりに残骸（炭素繊維の筒の黒い破片・チタンの輪）が散っていた。
#    🔴 ROV の映像そのものを真似しない（探査機の腕・画面の焼き込みの数字を描かせない）・人と遺体は描かせない・文字は描かせない
#    本番は反転版（字の外がカラー）＝地は明るく（カズヤくん「文字を目立たせるため、地の写真を明るく加工」）→ 焼くときに明るさを上げる
LOOK_TITAN = (
    "A real PHOTOGRAPH taken on the deep-sea floor by the camera of an expedition, at about 3,800 metres depth in "
    "the North Atlantic. Strong white floodlights from just above and in front light the scene evenly and brightly; "
    "the light falls off into deep blue-black water at the edges. Clear, sharp, high-resolution digital image with "
    "true depth of field, natural colours under the lamps, fine drifting particles of marine snow catching the light. "
)
FRAME_TITAN = (
    "COMPOSITION, critical: 16:9 frame. Very large lettering will later cover the top 15% and the bottom 20% of the "
    "frame, and one huge word will run across the whole middle. So the wreck — described above — must be large and "
    "fill the MIDDLE HORIZONTAL BAND across most of the width, seen from slightly above the seabed at a low angle, "
    "with the pale sediment brightly lit all around it so that the whole frame reads as light and clear, not dark. "
    "Keep the top as softly lit blue water with drifting particles, and the bottom as bright, plain, pale grey "
    "sediment. "
)
BAN_TITAN = (
    "No text, letters, numbers, words, logos, labels, signs, scale bars, timestamps, depth readouts, camera overlays, "
    "frames or watermarks of any kind. No people, no human remains, no clothing, no fish or animals, no robot arm or "
    "any part of the camera vehicle in view, no other wreck or ship in view. "
)
TAIL_TITAN = (
    "The result must look like a genuine, quiet, respectful photograph of the wreck as it was found. It must NOT look "
    "like a render, a video game, a movie poster, a 3D visualisation or an illustration. No lens flare, no dramatic "
    "colour grading, no air bubbles, no fire, no smoke."
)
SCENES.update({
    "titan_a": {
        "ep": "ep22",
        "name": "海底で見つかったタイタン号の尾部と残骸（深さ約3,800メートル・照明で明るく照らされた海底）",
        "hypothesis": "台本の冒頭 c101（尾部をとらえた）と同じ場面＝この事故だと形で分かる。反転版の字の外が明るい海底と白い尾部になり、"
                      "「タイタン号」の暗い字が立つ",
        "look": LOOK_TITAN, "frame": FRAME_TITAN, "ban": BAN_TITAN, "tail": TAIL_TITAN,
        "scene": (
            "The wreck of a small five-person deep-diving submersible lies on the flat seabed: the white, smooth, "
            "cone-shaped tail section of the craft, about two and a half metres across, rests partly sunk in the "
            "sediment, slightly tilted. At its broken front end there is a heavy ring of dull grey titanium, and "
            "short, frayed, splintered black carbon-fibre composite sticks out from it where the cylindrical hull "
            "was torn away. Around it, scattered across the sediment, lie many black carbon-fibre fragments, a few "
            "pieces of white fairing panel and bits of cable. Everything is still; the damage is crushed and torn, "
            "not burnt. "
        ),
    },
})


# ── 🆕 17本目 中華航空140便（2026-10-21・⑥）＝カズヤくん「（地は T1 を最有力にしたうえで）その他に、もっとインパクトがある刺激的な
#    イラストを OPENAI API で生成。生成前に案を出して、私が承認してから GO」。🔴 札は新規（ほかの回の札を流用しない＝ルール 6-55④）。
#    事実の芯（台本 第2版・報告書 S1）：1994-04-26 の夜 20時15分ごろ・名古屋空港・エアバス A300-600R（双発の大型機）・脚を出した着陸の形のまま、
#    機首が約52.6度まで上がり（第7章「52.6度」・c720）、高さ約530メートル（c721＝1,730ft）で速さを失って失速＝20:15:45 に墜落・炎上。
#    🔴 文字・旗・登録記号・会社の印は描かせない（実機の塗りは真似しない）。本番は H 型の反転版（字の外がカラー）＝夜の地は焼くときに明るさを上げる
LOOK_CAL = (
    "A real PHOTOGRAPH taken at night with a professional camera and a long telephoto lens: sharp, clear and "
    "high-resolution, with true depth of field and the natural colours of airport lighting. The subject is brightly lit "
    "by its own landing lights and by the glow of the airport floodlights, so that its whole shape reads clearly against "
    "a deep navy-blue night sky. "
)
FRAME_CAL = (
    "COMPOSITION, critical: 16:9 frame. Very large lettering will later cover the top 15% and the bottom 20% of the "
    "frame, and one huge word will run across the whole middle, so the picture will mostly be seen through the gaps "
    "between its letters. So the subject described above must be LARGE and fill most of the width of the frame, with "
    "its shape and angle obvious at a glance even when the picture is tiny. Keep the top of the frame as plain night sky "
    "and the bottom as dark flat ground with rows of airport lights. "
)
BAN_CAL = (
    "No text, letters, numbers, words, logos, flags, emblems, registration marks, airline names, signs or watermarks of "
    "any kind, in any language — the aircraft is painted plain white with grey wings and carries no markings at all. "
)
TAIL_CAL = (
    "The result must look like a genuine, dramatic news photograph of a real moment. It must NOT look like a render, a "
    "video game, a movie poster, a 3D visualisation or an illustration. No lens flare, no motion blur, no dramatic "
    "colour grading."
)
CAL_PLANE = (
    "A large twin-engine wide-body airliner (an Airbus A300-600R: two big engines under the wings, a long white fuselage, "
    "a single tall tail fin), with its landing gear down, "
)
SCENES.update({
    "cal_a": {
        "ep": "ep17",
        "name": "機首が約50度まで上がった機体（夜・名古屋空港の上空・脚を出したまま・失速の直前）",
        "hypothesis": "第7章「52.6度」＝この事故のいちばんの山場。「飛行機が空を向いている」異様さが 210px でも形で分かる。"
                      "上の赤「押し合い」（人と自動操縦）の行き着いた先が絵になる",
        # ✅ 10-21 カズヤくん「人・炎は描かない というルールは不要です。案Aで進めて」＝禁止は文字だけ（ルール §6-55b と同じ）。
        #    場面の事実（失速の直前・まだ壊れずに飛んでいる）は scene のまま
        "look": LOOK_CAL, "frame": FRAME_CAL, "ban": BAN_CAL, "tail": TAIL_CAL,
        "scene": (
            "April 26, 1994, about a quarter past eight in the evening, a clear, dark spring night above Nagoya Airport "
            "in Japan. " + CAL_PLANE +
            "is pitched up at a terrifying, extreme nose-high angle of about 50 degrees, about 500 metres above "
            "the airport, its engines at full power, hanging in the air and losing speed just before it stalls. Its "
            "landing lights blaze and its navigation lights glow at the wingtips. Far below, the long rows of runway "
            "edge lights and approach lights glow white and orange in the darkness, with the lights of the city beyond. "
            "Seen from the ground off to one side and slightly below, so that the whole steeply tilted aircraft is large "
            "in the frame, nose high on the right and tail low on the left. "
        ),
    },
    "cal_b": {
        "ep": "ep17",
        "name": "墜落のあと、空港の草地で燃える機体と放水する消防車（夜）",
        "hypothesis": "いちばん刺激が強い絵（炎と放水）。事故の大きさは伝わるが、何が起きたか（機首上げ）は絵から分からない。"
                      "YouTube のサムネの決まり（衝撃を狙う暴力的な絵）に触れないよう、人は遠い小さな影だけ",
        "look": LOOK_CAL.replace("brightly lit by its own landing lights and by the glow of the airport floodlights",
                                 "lit from below by the orange light of the fire"),
        "frame": FRAME_CAL.replace("dark flat ground with rows of airport lights", "dark flat grass with the runway lights"),
        "ban": BAN_CAL + "No victims, no bodies, no injuries; any firefighters are only tiny, distant dark silhouettes. ",
        "tail": TAIL_CAL,
        "scene": (
            "April 26, 1994, at night, some minutes after the crash, Nagoya Airport in Japan. The "
            "broken wreckage of a large white twin-engine wide-body airliner lies burning on the flat grass field beside "
            "the runway: large torn sections of the white fuselage and a wing lie scattered, orange flames and thick dark "
            "smoke rise into the black sky. Several airport fire engines with flashing red lights stand around it, "
            "spraying long white arcs of water and foam at the flames. The runway edge lights stretch away into the "
            "darkness. Seen from a distance at a low angle, so that the whole burning wreck runs across the middle of the "
            "frame. "
        ),
    },
})


# ── 🆕 24本目 チェルノブイリ原発事故（2026-10-24・⑥）＝カズヤくん「写真の候補＋生成AIの案文」（地の写真8枚は今の昼の石棺・覆い＝迫力が弱い）。
#    🔴 札は新規（ほかの回の札を流用しない＝ルール 6-55④）。禁止は文字だけ（10-21 の決め＝§6-55b）。
#    事実の芯（台本 第2版）：1986-04-26 1時24分ごろ・4号炉の建屋の上が壊れ、屋根の上に火（INSAG-1＝30か所あまり・5時までに消えた）・
#    隣の赤白の排気筒。数日後から軍のヘリが砂・鉛などを炉へ落とした（INSAG-1）。🔴 言い伝えの「青い光の柱」は描かせない（台本で扱わない）。
#    🔴 1986年の有名な空撮（第三者の写真）の構図をまねない＝地上から遠くに見る形。本番は H 型の反転版（字の外がカラー）＝夜の地は焼くときに明るく
LOOK_CHN = (
    "A real PHOTOGRAPH taken with a professional camera and a long telephoto lens: sharp, clear and high-resolution, "
    "with true depth of field and natural colours. The shapes of the buildings read clearly against the sky. "
)
FRAME_CHN = (
    "COMPOSITION, critical: 16:9 frame. Very large lettering will later cover the top 15% and the bottom 20% of the "
    "frame, and one huge word will run across the whole middle, so the picture will mostly be seen through the gaps "
    "between its letters. So the subject described above must be LARGE and fill most of the width of the frame, "
    "readable at a glance even when the picture is tiny. Keep the top of the frame as sky with the rising smoke and "
    "the bottom as dark ground. "
)
BAN_CHN = (
    "No text, letters, numbers, words, logos, flags, emblems, signs or watermarks of any kind, in any language. "
)
TAIL_CHN = (
    "The result must look like a genuine, dramatic news photograph of a real moment. It must NOT look like a render, a "
    "video game, a movie poster, a 3D visualisation or an illustration. No lens flare, no dramatic colour grading."
)
CHN_PLANT = (
    "the huge rectangular concrete reactor building of Unit 4 of the Chernobyl nuclear power plant, its roof and the "
    "top of its walls blown open: jagged broken concrete and twisted steel beams stick up against the sky. Right beside "
    "the building stands the tall red-and-white striped ventilation stack with its steel lattice. "
)
SCENES.update({
    "chn_a": {
        "ep": "ep24",
        "name": "事故の夜の4号炉（1時24分すぎ・壊れた建屋から湯気と煙・屋根の上の火・赤白の排気筒）",
        "hypothesis": "この事故でいちばん知られた「壊れた4号炉」を夜の火の色で。反転版の字のすき間に橙の火と排気筒が出る。"
                      "上の赤「書き直された」（報告の書き直し）とは別の入口＝事故そのものの絵",
        "look": LOOK_CHN.replace("natural colours.", "natural colours, at night, lit by the orange glow of fires."),
        "frame": FRAME_CHN, "ban": BAN_CHN, "tail": TAIL_CHN,
        "scene": (
            "The early hours of April 26, 1986, minutes after the explosion, a dark spring night in the Soviet Union. "
            + CHN_PLANT[0].upper() + CHN_PLANT[1:] +
            "A thick column of white steam and grey smoke rises from the open, ruined top of the building into the deep "
            "navy-blue night sky. Several orange fires burn on the flat roofs of the reactor building and of the long, "
            "lower turbine hall in front of it, and glowing fragments lie scattered on the roofs. Seen from about one "
            "kilometre away at a low angle across dark flat ground, so that the whole damaged building and the stack are "
            "large in the frame. "
        ),
    },
    "chn_b": {
        "ep": "ep24",
        "name": "数日後の昼、煙を上げる4号炉の上を砂の袋を吊った軍のヘリが飛ぶ",
        "hypothesis": "事故の大きさ（炉を空から埋める）が昼の明るい色で伝わる。反転版の字のすき間に機体と排気筒が出る。"
                      "ヘリの細部（型・印）は描かせない",
        "look": LOOK_CHN.replace("natural colours.", "natural colours, in hazy daylight."),
        "frame": FRAME_CHN, "ban": BAN_CHN, "tail": TAIL_CHN,
        "scene": (
            "Early May 1986, a few days after the explosion, daytime under a hazy sky. "
            + CHN_PLANT[0].upper() + CHN_PLANT[1:] +
            "A thin plume of grey smoke still rises from the ruined top of the building. Two large military transport "
            "helicopters in plain olive-green paint fly low over the ruined building, each carrying a big sack in a net "
            "hanging under it on a long cable, about to drop sand into the open reactor. Seen from a distance at a "
            "slightly low angle, so that the building, the stack and the helicopters are large across the middle of the "
            "frame. "
        ),
    },
})

# 🆕 25本目（2026-10-26・⑥）：JR福知山線脱線事故＝カズヤくん「T2（付図12 の空撮）の拡大が最有力。T2 をより派手に再現した AI イラストを生成」
#    🔴 札は新規（ほかの回の札を流用しない＝ルール 6-55④）。禁止は文字だけ（10-21 の決め＝§6-55b）＋この回の約束で、亡くなった人・
#    けがをした人・血は描かせない（乗客106人と運転士が亡くなった実在の事故＝人は救助の人が小さく写る程度）。
#    事実の芯（報告書 p.1・付図12）：2005-04-25 9時18分ごろ・晴れた朝・尼崎市の右の曲線・7両編成のうち前の5両が脱線・前の2両は線路の脇の
#    マンションにぶつかった（1両目はマンションの1階の駐車場に入り込み、2両目は建物の角に巻き付くように）・隣に平らな駐車場・救助のクレーン。
#    電車＝ステンレスの銀色の車体に青い帯（207系）＝会社の印・字は描かせない。本番は H 型の反転版（字の外がカラー・大きな語「JR福知山線」）
LOOK_FUK = (
    "A real aerial PHOTOGRAPH taken from a helicopter with a professional camera: sharp, clear and high-resolution, "
    "bright late-April morning sunlight, natural and vivid colours, strong contrast, true depth of field. "
)
FRAME_FUK = (
    "COMPOSITION, critical: 16:9 frame, seen obliquely from above at about 35 degrees, closer than a usual news "
    "aerial. A wide white line of lettering will later cover the top 18% of the frame, a yellow line the bottom 22%, "
    "and one huge word will run across the whole middle. So the crushed front cars and the building must be LARGE, "
    "spread across most of the width of the frame through the middle, and readable at a glance even when the "
    "picture is tiny. "
)
BAN_FUK = (
    "No text, letters, numbers, words, logos, emblems, signs, number plates or watermarks of any kind, in any language. "
    "No injured people, no bodies, no blood. "
)
TAIL_FUK = (
    "The result must look like a genuine, dramatic news photograph of a real moment, full of urgent detail. It must "
    "NOT look like a render, a video game, a movie poster, a 3D visualisation, a model or an illustration."
)
SCENES.update({
    "fuk_a": {
        "ep": "ep25",
        "name": "脱線の直後の朝の空撮（前の2両がマンションに突っ込み・後ろの車両が曲線に折れ曲がる・救助のクレーンと車）",
        "hypothesis": "カズヤくんの選んだ T2（付図12 の空撮）の構図を近く・明るく・細部を多く。原寸 653px の引き伸ばしのぼけを避ける。"
                      "反転版の字の外に銀の車体と建物とクレーンが出る",
        "look": LOOK_FUK, "frame": FRAME_FUK, "ban": BAN_FUK, "tail": TAIL_FUK,
        "scene": (
            "A spring day in 2005 in a dense residential district of a Japanese city, during the rescue operation on "
            "the same day a commuter train derailed on a sharp right-hand curve of a double-track railway line. The train "
            "is made of silver stainless-steel commuter cars with a blue stripe along the sides. The first car has "
            "been crushed flat into the open ground-floor parking garage of a tall, light-beige nine-storey apartment "
            "building right beside the track; the second car is bent around the corner of the building like a "
            "folded sheet of metal, its silver body torn open and dented; the third, fourth and fifth cars have "
            "jumped off the rails and lie crooked and tilted across the tracks and the gravel, zig-zagging back "
            "along the curve, while the last two cars still stand on the rails. Bright orange and red mobile cranes "
            "with long extended booms stand beside the wreck, and many red fire engines, white ambulances and rescue "
            "vehicles with flashing lights crowd the narrow streets and a big flat car park full of parked cars next "
            "to the building. Blue tarpaulins lie on the ground. Rescue workers in helmets are visible only as tiny "
            "figures. Bright morning sunlight glints on the twisted steel. "
        ),
    },
    # 🆕 10-26 カズヤくん（fuk_a を H 型の反転版に当てた並べを見て）「もっと車両に寄せて、横転した車両で画面がいっぱいになるようなイラストを生成」
    #    ＝寄りの空撮。横倒しの銀の車体（青い帯）が画面の横いっぱい・建物の角とクレーンは端だけ。人は救助の人が小さく（顔・けが・血は描かない）
    "fuk_b": {
        "ep": "ep25",
        "name": "寄りの空撮：横倒しになった銀と青の車両が画面いっぱい（線路の砂利・ねじれた鋼・端に建物の角）",
        "hypothesis": "反転版は字の外がカラー＝字のすき間がどこでも横倒しの車体の銀と青になる。fuk_a は車両が小さく字の後ろに隠れた",
        "look": LOOK_FUK, "ban": BAN_FUK, "tail": TAIL_FUK,
        "frame": (
            "COMPOSITION, critical: 16:9 frame, a CLOSE aerial view from a low-flying helicopter, looking down at about "
            "50 degrees. The overturned train cars must FILL THE WHOLE FRAME from the left edge to the right edge and "
            "from top to bottom, so that any small part of the picture shows silver steel, the blue stripe, broken "
            "windows or twisted metal. A wide line of lettering will later cover the top 18% and the bottom 22%, and "
            "one huge word will run across the whole middle, so there must be no empty sky and no plain ground. "
        ),
        "scene": (
            "A spring day in 2005 in a Japanese city, during the rescue operation on the same day a commuter train "
            "derailed on a sharp right-hand curve. Seen from close above: two silver stainless-steel commuter train "
            "cars with a blue stripe along their sides lie overturned on their sides across the double track and the "
            "grey gravel, one behind the other, their roofs and sides crumpled, dented and torn open, rows of broken "
            "windows, bent window frames and twisted steel panels, a bogie with its wheels lying beside them, the "
            "rails bent out of shape under the cars. At one edge of the frame, the corner of a light-beige apartment "
            "building is smashed where the front of the train hit it, with concrete rubble and dust. A bright orange "
            "mobile crane boom reaches across one corner. Tiny rescue workers in orange and dark blue uniforms and "
            "white helmets stand on and around the cars. Bright morning sunlight glints on the twisted steel. "
        ),
    },
})


def build(v):
    """🔴 質感（look）と締め（tail）は**場面ごとに差し替えられる**（2026-09-22 追加）。

    それまではここが「崩れた**あと**」「動きのブレなし」で決め打ちだった。
    「崩れている**最中**」を作るには、静けさを求める `LOOK` と
    「no motion blur / no dramatic lighting」で終わる締めが**真正面からぶつかる**。
    ⚠️ 10本目の場面は `FRAME`（文字の帯）・`BAN`（人・炎・文字）・`PINK` を外さない。
    🆕 14本目（2026-09-29）：構図と禁止も**場面ごとに差し替える**（`frame`・`ban`）。
       10本目の札は建物の崩落向け（粉じん・地面の靴・車）＝海の場面に流用しない。
    """
    s = SCENES[v]
    return (f"{s.get('look', LOOK)}{s['scene']}{s.get('frame', FRAME)}"
            f"{s.get('ban', BAN)}{s.get('tail', TAIL)}")


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
    # 🆕 14本目（2026-09-29）：出力先と名前の頭を場面の `ep` から（無ければ10本目のまま）
    ep = SCENES[v].get("ep", "ep10")
    out = HERE / "ref" / ep / "ai"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{ep}_{v}_prompt.txt").write_text(prompt, encoding="utf-8")

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
    # 🆕 15本目（2026-09-30）：生成の原寸も残す（14本目は 1280x720 に縮めた版しか残らず、寄ると細部が甘かった）
    im.save(out / f"{ep}_{v}_orig.png")
    w, h = im.size
    target = w * 9 / 16
    if h > target:
        t = int((h - target) / 2)
        im = im.crop((0, t, w, int(t + target)))
    im = im.resize((1280, 720), Image.LANCZOS)
    dst = out / f"{ep}_{v}.jpg"
    im.save(dst, "JPEG", quality=94)
    im.resize((246, 138), Image.LANCZOS).save(out / f"{ep}_{v}_246.jpg", "JPEG", quality=92)
    print(f"OK -> {dst}（246px版も出力）")
    print("🔴 次＝thumb_jiko.py で赤・黄を焼いてから検品する（地だけで判断しない）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
