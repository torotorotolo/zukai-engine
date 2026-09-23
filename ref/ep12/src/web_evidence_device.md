# ep12 装置と威力の事実確認（web 証拠）— 予測威力・リチウム7・シュリンプ・DOE/NV-209

- 取得日：**2026-09-23**（全項目共通。各出典の行にも書いた）
- 範囲：依頼の A1〜A6（番号は依頼文どおり）。文字のみ。画像は見ていない
- 出典の種類（この順に強い）
  - **政府（一次文書）**＝当時の政府・軍の文書そのもの（AEC 一般諮問委員会 GAC の議事録、AFSWP の報告 WT-934、ホワイトハウス記者会見の速記、DNA の説明資料、DOE/NV-209、DNA 6036F、FRUS）
  - **政府（公式史）**＝Hewlett & Holl『Atoms for Peace and War 1953–1961』（AEC 公式史の第3巻。奥付に "Prepared by the Atomic Energy Commission; work made for hire." とある。University of California Press 1989）
  - **政府（DTRA 報告）**＝Kunkle & Ristvet 2013（DTRA の特別報告。著者の Kunkle は LANL 所属）
  - **国立研究所**＝LANL の歴史担当 R. A. Meade の LA-UR 報告、LLNL の Marshall Islands Program のページ
  - **学術**＝査読論文（Fusion Science and Technology）。ジョージ・ワシントン大学の National Security Archive（NSArchive）は「学術（大学の資料集）」とした。**NSArchive が載せる文書そのものは一次、NSArchive の解説文は二次**として扱う
  - **二次**＝Wikipedia、nuclearweaponarchive.org（Carey Sublette）、Brookings の記事、Britannica。**手がかりとしてだけ使い、台本の根拠にしない**
- 引用のしかた
  - 原文のまま写した。変えたのは (1) PDF の改行で割れた単語のハイフンをつないだこと（例：spec- tacular → spectacular）、(2) 連続した空白を1つにしたこと、だけ
  - **OCR（紙の文書を文字に起こしたもの）で崩れている一次文書**（GAC 議事録・WT-934・ストローズ声明）は、**「原文（OCR のまま）」をそのまま写し、そのあとに「読み（整形＝当方）」を別に書いた**。読みは当方の復元であり、原文ではない
  - ページは「印刷ページ」を優先し、わかる範囲で PDF の何枚目かを添えた
- 単位の換算は当方の計算（1 ft＝0.3048 m、1 mi＝1.609 km、1 lb＝0.4536 kg、1 short ton＝0.907 t）
- 取得方法と副作用（正直に書く）
  - HTML は WebFetch で読んだ。Kunkle & Ristvet は DTIC が 403 だったので、Internet Archive の全文検索 API（`fulltext/inside.php`）で段落単位の原文を取った
  - **PDF は WebFetch が本文を読めず、ツールが自動で一時フォルダに PDF を保存した**（当方が保存を指示したものではない）。その自動保存コピーから Python の pypdf で文字を抜いた。新たなダウンロードや、ほかの場所への保存はしていない。自動保存されたファイルは末尾「付記 C」に列挙した
  - 403 で読めなかったもの：tandfonline（Bates & Chadwick 2024 の本文）、dtra.mil（2021年版ファクトシート）、apps.dtic.mil、core.ac.uk。web.archive.org はツールが使えない。scholar.archive.org は CAPTCHA（ロボット確認）が出たので止めた

---

## 0. 結論 — 台本での推奨の言い方（早見表）

| 項目 | 推奨の言い方 | 裏づけ | 詳細 |
|---|---|---|---|
| 事前の予測威力 | 「**事前の予測は4〜8メガトン。いちばん可能性が高いとされた値は6メガトン**」 | 強（1954年7月の AEC 諮問委員会議事録＝一次＋AEC 公式史） | A1-1, A1-2 |
| 5メガトン説 | 使わない。触れるなら「国防側の効果試験の報告は『5メガトン』と書いている」 | 中（WT-934＝一次。ただし国防側の効果試験の計画値の可能性。理由は未確認） | A1-3 |
| 実際の威力 | **15メガトン** | 強（DOE/NV-209 の公式一覧＝15 Mt、GAC 議事録＝15 ± 0.5 MT） | A1-1, A4 |
| 「予測の2.5倍」 | 使うなら「**最有力値6メガトンの2.5倍**」と、**計算だとわかる形**で。政府資料の文言は「3倍近く」（AEC 公式史）・「約3倍」（WT-934。5メガトン基準）・「約2倍」（1954年のストローズ AEC 委員長の公式発表） | 「2.5倍」という**言葉そのものは二次資料だけ**（Wikipedia・nuclearweaponarchive）。6と15は政府資料 | A1-8 |
| 「まったくの想定外」か | 「**予測を大きく上回った**」は強い。「**誰も想定していなかった**」とは言わない | DTRA 報告（2013）：ロスアラモスは安全対策用の「最大値」を15メガトン規模まで見積もって伝えていた（1954年2月18日の電報）。現地の科学責任者オーグルは15メガトン超を前提に人員の安全策を指示 | A1-5 |
| 威力が大きかった理由 | 「**当時ロスアラモスは、リチウム7の核反応で説明した**（1954年7月、カーソン・マーク）」まで。**「リチウム7のせいだった」と断定しない** | 一次は強。ただし **2024年、ロスアラモスの研究者自身の査読論文が「この通説は誤り」と明記** | A2-1, A2-2 |
| リチウム7の扱い | 一次資料の言い方は「**リチウム6や液体重水素よりずっと劣る燃料だと考えられていた**」。「**反応しない（inert）と思われていた**」は二次資料の言い方 | 一次（GAC 議事録）／二次（NSArchive 解説・Wikipedia） | A2-1, A6 |
| リチウム6の濃縮度 約40% | **使わない**。使うなら「約4割とされる」＋二次資料と明記 | **二次のみ**（Hansen『Swords of Armageddon』経由の Wikipedia、nuclearweaponarchive「37〜40%」、Brookings「40%」） | A2-6 |
| 天然リチウムのリチウム6 | 「天然のリチウムでは約7%しかない」 | 強（AEC 公式史 p.162） | A2-3 |
| 装置名「シュリンプ」 | 使うなら「“シュリンプ（エビ）”と呼ばれた装置」 | 中（NSArchive＝学術。LANL 所蔵写真の説明に "Shrimp"）。**政府文書の本文では確認できず** | A3-1 |
| TX-21 | **使わない** | 「シュリンプ＝TX-21」は**二次のみ**（1954年7月の GAC 議事録に開発中の兵器 TX-21 は出てくるが、ブラボーとの結びつきは書いていない） | A3-2 |
| 設計 | **ロスアラモス（LANL）** | 強（DOE/NV-209 の Sponsor 欄＝LANL） | A3-3 |
| 燃料の形 | 「**固体の重水素化リチウムを使う『乾式』の水爆の、最初の実験**」。マイクは「**液体重水素を極低温で冷やす『湿式』**」 | 強（AEC 公式史 p.172「the first test of a dry thermonuclear system」、p.179「the wet device」） | A3-4 |
| シュリンプの重さ・寸法（約10.7 t、長さ4.56 m、直径1.37 m） | **使わない**。使うなら二次資料と明記 | **二次のみ**（nuclearweaponarchive／Wikipedia。元は Hansen） | A3-5 |
| 「爆撃機で運べる初の水爆」 | 「**飛行機で運べる兵器を目指した、乾式の水爆の最初の実験**」。ブラボー自体は**礁の上の小屋に置いて**爆発させた。**「投下された」とは言わない** | 強（AEC 公式史 p.155・p.172、DTRA 報告 p.29。米国が初めてメガトン級を空中投下したのは1956年の CHEROKEE＝DTRA 報告 p.84） | A3-6 |
| アイビー・マイク | 「**1952年11月1日 午前7時15分（現地）、10.4メガトン**」 | 強（DOE/NV-209・DNA 6036F・DTRA 報告） | A3-7, A3-8 |
| マイクの重さ | 数字を言わず「**冷却装置ごと3階建ての建物ほどの装置**」。数字を言うなら出典で割れていると認識する | DTRA 報告（2013）は **80,000ポンド（約36 t）**。「**82トン**」は**二次**（Britannica、Wikipedia が引く Parsons & Zaballa 2017） | A3-9 |
| 公式の実験一覧 DOE/NV-209 | 「**1954年2月28日 18時45分（グリニッジ標準時）＝現地3月1日 午前6時45分、ビキニ環礁、地表、15メガトン、LANL**」 | 強（一次） | A4 |
| 火の玉・雲・クレーター | 「火の玉は数秒で**差し渡し4.8km（3マイル）以上**」「雲は1分で**高さ約14km**、5分で**3万5千m以上**、10分で**幅約120km**」「クレーターは**幅約1.6km**、深さ**約73m**（測深）」 | 強（DTRA 報告 2013・LANL Meade 2021・WT-934） | A5 |

