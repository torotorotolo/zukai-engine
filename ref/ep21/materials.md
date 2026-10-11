# 21本目（9.11 米国同時多発テロのリメイク）素材の棚卸し ── 判定の表（2026-10-11・①素材の係）

> ①は**判定の表だけ**（取得はしない）。動画・画像の本体は落としていない＝目録・API のメタデータ・頁の文字・`ffprobe` のヘッダ・YouTube の情報と自動字幕（`yt-dlp --skip-download`）だけで判定した。**画は1枚も見ていない**＝「写っている物」は題・説明・目録の索引語・自動字幕からの読み。
> 物差し＝Vault `事故検証-ルール統合版-20260923`（§2-1 写真・映像20%以上／§2-3 対象そのもの／§2-5b PD以外も可／§2-5c フリー素材は「イメージ」／§2-10・2-12b PD の根拠を分ける／§2-13 BY-SA は額装・無加工／§2-20b・2-21 器の札は嘘をつく／§1-8 【映像あり】は幅1280以上／§B2-2・B2-2b 人が写る写真）と、10-06「冒頭は実写」・10-11「写真は画面いっぱい」の決め。手本＝`ref/ep20/materials.md`。
> 旧版＝7本目（2026-09-14 公開・10-05 非公開）。旧版の素材の記録＝`ref/CREDITS.md` §9.11・`ref/ep7/clips.json`・`config/meta_ep7.json`・帳簿 `ref/themes/ledger.json` の 7本目の行。
> 生の結果（API の返り値・ffprobe・自動字幕の写し・道具）＝`ref/ep21/src/materials_raw/`（git の外）。PD の根拠の記号＝**A** 米連邦の職務（17 U.S.C. §105）／**B** 保護期間の満了・方式／**C** 自主宣言（PD-self・CC0・献呈）／**C'** 撮影者が権利を放棄（議会図書館の説明）／**D** 「知られた制限は無い」（議会図書館など）／**E** 根拠不明／**F** CC（PD ではない）。

## 0. 結論
1. 🔴 **冒頭（〜最初の見出し）は実写で組める。** 権利の通る（**A**＝米連邦の職員・軍・ホワイトハウス通信局〈WHCA＝国防総省の機関〉の職務の撮影）**2001年9月の動く実写**が、すぐ取れる置き場（DVIDS・ブッシュ大統領図書館〈YouTube と NARA〉・Commons）に**約20本・計 約4時間**（重複を含む・使える秒は映像方針で）ある。いちばん強いのは **当日9月11日のペンタゴン（米空軍 第11通信隊の撮影・DVIDS・18分32秒）**。
   ⚠️ 旧版①（2026-09-13）の「DVIDS に2001年の映像は0本」「Commons の当日〜直後14本はほぼ演説」「NARA は動画の絞り込みが効かない」は**3つとも覆った**（DVIDS は投稿日が2011年以降でも中身が2001年の物が9本〈うち7本は撮影日の欄も2001年〉／Commons に大統領図書館の未編集テープが 2026-09-24 に上がった／NARA は `typeOfMaterials=Moving Images` で絞れる〈陽性対照 Thresher 8,916→90〉）。
2. 🔴 **WTC の当日（衝突〜崩落）の動く実写で権利の通る物は 0本**（探した範囲＝下の §1）。全部が報道局・私人・市（NYPD）の撮影。WTC の当日は**写真**（議会図書館の撮影者不詳の 250枚＝撮影者が権利を放棄）で受ける。
3. 🔴 **【映像あり】は付けない（推奨）。** 9.11 の実写で**実効1280以上は 0本**（2001年の撮影は全部標準画質＝器の最大 854×474〈YouTube〉・720×486〈NARA の ProRes 原本〉・640×480〈DVIDS〉）。器が 1280 なのは旧版の RG237 の**画面収録3本（1280×1024・レーダー再生ソフト）だけ**＝実写ではない。17本目の前例（器4K・中身は標準画質＝付けない）に合わせる。RG237 で名乗るかは親とカズヤくんの決め（旧版7本目はこれを含む RG237 で名乗った）。
4. **衝突の瞬間**が写る権利の通る動く映像は、**ペンタゴンの監視カメラ2本（国防総省・2006年公開・312×212 と 352×240）だけ**。旧版は「衝突の瞬間」を禁じ手にしていた＝使うかは決め。
5. **旧版の写真67点**：根拠 A 22・C 10・C' 2・D 6・F（CC BY）27・**BY-SA 0**・B 0・E 0。67点とも幅1920以上（縦長12点）。今のルールで見直すと **◎○ 18点（対象そのもの・時代も合う）／△ 29点（イメージ扱い）／× 20点（別物・時刻違い・型違い＝差し替え）**。🔴 出典・中身の誤り2件（`wtc_smoke_day` の撮影者・`fire_trucks_day` の時刻）。
6. **旧版の動く素材 RG237 32点**は変わらず使える（use=Unrestricted）。⚠️ 旧版の台帳の「access も Unrestricted」は今の目録では **Restricted - Possibly**（FAA の黒塗りの注記）＝利用の制限ではない。
7. **写真の在庫**：撮影日が 2001-09-11 の写真で幅1920以上・本当に A のものが**約470点**（9/12〜9/14 で約135点）＝当日の写真で 20% を満たす量はある。🔴 議会図書館の 9.11 の 250点は Commons の札が「PD US Government」だが実は撮影者が権利を放棄した写真（C'）＝出典の書き方を分ける。
8. **声**：NARA の管制の録音の条件は旧版①のまま（全点 use=Unrestricted）。点数は変わった（RG237 音 770→1,042・RG148 5952561 342→272）。UA93 の CVR は封印のまま（裁判所の頁は今 404）。

## 1. 冒頭の実写の候補（推奨の順）

