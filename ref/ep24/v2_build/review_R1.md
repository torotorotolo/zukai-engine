# 24本目 ④' 当て直し R1（前半＝つかみ〜第6章・c105〜c717）

- 係＝R1（当て直しの係）。見たのは **第1版→第2版で直したカットだけ**（diff_v1_v2.md の1〜509行＝61カット）。直していない行の照合はやり直していない
- 所見＝ `review_R1.json` の **9件**（🟡2・🟢7・🔴0）。案をみな採ると語りの字は **差し引き +11字**（上限 +15）
- 試し組み＝ `fcheck24.py --allfix review_R1.json --tag R1` → 当てた 184・当て損ない 0・**E（当て損ない・形・門番）0 件**（終了コード 0）。写しの字数 句読点なし 13,412＋ed01 46＝**13,458字**（--allfix の写しは G0 の c504・cc13 の足しを含まない。第2版 13,459字に当てれば 13,470字＝上限 13,505 の内）。冒頭 c105 の終わり 44.7秒（触っていない）
- 名前の網＝ `namecheck24.py` で2ファイルとも0件

## 所見（要点）

| id | カット | 重さ | 一言 |
|---|---|---|---|
| R1-001 | c420 | 🟡 | 入口の水が沸く寸前の主な原因は低い出力（付属書I「primarily」）。「出力も低いため」で重みが逆＝語順を替える（±0字） |
| R1-002 | c504 | 🟡 | 同じ表I-I を c305「1991年の委員会の報告の表」・c504「1992年の報告の表」と呼び分けている＝c504 を c305 に合わせる（+1字・G0 の足しの上） |
| R1-003 | c606 | 🟢 | 書き直しでも「試験の山場で」（during the critical part of the test）が落ちたまま（ca19 は残した）＝+6字 |
| R1-004 | c212 | 🟢 | 「炉を止める制御棒は、全部で211本」＝下から入る短い24本（緊急のときは入れない）まで止める棒に数える＝+3字 |
| R1-005 | c414 | 🟢 | 「この点を」を外して何を強く書いたかが抜けた＝「禁止と強く書いたのは」+2字 |
| R1-006 | c302 | 🟢 | 1カットに「ここで」「ここでは」＝「この動画では」（c202 と同じ）+2字 |
| R1-007 | c316 | 🟢 | 「出力を下げる」が c315〜c317 で3カット続く＝「その作業は」−4字 |
| R1-008 | c412 | 🟢 | 画の欄の札「3,200MW 定格」が残る（c211 は「最大の出力」にそろえた）＝札だけ直す |
| R1-009 | c716 | 🟢 | 反応「〜んだ。」はまとめの形で次に「そう。」が無い・「念のため」を日本全体に広げる＝「国の注意は、念のためだったのか。」+1字 |

## 担当の直したカットの全部（61カット）

