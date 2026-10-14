# 22本目 ④' 原文の照合 G5（第9章 ca01〜ca26・第10章 cb01〜cb19）

- 担当：G5（照合の係・書いた人とは別の目）・2026-10-14。台本・カード・設計図は書き換えていない
- 読んだもの：`daihon_v1.md` の 917〜1118 行・§0-1・§0-2・§1-5・§9／カード `src/cards/g5_ca-cb.md`（全部）／3冊は `pg22.py` で引き直した
  - USCG：p.233・234・235・236・237・238・282・283・286・289・290・294・295・80（page）＋ find で p.7・78・84・136・230・231・256・311・327・328
  - NTSB：p.31・36・51・52・53・58・59・60・64・65（page）＋ find で p.9 脚注1・p.14・p.16・p.35・p.38（図10 凡例）
  - TSB：§1.10.9・§1.10.10.1・§1.17.12.1・§1.20.1.2・§1.20.2.2・§1.21.1（2つ）・§1.22・§2.1.3・付録B（2022・2023年の行）・脚注75（sec／fn）＋ find で §1.7・§1.20.2・§1.23.1
- 判定の印：**OK**＝原文と合う（理由を一言）／**ずれ**＝所見あり（`findings_G5.json` の id）／**要確認**＝画像か親の判断でしか決まらない
- 守ったこと：画像・動画は開いていない。ファイルは落としていない。ウェブは開いていない。私人の名前と CEO の名前は書いていない（USCG の片に名前が入る所は使わないか [CEO] にした）
- 所見の数：35（🔴2・🟡18・🟢15）。字数の増え（全部採ったとき）＝第9章 +92・第10章 +43。任意の物（G5-013・G5-019・G5-026）を外し、削る候補（G5-023）を採ると第9章 +41・第10章 +38（第9章は G5-008 も外せば +40）

## 照合の表

