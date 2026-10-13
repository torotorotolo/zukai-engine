# 旧版タイタン号の主張照合 係A（プロローグ〜第3章）2026-10-13

- 対象：`ref/ep22/src/old/old_script_224e259.md` のプロローグ・第1章・第2章・第3章（105カット）＋ `tools_cuts_pr.py`／`c1`／`c2`／`c3` の図の値
- 一次資料：USCG MBI 報告（`uscg_mbi_pages.txt`・2025-08-04）／NTSB MIR-25-36（`ntsb_mir2536_pages.txt`・2025-10-02）
- 出典の書き方：USCG は「PDF p.N〈印字 p.X〉」（印字＝PDF−8）。NTSB は PDF の頁だけ（印字の自動の読みが粗いため）
- 判定：一致／言いすぎ／ずれ／逆／見つからない／一次資料の外。「（軽）」＝直すのは1語程度
- ⚠️ 写真の中身は見ていない（文字の層だけ）。写真について書いた所は `old/ref_CREDITS.md` の記述による

## §1 集計

- 数え方：§3 の1行＝1主張。語り・見出し・図で同じ主張をくり返す所は1行にまとめた。問いだけの文（pr09 など）と、事実を含まない受けの文（c135 の後半など）は数えていない。集計は §3 の「判定」の列を機械で数えた値

| 判定 | 件数 | 内訳 |
|---|---|---|
| 一致 | 150 | うち27行は §4 の印つき（片方の報告書とは合うが、もう一方とは値が割れる） |
| 言いすぎ | 26 | うち（軽）15 |
| ずれ | 32 | うち（軽）11。名称「海難審判部」8行を含む |
| 逆 | 2 | c105（波）・c208（図の札） |
| 見つからない | 2 | c109（中からは開かない）・c118（ゲージの目盛り） |
| 一次資料の外 | 2 | pr03（2023年9月30日）・c128（報道の時計） |
| **計** | **214** | プロローグ35／第1章96／第2章45／第3章38。§4 の印つきは全体で31行 |

章ごと：プロローグ＝一致26・言いすぎ3・ずれ5・外1／第1章＝一致61・言いすぎ16・ずれ15・逆1・見つからない2・外1／第2章＝一致31・言いすぎ5・ずれ8・逆1／第3章＝一致32・言いすぎ2・ずれ4

**傾向**
- 旧版は時刻と深さを USCG、人数と経過の多くを NTSB から取り、断りなく混ぜた所で**順序や比べる相手**がずれた（c107〜c109・c115d・c123・c124）
- 図の注の出どころ「沿岸警備隊 **海難審判部** 報告書」は名称が誤り（8か所）。うち2か所（c208・c224）は中身も NTSB の記述だった
- 第2章・第3章はほぼ NTSB の筋どおりで、語りの誤りは少ない。ただし USCG のほうが詳しく書く所（縮尺模型の試験4回・亀裂の日付と大きさ・1号殻の格下げ）で2冊が割れる（§4）

## §2 重い順の上位15

1. **c114（語り）ずれ** — 「10:47:02、重り2つの電文が**届いた**」。02秒は潜水艇が**送った**時刻で、母船に届いたのは 10:47:26＝爆縮（09秒ごろ）の**後**（USCG PDF p.35〈27〉）。並びの意味が変わる。
2. **c115d（語り・見出し・副題・図）ずれ** — 「NTSB は同じ電文を3,363m、差は17m」。NTSB の3,363mは「重り2つ」の電文の深さで、USCG では同じ電文が3,341m＝差は**22m**。17mは別の送信（10:47:08 の位置）との差（NTSB PDF p.17／USCG p.35〈27〉）。
3. **c105（語り・図）逆** — 「波は穏やかだった」。USCG は到着時「波の高さ2〜3m」（PDF p.24〈16〉）。NTSB は事故時「2〜3フィート」（PDF p.53）で、2冊でも割れる。
4. **c208（図）逆** — 札「炭素繊維の強さ：強＝圧縮／弱＝引っ張り」が性質の事実に読める。USCG は「引っ張りで実績、深海の圧縮では実績が無く一般に劣る」（PDF p.274〈266〉）。注の出どころ「USCG」も誤りで、CEO の考えは NTSB p.25（元部長の証言）。
5. **c302（語り）ずれ** — 「タイタニックの3倍以上、深く**潜れる**計算」。13,200mは**壊れる**深さ（NTSB PDF p.25）。潜ってよい深さの目標は6,000m（p.24）＝約1.6倍。
6. **pr06（図）ずれ** — 音の山を15:21、ひずみの跳びを15:17と15:22の**2段**に描く。USCG は「15:17ごろ増え始め、15:26:45 に一瞬で跳ぶ（1回）」（PDF p.283〜286〈275〜278〉）。
7. **pr04（図）ずれ** — 「浮上している途中」の印を水深1,600mに置く。原文は「海面にかなり近い所」（USCG p.233〈225〉）／「浮上した後に傷んだ可能性が高い」（NTSB p.59）。
8. **c123（語り）ずれ** — 「7時10分、カナダから**ボストンへ引き継がれた**」。カナダ側は母船に「ボストンへ連絡を」と案内し、母船が自分で連絡した（USCG p.6〈vi〉・p.39〈31〉／NTSB p.18）。時刻も2冊で割れる（§4）。
9. **c112（語り・図）ずれ** — 「文字が届くまで15〜20秒」。USCG は「約15〜30秒」（PDF p.36〈28〉）。15〜20秒は2冊のどちらにも無い。
10. **c113a（語り・図）ずれ** — 毎分33mの電文は**母船が送った**もの（USCG p.33〈25〉）。図の「14分後＝460m」は USCG の深さの記録（9:23 に436m・9:31 に680m）と合わず、9:28 は約600m。
11. **c227（見出し）ずれ** — 「**外部の**技術者が警告」。原文は2017年に雇われた**社員**（元USCGの運航技術者）（NTSB PDF p.47）。
12. **c224（語り・見出し・図）言いすぎ** — 「沿岸警備隊にも船級協会にも『実験的』の区分は無い」。NTSB 脚注17の前半「船級協会には新技術を証明する道がある」と「旅客・貨物を運ぶ船について」の限定を切った（NTSB p.23）。注の「USCG」も帰属ずれ（USCG p.319〈311〉は米国の規則についてだけ）。
13. **c119（見出し・図）言いすぎ／ずれ** — 引用札が「緊急事態とは受け取っていない」を船長自身の受け止めの形にし、主語（オーシャンゲート）が落ちた。札は「事故後の聴聞」だが、USCG はこの言葉を**書面の回答**として引く（USCG p.38〈30〉）。見出し「母船と会社で受け止めが違った」は原文に無い。
14. **c124（見出し・図）ずれ／言いすぎ** — 図「18:55＝**最初の**通報」。USCG では船長が18:27に JRCC ハリファクスへ電話していた（途中で切れた・PDF p.39〈31〉）。見出し「外の誰も知らなかった」は原文（USCG は知らなかった）より広い。
15. **「海難審判部」（pr10・c115c・c119・c203・c207・c208・c224・c230 の図の札・注）ずれ（名称）** — 原文は Marine Board of Investigation＝海難調査委員会（USCG PDF p.1）。裁く所ではない。8か所まとめて直す。

次点：c132「船首のすぐそば」（NTSB は約500m／1,148ft・p.20）／c130 図「海底まで潜らせて壊れた」（NTSB は「海底を目指して」まで）／c118「母船の側は」（疑ったのは会社の担当・船長が知ったのは11:15）／c121「15時には出ているはずだった」（「手順どおりなら」が落ちた）／c107〜c109 の順序／pr05「船の中にいた人」（＝潜水艇の中）

## §3 全件の表

### プロローグ（pr01〜pr10）

