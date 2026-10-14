# 第1版 → 第2版の対照（22本目 ④'・直したカットだけ）

- 行頭 `-` が第1版、`+` が第2版。`id` は差し替え表 `patches22.json` の番号（所見の id）
- 原文は `python ref/ep22/v2_build/pg22.py page USCG 35` ／ `sec 1.3.2` ／ `find 語` で引ける

## c101
- id `G7-007`：タイタニックを冒頭で1語出す（c106 を受ける）。1行41字に収めるため2行に組み直した（C）
```diff
-> 2023年6月22日。北大西洋の、深さ約3,800メートルの海の底。
-> 無人の探査機のカメラが、潜水艇の尾部をとらえた。
+> 2023年6月22日。北大西洋、タイタニックの眠る深さ約3,800メートル。
+> 海の底で、無人の探査機のカメラが、潜水艇の尾部をとらえた。
```

## c106
- id `G0-015`：聞き役の質問の割合（63%）を下げるため、冒頭の驚きを反応にした（答えの「その夏のうちに3回」はそのまま続く）
- id `G1-020`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c106** ／ 実写 USCG の記者会見 888022（別の区間） ／ NTSB p.36（`The Titan completed three additional dives following dive 80`）
-> Q: 大きな音がしたのに、また潜ったの？
+**c106** ／ 実写 USCG の記者会見 888022（別の区間） ／ NTSB p.36（`The Titan completed three additional dives following dive 80`）・NTSB p.36（`the submersible reached 3,840 meters (12,598 feet) on dives 81 and 82`）
+> Q: 大きな音がしたのに、また潜ったんだ。
```

## c107
- id `G1-001`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> この潜水艇は、海の底で、何が壊れたのか。
-> なぜ、潜り続けたのか。そして、誰が止められたのか。
+> この潜水艇は、深い海の中で、何が壊れたのか。
+> なぜ、潜り続けたのか。そして、誰なら止められたのか。
```

## c109
- id `G7-008`：何をしに潜っていたかを橋で先に言う（係の案）を、冒頭の秒のために1文にした（C）
```diff
-> まずは、この潜水艇が、何をしに潜っていたのかから見ていく。
+> この潜水艇は、客を乗せて、タイタニックを見に行っていた。
```

## c202
- id `G1-026`：係の案どおり（G0 が原文に引き直した）（字数：1回目の試し組みで上限を444字超えた＝足しの言い添えを戻した）（A）
```diff
-> そこでは、海の水の重さが、すさまじい力でのしかかる。
+> そこでは、水の重さがのしかかる。
```

## c205
- id `G1-002`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 母船で運ばれ、海に降ろされてから潜る、小さな潜水艇だ。
+> 母船に運ばれて現場まで行き、そこから潜る、小さな潜水艇だ。
```

## c206
- id `G1-025`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c206** ／ 図 線 同じ線画（人が乗る部分＝筒と両端のドームを明るく・札「炭素繊維の筒」「チタンのドーム」） ／ TSB（`The Titan’s pressure hull consisted of a carbon fibre cylinder that was capped at either end by titanium domes.`）
+**c206** ／ 図 線 同じ線画（人が乗る部分＝筒と両端のドームを明るく・札「炭素繊維の筒」「チタンのドーム」） ／ TSB §1.10.1（`The Titan’s pressure hull consisted of a carbon fibre cylinder that was capped at either end by titanium domes.`）・§1.2.1（`Two hemispherical domes made of titanium were fitted to either end of the cylinder.`）
```

## c207
- id `G1-003`：係の案どおり（G0 が原文に引き直した）（B）
- id `G1-004`：係の案どおり（G0 が原文に引き直した）（D）
- id `G7-078`：CEO の初出に一言（会社のトップ）。G1-003 の行（3行目）とは別の行（A）
- id `R1-010`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-**c207** ／ 図 再現 TSB 表4（2023年の上級の8つの職と、その席が埋まっていたか＝欄は英字のまま・CEO の行を明るく） ／ TSB §1.3（`the Titan’s pilot, who was OceanGate’s chief executive officer (CEO)`）・§1.23.1（`As a small company, OceanGate was led primarily by the CEO.`）
+**c207** ／ 図 再現 TSB 表4（2023年の上級の8つの職と、その席が埋まっていたか＝欄は英字のまま・CEO の行を明るく） ／ TSB §1.3（`the Titan’s pilot, who was OceanGate’s chief executive officer (CEO)`）・§1.9.1（`had piloted it on numerous previous dives, including dives to the Titanic in 2021 and 2022`）・§1.23.1（`As a small company, OceanGate was led primarily by the CEO.`）・§1.23.1（`The CEO was integrated into all aspects of the company, including human resources, finance, operations, and submersible design and construction.`）
-> CEO の〈CEOの名前〉だ。潜水艇の操縦も、自分でしていた。
-> 小さな会社で、人事やお金から潜水艇の設計まで、CEO がほとんどを率いていた。
+> 会社のトップ、CEO の〈CEOの名前〉だ。潜水艇の操縦も、自分でしていた。
+> 小さな会社を、CEO が主に率い、人事やお金から設計まで、すべてに関わった。
```

## c208
- id `G1-005`：係の案どおり（G0 が原文に引き直した）（B）
- id `G1-006`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c208** ／ 図 再現 同じ表4（2023年の初めの社員の数「15」の札を足す） ／ TSB §1.23（`At the beginning of the 2023 operating season, OceanGate had 15 employees`）・§1.23.1（`viewed the design, development, and operation of the Titan as being experimental`）・§1.23.1（`There was no precedent for diving a human-occupied carbon fibre submersible to the deep ocean`）
-> 2023年の初めの社員は15人。
+**c208** ／ 図 再現 同じ表4（2023年の潜航の季節の初めの社員の数「15」の札を足す） ／ TSB §1.23（`At the beginning of the 2023 operating season, OceanGate had 15 employees`）・§1.23.1（`viewed the design, development, and operation of the Titan as being experimental`）・§1.23.1（`There was no precedent for diving a human-occupied carbon fibre submersible to the deep ocean`）
+> 2023年の潜航の季節の初め、社員は15人。
```

## c211
- id `G1-007`：問いを呼び名を聞く形に（係の案）。語の訳「任務の専門家」は外した（字数：1回目の試し組みで上限を444字超えた＝足しの言い添えを戻した）（C）
- id `G1-008`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c211** ／ 図 再現 会社の計画書の一節（NTSB 脚注8 が引く `guests who help fund OceanGate expeditions` の英字＋訳は字幕） ／ NTSB p.15（`OceanGate referred to its clients as “mission specialists.”`）・USCG p.317〈309〉（`to conceal that their mission specialists were actually paying passengers`）
-> Q: ミッション・スペシャリストって、何？
-> 会社が、お金を払う客をそう呼んだ。米沿岸警備隊の委員会は、
+**c211** ／ 図 再現 会社の計画書の一節（NTSB 脚注8 が引く `guests who help fund OceanGate expeditions` の英字＋訳は字幕） ／ NTSB p.15（`OceanGate referred to its clients as “mission specialists.”`）・USCG p.300〈292〉（`reclassifying their passengers as “mission specialists” to conceal their illegal passenger operations`）・USCG p.317〈309〉（`to conceal that their mission specialists were actually paying passengers`）
+> Q: お客さんは、会社から何と呼ばれていたの？
+> ミッション・スペシャリスト。米沿岸警備隊の委員会は、
```

## c213
- id `G1-009`：NTSB p.14＝attempted numerous dives … but only successfully completed 13＝「だけ」を語りに置き、聞き役は数を言わない反応に。c214 の「ただ」は G0-001 で外した（C）
- id `R1-004`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> そのうち、タイタニックの深さまで届いたのは13回だった。
-> Q: けっこう、行けていたんだ。
+> そのうち、タイタニックの深さまで届いたのは、13回だった。
+> Q: 毎回、行けたわけじゃないんだ。
```

## c214
- id `G0-001`：c213 の聞き役を「毎回、行けたわけじゃないんだ」にしたので、c214 の頭の「ただ」は逆接にならない＝外して「不具合も並ぶ」
- id `G1-027`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> ただ、表の備考の欄には、不具合が並ぶ。
-> 1行目は、回収のときに前のドームが外れて落ちた、という記録だ。
+> 表の備考の欄には、不具合も並ぶ。
+> 1行目は、回収のときに前のドームが外れて落ちた記録だ。
```

## c215
- id `G1-010`：電池と荒れた海の2つの理由（NTSB p.36）。「潜水艇を載せる」は字数で外した（台は c304・c305 で説明）（字数：2回目の試し組みでも上限を67字超えた）（B）
```diff
-> 電池が切れて台に戻れず、人を乗せたまま海面で一晩を過ごし、
-> 潜航が27時間に及んだ回もあった。
+> 電池が切れ、海も荒れて台に固定できず、
+> 人を乗せたまま海面で一晩を過ごし、潜航が27時間に及んだ回もあった。
```

## c216
- id `G1-011`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-> 推進器の故障、重りの不具合、通信の不具合。カナダの報告書は、
-> 会社が主に、やってみて直すやり方で運航していた、と書いている。
+> 推進器の故障、重りの不具合、通信の不具合。
+> カナダの報告書は、会社が主に、やってみて直すやり方で運航していた、と書いている。
```

## c217
- id `G1-012`：係の案（報告書は手で持つ無線のとだけ書く・写真の物はゲーム機用）を詰めた（B）
- id `G1-013`：係の案どおり（G0 が原文に引き直した）（D）
- id `R1-011`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-**c217** ／ 実写 MBI 図65 前の艇 Cyclops I の中のコントローラーとキーボード（USCG 報告 p.103・2023年10月に MBI が撮影・A＝副題「前の艇 サイクロプス1 の操縦の道具（2023年10月撮影）」） ／ TSB §1.10.5（`The pilot operated the thrusters using a handheld wireless controller`）・USCG p.103〈95〉（`Photo of the Logitech PlayStation controller inside CYCLOPS I taken by the MBI`）
+**c217** ／ 実写 MBI 図65 前の艇 Cyclops I の中のコントローラーとキーボード（USCG 報告 p.103・2023年10月に MBI が撮影・A＝副題「前の艇 サイクロプス1 の操縦の道具（2023年10月撮影）」） ／ TSB §1.10.5（`The pilot operated the thrusters using a handheld wireless controller`）・NTSB p.11（`a wireless, battery-operated controller that communicated with control software`）・USCG p.103〈95〉（`the CYCLOPS I being operated with a PlayStation® controller`）・USCG p.103〈95〉（`Photo of the Logitech PlayStation controller inside CYCLOPS I taken by the MBI`）
-> 報告書は、手で持つ無線のコントローラーと書き、どれも原因とはしていない。
-> この写真は、会社の前の潜水艇の物だ。
+> 報告書は、手で持つ無線のコントローラーとだけ書き、原因とはしていない。
+> 写真は、会社の前の潜水艇の物で、こちらはゲーム機用だ。
```

## c218
- id `G1-014`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 2021年と2022年の遠征では、別の会社の船を母船にしていた。
+> 2021年と2022年の遠征では、別の船を借りて、母船にしていた。
```

## c219
- id `G1-015`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> ニューファンドランドのセントジョンズから、約685キロ先の現場へ向かった。
+> ニューファンドランドのセントジョンズから、約700〜800キロ先の現場へ向かった。
```

## c301
- id `G1-016`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> カナダの船籍の、全長約67メートルの貨物船だ。
+> カナダの船籍の、全長70メートル近い貨物船だ。
```

## c311
- id `G1-021`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c311** ／ 図 線 タイタンの横の線画（前のドームの縁に、外から留めるボルトの札） ／ TSB §1.2.1（`The forward dome could be bolted and unbolted from outside the submersible to provide access to the cabin; this was the only way that people could enter and exit the submersible.`）
+**c311** ／ 図 線 タイタンの横の線画（前のドームの縁に、外から留めるボルトの札） ／ TSB §1.2.1（`The forward dome could be bolted and unbolted from outside the submersible to provide access to the cabin; this was the only way that people could enter and exit the submersible.`）・TSB §2.5（`could not egress on the surface without the Titan first being reattached to the LARS and the forward dome being unbolted by people outside the submersible`）
```

## c312
- id `G1-022`：係の案どおり（G0 が原文に引き直した）（D）
- id `G7-012`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-**c312** ／ 図 帯 同じ時刻の帯（08:24 に「艇の中の生命維持へ」の札） ／ TSB §1.3.1（`At this point, the Titan crew and passengers were sealed inside the cabin, and the submersible was using its internal life support system.`）
-> この時から5人は艇の中に閉じられ、酸素を足し、
-> 吐いた息の二酸化炭素を取る、艇の中の仕組みで息をすることになった。
+**c312** ／ 図 帯 同じ時刻の帯（08:24 に「艇の中の生命維持へ」の札） ／ TSB §1.3.1（`At this point, the Titan crew and passengers were sealed inside the cabin, and the submersible was using its internal life support system.`）・TSB §1.2.1（`The cabin had an internal life support system that consisted of oxygen tanks`）・§1.2.1（`CO2 scrubbing capability for the same occupancy`）
+> この時から5人は、閉じた潜水艇の中で、酸素を足し、
+> 吐いた息の二酸化炭素を取る、生命維持の仕組みで息をすることになった。
```

