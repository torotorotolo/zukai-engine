# 21本目 9.11 米国同時多発テロ（2001-09-11＝7本目のリメイク）台本 第2版

> **2026-10-12・21本目のチャット4＝④' 台本【チェックと修正】**で組んだ。第1版 [daihon_v1.md](daihon_v1.md)（md5 `571cb11c71d4264fc9add8911c61eac3`＝1文字も書き換えていない）に差し替え表 `v2_build/patches21.json` を `v2_build/build21_v2.py` で当てた。🔧＝画の欄か語りが第1版から変わったカット（出典の欄だけの直しは印なし）。
> 第2版を直すときは **`v2_build/decide21.py`（係の所見の扱い）か `v2_build/gen_g0.py`（G0 の直し）に書き足して `python ref/ep21/v2_build/make21.py`** で組み直す（第2版を手で直すと、次に組んだとき消える）。対照表＝`v2_build/diff_v1_v2.md`・所見の台帳＝`v2_build/ledger21.md`・門番の出力＝`v2_build/gates.md`・原文を引く道具＝`v2_build/pg21.py`。
> 設計図＝[kousei.md](kousei.md)・事実の出どころ＝[sources.md](sources.md)・素材＝[materials.md](materials.md) §7・通説＝[legend_2026-10-11.md](legend_2026-10-11.md)・旧版の当て直し＝[claims_check_2026-10-11.md](claims_check_2026-10-11.md)。
> 語りは「だ・である」（まりさ）。聞き役（れいむ）の行の印は `> Q: `（音にも字幕にも出さない）。役割（質問・まとめ・反応）は `v2_build/roles_map.json` → `roles.tsv`。決め所（★）の行は無い（10-07）。
> 画の欄の頭の語＝`実写`（この事件の写真・映像＝写真の割合に数える）／`図 p数字`（資料の頁）／`図 模式`・`図 NTSB`・`図 RG237`（作る図・資料の図をなぞる図・レーダー再生の画面＝数えない）／`イメージ`（フリー素材・後年の写真＝画面に「イメージ」と出す・数えない）／文字だけの頁は「（文字の頁）」。頁は委員会報告の印字の頁（PDF＝印字＋18）。
> 🔴 このリポは公開＝私人（乗客・ご遺族・建物にいた人・電話を受けた人）・乗っ取った側・乗員の名前を書かない（乗員は役職で）。語りで名前を出すのは、公的な任務の人で語りが追う人＝FAA の全米の運用の責任者・大統領・副大統領だけ（§1-4）。

## 0. 第2版の机上検査（2026-10-12・チャット4＝④'）

| 門番・数え | 第1版 | **第2版** | 判定 |
|---|---|---|---|
| 字数（`v1_build/m21.py`・句読点なし・ed01 こみ） | 13,244 | **13,436**（幅 13,140〜13,505・上限まで69字） | ✅ 内 |
| 尺の3通り | ① 36分29秒 ② 36分17秒 ③ 36分17秒・開き12秒 | ① 36分29秒 ② **36分48秒** ③ 36分48秒・開き18秒 | ✅（目標36〜37分の内） |
| 冒頭（÷365 を1カットずつ） | 引き c105＝32.9秒・最初の聞き役 32.9秒・最初の見出し 60.2秒 | **同じ**（c101〜c109 は触っていない） | ✅ 46秒より前 |
| 行の形 | 237カット・529行・最長41字 | 237カット・**530行**・1カット1〜3行・最長41字 | ✅ E 0 |
| 聞き役（`check_listener.judge`・`v2_build/roles.tsv`） | 64行・質問38／まとめ18／反応8 | **64行＝行の12.1%・1分1.74回・最初32.9秒・最長の空き82.2秒・数字0・質問38（59.4%）・まとめ19（29.7%）・反応7（10.9%）** | ✅ E 0・W 0 |
| 写真・実写 | 64（27.0%） | 64（27.0%） | ✅ 20%以上 |
| 文字だけ（`count_text_screens.py --gate`＋🆕 `romanpage`） | 2（c315・ca18）と数えていた＝**実は3**（ca01＝`図 p.xv` を道具が図解に数えた） | **1**（ca18）・romanpage 0 | ✅ |
| 出典の引用の照合（`v2_build/quotes21v2.py`） | 319片＝OK 302・原寸 15・OCR 2・無し 0 | **364片＝OK 344・原寸 18・OCR 2・無し 0** | ✅（OCR 2＝ca12・cb16 の NIST） |
| 書かない名前（`src/core_raw/namecheck.py`＝git の外・陽性対照で当たる） | 0 | **0**（台本と `v2_build/` の md・json・tsv の全部） | ✅ |
| `tools/check_script.py` | E 1（尺）・W | E 1・W 5 | ⚠️ E は尺の式だけ（ゆっくりに合わない定数＝§5a-28b の既知）／W＝尺の開き（同じ理由）・章 c3／c4／c8／ca の写真映像が20%未満 |
| `tools/check_script_diff.py`（🔧 と差分） | — | 🔧 117＝実際に変わった117・欠番0・新設0 | ✅ |
| 決め所（★） | 0 | 0 | ✅（10-07） |

- 章ごと（句読点なし・目安との差）：c1 366（+1）・c2 1,100（+96）・c3 1,110（+15）・c4 1,517（+57）・c5 1,245（+59）・c6 1,439（+70）・c7 883（−30）・c8 1,726（−99）・c9 1,294（+108）・ca 1,251（+65）・cb 894（−201）・cc 565（−74）
- 回したコマンド（次の工程も引き写さず回し直す）：`python ref/ep21/v2_build/make21.py`（扱いの表→G0 の直し→差し替え表→試し組み→「報せ」の行ごとの直し→本組み→役割表→m21→quotes21v2→名前の網→check_script→check_script_diff→count_text_screens→romanpage→対照表→台帳＝`gates.md`）

### 0-1. ④' でやったこと（ルール 4'-19 の型）
1. **下ごしらえ**＝④の数え（237カット・13,244字・36分17秒・聞き役64・写真27%・引用319片・名前0）を自分で回して同じ値／原文を引く道具 `pg21.py`（係もこちらも同じ物差し）／組む道具は20本目の `build20_v2.py` ほかを写した
2. **G0 の通し読み**（このチャット・§4 を頭から全部）＝第6章の並びと写真の取り違え・intercept の訳・「報せ」の読み・聞き役の「つまり」の型・文字の頁の数え漏れ ほか
3. **原文照合 6係**（Workflow・同時2本・検証役なし・画像なし）＝G1 つかみ〜第2章／G2 第3〜4章／G3 第5〜6章／G4 第7章／G5 第8〜9章／G6 第10章・終章・§1・§5〜§9。記録＝`v2_build/check_G1〜G6.md`・所見＝`findings_G1〜G6.json`（**141件＝🔴12・🟡80・🟢49**）
4. **G0 が原文に引き直した**＝🔴12件すべてと言い回しの大きい🟡（p3・p18・p19・p21・p25・p27・p31・p40〜p45・p451・注39・注67〜68・法律 §104・国立公園局・AP）。⚠️ 途中で `pg21.py` の穴（行末のハイフンで割れた語を、問いにハイフンが無いと探さない）を見つけて直し、係の「無い」の判断を引き直した（§0-6）
5. **ウェブで一次を取った**＝運輸省の監察総監の報告 CC-2006-085（2006-08-31・30頁・`src/new/web5/`）。国防総省の側（06-INTEL-12）は取れない（403・ダウンロードになる）
6. **別の目2本**（4'-18＝第1版→第2版の対照を前半・後半で原文に当て直し）＝**42件（🔴2・🟡24・🟢16）**＝直しが生んだずれ（「証拠は無い」への強め・題 C の「軍」の言い広げ・並べ替えで「この命令」が長官の命令を指す・足した反応を次の語りが受けない・消した行の空の「> 」・§2／§3 の表が古い ほか）→ 扱いを決めて組み直した（`review_R1.md`・`review_R2.md`）
7. **承認①**（§0-4）
8. 台帳（197件）＝`v2_build/ledger21.md`：採る・一部（G0 の文で）・済み（G0 の組み替えに入れた）・採らない・今のまま・映像方針へ。⚠️ 直さなかった所見と理由は台帳の「採らない」「今のまま」「映像方針へ」の行

### 0-2. 重い所見（🔴＝どれも G0 が原文で確かめた）
| カット | 第1版 | 第2版 | 原文 |
|---|---|---|---|
| c313 | 迎え撃つことは、手順に無かった | そばまで寄せて確かめることは、手順に無かった（c918・c919 の「迎え撃つ」もやめた） | p18 `The protocols did not contemplate an intercept`＝近づいて確かめること。撃ち落とす道は別（p17） |
| c203 | 聞き役「遠くへ行く便を選んでいたの？」に答えていない | そう。選んだのは、燃料を多く積む長い便だ。旅客機を、大きなミサイルに変えるためだった | 注1 p451 `heavily fueled`・p245・p4 |
| c514 | 聞き役の行が2つ続く（南棟の衝突の直後に反応） | 反応の行を外した | ルール 4'-15 |
| c605 | 理由は管制のソフトだけ | ソフトと、77便の辺りのレーダーの弱さ | p25 `as well as from poor primary radar coverage` |
| c701 | もう飛んでいる機には、まだ何も言っていない（誤り） | 止めたのは地上の機で、もう飛んでいる機は、そのままだ | p10・注67〜68（9:07 ボストン・センターの警告・9:19 デルタ1989便） |
| c712 | 運輸長官の語りに大統領の電話の写真 | 第6章を並べ替え（G0-001）＝写真は専用機の語りへ・長官の証言は図（c709） | §0-1 #6 |
| c832 | 「その言葉を最初に伝えたのは…AP 通信だ」 | 事件の6日後の新聞に、AP 通信の記事として載っている | AP の写し・sources §11-3（これより早い報道は見つけていない＝全数ではない） |
| c834 | 委員会は、別の章で | 委員会は、こうも書いている | p45 は p14 と同じ第1章 |
| c903 | 軍は93便を、一度もレーダーで捉えていない | NEADS は93便を、一度もレーダーで捉えていない | p31 `The NEADS air defenders never located the flight` |
| c913 | 聞き役「なんで、届かなかったの？」に答えていない | 「副大統領は、届いていないことを、知っていたの？」（答え＝NORAD の指揮で飛ぶ操縦士に伝わっていると思っていた） | p44 |
| ca09〜ca10 | 監察総監＝二次（報道）・主語が FAA なのに NORAD の証言の話・「正さなかった幹部」が落ちた | 一次で書き直した＝委員会は「わざとか」を調べず国防総省と運輸省の監察総監に引き継いだ／FAA の職員がわざと事実と違うことを言った証拠は見つからない／委員会への答えの別の誤りを正さなかった幹部2人の処分を考えるよう求めた | CC-2006-085 PDF p1〜p3 |
| ca10（当て直し R2-001） | （④'の第1稿）証拠は無い | 証拠は見つからない | p2 `did not find evidence to conclude` |
| §1-1 題 | 「…前もっての知らせが無く、2,977人が亡くなった」＝因果に読める | 「。」で切る（承認①で旧版の文） | p31・p45 `We are not so sure` |
| §1-1 題 C（当て直し R2-005） | 軍が乗っ取りを知ったのも墜落の後 | 軍の当直が…（案の記録） | p42 国防総省の指揮所は 10:03ごろ |

### 0-3. 第1版 §0-1「④' で見てほしい所」13項目の決着
1. **題の因果** → 「。」で切る形にした（G6-001）。承認①で「旧版の文・決まりだけ今」に決まった（§0-4）＝旧版も「。」で切っていた
2. **写真27%** → 64（27.0%）のまま（20%以上）。増やすのは映像方針で＝当日の WTC・ペンタゴンを語りの時刻に合う所だけ（§0-5）。c515 は 8:51〜9:02 の語りなので事件の前の写真に替えた（両棟が燃える写真を置かない）
3. **c211「2人」** → 合っている（p3＝2人が1つ目と2つ目の探知機を両方鳴らし、2人とも手持ちの探知機で調べられて通過。3人目は1つ目だけ鳴らし2つ目で通った）。委員会が頼んだ専門家の見方（鳴った物を確かめていない）を足した
4. **生々しさ**（c404・c505・c807） → 線の内。どれも委員会の地の文と電話の言葉で、傷や体を描かない・記録音声は鳴らさない。c807 は声の主（機長か副操縦士）を足した
5. **c609** → 「ビルにぶつかった2機目は、77便かもしれない、と考えた。実際は175便だ」と、本社の読み違いだと言った
6. **c712・c713** → 第6章を並べ替えた（G0-001）＝命令（スライニー）→前例の無い命令・時刻は書かれていない→長官の証言（図）→「誰の命令？」→報告書と証言を分けて言う。大統領の電話の写真は専用機の語りへ
7. **CVR の秒** → 時刻は逐語（P200056T）の 10:00:25・10:00:42 のまま、「17秒後」を言わない（委員会は16秒後＝10:00:42 は両方で一致）
8. **Let's roll** → 「最初に」を外した／誰が言ったか（電話をかけていた乗客）と誰が聞いたか（電話会社の係員）を役割で残した／画の札「書き起こしには無い」は逐語を p7 しか原寸で見ていない＝「電話の向こうで聞かれた言葉」に／c833 の重なる2行目を外した
9. **ca10 監察総監** → 一次（CC-2006-085）を取って書き直した（§0-2）。⚠️ 国防総省の側は一次が取れない＝結論を言わない
10. **ca12** → 「どれかが間違い、というより」を外し、「委員会の時刻は NTSB の飛行経路の調べ（注39）による／NIST はテレビの時刻表示」と、出どころだけを並べた。NTSB の初出の説明を ca12 へ移した
11. **cb03・cb04・cb15 の大統領の訪問** → 9/12 のペンタゴンは委員会報告の注61（p559）にもある。9/14 のニューヨークは委員会報告に無い＝NARA の目録の説明だけ。言ってよいが、映像方針で中身を見て絵と合わなければ替える
12. **cc08 検視局** → 写しと語りは合う。「25年がたった2026年8月」→「事件から25年目の2026年8月」（8/24 は24年11か月）。「いまも続く」は言わない。⑥で頁をもう一度開く
13. **聞き役** → c424（決めつけ→まとめ）・c514（2行続き→外した）・c612（事実→驚き）・cc04（「しかなかった」→「組み立てようとした」）。問いに次の語りが答えない所を直した（c202／c203・c401・c801・c804・c901・c913・cb19）。反応を c312 に1つ足した（質問60%・まとめ30%の境目）。「つまり、…んだね？」14回→7回

### 0-4. ✅ カズヤくんの承認①（2026-10-12・このチャット）
| 項目 | いま（④の推奨） | 決めたあと |
|---|---|---|
| §1-1 題 | A「軍の当直に乗っ取りの知らせが前もって届いたのは、1機目の9分前だけ。残る3機は前もっての知らせが無く、2,977人が亡くなった…」（93字） | **「軍が1機目の乗っ取りを知らされたのは衝突9分前。残る3機は墜ちるまで知らされなかった。2,977人が亡くなった9.11アメリカ同時多発テロの真相【事故検証】【ゆっくり解説】」（86字）**＝「旧版と同じ」→ 文は旧版・決まりだけ今（数 2,973→2,977・末尾【ゆっくり解説】・【映像あり】は付けない） |
| §1-2 サムネの赤 | A「犠牲2,977人 猶予は9分」 | **「2,977人犠牲 猶予は9分」（14字）**＝「旧版と同じ」→ 旧版の並び（数が先）・「死亡」は「犠牲」に・数は 2,977 |
| §1-3 コメントの問い | A「この動画を見て、いちばん意外だったことは何でしたか。…」 | **C「飛行機に乗る前の保安検査で、印象に残っていることはありますか。よければ、コメントで教えてください。」**（cc10 に入れた） |

- 聞き方：1回目に「旧版と同じ」（題・サムネ）と C（問い）。旧版の文を一字一句そのままだと決まり3つ（【ゆっくり解説】・【映像あり】の位置と付ける条件・サムネに「死亡」を使わない）と数（2,973）がぶつかる＝2回目にどこまで合わせるかを聞いた

### 0-5. 映像方針へ渡すもの
1. 冒頭（c101〜c109）の実写の秒＝DVIDS 122342・122343・122347・議会図書館 LC-A05-A17・NASA ISS003-E-5388・WHTV 1501・606（遺体・担架・負傷者の写らない窓・私人の近景は顔だけモザイク）
2. **写真27%**：章 c3（1/20）・c4（4/26）・c8（4/35）・ca（3/20）は W。c403〜c417 の15カットに実写0（G2-026）＝事件の前の実写（管制の卓の別の点など）を挟めるか
3. **「当日の WTC（A）」の両棟が燃える点**を原寸で数える＝c514・c519・c609・c701・c706・ca11・cc03 の7か所（G3-024）。c515 は事件の前の写真（北棟だけが燃える点が見つかればそれ・副題は絵を見て）
4. 1点ずつ：c518 小学校のテレビの写真の時刻と部屋（G2-025）／c904〜c906 PEOC の日時（NARA の目録・副題に日付を書かない）／c908 fighter_dc の撮影地（「首都の上空」は書かない）／c712 大統領の電話の写真・c914 電話の写っていない機内の点／c623（衝突のすぐ後の煙）と c624（夕方の西側）を入れ替えた／cb03・cb04・cb15 の WHTV 600・609・610 の中身（9/14 の訪問は委員会報告に無い）／cb17 中庭の無人機の展示（2025年7月）／cc01・cc02 の写真の人と語りの取り違え（副題で写っている人を書く）
5. NIST の OCR 2片（ca12・cb16）＝頁を画面に出すなら原寸
6. 国防総省の監察総監の報告（06-INTEL-12・2006-09-12）＝一次が取れれば ca10 に軍の側の1文を足せる
7. サムネ＝赤「2,977人犠牲 猶予は9分」・黄「9.11同時多発テロの真相」・地 `wtc_smoke_day`（C'＝出典の表記だけ直す）。A＋B1。⑥で横210px
8. 読み（§6 に足した語＝北棟・南棟・空の・開いた・港湾公社・何機か・約4,500機）は⑤a で音声記号列に

### 0-6. ④' で見つけた門番と道具の穴（直したもの・直していないもの）
- 🔴 **文字だけの数え漏れ**：`count_text_screens.py` は画の欄を `図\s*p\d` で拾う＝`図 p.xv`（ローマ数字・点つき）を「図解」と数える。第1版は ca01 が漏れて「2」と書いた（実は3）。道具は直さない（Vault の共有の道具）＝`final21.py` に `romanpage` の見張りを足した
- 🔴 **`pg21.py`（この回の道具）の find の穴**：行末のハイフンで割れた語を、問いにハイフンが無いと探さなかった（`cov- erage` が0件＝c605 の2つ目の理由が見えなかった）。直して、係の「無い」を引き直した（c605＝有る・cc04 の and failed＝無い・9/14 の訪問＝無い）
- ⚠️ `quotes21v2.py` は web と一次の写し（国立公園局・AP・法律・記念館・運輸省の監察総監）を頁で割らずに全体から探す＝頁は人が見た（ca10 の片の頁を当て直しで p2→p3 に直した）
- ⚠️ G0 自身の誤り：運輸省の監察総監の報告で「報道の『幹部3人』は一次の『2人』と食い違う＝孫引きのずれ」と一度書いた＝誤り（誤りを知った幹部は3人＝いまいる2人と退職1人・処分を考えるよう求めたのはいまいる2人）。当て直し（R2-004）のあと原文を読み直して直した

