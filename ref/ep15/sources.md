# 15本目（リノ・エアレース2011・2011-09-16）── 一次資料の台帳

**取った日＝2026-09-24（②③のチャット）。**置き場＝`ref/ep15/src/`（リポの無視設定＝**PDF・本文・JSON はコミットしない**。この台帳の URL と md5 で取り直す）。
骨の照合＝[facts_ntsb.md](facts_ntsb.md)／素材＝[materials.md](materials.md)／尺＝[kousei.md](kousei.md)／ドケットの全59件の目録＝[ntsb_docket_items.tsv](ntsb_docket_items.tsv)（1件1行・URL・md5・頁・写真数）

---

## 0. 読み方（まずここ）
1. 🔴 **正本の順位＝NTSB AAB-12/01（最終・2012-08-27 採択）＞ドケットの各報告（2012-05〜08）＞勧告書（2012-04-10・暫定の数を含む）＞CAROL（勧告のその後）＞RARA・NAG の手紙（民間）＞報道（二次）**
2. 🔴 **負傷者の数は NTSB の文書の中でも割れる**：勧告書（2012-04）「66人が重傷」（暫定）⇔ AAB（2012-08）「少なくとも64人・うち重傷16人以上・**正確には決められない**」⇔ 映像解析 #41「60人以上」。**台本は AAB の言い方**（facts_ntsb.md §G・§K）
3. 🔴 **AAB 脚注28・画像解析は「原寸の写真はドケットにある」と書くが、ドケットに JPG・MP4 は無い**（59件＝PDF 58＋CSV の ZIP 1）。写真は PDF に埋め込まれた最大 1431px だけ
4. 🔴 **報告書の写真の多くは "Photograph courtesy of 〈個人〉"＝撮影者の著作物**。PD（米連邦 §105）は本文と NTSB 自身の図・写真だけ（facts_ntsb.md §J）
5. ⚠️ 時刻は **PDT（太平洋夏時間＝UTC−7）**。日本時間は＋16時間（衝突 16:24:38 PDT＝2011-09-17 08:24:38 JST）
6. ⚠️ AAB の頁は **PDF の頁**で書く（印字の頁＝PDF −9）。ドケット #20（耐空性の写真付録）は **NTSB のサーバーで壊れている**（先頭 876,544 バイトだけ中身・取り直しても同じ md5）

---

## 1. 取得ずみ（1件1行）
| # | 資料 | 取った URL（状態） | 保存名 | 大きさ・頁 | md5 | 権利 |
|---|---|---|---|---|---|---|
| S1 | 🔴 **NTSB/AAB-12/01**「Pilot/Race 177, The Galloping Ghost, North American P-51D, N79111, Reno, Nevada, September 16, 2011」（Aircraft Accident Brief・2012-08-27 採択） | https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf（200・Content-Length 一致） | `AAB1201.pdf` → 全文 `AAB1201.txt` | 2,434,266 B・52頁 | `ffd36fc6cc8d868db5b9a8e5e39f8a6b` | 本文・NTSB の図＝**PD（A）**／図4〜10・15〜17 の写真＝撮影者 © |
| S2 | **NTSB 公開ドケット WPR11MA454**（59件の目録） | https://data.ntsb.gov/Docket/?NTSBNumber=WPR11MA454（目次 `/Docket/TOCPrintable?data=81814`・各資料 `/Docket/Document/docBLOB?ID=<id>&FileExtension=.PDF&FileName=<名前>`） | `ntsb_docket_items.tsv`（`ref/ep15/` に写し） | 59件 | 1件ずつ tsv に | PD（A）。中の民間の写真と RARA・NAG の手紙は除く |
| S2-a | ドケットのうち取った22件＝#01 気象（32頁）・#14 データ記録（40）・#15 同 付属1 FBI（3）・#16 同 付属2 CSV の ZIP・#17 耐空性（29）・#18 同 追補1 レースの速さ（3）・#19 追補2（2）・#20 写真付録（破損）・#22 聞き取りの要約（26）・#33 生存要因と運航（22）・#37 2011年のコース図（2）・#39 現場指揮者（2）・#40 材料試験 12-029（61）・#41 映像解析（11）・#42 画像解析（27）・#43 目撃者の映像（1）・#51 医学（4）・#53 性能解析（29）・#54 FAA の回答（2）・#55 NTSB→FAA（2）・#56 NAG の回答（6）・#57 RARA の回答（5）・#59 耐空性 追補3（20） | 同上 | `ntsb_docket_NN_*.pdf`（＋頁区切りの `.txt`） | — | tsv の各行 | PD（A）＋民間（#56・#57 の手紙・#42 の写真） |
| S3 | 勧告書 **A-12-08**（FAA 宛・2012-04-10） | https://www.ntsb.gov/safety/safety-recs/recletters/A-12-008.pdf（200） | `ntsb_recletter_A-12-008.pdf` | 501,523 B・5頁 | `9f4efe5255480f64f89ac1cee8532c70` | PD（A） |
| S4 | 勧告書 **A-12-09〜12**（NAG 無制限部門宛） | https://www.ntsb.gov/safety/safety-recs/recletters/A-12-009-012.pdf（200） | `ntsb_recletter_A-12-009-012.pdf` | 226,730 B・6頁 | `42c41cb201d572eafc8b6c1aca918b50` | PD（A） |
| S5 | 勧告書 **A-12-13〜17**（RARA 宛） | https://www.ntsb.gov/safety/safety-recs/recletters/A-12-013-017.pdf（200） | `ntsb_recletter_A-12-013-017.pdf` | 228,067 B・7頁 | `84ff961170f71aed43cd39e87415859a` | PD（A） |
| S6 | **CAROL 勧告の記録 10件**（A-12-08〜17・往復書簡の要約と最終の分類）→ 照合の結果＝[facts_ntsb.md §K](facts_ntsb.md) | `https://data.ntsb.gov/carol-main-public/api/Query/GetSrRecord/A-12-008` ほか（末尾の番号を替える） | `ntsb_carol_sr_A-12-0xx.json` | 19,886〜36,408 B | 008 `21ea717b3e1d90333d15f305db660a94`／009 `f39da10f9671100af9abacc0ae9c95f6`／010 `fff89a27718a0ad4d6ac2b99a885f53e`／011 `d19c840b43cb194305ad86105a32b199`／012 `e57506eb73b0d7a44486f0c549ff937f`／013 `2fbe09105d132b3abbc6685df1e41160`／014 `4c6c21858be18a9b701de5591215ab03`／015 `5bac305cb89d691132dcd076ae32fb2d`／016 `acb156d8fadb8e29025422f8b8ecef4c`／017 `6a8f0ce6df614bb62a246c1d21ea5bdf`（⚠️ API の返事＝取り直すと md5 は変わりうる） | PD（A） |
| S7 | 2012-01-10 公聴会・第2パネルの **RARA の発表資料**（Houghton） | 取得元は一次資料役の作業記録に残っていない（題名で探し直す） | `ntsb_hearing_20120110_panel2_RARA_Houghton.pdf` | 6,316,198 B・18頁 | `617b73b5ecf630b4837adf3baffe5891` | RARA ©＝引用 |
| S8 | FAA **AC 43-209A**「Recommended Inspection Procedures for Former Military Aircraft」（2013-04-12・AFS-300） | 同上（FAA の文書情報ページは403） | `faa_AC_43-209A.pdf` | 73,389 B・12頁 | `a191514aeeb9eef67f99cd30cabd0ef3` | PD（A） |

