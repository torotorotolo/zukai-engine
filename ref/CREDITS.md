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

### ⑤b（2026-09-08）に作った素材 ── 報告書の図32枚＋Commons 写真11点

**道具＝`tools/keybridge_assets.py`。表と1対1。**

#### 報告書のページ（`ref/keybridge/kb_p<印字>_fig<図番>.png`・**40枚**）
NTSB **MIR-25-40** を 3.0倍で PNG に焼き、グレースケールで保存（このリポは public）。
権利＝合衆国政府の職務著作（17 U.S.C. §105）。**画面に出すのは印字ページ**（PDF ＝ 印字 ＋ 2）。
`--selftest` が40枚すべてについて「本文の語」と「`Figure N.`」の**両方**をそのページで照合する（**82/82 ✓**）。
⚠️ 2026-09-09（⑤c）に**実測で数え直した**。ここは「32枚・66/66」と書いてあったが、
　 ⑤b-5／⑤b-6 で8枚焼き足したあと**この行だけ古いまま**だった（道具の側は40枚を見ている）。
　 報告書に在る図そのものは **71枚**（`python tools/keybridge_assets.py list`）。焼いたのはそのうち40枚。

🔴 **台本 §4 の画の欄の書き間違い3件をここで直した**（出典欄のほうが正しかった）:
`c712` p112→**p114**（Figure 50 HR1 UVR control circuit）／
`c715` p113→**p115**（Figure 51 Terminal Block 381）／
`ca02` p113→**p118**（Figure 53 Wire 1 と Wire 3）。

#### Commons の写真（`ref/keybridge/kb_*.jpg`・11点）

🔴 **②の「事故前の写真は在庫に1点も無い」は誤りだった。**
②が数えたのは `Category:Francis Scott Key Bridge collapse`（1,017点・全部 崩落後）と
郡 Flickr の `FSK-Collapse-NNN`（170点・同）だけ。
**`Category:Francis Scott Key Bridge (Baltimore)` に 252点あり、うち事故前が 99点**
（幅1280以上・連続階調 92点／PD 19・CC BY 12・残り CC BY-SA）。
台帳＝`analytics/materials/kb_pre.json`・`kb_const.json`。

⚠️ **CC BY-SA は採らない**（「継承」が動画全体に及ぶ論点を抱えない）。下は PD と CC BY だけ。

| 名前 | 中身 | 権利 |
|---|---|---|
| `kb_pre_1976` | 1976-08-11 開通前の橋（The Evening Sun） | PD（US no notice） |
| `kb_pre_harbor07` | 2007 内港から見た全景 | PD（撮影者が放棄） |
| `kb_pre_navy12` | 2012 橋の下をくぐる USS San Antonio | PD 米海軍 |
| `kb_pre_oakhill14` | 2014 橋に近づく USS Oak Hill | PD 米海軍 |
| `kb_pre_catlett22` | 2022 橋の下を通る工兵隊の測量艇 CATLETT | PD 米陸軍工兵隊 |
| `kb_pre_deck05` | 2005 橋の路面（車内から・4車線） | CC BY 2.0 Brent Moore |
| `kb_pre_2019` | 2019 全景 5416×3610 | CC BY 2.0 Rafael Saldaña |
| `kb_bld_harbor` `kb_bld_piers` `kb_bld_supports` `kb_bld_curtis` | 建設中の橋・橋脚（NARA 546833/546837/546929/546911） | PD |

🔴 **2026-09-09（⑤c'）：CC BY の2点は「改変した旨」も画面に出す。**
`kb_pre_deck05`（→ `c106` `c112` `c201` `c213`）と `kb_pre_2019`（→ `c101` `ep06`）の
**6カットは全部が改変物**です。この動画は写真をすべてデュオトーンにし
（`build_jiko.duotone`＝`convert("L")` から2色へ）、枠に合わせて切り出しています。
CC BY 2.0 §4(b) は帰属に加えて**改変した旨の表示**を条件にしているので、
`scene_jiko.credit_of()` が CC BY の行にだけ `／改変：色調変更・切出` を足します。

- ⚠️ **PD の素材には足さない。** 同じ断りを付けると、表示の義務が無いものにも
  あるように見える（PD はこの動画で40カット以上ある）。
- ⚠️ 判定は文字列 `"CC BY"` を含むかどうか。CC BY-SA は**そもそも採っていない**ので
  この網には入らないが、将来 CC BY-SA を採るなら**継承の扱いを先に決める**こと。
- 実測：この網に掛かるのは上の6カットだけ。行の幅は最大 864px（24px・枠1,776px）。

⚠️ **まだ足りない主題**（⑤b の続きで測る）: 事故前の 17番橋脚まわり・防衝工・トラスの内側・
夜の港・補修班の車両・州交通局警察の車と艇。**代用しない**（無ければ図に置き換える）。

#### 動画から抜いた静止画（`ref/keybridge/fb_<cid>.jpg`・**37枚**）

`footage.USE` の各欄が指す**その秒のコマ**を1枚だけ焼いたもの（`python tools/keybridge_assets.py fb`）。
**権利は元の動画と同じ**（上の記録映像の表）。画面の出典も `scene_jiko.credit_of` が
`KB_FB` の規則で元の動画の出典を出す（`（静止画）` を付ける）。

- **動画のコマが取れたときは動画が勝つ。**これは取れなかったときに出る控え
- 🔴 2026-09-09（⑤c）：**37枚とも焼かれていなかった**（`keybridge_assets.fb()` が
  「落としたクリップ `out/jiko/clip/*.mp4`」しか見ていなかったが、`footage.py` は
  **落とさずに URL から区間だけ**取る作りなので clip/ は永久に空）。
  → URL からも1コマ抜けるようにして焼いた。⚠️ **Wikimedia は続けて投げると5本目から落ちる**
  ので、間を空けて3回まで試す（1件ずつ手で叩くと通るのに、まとめて回すと落ちる形）

## 9.11 米国同時多発テロ（2001-09-11・7本目）

**2026-09-13（②素材）に実測した。**①の当たりは
Vault `Projects/引き継ぎ-事故検証-7本目-①題材-20260913-9.11の当たり.md`、
正本の数字は `ref/themes/ledger.json` の 9.11 の行。
②の生データ＝`analytics/materials/ep7/s2/`（git 管理外）。

### 1. 動く素材 ── NARA RG237（FAA）naId 7419198 の32点だけを使う

**32点・10,740.9秒（179.0分）。32点すべて `use=Unrestricted`。**
根拠＝**合衆国法典17編105条**（連邦航空局＝米連邦機関の職務著作）。
台帳＝`ref/ep7/clips.json`（`analytics/materials/ep7/s2/make_clips.py` が ffprobe の実測から
書き出す。**手で書かない**）。

| 便 | 本数 | 秒 | 分 |
|---|---:|---:|---:|
| UAL 93（シャンクスビル） | 11 | 9,470.1 | 157.8 |
| 5 その他・全体図 | 14 | 807.5 | 13.5 |
| AAL 77（ペンタゴン） | 3 | 158.1 | 2.6 |
| UAL 175（WTC南棟） | 2 | 158.1 | 2.6 |
| AAL 11（WTC北棟） | 2 | 147.1 | 2.5 |
| **計** | **32** | **10,740.9** | **179.0** |

中身は**四便の航跡レーダー再現と ARTCC（航空路管制センター）の画面**。他局がまず使っていない。

#### 🔴 実測（①は尺と解像度だけ。②で fps と kbps を足した）

| | 値 |
|---|---|
| 解像度 | 720×480 **27本** ／ 1280×1024 3本 ／ 640×480 2本。**1920以上は0点** |
| fps | 60.0 **27本** ／ 20.0 3本 ／ 30.0 1本 ／ **1.001 1本** |
| コーデック | h264 27 ／ tscc（画面録画）3 ／ mpeg1video 1 ／ rawvideo 1 |
| kbps | 最小 259 ／ 中央 2,623 ／ 最大 3,850 |
| 音声トラック | **28／32本にある** |

#### 🔴🔴 切り出しの前に必ず効かせること3つ（どれも既存の門番は1本も鳴らない）

**① 画素が正方形でない。**27本が **SAR=10:11 ／ DAR=15:11**。
そのまま切り出すと **横に10%ふくらむ**（レーダーの円が卵になる）。

- `footage._cut_stream()` の `scale={want}:-2` は **SAR を見ない**。しかも 720 < 1920 なので
  `want == c["w"]` になり、**scale そのものが付かない**＝素通りする。
- → ⑤で `-vf` に **`scale=iw*sar:ih`** を足す。720×480 → **655×480**。
  台帳の **`dispw`** 欄がその幅。実測で `654×480` が返ることを確かめてある。

**② `-an` を必ず付ける。**28／32本に音声トラックがある。①で「音は鳴らさない」と決めている。

**③ `yadif` は付けない。**器の札は `field_order=tt`（インターレース）だが、**札が古い**。
3つの実測が「60p（1コマずつ本物）」で一致した：

| 測り方 | 結果 |
|---|---|
| `nb_frames ÷ 秒` | **60.00**（例：90,852 ÷ 1,514.3）＝コマが実在する |
| `ffmpeg -vf idet` 200コマ | **TFF 0 ／ BFF 0**（残りは Undetermined＝動きが少なく判定不能） |
| yadif あり／なしの櫛の指標 | **0.5% しか動かない**（0.544 → 0.541） |

⚠️ 札を信じて yadif を入れると、**480本しかない縦の解像度を無駄に半分**にする。
⚠️ 陰性対照（もともと progressive の `.mpg`）でも櫛の指標が 0.654 と高く出た＝
**この指標だけでは決められない**。決めたのは上の3本目の経路（コマ数）。
→ [[feedback-verify-your-own-instrument]]

**④ 額装パネル。**1920に届く点が0なので全画面にできない。
655×480 を `scene_jiko.PANEL_MAXW/H`（1120×648）に入れると **z=1.35 → 883×648**。
⑤で原寸目視して甘ければ `pw=655`（等倍）に落とす。

⚠️ **同じ naId に別形式が2点ある**（7601807 ＝ `.mp4` と `.mpg`）。
拡張子を落として鍵にすると1点消える（実測：31点・10,694.7秒＝**ちょうど46.2秒＝`.mpg` 1本ぶん**）。
→ 台帳の鍵は**拡張子つき**。検算は「32点」と「10,740.9秒」の**両方**で見る。

⚠️ 同じ RG237 系列の**音声770点は `access` が全点 `Restricted - Possibly`**（FAA の黒塗り注記）。
**映像32点（access も Unrestricted）とは扱いが違う。1行に混ぜない。**
⚠️ 系列に1999年ペイン・スチュワート機（N47BA）が15点まぎれ込むが、**映像32点には0点**
（ファイル名の頭が 1〜5 だけ。`6-` は0件＝道具で検算ずみ）。

⚠️ **NIST FOIA の2本（70.3分）は使わない。**1本は Commons で削除依頼中、
1920×1080 の方は撮影者が **WABC-TV（報道機関）**で、説明文に「窓から手を振る人」
「取り残された人」が明記＝この回の禁じ手に正面から当たる。
→ **動く絵は RG237 の32点に限り、報道由来の記録映像を1点も入れない。**

### 2. 写真 ── 「事故の前」の **PD の根拠を1点ずつ分けた**

→ [[feedback-pd-label-hides-two-different-grounds]]。Commons の札はどれも "Public domain" に
見えるが、根拠は少なくとも4つある。**1行に混ぜない。**

測り方＝①の2つのプール（`material_photo_rows.json` 9,283点 ＋ `p4_gap2_rows.json` 5,564点）から
「事故の前」を集めて和集合にし、別版（.jpg/.tif/cropped）を潰し、
**Commons のページ原文（wikitext）からライセンス雛形そのもの**を読んだ。

| | 点数 |
|---|---:|
| 和集合（題で潰して） | 710 |
| 別版を潰したあと | **698** |
| うち 幅1280以上 | 578 |
| うち **幅1920以上（全画面に耐える）** | **475** |

#### 🔴 幅1920以上 475点の根拠

| 根拠 | 点数 | 割合 | 画面の出典の書き方 |
|---|---:|---:|---|
| **A 米連邦 §105** | **185** | 38.9% | 「パブリックドメイン」と書ける。表示義務なし |
| **B 著作権の満了** | 9 | 1.9% | 同上 |
| **C 自主宣言（PD-self / CC0）** | 4 | 0.8% | 同上。礼儀として撮影者名を書く |
| — **PD と書ける小計（A+B+C）** | **198** | **41.7%** | |
| **D「知られた制限は無い」（LOC 等）** | 70 | 14.7% | 🔴 **PD の宣言ではない。**「米議会図書館蔵／既知の利用制限なし」と書く |
| **E 根拠不明** | 22 | 4.6% | 🔴 **使わない**（1点ずつ当たるまで） |
| **F CC（PDではない）** | **185** | 38.9% | 🔴 **表示（BY）が要る。SA は継承も要る** |

⚠️ **「事故の前 475点」の6割は PD ではない。**「PD が◯点ある」で素材計画を立てない。

⚠️ **28点は『事故の前』ではない**（日付が2001年より後）。
全部プール2＝①の `era` 分類の取りこぼし（airport 12・manhattan_90s 13・pentagon_pre 2・wtc_pre 1）。
**使う束を作るときに落とす。**

⚠️ 幅の最小は **125px**。「事故の前」の束は**幅の網を通っていない**ものを含む。
全画面に使えるのは 475点（68.0%）だけ。

#### ⚠️ 当該4機そのものの事故前の写真（①の実測。②で扱いだけ確認）

| 便 | 機体記号 | 最大 | 札 |
|---|---|---|---|
| AA11 | N334AA | 3767×2511（2001-04-08） | CC BY-SA 3.0 |
| AA77 | N644AA | 1280×850（1995-03） | GFDL 1.2 ほか |
| UA93 | N591UA | 1690×1078（1999-11-12）。**別の1点が事故3日前**（1000×635） | CC BY 2.0 ほか |
| **UA175** | **N612UA** | **1024×761** | GFDL 1.2 |

🔴 **4機とも札は CC で、§105 ではない。**表示（BY）と継承（SA）の様式が要る。
🔴 **UA175 だけ 1920幅に届かない。**額装パネルで出すか、4機を並べた合成
（`September 11 Aircraft Hijacked.jpg` 7200×2406・CC BY-SA 3.0）で受ける。

### 3. 音 ── **使わない**

| 系列 | 点数 | 時間 | use | access |
|---|---:|---:|---|---|
| RG237（FAA）7419198 | 770 | 746.6時間 | Unrestricted | 🔴 **Restricted - Possibly**（全点） |
| RG148（委員会）4319604 | 25 | 41.9時間 | Unrestricted | **Unrestricted** |
| RG148（委員会）5952561 | 342 | 67.3時間 | Unrestricted | Unrestricted 219／Partly 123 |
| 計 | **1,137** | **855.8時間** | | |

🔴 **①の決定どおり、7本目では1秒も鳴らさない。**理由は①§7-4。

🔴 **②で測ったこと＝「音から新しく起こせる逐語は 0分」。**
この ch に**耳で起こす工程が無い**（英語 ATC の混信・話者の特定）。
RG148 の25点（access まで Unrestricted・41.9時間）は
**全部が `[AAL 77] Washington ARTCC Certified Rerecording`＝1便・1センターぶん**でもある。
＝ 音を鳴らす構成に切り替えても、四便を通す背骨にはならない。

→ **使うのは「すでに活字になっている逐語」だけ。**

### 4. 逐語（文字）── 9/11委員会報告の第1章

`GPO-911REPORT.pdf` の文字層 **1,920,395字**。第1章「WE HAVE SOME PLANES」は
idx 15,950〜136,623 の **120,673字**。

| | 本数 |
|---|---:|
| 引用符（“…”）の対 ぜんぶ | 2,309 |
| 話者札つきの転記行（`FAA:` `NEADS:` `American 11:` …） | 38 |
| **無線・管制らしい逐語（第1章）** | **51** |
| うち前後300字に時刻がある | **35**（68.6%） |
| うち80字以下＝1行で出せる | 33 |

話者の内訳＝NEADS 10／FAA 7／Command Center 5／Boston Center 4／American 11 2／副大統領 2。

⚠️ **1回目の道具は「引用符の対」だけを数えて 170本と出し、いちばん要る形を丸ごと落としていた。**
この報告書で価値のある管制の交信は**引用符の外**、話者札つきの転記で組まれている：

```
FAA: Hi. Boston Center TMU, we have a problem here. We have a hijacked aircraft…
NEADS: Is this real-world or exercise?
FAA: No, this is not an exercise, not a test.
```

章分けの目印も `1 “WE…` と書いて実際の `1. “WE…`（ピリオドつき）に当たらず、
170本すべてが「前付」に入っていた。→ [[feedback-verify-your-own-instrument]]

🔴 **`Let's roll` は委員会報告に0件**（曲アポストロフィでも0）。
**一次資料に無い言葉なので、画面にも台本にも出さない。**出すなら出どころを別に取る。

### 5. 一次資料の図 ── NTSB Flight Path Study を OCR にかけた

4本・**27ページ・文字層0字**（完全スキャン）。埋め込み画像は全部 幅1700px。
PyMuPDF で 300dpi に焼き、Windows の OCR（`tools/ocr_win.ps1`）に通した。

| 資料 | ページ | OCR の行 | OCR の字 | 時刻 | 3〜5桁の数 |
|---|---:|---:|---:|---:|---:|
| AA11 | 6 | 275 | 12,071 | 86 | 126 |
| UA175 | 7 | 311 | 11,885 | 78 | 189 |
| AA77 | 7 | 340 | 11,267 | 69 | 133 |
| UA93 | 7 | 331 | 13,265 | 93 | 178 |
| **計** | **27** | **1,257** | **48,488** | **326** | **626** |

対照＝**陰性**：真っ白な PNG で 0行。**陽性**：文字層のある委員会報告 p41 で
OCR 2,431字 対 文字層 2,480字＝**98.0%**（件数でなく**字数**で見た）。

⚠️ **OCR は「,」「:」の前後に空白を入れる。**詰めてから数えないと
「時刻0個・数0個」という嘘の結果になる（1回目に実際に出た）。
⚠️ **英文の綴りは信用しない**（`Research`→`Resea?u ch` のように小文字 r が化ける箇所がある）。
**数字だけを取り、画面に出す値は1つずつ図に当たり直す** → [[feedback-verify-every-onscreen-quote]]

### 6. この回で使わないもの（決めてある）

| | 理由 |
|---|---|
| 衝突の瞬間・落下する人・遺体 | 在庫が**実質0点**（4通りの網）。そもそも禁じ手 |
| 被害者の通話音声（裁判所展示） | 落とせるが権利を与える文が1文も無い。録ったのは私企業と911通信指令＝§105 の外 |
| UA93 のコックピットボイスレコーダーの**音** | 封印（P200056 が Exhibit Under Seal）。**逐語PDFだけ公開**（9ページ・文字層0） |
| NIST FOIA の映像2本 | 削除依頼中／撮影者が報道機関で禁じ手の場面を含む |
| 崩落の力学（NIST の図） | 6冊中5冊が紙のスキャンで**切り出せる図版0点**。①で筋から外した |

### 7. 🔴🔴 ナレーションの声を替えました（2026-09-13・カズヤくん指示）

| | 4〜6本目 | **7本目から** |
|---|---|---|
| 声 | Hiro - Ultra Deep Japanese Voice | **Koichi-Deep Calm Japanese Narrator** |
| voice_id | `qaCSabKToUUT4sTqBZtz` | **`H8ZPDxbrPcks5hEsi2fq`** |
| モデル | `eleven_v3` | `eleven_v3`（変えない） |
| TEMPO（合成後の atempo） | 1.05（6本目）／1.0（5本目） | **1.0**（＝atempo を通さない） |
| stability / similarity_boost | 0.85 / 1.00 | **0.64 / 0.89** |

⚠️ **同じコレクションに「Koichi Takase - Clear and Measured」（`aEdqPekRcUrJjvnAh1Eb`）が別に在る。**
名前だけでは決まらないので説明文まで突き合わせた（`H8ZP…`＝"Japanese male narrator with over 7 years…"）。

#### 実測：Koichi は Hiro より 14.9% 速い

同じ24文（`narration.SCRIPT` から長さの分布をまたいで採る）を同じ設定で合成して割った。

| | 文字/秒（speed 1.0） | 物差しの誤差 |
|---|---:|---:|
| Hiro | 5.562 | 3.04% |
| **Koichi** | **6.388** | 5.63% |
| 比 | **1.1485** | 差14.9% > 誤差5.63% ＝**測れている** |

生データ＝`analytics/el_speed_probe_koichi.json`（Hiro は `analytics/el_speed_probe.json`）。費用 359クレジット。

**物差しの陽性対照**＝6本目の実績（11,117字・443行・216カット）を尺の式に入れると **37分25秒**。
実際の6本目は **37:24** で **1秒差**。⚠️ 5.62 を基にすると8秒ずれるので、**基は 5.642 を採った**
（2つの基が4.6%食い違う。混ぜない → [[feedback-verify-your-own-instrument]]）。

#### 🔴🔴 字数を減らしても密度は下がらない

行間 `GAP 0.40` と カット頭尻 `LEAD 0.35 + TAIL 0.50` の合計 **256.5秒（202カット・414行）は
構造で決まっていて字数では動かない**。だから声が速くなると**尺だけが縮み、同じ字数でも 字/分 が上がる**。

| | 字数 | 尺 | 密度 |
|---|---:|---:|---:|
| 6本目（Hiro・TEMPO1.05） | 11,117 | 37:24 | 297字/分 |
| 7本目に 10,400字 を据え置くと | 10,400 | 約28:07 | **351字/分** ← 減らしても密になる |
| **7本目（Koichi・TEMPO1.0）** | **11,367** | **35:00** | **325字/分** |

→ 密度を動かせるのは **TEMPO だけ**。**1.0 はカズヤくんの決定**（2026-09-13）。
✅ TEMPO は**合成キャッシュの鍵に入っていない**＝あとで下げても **0クレジット**で焼き直せる。

🔴 **④の台本は「1文を短く」書く。**字数は9.3%増えるが、**1文あたりの情報は増やさない。**

### 8. 🔴 使った写真 67点のクレジット（⑤c' で差し替え・2026-09-14）

出どころ＝`python qa_out/ep7_assets.py credits` の後半（この表はその出力そのもの）。
⚠️ **CC BY は撮影者名が使用条件**なので、⑥の概要欄に**この表の「撮影者」をそのまま**載せる。
⚠️ 欄は **67**、表も **67行**（数が合っていることを必ず確かめてから貼る）。
　2026-09-14（⑤c'）に **13欄を差し替え、3欄を新設**した（`cabin_767` `f15_alert2` `security_screen`）。
　新設の3欄は「同じ写真を2カットで使い回して**画素の差が0**だった」組を割ったもの。
　⚠️ 同じ日に、この表を作る側が **Commons から引き直した欄の撮影年を入れ忘れていた**のも直した
　（差し替えた13欄のうち8欄が「不明」と出ていた。年は副題の主張と突き合わせる根拠そのもの）。
　2026-09-13 に、この表を作る側が**台帳に無い欄を黙って落としていた**のを直した
　（`andrews` の1行が消えて 63行になっていた。[[feedback-parsers-fail-closed]]）。
⚠️ `andrews` は撮影日 2019-06-06・**写っているのはラムシュタイン基地（ドイツ）**。
　c719 の副題はそれに合わせて直したが、**素材そのものは要差し替え**（⑤b-3 送り）。

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 元の題名 |
|---|---|---:|---|---|---|
| `manhattan_pre` | pr01 | 2001 | PD（Public domain） | Carol M. Highsmith | World Trade Center towers, New York, LCCN2015645969.jpg |
| `commute_pre` | c218 | 1993 | CC BY（CC BY 4.0） | Alex Lozupone | Downfolders-downfolder34-2011 02 02 00 10 05.jpg |
| `wtc_far` | c213 | 1976 | PD（Public domain） | Balthazar Korab | World Trade Center, New York. Exterior. Twilight view from harbor - LCCN2021636615.jpg |
| `wtc_twin` | c214 | 1971 | PD（Public domain） | Thomas J. O'Halloran | View of the New World Trade Center, 1971.jpg |
| `wtc_base` | c215 | 1976 | PD（Public domain） | Balthazar Korab | World Trade Center Exterior Entrance arches with Sphere at Plaza Fountain sculpture - LCCN2021638448.jpg |
| `wtc_south` | c311 | 1976 | PD（Public domain） | Balthazar Korab | World Trade Center, New York. Exterior. View from plaza - LCCN2020714989.jpg |
| `wtc_under` | c801 | 1976 | PD（Public domain） | Balthazar Korab | World Trade Center, New York. Exterior. Night view - LCCN2021636612.jpg |
| `lobby_pre` | pr05 | 1973 | CC BY（CC BY 3.0） | Euthman Ed Uthman | Memphis-international-airport-1970s.jpg |
| `security_pre` | c111 | 1970 | CC BY（CC BY 2.0） | Orange County Archives | Orange County Airport, security officer, Sept. 1970.jpg |
| `gate_pre` | c114 c204 | 2023 | PD（CC0） | Infrastorian | Boarding Southwest Airways B737-700 N242WN at Long Island MacArthur Airport, February 20, 2023.jpg |
| `fids_pre` | c320 | 2017 | PD（CC0） | Redolta | Departure Board at ORD.jpg |
| `logan` | c106 | 1973 | PD（Public domain） | Michael Philip Manheim | LOGAN AIRPORT-CONTROL TOWER AND RUNWAYS SEEN FROM 16TH FLOOR OBSERVATION DECK - NARA - 548428.jpg |
| `logan_apron` | c116 | 1969 | PD（Public domain） | Balthazar Korab | Eastern Air Lines terminal at Logan Airport, 1969.jpg |
| `logan_takeoff` | c115 | 2024 | CC BY（CC BY 4.0） | 4300streetcar | United 737-800 N73283 takeoff roll Boston Dec 2024.jpg |
| `dulles` | c107 | 1985 | PD（Public domain） | PH1 DAVID C. MACLEAN | Aerial view of Dulles Airport, June 1985.JPEG |
| `dulles_rwy` | c117 | 2025 | CC BY（CC BY 4.0） | Dclemens1971 | Aerial view of Dulles Airport 03.jpg |
| `reagan` | c415 | 2025 | CC BY（CC BY 4.0） | G. Edward Johnson | E Concourse DCA National Airport 2025-10-22 15-05-36 1.jpg |
| `newark_757` | c602 | 2017 | CC BY（CC BY 2.0） | airbus777 from Washington, DC, USA | United 757-200 at EWR (37116055471).jpg |
| `b767` | c108 | 2025 | CC BY（CC BY 4.0） | 4300streetcar | Delta Boeing 767-300ER N194DN at Boston May 2025.jpg |
| `b757` | c109 | 2024 | CC BY（CC BY 4.0） | 4300streetcar | Delta 757-200 N710TW taxiing at Boston Nov 2024.jpg |
| `b767_cruise` | c201 | 2024 | CC BY（CC BY 4.0） | 4300streetcar | Lufthansa A350-900 and United 767-300ER above Boston.jpg |
| `b767_takeoff` | c302 | 2012 | CC BY（CC BY 2.0） | Valentin Hintikka from Finland | N352AA (15113637598).jpg |
| `b757_takeoff` | c402 | 2025 | CC BY（CC BY 4.0） | 4300streetcar | Delta Boeing 757-200 N702TW departing Boston April 2025 1.jpg |
| `airliner_cruise` | c403 | 2012 | PD（CC0） | Downtowngal | Aircraft crossing paths.jpg |
| `refuel` | c119 | 2026 | CC BY（CC BY 4.0） | 4300streetcar | Fueling Boeing 757-200 N58101 at Boston January 2026.jpg |
| `cabin_pre` | c205 | 2017 | PD（CC0） | Suhyeon Choi choisyeon | Airplane aisle during flight (Unsplash).jpg |
| `cockpit_door_pre` | c202 | 2015 | CC BY（CC BY 2.0 de） | User:Mattes | Puerto Rico — A 320 JetBlue — Open cockpit door during boarding.jpg |
| `cabin_phone` | c614 | 2018 | CC BY（CC BY 2.0） | Delta News Hub | A220 Main Cabin (43799968340).jpg |
| `cabin_767` | c309 | 2011 | CC BY（CC BY 2.0） | Vincent Desjardins | Delta 767-400ER Economy Cabin.jpg |
| `cockpit_pre` | c605 | 2025 | CC BY（CC BY 4.0） | Funforme3 | Avelo Airlines B737 Cockpit.jpg |
| `window_cruise` | c304 | 2025 | CC BY（CC BY 4.0） | Sergey A. Demidov | 20250928 View from aircraft in Turkey 01 (31935).jpg |
| `window_sky` | c909 | 2025 | CC BY（CC BY 4.0） | Sergey A. Demidov | 20250928 View from aircraft in Egypt 01 (21624).jpg |
| `artcc_screen_pre` | pr09 | 不明 | PD（Public domain） | アメリカ連邦航空局（FAA） | AirTraffic-8.jpg |
| `radar_scope_pre` | c210 | 2016 | PD（Public domain） | Tekniska museet | SR&T Plan position indicator.jpg |
| `controller_pre` | c306 | 1987 | PD（Public domain） | Department of Defense. American Forces Information Service.  | Air traffic controllers of the 1961st Communications Group man their duty stations in the base tower. The 1961st recently won the Major General Harold M. McClelland Award for commun - DPLA - 6a16bbcae66aff3a8a8616188e1d2e07.jpeg |
| `artcc_screen2` | c509 | 2025 | PD（Public domain） | U.S. Air Force AFCENT by Staff Sgt. Shaei Rodriguez | 378th EOSS Air Traffic Controller Demonstration (8829390).jpg |
| `artcc_alt` | c608 | 2010 | PD（Public domain） | Master Sgt. Linda Miller | Kingpin and Controllers Maintain Aircraft and Airspace DVIDS265967.jpg |
| `artcc_seat` | ep03 | 2021 | PD（Public domain） | U.S. Space Force photo by Tech. Sgt. James Hodgman | ATC aids TBM Avenger pilot (6666391).jpeg |
| `pentagon_ext_pre` | c409 | 1998 | PD（Public domain） | DoD photo by Master Sgt. Ken Hammond, U.S. Air Force | The Pentagon US Department of Defense building.jpg |
| `pentagon_aerial_pre` | c410 | 1986 | PD（Public domain） | Department of Defense. American Forces Information Service.  | An aerial view of the Pentagon - DPLA - 2bad8af340141770c277509bf649c466.jpeg |
| `pentagon_court_pre` | c412 | 2025 | PD（Public domain） | Pfc. Jose Rolando Garcia | XQ-58A Valkrie displayed at the Pentagon Center Courtyard.jpg |
| `pentagon_west_day` | c421 | 2001 | PD（Public domain） | CPL JASON INGERSOLL, USMC | DM-SD-02-03925.JPEG |
| `f15_alert` | c123 | 2024 | PD（Public domain） | U.S. Air Force photo by Airman 1st Class Melany Bermudez | Fond Farewell to F-15C A5095 (8605970).jpg |
| `f15_alert2` | c702 | 2020 | PD（Public domain） | U.S. Air Force photo by Tech. Sgt. Michael Charles | A 494th EFS F-15E Strike Eagle sits on the flight line prior to a sortie at Prince Sultan Air Base.jpg |
| `f15_takeoff` | c703 | 2023 | PD（Public domain） | U.S. Air Force photo by Airman 1st Class Alexandria Byrd | 391st FS F-15E prepares for takeoff at MCAS Iwakuni during Northern Edge 23-2.jpg |
| `f16_alert` | c707 | 2024 | PD（Public domain） | U.S. Air Force USAFE by Capt. Jose Davis | F-16s Arrive at NATO Air Base Geilenkirchen (8403619).jpg |
| `f16_takeoff` | c711 | 2023 | PD（Public domain） | U.S. Air National Guard photo by Master Sgt. Caila Arahood | Colorado and Massachusetts Air National Guard fighter jets depart Lithuania during exercise Air Defender 2023 (7867984).jpg |
| `base_rwy` | c708 | 1967 | PD（Public domain） | Unknown author | Aerial view of Tan Son Nhut Air Base down main runway.jpg |
| `fighter_dc` | c717 | 2001 | PD（Public domain） | U.S. Air Force photo by Master Sgt. Don Taggart | F-16C NJ ANG in flight Oct 2001.jpg |
| `andrews` | c719 | 2019 | PD（Public domain） | U.S. Air Force photo by Tech. Sgt. Timothy Moore | 76th AS Last C-40 on ramp.jpg |
| `wtc_smoke_day` | c313 | 2001 | PD（Public domain） | Mike Goad | Skyline of Manhattan with smoke billowing from the Twin Towers (29385426736).jpg |
| `fire_trucks_day` | c314 | 2001 | PD（Public domain） | Anonymous. Courtesy of the Prints and Photographs Division.  | LOC unattributed Ground Zero photos, September 11, 2001 - item 210.jpg |
| `shanksville_day` | c622 | 2015 | CC BY（CC BY 3.0） | Ron Shawley | Flight 93 Memorial - panoramio (1).jpg |
| `apron_day` | pr10 | 2017 | CC BY（CC BY 2.0） | airbus777 from Washington, DC, USA | Southwest 737s parked at Terminal A at DCA (39815401742).jpg |
| `apron_lined_day` | c516 ep05 | 2026 | CC BY（CC BY 4.0） | 4300streetcar | At gate B24 at Boston Logan International Airport January 2026.jpg |
| `stopped_day` | c505 | 2023 | CC BY（CC BY 4.0） | 4300streetcar | United Boeing 737 at Gate B25 at Boston September 2023.jpg |
| `stranded_day` | c517 | 2017 | CC BY（CC BY 2.0） | Nelo Hotsuma | Philadelphia Airport Lounge (36335419103).jpg |
| `hearing` | c807 | 2012 | PD（Public domain） | Nuclear Regulatory Commission from US | Congressional Hearing - Jul. 24, 2012 (7748554726).jpg |
| `library_reports` | c815 | 2025 | CC BY（CC BY 4.0） | Bjankuloski06 | Books, Community Languages, Takapuna Library.jpg |
| `recorder` | c805 | 2019 | PD（Public domain） | National Transportation Safety Board | Miami Air Flight 293 flight recorder (32830135147).jpg |
| `atc_tape` | c803 | 2013 | CC BY（CC BY 2.0） | Robert Taylor from Stirling, ON, Canada | Studer B67 reel-to-reel audio tape recorder, ca. 1978 (cropped and edited, larger 10 inch tapes).jpg |
| `logbook` | c809 | 2023 | PD（CC0） | The History Wizard of Cambridge | Billy Strachan log book.jpg |
| `security_now` | c901 | 2016 | PD（CC0） | Rakoon | 0083 Domodedovo International Airport 16th of August 2016.jpg |
| `security_screen` |  | 2016 | PD（CC0） | AMISOM Public Information | 2016 04 19 Airport Security-5 (26744283185).jpg |
| `artcc_now` | c905 | 2025 | PD（Public domain） | U.S. Air Force AFCENT by Staff Sgt. Shaei Rodriguez | 378th EOSS Air Traffic Controller Demonstration (8829389).jpg |
| `lobby_now` | c907 | 2018 | PD（CC0） | Mr. Satterly | Gillette–Campbell County Airport terminal interior in Campbell County, Wyoming (2).jpg |
| `clear_sky` | ep01 | 2025 | CC BY（CC BY 4.0） | Sergey A. Demidov | 20250928 View from aircraft in Turkey 01 (79961).jpg |


## スペースシャトル・コロンビア号 空中分解事故（2003-02-01・8本目）

**2026-09-14（②素材の取り直し）に実測した。**写真74点は`qa_out/ep8_assets.py` の `PICK` が正本で、この表は`qa_out/ep8_credtable.py` が**機械で書き出している**（手で書かない）。

### 1. 写真74点 ── すべて NASA の職務著作（PD）

根拠＝**合衆国法典17編105条**。撮影機関（KSC／JSC／MSFC）は`tools/scene_jiko.py` の `EP8_PHOTO` が出典行に出す。
⚠️ **末尾に年を書いた欄は別の年・別の飛行**（`slf_landing` `slf_approach` `columbia_middeck` `cargo_tool`＝2002年／`oex_recorder`＝**1988年**）。副題で必ずその年を名乗ること。**門番は年の食い違いだけを見ていて、被写体の食い違いは見ない。**

