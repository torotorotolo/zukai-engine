# 素材の出典と権利

**この事故検証チャンネルは、権利の確実な素材だけで作る。**
米連邦機関（NTSB / FAA / NASA / NOAA / USCG）と米国国立公文書館（NARA）の著作物は
すべてパブリックドメインなので、**航空事故を題材に選べば権利問題が最初から起きない**。

権利表記は `photo_frame()` で**必ず画面に出す**。出典を出さない写真は使わない。

## アロハ航空243便（1988-04-28・N73711）

| ファイル | 出典 | 作者 | ライセンス | 用途 |
|---|---|---|---|---|
| `aloha_left.jpg` | NTSB | NTSB | Public domain | p1（掴み・機体左側面） |
| `aloha_normal.jpg` | 米国国立公文書館（NARA） | Charles O'Rear | Public domain | p2（事故前の N73711 本人） |
| `aloha_aftermath.jpg` | FAA | FAA | Public domain | 予備 |
| `ref_aloha_fuselage.png` | NTSB | NTSB | Public domain | 作図の参考 |
| `ref_aloha_after.jpg` | FAA | FAA | Public domain | 予備 |
| `ref_aloha_route.jpg` | NASA | NASA | Public domain | 予備（航路図） |

いずれも Wikimedia Commons 経由で取得し、`LicenseShortName` が
`Public domain` であることを API で機械判定して確認した（2026-07-29）。

## 作図の一次資料

| ファイル | 出典 | 使い方 |
|---|---|---|
| `b737_3view.png` | NTSB 事故調査資料（DCA21FA174）添付の 737-200 三面図 | **機体側面図の形の根拠** |

`tools/jiko_style.py` の `b737_side()` は、この三面図を画素で実測して起こした。
記憶で描くと必ず形が狂う（初稿は主翼が三角・エンジンが楕円になっていた）。
実測値は同ファイルのコメントに全部書いてある。

> 図そのものを画面に出しているわけではなく、**寸法を測って自前のベクタを描き直している**。
> 画面に出るのは `jiko_style.py` が生成した SVG だけ。

## 日本航空123便（1985-08-12・JA8119）　※本番2本目

| | |
|---|---|
| ファイル | `ref/ja123/` の **168枚**（写真124・付図38・別添1の付図4と写真2） |
| 出典 | **運輸安全委員会** 航空事故調査報告書 62-2（JA8119）日本語版 分割PDF |
| ライセンス | **公共データ利用規約 PDL1.0**（`https://jtsb.mlit.go.jp/cyo.html`）。複製・**公衆送信**・翻案を許諾。**CC BY 4.0 互換** |
| 条件 | 出典の明示（機関名＋URL）と、**加工した旨**の記載 |
| 台帳 | **`ref/ja123/INDEX.md`**（168枚すべての報告書キャプション・実寸・加工内容） |
| 取り出し | `python tools/extract_photos.py`（キャプションのテキスト層を読んで番号を付ける） |

🔴 **1本目（NTSB・パブリックドメイン）と権利の性質が違う。**
PD ではなく**条件つきの許諾**なので、**出典表記を画面から外した時点で条件違反になる**。
`scene_jiko.PHOTO_CREDIT` が全カットに出す形にしてあり、外すと机上検査で落ちる。

⚠️ 著作権法32条2項（官公庁資料の転載）は**「刊行物への転載」**の規定で、
　 YouTube は公衆送信なので**当てはまらない**。根拠は PDL1.0 に置く。

### 解説書から切り出した図と表（2026-08-04 追加・12枚）

| | |
|---|---|
| ファイル | `ref/ja123/` の `kz*.png`（図）`kh*.png`（表）`k_keiki.png` `k_camera.png` |
| 出典 | **運輸安全委員会**「日本航空123便の御巣鷹山墜落事故に係る航空事故調査報告書についての解説」（62-2 JA8119・平成23年7月） |
| ライセンス | 報告書と同じ **PDL1.0** |
| 加工 | ページを **300dpi で描画してから矩形で切った**。長辺1800px超のみ縮小。**ぼかしは掛けていない** |
| 台帳 | `ref/ja123/INDEX.md` の末尾（12枚の番号・実寸・当てたカット） |
| 取り出し | `python tools/extract_kaisetsu.py` |

🔴 **報告書とは別の文書なので、画面に出す出典も分けてある。**
`scene_jiko.kaisetsu_credit()` が `kz009.png` → 「解説書 図9」のように**名前から作る**。
混ぜると「報告書に書いてある」と「解説書に書いてある」の取り違えを画面が起こす
（台本 §2 で2件やらかしている型）。

## 未確認（使う前に必ず規約を読む）

- NHK クリエイティブ・ライブラリー（営利利用の可否）
- Pixabay / Pexels（商用可とされるが未確認）
- 自治体・官公庁の公開素材

## タイタン号（本番1本目）2026-07-30 追加

すべて **NTSB/MIR-25-36「Hull Failure and Implosion of Submersible Titan」**（2025-10-02公開）
の図版から。米連邦機関の職務上の著作物＝**パブリックドメイン**。

| ファイル | 出所 | 内容 |
|---|---|---|
| `ntsb_titan_MIR2536.pdf` | ntsb.gov | 報告書本体（87ページ・図版24点） |
| `titan_hull_edge.jpg` | 図14（下） | 円筒の中央破断面を横から。積層が刃のように裂けている |
| `titan_hull_inner.jpg` | 図13（下） | 回収された耐圧殻の内面。白い部分が繊維の破断 |
| `titan_delam_ruler.jpg` | 図18（左） | 層間剥離をインチ定規と並べた接写 |

### ⚠️ 使ってはいけない図版（報告書に載っているが権利が残る）
凡例に出所が書かれているものは、NTSB ではなく提供元の著作物。

| 図 | 出所 | 判定 |
|---|---|---|
| 図1・図2 | OceanGate | ❌ 使わない |
| 図4（下）・図8 | Garry Comber（個人） | ❌ |
| 図5・図6 | Google Maps | ❌（利用規約） |
| 図9 | A. Harvey（個人） | ❌ |
| 図11・図12 | Pelagic Research Services | ❌（海底の残骸写真。惜しいが使えない） |
| 図19・図20 | OceanGate（背景） | ❌ ただし**数値そのものは事実なので自分で作図し直せる** |
| 図23 | Marine Technology Society（背景） | ❌ |

### ✅ 出所の記載が無い＝NTSB 作成／NTSB 撮影と判断したもの
図3（三面図と内部配置）／図7（コボンド工程図＋実物断面のインセット）／
図13・14・15・16・17・18（研究室での撮影）／図21（ダイブ75と80〜83のひずみ比較）／
図22（潜水艇の製造数）／図24（捜索に参加した船と機体）

### サムネイルの地（2026-07-30 差し替え）
| ファイル | 出所 | 判定 |
|---|---|---|
| `titan_titanic_bow.jpg` | **NOAA／Institute for Exploration／ロードアイランド大学**（2004年調査・水深3,840m） | ✅ 米連邦機関の著作物＝PD。Wikimedia Commons でも Public domain。1480×1036 |

⚠️ **NOAA のサイトに載っているタイタニックの写真でも PD とは限らない。**
`oceanexplorer.noaa.gov/explorations/04titanic/` の船首写真は
**"Image copyright Emory Kristof/National Geographic"** で権利が残る。
凡例を必ず読むこと（NTSB報告書の図版と同じ落とし穴）。

### USCG が公開したタイタン号本体の写真（2026-07-30 追加）

| ファイル | 出所 | 判定 |
|---|---|---|
| `titan_rov_tailcone.jpg` (1909×1080) | **United States Coast Guard**（MBIで公開）。ROVは Pelagic Research Services 6000 | ⚠️ **PDだが撮影者は請負業者**。Wikimedia Commons は米沿岸警備隊の著作物としてPD扱い。海底に立つ尾部コーン・深度3,775.9m の焼き込みあり |
| `titan_rov_aft.jpg` (1920×1080) | 同上。後部ドームと潰れた船体の残骸 | ⚠️ 同じ留保 |
| `titan_cf_evidence.jpg` (1500×1000) | **USCG本部 Melissa Leake 准尉が撮影**。回収した炭素繊維の破片を証拠として並べたもの（2023-09-30回収） | ✅ **米沿岸警備隊職員の撮影＝完全にPD。留保なし** |

⚠️ **上2点の留保について。**
凡例は「United States Coast Guard」だが、説明文に「Image taken by Pelagic Research
Services 6000, a remotely operated vehicle」とある。**撮影機材は請負業者のROV**で、
USCG が調査の一環として公表したもの。Commons は米連邦機関の著作物としてPDと判定している。
→ **最も安全なのは `titan_cf_evidence.jpg`（USCG職員本人の撮影）。**
　 権利申し立てを1件も受けたくない段階ではこちらを使う。

### ❌ 台帳に無いまま入っていた1点（2026-07-31 追記）

| ファイル | 状態 | 判定 |
|---|---|---|
| `titan_hull_pair.jpg` (1609×1490) | サムネの「2枚並べ案」（コミット `655f550`）で取得したが、出所を記録しないままコミットされていた | ✅ **2026-07-31 に NTSB 図13 と確認できたので解禁**（下記） |