## 2. 未入手（理由と、次に当たる先）
| 資料 | 状態 |
|---|---|
| 2012-01-10 公聴会（エアレースと航空ショーの安全）の**議事録・映像・証人一覧** | 見つからない（`https://www.ntsb.gov/investigations/Pages/WPR11MA454.aspx` にリンクなし）。ドケット ID 40264328 の「Hearing Transcript 1」は別の事故（2006年）＝除外 |
| **RARA の外部検証チーム（blue ribbon）の報告**（2012-04-27・AAB p38） | 本体は未入手。顔ぶれ（元 NTSB 委員長 Jim Hall ほか4人）・勧告の中身は**二次**（thisisreno.com 2012-01・nevadaappeal.com 2012-05-23） |
| FAA 命令 8130.2G への特例（2011-12-21） | 本体は未入手（AAB p50 だけ） |
| FAA 命令 8900.1 の改訂（2015-05-15・2020-02-27）／AC 91-45C の廃止（2020-11-03）／Notice 8900.526（2019-10-10） | **CAROL の往復書簡**で確認（2020-02-27 と 2020-11-03 は NTSB の最後の手紙 2021-07-13 の原文で Claude が確認＝facts_ntsb.md §K）・本体は未取得。AC 91-45D の存在は未確認 |
| ドケット #58（ドケット版の報告書・3,327,282 B＝手元の S1 と別ファイル）・#32／#34〜36（FAA 文書の束 37MB）・#2〜13／#52（証拠管理票）・#44〜49（関係者の声明） | 未取得（④で要れば tsv の URL から） |
| 目撃者の映像（Jason Schillereff・720×480・30fps） | ドケットに映像は無い。写しは NTSB の窓口（Public Inquiries）へ問い合わせ＝未 |
| 大会のその後（2023年がステッドで最後・2025年からロズウェル） | **二次**（空港当局と RARA の共同発表・RARA の記事＝本文未確認・観客数は AOPA） |
| 2011-09 の日本の報道 | 日経（共同電）2011-09-17「5人死亡40人以上負傷」・AFPBB 2011-09-17「9人死亡」＝**二次**（当日の速報の数） |

## 3. 資料どうしの食い違い（一次資料役の報告＋Claude の確認）
1. 🔴 負傷者の数（§0-2）＝勧告書「66 people sustained serious injuries」を Claude が原文で確認（S5 p1・脚注2＝49 CFR 830.2 の「重傷」の定義）
2. 🔴 原寸の写真の所在（§0-3）
3. #57 の題の「72912」＝中身は 2012-07-09 と 07-12 の手紙。CAROL は 07-09 の手紙を 07-12 で記録
4. ドケットの「最終更新 2012-08-21」＝実際は #56 が 08-22 作成・#54〜57 は 08-23 更新・#59 は 10-04 作成
5. NAG 2012-07-06 の手紙は「4件の勧告」と書きつつ A-12-9〜13 を挙げる（A-12-13 は RARA 宛）
6. NAG 2012-08-22 の手紙は A-12-9 を引くとき「major」が抜けている
7. RARA 2013-03-13 の手紙は NTSB の審議を「2012-08-12」と書く（NTSB・CAROL は 08-27）
8. FAA の回答（2012-06-26）＝8900.1 の改訂案づくりを「2011年7月」＝事故の前に始めたと書く（AAB はこの日付を省く）
9. 🔴 AAB の時点で Open だった A-12-08・09・13 は、のちに全部 Closed（facts_ntsb.md §K）＝**「その後」を語るときは CAROL の最終の分類で**
10. ドケット #20 の破損（§0-6）
