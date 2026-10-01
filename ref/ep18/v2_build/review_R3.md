# 18本目④' 当て直し3（R3・ルール 4'-18）— 今日（10-01）変えた23カット

- 台本＝`ref/ep18/daihon_v2.md`（17:02 版＝diff_today.md の「今」と同じ）。原文は `ref/ep18/v2_build/kwic.py` で引いた。画像は開いていない。
- 判定：OK 16／直す案あり 7（⚠️1・・6）。🔴 0。
- 冒頭（c101〜c105）のつかみの順（日時と場所 → 海の中からの声 → 声の主 → 129人全員・約2,600メートル → 査問会の「おそらく」と海軍長官の「決まっていない」→ 前の艦長の評価書）は、事実の順と強さを保っている。c105 の終わりは 44.9秒（46秒より前）。

## カットごとの判定

### c101 — OK
- kwic `FOR "minor difficult"`・`FOR "16\. "`＝認定16（V1 p.38／R08 p.185）「at about 0913R, THRESHER reported to SKYLARK」。`7909 "200 miles"`＝J 前付 p.9「approximately 200 miles off the northeastern coast」。
- 「潜水艦の」を外した（−3字）。声の主はすぐ次の c102 で言う＝落ちた主語は1カットで戻る。「海の中から、声が届いた」は水中電話の交信で事実どおり。日時と場所 → 声、の順は保たれている。

### c102 — OK
- 認定16「"Experiencing minor difficulties. Have positive up angle. Am attempting to blow."」＝「軽い問題が起き、浮き上がろうとしている」。
- 「という声。」→「と。」（−3字）。引用を受ける「と。」で文として通る（言った主語は1行目の「声の主は…スレッシャー」）。条件や限定の落ちは無い。

### c105 — OK
- `FOR "91\. "`＝認定91c（R08 p.195＝V1 p.48）「the most dangerous condition … is the danger of salt water flooding while at or near test depth」・serial 086 of 16 November 1962（事故の145日前＝約5か月前）。`8020 "most dangerous"`＝J p.20 にも同じ文（「he gave this report as he was leaving」＝前の艦長）。
- 聞き役「じゃあ、」を外した（−3字）。c104 の★「原因は決まっていない」を受ける質問として通る。roles.tsv（c105 質問「何も分からないの？」）と一致・数字なし。

### c116 — 直す案（・）：外した理由の記録が誤り
- kwic `4181 "first of a new class"`＝認定1（R08 p.181＝見える再録の頁）「the first of a new class of nuclear powered attack submarines, capable of diving to a depth [塗り] and with significant advances in sonar equipment, ability to resist shock, and **to operate with reduced noise radiation**」。
- R1 は「quiet が0件」で「音も静かに」の出典が無いとし、G0 は「quiet を支える見える一次の頁が無い」として語りから外した。**原文は quiet でなく noise radiation と書いている**＝出典欄にすでにある認定1 が支える（「0件は無いの証明ではない」の型）。
- 今の語り「それまでの艦より、深く潜れるように作られていた」は誤りではない（V1 p.92「the first of a deeper diving class」・AP「dive deeper than any previous sub」）。直すのは記録（台帳の扱いの文＝review_not.json の c116 の理由）。語りを戻すなら −1字の案を patches に書いた（任意）。

### c212 — OK
- `4208 "23\. "`＝意見23a「it appears … have not insured that all damage is found in the early intensive investigations」。`4217-4219 "shock test"`＝勧告8「shock tests of nuclear submarines be deferred until … the Bureau of Ships has reassessed: a. The adequacy of instrumentation coverage and capability to insure that all damage is found … b. The shock resistance and mass interaction of system components …」。
- 「計器の備えや機器の強さ」＝8a・8b に合う。「延期を勧めた」＝be deferred。1行41字（上限ちょうど）。聞き役はまとめ（roles 一致・数字なし）、次が「そう。」で受ける。

### c219 — 直す案（・）：「言い合い」が誰と誰か耳で分からない
- kwic `R08 "cite instances"`＝R08 p.77「I can't honestly cite instances. I can make one statement concerning one incident that occurred during the beginning of the fast cruise. … hot words exchanged between the boat officer and the Ship Superintendent. … That was the only incident I know of.」
- 新しい3行目「実際の例として挙げたのは、言い合いの1件だけだった」は原文の範囲に合う（例外を落としていない）。ただ「言い合い」の当事者が語りに無く、はじめて聞く人には何の言い合いか分からない。出港を急がせる圧力（造船所の側）の例であることが「艦と造船所」で耳に届く。画の欄はすでに「艦の士官と造船所の監督」。−2字の案。

