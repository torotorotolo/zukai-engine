# 21本目（9.11 米国同時多発テロのリメイク）一次資料の台帳

- 作成：2026-10-11（21本目 ①リメイクの棚卸し「芯の係（一次資料）」・サブエージェント）。通説の判定＝[legend_2026-10-11.md](legend_2026-10-11.md)。旧版の主張113行の照合＝[claims_check_2026-10-11.md](claims_check_2026-10-11.md)（照合の係・**同じ照合はやり直していない**）。旧版の棚卸し＝[old_script_inventory.md](old_script_inventory.md)
- 手元の写しと生の調べ＝`ref/ep21/src/`（git の外）。一次資料の写し（元は `analytics/materials/ep7/`。**コピーしただけ・元は消していない**）＝`src/*.pdf`。取り直した物＝`src/new/`。道具と出力＝`src/core_raw/`
- **画像は開いていない**（PDF の頁の画像も）。PyMuPDF の文字の層と、文字の層0の PDF は OCR（`tools/ocr_win.ps1`・300dpi・陽性対照＝委員会報告 PDF p41 で 2,431字／陰性対照＝白紙で0行）の文字だけで読んだ
- URL は 2026-10-11 19:53（日本時間）に `src/core_raw/url_check.py`（UA＝`zukai-engine-research/1.0`）で確かめた。結果の表＝`src/core_raw/url_check.tsv`
- 🔴 この台帳には**私人（乗客・犠牲になった私人・ご遺族・建物にいた人）と乗っ取った側の個人名を書かない**。乗員の名前は**数だけ**（名前入りの表は `src/core_raw/crew_tally.out`＝git の外・親だけが見る）

---

## 0. 先に結論

1. **委員会報告の頁＝PDF＝印字＋18**（PDF p19〜p585 の563頁すべてで、頁の数字の行と一致。機械で確かめた＝`src/core_raw/pagemap.out`）。照合の係の「＋18」をそのまま採る。前付けは **PDF の頁＝ローマ数字の値**（xv＝PDF p15）。本文＝PDF p19〜p446（印字 p1〜p428）／付録＝PDF p447〜p467（印字 p429〜p449）／注＝PDF p468〜p585（印字 p450〜p567。第1章の注は PDF p469＝印字 p451 から）
2. **govinfo の PDF はいまも開け、手元の写しと md5 が同じ**（`ae44f1ee61cc49d2ef8c4df3cd065e8c`）。刊行日は PDF の文字の層に無いが、**govinfo の書誌（MODS）に `dateIssued 2004-07-22`**（照合の係 §4 #10 の答え。表紙の印字は人が見ていない）
3. **乗員（操縦士・客室乗務員）の名前は、委員会報告の本文に11人・計35回出る**（4機の操縦士8人全員＋地上へ電話した客室乗務員3人）。**残りの客室乗務員22人は注だけに名前が出る**（計42回）。4機の乗員33人（11・9・6・7人）は全員、本文か注のどちらかに名前がある（§1-3）
4. **NIST・FEMA の図の撮影者の表記は、文字の層ではほとんど拾えない**：NCSTAR 1 の図の見出し49件のうち第三者の名・© が2件、「Source: NIST」が2件、**表記なし45件**／FEMA 403 は332件のうち第三者の名6件、**表記なし326件**。⚠️**「表記なし＝政府の撮影」ではない**＝写真を使うなら1枚ずつ出どころを当てる（§4-3）
5. **旧版が使っていない一次資料**のうち、手元に取ったもの＝**スタッフ声明 No.17「Improvising a Homeland Defense」（2004-06-17）**・**NIST NCSTAR 1A（WTC7 の最終報告・2008-11）**・**NIST の FAQ 2頁**（ツインタワー・WTC7）・**93便 CVR の逐語（ムサウイ裁判の証拠 P200056T）の OCR**。旧版のあとの新しい事実＝§7
6. **YouTube の広告のガイドラインは、旧版①の読みと同じ**（英語・日本語とも条文が同じ。「訃報・惨事」の緑はテロ攻撃を名指しで除外・FTO の段の緑「テロ攻撃を中心テーマにした教育的コンテンツ」・経過時間の条項は無い）＝§8
7. **人が原寸で見る頁**＝この係の分は **2件2頁**（P200056T PDF p7 の 10:00:42 の行・NCSTAR 1 PDF p79 の融点の数字）。照合の係の10件19頁（NTSB・NIST・委員会の図表）はそちらの §4。委員会報告の文字0の頁8頁は**画像も線も無い白紙**＝見なくてよい（§9）

---

## 1. 9/11委員会報告（政府印刷局版）

### 1-1 書誌

| 項目 | 中身 |
|---|---|
| 題 | The 9/11 Commission Report: Final Report of the National Commission on Terrorist Attacks Upon the United States |
| 出した機関 | National Commission on Terrorist Attacks Upon the United States（9/11委員会。Public Law 107-306 で設置＝p.xv） |
| 年 | **2004-07-22**（govinfo の MODS `dateIssued`。PDF の文字の層に日付は無い） |
| URL | https://www.govinfo.gov/content/pkg/GPO-911REPORT/pdf/GPO-911REPORT.pdf ＝**200**（2,475,163バイト・md5 が手元と同じ）。書誌＝https://www.govinfo.gov/metadata/pkg/GPO-911REPORT/mods.xml（200）。ISBN 0-16-072304-3（PDF p3） |
| 別の版 | 委員会のサイトの PDF＝https://www.9-11commission.gov/report/911Report.pdf と UNT の写し https://govinfo.library.unt.edu/911/report/911Report.pdf（どちらも 200・**7,574,768バイト＝別のファイル**・md5 `0b72a302b86eecad443bbcdcdc76a5b1`・585頁）。**印字の頁は同じで、PDF の頁が1つ少ない＝PDF＝印字＋17**（539頁で一致・4つの文で確かめた：印字 p21＝サイト版 PDF p38／GPO 版 PDF p39）。⚠️「PDF の頁」で書くときはどちらの版かを添える（この台帳と照合の係は GPO 版） |
| 頁数 | 585（PDF） |
| 文字の層 | **あり（生まれつき・OCR ではない）**。PyMuPDF で 1,936,842字（頁ごとの文字を strip して足した。旧版①の 1,920,395字とは数え方が違う）。⚠️語と語の空白が欠ける（「flight.The」）・行末ハイフンで語が割れる・曲がった引用符＝**NFKC＋空白を潰す＋ハイフンを消す／残すの2通り**で探す（`src/core_raw/srch.py`） |
| 権利 | 連邦の委員会の著作物＝17 U.S.C. §105 で PD。中の写真44点（最大313px・旧版①）は第三者のものを含む＝本文の文字だけを使う |
| 手元の写し | `src/GPO-911REPORT.pdf`（md5 `ae44f1ee61cc49d2ef8c4df3cd065e8c`）・文字の層 `src/GPO-911REPORT.pdf.txt`（md5 `f3a4a9f06c94f99cbb5caa674df25697`）・頁ごとの文字 `src/core_raw/GPO-911REPORT.pages.jsonl` |

