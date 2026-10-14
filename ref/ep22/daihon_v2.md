# 22本目 タイタン号（2023-06-18＝1本目のリメイク）台本 第2版

> **2026-10-14・22本目のチャット4＝④' 台本【チェックと修正】**で、第1版 [daihon_v1.md](daihon_v1.md)（④・commit `c827ba2`）を直した版。**第1版は1文字も書き換えていない**（md5 を組む前後で比べる）。直したカットの見出しに 🔧。
> 組み方＝`v2_build/make22.py`（扱いの表 `decide22.py` → 差し替え表 `patches22.json` → `build22_v2.py` → 呼び名の行ごとの直し `mech22.py` → 門番 `final22.py` → 台帳 `ledger22.py`）。**第2版を手で直さない**＝`decide22.py` に書き足して `python ref/ep22/v2_build/make22.py`。
> 所見の台帳＝`v2_build/ledger22.md`（照合の係7本＋当て直し2本＋G0）・門番の出力＝`v2_build/gates.md`・第1版→第2版の対照＝`v2_build/diff_v1_v2.md`・原文を引く道具＝`v2_build/pg22.py`・名前の網＝`v2_build/namecheck22.py`（一覧は git の外）。
> 語りは「だ・である」（まりさ）。聞き役（れいむ）の行の印は `> Q: `（印だけ音にも字幕にも出さない）。役割（質問・まとめ・反応）は `v2_build/roles_map.json` → `v2_build/roles.tsv`。決め所（★）の行は無い（10-07）。
> 画の欄の頭の語は第1版と同じ（`実写`＝写真の割合に数える／`図 再現`・`図 線`・`図 模式`・`図 地図`・`図 棒`・`図 帯`＝作る図／`panel`＝文字だけ）。頁は USCG＝「p.PDF〈印字〉」・NTSB＝PDF の頁・TSB＝節の番号。
> 🔴 このリポは公開＝私人の名前を書かない（役割と人数）。語りで名前を出すのは CEO だけ（1回）＝台本は〈CEOの名前〉と書き、名前は Vault の控え（④の引き継ぎ §8）に置く。チャンネルの内部の数字も書かない。
> 呼び名（④'でそろえた）＝語りは「米沿岸警備隊」「米運輸安全委員会」「カナダの調べ」。初出の c102・c203 だけ「アメリカ沿岸警備隊」「アメリカの運輸安全委員会」。

## 0. 第2版の机上の数え（2026-10-14・④'＝`final22.py` の出力を写した。正本は `v2_build/gates.md`）

| 門番・数え | 第1版 | 第2版 | 判定 |
|---|---|---|---|
| 字数（句読点なし・ed01 こみ＝`m22.py`） | 13,303 | **13,480**（本文13,434＋ed01 46）＝上限まで25字。〈CEOの名前〉は置き場の8字で数えた（名前は10字＝⑤a で+2＝13,482） | 幅 13,140〜13,505 の内 |
| 尺の3通り（`m22.py`） | 36分26秒 | **① 36分30秒 ／ ② 36分55秒 ／ ③ 36分55秒**＝開き25秒 | 2分以内 |
| 冒頭（÷365 を1カットずつ） | 引き 36.0秒・最初の見出し 60.8秒 | **引き 37.3秒（c105）・最初の聞き役 37.3秒・最初の見出し 62.6秒（c109）** | 46秒の内・見出しは1分前後 |
| カット・行 | 236・545行 | **236・540行**（1行 中央値28字・最長41字・1カット2.29行）・🔧139＝実際に変わった139 | 欠番0・新設0（`check_script_diff`） |
| 聞き役（`check_listener.judge`・`roles.tsv`） | 67行・質問40／まとめ18／反応9 | **67行（12.4%）・1.81回／分・最長の空き61秒・質問40／まとめ20／反応7（60／30／10%）** | E 0・W 0 |
| まとめのあとの「そう。」（`final22.py` の sou） | — | **まとめ20行のあと20行とも「そう。」**・まとめでない聞き役のあとの「そう。」0 | 0件 |
| 写真・実写 | 69（29.2%） | 69（29.2%）＝画の欄の頭の語は変えていない（副題・札の直しだけ＝c208・c405・c916・c918・c920・cb12） | 20%以上 |
| 文字だけ（`count_text_screens.py --gate`） | 1（cd09） | 1（cd09） | exit 0 |
| 出典の引用（`quotes22.py`） | 404片＝OK 404 | **461片＝OK 461**（④'で足した片も書いた頁・節に当たる・結果＝`v2_build/quotes22_v2.tsv`） | 無し 0 |
| 書かない名前（`namecheck22.py`） | 0 | 0（台本と v2_build の md・json・tsv） | — |
| `check_script.py` | 形の E 0・尺の E（ElevenLabs の定数＝信じない） | 形の E 0・尺の E（同じ理由＝§5a-28b） | 尺の E は信じない |
| 言わない語（`m22.py`） | 6件 | **5件**（c217「ゲーム機」2・c316「波は」誤検出・c511「叩く音」・c902「期限切れ」＝どれも噂の札で引いて報告書で閉じる）。cc05「寄与」は言い換えて消えた | 文脈で可 |

### 0-1. ④ が残した12項目への④'の答え
0. ✅ **承認①（2026-10-14・このチャットでカズヤくん）**＝題は**保留（最有力は A・70字）**／サムネの赤は **A「犠牲5人 異音の4日後も潜航」**／コメントの問いは **C「あなたは、もし乗れるとしたら、深い海の底を自分の目で見てみたいですか。…」**（cd09 に入れた）／cc01 は**「事故」のまま**（§1-1〜§1-3 に記録）
1. **題（§1-1）**：A を推す。題の事実（11か月前の大きな音・4日後にまた潜った）は本編 c104・c105・ca05〜ca14 と同じで、本編より強くない（G6）。「11か月前」が何の前かを言うなら「事故の11か月前」（+3字）＝承認①で聞く。題 B の注意書きに「決まりの1.25 は言い過ぎ（TSB は required・1.25 は会社が ISO に合わせた値）」を足した（G6-013）
2. **書類の再現図69カット**＝映像方針で約35に減らす案（下の §0-3 の表）。語りは変えていない
3. **章ごとの写真の少なさ**（c7 0/19・ca 1/26・c4 2/19）＝映像方針。CEO の写真は使わないまま（kousei §8）を推す
4. **第三者の写真2点**＝ca03（NTSB 図8）はそのまま額装。cb12（NTSB 図10）は凡例が5月20日・27日の写真＝副題を直し（G5-028）、5月24日の語りの横に置かない（cb11 へ移す案）＝映像方針
5. **c510**＝国土地理院「全国都道府県市区町村別面積調」令和8年4月1日版の PDF p.8（印字 -5-）で7都県を確かめた＝計 32,439.41km²（埼玉・千葉・東京は境界未定の参考値）・捜索の約 41,159km² は約1.27倍＝台本のまま。④で神奈川しか読めなかったのは、表の県名の字のあいだに空白（「茨 城 県」）があったため
6. **D10（c411〜c415）**＝「送ったのは壊れる前」は両方のまま。c413 の問いは寄っていない（G2 と同じ判断）。c415 のまとめを「届いたのが壊れる前か後かは、調べで違うんだね」にして c413 の問いを閉じた（G7-020）。「2つの調べ」は「米沿岸警備隊とカナダ」に（c410 の「アメリカの2つの調べ」と取り違えない＝G2-007）
7. **c410**＝カナダの調べも目的（速さを緩める＝suggests）は米2機関と同じ見方＝割れているのは「その深さで落とすのがふつうか」だけ（G2-004）
8. **c918 の棚のたとえ**＝比として正しい（安全率＝壊れる深さ÷潜ってよい深さ・圧は深さに比例）。「決まり」→「基準」・「余裕は、基準の半分も無い」を足した。1.25 の出どころ（2020年に会社が国際規格に合わせた・TSB §1.12.2）は c917 の頭に置いた（c708 の「最低1.5」は2015年＝時期で分かれる）
9. **cc01**＝「防ぐことができた事故」のまま推す（cc12・cd07 の this tragedy も「この事故」＝3か所そろう）。原文どおり「悲劇」と読むなら `tools/check_script.py` の `HYPE_QUOTE_OK` に登録が要る（④'は tools を触らない）＝承認①で聞いた→**「事故」のまま**（カズヤくん）
10. **cd04**＝向き（3冊が主な原因に挙げるのは会社）は言い過ぎではない。ただ「懸念を言った人は、会社を去った」は TSB の some・dismissed を落としていた（🔴 G6-001）＝「辞めた人も、辞めさせられた人もいた」に直した。問いは「誰なら止められたのか」（受身に聞こえない形＝c107・cc11 とそろえた）
11. **cb04**＝「摂氏」を外し、期間（この冬、12月から2月）を言う（G5-021）。`check_script` の W「物差しの無い0.5度」は既知（日本語の「度」は摂氏に聞こえる）。画の札の「℃」は映像方針で「−0.5°」のままにするか決める
12. **聞き役の言い方**＝c213（毎回、行けたわけじゃないんだ）・c216（不具合の並びの直後へ）・c319（降りるのは、順調そうだね）・c701（受けを「広く使われている」）・ca02（まとめにして ca03 を「そう。」で受ける）・cb12（運んでいるだけで、沈みかけたんだね）・cc08（外して cc10 に「分かれる所は？」）。質問の割合を60%に収めるため c106 を反応に・c910 は反応のまま

### 0-2. ④で見つかった設計図の誤り（第1版 §0-2 のまま）
- D10「10:47:02・3冊とも」→ **送った時刻は USCG だけ**（c408 で帰属）／「3つの国の調べ」→ **米国2・カナダ1**（c108・c203）／「ずれた**だけ**」の「だけ」は客の1人の言葉（c105）
- 「09:19 最初の交信 I hsvr trscking」→ **母船の側の字**・USCG は 9:18 から「k」（c317）／「中からは開けられない」の字は3冊に無い→「外の人がボルトを外すまで出られない」（c311・c520）
- 文字の遅れ・予定の長さ・重りの意味・外へ知らせた流れ・ROV の手配・事故のときの窓＝**🆕 D 番号の無い割れ**
- c6「潜るたびに擦れていた」は3冊に無い／屋外の保管は **195日＝半年あまり**／USCG は結論で「損ねた」と言い切る（cb06）／TSB の1.11 は前提つき（c919）／「3冊が一致＝炭素繊維の筒」→「**窓ではなく船体の炭素繊維の側**」（cc09・cd02）
- 🆕④'：設計図（sources・materials・claims_check_A）に CEO の名前が8か所＝伏せた（④'・名前の網）。⚠️ 過去のコミットの履歴には残る

### 0-3. ④'でしたこと・重い直し・映像方針へ渡すもの
- **照合の係7本**（章で割った6本＋通し読み1本・同時2本・検証役なし・画像なし）＝所見234件（🔴12・🟡137・🟢85）→ 🔴12件は G0 が pg22.py で原文に引き直した（全件、係の指摘どおり）。扱い＝`ledger22.md`
- **重い直し（🔴）**：c107（壊れたのは海の底ではなく約500m上の水の中・誰なら止められたのか）／c208（2023年の初め→潜航の季節の初め）／c404（generally considered＝ふつう十分とされる・米沿岸警備隊の帰属）／c419（記録は時刻と深さだけ＝c414 の音の記録と矛盾）／c606（継ぎ目は米沿岸警備隊だけ＝3冊が重なるのは炭素繊維の筒の側）／c814（indicated＝とみられた）／ca03（if any＝傷んだかは分からない）／ca22（調べなかったのは会社）／cb13（not likely・主語と述語）／cd04（some・dismissed）
- **字数の直し**：直しで +643字（13,949字）→ 足しの言い添え（🟢・任意）を戻し、長い言い回しを詰め、細部3つ（cb07 の給料の後払い・cb09 の免除の申し込み・c811 の届き方の割れ）と cb10 の道のりを外し、呼び名をそろえて（米運輸安全委員会＝18か所）幅の内へ
- **映像方針へ（画の欄の食い違い・語りは原文どおり）**：c514（語りは米空軍の輸送機・画は米沿岸警備隊の HC-130）／c609（語りは海の底の映像・画は9月に回収した破片）／ca05（音の印を水の中に・15:20ごろ 0m の点は NTSB 図19 を画像で）／cc04（語りは NTSB・画は米沿岸警備隊の記者会見）／c901（NTSB 図18 の右＝模型の端は c903〜c904 へ）／cb12（凡例の日付）／c910（MBI 図143 の数は事故のあとに端材で数えた物＝札で分ける）
- **書類の再現図69 → 約35に減らす案（映像方針で決める）**：

| 種類 | カット | 案 |
|---|---|---|
| 交信の記録（付録A）8 | c317・c318・c401・c403・c404・c406・c407・c408 | 4つ（c317・c401・c406・c408）は吹き出しの形（潜水艇＝左・母船＝右）で残す。c403・c404＝船首の上の母船と潜水艇の位置の模式／c318＝予備の装置の模式／c407＝時刻の帯（5分あまり途切れる） |
| 潜航の表（付録B・NTSB 表2）10 | c212〜c216・c813・ca01・ca02・ca15・cb14 | 表は c212 の1回。c813＝バハマの潜航の地図と点（番号の列を「回数」と読ませない）／c213・ca01＝点の並び（届いた回を明るく）／c214〜c216＝年表に不具合の印／ca02＝タイタニックの船首の線画（左舷の船首にぶつかる）／ca15＝模式／cb14＝深さの棒 |
| 職の表・人の数 3 | c207・c208・c303 | 組織の図（席が埋まった／空いた）・人の図（24＋17） |
| 証言・報告の一節（英字＋訳）18 | c705・c710・c712・c716・c717・c718・c719・c806・c810・c811・c919・ca09・ca11・cb06・cb18・cc13・cd05・cd06 | 引用カードとして残す（証拠の字）。人の言葉（c705・c712・c718・c806・ca11）は人の輪郭＋吹き出し |
| 要点の札 30 | c203・c209・c211・c706・c802・c804・c816・c902・c915・c922・ca04・ca12・ca13・ca23〜ca25・cb02・cb08・cb16・cb17・cc02・cc03・cc05〜cc08・cc11・cd02〜cd04 | 模式・棒・帯に替えられる候補＝c706（棒）・c915（端材を18に切る図）・c922・ca23〜ca25（監視装置の画面の色・センサー8つのうち3つが灰色・基準の出どころの矢印）・cb08（技術部長の席が空いた組織の図）・cb16（帯）・cb17（目盛り＝35と48の線）・cc02・cc03・cc05・cc06・cc11（3冊の色分けの3列）・cd02〜cd04（3つの問いのカード） |

- **未達・残っている粗**＝Vault の引き継ぎ §4

## 1. ④で決めたこと

### 1-1. 題（§B4・🆕 10-13 の型＝〈一目で事件が分かる語〉＋インパクトのある1句。〈事件名〉の真相【事故検証】【ゆっくり解説】）
- 🆕 **承認①（2026-10-14・④'のチャット）＝保留。最有力は A（70字）**（カズヤくん）。④'が推した「事故の11か月前」（73字）は選ばれなかった＝⑥でアップロードの前にもう一度決める
- 型は記憶 `feedback-jiko-title-form` の 10-13 の項（21本目の題「ツインタワー激突まで、軍に残された時間はわずか9分だった。9.11アメリカ同時多発テロの真相【事故検証】【ゆっくり解説】」）で確かめた。「N人が亡くなった」は入れない形。「死亡」を使わない。【映像あり】は映像方針で ROV・記者会見の実効の幅を測ってから（付けるなら先頭）
- 頭の語＝「タイタニック観光の潜水艇」（事件名より先に絵が浮かぶ語）。末尾の事件名＝「タイタン号潜水艇事故」

| 案 | 題 | 字数 | 根拠（台本のカット＝原文） |
|---|---|---:|---|
| **A（④の推奨）** | タイタニック観光の潜水艇、11か月前に「大きな音」。それでも会社は4日後にまた潜った。タイタン号潜水艇事故の真相【事故検証】【ゆっくり解説】 | 70 | c104・c105＝NTSB p.36・USCG p.233〈225〉・TSB §2.1.1（4 days before the subsequent dive）。冒頭の引きと同じ事実＝題と本編が食い違わない |
| B | タイタニックへ潜る潜水艇、安全の余裕は決まりの1.25に届かない1.11だった。タイタン号潜水艇事故の真相【事故検証】【ゆっくり解説】 | 67 | c9＝TSB §1.15。⚠️ 安全率は本編の後半＝題で引いて冒頭で回収できない。⚠️「決まりの1.25」は言い過ぎ（TSB の字は required・1.25 は会社が ISO に合わせた値＝TSB §1.12.2）＝使うなら「必要な1.25」（c917 と同じ）。1.11 は周りの向きだけ・試料が実物を代表するならの前提つき（TSB §1.15） |
| C | タイタニックの海で途絶えた潜水艇、外へ知らせたのは8時間後だった。タイタン号潜水艇事故の真相【事故検証】【ゆっくり解説】 | 60 | c506＝TSB §2.5（8 hours and 8 minutes）。⚠️ 救助の遅れを芯に見せると「待たなければ助かった」と読める＝TSB §2.5「どんな救助でも結果は変わらなかった」とぶつかる |

### 1-2. サムネの赤（§B5＝「犠牲N人＋核心」・空白こみ10〜14字・「死亡」は使わない）
- ✅ **承認①（2026-10-14）＝A「犠牲5人 異音の4日後も潜航」**（カズヤくん・④の推奨どおり）
| 案 | 赤の言葉 | 字数 | 根拠 |
|---|---|---:|---|
| **A（④の推奨）** | 犠牲5人 異音の4日後も潜航 | 14 | 題 A と同じ芯（c104・c105） |
| B | 犠牲5人 安全率1.11 | 12 | c9（TSB §1.15） |
| C | 犠牲5人 通報まで8時間 | 12 | c506（TSB §2.5）＝題 C と同じ注意 |
- 黄＝「タイタン号事故の真相」（10字）。H 型は v1 が標準（大きな語＝「タイタン」）。🔴 地に ROV の映像のコマ（Pelagic＝第三者）は使わない（10-14 の決め）・実在の顔と数を並べない（§B5-4）。地の候補（A＝米政府の写真）は映像方針・⑥で

### 1-3. コメントの問い（§B3-7b＝誰でも気軽に答えられる・責める相手を作らない・です・ます・3行以内＋🆕 10-13「あなたは」から）
- ✅ **承認①（2026-10-14）＝C「あなたは、もし乗れるとしたら、深い海の底を自分の目で見てみたいですか。よければ、コメントで教えてください。」**（カズヤくん・下の④の注を見たうえで C）＝cd09 に入れた（④'）
| 案 | 問い |
|---|---|
| **A（④の推奨＝cd09 に入れた）** | あなたは、この事故のことを、この動画を見る前から知っていましたか。よければ、コメントで教えてください。 |
| B | あなたは、この動画で、いちばん驚いたのはどこでしたか。よければ、コメントで教えてください。 |
| C | あなたは、もし乗れるとしたら、深い海の底を自分の目で見てみたいですか。よければ、コメントで教えてください。 |
- C は「乗りたいか」を問う＝5人が亡くなった事故の回では軽く聞こえる恐れ（④の判断）

### 1-4. そのほか
- **人**（kousei §8）＝語りで名前を出すのは CEO だけ（c207 の1回・台本は〈CEOの名前〉）。タイタニックの専門家（TSB は副操縦士）と客3人は役割と人数（年齢・国籍は言わない）。船長・通信班の長・技術部長・元運航部長は肩書き。客の言葉は「当時の客の1人」
- **記録の音**＝鳴らさない（10-14）。NOAA の録音・通信班の映像（CG 141）は使わない。付録A の交信は**語りと字幕だけ**・画面は書類の再現図（打ち間違いのまま・訳は字幕）。「this is ph」「hi PH」（10:12）は画面に出しても人に結び付けない
- **噂**（kousei §9）＝ゲーム機のコントローラーは c217（報告書は「手で持つ無線のコントローラー」・どれも原因としない）／叩く音は c511・c512（3冊は触れない→爆縮は最初の通報より前）／米海軍の探知は**入れない**（3冊に無い・報道の原文を確かめていない＝§5）
- **単位**＝メートルを先（§B1-2）。時刻は c306 でニューファンドランドの夏時間と1回断った。語りは「10時47分2秒」、画面の札は「10:47:02」（§B1-3）
- **死の語**＝「亡くなった」。爆縮の中の様子は描かない・秒（ミリ秒）の数で「一瞬」を言わない（「一瞬（米沿岸警備隊）」まで＝c411）
- **冒頭は実写だけ**（c101〜c109＝ROV 2本〈引用・額装〉・USCG の記者会見・HC-130J・指令センター）。爆縮の瞬間の映像は存在しない＝再現イラスト・アニメを冒頭に置かない
- **決め所の画面なし**（10-07）＝旧版の決め所16は語りに溶かした。原文照合は出典の欄（§2）

