# 33本目 グレンフェルタワー火災（2017-06-14・英国ロンドン・公開調査の報告は2019年と2024年に出た火災の回）台本 第2版

> **2026-11-12・33本目のチャット4＝④' 台本【チェックと修正】**で、第1版（`daihon_v1.md`・md5 `7eaadfced6af6dcdab244c7fe7919295`＝1文字も書き換えていない）に差し替え表 `v2_build/patches33.json` を当てて `v2_build/build33_v2.py` が組んだ。**手で直さない**（直すのは差し替え表＝`v2_build/gen33.py` が係の所見と ④' の決めから組む → `python -P -X utf8 ref/ep33/v2_build/final33.py` で組み直すと同じ字になる）。🔧＝画の欄か語り・聞き役の行が第1版と違うカット（出典の欄だけの直しには付けない）。
> 語りは「だ・である」（まりさ）。聞き役（れいむ）の行の印は `> Q: `（音にも字幕にも出さない）。役割（質問・まとめ・反応）は `v2_build/roles.tsv`（`v1_build/roles33.py` が第2版から組む）。**です・ます は最後の問いのカット（cc13）だけ**。決め所（★）の行は無い。
> 画の欄の頭の語・出典の欄の略・この回の線・言い切らない所は第1版の頭と同じ（下の §1-4〜§1-6 と第1版 `daihon_v1.md` の1〜9行）。④' で足した言い方＝「1時30分までに112人」（本文 P1V4 ¶28.14j に合わせた＝要約の表の「1時31分 110人」は使わない）・「この災害で72人」（72人目の死は火事が直接の原因ではない＝P1V1 ¶1.3）・英国の coroner は「検死官」・円は c604 の1回だけ語り、あとは画面の札。
> 数える道具＝`v1_build/m33.py`・`v1_build/roles33.py`・`v1_build/quotes33.py`（第1版と同じ）＋ ④' の `v2_build/`（`final33.py`＝組む→門番13種→対照表→消えた語・`gen33.py`＝差し替え表と扱いの上書きを組む・`ledger33.py`＝所見の台帳・`readable33.py`＝読みやすい版・`titles33.py`＝題の字数と型の網・`src33.py`＝原文を段落と語で引く・`cand33.py`＝Commons を番号で引く〈名前は網で伏せる〉・`split33.py`／`wfx33.py`＝係に渡す写しと結果の取り出し・`cut33.py`・`make_diff33.py`・`lost33.py`）。

## 0. 第2版の数と、④' でしたこと（2026-11-12・チャット4＝④'）

### 0-0. 門番（`v2_build/final33.py` → `v2_build/gates.md`・全部 exit 0・2回組んで同じ）
- カット **241**（欠番なし）・行 534・句読点なし 13,326字＋ed01 46＝**13,372字**（幅 13,120〜13,520 の内・目標 13,320 より +52）
- 尺＝① カット×9.05秒 36分21秒／② 句読点なし÷365 **36分38秒**／③ 章ごとの合計 36分38秒＝開き17秒。⚠️ `check_script` の尺の E（古い定数）は第1版と同じく信じない
- 冒頭＝実写だけ13カット・最初の聞き役 23.0秒・**引き（c105）の終わり 43.7秒**（46秒まで余り2.3秒）
- 聞き役＝67行（12.5%・1分1.83回・最長の空き67秒）・**質問40／まとめ15／反応12（60／22／18%）**＝第1版の質問64% を目安の60%の内へ（c111・c319・c520 を質問から反応とまとめへ・ca16 をまとめから反応へ）・まとめのあとの「そう。」15／15
- 写真・映像・紙面（実写）**114（47.3%）**＝紙面35・写真34・公的34・映像7・衛星4／イメージ25／図102（模式83）／文字だけの画面0
- 原文の片 **370**＝OK 366・OK(¶?) 4（P1V1 ¶1.3＝段落の札が文字の層に無い・片は在る）・**外れ 0**（`v2_build/quotes33_v2.tsv`）
- 名前の網＝2,204語×37ファイル（`git ls-files ref/ep33`＋`v2_build` の全部＋第2版）→ **0件**（第1版のときの3件＝道具のコードの関数名の中の字の並びの空鳴り＝その関数を使わない書き方に替えて消した。⚠️ 空鳴りの語をノートに書くと、そのノートが鳴る＝語は書かない）
- m33＝E 0・W 31（第1版と同じ数＝図の型「模式」の続き25・言わない語「最悪」〈c107＝報告の言い方〉・「まだ」〈c317・c505＝日付の要らない「まだ塔にいた」の型〉・言わない形〈cb01＝日付つき〉・文字の頁の続き〈ca07〉）
- `check_script_diff`＝🔧 112 と差分が一致・欠番 0

### 0-1. 第1版 §0-1（④' で見てほしい所）の11項目への答え
| # | 第1版の問い | 答え（④' でしたこと） |
|---|---|---|
| 1 | 質問64%・模式83・地の偏り | 質問 64%→**60%**（上の 0-0）。模式の続きと地の偏り（[35] 27・[24] 20・[72] 19 カット）は**映像方針**で替える（係の案＝c405 か c406 を P2V7 の実験の図か写真の全画面に・cc08〜cc10 の地を各章の代表の写真に・第8章の c905 か c910 を Commons の写真の全画面に） |
| 2 | c908（最期の話）を残すか | **承認①へ**（0-3 の3）。訳は原文どおり（範囲の限定・「みな」・findings）。通し読みの係は「外す」、照合の係は「残すなら言い換えは無理（限定を外すと原文より広い）」 |
| 3 | 罪名を入れるか | **承認①へ**（0-3 の4）。警1 の原文＝`They ask the CPS to consider charges including corporate manslaughter, gross negligence manslaughter, health and safety offences, fraud and fraud-related offences and misconduct in public office`＝including＝例示・どの容疑の対象にどの罪かは発表に無い |
| 4 | c101 の「4階」 | 語りを「1室の台所」・副題を「台所の窓のまわりの炎〈1:09〉」に（字は同じ・日付の二重も消えた）＝階の数が初めて出るのは断り（c204）のあとの c301 |
| 5 | 数の多いカット | c313（戻る時刻の1時13分を外した）・c427（168人の行）・c519（2時35分・8時7分を外す）・c612〜c614（円は c604 の1回だけ＝画面の札に残す）・cb05〜cb07（並びと言い方をそろえた）。c504 は残す（章の見取り図＝1:26→2:35→2:47） |
| 6 | 図と副題の時刻 | 第1段階の図は題の行が「Figure n.n」だけ＝時刻は図の前の本文の1文＝副題はその文とすべて合う（照合の係 G1・G2）。直した＝c311 の副題（1:15 は「燃えはじめ」でなく炎が部屋の上へ伸びた時＝¶22.27）・c413 の図を 11.7〈1:40〉から 13.1〈2:00 の冠の炎〉へ（語りは2時）＝⑤b で原寸。図10.6〜10.9 の並びと時刻の組は ⑤b で |
| 7 | c106「この火事で72人」 | 「この災害で、72人が亡くなった」（P1V1 ¶1.3＝72人目の死は火事が直接の原因ではない・警1 の72は tragedy が奪った命）。72人の内訳は c428 のまま |
| 8 | #15 の50秒を4つ | 短すぎない（使うカットは6〜10秒）。同じ副題の焼けた塔が4回＝⑤b で画角を見て、似ていれば3つに減らし c526 を写真に |
| 9 | 章の釣り合い | 第3章 −169・第2章 −95・第10章 −64・第1章 −62・第8章 −25／第5章 +101・第7章 +81・第9章 +78・第11章 +76・第6章 +56・第4章 +53（全体は幅の内）。第3章は字は少ないがカット最多（32）＝足さない |
| 10 | 第4章 38%・第8章 23% | 20%は満たす。第8章は実写が3つとも文字の頁＝映像方針で Commons の写真の全画面を1つ |
| 11 | 年次報告の「消防は第1段階の勧告をすべて実施」 | **入れない**＝年次報告の写し3つと進捗報告に語を変えて25通り当てて0件（消防の章の頁は文字の写しが無い）・進捗報告は第1段階の残り3をまだ追っている（§5 を直した） |

### 0-2. 所見の台帳（`v2_build/ledger33.md`＝`ledger33.py` が係の記録と差し替え表から組む・直す前の版＝git の外 `src/agents/wf33b/ledger33_pre.md`）
- 係＝照合 G1（冒頭〜第2章）・G2（第3〜4章）・G3（第5章）・G4（第6〜8章）・G5（第9〜11章と §）＋通し読み G6＝資料で割った6本（同時2本・反証の段なし）・別の目 R1・R2（直した所の当て直し）
- 所見 **241**＝照合と通し読み213（🔴3・⚠️69・・141）＋別の目28（🔴2・⚠️12・・14）＝直した177・済み20・直さない21・後の工程へ15・一部6・承認①へ2（未決0）
- 別の目の 🔴 の2件（④' 自身の直しが作った粗）＝c524（④' が採った直しで「定期の」が落ち、¶83.6 の no structured or regular … refresher training と逆に＝戻した）／cb01（cb06 と同じく頁を丸ごと額装すると罪名の列と幹部の名が写る＝頭の1文だけに）。⚠️ の多くは「語りを直したのに同じカットの画の札が古いまま」（c405・c514・c519・c523・c622・c626・c911・ca13・cb05）と、並べ替えの番号が § に届いていない所（§6・§7・§9）＝32本目の落とし穴と同じ型
- 🔴 の3件（④' が原文で引き直した）＝c204「住まいは4階から23階」は建てた時の設計（¶3.13 were designed to）＝改修で下の階に9戸（¶6.5）／c311 の副題「外壁が燃えはじめる〈1:15〉」＝¶22.27 は 01.15.36 に「かなりの勢いで燃えている」（移ったのは 1:09）／ca06 の画「報告の表紙を並べる」＝表紙に委員長と委員の名が刷られている（線）
- ⚠️ の主なもの（④' が原文で引き直した）＝c314（要約の表の 01.30 の通報は本文 ¶10.90 の 01.24.57 と合わない）・c316／c427（110人→本文の112人）・c317（「部屋で待て」の但し書き unless … directly affected）・c414（その夜のはしご→ロンドン消防のはしご＝隣の消防の42m のはしご車も来ていた ¶82.3）・c416（専門家の言葉の帰属）・c514（I have little doubt＝「まず間違いなく」）・c524（¶83.12 の範囲＝その夜の失敗）・c608（¶55.33 の時期＝2014年の話し合い）・c614（差を残す狙いは社員2人が「はっきりとは言わずに」認めたこと ¶55.59）・c615 の札（tend to suggest）・c617（残ったのは色と留め方だけ ¶55.71）・c623（We think）・c626（材料の助言 ¶67.14）・c705（exploit）・c707（わざとの策 ¶2.25）・c717（売り物でない品で試験・dishonestly ¶2.37）・c803（that warning＝人が亡くなる火事を待つな）・c810（業界の一部 ¶2.9）・c912（組織の運営と統率の欠け ¶2.91）・ca01（火事への対応そのもの ¶2.103）・ca12（外壁の燃える材料の禁止を足した 応 ¶23）・ca14（61＝58＋3 進）・cb13（政府への警告・外壁 ¶29.5）・cc11（失敗の主＝国と業界の組織 ¶2.4）
- ⚠️ 直さなかった主なもの＝c504（章の見取り図）・c513（2時4分前後は指揮者が2人＝受け身は許す）・c107 を反応に替える案（亡くなった人の場面に反応を置かない＝ルール 4-15）・c106 の「報告によれば」を外す案（「3時間足らず」は報告の言い方＝帰属を残す）

### 0-3. 承認①の表（いま → 変えたあと）＝🔴 カズヤくんに決めてもらう
| # | 決めること | いま（第2版） | 変えたあとの案 | ④' の推奨 |
|---|---|---|---|---|
| 1 | 題（§1-1） | A（④ の推奨・73字）「グレンフェルタワー火災の真相。外壁の板を選ぶ話し合いで、関わった人はみな見た目に集中し、火に強いかどうかを外していた。【事故検証】【ゆっくり解説】」 | **A'（82字）**「グレンフェルタワー火災の真相。2014年、外壁の板を選ぶ話し合いで、関わった人はみな見た目に集中し、火に強いかどうかはまるで見なかった。【事故検証】【ゆっくり解説】」／B（59）／C（57） | **A'**＝P2V4 ¶55.33 は「2014年の初め」の話し合いに限る（係 G3）・「外していた」は「的を外す」とも読める（係 G1・G6）＝語りの c105・c608 と同じ「まるで見なかった」（別の目 R1）。4案とも公開ずみ32本と型の網 0件（`titles33.py`） |
| 2 | 問い（§1-3） | A「あなたは、住んでいる建物や、よく行く建物の、非常階段の場所を知っていますか。よければ、コメントで教えてください。」（cc13） | B（この火事を知っていたか）／C（いちばん意外だった所） | **A**（第1章の「階段も1つ」と終章の日本の2つ以上の階段につながる・住民を責めない） |
| 3 | 最期の話（c908） | 残す（「4つ目。…報告は、遺体が火で失われた人はみな、炎が届いたとき、すでに亡くなっていたか、意識が無かった、と認めている。」＝P2V1 ¶2.102） | 外す（約 −77字＝約13,295字・c909「5つ目」→「4つ目」・c911「6つ目」→「5つ目」） | **残す**＝報告の認めたことを範囲の限定ごと言っていて、画面は文字の札だけ（人を描かない）・6つの話の1つが抜けると「よく言われる話を当てる」章が欠ける。⚠️ 通し読みの係は「外す」（中身を言わない「つらい話」のあとに遺体の話を聞かせる）＝どちらも筋が立つ |
| 4 | 罪名を入れるか（cb08） | 入れない（① の線②＝数と日付だけ） | 入れる＝「罪は、法人の過失致死や、重大な過失による致死、詐欺、公務の上の不正行為など。どの容疑の対象にどの罪かは、発表に無い。」（約 +60字＝約13,432字＝幅の内） | **入れない**＝第6章の会社の「不正」と「詐欺」が結びつき、どの会社が容疑の対象かを言わない線②に触れて聞こえる（係 G5）。画面の頁も罪名の列を入れない切り出しにした（cb06） |
| 5 | Commons の写真を取る | 未取得（縮小版の見本帳だけ） | **37点**＝本体34（第1版 §7）＋地だけの3（[24]・[25]・[63]）・権利 CC BY 2.0 が19・BY-SA 4.0 が7・BY-SA 2.0 が5・BY 4.0 が3・CC0 が3・原本の合計 144.1MB（1点最大16.0MB）＝取るのは標準の縮小版（記憶 `reference-commons-standard-thumbnail-sizes`）・置き場は git の外 `src/commons/` | **取る**（映像方針のチャットで・取る前に一覧の大きさをもう一度示す）。△＝[18]（横断幕の字）・[58]〜[60]（追悼の壁と掲示）・BY-SA の [26]・[30]・[31]・[33] は原寸で見てから使う |
| 6 | 章名（11） | 第1版のまま | 変える章があれば | **このまま**（「試験をごまかした会社」は ¶2.19 の manipulate the testing processes の範囲・「国は知っていた」は ¶2.5・¶2.9 の範囲＝係 G4） |

### 0-4. 名前の網
- 網＝git の外 `src/names_private.txt`（2,125語 → ④' で47語を足して2,172語）＋`src/names_commons.txt`（32語）＝語の一部でも鳴る。第2版と道具と、`git ls-files ref/ep33` の全部に当てて **0件**
- ⚠️ ④' で分かった網の穴＝報告の本文の住民の名の一部（名の方と、証人の一覧に無い住民）が網に無かった＝原文の窓に伏せられずに出た（どこにも写していない）→ 報告の本文の「Flat 番号」の近くに書かれた名を機械で拾い（184語）、網に無い48語のうち英単語の一部で鳴る1語を外した47語を網の末尾に足した（git の外・語は出さずに足した）。原文の窓を読むときは、網に加えて「大文字で始まる語の並び」も伏せる濾し器を通した（git の外の作業の道具）
- 係の申告＝`src33.py` の窓は名前を伏せない（道具の説明どおり）・`--fig` の窓の頭の札が図や脚注の番号を段落の札と読むことがある・`--fig 6.1` が 6.10 にも当たる・`cand33.py` は英単語の一部を伏せすぎることがある＝⑤ 以降で使うなら直す

### 0-5. 変更台帳（差し替え表 `v2_build/patches33.json` の要約）
- **190件**＝語り94・聞き役11・画の欄46・出典の欄19・§19・カットの並べ替え1（cb12〜cb14＝「待っている」を警視庁の説明のすぐ後ろへ・番号は振り替え）＝係の案をそのまま115・④' が字を書いた74（別の目の30を含む）
- 字＝13,491 → **13,372**（−119）・🔧 112 カット・欠番 0・カットの数は変わらない
- 対照表＝`v2_build/diff_v1_v2.md`（`make_diff33.py`）・消えた語＝git の外 `src/agents/wf33b/lost_words.txt`（`lost33.py`）

### 0-6. 係・道具・費用（チャット4）
- 照合と通し読みの係 6本（Workflow・同時2本）＝**179.2万トークン・道具323回・約87分**（見積もり 180〜220万の内）・線の申告は道具の穴だけ（名前を返事に書いた係は無い）
- 別の目 2本（R1＝冒頭〜第5章・R2＝第6〜11章と §・同時2本）＝**59.2万トークン・道具126回・約23分**（見積もり 60〜80万の内）・所見28（🔴2）・線の申告は道具の穴だけ
- 合わせて係8本＝約238.4万トークン
- 画像 0枚／40・web の頁 0（取得なし）・課金 API 0

### 0-7. ⑥ の頭と公開の直前に当て直す所（記憶 `feedback-jiko-recheck-time-bound-claims`）
- 刑事（cb01〜cb16）＝警視庁と検察の発表（写しの最新は 2026-09-30＝判断は2027年6月より前の約束）
- 勧告の実施（ca14＝2026年9月の時点で61のうち30）・取り壊し（ca15＝早くて2027年の春）・2つ目の階段の指針（ca13＝2025年2月の応答の「2026年から」＝施行されたか）
- 香港（cc06＝2026-01-15 の警察の発表の168人）・日本の決まり（cc02〜cc03＝2017年10月の国の表＝いまの形）

## 2. 照合の表
- 片 361（`v1_build/quotes33.py`・`v1_build/quotes33_result.tsv`）＝OK 357／OK(¶?) 4（P1V1 ¶1.3＝c427・c428）／外れ0
- ⚠️ quotes33 の OK は「片が巻の中に在り、2頁前までに段落の札がある」まで＝隣の段落の取り違えと、「…」で飛ばした条件・話者は拾えない（係の申告）＝④' は意味の照合を人と係で
- 係の点検のあとで足した片＝P1V2 ¶10.22（c306）・P1V4 ¶24.36（c422）・P1V4 ¶28.133（c414）・P2V5 ¶83.12 の別の文（c524）・P2V4 ¶55.71（c617）・¶55.72 の条件と別の文（c615・c616）・P2V1 ¶2.15（c712）・¶2.121 の続き（c721）・P1V1 ¶8.1 と P2V1 ¶9.41（c806）・P2V1 ¶11.77 の問いと返事（c813）・P1ES ¶2.18（c912）・国の調べの条件（cc04）・警1（cb08）
- 照らせない出典＝なし（計・画のほか）

## 3. 章ごと（始まりは句読点なし÷365 の積み上げ）

| 章 | 始まり | カット（目安） | 句読点なし（目安・差） | 分 | 実写（割合） | 聞き役 |
|---|---|---|---|---|---|---|
| 冒頭 | 0:00 | 13（13） | 673（730・−57） | 1.84 | 13（100%） | 3 |
| 第1章 | 1:50 | 17（17） | 905（910・−5） | 2.48 | 12（71%） | 7 |
| 第2章 | 4:19 | 20（20） | 1,026（1,100・−74） | 2.81 | 14（70%） | 6 |
| 第3章 | 7:08 | 32（33） | 1,722（1,830・−108） | 4.72 | 17（53%） | 8 |
| 第4章 | 11:51 | 26（26） | 1,526（1,460・+66） | 4.18 | 10（38%） | 7 |
| 第5章 | 16:01 | 30（30） | 1,782（1,640・+142） | 4.88 | 11（37%） | 9 |
| 第6章 | 20:54 | 23（23） | 1,359（1,280・+79） | 3.72 | 6（26%） | 7 |
| 第7章 | 24:38 | 20（20） | 1,155（1,100・+55） | 3.16 | 8（40%） | 5 |
| 第8章 | 27:48 | 13（13） | 715（730・−15） | 1.96 | 3（23%） | 3 |
| 第9章 | 29:45 | 17（17） | 986（910・+76） | 2.70 | 9（53%） | 5 |
| 第10章 | 32:27 | 17（17） | 848（910・−62） | 2.32 | 5（29%） | 4 |
| 第11章 | 34:47 | 13（13） | 748（684・+64） | 2.05 | 6（46%） | 3 |
| ed01 | 36:50 | — | 46 | — | — | — |

