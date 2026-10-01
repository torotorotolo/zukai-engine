# ④' 検査 G1（18本目 スレッシャー号・台本 第1版）

- 担当の行＝`ref/ep18/daihon_v1.md` 320〜493行（第1章 c101〜c117・第2章 c201〜c220）。見るだけ・台本は1文字も触っていない
- 見た行の数＝**131行**（空行を除く全行＝章見出し・前置きの表7行＋カットの見出し37行＋字幕の行84行＋区切り3行）
- 判定の内訳（行）＝OK 82／🔴 2／⚠️ 36／・ 11
- 所見の数＝**30件**（🔴1・⚠️23・・6）＝`findings_G1.json`
- 引いた原文の範囲＝R08 p.180〜186・189・193〜197・200・203〜204・208・212〜213・216〜218・220（＝p4180〜4220）／R08 p.2・33・60・64・68・76〜78・107〜109／V1 p.2・19・38・48・57・65（見えない頁）／IR18 p.1〜2・5〜6・16・46〜47・66〜67・74／J 前付 p.1・3・9、J p.5・9・15〜16・20・27・31〜32・34・60〜61・65・68・77・95・147・161・168・189／AP p9901／sources.md §1（原文ではない＝公開の回と頁数の出どころとしてだけ）
- 道具＝`python ref/ep18/v2_build/kwic.py -f ref/ep18/v2_build/q_G1.txt`（問いは3回に分けた）＋頁の丸ごと表示（同じ通し頁ファイル）
- 画像は1枚も読んでいない。OCR の崩れで決められない所は「親へ（画像）」と書いた（G1-09 の証拠111 の宛先）

## 第1章（320〜401行）