⚠️ **使ってはいけない値**（誤植・誤りと判断したもの）
- AEC 公式史（Hewlett & Holl p.172）の「**H-hour, at 6:54 a.m.**」→ DOE/NV-209（18:45 GMT）・DTRA 報告（6:45 a.m.）と食い違う。**誤植とみて使わない**（A4-3）
- LANL Meade「Operation Castle」の脚注「**March 1st, in the United States.**」→ 逆。米国では2月28日、現地が3月1日（A4-3）
- LANL Meade「Operation Ivy」の表の日付「**1/11/1952**」「**1/16/1952**」→ 書式が崩れている。使わない（A3-7）

---

## A1. 事前の予測威力と、実際の15メガトン

### A1-1　AEC 一般諮問委員会（GAC）第41回会合 議事録（1954年7月）— 予測「4-8 MT」、実測「15 ± 0.5 MT」

- 主張：ロスアラモスでの報告（Graves 博士による Castle の結果の総括）で示された表に、**予測威力（Predicted Yield）4-8 MT、火の玉から求めた全威力 15 ± 0.5 MT** の行がある。**実験名の欄は黒塗り**（"CLASSIFICATION CANCELLED WITH DELETIONS"）だが、Castle で15メガトンはブラボーだけ（DOE/NV-209）なので、この行はブラボー。NSArchive の編者も同じ読み（下の注釈）
- 出典：Minutes, Forty-first Meeting of the General Advisory Committee to the U.S. Atomic Energy Commission, July 12, 13, 14, and 15, 1954, Albuquerque, New Mexico and Los Alamos, New Mexico（元は DOE OpenNet。塗りつぶし版）
  - PDF：https://nsarchive.gwu.edu/sites/default/files/documents/s9j6zr-s789b/35.pdf
  - NSArchive の文書ページ：https://nsarchive.gwu.edu/document/31281-document-35-minutes-forty-first-meeting-general-advisory-committee-us-atomic-energy
- 種類：**政府（一次文書）**。取得 2026-09-23
- 表の直前（議事録 p.-10-、PDF 14枚目）。原文（OCR のまま）：

> In the first talk, Dr. Graves revie;,;ed the results of the Castle

> The following t~ulation gives essentially final results as to yield . and alpha of the various shots.

- 表（議事録 p.-11-、PDF 15枚目）。原文（OCR のまま）：

> Total Yield Yield.
> Predicted (ball of from fission Alpha
> Yield fire} (radiochemical) Shake-l
> 4-8 MT 15 ± 0,5 MT

- 読み（整形＝当方）：列は「Predicted Yield｜Total Yield (ball of fire)｜Yield from fission (radiochemical)｜Alpha」。1行目＝「4-8 MT｜15 ± 0.5 MT｜（黒塗り）｜（黒塗り）」。2行目以降は 11 ± 0.5（ロメオ）、7 ± 0.5（ユニオン）、13.5 ± 1.0（ヤンキー）、1.7 ± 0.3（ネクター）と読め、公式値と合う
- 同じ表の下の注（OCR のまま）：

> The figures· in p~rentheses are those which were predicted before the shots.

- NSArchive 編者の注釈（学術＝二次の解説。文書ページより）：

> This record of the July 1954 GAC meeting includes interesting details on the Castle Bravo test, including that the 'predicted yield' of the detonation was four to eight megatons (p. 11).

- 食い違い：この一次資料は**幅（4〜8）だけで、「6」という1つの数は書いていない**

### A1-2　AEC 公式史（Hewlett & Holl 1989）— 「最有力値は6メガトン」「その3倍近い15メガトン」

- 主張：最有力の見積もりは6メガトン。実測は15メガトンで「最有力値の3倍近く」
- 出典：Richard G. Hewlett and Jack M. Holl, *Atoms for Peace and War, 1953–1961: Eisenhower and the Atomic Energy Commission*（University of California Press, 1989。奥付 "Prepared by the Atomic Energy Commission; work made for hire."）
  - OSTI：https://www.osti.gov/biblio/774455 　全文 PDF：https://www.osti.gov/servlets/purl/774455
- 種類：**政府（公式史）**。取得 2026-09-23
- p.173（PDF 200枚目）：

> From the moment of firing Bravo gave every sign of being a spectacular success. Even the crudest, most preliminary measurements indicated a yield far greater than the six megatons estimated as the most likely figure.

- p.173（PDF 201枚目）：

> Examination of test data gave a yield of fifteen megatons, almost three times the most probable figure.

- 注：15 ÷ 6 ＝ 2.5。公式史はこれを「**almost three times（3倍近く）**」と書いている

### A1-3　WT-934（EX）Castle 効果試験の総括報告 — 「5 Mt ではなく約15 Mt」「予測の約3倍」

- 主張：国防側（軍事効果試験）の総括は、予測を **5 Mt**、実測を約15 Mt とし、「予測の約3倍」と書く
- 出典：WT-934 (EX) EXTRACTED VERSION, *Operation CASTLE, Summary Report of the Commander, Task Unit 13 — Military Effects, Programs 1-9*, K. D. Coleman, Col. USAF, et al., Headquarters Field Command, Armed Forces Special Weapons Project, January 30, 1959（機密部分を除いた版を 1981年5月15日に DNA 向けに作成）
  - https://www.osti.gov/opennet/servlets/purl/16039007-L0uAxS/16039007.pdf
- 種類：**政府（一次文書）**。取得 2026-09-23
- 印刷 p.60（PDF 59枚目）。原文（OCR のまま）：

> The documentation made by Project 3.5 (see Appendix) was not planned, but rather ar. opportunity initiated because Shot 1 gave a higher yield than originaily predicted. The objective of this project was to determine the effects of air blast from a high-yield device on miscellaneous structures. The unexpected high yield of Shot 1 (approximately 15 Mt instead of 5 Mt) caused dam;ige to certain structures at ranges where no damage had been expected.

- 印刷 p.112（PDF 110枚目）。原文（OCR のまま）：

> This project was not in the original program, but the unexpected structural damage which resulted from Shot 1 -with its yield of 15 Mt approxixnitcly three times that predicted-warranted documentation of SU the data possible about structural blast damage from high-yield detonations.

- 読み（整形＝当方）："an opportunity" "originally predicted" "damage" "approximately three times that predicted—warranted documentation of all the data possible"
- 注：Shot 1＝ブラボー。**5 と 6 の差の理由は資料に書かれていない**（国防側の効果試験の計画値だった可能性はあるが、**未確認の推測**）

### A1-4　ストローズ AEC 委員長の公式発表（1954年3月31日）— 「計算上の見積もりの約2倍」

- 主張：当時の公式発表は「約2倍」「制御不能ではなかった」
- 出典：President Eisenhower's Press and Radio Conference No. 33; Accompanied by Admiral Lewis L. Strauss, Chair, Atomic Energy Commission, March 31, 1954, 10:30 a.m.（速記録。NSArchive 文書16）
  - PDF：https://nsarchive.gwu.edu/sites/default/files/documents/s9j6px-77xgg/16.pdf
  - 文書ページ：https://nsarchive.gwu.edu/document/31263-document-16-president-eisenhowers-press-and-radio-conference-no-33-accompanied
  - 大統領記録（American Presidency Project）は声明本文を載せず、Department of State Bulletin vol. 30, p. 548 を指す：https://www.presidency.ucsb.edu/documents/the-presidents-news-conference-358
- 種類：**政府（一次文書）**。取得 2026-09-23
- 原文（OCR のまま。PDF 22枚目）：

> Now, about the specific tests: The first one bas been variously characterized as "devastating" and "out of control," and uitb other soma-what a:xa.ggara.te.id and miatakou descriptions. I would not wish to minimize it. It was e stupendous bleat in the mega ton range, but a·c no t1mo uas tha tes-cing out of control. The misapprehension seems to have arisen due to two facts: first, that the yield was about double that of the calculated estimate -- a margin of error which, I submit, is not incom- patibla with a totally nev weapon. In fact, the range of guesses on tbe first A-bomb covered a considerably relativa1, wider spectrum.

