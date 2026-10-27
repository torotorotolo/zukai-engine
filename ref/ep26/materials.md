
# 26本目（タイタニック号沈没事故）素材の台帳 ── ②素材

**2026-10-27（26本目の2本目のチャット＝②③）で作った。** 網は「権利 → 大きさ → 撮影年 → 場面」の4段（ルール §2-18）。🔴 **在庫は素材ではない＝絵は 640px の見本帳（2列×3行）で見て、名乗りは置き場の説明の語と絵の両方で**（記憶 `feedback-inventory-is-not-usable-material`）。見た見本帳は `src/sheets/`（git の外）・見た枚は `src/seen_log.tsv`（md5 つき＝機械で数えた）。
資料＝[sources.md](sources.md)／尺＝[kousei.md](kousei.md)。撮影者・作者の個人名は公開のリポに書かない（フリー素材の作者は `src/agents/agentB_rights/` と ⑤b の `src/credits_private.tsv`）。

- 道具＝`probe/commons26.py`（`fetch`＝分類の中の点を説明・撮影日・権利つきで／`list`＝網／`pick`＝欄ごとに選ぶ／`thumbs`＝縮小版）・`probe/sheet26.py`（見本帳）・`probe/dup26.py`（同じ写真の別の版を特徴点で）・`probe/seen26.py`（見た枚の台帳）
- Commons の網：① の目録（深さ2・2,642点）＋人と船の分類を足して **50分類・1,151点**（`src/commons/c26_meta.json`）→ 題名の網（模型・展示・記念碑・後年の映画・切手ほか）と幅400未満を外して **917点**（`c26_list.tsv`）→ **1行ずつ読んで114点**を12の欄に（`pick26.tsv`）→ 縮小版（10-26 カズヤくん了承「落としてよい」・`src/commons/thumb/`）→ 見本帳19枚
- ⚠️ 縮小版は API が幅640を標準の **960px** に切り上げる＝1点約230KB（見込みの約10MB ではなく合計 約26MB）。**画像が960px より小さい点は原本の URL が返り、原本は数点で 429**（52点目で止まった）＝その点だけ画像より小さい標準の幅（500・330px）で頼み直した（記憶 `reference-commons-standard-thumbnail-sizes` のとおり）

---

## 0. 結論（見込み・⑤b で1点ずつ当て直す）
1. **この事故の写真・紙面は足りる**＝見本帳で ◎○ と見た別々の写真 約90点（同じ写真の別の版は1つに数えた・§1-13）＋紙面（英国の報告・MAIB・米国の法）約10頁 → 見込み **約70〜85カット（244カットの29〜35%）**＝下限20%（49カット）を越える。フリー素材（Pexels・「イメージ」）は別に約8〜12
2. 🔴 **オリンピック号との取り違え**＝撮影日と場所・出どころ・**船名**で決めた（S1-084 は船尾に「TITANIC／LIVERPOOL」・S1-002 は船首に名＝拡大版 S2-033 で読める）。✕ S1-036（沈没のあとの絵はがき＝S1-002 の着色）。横から写した S1-032（＝S1-069）・S1-050 は ⑤b で原寸（A 甲板の前半の窓）
3. 🔴 **置き場の説明が食い違う点がある**（同じ写真に「シェルブール」と「コーヴ」・「吊り上げたボート」と「12号艇」）＝控えめな語で名乗る（§1-13）。「衝突した氷山」を名乗る写真は5点以上＝どれかは決まらない（§1-6）
4. **動く映像**＝1912年の出来事の映像で使える物は無い（ゴーモンのニュース映画は会社が権利を主張・LOC は確認画面）＝【映像あり】なし。**NOAA 2004 の残骸の映像（courtesy）が唯一の使える動く実写**（§2・§4）
5. **芯（カリフォルニアン号）の物**＝船の写真 S8-625（NARA・3000px）と S8-E03（カルパチア号の乗客が撮ったとされる）・船長の写真（英国の審問の場 S3-675・1908年 S3-749）・🆕 **本物の遭難の無線電報**（S4-320＝ビルマ号が受けた「We are sinking fast」）・**米国海軍水路部の日報**（S4-228）・**カルパチア号の船長の手書きの報告**（S4-242）・MAIB の位置の図（Annex 3＝描き直す）
6. **人の顔**＝乗員・他船の船長と通信士・審問の長は顔を出せる（§1-3）。乗客・群衆は遠景か顔だけモザイク（PD のとき）。会社の人の名前が絵に入る点（S9-646・S4-264）は名前を隠す
7. **権利**＝見本帳の114点のうち PD 112・CC0 1・制限なし 1。NOAA は2003年の写真と2004年の映像（courtesy）だけ使える側・2004年の写真は National Geographic の著作権＝使わない

---

## 1. Commons（見本帳で見た・640px＝「何の絵か」まで）

### 1-1 S1 船の外観（1912-04-02 試運転〜04-11 クイーンズタウン）＝見本帳1〜4
🔴 **オリンピック号（姉妹船）との取り違え**：1911〜12年の見分けは A 甲板（ボートの1つ下の甲板）の**前半が窓でふさがっている**のがタイタニック号・オリンピック号は全長が開いている。**640px ではこの窓は見えない**＝撮影日と場所（説明・出どころ）と、船名が読めるかで決めた。横から写した点で出どころの弱い3点は ⑤b で原寸。

