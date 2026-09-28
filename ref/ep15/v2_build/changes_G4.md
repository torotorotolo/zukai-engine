# G4 直した記録（第6章 c601〜c624）

原文は全部 `kwic.py` で引き直した（問いのファイル `q_G4.txt`＝20件）。差し替えたカット 19（c601・c603・c605〜c609・c611〜c617・c619〜c622・c624）／節の差し替え 3。

## 直した
- G4-01 c619 聞き役のまとめ「つまり、改造は無いと答えた？」→ 質問「どうして「いいえ」？」。語りを「前の年に「はい」で出したからかもしれない、と報告書はみる。」「でも、その年は走っていない。だから2010年も「はい」とすべきだった、とする。」に（c619 は正味 +31字＝第6章の削りで賄った）。AAB p50「It is possible that the pilot circled “no” on the 2010 form because he had previously registered the airplane with “yes” circled. However, because the airplane never raced in the 2009 NCAR, its major alterations should have been reported in 2010」・p37「since the airplane last raced at the NCAR」で確かめた。所見の案は「2010年の書類に書くべきだった」だったが、なぜ「いいえ」が違うのか（2009年は走っていない＝問いの「前に出たあと」の起点が改造の前）を耳で追えるように「その年は走っていない」を足し、「書く」の目的語が浮かないよう「「はい」とすべきだった」にした。「届ける」（FAA への届け）の語はここから消えた。roles_G4.tsv も まとめ→質問
- G4-02 c619 ★「2010年と11年は、出走資格が無いはず」→「2010年と11年は、本来資格が無かった」（20字・+1）。AAB p51「should not have been eligible to race the airplane in the 2010 or 2011 NCAR」。§2 の表 #10 と意味の照合 #10 を v2_sect_G4 で直した
- G4-03 c608「テレメトリーに残っていた飛行は、合わせて約23分。」「ただ、つながりが悪く、記録は欠けていた。飛び立ったのは5回だった。」→「テレメトリーの記録は、2日で合わせて約23分。」「ただ、欠けていた。飛び立った5回のうち、記録は2回ぶん。」（−7字）。AAB p36 注40「five flights were initiated, but data were recorded for only two flights … about 19 minutes of data … the recording ended about 4 minutes into the airplane’s flight … about 4 minutes of data … could not be correlated to a flight」＝約23分はデータの長さ。「つながりが悪く」は整備の仲間の説明（the crew stated）なので外した。所見の案「ただ記録は欠けていた。」から「記録は」を落とした（1行に「記録」が3回になるため）。出典欄に p49（five flights were initiated）を足した
- G4-16 c612「そう。記録に残る飛行は約23分。それでも記録簿では「終えた」ことになっていた。」→「そう。記録簿では、「終えた」ことになっていた。」（−16字）。約23分の3回目と注40の問題の繰り返しを消した
- G4-04 c609 まとめ「つまり、決められた時間に届いていない？」→「つまり、時間が足りなかったかも？」（−3字）。AAB p49「there was no evidence that the airplane had accumulated 3 hours of flight time」・p50「If it is assumed that all five flights were completed and each lasted 20 minutes, that would represent only 1 hour 40 minutes」＝語りは「証拠は無い」で止まる。案の「届いていないかも？」（+2）より短い形にした。次の c610「そう。」はそのまま受ける
- G4-05 → 下の「一部だけ採った」
- G4-06 c614「…もっと重い試験を求めたはずとする。」→「報告書は、届けていれば、FAAはおそらく、もっと重い試験を求めたとする。」（−3字）。AAB p50「Had the FAA been notified, it likely would have required a more substantial flight testing program」。G4-14 と合わせて2行の順を入れ替えた（届けた記録の無い改造 → この行）
- G4-14 c614「空気の取り入れ口を外したことも、おもりも、右の板の固定も、届けられていなかった。」→「空気の取り入れ口も、おもりも、右の板の固定も、届けた記録は無い。」（−8字）。AAB p50「there was no record that any FSDO was ever notified of other major modifications, such as the lower air scoop removal, the elevator and rudder counterweight increases …」＝no record を残した。所見の案は「取り入れ口も」だが、第5章 c505 から間が空くので「空気の」は残した（+3）。取付角は言わないまま（§1-8 の表の直しは add_G4.md）
- G4-07 c605 2行目を「届け先は、機体があったネバダの、リノの事務所。」の別の行に。AAB p49 注47「because the airplane was actually based in Minden, Nevada, the pilot was correct in contacting the Reno FSDO」。出典欄に p49 注47 を足した
- G4-08 c616「その年の公式の最高速度は、時速約602キロ（325ノット）未満。」→「その年、レースの平均の速さは、最も速くても時速約602キロ（325ノット）未満。」（40字）。AAB p36「The maximum official race speed41 … was less than 325 knots」・注41「Official race speed is the average ground speed around the course」。出典欄に注41
- G4-17 c616「いちばん下の組の最後尾から勝ち上がったが、ゴールドのレースは風で中止になった。」→「いちばん下の組から勝ち上がったが、ゴールドは風で中止になった。」（−8字）。AAB p38「started in the last place in the lowest heat … won a series of races and qualified to run the unlimited class gold race in 2010, but that race was cancelled due to wind」
- G4-09 c620「書類には、…。この機体で飛んだ時間は「約2,700時間」。」（41字）を2行に：「パイロットの書類には、事実と合わない数字もあった。」「2011年は、この機体で飛んだ時間が「約2,700時間」。」。AAB p12「The pilot’s 2011 NCAR entry form … his time in the “entered race airplane” … as “2,700±” hours」・注7「On the 2009 and 2010 entry forms … “2,500+” hours and “2,500 hrs ±”」
- G4-22 c620 出典欄を「AAB p12・注7・p15 注15・p51」に
- G4-10 c622「2011年の書類には、前の年から約200時間飛んだとある。」→「2011年の書類には、この機体で前の年から約200時間飛んだとある。」（+5字）。AAB p51「reported that he had accumulated about 200 flight hours in it since the previous year」
- G4-12 c613「レースの速さと力まで」→「レースの速さとGまで」（±0）。AAB p50「had not been flown through its normal range of racing speeds under the unique load factor regime」。G は c104・c308 で説明ずみ
- G7-13 c613 同上（c613 の分。c216 は G1 が直した）
- G4-13 c624「報告書の言葉は「不正確」。理由は分からず、事故との関係も見つかっていない。」→「報告書の言葉は「不正確」。」（−24字）。c623 の言い直しで、主語が「不正確な情報」に広がる所を消した（AAB p51 で証拠が無いのは「年齢や経験が事故に関わったこと」）
- G7-47 c624 同上
- G4-15 c606「試験は、ミンデンで行ってよいとした。」を削った（−18字）。AAB p36「the Reno FSDO issued authorization for the pilot to conduct the tests in Minden, Nevada」＝筋に効かない
- G4-18 c603「アリゾナ、テキサスと移り、2009年からはネバダにあった。」→「2009年からは、ネバダにあった。」（−12字）。AAB p49「The airplane was in Arizona and later Texas before it was moved to Nevada in 2009」
- G4-19 c607「整備の仲間によると、21日と22日に数回飛び、1回は15分から20分だった。」→「整備の仲間の話では、その日と翌日に数回飛び、1回あたり15分から20分。」（−2字）。AAB p36「a few test flights were performed on September 21 and 22, 2009, and that each flight lasted 15 to 20 minutes」＝each を「1回あたり」。数を1つ減らした（G7-42）
- G4-23 §6 の読みの候補を add_G4.md に書いた（「最後尾」は第2版で消えたので外した・この版で足した語も足した）
- G7-40 c601「事故機はフロリダ州オカラの飛行場だった。」→「事故機の基地は、フロリダ州オカラの飛行場。」（+1字）。AAB p35「based and maintained at Leeward Air Ranch Airport, Ocala, Florida」
- G7-41 c605 の聞き役「Q: 届けたのは？」を外し、語りを「でも、記録にあるのは、2009年の冷却装置の1件だけ。」で始めた（decisions「c605 の Q 採る」・slots_G7 c605）。AAB p36「FAA records show that the pilot notified the Reno, Nevada, FSDO of a major change involving the boil-off cooling system installation in 2009」。roles_G4.tsv から消した。後半（リノの意味）は G4-07
- G7-45 誰の数か：c620 の1行目を「パイロットの書類には、」で始めた（c621 の年齢の欄・c622 もこの枠の中＝パイロットが書類に書いた数）。c622 に「この機体で」（G4-10）。AAB p12・注7・p51。所見の案の「パイロットが」を c620・c622 の両方に足す形（+12字）でなく、枠を1回立てる形（+6字）にした

