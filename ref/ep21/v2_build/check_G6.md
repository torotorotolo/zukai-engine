# ④' 台本チェック 照合係 G6（第10章 cb01〜cb19・終章 cc01〜cc10・§1・§5〜§9）

- 台本＝`ref/ep21/daihon_v1.md`（第1版・読むだけ）。原文は `v2_build/pg21.py` で頁を引いた（委員会報告＝印字の頁）。法律・検視局・記念館・国立公園局は `src/new/web4/` の写し（2026-10-11 22:01）。画像は開いていない。ウェブは開いていない
- 判定：OK／ずれ／要確認。所見は `findings_G6.json`（G6-001〜G6-026・🔴1・🟡17・🟢8）
- 名前は書かない（原文の引用は [名前]）

## カットごと（29カット）

| カット | 当てた頁 | 判定 | 一言 |
|---|---|---|---|
| cb01 | p326 | OK | "At 8:30 that evening, President Bush addressed the nation from the White House"。画 NARA 6171390（夜の演説・大統領だけ＝materials §1-2）と合う。Q は cb02 が答える |
| cb02 | p327・p556 注24 | OK | "On the morning of September 13, the national airspace reopened for use by airports that met newly improvised security standards"＝「急いで決めた新しい保安の基準」。注24 "effective 11:00 A.M. on September 13, 2001, for flights out of or into airports that had implemented the FAA's new security requirements"＝午前11時 OK。2日後＝§9 OK。「開いた」の読み＝G6-018 |
| cb03 | p559 注61・materials §1-2 | ずれ（出典の欄） | 注61 に大統領の話として "On the evening of September 12, the President was at the Pentagon"＝報告書にも足場がある（G6-004）。13日→12日→14日と前後するが「その前の12日」で断ってあり可 |
| cb04 | materials §1-2（目録） | 要確認 | 9/14 のニューヨーク訪問は委員会報告に見つからない（下の §0-1 #11）。目録（NARA 6171391「Remarks from Ground Zero」・WHTV 609）と映像そのもので言う＝映像方針で中身を見る（親へ（原寸）） |
| cb05 | p391・PL107-71 | OK | "In November 2001, Congress passed and the President signed the Aviation and Transportation Security Act. This act created the Transportation Security Administration (TSA)"・法律 "Approved November 19, 2001" |
| cb06 | PL107-71 §44901(a)・p2・p3・p84・p391 | OK（出典に足す） | 「原則として」＝"except as otherwise provided in section 44919 or 44920 and except for … CAPPS"＝例外があるので正しい。2行目「航空会社が雇った警備の会社」＝p2・p3（claims_check K109）。出典の欄に無い＝G6-023 |
| cb07 | PL107-71 §110(c) | OK | "Not later than 1 year after the date of enactment of this Act, … shall deploy at all airports in the United States where screening is required … a sufficient number of Federal screeners"。「1年のうちに」＝法律ができてから（任意で「法律ができてから」を足すと中学生に分かりやすい） |
| cb08 | PL107-71 §104(a)(1)(B) | OK | 法律が FAA 長官に命令を出させる形（"the Administrator … shall issue an order … requiring the strengthening of the flight deck door and locks … to ensure that the door cannot be forced open from the passenger compartment"）＝「この法律が求めた」で可 |
| cb09 | p85 | ずれ（構成） | 2行とも c215 とほぼ同じ文・同じ片＝薄い。法律の §104(a)(1)(C)（飛行中は鍵をかけたまま）に替える＝G6-005・G6-006 |
| cb10 | p85 | ずれ | c308 と同じ問いと答え。原文の would have made little difference の反実仮想が落ち、語尾「書いていた」が cb09「書いている」と割れる＝G6-007（推奨は cb10 を外す＝G6-005） |
| cb11 | p391 | OK | "In November 2002, both the Homeland Security Act and the Maritime Transportation Security Act followed"・"which is now part of the Homeland Security Department"。運輸保安庁は初め運輸省の中（法律 "shall be an administration of the Department of Transportation"）＝「報告書が出たころには…その一部」で正しい |
| cb12 | p.xv（PDF p15）・sources §1 | ずれ（言い方） | "the Congress and the President created the National Commission … (Public Law 107-306, November 27, 2002)"＝「同じ2002年11月」OK。"we held 19 days of hearings"＝「19日の公聴会」は日付に聞こえる＝G6-008。刊行 2004-07-22（govinfo の書誌）＝「2004年7月」OK |
| cb13 | p393 | OK | "Improved use of 'no-fly' and 'automatic selectee' lists should not be delayed while the argument about a successor to CAPPS continues"。automatic selectee と should not be delayed は略した（意味は変わらない）。「報告書の終わりで」＝第12章（p361〜）＝「終わりのほうで」がより正確（🟢・所見にしない） |
| cb14 | p393 | ずれ | "must give priority attention to improving the ability of screening checkpoints to detect explosives on passengers"。「乗客が身に着けた」＝"screening people for explosives, not just their carry-on bags" で OK。「何より先に」は最上級に強めた＝G6-009 |
| cb15 | NCSTAR 1 PDF p3・NCSTAR 1A PDF p3・kousei §9 | ずれ | 「別に調べている」＝進行中に聞こえる（2005-09・2008-11 に最終報告）＝G6-010。「その結論は大きな話なので」＝噂の呼び水になりうる＝G6-011。爆破説の名指しは無い＝OK。画 WHTV 610 は cb04 と同じ日・同じ場所＝別の窓を選ぶ（映像方針） |
| cb16 | NCSTAR 1 PDF p1・p3（OCR） | OK | 題 "Final Report on the Collapse of the World Trade Center Towers" は表紙と扉の2頁とも OCR で字が崩れていない（崩れは別の行 "Federal BuUding"）＝②の写しで足りる。語りは NIST を引いていない（図の箱の札だけ） |
| cb17 | materials §3-3 | ずれ（画） | pentagon_court_pre＝2025-07-15・Commons の題は中庭の無人機 XQ-58A の展示。materials は副題「2025年」・「現在の」は△＝G6-012（親へ（原寸））。「25年がたった」は公開（2026-09-11 より後）の時点で正しい |
| cb18 | 国立公園局の写し・p33 | 要確認 | 頁の題 "Flight 93 National Memorial (U.S. National Park Service)"＝「国立公園局が受け持っている」OK。「墜ちた野原＝追悼の場」の字は写しの本文に無い＝G6-025（親へ（web））。画＝shanksville_day 系（2015年・materials「現在の」○） |
| cb19 | — | ずれ（聞き役） | 「どう書かれているの？」に次の語りが答えていない＝G6-013 |
| cc01 | p31 | ずれ | "We do not believe that the true picture of that morning reflects discredit on the operational personnel at NEADS or FAA facilities"＝留保（考えない）が落ちた＝G6-014。画＝救助の隊員で、語りの NEADS・FAA の人と取り違える恐れ＝G6-015 |
| cc02 | p31 | OK（🟢） | "NEADS commanders and officers actively sought out information, and made the best judgments they could on the basis of what they knew"。「指揮官たち」＝G6-022（🟢）。続く FAA の管制官を褒めた文（"executing that unprecedented order flawlessly"）は使っていない（任意）。画は cc01 と同じ注意 |
| cc03 | p311 | OK | 343・37・23 と "The FDNY suffered 343 fatalities—the largest loss of life of any emergency response agency in history" は原文どおり（最上級は報告書の字）。"emergency response agency"＝「救急や消防の組織」は狭めた側＝言いすぎにならない。「失った」は死の語の言い換えとして可（煽りではない）。「港湾公社」の読み＝G6-018 |
| cc04 | p45 | OK | "NORAD and the FAA were unprepared for the type of attacks launched against the United States on September 11, 2001. They struggled, under difficult circumstances, to improvise a homeland defense against an unprecedented challenge they had never before encountered and had never trained to meet."＝「備えが無かった」「経験も訓練も無い事態に、その場で…組み立てようとした」で合う。🔴 G0 の言う "attempted, and failed, to improvise" は **p45 に無い**（下の §0-1 の G0 の項）＝"and failed" は落ちていない。聞き役の反応＝G6-021（🟢） |
| cc05 | p31 | OK | "the NEADS air defenders had nine minutes' notice on the first hijacked plane, no advance notice on the second, no advance notice on the third, and no advance notice on the fourth"。"As it turned out"＝「記録の示した」で可 |
| cc06 | 記念館 FAQ の写し | OK | "The attacks killed 2,977 people from 90 nations: 2,753 people were killed in New York; 184 people were killed at the Pentagon; and 40 people were killed on Flight 93"。2,753＋184＋40＝2,977 ✓。画 LC-B20＝materials §7-2（崩れた後・遠くの通行人・顔は小さい）＝時刻を言わない語りなので可 |
| cc07 | p311・p552 注188 | OK | "the nation suffered the largest loss of life—2,973—on its soil as a result of hostile attack in its history"。注188 の WTC の数は "as of July 9, 2004"＝「2004年7月の時点で」OK。2,977−2,973＝4 ✓ |
| cc08 | 検視局の写し（ocme.txt） | ずれ | 中身は写しと合う（2026-08-24・市長と検視局の発表・"identification of a previously unknown victim"・"forensic investigative genetic genealogy (FIGG)"・市警と共同）。「いまも続いている」は言っていない＝§1-4 どおり。「25年がたった2026年8月」＝24年11か月13日＝G6-016 |
| cc09 | sources §1 | OK（出典の欄） | govinfo の PDF＝200・md5 が手元と同じ（2026-10-11）＝「いまも…誰でも読める」の裏付けあり。出典の欄が「—」＝G6-024。GPO は2014年から Government Publishing Office だが「印刷局」の訳で通じる |
| cc10 | — | OK | §B3-7b（誰でも答えられる・責める相手なし・です・ます・2行）。最後のカット＝ed01 の直前。画 DVIDS 122347（9/14 空撮・PD）と副題が合う |