⚠️ 使っていない欄が **15件** ある（`capcom` `crew_arrival` `crew_astrovan` `dittemore` `fd_cain` `fd_engelauf` `news_center` `orb_clark_husband` `orb_mccool` `recovery_team` `search_forest` `search_howell` `search_map` `suit_chawla` `test_panel2`）。②で落としたが置き場が無かったもの。**捨てていない。**

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | NASA の識別子 |
|---|---|---:|---|---|---|
| `pad_rss` | c104 c201 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0070 |
| `pad_stack` | c117 c203 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0076 |
| `et_orange` | c106 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0071 |
| `et_surface` | c108 c109 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0074 |
| `et_top` | c103 c219 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0075 |
| `launch_wide` | pr05 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0134 |
| `launch_flames` | c204 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0135 |
| `launch_sky` | c210 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Space Shuttle Projects |
| `strike_wide` | c205 c212 c302 c305 c306 pr07 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0242 |
| `strike_near` | c207 c208 c303 c309 c311 c312 c315 c515 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0243 |
| `crew_portrait` | pr03 | 2002 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2002e30459 |
| `crew_arrival` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0058 |
| `crew_astrovan` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0110 |
| `suit_chawla` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pp0144 |
| `suit_clark` | c202 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pp0145 |
| `orb_chawla` | c416 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Chawla smiles from the AFD of Columbia during STS-107 |
| `orb_husband` | c402 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Husband smiles for the camera beside Columbia's AFD control panel during STS-107 |
| `orb_husband_seat` | c215 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Husband seated in the CDR's seat on Columbia's FD during STS-107 |
| `orb_clark_arms` | c415 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Clark in the Spacehab RDM during activation of ARMS experiment equipment during STS-107 |
| `orb_chawla_hab` | c406 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Chawla in the Spacehab RDM during activation procedures during STS-107 |
| `orb_mccool` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | McCool works with Leukin activator cartridges on Columbia's MDK during STS-107 |
| `orb_chawla_clark` | c404 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Chawla and Clark in the Spacehab RDM during activation procedures on STS-107 |
| `orb_clark_husband` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Clark and Husband in the Spacehab RDM during activation procedures on STS-107 |
| `orb_clark_window` | c411 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Clark videotapes through an AFD window on Columbia during STS-107 |
| `orb_brown` | c408 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Brown in Columbia's FD/MDK access way during STS-107 |
| `orb_mccool_afd` | c501 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | McCool smiles for the camera from Columbia's AFD during STS-107 |
| `orb_ramon` | c405 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Ramon on Columbia's MDK during STS-107 |
| `orb_anderson` | c403 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Anderson smiles for the camera on Columbia's AFD during STS-107 |
| `orb_crew7` | c401 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-sts107-735-032 |
| `orb_anderson_read` | pr09 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-sts107-301-025 |
| `orb_earth` | c420 c703 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Space Shuttle Projects |
| `columbia_orbit` | c409 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e13222 |
| `mcc_launch` | c211 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e02609 |
| `mcc_feb1` | c721 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e03368 |
| `fd_cain` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e02610 |
| `capcom` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e02600 |
| `fd_engelauf` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e02611 |
| `search_line` | c806 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003-00151 |
| `search_brief` | c805 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003-00119 |
| `search_forest` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003-00127 |
| `search_queue` | c807 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e29065 |
| `search_map` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e28823 |
| `search_howell` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e26420 |
| `evidence_corsicana` | c803 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e28846 |
| `engine_dig` | c808 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e28147 |
| `engine_found` | c804 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e28148 |
| `barksdale` | c811 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e14383 |
| `hangar_floor` | c814 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd1070 |
| `hangar_grid` | c813 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0875 |
| `hangar_caib` | c816 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Columbia Accident Investigation Board |
| `hangar_exam` | c903 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Columbia Reconstruction Project Team |
| `le_fixture` | c815 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd1157 |
| `le_fixture2` | c709 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd1156 |
| `debris_truck` | c820 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Columbia Debris |
| `test_panel` | c907 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e40558 |
| `test_panel2` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e40593 |
| `test_hole` | c902 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e40715_nr |
| `caib_hearing` | c621 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0831 |
| `caib_gehman` | c901 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0836 |
| `report_copy` | c913 pr11 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e55050 |
| `report_copy2` | c620 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e55049 |
| `report_gehman` | c915 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e55047 |
| `report_mail` | c916 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | Columbia Accident Investigation Report |
| `ham_caib` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e09152 |
| `dittemore` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-jsc2003e31694 |
| `oex_recorder` | c707 c817 | 1988 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-s88-44993 |
| `slf_landing` | pr01 | 2002 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-sts109-s-013 |
| `slf_approach` | c730 | 2002 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-sts109-s-016 |
| `columbia_middeck` | c115 | 2002 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-s109e6032 |
| `cargo_tool` | c615 c619 | 2002 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | photo-s109e5386 |
| `atlantis_nose` | c603 c606 c609 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0369 |
| `atlantis_stack` | c607 c608 | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0372 |
| `recovery_team` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0270 |
| `news_center` |  | 2003 | PD（米連邦職員の職務著作・17 U.S.C. §105） |  | KSC-03pd0252 |

### 2. 動く映像9本

正本＝`ref/ep8/clips.json`（`tools/footage.py` の `CLIPS` が読む）。ショットの境目＝`ref/ep8/shots.json`（502ショット・1秒刻みの実測）。

| key | 出どころ | 権利の根拠 | 使うカット |
|---|---|---|---|
| `sts1` | NASA『STS-1 File Footage for 40th Anniversary』 | 米連邦職員の職務著作 | c101 c102 |
| `fd16` | NASA『STS-107 Entry Status Briefing Flight Day 16』 | 米連邦職員の職務著作 | c418 |
| `mc0201` | NASA『STS-107 Mission Control 02/01/2003』 | 米連邦職員の職務著作 | c622 c713 c727 |
| `fdcomm` | NASA『Flight Director Communications Loop』 | 米連邦職員の職務著作 | c701 c720 c724 |
| `mct` | NASA『STS-107 Mission Control & Telemetry 03/14/2003 Rev.5』 | 米連邦職員の職務著作 | c705 c711 c715 c717 |
| `guncam` | Commons『Shuttle Columbia Disaster gun camera footage』 | **NASA が2003-02-12に公開した録画**（§105）。⚠️ 残る不確かさは下記 | c725 |
| `tank` | NASA『Columbia Tank Found on Lakebed』 | 米連邦職員の職務著作 | ep01 ep02 |
| `cabin` | Commons『STS-107, final moments in cabin』 | 米連邦職員の職務著作 | **使わない**（⑤b-2 で外した） |
| `fdbrief` | NASA『2003-02-14 Entry Flight Director Briefing』 | 米連邦職員の職務著作 | 使わない（台本に置き場が無い） |

✅ **`guncam` の根拠は 2026-09-15（⑥）に Commons の原文を取り直して決着した**（カズヤくん判断＝**使う＋クレジットを直す**）。

Commons の説明文（原文）が言っているのは、こういう経路です。

> 2003年2月1日、フォートフッドで訓練中の**オランダ人パイロット2名**が AH-64D の搭載カメラで空中分解を記録した。事故の数日後、うち1名が**元の機密テープ**をバークスデール空軍基地にいた **NASA 職員**のところへ持って行き、職員は調査のために**その一部を録画することを許された**。**NASA の録画から作られた映像が、2003年2月12日に公開された。**

- ＝ **出回っている版は「NASA の録画」**。§105（米連邦職員の職務著作）で説明できるのは**この録画**です。
- → 画面の出典に**公開の経路を足した**：`出典：2003年2月1日 テキサス州フォートフッド／AH-64D の照準カメラの記録／NASA が同年2月12日に公開／パブリックドメイン`
- ⚠️ **不確かさは消えていません。**Commons の **Author 欄は空**で、札は §105 と **PDM 1.0** の2枚重ね（→ [[feedback-pd-label-hides-two-different-grounds]]＝1つに数えない）。**元の撮影者（オランダ人搭乗員）まで遡ると §105 では覆えません。**
- ⚠️ ②の実測では**空中分解そのものの映像はこの1本しか無い**（替えると図解になる）。その前提での判断です。
⚠️ `mct` は第三者の編集物だが、説明文に「Copyrighted portions … have been removed to maintain NASA Public-Domain status」とある。

✅ **`cabin` を外したままにすることは 2026-09-15（⑥）にカズヤくんが決めた。**（以下は⑤b-2 の経緯）
🔴 **`cabin` は⑤b-2 で外した。**640px のシートで中身を見たら、7人とも**再突入用の与圧服とヘルメット**を着けていた（10・45・270・375秒）。＝ 飛行11日目の絵ではなく **2月1日の再突入支度の絵**。台本 §1-2 が引いた線（再突入中の機内映像は画にも言葉にも出さない）の外側にある。

## テネリフェ空港衝突事故（1977-03-27・9本目）

**2026-09-16（⑤b-1）に実測した。**写真は `qa_out/ep9_assets.py` の `PICK` が正本で、この節は `python qa_out/ep9_assets.py credits --write` が**機械で書き出している**（手で書かない）。

### 1. 写真 126点 ── ウィキメディア・コモンズ（継承なし：CC0／PD／CC BY）

⚠️ **CC BY は撮影者名が使用条件**。⑥の概要欄には、この表の「撮影者」をそのまま載せる。
⚠️ **CC BY-SA・GFDL は1点も入れていない**（継承が動画全体に伝染する）。取得した権利表示で2回検査した。
⚠️ `losrodeos_now_*` `laspalmas_now_*` は**現在の空港**、`fog_laguna_*` は**2025年のラ・ラグーナの山地**、`cockpit_747_*` `engine_747_*` の多くは**博物館の保存機**。副題で必ず名乗る（[[feedback-fallback-stills-must-match-the-era]]）。**門番は年の食い違いだけを見ていて、被写体の食い違いは見ない。**
⚠️ いま画面に出しているのは **73点**（`使うカット` が空の欄は候補として落としただけ。捨てていない）。

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | Commons の題名 |
|---|---|---:|---|---|---|
| `wreck_klm_01` | c910 pr03 | 1977 | CC0 |  | Het verongelukte KLM-toestel De Rijn, Bestanddeelnr 929-1003.jpg |
| `wreck_klm_02` | c909 | 1977 | CC0 |  | Het verongelukte KLM-toestel De Rijn, Bestanddeelnr 929-1004.jpg |
| `wreck_klm_03` | c812 | 1977 | CC0 |  | Het verongelukte KLM-toestel De Rijn, Bestanddeelnr 929-1005.jpg |
| `wreck_both_01` | c813 c914 c917 | 1977 | CC0 |  | Eén de twee verongelukte toestellen, Bestanddeelnr 929-1006.jpg |
| `wreck_both_02` | c816 c912 c916 | 1977 | CC0 |  | Beeld van één van de twee verongelukte toestellen, Bestanddeelnr 929-1007.jpg |
| `wreck_engine_01` | c814 | 1977 | CC0 | Anefo | Vliegtuigmotor van één van de verongelukte jumbojets, Bestanddeelnr 929-1008.jpg |
| `panam_n736pa_01` | c103 | 不明 | CC BY（CC BY 2.0） | Rob Russell | Pan Am Boeing 747-121 N736PA at Sydney.jpg |
| `panam_ams1970_01` | c215 | 1970 | CC0 | Fotograaf Onbekend / Anefo, [onbekend] | De Boeing 747 aan de pier op het platform, Bestanddeelnr 923-6386.jpg |
| `panam_ams1970_02` | c208 | 1970 | CC0 | Anefo | De Boeing 747 zet de landing in, Bestanddeelnr 923-6390.jpg |
| `panam_ams1970_03` | c614 | 1970 | CC0 | Anefo | De Boeing 747 taxiet naar aankomstplaats op Schiphol, Bestanddeelnr 923-6398.jpg |
| `panam_747_same_type_01` | c115 | 1970 | PD（Public domain） | Karl Gritschke | Pan Am (Boeing 747).jpg |
| `panam_747_same_type_02` |  | 1970 | PD（Public domain） | Karl Gritschke | Pan Am Clipper B747-121.jpg |
| `panam_747_same_type_03` |  | 1975 | PD（Public domain） | 米国国立公文書館 | Photograph of President Gerald R. Ford Carrying a Vietnamese Baby from Clipper 1742, One of the Operation Babylift Planes that Transported Approximately 325 South Vietnamese Orphans from Saigon to the United State(...) - NARA - 7839930.jpg |
| `jumbo_era_01` | c101 | 1970 | PD（Public domain） | White House Photo Office | Pat Nixon christens Boeing 747 2749-18.jpg |
| `jumbo_era_02` | c119 | 1969 | CC0 | Anefo | Een model van een Boeing jumbo jet, Bestanddeelnr 922-6599.jpg |
| `jumbo_era_03` | c409 | 1969 | CC0 | Anefo | Een model van het interieur van een Boeing jumbo jet, Bestanddeelnr 922-6598.jpg |
| `jumbo_era_04` |  | 1969 | CC0 | Anefo | Een model van het interieur van een Boeing jumbo jet, Bestanddeelnr 922-6600.jpg |
| `jumbo_era_05` |  | 1970 | PD（Public domain） | White House photo office | Pat Nixon in first 747.png |
| `losrodeos_1930_01` | c301 | 1930 | CC BY（CC BY 2.0） | Iberia Airlines | Primer vuelo Península - Canarias (1930).jpg |
| `losrodeos_now_01` | c207 c302 | 2012 | CC BY（CC BY 3.0） | David Broad | Santa Cruz de Tenerife airport runway, Canary Islands, Spain - panoramio.jpg |
| `losrodeos_now_02` | c315 c519 c624 pr09 | 2012 | CC BY（CC BY 3.0） | David Broad | Santa Cruz de Tenerife airport runway, Canary Islands, Spain - panoramio (1).jpg |
| `losrodeos_now_03` | c515 | 2012 | CC BY（CC BY 3.0） | David Broad | Santa Cruz de Tenerife airport runway landing system, Canary Islands, Spain - panoramio.jpg |
| `losrodeos_now_04` | c309 | 2011 | CC BY（CC BY 2.0） | Santiago Atienza | Tenerife North Airport radar.jpg |
| `losrodeos_now_05` |  | 2011 | CC BY（CC BY 2.0） | Santiago Atienza | Bell 412SP aterrizando en el aeropuerto de Los Rodeos (Tenerife Norte).jpg |
| `losrodeos_now_06` | c212 c310 c906 | 2003 | CC BY（CC BY 2.5） | Guanxito2006 | Plataforma tfn.jpg |
| `losrodeos_now_07` | c209 c210 | 2003 | PD（Public domain） | Guanxito2006 | Terminal tfn.jpg |
| `losrodeos_now_08` | c606 c619 | 2009 | PD（Public domain） | Epp | Tenerife lennujaam.jpg |
| `laspalmas_now_01` | c202 | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Aeropuerto de Gran Canaria interior (5195390363).jpg |
| `laspalmas_now_02` |  | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Aeropuerto de Gran Canaria interior (5195391885).jpg |
| `laspalmas_now_03` |  | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Check-In Aeropuerto de Gran Canaria (5195973172).jpg |
| `laspalmas_now_04` |  | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Gates (5195996258).jpg |
| `laspalmas_now_05` |  | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Boarding (5196003292).jpg |
| `laspalmas_now_06` |  | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Busy traveller (5195388141).jpg |
| `laspalmas_now_07` | c120 | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Aeropuerto de Gran Canaria Tower (5195405623).jpg |
| `laspalmas_now_08` | c203 | 2012 | CC BY（CC BY 3.0） | hh oldman | Tower - panoramio (34).jpg |
| `laspalmas_now_09` | c308 | 2012 | CC BY（CC BY 3.0） | hh oldman | Airporttower(Cran Canaria) - panoramio.jpg |
| `laspalmas_now_10` |  | 2008 | CC BY（CC BY 3.0） | Kriki | Aeropuerto LPA Gran Canaria.jpg |
| `laspalmas_now_11` | c201 pr07 | 2010 | CC BY（CC BY 3.0） | Marc Ryckaert | Gran Canaria International Airport R01.jpg |
| `laspalmas_now_12` | c407 | 2013 | CC BY（CC BY 2.0） | oatsy40 | Planes (10136783155).jpg |
| `laspalmas_now_13` | c405 | 2012 | CC BY（CC BY 3.0） | hh oldman | In Reih und Glied - panoramio.jpg |
| `laspalmas_now_14` | c217 | 2012 | CC BY（CC BY 3.0） | hh oldman | Airport(Eingang) - panoramio.jpg |
| `laspalmas_now_15` |  | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Boarding aircraft (5195400705).jpg |
| `laspalmas_now_16` |  | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Boarding rear door (5195398367).jpg |
| `cockpit_747_01` |  | 2008 | CC BY（CC BY 2.0） | travelswiss | KLM Boeing 747 Cockpit.jpg |
| `engine_747_01` |  | 2010 | CC BY（CC BY 2.0） | Håkan Dahlström | Jet engine (5195403907).jpg |
| `nl_crisis_01` | ep04 | 1977 | CC0 | Bert Verhoeff for Anefo | Crisiscentrum te Amstelveen, Bestanddeelnr 929-0963.jpg |
| `nl_crisis_02` |  | 1977 | CC0 | Bert Verhoeff for Anefo | Crisiscentrum te Amstelveen, Bestanddeelnr 929-0964.jpg |
| `nl_crisis_03` | ep06 | 1977 | CC0 | Bert Verhoeff for Anefo | Overzicht crisiscentrum te Amstelveen, Bestanddeelnr 929-0965.jpg |
| `nl_crisis_04` | c918 | 1977 | CC0 | Bert Verhoeff / Anefo | Vlaggen halfstok voor het KLM-hoofdkantoor te Amstelveen, Bestanddeelnr 929-0961.jpg |
| `nl_crisis_05` |  | 1977 | CC0 | Bert Verhoeff for Anefo | President-directeur van KLM Orlandini staat de pers te woord, Bestanddeelnr 929-0962.jpg |
| `nl_mourning_01` | ep05 | 1977 | CC0 | Rob Croes / Anefo | 1 minuut stilte aan het begin van de herdenking, Bestanddeelnr 929-1118.jpg |
| `nl_mourning_02` |  | 1977 | CC0 | Rob Croes / Anefo | 1 minuut stilte aan het begin van de herdenking, Bestanddeelnr 929-1119.jpg |
| `nl_mourning_03` |  | 1977 | CC0 | Rob Croes for Anefo | Toespraak door de president-directeur van KLM, Sergio Orlandini, Bestanddeelnr 929-1120.jpg |
| `nl_mourning_04` |  | 1977 | CC0 | Fotograaf Onbekend / Anefo | Minister-president Den Uyl en minister Westerterp (Verkeer en Waterstaat) langs , Bestanddeelnr 929-1121.jpg |
| `nl_mourning_05` |  | 1977 | CC0 | Rob Croes for Anefo | Geëmotioneerde familieleden tijdens de dienst, Bestanddeelnr 929-1122.jpg |
| `nl_mourning_06` | ep01 | 1977 | CC0 | Rob Croes for Anefo | De kisten van de slachtoffers van de ramp, Bestanddeelnr 929-1123.jpg |
| `nl_mourning_07` |  | 1977 | CC0 | Rob Croes / Anefo | Aanwezigen verlaten de hal aan het einde van de dienst, Bestanddeelnr 929-1124.jpg |
| `nl_mourning_08` |  | 1977 | CC0 | Rob Croes for Anefo | Aanwezigen verlaten de hal aan het einde van de dienst, Bestanddeelnr 929-1125.jpg |
| `nl_mourning_09` |  | 1977 | CC0 | Rob Croes for Anefo | Slachtoffers, herdenkingen, vliegtuigongevallen, rampen, Bestanddeelnr 929-1126.jpg |
| `nl_mourning_10` | ep02 | 1977 | CC0 | Fotograaf Onbekend / Anefo | Tweede Kamer neemt voor het debat een minuut stilte in acht voor de slachtoffers, Bestanddeelnr 929-0988.jpg |
| `nl_funeral_01` |  | 1977 | CC0 | Fotograaf Onbekend / Anefo | Stoet trekt langs de kisten, Bestanddeelnr 929-1130.jpg |
| `nl_funeral_02` |  | 1977 | CC0 | Fotograaf Onbekend / Anefo | Stoet trekt langs de kisten, Bestanddeelnr 929-1131.jpg |
| `nl_funeral_03` |  | 1977 | CC0 | Fotograaf Onbekend / Anefo | Burgemeester Ivo Samkalden van Amsterdam legt een herdenkingskrans, Bestanddeelnr 929-1132.jpg |
| `nl_funeral_04` |  | 1977 | CC0 | Bert Verhoeff / Anefo | Stoet trekt langs de kisten, Bestanddeelnr 929-1133.jpg |
| `nl_funeral_05` |  | 1977 | CC0 | Fotograaf Onbekend / Anefo | Burgemeester Ivo Samkalden van Amsterdam loopt langs de kisten, Bestanddeelnr 929-1134.jpg |
| `nl_funeral_06` | ep03 | 1977 | CC0 | Fotograaf Onbekend / Anefo | Burgemeester Ivo Samkalden van Amsterdam na de kranslegging, Bestanddeelnr 929-1135.jpg |
| `schiphol_1977_01` | c105 pr05 | 1977 | CC0 | Nederlandse Spoorwegen | HUA-170857-Gezicht op de vertrekhal Noord van de luchthaven Schiphol, vanaf de hal van het in aanbouw zijnde N.S.-station Schiphol.jpg |
| `schiphol_1977_02` |  | 1977 | CC0 | Bert Verhoeff / Anefo | Proef met gescheiden paspoortcontrole op Schiphol bord in aankomsthal wijst r, Bestanddeelnr 929-2655.jpg |
| `schiphol_1977_03` |  | 1978 | CC0 | Fernando Pereira / Anefo | Vliegtuigkijkers bij Schiphol, Bestanddeelnr 929-9386.jpg |
| `memorial_01` | ep07 | 2015 | CC0 | Jesús Manuel Pérez Triana | International Tenerife Memorial March 27, 1977.jpg |
| `memorial_02` | ep08 | 2015 | CC0 | Jesús Manuel Pérez Triana | Memorial plaque at International Tenerife Memorial March 27, 1977.jpg |
| `memorial_03` | ep10 | 2009 | PD（Public domain） | Gotmarcus | TenerifeMemorial.JPG |
| `memorial_04` |  | 2011 | CC0 | NaturalHeaven1979 | VvZ Westgaarde.jpg |
| `losrodeos_now_09` | c507 c522 pr01 | 2007 | CC0 | Arrebar | A340-tenerifenorth.JPG |
| `losrodeos_now_10` | c305 c511 | 2009 | CC BY（CC BY 2.0） | George from Spain | Tenerife North Airport.jpg |
| `losrodeos_now_11` | c218 c518 c719 | 2009 | CC BY（CC BY 2.0） | George from Spain | Tenerife North Airport (2).jpg |
| `losrodeos_now_12` | c319 c701 | 2011 | CC BY（CC BY 2.0） | Santiago Atienza | Airbus 340-600 EC-IZX de Iberia landing in Los Rodeos airport.jpg |
| `losrodeos_now_13` | c521 c903 | 2013 | CC BY（CC BY 2.0） | Santiago Atienza | EC-JBJ (8663466023).jpg |
| `losrodeos_now_14` | c213 c307 | 2013 | CC BY（CC BY 2.0） | Santiago Atienza | EC-LKH (8667167560).jpg |
| `losrodeos_now_15` |  | 2013 | CC BY（CC BY 2.0） | Santiago Atienza | EC-LKH (8666109731).jpg |
| `losrodeos_now_16` |  | 2013 | CC BY（CC BY 2.0） | Santiago Atienza | EC-IDA (8663483661).jpg |
| `losrodeos_now_17` | c806 | 2013 | CC BY（CC BY 2.0） | Santiago Atienza | EI-EBW (8667219504).jpg |
| `losrodeos_now_18` | c810 | 2011 | CC BY（CC BY 2.0） | Santiago Atienza | Luke SkyVueling.jpg |
| `fog_laguna_01` | c901 | 2025 | CC BY（CC BY 4.0） | Flocci Nivis | 20250702 Mirador de Jardina 01.jpg |
| `fog_laguna_02` | c503 | 2025 | CC BY（CC BY 4.0） | Flocci Nivis | 20250702 Mirador de Jardina 02.jpg |
| `fog_laguna_03` |  | 2025 | CC BY（CC BY 4.0） | Flocci Nivis | 20250702 Mirador de Jardina 03.jpg |
| `fog_laguna_04` |  | 2025 | CC BY（CC BY 4.0） | Flocci Nivis | 20250702 Mirador de Jardina 04.jpg |
| `fog_laguna_05` | c501 | 2025 | CC BY（CC BY 4.0） | Flocci Nivis | 20250702 Mirador de Jardina 05.jpg |
| `fog_laguna_06` |  | 2024 | CC0 | Clemenspool | Mountains Tenerife north.jpg |
| `cockpit_747_02` | c111 | 1971 | CC0 | W. Punt for Anefo | Vlucht met Boeing 747 naar Rome van Schiphol cockpit, Bestanddeelnr 924-3165.jpg |
| `cockpit_747_03` | c107 | 1971 | CC0 | W. Punt for Anefo | Vlucht met Boeing 747 naar Rome van Schiphol cockpit, Bestanddeelnr 924-3166.jpg |
| `cockpit_747_04` | c419 | 1971 | CC0 | W. Punt for Anefo | Vlucht met Boeing 747 naar Rome van Schiphol, Bestanddeelnr 924-3167.jpg |
| `cockpit_747_05` |  | 1970 | CC0 | Joost Evers / Anefo | Vliegtrainingsgebouw KLM op Schiphol-Oost geopend interieur van cockpit Boeing , Bestanddeelnr 923-9767.jpg |
| `cockpit_747_06` |  | 1970 | PD（Public domain） | Robert LeRoy Knudsen | Mrs. Nixon visits the cockpit of the first commercial Boeing 747 jet in conjunction with the christening ceremony for... - NARA - 194665.tif |
| `cockpit_747_07` | c801 | 2013 | CC BY（CC BY 2.0） | Roel Hemkes | Boeing 747-206SUD flightdeck (9649946519).jpg |
| `cockpit_747_08` |  | 2013 | CC BY（CC BY 2.0） | kitmasterbloke | F-BPVJ cockpit, Air France Boeing 747-128.jpg |
| `cockpit_747_09` | c710 | 2007 | PD（Public domain） | Snowdog | B747-cockpit.jpg |
| `cockpit_747_10` | c731 | 2008 | PD（Public domain） | Leftright | B747-200SF FE Panel.JPG |
| `cockpit_747_11` | c725 | 2015 | CC0 | Daderot | Cockpit of Boeing 747-136, serial 20269, registration number G-AWNG, first flight in March 1971, last flight December 1998 - Hiller Aviation Museum - San Carlos, California - DSC03315.jpg |
| `cockpit_747_12` |  | 2015 | CC0 | Daderot | Cockpit of Boeing 747-136, serial 20269, registration number G-AWNG, first flight in March 1971, last flight December 1998 - Hiller Aviation Museum - San Carlos, California - DSC03318.jpg |
| `cockpit_747_13` |  | 2015 | CC0 | Daderot | Cockpit of Boeing 747-136, serial 20269, registration number G-AWNG, first flight in March 1971, last flight December 1998 - Hiller Aviation Museum - San Carlos, California - DSC03319.jpg |
| `cockpit_747_14` |  | 2010 | PD（Public domain） | Lance Cheung | E-4B cockpit.jpg |
| `cockpit_747_15` | c704 | 2012 | PD（Public domain） | NASA/Tim Jacobs | Cockpit of Shuttle Carrier Aircraft 905 (KSC-2012-2185).jpg |
| `cockpit_747_16` | c622 | 1973 | CC BY（CC BY 4.0） | Willy Pragher | Frankfurt- Flughafen; Jumbo-Jet; Cockpit - LABW - Staatsarchiv Freiburg W 134 Nr. 098695.jpeg |
| `cockpit_747_17` | c114 | 1989 | CC BY（CC BY 4.0） | Peter Nath | 1989 05 11 B747 121 LX FCV LO AF flt deck mid atlantic.jpg |
| `engine_747_02` | c403 | 2017 | CC0 | Daderot | Pratt & Whitney JT9D-7 turbofan engine, 1970 - Evergreen Aviation & Space Museum - McMinnville, Oregon - DSC00895.jpg |
| `engine_747_03` |  | 2014 | CC0 | Alf van Beem | Pratt & Whitney JT9D (1969) used in Boeing 747 at Flugausstellung Hermeskeil, pic1.JPG |
| `engine_747_04` |  | 2014 | CC0 | Alf van Beem | Pratt & Whitney JT9D (1969) used in Boeing 747 at Flugausstellung Hermeskeil, pic2.JPG |
| `engine_747_05` | c321 | 2010 | PD（Public domain） | Stickpen | Cityofeverett-engine.jpg |
| `panam_ams1970_04` | pr02 | 1970 | CC0 | Fotograaf Onbekend / Anefo, [onbekend] | De Boeing 747 wordt door een batsman naar een juiste positie op het platform van, Bestanddeelnr 923-6393.jpg |
| `panam_ams1970_05` | c314 | 1970 | CC0 | Fotograaf Onbekend / Anefo, [onbekend] | Onder een Hollandse wolkenlucht is de Boeing 747 Jumbo-jet op het platform Schip, Bestanddeelnr 923-6389.jpg |
| `panam_ams1970_06` | c311 | 1970 | CC0 | Fotograaf Onbekend / Anefo, [onbekend] | Op het platform van Schiphol kan de Boeing 747 tijdens het uitladen op grote bel, Bestanddeelnr 923-6388.jpg |
| `panam_ams1970_07` |  | 1970 | CC0 | Fotograaf Onbekend / Anefo, [onbekend] | De Boeing 747 aan de pier op het platform, Bestanddeelnr 923-6395.jpg |
| `panam_ams1970_08` |  | 1970 | CC0 | Anefo | De Boeing 747 aan de pier op het platform, Bestanddeelnr 923-6396.jpg |
| `panam_ams1970_09` |  | 1970 | CC0 | Fotograaf Onbekend / Anefo, [onbekend] | De Boeing 747 net voor de landing op Schiphol, Bestanddeelnr 923-6399.jpg |
| `panam_ams1970_10` | c808 | 1970 | CC0 | Anefo | De Boeing 747 landt op Schiphol, Bestanddeelnr 923-6392.jpg |
| `klm_747_1971_01` | c102 c420 | 1971 | CC0 | Bert Verhoeff / Anefo | Eerste Jumbo-Jet Boeing 747 B , van KLM arriveert op Schiphol KLM-Jumbo Jet, Bestanddeelnr 924-2251.jpg |
| `klm_747_1971_02` |  | 1971 | CC0 | Bert Verhoeff / Anefo | Eerste Jumbo-Jet Boeing 747 B , van KLM arriveert op Schiphol KLM-Jumbo Jet, Bestanddeelnr 924-2252.jpg |
| `wing_747_1972_01` |  | 1972 | CC0 | Bert Verhoeff / Anefo | KLM bouwt geluidsmuur rond platform waar wordt proef gedraaid de geluidsmuur , Bestanddeelnr 925-3335.jpg |
| `klm_747_1973_01` | c401 c416 c601 | 1973 | CC0 | Anefo | De gekaapte Jumbo is terugekeerd op Schiphol, Bestanddeelnr 926-8612.jpg |
| `panam_747_same_type_04` |  | 1970 | CC0 | Rob Mieremet / Anefo | Amerikaanse Luchtvaartmij Pan Am gaat 27 op Amsterdam vliegen met een 747 voo, Bestanddeelnr 923-5862.jpg |
| `panam_747_same_type_05` | c112 | 1974 | CC BY（CC BY 3.0） | Piergiuliano Chesi | Pan American World Airways Boeing 747 N750PA 01.jpg |
| `panam_747_same_type_06` | c113 | 1973 | PD（Public domain） | Arthur Tress | AT THE JOHN F. KENNEDY AIRPORT - NARA - 547951.jpg |
| `panam_747_same_type_07` | c116 | 1984 | CC BY（CC BY 2.0） | Kambui | Pan American World Airways - Pan Am Boeing 747-121 N732PA "Clipper Ocean Telegraph" (29935660081).jpg |
| `panam_747_same_type_08` |  | 1983 | CC BY（CC BY 2.0） | Kambui | Pan American World Airways - Pan Am Boeing 747-121 N754PA "Clipper Ocean Rover" (24059638596).jpg |
| `canary_iss_01` |  | 2009 | PD（Public domain） | NASA ジョンソン宇宙センター | ISS020-E-21144 - View of the Canary Islands.jpg |

## 三豊百貨店崩壊事故（1995-06-29・10本目）

**2026-09-20（⑤b-1）に実測した。**写真は `qa_out/ep10_assets.py` が正本で、この節は `python qa_out/ep10_assets.py credits --write` が**機械で書き出している**（手で書かない）。

### 1. 写真 92点（CC BY-SA 4.0 82点 ／ 公共ヌリ第1類型 10点）

🔴🔴 **CC BY-SA の点は額装でだけ使っている**（無加工・丸ごと・色を変えない・何も重ねない）。
　　継承は翻案物を共有するときだけ掛かるので、**動画を BY-SA にする必要はない**
　　（許諾 3(b)・1(a)・2(a)(4)／CC 公式 ShareAlike_interpretation。`ref/ep10/materials.md` §1 に原文）。
　　⚠️ 切る・色を変える・上に重ねると翻案になる。**止める仕掛け＝`cuts/ss.py` の `FRAME_ONLY`**。
⚠️ **BY-SA の表示に要るのは4つ**＝撮影者・許諾名と URL・素材の URL・**改変していないこと**。
　　画面の隅には「出典：撮影者／CC BY-SA 4.0（無改変）」だけを出し、URL はこの表と⑥の概要欄で出す。
⚠️ 撮影者名の原語はハングル。画面は片仮名にしている（`WHO_JA`）。個人名の読みは機械的な転写で、当人の名乗りではない。
⚠️ いま画面に出しているのは **0点**（`使うカット` が空の欄は候補として落としただけ。捨てていない）。

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 素材の題名 |
|---|---|---:|---|---|---|
| `sampoong_before_01` |  | 1995 | KOGL Type 1 + CC BY 4.0（手直し可） | ソウル特別市／ソウル研究院 | 삼풍백화점(붕괴전) 1995/6 · 01O01101Db8000 |
| `sampoong_before_02` |  | 1995 | KOGL Type 1 + CC BY 4.0（手直し可） | ソウル特別市／ソウル研究院 | 삼풍백화점(붕괴전) 1995/6 · 01O01102Db1000 |
| `sign_sampoong_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept25.jpg |
| `sign_sampoong_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept43.jpg |
| `sign_sampoong_03` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고110.jpg |
| `sign_sampoong_04` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고60.jpg |
| `sign_sampoong_05` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고82.jpg |
| `sign_sampoong_06` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고96.jpg |
| `sign_sampoong_07` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고51.jpg |
| `wreck_aerial_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 1995년 6월 29일 삼풍백화점 붕괴 사고 7.jpg |
| `wreck_aerial_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept26.jpg |
| `wreck_aerial_03` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept29.jpg |
| `wreck_aerial_04` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept45.jpg |
| `wreck_aerial_05` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept53.jpg |
| `wreck_aerial_06` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept07.jpg |
| `wreck_aerial_07` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept47.jpg |
| `wreck_aerial_08` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept56.jpg |
| `wreck_aerial_09` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고102.jpg |
| `wreck_aerial_10` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고97.jpg |
| `wreck_aerial_11` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 1995년 6월 29일 삼풍백화점 붕괴 사고 3.jpg |
| `wreck_ground_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept03.jpg |
| `wreck_ground_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept36.jpg |
| `wreck_ground_03` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept40.jpg |
| `wreck_ground_04` |  | 1995 | KOGL Type 1（手直し可） | ソウル歴史編纂院 | 처참한 모습을 드러낸 삼풍백화점 붕괴현장(1995.6.30) |
| `wreck_ground_05` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고138.jpg |
| `wreck_ground_06` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고140.jpg |
| `wreck_ground_07` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고144.jpg |
| `wreck_ground_08` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고162.jpg |
| `wreck_ground_09` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고165.jpg |
| `wreck_ground_10` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고21.jpg |
| `wreck_ground_11` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고64.jpg |
| `wreck_ground_12` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고84.jpg |
| `wreck_ground_13` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고91.jpg |
| `column_broken_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept21.jpg |
| `column_broken_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept34.jpg |
| `column_broken_03` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고166.jpg |
| `column_broken_04` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고170.jpg |
| `column_broken_05` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고175.jpg |
| `column_broken_06` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고177.jpg |
| `column_broken_07` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고178.jpg |
| `rescue_work_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept01.jpg |
| `rescue_work_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept02.jpg |
| `rescue_work_03` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept06.jpg |
| `rescue_work_04` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept08.jpg |
| `rescue_work_05` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept09.jpg |
| `rescue_work_06` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept10.jpg |
| `rescue_work_07` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept12.jpg |
| `rescue_work_08` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept22.jpg |
| `rescue_work_09` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept27.jpg |
| `rescue_work_10` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept31.jpg |
| `rescue_work_11` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept33.jpg |
| `rescue_work_12` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept35.jpg |
| `rescue_work_13` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept41.jpg |
| `rescue_work_14` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept46.jpg |
| `rescue_work_15` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept48.jpg |
| `rescue_work_16` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept50.jpg |
| `rescue_work_17` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept51.jpg |
| `rescue_work_18` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept52.jpg |
| `rescue_work_19` |  | 1995 | KOGL Type 1（手直し可） | ソウル歴史編纂院 | 삼풍백화점 붕괴현장의 구조활동(1995.6) |
| `rescue_work_20` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고41.jpg |
| `rescue_work_21` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고44.jpg |
| `rescue_work_22` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고47.jpg |
| `rescue_work_23` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고65.jpg |
| `ambulance_line_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept17.jpg |
| `ambulance_line_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept28.jpg |
| `ambulance_line_03` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept15.jpg |
| `ambulance_line_04` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept23.jpg |
| `ambulance_line_05` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept13.jpg |
| `ambulance_line_06` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고70.jpg |
| `street_cordon_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept24.jpg |
| `street_cordon_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고159.jpg |
| `street_cordon_03` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고69.jpg |
| `street_cordon_04` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고71.jpg |
| `street_cordon_05` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고79.jpg |
| `volunteers_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept32.jpg |
| `volunteers_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고156.jpg |
| `inside_store_01` |  | 1995 | KOGL Type 1（手直し可） | ソウル歴史編纂院 | 건물 붕괴 충격으로 아수라장이 된 삼풍백화점 본관 1층 현관 가판대(1995.6) |
| `site_cleanup_01` |  | 1995 | KOGL Type 1（手直し可） | ソウル歴史編纂院 | 삼풍백화점 붕괴현장 정리와 구조활동(1995.6) |
| `site_cleanup_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | チェ・グァンモ | Sampungdept37.jpg |
| `site_cleanup_03` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고13.jpg |
| `site_cleanup_04` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고6.jpg |
| `site_cleanup_05` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고89.jpg |
| `site_cleanup_06` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고85.jpg |
| `banner_daily_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고152.jpg |
| `banner_daily_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고81.jpg |
| `crack_wall_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고72.jpg |
| `night_work_01` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 19950629삼풍백화점 붕괴 사고26.jpg |
| `night_work_02` |  | 1995 | CC BY-SA 4.0（額装のみ・無改変） | ソウル特別市 消防災難本部 | 1995년 6월 삼풍백화점 붕괴 사고 6 서울특별시 소방공무원 현철호 민원석 등.jpg |
| `mourning_01` |  | 1995 | KOGL Type 1（手直し可） | ソウル歴史編纂院 | 서초구민회관에 마련된 삼풍참사 사망자 합동분향소(1995.7) |
| `missing_board_01` |  | 1995 | KOGL Type 1（手直し可） | ソウル歴史編纂院 | 삼풍백화점 사고 피해자를 찾는 벽보(1995.6) |
| `officials_visit_01` |  | 1995 | KOGL Type 1（手直し可） | ソウル歴史編纂院 | 시장 업무 인수 직후 삼풍백화점 현장을 찾은 조순 시장(1995.7.1) |
| `officials_visit_02` |  | 1995 | KOGL Type 1（手直し可） | ソウル歴史編纂院 | 4대 시의회 의장단 삼풍백화점 구조현장 방문(1995.7.12) |