### 1-1 上位5つ（取れる置き場にある・A）
| 順 | 素材（置き場） | 撮った人・根拠 | 写っている物（確かめた方法） | 撮った日 | 長さ | 器（実測）→ 実効 | 人の写り（説明で分かる範囲） | 衝突の瞬間 | 判定 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **ペンタゴン当日**：DVIDS `122342`「Noble Eagle, Sep 11 - Part 1」＋`122343`「Part 2」 https://www.dvidshub.net/video/122342 ・/122343 | 米空軍 第11通信隊 Tech. Sgt. Robert Stenberg（制作）＝**A**（DVIDS「PUBLIC DOMAIN」） | 説明「攻撃された直後のペンタゴンと救助の隊員のいろいろな映像」（DVIDS の説明文だけ） | **2001-09-11** | 8:52＋9:40＝**18:32** | プレーヤーの mp4 **640×480**（SAR 131:128）。頁に置かれた写しはこの1本だけ（HD が原本の動画には 1024×576 などの写しが付く＝例 DVIDS `814685`）。High-Res の原本は要ログイン＝未測 → 実効 ≤720（2001年の標準画質・推測） | 救助の隊員（消防・軍＝職務＝可）。負傷者・遺体の有無は説明に無い＝**未確認** | 無し（「直後」） | ◎ 冒頭の軸 |
| 2 | **ペンタゴン 9/12**：大統領図書館「[2021-0032-F] WHTV 600 09122001 President Tours Damage of the Pentagon」YouTube `iJz-wjjBu1s`（Commons に同じ物の写し＝2026-09-24 に上がった） | WHCA（国防総省の機関）＝**A**。図書館の説明「public domain・許諾不要・クレジットは Courtesy George W. Bush Presidential Library」（YouTube の札は CC BY） | 題「大統領がペンタゴンの被害を視察」（題だけ・自動字幕なし＝未編集のテープ） | 2001-09-12 | **30:29** | YouTube の最大 **854×474** → 実効 ≤720（同じ WHTV の NARA 原本は ProRes 720×486・SAR 40:33） | 大統領・国防長官ら（公職）・消防/軍（職務）。私人は未確認 | 無し | ○ |
| 3 | **WTC 跡 9/13〜**：DVIDS `734981`「Ground Zero Timeline Compilation」 https://www.dvidshub.net/video/734981 | FEMA・Video by Paul Luke＝**A**（DVIDS「PUBLIC DOMAIN」・VIRIN 010913-D-PL703-601） | 説明「FEMA が2001年に出した公式の B-roll。WTC 跡の捜索・復旧。崩落から8か月のあいだ報道向けに出した映像の寄せ集め」 | 2001-09-13〜（8か月分） | **30:35** | **640×480**（SAR 1:1）→ 実効 ≤720（推測） | 作業員・消防（職務）。🔴 捜索の映像＝遺体の収容・覆われた遺体・担架が入る恐れ＝**未確認** | 無し | ○ |
| 4 | **WTC 跡 9/14（大統領の現地入り）**：大統領図書館 WHTV 609「Trip to New York 1 of 2」YouTube `IEjC7NqlTJw`（41:58）＋WHTV 610「2 of 2」`9jhrvN9gfv8`（7:44）／NARA naId **6171391**「Remarks from Ground Zero」（MP4 640×360・MOV ProRes 720×486・2:23） | WHCA＝**A**（NARA use=Unrestricted・access=Unrestricted） | 目録「マレー街とウエスト街（WTC の跡）で、大統領が警察・消防・救助の作業員に話す」 | 2001-09-14 | 計 約52分 | 854×474／720×486 → 実効 ≤720 | 消防・警察・救助（職務）。周りの私人は未確認 | 無し | ○ |
| 5 | **ペンタゴン 9/14（空撮と地上）**：DVIDS `122347`「Noble Eagle, Sep 14」（空撮・VIRIN 010914-F-5177S-001）＋`122344`〜`122346`「Noble Eagle - Part 1〜3」（VIRIN 010914-F-0678B-002） | 米空軍 第1戦闘カメラ隊（1st CTCS）Tech. Sgt. T. Szestowicki／Staff Sgt. David Barlow＝**A** | 説明「攻撃で受けたペンタゴンの被害の空撮」「被害のいろいろな映像」 | 2001-09-14 | 2:24＋9:56＋9:54＋7:38＝**29:52** | **640×480** → 実効 ≤720 | 空撮は人が小さい見込み／地上は未確認 | 無し | ○（空撮は冒頭に強い） |

### 1-2 そのほかの当日〜直後（A）
| 素材（置き場） | 撮った人・根拠 | 写っている物 | 撮った日 | 長さ | 器 → 実効 | 人の写り | 衝突の瞬間 | 判定 |
|---|---|---|---|---|---|---|---|---|
| 小学校の朝（未編集）：大統領図書館「WHTV 598 20010911 Reading Program Demonstration at Emma Booker Elementary cut camera」YouTube `dIc3xqjFvUo`（Commons に写し）／編集版 NARA `6171388`（1:55） | WHCA＝A | 自動字幕＝朗読の授業が続く（首席補佐官の耳打ち〈委員会報告で 9:05 ごろ〉が入っている見込み・秒は**未確認**）→ 9:30 ごろの声明 | **2001-09-11** | 12:57 | 854×474 → ≤720 | 🔴 **子ども（私人・未成年）の顔**＝使うなら顔だけモザイク（PD なので可）／大統領・補佐官（公職） | 無し | △（強いが子どもの顔） |
| バークスデール空軍基地：WHTV 606 YouTube `CDB1RvFZzhg`／NARA `6171389`（MP4 **720×484**・893秒・1,120MB と 640×360・148秒） | WHCA＝A | 目録「大統領専用機の到着・報道官の声明・大統領の声明・出発」 | **2001-09-11** | 14:53 | 720×484 → ≤720 | 公職・基地の隊員（職務）・報道陣 | 無し | ○ |
| 夜の演説：NARA `6171390`「Address to Nation on Terrorist Attacks」（MOV ProRes **720×486**・285秒／MP4 640×360） | WHCA＝A | 執務室からの国民向け演説（夜） | **2001-09-11** | 4:45 | 720×486 → ≤720 | 大統領だけ | 無し | ○（締めの候補） |
| ホワイトハウスの退避：WHTV 1501「Crowd Shots outside Old Executive Office Building」YouTube `CAaOJiSqWkw` | WHCA＝A（図書館の説明「Records of White House Evacuation on September 11, 2001」） | 外に出た人の群れ。⚠️ 自動字幕に**テレビの報道の音声**が混じる（音は使わない） | **2001-09-11** | 11:31 | 最大 650×480 → ≤650 | 職員・通行人（私人の可能性）＝中景まで・近景は顔だけモザイク | 無し | △ |
| 国防長官の会見：DVIDS `154917`／Commons「9 11 Terror Attacks Historical Pentagon Briefing.webm」 | 国防総省＝A | ペンタゴンの会見室（当日の夜） | **2001-09-11** | 17:38 | **720×406** → ≤720 | 公職・記者 | 無し | △ |
| 米海軍「OPERATION NOBLE EAGLE PRIME CUTS」DVIDS `758340`（Defense VI Records Center） | 米海軍の撮影＝A（DVIDS「PUBLIC DOMAIN」。Date Taken 2019-06-10 は記録センターの受け入れ日） | 説明「ニューヨークとアーリントンで隊員と救助の人が質問に答える・2001-09-14」索引語＝空撮・消防・海兵隊 | 2001-09-14 | 13:14 | 640×480 → ≤720 | 隊員・救助（職務） | 無し | △ |
| **ペンタゴンの監視カメラ**：Commons「Pentagon Security Camera 1.ogv」（312×212・3:11）・「…2.ogv」（312×212・3:22）・「Flight77-2.ogv」（352×240・3:23） | 国防総省の無人カメラ（2006年に情報公開で公表）＝A（PD US Government） | 説明「1分25秒ごろに機が入って衝突」＝駐車場のゲートのカメラ・**爆発の火の玉** | **2001-09-11** 9:37 | 各 約3分 | 312×212／352×240 | 人は写らない見込み | 🔴 **あり** | △ 決め（旧版は禁じ手） |