## 台本 §1・§5〜§9

| 節 | 当てたもの | 判定 | 一言 |
|---|---|---|---|
| §1-1 題 | p31・p45・記憶 feedback-jiko-title-form・qa_out/ep7・ep15・ep16・ep19・ep20_meta.py | ずれ（🔴） | 下の §0-1 #1。字数を len で数え直すと A 93・B 90・C 83（表は 91・90・82）＝G6-001・G6-002 |
| §1-2 サムネの赤 | §B5-1・§B5-5 | ずれ | A 14・B **15**・C 14（空白とカンマこみ）＝B が上限超え＝G6-003。下の §0-1 |
| §1-3 コメントの問い | §B3-7b | OK | 下の §0-1 |
| §1-4・§1-5 | kousei §8・§10 | OK（注） | cc08 は「いまも続いている」を言わない。⚠️ kousei §10 は「言うのは『身元の確認はいまも続いている』まで」と書いていて、台本 §1-4（言わない）と食い違う。写しに無い字なので台本の側（言わない）が正しい＝kousei §10 を直すのは親へ |
| §5 使わなかったもの | 運輸長官の証言の写し・委員会報告 | OK（理由の1件は 🟢） | 「3,500」＝写しで "3,500"・"3500"・"thirty-five hundred" の3つで0件、"approximately 4500 aircraft were landed" はある＝使わない理由どおり。「最大の失敗は想像力の失敗」＝本文に3つの言い換えで0件・p339 は four kinds of failures だけ＝理由の「行末の割れ」は違う見込み＝G6-026 |
| §6 読み | 語りの全行（§4 の「> 」529行）を grep | ずれ | 報せ16・北棟5・南棟3・空の17・開いた3・港湾公社1・阻まれた1・何機2 が §6 に無い＝G6-018。「空の機」（c716）は意味も割れる＝G6-019 |
| §7 素材 | materials §1・§3-3・§7 | OK（注） | イメージ4点（c209・c210・cb06・cb08）は台本の画の欄と合う。「当日の WTC」8か所に cc03 が入っている＝OK。⚠️ cb17（2025年）・cb18（後年の追悼の場）は画の欄の頭が「実写」で写真の割合に数えている＝台本の冒頭の決め「後年の写真＝イメージ・数えない」と食い違う（実在の場所の写真なのでイメージとは違う、という読みもある）。外しても 62／237＝26.2%＝20% 以上（🟢・所見にしない＝親へ） |
| §8 用語 | 語りの初出の行 | OK | NORAD・NEADS・FAA・航空路管制センター・コマンドセンター・NTSB（c9「国の事故調査の役所」）・NIST（ca「建物を調べた国の研究機関」）・監察総監（ca「役所の仕事ぶりを調べる」）・運輸保安庁（cb05）・9.11委員会（cb12・PL 107-306）はどれも語りと食い違わない。トランスポンダ「便名と高度を知らせる」＝p16 "primary radar returns do not show the aircraft's identity and altitude" の裏返しで可。cb15 を G6-010 で「調べた」にすると §8 の NIST の説明と揃う |
| §9 式 | Python で全部計算し直した | OK（1件 🟢） | 下の §9 の表 |