## 1. ④で決めたこと

### 1-1. 題（§B4・型＝つかみ。もう一つの事実、N人が亡くなった〈事故名〉の真相【事故検証】【ゆっくり解説】）
- ✅ **承認①（2026-10-12 カズヤくん）＝「旧版と同じ」→ 文は旧版・決まりだけ今**＝**「軍が1機目の乗っ取りを知らされたのは衝突9分前。残る3機は墜ちるまで知らされなかった。2,977人が亡くなった9.11アメリカ同時多発テロの真相【事故検証】【ゆっくり解説】」（86字）**。旧版（7本目）から変えたのは、数（2,973→いまの 2,977）・末尾の【ゆっくり解説】（§B4-8）・【映像あり】を付けない（④の決め）の3つだけ。「。」で切る形＝因果に読ませない（G6-001）。原文：「軍が…9分前」＝p20（軍への最初の知らせ 8:37:52）・p21（9分）／「残る3機は墜ちるまで」＝p31（2〜4機目は前もっての知らせが無い）・93便は国防総省の指揮所が10時3分ごろ＝墜落とほぼ同時に知った（p42）
- 下の A〜C は④・④'の案（記録として残す）
- 型は記憶 `feedback-jiko-title-form` と20本目の題で確かめた。「9.11」を使う（§B4-4）・【映像あり】は付けない（実効1280以上の実写0本＝materials §2）・「死亡」を使わない・数は「いまの犠牲者数 2,977」（記念館）

| 案 | 題 | 字数 | 根拠 |
|---|---|---:|---|
| **A（④の推奨）** | 軍の当直に乗っ取りの知らせが前もって届いたのは、1機目の衝突の9分前だけ。残る3機には無かった。2,977人が亡くなった9.11 米国同時多発テロの真相【事故検証】【ゆっくり解説】 | 90 | p21・p31＝c104・c105・ca19。旧版の「0分」を「残る3機には無かった」に直し、「。」で切った（因果に読ませない＝G6-001） |
| B | 管制官は2機目に「乗っ取りかもしれない」と気づいていた。それでも軍に届いたのはぶつかったころだ。2,977人が亡くなった9.11 米国同時多発テロの真相【事故検証】【ゆっくり解説】 | 90 | p22・p23＝c506・c514（旧版の「誰も見ていない」の訂正） |
| C | 撃墜の許可が出たとき、93便はもう墜ちていた。軍の当直が乗っ取りを知ったのも墜落の後だ。2,977人が亡くなった9.11 米国同時多発テロの真相【事故検証】【ゆっくり解説】 | 86 | p30・p31・p41＝c901〜c905 |

### 1-2. サムネの赤（§B5＝「犠牲N人＋核心」・空白こみ10〜14字・旧版の「2,973人死亡 猶予は9分」の「死亡」を言い換え）
- ✅ **承認①（2026-10-12 カズヤくん）＝「旧版と同じ」→「2,977人犠牲 猶予は9分」（14字）**＝旧版の並び（数が先）のまま、「死亡」を「犠牲」に（§B5-5）・数をいまの 2,977 に。黄と地は旧版のまま（下）。A＋B1（B2 なし）
| 案 | 赤の言葉 | 字数 | 根拠 |
|---|---|---:|---|
| **A（④の推奨）** | 犠牲2,977人 猶予は9分 | 14 | 旧版の型のまま「死亡」と数を直した＝p21 |
| B | 犠牲2,977人 知らせ9分前 | 15（上限14を超える＝使えない） | p21 |
| C | 犠牲2,977人 届かぬ命令 | 14 | p43・p44 |
- 黄＝「9.11同時多発テロの真相」（13字）。地＝`wtc_smoke_day`（LC-A05-A01・両棟が燃える＝出典「米議会図書館蔵（撮影者不詳）」＝C'）を旧版の型のまま。A＋B1（B2 なし）。⑥で横210pxで確かめる。実在の顔と数を並べない（§B5-4）

### 1-3. コメントの問い（§B3-7b＝誰でも気軽に答えられる・責める相手を作らない・です・ます・3行以内）
| 案 | 問い |
|---|---|
| A（④の推奨） | この動画を見て、いちばん意外だったことは何でしたか。よければ、コメントで教えてください。 |
| B | 9.11のことを、あなたは、どこで知りましたか。よければ、コメントで教えてください。 |
| **C（✅ 承認① 2026-10-12＝cc10 に入れた）** | 飛行機に乗る前の保安検査で、印象に残っていることはありますか。よければ、コメントで教えてください。 |

### 1-4. そのほか
- **人**（kousei §8）＝語りで名前を出すのは FAA の全米の運用の責任者ベン・スライニー（p29）・ブッシュ大統領・チェイニー副大統領だけ。乗員は役職（機長・客室乗務員）・管制は機関の名（ボストン・センター・ニューヨーク・センター・インディアナポリス・センター・クリーブランド・センター・コマンドセンター）・軍は部署（NORAD・NEADS）と役職（指揮官・将校・補佐官）・運輸長官と首席補佐官は役職だけ・乗客／電話の相手／建物にいた人／電話会社の係員は人数と役割だけ。**乗っ取った側の名前は出さない**（c209 で断る）
- **記録音声**＝鳴らさない（10-11 カズヤくん）。管制の無線・電話・CVR の逐語は**語りと字幕だけ**・画面に大きく出さない（画の欄に「字幕だけ」と書いた）。CVR は P200056T の p7 の2行（②で原寸）だけ＝CVR の中の乗っ取った側の言葉と名前の入る行は使わない。管制の無線に流れた乗っ取った側の声（c409・c411＝委員会 p19・c808＝p12 の字・c502 は字を引かず「怪しい無線」と言うだけ（p7）・名前なし）は語りと字幕で使う（kousei §3-2 c8 の🔴＝名前の入る行を避ける）
- **噂**（kousei §9）＝撃墜は c903・c917（崩れる）／副大統領の命令は c904〜c917（墜落の後・届かなかった）／乗客が操縦室に入ったは c831（書かれていない）／Let's roll は c832・c833（帰属つき）／ミサイルは c624（名指しせず＝C-130H の操縦士と FDR）／演習が遅らせたは c417（むしろ早まった）／わざと隠したは ca09・ca10（誤り・わざとは帰属つき）／記録装置は全部燃えたは ca13〜ca15／携帯はつながらないは c815。第7ビル・崩壊の仕組み・インサイダー取引は扱わない（cb15 で「NIST が別に調べた」の1行だけ・爆破説の名指しなし）
- **2026年の動き**＝cc08 の1行だけ（検視局 2026-08-24＝「身元の分からなかった犠牲者の1人を新しい調べ方で確かめた」まで・頁に無い「いまも続く」とは言わない）。軍事委員会の公判日は扱わない
- **単位**＝メートルを先・原単位はかっこ（§B1-2・換算は §9）。時刻は語りで「8時46分40秒」、画面の札は「8:46:40」（§B1-3）。時刻は米東部の夏時間と c201 で1回断った
- **死の語**＝「亡くなった」。「殺され」（c505＝電話の言葉）・「死ぬ」（c823＝CVR の言葉）は引いた言葉の中だけ
- **冒頭は実写だけ**（c101〜c109＝DVIDS 122342・122343・122347・議会図書館・NASA・WHCA）。衝突の瞬間・火の玉・落ちる人・遺体・担架は使わない
- **決め所の画面なし**（10-07）＝旧版の★（「9分」「Roll it」「negative clearance」など）は語りに溶かした。原文照合は出典の欄（§2）

### 1-5. 割れる時刻と数（台本で1つに決めた所＝図の札もこの値）
| 項目 | 台本 | 別の言い方 | 出典 |
|---|---|---|---|
| 1機目の衝突 | 8時46分40秒（c421） | NIST 8:46:30／8:46:26（ca11・ca12 で3つを並べた） | p7・NCSTAR 1 表6-1・1-6 表6-1 |
| 2機目の衝突 | 9時3分11秒（c513） | NTSB 約9:02:40・NIST 9:02:59（台本では言わない） | p8 |
| 77便の衝突 | 9時37分46秒（c620） | NTSB 9:37:45（言わない）・委員会は注154で「推定」 | p10 |
| 93便の墜落 | 10時3分11秒（c827） | 委員会も some dispute と書く（言わない） | p30 |
| 93便の乗っ取りの降下 | 約210メートル（700フィート）（c806） | NTSB 約600フィート（言わない） | p11 |
| CVR の2行 | 10時0分25秒・10時0分42秒（c823・c824＝差の秒は語りで言わない＝④'） | 委員会 10:00:26・16秒後（p14）＝10:00:42 は両方で一致 | P200056T p7（②で原寸） |
| 93便への警告 | 9時24分に届いた（c804） | 送信 9:23（本文）・注79 は 9:24 に送った | p11 |
| 全機着陸の命令 | スライニーの命令（c706）・時刻は書かれていない（c708＝本文・注165・図表 p32〜33・スタッフ声明・p326 のどこにも無い＝④'で確かめた） | 運輸長官の証言 9:45ごろ「最後の命令」（c709） | p29・証言の写し |
| 降りた機の数 | 約4,500機（c711） | （長官の証言の写しに 3,500 は見つからない＝使わない） | p29 |
| 犠牲者 | いま 2,977（c103・cc06） | 委員会 2,973（2004年7月・cc07） | 記念館・p311 |
| 燃料 | 最大で約4万3,000リットル（1万1,400ガロン）（c203） | スタッフ声明 No.17 は11便に 24,000ガロン（言わない） | p4・スタッフ声明 p4 |

## 2. 照合の表（出典の欄そのもの＋機械の照合）

- 21本目も決め所（★）が0＝`tools/check_facts.py` の照合（★の表）は働かない。20本目と同じく **§4 の全カットの出典の欄に原文の字をバッククォートで書き**、`v1_build/quotes21.py` で資料の字に全片を当てた（全行＝第1版 `v1_build/quotes21_result.tsv`・🆕第2版 `v2_build/quotes21_v2.tsv`＝`v2_build/quotes21v2.py`）
- 揃え＝NFKC・小文字・空白を消す・ダッシュと引用符の揺れを揃える・行末ハイフンを消した形でも探す・「…」で区切って4字以上の片ごと。判定＝書いた資料・書いた頁にあるか

| 判定 | 片 | 中身 |
|---|---:|---|
| OK（書いた頁にある） | 344（第1版 302） | 委員会報告（文字の層・PDF＝印字＋18）・スタッフ声明 No.17・運輸長官の証言（2003-05-23 の写し）・国立公園局・AP（Seattle Times の写し）・法律 107-71（govinfo）・検視局・記念館（④で開いた写し＝`src/new/web4/`）・🆕運輸省の監察総監の報告 CC-2006-085（④'で取った一次＝`src/new/web5/`。⚠️ この資料は頁で割らずに全体から探す＝頁は人が見た＝PDF p1〜p3） |
| 原寸 | 18（第1版 15） | NTSB の4本・CVR の逐語 P200056T・委員会報告の図表 p32〜33・NIST の表6-1＝文字の層0か OCR の資料＝②が原寸で読んだ写し（sources §11-1）に当たった |
| OCR | 2 | NIST NCSTAR 1（文字の層が OCR 並み）＝ca12・cb16。④'＝OCR の層で文の形が読める（G5 が NCSTAR 1 p83 で確かめた）。画面に頁を出すなら映像方針で原寸 |
| 無し | 0 | — |

- ⚠️ この照合は「その字が資料にあるか」まで。**言い換えの強さ（推定→断定など）は人が見る**＝④' の B 面
- 資料に素の形で無い数（換算・計算・年）＝§9 に式

## 3. 章ごと（始まりは句読点なし÷365 の積み上げ）

| 区切り | 章 | 始まり | カット | 句読点なし（目安） | 分 | 写真・実写 | 聞き役 |
|---|---|---|---:|---:|---:|---:|---:|
| c1 | つかみ | 0:00 | 9 | 366（365） | 1.00 | 9 | 2 |
| c2 | 第1章　その朝、4つの便 | 1:00 | 17 | 1,100（1,004） | 3.01 | 7 | 4 |
| c3 | 第2章　乗っ取りの「常識」 | 4:00 | 20 | 1,110（1,095） | 3.04 | 1 | 7 |
| c4 | 第3章　1機目　応答しない11便 | 7:03 | 26 | 1,517（1,460） | 4.16 | 4 | 6 |
| c5 | 第4章　2機目　気づいていた管制官 | 11:12 | 20 | 1,245（1,186） | 3.41 | 6 | 5 |
| c6 | 第5章　3機目　画面から消えた点 | 14:37 | 24 | 1,439（1,369） | 3.94 | 7 | 7 |
| c7 | 第6章　空を閉じる | 18:34 | 16 | 883（913） | 2.42 | 5 | 5 |
| c8 | 第7章　4機目　93便の35分 | 20:59 | 35 | 1,726（1,825） | 4.73 | 4 | 9 |
| c9 | 第8章　届かなかった命令 | 25:42 | 21 | 1,294（1,186） | 3.55 | 7 | 7 |
| ca | 第9章　「9分」は、どう分かったか | 29:15 | 20 | 1,251（1,186） | 3.43 | 2 | 6 |
| cb | 第10章　その後の空 | 32:41 | 19 | 894（1,095） | 2.45 | 6 | 5 |
| cc | 終章　あの朝、持ち場にいた人たち | 35:08 | 10 | 565（639） | 1.55 | 6 | 1 |
| ed01 | 共通エンディング | 36:41 | — | 46 | 0.13 | — | — |
| **計** | | **36:48** | **237** | **13,436** | **36.82** | **64** | **64** |

- 1機目の衝突（8:46:40）は c421＝約10分（尺の約28%）。競合の中央値 約32%
- 章名は本文と突き合わせた（§4-11）：「応答しない」＝c402・「気づいていた管制官」＝c506・c507・「画面から消えた点」＝c603・「空を閉じる」＝c706・「93便の35分」＝c829・「届かなかった命令」＝c910・c913・「9分」＝ca19・「持ち場にいた人たち」＝cc03
- 目安（kousei §3-1）との差（第2版）：c2・c4・c5・c6・c9・ca が多め（＋57〜＋108）・c7・c8・cb・cc が少なめ（−30〜−201）＝合計は幅の中。cb は「その後」を厚くしない（競合の型＝競合分析 §6-1）

## 4. 台本

### つかみ（9カット）

**c101** ／ 実写 DVIDS 122342「Noble Eagle, Sep 11 Part 1」（米空軍 第11通信隊・PD・SD＝全画面・煙と消防車の遠景・ゆっくり寄る・秒は映像方針で＝副題「2001年9月11日のペンタゴン」） ／ 委員会報告 p1（`Tuesday, September 11, 2001, dawned temperate and nearly cloudless`）・p4（`The 19 men were aboard four transcontinental flights`）
> 2001年9月11日、火曜日の朝。
> アメリカで、旅客機4機が、相次いで乗っ取られた。

**c102** ／ 実写 議会図書館 LC-A05-A17（ミッドタウンの向こうに立ちのぼる煙の雲・C'＝米議会図書館蔵（撮影者不詳）・全画面・右へ流す・時刻は言わない＝副題「当日のマンハッタン」） ／ 委員会報告 p7（`crashed into the North Tower`）・p8（`struck the South Tower`）・p10（`crashed into the Pentagon`）・p14（`plowed into an empty field in Shanksville`）
> 2機は、ニューヨークの世界貿易センターの2つの高層ビルに、
> 1機は、首都ワシントンの対岸にある国防総省、ペンタゴンにぶつかった。
> 4機目は、ペンシルベニア州の野原に墜ちた。

**c103** ／ 実写 NASA ISS003-E-5388（国際宇宙ステーションから見たニューヨーク一帯と南東へ流れる煙・A・全画面・ゆっくり寄る・時刻は言わない＝副題「宇宙から見たニューヨークの煙（当日）」） ／ 記念館（`The attacks killed 2,977 people`）
> いま数えられている犠牲者は、2,977人だ。

**c104** ／ 実写 DVIDS 122343「Noble Eagle, Sep 11 Part 2」（米空軍・PD・SD＝全画面・救助にあたる隊員・負傷者と遺体の写らない窓だけ＝副題「当日のペンタゴン」） ／ 委員会報告 p21（`NEADS received notice of the hijacking nine minutes before it struck the North Tower`）
> アメリカ北東部の空を見張る軍の当直が、1機目の乗っ取りを知らされたのは、
> 北のビルにぶつかる、9分前だった。

**c105** ／ 実写 DVIDS 122342（別の窓・放水する消防車＝副題「当日のペンタゴン」） ／ 委員会報告 p31（`no advance notice on the second, no advance notice on the third, and no advance notice on the fourth`）
> 残る3機は、前もっての知らせが、無かった。

**c106** ／ 実写 WHTV 1501 ホワイトハウスからの退避（WHCA・A・SD＝全画面・私人の近景は顔だけモザイク・音は使わない＝副題「当日のホワイトハウス」） ／ 委員会報告 p22（`we may have a hijack`）
> Q: それじゃあ、乗っ取りに気づいた人は、誰もいなかったの？
> いや。地上の管制官のなかには、気づいていた人がいた。

**c107** ／ 実写 WHTV 606 バークスデール空軍基地に着いた大統領専用機（WHCA・NARA 6171389・A・SD＝全画面・手前の記者は顔だけモザイク＝副題「当日の午後、ルイジアナ州の空軍基地」） ／ 委員会報告 p23（`The notice came at about the time the plane was hitting the South Tower`）
> それでも、2機目の知らせが軍の当直に届いたのは、
> ちょうどビルにぶつかったころだった。

**c108** ／ 実写 DVIDS 122347「Noble Eagle, Sep 14」空撮（米空軍 第1戦闘カメラ隊・PD・SD＝全画面・ゆっくり回り込む＝副題「9月14日のペンタゴン（空撮）」） ／ —
> その朝、管制官と軍の当直は、何を見て、何を知らなかったのか。
> 調査委員会が集めた記録の時刻で、たどっていく。

**c109** ／ 実写 DVIDS 122343（別の窓・建物の西側と隊員＝副題「当日のペンタゴン」） ／ 委員会報告 p20（`Radar data show the Otis fighters were airborne at 8:53`）・p20（`NEADS: Is this real-world or exercise?`）・スタッフ声明 p18（`taped conversations at NEADS, but in taped conversations at FAA centers`）
> Q: 時刻まで、記録に残っているの？
> 無線も電話も録音され、レーダーの記録もある。

