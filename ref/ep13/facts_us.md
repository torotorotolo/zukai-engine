# 照合結果 B（米国側：AA96便・紳士協定・SB・AD）

- 照合日：2026-09-23／照合者：サブエージェント（テキストだけで照合。画像・Web は使っていない）
- 仕事の向き：裏づけではなく「まちがい探し」。資料に無いものは「？資料に無い」と書き、推測には「推測」と付けた
- **頁の書き方**：上院資料は「senate p.N（印字 M）」。本文の PDF p.13〜58 は **印字＝N−12**（例：p.30＝印字18）。前付けは p.7＝(iii)、p.9＝(v)、p.11＝(vii)
- 読んだ範囲
  - `senate_cprt93_dc10.txt`：文字のある p.5〜58 を**全文通読**（p.1〜4・59〜62 は文字なし）
  - `faa_Windsor-LocksReportAAR73-02.txt`：`ntsb_AAR73-02_N103AA_erau.txt` と **md5 が同一**（同じファイル）。付録A・C・D・G と表紙を確認。付録B（乗員）の頁は文字が無い
  - `ntsb_AAR73-02_N103AA.ocr.txt`：付録B（乗員情報）だけ確認（崩れが多い）
  - `faa_ll_TC-JAV.txt`：改行なし1行のため 200字で折り返して全文確認（FAA 自身のまとめ＝二次資料）
  - AD 74-08-04・74-12-07・75-15-05：全文。官報 `fr_1974-04-02_11992.txt`：DC-10 の該当部（p.1〜2）
  - SB 52-37・52-38：要部。**SB 52-27・SBA 52-35 は文字の層が無く読めない**（中身は上院資料と AD から）
  - 覚書（1992）・AC 25.783-1（1986）：語で当たっただけ（B の主張に関わる記述なし）
  - 補足で1回だけ：`aib_8-76_TC-JAV.ocr.txt`（仏報告の英訳）で「SB 52-37／52-38」の語を当たった

---

## 結論の一覧

| # | 判定 | 一言 |
|---|---|---|
| B1 | ⚠️（細部のみ） | 本筋は一致。「ウィンザー**上空**」は資料では "near Windsor"（付近）。便は LA 発 NY 行き（デトロイト・バッファロー経由）の1区間。搭乗67人・軽傷11人・死者0。機長名は **「Bryce・52歳」までしか読めない**（姓は判読不能） |
| B2 | ✅ | 一致。膝で押し込み→ハンドルは収まる→通気扉は斜め→整備士が出発を承認→警告灯は消えたまま |
| B3 | ⚠️ | 番号・中身は一致（A-72-97／98、1972-07-06 発出・06-23 採択）。②は「**床に穴**」ではなく「**客室と後部貨物室の間**に圧力逃がし口」。勧告は2件だけ（「等」は無い） |
| B4 | ⚠️ | 電話・1972-06-15・シェイファー→マクゴーエンは一致。ただし「gentlemen's agreement」は**バスナイト証言の又聞き**で、マクゴーエン本人は呼び名を留保。また FAA は**非公開の電報で航空会社に要請**しており「メーカー任せの完全な自主」ではない |
| B5 | ✅ | 西部地域局が AD を「準備していた」＋3者の暫定合意あり。ただし「案が書き上がっていた」は FAA まとめ（二次）だけの表現 |
| B6 | ❌ | **SB 52-37 に「のぞき窓」は含まれない**（のぞき窓は A52-35）。A52-35 の日付が資料間で食い違う（6月16日／6月19日） |
| B7 | ⚠️ | 本筋は一致。**印は2人**（品質保証の検査員1人＋製造の副職長1人）で「検査員が複数」ではない。**印の日付は資料に無い** |
| B8 | ⚠️ | 電報 3月7日・3月22日、官報 4月2日は一致。「SB 7本」は1974年4月版で一致（最終版は8本）。AD 74-12-07 は「換気口のドア」ではなく**SB 5本**（うち1本が貨物ドアの通気扉） |
| B9 | ⚠️ | 題名・委員会・委員長・日付は一致。**S. Prt. 番号は読めない**（？） |
| B10 | ？資料に無い | Convair・Applegate・FMEA・1969 は上院資料に**無い**（フォルダ内の全テキストでも0件） |
| B11 | ？資料に無い | 1974年3月時点の「未改修機の総数」は無い。個別の数字だけある（下表） |

別表1（FAA まとめの誤り）に ❌ が4件あります。台本で FAA まとめを使う箇所は要注意。

---

## B1. アメリカン航空96便（1972-06-12）

| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 日付・便名・機体 | ✅ | senate p.17（印字5） | "American Airlines, Inc., Flight 96, a DC-10-10, N103AA" | 1972-06-12、AA96便、DC-10-10、N103AA（製造番号 46503） |
| 区間 | ✅（注記） | senate p.17（5） | "from Los Angeles, California, to LaGuardia Airport, New York, with intermediate stops at Detroit, Michigan and Buffalo, New York" | 便はロサンゼルス発ニューヨーク（ラガーディア）行きで、デトロイトとバッファローに寄る。事故はデトロイト→バッファロー区間。「デトロイト発バッファロー行き」は**区間としては正しい** |
| 場所 | ⚠️ | senate p.17（5）／faa_Windsor p.2 | "NEAR WINDSOR, ONTARIO, CANADA" | 資料は「ウィンザー**付近**」。「上空」「真上」とは書いていない。NTSB の勧告書簡は "shortly after takeoff from Detroit"（senate p.46＝印字34） |
| 高度・上昇中 | ✅ | senate p.18（6）・p.21（9） | "at approximately 11,750 feet altitude and climbing at 260 knots" | 約11,750フィート（**約3,581 m**）、260ノット（約482 km/h）で上昇中、1925（米東部標準時）。離陸は1920。⚠️NTSB の勧告書簡だけは "approximately 12,000 feet"（約3,658 m） |
| ドア脱落・床の落下 | ✅ | senate p.17（5） | "The floor partially collapsed into the cargo compartment, disrupting various control cables" | 後部バルク貨物室のドアが脱落→急減圧→客室床（後部ラウンジ）が貨物室へ部分的に落ちた |
| 傷んだ系統 | ✅ | senate p.22〜23（10〜11）・p.28（16） | "severed some of the cables and severely impaired the operation of others to the No. 2 engine and empennage flight controls" | 左の昇降舵ケーブル2本が切断、方向舵ペダルが前に張り付き、第2エンジンのスロットル・燃料遮断・防火遮断ケーブルが破断、水平安定板トリムの指示計が不作動。外れたドアが**左水平尾翼の前縁も損傷** |
| 引き返して着陸 | ✅ | senate p.18〜19（6〜7） | "The airplane landed at 1944." | デトロイト・メトロポリタン空港の滑走路03Lに1944着陸。右へそれ、滑走路端から約8,800フィート（約2,682 m）で停止。全員スライドで脱出 |
| 死者・搭乗者・負傷者 | ✅ | senate p.17（5）・p.19（7） | "There were 56 passengers and a crew of 11 aboard ... Two stewardesses and nine passengers received minor injuries." | 搭乗**67人**（乗客56・乗員11）。死者**0**。軽傷**11人**（客室乗務員2・乗客9）。⚠️FAA まとめの「負傷者なし」は誤り（別表1） |
| 機長の名前 | ？（一部だけ） | ntsb_…ocr.txt p.19（付録B） | OCR："Brycc …agcd 52"／"First Offi ( p whitncy, agcd 34" | 付録Bは本体版では文字が無く、OCR版で**名「Bryce」・52歳**までしか読めない。**姓は崩れて判読不能**＝この資料では確認できない（一般に知られる姓はこの資料で裏が取れない）。副操縦士は姓「Whitney」・34歳。航空機関士は名前判読不能・50歳 |
| ドアの落下地点（参考） | 注記 | senate p.19（7） | "The cargo door was recovered from a field several miles from the airport." | 地名は書いていない |

## B2. NTSB の結論と地上係員の経緯

| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 推定原因（probable cause＝NTSB が最も確からしいとした原因） | ✅ | senate p.17（5）・p.28（16） | "permitted the door to be apparently closed, when, in fact, the latches were not fully engaged and the latch lockpins were not in place" | 「閉まったように見えて、実はラッチが掛かり切らずロックピンも入っていなかった」を**設計が許した** |
| 警告灯 | ✅ | senate p.28（16）・p.18（6） | "permitted the pilot indicator switch to make contact which turned the cockpit warning light off" | 機構のたわみでスイッチが接触し、操縦室の警告灯が消えた。航空機関士は「地上走行中も飛行中も一度も点かなかった」 |
| 地上係員が力で押し込んだ | ✅ | senate p.17〜18（5〜6） | "The agent could not close the handle with normal force, so he applied additional force with his knee." | 電動で閉める→モーター停止を聞いてハンドル→普通の力で閉まらず**膝で押し込む**→ハンドルは収まったが通気扉（vent door）が少し斜めに閉じた→**整備士に伝えたが整備士が出発を承認**→1911 に駐機場を出た |
| 押し込むのに要る力 | ✅ | senate p.24（12）・p.25（13）・p.37（25） | "the force required to stow the handle was approximately 120 pounds" | ロックピン無しでハンドルを収めるのに約120ポンド（**約54 kg重**）。正常なら約30ポンド（約14 kg重、ブリゼンディン証言） |
| ラッチの位置 | ✅ | senate p.21（9） | "approximately 0.1875 of an inch from their fully closed positions" | 全閉まで約0.1875インチ（約4.8 mm）、オーバーセンター（死点越え）まで0.35インチ（約8.9 mm）足りなかった |
| 主張に無いが台本で要る事実 | 注記 | senate p.28（16） | "this condition was attributed to low voltage to the latch motor" | ラッチが閉まり切らなかった原因は**ラッチモーターの電圧不足**。対策の SB 52-27 は出ていたが**未実施**（所見10・11） |

## B3. NTSB の勧告（1972）

| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 番号・日付・宛先 | ✅ | senate p.28（16）・p.46（34）／faa_Windsor p.42（印字37） | "ISSUED: July 6,1972 … on the 23rd day of June 1972" | **A-72-97 と A-72-98**。**1972-07-06 発出**（採択は 1972-06-23）。宛先は FAA 長官 John H. Shaffer |
| ① | ✅ | senate p.47（35） | "physically impossible to position the external locking handle and vent door … unless the locking pins are fully engaged" | 正確には「**ロックピン**が完全に入っていなければ、外のロックハンドルと通気扉を閉位置にできないように」。対象語は「ラッチ」でなく「ロックピン」 |
| ② | ⚠️ | senate p.47（35） | "relief vents between the cabin and aft cargo compartment to minimize the pressure loading on the cabin flooring" | 「床に穴」ではなく「**客室と後部貨物室の間に**圧力逃がし口（relief vents）」。目的が「床にかかる圧力の荷重を小さくする」 |
| 「等」 | ⚠️ | senate p.17（5） | "the Safety Board made two recommendations" | 勧告は**2件だけ** |
| その後（参考） | 注記 | senate p.47〜49（35〜37） | "checked the box 'Status of Activities' as 'Closed.'" | FAA は翌07-07 に返信（52-27 と A52-35 を300時間以内に実施中。**52-37 に触れず**）。NTSB 事務方は 1972-08-01 に A-72-97 を「Closed」扱い（局長署名 08-08）。上院は NTSB の追跡不足も批判 |

## B4. 「紳士協定」

| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 誰が | ✅ | senate p.30（18） | "the then-Federal Aviation Administrator, John H. Shaffer telephoned Jackson McGowen, then-President of the Douglas Aircraft Company" | FAA 長官シェイファー → ダグラス・エアクラフト社（マクドネル・ダグラス社の一部門）社長マクゴーエン |
| いつ | ✅ | senate p.30（18） | "Prior to Mr. Shaffer's call to Mr. McGowen on June 15, 1972" | **1972-06-15**（事故の3日後）。⚠️上院は "Apparently, three days after…" と**ぼかした書き方** |
| 電話か会談か／どこで | ✅電話／？場所 | senate p.30（18） | "telephoned" | **電話**。どこから・どこへは資料に無い |
| 資料の言葉①（出どころ） | ✅（出どころに注意） | senate p.30（18） | "the corrective measures could be undertaken as a product of a gentlemen's agreement thereby not requiring the issuance of an FAA airworthiness directive" | ⚠️これは**西部地域局長バスナイト（Arvin Basnight）の証言**として上院が引いた言葉＝**又聞き**。長官本人の発言記録ではない |
| 資料の言葉②（本人） | ✅ | senate p.32（20） | "I don't know whether you call it a gentleman's agreement or not." | マクゴーエンは呼び名を留保。合意の中身は「24時間態勢で部品を航空会社へ」＝**52-35 の部品**（本人が "-35" と確認） |
| 資料の言葉③ | ✅ | senate p.48（36） | "the decision to proceed by voluntary agreement between Douglas and the FAA" | "voluntary agreement" |
| 資料の言葉④（委員会の所見） | ✅ | senate p.55（43） | "the Administrator, pursuant to an oral agreement with the president of Douglas Aircraft, decided to address the problem with a company service bulletin" | "oral agreement"（口頭の合意） |
| 長官本人の証言 | ✅（注記） | senate p.31（19） | "we agreed that we would do it by service bulletin" | 当時の機体は "about 35 airplanes"。⚠️上院は長官の記憶（「簡単な板を足す」）を**誤り**と指摘：6/12〜16 に話していたのは**のぞき窓**で、板（52-37）はまだ開発前 |
| 「SB による自主的な改修にした」 | ⚠️ | senate p.32〜34（20〜22） | "absent an AD, the airlines could not be forced to comply" | AD は出さなかったが、FAA は **6月16日（副長官 K. M. Smith）と6月19日（飛行基準局長代行 C. R. Melugin Jr.）に4社へ電報**で点検と SB 52-27・A52-35 の300時間以内実施を要請（"For Official Use Only"＝部外秘扱い）。法的な強制力は無い。＝「FAA の非公開の要請＋メーカーの SB」 |
| 上院の評価（台本の公平のため） | 注記 | senate p.55（43） | "the Administrator was acting honestly and in good faith" | 誠実だったと認めたうえで、AD を使わなかったことを批判 |

## B5. 西部地域局の AD 案

| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| AD を準備 | ✅ | senate p.30（18） | "the FAA's Western Region in Los Angeles was preparing independently, an airworthiness directive which was to be addressed to mandatory modifications" | 6/15 の電話**より前に**、ロサンゼルスの西部地域局が独自に AD を準備していた |
| 3者の暫定合意 | ✅ | senate p.31（19）・p.55（43） | "had reached tentative agreement that the FAA would issue an AD" | 西部地域局・ワシントンの飛行基準局長・副長官 **Kenneth M. Smith** が「AD を出す」で暫定合意 |
| AD の中身 | ✅ | senate p.31（19）・p.36（24） | "related to the installation of a viewing port or window in the fuselage" | 準備中の AD は**のぞき窓**（＝52-35 の内容）。キャノン議員も "52-35 … originally proposed to be covered by an AD" |
| 「案が書き上がっていた」か | ？ | senate p.30（18）／faa_ll | "was preparing" | 上院は「準備中」まで。「書いたが出さなかった（written, but not released）」は **FAA まとめ（二次）だけ** |
| 異議 | ✅ | senate p.32（20） | "he personally appealed the decision to proceed with a company service bulletin to Mr. Shaffer" | バスナイトが数日後に長官へ直訴。長官は検討すると言ったが、その後連絡は無かった |
| 権限（参考） | 注記 | senate p.31（19） | "has delegated authority from the Administrator to issue AD's" | 地域局長は長官から AD を出す権限を委ねられていた |

## B6. SB 4本の日付と中身

| SB | 日付 | 中身 | 判定 | 資料と頁 |
|---|---|---|---|---|
| 52-27 | **1972-05-30**（ウィンザーの**前**） | 貨物ドアのラッチ駆動装置（actuator）の配線を太い線に替え、電圧降下を防ぐ。「recommended」、アラート表示なし | ✅ | senate p.15（3）・p.20（8）・p.33（21）／AD 1(B)。SB 本体は**読めない** |
| A52-35（アラート） | **1972-06-16**（上院 p.34＝印字22 の6/19電報）／**1972-06-19**（AD 74-08-04 の官報・R4） | ロック機構の**のぞき窓**（viewing window／inspection ports）と表示板の取付＋機能点検。1972-08-07 時点で全機完了 | ⚠️日付が資料間で食い違う（改訂日の違いかは不明＝推測の域） | senate p.34〜35（22〜23）／FR p.11992／AD R4 p.2。SB 本体は**読めない** |
| 52-37 | **1972-07-03**（改訂1 1972-08-05、改訂2 1972-08-25） | 題名 "Modify And Adjust Door Mechanism Assembly"。3つの貨物ドアのストライク・プレート交換とピン・スイッチ調整＋**後部ドアに "support and plate" を取付**。「Recommended」、FAA 承認 | ✅日付／❌**「のぞき窓」は含まない** | SB 52-37 p.1〜3／senate p.40〜45（28〜33）・p.32（20） |
| 52-38 | **1972-08-04**（改訂1 1972-10-11、改訂2 1973-03-15） | ラッチ点検口のふた（latch access covers）を、工具を差せる穴つきのふたに交換。電動で閉まらないとき**ふたを外さずに手動でラッチ**できるようにする。理由は「130件の遅延」。「Recommended」。**52-37 と組で実施**の指定 | 注記 | SB 52-38 p.1〜4 |

- 引用：52-37 "Installs support and plate on aft cargo door."（SB 52-37 p.3）。"support plate" の呼び名はダグラスの1974-05-03 書簡（senate p.53＝印字41）。部品表では Support（ADA7797-5）と Plate（ADA7797-7）の**2点**（senate p.45＝印字33）
- 52-37 の対象機（改訂2）に THY 機は**載っていない**。SB は「表に無い機体は引き渡し前に改修する」と書く（senate p.41＝印字29）＝THY 機はロングビーチで改修される前提
- 52-38 改訂2の対象表には "TK" と "46704"・"46705"、胴体番号 "29 and 33" が並ぶ（OCR の崩れで行の対応は確定できない＝**推測**で THY の2機）。仏報告の英訳（aib OCR p.33〜34）は、THY が穴をあけた加工を "incorrect execution of SB 52-38" と書く

## B7. 事故機（THY・29号機）について上院資料が書いていること

| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 機体の呼び方 | 注記 | senate p.52（40）・p.54（42） | "it indicates the No. 29 airplane, which was the Turkish airplane" | 上院資料に **"TC-JAV" の語は出ない**（「THY」「No. 29 airplane」「ship #29」）。仏報告の英訳ではドアに "F/N 29"・"S/N 46704" の刻印（aib OCR p.33） |
| 記録上は済み | ✅ | senate p.51（39） | "According to our manufacturing records, all service bulletins that had been issued to improve the cargo door latching mechanism had been incorporated" | 製造記録では全 SB 実施済み。実物のドアには support plate が無かった |
| 工場と時期 | ✅ | senate p.51（39） | "the aircraft was still on the Douglas assembly line at Long Beach" | 1972年6月時点でロングビーチの組立ライン。**引き渡しは1972年12月** |
| 不完全の中身 | ✅ | senate p.51（39） | "parts of Bulletin 52-37 had been accomplished on the Turkish airplane, although the part in question was not present" | 52-37 の一部は施工済み、肝心の板だけ無い |
| 隣にいた Laker 機 | ✅ | senate p.52（40） | "The Turkish airplane and the Lakers airplane were side by side, not in production, … but in our predelivery modification." | **生産ラインではなく「引き渡し前の改修」工程**で隣どうし。同じ時期・同じ人たち（検査印による）。Laker 機は板以外（ロックピン機構・スイッチ板の調整）は施工済みで、ピン無しで閉めるには約250ポンド（約113 kg重）要った（未施工なら150か120ポンド＝約68か54 kg重）。英国政府が対応（p.55＝印字43） |
| 印を押した人数 | ⚠️ | senate p.53（41） | "the Quality and Reliability Assurance Inspector and the Manufacturing Assistant Foreman whose stamps appeared on the paper work" | 印は**2人**：品質・信頼性保証の**検査員1人**＋製造の**副職長（assistant foreman）1人**。取り付け担当の整備士は**特定できず**。＝「検査員が複数」ではない。2人は検査業務から外され、けん責 |
| 印の日付 | ？資料に無い | senate p.51〜53（39〜41） | — | 押印の日付は無い。あるのは「1972年12月に工場を出た」「ほぼ同じ時期」「社内調査の開始 1974-03-11」だけ |
| 再発防止（参考） | 注記 | senate p.53（41） | "A new stamp agreement will be required from each of these employees every six months." | 印の数を減らし、使用条件の誓約書を半年ごとに取り直す |

