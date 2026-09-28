# R2 当て直し（第1版→第2版の対照）　2026-09-26

- 担当範囲：`diff_v1_v2.md` の「## 第6章」〜「## 第9章」の変わったカット **68**（第6章 20・第7章 20・第8章 15・第9章 13）＋「## 節の差し替え」**58 ブロック**（G1 3・G2 2・G3 1・G4 3・G5 3・G6 5・Z 41）
- 原文は `kwic.py -f q_R2.txt` で引いた（1回目＝第6〜9章の直した行 80件・2回目＝Z の §1-8 に足した行 11件）。報道・主催の団体の頁（RARA）は照合していない
- 形の機械検査（scratchpad `len_r2.py`・`daihon_v2.md` の c601〜c920）＝1行40字・文40字・聞き役20字・★20字・1カット3行・★が最後の行＝**違反0**
- 聞き役（roles_G4〜G6.tsv）と本文の `> Q: ` は28行とも一致。まとめ6つ（c609・c612・c717・c820・c911・c919）の次の語りは全部「そう。」。犠牲者の場面（c801〜c808）は質問2つ（c802・c805）だけ
- 指摘：🔴2・⚠️3・・9（うち節 4）

## 第6章（20）
c601｜・｜「事故機の基地は、オカラ」を事実のように言う。p35 は運用の制限が定めた基地、p49 注47 は actually based in Minden＝c605「機体があったネバダ」とぶつかる。「決められた基地は」（+1）（AAB p35・p49 注47）
c603｜OK｜p49「not been based in Ocala … since April 2007」「moved to Nevada in 2009」（AAB p49）
c605｜OK｜Q を外して「でも、」で c604 を受ける。届け先の意味は注47 どおり（AAB p36・p49 注47）
c606｜OK｜「3 hours of flight time and three takeoffs and landings」（AAB p36）
c607｜OK｜「a few test flights … on September 21 and 22」「each flight lasted 15 to 20 minutes」（AAB p36）
c608｜OK｜約23分＝データの長さ・5回のうち2回ぶん（AAB p36 注40・p49）。質問に次の行が答える
c609｜OK｜「If it is assumed … 1 hour 40 minutes」「no evidence」＝まとめ→c610「そう。」（AAB p49・p50）
c611｜🔴｜かぎ括弧の引用で throughout its normal range を「ふだんの速さ」に狭めた（第1版の「どこでも」から後退）。同じ 91.319(b) の言葉の c613「使う速さ…の全部」との対が切れる（AAB p15・p35・p50）
c612｜OK｜約23分の3回目を消した。まとめ→「そう。」
c613｜OK｜「under the unique load factor regime」＝「Gまで」（AAB p50）
c614｜OK｜no record・likely would have required＝「記録は無い」「おそらく」（AAB p50）
c615｜OK｜「a provision for the RARA to add an aircraft」（AAB p36）
c616｜OK｜注41「average ground speed around the course」・p38「lowest heat」「cancelled due to wind」。ゴールドは c214 で説明ずみ（AAB p36 注41・p38）
c617｜OK｜「主催の団体」に1本化（AAB p37）
c618｜OK｜G0 が Q を移した＝c619 の頭が答える（AAB p37）
c619｜・｜It is possible・should have been reported・should not have been eligible は残った。ただ p50 の「前に yes で登録したから」は 2010年の書類だけの話で、Q は2010年と2011年の両方を問う（AAB p50・p51）
c620｜・｜「パイロットの書類」＝c617・c618 の「参加の書類」と同じ物を別の名前で呼ぶ。「パイロットの参加の書類」（+3）（AAB p12・p51）
c621｜OK｜注7「the 2011 entry form accurately listed his age」（AAB p12 注7）
c622｜OK｜「about 200 flight hours in it since the previous year」「about 25 total hours」（AAB p51）
c624｜OK｜c623 の言い直しを消した（AAB p51）

## 第7章（20）
c701｜OK｜「NAG Unlimited Division technical inspection」・「4 days before」（AAB p37・p41）
c703｜OK｜「not having enough threads protruding」「properly positioning … cross-threaded」（AAB p37）
c705｜OK｜注42「consistent with previous cross-threading」＝「とみられる傷」（AAB p37 注42）
c707｜OK｜「All of the intact … screws were loose」（AAB p31）
c708｜🔴｜画の欄：#40 図73・図74 の右の画は FTIR の試料を削った跡の詰め物で、#40 p32 は「similar to the fibrous texture … in Figure 73」＝似て見える。札「事故機／新品」で差を見せる組み方は原文と逆。報告書が p31「(see figure 14)」で指す AAB 図14（p32）が本来の比べ（#40 p32・p59・p60・AAB p31・p32）
c709｜OK｜「consistent with relative motion due to the loose screws」・p40「In-flight movement … evident」（AAB p31・p40）
c710｜OK｜「yellow paint beneath the uppermost coat」「painted yellow before the 1985 NCAR」。Q「古さは」は c708 の「年月」を受ける（AAB p31・p41）
c713｜OK｜反応「短すぎたんだ…。」＝c712 の flush を受ける。数・非難なし（AAB p31・p32）
c714｜OK｜「corrosion … indicated … prolonged time」＝「とみられる」（AAB p39）
c715｜OK｜「板の震え、『フラッター』」（AAB p40）
c716｜OK｜「rapid periodic motion」「annoying “buzz”」（AAB p40）
c717｜OK｜まとめ→c718「そう。」（AAB p40）
c718｜OK｜「would not have been sufficient」「Flutter would be capable」＝「とみる」「うる」（AAB p40）
c720｜OK｜「likely tightened 4 days before」「only three flights (including …)」＋p31 loose（AAB p41・p31）
c721｜・｜受け身と free-play は直った。ただ「トリムの板」は4つ目の呼び名（板・尾翼の板・トリムタブ）。trim control tabs はどの板か限らない＝意図した言い方なので直さない（AAB p16）
c722｜OK｜「likely needed to be tightened several times」＝「必要があったとみられ」（AAB p41）
c723｜OK｜推定原因の噛み砕きは札（AAB p52）
c724｜OK｜「failure of the left trim tab link assembly, elevator movement, high flight loads, and a loss of control」（AAB p52）
c725｜OK｜「the pilot’s operation … without adequate flight testing」（AAB p52）
c726｜OK｜出典欄だけ（AAB p20「Within 62 minutes」）