### 1-5. 割れる時刻と数（台本で1つに決めた所＝図の札もこの値）
| 項目 | 台本 | 別の言い方（台本では言わない・帰属で並べた） | 出典 |
|---|---|---|---|
| 最後の文を送った時刻 | 10時47分2秒ごろ・3,341m（**米沿岸警備隊の記録**と帰属＝c408） | TSB・NTSB は送った時刻を書かない（⚠️ kousei §6-1 の「3冊とも」は誤り＝カードの g2 #12） | USCG p.35〈27〉 4.1.49 |
| 壊れた時刻と、文が届いた順（D10） | 「送ったのは壊れる前」は両方。届いたのが前か後かは分かれる（c411〜c415） | USCG＝10:47:09ごろ壊れ 10:47:26 に受信（壊れた後）／TSB＝10:47:26.903 に画面→5.397秒後に壊れた（壊れる前）。受信の時刻（26秒・32秒）は2冊で合う | USCG 4.1.51・4.1.54・4.1.55／TSB §1.3.2・§2.1 |
| 文が届くまでの遅れ（🆕 D 番号なし） | 言わない | USCG 約15〜30秒（4.1.54.1）／TSB 約2.2秒（脚注15） | 同上 |
| 重りを2つ落とした意味（🆕 D 番号なし） | 両方を並べた（c410） | 米2機関＝この深さのふつうのやり方／TSB＝海底まで約500m・いつもより早い・理由は分からない | NTSB p.17・USCG p.6〈vi〉／TSB §1.3.2・§2.1 |
| 壊れた深さ（D11） | 約3,350メートル（c418） | 3,341・3,346・3,350・3,355・3,363m | USCG・TSB・NTSB |
| 発見の時刻（D12） | 6月22日の午前・米2機関9時40分ごろ／カナダ10時40分ごろ（c517） | USCG の中に 8:40（p.269）・10:30（p.325）も | USCG p.7〈vii〉・NTSB p.20・TSB §1.3.3 |
| 外へ知らせるまで（D14） | 約8時間（カナダの調べで8時間8分＝c506） | USCG 本文「約7時間23分」・分析「7時間の遅れ」（自身の時刻と合わない） | TSB §2.5 |
| 外へ知らせた流れ（🆕 割れ） | 18:27 の電話は切れた（船長の陳述）・18:55 の電話から「ボストンの米沿岸警備隊へとつながっていった」（c505） | TSB＝JRCC が RCC ボストンへ電話を回した／USCG＝19:10 にカナダ沿岸警備隊へ→ボストンへ連絡を、と案内／NTSB＝19:10 に RCC ボストンへ | USCG 4.1.64・4.1.65／TSB §1.3.3／NTSB p.18 |
| 捜索の広さ（D15） | 約4万1,000平方キロ（TSB の約12,000平方海里＝c510） | USCG p.7 12,145平方海里・p.42 は同じ数を平方マイル | TSB §1.3.3 |
| 最初の ROV 船の時刻（D13） | 言わない（c513） | TSB 06:06・USCG 05:17・NTSB 15:00ごろ | — |
| ROV を手配したのは誰か（🆕 割れ） | 言わない（「米空軍の輸送機でニューファンドランドまで運ばれた」まで＝c514） | TSB＝米海軍が手配／USCG・NTSB＝会社が Pelagic と米空軍に | TSB §1.3.3／USCG 4.1.69・NTSB p.20 |
| 母船の乗員（D1） | 40人あまり（c303） | TSB 41・USCG／NTSB 42 | TSB §1.3.1 |
| 母船の乗客（TSB） | 乗客に数えられる人が24人・決まりの上限は12人（c302・c303） | 「観光客24人」ではない（カナダの法の定義＝会社の人も客もその家族も） | TSB §1.20.1.1・§1.20.1.2 |
| 母船の長さ（🆕④'） | 70メートル近い（c301） | NTSB 220フィート（p.14）＝67.1m・表E-2 は 220.4ft＝67.2m／TSB 表1 69.07m | NTSB p.14・p.85・TSB 表1（§1.1） |
| 現場までの距離（D3） | 約700〜800キロ（④'で幅に＝米2機関の370海里＝約685キロと TSB の約425海里＝約787キロ・c219） | TSB 約425海里 | USCG p.5〈v〉・NTSB p.1 |
| 現場に着いた時刻（D4） | 6月18日の早朝（c306） | TSB・NTSB 04:00／USCG 5:15 | TSB §1.3.1 |
| 予定の長さ（🆕 割れ） | 言わない | TSB 11時間15分／NTSB 約8時間 | TSB §1.3・NTSB p.16 |
| 最初の文字のやりとり | 「付録の記録」の 9時19分（c317）＝「最初の交信」と言わない | USCG は 9:18:16 から「k」「a」のやりとり・付録A の1行目は母船の側の字 | TSB 付録A・USCG p.32〈24〉 |
| 降りる速さ | 毎分33メートル（母船の画面＝母船が送った文・c319） | NTSB 毎分30m | TSB §1.3.2・USCG p.33〈25〉 |
| 参加費 | 2023年は1人最大25万ドル（c210） | 事故の回の客3人は 25万・25万・15万ドル（USCG p.18〈10〉＝言わない） | TSB §1.23・USCG p.64〈56〉 |
| タイタニックに届いた回数（D17） | 13回（c213＝米2機関・付録B の 3840 の行） | TSB 本文は14回 | NTSB p.14・USCG p.13〈5〉 |
| 創業 | 2009年に始まった会社（c204） | 法人化は TSB 2011／USCG 2009-08-31 | TSB §1.23・USCG p.59〈51〉 |

## 2. 照合の表（出典の欄そのもの＋機械の照合）

- 決め所（★）が0＝`tools/check_facts.py` の照合は働かない。21本目と同じく **§4 の全カットの出典の欄に原文の字をバッククォートで書き**、`v1_build/quotes22.py` で3冊の文字の層に全片を当てた（結果＝`v1_build/quotes22_result.tsv`）
- 揃え＝NFKC・小文字・空白（NBSP を含む）を消す・ダッシュと引用符の揺れを揃える・行末ハイフンを消した形でも探す・「…」で区切った4字以上の片ごと。判定＝書いた資料の書いた頁（USCG・NTSB）・節（TSB）にあるか

| 判定 | 片 |
|---|---:|
| OK（書いた頁・節にある。TSB の脚注は節を書かずに引いた） | 404 |
| 近・別頁・別節・無し | 0 |

- ⚠️ この照合は「その字が資料にあるか」まで。**言い換えの強さ（likely・may・suggested を落としていないか）と帰属は人が見る**＝④' の芯
- 原文の束（片の出どころ・ぼかしの注）＝`src/cards/`（係6本が3冊の文字の層で照らした片 1,400あまり・不一致0）
- 資料に素の形で無い数（換算・計算）＝§9 に式

## 3. 章ごと（始まりは句読点なし÷365 の積み上げ）

| 区切り | 章 | 始まり | カット | 句読点なし（目安） | 分 | 写真・実写 | 聞き役 |
|---|---|---|---:|---:|---:|---:|---:|
| c1 | つかみ | 0:00 | 9 | 370（365） | 1.01 | 9 | 2 |
| c2 | 第1章　タイタニックへの観光潜航 | 1:00 | 19 | 1,129（1,095） | 3.09 | 3 | 6 |
| c3 | 第2章　6月18日の朝 | 4:06 | 19 | 1,021（1,095） | 2.80 | 5 | 5 |
| c4 | 第3章　10時47分 | 6:54 | 19 | 1,116（1,095） | 3.06 | 2 | 6 |
| c5 | 第4章　96時間 | 9:57 | 23 | 1,359（1,278） | 3.72 | 13 | 7 |
| c6 | 第5章　海の底の残骸 | 13:41 | 19 | 1,028（1,095） | 2.82 | 15 | 5 |
| c7 | 第6章　炭素繊維の筒 | 16:30 | 19 | 1,101（1,095） | 3.02 | 0 | 5 |
| c8 | 第7章　1つ目の船体 | 19:31 | 19 | 1,027（1,095） | 2.81 | 3 | 5 |
| c9 | 第8章　2つ目の船体 | 22:19 | 23 | 1,357（1,278） | 3.72 | 7 | 7 |
| ca | 第9章　2022年7月15日の音 | 26:02 | 26 | 1,518（1,460） | 4.16 | 1 | 8 |
| cb | 第10章　最後の冬と2023年 | 30:12 | 19 | 1,073（1,095） | 2.94 | 5 | 5 |
| cc | 第11章　3つの報告書が出した答え | 33:08 | 13 | 697（730） | 1.91 | 3 | 4 |
| cd | 終章　3つの問いの答え | 35:03 | 9 | 461（502） | 1.26 | 3 | 2 |
| ed01 | 共通エンディング | 36:19 | — | 46 | 0.13 | — | — |
| **計** | | **36:26** | **236** | **13,303** | **36.45** | **69** | **67** |

- 事故の瞬間（10:47:09／10:47:32.3）は c411〜c414＝約9分40秒（尺の約27%・競合の中央値 約32%）
- 章名は本文と突き合わせた（§4-11）：「観光潜航」＝c210〜c213・「6月18日の朝」＝c306・「10時47分」＝c408・「96時間」＝c518・「海の底の残骸」＝c601・「炭素繊維の筒」＝c702・「1つ目／2つ目の船体」＝c801・c901・「2022年7月15日の音」＝ca03〜ca05・「最後の冬と2023年」＝cb01〜cb19・「3つの報告書が出した答え」＝cc01・「3つの問いの答え」＝cd01

## 4. 台本

### つかみ（9カット）

**c101** 🔧 ／ 実写 ROV「尾部」（NTSB ドケットの Pelagic video 1 of 2＝`04_ROV SNIPS-Rel.mp4`・2023-06-22・撮影は Pelagic Research Services の ROV＝第三者＝引用・額装・改変なし・出典「映像：Pelagic Research Services（米沿岸警備隊・NTSB 公開）」・左上の焼き込み「Depth (m): 3775」は残る＝語りは「約3,800メートル」・冒頭の区間は前半（10秒目から尾部）・秒は映像方針で＝副題「2023年6月22日の海の底」） ／ USCG p.7〈vii〉（`discovered the aft tail cone and other debris of the TITAN on the seafloor.`）・TSB（`to approximate the depth of the ocean floor at the location of the Titanic’s bow`）
> 2023年6月22日。北大西洋、タイタニックの眠る深さ約3,800メートル。
> 海の底で、無人の探査機のカメラが、潜水艇の尾部をとらえた。

**c102** ／ 実写 USCG の記者会見「残骸の発見」（DVIDS 888022・2023-06-22・A・登壇は公的な任務の人・語りは会見の発言を引かない＝副題「6月22日の記者会見（米沿岸警備隊）」） ／ USCG p.7〈vii〉（`which occurred at approximately 10:47 a.m. on June 18, 2023`）・TSB §1.3.3（`The U.S. Coast Guard indicated that the debris field was conclusive evidence of a catastrophic loss of the submersible.`）
> 4日前に連絡が途絶えた潜水艇、タイタンの残骸だった。
> アメリカ沿岸警備隊は、潜水艇が壊れた決定的な証拠だと示した。

**c103** ／ 実写 HC-130J の B-roll（DVIDS 888012・2023-06-21・A・基地での撮影＝副題「捜索に出た米軍の輸送機（6月21日）」） ／ NTSB p.9（`All five persons on board the vessel died.`）・USCG p.35〈27〉（`suffered a catastrophic implosion`）
> 乗っていたのは5人。全員が亡くなった。
> 潜水艇は、深い海の水の力に、押しつぶされていた。

**c104** ／ 実写 ROV「前のドーム」（NTSB ドケットの Pelagic video 2 of 2＝`07_ROV SNIPS-Rel.mp4` の前半・第三者＝引用・額装＝副題「海の底の残骸（6月22日）」） ／ NTSB p.36（`mission specialists inside the Titan and the crew of a small boat on the surface heard a “loud bang”`）
> その11か月前。同じ潜水艇の中にいた人たちと、
> 海面の小舟の人たちが、大きな音を聞いていた。

**c105** ／ 実写 ROV「後ろのドーム」（07 の後半・第三者＝引用・額装＝副題「海の底の残骸（6月22日）」） ／ USCG p.233〈225〉（`was caused by a shift in the TITAN’s position within its frame`）・TSB §2.1.1（`4 days before the subsequent dive on 19 July 2022`）
> 会社は、音の原因を「潜水艇が、枠の中でずれたため」とした。
> そして4日後、また潜った。

**c106** 🔧 ／ 実写 USCG の記者会見 888022（別の区間） ／ NTSB p.36（`The Titan completed three additional dives following dive 80`）・NTSB p.36（`the submersible reached 3,840 meters (12,598 feet) on dives 81 and 82`）
> Q: 大きな音がしたのに、また潜ったんだ。
> その夏のうちに3回。うち2回は、タイタニックの深さまで潜っている。

**c107** 🔧 ／ 実写 指令センターの B-roll（DVIDS 887734・2023-06-20・ボストンの第1管区・当直の隊員＝公的な任務・A・器 2720×1530 の実効の幅は映像方針で測る＝副題「捜索の指令センター（6月20日・ボストン）」） ／ —
> この潜水艇は、深い海の中で、何が壊れたのか。
> なぜ、潜り続けたのか。そして、誰なら止められたのか。

**c108** ／ 実写 ROV「尾部」（04 の後半・冒頭の c101 と別の区間・第三者＝引用・額装） ／ USCG p.1（`Report of the Marine Board of Investigation`）・NTSB p.76（`Report Date: October 2, 2025`）・TSB §4.2.4（`It was officially released on 17 June 2026.`）
> Q: 答えは、もう出ているの？
> アメリカの2つの調べと、カナダの調べが、それぞれ報告書にまとめている。

**c109** 🔧 ／ 実写 USCG の記者会見 888022（別の区間）→ 第1章の扉 ／ —
> この潜水艇は、客を乗せて、タイタニックを見に行っていた。

---

### 第1章　タイタニックへの観光潜航（19カット）

**c201** ／ 実写 タイタニックの船首（Commons「Titanic wreck bow.jpg」・2004年の調査・クレジット「Courtesy of NOAA/Institute for Exploration/University of Rhode Island」＝A の見込みは弱い＝出典の書き方と額装か全面かは映像方針で＝副題「タイタニックの船首（2004年の調査）」） ／ TSB §1.3（`a descent of approximately 3800 m`）
> Q: タイタニックって、そんなに深いところにあるの？
> 北大西洋の、深さ約3,800メートルの海の底だ。
> 富士山の高さよりも、まだ深い。

**c202** 🔧 ／ 図 模式 富士山（3,776m）を逆さにした高さと、タイタニックの深さ（約3,800m）の比べ・横に1円玉と乗用車の札（式は §9） ／ NTSB p.10（`At the depth of the Titanic wreckage site, water pressure is 5,554.5 pounds per square inch.`）
> そこでは、水の重さがのしかかる。
> 1円玉1枚の広さに、乗用車1台ぶん、約1.2トンの力がかかる計算だ。

**c203** ／ 図 再現 3つの報告書（表紙の題と日付だけを並べた図＝米沿岸警備隊の海難調査委員会 2025年8月／米国の運輸安全委員会 2025年10月／カナダの運輸安全委員会 2026年6月） ／ USCG p.5〈v〉（`August 4, 2025`）・NTSB p.76（`Report Date: October 2, 2025`）・TSB §4.2.4（`It was officially released on 17 June 2026.`）
> この動画で主に使うのは、3つの報告書だ。
> アメリカ沿岸警備隊の海難調査委員会、アメリカの運輸安全委員会、
> そして、カナダの運輸安全委員会がまとめた。

**c204** ／ 図 地図 北米の東半分（会社の本社＝米国ワシントン州エバレット・母船の港＝カナダのセントジョンズ・タイタニックの位置の3点だけ） ／ TSB §1.23（`OceanGate was first established as a limited liability company in 2009`）・§1.23（`OceanGate was headquartered in Everett, Washington`）
> 潜水艇タイタンを造り、動かしていたのは、アメリカの会社、オーシャンゲート。
> 2009年に始まった会社で、本社はアメリカ西海岸のワシントン州にあった。

**c205** 🔧 ／ 図 線 タイタンの横から見た線画（NTSB 図3 をなぞる・全長6.7m と「5人まで」の札だけ） ／ NTSB p.10（`The 22-foot-long submersible Titan was designed, built, and operated by OceanGate Inc.`）・TSB §1.2.1（`designed to accommodate up to 5 people`）
> タイタンは、全長6.7メートル。中には、5人まで乗れた。
> 母船に運ばれて現場まで行き、そこから潜る、小さな潜水艇だ。

**c206** ／ 図 線 同じ線画（人が乗る部分＝筒と両端のドームを明るく・札「炭素繊維の筒」「チタンのドーム」） ／ TSB §1.10.1（`The Titan’s pressure hull consisted of a carbon fibre cylinder that was capped at either end by titanium domes.`）・§1.2.1（`Two hemispherical domes made of titanium were fitted to either end of the cylinder.`）
> 人が乗るのは、炭素繊維の筒の両端を、チタンの半球のドームでふさいだ部分。
> 深い海の水の力に耐える殻で、耐圧殻という。

**c207** 🔧 ／ 図 再現 TSB 表4（2023年の上級の8つの職と、その席が埋まっていたか＝欄は英字のまま・CEO の行を明るく） ／ TSB §1.3（`the Titan’s pilot, who was OceanGate’s chief executive officer (CEO)`）・§1.9.1（`had piloted it on numerous previous dives, including dives to the Titanic in 2021 and 2022`）・§1.23.1（`As a small company, OceanGate was led primarily by the CEO.`）・§1.23.1（`The CEO was integrated into all aspects of the company, including human resources, finance, operations, and submersible design and construction.`）
> Q: 会社を動かしていたのは、誰なの？
> 会社のトップ、CEO の〈CEOの名前〉だ。潜水艇の操縦も、自分でしていた。
> 小さな会社を、CEO が主に率い、人事やお金から設計まで、すべてに関わった。

**c208** 🔧 ／ 図 再現 同じ表4（2023年の潜航の季節の初めの社員の数「15」の札を足す） ／ TSB §1.23（`At the beginning of the 2023 operating season, OceanGate had 15 employees`）・§1.23.1（`viewed the design, development, and operation of the Titan as being experimental`）・§1.23.1（`There was no precedent for diving a human-occupied carbon fibre submersible to the deep ocean`）
> 2023年の潜航の季節の初め、社員は15人。
> 会社は、タイタンの設計も運航も、「実験的」とみていた。
> 人を乗せた炭素繊維の潜水艇が深海へ潜った例は、それまで無かった。

**c209** ／ 図 再現 同意書の要点（USCG p.71 の箇条の英字＝`experimental submersible vessel`・`not been certified by any regulatory body`・「death」の数え＝9） ／ USCG p.71〈63〉（`The submersible had not been certified by any regulatory body.`）・p.71〈63〉（`A portion of the expedition would be conducted inside an experimental submersible vessel.`）・p.71〈63〉（`The liability waiver mentions death 9 times`）
> 客は参加の前に、責任を問わないという同意書に署名した。
> そこには、どの規制の機関の認証も受けていない、実験的な潜水艇だと書かれ、
> 米沿岸警備隊の委員会の数えでは、「死」に9回触れていた。

**c210** ／ 図 棒 参加費（2021年 105,129ドル → 2022年・2023年 25万ドル＝円は1ドル140円で計算と左下に） ／ USCG p.64〈56〉（`rising from $105,129 in 2021 to $250,000 for both 2022 and 2023.`）・TSB §1.23（`the cost for 1 passenger to join was up to 250 000 U.S. dollars`）
> Q: それでも、お客さんは乗ったの？
> 乗った。参加費は、2023年は1人最大25万ドル。
> 1ドル140円で計算すると、約3,500万円だ。

**c211** 🔧 ／ 図 再現 会社の計画書の一節（NTSB 脚注8 が引く `guests who help fund OceanGate expeditions` の英字＋訳は字幕） ／ NTSB p.15（`OceanGate referred to its clients as “mission specialists.”`）・USCG p.300〈292〉（`reclassifying their passengers as “mission specialists” to conceal their illegal passenger operations`）・USCG p.317〈309〉（`to conceal that their mission specialists were actually paying passengers`）
> Q: お客さんは、会社から何と呼ばれていたの？
> ミッション・スペシャリスト。米沿岸警備隊の委員会は、
> 料金を払う乗客だと隠すための呼び方だった、とみている。

**c212** ／ 図 再現 TSB 付録B の表（27行・欄は英字のまま＝日付・深さ・時間・人数・母船・目的・備考） ／ TSB 付録B（`The term “dive” refers to dives to any depth where there were people on board the submersible and the submersible was on life support.`）・付録B（`Dives made by the Titan between 2021 and the occurrence at the Titanic wreck site, in Canadian waters, or in Canada’s exclusive economic zone`）
> カナダの報告書の付録に、人が乗った潜航の記録の表がある。
> タイタニックの現場とカナダの海で、2021年から事故までの3つの夏に、27回。

**c213** 🔧 ／ 図 再現 同じ表（深さ「3840」の13行を明るく） ／ NTSB p.14（`only successfully completed 13 dives to the wreck`）
> そのうち、タイタニックの深さまで届いたのは、13回だった。
> Q: 毎回、行けたわけじゃないんだ。

**c214** 🔧 ／ 図 再現 同じ表（1行目の備考 `Forward dome fell off the submersible during recovery` を明るく） ／ TSB 付録B（`Forward dome fell off the submersible during recovery`）・TSB（`Following this dive, OceanGate began using 18 securing bolts.`）
> 表の備考の欄には、不具合も並ぶ。
> 1行目は、回収のときに前のドームが外れて落ちた記録だ。
> このあと会社は、ドームを留めるボルトを18本にした。

**c215** 🔧 ／ 図 再現 同じ表（`Batteries died on approach to LARS`・時間「27」を明るく） ／ TSB 付録B（`Batteries died on approach to LARS`）・NTSB p.36（`so the Titan remained on the surface with occupants aboard overnight.`）
> 電池が切れ、海も荒れて台に固定できず、
> 人を乗せたまま海面で一晩を過ごし、潜航が27時間に及んだ回もあった。

**c216** 🔧 ／ 図 再現 同じ表（推進器・重り・追跡と通信の備考を明るく） ／ TSB 付録B（`Starboard thrusters failed`）・付録B（`Incident with drop weight`）・TSB §1.23.1（`OceanGate primarily used a trial-and-error approach to operations`）
> 推進器の故障、重りの不具合、通信の不具合。
> Q: トラブル、多すぎない？
> カナダの報告書は、会社が主に、やってみて直すやり方で運航していた、と書いている。

**c217** 🔧 ／ 実写 MBI 図65 前の艇 Cyclops I の中のコントローラーとキーボード（USCG 報告 p.103・2023年10月に MBI が撮影・A＝副題「前の艇 サイクロプス1 の操縦の道具（2023年10月撮影）」） ／ TSB §1.10.5（`The pilot operated the thrusters using a handheld wireless controller`）・NTSB p.11（`a wireless, battery-operated controller that communicated with control software`）・USCG p.103〈95〉（`the CYCLOPS I being operated with a PlayStation® controller`）・USCG p.103〈95〉（`Photo of the Logitech PlayStation controller inside CYCLOPS I taken by the MBI`）
> 操縦は、ゲーム機のコントローラーだった、とよく語られる。
> 報告書は、手で持つ無線のコントローラーとだけ書き、原因とはしていない。
> 写真は、会社の前の潜水艇の物で、こちらはゲーム機用だ。