### c412 — OK
- 認定17（R08 p.185）は意味を書いていない（`FOR "16\. "` の続き）。後半 c919 で見せる読み方は「試験深度より約270メートル（900フィート）深い」の1つ（`AP "900"`＝「suggesting the sub was 900 feet beyond its test depth」）。「ある読み方」で範囲が合う。roles 一致（質問・数字なし）。

### c521 — OK
- `4187 "for the first time"`＝認定28b「became knowledgeable for the first time of the last communications … This information had not previously been communicated to him or to anyone outside SKYLARK.」・28c「the substance of the last UQC transmissions」。
- 「少将が知るまでのことを」で previously の区切りが言い切れた（★が「ずっと外へ出なかった」に読めない）。c509 の電文（最後の声は崩れていた）とも「中身」で食い違わない。★20字。

### c522 — OK（言い回しのメモだけ）
- `4214 "48\. "`＝意見48「failed fully to inform higher authority of all the information … for an unreasonable length of time; but that this could not conceivably have contributed in any way to the loss」。
- 「それが」を外したので3行目の主語は語の上では無いが、前の文の「救難艦の艦長が…伝えなかった」から続けて聞こえ、意味は原文（その不足は喪失に関わりようがない）と変わらない。次の c523 の聞き役「遅れたけど、それが原因ではないんだね」が受け直す。直さない。

### c617 — OK
- `4197`＝認定107「no further ultrasonic testing of old sil-braze joints was conducted pursuant to this program after 29 November 1962」。11月29日 → 4月9日の出港＝4か月と11日＝「4か月以上前」。「出港の」でも起点と終点は同じ。

### c618 — OK
- 認定105・106・108（R08 p.197）。画の欄の「写し」から「だけ」を外したのは認定106（a copy of this decision was furnished）どおり。語りは変わっていない。

### c619 — OK
- 認定108「… or to anyone in the operational command line higher than the Commanding Officer of THRESHER」。「艦に命令を出す側については」で★の「艦長より上」が命令の系統の話だと分かる。★20字。

### c620 — 直す案（・）：質問が「届いた」を前提にして、直前の「上がっていない」とぶつかって聞こえる
- `8017-8019 "11th"`＝J p.18 ブロケット少将「it was received after the 11th of April」・`J "Chief of the Bureau of Ships"`（J p.2・3・8）＝艦船局の長。語りは原文どおり。roles_G3 に c620 質問が入っている（数字なし）。
- c618「造船所から艦船局へは、上がっていない」・c619★の直後に「艦船局には、いつ届いたの？」が来ると、一瞬「届いていないのでは？」と引っかかる。「結局」を足すと「事故の前には上がらなかったが、いつかは届いた」の前提が耳で分かる。答えの「艦船局に」は質問と重なるので外す（+2 −4＝−2字）。

### c621 — 直す案（・）：出典欄の頁
- `4197 "109\."`・`4198 "109\."`（0件）・`4198 "^"`（頁の頭は認定110）・`50-51 "confidence"`＝**認定109 は R08 p.197（＝V1 p.50）の終わり**で、p.198 には無い。出典欄「認定109・意見18（R08 p.198・206）」の 198 は 197。
- 語り：認定109「management and workers exhibited a high degree of confidence in sil-braze joints」・意見18（R08 p.206）「did not aggressively pursue … nor did the Commanding Officer」＝「とみた」で意見の言い方に合う。41字。

### c624 — OK
- `8067-8068`＝J p.68「about 5 percent of her silver-brazed joints were ultrasonically inspected. These joints were in critical piping systems, 2-inch diameter or larger. … about 10 percent of those checked required repair or replacement.」・J p.59＝TUESDAY, JULY 23, 1963。分母に「銀ろう付けの」が戻り、c625 の★の前提（all the Thresher's silver-brazed joints）とそろった。

### c625 — 語りは OK／直す案（・）：節の注が古いまま
- J p.68「If the quality of the joints so inspected was representative of all the Thresher's silver-brazed joints this means that the ship had several hundred substandard joints」＝★は条件を保つ。「そして」を外しても主語（中将）は c624 から続く。
- ただ `v2_sect_Z.txt`（決め所 #9 の注）に「★の前の行は「そして、調べた分を見本として、条件をつけて、こう続けた。」（G7-63）」が残り、今の語りと食い違う＝注を今の文に合わせる。

