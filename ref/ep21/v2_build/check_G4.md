# ④' 台本チェック 照合係 G4（第7章　4機目　93便の35分　c801〜c835）

- 台本＝`ref/ep21/daihon_v1.md`（第1版・読むだけ）。原文は `v2_build/pg21.py` で頁を引いた（委員会報告＝印字の頁）。国立公園局・AP・記念館は `src/new/web4/` の写し（④で開いたもの）を読んだ。CVR（P200056T）は OCR の字が崩れているので sources.md §11-1 #11（②が原寸で読んだ写し）を正とした。画像は開いていない。ウェブは開いていない
- 判定：OK／ずれ／要確認。所見は `findings_G4.json`（G4-001〜G4-018）
- 名前は書かない（原文の引用は [名前]）

## カットごと（35カット）

| カット | 当てた頁 | 判定 | 一言 |
|---|---|---|---|
| c801 | p10 | ずれ | 語り2行は原文どおり（8:42 離陸・"the flight's crew members were unaware of the hijacking of American 11"）。ただし聞き役の「そのとき」は直前の c716（9:46・ワシントンまで29分）を指して聞こえ、答えの「西へ向かっていた」（8:42 の話）と食い違う＝G4-001 |
| c802 | p10 | OK | "Around 9:00, the FAA, American, and United were facing the staggering realization of apparent multiple hijackings"。「らしい」＝apparent が残っている |
| c803 | p11・注79 p456 | OK（🟢） | 警告の文＝"Beware any cockpit intrusion— Two a/c [aircraft] hit World Trade Center."・"his 16 transcontinental flights"＝「受け持つ便」。「文字で」は注79 "Text messages warning the cockpit of Flight 93" で裏が取れる。送り始めは 9:19（語りに無い＝c802 の9時ごろと続けて聞こえる）＝G4-002（任意） |
| c804 | p11・図表 p33 | ずれ | 9:24 受信＝"At 9:24, [名前]'s warning to United 93 was received in the cockpit" で OK。聞き役の問い「気をつけられたんじゃないの？」に c805 はそのまま答えていない（機長の返信を言うだけ）。乗員を責める含みもある＝G4-003 |
| c805 | p10・p11 | OK | 返信の主＝"the pilot, [名前], responded with a note of puzzlement"。p10 で同じ名前が "Captain" ＝機長で合う。9:26＝"Within two minutes, at 9:26"。返信の名前（宛名・署名）は語りに出していない |
| c806 | p11・NTSB 93便（§11-1 #5） | OK | 9:28・35,000ft・700ft（§9 の式どおり 10,668m・213m）。NTSB の約600ft は言わない（§1-5） |
| c807 | p11・p28 | ずれ | 中身は原文どおり。声の主＝"the captain or first officer could be heard declaring "Mayday""・"The captain or first officer could be heard shouting: "Hey get out of here…""が語りに無く、乗っ取った側の声とも聞こえる＝G4-004。生々しさは §0-1 #4 の答えを参照 |
| c808 | p12・p28・p13 | ずれ | p28 "At 9:32, a third radio transmission came over the frequency: "Keep remaining sitting. We have a bomb on board.""＝無線に流れたのは確か。だが乗客への放送そのものは p12 "made or attempted to make the following announcement"＝留保が落ちている＝G4-005。「おそらく偽物」＝p13 "probably fake" は残っている。「この爆弾も」の「も」は c214 を受けていて可 |
| c809 | p12・NTSB 93便 | OK（🟢） | "The flight data recorder (also recovered) indicates that [名前] then instructed the plane's autopilot to turn the aircraft around and head east"。語りに「何で分かったか（FDR）」が無い＝G4-006（任意）。「来た道を」は NTSB の針路120°（南東）と厳密には違うが claims_check K079 で一致の扱い＝そのまま |
| c810 | p28 | OK | "By 9:34, word of the hijacking had reached FAA headquarters" |
| c811 | p28・p29・p42 | OK | "At 9:49, 13 minutes after Cleveland Center had asked about getting military help, the Command Center suggested that someone at headquarters should decide whether to request military assistance"。「伝わっていない」＝この時点で軍は知らない（NMCC は約10:03＝p42、NEADS は10:07＝p30）で合う |
| c812 | p30 | OK（E） | "no one from FAA headquarters requested military assistance regarding United 93. Nor did any manager at FAA headquarters pass any of the information it had about United 93 to the military" で一致。「報せ」の読み＝G4-007 |
| c813 | p29・図表 p33・p16・NTSB 93便 | ずれ | 9:41＝p29 "At 9:41, Cleveland Center lost United 93's transponder signal"・NTSB "approximately 9:41"。「切られた」＝図表 p33 "9:41 Transponder is turned off"・p16 で裏が取れる（出典の欄に図表 p33 を足すとよい）。ただし p29 は続けて "The controller located it on primary radar … and tracked the flight"＝「画面から札も消えた」で止めると見失ったように聞こえる＝G4-008。9:49（c811）→9:41 と時刻が戻る＝G4-009 |
| c814 | 国立公園局 | ずれ | "According to the FBI, thirty-seven phone calls were placed from on board Flight 93 between 9:28 … until the time of the crash at 10:03. Thirty-five of these calls were made on the Airfones located on the back of the seats in the last nine rows"＝FBI・37・35 は合う。ただし最初の電話は 9:30（同じ頁の一覧）＝c813（9:41）の後で「かけ始めた」と言うと時刻が合わない＝G4-010 |
| c815 | 国立公園局・p12 | ずれ | 「携帯は残る2本」＝"Unless noted, the calls were made on Airfones" と一覧の 9:58 の2本（客室乗務員が "used her cell phone"・乗客が "used a cell phone to dial 911 and was connected for 70 seconds"）で合う。p12 "calls from GTE airphones and cellular phones"。ただし1文目が c814 の3行目（座席の背の35本）の繰り返しで、聞き役の問い（携帯はつながらない？）への答えが2文目にずれている＝G4-011 |
| c816 | p13・p12 | OK | "During at least five of the passengers' phone calls, information was shared about the attacks …"＝「少なくとも」が残っている。2行目＝p12 "They enabled the passengers to gain critical information" |
| c817 | p13 | OK | "Five calls described the intent of passengers and surviving crew members to revolt"・"According to one call, they voted on whether to rush the terrorists in an attempt to retake the plane"。"surviving" を落としたのは可（死の語を増やさない） |
| c818 | p13 | OK | "They decided, and acted." |
| c819 | p13 | OK（🟢） | 9:57＝"At 9:57, the passenger assault began"。"loved ones" を「家族」に狭めた＝G4-012（任意） |
| c820 | p13 | OK | "immediately began to roll the airplane to the left and right, attempting to knock the passengers off balance"・"the assault continued"。原文の順（"sustained" → 揺さぶり → "continued"）とも合う |
| c821 | p13 | OK | "At 9:58:57, [名前] told another hijacker in the cockpit to block the door." |
| c822 | p13 | OK | "The cockpit voice recorder captured the sounds of the passenger assault muffled by the intervening cockpit door." 聞き役の問いにそのまま答えている |
| c823 | CVR p7（§11-1 #11）・p14 | OK | 逐語 "10:00:25 In the cockpit. If we don't, we'll die."（原寸の写し）。乗客の声＝p14 "a passenger in the background said"。委員会は 10:00:26（1秒違い＝§0-1 #7 の答え）。「死ぬ」は引いた言葉の中だけ。OCR は該当行が崩れている（字の層では当たらない＝写しを正とした） |
| c824 | CVR p7・p14 | ずれ | 10:00:42 "Roll it."＝逐語（原寸）。委員会は "Sixteen seconds later, a passenger yelled, "Roll it!""＝10:00:26＋16＝10:00:42 で、42 は両方の資料で一致。「17秒後」は委員会の「16秒後」と食い違う数を新しく作る＝G4-013 |
| c825 | p14 | OK | "stopped the violent maneuvers at about 10:01:00"＝「ごろ」が残っている |
| c826 | p14 | OK | "The hijackers remained at the controls but must have judged that the passengers were only seconds from overcoming them."＝「とみられる」で推定が残っている。"The airplane headed down" |
| c827 | p30・p14 | OK | "United 93 crashed in Pennsylvania at 10:03:11, 125 miles from Washington, D.C."（125×1.609＝201km）・"plowed into an empty field in Shanksville, Pennsylvania … about 20 minutes' flying time from Washington, D.C."。画 shanksville_day は2015年＝副題「現在の」は materials §3-3 の判定（○「現在の」）どおり |
| c828 | 記念館 FAQ・p10 | OK | "40 people were killed on Flight 93"。44（乗客37＋乗員7）−4＝40（§9）。死の語＝「亡くなった」。犠牲者の場面に聞き役なし |
| c829 | p14 | OK | "[名前]'s objective was to crash his airliner into symbols of the American Republic, the Capitol or the White House."＝原文は言い切り。「とみている」は委員会の判断としての帰属で可。35分＝9:28→10:03:11 |
| c830 | p14 | OK（E 🟢） | "He was defeated by the alerted, unarmed passengers of United 93." 「阻まれた」の読み＝G4-014（任意） |
| c831 | p14・legend #4 | OK | 乗客が操縦室に入ったとは書いていない（"The hijackers remained at the controls"）。「機を下へ向けた」＝"The airplane headed down" と p14 の "shall we put it down?"/"pull it down" の引用から言える範囲 |
| c832 | AP（Seattle Times の写し 2001-09-17）・sources §11-3 | ずれ | 「最初に伝えたのは AP」＝sources §11-3 は「これより早い報道は見つけていない＝全数ではない」＝言い切れない＝G4-015（🔴）。話し手（電話をかけていた乗客）が語りに無い＝G4-016。画の札「書き起こしには無い」は9頁の原寸で確かめていない＝G4-017 |
| c833 | CVR p7・CVR の OCR 9頁 | 要確認 | 「書き起こしにあるのは Roll it のほう」は p7（原寸）で合う。OCR の9頁で "roll" 0件・"lets" 0件・"let" 7件（"Let's go guys."＝p5 の1行・"Let get e ��."＝p6 の崩れた1行・ほかは "let them" "Let him" など）。10:00:42 の "Roll it." 自体が OCR に出ない＝OCR では「無い」と言えない＝親へ（原寸） |
| c834 | p45・p46・p47 | ずれ | 引用は原文どおり（"We are sure that the nation owes a debt to the passengers of United 93. Their actions saved the lives of countless others, and may have saved either the Capitol or the White House from destruction."・"may have" が「かもしれない」で残る）。ただし p45 は第1章（柱 "WE HAVE SOME PLANES"・1.3 は p35〜46・第2章は p47 から）＝p14 と同じ章＝「別の章で」は誤り＝G4-018 |
| c835 | p14・p155・p166（標的の一覧） | OK | 聞き役の「まとめ」→「そう。」で受けている。「狙った建物に届かなかったのは93便だけ」＝p14（93便の狙い）と標的の一覧（p166 "a preliminary list of approved targets: the World Trade Center, the Pentagon, and the U.S. Capitol"・p155）で言える |

