# 21本目 台本 第1版 照合の記録（係 G2＝第3章 c401〜c426・第4章 c501〜c520）

- 2026-10-11・台本＝`ref/ep21/daihon_v1.md`（読むだけ・書き換えていない）
- 原文の引き方＝`v2_build/pg21.py page 委員会報告 N`（印字の頁）・`sec 11-1`（NTSB の写し）・`find`。画像は1枚も開いていない・ウェブは開いていない
- 当てた頁＝委員会報告 p4〜p8・p14〜p16・p18〜p24・p31・p35・p38・p278・p455（第1章 注66）・p458（第1章 注116）／NTSB 11便・175便（sources §11-1 #1・#2）／kousei §3-2・§6-1・§7・§8／materials §7-4／sources §8-2
- 所見＝`v2_build/findings_G2.json`（26件＝🔴1・🟡14・🟢11）。下の「判定」の「ずれ」は所見あり、「要確認」は親へ回す所

## 第3章　1機目　応答しない11便（c401〜c426）

| カット | 当てた頁 | 判定 | 一言 |
|---|---|---|---|
| c401 | p4 | ずれ（🟢） | 「Just before 8:14, it had climbed to 26,000 feet」＝合う。7,925 m＝§9 の式どおり。聞き役の問い「どこで」に、語りは時刻と高度で答えている＝G2-017 |
| c402 | NTSB 11便（§11-1 #1）・p4 | ずれ（🟡・🟢） | 8:13:29「turn 20 degrees to the right. The crew acknowledged」・8:13:47「climb … never acknowledged」＝右へ曲がる／上へ昇る／18秒後は NTSB どおり。ただし委員会 p4 は「Sixteen seconds」＝割れるのに §1-5・§9・kousei §6-1 に無い＝G2-013。「ボストン・センター」の呼び名を初出で結んでいない＝G2-016 |
| c403 | p4・p5 | ずれ（🟡） | 「8:14 or shortly thereafter」＝合う。「We do not know exactly how」の exactly が落ちた＝G2-012 |
| c404 | p5 | OK | 電話の相手＝「Southeastern Reservations Office」＝予約の窓口で合う。「About five minutes after the hijacking began」＋「At 8:19, [名前] reported」＝8時19分で合う。引いた言葉は「The cockpit is not answering, somebody's stabbed in business class … I think we're getting hijacked」の抜き出しで、意味は変わらない（Mace・息ができない は落とした＝生々しさを下げる向き） |
| c405 | p5 | OK | 「approximately 25 minutes」「calmly and professionally relayed」＝合う |
| c406 | p5 | ずれ（🟢） | 原文の主語は This＝地上へ電話したこと・範囲は「その日の何度かのうち最初」。台本は「伝え続けた」に寄せ「最初」を落とした（誤りではない）＝G2-018 |
| c407 | NTSB 11便・p18・p16 | OK | 「At about 8:21」「turned off its transponder」＝合う。トランスポンダの説明＝p16「primary radar returns do not show the aircraft's identity and altitude」の裏返しで合う |
| c408 | p18 | OK | 「seriously wrong … neither suspected a hijacking」＝合う |
| c409 | p19・NTSB 11便 | ずれ（🟢） | 8:24:38 と字は p19・NTSB で一致。「some planes」を「何機もある」＝数を強めて聞こえる＝G2-019。乗っ取った側の言葉を使うことは kousei の決め（名前の入る行を避ける）と食い違わない＝§1-4 の書き方が広すぎる＝G2-014 |
| c410 | p6・p19 | OK | 「The hijackers probably did not know how to operate … and thus inadvertently broadcast」＝probably が「とみられる」に残っている。「only heard something unintelligible」＝合う。p6 の段落が引くのは「Nobody move …」の方だが、2つの声は数秒違いで同じ意図の放送＝言い過ぎではない |
| c411 | p19 | OK | 「The next transmission came seconds later」「The controller told us that he then knew it was a hijacking」＝合う。帰属（委員会に話している）も合う |
| c412 | p19・図表 p32 | ずれ（🟡） | 「Between 8:25 and 8:32 … started notifying」＝始めた時刻に幅。「8時25分ごろから」は起点を寄せた＝G2-006 |
| c413 | p20 | OK | 「did not follow the protocol … prescribed chain of command」「took the initiative, at 8:34, to contact the military through the FAA's Cape Cod facility」＝合う |
| c414 | p20 | OK | 「former alert site in Atlantic City, unaware it had been phased out」＝合う |
| c415 | p20 | OK | 8:37:52・「first notification received by the military—at any level」＝合う |
| c416 | p20 | OK | 3つの言葉とも p20 の字どおり（F-16 を頼む部分は落とした＝問題なし）。画は字幕だけ＝§1-4 どおり |
| c417 | p458（第1章 注116） | OK | 「Vigilant Guardian, which postulated a bomber attack from the former Soviet Union」「the response was, if anything, expedited by the increased number of staff」＝if anything が「むしろ」に残る。原文は「We found」＝「とみている」はわずかに弱いが意味は変わらない（所見にしない）。演習の名は出していない |
| c418 | p20 | OK | 「ordered to battle stations the two F-15 alert aircraft at Otis … 153 miles away」＝合う。246.2 km＝§9 どおり。画は 2001年秋の別の点＝副題で断っている |
| c419 | p20 | ずれ（🟡） | 8:46 の発進＝合う。言ったのは「the officer directing the fighters」で「pressed for more information」＝「指揮をとる将校」は同じ頁の指揮官と取り違えやすく、「迫った」は強い＝G2-005 |
| c420 | p20 | OK | 「Because the hijackers had turned off the plane's transponder, NEADS personnel spent the next minutes searching their radar scopes for the primary radar return」＝合う |
| c421 | p7 | OK | 8:46:40・北棟＝合う（§1-5 どおり）。画は事件の前（1976年）＝§7 の決めどおり |
| c422 | p278 | OK | 「110 stories」「about 1,350 feet」「up to 50,000 office workers」＝合う。411.5 m＝§9 どおり |
| c423 | p20・p21 | OK | 8:53・「nine minutes」・「the most the military would receive of any of the four」＝合う（いちばん長い＝原文の most） |
| c424 | p20 | ずれ（🟡） | 「Shortly after 8:50, while NEADS personnel were still trying to locate the flight, word reached them that a plane had hit the World Trade Center」＝中身は合う。聞き役の決めつけ＝G2-002。「ぶつかった」の主語なし・報せ＝G2-003 |
| c425 | p38・p19（出典の欄は「—」） | ずれ（🟡） | 中身は p38「Boston Center bypassed the chain of command and directly contacted NEADS」で裏付けられるが、c413 の言い直しで薄い＝G2-004（p19 の FAA 本部の事実に差し替え） |
| c426 | p31・p18 | OK | p31「civilians who had never handled a hijacked aircraft that attempted to disappear」＝委員会もトランスポンダを切ったことを「姿を消そうとした」と見ている。p18 の前提1つ目と合う。「次は、2機目だ」で章の終わりの引きあり |