- 読み（整形＝当方）："...The first one has been variously characterized as "devastating" and "out of control," and with other somewhat exaggerated and mistaken descriptions. I would not wish to minimize it. It was a stupendous blast in the megaton range, but at no time was the testing out of control. The misapprehension seems to have arisen due to two facts: first, that the yield was about double that of the calculated estimate -- a margin of error which, I submit, is not incompatible with a totally new weapon..."
- 速記録の冒頭の注（OCR のまま）："This is not an official transcript. Under White House rules, the President must not be quoted <iirectl;Y" ——これは大統領の発言の引用を縛る注。ストローズの声明は国務省広報（DSB）にも載った
- 食い違い：NSArchive 編者は「ほぼ3倍だったのに『約2倍』と言った」と、**誤解を招く発表**だったと評している（文書ページの解説）。台本でこの発言を使うなら「当時の公式発表では『約2倍』」と、**発表であることを明示**する

### A1-5　DTRA 報告（Kunkle & Ristvet 2013）— 「最善の事前見積もりよりはるかに大きい。ただし“まったくの想定外”ではない」

- 主張：(1) 威力は最善の事前見積もりをはるかに超えた。(2) ただしロスアラモスは安全対策用の「最大値」を15メガトン規模まで見積もり、1954年2月18日の電報で現地に伝えていた。(3) 同じ電報の「最有力値」は最大値よりかなり小さい（**数字はこの報告に書かれていない**）。(4) 科学責任者オーグルは15メガトン超の上限を前提に人員の安全策を指示していた
- 出典：Thomas Kunkle (LANL) and Byron Ristvet (DTRA), *Castle Bravo: Fifty Years of Legend and Lore — A Guide to Off-Site Radiation Exposures*, DTRIAC SR-12-001, Defense Threat Reduction Agency, January 2013
  - DTIC：https://apps.dtic.mil/sti/tr/pdf/ADA572278.pdf（403 で読めず）
  - 全文（Internet Archive）：https://archive.org/details/DTIC_ADA572278 　全文検索 API で段落を取得
- 種類：**政府（DTRA 報告。著者1名は LANL）**。取得 2026-09-23
- ページ：印刷ページは Internet Archive の `page_numbers.json`（信頼度 92〜93）で対応させた。以下「印刷 p.77（IA leaf 88）」のように書く
- 印刷 p.77（IA leaf 88）：

> The yield of the BRAVO device was much larger than the best preshot estimates. Legend has it that this came as a complete surprise to both the weapon designers at Los Alamos and to the task force, and it was this unexpectedly large yield that caused the fallout on the inhabited atolls.

> The 15 Mt yield was not a total surprise. The nuclear device designers and task force scientists thought the maximum possible yield of BRAVO could be this large. This upper yield limit, “which is not expected but should be allowed for in safety considerations,” had been calculated by the Los Alamos nuclear device designers at the specific request of the task force scientific staff, and was communicated to Dr. Graves and Dr. William Ogle, commander of the Scientific Task Group (Figure 3-18), in a radiotelegram sent on 18 February 1954 (JF-2130 [1954]). This same message gives the final estimate of the most probable yield to be substantially less than the maximum possible yield. Throughout Operation CASTLE, it was the policy of the task force that personnel protection measures were to be predicated on the maximum possible yields, while protection measures for “things” were to be based on the most probable yields. In December 1953, even as he pressed the Los Alamos device design team for an official yield statement, Dr. Ogle instructed that shot-time aircraft separations (JF-3069 [1954]) and other personnel safety measures for BRAVO be predicated on his personal perception of an upper- yield limit larger than 15 Mt. His appreciation for the uncertainties inherent in the nuclear device may have prevented prompt loss of life in the detonation.

- 電報 JF-2130 の差出人（参考文献一覧、印刷 p.171／IA leaf 182）：

> JF-2130. 1954. Message to Alvin Graves, Task Group 7.1, from Darrol Froman and Carson Mark, Los Alamos Scientific Laboratory. Los Alamos J-Division vault, CASTLE files, Ogle’s notebook. Los Alamos, NM.

- 関連（「威力が大きかったから放射性降下物が島に届いた」という筋立てへの注意。印刷 p.78／IA leaf 89）：

> Although the 15 Mt yield certainly contributed to the BRAVO off-site fallout, it only exacerbated the situation. Had the design yield occurred, the inhabited atolls still would have been contaminated.

> The high yield of the BRAVO device was not in itself the cause of the fallout on the inhabited islands.

- 食い違い：nuclearweaponarchive（二次）は「推定最大値（8 Mt）のほぼ2倍」とする（A1-8）。DTRA 報告は「最大値は15 Mt 規模まで見積もられていた」とする。**「最大値」の定義が違う可能性**（GAC の 4〜8 は「予測の幅」、JF-2130 の上限は「安全対策のために見込む最大値」）。**JF-2130 そのものは web で見つけられなかった**

### A1-5b　DTRA 報告（2013）§3.1〜§3.4 —「知りながら撃った」「風が変わった」も**伝説**とする（④'で追加・2026-09-23）

🔴 **④の写し（p3001）に入っていなかった節。**台本 第1版の筋「島に灰を運んだのは威力ではなく風」は、同じ報告書のこの節が退けている。
取り方＝archive.org の全文テキストを curl で取り、④'のメインが grep で原文を引き直した（頁の画像は見ていない。印刷の頁は全文テキストの頁番号の並びから）。
URL＝https://archive.org/download/DTIC_ADA572278/DTIC_ADA572278_djvu.txt　／　写し＝`web_quotes.txt` の p3003

- **§3.2 冒頭（印刷 p.69）**：An often-told story in the BRAVO lore is that the task force was aware that the winds were blowing toward Rongelap, and that the commander ordered the test to proceed, knowing that these winds would blow fallout to the inhabited atolls. … The clear implication in this piece of BRAVO lore is that the fallout on the inhabited atoll was due to windblown radioactive material from the lower, tropospheric stem of the mushroom cloud. **This is not what happened.**
  - 同じ段落で、この話の出どころとして Weisgall（1994年2月24日の議会公聴会）・Hamilton（1994）・Firth（1987）を名指ししている＝**反対の立場があることを DTRA 自身が書いている**
- **§3.1 末（印刷 p.68）**：**The error in forecasting the BRAVO fallout was that the contribution from the stratosphere was not adequately considered.** Contrary to Lt. Col. Lulejian's widely circulated beliefs on the matter, there was, in fact, significant fallout from the stratosphere.
- **§3.2（印刷 p.70 前後）**：Although material from the lower portion of the cloud stem was initially blown in the direction of Rongelap, before moving far in that direction the fallout particles fell out into the trade winds, which carried them back to Bikini … **The fallout at Rongelap and Rongerik came from the high-altitude bulk of the cloud** that was blown to the north of these atolls.
- **§3.2（印刷 p.73）**：the winds between 5000 and 15,000 ft were essentially calm, and a 10 kn speed to the east was assigned as the most pessimistic situation for shot time. … Debris initially at 20,000 ft altitude would thus move at the most only 20 mi east before it would drop into the trade winds and be carried back to the west, away from the populated atolls.
  - 同じ頁に真夜中の打ち合わせの記録（Clarkson and Graves 1954）：it was considered that the distance to Rongelap and Rongerik compared to the resultant wind speeds were such that no fall-out should reach those atolls. … the time of travel to Rongelap would have been about 12 to 15 hours.
- **§3.2 末（印刷 p.74）**：It was radioactive material from the high-altitude portion of the BRAVO cloud that fell on Rongelap and Rongerik. As is documented by the photography, **the lower altitude winds played no direct role in the contamination of these atolls.**
- **§3.3（印刷 p.76）**：ストローズ委員長の「風が予報からずれた」（1954-03-31）も perhaps the single most enduring staple in the BRAVO lore。Clarkson–Graves 覚書 "Forecast for shot time winds at shot time was essentially correct."
- **§3.4（印刷 p.78）**：Had the design yield occurred, the inhabited atolls still would have been contaminated. **This is because the height and shape of the resulting mushroom cloud do not depend strongly on the yield of a nuclear device.**（p3001 は理由の文を落としていた）
  - 同じ段落（台本 c323 の根拠）：Had the BRAVO yield been closer to design, a very large stratospheric cloud still would have formed. This point is illustrated by the behavior of the 7 Mt CASTLE UNION event (refer to Figure 3-19). The cloud from UNION rose to a height of 94,000 ft, and spread in 10 minutes to form a still rapidly growing stratospheric cloud 45 mi in diameter (WT-933); these values are not greatly different from those of BRAVO.
- **DTRA 2013 の全文に lithium は0件**（web 原典の係の grep）＝リチウム7の話の根拠には使えない（台本も使っていない）

**台本での言い方**：DTRA は国防総省の機関で、当の部隊を擁護する立場にもなりうる。反対の証言（1994年の公聴会）もある。
→ 「**2013年の報告書は〜とする**」と帰属を付けて言い、**どちらかに寄せて断定しない**（記憶 feedback-famous-cause-may-be-legend）。

