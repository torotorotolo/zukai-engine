# G1 直した記録（第1章 c101〜c112・第2章 c201〜c220）

原文は全部 `kwic.py` で引き直した（問いのファイル `q_G1.txt`＋個別の引き）。

## 直した
- G1-01 c106 聞き役のまとめ「つまり、ずっと付いたままだった？」→「つまり、とても古いナットだった？」（±0・まとめのまま・次は「そう。」）。原文 AAB p31「all of the inserts showed evidence of age and reuse」・p41「had likely been installed for at least 26 years」・p16「The right elevator trim tab screws were also removed and reinstalled」で確かめた＝「ずっと付いたまま」は reuse と逆。出典欄に p31・p41 を足した。roles_G1.tsv も同じ文に
- G1-12 c103 聞き役「何が起きたの？」→「なぜ落ちたの？」（±0）。次の行（報道の見立て）がそのまま答える。roles_G1.tsv も
- G7-01 c103 同上（G1-12 と同じ直し）。slots_G7 の c103 案も同じ
- G7-02 c104「でも報告書の表では、」→「でも報告書では、」（−2字＝冒頭の余裕が増える）。AAB p28 本文「during the pitch-up maneuver, the maximum vertical load factor reached about 17.3 G」＝機首上げと最大Gは本文にある
- G1-13 c104 G7-02 で「の表」を外した＝「表の行に無い語（機首上げ）」の食い違いは消えた。「機首が上がり、」を削る案（−7字）は所見どおり採らない（通説との逆が聞こえにくくなる）
- G1-06 c102「傾き始めてから」→「崩れ始めてから」（±0）。AAB p28 の表 0秒「Airplane rounds pylon 8, begins to roll through 73° left bank」＝0秒で既に73度傾いている
- G1-14 c106 画の欄の鎖を「ナットの劣化 → ねじのゆるみ → かたさが落ちる → 板の震え → 棒が折れる → 機首上げ」に（本文0字）。AAB p52「the reduced stiffness of the elevator trim tab system that allowed aerodynamic flutter … The reduced stiffness was a result of deteriorated locknut inserts that allowed the trim tab attachment screws to become loose … a failure of the left trim tab link assembly, elevator movement」
- G7-05 c109 問い②の前提＝c106 の語りに「板の震え」を入れた（「そう。報告書は、そのナットから、板の震え、墜落までを、1本の鎖のようにつなぐ。」39字・AAB p52 aerodynamic flutter of the trim tabs）。問い③を問いの形に＝「そして、観客席との距離は、足りていたか。」（+4字）。「のか。」の3連（mech15 §4 が数える）を避けて3つ目は「か。」
- G1-20 c109 同上（3つ目を問いの形にした）
- G7-04 c108 2行目を「駐機場は、飛行機を止めておく広場。燃料を積んだ車も止まっていた。」に（+9字）。「駐機場」の初出で一言。燃料車は AAB p19「a fuel truck was parked on the ramp near the pits」。1行目（ボックス席の噛み砕き）はそのまま
- G1-10 c201 重なりを削った＝「2011年9月16日。ステッド空港の空は、よく晴れていた。」「気温は摂氏22度。西南西の風が吹いていた。」（−7字）。AAB p16「weather observing system at RTS … clear sky conditions below 12,000 feet agl, temperature 22°C」「wind was from 240°」。所見の案「ネバダ州リノは、よく晴れていた」は、観測がステッド空港（RTS）のものなので「ステッド空港の空は」にした（範囲を広げない）。「ネバダ州」は c201 から消える（c101「アメリカのリノ」・c112 で足りる）
- G7-07 c201 同上（「会場は、…ステッド空港」の言い直しを消した）
- G1-04 c204「塔の「パイロン」」→「柱の「パイロン」」（±0）。#33 p9（p2009）注4「Course pylons are constructed out of a barrel mounted at the top of a telephone pole measured at a height of about 50-feet」。出典欄に #33 p9 を足した。E85 の副題は下の「⑤bで原寸」
- G1-05 c207「約4.5秒前に…約8.8秒前に…」→「約4.5秒先を2位のヴードゥー、約8.8秒先を1位のストレガが飛んでいた。」（+6字）。AAB p10「trailing the second-place airplane … by about 4.5 seconds and the lead airplane … by about 8.8 seconds」。G1-05 の「秒差で」は述語が無いまま残るので、G7-09 の述語つきの形を採り、時制を c205「回っていた」に合わせて「飛んでいた」
- G7-09 c207 同上
- G1-15 c209「滑走路の南の端に引いた線」→「滑走路の南の端の線」（−3字）。AAB p17「the showline located on the south edge of runway 8/26」
- G1-03 c210 1行目「…FAAの条件は、水平に500フィート。」→「…FAAの条件は、水平の距離で決まっていた。」（+2字）。★は変えない。500フィートは語りから外した（c818 で括弧つきで出る・門番 check_script の単位の網は原単位にだけ鳴る＝メートルだけの★は E にならない）。出典欄に AAB p16（「The FAA issued a certificate of waiver or authorization on September 2, 2011, to enable the NCAR」）を足した。p17「no closer than 500 feet horizontally from the primary spectator areas for all aircraft」。G1-03 の案「水平の距離だった。」（−2字）でなく G7-10 の形にした＝「った。」で終わる文を増やさない（mech15 §4 が数える）
- G7-10 c210 同上
- G1-02 c213「配置の上では、満たしていた。」→「線の北を飛べば、満たしていた。」（+1字）。AAB p19「Racing airplanes were expected to fly parallel to the showline on the north side」＝前提を聞かせる形
- G7-11 c213「それは第8章で。」→「それは、あとの章で。」（+2字）。c817 の「第2章の終わりで触れた」は G6 の担当（申し送り）
- G7-13 c216「速さと力は」→「速さとGは」（±0）。AAB p29「true airspeed and vertical load factor during its final turn around pylon 8 … were similar to its speeds and load factors during its previous two turns」＝力＝G（c104 で噛み砕き済み）
- G7-06 c110「調べた資料を集めて公開した「ドケット」と合わせて、」→「調べた資料の束と合わせて、」（−12字）。「ドケット」は語りでこの1回だけ（概要欄の出典の「NTSB 公開ドケット」はそのまま）
- G1-09 c107 出典欄を「AAB p11・p12・p35・#17 p2」に（本文0字・noflag）。AAB p12「The accident pilot raced the airplane in the NCAR from 1983 through 1989」
- G1-07 c208 本文はそのまま。§9 の申告の行を add_G1.md に書いた（午後4時15分ごろ＝1625−10）
- G1-11 §6 の読みの候補を add_G1.md に書いた（c213 の「第8章」は消えたので外した・この版で足した語も足した）