## c313
- id `G0-013`：字数：1文に詰めた（「全員」「ここまでの」を外す）
```diff
-> 8時59分、会社の人たちは全員、予定どおり5分だけ作業を止め、
-> ここまでの進み具合と安全を考えた。
+> 8時59分、会社の人たちは予定どおり5分だけ作業を止め、進み具合と安全を考えた。
```

## c314
- id `G1-023`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c314** ／ 図 模式 台が沈む3段（水を入れる→台ごと水面の下→艇を切り離す） ／ TSB §1.3.1（`By 0905, the LARS and the Titan were submerged.`）・§1.3.1（`At 0914, divers detached the Titan from the LARS, and the Titan began its descent.`）
+**c314** ／ 図 模式 台が沈む3段（水を入れる→台ごと水面の下→艇を切り離す） ／ TSB §1.3.1（`At 0904, OceanGate divers began to fill the LARS’s ballast tanks with water to submerge it.`）・§1.3.1（`By 0905, the LARS and the Titan were submerged.`）・§1.3.1（`At 0914, divers detached the Titan from the LARS, and the Titan began its descent.`）
```

## c315
- id `G1-017`：「この年」を1回に（2つ目の文は「これが初めて」で同じ年を受ける）（A）
```diff
-> 10メートルより深く潜るのも、この年はこれが初めてだった。
+> 10メートルより深く潜るのも、これが初めてだった。
```

## c317
- id `G1-024`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c317** ／ 図 再現 付録A の表の最初の4行（09:19:36〜09:20:02・打ち間違いのまま＝`I hsvr trscking`・`descendingb thru 235`・`i have tracking`・`yeah`・訳は字幕） ／ TSB 付録A（`I hsvr trscking`）・付録A（`descendingb thru 235`）・TSB §1.3.2（`The Titan crew then transmitted a message stating that they were descending through 235 m.`）
+**c317** ／ 図 再現 付録A の表の最初の4行（09:19:36〜09:20:02・打ち間違いのまま＝`I hsvr trscking`・`descendingb thru 235`・`i have tracking`・`yeah`・訳は字幕） ／ TSB 付録A（`I hsvr trscking`）・付録A（`descendingb thru 235`）・TSB §1.3.2（`The Titan crew then transmitted a message stating that they were descending through 235 m.`）・TSB §1.3.2（`The surface support team sent a message back stating that they had tracking of the submersible.`）・USCG p.32〈24〉（`the POLAR PRINCE communicated to the TITAN that they have tracking`）
```

## c319
- id `G1-018`：係の案どおり（G0 が原文に引き直した）（B）
- id `G7-014`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-> 9時28分、母船は「画面で、毎分33メートルで降りているのが見える」と送った。
-> Q: ここまでは、順調そうだね。
+> 9時28分、母船は、毎分33メートルで降りているのが画面で見える、と送った。
+> Q: 降りるのは、順調そうだね。
```

## c401
- id `G2-010`：係の案どおり（G0 が原文に引き直した）（D）
- id `G7-015`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-**c401** ／ 図 再現 書類の再現図 TSB 付録A の表（10:11:55〜10:15:39 の4行・欄の値は英字のまま＝`lost system oand chat settings`・`yes`・`all good here`・`ack all good`・訳は字幕だけ） ／ TSB §1.3.2（`indicating that the communication system had temporarily stopped working`）・付録A（`10:14:35.5 T all good here`）
-> Q: そのあとも、やりとりは続いていたの？
-> 続いていた。10時11分、潜水艇は「通信の装置が、しばらく止まっていた」と返し、
+**c401** ／ 図 再現 書類の再現図 TSB 付録A の表（10:11:55〜10:15:39 のうち4行＝10:12 の4行は除く・欄の値は英字のまま＝`lost system oand chat settings`・`yes`・`all good here`・`ack all good`・訳は字幕だけ） ／ TSB §1.3.2（`indicating that the communication system had temporarily stopped working`）・付録A（`10:14:35.5 T all good here`）
+> Q: 返事は、また来たの？
+> 来た。10時11分、潜水艇から、通信の装置がしばらく止まっていた、と知らせがあり、
```

## c402
- id `G0-016`：字数：「タイタニックの眠る」は c101・c201 で言っている
- id `G7-016`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> このとき潜水艇は、深さ2,200メートルあたりを降りていた。
-> タイタニックの眠る海の底までは、あと1,500メートルほどだ。
+> このとき潜水艇は、深さ2,300メートル近くを降りていた。
+> 海の底までは、あと1,500メートルほどだ。
```

## c404
- id `G2-001`：generally considered＝「ふつう十分とされる」と米沿岸警備隊の帰属。1行に詰めた（B）
- id `G2-011`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c404** ／ 図 再現 付録A の表（10:29:12〜10:31:55 の5行） ／ TSB 付録A（`your position jumps significantly each ping`）・USCG p.34〈26〉（`generally considered to be an adequate signal`）
+**c404** ／ 図 再現 付録A の表（10:29:12〜10:31:55 の6行） ／ TSB 付録A（`your position jumps significantly each ping`）・USCG p.34〈26〉（`generally considered to be an adequate signal`）
-> 一方、潜水艇の知らせた信号の強さは、文字を送るには十分だった。
+> 米沿岸警備隊によると、信号の強さは、文字を送るにはふつう十分とされる値だった。
```

## c405
- id `G2-012`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c405** ／ 実写 MBI 図31 船橋の事務室（通信班の持ち場・机と画面・人なし・USCG 報告 p.32・A・全画面には小さい＝寄り弱め＝副題「母船の船橋の事務室（通信班の持ち場）」） ／ TSB 付録A（`remember to write down the location and time of niskin deployment`）・USCG p.34〈26〉（`Niskin bottles are used for collecting water samples at various depths`）
+**c405** ／ 実写 MBI 図31 船橋の事務室（通信班の持ち場・机と画面・人なし・USCG 報告 p.32・A・全画面には小さい＝寄り弱め＝副題「母船の船橋の事務室（通信班の持ち場・事故のあとに委員会が撮影）」） ／ TSB 付録A（`remember to write down the location and time of niskin deployment`）・USCG p.34〈26〉（`Niskin bottles are used for collecting water samples at various depths`）
```

## c410
- id `G2-004`：カナダの調べも目的（速さを緩める）は同じ見方＝係の案を詰めた（B）
- id `G2-005`：係の案どおり（G0 が原文に引き直した）（D）
- id `R1-012`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-**c410** ／ 図 帯 2段の札（上＝米国の2つの調べ「この深さのふつうのやり方」／下＝カナダ「海底まで約500m・いつもより早い・理由は分からない」） ／ NTSB p.17（`which was a standard procedure at this depth to slow its descent`）・TSB §1.3.2（`the submersible was approximately 500 m from the seabed`）・§2.1（`Dropping the 2 weights earlier than normal suggests`…`the reason for this is unknown`）
+**c410** ／ 図 帯 2段の札（上＝米国の2つの調べ「この深さのふつうのやり方」／下＝カナダ「海底まで約500m・いつもより早い・理由は分からない」） ／ NTSB p.17（`which was a standard procedure at this depth to slow its descent`）・USCG p.6〈vi〉（`As the TITAN approached the ocean floor, it followed standard procedure by releasing ballast weights to slow its descent.`）・TSB §1.3.2（`the submersible was approximately 500 m from the seabed`）・§2.1（`Dropping the 2 weights earlier than normal suggests`…`the reason for this is unknown`）
-> カナダの調べは、海の底まではまだ約500メートルあり、いつもより早かったとして、
-> その理由は分からない、と書いている。
+> カナダの調べは、海の底まではまだ約500メートルあり、いつもより早いとする。
+> 速さを緩めようとしたとみられるが、理由は分からない、と書く。
```

## c411
- id `G2-006`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 米沿岸警備隊によると、その7秒後の10時47分9秒ごろ、
+> 米沿岸警備隊によると、文を送った7秒後の10時47分9秒ごろ、
```

## c413
- id `G2-009`：係の案どおり（G0 が原文に引き直した）（D）
- id `G7-018`：係の案どおり（G0 が原文に引き直した）（E）
```diff
-**c413** ／ 図 帯 2段の帯（上＝米沿岸警備隊・下＝カナダ。「画面に出た」と「壊れた」の順が上下で逆） ／ USCG p.6〈vi〉（`which the investigation later correlated to the TITAN’s implosion`）・TSB §1.3.2（`At 1047:26.903, when the submersible was at 3350 m, a message appeared on the surface support team’s computer`）
+**c413** ／ 図 帯 2段の帯（上＝米沿岸警備隊・下＝カナダ。「画面に出た」と「壊れた」の順が上下で逆） ／ TSB §1.3.2（`At 1047:26.903, when the submersible was at 3350 m, a message appeared on the surface support team’s computer`）・§2.1（`The pressure hull’s structural failure happened 5.397 seconds after the text message about dropping the 2 weights appeared`）
-> 文が画面に出たのは10時47分26.9秒。壊れたのは、その5.397秒後だ。
+> 文が画面に出たのは10時47分26.9秒。壊れたのは、その約5.4秒後だ。
```

## c414
- id `G2-008`：G7-019 と1つに（何の理由か・母船に響いた音）。詰めた（A）
```diff
-> 母船にあったビデオカメラに、通信のパソコンの画面と、
-> 船体に響いた「ドン」という音が、録られていたからだ。
+> カナダの調べが秒まで言えるのは、母船のビデオカメラに、パソコンの画面と、
+> 母船に響いた「ドン」という音が、録られていたからだ。
```

## c415
- id `G2-007`：係の案どおり（G0 が原文に引き直した）（A）
- id `G7-020`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-> 母船が受け取った時刻も、2つの調べで合っている。違うのは、壊れた時刻だけだ。
-> Q: 送ったのは、どっちでも壊れる前なんだね。
+> 母船が受け取った時刻も、米沿岸警備隊とカナダで合っている。違うのは、壊れた時刻だ。
+> Q: 届いたのが壊れる前か後かは、調べで違うんだね。
```

## c419
- id `G7-002`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 残っているのは、時刻と深さの記録だけだ。
+> 残っているのは、時刻と深さ、そして音の記録だ。
```

## c501
- id `G2-013`：係の案どおり（G0 が原文に引き直した）（D）
- id `G7-021`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-**c501** ／ 実写 指令センターの B-roll（DVIDS 887734・2023-06-20・c107 と別の区間・A＝副題「米沿岸警備隊の指令センター（6月20日）」） ／ NTSB p.17（`first assumed there was an issue with the acoustic communications equipment`）・USCG p.39〈31〉（`None of the messages were answered and the TITAN’s location was never reacquired by the POLAR PRINCE.`）
+**c501** ／ 実写 指令センターの B-roll（DVIDS 887734・2023-06-20・c107 と別の区間・A＝副題「米沿岸警備隊の指令センター（6月20日）」） ／ NTSB p.17（`first assumed there was an issue with the acoustic communications equipment`…`sent two to three messages every minute`）・USCG p.39〈31〉（`None of the messages were answered and the TITAN’s location was never reacquired by the POLAR PRINCE.`）
-> 呼んでいない。母船にいた会社の担当は、まず通信の装置の不具合を疑った。
+> すぐには呼ばなかった。母船にいた会社の担当は、まず通信の装置の不具合を疑った。
```

## c504
- id `G2-024`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 18時までの海面の捜索で、手がかりは何も見つからなかった。
+> 18時までの捜索で、手がかりは見つからなかった。
```

## c505
- id `G2-014`：係の案どおり（G0 が原文に引き直した）（D）
- id `G7-022`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-**c505** ／ 図 帯 同じ帯（18:27 電話が切れた・18:55 カナダの救難調整センターへ→ボストンへ） ／ USCG p.39〈31〉（`I called the Joint Rescue Coordination Centre (JRCC) Halifax by sat phone but communications with JRCC were shortly thereafter cut-off.`）・TSB §1.3.3（`At 1855, the master of the Polar Prince called the Joint Rescue and Coordination Centre (JRCC) in Halifax`）
+**c505** ／ 図 帯 同じ帯（18:27 電話が切れた・18:55 カナダの救難調整センターへ→ボストンへ） ／ USCG p.39〈31〉（`I called the Joint Rescue Coordination Centre (JRCC) Halifax by sat phone but communications with JRCC were shortly thereafter cut-off.`）・TSB §1.3.3（`At 1855, the master of the Polar Prince called the Joint Rescue and Coordination Centre (JRCC) in Halifax`…`JRCC transferred the call to the Rescue Coordination Centre (RCC) in Boston`）
-> 18時55分の電話から、ボストンのアメリカ沿岸警備隊へとつながっていった。
+> 18時55分の電話から、ボストンの米沿岸警備隊へとつながっていった。
```