## B8. パリの事故のあとの AD

### AD 74-08-04
| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 電報で発効した日 | ✅ | FR p.11992／AD R4 p.4 | "effective immediately as to all known U.S. operators … by individual telegrams dated March 7, 1974, and March 22, 1974" | **3月7日**（事故の4日後）に電報で即時発効、**3月22日**に電報で改正 |
| 官報 | ✅ | FR p.11992 | "This amendment is effective April 2, 1974, as to all persons" | **1974-04-02（火）** 官報 Vol.39 No.64 p.11992 に掲載・全員に発効。発出は 1974-03-28 ワシントン（飛行基準局長 James F. Rudolph）。FR Doc.74-7594。⚠️AD の見出し（番号）は前頁 p.11991 にあり**手元に無い** |
| SB 7本？ | ✅（1974年版）／⚠️（最終版） | FR p.11992／AD R4 p.2〜4 | — | 1974年4月版：A52-35、52-27、52-37（52-49 実施機は除く）、52-43、52-44改1、52-49改1、52-54改1＝**7本**。手元の R4（1975-12-01 発効）は 52-109（近接スイッチ式の警告）が加わり **8本** |
| 義務の中身 | ✅ | FR p.11992 | "Ensure proper locking pin placement by visual check through inspection ports" | 次の飛行の前に3本（のぞき窓・配線・板）を実施。毎飛行前に乗員がのぞき窓でロックピンを目視。与圧に異常があれば降下して最寄りに着陸。30日以内に警告系配線、7月1日までに 52-49 と 52-54 |
| 改正の履歴 | 注記 | AD R4 p.1・p.5 | "Amendment 39-1811 as amended by Amendment 39-2013, 39-2112, and 39-2399 is further amended by Amendment 39-2443." | 原型は 39-1811。以後 39-2013（1974-11-21）、39-2112（1975-04-04）、39-2399（1975-10-31）、39-2443（1975-12-01） |
| 3月22日に「closed loop 方式」を義務化（FAA まとめ） | ？ | FR p.11992 | "Since these amendments clarify requirements or relax unintended restrictions" | p.11992 に見える3月22日改正の理由は「要件の明確化と意図しない制限の緩和」。closed loop の語は無い（前頁が無いので断定不可） |

### AD 74-12-07
| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 「換気口のドア？」 | ⚠️ | AD 74-12-07 p.1〜2 | "(a) Service Bulletin 52-98, 'Doors - Cargo - Modify Vent Doors,'" | 実際は **SB 5本**の義務化：52-98 通気扉の改修、52-99 のぞき窓の交換、52-102 下部貨物ドアの表示の改訂、52-106 ラッチ駆動装置の配線改訂、53-69 中央貨物ドア用ののぞき穴（-30/-30F/-40 だけ）。"vent door" は**貨物ドアについた小さな通気扉**で、客室床の圧力逃がし口ではない |
| 日付 | ✅ | AD 74-12-07 p.1〜2 | "Amendment 39-1861 became effective July 6, 1974." | 原型 39-1861 発効 1974-07-06、改正 39-1923 発効 1974-08-22、期限 1974-12-01 |

### AD 75-15-05
| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 中身と対象 | ✅ | AD 75-15-05 p.1〜2 | "the maximum size opening considered may not have an area of less than 20 square feet" | DC-10・L-1011・747・A300 の全機。下部貨物室に**20平方フィート（約1.86 m²）以上**の穴が急に開いても床が崩れないよう、通気の追加か床の強化（または両方） |
| 日付 | ✅ | AD 75-15-05 p.2〜3 | "Amendment 39-2262 became effective August 11, 1975." | 原型発効 1975-08-11、改正 39-2739 発効 1976-11-03。期限 1977-12-31（承認日程でも1978-12-31まで） |
| 「floors and doors AD」の呼び名 | ？ | faa_ll のみ | — | AD 本文に無い。本文は床のことだけ |