### 1-2 頁の換算（照合の係の「＋18」の確かめ）

- 各頁の先頭3行と末尾3行に出る「数字だけの行」を拾い、PDF の頁との差を数えた（`src/core_raw/pagemap.py`）：**差18が563頁・ほかの差は4頁で各1回（本文中の数字の行の誤検出）・食い違い0**。PDF p19（印字 p1）〜PDF p585（印字 p567）で一定
- 前付け：PDF p5＝v、p13＝xiii、p15＝xv、p18＝xviii（ローマ数字の値＝PDF の頁）
- 書き方は照合の係と同じ：「p21（PDF p39）」。注は「第1章 注76 p456（PDF p474）」
- 文字0の頁＝PDF p2・4・8・10・12・162・342・466 の8頁。**画像0・線0＝白紙**（`src/core_raw/cr_blank.out`）

### 1-3 乗員の名前の出方（数だけ。名前は書かない）

数え方：4機の乗員33人の名簿（4機の便ごとの人数＝本文 p4〜p10 の「操縦士2人＋客室乗務員 9／7／4／5人」と一致）を作り、姓か姓名で全頁を探した。一般の英単語と重なる姓（10人ぶん）は姓名で数えた。**同じ姓の別人（175便の乗客とその家族・93便の乗員の家族）は文脈を見て除いた**（道具＝`src/core_raw/crew_tally.py`・`notes_names_check.out`）。⚠️名簿は係の手元の知識から作った＝33人全員が報告書の中に見つかったので名簿は報告書と合っている

| 区分 | 人数 | 回数 | 中身 |
|---|---:|---:|---|
| **本文**（PDF p19〜446） | **11人** | **35回** | 4機の**操縦士8人全員**（機長・副操縦士。各便の最初の段落で「Captain … and First Officer … piloted」の形・各1回、93便の機長だけ2回＝ACARS の返信の引用 p11）＋**客室乗務員3人**（11便の2人＝地上へ電話した2人で計25回、77便の1人＝母親への電話で1回） |
| 注だけ（PDF p469〜） | 22人 | — | 残りの客室乗務員（11便の持ち場の割り当て＝第1章の注 p452（PDF p470。注番号は機械の拾いで 23＝未確認）・175便／77便の乗員＝PDF p472・93便＝PDF p473〜475 の電話の出どころの注ほか） |
| 注（本文にも出る人を含む） | — | 42回 | 同じ姓の別人6回を除いた |
| どこにも出ない | 0人 | — | — |

- 175便の電話をかけた男性の客室乗務員は**本文では名前なし**（「a male flight attendant」p7）。注には名前がある
- 旧版は乗員の名前を語り・画面とも0（old_script_inventory §5-1）

### 1-4 本文・注の中身で、この台帳から引く所（照合の係が当てていない所）

| 何 | 頁 |
|---|---|
| 93便の機内の通話の出どころ（FBI の聞き取り・委員会の聞き取り） | 第1章 注80・注81 p456〜457（PDF p474〜475） |
| 93便の CVR の逐語の出どころ（CVR の録音を委員会がアラビア語の分かる人と聞いた／逐語は NTSB と FBI が作った） | 第1章 注76 p456（PDF p474）・注89 p457（PDF p475） |
| 記録装置の回収（93便の CVR と FDR・77便の FDR は回収、11便と175便は見つからず、77便の CVR は焼けて読めず） | p12（PDF p30）・第1章 注76・注154（PDF p474・p479） |
| 演習「Vigilant Guardian」 | 第1章 注116 p458（PDF p476） |
| インサイダー取引の疑い | 第5章 注130 p499（PDF p517） |
| 刃渡り4インチ未満の刃物 | p84（PDF p102）・第3章 注57 p476（PDF p494） |
| 連邦航空保安官33人 | p85（PDF p103） |

---

## 2. NTSB「Flight Path Study」4本

| 項目 | 中身 |
|---|---|
| 題 | Flight Path Study – American Airlines Flight 11／United Airlines Flight 175／American Airlines Flight 77／United Airlines Flight 93 |
| 出した機関 | 国家運輸安全委員会（NTSB）。委員会報告の注は「NTSB report, “Flight Path Study—…,” Feb. 19, 2002」と引く |
| 年 | **2002-02-19**（4本とも。OCR の文字で確かめた） |
| URL | 元の場所 http://www.ntsb.gov/doclib/foia/9_11/ は**いま PDF を返さない**（同じ URL が HTML を返す）。**Wayback（id_）は4本とも 200**＝例 https://web.archive.org/web/20131203120558id_/http://www.ntsb.gov/doclib/foia/9_11/Flight_Path_Study_AA11.pdf（大きさは手元と同じ） |
| 頁数 | 6・7・7・7＝27頁 |
| 文字の層 | **0（完全なスキャン）**。②（7本目）の OCR＝`analytics/materials/ep7/s2/ocr/*.ocr.txt`（1,257行）。⚠️数字だけ取る・画面に出す値は人が原寸で見る（照合の係 §4 #1〜#5） |
| 権利 | 連邦の機関の著作物＝PD。図（経路・高度）は NTSB が作った図 |
| 手元の写し（md5） | AA11 `406580b71c290ec8007eec621fc9981f`／UA175 `351483d0430f69253e305843160c76e7`／AA77 `6e0b180f545ca120f51e18a9a2c994ac`／UA93 `5104f92c0a71210e6481a4d9b01a0858`（`src/ntsb_flight_path_study_*.pdf`） |

