# g4_c6 照合記録（台本 第1版 684〜775行＝第6章 c601〜c622）

- 照合日：2026-09-24（④' の検証役・書いた人とは別）
- 原文：`ref/ep13/src/thy_pages.txt`（頁タグ付きの写しを scratchpad `thy_tagged.txt` に作って grep）
- 画像は1枚も開いていない。絵の中身が要るものは「要画像」と書いた
- 判定：✓＝原文どおり／△＝語は在るが意味・強さ・帰属がずれる／✗＝原文に無い・原文と逆／—＝照合対象外（日本語・構成）

---

## c601 図 p5001 ／ SB p5001・p5003
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| SB 52-37は、3つの貨物ドアの錠の部品を取り替え | p5003（C. Description Group I (1)）・p5006（2.C）・p5003（B. Reason） | "Replaces strike plate and adjusts pins and switches on the forward, center, and aft cargo doors." ／ "Replace striker and adjust pins and switches." ／ Reason: "the lockpin tube will deflect and contact the lockpin limit switch striker, giving a false door closed, latched, and locked indication." | △ 取り替えるのは strike plate＝striker。Reason の文と仏 p87（図6の札 "STRIKER (POUSSOIR)"・"LOCK LIMIT WARNING SWITCH"）・p68 "le poussoir (striker) du 'unlock limit switch'" から、**警告灯のスイッチを押す部品**と読める（推測を含む。図6の絵は見ていない）。「錠の部品」はぼかしすぎ。c317（警告灯のスイッチ）と結べる |
| ピンとスイッチの位置を調整する改修だ | p5003 | "adjusts pins and switches" | ✓ |
| 図 p5001「SB 52-37の1頁目」 | p5001・p5002 | p5001="This page transmits ~evision 2 for DC-10Service Bulletin 52-37"（改訂2の送り状・1972-08-25）／p5002="DOORS- Cargo - Modify And Adjust Door MechanismAssembly." "Page 1 of 6" | △ p5001 は送り状。題と対象機の一覧が載る「1頁目」は p5002 |

## c602 図 p5003 ／ SB p5003・p5006
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 後ろの貨物ドアには、さらに支えの板を取り付ける | p5003・p5006・p4002（AD 74-08-04）・仏 p67・p80・英 p1034・p1041・p1051 | SB: "Installs support and plate on aft cargo door." ／ "Aft cargo door only - Install plate, support, jumper, and attaching parts." ／ 仏 p67: "Ie palier suWlem:ntaire prew pour Ie "torqu: tube" de la "vent door" par Ie SB 52-37 n 'avait pas ere installe" ／ p80: "Le palier suppl€m=n-taire prevu en apt?lication du SB 52-37 (fig. 6) a precis€ment pour but de s'0P.?Oser a cette defonna.tion."（＝通気扉の torque tube のたわみを止めるため） | △ 語は合う（上院 p2053 は "support plate"。SB は support と plate の2部品）。**何を支える板か**が本文に無い＝c314「ピンを動かす軸が、たわんでしまう」の軸（図7 "FLEXION DU TORQUE TUBE"）を支える板だと仏報告は書く。つなげれば第6章の「肝心の板」が中学生に分かる |
| 扱いは「推奨」。すすめるだけで、命令ではない | p5003・p2041 | "D. Compliance: Recommended." | ✓ |
| 図 p5003（後部ドアに支えと板） | p5003 | "(2) Installs support and plate on aft cargo door." | ✓（文字の頁。板の絵は仏 p87 の図6に在るか＝要画像） |

## c603 panel ／ 上院 p2051
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 議会の証言によれば、52-37の調整を済ませたドアは、ピンが入っていないと、ハンドルを倒すのに約113キロ（250ポンド） | p2051 | "When those things were done, the force required to close the vent door without the latch pins in position would have been 250 pounds" | ✓ 数・換算（113.4kg）は合う。△ 帰属：話し手は**ダグラス社の社長ブリゼンディン**（メーカー自身）で、レーカー機の話の流れ。「議会の証言」では誰の見方か分からない。紹介（c614）より前に数だけ先に出る |
| 調整の前なら、約54キロか約68キロ（120か150ポンド） | p2051 | "rather than the 150 pounds or 120 pounds prior to any work on the part the Bulletin 37 called for" | ✓ |

