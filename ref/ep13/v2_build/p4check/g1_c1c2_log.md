# g1_c1c2 照合記録（台本 第1版 228〜382行・c101〜c222）

- 照合日：2026-09-24／照合者：④'の検証役（書いた人とは別）
- 原文：`ref/ep13/src/thy_pages.txt`（頁は通し番号）。頁の取り出しは scratchpad `p4check/pg.py`（読むだけ）
- 画像は1枚も開いていない。文字の層で決められないものは「要画像」と書いた
- 判定：✅合う／⚠️ずれ（所見あり）／—出典なし（構成の行）

## 第1章

### c101 ／ 仏 p5・p12
| 行 | 当てた頁 | 原文の断片 | 判定 |
|---|---|---|---|
| 1974年3月3日、日曜日の昼 | p5 | `Dimanche 3 mars 1974 / peu avant 11.42` | ✅（11.42 UTC＝12.42 パリ＝昼） |
| パリの北東37キロの森に、旅客機が落ちた | p12 | `a 37 kIn dans Ie nord-est de Paris` | ✅ |
| 346人は、全員が亡くなった | p5・p13 | `Tues : 346`／`Il n'y a pas de survivant a bordo` | ✅ |

### c102 ／ 仏 p104 ／ 実写 B1
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 原因は…貨物室のドア／飛んでいる最中に外れた | p104 | `Llaccident resulte de llejection en vol de la porte cargo arriere gauche` | ✅ |
| B1＝1997年の破片・CC BY 4.0 | materials.md l.77 | `1997年5月、現場で撮られた機体の破片`・CC BY 4.0（Ian Abbott） | ✅ |

### c103 ／ 仏 p105・上院 p2017
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 約2年前にも | 日付の差 | 1972-06-12（p2017）→1974-03-03＝1年8か月19日 | ⚠️ 軽（「約2年前」は1.72年の切り上げ。章名は「約」も落ちる） |
| 同じ型の旅客機で | p2017 | `American Airlines, Inc., McDonnell Douglas DC-10-10` | ✅ |
| 同じ位置のドアが空中で外れていた | p2017・p2046 | `aft bulk cargo compartment door separated from the aircraft in flight at approximately 11,750 feet`／p2046 `The aft left-hand cargo door opened` | ✅（後部・左・飛行中に分離） |
| 結論の最後に | p100・p105・p106 | p100 `CONCLUSIONS - 5.1`／p104 `5.2.CAUSES`／p105 の最後の段落の次が p106 `6 - RECOMMANDATIONS`／英 p1053 は最後の段落の直後に署名 | ✅（第5章の最後の段落） |
| ★危険は、前の事故ですでに明らかだった | p105・p1053 | `L' ensenble de ces risques ayait deja ete mis en evidence, dix neuf nois auparavant lars de I'accident de WINDSOR, mais cette oonstatation n'avait pas ete suivie de mesures correctives efficaces.` | ⚠️ 中（「mais…」＝有効な対策が続かなかった、の半分を切った。c104 の「それでも」が別の資料の別の主張で埋めている。「ces risques」は床の通気と操縦ケーブルの通し方を含む＝ドアだけではない） |

### c104 ／ 上院 p2030・p2055 ／ 実写 A2
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 直すことは、アメリカ政府の命令にならなかった | p2030 | `An AD relating to the rear cargo door on the DC-10 was not issued until a few days after the fatal Turkish Airlines crash` | ✅ |
| 決めたのは、役所のトップとメーカーの社長の、電話1本だった | p2030・p2055 | p2030 `Apparently, three days after the June 12, incident, the then-Federal Aviation Administrator, John H. Shaffer telephoned Jackson McGowen` … `according to testimony of Arvin Basnight`／p2055 `the Administrator, pursuant to an oral agreement with the president of Douglas Aircraft, decided to address the problem with a company service bulletin, followed up by a telegraphic communication from the FAA to the airlines` | ⚠️ 中（原文は Apparently＋西部地域局長の証言による伝聞。上院の結論は「長官が、社長との口頭の合意にもとづき、SB と航空会社への電報で対処すると決めた」＝決めたのは長官・電報も出た。台本は断定で「電話1本」が決めたと言う） |
| 役所のトップ | — | FAA の初出は c406 | ⚠️ 軽（どの役所か、ここでは分からない） |
| A2＝TC-JAV の離陸・1973年・額装 | materials.md l.62 | `TC-JAV (6004629408).jpg`・離陸の瞬間・1973年夏 | ✅ |