---

## 3. NIST の報告（建物の側）

### 3-1 書誌

| 資料 | 題・年 | URL（2026-10-11） | 頁数 | 文字の層 | 頁の換算 | 手元（md5） |
|---|---|---|---:|---|---|---|
| **NCSTAR 1** | Final Report on the Collapse of the World Trade Center Towers・**2005-09**（PDF p3） | https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1.pdf ＝200（21,693,366バイト＝手元と同じ） | 302 | **OCR 並み**（「BuUding」「thennal」「fmd」など誤字あり） | **印字＝PDF−50**（PDF p51〜241）／PDF p242〜243 は白紙／**PDF p244 以降は印字＝PDF−52**（p244＝192・p245＝193）。前付けは PDF p6＝iv … | `src/ncstar1.pdf`（`c9c740b4f4cbe8e3442e37ee34efd4bc`） |
| **NCSTAR 1A** | Final Report on the Collapse of World Trade Center Building 7・**2008-11**（PDF p3） | https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1a.pdf ＝200（5,737,332バイト＝手元と同じ） | 130 | 生まれつきに近い（誤字が目立たない） | **印字＝PDF−42**（PDF p43〜130・88頁で一致） | `src/ncstar1a.pdf`（`d992fbc734e9cca33ee7c24c87e128f7`） |
| NCSTAR 1-9（WTC7 の詳細・参考） | — | https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1-9.pdf ＝200（52,766,002バイト） | — | 未取得 | — | 取っていない |
| FAQ（ツインタワー） | 「Created: September 14, 2011 \| Updated: September 10, 2021」 | https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-towers-investigation ＝200 | — | HTML | 問いの番号（Q21 など）で引く。⚠️2021年9月に番号を付け替えた（頁の注） | `src/new/nist_faq/faq_towers.html`（`f6ff7a07de8b7cda82710ffa037c3d6e`） |
| FAQ（WTC7） | 頁の中に「September 19, 2011 (updated 11/20/19) \| Updated: September 10, 2021」と「Created September 13, 2011, Updated April 5, 2022」の2つの日付 | https://www.nist.gov/world-trade-center-investigation/study-faqs/wtc-7-investigation ＝200 | — | HTML | 同上（自由落下＝Q32・爆発＝Q33・テルミット＝Q34） | `src/new/nist_faq/faq_wtc7.html`（`d4029f30dcde61f688ef71b620de84d2`） |

- ⚠️ https://www.nist.gov/topics/disaster-failure-studies/world-trade-center-disaster-investigation は **404**（旧版①の記録にある URL）。入口は https://www.nist.gov/world-trade-center-investigation（200）
- 旧版が手元に持っていた ncstar1-3・1-6v1・1-7・1-8v1 は `analytics/materials/ep7/nist/` のまま（この係はコピーしていない）

### 3-2 犠牲者の数が NIST の中でも割れる

| 出どころ | 数 | 中身 |
|---|---:|---|
| NCSTAR 1 表4-1 p48（PDF p98） | **2,749** | 世界貿易センターの犠牲者の居場所の表。注 e「Does not include the five hijackers per aircraft.」（乗っ取った側を含まない） |
| FAQ（ツインタワー）Q3 | **2,735** | 「There were 2,735 persons who died in the attacks on the WTC towers」。内訳に「129 persons aboard the two aircraft (119 passengers and crew, and 10 hijackers)」＝**乗っ取った側10人を含む**。2,749 との差の説明は頁に無い |

→ 数の正本の議論は legend #20（委員会 2,973 と、いまの公的な数）

### 3-3 権利（第三者の写真）

- NIST の文と NIST が作った図は連邦の著作物＝PD。**写真・映像のコマは報道機関・私人のものが多い**（旧版①：NCSTAR 6冊で © が5社7点・「許可を得て転載」14件＝`analytics/materials/ep7/nist/credits_and_time.txt`・`perm_quotes.txt`）
- この係の見本の数え（**図の見出しごと**・文字の層だけ・`src/core_raw/caption_credits.py`）：**NCSTAR 1 の図の見出し49件**＝第三者の名・© あり **2**（図5-2＝FDNY・港湾公社の名／図7-2＝©）・「Source: NIST」など政府だけ **2**・**表記なし 45**
- ⚠️ 見出しの拾いは文字の層が OCR 並みのため**取りこぼしがある**（NCSTAR 1 の図は49件より多い）。また写真の © が**絵の中に焼き込まれている**場合は文字の層に出ないことがある（旧版①の © は本文の層から拾った分だけ）。図3-1「175便が南棟にぶつかる直前」のように調査班が撮れない場面の写真も見出しに表記が無い（撮ったのは第三者のはず＝推測）。**「表記なし」を PD と読まない**

---

## 4. FEMA 403（建物の性能の調査・2002）

| 項目 | 中身 |
|---|---|
| 題 | World Trade Center Building Performance Study: Data Collection, Preliminary Observations, and Recommendations（FEMA 403） |
| 出した機関 | 連邦緊急事態管理庁（FEMA）。調べたのは FEMA と米国土木学会（ASCE）の調査班（BPAT）＝外部の技術者が多い |
| 年 | 2002-05 |
| URL | **https://www.fema.gov/pdf/library/fema403_ch1.pdf ＝200（2026-10-11）**。取り直した第1章の md5 `89c9beffd8f8e09d20aa1ec5f6f2c290` は、旧版①が Wayback から取った `wb_ch1.pdf` と**同じ**。写し＝https://archive.org/details/fema403-wtc（200） |
| 頁数 | 296（旧版①） |
| 文字の層 | あり（612,668字・旧版①）。章ごとの文字＝`analytics/materials/ep7/fema403/*.pdf.txt` |
| 権利 | ⚠️ 旧版①の読み「請負業者が作った部分が多く、§105 が素直に当たらない」。表紙の写真は「courtesy of」（民間の会社）。付録 D の写真は「Photo by（調査班の技術者の名）」が15件 |
| 撮影者の表記（この係の数え） | **図の見出し332件**（章の文字の層・重複を潰した）＝第三者の名あり **6**（第1章 図1-7＝設計事務所・港湾公社、第2章 図2-12＝FDNY、第3章 図3-7＝FDNY、第4章 図4-1＝設計者、第5章 図5-1＝港湾公社・ビルの所有者、図5-11＝港湾公社）・**表記なし 326**。⚠️見出しに表記が無くても FEMA の撮影とは限らない |
| 手元の写し | `analytics/materials/ep7/fema403/`（章ごと・この係はコピーしていない。md5＝`src/core_raw/md5_origin.txt`）・取り直し `src/new/fema/fema403_ch1_now.pdf` |

