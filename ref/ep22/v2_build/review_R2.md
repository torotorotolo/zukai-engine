# 22本目 ④' 当て直し R2（第9章〜終章＋カットの外）

- 担当：第9章〜終章（ca01〜cd09）の直したカット 50 と、カットの外（§1-1 題B・§1-5・§6・§8・§9）の直し 10 行＝diff_v1_v2.md の「## ca01」以降
- 読んだもの：`v2_build/diff_v1_v2.md`（l.889〜1353）・`daihon_v2.md`（l.905〜1342＝c922 から §11 まで）・`v2_build/ledger22.md`（ca〜cd・§ の行）・`v2_build/quotes22_v2.tsv`（ca〜cc の判定＝すべて OK）
- 原文は `pg22.py` で引いた：NTSB p.14・16・22・31・35・36・51・52・53・59・60・64・65・73・74・81・85／USCG p.7・8・78・136・137・213・230・233・235・238・256・283・289・290・294・295・307・311・325／TSB §1.1・1.3.1・1.10.10.1・1.12.2・1.15・1.20.2.2・1.21.1・1.22・1.23.1・1.30.2・2.1・2.1.3・3.1・3.2・脚注75・付録B
- 所見は `review_R2.json`（23件＝🔴1・🟡4・🟢18。🟢のうち6件は字数の埋め合わせ）

## カットごとの判定