| カット | 種類 | 旧版の主張（短く） | 判定 | 原文の抜き書き（英語25語まで） | 出典 | 直し方の当たり |
|---|---|---|---|---|---|---|
| pr01 | 語り | 2023年6月18日 午前10時47分 | 一致 | "at approximately 10:47 a.m. on June 18, 2023" | USCG PDF p.7〈vii〉／NTSB PDF p.9 | 「10時47分ごろ」でもよい |
| pr01 | 語り・見出し・図 | 北大西洋の水深3,346mで消えた（札「そのときの深さ 3,346 m」） | 一致（USCG）・§4 | "transmitted its final ping ... at a depth of 3,346.28 m (10,978 feet)" | USCG PDF p.35〈27〉／NTSB PDF p.17 は 3,363 m | 「最後に位置が届いた深さ」と言う。NTSB は 3,363m。写真（海底の残骸）は海底≈3,800mにあるので、見出しの深さと並べると残骸の深さに読める（CREDITS より） |
| pr01 | 図 | 札「最後の記録 10:47:08」 | 一致 | "At approximately 10:47:08 a.m., the TITAN transmitted its final ping" | USCG PDF p.35〈27〉 | — |
| pr01 | 副題 | 潜水艇タイタン 2023年6月18日 | 一致 | — | USCG PDF p.5〈v〉 | — |
| pr02 | 語り | 乗っていたのは5名。全員が亡くなった | 一致 | "All five persons on board the vessel died." | NTSB PDF p.9 | — |
| pr02 | 語り | 潜水艇は原型をとどめていなかった | 一致 | "the vessel imploded ... The Titan was a total loss" | NTSB PDF p.9 | — |
| pr02 | 見出し・図 | 操縦士1・案内役1・客3（札も同じ） | 一致 | "the OceanGate CEO as the Pilot, a TITANIC Content Expert, Mission Specialist #1, ... #3" | USCG PDF p.6〈vi〉／NTSB PDF p.15 | — |
| pr02 | 副題 | 88回目の潜航 | 一致（注） | "Dive 88 was the casualty dive." | NTSB PDF p.37 | 番号は1号殻・2号殻を通した「出かけた回」の通し番号（NTSB 脚注23・p.25）で、失敗・中止の回（86・87）も番号を持つ。「ダイブ88」が安全 |
| pr03 | 語り | 11か月前に前触れがあった | 一致 | "The first detectable indication of damage occurred at the end of dive 80" | NTSB PDF p.58 | — |
| pr03 | 見出し | 残ったのは、炭素繊維の破片だった | 言いすぎ | "debris field ... including the tail cone and both titanium domes" | NTSB PDF p.20 | 残骸は炭素繊維だけではない。「回収された炭素繊維の破片」など一部だと分かる形に |
| pr03 | 副題 | 2023年9月30日 回収された証拠 | 一次資料の外 | （2つの報告書に「2023年9月30日の回収」は無い） | — | 出どころは `ref_CREDITS.md` の写真説明。§5 |
| pr03 | 図 | 札「耐圧殻の材料 炭素繊維」 | 一致 | "an 8-foot long carbon fiber pressure hull glued to titanium end sections" | USCG PDF p.5〈v〉 | — |
| pr04 | 語り・見出し・副題 | 2022年7月15日、同じ潜水艇がタイタニックから浮上していた（80回目の潜航の帰り） | 一致 | "heard a “loud bang” as the Titan ascended after successfully reaching the Titanic wreckage" | NTSB PDF p.36／USCG PDF p.233〈225〉 | — |
| pr04 | 図 | 「浮上している途中」の印を水深1,600mに置く | ずれ | "fairly close to the surface, though still underwater, when there was a large bang" | USCG PDF p.233〈225〉／NTSB PDF p.59 "after it surfaced" | 印は海面のすぐ下に。1,600mは原文のどこにも無い |
| pr04 | 図 | タイタニックの深さ 3,840m | 一致・§4 | "the depth (3,840 meters (m); 12,598 feet) of the TITANIC" | USCG PDF p.13〈5〉／NTSB PDF p.10 は 3,880 m | — |
| pr05 | 語り | そのとき、大きな音がした | 一致 | "heard a “loud bang” as the Titan ascended" | NTSB PDF p.36 | — |
| pr05 | 語り | **船の中**にいた人も、海面の小さなボートにいた人も、同じ音を聞いた | ずれ（軽） | "the loud bang heard by the personnel inside the TITAN and by OceanGate support personnel in a small boat" | USCG PDF p.289〈281〉／NTSB PDF p.36 | この台本で「船」は母船。「潜水艇の中にいた人も」に。事実の部ではボートの乗組員が聞いたことは契約者の伝聞（USCG p.234〈226〉） |
| pr05 | 見出し・図 | 音は2か所で同時に聞こえた（注「同じときに」） | 一致 | 同上 | USCG PDF p.286〈278〉 | — |
| pr05 | 副題 | 船内の**客**と、海面のボートの乗組員 | ずれ（軽） | "with a pilot, a content expert, and two mission specialists aboard" | USCG PDF p.233〈225〉 | 中にいたのは客だけでなく4人全員（"heard by all personnel on the TITAN" p.290）。「潜水艇の中の4人」 |
| pr06 | 語り・見出し | 装置は、そのころの15分間に、音の急増とひずみの跳びを記録 | 一致 | "showed a burst of acoustic activity and a sudden jump in some of the strain gages between about 1515 and 1530" | NTSB PDF p.52 | — |
| pr06 | 副題 | リアルタイム監視装置 2022年7月15日 | 一致 | "Real Time Monitoring System (RTM)" | USCG PDF p.2 目次 | — |
| pr06 | 図 | 時間軸15:00〜15:45・帯15:15〜15:30「この15分」 | 一致 | 同上（時刻はニューファンドランド夏時間） | NTSB PDF p.52 | — |
| pr06 | 図 | 音の山を15:21、ひずみの跳びを15:17と15:22の**2段**に描く | ずれ | "These shifts in strain ... occurred in a fraction of a second and coincided with the large amplitude acoustic event on Dive 80 at 3:26:45 p.m." | USCG PDF p.286〈278〉（増え始め≈15:17・p.283〈275〉） | 音は15:17ごろから増え、山とひずみの跳び（1回・一瞬）は15:26:45 |
| pr07 | 語り | 船体が金属の受け台の中でずれた。そう説明された | 一致 | "staff and mission specialists were told the hull had shifted in its metal cradle" | NTSB PDF p.36／USCG PDF p.233〈225〉 "shift ... within its frame" | — |
| pr07 | 見出し・副題 | 会社は、異常とは扱わなかった／そのときの会社の説明 | 一致 | "directed that no further investigation or assessments were necessary" | USCG PDF p.290〈282〉 | — |
| pr07 | 図 | 札 who=オーシャンゲート・to=同乗した客と社員・when=7/15 浮上後 | 一致 | "upon inspection after we got on the ship, ... had just jumped in its carriage" | USCG PDF p.233〈225〉／NTSB PDF p.36 | — |
| pr08 | 語り・見出し | そのあと3回潜った | 一致 | "The Titan completed three additional dives following dive 80 (mission 4, dives 81-83)" | NTSB PDF p.36 | — |
| pr08 | 語り・図の注 | うち2回、タイタニックの深さへ**客を**運んだ | 言いすぎ（軽） | "reached 3,840 meters (12,598 feet) on dives 81 and 82" | NTSB PDF p.36／USCG PDF p.290〈282〉 | 81・82の各回に客が乗ったとは書かれていない（USCG は「後の潜航に客も乗った」とまとめて書くだけ） |
| pr08 | 副題・図 | ダイブ81・82・83 2022年7月／81=3,840m・82=3,840m・83=2,954m | 一致 | "2,954 meters (9,692 feet) on the final dive of the expedition" | NTSB PDF p.36／USCG PDF p.235〈227〉（81=7/19・最終=7/23） | — |
| pr09 | 副題・図 | 回収された耐圧殻の破断面／札「層に分かれて裂けている」 | 一致 | "identified two delaminations between the five 1-inch-thick layers" | NTSB PDF p.59／図14説明 p.42 | — |
| pr10 | 語り・副題 | 2025年に2つの最終報告書。事故から2年 | 一致 | "August 4, 2025" ／ "Report Date: October 2, 2025" | USCG PDF p.5〈v〉／NTSB PDF p.1・p.76 | — |
| pr10 | 図 | 「アメリカ沿岸警備隊 **海難審判部** 報告書 335ページ」 | ずれ（名称） | "Report of the Marine Board of Investigation" | USCG PDF p.1 | 「海難調査委員会（MBI）」。審判（裁く所）ではない。c115c・c119 の札も同じ |
| pr10 | 図 | 2025-08-04／MIR-25-36・87ページ・2025-10-02 | 一致 | 同上 | USCG PDF p.5／NTSB PDF p.1 | — |
| pr10 | 図 | 「2冊は違うところを見て、同じ場所に着いている」 | 一致（注） | — | USCG PDF p.7〈vii〉／NTSB PDF p.58 | 原因の大筋は同じだが、数（深さ・時刻・人数）は割れる所がある（§4） |
| pr10 | 図の注 | 「この動画の数値と時刻は、すべてこの2冊による」 | 言いすぎ | — | — | §5 のとおり報告書に無い数・日付がある（2023-09-30、15〜20秒 など） |

### 第1章 その日、10時47分（c101〜c135）

