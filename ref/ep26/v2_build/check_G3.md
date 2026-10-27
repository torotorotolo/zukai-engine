# ④' 原文照合の係 G3（26本目・2026-10-27・Workflow の返りを wfx26.py が書き出した）

- 当てた頁＝G1 p.56・57・58・59・60／G2 p.3（OCR）・9・10・13・14・15／G7 p.738・740（723 も検索で通過）／T1（書き起こし・WebFetch）Day 7 Q6670〜6959（カリフォルニアン号の船長）・Q7412〜7610（見習い）・Q7803〜8110（二等航海士）／Day 8 Q8111〜8300（三等航海士）／Day 28 Q25353〜25462（カルパチア号の船長）
- 所見＝[findings_G3.json](findings_G3.json)（20件）

# G3 第5章 カリフォルニアン号の甲板で（c601〜c641・565〜743行）原文照合の記録

## 当てた頁
- G1（英国の審問の報告）p.56・p.57・p.58・p.59・p.60（pg26 page で全文）
- G2（MAIB）p.3（OCR＝調査官・次長の位置）・p.9〜10（海の流れ）・p.13（低い信号弾）・p.14（会社の信号）・p.15（争いの無い事実）
- G7（米国の公聴会の印刷）p.738・p.740（通信士が寝た時刻・起こした人）
- T1（書き起こし・WebFetch・保存なし）Day 7＝船長 Q6670〜6959・見習い Q7412〜7610・二等航海士 Q7803〜8110／Day 8＝三等航海士 Q8111〜8300／Day 28＝カルパチア号の船長 Q25353〜25462
- 字の数え＝scratchpad の `wf26c/G3/cnt.py`（章の合計 2,327字＝§0 の値と一致）・`d.py`（直し案の delta と行の長さ）。41字をこえる行は0

## ④ の直しの確かめ（先に当てた所）
| カット | 判定 | 一言 |
|---|---|---|
| c603 | ✓（・ G3-008） | 「とされる」で `is said` を受けた。「星の」は狭めすぎ |
| c604 | ✓（・ G3-009） | 「当時…沈んだとされた位置」✓・19×1.852＝35.2km ✓ |
| c612 | ✓ | 「三等航海士の話では」＝同じカットに帰属 |
| c623 聞き役 | ✓ | まとめ＝語りの言い直し・数字なし・c624「そう。」 |
| c624 | ✓ | G2 p.15 は「争いが無い」とする事実（`Nor is there any dispute`） |
| c625 画の欄 | ✓ | 3発＝p.58 `three more white rockets` |
| c627 聞き役 | ✓ | 数字なし・c628「そう。」 |
| c633 | ✓ | 「二等航海士の話では」が2時40分と色の問いの両方にかかる |
| c637 | ✓（⚠️ G3-004 は画の欄） | 11時半（G1 p.57）・一等航海士（G7 p.740 `The chief officer`）。NY の時刻を出さない＝時計の混ぜなし |

