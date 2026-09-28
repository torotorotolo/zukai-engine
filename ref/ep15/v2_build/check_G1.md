# check_G1 — 15本目 ④'【見る】 G1＝第1章 c101〜c112・第2章 c201〜c220

- 担当＝`ref/ep15/daihon_v1.md` 340〜474 行（第1章 12カット・第2章 20カット）
- 見た行＝**100行**（見出し行 32＋字幕行 68＝第1章 12＋25・第2章 20＋43。§3 の表の行数と一致）
- 判定の内訳＝OK 76行／⚠️ 15行／🔴 1行／・ 8行（1行に2件付いた行は重い方で数えた。「OK・E G1-11」＝事実は合い、読みの注記だけ付いた行は OK に数えた）
- 所見＝20件（🔴1・⚠️11・・8）＝`findings_G1.json`
- 原文＝`ref/ep15/src/ep15_pages.txt`（kwic で引き直した）＋ドケットの txt（#17・#53・#59 を Grep）。facts・kousei・台本 §1〜§2・§9 の「原文」は引き写していない
- 字の長さ＝全行を数えた（1行41字超 0・1文40字超 0）。同じ語尾3字の3連続 0
- 報道の文言（c103 の通説）＝**未照合・親へ**。写真・図の写り＝**⑤bで原寸**