| 行 | 判定 | 原文の頁と短い引用（30〜80字） |
|---|---|---|
| 320 章見出し | OK | 章名「紙に残った知らせ」＝§1-10（背骨 c105・c107） |
| 322 注 | OK | ÷380 の秒＝本係の数え直しで c104 34.6秒・c105 44.8秒（聞き役の行を含む）＝§0-3 と一致 |
| 324 表 | OK | — |
| 325 表 | OK | — |
| 326 表 c101〜c103 | OK | 下の各行で当てた |
| 327 表 c104 | OK | IR18 p.2（p2002）"deserve further comment in this final endorsement"＝「最後の意見書」 |
| 328 表 c105 | OK | R08 p.195 認定91c "the most dangerous condition … salt water flooding while at or near test depth" |
| c101-330 見出し | ・ | 画 cm_USS_Thresher__SSN-593_＝materials ◎。出典 認定16（V1 p.38）に「東海岸の沖」は無い→ J前付 p.9 "approximately 200 miles off the northeastern coast of the United States"（G1-30） |
| c101-331 | OK | V1 p.38＝R08 p.185 認定16 "until about 0913R, when THRESHER reported"／認定22 "at 0913R"／J前付 p.9（位置） |
| c101-332 | OK | R08 p.185 認定12 "UQC (underwater telephone) provided the means of voice communication"・認定7 Skylark (ASR20) escort。・救難艦の一言は c304 |
| c102-334 見出し | OK | NARA 85185（materials §30・Use: Undetermined は materials どおり） |
| c102-335 | OK | R08 p.181 認定1 "the first of a new class of nuclear powered attack submarines" |
| c102-336 | ⚠️ | R08 p.185 認定16 "Experiencing minor difficulties. Have positive up angle. Am attempting to blow."＝minor を落とした（G1-01） |
| c103-338 見出し | OK | 認定17・19・20・14＝V1 p.38（見える頁）。thr_t2＝materials ○ |
| c103-339 | ⚠️ | R08 p.185 認定17 "about 0916R … garbled … about 0917R"／p.186 認定24 "UNABLE TO COMMUNICATE WITH THRESHER SINCE 0917R"＝事実は OK・改行（G1-02） |
| c103-340 | ⚠️ | 認定20 "all persons on board … died on 10 April 1963"／認定14 "Depth of water in this area is about 8500 feet"（2,590.8m）＝事実は OK・改行（G1-02） |
| c104-342 見出し | OK | 意見1（V1 p.57＝見える頁・R08 p.204）・IR18 p.1（日付の印）＋p.2（final）＋p.6（署名） |
| c104-343 | ・ | R08 p.204 意見1 "was in all probability due to: a. An initial flooding casualty … in the engine room"＝「おそらく始まり」は原文の範囲。意見を「とした」＝認定にしていない（G1-03） |
| c104-344 | ・ | IR18 p.6 "the proceedings, findings of fact, opinions and recommendations of the Court of Inquiry … are approved"＝「でも」は否定に聞こえうる（G1-03）。約2年後＝1963-06-05→1965-03-19 で21.5か月 ✓ |
| c104-345 ★ | OK | IR18 p.1 段落3 "Since the cause of THRESHER'S loss has not been determined, either by this Court of Inquiry or any other body"＝長官が事実として置いた前提。p.5 段落11 に主節で再掲＝主節を落としても意味は変わらない |
| c105-347 見出し | OK | V1 p.48＝R08 p.195 認定91c／J p.20（ホリフィールド議員が読み上げ "he gave this report as he was leaving"） |
| c105-348 Q | OK | 質問→次の行「分かっていることもある」が答える |
| c105-349 | OK | R08 p.195 認定91 "letter, serial 086 of 16 November 1962"→1963-04-10 まで145日＝4.8か月＝約5か月 ✓。・試験深度の一言は次の c106 |
| c105-350 | OK | "In my opinion the most dangerous condition that exists in THRESHER is the danger of salt water flooding while at or near test depth." |
| c106-352 見出し | ⚠️ | 意見45 を「V1 p.65」で引く＝⚠️見えない頁（kwic）→ R08 p.212（G1-04） |
| c106-353 | ・ | IR18 p.74 "a designed maximum operating depth (test depth)"＝定義の出どころが出典欄に無い（G1-30）。🔴 同じ頁の数は使わない |
| c106-354 | OK | R08 p.212 意見45 "It is known with reasonable certainty that at 0909R the THRESHER was at test depth"＝「査問会によると」で帰属あり |
| c107-356 見出し | ・ | 画＝艦橋に立つ乗員（85185 のコマ）と語り「分かっていた人はいた」が重なる（G1-05） |
| c107-357 Q | OK | 質問→次の行が答える |
| c107-358 | ⚠️ | R08 p.197 認定109 "management and workers exhibited a high degree of confidence in sil-braze joints"＝「危ないと分かっていた」は強い（G1-05） |
| c107-359 | OK | 認定102（13.8%）・認定91c（書類）＝記録に残っている ✓ |
| c108-361 見出し | OK | sources §1（台帳 xlsx・棚の更新日）＝通し頁に原文なし |
| c108-362 | ・ | sources §1「第5・6回＝査問会の記録ではない：1978年の2巻本」（G1-06） |
| c108-363 | ・ | sources §1「合計の頁＝5,348 PDF頁＋第4回327頁」＝第6回357頁を引いても5,000超 ✓。「頁」の読み（G1-28） |
| c109-365 見出し | OK | 画 p2001＝IR18 p.1（見える頁）。語り（訴え）と画（長官の意見書）はずれるが「公開された記録の見本」として可 |
| c109-366 Q | OK | 質問→次の行が答える |
| c109-367 | OK | AP "retired Capt. James Bryant, who sued for release of the documents under the Freedom of Information Act"・"himself the skipper of a Thresher-class submarine" |
| c109-368 | OK | sources §1「2020-02 に連邦地裁〈DC〉が月ごとの公開を命令」＝AP には無い（原文は通し頁に無い＝sources だけが根拠） |
| c110-370 見出し | OK | J前付 p.1 "HEARINGS BEFORE THE JOINT COMMITTEE ON ATOMIC ENERGY"。・流れ図の並びは年の順でない（1965→1964） |
| c110-371 | OK | 同 "JOINT COMMITTEE ON ATOMIC ENERGY CONGRESS OF THE UNITED STATES" |
| c110-372 | OK | 同 "JUNE 26, 27, JULY 23, 1963, AND JULY 1, 1964"＝1963年と64年 ✓ |
| c111-374 見出し | OK | IR18 p.67 "SUMMARY OF EVENTS"（・この頁に作成者の名は無い＝「法務総監の要旨」は頁からは確かめられない）／R08 p.180 "The court closed at 0921, 5 June 1963" |
| c111-375 | OK | IR18 p.67 "The Court met for the first time at 8:25 p.m. on Thursday, 11 April 1963. Before the Court closed on 5 June 1963" |
| c111-376 | ・ | IR18 p.67 "it heard 179 separate appearances of witnesses" ✓／"The Court developed 1718 pages of testimony"＝「記録の本文」より「証言の記録」（G1-07） |
| c112-378 見出し | OK | V1 p.2 索引 "Findings of Fact 1679 / Opinions 1702 / Recommendations 1715"／J p.5 "our 166 facts, 54 opinions, and 20 recommendations" |
| c112-379 | ⚠️ | 認定166（R08 p.203）が最後＝166 ✓。「認定」「意見」の語をここで立てていない（G1-08） |
| c112-380 | ⚠️ | 勧告20（R08 p.220）が最後＝20 ✓。後の章が「意見の1番」「認定の15番」と呼ぶのに「意見」が一度も紹介されない（G1-08） |
| c113-382 見出し | OK | パネル＝文字だけ（c112 と連続しない）。出典 — |
| c113-383 | ⚠️ | 事実の誤りなし（時刻の R＝現地）。前置きの区間の長さ（G1-29） |
| c113-384 | ⚠️ | 同上（G1-29） |
| c114-386 見出し | OK | nara_428-N-1057645（materials・Unrestricted） |
| c114-387 Q | OK | 質問→「追うのは3つ」が答える |
| c114-388 | ⚠️ | 改行「危ない知らせは、」で行が終わる（G1-09） |
| c114-389 | ⚠️ | R08 p.197 認定108 は超音波の結果だけ／V1 p.19 証拠111 "THRESHER CO … Ltr to BUSHIPS, Serial 086 of 16 Nov 62"（OCR 崩れ）＝前の艦長の書類は艦船局あて（G1-09） |
| c115-391 見出し | ・ | 画の欄「届かなかった知らせ」＝c114 と同じ広げすぎ（G1-09 の直しに合わせる） |
| c115-392 | OK | 方法の宣言（原文の事実を含まない） |
| c115-393 | OK | 同上 |
| c116-395 見出し | ⚠️ | 認定1 を「V1 p.34」で引く＝⚠️見えない頁→ R08 p.181（G1-04）。「深く」の出典が欄に無い（G1-10） |
| c116-396 | OK | R08 p.181 認定1 "the first of a new class of nuclear powered attack submarines" |
| c116-397 | ⚠️ | R08 p.181 認定1 "capable of diving to a depth [塗り] … to operate with reduced noise radiation"＝前の艦との比較は無い。比較は AP "dive deeper than any previous sub" だけ（G1-10） |
| c117-399 見出し | OK | NARA 83213（進水 1960）＝materials 旧版の6本。・語り「戻っていた」（1962）と画の年がずれる |
| c117-400 Q | ⚠️ | 質問「どうして？」に次の行が答えていない（G1-11） |
| c117-401 | ⚠️ | 9か月＝R08 p.195 認定92 "commenced on 16 July 1962"→p.181 認定2 "departed … on the morning of 9 April 1963"＝267日 ✓。答えになっていない（G1-11） |
| 403 区切り | OK | — |