| 番号 | 何の絵か（見本帳） | 説明の語（撮影日・場所・出どころ） | 原寸 | 判定 |
|---|---|---|---|---|
| **S1-002** | 4本煙突の全身・右へ進む・波 | RMS Titanic departing Southampton on April 10, 1912（地元の写真家の有名な1枚と同じ構図＝撮影者の名は git の外） | 5000×3677 | ◎ 冒頭・サムネの地の候補 T1 |
| **S1-084** | 船尾から・**船尾に「TITANIC／LIVERPOOL」が読める**・船尾の手すりに人（小さい） | De Titanic tijdens haar laatste stop in Queenstown, 11 april 1912（オランダ国立公文書館 Spaarnestad） | 2835×2252 | ◎ **船名で確定**・「最後の港」・サムネの候補 T2 |
| S1-001 | 右斜め前から・港 | 「leaving Southampton」（独の週刊誌 1912年30号）・撮影日の札 1912-04-12 | 3402×2818 | ○ 🔁 **S1-016 と同じ写真**（特徴点の一致 107）＝4月10日のサウサンプトン。札の4月12日は雑誌の日 |
| S1-006 | 岸壁を埋める群衆と船腹 | departing from Southampton Pier 44 | 3000×2000 | △ 私人の顔が近い＝使うなら顔だけモザイク（PD） |
| S1-008 | 岸壁・タグボート・船首 | Titanic at the docks of Southampton（04-10） | 3000×1885 | ○ 🔁 S1-013 と同じ写真の見込み（§1-13） |
| S1-013 | 同じ構図（縦に広い） | RMS Titanic passenger liner in Southampton（1912） | 4000×3375 | ○ 🔁 |
| S1-016 | タグボートと出航 | The Titanic leaving Southampton（04-10） | 2732×1640 | ○ |
| S1-017 | 岸壁に着いた船・クレーン | Berthed at the port of Southampton（04-09） | 1977×1149 | ○ |
| S1-020 | 岸壁の船首（縦長） | Titanic earlier Southampton, April 1912（04-04） | 1462×2000 | ○ 縦長＝全面は上下を切る |
| S1-032 | 真横の全身・海 | 「seen in Cherbourg, France rather than Southampton」（撮影者＝クイーンズタウンで降りた乗客の神父＝私人＝名は書かない） | 1920×1327 | ○ 🔁 **S1-069（「Cobh Harbour」）と同じ写真**（一致 1001）＝**説明が港を食い違える**＝港は名乗らない（「1912年4月・航海の途中の港で」）。⚠️ ⑤b で原寸（A 甲板） |
| S1-036 | 着色の全身＋下に「WRECKED IN MID-ATLANTIC … Copyright」の焼き込み | オランダの写真庫「[Waarschijnlijk ingekleurde opname]」 | 3625×2411 | ✕ **沈没のあとの絵はがき**（字の焼き込み・オリンピック号の写真の流用の恐れ） |
| S1-042 | 試運転・タグボート・左下に「H1721 H.W.」 | Titanic leaving Belfast（04-02）・Harland & Wolff Collection（北アイルランド国立博物館） | 6000×4523 | ◎ 試運転（ベルファスト）・高解像度 |
| S1-050 | 真横の全身 | 「Titanic from the side」（nl.wikipedia からの移し・出どころ弱い） | 3200×1800 | ○ ⚠️ ⑤b で原寸 |
| S1-053 | 錨を下ろした船と小舟 | 「reaching its first stop-off」（04-10・シェルブールへ） | 3200×2396 | ○ |
| S1-057 | 甲板から見下ろしたタグボートと人々 | 同じ乗客の神父の写真（04-10） | 3000×2306 | ○ 人は小さい |
| S1-067 | ボート甲板を歩く人々（横長の切り出し） | Spaarnestad（04-11） | 3499×1476 | 🔁 S2-054 と同じ場面 |
| S1-069 | 真横・停泊 | RMS Titanic pictured in Cobh Harbour（Cobh Heritage Centre） | 2880×1990 | ○ |
| S1-076 | 真横・停泊 | Titanic arriving at Cobh, 11 April 1912 | 4088×2103 | ○ 🔁 S1-069 との重なりを §1-13 |
| S1-089 | 岸から見た試運転・タグボート | The Titanic beginning a day of sea trials（04-02） | 3200×2294 | ○ |

### 1-2 S2 船上（ボート甲板・船橋・無線室）＝見本帳4〜5
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| **S2-033** | 船橋・前のマスト・見張り台（クロウズネスト）・船首に「TITANIC」 | bridge and crow nest（04-10） | 1804×1746 | ◎ c4（見張り）。🔁 **S1-002 の一部を拡大した版**（一致 87）＝別の写真として数えない（同じ回で両方使うなら離して） |
| S2-045 | ボート甲板・救命ボートとダビット・歩く人（小） | Second Class promenade and boat deck（04-11） | 1280×887 | ○ c2・c7（ボート） |
| **S2-054** | ボート甲板・救命ボート・デッキチェア・人（小） | portside boat deck of Second Class promenade（04-11） | 4050×2583 | ◎ c2（ボート20隻）高解像度 |
| S2-070 | ダビットに吊ったボート・手すりの人（後ろ姿） | 左舷の前のボート・吊り下がるのは2号艇（ロシア語の説明） | 1155×900 | ○ c5（2号艇＝のちに最初に救われたボート） |
| S2-203 | 甲板から船首（セピア・低画質の複写） | 本の複写（04-03） | 1600×1200 | △ |
| S2-206 | 無線室・ヘッドホンの通信士の後ろ姿（二重露光） | 「The only picture of the Marconi radio room onboard the Titanic. Harold Bride is seated at the desk.」 | 1280×956 | ○ c3（無線室）。S2-E01（オリンピック号の無線室）とは**別の部屋の写真**（見本帳で確認・特徴点の一致なし）。名乗りは「タイタニック号の無線室とされる唯一の写真（1912年4月）」まで（座る人の名は説明の語＝⑤b で出どころ） |
| S2-213 | 同じ場面（二重露光を直した版） | 同上（2019年の本で二重露光を直した＝手が入った版） | 648×467 | △ 🔁 S2-206 と同じ（一致 61）・手直しの版＝使うなら S2-206 |
| S2-085 | 甲板の2人＝事務長と船長（制服） | Chief Purser … and Captain Edward Smith photographed on the boat deck, 11 April 1912 | 1667×1212 | ◎ 船長（乗員＝顔可）。事務長は乗員＝役職で |
| S2-724 | 船橋に立つ船長（セピア） | at the Titanic bridge on the morning of April 10th, 1912 | 2040×1453 | ○ |
| S2-E01 | 白い服の通信士・計器の並ぶ無線室（別の部屋） | 1912年の本が「the wireless radio room aboard the SS Olympic」とした写真 | 2734×1854 | △ 姉妹船の無線室＝使うなら「姉妹船オリンピック号の無線室」と名乗る |

