# 21本目 台本 第1版 ④' 照合の記録 ── 係 G3（第5章 c601〜c624・第6章 c701〜c716）

- 2026-10-11・台本＝`ref/ep21/daihon_v1.md`（読むだけ・書き換えていない）
- 原文は `v2_build/pg21.py` で頁を引いた（委員会報告 p8〜p10・p24〜p31・p33・p34・p39・p325・p326・p455・p460〜p461・p552・p556／スタッフ声明 PDF p14〜p16／運輸長官の証言 2003-05-23 の写し／記念館 FAQ）。NTSB 77便・図表 p32〜p33 は sources §11-1（②の原寸の写し）と図表の文字の層の両方で当てた
- 🔴 名前＝スライニー・大統領・副大統領のほかは書かない（原文の引用は [名前]）。画像は1枚も開いていない（要る所は「親へ（原寸）」）
- 所見の詳細（直す案）＝`findings_G3.json`（G3-001〜G3-024）

## 1. カットごとの記録

| カット | 当てた頁 | 判定 | 一言 |
|---|---|---|---|
| c601 | p8 | OK | 8:51 の最後の定時の交信 ✓・ダレス→ロサンゼルス ✓。聞き役の「そのころ」（c520＝9:03 ごろ）から 8:51 へ時刻が戻る＝章の頭なので許容 |
| c602 | p8・p24 | OK | 8:51〜8:54・8:54 南へ ✓（NTSB の約8:55 は言わない＝§1-5 どおり） |
| c603 | p24・p25・p9 | OK | 8:56・インディアナポリス・センターが受け持ち（“which was controlling the flight”）✓ |
| c604 | p25・注142 p460 | ずれ（🟢） | 「壊れてはいない」は原文に無い（推論）。p25「FAA radar equipment tracked the flight from the moment its transponder was turned off」と注142（一次レーダーの無いレーダー・届きの弱いレーダー・ソフトが3番目と4番目のレーダーを出さない）からは筋の通る読み。「ずっと」は「切られた時から」が原文に近い＝G3-018 |
| c605 | p25・注142 p460 | **ずれ（🔴）** | 原文の理由は**2つ**：「the way the software processed radar information, **as well as from poor primary radar coverage where American 77 was flying**」。語りはソフトだけ＝G3-002 |
| c606 | p25 | OK | 「two managers and the controller … looked to the west and southwest along the flight's projected path, not east」✓（管制官たち＝責任者2人を含むまとめ方で可） |
| c607 | p25 | OK | 9:05・東・「either stopped looking … or were looking toward the west」の either/or が残っている ✓ |
| c608 | p25 | OK（出典の欄🟢） | 「In sum, Indianapolis Center never saw Flight 77 turn around.」✓。出典の欄が「—」＝G3-021 |
| c609 | p9・p455（注66）・図表 p33 | ずれ（🟡） | §0-1 #5。「2機目にぶつかったのは」は「2機目の機に衝突した」とも読める日本語。直前の c513 で「2機目＝175便」と聞いた人は混乱する＝G3-004。FAA の行（注66「There is no evidence to indicate that the FAA recognized Flight 77 as a hijacking until it crashed into the Pentagon」）✓。図表 p33 は「9:05 AA headquarters aware」＝本文の「Shortly before 9:10, suspecting」と割れる（台本は本文＝kousei §7 どおり） |
| c610 | p9・注57 p455 | OK | 電話の主＝乗客の1人（夫へ＝「家族」✓）・時刻は「At some point between 9:16 and 9:26」（語りは時刻を言わない＝割れに触れない）・中身「the hijackers had knives and box cutters」「they had put all the passengers in the back of the plane」✓。注57＝通話の記録から4本のどれが2本かは決められない（FBI と司法省は4本とも夫の職場との通話とみる）＝語りは時刻も本数も言わないので触れない。legend に77便の電話の行は無い |
| c611 | p26・図表 p32 | OK（画🟡・読み🟡） | 9:21・「FAA: Military, Boston Center. I just had a report that American 11 is still in the air」＝電話の主はボストン・センター ✓（図表「9:21 Boston Center advises NEADS」）。画の欄の札「11便はまだ飛んでいる」＝電話の逐語を画面に出す（§1-4 と二重表示）＝G3-013。「報せ」＝G3-015 |
| c612 | p26・§9 | OK（聞き役🟡） | 30分以上前（8:46:40→9:21＝34分20秒）✓・「We have been unable to identify the source of this mistaken FAA information」✓。聞き役が「もう、ぶつかった便」と事実を言う＝G3-014。「北棟」の読み＝G3-016 |
| c613 | p27・図表 p32 | OK（🟢） | 命令は 9:23 に出て「processed and transmitted to Langley Air Force Base at 9:24」・図表は「9:24 NEADS scrambles Langley」。「9時24分に命令が出た」は図表どおりだが本文では「届いた」＝G3-019。9:30 離陸・「not headed north toward the Baltimore area as instructed, but east over the ocean」✓ |
| c614 | p27 | OK | 理由3つ＝①命令に目標までの距離と場所が無い ②決まった形の飛行計画で真東（090）へ60マイルと思い込んだ ③先頭の操縦士と地元の FAA の管制官が、その指示が元の命令より優先と思い込んだ ✓（画の札3つも合う）。聞き役はまとめ→「そう。」✓ |
| c615 | p9・p25・図表 p33 | OK | p9「Dulles Terminal Radar Approach Control」＝ダレスの進入管制（空港の周りを受け持つレーダー管制）・p25「Several of the Dulles controllers」・図表「Dulles tower」。「ダレス空港の管制官たち」は中学生向けの言い方として可 |
| c616 | p27・p34 | ずれ（🟡） | 「南西」✓（p27 の言葉は「six miles southeast … Six, southwest」と言い直し・p34 は southwest）＝語りは南西で問題ない。「数分後」✓（p34「Then, minutes later」・p27 では 9:36）。ただし「報せが入る」は、NEADS が11便のことで自分からかけた電話で**たまたま**知った（p27「it had come by chance」）ことを落とす＝G3-006 |
| c617 | p9・NTSB 77便 p2（§11-1 #3） | ずれ（🟡） | 「そのとき」＝直前の c616 の最後の文（数分後＝9:36）を指して聞こえる。原文の「American 77 was then 5 miles west-southwest」の then は **9:34**＝G3-005。「時計回り」＝NTSB「a right 330-degree descending turn」（出典の欄に NTSB が無い） |
| c618 | p9・§11-1 #4・kousei §7 c418 | OK | 2,200ft＝670.6m ✓・「pointed toward the Pentagon and downtown Washington」✓・NTSB 図2（FDR の高度）＝9:34 ごろから約4分で地上へ ✓（kousei §7 の「一気に」は使っていない） |
| c619 | p25・p26 | OK | 輸送機に頼んだのは**レーガン・ナショナル**の管制官（「Reagan National controllers then vectored an unarmed National Guard C-130H」）✓・「identified it as a Boeing 757」✓（地の文で＝kousei §7） |
| c620 | p10・§9 | OK | 9:37:46・「approximately 530 miles per hour」＝時速約850キロ ✓ |
| c621 | p26 | OK | 「at 9:38, seconds after impact, reported to the control tower」✓ |
| c622 | 記念館 FAQ・p552（第9章 注188）・§9 | OK（出典🟢） | 記念館「184 people were killed at the Pentagon」✓。「乗っ取った5人は入っていない」は記念館の頁に無い＝p552「The Pentagon attack killed 184 nonterrorists」で言える＝G3-022。画 `pentagon_west_day` の撮影日（副題「当日」）は materials §7-3 で人の写りだけ確かめた＝日付は親へ（G3-024） |
| c623 | p27・スタッフ声明 PDF p14・p34 | ずれ（🟡） | 「The Langley fighters were about 150 miles away」＝**何から**は書いていない。直前の文（「faded over Washington」「The Pentagon had been struck」）からワシントン（ペンタゴン）からと読める。聞き役の「どこに」に答えていない＝G3-009。画（夕方・外の環が崩れた後）が語りの 9:38 より後の姿＝G3-010 |
| c624 | p26・注154 p461・注76 p456・NTSB 77便 図2 | OK（出典🟢） | 757 の見分け ✓。「飛行の記録装置も回収され」＝注154「Commission analysis of FDR」・注76（77便の CVR は焼けて読めず）・NTSB 図2 が FDR の高度＝出典の欄に無い＝G3-023。757 の見分けは c619 と重なる（🟢・任意） |
| c701 | p25・図表 p33・p10・注67・注68 p455 | **ずれ（🔴）** | 9:25 の全米の離陸停止は**コマンドセンター**が出した（p25「While this was being discussed by executives at FAA headquarters, the Command Center ordered one at 9:25」・図表「Herndon Command Center orders nationwide ground stop」）✓。「もう飛んでいる機には、まだ何も言っていない」は誤り＝ボストン・センターは自分の空域の便に警告を出し（注67）、コマンドセンターも 9:19 にデルタ1989便への警告を命じた（注68）。同じ台本の c804 でも 93便に 9:24 に警告が届いている＝G3-001。「まず9時25分」＝アメリカン航空の全米の地上待機（9:05〜9:10）の方が先＝G3-007 |
| c702 | p9・p10 | ずれ（🟡） | 9:00 に知って北東部の未出発の便を止めた ✓。「のちに全米へ」＝p10「American Airlines' nationwide ground stop between 9:05 and 9:10」＝FAA の 9:25 より**前**。「のちに」だと c701 の後と聞こえる＝G3-008 |
| c703 | p29 | OK | 「The Command Center's national operations manager, Ben Sliney」✓ |
| c704 | p29・§9 | OK（構成🟡） | 9:42・news reports・4分14秒＝およそ4分 ✓ |
| c705 | スタッフ声明 PDF p15 | 構成（🟡） | 「At 9:42, Command Center learned from television news reports」✓。ただし「テレビの」1語のためだけの薄いカット＝c704 に寄せて外す案＝G3-012 |
| c706 | p29・スタッフ声明 p15 | OK | 「ordered all FAA facilities to instruct all aircraft to land at the nearest airport」✓（スタッフ声明は all airborne aircraft） |
| c707 | p29・注165 p461・図表 p32〜p33・スタッフ声明 p15〜p16・p326・注24 p556 | OK | 命令の時刻は**どこにも書かれていない**（「land」「nearest airport」「grounded」「unprecedented」「all civil」「airspace was」で当てた）。本文は「9:42 に報道で知った」の次の文に命令を置くだけ。⚠️ c716 の画の欄「9:42 の命令」と食い違う＝G3-011 |
| c708 | p29・p326・証言 | OK | 原文「commercial and general aviation aircraft」＝自家用機は一般航空（自家用・社用の小型機など）の中学生向けの言い方として可。降ろしたのは民間機（p326「all nonemergency civilian aircraft」・証言「except military and medical traffic」）＝「すべて」は旅客機と自家用機を並べた後なので民間機と聞こえる。c709 の「小型機」と言い方が揃っていない（任意） |
| c709 | p29 | OK | 「handled it with great skill」「about 4,500」「soon landed without incident」✓（約・まもなく が残っている）。読み＝G3-017 |
| c710 | p39・p325 | OK | 「Air Force One departed at about 9:54 without any fixed destination」✓（p325 は airborne 9:55＝1分の割れ・「ごろ」で足りる）。聞き役の反応→「その一方で」で受ける＝可 |
| c711 | p325 | OK | 「Air Force One flew to Barksdale Air Force Base in Louisiana」✓（着陸は about 11:45） |
| c712 | 運輸長官の証言 2003-05-23 | **画（🔴）** | 語り ✓（「at approximately 9:45 a.m. … I gave the FAA the final order for all civil aircraft to land at the nearest airport as soon as possible」）。**画が大統領の電話**＝命じたのが大統領と見える＝G3-003 |
| c713 | p29・p326・証言 | OK | §0-1 #6＝帰属どおり（報告書はスライニーの命令・長官の名は本文では 9/11 夜の NSC の場面だけ＝p326／長官の言葉は本人の証言）。聞き役の問い「誰の命令」に、2つの出どころを並べて答える＝可 |
| c714 | p31・p10・注67 p455・スタッフ声明 p19 | OK（🟢） | 範囲 ✓：「Individual FAA controllers, facility managers, and Command Center managers thought outside the box in recommending a nationwide alert, in ground-stopping local traffic, and, ultimately, in deciding to land all aircraft」＝主語は FAA の管制官・施設の責任者・コマンドセンターの責任者のまとめ。全米の警報を求めた具体の場面は 9:07 のボストン・センター（p10・注67）＝全米の警報が出た跡は無い（注67）＝語りは「求め」で止めている ✓。「決まりの外まで考えて」は規則破りとも聞こえる＝G3-020 |
| c715 | p30 | OK | 93便について FAA 本部は軍に助けを求めなかった（p30）✓。まとめ→「そう。」✓ |
| c716 | p29・スタッフ声明 p16 | OK（画🟡） | 9:46・「twenty-nine minutes out of Washington, D.C.」✓。画の欄「9:42 の命令のころ」が c707 と食い違う＝G3-011 |