### A1-6　DNA（国防核兵器局）の説明資料「Operation CASTLE」— 「予想威力を大きく上回った」

- 出典：Fact Sheet, Defense Nuclear Agency, Public Affairs Office, Washington, D.C. 20305, "Operation CASTLE"（日付の記載なし）
  - https://www.osti.gov/opennet/servlets/purl/16367220-1TWi06/16367220.pdf
- 種類：**政府（一次文書）**。取得 2026-09-23
- 表の行（OCR のまま。注記記号 a が数字に付いている）：

> 1 March BRAVO Bikini; sandspit off Nam Island 15 MTa

- 本文：

> The first event of this series, designated BRAVO, had a yield of 15 MT and was the largest device ever detonated in atmospheric nuclear testing by the U.S. Government. Significantly exceeding its expected yield, BRAVO, detonated at Bikini Atoll, released large quantities of radioactive materials into the atmosphere, which were ‘caught up in winds that spread the particles over a much larger area than anticipated.

- 注："‘caught" の ‘ は原文どおり［ママ］。予測の数字は書いていない

### A1-7　NSArchive（学術＝解説は二次）— 「計画者の見積もり6メガトンのほぼ3倍」「予測は4〜8」「最大15もありうると理解していた」

- 出典：William Burr (ed.), "Castle BRAVO at 70: The Worst Nuclear Test in U.S. History," National Security Archive, Feb 29, 2024
  - https://nsarchive.gwu.edu/briefing-book/nuclear-vault/2024-02-29/castle-bravo-70-worst-nuclear-test-us-history
- 種類：**学術（大学の資料集）。解説文は二次**。取得 2026-09-23

> The Bravo detonation in the Castle test series had an explosive yield of 15 megatons—1,000 times that of the weapon that destroyed Hiroshima and nearly three times the six megatons that its planners estimated.

> Apparently, the designers at Los Alamos National Laboratory understood that the explosive yield could be far greater than the estimated six megatons, possibly as high as 15.

> A message from 2 March mentioned "heavy contamination" and a preliminary yield estimate of 15 megatons "plus or minus 5."

- 注：Wikipedia の「15 (± 5) Mt」はこの3月2日の速報値に当たる。**確定値ではない**

### A1-8　二次資料（手がかりのみ）— 「2.5倍」の言葉はここにしかない

- nuclearweaponarchive.org "Operation Castle"（Carey Sublette）https://nuclearweaponarchive.org/Usa/Tests/Castle.html — **二次**。取得 2026-09-23

> 6 Mt predicted, estimated yield range 4-8 Mt

> The yield of Bravo dramatically exceeded predictions, being about 2.5 times higher than the best guess and almost double the estimated maximum possible yield

- Wikipedia "Castle Bravo" https://en.wikipedia.org/wiki/Castle_Bravo — **二次**（出典は nuclearweaponarchive と Rhodes『Dark Sun』）。取得 2026-09-23

> Castle Bravo's yield was 15 megatons of TNT [Mt] (63 PJ), 2.5 times the predicted 6 Mt (25 PJ).

> The yield of 15 (± 5) Mt was triple that of the 5 Mt predicted by its designers.

- Brookings, Ariana Rowberry, "Castle Bravo: The Largest U.S. Nuclear Explosion," February 27, 2014 https://www.brookings.edu/articles/castle-bravo-the-largest-u-s-nuclear-explosion — **二次**。取得 2026-09-23

> They predicted that the yield of the device would be roughly five to six megatons

- **判定**：「2.5倍」は政府資料の文言にはない。**15（DOE/NV-209）と6（AEC 公式史の「最有力値」）から計算すれば 2.5**。Wikipedia は同じ記事の中で「6 Mt の2.5倍」と「5 Mt の3倍」が並んでいて、**記事内で食い違う**

### A1-9　参考：2024年の査読論文の要旨に出てくる「2倍」

- Bates & Chadwick（2024、下の A2-2）の要旨は、**世間でよく言われる話として**「予想の2倍」と書く（本人たちの見積もりではない）：

> It has been oft reported that the 1954 Castle Bravo nuclear test had a yield twice as large as expected because the nuclear explosive device designers had not properly accounted for the benefits from the 7Li isotope in the fuel; we note that this explanation is false.

### A1 のまとめ（数字の食い違い）

| 出典 | 種類 | 予測 | 実測 | 倍率の言い方 |
|---|---|---|---|---|
| GAC 議事録 1954年7月 | 政府（一次） | **4-8 MT** | 15 ± 0.5 MT | — |
| AEC 公式史 1989 | 政府（公式史） | **6 Mt（最有力）** | 15 Mt | almost three times |
| WT-934 1959（抜粋版 1981） | 政府（一次） | **5 Mt** | 約15 Mt | approximately three times |
| ストローズ声明 1954年3月31日 | 政府（一次・公式発表） | 数字なし | 数字なし（megaton range） | about double |
| DTRA 報告 2013 | 政府（DTRA） | 数字なし（「最有力値は最大値よりかなり小さい」） | 15 Mt | much larger than the best preshot estimates。最大値は15規模まで見積もり済み |
| DNA 説明資料 | 政府（一次） | 数字なし | 15 MT | Significantly exceeding its expected yield |
| NSArchive 2024 | 学術（解説は二次） | 6（幅は4〜8） | 15 | nearly three times |
| nuclearweaponarchive | 二次 | 6（幅4-8） | 15 | about 2.5 times／最大値のほぼ2倍 |
| Wikipedia | 二次 | 6 と 5 が混在 | 15 | 2.5 times／triple |
| Brookings 2014 | 二次 | 5〜6 | 15 | — |

---

## A2. 威力が大きかった物理的な理由（リチウム7）と、リチウム6の濃縮度

### A2-1　当時の説明（1954年7月、ロスアラモスのカーソン・マーク）— 一次資料

- 主張：Castle の各実験の威力はたいてい予測より大きかった。これはリチウム7の核反応で説明できると今はわかった。リチウム7は、以前は**リチウム6や液体重水素よりずっと劣る燃料**だと考えられていた
- 出典：A1-1 と同じ GAC 第41回議事録（議事録 p.-15-、PDF 19枚目。目次には "Li-7 as a Fuel" の見出しがある）
- 種類：**政府（一次文書）**。取得 2026-09-23
- 原文（OCR のまま）：

> Dr. Mark began by commenting on the fact that the yields of th~ ·~ . ~ Cast1e shots were substantially higher than predicted, in most cases. 11.-7 as a. 'E'uel . . This is now understood in terms of nuclea~ reactions of lithium-?, which had .formerly been assumed to be a much less good fuel than lithium-6 or liquid deuterium~

- 読み（整形＝当方）："Dr. Mark began by commenting on the fact that the yields of the Castle shots were substantially higher than predicted, in most cases. ［欄外見出し：Li-7 as a Fuel］ This is now understood in terms of nuclear reactions of lithium-7, which had formerly been assumed to be a much less good fuel than lithium-6 or liquid deuterium."
- 注：NSArchive の引用は "which had been assumed to be…" で、**原文の "formerly" が落ちている**。また一次資料の言い方は「**much less good fuel（ずっと劣る燃料）**」で、「**inert（反応しない）**」ではない

### A2-2　2024年の査読論文（LANL の研究者）— 「この説明は誤り」

- 主張：6Li（遅い中性子）と、6Li・7Li の両方（速い中性子）でトリチウムができる。そのうえで、「設計者が 7Li の効果を正しく見込まなかったから威力が2倍になった」という**よく言われる説明は誤り**
- 出典：C. R. Bates and M. B. Chadwick, "Lithium Neutron Cross Sections During the Manhattan Project and the Quest for the H-Bomb," *Fusion Science and Technology* 80 (sup1), S186–S191 (2024), published online 2024-07-23, doi:10.1080/15361055.2024.2370737（オープンアクセス CC BY-NC-ND。著者は2人とも LANL）
  - https://www.tandfonline.com/doi/full/10.1080/15361055.2024.2370737（**403 で本文は読めず**）
  - 要旨は Semantic Scholar の API で原文を取得：https://api.semanticscholar.org/graph/v1/paper/DOI:10.1080/15361055.2024.2370737?fields=title,abstract
- 種類：**学術（査読論文。国立研究所の著者）**。取得 2026-09-23
- 要旨（原文）：

