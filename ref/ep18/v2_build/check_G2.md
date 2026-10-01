# ④' 検査 G2（18本目 スレッシャー号・台本 第1版）

- 担当の行＝`ref/ep18/daihon_v1.md` 494〜695行（第3章 c301〜c320・第4章 c401〜c423）。見るだけ・台本は1文字も触っていない
- 見た行の数＝**154行**（空行を除く全行＝章見出し2・注1・区切り2＋カットの見出し43＋字幕の行106）
- 判定の内訳（行）＝OK 106／🔴 4／⚠️ 20／・ 24
- 所見の数＝**36件**（🔴2・⚠️16・・18）＝`findings_G2.json`
- 引いた原文の範囲＝R08 p.181〜186・211〜212・214（＝p4181〜4186・4211〜4212・4214）／V1 p.38（見える頁）・p.34・37（見えない頁＝R08 p.181・184 で当てた）・p.65・67（見えない頁＝R08 p.212・214）・p.66・p.93・p.109〜110・112〜113・116〜118・127・132・136（見えない頁）・137〜140・182〜183・211（見えない頁）・277〜278／IR18 p.44・49〜50・69〜71・105・133／X p.131（証拠50）／D p9001（国防総省の発表 509-63 の写し）／T p9801（No.710-64）／AP p9901
- 道具＝`python ref/ep18/v2_build/kwic.py -f ref/ep18/v2_build/q_G2.txt`（2回）＋頁の丸ごと表示（同じ通し頁ファイル）。画像は1枚も読んでいない
- 行長＝字幕の行106行すべて41字以下（最長＝c308-529 の41字）・★3件はすべて20字以内で最後の行

## 第3章（494〜585行）

