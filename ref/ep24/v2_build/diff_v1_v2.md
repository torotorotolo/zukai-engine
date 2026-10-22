# 第1版 → 第2版の対照（24本目 ④'・直したカットだけ）

- 行頭 `-` が第1版、`+` が第2版。`id` は差し替え表 `patches24.json` の番号（所見の id）
- 原文は `python ref/ep24/v2_build/pg24.py page S1 21` ／ `find S1 語` ／ `find all 語` ／ `find K1 語` で引ける（頁＝PDF頁／印刷頁）

## c105
- id `G1-002`：S1-付属書I p.53／43「during the physical startup of Ignalina Unit 1 and that of Chernobyl Unit 4」＝2つの炉で見つかった。「などの」で片方を落とさず、帰属は §4 の「1991年の委員会」の言い方にそろえた（字は差し引き−1・c105 の終わりは46秒の内を fcheck で確かめる）（B）
```diff
-> 止める棒の形にも、欠陥があった。ソ連の委員会の1991年の報告によれば、
-> それは事故の2年半ほど前、この4号炉の起動の試験で見つかっていた。
+> 止める棒の形にも、欠陥があった。1991年のソ連の委員会によれば、
+> それは事故の2年半ほど前、この4号炉などの起動の試験で見つかっていた。
```

## c107
- id `G1-013`：c104 の1986年と1992年の報告＝新旧。§3-1 で c205 は「主に3つ」になるので数を言わない形がよく、c206 の「1つずつ取り出して」との繰り返しも消える（−3字）（C）
```diff
-> では、何が4号炉を壊したのか。2つの報告を、
-> 事故の夜の時刻に沿って、1つずつ並べていく。
+> では、何が4号炉を壊したのか。新旧の報告を、
+> 事故の夜の時刻に沿って、見比べていく。
```

## c202
- id `G1-017`：c314・c716 で「キエフ」を使う断りが要る。首都は「町の名」より「地名」が合う（+1字）。ウェブ R3・R4 は §3-19 で G0 が原文どおりと確かめた（C）
```diff
-> この動画では、事故の名として広く知られた呼び方を使う。
+> この動画では、事故の名も地名も、広く知られた呼び方を使う。
```

## c205
- id `G1-014`：§3-1 のとおり「主に3つ」にし、1986年8月のソ連の報告は c217 で名乗る（F1-001）。出典の欄の does not retract の片は残す（c106 の語りと組）（C）
```diff
-> この動画で追うのは、3つの報告である。1986年の報告、
+> この動画で追うのは、主に3つの報告である。1986年の報告、
```

## c206
- id `G1-011`：7つはこの動画の選び方（INSAG-1 の表の違反は6行・0時28分は S2 では「運転員の誤り」＝c4 の語りも同じ）＝「取り上げる」で選んだことを言う（+3字）（B）
- id `G7-012`：7つの「違反」は1986年の2つの報告（S2 p.27・S3 p.26）から取る＝「最初の報告」では S3 と INSAG-1 のどちらか迷う。数字なし・先取りなし（字は増えない）（A）
```diff
-> Q: 最初の報告は、運転員の何を違反と言ったの？
-> 主なものは7つある。試験の計画から、残しておく制御棒の数まで。
+> Q: 事故の年には、運転員の何が違反とされたの？
+> 主なものを7つ取り上げる。試験の計画から、残しておく制御棒の数まで。
```

## c209
- id `G1-016`：「反応」の初出＝核分裂と結びつける（c210・c212 の「反応」が分かる）。黒鉛＝減速材（S1-付属書II p.113 graphite moderator）・物理として誤りなし（+2字）（A）
```diff
-> 黒鉛は、ウランから飛び出す中性子という粒を遅くして、反応を続けさせる。
+> 黒鉛は、ウランが割れて出る中性子という粒を遅くし、割れる反応を続けさせる。
```

## c211
- id `G7-013.1`：§3-2＝「定格」を語りで使わず「最大の出力」（S2 p.9 full power）。「出力が」の後なので「最大の」で言い、画の欄の札もそろえた（字は増えない）。§6 の「定格」の行は不要（G6）（A）
- id `G7-013.2`：§3-2＝「定格」を語りで使わず「最大の出力」（S2 p.9 full power）。「出力が」の後なので「最大の」で言い、画の欄の札もそろえた（字は増えない）。§6 の「定格」の行は不要（G6）（A）
```diff
-**c211** ／ 図 模式（出力と炉の性質＝定格のおよそ20%より下で、出力が上がるとさらに上がる向き＝目盛りの下の端を赤く） ／ S2 p.9／~4（`becomes positive below approximately 20% of full power`）
+**c211** ／ 図 模式（出力と炉の性質＝最大の出力のおよそ20%より下で、出力が上がるとさらに上がる向き＝目盛りの下の端を赤く） ／ S2 p.9／~4（`becomes positive below approximately 20% of full power`）
-> 1986年の報告も、そこを書いている。出力が定格のおよそ20%より下だと、
+> 1986年の報告も、そこを書いている。出力が最大のおよそ20%より下だと、
```

## c212
- id `G1-009.1`：S1 p.14／4「inserted into the reactor core from above, except for 24 shortened rods」＝「主に上から」。同じ行の G7-014（止める棒と制御棒が同じと言う）を1つにまとめ、語順を替えて字を抑えた（+2字）。本数は §5 で割れるので言わない。画の欄の札も「主に」（B）
- id `G1-009.2`：S1 p.14／4「inserted into the reactor core from above, except for 24 shortened rods」＝「主に上から」。同じ行の G7-014（止める棒と制御棒が同じと言う）を1つにまとめ、語順を替えて字を抑えた（+2字）。本数は §5 で割れるので言わない。画の欄の札も「主に」（B）
- id `R1-004`：S2 p.132／~125「all absorber rods (except for the shortened rods)」・S1 p.14／4＝止めるときに入るのは上からの棒＝211本ぜんぶが止める棒ではない（B）
```diff
-**c212** ／ 図 模式（上から差し込む制御棒＝211本・一番上から一番下まで18秒＝砂時計） ／ S1-付属書II p.113／103（`consists of 211 movable solid absorber rods`）・S1 p.14／4（`when starting from the upper limit stop switches, was 18 s`）
-> 反応をおさえるのは、上から差し込む制御棒である。全部で211本。
+**c212** ／ 図 模式（主に上から差し込む制御棒＝211本・一番上から一番下まで18秒＝砂時計） ／ S1-付属書II p.113／103（`consists of 211 movable solid absorber rods`）・S1 p.14／4（`when starting from the upper limit stop switches, was 18 s`）
+> 反応をおさえる制御棒は、全部で211本。止めるときに入る棒は、上から差し込む。
```

## c213
- id `G1-022`：S3 p.19／15 tests were to be carried out on turbogenerator No. 8＝意味は同じで「試験」の繰り返しを消す（−3字）（A）
```diff
-> その前に、8号タービンを使った試験をすることになっていた。
+> その前に、8号タービンを使って試すことになっていた。
```

## c215
- id `G1-021`：c214 の「それを確かめる試験だった」の言い直し＝消しても c215 は「なぜポンプか」を言い切る（S1-付属書II p.121／111 と食い違わない・−13字）（A）
```diff
-> 止めたあとの炉でも、燃料は熱を出し続ける。だから冷やす水を、
-> ポンプで送り続けなければならない。そのための備えの試験である。
+> 止めたあとの炉でも、燃料は熱を出し続ける。
+> だから冷やす水を、ポンプで送り続けなければならない。
```

## c217
- id `F1-001`：§3-1・§4＝1986年8月のソ連の報告（S3）は c217 で初めて名乗る＝初出は「1986年8月の」（c205 の「1986年の報告」＝INSAG-1 と耳で分ける）
```diff
-> 1986年のソ連の報告は、計画はきちんと作られておらず、
+> 1986年8月のソ連の報告は、計画はきちんと作られておらず、
```

## c218
- id `G1-008`：S1-付属書I p.61〜62／51〜52＝承認すべきは General Designer・Chief Design Engineer・Scientific Manager・regulatory body、規則はこれらの組織の承認を求めていなかった＝「設計者や規制側の」で限定を戻す（国より原文の regulatory body に近い）。出典の欄に2つの片を足した（+4字）（B）
```diff
-**c218** ／ イメージ Pexels（今の発電所の中の長い廊下か制御盤＝「イメージ：現在のチェルノブイリ原発」・映像方針で選ぶ・字と顔を原寸で見る） ／ S1-付属書I p.62／52（`there is nothing wrong with the programme itself`・`did not require the plant managers to obtain approval for such tests`）
+**c218** ／ イメージ Pexels（今の発電所の中の長い廊下か制御盤＝「イメージ：現在のチェルノブイリ原発」・映像方針で選ぶ・字と顔を原寸で見る） ／ S1-付属書I p.62／52（`there is nothing wrong with the programme itself`・`did not require the plant managers to obtain approval for such tests`・`from the aforementioned organizations`）・S1-付属書I p.61／51（`should be approved by the General Designer`）
-> そもそも当時の規則は、こうした試験に承認を求めていなかった、と。
+> 当時の規則は、こうした試験に、設計者や規制側の承認を求めていなかった、と。
```

## c219
- id `G1-001`：§2 のとおり。S3 p.19／15「the section on safety measures was drafted in a purely formal way」＝ソ連の報告（INSAG-1 には無い）（B）
```diff
-> 1986年の報告も、安全の節は形だけだった、と書いていた。
+> 1986年のソ連の報告も、安全の節は形だけだった、と書いていた。
```

## c220
- id `G1-003`：S1 p.34／24「unapproved changes in the test procedure were deliberately made on the spot」＝deliberately を落とさない（+1字・原文の強さのまま）（B）
```diff
-> 承認のないまま、その場で計画が変えられたことだった。
+> 承認のないまま、その場でわざと計画を変えたことだった。
```

## c221
- id `G1-015`：§3-1＝c221 は数を言わない（ここで割れる3つは S3・付属書I・INSAG-7 で c205 の顔ぶれと違う・−3字）（C）
```diff
-> そう。1つ目から、3つの報告の見方は割れている。
+> そう。1つ目から、報告の見方は割れている。
```

## c223
- id `G1-012`：S3 p.19／15 と付属書I p.61／51（the 1986 programmes provided for disconnection of the ECCS）がそろって書く事実への驚きに替え、計画を責める言い方（c218 の委員会の見方と逆に寄る）を外した。係の案の「冷却まで」は限定が外れて全部の冷却を切ると聞こえる＝「非常用の」を残した。反応のまま（−1字）（C）
```diff
-> Q: そんな計画で、試験をしようとしたなんて。
+> Q: 非常用の冷却まで切る計画だったなんて。
```

## c301
- id `G1-010`：1時ちょうどは S3 p.20／16（at exactly 1:00 hours）と S2 p.28／~25（At 01:00 on 25 April）がそろう・1時6分は付属書I の表＝「ソ連の報告」だと区別がつかず §4 の呼び分けにも外れる。出典の欄に2つの片を足す（+3字）（B）
```diff
-**c301** ／ 図 模式（25日の未明の4号炉＝出力の針が下がり始める・画面の時刻「1:06」） ／ S3 p.20／16（`at exactly 1:00 hours`）
+**c301** ／ 図 模式（25日の未明の4号炉＝出力の針が下がり始める・画面の時刻「1:06」） ／ S3 p.20／16（`at exactly 1:00 hours`）・S2 p.28／~25（`At 01:00 on 25 April`）・S1-表I-I p.63／53（`Start of reactor power reduction`）
-> ソ連の報告では、1時ちょうど。点検のため、炉を止める準備である。
+> 1986年の報告では、1時ちょうど。点検のため、炉を止める準備である。
```

## c302
- id `G7-017`：§3-3＝ORM を語りから外し「残した棒」で言う（§8 の概要欄には残す＝G6・−2字）（A）
- id `R1-006`：1カットに「ここで」「ここでは」＝c202 と同じ「この動画では」（A）
```diff
-> 制御棒の量である。運転反応度余裕、ORM という。
+> 制御棒の量である。この動画では「残した棒」と呼ぶ。
```

## c303
- id `G7-018`：S1-付属書I p.89／79「not less than 26-30 rods」＝「少なくとも26本から30本は残す」は同じ意味で、幅と否定の重なりが消える（字は同じ・40字）（A）
```diff
-> ふだんは26本から30本より少なくしない。15本まで減ったら、すぐ炉を止める。
+> ふだんは、少なくとも26本から30本は残す。15本まで減ったら、すぐ炉を止める。
```

## c304
- id `G1-019`：語りの31本・1,600メガワットの根拠は表I-I p.63／53 の01:06・03:47 の行（片は文字の層に当たることを find で確かめた）（B）
```diff
-**c304** ／ 実写 Commons c3309（CC BY 2.0・2013-10-10・新しい覆いの赤い骨組みと4号炉＝画面いっぱいでゆっくり寄る＝副題「現在の4号炉と新しい覆いの骨組み〈2013年〉」） ／ S2 p.35／~32（`Reactor power reduction stopped`）
+**c304** ／ 実写 Commons c3309（CC BY 2.0・2013-10-10・新しい覆いの赤い骨組みと4号炉＝画面いっぱいでゆっくり寄る＝副題「現在の4号炉と新しい覆いの骨組み〈2013年〉」） ／ S1-表I-I p.63／53（`ORM equals 31`・`Reactor thermal power is 1600 MW`）
```

## c305
- id `G1-020`：語りの7時10分・13.2本の根拠は表I-I p.63／53 の07:10 の行（find で当たる）（B）
```diff
-**c305** ／ 実写 Commons 現在の4号炉-シ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S1-表I-I p.63／53（`ORM equals 31`）
+**c305** ／ 実写 Commons 現在の4号炉-シ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S1-表I-I p.63／53（`ORM equals 13.2 manual control rods`）
```

## c306
- id `G1-006`：S1 p.21／11「The recent reports confirm … and in fact claim that this minimum ORM was also violated for several hours on 25 April」＝1992年の報告は新しい報告の言い分として引く。係の案の「ソ連の報告」は §4 で S3 を指すので「新しい報告」（recent reports）にし、出典の片に claim を入れた（+5字）（B）
```diff
-**c306** ／ 図 模式（25日の残した棒の数の線＝15本の線を下にくぐる所に印） ／ S1 p.21／11（`this minimum ORM was also violated for several hours on 25 April`）
+**c306** ／ 図 模式（25日の残した棒の数の線＝15本の線を下にくぐる所に印） ／ S1 p.21／11（`claim that this minimum ORM was also violated for several hours on 25 April`）
-> 1992年の報告も、25日に何時間も、この下限が破られていたと書く。
+> 1992年の報告も、25日に何時間も下限を割っていた、とする新しい報告を引く。
```

## c309
- id `G1-005`：§3-4。S2 p.35 の表＝14時の切り離しは計画どおり・違反の札は「ECCS remained isolated (e) Safety principle violation」に付く（+4字・片を出典の欄に足す）（B）
```diff
-**c309** ／ 実写 Commons 現在の4号炉-ウ（2013年の BY-SA の1点＝配管か建屋の寄り・額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S2 p.35／~32（`blocked ECCS played no role in transient to point of core disruption`）
-> 1986年の報告は、これを安全の原則に反するとした。
+**c309** ／ 実写 Commons 現在の4号炉-ウ（2013年の BY-SA の1点＝配管か建屋の寄り・額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S2 p.35／~32（`blocked ECCS played no role in transient to point of core disruption`・`ECCS remained isolated`）
+> 1986年の報告は、切りっぱなしを、安全の原則に反するとした。
```