### c105 ／ 国会 p6016・p6024
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 乗客のうち48人は、日本人だった | p6016（運輸大臣）・p6024（土井議員） | p6016 `日本人が四十九名、一名はまだ確認されていないそうでございます`／p6024 `日本人の乗客四十八人` | ⚠️ 軽（48は議員の数か49−1の引き算。§1-4 の方針「確認できた人で48人」の限定が本文で落ちた） |
| その多くは、春から銀行や商社で働くことが決まっていた、若い人たち | p6016・p6024 には無し → p6007・p6028 に在る | p6007 `さつき会の入社内定者のヨーロッパの研修旅行`・`東海銀行十六名、トーメン入社予定者が十五名、中央信託銀行六名、千代田生命一名`／p6028（小平議員）`日本の若いエリートが四十数名`・`入社は決定いたしておりますけれども、まだ正式社員でない` | ⚠️ 中（出典の頁違い。「春から」はどの頁にも無い＝推測。「若い」は議員の言葉） |

### c106 ／ 国会 p6210・p6132・p6126
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 1976年の国会の記録によれば、もとは日本向けに作られていた | p6126（石黒証人） | `日本向けにつくられた仕様を一部トルコ向けに` | ✅ |
| 日本の商社が、全日空に売るつもりで注文した6機の、1機 | p6210（証人）・p6132（野間議員）＋仏 p27 | p6210 `三井物産の判断で`…確定注文6機／p6132 `米国三井物産を介して注文された六機…四六七〇四`／仏 p27 `nO de serie 46.704` | ⚠️ 軽（「この機体＝6機の1機」の結び付けは議員の読み上げ＋仏 p27 の製造番号。p27 を出典に足す。証人は5桁の番号を知らないと述べている＝facts_japan C4 #192） |

### c107 ／ —
構成の行。✅（事実の主張なし）

### c108 ／ —
構成の行。✅

### c109 ／ 上院 p2014
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 旅客機の半ドアは、地上では何も起こさない | p2014 | `On May 29, 1970, while conducting a ground pressurization test … the forward cargo door had been improperly latched and the door came open due to the cabin pressure loads.` | ⚠️ 軽（出典の頁は「地上の与圧試験で半ドアが開いた」話。条件＝地上では機内に空気を詰めていない、を言わないと出典と逆に聞こえる） |
| 機内の空気が、ドアを外へ強く押す | p2014 | `came open due to the cabin pressure loads` | ✅ |

### c110 ／ 仏 p15・p60
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 報告書に載った墜落の現場の写真／矢印は機体が入ってきた向き | p15 | `Photographie aer1--enne de la zone d'impact" en foret d'Ermenonville" prise face a l'est. La fleche materialise l'axe d'arrivee du DC-10` | ✅（題に「航空写真・東向き・矢印＝進入の軸」が文字で在る。画像不要） |
| 長さ700メートル、幅100メートルほどの切れ目 | p60・p13 | p60 `une saignee longue de quelques 700 m sur une centaine de metres de largeur`／p13 `700 m x 100 m` | ✅ |

### c111 ／ 仏 p1・英 p1001・上院 p2005
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| フランスの事故調査委員会の報告書 | p1 | `RAPPORT FINAL DE LA COM~ISSION D'ENQUETE Fevrier 1976` | ✅ |
| アメリカ上院の調査報告 | p2005 | `REPORT ON THE OVERSIGHT HEARINGS AND INVESTIGATION OF THE DC-10 AIRCRAFT … COMMITTEE ON COMMERCE UNITED STATES SENATE JUNE 1974` | ✅ |

### c112 ／ 仏 p5
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 報告書の時刻は世界時／1時間足したパリの時刻 | p5 注 | `Les heures figurant dans ce rapport sont expnmees en temps univeroseZ. IZ convient d'ajoutero une heure pour obteniro Z'heuroe legaZe fran/laise` | ✅（「世界時」の噛み砕きが無い＝⚠️ 軽 面A） |

