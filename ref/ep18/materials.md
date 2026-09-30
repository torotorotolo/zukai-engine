# 18本目（スレッシャー号のリメイク）素材の再点検 ── 旧版 `ref/thresher/` 73点の判定表

- 作成：2026-09-30（18本目 ①）。**判定だけ・取得はしていない**（画像を新しく落としていない）。
- 旧版＝3本目（2026-08-16 公開）。旧版の台帳＝`ref/CREDITS.md` §USS Thresher（230〜373行）。
- ⚠️ `ref/thresher/`・`ref/_thresher_raw/` は**読むだけ**。18本目で使う物は ⑤b で `ref/ep18/` へ写してから使う（旧版の記録を動かさない）。
- 物差し＝ルール統合版 §2-10（PD の根拠は A〜D を分ける）・§2-11（隠しカテゴリで読む）・§2-13（BY-SA は額装）・§B2-2（人が写る写真）・§1-8（【映像あり】は幅1280以上の動く映像）。
- 読み直しの道具（scratchpad・リポに入れない）＝Commons API（`prop=categories&clshow=hidden`）と NARA `proxy/records/search?naId=`・映像はヘッダだけ `ffprobe`。

## 1. 結論（73点）

| 束 | 点数 | 出どころ | 根拠（§2-10） | 旧版の書き方 | 18本目での扱い |
|---|---|---|---|---|---|
| `thr_t1`〜`thr_t41` | 41 | NARA 289-T（RG 289 海軍情報部）fileUnit `138924735`「Photographs Taken During the Search for the USS Thresher」 | **A**（米連邦 §105）。NARA の表示＝Use: **Unrestricted**・Access: Unrestricted（2026-09-30 実測） | 米海軍の職務著作＝PD | そのまま使える。⚠️ 41点中およそ27点に英字の説明札（旧版の実測）＝切り出しか「頁として見せる」かを ⑤b で。⚠️ `t1` 表紙・`t2` 謝辞は**文字の頁**（§5b-79 の2割に入る） |
| `thr_page24` | 1 | 同 289-T-24 の**頁全体**（黒塗りの跡を見せるため・旧版 `ccd6f8d` で起こした） | **A** | 同上 | 使える（文字の頁でなく写真の頁） |
| `thr_fig_*` | 11 | 査問会記録 第9・10次公開 PDF（`tresher9_10_reduced.pdf`）の頁の切り出し＝海図4・表2・SKYLARK の記録4＋書き込みの一角1 | **A**（米海軍の記録。FOIA で公開） | 同上 | 使える。⚠️ 表・記録の頁は**文字の頁**に数える。⚠️ 海図の白い矩形は**原本の塗り潰し**（加工ではない＝旧版で実物確認） |
| `thr_film593_a/b/c` | 3 | NARA 記録映画 `85185`「USS THRESHER (SSN-593)」のコマ（622・628・631秒） | **A**（RG 428 海軍・Moving Images Relating to Military Activities）。⚠️ NARA の表示は Use: **Undetermined**（NARA が未判定という意味＝制限ではない。作り手は海軍の写真センター 428-NPC） | PD | 使える。⚠️ 元は **720×480**＝全画面に引き伸ばすと粗い（旧版はサムネの地に使った＝`thr_film_b2`） |
| `cm_330-PSA-*` | 10 | Commons（元は National Museum of the U.S. Navy の Flickr）＝海底の残骸5・国防総省の報道発表 1964-04-28 と 1964-10-01 の紙5 | **A**（隠しカテゴリ `PD US Navy`＋`CC-PD-Mark`） | PD | 使える。⚠️ 報道発表の5点は**文字の頁** |
| `cm_USS_Thresher__SSN-593_`・`_bow`・`_bow__cropped_`・`cm_USN_1048964…`・`cm_SSN593_service_entering` | 5 | Commons（米海軍の写真 1960-07-09〜1961-08-03） | **A**（`PD US Navy`） | PD | 使える。⚠️ `cm_USN_1048964`（1960-07-09＝**進水の日**）は岸に人＝観客（私人）の顔が写るなら §B2-2 で外す＝⑤b で原寸。⚠️ `service_entering` の Commons の作者欄は「U.S. Navy Photograph courtesy of Ed Mart…」＝出典は米海軍と書き、提供者名の要否は ⑤b で |
| 🔴 `cm_anp_thresher_1963` | 1 | Commons「**Amerikaanse atoomduikboot Thesher met 129 man vermist, Bestanddeelnr 915-0380**」＝**オランダの通信社 Anefo**（オランダ国立公文書館）・1963-04-11 | 🔴 **B**（所有者の自主宣言＝**CC0**）。**米海軍ではない** | 🔴 台帳は「Public domain」、画面の出典は `scene_jiko.py:302` で `CR_USN_PD`（米海軍）＝**根拠も名前も違っていた** | 使える（CC0）。**出典は「Anefo／オランダ国立公文書館（CC0）」と書く**。旧版は直さない（公開ずみ・⑥で非公開にするだけ） |
| `nara_428-N-1057645` | 1 | NARA `175539769`（RG 428 General B&W Photographic File）艦首 | **A**（Use: Unrestricted） | PD | 使える |
| **計** | **73** | | **A 72・B 1**（C・D は0） | | 旧版の73点はすべて権利の上では使える |