- 章の終わりのつなぎ（11）＝c113（塔が建てられた1970年代へ）・c217（報告は時刻を追う）・c320（外壁で何が起きたかを実験から）・c432（消防は塔の中の人にどう伝えたか）・c526（2012年へ）・c630（売った会社は何を知っていたか）・c723（国は何を知っていたか）・c820（よく言われる話を当てる）・c913（何が変わったか）・ca17（誰かが罪に問われるのか）・cb17（日本の話と3つの答え）
- 3つの問い（c109〜c110）の答え＝1つ目 c430・cc08／2つ目 c525・cc09・cb15／3つ目 第5〜7章・cc10（§1-2）

## 1. ④で決めたこと

### 1-1. 題（§B4・型＝〈事故名〉の真相。〈事実の1句〉【事故検証】【ゆっくり解説】・【映像あり】なし＝materials.md §0・「犠牲」「死亡」不可）
- 型は記憶 `feedback-jiko-title-form`（26本目からの「事故名を頭・1句を後ろ」）で確かめた。報告は2019年と2024年に出そろった＝「の真相」を使う（① の承認④）。字数は数えた（全角も半角も1字）。承認は ④' のあと

| 案 | 題 | 字数 | 根拠 |
|---|---|---:|---|
| **A（④の推奨）** | グレンフェルタワー火災の真相。外壁の板を選ぶ話し合いで、関わった人はみな見た目に集中し、火に強いかどうかを外していた。【事故検証】【ゆっくり解説】 | 73 | c105・c608＝P2V4 ¶55.33「throughout the discussions in early 2014 … everyone involved concentrated on the appearance … to the complete exclusion of their fire performance」（芯 A の問いにつながる・係の指摘で「選ぶ話し合いで」と範囲を合わせた） |
| **A'（④' の推奨）** | グレンフェルタワー火災の真相。2014年、外壁の板を選ぶ話し合いで、関わった人はみな見た目に集中し、火に強いかどうかはまるで見なかった。【事故検証】【ゆっくり解説】 | 82 | A の範囲を ¶55.33 に合わせて時期（early 2014）を足し、「外していた」（的を外すとも読める）を c105・c608 の語りと同じ「まるで見なかった」に（G3・G1・G6・R1 の所見）＝型の網 0（`v2_build/titles33.py`） |
| B | グレンフェルタワー火災の真相。台所のありふれた火は、3時間足らずで24階建ての塔を包んだ。【事故検証】【ゆっくり解説】 | 59 | c106・c419＝P1ES ¶2.13「enveloping the entire building in under three hours」・P1ES ¶2.12「perfectly foreseeable」 |
| C | グレンフェルタワー火災の真相。「部屋で待て」を改めるべき時から、1時間近くが失われた。【事故検証】【ゆっくり解説】 | 57 | c108・c519＝P1V4 ¶28.6「the best part of an hour had been lost」 |

### 1-2. 芯（① §9 の推奨どおり・kousei.md §3 の組み）
- **A＋B＋C の組み**・章の順は推奨どおり「夜（第2〜4章）を先に・なぜ（第5〜7章）を後で」。冒頭の問い（c109〜c110）＝1つ目 B「台所のありふれた火は、なぜ、あれほど速く塔を包んだのか」（答え＝第3章 c430・終章 cc08）／2つ目 C の前半「消防の『部屋で待て』は、何を間違えたのか」（答え＝第4章 c525・終章 cc09）／3つ目 A「燃える外壁は、誰が、なぜ選んだのか」（答え＝第5〜7章・終章 cc10）。C の後半「9年たっても出ない答え」は第10章
- 芯 A の問いは冒頭の引き（c105＝43.4秒）で先に立てた（kousei §4「引きは46秒より前」）。並べる順は答える順（B → C → A）
- 「よく言われる話」は第8章にまとめた（6つ＝合法・ガス・ブログ・最期・スプリンクラー・安さ）＋消防の対応。「見捨てた」の語は使わない（第4章も第8章も報告の言葉で）

### 1-3. コメントの問い（§B3-7b＝誰でも気軽に答えられる・責める相手を作らない・です・ます・3行以内・「あなたは」から）
| 案 | 問い |
|---|---|
| **A（④の推奨＝cc13 に入れた）** | あなたは、住んでいる建物や、よく行く建物の、非常階段の場所を知っていますか。よければ、コメントで教えてください。 |
| B | あなたは、この火事のことを、この動画を見る前から知っていましたか。よければ、コメントで教えてください。 |
| C | あなたは、この動画で、いちばん意外だったのはどこでしたか。よければ、コメントで教えてください。 |
- A は第1章（階段も1つ、入口も1つ）と終章（日本の2つ以上の階段）につながる。住民を責める形にしない

### 1-4. 語りと画面に出す人（① の承認①）
| 人 | 扱い |
|---|---|
| 住民 | 名前なし・人数だけ。出火した部屋の住人は「4階の1室の住人」「その住人」（責任は無い＝c304） |
| 消防 | 「最初の消防の隊」「隊員」「最初の現場の指揮者」「より上の幹部」「指令室の幹部たち」・名前なし（P1ES の年表の名前は片から外した） |
| 調査・政府 | 「調査の委員長」「首相」「国の担当の役人」「死因を調べる検死官」・名前なし |
| 会社と団体（報告が名指しした結論の範囲） | スタジオE（設計事務所）・ライドン（元請け）・ハーレー（外装の下請け）・CEP（板の加工）・アルコニック（板の製造）・セロテックスとキングスパン（断熱材）・管理の組織 TMO・区・試験の機関（BRE＝語りでは「その機関」）・認証の機関（BBA・LABC・UKAS＝語りでは名を出していない） |
| 社員・専門家 | 「下請けの社員」「管理の組織の担当者」「専門家」・名前なし |
| 刑事 | 警視庁の発表の数と日付だけ・どの会社や人が容疑の対象かは言わない（cb10 で断った） |

### 1-5. 割れる数と言い方（台本で決めた言い方）
| 項目 | 台本 | 別の言い方（言わない・帰属で並べた） | 出典 |
|---|---|---|---|
| 亡くなった人 | 72人（内訳は c428 で1回だけ＝塔から逃げられず70人・逃げたあとに死産となった子・7か月後に亡くなった人） | 審問70件・警視庁の推定79（2017-06-19）＝使わない | 警1・P1V4 ¶32.1・P1V1 ¶1.3 |
| 塔 | 地上24階・地下1階・高さ約67m・階は英国の数え方（地上の階＝0階・c204 で断った）・住戸129（7つは空き） | 国交省の「24階建・68m・120戸・8階から出火」＝使わない | P1V1 ¶3.9・¶3.13・P1V2 ¶10.130 |
| 逃げた人 | 1時30分までに112人（本文＝P1V4 ¶28.14j・要約の表は1時31分 110人）・1時50分 168人・合わせて227人・2時35分より後に46人（うち 2:53〜8:07 に約36人） | ― | P1V4 ¶28.14・P1ES ¶2.11・P1V1 ¶1.3・P1V4 ¶28.81 |
| 時間 | 「20分足らず」（1:09→1:26）・「3時間足らず」（報告の under three hours）・「1時間近く」（the best part of an hour）・最後の生存者 8時7分 | 「60時間燃えた」＝使わない・¶2.10 の 08.10＝使わない | P1V4 ¶28.14・P1ES ¶2.13・P1V4 ¶28.6・P1ES ¶2.11 |
| 外壁の額 | 2013年2月 30万ポンド（約4,300万円）／2014年3月の同じ板〈アルミ複合板・リベット〉＝下請け→元請け 約58万ポンド（約9,800万円）・元請け→管理の組織 約38万ポンド（約6,400万円）・差 約20万ポンド・見積りの誤り 約21万ポンド（約3,600万円） | カセットの額（£419,627・£293,368）・£243,000・£270,000・£800,000 は使わない | P2V4 ¶55.11・¶55.43・¶55.48・¶55.58〜55.59 |
| 円の換算 | **当時の月の平均**＝イングランド銀行の XUMAJYS（2013年2月 1ポンド＝144.08円・2014年3月 170.12円）＝画面に「換算：イングランド銀行の月平均（2013年2月／2014年3月）」 | 今の円で言わない（公開の日で変わる） | `src/web/boe/`（2026-11-12 に取得・robots.txt を確かめた） |
| 刑事 | 2024年 58人・19団体 → 2026年5月 57人・20団体 → 2026年9月30日 54人・20団体（書類20＋全体の証拠14）・判断は2027年6月より前 | 会社の名は言わない | 警1〜警3 |
| 勧告 | 58（国へ37・ほかへ21）・49を全面・9を考え方として・追う61のうち30が済み（2026年9月の時点） | 第2段階の58だけの済みの数（係の読み）＝使わない | 応・進 |

### 1-6. そのほか
- **決め所の画面なし**（10-07）・原文の片は語りの中・★の行なし。「すべて避けられた」は ca09 に**帰属つき**（調査の委員長の言葉を首相が議会で引用＝首）。報告の本文の言葉としては言わない
- **語の補足は業界の語だけ**＝アルミ複合板（c212）・カセット（c407）・区画（c317）・999（c301）・TMO（c208）・クラス0（c720）・等級E（c707）・試験用に組んだ外壁を燃やす大規模な試験（c710）・検死官（c806）。一般の語（スプリンクラー・弁護士・検察・容疑者など）は補足しない
- **時刻の札**は「1:09」の形（画の欄の副題）・語りは「午前1時9分」。英国の夏時間のまま言う（日本時間に直さない）
- 🔴 **動く部分**＝ca14〜ca15（勧告の実施・取り壊し）・ca13（2つ目の階段の指針＝2025年2月の応答が書いた「2026年から」の予定＝施行されたかを当て直す）・cb01〜cb17（刑事）・cc06（香港）＝⑥ の頭と公開の直前に当て直す（記憶 `feedback-jiko-recheck-time-bound-claims`）
- ⚠️ **最期の話（c908）**は、報告の認めたことだけを、つらい語を使わずに置いた＝④' と承認①で「残すか」を見てほしい

<!-- §1 の終わり -->

## 4. 台本

### 冒頭（13カット）

**c101** 🔧 ／ 実写 紙面 P1V4 図22.8（台所の窓のまわりの板の上から炎が外へ出るコマ〈01:09:30〜01:09:40〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「台所の窓のまわりの炎〈1:09〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第4巻 図22.8（2019）」） ／ P1ES¶2.11（`Fire breaks out of Flat 16 into exterior cladding and starts to climb the east facade rapidly`）
> 2017年6月14日、午前1時9分。ロンドンの24階建ての住宅、
> グレンフェルタワーの1室の台所から、炎が外壁に移った。

**c102** ／ 実写 紙面 P1V2 図10.14（東の面の外の炎・01:19:04 のコマ・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「外壁を上る炎〈1:19〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図10.14（2019）」） ／ P1ES¶2.12（`The fire had entered the cladding before firefighters opened the kitchen door in Flat 16 for the first time at 01.14`）
> 消防の隊が、その台所のドアを初めて開けたのは、1時14分。
> 火はもう、外壁の中に入りこんでいた。

**c103** ／ 実写 紙面 P1V2 図10.22（屋上の飾りの上で炎が続くコマ〈01:27:42 より後〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「屋上に届いた炎〈1:27ごろ〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図10.22（2019）」） ／ P1V4¶28.14（`very top of the building by 01.26, i.e. in under 20 minutes`）・P1ES¶2.11（`Fire reaches the roof and starts to spread horizontally`）
> 外壁を駆け上がった炎は、20分足らずで、塔のてっぺんに届いた。
> そこから、塔の上を、横へ回りはじめる。

**c104** ／ 実写 紙面 P1V2 図14.1（警察のヘリコプターから撮った 02:06 のコマ・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「警察のヘリコプターから〈2:06〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図14.1（2019）」） ／ P1ES¶2.13（`The principal reason why the flames spread so rapidly up, down and around the building was the presence of the aluminium composite material (ACM) rainscreen panels with polyethylene cores, which acted as a source of fuel`）
> Q: なぜ、そんなに速く？
> 外壁の板の芯は、燃えるプラスチックだった。調査の報告は、
> それが、炎がこれほど速く広がった、いちばんの理由だと結論している。

**c105** 🔧 ／ 実写 写真 [7]（夜明けの遠景・炎の見える塔・手前に低い建物と放水・全画面・副題「燃える塔〈2017年6月14日の夜明け〉」・出典の行「Wikimedia Commons（CC BY 4.0）」） ／ P2V4¶55.33（`everyone involved concentrated on the appearance of the rainscreen panels to the complete exclusion of their fire performance`）
> 報告によれば、外壁の板を選ぶ話し合いで、関わった人はみな見た目に集中し、
> 火に強いかどうかは、まるで見なかった。その板は、誰が、なぜ選んだのか。

**c106** 🔧 ／ 実写 写真 [12]（夜明け・煙の柱と炎の塔〈縦〉・高さいっぱい＋同じ写真のぼかしの地・副題「煙を上げる塔〈2017年6月14日の夜明け〉」・出典の行「Wikimedia Commons（CC BY 4.0）」） ／ P1ES¶2.11（`the fire starts to spread to the north elevation of the tower`…`Flames start to spread to south elevation`…`Fire starts to spread across the west elevation of tower`）・P1ES¶2.13（`enveloping the entire building in under three hours`）・警1（`took the lives of 72 people`）
> 報告によれば、炎は東の面から北、南、西へと回り、
> 3時間足らずで、塔をまるごと包んだ。この災害で、72人が亡くなった。

**c107** ／ 実写 写真 [3]（夜明けの空にロンドンの上を流れる煙の柱〈遠景・横長〉・BY-SA 4.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・副題「ロンドンの空を流れる煙〈2017年6月14日の朝〉」・出典の行「Wikimedia Commons（CC BY-SA 4.0）」） ／ P2V7¶98.1（`The Grenfell Tower fire was one of the worst post-war civil disasters in the UK`）
> Q: 調査は、この火事を、どう書いたの？
> 国が開いた公開の調査は、戦後の英国で最悪の災害の1つ、と書いた。

**c108** ／ 実写 写真 [8]（朝・煙と放水の塔の寄り〈縦〉・高さいっぱい＋同じ写真のぼかしの地・副題「朝の塔と放水〈2017年6月14日〉」・出典の行「Wikimedia Commons（CC BY 4.0）」） ／ P1V1¶4.3（`the occupants are advised to remain within their own flats unless they are directly affected by fire, heat or smoke`）・P1V4¶28.6（`the best part of an hour had been lost without any evacuation plan having been considered`）
> その夜、消防は、塔の住人に「部屋で待て」と伝え続けた。報告は、
> それを改めるべき時から、1時間近くが失われた、と書いている。

**c109** ／ 実写 映像 #15 焼けた塔A（3:00〜3:50 を4つに割った1つ目〈約12秒〉・通りから木の向こうの焼けた塔・副題「焼けた塔〈2017年7月〉」・出典の行「Wikimedia Commons（CC BY 3.0）」） ／ 計（この動画の問い）
> この動画は、調査の報告をもとに、3つの問いに答えていく。1つ目。
> 台所のありふれた火は、なぜ、あれほど速く、塔をまるごと包んだのか。

**c110** ／ 実写 写真 [40]（ロンドン消防の車と焼けた塔・全画面・副題「消防の車と焼けた塔〈2017年6月18日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ 計（この動画の問い）
> 2つ目。消防の「部屋で待て」は、何を間違えたのか。
> そして3つ目。燃える外壁は、誰が、なぜ選んだのか。

**c111** 🔧 ／ 実写 写真 [28]（青空の下の焼けた塔・全画面・副題「焼けた塔〈2017年6月16日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ 計（報告の PDF＝12冊・2,582頁＝第1段階 2019-10-30 の要約と4巻・第2段階 2024-09-04 の7巻・火事から第2段階の報告まで＝7年3か月）
> Q: どれも、知りたいことなんだ。
> 公開の調査は、2019年に、あの夜に何が起きたかを、
> 2024年に、なぜ起きたかを報告した。12冊、2,500ページをこえる。

**c112** ／ 実写 写真 [70]（下の階だけ白く残る焼けた塔〈縦〉・高さいっぱい＋同じ写真のぼかしの地・副題「焼けた塔〈2017年6月20日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P2V1¶2.4（`the fire at Grenfell Tower was the culmination of decades of failure by central government and other bodies in positions of responsibility in the construction industry`）
> この動画は、その報告と、政府と警察の発表をたどる。報告は、
> 会社や国の役所の名を挙げて、何十年にもわたる失敗を書いている。

**c113** ／ 実写 写真 [32]（家並みの奥の焼けた塔・全画面・副題「家並みの奥の塔〈2017年6月20日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P1V1¶3.1（`Grenfell Tower is a residential tower block built in 1974`）
> 話は、その塔が建てられた1970年代と、
> 外壁が新しくなった2010年代のロンドンにさかのぼる。

---

### 第1章　ロンドンの24階建ての塔（17カット）

**c201** ／ 実写 映像 #15 空撮A（0:25〜2:40 のうち川と高いビルの区間・副題「ロンドンの空撮〈2017年7月〉」・出典の行「Wikimedia Commons（CC BY 3.0）」） ／ P1V1¶3.1（`It is located in the Lancaster West Estate in North Kensington, London W11`）
> Q: どこにあった塔なの？
> ロンドンの西。ケンジントン・アンド・チェルシー区の北にある、
> ランカスター・ウェストという団地の中だ。

**c202** ／ 実写 衛星 ランカスター・ウェスト団地（塔の位置・南へのびる低い3棟・東の緑地・南西の地下鉄の駅〈Latimer Road〉の札・Google の表示を絵の近くに・副題「塔のある団地〈現在の衛星写真〉」） ／ P1V1¶3.2（`The walkways extend 150 metres south from the tower and enclose two green spaces`）・P1V1¶3.4（`approximately 200 metres' walking distance from the entrance to the tower`）
> 塔の南には、低い3棟の住宅が、緑地を囲んで150メートルのびていた。
> 地下鉄の駅のある通りまでは、塔の入口から歩いて約200メートルだ。

**c203** ／ 実写 紙面 P1V1 図3.2（改修の前の塔の外壁・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「改修の前の外壁」・出典の行「グレンフェル・タワー調査 第1段階の報告 第1巻 図3.2（2019）」） ／ P1V1¶3.1（`building work commenced in 1972 and was completed by 1974`）・P1V1¶3.9（`just over 67 metres tall and has 25 storeys, including a basement and ground floor to floor 23`…`central reinforced concrete core, reinforced concrete floors and perimeter reinforced concrete columns`）
> 塔ができたのは1974年。鉄筋コンクリートで、高さは約67メートル。
> 地上24階、地下1階の建物だ。

**c204** 🔧 ／ 図 立面（塔の階の札＝地上の階を0階・住戸は主に4階から23階・下の階には保育園などと、改修で足した9戸・地＝実写 写真 [28] を暗く） ／ P1V1¶3.13（`Floors 4 to 23 were designed to accommodate residential flats, with six flats on each floor`）
> イギリスでは、日本の1階にあたる階を、0階と数える。この動画も、そう数える。
> 住まいは、主に4階から23階で、各階に6つの住戸があった。

**c205** ／ 図 模式（1つの階の間取り＝真ん中に階段1つとエレベーター2基・まわりに6つの住戸・地＝実写 写真 [28] を暗く） ／ P1V1¶3.18（`Within the central core of the building was a single staircase and two lifts serving each floor of the tower`）
> Q: 逃げ道は、どこにあったの？
> 塔の真ん中に、階段が1つと、エレベーターが2基。
> そのまわりを、6つの住戸が囲んでいた。

**c206** ／ 実写 紙面 P1V2 図10.5（塔の0階の入口と消防の送水口・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「塔の入口」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図10.5（2019）」） ／ P1V1¶3.2（`the only access to the tower for residents was through the entrance at ground level on the south side`）
> 住人が出入りできる入口は、0階の南側の1か所。
> 階段も1つ、入口も1つの塔だった。

**c207** ／ 実写 写真 [61]（白い曲面の建物と焼けた塔〈隣のレジャーセンターと見られる〉・全画面・副題「塔と隣の建物〈2017年6月26日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P1V2¶10.130（`people in 129 flats in the tower, including visitors`…`Seven flats were empty on that night`…`Sixty-seven of those present were children under the age of 18`）
> 火が出た夜、塔の129の住戸には、訪ねてきた人も含めて297人がいた。
> 空いていた住戸は7つ。いた人のうち67人は、18歳より下の子どもだった。

**c208** ／ 図 模式（持ち主と管理の札＝ケンジントン・アンド・チェルシー区 → 管理の組織 TMO → 住人・地＝実写 写真 [61] を暗く） ／ P1V1¶3.1（`Grenfell Tower is owned by RBKC`）・P1V1¶3.6（`The vast majority of the residential flats in the tower were part of RBKC's provision of social housing within the borough`）・P1V1¶3.8（`RBKC entered into a Management Agreement with the TMO`）
> 塔の持ち主は区で、住戸のほとんどは、区が貸す家賃の安い住まいだった。
> 管理は、区が契約した、TMOという管理の組織が担っていた。

**c209** ／ 実写 写真 [29]（青空の焼けた塔・全画面・副題「焼けた塔〈2017年6月17日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P1V1¶3.7（`Some had grown up in North Kensington`…`Others had come to this country as refugees`…`Together they formed a vibrant community with a strong sense of identity and considerable social cohesion`）
> Q: どんな人たちが住んでいたの？
> この地で育った人も、ほかの国から逃れてきた人もいた。報告は、
> 強いつながりのある、活気のある地域だった、と書いている。