---

## 5. 93便の CVR の逐語（ムサウイ裁判の証拠 P200056T）

| 項目 | 中身 |
|---|---|
| 題 | United Airlines Flight #93 Cockpit Voice Recorder Transcript（証拠 P200056T＝P200056 の逐語。OCR の頭書き「GOVERNMENT EXHIBIT P200056T 01-455-A」） |
| 出した所 | 連邦地裁（バージニア東地区）・米国 対 ムサウイ（Crim. No. 01-455-A）の検察の証拠。逐語を作ったのは **NTSB と FBI**（委員会報告 第1章 注76 p456＝PDF p474「A transcript of the CVR recording was prepared by the NTSB and the FBI.」） |
| 年 | 2006（裁判で示された年。証拠の頁に日付の文字は拾えていない＝推測） |
| URL | 旧の場所は **404**（素材の係も 2026-10-11 に 404 と記録＝materials.md §5）。証拠の一覧の写し＝`analytics/materials/ep7/moussaoui_prosecution.html`（7本目①・09-13）：P200055＝93便の操縦士と客室乗務員・座席・**機内からの電話**の要約／P200056＝FDR と CVR の要約（**封印**）／**P200056T＝P200056 の逐語（公開）** |
| 頁数 | 9 |
| 文字の層 | **0（完全なスキャン）**。この係が OCR した＝420行・7,536字（`src/core_raw/P200056T.ocr.txt`）。⚠️**取りこぼしがある**：10:00:42 の時刻の行はあるのに中身の字が無い（§9） |
| 権利 | NTSB と FBI が作った逐語＝連邦の著作物＝PD と読める（推測を含む＝裁判所の頁に権利の文は無い）。⚠️中身は乗っ取った側の声と機内の暴力の音の記述＝扱いは親が決める |
| 手元の写し | `src/P200056T_ua93_cvr_transcript.pdf`（元 `analytics/materials/ep7/mx_P200056T.pdf`・md5 `e433a64597f07df8b17aacce27adf2dc`） |

- OCR で「Let's roll」「roll」は0件（ただし上の取りこぼしがある＝「0件」は「無い」ではない）。委員会報告は CVR から「Roll it!」を引く（p14＝PDF p32・10:00:26 の16秒後）

---

## 6. 委員会のスタッフ声明 No.17「Improvising a Homeland Defense」

| 項目 | 中身 |
|---|---|
| 題 | Improvising a Homeland Defense — Staff Statement No. 17 |
| 出した機関 | 9/11委員会のスタッフ。**第12回（最後の）公聴会 2004-06-17（木）**に読み上げた（https://govinfo.library.unt.edu/911/hearings/hearing12.htm） |
| URL | https://govinfo.library.unt.edu/911/staff_statements/staff_statement_17.pdf ＝200（127,562バイト）。一覧＝https://govinfo.library.unt.edu/911/staff_statements/index.htm（200） |
| 頁数 | 29 |
| 文字の層 | あり（73,721字） |
| 権利 | 連邦の委員会の著作物＝PD |
| 手元 | `src/new/staff/staff_statement_17.pdf`（md5 `20c011d4121aa0955aee936579dd463d`）・頁ごと `src/core_raw/staff17.pages.jsonl` |

- 最終報告 第1章 1.2・1.3 の元の形。言い方が少し違う所：p15「At 9:42, Command Center learned from **television** news reports」（最終報告 p29 は「news reports」）・「This was a **totally** unprecedented order.」・p13 ラングレー機が東へ向かった3つの理由（「a "generic" flight plan incorrectly led the Langley fighters to believe they were ordered to fly due east (090) for 60 miles」）・p18〜19「Conflicting Accounts」（NORAD の公の説明が事実と違った件）
- 最終報告が出た以上、引くのは最終報告（スタッフ声明は「早い時期の委員会スタッフの言い方」として）

---

## 7. 旧版が使っていない一次資料と、旧版のあと（2026-09-14 以降）に増えた物

（2026-10-11 親が検索で確かめた分。ウェブの係は未完のまま返った＝残りは ②③ の宿題＝下の【未完】）

| 何 | 中身 | 出どころ | 日付 | 旧版 |
|---|---|---|---|---|
| いまの犠牲者の数 | **2,977人**（WTC 2,753・ペンタゴン 184・93便 40＝乗っ取った19人を含まない）。記念館には 1993-02-26 の6人を足した 2,983 の書き方もある | 9/11 Memorial & Museum の FAQ https://www.911memorial.org/911-faqs ・年表 https://timeline.911memorial.org/timeline/10686 | 確認 2026-10-11 | 旧版は委員会の 2,973（2004-07-09 時点・第9章 注188） |
| 身元の確認の続報 | 市の検視局（OCME）が、遺伝の系譜の調べ（FIGG）で身元が分かった初めての犠牲者を公表（市警と共同）。検視局の頁に総数の記述は無い＝「約1,650人が確認・約4割が未確認」は報道の数（二次） | OCME https://www.nyc.gov/site/ocme/news/cm0226/mayor-mamdani-office-chief-medical-examiner-new-identification-world | 2026-08-24 | 旧版の公開の前だが使っていない |
| 軍事委員会（グアンタナモ） | 首謀者とされる被告ら4人の公判を 2028-06-05 に開くと軍事判事が決めた（検察の 2027-01 案は退けた）。2025年の控訴裁判所は国防長官が司法取引を撤回できると判断 | 報道（例 WNEM 2026-08-27） | 2026-08-26 | 使っていない（旧版は「なぜ狙われたか」を扱わない） |
| 25年の節目 | 2026-09-11 の追悼（ペンタゴンの式典） | 報道 | 2026-09-11 | — |
| 2026-09-14 より後 | 新しい公表・判決・記録は**見つからなかった**（検索3通り・2026-10-11・全数ではない） | — | — | — |

