# キー橋（6本目）— 一次資料から取り直した数字と原文

**この表に無い数字は、まだ照合していません。** ④の台本・画面・タイトルに出してよいのは、
ここに「✅」が付いている行と、`ntsb_MIR2540.txt` を自分で引いて確かめた行だけです。
→ [[feedback-secondhand-numbers-differ-from-the-original]] / [[feedback-verify-every-onscreen-quote]]

## 0. 出どころ（2026-09-08 に取得・②素材）

| 略号 | 何 | 実体 | 文字層 |
|---|---|---|---|
| **MIR-25-40** | NTSB 最終報告『Contact of Containership Dali with Francis Scott Key Bridge and Subsequent Bridge Collapse』 | `ref/keybridge/ntsb_MIR2540.pdf`（10.8MB） | ✅ **259頁すべてに有り**（521,788字・図81点）。OCR不要 |
| **MIR-25-10** | NTSB『Safeguarding Bridges from Vessel Strikes』 | `ref/keybridge/ntsb_MIR2510.pdf`（1.4MB） | ✅ 26頁すべてに有り（54,267字） |
| 抽出テキスト | 上の2本を頁ごとに割った素のテキスト | `ntsb_MIR2540.txt` / `ntsb_MIR2510.txt` | 頁の区切りは `=== p<PDFの頁> ===` |

⚠️ **PDFの頁と報告書の頁番号は2ずれています**（前付が i〜xxii）。報告書 p25 ＝ PDF p27。
- MIR-25-40 の PDF 作成日時 **2025-12-09 12:46 (EST)**。「2025-12-10 公表」は未照合のまま。
- 公開ドケット `https://data.ntsb.gov/Docket/?NTSBNumber=DCA24MM031`（未取得。写真の点数は未確認）

## 1. 事故の骨格（✅ すべて MIR-25-40 の原文）

| 事実 | 値 | 出どころ |
|---|---|---|
| ✅ 発生 | **2024年3月26日 約0129（現地時間）** | Executive Summary / p.xii |
| ✅ 船 | シンガポール船籍のコンテナ船 **Dali**・**全長984フィート**（約300m） | 同上 |
| ✅ ぶつかった先 | 中央径間を支える**南側の橋脚 Pier 17** | 同上 |
| ✅ 橋の上にいた人 | 道路補修班 **7名**（Brawner Builders 社）＋ **点検員1名**（Eborn Enterprises 社） | p.xii／2.5.3 |
| ✅ 亡くなった人 | **道路作業員6名** | p.xii |
| ✅ 生き残った人 | 作業員 **1名が重傷を負って生還**・**点検員は無傷** | p.xii |
| ✅ 船側 | 乗船 **23名**のうち1名が軽傷 | p.xii |
| ✅ 船の損害 | **1,800万ドル超**（積荷の損害は未確定） | p.xii |
| ✅ 架け替え | **43〜52億ドル**・**2030年後半**に開通見込み | p.xii |
| ✅ 迂回 | 1日**34,000台超**（うち10%がトラック）。危険物車両はトンネルを通れず大回り | p.xii |

🔴 **「生存者」がいます。**（効く語＝証言・記録・**生存者**＝1.94倍。→ [[feedback-jiko-thumbnail-rival-format]]）

## 2. 推定原因（✅ 原文。④で読む文はここから訳す）

> The National Transportation Safety Board determines that the probable cause of the contact of the
> containership Dali with the Francis Scott Key Bridge was **a loss of electrical power (blackout), due to
> a loose signal wire connection to a terminal block stemming from the improper installation of
> wire-label banding**, resulting in the vessel's loss of propulsion and steering close to the bridge.
> — MIR-25-40 報告書 p.202「Probable Cause」

**寄与要因は3つ**（引き継ぎの要約は1つ目しか書いていなかった）:

1. 停電から推進を回復するには**橋に近すぎて時間が足りなかった**こと。
2. **橋の側に、外航船の衝突で崩れないための対策が無かった**こと。
   AASHTO が勧めていた**脆弱性評価を MDTA（メリーランド州交通局）が実施していれば**打てた対策だった。