### 本編で画面に出す出典表記（`scene_jiko.CR_*`）

| ファイル | 画面に出す文字列 |
|---|---|
| `titan_hull_edge` `titan_hull_inner` `titan_delam_ruler` | 出典：NTSB（米国運輸安全委員会）／パブリックドメイン |
| `titan_rov_aft` `titan_rov_tailcone` | 出典：アメリカ沿岸警備隊／ROV撮影／パブリックドメイン |
| `titan_cf_evidence` | 出典：アメリカ沿岸警備隊／撮影 M. Leake／パブリックドメイン |
| `titan_titanic_bow` | 出典：NOAA／海洋探査研究所／ロードアイランド大学／パブリックドメイン |
| `titan_hull_pair` `titan_ntsb14〜17_*` | 出典：NTSB（米国運輸安全委員会）／パブリックドメイン |

### ★報告書の図版から取り出した標本写真（2026-07-31 追加・6枚）

**図13〜18 には出所の記載が無い＝NTSB 自身が研究室で撮影＝パブリックドメイン。**
本文の凡例で1枚ずつ確認した（OceanGate / Google Maps / Pelagic / A. Harvey の
記載がある図は1枚も含めていない）。`pypdf` で `ref/ntsb_titan_MIR2536.pdf` から
埋め込み画像を取り出し、図ごとに上下へ切り分けた。

| ファイル | 図 | 内容（報告書の凡例） | 使うカット |
|---|---|---|---|
| `titan_hull_pair.jpg` | **図13** | 回収した炭素繊維耐圧殻の**外面（上）と内面（下）** | `c308` |
| `titan_ntsb14_endface.jpg` | **図14（上）** | 機械加工した端面 | `c424` |
| `titan_ntsb15_endpiece.jpg` | **図15** | 切り落とした端材の側面 | `c422` |
| `titan_ntsb16_wrinkle.jpg` | **図16（上）** | しわの上で接着層にできた空隙 | `c411` |
| `titan_ntsb16_grind.jpg` | **図16（下）** | 外側の炭素繊維を工具で削った跡 | `c429` |
| `titan_ntsb17_layers.jpg` | **図17（上）** | 1層と2層の断面と、あいだの接着剤 | `c416` |
| `titan_ntsb17_voids.jpg` | **図17（下）** | **1層と2層のあいだの接着剤に並ぶ空隙** | `c427` |

⚠️ `titan_hull_pair.jpg` は**出所不明として使用禁止にしていたが、解禁した**。
報告書 p41 の埋め込み画像と**画素サイズが1609×1490で完全一致**し、
図13（"Recovered carbon fiber composite pressure hull outer surface and inner surface"）
であることが確認できたため。

⚠️ これらは 1431×325 のように細長い。**全画面に引き伸ばさず帯で置く**
（`cuts/__init__.py` の `PHOTO_OVERRIDE` で `band=True`）。
全画面にすると3.3倍に拡大して左右を切り落とすことになり、
「層が並んでいる」という写真の意味そのものが消える。

~~❌ 図11・図12（海底の残骸）は同じ手順で取り出せるが **Pelagic Research Services**
なので取り出したファイルごと捨てた。図1・2はOceanGate、図5・6はGoogle Maps、
図9はA. Harvey、図23はMTSなので同様に使わない。~~
→ **2026-08-01 の方針変更で撤回。下記のとおり戻した。**

---

## 2026-08-02 追加：PD限定をやめたので戻した図（`tools/extract_figs.py`）

**2026-08-01 にカズヤくんの指示で「素材はパブリックドメインだけ」の縛りを外した。**
ところが**解禁したまま、上で捨てた素材を戻していなかった**ので、実写の比率は
12.0% → 12.7% までしか動いていなかった。ここで戻して **14.8%（34/229）** にした。

🔴 **図18は出所の記載が無い＝NTSB作成＝PDで、従来の縛りでも使えたはずの取りこぼし。**
（図13〜18をPDと判定したときに、図18だけ拾い忘れていた。）
図7・図22も同じくPDだが、英字と細い凡例が多く 1920×1080 では読めないので
**採らなかった＝権利ではなく可読性の理由**。

| ファイル | 図 | 内容 | 出所 | 使うカット |
|---|---|---|---|---|
| `titan_f18_delam.png` | **図18** | 1号殻の端材に出た中心線の剥離 | 記載なし＝**PD** | `c324`（地） |
| `titan_f01_descend.jpg` | 図1 | 降下していくタイタン | オーシャンゲート | `c110`（地） |
| `titan_f04_lars.png` | 図4 | LARS に載ったタイタン（上から） | G. Comber | `c605`（地） |
| `titan_f08_launch.png` | 図8 | 船尾のランプから降ろす | G. Comber | `c109`（地） |
| `titan_f09_parking.png` | 図9 | セントジョンズの駐車場（屋外保管） | A. Harvey | `c602`（地） |
| `titan_f10_mishap.png` | 図10 | 2023年の遠征で起きた不具合 | S. Taragel | `c607`（地） |
| `titan_f11_wreck.png` | **図11** | **発見時**の残骸（焼き込み 06-22-2023） | Pelagic | `c132` |
| `titan_f12_wreck.png` | 図12 | 海底の残骸（破片A〜D） | Pelagic | 未使用 |
| `titan_f02_cylinder.png` | 図2 | 円筒とチタン端部の線画 | オーシャンゲート | 未使用（白地の線画で様式に合わない） |
| `titan_f07_cobond.png` | 図7 | コボンド工程の図解 | 記載なし＝PD | 未使用（英字が細かく読めない） |
| `titan_f22_production.png` | 図22 | 潜水艇の生産数 | 記載なし＝PD | 未使用（英字のグラフ） |
| `titan_f23_population.png` | 図23 | 有人潜水艇の数の推移 | MTS | 未使用（英字のグラフ） |

⚠️ 権利の留保が付くもの（Pelagic ／ オーシャンゲート ／ G. Comber ／ A. Harvey ／
S. Taragel）は、**申し立てを受けうる種類**であることを承知のうえで使っている
（2026-08-01 カズヤくん判断）。出典表記は画面の右上に必ず出る。

---

## 日航123便 第6章（噂の検証）で当たった文献

画像としては使っていない。**画面に出す事実の裏取りに使った文献**なので、
原本を `C:\Users\konar\Desktop\ja123_src\c6\` に保存してある（HTMLと抽出テキスト）。

| 保存名 | 文献 | 当てたカット | この文献から取った事実 |
|---|---|---|---|
| `qiita_tron.html/.txt` | 中島 浩一「『TRON(トロン)開発者が日航123便の墜落で死亡』デマの真実」Qiita、2025-08-10 | `c609`〜`c613` | 松下グループ17人の**所属の全一覧**（中央研究所の所属は0人／システムエンジニアリング本部3・ビデオ事業部2・ゼネラルオーディオ事業部2・電化調理事業部3 ほか）／開発の場所は大阪の中央研究所、システムエンジニアリング本部は東京／1985年時点は初期の研究開発段階で動くOSは無い／実験機1987年／一般発売1991年 |
| `jfc_cvr.html/.txt` | 日本ファクトチェックセンター「日航123便墜落事故で機長が『被弾したぞ』と発言? 記録も音声も根拠もなし」2025年8月 | `c614`〜`c619` | 判定は**根拠不明**／投稿の表示回数**601万回超**（8/18時点）／動画の再生**48万回以上**（同）／音の無いところに赤い字幕が足されている／動画の冒頭が「これが全文」「出回っているものはまがい物」と名乗っている |

🔴 **2026-08-05 にこの2本を取り寄せて照合し、5件を直した。**
　 それまで副題は「検証記事」「ファクトチェック」とだけ書いてあり、**どの文献か画面から
　 たどれなかった**。裏取りのできない状態で断定を出していたことになるので、
　 出典表記も記事名と年月まで出すように変えた。
⚠️ `c619` の旧「取材に対し、放送局は偽の動画であると答えている」は、
　 **どちらの文献にも、周辺の報道にも見当たらなかった**ので差し替えた。

## USS Thresher (SSN-593)（1963-04-10・3本目）

**権利：すべて米海軍の職務著作＝パブリックドメイン。**
根拠＝NARA「Works of the U.S. Government … are in the public domain」
<https://www.archives.gov/global-pages/privacy.html>
→ **継承義務も Content ID リスクも無い。切って寄せてよい。**

### ① NARA 289-T アルバム（RG 289 Records of the Naval Intelligence Command）

fileUnit `138924735`「Photographs Taken During the Search for the USS Thresher」
（1964年9月に海軍が編纂／TRIESTE・曳航カメラ NRL/MIZAR が撮影）。
取得＝`https://catalog.archives.gov/proxy/records/search?ancestorNaId=138924735`
（🔴 公式 `api/v2` はHTMLを返すので使えない）。

原本は 5831〜6879px・8bitグレー・41点350MB。**原本は `ref/_thresher_raw/`（git 管理外）**、
commit するのは写真部分を切り出した 2400px 版のみ。

