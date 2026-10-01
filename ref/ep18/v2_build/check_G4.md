# ④' 検査 G4（18本目 スレッシャー号・台本 第1版）

- 担当の行＝`ref/ep18/daihon_v1.md` 924〜1139行（第7章 c701〜c723・第8章 c801〜c823）。見るだけ・台本は1文字も触っていない
- 見た行の数＝**164行**（空行を除く全行＝章見出し2・前置きの注2・カットの見出し46・字幕の行112〈うち聞き役12・★3〉・区切り2）
- 判定の内訳（行）＝OK 114／🔴 5／⚠️ 28／・ 17
- 所見の数＝**31件**（🔴2・⚠️15・・14）＝`findings_G4.json`（items 45件＝§1-3・§1-5・§1-6・§1-7・§1-8・§1-9・§1-11・§2・§9-1 の担当分）
- 🔴 の2件＝**G4-12**（c715★＝「ティノサの」「試験で」が★にも前の行にも無く、スレッシャーのこし器が30秒で破れたと読める）・**G4-28**（c820＝「どの見方も一致…凍って吹き出せなかった」。査問会は「おそらく・凍りやすい／凍った減圧弁か電気の故障」、艦隊司令官は系統の性質まで＝当日の凍結を言うのはルール氏だけ。元は legend §2 L1 の判定）
- 引いた原文の範囲＝R08 p.16・25〜26・32〜33（証言）／R08 p.189〜191・204〜206・211〜215（認定38・46〜51・意見1〜10・36〜51）／V1 p.42〜44・49〜50・57〜58・64〜67・71（kwic の当たり・見えない頁は R08 で当てた）／IR18 p.1・5〜6・18〜23・48・67・120〜123／J 前付 p.7901〜7913（回の日付）・J p.31〜32・34〜35・37〜38・83・88〜89・111〜112／T p9801・p9802（R17 p.97 の要旨）／A-R（ルール氏の書簡の I. SUMMARY・II. BACKGROUND の頭＝住所の行は写していない）／J・D・NAVSEA・T（潜るときに海水を入れる説明＝0件）
- 回の日付（J 前付 p.7913 の表と本文の見出し）＝1963-06-26 p.1〜／06-27 p.29〜58（p.32・35・37・38）／07-23 p.59〜90（p.83・89）／1964-07-01 p.91〜（p.111・112）＝画の欄の日付は全部合う
- 形の機械検査（このチャットの scratchpad で数えた）＝字幕の行は全部41字以下・★3件は20字以内で最後の行・語りに「〜」なし・聞き役12行に数字なし・死の語／煽り語なし
- 見えない頁：担当の出典欄の V1 p.44（認定50）は見えない頁＝R08 p.191 で当てた。V1 p.57（意見2）は見える頁。証言の見えない頁（p102・128・136・145・197〜199・211）は担当に無い
- 道具＝`python ref/ep18/v2_build/kwic.py -f ref/ep18/v2_build/q_G4.txt` と頁の丸ごと表示（scratchpad の `pg4.py`＝同じ `ref/ep18/src/ep18_pages.txt` を頁ごとに出すだけ）
- 画像は1枚も読んでいない（写りの確認が要るもの＝G4-21 c805 thr_t33・c819 thr_t23 の札＝⑤bで原寸）

## 第7章（924〜1030行）

