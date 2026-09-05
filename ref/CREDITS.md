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
