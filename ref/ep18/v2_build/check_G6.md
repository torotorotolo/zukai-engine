# 18本目 ④' G6（第11章 cb01〜cb23＋帰属の横断・実名の横断・§9-2）— 全行の記録

- **担当の行**：台本 `ref/ep18/daihon_v1.md` 1341〜1447行（第11章 `cb01`〜`cb23`）＋帰属の横断で開いた行（`c109`・`c512`・`c515`・`c817`〜`c820`・`c906`・`c912`〜`c914`・`c918`〜`c919`）
- **見た行の数**：**127行**＝担当範囲 79行（章見出し1・注1・カットの見出し行23・字幕の行54〈うち聞き役5〉）＋帰属の横断 48行（見出し13・字幕35）
- **判定の内訳（行ごと・1行に複数の所見があるときは重い方）**：OK 91／🔴 5／⚠️ 22／・ 9
  - 担当範囲 79行＝OK 47／🔴 2／⚠️ 21／・ 9
  - 帰属の横断 48行＝OK 44／🔴 3／⚠️ 1
- **所見の数**：24件（🔴 2・⚠️ 14・・ 8）＝findings_G6.json
- **引いた原文の範囲**（`kwic.py -f v2_build/q_G6.txt` と頁の全文の書き出し）：R08 p.181・184（認定4〜6）／p.194〜197（認定73〜108）／p.202（認定154〜163）／p.204〜206（意見1〜19）／p.212（意見40〜45）／p.214（意見45 Case）／p.216（意見52〜55）／p.217（勧告の頭）／p.220（勧告20）／IR18 p.1・2・5・6（第7 endorsement 段落1〜5・10〜11）／IR18 p.122〜123（第1 endorsement）／J p.3〜4・45・59・79・89・91・93〜98・122〜124・127・166・174／D（Stierman＝3:40・10:30 の所）／AP p9901（全文）／NAVSEA p9951（全文）／A-R（ルール氏の書簡＝要点の語だけ grep。🔴 冒頭の私人の住所はどのファイルにも写していない）
- 画像は1枚も読んでいない。web は開いていない。台本・既存のファイルは1文字も書き換えていない（書いたのは `v2_build/` の check_G6.md・findings_G6.json・q_G6.txt だけ）

## 1. 所見の一覧（詳しくは findings_G6.json）

