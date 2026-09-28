# 当て直し R1（第1〜6章 c101〜c623）＝16本目 ④'・ルール 4'-18

- 見た人：R1（直した係 G1〜G3 とは別の目）。2026-09-27
- 見たもの：`decisions.md`（§0〜§7）・`diff_v1_v2.md` L5〜L1325（変わったカット 88）・`changes_G1〜G3.md`・`daihon_v2.md` の c101〜c623（前後の聞き役のつながり）・`roles_G1〜G3.tsv`
- 原文の引き直し：`kwic.py -f q_R1.txt` を3回（S1 PDF26・39・49・72・74・77・85・89・90・93・94・96・97・99・148・163・166・171・174・175・179・217・220・224・225・232／S8 p.41・p.46／S9 PDF4・5・6・10・12・18／S10 PDF20）
- 機械の確かめ：c101〜c623 の字幕の行は全部40字以内（最大40）・聞き役は20字以内で数字0・★の行は第1版と全部同じ（差分0）・「ヴァイオント」は字幕と画の欄に0
- 判定：○＝問題なし／⚠️＝直したほうがよい／・＝案（採るかは G0）

## 所見のまとめ（🔴 0・⚠️ 3・・ 4）

| cut | 重さ | 何が問題か | 原文 |
|---|---|---|---|
| c418 | ⚠️ | 「望ましかったのだが」は原文 come poteva essere desiderabile（望ましかったかもしれない）より強い。かぎかっこの中の引用で poteva の留保が落ちている | S1 PDF179 |
| c513 | ⚠️ | 「山がいっぺんに崩れた場合」は原文 crollo istantaneo（一瞬の崩落）と違う。「いっぺんに」＝まとめて1度に、と聞こえ、c508（2つの塊を時間をずらして）と第2版で足した c510（最悪も、いつも2つの塊）に食い違って聞こえる。★c514「一瞬に」ともそろわない | S1 PDF163・PDF97・PDF224 |
| c109 | ⚠️ | 「水位は、湖の水面の標高のこと」で「標高」が先に出る。「標高」の説明（海面からの高さ）は c114。水位の説明が、まだ説明していない語に頼っている（係 Z の指摘どおり） | 用語の順（§6） |
| c513 | ・ | 聞き役の案：まとめ→反応「Q: 絶対、とまで書いたんだ。」。まとめ 19（30%の境）→18（28.6%）・反応 8→9。語り手の「そう。」が「最悪でも安全」を認める形に聞こえるのも消える。★c514 の前で問いが答えを先に言わない | — |
| c513 | ・ | 上と同じ直しを roles_G3.tsv に | — |
| c412 | ・ | 「短くまとめただけだ」の「だけ」は原文に無い評価。PDF77 の多数派は従属節（Dopo aver escluso che…）で触れている＝「短くまとめている」で差は伝わる。c419「どちらかに決めない」と合わせて中立に | S1 PDF77・PDF217 |
| c513 | ・ | 「国の監督の担当者」の初出が c513 に前倒しになったが、どこにいた人かの説明（ダムに置かれた）は c619 のまま。上の反応の案を採るなら「ダムにいた国の監督の担当者が、」で行は40字に収まる（案は反応の案に依るので patch なし） | S1 PDF163・PDF96 |

## カットごとの記録