| ファイル | 原本 | 出典番号 | 中身 |
|---|---|---|---|
| `thr_t1.jpg` | 5831x3659 | 289-T-1 | USS Thresher (SSN-593) 1963-1964 Search Photography Cover |
| `thr_t2.jpg` | 5850x3555 | 289-T-2 | Acknowledgment Page |
| `thr_t3.jpg` | 5850x3555 | 289-T-3 | Photograph of the Bow Outer Hull Section |
| `thr_t4.jpg` | 5850x3555 | 289-T-4 | Photograph of Bow Outer Hull Aft of Sonar Dome |
| `thr_t5.jpg` | 5850x3555 | 289-T-5 | Photograph of Bow Plating |
| `thr_t6.jpg` | 5850x3640 | 289-T-6 | Photograph of Steel Webbing Supports |
| `thr_t7.jpg` | 5850x3640 | 289-T-7 | Photograph of Bow Outer Hull Plating |
| `thr_t8.jpg` | 5850x3688 | 289-T-8 | Photograph of Torn Bow Section |
| `thr_t9.jpg` | 5850x3688 | 289-T-9 | Photograph of Bow Section Seen from Aft |
| `thr_t10.jpg` | 5850x3688 | 289-T-10 | Photograph of Pressure Hull Portion |
| `thr_t11.jpg` | 5850x3688 | 289-T-11 | Photograph of Outer Hull, Right Hand Portion |
| `thr_t12.jpg` | 5850x3688 | 289-T-12 | Photograph of Light Debris |
| `thr_t13.jpg` | 5917x3745 | 289-T-13 | Photograph of Miscellaneous Debris |
| `thr_t14.jpg` | 5917x3745 | 289-T-14 | Shipyard Photograph |
| `thr_t15.jpg` | 5917x3745 | 289-T-15 | Photograph of Run #0029-C, Closeup |
| `thr_t16.jpg` | 5917x3745 | 289-T-16 | Photograph of Sail, Starboard Side |
| `thr_t17.jpg` | 6879x4879 | 289-T-17 | Mosaic of the Sail |
| `thr_t18.jpg` | 6879x4879 | 289-T-18 | Photograph of Air Bottle, Torpedo Shutter Door, and Sail, Upper Portion |
| `thr_t19.jpg` | 6879x4879 | 289-T-19 | Photograph of the Outer Hull |
| `thr_t20.jpg` | 6879x4879 | 289-T-20 | Photograph of the Bridge Access Trunk and ECM Mast |
| `thr_t21.jpg` | 6879x4879 | 289-T-21 | Photograph of the Diesel Exhaust Line |
| `thr_t22.jpg` | 5860x3726 | 289-T-22 | Shipyard Photograph |
| `thr_t23.jpg` | 5860x3726 | 289-T-23 | Mosaic Photograph of the Tail Section |
| `thr_t24.jpg` | 5860x3774 | 289-T-24 | Photograph of Draft Markers on Topside Rudder |
| `thr_t25.jpg` | 5860x3774 | 289-T-25 | Photograph of Port Stern Plane PUFFS Hydrophone |
| `thr_t26.jpg` | 5860x3774 | 289-T-26 | Photograph of Starboard Stern Plane PUFFS Hydrophone. |
| `thr_t27.jpg` | 5860x3774 | 289-T-27 | Photograph of Tail Section, Top View |
| `thr_t28.jpg` | 5860x3736 | 289-T-28 | Photograph of the Anchor |
| `thr_t29.jpg` | 5860x3736 | 289-T-29 | Photograph of Break at Frame 78, with Outer Hull |
| `thr_t30.jpg` | 5860x3736 | 289-T-30 | Photograph of Break at Frame 78, Top View |
| `thr_t31.jpg` | 5860x3802 | 289-T-31 | Photograph of Messenger Buoy Cable, Line Locker, and Escape Trunk Hatch |
| `thr_t32.jpg` | 5860x3679 | 289-T-32 | Photograph of Line Locker, Messenger Buoy Cable Reel Recess, Hand Recesses, Salvage Air Fi |
| `thr_t33.jpg` | 5860x3717 | 289-T-33 | Mosaic Photograph of the Outer Hull, Aft. |
| `thr_t34.jpg` | 5908x3755 | 289-T-34 | Photograph of Stern Chock Section, Top View |
| `thr_t35.jpg` | 5908x3698 | 289-T-35 | Photograph of Light Debris |
| `thr_t36.jpg` | 5860x3698 | 289-T-36 | Photograph of Shoe Cover |
| `thr_t37.jpg` | 5860x3698 | 289-T-37 | Photograph of Air Bottle |
| `thr_t38.jpg` | 5860x3774 | 289-T-38 | Photograph of Correspondence Paper Debris |
| `thr_t39.jpg` | 5860x3631 | 289-T-39 | Photograph of Outer Hull Plating |
| `thr_t40.jpg` | 5860x3631 | 289-T-40 | Photograph of Debris, Ladder |
| `thr_t41.jpg` | 5860x3631 | 289-T-41 | TRIESTE II Tracks |

⚠️ **ページには英字の説明札が貼ってあり、機械の切り出しでは 41点中およそ27点で残っている。**
　 全画面で使うカットは `scene_jiko.TRIM_BY_PHOTO` に**ファイル単位で手で**入れる。
⚠️ 左上と右下の黒帯は**機密指定印を手で塗り潰したもの**（切り出しでほぼ落ちている）。

### ② Wikimedia Commons（PD / CC0 のみ）

⚠️ カテゴリ50点の内訳は PD 40／CC BY-SA 4.0 4／CC0 2／CC BY-SA 3.0 2／CC BY 3.0 1／CC BY 2.5 1。
**CC BY-SA は継承が生じるので落としていない。**
⚠️ **原寸URLは 429 を返す。** API に `iiurlwidth` を渡して `thumburl` をもらうと通る
（勝手な幅の `/thumb/.../NNNpx-` は 400「Use thumbnail sizes listed on ...」で弾かれる）。
そのため 1920px 幅のものが混ざっている（本編は1920x1080なので実害なし）。
⚠️ 同じ絵の PNG/JPG 重複2組と、URLのクエリが名前に混ざった1点は削除ずみ（32bit指紋で検出）。

| ファイル | 実測 | ライセンス | 中身 |
|---|---|---|---|
| `cm_330-PSA-110-63__USN_711302___22171571340_.jpg` | 2160x1736 | Public domain | 海底の残骸（セピア調）。**289-T アルバムとは別の色味** |
| `cm_330-PSA-110-63__USN_711303___22172737989_.jpg` | 1920x1555 | Public domain | 海底の残骸（セピア調） |
| `cm_330-PSA-110-63__USN_711304___22333570016_.jpg` | 1920x1577 | Public domain | 海底の残骸（セピア調） |
| `cm_330-PSA-191-63__USN_711349___22333493576_.jpg` | 1920x1493 | Public domain | 粗い探査画像（青みがかった走査像） |
| `cm_330-PSA-191-65__USN_711345___22172639369_.jpg` | 1920x1503 | Public domain | ねじれた金属の高コントラスト写真 |
| `cm_330-PSA-309-64a__22791587391_.jpg` | 2396x3237 | Public domain | 🔴 **国防総省 NEWS RELEASE 1964-10-01「NAVY CONCLUDES RESEARCH OPERATIONS IN THRESHER SEARCH AREA」**（DoD の紋章つき・タイプ打ち原文） |
| `cm_330-PSA-309-64b__22766848982_.jpg` | 1920x2634 | Public domain | 同 2ページ目（TRIESTE II の運用・捜索の記述） |
| `cm_330-PSA-309-64c__22159229233_.jpg` | 1920x2063 | Public domain | 同 3ページ目（END まで） |
| `cm_330-PSA-99-64a__22356922549_.jpg` | 2272x3092 | Public domain | 🔴 **国防総省 NEWS RELEASE 1964-04-28「NAVY RELEASES REPORT OF ITS DEEP SUBMERGENCE SYSTEMS REVIEW GROUP」** |
| `cm_330-PSA-99-64b__22355788950_.jpg` | 1920x2613 | Public domain | 同 2ページ目（審査グループの構成員一覧） |
| `cm_SSN593_service_entering.jpg` | 1750x1211 | Public domain | 岸壁のスレッシャー。セイルの593と乗員が写る |
| `cm_USN_1048964_USS_Thresher__SSN-593_.jpg` | 5706x4554 | Public domain | ⭐造船所のスレッシャー。**艦首のソナードームと建造中の船体**・岸に人 |
| `cm_USS_Thresher__SSN-593_.jpg` | 5677x4441 | Public domain | ⭐**いちばん有名な航走中の写真**（競合17本の大半が使っている絵） |
| `cm_USS_Thresher__SSN-593__bow.jpg` | 4918x6136 | Public domain | ⭐**正面から見た艦首**。競合が使っていない構図 |
| `cm_USS_Thresher__SSN-593__bow__cropped_.jpg` | 1920x2429 | Public domain | 同・切り抜き版 |
| `cm_anp_thresher_1963.jpg` | 4095x3304 | Public domain | 1963年の報道写真（プリントを台紙に留めた状態で撮ったもの） |

### ②b NARA 静止画（General B&W Photographic File）