## 2. §0-1 の担当項目への答え

### #5 c609（アメリカン航空の本社が「2機目は77便かもしれない」と考えた）
- **混乱する**、と判断した。理由は2つ
  1. 「2機目に**ぶつかった**のは77便」は日本語として「2機目（の機）に衝突した」とも読める（原文は「the second aircraft to hit the World Trade Center」＝ビルにぶつかった2機目）
  2. 視聴者は c513 で「2機目＝175便が南棟に 9:03:11」と聞いたばかり。本社の**読み違い**だと言わないと、台本が食い違っているように聞こえる
- 直す案（G3-004）：「ビルにぶつかった2機目は、77便かもしれない、と考えた。実際は175便だ。」（37字）
- もう1つの案：この節ごと外して「9時10分の少し前、アメリカン航空の本社は、77便が乗っ取られたと疑っていた。」で止める（c609 の芯は「会社は疑った／FAA は認めた跡が無い」の対比なので、それだけで足りる）

### #6 c712・c713（全機着陸の命令＝委員会の書き方と運輸長官の証言の並べ方）
- **語りは帰属どおり**：委員会報告は命令の主をスライニー（p29）と書き、時刻は書かない（本文 p29・注165・図表 p32〜p33・スタッフ声明 p15〜p16・p326・注24 で確かめた）。運輸長官の名は報告書の本文では 9/11 夜の NSC の場面（p326）だけで、着陸の命令の話には出ない。「9:45ごろ」「最後の命令（the final order）」は長官の 2003-05-23 の証言の写しのとおり。c713 が「報告書は〜」「本人の証言として〜」と出どころを分けて答えているので、どちらかを事実と決めつけていない
- **崩しているのは画**：
  - c712 の画が「大統領専用機の機内で電話をする大統領」＝語りは長官なのに、命じたのが大統領に見える（G3-003・🔴）。案＝その写真は語りの合う c710（専用機が飛び立つ）へ移し、c712 は図（全米の地図＋「運輸長官の証言（2003年の公聴会）」の札・時刻と言葉は字幕だけ）
  - c716 の画の欄「9:42 の命令のころ」が c707「時刻は書かれていない」と食い違う（G3-011）
