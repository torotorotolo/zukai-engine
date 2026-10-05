---
title: 19本目①棚卸し — 旧版（4本目）の素材の再点検（判定の表）
created: 2026-10-05
tags: [project/jiko-kensho, ep19]
---

# 19本目①棚卸し — 旧版の素材 `ref/surfside/` 69点と記録映像の判定

> **判定の表だけ（取得はしていない）**。画像は開いていない＝大きさは PIL で頭だけ読み、中身は `ref/CREDITS.md`・`ref/surfside/ocr_slides.json`・`analytics/materials/surfside/tf_frames/INDEX.md`・`tools/footage.py` の注記・検品の台帳 `qa_out/surfside_open.md`（e6fe892）の文字から。**人が写るかは台帳の記述で、書いていない物は「不明＝⑤bで原寸」**。
> 表は `ref/ep19/old/materials_table.py` が書いた（大きさ・md5・使ったカット・出典行は機械、判定の欄は人）。
> `ref/surfside/` は `e6fe892`（公開版）と HEAD で69点とも同じ blob（`git diff` で確認）。

## §0 物差しと凡例

- **権利の根拠**（ルール §2-10・記憶 `feedback-pd-label-hides-two-different-grounds`）：**A＝米連邦 §105**（合衆国政府の職員の職務の著作）／B＝所有者の自主宣言（PDM・CC0）／C＝更新されなかった米国著作物／D＝撮影国の短い保護期間。この回の素材は **A か、A と推定**か、**第三者が混ざる**の3つだけ（B・C・D・CC は0点）。
- **NIST の方針**（https://www.nist.gov/copyrights-disclaimers ・2026-10-05 に読んだ）：著作権の印の付いた物を除き、NIST のサイトの情報は “considered public information and may be distributed or copied”。クレジットの表示を求めている。
- **人が写る写真**（§B2-2・§B2-2b・記憶 `feedback-jiko-photo-people-policy`）：公的な任務の人の顔＝使ってよい／私人の顔＝使わない（CC BY・PD は顔だけモザイクで可）／血・傷・損傷のある遺体＝使わない／覆われた遺体・担架＝遠景だけ。
- **量**（§2-1・記憶 `feedback-jiko-photo-ratio`）：写真・映像は20%以上・上限なし。PD 以外も引用の要件で使える（§2-5・2-5b）。公的機関の紙面に載った第三者の図・写真は「紙面の引用」（頁ごと・額装・無加工・出どころを出典に）で可（§2-6c）。
- **TF 動画**＝NIST『NCST Champlain Towers South Investigation | Technical Findings (June 2026)』（Kaltura `1_vezbt9jw`・77.3分・3840x2160）。スライドはここから1コマずつ抜き、上の見出し帯（12.8%）を切って 3200px 以下に縮めた物。
- **NIST 頁**＝ https://www.nist.gov/disaster-and-failure-studies/champlain-towers-south-collapse/news-and-updates （2026-10-05 に200。B-Roll 8本は「B-roll videos (for the media)」の節・写真は「Credit: NIST」など）。
- 19本目＝○ 使える／△ 条件つき／× 使わない。

### 素材を取った道具と URL（git の差分から）

| commit | 道具 | 当たった URL |
|---|---|---|
| `e65a771`（②素材の実測） | `surfside_video.py`・`surfside_vidsheet.py`・`surfside_slides.py`・`surfside_assets.py`・`dvids_probe.py` | NIST `…/disaster-and-failure-studies/champlain-towers-south-collapse`・同 `/news-and-updates`（記録映像の entry を読む頁）／Kaltura `cdnapisec.kaltura.com/p/684682/…/playManifest/entryId/<entry>/…`（実ファイル・範囲取得）／YouTube の記者会見2本（`youtube.com/watch?v=…`）／DVIDS の画像頁と CDN（`dvidshub.net/image/…`・`d1ldvf68ux039x.cloudfront.net/thumbs/photos/…`） |
| `431474d`（⑤b） | `tools/footage.py`（使う区間だけ切り出す）・スライドのコマ抜き | Kaltura の10本（§2）／GIF `https://www.nist.gov/sites/default/files/styles/2800_x_2800_limit/public/images/2026/06/22/PunchingShear_001.gif` |

⚠️ 旧版の道具3本（`footage.py`・`surfside_video.py`・`surfside_assets.py`）は `e6fe892` で **User-Agent に連絡先のメールアドレスが入っていた**（HEAD の `tools/` では0件）。昔の版から道具を写すときは消す（記憶 `feedback-no-email-in-tool-headers`）。

## §1 `ref/surfside/` 69点（1点1行）