### 1-3 S3 乗員と他船の船長・審問の長（公的な任務＝顔を出せる・ルール B2-1・B2-2）＝見本帳5〜8
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| **S3-714** | スミス船長の肖像（白い帽子・勲章） | NYT に載った（1912-04） | 1080×1451 | ◎ |
| S3-736 | 戸口の2人の航海士（二等・一等）と後ろの乗組員 | 2nd Officer Lightoller and 1st Officer Murdoch … at Queenstown, 11 April 1912 | 544×700 | ○ 小さい |
| S3-784 | 四等航海士の肖像（背広） | Register of Seamen（英国立公文書館の系列 BT348 ほか） | 426×573 | △ 小さい |
| **S3-352** | 通信士フィリップスの肖像（マルコーニ社の帽子） | Personal photo of Jack George Phillips | 1063×1376 | ◎ c3・c5 |
| **S3-775** | 包帯の足で運ばれる二人目の通信士（顔は下向き）・後ろに大勢 | LOC：Harold Bride … with feet bandaged, being carried up ramp of ship | 1536×1199 | ◎ c7（ニューヨーク着）。後ろの人々の顔は ⑤b で（私人なら顔だけモザイク） |
| S3-779 | 新聞の網点の2人（毛布） | Bride (left) and Cottam (right) | 1974×2690 | △ 低画質 |
| S3-781 | カルパチア号の通信士の顔（切り出し・小） | Carpathia's wireless operator | 592×395 | △ 小さい |
| **S3-675** | 山高帽の男性（新聞の網点） | **Captain Stanley Lord of the Californian attending the British inquiry … May 1912**（新聞） | 1906×1367 | ◎ **カリフォルニアン号の船長の1912年の唯一の写真**・c6・c8 |
| S3-749 | 甲板に立つ制服の船長（縦長・小） | Stanley Lord … as captain of the SS Louisianian in 1908 | 467×793 | ○ 小さい＝額装 |
| **S3-753** | ロストロン船長（はしごの前・制服） | while serving as master of the Cunard liner RMS Carpathia in 1912 | 2220×3656 | ◎ c7 |
| **S3-577** | カルパチア号の船長と航海士たち（銀杯）・ネガに「CAPT. ROSTRON & UNDER OFFICERS - "CARPATHIA"」 | LOC（Bain）ガラス乾板 | 5754×4191 | ◎ c7（1912年5月の表彰のころの見込み＝説明に日付なし） |
| **S3-810** | 見張りフリートの顔（近い） | British sailor and Titanic survivor Frederick Fleet | 2560×1881 | ◎ c4（「真正面に氷山」） |
| **S3-671** | シルクハットの2人が歩く | Lord Mersey and son … arrive at the British inquiry | 916×768 | ◎ c8（英国の審問の長） |
| **S3-698** | 椅子に座る議員・ネガに「SENATOR SMITH, MICH.」 | LOC（Bain）ガラス乾板 | 5766×4292 | ◎ c8（米国上院の小委員長） |
| **S3-424** | 4人の航海士の写真館の写真 | The four surviving officers（五等・二等・四等・三等） | 1486×1044 | ◎ c5〜c7 |
| S3-E02 | （見本帳18） | Californian's captain, Stanley Lord | 163×245 | ✕ 小さすぎる |

### 1-4 S9 審問の場 ＝見本帳8〜9
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| S9-645 | 上院の公聴会のスケッチ（新聞の絵・1912） | The Graphic（1912-05-11）＝会社の社長の証言の場面 | 1329×769 | ○ 絵（1912年の新聞） |
| S9-646 | 証人の似顔絵7つ（見張り・会社の副社長・四等航海士・議員・カルパチア号の通信士・二人目の通信士・五等航海士）＝**下に名前の焼き込み** | The Graphic（1912-05-11） | 1364×968 | △ **会社の人の名前が絵に入る**＝使うならその枠を切って外す |
| S9-648 | ウォルドーフ・アストリアの公聴会の部屋（大勢） | LOC：Senate Investigating Committee questioning individuals at the Waldorf Astoria | 1536×1209 | ○ 遠景（顔は小さい） |
| S9-666 | 公聴会（奥に帽子の女性たち） | Boxhall testifies … Senator William Alden Smith and［会社の社長］ | 960×540 | ○ ⚠️ 出どころ Reddit＝説明の人物の当ては未確認 |
| S9-667 | 公聴会 | Harold Cottam … testifies at the Waldorf Astoria（出どころ Reddit） | 960×716 | ○ ⚠️ 同上 |
| **S9-674** | 英国の審問の会場（ロンドンのスコットランド連隊の訓練ホール）・壁に大きなタイタニック号の模型・「COUNSEL」「RESERVED」の札・人なし | London Scottish Drill Hall, location for the British Titanic inquiry（審問の前） | 913×768 | ◎ c8（英国の審問） |
| S9-650 | 公聴会の部屋（大勢） | 二人目の通信士が証言する場面（1912-05-25・出どころ eBay） | 895×620 | ○ 遠景 ⚠️ 説明の人物の当ては未確認 |

### 1-5 S4 書類（無線の電報・覚書・新聞）＝見本帳9〜10
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| **S4-320** | **遭難の無線電報の用紙**（ロシア東アジア汽船会社「S.S. "Birma"」の Radio-Telegram・from Titanic・「about 1-40 a.m.」・「SOS SOS CQD CQD - MGY / We are sinking fast passengers being put into boats MGY」・右上に「M16307」の印） | Signal sent by Titanic's wireless operator … 15 April 1912（英国立公文書館 MT 9/920/C） | 500×402 | ◎ **c5 の決め所の物証**。⚠️ 小さい＝額装。⚠️ 権利＝Commons は PD・英国の未刊行の文書の扱いは ⑤b で英国立公文書館の頁の条件を読む |
| **S4-228** | 米国海軍水路部の日報（No. 1013・April 15, 1912）＝「COLLISION WITH ICEBERG - Apr 14 - Lat 41° 46', lon 50° 14', the British steamer TITANIC collided with an iceberg seriously damaging her bow」＋**「The German steamer AMERIKA reported by radio telegraph passing two large icebergs in lat 41° 27', lon 50° 08'.--TITANIC (Br ss)」**（赤の手書きの印） | NARA（naId 595107） | 2574×3300 | ◎ c3（アメリカ号の氷の通信をタイタニック号が中継した記録）・c5 |
| S4-313 | 同じ日報の黄ばんだ写し | Extract of US Navy memorandum | 600×768 | 🔁 S4-228 と同じ（一致 105）＝使わない |
| **S4-242** | カルパチア号の船長の手書きの報告（カルパチア号の便箋・「At 12.35 am (ships time) April 15th …」） | LOC（April 27, 1912） | 939×1536 | ◎ c7（船の時刻と書いている） |
| S4-300 | 新聞の網点「WIRELESS PLANTS ON THE ALERT FOR NEWS」＝ポイント・ジュディスの無線局の塔 | Providence Journal（1912-04-18） | 2436×2652 | ○ c3（陸の無線局） |
| **S4-254** | NYT 1912-04-15 の1面「NEW LINER TITANIC HITS AN ICEBERG; SINKING BY THE BOW AT MIDNIGHT; … LAST WIRELESS AT 12:27 A.M. BLURRED」（Commons で橙の枠が付いている） | The New York Times | 1021×1747 | ◎ c7（第一報）。枠は切る |
| **S4-264** | 英紙「"THE VESSEL UNSINKABLE."」（4月16日 p.9）＝会社の副社長が**事故のあと**（ニューヨーク・月曜）に「the vessel is unsinkable」と声明 | The Manchester Guardian | 1300×1400 | ○ c2（「沈まない」の出どころの1つ）。🔴 **本文に会社の人の名前**＝映すなら名前を隠す（ルール B2-1・① の人の扱い） |
| S4-304 | NY Tribune 1912-04-15 午前4:30 の号外の1面 | New-York Tribune | 2408×3637 | ○ c7 |
| S4-322 | NY Herald の1面「THE TITANIC SINKS WITH 1,800 ON BOARD; ONLY 675 …」＋乗客の顔写真の並び | LOC「Vc53.1」 | 470×640 | ✕ 乗客の顔と名・小さい |
| S4-702 | 本の表紙（赤い布）だけ | 上院議員の演説の本 | 1264×2150 | ✕ |