- 任意：「最後の命令」は「その日の最後の命令」とも聞こえる。原文の final は「最終的な」なので「最終の命令」も候補（c712・c713 の2か所を揃えて）。直さなくても誤りではない

## 3. 親（G0）の通し読みで気になった所への答え

| 所 | 答え |
|---|---|
| c604「壊れてはいない」 | 原文に無い（推論）。p25 と注142 からは筋が通る＝🟢 で言い換え案（G3-018） |
| c605 理由はソフトだけか | **違う**。続きがある＝「as well as from poor primary radar coverage where American 77 was flying」（p25）・注142 も同じ（🔴 G3-002） |
| c608「見ていなかった」 | p25「In sum, Indianapolis Center never saw Flight 77 turn around.」✓（出典の欄に足す＝G3-021） |
| c610 電話の主・時刻・中身 | 乗客の1人→夫（家族）・「At some point between 9:16 and 9:26」・ナイフとカッター・乗客を全員後ろへ ✓。注57＝4本の通話記録のどれが2本かは決められない（語りは時刻も本数も言わない＝触れなくてよい）。legend に77便の電話の行は無い |
| c611 電話の主・言葉 | ボストン・センター ✓（p26「Military, Boston Center」・図表 9:21）。言葉 ✓（原文は「I just had a report that …」＝伝え聞きの報告） |
| c613・c614 理由3つ | p27 ✓（距離と場所が無い／決まった形の飛行計画で真東60マイルと思い込んだ／その指示が元の命令より優先と思い込んだ） |
| c615 Dulles TRACON の言い方 | 「ダレス空港の管制官たち」で可（p25 も「the Dulles controllers」） |
| c616「南西」 | p27 の言い直し（southeast→southwest）と p34 の southwest のとおり＝問題ない |
| c617「そのとき」 | 食い違う＝5マイル西南西は 9:34（p9 の then）・c616 の「数分後」は 9:36（🟡 G3-005） |
| c618「最後の4分ほど」 | sources §11-1 #4（NTSB 図2）どおり ✓ |
| c619 C-130H に頼んだ管制 | レーガン・ナショナル ✓（p25） |
| c623 150 miles は何から | 原文は書いていない。文脈（ワシントン上空・ペンタゴン）からワシントンと読める（🟡 G3-009） |
| c624 | 答えになっている。FDR の出典が欄に無い（🟢 G3-023） |
| c701 9:25 は誰の命令 | コマンドセンター（本文 p25・図表 p33）✓。ただ「まだ何も言っていない」は誤り（🔴 G3-001） |
| c702 9時ごろ | 9:00 に知って北東部を止めた ✓／全米は 9:05〜9:10（p10）＝「のちに」が誤解を生む（🟡 G3-008） |
| c704・c705 | c705 は「テレビの」のためだけ＝薄い（🟡 G3-012） |
| c707 時刻 | 本文・注・図表・スタッフ声明のどれにも無い ✓。c716 の画と食い違う（🟡 G3-011） |
| c708「自家用機」 | 可（一般航空の言い換え）。c709「小型機」と揃えるかは任意 |
| c710 9:54 | p39 ✓（p325 は 9:55） |
| c711 p325 | ✓ |
| c712 画 | 合わない（🔴 G3-003） |
| c714 全米の警報 | p31 は FAA の管制官・施設とコマンドセンターの責任者のまとめ。具体は 9:07 のボストン・センターの申し入れ（p10・注67）＝語りの範囲で合う |
| c716 9:46 | ✓ |