### §9 の計算し直し（式の値・換算は 1ft＝0.3048m・1マイル＝1.609km・1ガロン＝3.785L）

| カット | 台本 | 計算し直した値 | 判定 |
|---|---|---|---|
| c203 | 約4万3,000L | 11,400×3.785＝43,149（3.785411784 なら 43,154＝kousei §6-3） | OK（どちらも約4万3,000） |
| c212 | 10cm | 10.16 | OK |
| c313・c617 | 約8km | 8.045 | OK |
| c401 | 約7,900m | 7,924.8 | OK |
| c402 | 18秒後 | 8:13:29→8:13:47＝18秒 | OK |
| c418 | 約246km | 246.2 | OK |
| c422 | 約410m | 411.5 | OK |
| c423 | 9分 | 8:37:52→8:46:40＝8分48秒（委員会の値 9分） | OK |
| c612 | 30分以上前 | 8:46:40→9:21＝34分20秒 | OK |
| c616 | 約10km | 9.65 | OK |
| c618 | 約670m | 670.6 | OK |
| c620 | 時速約850km | 852.8 | OK |
| c622 | 184人 | 125＋64−5＝184（p314 "All 64 people aboard … as were 125 people inside the Pentagon"・p8 乗客58＋客室乗務員4＋操縦士2＝64） | OK |
| c623 | 約240km | 241.4 | OK |
| c704 | およそ4分後 | 9:37:46→9:42＝4分14秒 | OK |
| c805 | 2分後 | 9:24→9:26 | OK |
| c806 | 約1万700m・約210m | 10,668・213.4 | OK |
| c824 | 17秒後 | 10:00:25→10:00:42＝17秒 | OK |
| c827 | 約200km | 201.1 | OK |
| c828 | 40人 | 37＋7−4＝40（p11 "only 37 passengers on United 93—33 in addition to the 4 hijackers"） | OK |
| c829 | 35分 | 9:28→10:03:11＝35分11秒 | OK |
| c902 | その4分前 | 10:03:11→10:07＝3分49秒 | OK（「4分ほど前」でもよい・担当の外） |
| c905 | 約130km | 128.7 | OK |
| c832 | 6日後 | 09-11→09-17＝6日 | OK |
| cb02 | 2日後 | 09-11→09-13＝2日 | OK |
| cc07 | 4人 | 2,977−2,973＝4 | OK |
| cc08 | 25年 | 2001-09-11→2026-08-24＝9,113日＝24年11か月13日 | **ずれ**＝G6-016・G6-017 |
| c204〜c207 | 乗員11・9・6・7 | 2＋9・2＋7・2＋4・2＋5（p4・p7・p8・p10） | OK |