## 第2章

### c201 ／ 仏 p9 ／ Googleアース イスタンブールの空港（現在）
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| イスタンブールを出て、オルリーに寄り、ロンドンへ | p9 | `vol TK 981 "ISTANBUL-PARIS-IDNDRES"` | ✅ |
| 素材＝イスタンブールの空港（現在） | 原文に空港名なし（grep `Istanbul` は都市名だけ） | — | ⚠️ 軽（推測：1974年の発着はイェシルキョイ＝のちのアタテュルク空港。いまの「イスタンブール空港」（2018〜）は別の場所。⑤bで取り違えない） |

### c202 ／ 仏 p27 ／ 実写 A1
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| ダグラス社が作ったDC-10 | p27 | `Consb:ucteur : M::: OONNELL OOUGIAS CDR!?`（McDonnell Douglas Corp.） | ✅（上院 p2014 `Douglas Aircraft Company, a division of the McDonnell-Douglas Corporation`＝部門名として可。所見にしない） |
| エンジンが3つある大型機 | p12（`reacteurs 1 et 3`・`reacteur n O 2`） | 一般知識の範囲 | ✅ |
| 1972年2月に初めて飛び、12月にトルコ航空に引き渡された | p27 | `Date du premier vol : 27.2.72. Date de livraison : 10.12.72.` | ✅ |
| A1＝TC-JAV の地上走行・1973年・額装 | materials.md l.61 | `1973年夏・ヒースロー`・地上走行 | ✅ |

### c203 ／ 国会 p6154 ／ 実写 D5
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| トルコ航空は、この型を3機まとめて買っていた | p6154（石黒証人） | `トルコ航空の方は三機とも一緒に四十七年の九月であったと思います` | ✅（証人の「と思います」の留保は軽い。所見にしない） |
| D5＝TC-JAU・1974年7月・フランクフルト・額装パネル | materials.md l.98 | `Douglas DC-10-10 TC-JAU THY FRA 28.07.74`・CC BY 3.0・1054px | ✅（事故の後の写真＝副題に年が要る。台本の欄には在る） |

### c204 ／ 仏 p9 ／ Googleアース オルリー
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 午前11時2分／時刻表どおりに | p9 | `se pose a Orly a 10.02, confonn€ment a l'horaire du vol TK 981` | ✅（10.02 UTC＋1＝11:02） |
| 南ターミナルの西にある、A2という場所 | p9・p43 | p9 `au point A2 du satellite OUest de l'aerogare Orly-Sud`／p43 `Le point A-2 est situe devant la face rord de la jetee qui prolonge 1 'aerogare "Orly-Sud" en direction de 1 'ouest` | ✅ |
| 167人のうち、50人がパリで降りた | p9 | `167 passagers sont a bard, 50 d Ientre eux slarretent a Paris` | ✅ |

### c205 ／ 仏 p9・p46
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 代わりに、ロンドンへ向かう200人あまりが乗りこんだ | p9・p46 | p9 `Deux cent dix sept nouveaux passagers`／p46 `216 passagers a destination de Londres ont ere atbarques` | ✅（数）／⚠️ 軽（「代わりに」＝50人と入れ替わったように聞こえる） |
| 英国航空とエールフランスから回ってきた、出発まぎわの客が大勢 | p9 | `nanbreux voyageurs de derniere minute en provenance des corrpagnies British Ail:ways et Air France` | ✅ |

### c206 ／ 仏 p9・p29〜p30 ／ 実写 D6
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| そのため、1時間の停留が1時間30分に延びた | p9 | `La duree nonnale d Iescale est d Iune heure, mais sera portee a une heure trente, en raison de 11 enbarquanent de nanbreux voyageurs de derniere minute` | ✅（因果は原文に在る。p5 `en retard sur I'ooraire ?ar suite de I' ernbarquenent de nanbreux pa.ssagers de derniere heure` も同じ） |
| 客室の席は、ほぼ埋まっていた | p29〜p30 に席数なし → p35 | p35 `la repartition des 332 passagers sur les 345 sieges que aomporte la aabine` | ✅（中身）／⚠️ 軽（出典の頁違い：席数は p35） |
| D6＝フィンエアーの DC-10 と乗客・CC BY 4.0 | materials.md l.99 | `題の「1970」は年代の可能性` | ✅（台本は「1970年代」。推測：フィンエアーの機体は -30 型。所見にしない） |