| カット | 種類 | 旧版の主張（短く） | 判定 | 原文の抜き書き（英語25語まで） | 出典 | 直し方の当たり |
|---|---|---|---|---|---|---|
| c101 | 語り・見出し・副題・図 | 2023年6月16日、セントジョンズから1隻の船が出た（略図） | 一致 | "began at 9:31 a.m. ... on June 16, 2023, when the POLAR PRINCE departed the port of St. John’s" | USCG PDF p.5〈v〉／NTSB PDF p.15 | — |
| c102 | 語り・見出し・副題 | ポーラープリンス、カナダ船籍、全長220フィート | 一致 | "chartered the 220-foot-long, Canadian-flagged vessel Polar Prince" | NTSB PDF p.14（p.85 は 220.4 ft） | — |
| c102 | 語り・図の注 | 後ろに潜水艇を載せる台を引いていた | 一致 | "The TITAN was secured atop the Launch and Recovery System (LARS) and was towed" | USCG PDF p.5〈v〉 | — |
| c102 | 図 | 220ft 対 22ft・「母船は潜水艇の10倍」 | 一致（計算） | — | NTSB PDF p.14・p.21 | — |
| c103 | 語り・見出し | 乗っていたのは42人 | 一致 | "There were 42 persons on board the Polar Prince" | NTSB PDF p.15／USCG PDF p.5〈v〉 | — |
| c103 | 語り | 乗組員17人・オーシャンゲートの関係者21人 | 一致（NTSB）・§4 | "21 OceanGate personnel, including the OceanGate chief executive officer (CEO), who also served as the Titan pilot" | NTSB PDF p.15／USCG PDF p.5〈v〉は "17 crew, 24 clients, and one non-designated person" | 内訳は NTSB による、と語りでも断る |
| c103 | 図 | 17・21・**「潜水艇に乗る側」4** | ずれ（軽） | 同上（CEO＝操縦士は21人の側に数えられている） | NTSB PDF p.15 | 潜ったのは5人。「客3＋案内役1」と書くか、CEOを分けて示す |
| c103 | 図の注 | 内訳はNTSB報告書による（USCGは別の分け方） | 一致 | — | — | 断りは良い |
| c104 | 語り・見出し・副題・図 | 料金を払った客3人、同乗する案内役1人、潜るのは5名 | 一致 | "3 individuals called “mission specialists” who had paid" ／ "1 Titanic expedition guide who would dive" | NTSB PDF p.15 | — |
| c105 | 語り・図 | 6月18日 午前5時15分、目的の海域に着いた（時計05:15） | 一致（USCG）・§4 | "On June 18, 2023, at 5:15 a.m., the POLAR PRINCE arrived in the vicinity of the TITANIC wreck site" | USCG PDF p.23〈15〉／NTSB PDF p.15 は "about 0400" | 2冊で時刻が割れることを断るか、USCG と明記 |
| c105 | 語り・図 | 風は南西から | 一致 | "SW winds 13-19 kts" | USCG PDF p.24〈16〉／NTSB PDF p.15 | — |
| c105 | 語り・図 | **波は穏やかだった**（札「波 穏やか」） | 逆 | "SW winds 13-19 kts with 2-3 m (6.9 to 9.8 feet) wave height" | USCG PDF p.24〈16〉（到着時の航海日誌）／NTSB PDF p.53 は事故時 "seas were 2–3 feet" | 到着時は波2〜3m（USCG）。§4。「穏やか」は削るか、出どころと時刻を言う |
| c106 | 語り・見出し・副題・図 | 午前5時30分、潜航前の打ち合わせ。操縦士はCEO本人 | 一致 | "About 0530, the mission director and the CEO—who was also the pilot for the dive—held a pre-dive brief" | NTSB PDF p.15／USCG PDF p.25〈17〉 | — |
| c107 | 語り・副題 | 午前8時30分、5名が乗り込んだ（前部ドームから） | 一致（USCG）・§4 | "At 8:30 a.m., the crew for Dive 88 were loaded into the TITAN and the forward dome was secured." | USCG PDF p.28〈20〉／NTSB PDF p.16 は乗り込み "About 0800"・ドーム閉め "About 0830" | — |
| c108 | 語り・図 | 全員が乗ると5分間の停止時間（図「乗り込み完了」から0〜5分） | 一致（NTSB）・§4（順序） | "Once aboard, all individuals involved ... conducted a 5-minute planned hold, known as a “stopski.”" | NTSB PDF p.16／USCG PDF p.29〈21〉は "approximately 8:57 a.m., prior to the submerging" | USCG ではドームを閉めた後・沈める直前 |
| c108 | 語り・見出し・副題 | 持ち場を確認する時間で、誰も口をきかない | 一致 | "reviewed their checklists ... and reflected on their responsibilities ... there was no talking" | NTSB PDF p.16 | — |
| c107〜c109 | 並び順 | 8:30 乗り込み → 停止5分 → ドームを閉める | ずれ（順序） | USCG：8:30 乗り込み＋ドーム固定 → 8:57 停止。NTSB：0800 乗り込み → 停止 → 0830 ドーム | USCG PDF p.28〜29〈20〜21〉／NTSB PDF p.16 | 2冊を混ぜたため、どちらの順序とも合わない。どちらか一方の順に |
| c109 | 語り・図 | 前のドームが18本のボルトで（外側から）閉じられた | 一致 | "The forward dome had 18 bolt holes ... closure, which was completed from the outside of the submersible." | USCG PDF p.122〈114〉／NTSB PDF p.16 | — |
| c109 | 語り・図 | 台に水が入れられ、潜水艇ごと海面下へ | 一致 | "Divers opened the LARS valves and began sinking the platform (with the Titan on it)" | NTSB PDF p.16 | — |
| c109 | 見出し | 外から締められ、**中からは開かない** | 見つからない（後半） | （「中から開けられない」の記述は2冊に無い） | USCG PDF p.122〈114〉は「外から閉める」まで | 後半は推論。§5。言うなら裏を取る |
| c110 | 語り・図 | 午前9時14分、台から切り離された（時計09:14） | 一致（USCG）・§4 | "At 9:14 a.m., according to the POLAR PRINCE Deck Logbook, the TITAN was disengaged from the LARS platform" | USCG PDF p.30〈22〉／NTSB PDF p.16 は "About 0900" | — |
| c110 | 語り・見出し・副題・図 | 動力でなく、重りの重さで落ちていく | 一致 | "The descent was a free fall through the water column, controlled by the vessel's ballast condition." | USCG PDF p.6〈vi〉 | — |
| c111 | 語り・見出し・副題・図 | 予定およそ8時間（2.5＋3＋2.5） | 一致 | "about 8 hours (2.5 hours to descend, 3 hours to explore the wreck, and 2.5 hours to ascend)" | NTSB PDF p.16〜17 | — |
| c112 | 語り・図 | 海の中では電波が**届かない** | 言いすぎ（軽） | "Since radio waves do not travel well through water" | USCG PDF p.32〈24〉 | 「ほとんど届かない」 |
| c112 | 語り | 連絡は音波で、短い文字のメッセージ | 一致 | "The installed system used abbreviated text fields to communicate" | USCG PDF p.30〈22〉 | — |
| c112 | 語り・図 | 声で話す装置は**積んでいない** | 言いすぎ（軽） | "not fitted with a voice communications system capable of communicating while the submersible was operating below the surface" | USCG PDF p.30〈22〉 | 「海中で使える声の装置は無い」 |
| c112 | 語り・図 | 文字が届くまで**15秒から20秒**の遅れ | ずれ | "had an approximate 15 to 30 second delay from when TITAN sent a message to when it was received" | USCG PDF p.36〈28〉 | 「15〜30秒」。15〜20秒は2冊に無い（§5） |
| c112 | 見出し・副題 | 使えるのは、音波の文字だけ | 一致 | "TITAN’S sole communications equipment capable of subsurface communications" | USCG PDF p.30〈22〉 | — |
| c113 | 語り・図 | ふだんは海面の近くで**一度止まり**、通信を確かめる（図「止まっていない」） | ずれ（軽） | "Typically, the TITAN would maneuver near the surface for a communication check" | USCG PDF p.6〈vi〉 | 「止まる」は原文に無い。「海面の近くで通信を確かめてから」 |
| c113 | 語り・見出し・副題 | 最後の潜航ではその手順を踏んでいない | 一致 | "on this final dive, it did not follow that procedure" | USCG PDF p.6〈vi〉 | — |
| c113a | 語り | 潜航から14分後、毎分33mで降下中という通信が**入った** | ずれ（軽・送り手）・§4 | "At 9:28:35 a.m., the POLAR PRINCE texted, “we see you at 33 m/sec,” ... a correction of “m/min.”" | USCG PDF p.33〈25〉／NTSB PDF p.16 は "30 meters per minute" | 送ったのは母船（追跡で見えた速さを潜水艇へ）。「母船は、毎分33mで降りていると伝えた」 |
| c113a | 語り | そのあとも確認のやりとりは続いていた | 言いすぎ（軽） | "At 9:53:51 a.m., there was a loss of communication ... sent the same message multiple times over the next 13 minutes" | USCG PDF p.33〈25〉 | 9:53〜10:08 に途切れがあった。NTSB p.17 は「10〜15分ごと」 |
| c113a | 副題 | 潜航から14分後の通信 09:28 | 一致 | 同上 | USCG PDF p.33〈25〉 | — |
| c113a | 図 | 「14分後の位置」を水深**460m**に置く | ずれ | "The depth of the TITAN at the time was 436 m" (9:23:04) ／ "have you at 680 meters" (9:31:30) | USCG PDF p.32〜33〈24〜25〉 | 9:28 はおよそ600m。33m×14分の掛け算は使えない |
| c114 | 語り | 10時47分02秒、3,341m、重りを2つ落としたというメッセージが**届いた** | ずれ | "At 10:47:26 a.m., the communications and tracking team ... received a message from the TITAN, stating, “dropped two wts.”" | USCG PDF p.35〈27〉（送信 10:47:02） | 02秒は**送った**時刻。母船に届いたのは26秒＝爆縮（09秒ごろ）の後 |
| c114 | 見出し・副題 | 重りを2つ落とした／潜水艇から届いた最後のメッセージ | 一致 | "This was the last message that was sent from the TITAN." | USCG PDF p.36〈28〉 | — |
| c114 | 図 | 3,341m・10:47:02 | 一致（USCG）・§4 | "At approximately 10:47:02 a.m., the TITAN sent a message ... The depth of the TITAN was 3,341 m." | USCG PDF p.35〈27〉／NTSB PDF p.17 は同じ電文を 3,363 m | — |
| c115 | 語り・見出し・副題・図 | 海底が近づいたので降下を緩める。決められた手順 | 一致 | "which was a standard procedure at this depth to slow its descent" | NTSB PDF p.17／USCG PDF p.6〈vi〉 | — |
| c115a | 語り・見出し・副題・図 | 6秒後の10:47:08、3,346m、自動で最後の位置を送信 | 一致 | "Six seconds later, at 10:47:08 a.m., at a depth of 3,346.28 meters, the TITAN sent an automated transmission" | USCG PDF p.6〈vi〉 | — |
| c115b | 語り・副題 | その1秒後（10時47分09秒）、耐圧殻は壊れた | 言いすぎ（軽） | "At approximately 10:47:09 a.m., the TITAN submersible suffered a catastrophic implosion" | USCG PDF p.35〈27〉 | 「およそ1秒後」「09秒ごろ」 |
| c115b | 語り・図の注 | 水圧はおよそ4,930psi | 一致 | "exposed to approximately 4,930 pounds per square inch of water pressure" | USCG PDF p.7〈vii〉 | — |
| c115b | 語り | 5名はただちに亡くなった | 一致 | "resulting in the instantaneous death of all five occupants" | USCG PDF p.35〈27〉 | — |
| c115b | 図 | 「耐圧殻が壊れた深さ」3,346m | 言いすぎ・§4 | "the Titan imploded at a depth of 3,363 meters (10,032 feet)" | NTSB PDF p.58／USCG の3,346mは10:47:08の位置の深さ（p.35） | 「最後に位置が届いた深さ」。NTSB は 3,363m（p.58 の 10,032 feet は NTSB 自身の誤記） |
| c115c | 語り・副題 | 2秒後、母船で通信と追跡の担当が、海面から響く音を聞いた | 一致 | "Two seconds later the TITAN Communications and Tracking Team on the POLAR PRINCE heard a “bang” emanating from the ocean’s surface" | USCG PDF p.6〈vi〉／p.35〈27〉（10:47:11） | — |
| c115c | 語り | 調査は後に、この音を爆縮と結びつけている | 一致 | "which the investigation later correlated to the TITAN’s implosion" | USCG PDF p.6〈vi〉 | — |
| c115c | 見出し | 音は、海面まで**届いていた** | 言いすぎ（軽） | 同上 | USCG PDF p.6〈vi〉 | 見出しは断定。「爆縮の音と見られる」 |
| c115c | 図の注 | 出典：沿岸警備隊 **海難審判部** 報告書 | ずれ（名称） | "Marine Board of Investigation" | USCG PDF p.1 | 「海難調査委員会」 |
| c115d | 語り・副題 | NTSBは**同じ電文**の深さを3,363mと書いている | ずれ | "At 1047, while the Titan was at a depth of 11,032 feet (3,363 meters), OceanGate received a message that the submersible was dropping two weights" | NTSB PDF p.17 | NTSB の3,363mは「重り2つ」の電文の深さ。USCG で同じ電文は3,341m。3,346mは別の送信（自動の位置） |
| c115d | 語り・見出し・図 | 差は**17メートル**（3,346 対 3,363） | ずれ | 同上 | NTSB PDF p.17／USCG PDF p.35〈27〉 | 同じ電文どうしなら 3,363−3,341＝**22m**（旧 cuts_c1.py の注釈にも22mとある）。比べる相手を揃える |
| c115d | 図 | NTSB「11,032フィートからの換算」 | 一致 | "11,032 feet (3,363 meters)" | NTSB PDF p.17 | — |
| c115d | 図の注 | 秒まで特定している沿岸警備隊の値を採る | 一致 | — | — | 断りは良い |
| c116 | 語り・見出し・副題・図 | 10:48、母船は受け取ったと返信。返事は来なかった | 一致（NTSB） | "At 1048, the Polar Prince sent a message back to acknowledge the Titan’s message, but they received no response." | NTSB PDF p.17 | USCG では電文が母船に届いたのが10:47:26（p.35） |
| c117 | 語り・見出し・副題・図 | 10:49、追跡を失ったと送った。返事は無い | 一致 | "At 1049, the Polar Prince sent the Titan a “lost tracking” message but received no response." | NTSB PDF p.17／USCG PDF p.37〈29〉（10:49:11） | — |
| c118 | 語り | **母船の側は**まず通信機器の不具合を疑った | 言いすぎ（主語を広げた） | "OceanGate crew aboard the Polar Prince first assumed there was an issue with the acoustic communications equipment" | NTSB PDF p.17／USCG PDF p.38〈30〉（船長が知らされたのは11:15） | 「母船に乗っていたオーシャンゲートの担当は」 |
| c118 | 語り・見出し・副題 | 1分に2〜3回、呼びかけを送り続けた | 一致 | "The POLAR PRINCE sent two to three messages every minute until 2:50:09 p.m." | USCG PDF p.39〈31〉／NTSB PDF p.17 | — |
| c118 | 図 | ゲージの目盛り（60・180・200）「呼びかけの回数」 | 見つからない（軽） | （送った総数は2冊に無い） | — | 数として画面に出るなら根拠が無い。出ないなら不問 |
| c119 | 語り | 船長によれば、オーシャンゲートは緊急事態と受け取っていなかった | 一致 | "“this was not perceived to be an emergency by OceanGate and that was communicated to me.”" | USCG PDF p.38〈30〉／NTSB PDF p.17 | — |
| c119 | 見出し | 母船と会社で受け止めが**違った** | 言いすぎ | 同上 | USCG PDF p.38〈30〉 | 母船側が緊急と見ていたとは書かれていない。「会社は緊急と見なかった」 |
| c119 | 図 | 引用札「緊急事態とは受け取っていない」who=船長 | ずれ（主語） | 同上 | USCG PDF p.38〈30〉 | 受け取らなかったのは会社。札だと船長自身の受け止めに読める。主語「オーシャンゲートは」を入れる |
| c119 | 図 | to=海難審判部・when=**事故後の聴聞**・doc=海難審判部の記録 | ずれ | "The Master of the POLAR PRINCE stated in a written response to the MBI" | USCG PDF p.38〈30〉 | USCG はこの言葉を**書面の回答**として引く（聴聞での発言とはしていない）。名称も「海難調査委員会」 |
| c120 | 語り・見出し・副題・図 | 手順書には、途絶えて60分で浮上を始めるとあった | 一致（NTSB） | "required the submersible to begin ascending to the surface 60 minutes after communications were lost" | NTSB PDF p.17 | USCG p.39〈31〉の HSE 手順書は別の決まり（15/30/45分の確認・1時間＋浮上時間で社内連絡・さらに3時間の捜索） |
| c121 | 語り・副題 | 最後の深さから計算すると、午後3時には海面に出ている**はずだった** | 言いすぎ（軽） | "should have surfaced about 1500 had the pilot followed OceanGate’s procedures" | NTSB PDF p.17／USCG PDF p.39〈31〉 "approximately 3:00 p.m." | 条件（手順どおりなら）と「ごろ」を戻す |
| c121 | 語り・見出し | 何も浮いてこなかった | 一致 | "there was no indication that the vessel had surfaced" | NTSB PDF p.18 | — |
| c121 | 図 | 最後に分かっている深さ 3,346m・10:47 | 一致（USCG）・§4 | "given the Titan’s anticipated ascent rate and last known depth (11,032 feet)" | NTSB PDF p.17 は 11,032 ft で計算 | 計算の主は NTSB の記述なので、深さも NTSB では 3,363m |
| c122 | 語り・図 | 午後3時、会社は船に海面の捜索を指示 | 一致 | "about 1500, OceanGate personnel directed the Polar Prince crew to search the surface" | NTSB PDF p.18 | 「午後3時ごろ」 |
| c122 | 語り・見出し・副題・図 | 船長は3時間見つからなければ助けを呼べと言われていた | 一致 | "he was instructed to call for help after 3 hours if the Titan had not been found" | NTSB PDF p.18 | — |
| c123 | 語り・図 | 午後6時55分、カナダの救難調整本部へ | 一致（NTSB）・§4 | "about 1855, the Polar Prince crew contacted Joint Rescue Coordination Center Halifax" | NTSB PDF p.18／USCG PDF p.39〈31〉は船長の言で "At (6:27 p.m.) ... I called the Joint Rescue Coordination Centre (JRCC) Halifax" | 2冊で割れる。断るか一方に |
| c123 | 語り | 7時10分、**そこから**ボストンへ**引き継がれた** | ずれ | "The Canadian Coast Guard directed the POLAR PRINCE and OceanGate support personnel to contact the U.S. Coast Guard Rescue Coordination Center Boston" | USCG PDF p.6〈vi〉・p.39〈31〉／NTSB PDF p.18 | カナダが引き継いだのでなく、母船が自分でボストンに連絡した。USCG では7:10はカナダ沿岸警備隊への連絡の時刻 |
| c123 | 見出し・副題・図の題 | 通報は2つの国をまたいだ／ここで初めて公的な捜索 | 一致 | "Upon receiving the notification, the First Coast Guard District Command Center entered the distress phase" | USCG PDF p.40〈32〉 | — |
| c124 | 語り・副題 | 最後の通信から8時間が過ぎていた | 一致（計算）・§4 | "(approximately seven hours and 23 minutes after the last communication)" | USCG PDF p.39〈31〉 | 10:47→18:55＝8時間8分。USCG の本文は「約7時間23分」と書き、自身の時刻（10:47→19:10＝8時間23分）と合わない |
| c124 | 見出し | **外の誰も**、知らなかった | 言いすぎ | "The United States Coast Guard First District was not aware of the TITAN’s TITANIC Expedition dive operations on this date" | USCG PDF p.40〈32〉／NTSB PDF p.18 | 原文は「USCG は潜航を知らなかった」まで |
| c124 | 図 | 18:55「**最初の通報**」 | ずれ・§4 | "At (6:27 p.m.) ... I called the Joint Rescue Coordination Centre (JRCC) Halifax by sat phone" | USCG PDF p.39〈31〉 | USCG では最初の電話は18:27（途中で切れた）。「最初の」を外すか出どころを言う |
| c125 | 語り・見出し・副題 | 9:24pm、付近の船へ一斉電文「白い船体の21フィートの潜水艦、予定超過」 | 一致 | "issued a SafetyNET HYDROLANT message at 2124 ... “21 foot submarine, white hull, overdue.”" | NTSB PDF p.19 | — |
| c125 | 図 | 札 to=付近を航行する**船すべて** | 言いすぎ（軽） | "seeking assistance from nearby vessels" | NTSB PDF p.19 | 「付近の船」 |
| c125 | 図 | 札 ctx「外に伝えられたのは、この程度の情報だった」 | 言いすぎ | — | — | 原文に無い評価。削る |
| c126 | 語り・見出し・副題・図 | 実際の全長は22フィート（差1フィート） | 一致 | "The Titan was actually 22 feet (6.7 meters) long." | NTSB PDF p.19 | — |
| c126 | 語り | この時点では、その程度のことしか分かっていなかった | 言いすぎ | — | — | 原文に無い解釈 |
| c127 | 語り・見出し・副題・図 | 午後10時、沿岸警備隊の輸送機が飛び立ち、1時間25分後に現場 | 一致 | "At 2200, a US Coast Guard C-130 Hercules ... launched ... At 2325, the C-130 arrived on scene" | NTSB PDF p.19／USCG PDF p.40〈32〉 | 機は国際流氷パトロール所属の C-130 |
| c128 | 語り・見出し・副題・図 | 酸素とCO2吸収はおよそ96時間＝4日ぶん | 一致 | "an estimated 96 hours—or about 4 days—of emergency oxygen and carbon dioxide-scrubbing capability" | NTSB PDF p.17 | — |
| c128 | 図の題 | この数字が、その後の報道の時計になった | 一次資料の外 | — | — | 報道についての主張。§5 |
| c129 | 語り・副題 | 6月20日午後3時、最初に無人探査機を積んだ船が着いた | 一致（NTSB）・§4 | "the vessel arrived on scene about 1500 on June 20 (about 34 hours after the request)" | NTSB PDF p.20／USCG PDF p.42〈34〉は "On June 20, 2023, at 05:17 a.m." | 割れる（15:00 対 05:17）。断るか一方に。写真は Odysseus が後で写した尾部で、最初に着いた機体の写真ではない（CREDITS） |
| c129 | 語り・見出し・図 | その機体は3,000mまで（札 3,000m・海底まで3,840m） | 一致 | "with two ROVs capable of reaching 9,843 feet (3,000 meters)" | NTSB PDF p.20 | 機体は2機 |
| c130 | 語り・見出し・副題 | 海底に届かせようと限界より約1,000m深く潜らせ、壊れた | 一致 | "dove the ROV beyond its rated depth, almost another 3,281 feet (1,000 meters); the ROV was destroyed" | NTSB PDF p.20 | — |
| c130 | 図 | 3,840mに「**海底まで**潜らせて壊れた」 | 言いすぎ | "in an effort to reach the seabed, they dove the ROV beyond its rated depth" | NTSB PDF p.20 | 海底に着いたとは書かれていない。「海底を目指して限界を超え、壊れた」 |
| c131 | 語り・副題 | **6月21日から22日にかけて**、6,000m級が2機届いた | ずれ（軽） | "On June 22, both the Atalante (with the Victor 6000) and the Horizon Arctic (with the Odysseus) were in position over the site." | NTSB PDF p.20／USCG PDF p.269〈261〉 | 現場に揃ったのは6月22日。21日は Odysseus を船に積んだ日 |
| c131 | 語り・図 | 1機は米空軍の輸送機、もう1機はフランスの調査船 | 一致 | "910th Air Wing flew the ROV Odysseus on a C-130 to Newfoundland and Labrador" | NTSB PDF p.20 | 空輸はニューファンドランドまで（そこから船） |
| c131 | 見出し・図の注 | 6,000m級が2機／出どころ NTSB 図24 | 一致 | "Figure 24. Assets that participated in the search for the Titan" | NTSB PDF p.67 | — |
| c132 | 語り・副題 | 6月22日午前9時40分、1機が残骸を見つけた | 一致・§4 | "At 0940, the Odysseus discovered a debris field consistent with the Titan" | NTSB PDF p.20／USCG PDF p.42〈34〉 | USCG の分析（p.269〈261〉）は "08:40 a.m."＝USCG の中で割れる |
| c132 | 語り・見出し | 尾部と2つのチタンのドーム | 一致 | "including the tail cone and both titanium domes" | NTSB PDF p.20 | — |
| c132 | 語り・図 | タイタニックの船首の**すぐそば** | 言いすぎ | "about 500 meters (1,148 feet) northeast of the bow of the Titanic" | NTSB PDF p.20 | 「船首から数百メートル」。500mと1,148ft はNTSBの中で合わない（§4） |
| c133 | 語り・見出し・副題・図 | 船11隻・航空機4機、1万2千平方海里超（12,145） | 一致・§4 | "11 vessels and four aircraft searched 12,145 square nautical miles" | USCG PDF p.7〈vii〉 | USCG p.42〈34〉は "12,145 square miles"（単位が USCG の中で割れる） |
| c133a | 語り・見出し・図 | 生還者はいなかった（5名全員） | 一致 | "There were no survivors." | NTSB PDF p.20 | — |
| c134 | 語り・見出し | 通常なら無人探査機を入れるまで2週間 | 言いすぎ（軽） | "US Coast Guard search and rescue personnel testified it would normally take 2 weeks to get an ROV to the location" | NTSB PDF p.20／USCG PDF p.41〈33〉 | 「捜索救助の担当者の証言では」と帰属を戻す |
| c134 | 語り・図 | それを4日でやっていた／96時間をわずかに過ぎた | 一致（計算） | "was achieved in days" | USCG PDF p.41〈33〉 | 4日は旧版の計算（6/18→6/22）。原文は "in days" |
| c135 | 語り | 救助が間に合う事故ではなかった | 一致 | "resulting in the instantaneous death of all five occupants" | USCG PDF p.35〈27〉 | — |
| c135 | 副題 | 回収された耐圧殻の破断面 | 一致 | "Recovered carbon fiber composite cylinder machined end face, and mid-span fractured face." | NTSB PDF p.42 | — |