## 第8章（15）
c801｜OK｜画の欄だけ（13:19 は推定＝分を書かない）
c803｜OK｜注4 の理由2つ＝「など」・勧告書 p1「based on preliminary information, 66」＞16＝「もっと多い」（AAB p10 注4・p6001）。呼び名は c820 の指摘へ
c805｜OK｜「First responder vehicles … remained on the outer perimeter」「all critical patients … en route」（AAB p20）
c806｜OK｜「immediate proximity of the accident site」（AAB p20）
c809｜OK｜「representatives of the RARA, FAA, …」（AAB p21）
c812｜OK｜反応→「this decision was put into practice」（AAB p21）
c813｜OK｜「many of the same local agencies」（AAB p21）
c814｜OK｜出典欄だけ（#33 p14「not damaged by debris」＝p2014）
c815｜OK｜★「燃料車は」18字・could easily（AAB p46）
c816｜OK｜「was not a factor」「would help mitigate risk … less serious accident」（AAB p46）
c817｜OK｜「provided in two documents: FAA Order 8900.1 … and Advisory Circular」（AAB p17）
c818｜OK｜「between the primary spectator area and the showline」（AAB p17）
c820｜⚠️｜比べは勧告書 p3 どおり。ただ「勧告書」の語が c903 の説明より前に出る（c803 は同じ理由で避けた＝G7-53）うえ、同じ A-12-08 を c803 は「報告書より前の、NTSBの書面」と呼ぶ＝2つの名前。「NTSBによれば、」（−4）（勧告書 A-12-08 p3＝p6003）
c821｜・｜語りは NTSB に直ったが、画の欄の札が「報告書が求めたこと」のまま（A-12-08 は 2012-04＝報告書より前）（AAB p46・p2）
c822｜OK｜「閉じる」→「片づく」

## 第9章（13）
c902｜OK｜画の欄だけ（p1 の上だけ）
c903｜OK｜CAROL の分類に Closed - Unacceptable Action もある＝「区切りがつくと」（CAROL p5008）
c905｜OK｜反応＝c904 の北へ・約2.4キロを受ける
c909｜OK｜「flutter characteristics」（AAB p43）
c910｜⚠️｜「事故の3か月後」を足した代わりに「レース機の」を落とし、「持ち主が」＝すべての持ち主に広がった。原文は exhibition and air racing の実験機・airplanes like the accident airplane。「レース機は」（+1・40字）（AAB p50）
c911｜OK｜まとめの数の語が消えた・→c912「そう。」
c912｜OK｜距離だけの勧告でない（勧告書 p6003「Another discrepancy」）
c913｜OK｜3回とも FAA の手紙のあと OPEN—ACCEPTABLE RESPONSE・「published revised Order … updated standards」（CAROL p5008）
c915｜OK｜「prohibits the use of mandatory language in an AC. Due to this new regulation」（CAROL p5008）
c917｜OK｜「the 2012 NCAR event」（CAROL p5013）。RARA は照合外
c918｜⚠️｜1行目（3つの答え）と2行目（手がかり3つ）がつなぎ無しで並び、3行目「どれも事故の前に…あった手がかり」が1行目の「先に折れたリンク」（事故の最中）まで含むように聞こえる。「この3つは、」（+3）。問い③「足りていたか」の答えが名詞「食い違った2つの資料」なのも噛み合いが弱い（AAB p41・p52・p6003）
c919｜OK｜「opportunities to identify and replace the deteriorated hardware」（AAB p41）
c920｜OK｜§B3-7＝責める相手を作らない問い

## 節の差し替え（58）
- G1〜G3（6）｜OK｜表の数・「報告書では」
- G4（3）｜OK｜#10 ★と意味の照合（AAB p50・p51）
- G5（3）｜OK｜章名「26年以上とみられるナット」＝likely・at least（AAB p41）
- G6（5）｜OK｜#15 ★（AAB p46）・表の数
- Z §1-8（足した行）｜OK｜p14 鉄の棒・#17 p3 1970年・#17 p4 July 1983・p43 inertia・p15 注13・p42 likely・p41 aileron・#33 p9 注4（p2009）・p16 waiver・p10 10 minutes を引いて一致
- Z §2 #9（c611）｜・｜c611 の指摘を採るなら、引いた訳と「normal range（範囲）は訳で落とした」を直す
- Z §6-1「3回・わずか3回…」｜・｜G0 が c720 から「わずか」を外した＝古い語が残る
- Z §6-1「3日前・4日前」｜・｜`c624`「事故の4日前」が抜けている（第1版から）
- Z §7「§5 #40 材料試験」｜・｜c708 の指摘を採るなら、`c708` の図を AAB 図14 に
- ほかの Z（§1-1・§1-3・§1-4・§1-5・§1-6・§1-9・§1-11・§3・§4・§5・§6-2・§8・§9・§10）｜OK｜第2版の本文と食い違いなし