---

## スペースシャトル・チャレンジャー号 空中分解事故（1986-01-28・11本目）　※2026-09-21（⑤c-2）

**この回は継承（ShareAlike）つきの素材を1点も使っていません**（10本目とは判断が違います）。
内わけ＝**写真 56点**（Commons の PD ＋ NASA 画像庫 §105）＋**動く映像からの止め絵 20点**。

🔴 **動く映像から抜いた止め絵は、写真ではなく映像の出典を名乗ります**（出所を偽らないため）。
   もとは2本＝NASA 記録映画「Space Shuttle Challenger Accident Investigation」（44分44秒）と、
   米国立公文書館／USIA「REPORT ON THE SPACE SHUTTLE CHALLENGER ACCIDENT - KEEL, 1986」
   （Local ID **306-WNET-239**・米連邦 §105）。

⚠️ **この表は手で書いていません。**`python qa_out/ep11_assets.py credits` が
   `ref/ep11/assets.json`（置き場に引き直した実測）と `cuts.SPEC` から書き出したものです。
⚠️ 撮影者が「不明」と返ってくる2点（`ascent_1`・`ice_team`）は、**NASA と名乗らせていません**。

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころ |
|---|---|---:|---|---|---|
| `accident_breakup` | pr03 | 1986 | Public domain | NASA | Challenger explosion.jpg |
| `ascent_1` | c315 | 1986 | Public domain | NASA | 70mm frame of Challenger during ascent.png |
| `ascent_2` | c316 | 1986 | Public domain | NASA | Challenger - GPN-2000-001347.jpg |
| `astronaut_manager` | ep08 | 1986 | Public domain (17 U.S.C. §105) | NASA | Members of the Presidential commission on Challenger accident arrive at KSC |
| `breakup_moment` | c322 | 1986 | Public domain | NASA | Challenger breakup.jpg |
| `breakup_sections` | c410 | 1986 | Public domain | NASA | Shuttle Destruction - GPN-2000-001423.jpg |
| `commission_hearing` | c911 | 1986 | Public domain (17 U.S.C. §105) | 米国立公文書館 | 記録映像 commission +2秒 |
| `commission_hearing_2` | c710 | 1986 | Public domain (17 U.S.C. §105) | 米国立公文書館 | 記録映像 commission +10秒 |
| `commission_members` | c912 | 1986 | Public domain (17 U.S.C. §105) | 米国立公文書館 | 記録映像 commission +14秒 |
| `commission_oversight` | ep05 | 1986 | Public domain (17 U.S.C. §105) | NASA | PRESIDENTIAL COMMISSION - STS-33/51L - KSC |
| `commission_report` | ep01 | 1986 | Public domain (17 U.S.C. §105) | ロジャース委員会報告書 | Internet Archive: reporttopreside00unit / cover |
| `commission_room` | c819 | 1986 | Public domain (17 U.S.C. §105) | 米国立公文書館 | 記録映像 commission +12秒 |
| `commission_testimony` | c709 | 1986 | Public domain (17 U.S.C. §105) | 米国立公文書館 | 記録映像 commission +6秒 |
| `crew_breakfast` | c215 | 1986 | Public domain | NASA | STS-51-L preflight breakfast.jpg |
| `crew_flightline` | ep11 | 1986 | Public domain (17 U.S.C. §105) | NASA | STS 51-L crewmembers at Ellington AFB for training flight in T-38 |
| `crew_jarvis` | c207 | 1985 | Public domain (17 U.S.C. §105) | NASA | Official portrait Gregory Jarvis STS 51-L payload specialist |
| `crew_mcnair` | c206 | 1985 | Public domain (17 U.S.C. §105) | NASA | Portrait - Astronaut McNair, Ronald E. |
| `crew_onizuka` | c204 | 1986 | Public domain (17 U.S.C. §105) | NASA | Portrait - Astronaut Onizuka, Ellison S. |
| `crew_portrait` | pr05 | 1985 | Public domain | NASA | Challenger flight 51-l crew.jpg |
| `crew_portrait_2` | 🔴未使用 | 1985 | Public domain (17 U.S.C. §105) | NASA | Official Portrait - STS-51L Crewmembers |
| `crew_portrait_3` | 🔴未使用 | 1986 | Public domain | NASA | 722342main challenger full full.jpg |
| `crew_resnik` | c205 | 1978 | Public domain | NASA | Judith A. Resnik, official portrait.jpg |
| `crew_scobee` | c202 | 1978 | Public domain | NASA | Francis Richard Scobee.jpg |
| `crew_smith` | c203 | 1981 | Public domain | NASA | Michael Smith (NASA).jpg |
| `crew_training` | c201 | 1986 | Public domain (17 U.S.C. §105) | NASA | STS 51-L crewmembers briefed during training session |
| `crew_whiteroom` | c216 | 1986 | Public domain | NASA | 51-L Challenger Crew in White Room - GPN-2000-001867.jpg |
| `debris_et` | c909 | 1986 | Public domain | NASA | STS-51-L Recovered Debris (ET and SRBs) - GPN-2004-00003.jpg |
| `debris_hangar` | c902 | 1986 | Public domain | NASA | ChallengerRemains.jpg |
| `et_breach` | c320 | 1986 | Public domain | NASA | LOX Tank Rupture - GPN-2000-001426.jpg |
| `fb_c101` | c101 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 pad +44秒 |
| `fb_c307` | c307 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 smoke +11秒 |
| `fb_c413` | c413 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 accident +49秒 |
| `fb_c503` | c503 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 joint +42秒 |
| `fb_c603` | c603 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 srb +36秒 |
| `fb_pr02` | pr02 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 launch +19秒 |
| `fb_pr07` | pr07 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 joint +30秒 |
| `fireball` | c406 | 1986 | Public domain | NASA | Challenger explosion (cropped).jpg |
| `fireball_wide` | c401 | 1986 | Public domain | NASA | SPACE SHUTTLE CHALLENGER DISASTER 1986 UNCORRECTED COLOR 20211117142954!Challenger explosion.jpg |
| `flag_half_mast` | c915 | 1986 | Public domain (17 U.S.C. §105) | NASA | Flags at half-staff in memorial of STS 51-L crewmembers |
| `flame_plume` | c317 | 1986 | Public domain | NASA | Booster Rocket Breach - GPN-2000-001425.jpg |
| `flame_plume_2` | c318 | 1986 | Public domain | NASA | Challenger 58 sec.jpg |
| `frustum_compare` | c907 | 1986 | Public domain | NASA | STS-51-L Recovered Debris (Forward Skirt) - GPN-2004-00006.jpg |
| `hydrogen_burn` | c403 | 1986 | Public domain | NASA | Challenger explosion (cropped).jpg |
| `ice_box` | c109 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 t_ice +18秒 |
| `ice_egress` | c108 | 1986 | Public domain (17 U.S.C. §105) | NASA | View of ice on the launch complex |
| `ice_icicle` | pr01 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 t_ice +14秒 |
| `ice_icicle_2` | c107 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 t_ice +23秒 |
| `ice_pad` | pr09 | 1986 | Public domain | NASA | Ice on the Pad on the Day of STS-51-L's Launch - GPN-2004-00011.jpg |
| `ice_team` | c110 | 1986 | Public domain | 米国立公文書館 | Photograph of Space Shuttle Ice and Frost Inspection - NARA - 593693.gif |
| `ice_trough` | c105 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 t_ice +9秒 |
| `joint_qual_test` | c804 | 1987 | Public domain (17 U.S.C. §105) | MSFC | Space Shuttle Projects |
| `joint_redesign` | ep02 | 1988 | Public domain (17 U.S.C. §105) | MSFC | Space Shuttle Project |
| `joint_test` | c513 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 joint +22秒 |
| `joint_test_new` | ep03 | 1988 | Public domain (17 U.S.C. §105) | MSFC | Space Shuttle Projects |
| `launch_51c` | c605 | 1985 | Public domain | NASA | STS-51C launch.jpg |
| `launch_pad_morning` | c301 | 1986 | Public domain | NASA | STS-51-L.jpg |
| `marshall_center` | c613 | 2013 | Public domain | NASA | Marshall Space Flight Center Bldg. 4200.jpg |
| `mcauliffe_class` | c208 | 1985 | Public domain (17 U.S.C. §105) | NASA | Official portrait Sharon Christa McAuliffe, STS 51-L Teacher in Space |
| `mcauliffe_morgan` | c211 | 1985 | Public domain | NASA | Christa McAuliffe and Barbara Morgan - GPN-2002-000004.jpg |
| `mcauliffe_training` | c209 | 1986 | Public domain | NASA | Christa McAuliffe in Training (28698549073).jpg |
| `memorial_service` | c913 | 1986 | Public domain (17 U.S.C. §105) | NASA | View of the STS 51-L Memorial service on JSC's main mall |
| `memorial_wreath` | ep10 | 1986 | Public domain (17 U.S.C. §105) | NASA | Barbara Morgan, 51-L backup payload specialist, at Memorial service |
| `mmt_meeting` | c116 | 1986 | Public domain | NASA | STS-51L riadiace stredisko.jpg |
| `mulloy_testimony` | c812 | 1986 | Public domain (17 U.S.C. §105) | NASA | Presidential commission investigating Challenger accident at JSC |
| `oring_channel` | c522 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 joint +22秒 |
| `oring_erosion` | c805 | 1986 | Public domain | NASA | STS-51-L Recovered Debris (Burn Marks on the SRM) - GPN-2004-00004.jpg |
| `oring_erosion_photo` | c705 | 1986 | Public domain | NASA | STS-51-L Recovered Debris (O-Ring Tracks on Right SRB Joint) - GPN-2004-00010.jpg |
| `oring_physical` | c506 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 joint +17秒 |
| `oring_resilience_test` | c517 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 joint +58秒 |
| `oring_soot` | c606 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 joint +16秒 |
| `past_launch` | c313 | 1984 | Public domain (17 U.S.C. §105) | NASA | Launch of space shuttle Challenger on the 41-C mission |
| `reagan_address` | c914 | 1986 | Public domain | ホワイトハウス写真室 | Presidents Speech to The Nation on The Space Shuttle Challenger in Oval Office - DPLA - 24415e25cef1697901176efda1f71503.jpg |
| `recovery_ship` | c901 | 1986 | Public domain | NASA | STS-51-L Debris Aboard the USGS Cutter Dallas - GPN-2004-00013.jpg |
| `rockwell_orbiter` | c113 | 1979 | Public domain | NASA | Space Shuttle Columbia receives her thermal tiles at KSC (KSC-79P-119).jpg |
| `rudder_burn` | c906 | 1986 | Public domain | NASA | STS-51-L Recovered Debris (Lower Right Vertical Stabilizer) - GPN-2004-00005.jpg |
| `safety_panel` | ep09 | 1986 | Public domain | NASA | Rogers Commission members arrive at Kennedy Space Center.jpg |
| `smoke_puffs` | c310 | 1986 | Public domain | NASA | STS51L-10144 black smoke.jpg |
| `srb_burn_hole` | c903 | 1986 | Public domain | NASA | STS-51-L Recovered Debris (Left Solid Rocket Booster) - GPN-2004-00009.jpg |
| `srb_burn_hole_2` | c904 | 1986 | Public domain (17 U.S.C. §105) | NASA | View of left SRB first piece retrieval |
| `srb_inside` | c905 | 1986 | Public domain | NASA | STS-51-L Recovered Debris (O-Ring Tracks on Right SRB Joint) - GPN-2004-00010.jpg |
| `srb_stack` | c501 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 srb +18秒 |
| `srb_sun_shade` | c519 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 pad +12秒 |
| `srb_trails` | c412 | 1986 | Public domain | NASA | Challenger Rocket Booster - GPN-2000-001422.jpg |
| `srm_horizontal` | c803 | 1979 | Public domain (17 U.S.C. §105) | MSFC | Space Shuttle Projects |
| `srm_vertical_test` | ep04 | 1987 | Public domain (17 U.S.C. §105) | MSFC | Space Shuttle Projects |
| `ssme_ignition` | c303 | 1986 | Public domain (17 U.S.C. §105) | NASA「Space Shuttle Challenger Accident Investigation」 | 記録映像 launch +9秒 |
| `ssme_salvage` | c910 | 1986 | Public domain | NASA | STS-51-L Recovered Debris (SSME Close Up) - GPN-2004-00008.jpg |
| `telecon_room` | c715 | 1986 | Public domain | NASA | STS-51-L mcc 01.jpg |
| `training_zero_g` | c212 | 1985 | Public domain | NASA | Zero-G training for crew of 1985 and 1986 space shuttle missions.jpg |

## キャッスル・ブラボー水爆実験（1954-03-01・12本目）　※2026-09-23（⑤b-2）

### 1. 写真（NARA RG 678 ＝ 米連邦 §105 ／ Commons ＝ 米国の職務著作 PD・日本の1954年の報道写真 PD）
`qa_out/ep12_assets.py credits --write` が書く（手で直さない）。

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 所蔵と識別子 |
|---|---|---|---|---|---|
| `fb_aerial_a` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763394（RG 678） |
| `fb_aerial_b` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763404（RG 678） |
| `fb_estes_a` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763408（RG 678） |
| `fb_estes_b` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763406（RG 678） |
| `fb_color_a` | （章ファイル） | 1954 | Public domain（米国の職務著作） | United States Department of Energy | Wikimedia Commons「Castle Bravo Blast.jpg」 |
| `fb_color_b` | （章ファイル） | 1954 | Public domain（米国の職務著作） | United States Department of Energy | Wikimedia Commons「Castle Bravo nuclear test.jpg」 |
| `fb_bw` | （章ファイル） | 1954 | Public domain（米国の職務著作） | Federal Government of the United States | Wikimedia Commons「Castle Bravo (black and white).jpg」 |
| `fb_close_a` | （章ファイル） | 1954 | Public domain（米国の職務著作） | Federal government of the United States | Wikimedia Commons「Castle Bravo 005.jpg」 |
| `fb_close_b` | （章ファイル） | 1954 | Public domain（米国の職務著作） | ENERGY.GOV | Wikimedia Commons「HD.10.290 (10540757794).jpg」 |
| `romeo_cloud` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763402（RG 678） |
| `union_cloud` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763398（RG 678） |
| `nectar_cloud` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763396（RG 678） |
| `yankee_fb_1` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763410（RG 678） |
| `yankee_fb_2` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763412（RG 678） |
| `yankee_fb_3` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763414（RG 678） |
| `yankee_cloud` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763400（RG 678） |
| `mine_recovery` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763464（RG 678） |
| `dev_shrimp` | （章ファイル） | 1954 | Public domain（米国の職務著作） | Federal government of the United States | Wikimedia Commons「Castle Bravo Shrimp Device 002.jpg」 |
| `dev_shrimp_men` | （章ファイル） | 1954 | Public domain（米国の職務著作） | USDE | Wikimedia Commons「BravoSHRIMPShotCab.jpg」 |
| `dev_shotcab` | （章ファイル） | 1954 | Public domain（米国の職務著作） | USDE | Wikimedia Commons「BravoShotCab.jpg」 |
| `dev_truck` | （章ファイル） | 1954 | Public domain（米国の職務著作） | United States Atomic Energy Agency | Wikimedia Commons「Operation Castle AW 1.jpg」 |
| `base_parry_aerial` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763422（RG 678） |
| `base_airfield` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763494（RG 678） |
| `base_metal` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763454（RG 678） |
| `base_tents` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763452（RG 678） |
| `base_dock` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763420（RG 678） |
| `base_eneman` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763428（RG 678） |
| `rongelap_landing` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763432（RG 678） |
| `rongelap_booties` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763434（RG 678） |
| `rongerik_station` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763424（RG 678） |
| `dmg_eneman` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763468（RG 678） |
| `dmg_mine` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763466（RG 678） |
| `suits_three` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763470（RG 678） |
| `suits_scrub` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763472（RG 678） |
| `suits_adrikan` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763450（RG 678） |
| `dc_f84g` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763492（RG 678） |
| `dc_curtis` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763430（RG 678） |
| `dc_yag40_deck` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763438（RG 678） |
| `dc_b36_tail` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763486（RG 678） |
| `dc_ship_scrub` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763474（RG 678） |
| `dc_parry_equip` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763440（RG 678） |
| `dc_b36_under` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763490（RG 678） |
| `dc_b36_wing` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763488（RG 678） |
| `dc_tent` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763446（RG 678） |
| `dc_yag40_spray` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763436（RG 678） |
| `dc_molala` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763456（RG 678） |
| `dc_f4u_test` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763444（RG 678） |
| `dc_f4u_wash` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763442（RG 678） |
| `fo_roll_prep` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763478（RG 678） |
| `fo_cave` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763460（RG 678） |
| `fo_f84g` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763476（RG 678） |
| `fo_tank` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763416（RG 678） |
| `fo_pig_lift` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763484（RG 678） |
| `fo_pig_place` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763482（RG 678） |
| `fo_wire` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763458（RG 678） |
| `fo_rolled` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763480（RG 678） |
| `fo_tray` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763448（RG 678） |
| `fo_buoy` | （章ファイル） | 1954 | Public domain (17 U.S.C. §105) | 米国立公文書館 | NARA 146763418（RG 678） |
| `jp_tuna_check` | （章ファイル） | 1954 | Public domain（日本・1957年より前に公表の写真） | Yomiuri Shimbun | Wikimedia Commons「Technical experts checking contamination by nuclear fallout of Tunas after Dai5 Fukuryū maru Incident - 1954 - The Yomiuri Shimbun.png」 |
| `jp_fish_sign` | （章ファイル） | 1954 | Public domain（日本・1957年より前に公表の写真） | Asahigraph | Wikimedia Commons「A signboard appealing shoppers that our fish shop does not sell tunas contaminated by nuclear fallout - 1954 - Asahi Graph.png」 |
| `eisenhower_strauss` | （章ファイル） | 1954 | Public domain（米国の職務著作） | NARA photograph | Wikimedia Commons「Eisenhower and Strauss.jpg」 |
| `doc_aec_letter` | （章ファイル） | 1954 | Public domain（米国の職務著作） | United States Department of Energy | Wikimedia Commons「AEC Authorization for Operation Castle.png」 |
| `doc_bikini_chart` | （章ファイル） | 1958 | Public domain（米国の職務著作） | Unknown authorUnknown author or not provided | Wikimedia Commons「Bikini Atoll - NARA - 140696551.jpg」 |
| `fb_c101` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 米エネルギー省 | https://commons.wikimedia.org/wiki/File:Castle_Bravo_Detonation_USDE.ogv |
| `fb_c501` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 米エネルギー省 | https://commons.wikimedia.org/wiki/File:Castle_Bravo_Detonation_USDE.ogv |
| `fb_c607` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 米エネルギー省 | https://commons.wikimedia.org/wiki/File:Castle_Bravo_Detonation_USDE.ogv |
| `fb_c506` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 米エネルギー省 | https://commons.wikimedia.org/wiki/File:Castle_Bravo_Detonation_USDE.ogv |
| `fb_c608` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 米エネルギー省 | https://commons.wikimedia.org/wiki/File:Castle_Bravo_Detonation_USDE.ogv |
| `fb_c324` | （章ファイル） | 1954 | Public domain（US not renewed） | Wikimedia Commons | https://commons.wikimedia.org/wiki/File:Castle_Bravo_15_megaton_detonation,_1954.webm |
| `fb_c502` | （章ファイル） | 1954 | Public domain（US not renewed） | Wikimedia Commons | https://commons.wikimedia.org/wiki/File:Castle_Bravo_15_megaton_detonation,_1954.webm |
| `fb_c606` | （章ファイル） | 1954 | Public domain（US not renewed） | Wikimedia Commons | https://commons.wikimedia.org/wiki/File:Castle_Bravo_15_megaton_detonation,_1954.webm |
| `fb_c110` | （章ファイル） | 1954 | Public domain（US not renewed） | Wikimedia Commons | https://commons.wikimedia.org/wiki/File:Castle_Bravo_15_megaton_detonation,_1954.webm |
| `fb_c102` | （章ファイル） | 1954 | Public domain（US not renewed） | Wikimedia Commons | https://commons.wikimedia.org/wiki/File:Castle_Bravo_15_megaton_detonation,_1954.webm |
| `fb_c522` | （章ファイル） | 1954 | Public domain（US not renewed） | Wikimedia Commons | https://commons.wikimedia.org/wiki/File:Castle_Bravo_15_megaton_detonation,_1954.webm |
| `doe_shotcab_near` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 米エネルギー省 | https://commons.wikimedia.org/wiki/File:Castle_Bravo_Detonation_USDE.ogv |
| `doe_shotcab_far` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 米エネルギー省 | https://commons.wikimedia.org/wiki/File:Castle_Bravo_Detonation_USDE.ogv |
| `doe_cloud_cap` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 米エネルギー省 | https://commons.wikimedia.org/wiki/File:Castle_Bravo_Detonation_USDE.ogv |
| `mike_cloud` | （章ファイル） | 1952 | Public domain（米国の職務著作） | Department of Defense. Defense Atomic Support Agency. 5/6/1959-3/29/1971 | Wikimedia Commons「IvyMike2 HR.jpg」 |
| `mike_device` | （章ファイル） | 1952 | Public domain（米国の職務著作） | United States Department of Energy | Wikimedia Commons「Ivy Mike Sausage device.jpg」 |
| `pg1` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 1頁 |
| `pg30` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 30頁 |
| `pg114` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 114頁 |
| `pg118` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 118頁 |
| `pg211` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 211頁 |
| `pg212` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 212頁 |
| `pg213` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 213頁 |
| `pg214` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 214頁 |
| `pg215` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 215頁 |
| `pg216` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 216頁 |
| `pg218` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 218頁 |
| `pg219` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 219頁 |
| `pg221` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 221頁 |
| `pg223` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 223頁 |
| `pg226` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 226頁 |
| `pg229` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 229頁 |
| `pg230` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 230頁 |
| `pg232` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 232頁 |
| `pg238` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 238頁 |
| `pg240` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 240頁 |
| `pg241` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 241頁 |
| `pg243` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 243頁 |
| `pg1015` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 医師団（Project 4.1） | WT-923 PDF 15頁 |
| `pg1082` | （章ファイル） | 1954 | Public domain（米国の職務著作） | 医師団（Project 4.1） | WT-923 PDF 82頁 |
| `pg2069` | （章ファイル） | 1979 | Public domain（米国の職務著作） | 国防原子力局（GE-TEMPO の抜粋版） | DASA 1251 PDF 69頁 |
| `pg2074` | （章ファイル） | 1979 | Public domain（米国の職務著作） | 国防原子力局（GE-TEMPO の抜粋版） | DASA 1251 PDF 74頁 |
| `pg31` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 31頁 |
| `pg209` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 209頁 |
| `pg217` | （章ファイル） | 1982 | Public domain（米国の職務著作） | 国防原子力局 | DNA 6035F PDF 217頁 |

## トルコ航空981便（1974-03-03・13本目）　※2026-09-24（⑤b-2）

### 1. 写真（Wikimedia Commons ＝ CC BY-SA は**額装・無改変・1点1カット**／CC BY／CC0／PD）と報告書の頁
`qa_out/ep13_assets.py credits --write` が書く（手で直さない）。BY-SA の表示＝撮影者・許諾名と URL・素材の URL・無改変（許諾の URL は概要欄で）。

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `tcjav_taxi` | c202 | 1973 | CC BY-SA 2.0 | clipperarctic | Wikimedia Commons「TC-JAV (5920254289) (2).jpg」　https://commons.wikimedia.org/wiki/File:TC-JAV_(5920254289)_(2).jpg |
| `tcjav_takeoff` | c104 | 1973 | CC BY-SA 2.0 | clipperarctic | Wikimedia Commons「TC-JAV (6004629408).jpg」　https://commons.wikimedia.org/wiki/File:TC-JAV_(6004629408).jpg |
| `tcjav_tail` | c606 | 不明 | CC BY-SA 2.0 | clipperarctic | Wikimedia Commons「TC-JAV, Turkish DC-10 (6060110163).jpg」　https://commons.wikimedia.org/wiki/File:TC-JAV,_Turkish_DC-10_(6060110163).jpg |
| `tcjav_landing` | c701 | 1973 | CC BY-SA 4.0 | M D West | Wikimedia Commons「THY Türk Hava Yolları - Turkish Airlines McDonnell Douglas DC-10-10 London - Heathrow 1973.jpg」　https://commons.wikimedia.org/wiki/File:THY_Türk_Hava_Yolları_-_Turkish_Airlines_McDonnell_Douglas_DC-10-10_London_-_Heathrow_1973.jpg |
| `n103aa_1977` | c401 | 1977 | CC BY 2.0 | GeorgeM757 | Wikimedia Commons「N103AA American DC-10-10 at KSFO.jpg」　https://commons.wikimedia.org/wiki/File:N103AA_American_DC-10-10_at_KSFO.jpg |
| `aa96_door` | c421 | 1972 | Public domain | 米連邦航空局（FAA） | Wikimedia Commons「Photo of American Airlines Flight 96 cargo door.jpg」　https://commons.wikimedia.org/wiki/File:Photo_of_American_Airlines_Flight_96_cargo_door.jpg |
| `wreck_1997` | c102 | 1997 | CC BY 4.0 | Ian Abbott | Wikimedia Commons「Paris DC-10 Crash- March 3, 1974.jpg」　https://commons.wikimedia.org/wiki/File:Paris_DC-10_Crash-_March_3,_1974.jpg |
| `names_wall` | c814 | 1997 | CC BY 4.0 | Ian Abbott | Wikimedia Commons「Paris DC-10 Crash, Names.jpg」　https://commons.wikimedia.org/wiki/File:Paris_DC-10_Crash,_Names.jpg |
| `stele_2010` | c801 | 2010 | CC BY-SA 2.0 fr | P.poschadel | Wikimedia Commons「Stèle du crash aérien de 1974 (parcelle 144).jpg」　https://commons.wikimedia.org/wiki/File:Stèle_du_crash_aérien_de_1974_(parcelle_144).jpg |
| `monument_2010` | c915 | 2010 | CC BY 3.0 | Mel22 | Wikimedia Commons「Monument DC10 Ermenonville-1.jpg」　https://commons.wikimedia.org/wiki/File:Monument_DC10_Ermenonville-1.jpg |
| `klm_landing_1972` | c506 | 1972 | CC0 | オランダ国立公文書館（Anefo） | Wikimedia Commons「Eerste DC 10 voor KLM landt op Schiphol, Bestanddeelnr 926-1070.jpg」　https://commons.wikimedia.org/wiki/File:Eerste_DC_10_voor_KLM_landt_op_Schiphol,_Bestanddeelnr_926-1070.jpg |
| `klm_apron_1972` | c207 | 1972 | CC0 | オランダ国立公文書館（Anefo） | Wikimedia Commons「Eerste DC 10 voor KLM landt op Schiphol, DC 10 op platform, Bestanddeelnr 926-1071.jpg」　https://commons.wikimedia.org/wiki/File:Eerste_DC_10_voor_KLM_landt_op_Schiphol,_DC_10_op_platform,_Bestanddeelnr_926-1071.jpg |
| `klm_cockpit_1972` | c704 | 1972 | CC0 | オランダ国立公文書館（Anefo） | Wikimedia Commons「Eerste DC 10 voor KLM landt op Schiphol, cockpit en interieur, Bestanddeelnr 926-1073.jpg」　https://commons.wikimedia.org/wiki/File:Eerste_DC_10_voor_KLM_landt_op_Schiphol,_cockpit_en_interieur,_Bestanddeelnr_926-1073.jpg |
| `klm_nice_1973` | c804 | 1973 | CC0 | オランダ国立公文書館（Anefo） | Wikimedia Commons「Vlucht met DC-10 naar Nice, cockpit DC-10 met piloten, Bestanddeelnr 926-2653.jpg」　https://commons.wikimedia.org/wiki/File:Vlucht_met_DC-10_naar_Nice,_cockpit_DC-10_met_piloten,_Bestanddeelnr_926-2653.jpg |
| `aa_dc10_1974` | c424 | 1974 | CC BY 3.0 | Piergiuliano Chesi | Wikimedia Commons「American Airlines McDonnell Douglas DC-10 01.jpg」　https://commons.wikimedia.org/wiki/File:American_Airlines_McDonnell_Douglas_DC-10_01.jpg |
| `kal_longbeach_1974` | c605 | 1974 | CC BY 3.0 | Piergiuliano Chesi | Wikimedia Commons「Korean Air Lines McDonnell Douglas DC-10 N198 01.jpg」　https://commons.wikimedia.org/wiki/File:Korean_Air_Lines_McDonnell_Douglas_DC-10_N198_01.jpg |
| `ua_longbeach_1974` | c617 | 1974 | CC BY 3.0 | Piergiuliano Chesi | Wikimedia Commons「United Airlines DC-10 N1826U.jpg」　https://commons.wikimedia.org/wiki/File:United_Airlines_DC-10_N1826U.jpg |
| `dc10_flight_1971` | c713 | 1971 | Public domain | マクドネル・ダグラス社の広報写真 | Wikimedia Commons「McDonnell Douglas DC-10 N1803U (C15-10).jpg」　https://commons.wikimedia.org/wiki/File:McDonnell_Douglas_DC-10_N1803U_(C15-10).jpg |
| `dc10_cabin` | c802 | 不明 | Public domain | マクドネル・ダグラス社の広報写真 | Wikimedia Commons「McDonnell Douglas DC-10 interior (CJ406257).jpg」　https://commons.wikimedia.org/wiki/File:McDonnell_Douglas_DC-10_interior_(CJ406257).jpg |
| `tcjau_fra_1974` | c203 | 1974 | CC BY 3.0 | RuthAS | Wikimedia Commons「Douglas DC-10-10 TC-JAU THY FRA 28.07.74 edited-2.jpg」　https://commons.wikimedia.org/wiki/File:Douglas_DC-10-10_TC-JAU_THY_FRA_28.07.74_edited-2.jpg |
| `finnair_dc10` | c206 | 不明 | CC BY 4.0 | Volker von Bonin／フィンランド文化遺産庁 | Wikimedia Commons「Finnairin DC-10 lentokone lentokentällä 1970 (HK7137-875).tif」　https://commons.wikimedia.org/wiki/File:Finnairin_DC-10_lentokone_lentokentällä_1970_(HK7137-875).tif |
| `orly_hall_1970` | c209 | 1970 | CC BY-SA 4.0 | スイス航空／ETH 図書館 | Wikimedia Commons「Departure hall at Paris-Orly airport (LBS SR04-038169).tif」　https://commons.wikimedia.org/wiki/File:Departure_hall_at_Paris-Orly_airport_(LBS_SR04-038169).tif |
| `pg11` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 11頁 |
| `pg15` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 15頁 |
| `pg16` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 16頁 |
| `pg17` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 17頁 |
| `pg53` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 53頁 |
| `pg63` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 63頁 |
| `pg80` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 80頁 |
| `pg88` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 88頁 |
| `pg90` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 90頁 |
| `pg91` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 91頁 |
| `pg92` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 92頁 |
| `pg94` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 94頁 |
| `pg95` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 95頁 |
| `pg104` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 104頁 |
| `pg105` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 105頁 |
| `pg107` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 107頁 |
| `pg109` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 109頁 |
| `pg141` | （章ファイル） | 1976 | 仏国の公文書＝引用（改変しない） | フランス事故調査委員会 | 仏 最終報告 PDF 141頁 |
| `pg1001` | （章ファイル） | 1976 | 英国の公文書＝引用（改変しない） | 英国事故調査局（仏報告の英訳） | AIB 8/76 PDF 1頁 |
| `pg1010` | （章ファイル） | 1976 | 英国の公文書＝引用（改変しない） | 英国事故調査局（仏報告の英訳） | AIB 8/76 PDF 10頁 |
| `pg1052` | （章ファイル） | 1976 | 英国の公文書＝引用（改変しない） | 英国事故調査局（仏報告の英訳） | AIB 8/76 PDF 52頁 |
| `pg1053` | （章ファイル） | 1976 | 英国の公文書＝引用（改変しない） | 英国事故調査局（仏報告の英訳） | AIB 8/76 PDF 53頁 |
| `pg2005` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 5頁 |
| `pg2014` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 14頁 |
| `pg2017` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 17頁 |
| `pg2030` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 30頁 |
| `pg2032` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 32頁 |
| `pg2033` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 33頁 |
| `pg2034` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 34頁 |
| `pg2046` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 46頁 |
| `pg2051` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 51頁 |
| `pg2055` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米上院 商業委員会 航空小委員会 | 米上院 報告 PDF 55頁 |
| `pg4001` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米連邦航空局（FAA） | AD 74-08-04 PDF 1頁 |
| `pg4101` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米連邦航空局（FAA） | AD 74-12-07 PDF 1頁 |
| `pg4201` | （章ファイル） | 1975 | Public domain（米国の職務著作） | 米連邦航空局（FAA） | AD 75-15-05 PDF 1頁 |
| `pg4301` | （章ファイル） | 1974 | Public domain（米国の職務著作） | 米官報（Federal Register） | 官報 1974-04-02 PDF 1頁 |
| `pg5002` | （章ファイル） | 1972 | 企業の技術文書＝引用（改変しない） | マクドネル・ダグラス社 | SB 52-37 PDF 2頁 |
| `pg5003` | （章ファイル） | 1972 | 企業の技術文書＝引用（改変しない） | マクドネル・ダグラス社 | SB 52-37 PDF 3頁 |

## セウォル号沈没事故（2014-04-16・14本目）　※2026-09-29（⑤b-7a）

### 1. 写真（Wikimedia Commons ＝ CC BY-SA は**額装・無改変・1点1カット**／CC BY／Attribution／CC0／PD／引用）・映像・判決と報告書の頁
`qa_out/ep14_assets.py credits --write` が書く（手で直さない）。BY-SA の表示＝撮影者・許諾名と URL・素材の URL・無改変（許諾の URL は概要欄で）。