| ファイル | 大きさ | 何か | 出どころ | 権利者 | 根拠 | 人が写るか | 旧版での使い方（カット） | 19本目 | 理由 |
|---|---|---|---|---|---|---|---|:-:|---|
| `fb_c106.jpg` | 1920x1012 | 海岸線の空撮（`fb_c434.jpg` と md5 が同じ） | B-Roll #2（空撮・現場）（Kaltura `1_64zdekws`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし（推測） | c106：8.0秒（静止画で表示） | **○** | 同じファイルが2つ＝1点として数える（md5 9b50db69 が同じファイルあり） |
| `fb_c119.jpg` | 1920x1012 | ドローン。片づいたデッキの床面と重機 | B-Roll #2（空撮・現場）（Kaltura `1_64zdekws`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 不明＝⑤bで原寸 | c119：99.0秒〜108.0秒（本編は動く映像＝この静止画は出ていない） | **○** | 崩落後の絵＝「門は直された」（崩落前）の語りと時制が合わない（台帳 A-13） |
| `fb_c128.jpg` | 1920x1014 | 瓦礫の上の捜索隊と柱 | B-Roll #1（崩落現場）（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 捜索隊 約12人・背中と横顔で顔は判別不能（台帳 A-18）＝公務。重機の銘「MAXIM」風 | c128：115.0秒〜118.5秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c204.jpg` | 1920x1012 | デッキ面の引き | B-Roll #2（空撮・現場）（Kaltura `1_64zdekws`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 不明＝⑤bで原寸 | c204：95.8秒〜98.8秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c217.jpg` | 1920x1014 | 現場の床面。鉄筋の出た版とコーン | B-Roll #1（崩落現場）（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし（推測） | c217：74.0秒〜77.8秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c223.jpg` | 1920x1014 | 瓦礫の山と重機の腕（59f065f で 102.5秒に差し替え） | B-Roll #1（崩落現場）（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 顔なし（台帳） | c223：102.5秒（静止画で表示） | **○** | — |
| `fb_c315.jpg` | 1920x1080 | NIST の GIF の1コマ（押し抜きせん断の動く図） | NIST の押し抜きせん断の GIF（https://www.nist.gov/sites/default/files/styles/2800_x_2800_limit/public/images/2026/06/22/PunchingShear_001.gif）＝NIST 頁 | NIST | A（頁に Credit: NIST） | なし | c315：0.0秒〜6.7秒（本編は動く映像＝この静止画は出ていない） | **○** | GIF そのものは Credit: NIST（頁に明記） |
| `fb_c321.jpg` | 1920x1080 | 試験場の引き。試験機と技術者 | B-Roll #8（実物大の試験）（Kaltura `1_lebmphjw`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 横顔が識別できる人物（頭部≈150px）・NIST ロゴのベスト3人（台帳 C-26）＝公務（NIST の職員と推測） | c321：10.0秒〜16.75秒（本編は動く映像＝この静止画は出ていない） | **○** | 公務の人の顔は使ってよい（§B2-2） |
| `fb_c322.jpg` | 1920x1080 | **ワシントン大学の表題カード**（OCR「Univ. of Washington \| Laboratory Testing. Replicas of the CTS Pool-Deck Slab-Column Connections」＝当時の start 128秒） | B-Roll #8（実物大の試験）（Kaltura `1_lebmphjw`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし | c322：139.0秒〜148.25秒（本編は動く映像＝この静止画は出ていない） | **×** | 表題カード＝絵として使わない（旧版の注意6）。本編では出ていない（動く映像が取れたため） |
| `fb_c324.jpg` | 1920x1080 | スラブを真上から。格子と計測器（ワシントン大の区間＝推測） | B-Roll #8（実物大の試験）（Kaltura `1_lebmphjw`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | しゃがむ人物（台帳 C-33）＝研究者。梯子の商標 WERNER／LEANSAFE（C-28） | c324：188.0秒〜198.0秒（本編は動く映像＝この静止画は出ていない） | **○** | 場所の書き分けが要る（§3 #4） |
| `fb_c325.jpg` | 1920x1080 | 圧縮試験機に入ったコア | B-Roll #6（コアの試験）（Kaltura `1_zdyysoml`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 不明。区間の後ろは男性2人の顔の寄り（台帳 C-29）＝⑤bで原寸 | c325：47.0秒〜51.75秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c326.jpg` | 1920x1080 | 鉄筋の引張試験機 | B-Roll #7（鉄筋の試験）（Kaltura `1_glesd05g`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし（推測） | c326：24.0秒〜34.75秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c327.jpg` | 1920x1080 | 柱まわり。スラブの裏側のひびと露出した鉄筋 | B-Roll #8（実物大の試験）（Kaltura `1_lebmphjw`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし（推測） | c327：80.0秒〜88.0秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c328.jpg` | 1920x1080 | スラブの面を走るひびと計測カメラ | B-Roll #8（実物大の試験）（Kaltura `1_lebmphjw`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 動く区間はベストの人物4人・横顔（台帳 C-32）＝公務・研究者 | c328：64.0秒〜70.0秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c329.jpg` | 1920x1080 | 真上から・上の面（ワシントン大の区間＝推測） | B-Roll #8（実物大の試験）（Kaltura `1_lebmphjw`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 人物の腕（C-34）・梯子の LEANSAFE | c329：193.5秒〜202.5秒（本編は動く映像＝この静止画は出ていない） | **○** | 場所の書き分けが要る（§3 #4） |
| `fb_c331.jpg` | 1920x1080 | 外れて落ちたスラブの裏側 | B-Roll #8（実物大の試験）（Kaltura `1_lebmphjw`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし（推測） | c331：121.0秒〜127.75秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c332.jpg` | 1920x1080 | タイムラプス 0秒（全景） | 材料試験タイムラプス（Kaltura `1_gvpcaamy`）＝NIST 頁 | NIST | A と推定（NIST 頁の『Materials testing time-lapse videos』＝ミネソタ大学での試験。撮影者の記載なし） | なし。**NIST の透かしの文字**が写る（OCR「…STITUTE OF／AND TECHNOLOGY／…NT OF COMMERCE」） | c332：0.0秒〜6.8秒（本編は動く映像＝この静止画は出ていない） | **△** | 透かしを切り方で外す（旧版の動く区間は外してあった） |
| `fb_c333.jpg` | 1920x1080 | タイムラプス 2.2秒（柱まわり） | 材料試験タイムラプス（Kaltura `1_gvpcaamy`）＝NIST 頁 | NIST | A と推定（NIST 頁の『Materials testing time-lapse videos』＝ミネソタ大学での試験。撮影者の記載なし） | なし。**NIST の透かし**（OCR） | c333：2.2秒〜6.8秒（本編は動く映像＝この静止画は出ていない） | **△** | 同上 |
| `fb_c334.jpg` | 1920x1080 | タイムラプス 4.7秒（落下） | 材料試験タイムラプス（Kaltura `1_gvpcaamy`）＝NIST 頁 | NIST | A と推定（NIST 頁の『Materials testing time-lapse videos』＝ミネソタ大学での試験。撮影者の記載なし） | なし | c334：4.7秒〜6.8秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c419.jpg` | 1920x1080 | 証拠倉庫で部材の鉄筋を測る | B-Roll #3（証拠倉庫）（Kaltura `1_h4yeyz2f`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 人物の顔（マスク・眼鏡）（台帳 D-11）＝公務（NIST の調査員と推測） | c419：40.0秒〜46.0秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c430.jpg` | 1920x1080 | 倉庫の引き。並んだ部材のあいだを歩く | B-Roll #5（コア抜き・倉庫）（Kaltura `1_ecar0b6h`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 中央の2人が正面向き・**NIST ロゴ入りヘルメット**（台帳 D-17）＝公務 | c430：102.0秒〜109.0秒（本編は動く映像＝この静止画は出ていない） | **○** | ロゴ入りヘルメットの寄りは旧版の禁止2に近い＝寄らない |
| `fb_c431.jpg` | 1920x1080 | 部材を積んだトレーラーが走る（120秒からカード） | B-Roll #4（部材の搬送）（Kaltura `1_jvdq95ze`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 不明＝⑤bで原寸 | c431：108.0秒〜118.0秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c434.jpg` | 1920x1012 | 海岸線の空撮（`fb_c106.jpg` と同じファイル） | B-Roll #2（空撮・現場）（Kaltura `1_64zdekws`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし（推測） | c434：8.0秒（静止画で表示） | **○** | 同上（md5 9b50db69 が同じファイルあり） |
| `fb_c505.jpg` | 1920x1012 | デッキの床面を歩く作業員 | B-Roll #2（空撮・現場）（Kaltura `1_64zdekws`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 作業員4人・顔は小さい・上から（台帳 E-05）＝公務（調査）と推測 | c505：46.0秒〜49.5秒（本編は動く映像＝この静止画は出ていない） | **○** | プランターは写らない |
| `fb_c513.jpg` | 1920x1080 | 錆びた鉄筋の標本（袋と札） | B-Roll #7（鉄筋の試験）（Kaltura `1_glesd05g`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし（推測） | c513：42.0秒〜46.25秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c519.jpg` | 1920x1080 | コア抜きの刃と水 | B-Roll #5（コア抜き・倉庫）（Kaltura `1_ecar0b6h`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 手元のみ（推測） | c519：39.0秒〜46.5秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c520.jpg` | 1920x1080 | 圧縮試験機の中のコア | B-Roll #6（コアの試験）（Kaltura `1_zdyysoml`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし。**Forney の銘板（社名・住所・電話・URL）**が読める（台帳 E-12） | c520：116.0秒〜125.0秒（本編は動く映像＝この静止画は出ていない） | **△** | 銘板を切り方で外す |
| `fb_c521.jpg` | 1920x1080 | 倉庫の床一面の部材 | B-Roll #5（コア抜き・倉庫）（Kaltura `1_ecar0b6h`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 不明＝⑤bで原寸 | c521：11.0秒〜16.3秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c607.jpg` | 1920x1080 | 試験機の全景（38秒から顔） | B-Roll #8（実物大の試験）（Kaltura `1_lebmphjw`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 作業員3人（台帳 F-04）＝研究者 | c607：32.0秒〜37.75秒（本編は動く映像＝この静止画は出ていない） | **○** | — |
| `fb_c628.jpg` | 1920x1014 | 残った棟の断面＋重機の腕（853bb3f で 159.3秒に差し替え） | B-Roll #1（崩落現場）（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし。**重機の商標 ALPI（ALPINE）**が大きく読める（台帳 F-25） | c628：159.3秒（静止画で表示） | **△** | 断面が見えるのは 159〜160秒の1秒だけ |
| `fb_c703.jpg` | 1920x1014 | 高い所からの現場の引き（海が見える） | B-Roll #1（崩落現場）（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 不明。OCR に「ALPHA」（重機の商標の可能性＝推測） | c703：198.0秒〜203.5秒（本編は動く映像＝この静止画は出ていない） | **△** | 区間の尻（204秒）から表題カード（台帳 H-01） |
| `fb_c709.jpg` | 1920x1014 | 残った棟＝住民が住んでいた建物の断面 | B-Roll #1（崩落現場）（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 人はいない（推測）が**住戸の中が見える**＝私人の暮らしの場 | c709：138.0秒〜143.0秒（本編は動く映像＝この静止画は出ていない） | **△** | §B2-2 の表に無い型＝見せ方はカズヤくんの判断（推測で×にしない） |
| `fb_c713.jpg` | 1920x1080 | 倉庫でコアに計測器をあてる手元（B-Roll #5 153秒＝⑤b の割り当て） | B-Roll #5（Kaltura `1_ecar0b6h`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 手元（推測） | 未使用（USE に無い） | **○** | 旧版では未使用（⑤c H-10 で p185 に差し替え）＝`fb_c713.jpg` だけ残った |
| `fb_c726.jpg` | 1920x1012 | ドローン。現場の引き | B-Roll #2（空撮・現場）（Kaltura `1_64zdekws`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 不明。区間の尻（114秒〜）に NIST の表題カードと**氏名テロップ**（台帳 H-21） | c726：110.0秒〜113.25秒（本編は動く映像＝この静止画は出ていない） | **○** | until 113.25 を守る |
| `fb_pr01.jpg` | 1920x1014 | 崩れた棟（853bb3f で銘板のコマから 12.5秒に差し替え） | B-Roll #1（崩落現場）（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 不明＝⑤bで原寸 | pr01：12.5秒（静止画で表示）／サムネの地（pr01＝採用案） | **○** | サムネの地にも使った（ss_b_face_bars ほか4案） |
| `fb_pr02.jpg` | 1920x1014 | 瓦礫の山と捜索の列（隣家の屋根） | B-Roll #1（崩落現場）（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 捜索隊 約10人・顔は判別不能（台帳 PR-04）＝公務・遠景 | pr02：53.8秒（静止画で表示）／サムネの案の地 | **○** | — |
| `fb_pr03.jpg` | 1920x1014 | せん断された断面と瓦礫の上の捜索隊 | B-Roll #1（崩落現場）（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | 捜索隊＝公務。動く区間には**重機の商標と広告文・電話番号**（ALPHA WRECKING・We Break it Better・VOLVO＝台帳 PR-05） | pr03：15.0秒〜18.8秒（本編は動く映像＝この静止画は出ていない）／サムネの案の地 | **△** | 商標・電話番号を切り方か秒で外す |
| `ocr_slides.json` | — | 67点の OCR（Windows OCR・座標つき）。tf_p016_legend だけ無い | — | （自作のデータ） | — | — | —（データ） | **○** | 切り方と英字の門番の材料（画面に出す物ではない） |
| `ss_b1_sign.jpg` | 1920x1014 | B-Roll #1 の約9秒（建物の銘板 CHAMPLAIN TOWERS 8777 SOUTH） | B-Roll #1（Kaltura `1_ju6nndhb`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | **作業員3人・横顔が判別できる（頭部≈120px）・ベストに社名 DESIMONE**（台帳 PR-13・PR-14）＝私企業の技術者の可能性（推測） | pr10、ep16 | **△** | 顔は切り方で外すか顔だけモザイク（PD は可＝§B2-2b）。旧版は pr10 と ep16 に同じ絵 |
| `ss_b2_87park.jpg` | 3840x2026 | B-Roll #2 の13秒（87 Park と現場の空撮） | B-Roll #2（Kaltura `1_64zdekws`）＝NIST 頁 | NIST | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | なし（重機の商標 CAT が読める＝台帳 H-03） | c705 | **○** | 3840x2026 の高解像 |
| `tf_p003_model.jpg` | 3200x1570 | TF p3 建物の3Dモデル＋寸法（West=demolished・Middle/East=collapsed・Pool Deck・寸法 ft と m） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c101、c102、c103、c104、c602 | **○** | NIST 製の3D。英字の札は訳を重ねる |
| `tf_p016_body.jpg` | 3200x1224 | TF p16 本文（「余裕は決定的に小さかった」の箱）＋赤黄の点の地図 | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | 未使用 | **○** | 旧版では未使用（map と legend に切り分けて使った） |
| `tf_p016_legend.jpg` | 680x310 | TF p16 の凡例だけ（severe 赤・moderate 黄） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c406 | **○** | 680x310 と小さい＝全画面は×2.8の拡大。⚠️ CREDITS.md の表に無い（台帳漏れ） |
| `tf_p016_map.jpg` | 1920x870 | TF p16 の赤黄の点の地図だけ（y<870 で切った） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c405 | **○** | 点の数＝赤36・黄19（ss.py の定数・機械で数えた値） |
| `tf_p016_q.jpg` | 3200x378 | TF p16 の問いの帯「Why did the structure collapse … 40 years after construction was complete?」 | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）と判断。OCR に Source 行なし・第三者の印も無し | なし | c404 | **○** | 文字だけの画面（2割の枠に数える） |
| `tf_p029_model.jpg` | 3200x1570 | TF p29 建物の3D（方角・各部） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c107、c503、c604、c625 | **○** | NIST 製の3D |
| `tf_p036_punch.jpg` | 3200x1427 | TF p36 押し抜きせん断の線図（白地・英語の表題は切った） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）と判断。OCR に Source 行なし・第三者の印も無し | なし | c301、c302、c316、c336 | **○** | 機構の線図。白地の細線＝地に敷かない |
| `tf_p048_deck.jpg` | 3200x1570 | TF p48 プールデッキの3D切り欠き（K/L/M・11.1/13.1） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c116、c317 | **○** | K・L の札はファイル上端＝見出し帯に入る（台帳 G-06・A-10） |
| `tf_p050_3d.jpg` | 2016x1285 | TF p50 3週間前の3D（右上の ©2021 の門の写真は切った） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c109 | **○** | ©2021 Used with permission の部分を切ってある |
| `tf_p050_gate.jpg` | 1536x842 | TF p50 門の描き起こし（1か月前・3週間前の2段） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A。札「Source: NIST (artist rendering based on eyewitness accounts)」 | なし | pr04、c110、c113 | **○** | 目撃談にもとづく絵＝数値は「目撃談」として扱う |
| `tf_p052_3d.jpg` | 2016x1134 | TF p52 1週間前の3D（右上の ©2021 は切った） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | 未使用 | **○** | 旧版では未使用 |
| `tf_p052_gate.jpg` | 1536x853 | TF p52 門の描き起こし（3段目「Approx. 1" vertical shift after repairs.」） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A。札「NIST (artist rendering based on eyewitness accounts)」 | なし | c121、c123、c125 | **○** | 同上 |
| `tf_p057_3d.jpg` | 2016x1177 | TF p57 17時間前の3D（右上の CTS Receiver の写真は切った） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c202、c203 | **○** | — |
| `tf_p057_memo.jpg` | 1248x810 | TF p57 手書きの図と文「Morning June 23 noticed in the floor area, a space or gap of 4 inches」＋凡例 | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A。INDEX.md の書き起こし＝`Source: NIST`・`Annotations (not to scale) from an eyewitness interview.` | なし | c205、c207、c211、c212 | **○** | ⚠️ 聞き取りのときの書き込み＝「崩落前日に住民が書いた」と読ませない（旧タイトルの誤り）。1248px＝4倍の拡大でにじむ（台帳 B-08） |
| `tf_p058_3d.jpg` | 1920x1220 | TF p58 9時間前の3D | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c219 | **○** | — |
| `tf_p058_note.jpg` | 1018x583 | TF p58 付箋「Leak from the ceiling, not the pipe - 1/4 inch deep crack」＋下地の駐車場の区画図（線・柱・丸印・赤い斜線） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | 付箋＝NIST（聞き取りの注記）／下地の区画図＝**CTS Receiver（管財人）の原図** | 混在：注記は A。原図は第三者（§105 の外）＝スライドの札「Source: CTS Receiver (original drawing)」 | なし | c220、c221 | **△** | 原図が写る（台帳 B-16）＝紙面の引用（額装・無加工・出典に原図の出どころ）か、付箋だけに切り直す。1018px と小さい |
| `tf_p062_summary.jpg` | 3200x1570 | TF p62 まとめ（3週間前・1週間前の吹き出し） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c115、c117、c127 | **○** | — |
| `tf_p065_garage.jpg` | 3200x1377 | TF p65 9分前の駐車場3D（カウントダウンの帯を除く） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）と判断。OCR に Source 行なし・第三者の印も無し | なし | c229、c528 | **○** | 柱の札が見出し帯に入る（台帳 E-19） |
| `tf_p067_deflect.jpg` | 3200x1570 | TF p67 6〜7分前のたわみ（a/b/c）＋左下の断面 | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）と判断。OCR に Source 行なし・第三者の印も無し | なし | c230、c231 | **○** | — |
| `tf_p075_cover.jpg` | 3200x1570 | TF p75 かぶり「¾ in. … design drawings／2 in. cover as built」＋スラブ断面の実物写真 | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c409、c410 | **○** | 決め所の頁。インチ＝換算を添える |
| `tf_p076_bars.jpg` | 3200x1570 | TF p76 設計図の抜粋（赤枠の注記 AT LEAST 25%…）＋柱の標本写真＋本文（At this location, only 2 rather than 4…） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | 写真＝NIST／**図面＝Town of Surfside（町）の提供** | 混在：写真は A。図面は §105 の外（町の提供・図の作者は当時の設計側＝推測）＝札「Source for photographs: NIST; Source for drawing: Town of Surfside」 | なし | c420、c421、c423、c424、c428 | **△** | 紙面の引用（§2-6c の型＝頁ごと・額装・無加工・図面の出どころを出典に）。旧版は切出・色・寄りで改変し出典は「PD」だけ |
| `tf_p084_salt.jpg` | 3200x1570 | TF p84 塩水浴と電極の腐食試験（Salt-Water Bath with Electrodes） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし（推測） | c522 | **○** | 試験の方法の頁＝「海の塩が原因」の根拠にはならない |
| `tf_p086_causes.jpg` | 3200x1570 | TF p86 原因5つの箱＋左2つの波括弧（プランターは near north side of pool） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）と判断。OCR に Source 行なし・第三者の印も無し | なし | c401、c402、c432、c433、c501、c502、c507、c527 | **○** | 文字だけの画面。旧版は8カットで使用 |
| `tf_p133_plan.jpg` | 1574x1728 | TF p133 崩落範囲の平面図だけ（Zone A／Zone B。右の断面写真は出さない） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）と判断。OCR に Source 行なし・第三者の印も無し（INDEX.md の p133 は Source: NIST） | なし | c620、c621、c622、c624、c629 | **○** | 右の断面写真（室内が見える）は切ってある＝そのまま |
| `tf_p139_bars.jpg` | 3200x1570 | TF p139 下端筋が抜ける線図（柱 D・E・H・I） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c609、c610、c611、c613、c617 | **○** | 決め所の頁 |
| `tf_p174_corr.jpg` | 3200x1570 | TF p174 鉄筋の腐食（Ongoing for more than 25 years）＋腐食した鉄筋の写真 | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | なし | c511、c512、c518 | **○** | — |
| `tf_p185_87park.jpg` | 3200x1570 | TF p185 87 Park の振動の解析（地盤と建物の連成・答え3つ）＋左上の現場写真 | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）。スライドに `Source: NIST` | **作業員が立つ現場の写真**（台帳 H-11）＝公務か不明＝⑤bで原寸 | c711、c712、c713、c714、c715、c716、c718、c719 | **○** | 旧版は6カット続けて使った（c711〜c716） |
| `tf_p189_not.jpg` | 3200x1570 | TF p189「Things that did not contribute significantly to the collapse」5項目 | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）と判断。OCR に Source 行なし・第三者の印も無し | なし | 未使用 | **○** | 旧版では画像は未使用（quote と absent の札で再現）。文字だけの画面 |
| `tf_p191_closing.jpg` | 3200x1570 | TF p191 Closing Remarks（p86 と同じ5つの箱・pool deck） | TF 動画（Kaltura `1_vezbt9jw`）のコマ＝NIST 頁 | NIST | A＝米連邦 §105（NIST の職務著作）と判断。OCR に Source 行なし・第三者の印も無し | なし | ep01、ep02、ep03、ep04、ep05、ep07、ep09 | **○** | 文字だけの画面。旧版は7回使い ep01〜ep09 が文字だけ9連続 |