## B9. 上院資料の書誌

| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 題名 | ✅ | senate p.5 | "REPORT ON THE OVERSIGHT HEARINGS AND INVESTIGATION OF THE DC-10 AIRCRAFT" | — |
| 会期・種別 | ✅ | senate p.5 | "93d Congress … 2d Session … COMMITTEE PRINT" | 第93議会 第2会期の委員会資料（Committee Print） |
| 委員会・委員長 | ✅ | senate p.5 | "Prepared at the Direction of Honorable Warren G. Magnuson, Chairman FOR THE USE OF THE COMMITTEE ON COMMERCE" | 上院**商業委員会**（委員長 ウォーレン・G・マグナソン） |
| 小委員会・委員長 | ✅ | senate p.7（iii） | "Howard W. Cannon, Chairman. Subcommittee on Aviation." | **航空小委員会**（委員長 ハワード・W・キャノン） |
| 公表日 | ✅ | senate p.5・p.7（iii） | "JUNE 1974" ／ "June 27, 1974." | 表紙「1974年6月」、送り状 1974-06-27。表紙の「JUL 9 1974」は図書館（カンザス州立大）の受入印とみられる（推測） |
| 公聴会 | ✅ | senate p.13（1）・p.30（18） | "March 26 and March 27, 1974" | 2日間 |
| 資料番号（S. Prt.） | ？ | senate p.5 | — | OCR に **S. Prt. 番号は読めない**。表紙で読める番号は「33-379 O」だけ（米政府印刷局の整理番号とみられる＝推測。S. Prt. 番号ではない） |
| 頁数 | ✅ | — | — | PDF 62頁。印字は v〜vii＋1〜46 |

## B10. Convair・Applegate・FMEA への言及

| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| Convair・Applegate | ？資料に無い | senate 全文（通読＋grep） | — | **無い**。フォルダ内の全テキスト（仏・英報告を含む）でも0件 |
| FMEA（故障モード影響解析）・1969年 | ？資料に無い | senate 全文 | — | **無い**。1969 の語は NTSB の OCR に1件だけ（客室乗務員の入社日） |
| 近い記述（故障解析） | 注記 | senate p.14（2） | "The FAA did in fact require 32 separate system fault analyses for certification of the DC-10" | ブリゼンディン（ダグラス社長）の証言 |
| 同上 | 注記 | senate p.15（3） | "We did not require what in retrospect might have been required, a so-called fault analysis testing." | バスナイト。バッケ（FAA 安全担当）は「当時の規則にこのドアの故障解析の明示的要件は無かった（のちに追加）」 |
| 1970年の地上試験 | 注記 | senate p.14（2） | "On May 29, 1970, while conducting a ground pressurization test … the forward cargo door had been improperly latched and the door came open" | 胴体1号機。これを受けて全貨物ドアに、ロックピンハンドルと連動する通気扉を付けた（FAA 立ち会いなし＝バスナイト証言） |

## B11. 「改修の遅れ」の数字

| 項目 | 判定 | 資料と頁 | 原文の短い引用 | 要点 |
|---|---|---|---|---|
| 1974年3月時点の未改修機の総数 | ？資料に無い | senate 全文 | — | 総数は無い。「機体ごとの報告（ship-by-ship report）」を最近受けた、とだけある（p.35＝印字23） |
| 1972年6月の機数 | ✅ | senate p.31（19） | "at that time there were about 35 airplanes in the system" | 長官の証言で約35機 |
| 1972-08-07 の状況 | ✅ | senate p.35（23） | "service bulletin 52-37, modify and adjust door mechanism assembly, no airplanes complete as of this date" | 52-27・52-35 は全機完了、**52-37 は0機**（キットは UA と AA に発送済み） |
| 1972-08-18 | ✅ | senate p.35（23） | "checked by United Airlines on airplane fuselage number 45" | 改訂版を UA の胴体45号機で確認、全機の改修を開始 |
| National の N60NA | ✅ | senate p.38（26） | "Service Bulletin 52-37 was completed on N60NA after Trip 34 of March 6, 1974" | **パリ事故の3日後**に完了。1973-12-19 から完了まで **782時間48分・着陸438回** を 52-37 無しで飛んだ。同期間の貨物ドアの不具合件数の表もあるが、OCR で列（前・中央・後部）の対応が崩れていて**どのドアの数か確定できない**（読める数字は操縦士報告「0・10」、整備所見「4・12」）。National は「不具合はスイッチと電動の閉めだけ、機械のラッチには問題なし」と書く |
| 委員会の所見 | ✅ | senate p.55（43） | "in at least one instance a U.S. registered aircraft was not modified pursuant to Service Bulletin 52-37 until after the Paris accident" | 「少なくとも1機」 |
| 追跡の遅れ | ✅ | senate p.36（24） | "more than six weeks after the telegraphic alert from the FAA on June 19, 1972" | FAA は自分で確かめず、ダグラスの報告任せ |
| 52-37 の対象機（参考） | 注記 | senate p.40（28）／SB 52-37 p.2 | — | 改訂2：キット要（グループI）AA14・CO5・NA5・UA15＝39機、キット不要（グループII）AA4・LT1＝5機 |
| 通気の勧告 | ✅ | senate p.58（46） | "it took more than a year before the Company and the FAA dealt with the recommendation in an exchange of letters" | A-72-98 は1年以上放置 |