---

### 第1章　その朝、4つの便（17カット）

**c201** ／ 実写 manhattan_pre（事件の2か月前のマンハッタン・2001年7月・C＋D＝米議会図書館蔵／知られた制限なし・全画面・右へ流す＝副題「事件の前のマンハッタン（2001年7月）」） ／ 委員会報告 p1（`nearly cloudless`）
> まず、その朝の4つの便を見ていく。
> 主に使う資料は、2004年にアメリカの調査委員会がまとめた報告書だ。
> 時刻はすべて、アメリカ東部の夏の時間で言う。

**c202** ／ 図 模式 4便の経路の地図（出発の3つの空港と行き先の2つの街＝NTSB の4本の経路の図をなぞる・東から西へ線が伸びる） ／ 委員会報告 p4（`four transcontinental flights`）
> その朝、アメリカ東部は、雲のほとんど無い晴れだった。
> 4機とも、東の海岸から西の海岸へ、大陸を横切る便だ。
> Q: わざわざ、遠くへ行く便を選んでいたの？

**c203** 🔧 ／ 実写 logan（ボストンのローガン空港・1973年・EPA DOCUMERICA・A・全画面・ゆっくり寄る＝副題「ボストンのローガン空港（1973年）」） ／ 委員会報告 p4（`turn them into large guided missiles, loaded with up to 11,400 gallons of jet fuel`）・第1章 注1 p451（`they simply booked heavily fueled east-to-west transcontinental flights`）・p245（`select planes departing on long flights because they would be full of fuel`）
> そう。報告書によると、選んだのは、燃料を多く積む長い便だ。
> 旅客機を、大きなミサイルに変えるためだった。
> 燃料は、最大で約4万3,000リットル（1万1,400ガロン）を積んでいた。

**c204** ／ 実写 AA11 N334AA（11便の機体の事件の前の写真・CC BY-SA 3.0・額装・無加工＝副題「11便の機体（事件の前）」） ／ 委員会報告 p4（`Eighty-one passengers boarded the flight with them (including the five terrorists)`・`The plane took off at 7:59`・`It carried its full capacity of nine flight attendants`）
> 1機目は、アメリカン航空11便。ボストンからロサンゼルスへ向かう。
> 7時59分に離陸した。機体はボーイング767。
> 乗員は操縦士2人と客室乗務員9人。乗客81人には、乗っ取った5人も入る。

**c205** ／ 実写 Torri Gemelle（事件の前の世界貿易センター・1999年・CC BY-SA・720×576・額装・無加工＝副題「事件の前の世界貿易センター（1999年）」） ／ 委員会報告 p7（`Fifty-six passengers boarded the flight`・`departed Logan Airport at 8:14`）
> 2機目は、ユナイテッド航空175便。同じボストンから、ロサンゼルスへ。
> 8時14分に離陸した。こちらも767で、乗客56人、乗員9人。

**c206** ／ 実写 dulles（ワシントン・ダレス空港・1985年・A・全画面・左へ流す＝副題「ワシントン・ダレス空港（1985年）」） ／ 委員会報告 p8（`the flight carried 58 passengers`・`took off at 8:20`・`There were four flight attendants`）
> 3機目は、アメリカン航空77便。ワシントン・ダレス空港から、ロサンゼルスへ。
> 8時20分に離陸した。機体はボーイング757。乗客58人、乗員6人。

**c207** ／ 実写 UA93 N591UA（93便の機体の事件の前の写真・CC BY 2.0・全画面・ゆっくり寄る＝副題「93便の機体（事件の前）」） ／ 委員会報告 p10（`At 8:42, United Airlines Flight 93 took off from Newark`・`Thirty-seven passengers, including the hijackers, boarded the plane`・`there were five flight attendants`）
> 4機目は、ユナイテッド航空93便。ニューアークから、サンフランシスコへ。
> 8時42分に離陸した。757で、乗客37人、乗員7人。

**c208** ／ 図 模式 時間の帯（4機の離陸＝7:59・8:14・8:20・8:42＝この回の芯の帯の始まり） ／ 委員会報告 p10（`Three of the flights had actually taken off within 10 to 15 minutes of their planned departure times`・`the flight was running more than 25 minutes late`）
> ほかの3機は、予定から10分から15分ほどで飛び立った。
> 93便だけは、朝の混雑で、離陸が25分あまり遅れていた。
> Q: 乗っ取った人たちは、全部で何人いたの？

**c209** ／ イメージ b767_takeoff（2012年のアメリカン航空の767・フリー素材＝副題「イメージ」） ／ 委員会報告 p4（`The 19 men were aboard four transcontinental flights`）
> 19人だ。11便、175便、77便に5人ずつ。93便には4人いた。
> この動画では、乗っ取った側の名前は出さない。

**c210** ／ イメージ security_pre（1970年の空港の保安検査・CC BY・私人の顔だけモザイク＝副題「イメージ（1970年の空港）」） ／ 委員会報告 p2（`operated by Globe Security under a contract with American Airlines`・`contracted with Huntleigh USA to perform the screening`）・p3（`had contracted out the work to Argenbright Security`）・p4（`operated under contract by Argenbright Security`）・p2（`calibrated to detect items with at least the metal content of a .22-caliber handgun`）
> 19人は全員、その朝の保安検査を通っていた。
> 検査を受け持っていたのは、航空会社が雇った警備の会社だ。
> 金属探知機は、小さな拳銃くらいの金属で鳴るように合わせてあった。

**c211** 🔧 ／ 図 模式 保安検査の流れ（探知機の門・手持ちの探知機・通過＝人は影だけ） ／ 委員会報告 p3（`set it off, a screener wanded him. He passed this inspection`・`set off the alarms for both the first and second metal detectors and was then hand-wanded before being passed`・`it was clear that he did not`）
> ワシントンの空港では、77便の犯人のうち2人が、探知機を2回鳴らしている。
> 2人とも、手持ちの探知機で調べられたが、鳴った物を確かめないまま通された。

**c212** ／ 図 模式 刃渡りの物差し（10センチの線と刃物の影・人は描かない） ／ 委員会報告 p84（`knives with blades under 4 inches long`・`explicitly permitted them`）
> Q: 刃物は、持ち込めなかったの？
> 当時は、刃渡り10センチ（4インチ）未満なら、持ち込めた。
> 航空会社の検査の手引きが、はっきり認めていた。

**c213** 🔧 ／ 図 模式 同じ物差し（3つの理由の札） ／ 委員会報告 p84（`the agency did not consider such items to be menacing`・`most local laws did not prohibit individuals from carrying such knives`・`such knives would have been difficult to detect unless the sensitivity of metal detectors had been greatly increased`）
> 国の空の役所、FAA の理由は3つ。まず、危ない物とは考えていない。
> 多くの地域の法律でも、持ち歩くのは禁じられていない。
> そして、探知機をよほど鋭くしないと、見つけにくい。

**c214** 🔧 ／ 図 模式 機内からの電話が伝えた道具（刃物・スプレー・「爆弾」の札に「おそらく偽物」） ／ 委員会報告 p7（`They used knives`）・p5（`I think there's Mace`）・p13（`we believe the bombs were probably fake`）
> 機内からの電話によると、犯人たちが使ったのは、刃物と、
> 目や喉を刺激するスプレー。3つの便で、犯人は爆弾があると言ったが、
> 委員会は、その爆弾は、おそらく偽物だったとみている。

**c215** ／ 図 模式 操縦室の扉（閉めて鍵＝当時の決まり） ／ 委員会報告 p85（`required air crews to keep the cockpit door closed and locked in flight`・`This requirement was not always observed or vigorously enforced`）
> 当時の決まりでは、操縦室の扉は、飛んでいるあいだ閉めて鍵をかける。
> ただ、その決まりは、いつも守られていたわけではなかった。

**c216** ／ 実写 logan_apron（ローガン空港の駐機場・1969年・D＝米議会図書館蔵／知られた制限なし・全画面・ゆっくり引く＝副題「ローガン空港（1969年）」） ／ 委員会報告 p4（`By 8:00 A.M. on the morning of Tuesday, September 11, 2001, they had defeated all the security layers`）
> 報告書は、こう書いている。朝の8時には、19人はもう、
> 当時の空の保安の仕組みを、すべて通り抜けていた。

**c217** ／ 図 模式 時間の帯（8:00 の線） ／ —
> Q: つまり、乗る前の関門では、誰も止められなかったんだね？
> そう。では、空に上がってからは、どうだったのか。
> その鍵は、当時の、乗っ取りの「常識」にある。

---

### 第2章　乗っ取りの「常識」（20カット）

**c301** ／ 実写 F-15 オーティス基地（102戦闘航空団 101戦闘飛行隊・尾翼「MA」・A・VIRIN で 2001-11-06・全画面・右へ流す＝副題「オーティス基地のF-15（2001年11月）」） ／ —
> Q: 乗っ取りの「常識」って、どういうこと？
> 乗っ取りが起きたら、乗員も、管制も、軍も、どう動くか。その前提だ。

**c302** 🔧 ／ 図 模式 乗員の手引きの年表（1960年代から2001年まで） ／ 委員会報告 p85（`The FAA-approved "Common Strategy" had been elaborated over decades of experience with scores of hijackings, beginning in the 1960s`）
> まず乗員。連邦航空局（FAA）が認めた、
> 乗員の手引きがあった。1960年代から、数多くの乗っ取りの経験を重ねて作られた。

**c303** ／ 図 模式 昔ながらの乗っ取り（要求・着陸・あとは警察と軍の3つの箱） ／ 委員会報告 p85（`accommodate their demands, get the plane to land safely, and then let law enforcement or the military handle the situation`・`the longer a hijacking persisted, the more likely it was to end peacefully`）
> 教えていたのは、犯人の要求をのみ、機を無事に着陸させ、
> あとは警察や軍に任せる、というやり方。長引くほど、無事に終わりやすいとされた。

**c304** 🔧 ／ 図 模式 同じ箱（「要求」に亡命・仲間の釈放の札） ／ 委員会報告 p85（`hijackers issue negotiable demands (most often for asylum or the release of prisoners)`・`suicide wasn't in the game plan`）
> 犯人は、亡命や仲間の釈放など、話し合える要求を出すもの、とされていた。
> FAA のある職員の言葉では、「自殺は、乗っ取り犯の筋書きに入っていない」。

**c305** 🔧 ／ 図 模式 同じ箱（「暴力が起きたら」の箱だけ空白） ／ 委員会報告 p85（`FAA training material provided no guidance for flight crews should violence occur`）
> Q: 犯人とは戦わない、っていう前提だったんだ。
> そう。FAA の教材には、暴力が起きたときの手引きが、何も無かった。

**c306** 🔧 ／ 図 模式 操縦室の扉（金庫の扉の絵記号） ／ 委員会報告 p85（`proposals were made in early 2001 to install reinforced cockpit doors`）
> 2001年の初め、操縦室の扉を頑丈にする案が出たとき、
> 操縦士の組合の保安委員長は、こう話している。

**c307** ／ 図 模式 同じ扉（鍵が外れる） ／ 委員会報告 p85（`Even if you make a vault out of the door, if they have a noose around my flight attendant's neck, I'm going to open the door`）
> 「扉を金庫のようにしても、客室乗務員の首に縄をかけられたら、
> 私は扉を開ける」

**c308** 🔧 ／ 図 模式 同じ扉と箱（「要求に従う」の矢印） ／ 委員会報告 p85（`even a hardened cockpit door would have made little difference in a hijacking`）
> Q: 従うのが決まりなら、扉を丈夫にしても、同じってこと？
> そう。委員会も、扉が丈夫でも、ほとんど違いは無かっただろう、と書いている。

**c309** ／ 図 模式 年表（1986年の印から2001年まで） ／ 委員会報告 p85（`no terrorist had hijacked a U.S. commercial aircraft anywhere in the world since 1986`）
> それに、テロリストによるアメリカの旅客機の乗っ取りは、
> 1986年を最後に、世界のどこでも起きていなかった。

**c310** 🔧 ／ 図 模式 機内の座席（保安官の席に印が無い） ／ 委員会報告 p85（`only 33 armed and trained federal air marshals as of 9/11`・`They were not deployed on U.S. domestic flights`）
> Q: 機内に、警備の人は乗っていなかったの？
> 武器を持ち、訓練を受けた連邦航空保安官は、全米で33人。
> しかも、国内線の警備にはついていなかった。

**c311** 🔧 ／ 図 模式 手順の段（管制官→上司→FAA 本部→国防総省の指揮所→国防長官の許し→NORAD→戦闘機） ／ 委員会報告 p17（`Controllers would notify their supervisors, who in turn would inform management all the way up to FAA headquarters in Washington`）
> 次に、管制と軍。北アメリカの空を守る軍の司令部を、NORAD という。
> 乗っ取りが分かると、管制官が上司に伝え、知らせは段を上がって FAA 本部へ。

**c312** 🔧 ／ 図 模式 同じ段（下の段へ光が進む） ／ 委員会報告 p18（`to contact the Pentagon's National Military Command Center`・`seek approval from the Office of the Secretary of Defense`・`transmitted down NORAD's chain of command`）
> 本部から国防総省の指揮所へ。国防長官の許しが出れば、
> 命令は NORAD の段を降りて、やっと戦闘機が動く。
> Q: ずいぶん、段が多いんだね。

**c313** 🔧 ／ 図 模式 乗っ取られた機と後ろの戦闘機（約8キロの間隔） ／ 委員会報告 p18（`five miles directly behind the hijacked aircraft`・`The protocols did not contemplate an intercept`）
> そう。戦闘機は、乗っ取られた機の約8キロ（5マイル）後ろに付き、
> 目立たないように見守る。そばまで寄せて確かめることは、手順に無かった。

**c314** 🔧 ／ 図 模式 同じ（段と後ろの戦闘機を1枚に） ／ —
> Q: 段を順に上がって、後ろからそっと見守る。それが決まりだったんだね。
> そう。委員会は、この手順には3つの前提があった、と書いている。

**c315** 🔧 ／ 図 模式 3つの前提の箱（1つ目に印＝すぐに見分けがつき、姿を消そうとはしない） ／ 委員会報告 p18（`the hijacked aircraft would be readily identifiable and would not attempt to disappear`）
> 1つ目。乗っ取られた機は、すぐに見分けがつき、姿を消そうとはしない。

**c316** ／ 図 模式 3つの前提の箱（2つ目と3つ目に印） ／ 委員会報告 p18（`there would be time to address the problem through the appropriate FAA and NORAD chains of command`・`the hijacking would take the traditional form`）
> 2つ目。FAA と軍の指揮の段を、順に上がるだけの時間がある。
> 3つ目。昔ながらの乗っ取りで、機を誘導ミサイルにするようなものではない。

**c317** ／ 図 模式 待機の基地の数（冷戦の最大26か所から7か所への棒） ／ 委員会報告 p16（`reduced from its Cold War high of 26`）・p17（`only seven alert sites left in the United States, each with two fighter aircraft on alert`）
> Q: 軍のほうの備えは、どうだったの？
> すぐ飛び立てる戦闘機の待機の基地は、冷戦のころの最大26か所から減り、
> 全米で7か所。それぞれに2機ずつだった。

**c318** 🔧 ／ 図 模式 北東部の地図（NEADS のあるローム・オーティス・ラングレー・ニューヨーク・ワシントン） ／ 委員会報告 p17（`Northeast Air Defense Sector (also known as NEADS), which is based in Rome, New York`・`NEADS could call on two alert sites, each with one pair of ready fighters`）
> 北東部の空を受け持つのは、ニューヨーク州ロームにある、
> NORAD の部署、NEADS だ。
> NEADS がすぐ呼べたのは、オーティスとラングレーの2か所、4機だけだった。

**c319** 🔧 ／ 図 模式 同じ地図（海の外から来る矢印だけ） ／ 委員会報告 p352（`only aircraft that were coming from overseas`）・p17（`was not recognized by NORAD before 9/11`）
> 乗っ取られた機が向かってくる想定は、海外から来る機だけだった。
> 国内の旅客機がミサイルにされることを、NORAD は、脅威と考えていなかった。

**c320** ／ 図 模式 時間の帯（7:59 から先が空白のまま伸びる） ／ 委員会報告 p18（`unsuited in every respect`）
> 委員会は、この手順はその朝の出来事に、あらゆる点で合っていなかった、と書いた。
> その朝、1機目の11便で、何が起きたのかを見ていく。

---

### 第3章　1機目　応答しない11便（26カット）

**c401** 🔧 ／ 図 NTSB 11便の経路（PDF p3 の経路図をなぞる・ボストンから西へ、南へ折れてニューヨークへ） ／ 委員会報告 p4（`Just before 8:14, it had climbed to 26,000 feet`）
> Q: 最初の便は、いつ、おかしくなったの？
> 8時14分の少し前まで、11便に、異常は無かった。
> 高度約7,900メートル（2万6,000フィート）まで上がっていた。

**c402** 🔧 ／ 実写 artcc_screen_pre（FAA の航空路管制センターの卓・A・全画面・ゆっくり寄る＝副題「航空路管制センター（別のセンター・年は不明）」） ／ NTSB 11便（`At 8:13:29`・`The crew acknowledged`・`The crew never acknowledged`）
> 担当は、ボストン・センター。空の道の機をレーダーで見守る、航空路管制センターだ。
> 8時13分29秒、右へ曲がる指示に、乗員は応えた。
> ところが18秒後の、上へ昇る指示には、もう応えなかった。

**c403** 🔧 ／ 図 模式 11便の機内（前の座席と操縦室の扉＝人は描かない） ／ 委員会報告 p4（`we believe the hijacking began at 8:14 or shortly thereafter`）・p5（`We do not know exactly how the hijackers gained access to the cockpit`）
> 委員会は、乗っ取りは8時14分か、その少しあとに始まった、とみている。
> 犯人たちが、どうやって操縦室に入ったのかは、はっきりとは分かっていない。

**c404** ／ 図 模式 機内の電話から地上への線（人は描かない） ／ 委員会報告 p5（`The cockpit is not answering, somebody's stabbed in business class`・`I think we're getting hijacked`）
> 8時19分。客室乗務員の1人が、機内の電話で、航空会社の予約の窓口につないだ。
> 「操縦室が応答しない。人が刺された。乗っ取られていると思う」

**c405** ／ 図 模式 同じ線（電話の時間の帯＝約25分） ／ 委員会報告 p5（`The emergency call lasted approximately 25 minutes`・`calmly and professionally relayed information`）
> 電話は約25分続いた。乗務員は、機内のようすを、落ち着いて地上へ伝え続けた。
> Q: 乗務員の人たちは、こういうときの訓練を、受けていたの？