## c311
- id `G1-004`：S1 p.20／10「This could be viewed as no violation only if … which it clearly was not」＝違反でないとは言えない、まで言う。§3-5＝「約11時間」でよい（+4字・40字）（B）
```diff
-**c311** ／ イメージ Pexels（今の発電所の配管か弁＝「イメージ：現在のチェルノブイリ原発」・映像方針で選ぶ） ／ S1 p.20／10（`which it clearly was not`・`are indicative of an absence of safety culture`）
-> ただ、半分の出力のまま、およそ11時間も切っておいたのは、計画の外だった。
+**c311** ／ イメージ Pexels（今の発電所の配管か弁＝「イメージ：現在のチェルノブイリ原発」・映像方針で選ぶ） ／ S1 p.20／10（`which it clearly was not`・`are indicative of an absence of safety culture`・`This could be viewed as no violation only if`）
+> ただ、半分の出力で約11時間も切っていたのは計画の外で、違反でないとは言えない。
```

## c312
- id `G1-018`：S1-付属書I p.82／72「a violation of Section 2.10.5 of the Operating Procedures」＝運転の規則（c309 の INSAG-1 の「安全の原則」と分ける・字は同じ）（B）
```diff
-> 1991年のソ連の委員会は、安全の規則に反する、と書く。
+> 1991年のソ連の委員会は、運転の規則に反する、と書く。
```

## c316
- id `G1-007`：S2 p.28／~25「The power reduction was stopped on request from system control and not resumed until approximately 9 h later」＝止まっていたのは出力を下げる作業（試験の予定の時刻はどの資料にも無い）。真夜中の繰り返し（c317）も消える（−2字）（B）
- id `R1-007`：S2 p.28／~25 の power reduction＝c315〜c317 の繰り返しを減らす（−4字）（A）
```diff
-**c316** ／ 図 模式（延期で長くなった待ち時間＝14:00 から 23:10 の帯を赤く） ／ S3 p.20／16（`At 23:10 hours, the power reduction was resumed`）・S2 p.28／~25（「延期はおよそ9時間」＝要約）
+**c316** ／ 図 模式（延期で長くなった待ち時間＝14:00 から 23:10 の帯を赤く） ／ S3 p.20／16（`At 23:10 hours, the power reduction was resumed`）・S2 p.28／~25（`not resumed until approximately 9 h later`）
-> そう。試験は、予定から9時間ほど遅れて、真夜中へ向かう。
+> そう。その作業は、9時間ほど止まっていた。
```

## c401
- id `G2-002`：語りの「0時5分に720メガワット」の出どころ（表I-I p.63／53 の 00:05 の行）と、INSAG-1 の 700〜1,000（S2 p.28／~25）を pg24 で文字の層に1回ずつ当てた＝出典の欄だけの直し（D）
- id `G7-019`：c209「炉が出す熱は3,200メガワット」と同じ言い方にそろえ（S3 p.20／16 MW(th)）、前のメガワットを省いて字を返した（値と範囲は原文どおり）（A）
```diff
-**c401** ／ 図 模式（26日 0:05 の出力の針＝720MW） ／ S3 p.20／16（`was to be carried out at a reactor power of 700-1000 MW(th)`）
+**c401** ／ 図 模式（26日 0:05 の出力の針＝720MW） ／ S1-表I-I p.63／53（`Reactor thermal power was 720 MW`）・S3 p.20／16（`was to be carried out at a reactor power of 700-1000 MW(th)`）・S2 p.28／~25（`reduction of power to between 700 and 1000 MW(th)`）
-> 試験の予定は、熱出力で700メガワットから1,000メガワットである。
+> 試験の予定は、炉が出す熱で700から1,000メガワットである。
```

## c402
- id `G2-003`：原文は power control（S1 p.21／11）＝押し下げる向きの「おさえる」より「保つ」が合い、c404「出力を保つ指示」とも語がそろう（A）
```diff
-> 0時28分、出力をおさえる自動の仕組みを、炉の部分ごとのものから、
+> 0時28分、出力を保つ自動の仕組みを、炉の部分ごとのものから、
```

## c407
- id `G2-005`：inability to control the power（S1 p.21／11）・付属書I p.73／63 の allowed the thermal power of the reactor to fall＝出力は下がりすぎた場面なので「おさえきれない」は向きが逆、「思うように保てなかった」で原文の強さのまま（A）
```diff
-**c407** ／ 図 模式（1991年の委員会の見方＝「原因は確かめられない」「おさえきれなかった」の2つの札＝字は少なく） ／ S1 p.21／11（`refers to an unknown cause and inability to control the power`）
+**c407** ／ 図 模式（1991年の委員会の見方＝「原因は確かめられない」「保てなかった」の2つの札＝字は少なく） ／ S1 p.21／11（`refers to an unknown cause and inability to control the power`）
-> おさえようとしても、出力をおさえきれなかった、とした。
+> 出力を、思うように保てなかった、とした。
```

## c412
- id `G2-006`：INSAG-1 が禁止と書いたのは continuous operation below 700 MW(th)（S2 p.25／~22）・1992年も sustained operation（S1 p.21／11）＝「運転を続けた」を足し、語尾を「ことだ」にして字を2字返した（B）
- id `R1-008`：c211 と同じ「最大の出力」（decisions §3 の2）＝画の欄の札だけ（D）
```diff
-**c412** ／ 図 棒（熱出力の棒＝3,200MW 定格／1,600MW 25日／700MW 試験の予定／200MW その夜／30MW 0時28分＝色を多く） ／ S2 p.25／~22（`continuous operation below 700 MW(th) is forbidden by normal safety procedures`）
-> ここで4つ目の「違反」。700メガワットより下での運転である。
+**c412** ／ 図 棒（熱出力の棒＝3,200MW 最大の出力／1,600MW 25日／700MW 試験の予定／200MW その夜／30MW 0時28分＝色を多く） ／ S2 p.25／~22（`continuous operation below 700 MW(th) is forbidden by normal safety procedures`）
+> ここで4つ目の「違反」。700メガワットより下で、運転を続けたことだ。
```

## c414
- id `G2-007`：S1 p.20／10 was based on oral statements made by Soviet experts（その直後に p.21／11 The emphasis … was not warranted）＝出どころを足して1986年の報告が根拠なく書いたと聞こえないようにし、字は「この点を」を外して縮めた（ソ連の説明は第7章まで出ないので「ソ連の」は残す）（B）
- id `R1-005`：S1 p.20／10＝強く書いたのは700MW 未満の禁止＝何を強く書いたかを戻す（A）
```diff
-**c414** ／ 図 模式（1986年の報告の頁に「強調は当たらない」の札＝字は少なく） ／ S1 p.21／11（`The emphasis placed on this statement in INSAG-1 was not warranted.`）
-> 1986年の報告がこの点を強く書いたのは、当たらなかった、とまで書く。
+**c414** ／ 図 模式（1986年の報告の頁に「強調は当たらない」の札＝字は少なく） ／ S1 p.21／11（`The emphasis placed on this statement in INSAG-1 was not warranted.`）・S1 p.20／10（`was based on oral statements made by Soviet experts`）
+> 1986年の報告が、ソ連の口頭の説明をもとに、
+> 禁止と強く書いたのは、当たらなかった、とまで書く。
```

## c415
- id `G2-008`：S1 p.38／28 INSAG has been informed that operating instructions have been updated＝事故のあとの下限は伝え聞きなので「という」で残す（B）
```diff
-> 事故のあと、700メガワットは、ふだんの運転の下限として決められた。
+> 事故のあと、700メガワットは、ふだんの運転の下限として決められた、という。
```

## c416
- id `G2-009`：付属書I p.59／49 の片は A ban on operation of the four main circulating pumps の禁止（別の禁止）で、語りの「事故の前に低い出力の禁止は無かった」は p.87／77 there were no safe operating limits … にある＝片の差し替えだけ（B）
```diff
-**c416** ／ 図 模式（3つの欄＝設計・規制・運転の指示書＝どれにも「禁止なし」の印・その下に「事故のあとで下限に」） ／ S1-付属書I p.59／49（`this confirms that there was no such ban before the accident`）
+**c416** ／ 図 模式（3つの欄＝設計・規制・運転の指示書＝どれにも「禁止なし」の印・その下に「事故のあとで下限に」） ／ S1-付属書I p.87／77（`there were no safe operating limits in terms of minimum permissible thermal reactor power`）
```

## c417
- id `G2-010`：S1 p.15／5 Control at lower power levels relied solely on the ex-core detectors・they were all located at the mid-plane of the core＝「多く」は all を弱め、炉の中の計器が使えない要の点を落としていた（字は +3）（B）
```diff
-**c417** ／ 図 模式（低い出力の炉の計器＝計器の多くが炉の真ん中の高さにある・上と下が見えない） ／ S1 p.15／5（`a reactor operator had to rely mainly on experience and intuition`）
-> 低い出力の RBMK は、扱いが難しい。計器の多くは炉の真ん中の高さにある。
+**c417** ／ 図 模式（低い出力の炉の計器＝炉の中の計器は使えず、外の計器はどれも炉の真ん中の高さ・上と下が見えない） ／ S1 p.15／5（`they were all located at the mid-plane of the core`・`a reactor operator had to rely mainly on experience and intuition`）
+> 低い出力では、炉の中の計器が使えない。外の計器は、どれも炉の真ん中の高さにある。
```

## c420
- id `G2-011`：S1 p.18／8 In addition, owing to the lower reactor power level at that time, the core inlet coolant was only slightly subcooled（付属書I p.74／64 も primarily as a result of the low reactor power level）＝「出力も低いため」は原文の In addition の並べのまま（B）
- id `R1-001`：付属書I p.74／64「primarily as a result of the low reactor power level」＝主因は低い出力・流れは足し（In addition）＝重みを戻す（B）
```diff
-**c420** ／ 図 模式（炉の入口の水の温度＝沸く温度のすぐ手前） ／ S1 p.18／8（`The use of all eight pumps increased the coolant flow rate above that under nominal`）
-> そう。水の流れが増え、炉の入口の水は、沸く寸前の熱さになっていた。
+**c420** ／ 図 模式（炉の入口の水の温度＝沸く温度のすぐ手前） ／ S1 p.18／8（`The use of all eight pumps increased the coolant flow rate above that under nominal`・`owing to the lower reactor power level at that time`）
+> そう。出力が低いうえ、水の流れも増え、炉の入口の水は沸く寸前だった。
```

## c421
- id `G2-012.1`：decisions §3 の6＝採る・字は縮める：付属書I p.87／77 the flow rates of certain MCPs actually exceeded the limit (violation …)・同 p.88／78 if anything hindered the reactor runaway＝違反と「むしろ妨げた」の両方を同じ委員会の言葉として並べ、G2-013（最後の1時間を消す）と G7-020（炉の暴走）を同じ直しに入れて差し引き −1字（C）
- id `G2-012.2`：decisions §3 の6＝採る・字は縮める：付属書I p.87／77 the flow rates of certain MCPs actually exceeded the limit (violation …)・同 p.88／78 if anything hindered the reactor runaway＝違反と「むしろ妨げた」の両方を同じ委員会の言葉として並べ、G2-013（最後の1時間を消す）と G7-020（炉の暴走）を同じ直しに入れて差し引き −1字（C）
```diff
-**c421** ／ 実写 Commons 現在の4号炉-ヒ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S1-付属書I p.88／78（`if anything hindered the reactor runaway`）
-> ただし1991年の委員会は、8台のポンプは、むしろ暴走を妨げたかもしれない、
-> と書く。ここでも見方は割れる。こうして炉は、試験の夜の最後の1時間を迎える。
+**c421** ／ 実写 Commons 現在の4号炉-ヒ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S1-付属書I p.88／78（`if anything hindered the reactor runaway`）・S1-付属書I p.87／77（`the flow rates of certain MCPs actually exceeded the limit`）
+> ただし1991年の委員会は、一部のポンプの流れすぎは違反としつつ、
+> 8台のポンプは、むしろ炉の暴走を妨げたかもしれない、と書く。
+> ここでも見方は割れる。
```

## c501
- id `G2-014`：同じカットに「自動で炉を止める」が2回＝言い回しだけの直しで字を3字返す（意味は2行目の説明で残る）（A）
```diff
-> 次の2つは、炉を自動で止める保護の話である。保護とは、
+> 次の2つは、炉を止める保護の話である。保護とは、
```

## c504
- id `G2-015`：S1 p.22／12 The recent information suggests that the steam drum protection was changed as early as 00:36＝1992年の報告の推量（suggests）を断定にしていたので「らしい」で残す（B）
- id `G0-001`：c504→c505 が矛盾して聞こえる（F2 の申し送り）：0時36分に変えたのは蒸気の圧力の保護の設定（付属書I p.85／75「At 00:36:24 the personnel changed the set point … 55 … to 50」＝手順の内・表I-I p.64／54）。違反とされたのは水位の設定を切り替えなかった別の件（c505）。INSAG-7 本文 (6) は2つを1つの文で書く＝帰属を「報告の表」にして圧力と言う（本文の suggests のらしいは、表が時刻を言い切るので外す）
- id `G0-002`：c504 の画の欄と出典の欄を G0-001 に合わせる（表I-I の 00:36:24 の行）
- id `G0-003`：c504 の出典の欄に表I-I の片
- id `R1-002`：表I-I は付属書I（1991年の委員会）の表＝c305「1991年の委員会の報告の表」と呼び分けをそろえる（c505 の主語とも続く）。decisions §4 の「1992年の報告の表」は G0 の書き損じ＝こちらが正（B）
```diff
-**c504** ／ 図 模式（ドラムの水位の保護の2つの段＝上の段の設定を変えた・下の段は最後まで効いていた） ／ S1 p.22／12（`as early as 00:36 on April 26 and not at 01:19:00 as stated`）・S1 p.22／12（`protection at the lower steam drum level remained effective throughout the event`）
-> 1992年の報告によれば、設定が変えられたのは、もっと早い0時36分。
-> そして保護には2つの段があり、下の段は、最後まで効いていた。
+**c504** ／ 図 模式（ドラムの保護＝0時36分に圧力の保護の設定を変えた〈手順の内〉・水位の保護の2つの段＝下の段は最後まで効いていた） ／ S1 p.22／12（`as early as 00:36 on April 26 and not at 01:19:00 as stated`）・S1 p.22／12（`protection at the lower steam drum level remained effective throughout the event`）・S1-表I-I p.64／54（`The EPS trip point in response to a pressure drop in the steam separator drums was changed`）
+> 1991年の委員会の表では、もっと早い0時36分に、圧力の保護の設定が変わる。
+> そして水位の保護には2つの段があり、下の段は、最後まで効いていた。
```

## c505
- id `G2-016`：decisions §2＝付属書I p.85／75 These personnel actions were in violation of Section 9（水位の設定を切り替えなかった件）・p.88／78 were not the causes of the accident and did not affect its scale、責めないとしたのは p.85〜86／75〜76 の蒸気の圧力の保護の別件＝帰属を直し、出典の欄に p.85 の片も足した（B）
```diff
-**c505** ／ 実写 Commons 現在の4号炉-カ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S1 p.22／12（`technically in violation of Item 9`）
-> 運転員は、設定を戻していない。だから形の上では、違反になる。
-> ただ、1991年の委員会は、これで運転員を責めてはいない。
+**c505** ／ 実写 Commons 現在の4号炉-カ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S1 p.22／12（`technically in violation of Item 9`）・S1-付属書I p.85／75（`These personnel actions were in violation of Section 9`）・S1-付属書I p.88／78（`were not the causes of the accident and did not affect its scale`）
+> 運転員は、水位の設定を切り替えていない。だから形の上では、違反になる。
+> ただ1991年の委員会は、違反とはしたが、事故の原因ではなかった、とする。
```