---

## 別表1：FAA Lessons Learned（二次資料）と一次資料の食い違い

| FAA まとめの記述 | 判定 | 一次資料 |
|---|---|---|
| "none of the 67 persons on board were injured" | ❌ | NTSB：軽傷11人（senate p.17＝印字5、p.19＝印字7） |
| "Windsor-Locks, Ontario" | ❌ | NTSB："near Windsor, Ontario, Canada"。"Windsor Locks" の表記は NTSB に無い |
| "About a year prior to the Paris accident"（AA 事故の時期） | ❌ | 1972-06-12 → 1974-03-03＝**約21か月**。同じページ内でも "Twenty-one months" "nineteen months" "19 months" と揺れる |
| AD 74-08-04 の SB を "(SB 52-27, SB 52-37, SB 52-38)"、"All … issued shortly after the American Airlines accident" | ❌ | 52-27 は 1972-05-30＝事故の**前**。52-38 は AD 74-08-04 の本文に**無い** |
| 勧告 A-72-97 が "given rise to" 52-35・52-27・52-37 | ❌（時系列） | 52-27（05-30）・A52-35（06-16/19）・52-37（07-03）はどれも勧告の発出（07-06）より前 |
| "the FAA had written, but not released, an AD" | ⚠️ | 上院は「準備中」と「暫定合意」まで（senate p.30〜31） |
| M-D が "issue the service bulletin as mandatory" を提案 | ⚠️ | SB は「Recommended」か「alert」。上院では電話をかけたのは長官側（senate p.30） |
| "Turk-Hava had only incorporated two of the three service bulletins" | ⚠️ | 上院：改修は**ダグラスが引き渡し前に**ロングビーチで行い、52-37 は**一部だけ**施工（senate p.51〜52） |
| AD 74-08-04 R4 が "seven" SB | ⚠️ | 7本は1974年4月版。R4 は8本 |
| "On March 22, 1974 … 'closed loop' system" | ？ | 官報 p.11992 では確認できない |
| AD 75-15-05 を "floors and doors" AD | ？ | AD 本文に無い呼び名。本文は床だけ |

## 別表2：資料どうしの食い違い・誤植（台本で数字を使うときの注意）

| 箇所 | 中身 |
|---|---|
| senate p.30（18） | "the incident of July 12, 1972" → 同じ頁の他所は June 12。**誤植** |
| senate p.35（23）と p.36（24） | ダグラス書簡の日付が "August 7, 1972" と "August 6, 1972" で食い違う |
| senate p.51（39） | "Service Bulletins 52-29, 52-35 and 52-37" → 52-29 は 52-27 の誤植と思われる（**推測**） |
| A52-35 の日付 | 上院の6/19電報は "16 June 1972"、AD 74-08-04（官報・R4）は "June 19, 1972" |
| 官報 p.11992 の OCR | "52-37 dated July 8, 1972"（SB と R4 は July 3）、"52-43 dated October 6, 1972"（R4 は October 5）＝OCR か印刷の誤りと思われる（**推測**） |
| NTSB の高度 | 最終報告 11,750 ft、勧告書簡 approximately 12,000 ft |
| SB 52-38 | p.2 の見出しが "Revision 2 March 15/72"、送り状は "March 15/73"（SB 側の誤植） |
| senate p.38（26） | National の書簡 "Telegraphic A.D. received 07/00142 March 1974" は OCR 崩れ。「07/0014Z」＝3月7日00時14分（世界時）とも読める（**推測**） |

---

## 1969〜1974年の時系列