### 1-6 S5 氷山（1912年4月・現場の近く）＝見本帳11〜12
🔴 **「衝突した氷山」と名乗る写真が置き場に何枚もある**（撮った船が違う）＝どれが当たった氷山かは記録で決まらない。名乗りは「1912年4月、現場の近くで撮られた氷山（〜号の乗組員が撮った）」まで（記憶 `feedback-famous-cause-may-be-legend`）
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| **S5-359** | 遠くの平たい氷山・暗い海 | NARA「A Photograph of an Iceberg Floating Near the Site of the TITANIC Sinking.」 | 3000×2099 | ◎ 冒頭 c103・サムネの候補 T3（説明が控えめ） |
| S5-357 | 尖った氷山・根もとに黒い帯 | プリンツ・アダルベルト号の司厨長が4月15日朝に撮った（USCG の氷山監視の頁より） | 1308×740 | ○ 帰属つき |
| S5-358 | 平たい氷山 | ミニア号の船長が持っていた写真（同上） | 715×468 | ○ |
| S5-361 | 氷山 | 1912年の本 | 753×500 | ○ |
| S5-362 | 氷原と遠くの氷山＋下に「GIANT CAUSE OF THE DISASTER — … photographed near the scene of the wreck by a passenger on the rescue ship Carpathia」（Underwood & Underwood） | 1912年の本の頁 | 3801×2606 | ○ 本の主張ごと（「1912年の本はこう書いた」）か、字を外して |
| S5-364 | 黒っぽい三角の氷山 | ビルマ号から撮ったとされる | 960×626 | ○ |
| S5-365 | 白い氷山 | 4月20日・ブレーメン号の船員が撮った（2000年に見つかった） | 1455×765 | ○ |
| S5-363 | セピアの氷山＋手書き「Copyright」と「… on 12/04/12 … Titanic struck 14/04/12」 | 競売の品 | 1536×1256 | ✕ **衝突の前の日付・「Copyright」の書き込み** |

### 1-7 S6 救命ボート・救助（カルパチア号から・ニューヨーク）＝見本帳12〜14
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| **S6-480** | 海の上の2隻のボート（帆を張った1隻と、漕ぐ1隻）・人は遠い | BnF（Rol 通信社）「les rescapés (dans les canots sur la mer, le 15 avril 1912)」 | 8305×5994 | ◎ c7（4月15日の朝）・冒頭やサムネの候補。人は遠景 |
| **S6-379** | 夜のカルパチア号の舷側・タイタニック号のボート3隻が吊られている・手すりの人々（小） | Lifeboats … uploaded to the RMS Carpathia（1912-04-18＝ニューヨーク着の夜） | 2100×1058 | ◎ c7 |
| S6-383 | 縦長＝船腹の横のボートに人がぎっしり（上から） | Spaarnestad「reddingsboot … opgehesen aan … Carpathia」 | 2220×3936 | ○ 人は小さい・縦長 |
| S6-384 | 甲板に吊り上げたボート（縦長） | NARA「presumed to be a TITANIC lifeboat being hoisted to drain it of water」 | 2339×3000 | ○ 🔁 S6-561（「12号艇・15日朝」）と同じ写真（一致 354）＝**説明が割れる**＝NARA の控えめな語で |
| S6-427 | カルパチア号の甲板の生存者（後ろ姿）・ネガに「SURVIVORS OF "TITANIC" ON "CARPATHIA"」 | LOC（Bain） | 5754×4160 | ○ 顔は見えない |
| S6-619 | LOC の台紙に小さな2枚（ボートを積んだカルパチア号） | LOC | 4096×3278 | △ 台紙ごと＝切り出し |
| **S6-372** | 桟橋に並ぶ救命ボート13隻ほど | 1950年代の本の頁（1912年の写真） | 1627×1095 | ◎ c7・c8（ニューヨークに残ったボート） |
| **S6-377** | ピア54 の水面のボートの列・その上に立つ男たち | Titanic's Lifeboats at The White Star Lines Pier 54 in NYC（1912-04） | 2150×1500 | ◎ |
| **S6-374** | 漕ぐボートの横に、ひっくり返った折りたたみ艇 | The Boat B … found by the Mackay-Bennett（1912） | 2000×1532 | ◎ c7（折りたたみ艇 B）。⚠️ マッケイ・ベネット号は遺体の回収の船＝語りは船の名だけに |
| S6-376 | 新聞の網点＝カルパチア号の甲板のボートと人 | Times Dispatch（4月21日） | 3483×2187 | △ 低画質 |
| S6-378 | 浸水した折りたたみ艇と2人の水夫（上から） | 「1912-05-13 オセアニック号が見つけた折りたたみ艇 A・中に遺体3人」 | 1472×1058 | ✕ 640px で遺体は見えないが、遺体の回収の場面＝使わない（ルール B2-2） |

### 1-8 S7 カルパチア号のニューヨーク着・群衆 ＝見本帳14〜15
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| **S7-594** | ピアに着いたカルパチア号（船首に「CARPATHIA」・錨・タグボート） | BnF「Carpathia à New-York (20 avril 1912)」 | 8305×5994 | ◎ c7 |
| S7-598 | タグボートに押されて港に入るカルパチア号（ネガに「"CARPATHIA"」） | LOC（Bain）1912-04-19 | 1536×1026 | ◎ 🔁 S7-615 と同じ（一致 1316） |
| S7-599 | 横向き・タグボート4隻 | LOC | 1536×895 | ○ |
| S7-463 | ピア54 のカルパチア号（縦長） | LOC | 979×1472 | ○ |
| S7-112・S7-126 | ホワイト・スター・ライン社の事務所の前の人々・騎馬警官 | LOC（Bain） | 5735×4222・5741×4091 | △ 私人の顔が中くらい＝使うなら顔だけモザイク（PD） |
| S7-462 | 夜の群衆（ピアの門の前・「CROWD AWAITING SURVIVORS FROM "TITANIC"」） | LOC | 1473×1052 | △ 同上 |