| ファイル | 実測 | 出典 | 中身 |
|---|---|---|---|
| `nara_428-N-1057645.jpg` | 2301x2850 RGB | NARA `175539769`（428-N-1057645） | Bow View of the Nuclear-Powered Attack Submarine USS Thresher。**PD** |

### ③ 査問会記録（Court of Inquiry・2020〜2021年に機密解除）

| 資料 | URL | 中身 |
|---|---|---|
| Volume I（300ページ・87.3MB） | `https://assets.documentcloud.org/documents/7216658/Ocr-THRESHER-Pg-1-300.pdf` | 本文741,536文字。Findings of Fact はPDF 34〜56ページ |
| 第9・10次公開（600ページ・41.0MB） | `https://s3.documentcloud.org/documents/20986255/tresher9_10_reduced.pdf` | 本文632,904文字。海図・緊急浮上試験のデータ表・SKYLARK の記録 |

⚠️ `curl -sL -o` は0バイトで落ちる。`--fail --retry 3 -A "Mozilla/5.0" -e "https://www.documentcloud.org/"` で取る。
**PDFは `ref/_thresher_raw/` に置く（git 管理外）。**

取り出した図版（`tools` 相当の処理は `scratchpad/pdf_figs.py` + `pick_figs.py`）：

| ファイル | 元 | 実測 | 中身 |
|---|---|---|---|
| `thr_fig_chart_exhibit50.jpg` | 第9・10次 PDF 131ページ | 2600x1864（原 7808x5600） | 捜索海図（EXHIBIT 50・線画・航跡と爆発位置） |
| `thr_fig_chart_redact_a.jpg` | 第9・10次 PDF 132ページ | 2600x1835（原 3964x2799） | 捜索海図（鉛筆の航跡・白い塗り潰し 173x120px） |
| `thr_fig_chart_redact_b.jpg` | 第9・10次 PDF 135ページ | 2600x1824（原 3988x2799） | 捜索海図（鉛筆の航跡・白い塗り潰し 367x236px） |
| `thr_fig_chart_c.jpg` | 第9・10次 PDF 133ページ | 2600x1834（原 3966x2799） | 捜索海図（同系・別葉） |
| `thr_fig_table_thresher.jpg` | 第9・10次 PDF 490ページ | 2600x1615（原 4224x2624） | TABLE I 緊急浮上試験の実測（THRESHER SSN-593） |
| `thr_fig_table_permit.jpg` | 第9・10次 PDF 491ページ | 2600x1615（原 4224x2624） | TABLE 2 同（PERMIT SSN-594） |
| `thr_fig_log_cover.jpg` | 第9・10次 PDF 119ページ | 1540x2600（原 2560x4320） | SKYLARK 報告 表紙（ORIGINAL 印） |
| `thr_fig_log_p1.jpg` | 第9・10次 PDF 120ページ | 1540x2600（原 2560x4320） | SKYLARK 経過記録 1 |
| `thr_fig_log_p2.jpg` | 第9・10次 PDF 121ページ | 1540x2600（原 2560x4320） | SKYLARK 経過記録 2 |
| `thr_fig_log_p3.jpg` | 第9・10次 PDF 122ページ | 1540x2600（原 2560x4320） | SKYLARK 経過記録 3（0900〜0917R） |

🔴 `thr_fig_chart_redact_a/b.jpg` の**白い矩形は塗り潰し**（実物で確認）。
　 紙の明るさ 185〜187 に対して 255 の純白が乗っている。**加工ではない。**

### ④ NARA 記録映画（すべてPD・**720x480 の4:3**）

動画はリポジトリに入れない（`tools/footage.py` の約束どおり URL から落とす）。

| naId | 尺 | 中身 |
|---|---|---|
| `85185` | 789秒 | USS THRESHER (SSN-593) |
| `83755` | 670秒 | SEARCH FOR USS THRESHER (SSN-593) TRIESTE Test Dive |
| `83737` | 515秒 | SEARCH FOR USS THRESHER (SSN-593) 250 Miles East of Cape Cod over Atlantic |
| `83740` | 328秒 | THRESHER MEMORIAL SERVICE Portsmouth, N. H |
| `83750` | 282秒 | SEARCH FOR USS THRESHER (SSN-593) |
| `83213` | 190秒 | LAUNCHING OF USS THRESHER (SSN-593) Naval Shipyard, Portsmouth |

ほかに未取得14本（83741 / 83746 / 83754 / 83757 / 83758 / 83759 / 83760 /
83766 / 83767 / 83771 / 83795 / 84149 ほか）。計20本・2,328MB。
🔴 **83774（記者会見）は使わない**（人の顔が写る記者会見は使わない、というルール）。

## 4本目：サーフサイド（Champlain Towers South・2021-06-24）　※2026-09-05

| | |
|---|---|
| 出どころ | **NIST（米国立標準技術研究所）** の Champlain Towers South 調査ページ `news-and-updates` |
| ライセンス | 米国政府の職務著作＝**パブリックドメイン**。B-Roll は "for the media" として配布 |
| 置き場所 | `ref/surfside/`（gitignore は `!ref/surfside/` で許可。4K の原コマは `analytics/` に置きリポには入れない） |
| 画面の出典表記 | `scene_jiko.surfside_credit()` が名前から機械的に作る。動画のカットは `footage.credit_of()` |

### ① 技術的知見（Technical Findings・2026-06-22 公表）のスライド＝`tf_pNNN_*.jpg`

77.3分・3840x2160 の解説動画（Kaltura `1_vezbt9jw`）から**1コマずつ範囲取得で抜き**、
上の見出し帯（NIST ロゴと英語の表題・上 12.8%）を切り落として 3200px に縮めたもの。
ページ番号はコマの右下の数字。抜いた秒は `analytics/materials/surfside/tf_frames/INDEX.md`。

🔴 **切り落として使わない部分**（権利が NIST に無い）：
- `©2021 Used with permission` の写真 … p45・p103・p119・p147（スライドごと使わない）、**p50・p52 の右上**（門の実写）
- Google Earth／ストリートビュー … p184（スライドごと使わない。9フィートは自作図）
- 管財人（CTS Receiver）の写真と原図 … p57・p58（**手書きのメモと付箋の周りだけ**を切った）
- Miami Dade County Open Data Hub の航空写真 … p58 右上

| ファイル | 頁 | 切り出し | 中身 |
|---|---:|---|---|
| `tf_p003_model.jpg` | 3 | 見出し帯を除く全体 | 建物の3Dモデル＋寸法 |
| `tf_p016_q.jpg` `tf_p016_body.jpg` `tf_p016_map.jpg` | 16 | 問いの帯／本文／赤黄の点の地図 | NIST の問いと「余裕は決定的に小さかった」 |
| `tf_p029_model.jpg` | 29 | 全体 | 3D（西＝解体／中央・東＝崩落、プールデッキ、街路駐車場） |
| `tf_p036_punch.jpg` | 36 | 英語の表題を除く線図 | パンチング・シアの線図 |
| `tf_p048_deck.jpg` | 48 | 全体 | プールデッキの3D切り欠き（K/L/M・11.1/13.1） |
| `tf_p050_3d.jpg` `tf_p050_gate.jpg` | 50 | 左の3D／右下の描き起こし（右上の ©2021 は切った） | 3週間前 |
| `tf_p052_3d.jpg` `tf_p052_gate.jpg` | 52 | 同上 | 1週間前 |
| `tf_p057_3d.jpg` `tf_p057_memo.jpg` | 57 | 左の3D／右下の手書きメモ（右上の写真は切った） | 17時間前 |
| `tf_p058_3d.jpg` `tf_p058_note.jpg` | 58 | 左の3D／付箋の周り（航空写真は切った） | 9時間前 |
| `tf_p062_summary.jpg` | 62 | 全体 | まとめ（3週間前・1週間前の吹き出し） |
| `tf_p065_garage.jpg` | 65 | カウントダウンの帯を除く | 9分前の駐車場3D |
| `tf_p067_deflect.jpg` | 67 | 全体 | 6〜7分前のたわみ（a/b/c） |
| `tf_p075_cover.jpg` | 75 | 全体 | かぶり ¾インチ／2インチ（決め所） |
| `tf_p076_bars.jpg` | 76 | 全体 | 上端筋 4本→2本（図面は Town of Surfside 提供と明記） |
| `tf_p084_salt.jpg` | 84 | 全体 | 塩水浴と電極の試験 |
| `tf_p086_causes.jpg` | 86 | 全体 | 原因5点の箱と波括弧 |
| `tf_p133_plan.jpg` | 133 | **左の平面図だけ**（右の断面写真は出さない） | 崩落範囲（Zone A/B） |
| `tf_p139_bars.jpg` | 139 | 全体 | 下端筋が抜ける線図（決め所） |
| `tf_p174_corr.jpg` | 174 | 全体 | 鉄筋の腐食（25年以上） |
| `tf_p185_87park.jpg` | 185 | 全体 | 87パークの振動の解析 |
| `tf_p189_not.jpg` | 189 | 全体 | そうではなかったもの（5項目） |
| `tf_p191_closing.jpg` | 191 | 全体 | Closing Remarks |

### ② 記録映像（B-Roll・タイムラプス・GIF）＝動画はリポジトリに入れない