> Abstract Neutron cross sections of the stable lithium isotopes 6Li and 7Li were of interest in the 1940s and 1950s in part because of their reactions, which form tritium using moderated neutrons on 6Li and higher-energy neutrons on either isotope. Lithium remains of interest today for use as a blanket and shielding material in fusion reactors, where it can be used to breed tritium for a self-sustaining fuel cycle. During the Manhattan Project, the resonance in the 6Li(n,t) reaction was discovered and later became important for enhancing tritium production for nuclear technologies. The dominant natural isotope 7Li was and remains of interest because of the expense of enriching 6Li. It has been oft reported that the 1954 Castle Bravo nuclear test had a yield twice as large as expected because the nuclear explosive device designers had not properly accounted for the benefits from the 7Li isotope in the fuel; we note that this explanation is false.

- ⚠️ **本文は未確認**。検索エンジンの要約（原文ではない）によれば、本文は「現代の LANL の計算では 7Li の反応は威力にあまり効いていない」「LLNL の Peter Rambo が現代のコードで独立に計算して同じ結果」「本当の原因は、事前計算の別の不備（たとえば物質の状態方程式）かもしれない」「本当の理由は完全にはわからないかもしれない」と述べているらしい。**原文で確かめていないので、台本の根拠にしない**
- 本文が引く LANL の報告 **LA-CP-24-10255**（C. R. Bates ほか、2024-03-28「Lithium-7 Cross Sections and the Puzzle of the Castle Bravo Prediction」）は、"LA-CP"＝**配布制限つきで公開されていない**（検索結果の要約による。未確認）
- 食い違い：A2-1 の1954年の説明（リチウム7の核反応で説明できる）と真っ向から対立する。**台本は「当時はこう説明された。ただし近年、ロスアラモス自身の研究者が異論を出している」の形にする**

### A2-3　AEC 公式史 — 「リチウム6が必要に見えた」「天然では7%」

- 出典：A1-2 と同じ Hewlett & Holl。種類：**政府（公式史）**。取得 2026-09-23
- p.162（PDF 189〜190枚目）：

> There was another approach to the thermonuclear weapon that could conceivably reduce the demand on reactor capacity for tritium production. This was the idea, first discussed at the Princeton conference in 1951, of placing lithium in the weapon itself and using fission neutrons to produce tritium in place. For this purpose, however, it appeared necessary to use the lighter isotope of lithium, which made up only 7 percent of the element in nature.

- p.163（PDF 190枚目）：

> Within a matter of weeks, however, this plan was overtaken by Los Alamos research, which suggested the possibility of a dry thermonuclear fuel using lithium deuteride.

### A2-4　NSArchive の解説（学術＝二次）— 「リチウム7は、設計者の想定と違って不活性ではなかった」

- 出典：A1-7 と同じ。種類：**学術（解説は二次）**。取得 2026-09-23

> To increase the explosive yield, the weapons designers included lithium deuteride in the fuel for Bravo, some of which was in the form of lithium-7.

> But the lithium-7 was not inert, as the designers had assumed.

- ⚠️ ページ上、この "inert" の語には **military-history.fandom.com（ファンのウィキ）へのリンク**が張られている。NSArchive のこの一文は**二次資料に寄りかかっている**

### A2-5　二次資料の物理の説明（手がかりのみ）

- Wikipedia "Castle Bravo"（二次。出典は Rhodes『Dark Sun』p.541 ほか）。取得 2026-09-23

> They considered only the lithium-6 isotope in the lithium deuteride secondary to be reactive; the lithium-7 isotope, accounting for 60% of the lithium content, was assumed to participate in reactions that were too slow to contribute to the yield.

> However, when lithium-7 is bombarded with energetic neutrons with an energy greater than 2.47 MeV, rather than simply absorbing a neutron, it undergoes nuclear fission into an alpha particle, a tritium nucleus, and another neutron.

- nuclearweaponarchive（二次）：

> When one of these high energy neutrons collided with a lithium-7 atom, it could fragement it into a tritium and a helium atom.

（"fragement" は原文どおり［ママ］）
- ⚠️ 当方の計算（出典ではない）：7Li(n,n′α)t の Q 値は約 −2.47 MeV。止まっている 7Li に中性子を当てるときの**しきい値は約2.8 MeV**（2.47 × 8/7）。Wikipedia の「2.47 MeV より大きい」は Q 値としきい値を混同している可能性がある。**台本で MeV の数字を出さない**

### A2-6　ブラボーの燃料のリチウム6濃縮度（約40%）— **二次のみ**

- 政府・国立研究所・査読論文で、ブラボーの濃縮度を書いたものは**見つからなかった**（GAC 議事録の兵器ごとの「Li6 enrichment」の表は黒塗り）
- Wikipedia（二次。出典は Hansen『Swords of Armageddon』Vol. III, p.208）：

> The enriched lithium used in Bravo was nominally 40% lithium-6 (the remainder was the much more common lithium-7, which was incorrectly assumed to be inert).

> The fuel slugs varied in enrichment from 37 to 40% in 6Li, and the slugs with lower enrichment were positioned at the end of the fusion-fuel chamber, away from the primary.

- nuclearweaponarchive（二次）：

> The fuel consisted of 37-40% enriched lithium-6 deuteride encased in a natural uranium tamper.

- Brookings 2014（二次）：

> The miscalculation occurred because scientists did not realize that the 'dry' source of fusion fuel, lithium deuteride with 40 percent content of lithium-6 isotope, would contribute so greatly to the overall yield

---

## A3. 装置（シュリンプ／TX-21／LANL／乾式／重さ／運搬できたか）と、アイビー・マイク

### A3-1　装置名「Shrimp（シュリンプ）」— 学術・二次のみ

- 政府文書の本文では確認できなかった（DOE/NV-209・DNA 説明資料・AEC 公式史・DTRA 報告・LANL Meade・GAC 議事録の抽出文字に "Shrimp" はない。DTRA 報告は全文検索で0件）
- NSArchive（学術）。取得 2026-09-23：

> Seventy years ago, on 1 March 1954 (28 February in Washington), the U.S. government detonated a thermonuclear weapon, code-named "Shrimp," on Bikini Atoll in the Marshall Islands in what turned out to be the largest nuclear test in U.S. history.

- 同ページの写真説明（写真は LANL 所蔵）：

> The 'Shrimp' test device is shown loaded on a flatbed truck, 20 February 1954 (Photo from Los Alamos National Laboratory collections; courtesy of Alex Wellerstein)

- AEC 公式史の図版一覧は "Castle-Bravo Device—Inside the shot house / February 1954 / DOE Archives B-83485" で、**愛称は書いていない**

### A3-2　TX-21 — 二次のみ

- Wikipedia（二次。出典は Hansen）：

> Castle Bravo was the first test by the United States of a practical deliverable fusion bomb, even though the TX-21 as proof-tested in the Bravo event was not weaponized.

- 参考：GAC 議事録（1954年7月。政府・一次）には **TX-21 という開発中の兵器**が出てくる。PDF 8枚目（p.-3- と p.-4- の間の頁。頁番号は読み取れない）。Henderson 氏による熱核兵器計画の説明の一部（議事録の目次ではこの部分は「Sandia Briefings」の中）：

> The 17,400 lb TX-21 is in its infancy. Mr. Henderson said that a lightened version might eventually take the place of the TX-15 in filling the class C requirement. The TX-21 appears to be compatible with the B-58 aircraft (Hustler) •

　「熱核兵器の現状」の表にも "21-0"（クラス B）がある（議事録 p.-12-、PDF 16枚目）。ただし**この TX-21 とブラボーの試験装置（シュリンプ）を結びつける記述は、抽出した文字の中にない**（"Shrimp" の語も0件）。17,400 lb（約7.9 t）は1954年7月時点の兵器としての TX-21 の重さで、**二次資料が書くシュリンプの 23,500 lb とは別物として扱う**。台本では TX-21 を使わない

### A3-3　設計した研究所 — ロスアラモス

- DOE/NV-209 Rev 16（A4）の Sponsor 欄：**LANL**
- LANL Meade「Operation Castle」の表：

> Bravo 02/28/1954 LASL Bikini Surface 15

（LASL＝当時の名称 Los Alamos Scientific Laboratory）
- 出典：R. A. Meade, "Operation Castle," LA-UR-21-29474 (Los Alamos National Laboratory, issued 2021-09-27) https://www.osti.gov/biblio/1822703 — **国立研究所**。取得 2026-09-23

### A3-4　燃料の形 — 固体の重水素化リチウム＝「乾式」、マイクは液体重水素＝「湿式」

- AEC 公式史（政府・公式史）。取得 2026-09-23
- p.172：

> On February 22, 1954, the scientific task group under Ogle's direction completed the installation of the Bravo test device. Because it was to be the first shot in the series, the device had not been placed on a barge but in a small structure on a reef off Namu Island at the northwestern perimeter of the atoll. As the first test of a dry thermonuclear system, Bravo had special significance.