**c210** ／ 実写 紙面 P1V1 図6.1（改修のあとの上の階の外壁の寄り・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「改修のあとの外壁」・出典の行「グレンフェル・タワー調査 第1段階の報告 第1巻 図6.1（2019）」） ／ P1V1¶6.1（`the refurbishment carried out between 2012 and 2016`…`the over-cladding of every storey of the existing building with a new insulation and rainscreen cladding system`）
> 2012年から2016年にかけて、塔は大きく改修された。
> 元の外壁の外側に、断熱材と、新しい外装の板をかぶせたのだ。

**c211** ／ 図 断面（外壁の断面＝外から外装の板〈アルミ複合板〉・すき間・断熱材・元のコンクリートの壁の順・地＝実写 写真 [72] を暗く） ／ P1V1¶6.7（`At floors 4 to 23 they comprised insulation materials, new windows, new window infill panels and outer aluminium composite material (ACM) rainscreen panels`）
> 外から順に、外装の板、すき間、断熱材、そして元のコンクリートの壁。
> 外装の板は、アルミ複合板という板だった。

**c212** ／ 図 模式（アルミ複合板の断面＝2枚の薄いアルミの板と、あいだのポリエチレン・地＝実写 写真 [72] を暗く） ／ P2V1¶2.21（`They were an ACM product made of two thin sheets of aluminium with a polyethylene core`…`Polyethylene burns fiercely`）
> Q: アルミ複合板って、どんな板？
> 2枚の薄いアルミの板で、ポリエチレンというプラスチックをはさんだ板だ。
> ポリエチレンは、激しく燃える。

**c213** ／ 実写 紙面 P1V1 図6.11（屋上の飾り〈クラウン〉の設計図・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「屋上の飾りの設計図」・出典の行「グレンフェル・タワー調査 第1段階の報告 第1巻 図6.11（2019）」） ／ P1V1¶6.35（`The fins and the associated structure at the crown had no functional purpose and were purely aesthetic`）
> 塔のてっぺんには、同じ板で、冠のような飾りも付けた。
> 報告によれば、役目は何も無い、見た目のためだけの飾りだった。
> Q: 見た目のためだけ、なんだ。

**c214** ／ 実写 写真 [71]（焼けた塔の上部〈横長〉・全画面・副題「焼けた塔の上部〈2017年6月20日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P1V1¶6.4（`The Department of Building Control at RBKC acted as building control authority`…`The Building Certificate for completion of the works was signed by RBKC on 7 July 2016`）・計（2016-07-07 から 2017-06-14 まで＝11か月）
> 区の建築を確かめる部署が、工事の完了の証明に署名したのは、2016年7月。
> 火事の、1年足らず前のことだ。

**c215** 🔧 ／ 実写 写真 [55]（焼けた塔〈縦〉・高さいっぱい＋同じ写真のぼかしの地・副題「焼けた塔〈2017年6月16日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P1ES¶2.16（`they did not adequately resist the spread of fire having regard to the height, use and position of the building`…`On the contrary, they actively promoted it`）
> Q: 新しい外壁は、火に強かったの？
> 報告は、その外壁は火の広がりを十分に防がず、
> それどころか、広がりを強めた、と書いている。

**c216** 🔧 ／ 実写 写真 [62]（焼けた塔の寄り・全画面・副題「焼けた塔〈2017年6月26日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ 計（第5章へのつなぎ）
> Q: その外壁を、誰が選んだのかが、問題なんだね。
> そう。それは後の章で、報告をたどる。その前に、まず、あの夜に何が起きたかだ。

**c217** ／ 実写 写真 [19]（遠景の焼けた塔とクレーン・全画面・副題「焼けた塔とクレーン〈2017年6月20日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P1ES¶2.10（`organised into 11 separate periods between 00.54`…`when the last survivor left the tower`）
> 報告は、その夜を、午前0時54分から朝8時すぎまで、
> 11の時間帯に分けて、時刻を追って書いている。

---

### 第2章　午前0時54分、4階の台所（20カット）

**c301** ／ 実写 紙面 P1V4 図21.1（火のあとの台所〈出火元〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「出火した台所〈火事のあと〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第4巻 図21.1（2019）」） ／ P1ES¶2.11（`calls 999 to report a fire in Flat 16, floor 4 Grenfell Tower`）
> 6月14日の午前0時54分。4階の1室の住人が、
> 緊急の番号、999に電話をかけた。台所で、火が出ていた。

**c302** ／ 実写 紙面 P1V4 図21.4（大きな冷凍冷蔵庫の下の床の焼け跡・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「冷凍冷蔵庫の下の床の焼け跡」・出典の行「グレンフェル・タワー調査 第1段階の報告 第4巻 図21.4（2019）」） ／ P1ES¶2.12（`it was started by an electrical fault in a large fridge-freezer in the kitchen of Flat 16`）
> 火元は、台所にあった、大きな冷凍冷蔵庫だ。
> 報告は、その電気の故障から火が出た、と結論している。

**c303** ／ 実写 紙面 P1V4 図21.6（部屋の配電盤〈スイッチの位置〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「部屋の配電盤」・出典の行「グレンフェル・タワー調査 第1段階の報告 第4巻 図21.6（2019）」） ／ P1ES¶2.12（`I have not been able to establish the precise nature of the fault in the fridge`…`how the failure of a common domestic appliance could have had such disastrous consequences`）
> Q: どんな故障だったの？
> 報告は、故障の中身までは突き止められなかった、と書く。大事なのは、
> ありふれた家電の故障が、なぜ、これほどの結果につながったかだ、と。

**c304** 🔧 ／ 図 模式（台所の間取り＝冷凍冷蔵庫・窓・換気扇の板・ドアの位置の札・地＝実写 写真 [63] を暗く） ／ P1ES¶2.12（`bears no blame`）
> Q: 住んでいた人に、落ち度はあったの？
> 無い。報告によれば、その部屋の住人には、何の責任も無い。

**c305** ／ 実写 紙面 P1V2 図10.6（台所の窓の中の火のコマ〈01:05・01:06・01:08・01:09〉＝住人の携帯電話の映像のコマ・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「台所の窓の中の火〈1:05〉」・図と時刻の組は ⑤b で本文の並び〈1:05・1:06・1:08・1:09〉と照らす・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図10.6（2019）」） ／ P1V2¶10.36（`After he had alerted his neighbours`…`From that position he filmed the development of the fire using his mobile telephone`）
> その住人は、近くの部屋に知らせてから、塔の外へ出た。
> そして、部屋の真下から、携帯電話で、火を撮り続けた。

**c306** 🔧 ／ イメージ（フリー素材＝夜の街を走る消防車〈車体の字と番号と人の顔は見せない〉・画面に「イメージ」） ／ P1ES¶2.11（`First firefighters reach the tower`…`having made up from 4 to 6, to 8, to 10 and to 15 between 01.13 and 01.28`）・P1V2¶10.22（`The four appliances arrived within the targets set by the 2017 London Safety Plan`）
> 最初の消防の隊が塔に着いたのは、通報から5分後の、0時59分。
> はじめに向かった消防車は4台。台所の火の通報への、出動だった。

**c307** ／ 実写 紙面 P1V2 図10.7（台所の窓の中の火の続きのコマ・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「台所の窓の中の火〈1:06〉」・図と時刻の組は ⑤b で照らす・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図10.7（2019）」） ／ P1V2¶10.37（`When the firefighters reached floor 4 they found the visibility`…`While they were waiting for the dry rising main to be charged with water`）
> 隊員は、4階へ上がった。廊下の見通しは、よかった。
> 部屋の前でホースを伸ばし、水が届くのを待つ。

**c308** ／ 図 模式（窓のわきの樹脂の枠が熱い煙でゆがみ、外壁の中のすき間へ火の通り道ができるまで〈報告の見立て〉・地＝実写 写真 [63] を暗く） ／ P1ES¶2.12（`The fire is most likely to have entered the cladding as a result of hot smoke impinging on the uPVC window jamb, causing it to deform and collapse`）
> Q: 火は、どこから外へ出たの？
> 報告が、最もありうるとみる道はこうだ。熱い煙が、窓のわきの樹脂の枠を、
> ゆがませ、崩した。そこに、外壁の中のすき間への、火の通り道ができた。

**c309** ／ 図 模式（もう1つの道＝開いていた窓から炎が外の板へ〈報告は「ありうるが、見込みは低い」〉・地＝実写 写真 [63] を暗く） ／ P1ES¶2.12（`It is, however, possible (but less likely) that flames from the fire in the fridge-freezer passed through the open kitchen window and impinged on the ACM cladding panels above`）
> 開いていた台所の窓から、炎がじかに外の板へ当たった、という道もありうる。
> ただ報告は、そちらは、見込みがより低いとしている。

**c310** ／ 実写 紙面 P1V2 図10.9（台所の窓のまわりの火のコマ〈01:09 のころ〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「窓のまわりの火〈1:09ごろ〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図10.9（2019）」） ／ P1ES¶2.11（`Fire breaks out of Flat 16 into exterior cladding and starts to climb the east facade rapidly`）
> 1時9分。炎は、台所の窓のまわりから外壁へ移り、
> 塔の東の面を、速い勢いで上りはじめる。

**c311** 🔧 ／ 実写 紙面 P1V4 図22.15（01:15:36 ごろのコマ＝外壁が燃え、炎が部屋の上へ伸びる・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「部屋の上へ伸びる炎〈1:15ごろ〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第4巻 図22.15（2019）」） ／ P1V4¶22.27（`cladding can be seen to be burning with some intensity and external flames are extending approximately two floors above Flat 16`）・P1V4¶22.27（`there is a noise which is likely to be the breaking of at least one pane of glazing within the kitchen window`）
> 1時15分ごろには、外壁が強く燃え、炎は部屋の2階ぶん上まで伸びていた。
> 台所の窓のガラスが割れたとみられる音も、映像に残っている。

**c312** ／ 実写 紙面 P1V2 図10.15（01:21:15 の東の面の外の火のコマ・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「東の面の外の火〈1:21〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図10.15（2019）」） ／ P1ES¶2.12（`A kitchen fire of that relatively modest size was perfectly foreseeable`）・P1V1¶4.2（`The principle of the design known as "compartmentation" lies at the heart of these safety features`）
> Q: 台所の火って、よくあるものなの？
> 報告は、この比較的小さな台所の火は、十分に予想できるものだったと書く。
> 塔は本来、こうした火を、その部屋の中に閉じこめる作りのはずだった。

**c313** 🔧 ／ 図 帯（時刻の帯＝0:54 通報・0:59 隊が着く・1:09 外壁へ・1:13 5階・1:14 台所のドア・1:21 塔の中からの通報・1:26 てっぺん・地＝実写 写真 [63] を暗く） ／ P1V4¶28.14（`It had reached floor 5 by 01.13`…`very top of the building by 01.26, i.e. in under 20 minutes`）
> 外壁の火は、1時26分には、塔のてっぺんに届いた。
> 外壁に移ってから、20分足らずのことだ。

**c314** 🔧 ／ 実写 紙面 P1V2 図10.17（01:27:58 のコマ＝東の面の柱にそって上る炎・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「柱にそって上る炎〈1:27〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図10.17（2019）」） ／ P1ES¶2.11（`First 999 call to the control room from an occupant in the tower`…`First 999 call to report smoke coming into flat from lobby`）・P1V2¶10.90（`said that there was a fire in her kitchen`）
> 1時21分。22階に残る人から、初めての通報が入る。
> 1時25分ごろには、台所が燃えている、廊下から煙が入る、という通報が続く。

**c315** ／ 実写 紙面 P1V2 図10.24（南と北へ回りはじめた炎のコマ・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「横へ回る炎」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図10.24（2019）」） ／ P1ES¶2.11（`makes pumps 20`…`having made up from 4 to 6, to 8, to 10 and to 15 between 01.13 and 01.28`…`makes pumps 25`…`First NPAS (police) helicopter arrives at the scene`）
> 消防は、呼ぶ消防車を次々と増やし、1時31分には、25台を求めた。
> 1時45分には、警察のヘリコプターも、塔の上空に着いた。

**c316** 🔧 ／ 実写 写真 [30]（焼けた塔〈縦〉・BY-SA 2.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・中身は ⑤b で原寸・副題「焼けた塔〈2017年6月18日〉」・出典の行「Wikimedia Commons（CC BY-SA 2.0）」） ／ P1V4¶28.14（`A total of 112 people had left the tower in the 35 minutes that followed`）
> 1時30分までに、塔にいた297人のうち、外へ逃げられたのは112人。
> Q: 残りの人たちは、どうしていたの？

**c317** 🔧 ／ 図 模式（「部屋で待て」の考え方＝火や煙が来ない限り、部屋にとどまる・部屋ごとに火を閉じこめる区画・地＝実写 写真 [63] を暗く） ／ P1V1¶4.3（`The concept of compartmentation, combined with other supporting fire safety provisions, has given rise to the "stay put" strategy`…`unless they are directly affected by fire, heat or smoke`）
> まだ塔の中にいた。高層の住宅には、「部屋で待て」という考え方がある。
> 火や煙が来ない限り、自分の部屋にとどまる、という考え方だ。

**c318** ／ 実写 写真 [69]（焼けた塔〈縦〉・高さいっぱい＋同じ写真のぼかしの地・副題「焼けた塔〈2017年6月20日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P1ES¶2.14（`The fire on the outside of the building quickly entered many flats and smoke spread rapidly through the interior of the building`）
> その前提は、部屋ごとに火を閉じこめる、建物の作りだ。
> ところが外壁の火は、窓を破って、次々と部屋へ入りこんでいく。

**c319** 🔧 ／ 実写 紙面 P1V2 図11.5（1時40分ごろに消防の幹部が撮った塔の写真・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「消防の幹部が撮った塔〈1:43に送られた写真〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図11.5（2019）」） ／ 計（1つ目の問いへのつなぎ）
> Q: 外の火の速さが、鍵なんだね。
> そう。それが、1つ目の問いの中心だ。

**c320** ／ 実写 紙面 P2V7 図109.1（エディンバラ大学の実験の装置〈試す前〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「外壁の材料を燃やす実験の装置」・出典の行「グレンフェル・タワー調査 第2段階の報告 第7巻 図109.1（2024）」） ／ P2V1¶2.116（`In a series of experiments designed by`…`and carried out at Edinburgh University`）
> 次の章では、塔の外壁で何が起きていたのかを、
> 報告と、調査のためにおこなわれた実験からたどる。

---

### 第3章　3時間足らずで、塔を包んだ火（32カット）

**c401** 🔧 ／ 実写 紙面 P2V7 図109.2（実験の 9.44分のコマ＝外装の板の内側と断熱材の表面に炎・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「外壁の材料を燃やす実験〈9分44秒〉」・出典の行「グレンフェル・タワー調査 第2段階の報告 第7巻 図109.2（2024）」） ／ P2V1¶2.115（`The first concerned the respective contributions to the fire made by the ACM rainscreen panels and the polyisocyanurate and phenolic insulation boards`）
> Q: どんな実験をしたの？
> 調査は、塔の外壁と同じ材料を、イギリスのエディンバラ大学で燃やし、
> どの材料が、どれだけ火を大きくしたのかを確かめた。

**c402** ／ 図 模式（アルミ複合板の芯が熱で溶け、流れ、燃える＝薄いアルミの板が熱を広げ、溶ける芯が増えていく・地＝実写 写真 [72] を暗く） ／ P2V7¶109.19（`Once the polyethylene begins to melt, flow and ignite a complex heat transfer process occurs within the system`…`leading to the melting and involvement of ever greater quantities of polyethylene that then becomes available to burn`）
> 板の芯のポリエチレンは、熱で溶け、流れ、そして燃える。
> 薄いアルミの板が熱を広げ、溶けて燃える芯が、どんどん増えていく。

**c403** ／ 実写 紙面 P2V7 図109.3（実験で板がすっかり燃えたコマ・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「板がすっかり燃えた実験」・出典の行「グレンフェル・タワー調査 第2段階の報告 第7巻 図109.3（2024）」） ／ P2V1¶2.116（`the ACM panels were shown to have been by far the largest potential contributor to energy release in the external wall system at Grenfell Tower`）
> 実験では、外壁の中で、とびぬけて多くの熱を出しうるのは、
> アルミ複合板だった。断熱材の熱の出方は、それよりずっと小さかった。

**c404** 🔧 ／ 図 模式（外壁の中＝板と断熱材のあいだのすき間・断熱材が熱をため、燃えて熱を足す・燃えない断熱材でも板はすっかり燃えた・地＝実写 写真 [72] を暗く） ／ P2V1¶2.117（`Insulation also needs to be present, either to retain energy in the system or to burn and contribute additional energy`…`Even non-combustible insulation in the form of mineral wool resulted in the growth of the fire to full involvement of the ACM panel`）
> Q: 断熱材は、関係なかったの？
> 関係はあった。断熱材は、熱をため、自分も燃えて、火を大きくした。
> ただ、燃えない断熱材に替えても、板は、すっかり燃えた。

**c405** 🔧 ／ 図 模式（縦の燃え広がりを強めたものの札＝板の裏の2種類の断熱材・もしかすると窓まわりの部材・地＝実写 写真 [72] を暗く） ／ P1ES¶2.13（`The presence of polyisocyanurate (PIR) and phenolic foam insulation boards behind the ACM panels, and perhaps components of the window surrounds, contributed to the rate and extent of vertical flame spread`）
> 2019年の報告も、板の裏の2種類の断熱材と、もしかすると窓のまわりの部材が、
> 炎が上へ広がる速さと広さを、大きくした、と書いていた。

**c406** ／ 図 模式（報告の結論の札＝いちばんの理由は芯のポリエチレン・断熱材は火を育てた決め手・地＝実写 写真 [72] を暗く） ／ P2V1¶2.118（`the principal factor which led to the rapid growth of the fire was the presence of unmodified polyethylene in the cores of the ACM panels rather than the insulation`…`a decisive factor in promoting the growth of the fire`）
> 報告の結論は、火を急に大きくした、いちばんの理由は、
> 板の芯のポリエチレンだ。ただ、断熱材も、火を育てる決め手になった、と。

**c407** ／ 図 比べ（板の留め方＝平らな板をリベットで留める形と、箱の形に折った板を引っかける形〈カセット〉・地＝実写 写真 [72] を暗く） ／ P2V1¶2.21（`either as flat panels by rivets or as three-dimensional structures, known as cassettes`）・P2V1¶2.117（`Panels in cassette form behave far worse than panels in riveted form`）
> 板の留め方は、2つある。平らな板をリベットで留める形と、
> 板を箱の形に折って引っかける、カセットという形だ。

**c408** ／ 実写 写真 [72]（焼けた外壁の寄り・全画面・副題「焼けた外壁〈2017年6月16日〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P2V1¶2.117（`Panels in cassette form behave far worse than panels in riveted form`）・P2V4¶55.34（`the Reynobond panels installed at Grenfell Tower were cassette-fixed`）
> 実験では、カセットの形のほうが、火の中で、はるかに危なかった。
> この塔に付けられていたのは、そのカセットの形だった。

**c409** ／ 図 模式（てっぺんの飾りの冠に沿って横へ回る炎・地＝実写 写真 [71] を暗く） ／ P1ES¶2.13（`The crown was primarily responsible for the spread of the fire horizontally`）
> Q: てっぺんに届いた炎は、そのあと、どうなったの？
> てっぺんの飾りの冠を伝って、塔の上を、左右へ回っていった。
> 報告は、横へ広げた主な通り道は、この冠だったとしている。

**c410** ／ 図 模式（上から溶けて落ちる燃えたポリエチレン → 下の階の外壁に火がつく → 火がまた上へ → 斜めに進む炎の前線・地＝実写 写真 [71] を暗く） ／ P1ES¶2.13（`The principal mechanism for the spread of the fire horizontally and downwards was the melting and dripping of burning polyethylene from the crown and from the spandrel and column panels, which ignited fires lower down the building`…`thereby allowing the flame front to progress diagonally across each face of the tower`）
> 冠や窓の上下の板からは、燃えたポリエチレンが、溶けて垂れ落ちた。
> それが下の階に火をつけ、その火がまた上る。炎は、斜めに進んでいった。
> Q: 燃えながら、落ちてくるんだ。

**c411** ／ 実写 紙面 P1V2 図11.6（1時40分ごろの塔の写真〈消防の幹部が撮った5枚の1枚〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「燃え広がる塔〈1:40ごろ〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図11.6（2019）」） ／ P1ES¶2.13（`the columns were a principal route of downwards fire spread`）
> 下へ火を運ぶ、主な通り道の1つは、塔の角や壁から張り出した柱だった。
> 柱の外側も、同じ板で覆われていた。

**c412** ／ 図 方位（塔の4つの面＝東・北・南・西と、炎が回った時刻の札〈1:09 東・1:31 北・2:20 南・3:00 西・4:02 合わさる〉・地＝実写 写真 [29] を暗く） ／ P1ES¶2.11（`the fire starts to spread to the north elevation of the tower`…`Flames start to spread to south elevation`…`Fire starts to spread across the west elevation of tower, from north to south`）
> 炎が北の面へ回りはじめたのは、1時31分。南の面へは2時20分。
> 西の面には、3時ごろから、北から南へと広がっていった。

