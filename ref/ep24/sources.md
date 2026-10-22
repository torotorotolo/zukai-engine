
# 24本目（チェルノブイリ原発事故・1986-04-26・ソ連〈いまのウクライナ〉4号炉 RBMK-1000）一次資料の台帳と骨の照合

**2026-10-22（24本目の2本目のチャット＝②③）で作った。** ①の詳細＝[legend_2026-10-22.md](legend_2026-10-22.md)（通説の判定・数の割れ）。このファイルは①を**引き写さず**、取り直した原本で自分で当てた結果（道具＝`probe/verify24.py`・`verify24b.py`・`rows.py`・`grep24.py`／出力＝`src/probe_out/verify_run1〜5.txt`・`kokkai_check1〜2.txt`・`rows_run1.txt`＝**git の外**＝報告書の文の抜き出しが長いため公開のリポに入れない）。
素材＝[materials.md](materials.md)／尺の骨＝[kousei.md](kousei.md)

- 凡例：**S**＝1986〜1992年の当局・IAEA の一次資料／**L**＝後年の公的な報告（国連・IAEA・WHO・IARC）／**K**＝国会会議録／**U**＝米国の政府機関（PD）／**R**＝権利の資料
- 頁＝「PDF頁／印刷頁」。ずれは**頁の数字を見て**確かめた（INSAG-7＝PDF−10・ソ連報告＝PDF−4・UNSCEAR 2000 Annex J＝PDF＋448・2008 Annex D＝PDF＋40・フォーラム＝PDF＋2＝どれも①と一致）。⚠️ GC(SPL.I)/3 は途中でずれが変わる（PDF 6→印刷1・PDF 112→105）＝頁頭の「- N -」で読む（`~105` の形で書く）
- 時刻は**モスクワ時間**（現地）。英文の引用は15語以内。文字は NFKC＋空白を潰して照合（`probe/extract.py`）
- ⚠️ 「0件」は「この綴りでは出ない」であって「無い」ではない（OCR の崩れ・改行のハイフン）

---

## 1. 資料（1件1行）

保存先＝`ref/ep24/src/`（**git の管理外**・112MB）。取得の http・大きさ・md5＝`src/fetch_log.tsv`（10-22 08:48・14件すべて http 200）。①の PDF は別セッションの scratchpad にあって消えていた＝**md5 を照らす相手は無い**（今回の値を正本にする）。