## c507
- id `G2-015`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c507** ／ 図 模式 母船の上の2つの組（会社の潜航の班と、船の会社の船長＝取り決めの書類が無い・船長の権限がはっきりしない） ／ TSB §2.5（`the situation with the Titan initially appeared to be a communication and tracking loss, and so the surface support team followed the missed communications protocol.`）・TSB §2.6（`did not follow the maritime best practice of notifying SAR authorities as soon as possible`）
+**c507** ／ 図 模式 母船の上の2つの組（会社の潜航の班と、船の会社の船長＝取り決めの書類が無い・船長の権限がはっきりしない） ／ TSB §2.5（`the situation with the Titan initially appeared to be a communication and tracking loss, and so the surface support team followed the missed communications protocol.`）・TSB §2.6（`the master’s authority in the loss of communication emergency with the Titan was unclear`）・§2.6（`Without a bridging document`）・§2.6（`missed communications protocol ended up taking precedence even though it did not follow the maritime best practice of notifying SAR authorities as soon as possible once the potential need for help developed`）
```

## c508
- id `G7-023`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> Q: 会社の手順のほうが、先になっていたんだね。
-> そう。知らせを受けたアメリカ沿岸警備隊は、この日の潜航を知らなかった。
+> Q: 外に知らせるより、会社の手順を先にしたんだね。
+> そう。知らせを受けた米沿岸警備隊は、この日の潜航を知らなかった。
```

## c509
- id `G7-024`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 22時、沿岸警備隊の輸送機がニューファンドランドから飛び立ち、
+> 22時、米沿岸警備隊の輸送機がニューファンドランドから飛び立ち、
```

## c512
- id `G2-018`：係の案どおり（G0 が原文に引き直した）（C）
```diff
+> 音が報じられたころ、5人はもう亡くなっていた。
```

## c513
- id `G2-019`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 限界の3,000メートルより約1,000メートル深く潜らせて、壊れた。
+> 限界の3,000メートルより1,000メートル近く深く潜らせて、壊れた。
```

## c514
- id `G2-021`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c514** ／ 実写 DVIDS 7875471 格納庫の HC-130（A＝副題「捜索に出た米沿岸警備隊の輸送機」） ／ USCG p.41〈33〉（`emergency transportation of a Pelagic® Odysseus ROV from Buffalo, NY`）・NTSB p.20（`flew the ROV Odysseus on a C-130 to Newfoundland and Labrador`）
+**c514** ／ 実写 DVIDS 7875471 格納庫の HC-130（A＝副題「捜索に出た米沿岸警備隊の輸送機」） ／ NTSB p.18（`which was capable of reaching 19,685 feet (6,000 meters). (The Odysseus was in Buffalo, New York, at the time.)`）・USCG p.41〈33〉（`emergency transportation of a Pelagic® Odysseus ROV from Buffalo, NY`）・NTSB p.20（`flew the ROV Odysseus on a C-130 to Newfoundland and Labrador, where it was loaded aboard the Horizon Arctic`）
```

## c515
- id `G0-020`：G7-028 の「その ROV を積んだ船」の「その」が、同じカットの1行目（フランスの ROV）を指して聞こえる＝バッファローの ROV と言う（G0 の通し読み）＝文は当て直しの係の案（R1-005・現場にそろった）
```diff
-> 6月22日、2つの船が、現場の上にそろった。
+> 6月22日、バッファローの ROV を積んだ船と、フランスの船が、現場にそろった。
```

## c520
- id `G2-022`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 海面に浮いても、外からボルトを外さないと出られなかった。
-> Q: 中からは、出られない作りだったんだね。
+> 海面に浮いても、台に戻し、外からボルトを外さないと出られなかった。
+> Q: 浮いてきても、すぐには出られなかったんだね。
```

## c522
- id `G2-023`：係の案どおり（G0 が原文に引き直した）（B）
- id `G0-M01`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> アメリカの運輸安全委員会は、国の指針どおりに備えていれば、
+> 米運輸安全委員会は、会社が国の指針どおりに救助の備えをしていれば、
```

## c523
- id `G7-030`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-> 残る問いは、海の底の残骸が答えている。
+> 最初の問いには、海の底の残骸が答えている。
```

## c601
- id `G3-015`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c601** ／ 実写 ROV「前のドーム」（NTSB ドケットの Pelagic video 2 of 2・c104・c522 と別の区間・第三者＝引用・額装・焼き込みは残る＝副題「海の底の残骸（6月22日）」） ／ NTSB p.20（`including the tail cone and both titanium domes`）・NTSB p.38（`ROVs discovered the wreckage about 330 meters (1,083 feet) east-northeast of the Titanic’s bow.`）
+**c601** ／ 実写 ROV「前のドーム」（NTSB ドケットの Pelagic video 2 of 2・c104・c522 と別の区間・第三者＝引用・額装・焼き込みは残る＝副題「海の底の残骸（6月22日）」） ／ NTSB p.20（`including the tail cone and both titanium domes`）・NTSB p.38（`ROVs discovered the wreckage about 330 meters (1,083 feet) east-northeast of the Titanic’s bow.`）・NTSB p.39（`Other pressure vessel fragments, likely from the middle or forward portion of the cylinder, were scattered about the ocean floor.`）
```

## c603
- id `G3-016`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 残骸は引き揚げられ、9月には、もう一度回収が行われた。
+> 残骸の一部が引き揚げられ、9月には、もう一度回収が行われた。
```

## c604
- id `G3-002`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-**c604** ／ 実写 FBI 図270 前のドームの窓の押さえの輪（ボルトが切れている所に赤い丸と矢印・USCG 報告 p.294・3枚組で小さい＝額装・A＝副題「前のドームの窓の押さえの輪（FBI 撮影）」） ／ TSB §1.6（`the retaining ring for the viewport was deformed in a manner that indicated the viewport had blown outward. The viewport was not found.`）
+**c604** ／ 実写 FBI 図270 前のドームの窓の押さえの輪（ボルトが切れている所に赤い丸と矢印・USCG 報告 p.294・3枚組で小さい＝額装・A＝副題「前のドームの窓の押さえの輪（FBI 撮影）」） ／ TSB §1.6（`the retaining ring for the viewport was deformed in a manner that indicated the viewport had blown outward. The viewport was not found.`）・USCG p.293〈285〉（`the viewport was ejected outward during the implosion`）
-> 窓は、外へ押し出されたとみられている。
+> 窓は爆縮のとき、外へ押し出されたとみられている。
```

## c605
- id `G3-003`：係の案（窓が先に壊れたのではない・技術者の証言）を詰め、呼び名を米沿岸警備隊に（C）
- id `R1-008`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c605** ／ 実写 24-011 図47 の下（前のドームの窓の座・NTSB 研究所の撮影・A＝紙面の引用の型＝副題「前のドームの窓の座（研究所）」） ／ TSB §2.1（`the manner in which the retaining ring was deformed suggested that the viewport had not failed`）・USCG p.280〈272〉（`it is unlikely that the acrylic window itself caused the implosion`）
-> カナダの調べは、窓は壊れていなかったとみる。アメリカ沿岸警備隊も、
-> 窓の破片が残骸に無く、筒の残りも窓から壊れた形と合わないとして、
-> 窓が原因だった見込みは低い、とした。
+**c605** ／ 実写 24-011 図47 の下（前のドームの窓の座・NTSB 研究所の撮影・A＝紙面の引用の型＝副題「前のドームの窓の座（研究所）」） ／ TSB §2.1（`the manner in which the retaining ring was deformed suggested that the viewport had not failed`）・USCG p.280〈272〉（`it is unlikely that the acrylic window itself caused the implosion`）・p.280〈272〉（`the most probable failure mode for the acrylic window would have been inward. In such a scenario, fragments of acrylic would likely have been found in the debris.`）
+> カナダの調べは、輪の曲がり方から、窓が先に壊れたのではない、とみる。
+> 米沿岸警備隊も、窓が原因の見込みは低いとした。窓から壊れたなら、
+> 内へ割れて破片が残っていただろう、という証言も引く。
```

## c606
- id `G3-001`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-**c606** ／ 実写 FBI 図159 前部セグメント（青いシートの上・証拠の札・USCG 報告 p.189・A＝副題「前のチタンの輪（FBI 撮影）」） ／ TSB §2.1（`suggested that the pressure hull’s carbon fibre cylinder was the likeliest point of failure`）・USCG p.269〈261〉（`a loss of structural integrity of the carbon fiber or glue joint within the TITAN’s cylindrical pressure hull`）
+**c606** ／ 実写 FBI 図159 前部セグメント（青いシートの上・証拠の札・USCG 報告 p.189・A＝副題「前のチタンの輪（FBI 撮影）」） ／ TSB §2.1（`suggested that the pressure hull’s carbon fibre cylinder was the likeliest point of failure`）・USCG p.269〈261〉（`a loss of structural integrity of the carbon fiber or glue joint within the TITAN’s cylindrical pressure hull`）・NTSB p.61（`The postcasualty condition of the Titan pressure vessel was consistent with a local buckling failure.`）
-> 3つの調べの見方は、炭素繊維の筒と、その継ぎ目のあたりで重なる。
-> 壊れ始めた一点までは、決めきれていない。
+> 3つの調べは、炭素繊維の筒の側を指す。米沿岸警備隊は、
+> チタンの輪との継ぎ目も挙げる。壊れ始めた一点までは、決めきれていない。
```

## c608
- id `G7-033`：係の案どおり（G0 が原文に引き直した）（E）
```diff
-> こすれたような見た目で、内側の層が前から一部離れていた印かもしれない、
-> とアメリカ沿岸警備隊は書く。
+> こすれたような見た目で、内側の層がすでに一部離れていた印かもしれない、
+> と米沿岸警備隊は書く。
```

## c610
- id `G3-017`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 貼り合わせた面が離れることで、剥離という。分かれ目は、主に2か所だった。
+> 貼り合わせた面が離れることで、剥離という。分かれ目は、2か所だった。
```

## c611
- id `G0-M02`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> アメリカの運輸安全委員会の研究所は、回収した破片の1枚を調べた。
+> 米運輸安全委員会の研究所は、回収した破片の1枚を調べた。
```

## c612
- id `G7-035`：係の案どおり（G0 が原文に引き直した）（E）
```diff
-> その表の接着の面は、こすれて、平らになっていた。
+> 破片に残った接着剤の面は、こすれて、平らになっていた。
```

## c613
- id `G3-018`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 接着剤の中の小さなすき間、空隙には、こすれて出た粉が詰まっていた。
+> 接着剤の中の小さなすき間、空隙には、こすれて出た粉がたまっていた。
```

## c614
- id `G7-036`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> そう。1枚目と2枚目の層が、別々に縦に動かないと、
-> この粉はできない、とアメリカ沿岸警備隊は書いている。
+> そう。1枚目と2枚目の層が、別々に長さの向きに動かないと、
+> この粉はできない、と米沿岸警備隊は書いている。
```

## c618
- id `G7-037`：係の案どおり（G0 が原文に引き直した）（E）
- id `G0-M03`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> アメリカの運輸安全委員会は、前からの剥離と、そのあと加わった傷が、
+> 米運輸安全委員会は、爆縮の前からの剥離と、そのあと加わった傷が、
```

## c619
- id `G3-012`：係の案どおり（出典の欄＋橋を「炭素繊維の筒が選ばれたころ」に＝第6章は2015年の材料選びから始まる）（C）
```diff
-**c619** ／ 図 模式 筒の端の断面（剥離の起きた2つの面に、長い空隙が並ぶ＝c610 の図の拡大） ／ NTSB p.59（`these adhesive interfaces contained long extended voids`）
+**c619** ／ 図 模式 筒の端の断面（剥離の起きた2つの面に、長い空隙が並ぶ＝c610 の図の拡大） ／ NTSB p.59（`these adhesive interfaces contained long extended voids`）・NTSB p.42（`end pieces that had been trimmed from the v2 full-scale cylinder during the construction/production process`）
-> では、層は、いつ、なぜはがれたのか。話は、この筒が生まれたころにさかのぼる。
+> では、層は、いつ、なぜはがれたのか。話は、炭素繊維の筒が選ばれたころにさかのぼる。
```

## c701
- id `G3-011`：聞き役（反応）のあとなので「そう、」は付けず、widely used の「広く」を足す（C）
```diff
-> 使っている。強くて軽く、形も作りやすいからだ。
+> 広く使われている。強くて軽く、形も作りやすいからだ。
```

## c703
- id `G3-010`：係の案どおり（G0 が原文に引き直した）（D）
- id `G7-039`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-**c703** ／ 図 模式 ふつうの深海の潜水艇の殻（鋼かチタンの球）とタイタンの殻（炭素繊維の筒）の並べ図 ／ TSB §1.13（`submersibles used for deep-ocean diving are typically constructed of steel or titanium,`）・TSB 脚注53（`With the exception of the Titan, the TSB is not aware of any other carbon-fibre pressure hulls for human occupancy used for deep-ocean diving.`）
+**c703** ／ 図 模式 ふつうの深海の潜水艇の殻（鋼かチタンの球）とタイタンの殻（炭素繊維の筒）の並べ図 ／ TSB §1.13（`submersibles used for deep-ocean diving are typically constructed of steel or titanium,`…`and the pressure hull for human occupancy is typically spherical in shape`）・TSB 脚注53（`With the exception of the Titan, the TSB is not aware of any other carbon-fibre pressure hulls for human occupancy used for deep-ocean diving.`）
-> 人が乗る深海用の炭素繊維の殻は、タイタンのほかに知られていない。
+> カナダの調べが知る限り、人が乗る深海用の炭素繊維の殻は、タイタンのほかに無い。
```

## c706
- id `G3-009`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 2015年6月、外部の会社が設計書をまとめた。会社の望みは、
+> 2015年6月、外部の会社が設計書をまとめた。オーシャンゲートの望みは、
```