| カット | 当てた原文 | 判定 | 一言 |
|---|---|---|---|
| c105 | S1-付属書I p.53／43 `during the physical startup of Ignalina Unit 1 and that of Chernobyl Unit 4`・`almost two-and-a-half years` | OK | 2つの炉を「など」で残し「ほど」も残る。呼び名は c218 と同じ |
| c107 | 台本 c104・c205 | OK | 数を言わない＝c205「主に3つ」と食い違わない |
| c202 | R3・R4（親が §3-19 で原ページを確かめ済み・係はウェブを開いていない） | OK | 地名も古い呼び方で通す断りになった |
| c205 | S1 p.34／24（出典の欄） | OK | 「主に3つ」＝§3-1 |
| c206 | S2 p.27／~24・S3 p.26／22 | OK | 問いに数字なし。7つは S3 の表まで入れると「事故の年に違反とされた」に収まる |
| c209 | S1-付属書II p.113／103 `graphite moderator` | OK | 割れる反応＝核分裂。物理として誤りなし |
| c211 | S2 p.9／~4 `below approximately 20% of full power` | OK | 「最大の」＝§3-2（c412 の札は R1-008） |
| c212 | S1 p.14／4 `except for 24 shortened rods`・S2 p.132／~125 `except for the shortened rods` | ずれ | R1-004 |
| c213 | S3 p.19／15 `tests were to be carried out on turbogenerator No. 8` | OK | |
| c215 | S1-付属書II p.121／111 | OK | 削っても c214 とつながる |
| c217 | S3 p.19／15 | OK | S3 の初出「1986年8月の」 |
| c218 | S1-付属書I p.61／51 `approved by the General Designer, the Chief Design Engineer`・p.62／52 `from the aforementioned organizations` | OK | 「設計者や規制側の」で限定が戻った |
| c219 | S3 p.19／15 `drafted in a purely formal way` | OK | 帰属＝ソ連の報告 |
| c220 | S1 p.34／24 `deliberately made on the spot` | OK | 「わざと」 |
| c221 | 台本 c217〜c220 | OK | 数を言わない |
| c223 | S3 p.19／15・S1-付属書I p.61／51 | OK | 反応・数字なし・計画を責める言い方を外した |
| c301 | S2 p.28／~25 `At 01:00 on 25 April`・S3 p.20／16 | OK | INSAG-1 も1時＝「1986年の報告」で合う |
| c302 | 台本 c302 1行目 | ずれ（言い回し） | R1-006 |
| c303 | S1-付属書I p.89／79 `not less than 26-30 rods` | OK | 「少なくとも」で同じ意味 |
| c304 | 表I-I の組み直し 01:06・03:47 の行 | OK | 片は表の行に当たる |
| c305 | 表I-I の組み直し 07:10 の行 | OK | 呼び名の基準（R1-002 で c504 を合わせる） |
| c306 | S1 p.21／11 `The recent reports confirm`・`in fact claim that this minimum ORM was also violated` | OK | 1992年の報告が新しい報告の言い分として引く形 |
| c309 | S2 p.35 `ECCS remained isolated (e) Safety principle violation` | OK | 違反の札は「切りっぱなし」に付く |
| c311 | S1 p.20／10 `This could be viewed as no violation only if`・`which it clearly was not` | OK | 「計画の外で、違反でないとは言えない」は原文の強さのまま |
| c312 | S1-付属書I p.82／72 `a violation of Section 2.10.5 of the Operating Procedures` | OK | 「運転の規則」 |
| c316 | S2 p.28／~25 `not resumed until approximately 9 h later` | OK（言い回しは R1-007） | 起点は c313 の「午後2時」で耳に通る |
| c401 | 表I-I 00:05 の行・S3 p.20／16・S2 p.28／~25 | OK | 炉が出す熱＝c209 とそろう |
| c402 | S1 p.21／11 `Transfer from local to global power control` | OK | 「保つ」＝c404 と語がそろう |
| c407 | S1 p.21／11 `refers to an unknown cause and inability to control the power` | OK | 向きの逆が消えた |
| c412 | S2 p.25／~22 `continuous operation below 700 MW(th) is forbidden` | OK（札は R1-008） | 「運転を続けた」 |
| c414 | S1 p.20／10 `was based on oral statements made by Soviet experts`・p.21／11 `was not warranted` | OK（言い回しは R1-005） | 帰属は合う |
| c415 | S1 p.38／28 `INSAG has been informed`・`sets a lower limit of 700 MW(th)` | OK | 伝え聞きの「という」 |
| c416 | S1-付属書I p.87／77 `no safe operating limits in terms of minimum permissible thermal reactor power` | OK | 片の差し替え |
| c417 | S1 p.15／5 `there was no in-core instrumentation available`・`all located at the mid-plane of the core` | OK | all＝「どれも」 |
| c420 | S1 p.18／8 `In addition, owing to the lower reactor power level`・S1-付属書I p.74／64 `primar-ily as a result of the low reactor power level` | ずれ | R1-001 |
| c421 | S1-付属書I p.87／77 `the flow rates of certain MCPs actually exceeded the limit`・p.88／78 `if anything hindered the reactor runaway` | OK | 違反と「むしろ妨げた」を同じ委員会の言葉で並べた＝寄らない |
| c501 | — | OK | 言い回しだけ |
| c504 | S1 p.22／12・表I-I 00:36:24 の行・S1-付属書I p.85／75 | ずれ（呼び名） | R1-002。2行目（水位の保護の下の段）は付属書I の `another protection system … existed and was brought into operation` にもある＝表の下に置いても合う |
| c505 | S1-付属書I p.85／75 `These personnel actions were in violation of Section 9`・p.88／78 `were not the causes of the accident` | OK | 「切り替えていない」＝did not switch |
| c507 | S2 p.39 `two TGs-trip signal` | OK | 出典の欄だけ |
| c511 | S1 p.21／11 `the SCSSINP Commission … does not support the apportionment of any blame` | OK | 2行目を消しても帰属は委員会のまま |
| c512 | S1 p.21／11 `"This trip would have saved the reactor" seems not to be valid` | OK | 主語＝1992年の報告 |
| c513 | S1 p.28／18 `might well have caused … rather than shortly afterwards` | OK | 「少し早く」・かもしれない |
| c514 | 同上 | OK | 反応は c513 より強くない・数字なし |
| c516 | S1 p.29／19 `on the spot they modified the test conditions` | OK | 変えた主体＝運転員 |
| c603 | S3 p.23／19・p.26／22 | OK | §2 のとおり「およそ半分」 |
| c605 | 台本 c606 | OK | 次の語り「違反だったことは変わらない」が答える |
| c606 | S1 p.21／11 `during the critical part of the test`・`Probably he was aware` | 要確認 | R1-003（時の限定）。「からだ」の因果は消えた |
| c609 | S1 p.21／11 `were not aware that it had safety significance` | OK | まとめ→「そう。」 |
| c612 | S1-付属書I p.75／65 `there was no increase in reactor power` | OK | 「止めるボタン」 |
| c613 | S3 p.21／17・S1-付属書I p.75／65 | OK | 「食い違う」 |
| c617 | S3 p.21／17 `cut off the current to the sleeves of the servo drives` | OK | 帰属＝ソ連の報告 |
| c621 | S3 p.29／25・S2 p.68／~63 | OK | 「爆発のあと」 |
| c701 | S3 p.21／17 `some of which fell onto the roof` | OK | 「一部は」 |
| c702 | S2 p.68／~63 `the fire was quenched at 05:00` | OK | 出典の欄だけ |
| c703 | S3 p.42〜43／38〜39 `a number of plant and emergency service personnel`・`also suffered burns` | OK | 「何人もが」 |
| c709 | L2 p.24／472 `from 30 April through 3 May`・p.25／473 `from 3 May through 7 May`・p.24／472 `circle centred on the reactor` | OK | 2段の避難を1つの期間にまとめ、起点＝炉 |
| c713 | K1 1986-05-15 参院 内閣委・原子力安全調査室長（「十四日時点で、二十九都道府県にわたり…検出」） | OK | 「見つかっていた」 |
| c715 | K1 1986-05-07 参院 科学技術特別委・科学技術庁長官（「放射能は検出されておらず」） | OK | 「見つかっていなかった」 |
| c716 | L3 p.43／83・K1 1986-05-07（同上の答弁） | ずれ（言い回し） | R1-009。出典の欄の片は合う |
| c717 | S2 p.1 `held in Vienna` | OK | 「4か月」は c802 に残る＝重ならない |