## 一部だけ採った
- G7-03 c106「板の震え」を語りに入れたのは採った。反応「そんなに前から…。」に替えて「そう。」を取る案は採らない（決め＝G1-01 のまとめのまま）。行を40字以内にするため「つないでいる」→「つなぐ」（語り +3字・行39字）。slots_G7 の c106 案も同じ扱い
- G7-14 c218「傾き始め」に揃える案は採らない（決め＝0秒の出来事は語りでは「横転」）。初出の噛み砕きを採った＝「そう。そして、機体が急に横へ回る「横転」の、約8秒前。」「エンジンの圧力と回転が、目に見えて下がった。」（+13字・文を割って行を1つ足した）。決めの言い方「横にくるりと回る」は、原文 AAB p11「in less than 1 second, the airplane rolled from its established approximate 73°-left-bank turn to about 93° left bank」・p39「a rapid left roll upset」＝一回転ではないので「急に横へ回る」にした（④'が「くるりと」にするなら差し替えは1語）。AAB p29「About 8 seconds before the beginning of the upset, there was a noticeable reduction in engine manifold pressure and rpm」＝起点は合う。出典欄に p11・p39 を足した
- G1-17 c218 同上（初出の問題は噛み砕きで解いた。「崩れ始める」への揃えは決めにより採らない）
- G1-08 c206 本文は残した（決め）。出典欄だけ「一般の事実（新幹線の営業最高 時速320キロ）」に（noflag）。⚠️ mech15 §2 が「文書名で始まらない札」に c206 を1件数える（第1版の「—」は数えなかった）＝④'で許すか決める。⑥の前に新幹線の最高速度を1回確かめる（所見の案のまま）

## 不採用
- G7-15 c218 決め＝直さない（c218 の「報告書は、その理由には触れていない。」で閉じている）
- G7-12 c214「いちばん上の組」は原文に無い。AAB p38 は「the lowest heat in the class」「the unlimited class gold race」と言うだけ、p8・p10・p39・#33 p2 も gold race の名だけ＝足すと新しい事実（任意の所見）
- G7-08 c205 カットの並びは変えない（decisions §0）。「さかのぼると、」（+7字）は、c208「事故の、およそ10分前だった」・c214「3日前の予選」が自分で時を名乗っているので足さない（任意の所見）
- G1-16 c205 直さない。台本は報告書の数（AAB p10「about 445 knots as it passed pylon 8」）で正しい。勧告書 A-12-08 p1 の 460ノットの段落は、c902 で画面に出すとき映さない（⑤b・所見の案のまま）
- G1-18 c217「エンジンの力を示す圧力」は原文 p29 に無い言い換え（manifold pressure の説明）＝新しい説明を足すことになる。所見も「直さなくてよい」
- G1-19 c212 所見どおり直さない（c815 の燃料車への伏線で2回目も要る）

## ⑤bで原寸
- G1-04 c204 E85 を原寸で見る。写っている「上に審判が立つ物」が、電柱の上の樽のパイロン（#33 p9 注4）か、パイロンの横の審判の台かを見る。台なら副題を「パイロンと審判の台」に（materials.md の記述は「パイロン（鉄塔）と上に立つ審判2人」）
- G1-03 c210 quote の画面に「500フィート」を小さく添えるか決める（語りからは外した）
- c108 画の欄の #33 図13（p2015）は c814 でも使う（G6-07 と同じ図）。燃料車・ボックス席・事故地点が原寸で読めるかを見る。c814 と同じ絵が2回になるなら、どちらかを AAB p20 図3 の切り出しか Googleアースに

章の字数 第1版 → 第2版：c1 579 → 581（正味 +2字・うち c101〜c105 は −2字＝c105 の終わり 45.0秒 → 44.6秒〈mech15 §8〉）／c2 1,171 → 1,185（正味 +14字）／計 1,750 → 1,766（正味 +16字・上限 +50 の内）
