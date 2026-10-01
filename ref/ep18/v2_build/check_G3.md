# ④' 検査 G3（18本目 スレッシャー号・台本 第1版）

- 担当の行＝`ref/ep18/daihon_v1.md` 696〜923行（第5章 c501〜c523・第6章 c601〜c627）。見るだけ・台本は1文字も触っていない
- 見た行の数＝**173行**（空行を除く全行＝章見出し2・前置きの注1・カットの見出し50・字幕の行118・区切り2）
- 判定の内訳（行）＝OK 111／🔴 1／⚠️ 44／・ 17
- 所見の数＝**43件**（🔴1・⚠️32・・10）＝`findings_G3.json`（items 30件＝§1-3・§1-5・§1-7・§1-8・§1-9・§1-11・§2・§9-1 の担当分）
- 引いた原文の範囲＝R08 p.181・185〜189・196〜198・204・206〜207・214（認定・意見）／R08 p.11・13・46・47・65（証言）／V1 p.39〜42・167・175（kwic の当たり）／X p.60〜64・77・119〜124・131（OCR）／IR18 p.53・73・83・87・92・123・136／J p.1・12〜15・18・27・59・66〜68・90・91・150・156〜160／D p9001／all（nautical mile・average・S5W・seven miles）
- 🔴 の1件＝G3-34（c616 の聞き役のまとめ＋c615・c618・c622 の主語と図で、検査の結果が止まった所が艦長に寄る）
- 見えない頁：担当の出典欄の V1 p.39・40・50 は見える頁（BLANK_V1 の外）。認定は R08 の再録で当てた
- 道具＝`python ref/ep18/v2_build/kwic.py -f ref/ep18/v2_build/q_G3.txt`（問いは5回に分けた）＋通し頁ファイルの頁の丸ごと表示（scratchpad の `pg.py`＝同じ `ref/ep18/src/ep18_pages.txt` を頁ごとに出すだけ）
- 画像は1枚も読んでいない

## 第5章（696〜802行）