| 行 | 判定 | 原文の頁と短い引用 |
|---|---|---|
| c101-340 見出し | OK | 実写 B4＝materials §3-1（飛んでいる事故機を真下から）。副題「事故のレースの周回中」は materials §10-2 の許す範囲＝写りは⑤bで原寸。出典 AAB p10 |
| c101-341 | OK | AAB p10「On September 16, 2011 … National Championship Air Races … Reno/Stead Airport (RTS), Reno, Nevada」 |
| c101-342 | OK | AAB p10「an experimental … P-51D … collided with the airport ramp in the spectator box seating area」・p12「delivered … December 23, 1944」（古い戦闘機） |
| c102-344 見出し | OK | 図 p28＝「Table. Summary of events.」が p28 にある。出典 p28・p10 |
| c102-345 | ⚠️ G1-06・E G1-11 | AAB p28 表「0 Airplane rounds pylon 8, begins to roll through 73° left bank」…「~9.1 Airplane impacts ground」＝約9秒は合う。ただし0秒の時点で既に73°傾いている（「傾き始め」ではない）。「9秒」の読み |
| c102-346 | OK | AAB p10「The pilot and 10 people on the ground sustained fatal injuries」 |
| c103-348 見出し | OK | AAB p27「Figure 10. Inboard piece of left elevator trim tab separated. Photograph courtesy of Julia Kirchenbauer.」 |
| c103-349 | ⚠️ G1-12 | roles.tsv＝質問。次の語りは「何が起きたか」でなく「当時の報道の見立て」を答える |
| c103-350 | OK（報道の文言は未照合・親へ） | 「尾翼の小さな板」＝left elevator trim tab の言い換え。「板」の階層＝tab で、c104 の「板の一片」（inboard piece）と同じものを指す＝上位語への広げは無い |
| c104-352 見出し | OK | quote・出典 AAB p28 |
| c104-353 | ・ G1-13・E G1-11 | AAB p28 表「1624:30.20 1.3 Airplane reaches maximum vertical acceleration」／本文 p28「during the pitch-up maneuver, the maximum vertical load factor reached about 17.3 G」＝機首上げは表の行でなく本文 |
| c104-354 | OK | AAB p28「1624:33.5 4.6 Inboard piece of left elevator trim tab is separated」。4.6−1.3＝3.3→約3（注33＝時刻の精度は写真ごとに違う＝「約」で足りる）。19字 |
| c105-356 見出し | OK | AAB p32「Figure 14. Locknut in the left elevator trim tab outboard hinge. … an exemplar new locknut」＝左の板のナットと新品 |
| c105-357 | OK | AAB p31「The locknuts showed evidence of yellow paint beneath the uppermost coat of paint」（左右の板のナット全部＝左の板を含む＝「その板」で可） |
| c105-358 | OK | AAB p41「indicates that the locknuts had likely been installed for at least 26 years because the airplane’s trim tabs were painted yellow before the 1985 NCAR」＝likely→とみられる・at least→以上 |
| c106-360 見出し | ・ G1-14 | AAB p52「the probable cause … was the reduced stiffness of the elevator trim tab system … deteriorated locknut inserts … screws to become loose … fatigue cracking in one screw … failure of the left trim tab link assembly, elevator movement, high flight loads, and a loss of control」＝鎖から「かたさの低下」が落ちている |
| c106-361 | 🔴 G1-01 | AAB p31「all of the inserts showed evidence of age and reuse」・p41「had likely been installed」「The screws were likely tightened 4 days before the accident flight」・p16「The right elevator trim tab screws were also removed and reinstalled」 |
| c106-362 | OK（「そう。」の受け先は G1-01） | AAB p52 推定原因（ナットの詰め物の劣化→ねじのゆるみ→…→操縦を失う） |
| c107-364 見出し | ⚠️ G1-09 | AAB p11「The pilot, age 74」・p35「The accident pilot was the president of the company that owned the accident airplane」・#17 p2（p7002）「Operator: James K. Leeward」。「何度もリノを」の頁（p12）が出典欄に無い |
| c107-365 | OK（実名は承認の事項） | #17 p2「Operator: James K. Leeward」・AAB p35「president of the company that owned the accident airplane」（#59 p8 も「Both corporations have Mr. Leeward as president」） |
| c107-366 | ⚠️ G1-09 | AAB p11「age 74」・p12「The accident pilot raced the airplane in the NCAR from 1983 through 1989」・#17 p4（p7004）「Mr. Leeward raced the airplane at Reno under three different names through 1989」 |
| c108-368 見出し | OK（図の中身は⑤bで原寸） | #33 p15（p2015）「Figure 13: NCAR Ramp Area Layout」＝キャプションは合う。「斜めの空撮・燃料車・事故地点」は文字で確かめられない |
| c108-369 | OK | AAB p10・p19「collided with the airport ramp in the spectator box seating area」 |
| c108-370 | OK | AAB p19「a fuel truck was parked on the ramp near the pits」 |
| c109-372 見出し | OK | panel・出典— |
| c109-373 | OK | roles.tsv＝質問→次の行「3つの問いだ」が答える |
| c109-374 | OK・E G1-11 | —（予告）。「9秒」の読み |
| c109-375 | ・ G1-20 | —（3つ目だけ問いの形でない） |
| c110-377 見出し | OK | AAB p1「Accident Brief NTSB/AAB-12/01」＝表紙 |
| c110-378 | OK | AAB p10「National Transportation Safety Board … Aircraft Accident Brief」 |
| c110-379 | OK | AAB p11 注6「the video study in the public docket for this accident」 |
| c111-381 見出し | OK | panel |
| c111-382 | OK | AAB p10 注1「all times in this brief are Pacific daylight time」＝UTC−7。日本 UTC+9＝16時間 |
| c111-383 | OK | §B1 |
| c112-385 見出し | OK | 実写 D4＝materials §3-5「Reno Stead Field (3392833169)・BY-SA 2.0（2009-03-28）・高空から空港と周りの町」 |
| c112-386 | ⚠️ G1-10 | AAB p10「Reno/Stead Airport (RTS)」＝c201 1行目とほぼ同じ文が続く |
| c112-387 | OK | 橋の1行 |
| c201-393 見出し | OK | Googleアース①（materials §7） |
| c201-394 | ⚠️ G1-10 | AAB p10「Reno/Stead Airport (RTS), Reno, Nevada」 |
| c201-395 | OK | AAB p16「wind was from 240° at 15 knots with gusts to 21 knots, visibility 10 miles, clear sky conditions … temperature 22°C」。240°＝西南西（236.25〜258.75°） |
| c202-397 見出し | OK | A4＝materials §3-2「Strega の離陸の滑走・9/16 16:14ごろ」 |
| c202-398 | OK | AAB p10「National Championship Air Races (NCAR)」 |
| c202-399 | OK | #33 p15「closed course pylon racing」・AAB p10「six-lap race」 |
| c203-401 見出し | OK | A3＝materials §3-2「Voodoo（2位の機）がタキシング」。勧告書 A-12-08 p1（p6001）注1 |
| c203-402 | OK | roles.tsv＝質問→403 が答える |
| c203-403 | OK | AAB p10 注2「one of six NCAR race classes, includes several types of modified propeller-driven, reciprocating-engine-equipped airplanes」・p6001「six race classes: jet, sport, T-6, formula I, biplane, and unlimited」 |
| c203-404 | OK | AAB p10 注2「may operate at ground speeds in excess of 435 knots」。435×1.852＝805.6。may→「こともある」 |
| c204-406 見出し | ⚠️ G1-04 | E85＝materials §3-2「レースのパイロン（鉄塔）と上に立つ審判2人」⇔ #33 p9（p2009）注4「Course pylons are constructed out of a barrel mounted at the top of a telephone pole … about 50-feet」 |
| c204-407 | ⚠️ G1-04・E G1-11 | AAB p17「featured 10 pylons (plus 2 guide pylons), and the course distance was about 8.4 miles」。8.4×1.609＝13.5。「塔」⇔ telephone pole。「10本」の読み |
| c204-408 | OK | AAB p43「(all turns on the race course are to the left)」 |
| c205-410 見出し | OK | AAB p11「Figure 1. Diagram of the NCAR unlimited class race course at RTS, showing relative locations of pylons and the accident site」 |
| c205-411 | ・ G1-16 | AAB p10「traveling about 445 knots as it passed pylon 8」＝824.1。勧告書 p6001「Its airspeed was about 460 knots (530 mph)」＝資料の中の食い違い（AAB が後で最終） |
| c205-412 | OK | AAB p10「in third place during the third lap of the six-lap race」 |
| c206-414 見出し | ⚠️ G1-08 | 出典欄「—」＝一次資料に無い一般の事実 |
| c206-415 | ⚠️ G1-08 | 原文なし（新幹線の営業最高＝時速320キロ）。824÷320＝2.58＝「2倍を超える」は正しい |
| c206-416 | OK | roles.tsv＝反応・数字なし |
| c207-418 見出し | OK | A1＝materials §3-2「Strega（1位の機）がタキシング」 |
| c207-419 | ⚠️ G1-05 | AAB p10「trailing the second-place airplane (Voodoo …) by about 4.5 seconds and the lead airplane (Strega …) by about 8.8 seconds」＝「秒前に」が時刻の「前」にも聞こえる |
| c207-420 | OK | AAB p10「another experimental P-51D」「also an experimental P-51D」・注2「modified」 |
| c208-422 見出し | OK | A5＝materials §3-1「最後の離陸の滑走・9/16 16:15ごろ（推定）」。副題「事故のレースの離陸」＝§10-2 の範囲 |
| c208-423 | ⚠️ G1-07 | AAB p10「about 1625 … departed RTS about 10 minutes before the accident」＝「午後4時15分ごろ」は引き算で原文に無い・§9 に申告が無い（#17 p2 は「Time: 1626」） |
| c208-424 | OK・E G1-11 | AAB p10「about 10 minutes before the accident」。「10分前」の読み |
| c209-426 見出し | OK | #33 p9（p2009）「Figure 7: NCAR Unlimited Race Course Overlaid onto Google Earth」 |
| c209-427 | ・ G1-15 | AAB p17「the showline located on the south edge of runway 8/26」・注18「a prominent, readily visible ground reference, such as a river, runway, taxiway」＝引いた線ではなく滑走路の端そのもの |
| c209-428 | OK・E G1-11 | AAB p16〜17「all flights conducted at altitudes less than 1,000 feet agl must remain north of the showline」。×0.3048＝304.8 |
| c210-430 見出し | OK | quote・出典 p17（「大会を許可した」は p16） |
| c210-431 | ⚠️ G1-03 | AAB p16「The FAA issued a certificate of waiver or authorization on September 2, 2011, to enable the NCAR」・p17「no closer than 500 feet horizontally from the primary spectator areas for all aircraft」＝原単位だけの行 |
| c210-432 | ⚠️ G1-03 | AAB p17 同上。500ft＝152.4m。primary（主な）を落とした＝p46 で主な観客席はピット〜ボックス席〜一般席＝実害なし |
| c211-434 見出し | OK | AAB p20「Figure 3. NCAR ramp area layout with accident site depicted.」 |
| c211-435 | OK | roles.tsv＝質問→436 が答える |
| c211-436 | OK | AAB p19「The edge of the box seating area was 874 feet south of the showline」＝266.4 |
| c212-438 見出し | OK | Googleアース②（materials §7） |
| c212-439 | OK | AAB p19「the edge of the pit area (where many other spectators were located) was 748 feet south of the showline」＝228.0 |
| c212-440 | ・ G1-19 | AAB p19「a fuel truck was parked on the ramp near the pits」＝c108 2行目と同じ締め |
| c213-442 見出し | OK | panel 152・228・266（AAB p17・p19） |
| c213-443 | OK | roles.tsv＝質問 |
| c213-444 | ⚠️ G1-02 | AAB p19「Racing airplanes were expected to fly parallel to the showline on the north side」＝報告書は「満たしていた」と判定していない（874/748 はショーラインからの距離・500ft は飛行からの距離） |
| c213-445 | OK・E G1-11 | AAB p17「AC 91-45C stated that the unlimited racing class … “requires a spacing of 1,000 feet between the spectator area and the showline.”」。「第8章」の読み |
| c214-447 見出し | OK | AAB p38「qualified in fourth place for the unlimited class gold race during a flight on September 13, 2011」 |
| c214-448 | OK・E G1-11 | AAB p38 同上（13日→16日＝3日前）。「3日前」「4位」の読み |
| c214-449 | OK | AAB p10「unlimited class gold race」・p38 同 |
| c215-451 見出し | OK | panel・出典 p17・p18 |
| c215-452 | OK | AAB p17「The airplane was not equipped (and was not required to be equipped) with a flight data recorder or cockpit voice recorder」 |
| c215-453 | OK | AAB p17〜18「RCATS Systems telemetry system … transmitting it via data link … to a ground station」 |
| c216-455 見出し | OK | panel・出典 p29 |
| c216-456 | OK | AAB p29「true airspeed and vertical load factor during its final turn around pylon 8 … were similar to its speeds and load factors during its previous two turns」 |
| c216-457 | OK・E G1-11 | AAB p29「maximum 458-knot GPS ground speed between pylons 6 and 7」＝848.2。「6と7」の読み |
| c217-459 見出し | OK | panel・出典 p29 |
| c217-460 | OK | AAB p29「was the fastest that the airplane had flown on the course by about 35 knots」＝64.8 |
| c217-461 | ・ G1-18 | AAB p29「The accident flight had the highest engine manifold pressure and rpm (compared with all previous flights for which there were data)」 |
| c218-463 見出し | OK | panel・出典 p29 |
| c218-464 | OK | roles.tsv＝まとめ。語りが 460 で「最高より速い」と言い終えた直後・次が「そう。」 |
| c218-465 | ・ G1-17 | AAB p29「About 8 seconds before the beginning of the upset, there was a noticeable reduction in engine manifold pressure and rpm」＝起点は upset の始まり＝合う。「横転」はここが初出 |
| c218-466 | OK | AAB の本文に理由の記述なし（p18 は項目名・p29 だけ）。ドケットも理由は書かない＝#53 p9「the engine was cut back」・#59 p11「There was a reduction in power … appears valid」 |
| c219-468 見出し | OK（写りは⑤bで原寸） | B2＝materials §3-2 B1〜B3「Strega を真下から＝事故のレースの周回中（推定）」 |
| c219-469 | OK | AAB p35「both Voodoo and Strega had about 70° left bank through the turn past the accident airplane’s upset point」 |
| c219-470 | OK | AAB p10「trailing」 |
| c220-472 見出し | OK | panel・出典 p11・p28 |
| c220-473 | OK | AAB p11 注6「study calculations performed using photographs, video footage, and telemetry data」「video footage … provided by ground witnesses」 |
| c220-474 | OK・E G1-11 | AAB p28「The table below summarizes events in the sequence」。「9秒」の読み |