| カット | 判定（OK／ずれ／要確認） | 一言 |
|---|---|---|
| ca01 | OK | 問い「次の年の夏には」＝直前の年は c921 の2021年2〜3月→2022年の夏で合う。欄の TSB 脚注75（人が乗った回だけ数える）は付録B 表B1 の注とも合う。聞き役に数字なし |
| ca03 | OK（🟢 R2-009） | 「傷んだかは分からない」＝TSB §2.1.3 の if any ✓。「そう。」は ca02 の反応を受ける ✓。ただ第1版の「近くで」（closer view）が落ち、船の中へ入ったようにも聞こえる |
| ca04 | OK | 帰属は ca03 の「米沿岸警備隊によると」が受ける。USCG p.311 no incident report ✓ |
| ca06 | OK | NTSB p.31 音8・ひずみ8＋8＝16 ✓。問いに答えがその場で返る ✓ |
| ca07 | OK | USCG p.283 3:26:45 ✓。主語「分析」で、会社の記録を米沿岸警備隊が調べた形になった ✓ |
| ca08 | OK | NTSB p.52 between about 1515 and 1530 ✓。呼び名をそろえても文は崩れない（R2-022＝字数の埋め合わせの候補） |
| ca09 | OK | 「そう伝えられた」の「そう」＝枠の中でずれた音＝NTSB p.36 hull had shifted in its metal cradle ✓ |
| ca10 | OK | 足した欄の USCG p.289〈281〉 cursory external examination ✓（頁を確かめた） |
| ca11 | OK | NTSB p.36 ✓。「当時の」は USCG p.289 Director of Engineering at the time と合う |
| ca13 | OK | 「その場には」＝onboard ✓。with the authority は前の語りの行が言う＝まとめとして許せる |
| ca14 | OK | NTSB 表5（81＝7/19・82＝7/22 とも 3,840）・p.51（83＝7/23・別の場所・2,954）✓。「そう。」は ca13 のまとめを受ける ✓ |
| ca15 | OK | USCG p.235 control program reversed ✓・p.311 ✓。「そのまま」を落としても「続けた」で潜航を続けた意味は残る |
| ca16 | OK | NTSB p.64 difficult to compare ✓。1行目は NTSB p.51 の事実（帰属なしでも米運輸安全委の行の前置き） |
| ca17 | 要確認（🟢 R2-007） | NTSB p.53 Through dive 80 ✓。ただ「80回目」は語りでここだけに出る番号で、何の通し番号か分からない＝「あの音の潜航までは」で -4字 |
| ca18 | OK | 足した欄の NTSB p.59 脚注42 ✓ |
| ca19 | ずれ（🟡 R2-002） | 第1版の「よく合う形だという」（more consistent with）が消え、はがれの仕組み（原文は would have・筒の端との交わりの条件つき）を言い切りの一般論にした |
| ca20 | 要確認（🟢 R2-006） | 2021年8月の潜航は2回（8/4・8/5）＝「8月の潜航」では1回の値と分からない（G5-014 のねらいが届ききらない） |
| ca21 | OK | 足した欄の USCG p.289 It is likely … sudden delamination ✓ |
| ca22 | 要確認（🟡 R2-005） | 語りは TSB の主語（会社が調べなかった）どおり ✓。聞き役「まだ決まっていない」は、途中で決まるように聞こえ、ca21 の米2機関とも向きが合わない |
| ca25 | ずれ（🔴 R2-001） | 「大きな音の山も警告の形にならず」＝NTSB p.65 は「80回目のあとの潜航」のセンサーの話。山そのものの話にすり替え、「最初の傷み」の「最初の」も落とした |
| ca26 | OK（🟢 R2-008） | 主語を「音の記録」にしたのは G5-019 のとおり。原文の赤信号はひずみの曲がりと合わせて |
| cb02 | OK | 「アメリカへ運び戻していた」＝NTSB p.35（Everett）・USCG p.230（transported back to the United States）の重なり ✓ |
| cb04 | OK | TSB §1.22 Dec 2022–Feb 2023 ✓。ただ §9 の行が「摂氏」のまま（R2-019） |
| cb05 | OK | NTSB p.60 could have・TSB §2.1.3 introduced the potential ✓。「あり得る」のかぎかっこは原文の語ではない（字幕で引用に見えないかは⑤で） |
| cb07 | OK（🟢 R2-016＝欄） | 「当時の技術部長」＝USCG p.238 last Director of Engineering ✓。外した「給料の後払い」の片が欄に残る |
| cb08 | OK | TSB §1.23.1 no one formally ✓ |
| cb09 | OK（🟢 R2-017＝欄） | 外した免除の申し込みの片が欄に残る |
| cb10 | OK | towed by or tethered to ✓。§9 の行が外した語りのまま（R2-018）。R2-013＝字数の埋め合わせの候補 |
| cb11 | 要確認（🟢 R2-012） | significant wave heights＝有義波高。「波は、最大3.35メートル」は最大の波が3.35mに聞こえる（第1版から・G0-018 で「の高さ」も落ちた） |
| cb12 | OK（画は要確認） | partially submerged again ✓。聞き役「沈みかけたんだね」→ cb13「そう。」✓。画の欄の注記（図10 は5月24日でない・cb11 へ移す案）が未決のまま cb12 に残る＝映像方針で |
| cb13 | OK | USCG p.294〜295 would likely have … further weakened ✓・TSB §2.1.3 not likely a contributing factor／may have exacerbated ✓。途中の行の終わりも読点 ✓ |
| cb14 | OK | 足した欄の USCG p.256 ✓ |
| cb15 | OK | USCG p.295 Dive 87・improper ballasting・45-minutes・no evidence ✓。「3回目」＝cb14 の3回の3回目＝87回目 ✓ |
| cb17 | OK | USCG p.78 three or more strikes → cancel the day's dive operation ✓（TSB の「48を超えるとストライク」と同じ仕組み） |
| cb18 | OK | 82回目＝7/22（NTSB 表5）✓。日付にして83回目と取り違えなくなった |
| cb19 | OK | 「人が乗って初めて台を離れ」＝NTSB p.81 の表（84回目は無人の練習）・NTSB p.16 ✓ |
| cc03 | OK | USCG p.7 firings of senior staff members and the looming threat of being fired ✓ |
| cc04 | OK | 聞き役の行の呼び名も不自然でない（読みは R2-021） |
| cc05 | OK | NTSB p.74 Contributing … insufficient to ensure ／ flawed analysis ✓。40字 |
| cc08 | 要確認（🟡 R2-004） | 「委員会のページ」がどの委員会か耳で分からない（直前は米運輸安全委員会）。返事の有無は3冊の外（ウェブ）の事実 |
| cc09 | OK | 足した TSB §2.1・§3.1 の片 ✓ |
| cc10 | OK（🟢 R2-010） | 欄の3片 ✓。問い「分かれる所は？」に「ある。」は半歩ずれる |
| cc11 | OK | 欄の4片 ✓（TSB §3.2＝may or may not have been causal）。聞き役 → cc12「そう。」✓ |
| cc13 | OK | USCG p.307 Encouraging employees to voice concerns without fear of retaliation ✓ |
| cd01 | OK | 聞き役に数字なし ✓ |
| cd02 | OK | 「層の一部」「傷が重なって」＝3冊の重なり ✓ |
| cd03 | ずれ（🟡 R2-003・🟢 R2-015） | 「記録を読み解ける人もいないまま」は ca13 で直した限定（その場の・判断する立場の）を落とした。欄は消えた「読み違え」の NTSB p.74 のままで、足した2つの事実（USCG p.290）の片が無い |
| cd04 | OK | TSB §1.23.1 some … left the company or were dismissed（例＝運航部長の解任・財務と人事の部長の退社）✓。TSB §3.1 の5つはどれも会社と船体 ✓ |
| cd06 | OK | §1.30.2 の drift＝operations drift outside of safe limits ✓（R2-011＝字数の埋め合わせの候補） |
| cd07 | OK | 「と書いている」✓ |
| §1-1 題B の注意書き | OK | TSB §1.15 required 1.25・1.11・Assuming … representative ✓、§1.12.2 ISO ✓ |
| §1-5 母船の長さ | ずれ（🟢 R2-020） | 67.2m は欄の NTSB p.14 に無い（p.85 表E-2）。§9 は 67.1m＝台本の中で値が割れる |
| §1-5 D3 現場までの距離 | OK | 370海里＝685km（米2機関）・TSB §1.3.1 about 425 nautical miles＝787km ✓ |
| §6 約5.4秒 | OK | c413 の語りと合う |
| §8 船級 | OK | NTSB p.22 nongovernmental・reviewing plans … before and during construction・witnessing critical testing ✓ |
| §9 見出しの重なり | OK | 1つになった |
| §9 c205・c301 | OK | 語り「全長70メートル近い」（c301）と合う |
| §9 c219 | OK | 語り「約700〜800キロ」と合う |
| §9 cb10 | ずれ（🟢 R2-018） | 「台本の言い方」が④'で外した語り（5,000キロを超えた）のまま |
| §9 c918 | OK | 語り（100・125・111キロ）と合う |