| 行 | 判定 | 原文の頁と短い引用（30〜80字） |
|---|---|---|
| 924 章見出し | OK | 章名「30秒」＝§3。認定50 "in about thirty seconds"（R08 p.191） |
| 926 注 | OK | 方針（決め所＝ティノサのこし器・認定51＝別の30秒）は R08 p.191 の2つの30秒と合う。ただし★で「ティノサ」が落ちた（G4-12） |
| c701-928 見出し | ⚠️ | 出典欄「意見1d」に吹き出しの仕組みの説明は無い。J p.32 注 "provide air in order to displace water from the ship's ballast tanks thereby increasing buoyancy"（G4-01） |
| c701-929 | ⚠️ | 「主タンクに海水を入れて沈み」は引いた資料に無い（J・D・NAVSEA・T で0件）＝一般の知識（G4-01） |
| c701-930 | OK | J p.32 注 "displace water from the ship's ballast tanks thereby increasing buoyancy" |
| c702-932 見出し | ⚠️ | 画の順「減圧弁 → こし器」。原文はこし器が減圧弁の中：認定49 "reducing valves ... were fitted with conical mesh strainers"（R08 p.190）（G4-02） |
| c702-933 | ・ | 「圧力を下げる弁」＝reducing valves で OK。「減圧弁」の語がここで出ず c715 で初めて出る（G4-03）。J p.35 "your reducers pulled it down" |
| c702-934 | ⚠️ | 「弁の手前には」は原文に無い位置。認定50 "strainers in the reducers"・意見8c "at the conical strainers in the reducing valves"（R08 p.205）（G4-02） |
| c703-936 見出し | OK | 認定46 "a. An increase in test depth from 700 feet to [空白] b. About the same reserve buoyancy c. About the same high pressure air bank capacity" |
| c703-937 | OK | 認定46 "SKIPJACK, the immediately preceding class ... from 700 feet"（700×0.3048＝213.4m→約210） |
| c703-938 | OK | 認定46c "About the same high pressure air bank capacity" |
| c704-940 見出し | OK | 認定46d "(1) A reduction in the amount of ballast which could be blown ... (2) A reduction in the rate of blowing"＝数は b(1) の空白 |
| c704-941 | ・ | 事実は OK。「そのため」の因果は認定46 に無い（a〜d の並列）（G4-04） |
| c704-942 | OK | R08 p.190 "from [空白] per cent to [空白] per cent"＝b(1) で塗り |
| c704-943 Q | OK | 反応（roles.tsv）。c703 の言い直し・数字なし |
| c705-945 見出し | OK | 認定47（R08 p.190） |
| c705-946 | OK | 認定47 "the increasing operating depths of submarines has compressed the time available ... to take effective damage control action with respect to flooding" |
| c705-947 | ⚠️ | 認定47 "The shortness of time available to control flooding is not well recognized"＝事実は OK・「分かられていなかった」が不自然（G4-05） |
| c706-949 見出し | OK | 認定48 "blow all main ballast tanks twice at periscope depth ... no modification to this criteria for depth ... Dehydrators were not installed" |
| c706-950 Q | OK | 質問 → 次の語り「あった。」がそのまま答える |
| c706-951 | ・ | 認定48 "capability to blow all main ballast tanks twice at periscope depth"＝OK。行末の「ただ、」（G4-06） |
| c706-952 | OK | 認定48 "no modification to this criteria for depth of blowing ... no requirements ... which would prevent the formation of blockages due to ice" |
| c707-954 見出し | OK | J p.32 "your temperature drops down well below freezing"・認定48 "Dehydrators were not installed" |
| c707-955 | OK | J p.32 Brockett "this drop in temperature immediately when your upstream pressure is two times or more greater than your downstream" |
| c707-956 | OK | 認定50 "frozen moisture from the air system"（R08 p.191）／認定48 "Dehydrators were not installed" |
| c708-958 見出し | OK | J p.32（1963-06-27の回＝J前付 p.7913 の日付表で p.29〜58）"Depth is not significant insofar as freezeup is concerned" |
| c708-959 | OK | 同上（艦船局の長＝ブロケット少将・役で呼ぶ＝§1-3） |
| c708-960 | OK | J p.32 "upstream pressure is two times or more greater than your downstream"・J p.35 "It is a matter of pressure differential" |
| c709-962 見出し | ・ | R08 p.26 の証人は R08 p.16 "Captain Clarence J. Zurcher"（綴り＝ズーカー？）。写真 1961-07-24 は試運転（4/30〜5/2）の後（G4-07） |
| c709-963 | ・ | 年は認定38（R08 p.189）"Initial sea trials were held on 30 April 1961 to 2 May 1961"＝出典欄に無い。"until about 2:00 o'clock on the morning that we sailed at 6:00"＝2時「ごろ」（G4-07） |
| c709-964 | OK | R08 p.26 "a meeting on the barge ... Admiral Moore, Admiral Rickover, Admiral Palmer, the skipper, and myself" |
| c710-966 見出し | OK | R08 p.26 "we were all for having them in high, because we knew air was very questionable" |
| c710-967 | OK | R08 p.26 "what would happen if we flooded any one area from 700 feet down ... getting back to the pump speed" |
| c710-968 | OK | R08 p.26 "how much good it would do at that depth" |
| c710-969 | OK | R08 p.26 "because we knew air was very questionable"（その場にいた大佐＝"myself"） |
| c711-971 見出し | ⚠️ | 画の欄「やめた」＝原文は "it was decided that this would not be prudent"（試さないと決めた）（G4-08） |
| c711-972 Q | ⚠️ | 質問。J p.35 Brockett "a test depth requirement ... with the valves open to make sure air went through ... As soon as you got a bubble you stopped"＝短い吹き出しはあった（G4-08） |
| c711-973 | ⚠️ | R08 p.33 Jackson "after some discussion it was decided that this would not be prudent"・"the reason they concluded not to try it"＝決めたのは話し合い（G4-08） |
| c711-974 | OK | R08 p.33 "the air would expand, de-water the tanks more rapidly ... faster than you could vent it out"・"uncontrolled ascent" |
| c712-976 見出し | OK | J p.38（1963-06-27）＝§7 の文字の頁 p8038 |
| c712-977 | ・ | J p.38 Holifield "if you can make a full deballast against the pressure at that depth?"（G4-09） |
| c712-978 | ・ | J p.38 "As I understand it, it never has been done. / Admiral Maurer. That is right, sir."＝事実 OK・「理解している」の主語が語り手に読める（G4-09）／J p.37 の食い違い（G4-10） |
| c713-980 見出し | ⚠️ | 画の欄も主語「海軍は」が無い（G4-11）。J p.83 "That doesn't seem right to me."／"This isn't right." |
| c713-981 | ⚠️ | J p.83 "the Navy from the time of the 400-foot submarine ... did not basically change the blowing requirements as they went deeper"＝主語が落ちた（G4-11）。400×0.3048＝121.9m |
| c713-982 | ⚠️ | 同上（basically を落とした）（G4-11） |
| c713-983 | ⚠️ | 行頭の「と述べた。」＝不自然な改行（G4-11）。議員と中将のやりとりは J p.83 どおり |
| c714-985 見出し | OK | J p.32 注 "dockside tests were conducted of an identical high-pressure air system aboard the Tinosa, sister ship to Thresher" |
| c714-986 | OK | 認定50 "Under a test required by the court"（R08 p.191）・J p.32 注 "Subsequent to the lose of Thresher" |
| c714-987 | OK | J p.32 注 "The Tinosa was nearing completion at the Portsmouth Naval Shipyard" |
| c715-989 見出し | OK | 認定50 R08 p.191（V1 p.44 は見えない頁＝R08 で当てた） |
| c715-990 | 🔴 | 「減圧弁のこし器は」＝どの艦のこし器かが無い（G4-12） |
| c715-991 ★ | 🔴 | 認定50 "strainers in the reducers of the TINOSA were blocked and ruptured by the formation of ice in about thirty seconds"＝★に「ティノサ」も「試験」も無い（G4-12） |
| c716-993 見出し | OK | J p.32 注 "ice formed on the screen-type wire strainers in the air piping system cutting off air flow to the ballast tanks" |
| c716-994 | ⚠️ | 同注 "During the tests, ice formed ..."＝試験の話と示されない（G4-13） |
| c716-995 | OK | J p.32・p.112 の同じ注（公刊時の注） |
| c716-996 Q | ⚠️ | まとめ。次の c717 が「そう。」で受ける＝形は OK。中身は G4-13 と同じ根（ティノサが無い） |
| c717-998 見出し | OK | 認定51 "air banks 2, 3 and 4 would automatically be shut off and air bank #1 would be opened up slowly ... 10-50 seconds" |
| c717-999 | OK | 認定51（R08 p.191）＝認定50 とは別の30秒 |
| c717-1000 | OK | 認定51 "in event of loss of electrical power to the ballast control panel, air banks 2, 3 and 4 would automatically be shut off" |
| c717-1001 | ⚠️ | 認定51 "It takes thirty seconds to get valves fully open again"＝設計の説明→「かかった」は当日の出来事に読める（G4-14） |
| c718-1003 見出し | OK | 意見38k（R08 p.211） |
| c718-1004 | OK | 意見38k "The fail-closed concept for the three air banks ... is not desirable for safety of the ship at test depth" |
| c718-1005 | OK | 意見38k "should be modified to provide fail-on-the-line; i.e., air bank valves open" |
| c719-1007 見出し | OK | 意見45（R08 p.212）"If the main coolant pumps stopped, there would have been an automatic reactor shutdown ... about 5 knots" |
| c719-1008 Q | ⚠️ | 質問。答えは条件の場合だけ＝前提 "It is known, without much doubt, that at 0911R the main coolant pumps ... either stopped or were slowed" を落とした（G4-15） |
| c719-1009 | ⚠️ | 意見45 "If the main coolant pumps stopped, there would have been an automatic reactor shutdown (SCRAM)"＝条件は残った（G4-15） |
| c719-1010 | ⚠️ | R08 p.213 Case I "Power lost at 0911R when pumps stop ... showed it to be not highly probable"＝評価を落とした（G4-15） |
| c720-1012 見出し | OK | 意見45 "the 7.1 minutes between 0911R and time of collapse depth" |
| c720-1013 | OK | 意見45 "no normal main propulsion power available until after the 7.1 minutes between 0911R and time of collapse depth" |
| c720-1014 | OK | 同上 |
| c720-1015 | OK | 意見45 "Emergency Propulsion Motor which could be run from the battery ... only sufficient for about 5 knots"（5×1.852＝9.26） |
| c721-1017 見出し | OK | J p.111〜112（1964-07-01＝J p.91 の見出し "WEDNESDAY, JULY 1, 1964" から後）＝§7 の文字の頁 p8112 |
| c721-1018 | OK | J p.112 Bates（議員）"Did you ever blow at all—even at dockside—to the maximum degree before this happened to the Thresher?" |
| c721-1019 | OK | J p.112 Curtze（少将）"I don't know. I don't think so."＝推測のまま（G4-10 の食い違いは・） |
| c722-1021 見出し | ⚠️ | 画 thr_t37＝海の底の空気のボンベ（materials L73「因果は言わない」）。語り「外していなかった」と並んで原因と結びつく（G4-17） |
| c722-1022 | ・ | J p.35 "The strainers were removed ... After the Tinosa"・J p.112 Curtze "If my memory is correct, I think ... we had written orders to take them out and it hadn't been done yet"（G4-16） |
| c722-1023 | ・ | J p.112 Kern（大佐）"We don't believe they were."・"Certain strainers remained. Others came out."（G4-16） |
| c723-1025 見出し | OK | 意見39（R08 p.211） |
| c723-1026 | OK | 意見39 "the high pressure blow of submarine main ballast tanks needs to be tested" |
| c723-1027 | ・ | 意見39 "under conditions simulating a full blow at test depth"＝「全力で」は full blow（吹き切る）とずれる（G4-18） |
| c723-1028 Q | OK | 質問 → c801「査問会の答えは、意見の1番にある…おそらく、4つが重なった」が答える（章をまたぐ橋） |
| 1030 区切り | OK | — |