- 🔴 **私人の顔と名前は出さない**：G2（光化門 2018）の下の板＝見つかっていない5人の顔写真と名前／L1（救命胴衣の列）の奥の集会の人＝どちらも切り出し（`cuts/ss.py` の `TRIM`）で外した（改変の旨は画面の出典に出る）。🆕 2026-10-17：リポに置く原本も、G2 の下の板と売り場2か所（同じ5人の顔写真と名前）・L1 の上 57.5% に**モザイク**（`qa_out/ep14_assets.py` の `MASK`）＝リポの写しは改変あり。公開ずみの動画は焼き直さない（変わらない）
- 🔴 H1（当日の沈む船）＝Commons の表示「South Korea-Gov」に根拠が無い（削除依頼中）＝**引用**（額装・無改変・出典＝韓国 海洋警察）。サムネに使わない
- 🔴 **米国防総省（米海軍・米海兵隊）の写真と映像**（`site_0418`・`e1`・`e2`）＝DVIDS の条件「The appearance of U.S. Department of Defense (DoD) visual information does not imply or constitute DoD endorsement.」＝**概要欄に「米国防総省の画像の使用は、同省の推奨を意味しません」**（⑥の申し送り）
- 映像＝DVIDS 330919（USS Bonhomme Richard・2014-04-18・1920×1080）・332722（31st MEU・2014-04-19・1280×720）。原本は CloudFront の `DOD_<番号>.mp4`（`ref/ep14/clips.json` の `media`）

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `sinking_0416` | c107 | 2014 | 引用（Commons の表示 South Korea-Gov は根拠なし） | 韓国 海洋警察 | Wikimedia Commons「South-Korea-Ferry-Sewol-sinking.jpg」　https://commons.wikimedia.org/wiki/File:South-Korea-Ferry-Sewol-sinking.jpg |
| `sewol_incheon` | c202・c306・c501 | 2014 | Public domain | jinjoo2713 | Wikimedia Commons「Ferry Sewol 1.jpg」　https://commons.wikimedia.org/wiki/File:Ferry_Sewol_1.jpg |
| `naminoue_2010` | c301 | 2010 | CC BY-SA 2.0 | tsuda | Wikimedia Commons「Ferry Naminoue 20100214.jpg」　https://commons.wikimedia.org/wiki/File:Ferry_Naminoue_20100214.jpg |
| `mokpo_2017` | c412 | 2017 | CC BY-SA 4.0 | Trainholic | Wikimedia Commons「2017 MV Sewol in Mokpo New Port.jpg」　https://commons.wikimedia.org/wiki/File:2017_MV_Sewol_in_Mokpo_New_Port.jpg |
| `site_0418` | c918 | 2014 | Public domain | 米海軍 | Wikimedia Commons「USS Bonhomme Richard operations 140418-N-LM312-287.jpg」　https://commons.wikimedia.org/wiki/File:USS_Bonhomme_Richard_operations_140418-N-LM312-287.jpg |
| `search_tent_0418` | ca02 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (13999504453).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(13999504453).jpg |
| `search_ssu_0419` | ca03 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (13979939304).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(13979939304).jpg |
| `search_ship21_0419` | ca04 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (13956410506).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(13956410506).jpg |
| `search_waves_0420` | ca05 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (13976287932).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(13976287932).jpg |
| `search_night_0420` | ca06 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (13979938264).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(13979938264).jpg |
| `search_flare_0420` | ca07 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (13999503253).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(13999503253).jpg |
| `search_diver_0504` | ca09 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (14134129785).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(14134129785).jpg |
| `search_fleet_0506` | ca10 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (13947458749).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(13947458749).jpg |
| `search_banner_0504` | ca12 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (13947445037).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(13947445037).jpg |
| `search_divers_0504` | ca13 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (14134384094).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(14134384094).jpg |
| `search_flare_0501` | ca14 | 2014 | CC BY-SA 2.0 | 韓国 国防部 | Wikimedia Commons「2014.4 세월호 구조 작전 (14154193263).jpg」　https://commons.wikimedia.org/wiki/File:2014.4_세월호_구조_작전_(14154193263).jpg |
| `danwon_school` | cd01 | 2014 | Public domain | Fyodor Tertitskiy | Wikimedia Commons「Tanwon School 5.jpg」　https://commons.wikimedia.org/wiki/File:Tanwon_School_5.jpg |
| `danwon_banner` | cd02 | 2014 | Public domain | Fyodor Tertitskiy | Wikimedia Commons「Tanwon School 7.jpg」　https://commons.wikimedia.org/wiki/File:Tanwon_School_7.jpg |
| `seoul_plaza_2014` | cd03 | 2014 | CC0 | PuzzletChung | Wikimedia Commons「Sewol memorial ribbons, Seoul Plaza, 2014-06-22.jpg」　https://commons.wikimedia.org/wiki/File:Sewol_memorial_ribbons,_Seoul_Plaza,_2014-06-22.jpg |
| `ansan_street_2014` | cd04 | 2014 | CC BY-SA 3.0 | Piotrus | Wikimedia Commons「Memorial for the victims of the sinking of the MV Sewol 01.JPG」　https://commons.wikimedia.org/wiki/File:Memorial_for_the_victims_of_the_sinking_of_the_MV_Sewol_01.JPG |
| `gwanghwamun_2018` | cd05 | 2018 | Attribution | Garam | Wikimedia Commons「Memorial place of the MV Sewol on Gwanghwamun Plaza in 2018 - 2.jpg」　https://commons.wikimedia.org/wiki/File:Memorial_place_of_the_MV_Sewol_on_Gwanghwamun_Plaza_in_2018_-_2.jpg |
| `lifejackets_2017` | cd07 | 2017 | CC BY 3.0 | Mathew Schwartz | Wikimedia Commons「Lost Children (191940227).jpeg」　https://commons.wikimedia.org/wiki/File:Lost_Children_(191940227).jpeg |
| `fb_ca01` | ca01 | 2014 | Public domain（米国の職務著作） | 米海軍 | https://www.dvidshub.net/video/330919/　https://www.dvidshub.net/video/330919/ |
| `fb_ca11` | ca11 | 2014 | Public domain（米国の職務著作） | 米海兵隊 | https://www.dvidshub.net/video/332722/sewol-ferry-sar-efforts-31st-meu　https://www.dvidshub.net/video/332722/sewol-ferry-sar-efforts-31st-meu |
| `pg1` | （章ファイル） | 2015 | 判決＝韓国著作権法7条・日本の著作権法13条で権利の目的とならない | 大韓民国 大法院 | sewol_scourt.pdf PDF 1頁 |
| `pg12` | （章ファイル） | 2015 | 判決＝韓国著作権法7条・日本の著作権法13条で権利の目的とならない | 大韓民国 大法院 | sewol_scourt.pdf PDF 12頁 |
| `pg18` | （章ファイル） | 2015 | 判決＝韓国著作権法7条・日本の著作権法13条で権利の目的とならない | 大韓民国 大法院 | sewol_scourt.pdf PDF 18頁 |
| `pg20` | （章ファイル） | 2015 | 判決＝韓国著作権法7条・日本の著作権法13条で権利の目的とならない | 大韓民国 大法院 | sewol_scourt.pdf PDF 20頁 |
| `pg33` | （章ファイル） | 2015 | 判決＝韓国著作権法7条・日本の著作権法13条で権利の目的とならない | 大韓民国 大法院 | sewol_scourt.pdf PDF 33頁 |
| `pg1001` | （章ファイル） | 2014 | 公共ヌリの表示なし＝引用（紙面をそのまま・出典） | 海洋安全審判院 | kmst_sewol.pdf PDF 1頁 |
| `pg1015` | （章ファイル） | 2014 | 公共ヌリの表示なし＝引用（紙面をそのまま・出典） | 海洋安全審判院 | kmst_sewol.pdf PDF 15頁 |
| `pg1016` | （章ファイル） | 2014 | 公共ヌリの表示なし＝引用（紙面をそのまま・出典） | 海洋安全審判院 | kmst_sewol.pdf PDF 16頁 |
| `pg1060` | （章ファイル） | 2014 | 公共ヌリの表示なし＝引用（紙面をそのまま・出典） | 海洋安全審判院 | kmst_sewol.pdf PDF 60頁 |
| `pg1083` | （章ファイル） | 2014 | 公共ヌリの表示なし＝引用（紙面をそのまま・出典） | 海洋安全審判院 | kmst_sewol.pdf PDF 83頁 |
| `pg1091` | （章ファイル） | 2014 | 公共ヌリの表示なし＝引用（紙面をそのまま・出典） | 海洋安全審判院 | kmst_sewol.pdf PDF 91頁 |
| `pg1113` | （章ファイル） | 2014 | 公共ヌリの表示なし＝引用（紙面をそのまま・出典） | 海洋安全審判院 | kmst_sewol.pdf PDF 113頁 |
| `pg1136` | （章ファイル） | 2014 | 公共ヌリの表示なし＝引用（紙面をそのまま・出典） | 海洋安全審判院 | kmst_sewol.pdf PDF 136頁 |
| `pg2003` | （章ファイル） | 2026 | 一覧の頁の表示は公共ヌリ第4類型（改変禁止）＝引用（紙面をそのまま・出典） | 中央海洋安全審判院 | later/kmst_2026_001_central_verdict.pdf PDF 3頁 |
| `pg2089` | （章ファイル） | 2026 | 一覧の頁の表示は公共ヌリ第4類型（改変禁止）＝引用（紙面をそのまま・出典） | 中央海洋安全審判院 | later/kmst_2026_001_central_verdict.pdf PDF 89頁 |

## リノ・エアレース墜落事故（2011-09-16・15本目）

※2026-09-30（⑤b-6）。`qa_out/ep15_assets.py credits --write` が書く（手で直さない）。

### 1. 写真（Wikimedia Commons ＝ CC BY-SA は**額装・無改変・1点1カット**／CC BY）・報告書の courtesy の写真（紙面の引用）・報告書と資料の頁
BY-SA の表示＝撮影者・許諾名と URL・素材の URL・無改変（許諾の URL は概要欄で）。

- 🔴 **報告書の courtesy の写真（図5〜10・15・17）＝紙面の引用**（ルール §2-6c・09-25 カズヤくん）：写真だけを切り出さず、**図・説明の行・撮影者の行まで**を紙面のまま（`pg<頁>_fig<NN>`）。額装・寄り0・色を変えない・1点1カット。画面の出典＝撮影者名と NTSB（「引用・無改変」）
- 🔴 **tataquax（日本の観客＝私人）の撮影時刻は EXIF が日本時間のまま＝現地は −16時間**（推定・materials.md §3-0）。副題は「事故のレースの離陸／周回中」まで（「事故の◯秒前」と書かない）。撮影者名は Flickr の名前だけ
- 🔴 観客・整備の人は私人＝顔と名前は出さない。CC BY の2010年の2点（`gg_nose_2010`・`gg_pit_2010`）は**顔だけモザイク**（09-30 カズヤくん「顔面のみのモザイク加工」＝元画像を直す・`cuts/ss.py` の `NEEDS_MASK`・`masked.json` に md5）。BY-SA はモザイク自体が翻案＝かけない（近景の私人の顔が写る点は使わない・中景の小さな人は §B2-2 のとおり使う）
- 来歴の3点（Bill Larkins）の撮影年は題名の「69」「70」（Commons の日付 2011 は取り込みの年）
- 動く映像は使わない（【映像あり】なし＝09-25 カズヤくん）。Googleアースは使わない（09-30 カズヤくん＝地図に替えた）

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `gg_below_race` | c205 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6452065839).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6452065839).jpg |
| `gg_takeoff_race` | c208 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6452065605).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6452065605).jpg |
| `gg_taxi_0915` | c401 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Jimmy Leeward's Galloping Ghost at 2011 Reno Air Races.jpg」　https://commons.wikimedia.org/wiki/File:Jimmy_Leeward's_Galloping_Ghost_at_2011_Reno_Air_Races.jpg |
| `gg_nose_0916` | c419 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6452063939).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6452063939).jpg |
| `gg_pit_0914` | c504 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6452062347).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6452062347).jpg |
| `strega_taxi` | c207 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6361173745).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6361173745).jpg |
| `voodoo_taxi` | c203 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6450673359).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6450673359).jpg |
| `strega_takeoff` | c202 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6361174323).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6361174323).jpg |
| `strega_below` | c219 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6361174465).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6361174465).jpg |
| `voodoo_below` | c318 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6450673505).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6450673505).jpg |
| `stands_0916` | c801 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6179482685).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6179482685).jpg |
| `pylon_0916` | c204 | 2011 | CC BY-SA 2.0 | tataquax | Wikimedia Commons「Reno Air Races 2011 (6225303046).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Air_Races_2011_(6225303046).jpg |
| `candace_1969` | c405 | 1969 | CC BY-SA 2.0 | Bill Larkins | Wikimedia Commons「P-51n79111side69 (5658262832).jpg」　https://commons.wikimedia.org/wiki/File:P-51n79111side69_(5658262832).jpg |
| `taxi_1970` | c406 | 1970 | CC BY-SA 2.0 | Bill Larkins | Wikimedia Commons「P-51n79111side70 (5658262932).jpg」　https://commons.wikimedia.org/wiki/File:P-51n79111side70_(5658262932).jpg |
| `damage_1970` | c407 | 1970 | CC BY-SA 2.0 | Bill Larkins | Wikimedia Commons「P-51 N79111 after damage 1970 (6161387830).jpg」　https://commons.wikimedia.org/wiki/File:P-51_N79111_after_damage_1970_(6161387830).jpg |
| `gg_nose_2010` | c417 | 2010 | CC BY 2.0 | jeggernot | Wikimedia Commons「Galloping Ghost.jpg」　https://commons.wikimedia.org/wiki/File:Galloping_Ghost.jpg |
| `gg_pit_2010` | c416 | 2010 | CC BY 2.0 | jeggernot | Wikimedia Commons「GallopingGhost 2010-09-18.jpg」　https://commons.wikimedia.org/wiki/File:GallopingGhost_2010-09-18.jpg |
| `stead_2009` | c112 | 2009 | CC BY-SA 2.0 | Shawn from Airdrie | Wikimedia Commons「Reno Stead Field (3392833169).jpg」　https://commons.wikimedia.org/wiki/File:Reno_Stead_Field_(3392833169).jpg |
| `seminar_2016` | c906 | 2016 | CC BY 4.0 | Don Ramey Logan | Wikimedia Commons「2016 National Championship Air Races Pylon Racing Seminar by Don Ramey Logan.jpg」　https://commons.wikimedia.org/wiki/File:2016_National_Championship_Air_Races_Pylon_Racing_Seminar_by_Don_Ramey_Logan.jpg |
| `pg23_fig05` | c301 | 2011 | 引用（NTSB 報告書の紙面に載った courtesy の写真） | Jonathan Apfelbaum | NTSB AAB-12/01（2012年）PDF 23頁 図5　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf |
| `pg24_fig06` | c306 | 2011 | 引用（NTSB 報告書の紙面に載った courtesy の写真） | Jonathan Apfelbaum | NTSB AAB-12/01（2012年）PDF 24頁 図6　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf |
| `pg25_fig07` | c309 | 2011 | 引用（NTSB 報告書の紙面に載った courtesy の写真） | Jonathan Apfelbaum | NTSB AAB-12/01（2012年）PDF 25頁 図7　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf |
| `pg26_fig08` | c310 | 2011 | 引用（NTSB 報告書の紙面に載った courtesy の写真） | Jonathan Apfelbaum | NTSB AAB-12/01（2012年）PDF 26頁 図8　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf |
| `pg27_fig09` | c311 | 2011 | 引用（NTSB 報告書の紙面に載った courtesy の写真） | Frank Ranney | NTSB AAB-12/01（2012年）PDF 27頁 図9　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf |
| `pg27_fig10` | c103 | 2011 | 引用（NTSB 報告書の紙面に載った courtesy の写真） | Julia Kirchenbauer | NTSB AAB-12/01（2012年）PDF 27頁 図10　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf |
| `pg33_fig15` | c520 | 2011 | 引用（NTSB 報告書の紙面に載った courtesy の写真） | Florian Schmehl | NTSB AAB-12/01（2012年）PDF 33頁 図15　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf |
| `pg34_fig17` | c521 | 2011 | 引用（NTSB 報告書の紙面に載った courtesy の写真） | Florian Schmehl | NTSB AAB-12/01（2012年）PDF 34頁 図17　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf |
| `pg1` | c110 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 1頁 |
| `pg12` | c402 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 12頁 |
| `pg13` | c503 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 13頁 |
| `pg14` | c501 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 14頁 |
| `pg15` | c507 c611 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 15頁 |
| `pg17` | c818 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 17頁 |
| `pg20` | c211 | 2012 | PD（米連邦の職務著作・図の下地の空撮は出どころ未記載＝頁ごとの引用） | NTSB | AAB1201.pdf PDF 20頁 |
| `pg28` | c304 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 28頁 |
| `pg29` | c308 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 29頁 |
| `pg31` | c707 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 31頁 |
| `pg32` | c105 c708 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 32頁 |
| `pg35` | c409 c601 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 35頁 |
| `pg36` | c608 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 36頁 |
| `pg37` | c618 c703 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 37頁 |
| `pg43` | c901 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 43頁 |
| `pg46` | c904 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 46頁 |
| `pg51` | c624 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 51頁 |
| `pg52` | c724 | 2012 | PD（米連邦の職務著作） | NTSB | AAB1201.pdf PDF 52頁 |
| `pg1034` | c706 | 2012 | PD（米連邦の職務著作） | NTSB | ntsb_docket_40_materials_lab_12-029.pdf PDF 34頁 |
| `pg1036` | c710 | 2012 | PD（米連邦の職務著作） | NTSB | ntsb_docket_40_materials_lab_12-029.pdf PDF 36頁 |
| `pg1037` | c713 | 2012 | PD（米連邦の職務著作） | NTSB | ntsb_docket_40_materials_lab_12-029.pdf PDF 37頁 |
| `pg1038` | c714 | 2012 | PD（米連邦の職務著作） | NTSB | ntsb_docket_40_materials_lab_12-029.pdf PDF 38頁 |
| `pg1041` | c718 | 2012 | PD（米連邦の職務著作） | NTSB | ntsb_docket_40_materials_lab_12-029.pdf PDF 41頁 |
| `pg2009` | c209 | 2012 | PD（米連邦の職務著作・図の下地は Google Earth＝頁ごとの引用） | NTSB | ntsb_docket_33_survival_factors_operations_factual.pdf PDF 9頁 |
| `pg2015` | c814 | 2012 | PD（米連邦の職務著作・図の下地の空撮は出どころ未記載＝頁ごとの引用） | NTSB | ntsb_docket_33_survival_factors_operations_factual.pdf PDF 15頁 |
| `pg2019` | c805 | 2012 | PD（米連邦の職務著作・図の下地の空撮は出どころ未記載＝頁ごとの引用） | NTSB | ntsb_docket_33_survival_factors_operations_factual.pdf PDF 19頁 |
| `pg3014` | c317 | 2012 | PD（米連邦の職務著作・図の下地は Google Earth＝頁ごとの引用） | NTSB | ntsb_docket_14_data_recorders_factual.pdf PDF 14頁 |
| `pg4021` | c319 | 2012 | PD（米連邦の職務著作） | NTSB | ntsb_docket_53_aircraft_performance_study.pdf PDF 21頁 |
| `pg6001` | c902 | 2012 | PD（米連邦の職務著作） | NTSB | ntsb_recletter_A-12-008.pdf PDF 1頁 |

## バイオントダム災害（1963-10-09・16本目）

※2026-10-02（⑤b-7）。`qa_out/ep16_assets.py credits --write` が書く（手で直さない）。

### 1. 写真（Wikimedia Commons ＝ PD・CC BY・CC BY-SA は**額装・無改変・1点1カット**）・地形図・議会の報告書の頁
BY-SA の表示＝撮影者・許諾名と URL・素材の URL・無改変（許諾の URL は概要欄で）。

- 🔴 **PD の根拠は点ごとに違う**（記憶 feedback-pd-label-hides-two-different-grounds）＝米連邦 §105（米陸軍）／撮影者本人の宣言／伊の単純写真（撮影から20年＝1963年の写真は1983年に保護が切れた。米国でも PD-1996 の点がある）／1934年の地形図（PD-old）。権利の欄に1点ずつ書いた（「PD」と1行にまとめない）
- 🔴 **米陸軍の写真（1963年の4点・2023年の標識）＝⑥の概要欄に「米陸軍の写真の使用は推奨を意味しない」の断り書き**（ルール §5b-98⑧）
- 🔴 人が写る写真（§B2-2）：1968年の法廷（`trial_1968`）の座っている人の横顔8人は**顔だけモザイク**（2026-09-30 カズヤくん「顔面のみのモザイク加工」＝PD は手直しを許す＝元画像を直す・`cuts/ss.py` の `NEEDS_MASK`・`ref/ep16/masked.json`）。奥の判事席・憲兵（法廷の公務）・救援の兵士と消防（公的な任務）はそのまま。ほかの点の人（がれきの原の兵士・水辺の2人・天端の人影）は原寸で背丈 10〜25px＝顔は見分けられない
- 撮影年が割れる・分からない点（天端と満水の湖＝#084／#088 と同じ写真・操作の建物・カラーの絵はがき・建設前の絵はがき・水理模型）は撮影年を「不明」にし、**副題に年を書かない**（門番 credits）
- 取ったが当てない点：#029（道のトンネル＝事故のあとの記録）・#074（作業員の顔＝BY-SA）・#075（橋だけ）
- 動く映像は使わない（【映像あり】なし）。Google Earth は使わない（2026-10-02 カズヤくん＝7カットは地図〈VA〉に替えた）

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `dam_us_1963` | c103 c820 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | U.S. Army | Wikimedia Commons「Diga Vajont 1963.jpg」　https://commons.wikimedia.org/wiki/File:Diga_Vajont_1963.jpg |
| `toc_now` | c105 cb05 | 2016 | CC BY 3.0 | Davide Cavalli | Wikimedia Commons「Monte Toc (190845863).jpeg」　https://commons.wikimedia.org/wiki/File:Monte_Toc_(190845863).jpeg |
| `dam_houses_now` | c107 cb02 | 2005 | PD（撮影者本人の宣言） | Emanuele Paolini | Wikimedia Commons「La diga del Vajont vista da Longarone 18-8-2005.jpg」　https://commons.wikimedia.org/wiki/File:La_diga_del_Vajont_vista_da_Longarone_18-8-2005.jpg |
| `dam_gorge_now` | c111 ca27 cb03 | 2003 | CC BY 3.0 | Stefano Petri | Wikimedia Commons「Diga del Vajont da Longarone - panoramio.jpg」　https://commons.wikimedia.org/wiki/File:Diga_del_Vajont_da_Longarone_-_panoramio.jpg |
| `longarone_before` | c117 | 不明 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | 撮影者不明 | Wikimedia Commons「Vista della gola del Vajont prima della costruzione della diga.jpg」　https://commons.wikimedia.org/wiki/File:Vista_della_gola_del_Vajont_prima_della_costruzione_della_diga.jpg |
| `gorge_1956` | c201 | 1956 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Vajont 1956.jpg」　https://commons.wikimedia.org/wiki/File:Vajont_1956.jpg |
| `igm_1934` | c202 | 1934 | PD（1934年の地形図＝PD-old） | イタリア軍地理院 IGM | Wikimedia Commons「Mappa Vajont IGM 1934.jpg」　https://commons.wikimedia.org/wiki/File:Mappa_Vajont_IGM_1934.jpg |
| `gorge_1955` | c203 | 1955 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | M. Reberschak 編『Il grande Vajont』 | Wikimedia Commons「Valle del Vajont 1955.jpg」　https://commons.wikimedia.org/wiki/File:Valle_del_Vajont_1955.jpg |
| `bridge_works_1956` | c206 | 1956 | CC BY-SA 4.0 | Enel・Archivio Enel | Wikimedia Commons「1956. Ponte SACAIM. Avanzamento lavori.jpg」　https://commons.wikimedia.org/wiki/File:1956._Ponte_SACAIM._Avanzamento_lavori.jpg |
| `dam_works_1960` | c208 | 1960 | CC BY-SA 4.0 | Torno S.p.A.・Archivio Torno | Wikimedia Commons「Diga del Vajont vista da valle (1960).jpg」　https://commons.wikimedia.org/wiki/File:Diga_del_Vajont_vista_da_valle_(1960).jpg |
| `crest_cabin` | c212 c519 c622 c704 c709 | 不明 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | 撮影者不明 | Wikimedia Commons「Diga con cabina comandi.jpg」　https://commons.wikimedia.org/wiki/File:Diga_con_cabina_comandi.jpg |
| `crest_lake_1960` | c213 c317 c423 c610 c623 | 1960 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Vajont Diga 1960.jpg」　https://commons.wikimedia.org/wiki/File:Vajont_Diga_1960.jpg |
| `postcard_280_1961` | c214 | 1961 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Cartolina Diga del Vajont.jpg」　https://commons.wikimedia.org/wiki/File:Cartolina_Diga_del_Vajont.jpg |
| `erto_1960` | c215 c420 c702 | 1960 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | 撮影者不明 | Wikimedia Commons「Diga del Vajont 1960.jpg」　https://commons.wikimedia.org/wiki/File:Diga_del_Vajont_1960.jpg |
| `color_postcard` | c216 c521 c605 c714 | 不明 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | 撮影者不明 | Wikimedia Commons「Diga Vajont colori (bromocolor).jpg」　https://commons.wikimedia.org/wiki/File:Diga_Vajont_colori_(bromocolor).jpg |
| `crest_full_lake` | c219 c520 c615 | 不明 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | 撮影者不明 | Wikimedia Commons「Invaso Vajont estate 1963.jpg」　https://commons.wikimedia.org/wiki/File:Invaso_Vajont_estate_1963.jpg |
| `aerial_1960` | c220 | 1960 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Valle del Vajont 1960.jpg」　https://commons.wikimedia.org/wiki/File:Valle_del_Vajont_1960.jpg |
| `crack_1960` | c307 | 1960 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Frana Monte Toc 1960 1.jpg」　https://commons.wikimedia.org/wiki/File:Frana_Monte_Toc_1960_1.jpg |
| `slide_19601104` | c309 c323 c415 c501 | 1960 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Frana 4-11-1960.jpg」　https://commons.wikimedia.org/wiki/File:Frana_4-11-1960.jpg |
| `slide_1960_small` | c321 | 1960 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Frana Monte Toc 1960 2.jpg」　https://commons.wikimedia.org/wiki/File:Frana_Monte_Toc_1960_2.jpg |
| `model_nove` | c503 c505 c506 | 不明 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Simulazione frana Vajont.jpg」　https://commons.wikimedia.org/wiki/File:Simulazione_frana_Vajont.jpg |
| `trial_1968` | c719 ca01 ca12 | 1968 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Primo processo sul Vajont (1968).jpg」　https://commons.wikimedia.org/wiki/File:Primo_processo_sul_Vajont_(1968).jpg |
| `dam_slide_1963` | c804 cb18 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | U.S. Army | Wikimedia Commons「Vajont Dam landslide.jpg」　https://commons.wikimedia.org/wiki/File:Vajont_Dam_landslide.jpg |
| `aerial_slide_1963` | c818 | 1963 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Disastro Vajont.jpg」　https://commons.wikimedia.org/wiki/File:Disastro_Vajont.jpg |
| `dam_from_debris_1963` | c821 | 1963 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Vajont Dam 1963.jpg」　https://commons.wikimedia.org/wiki/File:Vajont_Dam_1963.jpg |
| `gorge_exit_1963` | c822 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「Vajont1963 8.jpg」　https://commons.wikimedia.org/wiki/File:Vajont1963_8.jpg |
| `longarone_before_after` | c901 | 1963 | PD（米連邦 §105＋伊の単純写真＝撮影から20年） | 撮影者不明・U.S. Army | Wikimedia Commons「Longarone disastro.jpg」　https://commons.wikimedia.org/wiki/File:Longarone_disastro.jpg |
| `rubble_tower_1963` | c902 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「Vajont1963 5.jpg」　https://commons.wikimedia.org/wiki/File:Vajont1963_5.jpg |
| `longarone_above_1963` | c903 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | U.S. Army | Wikimedia Commons「Longarone 1963.jpg」　https://commons.wikimedia.org/wiki/File:Longarone_1963.jpg |
| `pirago_tower_1963` | c904 | 1963 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Campanile Pirago.jpg」　https://commons.wikimedia.org/wiki/File:Campanile_Pirago.jpg |
| `rail_bridge_1963` | c905 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「Disastro del Vajont, 9 ottobre 1963 (2).jpg」　https://commons.wikimedia.org/wiki/File:Disastro_del_Vajont,_9_ottobre_1963_(2).jpg |
| `piave_valley_1963` | c909 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「Disastro del Vajont, 9 ottobre 1963.jpg」　https://commons.wikimedia.org/wiki/File:Disastro_del_Vajont,_9_ottobre_1963.jpg |
| `temp_bridge_1963` | c911 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「DisastroVajont5.jpg」　https://commons.wikimedia.org/wiki/File:DisastroVajont5.jpg |
| `army_trucks_1963` | c912 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「Vajont1963 2.jpg」　https://commons.wikimedia.org/wiki/File:Vajont1963_2.jpg |
| `tent_camp_1963` | c913 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「Vajont1963 1.jpg」　https://commons.wikimedia.org/wiki/File:Vajont1963_1.jpg |
| `tents_above_1963` | c914 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「Disastro del Vajont, 9 ottobre 1963 (1).jpg」　https://commons.wikimedia.org/wiki/File:Disastro_del_Vajont,_9_ottobre_1963_(1).jpg |
| `bulldozer_1963` | c915 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「Vajont1963 4.jpg」　https://commons.wikimedia.org/wiki/File:Vajont1963_4.jpg |
| `valley_above_1963` | c916 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | U.S. Army | Wikimedia Commons「Vajont1963usarmy.jpg」　https://commons.wikimedia.org/wiki/File:Vajont1963usarmy.jpg |
| `ruined_house_1963` | c917 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「DisastroVajont10.jpg」　https://commons.wikimedia.org/wiki/File:DisastroVajont10.jpg |
| `pirago_tower2_1963` | c920 | 1963 | PD（伊の単純写真＝撮影から20年） | 撮影者不明 | Wikimedia Commons「Longarone Pirago.jpg」　https://commons.wikimedia.org/wiki/File:Longarone_Pirago.jpg |
| `dam_now_downstream` | ca03 cb04 | 2008 | PD（撮影者本人の宣言） | Riccardo Sartor | Wikimedia Commons「Diga Vajont.jpg」　https://commons.wikimedia.org/wiki/File:Diga_Vajont.jpg |
| `dam_now_below` | ca07 cb17 | 2003 | CC BY 3.0 | Stefano Petri | Wikimedia Commons「Diga del Vajont - panoramio.jpg」　https://commons.wikimedia.org/wiki/File:Diga_del_Vajont_-_panoramio.jpg |
| `lake_now` | ca23 cb07 | 2015 | CC BY 4.0 | Gianmarco139 | Wikimedia Commons「Vale dal Vajont.jpg」　https://commons.wikimedia.org/wiki/File:Vale_dal_Vajont.jpg |
| `slide_surface_now` | ca24 cb06 | 2005 | CC BY 2.5 | Christian Thiergan | Wikimedia Commons「Bergsturz Monte Toc Vajont.jpg」　https://commons.wikimedia.org/wiki/File:Bergsturz_Monte_Toc_Vajont.jpg |
| `sign_2023` | cb09 | 2023 | PD（米連邦の職務著作 17 U.S.C. §105） | U.S. Army・Sgt. Bobbi-Jo McGinley | Wikimedia Commons「SETAF-AF remembers Vajont Dam (8062917).jpg」　https://commons.wikimedia.org/wiki/File:SETAF-AF_remembers_Vajont_Dam_(8062917).jpg |
| `memorial_cross_1963` | cb10 | 1963 | PD（伊の単純写真＝撮影から20年・米国も PD-1996） | イタリア消防 | Wikimedia Commons「DisastroVajont6.jpg」　https://commons.wikimedia.org/wiki/File:DisastroVajont6.jpg |
| `pg1` | c112 | 1965 | 保護の外（伊著作権法 第5条＝国の公文書）／Senato della Repubblica の公開版 | イタリア議会 ヴァイオント災害調査委員会 | senato_doc76bis_285307.pdf PDF 1頁 |
| `pg171` | c819 | 1965 | 保護の外（伊著作権法 第5条＝国の公文書）／Senato della Repubblica の公開版 | イタリア議会 ヴァイオント災害調査委員会 | senato_doc76bis_285307.pdf PDF 171頁 |
| `pg178` | ca06 | 1965 | 保護の外（伊著作権法 第5条＝国の公文書）／Senato della Repubblica の公開版 | イタリア議会 ヴァイオント災害調査委員会 | senato_doc76bis_285307.pdf PDF 178頁 |
| `pg179` | c416 | 1965 | 保護の外（伊著作権法 第5条＝国の公文書）／Senato della Repubblica の公開版 | イタリア議会 ヴァイオント災害調査委員会 | senato_doc76bis_285307.pdf PDF 179頁 |
| `pg207` | c910 ca08 | 1965 | 保護の外（伊著作権法 第5条＝国の公文書）／Senato della Repubblica の公開版 | イタリア議会 ヴァイオント災害調査委員会 | senato_doc76bis_285307.pdf PDF 207頁 |
| `pg217` | c412 | 1965 | 保護の外（伊著作権法 第5条＝国の公文書）／Senato della Repubblica の公開版 | イタリア議会 ヴァイオント災害調査委員会 | senato_doc76bis_285307.pdf PDF 217頁 |
| `pg225` | c516 | 1965 | 保護の外（伊著作権法 第5条＝国の公文書）／Senato della Repubblica の公開版 | イタリア議会 ヴァイオント災害調査委員会 | senato_doc76bis_285307.pdf PDF 225頁 |
| `pg226` | c606 | 1965 | 保護の外（伊著作権法 第5条＝国の公文書）／Senato della Repubblica の公開版 | イタリア議会 ヴァイオント災害調査委員会 | senato_doc76bis_285307.pdf PDF 226頁 |

## スレッシャー号のリメイク（1963-04-10・18本目）

※2026-10-04（⑤b-7a）。`qa_out/ep18_assets.py credits --write` が書く（手で直さない）。旧版（3本目）の節は上の「USS Thresher (SSN-593)（1963-04-10・3本目）」＝旧版の誤り（Anefo の1点を「米海軍」・シーウルフの記録を「スカイラーク」）は直さない（公開ずみ・⑥で非公開にするだけ）。18本目は Anefo の1点（写っているのはノーチラス）とシーウルフの記録の頁を使わない。

### 1. 写真（すべて米海軍の職務著作＝PD）
- 出どころは3つ：NARA 289-T（RG 289・1963〜64年の捜索のアルバム・NARA の表示 Use: Unrestricted）／NARA 428-N（RG 428）・記録映画 85185 のコマ（RG 428・作り手は海軍写真センター）／Wikimedia Commons（隠しカテゴリ `PD US Navy`＋`CC-PD-Mark`）
- 🔴 289-T の英字の説明札・428-N の台紙と札は**切り落とした**（`qa_out/ep18_assets.py` の crop＝OCR の文字の箱の外で切る）。頁全体を見せる `page24`（c911＝角の黒い塗り）だけ札が残る
- 🔴 人が写る写真（§B2-2）：就役式（1961-08-03）の左の座った観客（私人）は**切り落とした**（x 385 より左）。甲板の乗員と式台の造船所の人（公的な任務）は残る（原寸で顔 約10px）。進水（1960）の岸の人は全員が後ろ姿か横向き
- 撮影年が書かれていない・割れる点（289-T の造船所の写真2点と謝辞の頁の航走写真・スカイラークの2点）は撮影年を「不明」にし、**副題に年を書かない**（門番 credits）
- 記録映画のコマは画素が縦長（SAR 10:11）＝655×480 に直した。動く映像（記録映画）は §4（⑤b-7c で `clips.json`）
- Commons の新しい8点は、落とす前に一覧（名前・大きさ）でカズヤくんの了承を取った（2026-10-04）＝取ったファイルは Commons の原本と SHA-1 が一致（`ref/ep18/img/fetched.json`＝git の外）