- 人が写る写真（§B2-2）：負傷者・遺体の写真は0（捜索の写真は船体と残骸だけ＝「Shoe Cover」`t36`・「Correspondence Paper Debris」`t38` も人ではない）。⚠️ `t38` の紙に私信の文字が読めるなら ⑤b で原寸を見て決める。乗員（公的な任務）の顔は使ってよい。私人（観客・家族）の顔は使わない。
- BY-SA の額装（§2-13）：旧版の73点に BY-SA は0。

## 2. 【映像あり】（§1-8）＝**名乗れない**（旧版と同じ）

| naId | 尺 | 中身 | 実測（ヘッダだけ ffprobe・2026-09-30） | NARA の表示 |
|---|---|---|---|---|
| `85185` | 789.4秒 | USS THRESHER (SSN-593)（カラー・航走） | 720×480・SAR 10:11・表示 15:11・progressive | Use: Undetermined |
| `83755` | 670.2秒 | SEARCH … TRIESTE Test Dive | 720×480・同 | Undetermined |
| `83737` | 515.3秒 | SEARCH … 250 Miles East of Cape Cod | 720×480・同 | Undetermined |
| `83740` | 327.7秒 | THRESHER MEMORIAL SERVICE Portsmouth | 720×480・同 | Undetermined |
| `83750` | 281.6秒 | SEARCH FOR USS THRESHER (SSN-593) | 720×480・同 | Undetermined |
| `83213` | 189.7秒 | LAUNCHING OF USS THRESHER | 720×480・同 | Undetermined |

- 6本とも**幅720**＝「幅1280以上」に届かない（器の札は実効の画素より大きいことはあっても小さくはない＝これ以上は無い）。**動く映像としては使える**（§2-2「動いていれば効く」）が、タイトルに【映像あり】は付けない。
- 旧版の未取得14本（83741・83746・83754・83757・83758・83759・83760・83766・83767・83771・83795・84149 ほか）は ②で中身を当てる（§2-20＝名前の付いた動画は中身を見るまで記録映像ではない）。
- ⚠️ `83740` 追悼式＝家族（私人）の顔が写る＝顔の分かるショットは使わない。
- ⚠️ 旧版は `83774`（記者会見）を「人の顔が写る」で外した（08-08 の線）。**いまの線（§B2-2・09-20）は「公的な任務の人の顔は使ってよい・私人の顔は使わない」**＝海軍の会見者は使える・記者の顔は外す＝②で再審してよい。

## 3. Commons の今（Category:USS Thresher (SSN-593)・下位1段を含む・2026-09-30）

- **51点**＝Public domain 41／CC BY-SA 4.0 4／CC0 2／CC BY-SA 3.0 2／CC BY 3.0 1／CC BY 2.5 1。**旧版の調査（08-08・50点）より後に上がった点は0**（数の1点差は下位カテゴリ `John Wesley Harvey` の1点）。
- 旧版が使っていない候補（②で判定を仕上げる。どれも取得していない）：
  - `Ships searching for USS Thresher (SSN-593), 15 April 1963 (NH 97555).jpg`（738×586・PD US Navy）＝小さい＝額装
  - `USS Thresher memorial dedication at Arlington.jpg`（2019・米海軍・3551×2222）＝人が写る＝§B2-2
  - `Thresher Display.PDF`（米海軍 2013 の展示パネル・14212×12862）
  - `Public relations aspects of a major disaster- a case study of the loss of USS Thresher. (IA publicrelationsa00stie).pdf`（Stierman・PD US Government）＝**海軍の発表の遅れの研究**＝旧版の芯（情報が SKYLARK の外へ出なかった）に効く二次資料の候補
  - NH の小さい版（740px 前後）＝O-rings・brass pipe・debris・rudder sunk・sail sunk mosaic・sonar dome・surface・watertight door・stern・launching（289-T と同じ絵かは ②で画素で照合＝記憶 feedback-duplicate-art-needs-pixel-comparison）
  - BY-SA／BY（使うなら額装）＝`In Memoriam USS Thresher SSN 593, USS Scorpion SSN 589.jpg`（2019）・`Model of USS Thresher submarine in parade.jpg`（2025）・`USS Thresher memorial at US 1-ME 236 circle, April 2025.jpg`・`6707-ArlingtonCemetary…`（2点・1967）・`Thresher Commissioning Bottle.JPG`・図の gif 2点

## 4. 次（②③）へ
- 旧版の73点は**権利の上では全部使える**＝②で要るのは「場面の網」（§2-18＝権利→大きさ→撮影年→場面）と、**案C（再現イラスト）の形のもと**（PD の図だけ・§5b-78 ④）＝289-T の写真と査問会記録の図が候補。
- 写真・映像の割合（§2-1）は20%以上・上限なし＝旧版の素材だけで満たせる見込み（数は ④ の画の欄で数える）。
- 文字の頁（`t1`・`t2`・報道発表5・表と記録の頁）は §5b-79 の2割に入る＝要る所だけ。