### 1-3 置き場がオフライン（NARA に複製を頼めば出る＝費用＝課金＝要相談）
NARA の目録を `typeOfMaterials=Moving Images` で25語引き、重複を潰した 2,202件から 9.11 に当たる 248件を読んだ。**デジタルの写しが目録に付いているのは大統領図書館の WHTV（上の4点＋議会演説・愛国者法）と EPA の煙の拡散モデル（アニメ）だけ**。下は写しが無い。
| 系列 | 例（naId・題・日付） | use／access | 見立て |
|---|---|---|---|
| RG330（国防総省の戦闘カメラ「Moving Images Related to Combat Visual Information」） | `149281016`「Pentagon 9/11 - Fire Footage (Raw)」2001-09-11（索引語＝空撮・緊急対応）／`518615783`「Pentagon 9/11 Attack」2001-09-11（消防・FBI・ヘリ・会見）／`518615385`「Pentagon Relief Efforts…」2001-09-12／`519763159`・`518616104`「Aerials of Ground Zero」2001-09-19（大西洋艦隊戦闘カメラ群）／`519763158`「Evening/Night Shots of Ground Zero」9/19／`519763161`「Rescue Efforts NYC」9/15／`640883613`「WTC Strike Team」（沿岸警備隊）9/21 ほか約80件 | Restricted - Possibly（「著作権：一部が他者の権利かもしれない」という NARA の一般の札）／ほぼ Unrestricted | 撮影は A の見込み。**取り寄せは費用**。2001年の撮影＝標準画質＝【映像あり】には効かない見込み |
| RG311（FEMA） | `78073894`「Ground Zero Footage」2001-09-13／`78074567`「FEMA Footage of Ground Zero Cleanup」／`563888324` ほか「Post 911 WTC Recovery」 | 同上 | DVIDS `734981`（FEMA の寄せ集め 30分）と重なる見込み |

### 1-4 使わない（推奨）とその理由
| 候補 | 理由 |
|---|---|
| NIST の情報公開の映像（Internet Archive「NIST 9/11 Release NN」・Commons の2本） | 撮影者は報道局・私人・市（NYPD）＝§105 の外。IA の「Public Domain Mark」は載せた人の札（旧版①と同じ判断） |
| 報道の放送の録画（IA の放送アーカイブ・各局の YouTube） | 権利者がいる（§2-5b の引用でも、同じ場面を A で撮れているなら A を先に） |
| 『平成１３年防衛庁記録』（防衛省 YouTube `q0d-0t1dBkU`・CC BY 3.0・器 3840×2160＝中身は標準画質の見込み） | 03:48〜「米国同時多発テロ事件への日本の対応」。自動字幕では 03:58「9月11日 米国同時多発テロ事件発生」・04:06「翌12日…」のあとは日本の対応（輸送機の出発・護衛艦の出港）。テロの画（約25秒）は**報道の映像の見込み＝出どころ未確認**＝CC BY の札が第三者の映像まで覆うとは限らない |
| NIST の YouTube（`bERV6IRbXeM` 1920×1080 ほか） | 2011年の説明映像。中の当日の映像は報道の許諾物の見込み（未確認） |
| Commons「World trade center.ogv」（1976『The Twins』・648×486） | 札は「PD US Government」だが**制作は私企業（Western Electric）＝根拠 E**。事件の前の動く絵として使うなら②で根拠を当たる |
| Commons「Torri Gemelle - WTC - New York - Sept 99.ogv」（1999・CC BY-SA 3.0＋GFDL・720×576・4:53） | **事件の前のツインタワーの動く絵**（旧版①は「事件の前の動く絵 0本」）。冒頭でなく前提の章で。BY-SA＝額装・無加工＝「画面いっぱい」の例外 |
| NARA RG306（米国広報文化交流庁 USIA）「World Trade Center Dedicated in New York」1973-04-10（naId `215877110`）・「World Trade Center」1969（`215877109`） | 事件の前の動く絵・連邦の制作＝A の見込み（NARA の札は一般の「Restricted - Possibly」）。**オフライン**＝取り寄せは費用（要相談） |
| 2020年以降の 4K 空撮（Commons「Aerial views of World Trade Center…」CC BY 3.0・3840×2158 ほか） | 現在の現場＝「現在の」と断る・記録映像ではない＝【映像あり】と20%に数えない |

### 1-5 冒頭の見立て
- **冒頭は実写で組める**（10-06 の決めを満たす）。当日の動く実写＝ペンタゴン（米空軍 18分32秒）・大統領の一日（朝の小学校／昼のバークスデール／夜の演説＝WHCA）・ホワイトハウスの退避。翌日以降＝ペンタゴンの視察（9/12）・ペンタゴンの空撮（9/14）・WTC 跡（FEMA 9/13〜・大統領 9/14）。
- 旧版の背骨（空・管制・防空）に合わせるなら、冒頭の軸は **「当日のペンタゴン（米軍の撮影）」＋「大統領の一日」**。RG237（レーダーの再現・管制の画面）は実写ではない＝冒頭に置かない。
- WTC の当日は動く実写が無い＝**写真**（議会図書館の撮影者不詳の 250枚〈C'〉・NASA の宇宙ステーションの写真〈A・今回は未計数〉）を全面＋動き（寄る・流す）で受ける。
- 🔴 動く実写は**全部が標準画質**＝全面に出すと約2.7倍の引き伸ばし。全面か額装（地はぼかし＝17本目の型）かは映像方針で（10-11「写真は画面いっぱい」の決めは写真の話＝映像の扱いは未決）。

## 2. 【映像あり】の判定
| 種類 | 本数 | 器の最大（実測） | 実効（見込み） | 実効1280以上 |
|---|---:|---|---|---:|
| 当日〜直後の実写（§1-1・1-2） | 約20本 | 854×474（YouTube）・720×486（NARA ProRes）・640×480（DVIDS） | ≤720（2001年の標準画質） | **0** |
| NARA RG330・RG311（オフライン） | 約100件 | 未測 | 標準画質の見込み | 0（見込み） |
| 旧版の RG237（レーダー再現・管制の画面） | 32 | 1280×1024（3本）・720×480（27本・SAR 10:11）・640×480（2本） | 画面収録3本は 1280（ソフトの帯を除くと 1280×880）／ほかは ≤720 | 3（**実写ではない**） |
| 事件の前の WTC の動く絵 | 2 | 720×576・648×486 | ≤720 | 0 |
| 現在の空撮 | 5以上 | 3840×2158 | 未測 | 数えない |
- 判定＝**9.11 の実写で実効1280以上は 0本**＝【映像あり】は**付けない（推奨）**。RG237 の画面収録で名乗ると「タイトルが動画より強いことを言わない」（§B4-5）に当たる恐れ＝決めは親とカズヤくん。
- 「無い」の範囲＝DVIDS（題の語で24通り・TF-911 の17本）／ブッシュ大統領図書館の YouTube（検索で引いた範囲）／NARA（Moving Images・25語・248件）／Commons（動画の検索24通り＋9.11 の動画のカテゴリ23個＝962件・動画でない物を含む）／Internet Archive（検索5通り）／NASA の画像・動画の API（5通り＝9.11 の動画 0）。

## 3. 旧版の素材の再判定

### 3-1 動く素材（RG237 naId 7419198・32点）
- 32点（31 naId）は変わらず。**use=Unrestricted**（利用の制限なし）。🔴 **access は今の目録で「Restricted - Possibly」**（注記「FAA の黒塗りを含む記録がある・情報公開請求で見直しを求められる」・2026-06-07 の取り込み）＝旧版 CREDITS の「映像32点（access も Unrestricted）」は今の値と違う。access は閲覧の制限の札で、使えることは変わらない。
- 同じ系列の動画に N47BA（1999年）の VHS 7点が増えているが、9.11 の32点とは別（頭の番号 1〜5 で分けられる＝旧版の鍵のまま）。
- 実写ではない＝冒頭に置かない。本編の管制・航跡の場面の地（旧版どおり：SAR 10:11 の補正・`-an`・yadif なし）。