**c406** ／ 図 模式 同じ線（機内から操縦室への線に×） ／ 委員会報告 p5（`took action outside the scope of their training, which emphasized that in a hijacking, they were to communicate with the cockpit crew`）
> 訓練が教えていたのは、乗っ取りのときは、操縦室と連絡を取ること。
> 地上へ伝え続けたのは、訓練の外の動きだった、と委員会は書いている。

**c407** ／ 図 RG237（ボストン・センターのレーダー再生の画面・11便の札が消える所・FAA・Unrestricted） ／ NTSB 11便（`At about 8:21`）・委員会報告 p18（`At 8:21, American 11 turned off its transponder, immediately degrading the information available about the aircraft`）
> 8時21分ごろ、11便のトランスポンダが切られた。
> 便名と高度を、地上のレーダーに知らせる機体の装置だ。
> 管制官の画面の点から、便名と高度の札が消えた。

**c408** ／ 図 RG237（同じ画面・札の無い点） ／ 委員会報告 p18（`The controller told his supervisor that he thought something was seriously wrong with the plane, although neither suspected a hijacking`）
> 管制官は上司に、何かがひどくおかしい、と伝えた。
> ただ2人とも、まだ乗っ取りとは考えていなかった。

**c409** 🔧 ／ 図 模式 管制の無線（ボストン・センターと11便を結ぶ線） ／ 委員会報告 p19（`We have some planes. Just stay quiet, and you'll be okay. We are returning to the airport`）
> 8時24分38秒。11便から、管制の無線に、声が流れた。
> 「こっちには何機かある。静かにしていれば大丈夫だ。空港へ戻る」

**c410** ／ 図 模式 同じ線（機内の放送と管制の無線の切り替え） ／ 委員会報告 p6（`inadvertently broadcast their message over the air traffic control channel instead of the cabin public-address channel`）・p19（`The controller only heard something unintelligible`）
> 乗客に向けた放送のつもりが、管制の無線に流れたとみられる。
> ただ管制官には、この声が、よく聞き取れなかった。

**c411** ／ 図 模式 同じ線（2つ目の声） ／ 委員会報告 p19（`Nobody move`・`The controller told us that he then knew it was a hijacking`）
> Q: つまり、まだ乗っ取りだとは、分からなかったんだね？
> そう。けれど、すぐあとに、「誰も動くな」という声が続いた。
> 管制官は、これで乗っ取りだと分かった、と委員会に話している。

**c412** 🔧 ／ 図 模式 時間の帯（11便＝8:25 ボストン・センターが知る） ／ 図表 p32（`Boston Center aware of hijacking`）・委員会報告 p19（`Between 8:25 and 8:32, in accordance with the FAA protocol, Boston Center managers started notifying their chain of command`）
> 8時25分から32分のあいだに、ボストン・センターの管理職は、
> 手順どおり、FAA の上の段へ、乗っ取りを伝え始めた。

**c413** ／ 図 模式 手順の段（上へ伸びる矢印と、横から軍へ伸びる矢印） ／ 委員会報告 p20（`Boston Center did not follow the protocol in seeking military assistance through the prescribed chain of command`・`at 8:34, to contact the military through the FAA's Cape Cod facility`）
> ただ、軍を呼ぶところは、決められた段を飛ばした。
> 8時34分、ケープコッドにある FAA の施設を通して、軍を呼ぼうとしている。

**c414** ／ 図 模式 同じ（アトランティックシティの昔の基地に×） ／ 委員会報告 p20（`The center also tried to contact a former alert site in Atlantic City, unaware it had been phased out`）
> すでに無くなったことを知らずに、アトランティックシティの、
> 昔の待機の基地にも、電話をかけている。

**c415** ／ 図 模式 電話の線（ボストン・センターから NEADS へ・8:37:52） ／ 委員会報告 p20（`At 8:37:52, Boston Center reached NEADS. This was the first notification received by the military`）
> 8時37分52秒。電話が、NEADS につながった。
> これが、11便の乗っ取りが軍に届いた、最初の知らせだ。

**c416** ／ 図 模式 同じ線（やりとりは字幕だけ・画面に大きく出さない） ／ 委員会報告 p20（`We have a hijacked aircraft headed towards New York`・`Is this real-world or exercise?`・`No, this is not an exercise, not a test`）
> 「乗っ取られた機が、ニューヨークへ向かっている」。NEADS は、
> 「本物か、演習か」と聞き返した。答えは、「演習ではない。試験でもない」。

**c417** ／ 図 模式 同じ線（演習の予定表の札＝旧ソ連の爆撃機の想定） ／ 委員会報告 p458（`Vigilant Guardian`・`if anything, expedited`）
> Q: 演習と、取り違えたりしなかったの？
> その朝は、ちょうど軍の演習が予定されていた。旧ソ連の爆撃機を想定したものだ。
> 委員会は、演習で人が多かったぶん、対応はむしろ早まった、とみている。

**c418** ／ 実写 F-15 オーティス基地（別の点・2001年秋のニューヨーク上空の警戒・102戦闘航空団・A・全画面・左へ流す＝副題「オーティス基地のF-15（2001年秋）」） ／ 委員会報告 p20（`NEADS ordered to battle stations the two F-15 alert aircraft at Otis Air Force Base in Falmouth, Massachusetts, 153 miles away from New York City`）
> NEADS は、オーティス基地の F-15戦闘機2機を、すぐ飛べる構えにさせた。
> オーティスからニューヨークまでは、約246キロ（153マイル）ある。

**c419** 🔧 ／ 図 模式 北東部の地図（オーティスからの線・行き先に「？」） ／ 委員会報告 p20（`scrambled at 8:46 from Otis Air Force Base`・`I don't know where I'm scrambling these guys to. I need a direction, a destination`）
> 8時46分、発進の命令が出た。けれど、どこへ向かわせればいいのか分からない。
> 戦闘機に指示を出す将校は、「方角が要る。行き先が要る」と情報を求めた。

**c420** ／ 図 模式 レーダーの画面（札の無い点を探す） ／ 委員会報告 p20（`NEADS personnel spent the next minutes searching their radar scopes for the primary radar return`）
> トランスポンダが切られていたため、NEADS は、札の無い点を、
> レーダーの画面の上で、探し続けた。

**c421** ／ 実写 wtc_far（事件の前の世界貿易センター・1976年・D＝米議会図書館蔵／知られた制限なし・縦長＝全画面で上下を切る・ゆっくり上へ＝副題「事件の前の世界貿易センター（1976年）」） ／ 委員会報告 p7（`At 8:46:40, American 11 crashed into the North Tower of the World Trade Center in New York City`）
> 8時46分40秒。11便は、ニューヨークの世界貿易センターの北棟にぶつかった。

**c422** ／ 実写 wtc_base（事件の前の世界貿易センター・1976年・D・縦長＝全画面で上下を切る・ゆっくり寄る＝副題「事件の前の世界貿易センター（1976年）」） ／ 委員会報告 p278（`Both towers had 110 stories, were about 1,350 feet high`・`up to 50,000 office workers occupied the towers`）
> 北棟と南棟は、どちらも110階建て。高さは約410メートル（1,350フィート）。
> 働く日には、2つのビルに、多いときで5万人がいた。

**c423** ／ 図 模式 時間の帯（8:37:52 から 8:46:40 まで＝9分の帯・8:53 に離陸の印） ／ 委員会報告 p20（`Radar data show the Otis fighters were airborne at 8:53`）・p21（`That nine minutes' notice before impact was the most the military would receive of any of the four hijackings`）
> F-15が飛び立ったのは、8時53分。北棟にぶつかった、あとだった。
> 軍が知らされてから、ぶつかるまでは、9分。
> 4機のうち、軍が前もって受けた知らせで、これがいちばん長い。

**c424** 🔧 ／ 図 模式 同じ帯（NEADS のレーダーの画面を小さく重ねる） ／ 委員会報告 p20（`while NEADS personnel were still trying to locate the flight, word reached them that a plane had hit the World Trade Center`）
> Q: 戦闘機は、間に合わなかったんだね。
> そう。NEADS がまだ11便を探しているうちに、
> 飛行機がビルにぶつかった、という知らせが届いた。

**c425** 🔧 ／ 図 模式 手順の段（ボストン・センターから上へ伸びる段と、軍への近道） ／ 委員会報告 p19（`did not contact the NMCC to request a fighter escort`）
> Q: ボストンは、手順の段を飛ばしてでも、急いだんだ。
> そう。一方、段の上の本部は、国防総省の指揮所に、戦闘機の護衛を頼まなかった。

**c426** ／ 図 模式 3つの前提の箱（1つ目の「姿を消そうとはしない」に×） ／ 委員会報告 p31（`had never handled a hijacked aircraft that attempted to disappear`）
> 3つの前提の1つ目は、この時点で、もう崩れていた。
> 11便は、トランスポンダを切り、姿を消そうとした。次は、2機目だ。

---

### 第4章　2機目　気づいていた管制官（20カット）

**c501** ／ 実写 wtc_south（事件の前の世界貿易センター・1976年・D・縦長＝全画面で上下を切る・右へ流す＝副題「事件の前の世界貿易センター（1976年）」） ／ 委員会報告 p21（`At approximately 8:42, shortly after entering New York Center's airspace, the pilot of United 175 broke in`）
> Q: 次の便は、そのころ、どこにいたの？
> 175便は、ニューヨークの航空路管制センターの受け持ちに入ったところだった。
> 8時42分ごろ、175便の操縦士が、無線でこう伝えている。

**c502** 🔧 ／ 図 模式 管制の無線（ニューヨーク・センターと175便を結ぶ線） ／ 委員会報告 p7（`a "suspicious transmission" overheard from another plane (which turned out to have been Flight 11) just after takeoff`・`This was United 175's last communication with the ground`）
> 「ボストンを出るとき、怪しい無線を聞いた」。
> あとで分かると、それは11便から流れた声だった。
> 委員会は、これが175便と地上との、最後の交信だった、と書いている。

**c503** ／ 図 模式 175便の機内（前の座席と操縦室の扉＝人は描かない） ／ 委員会報告 p7（`The hijackers attacked sometime between 8:42 and 8:46`）・NTSB 175便（`at 8:47, when the aircraft changed beacon codes twice within a one-minute period`）
> 乗っ取りは、8時42分から46分のあいだに始まった。
> 8時47分、トランスポンダが知らせる番号が、1分のうちに2回、書き換わった。

**c504** 🔧 ／ 図 RG237（ニューヨーク・センターのレーダー再生の画面・175便の札の番号が変わる所） ／ 委員会報告 p21（`The New York Center controller and manager were unaware that American 11 had already crashed`・`At 8:51, the controller noticed the transponder change from United 175 and tried to contact the aircraft. There was no response`）
> 担当の管制官は、11便も受け持ち、もうぶつかったとは知らずに探していた。
> 番号の変化に気づいたのは、8時51分。呼びかけても、応答は無かった。

**c505** ／ 図 模式 機内の電話から地上への線（人は描かない） ／ 委員会報告 p7（`a male flight attendant called a United office in San Francisco`・`both pilots had been killed, a flight attendant had been stabbed`）・p8（`the hijackers were probably flying the plane`）
> 8時52分。175便の客室乗務員の1人が、航空会社の事務所に電話した。
> 操縦士2人が殺され、乗務員が刺された。たぶん、犯人が操縦している、と。

**c506** 🔧 ／ 図 RG237（同じ画面・175便の点が向きを変える） ／ 委員会報告 p22（`saying that "we may have a hijack" and that he could not find the aircraft`）
> 8時53分。ニューヨーク・センターの管制官は、同僚に伝えた。
> 「乗っ取りかもしれない」。機体が、見つからない、と。

**c507** ／ 図 模式 時間の帯（175便＝8:53「乗っ取りかもしれない」・8:55 上司へ） ／ 委員会報告 p22（`At about 8:55, the controller in charge notified a New York Center manager that she believed United 175 had also been hijacked`）
> Q: つまり、地上の管制官は、もう乗っ取りだと見ていたんだね？
> そう。8時55分ごろには、現場の責任者が上司に、
> 175便も乗っ取られたと思う、と伝えている。

**c508** 🔧 ／ 図 模式 手順の段（ニューヨーク・センターの上司から地域の管理職へ＝扉が閉じている） ／ 委員会報告 p22（`The manager tried to notify the regional managers and was told that they were discussing a hijacked aircraft (presumably American 11) and refused to be disturbed`）
> その上司は、さらに上の地域の管理職に伝えようとした。
> ところが管理職たちは、乗っ取られた機、たぶん11便について話し合っていて、
> 邪魔をされたくない、と取り次ぎを断った。

**c509** ／ 図 RG237（同じ画面） ／ 委員会報告 p22（`we might have a hijack over here, two of them`）
> 8時58分。175便を探す管制官は、別の管制官に言った。
> 「こっちで乗っ取りが起きているかもしれない。2機だ」

**c510** ／ 図 模式 電話の線（ニューヨーク・センターからハーンドンのコマンドセンターへ） ／ 委員会報告 p22（`Between 9:01 and 9:02, a manager from New York Center told the Command Center in Herndon`・`We have several situations going on here. It's escalating big, big time. We need to get the military involved with us`）
> 9時1分から2分にかけて、ニューヨーク・センターの管理職は、
> FAA のコマンドセンターに伝えた。「いくつもの事態が起きている。
> どんどん大きくなっている。軍の助けが要る」

**c511** ／ 図 模式 北アメリカの地図（バージニア州ハーンドンの印） ／ 委員会報告 p14（`Command Center, located in Herndon`）・p16（`Virginia, which oversees daily traffic flow within the entire airspace system`）
> Q: コマンドセンターって、どういう所なの？
> 全米の空の流れを見渡す、FAA の司令塔だ。
> 首都に近い、バージニア州のハーンドンにある。

**c512** 🔧 ／ 図 RG237（175便の点がマンハッタンの南部の上で途切れる） ／ 委員会報告 p22（`Heads up man, it looks like another one coming in`・`the radar data terminated over Lower Manhattan`）
> 9時2分、管制官の声が録音に残っている。「気をつけろ。また1機、来るみたいだ」。
> レーダーの点は、マンハッタンの南部の上で、途切れた。

**c513** ／ 実写 wtc_smoke_day（LC-A05-A01・エンパイア・ステート・ビルの向こうで燃える両棟・C'＝米議会図書館蔵（撮影者不詳）・全画面・ゆっくり寄る＝副題「燃える世界貿易センター（当日）」） ／ 委員会報告 p8（`At 9:03:11, United Airlines Flight 175 struck the South Tower of the World Trade Center`）
> 9時3分11秒。175便は、南棟にぶつかった。
> これで、2つのビルが、どちらも燃えることになった。

**c514** 🔧 ／ 実写 当日の世界貿易センター（A・Commons の説明に当日の日付がある14点から選ぶ・全画面・左へ流す＝副題は絵を見て書く） ／ 委員会報告 p23（`came in a phone call from New York Center to NEADS at 9:03`・`The notice came at about the time the plane was hitting the South Tower`）
> NEADS に、175便のことを知らせる最初の電話が入ったのは、9時3分。
> ちょうど、南棟にぶつかったころだった。

**c515** 🔧 ／ 実写 事件の前の世界貿易センター（D・別の点＝語りは 8:51〜9:02＝両棟が燃える写真は置かない。北棟だけが燃える点が見つかればそれ＝副題は絵を見て書く） ／ 委員会報告 p22（`refused to be disturbed`・`Between 9:01 and 9:02, a manager from New York Center told the Command Center`）・p23（`came in a phone call from New York Center to NEADS at 9:03`）
> Q: 気づいた人はいたのに、どうして、間に合わなかったの？
> 管制官が気づいてから、軍に届くまで、知らせは、何人もの人と段を通った。
> そのあいだに、175便は、もうニューヨークの上にいた。

**c516** ／ 図 模式 時間の帯（11便と175便を並べる・FAA が知った印＝乗っ取りから11分後と9分後） ／ 委員会報告 p455（`The FAA knew or strongly suspected that Flight 11 was a hijacking 11 minutes after it was taken over; Flight 175, 9 minutes after it was taken over`）
> 委員会の注によると、FAA は、11便が乗っ取りだと、
> 乗っ取られてから11分後に、知っていたか、強く疑っていた。175便は9分後だ。

**c517** ／ 図 模式 北東部の地図（ロングアイランドの沖の軍の空域・F-15の線） ／ 委員会報告 p20（`Lacking a target, they were vectored toward military-controlled airspace off the Long Island coast`）・p23（`decided against holding the fighters in military airspace away from Manhattan`）
> 8時53分に飛び立った F-15は、目標が無いまま、
> ロングアイランドの沖へ向かっていた。
> 2機目のあと、NEADS は、マンハッタンから離して待たせるのを、やめると決めた。

**c518** 🔧 ／ 実写 小学校の部屋のテレビに映る燃える両棟（ホワイトハウスの写真係・説明「9:10ごろ」・A の見込み＝権利の札は映像方針で確かめる・子どもが写るなら顔だけモザイク・全画面＝副題「フロリダ州の小学校（当日）」） ／ 委員会報告 p38（`The President was seated in a classroom when, at 9:05`・`A second plane hit the second tower. America is under attack`）
> そのころ、ブッシュ大統領は、フロリダ州の小学校にいた。
> 9時5分、首席補佐官が、耳もとでささやいた。
> 「2機目が、もう1つのビルにぶつかりました。アメリカは攻撃を受けています」

**c519** ／ 実写 当日の世界貿易センター（A・別の点＝副題は絵を見て書く） ／ 委員会報告 p35（`nearly everyone in the White House told us, they immediately knew it was not an accident`）
> ホワイトハウスでは、2機目のニュースで、ほとんどの人が、
> これは事故ではない、とすぐに分かった、と委員会に話している。

**c520** ／ 図 模式 時間の帯（11便と175便＝軍に届いた時刻の印） ／ —
> Q: つまり、地上では気づいていたのに、軍に届くのが、遅れたんだね？
> そう。そしてこのとき、3機目は、もう管制官の画面から消えていた。

---

### 第5章　3機目　画面から消えた点（24カット）

**c601** ／ 実写 pentagon_ext_pre（事件の前のペンタゴン・1998年・A・全画面・ゆっくり寄る＝副題「事件の前のペンタゴン（1998年）」） ／ 委員会報告 p8（`At 8:51, American 77 transmitted its last routine radio communication`）
> Q: その次の便は、そのころ、どこを飛んでいたの？
> ワシントンを出た77便は、西のロサンゼルスへ向かっていた。
> 8時51分には、ふだんどおりの交信をしている。

**c602** ／ 図 NTSB 77便の経路（PDF p5 の地図をなぞる・南へ曲がり、東へ戻る線） ／ 委員会報告 p8（`The hijacking began between 8:51 and 8:54`）・p24（`American 77 began deviating from its flight plan at 8:54, with a slight turn toward the south`）
> 乗っ取りは、8時51分から54分のあいだに始まった。
> 8時54分、77便は決められた道を外れ、南へ曲がり始めた。