## c507
- id `G2-017`：1時23分4秒に外したと書いたのは INSAG-1 の表I（S2 p.39 The personnel'blocked the (r) two TGs-trip signal・S1 p.21／11 as stated in INSAG-1）＝出典の欄に足すだけ（頁の書き方は c508 の ~36 にそろえた）（B）
```diff
-**c507** ／ 図 流れ（タービン2台が止まる→炉を止める信号→この信号を外す＝矢印に×） ／ S3 p.27／23（`Blocking of reactor protection system relying on shutdown signal from two turbogenerators`）
+**c507** ／ 図 流れ（タービン2台が止まる→炉を止める信号→この信号を外す＝矢印に×） ／ S2 p.39／~36（`two TGs-trip signal`）・S3 p.27／23（`Blocking of reactor protection system relying on shutdown signal from two turbogenerators`）
```

## c511
- id `G2-018`：2行目は c510「運転の手順と、試験の手順に沿ったもの」（S1 p.21／11 blocked in accordance with operational procedures and test procedures）の言い直しで、消すと c511 の委員会と c512 の1992年の報告が聞き分けやすくなり字も19字返る（A）
```diff
-> 手順どおりの操作だった、という見方である。
```

## c512
- id `G2-019`：decisions §2＝S1 p.21／11（INSAG 本文 3章(4)）"This trip would have saved the reactor" seems not to be valid＝主語を1992年の報告にし、c511（1991年の委員会）→c512・c513（1992年の報告の本文と別の節）が声に出して聞き分けられることを読んで確かめた（B）
```diff
-> そして、「保護が働けば炉は救われた」という1986年の見方は、
+> そして1992年の報告は、「保護が働けば炉は救われた」という1986年の見方も、
```

## c513
- id `G2-020`：decisions §2＝S1 p.28／18 might well have caused the destruction of the reactor at the time of turbine trip rather than shortly afterwards＝「少し早く」で比べを残し、条件（もし保護が働いていたら）と might well＝かもしれないは原文どおり（c513 は使う）（B）
```diff
-> タービンを止めたその時に、炉が壊れていたかもしれない、と。
+> タービンを止めたその時に、炉が少し早く壊れていたかもしれない、と。
```

## c514
- id `G2-021`：decisions §2＝原文は rather than shortly afterwards（どのみち壊れた・早まっただけ）なので、反応を「逆だった」から「壊れるのを早めたかもしれない」に弱め、c513 より強く言わない（数字なし・先取りなし）（B）
```diff
-> Q: 炉を救うはずの保護が、逆だったかもしれないなんて。
+> Q: 炉を救うどころか、壊れるのを早めたかもしれないなんて。
```

## c516
- id `G2-022`：S1 p.29／19 the operating staff did not stop and think, but on the spot they modified the test conditions＝受け身で消えていた「その場で条件を変えた」主体を運転員に戻し（係の案は主語が「試験は」のままで誰が変えたかがねじれる）、出典の欄に片を足した（B）
```diff
-**c516** ／ 図 模式（試験の出力の書き直し＝700MW の予定に×・200MW のまま進む） ／ S1 p.29／19（`When the reactor power could not be restored to the intended level of 700 MW(th)`）
-> 試験は、予定の700メガワットに戻せないまま、
-> 200メガワットで進められることになった。
+**c516** ／ 図 模式（試験の出力の書き直し＝700MW の予定に×・200MW のまま進む） ／ S1 p.29／19（`When the reactor power could not be restored to the intended level of 700 MW(th)`）・S1 p.29／19（`on the spot they modified the test conditions`）
+> 予定の700メガワットに戻せないまま、運転員はその場で条件を変え、
+> 200メガワットで試験を進めた。
```

## c603
- id `G3-004`：decisions §2 の🔴＝S3 p.23／19 の not more than half は S3 p.26／22 の決まり（fewer than 30 rods）に対しての言い方で、6〜8本は15本の0.4〜0.53倍＝「およそ半分」（B）
```diff
-> その値は、6本から8本。すぐ止めるべき15本の、半分以下だった。
+> その値は、6本から8本。すぐ止めるべき15本の、およそ半分だった。
```

## c605
- id `G7-021`：c220・c310 と同じ問いの3回目を避け、次の語り「違反だったことは変わらない」がそのまま答える問いになる（数字なし・先取りなし・字は1字減る）（A）
```diff
-> Q: 書き直した報告では、どうなったの？
+> Q: 書き直した報告でも、違反のまま？
```

## c606
- id `G3-002`：S1 p.21／11 は likely（値を知らなかった）のすぐ後に Probably he was aware（ORM が減っていることには気づいていた）と書き、原文に無い「からだ」の因果を外す＝運転員の側に寄らないよう両方を残し、係の案（+15字）を縮めて自分の文にした（おそらく・見込みが高いを落とさない）（B）
- id `G3-016`：G3-002 で足した「おそらく気づいていた」の片（S1 p.21／11）と画の欄の「10〜15分」の片（S1 p.16／6 `This data system required about 10-15 min`＝文字の層で確かめた）を出典の欄に足す（F）
- id `R1-003`：S1 p.21／11「during the critical part of the test」＝限定を戻す（4'-18）（B）
```diff
-**c606** ／ 図 模式（計算機 SKALA＝値を出す画面に「？」・10〜15分かかる） ／ S1 p.21／11（`it is likely that the operator did not know the value of the ORM`・`the computer SKALA, which was used to calculate the ORM, became unreliable`）
-> ただし、その値を運転員は知らなかった見込みが高い、とも書いた。
-> 値を計算する計算機 SKALA が、当てにならなくなっていたからだ。
+**c606** ／ 図 模式（計算機 SKALA＝値を出す画面に「？」・10〜15分かかる） ／ S1 p.21／11（`it is likely that the operator did not know the value of the ORM`・`the computer SKALA, which was used to calculate the ORM, became unreliable`・`Probably he was aware that continued operation`）・S1 p.16／6（`This data system required about 10-15 min`）
+> ただし、値を出す計算機 SKALA が、当てにならなくなっていた。
+> 運転員は試験の山場で値を知らなかった見込みが高いが、減ることには、
+> おそらく気づいていた、とも書く。
```

## c609
- id `G3-003`：c608 の語りと原文（S1 p.21／11 were not aware）はどちらも「知らなかった」で、受け身の「知らされていなかった」は責めを他へ移して運転員の側に寄る＝まとめを語りの言い直しに戻す（A）
```diff
-> Q: 違反ではあったけど、その意味は、知らされていなかったんだ。
+> Q: 違反ではあったけど、その意味は、知らなかったんだ。
```

## c612
- id `G7-023`：語りで「ボタン」が出るのは c612 がはじめて（AZ-5 の名は c613・中身は c614）＝「止めるボタン」で何のボタンかが聞いて分かる（1行39字）（A）
```diff
-> 1991年の委員会は、ボタンが押されるまで、出力は上がっていないと書く。
+> 1991年の委員会は、止めるボタンが押されるまで、出力は上がっていないと書く。
```

## c613
- id `G3-006`：S3 p.21／17 の began to rise slowly と付属書I p.75／65 の no increase は「逆」でなく食い違い（1991年は下がったとは書かない）＝decisions §3-8 のとおり役割は反応のまま語だけ替える（A）
```diff
-> Q: 報告によって、出力の話が逆なんだ。
+> Q: 報告によって、出力の話が食い違うんだ。
```

## c617
- id `G7-024`：decisions §2 の🔴＝電気を切って重さで落とす話は S3 p.21／17（He then cut off the current to the sleeves of the servo drives）にだけあり、§4 の呼び分けで「1986年のソ連の報告」（B）
```diff
-> 棒は、下まで入りきらずに止まった。1986年の報告では、運転員が、
+> 棒は、下まで入りきらずに止まった。1986年のソ連の報告では、運転員が、
```

## c621
- id `G3-007`：次の章の頭は夜の火事（S3 p.29／25 の 01.30・S2 p.68 の 05:00）で「事故の朝から」は時刻がずれるうえ、「わずか3キロ」は c705 の原文の just と2カットおいて重なる（A）
```diff
-> その前に、事故の朝からの動きを追っていこう。発電所の火事、
-> そして、わずか3キロ先の町で起きたことである。
+> その前に、爆発のあとの動きを追っていこう。発電所の火事、
+> そして、3キロ先の町で起きたことである。
```

## c701
- id `G3-008`：S3 p.21／17 は some of which fell onto the roof＝塊と火花の一部が屋根に落ちた（全部ではない）で、前半の「炉の上に飛び」は c618 の繰り返しなので削って字も返す（B）
```diff
-> 燃える塊や火花が炉の上に飛び、タービンの建屋の屋根に落ちて、
+> 燃える塊や火花の一部は、タービンの建屋の屋根に落ちて、
```

## c702
- id `G3-017`：語りの「朝の5時に消し止められた」の片が無い＝S2 p.68／~63 の `the fire was quenched at 05:00` を文字の層で確かめて出典の欄に足す（語りは変えない）（F）
```diff
-**c702** ／ 実写 IAEA 02790013（3・4号機の屋根のちりを抑える作業＝クレーンとコンクリートポンプ車・BY-SA 2.0・額装＝副題「3・4号機の屋根での作業〈1986年〉」） ／ S3 p.29／25（`Fire had broken out in over 30 places`）・S2 p.68／~63（`localized at 02:10 and 02:20 respectively`）
+**c702** ／ 実写 IAEA 02790013（3・4号機の屋根のちりを抑える作業＝クレーンとコンクリートポンプ車・BY-SA 2.0・額装＝副題「3・4号機の屋根での作業〈1986年〉」） ／ S3 p.29／25（`Fire had broken out in over 30 places`）・S2 p.68／~63（`localized at 02:10 and 02:20 respectively`・`the fire was quenched at 05:00`）
```

## c703
- id `G3-009`：S3 p.42／38〜p.43／39 は a number of plant and emergency service personnel＝火を消した人の全員ではなく何人も（上位語に広げない）（B）
```diff
-> 火を消した消防士や職員は、強い放射線を浴び、やけども負っていた。
+> 火を消した消防士や職員の何人もが、強い放射線を浴び、やけども負っていた。
```

## c709
- id `G3-010`：L2 p.24／472〜p.25／473 はウクライナの30キロの範囲の避難を2段（10キロの範囲の南は4月30日〜5月3日・残りは5月3日〜7日）と書く＝前の段を落とさず期間を4月30日〜5月7日にし、G7-025 の起点も同じ行に組んだ（起点は L2 p.14／462 の surrounding the reactor に合わせて「炉から」＝c705 の「壊れた炉から」と同じ・係の「発電所から」より2字短い）（B）
- id `G3-011`：G3-010 の「4月30日」の片（L2 p.24／472）に加え、「炉から30キロ」の片（L2 p.14／462 `the 30-km-radius area surrounding the reactor`＝文字の層で確かめた）も足す（F）
```diff
-**c709** ／ 実写 IAEA 02790025（森の道の「放射能」の標識＝未知への道・BY-SA 2.0・額装＝副題「放射能の標識〈1986年〉」） ／ L2 p.24／472（`Yanov (254 persons)`）・L2 p.25／473（`were evacuated from 3 May through 7 May.`）
-> 近くの駅、ヤノフの254人も一緒だった。ウクライナの側の30キロの範囲の、
-> ほかの町や村の人たちも、5月3日から7日にかけて避難した。
+**c709** ／ 実写 IAEA 02790025（森の道の「放射能」の標識＝未知への道・BY-SA 2.0・額装＝副題「放射能の標識〈1986年〉」） ／ L2 p.24／472（`Yanov (254 persons)`）・L2 p.24／472（`was carried out from 30 April through 3 May`）・L2 p.25／473（`were evacuated from 3 May through 7 May.`）・L2 p.14／462（`the 30-km-radius area surrounding the reactor`）
+> 近くの駅、ヤノフの254人も一緒だった。炉から30キロの範囲の、
+> ウクライナの側のほかの町や村の人たちも、4月30日から5月7日にかけて避難した。
```

## c713
- id `G3-014`：国会の答弁（1986-05-15 参院 内閣委・原子力安全調査室長）は「十四日時点で、二十九都道府県にわたり…ヨウ素131が検出」＝見つかった所の数で、「広がっていた」は測った所の外まで言うので少し強い（名前の入る出典の欄には触らない）（A）
```diff
-> 5月14日の時点では、29の都道府県に広がっていた。
+> 5月14日の時点では、29の都道府県で見つかっていた。
```

## c715
- id `G3-015`：答弁（1986-05-07 参院 科学技術特別委・科学技術庁長官）は「現在までのところ…放射能は検出されておらず」＝「出ていなかった」は放出されていないとも聞こえ c713 のヨウ素131と食い違うので「見つかっていなかった」に（名前の入る出典の欄には触らない）（A）
```diff
-> 国の答弁では、健康に影響を与えるような放射能は、出ていなかった。
+> 国の答弁では、健康に影響を与えるような放射能は、見つかっていなかった。
```

## c716
- id `G3-018`：c716 の出典の欄が「—」＝L3 p.43／83 にキエフで毎日通りを洗ったことがある（文字の層の wash-ing の後ろから9語で引いた）（F）
- id `G7-027`：反応「日本の雨にまで届いていた」は c713 のまとめの言い直しで受けが合わないが、係の案（質問に替える）は質問が61%（目安60%まで）で m24 が W を出した＝役割は反応のまま、直前の c714〜c715（答弁の「念のため」）を受けてソ連の話と対にする反応に替え、字も返す（数字なし・先取りなし・避難や病気の場面ではない・c223 と同じく「そう。」なし）（C）
- id `R1-009`：国会の答弁（K1 1986-05-07 の念のため）＝日本全体へ広げない・「〜んだ。」のまとめの形を外す（A）
```diff
-**c716** ／ 実写 IAEA 02790014（1986年5月1日、キエフの大通りで水による除染＝地下鉄の「M」・BY-SA 2.0・額装＝副題「キエフの通りの除染〈1986年5月1日〉」） ／ —
-> Q: 遠い国の事故が、日本の雨にまで届いていたんだ。
-> そう。ソ連の中では、キエフの町でも、通りに水をまいて汚れを落としていた。
+**c716** ／ 実写 IAEA 02790014（1986年5月1日、キエフの大通りで水による除染＝地下鉄の「M」・BY-SA 2.0・額装＝副題「キエフの通りの除染〈1986年5月1日〉」） ／ L3 p.43／83（`of streets in Kiev decreased the collective external dose`）
+> Q: 国の注意は、念のためだったのか。
+> ソ連の中では、キエフの町でも、通りに水をまいて汚れを落としていた。
```

## c717
- id `G3-019`：decisions §3-10 のとおり「事故から4か月」は c802 に残して c717 から外す＝S2 p.1 の held in Vienna に合わせて場所だけにする（A）
```diff
-> その場は、事故から4か月後のウィーンだった。
+> その場は、オーストリアのウィーンだった。
```

## c805
- id `G4-003`：前の問い「ソ連は、何と説明したの？」に「〜だ、と。」の引きの形で答え、語り手の言い切りに聞こえないようにした（S3 p.26／22 lists the most dangerous violations … committed by the staff・p.27／23 prime cause … combination of violations）＝係の案より4字短い。（B）
```diff
-> 事故の原因は、職員の規則違反の重なりだった。報告書は、
+> 原因は、職員の規則違反の重なりだ、と。報告書は、
```

