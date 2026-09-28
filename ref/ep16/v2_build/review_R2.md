# 16本目 ④' 照合し直し R2（第7〜11章 c701〜cb20 の変わったカット＋節 §1-1・§1-5・§2・§3・§9）

- 見た人：R2（直した係とは別の目）。ファイルは1つも直していない（案は `review_R2.json` の patch だけ）
- 読んだもの：`decisions.md`・`diff_v1_v2.md` L1326〜L2614 と節の差し替え・`changes_G4〜G6.md`・`daihon_v2.md`（第7〜11章の全文・§1-1・§1-5・§2・§3・§9）・`roles_G4〜G6.tsv`
- 原文：`kwic.py -f q_R2.txt` を4回（計65件）＋PDF146・PDF148 は頁をまるごと出して読んだ（PDF146＝印刷147 の途中から ENEL の委員会の専門家の引用が始まり、PDF148 の頭まで続くのを確かめた）
- 機械で：第7〜11章の全行＝1行40字超 0／文（句読点なし）38字超 0／聞き役20字超は c708 の1件だけ（第1版のまま・句読点を入れて21字）／聞き役の数字 0／★の文は第1版と全部同じ／「ヴァイオント」0（語りと画の欄）
- 判定の印：OK＝直しで誤りが入っていない／⚠️・・＝`review_R2.json` の issue

## 第7章

| カット | 見たこと | 判定 |
|---|---|---|
| c701 | 問い「朝から何が起きたの？」に次の行「朝から夜まで、山の動きは、目に見えて大きくなっていった」がそのまま答える（S9 PDF16〜17 の12時・13時・15〜16時・22時 cedere visibilmente）。3行目で財団の年表を説明するが、第2版は c509（G3 が足した）で先に「財団の年表によれば」を使う | OK（初出の一言の位置は ・ c509） |
| c702 | S9 PDF15「zona boscosa…due fessure larghe un metro e lunghe circa dieci」＝「林で、幅1メートルの割れ目が2本」。憲兵隊の一言を初出へ | OK |
| c703 | 3行目を削っただけ | OK |
| c704 | PDF95「Pancini direttore dei lavori…ferie (dal 1° ottobre)」・「Il richiamo dell'ingegner Pancini venne disposto con la seguente lettera dell'ingegner Biadene」・PDF96「doverla far rientrare anzitempo」「La lettera figurava datata soltanto il giorno 9」・S9 PDF16「9 ottobre, mattina…Biadene scrive a Pancini」＝「同じ朝…手紙を書いた」と合う | OK |
| c705 | PDF96「l'aprirsi della grande fessura che delimita la zona franosa, il muoversi dei punti…che finora erano rimasti fermi, fanno pensare al peggio」＝「崩れる区域を区切る大きな亀裂」「止まっていた目印まで動き出した」。5つを並べた原文を「3つ。／2つを1文」に割ったが、c706 の「そして、こう続ける」で手紙の文だと分かる | OK |
| c708 | 画の欄に【横から】だけ | OK（章の最初の札） |
| c709 | 写真 #078 に替え、左上に時刻の札 12:00。#078 は Commons の日付「before 1963」・場面「完成間近のダムの天端と操作室」＝この日の写真ではない。副題「事故の前」は10月9日の昼も含むので、札と並ぶとこの日の12時の写真に見える | ⚠️ |
| c710 | S9 PDF16「Consegnato…la mattina del 9, il rapporto viene spedito a Roma nel pomeriggio per posta ordinaria」 | OK |
| c712 | PDF228「Alle ore 17 l'ingegner Caruso fa sapere di aver ricevuto da Venezia le direttive di avvertire il Comando dei carabinieri, per disporre il blocco del traffico stradale nella zona di pericolo (ma non per fare sgomberare la popolazione)」＝17時の指示そのものについての少数派の文。帰属も「少数派の報告によれば」で合う | OK |
| c713 | S9 PDF16「per la prima volta, informa Penta degli esperimenti su modello del CIM e sulla presunta quota 700 come quota di sicurezza」＝「安全とされた」で presunta を残す。PDF175「geologo professor Penta, membro della Commissione di collaudo」 | OK |
| c715・c716 | 【上から】＋合図（前の札は c708【横から】） | OK |
| c717 | 問い「下流の町には、備えがあったの？」→「少数派の報告では、無かった。」＝そのまま答える | OK |
| c718 | PDF228「né l'ENEL-SADE, né le Autorità di Governo (Prefetti) si erano preoccupati di disporre un sistema di allarme e un piano di sgombero sia delle popolazioni a valle della diga del Vajont, sia dei cittadini del comune di Erto abitanti le case poste sotto il livello della strada cireumlacuale」＝語気・誰の備え・湖をめぐる道より下とも合う。★は第1版のまま | OK |
| c719 | S9 PDF18「colpevoli di non aver avvertito e di non avere messo in moto lo sgombero」＝「危険を知らせず、避難を始めなかった」。「最初の裁判、一審」の一言 | OK |
| c720 | S9 PDF15「geometra Rittmeyer, dipendente SADE presso la diga」・S9 PDF17「Ore 22. Rittmeyer telefona a Biadene, a Venezia」・PDF228「Alle 22,15…il geometra Ritmayer」 | OK |
| c721 | 語り→まとめ「つまり、模型が安全とした高さ？」→「そう。」。700が模型の安全の高さなのは c109・c511・c713 で言いずみ（先回りでない）。【横から】＋合図（前の札 c716【上から】） | OK |