**c413** 🔧 ／ 実写 紙面 P1V2 図13.1（2:00 の冠の炎＝東の面の柱 C5 の南側・中身は ⑤b で原寸・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「冠に広がる炎〈2:00〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図13.1（2019）」） ／ P1ES¶2.11（`Flames travel across the north and east elevations of the tower, and start to spread around the crown and diagonally across the face of the building`）
> 2時には、炎は北と東の面を横切り、冠に沿って広がりながら、
> 斜めに、建物の面を横切りはじめていた。

**c414** 🔧 ／ 実写 紙面 P1V2 図12.7（2:05 のころ、東の面に水をかけるはしご車・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「東の面のはしご車〈2:05〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図12.7（2019）」） ／ P1V2¶12.22（`turntable ladder had been set up with a water supply on the east side of the tower`）・P1V4¶28.133（`could reach a maximum height of 32 metres, which meant that they could not reach beyond floor 10 of the tower`）
> 東の面には、はしご車が水をかけた。だが報告によれば、ロンドン消防のはしごは、
> 最大で32メートル。塔の10階より上には、届かなかった。

**c415** ／ 実写 写真 [2]（青空の下、煙を上げる塔〈遠景〉・BY-SA 4.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・副題「朝の空に上る煙〈2017年6月14日〉」・出典の行「Wikimedia Commons（CC BY-SA 4.0）」） ／ P1ES¶2.11（`Fire spreads horizontally across the south elevation at the crown`…`Flames continue to spread across the south and west elevations of the tower`）
> Q: 塔の上の方には、はしごが届かなかったんだね。
> そう。2時50分には、南の面の冠を、炎が横に走った。
> 3時半になっても、南と西の面で、燃え広がりが続いた。

**c416** 🔧 ／ 実写 公的 P1V4 ¶28.3 の頁（PDF p96・額装・訳の札「燃える外装が付けられたことを、消防は知らされていなかった」〈専門家の言葉の引用と札に書く〉・出典の行「グレンフェル・タワー調査 第1段階の報告 第4巻 ¶28.3（2019）」） ／ P1V4¶28.3（`the fire brigade had never been informed that a combustible rainscreen system had been installed in the first place`）
> 報告は、専門家の言葉も引いている。燃える外装が付けられたことを、
> そもそも消防は知らされていなかった、と。

**c417** 🔧 ／ 実写 紙面 P1V3 図17.3（3:28 のコマ＝窓の下の板から、まだ燃えていなかった所に火が出る・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「下の階に出た新しい火〈3:28〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第3巻 図17.3（2019）」） ／ P1V3¶17.4（`caused fires to break out on previously uninvolved external areas`）
> 3時半ごろの写真には、燃えながら落ちたかけらが窓の下に乗り、
> それまで燃えていなかった所に、新しい火が出る様子が写っている。

**c418** 🔧 ／ 実写 紙面 P1V3 図19.1（4:02 のコマ＝南の面と西の面の炎が西の面の南の角の上で合わさりはじめる〈2つの炎のあいだにまだ小さなすき間〉・中身は ⑤b で原寸・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「合わさりはじめる炎〈4:02〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第3巻 図19.1（2019）」） ／ P1V3¶19.1（`began converging at the top of the southern corner of the west face`）・P1ES¶2.11（`Fires on the south and west elevations start to converge at the top of the southern corner of the west face`）
> 4時2分。南の面と西の面の炎が、2つの面の角の上の方で、
> 合わさりはじめた。

**c419** 🔧 ／ 図 年表（1:09 外壁へ → 1:26 てっぺん → 1:31 北 → 2:00 冠と斜め → 2:20 南 → 3:00 西 → 4:02 合わさる・地＝実写 写真 [29] を暗く） ／ P1ES¶2.13（`It then spread around the top of the building in both directions and down the sides until the advancing flame fronts converged on the west face near the south-west corner, enveloping the entire building in under three hours`）
> 報告によれば、炎は、台所から外壁へ移ってから、
> 3時間足らずで、建物をまるごと包んだ。

**c420** ／ 実写 写真 [31]（焼けた塔〈縦〉・BY-SA 2.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・中身は ⑤b で原寸・副題「焼けた塔〈2017年6月18日〉」・出典の行「Wikimedia Commons（CC BY-SA 2.0）」） ／ P1ES¶2.14（`effective compartmentation was lost at an early stage`）
> Q: 塔の中は、どうなっていたの？
> 外の炎は、次々と部屋の中へ入った。報告は、
> 部屋ごとに火を閉じこめる区画が、早いうちに失われた、と書いている。

**c421** ／ 図 模式（区画が崩れたわけ＝熱で窓のガラスが割れる・台所の換気扇の箱がゆがんで外れる・閉じない防火の扉・地＝実写 写真 [62] を暗く） ／ P1ES¶2.14（`The intensity of the heat was such that the glass in the windows inevitably failed, allowing the fire to penetrate flats`…`Extractor fan units in the kitchens had a propensity to deform and become dislodged, providing a point of entry`）
> 熱で、窓のガラスは割れた。台所の換気扇の箱は、ゆがんで外れやすく、
> そこが火の入り口になった。

**c422** 🔧 ／ 図 模式（防火の扉の札＝自動で閉じる仕掛けが働かず開いたまま・消防が入るために壊した扉・ホースなどではさまれた階段の扉・地＝実写 写真 [62] を暗く） ／ P1ES¶2.14（`Some were left open and failed to close because they lacked effective self-closing devices`…`others were broken down by firefighters or wedged open with firefighting equipment`）・P1V4¶24.36（`some doors to flats had to be broken down to enable firefighters to gain entry`）
> 防火の扉には、煙を食い止めたものもあった。だが、
> 自動で閉まる仕掛けが働かず、開いたままの扉や、消防が入るために壊した扉もあった。

**c423** 🔧 ／ 図 帯（廊下の煙の帯＝1:20 ごろ多くの廊下に煙・1:40 一部でかなりの煙・2:00 多くの階で濃い煙・地＝実写 写真 [62] を暗く） ／ P1ES¶2.15（`Many lobbies had started to fill with smoke by around 01.20 and some were significantly smoke-logged by 01.40`…`By 02.00 a significant number were heavily smoke-logged`）
> 1時20分ごろには、多くの廊下に、煙が入りはじめていた。
> 2時には、多くの階の廊下が、濃い煙で満ちていた。

**c424** ／ 実写 紙面 P1V2 図11.8（1時40分ごろの塔の写真の続き・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「燃え広がる塔〈1:40ごろ〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第2巻 図11.8（2019）」） ／ P1ES¶2.15（`Until around 01.50 there was less smoke in the stairs; by then 168 people had been able to escape`…`After that time the stairs started to fill with smoke, particularly at lower levels`）
> 1つしかない階段は、1時50分ごろまでは、煙が少なかった。
> そのころまでに、168人が逃げていた。そのあと、階段にも煙が満ちていく。

**c425** 🔧 ／ 実写 紙面 P1V3 図17.4（3:27 のコマ＝窓の下の板から新しい火・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「燃え広がる塔〈3:27〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第3巻 図17.4（2019）」） ／ P1ES¶2.15（`At some levels the smoke was thick and the heat considerable`）
> 階によっては、階段の煙は濃く、熱も、かなりのものだった。

**c426** 🔧 ／ イメージ（フリー素材＝煙の立ちこめる暗い階段〈人は写さない〉・画面に「イメージ」） ／ P1ES¶2.15（`By 02.20 the smoke in the stairs did pose a risk to life, but the stairs were not absolutely impassable to all even after that time`）
> Q: 階段は、もう通れなかったの？
> 2時20分には、階段の煙は、命にかかわるほどになっていた。
> ただ報告は、そのあとも、通れる人はいた、と書く。

**c427** 🔧 ／ 図 棒（逃げた人の数＝1:30 112人・1:50 168人・合わせて227人・その夜塔にいた297人〈数は札にも〉・地＝実写 写真 [29] を暗く） ／ P1V4¶28.14（`A total of 112 people had left the tower in the 35 minutes that followed`）・P1ES¶2.11（`By this time 168 of 297 occupants had escaped`）・P1V1¶1.3（`A total of 227 people in all (residents and visitors) escaped from the tower`）
> 塔にいた297人のうち、外へ逃げられたのは、合わせて227人。

**c428** ／ 実写 写真 [20]（覆われた塔と緑のハート〈2018年7月〉・全画面・副題「火事から1年の塔〈2018年7月〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P1V4¶32.1（`70 people failed to escape from the building and lost their lives`）・P1V1¶1.3（`a child who was stillborn shortly after his mother had escaped`…`Another resident who had escaped from the building`…`died seven months later`）
> 塔から逃げられずに亡くなったのは、70人。母親が逃げたあとに死産となった子と、
> 塔から逃げ、7か月後に亡くなった人を合わせ、亡くなったのは72人になる。

**c429** ／ 実写 写真 [33]（焼けた塔・BY-SA 2.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・中身は ⑤b で原寸・副題「焼けた塔〈2017年7月19日〉」・出典の行「Wikimedia Commons（CC BY-SA 2.0）」） ／ P1ES¶2.11（`the last survivor to leave the tower, is evacuated`）
> 最後に助け出された人が塔を出たのは、朝8時7分。
> 火が出てから、7時間あまりがたっていた。

**c430** ／ 図 模式（1つ目の答えの札＝燃えるプラスチックの芯の板・熱をためる断熱材・火の中で危ないカセットの形・横へ広げた飾りの冠・地＝実写 写真 [29] を暗く） ／ 計（1つ目の問いの答え）
> 1つ目の問いの答えを並べる。芯が燃えるプラスチックの外装の板。
> 熱をためる断熱材。火の中で危ないカセットの形。そして、飾りの冠。

**c431** ／ 実写 映像 #15 焼けた塔B（3:00〜3:50 を4つに割った2つ目・副題「焼けた塔〈2017年7月〉」・出典の行「Wikimedia Commons（CC BY 3.0）」） ／ P1ES¶2.16（`there was compelling evidence that the external walls of the building failed to comply with Requirement B4(1) of Schedule 1 to the Building Regulations 2010`）
> Q: 外壁そのものが、燃えるものだったんだね。
> そう。報告は、外壁は、建物の規則の求めを満たしていなかった、
> と言える強い証拠がある、と書いている。

**c432** ／ 実写 写真 [21]（2018年1月の覆われる前の焼けた塔〈白黒の原本〉・全画面・色は原本のまま・副題「焼けた塔〈2018年1月〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ 計（2つ目の問いへのつなぎ）
> では、炎が塔を包んでいくあいだ、塔の中の人たちは、
> 消防から、どう伝えられていたのか。

---

### 第4章　「部屋で待て」（26カット）

**c501** 🔧 ／ 実写 紙面 P1V1 図7.2（ロンドン消防の指令室の中・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「指令室の中〈報告の図〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第1巻 図7.2（2019）」） ／ P1ES¶2.9（`those calls requiring potentially life-saving fire survival guidance (FSG calls)`）・P1ES¶2.11（`Control room decides to revoke the "stay put" advice and tell all occupants calling 999 to leave the tower`）
> Q: 通報は、誰が受けていたの？
> 999の電話を受けるのは、ロンドン消防の指令室だ。取り残された人には、
> 助かるための助言を伝える。2時35分まで、その助言は「部屋で待て」だった。

**c502** 🔧 ／ 図 模式（国の指針の札＝火が部屋の外へ広がり「部屋で待て」が成り立たなくなったときの避難の計画を、消防が前もって用意する・地＝実写 写真 [35] を暗く） ／ P1ES¶2.17（`National guidance requires fire and rescue services to draw up contingency evacuation plans for dealing with fires in high-rise buildings that spread beyond the compartment of origin causing a "stay put" strategy to become untenable`）
> 「部屋で待て」は、火が、火元の部屋に閉じこめられている間だけ成り立つ。
> 国の指針は、そうでなくなったときの避難の計画を、消防に求めていた。

**c503** ／ 実写 公的 P1V4 ¶28.6 の頁（PDF p97・額装・訳の札「その時点は、早くて1時30分、遅くとも1時50分には来ていた」・出典の行「グレンフェル・タワー調査 第1段階の報告 第4巻 ¶28.6（2019）」） ／ P1V4¶28.6（`That point had been reached by 01.30 at the earliest and by 01.50 at the latest`）
> 報告は、「部屋で待て」をやめ、全員を逃がすと決めるべき時は、
> 早くて1時30分、遅くとも1時50分には来ていた、と書いている。

**c504** ／ 図 時計（文字盤に4つの時刻の札＝1:26 てっぺん・1:30〜1:50 切り替えるべき時・2:35 指令室・2:47 現場・地＝実写 写真 [35] を暗く） ／ P1V4¶28.14（`very top of the building by 01.26`）・P1ES¶2.11（`Control room decides to revoke the "stay put" advice`）・P1V4¶28.6（`by 02.47 when the "stay put" advice was withdrawn`）
> 炎がてっぺんに届いたのが1時26分。指令室が助言を改めたのは2時35分。
> 現場で、「部屋で待て」を取りやめたのは、2時47分だった。

**c505** ／ 図 模式（1:50 の札＝168人が逃げた・階段はまだ通れた・全員を逃がすことだけが命を守る現実の道・地＝実写 写真 [21] を暗く） ／ P1V4¶28.19（`By 01.50 168 of the 297 occupants of the building had escaped`）・P1V4¶28.20（`a full evacuation of the building had become the only realistic way of minimising loss of life and serious injury`）・P1V4¶28.27（`at least up to 01.50 the stairs remained passable`）
> 1時50分の時点で、逃げていたのは168人。階段は、まだ通れた。
> 報告は、もう全員を逃がすことだけが、命を守る現実の道だったと書く。

**c506** ／ 図 模式（最初の現場の指揮者の札＝経験はある・階級は高くない・台所の火への出動・名前なし・地＝実写 写真 [21] を暗く） ／ P1ES¶2.19（`the first incident commanders, although experienced, were of relatively junior rank`）・P1V4¶28.4（`wholly outside his experience and training`）
> Q: どうして、そこで切り替えなかったの？
> 最初の現場の指揮者は、経験はあったが、階級は高くなかった。
> 呼ばれたのは台所の火で、そのあとの火の広がりは、経験と訓練の、まったく外だった。

**c507** ／ 図 模式（指揮者の考えの外にあった2つの札＝区画が全体で崩れる・大勢をまとめて逃がす・地＝実写 写真 [35] を暗く） ／ P1ES¶2.19（`None of them seem to have been able to conceive of the possibility of a general failure of compartmentation or of a need for mass evacuation`）
> 報告によれば、最初の指揮者たちは、区画が全体で崩れることも、
> 大勢を一度に逃がすことも、思い描けていなかったようだ。

**c508** ／ イメージ（フリー素材＝並んだ防火服とヘルメット〈顔なし・紋章と字は見せない〉・画面に「イメージ」） ／ P1V4¶28.54（`the "stay put" concept had become an article of faith within the LFB so powerful that to depart from it was to all intents and purposes unthinkable`）
> ロンドン消防で、「部屋で待て」は、疑わずに信じる教えのようになっていたとみられる。
> 報告は、そこから離れることは、考えられないほどだったと書く。

**c509** ／ 図 模式（訓練の札＝いつ避難に切り替えるかの見きわめ方・避難の進め方＝どちらも教わっていない・地＝実写 写真 [35] を暗く） ／ P1V4¶28.45（`it was due to deficiencies in his training which failed to equip him with the means of deciding when to switch from the "stay put" strategy to one of partial or total evacuation`）・P1ES¶2.18（`LFB incident commanders had received no training in how to recognise the need for an evacuation or how to organise one`）
> Q: 指揮者の力が、足りなかったの？
> 報告は、個人の力ではなく、訓練の欠けだと書く。いつ避難に切り替えるか、
> どう避難させるかを、指揮者たちは、教わっていなかった。

**c510** ／ 実写 公的 P1ES ¶2.18 の頁（PDF p10〜p11・額装・訳の札「グレンフェル・タワーの避難の計画は無かった」・出典の行「グレンフェル・タワー調査 第1段階の報告 要約 ¶2.18（2019）」） ／ P1ES¶2.18（`There was no contingency plan for the evacuation of Grenfell Tower`…`had received no training in the particular dangers associated with combustible cladding`）
> この塔の避難の計画は、無かった。燃える外壁の危険についての訓練も、
> 現場の指揮者や幹部は、受けていなかった。

**c511** ／ 図 模式（情報の流れ＝指令室に入る通報の数と部屋・塔の中の火の広がり・警察のヘリの映像 → 現場の指揮者に届かない・地＝実写 写真 [35] を暗く） ／ P1ES¶2.19（`No systematic arrangements were made for information about the number and source of FSG calls to be communicated to the incident commanders`…`pictures from the police helicopter were not available to them`）
> 指令室に入る通報の数や、どの部屋からかを、現場の指揮者に伝える仕組みも無かった。
> 警察のヘリの映像も、指揮者には届いていなかった。

**c512** 🔧 ／ 図 流れ（現場の指揮者の交代の札＝1:50・1:58・2:04・2:11・2:44〈立場だけ・名前なし〉・地＝実写 写真 [35] を暗く） ／ P1ES¶2.11（`hands over incident command to`…`not knowing that`…`has already assumed command`…`takes handover from`）
> 1時50分から2時11分のあいだに、現場の指揮者は、何度も替わった。
> その途中、別の幹部が、すでに指揮者がいると知らずに、指揮を名乗った。

**c513** ／ イメージ（フリー素材＝夜の高層住宅の窓の明かり〈遠景・建物を特定できない〉・画面に「イメージ」） ／ P1V4¶28.74（`at or shortly after 02.00 that the "stay put" advice should be revoked and a full evacuation ordered`）
> 2時ごろ、現場の幹部の中には、「部屋で待て」をやめ、全員を逃がすべきだと、
> 意見を出した人もいた。だが、その意見は検討されなかった、と報告は書く。

**c514** 🔧 ／ 実写 公的 P1V4 ¶28.63 の頁（PDF p111・額装・訳の札「2時までに避難の命令が出ていれば、亡くなる人は、まず間違いなく、より少なかった」・出典の行「グレンフェル・タワー調査 第1段階の報告 第4巻 ¶28.63（2019）」） ／ P1V4¶28.63（`I have little doubt that fewer people would have died if the order to evacuate had been given by 02.00`）
> Q: もっと早く逃がしていたら？
> 報告は、2時までに避難の命令が出ていれば、亡くなる人は、
> まず間違いなく、より少なかった、と書く。

**c515** ／ イメージ（フリー素材＝電話の受話器とヘッドセット〈顔なし〉・画面に「イメージ」） ／ P1V4¶28.75（`taken at around 02.35`…`nowhere in the building could be regarded as a place of safety and that the "stay put" advice should be revoked`）
> 2時35分。指令室の幹部たちは、塔の中に、もう安全な所は無いと判断し、
> 電話をかけてきた人全員に、外へ出るよう伝えると決めた。

**c516** ／ 実写 写真 [26]（2018年6月の焼けた塔〈縦〉・BY-SA 2.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・中身は ⑤b で原寸・副題「塔〈2018年6月〉」・出典の行「Wikimedia Commons（CC BY-SA 2.0）」） ／ P1ES¶2.11（`takes over incident command from`…`revokes the "stay put" advice`）
> 2時44分、より上の幹部が、現場の指揮を引き継いだ。
> そして2時47分、「部屋で待て」は、取りやめられた。

**c517** ／ 図 時計（文字盤＝遅くとも1:50 から 2:47 までを塗る・地＝実写 写真 [35] を暗く） ／ P1V4¶28.6（`by 02.47 when the "stay put" advice was withdrawn the best part of an hour had been lost without any evacuation plan having been considered`）
> 報告は、遅くとも1時50分から、2時47分に取りやめるまでに、
> 避難の計画も考えないまま、1時間近くが失われた、と書く。
> Q: 避難の計画が無いまま、時間が過ぎたんだね。

**c518** ／ 図 模式（2:44 の札＝階段の様子が悪くなり、全員をまとめて逃がすのは、もう間に合わない・地＝実写 写真 [21] を暗く） ／ P1V4¶28.77（`it was no longer practicable to carry out a supervised mass evacuation due primarily to the deterioration in conditions in the stairs`）
> そう。2時44分には、階段の様子が悪くなり、全員をまとめて逃がすのは、
> もう間に合わなかった、と報告は書いている。

**c519** 🔧 ／ 図 棒（2:35 より前に逃げた181人・2:35 より後に逃げた46人＝うち 2:53〜8:07 に約36人・地＝実写 写真 [35] を暗く） ／ P1V4¶28.81注72（`The total number of occupants escaping after the control room revoked the "stay put" advice at around 02.35 was 46`）・P1V4¶28.81（`some 36 occupants escaped from the tower between 02.53 and 08.07`）・計（227−46＝181）
> 報告によれば、指令室が助言を改めたあとに、塔から逃げたのは46人。
> そのうち約36人は、2時53分から朝までに逃げた。

**c520** 🔧 ／ 実写 写真 [23]（地下鉄の線路と焼けた塔〈2018年1月・白黒の原本〉・全画面・色は原本のまま・副題「地下鉄と焼けた塔〈2018年1月〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P1ES¶2.19（`The firefighters who attended the tower displayed extraordinary courage and selfless devotion to duty`）・P1V4¶28.1（`displayed enormous courage and selfless devotion to duty`）
> Q: 朝まで、逃げた人もいたんだ。
> 報告は、塔に駆けつけた隊員たちは、並外れた勇気を示し、
> 自分をかえりみずに、務めを果たした、と書いている。