## c812
- id `G4-004.1`：S2 p.18／~13 を引き直すと、誤りの影響を大きくし暴走を招いたのは炉の性質（features which compounded and amplified … and led to the reactivity excursion）＝係の案は「違反が…暴走を招いた」とも聞こえるので、性質を主語に立て直し、c103「炉の性質と重なって起きた」と語をそろえ、出典の欄に led to の片を足した。（B）
- id `G4-004.2`：S2 p.18／~13 を引き直すと、誤りの影響を大きくし暴走を招いたのは炉の性質（features which compounded and amplified … and led to the reactivity excursion）＝係の案は「違反が…暴走を招いた」とも聞こえるので、性質を主語に立て直し、c103「炉の性質と重なって起きた」と語をそろえ、出典の欄に led to の片を足した。（B）
```diff
-**c812** ／ 図 p18 S2（1986年の報告の要約の頁＝原因の文・文字の頁・語りが名指しする所） ／ S2 p.18／~13（`the accident was eaused by a remarkable range of human errors`・`in combination with specific reactor features which compounded and amplified the effects of the errors`）
+**c812** ／ 図 p18 S2（1986年の報告の要約の頁＝原因の文・文字の頁・語りが名指しする所） ／ S2 p.18／~13（`the accident was eaused by a remarkable range of human errors`・`in combination with specific reactor features which compounded and amplified the effects of the errors`・`led to the reactivity excursion`）
-> 炉に特有の性質と組み合わさり、誤りの影響を大きくした。
+> 炉に特有の性質と重なって起きた。その性質が、誤りの影響を大きくし、暴走を招いた。
```

## c813
- id `G4-005`：S2 p.112／~105 の root cause … 'human element' は1行目で言い切れており、「重心は人の側」は c818 で言う＝同じ言い回しの2回目を消して13字返す（まとめの直後の「そう。」は残る）。（A）
```diff
-> 重心は、人の側に置かれていた。
```

## c815
- id `G7-029`：S2 p.47／~42 の no attempt has been made to find alternative explanations は1行目で言いずみ＝言い直しの2行目を消して29字返す（ソ連の資料に頼った点は c811「この説明を受けて」・c814 で通る）。（A）
```diff
-> ソ連の説明のほかの筋書きは、この時点では、探されなかったのである。
```

## c819
- id `G4-007`：S1 p.11／1 は made no attempt to generate alternative scenarios, although it was recognized that there were other possible explanations まで1文＝後半を足すが、「分かっていたが」を「知りつつ」にして係の案より字を抑えた（ほか の重なりを避け「別の筋書き」）。（B）
```diff
-**c819** ／ 実写 IAEA 02790040（溶接の火花＝事故のあとの作業・BY-SA 2.0・額装＝副題「事故のあとの溶接の作業〈1986年〉」） ／ S1 p.11／1（`made no attempt to generate alternative scenarios`）
+**c819** ／ 実写 IAEA 02790040（溶接の火花＝事故のあとの作業・BY-SA 2.0・額装＝副題「事故のあとの溶接の作業〈1986年〉」） ／ S1 p.11／1（`made no attempt to generate alternative scenarios`・`although it was recognized that there were other possible explanations`）
-> ソ連の説明をもっともらしいと考え、ほかの筋書きを作ろうとはしなかった、と。
+> ほかの説明もありうると知りつつ、ソ連の説明をもっともらしいと考え、
+> 別の筋書きを作ろうとはしなかった、と。
```

## c822
- id `G4-008`：S3 p.28／24 は eliminate the possibility of a continuing increase＝「おそれ」を戻すと、ソ連が現象を認めた形に強まらない（§0-1 の6）。（B）
```diff
-> 炉の下の方で反応が強まり続けるのを、なくすためだ、と書いてある。
+> 炉の下の方で反応が強まり続けるおそれを、なくすためだ、と書いてある。
```