| 日付 | 出来事 | 出典 |
|---|---|---|
| 1969 | **資料に記述なし**（FMEA・Convair の話は全ファイル0件） | — |
| 1970-05-29 | 胴体1号機の地上与圧試験で前方貨物ドアが開き、床が局所損傷 → 全貨物ドアに通気扉を追加 | senate p.14（2） |
| 1971-07-28 | N103AA が AA に引き渡される | faa_Windsor p.22（18）付録C |
| 1972-03-03 | N103AA の貨物ドアが電動で閉まらず手動でラッチ、スイッチを調整 | senate p.15（3）・p.19〜20（7〜8） |
| 1972-05-30 | SB 52-27（ラッチ配線を太く）発行・推奨 | senate p.15（3） |
| 1972-06-12 | AA96便、1925 に約11,750 ft（約3,581 m）でドア脱落、1944 デトロイト着陸 | senate p.17〜19（5〜7） |
| 1972-06-13 | ダグラスの点検手順 TWX（CL-SVC-DC-10-COM-77） | senate p.33（21） |
| 1972-06-15 | シェイファー長官がマクゴーエン社長に電話（「紳士協定」） | senate p.30（18） |
| 1972-06-16 | FAA 電報①（副長官 K. M. Smith）：点検・52-27 を300時間以内・「50ポンド（約23 kg重）以上かけるな」の表示板／A52-35 の日付（上院による） | senate p.33〜34（21〜22） |
| 1972-06-19 | FAA 電報②（Melugin 局長代行）：52-27 と A52-35 を300時間以内（A52-35 の日付は AD では6/19） | senate p.34（22）／FR p.11992 |
| 1972-06-23 | NTSB が勧告 A-72-97／98 を採択 | faa_Windsor p.42（37） |
| 1972-07-03 | SB 52-37（support and plate）発行・推奨 | SB 52-37 p.1／senate p.32（20） |
| 1972-07-06 | NTSB が勧告を FAA 長官へ発出 | senate p.46（34） |
| 1972-07-07 | 長官が返信（52-37 に触れず）／ダグラスが 52-37 を「immediate action program」に加えたと航空会社へ書簡 | senate p.47（35）・p.37（25） |
| 1972-07-13 | National が 52-35・52-27 を5機に完了 | senate p.39（27） |
| 1972-08-01 | NTSB 事務方が A-72-97 を「Closed」（08-08 局長署名） | senate p.48（36） |
| 1972-08-04 | SB 52-38 原版 | SB 52-38 p.1 |
| 1972-08-05 | SB 52-37 改訂1 | SB 52-37 p.1 |
| 1972-08-07 | ダグラス→西部地域局：52-27・52-35 は全機完了、52-37 は0機（別頁では8月6日） | senate p.35（23）・p.36（24） |
| 1972-08-18 | ダグラス書簡：改訂版 52-37 を UA 胴体45号機で確認、全機の改修開始 | senate p.35（23） |
| 1972-08-22 | NTSB 予備報告 | faa_Windsor p.19（15）付録A |
| 1972-08-25 | SB 52-37 改訂2 | SB 52-37 p.1 |
| 1972-10-05 | SB 52-43（警告系の配線）※官報 OCR は10月6日 | AD R4 p.3／FR p.11992 |
| 1972-10-11 | SB 52-38 改訂1 | SB 52-38 p.1 |
| 1972-12 | THY 機（29号機）と Laker 機が「52-37 済み」の記録のまま工場を出る。THY へ引き渡し | senate p.51（39） |
| 1973-02-23 | NTSB が FAA に通気の勧告（A-72-98）の進み具合を照会 | senate p.48（36） |
| 1973-02-28 | NTSB 報告 AAR-73-02 採択 | senate p.16〜17（4〜5） |
| 1973-03-15 | FAA 返信（メーカーに再評価を要請）／SB 52-38 改訂2 | senate p.48〜49（36〜37）／SB 52-38 p.1 |
| 1973-04-14 | SB 52-54 改訂1（AD の記載どおり） | FR p.11992 |
| 1973-08-14 | SB 52-44 改訂1 | FR p.11992 |
| 1973-09・11 | NTSB 事務方が FAA に照会、新情報なし | senate p.49（37） |
| 1973-10-25 | SB 52-49 原版 | FR p.11992 |
| 1973-12-19 | National の N60NA が運航に復帰（以後 52-37 無しで 782時間48分） | senate p.38（26） |
| 1974-03-03 | パリ近郊で THY の DC-10 が墜落、**346人全員死亡** | senate p.13（1） |
| 1974-03-06 | N60NA が 52-37 を完了 | senate p.38（26） |
| 1974-03-07 | AD 74-08-04 を電報で発効 | FR p.11992／AD R4 p.4 |
| 1974-03-11 | ダグラスが support plate の食い違いの社内調査を開始 | senate p.53（41） |
| 1974-03-15 | SB 52-49 改訂1 | FR p.11992 |
| 1974-03-22 | AD 74-08-04 を電報で改正／National が NTSB に回答書簡 | FR p.11992／senate p.38（26） |
| 1974-03-26・27 | 上院航空小委員会の公聴会 | senate p.13（1）・p.30（18） |
| 1974-03-28 | AD 74-08-04（改正込み）を官報用に発出 | FR p.11992 |
| 1974-04-02 | 官報に掲載、全員に発効 | FR p.11992 |
| 1974-04-30 | 仏大使館から委員会へ予備的な結論（ドア喪失と急減圧、爆発説は否定） | senate p.50（38） |
| 1974-05-03 | ダグラス（ブリゼンディン）が押印の調査結果を委員会へ | senate p.53（41） |
| 1974-06 | 上院の委員会資料（送り状 06-27） | senate p.5・p.7（iii） |
| 1974-07-06 | AD 74-12-07 原型発効 | AD 74-12-07 p.2 |
| 1974-08-22 | AD 74-12-07 改正発効 | AD 74-12-07 p.2 |
| 1974-11-21 | AD 74-08-04 改正（39-2013）発効 | AD 74-08-04 R4 p.5 |
| 1974-12-01 | AD 74-12-07 の期限 | AD 74-12-07 p.1 |
| （参考）1975-08-11 | AD 75-15-05（床）原型発効 | AD 75-15-05 p.2 |