## 全行
| カット | 語りの行の頭10字 | 当てた資料と頁 | 判定 | 一言 |
|---|---|---|---|---|
| c601 | Q: カリフォルニアン号で | 役割＝質問 | ✓ | 答えは c602 から（c601 は時計の宣言）＝章の頭の引きは c520 から続く |
| c601 | ここからは、カリフォ | G1 p.56 `Mr. Stanley Lord, master` | ✓ | 時計の宣言・船長の名前の初出 |
| c602 | 夜10時20分ごろ、 | G1 p.56 `until 10.20`・`stop and reverse engines` | ✓ | 「ごろ」＝10:21／10:26 の幅 |
| c602 | 氷原は、北にも南にも | G1 p.56 `as far as could then be seen to the northward and southward` | ✓ | |
| c603 | 船長は、止まった位置 | G1 p.56 `fixed by dead reckoning` | ✓ | 推測航法をかみ砕いてある |
| c603 | 星の観測でも確かめた | G1 p.56 `verified by observations`・p.59 `stellar observations at 7.30 p. m.` | ・ G3-008 | 星の観測は夜7時半のもの |
| c604 | 報告書によれば、この | G1 p.56 `about 19 miles N. by E.` | ✓ | N. by E.→「北」は丸め（可） |
| c604 | 約35キロ（19マイ | 同 | ✓ | |
| c604 | 海の流れなどで、ずれ | G2 p.9・p.3 | ・ G3-009 | 出典の欄に片なし。MAIB の2人とも南向きの流れを認める＝案B に寄らない |
| c605 | 船は、朝の5時15分 | G1 p.56 `approximately stationary until 5.15` | ✓ | |
| c605 | 夜のあいだ、船首はゆ | G1 p.56 `swinging around to starboard` | ✓ | starboard＝右 |
| c606 | Q: 止まっていた夜に、何 | 質問 | ✓ | 次の行がそのまま答える |
| c606 | 夜11時ごろ、東の方 | G1 p.57 `At about 11 p. m.`…`from the eastward` | ✓ | |
| c607 | 船長は、甲板の灯りと | G1 p.57 `a few deck lights, and also her green side light` | ✓ | 主語が船長＝本人の話。三等航海士・見習いは赤（左舷）＝c618 で見習いの「赤」を帰属つきで言う |
| c607 | 左側が赤の灯りで、色 | 一般の説明 | ✓ | 舷灯の初出のかみ砕き |
| c607 | 緑の灯は、11時から | G1 p.57 `between 11 and 11.30`…`about 5 miles off` | ✓ | 5×1.852＝9.26km |
| c608 | 船長の見立てでは、そ | G1 p.57 `about 11.30 she stopped` | ✓ | 帰属あり（§0-1-4） |
| c608 | 大きさは、自分の船く | G1 p.57 `a medium-sized steamer, "something like ourselves."`・T1 Q6754 | ・ G3-019 | G1 だけで立つ（書き起こし不要）・言い直しの重なり |
| c609 | 当直の三等航海士、チ | G1 p.57 `officer of the first watch` | ✓ | 名前＋役職の初出 |
| c609 | マストの灯が2つ見え | G1 p.57 `two masthead lights`・`evidently a passenger steamer` | ✓ | |
| c610 | 機関室の乗組員も、真 | G1 p.57 `on deck at midnight` | ✓ | 役職だけ（名前なし） |
| c610 | 客船でしかありえない | G1 p.57 `could not have been anything but a passenger boat, she was too large` | ✓ | |
| c611 | 船長は言った。モール | G1 p.57・T1 Q6755〜6758 | ✓ | 三等航海士の証言だが、船長も認める＝争いなし |
| c612 | 三等航海士の話では、 | G1 p.57 `That does not look like a passenger steamer` | ✓ | |
| c612 | 三等航海士は答えた。 | G1 p.57 `It is, sir. When she stopped her lights seemed to go out` | ✓ | |
| c612 | Q: 船長と、当直の航海士 | まとめ | ✓ | 数字なし・言い直し・c613「そう。」 |
| c613 | そう。灯りが消えたの | G1 p.57 `went out at 11.40` | ✓ | 三等航海士の記憶。タイタニック号の 11:40 と並べていない |
| c613 | 真夜中からの当直を起 | G1 p.57 `one bell was struck to call the middle watch` | ✓ | |
| c614 | 三等航海士のモールス | G1 p.58 `appears to have been ineffectual`・T1 Q6758 | ⚠️ G3-005 | 「届いていない」＝原因の付け足し |
| c614 | 0時すぎ、当直は二等 | G1 p.58 `just after midnight` | ✓ | 名前＋役職の初出 |
| c615 | 三等航海士は、引き継 | G1 p.58 `she has been stopped since 11.40; she is a passenger steamer` | ・ G3-017 | c612〜c613 の言い直し |
| c615 | 止まったころ、灯りを | G1 p.58 `put her lights out` | ・ G3-017 | |
| c616 | 当直を終えた三等航海 | T1 Day 8 Q8289 `between 12.15 and 12.20` | ✓（・ G3-010） | 書き起こしで確認。出典の欄の Q と句の並びが逆 |
| c616 | ヘッドホンを当ててみ | T1 Q8283・Q8285 `Nothing at all` | ✓ | 「証言している」で帰属 |
| c617 | 船長は二等航海士に、 | G1 p.58 `instructions to tell him if her bearings altered`・T1 Q6769・Q6772 | ✓ | 二等航海士の話だが船長も同じ＝争いなし |
| c617 | 方位とは、自分の船か | — | ✓ | 専門語のかみ砕き |
| c618 | 二等航海士と当直に立 | G1 p.58 `an apprentice named Gibson` | ✓ | 名前＋役職 |
| c618 | 0時20分ごろ、その | G1 p.58 `at about 12.20 a. m.`・`glare of white lights on her afterdeck` | ✓ | 40字 |
| c619 | 見習いは一度、灯の瞬 | G1 p.58 `next thought it was a Morse light` | ✓ | |
| c619 | ただの瞬きだと考え直 | G1 p.58 `as he had first supposed, the masthead light flickering` | ✓ | |
| c620 | 0時30分すぎには、 | G1 p.58 `Sometime after 12.30 a. m.`…`saw two rockets` | ⚠️ G3-003 | 「2発見た」＝「発見」と読まれうる |
| c620 | そして1時10分ごろ | G1 p.58・p.59 `(not five white rockets)` | ⚠️ G3-002 | 争いのある方（二等航海士）を帰属なしで |
| c621 | Q: 伝声管って、何？ | 質問 | ✓ | 次の行が答える |
| c621 | 管を通して、声を別の | G1 p.59・T1 Q6784 `just below the upper bridge` | ✓（・ G3-011・G3-012） | 「船橋の下」は欄の片では立たない／画の欄「服のまま」未確認 |
| c622 | 船長は聞き返した。会 | G1 p.58 `Are they company's signals`・T1 Q6910 | ✓ | 船長も同じ問いを認める |
| c622 | 二等航海士は答えた。 | G1 p.58 `I do not know, but they appear to me to be white rockets` | ✓ | 船長の証言（Q6910＝分からないと言った）と矛盾なし |
| c623 | 会社の信号とは、船の | G2 p.14・T1 Q6937 | ✓ | |
| c623 | ホワイト・スター・ラ | T1 Day 28 Q25394 `the green flare, which is the White Star Company's night signal` | ✓（・ G3-020） | 書き起こしで確認 |
| c623 | Q: 会社ごとに、決まった | まとめ | ✓ | |
| c624 | そう。船長は言った。 | G1 p.58 `go on Morsing`・T1 Q6920〜6929 | ✓ | 船長も認める |
| c624 | 取った手は、モールス | G2 p.15 `no action was taken save to make further attempts to raise her with the morse lamp` | ✓ | MAIB が「争いが無い」とする |
| c625 | 見習いはモールス灯で | G1 p.58 `at once proceeded again to call the steamer up by Morse` | ✓ | 見習いの時刻 12:55 は語らない（§1-5） |
| c625 | さらに3発、白い信号 | G1 p.58 `three more white rockets; these rockets were also seen by Mr. Stone` | ✓ | |
| c625 | Q: 何発も、見ていたんだ | まとめ | ・ G3-016 | まとめ→「そう。」の3連続（c623・c625・c627） |
| c626 | そう。二等航海士によ | T1 Day 7 Q7921 `only about half the height of the steamer's masthead light` | ✓ | 書き起こしで確認・帰属あり |
| c626 | 低い光だった。この低 | G2 p.13 `described as low-lying` | ・ G3-013 | 「論点になる」の片が欄に無い |
| c627 | 1時から1時40分の | G1 p.58 `Between 1 o'clock and 1.40` | ✓ | 見習いは 1時〜1時20分（Q7515）＝報告書の幅で可 |
| c627 | 二等航海士は言った。 | G1 p.58 `she looks very queer out of water`・T1 Q7515 | ・ G3-006 | very→「なんだか」 |
| c627 | Q: 何かおかしい、と感じ | まとめ | ✓ | |
| c628 | そう。見習いによれば | G1 p.58 `He also is said by Gibson` | ✓ | |
| c628 | 船が、何もないのに、 | G1 p.58 `not going to fire rockets at sea for nothing` | ✓ | |
| c628 | 本人も、そう言ったか | G1 p.58 `may possibly have used that expression` | ✓ | may possibly→かもしれない |
| c629 | Q: 遭難の合図だって、分 | 質問 | 🔴 G3-001 | 問いは「その夜の光」・答えは一般の決まり |
| c629 | 二等航海士は、のちの | T1 Day 7 Q8033・Q8034・Q7993 | 🔴 G3-001 | Q8034「その夜は分かっていたか」→「No」が落ちる |
| c629 | 1発ずつ上がる信号弾 | 同 | 🔴 G3-001 | |
| c630 | 二等航海士が最後の信 | G1 p.58 `the last of the rockets fired at about 1.40` | ✓ | |
| c630 | その20分ほどあと、 | G1 p.58 `some 20 minutes more`・`be sure and wake him` | ✓ | |
| c630 | 全部で8発の白い信号 | G1 p.58〜59 `eight of these white lights like white rockets`・`disappearing in the southwest` | ・ G3-015・G3-018 | 含みが落ちる・c633 と南西が重なる |
| c631 | Q: 船長は、起きていたの | 質問 | ✓ | |
| c631 | 見習いは、起きていた | G1 p.59 `the master was awake`・T1 Q7560・Q7570 | ✓ | 帰属あり |
| c631 | 2時5分。操舵室の時 | T1 Q7565 `Five minutes past two by the wheelhouse clock` | ✓ | 時計の札あり |
| c632 | 2人は、その船が見え | G1 p.59 `until she disappeared` | ✓ | |
| c632 | 灯りが少しずつ消えて | G1 p.59 `would be perfectly natural with a ship steaming away from us` | ✓ | would→「なら」 |
| c633 | 二等航海士の話では、 | G1 p.59 `At about 2.40 a. m.`・`SW. ½ W.` | ✓ | |
| c633 | 船長は、灯りに色は無 | G1 p.59 `just white rockets` | ✓ | |
| c634 | ところが、船長の記憶 | G1 p.59 `at about 1.15` | ✓ | 並べは同じ船の時計＝混ぜなし |
| c634 | 白い信号弾が1発、と | G1 p.59 `(not five white rockets)` | ✓ | |
| c635 | 1時半から4時半まで | G1 p.59 `between 1.30 and 4.30` | ✓ | 主語は行2の「と船長は言う」 |
| c635 | 見習いが海図室の戸を | G1 p.59 `remembered Gibson opening and closing the chart-room door` | ✓ | T1 Q7288 は出典の欄だけ（語りに使っていない） |
| c636 | Q: 伝えた人と、聞いた船 | まとめ | ✓ | |
| c636 | そう。英国の報告書も | G1 p.60 `contradictions and inconsistencies` | ✓ | |
| c637 | カリフォルニアン号の | 画の欄の帯 | ⚠️ G3-004 | 帯の「1:10ごろ 5発」に帰属なし |
| c637 | 通信士は、11時半に | G1 p.57 `turned in at 11.30 p. m.`・G7 p.740 `The chief officer` | ✓（・ G3-007） | |
| c638 | 4時、一等航海士のス | G1 p.59 `relieved Mr. Stone at 4 a. m.` | ・ G3-007 | 名前が2回目に出る |
| c638 | 4時半、船長を起こし | G1 p.59 `Yes, I know; he has been telling me` | ・ G3-014 | 後半が落ちる |
| c639 | 船橋に来た船長は、新 | G1 p.59 `apparently took the fresh steamer` | ✓ | apparently→らしい |
| c639 | 大丈夫そうだ。いまは | G1 p.59 `This mistake was not corrected` | ✓ | 帰属は c640 頭「報告書はそうみる」（聞き役を挟んで届く＝可） |
| c639 | Q: えっ、別の船と取り違 | 反応 | ✓ | |
| c640 | 報告書はそうみる。通 | G1 p.59 `had the wireless operator called` | ✓ | |
| c640 | ヴァージニアン号から | G1 p.59 `At about 6 a. m.` | ✓ | |
| c640 | 客はボート、船は沈み | G1 p.59 `at full speed` | ✓ | |
| c641 | だがタイタニック号は | G1 p.60 `At 2.20 a. m. the Titanic had foundered` | ✓ | 「何時間も前」＝時計の差に左右されない |
| c641 | ここで時計を、タイタ | — | ✓ | |