**c521** ／ 図 模式（2つの札＝隊員の勇気と、指揮と作戦の欠け〈前者は後者を覆い隠さない〉・地＝実写 写真 [35] を暗く） ／ P1V4¶28.5（`The bravery and commitment to duty shown by individual firefighters cannot mask or excuse the deficiencies in the command and conduct of operations`）
> ただ報告は、隊員一人ひとりの勇気は、指揮と作戦の欠けを、
> 覆い隠すことも、帳消しにすることもできない、とも書いている。

**c522** 🔧 ／ 実写 衛星 ラカナル・ハウス（ロンドン南部・サザーク区・Google の表示を絵の近くに・副題「ラカナル・ハウス〈現在の衛星写真〉」） ／ P1ES¶2.9（`On 3 July 2009 a fire broke out on floor 9 of Lakanal House, a 14-floor building in Southwark`…`Six people died`）・P2V5¶83.1（`had all been foreshadowed by previous fires, most particularly, the Lakanal House fire on 3 July 2009`）
> 2009年、ロンドン南部の高層住宅、ラカナル・ハウスで火事があった。
> 6人が亡くなった。2024年の報告は、あの夜の消防の失敗は、
> そこで予告されていたと書く。

**c523** 🔧 ／ 実写 公的 P2V5 ¶83.3 の頁（PDF p207・額装・訳の札「指導力の長年の欠け・慢心の文化」・出典の行「グレンフェル・タワー調査 第2段階の報告 第5巻 ¶83.3（2024）」） ／ P2V5¶83.3（`The LFB's failure lay in its inability to implement any effective response`…`a chronic lack of effective leadership, combined with an undue emphasis on process and a culture of complacency`）
> ロンドン消防の失敗は、その教訓を、実際の備えに変えられなかったことだ。
> 報告は、指導力の長年の欠けと、慢心の文化を挙げている。

**c524** 🔧 ／ 図 模式（指令室の訓練の札＝取り残された人への助言の定期の学び直しの訓練＝2009年も2017年も無し・お金の不足が原因と述べた証人はいない・地＝実写 写真 [35] を暗く） ／ P2V5¶83.6（`In 2009, no structured or regular fire survival guidance refresher training was provided by the LFB and this was still the case at the time of the Grenfell Tower fire in 2017`）・P2V5¶83.12（`none of the witnesses from whom we heard told us that insufficient financial or other resources had caused or contributed to the failings`）
> 指令室の、助かるための助言の、定期の学び直しは、2009年も2017年も無かった。
> あの夜の失敗を、お金の不足のせいにした証人はいなかった、と報告は書く。

**c525** ／ 実写 写真 [68]（高速道路から見た塔〈2021年〉・BY-SA 2.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・副題「高速道路から見た塔〈2021年〉」・出典の行「Wikimedia Commons（CC BY-SA 2.0）」） ／ 計（2つ目の問いの答え）
> Q: 隊員の勇気と、組織の備えは、別の話なんだね。
> そう。報告は、隊員の勇気と、組織の失敗を、分けて書いている。

**c526** ／ 実写 映像 #15 焼けた塔C（3:00〜3:50 を4つに割った3つ目・副題「焼けた塔〈2017年7月〉」・出典の行「Wikimedia Commons（CC BY 3.0）」） ／ 計（3つ目の問いへのつなぎ）
> では、外壁の板は、そもそも、誰が、なぜ選んだのか。
> 話は、火事の5年前、2012年にさかのぼる。

---

### 第5章　燃える外壁は、誰が、なぜ選んだのか（30カット）

**c601** 🔧 ／ 図 年表（2012〜2014年の札＝2012 亜鉛の案・2013年2月 アルミへ・2013年9月 喫茶店の会合・2014年3月 元請けと板・2014年4月 管理の組織への説明・2014年7月と9月 区の許可・地＝実写 写真 [35] を暗く） ／ P2V1¶2.73（`eventually an aluminium composite material (ACM), Reynobond 55 PE, was chosen, largely on the grounds of cost`）・P2V1¶2.74（`a series of errors caused by the incompetence of the organisations and individuals involved in the refurbishment`）
> Q: 設計した人が、選んだの？
> 一人が決めたのではない。報告は、2012年から2014年にかけて、
> いくつもの会社と組織の判断が重なっていった流れを追っている。

**c602** ／ 図 流れ（関わった会社と組織の札＝管理の組織 TMO・設計 スタジオE・元請け ライドン・外装の下請け ハーレー・板の加工 CEP・板の製造 アルコニック〈報告が名指しした範囲〉・地＝実写 写真 [35] を暗く） ／ P1V1¶6.3（`The architect for the main refurbishment was Studio E`…`The cladding subcontractor to Rydon was Harley Facades Ltd`）・P1V1¶6.2（`in June 2014 Rydon Maintenance Limited (Rydon) was eventually appointed the design and build contractor`）・P2V1¶2.21（`Arconic Architectural Products manufactured and sold the Reynobond 55 PE rainscreen panels used in the external wall of Grenfell Tower`）
> 設計は、スタジオEという設計事務所。2014年からの元請けは、ライドン。
> 外装はハーレーという会社が請け、板は、アルコニックという会社の製品だった。

**c603** 🔧 ／ 実写 写真 [41]（2018年5月の足場と覆いの工事・BY-SA 4.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・副題「覆いの工事〈2018年5月〉」・出典の行「Wikimedia Commons（CC BY-SA 4.0）」） ／ P2V1¶2.73（`Although Studio E had wanted to use zinc rainscreen panels`）・P2V4¶55.5（`which was considered by the planning officer present to be acceptable`）
> 2012年、設計事務所が望んだのは、亜鉛の板だった。
> 区の都市計画の担当者も、受け入れられる、としていた。

**c604** ／ 図 比べ（亜鉛の板とアルミの板の札＝節約の見込み 2013年1月 25万ポンド → 2月 30万ポンド〈当時の円で約4,300万円〉・地＝実写 写真 [35] を暗く） ／ P2V4¶55.11（`resulting in a potential saving of £250,000`…`costed the saving to be made by using aluminium panels at £300,000`）・換（2013年2月の月平均＝1ポンド 144.08円）
> 2013年の初め、亜鉛をアルミの板に替えれば、費用を減らせる、という案が出た。
> 節約の見込みは、2月には30万ポンド。当時の円で、約4,300万円だ。
> Q: 節約のための、見直しなんだ。

**c605** ／ 図 模式（圧力の札＝管理の組織 TMO → 設計事務所「亜鉛より安い材料を」・地＝実写 写真 [35] を暗く） ／ P2V4¶55.12（`it was under significant pressure from the TMO to specify a cheaper alternative to zinc`）
> 設計事務所は、改修を管理した組織、TMOから、
> 亜鉛より安い材料を選ぶよう、強い圧力を受けていた、と報告は書く。

**c606** 🔧 ／ 図 模式（2013年9月27日の会合の札＝ロンドン橋の近くの喫茶店・設計事務所と、のちの外装の下請け・話の中心は値段と見た目・地＝実写 写真 [35] を暗く） ／ P2V4¶55.22（`at a coffee shop in Hays Galleria near London Bridge to discuss options, costs and technical details for the cladding of Grenfell Tower`…`Harley's clients were frequently forced to use ACM because it was the cheapest product available`）
> 2013年9月、設計事務所と、のちの外装の下請けが、喫茶店で会った。証言では、
> 下請けの側は、客は安いアルミ複合板を選ばざるを得ないことが多い、と伝えた。

**c607** ／ 実写 公的 P2V4 ¶55.23 の頁（PDF p118・額装・訳の札「板の防火の安全は、まったく話されなかった」・出典の行「グレンフェル・タワー調査 第2段階の報告 第4巻 ¶55.23（2024）」） ／ P2V4¶55.23（`price and aesthetics were the dominant considerations`…`the fire safety of the panels was not discussed at all`）
> Q: 燃えるかどうかの話は、出たの？
> 報告は、話の中心は値段と見た目で、板の防火の安全は、
> まったく話されなかった、と書いている。

**c608** 🔧 ／ 図 模式（見た目の札が大きく、防火の札が欠けている〈報告の「まるで見なかった」〉・地＝実写 写真 [35] を暗く） ／ P2V4¶55.32（`Studio E did not investigate the fire performance of any of the proposed rainscreen panels`）・P2V4¶55.33（`everyone involved concentrated on the appearance of the rainscreen panels to the complete exclusion of their fire performance`）
> 設計事務所は、案に出たどの板の防火の性能も、調べなかった。
> 翌年の話し合いでも、みな見た目に集中し、防火は、まるで見なかった。

**c609** ／ 実写 写真 [39]（駅から見た塔〈2024年6月・縦〉・BY-SA 4.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・副題「駅から見た塔〈2024年6月〉」・出典の行「Wikimedia Commons（CC BY-SA 4.0）」） ／ P2V4¶55.28（`Planning permission for the refurbishment`…`on 10 January 2014`…`a requirement that the materials to be used on the external face of the building be approved in writing by RBKC`）
> 2014年1月、区は、改修の計画を許可した。
> 外に使う材料は、あとで区が書面で認める、という条件つきだった。

**c610** ／ 図 模式（入札の札＝3社・どれも予算をこえた・入札の途中で1社だけに見通しが伝わる・地＝実写 写真 [35] を暗く） ／ P2V4¶55.55（`only three tenders had been received and all exceeded the budget as it then stood`）・P2V4¶55.39（`Rydon was given an indication of the likely outcome of the tender process while it was still going on`）
> 元請けを選ぶ入札は3社。どれも、予算をこえていた。
> そして入札の途中で、ライドンにだけ、結果の見通しが伝えられていた。

**c611** 🔧 ／ イメージ（フリー素材＝夜の会議室の机と椅子〈人は写さない〉・画面に「イメージ」） ／ P2V1¶2.72（`although the TMO had received advice from its lawyers that it would be`…`it entered into discussions with Rydon before the procurement process had been completed`）・P2V4¶55.50（`A meeting took place during the evening of Tuesday 18 March 2014`）・P2V4¶55.51（`We do not know exactly what was discussed at the meeting because no record was kept of it`）
> 2014年3月、管理の組織は、入札が終わる前に、ライドンと話し合った。
> 弁護士には、してはいけないと言われていた。3月18日の夜の会合の記録は、無い。

**c612** 🔧 ／ 図 模式（見積りの誤りの札＝ライドンの入札に約21万2,000ポンドの不足〈当時の円で約3,600万円〉・地＝実写 写真 [35] を暗く） ／ P2V4¶55.43（`a shortfall of approximately £212,000 in its costing`）・換（2014年3月の月平均＝1ポンド 170.12円）
> そのころライドンは、自分の入札の見積りの誤りに、気づいていた。
> 足りない額は、約21万ポンドだった。

**c613** 🔧 ／ 図 表（同じ板の削減額の表＝アルミ複合板・リベット留め・2014年3月＝下請け → 元請け 57万6,973ポンド〈約9,800万円〉・元請け → 管理の組織 37万6,175ポンド〈約6,400万円〉・地＝実写 写真 [35] を暗く） ／ P2V4¶55.48（`£576,973`）・換（2014年3月の月平均＝1ポンド 170.12円）
> Q: その足りない分は、どうしたの？
> 外装の下請けは、アルミ複合板をリベットで留めれば、元請けに、
> 約58万ポンド減らせると伝えた。

**c614** 🔧 ／ 図 模式（差の札＝下請けが示した約58万ポンドと、元請けが管理の組織に示した約38万ポンド・差の約20万ポンドで見積りの不足を埋める狙い・地＝実写 写真 [35] を暗く） ／ P2V4¶55.58（`£376,175`）・P2V4¶55.59（`Those figures were all lower than those that Harley had given Rydon on 14 March 2014`…`the purpose was to enable Rydon to retain the difference in order to make up the shortfall caused by the £212,000 error in costing`）
> だが元請けが、管理の組織に示した削減額は、約38万ポンド。
> 差の約20万ポンドを残し、不足を埋める狙いだったと、元請けの社員は遠回しに認めた。

**c615** 🔧 ／ 実写 公的 P2V4 ¶55.72 の頁（PDF p129〜p130・額装・訳の札「議事録がうかがわせるように、この額がハーレーから得られる削減のすべてだと伝わったなら、明らかに偽りで、ライドンは偽りと知っていた」・出典の行「グレンフェル・タワー調査 第2段階の報告 第4巻 ¶55.72（2024）」） ／ P2V4¶55.72（`the TMO was told that there was a potential saving of up to £376,175`…`if, as the minutes tend to suggest, the TMO was given to understand that the sum of £376,175 reflected the full amount of the reduction available from Harley, that was clearly false and was known by Rydon to be false`）
> 報告によれば、議事録は、約38万ポンドが削減のすべてだと伝わった、とうかがわせる。
> 報告は、そうなら明らかに偽りで、元請けは偽りと知っていた、と書く。

**c616** ／ 図 模式（元請けの利益の札＝アルミ複合板を勧めると利益が増える・管理の組織は知らされていない・地＝実写 写真 [35] を暗く） ／ P2V4¶55.72（`Rydon did not tell the TMO that Harley was willing to reduce the cost of the rainscreen by as much as`）・P2V4¶55.60（`The TMO was kept entirely in the dark about Rydon's financial interest in recommending ACM`）
> Q: 下請けが示した額は、伝えなかったの？
> 伝えなかった。アルミ複合板を勧めれば、元請けの利益は増える。
> 管理の組織は、そのことを、まったく知らされていなかった。

**c617** 🔧 ／ 実写 写真 [35]（覆われた塔〈2023年5月〉・全画面・副題「覆いのかかった塔〈2023年5月〉」・出典の行「Wikimedia Commons（CC BY 2.0）」） ／ P2V4¶55.71（`From March 2014 onwards`…`the only product that was proposed for use was Reynobond 55 PE ACM panels`）
> 2014年3月からは、案に出た板は1つだけだった。芯がふつうのポリエチレンの、
> アルコニックの板だ。あとは、色と留め方だけが残った。

**c618** ／ 図 模式（燃えにくい芯の板もあった・下請けは認めた以上に知っていた・地＝実写 写真 [35] を暗く） ／ P2V1¶2.24（`Arconic did not consider withdrawing Reynobond 55 PE in favour of the fire-resistant version then available`）・P2V4¶55.83（`Harley knew more than it was willing to admit about the availability of a fire-resistant version of the Reynobond panel`）
> 同じ製品には、芯が燃えにくい板もあった。報告は、外装の下請けは、
> それを、認めた以上に知っていた、とみている。

**c619** 🔧 ／ 図 模式（区の許可の札＝2014年7月 カセットの留め方を認める・9月 色「スモーク・シルバー」で正式な許可・区が考えたのは見た目と費用と工期・地＝実写 写真 [35] を暗く） ／ P2V4¶55.74（`The appearance and cost of the cladding, together with concerns about the programme, were the only matters considered by the council`）・P2V4¶55.77（`the planning department had approved ACM rainscreen cladding using cassette fixings`…`for those panels in "smoke silver" on 25 September 2014`）
> 区が考えたのは、見た目と、費用と、工期だけだった。区は2014年7月に、
> カセットの留め方を認め、9月に、色も含めて、正式に許可した。

**c620** ／ 実写 紙面 P1V1 図6.8（窓まわりの改修の写真〈報告の図・中身は ⑤b で原寸〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「改修の窓まわり〈報告の図〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第1巻 図6.8（2019）」） ／ P2V4¶55.14（`stated (wrongly) that the panels might be regarded as having a Class 0 surface`）・P2V4¶55.61（`Astonishingly, at no stage of the project did anyone at Rydon, Harley or Studio E examine the certificate with any care`）
> Q: 板が燃えやすいって、誰も気づかなかったの？
> 板の認証の書類は、誤って、表面は燃えにくい等級とみなせる、と書いていた。
> 元請けも下請けも設計事務所も、その書類を、きちんと読まなかった。

**c621** 🔧 ／ 図 模式（前ぶれの札＝2012年1月 ロンドンの別の高層住宅の火事・下請けはアルミ複合板が燃えると知った・地＝実写 写真 [35] を暗く） ／ P2V4¶55.79（`16 January 2012 at Taplow House on the Chalcots Estate`）・P2V4¶55.80（`the fire at Taplow House had demonstrated to Harley that ACM would burn`）
> 前ぶれも、あった。2012年1月、ロンドンの別の高層住宅で、火事が起きた。
> 下請けの側は、この火事でアルミ複合板が燃えると分かった、と調査で認めた。

**c622** 🔧 ／ 実写 公的 P2V4 ¶55.84 の頁（PDF p133・額装・訳の札「火事になれば、アルミ複合板は、すぐに無くなる！」・出典の行「グレンフェル・タワー調査 第2段階の報告 第4巻 ¶55.84（2024）」） ／ P2V4¶55.84（`the ACM will be gone rather quickly in a fire!`）
> 工事中の2015年3月、下請けの社員は、メールにこう書いていた。
> 「火事になれば、アルミ複合板は、すぐに無くなる！」

**c623** 🔧 ／ 図 模式（2014年11月の問いの札＝管理の組織の担当者が、ラカナル・ハウスの火事を引いて「材料は燃えにくい必要があるか」と尋ねる・答えの記録なし・地＝実写 写真 [35] を暗く） ／ P2V4¶55.87（`whether in the light of the fire at Lakanal House there was any requirement for materials to be flame retardant`）・P2V4¶55.89（`no one in the design team gave any consideration to the question she had raised, despite the fact that it was of real importance`）
> Q: 燃えるって、分かっていたんだ。
> 2014年11月には、管理の組織の担当者が、ラカナル・ハウスの火事を引いて、
> 材料は燃えにくい必要があるか、と尋ねた。設計の側は、誰も考えなかったとみられる。

**c624** ／ イメージ（フリー素材＝ビルの外壁の工事と足場〈社名と人の顔は見せない〉・画面に「イメージ」） ／ P2V1¶2.73（`largely on the grounds of cost`）
> Q: じゃあ、安いから選んだ、ってこと？
> 大きな理由は、そうだ。報告は、アルミ複合板は、主に費用のために選ばれた、と書く。

**c625** ／ 実写 公的 P2V1 ¶2.74 の頁（PDF p28・額装・訳の札「関わった組織と人の力不足による、いくつもの誤りの結果」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.74（2024）」） ／ P2V1¶2.74（`The choice of combustible materials for the cladding of Grenfell Tower resulted from a series of errors caused by the incompetence of the organisations and individuals involved in the refurbishment`）
> ただ報告は、燃える材料が選ばれたのは、関わった組織と人の、
> 力の足りなさが生んだ、いくつもの誤りの結果だ、と書いている。

**c626** 🔧 ／ 図 模式（責任のたらい回しの札＝それぞれが、防火は誰かほかの人の責任と思う・防火の技術者に材料のことを尋ねた人はいない・地＝実写 写真 [35] を暗く） ／ P2V1¶2.74（`in each case assumed that someone else was responsible for matters affecting fire safety`）・P2V4¶67.14（`no one asked for advice or confirmation from a fire engineer`）
> どの会社も、防火のことは、誰かほかの人の責任だと思っていた。
> 防火の技術者に、材料のことを尋ねた人は、いなかった。

**c627** ／ 実写 公的 P2V4 ¶67.21 の頁（PDF p323・額装・訳の札「その悲惨な選択の責任を、TMO に負わせることはできない」・出典の行「グレンフェル・タワー調査 第2段階の報告 第4巻 ¶67.21（2024）」） ／ P2V4¶67.21（`the TMO was unduly concerned with reducing costs`…`The decision to choose Reynobond PE was part of a "value engineering" exercise performed at the TMO's insistence and designed to keep costs down`…`cannot be laid at the door of the TMO`）
> 管理の組織は、費用を減らすことに、こだわりすぎた。ただ報告は、
> この悲惨な選択の責任を、管理の組織に負わせることはできない、と書く。

**c628** ／ 図 模式（報告の67章の札＝多くの関係者の深刻な力不足・一部の建材の製造会社の明らかな不正・地＝実写 写真 [35] を暗く） ／ P2V4¶67.13（`a serious lack of competence on the part of many of those engaged on it and, in the case of some manufacturers of construction products, outright dishonesty`）
> 報告は、この改修には、多くの関係者の深刻な力不足と、
> 一部の製造会社の明らかな不正があった、とまとめている。

**c629** ／ 実写 紙面 P1V1 図6.7（窓のまわりの断熱材の板〈2枚の写真〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「窓のまわりの断熱材〈報告の図〉」・出典の行「グレンフェル・タワー調査 第1段階の報告 第1巻 図6.7（2019）」） ／ 計（3つ目の問いの前半の答え）
> Q: 選んだ人たちは、確かめるべきことを、確かめなかったんだね。
> そう。では、その板と断熱材を作り、売った会社は、何を知っていたのか。

**c630** 🔧 ／ 実写 紙面 P2V1 図5.9（大規模な外壁の燃焼試験のようす〈写真〉・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「外壁の燃焼試験〈報告の図〉」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 図5.9（2024）」） ／ P2V1¶2.19（`One very significant reason why Grenfell Tower came to be clad in combustible materials was systematic dishonesty on the part of those who made and sold the rainscreen cladding panels and insulation products`）
> 報告は、塔が燃える材料で覆われた大きな理由の1つを、
> それらの会社の、組織的な不正だ、と書いている。