| 記号 | 資料 | URL | 保存先（md5 の頭8字） | 権利・使い方 |
|---|---|---|---|---|
| **S1** | **INSAG-7**『The Chernobyl Accident: Updating of INSAG-1』（Safety Series No.75-INSAG-7・IAEA 1992・148 PDF頁）。**付属書I**＝ソ連の産業・原子力安全監督国家委員会（SCSSINP）の委員会の報告（委員長 N.A. シテインベルグ〈原文 Shteynberg〉・1991）／**付属書II**＝ソ連専門家作業部会（委員長 A.A. アバギャン） | https://www-pub.iaea.org/MTCD/Publications/PDF/Pub913e_web.pdf | `insag7_pub913e.pdf`（a38523c5） | © IAEA 1992（転載・翻訳は IAEA に申請）＝**頁の引用**（額装・出典つき・最小限）。文字の層は良好。⚠️ 表は列が崩れる＝`probe/rows.py`（語の座標から行を組み直す）＝`src/insag7_tableI-I_rows.txt`・`insag7_tableII-III_rows.txt` |
| **S2** | IAEA 総会文書 **GC(SPL.I)/3**（1986-09-24）＝INSAG『Summary Report on the Post-Accident Review Meeting on the Chernobyl Accident』（＝**INSAG-1 と同じ本文**・147 PDF頁） | https://www.iaea.org/sites/default/files/gc/gc-spl1-3.pdf | `gc_spl1_3_insag1text.pdf`（9465dcd3） | © IAEA＝頁の引用。スキャン＋OCR（誤字・表の列崩れ）＝**決め所は頁の画像で** |
| **S3** | ソ連国家原子力利用委員会『The Accident at the Chernobyl' Nuclear Power Plant and Its Consequences』**Part I**（IAEA 専門家会議 1986-08-25〜29 向け・「DRAFT August 1986」・60 PDF頁）。p.5／1 に作成した専門家団24人の名簿（アルファベット順・**Legasov V.A. を含む**＝団長とは書かれていない） | https://www.iaea.org/sites/default/files/gc/gc29inf-232-corr1_en.pdf | `ussr_report_part1.pdf`（06a65077） | ソ連の公文書の英訳（IAEA 配布）＝頁の引用。⚠️ 権利の根拠（公文書か）は**未確認** |
| **L1** | チェルノブイリ・フォーラム『Chernobyl's Legacy: Health, Environmental and Socio-Economic Impacts』第2改訂版（IAEA 2006・55 PDF頁） | https://www.iaea.org/sites/default/files/chernobyl.pdf | `forum_legacy_2006.pdf`（a912e744） | © IAEA＝引用。⚠️ 一部の行は文字の層が化けている（p.8／10 ほか） |
| **L2** | UNSCEAR 2000 Report Vol.II **Annex J**『Exposures and effects of the Chernobyl accident』（117 PDF頁） | https://www.unscear.org/unscear/uploads/documents/publications/UNSCEAR_2000_Annex-J.pdf | `unscear2000_annexJ.pdf`（cf4f0d04） | © 国連＝引用 |
| **L3** | UNSCEAR 2008 Report Vol.II **Annex D**『Health effects due to radiation from the Chernobyl accident』（訂正版・179 PDF頁） | https://www.unscear.org/unscear/uploads/documents/publications/UNSCEAR_2008_Annex-D-CORR.pdf | `unscear2008_annexD_corr.pdf`（2b754c58） | 同上。⚠️ 表 D7（p.149／189）は個人の頭文字＝画面に使わない |
| L4 | UNSCEAR 白書『Evaluation of data on thyroid cancer in regions affected by the Chernobyl accident』（2018-04 公表・30 PDF頁） | https://www.unscear.org/unscear/uploads/documents/publications/Chernobyl_WP_2017.pdf | `unscear_wp2018_thyroid.pdf`（032773d5） | 同上 |
| L5〜L7 | UNSCEAR 1988 Report 本文／Annex D／**Annex G**（付録＝チェルノブイリの急性障害） | https://www.unscear.org/unscear/uploads/documents/unscear-reports/UNSCEAR_1988_Report.pdf ・ …/publications/UNSCEAR_1988_Annex-D.pdf ・ …/publications/UNSCEAR_1988_Annex-G.pdf | `unscear1988_report.pdf`（4ee4de17）・`_annexD.pdf`（441a7fe2）・`_annexG.pdf`（3cf8ce7a） | 同上（OCR・印刷頁は未対応） |
| L8 | IARC『The Cancer Burden from Chernobyl in Europe』（briefing・2006） | https://www.iarc.who.int/wp-content/uploads/2018/07/IARCBriefingChernobyl.pdf | `iarc2006_briefing.pdf`（b3bfc2c4） | 引用 |
| L9 | WHO・IAEA・UNDP 合同発表「Chernobyl: the true scale of the accident」（2005-09-05） | https://www.who.int/news/item/05-09-2005-chernobyl-the-true-scale-of-the-accident | `who2005_true_scale.html`（d0604e3b） | 引用 |
| L10 | INES User's Manual 2008 Edition（IAEA・OECD/NEA 2013） | https://www-pub.iaea.org/MTCD/Publications/PDF/INES2013web.pdf | `ines_manual2008.pdf`（f620dda5） | 引用 |
| **K1** | 国会会議録（「チェルノブイル」97件・「チェルノブイリ」110件・1986-04-26〜1987-05-31＝重なりを除き**206発言**）＋会議名と日付で引いた15発言（§2-11 の4つの答弁は「チェルノブイル」の語を含まないので、語の検索では出なかった） | https://kokkai.ndl.go.jp/api/speech?any=… （`probe/fetch_kokkai.py`） | `kokkai_チェルノブイル_…json`（af7beb46）・`kokkai_チェルノブイリ_…json`（f102180f）・`kokkai_targets.json`（f8eab17a） | 著作権法40条1項（国会での演説・陳述は利用できる）＝会議名・日付・発言者を添える。⚠️ curl は**名乗りを変えたら通った**（①の「curl は403」は名乗りの違い） |
| **U1** | USGS（米国地質調査所）「Landsat Chernobyl」＝Landsat 5 の 1986-04-22（事故前）・04-29（事故後）と 2015-10 の Landsat 8 の3枚組 | https://www.usgs.gov/media/images/landsat-chernobyl | `usgs/412_L.jpg`（a1b99b7a・**5288×3000**） | **PD**（米連邦§105・頁に「Public Domain.」） |
| U2 | USGS「1986 Landsat 5 image Chernobyl after」（4月29日・注記つき） | https://www.usgs.gov/media/images/1986-landsat-5-image-chernobyl-after | `usgs/0_4-29-1986_Chernobyl_Intro-label.png`（1f245b4f・1000×807） | PD |
| U3 | USGS「1987 Landsat TM Chernobyl Images」 | https://www.usgs.gov/media/images/1987-landsat-tm-chernobyl-images | `usgs/1987-Landsat-TM-Chernobyl-Images.jpg`（c5cb4124・**600×410＝小さい**） | PD |
| **U4** | 🆕 USGS『1986 USGS Image Data of the Nuclear Accident Near Chernobyl Report』（25 PDF頁・文字の層なし＝中身は未見） | https://www.usgs.gov/media/files/1986-usgs-image-data-nuclear-accident-near-chernobyl-report | `usgs/1986_USGS_Image_Data_of_the_Nuclear_Accident_Near_Chernobyl_Report1.pdf`（4f506e86） | PD |
| R1 | Mixkit「Stock Video Restricted License」本文 | https://mixkit.co/license/#videoRestricted | `stock/mixkit_restricted_license_2026-10-22.txt` | 🔴 **YouTube の動画は不可**（Not Allowed に「YouTube videos」）＝materials.md §5 |
| R2 | Pexels License | https://www.pexels.com/license/ | `stock/pexels_lists_2026-10-22.txt` | 可（禁止は5つ＝人を悪く見せる・そのまま売る・推薦を装う・ほかの素材サイトで配る・商標） |
| R3 | 外務省 報道発表「ウクライナの首都等の呼称の変更」（令和4年3月31日） | https://www.mofa.go.jp/mofaj/press/release/press1_000813.html | （保存なし） | 中身は①のチャットがブラウザで原ページを確認（10-22）・**URL は②で検索して控えた** |
| R4 | 外交青書2022 第3章第1節4「軍縮・不拡散・原子力の平和的利用」（「チョルノービリ原子力発電所」） | https://www.mofa.go.jp/mofaj/gaiko/bluebook/2022/html/chapter3_01_04.html | （保存なし） | 同上 |