### 第1章
| カット | 見たこと | 判定 |
|---|---|---|
| c105 | 「ゆっくり」＝PDF148「generale lentissimo movimento di un ampio tratto del versante」（lentissimo より弱い側＝強めていない）。PDF148 の段は「gli esperti della Commissione ministeriale confermano」＝国の調査委員会の専門家の引用で帰属は正しい（電力公社の続きは PDF148 の頭の30百万m³まで）。S9 PDF6「1960 … Maggio. Vengono installati i primi capisaldi」。1行40字・c101〜c106 は −1 | ○ |
| c106 | 文を割っただけ。【横から】・谷に沿った断面 | ○ |
| c108 | 「前もって見通すこと、予見」＝初出の一言。§3 と食い違わない | ○ |
| c109 | 1行目「水位700メートルなら安全と結論していた」＝PDF89「la relazione concludeva che la quota 700 può considerarsi di assoluta sicurezza」（「絶対に」は c511・c512 で言う）。2行目で「標高」が c114 より先に出る | ⚠️ |
| c110 | PDF26「La Commissione ha approvato — con 19 voti favorevoli e 8 contrari」・S10 PDF20「dopo i tre gradi di giudizio」＝「3回出た」 | ○ |
| c111 | S9 PDF18：1969「Non viene riconosciuta la prevedibilità della frana」→1971「inondazione aggravata dalla previsione dell'evento」。「最初と最後の判決で、予見についての答えは、大きく変わった」は §3 と合い、ca19「最初の判決から、予見についての答えは、大きく変わった」・cb12 とも食い違わない。「予見できなかった」とも「予見できた」とも言っていない。反応「ぎりぎりだったんだ」→「そう。」 | ○ |
| c112 | 248ページ | ○ |
| c113 | PDF99「Il Ministro dei lavori pubblici, con suo decreto dell'11 ottobre 1963 … costituì una Commissione di inchiesta」「A sua volta l'ENEL nominò il 1° novembre 1963 altra Commissione」＝「事故のあとにできた2つ」「公共事業大臣がつくった」は原文どおり | ○ |
| c114 | c109 で水位を言ったので念押しに。c109 を直せば「標高」の初出の説明はここ | ○（c109 と組） |
| c116 | 【上から】・合図あり（c106 横→c116 上） | ○ |
| c117 | 問い「まず、何から見ていくの？」に次の行「この谷とダムの形からだ」がそのまま答える | ○ |

### 第2章
| カット | 見たこと | 判定 |
|---|---|---|
| c201・c204 | 「バイオント」 | ○ |
| c202 | 1934年の地形図【上から】 | ○ |
| c203 | PDF49「Il 30 gennaio 1929 la Società idroelettrica veneta presentò domanda」＝最初の申請は別の会社。「この峡谷にダムを築いたのが…サーデ」は正しい | ○ |
| c207 | まとめ「つまり、湖が大きくなるの？」は c205・c206 を受ける＝語りが言ったことのまとめ。次は「そう。」 | ○ |
| c208 | PDF72「la quota raggiunta dai getti di calcestruzzo varia dal minimo di 704 metri al massimo di 716 … sotto il piano di coronamento」（1960-06-08）・S8 p.41「constructed between 1957 and 1960」＝§2 どおり「1960年まで続いた」。月は言っていない | ○ |
| c209・c211 | 【上から】（右に横からの反りを小さく）→【横から】＋合図 | ○ |
| c210 | 「学術の総説」の初出の一言。★は変わっていない | ○ |
| c214・c220 | 出典欄だけ | ○ |
| c215 | c116 との重なりを削った | ○ |
| c217 | PDF90「fu istituito l'Ente nazionale energia elettrica (ENEL)」 | ○ |
| c219 | 問い「何が起きたの？」に「1960年の秋、山の斜面の一部が、湖へ崩れ落ちた」がそのまま答える（PDF72） | ○ |