## c604 panel ／ 上院 p2041・仏 p67
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| SBには、改修する機体の一覧が付いている。そこにトルコ航空の機体は無い | p2040・p5002（一覧）・仏 p67 | 一覧の胴体番号に 29 は無い（AA/CO/NA/UA＋Group II の AA 48,49,51・LT 47）／p67 "(1) Le BE 52-37 ne mentionne pas dans les avions concemes le TC-JAV" | ✓（ただし SB は1972-07-03・改訂2は08-25。トルコ航空への転売が決まったのは1972年9月＝国会 p6154。SB の時点で「トルコ航空の機体」はまだ無い＝言い方は「のちのトルコ航空の機体（29号機）」が正確） |
| 一覧に無い機体は、引き渡す前に工場で改修する、と書かれていた | p2041・p5003・仏 p67 | "Affected aircraft other than those listed above will be modified prior to delivery or included in a subsequent revision to this Service Bulletin." ／ p67 "la modification prevue aurait, en effet, du etre effectuee en usine avant la livraison" | △ SB の文は「引き渡し前に改修する**か、SBの後の改訂で一覧に加える**」の二択。後半を落として一択にしている（「工場で」は仏 p67 の言葉で SB の文には無い） |

## c605 実写 C6 ／ 上院 p2051
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 1972年6月、のちのトルコ航空の機体は、まだロングビーチのダグラスの工場にいた | p2051 | "the aircraft was still on the Douglas assembly line at Long Beach and had yet to be delivered to the Turkish Airlines in the June 1972 period" | ✓ |
| 実写 C6（1974年8月・CC BY 3.0） | materials.md 93行 | 「1974年8月・ダグラスのロングビーチ工場で引き渡し前の DC-10＝事故機が改修を受けたはずの場所と年」 | △ 副題の年（1974年8月）は正しく書いている。ただし materials.md の「場所と**年**」は誤り（改修は1972年・写真は事故の5か月後）。写っているのは大韓航空の機体（ファイル名）。副題に航空会社も |

## c606 実写 A3 ／ 仏 p27・p65・上院 p2052
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 工場での呼び名は、胴体29号機 | p65・p2052・p2040 | p65 ドアの刻印 "sIN 46704/11 FG 401 … FIN 29" ／ p2052 "it indicates the No. 29 airplane, which was the Turkish airplane" ／ p2040 "*Mfr's Fuselage No." | ✓ |
| 製造番号は46704 | p27 | "nO de serie 46.704." | ✓ |
| 登録記号TC-JAVを付けて飛ぶ、この機体 | p27 | "Imnatriculation TC:-JAV." | ✓ |
| 実写 A3（1973年・額装） | materials.md 63行 | A3＝尾部のエンジンと「TC-JAV」・撮影「同」＝1973年夏・ヒースロー・BY-SA | ✓ |

## c607 panel ／ 国会 p6210
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 1976年の日本の国会で語られた | 対応表 p6210＝1976-06-09・石黒規一（三井物産株式会社顧問） | — | ✓ |
| ロッキード事件を調べる、衆議院の特別委員会 | thy_pages の本文に委員会名は無い（URL 107703814X006… と facts_japan.md の記載だけ）。同じ日の発言に「ロッキード」が多数（p6112・p6114・p6119） | — | ✓（委員会名は本文で未確認）。— 面A：「ロッキード事件」の初出に一言の説明が無い |