## 第4章　2機目　気づいていた管制官（c501〜c520）

| カット | 当てた頁 | 判定 | 一言 |
|---|---|---|---|
| c501 | p21 | OK | 「At approximately 8:42, shortly after entering New York Center's airspace, the pilot of United 175 broke in」＝合う。画は事件の前＝語り 8:42 に合う |
| c502 | p21・p7 | ずれ（🟢） | 無線の言葉＝p21「we heard a suspicious transmission on our departure out of Boston」＝合う（「everyone stay in your seats」の部分は落とした）。「last communication with the ground」＝合う。「11便の声だった」は turned out（あとで分かった）と声の主（11便の無線に流れた乗っ取った側の声）が落ちる＝G2-020 |
| c503 | p7・NTSB 175便（§11-1 #2） | OK | 「The hijackers attacked sometime between 8:42 and 8:46」＝原文も言い切り。「at 8:47, when the aircraft changed beacon codes twice within a one-minute period」＝合う |
| c504 | p21 | ずれ（🟢） | 「unaware that American 11 had already crashed」「At 8:51 … There was no response」＝合う。気づくのが遅れた理由（同じ管制官が11便も受け持っていた）を足せる＝G2-021 |
| c505 | p7・p8 | OK | 「Also at 8:52, a male flight attendant called a United office in San Francisco」「both pilots had been killed, a flight attendant had been stabbed, and the hijackers were probably flying the plane」＝probably が「たぶん」に残る。「殺され」は電話の言葉の中（…と。）＝§1-4 の死の語の決めどおり |
| c506 | p21〜p22 | ずれ（🟢） | 誰が誰に＝「The controller … contacted another controller at 8:53, saying that "we may have a hijack" and that he could not find the aircraft」＝管制官から別の管制官へ（同僚）＝合う。「どこにも」は原文に無い強め＝G2-022 |
| c507 | p22 | OK | 「At about 8:55, the controller in charge notified a New York Center manager that she believed United 175 had also been hijacked」＝合う（about が「ごろ」に残る） |
| c508 | p22 | ずれ（🟡） | 「refused to be disturbed」＝邪魔をされるのを断った。「管理職たちは…取り次がれなかった」は主語と受け身がねじれる＝G2-011。presumably＝「たぶん」は委員会の推定として通る |
| c509 | p22 | OK | 8:58・「we might have a hijack over here, two of them」＝might が「かもしれない」に残る |
| c510 | p22 | OK | 「Between 9:01 and 9:02」・3つの言葉＝合う（We need to get the military involved with us＝「軍の助けが要る」は通る） |
| c511 | p14・p16（出典の欄は「—」） | ずれ（🟢） | 「Command Center, located in Herndon, Virginia, which oversees daily traffic flow within the entire airspace system」＝中身は合う。出典の欄が空＝G2-023。「首都に近い」は地理の一般の事実 |
| c512 | p22 | ずれ（🟡×2） | "Heads up man" の話し手＝ニューヨーク・センターの管制官（ターミナルの管制との通話・9:02）＝「管制官の声」で合う。「it looks like」が落ちた＝G2-007。Lower Manhattan を「南の端」＝狭めた＝G2-008（画の欄も同じに直す） |
| c513 | p8 | OK | 9:03:11・南棟＝合う。画 wtc_smoke_day（両棟が燃える）＝語り 9:03:11 より後の絵＝合う |
| c514 | p23 | ずれ（🔴） | 「came in a phone call from New York Center to NEADS at 9:03」「at about the time」＝語りは合う（「この瞬間」と言っていない＝kousei §7 どおり）。最後の聞き役の反応が c515 の問いと2行続く＝G2-001 |
| c515 | p21〜p23（出典の欄は「—」） | ずれ（🟡×2） | 「何人もの人と段を通った」は p21〜p23 の流れ（8:51→8:53→8:55→地域の管理職は取り次がず→9:01〜9:02 コマンドセンター→9:03 NEADS）で裏付けられる。「いくつもの人」「報せ」＝G2-009。語りは 9:03 より前なのに画が当日の WTC（両棟が燃える見込み）＝G2-010 |
| c516 | p455（第1章 注66 の続き） | OK | 「The FAA knew or strongly suspected that Flight 11 was a hijacking 11 minutes after it was taken over; Flight 175, 9 minutes after」＝「知っていたか、強く疑っていた」で留保ごと合う。8:14＋11＝8:25・8:42〜8:46＋9＝8:51〜8:55 で本文とも合う |
| c517 | p20・p23・p24 | OK | 「Lacking a target, they were vectored toward military-controlled airspace off the Long Island coast」「By 9:08 … decided against holding the fighters in military airspace away from Manhattan」＝合う。決めたのは NEADS の「mission crew commander」（語りは「NEADS」＝機関で言った＝許容）。実際に待機をやめたのは 9:13（p24）＝語りは「決めた」まで＝言い過ぎではない |
| c518 | p38 | ずれ（🟢×2） | 9:05・教室で座っていた・言葉「A second plane hit the second tower. America is under attack.」＝合う。動作は「whispered to him」だけ＝「近づき」は p38 に無い＝G2-024。画（説明「9:10ごろ」の部屋のテレビ）は語りより約5分後＝要確認・親へ（原寸）＝G2-025 |
| c519 | p35 | OK | 「When they learned a second plane had struck the World Trade Center, nearly everyone in the White House told us, they immediately knew it was not an accident」＝「ほとんどの人」「と委員会に話している」で帰属ごと合う（kousei §7 の c321 の言い方どおり）。画は WTC（語りは WH）＝見たニュースの絵として通る |
| c520 | p24 | OK | 「Two minutes later, it disappeared completely from radar at Indianapolis Center」（8:56）＝「3機目は、もう管制官の画面から消えていた」で合う。章の終わりの引きあり |