**c218** 🔧 ／ 実写 ホライゾン・アークティック（Commons・CC BY-SA 4.0・2022年＝第三者＝額装・改変なし・サムネに使わない＝副題「2021・22年の遠征の母船」） ／ TSB §1.2.2（`In previous years, OceanGate had chartered another vessel, the Horizon Arctic`）
> 2021年と2022年の遠征では、別の船を借りて、母船にしていた。

**c219** 🔧 ／ 図 地図 セントジョンズからタイタニックの現場まで（約685km の線） ／ TSB §1.2.2（`OceanGate first chartered the Polar Prince in March 2023.`）・USCG p.5〈v〉（`approximately 370 nautical miles`）
> 2023年の母船は、カナダの古い船、ポーラープリンス。
> ニューファンドランドのセントジョンズから、約700〜800キロ先の現場へ向かった。

---

### 第2章　6月18日の朝（19カット）

**c301** 🔧 ／ 実写 MBI 図3 ポーラープリンス（セントジョンズの岸壁・USCG 報告 p.14・2023-06-25 に MBI が撮影＝事故の後・A・幅1202＝寄り弱め＝副題「母船ポーラープリンス（事故の後の6月25日に撮影）」） ／ TSB §1.2.2（`The Polar Prince (Figure 4) is a Canadian-flagged general cargo vessel.`）・TSB §1.1（`“Year built” refers to the date the keel of the vessel was laid`）・NTSB p.14（`the 220-foot-long, Canadian-flagged vessel Polar Prince`）
> Q: 母船って、どんな船だったの？
> カナダの船籍の、全長70メートル近い貨物船だ。
> 造り始めたのは、1959年。

**c302** ／ 図 棒 乗客の数（貨物船の決まりの上限12人／この航海24人＝カナダの調べの数） ／ TSB §1.20.1.2（`it was permitted to carry up to 12 passengers.`）・§1.20.1.2（`on the occurrence voyage, it was carrying 24 passengers.`）
> 貨物船なので、乗客として乗せられるのは12人までだった。
> ところがこの航海では、乗客に数えられる人が24人乗っていた。

**c303** ／ 図 再現 乗っていた人の内わけ（TSB §1.3.1 の数＝会社の関係24・乗組員17） ／ TSB §1.20.1.1（`OceanGate passengers, who consisted of the Titan passengers and their family members.`）・TSB §1.3.1（`There were 41 people on board the Polar Prince in total: 24 people associated with OceanGate and 17 Polar Prince crew members.`）
> カナダの決まりでは、乗組員でない人は、会社の人も客もその家族も、乗客に数える。
> 母船に乗っていたのは、全部で40人あまりだった。

**c304** ／ 図 地図 セントジョンズから現場まで（6月16日に出る・6月18日に着く・約685km＝c219 と同じ地図の続き＝母船が台を引く線） ／ TSB §1.3.1（`the Polar Prince departed St. John’s, Newfoundland and Labrador, for the Titanic wreck site (Figure 5) towing the Titan on the LARS.`）
> 6月16日、母船はセントジョンズを出た。
> タイタンは台に載せ、母船の後ろに引いて運んだ。

**c305** ／ 実写 MBI 図5 台（LARS）が岸壁に（白い浮き・USCG 報告 p.16・2023-06-25 撮影・A＝副題「潜水艇を出し入れする台（事故の後に撮影）」） ／ TSB §1.2.1.1（`During launching, the tanks could be flooded with water in order to submerge the LARS and allow the Titan to detach underwater.`）
> この台は、浮きのタンクに水を入れると沈む。
> 潜水艇を載せたまま沈めて、水の中で切り離す仕組みだ。

**c306** ／ 図 帯 6月18日の朝の時刻の帯（左下に「時刻はニューファンドランドの夏時間」） ／ TSB 脚注13（`All times are Newfoundland Daylight Time (Coordinated Universal Time minus 2.5 hours).`）・TSB §1.3.1（`arrived with the Titan in tow on the LARS at 0400 on 18 June`）
> ここからの時刻は、すべて現地、ニューファンドランドの夏の時間で言う。
> 6月18日の早朝、母船は現場に着いた。

**c307** ／ 実写 MBI 図18 航海日誌 6/18 00:00〜06:00（黒い塗りは MBI の物・額装・USCG 報告 p.23・A＝副題「母船の航海日誌（6月18日の早朝）」） ／ TSB §1.3.1（`At 0534, OceanGate held a briefing that provided an overview of the plan for the upcoming dive.`）・TSB §1.3（`the Titan’s pilot, who was OceanGate’s chief executive officer (CEO); the copilot, who was an expert on deep-sea exploration and the Titanic; and 3 passengers`）
> 5時34分、潜航の計画の説明があった。乗るのは5人。
> 操縦するのは CEO 本人。副操縦士は、深海とタイタニックに詳しい専門家。
> そして、客が3人だった。

**c308** ／ 実写 MBI 図21 母船のヘリの格納庫と、中に並ぶ椅子（USCG 報告 p.25・2023-06-25 撮影・A・小さい＝額装＝副題「説明が行われた母船の格納庫（事故の後に撮影）」） ／ TSB §1.3.1（`At 0545, the 5 people boarding the Titan and their personal effects were weighed so that OceanGate could calculate the weight needed for the submersible to descend.`）
> 5時45分、乗る5人と、持ち物の重さを量った。
> Q: 体重まで量るんだ。
> 沈むのに要る重りを、計算するためだ。

**c309** ／ 実写 MBI 図24 母船の小舟2隻（USCG 報告 p.27・2023-06-23 撮影・A＝副題「母船の小舟（事故の後に撮影）」） ／ TSB §1.3.1（`From 0600 to 0800, OceanGate used rigid inflatable boats (RIBs) to transfer the Titan pilot, copilot, and other OceanGate personnel to the LARS`）・§1.3.1（`At approximately 0800, the 3 passengers were transferred from the Polar Prince to the LARS.`）
> 6時から、小舟で、操縦士と副操縦士、会社の人たちを台へ運んだ。
> 8時ごろ、客3人も台へ移った。

**c310** ／ 図 線 上から見た台と艇（NTSB 図4 の上の線画をなぞる・出どころの注なし＝NTSB） ／ TSB §1.3.1（`All 5 people were on board the Titan by 0820.`）・§1.3.1（`At 0824, OceanGate personnel on the LARS closed the Titan’s forward dome, bolted it shut, and used a torque wrench to tighten the bolts.`）
> 8時20分、5人が乗り終えた。8時24分、台の上の会社の人が、
> 前のドームを閉め、ボルトで締めた。

**c311** ／ 図 線 タイタンの横の線画（前のドームの縁に、外から留めるボルトの札） ／ TSB §1.2.1（`The forward dome could be bolted and unbolted from outside the submersible to provide access to the cabin; this was the only way that people could enter and exit the submersible.`）・TSB §2.5（`could not egress on the surface without the Titan first being reattached to the LARS and the forward dome being unbolted by people outside the submersible`）
> Q: 中からは、出られないの？
> 中の人だけでは出られない。前のドームは、外からボルトで締めたり外したりする。
> それが、人が出入りする、ただ一つの道だった。

**c312** 🔧 ／ 図 帯 同じ時刻の帯（08:24 に「艇の中の生命維持へ」の札） ／ TSB §1.3.1（`At this point, the Titan crew and passengers were sealed inside the cabin, and the submersible was using its internal life support system.`）・TSB §1.2.1（`The cabin had an internal life support system that consisted of oxygen tanks`）・§1.2.1（`CO2 scrubbing capability for the same occupancy`）
> この時から5人は、閉じた潜水艇の中で、酸素を足し、
> 吐いた息の二酸化炭素を取る、生命維持の仕組みで息をすることになった。

**c313** 🔧 ／ 図 帯 同じ帯（08:59 5分の一時停止） ／ TSB §1.3.1（`At 0859, all OceanGate personnel took a scheduled 5-minute pause in operations to consider the progress and safety of the operations so far.`）
> 8時59分、会社の人たちは予定どおり5分だけ作業を止め、進み具合と安全を考えた。

**c314** ／ 図 模式 台が沈む3段（水を入れる→台ごと水面の下→艇を切り離す） ／ TSB §1.3.1（`At 0904, OceanGate divers began to fill the LARS’s ballast tanks with water to submerge it.`）・§1.3.1（`By 0905, the LARS and the Titan were submerged.`）・§1.3.1（`At 0914, divers detached the Titan from the LARS, and the Titan began its descent.`）
> 9時4分、台に水を入れ始め、9時5分、台ごと水面の下へ。
> 9時14分、潜水士がタイタンを台から外し、降下が始まった。

**c315** 🔧 ／ 図 模式 重りで沈む潜水艇（線画・下向きの矢印だけ） ／ USCG p.6〈vi〉（`The descent was a free fall through the water column, controlled by the vessel's ballast condition.`）・TSB §1.3（`The occurrence dive on 18 June was the Titan’s first dive to the Titanic`）・NTSB p.16（`It was the first dive of the 2023 expedition to descend below 33 feet (10 meters).`）
> 動力で降りるのではない。重りの重さで、海の底へ向けて沈んでいく。
> この年、タイタニックへ向かう初めての潜航で、
> 10メートルより深く潜るのも、これが初めてだった。

**c316** ／ 図 模式 音で文字を送る（母船の下の送受信機と艇のあいだに音の波・電波は水を通りにくいの札） ／ USCG p.32〈24〉（`Since radio waves do not travel well through water, these modems rely on acoustics to send and receive information`）・p.30〈22〉（`The installed system used abbreviated text fields to communicate between the POLAR PRINCE and the TITAN.`）・p.30〈22〉（`The TITAN was not fitted with a voice communications system capable of communicating while the submersible was operating below the surface.`）
> Q: 潜っている間は、どうやって話すの？
> 電波は、水の中をうまく伝わらない。だから、音の波で短い文字を送り合う。
> 海の中で使える、声の装置は無かった。

**c317** ／ 図 再現 付録A の表の最初の4行（09:19:36〜09:20:02・打ち間違いのまま＝`I hsvr trscking`・`descendingb thru 235`・`i have tracking`・`yeah`・訳は字幕） ／ TSB 付録A（`I hsvr trscking`）・付録A（`descendingb thru 235`）・TSB §1.3.2（`The Titan crew then transmitted a message stating that they were descending through 235 m.`）・TSB §1.3.2（`The surface support team sent a message back stating that they had tracking of the submersible.`）・USCG p.32〈24〉（`the POLAR PRINCE communicated to the TITAN that they have tracking`）
> カナダの報告書の付録には、降りる間の文が、打ち間違いのまま残っている。
> 9時19分、母船が「追跡できている」と送り、潜水艇は「235メートルを通過中」。

**c318** ／ 図 再現 付録A の表（09:23:03〜09:24:05 の3行＝`no atm are you on`・`atm is on`・`do not read you on atm`） ／ TSB §1.3.2（`At 0923, the surface support team received a message from the Titan crew stating that the 2nd acoustic communication and tracking system was not functioning.`）・TSB 脚注16（`It is not known why this system was not functioning.`）
> 9時23分、潜水艇から、予備の通信と追跡の装置が動いていない、と知らせが来た。
> なぜ動かなかったのかは、分かっていない。

**c319** 🔧 ／ 図 線 深さの線（記録の点だけ＝9:19 235m・9:23 436m・9:31 680m・あいだは直線＝模式と左下で断る） ／ TSB §1.3.2（`they could see the Titan descending at 33 m per minute on their display`）・§1.3.2（`At 0953, the surface support team asked the Titan crew if they could see the Polar Prince on their display. The surface support team kept sending this message until 1010 without receiving a response.`）
> 9時28分、母船は、毎分33メートルで降りているのが画面で見える、と送った。
> Q: 降りるのは、順調そうだね。
> ところが9時53分から、母船の問いかけに、しばらく返事が来なくなる。

---

### 第3章　10時47分（19カット）

**c401** 🔧 ／ 図 再現 書類の再現図 TSB 付録A の表（10:11:55〜10:15:39 のうち4行＝10:12 の4行は除く・欄の値は英字のまま＝`lost system oand chat settings`・`yes`・`all good here`・`ack all good`・訳は字幕だけ） ／ TSB §1.3.2（`indicating that the communication system had temporarily stopped working`）・付録A（`10:14:35.5 T all good here`）
> Q: 返事は、また来たの？
> 来た。10時11分、潜水艇から、通信の装置がしばらく止まっていた、と知らせがあり、
> 10時14分には「こちらは全部順調」と送ってきた。

**c402** 🔧 ／ 図 線 深さの線（記録の点だけ＝9:31 680m・10:11〜10:15 2,203→2,289m・10:40 3,149m・10:47:02 3,341m＝米沿岸警備隊の値。あいだは直線＝模式と左下で断る。10:23 と 10:29 の約2,833m は USCG の中で時刻が揺れる＝点を置かない） ／ USCG p.34〈26〉（`from 2,203 m (7,227 feet) to 2,289 m (7,509 feet)`）
> このとき潜水艇は、深さ2,300メートル近くを降りていた。
> 海の底までは、あと1,500メートルほどだ。

**c403** ／ 図 再現 付録A の表（10:23:33・10:25:46 の2行＝`poi orks we are east south east of the nbow`・`we see you east north east of the bow`） ／ USCG p.34〈26〉（`would act as the point of interest and place itself directly above the desired location`）・TSB 付録A（`we are east south east of the nbow`）
> 10時23分からは、タイタニックの船首に対する位置のやりとりが続く。
> 母船が船首の真上へ動き、潜水艇がそこを目がけて進む段取りだった。

**c404** 🔧 ／ 図 再現 付録A の表（10:29:12〜10:31:55 の6行） ／ TSB 付録A（`your position jumps significantly each ping`）・USCG p.34〈26〉（`generally considered to be an adequate signal`）
> 母船は「そちらの位置が、送るたびに大きく跳ぶ」と伝えている。
> 米沿岸警備隊によると、信号の強さは、文字を送るにはふつう十分とされる値だった。

**c405** 🔧 ／ 実写 MBI 図31 船橋の事務室（通信班の持ち場・机と画面・人なし・USCG 報告 p.32・A・全画面には小さい＝寄り弱め＝副題「母船の船橋の事務室（通信班の持ち場・事故のあとに委員会が撮影）」） ／ TSB 付録A（`remember to write down the location and time of niskin deployment`）・USCG p.34〈26〉（`Niskin bottles are used for collecting water samples at various depths`）
> 10時36分、母船は、採水器の話を始めた。
> Q: 採水器って、何をする物？
> 海の水を、深さごとに採る瓶だ。ニスキン瓶という。

**c406** ／ 図 再現 付録A の表（10:36:50〜10:40:56 の8行・打ち間違いのまま＝`when? messages truncated`・`andn location`・`no niskin. never cleaned and string baf`） ／ TSB 付録A（`no niskin. never cleaned and string baf`）・USCG p.34〈26〉（`The depth of the TITAN was 3,149 m`）
> 位置と時刻を書き留めるよう頼む母船に、潜水艇は答えた。
> 「ニスキンは無し。洗っていないし、糸が悪い」。深さは3,149メートルだった。

**c407** ／ 図 再現 付録A の表（10:41:07・10:42:01 の2行＝`ack no niskin`・`a`） ／ TSB 付録A（`ack no niskin`）・付録A（`a = received your last, end thread`）
> 母船は「了解、ニスキンは無し」。10時42分、潜水艇は「受け取った」の印、
> 「a」を1文字だけ返した。このあと、文字のやりとりは5分あまり途切れる。

**c408** ／ 図 再現 付録A の表の最後の行（10:47:26.9 `dropped two wts`＝画面に出た時刻）と、米沿岸警備隊の送った時刻の札「10:47:02（送った）」 ／ USCG p.35〈27〉（`At approximately 10:47:02 a.m., the TITAN sent a message to the POLAR PRINCE, stating, “dropped two wts.”…The depth of the TITAN was 3,341 m.`）
> 米沿岸警備隊の記録では、10時47分2秒ごろ、潜水艇が短い文を送った。
> 「重りを2つ落とした」。深さは3,341メートルだった。

**c409** ／ 図 模式 重りで降りる仕組み（降りる→重りを落として止まる→浮く・NTSB 図3 の艇の線画をなぞる・重りの数と場所は描かない） ／ USCG p.35〈27〉（`weights were released to slow the descent to the intended operating depth or begin the ascent back to the surface`）
> Q: 重りを落としたのは、どうして？
> 重りは、海の底の近くで降りる速さを緩めるときか、浮き上がり始めるときに落とす。

**c410** 🔧 ／ 図 帯 2段の札（上＝米国の2つの調べ「この深さのふつうのやり方」／下＝カナダ「海底まで約500m・いつもより早い・理由は分からない」） ／ NTSB p.17（`which was a standard procedure at this depth to slow its descent`）・USCG p.6〈vi〉（`As the TITAN approached the ocean floor, it followed standard procedure by releasing ballast weights to slow its descent.`）・TSB §1.3.2（`the submersible was approximately 500 m from the seabed`）・§2.1（`Dropping the 2 weights earlier than normal suggests`…`the reason for this is unknown`）
> アメリカの2つの調べは、この深さでのふつうのやり方とみる。
> カナダの調べは、海の底まではまだ約500メートルあり、いつもより早いとする。
> 速さを緩めようとしたとみられるが、理由は分からない、と書く。

**c411** 🔧 ／ 図 帯 時刻の帯（米沿岸警備隊の段＝10:47:02 送った→10:47:08 最後の位置→10:47:09ごろ 壊れた） ／ USCG p.35〈27〉（`At approximately 10:47:09 a.m., the TITAN submersible suffered a catastrophic implosion`）・p.35〈27〉（`resulting in the instantaneous death of all five occupants`）
> 米沿岸警備隊によると、文を送った7秒後の10時47分9秒ごろ、
> 人の乗る耐圧殻が、内側へ押しつぶされた。爆縮だ。5人は、一瞬で亡くなった。

**c412** ／ 図 帯 同じ帯（10:47:11「バン」・10:47:26 受けた を明るく） ／ USCG p.35〈27〉（`heard a sound described by the leader for communications and tracking as a “bang”`）・p.35〈27〉〜p.36〈28〉（`This was the last message that was sent from the TITAN.`）
> 2秒後、母船の通信班は「バン」という音を聞いた。
> そして10時47分26秒、「重りを2つ落とした」の文が母船に届いた。
> 潜水艇から送られた、最後の文だった。

**c413** 🔧 ／ 図 帯 2段の帯（上＝米沿岸警備隊・下＝カナダ。「画面に出た」と「壊れた」の順が上下で逆） ／ TSB §1.3.2（`At 1047:26.903, when the submersible was at 3350 m, a message appeared on the surface support team’s computer`）・§2.1（`The pressure hull’s structural failure happened 5.397 seconds after the text message about dropping the 2 weights appeared`）
> Q: じゃあ、最後の文は、壊れた後に届いたの？
> そこが、調べによって分かれている。カナダの調べでは、
> 文が画面に出たのは10時47分26.9秒。壊れたのは、その約5.4秒後だ。

**c414** 🔧 ／ 図 帯 2段の帯（下の段＝10:47:26.903 画面→10:47:32.066 最後の位置→10:47:32.3 壊れた→10:47:34.522 船体に音） ／ TSB 脚注19（`included a view of the computer being used by the surface support team`）・TSB §1.3.2（`a loud sound, which could be characterized as a thud or a bang, reverberated through the hull of the Polar Prince`）・§2.1（`5.397 seconds after the text message about dropping the 2 weights appeared`）
> カナダの調べが秒まで言えるのは、母船のビデオカメラに、パソコンの画面と、
> 母船に響いた「ドン」という音が、録られていたからだ。

**c415** 🔧 ／ 図 帯 2段の帯（「送った」は両段とも壊れる前・「受けた」10:47:26／10:47:32 は両段で合う・「壊れた」だけが離れる） ／ USCG p.37〈29〉（`At 10:47:32 a.m., the POLAR PRINCE received the ping that was sent at 10:47:08 a.m.`）・TSB §1.3.2（`At 1047:32.066, the surface support team’s computer received the last automated position update`）
> 文を送ったのは、どちらの調べでも、壊れる前だ。
> 母船が受け取った時刻も、米沿岸警備隊とカナダで合っている。違うのは、壊れた時刻だ。
> Q: 届いたのが壊れる前か後かは、調べで違うんだね。

**c416** ／ 図 帯 時刻の帯（10:48「受け取った」を返す・10:49「追跡を失った」を送る・どちらも返事なし） ／ NTSB p.17（`At 1048, the Polar Prince sent a message back to acknowledge the Titan’s message, but they received no response.`）・p.17（`At 1049, the Polar Prince sent the Titan a “lost tracking” message but received no response.`）
> そう。母船は10時48分に「受け取った」と返した。
> 10時49分には「追跡を失った」と送った。返事は、どちらにも無かった。

**c417** ／ 実写 MBI 図37 航海日誌（6/18 06:00〜12:00 の頁・額装・頁の上の印＝「1047 lost communication with TITAN」の1行・USCG 報告 p.38・A＝副題「母船の航海日誌（事故のあとに委員会が撮影）」） ／ USCG p.38〈30〉（`At 11:15 a.m., the Master of the POLAR PRINCE was advised that as of approximately 10:47 a.m., there was a loss of communication with the TITAN.`）・p.38〈30〉（`it stated “1047 lost communication with TITAN.”`）
> 船長に知らされたのは11時15分。そのあと航海日誌に、こう書かれた。
> 「10時47分、タイタンとの通信が途絶えた」。

**c418** ／ 図 線 深さの線（最後の点 10:47:08 3,346.28m で線が止まる・海底は約3,800m の破線） ／ TSB §1.7（`At its last-known depth of 3355 m, the Titan was calculated to be under 33.587 MPa of hydrostatic pressure. This is equivalent to a pressure of 342.49 kg per square cm.`）
> 壊れた深さは、約3,350メートル。
> カナダの調べの計算では、1平方センチに約340キロの水の力がかかる深さだ。

**c419** 🔧 ／ 図 線 同じ図（線の止まった点に寄る） ／ USCG p.269〈261〉（`There were no witnesses to the implosion or video evidence recovered of the implosion`）
> Q: 壊れたところを、見た人はいるの？
> いない。爆縮を見た人も、写した映像も無い。
> 残っているのは、時刻と深さ、そして音の記録だ。

---

### 第4章　96時間（23カット）