### 2. 頁（査問会の記録・証拠・上級の意見書・議会の本・国防総省の発表の紙）＝⑤b-7b（2026-10-05）
- 欄 `pg<通し頁>`＝台本の通し頁（V1＝p1〜300・X＝p1001〜・IR18＝p2001〜・R08＝p4001〜・J＝印刷頁＋8000・No.710-64＝p9801）。画面の出典は資料の名と頁（`illu.rec_line`）
- 🔴 画面に映す頁は**見た目の字がある版だけ**（V1 の見えない43頁は使わない＝映像方針 §9）。塗り（b(1)・(b)(6)・［classified matter deleted］）は公開の版のまま
- 頁は灰色の PNG（PDF を 200dpi・議会の本は 300dpi・海図は 100dpi で描いた）。薄い海図（c910）は SPEC の `levels` で濃淡だけ強める＝出典の行に「濃淡補正」
- 名簿（認定4・R08 p.181）と名簿の終わり（p.184）の名前＝公務の乗員と、公務を果たすために乗っていた造船所・会社の人（認定6）＝実名の線（§B2-1）の内

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `bow_1961` | c114 c709 | 1961 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 175539769（428-N-1057645）　https://catalog.archives.gov/id/175539769 |
| `commission_1961` | c116 c215 | 1961 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「SSN593 service entering.jpg」　https://commons.wikimedia.org/wiki/File:SSN593_service_entering.jpg |
| `launch_1960` | c201 | 1960 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「USN 1048964 USS Thresher (SSN-593).jpg」　https://commons.wikimedia.org/wiki/File:USN_1048964_USS_Thresher_(SSN-593).jpg |
| `underway_1961` | cb23 | 1961 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「USS Thresher (SSN-593).jpg」　https://commons.wikimedia.org/wiki/File:USS_Thresher_(SSN-593).jpg |
| `running_t2` | c220 c423 c627 | 不明 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-2　https://catalog.archives.gov/id/138924735 |
| `shipyard_sail_t14` | c203 | 不明 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-14　https://catalog.archives.gov/id/138924735 |
| `shipyard_stern_t22` | c208 c611 | 不明 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-22　https://catalog.archives.gov/id/138924735 |
| `bottle_t37` | c722 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-37　https://catalog.archives.gov/id/138924735 |
| `hull_aft_t33` | c805 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-33　https://catalog.archives.gov/id/138924735 |
| `break78_t29` | c812 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-29　https://catalog.archives.gov/id/138924735 |
| `tail_t23` | c819 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-23　https://catalog.archives.gov/id/138924735 |
| `break78_top_t30` | c822 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-30　https://catalog.archives.gov/id/138924735 |
| `sail_t16` | c906 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-16　https://catalog.archives.gov/id/138924735 |
| `page24` | c911 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-24（頁全体）　https://catalog.archives.gov/id/138924735 |
| `stern_plane_t26` | c914 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-26　https://catalog.archives.gov/id/138924735 |
| `rudder_t24` | c920 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-24　https://catalog.archives.gov/id/138924735 |
| `plating_t39` | ca05 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-39　https://catalog.archives.gov/id/138924735 |
| `debris_711302` | ca06 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「330-PSA-110-63 (USN 711302) (22171571340).jpg」　https://commons.wikimedia.org/wiki/File:330-PSA-110-63_(USN_711302)_(22171571340).jpg |
| `bow_plating_t5` | ca13 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-5　https://catalog.archives.gov/id/138924735 |
| `tracks_t41` | ca20 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | NARA 138924735（289-T）「Photographs Taken During the Search for the USS Thresher」 289-T-41　https://catalog.archives.gov/id/138924735 |
| `film_a` | （章ファイル） | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍の記録映画 | NARA 85185（RG 428）「USS THRESHER (SSN-593)」記録映画 1963年3月　https://catalog.archives.gov/id/85185 |
| `film_b` | （章ファイル） | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍の記録映画 | NARA 85185（RG 428）「USS THRESHER (SSN-593)」記録映画 1963年3月　https://catalog.archives.gov/id/85185 |
| `film_c` | （章ファイル） | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍の記録映画 | NARA 85185（RG 428）「USS THRESHER (SSN-593)」記録映画 1963年3月　https://catalog.archives.gov/id/85185 |
| `skylark_front` | c304 c523 | 不明 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「USS Skylark (ASR-20).jpg」　https://commons.wikimedia.org/wiki/File:USS_Skylark_%28ASR-20%29.jpg |
| `skylark_side` | c306 c511 c415 | 不明 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「USS Skylark (ASR-20) underway c1950.jpg」　https://commons.wikimedia.org/wiki/File:USS_Skylark_%28ASR-20%29_underway_c1950.jpg |
| `door_711348` | ca10 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「330-PSA-191-63 (USN 711348) (22171493730).jpg」　https://commons.wikimedia.org/wiki/File:330-PSA-191-63_%28USN_711348%29_%2822171493730%29.jpg |
| `pipe_711350` | ca11 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「330-PSA-191-63 (USN 711350) (22172651149).jpg」　https://commons.wikimedia.org/wiki/File:330-PSA-191-63_%28USN_711350%29_%2822172651149%29.jpg |
| `trieste2_sea` | ca14 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「330-PSA-309-64 (KN-9302C) (22766865552).jpg」　https://commons.wikimedia.org/wiki/File:330-PSA-309-64_%28KN-9302C%29_%2822766865552%29.jpg |
| `trieste2_drawing` | ca17 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「330-PSA-276-63 (USN 711389) (22517726786).jpg」　https://commons.wikimedia.org/wiki/File:330-PSA-276-63_%28USN_711389%29_%2822517726786%29.jpg |
| `fish_1104636` | ca18 | 1964 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「330-PSA-309-64 (USN 1104636-D) (22592418930).jpg」　https://commons.wikimedia.org/wiki/File:330-PSA-309-64_%28USN_1104636-D%29_%2822592418930%29.jpg |
| `search_ships_1963` | cb09 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105） | 米海軍 | Wikimedia Commons「Ships searching for USS Thresher (SSN-593), 15 April 1963 (NH 97555).jpg」　https://commons.wikimedia.org/wiki/File:Ships_searching_for_USS_Thresher_%28SSN-593%29%2C_15_April_1963_%28NH_97555%29.jpg |
| `pg38` | c414 c909 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105）／海軍が FOIA の訴えで公開（第1回・2020-09-23） | 米海軍 スレッシャー号の査問会 | inquiry_vol1_p1-300.pdf PDF 38頁 |
| `pg57` | c104i | 1963 | PD（米連邦の職務著作 17 U.S.C. §105）／海軍が FOIA の訴えで公開（第1回・2020-09-23） | 米海軍 スレッシャー号の査問会 | inquiry_vol1_p1-300.pdf PDF 57頁 |
| `pg183` | c316 | 1963 | PD（米連邦の職務著作 17 U.S.C. §105）／海軍が FOIA の訴えで公開（第1回・2020-09-23） | 米海軍 スレッシャー号の査問会 | inquiry_vol1_p1-300.pdf PDF 183頁 |
| `pg1061` | c508 | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第9・10回・2021-05） | 米海軍 スレッシャー号の査問会（証拠） | inquiry_9_10.pdf PDF 61頁 |
| `pg1120` | c516 | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第9・10回・2021-05） | 米海軍 スレッシャー号の査問会（証拠） | inquiry_9_10.pdf PDF 120頁 |
| `pg1131` | c307 | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第9・10回・2021-05） | 米海軍 スレッシャー号の査問会（証拠） | inquiry_9_10.pdf PDF 131頁 |
| `pg1135` | c910 | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第9・10回・2021-05） | 米海軍 スレッシャー号の査問会（証拠） | inquiry_9_10.pdf PDF 135頁 |
| `pg1531` | c105 | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第9・10回・2021-05） | 米海軍 スレッシャー号の査問会（証拠） | inquiry_9_10.pdf PDF 531頁 |
| `pg1533` | c105t cb21 | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第9・10回・2021-05） | 米海軍 スレッシャー号の査問会（証拠） | inquiry_9_10.pdf PDF 533頁 |
| `pg2001` | c104o c109 | 1965 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第18回） | 米海軍長官（上級の意見書） | navy_IR18.pdf PDF 1頁 |
| `pg2005` | （c104＝⑤b-8） | 1965 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第18回） | 米海軍長官（上級の意見書） | navy_IR18.pdf PDF 5頁 |
| `pg4181` | cb22 | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第8回） | 米海軍 スレッシャー号の査問会 | navy_IR08.pdf PDF 181頁 |
| `pg4184` | c303 | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第8回） | 米海軍 スレッシャー号の査問会 | navy_IR08.pdf PDF 184頁 |
| `pg4204` | （c104＝⑤b-8） | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第8回） | 米海軍 スレッシャー号の査問会 | navy_IR08.pdf PDF 204頁 |
| `pg4220` | cb21t | 1963 | PD（米連邦の職務著作）／海軍が FOIA の訴えで公開（第8回） | 米海軍 スレッシャー号の査問会 | navy_IR08.pdf PDF 220頁 |
| `pg8013` | c623 | 1965 | PD（米議会の刊行物）／Stanford Digital Repository の PDF（印刷頁＋14＝PDF の頁） | 米議会 両院原子力合同委員会 | jcae1965_stanford.pdf PDF 27頁 |
| `pg8038` | c712 | 1965 | PD（米議会の刊行物）／Stanford Digital Repository の PDF（印刷頁＋14＝PDF の頁） | 米議会 両院原子力合同委員会 | jcae1965_stanford.pdf PDF 52頁 |
| `pg8079` | cb12 | 1965 | PD（米議会の刊行物）／Stanford Digital Repository の PDF（印刷頁＋14＝PDF の頁） | 米議会 両院原子力合同委員会 | jcae1965_stanford.pdf PDF 93頁 |
| `pg8089` | c814 | 1965 | PD（米議会の刊行物）／Stanford Digital Repository の PDF（印刷頁＋14＝PDF の頁） | 米議会 両院原子力合同委員会 | jcae1965_stanford.pdf PDF 103頁 |
| `pg8112` | c721 | 1965 | PD（米議会の刊行物）／Stanford Digital Repository の PDF（印刷頁＋14＝PDF の頁） | 米議会 両院原子力合同委員会 | jcae1965_stanford.pdf PDF 126頁 |
| `pg8122` | c905 | 1965 | PD（米議会の刊行物）／Stanford Digital Repository の PDF（印刷頁＋14＝PDF の頁） | 米議会 両院原子力合同委員会 | jcae1965_stanford.pdf PDF 136頁 |
| `pg8160` | c903 | 1965 | PD（米議会の刊行物）／Stanford Digital Repository の PDF（印刷頁＋14＝PDF の頁） | 米議会 両院原子力合同委員会 | jcae1965_stanford.pdf PDF 174頁 |
| `pg9801` | ca15 | 1964 | PD（米連邦の職務著作）／Wikimedia Commons「330-PSA-309-64a (22791587391).jpg」（NARA RG 330） | 米国防総省 | cm_330-PSA-309-64a__22791587391_.jpg |

### 3. フリー素材の映像（イメージ）＝⑤b-7b（2026-10-05 カズヤくん了承・頭の1行の差し込み11カット＝差し込みは ⑤b-7c）
- ルール §2-5c：画面に「イメージ（フリー素材）：サイト名／撮影者」を出す・【映像あり】と20%に数えない・動画はリポに入れない（`ref/ep18/stock/`＝git の外・本番は Actions が URL から取る）
- ライセンス：Pexels License（https://www.pexels.com/license/）／Pixabay Content License（https://pixabay.com/service/license-summary/）＝商用可・クレジット不要・改変可。生成AI＝Pexels は規約で投稿を認めない・Pixabay は印を付ける（選んだ点に印なし）

- `docs_binders_7710340`（c109）机の上に積んだ書類の綴じ込み（人は写らない）＝Pexels・Kaboompics・投稿 2021-04-29・2048×1080・12.8秒・Pexels License・取った日 2026-10-05　https://www.pexels.com/video/documents-on-the-table-7710340/
- `deep_rays_63427`（c114）水の中から見上げた水面と光の筋＝Pixabay・Jackdrafahl・投稿 2021-01-30・2560×1440・23.4秒・Pixabay Content License・取った日 2026-10-05　https://pixabay.com/videos/waves-ocean-sea-underwater-water-63427/
- `pier_blue_10354787`（c215）桟橋の杭と海面のさざ波（人・船なし）＝Pexels・Engin Akyurt・投稿 2021-11-26・2048×1080・59.93秒・Pexels License・取った日 2026-10-05　https://www.pexels.com/video/ripples-in-water-surface-under-a-pier-10354787/
- `pier_dark_11812247`（c220）桟橋の下の暗い海面（人・船なし）＝Pexels・Engin Akyurt・投稿 2022-04-14・2048×1080・60.03秒・Pexels License・取った日 2026-10-05　https://www.pexels.com/video/ripples-on-seawater-under-a-pier-11812247/
- `sea_dark_5668613`（c511）暗い沖の海面＝Pexels・ROMAN ODINTSOV・投稿 2020-10-22・2048×1080・8.01秒・Pexels License・取った日 2026-10-05　https://www.pexels.com/video/dark-surface-of-the-deep-water-5668613/
- `deep_sun_48596`（c805）水の中から見上げた太陽（暗い青）＝Pixabay・ChristianBodhi・投稿 2020-09-04・2560×1440・20.0秒・Pixabay Content License・取った日 2026-10-05　https://pixabay.com/videos/underwater-rays-light-sun-48596/
- `deep_blue_32790667`（c812）青い水の中に差す光の筋＝Pexels・JUN HO LEE・投稿 2025-06-30・1920×1080・14.63秒・Pexels License・取った日 2026-10-05　https://www.pexels.com/video/underwater-ocean-view-with-sunlight-rays-32790667/
- `typewriter_33068304`（c903）古いタイプライターの活字の寄り＝Pexels・Stefan・投稿 2025-07-18・1920×1080・48.6秒・Pexels License・取った日 2026-10-05　https://www.pexels.com/video/vintage-typewriter-typing-close-up-33068304/
- `files_hands_6549976`（c906）引き出しの記録のカードを手で繰る（顔は写らない）＝Pexels・Tima Miroshnichenko・投稿 2021-01-20・1920×1080・21.61秒・Pexels License・取った日 2026-10-05　https://www.pexels.com/video/looking-among-files-6549976/
- `seabed_sand_11781634`（ca05）光のゆらぐ砂の海底（タイムラプス）＝Pexels・Markus Winkler・投稿 2022-04-11・1920×1080・45.93秒・Pexels License・取った日 2026-10-05　https://www.pexels.com/video/time-lapse-of-a-sandy-seabed-11781634/
- `seabed_murky_33896777`（ca06）砂の動く海の底（濁った青緑）＝Pexels・JUN HO LEE・投稿 2025-09-14・1920×1080・15.6秒・Pexels License・取った日 2026-10-05　https://www.pexels.com/video/underwater-ocean-floor-with-sand-movement-33896777/

### 4. 記録映画（動く映像）＝⑤b-7c（2026-10-05・取得は 10-04 カズヤくん了承＝丸ごとは保存しない）
- NARA RG 428（海軍写真センター 428-NPC）の記録映画＝米海軍の職務著作＝PD（17 U.S.C. §105）。NARA の表示 Use: Undetermined（未判定＝制限ではない）。画面の出典＝「出典：米海軍の記録映画（NARA <naId>・パブリックドメイン）」
- すべて 720×480・画素が縦長（SAR 10:11）＝655×480 に直して額装＋地のぼかし（映像方針 §8）。【映像あり】は付けない
- 本番（Actions・Modal）は `tools/footage.py` が URL から使う区間だけ切り出す（落とさない＝`"range": true`）。ショットの境目は `ref/ep18/shots.json`（1秒刻み）・使う区間は `footage.USE`

- NARA 85185「USS THRESHER (SSN-593)」カラーの航走（セイルの593・艦橋の乗員）・789秒　https://catalog.archives.gov/id/85185
- NARA 83213「LAUNCHING OF USS THRESHER (SSN-593) Naval Shipyard, Portsmouth」1960年の進水（空から見た造船所と艦）・190秒　https://catalog.archives.gov/id/83213
- NARA 83750「SEARCH FOR USS THRESHER (SSN-593)」捜索の海の艦（空から）・282秒　https://catalog.archives.gov/id/83750
- NARA 83751「SEARCH FOR USS THRESHER (SSN-593)」捜索の艦（空から・艦番号179 ほか）・311秒　https://catalog.archives.gov/id/83751
- NARA 83746「SEARCH FOR USS THRESHER (SSN-593) On Board USS ALLEGHENY (ATA-179)」アレゲニーの艦上の乗員と機器（乗用車の場面は使わない）・505秒　https://catalog.archives.gov/id/83746
- NARA 83737「SEARCH FOR USS THRESHER (SSN-593) 250 Miles East of Cape Cod over Atlantic」哨戒機から見た捜索の海・515秒　https://catalog.archives.gov/id/83737
- NARA 83759「SEARCH FOR USS THRESHER (SSN-593) Naval Shipyard, Boston, Mass」ボストンの造船所・艦番号422 の潜水艦（トロ）・178秒　https://catalog.archives.gov/id/83759
- NARA 83795「THRESHER SEARCH 220 Miles East of Cape Cod at Sea」海の上の初代トリエステ・248秒　https://catalog.archives.gov/id/83795
- NARA 83766「SEARCH FOR USS THRESHER (SSN-593) Boston Naval Shipyard」ボストンの造船所・194秒　https://catalog.archives.gov/id/83766
- NARA 83757「SEARCH FOR USS THRESHER (SSN-593) TRIESTE Test Dive Boston, Mass. & at Sea」初代トリエステの試験潜航（1963-05-03・ボストンの東 約60マイル）・643秒　https://catalog.archives.gov/id/83757
- NARA 83741「USS THRESHER (SSN-593) MEMORIALS」追悼（参列者の顔のショットは使わない）・575秒　https://catalog.archives.gov/id/83741
- NARA 83740「THRESHER MEMORIAL SERVICE Portsmouth, N. H」ポーツマスの追悼の式（頭2秒は NARA のロゴ・顔の分かるショットは使わない）・328秒　https://catalog.archives.gov/id/83740

## サーフサイドのマンション崩壊のリメイク（2021-06-24・19本目）

※2026-10-06（⑤b-7a）。`qa_out/ep19_assets.py credits --write` が書く（手で直さない）。旧版の節は上の「4本目：サーフサイド（Champlain Towers South・2021-06-24）」＝直さない（公開ずみ）。

### 1. 写真（NIST・FEMA〈DVIDS〉・DHS＝米連邦の職務著作 PD／マイアミ・デイド郡消防＝フロリダ州の公記録／CC BY 2.0）
- 🔴 **郡の消防の写真（Commons の PD-FLGov）は画面に「PD」と書かない**（決め①・10-06 カズヤくん）＝「マイアミ・デイド郡消防（フロリダ州の公記録）」
- 🔴 CC BY-SA は使わない（決め③）。CC BY 2.0 の1点（Steve Jurvetson）は章の色のデュオトーン＝色の改変＝出典に「色調を変更」
- 🔴 もとから在る大きな商標・社名・電話番号・顔の近い人（郡警察の鑑識）は束の中で**切り落とした**（`qa_out/ep19_assets.py` の CROP＝⑤b-1 の原寸で決めた箱）。車のナンバー1つは**モザイク**（PD の写真だけ・BLUR）
- 🔴 人が写る写真（§B2-2）：救助隊・調査員は公務。住戸の中は引きだけ（決め⑤）・追悼の場は DHS の引きだけ（決め⑥）
- 撮影年＝写真の説明（NIST・DVIDS・Commons）から映像方針で書いた副題の年。副題に年の無い写真は「不明」

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `c01_mdfr1` | c702 | 2021 | Public domain（PD-FLGov の可能性） | マイアミ・デイド郡消防（フロリダ州の公記録） | File:Surfside condominium collapse photo from Miami-Dade Fire Rescue 1.jpg |
| `c04_mdfr4` | c621 | 2021 | Public domain（PD-FLGov の可能性） | マイアミ・デイド郡消防（フロリダ州の公記録） | File:Surfside condominium collapse photo from Miami-Dade Fire Rescue 4.jpg |
| `c06_mdfr6` | c703 | 2021 | Public domain（PD-FLGov の可能性） | マイアミ・デイド郡消防（フロリダ州の公記録） | File:Surfside condominium collapse photo from Miami-Dade Fire Rescue 6.jpg　モザイク [[298, 774, 350, 802]] |
| `c13_jurvetson` | c923 | 2021 | CC BY 2.0（CC BY 2.0） | Steve Jurvetson（CC BY 2.0） | File:Remains of the Collapsed Florida Surfside Condo (2021-10-04).jpg |
| `d06_dhs` | cc01 | 2021 | Public domain（A（DHS）） | 米国土安全保障省（DHS） | File:DHS Secretary Alejandro Mayorkas Visits Surfside Condo Collapse Site (51390531311).jpg |
| `d13_dhs` | cc06 | 2021 | Public domain（A（DHS）） | 米国土安全保障省（DHS） | File:DHS Secretary Alejandro Mayorkas Visits Surfside Condo Collapse Site (51390783308).jpg　切り出し [1500, 0, 2500, 562] |
| `f6717685_debris` | c709 | 2021 | Public domain（A（FEMA）） | FEMA（DVIDS） | https://www.dvidshub.net/image/6717685/fema-assists-recovery-surfside-building-collapse |
| `f6717686_debris` | c707 | 2021 | Public domain（A（FEMA）） | FEMA（DVIDS） | https://www.dvidshub.net/image/6717686/fema-assists-recovery-surfside-building-collapse　切り出し [325, 125, 2000, 1068] |
| `f6723297_team` | c713 | 2021 | Public domain（A（FEMA）） | FEMA（DVIDS） | https://www.dvidshub.net/image/6723297/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery |
| `f6723299_pa_tf1` | c708 | 2021 | Public domain（A（FEMA）） | FEMA（DVIDS） | https://www.dvidshub.net/image/6723299/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery |
| `n03_chloride` | c916 | 2022 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2022/06/15/Ruthie%20Corzo.jpg |
| `n10_column_before` | c419 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2021/08/25/KAM_3717%28July6th%29.JPG　切り出し [252, 588, 5082, 4480] |
| `n11_column_move` | ca19 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2021/08/25/KAM_3753%20%28july7th%29.JPG　切り出し [1260, 630, 6720, 3700] |
| `n12_concrete` | c319 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2021/08/25/NIST%20team%20July1.jpg　切り出し [0, 300, 2900, 1931] |
| `n13_laydown` | c524 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2021/08/25/NIST%20team%20July2.jpg |
| `n16_column_tag` | c715 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2021/08/25/KAM_3691%28July6th%29.JPG　切り出し [0, 1386, 5124, 4267] |
| `n17_remaining` | ca13 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2021/06/30/IMG_6362.JPG　切り出し [0, 0, 4032, 2268] |
| `n18_from_south` | c701 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2021/07/19/IMG_0122-%28Jonathan-070721%29.jpg |
| `n19_lidar` | c716 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2021/07/15/Lidar%20and%20other%20instruments%20.jpg |
| `n20_police_escort` | c717 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2021/07/15/IMG_0428.JPG　切り出し [0, 1008, 3583, 3024] |
| `n28_warehouse_column` | cc21 | 2023 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2023/05/31/image8.jpg |
| `n33_coring` | c317 | 2023 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2023/09/06/Coring%20and%20MOA%20tests%20%20%28Sep2023%29.jpg　切り出し [0, 580, 4032, 2848] |
| `n42_absorption` | c915 | 2024 | Public domain（A） | R. Eskalis/NIST | https://www.nist.gov/sites/default/files/images/2024/09/12/NCSTInvestigation_BrollReel07_v01.00_00_14_16.Still005.jpg |
| `n43_model` | cb04 | 2023 | Public domain（A） | L. Gerskovic/NIST | https://www.nist.gov/sites/default/files/images/2024/11/21/CNST%20CTS%20Update%20Dec.jpg |
| `n44_aerial_photos` | c720 | 不明 | Public domain（A） | L. Gerskovic/NIST | https://www.nist.gov/sites/default/files/images/2024/11/21/CNST%20CTS%20Update%20Dec-2.jpg |
| `n48_lidar_0714` | ca21 | 2021 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2025/02/04/Lidar_Data_from_Leica_C10_July-14-2021.jpg |
| `n53_after_test` | cc27 | 2025 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%289%20of%2038%29.jpg　切り出し [389, 137, 2972, 1591] |
| `n60_mast_after` | ca09 | 2025 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2831%20of%2038%29.jpg |
| `n61_shear_uw` | c818 | 2025 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2839%20of%204%29.jpg |
| `n66_slab_section` | c812 | 2025 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2025/06/20/June%20CTS%20Update%20Concrete%20Slab.jpg |
| `n69_corroded_bars` | c813 | 2025 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%287%20of%207%29.jpg |
| `n70_slab_cracks` | c812 | 2025 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%288%20of%207%29.jpg |
| `n71_mast_test` | cc23 | 不明 | Public domain（A） | NIST | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%283%20of%207%29.jpg |
| `ncst_p047` | c618 | 2021 | Public domain（映像のコマは引用）（A＋第三者（引用）） | NIST（諮問委員会の資料 2026年9月 p.47）・映像のコマ：© 2021 Used with permission | NIST 諮問委員会（NCST Advisory Committee）2026年9月の資料 |
| `tf_p003_model` | c205 c206 | 不明 | Public domain（A） | NIST（技術的知見の動画のスライド3） | NIST 技術的知見の動画（2026年6月） |
| `tf_p050_3d` | c502 | 不明 | Public domain（A） | NIST（技術的知見の動画のスライド50） | NIST 技術的知見の動画（2026年6月） |
| `tf_p050_gate` | c504 | 不明 | Public domain（A） | NIST（技術的知見の動画のスライド50・目撃談にもとづく絵） | NIST 技術的知見の動画（2026年6月） |
| `tf_p052_gate` | c509 | 不明 | Public domain（A） | NIST（技術的知見の動画のスライド52・目撃談にもとづく絵） | NIST 技術的知見の動画（2026年6月） |
| `tf_p057_3d` | c515 | 不明 | Public domain（A） | NIST（技術的知見の動画のスライド57） | NIST 技術的知見の動画（2026年6月） |
| `tf_p057_memo` | c516 | 不明 | Public domain（下地の図は引用）（A＋第三者（引用）） | NIST（技術的知見の動画のスライド57）・下地の図：管財人（CTS Receiver） | NIST 技術的知見の動画（2026年6月） |
| `tf_p058_note` | c520 | 不明 | Public domain（下地の図は引用）（A＋第三者（引用）） | NIST（技術的知見の動画のスライド58）・下地の図：管財人（CTS Receiver） | NIST 技術的知見の動画（2026年6月） |
| `tf_p075_cover` | c906 | 不明 | Public domain（A） | NIST（技術的知見の動画のスライド75） | NIST 技術的知見の動画（2026年6月） |
| `tf_p076_bars` | c909 | 不明 | Public domain（下地の図は引用）（A＋第三者（引用）） | NIST（技術的知見の動画のスライド77）・図面：Town of Surfside | NIST 技術的知見の動画（2026年6月） |
| `tf_p084_salt` | c811 | 不明 | Public domain（A） | NIST（技術的知見の動画のスライド84） | NIST 技術的知見の動画（2026年6月） |
| `tf_p174_corr` | c307 | 不明 | Public domain（A） | NIST（技術的知見の動画のスライド174） | NIST 技術的知見の動画（2026年6月） |
| `tf_p185_87park` | cb07 | 不明 | Public domain（A） | NIST（技術的知見の動画のスライド185） | NIST 技術的知見の動画（2026年6月） |
| `pg3004` | cc02 | 2021 | フロリダ州の公記録（郡の州検事局が公開） | マイアミ・デイド郡の大陪審 | miamidade_grandjury_2021spring_report_redacted.pdf PDF 4頁 |
| `pg3020` | c402 | 2021 | フロリダ州の公記録（郡の州検事局が公開） | マイアミ・デイド郡の大陪審 | miamidade_grandjury_2021spring_report_redacted.pdf PDF 20頁 |
| `pg3021` | c407 c410 | 2021 | フロリダ州の公記録（郡の州検事局が公開） | マイアミ・デイド郡の大陪審 | miamidade_grandjury_2021spring_report_redacted.pdf PDF 21頁 |
| `pg4007` | c310 | 2018 | サーフサイド町が公開した記録（フロリダ州の公記録） | モラビト社（構造技術者） | surfside_morabito_2018-10-08_structural_field_survey.pdf PDF 7頁 |

## 日本航空123便のリメイク（1985-08-12・20本目）

※2026-10-08（⑤b-2）。`qa_out/ep20_assets.py credits --write` が書く（手で直さない）。旧版の節は上の「日本航空123便（1985-08-12・JA8119）　※本番2本目」＝直さない（旧版は 10-05 に非公開）。

### 0. 防衛庁記録（動く映像）
- 防衛省・自衛隊『昭和60年防衛庁記録』（公式 YouTube modchannel・https://www.youtube.com/watch?v=LKrLJc4R0X8）＝頁の表示「クリエイティブ・コモンズ 著作権表示必須ライセンス」＝**CC BY 3.0**。焼くときの媒体は Wikimedia Commons の同じ映画（File:昭和６０年防衛庁記録.webm の 1080p 版）・手元の走査は YouTube の 1080p。
- 使う区間＝c103（上空から見た墜落現場）・c104（ヘリの遠景）・c107（まつゆきのボートの前半）・c503（指揮所＋F-4〈昼の離陸〉）・c601（海の尾翼＋ボートの後半）＝`ref/ep20/eizou_build/bv_shots20.tsv`。改変＝切り出し（4:3 の中身だけ）・額装・再生速度・音なし
- 🔴 使わない区間（`tools/footage.py` の NOGO）：新聞の切り抜き（第三者の著作物）・生存者の救出の寄り・担架と捜索・報道陣の顔

### 1. 写真（報告書 62-2＝PDL1.0／JA8119 の3点＝CC BY 2.0・CC BY-SA 2.0・3.0／御巣鷹の尾根と慰霊の6点＝CC BY 3.0）
- 報告書の写真・付図＝`ref/ja123/`（旧版の取り出し・縮小・ぼかし0.7・頁から切出）を束へ写した＝白黒のまま。PDL1.0 の条件＝出典と加工した旨（画面の出典「／縮小・切出」）
- 🔴 **CC BY-SA の2点（J2・J3）は額装・無加工・色そのまま・上に重ねない・1点1カット**（`cuts/ss.check_frame_only`）。動きは額ごと（絵は切らない）
- 🔴 **写真-124（c408）は地上の第三者の撮影＝引用**（額装・無加工・この1カットだけ・冒頭とサムネに使わない）
- 🆕 写真-14（c310）の白いシャツの男性（制服が無く公的な任務の人か写真から決められない）は**顔だけモザイク**（2026-09-30 カズヤくん「顔面のみのモザイク加工」＝PDL1.0 は手直しを許す・元画像を直す＝`cuts/ss.py` の NEEDS_MASK・`ref/ep20/masked.json`）＝画面の出典に「顔にモザイク」
- CC BY（J1・O1〜O6）は額・寄り・流しで端を切ることがある＝画面の出典に「改変：切出」。20本目は写真を原色で出す（色は変えない）
- 撮影年＝映像方針で書いた副題の年（JA8119＝写真の題・daipresents の6点＝EXIF 2009-08-14 の朝）。副題に年の無い写真は「不明」

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `a1f001` | c803 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `a1f002` | c804 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `a1f003` | c808 c810 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `a1f004` | c821 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `a1p001` | c801 | 1978 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `a1p002` | c802 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f001` | c208 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f002` | c511 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f004` | c202 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f005` | c203 c217 c516 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f008` | c311 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f012` | c205 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f013` | c524 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f014` | c525 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f019` | c420 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f020` | c602 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f021` | cb01 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f027` | c409 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f028` | c603 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f032` | c623 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f036` | c703 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `f037` | c718 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `j1_ja8119_chitose_1985` | c101 | 1985 | CC BY 2.0（Flickr の審査ずみ） | Dennis HKG（Flickr） | https://commons.wikimedia.org/wiki/File:Japan_Airlines_-_Boeing_747SR_-_JA8119_-_Sapporo_Chitose.jpg |
| `j2_ja8119_haneda_19850303` | c201 | 1985 | CC BY-SA 2.0（Flickr の審査ずみ・VRTS の許諾確認） | Stuart Jessup（Flickr） | https://commons.wikimedia.org/wiki/File:BOEING_747SR-46,_JA8119_,_JAPAN_AIRLINES.jpg |
| `j3_ja8119_itami_1984` | c721 | 1984 | CC BY-SA 3.0（GFDL 併記・自作） | Harcmac60（Wikimedia Commons） | https://commons.wikimedia.org/wiki/File:Japan_Airlines_B747SR-46_(JA8119)_at_Itami_Airport_in_1984.jpg |
| `kz018` | cb06 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `o1_osutaka_trailhead` | c106 | 2009 | CC BY 3.0（Panoramio・信頼できる利用者の審査ずみ） | daipresents（Panoramio） | https://commons.wikimedia.org/wiki/File:御巣鷹の尾根・昇魂之碑_新登山道入り口_-_panoramio.jpg |
| `o2_osutaka_stairs` | cc19 | 2009 | CC BY 3.0（Wikimedia Commons） | daipresents（Panoramio） | https://commons.wikimedia.org/wiki/File:2009年に作られた階段と手すり_-_panoramio.jpg |
| `o3_shokon_no_hi` | cc05 | 2009 | CC BY 3.0（Wikimedia Commons） | daipresents（Panoramio） | https://commons.wikimedia.org/wiki/File:Narahara,_Ueno,_Tano_District,_Gunma_Prefecture_370-1617,_Japan_-_panoramio.jpg |
| `o4_sign_r299` | cc01 | 2009 | CC BY 3.0（Wikimedia Commons） | daipresents（Panoramio） | https://commons.wikimedia.org/wiki/File:国道299号線_御巣鷹の尾根の標識_-_panoramio.jpg |
| `o5_sign_p124` | cc16 | 2009 | CC BY 3.0（Wikimedia Commons） | daipresents（Panoramio） | https://commons.wikimedia.org/wiki/File:県道124号線_御巣鷹の尾根の標識_-_panoramio.jpg |
| `o6_ireinosono` | cc08 | 2009 | CC BY 3.0（Wikimedia Commons） | daipresents（Panoramio） | https://commons.wikimedia.org/wiki/File:慰霊の園_慰霊塔_-_panoramio.jpg |
| `p001` | c514 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p002` | c108 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p003` | c421 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p004` | c512 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p005` | c515 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p006` | c615 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p007` | c517 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p008` | c518 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p009` | c520 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p010` | c521 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p012` | c105 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p013` | c605 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p014` | c310 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p015` | c102 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p016` | c218 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p017` | c322 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p018` | c401 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p019` | c316 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p020` | c306 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p021` | c604 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p022` | c613 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p023` | c614 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p024` | c608 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p025` | c609 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p043` | c610 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p058` | c611 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p059` | c612 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p064` | c624 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p065` | c901 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p071` | c701 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p073` | c702 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p077` | c704 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p084` | c719 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p085` | c710 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p086` | c713 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p087` | c909 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p088` | c912 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p092` | c910 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p093` | c911 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p098` | ca01 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p109` | c706 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p110` | c707 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p115` | c709 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p116` | c715 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p119` | c717 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p123` | c716 | 不明 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会（報告書 62-2・昭和62年） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `p124` | c408 | 不明 | 引用（報告書の写真-124）（著作権法32条・第三者の写真） | 第三者（地上の撮影者・報告書に名前の表記なし） | https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html |
| `pg102` | c813 | 1987 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会 | ja_04.pdf PDF 2頁 |
| `pg125` | c907 | 1987 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会 | ja_04.pdf PDF 25頁 |
| `pg126` | ca18 | 1987 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会 | ja_04.pdf PDF 26頁 |
| `pg2001` | ca04 | 2011 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会 | jtsb_kaisetsu.pdf PDF 1頁 |
| `pg3004` | cc06 | 1987 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会 | ja_01.pdf PDF 4頁 |
| `pg311` | c211 | 1987 | PDL1.0（運輸安全委員会 公共データ利用規約） | 運輸安全委員会 | ja_11.pdf PDF 45頁 |

## 9.11 米国同時多発テロのリメイク（2001-09-11・21本目）

※2026-10-12（⑤b-2）。`qa_out/ep21_assets.py credits --write` が書く（手で直さない）。旧版の節は上の「9.11 米国同時多発テロ（2001-09-11・7本目）」＝直さない（旧版は 10-05 に非公開）。

### 0. 動く映像（7本・音はすべて使わない＝`-an`）
- DVIDS 122342／122343／122347＝米空軍（第11通信隊・第1戦闘カメラ隊ほか）の職務＝PD（DVIDS の表示「PUBLIC DOMAIN」）。640×480・画素は正方形でない（SAR 131:128＝表示の幅 655）＝4:3 の額装＋地のぼかし・左右の黒い縁を寄り 1.03 で外す
- WHTV 606・1501＝ホワイトハウス通信局（WHCA＝国防総省の機関）の職務＝PD（ジョージ・W・ブッシュ大統領図書館）。606 は Commons の webm（854×474・16:9＝全画面・右端のレンズの縁の影を寄せで外す）。🔴 **1501 は大統領図書館の YouTube にしか無い**＝使う区間（もとの380〜392秒）だけを `ref/ep21/clip/` に切り出してリポに入れた（Actions・Modal は網から取れない・md5 は clips.json）
- NARA 6171390（大統領の夜の演説・cb01）＝WHCA の職務＝PD（use=Unrestricted）。16:9＝全画面
- 🔴 **1999年の塔（TG99・c205）は CC BY-SA 3.0＋GFDL（Zaqq72）**＝額装・無加工・寄り0・等速・地は無地（`plain=True`）・音なし・1点1カット
- 🔴 使わない窓（`tools/footage.py` の NOGO＝映像方針 §2）：担架と運ばれる人・助けられる人・記者の寄り＝その秒を含むショットまるごと