## 章をまたぐ所

- **画の型の連続**（C・F）：c409〜c417 の9カット（約80秒）が続けて「図 模式」、c403〜c417 の15カットに実写が無い＝G2-026（🟢・映像方針で）
- **時刻の前後**：c423（8:53）→ c424（8:50 過ぎ・時刻は言わない）、c515（9:03 の後に 8:51〜9:02 を振り返る）、c517（9:08）→ c518（9:05「そのころ」）。どれも問い・「そのころ」で受けていて、分かりにくくはない
- **章の頭と終わり**：第3章＝問いで入り「次は、2機目だ」で終わる／第4章＝問いで入り「3機目は、もう管制官の画面から消えていた」で終わる＝引きあり
- **誤読（E）**：「報せ」（c424・c425・c515）は §6 に無い＝G2-003・G2-004・G2-009 で「知らせ」に揃える案。「北棟・南棟」が §6 に無く「北東（ほくとう）」と同じ音になりうる＝G2-015。ほか（札・要る・首席補佐官・ハーンドン・ケープコッド・アトランティックシティ・ロングアイランド・オーティス）は §6 にある
- **死の語・煽り語・チャンネル名**（D）：第3章・第4章とも「死亡」「死んだ」0。「殺され」は c505 の電話の言葉の中だけ。煽り語・チャンネル名 0
- **単位・換算**：c401（7,925 m）・c402（18秒＝NTSB）・c418（246.2 km）・c422（411.5 m）・c423（8分48秒→委員会の「9分」）＝§9 の式どおり