`tools/footage.py` が**使う区間だけ**を Kaltura の実ファイルから範囲取得で切り出す（落とさない）。
ひかえの静止画 `fb_<cid>.jpg`（動画が取れないときだけ出る）と、わざと静止画で使う
`ss_b1_sign.jpg`（銘板・B-Roll #1 の 9秒）`ss_b2_87park.jpg`（87 Park の空撮・B-Roll #2 の 13秒）を置く。

| clip | Kaltura entry | 尺 | 解像度 | 中身 |
|---|---|---:|---|---|
| ss_b1 | `1_ju6nndhb` | 250秒 | 1920x1014 | 崩落現場（銘板・瓦礫・残った棟の断面） |
| ss_b2 | `1_64zdekws` | 310秒 | 4096x2160 | 海岸線の空撮・ドローン・現場 |
| ss_b3 | `1_h4yeyz2f` | 74秒 | 1920x1080 | 証拠倉庫 |
| ss_b4 | `1_jvdq95ze` | 216秒 | 1920x1080 | 部材の梱包・搬送 |
| ss_b5 | `1_ecar0b6h` | 333秒 | 3840x2160 | コア抜き・倉庫 |
| ss_b6 | `1_zdyysoml` | 263秒 | 3840x2160 | コアの圧縮試験 |
| ss_b7 | `1_glesd05g` | 337秒 | 3840x2160 | 鉄筋の試験 |
| ss_b8 | `1_lebmphjw` | 207秒 | 3840x2160 | 実物大レプリカ試験（ミネソタ大学。撮影は NIST） |
| ss_tl | `1_gvpcaamy` | 6.8秒 | 3840x2160 | 材料試験タイムラプス（右下に NIST の透かし＝切り方で外す） |
| ss_gif | `PunchingShear_001.gif` | 167コマ | 1920x1080 | 押し抜きせん断の動く図（NIST ニュース 2026-06-22） |

⚠️ 使わないと決めたもの：顔の寄り・NIST ロゴ入りヘルメットの寄り・各巻のインタビュー帯（#1 3:24〜、#2 1:54〜）・
表題カード（各巻の先頭 7〜8秒、#8 の 2:08〜2:12）。

---

## 5本目：SL-1 原子炉暴走事故（1961-01-03・米アイダホ州）　※2026-09-07（②素材）

| | |
|---|---|
| 出どころ | **NARA（米国立公文書館）の記録映画2本**／**Wikimedia Commons `Category:SL-1 Reactor` 59点**／**一次資料 IDO-19302**（OSTI） |
| ライセンス | すべて**合衆国政府の職務著作＝パブリックドメイン**（17 U.S.C. §105）。Commons の内訳は `PD-USGov-NPS` 43・`PD-USGov` 6・`PD-USGov-DOE` 4・`PD-USGov-Military-Army` 1 |
| 置き場所 | 記録映画＝**リポに入れない**（URL から範囲取得）／`ref/sl1/shots.json`（ショットの実測）・`ref/sl1/materials.json`（写真の実測）はリポに入れる／`ref/sl1/IDO-19302.pdf`（17MB）は gitignore |
| 実測の道具 | `tools/shots.py`（ショットの境目・1秒刻み）／`tools/src_probe.py`（全画面に出せるか）／`tools/footage.py --selftest` |

### ① 🔴 記録映画2本（NARA・RG 330／DIMOC）＝**権利の結論：使える**

| naId | 題 | 尺 | 解像度 | ショット | URL |
|---|---|---|---|---:|---|
| `174689848` | SL-1 Accident Phase I & II | 24分55秒（1,494.71秒） | 1920x1080 / 24fps | **139** | `https://catalog.archives.gov/medialz/mopix/330/DIMOC/330-dimoc-redstone1860.mp4`（447.8MB） |
| `174689849` | SL-1 Accident Phase III | 30分48秒（1,847.50秒） | 1920x1080 / 24fps | **271** | `https://catalog.archives.gov/medialz/mopix/330/DIMOC/330-dimoc-redstone1861.mp4`（553.4MB） |

**NARA の札：`accessRestriction = Unrestricted` ／ `useRestriction = Restricted - Possibly（Copyright）`。**
①題材のチャットでは「3本目スレッシャー（`Undetermined`）より重い」と見て②の宿題にしていた。
**②で当たった結果、この札は個別の判断ではなくシリーズ一括の定型文だった。**

**札が一括である根拠（実測）**
1. シリーズ本体 `88680113`（Moving Images Related to Combat Visual Information）**そのものが同じ注記**を持つ
2. 同シリーズの兄弟レコードを標本で数えたら **299件が 299/299 で同じ札**（0件の例外）
3. NARA の SL-1 の3件目 `66396247`（**RG 434 エネルギー省**・未デジタル化）にも同じ札が付く。
   DOE の記録が連邦の職務著作でないはずがないので、**札は作者の判断を表していない**

**PD である根拠（実測）**
1. `contributors` の Originator ＝ **Department of Defense / Department of the Army**（連邦機関）
2. `scopeAndContentNote` ＝「**The U.S. Atomic Energy Commission** reports on phases 1 and 2 of the … SL-1 accident recovery efforts」＝ AEC（米原子力委員会）の制作
3. 同じ AEC アイダホ支所のブリーフィング映画を **DOE/OSTI 自身が公開**している（OSTI ID `1122857`）。
   Internet Archive の Prelinger 版は `creator = U.S. Atomic Energy Commission, Idaho Operations Office`。
   Commons にも `"Nuclear Power Reactor - The SL-1 Accident Video- Briefing Film Report" (1961).webm` が PD で上がっている
4. 合衆国法典 **17編105条**により、合衆国政府の職務著作には著作権が発生しない

⚠️ **残る危険＝映画の中に第三者の映像（ニュース映画・音楽）が混ざっている可能性。**
札が一括であることは「中身に第三者の素材が無い」ことまでは証明しない。
→ ⑤b でショットを選ぶとき、**局のロゴ・クレジット・見慣れた報道映像**が無いかを見る。

⭐ **落とさずに使える。** `Range: bytes=0-1023` に **206** を返し、`ffprobe <URL>` がそのまま通る
（4本目の Kaltura と同じやり方。署名も期限も無いので URL は固定でよい）。

#### ショットの境目（`ref/sl1/shots.json`・`tools/shots.py` で1秒刻みに実測）

| | Phase I & II | Phase III |
|---|---:|---:|
| ショット数 | **139** | **271** |
| 長さ 中央値 | 7秒 | 5秒 |
| 6秒以上 | 85本（21.8分） | 110本（21.4分） |
| 8秒以上 | 68本（20.0分） | 63本（16.3分） |
| ほぼ静止（`motion<2.0`）＝`still=True` 向き | 35本 | 35本 |

🔴 **ffmpeg の scene 検出だけでは足りない。**
`select=gt(scene,0.18)` は**ハードな切り替えしか見ず、ディゾルブ（重ね消し）を見ない**。
それだけだと 77本／165本しか出ず、**1本のショットが 333秒**という嘘が出た。
1秒ごとの見た目の署名で採り直して 139本／271本＝**168本を見落としていた**。
→ 秒は必ず `ref/sl1/shots.json` から採る。`footage.py` の `outside_shot()` がまたぎを exit 3 で止める。

### ② Wikimedia Commons `Category:SL-1 Reactor`（59点・**全部 PD**）

🔴 **①題材のチャットの「全画面8点」は誤り。実測すると 39点。**
題名（"floor plan" / "Interior view"）では連続階調か線図かは決まらないので、
`tools/src_probe.py` で**インク率**（明度200未満の画素の割合）を測って分けた。
図面 0.12〜0.35／写真 0.49〜1.00 で**間に1点も無く**、59点すべてで題名と一致した（しきい値 0.42）。

⚠️ **44点は HAER ID-33**（Historic American Engineering Record・米国の産業遺産の記録）。
`loc.gov/pictures` は UA と Referer を足しても 403 のままだが、**当たる必要が無かった**＝
Commons 側が原本の TIFF（`lcweb2.loc.gov/pnp/habshaer/id/id0400/id0410/photos/…`）から
5300x4300 で上げ直しており、LoC に取りに行っても同じ絵になる。

⚠️ **「HAER ＝ 1968年以降に編纂」だが、中身は当時の写真を含む。**
HAER の記録には INEEL（アイダホ国立工学環境研究所）が撮った 1957〜1961年の写真が複写されている。
**当時（〜1961）24点／1968年以降の記録 15点**に分けた（下の表）。

