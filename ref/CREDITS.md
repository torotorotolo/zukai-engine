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

❌ 図11・図12（海底の残骸）は同じ手順で取り出せるが **Pelagic Research Services**
なので取り出したファイルごと捨てた。図1・2はOceanGate、図5・6はGoogle Maps、
図9はA. Harvey、図23はMTSなので同様に使わない。