## §0-1 の担当項目への答え

### #4（c807「メーデー」と争う音の生々しさ）
- **線は越えていない**と見る。語りは委員会の地の文（p11 "declaring "Mayday" amid the sounds of a physical struggle"・"Hey get out of here"）をそのまま訳しただけで、傷・血・死の描写が無い。録音は鳴らさない（§1-4）。広告の赤（War & conflict "Graphic images or accounts of … bombings"）の "accounts" に当たる中身（生々しい描写）は無い
- ただし声の主（機長か副操縦士）が落ちていて、乗っ取った側の叫びにも聞こえる＝G4-004 で「機長か副操縦士の声」を足す案

### #7（c823・c824 の CVR の時刻と「17秒後」）
- 逐語（P200056T p7・原寸）＝10:00:25 と 10:00:42。委員会 p14＝10:00:26 と "Sixteen seconds later"（＝10:00:42）。**10:00:42 は両方で一致**し、割れるのは1行目の1秒だけ
- 推奨＝**c824 の「17秒後の」を消し、「10時0分42秒には」だけにする**（G4-013）。「17秒」は委員会の本文の「16秒」と食い違う数を台本が新しく作る形になり、どちらの資料にも書かれていない数（計算）を言うことになる。c823 の 10:00:25 は逐語（出典の欄の1つ目）どおりで、画の帯の札とも揃うのでそのままでよい
- 直すなら §1-5 の表（CVR の2行）と §9 の c824 の行（17秒後）も合わせて直す