### 第3章
| カット | 見たこと | 判定 |
|---|---|---|
| c301 | 「水をためると、山はどうなるのか」＝試験を「山を見る試験」と言っていない | ○ |
| c302・c304・c306・c308・c312・c315・c316 | 向きの札。c302 横→c304 正面（合図あり）→c315 上（合図あり）。場面2＝【正面から】は §4 どおり | ○ |
| c303 | PDF148 の国の調査委員会の専門家（Commissione ministeriale）＝帰属は正しい。「のちに」 | ○ |
| c307 | 1行削っただけ | ○ |
| c308・c309 | まとめ「つまり、亀裂の内側が、動く塊？」は c308 の2行目（塊のふち）を受ける。c309 は「そう。」で受ける | ○ |
| c311 | PDF72「una parte si era staccata dallo spigolo più settentrionale del Toc, l'altra, di maggiori dimensioni, da una grande nicchia a valle della Pozza」＝「北のかどと、斜面の大きなくぼみ」 | ○ |
| c317 | PDF85「In data 5 ottobre 1961 … la galleria by-pass era stata ultimata … sino a quota 680」・S8 p.46「In October 1961, when the construction of the by-pass tunnel was completed」・S9 PDF10「10 maggio. La galleria di sorpasso è ultimata」＝「秋までに」で両方を満たす。役割 質問→反応（文は「？」のまま・次は「そう。」） | ○ |
| c319 | 「なると」 | ○ |
| c322 | §2 どおり「操れる？」。PDF77「regolare la velocità」。次の行「専門家の中にも、そう考える人がいた」がそのまま答える | ○ |
| c323 | 聞き役を外して語りに。c322 の「そのもとになった報告」を受ける | ○ |

### 第4章
| カット | 見たこと | 判定 |
|---|---|---|
| c401 | 「話を、1960年の崩落の前に戻す」＝c402（1960年6月）・c405（1960年2月）と合う | ○ |
| c403〜c405 | 【横から】。c405 PDF74「almeno per quanto riguarda i profili lungo i quali si è sperimentato … un potente supporto roccioso autoctono」＝「調べた所では、厚い岩の土台」。PDF174「I sondaggi suggeriti furono eseguiti … ma non trovarono traccia del supposto piano di appoggio」 | ○ |
| c406 | 1行削除・出典に PDF75 | ○ |
| c408 | 場面2【正面から】＋合図（c405 横→正面） | ○ |
| c411・c413 | 読点・文の切り方だけ。c413 の引用は PDF217 の「;」の前まで（第1版と同じ範囲） | ○ |
| c412 | PDF77 の多数派「Dopo aver escluso che i franamenti potessero venir arrestati mediante misure artificiali」（従属節）／PDF217 の少数派は全文を引く＝差は原文どおり。ただ「だけだ」が評価を足す | ・ |
| c414 | PDF85「sul piano teorico erano ritenuti, dal dottor Mueller e dal professor Penta, il mezzo migliore per controllare e regolare i movimenti franosi」＝「理屈の上では」を残した。PDF175「Penta, membro della Commissione di collaudo」・S9 PDF4（IV sezione del Consiglio Superiore が任命）＝「ダムを検査する国の委員」。まとめ「つまり、止められない？」→「そう。でも…」。行40字 | ○ |
| c415 | 問いに「届いたかどうかが、議会で争われた点だ」がそのまま答える | ○ |
| c418 | 1行目は第1版のままだが、PDF179「benché non consti che le relazioni siano state ufficialmente trasmesse, come poteva essere desiderabile」＝poteva の控えめな言い方が「望ましかったのだが」で言い切りになっている。2・3行目は PDF232「all'occultamento alle autorità, ai Prefetti, e al Genio civile … della relazione Ghetti come delle relazioni Semenza-Giudici e Müller」どおり | ⚠️ |
| c419 | 1行削除。問い「どっちが本当なの？」に「どちらかに決めない」が答える | ○ |
| c420・c421 | PDF220・S9 PDF5「si denunciavano le responsabilità della SADE e si segnalavano i pericoli … gli abitanti di Erto」・PDF39「il procedimento penale … per l'articolo pubblicato sull'Unità del 5 maggio 1959 e conclusosi con sentenza di assoluzione」＝「その記事で訴えられた」「無罪」は原文どおり | ○ |
| c422 | 画の欄だけ | ○ |
| c423 | PDF171「Prima della frana del novembre 1960 le corrispondenze pubblicate su « L'Unità » … Erto sul bordo destro … senza alcun cenno a pericoli sulla sponda sinistra dove si è verificato il disastro」＝帰属（多数派）・向き（右岸＝北）とも正しい。章の橋の問いは新しい事実なし | ○ |