**c501** 🔧 ／ 実写 指令センターの B-roll（DVIDS 887734・2023-06-20・c107 と別の区間・A＝副題「米沿岸警備隊の指令センター（6月20日）」） ／ NTSB p.17（`first assumed there was an issue with the acoustic communications equipment`…`sent two to three messages every minute`）・USCG p.39〈31〉（`None of the messages were answered and the TITAN’s location was never reacquired by the POLAR PRINCE.`）
> Q: 母船の人たちは、すぐに助けを呼んだの？
> すぐには呼ばなかった。母船にいた会社の担当は、まず通信の装置の不具合を疑った。
> 1分に2回から3回、文を送り続けたが、答えは無かった。

**c502** ／ 図 帯 会社の手順の流れ（途絶→1時間＋浮上にかかる時間→社内へ連絡→さらに3時間の海面の捜索→外へ・札「事情によっては短くしてよい」） ／ USCG p.39〈31〉（`Internal contacts and backup personnel will be called following 1 hour of no communications plus required surface time`）・p.39〈31〉（`An additional 3 hours of local surface search will be done before contacting outside emergency personnel unless circumstances merit a shorter delay.`）
> 会社の手順では、連絡が途絶えたら、まず浮き上がってくるのを待つ。
> そのあと3時間、近くの海面を探してから、外に知らせる。
> 事情によっては縮めてよい、とも書かれていた。

**c503** ／ 図 帯 6月18日の午後の時刻の帯（15:00 浮上の見込み・海面の捜索を始める） ／ TSB §1.3.3（`the estimated resurfacing time was approximately 3 hours and 13 minutes (at 1500)`）・§1.3.3（`At 1500, with no communication from the Titan, the Polar Prince commenced the 3-hour surface search.`）
> 浮き上がってくる見込みは、15時ごろだった。
> 15時になっても何も現れず、母船は3時間の海面の捜索を始めた。

**c504** 🔧 ／ 図 帯 同じ帯（16:34 陸の班へ電話・18:00 手がかりなし） ／ TSB §1.3.3（`At 1634, as the surface search was ongoing, the master of the Polar Prince called the Horizon Maritime Services Ltd. shore-based emergency team`）・§1.3.3（`By 1800, the surface search had found no signs of the submersible.`）
> 16時34分、船長は、船の会社の陸にいる緊急対応の班に電話した。
> 18時までの捜索で、手がかりは見つからなかった。

**c505** 🔧 ／ 図 帯 同じ帯（18:27 電話が切れた・18:55 カナダの救難調整センターへ→ボストンへ） ／ USCG p.39〈31〉（`I called the Joint Rescue Coordination Centre (JRCC) Halifax by sat phone but communications with JRCC were shortly thereafter cut-off.`）・TSB §1.3.3（`At 1855, the master of the Polar Prince called the Joint Rescue and Coordination Centre (JRCC) in Halifax`…`JRCC transferred the call to the Rescue Coordination Centre (RCC) in Boston`）
> 船長の陳述では、18時27分にカナダの救難調整センターへ電話したが、すぐ切れた。
> 18時55分の電話から、ボストンの米沿岸警備隊へとつながっていった。

**c506** ／ 図 帯 同じ帯（10:47 から 18:55 までを1本の矢印に・「8時間8分」の札） ／ TSB §2.5（`This was 8 hours and 8 minutes after communication and tracking had been lost`）
> 連絡が途絶えてから、約8時間。カナダの調べでは、8時間8分がたっていた。
> Q: どうして、そんなに待ったの？

**c507** ／ 図 模式 母船の上の2つの組（会社の潜航の班と、船の会社の船長＝取り決めの書類が無い・船長の権限がはっきりしない） ／ TSB §2.5（`the situation with the Titan initially appeared to be a communication and tracking loss, and so the surface support team followed the missed communications protocol.`）・TSB §2.6（`the master’s authority in the loss of communication emergency with the Titan was unclear`）・§2.6（`Without a bridging document`）・§2.6（`missed communications protocol ended up taking precedence even though it did not follow the maritime best practice of notifying SAR authorities as soon as possible once the potential need for help developed`）
> 初めは、通信と追跡が切れただけに見えた。だから会社の手順に従った。
> だがその手順は、できるだけ早く救難の当局に知らせるという、
> 海の上のならいに沿っていなかった、とカナダの調べは書く。

**c508** 🔧 ／ 実写 USCG の記者会見（DVIDS 887718・2023-06-20・A＝副題「6月20日の記者会見（米沿岸警備隊）」） ／ USCG p.40〈32〉（`The United States Coast Guard First District was not aware of the TITAN’s TITANIC Expedition dive operations on this date`）・p.40〈32〉（`entered the distress phase`）
> Q: 外に知らせるより、会社の手順を先にしたんだね。
> そう。知らせを受けた米沿岸警備隊は、この日の潜航を知らなかった。
> すぐに、遭難として扱う段階に入った。

**c509** 🔧 ／ 実写 HC-130J の B-roll（DVIDS 888011・2023-06-21・第106救難航空団・A＝副題「捜索に加わった米軍の輸送機（6月21日）」） ／ NTSB p.19（`At 2200, a US Coast Guard C-130 Hercules`）・p.19（`At 2325, the C-130 arrived on scene and began conducting an overflight air search.`）
> 22時、米沿岸警備隊の輸送機がニューファンドランドから飛び立ち、
> 23時25分、現場の空から探し始めた。

**c510** ／ 実写 DVIDS 7875444 HC-130 の操縦席（2023-06-21・背中だけ・顔は写らない・A＝副題「捜索中の輸送機の操縦席（6月21日）」） ／ TSB §1.3.3（`In total, the SAR response involved 11 vessels and 4 aircraft, which searched approximately 12 000 square nautical miles of ocean.`）
> 捜索には、船11隻と航空機4機が加わった。探した海は約4万1,000平方キロ。
> 関東地方の1都6県を合わせたよりも広い。

**c511** ／ 実写 DVIDS 7875448 機内から見た海と船（2023-06-21・A＝副題「捜索の機内から見た海（6月21日）」） ／ USCG p.40〈32〉（`later to be joined by P-3 aircraft with sonobuoys`）
> 捜索のさなか、海の中で「叩く音」が聞こえたと報じられ、
> 中の人の合図ではないか、と語られた。3つの報告書は、その音に触れていない。

**c512** 🔧 ／ 実写 USCG の記者会見（DVIDS 887852・2023-06-21・器 1280・A＝副題「6月21日の記者会見（米沿岸警備隊）」） ／ USCG p.325〈317〉（`due to the instantaneous implosion occurring prior to the initial distress call`）
> Q: じゃあ、合図じゃなかったの？
> 米沿岸警備隊によると、爆縮は、最初に助けを求める連絡より前に起きていた。
> 音が報じられたころ、5人はもう亡くなっていた。

**c513** 🔧 ／ 実写 USCG の記者会見（DVIDS 887597・2023-06-19・A＝副題「6月19日の記者会見（米沿岸警備隊）」） ／ NTSB p.20（`with two ROVs capable of reaching 9,843 feet (3,000 meters)`）・p.20（`they dove the ROV beyond its rated depth, almost another 3,281 feet (1,000 meters); the ROV was destroyed in the process.`）
> Q: 海の底は、どうやって探すの？
> 遠くから操る無人の探査機、ROV を使う。最初に着いた船の ROV は、
> 限界の3,000メートルより1,000メートル近く深く潜らせて、壊れた。

**c514** ／ 実写 DVIDS 7875471 格納庫の HC-130（A＝副題「捜索に出た米沿岸警備隊の輸送機」） ／ NTSB p.18（`which was capable of reaching 19,685 feet (6,000 meters). (The Odysseus was in Buffalo, New York, at the time.)`）・USCG p.41〈33〉（`emergency transportation of a Pelagic® Odysseus ROV from Buffalo, NY`）・NTSB p.20（`flew the ROV Odysseus on a C-130 to Newfoundland and Labrador, where it was loaded aboard the Horizon Arctic`）
> 6,000メートルまで潜れる ROV が、ニューヨーク州のバッファローにあった。
> アメリカ空軍の輸送機で、ニューファンドランドまで運ばれた。

**c515** 🔧 ／ 図 地図 北大西洋（セントジョンズ・現場・フランスの調査船が向かってきた向き＝矢印だけ） ／ USCG p.42〈34〉（`The French research vessel ATALANTE responded from mid-ocean, carrying the 6,000-meter-capable ROV VICTOR 6000.`）・NTSB p.20（`On June 22, both the Atalante (with the Victor 6000) and the Horizon Arctic (with the Odysseus) were in position over the site.`）
> フランスの調査船も、6,000メートル級の ROV を積んで向かった。
> 6月22日、バッファローの ROV を積んだ船と、フランスの船が、現場にそろった。

**c516** ／ 実写 HC-130J の B-roll（DVIDS 888012・c103 と別の区間・A） ／ USCG p.41〈33〉（`what would typically take two weeks—mobilizing an ROV, modifying a vessel, and assembling a crew—was achieved in days.`）
> 捜索救助の担当者は、ふつうなら2週間かかる支度を、
> 数日でやり遂げた、と証言している。

**c517** ／ 実写 ROV「尾部」（04 の中ほど・c101・c108 と別の区間・第三者＝引用・額装＝副題「6月22日、海の底で見つかった尾部」） ／ USCG p.7〈vii〉（`On June 22, 2023, at approximately 9:40 a.m.`）・TSB §1.3.3（`At approximately 1040, the ROV discovered the Titan’s forward dome and tail piece on the seabed.`）
> 6月22日の午前、海の底で、潜水艇の残骸が見つかった。
> 時刻は、アメリカの2つの調べで9時40分ごろ、カナダの調べでは10時40分ごろだ。

**c518** ／ 図 帯 96時間の帯（6/18 08:24 ドームを閉めた→6/22 08:24＝96時間→05:40 ROV を降ろす〈93時間16分〉→10:40ごろ 発見〈98時間16分〉＝カナダの調べの値） ／ TSB §1.2.1（`enough oxygen to last approximately 96 hours based on an occupancy of 5 people`）・TSB §2.5（`98 hours and 16 minutes after life support had been started on the Titan`）
> 潜水艇の酸素は、5人で約96時間ぶん。見つかったのは、カナダの調べで、
> 生命維持を始めてから98時間16分後。その目安を過ぎていた。
> Q: 見つかったときには、もう過ぎていたんだね。

**c519** ／ 実写 USCG の記者会見「残骸の発見」（DVIDS 888022・c102・c106・c109 と別の区間・A） ／ TSB §2.5（`neither the actual response nor any other response would have changed the outcome given that the Titan’s crew and passengers were fatally injured at the time of the implosion`）
> そう。ただ、カナダの調べは書いている。実際の救助でも、ほかのどんな救助でも、
> 結果は変わらなかった。5人は、爆縮のときに亡くなっていた。

**c520** 🔧 ／ 図 線 タイタンの線画（前のドームを明るく＝外から留めるボルトの位置の札・ハッチなし） ／ TSB §2.5（`Other aspects of the Titan’s design and operations may also have hindered a rescue.`）・§2.5（`the Titan did not have a hatch so its crew and passengers could not egress on the surface without the Titan first being reattached to the LARS`）
> それでも、救助を妨げたかもしれない点がある。タイタンにはハッチが無く、
> 海面に浮いても、台に戻し、外からボルトを外さないと出られなかった。
> Q: 浮いてきても、すぐには出られなかったんだね。

**c521** ／ 図 模式 救助の備え（「水の中の位置を知る手段」「ROV の会社との契約」の2つの欄が空） ／ TSB §2.5（`OceanGate also did not have a means of determining where the Titan was underwater if the tracking and communication systems on the submersible were not functioning.`）・§2.5（`When conducting diving operations, OceanGate also did not have any contracts in place with these ROV operators.`）
> そう。通信と追跡が止まれば、水の中のどこにいるかを知る手段も無かった。
> 会社は、ROV の会社と、救助の契約も結んでいなかった。

**c522** 🔧 ／ 実写 ROV「前のドーム」（07・c104 と別の区間・第三者＝引用・額装） ／ NTSB p.66（`they likely would have had emergency response assets standing by and the Titan likely would have been found sooner`）
> 米運輸安全委員会は、会社が国の指針どおりに救助の備えをしていれば、
> もっと早く見つかった可能性が高い、とみている。

**c523** 🔧 ／ 実写 ROV「後ろのドーム」（07・c105 と別の区間・第三者＝引用・額装）→ 次の章の扉 ／ —
> 最初の問いには、海の底の残骸が答えている。
> 潜水艇の、何が壊れたのか。

---

### 第5章　海の底の残骸（19カット）

**c601** ／ 実写 ROV「前のドーム」（NTSB ドケットの Pelagic video 2 of 2・c104・c522 と別の区間・第三者＝引用・額装・焼き込みは残る＝副題「海の底の残骸（6月22日）」） ／ NTSB p.20（`including the tail cone and both titanium domes`）・NTSB p.38（`ROVs discovered the wreckage about 330 meters (1,083 feet) east-northeast of the Titanic’s bow.`）・NTSB p.39（`Other pressure vessel fragments, likely from the middle or forward portion of the cylinder, were scattered about the ocean floor.`）
> 残骸は、タイタニックの船首から数百メートルの、海の底にあった。
> 尾部と、前と後ろの2つのチタンのドーム。そして、筒の破片が散らばっていた。

**c602** ／ 実写 ROV「後ろのドーム」（07・c105・c523 と別の区間・第三者＝引用・額装） ／ NTSB p.39（`were located together in a comingled mass that included compressed metal, plastic, electronic components, and other materials; the forward dome was located by itself`）
> 後ろのドームと筒の後ろの部分は、つぶれた金属や部品と、一塊になっていた。
> 前のドームは、離れた所に1つだけあった。

**c603** 🔧 ／ 実写 DVIDS 9057342 回収船の甲板で破片を調べる隊員（2023-09-30・白い防護服・米沿岸警備隊の撮影・A・縦長＝額装＝副題「9月の回収（回収船の甲板）」） ／ TSB §1.6（`The U.S. Coast Guard returned to the site in September 2023 and recovered additional debris. Not all of the debris was recovered.`）
> 残骸の一部が引き揚げられ、9月には、もう一度回収が行われた。
> それでも、全部が戻ってきたわけではない。

**c604** 🔧 ／ 実写 FBI 図270 前のドームの窓の押さえの輪（ボルトが切れている所に赤い丸と矢印・USCG 報告 p.294・3枚組で小さい＝額装・A＝副題「前のドームの窓の押さえの輪（FBI 撮影）」） ／ TSB §1.6（`the retaining ring for the viewport was deformed in a manner that indicated the viewport had blown outward. The viewport was not found.`）・USCG p.293〈285〉（`the viewport was ejected outward during the implosion`）
> Q: 窓が割れて、壊れたんじゃないの？
> よく、そう語られる。窓そのものは見つかっていない。だが押さえの輪は外へ曲がり、
> 窓は爆縮のとき、外へ押し出されたとみられている。

**c605** 🔧 ／ 実写 24-011 図47 の下（前のドームの窓の座・NTSB 研究所の撮影・A＝紙面の引用の型＝副題「前のドームの窓の座（研究所）」） ／ TSB §2.1（`the manner in which the retaining ring was deformed suggested that the viewport had not failed`）・USCG p.280〈272〉（`it is unlikely that the acrylic window itself caused the implosion`）・p.280〈272〉（`the most probable failure mode for the acrylic window would have been inward. In such a scenario, fragments of acrylic would likely have been found in the debris.`）
> カナダの調べは、輪の曲がり方から、窓が先に壊れたのではない、とみる。
> 米沿岸警備隊も、窓が原因の見込みは低いとした。窓から壊れたなら、
> 内へ割れて破片が残っていただろう、という証言も引く。

**c606** 🔧 ／ 実写 FBI 図159 前部セグメント（青いシートの上・証拠の札・USCG 報告 p.189・A＝副題「前のチタンの輪（FBI 撮影）」） ／ TSB §2.1（`suggested that the pressure hull’s carbon fibre cylinder was the likeliest point of failure`）・USCG p.269〈261〉（`a loss of structural integrity of the carbon fiber or glue joint within the TITAN’s cylindrical pressure hull`）・NTSB p.61（`The postcasualty condition of the Titan pressure vessel was consistent with a local buckling failure.`）
> Q: じゃあ、どこが壊れたの？
> 3つの調べは、炭素繊維の筒の側を指す。米沿岸警備隊は、
> チタンの輪との継ぎ目も挙げる。壊れ始めた一点までは、決めきれていない。

**c607** ／ 実写 FBI 図157 後部セグメント（チタンの輪・貫通部・炭素繊維の残り・USCG 報告 p.188・2023-07-05・A＝副題「後ろのチタンの輪（FBI 撮影）」） ／ USCG p.292〈284〉（`the adhesive used to bond the hull to the titanium segments had disbonded from the entire forward segment`）
> 筒とチタンの輪をつないでいた接着剤は、前の輪からは、すっかりはがれていた。

**c608** 🔧 ／ 実写 USCG 図268 後部セグメントに残った接着剤（USCG 報告 p.292・A＝副題「後ろの輪に残った接着剤」） ／ USCG p.292〈284〉（`The adhesive was mostly disbonded from the aft segment, except for an approximately 90-degree arc`）・p.293〈285〉（`could be an indicator that the partial separation of the inner layers already existed`）
> 後ろの輪でも、上の一部を除いて、はがれていた。残った接着剤の内側寄りは、
> こすれたような見た目で、内側の層がすでに一部離れていた印かもしれない、
> と米沿岸警備隊は書く。

**c609** ／ 実写 DVIDS 9057369 証拠として並べた炭素繊維の破片（9月の回収のあと・米沿岸警備隊・A・🔴 副題に撮影日を書かない・2022年の札を付けない＝副題「回収された炭素繊維の破片」） ／ NTSB p.40（`had delaminated into multiple layers nearly around the entire circumference`）
> 海の底の映像を見ると、炭素繊維の筒は、ほぼぐるりと一周、
> 何枚もの層に分かれていた。

**c610** 🔧 ／ 図 模式 筒の断面（5枚の層を内側から1〜5・分かれ目＝1と2・3と4のあいだを赤で） ／ NTSB p.40（`One delamination was between layers 1 and 2 and the other was between layers 3 and 4.`）・NTSB p.59（`the five 1-inch-thick layers`）
> 筒は、厚さ約2.5センチの層を5枚、貼り合わせて作られていた。
> Q: 層に分かれるって、どういうこと？
> 貼り合わせた面が離れることで、剥離という。分かれ目は、2か所だった。

**c611** 🔧 ／ 実写 NTSB 図13 回収片の外面と内面（NTSB 研究所・A・🔴「海底に残された円筒部」と書かない＝副題「回収された破片（研究所で撮影）」） ／ NTSB p.41（`which had been recovered about 350 feet (107 meters) from the main wreckage and measured about 61 inches long by 20 inches wide by 1 inch thick`）・p.41（`indicating that the piece originated from layer 1, the innermost co-bonded layer`）
> 米運輸安全委員会の研究所は、回収した破片の1枚を調べた。
> 長さ約1.5メートル。いちばん内側の、1枚目の層の破片だった。

**c612** 🔧 ／ 実写 24-011 図15 接着の面（つや消しの擦れた所・光る所・空隙＝英字の札は §B1-4・研究所・A＝紙面の引用の型） ／ NTSB p.44（`The adhesive regions were rubbed flat and adhesive wear debris was found collecting in the voids.`）
> 破片に残った接着剤の面は、こすれて、平らになっていた。

**c613** 🔧 ／ 実写 24-011 図22 空隙に詰まった削り粉（洗う前と後・研究所・A＝紙面の引用の型・🔴 旧版 c627 の写真〈1つ目の船体の端材〉の差し替え） ／ NTSB p.44（`The rub marks in the adhesive were oriented in the lengthwise direction.`）
> 接着剤の中の小さなすき間、空隙には、こすれて出た粉がたまっていた。
> こすれた跡は、筒の長さの向きにそろっていた。
> Q: 層どうしが、こすれ合っていたんだね。

**c614** 🔧 ／ 実写 24-011 図21 電子顕微鏡で見た縦向きのこすれた跡（研究所・A＝紙面の引用の型） ／ USCG p.289〈281〉（`could only have been created by the longitudinal independent movement of the carbon fiber layers`）
> そう。1枚目と2枚目の層が、別々に長さの向きに動かないと、
> この粉はできない、と米沿岸警備隊は書いている。

**c615** ／ 図 模式 2枚の層が別々にずれてこすれる（矢印・断面の拡大） ／ NTSB p.59（`indicating that the delamination existed before the implosion`）・NTSB p.44（`had likely failed before the casualty`）
> つまり、1枚目と2枚目の層は、爆縮の前から、はがれていたとみられる。
> Q: 壊れる前から、もう離れていたんだね。

**c616** ／ 実写 24-011 図48 4枚目と5枚目の層の大きな破片（外面・内面・研究所・A） ／ NTSB p.59（`The extent of the delamination at the second interface before the implosion could not be determined.`）
> そう。ただ、3枚目と4枚目のあいだが、
> 爆縮の前にどこまで離れていたかは、分かっていない。

**c617** ／ 図 模式 局所座屈（厚い1枚→薄い2枚に分かれる→押されて内へ曲がる） ／ NTSB p.61（`Delaminations are a known cause of local buckling failures. The delamination divides a single thicker composite layer into two thinner layers.`）
> はがれると、厚い1枚の層が、薄い2枚に分かれる。
> 薄い板は、押されると曲がりやすい。押されて形を保てず曲がることを、座屈という。

**c618** 🔧 ／ 実写 NTSB 図14 回収片の端面と中央の破断面（研究所・A＝副題「回収された破片の断面」） ／ NTSB p.61（`likely resulted in a local buckling failure that led to the implosion of the Titan`）
> 米運輸安全委員会は、爆縮の前からの剥離と、そのあと加わった傷が、
> 筒の一部の座屈を起こし、爆縮に至った可能性が高い、とみている。

**c619** 🔧 ／ 図 模式 筒の端の断面（剥離の起きた2つの面に、長い空隙が並ぶ＝c610 の図の拡大） ／ NTSB p.59（`these adhesive interfaces contained long extended voids`）・NTSB p.42（`end pieces that had been trimmed from the v2 full-scale cylinder during the construction/production process`）
> 剥離の起きた2つの面には、作られたときから、長い空隙が並んでいた。
> では、層は、いつ、なぜはがれたのか。話は、炭素繊維の筒が選ばれたころにさかのぼる。