## 第8章（見る向きの並び：c802【上】→c805【横】合図→c806・c807・c809・c810・c811【横】→c812【上】合図→c814・c815【上】→c816【横】合図〈ダムを東西に切る＝c810 の南北と90度〉→c817【横】→写真5枚→c823【上】合図。合図の抜けは無い）

| カット | 見たこと | 判定 |
|---|---|---|
| c801 | PDF98 の段の頭は「La notte fra il 9 ed il 10…」＝「こう書く」 | OK |
| c802 | PDF144「franò una superficie di circa 1,9 kmq, su un fronte di circa 1,7 km」＝国の調査委員会の専門家。【上から】で範囲だけ | OK |
| c805 | 【横から】＋合図（c802 の図に南北の切り口の線）。倍率「500万倍から600万倍」は原文 PDF146 頭「5 o 6 milioni di volte」（国の専門家の段）と PDF98 の数のまま（計算ではない） | OK |
| c806 | S8 p.41「in less than 45 s」・p.46「some 300 to 400 m horizontally」 | OK |
| c807・c809 | 場面3【横から】・3行目を削っただけ／S9 PDF17「Non in due tempi, bensì come corpo unico, compatto」 | OK |
| c810 | PDF146 の「Gli esperti tecnico-scientifici della Commissione istituita dall'ENEL…con le seguenti constatazioni」に続く引用の中に「la quota 866」「165 metri superiore al livello dell'acqua」＝電力公社の調査委員会の専門家で合う | OK |
| c811 | 【横から】（c810 と同じ南北の断面）・問いに次の行が答える | OK |
| c812 | 帰属「同じ専門家の調べでは」＝PDF146「Secondo gli accertamenti degli esperti…ENEL…930…di ben 200…in due punti…traverso della diga e a circa 1.100 metri a monte」で合う。ただ画は【上から】に替わるのに、1〜2行目は高さ（標高930・水面より200）＝decisions §4 の「駆け上がる高さは横から」。口の合図「上から見ると」は3行目で遅れる | ⚠️ |
| c813 | PDF97 の条件「con il massimo invaso e con il crollo istantaneo」を戻した・「di ben 200」＝「200メートル以上も」・「測り方は同じではない」を保つ（比べの向きの逆は無い） | OK |
| c814 | 「2つに」。PDF207「l'ondata investiva Pineda, si rifletteva a colpire San Martino」は出典欄だけ＝語りに「はね返った」は無いので少数派の帰属は要らない。失われた＝PDF98・S9 PDF17 | OK |
| c815 | PDF146「si sia riversata verso ovest, tracimando la diga」（ENEL の引用の中） | OK |
| c816 | PDF148 頭「Se ne conclude che il volume d'acqua espulso a valle…dovrebbe aggirarsi intorno a 30 milioni」＝PDF146 から続く ENEL の引用。「同じ専門家の見積もり」「およそ」で帰属と留保が合う。【横から】＋合図（ダムを横から見ると・90度ちがう） | OK |
| c817 | S8 p.47「overtopped the dam more than 100 m above the crest」。「2通り」を言わない・140 を言わない | OK |
| c818・c820 | S8 p.42「resisted…suffered only minor damages」・S9 PDF17「In tutta la zona l'unica opera umana che resiste, senza danni」＝「一帯で」 | OK |
| c821 | PDF147「riempire il fondo valle del Vajont」・PDF146「il bacino rimasto isolato ad est [della frana]」。ただ「その奥に」は、写真 #021（崩れた土砂の上からダムを見る・残った池が写る）と並ぶとダム側の池を指して聞こえる＝原文は崩れた山の東（上流） | ・ |
| c822 | 帰属＝PDF148「volume d'acqua espulso a valle e che provocò la funesta onda nella valle del Piave」で合う。写真 #031（photos_commons：1963・Ispettorato VVF・峡谷の出口と水たまり）は語り「峡谷を下流へ・ピアーヴェ川の谷へ出た」と合う。「事故のあと」は日付が「1963」だけ＝⑤b で原寸（G4・§1-4 に記載ずみ） | OK |
| c823 | 【上から】＋合図・「上から見ると、」 | OK |