| id | カット | 行 | 面 | 深刻さ | 型 | 要約 |
|---|---|---:|---|---|---|---|
| G6-01 | c515 | 763 | B | ⚠️ | 帰属の欠け | 作戦部長の会見は二次の論文（D）だけが出典なのに地の文（c512 の「論文によると」は間に査問会の2カットを挟んで切れる） |
| G6-02 | c820 | 1123 | B | 🔴 | 推測の断定化・同じ強さに | 「どの見方も一致＝空気の系統が凍って吹き出せなかった」＝査問会と司令官は「凍りやすい」まで。凍ったと言うのはルール氏だけ |
| G6-03 | cb03 | 1356 | F | ⚠️ | 出典欄の頁の欠け | 「10の課題」は J p.4（1963）にだけある。出典欄の J p.93〜98 には無く、p.98 は「16の課題と91の小課題」（1964） |
| G6-04 | cb04 | 1360 | B | ⚠️ | 方針を事実に・不自然な改行 | J p.93 は「解かれるまで続く」（will remain＝1964年の方針）→「解かれなかった」と過去の事実に。行末に次の文の頭 |
| G6-05 | cb06 | 1368 | A | ⚠️ | 不自然な改行・範囲の欠け | 「海軍航空にあるような、」が行末で「組織」と割れる。「潜水艦の安全にかかわる」出来事、の範囲が落ちた |
| G6-06 | cb06〜cb08 | 1367 | C | ⚠️ | 同じ型の3連続 | 画の欄が「書類の再現図」3連続（勧告20→認定157→意見42）・語りも査問会の文の読み上げが3連続 |
| G6-07 | cb08 | 1377 | A | ⚠️ | 専門語の初出 | 「バーベル」が語りで初出（c604 は画の欄だけ）＝潜水艦の名と分からない |
| G6-08 | cb08 | 1378 | A | ⚠️ | 分かりにくい・不自然な改行 | 「スレッシャーを失ったとみられる欠陥」＝欠陥が艦を失った主語に読める（原文＝喪失の原因とみられる欠陥）。「分析し、／伝えていれば」が割れる |
| G6-09 | cb09 | 1383 | B | ⚠️ | 原文に無い断定 | 「衝撃試験の損傷の記録も…紙に書かれていた」＝認定96 は「整備の間ずっと見つかり続けた」まで。紙の記録の有無は書いていない |
| G6-10 | cb10 | 1386 | B | ⚠️ | 上位語に広げる・範囲の欠け | 話者は艦船局の副長（艦船局の長の言葉の引用を含む）→「海軍は」。「速く遠くへ行きすぎ」は何が（攻撃と防御の力）が落ちた。2行目が「と強調した」で始まる |
| G6-11 | cb11 | 1391 | B | ・ | 可能性を断定寄りに | could be … beyond our rescue capability →「救えない艦がある」。画の欄「浅さ」と語り「深さ」 |
| G6-12 | cb13 | 1399 | B | ⚠️ | 範囲の欠け | 「わが国の艦艇建造の計画で許されてきた」が落ち、誰の考え方かが消える（造船所1か所の考え方に聞こえうる） |
| G6-13 | cb12 | 1395 | C | ・ | 同じ言い方が別の場面 | c814（J p.89）と cb12（J p.79）がどちらも「声明の結び」 |
| G6-14 | cb14 | 1403 | A | ⚠️ | 不自然な改行 | 「スレッシャーは、」が行末で、述語「警告だ」が次の行 |
| G6-15 | cb15 | 1407 | A | ⚠️ | 不自然な改行・語の欠け | 「この艦の整備と、」／「安全な運用」が割れる。原文の「状態」（conditions）が落ちた（画の欄にはある） |
| G6-16 | cb16 | 1411 | A | ・ | 分かりにくい | 「この10年の急な変化」＝何の変化か（材料・工作・運用の条件）が落ちた |
| G6-17 | cb17 | 1415 | B | ・ | 意見を結論と呼ぶ | 意見55 を「査問会は結論している」（前の行で意見と分かるので軽い） |
| G6-18 | cb18 | 1418 | D | ・ | 画と語りの取り合わせ | 追悼式の映像に「原因を決められなかったことには良い面もあった」を重ねる |
| G6-19 | cb20 | 1427 | B | ⚠️ | 範囲の欠け（画の欄） | 「1963年まで＝16隻」＝原文は「第一次大戦の始まりから1963年まで」。数の比べで期間が消える |
| G6-20 | cb21 | 1434 | B | ⚠️ | 背骨の言い過ぎ | 「足りなかったのは〜仕組みだった」＝唯一の欠けに聞こえる（意見55＝多くの慣行・状態・基準）。「人を動かす」は原文に無い |
| G6-21 | cb22 | 1437 | A | ・ | 不自然な改行 | 「名前が、」が行末 |
| G6-22 | cb23 | 1442 | B | 🔴 | 原因を決めつける問い・責める相手 | 問いが13.8%（継手）を「防げた所」に結ぶ＝本編の芯「原因は決まっていない」に反し、見た立場（造船所・艦長）へ寄る |
| G6-23 | cb03 | 1356 | E | ・ | 読みの固定 | 「10の課題」（じゅうの／とおの）が §6-1 に無い |
| G6-24 | cb07 | 1374 | A | ・ | 分かりにくい | 「海軍のどの段にも」＝at any level →「どの階層にも」 |

## 2. 担当範囲の全行（1341〜1447）