### 3-2 写真67点の要約（`ref/CREDITS.md` の7本目の表・Commons の頁と隠しカテゴリで当て直した）
- **根拠**：A 22（米軍・FAA・NTSB・原子力規制委員会・EPA）／C 10（CC0 8・Highsmith の献呈 1〈＋D〉・博物館の PD-author 1）／C' 2（議会図書館の「撮影者不詳の写真」＝撮影者が権利を放棄）／D 6（Korab 5＝議会図書館「知られた制限は無い」・U.S. News & World Report 1）／F（CC BY）27／**CC BY-SA 0**／B 0／E 0。
  ⚠️ 旧版の概要欄は A・C・C'・D をまとめて「写真（パブリックドメイン）」と書いていた＝D は PD の宣言ではない（§2-12b）＝21本目は「米議会図書館蔵／知られた制限なし」と書き分ける。⚠️ `hearing` は Flickr の札が CC BY 2.0・Commons は PD-USGov-NRC（連邦の職務＝A と読む）。
- **大きさ**：67点とも幅1920以上・高さ1080以上。**縦長12点**（WTC の Korab 4・USNWR 1・保安検査・操縦室の扉・管制 2・レーダー・公聴会・録音機）＝画面いっぱいにすると大きく切る＝例外の候補（10-11 の決めの④）。
- **BY-SA**：旧版は「PD と CC BY だけ」で選んだ＝0点。21本目で外から足す BY-SA（例：AA11 の事故の前の写真 N334AA・CC BY-SA 3.0／4機を並べた合成 CC BY-SA 3.0／1999年の WTC の動画）は**額装・無加工＝画面いっぱいの例外**に印。
- **使い方の再判定**：◎ 4・○ 14（この事故の対象そのもの＋時代が合う）／△ 29（イメージ扱い＝対象そのものでない・会社や時代が違う＝今のルールなら「イメージ」と出し、20%に数えない）／× 20（別物・時刻違い・型違い＝差し替え）。
- 🔴 **出典・中身の誤り（旧版の行を流用すると誤りが残る）**
  1. `wtc_smoke_day`：撮影者は Mike Goad では**ない**。Commons の頁は「撮影者 {{Anonymous}}・議会図書館の『撮影者不詳の写真』（ニューヨーク地区検察局から受けた 250枚のスライド・撮影者が権利と名前の表示を放棄）」。Mike Goad は Flickr に載せ直した人（頁の題に Flickr の番号）。⚠️ 題は「両棟から煙」＝両棟が燃えている絵なら 9:03 より後＝旧版の c313「北棟から上がる煙」（9:03 より前の場面）と食い違う恐れ（絵は未見）。
  2. `fire_trucks_day`：説明は「**燃える第7ビル（7 WTC）**」「午前10時〜午後1時30分ごろの撮影」＝旧版の c314「街の目は、北棟に集まった」（8:46〜9:03 の場面）・副題「現場へ向かう消防車」と時刻も中身も食い違う。
  3. `pentagon_west_day`：Commons のカテゴリに「Remains and debris related to the September 11 attacks」＝**遺体の写りを②で原寸で確かめるまで冒頭に置かない**。
  4. `commute_pre`：説明は「深夜の地下鉄の駅」＝旧版は「8時台」の朝の画に使った。
  5. **時代の逆転**：`gate_pre`（2023）・`fids_pre`（2017）を「事件の前」の欄に、`cockpit_door_pre`（2015＝事件の後の強化扉の時代）を「事件の前の造りの扉」に、`cabin_phone`（2018・座席の電話なし）を「機内から電話」に使っていた（副題に年は出していた）。`logan_takeoff`（2024 のユナイテッド 737＝11便は AA の 767）・`b767_cruise`・`dulles_rwy`・`window_cruise` は副題に年も無かった。
- **別物の疑い（名指しの3つ）**：AMISOM Public Information＝**2016年・ソマリアのモガディシュ空港**の X 線検査（旧版の本編では未使用・CREDITS の表にだけ残る）／Tekniska museet＝**スウェーデン・アーランダ空港のレーダー表示器**（博物館の展示品・副題で断っていた）／Nuclear Regulatory Commission from US＝**2012年・原子力規制委員会の委員長が答える議会公聴会**（9.11 委員会ではない）。ほかの別物＝`andrews`（ドイツのラムシュタイン）・`base_rwy`（1967年のベトナム）・`controller_pre`（1987年のフィリピンのクラーク空軍基地）・`artcc_screen2`／`artcc_now`（2025年・中東の米空軍）・`artcc_alt`（2010年・米空軍の遠征部隊）・`artcc_seat`（2021年・宇宙軍の基地）・`recorder`（2019年のマイアミ航空293便）・`logbook`（第二次大戦の英空軍）・`library_reports`（ニュージーランド）・`security_now`（モスクワ）。
- **人の写り**（説明で分かる範囲・画は未見）：職務の人（管制官・整備員・消防士・NTSB 調査官・原子力規制委員会の委員長）＝使ってよい。私人の可能性＝`lobby_pre`・`security_pre`・`gate_pre`・`reagan`・`cabin_pre`・`stranded_day`・`security_now`・`shanksville_day`（来訪者）。BY-SA が無い＝私人の顔は全部「顔だけモザイク」が使える（CC BY・PD・CC0）。血・負傷者・落下する人は説明に無い（`pentagon_west_day` のカテゴリだけ要確認）。