旧版が使っていない一次資料（手元にある物）＝スタッフ声明 No.17（§6）・NCSTAR 1A と NIST の FAQ（§3）・93便の CVR の逐語 P200056T（§5）。

【未完＝②③ の宿題】国防総省・運輸省の監察総監の2006年の報告（legend #20 の「わざと」）／「Let's roll」の最初の出どころ（#5）／93便の機内からの電話の本数（ムサウイ裁判の証拠 P200055・#26）／NARA の委員会記録（MFR）・「28ページ」（2016）・FBI の機密解除（2021〜22）の URL

---

## 8. YouTube「広告掲載に適したコンテンツのガイドライン」（2026-10-11 の原文）

- URL：https://support.google.com/youtube/answer/6162278?hl=en ＝200（HTML 1,722,420バイト・md5 `f8901be502380ba075f2af15aa07d384`）／?hl=ja ＝200（md5 `f8bfa685dbd614f99952ea6966f1b4b0`）。写し＝`src/new/yt/`（HTML と文字）。取った日時 2026-10-11 19:53
- 節の並び（英語）：Inappropriate language／**Violence**／Adult content／Shocking content／Harmful acts and unreliable content／Hateful & derogatory content／Recreational drugs／Firearms-related content／Controversial issues／**Sensitive events**／Enabling dishonest behavior／Inappropriate content for kids and families／**Incendiary and demeaning**／Tobacco-related content

### 8-1 旧版①の読みとの突き合わせ

| 旧版①の読み（帳簿の note・7本目①の引き継ぎ §7-1） | 2026-10-11 の原文 | 変わったか |
|---|---|---|
| 「訃報・惨事」の緑は**テロ攻撃を名指しで除外** | Violence ＞ 緑（This content can earn ad revenue）＞ Death & tragedy：“Coverage of tragedies involving one or more deaths (excluding sensitive events such as mass shootings or terrorist attacks) with limited or no display of violent acts or their results.”／日本語「暴力行為またはその結果の描写が制限されるかまったくない、1 人以上の死者を出した惨事の報道（銃乱射事件やテロ攻撃などのデリケートな事象を除く）。」 | **同じ** |
| 別の緑＝FTO の段の「テロ攻撃を中心テーマにした教育的コンテンツ」 | Violence ＞ 緑 ＞ Foreign terrorist organizations (FTOs)：“Educational, journalistic reports, or music videos discussing a terrorist attack as a central subject.”／日本語「テロ攻撃を中心的なテーマとして議論している、教育的コンテンツ、ニュース報道、ミュージック ビデオ。」 | **同じ** |
| 経過時間の条項は無い | 英語「time has passed／elapsed／since the event／years ago」0件、日本語「経過」「時間が経」0件。「recent」は黄の “A documentary on a recent homicide …” の1か所だけ（殺人の話） | **同じ**（無い） |
| 黄の引き金は絵でなくナレーション | 黄（limited ad earnings）の要約：“… description of graphic details of tragedies …”／例：“Highly graphic descriptions of tragedies (in the form of audio or video).”・“Reporting of tragedies involving multiple casualties which include graphic or gruesome details.” | **同じ** |
| 「起きていない」「遺族はやらせ」は赤 | Incendiary and demeaning：“Content that suggests a tragic event did not happen, or that victims or their families are actors, or complicit in a cover-up of the event”／Hateful & derogatory の黄〜赤の例に “Denies tragic events happened and are cover-ups.” | **同じ**（「隠蔽に加担した」も入っている） |

### 8-2 旧版①が書いていない条文（21本目で効くもの）

- **緑の中**（Violence ＞ Death & tragedy）：“Implied moment of death or severe bodily harm in an educational, documentary, journalistic reporting or music video context.” の下の段に “Severe property damage where death or severe bodily harm likely occurred (such as bombings, fires, building collapses, etc).”＝**建物の崩壊を教育・記録の文脈で扱うのは緑**。同じ下の段の文が、赤では “Non-educational, documentation, or news of implied moment of death or severe bodily harm.” の下にある（HTML の入れ子で確かめた＝`src/core_raw/yt_nesting2.out`）＝分かれ目は「教育・記録・報道の文脈か」
- **赤**（FTO）：“Non-educational videos focusing on FTOs or the subject of terrorism, such as: Discussions of a terrorist attack as a central subject. Relevant imagery or names of the group/leader anywhere in the content (such as in the thumbnail).”＝**教育的でないと見られると、同じ「テロ攻撃が中心」が赤に落ちる**（2つの例は “Non-educational videos …, such as:” の下の段＝HTML の入れ子で確かめた＝`src/core_raw/yt_nesting3.out`）。旧版の決め「サムネに組織と首謀者の名と顔を置かない」はこの条文の2つ目の例（“such as in the thumbnail”）に当たる＝教育的と読まれれば赤ではないが、読まれなかった時の保険として旧版の決めは今も効く
- **赤**（FTO）：“Content that celebrates or denies terrorist attacks.”
- **赤**（War & conflict）：“Graphic images or accounts of shootings, explosions, executions, or bombings.”＝**爆発の生々しい語り（accounts）は文脈を問わず赤**の書き方
- **Sensitive events**（デリケートな事象）：“Examples of sensitive events include civil emergencies, natural disasters, public health emergencies, terrorism and related activities, conflict, or mass acts of violence. This policy applies even if the content contains no graphic imagery.”・緑 “Discussions involving the loss of life or tragedy that are not exploitative or dismissive.”・“we may allow content to earn ad revenue if it features news reporting, documentary content or discussions about a sensitive event.”・赤 “Using keywords related to a sensitive event to attempt to drive additional traffic.”。⚠️ この節は「During a sensitive event」（いま起きている事象）を前提にした書き方。25年前の 9.11 がいま「sensitive event」に指定されているかは頁から分からない
- **Harmful acts and unreliable content の緑**：“Educational or documentary content with a focus on debunking harmful misinformation.”＝**陰謀論を一次資料で崩す節は緑**の書き方