### 1-9 S8 カリフォルニアン号・ほかの船 ＝見本帳15〜16・19
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| **S8-625** | 海上のカリフォルニアン号（煙突1本・マスト4本） | NARA（naId 278339）「A photograph of the CALIFORNIAN which may have been taken from the deck of the CARPATHIA.」 | 3000×2096 | ◎ **この回の核の写真**＝冒頭 c102・c6・サムネの候補 T2。名乗りは NARA の語（「カルパチア号の甲板から撮られたとみられる」） |
| S8-624 | 同じ写真 | 「1912-04-15」（maritimequest） | 1200×838 | 🔁 S8-625 と同じ（一致 857） |
| **S8-E03** | 手前に綱とボートのダビット・その向こうにカリフォルニアン号（別の写真） | 「S.S. Californian photographed by passenger aboard R.M.S. Carpathia, April 15th 1912」（出どころ Reddit） | 977×589 | ○ c7（朝・カルパチア号から）。⚠️ 出どころが弱い＝名乗りは「カルパチア号の乗客が撮ったとされる」 |
| S8-630 | 港のカリフォルニアン号とタグボート | The Leyland liner Californian in port（1907-05-10） | 1475×716 | ○ 「1907年のカリフォルニアン号」 |
| S8-631 | 座礁したマウント・テンプル号（1907年の絵はがき） | 1907年の座礁 | 932×585 | △ 別の出来事の写真＝使うなら年を断る |
| S8-629 | 油絵（波と旗） | 競売の品「The SS Californian en route to America」（20世紀） | 5678×2880 | ✕ 絵画・年不明 |
| S8-634 | 着色の絵はがき「HANDS ACROSS THE SEA」（ヴァージニアン号） | — | 800×504 | ✕ |

### 1-10 S10 図面・地図 ＝見本帳16〜18
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| **S10-871** | 1912年の本の図＝タイタニック号の横の区画（1〜6）と「LENGTH OF RENT IN SIDE PLATING」・ボイラーの配置（モーリタニア号と比べる） | 『An Unsinkable Titanic』（1912）p.129 | 3170×1970 | ◎ c4（前の5区画）。⚠️ 「裂け目の長さ」の札は1912年の本の見立て＝NIST は裂け目でなく継ぎ目の開き（legend §3-2） |
| **S10-905** | 1912年の新聞の地図＝ニューファンドランド・タイタニック号・カルパチア号・ヴァージニアン号・パリジャン号・バルティック号・オリンピック号・「FIELD ICE LIMIT IN APRIL」「LIMIT OF ICEBERGS IN APRIL」 | Spaarnestad（1912） | 3508×2540 | ◎ c5・c7（当時の見立ての地図＝船の位置は1912年の報道の推し量り） |
| S10-833 | 船の真ん中の断面図（白い線画） | White Star Line の宣伝物（1911〜12） | 1401×2088 | ○ c2 |
| S10-852 | 船の切断図（1912年の挿絵） | Spaarnestad | 3190×3535 | ○ |
| S10-163 | カナード社の大西洋の海図の写真（手書きの書き込み・署名） | 「Nautical chart of RMS Carpathia, 1912.04.15」（ハンガリーの資料） | 1026×684 | △ 何の線か未確認（⑤b） |
| S10-275・S10-866 | ボート甲板の平面図に色を足した版／横からの図に札を足した版 | Commons の利用者の手直し | 3000×693・3735×1180 | △ 元の1911〜12年の図（手直しなし）を ⑤b で（分類 `Titanic plans and diagrams` の「Olympic and Titanic Side Plan 1911」ほか） |
| S10-872 | 別の船（インペラトール号）の図 | — | — | ✕ |
| S10-880 | 地球儀のアプリの画面写し（座標の札） | — | 977×606 | ✕ |
| S10-829 | 舵と号令の模式図（CC0・小さい） | 2011年の作図 | 417×413 | ✕（自分で描く） |

### 1-11 S11 残骸 ＝見本帳18
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| **S11-910** | 垂れ下がるラスティクル（鉄を食べる微生物のつらら） | NOAA 2003（［撮影者］・courtesy） | 3000×2250 | ◎ c9（残骸）・冒頭 |
| **S11-716** | 船長の浴室の浴槽とラスティクル | NOAA 2003（同上）＝Commons の札「2004-06」は誤り | 2250×2250 | ◎ c9 |
| S11-911 | 船首と手すり（海底） | 「2004年6月・ROV Hercules」 | 1480×1036 | ✕ **NOAA の頁で「Image copyright ［撮影者］/National Geographic」**の3点のどれかの見込み |

### 1-12 S12 その後・1912年の反響 ＝見本帳18〜19
| 番号 | 何の絵か | 説明の語 | 原寸 | 判定 |
|---|---|---|---|---|
| S12-913 | 机を囲む7人（1923年の国際氷山監視の委員会） | LOC（Bain） | 6054×4380 | ○ ca（公的な任務の人） |
| S12-471 | 1912年の風刺画（氷山の上の骸骨・沈む船・海の中の人） | Puck「Luxuries versus lifeboats」 | 5239×7805 | ✕ 海の中の人を描く |
| S12-493 | 1912年の風刺画（乗客名簿を読む死神）＋色票 | LOC | 925×1024 | △ 暗すぎる（使うなら色票を切る） |
| S12-483 | 1912年の風刺画（「PUBLIC SERVICE」の机） | Library and Archives Canada は自由利用を認めていない | 597×485 | ✕ |

### 1-13 同じ写真の別の版（特徴点 ORB＋RANSAC・`src/commons/dup26.tsv`・一致25以上＝11組）
| 一致 | 組 | 扱い |
|---:|---|---|
| 1316 | S7-598 ＝ S7-615 | 同じ（LOC の2つの登録） |
| 1001 | S1-032 ＝ S1-069 | 🔴 **港の説明が食い違う**（シェルブール／コーヴ） |
| 857 | S8-624 ＝ S8-625 | 同じ（NARA の語で名乗る） |
| 528 | S1-008 ＝ S1-013 | 同じ |
| 354 | S6-384 ＝ S6-561 | 🔴 説明が割れる（吊り上げたボート／12号艇） |
| 253 | S1-067 ＝ S2-054 | 同じ場面（切り出し） |
| 122 | S1-002 ＝ S1-036 | 絵はがき（✕）は S1-002 の着色 |
| 107 | S1-001 ＝ S1-016 | 同じ（4月10日） |
| 105 | S4-228 ＝ S4-313 | 同じ書類 |
| 87 | S1-002 ＝ S2-033 | S2-033 は S1-002 の拡大 |
| 61 | S2-206 ＝ S2-213 | 同じ（手直しの版） |
- ⚠️ 縮小版（960px・小さい点は330〜500px）どうしの照合。⑤b で原寸を落としたら、使う点どうしでもう一度（記憶 `feedback-duplicate-art-needs-pixel-comparison`）

---

## 2. NOAA（残骸の写真と映像・係B が頁の文字で点ごとに＝画像は開いていない）
- 方針（N2）＝"If the image caption includes the word “copyright,” additional permissions are required for use."・"we ask that you include the credit information included in the caption"
- 🔴 **旧 URL は 404＝保管のサブドメイン `archive.oceanexplorer.noaa.gov` へ移った**