## §0-1 の担当項目への答え

### #4（c404「人が刺された」・c505「操縦士2人が殺され」の生々しさ）＝**線は越えていない**（いまのままでよい）
- 広告の赤（sources §8-2）は「Graphic images or accounts of shootings, explosions, executions, or bombings」＝銃撃・爆発・処刑・爆破の生々しい語り。黄は「graphic or gruesome details」。c404・c505 は「刺された」「殺され」という**事実の一語だけ**で、傷のようす・血・苦しむ声などの細部は無い
- 台本はすでに強い所を落としている：c404 は原文の「Mace…息ができない」を落とした／p6 の「a man in first class had his throat slashed」（のどを切られた）は使っていない
- どちらも報告書の地の文に引かれた**電話の報告**で、c505 の「殺され」は「…と。」で電話の言葉と分かる形（§1-4 の死の語の決めどおり）。175便の「犯人がたぶん操縦している」を伝えるのに要る事実＝削ると話が通らない
- 気をつけること：⑤の画で、刺す場面・機内の人を描かない（画の欄は「人は描かない」で合っている）。字幕で「殺され」を大きく出さない（語りと字幕だけ＝§1-4）

### #13 の一部（c424・c514 の聞き役の反応）
- **c424**「それじゃあ、ほとんど何もできないよね。」＝報告書に無い評価を聞き役に言わせる決めつけで、語りが「そう。」で認める＝**直す**（G2-002：「つまり、戦闘機は、間に合わなかったんだね？」＝c423 を受けるまとめに。数字なし）
- **c514**「知らせと、ぶつかったのが、ほとんど同じだったんだ。」＝①次の c515 の問いと聞き役の行が2つ続く ②南棟への衝突の直後（犠牲者の場面）の反応 ③語りがいま言った事実の言い直し＝**消す**（G2-001・🔴）

## 親（G0）の気になった所への答え