- pp.165–166：

> And beyond that point, there was still no positive assurance that a dry weapon would work. If the first test in the series, which was to be a weapon using lithium deuteride, should fail, the test schedule would have to be revised, and the possibility would increase that Los Alamos would have to fall back for emergency capability on such unpromising systems as the weapon version of Mike with its great bulk and cumbersome cryogenic gear.

- p.178：

> In addition to demonstrating the feasibility of a dry thermonuclear weapon, Bravo opened the way to other design improvements, of which the surprisingly high yield was only one indication.

- p.179：

> The feasibility of the dry thermonuclear weapon had been demonstrated so decisively that the Commission with confidence could cancel its contracts for cryogenics research for the wet device.

- LANL Meade「Operation Castle」（国立研究所）：

> As the Los Alamos program proceeded to develop cryogenic devices, research suggested an alternative - a cheaper, more efficient dry fuel. Harold Agnew and Hans Bethe proposed shifting the focus of Los Alamos research to such designs in 1953.

> Agnew quickly sent a cleverly written message back to Los Alamos saying, “Why buy a cow when powdered milk is so cheap?” His message was clear: Bravo marked the end of cryogenic thermonuclear designs, including the cancellation of the planned second Castle test.

- nuclearweaponarchive（二次）：

> This was the first "dry" or solid fuel (lithium deuteride fueled) H-Bomb tested by the U.S.

### A3-5　シュリンプの重さ・寸法 — **二次のみ**

- 政府・国立研究所の資料では見つからなかった
- nuclearweaponarchive（二次）：

> Its weight was a comparatively light 23,500 lb, and it was 179.5 in long and 53.9 in wide.

（換算：約10.7 t、長さ約4.56 m、直径約1.37 m）
- Wikipedia（二次。出典は nuclearweaponarchive）：

> The Castle Bravo device was housed in a cylinder that weighed 23,500 pounds (10,700 kg) and measured 179.5 inches (456 cm) in length and 53.9 inches (137 cm) in diameter.

### A3-6　「飛行機で運べる（投下できる）初の水爆」か — 言い方に注意

- AEC 公式史 p.155（Castle の目的）：

> Design work had just been completed at Los Alamos on some new principles that would be used in the Castle series in the Pacific early in 1954 to develop a deliverable thermonuclear weapon.

- DTRA 報告 印刷 p.29（IA leaf 39）：

> The successful test of the IVY MIKE device confirmed the scientific feasibility of superweapons. Weighing 80,000 lb, requiring cryogenic cooling, and occupying a three-story building, the MIKE device was not, however, a practicable weapon (Figure 1-10).

> The Emergency Capability Program was established with the mission and presidential charter to produce a deliverable superweapon at the earliest possible date. Operation CASTLE, already envisioned as a Pacific test series in which experimental very-high-yield devices would be evaluated, was redirected toward establishing whether any of the notional designs could be made into an actual weapon and rushed into production.

- LANL Meade「Operation Castle」：

> Each, with the exception of Koon, performed better than predicted, providing the United States with stable, deliverable thermonuclear weapons, albeit ones still very large and cumbersome.

> Very soon, however, a number of issues coalesced, fundamentally changing Castle beginning with the realization that Mike, although not yet tested, could not be a weapon of war. It was too big.

> In addition to being too big, Mike had a second major problem, its cryogenic design made stockpiling nearly impossible.

- **ブラボーは投下されていない**：DOE/NV-209 の Type は "Surface"（A4）。米国初のメガトン級の空中投下は1956年（DTRA 報告 印刷 p.84／IA leaf 95 の脚注26）：

> The first airdrop of a megaton-yield weapon was conducted in 1956 as the CHEROKEE test of Operation REDWING. The bomb fell about 4 mi distant from the intended explosion point, and nearly all device diagnostic information was lost.

- 二次（Wikipedia、A3-2 の引用）は「practical deliverable fusion bomb の最初の試験。ただし試験したものは兵器化されていない」とする
- **推奨**：「飛行機で運べる兵器を目指した、乾式の水爆の最初の実験」。「初めて投下された水爆」「初の実用水爆」とは言わない

### A3-7　アイビー・マイクの日時

- DOE/NV-209 Rev 16（政府・一次。A4 と同じ文書、印刷 pp.4–5）の行：

> 31 Mike
> Experimental thermonuclear device 10/31/1952 LANL Enewetak Atoll - - - - Surface

> 19:15:00.00 11.667000 162.189900 10 7 Weapons Related 10.4 Mt 31

（GMT。現地（GMT＋12）では **1952年11月1日 07:15**）
- DNA 6036F *Operation IVY: 1952*（Defense Nuclear Agency, 1982）https://www.govinfo.gov/content/pkg/GOVPUB-D15-PURL-gpo222810/pdf/GOVPUB-D15-PURL-gpo222810.pdf — **政府（一次）**。取得 2026-09-23
  - 説明資料 p.1（表。見出しは Assigned Name / Local Date / Location / Yield。OCR のまま）：

> MIKE 1 Nov Eluklab Island; surface 10.4 MT

  - 印刷 p.187（PDF 193枚目）：

> MIKE was detonated on Eluklab Island at 0714.59.4 on 1 November, approximately 0.6 second early because of a power failure aboard Estes where the firing party was stationed. The 10.4-MT blast produced a tremendous fireball followed by a gigantic mushroom cloud.

- DTRA 報告 印刷 p.28（IA leaf 38）：

> The IVY MIKE test was conducted on 1 November 1952. The device functioned about as envisioned, producing a yield of 10.4 Mt. The explosion partially vaporized Elugelab Island and left a mile- wide crater in the reef.

- ⚠️ LANL Meade「Operation Ivy」（LA-UR-21-29142, https://www.osti.gov/biblio/1821343）の表は "Mike 1/11/1952 Elugelab Surface 10.4" "King 1/16/1952 Runit 1,480 0.5" と**日付の書式が崩れている**（King は11月16日のはず）。使わない

### A3-8　アイビー・マイクの威力（10.4 Mt）と「最初の熱核爆発」

- DOE/NV-209・DNA 6036F・DTRA 報告（上）がそろって **10.4 Mt**
- DNA 6036F 説明資料 p.1：

> MIKE was an experimental device and produced the first thermonuclear detonation, in which a substantial portion of its energy was generated by tLe fusion, or joining, of hydrogen atoms.

（"tLe" は OCR のまま［ママ］＝the）
- 事前の見込み（DTRA 報告 印刷 p.27／IA leaf 37）：

> Should it function as envisioned, the yield would be 10,000 kt, or 10 Mt, with an outside possibility of 50 Mt.

- 査読論文の要旨も 10.4 Mt（J. Morgan, "The Untold Story of Building the First Megaton Thermonuclear Fusion Device: The Simple Element and IVY Mike," *Fusion Science and Technology* 82, 487–550 (2025), doi:10.1080/15361055.2025.2503035。要旨は Semantic Scholar API で取得）— **学術**：

> This report is a research and development engineer’s perspective on the fascinating story of the world’s first megaton-class thermonuclear device, IVY Mike (10.4 Mt).

### A3-9　アイビー・マイクの重さ — **出典で割れる**

- DTRA 報告（政府）：「**Weighing 80,000 lb**」（A3-6 の引用。約36 t＝40 short tons）
- 「**82トン**」は**二次のみ**で確認：
  - Britannica "Mike | thermonuclear device"（二次。検索結果の抜粋。本文は未取得）："weighed 82 tons, in part because of cryogenic (low-temperature) refrigeration equipment necessary to keep the deuterium in liquid form"
  - Wikipedia "Ivy Mike"（二次。出典は K. M. Parsons & R. A. Zaballa, *Bombing the Marshall Islands*, Cambridge University Press, 2017＝学術書）：

> The entire 'Mike' device (including cryogenic equipment) weighed 82 short tons (74 metric tons)

- 2021年版 DTRA ファクトシート（IVY）に「82 tons」があるという検索結果の要約を見たが、**dtra.mil が 403 で原文を確認できなかった**
- **推奨**：重さの数字を言わず、DTRA 報告の「**occupying a three-story building**（3階建ての建物ほど）」「**requiring cryogenic cooling**（極低温の冷却が必要）」で描く

---

## A4. 公式の実験一覧 DOE/NV-209 のブラボーの行

- 出典：*United States Nuclear Tests, July 1945 through September 1992*, DOE/NV--209-REV 16, September 2015, U.S. Department of Energy, National Nuclear Security Administration Nevada Field Office
  - https://www.osti.gov/servlets/purl/1351809 （OSTI レコード https://www.osti.gov/biblio/1351809）
  - 同じ文書：https://nnss.gov/wp-content/uploads/2023/08/DOE_NV-209_Rev16.pdf