---

### 第6章　試験をごまかした会社（23カット）

**c701** ／ 実写 公的 P2V1 ¶2.19 の頁（PDF p20・額装・訳の札「試験のやり方を操り、試験の結果を偽って伝え、市場を欺く」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.19（2024）」） ／ P2V1¶2.19（`They engaged in deliberate and sustained strategies to manipulate the testing processes, misrepresent test data and mislead the market`）
> Q: 組織的な不正って、何をしたの？
> 報告によれば、試験のやり方を操り、試験の結果を偽って伝え、
> 市場を欺く。そういう策を、わざと、長く続けていた。

**c702** 🔧 ／ 図 模式（報告が名を挙げた3社の札＝外装の板 アルコニック・断熱材 セロテックス・断熱材 キングスパン・地＝実写 写真 [72] を暗く） ／ P2V1¶2.21（`Arconic Architectural Products manufactured and sold the Reynobond 55 PE rainscreen panels`）・P2V1¶2.28（`Celotex manufactured RS5000, a combustible polyisocyanurate foam insulation`）・P2V1¶2.41（`one of the insulation products used on Grenfell Tower, Kingspan K15`）
> 報告が名指ししたのは、外装の板のアルコニックと、
> 断熱材のセロテックス、キングスパンの3社。まず、板の会社からだ。

**c703** ／ 図 模式（同じ板の2つの形＝リベット留めの平らな板とカセット・カセットは火にとても危ない反応〈2005年の初めの試験〉・地＝実写 写真 [72] を暗く） ／ P2V1¶2.22（`from early 2005 Arconic had been in possession of test data showing that in its cassette form the product reacted to fire in a very dangerous way`）
> アルコニックは、2005年の初めには、カセットの形の板が、
> 火にとても危ない反応をするという、試験の結果を持っていた。

**c704** 🔧 ／ イメージ（フリー素材＝積み重ねたアルミの板〈社名と字は見せない〉・画面に「イメージ」） ／ P2V1¶2.22（`Arconic persisted in telling the market that the panels had been classed B-s2, d0 without drawing any distinction between the cassette and riveted forms`）・P2V1¶2.21（`From 2005 until after the Grenfell Tower fire Arconic deliberately concealed from the market the true extent of the danger of using Reynobond 55 PE in cassette form`）
> それでも、留め方の違いを言わずに、板の等級を伝え続けた。
> 報告は、危険の大きさを、2005年から火事のあとまで、わざと隠した、と書く。

**c705** 🔧 ／ 図 模式（規制が弱いと見た国〈イギリスを含む〉へ、カセットの形のまま売る・地＝実写 写真 [72] を暗く） ／ P2V1¶2.23（`it was determined to exploit what it saw as weak regulatory regimes in certain countries (including the UK) to sell Reynobond 55 PE in cassette form`）
> Q: わざと隠した、なんて。
> 報告によれば、イギリスなどの、弱いと見た規制につけこみ、
> カセットの形の板を、住宅にも売ると決めていた。

**c706** ／ イメージ（フリー素材＝夜の都市の高層ビル群〈特定の建物は見せない〉・画面に「イメージ」） ／ P2V1¶2.24（`Despite the knowledge gained from cladding fires in Dubai in 2012 and 2013, Arconic did not consider withdrawing Reynobond 55 PE in favour of the fire-resistant version then available`）
> 2012年と2013年には、ドバイで、外装の火事が続いた。それでもアルコニックは、
> 芯が燃えにくい板に切り替えようとは、しなかった。

**c707** 🔧 ／ 図 模式（等級の札＝2013年の試験のあと、自ら等級を燃えやすい方のEにすると決める・イギリスの客と認証の機関に、わざと伝えない・地＝実写 写真 [72] を暗く） ／ P2V1¶2.25（`Following further testing in 2013, Arconic decided that Reynobond 55 PE would be certified as Class E only, whether used in riveted or cassette form`…`it did not pass that information to its customers in the UK or to the BBA`…`That was not an oversight`）
> 2013年の試験のあと、アルコニックは、板の等級を、
> 燃えやすい方のEにすると決めた。だが、わざと、そのことを、
> イギリスの客にも、製品の証明書を出す認証の機関にも、伝えなかった。

**c708** 🔧 ／ 図 模式（証明書の札＝留め方を分けない証明書・カセットの形の試験の結果は渡さない・地＝実写 写真 [72] を暗く） ／ P2V1¶2.27（`Arconic persuaded the BBA to issue a certificate that drew no distinction between the different forms of fixing`…`It concealed important information from the BBA, in particular the test data relating to the product in cassette form`）
> さらに認証の機関に、留め方を分けない証明書も出させていた。
> カセットの形の試験の結果は、認証の機関にも、隠していた。

**c709** ／ イメージ（フリー素材＝断熱材の板の束〈社名と字は見せない〉・画面に「イメージ」） ／ P2V1¶2.28（`In an attempt to break into the market for insulation suitable for use on high-rise buildings`…`Celotex embarked on a dishonest scheme to mislead its customers and the wider market`）
> Q: 断熱材の会社は？
> セロテックスは、高い建物に使える断熱材の市場に入りこもうとして、
> 客と市場を欺く、不正なたくらみに乗り出した。

**c710** 🔧 ／ 実写 紙面 P2V1 図5.8（大規模な外壁の燃焼試験の装置の図と写真・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「燃焼試験の装置〈報告の図〉」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 図5.8（2024）」） ／ P2V1¶2.29（`in May 2014 Celotex tested in accordance with BS 8414 a system incorporating RS5000 that contained two sets of fire-resistant magnesium oxide boards placed in critical positions to ensure that it passed`）
> 2014年5月、セロテックスは、試験用に組んだ外壁を燃やす大規模な試験を受けた。
> その壁の大事な所には、合格させるために、燃えにくい板が2組、仕込まれていた。

**c711** ／ 実写 公的 P2V1 ¶2.29 の頁（PDF p21・額装・訳の札「その板について何も書かない、試験の報告」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.29（2024）」） ／ P2V1¶2.29（`It then obtained from BRE a test report that omitted any reference to the magnesium oxide boards`）・P2V1¶2.19（`the Building Research Establishment (BRE) was complicit in that strategy`）
> 試験の結果の書類には、その燃えにくい板のことが、書かれなかった。
> 報告は、試験をした機関も、このたくらみに加わっていた、と書く。

**c712** 🔧 ／ 図 模式（試験の機関の札＝1921年 国の機関として始まる・1991年から 外壁の防火の試験の仕事の多くが、ずさんで科学として甘い・地＝実写 写真 [72] を暗く） ／ P2V1¶2.11（`had been established in 1921 as a government body`）・P2V1¶2.15（`However, from 1991 much of the work it carried out in relation to testing the fire safety of external walls was marred by unprofessional conduct, inadequate practices, a lack of effective oversight, poor reporting and a lack of scientific rigour`）
> Q: 試験をする側まで、なんだ。
> その機関は、もとは国の研究所だった。報告は、
> 1991年からの外壁の試験の仕事の多くが、ずさんで、科学として甘かった、と書く。

**c713** ／ イメージ（フリー素材＝建材の売り込みの冊子とカタログ〈社名と字は見せない〉・画面に「イメージ」） ／ P2V1¶2.30（`"the first PIR board to successfully test to BS 8414"`…`"acceptable for use in buildings above 18 metres in height"`）
> セロテックスは、その結果を使い、高さ18メートルをこえる建物に使える、
> この種類の断熱材で初めて試験に合格した、と売り出した。

**c714** ／ 図 模式（勧めの札＝外装の下請けに「この塔にふさわしく安全」と勧める・そうでないと知りながら・地＝実写 写真 [72] を暗く） ／ P2V1¶2.31（`Celotex presented RS5000 to Harley as suitable and safe for use on Grenfell Tower, although it knew that was not the case`）
> そして外装の下請けに、この塔に使うのに、ふさわしく安全な材料だ、と勧めた。
> そうではないと、知りながらだ。

**c715** ／ 図 模式（キングスパンの札＝2005年から調査が始まったあとまで、18メートルをこえる建物の断熱材に偽りの市場・地＝実写 写真 [72] を暗く） ／ P2V1¶2.32（`From 2005 until after this Inquiry had begun, Kingspan knowingly created a false market in insulation for use on buildings over 18 metres in height`）
> もう1社のキングスパンは、2005年から、この調査が始まったあとまで、
> 高い建物に使える断熱材だと、偽って売り込んでいた、と報告は書く。

**c716** ／ 図 模式（頼った試験の札＝2005年の1回の試験・2006年に中身を変えたことは言わない・2007年と2008年の試験はひどい結果・地＝実写 写真 [72] を暗く） ／ P2V1¶2.33（`relied on the results of a single BS 8414-1 test performed in 2005`…`without disclosing that it had changed the composition of the product in 2006`…`Tests performed in 2007 and 2008 on systems incorporating the then current form of K15 were disastrous`）
> 頼ったのは、2005年の、1回の試験の結果。2006年に製品の中身を変えたことは、
> 伝えなかった。2007年と2008年の試験は、ひどい結果だった。

**c717** 🔧 ／ イメージ（フリー素材＝工場に積まれた断熱材の板〈社名と字は見せない〉・画面に「イメージ」） ／ P2V1¶2.37（`Kingspan did not use the product currently on the market but used modified or trial versions`…`continued to do so until October 2020`）
> Q: それでも、売り続けたの？
> 売り続けた。報告は、売り物と違う、試作などの品の試験の結果を不正に使い、
> 2020年10月まで、高い建物向けに売っていた、と書く。

**c718** 🔧 ／ 図 模式（認証の機関の札＝製品の証明書を出す2つの機関は、証明書の中身を確かめない・それを見守る機関は、監督が不十分・地＝実写 写真 [72] を暗く） ／ P2V1¶2.20（`failed to ensure that the statements in their product certificates were accurate and based on test evidence`…`standards of monitoring and supervision`）
> 製品を確かめるはずの認証の機関も、働かなかった。証明書の中身が正しく、
> 試験の証拠に基づくかを、確かめていなかった。

**c719** ／ 実写 公的 P2V2 ¶29.48 の頁（PDF p223・額装・訳の札「客に合わせ、証明書を信じる人を損なう」・出典の行「グレンフェル・タワー調査 第2段階の報告 第2巻 ¶29.48（2024）」） ／ P2V2¶29.48（`it was willing to accommodate the customer at the expense of those who relied on the certificates`）
> 報告によれば、ある認証の機関は、客に合わせるためなら、
> 証明書を信じて使う人の側が損をすることも、いとわなかった。

**c720** 🔧 ／ 実写 紙面 P2V1 図5.2（小さな試料の燃焼試験〈表面の炎の広がり〉のようす・紙面の引用＝図の番号と題の行ごと・額装・無加工・副題「表面の炎の広がりを見る試験〈報告の図〉」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 図5.2（2024）」） ／ P2V1¶2.121（`The use of Class 0 as a standard of fire performance for products to be used on the external wall of tall buildings was wholly inappropriate`）
> Q: 燃えにくさの等級は、どうやって決めていたの？
> イギリスの指針は、小さな試料を燃やす試験の「クラス0」という等級を、
> 高い建物の外壁の板にも使っていた。報告は、まったくふさわしくなかったと書く。

**c721** ／ 図 模式（小さな試料の試験と、建物の外で広がる火＝試験では分からない・地＝実写 写真 [72] を暗く） ／ P2V1¶2.121（`Neither of the main British Standard tests relevant to that classification reflected the development of a fire on the outside of a building or provided the information needed to assess how an external wall incorporating the product would perform in a fire`）
> 小さな試料の試験は、建物の外で火がどう広がるかを、映していなかった。
> 外壁に使ったときに、どう燃えるかを見きわめる情報も、与えなかった。

**c722** 🔧 ／ 図 模式（仕組みの札＝作る・売る・試す・認める・見守る＝ばらばら・まとめられるのは国だけ・地＝実写 写真 [72] を暗く） ／ P2V2¶29.58（`that system lacked the degree of integration required`）・P2V2¶29.59（`That is a task that only the government can undertake.`）
> Q: 売る側だけの話じゃ、なかったんだね。
> そう。報告は、仕組み全体の失敗とし、それを取りまとめられるのは国だけだと書く。

**c723** ／ 実写 写真 [59]（2024年8月の覆われた塔と工事の囲い・CC0・全画面・副題「覆われた塔〈2024年8月〉」・△ 追悼の掲示に名前と顔が写らないかを ⑤b で原寸＝写れば替える・出典の行「Wikimedia Commons（CC0）」） ／ P2V1¶2.5（`by 2016 the department was well aware of those risks, but failed to act on what it knew`）
> では、国は、何を知っていたのか。報告は、2016年までに、国の省は、
> その危険をよく知りながら、動かなかったと書いている。

---

### 第7章　国は知っていた（20カット）

**c801** ／ 実写 公的 P2V1 ¶2.5 の頁（PDF p17・額装・訳の札「1991年から2017年まで、危険に気づく機会は何度もあった」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.5（2024）」） ／ P2V1¶2.5（`In the years between the fire at Knowsley Heights in 1991 and the fire at Grenfell Tower in 2017 there were many opportunities for the government to identify the risks posed by the use of combustible cladding panels and insulation`）
> Q: 国は、いつから知っていたの？
> 報告は、1991年の、ある高層住宅の火事から話を始める。そこから2017年まで、
> 燃える外装の危険に気づく機会は、国に、何度もあった、と。

**c802** ／ イメージ（フリー素材＝ロンドンの議会の建物〈遠景〉・画面に「イメージ」） ／ P2V1¶2.5（`it failed to heed the warning of the Environment and Transport Select Committee in December 1999 that it should not take a serious fire in which people were killed before steps were taken to minimise the risks posed by some external cladding systems`）
> 1999年12月、議会の委員会は、国に警告していた。
> 人が亡くなる大きな火事が起きるのを待ってから、
> 外装の危険に手を打つのでは、いけない、と。

**c803** 🔧 ／ 図 模式（1999年の委員会の勧め＝外壁は大規模な試験で確かめる・小さな試験の等級はやめる・地＝実写 写真 [23] を暗く） ／ P2V1¶2.5（`It also failed to implement or keep under review the committee's recommendation that the large-scale test that had recently been developed should be substituted in Approved Document B`）・P2V2¶29.5（`Unfortunately, that warning was ignored`）
> 報告は、その警告は、聞き流された、と書いている。
> 委員会は、外壁は、大規模な試験で確かめるべきだ、とも勧めた。
> Q: 前から、言われていたんだ。

**c804** ／ 図 模式（2001年の大規模な試験＝芯がふつうのポリエチレンのアルミ複合板は激しく燃えた・結果は公表されず・地＝実写 写真 [23] を暗く） ／ P2V1¶2.6（`the striking results of a large-scale test in 2001 involving aluminium composite panels with unmodified polyethylene cores, which burned violently`…`It failed even to publish the results of the test`）
> 2001年の大規模な試験で、芯がふつうのポリエチレンのアルミ複合板は、
> 激しく燃えた。だが国の省は、その結果を、公表することさえしなかった。

**c805** ／ 実写 公的 P2V1 ¶2.7 の頁（PDF p18・額装・訳の札「小さな試験の等級は外壁にふさわしくないと、何度も知らされていた」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.7（2024）」） ／ P2V1¶2.7（`On many subsequent occasions the department was made aware that national Class 0 was an inappropriate standard by which to determine the suitability of external wall panels but allowed it to remain as part of the statutory guidance until after the Grenfell Tower fire`）
> 小さな試験の等級は、外壁の板にはふさわしくない。国の省は、
> そう何度も知らされながら、火事のあとまで、指針に残し続けた。

**c806** 🔧 ／ イメージ（フリー素材＝ロンドンの古い高層住宅の遠景〈特定できない〉・画面に「イメージ」） ／ P1V1¶8.1（`Six people died in the fire, three of whom were children`）・P2V1¶9.41（`On 28 March 2013, the coroner wrote a letter to the`）・P2V1¶2.12（`Following the fire at Lakanal House the coroner recommended that Approved Document B be reviewed`）
> 2009年のラカナル・ハウスの火事では、6人が亡くなり、
> そのうち3人は、子どもだった。死因を調べる検死官は、
> 2013年、国に、指針を見直すよう勧めた。

**c807** 🔧 ／ 図 模式（検死官の勧め → 国の省＝急ぐべきこととして扱わない・慢心し、ときに守りに入る・地＝実写 写真 [23] を暗く） ／ P2V1¶2.12（`her recommendations were not treated with any sense of urgency`…`The department displayed a complacent and at times defensive attitude to matters affecting fire safety`）
> だがその勧めは、急ぐべきこととして扱われなかった。報告は、国の省の態度を、
> 慢心し、ときに、守りに入っていた、と書く。

**c808** ／ 実写 公的 P2V1 ¶2.13 の頁（PDF p19・額装・訳の札「命の安全にかかわることまで、無視され、先送りされ、顧みられなかった」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.13（2024）」） ／ P2V1¶2.13（`the government's deregulatory agenda`…`dominated the department's thinking to such an extent that even matters affecting the safety of life were ignored, delayed or disregarded`）
> Q: どうして、急がなかったの？
> そのころ政府は、規制を減らす方針を、強く進めていた。報告は、
> 命の安全にかかわることまで、無視され、先送りされ、顧みられなかった、と書く。

**c809** 🔧 ／ イメージ（フリー素材＝夜の高層ビル群の遠景〈特定できない〉・画面に「イメージ」） ／ P2V1¶2.9（`Between 2012 and 2017 the department received numerous warnings about the risks involved in using polymeric insulation and aluminium composite panels with unmodified polyethylene cores`…`It also became aware of several major cladding fires abroad`）
> 2012年から2017年にも、警告は、何度も国に届いた。
> 国は、海外の、外装が燃える大きな火事も、いくつも知っていた。

**c810** 🔧 ／ 図 模式（2016年2月の懸念＝高い建物で、燃える断熱材とアルミ複合板が、規則に反して当たり前に使われている・地＝実写 写真 [23] を暗く） ／ P2V1¶2.9（`by February 2016 it had become aware that some in the industry were worried that combustible insulation and aluminium composite material (ACM) panels with unmodified polyethylene cores were routinely being used on high-rise buildings in breach of functional requirement B4`）
> 2016年2月には、高い建物で、燃える断熱材とアルミ複合板が、
> 規則に反して当たり前に使われている、という業界の一部の懸念も、届いていた。

**c811** ／ 図 模式（問い合わせの札＝ある会社から国の担当の役人へ・アルミ複合板を張った18メートルをこえる英国の建物は、どれも規則を満たしていない・地＝実写 写真 [23] を暗く） ／ P2V1¶11.71（`none of the existing buildings in the UK over 18 metres in height that were clad in aluminium composite panels currently met functional requirement B4`）
> その月、ある会社が、国の担当の役人に知らせた。アルミ複合板を張った、
> 18メートルをこえる英国の建物は、どれも規則を満たしていない、と。

**c812** ／ 実写 公的 P2V1 ¶11.71 の頁（PDF p202・額装・訳の札「うわべだけで、急いだ、役に立たない答え」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 ¶11.71（2024）」） ／ P2V1¶11.71（`superficial, hurried and unhelpful response to a serious question that required careful thought was clearly inadequate`）・P2V1¶2.10（`He failed to bring to the attention of more senior officials the serious risks of which he had become aware`）
> 担当の役人の返事を、報告は、うわべだけで、急いだ、役に立たない答えと書く。
> 役人は、その危険を、上の役職の人たちに、伝えなかった。

**c813** 🔧 ／ イメージ（フリー素材＝砂漠の都市の高層ビル群〈特定の建物は見せない〉・画面に「イメージ」） ／ P2V1¶11.77（`the fire at the Address Downtown on 31 December 2015`…`He asked whether similar panels were used in the UK and whether there was a risk of a similar fire occurring in this country`…`The honest response would have been that the risk did exist`…`gave the same response as he had given to`）
> 同じ月、構造の安全を見る団体も、ドバイの高層ビルの火事を受けて、
> 似た板が英国で使われているか、似た火事の危険はあるかと尋ねた。報告は、
> 正直な答えは「危険はある」だったが、返事は前と同じだった、と書く。

**c814** 🔧 ／ 図 模式（ひとりの役人の札＝建物の規則と指針の日々の担当・上の監督が足りない・地＝実写 写真 [23] を暗く） ／ P2V1¶2.10（`It was a serious failure to allow such an important area of activity to remain in the hands of one relatively junior official`）
> Q: そんな大事なことを、誰が受けていたの？
> 報告は、命にかかわる分野を、比較的下の役職の、
> ひとりの役人に任せていたこと自体が、重大な失敗だった、と書く。

**c815** ／ 図 模式（国の指針の札＝外壁の防火の指針に根本的な欠陥・地＝実写 写真 [23] を暗く） ／ P2V1¶2.120（`the statutory guidance on complying with functional requirement B4(1) of the Building Regulations was fundamentally defective`）
> 報告は、外壁の防火について、国の公式の指針そのものに、
> 根本的な欠陥があった、とも書いている。