## c708
- id `G7-040`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 当時の会社は、アメリカの機械学会の規格の、最低1.5に拠っていた。
+> 当時の会社は、アメリカの機械学会の規格の、最低1.5に従っていた。
```

## c709
- id `G3-019`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 外部の会社の応力の解析では、壊れる深さは約1万3,200メートル。
+> 外部の会社の強さの計算では、壊れる深さは約1万3,200メートル。
```

## c710
- id `G3-008`：係の案どおり（G0 が原文に引き直した）（A）
- id `G0-M04`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> ただ、この計算は、形も繊維の向きも完全な、理論の模型の上の値だった。
-> 実物で確かめるべきだった、とアメリカの運輸安全委員会は書く。
+> ただ、この計算は、形も繊維の向きも完全だとした、理屈の上の値だった。
+> 実物で確かめるべきだった、と米運輸安全委員会は書く。
```

## c711
- id `G3-014`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c711** ／ 図 模式 3分の1の模型（炭素繊維の筒と炭素繊維のドーム・加圧の矢印） ／ TSB §1.12.1（`One of the carbon fibre end domes failed at pressures equivalent to depths of around 3000 m.`）
+**c711** ／ 図 模式 3分の1の模型（炭素繊維の筒と炭素繊維のドーム・加圧の矢印） ／ TSB §1.12.1（`In December 2015, OceanGate conducted a pressure test on this one-third scale model at the UW-APL`…`One of the carbon fibre end domes failed at pressures equivalent to depths of around 3000 m.`）
```

## c712
- id `G3-007`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> CEO は、出資者などへの手紙に書いた。
+> CEO は、会社の関係者への手紙に書いた。
```

## c713
- id `G7-043`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 模型の試験はそのあとも重ねたが、目標の4,500メートルには届かなかった。
+> 模型の試験はそのあとも重ねたが、運航で目指した4,500メートルには届かなかった。
```

## c714
- id `G7-044`：問いを中身で聞く形は採り、立ち会うのは試験（NTSB p.22）。定期の検査は画の札へ（字数：2回目の試し組みでも上限を67字超えた）（C）
```diff
-> Q: 船級って、何？
-> 国とは別の団体が、設計を見て工事に立ち会い、試験を確かめる仕組みだ。
-> 合格すると証明書が出て、そのあとも定期の検査が要る。
+> Q: 船の安全は、外の誰かが確かめないの？
+> 船級という仕組みがある。船級協会という民間の団体が、設計や工事を確かめ、
+> 試験に立ち会って、証明書を出す。
```

## c715
- id `G3-013`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c715** ／ 図 帯 船級の年表（2016年 船級の相談→2018年 あきらめる→2019年2月 ブログ） ／ NTSB p.22（`the company planned to class the submersible through Lloyd’s Register or DNV.`）・NTSB p.23（`In 2018, OceanGate abandoned classing efforts.`）
+**c715** ／ 図 帯 船級の年表（2016年 船級の相談→2018年 あきらめる→2019年2月 ブログ） ／ NTSB p.22（`the company planned to class the submersible through Lloyd’s Register or DNV.`）・NTSB p.23（`the OceanGate CEO ultimately decided classing the Titan would take too long`…`In 2018, OceanGate abandoned classing efforts.`）
-> 2018年に、あきらめた。
+> 2018年に、会社はあきらめた。
```

## c717
- id `G0-M05`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> アメリカの運輸安全委員会は、そう書く。
+> 米運輸安全委員会は、そう書く。
```

## c719
- id `G3-005.1`：出典の欄は係の案。語りは G7-045 の言い方（料金を取って人を乗せる以上、呼び名を変えるだけでは）（A）
- id `G3-005.2`：出典の欄は係の案。語りは G7-045 の言い方（料金を取って人を乗せる以上、呼び名を変えるだけでは）（A）
- id `R1-013`：呼び名をそろえる。「元技術者の社員」は硬い＝「米沿岸警備隊で技術者だった社員」（A）
```diff
-**c719** ／ 図 再現 社員の懸念の一節（NTSB p.47 が引く英字＋訳は字幕） ／ NTSB p.47（`who had previous experience as an engineer/machinery technician in the US Coast Guard`）・p.47（`you can’t just change the title of a person when you’re receiving compensation.”`）
-> 社内にも、声はあった。沿岸警備隊で技術者だった社員は、
-> 報酬を受け取る以上、肩書きを変えるだけでは済まない、と CEO に伝え、
+**c719** ／ 図 再現 社員の懸念の一節（NTSB p.47 が引く英字＋訳は字幕） ／ NTSB p.47（`who had previous experience as an engineer/machinery technician in the US Coast Guard`）・p.47（`the company accepting paying clients as “mission specialists.”`）・p.47（`you can’t just change the title of a person when you’re receiving compensation.”`）・p.47（`The technician resigned following this conversation`）
+> 社内にも、声はあった。米沿岸警備隊で技術者だった社員は、
+> 料金を取って人を乗せる以上、呼び名を変えるだけでは済まない、と CEO に伝え、
```

## c802
- id `G4-001`：点検の相手は潜水艇（TSB・USCG）。「運航を受け持つ」は字数で外した（字数：2回目の試し組みでも上限を67字超えた）（B）
```diff
-> そのころ、運航を受け持つ運航部長が、船体を点検した。
+> そのころ、運航部長が、潜水艇を点検した。
```

## c803
- id `G0-M06`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> 事故のあと、アメリカの運輸安全委員会も、1つ目の船体の切り落とした端を調べた。
+> 事故のあと、米運輸安全委員会も、1つ目の船体の切り落とした端を調べた。
```

## c804
- id `G4-026`：係の案どおり（G0 が原文に引き直した）（A）
- id `R1-003`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 報告は、筒と接着の線を全部点検して確かめ、その結果を、
+> 報告は、筒と、チタンの輪との接着の線を全部点検して確かめ、その結果を、
```

## c807
- id `G7-047`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-> Q: 安全のことを言ったのに、辞めさせられたの？
+> Q: 辞めさせられた人は、黙っていたの？
```

## c808
- id `G4-002`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-> 元運航部長は、船員を守る法律にもとづき、労働安全衛生局に申し立てた。
+> 元運航部長は、安全を訴えたための解任だとして、労働安全衛生局に申し立てた。
```

## c809
- id `G4-003`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> Q: 安全を心配した人が、会社を去ったんだね。
+> Q: 安全を心配した人が、会社を追われたんだね。
```

## c811
- id `G0-012`：字数：届き方の割れ（口頭か手紙か）は台本で言わない＝「届き方は調べによって違うが」を外した
```diff
-> 届き方は調べによって違うが、その中身は、CEO に伝わっていた。
+> その中身は、CEO に伝わっていた。
```

## c814
- id `G4-004`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> Q: ひびが入った船体は、どうなったの？
+> Q: 音がした船体は、どうなったの？
-> 表面の下の剥離から始まっていた。
+> 表面の下の剥離から始まっていたとみられた。
```

## c815
- id `G4-005`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c815** ／ 図 模式 筒の内側の亀裂の位置（前の左舷に3つ＝カナダの調べの値・剥離の札） ／ NTSB p.26（`the first director of engineering stated that he told the CEO that because there was a crack, the pressure vessel hull was “done,”`）・p.26（`The director of engineering stated that he would not sign off on the planned 2019 expedition.`）
+**c815** ／ 図 模式 筒の内側の亀裂の位置（前の左舷に3つ＝カナダの調べの値・剥離の札） ／ NTSB p.26（`the first director of engineering stated that he told the CEO that because there was a crack, the pressure vessel hull was “done,”`）・p.26（`The director of engineering stated that he would not sign off on the planned 2019 expedition.`）・USCG p.161〈153〉（`However, the Director of Engineering refused`）
```

## c816
- id `G4-006`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c816** ／ 図 再現 客への手紙の要点（2019年の遠征の中止・亀裂の語が無い） ／ USCG p.162〈154〉（`OceanGate did not make any external notifications`）・NTSB p.26（`The planned 2019 expedition to the Titanic wreck site was cancelled.`）
+**c816** ／ 図 再現 客への手紙の要点（2019年の遠征の中止・亀裂の語が無い） ／ USCG p.162〈154〉（`OceanGate did not make any external notifications`）・NTSB p.26（`The planned 2019 expedition to the Titanic wreck site was cancelled.`）・USCG p.164〈156〉（`The letter, nor any other separate correspondence, disclosed that there was a crack found`）
```

## c818
- id `G4-007`：係の案どおり（G0 が原文に引き直した）（B）
- id `R1-001`：🔴 G0 が TSB §1.12.1 で確かめた＝depth rating を3,000m に下げ、2,000m より深く潜らない了解。「潜ってよい深さ」を3,000m にすると原文の2,000m とぶつかる＝了解の方を語りで言う（格付けの数は画の帯の札へ）（B）
```diff
-> 10月、亀裂のある船体をメリーランドの施設で加圧すると、亀裂と剥離が増えた。
-> 11月、会社は船体の等級を4,000メートルから3,000メートルに下げた。
+> 10月、亀裂のある船体を加圧する試験のあと、亀裂と剥離がさらに見つかった。
+> 11月、会社は、この船体で潜るのを2,000メートルまでとした。
```

## c819
- id `G4-008`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c819** ／ 実写 24-011 図39 1つ目と2つ目の筒の切り落とした端の厚さの比べ（定規・青い背景・NTSB 研究所・A＝副題「1つ目（左）と2つ目の筒の端（研究所）」） ／ NTSB p.45（`trimmed end piece of first full-scale Titan pressure vessel`）
+**c819** ／ 実写 24-011 図39 1つ目と2つ目の筒の切り落とした端の厚さの比べ（定規・青い背景・NTSB 研究所・A＝副題「1つ目（左）と2つ目の筒の端（研究所）」） ／ NTSB p.62（`after the failure of the v1 full-scale pressure vessel, OceanGate used different materials (pre-preg carbon fiber) and manufacturing methods`）
```

## c902
- id `G4-010.1`：噂がどちらの船体の話でも閉じられるよう、両方の材料の出どころを言う（USCG p.118〈110〉・p.174〈166〉）。「日本の」は3冊の字ではない＝外した（B）
- id `G4-010.2`：噂がどちらの船体の話でも閉じられるよう、両方の材料の出どころを言う（USCG p.118〈110〉・p.174〈166〉）。「日本の」は3冊の字ではない＝外した（B）
```diff
-**c902** ／ 図 再現 材料の発注の要点（2020年・東レのアメリカの会社・テープの品名は出さない） ／ USCG p.174〈166〉（`The specific pre-preg system used was Toray Composite Materials America’s P2362W-19L`）・p.174〈166〉（`On February 21, 2020, OceanGate issued a purchase order for 7,700 lbs of P2362W-190U-013 composite material from Toray Composites`）
-> テープは、日本の東レのアメリカの会社の物で、2020年に買っている。
+**c902** ／ 図 再現 材料の発注の要点（2020年・東レのアメリカの会社・テープの品名は出さない） ／ USCG p.118〈110〉（`The carbon fiber material used for the first TITAN hull was standard-modulus Grafil 37-800`）・p.174〈166〉（`The specific pre-preg system used was Toray Composite Materials America’s P2362W-19L`）・p.174〈166〉（`On February 21, 2020, OceanGate issued a purchase order for 7,700 lbs of P2362W-190U-013 composite material from Toray Composites`）
+> 1つ目の筒の糸は三菱ケミカル系、2つ目のテープは東レの米国の会社の物だ。
```

## c903
- id `G4-011`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> この材料で作った3分の1の模型は、2020年の試験で、壊れたか、壊れる寸前だった。
+> この材料の3分の1の模型2つは、2020年の試験で、壊れたか、壊れる寸前だった。
```

## c904
- id `G4-012`：係の案どおり（G0 が原文に引き直した）（B）
- id `R1-014`：「請負」は硬い。「会社と、解析の会社」は会社が2度続く＝オーシャンゲートの名で分ける（A）
```diff
-> 原因は、炭素繊維の層の一部にできた、波のようなうねりと見られた。
+> オーシャンゲートと解析の会社は、原因を、層の一部にできた、波のようなうねりと見た。
```

## c907
- id `G4-028`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-> カナダの調べでは、この作り方を強く求めたのは、作り手の会社だった。
+> カナダの調べでは、この作り方は、作り手の会社が強く求めた。
```

## c908
- id `G4-013`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c908** ／ 図 帯 年表（2020年11月〜2021年1月 実物大の筒・模型は作らず） ／ NTSB p.62（`OceanGate did not build or test any new sub-scale models using the co-bonding process`）・p.62（`the only article produced using the co-bonding process was the v2 full-scale cylinder ultimately used in the casualty dive.`）
+**c908** ／ 図 帯 年表（2020年11月〜2021年1月 実物大の筒・模型は作らず） ／ NTSB p.28（`between November 2020 and January 2021.`）・NTSB p.62（`OceanGate did not build or test any new sub-scale models using the co-bonding process`）・p.62（`the only article produced using the co-bonding process was the v2 full-scale cylinder ultimately used in the casualty dive.`）
```