### 8-3 （参考）コミュニティガイドライン「暴力的な過激主義または犯罪組織」（削除の基準・広告とは別）

- URL：https://support.google.com/youtube/answer/9229472?hl=en ＝200（写し `src/new/yt/vec_policy_en.html`）
- “If posting content related to terrorism or crime for an educational, documentary, scientific, or artistic purpose, be mindful to provide enough information in the video or audio itself so viewers understand the context.”＝**文脈は動画の中（絵か声）で示す**（概要欄だけに頼らない）
- 載せてはいけない例：“Raw and unmodified reuploads of content created by terrorist, criminal, or extremist organizations”・“Footage filmed by the perpetrator during a deadly or major violent event …”＝**実行した側が作った映像・声明の映像は使わない**（旧版も使っていない）

---

## 9. 人が原寸で見る頁（この係の分）

| # | ファイル・PDF頁 | 何を確かめるか | 使う所 |
|---|---|---|---|
| 1 | `src/P200056T_ua93_cvr_transcript.pdf` PDF p7 | **10:00:42 の行の中身**（OCR は時刻だけ拾い、字を拾えていない）。委員会報告 p14 の「Roll it!」がこの行か。あわせて「Let's roll」が逐語の中に無いこと（文字の層0＝全9頁を OCR だけで読んだ） | legend #5 |
| 2 | `src/ncstar1.pdf` PDF p79（印字 p29） | 鋼の融点「about 1 ,600 °C」（OCR 並みの層で数字の間に空白）。FAQ Q21 は「about 1,500」 | legend #10・§2 |

- 合計 **2件2頁**。照合の係の §4（10件19頁）と重ならない
- 委員会報告の文字0の頁（8頁）は白紙＝見なくてよい。NCSTAR 1 の文字の少ない頁（19頁）は図の頁＝この係は図を引いていない

---

## 10. 確かめていないこと

- NCSTAR 1 の図の見出しの取りこぼし（49件より多い）と、絵に焼き込まれた © の数（人が原寸で見るか、NCSTAR 1-5A などの写真の台帳に当たる）
- P200056T の逐語の全行（OCR の取りこぼしがある）
- 乗員の名簿は係の手元の知識から作った（公的な名簿とは照合していない。33人全員が報告書の中に見つかった＝報告書とは合う）

## 11. ②③（2026-10-11）で原寸で見た頁と、ウェブの宿題の答え

> 21本目の2本目のチャット（②③）。**画像は親が自分で見た**（サブエージェントに読ませていない）。頁は PyMuPDF で 110〜200dpi に書き出し、要る所だけ PIL で切り出した（文字の層0の頁は Windows OCR の行の箱で位置を決めた）。写しと切り出しは scratchpad（git の外）。🔴 この節も私人と乗っ取った側の名前を書かない

### 11-1. 人が原寸で見た頁（claims_check §4 の10件19頁＋この台帳 §9 の2件）