| 年 | 点 | クレジットの原文 | 判定 |
|---|---|---|---|
| 2003 | 船首（ミール1号の外付けカメラ） https://archive.oceanexplorer.noaa.gov/explorations/03titanic/media/titanicbow.html | "Image courtesy of NOAA and the Russian Academy of Sciences." | ○ courtesy（copyright の語なし）。⚠️ 提供元に NOAA の外が入る |
| 2003 | 船長の浴室の浴槽とラスティクル https://archive.oceanexplorer.noaa.gov/explorations/03titanic/media/titanic_bathtub.html （＝Commons S11-716） | "Image courtesy of ［撮影者］, RMS Titanic Expedition 2003, NOAA-OE."（撮影者の名は git の外） | ○ 同上（Commons の撮影日の札「2004-06」は誤り＝NOAA は2003） |
| 2003 | 船尾のラスティクル・錨の下（3点）（＝Commons S11-910） | 同上の courtesy | ○ |
| 2003 | スライド21点（多くは人・船・潜水艇。残骸は窓枠・浴槽・ラスティクル） | "Image courtesy of the RMS Titanic Team Expedition 2003, ROI, IFE, NOAA-OE." | ○（人の写る点は使わない） |
| 2004 | 船首と手すり・船首・船橋の操舵機（3点） https://archive.oceanexplorer.noaa.gov/explorations/04titanic/media/titanic_bow.html ほか | 🔴 **"Image copyright ［撮影者］/National Geographic."** | ✕ 追加の許可が要る。**Commons S11-911（2004年6月の船首）はこの3点のどれかの見込み＝使わない** |
| 2004 | スライド33点 | "Image courtesy of ［撮影者］ © National Geographic Society" ほか（全点 ©） | ✕ |
| **2004** | **映像** https://archive.oceanexplorer.noaa.gov/explorations/04titanic/media/movies/titanic2004_video.html （mp4 32.3MB と表示）・新サイト https://oceanexplorer.noaa.gov/multimedia/video-playlist-best-titanic/ （41.2MB） | **"Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE."**（copyright・© なし） | ◎ **この題材で唯一の、使える側の動く実写**＝冒頭 c105・c9。⚠️ 中身（どの場面か・字の焼き込み）は取ってから見る（公的な機関＝許可不要）。⚠️ 「portal の映像は PD」の一文がこの映像に当たるかは頁に書いていない |
- 「NOAA/IFE/URI」の綴りは NOAA の読めた頁に無い・ROI の正式名も無い

## 3. 米国立公文書館（NARA・目録の JSON）
| naId | 題 | 日付 | 判定 |
|---|---|---|---|
| 278339 | A photograph of the CALIFORNIAN which may have been taken from the deck of the CARPATHIA. | 1912-05-14（目録） | ◎ Unrestricted（大きい版は Commons S8-625） |
| 278334 | A Photograph of an Iceberg Floating Near the Site of the TITANIC Sinking. | 1912-12-14（目録） | ○（Commons S5-359） |
| 278337・278338 | Photograph of a Lifeboat Carrying Titanic Survivors（注記＝6号・14号から移った［乗客］） | 1912-04-15 | ○ 私人＝遠景 |
| 278335・278331・278332 | 救命ボートの生存者／水を抜くために吊り上げるボート（presumed）／タイタニック号に似た船の甲板（uncaptioned） | 1912 | ○・○・✕（別の船） |
| 5729534 | Routes and Ice Flows Chart | 1912 | ○ 図（物は小さい＝0.0MB） |
| 5722336 | Deck Views of RMS Titanic | 1912 | ○ 図 |
| 595107 | Daily Memorandum from the Hydrographic Office Reporting Titanic Disaster | 1912-04-15 | ○ 書類（Commons S4-228） |
- RG21 の Admiralty Case Files（1912〜1916 の責任の制限の裁判・ボートの中身の目録ほか）は大きい（数十〜数百MB）＝要るときだけ
- 氷山監視の写真（RG26）は1938〜1965年＝1912年の絵ではない

## 4. 動く映像
| 置き場 | 中身 | 権利 | 判定 |
|---|---|---|---|
| Commons「Titanic Disaster - Genuine Footage (1911-1912)」（480×360・401秒）と補正版（622×480） | ゴーモンのニュース映画（説明「This Gaumont newsreel contains the only known footage of the Titanic. Pathé has joint rights in this film」・出どころ＝British Pathé の YouTube） | Commons は PD と書くが、**会社（British Pathé）が権利を主張**・YouTube の申し立ての恐れ・画質も 480×360 | ✕ 推奨＝使わない（使うなら映像方針でカズヤくんに） |
| British Pathé | 「TITANIC DISASTER - GENUINE FOOTAGE」ほか（係B＝検索エンジンの要約・頁は 403） | 有料のライセンスの見込み（原文未確認） | ✕ |
| archive.org | 1912年のニュース映画の写し（PeriscopeFilm）＝CC BY-NC-ND 4.0／1912年の劇映画 | 収益化した動画は NC に当たる | ✕ |
| 米国議会図書館（LOC） | 1910年代の映像の目録 | — | ⏳ **確認画面＝カズヤくんが内蔵ブラウザで通す段取り**（10-27 了承）。通れば目録を読んで候補を出す（落とす前に聞く） |
| NOAA 2004 | 残骸の映像（§2） | courtesy | ◎ |
- 🔴 **【映像あり】はいまは付けない**（1912年の出来事の動く記録で使える物が無い）。NOAA の残骸の映像を【映像あり】に数えるかは映像方針でカズヤくんに（ルール §6-38・Claude の推奨＝数えない＝出来事の記録ではない）

## 5. フリー素材（Pexels・係B が頁の中のデータで＝絵は見ていない）
- 許諾＝Pexels License（ヘルプセンターの原文＝YouTube は自分の動画の一部としてなら可・クレジット不要・写る人を悪く見せない）。⚠️ pexels.com/license は 403＝ヘルプセンターで読んだ
- 🔴 **当夜は月が無かった**（英国の報告 p.40「There was no moon」）＝**月の写る夜の海は使わない**
- 候補（作者の名前は git の外）：氷山の写真 5点（16623269「Icebergs in the Ocean under a Dark Sky」6214×4143・5317286・17571884・33614408・26796269）＝どれも昼か曇り／夜の海の映像 3点（4938208「The Sea During the Night」4K 13秒・10589476「Seascape at Night」4K 11秒・11287848「Water with Waves」4K 30秒）。✕＝7513671（説明に「3D render」＝CG）・月の写る 32924946・39293076・32597068
- 信号弾・信号灯・夜の甲板・氷山の映像は Pexels が 403 で探せていない＝⑤b
- 落とす前に一覧でカズヤくんの了承（ルール §2-5c）。画面に「イメージ」・20% に数えない