### 1-1. 取れなかったもの・読んでいないもの（隠さず）
- **INSAG-1 の刊行版**（Safety Series No.75-INSAG-1・STI/PUB/740・1986・106頁・ISBN 92-0-123186-5＝IAEA の目録 https://www.iaea.org/node/58522 ・INIS https://inis.iaea.org/records/8e700-gms57 ）＝このチャットでも **PDF は未入手**（①＝INIS は Cloudflare）。本文は S2 で足りる。⚠️ INSAG-7 が引く「INSAG-1 (p. 15)」は**刊行版の頁**＝S2 では印刷 ~22（PDF 25）
- **ソ連報告 Part II**（「100倍」の元の計算）
- **WHO 2006**『Health Effects of the Chernobyl Accident…』＝iris.who.int は JS の頁で、curl では755バイトの案内だけ（`src/who2006_health_effects.dspace.html`）
- **NEA 2002**＝サイトが Cloudflare の確かめ・直の PDF はログインの頁へ転送（使うのは2回目の爆発が未確定の1行だけ＝INSAG-1 と INSAG-7 で足りる）
- **1987年の裁判の一次資料**（未入手）
- ✅ 🆕 **レガソフがソ連の専門家の長だった一次の記録**＝IAEA の写真 02790060（1986年8月の事故後検討会議・Commons・CC BY-SA 2.0）の机の名札「**V. LEGASOV / HEAD, USSR EXPERTS**」を原寸の切り出しで確認（`src/crops/IAEA_02790060_plate.png`・materials.md §1-1）。S3 の名簿（作成に加わった24人）とあわせて「ソ連の専門家団の長として説明した」と言える。⚠️ 説明の**中身**（何を言ったか）は S3 と INSAG-1 で当てる＝「法廷証言」「欠陥を隠した／暴いた」は引き続き言わない
- **ウクライナ著作権法の原文**＝zakon.rada.gov.ua は curl でもアプリ内のブラウザでもつながらない（音声の根拠は materials.md §4）