---

### 第6章　炭素繊維の筒（19カット）

**c701** 🔧 ／ 図 線 タイタンの横の線画（NTSB 図3 をなぞる＝筒・チタンの輪・ドームの位置） ／ TSB §1.13（`Carbon fibre is widely used in commercial aviation because of its high strength, low weight, and ability to be moulded.`）
> Q: 炭素繊維って、飛行機にも使われてるよね。
> 広く使われている。強くて軽く、形も作りやすいからだ。

**c702** ／ 図 模式 引っ張りと圧縮（左＝旅客機の胴体・中の空気が外へ押す＝引っ張り／右＝深海の殻・外から押しつぶす＝圧縮。🔴 旧版 c208 の札「強＝圧縮」は逆＝札は米沿岸警備隊の書くとおり） ／ USCG p.274〈266〉（`Carbon fiber has demonstrated its effectiveness in other applications where the material is primarily under tension`）・p.274〈266〉（`a scenario for which carbon fiber has no established track record and is generally understood to be less effective`）
> ただ、炭素繊維が実績を上げてきたのは、旅客機の胴体のように、引っ張られる使い方だ。
> 深い海では、殻は外から押しつぶされる。そこでは確かな実績が無く、
> 一般に弱いと考えられている、と米沿岸警備隊は書く。

**c703** 🔧 ／ 図 模式 ふつうの深海の潜水艇の殻（鋼かチタンの球）とタイタンの殻（炭素繊維の筒）の並べ図 ／ TSB §1.13（`submersibles used for deep-ocean diving are typically constructed of steel or titanium,`…`and the pressure hull for human occupancy is typically spherical in shape`）・TSB 脚注53（`With the exception of the Titan, the TSB is not aware of any other carbon-fibre pressure hulls for human occupancy used for deep-ocean diving.`）
> 深海の潜水艇は、ふつう鋼かチタンで、人の入る殻は球の形だ。
> カナダの調べが知る限り、人が乗る深海用の炭素繊維の殻は、タイタンのほかに無い。

**c704** ／ 図 模式 同じ並べ図（タイタンの側に「軽い」「中が広い」の札） ／ TSB §1.13（`which creates cost savings when it comes to systems for transporting and launching and recovering the submersible.`）・§1.13（`OceanGate’s decision to use carbon fibre in the construction of the Titan was largely based on these factors.`）
> Q: じゃあ、どうして炭素繊維の筒にしたの？
> 軽ければ、運ぶ仕組みも降ろす仕組みも安くすむ。筒の形なら、中も広い。
> カナダの調べは、会社が主にそうした理由で選んだ、とみる。

**c705** ／ 図 再現 元運航部長の証言の一節（NTSB p.25 が引く英字＝`better in compression than tension`・訳は字幕） ／ NTSB p.25（`the CEO chose carbon fiber because he believed it was “better in compression than tension.”`）
> 元運航部長によると、CEO は、炭素繊維は引っ張りより押しつぶしに強い、
> と考えていた。米沿岸警備隊の書く見方とは、逆の向きだ。

**c706** 🔧 ／ 図 再現 2015年の設計書の要点（2015年6月25日・望み6,000m・受け入れ3,000m・安全率の目標2.25） ／ TSB §1.12.1（`On 25 June 2015, this company produced a design document that showed that OceanGate wanted a submersible made primarily of carbon fibre rated up to 6000 m`）・§1.12.1（`OceanGate had a goal of 2.25 for the safety factor, but that it was willing to accept 1.5.`）
> 2015年6月、外部の会社が設計書をまとめた。オーシャンゲートの望みは、
> 炭素繊維の艇で深さ6,000メートル。安全率の目標は2.25だった。

**c707** ／ 図 棒 安全率のしくみ（潜ってよい深さの棒と、壊れる深さの棒・その比＝安全率） ／ NTSB p.24（`Safety factor in submersible design is the ratio between the failure depth and the maximum allowable operational depth.`）
> Q: 安全率って、何？
> 壊れる深さが、潜ってよい深さの何倍あるか、という数だ。
> 1より大きいほど、余裕がある。

**c708** 🔧 ／ 図 棒 設計書の安全率（2.19・2.21 の棒・目標2.25 と下限1.5 の線） ／ TSB §1.12.1（`had a safety factor of 2.19 with grade 5 titanium end domes and a safety factor of 2.21 with carbon fibre end domes.`）・TSB 脚注45（`At the time, OceanGate was basing its safety factor on the American Society for Mechanical Engineers standard`…`that required a minimum safety factor of 1.5.`）
> 設計書の筒の安全率は、2.19と2.21。
> 当時の会社は、アメリカの機械学会の規格の、最低1.5に従っていた。

**c709** 🔧 ／ 図 棒 深さの比べ（約1万3,200m＝壊れる深さの計算・6,000m＝目標・約3,800m＝タイタニック＝縮尺どおり） ／ NTSB p.25（`the analysis indicated an implosion depth about 13,200 meters (43,307 feet)`）
> 外部の会社の強さの計算では、壊れる深さは約1万3,200メートル。
> 壊れるのはタイタニックの3倍あまり深い所、という計算だった。

**c710** 🔧 ／ 図 再現 NTSB p.63 の要点（「完全な形と繊維の向きを仮定した、理論の模型」の英字の一節） ／ NTSB p.63（`were based on theoretical models of composite structures that assumed perfect geometry and fiber orientation`）・p.63（`To rely on the models, OceanGate should have validated them through physical testing`）
> ただ、この計算は、形も繊維の向きも完全だとした、理屈の上の値だった。
> 実物で確かめるべきだった、と米運輸安全委員会は書く。

**c711** ／ 図 模式 3分の1の模型（炭素繊維の筒と炭素繊維のドーム・加圧の矢印） ／ TSB §1.12.1（`In December 2015, OceanGate conducted a pressure test on this one-third scale model at the UW-APL`…`One of the carbon fibre end domes failed at pressures equivalent to depths of around 3000 m.`）
> 2015年12月、3分の1の大きさの模型を加圧すると、
> 炭素繊維のドームの1つが、約3,000メートル相当の圧で壊れた。

**c712** 🔧 ／ 図 再現 CEO の手紙の一節（USCG p.111 が引く英字＋訳は字幕） ／ USCG p.111〈103〉（`Fortunately, there was no damage to the main cylindrical section, which is the critical part and a shape that is far better understood.`）
> CEO は、会社の関係者への手紙に書いた。
> 「肝心の筒には傷が無い。筒の形のほうが、ずっとよく分かっている」。

**c713** 🔧 ／ 図 棒 模型の試験の深さと目標（4,500m の線に届かない・回ごとの値は3冊で割れる＝棒にしない・目標の線と「届かず」の札だけ） ／ USCG p.114〈106〉（`which was less than the 4,500 m (14,764 feet) that was the target max pressure depth for TITAN’s operations.`）・NTSB p.25（`According to the CEO, that model had a delamination in the carbon fiber cylinder.`）
> 模型の試験はそのあとも重ねたが、運航で目指した4,500メートルには届かなかった。
> CEO によれば、模型の筒には、剥離もあった。

**c714** 🔧 ／ 図 模式 船級のしくみ（船の持ち主→民間の団体が設計を見る・工事に立ち会う・試験を確かめる→証明書→定期の検査） ／ NTSB p.22（`Classification societies are nongovernmental organizations that establish and maintain standards for shipbuilding and operations.`）・p.22（`To maintain a valid certificate of classification, a vessel must undergo additional periodic surveys`）
> Q: 船の安全は、外の誰かが確かめないの？
> 船級という仕組みがある。船級協会という民間の団体が、設計や工事を確かめ、
> 試験に立ち会って、証明書を出す。

**c715** 🔧 ／ 図 帯 船級の年表（2016年 船級の相談→2018年 あきらめる→2019年2月 ブログ） ／ NTSB p.22（`the company planned to class the submersible through Lloyd’s Register or DNV.`）・NTSB p.23（`the OceanGate CEO ultimately decided classing the Titan would take too long`…`In 2018, OceanGate abandoned classing efforts.`）
> 会社は初め、船級を取るつもりだった。だが CEO は、時間がかかりすぎると判断し、
> 2018年に、会社はあきらめた。

**c716** ／ 図 再現 会社のブログの題「Why Isn’t Titan Classed?」と一節（英字＋訳は字幕） ／ TSB §1.26.3.1（`On 21 February 2019, OceanGate posted a blog entitled “Why Isn’t Titan Classed?”.`）・NTSB p.24（`by itself, classing is not sufficient to ensure safety.`）
> 2019年、会社はブログに「なぜタイタンは船級を取らないのか」を出した。
> 船級だけでは、安全を保証するのに足りない、という言い分だった。
> Q: 船級を取らないまま、進めたんだね。

**c717** 🔧 ／ 図 再現 NTSB 脚注17 の要点（「新しい技術を確かめる道はある」「旅客や貨物を運ぶ船に『実験的』の区分は無い」） ／ NTSB p.23（`Classification societies have a path for owners to prove seaworthiness of new technology.`）・p.23（`have no “experimental” design endorsement for vessels carrying passengers or cargo.`）
> そう。船級協会には、新しい技術を確かめる道もある。
> 一方で、旅客を運ぶ船に、「実験的」という区分は無い。
> 米運輸安全委員会は、そう書く。

**c718** ／ 図 再現 2021年のテレビの取材の一節（USCG p.301 が引く英字＋訳は字幕） ／ USCG p.301〈293〉（`“I’d like to be remembered as an innovator.`）・p.301〈293〉（`And I've broken some rules to make this.”`）
> 2021年、CEO はアメリカのテレビ局の取材に、こう答えている。
> 「革新者として覚えられたい」。
> 「これを作るのに、いくつか規則を破った」。

**c719** 🔧 ／ 図 再現 社員の懸念の一節（NTSB p.47 が引く英字＋訳は字幕） ／ NTSB p.47（`who had previous experience as an engineer/machinery technician in the US Coast Guard`）・p.47（`the company accepting paying clients as “mission specialists.”`）・p.47（`you can’t just change the title of a person when you’re receiving compensation.”`）・p.47（`The technician resigned following this conversation`）
> 社内にも、声はあった。米沿岸警備隊で技術者だった社員は、
> 料金を取って人を乗せる以上、呼び名を変えるだけでは済まない、と CEO に伝え、
> のちに辞めた。

---

### 第7章　1つ目の船体（19カット）

**c801** ／ 図 模式 筒の作り方（樹脂の槽をくぐった炭素繊維の糸を、回る芯に巻きつける） ／ TSB §1.12.1（`the carbon fibre cylinder was manufactured through a process known as filament winding, which involved winding a continuous strand of carbon fibre on a mandrel.`）・USCG p.152〈144〉（`The assembly of the first TITAN submersible was completed in January 2018.`）
> Q: 最初のタイタンは、どんな船体だったの？
> 炭素繊維の糸を、樹脂にくぐらせながら芯に巻きつけて、筒にした。
> 組み上がったのは、2018年1月だ。

**c802** 🔧 ／ 図 再現 品質点検の報告の要点（2018年1月18日・「切り落とした筒の端に空隙と剥離」の1行を明るく） ／ USCG p.146〈138〉（`on January 18, 2018, submitted a report highlighting critical safety concerns.`）・TSB §1.12.1（`visible voids and delaminations were present in the carbon fibre end segments that had been cut off after the manufacturing process.`）
> そのころ、運航部長が、潜水艇を点検した。
> 2018年1月18日の報告は、作ったあとに切り落とした筒の端に、
> 目に見える空隙と剥離がある、と書いていた。

**c803** 🔧 ／ 実写 NTSB 図18 の左＝1つ目の船体の切り落とした端の剥離（事故のあと NTSB の研究所が調べた・A・🔴 旧版 c307・c627 の副題「回収された破片」は取り違え＝副題「1つ目の船体の切り落とした端（事故のあとに調べた物）」） ／ NTSB p.44（`The v1 pressure vessel cylinder’s trimmed end contained multiple delaminations and voids.`）
> 事故のあと、米運輸安全委員会も、1つ目の船体の切り落とした端を調べた。
> 剥離と空隙が、いくつもあった。

**c804** 🔧 ／ 図 再現 同じ報告の要点（「筒と接着の線を全部点検」「結果は人が乗る潜航の前に」） ／ TSB §1.12.1（`The report noted that a full inspection of the cylinder and the bond lines between the cylinder and the titanium rings was needed to verify their integrity.`）・§1.12.1（`the results of this inspection needed to be provided to the director of operations before any dives were conducted with people on board.`）
> 報告は、筒と、チタンの輪との接着の線を全部点検して確かめ、その結果を、
> 人が乗る潜航の前に示すよう求めた。

**c805** ／ 図 模式 会合の席（CEO・運航部長・社員3人の札と、録音の印） ／ TSB §1.12.1（`The following day, a meeting was held between the CEO, the director of operations, and 3 other OceanGate employees.`）・USCG p.149〈141〉（`argued for additional testing of the TITAN submersible’s hull`）・p.149〈141〉（`was audio recorded by the CEO.`）
> 翌日、CEO と運航部長ら5人の会合が開かれた。運航部長は、
> 船体の追加の試験を求めた。会合は、CEO が録音していた。

**c806** ／ 図 再現 録音の一節（NTSB p.48 が引く英字＋訳は字幕） ／ NTSB p.48（`“it’s clear that there is not a lot of confidence on your part in the engineering that went into this vessel`）
> 録音の中で、CEO は言った。
> 「この船の技術に、あなたはあまり信頼を置いていない」。

**c807** 🔧 ／ 図 帯 2018年の年表（1/18 報告→1/19 会合→1/23 解任） ／ USCG p.149〈141〉（`On January 23, 2018, OceanGate fired the Director of Marine Operations.`）・TSB §1.12.1（`because he held different opinions from the CEO on the safety of the Titan.`）
> 1月23日、会社は運航部長を解任した。
> カナダの調べは、安全について、CEO と考えが違ったため、と書く。
> Q: 辞めさせられた人は、黙っていたの？

**c808** 🔧 ／ 図 帯 同じ年表（2/6 労働安全衛生局へ申し立て） ／ NTSB p.48（`filed a complaint with the Occupational Safety and Health Administration (OSHA) under the Seaman’s Protection Act.`）・p.48（`He told an OSHA investigator that cut-off sections of the carbon fiber cylinder were “like Swiss cheese”`）
> 元運航部長は、安全を訴えたための解任だとして、労働安全衛生局に申し立てた。
> 調査官には、切り落とした筒の断面は「スイスチーズのよう」だった、と話している。

**c809** 🔧 ／ 図 帯 同じ年表（6/25 会社が訴える→12/13 申し立ての取り下げ） ／ USCG p.150〈142〉（`OceanGate filed a lawsuit against him on June 25, 2018`）・p.151〈143〉（`withdrew his SPA complaint against OceanGate`）
> 会社は元運航部長を訴え、元運航部長は、その年のうちに申し立てを取り下げた。
> Q: 安全を心配した人が、会社を追われたんだね。

**c810** ／ 図 再現 業界の委員会の手紙の一節（NTSB p.23 が引く英字＋訳は字幕） ／ NTSB p.23（`expressing “unanimous concern regarding the development of ‘TITAN’ and the planned Titanic Expedition.”`）・p.23（`could result in negative outcomes (from minor to catastrophic)`）
> そう。同じ2018年、業界の委員会の人たちが、CEO 宛ての手紙の案を書いた。
> 会社の「実験的」なやり方は、小さなものから破滅的なものまで、
> 悪い結果を招きかねない、と。

**c811** 🔧 ／ 図 再現 同じ手紙（「船級協会が見て立ち会う試作の試験を」の1行） ／ TSB §1.12.1（`The letter recommended that OceanGate institute a prototype testing program that was reviewed and witnessed by a classification society.`）・§1.12.1（`the MUV committee chair relayed the contents of the letter verbally to OceanGate’s CEO.`）
> 手紙は、船級協会が見て立ち会う、試作の試験を勧めていた。
> その中身は、CEO に伝わっていた。

**c812** ／ 図 地図 バハマ（2018年5月〜2019年4月の試しの潜航の場所） ／ TSB §1.12.1（`During this time, OceanGate conducted 20 dives with people on board, the deepest one being 3939 m.`）
> 2018年5月から、1つ目の船体はバハマで潜航を重ねた。
> 人が乗った潜航は20回。いちばん深くて、3,939メートルだった。

**c813** ／ 図 再現 NTSB 表2（1つ目の船体の潜航の表＝場所ごとの3行・番号の列は「回数」と読ませない） ／ NTSB p.26（`persons aboard the Titan reported hearing cracking sounds.`）
> 2019年、バハマでのいくつかの潜航で、乗っていた人たちは、
> ひび割れるような音を聞いた、と話している。

**c814** 🔧 ／ 実写 DVIDS 9057367 1つ目の船体（エバレットの会社の施設・内側の亀裂を削った跡・2023-08-02 に米沿岸警備隊の委員会が撮影＝MBI 図132 と同じ場面・A・全画面・🔴 DVIDS の撮影日欄「05.29.2019」は亀裂の日＝副題に写さない＝副題「1つ目の船体（2023年8月、委員会が撮影）」） ／ TSB §1.12.1（`a crack was found in the carbon fibre cylinder after a dive.`）・NTSB p.26（`it had originated from a sub-surface delamination (an internal separation within the carbon fiber cylinder).`）
> Q: 音がした船体は、どうなったの？
> 2019年、筒に亀裂が見つかった。調べると、亀裂は、
> 表面の下の剥離から始まっていたとみられた。

**c815** ／ 図 模式 筒の内側の亀裂の位置（前の左舷に3つ＝カナダの調べの値・剥離の札） ／ NTSB p.26（`the first director of engineering stated that he told the CEO that because there was a crack, the pressure vessel hull was “done,”`）・p.26（`The director of engineering stated that he would not sign off on the planned 2019 expedition.`）・USCG p.161〈153〉（`However, the Director of Engineering refused`）
> 初代の技術部長は、亀裂がある以上この船体は終わりだ、と CEO に言った、
> と述べている。その年の遠征も、認めなかった。

**c816** ／ 図 再現 客への手紙の要点（2019年の遠征の中止・亀裂の語が無い） ／ USCG p.162〈154〉（`OceanGate did not make any external notifications`）・NTSB p.26（`The planned 2019 expedition to the Titanic wreck site was cancelled.`）・USCG p.164〈156〉（`The letter, nor any other separate correspondence, disclosed that there was a crack found`）
> 2019年の遠征は中止。米沿岸警備隊の委員会によると、会社は亀裂のことを、
> 客にも当局にも、船級協会にも知らせなかった。

**c817** ／ 図 帯 2019年の年表（7月 技術部長の解任・10月 加圧試験・11月 等級を下げる） ／ USCG p.164〈156〉（`On July 26, 2019, OceanGate fired the Director of Engineering.`）
> その技術部長も、2019年7月に解任された。

**c818** 🔧 ／ 図 帯 同じ年表（10月・11月を明るく） ／ TSB §1.12.1（`Following that test, further cracks and delamination were found in the carbon fibre cylinder.`）・§1.12.1（`from 4000 m to 3000 m with an understanding not to dive below 2000 m.`）・§1.12.1（`This carbon fibre cylinder was not subsequently used for any more dives.`）
> 10月、亀裂のある船体を加圧する試験のあと、亀裂と剥離がさらに見つかった。
> 11月、会社は、この船体で潜るのを2,000メートルまでとした。
> この筒は、それきり潜らなかった。

**c819** ／ 実写 24-011 図39 1つ目と2つ目の筒の切り落とした端の厚さの比べ（定規・青い背景・NTSB 研究所・A＝副題「1つ目（左）と2つ目の筒の端（研究所）」） ／ NTSB p.62（`after the failure of the v1 full-scale pressure vessel, OceanGate used different materials (pre-preg carbon fiber) and manufacturing methods`）
> Q: 最初の船体は、そこで終わったんだね。
> そう。会社は、作り方を変えて、2つ目の筒を作ることにした。

---

### 第8章　2つ目の船体（23カット）

**c901** ／ 実写 NTSB 図18 の右＝1/3 模型の切り落とした端のしわと剥離（NTSB 研究所・A・c803 は同じ図の左＝別の写真＝副題「3分の1の模型の端（研究所）」） ／ TSB §1.12.2（`In early 2020, OceanGate engaged a new company, Electroimpact Inc., to construct a replacement carbon-fibre cylinder.`）・TSB §1.12.2（`The layers were made using a unidirectional carbon fibre tape that was pre-impregnated with epoxy resin`）
> Q: 次の船体は、何を変えたの？
> 2020年の初め、会社は別の会社に、代わりの筒を頼んだ。
> 材料は、樹脂をあらかじめ含ませた、炭素繊維のテープに変えた。

**c902** 🔧 ／ 図 再現 材料の発注の要点（2020年・東レのアメリカの会社・テープの品名は出さない） ／ USCG p.118〈110〉（`The carbon fiber material used for the first TITAN hull was standard-modulus Grafil 37-800`）・p.174〈166〉（`The specific pre-preg system used was Toray Composite Materials America’s P2362W-19L`）・p.174〈166〉（`On February 21, 2020, OceanGate issued a purchase order for 7,700 lbs of P2362W-190U-013 composite material from Toray Composites`）
> 1つ目の筒の糸は三菱ケミカル系、2つ目のテープは東レの米国の会社の物だ。
> 期限切れの炭素繊維を安く買った、とよく語られるが、3つの報告書にその話は無い。

**c903** 🔧 ／ 図 模式 2020年の1/3 模型2つ（1つ目＝壊れた・2つ目＝壊れる寸前で試験を止めた＝米運輸安全委の書き方・深さの数は描かない） ／ NTSB p.62（`either imploded or nearly imploded at depths less than 3,000 meters (9,843 feet), significantly less than the depth needed to reach the Titanic wreckage.`）
> Q: 模型の試験は、うまくいったの？
> この材料の3分の1の模型2つは、2020年の試験で、壊れたか、壊れる寸前だった。
> どちらも、タイタニックの深さの、ずっと手前だ。