## §0-1 の担当項目への答え

### #1 題の因果（§1-1）
- 型（記憶 feedback-jiko-title-form・§B4-1）＝「つかみ。もう一つの事実、N人が亡くなった〈事故名〉の真相【事故検証】【ゆっくり解説】」・67〜94字（上限100）。公開ずみの題（15・16・19・20本目）は2つ目の事実のあと「、」でつなぎ、どれも**事故の原因として報告書が書いた事実**（ナット・模型の実験・鉄筋・修理）なので因果に読めても困らない
- 9.11 の A は「残る3機は前もっての知らせが無く、2,977人が亡くなった」＝「知らせが無かったから亡くなった」と読める。委員会は p31 で4機の知らせを並べただけで、犠牲との因果は書いていない。p45 では軍の「93便は撃ち落とせた」に "We are not so sure." と返し、乗客の行動が議事堂かホワイトハウスを救ったかもしれない、と書く＝知らせがあれば助かった、は報告書より強い（§B4-5・4'-6⑤反実仮想を足す）＝**🔴（G6-001）**
- 「。」で切る案を比べた（len で数えた字数）：

| 案 | 題 | 字数 | 判定 |
|---|---|---:|---|
| A（第1版） | 軍の当直に乗っ取りの知らせが前もって届いたのは、1機目の9分前だけ。残る3機は前もっての知らせが無く、2,977人が亡くなった9.11 米国同時多発テロの真相【事故検証】【ゆっくり解説】 | 93 | 因果に読める |
| A'（「。」で切る） | 軍の当直に乗っ取りの知らせが前もって届いたのは、1機目の9分前だけ。残る3機には前もっての知らせが無かった。2,977人が亡くなった… | 96 | 型の幅（94）を2字超える |
| **A''（推奨）** | 軍の当直に乗っ取りの知らせが前もって届いたのは、1機目の衝突の9分前だけ。残る3機には無かった。2,977人が亡くなった9.11 米国同時多発テロの真相【事故検証】【ゆっくり解説】 | 90 | 因果が切れる・「衝突の」で何の9分前かが分かる（7本目「衝突9分前」と同じ）・幅の内 |
| 7本目（公開ずみ） | 軍が1機目の乗っ取りを知らされたのは衝突9分前。残る3機は墜ちるまで知らされなかった。2,973人が亡くなった…【事故検証】【映像あり】 | 84 | 7本目も「。」で切っていた＝型を崩した前例は自分の回にある |