### 3-3 写真67点の表
「旧版の使い方」は 7本目の最終のカット定義（git `037691a` の `tools/cuts/*.py` の `t=`・`s=`）から。日付・大きさ・根拠は Commons の頁（2026-10-11）。
| 欄 | 旧版のカット「副題」 | 元の題（Commons） | 撮影者（出典） | 撮った日 | 根拠 | 画面いっぱい | 人（説明の範囲） | 時代・別物 | 21本目 |
|---|---|---|---|---|---|---|---|---|---|
| `manhattan_pre` | pr01「ローワーマンハッタン　2001年以前」 | World Trade Center towers, New York, LCCN20156… | Carol M. Highsmith | 2001-07 | C（Highsmith の献呈）＋D | ○ 5740×3981（上下を少し切る） | 遠景・人なし | 事件の前（2001-07）＝正しい | ◎ 冒頭・c1（事件の前の朝の街） |
| `commute_pre` | c218「ニューヨークの地下鉄の駅　1993年撮影」 | Downfolders-downfolder34-2011 02 02 00 10 05.j… | Alex Lozupone | 1993-01-29 | F（BY） | ○ 2935×2062（上下を少し切る） | 説明に人の記載なし（未確認） | ⚠️ 説明＝「深夜の地下鉄の駅」→ 旧版は「8時台」の朝の画に使った（時間帯が逆） | △ 使うなら副題を「夜」に合わせる |
| `wtc_far` | c213「世界貿易センター　2001年以前」 | World Trade Center, New York. Exterior. Twilig… | Balthazar Korab | 1976 | D | △ 縦長 3303×4855 | 建物（遠景） | 事件の前（1976） | ○ |
| `wtc_twin` | c214「ツインタワー　2001年以前」 | View of the New World Trade Center, 1971.jpg | Thomas J. O'Halloran | 1971-01-12 | D（USNWR＝議会図書館へ譲渡） | △ 縦長 3458×5226 | 建物 | 事件の前（1971・建設中の可能性＝未確認） | ○（建設中なら副題で断る） |
| `wtc_base` | c215「世界貿易センターの足元　2001年以前」 | World Trade Center Exterior Entrance arches wi… | Balthazar Korab | 1976 | D | △ 縦長 6209×7923 | 広場（人が小さく写る可能性・未確認） | 事件の前（1976） | ○ 縦長 |
| `wtc_south` | c311「ツインタワーの南棟　2001年以前」 | World Trade Center, New York. Exterior. View f… | Balthazar Korab | 1976 | D | △ 縦長 4536×5758 | 広場から見上げ（未確認） | 事件の前（1976） | ○ 縦長 |
| `wtc_under` | c801「世界貿易センター　1976年撮影」 | World Trade Center, New York. Exterior. Night … | Balthazar Korab | 1976 | D | △ 縦長 3233×4896 | 建物（夜景） | 事件の前（1976）。欄の狙いは「地下」だが絵は夜景＝副題は旧版で直してあった | ○ |
| `lobby_pre` | pr05「空港の出発ロビー　2001年以前」 | Memphis-international-airport-1970s.jpg | Euthman Ed Uthman | 1973 | F（BY） | ○ 2770×1847 | 乗客（私人）の可能性 | 1970年代のメンフィス空港＝当日の空港ではない | △ イメージ（「1970年代・別の空港」と断る） |
| `security_pre` | c111「空港の保安検査場　2001年以前」 | Orange County Airport, security officer, Sept.… | Orange County Archives | Sept. 1970 | F（BY） | △ 縦長 2681×3912 | 保安係（職務）＋乗客（私人）の可能性 | 1970年のオレンジ郡空港 | △ イメージ。私人の顔は CC BY＝顔だけモザイク可 |
| `gate_pre` | c114・c204「空港の搭乗口　2023年撮影」 | Boarding Southwest Airways B737-700 N242WN at … | Infrastorian | 2023-02-20 | C | ○ 4032×3024（上下を切る） | 乗客（私人）の可能性 | 🔴 2023年の写真を「事件の前の搭乗口」の欄に（副題は2023年と断っていた） | × 差し替え（時代が合わない） |
| `fids_pre` | c320「空港の出発案内板　2017年撮影」 | Departure Board at ORD.jpg | Redolta | 2017-03-15 | C | ○ 3145×2359（上下を切る） | 未確認 | 🔴 2017年のシカゴの案内板を「事件の前」の欄に | × 差し替え |
| `logan` | c106「ローガン空港　2001年以前」 | LOGAN AIRPORT-CONTROL TOWER AND RUNWAYS SEEN F… | Michael Philip Manheim | 1973-09 | A（EPA DOCUMERICA） | ○ 3000×2045 | 遠景 | 事件の前（1973）。DOCUMERICA は請負の撮影者＝A の根拠はやや弱い | ○ |
| `logan_apron` | c116「ローガン空港の駐機場」 | Eastern Air Lines terminal at Logan Airport, 1… | Balthazar Korab | 1969 | D | ○ 5796×4612（上下を切る） | 未確認 | 事件の前（1969） | ○ |
| `logan_takeoff` | c115「ローガン空港を離陸する旅客機」 | United 737-800 N73283 takeoff roll Boston Dec … | 4300streetcar | 2024-12-31 | F（BY） | ○ 8256×5504 | 機体 | 🔴 2024年のユナイテッド 737-800（11便は AA の 767）・副題に年が無かった | × 差し替え（型・会社・時代） |
| `dulles` | c107「ワシントン・ダレス空港　2001年以前」 | Aerial view of Dulles Airport, June 1985.JPEG | PH1 DAVID C. MACLEAN | 1985-06-25 | A | ○ 2790×1860 | 空撮・人なし | 事件の前（1985） | ○ |
| `dulles_rwy` | c117「ダレス空港の滑走路」 | Aerial view of Dulles Airport 03.jpg | Dclemens1971 | 2025-07-24 | F（BY） | ○ 4032×3024（上下を切る） | 空撮 | ⚠️ 2025年の空撮・副題に年が無かった | △ 「現在の」と断る |
| `reagan` | c415「レーガン・ナショナル空港　2025年撮影」 | E Concourse DCA National Airport 2025-10-22 15… | G. Edward Johnson | 2025-10-22 | F（BY） | ○ 8160×6144（上下を切る） | 利用者（私人）の可能性 | 2025年（副題で断っていた） | △ 「現在の」 |
| `newark_757` | c602「ニューアーク空港のボーイング757　2017年撮影」 | United 757-200 at EWR (37116055471).jpg | airbus777 from Washington, DC, USA | 2017-09-16 | F（BY） | ○ 3769×2254 | 機体 | 2017年のユナイテッド 757（型と会社は合う・塗装は当時と違う） | △ イメージ |
| `b767` | c108「ボーイング767　2025年撮影」 | Delta Boeing 767-300ER N194DN at Boston May 20… | 4300streetcar | 2025-05-07 | F（BY） | ○ 8256×5504 | 機体 | 2025年のデルタ 767-300ER（型は近い・会社が違う） | △ イメージ |
| `b757` | c109「ボーイング757　2024年撮影」 | Delta 757-200 N710TW taxiing at Boston Nov 202… | 4300streetcar | 2024-11-05 | F（BY） | ○ 8256×5504 | 機体 | 2024年のデルタ 757（会社が違う） | △ イメージ |
| `b767_cruise` | c201「巡航する旅客機」 | Lufthansa A350-900 and United 767-300ER above … | 4300streetcar | 2024-12-27 | F（BY） | ○ 8256×5504 | 機体 | ⚠️ 2024年・ルフトハンザ A350 とユナイテッド 767・副題に年が無かった | × 差し替え |
| `b767_takeoff` | c302「離陸に向かうボーイング767　2012年撮影」 | N352AA (15113637598).jpg | Valentin Hintikka from Finland | 2012-07-27 | F（BY） | ○ 3520×1980 | 機体 | 2012年の AA 767-300（11便は 767-200ER・塗装は当時に近い） | ○〜△ イメージ |
| `b757_takeoff` | c402「離陸するボーイング757　2025年撮影」 | Delta Boeing 757-200 N702TW departing Boston A… | 4300streetcar | 2025-04-01 | F（BY） | ○ 8024×4513 | 機体 | 2025年のデルタ 757 | △ イメージ |
| `airliner_cruise` | c403「巡航する旅客機　2012年撮影」 | Aircraft crossing paths.jpg | Downtowngal | 2012-12-04 | C | ○ 2208×1656（上下を切る） | 機体 | 2012年・上下に交差する旅客機（管制の間隔の説明） | △ イメージ |
| `refuel` | c119「給油中の旅客機　2026年撮影」 | Fueling Boeing 757-200 N58101 at Boston Januar… | 4300streetcar | 2026-01-28 | F（BY） | ○ 8256×5504 | 作業員（未確認） | 2026年のユナイテッド 757 の給油 | △ イメージ |
| `cabin_pre` | c205「旅客機の客室　2017年撮影」 | Airplane aisle during flight (Unsplash).jpg | Suhyeon Choi choisyeon | 2017-01-03 | C | ○ 7360×4912 | 乗客（私人）の可能性 | 2017年（Unsplash） | △ イメージ |
| `cockpit_door_pre` | c202「旅客機の操縦室の扉　2015年撮影」 | Puerto Rico — A 320 JetBlue — Open cockpit doo… | User:Mattes | 2015-02-28 | F（BY） | △ 縦長 3456×4608 | 未確認 | 🔴 2015年の A320 の扉＝事件の後の強化扉の時代の扉を「事件の前の造り」の画に | × 差し替え |
| `cabin_phone` | c614「旅客機の客室　2018年撮影」 | A220 Main Cabin (43799968340).jpg | Delta News Hub | 2018-10-28 | F（BY） | ○ 8256×5504 | 人なしの見込み | 🔴 2018年の A220 の客室（座席の電話は無い）を「機内から電話」の画に | × 差し替え |
| `cabin_767` | c309「旅客機の客室　2011年撮影」 | Delta 767-400ER Economy Cabin.jpg | Vincent Desjardins | 2011-02-03 | F（BY） | ○ 4368×2912 | 未確認 | 2011年のデルタ 767-400ER | △ イメージ |
| `cockpit_pre` | c605「旅客機の操縦室　2025年撮影」 | Avelo Airlines B737 Cockpit.jpg | Funforme3 | 2025-02-24 | F（BY） | ○ 4032×1908 | 未確認 | 2025年のアベロ 737 の操縦室（93便は 757） | × 差し替え |
| `window_cruise` | c304「巡航する旅客機の窓」 | 20250928 View from aircraft in Turkey 01 (3193… | Sergey A. Demidov | 2025-09-28 | F（BY） | ○ 8160×4592 | なし | ⚠️ 2025年・トルコ上空のアエロフロート機の窓・副題に年が無かった | △ イメージ |
| `window_sky` | c909「飛行機の窓から見た空　2025年撮影」 | 20250928 View from aircraft in Egypt 01 (21624… | Sergey A. Demidov | 2025-09-28 | F（BY） | ○ 8160×4592 | なし | 2025年（同上） | △ イメージ |
| `artcc_screen_pre` | pr09「航空路管制センターの卓　連邦航空局の写真」 | AirTraffic-8.jpg | アメリカ連邦航空局（FAA） | 不明 | A（{{PD-USGov-FAA}}・隠しカテゴリなし） | ○ 3008×1960 | 管制官（職務） | ワシントン航空路管制センター（77便の当事者の施設）・年は不明（2007年以前の FAA の報道用写真） | ◎（副題は「撮影年不明」） |
| `radar_scope_pre` | c210「レーダー画面（博物館の展示品）　2016年撮影」 | SR&T Plan position indicator.jpg | Tekniska museet | 2016-03-17 | C（PD-author＝博物館） | △ 縦長 2634×3543 | 展示品 | 🔴 別物＝スウェーデンのアーランダ空港のレーダー表示器（博物館）。副題は「博物館の展示品」と断っていた | △ イメージ |
| `controller_pre` | c306「管制卓に着く管制官　1987年撮影」 | Air traffic controllers of the 1961st Communic… | Department of Defense. American Forces Information Service. | 1987-08-12 | A | △ 縦長 1948×3000 | 軍の管制官（職務） | 🔴 別物＝1987年のクラーク空軍基地（フィリピン）の管制塔＝FAA の航空路管制ではない | × 差し替え |
| `artcc_screen2` | c509「航空管制の卓　2025年撮影」 | 378th EOSS Air Traffic Controller Demonstratio… | U.S. Air Force AFCENT by Staff Sgt. Shaei Rodriguez | 2025-01-06 | A | ○ 7993×5995（上下を切る） | 軍の管制官（職務） | 🔴 別物＝2025年・中東の米空軍の管制塔 | × 差し替え |
| `artcc_alt` | c608「航空管制のレーダー卓　2010年撮影」 | Kingpin and Controllers Maintain Aircraft and … | Master Sgt. Linda Miller | 2010-03-24 | A | ○ 6384×4248 | 軍の管制官（職務） | 🔴 別物＝2010年・米空軍の遠征部隊のレーダー管制 | × 差し替え |
| `artcc_seat` | ep03「航空管制の席　2021年撮影」 | ATC aids TBM Avenger pilot (6666391).jpeg | U.S. Space Force photo by Tech. Sgt. James Hodgman | 2021-05-26 | A | △ 縦長 5504×8256 | 管制官（職務） | 🔴 別物＝2021年・パトリック宇宙軍基地の管制塔 | × 差し替え |
| `pentagon_ext_pre` | c409「ペンタゴン　1998年撮影」 | The Pentagon US Department of Defense building… | DoD photo by Master Sgt. Ken Hammond, U.S. Air Force | 1998 | A | ○ 2734×1726 | 建物 | 事件の前（1998） | ◎ |
| `pentagon_aerial_pre` | c410「ペンタゴンの空撮　1986年撮影」 | An aerial view of the Pentagon - DPLA - 2bad8a… | Department of Defense. American Forces Information Service. | 1986-05-01 | A | ○ 2800×1880 | 空撮 | 事件の前（1986） | ◎ |
| `pentagon_court_pre` | c412「ペンタゴンの中庭　2025年撮影」 | XQ-58A Valkrie displayed at the Pentagon Cente… | Pfc. Jose Rolando Garcia | 2025-07-15 | A | ○ 8256×5504 | 展示イベントの人（未確認） | 2025年・中庭に無人機の展示（副題は2025年） | △ 「現在の」 |
| `pentagon_west_day` | c421「ペンタゴン西側　2001年9月11日」 | DM-SD-02-03925.JPEG | CPL JASON INGERSOLL, USMC | 2001-09-11 | A | ○ 3600×2362 | 残骸。🔴 Commons のカテゴリに「Remains and debris」＝遺体の写りは未確認（②で原寸） | 当日（9時30分ごろの衝突の後・煙が晴れたあと） | ○ ②で原寸の確認が先 |
| `f15_alert` | c123「待機中のF-15　2024年撮影」 | Fond Farewell to F-15C A5095 (8605970).jpg | U.S. Air Force photo by Airman 1st Class Melany Bermudez | 2024-08-15 | A | ○ 8213×5475 | 整備員（職務） | 2024年・嘉手納の F-15C（オーティスの部隊ではない） | △ イメージ |
| `f15_alert2` | c702「待機するF-15　2020年撮影」 | A 494th EFS F-15E Strike Eagle sits on the fli… | U.S. Air Force photo by Tech. Sgt. Michael Charles | 2020-01-08 | A | ○ 8256×5504 | 未確認 | 2020年・サウジの F-15E（複座の攻撃型） | △ イメージ（型が違う） |
| `f15_takeoff` | c703「離陸するF-15　2023年撮影」 | 391st FS F-15E prepares for takeoff at MCAS Iw… | U.S. Air Force photo by Airman 1st Class Alexandria Byrd | 2023-07-01 | A | ○ 6192×4128 | 整備員（職務） | 2023年・F-15E | △ イメージ（型が違う） |
| `f16_alert` | c707「駐機するF-16　2024年撮影」 | F-16s Arrive at NATO Air Base Geilenkirchen (8… | U.S. Air Force USAFE by Capt. Jose Davis | 2024-05-13 | A | ○ 7008×4672 | なし | 2024年・ドイツの NATO 基地の F-16 | △ イメージ |
| `f16_takeoff` | c711「離陸するF-16　2023年撮影」 | Colorado and Massachusetts Air National Guard … | U.S. Air National Guard photo by Master Sgt. Caila Arahood | 2023-06-12 | A | ○ 4371×2972 | なし | 2023年・リトアニアの州兵の F-16 | △ イメージ |
| `base_rwy` | c708「基地の滑走路　1967年撮影」 | Aerial view of Tan Son Nhut Air Base down main… | Unknown author（NARA 342-B＝米空軍の写真） | 1967-09-26 | A | ○ 3765×2951（上下を切る） | 空撮 | 🔴 別物＝1967年のタンソンニャット空軍基地（ベトナム） | × 差し替え |
| `fighter_dc` | c717「飛行中のF-16　2001年10月撮影」 | F-16C NJ ANG in flight Oct 2001.jpg | U.S. Air Force photo by Master Sgt. Don Taggart | 2001-10-07 | A | ○ 3000×2400（上下を切る） | 機体 | 2001-10-07・ニュージャージー州兵の F-16C の上空警戒（首都の部隊ではない） | ○〜△（副題で部隊を断る） |
| `andrews` | c719「アメリカ空軍の輸送機　2019年撮影」 | 76th AS Last C-40 on ramp.jpg | U.S. Air Force photo by Tech. Sgt. Timothy Moore | 2019-06-06 | A | ○ 6960×4352 | 機体 | 🔴 別物＝2019年・ラムシュタイン（ドイツ）の C-40B（CREDITS で既出） | × 差し替え |
| `wtc_smoke_day` | c313「北棟から上がる煙　2001年9月11日」 | Skyline of Manhattan with smoke billowing from… | 旧版の表記 Mike Goad＝🔴 誤り。撮影者は不詳（議会図書館「撮影者不詳の写真」250枚の1枚・LC-A05-A01）。Mike Goad は Flickr に載せ直した人 | 2001-09-11 | C'（撮影者が権利を放棄＝議会図書館の説明） | ○ 2500×1666 | 遠景・人なし | 当日。⚠️ 題は「両棟から煙」＝両棟が燃えている絵なら 9:03 より後＝旧版の c313（9:03 より前の場面）と食い違う恐れ（未見） | ○ ②で絵の時刻を確かめる |
| `fire_trucks_day` | c314「現場へ向かう消防車　2001年9月11日」 | LOC unattributed Ground Zero photos, September… | Anonymous. Courtesy of the Prints and Photographs Division.（議会図書館・LC-A05-F35） | 2001-09-11 | C'（同上） | ○ 4086×2774 | 消防士（職務） | 🔴 説明＝「燃える第7ビル（7 WTC）」「午前10時〜午後1時30分ごろの撮影」→ 旧版は c314「街の目は、北棟に集まった」（8:46〜9:03 の場面）に「現場へ向かう消防車」と副題＝時刻も中身も食い違う | ○ 時刻の合う場面に移す（副題は「燃える第7ビル　午前10時以降」） |
| `shanksville_day` | c622「93便が落ちた野原　2015年撮影」 | Flight 93 Memorial - panoramio (1).jpg | Ron Shawley | 2015-10-17 | F（BY） | ○ 5184×3456 | 来訪者（私人）の可能性 | 2015年の追悼施設（副題は2015年と断っていた） | ○ 「現在の」 |
| `apron_day` | pr10「駐機場に並ぶ旅客機　2017年撮影」 | Southwest 737s parked at Terminal A at DCA (39… | airbus777 from Washington, DC, USA | 2017-11-14 | F（BY） | ○ 5447×2825 | 機体 | 2017年のレーガン空港（当日の画として冒頭 pr10 に） | △ イメージ |
| `apron_lined_day` | c516・ep05「駐機場に並ぶ旅客機　2026年撮影」 | At gate B24 at Boston Logan International Airp… | 4300streetcar | 2026-01-28 | F（BY） | ○ 8256×5504 | 機体 | 2026年のボストン（当日の画として） | △ イメージ |
| `stopped_day` | c505「搭乗口で待つ旅客機　2023年撮影」 | United Boeing 737 at Gate B25 at Boston Septem… | 4300streetcar | 2023-09-12 | F（BY） | ○ 5568×3712 | 機体 | 2023年のボストン | △ イメージ |
| `stranded_day` | c517「空港の待合室　2017年撮影」 | Philadelphia Airport Lounge (36335419103).jpg | Nelo Hotsuma | 2017-05-07 | F（BY） | ○ 6000×4000 | 私人の可能性 | 2017年のフィラデルフィア空港 | △ イメージ |
| `hearing` | c807「アメリカ議会の公聴会　2012年撮影」 | Congressional Hearing - Jul. 24, 2012 (7748554… | Nuclear Regulatory Commission from US | 2012-07-24 | A（NRC・Flickr は CC BY の札） | △ 縦長 3240×5064 | 委員長（公職）＋傍聴者 | 🔴 別物＝2012年・原子力規制委員会の議会公聴会（9.11 委員会ではない） | × 差し替え |
| `library_reports` | c815「図書館の書架　2025年撮影」 | Books, Community Languages, Takapuna Library.j… | Bjankuloski06 | 2025-01-29 | F（BY） | ○ 6000×4000 | なし | 🔴 別物＝2025年・ニュージーランドの図書館 | × 差し替え |
| `recorder` | c805「飛行記録装置　2019年撮影」 | Miami Air Flight 293 flight recorder (32830135… | National Transportation Safety Board | 2019-05-04 | A | ○ 5472×3648 | NTSB 調査官（職務） | 🔴 別物＝2019年のマイアミ航空293便の記録装置 | × 差し替え |
| `atc_tape` | c803「オープンリールの録音機　1978年ごろの機種」 | Studer B67 reel-to-reel audio tape recorder, c… | Robert Taylor from Stirling, ON, Canada | 2013-08-07 | F（BY） | △ 縦長 2530×2560 | なし | 1978年ごろの機種のスタジオ用録音機（FAA の録音機ではない） | △ イメージ |
| `logbook` | c809「飛行記録簿　1943年の手書き」 | Billy Strachan log book.jpg | The History Wizard of Cambridge | 2023-05-30 | C | ○ 4032×3024（上下を切る） | 展示物 | 🔴 別物＝第二次大戦の英空軍の操縦士の記録簿（博物館） | × 差し替え |
| `security_now` | c901「空港の保安検査の列　2016年撮影」 | 0083 Domodedovo International Airport 16th of … | Rakoon | 2016-08-16 | C | ○ 4948×3280 | 検査の列（私人） | 🔴 別物＝2016年・モスクワのドモジェドボ空港（米国の運輸保安庁の話に） | × 差し替え |
| `security_screen` | （本編では未使用） | 2016 04 19 Airport Security-5 (26744283185).jpg | AMISOM Public Information | 2016-04-19 | C | ○ 4388×2921 | 保安職員（職務） | 🔴 別物＝2016年・ソマリアのモガディシュ空港 | × 使わない |
| `artcc_now` | c905「今の航空管制の卓　2025年撮影」 | 378th EOSS Air Traffic Controller Demonstratio… | U.S. Air Force AFCENT by Staff Sgt. Shaei Rodriguez | 2025-01-06 | A | ○ 8448×6336（上下を切る） | 軍の管制官（職務） | 🔴 別物＝2025年・中東の米空軍の管制塔 | × 差し替え |
| `lobby_now` | c907「今の空港の出発ロビー　2018年撮影」 | Gillette–Campbell County Airport terminal inte… | Mr. Satterly | 2018-05-15 | C | ○ 5472×3648 | 未確認 | 2018年・ワイオミング州の地方空港 | △ イメージ |
| `clear_sky` | ep01「空　2025年撮影」 | 20250928 View from aircraft in Turkey 01 (7996… | Sergey A. Demidov | 2025-09-28 | F（BY） | ○ 8160×4592 | なし | 2025年・トルコ上空の機窓（「その朝は晴れていた」の画） | △ イメージ |

## 4. 写真の在庫の当たり（帳簿 7本目の行 `material`＝2026-09-13 からの変化）
- 測り方：旧版①の深さを決めたカテゴリ歩き（`material_photo.json`）は、今回 Commons の 429（問い合わせが多すぎる）が続いて40分で止めた（途中の値は使わない）。代わりに Commons の検索の件数（`deepcat:`＝下のカテゴリを深さ5まで含む・`filew:>1919`＝幅1920以上・`incategory:`＝米連邦の札のカテゴリ17種のどれか）で**当たり**を取った（生の値＝`src/materials_raw/inv_search*.out`）。⚠️ 深さが違う＝旧版の数と同じ物差しではない。

| 物差し | 2026-10-11 | 幅1920以上 | うち米連邦の札（A） | 旧版①（09-13）の値 |
|---|---:|---:|---:|---|
| 撮影日のカテゴリ「United States photographs taken on **2001-09-11**」以下 | 1,938 | 1,185 | 723（🔴 うち議会図書館の 250点は札が誤り＝下の注）→ **実質 473** | 「当日」529（分類のやり方が違う） |
| 同 2001-09-12 | 203 | 67 | 67 | — |
| 同 2001-09-13 | 68 | 31 | 30 | — |
| 同 2001-09-14 | 99 | 42 | 38 | — |
| `deepcat:`「September 11 attacks at the World Trade Center」 | 12,522 | 9,978 | 1,780 | 深さ3で 1,548（後年・追悼を含むかが違う） |
| `deepcat:`「September 11 attacks at the Pentagon」 | 4,089 | 3,032 | 1,498 | 深さ3で 1,537（＋「Aftermath of 9/11 at the Pentagon」3,171） |
| `deepcat:`「United Airlines Flight 93」 | 750 | 551 | 23 | 深さ2で 251 |
| 「Library of Congress images of the September 11 attacks」 | 251 | 251 | 250（札の誤り） | 251 |

- 🔴 **議会図書館の 9.11 の 250点（LC-A05・GWToolset の一括アップロード）は Commons の札が「PD US Government」だが、議会図書館の説明では撮影者不詳の個人が権利を放棄した写真＝A ではなく C'**（§2-12「札と著者を一緒に見る」）。出典は「米議会図書館蔵（撮影者不詳）」と書く。旧版の `wtc_smoke_day`・`fire_trucks_day` はこの束の写し。WTC の当日（衝突〜崩落）を全面で受ける写真の主力。
- 見立て：**当日9月11日・幅1920以上・本当に A の写真は 約470点**、9/12〜9/14 で 約135点。旧版①の「当日529点」から大きく減ってはいない（物差しが違うので増減は言えない）。写真の 20%（§2-1）を当日の写真で満たす量はある。
- 外の候補（数えていない＝②で）：NASA の宇宙ステーション（第3次長期滞在）が当日撮ったニューヨークの煙の写真（A）／FEMA の Andrea Booher ほかの写真（A・9/13〜）／FBI のペンタゴンの写真（A）。
- 4機の事故の前の写真（帳簿の値・今回は測り直していない）：AA11 N334AA＝CC BY-SA 3.0（3767×2511）／AA77 N644AA＝GFDL 1.2 ほか（1280×850）／UA93 N591UA＝CC BY 2.0 ほか（1690×1078）／UA175 N612UA＝GFDL 1.2（1024×761）。今のルールでは BY-SA も使える（額装・無加工＝画面いっぱいの例外）。⚠️ GFDL だけの点は全文の添付が要る＝動画に向かない＝CC との二重の札かを②で確かめる。

## 5. 人の声の記録（参考・使うかは親が決める）
| 系列 | 点数（2026-10-11） | 旧版①（09-13） | use | access | 中身 |
|---|---:|---:|---|---|---|
| NARA RG148（委員会）4319604 | 26（音 25・画像 1） | 25 | **Unrestricted** | **Unrestricted** | [AAL 77] ワシントン航空路管制センターの認証つき再録音（1便・1センターぶん） |
| NARA RG148 5952561 | **272**（音 236・データ 34・文書 2） | 342 | Unrestricted | Unrestricted 203／Restricted - Partly 69 | 委員会の聞き取り（Team 8）＝FAA・NORAD の職員への聞き取り |
| NARA RG237（FAA）7419198 の音 | **1,042** | 770 | Unrestricted | Restricted - Possibly（FAA の黒塗りの注記） | 管制の録音（N47BA＝1999年を含む） |
- **旧版①の読み「全点 use=Unrestricted・§105」は今も正しい**。点数の変化は目録の付け直しの見込み（理由は未確認）。音を新しく起こす工程がこの ch に無い＝使えるのは活字になった逐語（委員会報告 第1章）という旧版の結論は変わらない。
- **UA93 の CVR**：裁判所（米国 対 ムサウイ）の証拠の頁は 2026-10-11 に **404**（旧の場所が消えた）。旧版①の写し（09-13・`analytics/materials/ep7/moussaoui_prosecution.html`）では P200056（CVR の音を含む提示）は「封印（under seal）」・逐語 P200056T は公開。封印が解かれた記録は見つけていない（探したのは裁判所の頁だけ）。
- **機内からの電話**：録ったのは航空会社（私企業）と通信指令（市）＝§105 の外＝使わない（旧版①の読みのまま）。
- Commons「September 11, 2001 ATC in real time (FAA-NORAD audio).ogv」（1280×720・1時間51分・YouTube から）：札は「FAA and NORAD」の PD だが、画面と編集をしたのは YouTube の投稿者（中身は未確認）＝音の出どころを NARA の原本に当て直すまで使わない。

## 6. 確かめていないこと（映像方針で測るもの）
1. **全部の動く実写の実効の幅**（DVIDS の High-Res の原本は要ログイン＝未測。プレーヤーの mp4 は 640×480）。WHCA の 16:9 の器（SAR 40:33）は本物の 16:9 か、4:3 の左右に黒か。
2. **中身を1秒1コマで**（特に DVIDS `122342`・`122343`・`734981`・WHTV 600 の遺体・担架・負傷者／小学校のテープの耳打ちの秒と子どもの顔／退避のテープの私人の近景）。焼き込みの文字（題のカード・局のロゴ）。
3. NARA のオフラインの RG330・RG311 を取り寄せるか（費用＝要相談）。
4. 『平成１３年防衛庁記録』03:48〜04:22 の画の出どころ。
5. `wtc_smoke_day` の絵の時刻（両棟か）・`pentagon_west_day` の遺体・`wtc_twin`（1971年＝建設中か）。
6. 「World trade center.ogv」（1976）の PD の根拠。
7. DVIDS は題の語で引いた＝全文の網ではない（ほかにも 2001年の映像がある見込み）。大統領図書館の YouTube のほかの WHTV（9/11〜9/20）も検索で引いた範囲だけ。
8. 在庫（§4）は検索の件数の当たりだけ（旧版①と同じカテゴリ歩きは Commons の 429 で止めた）＝撮影日のカテゴリに入っていない当日の写真・札の誤り（議会図書館の束のほかにもありうる）は数えていない。
9. ⚠️ この `ref/ep21/` は `.gitignore` の `ref/*` の下＝commit するときは許可の行か `git add -f` が要る（親が決める）。`src/materials_raw/` は git に入れない。