| # | 頁 | 見た結果（原寸） | ①の記述との差 |
|---|---|---|---|
| 1 | NTSB 11便 PDF p1〜p2 | 離陸「runway 4R … at approximately 8:00 AM」／「At 8:13:29, while passing through 26,000 ft., Boston Center instructed flight 11 to turn 20 degrees to the right. The crew acknowledged」／「at 8:13:47 (point B), Boston Center instructed flight 11 to climb and maintain 35,000 ft. The crew never acknowledged」／「At 8:24:38 an unknown voice … “we have some planes just stay quiet and you'll be okay we are returning to the airport.”」／「At about 8:21 (point D) radar stations stop receiving transponder returns」／**「impacted the North tower at approximately 8:46:40 (point I)」** | 🔴 **訂正**：①（claims_check §3-1・§4 #1）の「NTSB 約8:?:40（OCR で分が欠ける）」＝**分は刷られている（8:46:40）**＝NTSB は委員会と同じ値。⚠️ 同じ頁の「the 1 hour and 47 minute duration of the flight」は離陸〜衝突（約47分）と合わない＝使わない |
| 2 | NTSB 175便 PDF p2 | 「about 8:33 AM (B)」／「The final radio transmission … at 8:42 (D)」／**「at 8:47, when the aircraft changed beacon codes twice within a one-minute period (E)」**／「At approximately 8:51 … deviated from the assigned altitude」／「At 8:52, FAA's New York Center … attempted to contact the flight several times」／「reaching 33,500 feet」／**「impacted the south tower … at approximately 9:02:40 AM」** | 一致（①のとおり） |
| 3 | NTSB 77便 PDF p2 | 「departed Washington Dulles at 8:20 AM」／「approximately 8:55(C), when the aircraft started a turn to the south. One minute later, radar stations stopped receiving transponder returns」／「At approximately 9:07 AM … leveled off at 25,000 feet … One minute later, the autopilot was disconnected for approximately 3 minutes … as low as 22,000 feet」／**「At approximately 9:29 AM, when the aircraft was approximately 35 miles west of the Pentagon, the autopilot was disconnected (F) as the aircraft leveled near 7000 feet」**／「At 9:34 AM … about 3.5 miles west-southwest of the Pentagon, and started a right 330-degree descending turn to the right. At the end of the turn, the aircraft was at about 2000 feet altitude and 4 miles southwest」／「accelerated to approximately 460 knots (530 miles per hour)」／**「The time of impact was 9:37:45 AM.」** | 一致。「9:08ごろの解除」＝原文は「9:07 の1分後・約3分」 |
| 4 | NTSB 77便 PDF p4〜p7 | **p4＝図2「Altitude Profile」（FDR Pressure Altitude・横倒し）**：8:20 離陸→8:46ごろ 35,000ft→9:00ごろから降下→9:07ごろ約25,000ft（9:09ごろ約22,000ft まで揺れる）→9:22ごろから急な降下→9:29ごろ約7,000ft（F）→約6,800〜8,800ft で揺れ→**9:34ごろから約4分で地上へ**。p5＝地図（横倒し・OCR で「Pentagon」「Impact」）。**p6〜p7＝図ではなく管制の交信の表**（時刻と話し手の欄＝OCR で 8:19:20〜9:03 台） | 🔴 **訂正**：①の「p4〜p7＝図」→図は p4・p5 だけ。c418「最後の数分で一気に」＝線には出るが、9:22〜9:29 の降下も同じくらい急＝kousei §7 |
| 5 | NTSB 93便 PDF p2 | 「departed Newark, NJ at 8:42 am」／「cruising altitude of 35,000 feet at about 9:02 am」／**「a brief descent of about 600 feet starting at 9:28 (C). The words “get out of here” and sounds of a struggle were recorded on the air traffic control radio」**／「CVR … began providing sounds from the cockpit at approximately 9:32」／**「At 9:34 (D) … begins a left turn to a Southeast heading of 120°」**／「maximum altitude of 41,000 feet for about 2 minutes … descending at about 9:39」／「stopped receiving transponder returns … at approximately 9:41」／「From approximately 10:00 to 10:02 there were four distinct control column inputs」／「impacted the ground at about 490 knots (563 mph) in a 40 degree nose-down, inverted attitude. **The time of impact was 10:03:11.**」 | 一致（OCR が落とした「left」を原寸で補った） |
| 6 | NCSTAR 1 PDF p55（印字 p5） | 「The roof of WTC 1 was **1,368 ft above the Concourse Level**, 6 ft taller than WTC 2, and supported a **360 ft** tall antenna mast」／「a square, **about 210 ft** on a side」／「each floor was a square, about 206 ft on a side」 | 一致 |
| 7 | NCSTAR 1 PDF p134（印字 p84） | 表6–1「Times for major events on September 11, 2001.」＝First Aircraft Strike **8:46:30**／Second **9:02:59**／Collapse of WTC 2 **9:58:59**／Collapse of WTC 1 **10:28:22**。崩壊の時刻は「建物全体が崩れ始めたのが最初に見えた時点」と定義 | 一致 |
| 8 | NCSTAR 1-6 PDF p240（印字 p156）／PDF p79（印字 p.lxxv） | 表6–1「WTC 1 Timeline of Observed Structural and Fire Events.」1行目 Start Time **8:46:26**（Floors 93-99・Face N・Columns 109-152）／**Finding 24**「The time to collapse initiation was 102 minutes from the aircraft impact (**8:46:30** a.m. until 10:28:22 a.m.)」 | 一致（同じ巻の中で 8:46:26 と 8:46:30 が割れる） |
| 9 | 委員会報告 PDF p50〜p51（印字 p32〜p33）の図表 | 11便：7:59 Takeoff・8:14 Last routine radio communication; likely takeover・8:19・8:21・8:23・**8:25 Boston Center aware of hijacking**・**8:38 Boston Center notifies NEADS**・8:46 NEADS scrambles Otis・8:46:40・8:53 Otis airborne・9:16・**9:21 Boston Center advises NEADS that AA 11 is airborne heading for Washington**・**9:24 NEADS scrambles Langley fighter jets in search of AA 11**／175便：8:14・8:42・8:42-8:46 Likely takeover・8:47・8:52・8:54・**8:55 New York Center suspects hijacking**・9:03:11・9:15・9:20／77便：8:20・8:51・8:51-8:54・8:54・8:56・**9:05 AA headquarters aware that Flight 77 is hijacked**・9:25 Herndon … nationwide ground stop・9:32・9:34・9:37:46・10:30／93便：8:42・**9:24 Flight 93 receives warning from UA**・9:27・9:28・9:34・9:36・9:41・9:57 Passenger revolt begins・10:03:11・10:07・10:15 | 🔴 **割れる**：77便の 9:05（図表）と本文 p9「Shortly before 9:10, suspecting …」。9:24（受信）は本文と合う。8:38 は本文の 8:37:52 の丸め |
| 10 | 委員会報告 PDF p1〜p4 | p1＝「THE 9/11 COMMISSION REPORT」だけ（半扉）／p3＝扉「Final Report of the National Commission on Terrorist Attacks Upon the United States」「OFFICIAL GOVERNMENT EDITION」・販売の文・ISBN 0-16-072304-3／**p2・p4＝白紙**（画素の最小値255）。**刊行年はどこにも刷られていない**（前付け PDF p1〜p18 の文字の層でも「2004」0件） | 刊行日は govinfo の書誌 2004-07-22（§1-1）で言う |
| 11 | P200056T（93便の CVR の逐語）PDF p7 | **「10:00:25 _In the cockpit. If we don't, we'll die._」**／「10:00:29 **Up, down. Up, down, in the** _cockpit._」／「10:00:33 **The** _cockpit._」／（10:00:37 の行は乗っ取った側の名前を含む＝写さない）／**「10:00:42 _Roll it._」**／「10:00:55 Unintelligible.」。頁の凡例（p1・OCR）「Bolded text = English translation from Arabic」 | 🔴 委員会 p14 の「Roll it!」＝この 10:00:42 の行。委員会の 10:00:26 は逐語の 10:00:25 と1秒違う。⚠️ 全9頁の通しは見ていない＝「Let's roll が逐語に無い」は p7 の範囲だけ |
| 12 | NCSTAR 1 PDF p79（印字 p29） | 囲み「Structural steels do not need to melt to lose strength. Their melting points are **about 1,600 °C**, well above the 1,100 °C typical peak value」／本文「At temperatures of about 300 °C, steel loses about 20 percent of its yield strength」 | 一致（文字の層の「1 ,600」は層の崩れ） |

- 見た画像＝10枚（NTSB 4本の本文4・77便の高度の図1・NIST 4頁の切り出しを1枚に・93便 p7・委員会の表紙と扉1・図表2）