- B（「それでも軍に届いたのはぶつかったころで、2,977人が亡くなった」）も同じ因果の読み。C（「軍が乗っ取りを知ったのも墜落の後で、…」）は93便の話で、2,977人の大半（WTC）とつながらない＝どれも「、」でつなぐ限り同じ問題。A'' を推奨

### #11 cb03・cb04 大統領の訪問（§0-1 の「cb13」は cb15 の取り違え＝G6-020）
- **9月12日のペンタゴン**：委員会報告 p559 注61 に大統領の話として "On the evening of September 12, the President was at the Pentagon and then went to the White House residence."＝報告書にも足場がある。「被害を視察」の字は無いので、語り「現場を訪れている」はこのままで、出典の欄に注61 を足す（G6-004）
- **9月14日のニューヨーク**：委員会報告で "Ground Zero"（2件＝公聴会の証人の本の題・EPA の注）・"September 14"（4件＝副大統領の新組織・サウジの便・国務省の電報）・"visited the Pentagon"・"toured"・"visited New York"・"traveled to New York"・"went to New York"（2件＝別の人）・"flew to New York"（1件＝別の人）・"WTC site"・"the site"・"rubble"・"recovery workers"・"Cathedral"・"the President visited" の14語を引いて、訪問の記述は**見つからない**（0件は無いではない）。語りは目録（NARA 6171391「Remarks from Ground Zero」・WHTV 609「Trip to New York」）と映像そのものが足場＝公的な記録の目録と実写なので「訪れた」は言ってよい。映像方針で中身（日付の札・場所）を見てから確定（親へ（原寸））
- cb15 の WHTV 610 も同じ 9/14 の束（語りは NIST＝訪問を言っていない）