| 記号 | 使うカット | 画面の出典 | 権利 | 出どころ |
|---|---|---|---|---|
| `DV42` | c101 c105 | 出典：米空軍（DVIDS 122342・パブリックドメイン） | A（米空軍 第11通信隊の職務・DVIDS「PUBLIC DOMAIN」） | https://www.dvidshub.net/video/122342 |
| `DV43` | c104 c109 | 出典：米空軍（DVIDS 122343・パブリックドメイン） | A（米空軍の職務・DVIDS「PUBLIC DOMAIN」） | https://www.dvidshub.net/video/122343 |
| `DV47` | c108 cc10 | 出典：米空軍（DVIDS 122347・パブリックドメイン） | A（米空軍 第1戦闘カメラ隊の職務・DVIDS「PUBLIC DOMAIN」） | https://www.dvidshub.net/video/122347 |
| `W606` | c107 c713 | 出典：ジョージ・W・ブッシュ大統領図書館（WHTV 606・パブリックドメイン） | A（ホワイトハウス通信局 WHCA＝国防総省の機関の職務・大統領図書館「public domain」） | https://commons.wikimedia.org/wiki/File:(2021-0031-F)_WHTV_606_20010911_Arrival,_Departure_and_OTRs_Trip_to_Florida_and_Louisiana.webm |
| `W1501` | c106 | 出典：ジョージ・W・ブッシュ大統領図書館（WHTV 1501・パブリックドメイン） | A（WHCA の職務・大統領図書館「Records of White House Evacuation on September 11, 2001」） | https://www.youtube.com/watch?v=CAaOJiSqWkw |
| `W593` | cb01 | 出典：ジョージ・W・ブッシュ大統領図書館（NARA 6171390・パブリックドメイン） | A（WHCA の職務・NARA 6171390・use=Unrestricted） | https://commons.wikimedia.org/wiki/File:Address_to_Nation_on_Terrorist_Attacks_-_NARA_-_6171390.ogv |
| `TG99` | c205 | 出典：Zaqq72（Wikimedia Commons）／CC BY-SA 3.0／改変なし | F（CC BY-SA 3.0＋GFDL＝額装・無加工・速さも変えない） | https://commons.wikimedia.org/wiki/File:Torri_Gemelle_-_WTC_-_New_York_-_Sept_99.ogv |

### 1. 写真（米連邦の職務〈A〉・議会図書館の撮影者不詳〈C'＝撮影者が権利を放棄〉・知られた制限なし〈D〉・CC BY／BY-SA／CC0）
- 束＝`ref/ep21/photo/`（git の外）の長辺を幅 2400／高さ 1350 まで縮めただけ（色・切り口はそのまま＝原色）。
- 🔴 **D（米議会図書館の「知られた制限なし」）は PD の宣言ではない**＝画面は「米議会図書館蔵／知られた制限なし」（§2-12b）
- 🔴 **CC BY-SA の写真（AA11＝c204）は額装・無加工・色そのまま・上に重ねない・寄り0・1点1カット**（`cuts/ss.check_frame_only`）
- CC BY は額・寄り・流しで端を切ることがある＝画面の出典に「改変：切出」
- 🔴 **イメージ（この事件の物でない写真）**＝`ep21/stock/` の名・画面の左上に「イメージ」・20% に数えない。顔だけモザイクの保留3点（SEC70・SHANK15・TSA20）は ⑤b-7 で2倍に拡大して測った＝私人の分かる顔は0（SEC70＝制服の保安係1人＝公務・SHANK15＝来訪者の顔 約4px の遠景）。🔴 TSA20 は手前の列の客（顔 30〜40px）を束の段階で切り落とした（縦の上 1000px だけ＝「改変：切出」）
- 撮影年＝Commons の頁の日付（上げた日・公開の日・不明のものは出どころの説明から＝`qa_out/ep21_assets.py` の YEAR_FIX）。副題の「当日」は 2001年として照らした

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `df_sd_02_09094` | c621 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米空軍（TSgt Jim Varhegyi） | https://commons.wikimedia.org/wiki/File:DF-SD-02-09094.JPEG |
| `dm_sd_02_03925` | c622 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海兵隊（Cpl J. Ingersoll） | https://commons.wikimedia.org/wiki/File:DM-SD-02-03925.JPEG |
| `dn_sd_03_08938` | cc01 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海軍（PH2 Robert Houlihan） | https://commons.wikimedia.org/wiki/File:DN-SD-03-08938.JPEG |
| `dn_sd_03_11447` | c624 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海軍（PH2 Jim Watson） | https://commons.wikimedia.org/wiki/File:DN-SD-03-11447.JPEG |
| `dod_pentagon_visit_0912` | cb03 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米国防総省 | https://commons.wikimedia.org/wiki/File:George_W._Bush_visits_Pentagon_9-12-01.jpg |
| `dulles_1985` | c206 | 1985 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海軍（PH1 David C. Maclean） | https://commons.wikimedia.org/wiki/File:Aerial_view_of_Dulles_Airport,_June_1985.JPEG |
| `ewr_gate17_flag_2006` | c801 | 2006 | PD（自主宣言）（C） | Tshevlin | https://commons.wikimedia.org/wiki/File:Ewr_flag.jpg |
| `f15_102fw_nyc_2001` | c418 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米空軍 | https://commons.wikimedia.org/wiki/File:102d_FW_F-15_over_NYC_2001.jpg |
| `f15_otis_nyc_2001_11` | c301 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米空軍 | https://commons.wikimedia.org/wiki/File:F-15A_Eagle_of_the_101st_Fighter_Squadron_flying_over_New_York_City_after_September_11,_2001.jpg |
| `f16c_nj_ang_2001_10` | c908 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米空軍（MSgt Don Taggart） | https://commons.wikimedia.org/wiki/File:F-16C_NJ_ANG_in_flight_Oct_2001.jpg |
| `faa_artcc` | c402 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米連邦航空局（FAA） | https://commons.wikimedia.org/wiki/File:AirTraffic-8.jpg |
| `fema_3894_0914` | cb15 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | FEMA（Andrea Booher） | https://commons.wikimedia.org/wiki/File:FEMA_-_3894_-_Photograph_by_Andrea_Booher_taken_on_09-14-2001_in_New_York.jpg |
| `fema_3905_0914` | cb04 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | FEMA（SFC Thomas R. Roberts） | https://commons.wikimedia.org/wiki/File:FEMA_-_3905_-_Photograph_by_SFC_Thomas_R._Roberts_taken_on_09-14-2001_in_New_York.jpg |
| `flight93_memorial_aerial_2024_05` | c828 | 2024 | PD（CC0）（C） | Designism | https://commons.wikimedia.org/wiki/File:Flight_93_National_Memorial_aerial_20241223_(5).jpg |
| `flight93_memorial_aerial_2024_12` | cb18 | 2024 | PD（CC0）（C） | Designism | https://commons.wikimedia.org/wiki/File:Flight_93_National_Memorial_aerial_20241223_(12).jpg |
| `lc_a05_a01` | c513 | 2001 | PD（撮影者が権利を放棄）（C'） | 撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄） | https://commons.wikimedia.org/wiki/File:September_11th_terrorist_attack_on_the_World_Trade_Center_LCCN2002717279_LC-A05-A01.tif |
| `lc_a05_a03` | c514 | 2001 | PD（撮影者が権利を放棄）（C'） | 撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄） | https://commons.wikimedia.org/wiki/File:September_11th_terrorist_attack_on_the_World_Trade_Center_LCCN2002717279_LC-A05-A03.tif |
| `lc_a05_a05` | c701 | 2001 | PD（撮影者が権利を放棄）（C'） | 撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄） | https://commons.wikimedia.org/wiki/File:September_11th_terrorist_attack_on_the_World_Trade_Center_LCCN2002717279_LC-A05-A05.tif |
| `lc_a05_a06` | c519 | 2001 | PD（撮影者が権利を放棄）（C'） | 撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄） | https://commons.wikimedia.org/wiki/File:September_11th_terrorist_attack_on_the_World_Trade_Center_LCCN2002717279_LC-A05-A06.tif |
| `lc_a05_a09` | c609 | 2001 | PD（撮影者が権利を放棄）（C'） | 撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄） | https://commons.wikimedia.org/wiki/File:September_11th_terrorist_attack_on_the_World_Trade_Center_LCCN2002717279_LC-A05-A09.tif |
| `lc_a05_a10` | c706 | 2001 | PD（撮影者が権利を放棄）（C'） | 撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄） | https://commons.wikimedia.org/wiki/File:September_11th_terrorist_attack_on_the_World_Trade_Center_LCCN2002717279_LC-A05-A10.tif |
| `lc_a05_a17` | c102 | 2001 | PD（撮影者が権利を放棄）（C'） | 撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄） | https://commons.wikimedia.org/wiki/File:September_11th_terrorist_attack_on_the_World_Trade_Center_LCCN2002717279_LC-A05-A17.tif |
| `lc_a05_b20` | cc06 | 2001 | PD（撮影者が権利を放棄）（C'） | 撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄） | https://commons.wikimedia.org/wiki/File:September_11th_terrorist_attack_on_the_World_Trade_Center_LCCN2002717279_LC-A05-B20.tif |
| `loc_item210` | cc03 | 2001 | PD（撮影者が権利を放棄）（C'） | 撮影者不詳（米議会図書館蔵・撮影者が権利と名前の表示を放棄） | https://commons.wikimedia.org/wiki/File:LOC_unattributed_Ground_Zero_photos,_September_11,_2001_-_item_210.jpg |
| `logan_1973` | c203 | 1973 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米環境保護庁 DOCUMERICA（NARA 548428） | https://commons.wikimedia.org/wiki/File:LOGAN_AIRPORT-CONTROL_TOWER_AND_RUNWAYS_SEEN_FROM_16TH_FLOOR_OBSERVATION_DECK_-_NARA_-_548428.jpg |
| `logan_apron_1969` | c216 | 1969 | 米議会図書館蔵／知られた制限なし（D） | Balthazar Korab | https://commons.wikimedia.org/wiki/File:Eastern_Air_Lines_terminal_at_Logan_Airport,_1969.jpg |
| `manhattan_2001_07` | c201 | 2001 | PD（自主宣言）（C＋D） | Carol M. Highsmith | https://commons.wikimedia.org/wiki/File:World_Trade_Center_towers,_New_York,_LCCN2015645969.jpg |
| `n334aa_2001_04` | c204 | 2001 | CC BY-SA 3.0（F） | Ken Fielding | https://commons.wikimedia.org/wiki/File:N334AA_B767-223ER_American_MAN_08APR01_(6839074488).jpg |
| `n591ua_1999` | c207 | 1999 | CC BY 2.0（F） | simon butler | https://commons.wikimedia.org/wiki/File:N591UA_United_Airlines_B757-222_at_John_Wayne_Airport,_1999.jpg |
| `nasa_iss003_e_5388` | c103 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | NASA | https://commons.wikimedia.org/wiki/File:Manhattan_smoke_plume_on_September_11,_2001_from_International_Space_Station_(ISS003-E-5388).jpg |
| `pen_010911_m_ci426_007` | cc02 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海兵隊（Cpl J. Ingersoll） | https://commons.wikimedia.org/wiki/File:View_of_the_Pentagon_from_the_Navy_Annex_minutes_after_a_hijacked_jetliner_crashed_into_building_at_approximately_0930_on_September_11,_2001_010911-M-CI426-007.jpg |
| `pen_010911_m_ci426_009` | c620 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海兵隊（Cpl J. Ingersoll） | https://commons.wikimedia.org/wiki/File:View_of_the_Pentagon_from_the_Navy_Annex_minutes_after_a_hijacked_jetliner_crashed_into_building_at_approximately_0930_on_September_11,_2001_010911-M-CI426-009.jpg |
| `pen_010911_m_ci426_012` | cc05 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海兵隊（Cpl J. Ingersoll） | https://commons.wikimedia.org/wiki/File:The_Pentagon_in_flames_moments_after_a_hijacked_jetliner_crashed_into_building_at_approximately_0930_on_September_11,_2001_010911-M-CI426-012.jpg |
| `pen_010911_m_ci426_021` | c623 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海兵隊（Cpl J. Ingersoll） | https://commons.wikimedia.org/wiki/File:The_Pentagon_in_flames_moments_after_a_hijacked_jetliner_crashed_into_building_at_approximately_0930_on_September_11,_2001_010911-M-CI426-021.jpg |
| `pen_010911_n_1993r_015` | c705 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海軍 | https://commons.wikimedia.org/wiki/File:Smoke_rising_over_the_Pentagon_on_Sep._11.jpg |
| `pen_010911_n_pu293_077` | ca09 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米海軍 | https://commons.wikimedia.org/wiki/File:A_nighttime_view_of_the_Pentagon_Building_showing_smoke_rising_from_the_building_after_the_September_11,_2001_attacks_010911-N-PU293-077.jpg |
| `pentagon_1998` | c601 | 1998 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米国防総省（MSgt Ken Hammond, USAF） | https://commons.wikimedia.org/wiki/File:The_Pentagon_US_Department_of_Defense_building.jpg |
| `pentagon_aerial_2023` | cb17 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米国防総省 | https://commons.wikimedia.org/wiki/File:An_aerial_view_of_the_Pentagon,_Washington,_D.C.,_May_15,_2023_230515-D-PM193-1762C.jpg |
| `shanksville_2015a` | c827 | 2015 | CC BY 3.0（F） | Ron Shawley | https://commons.wikimedia.org/wiki/File:Flight_93_Memorial_-_panoramio_(1).jpg |
| `shanksville_2015b` | c829 | 2015 | CC BY 3.0（F） | Ron Shawley | https://commons.wikimedia.org/wiki/File:Flight_93_Memorial_-_panoramio_(20).jpg |
| `cockpit_door_2015` | cb08 | 2015 | CC BY 2.0 de（F）・イメージ | Mattes | https://commons.wikimedia.org/wiki/File:Puerto_Rico_—_A_320_JetBlue_—_Open_cockpit_door_during_boarding.jpg |
| `n352aa_2012` | c209 | 2012 | CC BY 2.0（F）・イメージ | Valentin Hintikka | https://commons.wikimedia.org/wiki/File:N352AA_(15113637598).jpg |
| `security_1970` | c210 | 1970 | CC BY 2.0（F）・イメージ | Orange County Archives | https://commons.wikimedia.org/wiki/File:Orange_County_Airport,_security_officer,_Sept._1970.jpg |
| `tsa_checkpoint_2020` | cb06 | 2020 | CC BY 2.0（F）・イメージ | Tony Webster | https://commons.wikimedia.org/wiki/File:TSA_Security_Checkpoint_at_Airport.jpg |
| `wh_af1_phone` | c712 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | Eric Draper（Courtesy George W. Bush Presidential Library） | https://commons.wikimedia.org/wiki/File:President_George_W._Bush_Talks_on_the_Telephone_aboard_Air_Force_One.jpg |
| `wh_af1_window` | c914 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | Eric Draper（Courtesy George W. Bush Presidential Library） | https://commons.wikimedia.org/wiki/File:President_George_W._Bush_aboard_Air_Force_One.jpg |
| `wh_booker_tv` | c518 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | Eric Draper（Courtesy George W. Bush Presidential Library） | https://commons.wikimedia.org/wiki/File:President_George_W._Bush_watches_Television_Coverage_of_Terrorist_Attacks.jpg |
| `wh_nsc_night` | c913 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | Eric Draper（Courtesy George W. Bush Presidential Library） | https://commons.wikimedia.org/wiki/File:After_addressing_the_nation,_President_George_W._Bush_meets_with_his_National_Security_Council.jpg |
| `wh_offutt_vtc` | c920 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | Eric Draper（Courtesy George W. Bush Presidential Library） | https://commons.wikimedia.org/wiki/File:President_George_W._Bush_Teleconference_at_Offutt_Air_Force_Base.jpg |
| `wh_peoc_lynne` | c906 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | Courtesy George W. Bush Presidential Library（NARA） | https://commons.wikimedia.org/wiki/File:Vice_President_Cheney_with_Lynne_Cheney_in_the_President's_Emergency_Operations_Center_(PEOC)_-_DPLA_-_9c6475003a2ce1cd0dc7a2cc60b7275b.jpg |
| `wh_peoc_lynne_rice` | c905 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | Courtesy George W. Bush Presidential Library（NARA） | https://commons.wikimedia.org/wiki/File:Vice_President_Cheney_with_Lynne_Cheney_and_Condoleezza_Rice_in_the_President's_Emergency_Operations_Center_(PEOC)_-_DPLA_-_4fe01881026e81b415376664eee65939.jpg |
| `wh_peoc_rice` | c904 | 2001 | PD（米連邦の職務・17 U.S.C. §105）（A） | Courtesy George W. Bush Presidential Library（NARA） | https://commons.wikimedia.org/wiki/File:Vice_President_Cheney_with_National_Security_Advisor_Condoleezza_Rice_in_the_President's_Emergency_Operations_Center_(PEOC)_-_DPLA_-_d03f9c358c94caa6814e92d038b734f2.jpg |
| `wtc_1971` | c515 | 1971 | 米議会図書館蔵／知られた制限なし（D） | Thomas J. O'Halloran | https://commons.wikimedia.org/wiki/File:View_of_the_New_World_Trade_Center,_1971.jpg |
| `wtc_base_1976` | c422 | 1976 | 米議会図書館蔵／知られた制限なし（D） | Balthazar Korab | https://commons.wikimedia.org/wiki/File:World_Trade_Center_Exterior_Entrance_arches_with_Sphere_at_Plaza_Fountain_sculpture_-_LCCN2021638448.jpg |
| `wtc_far_1976` | c421 | 1976 | 米議会図書館蔵／知られた制限なし（D） | Balthazar Korab | https://commons.wikimedia.org/wiki/File:World_Trade_Center,_New_York._Exterior._Twilight_view_from_harbor_-_LCCN2021636615.jpg |
| `wtc_night_1976` | ca11 | 1976 | 米議会図書館蔵／知られた制限なし（D） | Balthazar Korab | https://commons.wikimedia.org/wiki/File:World_Trade_Center,_New_York._Exterior._Night_view_-_LCCN2021636612.jpg |
| `wtc_south_1976` | c501 | 1976 | 米議会図書館蔵／知られた制限なし（D） | Balthazar Korab | https://commons.wikimedia.org/wiki/File:World_Trade_Center,_New_York._Exterior._View_from_plaza_-_LCCN2020714989.jpg |
| `pg2003` | c401 | 2002 | PD（米連邦の職務） | NTSB | ntsb_flight_path_study_AA11.pdf PDF 3頁（200dpi・灰色・270度回して正立） |
| `pg3003` | c506 | 2002 | PD（米連邦の職務） | NTSB | ntsb_flight_path_study_UA175.pdf PDF 3頁（200dpi・灰色・270度回して正立） |
| `pg34` | ca18 | 2004 | PD（米連邦の職務） | 9.11委員会（米連邦の調査委員会） | GPO-911REPORT.pdf PDF 52頁（200dpi・灰色・0度回して正立） |
| `pg4003` | c602 | 2002 | PD（米連邦の職務） | NTSB | ntsb_flight_path_study_AA77.pdf PDF 3頁（200dpi・灰色・270度回して正立） |
| `pg4004` | c618 | 2002 | PD（米連邦の職務） | NTSB | ntsb_flight_path_study_AA77.pdf PDF 4頁（200dpi・灰色・270度回して正立） |
| `pg4005` | c617 | 2002 | PD（米連邦の職務） | NTSB | ntsb_flight_path_study_AA77.pdf PDF 5頁（200dpi・灰色・270度回して正立） |
| `pg5003` | c802 c809 | 2002 | PD（米連邦の職務） | NTSB | ntsb_flight_path_study_UA93.pdf PDF 3頁（200dpi・灰色・270度回して正立） |
| `pg5004` | c806 | 2002 | PD（米連邦の職務） | NTSB | ntsb_flight_path_study_UA93.pdf PDF 4頁（200dpi・灰色・270度回して正立） |
| `pgr11` | c408 | 2001 | PD（米連邦の職務） | 米連邦航空局（FAA） | `out/ep7_shotscan/3-AWA-716-WTC1__s01.png`（38.0秒のコマ・上下の黒い帯 y 0〜48・430〜を切った） |
| `pgr4` | ca02 | 2001 | PD（米連邦の職務） | 米連邦航空局（FAA） | `out/ep7_shotscan/5-AWA-716-All-4-AC__s01.png`（37.5秒のコマ・上下の黒い帯 y 0〜48・430〜を切った） |

### 2. 頁（米連邦の資料＝PD・`qa_out/ep21_assets.py pages`・切り口は `ref/ep21/pages.json`）
- NTSB の飛行経路の調べ（2002年・スキャン）＝PDF の頁を 200dpi の灰色に焼いて正立（横倒しの図）・図の範囲で切る。
- RG237＝米連邦航空局のレーダーの再生の動画（NARA）の1コマ＝7本目の見本帳の静止画（`out/ep7_shotscan/`・表示の幅に直したもの）の上下の黒い帯を切る。
- 委員会報告の文字の頁（GPO の PDF・本物の字）＝PDF の頁を 200dpi の灰色に焼いて、語りの段を含む行で切る（頁の上の印は文字の層の句の位置）。

| 頁 | 使うカット | 中身 | 元 |
|---|---|---|---|
| `pg2003.png` | c401 | 11便のレーダーの航跡（Figure 1・点 A〜I と時刻） | ntsb_flight_path_study_AA11.pdf PDF 3頁（200dpi・灰色・270度回して正立） |
| `pg3003.png` | c506 | 175便のレーダーの航跡（Figure 1・点 A〜G） | ntsb_flight_path_study_UA175.pdf PDF 3頁（200dpi・灰色・270度回して正立） |
| `pg34.png` | ca18 | 委員会報告 p34（2003年5月の証言の誤りを書いた段） | GPO-911REPORT.pdf PDF 52頁（200dpi・灰色・0度回して正立） |
| `pg4003.png` | c602 | 77便の飛行経路（Figure 1・点 A〜F） | ntsb_flight_path_study_AA77.pdf PDF 3頁（200dpi・灰色・270度回して正立） |
| `pg4004.png` | c618 | 77便の高度（Figure 2・飛行の記録装置の気圧高度） | ntsb_flight_path_study_AA77.pdf PDF 4頁（200dpi・灰色・270度回して正立） |
| `pg4005.png` | c617 | ワシントンの辺りの経路（Figure 3・地形の地図の上） | ntsb_flight_path_study_AA77.pdf PDF 5頁（200dpi・灰色・270度回して正立） |
| `pg5003.png` | c802 c809 | 93便のレーダーの航跡（Figure 1・点 A〜I と時刻） | ntsb_flight_path_study_UA93.pdf PDF 3頁（200dpi・灰色・270度回して正立） |
| `pg5004.png` | c806 | 93便の高度（Figure 2・点 A〜I） | ntsb_flight_path_study_UA93.pdf PDF 4頁（200dpi・灰色・270度回して正立） |
| `pgr11.png` | c408 | 11便の航跡の再生（FAA・3-AWA-716-WTC1 の 38.0秒） | `out/ep7_shotscan/3-AWA-716-WTC1__s01.png`（38.0秒のコマ・上下の黒い帯 y 0〜48・430〜を切った） |
| `pgr4.png` | ca02 | 4機の航跡の再生（FAA・5-AWA-716-All-4-AC の 37.5秒） | `out/ep7_shotscan/5-AWA-716-All-4-AC__s01.png`（37.5秒のコマ・上下の黒い帯 y 0〜48・430〜を切った） |

## タイタン号のリメイク（2023-06-18・22本目）

※2026-10-14（⑤b-2）。`qa_out/ep22_assets.py credits --write` が書く（手で直さない）。旧版の節は上の「タイタン号（本番1本目）」＝直さない（旧版は 10-13 に非公開を確かめた・ROV の映像を PD と書いていた誤りは旧版の節に残る）。
名前が要る3点（C218＝CC BY-SA の撮影者・N08／N10＝NTSB の報告書の図の写真の出どころの個人）は画面の出典の行に名前を出す（✅ 2026-10-14 カズヤくん「リポに書く」＝名前を出すこと自体が使う条件・同じ3人の名前は旧版の節にもある）。

### 0. 動く映像（9本・音はすべて使わない＝`-an`）
- 🔴 **ROV の映像2本（R04＝尾部・R07＝前と後ろのドーム）は第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22）**＝米沿岸警備隊と米運輸安全委員会が NTSB のドケットで公開した物の引用。**額装・等速（rate 1.0）・寄り 1.0・無加工・地は無地（`plain=True`）・焼き込み（深さ・日付）は残す・サムネに使わない**（了承② 決め3）。旧版はパブリックドメインと誤って書いていた
- DVIDS 888022／887734／887597／887852／888248＝米沿岸警備隊の職員の職務＝PD。888012／888011＝米空軍州兵 第106救難航空団の職務（連邦の任務の扱いが弱い所＝DVIDS の表示に従う）。記者会見は使う区間＋前後10秒だけを手元に置き（`ref/ep22/src/film/<記号>/clips/`・git の外）、焼くときは媒体の URL から区間だけ読む（`range`）
- 使わない窓（`tools/footage.py` の NOGO）：887734 の机の上の顔写真入りの身分証（その秒を含むショットまるごと）

| 記号 | 使うカット | 画面の出典 | 権利 | 出どころ |
|---|---|---|---|---|
| `R04` | c101 c108 c517 cd01 | 出典：Pelagic Research Services の ROV 映像（米沿岸警備隊・米運輸安全委員会が公開） | 第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開） | https://data.ntsb.gov/Docket/?NTSBNumber=DCA23FM036 |
| `R07` | c104 c105 c522 c523 c601 c602 c609 cd08 | 出典：Pelagic Research Services の ROV 映像（米沿岸警備隊・米運輸安全委員会が公開） | 第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開） | https://data.ntsb.gov/Docket/?NTSBNumber=DCA23FM036 |
| `U022` | c102 c106 c109 c519 | 出典：米沿岸警備隊（DVIDS 888022・パブリックドメイン） | A（米沿岸警備隊の職員の職務・DVIDS） | https://www.dvidshub.net/video/888022 |
| `U734` | c107 c508 | 出典：米沿岸警備隊（DVIDS 887734・パブリックドメイン） | A（米沿岸警備隊の職員の職務・DVIDS） | https://www.dvidshub.net/video/887734 |
| `U597` | c513 | 出典：米沿岸警備隊（DVIDS 887597・パブリックドメイン） | A（米沿岸警備隊の職員の職務・DVIDS） | https://www.dvidshub.net/video/887597 |
| `U852` | c512 | 出典：米沿岸警備隊（DVIDS 887852・パブリックドメイン） | A（米沿岸警備隊の職員の職務・DVIDS） | https://www.dvidshub.net/video/887852 |
| `U248` | cc12 | 出典：米沿岸警備隊（DVIDS 888248・パブリックドメイン） | A（米沿岸警備隊の職員の職務・DVIDS） | https://www.dvidshub.net/video/888248 |
| `U012` | c103 | 出典：米空軍州兵 第106救難航空団（DVIDS 888012・パブリックドメイン） | A（米空軍州兵＝第106救難航空団の職務・連邦の任務の扱いが弱い所） | https://www.dvidshub.net/video/888012 |
| `U011` | c516 | 出典：米空軍州兵 第106救難航空団（DVIDS 888011・パブリックドメイン） | A（米空軍州兵＝第106救難航空団の職務・連邦の任務の扱いが弱い所） | https://www.dvidshub.net/video/888011 |

### 1. 写真と報告書の図（米連邦の職務〈A〉・第三者〈引用〉・CC BY-SA・共同）
- 束＝`ref/ep22/photo/`（git の外）の長辺を幅 2400／高さ 1350 まで縮めただけ（色・切り口はそのまま）。報告書の図（PDF の埋め込みの PNG）は JPEG に直しただけ。🔴 EXIF の向きの札は絵に当てた（D367＝1つ目の船体は縦長）・色の札が Display P3 の2点（D342・D367）は sRGB に写した（見た目の色はそのまま）。組み写真の片側だけを使う NTSB 図16・17・18 は白いすき間で割った（`_l`・`_r`・`_t`・`_b`＝割り目は機械で探した）
- 🔴 **額装だけ（了承② 決め3）**＝第三者（NTSB 図8・図10＝個人の撮影）・共同（タイタニックの船首＝NOAA と連邦の外の機関）・CC BY-SA 4.0（ホライゾン・アークティック）＝無加工・色そのまま・上に重ねない・寄り0・1点1カット（`cuts/ss.check_frame_only`）・サムネに使わない
- 報告書の図の撮った機関＝米沿岸警備隊の海難調査委員会（MBI）・FBI（図157・159・270）・米運輸安全委員会の研究所（図255・NTSB の図13〜18・24-011）
- 研究所の報告 24-011 の頁まるごとの画像（図15・21・48）は紙面の引用＝図と説明の行まで切るのは ⑤b-4
- 撮影年＝報告書の図の説明・EXIF・Commons の頁（`qa_out/ep22_assets.py` の YEAR＝出どころつき）。分からない点は「不明」＝副題に年を書かない

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `commons_horizon_arctic_2022_02` | c218 | 2022 | CC BY-SA 4.0（BY-SA） | Gordon Leggett（Commons の頁の作者（Own work・CC BY-SA 4.0・fetch22.py が API で取った値）） | https://commons.wikimedia.org/wiki/File:2022-08-21_02_HORIZON_ARCTIC_-_IMO_9732838.jpg |
| `commons_titanic_wreck_bow` | c201 | 2004 | PD（Commons の表示）・共同＝額装（共同） | NOAA/Institute for Exploration/University of Rhode Island（2004年） | https://commons.wikimedia.org/wiki/File:Titanic_wreck_bow.jpg |
| `commons_uscg_mbi_8668382` | cc01 | 2024 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊（DVIDS 8668382） | https://commons.wikimedia.org/wiki/File:U_S_Coast_Guard_Marine_Board_of_Investigation_(8668382).jpg |
| `dvids7875444_hc130_cockpit` | c510 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊（DVIDS 7875444） | https://www.dvidshub.net/image/7875444 |
| `dvids7875448_sea_from_aircraft` | c511 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊（DVIDS 7875448） | https://www.dvidshub.net/image/7875448 |
| `dvids7875471_hc130_hangar` | c509 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊（DVIDS 7875471） | https://www.dvidshub.net/image/7875471 |
| `dvids9057342_deck_survey` | c603 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊（DVIDS 9057342） | https://www.dvidshub.net/image/9057342 |
| `dvids9057367_first_hull` | c814 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊（DVIDS 9057367） | https://www.dvidshub.net/image/9057367 |
| `lab24011_p37_fig15` | c612 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会 研究所の報告 24-011 図15 | pdf:ref/ep22/src/materials_raw/ntsb_docket_pdf/lab24011.pdf:37:0 |
| `lab24011_p44_fig21` | c614 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会 研究所の報告 24-011 図21 | pdf:ref/ep22/src/materials_raw/ntsb_docket_pdf/lab24011.pdf:44:0 |
| `lab24011_p46_fig22a` | c613 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会 研究所の報告 24-011 図22 | pdf:ref/ep22/src/materials_raw/ntsb_docket_pdf/lab24011.pdf:46:0 |
| `lab24011_p53_fig28` | c916 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会 研究所の報告 24-011 図28 | pdf:ref/ep22/src/materials_raw/ntsb_docket_pdf/lab24011.pdf:53:0 |
| `lab24011_p67_fig39` | c819 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会 研究所の報告 24-011 図39 | pdf:ref/ep22/src/materials_raw/ntsb_docket_pdf/lab24011.pdf:67:0 |
| `lab24011_p71_fig43b` | cd07 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会 研究所の報告 24-011 図43 | pdf:ref/ep22/src/materials_raw/ntsb_docket_pdf/lab24011.pdf:71:1 |
| `lab24011_p73_fig45a` | cc04 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会 研究所の報告 24-011 図45 | pdf:ref/ep22/src/materials_raw/ntsb_docket_pdf/lab24011.pdf:73:0 |
| `lab24011_p75_fig47b` | c605 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会 研究所の報告 24-011 図47 | pdf:ref/ep22/src/materials_raw/ntsb_docket_pdf/lab24011.pdf:75:1 |
| `lab24011_p76_fig48` | c616 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会 研究所の報告 24-011 図48 | pdf:ref/ep22/src/materials_raw/ntsb_docket_pdf/lab24011.pdf:76:0 |
| `mbi_fig003_polar_prince` | c301 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図3 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:14:0 |
| `mbi_fig005_lars` | c305 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図5 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:16:0 |
| `mbi_fig018_log_0000` | c307 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図18 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:23:2 |
| `mbi_fig021_hangar` | c308 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図21 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:25:0 |
| `mbi_fig024_small_boats` | c309 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図24 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:27:0 |
| `mbi_fig031_bridge_office` | c405 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図31 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:32:0 |
| `mbi_fig037_log_0600` | c417 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図37 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:38:1 |
| `mbi_fig065_cyclops_controller` | c217 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図65 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:103:0 |
| `mbi_fig109_lars_dock` | cb07 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図109 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:142:0 |
| `mbi_fig112_ballast_valve` | cb12 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図112 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:144:0 |
| `mbi_fig115_air_regulator` | cb15 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図115 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:145:1 |
| `mbi_fig157_aft_segment` | c607 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図157（FBI） | pdf:ref/ep22/src/uscg_titan_mbi.pdf:188:0 |
| `mbi_fig159_fwd_segment` | c606 | 2023 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図159（FBI） | pdf:ref/ep22/src/uscg_titan_mbi.pdf:189:0 |
| `mbi_fig255_layers` | c906 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図255（米運輸安全委員会） | pdf:ref/ep22/src/uscg_titan_mbi.pdf:276:0 |
| `mbi_fig268_adhesive` | c608 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図268 | pdf:ref/ep22/src/uscg_titan_mbi.pdf:292:0 |
| `mbi_fig270_viewport_ring` | c604 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米沿岸警備隊 海難調査委員会の報告書 図270（FBI） | pdf:ref/ep22/src/uscg_titan_mbi.pdf:294:0 |
| `ntsb_fig08_launch_2022` | ca03 | 2022 | 引用（第三者の撮影・報告書の図）（第三者） | Garry Comber（NTSB MIR-25-36 図8 の説明「(Source: Garry Comber)」（`src/ntsb_mir2536_pages.txt`）） | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:34:0 |
| `ntsb_fig10_lars_tipped` | cb11 | 2023 | 引用（第三者の撮影・報告書の図）（第三者） | Steven Taragel（NTSB MIR-25-36 図10 の説明「(Source: Steven Taragel)」（同）） | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:38:1+0 |
| `ntsb_fig13_recovered_piece` | c611 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図13 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:41:0 |
| `ntsb_fig14_faces` | c618 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図14 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:42:0 |
| `ntsb_fig15_end_piece` | c911 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図15 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:42:1 |
| `ntsb_fig16_wrinkle_b` | c909 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図16 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:43:0 |
| `ntsb_fig16_wrinkle_t` | c914 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図16 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:43:0 |
| `ntsb_fig17_layers_b` | c913 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図17 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:44:0 |
| `ntsb_fig18_delam_l` | c803 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図18 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:45:0 |
| `ntsb_fig18_delam_r` | c904 | 不明 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図18 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:45:0 |
| `ntsb_fig21_strain_l` | ca17 | 2022 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図21 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:53:0 |
| `ntsb_fig21_strain_r` | ca18 | 2022 | PD（米連邦の職務・17 U.S.C. §105）（A） | 米運輸安全委員会の報告書 図21 | pdf:ref/ep22/src/ntsb_titan_MIR2536.pdf:53:0 |

### 2. 地図の衛星写真（Google マップ・束に入れない）
- G01〜G06＝Google マップの衛星写真（⑤b-1 に撮った・G06 は ⑤b-3 で撮り直し・`ref/ep22/photo/gmap_g0*.png`＝git の外）。Google の地理の指針（教育の動画は許可不要・収益化も可）に従い、**絵の下の帰属の行（地図データ ©2026 Google・画像 ©提供元）とロゴを映す間ずっと残す**・色を変えない・動かさない・点と線と札は描き足してよい（地図の型 `tools/satmap.py`・門番 `tools/check_sat.py`）
- 🔴 公開のリポに画像を置かない＝Modal の保管庫 `jiko-assets` の `ref/ep22/photo/`（`modal_app.pull_private`）・地図のカットの検品画像は Modal の qa（Actions は理由を出して飛ばす）。画面の出典の行＝「地図：Google マップの衛星写真（帰属は地図の右下）」（額の下）