### c207 ／ 仏 p46・p47 ／ 実写 C2
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 荷物の積み下ろしと、燃料の補給が進んだ | p45〜p47 | p47 `L I avitaillanent en carbureacteur a debute a 10 h.15 et s lest tenn:ine a 10 h. 30.` | ✅ |
| 後ろの左の貨物室は、下ろすだけで、何も積まなかった | p45〜p46 | p46 `(la soute a ete entierenent videe de sa charge)`・`11 n Iy a eu aucune charge (fret ou bagages) ernbal:qUee dans cette saute.` | ✅（見出し「Soute arriere」は p45。出典に p45 を足すとよい） |
| C2＝KLM・1972年・CC0・荷物車と作業員 | materials.md l.88・l.87 | 同じシリーズ C1 が1972年 | ✅ |

### c208 ／ SB p5003
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 床の下の荷物の部屋・ドアが3つ | p5003・p157 | p5003 `on the forward, center, and aft cargo doors`／p157 `Ceci est valable pour les trois partes de saute` | ✅ |
| 後ろの左側のドア | p104 | `porte cargo arriere gauche` | ✅ |

### c209 ／ 仏 p10・p43・p147 ／ 実写 オルリー（未見）
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 午前11時35分ごろ | p10・p46 | p10 `La fenreture de la porte desservant la soute arriere gauche intervient vers 10.35.` | ✅（10.35 UTC＋1） |
| 空港で荷物を扱う会社の係員 | p45・p144 | p45 `nanutentionnai..res "arr:ineurs/soutiers" … W\HM:XJDI`／p144 `Manutentionnaire` | ✅ |
| パリの空港公団から、仕事を請け負っていた会社 | p43 | `1'assistance aeroportuaire proprenent dite etait assures par 1'Aeroport de Paris et son entreprise sous-traitante, 1a Societe SAIDR.` | ✅ |
| 1968年からこの会社で | p147・p144 | `Je suis entroe a "la SAMOR "le 16 aout 1968` | ✅ |
| 素材＝オルリー出発ロビー1970 | materials.md l.47・l.102 | `Departure hall at Paris-Orly airport (LBS SR04-038169).tif（1970）`＝BY-SA・未見 | ⚠️ 軽（在庫には在る。ただし語りは駐機場のドアの話で、絵は客の出発ロビー） |

### c210 ／ 仏 p146・p148 ／ panel 係員の供述（1974年3月6日）
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 事故の3日後、調べに対してこう話している | p144〜p146 | p146 `3. Le 6 mal'S 1974 Signe : MAHMOUDI`（証言は p144 の頁1〜p146 の頁3） | ✅（日付は3月6日の証言のもの） |
| スイッチを押し、ドアが下りて収まり、カチッと鳴るまで押し続けた | p148 | `J'ai actionne l'interrupteur, la porte est descendue normalement et s'est mise en place. J'ai maintenu l'interrupteur baisse jus-qu'a ce que j'entende le declic` | ⚠️ 中（中身は p147〜p149 の「Complements aux declarations」＝3月6日の署名の後に綴じた別の文書。文字の層に日付なし。3月6日の証言 p145 は `j'ai appuye sur Ze bouton electrique, la porte est descendue et elle est venue se mettre en place, des qu'elle est en place un declic se produit … puis j'ai actionne le levier`＝「押し続けた」は無い）。要画像：補足の日付 |

### c211 ／ 仏 p148 ／ panel 係員の供述（続き）
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 錠のレバーを倒そうとしたが、立つ位置が悪かった | p148 | `J 'ai voulu baisser le levier de verrouillage, mais je n'etais pas en bonne position.` | ✅（語句）／⚠️ 中（c210 と同じ：「続き」は3月6日の証言の続きではなく補足） |
| 少し動いてから、いつもより強い力は使わずに、レバーを閉めた | p148 | `J'ai da me depla-cer legerement sur le tapis et j 'ai pu alors fe~mer ce levier, sans plus d'effort que d'habitude.` | ✅（「使わずに」は sans plus d'effort の直訳として合う。「要らなかった」ではない） |