### 第2章 炭素繊維という選択（c201〜c230）

| カット | 種類 | 旧版の主張（短く） | 判定 | 原文の抜き書き（英語25語まで） | 出典 | 直し方の当たり |
|---|---|---|---|---|---|---|
| c201 | 語り・見出し・副題・図 | タイタニックは水深3,800m超の海底（札「3,800 m これより深い」） | 一致・§4 | "the depth (3,840 meters (m); 12,598 feet) of the TITANIC on the ocean floor" | USCG PDF p.13〈5〉／NTSB PDF p.10 は 3,880 m | — |
| c201 | 語り・図 | 水圧はおよそ5,500psi | 一致 | "At the depth of the Titanic wreckage site, water pressure is 5,554.5 pounds per square inch." | NTSB PDF p.10 | — |
| c202 | 語り | 海面の気圧のおよそ378倍 | 一致（計算） | "At sea level, atmospheric pressure is 14.7 pounds per square inch." | NTSB PDF p.10 | 5,554.5÷14.7＝377.9 |
| c202 | 図 | 札「水深3,800メートルの水圧」＝378倍・5,500psi | ずれ（軽） | 同上（NTSB はこの水圧を、深さ3,880mとする残骸の場所の値として書く） | NTSB PDF p.10 | 「タイタニックの深さの水圧」 |
| c202 | 語り・見出し・副題 | 息をする空気を保ち続ける入れ物が耐圧殻 | 一致 | "maintained atmospheric air pressure for the Titan’s human occupants during dives" | NTSB PDF p.10 | — |
| c203 | 語り・見出し・副題・図 | 全長22フィート・6.7m、定員は操縦士を含め5名 | 一致 | "could carry up to five persons, including one pilot" ／ "Length (overall) 22.0 ft (6.7 m)" | NTSB PDF p.21／USCG PDF p.11〈3〉"Length: 22 feet" | — |
| c203 | 図の注 | 出どころ：沿岸警備隊 海難審判部 報告書 | ずれ（名称・帰属） | — | NTSB PDF p.21 | 名称は「海難調査委員会」。6.7mと定員の書き方は NTSB |
| c204 | 語り・図 | 円筒の長さは8.1フィート | 一致（NTSB）・§4 | "The cylindrical-shaped 8.1-foot-long pressure hull (pressure vessel)" | NTSB PDF p.10／USCG PDF p.5〈v〉は "8-foot long" | — |
| c204 | 語り・見出し | 人が入るのは**円筒だけ** | 言いすぎ（軽） | "the Titan pressure vessel includes the carbon fiber-based composite cylinder, titanium rings, and titanium domes" | NTSB PDF p.10 | 人のいる空間は両端のドームの内側まで。「人が入るのは耐圧殻の中」 |
| c204 | 語り・副題・図 | 炭素繊維の円筒の両端にチタンのリング | 一致 | "a thick-walled, carbon fiber-based composite cylinder fitted at each end with a titanium ring (segment)" | NTSB PDF p.10 | — |
| c205 | 語り・見出し・副題・図 | ドームは18本のボルト、リングと円筒は接着 | 一致 | "The titanium segments were glued to the cylinder, and the titanium domes were bolted to the segments." | NTSB PDF p.10・p.30 | — |
| c206 | 語り・見出し・副題・図 | 前のドームにのぞき窓 | 一致 | "viewport, which was seated in a machined titanium cutout in the forward dome" | USCG PDF p.188〈180〉 | — |
| c207 | 語り・見出し・副題・図 | 炭素繊維の耐圧殻に、国内・国際の認められた規格は無い | 一致 | "There are currently no recognized national or international standards that approve of the use of carbon fiber pressure hulls for submersibles." | USCG PDF p.274〈266〉／NTSB PDF p.47 | 「潜水艇の」と限定を足すとなお良い |
| c207 | 図の注 | 出どころ：沿岸警備隊 **海難審判部** 報告書 | ずれ（名称） | "Report of the Marine Board of Investigation" | USCG PDF p.1 | 「海難調査委員会」。中身の帰属（USCG p.274）は正しい |
| c208 | 語り・副題 | CEOは炭素繊維が引っ張りより圧縮に強いと考えていた | 一致（注） | "the CEO chose carbon fiber because he believed it was “better in compression than tension.”" | NTSB PDF p.25（元海洋運用部長の証言） | 誰の証言かを足す。USCG はこの理由を書かず「強さと重さの比」を挙げる（p.274） |
| c208 | 図 | 札「炭素繊維の強さ：強＝圧縮／弱＝引っ張り」 | 逆 | "extreme compressive forces, a scenario for which carbon fiber has no established track record and is generally understood to be less effective" | USCG PDF p.274〈266〉 | 札は性質の事実に読める。USCG は逆（引っ張りで実績・圧縮で劣る）。札に「CEOの考え」と書くか、USCG の見方を並べる |
| c208 | 図の注 | 出どころ：沿岸警備隊 海難審判部 報告書 | ずれ（帰属） | （"better in compression than tension" は USCG に無い） | NTSB PDF p.25 | 出どころは NTSB |
| c209 | 語り | 軽いので浮力の助けが少なくて済み、いろいろな船から出せる | 言いすぎ（軽） | "the CEO believed it would require less buoyancy and could be launched from a bigger variety of surface tenders" | NTSB PDF p.25 | CEO の考えを事実の形で言っている。「CEOは…と考えた」 |
| c209 | 見出し・副題・図 | もうひとつの理由は軽さ（浮力材が減る・母船を選ばない） | 一致 | 同上 | NTSB PDF p.25 | 「理由」と言っているので可 |
| c211 | 語り・見出し・副題・図 | 最初の目標：6,000m・安全率2.25（壊れる深さ÷潜ってよい深さ）・1万回 | 一致 | "rated to dive up to 6,000 meters (19,680 feet) with a 2.25 safety factor and a 10,000-cycle life limit" | NTSB PDF p.24 | 原文は「最適の設計目標」。USCG p.109〈101〉の2015年の設計計算は安全率2.19／2.21（§4） |
| c213 | 語り・見出し・副題・図 | 船級＝国とは別の第三者が図面・工事・試験を確かめる | 一致 | "Classification societies are nongovernmental organizations ... reviewing plans ... witnessing critical testing, and surveying the vessel." | NTSB PDF p.22 | — |
| c214 | 語り・見出し・副題・図 | 合格で証明書、定期検査を受けないと続かない | 一致 | "To maintain a valid certificate of classification, a vessel must undergo additional periodic surveys" | NTSB PDF p.22 | — |
| c215 | 語り・見出し・副題・図 | 2016年に入った海洋運用部長によれば、当初はロイズかDNVで船級を取るつもり | 一致 | "when he was hired in 2016, the company planned to class the submersible through Lloyd’s Register or DNV" | NTSB PDF p.22 | — |
| c216 | 語り・見出し・副題・図 | 2018年に計画を捨てた。CEOは時間がかかりすぎると判断 | 一致 | "the OceanGate CEO ultimately decided classing the Titan would take too long ... In 2018, OceanGate abandoned classing efforts." | NTSB PDF p.23 | — |
| c217 | 語り・副題・図 | ある業界関係者に、CEOは「船級は高すぎる。できない」と言っている | 言いすぎ（軽） | "According to the signatory, the CEO stated that classification was “too expensive” and “not doable.”" | NTSB PDF p.24 | 聞いた本人（書簡の署名者）の証言であることを足す |
| c216〜c218 | 並び順 | 「高すぎる」の発言（c217）を2018年2月の書簡（c218）より前に置く | ずれ（軽・順序） | "the CEO received the letter; afterward, in a conversation with the CEO, the signatory expressed concern" | NTSB PDF p.24 | 原文ではこの会話は書簡を受け取った後 |
| c218 | 語り・見出し・副題・図 | 2018年2月、海洋技術協会の潜水艦委員会が集まり、CEO宛ての書簡の草案を書いた | 一致 | "In February 2018 ... members of the Marine Technology Society’s Submarine Committee met for a conference" | NTSB PDF p.23／USCG PDF p.152〈144〉 | — |
| c219 | 語り・見出し・副題・図 | 開発と遠征に、全員一致の懸念を表明する | 一致 | "expressing “unanimous concern regarding the development of ‘TITAN’ and the planned Titanic Expedition.”" | NTSB PDF p.23 | — |
| c220 | 語り・見出し・副題・図 | 実験的な進め方は、軽いものから破滅的なものまで悪い結果を招きかねない | 一致 | "the current ”experimental” approach adopted by OceanGate could result in negative outcomes (from minor to catastrophic)" | NTSB PDF p.23 | — |
| c221 | 語り・図 | 業界の関係者が**何十人も**署名 | 一致（NTSB）・§4 | "The letter was signed by dozens of other industry representatives." | NTSB PDF p.24／USCG PDF p.152〈144〉は "More than 20 professionals signed the letter" | 「20人を超える」なら両方に合う |
| c221 | 語り・見出し・副題・図 | 正式には送られなかったが、CEOは中身を知っていた | 一致 | "it was confirmed that the CEO of OceanGate received the letter and responded to it" | USCG PDF p.152〈144〉／NTSB PDF p.24 | — |
| c222 | 語り・見出し・副題・図 | そのあと、会社のサイトはタイタンを実験的な潜水艇と書き換えた | 一致 | "OceanGate’s website was later updated to reflect that the Titan was an “experimental submersible.”" | NTSB PDF p.24 | 図の注「出どころ：ウェブサイト」は NTSB の記述による |
| c223 | 語り・見出し・副題 | 2019年、会社は「船級を取ること自体では安全は保証できない」 | 一致 | "In a 2019 blog post on its website, OceanGate stated, … by itself, classing is not sufficient to ensure safety." | NTSB PDF p.24 | — |
| c223 | 図 | 引用札「船級では保証できない」・ctx「サイトを書き換えたあとに」 | 言いすぎ（軽） | 同上 | NTSB PDF p.24 | 「それだけでは」が落ちた。書き換えとの前後は原文に無い |
| c224 | 語り・見出し・図 | 報告書ははっきり書く：沿岸警備隊にも船級協会にも「実験的」という区分は無い | 言いすぎ | "Classification societies have a path for owners to prove seaworthiness of new technology. However, ... no “experimental” design endorsement for vessels carrying passengers or cargo." | NTSB PDF p.23（脚注17）／USCG PDF p.319〈311〉 | 前半（新技術を証明する道はある）を切り、「旅客・貨物を運ぶ船について」の限定も落ちた |
| c224 | 副題・図の注 | 報告書が当たった2つの制度／出どころ：沿岸警備隊 海難審判部 報告書 | ずれ（帰属） | "the term “experimental” is not officially recognized to apply to vessels or submersibles under U.S. commercial maritime regulations" | USCG PDF p.319〈311〉 | 2つの制度を並べたのは NTSB の脚注。USCG は米国の規則についてだけ |
| c225 | 語り・見出し・副題・図 | 料金を払った人たちはミッションスペシャリストと呼ばれた | 一致 | "OceanGate referred to its clients as “mission specialists.”" | NTSB PDF p.15／USCG PDF p.317〈309〉節名 | — |
| c226 | 語り・見出し・副題・図 | 計画書：資金を助ける客で、乗組員に加わり機材の作業を手伝う選択肢を持つ | 一致 | "“guests who help fund OceanGate expeditions … [who had] the option to join OceanGate crew and physically work with us on our equipment”" | NTSB PDF p.48 | — |
| c227 | 語り・図 | 沿岸警備隊にいた元技術者がCEOに「対価を受け取っている以上、肩書きを変えるだけでは済まない」 | 一致 | "“… you can’t just change the title of a person when you’re receiving compensation.”" | NTSB PDF p.47 | — |
| c227 | 見出し | **外部の**技術者が警告していた | ずれ | "A former operations technician (hired in 2017), who had previous experience as an engineer/machinery technician in the US Coast Guard" | NTSB PDF p.47 | 外部でなく社員（2017年採用の運航技術者）。「社内の技術者が」 |
| c228 | 語り・副題・図 | のちの会話でCEOは「沿岸警備隊が問題になるなら議員を1人買って消す」と言ったという | 一致 | "“if the [US] Coast Guard became a problem … he would buy himself a congressman and make it go away.”" | NTSB PDF p.47／USCG PDF p.299〈291〉・p.306〈298〉 | — |
| c228 | 見出し | 制度そのものを軽んじていた | 一致（解釈） | "Mr. Rush’s response demonstrates that he was aware that his operations were outside regulatory compliance." | USCG PDF p.299〈291〉 | USCG の評価は「規則の外と分かっていた」 |
| c229 | 語り・見出し・副題・図 | 技術者は会社の運営の合法性への懸念から辞めた | 一致 | "The technician resigned following this conversation, citing concerns for “the legality of how it [OceanGate] was operating.”" | NTSB PDF p.47 | — |
| c230 | 語り・見出し・副題・図 | 州の登録・国の船舶登録・どこかの国の検査、どれも無し | 一致 | "The Titan was not registered in any US state, documented by the US National Vessel Documentation Center, nor inspected by any flag state." | NTSB PDF p.21／USCG PDF p.58〈50〉・p.11〈3〉 | — |
| c230 | 図の注 | 出どころ：沿岸警備隊 **海難審判部** 報告書 | ずれ（名称） | "Report of the Marine Board of Investigation" | USCG PDF p.1 | 「海難調査委員会」。中身の帰属（USCG p.5・p.58）は正しい |