### #12 cc08 検視局
- `src/new/web4/ocme.txt` の本文は1段落：2026-08-24・市長と検視局が "the identification of a previously unknown victim of the September 11, 2001 terror attacks on the World Trade Center using the breakthrough technique of forensic investigative genetic genealogy (FIGG), in collaboration with the [市警]" を発表
- 語り「ニューヨーク市の検視局が、身元の分からなかった犠牲者の1人を、新しい調べ方で確かめた、と発表した」＝合う（「世界貿易センターの」「市警と共同」は略＝意味は変わらない）。「いまも続いている」は言っていない＝§1-4 どおり（kousei §10 の書き方とは食い違う＝親へ）
- ずれは「25年がたった2026年8月」だけ＝24年11か月13日（G6-016）。⑥の時点でもう一度開くのは台本どおり

### §1-2 サムネの赤3案（§B5-1・§B5-5）
- 字数（空白とカンマこみ）：A「犠牲2,977人 猶予は9分」14／B「犠牲2,977人 知らせ9分前」**15**（上限超え＝G6-003）／C「犠牲2,977人 届かぬ命令」14
- 「犠牲N人＋核心」・死の語なし＝A・C は満たす。A の「猶予は9分」は p31 の nine minutes' notice の言い換えで、7本目の型のまま＝推奨どおり A でよい。C の核心（命令）は p43〜p44 の話で、題（9分）と核心がずれる
- 黄「9.11同時多発テロの真相」13字＝OK（§B4-4「9.11」を使う）

### §1-3 コメントの問い（§B3-7b）
- A「この動画を見て、いちばん意外だったことは何でしたか。よければ、コメントで教えてください。」＝誰でも答えられる・責める相手なし・です・ます・2行＝**A でよい**
- B「どこで知りましたか」は2001年より後に生まれた人が答えにくく、当日の体験を思い出させる。C は答えやすいが本編（空の側）との結びが弱い