**c904** 🔧 ／ 図 模式 層のうねり（まっすぐな繊維と、波打った繊維の並べ図） ／ TSB §1.12.2（`identified that ply waviness in localized areas in the carbon fibre cylinder was the cause of each failure.`）・§1.12.2（`Ply waviness reduces the compressive strength and buckling resistance of a laminate composite.`）
> オーシャンゲートと解析の会社は、原因を、層の一部にできた、波のようなうねりと見た。
> うねりがあると、押しつぶす力に弱くなる。

**c905** ／ 図 模式 1層ずつ固める作り方（巻く→固める→接着剤の膜→次の層・5回くり返す） ／ TSB §1.12.2（`The manufacturing process therefore involved Electroimpact Inc. creating the cylinder in 5 layers, each of which was cured separately.`）・TSB 脚注50（`A multi-cure method allows for the layers of carbon fibre to be thinner, which reduces the probability of ply waviness.`）
> そこで実物の筒は、5つの層に分け、1層ずつ固めて重ねる作り方にした。
> 1層を薄くすると、うねりができにくい。

**c906** ／ 実写 MBI 図255 5層の断面（英字の札と定規・NTSB の撮影・USCG 報告 p.276・A・英字の札は §B1-4＝映像方針で＝副題「事故の船体の筒の断面（5つの層）」） ／ TSB §1.12.2（`Each layer contained 133 fibre plies.`）・§1.12.2（`The laminate stacking sequence was 2 cylindrical plies first, followed by 1 longitudinal ply.`）
> 1つの層は、薄い炭素繊維の膜を133枚重ねたもの。
> 筒の周りの向きに2枚、長さの向きに1枚を、くり返した。

**c907** 🔧 ／ 図 模式 同じ作り方の図（「作り手が強く求めた」「費用は作り手が持った」の札） ／ TSB §1.12.2（`OceanGate initially rejected this recommendation because it would cost more, but Electroimpact Inc. insisted on it and agreed to cover the cost of it.`）
> カナダの調べでは、この作り方は、作り手の会社が強く求めた。
> 会社は費用を理由に一度断り、作り手が費用を持つことで決まった。

**c908** ／ 図 帯 年表（2020年11月〜2021年1月 実物大の筒・模型は作らず） ／ NTSB p.28（`between November 2020 and January 2021.`）・NTSB p.62（`OceanGate did not build or test any new sub-scale models using the co-bonding process`）・p.62（`the only article produced using the co-bonding process was the v2 full-scale cylinder ultimately used in the casualty dive.`）
> 筒は、2020年11月から2021年1月にかけて作られた。
> この作り方で、模型は1つも作らず、試してもいない。
> Q: 試さないまま、本物を作ったんだね。

**c909** ／ 実写 NTSB 図16 の下＝事故の船体の端材のしわの削り跡（研究所・A＝副題「しわを削った跡（事故の船体の端材）」） ／ TSB §1.12.2（`The carbon fibre plies in these areas were ground down by OceanGate to make them flush with the rest of the outer surface before the next layer was added.`）・§1.12.2（`Grinding down the carbon fibre severed some of the fibres and introduced defects on the surface.`）・§1.12.2（`Grinding did not mitigate ply waviness below the outer surface of each layer of the cylinder.`）
> そう。しかも、層を重ねる途中で、うねりで盛り上がった所を、削って平らにしていた。
> 削ると繊維が切れ、表面に傷が入る。その下のうねりは、直らない。

**c910** 🔧 ／ 図 棒 MBI 図143 の数（層ごとの「削ったしわ」の数＝⑤b で原寸から読む・文字の層に無い） ／ TSB §2.1（`The overall extent of the grinding was not documented and therefore could not be determined.`）
> Q: それは、心配になるね。
> どこまで削ったのか、記録されていない。

**c911** 🔧 ／ 実写 NTSB 図15 事故の船体の端材の側面（研究所・A＝副題「事故の船体の筒の切り落とした端（研究所）」） ／ NTSB p.29（`The cylinder was manufactured with excess material at both ends, which was subsequently trimmed off.`）・NTSB p.42（`We also examined end pieces that had been trimmed from the v2 full-scale cylinder during the construction/production process`）
> 事故のあと、米運輸安全委員会は、筒の両端の余りを切り落とした端材を調べた。

**c912** ／ 図 模式 筒の厚さ（設計＝約12.7cm〈5インチ〉の溝・端材＝約13.1cm・外側を削って溝に入れた） ／ NTSB p.43（`The excess porosity resulted in an increase in layer thickness.`）・p.43（`which could only accommodate a 5-inch-thick cylinder.`）
> 端材の層は、細かい泡の穴のせいで、思っていたより厚かった。
> チタンの輪の溝に入らないので、筒の外側を削って入れていた。

**c913** 🔧 ／ 実写 NTSB 図17 の下＝1枚目と2枚目の層のあいだの接着剤の空隙（研究所・A＝副題「層のあいだの接着剤のすき間（事故の船体の端材）」） ／ NTSB p.43（`The voids were present in all layers but were significantly greater in size and number at the interface between the first and second layers and the third and fourth layers.`）
> 層と層をつなぐ接着剤には、空隙があった。特に大きく多かったのは、
> 1枚目と2枚目の層、3枚目と4枚目の層のあいだ。残骸の映像で、はがれていた面だ。
> Q: はがれた面と、同じ所なんだね。

**c914** 🔧 ／ 実写 NTSB 図16 の上＝しわのまわりで接着剤がテントのように浮いた空隙（研究所・A＝副題「しわのまわりのすき間（事故の船体の端材）」） ／ NTSB p.62（`the co-bonding process did not completely eliminate the wrinkles and, at the same time, introduced additional anomalies.`）
> そう。米運輸安全委員会は、この作り方は、しわやうねりを無くしきれず、
> ほかの異常も持ち込んだ、とみている。

**c915** 🔧 ／ 図 再現 TSB の研究所の試験の要点（端材を18の試料に・長さの向き9・周りの向き9） ／ TSB §1.14（`The TSB Laboratory was able to obtain a trimmed-off end piece that came from the 2nd construction of Titan’s carbon fibre cylinder`）・TSB §1.15（`The TSB Laboratory cut and machined the end piece into 18 samples, 9 in the axial direction and 9 in the circumferential direction.`）
> カナダの研究所も、2つ目の筒の端材を、18の試料に切って試験した。

**c916** 🔧 ／ 実写 24-011 図28 2つ目の筒の切り落とした端面のうねり（黄の目盛り・NTSB 研究所・A＝副題「端面に見える層のうねり（米運輸安全委員会の研究所）」） ／ TSB §1.15（`there was a general waviness in the plies.`）
> 周りの向きの層には、全体に、うねりがあった。

**c917** 🔧 ／ 図 棒 安全率（長さの向き3.05・周りの向き1.11・必要な1.25 の線＝何メートルでの値かは書かない） ／ TSB §1.12.2（`OceanGate also changed its safety factor to 1.25`）・§1.15（`as evidenced by the calculated safety factor of 3.05, which was greater than the required 1.25.`）・§1.15（`the calculated safety factor was 1.11, which did not meet the required safety factor of 1.25.`）
> 2020年、会社は安全率の基準を、国際規格に合わせて1.25にしていた。
> 試料から計算した安全率は、長さの向きで3.05。十分に上回った。
> ところが周りの向きは、1.11。1.25に、届いていなかった。

**c918** 🔧 ／ 図 模式 棚のたとえ（いつも100キロを載せる棚＝基準は125キロまで耐える／この筒の周りの向き＝111キロまで・式は §9） ／ —
> Q: それって、どのくらい足りないの？
> いつも100キロを載せる棚なら、125キロまで耐えるように作る、という基準だ。
> この筒の周りの向きは、111キロまで。余裕は、求める分の半分も無い計算だ。

**c919** 🔧 ／ 図 再現 TSB §1.15 の一節（前提の「試料が実物を代表するなら」と、結論の文を英字で＋訳は字幕） ／ TSB §1.15（`Assuming that the test results from the samples are representative of the properties of the carbon fibre cylinder used in the Titan`）・§1.15（`it was unsafe for the Titan to have been repeatedly exposed to pressures equivalent to the depth of the Titanic or deeper (which occurred during pressure tests).`）
> カナダの調べは書く。試料が実物の筒を代表するなら、タイタニックの深さか、
> それより深い圧力に、加圧試験も含めてくり返しさらされるのは、安全ではなかった。

**c920** 🔧 ／ 図 棒 疲れの寿命（米運輸安全委が試した試料でカナダの研究所が計算、いちばん強い物＝耐えた見込み／いちばん弱い物＝82% を超えて使った可能性） ／ TSB §1.16（`would reasonably have been expected to survive based on the sample with the highest compressive strength value`）・§1.16（`it could have used more than 82% of its fatigue life in the time up to the occurrence dive based on the sample with the lowest compressive strength value.`）
> カナダの研究所は、米運輸安全委員会が試した試料でも計算した。
> いちばん強い物なら耐えた見込み。いちばん弱い物なら、事故の潜航までに、
> くり返しで壊れるまでの寿命の、82%を超えて使っていた可能性がある。

**c921** 🔧 ／ 図 帯 2021年2〜3月の加圧試験4回（4,000m 前後・4,200m は1回・20分＝米沿岸警備隊の書き方・タイタニックの約3,840m の線） ／ TSB §1.12.2（`In February and March 2021, the pressure hull was tested at the Deep Ocean Test Facility. Four tests were done.`）・TSB §1.15（`the Titan had 4 successful pressure tests at the Deep Ocean Test Facility`）・NTSB p.58（`marginally greater than the 3,840-meter (12,598-foot) dive depth required to reach the Titanic.`）
> 2021年2月から3月、船体は、4,000メートル前後の加圧を4回受け、
> 試験を通った。いちばん深い4,200メートルでも、
> タイタニックの深さを、少し上回るだけだ。

**c922** 🔧 ／ 図 再現 TSB §1.12.2・§2.1 の要点（「疲れの計算の代わりに音の監視」「耐えられる回数は分からない」） ／ TSB §1.12.2（`the acoustic emission monitoring system would be used to detect damage in real time`）・TSB §2.1（`The number of cycles at extreme pressure that the full-scale pressure hull could withstand was therefore unknown.`）
> Q: 試験には、通ったんだね。
> そう。ただ、何回くり返せば壊れるかは、分からないままだった。
> くり返しの計算を聞かれた会社は、傷は音の監視でその場で分かる、と答えていた。

**c923** 🔧 ／ 図 模式 前のドームの窓（内側が平ら・外側がふくらんだ形・等級の札＝約650m〈米沿岸警備隊・カナダ〉／1,000m の認証〈米運輸安全委〉） ／ USCG p.278〈270〉（`certified the window to a pressure rating of 945 psi, corresponding to a depth of only 650 m (2,133 feet).`）・NTSB p.30（`an acrylic window certified to 1,000 meters (3,281 feet).`）・TSB §1.12.1（`only a fraction of what OceanGate required for dives to the Titanic`）・§1.12.2（`The new viewport from Germany was installed in this construction`）
> 前のドームの窓も心配された。最初の窓が認められた深さは約650メートルで、
> タイタニックに遠く及ばない。米運輸安全委員会は1,000メートルと書く。
> 事故のときの窓が何だったかは、調べによって見方が分かれる。

---

### 第9章　2022年7月15日の音（26カット）

**ca01** 🔧 ／ 図 再現 TSB 付録B の表の2022年の13行（深さ「3840」の7行を明るく・欄は英字のまま） ／ NTSB p.35（`the Titan reached 3,840 meters (12,598 feet) seven times`）・USCG p.235〈227〉（`While 7 of the 13 dives reached the TITANIC depth of 3840 m`）・TSB 脚注75（`Dives without people on board are not included.`）
> Q: 次の年の夏には、何があったの？
> 人が乗った潜航は13回。うち7回が、タイタニックの深さまで届いた。

**ca02** 🔧 ／ 図 再現 同じ表（2022-07-03 の行の備考 `Titan collided with the port bow of the Titanic and was disabled on recovery` を明るく） ／ TSB 付録B（`Titan collided with the port bow of the Titanic and was disabled on recovery`）・TSB §2.1.3（`The investigation could not conclusively quantify the extent of damage, if any, from these other sources`）
> カナダの調べによると、7月3日、潜水艇はタイタニックの船首の左側にぶつかり、
> 回収のときに動けなくなった。
> Q: タイタニックに、ぶつかっていたんだ。

**ca03** 🔧 ／ 実写 NTSB 図8 2022年、母船の船尾から台ごと海へ降ろされるタイタン（MIR p.34・撮影は個人＝第三者＝額装・改変なし・サムネに使わない・旧版 c109 のように地に敷かない＝副題「台ごと海へ降ろされるタイタン（2022年）」） ／ TSB §2.1.3（`such as the Titan colliding with the port bow of the Titanic on 03 July 2022`）・USCG p.233〈225〉（`the TITAN became entangled in the TITANIC’s stairwell.`）
> そう。傷んだかは分からないが、カナダの調べは、これも傷みの出どころの候補に挙げる。
> そして7月15日、米沿岸警備隊によると、潜水艇はタイタニックの中をのぞこうと降り、
> その階段に、引っかかった。

**ca04** 🔧 ／ 図 再現 USCG p.233 の要点（「少しのあいだ動けず」「事故の報告は出されなかった」） ／ USCG p.233〈225〉（`For a moment, the TITAN remained trapped, but the content expert was subsequently able to work the controls to free the TITAN from the TITANIC wreckage.`）・USCG p.311〈303〉（`no incident report was filed for this event.`）
> 少しのあいだ動けなかったが、操縦していたタイタニックの専門家が外した。
> 事故としての報告は、出されなかった。

**ca05** ／ 図 線 80回目の深さの線（記録の点だけ＝10:05〜13:35 に 3,840m 付近・15:20ごろ 0m＝NTSB 図19 を記録の点で描き直す・元は OceanGate のデータ） ／ USCG p.234〈226〉（`which occurred as the TITAN was still submerged but nearing the surface.`）・NTSB p.36（`heard a “loud bang” as the Titan ascended`）・TSB §1.10.10.1（`a loud bang was heard by crew and passengers of the submersible while it was surfacing.`）
> その帰り、浮上の終わりの海面の近くで、大きな音がした。
> 中にいた人たちと、海面の小舟の人たちが聞いている。

**ca06** 🔧 ／ 図 模式 監視装置の配置（筒の内側に音のセンサー8つ・ひずみ計16の印） ／ NTSB p.31（`The system was comprised of eight acoustic emission sensors, eight circumferential (hoop) strain gages, and eight longitudinal (axial) strain gages.`）
> Q: 音の監視の装置って、どんな物？
> 船体の中の音を拾うセンサーが8つと、ひずみを測る計器が16。
> ひずみとは、押されて、ほんの少し縮んだり伸びたりすることだ。

**ca07** 🔧 ／ 図 線 音とひずみの線（記録の点だけ＝15:17ごろから音が増える・15:26:45 に大きな山・同じ瞬間にひずみが跳ぶ＝USCG の値・NTSB 図19・20 と USCG 図215・216 を描き直す・左下に「元は会社の記録」） ／ USCG p.283〈275〉（`At 3:26:45 p.m., the TITAN’s RTM system recorded a major acoustic emission event`）・USCG p.286〈278〉（`occurred in a fraction of a second and coincided with the large amplitude acoustic event on Dive 80 at 3:26:45 p.m.`）
> 米沿岸警備隊の分析では、15時26分45秒、装置は大きな音の山をとらえた。
> 同じ瞬間、ひずみの値も、一瞬で跳んでいた。

**ca08** 🔧 ／ 図 線 同じ図（15:17ごろからの音の増えを明るく・NTSB の幅 15:15〜15:30 の帯） ／ USCG p.283〈275〉（`revealed increased acoustic emission activity beginning at approximately 3:17 p.m.`）・NTSB p.52（`showed a burst of acoustic activity and a sudden jump in some of the strain gages between about 1515 and 1530`）
> 音は、15時17分ごろから増え始めていた。米運輸安全委員会は、
> 15時15分から15時30分ごろのあいだ、と幅で書く。

**ca09** 🔧 ／ 図 再現 会社の説明（NTSB p.36 の英字＝`the hull had shifted in its metal cradle`＋訳は字幕） ／ USCG p.233〈225〉（`was caused by a shift in the TITAN’s position within its frame.`）・NTSB p.36（`staff and mission specialists were told the hull had shifted in its metal cradle.`）
> 会社は、潜水艇が枠の中でずれた音だ、と結論した。
> 社員と客にも、そう伝えられた。

**ca10** ／ 図 模式 筒と内張り（外から見るだけ＝層のあいだのはがれは外から見えない） ／ USCG p.289〈281〉（`a cursory external examination of the TITAN was conducted following the loud bang with no visible damage identified.`）・USCG p.290〈282〉（`no effort was made to remove the TITAN’s insert or take the submersible temporarily out of service for a more detailed assessment.`）
> Q: 音のあと、船体は調べたの？
> 外から見ただけだ。中の内張りは外さず、
> 潜水艇を休ませて詳しく調べることもしなかった。

**ca11** 🔧 ／ 図 再現 CEO の言葉（NTSB p.36 が引く英字＋訳は字幕） ／ NTSB p.36（`after inspecting the strain and acoustic emission data, told the director of engineering, "Let's dive again and see what happens"`）
> 米運輸安全委員会によると、CEO はデータを見たうえで、
> 当時の技術部長に言った。「もう一度潜って、どうなるか見よう」。

**ca12** ／ 図 再現 USCG p.290 の要点（「次の潜航の前にも、冬の休みのあいだにも、調べは要らないと指示」） ／ USCG p.290〈282〉（`directed that no further investigation or assessments were necessary ahead of the next scheduled 2022 dive or during the TITAN’s extended layup period ahead of the 2023 TITANIC Expedition.`）
> 米沿岸警備隊によると、CEO は、次の潜航の前にも、冬の休みのあいだにも、
> それ以上の調べは要らない、と指示した。

**ca13** 🔧 ／ 図 再現 USCG p.290 の要点（「権限のある誰も、ひずみのデータを読み解く専門の力を持たなかった」） ／ USCG p.290〈282〉（`neither the Director of Engineering nor anyone else onboard with the authority to assess the submersible’s safety possessed the necessary engineering expertise to interpret the strain gauge data`）
> 技術部長も、その場で安全を判断する立場の誰も、
> ひずみのデータを読み解く専門の力を持っていなかった、と米沿岸警備隊は書く。
> Q: その場には、データを読める人がいなかったんだね。

**ca14** 🔧 ／ 図 帯 2022年7月の年表（15日 80回目→19日 81回目→22日 82回目→23日 83回目） ／ NTSB p.36（`the submersible reached 3,840 meters (12,598 feet) on dives 81 and 82 and 2,954 meters (9,692 feet) on the final dive of the expedition.`）・NTSB p.51（`The last of these dives (dive 83) took place on July 23, 2022, but at a different dive location`）・TSB §2.1.1（`4 days before the subsequent dive on 19 July 2022`）
> そう。4日後の7月19日と、22日の潜航は、どちらもタイタニックの深さまで。
> 23日の、その夏最後の潜航は、別の場所で深さ2,954メートルだった。

**ca15** 🔧 ／ 図 再現 付録B の 2022-07-19 の行（備考 `Thruster control mapping failure, electrical problems`） ／ USCG p.235〈227〉（`The pilot overcame the malfunctioning thrusters by turning the controller around and operating the controls in reverse.`）・USCG p.311〈303〉（`the dive proceeded after the pilot compensated for the failures instead of ascending for repairs in a controlled environment.`）
> 19日は推進器の操作が逆になり、操縦士はコントローラーを逆さに持って続けた。

**ca16** 🔧 ／ 図 線 時刻に沿って並べたひずみ（潜航ごとの線が横に並ぶ＝比べにくい形の模式） ／ NTSB p.51（`OceanGate analyzed hull strain by plotting it side-by-side with dive depth as a function of time.`）・NTSB p.64（`analyzing strain data in this way was flawed because it was difficult for OceanGate to compare data between dives.`）
> 会社は、ひずみを時刻に沿って並べて見ていた。
> 米運輸安全委員会によると、これでは潜航どうしを比べにくい。

**ca17** 🔧 ／ 図 NTSB 図21 の左（75回目と80回目の浅い1,000m のひずみ＝出どころの注なし＝NTSB・A・額装か記録の点で描き直す） ／ NTSB p.53（`Through dive 80, the strain response of the hull was linear at all depths (a typical mechanical behavior).`）
> 事故のあと、同じデータを深さに沿って並べ直すと、あの音の潜航までは、
> どの深さでも線はまっすぐだった。材料としてふつうの形だ。

**ca18** ／ 図 NTSB 図21 の右（81〜83回目の浅い所の「Non-linear behavior」を明るく） ／ NTSB p.53（`During dive 81, the first dive after the audible event, the strain response at low depth was non-linear.`）・NTSB p.59 脚注42（`The strain response at greater depths remained linear, similar to previous dives`）
> ところが、音のあとの潜航から、浅い所で線が曲がっていた。
> その次も、その次も。深い所は、まっすぐのままだった。

**ca19** 🔧 ／ 図 模式 層がはがれた筒（浅い所で線が曲がるしくみ・ひずみ計の位置＝筒の前の端） ／ NTSB p.59（`This change in strain response is more consistent with a delamination between layers.`）・p.59（`indicating that the damage extended to the forward end of the cylinder.`）
> Q: 浅い所だけ曲がるって、どういうこと？
> 層のはがれとよく合う、と米運輸安全委員会は書く。はがれた層は浅い所で別々に動き、
> 深い所ではまとまって動く。計器は筒の前の端にあり、傷みはそこまで届いていた。

**ca20** 🔧 ／ 図 棒 浅い所（10〜300m）のひずみの傾き（2021-08-05＝全体より21%大きい／2022-07-19＝98%大きい＝カナダの調べの値） ／ TSB §1.10.10.1（`the strain slope was found to be 98% greater than the slope for the entire dive profile.`）
> カナダの調べも、浅い所のひずみの傾きを計算している。
> 2021年8月5日の潜航は全体より21%、2022年7月19日は98%大きかった。

