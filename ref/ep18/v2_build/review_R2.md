# 18本目④' 第2版の当て直し R2（第7〜11章 c701〜cb23・節の差し替え v2_sect_Z）

- 見た数：**143**＝変わったカット 84（c7 18・c8 16・c9 17・ca 14・cb 19）＋節の差し替え 59
- 指摘：**🔴 0 ／ ⚠️ 5 ／ ・ 3**（返り値の issues と同じ。⚠️＝c904・c916・c917・c918・c820、・＝c720・cb07・§1-8 意見45）
- 引いたもの：`kwic.py`（FOR・R08・J・IR18・AP・NAVSEA・T）／ルール氏の書簡の文字（本文だけ・冒頭の住所は写していない）／`titles18.py`（exit 0）／`tools/check_facts.py`（原文に素の形で無い数 2件＝2013・2020／決め所 19件中 当たらない 0件）
- 形の機械チェック（c701〜cb23）：最長41字＝c709・c720・cb10（上限ちょうど）／★は全部20字以内／1カット1〜3行（＋聞き役）／波ダッシュなし／煽り語は c913「隠蔽」（既知）だけ
- 直しの案の字数（句読点なし）：c9 の中で c904 −1・c905 −2・c916 +2・c917 −1（+1 −2）・c918 ±0＝**−2**。c820・§1-8 は画の欄と節だけ（語りの字は変わらない）

## カット