### c212 ／ 仏 p146 ／ quote
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 供述は、こう結ばれている | p146 | 署名の直前の文 | ✅（3月6日の証言の結び） |
| ★ドアを閉めたとき、私にはすべて正常だった（20字） | p146 | `Je suis l'este envil'on 1/4 d'heul'e dans Za soute amel'e gauahe, je n 'ai !'ien l'emarque d'ano1'maZ, je n 'ai senti auaune odeul' bizal'l'e, je n 'ai pas aonstate de ahaZeU1' ano1'male … et pOUl' moi tout etait n01'maZ ZOl'Sque j 'ai fe1'me Za pOl'te de Za soute.` | ✅（語句）／⚠️ 軽（「すべて」は貨物室の中＝におい・熱・異常の話の結び。ドアの錠についての本人の断言は p145 `Je suis formel, la porte etait bien fermee`） |

### c213 ／ 仏 p94 ／ 図（模式図）
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| このドアの下には、小さなのぞき窓 | p94・p151・p156・p105 | p94 `"Regard" par lequel peut s 'effectuer la verification de l'engagement des broches`／p156 `un trou situe en bas de cette porte`／p105 `Ie diametre, a I 'epoque insuffi-sant, du hublot` | ✅ |
| 中のピンが正しく入ったかを、外から確かめる | p94・p104 | p104 `un hublot de controle etait destine a pennettre une verification visuelle de 11engaganent de ces broches` | ✅（中身）／⚠️ 軽 面A（「ピン」の初出。ロックピンの説明は c307） |

### c214 ／ 仏 p149 ／ quote
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| この窓について聞かれ、こう答えている | p149 | `Question - Connaissez-vous l'existence d'un oeil de controle de la fermeture ?` | ✅（補足の問答。日付は言っていない＝問題なし） |
| ★あの小窓が何のためか、知らなかった（16字） | p149 | `Je ne savais pas a quoi cet oeil servait.` | ✅（直前 `j'ai vu les mecaniciens de la compagnie regarder par ce trou avec une lampe electrique` と矛盾しない） |

### c215 ／ 仏 p149
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 閉め方を、文書で指示されたことは一度も無かった | p149 | `Je n'ai jamais eu de consignes ecrites pour la ferrneture des portes.` | ✅（「文書で」＝ecrites が原文に在る） |
| 会社の誰からも、のぞき窓について教わっていなかった | p149 | `Jamais personne a la SAMOR ne m'a donne ni de consignes, ni d'indications.` | ✅（語句）／⚠️ 軽（直前の p148：閉め方は職長 CANOT が実演して教えた＝口頭の訓練はあった。言わないと「何も教わらなかった」に聞こえる） |

### c216 ／ 仏 p46・p156〜p157
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| トルコ航空がオルリーに置いていた主任整備士 | p156・p23 | `Chef Mecanicien THY - escale d'Orly`／p23 `Ie mecanicien permanent de la THY a Paris` | ✅ |
| 毎便、窓からピンを確かめていた | p156〜p157（本人の証言・1974-04-12） | `c'est d ce momenf;-ld que je verifie la bonne fermeture … en regardant par un trou situe en bas de cette porte`／`Cette visite se fait systematiquement a taus les va ls.` | ⚠️ 中（本人の証言を地の文の事実として言っている。職長 p151 は反対のことを言い、c217 はそちらだけ「と話している」を付ける） |
| ピンは白く光って、よく見えるという | p156 | `Le "lock pin" est blanc et briZZant et se voit assez bien.` | ⚠️ 軽（assez bien＝「かなり／まあまあ」。同じ頁に「後ろへ2〜3m下がれば地上から見える。見えなければ脚立と懐中電灯」） |

