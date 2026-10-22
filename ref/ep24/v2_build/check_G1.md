# 24本目 ④' 照合の係 G1 の記録（つかみ・第1章・第2章）

- 担当＝daihon_v1.md 173〜393行＝c101〜c107・c201〜c224・c301〜c317＝**48カット**（橋を見るため c401 の頭も読んだ）
- 所見＝`findings_G1.json`＝**25件**（🔴1・🟡18・🟢6）＝案あり22・親へ（案なし）3
- 門番＝`python ref/ep24/v2_build/fcheck24.py ref/ep24/v2_build/findings_G1.json --tag G1`＝**E 0件**（exit=0）。当てた写しの m24：句読点なし 13,317＋ed01 46＝**13,363字**（第1版 13,358 → **+5字**）・W 32件（第1版と同じ）・聞き役 質問39／まとめ19／反応8（変えず）
- 冒頭（÷365）：c104 ひっくり返し **34.4秒**（変えず）・c105 棒の欠陥 44.9→**44.7秒**・最初の聞き役 **44.7秒**・最初の見出し 61.0→**60.3秒**

## 読んだもの
- daihon_v1.md 1〜130行（頭の注・§0・§0-1・§0-2・§1-1〜§1-5）・165〜404行（担当＋前後の橋）・1243〜1268行（§5）・1345〜1385行（§9・§10）
- sources.md 1〜163行（§1・§2・§3＝§2-5／§3-2 前半は ④で訂正ずみ）・legend_2026-10-22.md 80〜87行・162〜165行・kousei.md 146〜164行
- 原文（`pg24.py page`）：S1 p.13〜14・20〜22・33〜34・53・61〜62・89／S2 p.18・27〜28・35／S3 p.16・19〜21／表I-I の組み直し（`insag7_tableI-I_rows.txt` の p.63〜64）
- 人の名前：国会の発言者・付属書の委員長は役職で書いた（この記録とJSONに5人のほかの名前は無い）

## 語で引いたもの（`pg24.py find`／`re`）
- S2：`so-called 'human element'`・`fire-fighting personnel admitted`・`3200 MW(th)`・`below approximately 20%`・`standby diesel generators`・`reactivity margin`・`(30|15) rods|minimum permissible`（正規表現）・`not resumed until approximately 9 h later`・`At 01:00 on 25 April`・`ECCS remained isolated`・`Safety principle violation`・`Done in accordance with the test plan`
- S1：`211 movable`・`1660 fuel channels`・`forced cir-culation could be maintained`・`altered on an ad hoc basis`・`violation of Section 2.10.5`・`did not affect the initiation and scale`・`several hours|for several`（正規表現）・`Reactor thermal power is 1600 MW`・`ORM equals 13.2 manual control rods`・`except for 24 shortened rods which are inserted upwards`・`from 07:00 until 13:30 on 25 April`・`This could be viewed as no violation only if`・`should be approved by the General Designer`・`Start of reactor power reduction`
- S3：`prior to shut-down of the unit`
- K1：`五月三日に至り`・`五月三日以降採取した浮遊じん`
- ⚠️ 0件の語は無い（引いた語はすべて当たった）。所見の新しい出典の片（バッククォート）はどれも上の find で文字の層に当たることを確かめた

## 判定の印
- **OK**＝原文と意味・強さ・帰属が合う／**OK（注）**＝合うが一言残す（所見にしない理由を書いた）／**ずれ**＝所見あり（id）／**要確認**＝係は開けない（ウェブ・画像）＝親へ

## カットの表