| 行 | 判定 | 原文の頁と短い引用（30〜80字） |
|---|---|---|
| 章-1341 見出し | OK | §3＝cb 23カット・54行＝数え直して一致（cb01〜cb23・字幕54行） |
| 章-1343 注 | OK | 勧告20「early consideration be given」・NAVSEA＝帰属つき（本文 cb06・cb20 で守られている） |
| cb01-1345 見出し | OK | thr_film593_b＝§7 にある。R08 p.202「159. That all submarines are now restricted to a maximum depth of 500 feet.」 |
| cb01-1346 | OK | 同上（「海軍は」＝認定159 は主語なし・J p.97「restricted, by the operational commanders」） |
| cb01-1347 | OK | 500×0.3048＝152.4→約150メートル（§9-1 と一致） |
| cb02-1349 見出し | OK | R08 p.204 意見4「it would be prudent to retain the current interim depth limitation」 |
| cb02-1350 | OK | 同「until each individual submarine's readiness has been reassessed」 |
| cb02-1351 | OK | 同「prudent」＝賢明 |
| cb03-1353 見出し | ⚠️ G6-03 | 出典欄 J p.93・94・97・98 に「10の課題」は無い（J p.98「16 tasks and 91 subtasks」） |
| cb03-1354 | OK | J p.97「the Chief of the Bureau of Ships on June 3, 1963, directed the establishment within the Bureau of a submarine safety program」 |
| cb03-1355 | OK | J p.98「BuShips Instruction 5100.18 of July 8,1963」 |
| cb03-1356 | ⚠️ G6-03・・G6-23 | J p.4「Admiral Brockett has established within the Bureau of Ships a Submarine Safety Task Group, with 10 separate tasks」 |
| cb04-1358 見出し | OK | J p.93「until all subsafe measures have been accomplished and certified by the Bureau of Ships in the case of each submarine」（1964-07-01＝J p.91・Vice Admiral Ramage） |
| cb04-1359 | ⚠️ G6-04 | 行末に次の文の頭「安全の改修を終え、」。「subsafe」の語は J p.93 が資料で最初（のちに＝可） |
| cb04-1360 | ⚠️ G6-04 | J p.93「This interim restriction … will remain in effect until …」＝方針（未来形） |
| cb04-1361 Q | OK | まとめ（roles.tsv）＝語りの直後・次の cb05 が「そう。」で受ける・数字なし |
| cb05-1363 見出し | OK | J p.94「On February 18, 1964, the Secretary of the Navy established the Submarine Safety Center at Groton, Conn.」 |
| cb05-1364 | OK | 同上 |
| cb05-1365 | OK | J p.94「projects which have been started include a subsafe manual, … casualty information collection」 |
| cb06-1367 見出し | ⚠️ G6-06 | R08 p.220 勧告20「establishment of an organization, similar to that employed in Naval Aviation」 |
| cb06-1368 | ⚠️ G6-05 | 同「in the interest of safe submarine operating procedures」（最後の勧告＝20 が最後・p.220 で署名へ続く） |
| cb06-1369 | ⚠️ G6-05 | 同「analysis of events and developments which pertain to submarine safety and the timely dissemination」 |
| cb07-1371 見出し | ⚠️ G6-06 | R08 p.202「157. That there is at present no organization at any level within the Navy with the sole responsibility for submarine safety.」 |
| cb07-1372 Q | OK | 質問＝次の行「無かった。」がそのまま答える |
| cb07-1373 | OK | 同上「sole responsibility for submarine safety」 |
| cb07-1374 | ・ G6-24 | 同「at any level within the Navy」 |
| cb08-1376 見出し | ⚠️ G6-06 | R08 p.212 意見42「could have been reduced by thorough and imaginative analysis and timely dissemination」 |
| cb08-1377 | ⚠️ G6-07 | 同「all information to be had from the BARBEL and other casualties」 |
| cb08-1378 | ⚠️ G6-08 | 同「the deficiencies which probably caused THRESHER's loss (Opinion 1)」 |
| cb09-1380 見出し | OK | NH 97555＝§7 にある。認定102・108・91c・96（R08 p.195〜197） |
| cb09-1381 Q | OK | まとめ＝cb08 の直後・次が「そう。」で受ける（答えは cb08 のバーベルの情報からスレッシャー自身の記録へ移る＝可） |
| cb09-1382 | ・（G6-09 に含む） | R08 p.197「by 29 November 1962, 145 old joints … rejection rate of 13.8 per cent」・104「reported the results of the survey」／p.195「91. … his letter, serial 086 of 16 November 1962」 |
| cb09-1383 | ⚠️ G6-09 | R08 p.196「96. … Despite such efforts, shock damage continued to be found during the entire post shakedown availability.」 |
| cb10-1385 見出し | ⚠️ G6-10 | 画の欄「海軍の2つの言葉」＝J p.95・97 の話者は Admiral Curtze（艦船局の副長＝J p.174） |
| cb10-1386 | ⚠️ G6-10 | J p.95「The genesis of this effort was not Thresher's loss but stemmed from our very first attempts」 |
| cb10-1387 | ⚠️ G6-10 | J p.97「with respect to submarine design, we moved too fast and too far in areas of offensive and defensive capabilities. Submarine safety did not keep pace.」 |
| cb11-1389 見出し | ・ G6-11 | J p.94「In April, the Deep Submergence System Review Group … submitted its recommendations」 |
| cb11-1390 | OK | 同上（1964＝J p.91 の日付） |
| cb11-1391 | ・ G6-11 | J p.94「could be disabled in water too shallow to collapse the hull and still be beyond our rescue capability」 |
| cb11-1392 Q | OK | 反応＝事実・数字なし |
| cb12-1394 見出し | OK | p8079＝§7 の文字の頁にある。J p.79（1963-07-23＝J p.59 の日付） |
| cb12-1395 | ・ G6-13 | J p.79「Now I will conclude.」（c814 の J p.89 は「My views sum up as follows」） |
| cb12-1396 | OK | J p.79「should not be viewed solely as the result of failure of a specific braze, weld, system, or component」（system は略） |
| cb13-1398 見出し | OK | 同 |
| cb13-1399 | ⚠️ G6-12 | J p.79「should be considered a consequence of the philosophy …, that has been permitted in our naval shipbuilding programs」 |
| cb13-1400 ★ | OK | 意味の照合＝主語「喪失は」・「と見るべき」は前の行・中将の意見（I believe）＝語りで示されている。落ちた範囲は G6-12 |
| cb14-1402 見出し | OK | NARA 83741＝§7。J p.127＝Admiral Rickover・1964-07-01（J p.91） |
| cb14-1403 | ⚠️ G6-14 | 改行（主語「スレッシャーは、」が行末） |
| cb14-1404 | OK | J p.127「In my opinion the Thresher is a warning made at great sacrifice of life, that we must change our way of doing business」 |
| cb15-1406 見出し | OK | R08 p.216 意見55（55 が最後の意見＝p.217 は RECOMMENDATIONS から） |
| cb15-1407 | ⚠️ G6-15 | 同「numerous practices, conditions and standards which were short of those required」 |
| cb15-1408 | ⚠️ G6-15 | 同「to insure the thorough overhaul and safe operation of the U.S.S. Thresher」 |
| cb16-1410 見出し | OK | 同 |
| cb16-1411 | ・ G6-16 | 同「rapid changes in materials, workmanship and operating conditions of submarines during the last decade and to the accelerated pace」 |
| cb16-1412 | OK | 同「They can be blamed on no individual or individuals, and many would not have come to notice had THRESHER not been lost.」 |
| cb17-1414 見出し | OK | V1 p.69（見える頁＝BLANK_V1 に無い）・R08 p.216 |
| cb17-1415 | ・ G6-17 | 意見55（opinion） |
| cb17-1416 ★ | OK | 同「cannot be charged to neglect or dereliction on the part of any individual or group of individuals」＝意味一致（誰の＝個人・集団） |
| cb18-1418 見出し | ・ G6-18 | NARA 83740＝§7。IR18 p.6 |
| cb18-1419 | OK | IR18 p.2「deserve further comment in this final endorsement」＝最後の意見書 |
| cb18-1420 | OK | IR18 p.6「The fact that we have not been able to establish the cause, however, has had its beneficial effects.」 |
| cb19-1422 見出し | OK | IR18 p.6 |
| cb19-1423 | OK | 同「Not knowing the exact cause, we have carefully examined all phases of submarine safety -- design, material and operational.」 |
| cb19-1424 | OK | 同上（§2 #1 の「主節は cb18〜19」は段落11 の文で読んでいる＝items） |
| cb19-1425 Q | OK | まとめ＝語りの直後・次の cb20 が「そう。」で受ける・数字なし |
| cb20-1427 見出し | ⚠️ G6-19 | NAVSEA「from the onset of World War I to 1963, the U.S. lost 16 submarines in non-combat related incidents」 |
| cb20-1428 | OK | NAVSEA 2023-04-06（帰属＝「海軍の艦艇の部門は、2023年に」） |
| cb20-1429 | OK | 同「Since adopting SUBSAFE procedures the U.S. Navy has only lost one submarine, USS Scorpion」 |
| cb20-1430 | OK | 同「Scorpion was not SUBSAFE-certified and sank for unknown reasons in 1968」 |
| cb21-1432 見出し | OK | thr_t1＝§7。認定108・157・意見42・勧告20 |
| cb21-1433 | OK | 認定91（1962-11-16 の手紙）・104（1962-11-29 の報告）＝事故の前の文書（認定96 の注は G6-09） |
| cb21-1434 | ⚠️ G6-20 | R08 p.216 意見55「numerous practices, conditions and standards which were short」／p.212 意見42「analysis and timely dissemination」 |
| cb22-1436 見出し | OK | R08 p.181（見える頁）「4. That the following persons … were on board when she was lost:」（名簿の USS THRESHER＝108件） |
| cb22-1437 | ・ G6-21 | 同上 |
| cb22-1438 | OK | R08 p.184「6. That all persons on board THRESHER were on board for the purpose of executing official duties.」 |
| cb23-1440 見出し | OK | 航走の写真＝§7（c101 と同じ絵） |
| cb23-1441 | 🔴 G6-22 | 改行「あなたが、」も |
| cb23-1442 | 🔴 G6-22 | R08 p.197「108. … neither the results … nor the decision … was made known」・p.216 意見55／IR18 p.1「cause … has not been determined」 |
| cb23-1443 | OK | です・ます・3行以内（§B3-7） |