## c909
- id `G4-014`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c909** ／ 実写 NTSB 図16 の下＝事故の船体の端材のしわの削り跡（研究所・A＝副題「しわを削った跡（事故の船体の端材）」） ／ TSB §1.12.2（`The carbon fibre plies in these areas were ground down by OceanGate to make them flush with the rest of the outer surface before the next layer was added.`）・§1.12.2（`Grinding down the carbon fibre severed some of the fibres and introduced defects on the surface.`）
+**c909** ／ 実写 NTSB 図16 の下＝事故の船体の端材のしわの削り跡（研究所・A＝副題「しわを削った跡（事故の船体の端材）」） ／ TSB §1.12.2（`The carbon fibre plies in these areas were ground down by OceanGate to make them flush with the rest of the outer surface before the next layer was added.`）・§1.12.2（`Grinding down the carbon fibre severed some of the fibres and introduced defects on the surface.`）・§1.12.2（`Grinding did not mitigate ply waviness below the outer surface of each layer of the cylinder.`）
```

## c910
- id `G4-015`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-> どこまで削ったのか、記録は残っていない。
+> どこまで削ったのか、記録されていない。
```

## c911
- id `G4-029`：係の案どおり（G0 が原文に引き直した）（C）
- id `G0-M07`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> 筒は両端に余りをつけて作り、あとで切り落とした。
-> 事故のあと、アメリカの運輸安全委員会は、その端材を調べた。
+> 事故のあと、米運輸安全委員会は、筒の両端の余りを切り落とした端材を調べた。
```

## c913
- id `G4-016`：係の案どおり（G0 が原文に引き直した）（A）
- id `R1-002`：🔴 G0 が NTSB p.40 で確かめた（2つの剥離は残骸で見た＝investigators could see・Piece A〜D）（B）
```diff
-> 1枚目と2枚目、3枚目と4枚目のあいだ。海の底で、はがれていた面だ。
+> 1枚目と2枚目の層、3枚目と4枚目の層のあいだ。残骸の映像で、はがれていた面だ。
```

## c914
- id `G4-017`：係の案どおり（G0 が原文に引き直した）（B）
- id `G0-M08`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> そう。アメリカの運輸安全委員会は、この作り方は、しわを無くしきれず、
-> ほかの異常も持ち込んだ、とまとめている。
+> そう。米運輸安全委員会は、この作り方は、しわやうねりを無くしきれず、
+> ほかの異常も持ち込んだ、とみている。
```

## c915
- id `G0-017`：字数：1文に詰めた（c920 の「カナダの研究所」と同じ呼び方）
```diff
-> カナダの運輸安全委員会の研究所も、2つ目の筒の端材を手に入れ、
-> 18の試料に切って、試験した。
+> カナダの研究所も、2つ目の筒の端材を、18の試料に切って試験した。
```

## c916
- id `G4-018`：係の案どおり（G0 が原文に引き直した）（D）
- id `R1-009`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c916** ／ 実写 24-011 図28 2つ目の筒の切り落とした端面のうねり（黄の目盛り・NTSB 研究所・A＝副題「端面に見える層のうねり（研究所）」） ／ TSB §1.15（`there was a general waviness in the plies.`）
+**c916** ／ 実写 24-011 図28 2つ目の筒の切り落とした端面のうねり（黄の目盛り・NTSB 研究所・A＝副題「端面に見える層のうねり（米運輸安全委員会の研究所）」） ／ TSB §1.15（`there was a general waviness in the plies.`）
```

## c917
- id `G4-009.1`：c901 に足すと1カット4行＝1.25 の出どころ（2020年に会社が ISO に合わせた・TSB §1.12.2）は c917 の頭に置いた。c708 の「最低1.5」（2015年）と時期で分かれる（C）
- id `G4-009.2`：c901 に足すと1カット4行＝1.25 の出どころ（2020年に会社が ISO に合わせた・TSB §1.12.2）は c917 の頭に置いた。c708 の「最低1.5」（2015年）と時期で分かれる（C）
```diff
-**c917** ／ 図 棒 安全率（長さの向き3.05・周りの向き1.11・必要な1.25 の線＝何メートルでの値かは書かない） ／ TSB §1.15（`as evidenced by the calculated safety factor of 3.05, which was greater than the required 1.25.`）・§1.15（`the calculated safety factor was 1.11, which did not meet the required safety factor of 1.25.`）
-> 試料から計算した安全率は、長さの向きで3.05。必要な1.25を、十分に上回った。
-> ところが周りの向きは、1.11。必要な1.25に、届いていなかった。
+**c917** ／ 図 棒 安全率（長さの向き3.05・周りの向き1.11・必要な1.25 の線＝何メートルでの値かは書かない） ／ TSB §1.12.2（`OceanGate also changed its safety factor to 1.25`）・§1.15（`as evidenced by the calculated safety factor of 3.05, which was greater than the required 1.25.`）・§1.15（`the calculated safety factor was 1.11, which did not meet the required safety factor of 1.25.`）
+> 2020年、会社は安全率の基準を、国際規格に合わせて1.25にしていた。
+> 試料から計算した安全率は、長さの向きで3.05。十分に上回った。
+> ところが周りの向きは、1.11。1.25に、届いていなかった。
```

## c918
- id `G4-019`：係の案どおり（G0 が原文に引き直した）（A）
- id `G7-054`：G4-019（決まり→基準）にそろえて「基準の半分も無い」（C）
- id `R1-006`：係の案どおり（G0 が原文に引き直した）（A）
- id `R1-007`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**c918** ／ 図 模式 棚のたとえ（いつも100キロを載せる棚＝決まりは125キロまで耐える／この筒の周りの向き＝111キロまで・式は §9） ／ —
+**c918** ／ 図 模式 棚のたとえ（いつも100キロを載せる棚＝基準は125キロまで耐える／この筒の周りの向き＝111キロまで・式は §9） ／ —
-> いつも100キロを載せる棚なら、125キロまで耐えるように作る、という決まりだ。
-> この筒の周りの向きは、111キロまでしか耐えない計算になる。
+> いつも100キロを載せる棚なら、125キロまで耐えるように作る、という基準だ。
+> この筒の周りの向きは、111キロまで。余裕は、求める分の半分も無い計算だ。
```

## c919
- id `G7-055`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> それより深い圧力に、くり返しさらされるのは、安全ではなかった。
+> それより深い圧力に、加圧試験も含めてくり返しさらされるのは、安全ではなかった。
```

## c920
- id `G0-003`：画の欄の「アメリカの研究所の試料で」も、語り（G4-020）にそろえて誰の試料で誰が計算したかを書く
- id `G4-020`：係の案どおり（G0 が原文に引き直した）（B）
- id `G0-M09`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-**c920** ／ 図 棒 疲れの寿命（アメリカの研究所の試料で、いちばん強い物＝耐えた見込み／いちばん弱い物＝82% を超えて使った可能性） ／ TSB §1.16（`would reasonably have been expected to survive based on the sample with the highest compressive strength value`）・§1.16（`it could have used more than 82% of its fatigue life in the time up to the occurrence dive based on the sample with the lowest compressive strength value.`）
-> アメリカの研究所の試料では、いちばん強い物なら耐えた見込みだが、
-> いちばん弱い物なら、事故の潜航までに、くり返しで壊れるまでの寿命の、
-> 82%を超えて使っていた可能性があるという。
+**c920** ／ 図 棒 疲れの寿命（米運輸安全委が試した試料でカナダの研究所が計算、いちばん強い物＝耐えた見込み／いちばん弱い物＝82% を超えて使った可能性） ／ TSB §1.16（`would reasonably have been expected to survive based on the sample with the highest compressive strength value`）・§1.16（`it could have used more than 82% of its fatigue life in the time up to the occurrence dive based on the sample with the lowest compressive strength value.`）
+> カナダの研究所は、米運輸安全委員会が試した試料でも計算した。
+> いちばん強い物なら耐えた見込み。いちばん弱い物なら、事故の潜航までに、
+> くり返しで壊れるまでの寿命の、82%を超えて使っていた可能性がある。
```

## c921
- id `G4-025`：係の案どおり（G0 が原文に引き直した）（D）
- id `G4-027`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-**c921** ／ 図 帯 2021年2〜3月の加圧試験4回（4,000m 前後・4,200m は1回・20分＝米沿岸警備隊の書き方・タイタニックの約3,840m の線） ／ TSB §1.12.2（`In February and March 2021, the pressure hull was tested at the Deep Ocean Test Facility. Four tests were done.`）・NTSB p.58（`marginally greater than the 3,840-meter (12,598-foot) dive depth required to reach the Titanic.`）
-> 2021年2月から3月、完成した船体は、4,000メートル前後の加圧を4回受け、
+**c921** ／ 図 帯 2021年2〜3月の加圧試験4回（4,000m 前後・4,200m は1回・20分＝米沿岸警備隊の書き方・タイタニックの約3,840m の線） ／ TSB §1.12.2（`In February and March 2021, the pressure hull was tested at the Deep Ocean Test Facility. Four tests were done.`）・TSB §1.15（`the Titan had 4 successful pressure tests at the Deep Ocean Test Facility`）・NTSB p.58（`marginally greater than the 3,840-meter (12,598-foot) dive depth required to reach the Titanic.`）
+> 2021年2月から3月、船体は、4,000メートル前後の加圧を4回受け、
```

## c922
- id `G4-021`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 会社は、傷は音の監視の装置で、その場で見つけられる、と説明していた。
+> くり返しの計算を聞かれた会社は、傷は音の監視でその場で分かる、と答えていた。
```

## c923
- id `G0-004`：G4-022 の語り（タイタニックに遠く及ばない・窓は取り替えた）の出どころを出典の欄に足す（TSB §1.12.1・§1.12.2）
- id `G4-022`：係の案（タイタニックに遠く及ばない）を採り、「窓は取り替えた」は出典の欄（G0-004）に置いて語りは詰めた（A）
```diff
-**c923** ／ 図 模式 前のドームの窓（内側が平ら・外側がふくらんだ形・等級の札＝約650m〈米沿岸警備隊・カナダ〉／1,000m の認証〈米運輸安全委〉） ／ USCG p.278〈270〉（`certified the window to a pressure rating of 945 psi, corresponding to a depth of only 650 m (2,133 feet).`）・NTSB p.30（`an acrylic window certified to 1,000 meters (3,281 feet).`）
-> 前のドームの窓も、心配された所だ。最初の窓の等級は、約650メートル。
-> アメリカの運輸安全委員会は、1,000メートルまでの認証と書く。
+**c923** ／ 図 模式 前のドームの窓（内側が平ら・外側がふくらんだ形・等級の札＝約650m〈米沿岸警備隊・カナダ〉／1,000m の認証〈米運輸安全委〉） ／ USCG p.278〈270〉（`certified the window to a pressure rating of 945 psi, corresponding to a depth of only 650 m (2,133 feet).`）・NTSB p.30（`an acrylic window certified to 1,000 meters (3,281 feet).`）・TSB §1.12.1（`only a fraction of what OceanGate required for dives to the Titanic`）・§1.12.2（`The new viewport from Germany was installed in this construction`）
+> 前のドームの窓も心配された。最初の窓が認められた深さは約650メートルで、
+> タイタニックに遠く及ばない。米運輸安全委員会は1,000メートルと書く。
```

## ca01
- id `G5-002`：係の案どおり（G0 が原文に引き直した）（D）
- id `G7-058`：問い「次の年の夏には」で年が伝わる＝語りの「2022年の夏、」は足さない（字数：1回目の試し組みで上限を444字超えた＝足しの言い添えを戻した）（C）
```diff
-**ca01** ／ 図 再現 TSB 付録B の表の2022年の13行（深さ「3840」の7行を明るく・欄は英字のまま） ／ NTSB p.35（`the Titan reached 3,840 meters (12,598 feet) seven times`）・USCG p.235〈227〉（`While 7 of the 13 dives reached the TITANIC depth of 3840 m`）
-> Q: その夏、何があったの？
+**ca01** ／ 図 再現 TSB 付録B の表の2022年の13行（深さ「3840」の7行を明るく・欄は英字のまま） ／ NTSB p.35（`the Titan reached 3,840 meters (12,598 feet) seven times`）・USCG p.235〈227〉（`While 7 of the 13 dives reached the TITANIC depth of 3840 m`）・TSB 脚注75（`Dives without people on board are not included.`）
+> Q: 次の年の夏には、何があったの？
```

## ca02
- id `R2-023`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> カナダの調べの付録によると、7月3日、潜水艇はタイタニックの船首の左側にぶつかり、
+> カナダの調べによると、7月3日、潜水艇はタイタニックの船首の左側にぶつかり、
```

## ca03
- id `G5-003`：係の案（傷んだかは分からない・米沿岸警備隊の帰属・「そう。」で受ける）。途中の行の終わりを読点にした（B）
- id `R2-009`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 傷みの量は分からないが、カナダの調べは、これも傷みの出どころの候補に挙げる。
-> そして7月15日。タイタニックの中を近くで見ようと降りた潜水艇は、
+> そう。傷んだかは分からないが、カナダの調べは、これも傷みの出どころの候補に挙げる。
+> そして7月15日、米沿岸警備隊によると、潜水艇はタイタニックの中をのぞこうと降り、
```