**c603** ／ 図 RG237（インディアナポリス・センターのレーダー再生の画面・77便の札が消える所） ／ 委員会報告 p25（`its transponder was turned off at 8:56`）
> 8時56分、77便のトランスポンダが切られた。
> 見守っていたのは、インディアナポリスの航空路管制センターだ。
> その管制官の画面から、77便の点が、消えた。

**c604** 🔧 ／ 図 RG237（同じ画面・点の無いまま時計が進む） ／ 委員会報告 p25（`FAA radar equipment tracked the flight from the moment its transponder was turned off at 8:56`・`for 8 minutes and 13 seconds, between 8:56 and 9:05, this primary radar information on American 77 was not displayed to controllers at Indianapolis Center`）
> Q: レーダーが、壊れていたの？
> あとの調べで、FAA のレーダーは、点が消えたあとも77便を捉えていた。
> けれど8分13秒のあいだ、その点は、管制官の画面に出ていなかった。

**c605** 🔧 ／ 図 模式 レーダーの重ね方（一次レーダーの点・札・画面＝人は描かない） ／ 委員会報告 p25（`The reasons are technical, arising from the way the software processed radar information`）
> 理由は技術的で、管制のソフトが、
> レーダーの情報をどう扱うかと、77便の辺りのレーダーの弱さによる、と委員会は書く。

**c606** ／ 図 NTSB 77便の経路（同じ地図・管制官が西と南西を見る矢印と、東へ向かう線） ／ 委員会報告 p25（`looked to the west and southwest along the flight's projected path, not east`）
> 管制官たちは、77便を、予定の道の先の、西と南西に探した。
> けれど77便は、そのとき、東へ向かっていた。

**c607** ／ 図 RG237（9:05 に東で点が戻る所） ／ 委員会報告 p25（`reemerged as a primary target on Indianapolis Center radar scopes at 9:05, east of its last known position`・`controllers had either stopped looking for the aircraft because they thought it had crashed or were looking toward the west`）
> 9時5分、77便の点は、東の方で画面に戻ってきた。ただそのころには、
> 管制官は、墜ちたと考えて探すのをやめたか、西を見ていた。

**c608** ／ 図 模式 同じ地図（西を見る矢印と、東へ伸びる線を並べる） ／ 委員会報告 p25（`Indianapolis Center never saw Flight 77 turn around`）
> Q: つまり、画面に出ないあいだに、逆の方へ飛んでいたんだね？
> そう。インディアナポリス・センターは、77便が向きを変えるところを、
> 見ていなかった。

**c609** 🔧 ／ 実写 当日の世界貿易センター（A・別の点・両棟が燃える時刻の点だけ・全画面・左へ流す＝副題は絵を見て書く） ／ 委員会報告 p9（`Shortly before 9:10, suspecting that American 77 had been hijacked, American headquarters concluded that the second aircraft to hit the World Trade Center might have been Flight 77`）・p455（`There is no evidence to indicate that the FAA recognized Flight 77 as a hijacking until it crashed into the Pentagon`）
> 9時10分の少し前、アメリカン航空の本社は、77便の乗っ取りを疑い、
> ビルにぶつかった2機目は、77便かもしれない、と考えた。実際は175便だ。
> FAA が77便を乗っ取りと認めた跡は、ぶつかるまで無い、と委員会は書く。

**c610** ／ 図 模式 機内の電話から地上への線（人は描かない） ／ 委員会報告 p9（`the hijackers had knives and box cutters`・`they had put all the passengers in the back of the plane`）
> 機内からは、乗客の1人が家族に電話している。
> 犯人たちはナイフとカッターを持ち、乗客を全員、後ろへ集めた、と。

**c611** 🔧 ／ 図 模式 北東部の地図（ボストン・センターから NEADS への電話・「9:21 ボストン・センター→NEADS」の札＝電話の言葉は字幕だけ） ／ 委員会報告 p26（`I just had a report that American 11 is still in the air, and it's on its way towards`）
> そのころ NEADS には、別の知らせが届いていた。
> 9時21分、ボストン・センターからの電話だ。
> 「11便は、まだ飛んでいる。ワシントンへ向かっている」

**c612** 🔧 ／ 図 模式 同じ地図（北棟に×・11便の札） ／ 委員会報告 p26（`We have been unable to identify the source of this mistaken FAA information`）
> Q: えっ、その便が、まだ飛んでいるって？
> 誤った知らせだった。11便は、30分以上前に、北棟にぶつかっている。
> どこから出た話なのか、委員会も、突き止められなかった。

**c613** 🔧 ／ 図 模式 ラングレーから東の海へ伸びる線 ／ 委員会報告 p27（`That order was processed and transmitted to Langley Air Force Base at 9:24`・`Radar data show the Langley fighters airborne at 9:30`・`not headed north toward the Baltimore area as instructed, but east over the ocean`）
> この知らせを受けて、9時24分、ラングレー基地に発進の命令が届いた。
> 9時30分に飛び立った戦闘機は、北ではなく、東の海の上へ向かった。

**c614** ／ 図 模式 同じ線（3つの理由の札＝目標の場所が無い・決まった飛び方の型・読み違え） ／ 委員会報告 p27（`The Langley fighters were heading east, not north, for three reasons`・`this order did not include a distance to the target or the target's location`）
> Q: もう無い便を追って、しかも、違う方へ飛んだってこと？
> そう。命令に目標の場所が無かったことなど、委員会は理由を3つ挙げている。

**c615** ／ 図 RG237（ダレスのレーダー再生・東へ速く動く点） ／ 委員会報告 p25（`observed a primary radar target tracking eastbound at a high rate of speed`・`The aircraft's identity or type was unknown`）
> 9時32分。ダレス空港の管制官たちが、東へ速く動く、ひとつの点を見つけた。
> 正体も、機の種類も、分からない。

**c616** 🔧 ／ 図 模式 ワシントンの地図（ホワイトハウス・ペンタゴン・レーガン空港・点の動き） ／ 委員会報告 p27（`it had come by chance`）・p34（`It was notified at 9:34 that American 77 was lost`・`an unknown plane was 6 miles southwest of the White House`）
> 9時34分、NEADS は、別の用でかけた電話で、「77便も見失った」と知る。
> 数分後、「ホワイトハウスの南西約10キロ（6マイル）に、正体不明の機」。

**c617** 🔧 ／ 図 NTSB 77便の経路（ペンタゴンの西南西で時計回りに大きく回る線） ／ 委員会報告 p9（`American 77 was then 5 miles west-southwest of the Pentagon and began a 330-degree turn`）
> 同じ9時34分、77便は、ペンタゴンの西南西、約8キロ（5マイル）にいた。
> 時計回りに330度、回りながら、降りていった。

**c618** ／ 図 NTSB 77便 図2（PDF p4・飛行の記録装置の高度を、点を結んで順に描く） ／ 委員会報告 p9（`descending through 2,200 feet, pointed toward the Pentagon and downtown Washington`）・NTSB 77便（`Altitude Profile`）
> 回り終えたとき、高度は約670メートル（2,200フィート）。
> 機首の先には、ペンタゴンと、ワシントンの中心があった。
> 飛行の記録装置の記録では、最後の4分ほどで、地上まで下がっている。

**c619** ／ 図 模式 ワシントン上空（低く飛ぶ軍の輸送機 C-130H と77便の線） ／ 委員会報告 p25（`vectored an unarmed National Guard C-130H cargo aircraft`）・p26（`identified it as a Boeing 757`）
> 首都のレーガン・ナショナル空港の管制官は、近くを飛ぶ軍の輸送機に、
> その機を見て、追うよう頼んだ。輸送機の操縦士は、ボーイング757だと見分けた。

**c620** ／ 実写 当日のペンタゴン（米軍の写真・A・Commons の説明に当日の日付・煙の上がる遠景・全画面・ゆっくり寄る＝副題は絵を見て書く） ／ 委員会報告 p10（`At 9:37:46, American Airlines Flight 77 crashed into the Pentagon, traveling at approximately 530 miles per hour`）
> 9時37分46秒。77便は、ペンタゴンにぶつかった。
> 速さは、時速約850キロ（530マイル）だった。

**c621** ／ 実写 DF-SD-02-09094（米空軍・当日・放水と救急車・軍人と消防・A・全画面・左へ流す＝副題「当日のペンタゴン」） ／ 委員会報告 p26（`at 9:38, seconds after impact, reported to the control tower`・`looks like that aircraft crashed into the Pentagon sir`）
> 衝突の数秒後、輸送機の操縦士は、管制塔に伝えている。
> 「あの機は、ペンタゴンにぶつかったようです」

**c622** ／ 実写 pentagon_west_day（DM-SD-02-03925・米海兵隊・煙が晴れたあとの建物の内側の環・A・全画面・使う窓だけ原寸で見る＝副題「当日のペンタゴン」） ／ 記念館（`184 people were killed at the Pentagon`）・委員会報告 p552 注188（`attack killed 184 nonterrorists`）
> ペンタゴンでは、乗っていた人と建物の中にいた人、あわせて184人が亡くなった。
> この数に、乗っ取った5人は入っていない。

**c623** 🔧 ／ 実写 当日のペンタゴン（米軍の写真・A・別の点・衝突のすぐ後の煙＝副題は絵を見て書く） ／ 委員会報告 p27（`The Langley fighters were about 150 miles away`）
> Q: 戦闘機は、そのとき、どこにいたの？
> ラングレーの戦闘機は、ワシントンから約240キロ（150マイル）離れていた。

**c624** 🔧 ／ 実写 DN-SD-03-11447（米海軍・夕方の西側と消防車・崩れた外の環・A・全画面・右へ流す＝副題「当日の夕方のペンタゴン」） ／ 委員会報告 p26（`identified it as a Boeing 757`）・注154 p461（`Commission analysis of FDR`）・NTSB 77便 図2（`FDR Pressure Altitude`）
> Q: ペンタゴンにぶつかったのは、本当に旅客機だったの？
> 輸送機の操縦士が、757だと見分けている。
> 77便の飛行の記録装置も回収され、その記録から、最後の飛び方が描かれている。

---

### 第6章　空を閉じる（16カット）

**c701** 🔧 ／ 実写 当日の世界貿易センター（A・Commons の説明に当日の日付がある14点から・両棟が燃える時刻の点だけ・全画面・右へ流す＝副題は絵を見て書く） ／ 図表 p33（`nationwide ground stop`）・委員会報告 p25（`the Command Center ordered one at 9:25`）
> Q: そのあいだ、空の上のほかの飛行機は、どうなっていたの？
> 9時25分。ハーンドンのコマンドセンターが、全米で離陸を止めた。
> ただ、止めたのは地上の機で、もう飛んでいる機は、そのままだ。

**c702** 🔧 ／ 図 模式 全米の地図（空港の点が止まる＝離陸の停止・「本部は話し合い中」の札） ／ 委員会報告 p25（`A manager at the Herndon Command Center asked FAA headquarters if they wanted to order a`・`While this was being discussed by executives at FAA headquarters, the Command Center ordered one at 9:25`）
> 止める前、コマンドセンターは FAA の本部に、離陸を止めるかを尋ねていた。
> 本部の幹部が話し合っているうちに、コマンドセンターは自分で決めた。

**c703** 🔧 ／ 図 模式 全米の地図（アメリカン航空の便の点が止まる＝9:00 北東部・9:05〜9:10 全米） ／ 委員会報告 p9（`He ordered all American Airlines flights in the Northeast that had not taken off to remain on the ground`・`extended the ground stop nationwide`）・p10（`nationwide ground stop between 9:05 and 9:10`）
> 航空会社は、それより先に動いていた。アメリカン航空は9時ごろ、
> 北東部で、まだ飛び立っていない便を止め、9時10分までに全米へ広げた。

**c704** 🔧 ／ 図 模式 コマンドセンターの卓の配置（人は描かない） ／ 委員会報告 p29（`The Command Center’s national operations manager, Ben Sliney`）
> その日、コマンドセンターで全米の運用をまとめていたのは、ベン・スライニー。
> 全米の空の流れの、責任者だ。

**c705** 🔧 ／ 実写 当日のペンタゴン（米軍の写真・A・別の点・煙の柱の遠景＝副題は絵を見て書く） ／ 委員会報告 p29（`At 9:42, the Command Center learned from news reports that a plane had struck the Pentagon`）・スタッフ声明 p15（`At 9:42, Command Center learned from television news reports`）
> 9時42分。コマンドセンターは、ペンタゴンに機がぶつかったことを、
> テレビの報道で知った。ぶつかってから、およそ4分後のことだ。

**c706** 🔧 ／ 実写 当日の世界貿易センター（A・別の点・両棟が燃える時刻の点だけ＝副題は絵を見て書く） ／ 委員会報告 p29（`ordered all FAA facilities to instruct all aircraft to land at the nearest airport`）
> スライニーは、全米の FAA の施設に命じた。
> 飛んでいるすべての機に、いちばん近い空港へ降りるよう、伝えよ。

**c707** 🔧 ／ 図 模式 全米の地図（飛んでいる機の点が、いちばん近い空港へ向かう矢印） ／ —
> Q: 空にいる飛行機を、全部、降ろすってこと？
> そう。旅客機も、小さな自家用機も、すべてだ。

**c708** 🔧 ／ 図 模式 同じ地図（命令の時刻の札は空白） ／ 委員会報告 p29（`This was an unprecedented order`）
> 委員会は、これを「前例の無い命令」と書いている。
> ただ、命令が何時何分に出たのかは、報告書に書かれていない。

**c709** 🔧 ／ 図 模式 同じ地図（命令の札を2つ並べる＝報告書と証言・時刻と言葉は字幕だけ） ／ 運輸長官の証言（`at approximately 9:45 a.m.`・`I gave the FAA the final order for all civil aircraft to land at the nearest airport as soon as possible`）
> 当時の運輸長官は、のちの公聴会で、こう話している。
> 9時45分ごろ、すべての民間機を降ろす、最後の命令を FAA に出した、と。

**c710** 🔧 ／ 図 模式 同じ地図（2つの札に「報告書」「本人の証言」） ／ —
> Q: 結局、空を閉じたのは、誰の命令だったの？
> 委員会の報告書は、スライニーの命令として書いている。
> 長官の「最後の命令」は、本人の証言として残っている。

**c711** 🔧 ／ 図 模式 全米の地図（点が減っていく・数の札「約4,500機」） ／ 委員会報告 p29（`The air traffic control system handled it with great skill, as about 4,500 commercial and general aviation aircraft soon landed without incident`）
> 管制は、降ろす命令を見事にこなした。
> 旅客機と小型機、約4,500機が、まもなく、事故なく降りた。

**c712** 🔧 ／ 実写 大統領専用機の機内で電話をする大統領（ホワイトハウスの写真係・A・全画面・ゆっくり寄る・撮影の時刻は書かない＝副題「当日、大統領専用機の機内」） ／ 委員会報告 p39（`Air Force One departed at about 9:54 without any fixed destination`）
> Q: そんなにたくさんの飛行機が、無事に降りられたんだ。
> その一方で、大統領を乗せた専用機は、9時54分ごろ、
> 行き先を決めないまま、空へ上がっている。

**c713** 🔧 ／ 実写 バークスデール空軍基地の大統領（ホワイトハウスの写真係・A・手前の記者は顔だけモザイク・全画面＝副題「当日、ルイジアナ州の空軍基地」） ／ 委員会報告 p325（`Air Force One flew to Barksdale Air Force Base in Louisiana`）
> 専用機は、そのあと、ルイジアナ州のバークスデール空軍基地に降りた。

**c714** 🔧 ／ 図 模式 全米の地図（点が空港へ降りきる） ／ 委員会報告 p31（`thought outside the box in recommending a nationwide alert, in ground-stopping local traffic, and, ultimately, in deciding to land all aircraft and executing that unprecedented order flawlessly`）
> 委員会は、FAA の管制官や管理職が、型にとらわれずに考えて動いた、と書く。
> 全米に警報を出すよう求め、離陸を止め、すべての機を降ろしきった。

**c715** ／ 図 模式 同じ地図 ／ —
> Q: つまり、空の流れを止めるところは、うまくいったんだね？
> そう。ただ、その陰で、軍への知らせは、まだ遅れていた。

**c716** 🔧 ／ 図 模式 時間の帯（9:42 に報道で知る〜9:46・93便はすでに乗っ取られている） ／ 委員会報告 p29（`At 9:46 the Command Center updated FAA headquarters that United 93 was now "twenty-nine minutes out of Washington, D.C."`）
> 空にいた機が降りていくなかで、4機目の93便は、もう乗っ取られていた。
> 9時46分、コマンドセンターは FAA の本部に伝えている。
> 93便は、ワシントンまで、あと29分の所にいる、と。

---

### 第7章　4機目　93便の35分（35カット）

**c801** 🔧 ／ 実写 ニューアーク空港の93便の搭乗口の記念の旗（後年・C・全画面・ゆっくり寄る＝副題「現在のニューアーク空港・93便の搭乗口」） ／ 委員会報告 p10（`As United 93 left Newark, the flight's crew members were unaware of the hijacking of American 11`）
> Q: 最後の便は、どこから飛び立ったの？
> 8時42分にニューアークを飛び立った93便は、西へ向かっていた。
> 乗員たちは、11便が乗っ取られたことを、まだ知らない。

**c802** ／ 図 NTSB 93便の経路（PDF p3 の地図をなぞる・ニューアークから西へ） ／ 委員会報告 p10（`Around 9:00, the FAA, American, and United were facing the staggering realization of apparent multiple hijackings`）
> 9時ごろには、FAA と航空会社が、
> 乗っ取りが何機も起きているらしい、と気づき始めていた。

**c803** 🔧 ／ 図 模式 操縦室の画面に届く文字の連絡（人は描かない） ／ 委員会報告 p11（`Beware any cockpit intrusion`）
> 9時19分。ユナイテッドの運航管理の担当が、受け持つ便に、文字の警告を送り始めた。
> 「操縦室への侵入に気をつけよ。2機が世界貿易センターにぶつかった」

**c804** 🔧 ／ 図 模式 同じ（93便の画面に届く＝9:24） ／ 委員会報告 p11（`warning to United 93 was received in the cockpit`）
> 93便の操縦室に届いたのは、9時24分。
> Q: その警告に、操縦室は、どう応えたの？

**c805** ／ 図 模式 同じ（返信の文字＝字幕だけ） ／ 委員会報告 p11（`responded with a note of puzzlement`・`confirm latest mssg plz`）
> 2分後、機長は、戸惑ったように、こう返している。
> 「最新の連絡を、確かめてほしい」

**c806** ／ 図 NTSB 93便の高度（9:28 の小さな降下の印） ／ 委員会報告 p11（`The hijackers attacked at 9:28`・`While traveling 35,000 feet above eastern Ohio, United 93 suddenly dropped 700 feet`）・NTSB 93便（`a brief descent of about 600 feet starting at 9:28`）
> 9時28分。高度約1万700メートル（3万5,000フィート）を飛ぶ93便が、
> 急に約210メートル（700フィート）下がった。乗っ取りが始まった。

