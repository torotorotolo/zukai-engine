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
| S7 | 2012-01-10 調査のための公聴会（Air Race and Air Show Safety）・第2パネルの **RARA の発表資料**（Michael Houghton・PDF の作成 2012-01-10） | https://www.ntsb.gov/news/events/Documents/air_show-panel2_Houghton.pdf（09-25 に HEAD 200・**6,316,198 B＝手元と同じ大きさ**・md5 は未照合）。旧名 `2012_Air_Race_Show_IHG-Panel2a_Houghton.pdf`（Wayback の索引） | `ntsb_hearing_20120110_panel2_RARA_Houghton.pdf` | 6,316,198 B・18頁 | `617b73b5ecf630b4837adf3baffe5891` | RARA ©＝引用 |
| S8 | FAA **AC 43-209A**「Recommended Inspection Procedures for Former Military Aircraft」（2013-04-12・AFS-300） | https://www.faa.gov/documentlibrary/media/advisory_circular/ac_43-209a.pdf（09-25 に HEAD 200・**73,389 B＝手元と同じ大きさ**） | `faa_AC_43-209A.pdf` | 73,389 B・12頁 | `a191514aeeb9eef67f99cd30cabd0ef3` | PD（A） |

## 2. 未入手（理由と、次に当たる先）
| 資料 | 状態 |
|---|---|
| 2012-01-10 公聴会（エアレースと航空ショーの安全）の**議事録・映像・証人一覧** | 議事録と公式の録画は**見つからない**（当時の NTSB の頁は「中継は3か月保存」の定型文＝Wayback 2017-04-28）。**証人一覧は Wayback の Agenda 頁にある**＝第1パネル McGraw・Cudahy／第2 **Houghton（RARA）**・Hightower・Cline／第3 Sebastian・Downum・Stenevik・DiMatteo・Tucker。NTSB の YouTube にあるのは委員長の記者向け発言（`a2YerSPpidE`・2012-01-11・6:48）だけ。ドケット ID 40264328 の「Hearing Transcript 1」は別の事故（2006年）＝除外 |
| **RARA の外部検証チーム（blue ribbon）の報告**（2012-04-27・AAB p38） | 本体は**見つからない**（検索2回）。顔ぶれ（元 NTSB 委員長 Jim Hall・元 FAA の Nick Sabatini ほか）は検索要約だけ＝**二次**。公表を「2012年5月」とする要約あり＝AAB の 04-27 と食い違う（未確認） |
| FAA 命令 8130.2G への特例（2011-12-21） | 本体は未入手（AAB p50 だけ） |
| FAA 命令 8900.1 の改訂（2015-05-15・2020-02-27）／AC 91-45C の廃止（2020-11-03）／Notice 8900.526（2019-10-10） | **CAROL の往復書簡**で確認（2020-02-27 と 2020-11-03 は NTSB の最後の手紙 2021-07-13 の原文で Claude が確認＝facts_ntsb.md §K）・本体は未取得。AC 91-45D の存在は未確認 |
| ドケット #58（ドケット版の報告書・3,327,282 B＝手元の S1 と別ファイル）・#32／#34〜36（FAA 文書の束 37MB）・#2〜13／#52（証拠管理票）・#44〜49（関係者の声明） | 未取得（④で要れば tsv の URL から） |
| 目撃者の映像（Jason Schillereff・720×480・30fps） | ドケットに映像は無い。🔴 **撮影者本人が Vimeo に元の映像を公開中**＝`vimeo.com/29519344`「Final Flight of the Ghost」（2011-09-24・10:37・説明「地面への衝突は写っていない」「一部を NTSB に提供」・元の解像度は不明）。AVweb「NTSB Video of Reno Crash」（YouTube `JyWUTXuXjr0`・2012-08-27・1:24・720×480・撮影者名なし）は同じ映像の抜粋の**可能性**（推測・画で照合していない）。**NTSB が配っても著作権は撮影者に残る** |
| NTSB 製の動く映像 | YouTube NTSBgov の**記者会見と調査団の出発だけ**（2011-09-17〜18 の4本・1280×720／2012-01-11・2012-04-10）＝米連邦の職員の作＝PD になりうる（事故そのものは写っていない見込み・未視聴）。2012-08-27 の理事会の録画は NTSB のチャンネルに無い（第三者の再アップ `EMmhOkXQB0s`・400×300 だけ）。**NTSB 製のアニメーションは見つからない**。C-SPAN も見つからない |
| 観客の撮った映像（ネット） | 1080p は2本＝`X_qKVMyieVo`（AutoPilotof4・1:46・692万回・中身の記述なし）・`d-09s_eleMs`（**Gary Stone**・観客席から・1:26・「むごい場面は無い」・衝突の力・観客の反応・救急車・場内の「下がって」の放送）。ほかは 720×480 以下。Smithsonian Channel の番組の切り出し（`tFurMChEhno`）は番組の権利 |
| 🔴 **使用許諾を買える映像（Pond5・2026-09-25 に商品頁を確認・買っていない）** | ①**item 8833966「Airplane Crash - Reno Air Races (Galloping Ghost)」by gkstone**（＝Gary Stone の映像と説明文が同じ）＝**1920×1080・mov・215.7MB・¥23,000**（Individual License）／②**item 42241236「Reno Air Race Airplane Crash」by benpcissell**＝**1440×1080**（⚠️ 横は実効1440の見込み＝記憶 `feedback-container-labels-lie-about-the-picture`）・mov・304.5MB・**¥6,000**・中身は未確認。どちらも **Editorial（報道用）だけ**。許諾の原文（`pond5.com/legal/license` 第7条）＝①報道価値のある出来事・公共の関心事に使う ②商品・広告・販促・広告記事・「その他の商用の制作物」には使えない（作品そのものの宣伝は可）③写っている人の肖像・プライバシーの許諾は無い ④**長さの編集とほかの素材との組み合わせだけ可・意味を変えない** ⑤**撮影者と Pond5 のクレジット**（ネットなら pond5.com へのリンク）＝第9条 |
| 大会のその後 | 🔴 **2022-09-18 ジェットの L-29 が墜落・操縦士1人**（撮影者の説明文・二次）／**2023-09-17 T-6 の2機が空中衝突・操縦士2人**（KTNV 2023-09-19・二次。NTSB 番号 WPR23FA345 は検索要約だけ＝未確認）／ステッドでの最後の年＝**2023年**（検索要約だけ）／🔴 **RARA 2024-05-23 の発表＝2025年からロズウェル（ニューメキシコ州）が新しい開催地**（airrace.org＝**一次**・移転の理由と「最後の年」は書いていない）／2025年に実際に開かれたか＝未確認 |
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
11. 🔴 **タブの一片が離れた時刻はどちらも 16:24:33.5 だが、「横転から何秒」が違う**＝ドケット #42 画像解析 図37「横転の**5.3秒後**」⇔ AAB p28 の表「**4.6秒**」（起点の置き方の違い＝Claude が #42 の説明文と AAB の表で確認）。🔴 **台本は時刻と AAB の表で語る**。AOPA 2012-08-22 の「最大Gから2秒未満」（検索要約だけ）は、**ちょうつがいから外れた約3.1秒（最大Gの約1.8秒後）**のことかもしれない（推測）
12. 速さ：報道の「530 mph（約853km/h）」（AP 2012・Military Times）は AAB の**最高 458ノット（約848km/h）**に当たる（パイロン8の 445ノット＝約824km/h とは別の数）。「400 mph（約644km/h）で衝突」は英語版 Wikipedia の**出典の無い文**。日本語の「時速約650km」の出どころは当たっていない
13. 負傷者の報道の数は日を追って変わる＝56（AP 2011-09-17）→「50人超が病院へ」（CSM 09-18）→ 69（英語版 Wikipedia・出典 NBC）→「70人超」（AP 2012-08-27）／死者は 3 → 9 → 10 → 11
14. 年齢：AP 2012-08-27 は「listed his age as 59」「cutting 15 years from his own age」＝**意図を匂わせる書き方**。AAB は "inaccurate"・理由は不明。"lied" は開けた記事には無い
15. NTSB の Mark Rosekind の肩書＝当時は**委員（Board Member）**（要約ツールの "spokesman" は誤り）
16. 依頼文（Claude）の誤り「2022-09-18 の T-6 空中衝突（2人）」＝**2件の混同**（2022＝L-29・1人／2023＝T-6・2人）