## 3. 🔴 帰属の横断（全台本）

grep（「ルール」「フリードマン」「分析家」「分析官」「AP」「NAVSEA」「Stierman」「報道」「記者」「論文」「手紙」「記事」「艦艇の部門」「2013」「2021」「2023」）で拾った語りの行＝下の表と c108・c907（sources §1＝海軍の台帳・帰属の要らない事実）・c842・c1154（公文書の手紙）。漏れは無かった。

| 行 | 判定 | 原文の頁と短い引用 |
|---|---|---|
| c109-365 見出し | OK | sources §1・AP |
| c109-366 Q | OK | 質問＝次の行が答える |
| c109-367 | OK | AP「retired Capt. James Bryant, who sued for release of the documents under the Freedom of Information Act」 |
| c109-368 | OK | 裁判所の命令＝sources §1（海軍の台帳＝通し頁の外・事実の照合は担当の係） |
| c512-747 見出し | OK | D＋509-63 |
| c512-748 | OK | 帰属「論文によると」＝D「the Chief of Naval Operations learned at 3:40 p.m. that THRESHER might be in difficulty」 |
| c512-749 | OK | 同上 |
| c512-750 | OK | D「overdue and presumed missing」（509-63＝一次） |
| c515-762 見出し | OK | D |
| c515-763 | ⚠️ G6-01 | D「At a 10:30 a.m. press conference, Admiral Anderson told the press that he "reluctantly" had reached the conclusion」＝二次の論文だけ |
| c515-764 | OK | 同上（結論せざるをえない＝reluctantly） |
| c817-1107 見出し | OK | A-R |
| c817-1108 | OK | A-R |
| c817-1109 | OK | A-R「As the Analysis Officer at the SOSUS Evaluation Center in April 1963」 |
| c817-1110 | OK | A-R 2013-04-10・宛先＝OPNAV N97（海軍） |
| c818-1112 見出し | OK | 流れ図＝個人の推定の札 |
| c818-1113 | OK | 帰属「ルール氏の推定では」＝A-R「the failure at 0911 … of the primary (non-vital) electrical bus」 |
| c818-1114 | OK | A-R「which shut down the submarine's Main Coolant Pumps (MCPs) resulting in the immediate scram」 |
| c818-1115 | OK | A-R「no flooding prior to collapse」（「としている」＝帰属） |
| c819-1117 見出し | OK | （画＝艦尾の海底の写真と「どっちが正しい」の取り合わせは §5b-74③ の観点で⑤bで原寸・G6 の範囲外） |
| c819-1118 Q | OK | 質問＝次の行「記録からは、決められない」が答える |
| c819-1119 | OK | 意見2・49 と同じ線 |
| c819-1120 | OK | 「1人の元分析官の推定」＝帰属 |
| c820-1122 見出し | 🔴 G6-02 | 画の欄「3つの見方が一致する所…空気の系統が凍り、吹き出せなかった」 |
| c820-1123 | 🔴 G6-02 | R08 p.204 意見1d「A deficient air system, susceptible to freeze-up, with low capacity and low blow rate」 |
| c820-1124 | 🔴 G6-02 | IR18 p.122「inadequate capacity, susceptible to freeze-up and with an inadequate blow rate」／R08 p.214「would not be inconsistent with … a frozen reducer … or an electrical failure」 |
| c906-1166 見出し | OK | sources §1・AP |
| c906-1167 Q | OK | 質問＝次の行が答える |
| c906-1168 | OK | AP「Bryant, himself the skipper of a Thresher-class submarine」 |
| c906-1169 | OK | AP「sued … under the Freedom of Information Act」・2019＝sources §1（§9-2 に申告） |
| c912-1193 見出し | OK | AP |
| c912-1194 Q | OK | 質問＝c912〜c913 が答える |
| c912-1195 | OK | AP「retired Capt. James Bryant, who sued」 |
| c912-1196 | OK | AP「documents show …」「he said」 |
| c913-1198 見出し | OK | AP |
| c913-1199 | OK | 帰属「AP通信の記事」 |
| c913-1200 ★ | OK | AP「“There's no coverup. No smoking gun,” he said.」 |
| c914-1202 見出し | OK | AP |
| c914-1203 | OK | 帰属「ブライアント氏によれば」 |
| c914-1204 | OK | AP「the Navy's policies and procedures failed to keep pace with fast-moving technological advances during the Cold War」 |
| c918-1219 見出し | OK | A-R・AP（Friedman） |
| c918-1220 Q | OK | 質問＝次の行が答える |
| c918-1221 | OK | AP「The test depth was redacted」 |
| c918-1222 | OK | AP「previously declassified documents indicated it was 1,300 feet, said Norman Friedman, a naval analyst」／A-R「test-depth of 1300-feet」。1300×0.3048＝396→約400 |
| c919-1224 見出し | OK | 認定17・AP・A-R |
| c919-1225 | OK | A-R「0917: THRESHER message … includes the number 900」 |
| c919-1226 | OK | A-R「900-feet below the 1300-foot test-depth」／AP「suggesting the sub was 900 feet beyond its test depth」。900×0.3048＝274→約270 |
| c919-1227 | OK | 帰属「読む人もいる」・査問会は書いていない |