| 行 | 判定 | 原文の頁と短い引用（30〜80字） |
|---|---|---|
| 696 章見出し | OK | 章名「救難艦の5時間」＝§3。9:17〜14:35（認定26）で約5時間18分 |
| 698 注 | OK | 見る向きの合図 `c503`＝語り「上から見た地図で見る」と一致（§5b-80） |
| c501-700 見出し | ・ | 時間の帯の時刻は全部 認定22〜26 にある。ただし語りの1〜2行目は認定29（R08 p.187 "commenced an expanding search pattern"）＝出典欄に無い（G3-01） |
| c501-701 | OK | R08 p.187 認定29 "shortly after 0917R, when efforts to communicate with THRESHER had been unsuccessful, SKYLARK commenced an expanding search pattern" |
| c501-702 | OK | 認定29 "The QHB-A sonar was the principal means of underwater detection" |
| c501-703 | ・ | R08 p.186 認定22e "Attempted to establish communication by underwater telephone, sonar and radio"＝事実は OK・1行目の「呼びかけを続けながら」と重なる（G3-01） |
| c502-705 見出し | ⚠️ | 出典欄＝認定29 だけ。語りの2行は認定12・14（R08 p.185）（G3-02） |
| c502-706 | ⚠️ | R08 p.185 認定12 "did not have sonar contact on THRESHER at any time on 10 April 1963"＝事実は OK・出典欄に無い（G3-02） |
| c502-707 | ⚠️ | R08 p.185 認定14 "Depth of water in this area is about 8500 feet"（2,590.8m）＝事実は OK・出典欄に無い（G3-02） |
| c503-709 見出し | ・ | 認定22d OK。「基準点 北緯41度45分・西経65度」は R08 p.65 "datum, 65 degrees west and 41 degrees, 45 minutes north"＝出典欄に無い。X p.131（証拠50）は OCR で字が読めない＝⑤bで原寸（G3-03） |
| c503-710 | ⚠️ | 事実 OK。「9時21分、」が行末で、その節（2行目）と割れる＝不自然な改行（G3-03） |
| c503-711 | OK | R08 p.186 認定22d "Established LORAN position (logged at 0921R as 41-45N 64-59W)"／R08 p.65 datum＝65W・41-45N（「このあたり」で可） |
| c504-713 見出し | ・ | 画の欄の「報告を出しますか」は原文の言葉ではない（認定23a "if he should send such a message"＝間接の問い）（G3-04） |
| c504-714 | OK | R08 p.186 認定23a "At about 0940R, when the Operations Officer had asked the Commanding Officer" |
| c504-715 | OK | 認定23 "a message reporting the loss of contact with THRESHER" |
| c505-717 見出し | OK | V1 p.39（見える頁）＝R08 p.186 |
| c505-718 | OK | 認定23a "the reply was to the effect that"＝「こういう趣旨」を残した |
| c505-719 ★ | OK | "It is too early."＝決め所 #6。主語（救難艦の艦長）・趣旨は前の行＝意味の照合 OK |
| c506-721 見出し | OK | NARA 83750＝§7 |
| c506-722 | OK | R08 p.186 認定22f "At 1040R commenced dropping series of hand grenades" |
| c506-723 | ⚠️ | 認定22f "indicating to THRESHER that she should surface"＝事実 OK。「手りゅう弾」は読みが2通り（てりゅうだん／しゅりゅうだん）＝§6 に無い（G3-42） |
| c507-725 見出し | OK | 認定23b〜d（NBL＝Radio New London） |
| c507-726 | ・ | 認定23 "at about 1045R, SKYLARK began preparation of a message"＝「ごろ」が落ちた（G3-05）／23c "difficulty was reported at the time of transmission" |
| c507-727 | OK | 23c "SKYLARK shifted to an alternate frequency"／23d "NBL receipted for the message at 1245R" |
| c508-729 見出し | ⚠️ | X p.64（p1064）の文字は 2244Z〜2315Z の交信と "END OF DAY"＝12:45 の受け取りの行が無い（OCR）。101604Z の送信と "R 101604Z" の受領（1745Z＝12:45R）は X p.61（p1061）。X p.77（p1077）は12日の「最後の3つの交信」の電文＝認定28c の側（G3-06） |
| c508-730 Q | OK | まとめ（10時45分→12時45分の直後）。数字なし |
| c508-731 | OK | 9:13→12:45＝3時間32分（§9-1）。起点は「9時13分の声」と明示 |
| c509-733 見出し | OK | 認定24（R08 p.186） |
| c509-734 | OK | 認定24 "UNABLE TO COMMUNICATE WITH THRESHER SINCE 0917R … LAST TRANSMISSION RECD WAS GARBLED" |
| c509-735 | OK | "INDICATED THRESHER WAS APPROACHING TEST DEPTH … CONDUCTING EXPANDING SEARCH" |
| c510-737 見出し | ・ | 認定25 OK。画の欄の「軽い問題」が決め所 #4 の「軽微な問題」と語が違う（G3-04） |
| c510-738 Q | OK | 質問＝次の行「入っていない」がそのまま答え |
| c510-739 | OK | R08 p.186 認定25a "was suggested by the Operations Officer" |
| c510-740 | OK | 25a "the Commanding Officer decided not to include such information"／R08 p.187 25b "did not include such additional information in any subsequent reports" |
| c511-742 見出し | ・ | Commons Skylark underway＝§7。出典欄は認定26 だけ＝3行目は認定27（同じ R08 p.187）（G3-07） |
| c511-743 | OK | R08 p.187 認定26 "in Annapolis, Maryland, in a duty status, delivering a submarine presentation" |
| c511-744 | OK | 認定26 "returned to Norfolk at about 1420R. At 1435R he was advised of THRESHER's status" |
| c511-745 | OK | 認定27 "en route to New London, Connecticut from Key West, Florida" |
| c512-747 見出し | OK | D p9001 "NO. 509-63 … Statement by Admiral George W. Anderson … April 10, 1963, 8:00 p.m." |
| c512-748 | ⚠️ | 帰属「論文によると」OK。「制服組のトップ、」が行末で、名詞「海軍作戦部長」と別の行＝不自然な改行（G3-08） |
| c512-749 | OK | D "the Chief of Naval Operations learned at 3:40 p.m. that THRESHER might be in difficulty" |
| c512-750 | OK | 509-63 "being notified that the ship is overdue and presumed missing" |
| c513-752 見出し | ⚠️ | 画の欄「南東 約11キロ」＝マイルの種類が原文に無い（G3-09） |
| c513-753 Q | OK | 質問＝3行目「油の帯」が答え |
| c513-754 | ⚠️ | R08 p.188 認定30 "joined in the search area by patrol aircraft and by the U.S.S. Recovery (ARS-43) during the afternoon"＝事実 OK。「哨戒機」＝§6 に無い（G3-42） |
| c513-755 | ⚠️ | 認定31 "about 1730R, RECOVERY sighted an oil slick about seven miles to the Southeast of SKYLARK's 0917R position"＝×1.609 の前提（G3-09） |
| c514-757 見出し | OK | NARA 83751＝§7 |
| c514-758 | ⚠️ | 認定32 "samples were collected and articles of debris were recovered … materials which could have come from THRESHER"＝「ありうる」OK・何が拾われたかを言っていない（G3-10） |
| c514-759 | OK | 認定33 "No radioactivity beyond normal background level was found" |
| c514-760 Q | ⚠️ | 反応が事実の言い直し＋「出ていなかった」は原文（ふだんの値を超えていない）より強い（G3-11） |
| c515-762 見出し | OK | NARA 83746（乗用車の場面は使わない＝§1-4） |
| c515-763 | ⚠️ | D "At a 10:30 a.m. press conference, Admiral Anderson told the press"＝二次（D）だけの事実・帰属が c512 から2カット離れた（G3-12） |
| c515-764 | OK | D "he “reluctantly” had reached the conclusion that THRESHER was lost" |
| c516-766 見出し | OK | X p.120（p1120）"Narrative of USS SEAWOLF … Operations conducted in search for USS THRESHER"・証拠49 |
| c516-767 | OK | X p.121 "11 April 1963 … Submerged at datum"／認定35 "recorded possible electronic emissions and underwater noises" |
| c516-768 | ⚠️ | 事実 OK。「水中電話で、」が行末で、その節（3行目）と割れる（G3-13） |
| c516-769 | OK | X p.122〜123 "To THRESHER on UQC “If you hear my transmission, key your underwater telephone.”" |
| c517-771 見出し | OK | X p.122 "what may be interrupted keying"・X p.123 "Total of 37 pings heard counted"・X p.124 "May hear very weak voice … Unreadable" |
| c517-772 | ⚠️ | X p.122 "We hear what may be interrupted keying now"＝may を残した・OK。「打鍵」が初出で説明なし（G3-14） |
| c517-773 | OK | X p.124 "May hear very weak voice on 8KC … Unreadable"＝may を残した |
| c518-775 見出し | OK | 認定35（R08 p.188）・噂の札 |
| c518-776 Q | OK | 質問＝次の行が答え（通説の引き） |
| c518-777 | OK | §1-9 どおり「そう言われることがある」で引いた |
| c518-778 | ⚠️ | 認定35 "None of the signals which SEAWOLF received equated with anything that could have been originated by human beings"＝「言えるもの」は原文より弱い（G3-15） |
| c519-780 見出し | OK | 認定34・R08 p.65 |
| c519-781 | ⚠️ | 認定34 "passed from Commanding Officer, SKYLARK, to Commander Submarine Development Group TWO at about 0530R on 11 April"＝「翌朝」の起点がずれる（G3-16） |
| c519-782 | OK | R08 p.181 認定3 "THRESHER was a unit of Submarine Development Group TWO"／認定36 "The search for THRESHER is continuing" |
| c520-784 見出し | ⚠️ | 画の欄「12日 夕方」＝原文に無い時刻（G3-17）／「13日 査問会が証言で知る」＝認定28d OK |
| c520-785 | OK | R08 p.187 認定28b "Rear Admiral Ramage interviewed Lieutenant (jg) Watson and examined the UQC (underwater telephone) log" |
| c520-786 | ⚠️ | 28a の 1630R は捜索の指揮の交代の時刻。記録を見たのは "Shortly after the transfer to BLANDY"（時刻なし）（G3-17） |
| c521-788 見出し | OK | V1 p.40（見える頁）＝R08 p.187 |
| c521-789 | ⚠️ | 28b "became knowledgeable for the first time of the last communications from THRESHER"＝OK。「それまで」（previously）が★に無い（G3-18） |
| c521-790 ★ | ⚠️ | 28b "This information had not previously been communicated to him or to anyone outside SKYLARK"＝範囲（少将にも外の誰にも）は保った・時点が落ちた・c509 の電文と食い違って聞こえる（G3-18） |
| c522-792 見出し | ⚠️ | 画の欄「知らせるのが不当に長く遅れた」＝意見48 の中身が縮む（G3-19） |
| c522-793 | ⚠️ | R08 p.214 意見48 "failed fully to inform higher authority of all the information available to him pertinent to the circumstances attending the last transmission … as it was his duty to do, for an unreasonable length of time"（G3-19） |
| c522-794 | OK | 意見48 "this could not conceivably have contributed in any way to the loss of THRESHER"＝「考えられない」OK |
| c522-795 Q | OK | まとめ＝語りの直後・次の語りは「そう。」 |
| c523-797 見出し | ⚠️ | thr_film593_b＝スレッシャーの艦橋の乗員。語りの「1隻の艦」はスカイラーク（G3-20） |
| c523-798 | OK | 意見48 "was not materially connected therewith" |
| c523-799 | OK | 認定28b "had not previously been communicated to him or to anyone outside SKYLARK" |
| c523-800 | ・ | 章の橋。「同じ形」はこちらの見立て（原文に無い比較）（G3-21） |
| 802 区切り | OK | — |