**c816** 🔧 ／ 実写 写真 [60]（2024年8月の工事の囲いと掲示〈縦〉・CC0・高さいっぱい＋同じ写真のぼかしの地・副題「工事の囲いと塔〈2024年8月〉」・△ 掲示に名前と顔が写らないかを ⑤b で原寸＝写れば替える・出典の行「Wikimedia Commons（CC0）」） ／ P2V2¶29.21（`only a major fire in a high-rise building leading to a large number of casualties would prompt it to take the necessary action`）
> 報告は、国の省は、大勢の死傷者を出す高層の火事が起きるまで、
> 必要な手を打たないおそれが強かった、とまで書いている。

**c817** ／ 実写 公的 P2V2 ¶29.21 の頁（PDF p217・額装・訳の札「政府は、仕組みの失敗に責任を負わなければならない」・出典の行「グレンフェル・タワー調査 第2段階の報告 第2巻 ¶29.21（2024）」） ／ P2V2¶29.21（`The government must take responsibility for the systemic failures that played a significant part in enabling the Grenfell Tower fire to occur`）
> そして、政府は、この火事が起きるのに大きな役割を果たした仕組みの失敗に、
> 責任を負わなければならない、と結んでいる。

**c818** ／ 実写 写真 [58]（2024年8月の覆われた塔〈縦〉・CC0・高さいっぱい＋同じ写真のぼかしの地・副題「覆われた塔〈2024年8月〉」・△ 追悼の壁に名前と顔が写らないかを ⑤b で原寸＝写れば替える・出典の行「Wikimedia Commons（CC0）」） ／ 計（第7章のまとめ）
> Q: 人が亡くなる前に、という警告が、当たってしまったんだね。
> そう。報告は、警告を受けても動かなかった国の省の姿を、細かく書き残している。

**c819** ／ 図 模式（警告と火事の並び＝1991・1999・2001・2009・2013・2016 の札〈年は札の中〉・地＝実写 写真 [20] を暗く） ／ 計（P2V1 ¶2.5〜¶2.12 と ¶11.71〜¶11.77 の年）
> 1991年、1999年、2001年、2009年、2013年、そして2016年。
> 警告と火事は、くり返されていた。

**c820** ／ 実写 映像 #15 空撮B（0:25〜2:40 のうち新しい高層住宅の並ぶ区間・副題「ロンドンの空撮〈2017年7月〉」・出典の行「Wikimedia Commons（CC BY 3.0）」） ／ 計（第8章へのつなぎ）
> 次の章では、この火事について、よく言われる話を、報告に当ててみる。

---

### 第8章　よく言われる話を、報告に当てる（13カット）

**c901** 🔧 ／ 図 模式（「よく言われる話 → 報告」の札の型〈事実の図と見た目を分ける〉・地＝実写 写真 [20] を暗く） ／ 計（第8章の型）
> Q: この火事には、よく言われる話も、多いの？
> 多い。中には、報告と食い違う話もある。

**c902** 🔧 ／ 実写 公的 P2V4 ¶63.10 の頁（PDF の頁は ⑤b で＝段落で探す・額装・訳の札「外壁は、規則の求めを満たしていなかった」・出典の行「グレンフェル・タワー調査 第2段階の報告 第4巻 ¶63.10（2024）」） ／ P2V4¶63.10（`As a consequence, the external wall did not comply with functional requirement B4(1)`）・P1V4¶26.4（`there is compelling evidence that requirement B4(1) was not met in this case`）
> まず、「当時の規則では、あの外壁は合法だった」という話。
> 報告は、外壁は、建物の規則の求めを、満たしていなかったと結論している。

**c903** 🔧 ／ 図 模式（2つの札＝外壁は規則の求めを満たさない・国の指針そのものにも根本的な欠陥・地＝実写 写真 [20] を暗く） ／ P2V1¶2.120（`was fundamentally defective`）
> ただし、前の章で見たとおり、国の指針そのものにも、
> 根本的な欠陥があった。誤りは、1か所ではなかった。

**c904** 🔧 ／ イメージ（フリー素材＝建物の中のガスの管〈特定できない〉・画面に「イメージ」） ／ P1V4¶34.15（`Although the supply of gas allowed fires within individual flats to continue to burn until it was shut off at 23.40 that day, its contribution to the fire which consumed the tower appears to have been minimal`）
> 次に、「ガス管が、火を大きくした」という話。報告は、部屋の中のガスは、
> その日の夜11時40分に止めるまで燃え続けたが、塔を包んだ火への影響は、
> ごく小さかったとみられる、と書く。

**c905** ／ 図 模式（火を大きくしたものの札＝外壁の板の芯〈いちばん〉・断熱材・ガス〈ごく小さい〉・地＝実写 写真 [20] を暗く） ／ P1ES¶2.13（`The principal reason why the flames spread so rapidly`）
> Q: 火を大きくしたのは、ガスではなかったんだね。
> そう。報告が、いちばんの理由としたのは、外壁の板の芯だった。

**c906** ／ イメージ（フリー素材＝パソコンの画面のブログ〈字と名前は読めない〉・画面に「イメージ」） ／ P2V3¶42.41（`On 20 November 2016`…`posted an article on the Grenfell Action Group blog`…`he criticised the TMO for failing to take fire safety seriously`）
> 3つ目。「住民の団体のブログが、火事を予言していた」という話。
> 2016年11月、住民の団体のブログは、管理の組織の防火の扱いを、厳しく批判した。

**c907** ／ 実写 公的 P2V3 ¶42.42 の頁（PDF の頁は ⑤b で＝段落で探す・額装・訳の札「火事を予言してはいなかった。だが、聞き流してはいけない知らせだった」・出典の行「グレンフェル・タワー調査 第2段階の報告 第3巻 ¶42.42（2024）」） ／ P2V3¶42.42（`it did not in fact predict the fire at Grenfell Tower, much less what turned out to be its cause`…`it was a message that the TMO could not afford to ignore`）
> 報告は、その投稿は、火事も、その原因も、予言してはいなかったと書く。
> ただ、管理の組織が、聞き流してはいけない知らせだった、とも書いている。

**c908** ／ 図 模式（報告の認めたことの札〈文字は小さく・人は描かない〉・地＝実写 写真 [20] を暗く） ／ P2V1¶2.102（`all those whose bodies were destroyed by the fire were dead or unconscious when the fire reached them`）
> 4つ目。亡くなった人の最期について、つらい話が語られることがある。
> 報告は、遺体が火で失われた人はみな、炎が届いたとき、
> すでに亡くなっていたか、意識が無かった、と認めている。

**c909** 🔧 ／ 実写 公的 P1ES ¶33.26 の頁（PDF p23・額装・訳の札「第1段階では調べていない」・出典の行「グレンフェル・タワー調査 第1段階の報告 要約 ¶33.26（2019）」） ／ P1ES¶33.26（`whether such a system would be likely to have suppressed the fire in Flat 16 or prevented it from escaping into the cladding before the firefighters could extinguish it is not something that was investigated in Phase 1`）
> 5つ目。「スプリンクラーがあれば、防げた」という話。2019年の報告は、
> スプリンクラーで、この台所の火を抑えられたかは、調べていない、と書く。

**c910** ／ 図 模式（言い切らない所の札＝調べていないことは、言い切らない・地＝実写 写真 [20] を暗く） ／ 計（この動画の書き方）
> Q: 調べていないことは、言い切れないんだね。
> そう。この動画も、報告が言い切っていないことは、言い切らない。

**c911** 🔧 ／ 図 模式（「安さで選んだ」の札＝費用は主な理由・根にあったのは力不足が生んだ誤りの重なり・地＝実写 写真 [20] を暗く） ／ P2V1¶2.73（`largely on the grounds of cost`）・P2V1¶2.74（`a series of errors caused by the incompetence of the organisations and individuals involved in the refurbishment`）
> 6つ目。「安さで選んだ」という話。費用は、たしかに主な理由だった。
> だが根にあったのは、関わった組織と人の力不足が生んだ、誤りの重なりだった。

**c912** 🔧 ／ 図 模式（「消防の対応」の札＝報告が問うたのは、組織の運営と備え・訓練・指揮・隊員の勇気は別に書く・地＝実写 写真 [20] を暗く） ／ P2V1¶2.91（`chronic lack of effective management and leadership`）・P1V4¶28.8（`the principal failure was one of command`）・P1ES¶2.18（`LFB incident commanders had received no training in how to recognise the need for an evacuation or how to organise one`）・P1V4¶28.1（`displayed enormous courage and selfless devotion to duty`）
> 消防の対応も、強い言葉で語られることがある。報告が問うたのは、
> 隊員の勇気ではなく、組織の運営と備え、訓練と指揮だった。

**c913** ／ イメージ（フリー素材＝夕暮れのロンドンの街並み〈特定できない〉・画面に「イメージ」） ／ 計（第9章へのつなぎ）
> では、あの夜のあと、何が変わったのか。そして、変わっていないものは何か。

---

### 第9章　あの夜のあとに、変わったこと（17カット）

**ca01** 🔧 ／ 実写 公的 P2V1 ¶2.103 の頁（PDF p36・額装・訳の札「混乱し、遅く、決められず、場当たりだった」・出典の行「グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.103（2024）」） ／ P2V1¶2.103（`In the first week after the fire at Grenfell Tower the response of the government and RBKC was muddled, slow, indecisive and piecemeal`）
> Q: 火事のあと、住んでいた人たちは、どうなったの？
> 最初の1週間の、政府と区の対応を、報告は、
> 混乱し、遅く、決められず、場当たりだった、と書いている。

**ca02** ／ イメージ（フリー素材＝ロンドンの住宅街の遠景〈特定できない〉・画面に「イメージ」） ／ P2V7¶98.1（`hundreds of people were displaced from their homes in the tower and surrounding`）・P2V1¶2.104（`Certain aspects of the response demonstrated a marked lack of respect for human decency and dignity`）
> 塔とそのまわりの住まいから、何百人もの人が、家を離れることになった。
> 報告によれば、その対応には、人の尊厳を欠くものもあった。

**ca03** 🔧 ／ イメージ（フリー素材＝支援の物資を仕分ける手もと〈顔なし〉・画面に「イメージ」） ／ P2V1¶2.114（`With the support of local voluntary organisations, they provided support in the hours immediately following the fire when the authorities were conspicuous by their absence`）
> 支えになったのは、地域の人たちと、地元のボランティアの団体だった。
> 報告は、火事の直後、役所の姿が見えなかった時に、彼らが人を支えた、と書く。

**ca04** ／ 実写 公的 中（独立の見直しの中間報告の頁〈p.9〉・額装・訳の札「規制の仕組みは、目的に合っていない」・出典の行「建築規制と防火の独立の見直し 中間報告（2017年12月・英国政府）」） ／ 中（`the current regulatory system for ensuring fire safety in high-rise and complex buildings is not fit for purpose`）
> 火事の半年後、国が頼んだ独立の見直しは、
> 高い建物の防火を守る規制の仕組みは、目的に合っていない、と結論した。

**ca05** 🔧 ／ 図 模式（「底辺への競争」の札＝安く早くを競う・知らないか、無関心か、仕組みが良いやり方を助けないか・地＝実写 写真 [25] を暗く） ／ 終（`can be described as a 'race to the bottom' caused either through ignorance, indifference, or because the system does not facilitate good practice`）
> 2018年5月の、見直しの最終の報告は、業界で、安さを競う「底辺への競争」が、
> 無知か、無関心か、仕組みのせいで、起きていたと書いた。
> Q: 安さの競争、なんだ。

**ca06** 🔧 ／ 実写 公的 報告の頁（第1段階 2019年10月と第2段階 2024年9月の報告の、委員長と委員の名が写らない頁〈目次の頁など〉を並べる・額装・出典の行「グレンフェル・タワー調査 第1段階の報告（2019）・第2段階の報告（2024）」） ／ 計（第1段階の報告＝2019-10-30・第2段階の報告＝2024-09-04）
> 公開の調査は、2019年10月に、その夜に何が起きたかの報告を出した。
> 2024年9月には、なぜ起きたのかの報告を出した。

**ca07** ／ 実写 公的 法（建築安全法 第65条の頁〈legislation.gov.uk〉・額装・訳の札「高さ18メートル以上か7階建て以上・住戸2つ以上」・出典の行「Building Safety Act 2022 第65条（英国）」） ／ 法（`28th April 2022`…`at least 18 metres in height or has at least 7 storeys`…`contains at least 2 residential units`）
> 2022年4月には、建築安全法ができた。高さ18メートル以上か、7階建て以上で、
> 住戸が2つ以上ある建物を、危険の高い建物として見る仕組みだ。

**ca08** ／ 図 模式（第2段階の報告の勧告の札＝58・国へ37・ほかの組織へ21・地＝実写 写真 [24] を暗く） ／ 応（`The Inquiry made 58 recommendations, of which 37 were directed at the government and 21 were directed at other bodies and institutions`）
> 2024年の報告は、58の勧告を出した。そのうち37は国に、
> 21は、ほかの組織に向けたものだった。

**ca09** 🔧 ／ 実写 公的 首（首相の議会での声明の頁〈gov.uk・2024年9月4日〉の引用の行だけ〈委員長と首相の名の行を入れない〉・額装・訳の札「起きた死は、すべて避けられた」〈委員長の言葉の引用〉・出典の行「首相の議会での声明（2024年9月4日・英国政府）」） ／ 首（`concluded this morning`…`the simple truth is that the deaths that occurred were all avoidable`）
> Q: 国は、何と言ったの？
> 報告が出た日、首相は議会で、調査の委員長が述べた言葉を引いた。
> 「単純な真実は、起きた死は、すべて避けられた、ということだ」。

**ca10** ／ 実写 写真 [18]（覆いと横断幕の塔の寄り〈2018年6月〉・BY-SA 4.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・△ 横断幕の字に名前が無いかを ⑤b で原寸＝あれば替える・副題「火事から1年の塔〈2018年6月〉」・出典の行「Wikimedia Commons（CC BY-SA 4.0）」） ／ 首（`I want to start with an apology on behalf of the British state to each and every one of you`…`It should never have happened`）
> そして首相は、国を代表して、遺族と生き残った人たちに、謝った。
> 「起きてはならないことだった」と。

**ca11** 🔧 ／ 実写 公的 応（政府の応答の頁〈gov.uk・2025年2月26日〉・額装・訳の札「49は全面で、残る9は考え方として受け入れる」・出典の行「グレンフェル・タワー調査 第2段階の報告への政府の応答（2025年2月）」） ／ 応（`49 of the recommendations are being accepted in full by the government and other responsible organisations`…`As regards the remaining 9, which are all directed at government, the government accepts them in principle`）
> 2025年2月、政府は勧告に応えた。58の勧告のうち49は、政府とほかの組織が、
> そのまま受け入れる。国に向けた残りの9は、考え方として受け入れる、とした。

**ca12** 🔧 ／ 図 模式（変わった決まりの札＝18メートルをこえる住宅などの外壁に燃える材料を禁止〈イングランド〉・新しい共同住宅のスプリンクラー〈30メートルをこえる → 11メートルをこえる〉・地＝実写 写真 [24] を暗く） ／ 応（`The use of combustible materials in and on external walls of buildings, including flats, hospitals and student accommodation over 18 metres in height, has been banned`…`The threshold for the provision of sprinklers in new blocks of flats has been lowered from over 30 metres to over 11 metres`）
> 18メートルをこえる住宅などの外壁では、燃える材料が、すでに禁じられた。
> 新しい共同住宅のスプリンクラーも、11メートルをこえる建物へ広げられた。

**ca13** 🔧 ／ 図 模式（変わる決まりの札＝18メートルをこえる新しい建物に2つ目の階段〈2026年から＝2025年2月の応答〉・国の資金で直す18メートル超の危ない外壁〈2029年の終わりまで〉・地＝実写 写真 [24] を暗く） ／ 応（`There will be statutory guidance on the need for a second staircase in all new buildings over 18 metres coming into force in 2026`…`By the end of 2029, all buildings over 18 metres with unsafe cladding in a government funded scheme will have been remediated`）
> 18メートルをこえる新しい建物に、2つ目の階段を求める指針は2026年から、
> 国の資金で直す18メートル超の危ない外壁は、2029年の終わりまでに、とされた。
> Q: 決まりは、少しずつ変わっているんだね。

**ca14** 🔧 ／ 実写 公的 進（進捗報告の表の頁〈gov.uk・2026年9月〉・額装・訳の札「61件のうち30件が済み」・出典の行「グレンフェル・タワー調査への政府の進捗報告（2026年9月）」） ／ 進（`Total 61 31 30`…`We continue to expect that all recommendations will be implemented by the end of 2029`）
> そう。政府は、2019年の報告の残りも合わせて、61の勧告を追っている。
> 2026年9月の時点で、済んだのは30。
> 政府は、すべての実施を、2029年の終わりまでと見込んでいる。

**ca15** ／ 実写 写真 [45]（2018年5月の隣の学校と覆いの塔・BY-SA 4.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・副題「覆われた塔〈2018年5月〉」・出典の行「Wikimedia Commons（CC BY-SA 4.0）」） ／ 塔（`will be carefully taken down to the ground`…`commenced in September 2025`）・年（`We expect the work to continue until at least spring 2027`）
> 塔の取り壊しは、2025年9月に、慎重に始められた。
> 2026年2月の政府の報告では、作業は、早くても2027年の春まで続く見込みだ。

**ca16** 🔧 ／ 図 模式（変わったことの札＝見直し・建築安全法・2つの報告・勧告の半分近く・取り壊し・地＝実写 写真 [24] を暗く） ／ 計（第9章のまとめ）
> Q: 取り壊しも、始まっているんだ。
> そう。ただ、2026年11月の時点で、まだ出ていない答えもある。

**ca17** ／ 図 模式（問いの札＝誰かが、罪に問われるのか・地＝実写 写真 [24] を暗く） ／ 計（第10章へのつなぎ）
> 火事で人が亡くなったことについて、誰かが、罪に問われるのか、という答えだ。

---

### 第10章　9年たっても出ない答え（17カット）

**cb01** 🔧 ／ 実写 公的 警1（警視庁の発表の頁〈2026年9月30日〉の頭の1文だけ〈罪名の列と幹部の名を入れない〉・額装・訳の札「すべての書類を検察へ」・出典の行「ロンドン警視庁の発表（2026年9月30日）」） ／ 警1（`The Met has now submitted all files to the Crown Prosecution Service to allow them to make charging decisions in relation to the Grenfell Tower fire`）
> Q: 裁判は、始まっているの？
> 2026年11月の時点で、まだ、起訴された人も会社も無い。ロンドン警視庁は、
> 火事のあとから、ずっと捜査を続けてきた。

**cb02** ／ 図 模式（容疑の数の札＝2024年 19の会社や団体と58人・名前は出さない・地＝実写 写真 [24] を暗く） ／ 警3（`Identified and are investigating 19 companies or organisations and 58 individuals, as suspects`）
> 2024年、警視庁は、19の会社や団体と、58人を、
> 容疑者として調べている、と発表した。

**cb03** 🔧 ／ イメージ（フリー素材＝積み上げた書類の箱〈字は読めない〉・画面に「イメージ」） ／ 警3（`Interviewed under caution over 50 suspects for a total of more than 300 hours`）
> 50をこえる容疑者から、合わせて300時間をこえる聴取をした、ともしている。

**cb04** ／ 図 模式（警視庁の見込みの札＝2024年5月の時点で、報告を読みこみ書類を仕上げるのは、少なくとも2025年の終わりまで・地＝実写 写真 [24] を暗く） ／ 警3（`at least until the end of 2025 to fully assess the public inquiry's phase 2 report and finalise evidential files`）
> 2024年5月、警視庁は、調査の報告を読みこみ、書類を仕上げるまでに、
> 少なくとも2025年の終わりまでかかる、と見ていた。

**cb05** 🔧 ／ 図 模式（調べた範囲の札＝1万5,000人と700の組織・容疑者は20の会社や団体と57人〈2026年5月〉・地＝実写 写真 [24] を暗く） ／ 警2（`The role of 15,000 individuals and 700 organisations have been examined of which 57 people and 20 organisations are suspects for criminal offences`）
> 2026年5月の警視庁の発表では、1万5,000人と700の組織の役割を調べ、
> 容疑者は、20の会社や団体と、57人になっていた。

**cb06** 🔧 ／ 実写 公的 警1（警視庁の発表の頁〈2026年9月30日〉の「20 files」の1文だけ〈罪名の列と幹部の名を入れない〉・額装・訳の札「20の会社と団体、54人」・出典の行「ロンドン警視庁の発表（2026年9月30日）」） ／ 警1（`The 20 files relate to 20 companies and organisations and 54 individuals`）
> そして2026年9月30日。警視庁は、すべての捜査の書類を、検察に送った。
> 書類は、20の会社と団体と、54人についてのものだ。

**cb07** 🔧 ／ イメージ（フリー素材＝棚に並んだ書類のファイル〈字は読めない〉・画面に「イメージ」） ／ 警1（`As well as the 20 files, the submission to the CPS also includes 14 overarching evidence files`）
> Q: 書類が、そろったんだ。
> その書類とは別に、事件の全体にかかわる証拠の書類も、14あった。

**cb08** ／ 図 模式（誰が決めるかの札＝警視庁は証拠の書類を送る → 起訴するかを決めるのは検察・地＝実写 写真 [24] を暗く） ／ 警1（`to allow them to make charging decisions in relation to the Grenfell Tower fire`）
> 起訴するかどうかを決めるのは、警視庁ではなく、検察だ。
> 警視庁は、その判断のための証拠を、書類にまとめて送った。