## 4. 聞き役の行の点検（第5章 7行・第6章 5行）

| カット | 行 | 役割 | 判定 |
|---|---|---|---|
| c601 | その次の便は、そのころ、どこを飛んでいたの？ | 質問 | OK（数なし・次の行が直に答える） |
| c604 | レーダーが、壊れていたの？ | 質問 | OK（答えの「壊れてはいない」は G3-018） |
| c608 | つまり、画面に出ないあいだに、逆の方へ飛んでいたんだね？ | まとめ | OK（「そう。」で受ける） |
| c612 | もう、ぶつかった便なのに、まだ飛んでいるって？ | 反応 | **🟡** 聞き役が「もう、ぶつかった」と事実を言う＝G3-014（案「えっ、その便が、まだ飛んでいるって？」） |
| c614 | もう無い便を追って、しかも、違う方へ飛んだってこと？ | まとめ | OK（c612・c613 で語った事のまとめ・「そう。」で受ける） |
| c623 | 戦闘機は、そのとき、どこにいたの？ | 質問 | 🟡 答えの行に「どこから」が無い＝G3-009。犠牲者の行（c622）の直後だが質問なので反応の禁止には当たらない |
| c624 | ペンタゴンにぶつかったのは、本当に旅客機だったの？ | 質問 | OK（ミサイル説を名指ししない・次の行が直に答える） |
| c701 | そのあいだ、空の上のほかの飛行機は、どうなっていたの？ | 質問 | 🟡 答えの1行目は地上の離陸の停止、3行目が「まだ何も言っていない」（誤り）＝G3-001 の案で「もう飛んでいる機は、そのままだ」と直に答える形になる |
| c708 | 空にいる飛行機を、全部、降ろすってこと？ | 質問 | OK |
| c710 | そんなにたくさんの飛行機が、無事に降りられたんだ。 | 反応 | OK（犠牲者の場面ではない・数なし） |
| c713 | 結局、空を閉じたのは、誰の命令だったの？ | 質問 | OK（出どころを分けて答える） |
| c715 | つまり、空の流れを止めるところは、うまくいったんだね？ | まとめ | OK（「そう。」で受ける） |