### 第3章 一度目の船体（c301〜c328）

| カット | 種類 | 旧版の主張（短く） | 判定 | 原文の抜き書き（英語25語まで） | 出典 | 直し方の当たり |
|---|---|---|---|---|---|---|
| c301 | 語り・見出し・副題・図 | 2015年、外部の会社に円筒の応力解析を頼み、爆縮深度はおよそ13,200m | 一致（NTSB）・§4 | "hired Spencer Composites in 2015 to complete a stress analysis ... the analysis indicated an implosion depth about 13,200 meters" | NTSB PDF p.24〜25／USCG PDF p.109〈101〉は安全率2.19／2.21と書き、13,200mは無い | — |
| c302 | 語り | タイタニックの**3倍以上、深く潜れる**という計算 | ずれ | 同上（13,200mは「壊れる深さ」） | NTSB PDF p.25／p.24（潜ってよい深さの目標は6,000m） | 「壊れる深さはタイタニックの3倍以上という計算」。潜ってよい深さ（6,000m）は約1.6倍 |
| c302 | 語り・副題 | これは紙の上の数字 | 一致 | — | — | — |
| c302 | 見出し・図 | 設計は大きな余裕／13,200 対 3,800・3倍以上 | 一致（計算） | — | NTSB PDF p.25 | 札の「爆縮深度」の言い方は正しい |
| c303 | 語り | 2016年3月までに3分の1の縮尺模型 | 一致 | "Spencer Composites constructed the model sometime before March 2016." | NTSB PDF p.25 | USCG では最初の試験が2015-12-21（p.111〈103〉） |
| c303 | 副題 | 2016年3月 3分の1の縮尺模型 | ずれ（軽） | 同上 | NTSB PDF p.25 | 「までに」が落ちて3月に作ったと読める |
| c303 | 語り・見出し・図 | 糸を液体の樹脂にくぐらせ、濡れたまま巻く | 一致 | "wet winding—wherein carbon fiber strands were run through a bath of liquid resin" | NTSB PDF p.25 | — |
| c304 | 語り・副題 | 試験を2回続けたら炭素繊維のドームが先に壊れた（副題「試験は2回」） | 一致（NTSB）・§4 | "During two successive tests of sub-scale models, the carbon fiber domes prematurely failed" | NTSB PDF p.25／USCG PDF p.111〜113〈103〜105〉は4回（2015-12・2016-02・2016-03・2016-07） | USCG とは回数も順も違う。副題「試験は2回」は全体の回数に読める |
| c304 | 語り・見出し・図 | ドームだけをチタンに替えた | 一致（NTSB）・§4 | "OceanGate replaced the carbon fiber domes with titanium end domes constructed by TiFab" | NTSB PDF p.25／USCG PDF p.114〈106〉は「チタンのドームで新しい模型を作る案は却下」 | 2冊で食い違う（USCG では2016-03にも炭素繊維のドームで試験） |
| c306 | 語り・副題・図 | 2016年6月、作り直した模型は4,200m相当で爆縮 | 一致（NTSB）・§4 | "During testing in June 2016, the updated sub-scale model pressure vessel imploded at a depth of about 4,200 meters" | NTSB PDF p.25／USCG PDF p.112〈104〉は2016年2月に4,200m、p.113〈105〉は2016-07-07に4,304m | 「およそ」を戻す。月は2冊で割れる |
| c306 | 語り・図 | 計算の13,200mには遠く届かない（3分の1にも届かない） | 一致（計算・注） | "managed to withstand pressures equivalent to 4,200 m (13,780 feet), which was less than the 4,500 m (14,764 feet) that was the target" | USCG PDF p.114〈106〉 | USCG は目標4,500mと比べている |
| c307 | 語り・見出し | CEOによれば、その模型の円筒に剥離があった | 一致 | "According to the CEO, that model had a delamination in the carbon fiber cylinder." | NTSB PDF p.25 | 写真は2023年の回収破片（副題で断りあり） |
| c308 | 語り・見出し | 剥離＝層と層のあいだが離れること。円筒は何層も | 一致 | "A delamination is a failure mode in layered materials where a separation forms between layers." | NTSB PDF p.25（脚注22） | — |
| c308 | 図 | 5層と「接着の面」の断面図（c318・c324 も同じ図） | ずれ（軽） | "two delaminations between the five 1-inch-thick layers" | NTSB PDF p.59（2号殻） | 5層を接着で重ねたのは2号殻。1号殻は濡れたまま巻いた円筒（NTSB p.25 "again using wet winding"・USCG p.109〈101〉） |
| c309 | 語り・見出し・副題・図 | 2018年、同じ会社が実物大の1号殻を作った | 一致（NTSB）・§4 | "In 2018, Spencer Composites constructed the first (v1) full-scale Titan pressure vessel" | NTSB PDF p.25／USCG PDF p.118〜119〈110〜111〉は製造2017年3月〜10月、組み立て完了2018年1月（p.152） | 「2018年に組み上がった」なら両方に合う |
| c310 | 語り・見出し・副題・図 | 2018年1月、海洋運用部長がCEOと役員に品質検査の報告書 | 一致 | "In January 2018, OceanGate’s director of marine operations submitted a “quality control inspection report” ... to the CEO and other OceanGate directors." | NTSB PDF p.47／USCG PDF p.146〈138〉（1月18日） | — |
| c311 | 語り・見出し・副題・図 | 削り落とした円筒の端に、はっきり見える剥離と空隙 | 一致 | "“very visible signs of delamination and porosity” in the machined-off ends of the v1 carbon fiber cylinder" | NTSB PDF p.47 | — |
| c313 | 語り・図 | 1月19日の会話をCEO自身が録音していた | 一致 | "The meeting lasted two hours and four minutes and was audio recorded by the CEO." | USCG PDF p.149〈141〉／NTSB PDF p.48 | — |
| c313 | 見出し・副題・図 | **2人は**話していた（部長とCEO） | ずれ（軽）・§4 | "met with Mr. Rush, the Director of Engineering, a Human Resources representative, and the COO, for a two-hour meeting" | USCG PDF p.149〈141〉／NTSB PDF p.48 は2人の会話として書く | 「2人」は NTSB の書き方。USCG では5人の会合 |
| c314 | 語り・図 | CEO「設計に、あなたが信頼を**置いていない**のは明らか」 | 言いすぎ（軽） | "“it’s clear that there is not a lot of confidence on your part in the engineering that went into this vessel”" | NTSB PDF p.48 | 「あまり信頼していない」 |
| c314 | 語り・見出し | 他の船での経験から、ごく基本の部分で安全を心配している | 一致 | "your experience in other vessels gives you serious concerns about the safety of [the Titan] from the very fundamental level" | NTSB PDF p.48 | — |
| c315 | 語り・見出し・副題・図 | 4日後の1月23日に解雇 | 一致 | "On January 23, 2018, OceanGate terminated the director of marine operation’s employment." | NTSB PDF p.48／USCG PDF p.149〈141〉 | — |
| c316 | 語り・見出し・副題・図 | 船員を守る法律にもとづき労働安全衛生局へ申し立て | 一致 | "filed a complaint with the Occupational Safety and Health Administration (OSHA) under the Seaman’s Protection Act" | NTSB PDF p.48／USCG PDF p.149〈141〉（2018-02-06） | — |
| c317 | 語り・見出し・副題・図 | 調査官に「切り落とした断面はスイスチーズのよう」 | 一致 | "He told an OSHA investigator that cut-off sections of the carbon fiber cylinder were “like Swiss cheese”" | NTSB PDF p.48 | — |
| c318 | 語り・見出し・副題 | 樹脂がきちんと接着されていない剥離が全部見える | 一致 | "“you can see all the delaminations where the resin has not been glued properly.”" | NTSB PDF p.48 | 図は c308 と同じ注 |
| c319 | 語り・見出し・副題・図 | 会社が秘密保持契約の違反などで提訴、部長は申し立てを取り下げ | 一致 | "OceanGate subsequently filed a lawsuit, citing a breach of a non-disclosure agreement, among other things." | NTSB PDF p.48／USCG PDF p.150〜151〈142〜143〉（提訴2018-06-25・取り下げ2018-12-13） | — |
| c320 | 語り・見出し・図 | 通常なら、労働安全衛生局は開始と終了を手紙で沿岸警備隊に知らせる | 言いすぎ（軽） | "An OSHA investigator stated that OSHA typically sent letters to the US Coast Guard when they opened and closed investigations" | NTSB PDF p.48 | 調査官の証言であることを足す |
| c320 | 語り | この件のやりとりを、どちらの担当者も覚えていない | 一致（注）・§4 | "he couldn’t recall any contact with the US Coast Guard for this case" | NTSB PDF p.48／USCG PDF p.150〈142〉 | USCG は「2018-02-26 に OSHA が USCG へメールを送ったが、受け取られていなかった」と調べている。④で足す価値あり |
| c321 | 語り・見出し・副題・図 | 2018〜2019年、1号殻は49回潜航（エヴェレットとバハマ） | 一致 | "Between February 2018 and June 2019, OceanGate completed 49 dives of the Titan v1 pressure vessel" | NTSB PDF p.25〜26 | 番号は「出かけた回」の通し番号（NTSB 脚注23） |
| c321 | 語り・図の注 | 最も深い潜航は4,000m | 一致（NTSB）・§4 | "2 to 4,000 meters"（表2） | NTSB PDF p.26／USCG PDF p.157〈149〉は最深 3,939 m（2018-12-12） | 「約4,000m」 |
| c322 | 語り・見出し・副題・図 | 2019年のバハマの複数の潜航で、ひび割れるような音 | 一致 | "During dives 42 through 44 and 45.1 through 47, conducted in The Bahamas in 2019, persons aboard the Titan reported hearing cracking sounds." | NTSB PDF p.26／USCG PDF p.314〈306〉 | — |
| c323 | 語り・見出し・副題・図 | 2019年6月、48回目のあと、準備中の社員が円筒に髪の毛のような亀裂 | 一致（NTSB）・§4 | "In June 2019, after dive 48, while making preparations for a dive, an OceanGate employee noticed a hairline fracture" | NTSB PDF p.26／USCG PDF p.161〈153〉は2019-05-29・操縦士・縦に約4フィート | 日付・見つけた人・大きさが2冊で割れる |
| c324 | 語り・見出し・副題 | 亀裂は表面の下の剥離から始まっていた | 一致 | "An examination of the crack indicated that it had originated from a sub-surface delamination" | NTSB PDF p.26 | — |
| c325 | 語り・見出し・図 | 初代の技術部長はCEOに「亀裂がある以上、この耐圧殻は終わりだ」と言ったと述べている | 一致（NTSB）・§4 | "he told the CEO that because there was a crack, the pressure vessel hull was “done,”" | NTSB PDF p.26／USCG PDF p.161〜162〈153〜154〉 | USCG では承認の拒否は亀裂の前（2019年春）、亀裂の後は COO に「修理できない」と伝えた。順序と相手が2冊で違う |
| c326 | 語り・見出し・副題・図 | 「どこへも持っていくつもりはない」、2019年の遠征の承認を拒んだ | 一致 | "he was “not going to take this [the Titan] anywhere.” ... he would not sign off on the planned 2019 expedition" | NTSB PDF p.26／USCG PDF p.161〈153〉"refused" | — |
| c327 | 語り・見出し・副題・図 | 客の予約はすでに入っていた。技術部長はまもなく解雇 | 一致 | "had booked clients (“mission specialists”) ... He was terminated shortly thereafter." | NTSB PDF p.26 | — |
| c328 | 語り・副題・図 | 2019年の遠征は中止、メリーランドで追加の試験 | 一致 | "The v1 pressure vessel was shipped to the Deep Ocean Test Facility ... in Annapolis, Maryland, for additional testing." | NTSB PDF p.26／USCG PDF p.166〈158〉（Bethesda, Maryland） | — |
| c328 | 語り・見出し・図 | 会社は1号殻を**使用不可**と判断 | 一致（NTSB）・§4 | "OceanGate condemned the v1 pressure vessel following this testing" | NTSB PDF p.26／USCG PDF p.167〈159〉は "a de-rating of the first TITAN hull to a maximum operational depth of 3,000 m" | USCG では「3,000mまでに格下げ」。どちらの報告か言う |