## ca04
- id `G5-004`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 米沿岸警備隊によると、事故としての報告は、出されなかった。
+> 事故としての報告は、出されなかった。
```

## ca06
- id `G7-059`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-> Q: 音を記録する装置も、付いていたの？
-> 付いていた。船体の中の音を拾うセンサーが8つ、ひずみを測る計器が16。
+> Q: 音の監視の装置って、どんな物？
+> 船体の中の音を拾うセンサーが8つと、ひずみを測る計器が16。
```

## ca07
- id `G5-006`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 米沿岸警備隊の記録では、15時26分45秒、装置は大きな音の山をとらえた。
+> 米沿岸警備隊の分析では、15時26分45秒、装置は大きな音の山をとらえた。
```

## ca08
- id `G7-060`：係の案どおり（G0 が原文に引き直した）（E）
- id `G0-M10`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
- id `R2-022`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 音は、15時17分ごろから増え始めていた。アメリカの運輸安全委員会は、
-> 15時15分から30分ごろのあいだ、と幅で書いている。
+> 音は、15時17分ごろから増え始めていた。米運輸安全委員会は、
+> 15時15分から15時30分ごろのあいだ、と幅で書く。
```

## ca09
- id `G0-019`：字数：1行目と同じ中身（ずれた音）の言い直し＝「そう伝えられた」に詰めた（出典の欄の NTSB p.36 は残す）
```diff
-> 社員と客にも、船体が金属の受け台の中でずれた、と伝えられた。
+> 社員と客にも、そう伝えられた。
```

## ca10
- id `G5-007`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**ca10** ／ 図 模式 筒と内張り（外から見るだけ＝層のあいだのはがれは外から見えない） ／ USCG p.290〈282〉（`no effort was made to remove the TITAN’s insert or take the submersible temporarily out of service for a more detailed assessment.`）
+**ca10** ／ 図 模式 筒と内張り（外から見るだけ＝層のあいだのはがれは外から見えない） ／ USCG p.289〈281〉（`a cursory external examination of the TITAN was conducted following the loud bang with no visible damage identified.`）・USCG p.290〈282〉（`no effort was made to remove the TITAN’s insert or take the submersible temporarily out of service for a more detailed assessment.`）
```

## ca11
- id `G7-061`：係の案どおり（G0 が原文に引き直した）（A）
- id `G0-M11`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> アメリカの運輸安全委員会によると、CEO はデータを見たうえで、技術部長に言った。
-> 「もう一度潜って、どうなるか見よう」。
+> 米運輸安全委員会によると、CEO はデータを見たうえで、
+> 当時の技術部長に言った。「もう一度潜って、どうなるか見よう」。
```

## ca13
- id `G5-008`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> Q: データはあっても、読める人がいなかったんだね。
+> Q: その場には、データを読める人がいなかったんだね。
```

## ca14
- id `G5-009`：係の案どおり（G0 が原文に引き直した）（A）
- id `G5-010`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**ca14** ／ 図 帯 2022年7月の年表（15日 80回目→19日 81回目→22日 82回目→23日 83回目） ／ NTSB p.36（`the submersible reached 3,840 meters (12,598 feet) on dives 81 and 82 and 2,954 meters (9,692 feet) on the final dive of the expedition.`）・TSB §2.1.1（`4 days before the subsequent dive on 19 July 2022`）
-> そう。4日後の7月19日、次の潜航。22日の潜航も、タイタニックの深さまで。
+**ca14** ／ 図 帯 2022年7月の年表（15日 80回目→19日 81回目→22日 82回目→23日 83回目） ／ NTSB p.36（`the submersible reached 3,840 meters (12,598 feet) on dives 81 and 82 and 2,954 meters (9,692 feet) on the final dive of the expedition.`）・NTSB p.51（`The last of these dives (dive 83) took place on July 23, 2022, but at a different dive location`）・TSB §2.1.1（`4 days before the subsequent dive on 19 July 2022`）
+> そう。4日後の7月19日と、22日の潜航は、どちらもタイタニックの深さまで。
```

## ca15
- id `G0-014`：字数：1文に詰めた
- id `G5-011`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**ca15** ／ 図 再現 付録B の 2022-07-19 の行（備考 `Thruster control mapping failure, electrical problems`） ／ USCG p.235〈227〉（`The pilot overcame the malfunctioning thrusters by turning the controller around and operating the controls in reverse.`）
-> 19日の潜航では、推進器の向きの割り当てが逆になった。
-> 操縦士はコントローラーを逆さに持って、そのまま続けた。
+**ca15** ／ 図 再現 付録B の 2022-07-19 の行（備考 `Thruster control mapping failure, electrical problems`） ／ USCG p.235〈227〉（`The pilot overcame the malfunctioning thrusters by turning the controller around and operating the controls in reverse.`）・USCG p.311〈303〉（`the dive proceeded after the pilot compensated for the failures instead of ascending for repairs in a controlled environment.`）
+> 19日は推進器の操作が逆になり、操縦士はコントローラーを逆さに持って続けた。
```

## ca16
- id `G7-062`：係の案どおり（G0 が原文に引き直した）（C）
- id `G0-M12`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> 会社は、ひずみを時刻に沿って並べて見ていた。これでは潜航どうしを比べにくい、
-> とアメリカの運輸安全委員会は書く。
+> 会社は、ひずみを時刻に沿って並べて見ていた。
+> 米運輸安全委員会によると、これでは潜航どうしを比べにくい。
```

## ca17
- id `G7-063`：係の案どおり（G0 が原文に引き直した）（A）
- id `R2-007`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 事故のあと、同じデータを深さに沿って並べ直すと、80回目までは、
+> 事故のあと、同じデータを深さに沿って並べ直すと、あの音の潜航までは、
```

## ca18
- id `G5-012`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**ca18** ／ 図 NTSB 図21 の右（81〜83回目の浅い所の「Non-linear behavior」を明るく） ／ NTSB p.53（`During dive 81, the first dive after the audible event, the strain response at low depth was non-linear.`）
+**ca18** ／ 図 NTSB 図21 の右（81〜83回目の浅い所の「Non-linear behavior」を明るく） ／ NTSB p.53（`During dive 81, the first dive after the audible event, the strain response at low depth was non-linear.`）・NTSB p.59 脚注42（`The strain response at greater depths remained linear, similar to previous dives`）
```

## ca19
- id `G5-013`：なぜ浅い所だけか（NTSB p.59）を足し、1カット3行に収めた（C）
- id `G0-M13`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
- id `R2-002`：係の案どおり（G0 が原文に引き直した）（more consistent with を戻す・R2-022・R2-023 で埋める）（B）
```diff
-> 層と層がはがれたときに、よく合う形だという。その計器は筒の前の端にあり、
-> 傷みは前の端まで届いていた、とアメリカの運輸安全委員会は書く。
+> 層のはがれとよく合う、と米運輸安全委員会は書く。はがれた層は浅い所で別々に動き、
+> 深い所ではまとまって動く。計器は筒の前の端にあり、傷みはそこまで届いていた。
```

## ca20
- id `G5-014`：係の案どおり（G0 が原文に引き直した）（B）
- id `R2-006`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 前の年の夏は全体より21%大きく、2022年7月19日は98%大きかった。
+> 2021年8月5日の潜航は全体より21%、2022年7月19日は98%大きかった。
```

## ca21
- id `G5-015`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**ca21** ／ 図 帯 3つの見方の並べ（米沿岸警備隊＝強く示す／米運輸安全委＝可能性が高い／カナダ＝決められない） ／ USCG p.289〈281〉（`strongly suggests that the carbon fiber hull sustained irreversible damage at the end of Dive 80.`）・NTSB p.59（`the NTSB concludes that the Titan pressure vessel likely sustained damage after it surfaced at the end of dive 80`）
+**ca21** ／ 図 帯 3つの見方の並べ（米沿岸警備隊＝強く示す／米運輸安全委＝可能性が高い／カナダ＝決められない） ／ USCG p.289〈281〉（`strongly suggests that the carbon fiber hull sustained irreversible damage at the end of Dive 80.`）・USCG p.289〈281〉（`It is likely that the loud bang heard on the surface during Dive 80 was the result of a sudden delamination occurring between layers 1 and 2`）・NTSB p.59（`the NTSB concludes that the Titan pressure vessel likely sustained damage after it surfaced at the end of dive 80`）
```

## ca22
- id `G5-016`：係の案どおり（G0 が原文に引き直した）（B）
- id `R2-005`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-> カナダの調べは、きちんと調べなかったので、あの音が線の曲がりのきっかけかは、
-> 決められない、とした。
-> Q: きっかけかどうかは、まだ決まっていないんだね。
+> カナダの調べは、会社が音のあと船体をきちんと調べなかったので、
+> あの音が線の曲がりのきっかけかは、決められない、とした。
+> Q: 会社が調べなかったから、決められないんだね。
```

## ca25
- id `G5-017`：帰属を足すと1カット4行＝2行に詰め、G7-064（とらえたのに警告が出ない、の矛盾）も同じ行で解いた（B）
- id `G5-018`：係の案どおり（G0 が原文に引き直した）（D）
- id `G0-M14`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
- id `R2-001`：🔴 G0 が NTSB p.65 で確かめた（the dives that followed dive 80 … never produced the type of … alert・initial damage）（B）
```diff
-**ca25** ／ 図 再現 警告の基準の出どころ（1つ目の船体と模型の音＝作り方の違う船体） ／ NTSB p.31（`The warning levels were based on the acoustic activity of the v1 pressure vessel`）・NTSB p.65（`never produced the type of acoustic emission signal that would have triggered an alert and thus did not detect the initial damage.`）
-> 警告の基準は、作り方の違う1つ目の船体と、模型の音から決めていた。
-> あの音のあとも、警告を出す形の音は出ず、最初の傷みに気づけなかった。
+**ca25** ／ 図 再現 警告の基準の出どころ（1つ目の船体と模型の音＝作り方の違う船体） ／ NTSB p.31（`The warning levels were based on the acoustic activity of the v1 pressure vessel`）・NTSB p.64（`the v1 full-scale pressure vessel and sub-scale models were manufactured using a different method`）・NTSB p.65（`never produced the type of acoustic emission signal that would have triggered an alert and thus did not detect the initial damage.`）
+> 米運輸安全委員会によると、警告の基準は、作り方の違う1つ目の船体と、
+> 模型の音で決めた。音のあとの潜航でも警告の形にならず、最初の傷みに気づけなかった。
```

## ca26
- id `G5-019`：赤信号の主語は音の記録（USCG）。詰めた（B）
- id `R2-008`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> そう。米沿岸警備隊は、あの音は、すべての潜航を止める赤信号だったはずだ、と書く。
+> そう。米沿岸警備隊は、あの音とひずみの記録は、
+> すべての潜航を止める赤信号だったはずだ、と書く。
```

## cb02
- id `G5-020`：G7-065（同じ事実の4回目）と1つにした＝前の冬と、この冬を1行で比べる（B）
```diff
-> 前の冬は、本社のある町へ運び、屋内に置いていた。
-> この冬、潜水艇は、覆いも無いまま外にあった。
+> 前の冬は、アメリカへ運び戻していた。この冬は、覆いも無いまま外にあった。
```

## cb04
- id `G5-021`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> セントジョンズの冬は、最高気温の平均でも、摂氏マイナス0.5度。
+> この冬、12月から2月のセントジョンズは、最高気温の平均でもマイナス0.5度。
```

## cb05
- id `G5-022`：係の案どおり（G0 が原文に引き直した）（B）
- id `G0-M15`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> アメリカの運輸安全委員会とカナダの調べは、可能性までとする。
+> 米運輸安全委員会もカナダの調べも、外での傷みは「あり得る」までだ。
```

## cb07
- id `G5-023`：係の案どおり（G0 が原文に引き直した）（字数：1回目の試し組みで上限を444字超えた＝足しの言い添えを戻した）（C）
- id `R2-016`：語りを外した片を欄から外す（G5-023 の対）（D）
```diff
-**cb07** ／ 実写 MBI 図109 岸壁の台（LARS）と白い浮き（USCG 報告 p.142・2023-06-25 撮影・c305 の図5 と同じ場面の別の写真・A＝副題「潜水艇を載せる台（事故の後に撮影）」） ／ USCG p.238〈230〉（`what we really wanted to do was bring the sub back, at least, to Everett and pull the insert and look at`）・TSB §1.23（`at certain times in 2022 and 2023, OceanGate employees were asked to volunteer to defer their pay because of issues with company finances.`）
+**cb07** ／ 実写 MBI 図109 岸壁の台（LARS）と白い浮き（USCG 報告 p.142・2023-06-25 撮影・c305 の図5 と同じ場面の別の写真・A＝副題「潜水艇を載せる台（事故の後に撮影）」） ／ USCG p.238〈230〉（`what we really wanted to do was bring the sub back, at least, to Everett and pull the insert and look at`）
-> だが、できなかった、と当時の技術部長は証言している。会社のお金は苦しく、
-> 2022年と2023年には、社員が給料の後払いを頼まれていた。
+> だが、できなかった、と当時の技術部長は証言している。
```