**c807** 🔧 ／ 図 模式 管制の無線（クリーブランド・センターと93便を結ぶ線） ／ 委員会報告 p11（`could be heard declaring "Mayday" amid the sounds of a physical struggle in the cockpit`・`Hey get out of here`）
> クリーブランドの管制センターの無線に、機長か副操縦士の声が入った。
> 「メーデー」という声と、争う音。続いて、「ここから出ていけ」という叫び。

**c808** 🔧 ／ 図 模式 同じ（機内の放送が無線に流れる線） ／ 委員会報告 p12（`made or attempted to make the following announcement to the passengers`・`We have a bomb on board`）・p28（`At 9:32, a third radio transmission came over the frequency`）・p13（`we believe the bombs were probably fake`）
> 9時32分。犯人の1人が、乗客に向けて放送しようとした声が、管制の無線に流れた。
> 「座っていろ。機内に爆弾がある」。
> この爆弾も、おそらく偽物だった、と委員会はみている。

**c809** 🔧 ／ 図 NTSB 93便の経路（オハイオの上で向きを変え、東へ戻る線） ／ 委員会報告 p12（`instructed the plane's autopilot to turn the aircraft around and head east`）
> 飛行の記録装置によると、そのあと93便の自動操縦に、東へ向かう指示が入った。
> 4機目は、来た道を、東へ引き返し始めた。

**c810** ／ 図 模式 時間の帯（93便＝9:28 乗っ取り・9:34 FAA 本部へ） ／ 委員会報告 p28（`By 9:34, word of the hijacking had reached FAA headquarters`）
> 9時34分には、93便の乗っ取りは、FAA の本部に伝わっていた。
> Q: それなら、軍にも、すぐ伝わったんだよね？

**c811** ／ 図 模式 手順の段（FAA 本部から国防総省への矢印が途中で止まる） ／ 委員会報告 p29（`At 9:49, 13 minutes after Cleveland Center had asked about getting military help, the Command Center suggested that someone at headquarters should decide whether to request military assistance`）
> 伝わっていない。9時49分、コマンドセンターは本部に、
> 軍に助けを頼むかどうか、誰かが決めるべきだ、と促している。

**c812** 🔧 ／ 図 模式 同じ（矢印に×） ／ 委員会報告 p30（`no one from FAA headquarters requested military assistance regarding United 93. Nor did any manager at FAA headquarters pass any of the information it had about United 93 to the military`）
> けれど、FAA の本部から軍へ、助けを頼むことも、
> 93便の知らせを渡すことも、無かった。

**c813** 🔧 ／ 図 模式 時間の帯（9:41 トランスポンダの印） ／ NTSB 93便（`stopped receiving transponder returns`）・委員会報告 p29（`The controller located it on primary radar`・`tracked the flight as it turned east, then south`）
> その前の9時41分ごろ、93便のトランスポンダも、切られた。
> 札は消えたが、管制官は、93便の点をレーダーで追い続けた。

**c814** 🔧 ／ 図 模式 機内の座席（後ろの席と座席の背の電話＝人は描かない） ／ 国立公園局（`thirty-seven phone calls were placed from on board Flight 93`・`Thirty-five of these calls were made on the Airfones located on the back of the seats in the last nine rows of the plane`）
> 機内では、9時半ごろから、乗客と乗員が、地上へ電話をかけていた。
> 連邦の警察の役所、FBI によると、その数は37本。
> そのうち35本は、座席の背の電話からだった。

**c815** 🔧 ／ 図 模式 同じ（後ろの9列に印） ／ 国立公園局（`Unless noted, the calls were made on Airfones`・`used her cell phone to call`・`used a cell phone to dial 911 and was connected for 70 seconds`）
> Q: 空の上からだと、携帯電話は、つながらないって聞いたけど？
> 携帯電話からも、2本がつながっている。座席の背の電話は、後ろの9列にあった。

**c816** ／ 図 模式 地上の側（家族・航空会社・当局の3つの箱） ／ 委員会報告 p13（`During at least five of the passengers' phone calls, information was shared about the attacks that had occurred earlier that morning at the World Trade Center`）
> 少なくとも5本の電話で、世界貿易センターのことが伝えられた。
> 乗客たちは、地上で何が起きているのかを、知った。

**c817** ／ 図 模式 機内の座席（話し合いの印） ／ 委員会報告 p13（`Five calls described the intent of passengers and surviving crew members to revolt against the hijackers`・`According to one call, they voted on whether to rush the terrorists in an attempt to retake the plane`）
> Q: それで、乗客たちは、どうしたの？
> 5本の電話が、乗客と乗員が反撃するつもりだと伝えている。
> 1本の電話によると、乗客たちは、犯人に向かうかどうか、決をとった。

**c818** ／ 図 模式 同じ ／ 委員会報告 p13（`They decided, and acted`）
> 委員会の言葉では、「彼らは決め、そして動いた」。

**c819** 🔧 ／ 図 模式 時間の帯（9:57 反撃） ／ 委員会報告 p13（`At 9:57, the passenger assault began`・`Several passengers had terminated phone calls with loved ones in order to join the revolt`）
> 9時57分、乗客たちの反撃が始まった。
> 何人かは、大切な人との電話を切って、そこに加わった。

**c820** ／ 図 模式 機の向き（左右に傾く記号＝人は描かない） ／ 委員会報告 p13（`immediately began to roll the airplane to the left and right, attempting to knock the passengers off balance`・`But the assault was sustained`）
> 操縦していた犯人は、乗客の体勢を崩そうと、機を左右に大きく傾けた。
> それでも、反撃は続いた。

**c821** ／ 図 模式 操縦室の扉（扉の内と外＝人は描かない） ／ 委員会報告 p13（`told another hijacker in the cockpit to block the door`）
> 9時58分57秒、操縦していた犯人は、操縦室のもう1人に、扉をふさげ、と言った。

**c822** ／ 図 模式 同じ扉（扉の外からの音の波） ／ 委員会報告 p13（`The cockpit voice recorder captured the sounds of the passenger assault muffled by the intervening cockpit door`）
> Q: 機内のようすは、どうして分かるの？
> 操縦室の音声の記録装置に、扉の向こうの、乗客たちの反撃の音が、
> こもった音で残っている。

**c823** ／ 図 模式 操縦室の音声の時刻の帯（10:00:25・10:00:42＝字幕だけ・画面に大きく出さない） ／ CVR p7（`In the cockpit. If we don't, we'll die.`）・委員会報告 p14（`a passenger in the background said`）
> その録音には、乗客の声も入っている。
> 10時0分25秒。「操縦室へ。やらなければ、死ぬ」

**c824** 🔧 ／ 図 模式 同じ帯 ／ CVR p7（`Roll it.`）・委員会報告 p14（`Sixteen seconds later, a passenger yelled, "Roll it!"`）
> 10時0分42秒には、「転がせ」と叫ぶ声。英語で「Roll it」だ。

**c825** ／ 図 模式 機の向き（傾きが止まる記号） ／ 委員会報告 p14（`stopped the violent maneuvers at about 10:01:00`）
> 10時1分ごろ、犯人は、機を大きく揺さぶるのを、やめた。

**c826** ／ 図 模式 同じ帯（10:02 前後） ／ 委員会報告 p14（`The hijackers remained at the controls but must have judged that the passengers were only seconds from overcoming them`・`The airplane headed down`）
> 犯人たちは、操縦を握ったまま、乗客に押さえ込まれる寸前だ、と判断したとみられる。
> 機は、下へ向かった。

**c827** ／ 実写 shanksville_day（ペンシルベニア州シャンクスビルの93便の追悼の場・2015年・F・全画面・来訪者は顔だけモザイク・ゆっくり引く＝副題「現在の93便の墜落現場（追悼の場）」） ／ 委員会報告 p30（`United 93 crashed in Pennsylvania at 10:03:11, 125 miles from Washington, D.C.`）・p14（`about 20 minutes' flying time from Washington, D.C.`）
> 10時3分11秒。93便は、ペンシルベニア州シャンクスビルの野原に墜ちた。
> ワシントンまで約200キロ（125マイル）。飛んで約20分の所だった。

**c828** ／ 実写 93便の追悼の場（別の点・後年・全画面・右へ流す＝副題「現在の93便の墜落現場（追悼の場）」） ／ 記念館（`40 people were killed on Flight 93`）
> 乗っていた40人が、亡くなった。この数に、乗っ取った4人は入っていない。

**c829** ／ 実写 93便の追悼の場（別の点・後年・名前の壁は写さない＝副題「現在の93便の追悼の場」） ／ 委員会報告 p14（`symbols of the American Republic, the Capitol or the White House`）
> 乗っ取りから墜落まで、35分。
> 委員会は、犯人の狙いは、連邦議会の議事堂か、ホワイトハウスだった、とみている。

**c830** 🔧 ／ 図 模式 時間の帯（9:28 から 10:03 まで＝35分） ／ 委員会報告 p14（`He was defeated by the alerted, unarmed passengers of United 93`）
> そして、こう書いている。
> 犯人は、事態を知らされた、武器を持たない乗客たちに、敗れた。

**c831** ／ 図 模式 同じ帯 ／ —
> Q: 乗客たちが、操縦室に入って、機を取り戻したの？
> そこまでは書かれていない。委員会が書いているのは、
> 犯人が操縦を握ったまま、機を下へ向けた、ということだ。

**c832** 🔧 ／ 図 模式 操縦室の音声の時刻の帯（「Let's roll」の札に「電話の向こうで聞かれた言葉」） ／ AP（`Let's roll`・`leaving the line open. It was then that the operator heard his words`）
> Q: 「レッツ・ロール」っていう言葉、聞いたことがあるよ。
> その言葉は、事件の6日後の新聞に、AP 通信の記事として載っている。
> 電話をかけていた乗客がそう言うのを、電話会社の係員が聞いた、と伝えられた。

**c833** 🔧 ／ 図 模式 同じ帯 ／ CVR p7（`Roll it.`）
> 操縦室の録音の書き起こしにあるのは、「Roll it」のほうだ。

**c834** 🔧 ／ 図 模式 同じ帯 ／ 委員会報告 p45（`We are sure that the nation owes a debt to the passengers of United 93`・`Their actions saved the lives of countless others, and may have saved either the Capitol or the White House from destruction`）
> 委員会は、こうも書いている。国は、93便の乗客たちに恩がある。
> 彼らの行動は、数えきれない命を救った。議事堂か、ホワイトハウスを、
> 壊されることから救ったかもしれない、と。

**c835** 🔧 ／ 図 模式 4機の行き先の地図（3つの印と、野原の印） ／ —
> Q: 狙われた建物には、届かなかったんだね。
> そう。4機のうち、狙った建物に届かなかったのは、93便だけだ。

---

### 第8章　届かなかった命令（21カット）

**c901** 🔧 ／ 図 模式 時間の帯（93便＝10:03:11 墜落・10:07 NEADS が知る） ／ 委員会報告 p30（`NEADS first received a call about United 93 from the military liaison at Cleveland Center at 10:07`）
> Q: NEADS は、最後の便のことを、いつ知ったの？
> NEADS に、93便の最初の知らせが入ったのは、10時7分。
> クリーブランドの管制センターにいる、軍の連絡係からだった。

**c902** 🔧 ／ 図 模式 同じ帯（10:15 墜落の報せ） ／ 委員会報告 p30（`NEADS was never able to locate United 93 on radar because it was already in the ground`）・p31（`The time of notification of the crash of United 93 was 10:15`）
> 93便は、その約4分前に、もう墜ちていた。
> NEADS は、レーダーで93便を見つけられなかった。もう地上にあったからだ。
> 墜落の知らせが届いたのは、10時15分だった。

**c903** 🔧 ／ 図 模式 同じ帯（「撃墜」の札に×） ／ 委員会報告 p31（`The NEADS air defenders never located the flight or followed it on their radar scopes. The flight had already crashed by the time they learned it was hijacked`）
> Q: 軍が、あの便を撃ち落とした、っていう話も聞いたけど？
> 委員会の答えは、こうだ。NEADS は93便を、一度もレーダーで捉えていない。
> 乗っ取りを知ったときには、もう墜ちていた。

**c904** 🔧 ／ 実写 PEOC の写真（ホワイトハウスの地下の危機管理室の副大統領と政府の人たち・NARA・A・撮影の日時は NARA の目録で確かめるまで言わない・全画面・ゆっくり寄る＝副題「ホワイトハウスの地下の危機管理室」（日付は NARA の目録で確かめてから足す）） ／ 委員会報告 p40（`the Vice President arrived in the room shortly before 10:00, perhaps at 9:58`）
> では、撃墜の許可は、いつ、どこで出たのか。
> チェイニー副大統領は、10時の少し前、ホワイトハウスの地下の危機管理室に入った。

**c905** 🔧 ／ 実写 PEOC の写真（別の点・同じ断り＝副題「ホワイトハウスの地下の危機管理室」（日付は NARA の目録で確かめてから足す）） ／ 委員会報告 p41（`At some time between 10:10 and 10:15, a military aide told the Vice President and others that the aircraft was 80 miles out`・`The Vice President authorized fighter aircraft to engage the inbound plane`）
> 10時10分から15分のあいだ、軍の補佐官が告げた。
> 機が、約130キロ（80マイル）先にいる。
> 副大統領は、戦闘機がその機と交戦することを、許した。

**c906** 🔧 ／ 実写 PEOC の写真（別の点・同じ断り＝副題「ホワイトハウスの地下の危機管理室」（日付は NARA の目録で確かめてから足す）） ／ 委員会報告 p41（`quick and decisive`）
> 副大統領の首席補佐官は、その判断は素早く、きっぱりしていた、と話している。

**c907** 🔧 ／ 図 模式 ワシントンへ伸びる予測の点線（実際の93便はペンシルベニアで止まっている） ／ 委員会報告 p41（`The FAA may have been tracking the progress of United 93 on a display that showed its projected path to Washington, not its actual radar return`・`the Secret Service was relying on projections and was not aware the plane was already down in Pennsylvania`）
> けれど、93便は、もう墜ちている。大統領を守るシークレットサービスは、
> 首都へ向かう、という予測を頼りにしていて、墜ちたことを知らなかった。

**c908** 🔧 ／ 実写 fighter_dc（首都の上空を警戒する F-16C・2001年10月7日・ニュージャージー州兵＝首都の部隊ではない・A・全画面・右へ流す＝副題「上空を警戒する F-16（2001年10月・ニュージャージー州兵）」） ／ 委員会報告 p31（`he explicitly instructed the Langley fighters`）・p45（`At 10:10, the pilots over Washington were emphatically told, "negative clearance to shoot."`）
> Q: 首都の上の戦闘機には、どんな指示が届いていたの？
> 同じころ、首都の上を飛ぶラングレーの戦闘機には、はっきりした指示が届いていた。
> 「撃つ許可は、出ていない」

**c909** 🔧 ／ 図 模式 NORAD の連絡の箱（副大統領から NORAD、NEADS、戦闘機へ） ／ 委員会報告 p42（`Vice president has cleared to us to intercept tracks of interest and shoot them down if they do not respond`・`NEADS personnel first learned of the shootdown order from this message`）
> 撃墜の許可が NEADS に届いたのは、10時31分。
> NORAD の文字の連絡で「副大統領が、応じない機の撃墜を許した」と流れた。

**c910** 🔧 ／ 図 模式 同じ箱（NEADS から戦闘機への矢印に×） ／ 委員会報告 p43（`The NEADS commander told us he did not pass along the order because he was unaware of its ramifications`・`they did not pass the order to the fighters circling Washington and New York because they were unsure how the pilots would, or should, proceed with this guidance`）
> けれど、NEADS の指揮官は、この命令を下へ流さなかった。
> その命令が何を引き起こすのか、分からなかったからだ、と委員会に話している。
> 現場の将校2人も、操縦士がどう動くべきか分からず伝えなかった、と述べた。

**c911** ／ 図 模式 同じ箱（首都の側の「撃ち落とせ」の札と、操縦士の側の「種類と尾翼の番号を確かめよ」の札） ／ 委員会報告 p43（`while leaders in Washington believed that the fighters above them had been instructed to "take out" hostile aircraft, the only orders actually conveyed to the pilots were to "ID type and tail."`）
> 首都の指導者たちは、上を飛ぶ戦闘機に、撃ち落とせと命じてある、と思っていた。
> 実際に操縦士に届いた命令は、機の種類と尾翼の番号を確かめよ、だけだった。

**c912** 🔧 ／ 図 模式 同じ箱 ／ —
> Q: 上の人たちと空の上とで、命令の中身が、食い違っていたってこと？
> そう。委員会は、その食い違いを、記録でたどっている。

**c913** 🔧 ／ 実写 当日の夜の大統領と副大統領（ホワイトハウスの写真係・A・全画面・ゆっくり引く＝副題「当日の夜のホワイトハウス」） ／ 委員会報告 p44（`The Vice President was mistaken in his belief that shootdown authorization had been passed to the pilots flying at NORAD's direction`）
> Q: 副大統領は、届いていないことを、知っていたの？
> 副大統領は、NORAD の指揮で飛ぶ操縦士に、命令が伝わっている、と思っていた。
> 委員会は、それは思い違いだった、と書いている。

**c914** 🔧 ／ 実写 大統領専用機の機内の大統領（電話の写っていない点）（別の点・ホワイトハウスの写真係・A・撮影の時刻は書かない＝副題「当日、大統領専用機の機内」） ／ 委員会報告 p40（`The Vice President stated that he called the President to discuss the rules of engagement`・`The President said he remembered such a conversation`）・p41（`He told us he based this authorization on his earlier conversation with the President`）
> 副大統領は、許可を出す前に、大統領と電話で話した、と言っている。
> その話をもとに、許可を出した、と。大統領も、そうした話を覚えている、と言う。

**c915** ／ 図 模式 同じ（電話の線に「記録なし」の札） ／ 委員会報告 p41（`there is no documentary evidence for this call, but the relevant sources are incomplete`）
> けれど委員会は、その電話の記録を、見つけられなかった。
> ただし、手がかりになる資料は不完全だ、とも断っている。

**c916** 🔧 ／ 図 模式 首都の上の2組の戦闘機（ラングレーと、アンドルーズの州兵） ／ 委員会報告 p44（`By 10:45 there was, however, another set of fighters circling Washington that had entirely different rules of engagement`・`launched out of Andrews Air Force Base in Maryland in response to information passed to them by the Secret Service`・`the decision to shoot rests in the cockpit`）
> 10時45分には、撃つかを操縦士が決めてよい、別の戦闘機も首都の上にいた。
> シークレットサービスの話を受けて、アンドルーズ基地から上がった州兵の機だ。

**c917** 🔧 ／ 図 模式 時間の帯（10:03:11 墜落・10:10 から 10:15 許可・10:31 NEADS へ） ／ —
> Q: つまり、許可が出たときには、あの便は、もう墜ちていたんだね？
> そう。許可も、それが NEADS に届いたのも、93便が墜ちたあとだった。