| 記号 | 使うカット | 中心（緯度, 経度）・ズーム | md5 |
|---|---|---|---|
| `G01` | c204 | 45.0, -87.0・4 | `70ff2619fdbaf91c3b1c5651b82d7c8e` |
| `G02` | c219 c304 cb09 | 44.6, -51.3・6 | `4c9a76312ec1bb0053611ec20add3068` |
| `G03` | c514 | 45.5, -65.8・5 | `57eb70a4722acc83aa5653315a0171ec` |
| `G04` | c515 | 45.0, -47.0・5 | `67507f0134ae97af6abac1dcafc49299` |
| `G05` | c812 c813 | 25.0, -77.0・7 | `35b8c66417c27d9d68155c244a7d0337` |
| `G06` | cb01 | 47.5675, -52.701・17 | `2ac970d434b7b1a7c735a8f334926ab7` |

## 三豊百貨店崩壊事故のリメイク（1995-06-29・23本目）

※2026-10-18（⑤b-2）。`qa_out/ep23_assets.py credits --write` が書く（手で直さない）。旧版の節は上の「三豊百貨店崩壊事故（1995-06-29・10本目）」＝直さない。
写真は映像方針の一覧 `ref/ep23/eizou_list23.md`（了承② 2026-10-18）。この事故の動く映像は使わない（写真の動きだけ）。

### 0. フリー素材の映像（イメージ・この事故の物でない・音はすべて使わない＝`-an`）
- Pexels・Pixabay（生成AI は使わない＝Pexels は規約で投稿を認めない）。画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」「イメージ（Pixabay）」だけ（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。20% に数えない
- 🔴 映像そのものも、ひかえの静止画も git に入れない（19本目 決め⑨）。焼くときに台帳 `ref/ep23/clips.json` の `media` から取る

| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |
|---|---|---|---|---|
| `Xc205a` | c205 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/35217402/ |
| `Xc211a` | c211 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/35988850/ |
| `Xc219a` | c219 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/36443290/ |
| `Xc617b` | c308 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/6281080/ |
| `Xc613b` | c613 | イメージ（Pixabay） | Pixabay Content License | https://pixabay.com/videos/id-40298/ |
| `Xc613a` | c704 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/14059234/ |
| `Xc712a` | c712 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/39924242/ |
| `P29880216` | c817 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/water-cascading-over-weathered-concrete-edge-29880216/ |
| `Xc903b` | c903 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/8094275/ |
| `Xc905b` | c905 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/7830320/ |
| `Xc909b` | c909 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/7793216/ |
| `P5571839` | ca04 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/water-dripping-on-welded-metal-pipes-5571839/ |
| `Xca07a` | ca07 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/20755878/ |
| `P7830155` | ca12 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/a-crack-on-the-wall-7830155/ |
| `Xcb09b` | cb09 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/5647337/ |
| `Xcb12a` | cb12 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/6109240/ |
| `Xc704b` | cc04 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/5972195/ |

### 1. 写真（ソウル研究院・ソウル歴史編纂院・Commons〈ソウル特別市 消防災難本部・個人名義〉・イメージ）
- 束＝元の画像（git の外）の長辺を幅 2400／高さ 1350 まで縮めただけ（色・切り口はそのまま）。歴史編纂院の8点は CMYK＝色の札で sRGB に写した（技術の変換）
- ソウル研究院（서울연구데이터서비스）＝公共ヌリ第1類型＋CC BY 4.0（頁の「이용목적」で 상업적 활용 を選んで 1600px を取った）。全面と額の中の寄りで端を切る＝画面の出典に「改変：切出」
- ソウル歴史編纂院＝公共ヌリ第1類型（頁の「자료 이용 조건 동의서」で商業の出版・出典を書くことに同意）。幅1000未満＝額装（額の中で寄る）
- 🔴 **CC BY-SA 4.0（ソウル特別市 消防災難本部・個人名義）は額装だけ**（了承② 決め3＝高さいっぱいの額装・寄り0・色は原本・上に重ねない・額ごと動かす・1点1カット＝`cuts/ss.check_frame_only`・サムネに使わない）
- 🔴 **個人名義の10点は画面の出典の行に作者欄の名前**（了承② 決め4＝クレジット A）。名前はこのリポに書かない（10-17「名前0」）＝`ref/ep23/credits.json` は印 `{作者}` だけ・焼くときに git の外の表から足す（`tools/scene_jiko.ep23_credit`）。名前は各行の Commons の頁の作者欄
- 顔だけモザイク（了承② 決め2）＝研究院 52400（右を歩く男性）・歴史編纂院 077（写真展を見る男性と子ども）＝元の画像を直した（`cuts/ss.NEEDS_MASK`・`ref/ep23/masked.json`）。歴史編纂院 104（行方を探す掲示板）は10本目に顔と名前を隠した版
- イメージ（Pexels の写真8点）＝`ep23/stock/` の名・画面の左上に「イメージ」・20% に数えない・git に入れない（焼くときに取り直して md5 を照らす）
- 撮影年＝本部の写真は Commons の題（「19950629…」）・研究院と歴史編纂院は頁の注・個人名義は Commons に撮影日の記載なし＝写っている崩壊直後の救助から1995年（`qa_out/ep23_assets.py` の year_of＝出どころつき）

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `c100_960` | c616 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A024.jpg |
| `c102_960` | c506 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A026.jpg |
| `c10_960` | c718 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0109.jpg |
| `c120_960` | c108 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A042.jpg |
| `c129_960` | c412 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A051.jpg |
| `c130_960` | c911 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A052.jpg |
| `c133_960` | c522 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A055.jpg |
| `c138_960` | c302 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A060.jpg |
| `c13_960` | c507 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0111.jpg |
| `c143_960` | c505 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A065.jpg |
| `c144_960` | c515 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A066.jpg |
| `c147_960` | c605 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A069.jpg |
| `c148_960` | c501 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A070.jpg |
| `c150_960` | ca01 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A072.jpg |
| `c151_960` | c417 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A073.jpg |
| `c157_960` | ca14 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A079.jpg |
| `c159_960` | c203 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A081.jpg |
| `c160_960` | c305 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A082.jpg |
| `c165_960` | c901 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A087.jpg |
| `c170_960` | c523 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A091.jpg |
| `c172_960` | c716 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A093.jpg |
| `c175_960` | c309 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A096.jpg |
| `c176_960` | c105 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A097.jpg |
| `c182_3840` | c414 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:1995%EB%85%84_6%EC%9B%94_29%EC%9D%BC_%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0_7.jpg |
| `c193` | c801 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept07.jpg |
| `c1_960` | c503 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A01.jpg |
| `c203` | c510 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept17.jpg |
| `c207` | c406 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept21.jpg |
| `c209` | cb10 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept23.jpg |
| `c211_1280` | cb14 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept25.jpg |
| `c212` | c410 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept26.jpg |
| `c215` | c107 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept29.jpg |
| `c216` | c508 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept31.jpg |
| `c219` | ca10 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept34.jpg |
| `c224` | ca19 | 1995 | CC BY-SA 4.0（BY-SA） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep23/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sampungdept40.jpg |
| `c29_960` | c914 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0127.jpg |
| `c2_960` | c408 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0100.jpg |
| `c2k001_3840` | c102 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:2000%EB%85%84%EB%8C%80_%EC%B4%88%EB%B0%98_%EC%84%9C%EC%9A%B8%EC%86%8C%EB%B0%A9_%EC%86%8C%EB%B0%A9%EA%B3%B5%EB%AC%B4%EC%9B%90%28%EC%86%8C%EB%B0%A9%EA%B4%80%29_%ED%99%9C%EB%8F%99_%EC%82%AC%EC%A7%84_%EC%82%BC%ED%92%8D001.jpg |
| `c31_960` | c509 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0129.jpg |
| `c36_960` | c109 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0133.jpg |
| `c37_960` | c814 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0134.jpg |
| `c39_960` | c214 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0136.jpg |
| `c3_960` | c419 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0101.jpg |
| `c40_960` | c705 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0137.jpg |
| `c41_960` | c610 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0138.jpg |
| `c43_960` | c512 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A014.jpg |
| `c47_960` | c514 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0143.jpg |
| `c48_960` | c106 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0144.jpg |
| `c49_960` | c615 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0145.jpg |
| `c55_960` | c612 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0150.jpg |
| `c5_960` | ca06 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0104.jpg |
| `c65_960` | c516 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A016.jpg |
| `c70_960` | c318 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0165.jpg |
| `c71_960` | c619 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0166.jpg |
| `c73_960` | c517 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0168.jpg |
| `c74_960` | c401 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0169.jpg |
| `c77_960` | c409 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0171.jpg |
| `c78_960` | c907 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0172.jpg |
| `c7_960` | c702 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0106.jpg |
| `c80_960` | c707 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0174.jpg |
| `c83_960` | c714 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0177.jpg |
| `c84_960` | c411 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0178.jpg |
| `c86_960` | c709 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A018.jpg |
| `c8_960` | c405 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0107.jpg |
| `c90_960` | c711 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0183.jpg |
| `c93_960` | c808 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A0186.jpg |
| `c95_960` | c217 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A019.jpg |
| `c99_960` | c521 | 1995 | CC BY-SA 4.0（BY-SA） | ソウル特別市 消防災難本部 | https://commons.wikimedia.org/wiki/File:19950629%EC%82%BC%ED%92%8D%EB%B0%B1%ED%99%94%EC%A0%90_%EB%B6%95%EA%B4%B4_%EC%82%AC%EA%B3%A023.jpg |
| `hs_2301030077_0` | cb06 | 1996 | 公共ヌリ第1類型（A・顔にモザイク） | ソウル歴史編纂院 | https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=2301030077&key=2211220005 |
| `hs_2301030083_0` | cb13 | 1996 | 公共ヌリ第1類型（A） | ソウル歴史編纂院 | https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=2301030083&key=2211220005 |
| `hs_2301030100_0` | cd06 | 1998 | 公共ヌリ第1類型（A・顔にモザイク） | ソウル歴史編纂院 | https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=2301030100&key=2211220005 |
| `hs_2301030102_0` | cb01 | 1995 | 公共ヌリ第1類型（A） | ソウル歴史編纂院 | https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=2301030102&key=2211220005 |
| `hs_2301030107_0` | c416 | 1995 | 公共ヌリ第1類型（A） | ソウル歴史編纂院 | https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=2301030107&key=2211220005 |
| `hs_2301030108_0` | c415 | 1995 | 公共ヌリ第1類型（A） | ソウル歴史編纂院 | https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=2301030108&key=2211220005 |
| `hs_2301030109_0` | c103 | 1995 | 公共ヌリ第1類型（A） | ソウル歴史編纂院 | https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=2301030109&key=2211220005 |
| `hs_2301030510_0` | c520 | 1995 | 公共ヌリ第1類型（A） | ソウル歴史編纂院 | https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=2301030510&key=2211220005 |
| `missing_board_01` | cb03 | 1995 | 公共ヌリ第1類型（A・顔と名前にモザイク（隠した版）） | ソウル歴史編纂院 | https://history.seoul.go.kr/archive/bbsctt/view.do?bbscttSn=2301030104&key=2211220005 |
| `sire_31733` | cd05 | 2000 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/31733 |
| `sire_31735` | cc22 | 2000 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/31735 |
| `sire_31737` | cb17 | 2000 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/31737 |
| `sire_31740` | cd01 | 2000 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/31740 |
| `sire_50279` | c603 | 1995 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/50279 |
| `sire_52394` | c601 | 1995 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/52394 |
| `sire_52395` | cc01 | 1995 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/52395 |
| `sire_52396` | cc02 | 1995 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/52396 |
| `sire_52397` | cc10 | 1995 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/52397 |
| `sire_52398` | c608 | 1995 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/52398 |
| `sire_52399` | c101 c201 | 1995 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/52399 |
| `sire_52400` | c104 cd08 | 1995 | 公共ヌリ第1類型＋CC BY 4.0（A・顔にモザイク） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/52400 |
| `sire_53849` | cc14 | 1996 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/53849 |
| `sire_53868` | cc06 | 1996 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/53868 |
| `sire_53880` | cc08 | 1996 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/53880 |
| `sire_60607` | cc17 | 2020 | 公共ヌリ第1類型＋CC BY 4.0（A） | ソウル研究院（서울연구데이터서비스） | https://data.si.re.kr/node/60607 |
| `c208a` | c208 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/17139756/ |
| `c216b` | c216 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/7616004/ |
| `c311a` | c311 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/36003982/ |
| `c313b` | c313 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/18137069/ |
| `c313c` | c617 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/27452439/ |
| `c314b` | c314 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/7168444/ |
| `c802a` | c802 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/8456426/ |
| `c805a` | c805 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/6034678/ |

## 中華航空140便墜落事故（1994-04-26・17本目）

※2026-10-20（⑤b-2）。`qa_out/ep17_assets.py credits --write` が書く（手で直さない）。写真と映像は映像方針の一覧 `ref/ep17/eizou_list17.md`（了承② 2026-10-19）。

### 0. 映像（記録映像 V1・フリー素材＝音はすべて使わない＝`-an`）
- 記録映像 V1＝防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0・防衛省の YouTube 公式・Commons にも同じ版）。4:3 の中身を横いっぱい・上を残して下を切る（焼き込みの字幕と日付を外す）・再生の速さを変えることがある＝画面の出典に「改変：切出・再生速度」
- フリー素材（Pexels・Pixabay・生成AI は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」「イメージ（Pixabay）」だけ（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）

| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |
|---|---|---|---|---|
| `V1` | c101 c805 c807 | 出典：防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0）・改変：切出・再生速度 | CC BY 3.0 | https://commons.wikimedia.org/wiki/File:%E5%B9%B3%E6%88%90%EF%BC%96%E5%B9%B4%E9%98%B2%E8%A1%9B%E5%BA%81%E8%A8%98%E9%8C%B2.webm |
| `Xc3` | c203 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/airplane-window-view-from-above-the-clouds-11292227/ |
| `Xd2` | c207 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/a-small-airplane-flying-over-a-cloudy-sky-17118515/ |
| `Xb3` | c215 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/footage-of-a-flying-airplane-at-night-6467678/ |
| `Xb4` | c323 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/airplane-departing-at-night-11878578/ |
| `Xm1` | c811 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/a-closed-gate-with-a-chain-and-a-padlock-3999371/ |
| `Xi2` | c814 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/a-fire-truck-spraying-water-on-a-runway-15448013/ |
| `Xk1` | ca13 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/close-up-of-hands-flipping-through-old-documents-30117908/ |
| `Xc1` | cb13 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/commercial-airplane-flying-high-in-cloudy-sky-38530430/ |

### 1. 写真・頁（報告書 96-5〈PDL1.0〉・Commons・イメージ）
- 報告書の写真と付図＝運輸省 航空事故調査委員会『航空事故調査報告書 96-5』（1996年・公共データ利用規約 PDL1.0＝出典と加工の旨）。頁の走査（灰色・約400dpi）から切り出し、白黒のまま縮めた＝画面の出典に「（加工して作成）」
- 🔴 **CC BY-SA・GFDL は額装だけ**（了承② 決め7＝無加工・額ごと動かす・1点1カット＝`cuts/ss.check_frame_only`）
- 🔴 **個人名義の点は画面の出典の行に作者欄の名前**。名前はこのリポに書かない＝`ref/ep17/credits.json` は印 `{作者}` だけ・焼くときに git の外の表から足す（`tools/scene_jiko.ep17_credit`）。名前は各行の Commons の頁の作者欄。CC0・PD は表示が任意＝名前を出さない
- 「関連」＝事故そのものではない実物（同じ型の操縦室・機関の建物・空港・消防車・中華航空のほかの機体）＝20% の数（この事故の写真）に入れない
- イメージ（Pexels の写真）＝`ep17/stock/` の名・画面の左上に「イメージ」・20% に数えない・git に入れない（焼くときに取り直して md5 を照らす）

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `a310` | c913 | 1982 | CC BY 2.0（関連） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:F-WZLI_(172)_11-9-82_Farnborough_(52797770066).jpg |
| `ab1` | c311 | 2024 | CC0（関連） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Toulouse_Si%C3%A8ge_Airbus.jpg |
| `ab2` | c614 | 2024 | CC0（関連） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Toulouse_Si%C3%A8ge_Airbus_%2B_b%C3%A9luga_01.jpg |
| `ab3` | ca15 | 2024 | CC0（関連） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Beluga_takes_off_above_Airbus%27_Headquarters.jpg |
| `arf` | c802 | 2014 | CC BY 3.0（関連・顔にモザイク） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:A-MB-2_JASDF_Airport_crash_tender_,_%E8%88%AA%E7%A9%BA%E8%87%AA%E8%A1%9B%E9%9A%8A_%E7%A0%B4%E5%A3%8A%E6%95%91%E9%9B%A3%E6%B6%88%E9%98%B2%E8%BB%8A_-_Panoramio_103521917.jpg |
| `arf2` | c808 | 2014 | CC BY-SA 3.0（関連） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:JASDF_A-MB-3_crash_tender(48-6320)_right_front_view_at_Komaki_Air_Base_February_23,_2014.jpg |
| `b192` | c418 cb05 | 1998 | CC BY 2.0（関連） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:HONG_KONG_KAI_TAK_FEB_1998_CHINA_AIRLINES_AIRBUS_A300_B-192_(8673301706).jpg |
| `b747` | c618 | 1996 | CC BY 2.0（関連） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:China_Airlines_Boeing_747-409_B-163_(23842205736).jpg |
| `ct1` | c506 cb18 | 2021 | CC0（関連） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Nagoya-High-Court-1.jpg |
| `e1` | c102 | 1993 | CC BY-SA 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Photo_of_China_Airlines_Airbus_A300B4-622R_B-1816_at_Nagoya-Komaki_International_Airport_(NGO,_RJNN).jpg |
| `e2` | c204 | 不明 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:CI_A300_B-1816.jpg |
| `e3` | c315 | 1991 | GFDL 1.2（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:China_Airlines_B-1816_Airbus_A300_at_HK_Airport.jpg |
| `f01` | c201 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `f03` | c213 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `f04` | c219 c713 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `f05` | c521 c701 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `f08` | c803 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `f09` | c816 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `f11` | c723 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `f12` | c806 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `f28` | c722 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `f29` | c106 c113 c309 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `faa` | cb11 | 2016 | パブリックドメイン（関連） | 米議会図書館 | https://commons.wikimedia.org/wiki/File:Orville_Wright_Federal_Building,_Washington,_D.C_LCCN2016648213.tif |
| `hel` | c905 | 1981 | CC BY 4.0（関連） | ヘルシンキ市立博物館 | https://commons.wikimedia.org/wiki/File:Helsinki-Vantaan_lentoasemaa_1981_(HK19940104-3144).tif |
| `j1` | cb14 | 2003 | 判決（著作権の目的とならない）（頁） | 名古屋地方裁判所（判決＝著作権の目的とならない・著作権法13条） | https://www.courts.go.jp/hanrei/7587/detail4/index.html |
| `j98` | cb22 | 2003 | 判決（著作権の目的とならない）（頁） | 名古屋地方裁判所（判決＝著作権の目的とならない・著作権法13条） | https://www.courts.go.jp/hanrei/7587/detail4/index.html |
| `jas` | ca18 | 1999 | CC BY 4.0（関連） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Japan_Air_System_Airbus_A300-600R_JA8562,_Xian,_Oct99_(52040271670).jpg |
| `k04` | ca20 | 2004 | CC0（この事故） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:ChinaAirlines_A300_fukuoka_20041023102346.jpg |
| `k05` | c902 | 2005 | CC0（この事故） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:ChinaAirlines_A300_fukuoka_20050925102120.jpg |
| `k05b` | cb06 | 2005 | CC0（この事故） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:ChinaAirlines_A300_fukuoka_20050429102946.jpg |
| `l03` | cb12 | 1996 | パブリックドメイン（米連邦政府）（頁） | アメリカ連邦航空局（FAA Human Factors Team・1996年6月） | https://www.faa.gov/sites/faa.gov/files/2022-11/interfac.pdf |
| `l64` | c406 | 1996 | パブリックドメイン（米連邦政府）（頁） | アメリカ連邦航空局（FAA Human Factors Team・1996年6月） | https://www.faa.gov/sites/faa.gov/files/2022-11/interfac.pdf |
| `l80` | c922 | 1996 | パブリックドメイン（米連邦政府）（頁） | アメリカ連邦航空局（FAA Human Factors Team・1996年6月） | https://www.faa.gov/sites/faa.gov/files/2022-11/interfac.pdf |
| `n1810` | cb30 | 不明 | CC BY-SA 2.0（関連） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:China_Airlines_Airbus_A300B4-220_(B-1810-179).jpg |
| `ntsb` | ca19 | 2026 | CC0（関連） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:NTSB_Headquarters.jpg |
| `p51` | c404 c416 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `p95` | cb01 cb17 | 1996 | PDL1.0（頁） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `qa` | c306 | 2004 | GFDL 1.2（関連） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Airbus_A300B4-622R,_Air_Paradise_International_AN0658015.jpg |
| `qb` | c413 | 2003 | GFDL 1.2（関連） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Airbus_A300B4-605R,_Lufthansa_AN0529814.jpg |
| `qc` | c105 c918 cb07 | 2020 | CC BY 2.0（関連） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Das_Cockpit_des_Parabelfliegers_-_50375105997.jpg |
| `r01` | c103 cb28 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r02` | c815 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r03` | c101 c725 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r04` | c817 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r05` | cb03 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r08` | c109 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r09` | c319 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r10` | c305 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r11` | c104 c510 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r12` | c511 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r13` | c717 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r27` | c107 cb08 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r29` | c108 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r31` | c706 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r35` | c408 c607 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r36` | c209 c606 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r37` | c403 c405 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r38` | c217 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r39` | c604 c608 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r40` | c216 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r41` | c503 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r42` | c610 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r43` | c111 c505 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r44` | c112 c411 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `r49` | c724 | 1994 | PDL1.0（この事故） | 運輸省 航空事故調査委員会（報告書 96-5・1996年） | https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851 |
| `xf1` | c302 cb23 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/yoke-in-airplane-cockpit-2353936/ |
| `xg1` | c211 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/illuminated-top-of-a-plane-dashboard-12463498/ |
| `xg2` | c515 c707 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/an-aircraft-gear-shift-levers-and-illuminated-control-panel-6896137/ |
| `xh1` | c801 | 不明 | Pexels License（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/crescent-over-air-traffic-control-tower-at-night-20677027/ |
| `t1` | c202 ca06 | 1993 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep17/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:HONG_KONG_KAI_TAK_19_OCT_1993_CHINA_AIRLINES_AIRBUS_A300_B-1814.jpg |

## チェルノブイリ原発事故（1986-04-26・24本目）

※2026-10-22（⑤b-2）。`qa_out/ep24_assets.py credits --write` が書く（手で直さない）。写真と映像は映像方針の一覧 `ref/ep24/eizou_list24.md`（了承② 2026-10-22）。

### 0. 映像（フリー素材＝音はすべて使わない＝`-an`）
- フリー素材（Pexels・生成AI は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」だけ（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）

| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |
|---|---|---|---|---|
| `X13188726` | c101 cb23 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/13188726/ |
| `X13188720` | c107 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/13188720/ |
| `X12191470` | c621 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/12191470/ |
| `X13188723` | c927 cc20 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/13188723/ |
| `X13188717` | ca15 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/13188717/ |
| `X13183773` | cb22 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/13183773/ |

### 1. 写真・頁（IAEA Imagebank・Commons・USGS・報告書と会議録の頁）
- 🔴 **CC BY-SA は額装だけ**（了承② 決め4＝無加工・額ごと動かす・1点1カット＝`cuts/ss.check_frame_only`）。IAEA 0279 の34点は全部 CC BY-SA 2.0
- 🔴 **個人名義の点は画面の出典の行に作者欄の名前**。名前はこのリポに書かない＝`ref/ep24/credits.json` は印 `{作者}` だけ・焼くときに git の外の表から足す（`tools/scene_jiko.ep24_credit`・名乗りの短い形＝`_ep24_short`）。CC0・PD は表示が任意＝名前を出さない
- 「参考」＝この事故の物ではない実物（同じ型の炉＝レニングラード・クルスク・イグナリナ）＝20% の数（この事故の写真）に入れない
- 報告書・会議録の頁＝引用（著作権法32条＝無加工・出典）。頁は使う章のチャットで足す（⑤b-2 は c104 の INSAG-7 p.34 だけ）
- 撮影年＝Commons の撮影日の欄。IAEA 0279 の組の多くは欄が取り込みの日（2005・2006年）で説明に年が無い＝「不明」（副題に年を書かない）

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `az5` | c613 | 2019 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:%C5%98%C3%ADzen%C3%AD_jadern%C3%A9_%C4%8D%C3%A1sti_RBMK1000.jpg |
| `c0` | cc18 | 2008 | CC BY 3.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl,_fourth_reactor_bloc.JPG |
| `c1` | ca19 | 2008 | CC BY 3.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Reactor_bloc_of_the_Chernobyl_Nuclear_Power_Plant.JPG |
| `c2` | cb01 | 2007 | パブリックドメイン（この事故） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Chernobylreactor.jpg |
| `c27` | cb19 | 2018 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_-_39484641685.jpg |
| `c3` | cc05 | 2013 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_and_Pripyat_-_June_2013.jpg |
| `c3290` | cc09 | 2018 | CC0（この事故） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Chernobyl_nuclear_disaster_aftermath_abandoned_town_of_Pripyat_02.jpg |
| `c3305` | cc07 | 2018 | CC0（この事故） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Chernobyl_second_sarcophacus_2018_hnapel_14a.jpg |
| `c3309` | ca13 | 2013 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Construction_of_the_new_sarcophagus_in_Chernobyl.jpg |
| `c3313` | c904 | 2018 | パブリックドメイン（この事故） | NASA | https://commons.wikimedia.org/wiki/File:ISS-57_Chernobyl_Nuclear_Power_Plant,_Ukraine.jpg |
| `c3319` | cc10 | 2016 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:New_Safe_Confinement_Structure.jpg |
| `c475` | c923 | 2013 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_10_(13511028923).jpg |
| `c486` | c704 | 2017 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_nuclear_power_plant_(38342070546).jpg |
| `c488` | ca17 | 2006 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_Nuclear_Power_Plant_in_2006.jpg |
| `c496` | ca18 | 2016 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_snow_storm_(31397711360).jpg |
| `cia` | cb18 | 1996 | パブリックドメイン（頁） | CIA | https://commons.wikimedia.org/wiki/File:Chornobyl_radiation_map.jpg |
| `cr1` | c218 | 2011 | CC BY-SA 3.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:ChNPP_Unit1control.JPG |
| `cr3a` | c213 | 2010 | CC BY-SA 2.0（この事故） | IAEA Imagebank | https://commons.wikimedia.org/wiki/File:Control_Room_of_Chernobyl_Nuclear_Power_Plant_Unit_3.jpg |
| `cr3b` | c405 | 2021 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sterownia_reaktora_3_Czarnobylskiej_Elektrowni_Atomowej.jpg |
| `cr4` | c601 | 2021 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Sterownia_reaktora_4_Czarnobylskiej_Elektrowni_Atomowej.jpg |
| `cr4b` | cc16 | 2025 | CC0（この事故） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Physics_student_inside_the_Control_Room_of_Unit_4_at_Chernobyl_NPP.jpg |
| `cr4b2` | c418 | 2025 | CC0（この事故） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Physics_student_inside_the_Control_Room_of_Unit_4_at_Chernobyl_NPP.jpg |
| `gcp140` | c419 | 1986 | 引用（著作権法32条）（頁） | GC(SPL.I)/3＝INSAG-1 の Fig.9 | ref/ep24/src/gc_spl1_3_insag1text.pdf#140 |
| `gcp142` | c309 | 1986 | 引用（著作権法32条）（頁） | GC(SPL.I)/3＝INSAG-1 の Fig.11 | ref/ep24/src/gc_spl1_3_insag1text.pdf#142 |
| `gcp43` | c611 | 1986 | 引用（著作権法32条）（頁） | GC(SPL.I)/3＝INSAG-1 の図1 | ref/ep24/src/gc_spl1_3_insag1text.pdf#43 |
| `h01` | cc11 | 2018 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_second_sarcophacus_2018_hnapel_01.jpg |
| `h06` | ca21 | 2018 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_second_sarcophacus_2018_hnapel_06.jpg |
| `h11` | cc12 | 2018 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_second_sarcophacus_2018_hnapel_11.jpg |
| `i11` | cb20 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790011_(5613120994).jpg |
| `i13` | c818 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790013_(5613114278).jpg |
| `i14` | c716 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790014_(5613114630).jpg |
| `i15` | c103 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790015_(5613115146).jpg |
| `i18` | cc02 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790018_(5613118272).jpg |
| `i19` | c717 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790019_(5613119300).jpg |
| `i22` | c201 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790022_(5612542985).jpg |
| `i23` | c204 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790023_(5613122572).jpg |
| `i24` | c106 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790024_(5612544127).jpg |
| `i25` | c703 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790025_(5613123428).jpg |
| `i26` | c221 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790026_(5613123694).jpg |
| `i27` | c708 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790027_(5612545017).jpg |
| `i28` | c202 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790028_(5612545537).jpg |
| `i30` | c919 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790030_(5613125186).jpg |
| `i32` | c916 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790032_(5612547277).jpg |
| `i34` | c709 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790034_(5612537067).jpg |
| `i35` | cc03 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790035_(5612540377).jpg |
| `i36` | c105 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790036_(5613126700).jpg |
| `i40` | c819 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790040_(5612540779).jpg |
| `i42` | c921 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790042_(5613127192).jpg |
| `i44` | ca02 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790044_(5613128120).jpg |
| `i45` | c801 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790045_(5612549777).jpg |
| `i48` | c823 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790048_(5612550447).jpg |
| `i49` | c925 | 不明 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790049_(5612553615).jpg |
| `i50` | cc01 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790050_(5612554065).jpg |
| `i55` | ca09 | 1988 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790055_(5612554241).jpg |
| `i56` | c802 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790056_(5612555893).jpg |
| `i57` | c809 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790057_(5612555629).jpg |
| `i58` | c807 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790058_(5613134426).jpg |
| `i59` | c811 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790059_(5613134174).jpg |
| `i60` | c804 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790060_(5612554949).jpg |
| `i61` | c803 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790061_(5613133650).jpg |
| `i62` | c814 | 1986 | CC BY-SA 2.0（この事故） | IAEA Imagebank／Photo: USFCRFC | https://commons.wikimedia.org/wiki/File:IAEA_02790062_(5613133306).jpg |
| `iga` | c912 | 2024 | CC BY-SA 4.0（参考） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Ignalina_Nuclear_Power_Plant_Units.jpg |
| `igb` | ca06 | 2008 | CC0（参考） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Ignalina_Nuclear_Power_Plant,_Visaginas,_Lithuania_-_20080730.jpg |
| `k19860507` | c715 | 1986 | 引用（著作権法32条）（頁） | 国会会議録 1986-05-07 参議院 科学技術特別委員会 第6号 | https://kokkai.ndl.go.jp/img/110413928X00619860507 |
| `k19861127` | cb05 | 1986 | 引用（著作権法32条）（頁） | 国会会議録 1986-11-27 衆議院 科学技術委員会 | https://kokkai.ndl.go.jp/ |
| `l1p15` | cb16 | 2006 | 引用（著作権法32条）（頁） | チェルノブイリ・フォーラム 図3 | ref/ep24/src/forum_legacy_2006.pdf#15 |
| `l1p8` | cb11 | 2006 | 引用（著作権法32条）（頁） | チェルノブイリ・フォーラム『Chernobyl's Legacy』2006 の図1 | ref/ep24/src/forum_legacy_2006.pdf#8 |
| `lenn` | ca11 | 2010 | パブリックドメイン（参考） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Leningrad_Nuclear_Power_Plant_20JUL2010-4_(cropped_to_northern_reactor).jpg |
| `lenw` | c315 | 2010 | パブリックドメイン（参考） | Commons の投稿者（CC0・PD＝表示は任意） | https://commons.wikimedia.org/wiki/File:Leningrad_Nuclear_Power_Plant_20JUL2010-4_(cropped_to_western_reactor).jpg |
| `memf` | c702 | 2021 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:%D0%A2%D0%B8%D0%BC,_%D1%85%D1%82%D0%BE_%D0%B2%D1%80%D1%8F%D1%82%D1%83%D0%B2%D0%B0%D0%B2_%D1%81%D0%B2%D1%96%D1%82.jpg |
| `mit` | cb10 | 2013 | CC BY-SA 3.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Chernobyl_memorial.jpg |
| `mx7` | c618 | 2006 | CC BY 2.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Csernobil_makett_7.jpeg |
| `nsc17` | cc19 | 2017 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:NSC-Oct-2017.jpg |
| `p84_plant` | c223 | 1984 | パブリックドメイン（この事故） | USGS EarthExplorer（アメリカの偵察衛星） | https://commons.wikimedia.org/wiki/File:%D0%9F%D1%80%D0%B8%D0%BF%D1%8F%D1%82%D1%8C_1984.jpg |
| `p84_town` | c705 | 1984 | パブリックドメイン（この事故） | USGS EarthExplorer（アメリカの偵察衛星） | https://commons.wikimedia.org/wiki/File:%D0%9F%D1%80%D0%B8%D0%BF%D1%8F%D1%82%D1%8C_1984.jpg |
| `r09` | c505 | 2008 | CC BY-SA 3.0（参考） | RIA Novosti archive／作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:RIAN_archive_305009_Leningrad_nuclear_power_plant.jpg |
| `r1` | c712 | 1986 | CC0（この事故） | オランダ国立公文書館 | https://commons.wikimedia.org/wiki/File:Onderzoek_naar_veranderde_Radioactiviteit_door_RIVM_na_nucleaire_ramp_in_Sovjet_,_Bestanddeelnr_933-6455.jpg |
| `r11` | c212 | 2008 | CC BY-SA 3.0（参考） | RIA Novosti archive／作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:RIAN_archive_305011_Leningrad_nuclear_power_plant.jpg |
| `r15` | c207 | 2008 | CC BY-SA 3.0（参考） | RIA Novosti archive／作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:RIAN_archive_305015_Leningrad_nuclear_power_plant.jpg |
| `r94` | c413 | 2011 | CC BY-SA 3.0（参考） | RIA Novosti archive／作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:RIAN_archive_894445_Leningradskaya_nuclear_power_plant.jpg |
| `r96` | c511 | 2008 | CC BY-SA 3.0（参考） | RIA Novosti archive／作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:RIAN_archive_341196_Kursk_Nuclear_Power_Plant.jpg |
| `s1p127` | c304 | 1992 | 引用（著作権法32条）（頁） | INSAG-7 付属書II の図 II-3・II-4 | ref/ep24/src/insag7_pub913e.pdf#127 |
| `s1p128` | c411 | 1992 | 引用（著作権法32条）（頁） | INSAG-7 付属書II の図 II-5 | ref/ep24/src/insag7_pub913e.pdf#128 |
| `s1p129` | c604 | 1992 | 引用（著作権法32条）（頁） | INSAG-7 付属書II の図 II-6 | ref/ep24/src/insag7_pub913e.pdf#129 |
| `s1p133` | c907 | 1992 | 引用（著作権法32条）（頁） | INSAG-7 付属書II の図 II-10 | ref/ep24/src/insag7_pub913e.pdf#133 |
| `s1p138` | cc13 | 1992 | 引用（著作権法32条）（頁） | INSAG-7 付属書II の図 II-13 | ref/ep24/src/insag7_pub913e.pdf#138 |
| `s1p141` | c910 | 1992 | 引用（著作権法32条）（頁） | INSAG-7 付属書II の図 II-15 | ref/ep24/src/insag7_pub913e.pdf#141 |
| `s1p15` | c901 | 1992 | 引用（著作権法32条）（頁） | INSAG-7 の図1 | ref/ep24/src/insag7_pub913e.pdf#15 |
| `s1p28` | c513 | 1992 | 引用（著作権法32条）（頁） | INSAG-7 | ref/ep24/src/insag7_pub913e.pdf#28 |
| `s1p34` | c104 | 1992 | 引用（著作権法32条）（頁） | INSAG-7（IAEA 1992） | ref/ep24/src/insag7_pub913e.pdf#34 |
| `s1p41` | ca01 | 1991 | 引用（著作権法32条）（頁） | INSAG-7 付属書I | ref/ep24/src/insag7_pub913e.pdf#41 |
| `s1p63` | c305 | 1991 | 引用（著作権法32条）（頁） | INSAG-7 付属書I 表I-I | ref/ep24/src/insag7_pub913e.pdf#63 |
| `s1p65` | c619 | 1991 | 引用（著作権法32条）（頁） | INSAG-7 付属書I 表I-I | ref/ep24/src/insag7_pub913e.pdf#65 |
| `s2p18` | c812 | 1986 | 引用（著作権法32条）（頁） | GC(SPL.I)/3＝INSAG-1 の本文 | ref/ep24/src/gc_spl1_3_insag1text.pdf#18 |
| `s2p39` | c508 | 1986 | 引用（著作権法32条）（頁） | GC(SPL.I)/3＝INSAG-1 の本文 | ref/ep24/src/gc_spl1_3_insag1text.pdf#39 |
| `s3p19_s1p62` | c217 | 1986 | 引用（著作権法32条）（頁） | ソ連の報告 Part I（1986年8月）p.19 と INSAG-7 付属書I p.62 | ref/ep24/src/ussr_report_part1.pdf#19+ref/ep24/src/insag7_pub913e.pdf#62 |
| `s3p26` | c805 | 1986 | 引用（著作権法32条）（頁） | ソ連の報告 Part I（1986年8月） | ref/ep24/src/ussr_report_part1.pdf#26 |
| `s3p28` | c821 | 1986 | 引用（著作権法32条）（頁） | ソ連の報告 Part I（1986年8月） | ref/ep24/src/ussr_report_part1.pdf#28 |
| `sel` | c517 | 2014 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Selsyny_%C5%99%C3%ADd%C3%ADc%C3%ADch_ty%C4%8D%C3%AD.jpg |
| `t138` | ca23 | 2010 | CC BY-SA 2.0（この事故） | IAEA Imagebank | https://commons.wikimedia.org/wiki/File:The_damaged_unit_4_reactor_and_shelter_at_Chernobyl_(02710138).jpg |
| `t143` | c914 | 2010 | CC BY-SA 2.0（この事故） | IAEA Imagebank | https://commons.wikimedia.org/wiki/File:Transmission_towers_for_the_transfer_of_electricity_frame_the_damaged_unit_4_reactor_at_Chernobyl_(02710143).jpg |
| `t155` | cb03 | 2010 | CC BY-SA 2.0（この事故） | IAEA Imagebank | https://commons.wikimedia.org/wiki/File:The_damaged_unit_4_reactor_and_shelter_at_Chernobyl_(02710155).jpg |
| `t157` | ca08 | 2010 | CC BY-SA 2.0（この事故） | IAEA Imagebank | https://commons.wikimedia.org/wiki/File:The_ventilation_stack_of_the_damaged_unit_4_reactor_at_Chernobyl_(02710157).jpg |
| `t158` | cb07 | 2010 | CC BY-SA 2.0（この事故） | IAEA Imagebank | https://commons.wikimedia.org/wiki/File:Chernobyl_Unit_4_Reactor_(02710158).jpg |
| `u1_0422` | c102 | 1986 | パブリックドメイン（この事故） | USGS | ref/ep24/src/usgs/412_L.jpg |
| `u1_0429` | c102 | 1986 | パブリックドメイン（この事故） | USGS | ref/ep24/src/usgs/412_L.jpg |
| `u2` | c710 | 1986 | パブリックドメイン（この事故） | USGS | ref/ep24/src/usgs/0_4-29-1986_Chernobyl_Intro-label.png |
| `u4f12` | c711 | 1987 | パブリックドメイン（頁） | USGS | ref/ep24/src/usgs/1986_USGS_Image_Data_of_the_Nuclear_Accident_Near_Chernobyl_Report1.pdf#19 |
| `wbg` | cb14 | 1986 | CC BY-SA 4.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep24/src/credits_private.tsv`） | https://commons.wikimedia.org/wiki/File:Autoradiography,_grass_sample_after_Chernobyl_disaster_in_1986.jpg |