**ca21** ／ 図 帯 3つの見方の並べ（米沿岸警備隊＝強く示す／米運輸安全委＝可能性が高い／カナダ＝決められない） ／ USCG p.289〈281〉（`strongly suggests that the carbon fiber hull sustained irreversible damage at the end of Dive 80.`）・USCG p.289〈281〉（`It is likely that the loud bang heard on the surface during Dive 80 was the result of a sudden delamination occurring between layers 1 and 2`）・NTSB p.59（`the NTSB concludes that the Titan pressure vessel likely sustained damage after it surfaced at the end of dive 80`）
> アメリカの2つの調べは、あの潜航の終わりに、船体が層のはがれという形で、
> 傷んだ可能性が高い、とみる。

**ca22** 🔧 ／ 図 帯 同じ並べ（カナダの段を明るく） ／ TSB §1.10.10.1（`so it cannot be determined whether this event precipitated the non-linear readings on 19 July 2022.`）
> カナダの調べは、会社が音のあと船体をきちんと調べなかったので、
> あの音が線の曲がりのきっかけかは、決められない、とした。
> Q: 会社が調べなかったから、決められないんだね。

**ca23** ／ 図 再現 監視装置の決まり（30で黄・50で赤・警報の音なし・潜航ごとにゼロ） ／ NTSB p.31（`if the system detected 30 hits during a dive, the system issued a yellow display warning.`）・TSB §1.10.9（`The system did not have audible alarms.`）・NTSB p.31（`Hit counts did not accumulate between successive dives, and hits while at the surface were not counted.`）
> そう。監視装置にも、限りがあった。音の数が30で画面が黄色、50で赤とされ、
> 警報の音は無く、数は潜航ごとにゼロに戻った。

**ca24** ／ 図 再現 センサー8つのうち3つ（1・3・5番）が2022年の潜航で一度も音を拾わず ／ NTSB p.51（`Three of the eight acoustic sensors (channels 1, 3, and 5) did not register acoustic events for any of the 2022 dives.`）・USCG p.282〈274〉（`OceanGate operated TITAN with three out of eight sensors (37.5%) inoperable was reckless`）
> しかも、音のセンサー8つのうち3つは、
> 2022年の潜航で、一度も音を拾っていなかった。
> 米沿岸警備隊は、そのまま運航したのは無謀だった、と書く。

**ca25** 🔧 ／ 図 再現 警告の基準の出どころ（1つ目の船体と模型の音＝作り方の違う船体） ／ NTSB p.31（`The warning levels were based on the acoustic activity of the v1 pressure vessel`）・NTSB p.64（`the v1 full-scale pressure vessel and sub-scale models were manufactured using a different method`）・NTSB p.65（`never produced the type of acoustic emission signal that would have triggered an alert and thus did not detect the initial damage.`）
> 米運輸安全委員会によると、警告の基準は、作り方の違う1つ目の船体と、
> 模型の音で決めた。音のあとの潜航でも警告の形にならず、最初の傷みに気づけなかった。
> Q: 装置があっても、見逃していたんだね。

**ca26** 🔧 ／ 図 帯 2022年7月から2023年6月までの帯（タイタニックの深さへの最後の潜航〈7月22日〉→事故まで約11か月） ／ USCG p.290〈282〉（`should have been a red flag to stop all dive operations.`）・NTSB p.60（`Therefore, the pressure vessel must have sustained additional damage after dive 82 and before the casualty dive 11 months later (dive 88).`）
> そう。米沿岸警備隊は、あの音とひずみの記録は、
> すべての潜航を止める赤信号だったはずだ、と書く。
> そして船体は、次の夏まで、11か月を過ごすことになる。

---

### 第10章　最後の冬と2023年（19カット）

**cb01** ／ 実写 NTSB 図9 港の基地の屋外の駐車場に置かれたタイタンと台（MIR p.36 の図・撮影は基地の会社＝第三者＝額装・改変なし・サムネに使わない＝副題「屋外に置かれたタイタン（2022年の秋から冬）」） ／ TSB §1.22（`OceanGate opted to keep the Titan and the LARS in St. John’s because OceanGate did not have enough money to transport them back to Everett.`）・NTSB p.36（`It was left in a parking lot, outside, uncovered (see figure 9).`）
> Q: 冬のあいだ、潜水艇はどこにあったの？
> セントジョンズの港の基地の、屋外の駐車場だ。カナダの調べによると、
> 本社へ運び戻すお金が無かった。

**cb02** 🔧 ／ 図 再現 覆いの見積もり（基地からのメール・会社の返事なし） ／ USCG p.237〈229〉（`they had not received approval to proceed, so the tarp was not purchased.`）・NTSB p.35（`OceanGate shipped the Titan and LARS to Everett, where they were stowed indoors at an OceanGate facility during the winter season.`）
> 覆いをかける見積もりは届いたが、会社は返事をせず、覆いは買われなかった。
> 前の冬は、アメリカへ運び戻していた。この冬は、覆いも無いまま外にあった。

**cb03** ／ 図 帯 屋外の期間（2022年7月26日〜2023年2月6日＝195日） ／ USCG p.236〈228〉（`On July 26, 2022, the TITAN, the LARS, and associated equipment were demobilized at the A Harvey Marine Base in St. John’s, Canada.`）・USCG p.238〈230〉（`unprotected from the elements until February 6, 2023.`）
> 外にあったのは、2022年7月26日から、2023年2月6日まで。半年あまりだ。

**cb04** 🔧 ／ 図 棒 セントジョンズの冬の気温（2022年12月〜2023年2月の最高気温の平均 −0.5℃・最低気温の平均 −5.5℃＝カナダの調べの値） ／ TSB §1.22（`The average high temperature in St. John’s between December 2022 and February 2023 was -0.5° and the average low was -5.5°.`）・§1.22（`experiences snow, strong winds, freezing rain, and hail.`）
> この冬、12月から2月のセントジョンズは、最高気温の平均でもマイナス0.5度。
> 雪や強い風、凍る雨もある。

**cb05** 🔧 ／ 図 模式 水が入って凍る（船体のすき間の水が氷になってふくらむ・溶けて縮む・くり返す） ／ NTSB p.60（`If water had penetrated any part of the pressure vessel and frozen, the expansion that occurs due to the phase change to ice could have caused additional damage.`）・TSB §2.1.3（`The investigation could not conclusively quantify the extent of damage, if any, from these other sources`）
> 船体に水が入って凍れば、ふくらんで、さらに傷めた可能性がある。
> 米運輸安全委員会もカナダの調べも、外での傷みは「あり得る」までだ。

**cb06** ／ 図 再現 米沿岸警備隊の主たる要因の8つ目（英字＋訳は字幕） ／ USCG p.328〈320〉（`compromised the TITAN’s hull integrity.`）・USCG p.7〈vii〉（`OceanGate’s failure to conduct preventative maintenance on the TITAN’s hull or protect it from the elements during the extended offseason layup period`）
> 米沿岸警備隊は、結論で、屋外に置いたことが船体を損ねた、とまで書き、
> 事故の主たる要因の1つに挙げている。

**cb07** 🔧 ／ 実写 MBI 図109 岸壁の台（LARS）と白い浮き（USCG 報告 p.142・2023-06-25 撮影・c305 の図5 と同じ場面の別の写真・A＝副題「潜水艇を載せる台（事故の後に撮影）」） ／ USCG p.238〈230〉（`what we really wanted to do was bring the sub back, at least, to Everett and pull the insert and look at`）
> 技術の人たちは、本社へ戻して内張りを外し、船体の内側を見たかった。
> だが、できなかった、と当時の技術部長は証言している。

**cb08** 🔧 ／ 図 再現 2023年の計画書の人の欄（技術部長＝「TBD」） ／ USCG p.246〈238〉（`OceanGate’s Director of Engineering position for the expedition was listed as To Be Determined (TBD).`）・TSB §1.23.1（`there was no one formally in the position of director of engineering for the remainder of the 2023 season.`）
> Q: そのあと、誰が船体を見ていたの？
> 2023年の遠征の計画書では、技術部長の欄は「未定」。
> 技術の責任者の席は、正式には空いたままだった。

**cb09** 🔧 ／ 図 地図 セントジョンズから現場まで（母船の後ろに台ごと引く線） ／ TSB §1.20.2（`because the Polar Prince did not have equipment to lift the Titan and the LARS on and off the deck.`）・USCG p.246〈238〉（`the LARS and TITAN had to be towed behind the POLAR PRINCE for the entirety of each 2023 TITANIC mission.`）
> 2023年の母船には、潜水艇を甲板に上げる設備が無く、潜水艇は台に載せたまま、
> 後ろに引いて運ばれた。

**cb10** 🔧 ／ 図 棒 引かれていた時間（約950時間＝カナダの調べ）と道のり（2,900海里あまり＝約5,400km＝米沿岸警備隊） ／ TSB §1.20.2.2（`towed by or tethered to, via a towline, the Polar Prince in the North Atlantic for approximately 950 hours in the 2023 season.`）・USCG p.294〈286〉（`towed behind the POLAR PRINCE for a total distance of more than 2,900 NM.`）
> その年、母船の綱につながれていた時間は、合わせて約950時間。

**cb11** 🔧 ／ 実写 MBI 図112 台の注水弁（黄の丸＝MBI・USCG 報告 p.144・A＝副題「台の注水弁（事故の後に撮影）」） ／ TSB §1.20.2.2（`were subjected to considerably higher accelerations than those recommended by DNV`）・§1.20.2.2（`The Titan was also towed through significant wave heights of up to 3.35 m on the LARS`）
> 引かれているあいだ、潜水艇は、業界の目安よりかなり大きな揺れを受け、
> 波の高さの目安は、最大3.35メートルあった。

**cb12** 🔧 ／ 実写 NTSB 図10 傾いた台（撮影は個人＝第三者＝額装・改変なし・④' と映像方針で使うか確かめる＝副題「傾いた台（2023年5月20日と27日）」＝NTSB 図10 の凡例の日付・5月24日に半ば沈んだ場面ではない＝語りの5月24日と並べない（引かれて揺れた cb11 へ移す案）） ／ TSB §1.21.1（`On the morning of 24 May, while en route to the wreck site, the LARS and the Titan partially submerged while under tow.`）・§1.21.1（`The Titan and the LARS partially submerged again on the return to St. John’s.`）
> 5月24日、現場へ向かう途中で、引かれていた台と潜水艇が、半ば沈んだ。
> カナダの調べでは、港へ戻る途中でも、半ば沈んでいる。
> Q: 運んでいるだけで、沈みかけたんだね。

**cb13** 🔧 ／ 図 帯 3つの見方（引かれたことの影響＝米沿岸警備隊「さらに弱った可能性が高い」／米運輸安全委「影響は分からない」／カナダ「引いただけでは原因でない・すでにあった傷を広げたかもしれない」） ／ USCG p.295〈287〉（`subjected the TITAN to repeated impact damage that further weakened its structural integrity of its hull.`）・NTSB p.60（`their actual effects are unknown.`）・TSB §2.1.3（`towing the Titan and submerging it while under tow may have exacerbated existing damage.`）
> そう。引かれたことの影響も、見方が分かれる。米沿岸警備隊は、
> 船体がさらに弱った可能性が高い、とみる。カナダの調べは、引いただけでは、
> 原因になった見込みは低いが、すでにあった傷を広げたかもしれない、とする。

**cb14** ／ 図 再現 TSB 付録B の2023年の4行（10・10・10・3346） ／ TSB §1.21.4（`The dive was aborted at a depth of 10 m. The Titan did not disconnect from the LARS on this dive.`）・NTSB p.14（`None of the dives exceeded 33 feet (10 meters) depth.`）・USCG p.256〈248〉（`10 m dives were dives which did not leave the LARS platform.`）
> Q: 事故の年も、潜ってはいたの？
> 人が乗った潜航は3回。どれも深さ10メートルで止まり、台からも離れなかった。

**cb15** 🔧 ／ 実写 MBI 図115 台を浮かせる空気の装置（黄と赤の浮き袋・USCG 報告 p.145・A＝副題「台を浮かせる空気の装置（事故の後に撮影）」） ／ USCG p.295〈287〉（`repeatedly slammed against the LARS platform for approximately 45-minutes by passing ocean swells`）・p.295〈287〉（`There is no evidence that OceanGate conducted a post-incident hull inspection or incident report`）
> 米沿岸警備隊によると、3回目の潜航では、台の浮き沈みの調整を誤り、
> 潜水艇は波で約45分、台に打ちつけられた。そのあと船体を点検した記録は無い。

**cb16** ／ 図 再現 監視装置の記録の有無（2022年＝あり／2023年＝なし） ／ USCG p.139〈131〉（`No real-time monitoring data was available to the MBI from Expedition 2023 (Dives 84-88).`）・TSB §1.10.9（`There was no data available for the 2023 season.`）
> 2023年の潜航の、監視装置の記録は、残っていない。

**cb17** 🔧 ／ 図 再現 危険度の点数（事故の回＝35・「48を超えるとストライク」の決まり＝TSB 図16 は使わず数だけ） ／ TSB §1.17.12.1（`The mission director checklist specified that a risk index of greater than 48 was considered to be a strike. The risk assessment for the occurrence dive (Figure 16) had a risk index of 35.`）・USCG p.78〈70〉（`If there was a total of three or more “strikes” encountered during a dive evolution, the Mission Director was required to cancel the day’s dive operation.`）
> 6月18日の潜航の計画で、危険度の点数は35。会社の決まりでは、
> 48を超えると「ストライク」が1つ付き、3つたまると、その日の潜航をやめる。

**cb18** 🔧 ／ 図 再現 NTSB の所見2（英字＋訳は字幕） ／ NTSB p.73（`After dive 82, the Titan sustained additional damage—of unknown origin—that further deteriorated and weakened the pressure vessel to a point where it could not survive a dive to the depth of the Titanic.`）
> 米運輸安全委員会は、2022年7月22日の潜航のあと、
> 出どころの分からない傷みが加わり、
> タイタニックの深さに耐えられないほど弱っていた、とみている。

**cb19** 🔧 ／ 図 帯 2023年6月18日（この年初めて台を離れて深く潜る潜航） ／ USCG p.295〈287〉（`Dive 88 was the first dive to leave the LARS platform for the TITANIC Survey Expedition 2023`）・NTSB p.16（`It was the first dive of the 2023 expedition to descend below 33 feet (10 meters).`）
> そして6月18日。それは、この年、人が乗って初めて台を離れ、深く潜る潜航だった。
> Q: 船体をよく確かめないまま、その日を迎えたんだね。

---

### 第11章　3つの報告書が出した答え（13カット）

**cc01** ／ 実写 米沿岸警備隊の海難調査委員会の公聴会（2024年9月・USCG の公式の配信・委員会の職員だけが写る区間・A＝副題「海難調査委員会の公聴会（2024年9月）」） ／ USCG p.5〈v〉（`in what is considered to be a preventable tragedy.`）
> そう。事故のあと、3つの調べが、それぞれの答えを出した。
> 米沿岸警備隊の委員会の報告は、防ぐことができた事故と考えられる、と書き出す。

**cc02** ／ 図 再現 主な要因8つ（USCG p.7 の8項目の要点の札＝主語は全部「会社」か「船体」・欄の英字は小さく） ／ USCG p.5〈v〉（`OceanGate’s failure to follow established engineering protocols for safety, testing, and maintenance of their submersible, was the primary causal factor.`）・USCG p.7〈vii〉（`The primary causal factors that directly contributed to the casualty include:`）
> 主な原因は、会社が、安全と試験と整備について、確立された手順に従わなかったこと。
> 挙げた主な要因8つは、どれも会社と船体のことだ。

**cc03** 🔧 ／ 図 再現 同じ札（7つ目＝職場の文化・その他の寄与要因の4つ目＝規則の足りなさ） ／ USCG p.7〈vii〉（`used firings of senior staff members and the looming threat of being fired`）・USCG p.8〈viii〉（`the lack of comprehensive and effective regulations for the oversight and operation of manned submersibles`）
> 幹部の解雇と、解雇の脅しで、安全の懸念を言いにくくした職場も、その1つだ。
> 規則の足りなさは、その他の要因に挙げられた。

**cc04** 🔧 ／ 実写 米沿岸警備隊の記者会見（2024-09-15・公聴会の前・A・登壇は公的な任務の人＝副題「公聴会の前の記者会見（2024年9月）」） ／ NTSB p.74（`the probable cause of the hull failure and implosion of the submersible Titan was OceanGate’s inadequate engineering process,`）・NTSB p.74（`which failed to establish the actual strength and durability of the Titan pressure vessel`）
> Q: 米運輸安全委員会は、どう書いたの？
> 推定される原因は、会社の技術の進め方が不十分だったこと。
> 船体の本当の強さと持ちを、確かめないままだった、とした。

**cc05** 🔧 ／ 図 再現 推定原因の「寄与」（指針と規則が足りなかった・監視の記録の読み違い） ／ NTSB p.74（`Contributing were US and international voluntary guidance and US small passenger vessel regulations that were insufficient to ensure OceanGate adhered to established industry standards.`）・p.74（`Also contributing was OceanGate’s flawed analysis of their pressure vessel monitoring system data`）
> 原因を後押ししたのは、会社に業界の基準を守らせる規則や指針が、足りなかったこと。
> そして、会社が監視の記録を読み違えたことだ。

**cc06** ／ 図 再現 TSB の所見（原因と寄与5＝会社と船体の札） ／ TSB §3.1（`The as-built properties of the Titan’s carbon fibre cylinder were never validated to ensure they met the theoretical values used in the design process,`）・§3.1（`likely led the cylinder to fail progressively with damage accumulating during each dive cycle until it imploded`）
> カナダの調べは、筒の実際の強さは一度も確かめられず、
> 潜るたびに傷が積もって壊れた可能性が高い、とした。

**cc07** ／ 図 再現 TSB の要点（運輸省は登録が無いと知らなかった・ほかの役所の情報が届かなかった） ／ TSB §4.2.1（`TC was unaware that the Titan was not registered with any flag state.`）・TSB §1.28.5（`In this occurrence, both DFO and the CBSA had information about the Titan that TC was not aware of.`）
> カナダの運輸省は、タイタンがどの国にも登録されていないことを、知らなかった。
> ほかの役所が持っていた情報も、届いていなかった。

**cc08** 🔧 ／ 図 再現 TSB の勧告6つ（宛先は6つともカナダ運輸省・番号 M26-02〜07） ／ TSB §4.2（`The investigation identified safety deficiencies that led the Board to issue the following 6 recommendations.`）・TSB の勧告のページ（rec-m2602・m2604〜m2607＝Date of the latest response: N/A・Not Yet Assessed／m2603 は頁なし＝2026-10-14 に見た・3冊の外・記録は src/new/tsb_rec/）
> カナダの調べは、運輸省に6つの勧告を出した。
> 運輸省の返事は、2026年10月の時点で、勧告のページにまだ載っていない。

**cc09** ／ 図 帯 3つの答えの並べ（重なる所＝窓でなく船体の炭素繊維の側・強さと寿命を確かめず・監視の読み方） ／ USCG p.325〈317〉（`the probable failure point of the hull was either the adhesive joint between the TITAN’s forward dome and the titanium segment or the carbon fiber hull near the forward end of the TITAN.`）・NTSB p.73（`the company was unaware of its actual strength and durability`）・TSB §2.1（`suggested that the pressure hull’s carbon fibre cylinder was the likeliest point of failure.`）・TSB §3.1（`OceanGate did not know for how long the pressure hull would remain safe`）
> Q: 答えは、どれも同じなの？
> 重なる所が多い。壊れたのは窓ではなく、船体の炭素繊維の側。
> 会社は本当の強さと寿命を確かめず、監視の記録も生かせなかった。

**cc10** 🔧 ／ 図 帯 同じ並べ（分かれる所＝2022年の音の重み・最後の数秒の順番を明るく） ／ USCG p.289〈281〉（`strongly suggests that the carbon fiber hull sustained irreversible damage at the end of Dive 80.`）・NTSB p.73（`The Titan pressure vessel likely sustained damage after it surfaced at the end of dive 80`）・TSB §1.10.10.1（`so it cannot be determined whether this event precipitated the non-linear readings on 19 July 2022.`）
> Q: 分かれる所は？
> 2022年の音をどれだけ重く見るかと、最後の数秒の順番だ。

**cc11** 🔧 ／ 図 再現 規則と監督の穴の重み（米運輸安全委＝寄与／米沿岸警備隊＝その他の要因／カナダ＝危険の所見） ／ NTSB p.74（`Contributing were US and international voluntary guidance and US small passenger vessel regulations`）・USCG p.8〈viii〉（`the lack of comprehensive and effective regulations for the oversight and operation of manned submersibles`）・TSB §3.2（`Canada’s approach to regulatory oversight of vessels enabled the Titan to operate without any independent verification to identify safety deficiencies,`）・TSB §3.2（`These factors may or may not have been causal or contributing to the occurrence`）
> 外から監督する仕組みの穴も、3つとも書く。ただ、どの調べも、
> それを主な原因にはしていない。
> Q: 止めることができたのは、まず会社自身だったってこと？

**cc12** ／ 実写 米沿岸警備隊の記者会見（DVIDS 888248・2023-06-25・海難調査委員会を開くと発表・器 1280・A＝副題「海難調査委員会を開く記者会見（2023年6月25日）」） ／ USCG p.307〈299〉（`Had OceanGate adhered to the safety standards outlined in its own HSE Manual and fostered a culture of transparency and accountability, this tragedy would likely have been averted`）
> そう。米沿岸警備隊は、会社が自分の安全の手引きを守り、
> 隠さず責任を持つ文化を育てていれば、この事故はおそらく避けられた、と書いている。

**cc13** 🔧 ／ 図 再現 同じ節の一節（英字＋訳は字幕） ／ USCG p.307〈299〉（`Encouraging employees to voice concerns without fear of retaliation and prioritizing safety over expediency could have prevented the sequence of events that led to the disaster.`）
> 社員が仕返しを恐れずに懸念を言える場をつくり、早さより安全を先にしていれば、
> 防げたかもしれない、とも。

---

### 終章　3つの問いの答え（9カット＋共通エンディング）

**cd01** 🔧 ／ 実写 ROV「尾部」（04・c101・c108・c517 と別の区間・第三者＝引用・額装＝副題「海の底の残骸（2023年6月22日）」） ／ —
> Q: はじめに立てた問いの答えは、出たの？
> 出ている。まず、何が壊れたのか。