### #8（c832・c833「Let's roll」）
- **名前は出ていない**（AP の記事には乗客と係員の名前があるが、台本は役割だけ）＝OK
- **帰属は半分**：「電話会社の係員が聞いた、と伝えられた」はあるが、**誰の言葉か（電話をかけていた乗客の1人）が無い**＝G4-016。AP の原文は "[名前] dropped the phone after talking to [名前], leaving the line open. It was then that the operator heard his words: "Let's roll.""（乗客の妻が係員から聞いた話として）
- **「最初に伝えたのは AP」は言い切れない**＝G4-015（🔴）。sources §11-3 が「これより早い報道は見つけていない＝全数ではない」と書いている。しかも AP の記事の中に「係員は金曜（9/14）に妻へ電話した」「（電話会社は）yesterday コメントを断った」とあり、9/14〜9/16 にほかの媒体が先に書いた余地がある。「最初に」を落とし「6日後の新聞に AP の記事として載っている」とする案。最初を言いたいなら親へ（web）
- c833 の「書き起こしにあるのは Roll it のほう」は p7 で合う。画の札「書き起こしには無い」は全9頁の原寸を見ていない（sources §11-1 #11 の⚠️）＝親へ（原寸）＝G4-017

## G0 の通し読みの点への答え（まとめ）
- c803 OK（原文 p11・文字＝注79）／c804 の問い→ c805 は答えになっていない（G4-003）／c805 返信の主＝機長・9:26 OK／c806 OK／c807 声の主の落ち（G4-004）／c808 "made or attempted" の留保の落ち（G4-005）／c809 FDR の原文 OK（帰属は任意で G4-006）／c811・c812 OK／c813 9:41 OK（NTSB "approximately 9:41"・委員会 "At 9:41"）・ただし一次レーダーで追い続けた所が落ちる（G4-008）／c814「FBI によると」は国立公園局の頁にある・37本・35本 OK（時刻は G4-010）／c815「携帯は残る2本」OK・c814 と重なる（G4-011）／c816「少なくとも5本」OK／c817・c819 OK／c821 9:58:57 OK／c823 逐語 p7 の字 OK／c825・c826 留保 OK／c827 125マイル・20分 OK／c829 p14 OK／c830・c831 OK／c833 OCR では確かめきれない（G4-017）／c834 頁は p45 で合う・「別の章」は誤り（G4-018）／c835 OK