## 4. 実名の横断（全台本の語りと字幕の577行）

- §1-3 で「役で呼ぶ」と決めた人（ニッツェ・コース・オースティン・ブロケット・ホリフィールド・アンダーソン・ジャクソン・ズーカー・モーラー・カーツェ・カーン）＝**語りと字幕の行に0件**（画の欄・出典欄だけ＝可）
- 私人（乗員の家族・記者・参列者・AP の記事の遺族 Noonis 氏・海軍の広報官）＝0件。「記者」は c515・c912 の一般の語だけ
- 語りに出る名前＝ハーヴェイ・アクシーン・ヘッカー・ワトソン・スメドバーグ・アンドリュース・レイミッジ・リッコーヴァー・ルール・ブライアント・ウォーゼル＝すべて §1-3 の「実名」の行にある。フリードマン氏は語りでは「海軍に詳しい分析家」（画の欄だけ名前）＝可
- cb の中の役の呼び方＝「艦船局の長」（cb03）・「海軍長官」（cb18）・「中将」（cb14）＝決めどおり

## 5. §9-2（check_facts の「原文に素の形で無い数」）

- 2013＝c817 の語り・c918 の出典欄（A-R）＝通し頁に入っていない書簡の年＝申告どおり
- 2019＝c906 の語り＝sources §1＝申告どおり
- 2020＝c108・c907 の語り＝sources §1＝申告どおり
- 第11章の数（1963年6月3日・7月・10の課題・1964年2月・1964年・1963年7月・この10年・1965年・2023年・1隻・129人・13.8）はすべて通し頁に素の形である（10＝J p.4、16＝NAVSEA は画の欄だけ）。換算は cb01 の約150メートル（500フィート＝152.4m）だけ＝§9-1 と一致

## 6. ⑤b・親へ

- cb22 の名簿の頁＝R08 p.181〜184（第8回・見える頁）を使うこと。V1 p.34・36・37 は見えない頁（kwic の印）＝⑤bで原寸
- cb20 の数の比べ＝期間（第一次大戦〜1963年）と「NAVSEA 2023 の数」の札を画に入れる（G6-19）＝⑤bで原寸
- c819 の画（艦尾のつぶれた所の写真）と「どっちが正しいの？」の取り合わせ＝§5b-74③ の観点で⑤bで原寸（G6 の範囲外・c8 の係へ）