---

## 2. 骨の照合（①を原文に当て直した結果）

判定：✓＝①と同じ／✏️＝①を直す・細くする／🆕＝①に無かった

### 2-1. 時刻（モスクワ時間）
| 出来事 | 原文と資料 | 判定 |
|---|---|---|
| 出力低下の開始（25日） | S3「at exactly 1:00 hours」（p.20／16）⇔ 付属書I 表I-I「01:06 Start of reactor power reduction; ORM equals 31」（S1 p.63／53） | ✓ 割れる（01:00／01:06） |
| ECCS の切り離し・試験の延期 | 表I-I「14:00 Disconnection of the ECCS…」「14:00 Postponement of testing programme requested by Kiev power grid controller」（S1 p.63／53） | ✓ |
| 出力低下の再開 | 「At 23:10 hours, the power reduction was resumed」（S3 p.20／16）・表I-I「23:10 … ORM equals 26」（S1 p.63／53）⇔ INSAG-1 本文「At 23:00 power reduction resumed」（S2 p.28／~25） | ✓ 割れる |
| 制御の切替と出力の急落 | 表I-I「00:28 At reactor thermal power of about 500 MW transfer made…」（S1 p.63／53）・S3「the power fell below 30 MW(th)」（p.20／16・時刻の数字なし）・INSAG-7「precipitous fall in power to 30 MW(th)」（S1 p.21／11） | ✓（「未満」は S3） |
| 200MW で安定 | S3「Only at 1:00 on 26 April … stabilizing it at 200 MW(th)」（p.20／16）⇔ 表I-I「01.03 Reactor thermal power increased to 200 MW and stabilized」（S1 p.64／54）・表II-III 01:03（p.123／113） | ✓ 割れる（01:00／01:03） |
| 🔴 タービン2台の停止で炉を止める保護の無効化 | INSAG-7 本文「occurred at 00:43:27 rather than at 01:23:04 as stated in INSAG-1」（S1 p.21／11）⇔ 表II-III「00:43:37 The emergency protection system which shuts down both turbogenerators was disabled」（S1 p.123／113）・表I-I も 00:43:37 の行（p.64／54・列が崩れている） | ✏️ **10秒の割れ**（①は時刻を並べただけ）→ 画面は「0時43分ごろ」 |
| 試験の開始 | 01:23:04（S3 p.21／17・表I-I p.64／54・付属書I 1-4.6.2 p.75／65） | ✓ |
| 止めるボタン（AZ-5＝付属書の訳では EPS-5） | 表I-I「01:23:40 EPS-5 button was pressed」＋「(01:23:39 on teletape)」（S1 p.65／55）・1-4.6.3「The Commission was unable to establish why the button was pressed」（p.76／66） | ✓ |
| 出力の非常信号 | 表I-I「01:23:43 Power excursion rate emergency protection system signals on」（p.65／55） | ✓ |
| 爆発 | S3「According to observers outside unit 4, at about 1:24 there occurred two explosions」（**p.21／17**）・INSAG-1「The two explosions occurred around 01:24」（S2 p.68／~63）・上級運転員の日誌「01:24: Severe shocks」（表I-I p.65／55） | ✓（✏️ S3 の頁は p.21／17） |
| 「1時23分44秒」 | INSAG-1 表I の 1:23:44 の行（S2 p.40・計算の行）＝爆発の時刻ではない | ✓ |
| 屋根の火 | 「the fires on the roofs of Units 3 and 4 were localized at 02:10 and 02:20 respectively, and the fire was quenched at 05:00」（S2 p.68／~63） | 🆕 |