## §2 記録映像（クリップ）

器の大きさ＝②素材（2026-09-04）に ffprobe で測った値（`tools/footage.py` の `_SS`）。⚠️ **実効の幅は測っていない**（器の札は絵について嘘をつく＝§2-21・⑤bで使うコマごとに測る）。

| クリップ | 中身（`footage.py` の注記） | 元（Kaltura entry） | 長さ | 器の幅×高 | 1280以上 | 権利 | 旧版で使った区間（カット・秒） | 19本目 |
|---|---|---|---:|---|:-:|---|---|:-:|
| ss_b1 | 崩落現場。0:07まで題名カード／3:24以降はインタビュー。顔の寄りが多い | `1_ju6nndhb` | 250.1秒 | 1920x1014 | ○ | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | pr01 12.5（静止画）／pr02 53.8（静止画）／pr03 15.0〜18.8×0.5／c128 115.0〜118.5×0.53／c217 74.0〜77.8×0.5／c223 102.5（静止画）／c628 159.3（静止画）／c703 198.0〜203.5×0.85／c709 138.0〜143.0×0.42 | **○** 顔の寄り・重機の商標（ALPHA WRECKING・ALPI・MAXIM）・残った棟の住戸の中を避けて区間を選ぶ |
| ss_b2 | 0:08〜0:11 海岸線の空撮／0:12〜0:14 現場と 87 Park／1:39〜1:53 ドローン／1:54以降インタビュー | `1_64zdekws` | 309.7秒 | 4096x2160 | ○ | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | c106 8.0（静止画）／c119 99.0〜108.0／c204 95.8〜98.8×0.4／c434 8.0（静止画）／c505 46.0〜49.5×0.41／c726 110.0〜113.25×0.37 | **○** 1:54以降はインタビュー。区間の尻の表題カード・氏名テロップ（台帳 H-21）に注意 |
| ss_b3 | 倉庫で部材と鉄筋を測る | `1_h4yeyz2f` | 74.2秒 | 1920x1080 | ○ | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | c419 40.0〜46.0×0.6 | **○** — |
| ss_b4 | 部材の梱包・積み込み・トレーラーでの搬送 | `1_jvdq95ze` | 216.3秒 | 1920x1080 | ○ | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | c431 108.0〜118.0×0.95 | **○** 120秒からカード |
| ss_b5 | 倉庫の床一面の部材／コア抜き／コアの記録 | `1_ecar0b6h` | 333.4秒 | 3840x2160 | ○ | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | c430 102.0〜109.0×0.55／c519 39.0〜46.5×0.98／c521 11.0〜16.3×0.58 | **○** ロゴ入りヘルメットの寄りを避ける |
| ss_b6 | 圧縮試験・弾性係数試験 | `1_zdyysoml` | 263.2秒 | 3840x2160 | ○ | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | c325 47.0〜51.75×0.6／c520 116.0〜125.0×0.97 | **○** Forney の銘板（社名・電話）が写る区間に注意 |
| ss_b7 | 鉄筋の標本・引張試験機 | `1_glesd05g` | 337.0秒 | 3840x2160 | ○ | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | c326 24.0〜34.75×0.98／c513 42.0〜46.25×0.5 | **○** 36秒からカード |
| ss_b8 | 0:08まで表題カード。実物大レプリカ試験。2:08〜ワシントン大の試験 | `1_lebmphjw` | 207.0秒 | 3840x2160 | ○ | A と推定（NIST 頁の『B-roll videos (for the media)』。撮影者の記載なし） | c321 10.0〜16.75×0.6／c322 139.0〜148.25×0.9／c324 188.0〜198.0／c327 80.0〜88.0／c328 64.0〜70.0×0.8／c329 193.5〜202.5×0.98／c331 121.0〜127.75×0.92／c607 32.0〜37.75×0.64 | **△** **2:08 以降はワシントン大学の試験**（注記）＝区間ごとに場所を書き分ける。撮影者の記載なし＝大学の撮影なら §105 の外（未確認） |
| ss_tl | 6.8秒。柱まわりのスラブが割れて外れる。⚠️ 右下に NIST の透かし（x0.63〜0.95・y0.84〜0.89） | `1_gvpcaamy` | 6.8秒 | 3840x2160 | ○ | A と推定（NIST 頁の『Materials testing time-lapse videos』＝ミネソタ大学での試験。撮影者の記載なし） | c332 0.0〜6.8×0.25／c333 2.2〜6.8×0.25／c334 4.7〜6.8×0.25 | **○** 右下の NIST の透かしを切る。ミネソタ大学の試験（NIST 頁の説明）・撮影者の記載なし |
| ss_gif | 167コマ。力が柱の周りに集まり、ひびが回り込んで抜ける | https://www.nist.gov/sites/default/files/styles/2800_x_2800_limit/public/images/2026/06/22/PunchingShear_001.gif?itok=e2hzBAS5 | 167コマ（≈6.7秒） | 1920x1080 | ○ | A（頁に Credit: NIST） | c315 0.0〜6.7×0.65 | **○** 頁に Credit: NIST・図（人なし） |
| （参考）TF 動画 | 技術的知見の解説（77.3分）。スライドの出どころ。話者 Judith Mitrani-Reiser・Glenn Bell（NIST の共同責任者＝公務） | `1_vezbt9jw` | 77.3分 | 3840x2160 | ○ | A（ただし p45・p103・p119・p147 は ©2021 Used with permission、p184 は Google Earth、p50・p52 右上は ©2021、p57・p58 は CTS Receiver の写真と原図、p58 右上は Miami Dade County Open Data Hub＝出さない） | 映像としては未使用（コマだけ） | **○** スライドの頁。p88 の CONTENT WARNING（第3・4節）の範囲は絵にしない |