| カット | 判定 | 原文の頁と短い引用 | メモ |
|---|---|---|---|
| c701 | OK | J p.32 注 "displace water from the ship's ballast tanks thereby increasing buoyancy" | 「海水を入れて沈み」を消した＝引いた頁に無い |
| c702 | OK | R08 p.190 認定49 "reducing valves … fitted with conical mesh strainers" | 「その弁には」＝弁に付いた、で合う |
| c704 | OK | R08 p.190 認定46 a〜d（並列） | 「そのため」→「しかも」＝因果を外した。c703「なのに」から続く |
| c705 | OK | R08 p.190 認定47 "is not well recognized" | |
| c706 | OK | 認定48 | 改行だけ |
| c708 | OK | J p.32 "Depth is not significant insofar as freezeup" | 改行だけ |
| c709 | OK | R08 p.26 "until about 2:00 o'clock on the morning that we sailed at 6:00" | 41字（上限） |
| c711 | OK | R08 p.33 "after some discussion it was decided that this would not be prudent" | 受け身＝1人が決めた形にしていない。聞き役の「吹き切って」は c712（J p.38 full deballast）に合わせた語＝許容 |
| c712 | OK | J p.38 "As I understand it, it never has been done." / "That is right, sir." | 画の欄の注（J p.37 Maurer）も原文どおり |
| c713 | OK | J p.83 "the Navy from the time of the 400-foot submarine … did not basically change the blowing requirements" | 主語＝海軍・「基本的に」あり。400ft×0.3048＝121.9m |
| c715 | OK | R08 p.191 認定50 "Under a test required by the court, strainers in the reducers of the TINOSA were blocked and ruptured by the formation of ice in about thirty seconds" | ★19字＝decisions §2 の例どおり。blocked は c716「タンクへの空気が止まった」が受ける。前の行「同じ型のティノサで」は c714 と重なるが決めどおり（直さない） |
| c716 | OK | J p.32・p.112 注 "During the tests, ice formed on the screen-type wire strainers … cutting off air flow" | 試験の話と分かる。まとめ→c717「そう。」 |
| c717 | OK | R08 p.191 認定51 "air banks 2, 3 and 4 would automatically be shut off … It takes thirty seconds" | 設計の説明（「かかる」）＝当日の出来事にしていない |
| c719 | OK | R08 p.212 意見45 "either stopped or were slowed to 'SLOW mode'" | 「分からない。」＝止まったか遅い回し方か割れる。質問に答える |
| c720 | ・ | R08 p.213 "In Case I … 3. Power lost at 0911R when pumps stop … not highly probable, mainly due to … decreased depth only about 100 feet" | 前提と評価は合う。ただ評価の理由は軌跡。c802（意見1b＝電気が引き金の原子炉の自動停止＝おそらくの原因）と食い違って聞こえないか＝最もありうる Case III は 0911 に遅い回し方・停止はそのあと（R08 p.213〜214）。判断は係へ。41字 |
| c721 | OK | J p.112 "I don't know. I don't think so." | 改行だけ |
| c722 | OK | J p.112 Curtze "we had written orders to take them out and it hadn't been done yet"・Kern "We don't believe they were."・J p.35 "those have been removed" | 帰属＝少将と大佐。画は⑤b（G4-17） |
| c723 | OK | R08 p.211 意見39 "simulating a full blow at test depth" | |
| c801 | OK | 意見1 | 改行だけ |
| c803 | OK | 意見1c・d | まとめ→c804「そう。」 |
| c805 | OK | R08 p.212 "It is recognized that the specific nature of the THRESHER loss cannot be determined by assumptions and computer solutions" | 外した "It is impossible, with the information now available…" は同じ向きの断り＝意味は減らない。「認めている」＝recognized |
| c808 | OK | 意見5 a〜f | まとめ→「そう。」 |
| c809 | OK | 意見2 "there is a danger … conjecture may be stretched too far … thus narrowing" | may を保った |
| c811 | OK | 意見49 "we do know enough to make it necessary for us to explore in depth the many possible causes" | 40字。反応 |
| c812 | OK | IR18 p.1 "SEVENTH ENDORSEMENT on VADM Bernard L. AUSTIN … ltr of 7 June 1963"・p.5 "has not been determined despite … Probably" | 「査問会の報告に添えた」＝査問会の長の書簡（報告）への7番目の書き添え＝正しい |
| c813 | OK | IR18 p.6 | 改行だけ |
| c816 | OK | J p.89 "(b) I do know there were weaknesses in her design, fabrication, and inspection" | まとめ→c817「そう。」 |
| c817 | OK | 書簡 "By Bruce Rule"・"As the Analysis Officer at the SOSUS Evaluation Center in April 1963" | 39字 |
| c818 | OK | 書簡 "no flooding prior to collapse of the THRESHER pressure-hull"・"failure at 0911 … shut down the … MCPs resulting in the immediate scram" | 帰属は1行目「推定では」＋2行目「としている」 |
| c819 | OK | — | 改行だけ |
| c820 | ⚠️ | 意見1d "in all probability due to … d. A deficient air system, susceptible to freeze-up"・書簡 "unable to deballast because of the formation of ice" | 帰属は行ごと・強さ（おそらく…とみた／とみる）も原文どおり。ただ**語りの順**＝査問会→ルール氏→（c821）司令官、**画の欄の順**＝査問会→司令官→ルール氏＝声と画面がずれる。画の欄の「おそらくの原因」も字の崩れ |
| c821 | OK | IR18 p.122 "This grossly unsatisfactory situation … Immediate steps have been taken in operating ships to: (1) remove high pressure air reducer strainers" | 40字 |
| c822 | OK | R17 p.97 | 写真を原因と結びつけていない |
| c823 | OK | — | 「塗られている」に揃えた |
| c901 | OK | — | 「長く、」を外した |
| c902 | OK | J p.147 "Any unauthorized release would seriously affect our nuclear ship and Polaris programs." | 「当時の」＝1963年の長官（1965年の長官と分けた） |
| c903 | OK | J p.160 "use security classification to protect the people from the truth … specifically designate what information in the hearing records is properly classified" | 「反発した」をやめた |
| c904 | ⚠️ | J p.164 "The hearings transcript should at this time maintain its classified status … a poor time indeed to release piecemeal" | 語りは原文どおり。**足した聞き役「その記録は」**が c902 の査問会の記録とも取れ、c905 が第1版の「公聴会の記録」を落としたので「査問会の記録が1965年に出た」と聞こえる（c906・c907 と食い違う） |
| c905 | OK | J 前付 p.3 "WASHINGTON: 1965 For sale"・J p.93 "These dives [classified matter deleted] feet"・J p.124 "for [classified matter deleted] feet or any other depth" | 「証言の中の深さの数字も、削られている」は原文どおり（J p.122〜123 も深さが塗り）。約240（239） |
| c906 | OK | AP "who sued for release of the documents under the Freedom of Information Act"・"himself the skipper of a Thresher-class submarine" | 「あの訴え」は c109 を受ける。訴え→公開のつながりは第1版から（AP は並べて書く） |
| c907 | OK | 台帳・棚（decisions §5） | 「2023年5月までに」＝棚の日付を公開日と言わない |
| c908 | OK | V1 p.54 "b(3) 10 USC 130"・R08 p.181 b(6)・V1 p.38 b(1) | 「3種類」＝通し頁の文字の層を機械で数えて b(1)・b(3)・b(6) だけ（ほかの番号は0） |
| c909 | OK | V1 p.38 | 「塗られている」 |
| c910 | OK | — | 艦名の行を消した。白い四角は⑤b |
| c911 | OK | — | 「捜索の」＝289-T に1963年の写真も入る（G5-28） |
| c915 | OK | J p.122 | 改行だけ |
| c916 | ⚠️ | J p.122 "It was originally just on the basis of cost."・"There has been no real evaluation made yet." | G7-104 の「強める語」は**所見の誤り**（第1版の「元は、費用だけが根拠だった」は原文どおり）。替えた文も原文にあるが、反応「元は、お金の計算だったんだ。」の「元は」を受ける文が語りから消えた |
| c917 | ⚠️ | J p.124 "the depth to which we would go is what the state of the art will allow us. Therefore, there is not a tactical justification for [classified matter deleted] feet or any other depth." | 「その数字に」は "or any other depth" を落とし、範囲を狭めた（画の欄は「その数字にも、ほかのどの深さにも」） |
| c918 | ⚠️ | 書簡 "test-depth of 1300-feet (580 psi)"・"the 1300-foot test-depth"／AP "The test depth was redacted but previously declassified documents indicated it was 1,300 feet, said Norman Friedman, a naval analyst" | ルール氏「書簡に…と書いた」は書簡の字どおりで良い。分析家の中身も推定にしていない。ただ「AP通信の記事の分析家も」は分析家が AP の人に聞こえる＝§4-2 の「記事で／によると」の形に |
| c919 | OK | AP "'900 north' suggesting the sub was 900 feet beyond its test depth" | 「ごろ」 |
| c920 | OK | — | 質問→ca01「いや、…」が答える |
| ca01 | OK | J p.169 "lasted nearly 5 months and involved more than three dozen ships and thousands of men" | |
| ca02 | OK | R08 p.65 "10 miles by 10 miles centered at the point called datum" | 数を言わない（§4-1） |
| ca03 | OK | R08 p.65 "LORAN-A … can't get your position any closer than a mile and a half" | 1.5マイル＝2.41〜2.78km→「2キロ半ほど」 |
| ca04 | OK | R08 p.66 "a very easy operation … the camera must be 30 feet from the spot … an airplane 8500 feet high" | 8,500ft＝2,591m。質問に答える |
| ca06 | OK | R08 p.171 "the small object in one segment of the circle"・"trigger weight" | |
| ca08 | OK | J p.169 "Trieste's gondola" | ガソリンの浮きを消した（§4-11） |
| ca09 | OK | J p.169 "the Trieste made a total of 10 dives"・J p.30 "the expedition of the Trieste yesterday? … No results, sir." | |
| ca10 | OK | — | 説明文と写りは⑤b（G5-31） |
| ca13 | OK | J p.169 "On September 5, 1963 … terminated"・"no part of Thresher's pressure hull was sighted or photographed" | 「1964年2月の時点でも」を外しても同じ意味（1963年の捜索のまとめ）。まとめ→ca14「そう。」 |
| ca14 | OK | No.710-64 | |
| ca15 | OK | T p9801 "The operations were conducted during June, July and August." | 220マイルを言わない |
| ca18 | OK | T p9802 "an unmanned vehicle which is remotely controlled and towed from a surface ship" | 索と音を消した |
| ca19 | OK | No.710-64 p.2（decisions §4-10）"a 1,200 square yard field of 900 markers" | 広さの数なし・HOIST なし |
| ca22 | OK | T p9802 "TRIESTE II was able to locate on top of a portion of the THRESHER hull" | 「人の乗った」で ca23 のまとめを受ける |
| cb03 | OK | J p.4 "a Submarine Safety Task Group, with 10 separate tasks" | |
| cb04 | OK | J p.93 "will remain in effect until all subsafe measures have been accomplished and certified by the Bureau of Ships in the case of each submarine" | 方針の形。まとめ→cb05「そう。」 |
| cb06 | OK | R08 p.220 勧告20 "events and developments which pertain to submarine safety and the timely dissemination" | 40字 |
| cb07 | ・ | R08 p.202 認定157 "no organization at any level within the Navy" | 語りは良い。画 thr_film593_c は c212・c318・c701 と同じ絵で4回目（c722 と入れ替える案 G4-17 もある）＝⑤bで |
| cb08 | OK | 意見42 "the deficiencies which probably caused THRESHER's loss … could have been reduced" | |
| cb09 | OK | 認定102 "rejection rate of 13.8 per cent"・認定91 "his letter, serial 086 of 16 November 1962" | まとめ→「そう。」 |
| cb10 | OK | J p.95 "The genesis of this effort was not Thresher's loss"・J p.97 "we moved too fast and too far in areas of offensive and defensive capabilities. Submarine safety did not keep pace."・J p.174 "Rear Admiral Curtze, Deputy Chief, Bureau of Ships" | 41字（上限）。「艦船局の長も言ったとおり」は画の欄だけ＝許容 |
| cb11 | OK | J p.94 "could be disabled in water too shallow to collapse the hull and still be beyond our rescue capability" | |
| cb12 | OK | J p.79 "Now I will conclude. I believe the loss of the Thresher should not be viewed solely as the result of failure of a specific braze, weld, system, or component" | 第1版の「結び」も原文どおりだった（外しても誤りではない） |
| cb13 | OK | J p.79 "the philosophy of design, construction, and inspection, that has been permitted in our naval shipbuilding programs" | 限定を戻した。「考え方を挙げ」は言い回しだけ |
| cb14 | OK | J p.127 "a warning made at great sacrifice of life" | 改行だけ |
| cb15 | OK | R08 p.216 意見55 "numerous practices, conditions and standards which were short of those required" | |
| cb17 | OK | R08 p.216 "cannot be charged to neglect or dereliction on the part of any individual or group of individuals." | 意見55 の最後の文＝「結ぶ」で合う |
| cb18 | OK | IR18 p.6 | 追悼の絵に「良い面」を重ねない入れ替え |
| cb19 | OK | IR18 p.6 "Not knowing the exact cause, we have carefully examined all phases of submarine safety -- design, material and operational." | まとめ→cb20「そう。」 |
| cb20 | OK | NAVSEA "from the onset of World War I to 1963 … 16 submarines in non-combat related incidents … Scorpion was not SUBSAFE-certified" | 画の欄の範囲 |
| cb21 | OK | R08 p.220 勧告20 | 背骨を勧告20 に帰属。「それを」は勧告の対象（安全にかかわる出来事）より狭い物を指すが、言い回しの範囲 |
| cb22 | OK | R08 p.181〜184 | 改行だけ・読み上げない |
| cb23 | OK | decisions §2 の例どおり | §B3-7 の型 |