### 2-2. 運転反応度余裕（ORM＝差し込んだままの制御棒が「標準の棒何本ぶん」か）
| 論点 | 原文と資料 | 判定 |
|---|---|---|
| 規則の数 | 付属書I 1-4.8 が規則を引く＝定常は「not less than 26-30 rods」・26本未満は技師長の許可・「When the ORM falls to 15 rods, the reactor should be shut down immediately」（S1 p.89／79）。同じ節に別の文書の「26本以上35本以下」も（p.90／80） | ✓（「30本」とだけ言わない） |
| 🆕 25日の値 | 表I-I＝01:06 **31本**・07:10 **13.2本**・15:20 16.8本・23:10 26本（S1 p.63／53）＝07:10 は即時停止の15本を下回る。INSAG-7 (5)「this minimum ORM was also violated for several hours on 25 April」（p.21／11） | 🆕 |
| 1:22:30 の値 | S3「only 6-8 rods … not more than half of the minimum permissible value」（p.23／19）／表I-I「ORM proved to be equal to 8 manual control rods」＝**事故のあとスモレンスク原発で PRIZMA で計算**（p.64／54）／付属書II＝発電所では計算していない・標準の曲線で 1.9本・実際の分布で 6〜8本（p.123／113） | ✓ |
| 運転員は知っていたか | S3「the operator saw from a printout … requiring immediate shutdown」（p.21／17）⇔ INSAG-7「it is likely that the operator did not know the value of the ORM」（計算機 SKALA が当てにならなかった・p.21／11） | ✓ **逆** |

### 2-3. 非常用炉心冷却系（ECCS）
| 資料 | 原文 | 判定 |
|---|---|---|
| INSAG-7 (1)（S1 p.20／10） | 「blocking of the ECCS was in fact permissible … if authorized by the Chief Engineer」・試験の手順の承認された一歩・事故の始まりと進みに影響なし。🆕 ただし「半分の出力で約**11時間**、ECCS を切ったまま」は試験の計画の外＝違反でないとは言えない | ✓＋🆕 |
| 付属書I 1-4.7.2（S1 p.82／72） | 「taking the ECCS out of operation is a violation of Section 2.10.5」・同時に「did not affect the initiation and development of the accident」（自動起動の信号は記録されていない） | ✓ 割れる・**効いていないは全資料で一致** |

### 2-4. 0時28分の出力の急落
- INSAG-7 (3)（S1 p.21／11）：INSAG-1 は運転員の誤りとした → 「Recent reports suggest that there was no operator error as such」＝付属書I は原因不明と制御できなかったこと・🆕 **元副技師長 A.S. ジャトロフの私信**（系統が正しく働かなかった）を引く
- ✏️ 付属書I の本文 1-4.6.1 は「the senior reactor control engineer failed to eliminate fast enough the imbalance」（S1 p.73／63）＝**付属書I の中にも言い方が2つ**。→ 台本は「INSAG-7 は『運転員の誤りとは言えない』と書き直した」と**帰属**して言う

### 2-5. タービン2台の停止の信号（INSAG-7 (4)・S1 p.21／11）
- 時刻は 00:43:27（付属書は 00:43:37＝§2-1）・「blocked in accordance with operational procedures and test procedures」・付属書I 1-4.7.4 は運転員に責めを負わせない
- INSAG-1 の表の「This trip would have saved the reactor」は、ポジティブ・スクラムに照らすと「seems not to be valid」
- ✏️ ①の「働けば早く壊れたかもしれない」は **INSAG-7 の文に無い**（「炉を救ったはず、は成り立たないようだ」まで）