| カット | 当てた資料と頁 | 判定 | 一言 |
|---|---|---|---|
| c101 | K1 1986-05-07 参院 科学技術特別委 発言204（科学技術庁長官）・1986-05-08 衆院 農林水産委 発言41（原子力安全調査室長） | OK（注）＋ずれ | 5月3日・東京・千葉・神奈川＝長官の答弁。「ちりや雨水」は室長の「5月3日以降採取した浮遊じん、雨水等」（全国）を合わせた形＝sources §2-11 の決めどおり。出典の欄に発言者の実名2つ＝G1-024 |
| c102 | S3 p.21／17・U1（画） | OK（注） | at about 1:24 two explosions ✓・1週間前 ✓。「出どころは」は長官の「起因すると思われる」を断定にしているが、今は確定の事実＝所見にしない |
| c103 | S2 p.18／~13・p.112／~105 | OK | 「炉の性質と重なって」まで言っている（in combination with specific reactor features）✓・根本原因＝so-called 'human element' ✓ |
| c104 | S1 p.34／24（6） | OK | were in fact not violations ✓・6年後 ✓・画の欄 p34＝(6) の頁 ✓ |
| c105 | S1-付属書I p.53／43 | ずれ | G1-002（イグナリナ1号機を落とした）・帰属は付いている・almost two-and-a-half years ✓ |
| c106 | S1 p.34／24 | OK | most ill judged ✓・打ち消しは同じカットで閉じる ✓ |
| c107 | S1 p.33／23 | ずれ | G1-013（「2つの報告」⇔ c205「3つ」・c206 と同じ言い回し） |
| c201 | S3 p.21／17・p.6／2 | OK | 1時24分ごろ＝爆発の時刻 ✓（p.6 の 1.23 a.m. は事故の始まり）・モスクワ時間 ✓ |
| c202 | R3・R4（ウェブ） | 要確認（ウェブ）＋ずれ | G1-017（キエフを使い続ける断りが無い）・外務省の原ページは親へ |
| c203 | S3 p.16／12 | OK | 176人＝1・2期の敷地の当直と各部門・保守の作業員 ✓／268人＝3期の建設現場の夜勤の建設・組立の作業員 ✓（号機の名は言わない＝§0-1 の10） |
| c204 | S2 p.118／~111 | OK | 300人・31人 ✓・ソ連の発表と帰属 ✓（so far＝これまでに、は落としたが次の行の「資料によって違う」で足りる） |
| c205 | S1 p.34／24 | ずれ | G1-014（3つの報告 ⇔ 第1・2章の4つ目＝S3）・出典の片 does not retract を語りは言わない |
| c206 | S2 p.27／~24 | ずれ | G1-011（7つは動画の選び方・0時28分は INSAG-1 では「誤り」） |
| c207 | S1-付属書II p.113／103 | OK | graphite moderator・boiling light water ✓・画は号機を名乗らない ✓ |
| c208 | S1-付属書II p.113／103 | OK（一般の説明） | 1660 fuel channels ✓。「沸いて蒸気になる」は実際は一部（steam-water mixture）＝c502 で分かる・中学生向けとして可 |
| c209 | S2 p.8／~3 | ずれ | G1-016（「反応」の初出のかみ砕き）・3,200MW(th)／1,000MW(e) ✓・物理として誤りなし |
| c210 | S1 p.13／3 | OK（一般の説明） | 水は中性子を吸う・泡で吸う水が減り反応が強まる＝RBMK として正しい。原文は「事故のとき void・power とも正」（新しい燃料では負）＝「この性質」の言い方で可 |
| c211 | S2 p.9／~4 | OK（🟢） | below approximately 20% of full power ✓・1986年の報告＝INSAG-1 ✓・「定格」のかみ砕き無し＝G1-023 |
| c212 | S1-付属書II p.113／103・S1 p.14／4 | ずれ | G1-009（211本に下から入る短い棒も入る）・18 s＝止める棒が上端から全部入る時間 ✓ |
| c213 | S2 p.27／~24・S3 p.19／15 | OK（🟢） | 点検の前・8号タービン ✓・G1-022（試験の繰り返し） |
| c214 | S3 p.19／15・S2 p.9／~4 | OK | 回る勢い＝mechanical energy of the rotor ✓・until the standby diesel generators ✓ |
| c215 | S1-付属書II p.121／111 | OK（🟢） | 止めたあとの熱＝一般の説明として正しい・G1-021（c214 の繰り返しを削る） |
| c216 | S1-付属書I p.61／51 | OK | 1982年 3号機・1984年と1985年 改良した装置・4号機は1983年12月に試験なしで運転開始 ✓（S3 p.19 Similar tests had already been carried out も同じ） |
| c217 | S3 p.19／15 | OK | not properly prepared・requisite approval ✓・帰属＝1986年のソ連の報告 ✓・画 p19 S3／p62 S1 ✓（p62 に nothing wrong with the programme itself） |
| c218 | S1-付属書I p.61〜62／51〜52 | ずれ | G1-008（どこの承認かを落とした＝上位語・寄せ） |
| c219 | S1-付属書I p.62／52・S3 p.19／15 | ずれ | G1-001 🔴（S3 の文を「1986年の報告」＝INSAG-1 の名で言った） |
| c220 | S1 p.34／24 | ずれ | G1-003（deliberately を落とした） |
| c221 | S1 p.29／19 | ずれ（🟢） | G1-015（3つの顔ぶれが c205 と違う）・ad hoc ✓・まとめ→「そう。」✓ |
| c222 | S3 p.19／15 | OK | called for shutting off the ECCS ✓・about four hours, safety substantially reduced ✓ |
| c223 | S3 p.19／15 | ずれ | G1-012（反応が計画を責める）・語りの not aware of the possible dangers・departed from the programme ✓・「準備不足の班」は言っていない ✓ |
| c224 | S2 p.35 | OK | 橋 ✓ |
| c301 | S3 p.20／16・S2 p.28／~25・表I-I p.63／53 | ずれ | G1-010（1時6分も1時もソ連＝区別がつかない・1時は1986年の2つの報告がそろう） |
| c302 | S1-付属書I p.89／79 | OK | 運転反応度余裕（ORM）✓ |
| c303 | S1-付属書I p.89／79 | OK（注） | not less than 26-30 rods・15 rods shut down immediately ✓（「30本」とだけ言わない ✓）。原文は At nominal power during steady state operation＝「ふだんは」は少し広いが c304・c305 と矛盾しない＝所見にしない（41字で言い換えの余地なし）。26本未満は技師長の許可、は落とした |
| c304 | 表I-I p.63／53（出典の欄は S2 p.35） | ずれ（🟢） | G1-019（出典の欄の片が語りの根拠でない）・01:06 31本 ✓・03:47 1600MW ✓（04:13〜12:36 は1500MW） |
| c305 | 表I-I p.63／53 | ずれ（🟢） | G1-020（出典の片を13.2本の行へ）・07:10 13.2 ✓・付属書I 1-4.7.1「7時ごろ15本」は言わない ✓ |
| c306 | S1 p.21／11・S1-付属書I p.88／78 | ずれ | G1-006（INSAG-7 は claim を引いている）・付属書I＝25日7時〜13時30分に15本以下 |
| c307 | 表I-I p.63／53・S2 p.35・S3 p.20／16 | OK | 13時5分 7号タービン ✓ |
| c308 | 表I-I p.63／53・S1 p.20／10 | OK（注） | 14:00 ✓・「2つ目の違反」は INSAG-7 (1) の言い方（INSAG-1 自身の表では切り離しは計画どおり）＝G1-005 の parent |
| c309 | S2 p.35・p.28／~25 | ずれ | G1-005（違反とされたのは切ったままにしたこと） |
| c310 | S1 p.20／10 | OK | permissible if authorized by the Chief Engineer・approved step ✓・条件「認めれば」を残した ✓ |
| c311 | S1 p.20／10 | ずれ | G1-004（違反でないとは言えない、が落ちた）・安全文化の欠けの主語＝期間中の切断と長い運転を許したこと＝「そこに」で合う（§0-1 の9） |
| c312 | S1-付属書I p.82／72・p.88／78 | ずれ | G1-018（Operating Procedures＝運転の規則）・割れを並べた ✓・効いていないは3つとも同じ ✓ |
| c313 | S1-付属書I p.88／78 | OK | まとめ→「そう。」✓ |
| c314 | 表I-I p.63／53 | OK | Kiev power grid controller ✓ |
| c315 | 表I-I p.63／53 | OK | 15:20 16.8・23:10 26 ✓（INSAG-1 の23時は言わない＝§1-5 ✓） |
| c316 | S2 p.28／~25・S3 p.20／16 | ずれ | G1-007（9時間は出力を下げる作業が止まった長さ）・反応は c314〜c315 の事実から＝先取りなし ✓ |
| c317 | — | OK | 橋 ✓（c401「日付が変わって」へ） |

## 親へ（係は開けない・決め）
- **ウェブ**：R3・R4（外務省 2022-03-31・外交青書2022）＝c202
- **決め**：c101 の出典の欄の発言者の実名（cb02 にも）＝G1-024／c308 の「2つ目の違反」の言い方＝G1-005／c205 の「3つの報告」と S3＝G1-014／c211「定格」＝G1-023／c311「およそ」→「約」＝G1-004
- **映像方針へ**：第2・3章の今の写真（G1-025・12カット）／c212 の図の札「211本」（G1-009）
- 画像を開く必要のある所見は無い（図1 の寸法などは担当の外）