**c918** 🔧 ／ 図 模式 同じ帯 ／ 委員会報告 p45（`NORAD officials have maintained that they would have intercepted and shot down United 93. We are not so sure.`）
> NORAD の幹部は、93便に追いつき、撃ち落とせただろう、と言ってきた。
> 委員会の答えは短い。「我々には、そうは言い切れない」。

**c919** 🔧 ／ 図 模式 同じ帯（見つける・追う・命令を渡す、の3つの箱が空白） ／ 委員会報告 p45（`to locate the flight, receive authorization to shoot it down, and communicate the order to the pilots`・`did not know where United 93 was located, and did not have shootdown authorization`）
> 撃ち落とすには、まず93便を見つけて追い、操縦士に命令を渡す必要がある。
> その朝、そのどれも、できていなかった。

**c920** 🔧 ／ 実写 オファット空軍基地での会議（ホワイトハウスの写真係・当日の午後・A・全画面＝副題「当日の午後、ネブラスカ州の空軍基地」） ／ 委員会報告 p326（`Air Force One arrived at Offutt at 2:50 P.M.`・`At about 3:15, President Bush met with his principal advisers through a secure video teleconference`）
> 午後3時15分ごろ、大統領は、ネブラスカ州のオファット基地から、
> 画面越しに、政府の幹部と会議を開いている。

**c921** 🔧 ／ 図 模式 時間の帯（その朝の4機と命令の時刻をすべて重ねる） ／ —
> Q: こんな細かい時刻が、最初から分かっていたの？
> 実は、そうではない。事件のあと、先に世に出た説明は、
> 記録とは違っていた。

---

### 第9章　「9分」は、どう分かったか（20カット）

**ca01** 🔧 ／ 図 模式 委員会の調べの数（文書の山・話を聞いた人・国の数の札） ／ 委員会報告 p.xv（`Public Law 107-306, November 27, 2002`・`we have reviewed more than 2.5 million pages of documents and interviewed more than 1,200 individuals in ten countries`）
> 調べたのは、2002年11月に法律でつくられた、国の調査委員会だ。
> 250万頁を超える文書を読み、10の国で、1,200人を超える人から話を聞いた。

**ca02** ／ 図 RG237（FAA のレーダー再生の画面の収録・委員会が使った記録のひとつ） ／ 委員会報告 p457（`Times assigned to audio transmissions were derived by the Commission from files provided by the FAA and the Northeast Air Defense Sector (NEADS) based on audio time stamps`）
> 無線や電話の時刻は、FAA と NEADS が出した録音の記録に刻まれた時刻から、
> 委員会が割り出した。
> Q: 録音の時刻なら、確かそうだね。

**ca03** 🔧 ／ 図 模式 時間の帯（2003年5月の証言の3つの札） ／ 委員会報告 p34（`In public testimony before this Commission in May 2003, NORAD officials stated that at 9:16, NEADS received hijack notification of United 93 from the FAA`）
> 一方、委員会の報告より前に出た説明は、記録と違っていた。
> 2003年5月、委員会の公聴会で、NORAD の幹部は、こう証言した。
> 9時16分に、FAA から93便の乗っ取りの知らせを受けた、と。

**ca04** ／ 図 模式 同じ帯（9:16 の札に×・93便の乗っ取りは 9:28） ／ 委員会報告 p34（`This statement was incorrect. There was no hijack to report at 9:16. United 93 was proceeding normally at that time`）
> 委員会は、これを誤りとした。9時16分には、伝えるべき乗っ取りが無い。
> 93便は、そのとき、まだふつうに飛んでいた。

**ca05** 🔧 ／ 図 模式 同じ帯（9:24 の札に×） ／ 委員会報告 p34（`NORAD officials stated that at 9:24, NEADS received notification of the hijacking of American 77`・`NEADS never received notice that American 77 was hijacked`）
> 同じ証言で、9時24分に、77便の乗っ取りの知らせを受けた、とも言った。
> これも誤りだった。NEADS は、77便が乗っ取られたという知らせを受けていない。

**ca06** 🔧 ／ 図 模式 同じ帯（ラングレー機の線＝実は11便の誤報で飛んだ） ／ 委員会報告 p34（`The inaccurate accounts created the impression that the Langley scramble was a logical response to an actual hijacked aircraft`）
> そして、ラングレーの戦闘機は、77便か93便、またはその両方に備えた、という説明。
> 実際は、もう無い11便の、誤った知らせで飛んでいた。

**ca07** 🔧 ／ 図 模式 同じ帯（「14分」の札に×） ／ 委員会報告 p34（`Thus the military did not have 14 minutes to respond to American 77, as testimony to the Commission in May 2003 suggested`）
> Q: 先に出た説明は、どれも間違っていた、ってこと？
> そう。証言のとおりなら、軍には77便に備える時間が、14分あったことになる。
> 委員会は、あったのは長くても1分か2分だった、と書いている。

**ca08** 🔧 ／ 図 模式 同じ帯（「間に合ったように見えた」の札） ／ 委員会報告 p34（`More than the actual events, inaccurate government accounts of those events made it appear that the military was notified in time to respond to two of the hijackings`）
> 委員会は、こうまとめている。実際の出来事よりも、政府の誤った説明が、
> 軍は2機に間に合うよう知らされていた、と見せてしまった。

**ca09** 🔧 ／ 実写 当日のペンタゴン（米軍の写真・A・別の点＝副題は絵を見て書く） ／ 運輸省の監察総監の報告 CC-2006-085 p1（`did not investigate whether the inaccurate statements were knowingly false`・`referred to the Department of Defense (DOD) and Department of Transportation (DOT) Inspectors General`）
> Q: それって、わざと、ごまかしたの？
> 報告書は「誤り」と書いた。わざとかどうかまでは、委員会は調べていない。
> その問いは、役所の中を調べる、国防総省と運輸省の監察総監に引き継がれた。

**ca10** 🔧 ／ 図 模式 同じ帯（「誤り」の札から「監察総監」の札へ矢印） ／ 運輸省の監察総監の報告 CC-2006-085 p2（`We did not find evidence to conclude that FAA officials knowingly made false`）・p3（`consider appropriate administrative action for the two current executives who did not act to correct the record with the Commission`）
> 2006年、運輸省の監察総監は、FAA の職員が、
> わざと事実と違うことを言った証拠は見つからない、とした。
> ただ、委員会への答えの別の誤りを正さなかった幹部2人の処分を考えるよう、求めた。

**ca11** ／ 実写 当日の世界貿易センター（A・別の点＝副題は絵を見て書く） ／ 委員会報告 p7（`At 8:46:40`）・NIST NCSTAR 1 表6-1 印字 p84（`8:46:30`）・NCSTAR 1-6 表6-1 印字 p156（`8:46:26`）
> Q: ほかにも、記録が食い違っているところは、あるの？
> 1機目が北棟にぶつかった時刻も、資料によって3つある。
> 8時46分40秒、8時46分30秒、8時46分26秒だ。

**ca12** 🔧 ／ 図 模式 同じ3つの値の帯（どれも数秒の幅に並ぶ） ／ 委員会報告 p454 注39（`Flight Path Study`）・NTSB 11便（`impacted the North tower at approximately 8:46:40`）・NIST（`established from the time stamps in the September 11 telecasts`）
> 委員会の時刻は、国の事故調査の役所 NTSB が、飛んだ道を調べた報告による。
> 一方、建物を調べた国の研究機関 NIST は、
> テレビの放送の時刻表示を手がかりに、写真と映像の時刻をそろえている。

**ca13** ／ 図 模式 記録装置の表（4機それぞれの、操縦室の音声と飛行の記録） ／ 委員会報告 p456（`The CVRs and FDRs from American 11 and United 175 were not found, and the CVR from American Flight 77 was badly burned and not recoverable`）・p12（`The flight data recorder (also recovered)`）・NTSB 77便 図2（`FDR Pressure Altitude`＝sources §11-1 #4）
> 機体の記録装置で、中身が読めたのは、93便の2つと、77便の飛行の記録装置。
> 11便と175便のものは見つからず、77便の音声の記録装置は、ひどく焼けていた。

**ca14** 🔧 ／ 図 模式 同じ表（93便の音声の記録装置に印） ／ 委員会報告 p456（`United 93's cockpit voice recorder recorded the last 31 minutes of sounds from the cockpit`・`A transcript of the CVR recording was prepared by the NTSB and the FBI`）
> 93便の音声の記録装置は、操縦室の最後の31分の音を録っていた。
> その書き起こしは、NTSB と、FBI が作った。

**ca15** 🔧 ／ 図 模式 同じ表 ／ 委員会報告 p462（`Commission analysis of FDR, CVR, radar, and impact data`）・sources §5（P200056T＝93便の CVR の逐語・裁判の証拠として公開）
> Q: 記録が全部燃えて、隠された、なんて話も聞いたけど？
> 全部ではない。読めた記録は、
> 委員会の報告書に使われ、93便の音声は、裁判の証拠として書き起こしも出た。

**ca16** ／ 図 模式 時間の帯（9:21 の誤報の札＝出どころ不明） ／ 委員会報告 p26（`We have been unable to identify the source of this mistaken FAA information`）
> それでも、分からないことは残った。
> 11便がまだ飛んでいる、というあの誤報の出どころは、委員会も突き止められなかった。

**ca17** ／ 図 模式 同じ帯 ／ —
> Q: 分からないことも、そのまま書いてあるんだね？
> そう。分からないことは分からないと書き、そのうえで、それまでの説明を書き改めた。

**ca18** ／ 図 p34（文字の頁・2003年の証言の誤りを書いた段落を寄る） ／ 委員会報告 p34（`This statement was incorrect`）
> 委員会報告のこの頁が、軍に届いた知らせの時刻を、記録で正した所だ。

**ca19** ／ 図 模式 時間の帯（4機と、軍に届いた知らせの印をすべて重ねる） ／ 委員会報告 p31（`the NEADS air defenders had nine minutes' notice on the first hijacked plane, no advance notice on the second, no advance notice on the third, and no advance notice on the fourth`）
> 1機目は9分前。残る3機は、前もっての知らせが無かった。
> 冒頭の「9分」は、こうして記録から確かめられた数字だ。

**ca20** ／ 図 模式 同じ帯（11月の法律の札へつながる） ／ —
> では、あの朝のあと、アメリカの空は、どう変わったのか。

---

### 第10章　その後の空（19カット）

**cb01** ／ 実写 当日の夜の演説（NARA 6171390・WHCA・A・720×486＝全画面・大統領だけ＝副題「当日の夜、ホワイトハウスでの演説」） ／ 委員会報告 p326（`At 8:30 that evening, President Bush addressed the nation from the White House`）
> その日の夜8時30分。ブッシュ大統領は、ホワイトハウスから国民に向けて話した。
> Q: 空は、いつ、また開いたの？

**cb02** ／ 図 模式 全米の地図（9月13日・空港の点が戻り始める） ／ 委員会報告 p327（`On the morning of September 13, the national airspace reopened for use by airports that met newly improvised security standards`）・p556（`effective 11:00 A.M. on September 13, 2001`）
> 2日後の9月13日、午前11時。急いで決めた新しい保安の基準を満たした空港から、
> アメリカの空が、ふたたび開いた。

**cb03** ／ 実写 WHTV 600 ペンタゴンを訪れる大統領（9月12日・WHCA・A・SD＝全画面＝副題「9月12日のペンタゴン」） ／ materials.md §1-2（WHTV 600＝9/12 のペンタゴン視察・未編集 30:29＝目録の説明。中身の秒は映像方針で）・委員会報告 p559 注61（`On the evening of September 12, the President was at the Pentagon`）
> その前の12日、大統領は、ペンタゴンの現場を訪れている。

**cb04** ／ 実写 WHTV 609 世界貿易センターの跡を訪れる大統領（9月14日・WHCA・A・消防と救助の人の顔＝職務・全画面＝副題「9月14日の世界貿易センターの跡」） ／ materials.md §1-2（WHTV 609・610／NARA 6171391＝9/14 の大統領と消防・警察・救助＝目録の説明。中身の秒は映像方針で）
> 14日には、ニューヨークの、世界貿易センターの跡を訪れた。

**cb05** ／ 図 模式 年表（2001年11月の法律の印） ／ 委員会報告 p391（`In November 2001, Congress passed and the President signed the Aviation and Transportation Security Act. This act created the Transportation Security Administration (TSA)`）・法律（`November 19, 2001`）
> 2001年11月、空の保安についての法律ができた。
> この法律で、空の保安を受け持つ国の役所、運輸保安庁がつくられた。

**cb06** ／ イメージ 現在の空港の保安検査（後年・フリー素材＝副題「イメージ（現在の空港）」） ／ 法律（`the screening shall take place before boarding and shall be carried out by a Federal Government employee`・`except as otherwise provided in section 44919 or 44920`）・委員会報告 p2（`under a contract with American Airlines`）・p3（`had contracted out the work`）
> Q: 保安検査も、変わったの？
> 法律は、保安検査を、原則として国の職員が行うと定めた。
> それまで受け持っていたのは、航空会社が雇った警備の会社だった。

**cb07** ／ 図 模式 年表（2001年11月の法律から1年の帯） ／ 法律（`Not later than 1 year after the date of enactment of this Act, the Under Secretary of Transportation for Security shall deploy at all airports in the United States where screening is required`）
> 法律は、1年のうちに、検査をする国の職員を、
> 検査が必要なすべての空港に置くよう、求めていた。

**cb08** ／ イメージ 現在の旅客機の操縦室の扉（後年・フリー素材＝副題「イメージ」） ／ 法律（`requiring the strengthening of the flight deck door and locks`・`to ensure that the door cannot be forced open from the passenger compartment`）
> 操縦室の扉と鍵を、強くすることも、この法律が求めた。
> 客室の側から、無理に開けられない扉にすること、とある。

**cb09** 🔧 ／ 図 模式 操縦室の扉（当時＝閉めて鍵の決まり・守られないこともあった→強い扉） ／ 法律（`requiring that such flight deck doors remain locked while any such aircraft is in flight`）・委員会報告 p85（`required air crews to keep the cockpit door closed and locked in flight`・`This requirement was not always observed or vigorously enforced`）
> さらに、飛んでいるあいだは、扉に鍵をかけたままにすること。
> 事件の前にも同じ決まりはあったが、いつも守られてはいなかった。

**cb10** 🔧 ／ 図 模式 同じ ／ 委員会報告 p85（`even a hardened cockpit door would have made little difference in a hijacking`）
> Q: 扉を強くするだけでは、足りないってこと？
> そう。委員会は、犯人に従うやり方のままなら、扉が丈夫でも、
> ほとんど違いは無かっただろう、と書いている。

**cb11** ／ 図 模式 年表（2002年11月の法律・国土安全保障省の印） ／ 委員会報告 p391（`which is now part of the Homeland Security Department`・`In November 2002, both the Homeland Security Act and the Maritime Transportation Security Act followed`）
> 2002年11月には、国の守りをまとめる、国土安全保障省をつくる法律もできた。
> 報告書が出たころには、運輸保安庁も、その一部になっていた。

**cb12** 🔧 ／ 図 模式 年表（2002年11月 委員会・2004年7月 報告） ／ 委員会報告 p.xv（`the Congress and the President created the National Commission on Terrorist Attacks Upon the United States`・`we held 19 days of hearings`）
> 同じ2002年11月、議会と大統領は、この事件を調べる委員会をつくった。
> 委員会は、のべ19日の公聴会を開き、2004年7月に報告書を出した。
> この動画が主に使っている資料だ。

**cb13** ／ 図 模式 委員会の勧告の箱（乗ってはいけない人の名簿・爆発物の検査） ／ 委員会報告 p393（`Improved use of "no-fly" and "automatic selectee" lists should not be delayed`）
> 委員会は、報告書の終わりで、空の保安について、いくつも勧告を出した。
> たとえば、乗ってはいけない人の名簿を、もっと生かすこと。

**cb14** 🔧 ／ 図 模式 同じ箱（爆発物の検査に印） ／ 委員会報告 p393（`The TSA and the Congress must give priority attention to improving the ability of screening checkpoints to detect explosives on passengers`）
> そして、検査の場で、乗客が身に着けた爆発物を見つける力を、
> 優先して高めること。

**cb15** 🔧 ／ 実写 WHTV 610 世界貿易センターの跡（9月14日・WHCA・NARA 6171391・A・消防と救助の人の顔＝職務・全画面＝副題「9月14日の世界貿易センターの跡」） ／ —
> Q: ずいぶん、いろいろ変わったんだね。
> 一方、建物がなぜ崩れたのかは、NIST が、別に調べた。
> 建物の側は、この動画では扱わない。

**cb16** ／ 図 模式 2つの調べの箱（委員会＝空の側／NIST＝建物の側） ／ NIST（`Final Report on the Collapse of the World Trade Center Towers`）
> この動画で追ったのは、空の側の記録だ。
> 管制と軍が、その朝、何を知り、何を知らなかったのか。

**cb17** 🔧 ／ 実写 pentagon_court_pre（ペンタゴンの中庭・2025年7月・A・全画面・ゆっくり寄る＝副題「ペンタゴンの中庭（2025年）」。中庭に無人機の展示が写る＝映像方針で原寸を見て、締めに合わなければ別の点） ／ —
> これは、2023年のペンタゴンだ。

**cb18** ／ 実写 93便の追悼の場（別の点・後年・全画面＝副題「現在の93便の追悼の場」） ／ 国立公園局（`Flight 93 National Memorial`）
> そして、93便が墜ちた野原は、いま、追悼の場になっている。
> 国の記念の場所として、国立公園局が受け持っている。

**cb19** 🔧 ／ 図 模式 時間の帯（あの朝の4機） ／ —
> Q: 最後は、何を見ていくの？
> 最後に、委員会が、あの朝の人たちについて書いたことを見ておく。

---

### 終章　あの朝、持ち場にいた人たち（10カット）

**cc01** 🔧 ／ 実写 当日のペンタゴン（米軍の写真・A・救助にあたる隊員・別の点＝副題は「当日のペンタゴンの救助」のように写っている人を書き、語りの NEADS・FAA の人と取り違えさせない。合わなければ人の写らない点か図） ／ 委員会報告 p31（`We do not believe that the true picture of that morning reflects discredit on the operational personnel at NEADS or FAA facilities`）
> 委員会は、こう考えている。あの朝の本当の姿は、
> NEADS や FAA の現場の人たちの落ち度を、示すものではない。

**cc02** 🔧 ／ 実写 当日のペンタゴン（米軍の写真・A・別の点＝副題は絵を見て書く） ／ 委員会報告 p31（`NEADS commanders and officers actively sought out information, and made the best judgments they could on the basis of what they knew`）
> NEADS の指揮官や将校たちは、自分から情報を探し、
> 知っていることをもとに、できるかぎりの判断をした。