| カット | 当てた頁 | 判定 | 一言 |
|---|---|---|---|
| ca01 | NTSB p.35・USCG p.235〈227〉・TSB 付録B（2022年13行）・脚注75 | ずれ | 13回・7回は3冊で合う。ただ「その夏」が何年か分からない（直前 c921〜c923 は2021年の試験）＝語りに年（G5-001）。「人が乗った」は TSB 脚注75 を欄に（G5-002） |
| ca02 | TSB 付録B（2022-07-03）・§2.1.3 | OK | `collided with the port bow of the Titanic and was disabled on recovery` どおり・「カナダの調べの付録によると」と帰属あり。聞き役「ぶつかっていたんだ」は反応として可（ca03 を「そう。」で受ける案＝G5-003） |
| ca03 | TSB §2.1.3・USCG p.233〈225〉 4.34.8 | ずれ | 「近くで見ようと降りた」は USCG `descended for a closer view of TITANIC's interior` で合う（親の問いの出どころ＝ここ・客の1人の証言を地の文で）。ただ「傷みの量は分からない」が `if any` を落とす・階段は USCG だけなのに帰属なし（G5-003） |
| ca04 | USCG p.233〈225〉・p.311〈303〉 | OK | 親の問い：`the content expert, who was piloting the TITAN at the time`＝操縦していた・`work the controls to free the TITAN`＝外した で合う。ca03 に帰属を移すなら2行目の帰属は外せる（G5-004・字を浮かせるだけ） |
| ca05 | USCG p.233〈225〉・p.234〈226〉・p.290〈282〉・NTSB p.36・p.58・p.59・TSB §1.10.10.1・付録B | 要確認 | 語り「浮上の終わりの海面の近く」は3冊を包む（USCG＝まだ水の中・海面の近く／後の分析＝浮上の後、NTSB＝音は ascended・傷みは after it surfaced、TSB＝while it was surfacing）。画の「15:20ごろ 0m」は図の読みで文字に無い＝ca07 の 15:26:45 の山が浮上の後に見える恐れ（G5-005＝画像で） |
| ca06 | NTSB p.31・TSB §1.10.9 | OK | 音8・周8・縦8＝センサー8・ひずみ計16。画の「筒の内側に」は TSB `affixed to the interior of the pressure hull` で合う |
| ca07 | USCG p.283〈275〉・p.286〈278〉・p.235〈227〉 | ずれ | 時刻と「同じ瞬間・一瞬で」は `occurred in a fraction of a second and coincided with` で合う。「米沿岸警備隊の記録では」は記録した主を取り違えて聞こえる（元は会社の装置）→「分析では」（G5-006） |
| ca08 | USCG p.283〈275〉・NTSB p.52 | OK | `approximately 3:17 p.m.`＝ごろ・`between about 1515 and 1530`＝幅で、ぼかしを残している |
| ca09 | USCG p.233〈225〉・NTSB p.36 | OK | 会社の結論（`caused by a shift in the TITAN’s position within its frame`）と、社員と客への説明（`were told the hull had shifted in its metal cradle`）を分けて書けている |
| ca10 | USCG p.290〈282〉・p.289〈281〉・p.233〈225〉 | ずれ | 語りは合う。「外から見ただけ」の片が欄に無い（G5-007・欄だけ） |
| ca11 | NTSB p.36 | OK | 帰属「アメリカの運輸安全委員会によると」あり。NTSB の地の文（`The CEO wanted to continue operations and, after inspecting the strain and acoustic emission data, told the director of engineering`）。USCG はデータを見たのは技術部長と書く（割れ）が、帰属があるので可 |
| ca12 | USCG p.290〈282〉 | OK | `directed that no further investigation or assessments were necessary ahead of the next scheduled 2022 dive or during the TITAN’s extended layup period` どおり・帰属あり |
| ca13 | USCG p.290〈282〉 | ずれ | 語りは onboard（その場）・with the authority（安全を判断する立場）の限定を残していて OK。聞き役のまとめが限定を落とし「会社に一人もいない」に広がる（G5-008・軽い） |
| ca14 | NTSB p.36・p.51・p.60・USCG p.235〈227〉・TSB §2.1.1・付録B | ずれ | 「4日後」は TSB `4 days before the subsequent dive on 19 July 2022` で合う。19日もタイタニックの深さだと分かる形に（G5-009）。親の問い「23日・別の場所」の出どころ＝NTSB p.51（`took place on July 23, 2022, but at a different dive location`）・USCG p.235（海山）＝欄に足す（G5-010）。NTSB p.60 は7月25日と書く（NTSB の中の揺れ） |
| ca15 | USCG p.235〈227〉・p.311〈303〉・TSB 付録B（2022-07-19） | ずれ | 語りは合う（`The thruster control mapping was found to be incorrect`・`turning the controller around`）。「そのまま続けた」の片が欄に無い（G5-011・欄だけ） |
| ca16 | NTSB p.51・p.64 | OK | `plotting it side-by-side with dive depth as a function of time`・`difficult for OceanGate to compare data between dives` どおり・帰属あり |
| ca17 | NTSB p.53・USCG p.290〈282〉 | OK | `Through dive 80, the strain response of the hull was linear at all depths (a typical mechanical behavior).` どおり。「事故のあと」は USCG `plotted post-casualty`・NTSB p.64 `after the implosion` |
| ca18 | NTSB p.53・p.59・脚注42 | ずれ | 語りは合う（81〜83回目の浅い所の非線形）。「深い所はまっすぐのまま」の片が欄に無い（G5-012・欄だけ） |
| ca19 | NTSB p.59 | ずれ | `more consistent with a delamination`＝よく合う・`indicating that the damage extended to the forward end` で合う。ただ聞き役の「どういうこと？」に理由で答えていない（NTSB p.59 に理由の文あり）＝足す案（G5-013・任意・+40字） |
| ca20 | TSB §1.10.10.1 | ずれ | 98% は合う。21% は2021年8月5日の1回の潜航・1つの計器の値なのに「前の年の夏は」と広げている（G5-014） |
| ca21 | USCG p.289〈281〉・p.290〈282〉・NTSB p.59・p.73 | OK | 親の問い：USCG もはがれと言う（p.289 `It is likely that the loud bang … was the result of a sudden delamination`・p.290 `The initial delamination … likely occurred after surfacing`）。強さ「可能性が高い」は2冊の likely に合う（strongly suggests は傷みの方）。欄に USCG のはがれの片を足す案（G5-015・欄だけ） |
| ca22 | TSB §1.10.10.1・§2.1.1 | ずれ | 🔴 親の問いどおり：調べなかったのは会社（`OceanGate did not conduct a thorough inspection`）なのに、カナダの調べが調べなかったと聞こえる（G5-016） |
| ca23 | NTSB p.31・TSB §1.10.9 | OK | 30・50 は3代目の技術部長の話（NTSB）・TSB は reported の30〜50＝「とされ」でぼかしが残る。警報の音なし・潜航ごとにゼロ・海面では数えないも合う。「そう。」は前のまとめ（ca22 の聞き役）を受けている |
| ca24 | NTSB p.51・USCG p.282〈274〉・p.283〈275〉 | OK | `did not register acoustic events for any of the 2022 dives`（NTSB の字どおり）。`was reckless` は MBI の評価＝「と書く」で帰属あり |
| ca25 | NTSB p.31・p.64・p.65・USCG p.136〈128〉 | ずれ | 事実は NTSB で合うが、帰属が無く直前の米沿岸警備隊の続きに聞こえる（USCG は「ヒットの決め方は CEO が決めた」と別の面を書く）（G5-017）。「作り方の違う」は p.64 の片を欄に（G5-018） |
| ca26 | USCG p.290〈282〉・NTSB p.60 | ずれ | 「11か月」は NTSB `11 months later`（82回目→88回目）で合う。「赤信号」の主語は聞こえた音でなく、全センサーの大きな音の記録とひずみの曲がり（G5-019・軽い・任意） |
| cb01 | TSB §1.22・NTSB p.36・USCG p.236〈228〉 | OK | 駐車場（NTSB・USCG）・お金が無かった（TSB・帰属あり）で合う。「本社へ」＝Everett |
| cb02 | USCG p.236〈228〉・p.237〈229〉・NTSB p.35・USCG p.230〈222〉・p.231〈223〉 | ずれ | 覆いの話は USCG どおり（基地の担当者が「返事が無かった」と確かめた）。「前の冬は本社の町の屋内に」は NTSB だけ＝USCG は7か月の宣伝の巡回と書く（割れを帰属なしで片方）（G5-020） |
| cb03 | USCG p.236〈228〉・p.238〈230〉・TSB §1.22 | OK | 7月26日〜2月6日＝195日＝「半年あまり」（USCG の approximately 7 months を丸め直さず日付で言っている） |
| cb04 | TSB §1.22・§1.7 | ずれ | 親の問いどおり：「摂氏」は TSB の字に無い（°だけ）・「セントジョンズの冬は」は2022年12月〜2023年2月の値を冬一般に広げる（G5-021） |
| cb05 | NTSB p.60・TSB §2.1.3 | ずれ | 1行目は NTSB の if … could have を残していて OK。2行目は TSB も凍る水の話をしたように聞こえる（TSB は the elements まで）・「可能性までとする」が分かりにくい（G5-022） |
| cb06 | USCG p.328〈320〉 6.1.1.11.1・p.7〈vii〉 | OK | 結論は言い切り（`compromised the TITAN’s hull integrity.`）＝「とまで書き」で帰属。主たる要因の8つ目＝整備も風雨からの保護もしなかったこと |
| cb07 | USCG p.238〈230〉・TSB §1.23・§1.22 | OK | 証言の主＝最後の技術部長（2021〜2023年初め）＝「当時の技術部長」で合う。`we couldn't do that` ＝できなかった。後半の給料の後払いは TSB どおり（字数の削る候補＝G5-023・誤りではない） |
| cb08 | USCG p.84〈76〉・p.246〈238〉・TSB §1.23.1 | ずれ | 計画書の「未定」は合う。「席は空いたまま」だと、誰も見ていなかったように聞こえる（TSB は残った社員が受け持ち・正式に就いた人なし）（G5-024） |
| cb09 | TSB §1.20.2・§1.20.1.2・USCG p.246〈238〉 | ずれ | 上げ下ろしの設備が無い・台ごと引いた、は合う。免除の申し込みなし は TSB だけ＝帰属を付ける（G5-025） |
| cb10 | TSB §1.20.2.2・USCG p.294〈286〉・NTSB p.60・p.9 脚注1 | ずれ | 5,000キロ超＝2,900海里あまり×1.852 で合う（NTSB の miles も海里）。950時間は「引かれるか綱でつながれていた」時間（G5-026・軽い・任意） |
| cb11 | TSB §1.20.2.2・§2.1.3 | OK | `considerably higher accelerations than those recommended by DNV`＝業界の目安よりかなり大きな揺れ・`significant wave heights of up to 3.35 m` で合う（出どころは TSB が頼んだ曳航の調べ＝帰属は cb13 で出る） |
| cb12 | TSB §1.21.1（2つ目）・NTSB p.38 図10 凡例 | ずれ | 5月24日と2回は TSB どおり（NTSB は5月23日＝割れ）。2回目の「沈んでいる」に「半ば」が無い・聞き役の言い方（§0-1-12）（G5-027）。画の NTSB 図10 は5月20日と27日の写真＝5月24日の場面ではない（G5-028） |
| cb13 | USCG p.294〈286〉〜p.295〈287〉・NTSB p.60・TSB §1.20.2.2・§2.1.3 | ずれ | 🔴 TSB の `not likely a contributing factor` を「原因にならない」と言い切る（強め）。「米沿岸警備隊は、さらに弱った可能性が高い」は主語と動詞が抜ける（G5-029）。USCG の likely＝可能性が高い は合う |
| cb14 | TSB 付録B（2023年4行）・§1.21.4・NTSB p.14・USCG p.256〈248〉 | ずれ | 語りは合う（3回・10m・台から離れず）。85・86回目が台を離れなかった片が欄に無い（G5-030・欄だけ） |
| cb15 | USCG p.295〈287〉・NTSB p.37（カードの片） | ずれ | 45分・点検の形跡なし は USCG どおり。親の問い：どの潜航か＝87回目（USCG・NTSB 6月12日／TSB 6月13日）。「6月の3回目」は6月の中の3回目に聞こえる（6月は2回だけ）・「台の操作」は浮き沈みの水の調整（G5-031） |
| cb16 | USCG p.139〈131〉・TSB §1.10.9・NTSB p.51 | OK | 3冊とも2023年の記録なし＝「残っていない」で合う（「記録していなかった」と言っていない） |
| cb17 | TSB §1.17.12.1・USCG p.25〈17〉・p.78〈70〉・p.80〈72〉 | ずれ | 35・48 は TSB どおり（35 は USCG にもある）。親の問いどおり「ストライク」が中学生に通じない・35 との関係が言われない（G5-032） |
| cb18 | NTSB p.60・p.73・p.51 | ずれ | 所見2 の中身は合う（出どころ不明・タイタニックの深さに耐えられない）。「2022年の最後の深い潜航」は83回目（2,954m）にも聞こえる＝82回目は7月22日（G5-033） |
| cb19 | USCG p.295〈287〉・p.311〈303〉・TSB §1.21.1（2つ目）・NTSB p.16 | ずれ | 「この年初めて台を離れ」は USCG の書き方＝TSB は5月22日の無人の潜航で台から離したと書く（割れ）→「人が乗って初めて」。聞き役「確かめないまま」は USCG の「十分に点検された見込みは低い」より強い（G5-034・G5-035） |