3. 🔴 **橋の上の作業員に退避を知らせる、実効的で即時の連絡手段が無かった**こと。

## 3. 4分9秒（✅ 秒はすべて原文。1.1.2 Event Sequence／報告書 p25〜）

括弧内は**衝突までの残り時間**（報告書の書き方そのまま）。

| 時刻 | 何が起きたか |
|---|---|
| 0005 | 水先人2名（メリーランド州水先人組合の上級水先人と訓練生）が乗船 |
| 0036 | タグボート2隻の補助で離岸 |
| 0107 / 0108 | タグを順に離す。主航路（Fort McHenry Channel）を南西へ |
| 0121 | 上級水先人が訓練生に「10ノット以下に保て」 |
| **0125:00（-4:09）** | **低圧側の停電。舵を失う。**速力8.9ノット・針路142°・**橋まで約3,200フィート**（船体3.3隻ぶん） |
| 0125:03（-4:06） | 航海データ記録装置（VDR）がデータの記録を止める |
| 0125:08（-4:01） | **主機関が停止。推進を失う** |
| 0125:58（-3:11） | 停電から58秒。電気技師が「高圧は生きていて低圧だけ落ちている」と気づく |
| 0126:10（-2:59） | 非常用発電機が非常母線に接続。操舵ポンプ3号機が動く |
| 0126:38（-2:31） | 上級水先人が無線でタグを要請 |
| **0126:44** | **水先人組合の配車係が MDTA の当直に電話。「橋を通行止めにしてほしい」** |
| 0127:02（-2:07） | 橋まで約1,500フィート。左舷錨を投下せよの号令 |
| 0127:04 | **2度目の停電** |
| 0127:36（-1:33） | 電気技師が別の変圧器の遮断器を手で閉じ、低圧が復旧 |
| 0127:46（-1:23） | 橋まで **939フィート**（船体1隻ぶんを切る）。速力7.5ノット |
| **0127:53（-1:16）** | 🔴 **MDTA 当直が、橋の両端にいた警官に「車を止めろ」と指示** |
| 0127:55（-1:14） | 甲板長「錨のブレーキが開かない」 |
| 0128:10（-0:59） | 船首が航路の外へ。Pier 17 の近くの泥に乗り上げ始める |
| **0128:21（-0:48）** | **両端の警官が車線を塞ぐ。一般車両は橋に入らなくなった** |
| 0128:42 | 甲板長がブレーキを手で外し、錨が落ちる |
| **0129:09** | **船首右舷が Pier 17 の北西柱に接触**（6.4ノット） |
| **0129:22** | 接触から約13秒で **Pier 17 が崩れる** |
| 0155 | 生還した作業員が Pier 20 付近で MDTA 警察の艇に救助される |

## 4. 🔴 決め所：1分16秒（✅ 2.5.3 Highway Worker Emergency Communications／報告書 p177）

- 点検員は、橋の両端の MDTA 警官と作業長と**携帯番号を交換していた**。
- それでも、警官は通行止めの指示を受けたとき**点検員に電話をかけなかった**。
  応援が来てから橋に乗り入れて知らせるつもりだった。**その前に船が当たった。**
- 作業員は Span 18 と Span 20 の車内で休憩中。点検員は Span 22 を歩いていた。
- 崩れなかったいちばん近い場所は **Span 16**。Span 20 の車から **2,928フィート**、Span 18 の4台から **1,694フィート**。
- 🔴 **警官が知らされたのと同じ時に作業員も知らされていれば、衝突まで1分16秒**
  （崩落までなら1分29秒）**あった。NTSB は「退避して崩れない径間に着くのに足りたかもしれない」と結論している。**

> The NTSB concludes that had the inspector and highway workers been notified of the Dali's emergency
> situation about the same time the MDTA police officers at each end of the bridge were told to block
> vehicular traffic, the highway workers may have had sufficient time to drive to a portion of the bridge
> that did not collapse. — 報告書 p177

## 5. 橋そのもの（✅ 1.5.1 General／報告書 p60）