## c608 panel ／ 国会 p6210
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 証言したのは、三井物産の顧問 | 対応表 | 肩書「三井物産株式会社顧問」 | ✓ |
| うそを言わないと誓ったうえでの証言だ | p6101〜p6223 を「宣誓・誓・偽証・証言法」で探して0件 | 全体では p6266（別の日・別件）に「議院における証人の宣誓及び証言等に関する法律違反」、p6177 に予算委の証人喚問での宣誓の話だけ | △ 出典欄の p6210 に無い。取り込んだ発言は #20 以降で、宣誓の場面（冒頭）が入っていない。法律上は宣誓が原則なので事実としてはほぼ確かだが、原文ファイルでは確かめられない |
| 全日空に売るつもりで、DC-10を6機、確定の注文で押さえていた | p6210・p6152・p6002 | p6210 "三井物産の判断でファーム、確定注文を六機に、それからオプションを四機に変更いたしております" ／ p6152 "三井物産が全日空のために確定注文何機それからオプション何機を持っている" | ✓。— 面A：「確定の注文」の噛み砕き（§1-5・§8 は「取り消さない前提で出す注文」）が本文に無い |

## c609 panel ／ 国会 p6152
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| ただし、全日空が注文したわけではない。証人は、全日空は一度も「発注する」とは言わなかった | p6152 | "全日空が発注するというようなことは一度もおっしゃいませんでした。ただ、認知されてないまま三井物産が全日空のために確定注文何機それからオプション何機を持っているということは、全日空の方々は知っておられました。したがって、責任は持たないけれども…好ましいことと判断しておられました" | △ 前半は✓。**直後の逆接「ただ、…全日空の方々は知っておられました／好ましいことと判断」を切っている** |

## c610 panel ／ 国会 p6220
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 機体ができる時期が、全日空が使いはじめる予定より、早すぎた | p6220 | "われわれの用意している飛行機の納期が非常に早い。それで導入がだんだんとおくれてきて、四十九年になる…二年もその間にギャップがあるわけです" | ✓ |
| 三井物産は1971年5月から、ほかの買い手を探した | p6220・p6114 | p6220 "大体昭和四十六年の五月ごろ" "四十六年の五月から売り込みにかかりまして" ／ p6114 "私の方が転売を始めたのは四十六年の五月からでございます" | ✓（昭和46年＝1971年） |

## c611 panel ／ 国会 p6153・p6154
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 決まったのは、イギリスのレーカー航空とトルコ航空。3機ずつだった | p6220・p6153・p6154・上院 p2051 | p6220 "最終的にこのレーカーとトルコ航空に決めた" ／ p6153（坂井委員の問い）"トルコ航空、レーカー航空それぞれ三機ずつ転売" ／ p6154 "レーカーの方が二機と一機と分かれておりまして…最後の三機目は四十九年の一月" ／ p2051 "Laker Airways in Britain" | ✓（「3機ずつ」は議員の問いの言葉。レーカーの3機目は1974年1月＝29号機の引き渡し時点ではレーカーは2機） |
| トルコ航空の3機は、1972年9月に決まった | p6154 | "トルコ航空の方は三機とも一緒に四十七年の九月であったと思います。正式契約は、契約書的なものは若干それからずれておると思います。" | △ 証人の「〜と思います」と「正式契約は若干ずれる」を落として断定（軽） |

## c612 panel ／ 国会 p6132・p6130・p6148
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 同じ日、議員は6機の製造番号を読み上げた。その中に46704がある | p6132（#199 野間友一） | "米国三井物産を介して注文された六機、これの番号も調べてみますと四六七〇四、七〇五、七二七、それから四六九〇五、九〇六、九〇七、この六機になっておる" | ✓ |
| 証人は5けたの番号は知らないと答えたが | p6130（#192）・p6131（#198）・p6134（#200） | p6129（#191）"この六機のシリアルナンバーは御存じでしょう。"→p6130 "存じておりません。" ／ p6131 "そんな大きなけたの番号はいまだ耳にしたことはございませんで…私が知っているのは、全日空向けの二九番、三三番というような番号は知っております" ／ p6134 "残念ながら全く存じておりませんでした。"（＝日航の先の注文についての答え） | △ 中身は✓。ただし「知らない」は**読み上げ（#199）の前**の答え（#192・#198）。台本の並び（読み上げた→知らないと答えた）は順が逆。いちばん強い根拠 p6131 が出典欄に無い |
| 確定の注文に「29番」を挙げていた | p6148（#236）・p6131 | p6148 "確定注文の六機は、二九番、三三番それから四七番それから五〇番、八三番、八七番でしたか、なかなか正確に覚え切れないので困っておるのですが" | ✓（証人は「でしたか」とあいまい。p6131 でも「全日空向けの二九番」） |