## 6. 冒頭（c101〜c107・約63秒）の候補と秒（kousei.md §4 と対・ルール＝冒頭は実写）
| カット | 秒（累計） | 画（候補） | 大きさ・動き |
|---|---:|---|---|
| c101 | 0〜9 | S1-002 出航するタイタニック号（1912-04-10） | 5000px・全面のゆっくり寄り |
| c102 | 9〜18 | S8-625 カリフォルニアン号（NARA） | 3000px・全面のゆっくり寄り |
| c103 | 18〜27 | S5-359 現場の近くの氷山（NARA） | 3000px・全面 |
| c104 | 27〜36 | S6-480 朝の海のボート（BnF・人は遠景）＝語りで p.60 の「救えたかもしれない」 | 8305px・全面（決め所の画面は作らない＝語りで言う） |
| c105 | 36〜45 | NOAA 2004 の残骸の映像（courtesy）＝「80年後」 | 映像（中身は ⑤b で見て区間を決める） |
| c106 | 45〜54 | S8-E03 カルパチア号の甲板から見たカリフォルニアン号＝「見えていた／たぶん見えていなかった」 | 977px＝小さい＝全面だと約2倍の引き伸ばし（ぼけを受け入れるか額装かは映像方針で）。代わり＝S11-910（3000px） |
| c107 | 54〜63 | 夜の海（Pexels・月の無いもの・「イメージ」）＋この動画の問い | 4K 映像 |
- 🔴 冒頭に再現イラスト・図を置かない（記憶 `feedback-jiko-opening-flashy-but-faithful`）。額装の写真は動かさない（記憶 `feedback-jiko-framed-photo-no-shake`）・全面の写真のゆっくり寄りはこのままでよいかを映像方針で一言
- 🔴 引き（1912年の結論→1992年に割れた）は c104〜c105＝27〜45秒＝46秒より前

## 7. サムネの写真の候補（3点・実在の顔と犠牲の数を並べない＝ルール B5-4）
| 候補 | 写真 | 210px で | 注 |
|---|---|---|---|
| **T1** | S1-002 出航するタイタニック号（5000px・顔なし） | 4本の煙突の形で一目で分かる | 定番の構図（競合と似る） |
| **T2** | S8-625 カリフォルニアン号（3000px・顔なし） | ただの汽船に見える＝赤の1行で「もう1隻」を言わせる | 🔴 この回だけの核心（ほかの回に無い船）。T1 と左右に並べる案は ④ で |
| T3 | S5-359 現場の近くの氷山（3000px） | 平たい白＝弱い | 代わり＝S6-480（朝の海のボート・人は遠い）。⚠️ ボートの人と犠牲の数を並べない |
- 黄＝「タイタニック号の真相」・赤＝「犠牲1490人＋この回だけの核心」（「死亡」不可・言い切らない＝「救えた？」のような問いの形か帰属つき）＝④（記憶 `feedback-jiko-thumbnail-rival-format`）

## 8. 案C（再現イラスト）で描ける場面と記録の頁（ルール §5b-73〜75・部品ごとに rec=）
| 場面 | 描く物・動作・時刻（記録にあるものだけ） | 記録 | 守り |
|---|---|---|---|
| ① カリフォルニアン号の船橋（0時すぎ〜2時ごろ・カリフォルニアン号の時計） | 当直の二等航海士と見習い・遠くの船の灯（マストの灯と赤い舷灯）・**白い火箭が低く**（「マストの灯の半分くらいの高さ」）・双眼鏡・モールス灯で呼ぶ（答えなし）・伝声管で海図室へ（1:10ごろ）・見習いが階段を下りる（2:05） | 英 p.57〜59・Q7814・Q7832〜7840・Q7921・Q7565 | 🔴 遠くの船を**タイタニック号と名乗らない・形を描き分けない**（未決＝§5b-74③）。火箭の数は「約8」の札（数えられる形で描くなら8＝p.54・p.60） |
| ② 海図室（同じころ） | 船長が横になっている（服のまま）・戸が開いて閉まる | 英 p.59・Q6859・Q7288（「half awake」） | 顔の無い影。眠りの状態は描かない（記録は「覚えていない」） |
| ③ カリフォルニアン号の無線室（23:30〜） | 通信士が寝台で眠る・机の上のヘッドホン・0:15〜0:20 に三等航海士がヘッドホンを耳に当てる（何も聞こえない） | 英 p.57・Q8927・Q8285〜8289 | 無線の文字（モールス）を絵に書かない |
| ④ タイタニック号のボート甲板（0:45ごろ〜1:45ごろ・タイタニック号の時計） | 1号艇のそばの発射筒から火箭・白い星が散る・四等航海士がモールス灯で前方左の灯を呼ぶ（5〜6マイル・答えなし） | 英 p.54・Q15395〜15410 | 乗客は顔の無い群れまで・1人を抜き出さない（§5b-74②） |
| ⑤ 1号艇 | 40人乗りの席を40の**席の印**で描き、乗ったのは12（残り28は空席）＝人の形で数を名乗らない | 英 p.51〜52 | 人の形のアイコンで人数を出さない（§5b-74②・§C-1 #59） |
| ⑥ カルパチア号（4:10・カルパチア号の時計） | 夜明け・まわりに氷山・2号艇（緑の灯）を横に着ける | 英 p.55・米 Rostron01 | ボートの中の人は顔の無い群れ・数を出さない |
- 🔴 **描かない**＝2隻が互いに見えたか（未決）・沈む瞬間・海の中の人・船が折れる瞬間（1912年の報告は「折れていない」・のちに NIST と NOAA が「海面で2つに」＝時と所は未決）
- 案C の場所（置き場）は ①〜③ がカリフォルニアン号の船内、④⑤ がタイタニック号のボート甲板、⑥ が朝の海＝映像方針で場面数と秒を決める

## 9. 地図（25本目からの既定＝Google の衛星写真＋描き足し）
- 🔴 **作り方は映像方針でカズヤくんに2択（推奨つき）**（記憶 `reference-google-maps-satellite-capture`）。この回の事情：①航路（サウサンプトン→シェルブール→クイーンズタウン→ニューヨーク）は衛星写真に陸が写る＝衛星写真で足りる ②**事故の海域（北緯41〜42°・西経49〜50°）は衛星写真では一面の海**＝位置はすべて描き足し（点・線・札）になる
- 位置の数（sources.md §2-1）＝衝突の推定 41°47′N 49°55′W／沈んだ位置 41°43′.6N 49°56′.9W／1912年の位置 41°46′N 50°14′W（約13マイルのずれ）／カリフォルニアン号＝船長の位置 42°05′N 50°07′W・調査官 41°50′N 50°07′W（たぶんもっと東で5〜7マイル）・次長 42°00′N 50°09′W（約18マイル）／カルパチア号＝58マイル・N52W
- **MAIB の Annex 3（位置の図・見た11枚目）**は配置の正本として使い、図そのものは描き直す（Crown copyright の扱いが未確定＝数だけを使う）。図にある札＝船長の停止位置（2221）・次長の位置(1)・調査官の位置(2)(3)・「Possible position of vessel seen by CALIFORNIAN」・推定の衝突位置・残骸（1985）・SOS の位置・カルパチア号の出発の推測位置と線・5／10／15マイルの弧・北極星の緯度（1930）・アンティリアン号への位置（1830）
- 🔴 地図の上で「見えた／見えなかった」を線で描かない（未決）。2人の見方は**別々の点**で並べ、どちらにも帰属の札