| 所 | 答え |
|---|---|
| c402 NTSB 8:13:29・右へ曲がる・18秒後の上昇 | §11-1 #1 の写しどおり（turn 20 degrees to the right・acknowledged／8:13:47 climb・never acknowledged＝18秒）。ただし委員会 p4 は16秒＝割れる＝G2-013 |
| c404 8時19分・電話の相手 | OK（p5：乗っ取りの約5分後に Southeastern Reservations Office へ・At 8:19 に報告） |
| c406 原文の主語と範囲 | 主語は This＝地上へ電話したこと／範囲はその日の何度かの最初。台本は寄せ方が少し違う＝G2-018（🟢） |
| c409・c411 乗っ取った側の言葉 | kousei の決め（§3-2 c8 の🔴）は「名前の入る行を避ける」で、§5 の表も CVR の例だけ＝**CVR に限った決め**と読める。c409・c411 は p19 の本文の管制の無線の字で名前なし＝食い違わない。§1-4 の書き方が広すぎる＝G2-014 で範囲を書く |
| c410「流れたとみられる」 | OK（p6 の probably がかかる＝留保は原文どおり） |
| c417 演習（p458 注） | OK（注116：Vigilant Guardian・旧ソ連の爆撃機・if anything, expedited・人が多かった＝合う） |
| c419「迫った」 | 言ったのは the officer directing the fighters（戦闘機を差し向ける役）で、誰に言ったかは書いていない。「pressed for more information」＝「迫った」は強い＝G2-005 |
| c425 薄いか | 薄い（c413 の言い直し）＝G2-004 で p19 の事実に差し替え |
| c426「姿を消そうとした」 | OK（p31 も11便などを「attempted to disappear」した機と見ている・p18 の前提1つ目と合う） |
| c502 無線の言葉 | OK（p21 の字）。「11便の声」だけ G2-020（🟢） |
| c506 8時53分・誰が誰に | OK（管制官→別の管制官＝同僚）。「どこにも」だけ G2-022（🟢） |
| c508「取り次がれなかった」・presumably | 主語と述語がねじれる＝G2-011。presumably＝「たぶん」は通る |
| c512 "Heads up man" | 話し手＝ニューヨーク・センターの管制官（ターミナルとの通話）＝合う。it looks like の落ち＝G2-007・Lower Manhattan＝「南部」＝G2-008 |
| c514 と c515 の聞き役2行 | 続いている＝🔴 G2-001 |
| c515「いくつもの人と段」 | 中身は p21〜p23 で裏付けられる（出典の欄を埋める）。言い方と画＝G2-009・G2-010 |
| c516 p455 注 | OK（knew or strongly suspected・11分・9分） |
| c517 | OK（p20・p23。決めたのは NEADS の mission crew commander） |
| c518「9時5分」「近づき、耳もとで」 | 9:05・教室・言葉は合う。動作は whispered だけ＝「近づき」は無い＝G2-024。画の時刻（9:10ごろ）は親へ（原寸）＝G2-025 |
| c519 p35 | OK（nearly everyone in the White House told us＝帰属つき） |

## 聞き役の行の点検（第3章 6行・第4章 6行）

| カット | 聞き役の行 | 役割 | 次の語り | 判定 |
|---|---|---|---|---|
| c401 | 最初の便は、どこで、おかしくなったの？ | 問い | 時刻と高度で答える | 🟢 問いと答えがずれる＝G2-017（「いつ」に） |
| c405 | 乗務員の人たちは、こういうときの訓練を、受けていたの？ | 問い | c406「訓練が教えていたのは…」 | OK（数字・非難なし・答えている） |
| c411 | つまり、まだ乗っ取りだとは、分からなかったんだね？ | まとめ | 「そう。けれど…」 | OK（「そう。」で受ける） |
| c417 | 演習と、取り違えたりしなかったの？ | 問い | 「…対応はむしろ早まった」 | OK（3行目で答える・kousei §3-2 c4 の決めどおり1回だけ） |
| c424 | それじゃあ、ほとんど何もできないよね。 | 反応 | 「そう。NEADS が…」 | 🟡 決めつけ＝G2-002 |
| c425 | つまり、ボストンは、手順の段を飛ばしてでも、急いだんだね？ | まとめ | 「そう。…」 | OK（形は合う。カットの中身が薄い＝G2-004） |
| c501 | 次の便は、そのころ、どこにいたの？ | 問い | 「175便は、ニューヨークの…受け持ちに入ったところだった」 | OK |
| c507 | つまり、地上の管制官は、もう乗っ取りだと見ていたんだね？ | まとめ | 「そう。8時55分ごろには…」 | OK |
| c511 | コマンドセンターって、どういう所なの？ | 問い | 「全米の空の流れを見渡す、FAA の司令塔だ」 | OK |
| c514 | 知らせと、ぶつかったのが、ほとんど同じだったんだ。 | 反応 | （次も聞き役） | 🔴 2行続く・犠牲者の場面・事実の言い直し＝G2-001 |
| c515 | 気づいた人はいたのに、どうして、間に合わなかったの？ | 問い | 「管制官が気づいてから…」 | OK（前提は c506〜c509 の語りの言い直し・非難の語なし） |
| c520 | つまり、地上では気づいていたのに、軍に届くのが、遅れたんだね？ | まとめ | 「そう。そしてこのとき…」 | OK |

- 数字（漢数字こみ）を言わせた行＝0（G2-002 の直す案も「戦闘機」と書き、F-15 の数字を避けた）
- 聞き役の行が2つ続く所＝c514→c515 の1か所（G2-001 で消える）
- 犠牲者の場面（c421・c513）の直後の反応＝c514 の1か所（同じく消える）。c421 の直後（c422〜c423）に反応は無い
- G2-001・G2-002 を入れると第3章 6行・第4章 5行（計 64→63）。roles21.py の表（c424 反応→まとめ・c514 を外す）を直す