- 動く映像を当てたのは **30カット**（静止画で受けた6カット＝pr01 pr02 c106 c223 c434 c628 を除く）。本編で静止画に落ちたのはこの6件だけ＝取得失敗は0（06e §4 の照合）。
- **【映像あり】の条件（器の幅1280以上）は10本とも満たす**。中身は**崩落の後**の現場・倉庫・試験で、**崩落の瞬間の映像は無い**（p119 の廊下の映像は ©2021 Used with permission＝出さない）。
- NIST の頁にはほかに記者会見2本（2021・1280x720／1920x1014）・NCST Insider 14本（調査員の紹介＝顔の寄り）・タイムラプス2本目（set-up）がある＝旧版では未使用（②の実測 `事故検証-サーフサイド-素材実測の全文-20260904` §1）。

## §3 🔴 旧版の出典の書き方の誤り（権利者・根拠・場所の取り違え）

| # | どこ | 旧版の書き方 | 実際（原文） | 19本目での直し方 |
|---:|---|---|---|---|
| 1 | `tf_p076_bars.jpg`（c420 c421 c423 c424 c428） | 画面「出典：NIST 技術的知見（2026年6月22日公表） スライド76ページ／パブリックドメイン／切出」 | スライドの札「Source for photographs: NIST; **Source for drawing: Town of Surfside**」（OCR・INDEX.md）＝図面は §105 の外 | 図面の出どころを出典に出す・紙面の引用の型（額装・無加工）。旧版はデュオトーン・切り出し・寄りで改変していた |
| 2 | `tf_p058_note.jpg`（c220 c221） | 画面「出典：NIST 技術的知見（2026年6月22日公表） スライド58ページ／パブリックドメイン／切出」 | p58 の札「**Source: CTS Receiver (original drawing)**」＋「Annotations from an eyewitness interview.」＝下地の区画図は管財人の原図（台帳 B-16：写っているのは区画の線・柱・丸印・赤い斜線・付箋） | 原図の出どころを出す（紙面の引用）か、付箋だけに切り直す |
| 3 | `ref/CREDITS.md` §4本目「切り落として使わない部分」 | 「管財人（CTS Receiver）の写真と原図 … p57・p58（**手書きのメモと付箋の周りだけを切った**）」＝切ったので権利の外、と読める | p58 の付箋の切り出しに原図が残っている（#2） | 台帳を直す |
| 4 | B-Roll #8 の出典行と語り（c322 c324 c329） | 画面「出典：NIST（米国立標準技術研究所） 記録映像 B-Roll #8（実物大試験・ミネソタ大学）／パブリックドメイン」／c322 の語り「場所は、ミネソタ大学の試験場である」 | 使った区間（139〜148.25・188〜198・193.5〜202.5秒）は **128秒の表題カード「Univ. of Washington \| Laboratory Testing: Replicas of the CTS Pool-Deck Slab-Column Connections」より後**＝ワシントン大学の試験（`footage.py` の注記「2:08〜ワシントン大の試験」・台帳 C-27・`fb_c322.jpg` の OCR）＝**推測（映像は見ていない）** | 区間ごとに場所を書き分ける（NIST 頁＝「ワシントン大学とミネソタ大学で実物大の複製を作って壊した」） |
| 5 | `ref/CREDITS.md`・`tools/footage.py` の B-Roll #8 | 「ミネソタ大学。**撮影は NIST**」 | NIST 頁に撮影者の記載は無い（B-Roll は題と「for the media」だけ・写真には Credit: NIST 等がある）。§105 は連邦の職員の職務の著作だけ＝大学や請負の撮影なら別＝**未確認** | 「NIST 配布（撮影者の記載なし）」と書き、根拠は「A と推定」で残す |
| 6 | 概要欄の出典 URL | `https://www.nist.gov/disaster-failure-studies/champlain-towers-south-investigation` | 2026-10-05 に GET で **404**。正しい頁＝`https://www.nist.gov/disaster-and-failure-studies/champlain-towers-south-collapse`（200）・その `/news-and-updates`（200） | 正しい URL に |
| 7 | `ref/CREDITS.md` §4本目の「ライセンス」の1行 | 「米国政府の職務著作＝パブリックドメイン」（全部を1行で） | スライドの中に第三者の部分がある（#1・#2）・B-Roll は撮影者の記載なし（#5）＝根拠が3通りに割れる | 階層ごとに行を分ける（§2-10） |
| 8 | `tf_p016_legend.jpg`（c406） | CREDITS.md の表に**載っていない**（853bb3f で地図から切り分けた） | — | 台帳に足す |
| 9 | `fb_c713.jpg` | 台帳・USE のどこにも無いのに `ref/surfside/` に残る（⑤c H-10 で c713 を p185 に差し替えた残り） | — | 19本目で使うなら出典を書き直す |