## 第9章

| カット | 見たこと | 判定 |
|---|---|---|
| c902 | PDF98「all'alba del 10 ottobre i paesi di Longarone, di Pirago, di Fornace, di Faè e parte di Castellavazzo…di Pineda e San Martino ai bordi del lago, non esistevano più」 | OK |
| c903 | S9 PDF17 は集落の名を多く挙げる | OK |
| c904 | S8 p.41「still had a height of about 70 m downstream, at the confluence of the Vaiont with the Piave Valley」＝峡谷の出口。140 は言わない | OK |
| c907・c908 | まとめ→「そう。4人のうち3人」（1,450÷1,917＝75.6%）・「峡谷の出口の先にあった町」は c823 の語り | OK |
| c910 | PDF207「duemila…cinquecento bambini」 | OK |
| c911 | PDF99 は「i soldati di ogni arma e corpo」＝兵士。消防（vigili）と仮の橋（ponte）は PDF99 に0件＝写真の撮影者と #013 の説明から（語りの誤りではない） | OK（出典欄は兵士の分だけ） |
| c912 | PDF99「diedero coraggio agli scampati…soccorsero i feriti, seppellirono i morti, posero mano alle prime misure di ristabilimento delle minime esigenze di vita」 | OK |
| c913 | PDF99「Anche da molti paesi stranieri giunsero innumerevoli espressioni…di solidarietà」 | OK |
| c914 | 質問を外して語りに（犠牲者の章に反応を置かない） | OK |
| c915 | PDF99「come pure agli emigrati, accorsi nella vana speranza di ritrovare i loro cari」＝「遠くへ働きに出ていた人たちも、家族を捜しに戻ってきた」（vana は落としたが事実は合う・並べただけで因果にしていない） | OK |
| c916・c917 | PDF98〜99「numerosi lavoratori addetti alla diga e tecnici addetti ai controlli con le loro famiglie」 | OK |
| c920 | 問い→「裁判所と、政府と、議会だ」＝PDF99「L'Autorità giudiziaria, il Governo ed il Parlamento…ricercare…la verità」でそのまま答える。ただ問いの列は PDF99 では「subito seguirono dubbi angosciosi e conturbanti. Era prevedibile tanta catastrofe?…」＝人々に起きた疑いとして並ぶ。「議会の報告書は問う」は主語が少しずれる | ・ |

## 第10章（予見の言い方と11人の数え方）