### G0（親）の通し読みで気になった所
| 項目 | 結果 |
|---|---|
| cb01 8:30 の演説 p326 | OK（原文どおり） |
| cb02 p327・p556 | OK（9/13 の朝・午前11時・新しい保安の基準） |
| cb05 p391 と法律の日付 | OK（2001年11月・"Approved November 19, 2001"） |
| cb06「原則として国の職員が行う」 | OK＝法律に例外（44919・44920・CAPPS ほか）がある。2行目の出典を足す＝G6-023 |
| cb07 1年の期限 | OK（"Not later than 1 year after the date of enactment"・screening が必要な全空港） |
| cb08 扉の原文 | OK（§104(a)(1)(B)＝FAA 長官に命令を出させる形） |
| cb09〜cb10 c215・c308 の繰り返し・「書いていた」 | **薄い**＝G6-005〜007（cb10 を外すのを推奨・残すなら would have と時制） |
| cb11 p391 | OK |
| cb12「19日の公聴会」・2004年7月 | 「19日」が日付に聞こえる＝G6-008。2004年7月は OK |
| cb13・cb14 p393 | cb13 OK／cb14「何より先に」＝G6-009 |
| cb15「その結論は大きな話なので」 | 名指しは無いが呼び水になる＝G6-011。「調べている」＝G6-010 |
| cb16 NIST の題（OCR） | OK（PDF p1・p3 で題の行は崩れていない） |
| cb17「25年がたった、いまのペンタゴン」と画 | 画が2025年・中庭の無人機の展示＝G6-012 |
| cc01・cc02 p31 | cc01 の留保の落ち＝G6-014・画＝G6-015／cc02 は 🟢（G6-022） |
| cc03 p311（343・37・23・「歴史上いちばん多い」） | OK＝最上級の範囲は "of any emergency response agency in history" の FDNY だけで、語りもそこだけ |
| cc04 "attempted, and failed, to improvise" | **その句は p45 に無い**。p45 は "They struggled, under difficult circumstances, to improvise…"（スタッフ声明 p29 も同じ）。"and failed" を委員会報告で引くと6件でどれも別の話（p9 管制の呼びかけ・p111・p224・p371・p384・p564）。"improvise" 11件にも無い＝「組み立てようとした」で落ちは無い＝OK |
| cc05 | OK（p31） |
| cc06 記念館（2,977・2,753・184・40） | OK（写しと一致・足し算も合う） |
| cc07 p311 2,973 | OK（注188＝2004-07-09 時点） |
| cc08 | 25年＝G6-016 |
| cc09「印刷局のサイトで誰でも読める」 | 裏付けあり（sources §1）・出典の欄に書く＝G6-024 |
| cc10 | OK |
| §6 読み | 漏れ8語＝G6-018・c716＝G6-019 |
| §9 の式 | 全部計算し直した＝cc08 だけずれ（G6-017） |
| §8 用語 | 食い違いなし |

## 聞き役の行の点検（4'-15）

| カット | 問い | 役割（roles.tsv） | 判定 |
|---|---|---|---|
| cb01 | 空は、いつ、また開いたの？ | 質問 | cb02「2日後の9月13日、午前11時。…ふたたび開いた。」が答える。数字なし。OK |
| cb06 | 保安検査も、変わったの？ | 質問 | 「法律は、保安検査を、原則として国の職員が行うと定めた。」が答える。OK |
| cb10 | つまり、扉を強くするだけでは、足りないってこと？ | まとめ | 「そう。」で受ける。ただ c308 の問いとほぼ同じ＝カットごと外すのを推奨（G6-005・G6-007） |
| cb15 | ずいぶん、いろいろ変わったんだね。 | 反応 | 事実・数字・非難なし。犠牲者の場面ではない。OK |
| cb19 | あの朝、持ち場にいた人たちのことは、どう書かれているの？ | 質問 | **次の語りが答えていない**（「見ておく」）＝G6-013 |
| cc04 | その場で、組み立てるしかなかったんだね。 | 反応 | 「しかなかった」が決めつけを足す＝G6-021（🟢）。犠牲者の場面（cc03）の直後ではなく cc04 の語りを挟む＝可 |

- 聞き役に数字（漢数字も）・非難：なし
- 聞き役の行が2つ続く所：なし
- 犠牲者の場面（cc03・cc06・cc07・cc08）に反応なし：OK（cc04 の反応は NORAD・FAA の語りへの反応）
- cb10 を外すと、cb の聞き役は5→4・cb06→cb15 の空きは句読点なし約360字＝約59秒（最長の空き 81.7秒の内）

## 構成（C）の気づき（所見にしないもの）
- cb02（13日）→cb03（12日）→cb04（14日）と日付が前後する。「その前の12日」で断ってあるので可（並べ替えると cb01 の問いの答えがずれる）
- cb09〜cb14 は「図 模式」が6連続（扉・扉・年表・年表・箱・箱）。cb10 を外すと4連続
- cb04 と cb15 は同じ 9/14 の WTC 跡の束（副題も同じ）＝映像方針で別の窓