| 事実 | 値 |
|---|---|
| ✅ 開通 | **1977年3月23日**（＝崩落の **47年と3日前**） |
| ✅ 形式 | 連続鋼スルートラス橋。メリーランド州道695号を Patapsco 川に渡す。MDTA が保有・運営 |
| ✅ 全長 | **9,086フィート＝約2,769m**（⚠️ 引き継ぎの「2.6km」は不正確。**2.77km と書く**） |
| ✅ 桁下 | 主航路（幅700フィートの Fort McHenry 連邦航路）上で **185フィート** |
| ✅ 下部構造 | 橋台2基＋**橋脚36基** |
| 🔴 ✅ **NSTM** | **nonredundant steel tension member ＝ 非冗長鋼引張部材**（2022年まで "fracture critical member" と呼ばれた）。定義は「①鋼製 ②全部または一部が引張 ③**その1部材が壊れると橋が部分的または全体的に崩れる**」。24か月以内ごとに腕の届く距離での点検が要る | |

→ 第6章「なぜ2.77kmが一度に落ちたのか」の答えはここ。**連続トラス＋NSTM**。

## 6. ⚠️ 1980年（1977年？）Blue Nagoya — 報告書の中で年が食い違う

報告書 **1.5.4 の節の題は「1977 Contact by Containership Blue Nagoya」**なのに、
**本文は "The Key Bridge's pier protection was struck in 1980"** と書いています（報告書 p72）。

- 日本船籍・全長390フィートのコンテナ船 **Blue Nagoya**（排水量は Dali の**約10分の1**）が
  **橋から約600ヤードで操舵を失い、同じ Pier 17 に衝突**。
- **圧壊するコンクリートと木材の防衝工が船を止めた。**柱には軽微な表面損傷だけ。防衝工は原設計どおり作り直された。
- 出典表記は (National Research Council 1983; AASHTO 2009)。

🔴 **④で年を1つに決めるまで、画面にもナレーションにも年を出さない。**
（ドケットか AASHTO 2009 の原文に当たる。→ [[feedback-secondhand-numbers-differ-from-the-original]]）

## 7. ⚠️ 素材の説明文にある誤り（画面に写さない）

- Commons/DVIDS の `240326-G-KH296-2189`（沿岸警備隊の説明文）は
  **"a 948-foot containership"** と書いていますが、MIR-25-40 は **984フィート**。**数字が入れ替わっています。**
  → 一次資料を採る。**984フィート**。

## 8. 報告書の章立て（④の章割りの下敷き。報告書の頁番号）

| 節 | 中身 | 頁 |
|---|---|---|
| 1.1.2 | Event Sequence（分秒の並び） | 25 |
| 1.2 | Response（捜索救助・統合指揮・油と危険物・ガス管・サルベージ） | 51 |
| 1.3 / 1.4 | Injuries / Damage（Dali・橋） | 56 |
| 1.5 | Bridge Information（諸元・**橋脚の防護**・他橋の防護・**1977/1980 Blue Nagoya**・架け替え） | 60 |
| 1.6 / 1.7 | Vessel Information / 機関と電気（電源・推進・制御・燃料・**3月25日の停泊中の停電**） | 77 / 80 |
| 1.13 / 1.14 | VDR とデータ回収 / **HR1 制御回路と緩んだ信号線の発見** | 108 / 110 |
| 1.16 | **外航船の衝突に対する橋の脆弱性**（AASHTO 指針・キー橋の脆弱性） | 131 |
| 2.2 | **配線ラベルのバンディングの不適切な取り付け** | 143 |
| 2.5 | 連絡（船内と陸上・**運転者への警報**・**作業員への連絡**） | 168 |
| 2.9 | 橋の脆弱性の評価 | 192 |
| 3 | Conclusions（Findings・**Probable Cause p202**） | 199 |
| 4 | Recommendations | 203 |

## 関連
- `ref/keybridge/SHOTS_INDEX.md` — 実写素材の台帳（②で実測）
- `ref/CREDITS.md` §キー橋 — 権利の台帳