## 10. 紙面（報告書の頁）
| 頁 | 使い道 | 権利 |
|---|---|---|
| 英国の報告 S. Doc. 933 p.60（「might have saved many if not all of the lives」）・p.85（問24(b)）・p.5（1,490）・p.54（火箭） | c1・c5・c8 | PD（米国の公文書） |
| MAIB 1992 送り状（首席が次長を支持）・p.3（結論の要約）・p.18（「different outcome」と「should have been made」）・p.19（「no villains」） | c9 | 引用の型（OGL／Crown copyright 未確定＝額装・無加工・必要最小限） |
| 米国の法 37 Stat. 199 の条文 | ca | PD |
- ⚠️ MAIB は 2000×2816 の白黒2値（1ビット）のスキャン＝全面に置かず額装（ルール §2-25）

## 11. 映像方針で足したこと（2026-10-27・26本目のチャット5）
正本＝[eizou_list26.md](eizou_list26.md)（生成物・235カット・門番 E 0）＝入力 `eizou_build/assign26.psv`（当て方）・`eizou_build/sources26.psv`（出どころ）→ `eizou_build/make_list26.py`。取得＝`eizou_build/fetch26.py`（記録 `eizou_build/fetch26.tsv`）・見た枚＝`eizou_build/seen26e.tsv`。
- ✅ **了承②（10-27 カズヤくん・4問とも推奨どおり）**＝取る素材（Commons 70点＝🆕6点を含む・Pexels 8カットは ⑤b で1本ずつ）・地図は衛星写真＋描き足し（外洋も）・見せ方（全面が既定・縦長と紙面と MAIB の頁は額装＝静止・全面のゆっくり寄る／流すは続ける）と人の写り・クレジット／案C の形のもと（🆕案C-9）／NOAA の映像は【映像あり】に数えない／LOC の映像の目録は見ない
- ✅ **NOAA 2004 の映像を取得**（公的な機関＝許可不要）＝`src/eizou/N04-video.mp4`（https://archive.oceanexplorer.noaa.gov/explorations/04titanic/media/movies/titanic2004_640.mp4・33,946,045 bytes＝HEAD と一致・md5 `d13757669b5ef044aadf0b0969a9d480` を2回）＝640×426・30fps・5分53秒・音声つき（音は使わない）。**16コマを原寸で見た**（`src/look_eizou/n04a〜d.png`）＝全編が海の底の残骸・字の焼き込みも人も無い・0〜9.5秒と346秒〜は黒。場面＝船首の手すり（10〜52秒）・船首の横（52〜67秒）・舷側の手すり（67〜88秒）・甲板の縁（88〜95秒）・前甲板の巻き上げ機と錨の鎖（95〜139秒）・甲板（139〜147秒）・浴槽（147〜161秒）・船室の窓（161〜183秒）・甲板の構造物（183〜249秒）・明るい甲板（249〜269秒）・暗い構造物（269〜346秒）＝13区間に割った（一覧 §0）。場面の切れ目は溶け合う転換が多く、ffmpeg の scene では1か所しか出ない＝小さな灰色のコマの差で割った（scratchpad の道具）
- 🆕 **足した Commons の6点**（目録の文字で選んだ・絵は取ってから原寸で）＝S8-N01 バルティック号（1904年・Harland & Wolff Collection・3800px）・S8-N02 メサバ号（1898〜1909年ごろ・英国国立海事博物館 G967・1265px）・S8-N03 海上のカルパチア号（撮影年不明・出どころ americanhistory.si.edu・3241px）・S8-N04 マウント・テンプル号（1900年代はじめ・1673×491）・S8-N05 ニューヨークのホワイト・スター・ラインの桟橋（1905年ごろの絵はがき・3294px）・S4-N06 アメリカ号の氷の電報（Commons の説明「Telegram from SS Amerika via SS Titanic…」・出どころ表記「Inquiry into the sinking of the SS Titanic 1912」・3300px）
- 🆕 **ほかの候補（目録で見つけた・今回は使わない＝控え）**＝AMERIKA（LOC Bain・1910・5735px＝公的な機関）・カルパチア号の通信士の新聞の写真（NYT 1912-04-20・2238px）・海上のバルティック号（LOC 1914）・Fortepan のカルパチア号（1903＝⚠️ Fortepan は CC BY-SA のことが多い）・ピア54 の写真（Cunard pier awaiting Carpathia 1912）
- ✕ **使わないと決めた点**＝一覧 §5 の NG（S6-384 を足した＝カルパチア号に吊り上げたボートは語りの「下ろす」場面に合わない／S1-050 を足した＝下の取得の節）
- ✅ **取得（了承②のあと・10-27）**＝`eizou_build/fetch26.py fetch`＝Commons **70点・失敗0**（原本の幅3840超→3840px・1920超→1920px の標準の縮小版／それ以下は原本＝sha1 も一致）・md5 を2回取って全点一致・合計 59.6MB・`src/eizou/`（git の外）。途中で 429 が3回＝道具が120〜360秒待って取り直した（間は10秒）
- ✅ **原寸で確かめた字**（見た画像は `eizou_build/seen26e.tsv`・英語の OCR は入っていない＝日本語の OCR では英字が崩れる→目で読んだ）＝S4-264 見出し「THE VESSEL UNSINKABLE.」（本文の頭の行 y286〜 に会社の人の名前＝切り出しの外）・S4-242「At 12.35 a.m. (ship's time) April 15th (Monday), 1912」・S4-320「We are sinking fast passengers being put into boats」・S4-254「NEW YORK, MONDAY, APRIL 15, 1912」・S1-084 船尾の「TITANIC」「LIVERPOOL」・S3-698 のネガの字は上の帯・S4-228「COLLISION WITH ICEBERG…」と「…AMERIKA…--TITANIC (Br ss).」が同じ頁に並ぶ・🆕 S4-N06 は本物の受信の用紙（S S Amerika via S S Titanic and Cape Race…／水路部の受付印 APR 15 1912）
- ✕ **S1-050**（真横の全身・nl.wikipedia からの移し）＝1920px の版で A 甲板の前半の窓を見たが、オリンピック号と見分けきれない＝使わない（ファイルは `src/eizou/_使わない/` へ移した＝消していない）。S1-032 は撮影者がタイタニック号の乗客という来歴で使う