## §4 2つの報告書で割れる数

29行＝2冊で割れる22（事故の深さ〜メリーランドの試験の後のうち、下の5行と参考2行を除いたもの）／1冊の中で食い違う5（通報までの時間・残骸の発見時刻・捜索の広さの単位・最後の位置の座標＝USCG、残骸と船首の距離＝NTSB）／参考2（安全率・13,200m＝量が違う、または片方にしか無い）

| 項目 | USCG | NTSB | 旧版の扱い |
|---|---|---|---|
| 事故の深さ | 3,341m（10:47:02 の「重り2つ」の電文）／3,346.28m＝10,978ft（10:47:08 の最後の位置） PDF p.35〈27〉 | 3,363m＝11,032ft（1047 の「重り2つ」の電文・事故の深さ） PDF p.17・p.53・p.58（p.58 の "10,032 feet" は NTSB の誤記） | USCG を採用（c115d に断りあり）。ただし c115d は比べる相手がずれ、差を17mとした（同じ電文なら22m） |
| 42人の内訳 | 乗組員17・clients 24・指定なし1 PDF p.5〈v〉 | 乗組員17・会社側21（CEO を含む）・客3・案内役1 PDF p.15 | NTSB を採用。図の注で断りあり。語りは断りなし |
| 現場に着いた時刻 | 5:15 a.m. PDF p.23〈15〉 | about 0400 PDF p.15 | USCG（断りなし） |
| 波 | 到着時 2〜3m PDF p.24〈16〉（NOAA は「朝に短い凪」 p.20〈12〉） | 事故時 2〜3 feet PDF p.53 | 「穏やか」＝どちらの数とも書かず、USCG とは逆 |
| 乗り込み・ドーム・停止の順 | 8:30 乗り込み＋ドーム固定 → 8:57 停止 → 9:04 沈める PDF p.28〜29 | 0800 乗り込み → 停止 → 0830 ドーム → 沈める PDF p.16 | 混ぜたため、どちらの順とも合わない |
| 台から離れた時刻 | 9:14 a.m. PDF p.30〈22〉 | about 0900 PDF p.16 | USCG（断りなし） |
| 降下の速さ | 33 m/min（9:28 の母船の電文） PDF p.33〈25〉 | 98 ft/min（30 m/min） PDF p.16 | USCG（断りなし） |
| JRCC ハリファクスへの連絡 | 6:27 p.m.（船長の言・途中で切れた）。7:10 p.m. カナダ沿岸警備隊へ→ボストンへの連絡を案内 PDF p.39〈31〉 | about 1855 JRCC Halifax、1910 RCC Boston PDF p.18 | NTSB の時刻＋「カナダから引き継がれた」（どちらとも違う流れ） |
| 通報までの時間 | 本文は「約7時間23分」（自身の 10:47→19:10＝8時間23分と合わない） PDF p.39〈31〉 | （時刻のみ） | 8時間（NTSB の時刻からの計算） |
| 最初の ROV 船の到着 | 6月20日 05:17 a.m. PDF p.42〈34〉 | 6月20日 about 1500 PDF p.20 | NTSB（断りなし） |
| 残骸の発見時刻 | 09:40（p.7・p.42）と 08:40（分析 p.269〈261〉）＝USCG の中で割れる | 0940 PDF p.20 | 9:40（両方の多数側） |
| 捜索の広さの単位 | 12,145 square nautical miles（p.7）と square miles（p.42）＝USCG の中で割れる | （付録C） | 平方海里 |
| 最後の位置の座標 | 41°44.06′N 049°56.54′W（p.35）と 41°49.06′N 048°56.54′W（分析 p.269）＝USCG の中で割れる | — | 画面に出していない（c115a「緯度経度つき」のみ） |
| タイタニックの深さ | 3,840m（p.13）・約3,800m（p.61） | 3,880m（p.10）・3,840m（p.30・p.36ほか） | 3,840m／3,800m超 |
| 残骸と船首の距離 | — | "about 500 meters (1,148 feet)"＝NTSB の中で合わない（500m＝1,640ft） PDF p.20 | 「すぐそば」 |
| ダイブ80の音の時刻 | 15:17ごろ増え始め、15:26:45 に大きな音とひずみの跳び（p.283〜286〈275〜278〉）。剥離を 15:26:56 とも書く（p.289〈281〉＝USCG の中で11秒ずれる） | "between about 1515 and 1530" PDF p.52 | NTSB の幅で帯を描いたが、山と跳びの位置は USCG と合わない |
| ダイブ80で傷んだ時点 | "still submerged but nearing the surface"（p.234・p.286）と "after surfacing from Dive 80"（p.290）＝USCG の中で揺れる | "after it surfaced at the end of dive 80" PDF p.59 | 「浮上の途中」。図は1,600m（どちらにも無い） |
| 耐圧殻の円筒の長さ | "8-foot long" PDF p.5〈v〉 | "8.1-foot-long" PDF p.10 | NTSB（断りなし） |
| 安全率 | 2015年の設計計算 2.19（チタンのドーム）／2.21（炭素繊維のドーム）、塑性崩壊は設計荷重の1.88〜2.03倍 PDF p.109〈101〉 | 最初の設計目標 2.25 PDF p.24 | NTSB の目標の値（量が違うので矛盾ではない） |
| 2015年の解析の爆縮深度 | 13,200m の記述なし | about 13,200 m PDF p.25 | NTSB（断りなし） |
| 書簡の署名の数 | "More than 20 professionals" PDF p.152〈144〉 | "dozens" PDF p.24 | NTSB（何十人も） |
| 1号殻の縮尺模型の試験 | 4回：2015-12-21（炭素繊維のドームが約3,000m相当で破損）・2016-02（6,000psi＝4,200m）・2016-03-11（4,009psi・炭素繊維のドーム）・2016-07-07（4,304m）。チタンのドームの模型の案は却下 PDF p.111〜114〈103〜106〉 | 2回続けて炭素繊維のドームが早く壊れ→TiFab のチタンのドームに→2016年6月に約4,200mで爆縮 PDF p.25 | NTSB（断りなし） |
| 1号殻を作った年 | 円筒の製造 2017年3月〜10月、組み立て完了 2018年1月 PDF p.118〜119・p.152 | 2018年 PDF p.25 | NTSB |
| 2018-01-19 の話し合い | 5人の会合（CEO・技術部長・人事・COO・海洋運用部長）2時間4分 PDF p.149〈141〉 | 部長とCEOの会話 PDF p.48 | NTSB（「2人」） |
| OSHA と USCG の連絡 | 2018-02-26 に OSHA が USCG へメール（受け取られず）、2019-08-28 の一覧にも載る PDF p.150〈142〉 | 双方の担当者とも連絡を覚えていない PDF p.48 | NTSB のみ |
| 1号殻の最深 | 3,939m（2018-12-12） PDF p.157〈149〉 | 4,000m（表2の幅の上端） PDF p.26 | NTSB |
| 亀裂の発見 | 2019-05-29・潜航前点検の操縦士・縦に約4フィート、周の約3分の1 PDF p.161〈153〉 | 2019年6月・48回目のあと・社員・"hairline" PDF p.26 | NTSB |
| 技術部長の承認拒否 | 2019年春（亀裂の前）。亀裂の後は COO に「修理できない」 PDF p.161〜162〈153〜154〉 | 亀裂の後、CEO に "done" PDF p.26 | NTSB |
| メリーランドの試験の後 | 最大3,000mに格下げ（de-rating）・施設は Bethesda PDF p.166〜167〈158〜159〉 | condemned（使用不可）・Annapolis PDF p.26 | NTSB（使用不可） |