### c217 ／ 仏 p23・p46・p151
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 荷物の会社の職長は、その確認は毎回ではなかった | p151（DUMAS・1974-04-11） | `Cette verifiaation n 'est pas systematique. EUe est seulement pratiquee quelquefois.` | ✅（弱め：原文は「ときどきしか」。⚠️ 軽） |
| 研修でイスタンブールに行っていて、いなかった | p23・p46・p157 | p23 `se trouvant a Istanbul ?Our narticiper a un cours d'instruction technique`／p157 `J'etais a Istanbul du 10 fevrier au 14 mars 1974.` | ✅ |

### c218 ／ 仏 p23・p46
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 代わりに、イスタンブールから同じ機体に、整備士が1人 | p23・p46・p157 | p23 `H. ucaR avait ete embarque a bard du TC-J1W »Our Ie rerrnlacer`／p46 `un autre mecanicien avait ere €!Obal:que au depart de ce dernier aeroport` | ✅（「代わりに」の因果は原文 pour le remplacer に在る） |
| その整備士が窓を確かめるのを、見た人はいない | p46 | `personne n Ia vu ce mecanicien au un autre nenbre d I~page proceder, au rroyen du hublot prevu a cet effet, a l'inspection des broches dent le non engagement n Ia done pas ete oonstate` | ⚠️ 軽（「ほかの乗員も」が落ちた） |

### c219 ／ 仏 p46・p18
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 作業のあとで窓をのぞくには、足場を置き直す必要があった | p46 | `cette operation aurait, d'ailleurs, neoessite, une fois Ie travail de M. Ml\HMXJDI tennine, la mise en place d'un dispositif d'acces.` | ⚠️ 軽（原文は条件法「〜を要したであろう」・mise en place＝置く（「置き直す」ではない）。主任整備士 p156 は「地上から2〜3m下がれば見える」） |
| 乗員の1人として981便に乗っていた | p18・p23・p157 | p18 乗員 `12`／p157 `Il est reparti dans l'avion a destination de Londres.` | ✅ |

### c220 ／ 仏 p9・p10
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 昼の12時30分30秒 | p10 | `Ie decollage a lieu sensiblement a. 11.30'30"` | ✅（UTC＋1） |
| 東へ向かって滑走路を飛び立った | p10・p47 | p10 `autorisation d'Orly-sol pour rouler vers la piste 08`／p47 `seuil de la piste de decol-lage 08` | ✅（滑走路08＝東向き） |
| ドアが閉められてから、およそ55分後 | p10 | 10.35 → 11.30'30" | ✅ |

### c221 ／ 仏 p46・p148
| 行 | 頁 | 原文 | 判定 |
|---|---|---|---|
| 係員は、いつもどおりに閉めた。手ごたえにも、おかしなところは無かった | p148・p150 | p148 `sans plus d'effort que d'habitude`／p150 `Parce que la poignee de la porte est bien rentree dans son logement sans difficulte.` | ⚠️（本人の証言を地の文で断定） |
| 報告書の本文も、係員はいつもどおり閉め、異常に気づかなかったと書いている | p46・英 p1027 | p46 `par M. MlUiMXJDI qui a declare avoir procede, ccmne a llordinaire, sans difficulres parti-culieres et n Iavoir constate aucune aranalie.`／p1027 `has stated that [he] proceeded usual` | ⚠️ 中（本文は「本人がそう述べた」と書いている。報告書が自分の判断として書いたのではない） |

### c222 ／ —
橋の行。✅

## 章名（ルール4-11）
- 第1章「2年前にも外れていたドア」：本文は「約2年前」、日付の差は1年8か月19日 → ⚠️ 軽（「2年近く前」なら章名も本文も合う）
- 第2章「その日のオルリー」：c201〜c222 はオルリーの到着〜離陸 → ✅

## 読み（面E・§6 の表に無いもの）
- `A2`（c204）：エーツー／エーに の2通り
- `3つ`（c107・c202・c208）：みっつ／さんつ
- `6機の、1機`（c106）・`3機`（c203）：ろっき／ろくき、いっき／いちき

## 章の範囲の外で気づいたこと（所見には入れない）
- 「ウィンザー」の本文の初出は `c317`（台本 453行「ウィンザーの調べでは…」）で、何の事故かの紹介は `c416`（541行「カナダのウィンザーの近くで…」）＝紹介より先に名前が出る（g2 の担当範囲。第1章 c103 は名前を出さず「前の事故」としている）