## c613 panel ／ 国会 p6126・p6002
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 日本向けに作られた仕様を、トルコ向けに一部改装したとも述べている | p6126 | "日本向けにつくられた仕様を一部トルコ向けに、あるいはレーカーの場合もそうですけれども、改装するために費用がかかっている" | ✓（赤字の説明の中の言葉） |
| 1972年3月の国会でも、議員が「29番」の機体に触れていた | p6002（1972-03-24 楢崎弥之助） | "この一二井物産が注文したこれらの飛行機の一連番号は、二十九番、三十三番、四十七番、五十番、七十八番、この五機" | ✓ |

## c614 図 p2051 ／ 仏 p27・上院 p2051
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 1972年12月、29号機はトルコ航空に引き渡された | p27・p2051・p2052 | p27 "Date de livraison : 10.12.72." ／ p2051 "delivery to the airline, which took place in December of 1972" | ✓ |
| ダグラス社の社長ブリゼンディンは、議会でこう述べている | p2014・p2036・p2051・p2053 | p2014 "Mr. John Brizendine, president of the Douglas Air­[craft]" ／ p2053 公聴会＝"March 27, 1974" | ✓ |

## c615 panel ／ 上院 p2051
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 社長は、パリで見つかったドアから、改修の大事な部品が1つ欠けていた、と伝えられている | p2051・仏 p64 | "It has been reported from Paris that a key part of one of the modifications to the cargo door, which I will discuss later, was found missing upon inspection of the aft cargo door located at the accident site." ／ p64 ドアの破片は Saint-Pathus（本体の15km手前） | △ 「パリ」は知らせの出どころ（reported from Paris）。ドアが見つかった場所ではない（サン・パテュス） |

## c616 ★ ／ 上院 p2051
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| ★製造の記録では、改修はすべて済んでいた | p2051 | "According to our manufacturing records, all service bulletins that had been issued to improve the cargo door latching mechanism had been incorporated in the Turkish Airlines aircraft prior to its delivery." | ✓（語句・帰属＝記録は合う）。△ 範囲：原文は「貨物ドアの錠を直すSBはすべて」。★単独だと機体の改修全部に聞こえる（軽）。18字＝20字以内 ✓・最後の行 ✓ |

## c617 実写 D1 ／ 上院 p2051
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 社長は、この食い違いを、いまは説明できないと述べている | p2051 | "At this time we are unable to satisfactorily explain this discrepancy, but we are continuing to investigate this matter." | ✓（「調べを続けている」は落としている） |
| 52-37のほかの作業は一部済んでいたが、肝心の板だけが無かった | p2051・仏 p67・p78〜p81・p102・p104・英 p1051〜p1052 | p2051 "the parts on the Turkish airplane indicated that parts of Bulletin 52-37 had been accomplished on the Turkish airplane, although the part in question was not present" ／ p104 "application partielle du Service Bulletin 52-37, - rrodifications et reglages incorrects ayant notam-ment conduit a une protrusion insuffisante des broches" ／ p1052 "the incomplete application of modification SB 52 7 (absence of support pjaic specified) and the adjustments found on measurement tO be incorrect (lock pins and $triker)" | ✗ 「だけ」は原文に無い。仏の報告は板の欠落**と**調整の誤り（ピン・スイッチを押す部品）を並べる。さらに「一部済んでいた」と「だけが無かった」は文の中で食い違う（一部しか済んでいないなら、無いのは板だけではない） |
| 実写 D1 | materials.md 94行 | "ロングビーチ空港のダグラス（ユナイテッド機）"・撮影年の記載なし | △ 副題に年が無い（ルール：副題に撮影年） |