### 第5章
| カット | 見たこと | 判定 |
|---|---|---|
| c502 | 「決して」＝assolutamente | ○ |
| c503・c505・c506 | 削除・「約260メートル」・S9 PDF18（Ghetti「per non aver commesso il fatto」） | ○ |
| c504・c507〜c509・c513 | 場面3＝【横から】で章の中の切り替えなし。c507 の前面の幅は語りだけ（§4） | ○ |
| c507 | PDF89「una fronte complessiva di 1,8 chilometri, dalla quota 600 alla quota 1200, avente nella parte centrale uno spessore di 200 metri」 | ○ |
| c509 | S9 PDF10「Le prove prevedono che, secondo l'interpretazione degli ingegneri SADE degli studi di Mueller, si tratti di due frane distinte」＝帰属「財団の年表によれば」つき・§2 どおり。問い「どうして…？」にそのまま答える | ○ |
| c510 | PDF89「sul presupposto di determinare gli effetti del più catastrofico prevedibile crollo franoso」＝「予想できる中で、最も破局的な崩れの影響を確かめる…前提」。PDF224（少数派）「tale catastrofico evento era previsto dal professor Ghetti sempre partendo dall'ipotesi che si trattasse di due frane distinte」＝帰属・「いつも」とも原文どおり | ○ |
| c512 | 切り方だけ（PDF89 の引用の範囲は同じ） | ○ |
| c513 | 25メートルの出どころ＝PDF163「nel rapporto 8 ottobre 1963 diretto dall'Assistente governativo ingegner Bertolissi … « è risultato che con il massimo invaso e con il crollo istantaneo della frana l'onda conseguente raggiungerebbe una altezza di 25 metri »」＝「事故の前日の報告」は正しい。3行目「いっぺんに」が crollo istantaneo と違い、c510 の新しい1文と食い違って聞こえる。まとめ→反応の案・「国の監督の担当者」の初出の説明 | ⚠️・・ |
| c517・c518 | PDF225「nella sua riunione del 30 aprile 1962 espresse il parere」・S9 PDF12「30 marzo … è del parere」＝日を言わず「春」。PDF89「La relazione segnalava poi l'opportunità di « esaminare sul modello convenientemente prolungato gli effetti … alla confluenza nel Piave »」＝勧めは原文どおり（目的＝もっと高い水位を許せるか、は言わないが、慎重さの勧めとも言っていない） | ○ |
| c519・c520 | c519 は PDF179「erano conosciuti alla Pubblica Amministrazione」。c520 は PDF89「il modello idraulico era stato visitato il 19 settembre 1961 dall'ingegner Padoan, Presidente generale del Consiglio superiore … e dall'ingegner Batini, Presidente della IV sezione da cui dipendeva il Servizio dighe, i quali si erano informati dell'andamento e dei risultati delle prove」＝訪問と「進み具合と結果を聞いた」は同じ段に1つの出来事として書かれている（2つの事実をつないだのではない）。PDF163 も同じ | ○ |