## 第8章（1032〜1138行）

| 行 | 判定 | 原文の頁と短い引用（30〜80字） |
|---|---|---|
| 1032 章見出し | OK | 章名「原因は決まっていない」＝§3。IR18 p.1 段落3 "has not been determined"・p.5 段落11 |
| 1034 注 | OK | 方針（査問会の結論を噂扱いしない・ルール氏は帰属・海の底の写真を原因と結びつけない）は §1-9・§5b-74③ と合う |
| c801-1036 見出し | OK | 意見1 a〜d（R08 p.204）"orifice between 2" and 5" ... electrically-induced automatic shutdown ... Inadequate operating procedures ... deficient air system" |
| c801-1037 | OK | 意見1 "That the loss of the U.S.S. THRESHER was in all probability due to" |
| c801-1038 | OK | 意見1 "in all probability"＝おそらく・"which continued, compounded by"＝重なった |
| c802-1040 見出し | OK | 意見1a・b（R08 p.204） |
| c802-1041 | OK | 意見1a "An initial flooding casualty from an orifice between 2" and 5" in size in the engine room"（5.08〜12.7cm） |
| c802-1042 | OK | 意見1b "Loss of reactor power due to an electrically-induced automatic shutdown" |
| c803-1044 見出し | OK | 意見1c・d（R08 p.204） |
| c803-1045 | OK | 意見1c "Inadequate operating procedures with respect to minimizing the effects of a flooding casualty and the loss of reactor power" |
| c803-1046 | OK | 意見1d "A deficient air system, susceptible to freeze-up, with low capacity and low blow rate" |
| c803-1047 Q | OK | まとめ。語りが4つを言い終えた直後・次の c804 が「そう。」で受ける |
| c804-1049 見出し | OK | 意見45 Case III（R08 p.214）"both flooding and full speed ... occur 1.5 minutes earlier"＝9:09 ごろ |
| c804-1050 | OK | 意見45 "From the many computer solutions there emerge three which bracket the probable actual situation"（R08 p.212） |
| c804-1051 | OK | R08 p.214 "This is the most probable approximation of the sequence of events" |
| c804-1052 | OK | R08 p.214 "just prior to the sending of the "Minor difficulties..." message at 0913R, depth would have been reduced to about 750 feet"（228.6m） |
| c805-1054 見出し | ・ | 画 thr_t33 は materials L70 の t29〜t34（frame 78 の切れ目・上甲板・艦尾の係留金具）の1枚＝どこの写りかは⑤bで原寸（G4-21）。出典 意見45 は OK |
| c805-1055 | OK | R08 p.212 "the specific nature of the THRESHER loss cannot be determined by assumptions and computer solutions based on those assumptions" |
| c805-1056 | OK | R08 p.212 "It is impossible, with the information now available, to obtain a more precise determination of what actually happened" |
| c805-1057 | ⚠️ | 行頭の「と。」（G4-20）。"in an effort to determine the parameters of the unknown factors, such as size of leak"＝事実は OK |
| c806-1059 見出し | OK | 意見5 "That a flooding casualty in THRESHER could have resulted from: a〜f"（R08 p.204） |
| c806-1060 Q | OK | 質問 → 次の語り「1つに決めていない」がそのまま答える |
| c806-1061 | OK | 意見5 "could have resulted from"＝並列。R08 p.204〜216 の意見に sil-braze を1つに絞る文は無い（kwic） |
| c806-1062 | OK | 意見5 a〜f＝6つ |
| c807-1064 見出し | OK | 意見5 a〜f |
| c807-1065 | OK | 意見5 "a. A faulty sil-braze joint. b. Undiscovered shock damage. c. A flexible hose failure." |
| c807-1066 | OK | 意見5 "d. A casting or piping failure. e. A minor hull failure. f. Unknowns, including component failure." |
| c808-1068 見出し | OK | 意見5・legend §2 L1（通説「銀ろう継手が破れて浸水…」） |
| c808-1069 Q | OK | まとめ（6つの候補を聞いた直後）・次が「そう。」 |
| c808-1070 | ⚠️ | 「よくそう語られる」の「そう」が直前の聞き役「決まったわけじゃない」を指して逆に読める・通説の中身が音に出ない（G4-22） |
| c808-1071 | OK | 意見5a "A faulty sil-braze joint"＝6つの1つ |
| c809-1073 見出し | OK | 意見2（R08 p.204） |
| c809-1074 | OK | 意見2 は意見1 のすぐ後＝「結論に添えた」で可 |
| c809-1075 | ⚠️ | 意見2 "there is a danger that ... conjecture may be stretched too far ... thus narrowing the field of search"＝「狭めてしまう」と断定（G4-23） |
| c810-1077 見出し | OK | 意見2（V1 p.57＝見える頁・R08 p.204） |
| c810-1078 | OK | 同上 |
| c810-1079 ★ | OK | 意見2 "conjecture may be stretched too far and become accepted as fact"＝danger・may を「おそれ」で残した（意味 OK） |
| c811-1081 見出し | ⚠️ | 画の欄も「深く調べるには十分なことが分かっている」（G4-24） |
| c811-1082 | OK | 意見49（R08 p.215）"although we may never learn the exact cause of the tragic loss of THRESHER" |
| c811-1083 | ⚠️ | 意見49 "we do know enough to make it necessary for us to explore in depth the many possible causes"＝必要→十分・possible を落とした（G4-24） |
| c811-1084 Q | ・ | 反応。「査問会も」の「も」の相手が前に無い（c805〜c811 は全部査問会）（G4-25） |
| c812-1086 見出し | OK | IR18 p.5〜6（1965-03-19）・画 thr_t29＝materials L70（frame 78 の切れ目を真上から） |
| c812-1087 | OK | IR18 p.5 "has not been determined despite the most thorough investigative efforts by the Navy and the Joint Atomic Energy Committee of the Congress" |
| c812-1088 | OK | IR18 p.5〜6 "Probably ... the cause will never be known" |
| c813-1090 見出し | OK | IR18 p.6 "whether faulty design, structural or mechanical failure or malfunction or personnel error set in motion the chain of events" |
| c813-1091 | ・ | 同上。行末の「どれが、」（G4-26） |
| c813-1092 | OK | IR18 p.6 "set in motion the chain of events which led to eventual catastrophe"・"will never know" |
| c814-1094 見出し | OK | J p.89（1963-07-23・"this concludes my prepared testimony"）＝§7 の文字の頁 p8089 |
| c814-1095 | OK | J p.89 "My views sum up as follows"＝声明の結び |
| c814-1096 | OK | J p.89 "(a) There is insufficient information to pin down what really happened to the Thresher." |
| c815-1098 見出し | OK | J p.89 |
| c815-1099 | OK | J p.89 "I do not know."（直後の文） |
| c815-1100 ★ | OK | J p.89 "insufficient information to pin down what really happened ... I do not know."＝2文を1つにした・意味は同じ |
| c816-1102 見出し | OK | J p.89 "(b) I do know there were weaknesses in her design, fabrication, and inspection that must be corrected" |
| c816-1103 | OK | 同上 |
| c816-1104 | OK | 同上 "that must be corrected" |
| c816-1105 Q | OK | まとめ（(a)(b) の直後）・次の c817 が「そう。」 |
| c817-1107 見出し | ・ | 画の欄の「浸水は無かった」は A-R "no flooding prior to collapse" の範囲が落ちる（G4-27 と同じ根）。「2013年の書簡＝個人の推定」の帰属は OK |
| c817-1108 | OK | A-R "As the Analysis Officer at the SOSUS Evaluation Center in April 1963" |
| c817-1109 | OK | 同上＝肩書（評価センターで分析の担当）は本人の言い方と合う |
| c817-1110 | OK | A-R 2013-04-10・宛先は海軍作戦部の少将（OPNAV）＝海軍に宛てた。COI の浸水の説を退ける筋書き |
| c818-1112 見出し | ⚠️ | 画の欄「浸水は無かった」も "prior to collapse" が落ちる（G4-27） |
| c818-1113 | ⚠️ | A-R "the initial casualty ... was the failure at 0911"＝OK。行末の「9時11分の、」＝不自然な改行（G4-27） |
| c818-1114 | ⚠️ | A-R "shut down the submarine's Main Coolant Pumps (MCPs) resulting in the immediate scram"＝A-R どおり。ただ2文目「ポンプが止まり、原子炉が止まった。」に帰属が掛からない（G4-27） |
| c818-1115 | ⚠️ | A-R "Multiple, independent lines of evidence confirm there was no flooding prior to collapse"＝「押しつぶされるまで」が落ちた（G4-27） |
| c819-1117 見出し | ・ | 画 thr_t23＝materials L68（艦尾の frame 103 のつぶれた所）。「どっちが正しい」の問いと並ぶ＝札を切り原因と結びつけない（§5b-74③）を⑤bで確かめる |
| c819-1118 Q | OK | 質問 → 「記録からは、決められない。」がそのまま答える |
| c819-1119 | OK | どちらも正しいとは言わない（意見1 "in all probability"・A-R は個人） |
| c819-1120 | OK | A-R は個人の書簡＝帰属 |
| c820-1122 見出し | 🔴 | 画の欄「3つの見方が一致＝空気の系統が凍り、吹き出せなかった」（G4-28） |
| c820-1123 | 🔴 | 「どの見方も」＝この章の海軍長官 "Probably the cause will never be known"・中将 "I do not know" まで含んで読める（G4-28） |
| c820-1124 | 🔴 | 意見1d "susceptible to freeze-up"（in all probability）・意見45 "a frozen reducer at 0911.3R or an electrical failure"・IR18 p.122 "susceptible to freeze-up"＝当日に凍って吹き出せなかったとは書いていない（G4-28） |
| c821-1126 見出し | OK | IR18 p.122 "This grossly unsatisfactory situation ... remove high pressure air reducer strainers"・日付 IR18 p.120 "12 June 1963 FIRST ENDORSEMENT" |
| c821-1127 | OK | IR18 p.120 "12 June 1963" |
| c821-1128 | ・ | IR18 p.122 "Immediate steps have been taken in operating ships to: (1) remove high pressure air reducer strainers"＝OK。「動いている艦」（G4-29） |
| c822-1130 見出し | OK | R17 p.97 の要旨（p9802）・画 thr_t30＝materials L70（frame 78 の前の上甲板） |
| c822-1131 | OK | p9802 "succeeded in photographing, as far as appears possible, all of the THRESHER hulk pieces still visible above the ocean floor" |
| c822-1132 | ・ | 2文目は p9802 に無い評価（帰属なし）＝§5b-74③ には沿う（G4-30） |
| c823-1134 見出し | OK | 橋のカット（出典なし＝要らない） |
| c823-1135 | OK | 意見1・意見49・IR18 p.5（原因未決）／第9章の塗り |
| c823-1136 | OK | 第9章への橋。噂は c901 で「噂」と言う |
| 1138 区切り | OK | — |