## c618 panel ／ 上院 p2052・p2055・国会 p6153
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 引き渡しの前の改修の工程で、29号機の隣にいたのは、レーカー航空の機体だった | p2052 | "The Turkish airplane and the Lakers airplane were side by side, not in production, as was indicated yesterday, but in our predelivery modification." | ✓ |
| 同じころ、同じ人たちが作業し | p2052・p2053 | "The work was accomplished at about the same time, and by the same people, according to the inspection stamps on our records." ／ "The manufacturing records are stamped with the stamps of both individuals for the aircraft" ／ p2053 "We have been unable to identify the Manufacturing Mechanic who was assigned to install the support plate" | △ 原文は「記録の検査の印によれば」。印は検査員と副職長のもので、作業した人は特定できていない（c619 と食い違う） |
| その機体も52-37を全部は済ませていなかった | p2051・p2055 | p2051 "The same discrepancy was also found as to another aircraft and the part has since been installed on that aircraft." ／ p2055 "Lakers Airways operation of a DC-10 which we later learned had not been completely modified in conformance with Service Bulletin 52-37." | ✓ |
| レーカー航空は、三井物産の6機のうち3機を買った会社でもある | p6153・p6154 | 上の c611 と同じ | ✓（隣の機が三井の6機のどれかとは言っていない＝言い過ぎていない。参考：SB 52-37 の一覧で LT 46905＝胴体47、SB 52-38 で LT 46905・46906＝47・50。証人の挙げた6機に 47・50 が在る＝推測としては三井の機体の可能性が高いが、上院は番号を言っていない） |

## c619 panel ／ 上院 p2053
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 書類に「板を取り付けた」と印を押したのは、品質の検査員と、製造の副職長の2人 | p2053 | "the Quality and Reliability Assurance Inspector and the Manufacturing Assistant Foreman whose stamps appeared on the paper work indicating that the support plate had been installed on the THY DC-10" | ✓ |
| 取り付けるはずの整備士は特定できず | p2053 | "We have been unable to identify the Manufacturing Mechanic who was assigned to install the support plate on the aircraft." | ✓（— 面A：「整備士」は c2 の「同乗の整備士」「主任整備士」と同じ語で別の人。工場の作業員） |
| 2人は検査の仕事から外された | p2053・p2052 | "These two individuals have been removed from any work involving inspection and they have been given reprimands." | ✓ |
| — 読み | — | 「印を押した」＝いん／しるし | 面E |

## c620 panel ／ 仏 p67・p80
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| フランスの報告書は、これをメーカーの見落としとしている | p67・英 p1051 | "Par suite d'un oubli du cons-tructeur, l'avion a ete livre sans la modification" ／ "this oversight had not been detected at the time of delivery" | ✓（p80 には無い。p67 の脚注） |
| 報告書の試験では、ピンを動かす管の調整が、7.95ミリ足りなかった | p78・p79・英 p1040 | p78 "Ces cotes ont ensuite ete reportees sur les elements correSIX>n-dants d' une porte de l'rI€!'re type pretee par ~ Donnel Douglas, sur laquelle Ie palier supplementaire prevu par Ie SB 52-37 avait ete supprime" ／ p79 "Ie lock tube avait sur ce TIDntage une position de verrouillage insuffisante de 6,35 + 1, 6 = 7, 95 rrm." | △ 数は✓。7.95ミリは「試験で作った条件」ではなく、**事故機のドアの残骸で測った調整棒の長さを、同じ型の新しいドア（板を外したもの）に写した結果**。「報告書の試験では」だけでは起点が伝わらない |
| （書いていないこと） | p80 | "Lorsque ce reglage est confonne aux prescriptions du cons-tructeur … il est hu-naine:nent inp::>ssible de forcer la poignee meme en I'absence du palier supplemantaire (SB 52-37)." | 構成：正しい調整なら板が無くても人の力では閉まらない、と報告書は書く。台本はこれを言わない＝板だけが原因に聞こえる |
| — 面A | c314 | c314「ピンを動かす軸」（torque tube）／c620「ピンを動かす管」（lock tube） | 別の部品を同じ「ピンを動かす」で呼んでいる |
| — 読み | — | 「管」＝くだ／かん | 面E |