## 不採用
- G4-11 c623 ★に主語を足す案＝不採用。decisions §0「★を替えるもの（§2 の表）以外の★の文は変えない」。誰の書類かは c620 の「パイロットの書類には」で立つ
- G4-20 c615 の決まりの使い方の判断（p50「should not have been eligible to enter the 2010 race」）を足す案＝所見自身が「直さなくてよい（字が要る）」。第6章は −30字以下
- G4-21 c601 の章の頭の引き＝任意・字（+4）。前の章の橋を受けている。c601 は G7-40 だけ直した
- G4-24 c613 の「安全」を c611 の言葉にそろえる案＝任意。c611（安全に運用できる）と c613（安全と示すまで）は「安全」で耳でつながる。「操縦できる」だけにすると no hazardous characteristics が落ちる
- G7-44 c616 を「事故の日の速さより、時速240キロ以上遅い」に替える案＝不採用。602キロは公式のレース速度＝コースを回る平均の対地速度（AAB p36 注41）、c216 の約848キロはパイロン6と7のあいだの真対気速度の最高（AAB p29）＝別の物差しで、引き算すると差が大きく見える（図は既定値で嘘をつく型）
- G7-46 c621 の年齢の行を削る案＝decisions のとおり不採用（年齢の食い違いは p51 が挙げた inaccurate の中身）。誰の数かは G7-45 で c620 の枠に入れた。2行目は「2011年は、正しく書かれていた。」に縮めた（−4字・AAB p12 注7「the 2011 entry form accurately listed his age」）
- G7-21（c614 の分）slots_G7 の c614 まとめ「つまり、試験が足りないまま？」＝不採用。字（+17＋c615 の「そう。」+3＝第6章の −30 を割る）と、c609・c612 のまとめのすぐ後で3つ目になるため。c612→c617 の空きは第1版で66秒（90秒以内）で、第2版は c613〜c616 を縮めたので短くなる
- G2-10（c620 の分）数は「約1,453時間」のまま＝G2 が c415 を「約1,453時間」のまま残したのでそろえた（AAB p15 注15 の 1,453.6 を切り捨て）。直すなら c415 と c620 を一緒に（④'へ・add_G4.md）