## c902
- id `G4-009`：S1 p.14／4 の A graphite rod termed a 'displaced is attached（OCR の綴りのまま）が c902 の語り（黒鉛の棒がつながる）を支える片＝1.25m の片は c903 へ移す（G4-010）。（F）
```diff
-**c902** ／ 図 模式（棒の作り＝上に中性子を吸う棒・その下に黒鉛の押しのけ棒＝縦に並べた絵） ／ S1 p.14／4（`with 1.25 m of water at either end`）
+**c902** ／ 図 模式（棒の作り＝上に中性子を吸う棒・その下に黒鉛の押しのけ棒＝縦に並べた絵） ／ S1 p.14／4（`A graphite rod termed a 'displaced is attached`）
```

## c903
- id `G4-010`：decisions §3 の18＝G0 が図1(a) を頁の画像で見た（450・125・125cm）＝出典の欄に本文の片 S1 p.14／4（with 1.25 m of water at either end）と、G7-030 で語りに足す炉の高さの片 S1 p.16／6（height 7 m）を足し、「頁の画像で読む」を「確かめた」にした。（B）
- id `G7-030`：S1 p.16／6 の reactor core (height 7 m, …) と p.14／4 の displacer sat centrally … with 1.25 m of water at either end で 4.5＋1.25×2＝7 が合う＝耳だけで「真ん中・上下に水」が分かる（出典の片は G4-010 で足した）。（A）
```diff
-**c903** ／ 図 模式（棒を抜き切った状態＝押しのけ棒が炉の真ん中・上と下に1.25mずつの水＝図1 の寸法） ／ S1-図1 p.15／5（図の中の寸法＝押しのけ棒 450cm・水 125cm＝頁の画像で読む）
-> 棒を上まで抜き切ると、長さ4.5メートルの押しのけ棒が、炉の真ん中に来る。
-> その上と下には、1.25メートルずつ、水だけの部分が残る。
+**c903** ／ 図 模式（棒を抜き切った状態＝押しのけ棒が炉の真ん中・上と下に1.25mずつの水＝図1 の寸法） ／ S1 p.14／4（`with 1.25 m of water at either end`）・S1 p.16／6（`height 7 m`）・S1-図1 p.15／5（図の中の寸法＝押しのけ棒 450cm・水 125cm＝頁の画像で確かめた）
+> 棒を上まで抜き切ると、長さ4.5メートルの押しのけ棒が、
+> 高さ7メートルの炉の真ん中に来る。その上と下には、1.25メートルずつ、
+> 水だけの部分が残る。
```

## c904
- id `G4-011`：付属書I p.53／43 に the absorbing capacity of the graphite displacer … is lower than that of the water being forced out が文字の層で在る＝「黒鉛は水ほど中性子を吸わない」に片が付く（語りは変えない）。（F）
```diff
-**c904** ／ 実写 IAEA 02790041（作業員の寄り＝説明なし・BY-SA 2.0・額装・名乗らない＝副題「事故のあとの作業員〈1986年〉」） ／ —
+**c904** ／ 実写 IAEA 02790041（作業員の寄り＝説明なし・BY-SA 2.0・額装・名乗らない＝副題「事故のあとの作業員〈1986年〉」） ／ S1-付属書I p.53／43（`the absorbing capacity of the graphite displacer`・`is lower than that of the water being forced out`）
```

## c906
- id `G4-012`：S1 p.14／4 は The magnitude of this 'positive scram' effect depended on the spatial distribution … and the operating regime、付属書I p.49／39 は initial increase … as they start to move＝「入り始めに、…ことがある」の係の案を採り、出典の欄には条件しだいの片（p.14／4）も足した（「数秒」はどの資料にも無い）。（B）
```diff
-**c906** ／ 図 模式（炉の下の方だけ反応が強まる＝下半分を赤く・上半分は青く） ／ S1-付属書I p.54／44（`Triggering of the EPS in this case may lead to the introduction of positive reactivity.`）
+**c906** ／ 図 模式（炉の下の方だけ反応が強まる＝下半分を赤く・上半分は青く） ／ S1 p.14／4（`depended on the spatial distribution of the power density and the operating regime`）・S1-付属書I p.53／43（`local introduction of positive reactivity in the lower part of the core occurs`）・S1-付属書I p.49／39（`predetermine an initial increase in positive reactivity`）
-> 止めるための棒が、入り始めの数秒、逆の働きをしてしまうのだ。
+> 止めるための棒が、入り始めに、逆の働きをすることがあるのだ。
```

## c907
- id `G4-013`：逆に働くのは棒（S1 p.14／4 local insertion of positive reactivity）でボタンではない＝「AZ-5 が爆発を起こした」側に寄らない形で、係2つの案のうち字の短い方（G7-031 より3字短い）。（B）
- id `R2-007`：S1 p.14／4「depended on … the operating regime」＝c906 の限定（ことがある）を聞き役でも残す（C）
```diff
-> Q: 止めるボタンなのに、逆になるなんて。
+> Q: 止める棒が、逆に働くこともあるなんて。
```

## c908
- id `G4-014`：S1 p.37／27 は INSAG has been informed that … reduced from 18 s to 12 s＝伝聞なので「とされる」を付け、要約の注を文字の層の片に替える。（B）
```diff
-**c908** ／ 図 模式（棒が入りきるまで18秒＝砂時計・事故のあとは12秒） ／ S1 p.14／4（`when starting from the upper limit stop switches, was 18 s`）・S1 p.37／27（事故のあと12秒に＝要約）
+**c908** ／ 図 模式（棒が入りきるまで18秒＝砂時計・事故のあとは12秒） ／ S1 p.14／4（`when starting from the upper limit stop switches, was 18 s`）・S1 p.37／27（`reduced from 18 s to 12 s`）
-> 事故のあと、これは12秒に縮められている。
+> 事故のあと、これは12秒に縮められた、とされる。
```

## c910
- id `G4-015`：出典の欄に S1 p.28／18（INSAG now repeats that the violation took place）と p.21／11（were not aware that it had safety significance＝ORM の下限の意味）を足す。「違反」のかぎ括弧は c603 前後の「7つ目の「違反」」と同じ呼び名なので残す（音は同じ）。（F）
```diff
-**c910** ／ 実写 IAEA 02790037（装甲車のそばの作業員＝特別の配給を受ける作業員・BY-SA 2.0・額装＝副題「事故のあとの作業員〈1986年〉」） ／ S1 p.24／14（`made them crucially sensitive to the extent of insertion of the control and protection rods`）
+**c910** ／ 実写 IAEA 02790037（装甲車のそばの作業員＝特別の配給を受ける作業員・BY-SA 2.0・額装＝副題「事故のあとの作業員〈1986年〉」） ／ S1 p.24／14（`made them crucially sensitive to the extent of insertion of the control and protection rods`）・S1 p.28／18（`INSAG now repeats that the violation took place`）・S1 p.21／11（`were not aware that it had safety significance`）
```

## c911
- id `G7-033`：付属書I p.53／43 の physical startup は c105 で「起動の試験」と言った同じ試験＝呼び名をそろえ3字返す。（A）
```diff
-> 動かし始めの試験の中で、実験で見つかっていた。
+> 起動の試験の中で、実験で見つかっていた。
```

## c913
- id `G4-016`：S1 p.23／13 は it had first been identified at the Ignalina RBMK plant＝「最初に」を戻すと本文と付属書I（イグナリナ1号機とチェルノブイリ4号機）が両立して聞こえる。（B）
```diff
-> ただし、1992年の報告の本文は、イグナリナで見つかった、とだけ書く。
+> ただし、1992年の報告の本文は、イグナリナで最初に見つかった、とだけ書く。
```

## c914
- id `G4-017`：decisions §2 のとおり＝S1 p.23／13 は主任設計技師がほかの RBMK の発電所に promulgated と書き、付属書I p.96／86 は The personnel were unaware of some of the dangerous features＝「一部」と委員会の帰属を付けた案を pg24 で当て直した。（B）
- id `R2-008`：付属書I p.96／86「The personnel」＝同じ付属書を ca04・ca06〜ca08 は「職員」＝呼び分けをそろえる（decisions §2 の字は G0 の書き方の揺れ）（B）
```diff
-**c914** ／ 実写 IAEA 02790043（「技術水の管理」の札と線量計＝アルメニア原発から来た職長・BY-SA 2.0・額装＝副題「線量計を持つ職長〈1986年〉」） ／ S1-付属書I p.53／43（`The Chief Design Engineer [22] and the Scientific Manager knew about this effect`）
+**c914** ／ 実写 IAEA 02790043（「技術水の管理」の札と線量計＝アルメニア原発から来た職長・BY-SA 2.0・額装＝副題「線量計を持つ職長〈1986年〉」） ／ S1-付属書I p.53／43（`The Chief Design Engineer [22] and the Scientific Manager knew about this effect`）・S1-付属書I p.96／86（`The personnel were unaware of some of the dangerous features of the reactor`）
-> それでも、運転する人たちには、伝わっていなかった。
+> 一方、職員は、炉の危ない性質の一部を知らなかった、と委員会は書く。
```

## c916
- id `G4-018`：S1 p.25／15 は restrictions were never imposed and apparently the matter was forgotten＝反応を「そのままだった」（制限がかけられなかった）にして、語りの「どうやら」を断定に戻さない。（B）
```diff
-> Q: 見つかっていたのに、忘れられたなんて。
+> Q: 見つかっていたのに、そのままだったなんて。
```

## c919
- id `G4-019`：S1 p.26／16 は The most likely final event now seems to have been the insertion of safety rods …, which worsened to a destructive level the conditions already prevailing because of the positive power coefficient＝「炉の性質で、すでに危うかった状態への」を足して棒だけが原因と聞こえないようにし、係の案より短く「いちばんありそう」を残した（読みの「ひと押し」も入れた）。（B）
```diff
-**c919** ／ 実写 IAEA 02790030（マスクの兵士の敬礼＝片づけに加わった兵士・BY-SA 2.0・額装＝副題「片づけに加わった兵士〈1986年〉」） ／ S1 p.26／16（`most likely final event`）
+**c919** ／ 実写 IAEA 02790030（マスクの兵士の敬礼＝片づけに加わった兵士・BY-SA 2.0・額装＝副題「片づけに加わった兵士〈1986年〉」） ／ S1 p.26／16（`most likely final event`・`the conditions already prevailing because of the positive power coefficient`）
-> 1992年の報告は、慎重に書く。暴走の最後の一押しとして、
-> いちばんありそうなのは、止める棒を入れたことだ、と。
+> 1992年の報告は、慎重に書く。炉の性質で、すでに危うかった状態への、
+> 最後のひと押しとして、いちばんありそうなのは、止める棒を入れたことだ、と。
```

## c920
- id `G4-020`：decisions §2 のとおり＝付属書I p.93／83 は暴走は displacers の反応の強まりから initially arose と言い切る＝「委員会も」の2行目を消して28字返し、c921 は「同じ報告は…とも書く」から1992年の報告の続きとして通る。（B）
```diff
-> 1991年の委員会も、ボタンを押した理由は、確かめられなかった。
```

## c921
- id `G7-036`：S1 p.24／14 は which shortcoming was the actual cause＝「実際の原因」で1行の「本当」の重なりを解く（字は同じ）。（A）
```diff
-> どの弱点が本当の原因かは、本当に大事なのか、とまで問いかけている。
+> どの弱点が実際の原因かは、本当に大事なのか、とまで問いかけている。
```

## c922
- id `G4-022`：decisions §2 の字のとおり（定格を使わず最大の出力＝S2 p.10／~5 nominal power・付属書II p.131／121 the initial value）に、原文の approximately 80 times の「およそ」を4'-18 で戻した。（B）
```diff
-> 1986年の報告は、ソ連の専門家の計算で、4秒以内に100倍。
-> のちの計算には、3.5倍から80倍までの幅がある。
+> 1986年の報告は、ソ連の専門家の計算で、4秒以内に最大の出力の100倍。
+> のちの計算は、はじめの出力の3.5倍から、およそ80倍。比べるもとが違う。
```

## c926
- id `G4-024.1`：decisions §3 の12＝S1 p.33／23 の the concurrence of the following major factors（炉の物理の性質・止める棒の作り・手順に無い状態へ持ち込んだこと）に合わせ「8台のポンプ」を「炉の性質」に、片も替えた。factors に合わせ「弱点」を「条件」にし、まとめの問いも同じ語にした。（B）
- id `G4-024.2`：decisions §3 の12＝S1 p.33／23 の the concurrence of the following major factors（炉の物理の性質・止める棒の作り・手順に無い状態へ持ち込んだこと）に合わせ「8台のポンプ」を「炉の性質」に、片も替えた。factors に合わせ「弱点」を「条件」にし、まとめの問いも同じ語にした。（B）
- id `R2-009`：聞き役が直前の語りの字をそのまま繰り返さない（まとめは言い直し）（A）
```diff
-**c926** ／ 図 模式（4つの札が1つの炉に集まる＝低い出力・少ない残りの棒・8台のポンプ・棒の欠陥） ／ S1 p.29／19（`Such a mode of operation in itself could have led to a destructive accident`）
-> 低い出力、少ない残りの棒、8台のポンプ、そして棒の欠陥。
-> 事故の夜、この炉には、いくつもの弱点が重なっていた。
-> Q: 弱いところが、いくつも重なっていたんだ。
+**c926** ／ 図 模式（4つの札が1つの炉に集まる＝低い出力・少ない残りの棒・炉の性質・棒の欠陥） ／ S1 p.33／23（`the concurrence of the following major factors`）
+> 低い出力、少ない残りの棒、炉の性質、そして棒の欠陥。
+> 事故の夜、この炉には、いくつもの条件が重なっていた。
+> Q: 条件が、そろってしまっていたんだ。
```

## ca01
- id `G5-001`：decisions §2 のとおり＝付属書I p.41／31 は some of the engineering defects・by the end of May or beginning of June 1986（「一部」と「か」）。（B）
- id `G5-034`：出典の欄の片を、語りの「一部」と時期を支える2つの片（付属書I p.41／31 の文字の層で一致を見た）に替えた（係の案は「一部」の片を欠く）。（B）
```diff
-**ca01** ／ 図 p41 S1（1991年の委員会の報告〈INSAG-7 の付属書I〉の頁＝「IAEA に出した資料に入っていなかった」・文字の頁・印刷31・語りが名指しする所） ／ S1-付属書I p.41／31（`the defects identified in the reactor design and its unsatisfactory physical parameters`）
+**ca01** ／ 図 p41 S1（1991年の委員会の報告〈INSAG-7 の付属書I〉の頁＝「IAEA に出した資料に入っていなかった」・文字の頁・印刷31・語りが名指しする所） ／ S1-付属書I p.41／31（`some of the engineering defects in the RBMK-1000 reactor design`・`had already been realized by the end of May or beginning of June 1986`）
-> 炉の設計の欠陥は、事故の年の5月の終わりから6月の初めには、分かっていた。
+> 炉の設計の欠陥の一部は、事故の年の5月の終わりか6月の初めには、分かっていた。
```

## ca03
- id `G5-012`：§4 の「問いには次の語りの行がそのまま答える」に当たる＝付属書I p.70／60 の not to the actions of the operating personnel, but to the design が新しい問いの答えになり、c927 の問いのくり返しも消える。（C）
- id `G5-024`：付属書I p.70／60 は5月1日に所長へ、のちに9 May 1986 の手紙で国の指導者へ＝画の欄の字だけで直せて原文に合う（decisions §3 の22）。（F）
```diff
-**ca03** ／ 図 模式（1986年5月1日の見方＝研究所の研究グループの長から所長へ「原因は炉の設計」の手紙） ／ S1-付属書I p.70／60（`V.P. Volkov, head of the I.V. Kurchatov Institute Research Group on the Reliability and Safety`・`not to the actions of the operating personnel, but to the design of the reactor`）
-> Q: どうして、入らなかったの？
-> 事故から5日後の5月1日、クルチャトフ研究所の研究グループの長、ヴォルコフは、
-> 原因は運転員ではなく、炉の設計にあると見ていた、と委員会は書く。
+**ca03** ／ 図 模式（1986年5月1日の見方＝研究所の研究グループの長から所長へ・9日には手紙で国の指導者へ「原因は炉の設計」） ／ S1-付属書I p.70／60（`V.P. Volkov, head of the I.V. Kurchatov Institute Research Group on the Reliability and Safety`・`not to the actions of the operating personnel, but to the design of the reactor`）
+> Q: 設計を疑う人は、いなかったの？
+> いた。事故から5日後の5月1日、クルチャトフ研究所の研究グループの長、
+> ヴォルコフは、原因は運転員ではなく、炉の設計にあると見ていた、と委員会は書く。
```

## ca04
- id `G5-013`：decisions §3 の13＝付属書I p.70／60 はこの文で会議を Interdepartmental Science and Technology Council と書くだけ＝「研究所の所長」と言わない（10字返す）。（B）
```diff
-> 研究所の所長が議長を務めた、省庁の科学技術の会議である。
+> 省庁をまたぐ、科学技術の会議である。
```

## ca05
- id `G5-008.1`：付属書I p.70／60 の paved the way for the one-sided presentation（IAEA・専門家・一般へ）＝係の案の語りを採り、出典の欄の要約も同じ片に替えた。（B）
- id `G5-008.2`：付属書I p.70／60 の paved the way for the one-sided presentation（IAEA・専門家・一般へ）＝係の案の語りを採り、出典の欄の要約も同じ片に替えた。（B）
- id `G5-026`：🔴の直し（ca07・cb12）で字が足りないので使う＝1988年の訪問は副題が言い、ブリクスの名は c803 で出ている（写真の当て方は G5-022 で映像方針へ）。（D）
```diff
-**ca05** ／ 実写 IAEA 02790055（背広の人々＝ブリクス IAEA 事務局長の1988年5月の訪問・BY-SA 2.0・額装＝副題「ブリクス事務局長の訪問〈1988年5月〉」） ／ S1-付属書I p.70／60（「この結論が IAEA への説明の道を開いた」＝要約）
-> この会議の結論が、ウィーンでの説明につながった、と委員会は見ている。
-> 写真は、2年後の1988年に現地を訪れた、ブリクス事務局長の一行である。
+**ca05** ／ 実写 IAEA 02790055（背広の人々＝ブリクス IAEA 事務局長の1988年5月の訪問・BY-SA 2.0・額装＝副題「ブリクス事務局長の訪問〈1988年5月〉」） ／ S1-付属書I p.70／60（`paved the way for the one-sided presentation of information`）
+> この会議の決定が、ウィーンなどでの一方的な説明に道を開いた、と委員会は書く。
```

## ca06
- id `G5-005.1`：decisions §2 の形＝責め・評価の行（付属書I p.39／29 erroneous actions・p.41／31 no better, but no worse）に事故のあとの作業員の顔を当てない＝画の欄を「人の顔の写らない1986年の写真」に替えた。（F）
```diff
-**ca06** ／ 実写 IAEA 02790044（新聞を読む作業員＝毎日届いた新聞・BY-SA 2.0・額装＝副題「事故のあとの作業員〈1986年〉」・新聞の字は映像方針で原寸） ／ S1-付属書I p.41／31（`They were no better, but no worse, than the personnel at other nuclear plants.`）
+**ca06** ／ 実写（人の顔の写らない1986年の写真＝映像方針で選ぶ） ／ S1-付属書I p.41／31（`They were no better, but no worse, than the personnel at other nuclear plants.`）
```

## ca07
- id `G5-002.1`：decisions §2 の形＝付属書I p.81／71 は ORM fell to 15 … should be shut down. The personnel did not abide・deliberately・this violation was not die cause of the accident（止めなかったこと＋原因ではない）＝c303 の「15本まで減ったら止める」とつなぐため「残した棒が」を残し（1行目の「ただ」と重ねないよう3行目は接続の語なし）、出典の欄に原因ではない片を足した。（B）
- id `G5-002.2`：decisions §2 の形＝付属書I p.81／71 は ORM fell to 15 … should be shut down. The personnel did not abide・deliberately・this violation was not die cause of the accident（止めなかったこと＋原因ではない）＝c303 の「15本まで減ったら止める」とつなぐため「残した棒が」を残し（1行目の「ただ」と重ねないよう3行目は接続の語なし）、出典の欄に原因ではない片を足した。（B）
- id `G5-023`：G5-002 の語りに画の欄の札をそろえる（付属書I p.81／71＝止めなかったこと・原因ではない）＝画の欄の字だけで直せる。（F）
- id `R2-006`：付属書I p.81／71「this violation was not the cause」＝原因でないのはこの違反だけ（B）
```diff
-**ca07** ／ 図 模式（委員会が認めた職員の違反＝25日の朝に残した棒を15本より少なく〈わざと〉＝札） ／ S1-付属書I p.81／71（`The Commis-sion assumes that the personnel deliberately violated this requirement.`）
+**ca07** ／ 図 模式（委員会が認めた職員の違反＝25日の朝、残した棒が15本まで減っても止めなかった〈わざと・原因ではない〉＝札） ／ S1-付属書I p.81／71（`The Commis-sion assumes that the personnel deliberately violated this requirement.`・`this violation was not die cause of the accident`）
-> 25日の朝、残した棒を15本より少なくしたのは、わざとだったと見ている。
+> 25日の朝、残した棒が15本まで減っても止めなかったのは、わざとだと見る。
+> この違反は、事故の原因ではなかった、とも書く。
```

## ca08
- id `G5-005.2`：decisions §2 の形＝責め・評価の行（付属書I p.39／29 erroneous actions・p.41／31 no better, but no worse）に事故のあとの作業員の顔を当てない＝画の欄を「人の顔の写らない1986年の写真」に替えた。（F）
- id `G5-020`：付属書I p.39／29 の disproportionately disastrous consequences＝誤りの大きさに釣り合わないほどの被害、という比べが結論の芯なので戻す（寄せない）。（B）
```diff
-**ca08** ／ 実写 IAEA 02790039（作業員の寄り＝説明なし・BY-SA 2.0・額装・名乗らない＝副題「事故のあとの作業員〈1986年〉」） ／ S1-付属書I p.39／29（`which was initiated by erroneous actions on the part of the operating personnel`・`had disproportionately disastrous consequences because of deficiencies in the design of the reactor`）
+**ca08** ／ 実写（人の顔の写らない1986年の写真＝映像方針で選ぶ） ／ S1-付属書I p.39／29（`which was initiated by erroneous actions on the part of the operating personnel`・`had disproportionately disastrous consequences because of deficiencies in the design of the reactor`）
-> 被害が、とてつもなく大きくなったのは、炉の設計の欠陥のためである。
+> 被害が、始まりに釣り合わないほど大きくなったのは、炉の設計の欠陥のためである。
```

## ca10
- id `G7-039.1`：S1 p.33／23 の reactor control elements＝台本の呼び名「止める棒」にそろえ、画の欄の札も同じ語にした（字は増えない）。（A）
- id `G7-039.2`：S1 p.33／23 の reactor control elements＝台本の呼び名「止める棒」にそろえ、画の欄の札も同じ語にした（字は増えない）。（A）
```diff
-**ca10** ／ 図 模式（3つが重なる＝炉の物理の性質・制御の棒の設計・手順に定めのない状態へ持ち込んだこと） ／ S1 p.33／23（`not specified by procedures or investigated by an independent safety body`）
-> 事故は、3つが重なって起きた。炉の物理の性質、制御の棒の設計。
+**ca10** ／ 図 模式（3つが重なる＝炉の物理の性質・止める棒の設計・手順に定めのない状態へ持ち込んだこと） ／ S1 p.33／23（`not specified by procedures or investigated by an independent safety body`）
+> 事故は、3つが重なって起きた。炉の物理の性質、止める棒の設計。
```

## ca12
- id `G7-040.1`：decisions §3 の17＝G7-040 の語りを採り、S1 p.33／23 の is even considered by some to have been a precursor の片を出典の欄に足し、画の欄の札も「見る人もいる」にした。（B）
- id `G7-040.2`：decisions §3 の17＝G7-040 の語りを採り、S1 p.33／23 の is even considered by some to have been a precursor の片を出典の欄に足し、画の欄の札も「見る人もいる」にした。（B）
- id `G7-040.3`：decisions §3 の17＝G7-040 の語りを採り、S1 p.33／23 の is even considered by some to have been a precursor の片を出典の欄に足し、画の欄の札も「見る人もいる」にした。（B）
```diff
-**ca12** ／ 図 模式（前触れ＝1975年 レニングラード1号機→伝わらない→1986年 チェルノブイリ） ／ S1 p.33／23（`were not aware of the nature and causes of the accident at Leningrad Unit 1`）
-> 前触れもあった。1975年の、レニングラード1号機の事故である。
+**ca12** ／ 図 模式（前触れと見る人もいる＝1975年 レニングラード1号機→伝わらない→1986年 チェルノブイリ） ／ S1 p.33／23（`is even considered by some to have been a precursor`・`were not aware of the nature and causes of the accident at Leningrad Unit 1`）
+> 前触れと見る人もいる事故があった。1975年の、レニングラード1号機である。
```

## ca13
- id `G5-010`：decisions §3 の17＝S1 p.34／24 の the Soviet view … which laid blame almost entirely＝「ソ連の見方」を足し、G7-041 の言い方（cc18 と同じ「ほとんど運転員だけを責める見方の、重み」）にまとめた（＋1字）。（B）
```diff
-> そうではない。報告は、運転員をほとんど全面的に責めた見方は、
+> そうではない。報告は、ほとんど運転員だけを責めたソ連の見方の、
```

## ca14
- id `G5-011`：S1 p.34／24 の INSAG remains of the opinion that critical actions of the operators were most ill judged＝帰属を1文目に戻す（話の芯の釣り合いの文なので語り手の言い切りにしない）。（B）
```diff
-> だが続けて、運転員の決定的な操作は、きわめて判断を誤っていた。
+> だが続けて、運転員の決定的な操作は、きわめて判断を誤っていた、と見る。
```

## ca17
- id `G7-042`：decisions §3 の14＝S1 p.21／11 の Recent reports suggest that there was no operator error as such＝c406 と同じ推量に戻す。（B）
```diff
-> 運転員の誤りとは言えない。700メガワットより下は、禁止されていなかった。
+> 運転員の誤りとは言えないようだ。700メガワットより下は、禁止されていなかった。
```

## ca19
- id `G5-007.1`：S1 p.21／11 は値を知らなかったのは likely かつ during the critical part of the test・安全の上の意味を知らなかったのは言い切り（were not aware）、S1 p.34／24 は Most reprehensibly, unapproved changes … were deliberately made on the spot＝この3つを1語ずつ戻し、出典の欄に片を足した。（B）
- id `G5-007.2`：S1 p.21／11 は値を知らなかったのは likely かつ during the critical part of the test・安全の上の意味を知らなかったのは言い切り（were not aware）、S1 p.34／24 は Most reprehensibly, unapproved changes … were deliberately made on the spot＝この3つを1語ずつ戻し、出典の欄に片を足した。（B）
- id `R2-004`：S1 p.34／24「unapproved changes in the test procedure」＝試験の計画（c220 とそろえる）（B）
```diff
-**ca19** ／ イメージ Pexels（今の発電所の建屋の壁＝「イメージ：現在のチェルノブイリ原発」・映像方針で選ぶ） ／ S1 p.21／11（`it is likely that the operator did not know the value of the ORM`）
-> 残した棒の数は、違反だった。ただし運転員は、その値も、その意味も、
-> 知らなかった見込みが高い。試験の計画は、その場で変えられたことが責められた。
+**ca19** ／ イメージ Pexels（今の発電所の建屋の壁＝「イメージ：現在のチェルノブイリ原発」・映像方針で選ぶ） ／ S1 p.21／11（`it is likely that the operator did not know the value of the ORM`・`during the critical part of the test`）・S1 p.34／24（`Most reprehensibly, unapproved changes in the test procedure were deliberately made`）
+> 残した棒の数は、違反だった。ただ運転員は、その意味を知らず、
+> 試験の山場では、その値も知らなかった見込みが高い。
+> 承認なく、その場で計画をわざと変えたことが、いちばん強く責められた。
```

## ca20
- id `G5-028`：§4 の聞き役に数の語を置かない（「ゼロ」は数の網に掛からない）＝言い換えで1字減る。（A）
- id `G5-038`：打ち消しの根拠＝S1 p.34／24 の operating rules were violated・does not retract INSAG-1（文字の層で一致）を出典の欄に置く。（B）
```diff
-**ca20** ／ 図 模式（「無実」でも「うそ」でもない＝2つの札に×・真ん中に「重心が動いた」） ／ —
-> Q: 違反の数は減ったけど、ゼロにはならなかったんだ。
+**ca20** ／ 図 模式（「無実」でも「うそ」でもない＝2つの札に×・真ん中に「重心が動いた」） ／ S1 p.34／24（`operating rules were violated`・`does not retract INSAG-1`）
+> Q: 違反は減ったけど、なくなりはしなかったんだ。
```

## ca21
- id `G7-043`：decisions §2＝S1 p.34／24 の almost entirely・S2 p.18／~13 の in combination with specific reactor features＝1986年の説明が人だけを見たとは言わない。（B）
```diff
-> 変わったのは、重心だ。人だけを見る説明から、炉の作りと、
+> 変わったのは、重心だ。ほとんど人だけを責める説明から、炉の作りと、
```

## cb01
- id `G5-029`：ca23 の語りの問い「何人が亡くなったのか」を聞き役がくり返さない形にし、答え「答えは1つではない」がそのまま答える（数の語なし・反応でなく問い）。（C）
```diff
-> Q: 結局、この事故で、何人が亡くなったの？
+> Q: 亡くなった人の数も、はっきりしないの？
```

## cb03
- id `G5-031`：S3 p.42〜43／38〜39 の plant and emergency service personnel・among personnel stood at 28＝発電所の職員だけに聞こえないよう「作業員」にした（係の案より5字短い）。（A）
```diff
-> 職員のうち亡くなった人は、28人だった。
+> 作業員のうち亡くなった人は、28人だった。
```

## cb05
- id `G7-045`：c204・cb04・cb07・cb08 の「31人」にそろえる（K1 の三十一名＝数は同じ）。（A）
```diff
-> 11月の国会でも、ソ連の発表として、31名と答えている。
+> 11月の国会でも、ソ連の発表として、31人と答えている。
```

## cb06
- id `G7-046`：§4 の呼び名は「国連の科学委員会」（UNSCEAR の字は画の欄と §8 に残る）＝読みの決まっていない英字を語りから外す（7字返す）。（E）
```diff
-> のちの国連の科学委員会、UNSCEAR の2000年の報告は、30人とした。
+> のちの国連の科学委員会の、2000年の報告は、30人とした。
```

## cb08
- id `G5-025`：S2 p.115／~108 の the fatal outcome of the disease in 29 victims＝「内訳なし」は11月の国会の答弁の内訳（消防士かどうか）の話で言い過ぎ＝画の欄の字だけで直せる。（F）
- id `R2-012`：S2 p.115／~108 の片を出典の欄に（画の欄の29の根拠）（F）
```diff
-**cb08** ／ 図 模式（同じ31でも中身が違う＝ソ連の発表の31〈内訳なし〉とフォーラムの31〈28＋2＋1〉） ／ —
+**cb08** ／ 図 模式（同じ31でも中身が違う＝ソ連の発表の31〈うち急性放射線障害29＝1986年の報告〉とフォーラムの31〈28＋2＋1〉） ／ S2 p.115／~108（`the fatal outcome of the disease in 29 victims`）
```

## cb09
- id `G7-047`：§4 の帰属の呼び分け（UNSCEAR＝国連の科学委員会）＝L2 p.40／488 は UNSCEAR 2000。（A）
```diff
-> 国連の報告では、237人を調べ、134人が、この病気と確かめられた。
+> 国連の科学委員会によれば、237人を調べ、134人が、この病気と確かめられた。
```

## cb11
- id `G5-039.1`：🔴の直しで字が足りないので3行目を消し（cb12〜cb14 が違いを見せる）、出典の欄の片を cb15 と重ならない推計の片（L1 p.13／15 の文字の層で一致）に替えた。（C）
- id `G5-039.2`：🔴の直しで字が足りないので3行目を消し（cb12〜cb14 が違いを見せる）、出典の欄の片を cb15 と重ならない推計の片（L1 p.13／15 の文字の層で一致）に替えた。（C）
```diff
-**cb11** ／ 図 p8 L1（チェルノブイリ・フォーラム 図1＝ヨーロッパのセシウム137の地図の頁・図の頁・印刷10） ／ L1 p.13／15（`These predictions were based on the experience of other populations exposed to radiation`）
+**cb11** ／ 図 p8 L1（チェルノブイリ・フォーラム 図1＝ヨーロッパのセシウム137の地図の頁・図の頁・印刷10） ／ L1 p.13／15（`An international expert group has made projections to provide a rough estimate`）
-> そして、どこが推計したかで、大きく違う。
```

## cb12
- id `G5-004.1`：decisions §2 の形＝L1 p.13〜14／15〜16 の up to four thousand fatal cancers in addition to the approximately 100 000 fatal cancers … due to all other causes・eventually・might を「ほかの原因のおよそ10万人に加え、放射線のために…増える」「最終的に」「最大」「かもしれない」で残し、「死者」を使わず（m24 の「4,000人が亡くな」の形も避けた）、60万人も原文の receiving more significant exposures（最もではない）に合わせ、出典の欄に10万人の片を足した。（B）
- id `G5-004.2`：decisions §2 の形＝L1 p.13〜14／15〜16 の up to four thousand fatal cancers in addition to the approximately 100 000 fatal cancers … due to all other causes・eventually・might を「ほかの原因のおよそ10万人に加え、放射線のために…増える」「最終的に」「最大」「かもしれない」で残し、「死者」を使わず（m24 の「4,000人が亡くな」の形も避けた）、60万人も原文の receiving more significant exposures（最もではない）に合わせ、出典の欄に10万人の片を足した。（B）
```diff
-**cb12** ／ 実写 RIVM #02（CC0・オランダでの測定の別の1枚＝副題「オランダでの放射線の測定〈1986年5月1日〉」） ／ L1 p.14／16（`This might eventually represent up to four thousand fatal cancers`）
-> 2006年のフォーラムは、最も多く放射線を浴びた60万人について、
-> がんで亡くなる人が、最終的に最大4,000人になるかもしれないと推計した。
+**cb12** ／ 実写 RIVM #02（CC0・オランダでの測定の別の1枚＝副題「オランダでの放射線の測定〈1986年5月1日〉」） ／ L1 p.14／16（`This might eventually represent up to four thousand fatal cancers`・`in addition to the approximately 100 000`・`to be expected due to all other causes`）
+> 2006年のフォーラムは、多く放射線を浴びた60万人について、
+> がんで亡くなる人は、ほかの原因のおよそ10万人に加え、放射線のために、
+> 最終的に最大4,000人増えるかもしれないと推計した。
```

## cb13
- id `G5-016`：L8 p.5 の these cancers＝radiation from the accident による甲状腺がんとほかのがん＝語りに指す先が無いので中身を言う（cb12 の「放射線のために」と続くので「事故の」は省き、係の案より3字短く）。（A）
- id `R2-001`：L3 p.24／64 第98段落＝低い線量の人たちに限る＝図の札も cb14 の語りにそろえる（F）
```diff
-**cb13** ／ 図 比べ（長い年月の推計＝フォーラム 最大4,000人〈60万人〉／国際がん研究機関 約1万6,000人〈ヨーロッパ40か国・2065年まで〉／UNSCEAR 2008 推計しない） ／ L8 p.5／5（`about 16,000 deaths (95% UI 6,700 – 38,000) from these cancers may occur`）・L8 p.2／2（`The present analysis focused on 40 European`）
+**cb13** ／ 図 比べ（長い年月の推計＝フォーラム 最大4,000人〈60万人〉／国際がん研究機関 約1万6,000人〈ヨーロッパ40か国・2065年まで〉／UNSCEAR 2008 浴びた放射線の少ない人たちの数は出さない） ／ L8 p.5／5（`about 16,000 deaths (95% UI 6,700 – 38,000) from these cancers may occur`）・L8 p.2／2（`The present analysis focused on 40 European`）
-> およそ1万6,000人が、これらのがんで亡くなるかもしれないと推計した。
+> およそ1万6,000人が、放射線によるがんで亡くなるかもしれないと推計した。
```

## cb14
- id `G5-018`：L3 p.24／64 第98段落は in populations exposed to low radiation doses に限る＝多く浴びた60万人まで出さないと決めたように聞こえる範囲の広げを戻す。（B）
- id `G7-049`：G7-046 と同じ（§4 の呼び名・読みの決まっていない英字を語りから外す・7字返す）。（E）
```diff
-> 一方、2008年の国連の科学委員会、UNSCEAR は、
-> こうした推計の数を出さない、と決めた。
+> 一方、2008年の国連の科学委員会は、
+> 浴びた放射線の少ない人たちの推計の数は、出さないと決めた。
```

## cb15
- id `G7-050.1`：decisions §3 の16＝L1 p.13／15 に such as the survivors of the atomic bombing in Hiroshima and Nagasaki が文字の層にある＝係の案の語りを採り（「死者」をやめ、cb21 と重なる文を消す）、出典の欄にその片を足した。（D）
- id `G7-050.2`：decisions §3 の16＝L1 p.13／15 に such as the survivors of the atomic bombing in Hiroshima and Nagasaki が文字の層にある＝係の案の語りを採り（「死者」をやめ、cb21 と重なる文を消す）、出典の欄にその片を足した。（D）
- id `R2-010`：L1 p.13／15「based on the experience of other populations」＝問いに次の語りがそのまま答える（C）
```diff
-**cb15** ／ 図 模式（推計の作り＝ほかに放射線を浴びた人たちの経験→計算→推計の数＝「数えた数」ではない） ／ L1 p.13／15（`These predictions were based on the experience of other populations exposed to radiation`）
-> Q: じゃあ、どの推計が正しいの？
-> どれも、ほかに放射線を浴びた人たちの経験から作った計算で、
-> 数えた死者ではない。出どころを添えて言うしかないのである。
+**cb15** ／ 図 模式（推計の作り＝ほかに放射線を浴びた人たちの経験→計算→推計の数＝「数えた数」ではない） ／ L1 p.13／15（`These predictions were based on the experience of other populations exposed to radiation`・`such as the survivors of the atomic bombing in Hiroshima and Nagasaki`）
+> Q: 推計は、何をもとにしているの？
+> どれも、広島と長崎の被爆者など、ほかで放射線を浴びた人たちの、
+> 経験から作った計算で、実際に数えた人数ではない。
```

## cb16
- id `G5-027`：🔴の直しで字が足りないので使う＝この章は数の章で、薬の配布（S2 p.100／~93）は言わなくても甲状腺がんの話が通る。（C）
- id `G5-037`：S2 p.100 の頁頭は「- 93 -」＝ほかの S2 の出典と同じ書き方にそろえる。（B）
```diff
-**cb16** ／ 図 p15 L1（フォーラム 図3＝子どもの甲状腺がんのグラフの頁・図の頁・印刷17） ／ S2 p.100（`accumulation of radionuclides of iodine in the thyroid glands`）
+**cb16** ／ 図 p15 L1（フォーラム 図3＝子どもの甲状腺がんのグラフの頁・図の頁・印刷17） ／ S2 p.100／~93（`accumulation of radionuclides of iodine in the thyroid glands`）
-> 1986年には、それを防ぐための薬も配られた。
```

## cb17
- id `G5-019`：L4 p.7／v (c) の The Committee estimated＝帰属は §4 の「国連の科学委員会」（係の案の「国連」では呼び名が外れ、1行に入らない）なので、2行目の終わりを「、」にして3行目の頭で名乗った。（B）
- id `G5-035`：L4 p.20／12 の 0.6 and 0.25 for the evacuated and non-evacuated children and adolescents（文字の層で一致）＝要約を片に替える。（B）
```diff
-**cb17** ／ 図 模式（甲状腺がん＝およそ2万例の帯・放射線によるものの見積もり〈およそ4分の1・幅は7%〜50%〉を色で） ／ L4 p.7／v（`registered in the period 1991−2015 in males and females, who were under 18 in 1986`・`The uncertainty range of the estimated attributable fraction extends at least from 0.07 to 0.5`）・L4 p.20／12（「避難しなかった人で 0.25」＝要約）
+**cb17** ／ 図 模式（甲状腺がん＝およそ2万例の帯・放射線によるものの見積もり〈およそ4分の1・幅は7%〜50%〉を色で） ／ L4 p.7／v（`registered in the period 1991−2015 in males and females, who were under 18 in 1986`・`The uncertainty range of the estimated attributable fraction extends at least from 0.07 to 0.5`）・L4 p.20／12（`0.6 and 0.25 for the evacuated and non-evacuated children and adolescents`）
-> 放射線によるものは、避難しなかった人で、およそ4分の1と見積もられている。
-> ただし幅は大きく、少なくとも7%から50%まである。
+> 放射線による分は、避難しなかった人で、およそ4分の1と、
+> 国連の科学委員会は見積もる。ただし幅は大きく、少なくとも7%から50%まである。
```

## cb19
- id `G7-051`：§4 の呼び名だけを直した（L2 p.25／473 は UNSCEAR 1988 も135,000 を引いた＝「まとめ直している」は原文どおりなので言い回しは残す・係の案より字が少ない）。（A）
```diff
-> のちの国連の報告は、それより少し少ない数に、まとめ直している。
+> のちの国連の科学委員会は、それより少し少ない数に、まとめ直している。
```

## cb20
- id `G5-033`：L2 p.5／453 の24万人は避難した人とは別の作業の人＝「こうした数の外」は60万人の外に聞こえる。（A）
- id `G5-036`：L2 p.5／453 の about 240,000 workers・were called upon in 1986 and 1987 to take part in major mitigation activities（文字の層で一致）＝要約を片に替える。（B）
- id `G7-052`：G7-047 と同じ（§4 の帰属の呼び分け＝L2 は UNSCEAR 2000）。（A）
```diff
-**cb20** ／ 実写 Commons 現在の4号炉-ツ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ L2 p.5／453（「事故の処理にあたった人＝1986〜87年におよそ24万人」＝要約）
+**cb20** ／ 実写 Commons 現在の4号炉-ツ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ L2 p.5／453（`about 240,000 workers`・`were called upon in 1986 and 1987 to take part in major mitigation activities`）
-> そう。そして、こうした数の外に、事故の片づけにあたった大勢の人がいる。
-> 国連の報告では、1986年と87年だけで、およそ24万人である。
+> そう。そして、避難した人とは別に、事故の片づけにあたった大勢の人がいる。
+> 国連の科学委員会によれば、1986年と87年だけで、およそ24万人である。
```

## cc01
- id `G6-011`：decisions §3 の20（cc01 の問いを替える）：cb23 の語りと同じ問いを繰り返さないよう問いを替え、次の語りの頭に「違う。」を置いて問いにそのまま答える（係の案の「そのまま」を外して字を増やさない・章の頭の聞き役は残す）（C）
```diff
-> Q: 壊れた炉は、そのあと、どうなったの？
-> コンクリートと鉄の建物で、まるごと覆われた。石棺と呼ばれる。
+> Q: 壊れた炉は、放っておかれたの？
+> 違う。コンクリートと鉄の建物で、まるごと覆われた。石棺と呼ばれる。
```

## cc03
- id `G6-010`：S2 p.11／~6（At the same time, Unit 3 … was shut down＝5時・Units 1 and 2 … early in the morning of 27 April）と S3 p.32／28（Unit 3 … was shut down at 05.00 on 26 April）で、cc04 の「3号機も」の前提を足す。係の案（+4字）を縮め、「1号機と2号機」の繰り返し（G7-054）も同じ直しで消した（3号機の再開は1987年12月なので「その年の秋」は言わず「やがて」）（B）
```diff
-**cc03** ／ 実写 Commons 現在の4号炉-テ（2013年の BY-SA の1点＝1〜3号機の建屋の側・額装・⑤b で選ぶ＝副題「現在の発電所〈2013年〉」） ／ S2 p.11／~6（`Units 1 and 2 were shut down early in the morning of 27 April`）
-> 同じ発電所の1号機と2号機は、27日の早朝に止められた。
-> だが1号機と2号機は、その年の秋に、また動き始める。
+**cc03** ／ 実写 Commons 現在の4号炉-テ（2013年の BY-SA の1点＝1〜3号機の建屋の側・額装・⑤b で選ぶ＝副題「現在の発電所〈2013年〉」） ／ S2 p.11／~6（`Units 1 and 2 were shut down early in the morning of 27 April`）・S3 p.32／28（`was shut down at 05.00 on 26 April`）
+> 同じ発電所のほかの3つの号機は、26日の朝から27日の早朝にかけて止められた。
+> だが、やがて、また動き始める。
```

## cc06
- id `G6-012.1`：L10 p.12／1 は Events are classified on the scale at seven levels: Levels 4–7 … accidents and Levels 1–3 incidents・Below Scale/Level 0＝「事故の重さ」「8段」は言い過ぎなので「出来事」「0から7の段」にした（係の案の「までの」は字が増えるので外した）。画の欄の「8段」も同じ原文に合わせた（B）
- id `G6-012.2`：L10 p.12／1 は Events are classified on the scale at seven levels: Levels 4–7 … accidents and Levels 1–3 incidents・Below Scale/Level 0＝「事故の重さ」「8段」は言い過ぎなので「出来事」「0から7の段」にした（係の案の「までの」は字が増えるので外した）。画の欄の「8段」も同じ原文に合わせた（B）
- id `G7-055`：decisions §3 の3＝正式名は語りから外し INES で言う（§8 の概要欄に正式名を残す＝G7-063 の直しで足した）（A）
```diff
-**cc06** ／ 図 模式（INES の物差し＝0から7の8段・7に「チェルノブイリ 1986年」） ／ L10 p.12／1（`The scale was developed in 1990 by international experts convened by the IAEA`）・L10 p.13／2（`accident at the Chernobyl nuclear power plant is rated at Level 7 on INES.`）
-> 原子力の事故の重さを、0から7の8段で表す物差しがある。
-> 国際原子力・放射線事象評価尺度、INES だ。できたのは1990年。
+**cc06** ／ 図 模式（INES の物差し＝0から7の段〈4〜7が事故・1〜3はそれより軽い出来事・0は尺度より下〉・7に「チェルノブイリ 1986年」） ／ L10 p.12／1（`The scale was developed in 1990 by international experts convened by the IAEA`）・L10 p.13／2（`accident at the Chernobyl nuclear power plant is rated at Level 7 on INES.`）
+> 原子力の出来事の重さを、0から7の段で表す物差しがある。
+> INES と呼ばれ、できたのは1990年である。
```

## cc11
- id `G6-004`：🔴 G0 がウェブで確かめた：2025-02-14 に無人機が新しい覆いに当たり（国連ニュース 2025-02-14「could see a breach of the outer layer of the NSC」）、IAEA は 2025年12月に「lost its primary safety functions, including the confinement capability」と評価（NucNet 2025-12-08・IAEA GOV/2026/7 も同旨）＝「いまも、そのまま残っている」は言い過ぎ。問いを替える（B）
- id `G6-017`：G0：字に余りがある（直す係6本を重ねて上限まで約60字）＝受け手は事業者の頁 2019-07-11「to the Client, i.e. the SSE "Chornobyl NPP"」で G0 が確かめた（A）
```diff
-> 引き渡されたのは、2019年7月。事故から33年がたっていた。
-> Q: いまも、そのまま残っているの？
+> 発電所へ引き渡されたのは、2019年7月。事故から33年がたっていた。
+> Q: そのあとも、何か起きたの？
```

## cc12
- id `G6-005.1`：G6-004 と組。2022年は WNN 2022-04-01「Ukraine informed the IAEA on 31 March … in writing」＝ウクライナの通知に帰属（3月31日は伝えた日）。2025年の件を1行（帰属は出典の欄＝IAEA の評価）（C）
- id `G6-005.2`：G6-004 と組。2022年は WNN 2022-04-01「Ukraine informed the IAEA on 31 March … in writing」＝ウクライナの通知に帰属（3月31日は伝えた日）。2025年の件を1行（帰属は出典の欄＝IAEA の評価）（C）
```diff
-**cc12** ／ イメージ Pexels 30560422（プリピャチの観覧車＝「イメージ：現在のプリピャチ（Pexels）」） ／ WEB IAEA Update 38（World Nuclear News 2022-04-01 の写し）（「transferred control of Chernobyl nuclear power plant to Ukrainian personnel」）
-> 残っている。2022年には、ロシア軍が2月24日から発電所を支配し、
-> 3月31日、管理をウクライナの職員に書面で引き渡した。
+**cc12** ／ イメージ Pexels 30560422（プリピャチの観覧車＝「イメージ：現在のプリピャチ（Pexels）」） ／ WEB IAEA Update 38（World Nuclear News 2022-04-01 の写し）（「transferred control of Chernobyl nuclear power plant to Ukrainian personnel」）・WEB 国連ニュース 2025-02-14（「could see a breach of the outer layer of the NSC」）・WEB NucNet 2025-12-08＝IAEA の評価の写し（「lost its primary safety functions, including the confinement capability」）
+> 起きた。2022年には、ロシア軍が2月24日から発電所を支配した。
+> 管理を書面で職員に戻した、と3月31日にウクライナが伝えた。
+> 2025年2月、無人機がアーチに当たり、閉じ込める働きを失ったとされる。
```

## cc13
- id `G6-014`：decisions §3 の18：図1 の題（S1 p.15／5 の文字の層＝(a) before and (b) after the improvements made in response to the Chernobyl accident）と、棒を改めた付属書II（p.135／125 the manual control rods were replaced with ones of improved design）を出典の欄に足す（語りは変えない）（B）
- id `G0-004`：cc12（2025年の無人機）から cc13（棒の改良）へ橋が無い（F6 の親へ・G6-014 の parent）＝話を戻す一言
```diff
-**cc13** ／ 図 模式（事故のあとの棒の改良＝図1 の (b)・入りきるまで12秒・速く止める棒＝c903 と別の絵） ／ S3 p.28／24（`as the rods move down from the upper stops`）
-> 事故のあと、RBMK の止める棒は改められた。
+**cc13** ／ 図 模式（事故のあとの棒の改良＝図1 の (b)・入りきるまで12秒・速く止める棒＝c903 と別の絵） ／ S3 p.28／24（`as the rods move down from the upper stops`）・S1-図1 p.15／5（`(a) before and (b) after the improvements made in response to the Chernobyl accident`）・S1-付属書II p.135／125（`the manual control rods were replaced with ones of improved design`）
+> 話を棒に戻そう。事故のあと、RBMK の止める棒は改められた。
```

## cc14
- id `G6-013`：答えは S1 p.35／25 の broader problems contributing to the accident の1つで教訓ではない＝問いを答えに合わせる案を採り、「根っこ」の出どころの 6(5)（S1 p.33／23 flowed from deficient safety culture）を出典の欄に足した（C）
```diff
-**cc14** ／ 実写 Commons 現在の4号炉-ナ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S1 p.35／25（`lack of safety culture in nuclear matters, at the national level as well as locally`）
-> Q: この事故から、何を学んだの？
+**cc14** ／ 実写 Commons 現在の4号炉-ナ（2013年の BY-SA の1点＝額装・⑤b で選ぶ＝副題「現在の4号炉〈2013年〉」） ／ S1 p.35／25（`lack of safety culture in nuclear matters, at the national level as well as locally`）・S1 p.33／23（`The accident can be said to have flowed from deficient safety culture`）
+> Q: 事故の根っこには、何があったの？
```

## cc15
- id `G6-001`：decisions §2 の🔴どおり：0時28分（S2 p.36／~33・S1 p.21／11）と1時23分40秒（S2 p.31／~28・S3 p.21／17）はどの報告でも同じで、c504・c510 の2つの保護の時刻は S1 p.21／11・p.22／12 で書き直された＝「どの報告でも」を外して2つの時刻に限った案を採る（S3 は0時28分の数字を持たないので「どの報告でも」を残さない）（B）
```diff
-> 事故の夜の時刻は、どの報告でも、ほとんど変わらない。
+> 0時28分も1時23分40秒も、時刻そのものは変わらない。
```

## cc16
- id `G6-007`：S1 p.26／16 の The most likely final event now seems to have been the insertion of safety rods は「かもしれない」より強く、c919（G4-019）の「いちばんありそう」とそろえて「とみられる」に戻す（断定にはしない）。読みの G7-058 の「ひと押し」（c919 と同じかな）も同じ行で入れた（B）
- id `G6-008`：「誤りとは言えないへ」は文の形が崩れていて耳で切れ目がつかめない＝2行目の「〜ものへ」とそろえる（意味は S1 p.21／11 の no operator error as such のまま・+2字）（A）
- id `R2-003`：S1 p.21／11「suggest」＝ca17 の「ようだ」と同じ強さに（結びで断定に戻さない）（B）
```diff
-> 0時28分の急落は、運転員の誤りから、誤りとは言えないへ。
-> 1時23分40秒のボタンは、止める操作から、最後の一押しかもしれないものへ。
+> 0時28分の急落は、運転員の誤りから、誤りとは言えないらしいものへ。
+> 1時23分40秒のボタンは、止める操作から、最後のひと押しとみられるものへ。
```

## cc17
- id `G6-006`：S1 p.34／24 の Most reprehensibly, unapproved changes … deliberately made on the spot と p.26／16 の It is reprehensible that such a deficiency had been known of for so long で、責めの語を人と設計の両方に当てる（人の要素は大きい＝ca14 で言いずみ）。係の案の「試験の計画をその場で変えた」は reprehensible の根の unapproved を落とすので、4'-18 で「承認なしに」を残した自分の文にした（B）
- id `R2-005`：S1 p.34／24「deliberately」＝結びの天秤で人の側の決め手を落とさない（寄せない）（B）
```diff
-**cc17** ／ 図 模式（天秤＝人と設計の両方が載る） ／ S1 p.34／24（`the human factor has still to be considered as a major element`）
+**cc17** ／ 図 模式（天秤＝人と設計の両方が載る） ／ S1 p.34／24（`Most reprehensibly, unapproved changes in the test procedure were deliberately made`）・S1 p.26／16（`It is reprehensible that such a deficiency had been known of for so long`）
-> どちらか1つではない。1992年の報告も、人の要素は大きいと書き、
-> 棒の欠陥を長く残したことは、責められるべきだと書いた。
+> どちらか1つではない。1992年の報告は、承認なしに計画をわざと変えたことも、
+> 棒の欠陥を長く残したことも、責められるべきだと書いた。
```

## cc18
- id `G6-009`：decisions §3 の17（ca13・cc18 を「ソ連の見方」にそろえる）どおり：S1 p.34／24 は The weight given in INSAG-1 … to the Soviet view …, which laid blame almost entirely on actions of the operating staff, is thereby lessened＝ほとんど運転員だけを責めたのはソ連の見方（B）
- id `G7-059`：「原因は運転員」のかぎ括弧は原文の引用に見える（S2 p.112／~105 は so-called human element）＝括弧だけを外し、字を増やさない言い方にした（角度の言い方は変えない）（A）
- id `R2-011`：S2 p.18／~13「in combination with specific reactor features」＝「原因を運転員とした」は ca21 で直した言い過ぎ＝運転員の側に置いた（B）
```diff
-> 「原因は運転員」とした報告は、6年後に書き直された。
-> 書き直されたのは、ほとんど運転員だけを責める見方の、重みである。
+> 原因を運転員の側に置いた報告は、6年後に書き直された。
+> 書き直されたのは、ほとんど運転員だけを責めたソ連の見方の、重みである。
```

## cc19
- id `G6-016`：意味は変わらず字を5字返せる（S1・S2 の URL は出典の欄のまま）（A）
```diff
-> 2つの報告も、いまも国際原子力機関のサイトで読むことができる。
+> 2つの報告も、いまも国際原子力機関のサイトで読める。
```

## cc20
- id `G7-060`：「2つの報告の答え」は1986年の報告も同じ答えを出したと聞こえる＝重心が動いた（S1 p.33／23 shift the emphasis・p.34／24 the balance … has shifted）は2つを読み比べて見えること、と分かる言い方にした（G6-015 と同じ直し）（C）
```diff
-> ただし、人の側から消えたわけではない。それが、2つの報告の答えである。
+> ただし、人の側から消えたわけではない。それが、2つの報告を読み比べた答えである。
```

## cc21
- id `G7-061`：語順だけの直し（decisions §1・§3 の20 の答え＝問いの中身は承認①で決める）（A）
```diff
-> あなたは、チェルノブイリ原発事故の原因を、この動画を見る前は、
+> あなたは、この動画を見る前、チェルノブイリ原発事故の原因を、
```

## カットの外（§1〜§3・§5〜・章の見出し。頭と §0 は除く）
- id `F6-001`：§6 の行を語りに合わせる：定格（G7-013＝c211 は「最大の」）と ORM（G7-017＝c302 は「残した棒」）は語りから外れた（decisions §3 の2・3）
- id `F6-002`：§6 の行を語りに合わせる：国際原子力・放射線事象評価尺度は G7-055 で語りから外れた（decisions §3 の3）
- id `F6-003`：§5 の2022年の行を cc12 の新しい字（fix_G0 の G6-005＝ウクライナの通知に帰属）に合わせる
- id `G6-003`：decisions §2（c603 は G3-004 で「15本の、およそ半分」）に合わせ、§9 の言い方を G3-004 の字にそろえ、S3 の half の基準（p.23／19 と p.26／22 の fewer than 30 rods）を式の欄に書いた（B）
- id `G6-021.1`：decisions §3 の19 の URL（G0 が原ページで確かめた9本）を §10 の WEB の行（7本）と R3・R4 の行（外務省の2本）に書き写し、git の外の scratchpad を正本にしない（B）
- id `G6-021.2`：decisions §3 の19 の URL（G0 が原ページで確かめた9本）を §10 の WEB の行（7本）と R3・R4 の行（外務省の2本）に書き写し、git の外の scratchpad を正本にしない（B）
- id `G6-022`：日付の引き算で確かめた（1986-04-26→2000-12-15＝14年7か月19日・→2019-07-10＝33年2か月14日）＝§9 の式だけ直す・語りは合う（B）
- id `G6-023`：係が検算した換算（6年・3日後・4か月・5日間・4か月のうち）に、c615（表I-I＝01:23:40→01:23:43）と c811（S2 p.2＝30 August - 5 September 1986）を F6 が引いて確かめた2行を足し、§9 の末に並べた（c717 の「4か月」は §3 の10 で外れるので書かない）（B）
- id `G6-024`：decisions §3 の19 で G0 が確かめたのは EBRD 2016-11-29 の頁の 327 metres（cc10）で、大きさの値は確かめていない＝§5 の理由をその範囲で書き直し、語りに要らない（尺）を理由に足した（B）
- id `G7-062`：decisions §3 の21・§3 の7：§6 に通し読みの挙げた語と c403 の「20分の1」と F6 の直し（cc03）の語を足した（一押しは c919・cc16 ともかなの「ひと押し」にしたので行は要らない・被爆者は G5 の採否しだい）（E）
- id `G7-063.1`：decisions §3 の21・§3 の3：§8 に4語を足し（S3 p.3／-1 の表紙・S1 p.39／29〜p.40／30 の付属書Iの名乗り・S1 p.66／56・p.125／115 の SKALA・L8 p.1 の見出しと p.7 の所在地）、INES の行に正式名と段の呼び分け（L10 p.12／1）を入れた（C）
- id `G7-063.2`：decisions §3 の21・§3 の3：§8 に4語を足し（S3 p.3／-1 の表紙・S1 p.39／29〜p.40／30 の付属書Iの名乗り・S1 p.66／56・p.125／115 の SKALA・L8 p.1 の見出しと p.7 の所在地）、INES の行に正式名と段の呼び分け（L10 p.12／1）を入れた（C）
- id `G0-005`：§1-1 に ④' の推奨 B' と理由（G7-001〜003・公開ずみの題と型を照らした＝4'-8）
- id `G0-006`：§1-2 に ④' の見立て（G7-004〜006）
- id `G0-007`：§1-3 に ④' の見立て（G7-007〜009・G7-061）
- id `G0-008`：§1-5 のドラムの保護を c504・c505 の第2版に（G0-001）
- id `G0-009`：§1-5 の出力の倍数を c922 の第2版に（G4-022＝比べるもとが違う）
- id `G0-010`：§1-5 の 1:22:30 の残した棒を c603 の第2版に（G3-004）
- id `G0-011`：§1-5 の長期の推計を cb12 の第2版に（G5-004＝上乗せの数）
- id `G0-012`：§1-5 の2022年を cc12 の第2版に＋2025年の行（G6-004・G6-005）
- id `R2-002`：R2-001 と組＝§1-5（図の札もこの値）（B）
- id `R2-013`：§6＝UNSCEAR は語りから外れた（E）
- id `R2-014`：§6＝cb15 に被爆者が入った（G7-050）（E）
- id `R2-015`：§9＝ca05 の1988年は語りから消えた（G5-026）（B）
- id `R2-016`：§5＝ca12 の言い方（前触れと見る人もいる）にそろえる（B）
- id `R2-017`：§8＝c906 から外した「入り始めた数秒」を概要欄からも外す（S1 p.14／4）（B）
- id `R2-018`：§1-5＝ca07 が同じ節を時刻と値なしで言うことを書く（B）
- id `R2-019`：§5＝R2-018 と組（B）
```diff
+| **B'（④'の推奨）** | 爆発した4号炉、止めるはずの棒には、2年半ほど前に見つかっていた欠陥があった。チェルノブイリ原発事故の真相【事故検証】【ゆっくり解説】 | 67 | c105・c911〜c913（付属書I p.53／43＝1983年11〜12月→1986年4月＝2年4〜5か月＝「ほど」）・G7-002 |
+- 🆕 **④'（10-22）：推奨を B' に替えた**（G7-001〜003）＝A は「違反ではなかった」が「運転員は無実」と読まれやすい／B は「2年半前」が「ほど」を落とし、頭に事件の絵の語が無い／C は「」が原文の引用に見え、書き直しが撤回に読める。公開ずみの21〜23本目の題（49〜70字・事実の1句＋〈事件名〉の真相【事故検証】【ゆっくり解説】）と型を照らした＝A（62字）・B'（67字）とも型の内。**承認①で決める**
+- 🆕 ④'（10-22）：推奨は **A のまま**（G7-004＝題 B' と別の入口になる）。B は「犠牲31人」と並ぶと棒の欠陥が亡くなった人の因果に読める（G7-005）・C は責める相手を作る（G7-006）。**承認①で決める**
+- 🆕 ④'（10-22）：推奨は **A のまま**（G7-007）。cc21 は語順だけ直した＝「あなたは、この動画を見る前、チェルノブイリ原発事故の原因を、…」（G7-061）。B は角度とつながらない・C はどの回にも使える。**承認①で決める**
-| ドラムの保護 | 0時36分（c504） | INSAG-1 1:19（c503） | S1 p.22／12 |
+| ドラムの保護 | 0時36分＝圧力の保護の設定（c504・表I-I 00:36:24＝手順の内）／水位の設定を切り替えなかったのは違反だが事故の原因ではない（c505＝1991年の委員会） | INSAG-1 1:19（c503）・INSAG-7 本文 (6) は2つを1つの文で書く | S1 p.22／12・p.64／54・p.85／75・p.88／78 |
-| 出力の倍数 | 1986年の報告 100倍（4秒以内）・のちの計算 3.5倍から80倍（c922） | 付属書I の数十倍・約30倍・31倍か64倍は言わない | S2 p.10／~5・付属書II p.131／121 |
-| 1:22:30 の残した棒 | 6本から8本（c603） | 表I-I 8本（事故のあとの計算）は出典の欄だけ・1.9本・7本は言わない | S3 p.23／19・S1 p.64／54 |
-| 25日の残した棒 | 7時10分 13.2本（c305） | 付属書I 1-4.7.1「7時ごろ15本」は言わない | 表I-I p.63／53 |
+| 出力の倍数 | 1986年の報告 最大の出力（定格・nominal）の100倍（4秒以内）・のちの計算 はじめの出力（initial value）の3.5倍から、およそ80倍（approximately は80倍だけ＝R2-020）＝比べるもとが違う（c922） | 付属書I の数十倍・約30倍・31倍か64倍は言わない | S2 p.10／~5・付属書II p.131／121 |
+| 1:22:30 の残した棒 | 6本から8本＝即時停止の15本の「およそ半分」（c603。S3 の not more than half は S3 の決まり〈30本〉に対して＝15本の半分以下とは言わない） | 表I-I 8本（事故のあとの計算）は出典の欄だけ・1.9本・7本は言わない | S3 p.23／19・S1 p.64／54 |
+| 25日の残した棒 | 7時10分 13.2本（c305） | 付属書I 1-4.7.1「7時ごろ15本」の時刻と値は言わない（ca07 は同じ節を「15本まで減っても止めなかった」＝止める決まりを守らなかったこととして言う） | 表I-I p.63／53 |
-| 長期の推計 | フォーラム 最大4,000人・IARC 約1万6,000人・UNSCEAR 2008 は推計しない（cb12〜cb14） | 9万3,000人（グリーンピース）は扱わない | L1・L8・L3 |
+| 長期の推計 | フォーラム 最大4,000人（60万人で、ほかの原因のがんの約10万人に**加えて**放射線で増える分＝L1 p.14／16）・IARC 約1万6,000人・UNSCEAR 2008 は浴びた放射線の少ない人たちの数を出さない（cb12〜cb14・L3 p.24／64 第98段落） | 9万3,000人（グリーンピース）は扱わない | L1・L8・L3 |
-| 2022年 | 2月24日から支配・3月31日に管理を書面で引き渡した（cc12） | 「全員が去った」は言わない | IAEA Update 38（WNN の写し） |
+| 2022年 | 2月24日から支配・3月31日に「書面で管理を職員に戻した」とウクライナが IAEA に伝えた（cc12＝ウクライナの通知に帰属） | 「全員が去った」は言わない | IAEA Update 38（WNN 2022-04-01 の写し） |
+| 🆕 2025年 | 2月14日 無人機が新しい覆い（アーチ）に当たった・12月 IAEA「閉じ込めの働きを含む主な安全の働きを失った」（cc12＝「とされる」） | 支える骨組みと監視の系は恒久の損傷なし・仮の屋根の直し＝語りでは言わない（尺） | 国連ニュース 2025-02-14・NucNet 2025-12-08・IAEA GOV/2026/7（2026-02-25） |
-| 25日の「7時ごろ15本」（付属書I 1-4.7.1） | 表I-I の7時10分 13.2本と割れる＝表の値だけ |
+| 25日の「7時ごろ15本」（付属書I 1-4.7.1） | 表I-I の7時10分 13.2本と割れる＝表の値だけ（ca07 は同じ節の「15本まで減っても止めなかった」を決まりの下限として言う＝時刻と値は言わない） |
-| 1975年のレニングラード1号機の事故の中身・公式の原因 | 尺＝ca12 は「前触れがあった・職員は知らなかった」まで |
+| 1975年のレニングラード1号機の事故の中身・公式の原因 | 尺＝ca12 は「前触れと見る人もいる・職員は知らなかった」まで |
-| 新しい覆いの大きさ（幅257m・長さ162m・高さ108m・36,000トン） | EBRD の頁の値（係C）＝原ページの字を見ていない＝言わない |
-| 2022年の「全員が去った」 | IAEA の原ページが開けず二次だけ（係C）＝「管理を書面で引き渡した」まで |
+| 新しい覆いの大きさ（幅257m・長さ162m・高さ108m・36,000トン） | EBRD の頁の値（係C）＝G0 が原ページで確かめたのは 2016-11-29 の頁の 327 metres（cc10）だけで、大きさの字は見ていない・語りにも要らない（尺）＝言わない |
+| 2022年の「全員が去った」 | IAEA の原ページが開けず二次だけ（係C）＝「管理を書面で職員に戻した、とウクライナは伝えている」まで（cc12） |
-| 定格 | ていかく | c211 |
-| 運転反応度余裕・ORM | うんてんはんのうどよゆう・オーアールエム | c302 |
+| 定格 | （語りから外した＝c211 は「最大の出力」） | ─ |
+| 運転反応度余裕・ORM | （語りから外した＝c302 は「残した棒」・§8 の概要欄だけ） | ─ |
-| UNSCEAR | アンスケア（⑤a で決める） | cb06・cb14 |
+| UNSCEAR | （語りから外した＝cb06・cb14 は「国連の科学委員会」・画の欄と §8 だけ） | ─ |
-| 国際原子力・放射線事象評価尺度 | こくさいげんしりょく・ほうしゃせんじしょうひょうかしゃくど | cc06 |
+| 国際原子力・放射線事象評価尺度 | （語りから外した＝§8 の概要欄だけ） | ─ |
+| 人的要素 | じんてきようそ | c103・c813 |
+| 私信 | ししん | c408 |
+| 事故後検討会議 | じこごけんとうかいぎ | c802 |
+| 鉛 | なまり | cc02 |
+| 1.2メートル | いってんにメートル | c822 |
+| 20分の1 | にじゅうぶんのいち | c403 |
+| レベル7・0から7の段 | レベルなな・ゼロからななのだん | cc06〜cc09 |
+| 8本・8台・6台・30か所・2万例 | はっぽん・はちだい・ろくだい・さんじゅっかしょ・にまんれい | c603・c419・c421・c702・cb17 |
+| ほかの3つの号機・26日の朝・27日の早朝 | みっつのごうき・にじゅうろくにちのあさ・にじゅうしちにちのそうちょう | cc03 |
+| 被爆者 | ひばくしゃ | cb15 |
-- ポジティブ・スクラム…抜き切った制御棒が入り始めた数秒、炉の下の方で反応をかえって強めてしまう現象
+- ポジティブ・スクラム…抜き切った制御棒が入り始めに、炉の下の方で反応をかえって強めてしまう現象（強さは出力の分布と運転の状態しだい）
-- INES…原子力の事故の重さを、0から7の8段で表す物差し（1990年にできた）
+- INES（国際原子力・放射線事象評価尺度）…原子力や放射線の出来事の重さを、0から7の段で表す物差し（1990年にできた）。4〜7が「事故」、1〜3はそれより軽い出来事、0は安全の上で意味のない出来事
+- 1986年8月のソ連の報告…ソ連の原子力利用国家委員会が、1986年8月25〜29日にウィーンで開かれた IAEA の会議（事故後検討会議）のためにまとめた資料
+- 1991年の委員会…ソ連の産業・原子力安全監督国家委員会が設けた委員会。その報告（モスクワ・1991年）は、1992年の報告（INSAG-7）に付属書Iとして収められた
+- SKALA…発電所の集中制御の計算機のしくみ。残した棒の数（ORM）など炉の主な値を、およそ5分ごとに計算した
+- 国際がん研究機関（IARC）…世界保健機関（WHO）の、がんを研究する機関（フランスのリヨン）。2006年に、ヨーロッパでの事故によるがんの見積もりを出した
-| c603 | 15本の半分以下 | 6〜8÷15＝0.4〜0.53（S3「not more than half of the minimum permissible value」） |
+| c603 | 15本の、およそ半分 | 6〜8÷15＝0.4〜0.53（S3 の not more than half〈p.23／19〉は S3 の決まりの30本〈p.26／22 fewer than 30 rods〉に対して＝15本には当てない） |
-| ca05 | 2年後の1988年 | 1986→1988（写真の説明 02790055） |
-| cc05 | 事故から14年あまり | 1986年4月→2000年12月15日＝14年8か月 |
-| cc11 | 事故から33年 | 1986年4月→2019年7月＝33年3か月 |
+| cc05 | 事故から14年あまり | 1986年4月26日→2000年12月15日＝14年7か月あまり |
+| cc11 | 事故から33年 | 1986年4月26日→2019年7月10日＝33年2か月あまり |
+| c104・c819・cc18・cc20 | 6年後・6年かけて | 1986年（1986年の報告＝9月）→1992年（1992年の報告）＝6年 |
+| c615 | その3秒後 | 1:23:40→1:23:43（S1-表I-I p.65／55）＝3秒 |
+| c711 | 事故から3日後の29日 | 4月26日→29日＝3日 |
+| c802 | 8月25日からの5日間・事故から4か月 | 25〜29日＝5日（S2 p.1 from 25 to 29 August 1986）・4月26日→8月25日＝3か月30日 |
+| c811 | 会議のあとの1週間 | 8月30日〜9月5日＝7日（S2 p.2 30 August - 5 September 1986） |
+| cb10 | 事故から4か月のうちに | L2 p.40／488（within the first four months of the accident） |
-| R3・R4 | 外務省 報道発表（2022-03-31）・外交青書2022 | （保存なし＝①で原ページ） | — |
-| WEB | 事業者 chnpp.gov.ua（再開の日・2000-12-15・2019-07-10 の引き渡し）・EBRD（2016-11-14・11-29）・内閣府 防災白書 平成23年版・World Nuclear News 2022-04-01（IAEA Update 38 の写し＝原ページは開けなかった） | URL は確かめの係C の答え（scratchpad `wf_係C.md`） | — |
+| R3・R4 | 外務省 報道発表（2022-03-31）・外交青書2022 | （保存なし＝①で原ページ）＝https://www.mofa.go.jp/mofaj/press/release/press1_000813.html ・https://www.mofa.go.jp/mofaj/gaiko/bluebook/2022/html/chapter3_01_04.html （G0 が 2026-10-22 に確かめた） | — |
+| WEB | 事業者 chnpp.gov.ua（再開の日・2000-12-15・2019-07-10 の引き渡し＝https://chnpp.gov.ua/en/about/history-of-the-chnpp/chnpp-shutdown ・https://chnpp.gov.ua/en/infocenter/news/5360-events-devoted-to-handing-over-and-accepting-the-new-safe-confinement-from-jv-novarka-to-chornobyl-npp-last-in-ukraine-for-two-days ）・EBRD（2016-11-14・11-29＝11-29 の頁 https://www.ebrd.com/news/2016/unique-engineering-feat-concluded-as-chernobyl-arch-has-reached-resting-place.html ）・内閣府 防災白書 平成23年版（https://www.bousai.go.jp/kaigirep/hakusho/h23/bousai2011/html/honbun/1b_2h_1s_1.htm ）・World Nuclear News 2022-04-01（IAEA Update 38 の写し＝原ページは開けなかった・https://world-nuclear-news.org/articles/ukraine-says-russian-forces-have-left-chernobyl ）・国連ニュース 2025-02-14（https://news.un.org/feed/view/en/story/2025/02/1160141 ）・NucNet 2025-12-08＝IAEA の評価の写し（https://www.nucnet.org/news/iaea-says-chernobyl-shelter-lost-primary-safety-functions-following-drone-strike-12-1-2025 ） | （保存なし）＝URL は G0 が 2026-10-22 に原ページで確かめた（v2_build/decisions.md §3 の19） | — |
```