| 行 | 判定 | 原文の頁と短い引用（30〜80字） |
|---|---|---|
| 494 章見出し | OK | 章名「4月10日の朝」＝§3 の表と一致・20カット＝c301〜c320 |
| c301-496 見出し | ・ | 画 thr_film593_a＝materials ○（720×480）。出典「V1 p.34」は見えない頁＝R08 p.181 を併記（G2-33） |
| c301-497 | OK | R08 p.181 認定2 "departed Portsmouth Naval Shipyard, on the morning of 9 April 1963" |
| c301-498 | ・ | R08 p.181 認定2 "sea trials following a post shakedown availability which extended from 16 July 1962 to 11 April 1963"＝整備の期間は11日まで（G2-19） |
| c302-500 見出し | ⚠️ | R08 p.181〜184 を数え直した＝USS THRESHER 108（士官12・下士官兵96）＋造船所の海軍士官3＋Civilian Employee 13＋Contractor's Representative 4＋STAFF 1＝129 ✓。「請負の会社の技術者」の「技術者」は原文に無い（G2-06） |
| c302-501 | OK | 認定4 の名簿（R08 p.181〜184）＝129・108 ✓ |
| c302-502 | ⚠️ | R08 p.184 "Contractor's Representative, Sperry Corporation"／認定5 "civilian employees of activities under Government contract"＝「機器を納めた」「技術者」は原文に無い（G2-06）。行末「士官の、」（G2-07） |
| c302-503 | OK | 士官 12＋3＋1＝16・下士官兵96・民間 13＋4＝17・計129 ✓ |
| c303-505 見出し | OK | p4181＝R08 p.181（見える頁・認定4 の名簿の1頁目）。§1-3 の決め＝頁を映す ✓ |
| c303-506 | OK | 認定4 "the following persons … were on board THRESHER"（名前は読み上げていない ✓） |
| c303-507 | OK | R08 p.184 認定6 "all persons on board THRESHER were on board for the purpose of executing official duties" |
| c304-509 見出し | ・ | 画 Skylark (ASR-20).jpg＝materials △（条件つき＝額装）✓。出典「V1 p.37」は見えない頁＝R08 p.184（G2-33） |
| c304-510 | OK | 聞き役（質問）＝次の行が答えている ✓ |
| c304-511 | OK | D p9001（発表 509-63）"The submarine rescue vessell USS SKYLARK was accompanying the THRESHER" |
| c304-512 | OK | R08 p.184 認定7 "under command of Lieutenant Commander Stanley HECKER … designated to act as escort to THRESHER during sea trials"（実名の線 §1-3 ✓） |
| c305-514 見出し | OK | 認定8 の再現図（秘／秘でない・予定表は無い）＝原文どおり |
| c305-515 | OK | R08 p.184 認定8 "THRESHER's movement orders were CONFIDENTIAL; SKYLARK's were unclassified" |
| c305-516 | OK | 認定8 "Sea trial agenda … were unclassified and were not held by SKYLARK" |
| c305-517 | ⚠️ | 聞き役（まとめ）「予定を知らなかった」＝原文は「予定表を持っていなかった」。V1 p.183 艦長 "…an approximate time by 'phone to my Operations Officer"（OCR 崩れ）（G2-04） |
| c306-519 見出し | OK | 画 Skylark underway c1950.jpg＝materials △（額装）✓・出典 認定12（R08 p.185）✓ |
| c306-520 | ・ | R08 p.185 認定12 "UQC (underwater telephone) provided the means of voice communication"＝「だけ」は V1 p.183 "The UQC … was the only equipment I could place some reliance on" で裏付く＝出典欄に足す（G2-20） |
| c306-521 | ・ | 認定12 "maximum range scale of 3750 yards"＝3,429m→約3.4キロ ✓。「目盛りの最大」を探知の距離と言い切っている（G2-21） |
| c306-522 | OK | 認定12 "did not have sonar contact on THRESHER at any time on 10 April 1963" |
| c307-524 見出し | OK | p1131＝X p.131 "EXHIBIT 50: CHART DISPLAYING … POSITIONS … STATION FOX"（塗り b(1) 多数）✓ |
| c307-525 | OK | R08 p.185 認定10 "on completion of a scheduled shallow dive, the two ships proceeded independently during the night" |
| c307-526 | ・ | 認定10 "second rendezvous in the vicinity of Latitude 41-46 North, Longitude 65-03 West"。「ボストンの東」は認定に無い＝D p9001 発表 509-63 "some 220 miles east of Boston"・T p9801 で裏付く（G2-22） |
| c308-528 見出し | OK | 認定11 北緯41-46・西経65-03・"bore 147° True, 3400 yards"＝3,109m→約3.1キロ ✓ |
| c308-529 | OK | R08 p.185 認定11 "at 0745R, 10 April 1963 … THRESHER reported to her that SKYLARK bore 147° True, 3400 yards"（41字＝上限ちょうど） |
| c308-530 | OK | 同上（2隻が同じ海域） |
| c309-532 見出し | ・ | 「近くにほかの船なし」は原文 "No other ships are known"＝知られていない（画の札で言い切らない） |
| c309-533 | OK | 聞き役（質問）＝次の行が答えている ✓ |
| c309-534 | OK | R08 p.185 認定14 "the sea was calm, with a slight swell, at 0900R … Wind … at seven knots"＝12.96→時速約13キロ ✓ |
| c309-535 | ⚠️ | 認定14 "Visibility was about ten miles"＝マイルの種類は原文に無い（海里なら約18.5キロ）。「ほかの船は知られていない」の日本語（G2-09） |
| c310-537 見出し | OK | A1・rec= 認定11・14・15・「試験深度の数は出さない」✓ |
| c310-538 | OK | V1 p.38 認定15 "at 0747R, THRESHER reported by underwater telephone that she was starting a deep dive" |
| c310-539 | ⚠️ | 認定15 "Depth for this dive had been set at"＋b(1)＝空欄ではなく塗り（§1-5 6-3 の決め）（G2-05） |
| c311-541 見出し | OK | A1（段ごとに下がる）＝V1 p.113 ワトソン中尉 "proceeding one-half test depth" で裏付く |
| c311-542 | ・ | 認定15 "THRESHER reported course changes and depth changes"。「段ごとに」は V1 p.113（0809「試験深度の半分へ」）＝出典欄に足す（G2-23） |
| c311-543 | OK | 認定15 "SKYLARK then maintained her approximate position" |
| c311-544 | OK | 認定15 "but SKYLARK did not plot THRESHER's position" |
| c312-546 見出し | OK | 意見45（R08 p.212）＝9:09 試験深度・9:10 針路 090（東）"gave no indication of any difficulty" ✓ |
| c312-547 | OK | 聞き役（質問）＝次の行が答えている ✓ |
| c312-548 | ・ | R08 p.212 意見45 "It is known with reasonable certainty that at 0909R the THRESHER was at test depth"＝「着いた」より「いた」（G2-24） |
| c312-549 | OK | 意見45 "At about 0910R a message from THRESHER announced a course change … and gave no indication of any difficulty" |
| c313-551 見出し | OK | A1・救難室の限界 約260メートル＝V1 p.38 認定13 "850 feet" ✓ |
| c313-552 | OK | V1 p.38 認定13 "SKYLARK carried a rescue chamber" |
| c313-553 | OK | 聞き役（質問）＝次の行が答えている ✓ |
| c313-554 | ⚠️ | 「鐘のような形」は通し頁のどこにも無い（bell・diving bell・McCann＝0件）＝自分の知識の補い（G2-08） |
| c314-556 見出し | OK | A1・約260／約2,600 を並べる ✓ |
| c314-557 | OK | V1 p.38 認定13 "maximum depth capability of 850 feet"（IR18 p.71 も 850）＝259m→約260 ✓。⚠️ R08 p.185 の文字の層では数が欠ける（items） |
| c314-558 | OK | 認定14 "about 8500 feet"＝2,591m→約2,600（§1-5 6-1）・8500÷850＝10.0 →「およそ10倍」✓ |
| c315-560 見出し | OK | 数の比べ 約260／約2,600 ✓ |
| c315-561 | OK | 聞き役（まとめ）＝c314 の直後・次は「そう。」✓ |
| c315-562 | OK | 認定13・14 からの帰結（10倍） |
| c315-563 | OK | V1 p.183 "what are the capabilities of SKYLARK for assisting a submarine out of control" |
| c316-565 見出し | OK | p183＝V1 p.183（見える頁）"The court recessed at 1151 hours, 15 April 1963" ✓ |
| c316-566 | OK | 1963-04-15＝事故（04-10）の5日後 ✓ |
| c316-567 | OK | V1 p.183 "capabilities of SKYLARK for assisting a submarine out of control..." |
| c317-569 見出し | OK | 決め所 #3・V1 p.183（記録 p.110）✓ |
| c317-570 | ・ | V1 p.183 "Q. ... if that submarine is in 8400 feet of water? A. None, sir."＝条件は「深い海」でなく「8,400フィートの海」（G2-25） |
| c317-571 ★ | OK | V1 p.183 "None, sir." ／ "Admiral, I could not even plant a buoy."＝問答の順と合う（最初の None は条件の前・★は条件の後の答えと同じ） |
| c318-573 見出し | OK | 画 thr_film593_c＝materials ○ |
| c318-574 | ・ | V1 p.183 "I have 7200 feet of 7-inch nylon line that I could have used, and it wouldn't have helped"＝2,195m→約2,200 ✓。「索」1字の読み（G2-26） |
| c318-575 | OK | V1 p.183 "I could not even plant a buoy" ／ "to mark some position" |
| c319-577 見出し | OK | A1・rec= 認定12・16 ✓ |
| c319-578 | ⚠️ | 認定22 "SKYLARK initiated the following actions: a. Advised … d. Established LORAN position … f. … hand grenades"＝できたのは声を聞き記録することだけ、は原文に無い（G2-03） |
| c319-579 | ⚠️ | 同上（G2-03） |
| c320-581 見出し | OK | 意見45・認定16（9:09・9:10・9:13 は空ける）✓ |
| c320-582 | OK | 聞き役（まとめ・予告型）＝声は c102 で既出。次は「そう。」✓ |
| c320-583 | OK | 9:13→9:18＝5分 ✓ |
| 585 区切り | OK | — |