## 第6章（804〜922行）

| 行 | 判定 | 原文の頁と短い引用（30〜80字） |
|---|---|---|
| 804 章見出し | OK | 章名「13.8パーセント」＝R08 p.197 認定102 "a rejection rate of 13.8 per cent" |
| c601-806 見出し | ・ | 出典欄は認定112 だけ。「網の目のように」の根は R08 p.189 認定43 "extensively used in vital piping systems throughout the ship"（G3-22） |
| c601-807 | ・ | 認定43 に近い一般の説明（「海水を通す」は認定43 に無い）（G3-22） |
| c601-808 | OK | 継手は `c208` で初出ずみ（§1-6）＝言い直しで可 |
| c602-810 見出し | OK | 模式図（銀ろう付けの面） |
| c602-811 | ⚠️ | 認定43「多く」≒extensively used＝OK（出典欄は認定103・112）。「銀を含む金属を溶かして、」が行末で定義の文が割れる（G3-22） |
| c602-812 | ・ | 仕組みの説明は出典の頁に無い＝一般の説明（G3-26） |
| c603-814 見出し | OK | R08 p.198 認定112 "over 3000 of 2-inch size and above in hazardous systems" |
| c603-815 | ・ | 認定112 "in an S5W reactor equipped ship … in hazardous systems"＝「海水など」は原文に無い・「同じ型」は認定42（R08 p.189 "a model S5W nuclear power plant"）（G3-23） |
| c603-816 | OK | 2インチ×2.54＝5.08cm。"is over 3000"（「超えた」は「超える」が近い＝G3-23） |
| c603-817 Q | OK | 反応（事実・数字なし） |
| c604-819 見出し | OK | 認定111 の6隻 |
| c604-820 Q | OK | 質問＝次の行「あった。」が答え |
| c604-821 | OK | R08 p.198 認定111 "prior to THRESHER's post shakedown availability, there had been reports of serious failures of sil-braze joints" |
| c604-822 | OK | "in BARBEL, SKATE, SNOOK, SCULPIN, ETHAN ALLEN and THRESHER"＝6隻・スレッシャーを含む |
| c605-824 見出し | ・ | 600ft＝182.9m（約180）・570ft＝173.7m（約170）＝換算 OK。§9-1 の表に無い（G3-43） |
| c605-825 | ⚠️ | 認定111 "a 3-inch sil-braze joint parted"（7.62cm）＝OK。「場所は、」が行末・次の行が「査問会は」＝「は」が2つ重なる（G3-24） |
| c605-826 | ⚠️ | IR18 p.123 "did not occur under the ice but in open water at a depth of about 570 feet"＝OK。「上の意見書」が何か分からない（G3-24） |
| c606-828 見出し | OK | J p.67（リッコーヴァー中将） |
| c606-829 | OK | J p.67 "the failure of a [classified matter deleted] silver-brazed joint in the trim system of the Thresher in May 1961" |
| c606-830 | OK | J p.67＝1963-04-29 の査問会の証言を議会（1963-07-23・J p.59）で読み上げた |
| c607-832 見出し | OK | NARA 85185＝§7。R08 p.46 "Lawson P. Ramage, RADM … was recalled as a witness" |
| c607-833 Q | OK | 質問＝次の行「しばらくは、分からなかった」が答え |
| c607-834 | ⚠️ | 事実 OK。「1962年2月より前、」が行末で、その節（次の行）と割れる（G3-25） |
| c607-835 | OK | R08 p.47 "prior to February 1962, there were no non-destructive tests, such as ultrasonic or radiographic, for silver-brazed joints" |
| c608-837 見出し | OK | 認定103・J p.13（"You have to allow for roughly 10 to 17 percent error"） |
| c608-838 | ・ | R08 p.11 "13 February 1962, recommending visual inspection and certain non-destructive testing"＝「使われ始めた」OK。「外から音を当て、はね返りで」は出典の頁に無い（G3-26） |
| c608-839 | OK | 認定103 "40 per cent bond"＝付いている割合を見る |
| c609-841 見出し | OK | 認定98（R08 p.196）"dated 28 August 1962" |
| c609-842 | OK | 認定98 "by letter to the Commander, Portsmouth Naval Shipyard dated 28 August 1962, the Bureau of Ships" |
| c609-843 | OK | 98b "employ a minimum of at least one ultrasonic test team throughout the entire assigned post shakedown availability … the maximum number" |
| c610-845 見出し | ・ | 「工期を遅らせない範囲で」は認定97（到着の会議の決め）＝作業の指示（認定99）ではない（G3-27） |
| c610-846 | OK | R08 p.196 認定99 "called for use of one ultrasonic test team" |
| c610-847 | OK | 99 "to test first those joints not lagged … if time permitted thereafter, lagging would be removed" |
| c611-849 見出し | OK | thr_t22＝§7 |
| c611-850 | ⚠️ | 「保温材＝覆い」は一般の説明（G3-26）。「そして、検査は、」が行末で文が割れる（G3-28） |
| c611-851 | OK | R08 p.196 認定97 "was placed on a not-to-delay vessel basis" |
| c612-853 見出し | ⚠️ | 画の欄「平均40%以上」＝「平均」は原文に無い（G3-29） |
| c612-854 | ⚠️ | R08 p.197 認定103 "40 per cent bond, 25 per cent minimum, either land"（G3-29） |
| c612-855 | OK | "25 per cent minimum, either land" |
| c613-857 見出し | OK | 145×0.138＝20.01（計算と明示） |
| c613-858 | ⚠️ | R08 p.197 認定102 "by 29 November 1962, 145 old joints had been ultrasonically tested"＝OK。「古い継手」が何か分からない（G3-30） |
| c613-859 | OK | 認定102 "rejection rate of 13.8 per cent"／1÷0.138＝7.25 |
| c613-860 | OK | 「計算だ」と明示（§9-1） |
| c614-862 見出し | ⚠️ | 画の欄「145本／3,000本を超える＝約5%」＝分母の範囲が違う数の割り算・c624 の中将の約5% と同じ数（G3-32） |
| c614-863 Q | OK | 反応 |
| c614-864 | ⚠️ | 「そう見ている」＝意見19 は「多い」とは言っていない（G3-31） |
| c614-865 | ⚠️ | R08 p.206 意見19 "the rejection rate of 13.8% on original sil-braze joints in THRESHER was a clear indicator that additional action was required"＝中身 OK・出典欄は認定102・112（G3-31） |
| c615-867 見出し | OK | 認定104・105 |
| c615-868 | ⚠️ | R08 p.197 認定104 "reported the results … and requested decision as to whether lagged joints should be unlagged"＝OK。「決めてほしい、」／「と上げた。」で割れる（G3-33） |
| c615-869 | ⚠️ | 認定105 "decision was made on 4 December 1962 not to unlag"＝OK。決めた主語が無い（G3-34）・「4日」の読み（G3-42） |
| c616-871 見出し | OK | 認定105・106 |
| c616-872 | OK | 認定105 "known to the management personnel of the Shipyard, including the Production Officer and the Commander" |
| c616-873 | OK | 認定106 "a copy of this decision was furnished the Commanding Officer of THRESHER" |
| c616-874 Q | 🔴 | まとめが艦長だけを拾う→c617「そう。ただ」→★「艦長より上に」＝止まった所が艦長に寄る（G3-34） |
| c617-876 見出し | OK | 認定107・4月9日 出港＝R08 p.181 認定2 "departed … on the morning of 9 April 1963" |
| c617-877 | ⚠️ | R08 p.197 認定107 "no further ultrasonic testing of old sil-braze joints was conducted pursuant to this program after 29 November 1962"＝この計画での、が落ちた（G3-35） |
| c617-878 | OK | 1962-11-29→1963-04-09＝4か月11日（§9-1） |
| c618-880 見出し | ⚠️ | 流れ図「→ 艦長 ✕ 艦船局・作戦の指揮系統」＝艦船局への道も艦長を通るように読める（G3-37） |
| c618-881 | ⚠️ | 「結果の数字も、」が行末で文が割れる（G3-36） |
| c618-882 | OK | 認定108 "neither the results of the surveillance nor the decision not to proceed further … was made known to the Bureau of Ships or to anyone in the operational command line" |
| c619-884 見出し | OK | V1 p.50（見える頁）＝R08 p.197 |
| c619-885 | OK | 「認定」＝finding of fact（階層が合う） |
| c619-886 ★ | OK | 認定108 "higher than the Commanding Officer of THRESHER"＝決め所 #8。やめる決定・艦船局は前の行＝範囲 OK |
| c620-888 見出し | OK | J p.18（1963-06-26 の会） |
| c620-889 | OK | J p.18 Brockett "It was in process and it was received after the 11th of April." |
| c620-890 | OK | 同（艦船局の長＝ブロケット少将・役で呼ぶ） |
| c621-892 見出し | OK | 認定109・意見18（R08 p.197・206）。人は後ろ姿の遠景だけ |
| c621-893 | OK | R08 p.197 認定109 "management and workers exhibited a high degree of confidence in sil-braze joints" |
| c621-894 | OK | R08 p.206 意見18 "Shipyard did not aggressively pursue … Deputy Commander … did not aggressively pursue …, nor did the Commanding Officer"＝3者とも・意見と帰属 OK |
| c622-896 見出し | OK | 意見21（R08 p.207） |
| c622-897 | ⚠️ | 意見21 "the management of the Portsmouth Naval Shipyard did not exercise good judgment in determining not to unlag"＝意見を地の文で・主語が落ちた（G3-38） |
| c622-898 | ・ | J p.14 "the shipyard did use poor judgment"・J p.15 "he had used poor judgment"＝「誤り」は poor judgment より少し強い（G3-38） |
| c623-900 見出し | OK | p8013＝J p.13（1963-06-26 の会＝J p.1〜27）Holifield "why the other 2,855 joints were never tested"／Austin "same reaction" |
| c623-901 | OK | J p.12 "Why were not more joints tested, and why were not all of the joints tested" |
| c623-902 | OK | J p.13 "The court had the same reaction which you have evidenced on this point." |
| c624-904 見出し | OK | J p.67 "the testimony I gave in closed session to the court of inquiry on April 29, 1963"／J p.59 "TUESDAY, JULY 23, 1963" |
| c624-905 | OK | 同 |
| c624-906 | ⚠️ | J p.68 "during the recent stay of Thresher at Portsmouth about 5 percent of her silver-brazed joints were ultrasonically inspected. These joints were in critical piping systems, 2-inch diameter or larger"＝誰の・どこの・どの継手が落ちた（G3-39） |
| c624-907 | OK | J p.68 "about 10 percent of those checked required repair or replacement" |
| c625-909 見出し | OK | J p.68 |
| c625-910 | ・ | 「条件をつけて」＝OK。"the ship … when she last went to sea" が前の行にも★にも無い（G3-40） |
| c625-911 ★ | OK | J p.68 "If the quality of the joints so inspected was representative of all the Thresher's silver-brazed joints this means that the ship had several hundred substandard joints"＝条件を残した・決め所 #9 |
| c626-913 見出し | OK | 認定102・J p.68（13.8%／約10%＝約5%の見本／14%） |
| c626-914 | OK | J p.68 Holifield "Our figure on this is 14 percent." |
| c626-915 | OK | J p.68 Rickover "The figures may have changed because more accurate information has been made available." |
| c626-916 | OK | J p.68 "I am merely pointing out a principle … they would only repair those they found wrong in that sample"＝「数百」を事実と言っていない |
| c627-918 見出し | OK | 意見1d（R08 p.204）"A deficient air system, susceptible to freeze-up, with low capacity and low blow rate"＝次の章の題 |
| c627-919 Q | ⚠️ | 質問に次の語りが答えていない（G3-41） |
| c627-920 | ⚠️ | 「そこが、次の問いになる」＝答えを先送り（G3-41） |
| 922 区切り | OK | — |