### 11-2. 旧版の言いすぎ・ずれ（claims_check §2）を委員会報告の文字の層で当て直した（②・自分で再現）
- NFKC＋引用符をまっすぐ＋空白を1つに・行末ハイフンを消す／残すの2通りで文の単位で探した（scratchpad `chk4.py`）＝**§2 の20項目は①と同じ結論**
- 足した頁：K025 の「1991」と「1993」＝**第1章 注91・注90（p457＝PDF p475）**（①は頁なし）／K045 の 8:29＝本文は「At 8:23 … Six minutes later, the air traffic control specialist in American's operations center contacted the FAA's Boston Air Traffic Control Center」（p5）＝**8:29 は計算**／K048 の 8:55＝「At about 8:55, the controller in charge notified a New York Center manager that she believed United 175 had also been hijacked.」（p22）／K027＝「reduced from its Cold War high of 26」（p16）・「only seven alert sites left」（p17）
- 手順の3つの前提（kousei の c3 の芯）＝p18「the protocols in place on 9/11 for the FAA and NORAD to respond to a hijacking presumed that • the hijacked aircraft would be readily identifiable and would not attempt to disappear; • there would be time to address the problem through the appropriate FAA and NORAD chains of command; and • the hijacking would take the traditional form …」（①は未使用）

### 11-3. ウェブの宿題の答え（legend #5・#26・§5 の置き場）
| 何 | 答え | 出どころ（2026-10-11 に開いた） |
|---|---|---|
| **93便の機内からの電話の本数**（#26） | 「According to the FBI, **thirty-seven** phone calls were placed from on board Flight 93 between 9:28 … until the time of the crash at 10:03. **Thirty-five** of these calls were made on the Airfones located on the back of the seats in the last nine rows」・「Unless noted, the calls were made on Airfones」（＝残り2本は携帯）・「These phone records were entered as evidence during the sentencing trial of [被告] in 2006」 | 国立公園局（NPS）「Phone Calls from Flight 93」https://www.nps.gov/flni/learn/historyculture/phone-calls-from-flight-93.htm（Last updated: June 24, 2023）＝連邦の機関の頁（FBI の数を引く＝二次の公的な頁）。→ legend #26 は**崩れる**で確定 |
| ムサウイ裁判の証拠の置き場（§5） | 旧の頁は404だが、**裁判所の頁は `coop.vaed.uscourts.gov` に移っている**＝P200055 の頁は開く（説明「Summary from Flight 93 depicting: the identity of pilots and flight attendants, seat assignments of passengers, and telephone calls from the flight」・中身は Flash の ZIP 27MB＝落としていない） | https://coop.vaed.uscourts.gov/moussaoui/exhibits/prosecution/flights/P200055.html |
| **「Let's roll」の最初の出どころ**（#5） | 2001-09-17 の AP（Joann Loviglio）：乗客の1人が機内の電話で GTE の係員と13分話し、受話器を置いて回線が開いたままになったとき、係員が「Let's roll」を聞いた（乗客の妻が係員から聞いた話として）。**CVR の逐語にあるのは 10:00:42「Roll it.」**（§11-1 #11） | Seattle Times の AP の写し https://archive.seattletimes.com/archive/20010917/heroes17/last-words-from-victims-lets-roll （これより早い報道は見つけていない＝全数ではない）。⚠️ 係員の後年の話（「Are you guys ready? Okay. Let's roll」）は二次＝名前は出さない |
| 委員会の聞き取りの記録（MFR） | Commons に NARA の写しの PDF がある（題「Memorandum for the Record (MFR) of …」＝NEADS の説明・ボストン・センターの訪問・運航管理者の聞き取りほか） | Commons のファイルの検索。④で要るときに頁を開く |
| 「28ページ」（2016）・FBI の機密解除（2021〜22） | **調べていない**＝案A・案B とも範囲の外（「なぜ狙われたか」を扱わない） | — |

### 11-4. 国防総省と運輸省の監察総監の2006年の報告（#20 の「わざと」）
- **一次の頁は取れなかった**（運輸省の監察総監のサイト・国防総省の監察総監の置き場で見つからず、写しを載せたブログは Cloudflare で弾かれた＝403）
- 当時の報道で言えること＝**運輸省の監察総監（代行）**：「We did not find evidence to conclude that FAA officials knowingly made false statements」・わざと省いた／誤りを知って直さなかった証拠も無い。ただし FAA の幹部3人が、委員会の問い（公式の時系列）への不正確な答えを直さなかった＝「administrative action」を勧めた（Air Force Magazine の Daily Report「DOT Agrees No Willful Deception」2006-09-07＝https://www.airandspaceforces.com/1140dot ）。報告の番号は CC-2006-085・2006-08-31（ブログの写しの見出し＝二次）
- **国防総省の監察総監**：06-INTEL-12（2006-09-12）＝「不正確だったが、わざとではない」とした、と検索の要約にある（二次・本文は読めていない）
- → 台本で言うなら「2006年、運輸省の監察総監は、FAA の職員がわざと偽った証拠は見つからないとした（当時の報道）」まで。言わないなら委員会報告 p34 の「incorrect」で足りる（kousei §11-3）

### 11-5. ①の在庫の数の訂正（materials.md §7 に詳しく）
- ①「撮影日 2001-09-11・幅1920以上・本当に A＝約470点」は、日付のカテゴリの下に**後年の追悼・行事の写真が混ざる**（2011年の記念館の名前の板・2023〜2024年の式典ほか）。説明に 9/11 の日付がある A は **240点**（ペンタゴン 143・大統領 39・WTC 14・ほか 44）＋日付の語の無い A 152＋議会図書館 251（C'）

## 関連

- [legend_2026-10-11.md](legend_2026-10-11.md)／[claims_check_2026-10-11.md](claims_check_2026-10-11.md)／[old_script_inventory.md](old_script_inventory.md)／[materials.md](materials.md)／[kousei.md](kousei.md)（③の骨）
- 20本目の同じ係の台帳＝[../ep20/sources.md](../ep20/sources.md)