## 第2章（405〜492行）

| 行 | 判定 | 原文の頁と短い引用（30〜80字） |
|---|---|---|
| 405 章見出し | OK | 章名「9か月の整備」＝c117 の橋と合う |
| c201-407 見出し | ・ | 画 cm_USN_1048964（進水・顔なし＝materials）。出典 認定37・38・40 に進水の年は無い→ J p.189 "July 9, 1960—Launched"（G1-30） |
| c201-408 | OK | R08 p.189 認定38 "Portsmouth Naval Shipyard built THRESHER, starting in 1958" |
| c201-409 | OK | J p.189 "July 9, 1960—Launched"／R08 p.189 認定40 "commissioned and delivered on 3 August 1961" |
| c202-411 見出し | OK | R08 p.189 認定38 |
| c202-412 | ⚠️ | 認定38 "aborted at [塗り] by instrumentation deficiencies" ✓／同じ認定 "The next sea trial, fully instrumented … was fully successful" を落とした（G1-12） |
| c202-413 | ⚠️ | 認定38 "Severe water hammer … an extensive program of hydraulic shock and impulse tests"＝「配管の衝撃の試験」が c206 の衝撃試験と紛れる（G1-12） |
| c203-415 見出し | OK | thr_t14（造船所の写真・materials ◎）・認定90・92（R08 p.195） |
| c203-416 | ⚠️ | R08 p.195 認定90 "THRESHER arrived at Portsmouth 11 July 1962" ✓。行末「〜のあとの、」（G1-13） |
| c203-417 | ⚠️ | 認定92 "a scheduled duration of six months" ✓。修飾語と名詞が別の行（G1-13） |
| c204-419 見出し | OK | 認定92・95（R08 p.195〜196）＝見込み35,000・予定日5回・10万超 ✓ |
| c204-420 | ⚠️ | 認定92 "an estimate of approximately 35,000 man-days" ✓。「1日」の読み（G1-15） |
| c204-421 | ⚠️ | R08 p.196 認定95 "successively extended from 18 January to 15 February, to 28 February, to 30 March, to 2 April, and finally to 11 April … over 100,000"＝5回 ✓。文のねじれ（G1-14） |
| c205-423 見出し | ⚠️ | 認定2 を「V1 p.34」で引く＝⚠️見えない頁→ R08 p.181（G1-04）。後始末の根拠 認定93 が欄に無い（G1-30） |
| c205-424 Q | OK | 質問→次の行が答える |
| c205-425 | ⚠️ | 認定95 "because of work added and the under-estimation of the effects of new and old work"＝事実 OK・行末の「、」で引用の「と」が次の行頭へ（G1-16） |
| c205-426 | ⚠️ | R08 p.195 認定93 "repairs found necessary as a result of inspections to be made for shock trial damage" ✓・行頭「と査問会は」（G1-16） |
| c206-428 見出し | OK | 認定79・80（R08 p.194）・認定90。図の距離 約110〜360m＝112.8／359.7m ✓ |
| c206-429 | OK | R08 p.194 認定79 "Key West area during the period 17 - 29 July 1962"＝月は言わない（§1-5 6-5）。「整備に入る前」は認定87〜90 の順（試験→潜航→回航→7月11日着）で立つ |
| c206-430 | OK | R08 p.181 認定1 "ability to resist shock"＝揺れに耐えるか ✓ |
| c207-432 見出し | OK | 認定80（R08 p.194） |
| c207-433 | OK | 認定80 "detonation of ten thousand pound charges"×0.4536＝4,536kg＝約4.5トン ✓ |
| c207-434 | OK | 認定80 "at ranges varying from 1180 feet to 370 feet"＝359.7m→112.8m ✓。括弧の原単位は §1-7 どおり |
| c207-435 Q | OK | 反応（数・事実なし） |
| c208-437 見出し | OK | thr_t22（造船所の写真）・認定84〜86（R08 p.195） |
| c208-438 | ⚠️ | R08 p.195 認定84 "there was no loss of main power, and no hull rupture was suffered" ✓。行末が「ただ、」（G1-17） |
| c208-439 | ⚠️ | 認定85 "a number of derangements occurred to joints, fittings, bolts, rivets, straps"＝「ずれ」は derangements の一部（G1-17） |
| c209-441 見出し | OK | 認定86・96（R08 p.195〜196） |
| c209-442 | ⚠️ | R08 p.196 認定96 "intensively investigated by ship's force, Bureau of Ships, and Shipyard personnel" ✓。艦船局の初出に一言が無い（G1-18） |
| c209-443 | OK | R08 p.195 認定86 "damaged items were scheduled for repair during the post shakedown availability" |
| c210-445 見出し | OK | 認定96（V1 p.49＝見えない頁→ R08 p.196 を併記ずみ） |
| c210-446 | OK | 認定（finding of fact）＝「認めている」で階層が合う |
| c210-447 ★ | OK | R08 p.196 "Despite such efforts, shock damage continued to be found during the entire post shakedown availability."＝意味 OK |
| c211-449 見出し | OK | 認定96（R08 p.196） |
| c211-450 | ・ | 認定96 "the discovery of loose condenser foundation bolts in January, 1963" ✓。「復水器」の読み（G1-27） |
| c211-451 | OK | 認定96 "a misaligned torpedo ejection pump in March, 1963" ✓。3月の日は無い＝「ひと月前」は 0.3〜1.3か月（「ひと月ほど前」が安全＝任意） |
| c212-453 見出し | OK | 意見23（R08 p.208）・勧告8（R08 p.218）＝頁は合う |
| c212-454 Q | ⚠️ | まとめ＝「見落とし」は語りがまだ言っていない評価の語（G1-19） |
| c212-455 | ⚠️ | R08 p.208 意見23 "it appears that … have not insured that all damage is found in the early intensive investigations"＝「見つからない」と断定（G1-19） |
| c212-456 | ⚠️ | R08 p.218 勧告8 "shock tests of nuclear submarines be deferred until such time as the Bureau of Ships has reassessed"＝誰が何を見直すかが抜けた（G1-20） |
| c213-458 見出し | OK | 認定69（R08 p.193） |
| c213-459 | OK | R08 p.193 認定69 "prepared by an outside firm under subcontract … used an SS(N) 588 Class Ship Information Book as a guide" |
| c213-460 | ⚠️ | 認定69 "virtually copied large portions of it, although many systems on THRESHER were quite different"＝large portions→「大部分」（G1-21） |
| c213-461 Q | OK | 反応（事実を足していない） |
| c214-463 見出し | OK | パネル（c213 は図＝文字だけの連続なし） |
| c214-464 | OK | 認定69 "not approved by the Bureau of Ships; a temporary book was provided" |
| c214-465 | OK | 認定69 "The finally approved version was not available to THRESHER even at the end of the post shakedown availability" |
| c215-467 見出し | OK | 認定166・意見53（R08 p.203・216）。画は c116 と同じ就役式（1961） |
| c215-468 Q | OK | 質問→次の行が答える（造船所の2人も含むが可） |
| c215-469 | OK | R08 p.203 認定166 a〜d（艦長・副長 1963年1月／監督 12月／補佐 11月）。・「2人」の読み＝ふたり |
| c215-470 | OK | R08 p.216 意見53 "was not conducive to optimum completion of the work undertaken"＝意見を「としている」で帰属 |
| c216-472 見出し | OK | 図の並び「11月 補佐・12月 監督」＝認定166 どおり |
| c216-473 | ⚠️ | 認定166 "Ship Superintendent in December, 1962 … Assistant Ship Superintendent in November, 1962"＝語りの並びが逆（G1-22） |
| c216-474 | OK | 認定166 "Commanding Officer in January, 1963"／R08 p.107 "within about ninety days of the conclusion"＝3か月ほど前 ✓ |
| c217-476 見出し | OK | R08 p.107（スメドバーグ中将の証言）＝画の欄の2点とも同じ頁 "We don't like to move commanding officers and executive officers during overhaul" |
| c217-477 | OK | R08 p.107 "I am the Chief of Naval Personnel"＝人事の責任者 ✓ |
| c217-478 | OK | R08 p.107 "the pressure placed on the Bureau of Naval Personnel to furnish experienced commanding officers for the POLARIS submarines" |
| c218-480 見出し | OK | R08 p.107・109 |
| c218-481 | OK | R08 p.107 "we had to have him as Prospective Commanding Officer of the JOHN C, CALHOUN SSB(N) 630"・"Commander Axene"＝中佐 ✓ |
| c218-482 | ⚠️ | R08 p.109 "I felt that Harvey was one of the best qualified people we could find."＝「」の中で we could find・I felt を落とした（G1-23） |
| c219-484 見出し | ⚠️ | 画の欄の「その圧力に抗え」「抗う」＝原文は間接話法（G1-24） |
| c219-485 | ⚠️ | R08 p.64 "Commander, Submarine Development Group TWO"＝上の部隊の司令 ✓。助言は大佐の証言＝帰属が無い（G1-24） |
| c219-486 | ⚠️ | R08 p.77 "I advised him that he must resist that pressure … He assured me that … he would resist it"／同頁 "I can't honestly cite instances."（G1-24）・「抗え」の読み（G1-26） |
| c220-488 見出し | OK | thr_t2（別の切り出し）・認定140・142・145（R08 p.200）。・142 は語りに出ない |
| c220-489 | 🔴 | R08 p.200 認定140 "it required twenty minutes to isolate a leak. This was one of the early drills. Changes had been made in the system"（G1-25） |
| c220-490 | 🔴 | 認定145 "was reported as having been completed satisfactorily, and the Commanding Officer expressed his concurrence"＝「それでも」が艦長に非を寄せる（G1-25） |
| 492 区切り | OK | — |