- 種類：**政府（一次文書）**。取得 2026-09-23

### A4-1　ブラボーの行（「U.S. Nuclear Tests – By Date」印刷 pp.4–5。左右2ページにまたがる表）

- 左ページ（列：Test / Date (mm/dd/yyyy) (GMT) / Sponsor / Location / Hole / Type）：

> 44
> Bravo
> Experimental thermonuclear device
> Highest-yield U.S. nuclear test
> 02/28/1954 LANL Bikini Atoll - - - - Surface

- 右ページ（列：Time (GMT) / Latitude (degrees) / Longitude (degrees) / Surface Elevation (ft) / Height of Burst or Depth of Burial (ft) / Purpose / Yield Range / Test）：

> 18:45:00.00 11.697130 165.274200 10 7 Weapons Related 15 Mt 44

- 読み：通し番号44、ブラボー、「実験用の熱核装置」「米国の核実験で最大の威力」、**1954年2月28日（GMT）**、LANL、ビキニ環礁、Hole 欄は空、**Type＝Surface（地表）**、**18:45:00.00 GMT**、北緯11.697130度・東経165.274200度、地表の標高10フィート、爆発の高さ7フィート（約2 m）、目的＝Weapons Related（兵器関連）、**威力15 Mt**
- 名前順の一覧（「U.S. Nuclear Detonations – By Name」印刷 pp.122–123）にも同じ行：

> 44 Bravo 02/28/1954 LANL Bikini Atoll - - - - Surface

> 18:45:00.00 11.697130 165.274200 10 7 Weapons Related 15 Mt 44

### A4-2　日時の約束ごと（同文書 p.viii と p.xii）

> Detonation time and date for all detonations listed in this document were converted from local time to Greenwich Mean Time (GMT). The date listed is the GMT date for the detonation. Times are given in the hundredth of a second where available; otherwise, a default value of 0.00 seconds is used.

> One last hint to aid in research: Although the tests are listed by GMT, using local time will often assist in identifying details in associated photographs.

- 現地時刻への換算：DTRA 報告（印刷 p.73／IA leaf 84 の脚注2）が「マーシャル諸島の現地時刻はグリニッジより12時間進み」と明記：

> Date and time are indicated in the form “dd-hh:mm.” A following M indicates local time in the Marshall Islands, which is 12 hours ahead of Greenwich or “Zulu” time. The BRAVO detonation occurred at March 01-06:45M, that is, at 6:45 a.m. local time in the Marshall Islands on 1 March 1954.

- ＝**現地 1954年3月1日 午前6時45分**。日本時間（GMT＋9）なら **3月1日 午前3時45分**（当方の換算）
- 日付のずれの話（DTRA 報告 印刷 p.75／IA leaf 86）：

> (This directive was “bent” somewhat when BRAVO was shot on 28 February, local time in Washington, D.C.)

### A4-3　食い違い（使わない値）

- AEC 公式史 p.172：

> Once the final equipment checks were completed, the long countdown began to H-hour, at 6:54 a.m., local time, on March 1.

　→ **6:54 は DOE/NV-209（18:45 GMT＝6:45 現地）・DTRA 報告（6:45 a.m.）と食い違う**。誤植とみて使わない（OCR の2文字入れ替わりの可能性は低い）
- LANL Meade「Operation Castle」本文と脚注：

> On February 28, 1954, Bravo, the first of six thermonuclear devices tested during Operation Castle, burst into the sky over Bikini Atoll.1

> 1 March 1st, in the United States.

　→ **脚注が逆**（米国では2月28日、現地が3月1日）。使わない
- 場所の表現：DNA 説明資料「Bikini; sandspit off Nam Island」、AEC 公式史「a small structure on a reef off Namu Island」、LLNL「ground-surface test」（A5-4）。DOE/NV-209 は「Bikini Atoll」「Surface」だけ

---

## A5. 火の玉・雲・クレーターの大きさ（DNA 6035F 以外）

### A5-1　DTRA 報告（2013）— 火の玉・雲

- 出典：A1-5 と同じ。**政府（DTRA）**。取得 2026-09-23
- 印刷 p.52（IA leaf 63）：

> As the BRAVO device detonated, a huge fireball formed (Figure 3-1). Composed of what had been the bomb itself and the surrounding equipment, coral, seawater, and air, the fireball grew within seconds to be more than 3 mi across. For a moment it seemed to cling to the earth, but then it sprung into the sky (Figure 3-2). Ten million tons of pulverized coral debris were coated with radioactive fission products and sucked up into the rising fireball. Surrounded by moisture condensation rings caused by the passage of the shock wave, the huge bubble of superheated gas and debris rose 45,000 ft in its first minute, leaving behind a 4 mi wide stem of radioactive debris (Figure 3-3). It continued to rocket upward, punching through the tropopause and into the stratosphere. Coasting upward through the stratosphere, the cloud was squashed by dynamic pressure. After 5 minutes, the rising cloud finally came to a stop at an altitude of over 115,000 ft. An immense trumpet- shaped cloud formed. Ten minutes after the explosion, the head of the mushroom cloud had widened into an anvil resting upon the tropopause, measuring 75 mi across and growing rapidly (Figure 3-4). And from the base of the immense anvil cloud, looking like virga from a desert shower, was debris falling toward the earth below (Clarkson and Graves 1954, 29).

- 換算（当方）：3 mi＝約4.8 km／45,000 ft＝約13.7 km／4 mi＝約6.4 km／115,000 ft＝約35.1 km／75 mi＝約121 km
- 参考（印刷 p.50／IA leaf 61。設計どおりの威力なら雲は約3万m）：

> ...it was expected that if CASTLE BRAVO were to achieve its design yield, the resulting mushroom cloud would rise to a height of almost 100,000 ft.

### A5-2　LANL Meade（2021）— 雲

- 出典：A3-3 と同じ LA-UR-21-29474。**国立研究所**。取得 2026-09-23

> Five minutes after detonation, Bravo’s mushroom cloud punched through the stratosphere topping out at 115,000 feet. At ten minutes, the cloud was more than seventy-five miles wide and still expanding.

### A5-3　クレーター

- DTRA 報告 印刷 p.35（IA leaf 46。図1-17の説明）：

> The mile-wide crater produced by the detonation is the prominent hole in the Bikini Atoll reef at the top left.

- WT-934（EX）印刷 p.65（PDF 64枚目）— 深さ。原文（OCR のまま）：

> It io pertinent that the fathometer survey-of the Shot 1 crater showed a uniform flat bottom at a depth of 170 feet; however, this flat bottom un- doubtedly represented the upper surfaoe 18yer of mud and suspended eand which was set- tling in +he crater. By contra&, lead-line sounding6 taken at approximately the same

> time recorded a depth of 240 feet, which is considered to be the Shot 1 depth of crater.

- 読み（整形＝当方）："It is pertinent that the fathometer survey of the Shot 1 crater showed a uniform flat bottom at a depth of 170 feet; however, this flat bottom undoubtedly represented the upper surface layer of mud and suspended sand which was settling in the crater. By contrast, lead-line soundings taken at approximately the same time recorded a depth of 240 feet, which is considered to be the Shot 1 depth of crater."（240 ft＝約73 m）
- 同ページの表 4.1 には直径らしい数字もあるが、**OCR が崩れていて読めない**ので使わない

### A5-4　LLNL（国立研究所）— 地表実験・15 Mt

- 出典：The Marshall Islands Program (LLNL), "Bikini Atoll" https://marshallislands.llnl.gov/affected-areas/bikini-atoll — **国立研究所**。取得 2026-09-23

> This ground-surface test was code named Bravo and had an estimated explosive yield of 15 Mt.

### A5-5　食い違い（二次資料の数字）

| 項目 | 政府・国立研究所 | 二次資料 |
|---|---|---|
| 火の玉 | 数秒で「more than 3 mi」（約4.8 km 超）＝DTRA | Wikipedia「within one second it formed a fireball almost 4.5 miles (7.2 km) across」（**脚注なし**） |
| 雲の高さ | 5分で「over 115,000 ft」（約35 km 超）＝DTRA・LANL | Wikipedia「a height of 130,000 feet (40 km) and 62 mi (100 km) in diameter in less than 10 minutes」（**脚注なし**） |
| 1分後の雲 | 45,000 ft（約13.7 km）＝DTRA | Wikipedia「47,000 feet (14,000 m) and a diameter of 7 miles (11 km) in about a minute」 |
| クレーターの幅 | 「mile-wide」（約1.6 km）＝DTRA | nuclearweaponarchive「a diameter of 6510 ft」（約1.98 km）、Wikipedia「6,500 feet (2,000 m)」 |
| クレーターの深さ | 240 ft（約73 m。測深）＝WT-934 | nuclearweaponarchive・Wikipedia「250 ft」（約76 m） |