### 2-6. 蒸気ドラムの保護（INSAG-7 (6)・S1 p.22／12）
- INSAG-1 の 01:19 → 「changed as early as 00:36」・付属書I は運転員を責めない
- 保護は2段（600mm と、ふだんは 1100mm）。運転員は設定を戻さず「technically in violation of Item 9」＝**形の上では違反**。ただし「protection at the lower steam drum level remained effective throughout the event」
- ✏️ ①の「無効化は起きていない」＝「下の段の保護は最後まで効いていた」が正確（形の上の違反も添える）

### 2-7. 止める棒の欠陥（ポジティブ・スクラム）
| 論点 | 原文と資料 | 判定 |
|---|---|---|
| 棒の形 | 吸収材の先に黒鉛の「displacer」（押しのけ棒）・「a water filled space of 1.25 m」・抜き切ると押しのけ棒が炉心の真ん中に来て両端に 1.25m の水（INSAG-7 2.2・S1 p.14／4・図1 p.15／5） | ✓（案C の断面の正本） |
| 何が起きるか | 抜き切った棒が落ち始めると、炉の下の方の水が押し出されて「a local insertion of positive reactivity in the lower part of the core」（p.14／4） | ✓ |
| 見つかった時 | 付属書I 1-3.8「discovered experimentally in November/December 1983 during the physical startup of Ignalina Unit 1 and that of Chernobyl Unit 4」・主任設計技師と科学責任者は事故の前に知っていた（S1 p.53／43） | ✓ |
| ✏️ INSAG-7 本文の言い方 | 4.1 は「first identified at the Ignalina RBMK plant … in 1983」とだけ（S1 p.23／13）＝**本文はイグナリナだけ・付属書I は両方** | ✏️ 「この4号炉自身で」は**付属書I（ソ連の規制側の委員会・1991）によると**と帰属 |
| その後 | 4.2「Such restrictions were never imposed and apparently the matter was forgotten」（p.25／15） | ✓ |
| 公に認めた時 | 4.1「first acknowledged by Soviet experts at the Conference … in Vienna in 1987」（p.23／13） | ✓ |

### 2-8. 1986年の説明と1992年の書き直し（言葉）
| 資料 | 原文 | 頁 |
|---|---|---|
| INSAG-1（S2） | 根本原因は「the so-called 'human element'」／「a remarkable range of human errors and violations of operating rules」／「deliberately and in violation of rules withdrew most control and safety rods」／ソ連の説明は「entirely plausible」／700MW 未満は「forbidden by normal safety procedures」 | p.112／~105・p.18／~13・p.10／~5・p.110／~103・p.25／~22 |
| ソ連報告（S3） | 「the prime cause … was an extremely improbable combination of violations」／違反の表（第4章）／試験の計画は「had not received the requisite approval」 | p.27／23・p.26／22・p.19／15 |
| INSAG-7（S1） | 6(2)「shift the emphasis to the contributions of particular design features」／6(6)「were in fact not violations」＋「critical actions of the operators were most ill judged」／6(7)「does not retract INSAG-1」／6(4)「It is not known for certain what started the power excursion」／5.1「most likely final event … the insertion of safety rods」／700MW 未満は「not proscribed, either in design, in regulatory limitations or in operating instructions」＋「There should have been such a proscription」 | p.33／23・p.34／24・p.26／16・p.21／11・p.28／18 |
| 付属書I（1991） | 欠陥は「not included in the papers presented to the IAEA」／1986年6月「reduced exclusively to personnel errors」／1986-05-01 クルチャトフ研のヴォルコフ／試験計画は「there is nothing wrong with the programme itself」／職員は「no better, but no worse」／引き金は EPS-5 を押したこと・押した理由は確定していない | p.41／31・p.70／60・p.62／52・p.93／83 |
| 「核爆発」の語 | 「nuclear explosion」＝S1・S2・S3 とも**0件**（綴りの限り） | — |
| 100倍 | INSAG-1「The Soviet experts calculated that the first power peak reached 100 times the nominal power within four seconds」（S2 p.10／~5）⇔ 付属書I「increased in comparison with the initial value several tens of times during a period of about 5 s」（S1 p.77／67） | ✓ |