**cd02** 🔧 ／ 図 再現 3つの問いの札（①何が壊れたのか＝「窓ではなく船体の炭素繊維の側」を明るく） ／ NTSB p.74（`resulting in a damaged internal structure that subsequently led to a local buckling failure of the pressure vessel.`）・TSB §2.1（`suggested that the pressure hull’s carbon fibre cylinder was the likeliest point of failure.`）
> 窓ではなく、船体の炭素繊維の側だ。層の一部は爆縮の前からはがれ、
> 傷が重なって弱り、押しつぶされたとみられる。

**cd03** 🔧 ／ 図 再現 同じ札（②なぜ潜り続けたのか） ／ USCG p.290〈282〉（`should have been a red flag to stop all dive operations. However, OceanGate proceeded to continue scheduled dive operations afterward,`）・USCG p.289〈281〉（`a cursory external examination of the TITAN was conducted following the loud bang with no visible damage identified.`）・USCG p.290〈282〉（`directed that no further investigation or assessments were necessary`）・USCG p.290〈282〉（`neither the Director of Engineering nor anyone else onboard with the authority to assess the submersible’s safety possessed the necessary engineering expertise to interpret the strain gauge data`）
> 次に、なぜ潜り続けたのか。2022年の音のあと、CEO は調べは要らないと指示し、
> その場に記録を読み解ける人もいないまま、外から軽く見ただけで、予定どおり潜った。

**cd04** 🔧 ／ 図 再現 同じ札（③誰が止められたのか） ／ USCG p.307〈299〉（`this tragedy would likely have been averted`）・NTSB p.74（`the probable cause of the hull failure and implosion of the submersible Titan was OceanGate’s inadequate engineering process,`）・TSB §3.1（`These are the factors that were found to have caused or contributed to the occurrence.`）・TSB §1.23.1（`some OceanGate employees with expertise in specific areas left the company or were dismissed after raising safety-related concerns`）・NTSB p.70（`the existing regulations and voluntary guidance, as currently written, enabled OceanGate’s operation of the Titan in an unsafe manner.`）
> そして、誰なら止められたのか。3つの報告書が主な原因に挙げるのは、会社自身だ。
> 安全の懸念を言った社員の中には、辞めた人も、辞めさせられた人もいた。
> 外から止める仕組みが働かなかったことは、主な原因の次に置かれている。

**cd05** ／ 図 再現 TSB の一節（過去の成功は将来の成功を約束しない＝英字＋訳は字幕） ／ TSB §1.23.1（`On each occasion, OceanGate had been able to recover the Titan.`）・TSB §1.30.2（`However, past success is not a guarantee of future success,`）
> うまくいかないことが起きても、そのたびに、潜水艇は戻ってきた。
> カナダの報告書には、こんな一文もある。過去の成功は、将来の成功を約束しない。

**cd06** 🔧 ／ 図 再現 同じ節の続き（ずれは少しずつで気づきにくい） ／ TSB §1.30.2（`because this drift occurs gradually, it is not easily identifiable and may go unnoticed as risk levels grow over time.`）
> 安全なやり方からのずれは少しずつで、気づかれにくい、とも書く。
> Q: 少しずつだと、気づきにくいんだね。

**cd07** 🔧 ／ 実写 24-011 図43 前部と後部のセグメント（パレットの上・NTSB 研究所・A・c606 の FBI 図159 とは別の写真＝副題「回収された前と後ろのチタンの輪（研究所）」） ／ USCG p.307〈299〉（`This tragedy serves as a stark reminder of the critical importance of prioritizing safety in high-risk operations`）
> そう。米沿岸警備隊は、危険の高い仕事で安全を先にすることの大切さを、
> この事故は強く思い出させる、と書いている。

**cd08** ／ 実写 ROV「後ろのドーム」（07・c105・c523・c602 と別の区間・第三者＝引用・額装） ／ NTSB p.9（`All five persons on board the vessel died.`）
> 2023年6月18日、タイタニックの眠る海で、5人が亡くなった。
> その日までの道のりは、3つの報告書の記録の中に残っている。

**cd09** 🔧 ／ panel コメントの問い（文字だけ＝問いの2行・ed01 の直前） ／ —
> あなたは、もし乗れるとしたら、深い海の底を自分の目で見てみたいですか。
> よければ、コメントで教えてください。

## 5. 使わなかったもの（理由）

| 物 | 理由 |
|---|---|
| 米海軍が当日に爆縮の音を探知していた（報道） | 3冊に無い（カード g2 #24＝「Navy」の近くに acoustic・detect が0件）。出どころの報道（WSJ・匿名の高官）の原文を確かめていない（legend 11）。kousei §9 は「帰属つきなら可」だが、④では確かめられないので入れなかった＝④' で原文を開けるなら c511 の後に1行 |
| CEO「ある所から先、安全はただの浪費だ」 | 3冊に無い（カード g3 7-48）。2022年のポッドキャストの発言（報道）＝原典の音声を確かめていない（legend 20） |
| CEO「沿岸警備隊が問題になったら、議員を1人買って片づける」 | NTSB p.47・USCG p.299〈291〉にあるが、社員の伝聞の言葉で強い＝切り取りになりやすい。c719 は同じ社員の「肩書きを変えるだけでは済まない」までにした |
| 6月22日の記者会見の発言 | 3冊に無い（カード g1 #3b）・映像を見ていない＝c102 は会見の映像を背にして、語りは TSB §1.3.3 の字（決定的な証拠と示した） |
| 記録の音（NOAA の録音・通信班の映像 CG 141） | 10-14 の決め（鳴らさない・遺族の顔）。NOAA の録音の「約16分後」（TSB §1.3.2）も語りに入れていない |
| 文字が届くまでの遅れ（USCG 15〜30秒／TSB 約2.2秒） | 3冊で割れる（🆕 D 番号なし）＝D10 の言い方を崩さないため言わない |
| 潜航の予定の長さ（TSB 11時間15分／NTSB 約8時間） | 割れる（🆕） |
| 重りの重さ（鉛の塊・落とす重り） | TSB の中で合わない（§1.3.1 と §1.10.4）＝カード g2 罠 |
| 最初の ROV 船の時刻（D13）・船の種類 | 3冊で割れる（kousei §11-7） |
| 発見の場所の距離（NTSB p.20 の 500m／p.38 の 330m） | NTSB の中で割れる＝「船首から数百メートル」 |
| 誰が ROV を手配したか（米海軍／会社） | 割れる（🆕）＝「米空軍の輸送機で運ばれた」まで |
| 「1つ目の船体は49回潜った」 | NTSB の番号は「出かけた回」の通し番号（人が乗らない回・1m の回も入る）＝人が乗った20回（TSB）だけ |
| 2019年10月の加圧試験の深さ（TSB 4,000m／USCG 3,743m）・2019年8月の試しの潜航（日と中止の理由が割れる） | 割れる（🆕）＝c818 は深さを言わない |
| 業界の委員会の手紙の署名の人数（20人を超える／数十人） | D28＝割れる |
| 1/3 模型の試験の回数・月・深さ（2016年） | D23＝3冊で割れる＝c713 は「目標の4,500m に届かなかった（USCG）」まで |
| 元運航部長が申し立てを取り下げた理由／解任の通知の文／当時の実習生の証言 | 私生活・名前入り・1人の証言（カード g4 罠） |
| 2018年のタイタニックの遠征の中止（雷のせいとされた） | 尺。言い方も割れる（TSB「雷とされた」／USCG「近くの落雷の過電流の可能性」） |
| OSHA から米沿岸警備隊へのメールが担当に届かなかった（USCG）／調査官は連絡を覚えていない（NTSB） | 尺（c8）。cc の監督の穴で使うかは ④' で |
| 遺品の写真（DVIDS 9057368）・引き揚げの ROV 映像3本（6/26）・MBI 図26／27（私人の顔の恐れ） | kousei §8（遺品・遺体の恐れ・私人の顔）。引き揚げの映像は映像方針で全数を見てから |
| ROV の静止画（MBI 図41・24-012 の図1〜24・旧版の titan_rov_*.jpg） | 第三者（Pelagic）の静止画＝ROV は映像の一次（04・07）を額装で受ける |
| 旧版の写真の取り違え（c307・c627＝NTSB 図18 左／c624・c323・c301＝回収片／ep07・pr03＝9月30日の破片） | materials §8-2。図18 左は c803 で正しい副題で使い、図13 は c611 で「研究所で撮影」と副題 |
| TSB の図・写真・動画 | Crown＝営利の再配布は許可が要る（materials §1-5）＝TSB は本文だけを出どころにした |
| CEO の顔の写真（Commons・CC BY 3.0） | kousei §8＝要らなければ使わない＝④では使わなかった（c207・c718 は書類の再現図） |

## 6. 読み間違えやすい語（⑤a の前に確かめる）

| 語 | 読み | 出る所 |
|---|---|---|
| 潜水艇 | せんすいてい | 全体 |
| 耐圧殻 | たいあつかく | c206 ほか |
| 爆縮 | ばくしゅく | c411 ほか |
| 剥離 | はくり | c6・c8・c9・ca |
| 空隙 | くうげき | c6・c8・c9 |
| 座屈 | ざくつ | c617・c618 |
| 尾部 | びぶ | c101・c601 |
| 母船 | ぼせん | 全体 |
| 船籍 | せんせき | c301 |
| 潜航 | せんこう | 全体（「潜行」と取り違えない） |
| 採水器・ニスキン瓶 | さいすいき・ニスキンびん | c405 |
| 一塊 | ひとかたまり | c602 |
| 船級 | せんきゅう | c714 ほか |
| 等級 | とうきゅう | c818 |
| 運航部長 | うんこうぶちょう | c8 |
| 遭難 | そうなん | c508 |
| 救難調整センター | きゅうなんちょうせいセンター | c505 |
| 1円玉 | いちえんだま | c202 |
| 1都6県 | いっとろっけん | c510 |
| 約5.4秒 | やく ごてんよん びょう（④'で 5.397 から丸めた） | c413 |
| 10時47分26.9秒 | じゅうじ よんじゅうななふん にじゅうろくてんきゅう びょう | c413 |
| 3,341メートル・3,149メートル | さんぜんさんびゃくよんじゅういち・さんぜんひゃくよんじゅうきゅう | c406・c408 |
| 約1万3,200メートル | いちまんさんぜんにひゃく | c709 |
| ROV | アールオーブイ | c513 ほか |
| CEO | シーイーオー | 全体 |
| 米運輸安全委員会・米沿岸警備隊 | べい うんゆあんぜんいいんかい・べい えんがんけいびたい（「こめ」と読ませない） | 全体（④'で呼び名をそろえた＝G0-M） |
| 「a」 | エー | c407 |
| ニューファンドランド・セントジョンズ・ポーラープリンス | （カタカナのまま） | c3・c5 |
| バッファロー・メリーランド・バハマ | （カタカナのまま） | c514・c818・c812 |
| 〈CEOの名前〉 | ⑤a で Vault の控えの名前のカタカナに置き換える（台本の字数は置き場の8字＝名前は10字） | c207 |

## 7. 素材との突き合わせ（映像方針へ）

- **ROV 2本（Pelagic＝第三者・引用・額装）の区間の割り振り**：04＝c101（前半）・c108（後半）・c517（中ほど）・cd01／07＝c104（前半）・c105（後半）・c522・c523・c601・c602・cd08＝**同じ区間を2回使わない**（区間の秒は映像方針で）。焼き込み「Depth (m): 3775」は海底の深さ＝壊れた深さ（約3,350m）を ROV の画に重ねない
- **USCG の動く映像（A）**：記者会見 888022（c102・c106・c109・c519＝区間を分ける）・887597（c513）・887718（c508）・887852（c512・器1280）・888248（cc12・器1280）・2024-09-15（cc04）・公聴会の配信（cc01＝委員会の職員だけの区間）・指令センター 887734（c107・c501＝器 2720×1530 の実効の幅を測る）・HC-130J 888012（c103・c516）・888011（c509）
- **A の写真**：MBI 図3（c301）・図5（c305）・図109（cb07）・図18（c307）・図21（c308）・図24（c309）・図31（c405）・図37（c417）・図65（c217）・図112（cb11）・図115（cb15）・図255（c906）／FBI 図157（c607）・図159（c606）・図270（c604）・USCG 図268（c608）／DVIDS 7875444（c510）・7875448（c511）・7875471（c514）・9057342（c603）・9057367（c814）・9057369（c609）／NTSB 図13（c611）・図14（c618）・図15（c911）・図16 上（c914）・図16 下（c909）・図17 下（c913）・図18 左（c803）・図18 右（c901）・図21（ca17・ca18＝図）／24-011 図15（c612）・図21（c614）・図22（c613）・図28（c916）・図39（c819）・図43（cd07）・図47 下（c605）・図48（c616）／Commons タイタニックの船首（c201）
- **第三者（額装・改変なし・サムネに使わない）**：ROV 04・07／NTSB 図8（ca03）・図9（cb01）・図10（cb12）／ホライゾン・アークティック（c218・CC BY-SA 4.0）
- **作る図**：深さの線（c402・c418・c419・c319＝記録の点だけ）・時刻の帯（c411〜c416・c502〜c506・c518）・音とひずみの線（ca07・ca08＝記録の点だけ・元は会社の記録）・書類の再現図（付録A・付録B・表4・同意書・報告の一節＝欄の値は英字のまま・訳は字幕）・模式（引っ張りと圧縮・1層ずつ固める・層のうねり・座屈・監視装置）・棒（安全率・参加費・気温）・地図（セントジョンズ〜現場・捜索の範囲）。🔴 色を多く（10-13）
- 英字の札の訳（§B1-4）：24-011 図15・MBI 図255
- DVIDS の元の大きさ（7875444 ほか 4032×3024）は映像方針で了承を取って落とす

## 8. 概要欄の用語（下書き）

- 潜水艇（せんすいてい）…母船に運ばれ、海に降ろされてから潜る小さな乗り物。タイタンは5人乗り
- 耐圧殻（たいあつかく）…人が乗る、深い海の水の力に耐える殻。タイタンは炭素繊維の筒の両端をチタンのドームでふさいだ形
- 爆縮（ばくしゅく）…外からの水の力で、一瞬で内側へ押しつぶされること
- 炭素繊維（たんそせんい）…細い炭素の糸を樹脂で固めた材料。軽くて強く、旅客機にも使われる
- 剥離（はくり）…貼り合わせた層と層のあいだが離れること
- 空隙（くうげき）…材料や接着剤の中にできた、小さなすき間
- 座屈（ざくつ）…押されて形を保てなくなり、曲がってしまうこと
- 安全率（あんぜんりつ）…壊れる深さが、潜ってよい深さの何倍あるかを表す数。1より大きいほど余裕がある
- 船級（せんきゅう）…国とは別の民間の団体（船級協会）が、船の設計や工事を確かめ、大事な試験に立ち会って証明する仕組み
- ROV（アールオーブイ）…遠くから操る、無人の探査機
- 生命維持（せいめいいじ）…艇の中で酸素を足し、吐いた息の二酸化炭素を取って、息ができるようにする仕組み
- 海難調査委員会（MBI）…アメリカ沿岸警備隊が、大きな海の事故を調べるために開く委員会（裁く所ではない）
- 運輸安全委員会…事故の原因を調べる国の機関。この動画では、アメリカ（NTSB）とカナダ（TSB）の2つが出てくる
- ニューファンドランドの夏時間…カナダの東の端の時間。協定世界時より2時間30分遅れ。この動画の時刻はすべてこの時間

## 9. 換算と計算（式）

> 換算の値＝1ft＝0.3048m・1海里＝1.852km・1psi＝6.894757kPa。計算はこのチャットの scratchpad で機械に出させた（手で写していない）

| カット | 台本の言い方 | 式・元の値 |
|---|---|---|
| c201 | 富士山の高さよりも、まだ深い | タイタニックの深さ 約3,800m（TSB 脚注11）−富士山 3,776m＝24m。会社の記録の 3,840m なら 64m |
| c202 | 1円玉1枚の広さに約1.2トン（乗用車1台ぶん） | 水圧 P＝ρgh＝1,025kg/m³×9.81m/s²×3,800m≈38.2MPa（NTSB p.10 の 5,554.5psi≈38.3MPa と合う）。1円玉＝直径2.0cm→面積 π×1.0²≈3.14cm²。38.2×10⁶Pa×3.14×10⁻⁴m²≈12,000N≈1,224kgf≈1.2トン。乗用車1台は約1.2トンを目安とした（車種で違う＝「ぶん」と丸めた） |
| c205・c301 | 全長6.7メートル／全長70メートル近い | 22ft×0.3048＝6.71m（NTSB p.19 脚注13 も 6.7m）／220ft×0.3048＝67.1m（NTSB）・TSB 表1 は 69.07m＝どちらも「70メートル近い」（④'・G1-016） |
| c210 | 1ドル140円で約3,500万円 | 250,000ドル×140円＝3,500万円（換算の日の率ではない＝「1ドル140円で計算すると」と台本で断った） |
| c219 | 約700〜800キロ | 370海里（USCG p.5〈v〉・NTSB p.1）×1.852＝685.2km／425海里（TSB）×1.852＝787.1km＝④'で幅に（G1-015）。画の札も幅か、帰属つきの2つの値で |
| c402 | あと1,500メートルほど | 約3,800m−2,289m（USCG 4.1.45）＝1,511m |
| c411 | その7秒後 | 10:47:02（送った・USCG 4.1.49）→10:47:09ごろ（爆縮・USCG 4.1.51） |
| c418 | 1平方センチに約340キロ | TSB §1.7 の値「3355 m で 33.587 MPa＝342.49 kg per square cm」をそのまま丸めた（自分の計算ではない） |
| c506 | 8時間8分 | 10:47→18:55（TSB §2.5 の値どおり・自分でも引き算した） |
| c510 | 約4万1,000平方キロ・関東地方の1都6県より広い | 約12,000平方海里（TSB §1.3.3）×1.852²＝41,159km²。関東の1都6県＝茨城6,098.32・栃木6,408.09・群馬6,362.28・埼玉3,797.75・千葉5,156.48・東京2,199.94・神奈川2,416.55＝約32,440km²（国土地理院「全国都道府県市区町村別面積調」令和8年4月1日版の PDF を④で取得＝🔴 機械で読めたのは p.8 の神奈川県 2,416.55 だけ・ほかの6都県は令和7・8年版の写しの値＝④' で原典の表を開いて確かめる）。41,159÷32,440≈1.27＝向きは変わらない。⚠️ USCG p.42〈34〉は 12,145「平方マイル」（＝約31,460km²＝関東より狭い）＝台本は TSB の値と単位 |
| cb04 | マイナス0.5度（④'で「摂氏」を外した＝G5-021） | TSB §1.22 は「-0.5°」とだけ書く（摂氏はカナダの気温の慣例と、TSB がほかの所で °C を使うことからの読み＝推測） |
| c518 | 98時間16分 | 6/18 08:24（前のドームを閉め生命維持へ＝TSB §1.3.1）→6/22 10:40ごろ（発見＝TSB §1.3.3）＝98時間16分（TSB §2.5 の値と合う） |
| c104 | 11か月前 | 2022-07-15（80回目）→2023-06-18＝338日＝11か月と3日 |
| c105 | 4日後 | 2022-07-15→07-19（TSB §2.1.1 の字「4 days before the subsequent dive on 19 July 2022」） |
| cb10 | 画の札だけ＝約5,400km（語りの「5,000キロを超えた」は④'で外した＝G5-026） | 2,900NM×1.852＝5,370.8km（USCG p.294〈286〉 more than 2,900 NM＝2023年の遠征の季節）。「〜を超えた」は more than と向きが合う |
| c918 | 100キロ・125キロ・111キロ | 安全率＝壊れる荷÷ふだんの荷（c707＝NTSB p.24 脚注21 の深さの比を荷に置き換えた）。100×1.25＝125・100×1.11＝111（TSB §1.15 の 1.25・1.11）。何メートルでの値かは §1.15 に無い＝たとえに深さを足さない |

## 10. 資料（頁の対応）

| 略 | 資料 | 文字の層（ref/ep22/src/＝git の外） | 頁の書き方 |
|---|---|---|---|
| USCG | Report of the Marine Board of Investigation into the Implosion of the Submersible TITAN（米沿岸警備隊 海難調査委員会・2025-08-04） | `uscg_mbi_pages.txt` | 「p.PDF〈印字〉」＝印字＝PDF−8 |
| NTSB | Marine Investigation Report MIR-25-36（米国家運輸安全委員会・2025-10-02） | `ntsb_mir2536_pages.txt` | PDF の頁 |
| TSB | Marine Transportation Safety Investigation Report M23A0169（カナダ運輸安全委員会・2026-06-17 公表） | `tsb_m23a0169_html.txt`（付録A＝`core_raw/tsb_appxA.tsv`・付録B＝`core_raw/tsb_appxB.tsv`） | 節の番号・脚注の番号・付録 |
| 24-011 | NTSB Materials Laboratory Factual Report 24-011（2024-07-05） | `materials_raw/ntsb_docket_pdf/lab24011.txt`（**3冊の外**） | 画（図15・21・22・39・47・48）の出どころだけ。語りの事実は MIR の字（p.44・p.59） |

- 章ごとの原文の束（下調べの係のカード）＝`src/cards/g1_c1-c3.md`・`g2_c4-c5.md`・`g3_c6-c7.md`・`g4_c8-c9.md`・`g5_ca-cb.md`・`g6_cc-cd.md`（git の外＝私人の名前は伏せてあるが、原文の片の照合の記録を含む）
- 照合の道具＝`v1_build/quotes22.py`（結果＝`v1_build/quotes22_result.tsv`）

## 11. 関連

- 設計図＝[kousei.md](kousei.md)／台帳＝[sources.md](sources.md)（§3 割れる数・§10 ②で見た値）／素材＝[materials.md](materials.md)（§8 場面の網）／通説＝[legend_2026-10-13.md](legend_2026-10-13.md)／旧版の照合＝[claims_check_A_2026-10-13.md](claims_check_A_2026-10-13.md)・[claims_check_B_2026-10-13.md](claims_check_B_2026-10-13.md)／旧版の棚卸し＝[old_script_inventory.md](old_script_inventory.md)／現在地＝[genzaichi.md](genzaichi.md)
- 旧版の台本の写し＝`src/old/old_script_224e259.md`（git の外）
- Vault＝`Projects/引き継ぎ-事故検証-22本目-20261014-④台本.md`（このチャットの引き継ぎ・〈CEOの名前〉の控え）