---

## A6. 誰が、なぜ「リチウム7は（ほとんど）効かない」と考えたのか

### A6-1　一次資料で言えること

- **誰が**：一次資料（GAC 議事録）は受け身で "had formerly been assumed"（以前はそう考えられていた）と書くだけで、**主語を名指ししていない**。話しているのはロスアラモスのカーソン・マーク（A2-1）。ブラボーの「最有力値」と「最大値」を現地に伝えた1954年2月18日の電報 JF-2130 の差出人は **Darrol Froman と Carson Mark（LASL）**（A1-5）
- **何と考えたか**：「**リチウム6や液体重水素よりずっと劣る燃料**」（A2-1）。「まったく反応しない（inert）」ではない
- **なぜ**：一次資料には**理由が書かれていない**。AEC 公式史は、兵器の中でトリチウムを作るには「**リチウム6を使う必要があるように見えた**」と書く（A2-3, p.162）

### A6-2　反応断面積（中性子との反応のしやすさ）の理解については

- Bates & Chadwick 2024（査読論文・LANL）の要旨は、**7Li も速い中性子でトリチウムを作る**ことが1940〜50年代の関心事だったと書き（A2-2）、そのうえで「**7Li を見込まなかったから威力が2倍になった**」という通説を**誤り**とする
- 「1950年代初めの 7Li の中性子反応の計算上の扱いは粗かった。しかしそれが2倍の過小評価につながったわけではない」「原因は状態方程式など別の不備かもしれない」という趣旨の記述は、**検索エンジンの要約でしか見ていない（原文未確認）**
- 二次資料（Wikipedia が引く Rhodes『Dark Sun』p.541）は「リチウム7は、威力に効くには遅すぎる反応しかしないと考えられた」とする（A2-5）

### A6-3　結論

- 「**当時ロスアラモスは、リチウム7が燃料としてずっと劣ると考えていた。実験後、リチウム7の核反応で威力の大きさを説明した**」までは一次資料で言える
- 「**なぜそう考えたか**」「**本当にリチウム7が原因だったか**」は、**権威ある資料で決着していない**。2024年の LANL 研究者の論文は通説を否定している。台本で「リチウム7が原因だった」と**断定しない**

---

## A7. DTRA は DNA の後身か（c111・c320「国防総省の機関」／④'の申し送り）

**一次資料**＝DTRA 公式の沿革 https://www.dtra.mil/About/DTRA-History/ （2026-09-23 ⑤b で読んだ。WebFetch・curl は UA を付けても 403 → アプリ内ブラウザで本文を取得）

- 「With the rapid military build-up and strategic modernization, the Defense Nuclear Agency (DNA) was established as the successor of DASA in 1971 …」
- 「June 1996 - DNA was renamed Defense Special Weapons Agency (DSWA) as the mission scope expanded to include non-nuclear development activities.」
- 「OCTOBER 1998 - The Defense Threat Reduction Agency (DTRA) was established, joining DSWA, OSIA, CTR and the Chemical Biological Defense Program.」
- 同じ頁：AFSWP は「re-designated as the Defense Atomic Support Agency (DASA) in 1959」

**結論**：AFSWP → DASA（1959）→ DNA（1971）→ DSWA（1996・改名）→ DTRA（1998・DSWA ほかを合わせて発足）。
**「DTRA は DNA の後身」は正しい。** 12本目の3冊（DASA 1251・DNA 6035F・DTRA 2013）は**同じ系譜の機関**が出したもの。
台本 c111「国防総省の機関が1982年と2013年にまとめた2冊」・c320「2013年に国防総省の機関がまとめた報告書」は、このままでよい（「別の機関」と言わないのが正しい）。

---

## 付記

### A. 見つけられなかった・確認できなかったもの

- 電報 JF-2130（1954年2月18日、Froman と Mark から Graves へ）の本文。最有力値と最大値の数字は、DTRA 報告には書かれていない
- Bates & Chadwick 2024 の本文（tandfonline が 403）。LA-CP-24-10255 は非公開の可能性
- 2021年版 DTRA ファクトシート（CASTLE・IVY）。dtra.mil が 403
- シュリンプの重さ・寸法、リチウム6濃縮度を書いた政府・国立研究所の資料。「シュリンプ＝TX-21」と結びつける政府・国立研究所の資料（TX-21 という兵器の存在は GAC 議事録にある）
- マイクの「82トン」を書いた政府資料

### B. このファイルの引用で使った一次資料の所在（まとめ）

| 資料 | URL |
|---|---|
| GAC 第41回議事録（1954年7月） | https://nsarchive.gwu.edu/sites/default/files/documents/s9j6zr-s789b/35.pdf |
| AEC 公式史 Hewlett & Holl | https://www.osti.gov/servlets/purl/774455 |
| WT-934 (EX) | https://www.osti.gov/opennet/servlets/purl/16039007-L0uAxS/16039007.pdf |
| 1954年3月31日 記者会見速記 | https://nsarchive.gwu.edu/sites/default/files/documents/s9j6px-77xgg/16.pdf |
| DTRA 報告 SR-12-001（全文） | https://archive.org/details/DTIC_ADA572278 |
| DNA 説明資料 CASTLE | https://www.osti.gov/opennet/servlets/purl/16367220-1TWi06/16367220.pdf |
| DOE/NV-209 Rev 16 | https://www.osti.gov/servlets/purl/1351809 |
| DNA 6036F（IVY） | https://www.govinfo.gov/content/pkg/GOVPUB-D15-PURL-gpo222810/pdf/GOVPUB-D15-PURL-gpo222810.pdf |
| LANL Meade「Operation Castle」 | https://www.osti.gov/biblio/1822703 |
| LANL Meade「Operation Ivy」 | https://www.osti.gov/biblio/1821343 |
| FRUS 1952–54 Vol. II Pt. 2, Doc. 185（ダレス国務長官とストローズの電話、1954年3月29日。「Nothing was out of control.」） | https://history.state.gov/historicaldocuments/frus1952-54v02p2/d185 |

### C. ツールが自動で保存したファイル（当方は保存を指示していない）

WebFetch が PDF を読めなかったときに、ツールが次のフォルダへ自動で保存した。文字の抽出にだけ使った。消すかどうかはカズヤくんの判断（Claude は完全削除しない決まり）。

`C:\Users\konar\.claude\projects\C--Users-konar-Documents-Obsidian-Vault\144bef86-c5ee-43ee-ad2d-4ee4b05d56dd\tool-results\`

| ファイル | 中身 | 大きさ |
|---|---|---|
| webfetch-1790114857412-8h0vcj.pdf | DTRA 報告 SR-12-001（nuclearsecrecy のコピー。未使用） | 8.6 MB |
| webfetch-1790115294690-mml5hi.pdf | GAC 第41回議事録 | 2.8 MB |
| webfetch-1790115597355-kc1ij6.pdf | LANL Meade「Operation Castle」 | 2.1 MB |
| webfetch-1790115627491-mo9tza.pdf | LANL Meade「Operation Ivy」 | 0.2 MB |
| webfetch-1790115631141-byypyj.pdf | LANL Meade「Nuclear Weapons and the Atmospheric Test Era」（ブラボーの数字なし） | 0.3 MB |
| webfetch-1790115671460-zknggq.pdf | DNA 説明資料 CASTLE | 0.2 MB |
| webfetch-1790115701408-3v8du1.pdf | DOE/NV-209 Rev 16 | 2.0 MB |
| webfetch-1790115828723-58hhx4.pdf | AEC 公式史 Hewlett & Holl | 9.4 MB |
| webfetch-1790115983455-a4m69f.pdf | 1954年3月31日 記者会見速記 | 0.9 MB |
| webfetch-1790116429124-qe2gf1.pdf | DNA 6036F（IVY） | 5.9 MB |
| webfetch-1790116498514-0wxpde.pdf | OpenNet 16367228（IVY と思ったが WIGWAM の説明資料。未使用） | 0.2 MB |
| webfetch-1790116566754-g7uf1l.pdf | WT-934 (EX) | 9.9 MB |
| bql60kww4.txt／bqyezqd6p.txt | 当方の抽出結果が長すぎてツールが退避したテキスト | 0.1 MB 以下 |

同じフォルダにあるほかのファイル（rv2r4k・bwjjw5・5q97cg など）は、このファイルの作業で作られたものではない。