### 2-9. 亡くなった方（事故の夜〜数か月）
| 資料 | 原文・数 | 判定 |
|---|---|---|
| ソ連報告 1986-08（S3 p.43／39） | 6時までに108人が入院・その日のうちに24人。「One person died from severe burns at 6:00 hours on 26 April and one of those working at the damaged unit was not found」 | ✓＋🆕 108・24 |
| UNSCEAR 1988 付録（L7 PDF p.74） | 「One person with severe thermal burns died during the first hour. Another, a reactor operator, could not be found」 | ✏️ **やけどの1人の時刻が割れる**（ソ連＝6時／UNSCEAR 1988＝最初の1時間以内）→ 時刻は言わない |
| INSAG-1（S2） | 「300 power plant and fire-fighting personnel admitted to hospitals, of whom 31 have so far died」（p.118／~111）・急性放射線症で29人（p.115／~108） | ✓ |
| フォーラム 2006（L1 p.12／14） | 28人が1986年に急性放射線障害（ARS）で・2人は4号機で放射線と無関係のけが・1人は冠動脈血栓とされた | ✓（＝31） |
| UNSCEAR 2000（L2） | 30人（うち放射線28人）（p.5／453・p.67／515）／237人を調べ確定134人（第186段落 p.40／488）／「Among the 134 cases, 28 died within the first four months」（第191段落） | ✓ |
| UNSCEAR 2008（L3） | 直後の2人（p.7／47）／104人＋のちに30人＝134人・28人（第49段落 p.18／58） | ✓ |
| 国会 1986-11-27 衆院 科学技術委（K1） | 佐々木壽康 局長「これまでソ連から発表されております数字でございますが、死亡者は三十一名」・ARS 174名・「その辺の内訳はソ連から出されておりません」 https://kokkai.ndl.go.jp/txt/110703911X00419861127/7 | ✓ |
| 国会 1987-05-18 衆院 外務委（K1） | 遠藤哲也 審議官「二十九人が急性放射線障害で死亡…爆発直後にやけどで死亡した方が二人…合計三十一人」（1987-01-20 のソ連の医療調査団の記者会見＋4月の IAEA の…） https://kokkai.ndl.go.jp/txt/110803968X00219870518/68 | ✓ |
| 🆕 国会 1986-05-15 参院 内閣委（K1） | 今村治 室長「合計九名が死亡していると聞いております」・「四万八千人が避難」＝**5月半ばの数**（のちに31へ） https://kokkai.ndl.go.jp/txt/110414889X00819860515/218 | 🆕 |

### 2-10. 避難
| 論点 | 原文と資料 | 判定 |
|---|---|---|
| プリピャチ | 第92段落「the residents of Pripyat (49,360 persons) and of the nearest railway station, Yanov (254 persons)」・決定は26日「22:00」・「nearly 1,200 buses」・🆕「Around noon on 27 April the evacuation order was broadcast」・「began at 14:00 and finished at 17:00」（L2 p.24／472） | ✓＋🆕 放送は正午ごろ |
| 1986年の避難・その後の移住 | 約11万6,000人（1986年）・約22万人（1986年より後）（L2 p.5／453・p.67／515）・フォーラム「116 000 people were evacuated in the spring [and summer of 1986]」（L1 p.8／10・文字の層が一部化けている）・「Another 220 000 people were relocated」（p.9／11） | ✓ |
| 日付の割れ | 第105段落だけ「Pripyat (28 April)」（L2 p.26／474） | ✓ |