## どちらかに寄せていないか（前半の直しの積み重ね）

- 運転員の側を強めた直し（c220 わざと・c311 違反でないとは言えない・c412 運転を続けた・c421 流れすぎは違反・c516 運転員が変えた・c606 おそらく気づいていた）は、どれも原文の強さに戻したもの
- 設計・規則の側の直し（c218 承認を求めていなかった・c417 計器・c505 原因ではなかった・c512〜c514）も原文どおりで、反応（c223・c514）は非難を外した
- ＝前半の直しで新しく生まれた寄りは見つからなかった

## 読んだもの

- `ref/ep24/v2_build/decisions.md`（全文）
- `ref/ep24/v2_build/diff_v1_v2.md` の1〜509行（c105〜c717）
- `ref/ep24/daihon_v2.md` の §4 台本 c101〜c717 と c801〜c806（つながりの確かめ）・ca19 の語り
- `python ref/ep24/v2_build/ledger24.py show --cover c1,c2,c3,c4,c5,c6,c7`（92件）と `ledger24.md` の c1〜c7 の扱い
- `ref/ep24/v2_build/roles.tsv`（聞き役の役割）・`ref/ep24/src/insag7_tableI-I_rows.txt`（表I-I の組み直し）
- `pg24.py` で引いた原文：S1（本文 p.14・15・18・20・21・22・28・29・34・38・55／付属書I p.53・61・62・64・74・75・82・85・87・88）・S2（p.9・25・28・35・39・68・132）・S3（p.19・21・42〜43）・L2（p.14・24・25）・L3（p.43）・K1（1986-05-07 発言204・1986-05-15 発言218）
- 門番の作り：`fcheck24.py`・`build24_v2.py` の apply（old は塊の中の部分の字でも当たる）
