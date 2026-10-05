# -*- coding: utf-8 -*-
"""19本目①棚卸し：旧版（4本目）の素材 `ref/surfside/` 69点と記録映像の判定表を書き出す。

    python ref/ep19/old/materials_table.py      → ref/ep19/materials.md

機械で取る欄＝大きさ（PIL で頭だけ読む）・md5・旧版でどのカットに使ったか（old_metrics.json）・
記録映像の割り当て（同）・画面に出た出典行（同）・OCR の行数（ref/surfside/ocr_slides.json）。
判定の欄（何か・権利・人・19本目で使えるか）は下の J（人が書いた判定）＝出どころはそれぞれの「根拠の資料」。
⚠️ 画像は「開いて見て」いない（大きさの頭と OCR の文字だけ）。人が写るかは検品の台帳の記述から。
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent            # ref/ep19/old
REPO = HERE.parents[2]
SRC = REPO / "ref" / "surfside"
OUT = HERE.parent / "materials.md"

TF = "TF 動画"      # 凡例で説明
NU = "NIST 頁"

# ── 判定（人が書いた）──────────────────────────────────────
# what=何か／who=権利者／basis=根拠／people=人が写るか／ok=○△×／why=理由
A_SLIDE = "A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST`"
A_SLIDE_NOSRC = "A＝米連邦 §105（NIST の職務著作）と判断。OCR に Source 行なし・第三者の印も無し"
A_BROLL = "A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし）"
A_TL = "A と推定（NIST 頁の『Materials testing time-lapse videos』＝ミネソタ大学での試験。撮影者の記載なし）"
A_GIF = "A（頁に Credit: NIST）"


def basis_of_clip(clip):
    return A_TL if clip == "ss_tl" else (A_GIF if clip == "ss_gif" else A_BROLL)
J = {
    # 技術的知見のスライド（TF 動画のコマ・見出し帯を切って 3200px 以下に）
    "tf_p003_model.jpg": dict(what="TF p3 建物の3Dモデル＋寸法（West=demolished・Middle/East=collapsed・Pool Deck・寸法 ft と m）",
                              who="NIST", basis=A_SLIDE, people="なし", ok="○", why="NIST 製の3D。英字の札は訳を重ねる"),
    "tf_p016_body.jpg": dict(what="TF p16 本文（「余裕は決定的に小さかった」の箱）＋赤黄の点の地図", who="NIST", basis=A_SLIDE,
                             people="なし", ok="○", why="旧版では未使用（map と legend に切り分けて使った）"),
    "tf_p016_legend.jpg": dict(what="TF p16 の凡例だけ（severe 赤・moderate 黄）", who="NIST", basis=A_SLIDE,
                               people="なし", ok="○", why="680x310 と小さい＝全画面は×2.8の拡大。⚠️ CREDITS.md の表に無い（台帳漏れ）"),
    "tf_p016_map.jpg": dict(what="TF p16 の赤黄の点の地図だけ（y<870 で切った）", who="NIST", basis=A_SLIDE,
                            people="なし", ok="○", why="点の数＝赤36・黄19（ss.py の定数・機械で数えた値）"),
    "tf_p016_q.jpg": dict(what="TF p16 の問いの帯「Why did the structure collapse … 40 years after construction was complete?」",
                          who="NIST", basis=A_SLIDE_NOSRC, people="なし", ok="○", why="文字だけの画面（2割の枠に数える）"),
    "tf_p029_model.jpg": dict(what="TF p29 建物の3D（方角・各部）", who="NIST", basis=A_SLIDE, people="なし", ok="○", why="NIST 製の3D"),
    "tf_p036_punch.jpg": dict(what="TF p36 押し抜きせん断の線図（白地・英語の表題は切った）", who="NIST", basis=A_SLIDE_NOSRC,
                              people="なし", ok="○", why="機構の線図。白地の細線＝地に敷かない"),
    "tf_p048_deck.jpg": dict(what="TF p48 プールデッキの3D切り欠き（K/L/M・11.1/13.1）", who="NIST", basis=A_SLIDE, people="なし",
                             ok="○", why="K・L の札はファイル上端＝見出し帯に入る（台帳 G-06・A-10）"),
    "tf_p050_3d.jpg": dict(what="TF p50 3週間前の3D（右上の ©2021 の門の写真は切った）", who="NIST", basis=A_SLIDE, people="なし",
                           ok="○", why="©2021 Used with permission の部分を切ってある"),
    "tf_p050_gate.jpg": dict(what="TF p50 門の描き起こし（1か月前・3週間前の2段）", who="NIST",
                             basis="A。札「Source: NIST (artist rendering based on eyewitness accounts)」", people="なし",
                             ok="○", why="目撃談にもとづく絵＝数値は「目撃談」として扱う"),
    "tf_p052_3d.jpg": dict(what="TF p52 1週間前の3D（右上の ©2021 は切った）", who="NIST", basis=A_SLIDE, people="なし",
                           ok="○", why="旧版では未使用"),
    "tf_p052_gate.jpg": dict(what="TF p52 門の描き起こし（3段目「Approx. 1\" vertical shift after repairs.」）", who="NIST",
                             basis="A。札「NIST (artist rendering based on eyewitness accounts)」", people="なし",
                             ok="○", why="同上"),
    "tf_p057_3d.jpg": dict(what="TF p57 17時間前の3D（右上の CTS Receiver の写真は切った）", who="NIST", basis=A_SLIDE,
                           people="なし", ok="○", why="—"),
    "tf_p057_memo.jpg": dict(what="TF p57 手書きの図と文「Morning June 23 noticed in the floor area, a space or gap of 4 inches」＋凡例",
                             who="NIST", basis="A。INDEX.md の書き起こし＝`Source: NIST`・`Annotations (not to scale) from an eyewitness interview.`",
                             people="なし", ok="○",
                             why="⚠️ 聞き取りのときの書き込み＝「崩落前日に住民が書いた」と読ませない（旧タイトルの誤り）。1248px＝4倍の拡大でにじむ（台帳 B-08）"),
    "tf_p058_3d.jpg": dict(what="TF p58 9時間前の3D", who="NIST", basis=A_SLIDE, people="なし", ok="○", why="—"),
    "tf_p058_note.jpg": dict(what="TF p58 付箋「Leak from the ceiling, not the pipe - 1/4 inch deep crack」＋下地の駐車場の区画図（線・柱・丸印・赤い斜線）",
                             who="付箋＝NIST（聞き取りの注記）／下地の区画図＝**CTS Receiver（管財人）の原図**",
                             basis="混在：注記は A。原図は第三者（§105 の外）＝スライドの札「Source: CTS Receiver (original drawing)」",
                             people="なし", ok="△",
                             why="原図が写る（台帳 B-16）＝紙面の引用（額装・無加工・出典に原図の出どころ）か、付箋だけに切り直す。1018px と小さい"),
    "tf_p062_summary.jpg": dict(what="TF p62 まとめ（3週間前・1週間前の吹き出し）", who="NIST", basis=A_SLIDE, people="なし", ok="○", why="—"),
    "tf_p065_garage.jpg": dict(what="TF p65 9分前の駐車場3D（カウントダウンの帯を除く）", who="NIST", basis=A_SLIDE_NOSRC,
                               people="なし", ok="○", why="柱の札が見出し帯に入る（台帳 E-19）"),
    "tf_p067_deflect.jpg": dict(what="TF p67 6〜7分前のたわみ（a/b/c）＋左下の断面", who="NIST", basis=A_SLIDE_NOSRC,
                                people="なし", ok="○", why="—"),
    "tf_p075_cover.jpg": dict(what="TF p75 かぶり「¾ in. … design drawings／2 in. cover as built」＋スラブ断面の実物写真", who="NIST",
                              basis=A_SLIDE, people="なし", ok="○", why="決め所の頁。インチ＝換算を添える"),
    "tf_p076_bars.jpg": dict(what="TF p76 設計図の抜粋（赤枠の注記 AT LEAST 25%…）＋柱の標本写真＋本文（At this location, only 2 rather than 4…）",
                             who="写真＝NIST／**図面＝Town of Surfside（町）の提供**",
                             basis="混在：写真は A。図面は §105 の外（町の提供・図の作者は当時の設計側＝推測）＝札「Source for photographs: NIST; Source for drawing: Town of Surfside」",
                             people="なし", ok="△",
                             why="紙面の引用（§2-6c の型＝頁ごと・額装・無加工・図面の出どころを出典に）。旧版は切出・色・寄りで改変し出典は「PD」だけ"),
    "tf_p084_salt.jpg": dict(what="TF p84 塩水浴と電極の腐食試験（Salt-Water Bath with Electrodes）", who="NIST", basis=A_SLIDE,
                             people="なし（推測）", ok="○", why="試験の方法の頁＝「海の塩が原因」の根拠にはならない"),
    "tf_p086_causes.jpg": dict(what="TF p86 原因5つの箱＋左2つの波括弧（プランターは near north side of pool）", who="NIST",
                               basis=A_SLIDE_NOSRC, people="なし", ok="○", why="文字だけの画面。旧版は8カットで使用"),
    "tf_p133_plan.jpg": dict(what="TF p133 崩落範囲の平面図だけ（Zone A／Zone B。右の断面写真は出さない）", who="NIST",
                             basis=A_SLIDE_NOSRC + "（INDEX.md の p133 は Source: NIST）", people="なし", ok="○",
                             why="右の断面写真（室内が見える）は切ってある＝そのまま"),
    "tf_p139_bars.jpg": dict(what="TF p139 下端筋が抜ける線図（柱 D・E・H・I）", who="NIST", basis=A_SLIDE, people="なし", ok="○", why="決め所の頁"),
    "tf_p174_corr.jpg": dict(what="TF p174 鉄筋の腐食（Ongoing for more than 25 years）＋腐食した鉄筋の写真", who="NIST",
                             basis=A_SLIDE, people="なし", ok="○", why="—"),
    "tf_p185_87park.jpg": dict(what="TF p185 87 Park の振動の解析（地盤と建物の連成・答え3つ）＋左上の現場写真", who="NIST",
                               basis=A_SLIDE, people="**作業員が立つ現場の写真**（台帳 H-11）＝公務か不明＝⑤bで原寸", ok="○",
                               why="旧版は6カット続けて使った（c711〜c716）"),
    "tf_p189_not.jpg": dict(what="TF p189「Things that did not contribute significantly to the collapse」5項目", who="NIST",
                            basis=A_SLIDE_NOSRC, people="なし", ok="○", why="旧版では画像は未使用（quote と absent の札で再現）。文字だけの画面"),
    "tf_p191_closing.jpg": dict(what="TF p191 Closing Remarks（p86 と同じ5つの箱・pool deck）", who="NIST", basis=A_SLIDE_NOSRC,
                                people="なし", ok="○", why="文字だけの画面。旧版は7回使い ep01〜ep09 が文字だけ9連続"),
    # 記録映像の1コマ
    "ss_b1_sign.jpg": dict(what="B-Roll #1 の約9秒（建物の銘板 CHAMPLAIN TOWERS 8777 SOUTH）", who="NIST", basis=A_BROLL,
                           people="**作業員3人・横顔が判別できる（頭部≈120px）・ベストに社名 DESIMONE**（台帳 PR-13・PR-14）＝私企業の技術者の可能性（推測）",
                           ok="△", why="顔は切り方で外すか顔だけモザイク（PD は可＝§B2-2b）。旧版は pr10 と ep16 に同じ絵"),
    "ss_b2_87park.jpg": dict(what="B-Roll #2 の13秒（87 Park と現場の空撮）", who="NIST", basis=A_BROLL,
                             people="なし（重機の商標 CAT が読める＝台帳 H-03）", ok="○", why="3840x2026 の高解像"),
    "ocr_slides.json": dict(what="67点の OCR（Windows OCR・座標つき）。tf_p016_legend だけ無い", who="（自作のデータ）",
                            basis="—", people="—", ok="○", why="切り方と英字の門番の材料（画面に出す物ではない）"),
}

# 控えの静止画 fb_<cid>.jpg（⑤b〈431474d〉で当時の USE の区間から1コマ。正確な秒の記録は無い。
#  秒が台帳で分かるもの＝pr01 12.5秒・c628 159.3秒（853bb3f）・c223 102.5秒（59f065f）・c322≈128秒の表題カード〈OCR〉）
FB = {
    "pr01": ("崩れた棟（853bb3f で銘板のコマから 12.5秒に差し替え）", "不明＝⑤bで原寸", "○", "サムネの地にも使った（ss_b_face_bars ほか4案）"),
    "pr02": ("瓦礫の山と捜索の列（隣家の屋根）", "捜索隊 約10人・顔は判別不能（台帳 PR-04）＝公務・遠景", "○", "—"),
    "pr03": ("せん断された断面と瓦礫の上の捜索隊", "捜索隊＝公務。動く区間には**重機の商標と広告文・電話番号**（ALPHA WRECKING・We Break it Better・VOLVO＝台帳 PR-05）", "△", "商標・電話番号を切り方か秒で外す"),
    "c106": ("海岸線の空撮（`fb_c434.jpg` と md5 が同じ）", "なし（推測）", "○", "同じファイルが2つ＝1点として数える"),
    "c119": ("ドローン。片づいたデッキの床面と重機", "不明＝⑤bで原寸", "○", "崩落後の絵＝「門は直された」（崩落前）の語りと時制が合わない（台帳 A-13）"),
    "c128": ("瓦礫の上の捜索隊と柱", "捜索隊 約12人・背中と横顔で顔は判別不能（台帳 A-18）＝公務。重機の銘「MAXIM」風", "○", "—"),
    "c204": ("デッキ面の引き", "不明＝⑤bで原寸", "○", "—"),
    "c217": ("現場の床面。鉄筋の出た版とコーン", "なし（推測）", "○", "—"),
    "c223": ("瓦礫の山と重機の腕（59f065f で 102.5秒に差し替え）", "顔なし（台帳）", "○", "—"),
    "c315": ("NIST の GIF の1コマ（押し抜きせん断の動く図）", "なし", "○", "GIF そのものは Credit: NIST（頁に明記）"),
    "c321": ("試験場の引き。試験機と技術者", "横顔が識別できる人物（頭部≈150px）・NIST ロゴのベスト3人（台帳 C-26）＝公務（NIST の職員と推測）", "○", "公務の人の顔は使ってよい（§B2-2）"),
    "c322": ("**ワシントン大学の表題カード**（OCR「Univ. of Washington | Laboratory Testing. Replicas of the CTS Pool-Deck Slab-Column Connections」＝当時の start 128秒）", "なし", "×", "表題カード＝絵として使わない（旧版の注意6）。本編では出ていない（動く映像が取れたため）"),
    "c324": ("スラブを真上から。格子と計測器（ワシントン大の区間＝推測）", "しゃがむ人物（台帳 C-33）＝研究者。梯子の商標 WERNER／LEANSAFE（C-28）", "○", "場所の書き分けが要る（§3 #4）"),
    "c325": ("圧縮試験機に入ったコア", "不明。区間の後ろは男性2人の顔の寄り（台帳 C-29）＝⑤bで原寸", "○", "—"),
    "c326": ("鉄筋の引張試験機", "なし（推測）", "○", "—"),
    "c327": ("柱まわり。スラブの裏側のひびと露出した鉄筋", "なし（推測）", "○", "—"),
    "c328": ("スラブの面を走るひびと計測カメラ", "動く区間はベストの人物4人・横顔（台帳 C-32）＝公務・研究者", "○", "—"),
    "c329": ("真上から・上の面（ワシントン大の区間＝推測）", "人物の腕（C-34）・梯子の LEANSAFE", "○", "場所の書き分けが要る（§3 #4）"),
    "c331": ("外れて落ちたスラブの裏側", "なし（推測）", "○", "—"),
    "c332": ("タイムラプス 0秒（全景）", "なし。**NIST の透かしの文字**が写る（OCR「…STITUTE OF／AND TECHNOLOGY／…NT OF COMMERCE」）", "△", "透かしを切り方で外す（旧版の動く区間は外してあった）"),
    "c333": ("タイムラプス 2.2秒（柱まわり）", "なし。**NIST の透かし**（OCR）", "△", "同上"),
    "c334": ("タイムラプス 4.7秒（落下）", "なし", "○", "—"),
    "c419": ("証拠倉庫で部材の鉄筋を測る", "人物の顔（マスク・眼鏡）（台帳 D-11）＝公務（NIST の調査員と推測）", "○", "—"),
    "c430": ("倉庫の引き。並んだ部材のあいだを歩く", "中央の2人が正面向き・**NIST ロゴ入りヘルメット**（台帳 D-17）＝公務", "○", "ロゴ入りヘルメットの寄りは旧版の禁止2に近い＝寄らない"),
    "c431": ("部材を積んだトレーラーが走る（120秒からカード）", "不明＝⑤bで原寸", "○", "—"),
    "c434": ("海岸線の空撮（`fb_c106.jpg` と同じファイル）", "なし（推測）", "○", "同上"),
    "c505": ("デッキの床面を歩く作業員", "作業員4人・顔は小さい・上から（台帳 E-05）＝公務（調査）と推測", "○", "プランターは写らない"),
    "c513": ("錆びた鉄筋の標本（袋と札）", "なし（推測）", "○", "—"),
    "c519": ("コア抜きの刃と水", "手元のみ（推測）", "○", "—"),
    "c520": ("圧縮試験機の中のコア", "なし。**Forney の銘板（社名・住所・電話・URL）**が読める（台帳 E-12）", "△", "銘板を切り方で外す"),
    "c521": ("倉庫の床一面の部材", "不明＝⑤bで原寸", "○", "—"),
    "c607": ("試験機の全景（38秒から顔）", "作業員3人（台帳 F-04）＝研究者", "○", "—"),
    "c628": ("残った棟の断面＋重機の腕（853bb3f で 159.3秒に差し替え）", "なし。**重機の商標 ALPI（ALPINE）**が大きく読める（台帳 F-25）", "△", "断面が見えるのは 159〜160秒の1秒だけ"),
    "c703": ("高い所からの現場の引き（海が見える）", "不明。OCR に「ALPHA」（重機の商標の可能性＝推測）", "△", "区間の尻（204秒）から表題カード（台帳 H-01）"),
    "c709": ("残った棟＝住民が住んでいた建物の断面", "人はいない（推測）が**住戸の中が見える**＝私人の暮らしの場", "△", "§B2-2 の表に無い型＝見せ方はカズヤくんの判断（推測で×にしない）"),
    "c713": ("倉庫でコアに計測器をあてる手元（B-Roll #5 153秒＝⑤b の割り当て）", "手元（推測）", "○", "旧版では未使用（⑤c H-10 で p185 に差し替え）＝`fb_c713.jpg` だけ残った"),
    "c726": ("ドローン。現場の引き", "不明。区間の尻（114秒〜）に NIST の表題カードと**氏名テロップ**（台帳 H-21）", "○", "until 113.25 を守る"),
}


CLIP_NAME = {   # 場所は書かない（B-Roll #8 は前半ミネソタ大・後半ワシントン大＝§3 #4）
    "ss_b1": "B-Roll #1（崩落現場）", "ss_b2": "B-Roll #2（空撮・現場）", "ss_b3": "B-Roll #3（証拠倉庫）",
    "ss_b4": "B-Roll #4（部材の搬送）", "ss_b5": "B-Roll #5（コア抜き・倉庫）", "ss_b6": "B-Roll #6（コアの試験）",
    "ss_b7": "B-Roll #7（鉄筋の試験）", "ss_b8": "B-Roll #8（実物大の試験）", "ss_tl": "材料試験タイムラプス",
    "ss_gif": "NIST の押し抜きせん断の GIF",
}


def esc(x):
    """Markdown の表の区切り「|」を逃がす。"""
    return str(x).replace("|", "\\|")


def size_of(p):
    from PIL import Image
    with Image.open(p) as im:
        return im.size


def main():
    m = json.loads((HERE / "old_metrics.json").read_text(encoding="utf-8"))
    ocr = json.loads((SRC / "ocr_slides.json").read_text(encoding="utf-8"))
    use, clips = m["footage_use"], m["footage_clips"]
    usage = {k.split("/", 1)[1]: v for k, v in m["photo_by_file"].items()}
    files = sorted(p.name for p in SRC.iterdir())
    md5 = {f: hashlib.md5((SRC / f).read_bytes()).hexdigest() for f in files}
    dup = Counter(md5.values())

    rows, tally, tally_kind, tally_basis = [], Counter(), Counter(), Counter()
    MIXED = {"tf_p076_bars.jpg", "tf_p058_note.jpg"}
    for f in files:
        if f.endswith(".json"):
            tally_basis["データ（ocr_slides.json）"] += 1
        elif f in MIXED:
            tally_basis["混在（NIST＋第三者）"] += 1
        elif f.startswith("tf_") or f == "fb_c315.jpg":
            tally_basis["A（スライドの Source: NIST／頁の Credit: NIST・GIF）"] += 1
        else:
            tally_basis["A と推定（B-Roll・撮影者の記載なし）"] += 1
        p = SRC / f
        wh = "—" if f.endswith(".json") else "{}x{}".format(*size_of(p))
        n_ocr = len(ocr.get(f, {}).get("lines", [])) if f in ocr else "—"
        if f.startswith("fb_"):
            cid = f[3:-4]
            what, people, ok, why = FB[cid]
            u = use.get(cid)
            if u:
                cl = clips[u["clip"]]
                seg = f"{u['start']}秒" + ("（静止画で表示）" if u.get("still") else
                                           f"〜{u.get('until', '')}秒（本編は動く映像＝この静止画は出ていない）")
                src = f"{CLIP_NAME[u['clip']]}（Kaltura `{cl.get('entry', '')}`）＝{NU}" \
                    if cl.get("entry") else f"{CLIP_NAME[u['clip']]}（{cl.get('url', '').split('?')[0]}）＝{NU}"
                used = f"{cid}：{seg}"
            else:
                src = f"B-Roll #5（Kaltura `1_ecar0b6h`）＝{NU}"
                used = "未使用（USE に無い）"
            if f in ("fb_pr01.jpg", "fb_pr02.jpg", "fb_pr03.jpg"):
                used += "／サムネの地（pr01＝採用案）" if f == "fb_pr01.jpg" else "／サムネの案の地"
            who, basis = "NIST", (basis_of_clip(u["clip"]) if u else A_BROLL)
            kind = "記録映像の控えの静止画"
        else:
            j = J[f]
            what, who, basis, people, ok, why = j["what"], j["who"], j["basis"], j["people"], j["ok"], j["why"]
            if f.startswith("tf_"):
                src = f"{TF}（Kaltura `1_vezbt9jw`）のコマ＝{NU}"
                kind = "技術的知見のスライド"
            elif f.startswith("ss_"):
                src = ("B-Roll #1（Kaltura `1_ju6nndhb`）" if "b1" in f else "B-Roll #2（Kaltura `1_64zdekws`）") + f"＝{NU}"
                kind = "記録映像の1コマ（わざと静止画）"
            else:
                src = "—"
                kind = "データ"
            used = "、".join(usage.get(f, [])) or ("—（データ）" if kind == "データ" else "未使用")
        if dup[md5[f]] > 1:
            why += f"（md5 {md5[f][:8]} が同じファイルあり）"
        tally[ok] += 1
        tally_kind[(kind, ok)] += 1
        cells = [f"`{f}`", wh, what, src, who, basis, people, used, f"**{ok}**", why]
        rows.append("| " + " | ".join(esc(x) for x in cells) + " |")

    o = []
    o.append("---\ntitle: 19本目①棚卸し — 旧版（4本目）の素材の再点検（判定の表）\ncreated: 2026-10-05\n"
             "tags: [project/jiko-kensho, ep19]\n---\n")
    o.append("# 19本目①棚卸し — 旧版の素材 `ref/surfside/` 69点と記録映像の判定\n")
    o.append("> **判定の表だけ（取得はしていない）**。画像は開いていない＝大きさは PIL で頭だけ読み、中身は "
             "`ref/CREDITS.md`・`ref/surfside/ocr_slides.json`・`analytics/materials/surfside/tf_frames/INDEX.md`・"
             "`tools/footage.py` の注記・検品の台帳 `qa_out/surfside_open.md`（e6fe892）の文字から。"
             "**人が写るかは台帳の記述で、書いていない物は「不明＝⑤bで原寸」**。\n"
             "> 表は `ref/ep19/old/materials_table.py` が書いた（大きさ・md5・使ったカット・出典行は機械、判定の欄は人）。\n"
             "> `ref/surfside/` は `e6fe892`（公開版）と HEAD で69点とも同じ blob（`git diff` で確認）。\n")
    o.append("## §0 物差しと凡例\n")
    o.append("- **権利の根拠**（ルール §2-10・記憶 `feedback-pd-label-hides-two-different-grounds`）：**A＝米連邦 §105**"
             "（合衆国政府の職員の職務の著作）／B＝所有者の自主宣言（PDM・CC0）／C＝更新されなかった米国著作物／D＝撮影国の短い保護期間。"
             "この回の素材は **A か、A と推定**か、**第三者が混ざる**の3つだけ（B・C・D・CC は0点）。")
    o.append("- **NIST の方針**（https://www.nist.gov/copyrights-disclaimers ・2026-10-05 に読んだ）：著作権の印の付いた物を除き、"
             "NIST のサイトの情報は “considered public information and may be distributed or copied”。クレジットの表示を求めている。")
    o.append("- **人が写る写真**（§B2-2・§B2-2b・記憶 `feedback-jiko-photo-people-policy`）：公的な任務の人の顔＝使ってよい／"
             "私人の顔＝使わない（CC BY・PD は顔だけモザイクで可）／血・傷・損傷のある遺体＝使わない／覆われた遺体・担架＝遠景だけ。")
    o.append("- **量**（§2-1・記憶 `feedback-jiko-photo-ratio`）：写真・映像は20%以上・上限なし。PD 以外も引用の要件で使える"
             "（§2-5・2-5b）。公的機関の紙面に載った第三者の図・写真は「紙面の引用」（頁ごと・額装・無加工・出どころを出典に）で可（§2-6c）。")
    o.append(f"- **{TF}**＝NIST『NCST Champlain Towers South Investigation | Technical Findings (June 2026)』"
             "（Kaltura `1_vezbt9jw`・77.3分・3840x2160）。スライドはここから1コマずつ抜き、上の見出し帯（12.8%）を切って 3200px 以下に縮めた物。")
    o.append(f"- **{NU}**＝ https://www.nist.gov/disaster-and-failure-studies/champlain-towers-south-collapse/news-and-updates "
             "（2026-10-05 に200。B-Roll 8本は「B-roll videos (for the media)」の節・写真は「Credit: NIST」など）。")
    o.append("- 19本目＝○ 使える／△ 条件つき／× 使わない。\n")
    o.append("### 素材を取った道具と URL（git の差分から）\n")
    o.append("| commit | 道具 | 当たった URL |")
    o.append("|---|---|---|")
    o.append("| `e65a771`（②素材の実測） | `surfside_video.py`・`surfside_vidsheet.py`・`surfside_slides.py`・`surfside_assets.py`・`dvids_probe.py` | "
             "NIST `…/disaster-and-failure-studies/champlain-towers-south-collapse`・同 `/news-and-updates`（記録映像の entry を読む頁）／"
             "Kaltura `cdnapisec.kaltura.com/p/684682/…/playManifest/entryId/<entry>/…`（実ファイル・範囲取得）／"
             "YouTube の記者会見2本（`youtube.com/watch?v=…`）／DVIDS の画像頁と CDN（`dvidshub.net/image/…`・`d1ldvf68ux039x.cloudfront.net/thumbs/photos/…`） |")
    o.append("| `431474d`（⑤b） | `tools/footage.py`（使う区間だけ切り出す）・スライドのコマ抜き | Kaltura の10本（§2）／"
             "GIF `https://www.nist.gov/sites/default/files/styles/2800_x_2800_limit/public/images/2026/06/22/PunchingShear_001.gif` |")
    o.append("")
    o.append("⚠️ 旧版の道具3本（`footage.py`・`surfside_video.py`・`surfside_assets.py`）は `e6fe892` で **User-Agent に連絡先のメールアドレスが入っていた**"
             "（HEAD の `tools/` では0件）。昔の版から道具を写すときは消す（記憶 `feedback-no-email-in-tool-headers`）。\n")

    o.append("## §1 `ref/surfside/` 69点（1点1行）\n")
    o.append("| ファイル | 大きさ | 何か | 出どころ | 権利者 | 根拠 | 人が写るか | 旧版での使い方（カット） | 19本目 | 理由 |")
    o.append("|---|---|---|---|---|---|---|---|:-:|---|")
    o += rows
    o.append("")

    o.append("## §2 記録映像（クリップ）\n")
    o.append("器の大きさ＝②素材（2026-09-04）に ffprobe で測った値（`tools/footage.py` の `_SS`）。"
             "⚠️ **実効の幅は測っていない**（器の札は絵について嘘をつく＝§2-21・⑤bで使うコマごとに測る）。\n")
    o.append("| クリップ | 中身（`footage.py` の注記） | 元（Kaltura entry） | 長さ | 器の幅×高 | 1280以上 | 権利 | 旧版で使った区間（カット・秒） | 19本目 |")
    o.append("|---|---|---|---:|---|:-:|---|---|:-:|")
    by_clip = {}
    for c, u in use.items():
        by_clip.setdefault(u["clip"], []).append((c, u))
    verdict = {
        "ss_b1": ("○", "顔の寄り・重機の商標（ALPHA WRECKING・ALPI・MAXIM）・残った棟の住戸の中を避けて区間を選ぶ"),
        "ss_b2": ("○", "1:54以降はインタビュー。区間の尻の表題カード・氏名テロップ（台帳 H-21）に注意"),
        "ss_b3": ("○", "—"),
        "ss_b4": ("○", "120秒からカード"),
        "ss_b5": ("○", "ロゴ入りヘルメットの寄りを避ける"),
        "ss_b6": ("○", "Forney の銘板（社名・電話）が写る区間に注意"),
        "ss_b7": ("○", "36秒からカード"),
        "ss_b8": ("△", "**2:08 以降はワシントン大学の試験**（注記）＝区間ごとに場所を書き分ける。撮影者の記載なし＝大学の撮影なら §105 の外（未確認）"),
        "ss_tl": ("○", "右下の NIST の透かしを切る。ミネソタ大学の試験（NIST 頁の説明）・撮影者の記載なし"),
        "ss_gif": ("○", "頁に Credit: NIST・図（人なし）"),
    }
    for k, cl in clips.items():
        segs = []
        for c, u in by_clip.get(k, []):
            if u.get("still"):
                segs.append(f"{c} {u['start']}（静止画）")
            else:
                segs.append(f"{c} {u['start']}〜{u.get('until', '')}" + (f"×{u['rate']}" if u.get("rate", 1.0) != 1.0 else ""))
        src = f"`{cl['entry']}`" if cl.get("entry") else cl.get("url", "")
        ok, why = verdict[k]
        wide = "○" if cl["w"] >= 1280 else "×"
        right = basis_of_clip(k)
        length = "167コマ（≈6.7秒）" if k == "ss_gif" else f"{cl['sec']}秒"
        o.append(f"| {k} | {esc(cl.get('note', ''))} | {src} | {length} | {cl['w']}x{cl['h']} | {wide} | {right} | "
                 f"{'／'.join(segs) or '—'} | **{ok}** {why} |")
    o.append("| （参考）TF 動画 | 技術的知見の解説（77.3分）。スライドの出どころ。話者 Judith Mitrani-Reiser・Glenn Bell（NIST の共同責任者＝公務） | `1_vezbt9jw` | 77.3分 | 3840x2160 | ○ | A（ただし p45・p103・p119・p147 は ©2021 Used with permission、p184 は Google Earth、p50・p52 右上は ©2021、p57・p58 は CTS Receiver の写真と原図、p58 右上は Miami Dade County Open Data Hub＝出さない） | 映像としては未使用（コマだけ） | **○** スライドの頁。p88 の CONTENT WARNING（第3・4節）の範囲は絵にしない |")
    o.append("")
    o.append("- 動く映像を当てたのは **30カット**（静止画で受けた6カット＝pr01 pr02 c106 c223 c434 c628 を除く）。"
             "本編で静止画に落ちたのはこの6件だけ＝取得失敗は0（06e §4 の照合）。")
    o.append("- **【映像あり】の条件（器の幅1280以上）は10本とも満たす**。中身は**崩落の後**の現場・倉庫・試験で、"
             "**崩落の瞬間の映像は無い**（p119 の廊下の映像は ©2021 Used with permission＝出さない）。")
    o.append("- NIST の頁にはほかに記者会見2本（2021・1280x720／1920x1014）・NCST Insider 14本（調査員の紹介＝顔の寄り）・"
             "タイムラプス2本目（set-up）がある＝旧版では未使用（②の実測 `事故検証-サーフサイド-素材実測の全文-20260904` §1）。\n")

    o.append("## §3 🔴 旧版の出典の書き方の誤り（権利者・根拠・場所の取り違え）\n")
    o.append("| # | どこ | 旧版の書き方 | 実際（原文） | 19本目での直し方 |")
    o.append("|---:|---|---|---|---|")
    cr76 = m["screen_credit"].get("c420", "")
    cr58 = m["screen_credit"].get("c220", "")
    cr8 = m["screen_credit"].get("c322", "")
    o.append(f"| 1 | `tf_p076_bars.jpg`（c420 c421 c423 c424 c428） | 画面「{cr76}」 | スライドの札「Source for photographs: NIST; **Source for drawing: Town of Surfside**」（OCR・INDEX.md）＝図面は §105 の外 | 図面の出どころを出典に出す・紙面の引用の型（額装・無加工）。旧版はデュオトーン・切り出し・寄りで改変していた |")
    o.append(f"| 2 | `tf_p058_note.jpg`（c220 c221） | 画面「{cr58}」 | p58 の札「**Source: CTS Receiver (original drawing)**」＋「Annotations from an eyewitness interview.」＝下地の区画図は管財人の原図（台帳 B-16：写っているのは区画の線・柱・丸印・赤い斜線・付箋） | 原図の出どころを出す（紙面の引用）か、付箋だけに切り直す |")
    o.append("| 3 | `ref/CREDITS.md` §4本目「切り落として使わない部分」 | 「管財人（CTS Receiver）の写真と原図 … p57・p58（**手書きのメモと付箋の周りだけを切った**）」＝切ったので権利の外、と読める | p58 の付箋の切り出しに原図が残っている（#2） | 台帳を直す |")
    o.append(f"| 4 | B-Roll #8 の出典行と語り（c322 c324 c329） | 画面「{cr8}」／c322 の語り「場所は、ミネソタ大学の試験場である」 | 使った区間（139〜148.25・188〜198・193.5〜202.5秒）は **128秒の表題カード「Univ. of Washington \\| Laboratory Testing: Replicas of the CTS Pool-Deck Slab-Column Connections」より後**＝ワシントン大学の試験（`footage.py` の注記「2:08〜ワシントン大の試験」・台帳 C-27・`fb_c322.jpg` の OCR）＝**推測（映像は見ていない）** | 区間ごとに場所を書き分ける（NIST 頁＝「ワシントン大学とミネソタ大学で実物大の複製を作って壊した」） |")
    o.append("| 5 | `ref/CREDITS.md`・`tools/footage.py` の B-Roll #8 | 「ミネソタ大学。**撮影は NIST**」 | NIST 頁に撮影者の記載は無い（B-Roll は題と「for the media」だけ・写真には Credit: NIST 等がある）。§105 は連邦の職員の職務の著作だけ＝大学や請負の撮影なら別＝**未確認** | 「NIST 配布（撮影者の記載なし）」と書き、根拠は「A と推定」で残す |")
    o.append("| 6 | 概要欄の出典 URL | `https://www.nist.gov/disaster-failure-studies/champlain-towers-south-investigation` | 2026-10-05 に GET で **404**。正しい頁＝`https://www.nist.gov/disaster-and-failure-studies/champlain-towers-south-collapse`（200）・その `/news-and-updates`（200） | 正しい URL に |")
    o.append("| 7 | `ref/CREDITS.md` §4本目の「ライセンス」の1行 | 「米国政府の職務著作＝パブリックドメイン」（全部を1行で） | スライドの中に第三者の部分がある（#1・#2）・B-Roll は撮影者の記載なし（#5）＝根拠が3通りに割れる | 階層ごとに行を分ける（§2-10） |")
    o.append("| 8 | `tf_p016_legend.jpg`（c406） | CREDITS.md の表に**載っていない**（853bb3f で地図から切り分けた） | — | 台帳に足す |")
    o.append("| 9 | `fb_c713.jpg` | 台帳・USE のどこにも無いのに `ref/surfside/` に残る（⑤c H-10 で c713 を p185 に差し替えた残り） | — | 19本目で使うなら出典を書き直す |")
    o.append("")

    o.append("## §4 集計\n")
    o.append("| 種類 | 点数 | ○ | △ | × |")
    o.append("|---|---:|---:|---:|---:|")
    kinds = ["技術的知見のスライド", "記録映像の控えの静止画", "記録映像の1コマ（わざと静止画）", "データ"]
    for k in kinds:
        n = sum(v for (kk, _ok), v in tally_kind.items() if kk == k)
        o.append(f"| {k} | {n} | {tally_kind[(k, '○')]} | {tally_kind[(k, '△')]} | {tally_kind[(k, '×')]} |")
    o.append(f"| **計** | **{sum(tally.values())}** | **{tally['○']}** | **{tally['△']}** | **{tally['×']}** |")
    o.append("")
    o.append("| 根拠 | 点数 |")
    o.append("|---|---:|")
    for k, n in tally_basis.most_common():
        o.append(f"| {k} | {n} |")
    o.append("| （混在の中身）tf_p076_bars＝町の図面／tf_p058_note＝管財人の原図 | — |")
    o.append("| B・C・D・CC BY・CC BY-SA・報道 | 0 |")
    o.append("")
    o.append("- 旧版で未使用＝`tf_p016_body.jpg`・`tf_p052_3d.jpg`・`tf_p189_not.jpg`・`fb_c713.jpg` の4点（ほか65点は1回以上）。"
             "md5 が同じ＝`fb_c106.jpg`＝`fb_c434.jpg`。")
    o.append("- **人の写り**（台帳の記述から）：公務（捜索隊・NIST の調査員・研究者）＝pr02・c128・c321・c328・c419・c430・c505・c607 ほか／"
             "**私企業の技術者の可能性**＝`ss_b1_sign.jpg`（ベストに DESIMONE・横顔が判別できる）／**私人の住居の中**＝`fb_c709.jpg`／"
             "不明＝⑤bで原寸＝表の「不明」の行。**私人の顔が写ると書かれた点は0**（台帳の範囲で）。血・遺体の写りの記述は0。")
    o.append("- **商標・連絡先の写り込み**：ALPHA WRECKING・We Break it Better・電話番号・VOLVO（pr03）／ALPI（c628）／MAXIM（c128）／"
             "Forney の銘板（c520）／WERNER・LEANSAFE（c324・c329）／CAT（c705）／DESIMONE（pr10・ep16）／NIST の透かし（c332・c333 の控え）。")
    o.append("- **19本目で足りないもの**（旧版の在庫の外）：崩落の前の建物の写真（Commons 2点は CC BY-SA 4.0・1280px 未満）／"
             "崩落の瞬間の映像（p119 は ©2021・隣の建物の監視カメラの映像は報道の素材＝引用の要件で検討）／"
             "FEMA（DVIDS）の現場写真28点（連邦＝A の候補）・Miami-Dade Fire Rescue の「PD」3点（**郡の機関＝§105 の外**＝根拠は Commons の印で見直す）・"
             "CC BY 2.0 1点（②の実測にあるが旧版は未使用）"
             "＝`事故検証-サーフサイド-素材実測の全文-20260904` §3〜§6。\n")
    o.append("## 関連\n- `ref/ep19/old_script_inventory.md`（台本とカットの数）／`ref/ep19/old/old_tables.md`（全部の表）"
             "／`ref/CREDITS.md` §4本目／Vault `事故検証-ルール統合版-20260923` §2・§B2\n")
    OUT.write_text("\n".join(o) + "\n", encoding="utf-8")
    print(f"✓ {OUT}（{len(rows)}行・○{tally['○']} △{tally['△']} ×{tally['×']}）")


if __name__ == "__main__":
    main()
