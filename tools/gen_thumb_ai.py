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