## c621 ★ ／ 仏 p80
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| その状態で、ハンドルを倒してみると | p80 | "Lors des essais effectues (avec Ie reglage du lock tube insuf-fisant de 7,95 mn)" | ✓ |
| ★ハンドルは、約22キロの力で閉まった | p80・英 p1041 | "la poignee a pu etre ainsi fennee ( et la vent cb:>r apparemnent close) avec un effort de 22 da.l\l (environ 50 Ibs)" | ✓（22daN≒22.4kg重）。18字 ✓・最後の行 ✓。△ ★単独では「ピンが入っていないのに」が落ち、ふつうのことに読める（軽） |

## c622 panel ／ 上院 p2034・仏 p80・p148
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 報告書は、この力を「およそ50ポンド」と書く | p80 | "(environ 50 Ibs)" | ✓ |
| 表示板が示した線と、ほぼ同じ力だ | p2034 | "“Do not apply more than 50 pounds of force to handle when closing.”" | ✓（数の比べとしては合う）。ただし p2034 の6月19日の電報は "This supersedes our telegram dated 16 June 1972" で、項目（1 点検／2 SB 52-27・A52-35／3 暫定）に表示板が無い。TC-JAV に50ポンドの表示板が付いていたという記述は仏・英の報告に無い（placard／plaque／plaquette／etiquette／pancarte／lbs／pound で探して、p80・p1041 の試験の力と p67 の「手動開放の説明板」だけ） |
| 係員の手ごたえも、いつもどおりだった | p148・p150 | p148 "j 'ai pu alors fe~mer ce levier, sans plus d'effort que d'habitude." ／ p150 "Je n 'ai pas l'impression d'avoir developpe un ef-fort important. J 'ai appuye, sur la poignee, avec une seule main." | ✓（供述＝係員の言葉） |
| 約23キロの目安では、異常に気づけなかった | p80・p81・p104・上院 p2052 | p81 "L'appaPence extePieUI'e … ne permet-tait pas, sans inspection visuelle paP le hublot pPevu acet effet, de suspec-tep une mauvaise fermetuPe." ／ p2052 "anyone who is at all familiar with the door knows that if the force is high, or greater than approx-imately 30 pounds, something is wrong" | ✗ 原文に無い推論を断定（反実仮想）。報告書が言うのは「外見からは、のぞき窓で見ないかぎり疑えなかった」。表示板との関係は報告書に無く、表示板がこの機体に在ったかも不明。ダグラスの証言は逆向き（ふつうは約30ポンド＝それを超えたらおかしいと分かるはず） |
| 1974年3月3日、その機体が、オルリーを飛び立つ | — | — | ✓ |

---

## 所見の数
- 重 2（c617「だけ」／c622「気づけなかった」）
- 中 7（c604 二択の片方を落とす／c609 逆接を切る／c618 同じ人たち／c620 7.95の起点／c620 正しい調整なら閉まらない を言わない／c622・c516〜c519 表示板は6月19日に消えている）
- 軽 残り（言い方・読み・素材の副題・出典欄）

## 実名の線（④' の判断材料・所見ではない）
- 証人＝石黒規一（三井物産株式会社顧問・p6126 ほか）。議員＝野間友一（c612 の読み上げ p6132）・楢崎弥之助（c613 の1972年 p6002）・坂井弘一（c611 の問い p6153）
- ブリゼンディン（メーカーの社長・議会で証言）を実名にしているのと、同じく公の場で宣誓して証言した石黒顧問を役割だけにしているのは、並べると線が揺れて見える（判断は本チャット）