## 第4章（587〜694行）

| 行 | 判定 | 原文の頁と短い引用（30〜80字） |
|---|---|---|
| 587 章見出し | OK | 章名「9時13分から9時18分」＝§3 の表と一致・23カット＝c401〜c423 |
| 589 注 | OK | §B2-4＝A2 は c411（9:17）で艦の絵を止め、c420・c422 は海面のスカイラークだけ ✓ |
| c401-591 見出し | OK | 時間の帯 上＝声（認定16・17）／下＝音（認定18）✓ |
| c401-592 | ⚠️ | 認定16〜18 の2種の記録 ✓。行末「1つは、」が次の行の中身と離れる（G2-10） |
| c401-593 | OK | R08 p.185 認定18 "Commander Oceanographic Systems Atlantic obtained information" |
| c402-595 見出し | ・ | V1 p.277 "hydrophone arrays at the fifteen monitoring stations"＝「海底の」は原文に無い（G2-27） |
| c402-596 | ・ | V1 p.277 "targets which are contacted by passive means by the hydrophone arrays"＝出典欄は認定18 だけ（G2-27） |
| c402-597 | OK | 認定18 "Commander Oceanographic Systems Atlantic"・V1 p.277 "…Atlantic in Norfolk" |
| c402-598 | OK | 認定18 "emanated from THRESHER at 0918.1R"・"indications of two disturbances" |
| c403-600 見出し | ・ | 画面の時刻「9:09.8〜9:11.3」＝分の小数と波ダッシュ（G2-35） |
| c403-601 | OK | 認定18 "one extending from 0909.8R to 0911.3R"＝9:09:48〜9:11:18 →「9分すぎから11分すぎ」✓ |
| c403-602 | ⚠️ | 認定18 "which could have been made by the blowing of the ballast tanks"＝様相 ✓。行末「吹くとは、」（G2-11）・「出うる」の読み（G2-28） |
| c403-603 | OK | 用語の一言（タンクを吹く） |
| c404-605 見出し | OK | 模式図・出典 認定18・意見45 ✓ |
| c404-606 | ⚠️ | 行末「回す、」＝修飾語と名詞（主冷却材ポンプ）が別の行（G2-12） |
| c404-607 | ⚠️ | R08 p.212 意見45 "It is known, without much doubt, that at 0911R the main coolant pumps … either stopped or were slowed"＝中身 ✓・行末「止まったのか、」（G2-12） |
| c404-608 | OK | 意見45 "either stopped or were slowed to 'SLOW mode'"＝どちらかは決めていない ✓（旧版の「ポンプが停止」は使っていない） |
| c405-610 見出し | OK | A2・rec= 認定16。潜水艦の位置は記録に無い（G2-29 の注） |
| c405-611 | OK | R08 p.185 認定16 "until about 0913R, when THRESHER reported to SKYLARK" |
| c405-612 | OK | 7:47→9:13＝86分→「1時間半近く」✓（§9-1） |
| c406-614 見出し | OK | 決め所 #4・認定16（V1 p.38＝見える頁）・V1 p.118 ✓ |
| c406-615 | OK | V1 p.118 "who was doing the recording in the UQC log … A Radioman Third Class"・V1 p.137 "Mostly I logged, sir." |
| c406-616 | OK | 認定16 "THRESHER reported to SKYLARK to the effect"＝趣旨を前の行で言っている ✓ |
| c406-617 ★ | OK | 認定16 "Experiencing minor difficulties."＝意味 ✓（誰の声か＝潜水艦・趣旨は前の行） |
| c407-619 見出し | OK | A2（艦首が上）＝認定16 "Have positive up angle" の範囲 ✓ |
| c407-620 | OK | 認定16 "Have positive up angle." |
| c407-621 | OK | 認定16 "Am attempting to blow. Will keep you informed." |
| c408-623 見出し | ・ | 画面の時刻「9:13.5〜9:14」（G2-35） |
| c408-624 | OK | 認定18 "the other from 0913.5R to 0914R" |
| c408-625 | OK | 認定18 "which could have been made by the blowing of the ballast tanks"（でありうる ✓） |
| c409-627 見出し | ・ | A2（呼びかけの輪）＝c409〜c411 が A2 の3連続（G2-29） |
| c409-628 | OK | 聞き役（質問）＝次の行が答えている ✓ |
| c409-629 | OK | R08 p.186 認定22a "Advised THRESHER that the area was clear"・V1 p.116 "At 0914 we told the THRESHER, 'No contacts in area'" |
| c409-630 | OK | 認定22c "Asked THRESHER at about 0915R, 'Are you in control?' and repeated this query." |
| c410-632 見出し | ・ | A2（崩れた声 9:16）（G2-29） |
| c410-633 | OK | 聞き役（質問）＝次の行が答えている |
| c410-634 | 🔴 | R08 p.185 認定17 "SKYLARK heard a garbled transmission which was believed to contain the words '... test depth'"（G2-01） |
| c410-635 | 🔴 | 同上。V1 p.139 記録係（9:16）"We couldn't make it out … none of us could"・V1 p.117 ワトソン "At 0917 … clearly understood were, 'test depth'"（G2-01） |
| c411-637 見出し | ・ | A2（9:17 で艦の絵を止める）＝§B2-4 ✓（G2-29） |
| c411-638 | 🔴 | 認定17 "An additional garbled transmission was received about 0917R, reported as containing the words '... nine hundred North'"（G2-02） |
| c411-639 | 🔴 | 同上（G2-02）＋行末「スカイラークの艦長は、」で主語と述語が別の行（G2-30） |
| c411-640 | OK | V1 p.182 "you didn't have any hunch that she was lost when you heard that garbled message at 0917? A. No, sir." |
| c412-642 見出し | OK | panel 認定17 の言葉（「……」を残した ✓） |
| c412-643 | OK | 聞き役（質問）＝次の行が答えている ✓ |
| c412-644 | OK | 認定17（R08 p.185・V1 p.38・IR18 p.70）は語を並べるだけ＝"nine hundred" の当たりは認定17 の文だけ |
| c412-645 | ⚠️ | AP "suggesting the sub was 900 feet beyond its test depth, according to the documents"＝「記録の外」は確かめられない（G2-14） |
| c413-647 見出し | OK | 時間の帯（上の段は 9:17 で終わる）✓・画面の「9:18.1」は G2-35 |
| c413-648 | ⚠️ | 認定18 "a high energy, low frequency noise disturbance of the type which could have been made by an implosion"＝中身 ✓・行末「型の、」（G2-13） |
| c413-649 | OK | 用語の一言（内破） |
| c414-651 見出し | OK | p38＝V1 p.38（見える頁・認定10〜20）✓。出典欄「V1 p.38〜39」＝認定20 も p.38 にある（直さなくてよい） |
| c414-652 | OK | V1 p.38 認定19 "THRESHER was lost at sea with all on board at about 0918R on 10 April 1963"＝認定の階層 ✓・死の語 ✓ |
| c414-653 | OK | V1 p.38 認定19 "Latitude 41-45 North, Longitude 65-00 West"・IR18 p.50 も同じ（R08 p.185 は位置が欠ける＝items） |
| c415-655 見出し | ・ | 画 NARA 85185＝スレッシャーの航走。語りはスカイラークの航海士と「壊れる音」（G2-36） |
| c415-656 | OK | V1 p.109 "James David Watson, lieutenant (junior grade), Navigator and First Lieutenant on the USS SKYLARK"（実名の線 ✓） |
| c415-657 | ⚠️ | V1 p.118 "Did the commanding officer, who was on the equipment…"／"Both of us, shortly after that, heard a sound"＝「そのすぐあと」の起点（G2-15） |
| c416-659 見出し | ・ | 書類の再現図の文と字幕が同じ中身（G2-31） |
| c416-660 | OK | V1 p.118 "I had heard a lot of ships breaking up during World War II after having been torpedoed at depths" |
| c416-661 | OK | V1 p.118 "It sounded as though there was a compartment collapsing or something similar to that nature." |
| c417-663 見出し | OK | 決め所 #5・V1 p.118（記録 p.45）✓ |
| c417-664 | OK | 聞き役（質問）＝原文の問い "Can you describe that sound to the court?" と同じ ✓ |
| c417-665 | OK | V1 p.109 "Questions by counsel for the court"（査問会の側の問い） |
| c417-666 ★ | OK | V1 p.118 "It is a rather muted, dull thud."＝意味 ✓（直前の第二次大戦の比べ＝c416 の順も原文どおり） |
| c418-668 見出し | ・ | 「甲板の乗員」＝V1 p.127 モーエン3等兵曹（当直の掌帆の下士官）・V1 p.132 で水中電話に「近くに船なし」を伝えた人／二重表示（G2-31） |
| c418-669 | ⚠️ | V1 p.132 "right after he made that transmission … You could hear air rushing into his tanks for about four to five seconds"＝9:13 の声のすぐあと（G2-16） |
| c418-670 | OK | V1 p.140 "Did you hear any noise, like air being blown into a tank …? A. No, sir, I don't think so." |
| c419-672 見出し | OK | 時間の帯まとめ（9:11 ポンプ＝止まったかは言わない）✓ |
| c419-673 | OK | 聞き役（まとめ）＝次は「そう。」✓ |
| c419-674 | ⚠️ | V1 p.139 記録係（9:13:30 の分）"I heard it plainly but I didn't catch what it said"・V1 p.117 ワトソン "clearly understood were, 'test depth'"（G2-17） |
| c419-675 | ⚠️ | 9:13→9:18.1＝5.1分 ✓。「そこから、約5分」の終点が無い（G2-17） |
| c420-677 見出し | OK | A2（潜水艦は描かない）✓ |
| c420-678 | OK | R08 p.212 意見45 "It is impossible, with the information now available, to obtain a more precise determination" |
| c420-679 | ・ | 「だけ」＝c415〜c418 の耳の証言（V1 p.117・118・132）も残っている（G2-34） |
| c420-680 | OK | 聞き役（まとめ）＝次は「そう。」✓ |
| c421-682 見出し | ・ | 出典欄は R08 p.212 だけ＝「最もありうる」は R08 p.214（G2-32） |
| c421-683 | OK | R08 p.212 意見45 "utilizing known factors and the most probable variants … as the inputs for computer solutions" |
| c421-684 | ・ | R08 p.214 意見45 "This is the most probable approximation of the sequence of events"＝近似と断り書き（G2-32） |
| c422-686 見出し | OK | A2（呼びかけを続ける）rec= 認定22 ✓ |
| c422-687 | OK | R08 p.186 認定22e "by underwater telephone, sonar and radio"・認定24 "CALLING BY UQC VOICE AND CW … EXPLOSIVE SIGNALS EVERY 10 MINS" |
| c422-688 | OK | 認定24 "WITH NO SUCCESS" |
| c423-690 見出し | OK | thr_t2＝materials ○（3つ目の切り出し）・出典 認定23 ✓ |
| c423-691 | ⚠️ | 聞き役（質問）＝次の行が答えていない（G2-18） |
| c423-692 | ⚠️ | R08 p.186 認定23 "at about 1045R, SKYLARK began preparation of a message"・23d "NBL receipted for the message at 1245R"（G2-18） |
| 694 区切り | OK | — |