### 第6章
| カット | 見たこと | 判定 |
|---|---|---|
| c606 | PDF166「Resta, peraltro, un motivo di perplessità sul fatto che le prove su modello avevano indicato nella quota 700 il limite ritenuto di sicurezza …」は715の許可の段＝「この許可には『疑問が残る』」は §2 の向き。多数派は「breve, ma non affrettata istruttoria」とも書く＝「少数派は、もっと厳しい」で多数派が弱い側と伝わる。反応「越えるのに？」にそのまま答える | ○ |
| c607 | PDF226「Dal 10 aprile cominciava dunque il terzo invaso … partendo da quota 647,5」。「その少し前」＝c605 の5月4日より前 | ○ |
| c608 | PDF93「segnò accelerazioni non rilevanti nonostante che il livello del lago fosse ritornato a quota 700」。まとめ「前に速まった高さまで、戻った？」は c602（1962年は700で速まった）と c607 を受ける。「そう。」 | ○ |
| c609 | PDF93「Nella metà dell'agosto 1963, mentre il livello del lago saliva dalla quota 705 circa verso la quota 710, si manifestò un'accelerazione」＝「約」を残した | ○ |
| c610 | 「強く」＝S9 PDF14 esige | ○ |
| c611・c613 | 途中の値を削った。200÷6.5＝30.8＝「30倍を超える」 | ○ |
| c612 | 出典欄だけ。★は同じ | ○ |
| c614 | まとめ「あの崩落のときに迫っていた？」は1行目を受ける。「そう。ただ、まだ届いてはいない」（PDF93 senza però raggiungerli） | ○ |
| c615 | PDF94「non intendeva aumentare l'invaso fino a raggiungere la quota autorizzata di metri 715」 | ○ |
| c616・c617 | PDF79 の「eventualmente」＝「しみこんでいれば」、「内側から」を外した | ○ |
| c618 | 【横から】＋合図・1行削除。PDF96「da quota 710 … a quota 702,50 (8 ottobre 1963)」 | ○ |
| c619 | PDF96「Tali incrementi sono aumentati a fine settembre … a fine settembre, a 5 cm/giorno toccando oggi il valore di circa 10 cm/giorno」＝「9月の終わりにさらに増し、今日は1日約100ミリ」 | ○ |
| c621 | PDF96〜97「i tecnici della impresa elettrica già SADE … 2) hanno tempestivamente informato le Autorità competenti della situazione, per cui il Sindaco … ha emesso una ordinanza per la evacuazione di persone ed animali dalla zona pericolante」＝主語（会社）・つながり（per cui）とも原文どおり | ○ |

## 型ごとの確かめ（R1 の範囲）
1. 縮めた文と原文の語：c109・c303・c423・c509・c510・c513・c619 を1語ずつ当てた。ずれは c513「いっぺんに」（第1版からの語だが c510 の1文で食い違いが表に出た）
2. 並べた事実を因果に：c520（訪問と結果を聞いたこと）・c621（per cui）は原文が1つの段・因果で書いている＝問題なし
3. 比べの向き：c412（多数派＝短く・少数派＝そのまま）・c606（多数派も／少数派はもっと厳しい）は原文どおり
4. 引用の範囲：c413・c512 は第1版と同じ範囲。c418 は範囲でなく語気（poteva）が強まっている
5. 新しく足した頁：c105 S9 PDF6・c203 PDF49・c208 PDF72・S8 p.41・c317 S8 p.46・S9 PDF10・c405 PDF76・PDF148・c414 S9 PDF4・c421 PDF220・c509 S9 PDF10・c510 PDF224・c513 PDF163・c517 S9 PDF12・c518 PDF89・c520 PDF89・c606 PDF166・c615 PDF94・c621 PDF97＝全部 kwic で当てた。帰属（国の調査委員会／多数派／少数派1／財団の年表）はどれも正しい
6. 予見の言い方：c108・c110・c111 は §3 と合い、ca19・cb12 とも食い違わない
7. 聞き役：問いの次の行はどれもそのまま答える。まとめの次は「そう。」。20字以内・数字0。roles_G1〜G3.tsv の役割と文は台本と一致
8. 見る向き：第1〜6章の向きの切り替え（c116・c211・c304・c315・c408）はどれも合図あり。場面2＝正面・場面3＝横は §4 どおり
9. 行の長さ・★・語：40字を超える行0・★の行の差0・「ヴァイオント」0・死の語／煽り語の新しい出0

## 範囲の外の気づき（patch なし）
- `daihon_v2.md` の1行目（`v2_head.md` から）が「ヴァイオント・ダム災害 … 台本 第1版」のまま。R1 の範囲外＝G0 か節の当て直しの係へ