## §5 一次資料の外・見つからないもの（④で裏を取るべき物）

**(a) 一次資料の外・見つからない**

| カット | 中身 | 判定 | ④でやること |
|---|---|---|---|
| pr03 | 副題「2023年9月30日 回収された証拠」 | 一次資料の外（`ref_CREDITS.md` の写真説明） | USCG の写真の公開情報で日付の裏を取るか、日付を外す |
| c109 | 見出し「中からは開かない」 | 見つからない（原文は「外から閉める」まで） | 裏が取れなければ「外からボルトで閉める」まで |
| c112 | 「15秒から20秒の遅れ」（語り・図） | 見つからない（2冊にこの幅は無い。USCG は15〜30秒） | 「15〜30秒」に直せば裏は要らない |
| c118 | ゲージの目盛り（60・180・200） | 見つからない | 画面に数として出るなら外す |
| c128 | 図の題「この数字が、その後の報道の時計になった」 | 一次資料の外（報道について） | 報道の裏を取るか削る |

**(b) 原文に無い解釈（判定は言いすぎ。④で削るか裏を取る）**

| カット | 中身 | ④でやること |
|---|---|---|
| pr10 | 図の注「この動画の数値と時刻は、すべてこの2冊による」 | (a) を直すまで言えない |
| c124 | 見出し「外の誰も、知らなかった」 | 原文は「USCG は潜航を知らなかった」（USCG p.40）まで |
| c125 | 札 ctx「外に伝えられたのは、この程度の情報だった」 | 削る |
| c126 | 「この時点では、その程度のことしか分かっていなかった」 | 削る |