| カット | 見たこと | 判定 |
|---|---|---|
| ca01 | 2行目を削っただけ | OK |
| ca03 | PDF26「respinto — con 7 voti favorevoli, 19 contrari」「con 1 voto favorevole, 17 contrari」「siano allegate le due relazioni di minoranza…in un unico fascicolo」 | OK |
| ca04 | PDF178「Non rientra nei compiti della Commissione parlamentare valutare se…avessero potuto essere previste…di pertinenza dell'Autorità giudiziaria」「confrontando…con tutte le ipotesi formulate」。問いに次の行がそのまま答える | OK |
| ca06 | 「当時の予測」＝le previsioni formulate | OK |
| ca07 | PDF166「Resta, peraltro, un motivo di perplessità sul fatto che le prove su modello avevano indicato nella quota 700 il limite ritenuto di sicurezza」＝許可の段の中＝「越える許可が出たこと」。PDF179「benché non consti che…ufficialmente trasmesse」＝「確かめられない」（c417★と字を変えただけ） | OK |
| ca08 | PDF207「prevedibile e probabile, e quindi evitabile」・PDF228 は prevedibilità と probabilità を分ける＝「起こる見込みも高く」で probabile を残す | OK |
| ca09 | PDF241「la tesi, piuttosto affermata che dimostrata…assoluta imprevedibilità」 | OK |
| ca10 | 役割はまとめ（「つまり」なし・見方が割れたことへの受け）＝反応に替えるとまとめ 19→18（30.2%→28.6%）・反応 8→9 | ・（役割の案） |
| ca12・ca14 | S9 PDF17「20 febbraio…deposita la sentenza…contro［11人］…Penta e Greco nel frattempo sono deceduti. 28 novembre. Mario Pancini si toglie la vita. 29 novembre. Inizia…il processo di primo grado」・S10 PDF20「due imputati su 11 che erano stati inizialmente rinviati a giudizio」＝11人・予審のあいだに2人・前の日に1人で食い違わない | OK |
| ca13 | S10 PDF19「su ordinanza della Cassazione adducendo il motivo di «legittima suspicione»…esacerbazione degli stati d'animo…mancata serenità dei giudici」。【上から】は章で1つだけ | OK |
| ca15 | S9 PDF18「Non viene riconosciuta la prevedibilità della frana」＝「予見できたとは、認められなかった」（decisions §3 どおり）・3人＝Biadene・Batini・Violin | OK |
| ca16・ca17 | S9 PDF18「riconosce la totale colpevolezza di Biadene e Sensidoni: riconosciuti colpevoli di frana, inondazione e degli omicidi」・無罪5（Frosini・Violin・Marin・Tonini・Ghetti）・Batini の stralcio。聞き役に漢数字なし | OK |
| ca18・ca19 | S9 PDF18「colpevoli di un unico disastro: inondazione aggravata dalla previsione dell'evento compresa la frana e gli omicidi」＝「予見していながらの、重い過失」（decisions §3）。ca19 のまとめは ca18 の言い直しで先回りでない。「最初の判決から…大きく変わった」＝c111 と同じ | OK |
| ca20・ca21 | S10 PDF20「a soli 15 giorni」・S9 PDF18「Dopo quindici giorni sarebbero scaduti i 7 anni e mezzo」 | OK |
| ca25 | S9 PDF18「rigetta la richiesta del comune di Longarone di rivalersi in solido contro la Montedison, società in cui è confluita la SADE, condannando viceversa l'ENEL al risarcimento dei danni subiti dalle pubbliche amministrazioni」 | OK |
| ca27 | 問いに「誰と誰を、一緒に罰したか、だ」で答える（S10 PDF20「colpiva insieme」）・cb01★を先回りしない | OK |

## 第11章