- 数字（漢数字も）を言う聞き役の行＝0。聞き役の行が2つ続く所＝0（c623 と c624 は間に語りが1行ある）

## 5. そのほか（所見にしなかった観察）
- 構成：c706〜c710 が「全米の地図」の図で5カット続く。G3-003 の案（大統領の写真を c710 へ）で c710 が実写になり、続きは4カットに減る。代わりに c712〜c715 が図で4カット続く
- 構成：c601 の「そのころ」（9:03 ごろ）→ 8:51 へ戻る。章の頭なので許容
- 構成：c619 と c624 で「757 と見分けた」が2回。c624 はミサイル説への答えなので重ねる意味はある（任意）
- 読み：「330度」「184人」「8分13秒」「西南西」「捉えていた」は §6 に無いが読み誤りの恐れは低いとみた（⑤a で耳）
- 画：c609・c701・c705（＋第4章 c514・c515・c519）に「当日の世界貿易センター（A）・両棟が燃える・別の点」が要る。A の WTC は14点。materials §7-4 で両棟が燃えると確かめた2点（c5 の欄）は議会図書館の `wtc_smoke_day`（C'）と小学校の部屋のテレビの画面で、A の WTC の14点の中身はまだ誰も見ていない＝足りるかは親へ（原寸）（G3-024）。c622 の `pentagon_west_day` の撮影日（副題「当日」）も、materials §7-3 は人の写りだけを見た＝目録の日付を親へ