#### 当時の写真（1957〜1961）＝事故の本筋に使える
| 年 | 寸法 | ink | HAER 番号 | 中身 |
|---:|---|---:|---|---|
| 1957 | 5319x4325 | 0.60 | HAER ID-33-D-51 | ARA-II. Camera looking southeast at foundation piers for SL-1 reactor building |
| 1957 | 5344x4365 | 0.56 | HAER ID-33-D-71 | ARA-II. Construction progress at SL-1 site near end of 1957. Buildings from ri |
| 1957 | 5289x4320 | 0.51 | HAER ID-33-D-53 | ARA-II. Steel shell for SL-1 reactor building goes up above supports. Septembe |
| 1957 | 5325x4269 | 0.71 | HAER ID-33-D-54 | ARA-II. Structural steel framing for bottom SL-1 reactor building. October 16, |
| 1957 | 4283x5314 | 0.54 | HAER ID-33-D-57 | ARA-II. Looking northwest at SL-1 reactor building during hoisting of turbine- |
| 1957 | 5335x4279 | 0.70 | HAER ID-33-D-52 | ARA-II. Support piers for SL-1 reactor building. September 5, 1957. Ineel phot |
| 1957 | 5284x4320 | 0.61 | HAER ID-33-D-55 | ARA-II. Looking down into SL-1 reactor building showing placement of four-inch |
| 1957 | 4258x5345 | 0.68 | HAER ID-33-D-56 | ARA-II. View inside reactor building looking at SL-1 reactor vessel. November  |
| 1957 | 5314x4283 | 0.77 | HAER ID-33-D-58 | ARA-II. Looking south, SL-1 reactor building operating floor with reactor pres |
| 1957 | 5289x4294 | 0.63 | HAER ID-33-D-70 | ARA-II. Support facilities building (ARA-602) goes up next to SL-1 reactor bui |
| 1958 | 4283x5309 | 0.65 | HAER ID-33-D-67 | ARA-II. Exterior view of enclosed stairway leading from SL-1 support building  |
| 1958 | 5263x4304 | 0.78 | HAER ID-33-D-69 | ARA-II. Aligning the turbo generator on the operating floor of SL-1. June 24,  |
| 1958 | 5299x4325 | 0.75 | HAER ID-33-D-73 | ARA-II. Aerial view of SL-1 site in May 1958 when construction was nearly comp |
| 1958 | 5299x4294 | 0.68 | HAER ID-33-D-61 | ARA-II. Interior view of SL-1 reactor building on operating floor. Feedwater p |
| 1958 | 5360x4284 | 0.75 | HAER ID-33-D-60 | ARA-II. Interior view of SL-1 reactor building, camera looking upward after to |
| 1958 | 5294x4325 | 0.75 | HAER ID-33-D-59 | ARA-II. Interior view of SL-1 reactor building, camera looking up toward as to |
| 1958 | 5309x4340 | 0.65 | HAER ID-33-D-63 | ARA-II. Ten-ton crane in SL-1 reactor building transports the reactor head. Fe |
| 1958 | 4258x5335 | 0.74 | HAER ID-33-D-66 | ARA-II. Looking up covered stairway outside SL-1 reactor building while worker |
| 1958 | 5324x4289 | 0.79 | HAER ID-33-D-62 | ARA-II. Ventilating fan in SL-1 reactor building, not yet hooked up, but in pl |
| 1958 | 5345x4314 | 0.74 | HAER ID-33-D-64 | ARA-II. Interior view of SL-1 reactor building with reactor head in place in c |
| 1958 | 5314x4314 | 0.72 | HAER ID-33-D-65 | ARA-II. Interior view of SL-1 reactor building control piping for water purifi |
| 1958 | 5314x4288 | 0.77 | HAER ID-33-D-68 | ARA-II. Workmen on SL-1 operating floor look at shielding gravel in cover of w |
| 1959 | 5350x4269 | 0.59 | HAER ID-33-D-74 | ARA-II. Dr. William Zinn of combustion engineering company and others at contr |
| 1961 | 5340x4299 | 0.70 | HAER ID-33-D-76 | ARA-II. After SL-1 explosion, operators shielded crane cab try to open door of |

#### 1968年以降の記録写真（解体・跡地・建屋の記録）
| 寸法 | ink | HAER 番号 | 中身 |
|---|---:|---|---|
| 5385x4334 | 0.73 | HAER ID-33-D-78 | ARA-II. Aerial view in 1982 prior to characterization. Facilities were in use  |
| 5360x4283 | 0.74 | HAER ID-33-D-16 | ARA-II Administration building ARA-613. South (front) and east sides. Camera f |
| 5339x4253 | 0.92 | HAER ID-33-D-17 | ARA-II Administration building ARA-613. West side of building. Camera faces ea |
| 5324x4253 | 0.77 | HAER ID-33-D-72 | ARA-II. Interior view in ARA-602 support building showing oil-fired hot air fu |
| 5279x4288 | 0.92 | HAER ID-33-D-15 | ARA-II Administration building ARA-613, west side (in shade) and south side. C |
| 5269x4309 | 0.72 | HAER ID-33-D-77 | ARA-II. Room at northeast corner of ARA-606 used for welding training and weld |
| 5181x4208 | 0.92 | HAER ID-33-D-14 | ARA-II Contextual view from distance, camera facing east. Two story building n |
| 4063x3158 | 0.81 | — | INEEL 58-1360 HAER ID-33-D-64 195650pu |
| 3200x2584 | 0.74 | — | HD.6D.111 (10731009074) |
| 2500x3200 | 0.58 | — | HD.6B.007 (10578937954) |
| 2487x3200 | 0.51 | — | HD.6B.006 (10579022233) |
| 1812x1111 | 0.71 | — | SL-1Burial |
| 1436x1113 | 0.74 | — | Sl-1-ineel61-9 |
| 1406x1881 | 0.56 | — | Sl-1-ineel81-3966 |
| 1402x1050 | 0.89 | — | SL-1 - Dismantling of the foundation piers |

#### 額装パネル・暗幕の地にするもの（図面・線図）＝全画面に出さない
| 寸法 | ink | HAER 番号 | 中身 |
|---|---:|---|---|
| 5421x4301 | 0.20 | HAER ID-33-D-129 | ARA-II Administrative and technical support building (ARA-606) sections showin |
| 5412x4282 | 0.19 | HAER ID-33-D-137 | ARA-II Building ARA-602 floor plan as it appeared in 1980 when electrical modi |
| 5411x4301 | 0.35 | HAER ID-33-D-138 | ARA-II Building ARA-606 floor plan for remodel as Inel Welding Laboratory. Sho |
| 5407x4287 | 0.19 | HAER ID-33-D-132 | ARA-II Administration building (ARA-613) elevations of north, south, east, and |
| 5402x4292 | 0.21 | HAER ID-33-D-126 | ARA-II Plot plan showing location of SL-1 power plant (reactor) building, and  |
| 5398x4291 | 0.18 | HAER ID-33-D-127 | ARA-II Administrative and technical support building (ARA-606) ground floor pl |
| 5398x4292 | 0.19 | HAER ID-33-D-131 | ARA-II Administration building (ARA-613) floor plans for first and second floo |
| 5397x4287 | 0.22 | HAER ID-33-D-128 | ARA-II Administrative and technical support building (ARA-606) elevations for  |
| 5393x4254 | 0.16 | HAER ID-33-D-134 | ARA-II SL-1 decontamination and lay down building (ARA-614) erected after acci |
| 5388x4264 | 0.16 | HAER ID-33-D-135 | ARA-II SL-I decontamination and lay down building (ARA-614) north, south, east |
| 5384x4273 | 0.18 | HAER ID-33-D-130 | ARA-II Administration building (ARA-613) vicinity map and plot plan showing re |
| 5379x4292 | 0.16 | HAER ID-33-D-133 | ARA-II SL-1 burial ground. Shows gravel path from ARA-II compound to the buria |
| 1454x1753 | 0.12 | — | SL-1 - Reactor schematic |
| 729x589 | 0.33 | — | SL-1 - Cutaway of reactor and control building |

#### ❌ 幅が足りず全画面に出せないもの（1280px 未満）
- 1261x884 `Sl-1-ineel61-667`
- 720x548 `ALPR`
- 704x346 `SL1nuclearpowerplant`
- 640x480 `"Nuclear Power Reactor - The SL-1 Accident Video- Briefing Film Report`
- 346x253 `US AEC SL-1`
- 160x110 `SL-1 The Accident Phases I and II Animated`

### ③ 一次資料 IDO-19302（AEC アイダホ支所の事故報告書・1962）

| | |
|---|---|
| 題 | *IDO Report on the Nuclear Incident at the SL-1 Reactor, January 3, 1961* |
| 取り方 | `curl -L -o ref/sl1/IDO-19302.pdf https://www.osti.gov/servlets/purl/4809634`（17.1MB・208ページ） |
| 権利 | AEC ＝合衆国政府の職務著作＝**パブリックドメイン** |
| リポ | ❌ 入れない（17MB）。上の1行で取り直せる |

**208ページを 100dpi で測った結果**
- **189/208 ページに文字層がある**＝原文照合にそのまま使える（OCR は要らない）。
  ⚠️ ①題材のときの「走査版」という見立ては誤り。文字が取れないのは1ページ目（表紙）だけ
- **図・写真のページ ＝ 43ページ**（文字400字未満・インク率0.03以上）。
  うち写真とみられる濃いページ＝**p1・p2・p46・p47・p48・p180〜p184**
- 図のページの一覧＝`analytics/materials/sl1_ido_pages.json`（頁・文字数・インク率・空白帯・bbox）

⚠️ **報告書の図の英字は焼き込まれている**（ベクタで付いてこない）。
画素で測って切る＝`tools/fitcrop.py`。→ [[reference-report-figures-have-burned-in-english]]

### ④ ❌ 使わないと決めたもの