| カット | 見たこと | 判定 |
|---|---|---|
| cb02 | S10 PDF20「l'esponente di una società industriale e finanziaria privata e un uomo appartenente all'istituzione pubblica dello Stato」 | OK |
| cb03 | PDF213（少数派1）「l'ultima relazione della Commissione in data 7 novembre 1963 che dichiara concluso il suo mandato e impossibile « la prosecuzione delle operazioni di collaudo »」・S9 PDF17 も同じ＝委員会の報告の言葉なので少数派の帰属は要らない | OK（変更なし） |
| cb04 | S9 PDF17「dichiara concluso il suo mandato」・PDF41「nota dell'ENEL, del 28 maggio 1965…galleria di scarico a quota 640 m., per lo svuotamento del lago residuo」＝並べただけ（因果にしていない） | OK |
| cb06 | 帰属（国の調査委員会の専門家＝PDF147）・S8 p.41「generally agreed…bands of clay」 | OK |
| cb07 | 問い「湖は、いまは？」に次の行が答える。PDF146・PDF41 は1963〜65年の「残った湖」で、「いま」は写真 #122 | OK |
| cb08 | PDF171「L'abitato di Erto si salvò in parte notevole」＝「かなりの部分」。ただ §2 #1 の訳はまだ「大部分が助かり」 | OK（§2 #1 は ・） |
| cb11 | S10 PDF11「organizzare…la mole di documenti sequestrati」・PDF24「l'Archivio del processo penale del disastro del Vajont」 | OK |
| cb12 | 多数派＝decisions §3 どおり（ca04 とそろう）。画の欄の破毀院の札は cb13 と同じく主語が抜ける | ・ |
| cb13 | 「破毀院は、崩落も含めた災害を予見していた、として」＝耳では破毀院が予見していたと聞こえる（予見したのは2人）。ca18・ca19 の「予見していながらの重い過失」ともそろっていない（G6 の「気づき」が求めたそろえ）。「過失」を避けた理由（本文に出ない語）は ca18 で「重い過失」が入ったので無くなった | ⚠️ |
| cb14 | S8 p.43「the knowledge and the technologies available at that time…have to be taken into account」。画の欄の年表「1962-04 下流の研究を見送る」は §1-5 の決め（1962年の春＝PDF225 4月30日と S9 PDF12 3月30日で割れる）と食い違う | ⚠️ |
| cb15 | 語り「1962年4月、下流の波の研究を、見送ったとき」＝少数派 PDF225 の月をそのまま言う。c517・c518 は「1962年の春」＝同じ出来事を章で違う言い方 | ⚠️ |
| cb17 | まとめ「つまり、決める場面は、何度もあった？」は cb14 で言いずみ→「そう。」 | OK |
| cb18・cb19 | 出典欄を足しただけ・「いま並べれば、誰にでも見える」（後知恵）を消した | OK |
| cb20 | です・ます・3行・責める相手なし・2行目36字 | OK |

## 節

| 節 | 見たこと | 判定 |
|---|---|---|
| §1-1 | 字数＝推奨A 78・控えB 68・控えC 77（数え直して一致）。推奨A「絶対に安全」＝PDF89 assoluta sicurezza・「その夜の水位は約700メートル」＝PDF96（今朝700のはず）・S9 PDF17（700,42）で合う・因果は言っていない | OK |
| §1-5 | 波・越えた水・速さ・その夜の水位・最後の電話・裁判の人数の行は原文と合う。「模型の研究所の委員会の意見」の行の注は cb14 の画だけを挙げ、cb15 の語り「1962年4月」を拾っていない | ・（cb14・cb15 を直すなら注も） |
| §2 | #11（PDF228 の主語 Prefetti・circumlacuale）・#12・#15（PDF178）・#16（S10 PDF20）を原文で確かめた。#1 は第2版で直していない行で「エルトの集落は大部分が助かり」＝cb08 で直した「かなりの部分」（in parte notevole）と食い違う | ・ |
| §3 | c7〜cb の行・字・写真・文字だけ・決め所・聞き役を台本から数え直して一致（例 c7 58行・c8 53行・c9 写真14） | OK |
| §9 | 24杯（3,000万÷124万＝24.2）・230杯（226〜242）・25メートルあまり（25.5）・4人のうち3人（75.6%）・3年以上前・60年以上・ただ3人／5人・1人・11人のうち3人を確かめた。「500万倍から600万倍」は原文の数（計算の申告は要らない） | OK |

## 数（R2 の issue）
- ⚠️ 5（cb13・cb15・cb14・c812・c709）／・ 7（cb12・§1-5・c821・c920・ca10・c509・§2 #1）／🔴 0
- 案を全部当てたときの字（句読点なし）：c812 +4・cb13 −1・c821 +1・c920 −3・cb15 ±0・c509 +5（第5章＝R1 の範囲。当てるかは G0）＝計 +6