**cc03** ／ 実写 当日の世界貿易センター（A・別の点・消防の人の顔＝職務＝副題は絵を見て書く） ／ 委員会報告 p311（`The FDNY suffered 343 fatalities`・`the largest loss of life of any emergency response agency in history`・`The PAPD suffered 37 fatalities`・`The NYPD suffered 23 fatalities`）
> あの朝、持ち場にいたのは、空の人たちだけではない。
> ニューヨークの消防は343人、港湾公社の警察は37人、市の警察は23人を失った。
> 消防の343人は、救急や消防の組織が失った命として、歴史上いちばん多い。

**cc04** 🔧 ／ 図 模式 時間の帯（4機と、軍に届いた知らせの印） ／ 委員会報告 p45（`NORAD and the FAA were unprepared for the type of attacks launched against the United States on September 11, 2001`・`an unprecedented challenge they had never before encountered and had never trained to meet`）
> 委員会は、NORAD も FAA も、あの形の攻撃への備えが無かった、と書く。
> 経験も訓練も無い事態に、その場で、国の守りを組み立てようとした。
> Q: その場で、組み立てようとしたんだね。

**cc05** ／ 実写 DVIDS 122342（別の窓・隊員と消防＝副題「当日のペンタゴン」） ／ 委員会報告 p31（`the NEADS air defenders had nine minutes' notice on the first hijacked plane`）
> 軍の当直に、前もって知らせが届いたのは、1機目の9分前だけ。
> 残る3機は、前もっての知らせが無かった。それが、記録の示した、あの朝の姿だ。

**cc06** ／ 実写 議会図書館 LC-B20（車内から見た通りと煙の柱・C'＝米議会図書館蔵（撮影者不詳）・遠くの人は顔の分からない遠景だけ・全画面＝副題「当日のマンハッタン」） ／ 記念館（`The attacks killed 2,977 people from 90 nations: 2,753 people were killed in New York; 184 people were killed at the Pentagon; and 40 people were killed on Flight 93`）
> いま数えられている犠牲者は、2,977人。
> ニューヨークで2,753人、ペンタゴンで184人、93便で40人だ。

**cc07** ／ 図 模式 数の帯（2,973＝2004年7月の委員会・2,977＝いまの数） ／ 委員会報告 p311（`the nation suffered the largest loss of life—2,973—on its soil as a result of hostile attack in its history`）
> 委員会は、2004年7月の時点で、2,973人と数えていた。
> いまの数とは、4人違う。

**cc08** 🔧 ／ 図 模式 同じ帯（2026年8月の札） ／ 検視局（`announced the identification of a previously unknown victim of the September 11, 2001 terror attacks on the World Trade Center using the breakthrough technique of forensic investigative genetic genealogy`）
> そして事件から25年目の2026年8月にも、ニューヨーク市の検視局が、
> 身元の分からなかった犠牲者の1人を、新しい調べ方で確かめた、と発表した。

**cc09** ／ 図 模式 委員会報告の表紙の絵と「米政府の印刷局のサイト」の札 ／ sources §1（govinfo の PDF＝200・md5 が手元と同じ・2026-10-11。⑥の時点でもう一度開く）
> この報告書は、いまも、アメリカ政府の印刷局のサイトで、誰でも読むことができる。

**cc10** 🔧 ／ 実写 DVIDS 122347「Noble Eagle, Sep 14」空撮（別の窓・PD・SD＝全画面・ゆっくり引く＝副題「9月14日のペンタゴン（空撮）」） ／ —
> 飛行機に乗る前の保安検査で、印象に残っていることはありますか。
> よければ、コメントで教えてください。

## 5. 使わなかったもの（理由）

| 物 | 理由 |
|---|---|
| 「着陸した機は3,500」（運輸長官の証言とされる数） | ④で証言の写し（`src/new/hearing2/transcript_0523.txt`）を探して「3,500」0件＝出どころを確かめられない。委員会の約4,500だけ |
| 乗っ取った側の言葉（93便の CVR の「Allah …」「Pull it down」ほか）・名前 | 10-11 の決め（名前を出さない）・名前の入る行が多い。乗っ取った側の行動は委員会の地の文（p13〜p14）で語った |
| 乗員・乗客・電話の相手の名前（委員会報告の本文にある客室乗務員2人・機長の返信の署名ほか） | repo に書かない（kousei §8）。役割で語れる（§1-4） |
| 「Let's roll」を言った乗客の名前・係員の後年の話 | 私人・二次（sources §11-3） |
| 副大統領の2回目の許可（10:12〜10:18 ごろ） | 1回目と同じく墜落の後＝話が重くなるだけ |
| 大統領の教室の「7分」 | 政治の評価に使われる話（legend #18）。c518 は耳打ちの言葉だけ |
| PEOC の写真の「10:10 の場面」 | 撮影の日時が未確認（materials §7・②）＝副題に日付を書かない（NARA の目録で確かめてから足す＝c904〜c906） |
| 「最大の失敗は想像力の失敗」（第11章）・「想像力の失敗」 | ④'で文字の層を行末のハイフンも揃えて引き直した＝委員会自身の地の文には無い。p336 に、ある人の見方として `failure of imagination` があるだけ（p339 は `four kinds of failures`）＝使わない |
| 乗員の手引き・NORAD の態勢の事件後の変化 | 一次資料に当てていない（kousei §11-4）＝cb は法律 107-71 の本文と委員会の勧告（p393）だけ |
| 第7ビル・塔の崩壊の仕組み・自由落下・溶けた鉄骨・インサイダー取引 | 案A の範囲の外（cb15 の1行だけ）。爆破説は名指ししない |
| 委員会の公聴会の写真（`hearing`） | 2012年の原子力規制委員会の公聴会＝別物（materials §3） |
| ペンタゴンの監視カメラの映像 | 衝突の瞬間（10-11 カズヤくん） |
| 国防総省の監察総監の報告（06-INTEL-12・2006-09-12＝NORAD の側） | ④'で一次の頁を取れなかった（取りに行くとファイルのダウンロードになる・media.defense.gov の 05-INTEL-13 は 403）＝ca10 は運輸省の監察総監（FAA の側）だけ。取れたら ca10 に1文足せる |
| Air Force Magazine（2006-09-07）＝二次 | 一次（CC-2006-085）を④'で取ったので使わない。⚠️ 報道の「幹部3人」は一次と食い違わない＝誤りを知った幹部は3人（いまいる2人と退職した1人・PDF p2）・処分を考えるよう求めたのはいまいる2人（PDF p3）。正さなかったのは NORAD の証言ではなく、FAA が委員会の書面の問いに答えた文の別の誤り（空軍の連絡係が電話会議に加わった時刻・PDF p2 の4.） |

## 6. 読み間違えやすい語（⑤a の前に確かめる）
- 英字：NEADS（ニーズ）・NORAD（ノーラッド）・FAA（エフエーエー）・NTSB（エヌティーエスビー）・FBI（エフビーアイ）・NIST（ニスト）・AP（エーピー）・F-15（エフじゅうご）・F-16（エフじゅうろく）・Roll it（ロール・イット）・Let's roll（レッツ・ロール）
- 便名・機種：11便（じゅういちびん）・175便（ひゃくななじゅうごびん）・77便（ななじゅうななびん）・93便（きゅうじゅうさんびん）・ボーイング767（ななろくなな）・757（ななごーなな）・9.11（きゅういちいち）
- 地名・施設：ハーンドン・ラングレー・オーティス・ケープコッド・アトランティックシティ・ロングアイランド・インディアナポリス・クリーブランド・ニューアーク・シャンクスビル・バークスデール・オファット・アンドルーズ・ローム・レーガン・ナショナル空港
- 漢字：刃渡り（はわたり）・寸前（すんぜん）・決をとった（けつをとった）・墜ちた（おちた）・札（ふだ）・頁（ページ）・要る（いる）・首席補佐官（しゅせきほさかん）・監察総監（かんさつそうかん）・検視局（けんしきょく）・追悼（ついとう）
- 🆕④'：北棟（きたとう）・南棟（みなみとう）＝北東（ほくとう）と同じ音にしない／空の（そらの＝「からの」にしない・c104・c216・c302 ほか）／開いた（ひらいた＝cb02「空が開いた」）／港湾公社（こうわんこうしゃ）／何機か（なんきか＝c409）／約4,500機（よんせんごひゃっき）。「報せ」は④'で語りから無くした（全部「知らせ」）
- 数：2,977人（にせんきゅうひゃくななじゅうななにん）・4万3,000リットル・1万1,400ガロン・10時0分25秒（じゅうじれいふん）・8時46分40秒・250万頁・1,200人

## 7. 素材との突き合わせ（映像方針へ）
- **写真・実写 64カット**（③の見込み 73＝31% から −9）。当日の写真が Commons にほぼ無い所（c3 手順・c4 管制と NEADS・c7 コマンドセンター・c8 93便の機内・ca 記録）は図（時間の帯・手順の段・地図・記録装置の表）と RG237 で受けた。増やすなら「当日の WTC（A・14点）」「当日のペンタゴン（A・約143点）」を、両棟が燃える時刻（9:03〜9:59）・衝突のあと（9:37:46〜）の語りに重ねる
- **1点ずつ確かめるもの**：DVIDS 122342・122343・122347 の秒（遺体・担架・負傷者の写らない窓）／議会図書館 LC-A05-A17 の時刻（塔が1本＋雲＝南棟の崩壊の後の見込み＝c102 は時刻を言わない）・LC-B20／NASA ISS003-E-5388／WHTV 1501・606・600・609・610（私人の近景は顔だけモザイク・音は使わない）／ホワイトハウスの写真係の写真（小学校の部屋のテレビ・大統領専用機の機内×2・バークスデール・オファット・夜の大統領と副大統領・PEOC×3）＝権利の札「?」28点の中＝1点ずつ／F-15 オーティス2点（VIRIN）・fighter_dc（副題で部隊を断る）／ペンタゴンの米軍の写真（DF-SD-02-09094・DN-SD-03-11447・pentagon_west_day ほか）＝1枚ずつ原寸／93便の追悼の場（shanksville_day ほか3点・来訪者は顔だけモザイク・名前の壁は写さない）／ニューアークの搭乗口の旗
- **イメージ（20%に数えない・画面に「イメージ」）**：b767_takeoff（c209）・security_pre（c210）・現在の保安検査（cb06）・現在の操縦室の扉（cb08）
- **「当日の世界貿易センター（A）」の7か所**（c514・c519・c609・c701・c706・ca11・cc03）は、語りの時刻に合う点を選ぶ（9:03 より前の語りに両棟が燃える写真を置かない＝c4 は事件の前の写真だけ・④'で c515〈8:51〜9:02 の語り〉は事件の前の写真に替えた）
- 🆕④'：c315・ca01 は図に（文字だけは ca18 の1つ）／大統領の電話の写真は専用機の語り c712 へ・長官の証言 c709 は図（語りと画の取り違え）／c623 と c624 の写真を入れ替え（夕方の写真は時刻を言わない c624 へ）／c914 は電話の写っていない機内の点／PEOC（c904〜c906）の副題に「当日」を書かない（NARA の目録で日時を確かめてから）／cb17 は中庭の無人機の展示が写る＝原寸で
- RG237（レーダー再生の画面の収録）は実写ではない＝冒頭に置かない・画の欄は「図 RG237」

## 8. 概要欄の用語（下書き）
- NORAD（ノーラッド）＝北アメリカの空を守る、アメリカとカナダの軍の司令部
- NEADS（ニーズ）＝NORAD のうち、アメリカ北東部の空を受け持つ部署（ニューヨーク州ローム）
- FAA＝連邦航空局。アメリカの空の交通と安全を受け持つ国の役所
- 航空路管制センター＝空の道を飛ぶ旅客機を、レーダーで見守る管制の拠点（ボストン・ニューヨーク・インディアナポリス・クリーブランドほか）
- コマンドセンター＝全米の空の流れを見渡す FAA の司令塔（バージニア州ハーンドン）
- トランスポンダ＝便名と高度を、地上のレーダーに知らせる機体の装置
- 操縦室の音声の記録装置（CVR）・飛行の記録装置（FDR）＝いわゆるブラックボックス
- NTSB＝アメリカの国家運輸安全委員会（事故を調べる国の役所）
- NIST＝アメリカの国立標準技術研究所（建物の崩壊を調べた国の研究機関）
- 運輸保安庁（TSA）＝2001年11月の法律でつくられた、空の保安を受け持つ国の役所
- 監察総監＝役所の中の仕事ぶりや不正を調べる職
- 9.11委員会＝2002年11月に法律でつくられた、事件を調べる国の調査委員会（報告書は2004年7月）

## 9. 換算と計算（式）
| カット | 画面・語り | 式 |
|---|---|---|
| c203 | 約4万3,000リットル（1万1,400ガロン） | 11,400 × 3.785 L ＝ 43,149 L |
| c212 | 刃渡り10センチ（4インチ） | 4 × 2.54 cm ＝ 10.16 cm |
| c313 | 約8キロ（5マイル） | 5 × 1.609 km ＝ 8.05 km |
| c401 | 約7,900メートル（2万6,000フィート） | 26,000 × 0.3048 m ＝ 7,925 m |
| c402 | 18秒後 | 8:13:47 − 8:13:29（NTSB 11便）。委員会 p4 は「Sixteen seconds after」＝割れる（語りは NTSB の時刻で計算・§1-5 にも行を足す） |
| c418 | 約246キロ（153マイル） | 153 × 1.609 km ＝ 246.2 km |
| c422 | 約410メートル（1,350フィート） | 1,350 × 0.3048 m ＝ 411.5 m（p278「about 1,350 feet」） |
| c423 | 9分 | 委員会の値（p21）。8:37:52 → 8:46:40 ＝ 8分48秒 |
| c612 | 30分以上前 | 8:46:40 → 9:21 ＝ 34分20秒 |
| c616 | 約10キロ（6マイル） | 6 × 1.609 km ＝ 9.66 km |
| c617 | 約8キロ（5マイル）・時計回りに330度 | 5 × 1.609 ＝ 8.05 km。右回り（NTSB「a right 330-degree descending turn」）＝上から見て時計回り |
| c618 | 約670メートル（2,200フィート） | 2,200 × 0.3048 m ＝ 670.6 m |
| c620 | 時速約850キロ（530マイル） | 530 × 1.609 ＝ 853 km/h |
| c622 | 184人・乗っ取った5人は入っていない | 記念館 184 ＝ 建物の中 125（p314）＋ 77便 64 − 5（p8 の乗客58＋乗員6・乗客に5人を含む） |
| c623 | 約240キロ（150マイル） | 150 × 1.609 ＝ 241 km |
| c705 | およそ4分後 | 9:37:46 → 9:42 ＝ 4分14秒 |
| c805 | 2分後 | 9:24 → 9:26（p11「Within two minutes, at 9:26」） |
| c806 | 約1万700メートル（3万5,000フィート）・約210メートル（700フィート） | 35,000 × 0.3048 ＝ 10,668 m・700 × 0.3048 ＝ 213 m |
| c824 | （差の秒は言わない＝④'） | 10:00:25 → 10:00:42 ＝ 17秒（P200056T p7）。委員会 p14 は 10:00:26 から16秒＝割れるので、語りは時刻だけ |
| c827 | 約200キロ（125マイル） | 125 × 1.609 ＝ 201 km |
| c828 | 40人・乗っ取った4人は入っていない | 記念館 40 ＝ 93便 44（乗客37＋乗員7・p10〜p11）− 4 |
| c829 | 35分 | 9:28 → 10:03:11 ＝ 35分11秒 |
| c902 | その約4分前 | 10:03:11 → 10:07 ＝ 3分49秒（10:07 の秒は書かれていない） |
| c905 | 約130キロ（80マイル） | 80 × 1.609 ＝ 128.7 km |
| c832 | 事件の6日後 | 2001-09-11 → 09-17 |
| cb02 | 2日後 | 09-11 → 09-13 |
| cc07 | 4人違う | 2,977 − 2,973 |
| cc08 | 25年目 | 2001-09-11 → 2026-08-24 ＝ 24年11か月13日（25年目） |
| c204〜c207 | 乗員 11・9・6・7人 | 操縦士2＋客室乗務員 9・7・4・5（p4・p7・p8・p10） |

## 10. 資料（頁の対応）
- 委員会報告（GPO 版・2004-07-22）＝**印字の頁**で書く（PDF＝印字＋18・前付けはローマ数字＝PDF の頁）。文字の層＝`src/core_raw/GPO-911REPORT.pages.jsonl`（sources §1）
- 図表 p32〜p33＝②の原寸の写し（sources §11-1 #9）／NTSB の飛行経路の研究4本（2002-02-19）＝②の原寸（§11-1 #1〜#5）／CVR の逐語 P200056T＝②の原寸（§11-1 #11）／NIST NCSTAR 1（2005-09）＝文字の層（OCR 並み）と②の原寸（#7・#8）
- スタッフ声明 No.17（2004-06-17）＝`src/core_raw/staff17.pages.jsonl`（PDF の頁）／運輸長官の証言（2003-05-23）＝`src/new/hearing2/transcript_0523.txt`
- 🆕④'で取った一次（2026-10-12・WebFetch）＝`src/new/web5/dot_oig_cc2006085.pdf`（運輸省の監察総監の報告 CC-2006-085・2006-08-31・30頁・md5 328b6ab593e67dc6207c7989c8196a69）と文字の層 `.txt`（頁は PDF の頁）
- ④で開いた写し（2026-10-11 22:01・UA に `@` なし）＝`src/new/web4/`：国立公園局「Phone Calls from Flight 93」・AP（Seattle Times の写し 2001-09-17）・Public Law 107-71（govinfo・2001-11-19）・検視局（2026-08-24）・記念館の FAQ（2,977）・Air Force Magazine の Daily Report（2006-09-07＝運輸省の監察総監代行の言葉）

## 11. 関連
- 設計図＝[kousei.md](kousei.md)／資料の台帳＝[sources.md](sources.md)／素材＝[materials.md](materials.md)／通説＝[legend_2026-10-11.md](legend_2026-10-11.md)／旧版の当て直し＝[claims_check_2026-10-11.md](claims_check_2026-10-11.md)／旧版の棚卸し＝[old_script_inventory.md](old_script_inventory.md)
- 数える道具＝`v1_build/m21.py`・`v1_build/roles21.py`（→ `roles.tsv`）・`v1_build/quotes21.py`（→ `quotes21_result.tsv`）
- 🆕④'の道具＝`v2_build/`（`pg21.py` 原文を引く・`decide21.py` 扱いの表・`gen_g0.py` G0 の直し・`ledger21.py` 台帳と差し替え表・`build21_v2.py` 組む・`quotes21v2.py` 引用の照合〈運輸省の監察総監の報告を足した〉・`final21.py` 門番をまとめて回す）
- 形の手本＝20本目 [../ep20/daihon_v2.md](../ep20/daihon_v2.md)