## cb08
- id `G5-024`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 技術の責任者の席は、空いたままだった。
+> 技術の責任者の席は、正式には空いたままだった。
```

## cb09
- id `G0-011`：字数：免除の申し込みの1文（TSB だけの事実・G5-025）は、台に載せて引いた話の途中で話題が跳ぶ（G7-067）＝外した。カナダの監督の穴は cc07
- id `R2-017`：語りを外した片を欄から外す（G0-011 の対）（D）
```diff
-**cb09** ／ 図 地図 セントジョンズから現場まで（母船の後ろに台ごと引く線） ／ TSB §1.20.2（`because the Polar Prince did not have equipment to lift the Titan and the LARS on and off the deck.`）・USCG p.246〈238〉（`the LARS and TITAN had to be towed behind the POLAR PRINCE for the entirety of each 2023 TITANIC mission.`）・TSB §1.20.1.2（`there had been no application for an MTRB exemption submitted for the charter with OceanGate.`）
+**cb09** ／ 図 地図 セントジョンズから現場まで（母船の後ろに台ごと引く線） ／ TSB §1.20.2（`because the Polar Prince did not have equipment to lift the Titan and the LARS on and off the deck.`）・USCG p.246〈238〉（`the LARS and TITAN had to be towed behind the POLAR PRINCE for the entirety of each 2023 TITANIC mission.`）
-> 後ろに引いて運ばれた。乗客の数の決まりを超えるための、
-> 免除の申し込みも、出されていなかった。
+> 後ろに引いて運ばれた。
```

## cb10
- id `G5-026`：約950時間は引かれていた＋綱でつながれていた時間の合計（TSB）。道のり（USCG）の1文は字数で外した（画の棒に残す）（字数：2回目の試し組みでも上限を67字超えた）（B）
- id `R2-013`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> その年、潜水艇が引かれていた時間は、合わせて約950時間。
-> 道のりは、5,000キロを超えた。
+> その年、母船の綱につながれていた時間は、合わせて約950時間。
```

## cb11
- id `G0-018`：字数
- id `R2-012`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 波の高さは、最大3.35メートルあった。
+> 波の高さの目安は、最大3.35メートルあった。
```

## cb12
- id `G5-027`：係の案どおり（G0 が原文に引き直した）（C）
- id `G5-028`：係の案どおり（G0 が原文に引き直した）（D）
- id `R2-014`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-**cb12** ／ 実写 NTSB 図10 傾いた台（撮影は個人＝第三者＝額装・改変なし・④' と映像方針で使うか確かめる＝副題「引かれて傾いた台（2023年5月）」） ／ TSB §1.21.1（`On the morning of 24 May, while en route to the wreck site, the LARS and the Titan partially submerged while under tow.`）・§1.21.1（`The Titan and the LARS partially submerged again on the return to St. John’s.`）
+**cb12** ／ 実写 NTSB 図10 傾いた台（撮影は個人＝第三者＝額装・改変なし・④' と映像方針で使うか確かめる＝副題「傾いた台（2023年5月20日と27日）」＝NTSB 図10 の凡例の日付・5月24日に半ば沈んだ場面ではない＝語りの5月24日と並べない（引かれて揺れた cb11 へ移す案）） ／ TSB §1.21.1（`On the morning of 24 May, while en route to the wreck site, the LARS and the Titan partially submerged while under tow.`）・§1.21.1（`The Titan and the LARS partially submerged again on the return to St. John’s.`）
-> カナダの調べでは、港へ戻る途中でも、もう一度沈んでいる。
-> Q: 運ぶだけで、そんなことになるんだ。
+> カナダの調べでは、港へ戻る途中でも、半ば沈んでいる。
+> Q: 運んでいるだけで、沈みかけたんだね。
```

## cb13
- id `G5-029`：係の案（not likely・主語と述語）。途中の行の終わりを読点にした（B）
```diff
-> 引かれたことの影響も、見方が分かれる。米沿岸警備隊は、さらに弱った可能性が高い。
-> カナダの調べは、引いただけでは原因にならないが、
-> すでにあった傷を広げたかもしれない、とする。
+> そう。引かれたことの影響も、見方が分かれる。米沿岸警備隊は、
+> 船体がさらに弱った可能性が高い、とみる。カナダの調べは、引いただけでは、
+> 原因になった見込みは低いが、すでにあった傷を広げたかもしれない、とする。
```

## cb14
- id `G5-030`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**cb14** ／ 図 再現 TSB 付録B の2023年の4行（10・10・10・3346） ／ TSB §1.21.4（`The dive was aborted at a depth of 10 m. The Titan did not disconnect from the LARS on this dive.`）・NTSB p.14（`None of the dives exceeded 33 feet (10 meters) depth.`）
+**cb14** ／ 図 再現 TSB 付録B の2023年の4行（10・10・10・3346） ／ TSB §1.21.4（`The dive was aborted at a depth of 10 m. The Titan did not disconnect from the LARS on this dive.`）・NTSB p.14（`None of the dives exceeded 33 feet (10 meters) depth.`）・USCG p.256〈248〉（`10 m dives were dives which did not leave the LARS platform.`）
```

## cb15
- id `G5-031`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 6月の3回目は、台の操作を誤り、潜水艇は波で約45分、台に打ちつけられた。
-> 米沿岸警備隊によると、そのあと船体を点検した記録は無い。
+> 米沿岸警備隊によると、3回目の潜航では、台の浮き沈みの調整を誤り、
+> 潜水艇は波で約45分、台に打ちつけられた。そのあと船体を点検した記録は無い。
```

## cb17
- id `G7-069.1`：ストライクの意味（USCG p.78〈70〉＝3つでその日の潜航をやめる）を足す。35が線の下なのは数で分かる＝言わない（字数：1回目の試し組みで上限を444字超えた＝足しの言い添えを戻した）（A）
- id `G7-069.2`：ストライクの意味（USCG p.78〈70〉＝3つでその日の潜航をやめる）を足す。35が線の下なのは数で分かる＝言わない（字数：1回目の試し組みで上限を444字超えた＝足しの言い添えを戻した）（A）
```diff
-**cb17** ／ 図 再現 危険度の点数（事故の回＝35・「48を超えるとストライク」の決まり＝TSB 図16 は使わず数だけ） ／ TSB §1.17.12.1（`The mission director checklist specified that a risk index of greater than 48 was considered to be a strike. The risk assessment for the occurrence dive (Figure 16) had a risk index of 35.`）
-> 6月18日の潜航の計画で、危険度の点数は35。
-> 会社の決まりでは、48を超えると「ストライク」とされていた。
+**cb17** ／ 図 再現 危険度の点数（事故の回＝35・「48を超えるとストライク」の決まり＝TSB 図16 は使わず数だけ） ／ TSB §1.17.12.1（`The mission director checklist specified that a risk index of greater than 48 was considered to be a strike. The risk assessment for the occurrence dive (Figure 16) had a risk index of 35.`）・USCG p.78〈70〉（`If there was a total of three or more “strikes” encountered during a dive evolution, the Mission Director was required to cancel the day’s dive operation.`）
+> 6月18日の潜航の計画で、危険度の点数は35。会社の決まりでは、
+> 48を超えると「ストライク」が1つ付き、3つたまると、その日の潜航をやめる。
```

## cb18
- id `G5-033`：係の案どおり（G0 が原文に引き直した）（B）
- id `G0-M16`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> アメリカの運輸安全委員会は、2022年の最後の深い潜航のあと、
+> 米運輸安全委員会は、2022年7月22日の潜航のあと、
```

## cb19
- id `G5-034`：係の案どおり（G0 が原文に引き直した）（B）
- id `G5-035`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**cb19** ／ 図 帯 2023年6月18日（この年初めて台を離れて深く潜る潜航） ／ USCG p.295〈287〉（`Dive 88 was the first dive to leave the LARS platform for the TITANIC Survey Expedition 2023`）
-> そして6月18日。それは、この年初めて台を離れ、深く潜る潜航だった。
-> Q: 船体を確かめないまま、その日を迎えたんだね。
+**cb19** ／ 図 帯 2023年6月18日（この年初めて台を離れて深く潜る潜航） ／ USCG p.295〈287〉（`Dive 88 was the first dive to leave the LARS platform for the TITANIC Survey Expedition 2023`）・NTSB p.16（`It was the first dive of the 2023 expedition to descend below 33 feet (10 meters).`）
+> そして6月18日。それは、この年、人が乗って初めて台を離れ、深く潜る潜航だった。
+> Q: 船体をよく確かめないまま、その日を迎えたんだね。
```

## cc03
- id `G6-008`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 解雇と、その圧力で、安全の懸念を言いにくくした職場も、その1つだ。
+> 幹部の解雇と、解雇の脅しで、安全の懸念を言いにくくした職場も、その1つだ。
```

## cc04
- id `G0-M17`：呼び名をそろえる（米運輸安全委員会・米沿岸警備隊＝初出の c102・c203 だけアメリカ）
```diff
-> Q: アメリカの運輸安全委員会は、どう書いたの？
+> Q: 米運輸安全委員会は、どう書いたの？
```

## cc05
- id `G6-003`：「寄与」を言い換え、2行目は主語（会社）だけ足した（係の短い案）（A）
```diff
-> 寄与したのは、指針や規則が、会社に業界の基準を守らせるには足りなかったこと。
-> そして、監視の記録の読み違いだ。
+> 原因を後押ししたのは、会社に業界の基準を守らせる規則や指針が、足りなかったこと。
+> そして、会社が監視の記録を読み違えたことだ。
```

## cc08
- id `G0-021`：「勧告のページにまだ載っていない」は3冊の外（G0 がアプリ内のブラウザで見た）＝出典の欄に注（R2-004 の親へ）
- id `G6-004`：聞き役を外し cc10 に移す（G6-004 と G6-005 は対）。返事の状態は G0 が TSB の勧告の頁で確かめた（2026-10-14・M26-02・04〜07 は N/A・M26-03 は頁なし）＝「勧告のページにまだ載っていない」と出どころを言う（「委員会のページ」はどの委員会か分からない＝G0 の通し読み）（C）
```diff
-**cc08** ／ 図 再現 TSB の勧告6つ（宛先は6つともカナダ運輸省・番号 M26-02〜07） ／ TSB §4.2（`The investigation identified safety deficiencies that led the Board to issue the following 6 recommendations.`）
+**cc08** ／ 図 再現 TSB の勧告6つ（宛先は6つともカナダ運輸省・番号 M26-02〜07） ／ TSB §4.2（`The investigation identified safety deficiencies that led the Board to issue the following 6 recommendations.`）・TSB の勧告のページ（rec-m2602・m2604〜m2607＝Date of the latest response: N/A・Not Yet Assessed／m2603 は頁なし＝2026-10-14 に見た・3冊の外・記録は src/new/tsb_rec/）
-> その答えは、2026年10月の時点で、まだ公表されていない。
-> Q: まだ、途中なんだね。
+> 運輸省の返事は、2026年10月の時点で、勧告のページにまだ載っていない。
```

## cc09
- id `G6-016`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**cc09** ／ 図 帯 3つの答えの並べ（重なる所＝窓でなく船体の炭素繊維の側・強さと寿命を確かめず・監視の読み方） ／ USCG p.325〈317〉（`the probable failure point of the hull was either the adhesive joint between the TITAN’s forward dome and the titanium segment or the carbon fiber hull near the forward end of the TITAN.`）・NTSB p.73（`the company was unaware of its actual strength and durability`）
+**cc09** ／ 図 帯 3つの答えの並べ（重なる所＝窓でなく船体の炭素繊維の側・強さと寿命を確かめず・監視の読み方） ／ USCG p.325〈317〉（`the probable failure point of the hull was either the adhesive joint between the TITAN’s forward dome and the titanium segment or the carbon fiber hull near the forward end of the TITAN.`）・NTSB p.73（`the company was unaware of its actual strength and durability`）・TSB §2.1（`suggested that the pressure hull’s carbon fibre cylinder was the likeliest point of failure.`）・TSB §3.1（`OceanGate did not know for how long the pressure hull would remain safe`）
```

## cc10
- id `G6-005`：聞き役を cc08 から移す（G6-004 と対）（C）
- id `G6-017`：係の案どおり（G0 が原文に引き直した）（D）
- id `R2-010`：係の案どおり（G0 が原文に引き直した）（C）
```diff
-**cc10** ／ 図 帯 同じ並べ（分かれる所＝2022年の音の重み・最後の数秒の順番を明るく） ／ TSB §1.10.10.1（`so it cannot be determined whether this event precipitated the non-linear readings on 19 July 2022.`）
-> 分かれるのは、2022年の音の重みと、最後の数秒の順番だ。
+**cc10** ／ 図 帯 同じ並べ（分かれる所＝2022年の音の重み・最後の数秒の順番を明るく） ／ USCG p.289〈281〉（`strongly suggests that the carbon fiber hull sustained irreversible damage at the end of Dive 80.`）・NTSB p.73（`The Titan pressure vessel likely sustained damage after it surfaced at the end of dive 80`）・TSB §1.10.10.1（`so it cannot be determined whether this event precipitated the non-linear readings on 19 July 2022.`）
+> Q: 分かれる所は？
+> 2022年の音をどれだけ重く見るかと、最後の数秒の順番だ。
```