| 何 | 理由 |
|---|---|
| archive.org の Prelinger 版ブリーフィング映画（640x480・524秒） | **解像度が足りない**（本レンダは1920x1080）。①の記録映画2本が同じ1920x1080で55分43秒あるので保険も要らない |
| 同 `sl-1-accident-briefing-report-1961…`（480x360） | 同上 |
| Commons の6点（`SL1nuclearpowerplant` 704px・`ALPR` 720px・`US AEC SL-1` 346px・briefing film webm 640px・`SL-1 The Accident … Animated.gif` 160px ほか） | **幅1280px 未満**＝全画面に耐えない |
| LoC `loc.gov/pictures` の HAER ID-33 原本 | 403 のままだが、**Commons に同じ絵が 5300px で在る**ので当たる必要が無い |

### ⑤ 画面に出す出典表記

- 記録映画 … `footage.credit_of()` が `CLIPS[...]["credit"]` から作る
  ＝「出典：米国国立公文書館（NARA）／米原子力委員会（AEC）撮影 「SL-1 Accident Phase I & II」（NARA naId 174689848）／パブリックドメイン」
- Commons の写真 … `HAER ID-33-D-NN`（`ref/sl1/materials.json` の `acc`）を添える
  ＝「出典：米議会図書館 HAER ID-33-D-76／パブリックドメイン」
- 報告書 … 「出典：IDO-19302（米原子力委員会アイダホ支所・1962）p.NN」
- 追加の3冊（下の⑥）… 「出典：IDO-19311（米原子力委員会／GE・1962）I-5」
  ／「出典：ANL-6692（アルゴンヌ国立研究所・1962）p.36」
  ／「出典：HAER No. ID-33-D（米議会図書館）」

⚠️ **必須でないクレジットは書かない**（→ [[feedback-no-optional-credits]]）。
⚠️ **概要欄・説明文に素材の方針を書かない。画面に出す運用は続ける**（2026-08-03 の決定）。

### ⑥ 🔴 2026-09-07（④台本）で追加した一次資料4件

**理由：IDO-19302 は前書きで「原因は扱わない」と宣言しており、原因が書けない。**
（`This IDO SL-1 Report ... does not attempt to determine the cause of the incident,`
`which is the subject of a separate report by the AEC Board of Investigation.` 印字 p.vii・原寸で確認）

| 資料 | 取り方（すべて HTTP と中身を実測） | 実測 | 権利 |
|---|---|---|---|
| **IDO-19311**『FINAL REPORT OF SL-1 RECOVERY OPERATION』GE・1962-07-27 | `curl -L -o ref/sl1/IDO-19311.pdf https://www.osti.gov/servlets/purl/4763434` | 200 / application/pdf / 29,526,451 B / **320ページ** | AEC 契約下の職務著作＝**PD**（17 U.S.C. §105） |
| **IDO-19313**『ADDITIONAL ANALYSIS OF THE SL-1 EXCURSION』GE・1962-11-21 | `curl -L -o ref/sl1/IDO-19313.pdf https://www.osti.gov/servlets/purl/4164582` | 200 / application/pdf / 33,604,028 B / **191ページ** | 同上 |
| **ANL-6692**『A RETROSPECTIVE ANALYSIS OF ASPECTS OF THE ALPR (SL-1) DESIGN』ANL・1962-11 | `curl -L -o ref/sl1/ANL-6692.pdf https://www.osti.gov/servlets/purl/4727996` | 200 / application/pdf / 5,819,351 B / **54ページ** | 同上 |
| **HAER No. ID-33-D**（Army Reactors Experimental Area の記録文書） | `curl -L -o ref/sl1/HAER_ID-33-D.pdf https://tile.loc.gov/storage-services/master/pnp/habshaer/id/id0400/id0410/data/id0410data.pdf` | 200 / application/pdf / 7,681,211 B / **64ページ** | 米議会図書館 HABS/HAER＝**PD** |

🔴 **IDO-19313 は「これらの値は IDO-19311 で報告された」と自ら書いている**（§II-1 冒頭）。
　 ＝ **数字の発生源は IDO-19311**。出典は 19311 を主、19313 を従にする。

#### ⚠️ 文字層は OCR で崩れている（引き継ぎの「そのまま照合に使える」は誤り）
文字間に空白が入り（`S t a t i o n`）、字が化ける（`AM:`＝AEC／`SrgO`＝Sr90／`118 inch`＝1/8 inch）。
**素の grep は「在るのに0件」を返す。**画面に出す語は**必ず原寸の画像で目視**すること。
台本第1版では、決め所17件のうち**5件が、原寸で見なければ語を決められなかった**。

道具＝**`tools/ido_text.py`**（1本にまとめた。`--selftest` PASS 19項目）:
- `extract` … PDF の文字層を全文テキストに落とす（`--02` などで1冊だけも可）
- `find` … 崩れに強い検索（①空白と記号を無視 ②`--fuzzy` で字を畳む ③`--near` で語の同居）
- `page` / `crop` … ページの素の文字／語で当たりを付けて**一部だけ**を PNG に切る（原寸を丸ごと読まない）

⚠️ **`--selftest` を先に通すこと。**この検算は 2026-09-07 に**3回、書き手の思い込みを捕まえた**：
① `lower()` を畳む前に掛けていて大文字 `I` が畳まれていなかった
② 「`Decontamination` は壊れている」→ **壊れているのは目次の1ページだけで本文11ページは無事**
③ 「原文は `20 inch`（単数）で `20 inches` は0件」→ **単数3件・複数1件。両方ある**（③は調査係の申し送りの誤り）

#### リポに入れたもの／入れなかったもの
- ✅ 入れた＝**全文テキスト3本**（`ido_all.txt` 376K／`IDO-19311_all.txt` 460K／`IDO-19313_all.txt` 248K）。
  OSTI が落ちても原文照合ができるように。
- ❌ 入れない＝**PDF 5本**（合計92MB）と、ページ単位に割ったテキスト（全文から作り直せる）。
- 🔴 **⑤b で報告書の図を画にするときは、`.gitignore` に1行足すのを忘れない。**
  足さないと `git add -A` が黙って落とし、**クラウドで初めて FileNotFoundError になる**（r24 の実例）。

#### 印字ページと PDF ページの対応（実測）
**IDO-19302 は PDF ＝ 印字 ＋ 11**（208ページ中134ページで印字番号を拾い、125ページがこの差で一致）。


### ⑦ 🔴 2026-09-07（⑤b 映像）で用意した素材 — **画面に出る絵はここが全部**

道具＝`tools/sl1_assets.py`（`--selftest` 30項目 PASS。印字ページと PDF ページの対応を**本文の語**で検算）。
⚠️ **PDF ページではなく印字ページ**を画面と出典に出す（IDO-19302 は PDF ＝ 印字 ＋ 11）。

| 種別 | 件数 | 出力名 | 画面に出す出典 | 権利 |
|---|---:|---|---|---|
| IDO-19302 のページ | 17 | `sl1/ido_p*.png` | 「出典：IDO-19302（米原子力委員会アイダホ支所・1962） p.NN／パブリックドメイン」 | AEC＝合衆国政府の職務著作 |
| IDO-19311 のページ | 2 | `sl1/i11_p*.png` | 「出典：IDO-19311（米原子力委員会／ゼネラル・エレクトリック・1962） 要旨 ii／I-5」 | AEC 契約下の職務著作 |
| ANL-6692 のページ | 2 | `sl1/anl_p*.png` | 「出典：ANL-6692（アルゴンヌ国立研究所・1962） 表紙／p.36」 | 同上 |
| **AEC 調査委員会報告** | 1 | `sl1/aec_p001_cover.png` | 「出典：米原子力委員会 SL-1 事故 調査委員会報告（1961年6月） 表紙」 | 同上 |
| **官報 36 FR 3258** | 1 | `sl1/fr_p3258_gdc.png` | 「出典：連邦官報 36 FR 3258（1971年2月20日）／10 CFR 50 付録A」 | 合衆国政府の編集著作＝PD |
| HAER の記録写真 | 14 | `sl1/haer_NN.jpg` | 「出典：米議会図書館 HAER ID-33-D-NN／パブリックドメイン」 | HABS/HAER＝PD |
| 記録映画のひかえの静止画 | 35 | `sl1/fb_<cid>.jpg` | 動画の出典＋「（静止画）」 | NARA／AEC＝PD |

#### 🔴 ④台本の時点で「未保存」だった2件を、⑤b で取った
| 資料 | 取り方（HTTP と中身を実測） | 実測 |
|---|---|---|
| **AEC 調査委員会報告**（1961年6月） | Internet Archive `SL1PressRelease1961` の `SL-1 Press Release 1961.pdf` | 200 / 97,094 B / **43ページ**。1ページ目＝`UNITED STATES ATOMIC ENERGY COMMISSION REPORT ON THE SL-1 INCIDENT, JANUARY 3, 1961 THE GENERAL MANAGER'S BOARD OF INVESTIGATION`。`single control rod` **0件**（台本 c904 の根拠を再現） |
| **官報**（1971-02-20） | `https://www.govinfo.gov/content/pkg/FR-1971-02-20/pdf/FR-1971-02-20.pdf` | 200 / 25,130,139 B / 96ページ。**印字 3258 ＝ PDF 12**。Criterion 25 と 26 が同じページに在ることを本文で確認 |