### c720 — OK
- `4212-4213`＝意見45「If the main coolant pumps stopped, there would have been an automatic reactor shutdown … no normal main propulsion power available until after the 7.1 minutes between 0911R and time of collapse depth … only sufficient for about 5 knots」・Case I「Power lost at 0911R when pumps stop … not highly probable」。
- 「9時11分に止まった場合」で Case I の前提に限られた。「止まった」の主語は語の上では無いが、c719 の「ポンプが止まっていたなら → 原子炉は自動で止まる」とどれを補っても Case I（power lost when pumps stop）と同じ。1行目41字。

### c820 — OK
- `4204 "in all probability"`＝意見1d「A deficient air system, susceptible to freeze-up, with low capacity and low blow rate」。`2122 "freeze"`＝IR18 p.122「inadequate capacity, susceptible to freeze-up … grossly unsatisfactory」。今日の変更は画の欄の並びだけ（語りの順＝査問会 → ルール氏 → c821 の司令官）＝声と画がそろった。

### c904 — 聞き役は OK／直す案（⚠️）：語りの「事実を」が原文の範囲より狭い
- `8164`＝J p.164（1963-08-29）「it would be a poor time indeed to release piecemeal **the facts and assumptions** documented by your hearings. Such action could materially downgrade … both in the public mind and the minds of our officers and men」。
- 新しい聞き役「公聴会の記録は、出たの？」は c903 の「議会の公聴会の記録も、機密のままにした」を指し、c905 の答えと合う（roles 一致・数字なし）。
- ただ語り1行目「今、事実を小出しにすれば」は assumptions（推測）を落としている（型③＝範囲を狭める）。噂の章（「海軍は何かを隠している」）で「事実を出すと評判が下がる」と聞こえ、長官の理由が「事実を隠す」寄りになる。G5-02 は字数のため「事実や推測」を画の欄だけに置いたが、2行目の「の中」2つを外せば語りに入れても −1字で収まる。

### c905 — OK
- 機械で数え直した：J の「classified matter deleted」231・「material」7・「matted」1（J p.36）＝239。もう1つ当たる「classified information deleted」は前付 p.11 の地の文（印ではない）＝数に入れないのが正しい。「の印が」で意味は変わらない。

### c916 — 語りは OK／直す案（・）：画の欄に語りの芯が無い
- `8122`＝J p.122「It was originally just on the basis of cost.」＝語り「元は、費用だけが根拠だった」は原文どおり（R2 の指摘どおり第1版に戻った）。聞き役「元は、お金の計算だったんだ。」（反応）も受ける文が戻った。
- ただ画の欄は「本当の評価はまだ無い」（語りでは言わない）を出し、語りの「元は費用だけが根拠」を出していない＝声と画がずれる（c820 と同じ型）。画の欄に足す。

### c917 — OK
- `8124 "tactical"`＝J p.124 Wilkinson「The general conclusion there is that … in general, the depth to which we would go is what the state of the art will allow us. Therefore, there is not a tactical justification for [classified] feet or any other depth.」＝「どの深さにも」で範囲が合う。「海軍の中の検討」＝Office of Chief of Naval Operations の検討（ほかの2つの外部の検討は「戦術上の価値があるかもしれない」で別）＝帰属は正しい。聞き役 roles 一致・数字なし。

### c918 — OK
- `AP "900|1,300|Friedman"`＝「The test depth was redacted but previously declassified documents indicated it was 1,300 feet, said Norman Friedman, a naval analyst」。「AP通信の記事で、分析家が」で記事の中の話者と分かる。「文書では同じ数」＝documents indicated。

## 直す案の一覧（StructuredOutput の issues と同じ）
| カット | 深刻さ | ファイル | 字数 |
|---|---|---|---|
| c904 | ⚠️ | v2_cuts_G5.txt | −1（第9章） |
| c620 | ・ | v2_cuts_G0.txt・roles_G3.tsv | −2（第6章） |
| c219 | ・ | v2_cuts_G1.txt | −2（第2章） |
| c116 | ・ | v2_cuts_G1.txt（任意）＋ review_not.json の理由の文 | −1（第1章・冒頭の外） |
| c621 | ・ | v2_cuts_G3.txt（出典欄） | ±0 |
| c916 | ・ | v2_cuts_G5.txt（画の欄） | ±0 |
| c625 | ・ | v2_sect_Z.txt（節の注） | ±0 |