## cc11
- id `G6-006`：係の案どおり（G0 が原文に引き直した）（A）
- id `G6-018`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**cc11** ／ 図 再現 規則と監督の穴の重み（米運輸安全委＝寄与／米沿岸警備隊＝その他の要因／カナダ＝危険の所見） ／ TSB §3.2（`Canada’s approach to regulatory oversight of vessels enabled the Titan to operate without any independent verification to identify safety deficiencies,`）
+**cc11** ／ 図 再現 規則と監督の穴の重み（米運輸安全委＝寄与／米沿岸警備隊＝その他の要因／カナダ＝危険の所見） ／ NTSB p.74（`Contributing were US and international voluntary guidance and US small passenger vessel regulations`）・USCG p.8〈viii〉（`the lack of comprehensive and effective regulations for the oversight and operation of manned submersibles`）・TSB §3.2（`Canada’s approach to regulatory oversight of vessels enabled the Titan to operate without any independent verification to identify safety deficiencies,`）・TSB §3.2（`These factors may or may not have been causal or contributing to the occurrence`）
-> Q: 止められたのは、まず会社自身だったってこと？
+> Q: 止めることができたのは、まず会社自身だったってこと？
```

## cc13
- id `G7-073`：係の案どおり（G0 が原文に引き直した）（E）
```diff
-> 社員が仕返しを恐れずに懸念を言え、早さより安全を先にしていれば、
+> 社員が仕返しを恐れずに懸念を言える場をつくり、早さより安全を先にしていれば、
```

## cd01
- id `G7-074`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> Q: 最初の問いの答えは、出たの？
+> Q: はじめに立てた問いの答えは、出たの？
```

## cd02
- id `G6-002`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> 窓ではなく、船体の炭素繊維の側だ。層は爆縮の前からはがれ、
-> 潜るたびの傷で弱って、押しつぶされたとみられる。
+> 窓ではなく、船体の炭素繊維の側だ。層の一部は爆縮の前からはがれ、
+> 傷が重なって弱り、押しつぶされたとみられる。
```

## cd03
- id `G6-019`：係の案どおり（G0 が原文に引き直した）（D）
- id `G7-075`：「なぜ」に届くよう、調べは要らないとした指示と読み解ける人の不在を足した（USCG p.290）。詰めた（C）
- id `R2-003`：係の案どおり（G0 が原文に引き直した）（B）
- id `R2-015`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**cd03** ／ 図 再現 同じ札（②なぜ潜り続けたのか） ／ USCG p.290〈282〉（`should have been a red flag to stop all dive operations. However, OceanGate proceeded to continue scheduled dive operations afterward,`）・USCG p.289〈281〉（`a cursory external examination of the TITAN was conducted following the loud bang with no visible damage identified.`）
-> 次に、なぜ潜り続けたのか。2022年の音のあと、会社は外から軽く見ただけで、
-> 記録も読み違え、予定どおり潜った。
+**cd03** ／ 図 再現 同じ札（②なぜ潜り続けたのか） ／ USCG p.290〈282〉（`should have been a red flag to stop all dive operations. However, OceanGate proceeded to continue scheduled dive operations afterward,`）・USCG p.289〈281〉（`a cursory external examination of the TITAN was conducted following the loud bang with no visible damage identified.`）・USCG p.290〈282〉（`directed that no further investigation or assessments were necessary`）・USCG p.290〈282〉（`neither the Director of Engineering nor anyone else onboard with the authority to assess the submersible’s safety possessed the necessary engineering expertise to interpret the strain gauge data`）
+> 次に、なぜ潜り続けたのか。2022年の音のあと、CEO は調べは要らないと指示し、
+> その場に記録を読み解ける人もいないまま、外から軽く見ただけで、予定どおり潜った。
```

## cd04
- id `G6-001`：係の案に「誰なら止められたのか」（G7-005）。1行41字に詰めた（B）
- id `G6-020`：係の案どおり（G0 が原文に引き直した）（D）
```diff
-**cd04** ／ 図 再現 同じ札（③誰が止められたのか） ／ USCG p.307〈299〉（`this tragedy would likely have been averted`）・TSB §1.23.1（`some OceanGate employees with expertise in specific areas left the company or were dismissed after raising safety-related concerns`）・NTSB p.70（`the existing regulations and voluntary guidance, as currently written, enabled OceanGate’s operation of the Titan in an unsafe manner.`）
-> そして、誰が止められたのか。3つの報告書が先に挙げるのは、会社自身だ。
-> 止めようとした人もいたが、懸念を言った人は、会社を去った。
-> 外から止める仕組みが働かなかったことは、その次に書かれている。
+**cd04** ／ 図 再現 同じ札（③誰が止められたのか） ／ USCG p.307〈299〉（`this tragedy would likely have been averted`）・NTSB p.74（`the probable cause of the hull failure and implosion of the submersible Titan was OceanGate’s inadequate engineering process,`）・TSB §3.1（`These are the factors that were found to have caused or contributed to the occurrence.`）・TSB §1.23.1（`some OceanGate employees with expertise in specific areas left the company or were dismissed after raising safety-related concerns`）・NTSB p.70（`the existing regulations and voluntary guidance, as currently written, enabled OceanGate’s operation of the Titan in an unsafe manner.`）
+> そして、誰なら止められたのか。3つの報告書が主な原因に挙げるのは、会社自身だ。
+> 安全の懸念を言った社員の中には、辞めた人も、辞めさせられた人もいた。
+> 外から止める仕組みが働かなかったことは、主な原因の次に置かれている。
```

## cd06
- id `G7-076`：係の案どおり（G0 が原文に引き直した）（B）
- id `R2-011`：係の案どおり（G0 が原文に引き直した）（A）
```diff
-> 危なさは少しずつ増えるので、気づかれにくい、とも書く。
+> 安全なやり方からのずれは少しずつで、気づかれにくい、とも書く。
```

## cd07
- id `G6-011`：係の案どおり（G0 が原文に引き直した）（B）
```diff
-> この事故は強く思い出させる、と結んでいる。
+> この事故は強く思い出させる、と書いている。
```

## cd09
- id `G0-022`：承認①（カズヤくん）＝コメントの問いは C（④の注「軽く聞こえる恐れ」を見たうえで）
```diff
-> あなたは、この事故のことを、この動画を見る前から知っていましたか。
+> あなたは、もし乗れるとしたら、深い海の底を自分の目で見てみたいですか。
```

## カットの外（§1〜§3・§5〜・章の見出し。頭と §0 は除く）
- id `G0-005`：§1-5 の D3（現場までの距離）を、語りの幅（約700〜800キロ＝G1-015）に合わせる
- id `G0-006`：§9 の c219 の行を幅の言い方に合わせる（c304 の語りに距離は無い）
- id `G0-007`：§9 の c205・c301 の行を「70メートル近い」（G1-016）に合わせる
- id `G0-008`：§6 の読みを c413 の「約5.4秒」（G7-018）に合わせる
- id `G0-009`：§8 の用語集の船級を c714 の言い方（NTSB p.22＝立ち会うのは試験）に合わせる（G3-006 の親へ）
- id `G0-010`：§1-5 に母船の長さの割れ（G1-016）を足す
- id `G0-023`：承認①の記録（題）
- id `G0-024`：承認①の記録（サムネの赤）
- id `G0-025`：承認①の記録（問い）
- id `G4-024`：係の案どおり（G0 が原文に引き直した）（§9 に c918 の行）（D）
- id `G6-013`：係の案どおり（G0 が原文に引き直した）（§1-1 の題 B の注意書き）（B）
- id `G6-014`：係の案どおり（G0 が原文に引き直した）（§9 の見出しの重なり）（D）
- id `G6-015`：係の案どおり（G0 が原文に引き直した）（§9 に cb10 の行）（D）
- id `R2-018`：係の案どおり（G0 が原文に引き直した）（D）
- id `R2-019`：係の案どおり（G0 が原文に引き直した）（D）
- id `R2-020`：係の案どおり（G0 が原文に引き直した）（D）
- id `R2-021`：係の案どおり（G0 が原文に引き直した）（⑤a の読みで「べい」）（E）
```diff
+- 🆕 **承認①（2026-10-14・④'のチャット）＝保留。最有力は A（70字）**（カズヤくん）。④'が推した「事故の11か月前」（73字）は選ばれなかった＝⑥でアップロードの前にもう一度決める
-| B | タイタニックへ潜る潜水艇、安全の余裕は決まりの1.25に届かない1.11だった。タイタン号潜水艇事故の真相【事故検証】【ゆっくり解説】 | 67 | c9＝TSB §1.15。⚠️ 安全率は本編の後半＝題で引いて冒頭で回収できない |
+| B | タイタニックへ潜る潜水艇、安全の余裕は決まりの1.25に届かない1.11だった。タイタン号潜水艇事故の真相【事故検証】【ゆっくり解説】 | 67 | c9＝TSB §1.15。⚠️ 安全率は本編の後半＝題で引いて冒頭で回収できない。⚠️「決まりの1.25」は言い過ぎ（TSB の字は required・1.25 は会社が ISO に合わせた値＝TSB §1.12.2）＝使うなら「必要な1.25」（c917 と同じ）。1.11 は周りの向きだけ・試料が実物を代表するならの前提つき（TSB §1.15） |
+- ✅ **承認①（2026-10-14）＝A「犠牲5人 異音の4日後も潜航」**（カズヤくん・④の推奨どおり）
+- ✅ **承認①（2026-10-14）＝C「あなたは、もし乗れるとしたら、深い海の底を自分の目で見てみたいですか。よければ、コメントで教えてください。」**（カズヤくん・下の④の注を見たうえで C）＝cd09 に入れた（④'）
-| 現場までの距離（D3） | 約685キロ（米2機関の370海里） | TSB 約425海里 | USCG p.5〈v〉・NTSB p.1 |
+| 母船の長さ（🆕④'） | 70メートル近い（c301） | NTSB 220フィート（p.14）＝67.1m・表E-2 は 220.4ft＝67.2m／TSB 表1 69.07m | NTSB p.14・p.85・TSB 表1（§1.1） |
+| 現場までの距離（D3） | 約700〜800キロ（④'で幅に＝米2機関の370海里＝約685キロと TSB の約425海里＝約787キロ・c219） | TSB 約425海里 | USCG p.5〈v〉・NTSB p.1 |
-| 5.397秒 | ごてんさんきゅうなな びょう | c413 |
+| 約5.4秒 | やく ごてんよん びょう（④'で 5.397 から丸めた） | c413 |
+| 米運輸安全委員会・米沿岸警備隊 | べい うんゆあんぜんいいんかい・べい えんがんけいびたい（「こめ」と読ませない） | 全体（④'で呼び名をそろえた＝G0-M） |
-- 船級（せんきゅう）…国とは別の団体が、船の設計を見て工事に立ち会い、試験を確かめて証明する仕組み
+- 船級（せんきゅう）…国とは別の民間の団体（船級協会）が、船の設計や工事を確かめ、大事な試験に立ち会って証明する仕組み
-## 9. 換算と計算（式）
-| c205・c301 | 全長6.7メートル／約67メートル | 22ft×0.3048＝6.71m（NTSB p.19 脚注13 も 6.7m）／220ft×0.3048＝67.1m |
+| c205・c301 | 全長6.7メートル／全長70メートル近い | 22ft×0.3048＝6.71m（NTSB p.19 脚注13 も 6.7m）／220ft×0.3048＝67.1m（NTSB）・TSB 表1 は 69.07m＝どちらも「70メートル近い」（④'・G1-016） |
-| c219・c304 | 約685キロ | 370海里（USCG p.5〈v〉・NTSB p.1）×1.852＝685.2km。⚠️ TSB は「約425海里」（D3）＝台本は米2機関の値 |
+| c219 | 約700〜800キロ | 370海里（USCG p.5〈v〉・NTSB p.1）×1.852＝685.2km／425海里（TSB）×1.852＝787.1km＝④'で幅に（G1-015）。画の札も幅か、帰属つきの2つの値で |
-| cb04 | 摂氏マイナス0.5度 | TSB §1.22 は「-0.5°」とだけ書く（摂氏はカナダの気温の慣例と、TSB がほかの所で °C を使うことからの読み＝推測） |
+| cb04 | マイナス0.5度（④'で「摂氏」を外した＝G5-021） | TSB §1.22 は「-0.5°」とだけ書く（摂氏はカナダの気温の慣例と、TSB がほかの所で °C を使うことからの読み＝推測） |
+| cb10 | 画の札だけ＝約5,400km（語りの「5,000キロを超えた」は④'で外した＝G5-026） | 2,900NM×1.852＝5,370.8km（USCG p.294〈286〉 more than 2,900 NM＝2023年の遠征の季節）。「〜を超えた」は more than と向きが合う |
+| c918 | 100キロ・125キロ・111キロ | 安全率＝壊れる荷÷ふだんの荷（c707＝NTSB p.24 脚注21 の深さの比を荷に置き換えた）。100×1.25＝125・100×1.11＝111（TSB §1.15 の 1.25・1.11）。何メートルでの値かは §1.15 に無い＝たとえに深さを足さない |
```