**cb09** ／ 図 暦（2027年6月の札＝火事から10年・それより前に起訴するかを決める約束・地＝実写 写真 [24] を暗く） ／ 警1（`The CPS has committed to making the charging decisions before the 10th anniversary of the fire in June 2027`）
> 検察は、火事から10年になる2027年6月より前に、起訴するかどうかを決める、
> と約束している。

**cb10** 🔧 ／ 図 模式（名前を出さない札＝警視庁の発表に容疑者の名は無い・この動画も、容疑の対象の会社や人を言わない・地＝実写 写真 [24] を暗く） ／ 計（この回の線）
> Q: どの会社が、疑われているの？
> 警視庁の発表に、容疑者の名は無い。この動画も、
> どの会社や人が容疑の対象なのかは、言わない。

**cb11** 🔧 ／ イメージ（フリー素材＝夜明けの空と街の遠景〈特定できない〉・画面に「イメージ」） ／ 警1（`has had a significant impact on those waiting for answers`…`it has necessarily taken this long to ensure our investigation is meticulous`）
> 警視庁は、答えを待つ人たちに、長い時間が重くのしかかってきたと認めた。
> そのうえで、念入りな捜査に、これだけの時間が必要だった、と説明している。

**cb12** 🔧 ／ 実写 衛星 取り壊し中の塔（ランカスター・ウェスト団地の塔の位置＝撮影の時点の姿は ⑤b で確かめる・Google の表示を絵の近くに・副題「塔のあたり〈衛星写真〉」） ／ 計（2017-06-14 から 2026-11 まで＝9年5か月）
> Q: 答えを、ずっと待っているんだね。
> そう。火事から、2026年11月で、9年と5か月になる。

**cb13** 🔧 ／ 実写 公的 P2V5 ¶83.13 の頁（PDF p210・額装・訳の札「2009年の火事が予告した欠けが、2017年6月14日の夜に、ふたたび現れた」・出典の行「グレンフェル・タワー調査 第2段階の報告 第5巻 ¶83.13（2024）」） ／ P2V5¶83.13（`the Lakanal House fire in July 2009 forewarned the LFB about the existence of the shortcomings which revealed themselves once more on the night of 14 June 2017`）
> 一方、調査の報告は、2009年のラカナル・ハウスの火事が示した消防の欠けが、
> 2017年6月14日の夜、ふたたび現れた、と書いている。

**cb14** 🔧 ／ 図 模式（2つの警告の札＝1999年の議会の委員会「外壁の火で人が亡くなるのを待つな」と国に・2009年のラカナル・ハウス・地＝実写 写真 [24] を暗く） ／ P2V2¶29.5（`it should not take a serious fire in which people were killed before steps were taken to minimise the risks posed by some external cladding systems`…`Unfortunately, that warning was ignored`）
> 1999年、議会の委員会は、外壁の火で人が亡くなるのを待つな、と国に警告していた。
> 報告は、その警告は聞き流された、と書く。

**cb15** 🔧 ／ 図 模式（「部屋で待て」の答えの札＝改めるべき時は1時30分から1時50分・取りやめは2時47分・欠けは備えと訓練と指揮・地＝実写 写真 [24] を暗く） ／ P1V4¶28.6（`That point had been reached by 01.30 at the earliest and by 01.50 at the latest`）
> 「部屋で待て」は、報告によれば、
> 午前1時30分から1時50分のあいだに改めるべきだった。
> 答えの一部は、報告の中に、もう書かれている。

**cb16** 🔧 ／ 図 模式（まだ出ていない答えの札＝罪に問われるか〈2027年6月より前〉・勧告の残り〈2029年の終わりまで〉・地＝実写 写真 [24] を暗く） ／ 計（2026年11月の時点）
> まだ出ていないのは、誰かが罪に問われるのか。そして、残りの勧告が、
> 本当に実施されるのか。2026年11月の時点の、答えの残りだ。

**cb17** 🔧 ／ 実写 映像 #15 空撮C（0:25〜2:40 のうち A・B と重ならない区間・副題「ロンドンの空撮」・出典の行「Wikimedia Commons（CC BY 3.0）」） ／ 計（第11章へのつなぎ）
> 最後に、日本の高い建物の話をしてから、3つの問いの答えをまとめる。

---

### 第11章　日本では。そして3つの答え（13カット）

**cc01** 🔧 ／ 実写 公的 国（国土交通省の資料6 の p.3〈日本の決まりとの比べの表〉の頁〈2017年10月6日〉＝p.2 は使わない・額装・訳なし＝日本語の資料・出典の行「国土交通省 社会資本整備審議会 資料6（2017年10月6日）」） ／ 国（`ロンドン共同住宅火災について`…`平成29年10月6日`）
> Q: 日本の国は、何かしたの？
> 火事から4か月足らずで、国土交通省は、グレンフェルタワーと、
> 日本の決まりとの違いを、表にまとめた。

**cc02** 🔧 ／ 図 表（日本の決まりとの比べの表＝2つ以上の地上への階段・スプリンクラー・外装の材料・地＝実写 写真 [24] を暗く） ／ 国（`2以上の直通階段の設置`…`6階以上の階に設置`…`11階以上の階に 設置`）
> 表によれば、日本の数え方で、6階以上の階などには、地上へ通じる階段が2つ以上要る。
> スプリンクラーも、11階以上の階には置く決まりがある。例外もある。

**cc03** ／ 図 模式（外装の材料の札＝材料そのものの決まりは無い・運用の指針で、燃えるプラスチック系の断熱材は耐火の構造の外壁に限る・地＝実写 写真 [24] を暗く） ／ 国（`外装材の材質自体に関する規制はないが`…`の外壁に限り可能`）
> 外装の材料そのものの決まりは無い。ただ運用の指針で、
> 一定のプラスチック系の断熱材を張れるのは、耐火の造りの外壁に限る、としている。

**cc04** 🔧 ／ 図 割合（寒い地方の11階以上の共同住宅 279棟＝外から断熱する造り 3棟・内から断熱する造り 276棟・地＝実写 写真 [24] を暗く） ／ 国（`平成24年4月から平成29年3月までに新築又は外壁改修を行ったもの`…`外断熱工法 棟数 279棟 276棟 3棟`）
> 寒い地方で、2012年からの5年に建てた、または外壁を直した、
> 11階以上の共同住宅279棟のうち、外から断熱する造りは、3棟だけだった。

**cc05** 🔧 ／ 実写 公的 国（建築基準整備促進事業 F11 の報告の p.24 の頁・額装・出典の行「国土交通省 建築基準整備促進事業 F11 の報告（平成28〜29年度）」） ／ 国（`ロンドン火災との比較において極めて危険という状況は認められない`）
> 国の事業でおこなわれた実験は、国内でふつうに使う断熱材と外装材は、
> ロンドンの火事と比べて、極めて危険という状況は認められない、とした。

**cc06** 🔧 ／ イメージ（フリー素材＝足場とシートに覆われた工事中の高層の建物〈特定できない〉・画面に「イメージ」・出典の行「香港警察の発表（2026年1月15日）」） ／ 香（`a total of 168 deceased persons confirmed`）
> 2025年11月、香港の高層住宅で、改修の工事中に火事が起きた。
> 香港の警察の発表では、168人が亡くなった。

**cc07** ／ 実写 公的 消（消防庁の通知の頁〈2026年3月30日〉・額装・出典の行「消防庁 予防課長 通知 消防予第120号（2026年3月30日）」） ／ 消（`工事用シートは、消防法令に基づき、防炎物品を使用すること`）
> 日本の消防庁は、2026年3月、工事中の建物の注意として、
> 工事用のシートには、燃えにくい防炎の品を使うよう、通知した。
> Q: 日本でも、工事中の火に気をつけているんだね。

**cc08** ／ 図 模式（1つ目の答えの札＝芯の燃える外装の板・熱をためる断熱材・カセットの形・飾りの冠・地＝実写 写真 [24] を暗く） ／ 計（1つ目の問いの答え）
> そう。最後に、3つの問いの答えを並べる。1つ目。台所の火が塔を包んだのは、
> 芯の燃える外装の板と、熱をためる断熱材、カセットの形、そして飾りの冠のためだった。

**cc09** ／ 図 模式（2つ目の答えの札＝改めるべき時を過ぎても続いた「部屋で待て」・欠けは備えと訓練と指揮・地＝実写 写真 [24] を暗く） ／ 計（2つ目の問いの答え）
> 2つ目。「部屋で待て」は、改めるべき時を過ぎても、続いた。報告によれば、
> 欠けていたのは、隊員の勇気ではなく、備えと訓練と、指揮だった。

**cc10** 🔧 ／ 図 模式（3つ目の答えの札＝見た目と費用だけを見た人たちが選ぶ・売った会社は危険を隠した・国は警告を受けても動かない・地＝実写 写真 [24] を暗く） ／ 計（3つ目の問いの答え）
> 3つ目。燃える外壁は、見た目と費用だけを見た人たちが選び、
> 売った会社は危険を隠し、国は、警告を受けても動かなかった。

**cc11** 🔧 ／ 実写 写真 [53]（2018年5月の覆いの塔・BY-SA 4.0＝額装・無加工・丸ごと・地は同じ写真のぼかし・副題「覆われた塔〈2018年5月〉」・出典の行「Wikimedia Commons（CC BY-SA 4.0）」） ／ P2V1¶2.4（`the culmination of decades of failure`）
> Q: いろいろな原因が、重なっていたんだね。
> そう。報告は、国などの何十年にもわたる失敗の行き着いた先が、この火事だ、と書く。

**cc12** 🔧 ／ 実写 映像 #15 焼けた塔D（3:00〜3:50 を4つに割った4つ目・副題「焼けた塔〈2017年7月〉」・出典の行「Wikimedia Commons（CC BY 3.0）」） ／ 計（結び）
> 72人が亡くなった夜の答えの多くは、もう報告に書かれている。
> 残っているのは、罪に問われるかと、仕組みを本当に変えられるかだ。

**cc13** 🔧 ／ 実写 衛星 ロンドン西部（塔のあたりと、まわりの街・地下鉄の線・Google の表示を絵の近くに・副題「ロンドン西部〈衛星写真〉」） ／ ―（問い）
> あなたは、住んでいる建物や、よく行く建物の、非常階段の場所を知っていますか。
> よければ、コメントで教えてください。

---

## 5. 使わなかったもの（理由）
- 「英国史上最悪」「60時間燃えた」＝一次資料に無い（① の決め⑨）。報告の言い方「戦後の英国で最悪の災害の1つ」だけ（c107）
- 制圧の日（2017-06-15・ロンドン市長の発表＝sources.md §2）＝語りでは使っていない（完全に消えた日時は無い）。最後の生存者 8:07 と、ガスを止めた 23:40 まで
- 亡くなった子どもの数＝報告の語の当たりで見つからない（報道の数は使わない）。塔にいた子ども67人（P1V2 ¶10.130）は在館の数として使った
- 「スプリンクラーが無かった」＝報告の文で確かめられなかった（国交省の表は「報道等による」）＝語りでは言わず、第1段階が効き目を調べていないことだけ（c909）
- 区の対応の章（P2V7 101〜105章）の人の名前と、ラマダンの話（P2V1 ¶2.104）＝話の枝が増える＝入れていない
- 2012年の別の高層住宅の火事（Taplow House）の名と細部・2013年のアラブ首長国連邦の火事の報道・2014年10月の外装の技術団体の会合＝第5章は「前ぶれも、あった」の1件と、2015年3月のメールに絞った
- カセットの額（£419,627・£293,368）・TMO の削減の目標（約£800,000）・予算の差（£270,000）＝数が多すぎる＝リベットの額と差だけ
- 香港の火事の原因（たばこ）と網の差し替えの疑い＝決め⑧（一言だけ）＝168人と工事中だけ
- 委員長の公表の日の声明の原文（調査のサイト＝robots で拒否）＝首相の議会での引用だけ（ca09）
- Commons の追悼の場55点・支援4点（未見）・#17（ロゴと私人の顔）・#38（掲示の名前が未確認）・報告のホワイトボードの図（P1V3 図16.4・16.5）
- 🆕 **警視庁が検察に検討を求めた罪名**（法人の過失致死・重大な過失による致死・安全衛生の法律の違反・詐欺とそれに関わる罪・公務の上の不正行為など＝警1）＝① の線②「数と日付だけ」に合わせて語りから外した（第6章で名を挙げた会社の「不正」と「詐欺」が結びついて聞こえるおそれも＝係の指摘）＝入れるかは承認①で
- 🆕 政府が追う「61」の内訳＝第2段階の58＋第1段階の残り3（進 2026-09-10 `all 58 Phase 2 recommendations and the 3 remaining Phase 1 recommendations` ✓）＝ca14 で言える
- 🆕 「消防は第1段階の勧告をすべて実施した（ロンドン消防への29件と全国への9件を含む）」（政府の年次報告の文として ④ が書いた）＝④' で年次報告の写し3つと進捗報告に語を変えて25通り当てて0件（消防の章の頁は文字の写しが無い）＝入れない（概要欄にも出さない）
- 🆕 はしご車の隊員の記憶（10階ほど・P1V2 ¶12.22）＝報告の結論の段落（P1V4 ¶28.133＝最大32メートル・10階より上に届かない）に替えた

## 6. 読み間違えやすい語（⑤a の前に確かめる）
| 語 | 読み | どこ |
|---|---|---|
| グレンフェルタワー | ぐれんふぇるたわー | c101 ほか |
| ケンジントン・アンド・チェルシー区 | けんじんとん・あんど・ちぇるしーく | c201 |
| ランカスター・ウェスト | らんかすたー・うぇすと | c201 |
| ラカナル・ハウス・サザーク | らかなる・はうす | c522・c623・c806・cb13 |
| エディンバラ | えでぃんばら | c401 |
| ドバイ | どばい | c706・c813 |
| 999 | きゅうきゅうきゅう（「きゅうひゃくきゅうじゅうきゅう」にしない） | c301・c501 |
| TMO・CEP・BRE | てぃーえむおー・しーいーぴー・びーあーるいー（BRE は語りに出していない） | c208・c602・c605 |
| スタジオE・等級E | すたじお・いー・とうきゅう・いー | c602・c707 |
| ライドン・ハーレー・アルコニック・セロテックス・キングスパン | 片かなのまま | 第5〜6章 |
| クラス0 | くらす・ぜろ | c720 |
| 0階 | ぜろかい | c204・c206 |
| 冠 | かんむり | c213・c409〜c410 |
| 亜鉛 | あえん | c603〜c605 |
| 検死官 | けんしかん | c806 |
| 慢心・尊厳・顧み | まんしん・そんげん・かえりみ | c523・c807・ca02・c808 |
| 底辺への競争 | ていへんへのきょうそう | ca05 |
| 表・応えた・18メートル超 | ひょう（「おもて」にしない）・こたえた・じゅうはちめーとるちょう | cc01・cc02・ca11・ca13 |
| 住戸・6階・11階・54人・279棟・防炎の品・9年と5か月 | じゅうこ・ろっかい・じゅういっかい・ごじゅうよにん・にひゃくななじゅうきゅうとう・ぼうえんのしな・きゅうねんとごかげつ | ca07・cc02・cb06・cc04・cc07・cb12 |
| 大勢・2組・2基・1か所・1室・10階・1回・20分・2,500ページ | おおぜい・ふたくみ・にき・いっかしょ・いっしつ・じゅっかい・いっかい・にじゅっぷん・にせんごひゃくぺーじ | c507・c710・c205・c903・c301・c414・c111 ほか |
| アルミ複合板・元請け・要る | あるみふくごうばん・もとうけ・いる | c212 ほか・第5章・cc02 |
| 1万5,000人・57万6,973ポンド ほか | 数字の読みを ⑤a で先回りしてかな固定（記憶 `feedback-tts-misreads-are-positional`） | cb05・c613 ほか |
| 午前0時54分・1時9分・2時47分・8時7分 | ⑤a で全件 | 多数 |

## 7. 素材との突き合わせ（映像方針へ）
- 報告の図（紙面の引用＝図の番号と題の行ごと・額装・無加工・サムネに使わない）＝P1V1 図3.2・6.1・6.7・6.8・6.11・7.2／P1V2 図10.5・10.6・10.7・10.9・10.14・10.15・10.17・10.22・10.24・11.5〜11.8・12.7・14.1／P1V3 図17.3・17.4・18.1／P1V4 図21.1・21.4・21.6・22.8・22.15／P2V1 図5.2・5.8・5.9／P2V7 図109.1〜109.3＝🔴 どれも ⑤b で頁を高い解像度で描いて切り出す（埋め込みは 880px 前後）・図6.8 と図11.5〜11.8 は中身を原寸で見ていない（見本帳の大きさだけ）
- Commons の写真（番号＝cand33.json）＝[2]・[3]・[7]・[8]・[12]・[18]・[19]・[20]・[21]・[23]・[26]・[28]・[29]・[30]・[31]・[32]・[33]・[35]・[39]・[40]・[41]・[45]・[53]・[55]・[58]・[59]・[60]・[61]・[62]・[68]・[69]・[70]・[71]・[72]（34点）＝取る前に一覧でカズヤくんの了承（Commons＝先に聞く・materials.md §9）。🔴 △＝[18]（横断幕の字）・[58]・[59]・[60]（追悼の壁と掲示の名前と顔）・[26]・[30]・[31]・[33]（BY-SA の中身は見本帳の大きさだけ）＝原寸で見てから。⚠️ 係の指摘＝同じ撮影者がほぼ同じ時刻に撮った対（[61]と[65]・[18]と[56]・[21]と[22]・[26]と[27]）は片方だけにした＝⑤b で画素でも比べる
- 地（説明カットの地）に使った写真＝[20]・[21]・[23]・[24]・[25]・[28]・[29]・[35]・[61]・[62]・[63]・[71]・[72]＝⚠️ [35]・[24]・[72] に偏っている（④' と映像方針で直前の写真に散らす）・[24]・[25]・[63] は地だけで本体に出していない・[58]・[59]（追悼の壁が写る）は係の指摘で地から外した
- 映像 #15＝焼けた塔A（c109）・B（c431）・C（c526）・D（cc12）・空撮A（c201）・B（c820）・C（cb17）＝🔴 区間は ⑤b で1秒ごとのコマを見て割る（焼けた塔は 3:00〜3:50 の50秒を4つ＝1区間 約12秒）
- 衛星写真＝ランカスター・ウェスト団地（c202）・ラカナル・ハウス（c522）・取り壊し中の塔（cb12＝撮影の年を ⑤b で）・ロンドン西部（cc13）
- 文字の頁（実写 公的）34＝報告の段落の頁・警視庁・政府・首相・国交省・消防庁＝訳の札は ⑤b で
- フリー素材（イメージ）25＝消防車・防火服・電話・会議室・アルミの板・断熱材・カタログ・高層ビル・議会の建物・ガスの管・ブログの画面・物資の仕分け・書類・工事中の建物 ほか＝社名・字・顔を見せない

## 8. 概要欄の用語（下書き）
- アルミ複合板＝2枚の薄いアルミの板で、プラスチックの芯をはさんだ外装の板
- カセット＝板を箱の形に折り、枠に引っかけて留める形
- 区画＝火や煙を、部屋ごとに閉じこめる、建物の作り
- 「部屋で待て」（stay put）＝高層の住宅で、火や熱や煙が直接及ばないかぎり、自分の部屋にとどまる、という考え方
- 公開の調査＝国が開く、公開の聞き取りの調査。グレンフェルタワーの調査は2019年と2024年に報告を出した
- 建築安全法＝2022年にできた英国の法律。イングランドで、高さ18メートル以上か7階建て以上で、住戸が2つ以上ある建物を、危険の高い建物として見る
- クラス0＝小さな試料を燃やす試験にもとづく、英国の古い燃えにくさの等級

## 9. 換算と計算（式）
- 1ポンド＝144.08円（2013年2月の月平均）・170.12円（2014年3月の月平均）＝イングランド銀行 XUMAJYS（`src/web/boe/xumajys_2013_2014.html`・md5 355cfc0c）
- 300,000×144.08＝4,322万円→約4,300万円／576,973×170.12＝9,815万円→約9,800万円／376,175×170.12＝6,399万円→約6,400万円／(576,973−376,175)＝200,798→約20万ポンド（3,416万円）／212,000×170.12＝3,607万円→約3,600万円
- 時刻の差＝0:54→0:59 5分・1:09→1:26 17分（20分足らず）・1:09→4:02 2時間53分（3時間足らず・報告の under three hours）・1:50→2:47 57分（1時間近く）・0:54→8:07 7時間13分（7時間あまり）
- 227−46＝181（2時35分より前に逃げた人・c519 の棒の札）
- 2016-07-07→2017-06-14＝11か月（1年足らず）／2017-06-14→2024-09-04＝7年2か月あまり（7年をかけて）／2017-06→2026-11＝9年5か月（cb12）
- 報告の PDF の頁＝12冊で 2,582頁（2,500ページをこえる）

## 10. 関連
- 設計図＝[kousei.md](kousei.md)・[sources.md](sources.md)・[materials.md](materials.md)
- Vault＝`Projects/事故検証-33本目-①芯の確認と数の表-20261112.md`・`Projects/引き継ぎ-事故検証-33本目-20261112-②③素材と尺.md`
- 32本目の形＝[../ep32/daihon_v1.md](../ep32/daihon_v1.md)