## 節の差し替え（v2_sect_Z.txt・59件）

| 節 | 判定 | 原文の頁と短い引用 | メモ |
|---|---|---|---|
| §1-1 見出し・A2 の行・理由の注 | OK | R08 p.195 認定91c "at or near test depth"・"16 November 1962" | `titles18.py` exit 0＝A2 96字・文2（36／59）・事故名と人数・使わない語なし・公開ずみとの8字以上の共通は「、スレッシャー号」だけ。titles18.json の A2 と1字違わず同じ |
| §1-3 ブルース・ルール氏の行 | OK | 書簡 "By Bruce Rule" | c817〜c820・c918 どれも帰属つき |
| §1-3 役で呼ぶ人の行・分析家の行 | OK | J p.174（副長）・J p.124（Wilkinson） | 語りに役の名は0件（c701〜cb23 を機械で当てた）。c918 を直すなら分析家の行の引用も合わせる（issues の c918） |
| §1-4 見出し・注 | OK | — | c523・cb07・cb18↔cb19＝63→64 |
| §1-5 数字の割れ（表の全行） | OK | J p.93・124／書簡／AP | 6-3・6-4・捜索の海域・マイル（7mi＝11.3〜13.0km・1.5mi＝2.41〜2.78km）・約240か所・3つの見方・公開の年と回数＝本文と合う（6-7 の c419 は R1 の範囲） |
| §1-5 単位の注 | OK | — | |
| §1-6 用語 | OK | — | 意見書（c812）・塗りの札（c908）・潜水艇（ca08）・扉（ca10）・艦の本体（ca13）・潜水艦バーベル（cb08）＝本文どおり |
| §1-8 見出し | OK | — | |
| §1-8 IR18 p.122 | OK | "operating ships" | |
| §1-8 R08 p.26・p.33 | OK | "until about 2:00"・"it was decided that this would not be prudent" | |
| §1-8 R08 p.77 | ・ | — | c219＝R1 の範囲（形だけ見た） |
| §1-8 認定の追記 | OK | 157・47・49〜51 を引いた | ほかは R1 の範囲 |
| §1-8 意見の追記 | ・ | R08 p.212 "If the main coolant pumps stopped … the 7.1 minutes between 0911R and time of collapse depth … about 5 knots" | 「Case III の約750フィート・7.1分・約5ノット」は、7.1分と5ノットが Case III の数に読める（ポンプが止まった場合の数）。⑤bの引き手が取り違えないよう節の文だけ直す |
| §1-8 勧告20 | OK | "the analysis of events and developments which pertain to submarine safety" | cb21 の帰属も |
| §1-8 V1 p.118・X p.1119 | ・ | — | R1 の範囲（形だけ） |
| §1-8 J | OK | p.30・32・35・37・79・83・93・95・97・122・124・160・163・164・174 を引いた | p.163 "perhaps 1,000 feet"＝新聞の推測 |
| §1-8 AP・A-R・No.710-64・T p9802・R08 p.65〜66・171・台帳 | OK | 書簡 "no flooding prior to collapse"・"1300-foot test-depth"／AP の Friedman の文 | IR18 p.67 は R1 の範囲 |
| §1-9 通説 | OK | — | c820 の行・c901・c808・c919 が本文と合う |
| §2 #10 と注（c715） | OK | "blocked and ruptured" | blocked を c716 が受けると注に書いてある |
| §2 ca16・ca23 の字数 | OK | — | 19字・16字（数え直した値で合う） |
| §2 c521・c618・c626 の注 | ・ | — | R1 の範囲（形だけ） |
| §2 c809・cb13・cb17 の注 | OK | — | 本文と合う |
| §0-2 聞き役の注 | OK | — | c7〜cb の聞き役＝6・6・7・5・5（役割表 G4〜G6 と一致） |
| §4 章の表・c7・c8・cb の頭 | OK | — | 表の数は mech18 の出力（数え直していない） |
| §5 外したもの | OK | — | 本文で消えたものと一致 |
| §6 読み | OK | — | 900個・磁力計・曳いた・綱・現役・賢明・私生活・ブルース・十数キロ・2キロ半＝本文の語 |
| §7 素材 | OK | — | thr_film593_c＝4回（cb07 の ・） |
| §9 換算 | OK | — | 3,400yd＝3.11km・400yd＝366m・30ft＝9.1m・600ft＝183m・570ft＝174m・マイルは幅 |
| §9-2 | OK | — | `check_facts.py`＝2013・2020 の2件で申告と一致 |
| 出典の一覧・次 | OK | — | |