## 字
- 足す：G3-001 +13・G3-014 +5・G3-015 +4＝+22
- 直しで減る：G3-005 −1・G3-007 −1・G3-008 −2
- 削る候補（type 削る）：G3-016 −12・G3-017 −12・G3-018 −12・G3-019 −7・G3-020 −7＝**−50**
- 全部入れると第5章は −32（2,327→2,295）

## 親へ

親へ（画像）：c601・c605・c608・c612・c614・c616 の副題（年・撮った人・どの船か）は画像と materials.md で確かめてください。c625 の3発、c634 の並べ、c637 の帯の札（G3-004）は ⑤ で見てください。
読み：「船橋」は全編で15回出ます（c612・c621・c639 ほか）。ゆっくりの声で「ふなばし」と読まれるおそれがあるので、章ごとの所見にせず、③で全編まとめて確かめてください。
§0-1-6（書き起こしだけで立つ語り）：c608 は G1 p.57 だけで立ちます（T1 は不要）。c616・c623・c626・c631 は書き起こしの句と問の番号を確かめました（c616 は番号の並びが逆＝G3-010）。語りは「証言している」「によれば」で証人に帰属しているので、画面の「書き起こしで確認」で足りる、というのが私の判断です。中身が崩れていたのは c629 だけでした（G3-001）。
自信の無い判断：G3-001 を🔴にしました。行そのものは正しいのですが、問いとの組で証言と逆の意味に聞こえるためです。G3-005 は「ようだった」で弱めてあるので⚠️にとどめました。
§0-1-4：c608・c612・c622・c631・c633〜c636 は、どれもカットの中で帰属を言っているか、船長も同じことを認めています（T1 Q6755・Q6772・Q6910・Q6920）。抜けていたのは c620 と c637 の帯です。
開けなかった資料：ありません。c621 の「服のまま」は見つけられませんでした。
字：足す +22、削る候補 −50、直しで −4。全部入れると第5章は −32 です。