## 判定の数

| | 第3章（71行） | 第4章（83行） | 計（154行） |
|---|---:|---:|---:|
| OK | 52 | 54 | **106** |
| 🔴 | 0 | 4 | **4** |
| ⚠️ | 8 | 12 | **20** |
| ・ | 11 | 13 | **24** |

- 所見＝**36件**（🔴2・⚠️16・・18）＝`findings_G2.json`
- items＝§1-3・§1-5・§1-6・§1-7・§1-8・§1-9・§1-11・§2・§9-1 のうち担当に当たる34件＝`findings_G2.json` の items

## 親へ（画像・原寸で確かめること）

- 🔴 R08 p.185（再録）の文字の層では、認定13 の救難室の深さ「850」と認定19 の位置「41-45 North, 65-00 West」が欠け、頁の下に (b)(1) が3つある（V1 p.38 は見える頁で両方とも読める・IR18 p.50・71 にも同じ数）。第8回で改めて塗られたのかを ⑤b で原寸（c314 の数・c414 の頁の選び方にかかわる）
- V1 p.183 の艦長の陳述（OCR が崩れる）"The UQC throughout this exercise was the only equipment I could place some reliance on"・"…an approximate time by 'phone to my Operations Officer" の字を原寸で（G2-04・G2-20 の根拠）
- V1 p.140 の問い "a further indication of words that have been [variously／previously] explained to this court"＝OCR が崩れて「いろいろに」か「前に」か決められない（G2-14 の補い）