## 親へ

1. **🔴 R2-001（ca25）だけは直さないと原文と違う。** 警告の形にならなかったのは「80回目のあとの潜航」の音（NTSB p.65）で、15時26分45秒の山そのものではない。第1版の「あの音のあとも…最初の傷みに」は正しかった＝G5-017 で詰めたときに崩れた。直す案は41字・+2字。「警告は出ず」と言い切らない理由（USCG p.235 の83回目の音の数）は JSON の parent に書いた
2. 🟡 4件はどれも「直す・詰める」で新しく生じたずれ：ca19＝「よく合う」（more consistent with）が消えた／cd03＝ca13 で直した限定（その場の）が終章で落ちた／cc08＝「委員会」がどれか分からない／ca22＝聞き役「まだ決まっていない」（G7-001 の後半が残った）
3. 欄（出典）の食い違い：cd03 は G6-019 と G7-075 がぶつかり、欄と語りが入れ違った（R2-015）。cb07・cb09 は語りを外した片が欄に残る（R2-016・017）。§9 の cb10・cb04 の行が外した語りの言い方のまま（R2-018・019）
4. 字数（句読点なし・全部採ると合計 +1＝上限まで残り 27）：
   - 第9章 ＋4（R2-001 +2・R2-002 +6・R2-006 +2・R2-008 +4 任意・R2-009 +1 任意／R2-005 −1・R2-007 −4・R2-022 −3・R2-023 −3）＝任意の2件を見送ると −1
   - 第10章 −2（R2-012 +6／R2-013 −4・R2-014 −4）
   - 第11章 −2（R2-004 ±0・R2-010 −2）
   - 終章 +1（R2-003 +4／R2-011 −3）
5. 映像方針へ：cb12 の画（NTSB 図10＝5月20日と27日の写真）は、画の欄の注記どおりなら5月24日の語りに重ねない＝cb11 へ移すかを決める（R2 は台本の字に触れないので JSON に入れていない）
6. 確かめきれなかった所：cc08 の「返事がページにまだ無い」は3冊の外（ウェブ）の事実で、R2 はウェブを開いていない＝G0 の 2026-10-14 の確認のまま