- 判定の数：OK 18・ずれ 26・要確認 1（全45カット）
- 親の気になった所への答え（まとめ）：ca03＝USCG 4.34.8（OK・帰属は足す）／ca04＝OK／ca05＝要確認（画像）／ca14＝NTSB p.51・USCG p.235（欄に足す）／ca21＝USCG もはがれ・強さ OK／ca22＝🔴 主語は会社／cb04＝「摂氏」を外し期間を言う／cb13＝🔴 USCG の likely は合うが TSB の not likely を言い切っている／cb15＝87回目・「6月の3回目」は言い換え／cb17＝意味を足す案／ca02・cb12 の聞き役＝ca02 は可・cb12 は言い換え案

## 親へ

1. **画像でしか決まらない**：ca05 の線の図（NTSB 図19 の深さの線が0に戻る時刻）と ca07・ca08 の音の山（15:26:45）の並び。語りは「浮上の終わり、海面の近く」で3冊を包むが、図で山が「海面に着いた後」に見えると、USCG の凡例（まだ水の中）と食い違って見える＝音の印を水の中に置かない・時刻の札の並びを画像で確かめる（G5-005）
2. **画像・映像方針**：cb12 の NTSB 図10 は5月20日・27日の台の傾きの写真＝5月24日の語りの横に置かない（cb11 へ移す案・G5-028）。cb07 の MBI 図109 は c305 の図5 と同じ場面の別の写真＝カード（g5 §3 末尾）は「1点1カット＝1回だけ」と書く＝映像方針で同じ場面を2回出してよいかを決める。cb07・cb11 の写真（岸壁の台・注水弁）は語り（技術部長の証言・引かれた揺れ）と中身が離れている＝映像方針で
3. **字数の幅（±40）**：全部採ると第9章 +92・第10章 +43。任意＝G5-013（ca19 の理由の一文 +40）・G5-019（ca26 +11）・G5-026（cb10 +6）。削る候補＝G5-023（cb07 の後半 −41）・cb02 の3行目（−22）・ca15（81回目の操作の逆＝補助の事実・語り52字）。G5-013 を採るなら ca15 を外すのが釣り合う
4. **台本の割れの表（§1-5）に足す候補**：5月の台が半ば沈んだ日（USCG・TSB 5月24日／NTSB 5月23日）・回数（TSB だけ2回）／2021年の遠征のあとの冬（NTSB＝本社の屋内／USCG＝7か月の宣伝の巡回）／84回目が台を離れたか（TSB＝離した／USCG＝88回目が初めて）／83回目の日（NTSB p.51 7月23日・p.60 7月25日）
5. **cb04 の画の札**：「−0.5℃・−5.5℃」の℃は推測（TSB は°だけ）。札を TSB の字どおりにするか、℃のまま「カナダの調べの値」と添えるかを決める（G5-021）
6. **cb13 の図の3つ目**：米運輸安全委の「影響は分からない」（NTSB p.60 `their actual effects are unknown.`）は語りに無い＝「見方が分かれる」と言う以上、語りにも足すかを決める（足すと +20字前後）
7. **ウェブが要る所**：無し（この担当の章で、3冊の外の事実は使っていない）