⚠️ **収蔵品の題は「Press Release」だが、中身は報告書本体だった。**題で決めず1ページ目を開いて確かめた。
❌ PDF はリポに入れない（`.gitignore` の `ref/sl1/*.pdf`）。上の1行で取り直せる。

#### 🔴 グレースケールで保存している
報告書のページは**全部グレースケールの PNG**。本編は低彩度のデュオトーンで焼くので紙の色は最終出力に出ず、
RGB のままだと 22.8MB になる（このリポジトリは public）。⇒ 12.5MB。絵は変わらない。
官報だけ色あせた紙の色（RGB 189/171/144）を持っていたが、同じ理由で落とした。

#### 🔴 記録映画2本の中身（⑤b で全410ショットを見た）
**台帳＝`ref/sl1/SHOTS_INDEX.md`。**⚠️ 2本とも「事故の夜の記録映像」ではなく、事故後に作られた**技術説明映画**。
夜の屋外・消防車・救急車・担架・門衛所・雪の砂漠は**1コマも無い**（1961年1月の夜に撮影班はいない）。
使ってはいけないショット（NARA の収蔵カード・出所カード・表題・制作クレジット・End of Recording）は
OCR で機械が名指しし、`tools/sl1_shots.BANNED` に入れてある。

---

## フランシス・スコット・キー橋 崩落（2024-03-26・6本目）

**2026-09-08（②素材）に Commons の 1,017点を1点ずつ実測した。**
生データ＝`analytics/materials/Category_Francis_Scott_Key_Bridge_collapse.json`（git 管理外）。

### 🔴 ここが今までと違う ── 「PD」の中に**米連邦でないもの**が4割入っている

これまでの5本は「PD＝米連邦の職務著作（17 U.S.C. §105）」で説明が付いた。
キー橋は付かない。**同じ "Public domain" の札で、根拠が2種類ある。**

| 階層 | 総点 | 全画面 | 根拠 | 表示義務 |
|---|---|---|---|---|
| **A 米連邦 §105** | 237 | 185 | 沿岸警備隊・陸軍工兵隊・海軍・NTSB・FBI の職務著作。多くは DVIDS 番号（`240407-A-PA223-1003`）付き | 無し |
| **B 所有者によるPD宣言** | 191 | 189 | 🔴 **ボルチモア郡（Baltimore County, Maryland）の Flickr `56007743@N08`** が180点。郡は州・地方政府なので §105 は当たらない。**郡自身が Public Domain Mark / CC0 を付けている**（＝任意の放棄） | 無し（礼儀として書く） |
| **C CC BY（表示が要る・継承なし）** | 582 | 576 | **メリーランド州知事室 `Maryland GovPics` が543点**。ほかに州会計監査官17・個人19・Capella Space（衛星SAR）2・**WBFF FOX45 Baltimore 1** | **有り** |
| **D 継承あり（CC BY-SA）・帰属のみ** | 7 | 1 | Wikipedia 利用者の作図と Copernicus Sentinel-2 | **使わない** |
| 合計 | **1,017** | **951** | | |

⚠️ **`license` の生の値と、分類ずみの値を混ぜて数えない**（①で一度これを踏んで「PD 0点」と誤った）。
生の値＝`CC BY 2.0 471／Public domain 419／CC BY 4.0 110／CC0 8／CC BY-SA 3.0 3／Attribution 2／その他4`。

⚠️ **B の「PD宣言」は §105 と同じではない。** CC は Public Domain Mark を法的な放棄の道具として
推奨していない（放棄なら CC0）。Commons は所有者本人が付けた PDM を受け入れているので使えるが、
**A と B を1つの数にまとめて「PD 428点」と書かない。**

⚠️ **`WBFF FOX45 Baltimore`（地元テレビ局）が1点だけ CC BY で混ざっている。**
報道映像は Content ID の当たりやすい種類なので、**使うなら1点ずつ判断する**。

### 🔴 「全画面951点」は使える枚数ではない ── 6割が会見・式典

題名で仕分けた全画面951点の内訳（実測）:

| 中身 | A連邦 | B所有者PD | C CC BY | 計 |
|---|---|---|---|---|
| 1 崩落現場・橋 | 92 | 177 | 11 | **281** |
| 2 サルベージ・撤去 | 63 | 0 | 8 | **71** |
| 3 貨物船 Dali | 28 | 5 | 12 | **45** |
| 4 会見・式典・視察・記念行事 | 2 | 7 | 545 | **554** |

🔴 **会見・式典を除いた実務的な母数＝397点（うちPD 365点）。**
38分＝写真110カットに対して 3.6倍。**足りるが、「951点で余る」は言い過ぎ**（①の見立ての訂正）。
⚠️ 崩落現場281点のうち **177点はボルチモア郡（B階層）**。連邦だけに絞ると崩落現場は92点まで落ちる。

### 中身は画素で測った（60点の抜き取り）

`src_probe.measure` で無作為60点（種 20260908）。**インク率 中央値 0.780・四分位 0.658〜0.924**。
`INK_FULL=0.42` を下回ったのは3点だけで、**どれも図面ではなく「1周年式典・円卓会議の明るい屋内写真」**。
⚠️ **SL-1 で決めたしきい値は、この題材では「図面と写真」ではなく「暗い屋外と明るい屋内」を分けている。**
図面の除外に使ってはいけない（bitdepth 1 の38点は別の網で既に落ちている）。
→ [[feedback-gate-threshold-from-ledger-split]]

### 動画 29本（すべてパブリックドメイン）

`ffprobe` で1本ずつ実測（`analytics/materials/keybridge_videos_probe.json`）。

- **合計 73.6分**。ただしホワイトハウスの総集編『A look back at March 2024』（23.9分）は
  キー橋以外が大半で第三者の映像が混ざるため**使わない**。⇒ **実質 28本・49.7分**
- 解像度＝**3840×2160 が12本・1920×1080 が12本**・2048×1080 が1本・
  720×958 と 480×848 が各1本（⚠️ **縦位置の携帯動画**。全画面には使えない）
- ⚠️ `upload.wikimedia.org` は**名乗らないと 429 Too Many Requests**。
  `ffprobe`/`ffmpeg` に `-user_agent` を渡す（`footage.UA` / `shots.UA`）。
  29本中19本が最初の走査で「0秒」に見えた＝**中身が空ではなく429だった**
- ✅ `Range: bytes=0-1023` に **206** を返す＝**落とさずに区間だけ切り出せる**（`footage.py` の方式が使える）

**ショットの台帳＝`ref/keybridge/SHOTS_INDEX.md`（全355ショット・1秒刻み）。**
🔴 **8秒以上のショットが152本（35.2分）、うち動きのあるものが142本。**

🔴🔴 **崩落の瞬間の映像は無い。** 事故当日（2024-03-26）に撮られたのは3本だけで、
どれも崩落**後**（NTSB の空撮 451秒／沿岸警備隊の応急艇 62秒／MH-65 の上空通過 156秒・縦位置）。
世に出回る「橋が落ちる瞬間」は StreamTime Live の定点カメラと報道の映像で、**PD ではない**。

### 一次資料

| 何 | 実体 | 文字層 |
|---|---|---|
| NTSB **MIR-25-40**（最終報告・259頁） | `ref/keybridge/ntsb_MIR2540.pdf` ← `https://www.ntsb.gov/investigations/AccidentReports/Reports/MIR2540.pdf` | ✅ 全259頁に有り。OCR不要 |
| NTSB **MIR-25-10**（船舶衝突に対する橋の脆弱性・26頁） | `ref/keybridge/ntsb_MIR2510.pdf` ← 同 `MIR2510.pdf` | ✅ 全26頁に有り |
| 公開ドケット | `https://data.ntsb.gov/Docket/?NTSBNumber=DCA24MM031` | 未取得 |

❌ PDF はリポに入れない（`.gitignore`）。上の URL で取り直せる。
抽出テキストと**照合ずみの数字**は `ref/keybridge/FACTS.md`。

### NARA は空振り（記録として残す）

`nara_probe search "Key Bridge collapse Baltimore"` → 該当8,424件・**写真/記録映像 0点**（全部 Textual）。
**2024年の事故は NARA に入るには早すぎる。**素材の本体は Commons／DVIDS／NTSB。

### DVIDS 本体は掘らないことにした（②の判断・2026-09-08）

Commons の連邦分237点は**ファイル名が DVIDS の命名そのもの**（`240407-A-PA223-1003`）で、
credit も `dvidshub.net` を指している＝**Commons は DVIDS の写し**。
実務的な母数397点は必要枚数の3.6倍あり、動画も49.7分ある。
**DVIDS を掘っても同じ絵が重複で増えるだけ**なので回さない。
⚠️ 逆に**枚数が足りないと分かった時点で掘る**（`tools/dvids_probe.py`。
CDN の `2000w_q95.jpg` は認証なしで通るが、**小さい原本を引き伸ばす**ので実効幅は原本と配信物の小さいほう）。
🔴 DoD の映像を使うときは「推奨を意味しない」断り書きの表示義務に注意（FEMA 撮影分には付かない）。