## 当て直した項目（§1-5・§1-6・§1-8・§1-11・§2・§9-1 のうち担当分）＝`findings_G1.json` の items

| 項目 | 判定 |
|---|---|
| §1-5 6-1 水深 約2,600m（c103） | OK（認定14 8,500ft＝2,590.8m） |
| §1-5 6-5 衝撃試験の月（c206） | OK（月を言っていない。認定79 の字面 7/17〜29 は認定90・92 と食い違う＝「整備に入る前」は認定87〜90 の順で立つ） |
| §1-5 6-10 査問会の規模（c111） | OK（IR18 p.67 179・1718）。「記録の本文」は ・（G1-07） |
| §1-6 用語（c104 査問会・c106 試験深度・c204 人日・c208 継手） | OK。ずれ：艦船局の一言が無い（G1-18）・試験深度は c105 が先に使う（・） |
| §1-8 IR18 p.1〜6（c104） | OK（段落3 の従属節＝長官が事実として置いた前提・段落11 で主節に再掲・p.2 "this final endorsement"） |
| §1-8 R08 p.77（c219） | ずれ：大佐の証言という帰属・同じ頁の「例は挙げられない」を落とした（G1-24） |
| §1-8 R08 p.107・109（c217・c218） | c217 OK／c218 ずれ（G1-23） |
| §1-8 認定38（c202） | ずれ：同じ認定の「次の試運転は完全に成功」を落とした（G1-12） |
| §1-8 AP（c109） | OK（元艦長・訴え）。「裁判所が命じて毎月」は AP に無い＝sources §1 だけ |
| §1-11 #1・#2 | OK |
| §2 #1・#2 の意味 | OK |
| §9-1 換算（2,600m・110〜360m・4.5トン） | OK |
| §9-1 日付の差（約5か月前・約2年後・3か月ほど前・ひと月前・9か月） | OK（145日・21.5か月・約90日・0.3〜1.3か月・267日） |