## JR福知山線脱線事故（2005-04-25・25本目）

※2026-10-25（⑤b-2）。`qa_out/ep25_assets.py credits --write` が書く（手で直さない）。写真と頁は映像方針の一覧 `ref/ep25/eizou_list25.md`（了承② 2026-10-25）。

### 0. 映像（フリー素材＝音はすべて使わない＝`-an`）
- フリー素材（Pexels・生成AI は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」だけ（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）
- 25本目は18カット＝⑤b-3 で取った（2026-10-25・カズヤくんの了承＝候補の名前・出どころ・大きさを示して先に聞いた・幅1920の版）。使う区間と寄せ（人の顔・字・ロゴ・会社の塗装を画面の外へ）は `qa_out/ep25_assets.py` の STOCK_WINDOW・STOCK_GEOM

| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |
|---|---|---|---|---|
| `X-depart` | c210 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/38837176/ |
| `X-desk` | c526 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/7685212/ |
| `X-training` | c532 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/6935499/ |
| `X-train` | c707 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/31065547/ |
| `X-blueprint` | c713 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/6615523/ |
| `X-signalwork` | c715 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/16222740/ |
| `X-platform` | c724 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/10677882/ |
| `X-clock` | c726 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/5220707/ |
| `X-signal` | c810 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/20312787/ |
| `X-train2` | c813 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/37514850/ |
| `X-court` | c902 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/39072934/ |
| `X-papers` | c920 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/9490310/ |
| `X-table` | ca05 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/5716999/ |
| `X-phone` | ca10 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/7661525/ |
| `X-meeting` | ca11 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/5519767/ |
| `X-janken` | ca13 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/8684433/ |
| `X-dusk` | cb13 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/16992918/ |
| `X-arrive` | cb14 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/33810511/ |

### 1. 写真・頁（運輸安全委員会の報告書・国土交通省の頁・国土地理院・裁判所・Commons）
- 報告書 RA2007-3・検証報告書・建議・国交省の発表＝公共データ利用規約（PDL1.0）＝出典の行「出典：…（運輸安全委員会の頁）を加工して作成」／「出典：国土交通省ウェブサイト（URL）」（了承② 決め4）。報告書の小さい写真も全面（原画＝PDF の上の注記は入らない）
- 会社の資料の写し（付図35・47・48）＝報告書に載った第三者の資料＝**頁ごと引用**（無加工・額装＝`frame`）
- 判決・決定＝著作権法13条（権利の目的とならない）。地理院の空中写真＝国土地理院コンテンツ利用規約（PDL1.0 準拠）
- 🔴 **人は役職だけ（①の承認）**＝名前の載る頁（建議 p.1・報告書の表紙の裏・最高裁の決定 p.1・検証報告書 p.50・p.53）は束の段で名前の外を切り出した（検証報告書 p.53 だけ姓の字に升目＝役職は残す）＝門番 `qa_out/ep25_assets.py names`（絵の OCR × git の外の名前の表）
- 🔴 **CC BY 3.0 の点は画面の出典の行に作者欄の名前**。名前はこのリポに書かない＝`ref/ep25/credits.json` は印 `{作者}` だけ・焼くときに git の外の表から足す（`tools/scene_jiko.ep25_credit`）。CC0 は表示が任意＝名前を出さない
- 撮影年＝Commons の撮影日・国交省の発表の日・資料の日。報告書の付図の写真は撮影の日の記載が無い＝「不明」（副題に年を書かない）

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `c10` | cb04 | 2025 | CC0（この事故・顔に升目） | Commons の投稿者（CC0＝表示は任意） | https://commons.wikimedia.org/wiki/File:Inori_no_mori,_the_scene_of_the_derailment_Accident_on_the_Fukuchiyama_Line.jpg |
| `c12` | cb05 | 2025 | CC0（この事故） | Commons の投稿者（CC0＝表示は任意） | https://commons.wikimedia.org/wiki/File:The_information_signboard_about_the_detour_on_25th_April_2025.jpg |
| `c13` | c802 cb11 | 2012 | CC0（この事故） | Commons の投稿者（CC0＝表示は任意） | https://commons.wikimedia.org/wiki/File:The_spot_where_Amagasaki_rail_crash_occurred.JPG |
| `c3` | c913 cb01 | 2016 | CC BY 3.0（この事故） | 作者欄のとおり（Commons の頁・名前は git の外 `ref/ep25/src/credits_private.tsv` の commons の行） | https://commons.wikimedia.org/wiki/File:Amagasaki-fukuchiyama_line.JPG |
| `c9` | cb02 cb12 | 2025 | CC0（この事故） | Commons の投稿者（CC0＝表示は任意） | https://commons.wikimedia.org/wiki/File:Inori_no_mori,_the_scene_of_the_Amagasaki_derailment.jpg |
| `f05_70` | c105 c509 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-2.pdf |
| `f05_7r` | c204 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-2.pdf |
| `f05_am` | c533 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-2.pdf |
| `f05_ar` | c615 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-2.pdf |
| `f07_f` | c320 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-2.pdf |
| `f07_s` | c414 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-2.pdf |
| `f11_p` | c402 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f11_w` | c417 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f12` | c103 c401 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_1b` | c520 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_1f` | c405 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_1m` | c620 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_1r` | c613 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_2d` | c406 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_2e` | c408 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_2f` | c403 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_3b` | cb07 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_3c` | c411 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_45` | c413 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f13_67` | c323 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-3.pdf |
| `f16_1d` | c504 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_1l` | c506 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_1m` | c222 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_1s` | c522 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_2a` | c322 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_2k` | c216 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_2r` | c224 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_2t` | c228 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_2u` | c309 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_3c` | c221 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_3p` | c704 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f16_3t` | c219 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `f26_1` | c102 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `f26_2` | c319 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `f26_3` | c515 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `f26_4` | c622 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `f26_5` | c721 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `f26_6` | ca02 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `f75` | c206 | 不明 | PDL1.0（この事故） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-7.pdf |
| `g1974` | c602 | 不明 | PDL1.0（この事故） | 国土地理院 | https://maps.gsi.go.jp/development/ichiran.html |
| `g1984` | c604 | 不明 | PDL1.0（この事故） | 国土地理院 | https://maps.gsi.go.jp/development/ichiran.html |
| `gnew` | c605 | 不明 | PDL1.0（この事故） | 国土地理院 | https://maps.gsi.go.jp/development/ichiran.html |
| `m050429` | c104 | 2005 | PDL1.0（この事故） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050430` | c229 c808 | 2005 | PDL1.0（この事故） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050501_2` | c303 | 2005 | PDL1.0（頁） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050501_3` | c202 | 2005 | PDL1.0（頁） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050502` | c907 | 2005 | PDL1.0（この事故） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050506_3` | c203 | 2005 | PDL1.0（この事故） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050517` | c330 | 2005 | PDL1.0（この事故） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050524_2` | c409 ca17 | 2005 | PDL1.0（この事故） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050804` | c416 c921 | 2005 | PDL1.0（この事故） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050811` | c419 | 2005 | PDL1.0（頁） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `m050818` | c404 | 2005 | PDL1.0（頁） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `msikensoukou` | c804 ca21 | 2005 | PDL1.0（この事故） | 国土交通省（航空・鉄道事故調査委員会の発表） | https://www.mlit.go.jp/fukuchiyama/index.html |
| `p_f05` | c601 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-2.pdf |
| `p_f16_1b` | c806 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `p_f16_1h` | c324 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-4.pdf |
| `p_f19_11` | c305 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f22_1` | c213 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f22_2` | c327 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f24_1` | c307 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f24_2` | c107 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f24_3` | c321 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f25_1` | c524 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f25_2` | c313 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f25_3` | c315 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f27_2` | c607 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f27_4` | c217 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f28` | c209 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f29` | c214 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f35` | c513 | 2007 | 引用（第三者の資料）（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-5.pdf |
| `p_f47` | c709 | 2003 | 引用（第三者の資料）（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-6.pdf |
| `p_f48` | c706 | 2003 | 引用（第三者の資料）（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-6.pdf |
| `p_f52` | c723 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-6.pdf |
| `p_f73` | c618 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-7.pdf |
| `p_f74` | c621 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-7.pdf |
| `p_i01` | c923 | 2006 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/ikenrail/shiryou/20070201-an01-honbun.pdf |
| `p_k05_1` | c805 | 2005 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/kyukengi/170906k.pdf |
| `p_r0` | ca18 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/rep-acci/RA2007-3-1.pdf |
| `p_r1_002` | c919 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf |
| `p_r1_030` | c410 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf |
| `p_r1_077` | c310 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf |
| `p_r1_220` | c519 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf |
| `p_r1_222` | c106 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf |
| `p_r1_230` | c711 ca01 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf |
| `p_r1_243` | c508 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf |
| `p_r1_264` | c501 | 2007 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf |
| `p_s1_50` | ca14 | 2011 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/fukuchiyama/kensyou/fu04-finalreport.pdf |
| `p_s1_53` | ca19 | 2011 | PDL1.0（頁・姓に升目） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/fukuchiyama/kensyou/fu04-finalreport.pdf |
| `p_s1k_2` | c208 | 2011 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/fukuchiyama/kensyou/fu04-finalreport-annex-2-2.pdf |
| `p_s1k_34` | c702 c716 | 2011 | PDL1.0（頁） | 運輸安全委員会（旧 航空・鉄道事故調査委員会） | https://jtsb.mlit.go.jp/fukuchiyama/kensyou/fu04-finalreport-annex-2-2.pdf |
| `p_s2_1` | c910 | 2017 | 著作権法13条（頁） | 裁判所 | https://www.courts.go.jp/assets/hanrei/hanrei-pdf-86834.pdf |
| `p_s2_5` | c912 | 2017 | 著作権法13条（頁） | 裁判所 | https://www.courts.go.jp/assets/hanrei/hanrei-pdf-86834.pdf |
| `p_s3_62` | c905 | 2012 | 著作権法13条（頁） | 裁判所 | https://www.courts.go.jp/assets/hanrei/hanrei-pdf-82178.pdf |

### 2. 地図の衛星写真（Google マップ）
- c101・c328・c517・ca23・cb03＝Google マップの衛星写真（束の外＝`cuts/ss.SAT`）。出典は画面の地図の右下の帰属の行（Google の地図の利用）＋出典の行「地図：Google マップの衛星写真（帰属は地図の右下）」。🔴 PNG は公開リポに置かない（git の外・md5 と出どころは `cuts/ss.SAT`・`GEO`）
- 🆕 ⑤b-3：描き足した線路の位置（c328・c517・ca23）＝国土地理院「地理院地図Vector」（experimental_bvmap・鉄道の中心線）を加工して作成（国土地理院コンテンツ利用規約＝出典の明示）＝額の下の断りに「線路の位置：地理院地図Vector（国土地理院）」・線の点は `cuts/ss.SAT_LINES`。駅と事故の現場の点＝Wikidata の座標（一般の座標＝断りに「一般の座標」）

## タイタニック号沈没事故（1912-04-15・26本目）

※2026-10-27（⑤b-2）。`qa_out/ep26_assets.py credits --write` が書く（手で直さない）。写真と頁は映像方針の一覧 `ref/ep26/eizou_list26.md`（了承② 2026-10-27）。

### 0. 映像（音はすべて使わない＝`-an`）
- **NOAA 2004 の残骸の映像**（N04＝米国海洋大気庁の Ocean Explorer の頁・5分53秒・640×426）＝頁の表記「Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.」（copyright・© の語なし＝NOAA の使い方の方針で courtesy は表記つきで使える）。画面の出典の行はこの表記のまま。13区間（扉を除くカットの秒＝narration.json の実測・`ref/ep26/eizou_build/list26.tsv`）・字の焼き込みも人も無い（映像方針で16コマを原寸）。【映像あり】に数えない（了承②）。映像そのものは git に入れない（焼くときに頁の直リンクから丸ごと取る＝`footage.local_media`・md5 は `ref/ep26/clips.json`）
- フリー素材（Pexels・生成AI は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」だけ（クレジットは任意＝投稿者の名前は書かない・概要欄にも書かない）。20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）＝26本目は8カット（⑤b-3 で取る）

| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |
|---|---|---|---|---|
| `N04` | c105 c107 c515 c813 c901 c907 c918 c926 c929 c932 c943 c944 ca13 | Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE. | courtesy（NOAA の使い方の方針・copyright の語なし） | https://archive.oceanexplorer.noaa.gov/explorations/04titanic/media/movies/titanic2004_video.html |
| `X-sea-stars` | c401 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/time-lapse-of-a-starry-night-sky-at-the-beach-13936805/ |
| `X-sea-calm` | c414 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/waves-on-the-beach-4938206/ |
| `X-flare-white` | c517 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/a-small-light-is-seen-in-the-dark-27456816/ |
| `X-ship-lights` | c610 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/nighttime-cruise-ship-on-patong-beach-waters-31085071/ |
| `X-dawn` | c638 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/aerial-view-of-calm-sea-at-sunrise-35466368/ |
| `X-meteor` | c939 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/stunning-night-sky-with-shooting-star-32270503/ |
| `X-flare-red` | ca11 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/the-lights-are-on-in-the-night-sky-17701269/ |
| `X-sea-night` | cb05 | イメージ（Pexels） | Pexels License | https://www.pexels.com/video/water-with-waves-11287848/ |

### 1. 写真・頁（Commons の PD・NOAA 2003・英国の審問の報告・MAIB 1992・米国の法）
- Commons の PD＝出どころの機関の名（NARA・LOC・BnF・オランダ国立公文書館・北アイルランド国立博物館）か「Wikimedia Commons（パブリックドメイン）」（了承② 決め4）。色は原本のまま・小さい写真も全面（ぼけは差し替えの理由にしない）
- NOAA 2003 の写真2点＝NOAA の頁の courtesy の表記（撮影者の個人名つき）。🔴 名前はこのリポに書かない＝`ref/ep26/credits.json` は印 `{作者}` だけ・焼くときに git の外の表から足す（`tools/scene_jiko.ep26_credit`）
- 英国の審問の報告（米国上院の刷り直し S. Doc. 933）・米国の法＝米国の公文書（PD）＝出典の行は資料名と頁。MAIB 1992＝引用の型（出典・主従・必要最小限・**無加工の額装**＝`frame`）
- 🔴 **人は名前＋役職か役職だけ・乗客は名前なし（①・承認①）**＝会社の人・議員の名（ネガの字）・MAIB の署名・電信会社の社長の名・カリフォルニアン号の機関部の乗組員の名前は束の段で切り出しの外（`qa_out/ep26_assets.py` の PHOTO_CROP・PAGE_CROP）。乗客の顔が分かる所は顔だけ升目（PD・MASK）
- 撮影年＝Commons の頁と置き場の説明の年（sources26 の題・根拠の欄）・NOAA の頁（2003）・頁は資料の年。年の分からない点は「不明」（副題に年を書かない）

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `p_g1_005` | c803 | 1912 | PD（頁） | 英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書 | https://www.govinfo.gov/content/pkg/SERIALSET-06179_00_00-019-0933-0000/pdf/SERIALSET-06179_00_00-019-0933-0000.pdf |
| `p_g1_041` | c806 | 1912 | PD（頁・名前の外を切り出し） | 英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書 | https://www.govinfo.gov/ |
| `p_g1_054` | c514 | 1912 | PD（頁） | 英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書 | https://www.govinfo.gov/ |
| `p_g1_056` | c603 | 1912 | PD（頁） | 英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書 | https://www.govinfo.gov/ |
| `p_g1_058` | c628 | 1912 | PD（頁・名前の外を切り出し） | 英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書 | https://www.govinfo.gov/ |
| `p_g1_059` | c635 | 1912 | PD（頁） | 英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書 | https://www.govinfo.gov/ |
| `p_g1_060` | c818 | 1912 | PD（頁） | 英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書 | https://www.govinfo.gov/ |
| `p_g1_076` | c215 | 1912 | PD（頁） | 英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書 | https://www.govinfo.gov/ |
| `p_g1_085` | c809 | 1912 | PD（頁） | 英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書 | https://www.govinfo.gov/ |
| `p_g2_01` | c904 | 1992 | 引用（OGL v3.0・© Crown copyright＝gov.uk の頁）（頁・名前の外を切り出し） | 英国運輸省 海難調査局（MAIB） | https://assets.publishing.service.gov.uk/media/54c15bf240f0b6158d000027/MAIBReport_ReappraisalOfEvidence-SSCalifornian-Titanic-1992.pdf |
| `p_g2_03` | c906 | 1992 | 引用（OGL v3.0・© Crown copyright＝gov.uk の頁）（頁・名前の外を切り出し） | 英国運輸省 海難調査局（MAIB） | https://assets.publishing.service.gov.uk/ |
| `p_g2_18` | c930 | 1992 | 引用（OGL v3.0・© Crown copyright＝gov.uk の頁）（頁・名前の外を切り出し） | 英国運輸省 海難調査局（MAIB） | https://assets.publishing.service.gov.uk/ |
| `p_g2_21` | c937 | 1992 | 引用（OGL v3.0・© Crown copyright＝gov.uk の頁）（頁・名前の外を切り出し） | 英国運輸省 海難調査局（MAIB） | https://assets.publishing.service.gov.uk/ |
| `p_g2_22` | c941 | 1992 | 引用（OGL v3.0・© Crown copyright＝gov.uk の頁）（頁・名前の外を切り出し） | 英国運輸省 海難調査局（MAIB） | https://assets.publishing.service.gov.uk/ |
| `p_g2_23` | cb02 | 1992 | 引用（OGL v3.0・© Crown copyright＝gov.uk の頁）（頁・名前の外を切り出し） | 英国運輸省 海難調査局（MAIB） | https://assets.publishing.service.gov.uk/ |
| `p_g4_2` | ca02 | 1912 | PD（頁） | 米国議会（法） | https://www.govinfo.gov/link/statute/37/199 |
| `s10_871` | c412 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s10_905` | c503 c814 | 1912 | PD（この事故） | オランダ国立公文書館（Spaarnestad Photo）（Commons の版） | https://commons.wikimedia.org/ |
| `s11_716` | c826 | 2003 | courtesy（NOAA・copyright の語なし）（この事故） | NOAA の頁の courtesy の撮影者（名前は git の外 `ref/ep26/src/credits_private.tsv` の (sources26, 記号) の行） | https://archive.oceanexplorer.noaa.gov/explorations/03titanic/media/titanic_bathtub.html |
| `s11_910` | c903 | 2003 | courtesy（NOAA・copyright の語なし）（この事故） | NOAA の頁の courtesy の撮影者（名前は git の外 `ref/ep26/src/credits_private.tsv` の (sources26, 記号) の行） | https://archive.oceanexplorer.noaa.gov/explorations/03titanic/welcome.html |
| `s12_913` | ca09 | 1923 | PD（この事故） | 米国議会図書館（LOC）（Commons の版） | https://commons.wikimedia.org/ |
| `s1_002` | c101 cb07 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s1_013` | c304 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s1_016` | c203 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s1_017` | c415 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s1_020` | c407 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s1_032` | c213 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s1_042` | c201 | 1912 | PD（この事故） | 北アイルランド国立博物館（Harland & Wolff Collection）（Commons の版） | https://commons.wikimedia.org/ |
| `s1_053` | c204 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s1_057` | c219 | 1912 | PD（この事故・顔に升目） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s1_076` | c404 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s1_084` | c205 cb03 | 1912 | PD（この事故） | オランダ国立公文書館（Spaarnestad Photo）（Commons の版） | https://commons.wikimedia.org/ |
| `s1_089` | c212 c920 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s2_033` | c217 c922 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s2_045` | c207 c519 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s2_054` | c208 c509 | 1912 | PD（この事故・顔に升目） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s2_070` | c518 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s2_085` | c315 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s2_206` | c220 c321 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s2_724` | c410 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s2_e01` | c616 ca01 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_352` | c301 | 不明 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_424` | c511 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_577` | c711 | 1912 | PD（この事故） | 米国議会図書館（LOC）（Commons の版） | https://commons.wikimedia.org/ |
| `s3_671` | c636 c801 | 1912 | PD（この事故・顔に升目） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_675` | c601 c622 c824 cb01 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_698` | c819 | 不明 | PD（この事故・名前の外を切り出し） | 米国議会図書館（LOC）（Commons の版） | https://commons.wikimedia.org/ |
| `s3_714` | c216 c805 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_736` | c402 c513 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_749` | c608 c624 c934 | 1908 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_753` | c709 c916 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_784` | c502 | 不明 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s3_810` | c405 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s4_228` | c310 | 1912 | PD（この事故） | 米国立公文書館（NARA）（Commons の版） | https://catalog.archives.gov/id/595107 |
| `s4_242` | c305 | 1912 | PD（この事故） | 米国議会図書館（LOC）（Commons の版） | https://commons.wikimedia.org/ |
| `s4_254` | c703 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s4_264` | c214 | 1912 | PD（この事故・名前の外を切り出し） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s4_300` | ca05 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s4_320` | c507 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s4_n06` | c309 | 1912 | PD（この事故・名前の外を切り出し） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/wiki/File:Amerika14April1912.JPG |
| `s5_357` | c314 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s5_358` | c307 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s5_359` | c103 | 1912 | PD（この事故） | 米国立公文書館（NARA）（Commons の版） | https://catalog.archives.gov/id/278334 |
| `s5_362` | c318 c817 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s5_365` | c409 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s6_372` | c718 ca12 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s6_377` | ca07 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s6_379` | c717 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s6_383` | c707 | 1912 | PD（この事故・顔に升目） | オランダ国立公文書館（Spaarnestad Photo）（Commons の版） | https://commons.wikimedia.org/ |
| `s6_427` | c714 | 1912 | PD（この事故・顔に升目） | 米国議会図書館（LOC）（Commons の版） | https://commons.wikimedia.org/ |
| `s6_480` | c104 c641 cb04 | 1912 | PD（この事故） | フランス国立図書館（BnF）（Commons の版） | https://gallica.bnf.fr/ |
| `s6_619` | c713 | 1912 | PD（この事故） | 米国議会図書館（LOC）（Commons の版） | https://commons.wikimedia.org/ |
| `s7_594` | c808 | 1912 | PD（この事故） | フランス国立図書館（BnF）（Commons の版） | https://gallica.bnf.fr/ |
| `s7_598` | c942 | 1912 | PD（この事故） | 米国議会図書館（LOC）（Commons の版） | https://commons.wikimedia.org/ |
| `s8_625` | c102 c605 c811 cb06 | 不明 | PD（この事故） | 米国立公文書館（NARA）（Commons の版） | https://catalog.archives.gov/id/278339 |
| `s8_630` | c316 c520 c640 | 1907 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s8_e03` | c106 c716 c931 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s8_n01` | c308 | 1904 | PD（この事故） | 北アイルランド国立博物館（Harland & Wolff Collection）（Commons の版） | https://commons.wikimedia.org/wiki/File:The_3rd_Big_Four_liner_Baltic_(II).jpg |
| `s8_n02` | c312 | 不明 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/wiki/File:SS_Mesaba.png |
| `s8_n03` | c504 | 不明 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/wiki/File:RMS_Carpathia.jpg |
| `s8_n04` | c715 | 不明 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/wiki/File:SS_Mount_Temple_in_London.jpg |
| `s8_n05` | c924 | 不明 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/wiki/File:1905_White_Star_Line_piers_New_York.jpg |
| `s9_645` | c705 c821 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |
| `s9_648` | c323 c820 | 1912 | PD（この事故・顔に升目） | 米国議会図書館（LOC）（Commons の版） | https://commons.wikimedia.org/ |
| `s9_674` | c629 c802 c823 | 1912 | PD（この事故） | Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄） | https://commons.wikimedia.org/ |

### 2. 地図の衛星写真（Google マップ）
- c218・c306・c909・c917＝Google マップの衛星写真＋描き足し（束の外＝`cuts/ss.SAT`・⑤b-3 で撮る）。出典は画面の地図の右下の帰属の行（Google の地図の利用）。🔴 PNG は公開リポに置かない（git の外・md5 と出どころは `cuts/ss.SAT`・`GEO`）

## 八田與一容疑者の事件（2022-06-29・27本目）

※2026-10-30（⑤b-2・⑤b-3）。`qa_out/ep27_assets.py credits --write` が書く（手で直さない）。写真は映像方針の一覧 `ref/ep27/eizou_list27.md`（了承② 2026-10-29・⑤b-3 の YT-A の当て直しは 10-30 カズヤくん了承）。
🔴 事件の回（ルール §B2-10）＝被害者・遺族・けがをした人・目撃者・SNS の投稿者の名前は書かない・容疑者は必ず「八田與一容疑者」。

### 0. 県警の動画（引用＝話している秒だけ・カットの秒で実時間・加工しない・音は使わない＝`-an`・サムネに使わない）
- 大分県の「著作権・リンク等について」は「『私的使用のための複製』や『引用』など著作権法で認められた場合を除き」無断の転載・複製・改変を禁じる＝引用は県が禁止の外に置く（`ref/ep27/materials.md` §1）。🔴 **動画も、そこから抜いたコマも公開リポに置かない**（焼くのは Modal＝保管庫）。🔴 YT-A の 0〜20秒・153.5〜159.25秒（重要指名手配のポスター＝小さな字に「犯人」）は使わない（門番 `make_list27.BAD`）

| 記号 | 使うカット | 画面の出典 | 使い方 | 取得 |
|---|---|---|---|---|
| `YT-A` |  | 出典：大分県警察 公式YouTube（2024年8月1日） | 引用（話している秒だけ・実時間・音は使わない） | 🔴 取れない（⑤b-2 の 403・回避しない）＝動画は使わない（⑤b-3：コマ YTA026 YTA034 YTA094 YTA165 を静止の引用に） |
| `YT-C` | c106 c305 | 出典：大分県警察 公式YouTube（2025年12月11日） | 引用（話している秒だけ・実時間・音は使わない） | 取得ずみ（git の外・md5 は clips.json） |

### 1. 写真（Commons の CC BY・BY-SA・CC0・Pexels のイメージ・県警と警察庁の引用）
- CC BY・BY-SA＝「写真：{作者}／Wikimedia Commons（ライセンス）」。🔴 撮影者の名前はこのリポに書かない＝`ref/ep27/credits.json` は印 `{作者}` だけ・焼くときに git の外の表 `ref/ep27/src/credits_private.tsv` から足す（`tools/scene_jiko.ep27_credit`）。CC0＝「Wikimedia Commons（CC0）」
- BY-SA＝額装（無加工・1点1カット・升目もかけない）。CC BY・CC0 の顔の分かる人は顔だけ升目（「／改変：顔にモザイク」）。色は原本のまま
- 説明カットの地（「地 c…」）＝CC BY・CC0 の写真を暗くするだけ（字と地の比 8:1 が下限＝了承② 決め1・出典の行は「地の写真：…／改変：明るさ」＝⑤b-3）
- イメージ（Pexels の写真）＝`ep27/stock/` の名・画面の左上に「イメージ」・20% に数えない・git に入れない（焼くときに直リンクから取り直して md5 を照らす）
- 県警・警察庁の引用（`ep27/police/` の名）＝**公開リポに置かない**（git の外・Modal の保管庫）・額装・加工しない（似顔絵は並べ方だけ）
- 撮影年＝Commons の頁の撮影日・県警の頁と動画の公開日（sources27 の時期の欄）。イメージは「不明」（副題に年を書かない）

| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |
|---|---|---|---|---|---|
| `cm001` | c319 | 2016 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM001 |
| `cm014` | c505 | 2024 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM014 |
| `cm022` | c413 | 2016 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM022 |
| `cm039` | c220 | 2016 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM039 |
| `cm040` | c514 | 2016 | CC BY-SA 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM040 |
| `cm044` | c204（地 c201 c203 c205 c517 c518） | 2022 | CC BY 2.0（この事件の土地・顔に升目） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM044 |
| `cm045` | c105（地 c519） | 2022 | CC BY 2.0（この事件の土地・顔と店名に升目） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM045 |
| `cm046` | c215 | 2022 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM046 |
| `cm051` | c516 | 2015 | CC BY 3.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM051 |
| `cm054` | c107 c706 | 2017 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM054 |
| `cm056` | c217 c705（地 c218） | 2020 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM056 |
| `cm057` | c704 | 2016 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM057 |
| `cm059` | c610 | 2016 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM059 |
| `cm072` | c101 | 2024 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM072 |
| `cm074` | c609 | 2024 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM074 |
| `cm075` | c219 | 2024 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM075 |
| `cm076` | c415 | 2024 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM076 |
| `cm102` | c520 | 2011 | CC BY 3.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM102 |
| `cm106` | c506（地 c501 c502 c503 c508） | 2020 | CC0（この事件の土地・店名に升目） | Commons の投稿者（CC0＝表示は任意） | commons:CM106 |
| `cm108` | c412 | 2023 | CC0（この事件の土地） | Commons の投稿者（CC0＝表示は任意） | commons:CM108 |
| `cm110` | c408（地 c410） | 2023 | CC0（この事件の土地） | Commons の投稿者（CC0＝表示は任意） | commons:CM110 |
| `cm112` | c411 | 2023 | CC0（この事件の土地・店名に升目） | Commons の投稿者（CC0＝表示は任意） | commons:CM112 |
| `cm144` | c320（地 c401） | 2022 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM144 |
| `cm145` | c315 | 2022 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM145 |
| `cm151` | c304 c703（地 c302 c513 c515） | 2022 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM151 |
| `cm152` | c307（地 c306） | 2022 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM152 |
| `cm153` | c308 c702（地 c310 c701） | 2022 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM153 |
| `cm154` | c214 c608 | 2022 | CC BY 2.0（この事件の土地・顔に升目） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM154 |
| `cm156` | c311（地 c312） | 2011 | CC BY 3.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM156 |
| `cm198` | c414 c616（地 c103） | 2020 | CC0（この事件の土地） | Commons の投稿者（CC0＝表示は任意） | commons:CM198 |
| `cm202` | c613 | 2016 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM202 |
| `cm203` | c507 | 2016 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM203 |
| `cm204` | c611 | 2016 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM204 |
| `cm205` | c602（地 c612） | 2011 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM205 |
| `cm208` | c206（地 c208） | 2022 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM208 |
| `cm254` | c404（地 c405 c406 c407 c605 c606 c607） | 2022 | CC BY 2.0（この事件の土地・店名に升目） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM254 |
| `cm257` | c317 c614（地 c318 c615） | 2013 | CC BY 3.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM257 |
| `cm258` | c209 c417（地 c210 c416） | 2013 | CC BY 3.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM258 |
| `cm259` | c402（地 c403） | 2013 | CC BY 3.0（この事件の土地・店名に升目） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM259 |
| `cm283` | c211 | 2022 | CC BY 2.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM283 |
| `cm289` | c409 | 2016 | CC BY-SA 4.0（この事件の土地） | Commons の撮影者（名前は git の外 `ref/ep27/src/credits_private.tsv` の記号の行＝画面は焼くときに足す） | commons:CM289 |
| `npa01` | c301 | 2022 | 引用（著作権法32条・大分県の頁が引用を禁止の外に置く）（引用・非公開） | 警察庁の重要指名手配の頁（写真は大分県警察＝第三者の権利） | web:npa_wanted_01.jpg |
| `sketch2` | c314 | 2024 | 引用（著作権法32条・大分県の頁が引用を禁止の外に置く）（引用・非公開） | 大分県警察 | web:2323829_4634890・4634891_misc.jpeg |
| `sketch6` | c313 | 2024 | 引用（著作権法32条・大分県の頁が引用を禁止の外に置く）（引用・非公開） | 大分県警察 | web:2323829_4634889〜4634894_misc.jpeg |
| `xpost1` | c603 c604 | 2026 | 引用（著作権法32条・大分県の頁が引用を禁止の外に置く）（引用・非公開） | 大分県警察 | x:oita_police/status/2071406565274640830 photo/1 |
| `yta026` | c102 | 2024 | 引用（著作権法32条・大分県の頁が引用を禁止の外に置く）（引用・非公開） | 大分県警察（公式 YouTube の手配の動画の1コマ） | frame:YT-A@26.0 |
| `yta034` | c309 | 2024 | 引用（著作権法32条・大分県の頁が引用を禁止の外に置く）（引用・非公開） | 大分県警察（公式 YouTube の手配の動画の1コマ） | frame:YT-A@34.0 |
| `yta094` | c303 | 2024 | 引用（著作権法32条・大分県の頁が引用を禁止の外に置く）（引用・非公開） | 大分県警察（公式 YouTube の手配の動画の1コマ） | frame:YT-A@94.0 |
| `yta165` | c316 | 2024 | 引用（著作権法32条・大分県の頁が引用を禁止の外に置く）（引用・非公開） | 大分県警察（公式 YouTube の手配の動画の1コマ） | frame:YT-A@165.0 |
| `px30037331` | c207 | 不明 | Pexels License（イメージ）（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/30037331/ |
| `px7146298` | c509 | 不明 | Pexels License（イメージ）（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/7146298/ |
| `px7508684` | c512 | 不明 | Pexels License（イメージ）（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/7508684/ |
| `px7553959` | c510 | 不明 | Pexels License（イメージ）（イメージ） | 投稿者（クレジットは任意＝書かない） | https://www.pexels.com/photo/7553959/ |

### 2. 地図の衛星写真（Google マップ）
- G1・G2・G3・G7・G9（9カット）＝Google マップの衛星写真＋描き足し（束の外＝`cuts/ss.SAT`・⑤b-4 で撮る）。出典は画面の地図の右下の帰属の行（Google の地図の利用）。🔴 PNG は公開リポに置かない（git の外・Modal の保管庫）