## §4 集計

| 種類 | 点数 | ○ | △ | × |
|---|---:|---:|---:|---:|
| 技術的知見のスライド | 29 | 27 | 2 | 0 |
| 記録映像の控えの静止画 | 37 | 29 | 7 | 1 |
| 記録映像の1コマ（わざと静止画） | 2 | 1 | 1 | 0 |
| データ | 1 | 1 | 0 | 0 |
| **計** | **69** | **58** | **10** | **1** |

| 根拠 | 点数 |
|---|---:|
| A と推定（B-Roll・撮影者の記載なし） | 38 |
| A（スライドの Source: NIST／頁の Credit: NIST・GIF） | 28 |
| 混在（NIST＋第三者） | 2 |
| データ（ocr_slides.json） | 1 |
| （混在の中身）tf_p076_bars＝町の図面／tf_p058_note＝管財人の原図 | — |
| B・C・D・CC BY・CC BY-SA・報道 | 0 |

- 旧版で未使用＝`tf_p016_body.jpg`・`tf_p052_3d.jpg`・`tf_p189_not.jpg`・`fb_c713.jpg` の4点（ほか65点は1回以上）。md5 が同じ＝`fb_c106.jpg`＝`fb_c434.jpg`。
- **人の写り**（台帳の記述から）：公務（捜索隊・NIST の調査員・研究者）＝pr02・c128・c321・c328・c419・c430・c505・c607 ほか／**私企業の技術者の可能性**＝`ss_b1_sign.jpg`（ベストに DESIMONE・横顔が判別できる）／**私人の住居の中**＝`fb_c709.jpg`／不明＝⑤bで原寸＝表の「不明」の行。**私人の顔が写ると書かれた点は0**（台帳の範囲で）。血・遺体の写りの記述は0。
- **商標・連絡先の写り込み**：ALPHA WRECKING・We Break it Better・電話番号・VOLVO（pr03）／ALPI（c628）／MAXIM（c128）／Forney の銘板（c520）／WERNER・LEANSAFE（c324・c329）／CAT（c705）／DESIMONE（pr10・ep16）／NIST の透かし（c332・c333 の控え）。
- **19本目で足りないもの**（旧版の在庫の外）：崩落の前の建物の写真（Commons 2点は CC BY-SA 4.0・1280px 未満）／崩落の瞬間の映像（p119 は ©2021・隣の建物の監視カメラの映像は報道の素材＝引用の要件で検討）／FEMA（DVIDS）の現場写真28点（連邦＝A の候補）・Miami-Dade Fire Rescue の「PD」3点（**郡の機関＝§105 の外**＝根拠は Commons の印で見直す）・CC BY 2.0 1点（②の実測にあるが旧版は未使用）＝`事故検証-サーフサイド-素材実測の全文-20260904` §3〜§6。

## 関連
- `ref/ep19/old_script_inventory.md`（台本とカットの数）／`ref/ep19/old/old_tables.md`（全部の表）／`ref/CREDITS.md` §4本目／Vault `事故検証-ルール統合版-20260923` §2・§B2