## 一部だけ採った
- G4-05 c611 を2行に割り「すべての動き」を入れた：「続けて、「ふだんの速さと、すべての動きで操縦できる。」「危ない特性は無く、安全に運用できる」。」（+5字）。AAB p15「controllable throughout its normal range of speeds and throughout all manevers [sic] to be executed, has no hazardous operating characteristics or design features, and is safe for operation」。所見の案の「速さの範囲と」は「速さと」にした（−3字）＝range の語は落とした。design features も第1版のまま言わない。sic の綴りは紙面（図 p15）に残るだけ
- G7-42 数の詰め込み：c606 のミンデン（G4-15）・c603 の州名（G4-18）・c607 の「21日と22日」→「その日と翌日」を削った。c607 の「2009年9月21日」は残した（c610 の「2009年9月22日」と対）。c616 の2行目・c621 は残した（G4-17・decisions）
- G7-43 c612 の語りを「そう。」だけにする案（−34字）は採らず、G4-16 の形（「そう。記録簿では、「終えた」ことになっていた。」）にした＝約23分の3回目は消したが、まとめの答えの語りは1文残す（「そう。」だけの行だとカットが空く）
- G7-48 呼び方の1本化：c615「主催者が加えられる」→「主催の団体が加えられる」、c617 の聞き役「主催者に出す書類は？」→「主催の団体に出す書類は？」（+2字）。AAB p36「a provision for the RARA to add an aircraft」・p37「The RARA is the overall organizer」。c615 は41字になったので「、という決まりを使った」→「決まりを使った」（−4字・c615 は正味 −2字）。c809（「主催者やFAA」）は G6 の担当・c701（無制限クラスの団体＝NAG で RARA とは別）は G5 の担当＝add_G4.md へ

## ⑤bで原寸
- c612 panel「約23分と「終えた」」＝語りから約23分が消えた（c608 で言う）。panel の文字が語りと食い違って見えないか（「記録は約23分」と「終えた」の対なら可）
- c605 panel「届けたのは冷却装置だけ」＝語りに「機体があったネバダの、リノの事務所」が入った。panel に届け先を書くなら「リノ（ネバダ）」で、オカラ（基地）の事務所と取り違えないか
- c608 図 p36＝本文の約23分と注40（5回・2回ぶん）が同じ頁に写っているか（注40 が写らないなら注の段を切り出す）

章の字数 第1版 1,509 → 第2版 1,472（正味 −37字）。行 54 → 56・聞き役 8 → 7（質問 4・まとめ 2・反応 1）