## 聞き役の行の点検（9行）

| カット | 聞き役の行 | 役割 | 点検 |
|---|---|---|---|
| c801 | 最後の便は、そのとき、どこにいたの？ | 質問 | 数字なし。ただし「そのとき」が 9:46 を指して聞こえ、答え（8:42 の離陸）とずれる＝G4-001 |
| c804 | 届いたなら、気をつけられたんじゃないの？ | 質問 | 乗員を責める含み（非難に近い）・次の語り（c805）がそのまま答えていない＝G4-003 |
| c810 | それなら、軍にも、すぐ伝わったんだよね？ | 質問 | 次の行「伝わっていない。」で答えている＝OK |
| c815 | 空の上からだと、携帯電話は、つながらないって聞いたけど？ | 質問 | 噂を「聞いた」の形で問うだけ＝OK。答えが2文目にずれる＝G4-011 |
| c817 | それで、乗客たちは、どうしたの？ | 質問 | 次の行で答えている＝OK |
| c822 | 機内のようすは、どうして分かるの？ | 質問 | 次の行（CVR）で答えている＝OK |
| c831 | 乗客たちが、操縦室に入って、機を取り戻したの？ | 質問 | 次の行「そこまでは書かれていない。」で答えている＝OK |
| c832 | 「レッツ・ロール」っていう言葉、聞いたことがあるよ。 | 反応 | 事実・数字・非難なし＝OK |
| c835 | つまり、狙われた建物には、届かなかったんだね？ | まとめ | 次の語りが「そう。」で受けている＝OK |

- 聞き役の行が2つ続く所：なし。犠牲者の場面（c828）に反応なし＝OK。数字（漢数字も）を言わせている行：なし
- 第7章の頭（c801）は聞き役から入る。第8章の頭（c901）も聞き役から入り、つなぎは自然

## そのほか（章の外・親へ）
- 「報せ」は第2章〜第8章で通しで使われている（c3xx の行296・c4xx の行439・443・c5xx の行518・c6xx の行593・599・603・615・c901・c902）。§6 に無い＝ゆっくりが「ほうせ」と読む恐れ。直すなら「知らせ」に揃える（この係の章は c812 だけ所見にした）
- 第7章の写真・実写は4/35（c801・c827・c828・c829）。c802〜c826 の25カットが続けて図＝§0-1 #2 の既知の件（新しい所見にはしない）