## 4. 通説の出どころ（台本で「よく言われる話」として引けるもの＝§B2-6）
| 通説 | 出どころ（開けたもの） | 報告書の答え |
|---|---|---|
| 「トリムタブが外れて、機首が上がった」 | Christian Science Monitor 2011-09-18（航空弁護士 Mike Danko「タブが無ければ操縦できなかったかもしれない」・AVweb の Russ Niles が1998年の Voodoo Chile の前例＝タブが外れて激しく機首上げ）／CBS 2011-09-19 の題「broken tail」／AP 2012-08-27 は部品を「tail stabilizer」と誤記 | 先にリンクが折れた（0.56秒）・一片が離れたのは最大Gの約3秒後（facts §A・§I） |
| 「最後に観客席を避けた」 | NPR 2011-09-19（Mark Memmott）が LA Times と Reno Gazette-Journal の**観客の印象**をまとめた（観客 Gerald DeRego・自家用操縦士の観客 Art O'Connor）。同じ記事に ABC の解説者 Steve Ganyard の「意識を失っていたのだろう」。**大会関係者・仲間のレース操縦士の発言は見つからない** | 意識は1秒未満の見込み・降下は操縦なし（facts §B） |
| 「虚偽の申告」「年齢を偽った」 | 日本語＝競合の題（ゆっくり危険の泉 2025-07）。英語＝AP の「cutting 15 years」（意図を匂わせる） | "inaccurate"・理由は不明・事故との関係の証拠なし（facts §E） |
| 「時速650km」 | 日本語＝競合の題。英語の「400 mph」は Wikipedia の出典の無い文 | パイロン8で約824km/h・最高約848km/h（facts §A） |
- 🔴 台本で引くときは**「〜と報じられました」「観客の中には〜と感じた人もいました」**の形（噂の札・§B2-6）。個人の名前（観客・弁護士）は出さない（私人・要らない）