### 2-11. 日本の入口（国会会議録・発言の原文で照合）
| 日・会議・発言者 | 原文 | URL |
|---|---|---|
| **1986-05-07** 参院 科学技術特別委 第6号・**河野洋平 科学技術庁長官**（発言204） | 「五月三日に至り、東京都、千葉県、神奈川県におきまして、今回の事故に起因すると思われる沃素131が検出されました」・🆕「五月四日早朝、放射能対策本部会合を開催」・国民への注意（雨水をじかにとるなら木炭等でこす／水道水・井戸水・牛乳は心配ない／葉菜類は念のため洗う） | https://kokkai.ndl.go.jp/txt/110413928X00619860507/204 |
| 1986-05-08 衆院 農林水産委・今村治 原子力安全調査室長（発言41） | 「五月三日夕方ごろまでは当該発電所に由来すると思われる影響は認められなかった」・「五月三日以降採取した浮遊じん、雨水等の核種分析の結果、沃素131等の放射性物質が検出」・4月29日から全国の調査 | https://kokkai.ndl.go.jp/txt/110405007X01619860508/41 |
| 1986-05-09 参院 エネルギー対策特別委・辻栄一 原子力安全局長（発言70） | 「千葉県ではいっとき雨水の中に一リットル当たり最高で一万三千ピコキュリーという沃素131」・毎日2.2リットルを2か月飲み続けて許容線量に「ようやく達する」程度 | https://kokkai.ndl.go.jp/txt/110413809X00319860509/70 |
| 1986-05-15 参院 内閣委・今村治 室長（発言218） | 「五月三日以降十四日時点で、二十九都道府県にわたり…ヨウ素131が検出」 | https://kokkai.ndl.go.jp/txt/110414889X00819860515/218 |
- ✏️ ①の未照合2つを解いた＝5月4日の呼びかけの字句（上）／最初の試料＝「浮遊じん、雨水等」（どちらが先かは言っていない＝台本は「空気中のちりや雨水から」）
- 表記＝1986年の国会は「チェルノブイル」（今村室長は「チュルノブイル」）・1987年の外務委は「チェルノブイリ」

---

## 3. ④ に渡す「言える・言えない」の更新（①の §1-4 に足す・直す）
1. ✏️ 「この4号炉自身の試験で見つかっていた」は**付属書I（ソ連の規制側の委員会・1991）の言葉**として言う（INSAG-7 本文はイグナリナだけ）
2. ✏️ 0時43分の保護の無効化は「0時43分ごろ」（秒は割れる）。「働けば炉を救った」は INSAG-7 が退けた（「働けば早く壊れた」とは言わない）
3. ✏️ 0時28分の急落を「運転員の誤りではない」と言うのは **INSAG-7 の書き直し**として（付属書I の本文には上級運転員が素早く直せなかったとも書いてある）
4. ✏️ 夜に亡くなった2人のうちやけどの1人の時刻は言わない（6時／最初の1時間で割れる）
5. 🆕 ORM は4月25日の朝（7時10分）にも13.2本＝即時停止の15本を下回っていた（表I-I）＝「規則を下回ったのは事故の直前だけではない」
6. 🆕 ECCS は「半分の出力のまま約11時間」切られていた（INSAG-7＝承認はあったが計画の外）
7. 🆕 国会の数は時期で増えた（1986-05-15 に9人 → 11-27 に31人）＝「31人」は「ソ連が発表した数」と帰属
8. 🆕 避難の放送は27日の正午ごろ（UNSCEAR 2000 第92段落）＝音声 `Pripyat 1986.ogg` の中身の時刻を確かめる手がかり（materials.md §4）
9. 実名の材料（§B2-1 の判断は④）：一次資料に出る名前は INSAG-7 の A.S. ジャトロフ（元副技師長・私信の引用）・付属書の委員長2人・S3 の専門家団24人（レガソフを含む）だけ。INSAG-1（S2）は名前0件。運転員・消防士の名前は一次資料に**無い**（二次資料だけ）。🆕 写真の記録＝1986年8月の会議の名札（V. LEGASOV「HEAD, USSR EXPERTS」・H. BLIX・R. ROMETSCH・M. ROSEN・L. KONSTANTINOV・AMB. KHLESTOV）＝materials.md §1-1
10. 🆕 電話の録音（Commons の字幕）は「3・4号機の屋根が燃えている」＝INSAG-1 の屋根の火と合う。ただし時刻は録音に無い・権利の根拠が弱い＝materials.md §4
