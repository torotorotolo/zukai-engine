# 18本目（スレッシャー号 SSN-593・1963-04-10 のリメイク）一次資料の台帳

- 作成：2026-09-30（18本目 ①「芯の再確認」）。芯の当て直しと通説の判定＝[legend_2026-09-30.md](legend_2026-09-30.md)。素材の権利＝[materials.md](materials.md)
- 凡例：**S**＝一次（査問会の記録・海軍の当時の文書・議会の記録）／**L**＝後年の公的な文書（海軍の後年の文書・NHHC・NAVSEA）／**A**＝当事者・元分析官の後年の分析（個人）／**D**＝同時代の研究（学位論文）／**P**＝報道・雑誌
- 頁の書き方：「PDF p.」＝ファイルの頁。「記録 p.」＝査問会の記録の通し頁。Vol.I（第1回）の**認定・意見・勧告は頁の印字が文字層に出ない**ので、索引（PDF p.2「Findings of Fact 1679／Opinions 1702／Recommendations 1715」）から換算＝**記録 p.＝PDF p.＋1645**（3か所の差が一致）。**証言の頁は下に印字がある＝記録 p.＝PDF p.−73**（例 PDF p.144＝印字 71）。第9・10次と第18回は文書ごとに自分の頁番号（Exhibit・「-3-」など）を持つ
- 文字は NFKC＋行末のハイフンの継ぎ＋空白を潰してから探した（scratchpad の `grepq.py`）。画像は読んでいない
- 保存先 `ref/ep18/src/` は **git の管理外**（`.gitignore:9 ref/*` で確認）。合計 **45MB**
- ⚠️ **取れなかった物（突破していない）**：USNI News の全記事（Cloudflare の確認画面）／DocumentCloud の API と静的な文字版（`s3`・`assets` とも同じ確認画面＝旧版の頃とは変わった）／usni.org の本の頁（403）。海軍の閲覧室は WebFetch では拒否、ふつうのブラウザ名（UA）の curl では 200（確認画面ではない）

---

## 1. 海軍の FOIA 公開＝**全23回**（James Bryant 元大佐の訴訟・2019 提訴・2020-02 に連邦地裁〈DC〉が月ごとの公開を命令）

- 棚（海軍の FOIA 閲覧室「THRESHER RELEASE」）：https://www.secnav.navy.mil/foia/readingroom/HotTopics/Forms/AllItems.aspx?RootFolder=%2Ffoia%2Freadingroom%2FHotTopics%2FTHRESHER%20RELEASE （34ファイル＋台帳 xlsx）
- 各ファイルの URL＝`https://www.secnav.navy.mil/foia/readingroom/HotTopics/THRESHER%20RELEASE/` ＋ファイル名（空白は `%20`、括弧は `%28` `%29`）
- 公開日＝海軍の台帳 `Running Release Inventory.xlsx`（第1〜17回・Excel の日付の通し番号を換算）。第18〜23回は台帳に無い＝**棚の更新日**。大きさ＝Range 要求の Content-Range、頁数＝線形化 PDF の `/N`（先頭 4KB だけ取って読んだ）
- 権利：**米海軍の記録＝米連邦政府の著作物（PD）**。⚠️ 黒塗りの札は b(1)（国家安全保障）・b(3) 10 USC 130（技術情報）・b(6)（個人の私生活）
- 旧版＝3本目（2026-08-16 公開）が使ったのは **第1回（DocumentCloud 7216658 の OCR 版）と第9・10回（DocumentCloud 20986255 `tresher9_10_reduced`＝第9回300頁＋第10回300頁）だけ**

| 回 | 公開日 | 棚の更新日 | ファイル | 大きさ | PDF頁 | 中身（台帳の記載／本文で確かめた所は ✓） | 旧版 | 手元 |
|---|---|---|---|---|---|---|---|---|
| 1 | 2020-09-23 | 2020-09-23 | `THRESHER pg 1-300.pdf` | 28.0MB | 300 | COI 第1巻（索引・記録 pp.1-227）：索引・証人一覧・証拠一覧・**認定・意見・勧告**・最初の証言 ✓ | ✅（DC 7216658 の OCR 版 87MB） | `_thresher_raw/inquiry_vol1_p1-300.pdf`（旧版の写し）→ 文字 `src/inquiry_vol1.pages.txt` |
| 2 | 2020-10-26 | 2020-10-26 | `m_0001_1 and 2 of 3 V2 N97_Review_page 301-600 JRG_Redacted.pdf` | 54.9MB | 300 | 第1巻 pp.228-280・第2巻 pp.281-526（証言の続き） | — | — |
| 3 | 2020-11-24 | 2020-11-24 | `USS Thresher Interim Release 3.pdf` | 66.4MB | 322 | 第2巻 pp.527-558・第3巻 pp.559-846（**Rickover 中将の証言**を含む）。DocumentCloud 20417074 にも写しあり（未読・確認画面） | — | — |
| 4 | 2020-12-22 | 2020-12-22 | `… Release 4 pt 1.pdf`・`pt 2.pdf` | 5.5＋6.4MB | **未測**（線形化でない・取得が海軍側で止まった） | 第4巻 pp.847-1173（証言の続き＝記録で327頁） | — | —（途中で打ち切り） |
| 5 | 2021-01-27 | 2021-02-02 | `… Release 5 pt 1(RS)_Part1/2a/2b/2c/3.pdf`・`pt 2(RS)_Part1/2.pdf`（7本） | 計53.6MB | **未測** | 🔴 **査問会の記録ではない**：1978年の2巻本『Sea-Based Airborne Antisubmarine Warfare 1940-1977』（台帳の記載） | — | — |
| 6 | 2021-02-24 | 2021-02-24・03-01 | `… Release 6 pt 1.pdf`・`pt 2.pdf` | 225.9＋4.9MB | 148＋209 | 同上（対潜航空の歴史の続き） | — | — |
| 7 | 2021-03-24 | 2021-03-24 | `… Release 7.pdf` | 59.4MB | 328 | 第5巻（証言の続き） | — | — |
| 8 | 2021-04-20 | 2021-04-27 | `… Release 8.pdf` | 44.7MB | 220 | 第6巻・第7巻（証拠 pp.1-80）：**最後の証言（人事局長を含む）**と最初の証拠 | — | — |
| 9 | 2021-05-24 | 2021-05-28 | `… Release 9.pdf` | 180.3MB | 300 | 第7・8巻（pp.1-164）＝証拠の続き | ✅（DC 20986255 の前半） | `_thresher_raw/inquiry_9_10.pdf`→ `src/inquiry_9_10.pages.txt` |
| 10 | 2021-06-28 | 2021-06-29 | `… Release 10.pdf` | 124.9MB | 300 | 第8・9巻（pp.1-225）＝証拠の続き（**Seawolf の記録＝証拠49** ✓ 旧写しの PDF p.122-124） | ✅（同 後半） | 同上 |
| 11 | 2021-07-26 | 2021-08-03 | `… Release 11.pdf` | 49.5MB | 300 | 第9・10巻（証拠） | — | — |
| 12 | 2021-08-28 | 2021-08-26 | `… Release 12.pdf` | 105.5MB | 301 | 第10・11・12巻（証拠） | — | — |
| 13 | 2021-09-30 | 2021-10-01 | `… Release 13.pdf` | 33.0MB | 194 | 第12巻・**DOE の機密解除の指針**（海水系の継手・衝撃試験の証拠） | — | — |
| 14 | 2021-10-31 | 2021-11-03・12-02 | `… Release 14 (1 of 3)/(2 of 3)/(3 of 3).pdf` | 104.5＋10.1＋15.6MB | 34＋14＋33 | 第12巻の最後の証拠＝**査問会の記録の公開はここで終わり** | — | — |
| 15 | 2021-11-30 | 2021-12-02 | `… Release 15 pt 1.pdf`・`pt 2.pdf` | 12.8＋17.0MB | 300＋304 | **USNS Mizar の1964年の写真**（残骸の場の写真302点） | — | — |
| 16 | 2021-12-21 | 2021-12-21 | `… Release 16.pdf` | 31.0MB | 690 | 同（写真345点） | — | — |
| 17 | 2022-01-26 | 2022-02-02 | `… Release 17.pdf` | 126.6MB | 319 | 造船局（BUSHIPS）との往復文書・**1964年の残骸の場への調査の報告** | — | — |
| 18 | 2022-03-03（棚） | 2022-03-03 | `… Release 18.pdf` | 21.4MB | 203 | ✓ **上級の意見書（1st＝大西洋艦隊司令官 1963-06-12／4th＝人事局／7th＝海軍長官・最終）**・勧告への措置のまとめ・事故の要約（Summary of Events）3版・1976〜77年の APL（ジョンズ・ホプキンズ大）の残骸の場の調査。🔴 **PDF p.69 に「set at 1300 fe…」**（legend §1-h） | — | `src/navy_IR18.pdf`（md5 c7122fd9…）→ 文字 `src/navy_IR18.pages.txt` |
| 19 | 2022-08-16（棚） | 2022-08-16 | `… Release 19 (rd).pdf` | 16.1MB | 86 | Naval Reactors（原子炉部門・NR）の内部文書（NR-HA の説明）。文字層なし＝中身は未確認。USNI 2022-09-08「放射能の危険の説明」の記事は第19回か第20回を扱ったもの（どちらかは未確定） | — | — |
| 20 | 2022-09-20（棚） | 2022-09-20 | `… Release 20.pdf` | 23.1MB | 102 | ✓ NR の往復文書：Rickover の部署から市民への返信・「潜水艦の安全の設計の検討」メモ（1963-04-22）・**Rickover の声明の下書き（継手の約5%を検査し約10%が要修理＝「数百の不良継手」）**・Rickover の AP 声明（1963-04-12・放射能なし） | — | `src/navy_IR20.pdf`（md5 3a4f17fc…）→ `src/navy_IR20.pages.txt` |
| 21 | 2023-05-02（棚） | 2023-05-02 | `… Release 21_Redacted.pdf` | 6.4MB | 7 | NR の内部文書（NR-HA の説明）。文字層なし | — | — |
| 22 | 2023-05-02（棚） | 2023-05-02 | `… Release 22.pdf` | 10.3MB | 6 | 同上 | — | — |
| 23 | 2023-05-02（棚） | 2023-05-02 | `USS THRESHEr INTERIM RELEASE 23.pdf` | 7.3MB | 28 | 同上（棚で最後のファイル＝2026-09-30 時点で第24回は無い） | — | — |
| 台帳 | 2022-02-02 | — | `Running Release Inventory.xlsx` | 20KB | — | 第1〜17回の日付・中身の一覧（海軍） | — | `src/navy_running_release_inventory.xlsx`（md5 3b12cc0d…） |

- **合計の頁**：測れた回の合計＝**5,348 PDF頁**（第4回・第5回を除く）＋第4回（記録で327頁）＋第5回（未測）＝**およそ5,700頁＋第5回**。Bryant の本の案内は「6,000頁を超える記録」＝矛盾しない。うち**査問会の記録そのもの（第1〜4・7〜14回）**は PDF で約3,300頁（本文 1,718頁〈第18回 p.67 の要約〉＋証拠）
- **旧版が使っていない回**＝第2・3・4・7・8・11〜23回（第5・6回は別の本）。特に効きそうなのは **第3回（Rickover の証言）・第8回（最後の証言）・第13回（機密解除の指針）・第17回（1964年の調査の報告）・第18回（上級の意見書と要約）・第20回（NR の文書）**
- 回の番号の注意：USNI News の「○回目（round）」の記事の番号・日付は海軍の回とずれる（例：USNI「7回目」2021-04-14・「8回目」2021-04-29・「最新」2021-07-09＝第9・10回）。**正本は海軍の棚の番号**
- 写し：NR-HA（原子力推進の歴史の会）の一覧 https://www.nr-ha.org/books-sources/1963-thresher-court-of-inquiry-proceedings-release （第1〜18回を Google Drive で配布。第19〜23回は会員だけ＝海軍の棚では誰でも取れる）

## 2. ほかの一次資料・後年の公的な資料

| 記号 | 資料 | 日付 | 頁数 | URL | 権利 | 旧版 | 手元 |
|---|---|---|---|---|---|---|---|
| **S-J** | 米議会 両院原子力合同委員会（JCAE）公聴会記録『Loss of the U.S.S. "Thresher"』（第88議会 第1・2会期／1963-06-26・27・07-23、1964-07-01） | 1965 刊（USGPO） | 192 p. | Stanford Digital Repository https://purl.stanford.edu/yk130sc8375 （画像の閲覧器。検索で出る直接の PDF `stacks.stanford.edu/file/yk130sc8375/00002075_mixed.pdf` は 2026-09-30 に 404）／NR-HA の案内 https://www.nr-ha.org/books-sources/1963-&-1964---the-loss-of-the-uss-thresher-congress-testimony | 🟢 **Public domain**（Stanford の表示＝Public Domain Mark 1.0。米議会の刊行物） | — | —（取得不要の指示） |
| S-P | 国防総省の報道発表 1964-04-28（`330-PSA-99-64a/b`）・1964-10-01（`330-PSA-309-64a/b/c`） | 1964 | 各1〜3枚 | Commons（元は米海軍国立博物館の Flickr）例 https://commons.wikimedia.org/wiki/File:330-PSA-309-64a_(22791587391).jpg | 🟢 PD-USNavy | ✅ | `ref/thresher/cm_330-PSA-*`（旧版の写し）。⚠️ **説明文に本文の書き起こしが無い＝画像だけ**（サブエージェントは読まない＝②で人が原寸で読む） |
| L-N1 | NHHC（海軍歴史遺産司令部）DANFS「Thresher II (SSN-593)」（**2021-07-13 公開の書き直し版**） | 2021-07-13 | 長い1頁 | https://www.history.navy.mil/research/histories/ship-histories/danfs/t/thresher-ssn-593-ii.html | 🟢 米政府の著作物（PD・頁内の写真は個別） | — | —（curl で読んだ・保存せず） |
| L-N2 | 旧 DANFS（2004 の写し）「空気がタンクに流れ込むような音」の文がある版 | 2004 の写し | — | https://webharvest.gov/peth04/20041017005029/http:/www.history.navy.mil/danfs/t/thresher.htm （未読・検索の要約だけ） | PD | — | — |
| L-N3 | NHHC の話題の頁「USS Thresher (SSN-593)」 | — | — | https://history.navy.mil/browse-by-topic/ships/submarines/uss-thresher--ssn-593-.html | PD | — | — |
| L-S1 | NAVSEA「Thresher 59th Remembrance: SUBSAFE Program」 | 2022 | — | https://www.navsea.navy.mil/Media/News/Article/2998364/thresher-59th-remembrance-subsafe-program/ | 🟢 PD（米海軍） | — | — |
| L-S2 | NAVSEA「USS Thresher: A Loss, A Legacy」（SUBSAFE は1963年6月に始まった、の公式の説明） | 2023 | — | https://www.navsea.navy.mil/Media/News/Article/3354927/uss-thresher-a-loss-a-legacy/ | 🟢 PD | — | — |
| L-S3 | Sullivan 少将（NAVSEA）の議会証言「SUBSAFE」（下院科学委員会・2003-10-29） | 2003 | — | 公式の原本は未特定（写しは spaceref 等） | PD（議会証言） | — | — |
| **D** | Stierman, Joseph William, Jr.（**海軍少佐**）『Public relations aspects of a major disaster: a case study of the loss of USS Thresher』Boston University 広報学修士論文 | 1964-05 | 426 画像（参考文献 p.188-194） | https://archive.org/details/publicrelationsa00stie （文字版 `…_djvu.txt`・所蔵＝海軍大学院 Dudley Knox 図書館） | ⚠️ IA の権利欄は空。Commons は PD（米政府）と表示。**BU の学位論文＝職務著作かは未確定**→ 引用の範囲で使う | — | `src/stierman1964_djvu.txt`（md5 11d2c08d…）・`src/ia_publicrelationsa00stie_meta.json` |
| S-X | 米海軍の報道発表「Department of Navy Releases Records Related to Loss of USS Thresher」 | 2020-09-23 | — | https://www.navy.mil/Press-Office/Press-Releases/display-pressreleases/Article/2358204/department-of-navy-releases-records-related-to-loss-of-uss-thresher/ （WebFetch は 403＝本文は未読） | PD | — | — |

## 3. 後年の分析・報道（二次＝**帰属つき**でしか使わない）

| 記号 | 資料 | 日付 | URL | 権利 | 読んだか |
|---|---|---|---|---|---|
| **A-R** | Bruce Rule（1963年4月に SOSUS 評価センターの分析士官）の書簡「Information and Security Issues Associated with the Loss of the USS THRESHER」＝海軍作戦部次長 Breckenridge 少将あて | 2013-04-10 | https://www.iusscaa.org/articles/brucerule/letter_to_the_deputy_cno.htm | 著作権あり（個人）＝短い引用だけ | ✅（WebFetch の要約＝原文の語は legend §2 に引用） |
| P-T | The War Zone「USS Thresher's Crew May Have Survived Many Hours After Its Disappearance According To New Docs (Updated)」Thomas Newdick | 2021-07（更新 07-15） | https://www.twz.com/41523/uss-threshers-crew-may-have-survived-many-hours-after-its-disappearance-according-to-new-docs | 著作権あり | ✅ |
| P-AP | AP（David Sharp）「Skipper: Docs show no coverup in submarine sinking」（Military Times 掲載） | 2021-08-02 | https://www.militarytimes.com/news/your-navy/2021/08/02/skipper-docs-show-no-coverup-in-submarine-sinking/ | 著作権あり | ✅ |
| P-U1 | USNI News の各回の記事（初回 2020-09-23・Rickover の証言 2020-11-25・4回目 2020-12-23・2021-02-04・2021-04-14・2021-04-29・2021-07-09・放射能の報告 2022-09-08） | 2020〜2022 | https://news.usni.org/2020/09/23/navy-releases-first-tranche-of-uss-thresher-documents ほか | 著作権あり | ❌ Cloudflare の確認画面＝**読めていない**（検索の要約だけ） |
| P-U2 | Proceedings「Declassify the Thresher Data」（2018-07）／「What Did the Thresher Disaster Court of Inquiry Find?」（2021-08）／Naval History「What Killed the Thresher?」（2023-04）／Proceedings「Was the Thresher Ready for Sea?」（2023-04） | 2018〜2023 | https://www.usni.org/magazines/proceedings/2021/august/what-did-thresher-disaster-court-inquiry-find ほか | 著作権あり | ❌ 未読 |
| P-B | James B. Bryant『Rush to Disaster』Naval Institute Press（288頁・「6,000頁を超える機密解除の記録」にもとづく） | **2026-12-08 発売予定** | https://www.usni.org/press/books/rush-disaster | 著作権あり | ❌ 未刊（案内の要約だけ） |
| P-M | Military.com「55 Years After Thresher Disaster, Navy Still Keeps Secrets」（2018-04-09）／「Questions About Infamous Lost Sub Resurface…」（2021-08-14）／Legion Magazine | 2018〜2021 | https://www.military.com/daily-news/2021/08/14/questions-about-infamous-lost-sub-thresher-resurface-navy-releases-new-documents-tied-decades-old-mystery.html ほか | 著作権あり | ❌ 未読 |

## 4. 手元のファイル（`ref/ep18/src/`・計 45MB・git の管理外）

| ファイル | 中身 | 大きさ | md5（先頭） |
|---|---|---|---|
| `inquiry_vol1.pages.txt` | 第1回（旧版の写し `_thresher_raw/inquiry_vol1_p1-300.pdf`）の文字層を1頁ずつ（`=== PDF p.N ===`）。300頁・空の頁0 | 770KB | 932b25ee… |
| `inquiry_9_10.pages.txt` | 第9・10回（旧版の写し `_thresher_raw/inquiry_9_10.pdf`）の文字層。600頁・空の頁31（図や白紙） | 693KB | b73da2f0… |
| `navy_IR18.pdf`／`.pages.txt` | 第18回（海軍の棚から 2026-09-30 取得）。203頁・文字層あり（OCR）・空の頁1 | 21.4MB／337KB | c7122fd9…／5c3a12ce… |
| `navy_IR20.pdf`／`.pages.txt` | 第20回（同）。102頁・文字層あり | 23.1MB／119KB | 3a4f17fc…／1cfb93ee… |
| `navy_running_release_inventory.xlsx` | 海軍の公開の台帳（第1〜17回） | 20KB | 3b12cc0d… |
| `stierman1964_djvu.txt`／`ia_publicrelationsa00stie_meta.json` | Stierman の論文の文字版と IA の目録 | 365KB／83KB | 11d2c08d…／a655c064… |

- 道具（リポに入れない・scratchpad）：`dump_pages.py`（1頁ずつ文字層を出す）・`grepq.py`（NFKC＋空白を潰して探す）・`pg.py`（頁の文字を出す）・`navy_sizes.py`（Range で大きさと `/N`）・`redact_probe.py`（語の位置の画素の明るさを**数値だけ**測る＝画像は保存も表示もしない）

## 5. ②で足した資料と訂正（2026-09-30・18本目 ②③）

### 5-1. 手元に足したファイル（`ref/ep18/src/`・git の外・合計 **306MB**）
| ファイル | 中身 | 大きさ | md5（先頭） | 文字の取り方 |
|---|---|---|---|---|
| `navy_IR03.pdf`／`.ocr.txt` | 第3回（海軍の棚 2026-09-30）。**322頁・文字の層は0頁**（全頁が画像） | 66.4MB／937KB | 6ca3b7ff／0e6e8f14 | Windows 標準 OCR（repo `tools/ocr_win.ps1`・200dpi・灰色）。⚠️ 日本語の設定なので英文にかなのゴミが混じる＝**引用は原寸で確かめてから** |
| `navy_IR08.pdf`／`.pages.txt` | 第8回。🔴 **300頁**（§1 の表の「220」は誤り＝線形化の目安の値）。p.1〜220 は文字の層あり・**p.221〜300 は画像だけ（未 OCR）** | 44.7MB／578KB | cfaf6427／8b330013 | PyMuPDF の文字の層 |
| `navy_IR13.pdf`／`.ocr.txt` | 第13回。194頁・🔴 **文字の層は0頁**（①の「1頁目に /Font がある＝文字の層がある見込み」は外れ） | 33.0MB／289KB | 8686f870／ebd26f74 | OCR（同上） |
| `navy_IR17.pdf`／`.ocr.txt` | 第17回。319頁・文字の層は1頁 | 126.6MB／565KB | 5c6f239a／4c78a59a | OCR（同上） |
| `jcae1965_stanford.txt` | **JCAE の公聴会記録の全文**（Stanford の文字起こし `yk130sc8375.txt`＝`https://stacks.stanford.edu/file/druid:yk130sc8375/yk130sc8375.txt`・http 200）。①は「直接の PDF は 404」＝文字の版は取れた。PD（米議会の刊行物） | 649KB | 9baf6b17 | Stanford の OCR（頁ごとの ALTO も 206頁ぶんある） |
- 取り方：海軍の棚は `curl -C - --speed-limit 2000 --speed-time 60`（止まったら続きから取り直す）。第13回が1MBで止まり、第17回は1回目が2.3MBで切れた＝再開で取れた
- 取っていない：第11・12・14回（証拠の続き＝スカイラークの水中電話の記録 UQC log はここにある見込み・未確認）・第2・4・7回（証言の続き）・第15・16回（1964年のミザーの写真 302＋345点）・第19・21〜23回

### 5-2. 回ごとの中身（②で読んだ所）
| 回 | 読んだ所と中身 | 読み方 |
|---|---|---|
| 第3回 | 第2巻の終わり〜第3巻の証言。Rickover の名は OCR の文字で p.56・58・91・176・179・181。衝撃試験の証言（BuShips の Riley 大佐・証拠83＝p.3〜）ほか | 読む係A（→ §5-4） |
| 第8回 | 最後の証言の束（Guerry・Hamby・Zurcher・H. A. Jackson・Ramage 再喚問・**Frank Andrews 大佐＝1963年の捜索の指揮官 p.64〜**・Smedberg 中将＝人事局長 p.107〜・**J. Lamar Worzel＝ラモント研究所 p.169〜** ほか） | 読む係A |
| 第13回 | 造船局の書簡・衝撃試験の不具合の一覧・**ほかの艦の海水配管の故障の表**（p.141「銀ろう付けの継手が破れ、栓を打ち込んだ。作動深度の近くでは不可能だった」・p.46 建造時の試験で試験深度への最初の潜航中に銀ろう付けの継手から配管が吹き抜けた報告＝艦名は OCR で崩れる＝要原寸）。🔴 **台帳の「DOE の機密解除の指針」は OCR の文字で見つからない**（p.55 の guidance は別の文脈） | 自分で grep |
| 第17回 | p.1 NAVSHIPS の送り状／**p.81〜「NAVY ACTIONS TAKEN ON THE RECOMMENDATIONS OF THE THRESHER COURT OF INQUIRY」1965-01-08**（勧告への措置）／**p.97〜 海軍研究所の報告『Deep-Ocean Search in the THRESHER Loss Area』**（1964年の捜索の技術報告・航法・ミザーのカメラの走行・トリエステ2世・作戦命令 CTG 168.1 No.1-64・付録の写真 Plate） | 自分で grep・p.97 は原寸 |
| JCAE | 全4会期（1963-06-26・27・07-23・1964-07-01）＋付録 | 読む係B（→ §5-4） |

### 5-3. 原寸で読んだ所（人の目・このチャットの画像の枠の内）
- **第18回 PDF p.69**（§5-5 の訂正）
- **国防総省の発表 1964-10-01 No.710-64**（`cm_330-PSA-309-64a/b`）＝「recently concluded oceanographic research and development operations conducted 220 miles east of Boston」「resulted in a significant improvement of the Navy's capability to search out and inspect objects in ocean depths approaching 10,000 feet」（⚠️**1万フィートは能力の話**・現場の深さではない）「A task group consisting of the bathyscaph TRIESTE II, the cargo ship USNS MIZAR, and the salvage vessel USS HOIST, conducted the three month program utilizing the THRESHER loss area and the wreckage of the THRESHER **as a target for testing new or improved deep search and inspection ideas and equipment**」「**the most thoroughly researched ocean section in the world**」「June, July and August」「TRIESTE II spent a total of **37 hours submerged during five dives**」「Following her first dive, motor problems resulted in her return to Boston and a one-month delay」／2頁目「located portions of wreckage were covered with one to two inches of sand crust」「**a 1,200 square yard field of 900 markers**」（文字と番号の付いた2フィートのナイロン索＋重り）「TRIESTE II … 45,000 gallons of gasoline … 20 tons of iron shot … three man team」「TRIESTE I … world's deep diving record of 35,800 feet in 1960」「all of the objectives were met」「MIZAR … converted Antarctic resupply ship … adapted by the Naval Research Laboratory … towed camera-magnetometer array and the improved underwater tracking system」「HOIST … used primarily to tow TRIESTE II」。**「8,400」はこの発表に無い**
- **第17回 PDF p.97 の要旨**（1964年の海軍研究所）＝「June-August 1964. Task Group 168.1, consisting of USNS MIZAR and a U.S. Naval Research Laboratory team, the USS PRESERVER, and the research vehicle TRIESTE II」「succeeded in photographing, as far as appears possible, **all of the THRESHER hulk pieces still visible above the ocean floor**」「the hulk has broken into **five or six large pieces**, and many small pieces, with all major debris lying in an area certainly no greater than **a circle of diameter 400 yd**」「TRIESTE II … was able to locate on top of a portion of the THRESHER hull, thus providing an opportunity for **close inspection by human eyes**」「exploration and study of the ocean floor by use of an unmanned vehicle which is remotely controlled and towed from a surface ship is extremely effective」
- ⚠️ **1964年の曳航艦が割れる**：発表＝HOIST／海軍研究所の要旨＝PRESERVER（1963年はフォート・スネリングとプリザーバー＝第17次 PDF p.105 の OCR）＝台本で艦名を言うなら出典を添える

### 5-4. 読む係の報告（scratchpad・自分で要所を原文に当て直した）
- 係B（JCAE）＝報告 `reading_B_JCAE.md`（約33万トークン・約20分）。**要所14か所を自分で grep して全部あった**：Rickover「I do not know.」（p.89）・「several hundred substandard joints」の計算＝**約5%を検査・約10%が要修理**（p.68・元は1963-04-29 の査問会の非公開の証言の読み上げ）と Holifield「Our figure on this is 14 percent」・前艦長の評価書「the most dangerous condition that exists in Thresher is the danger of salt water flooding while at or near test depth」（p.20）・深い所での全力の吹き出し「it never has been done」（p.38）・こし器は「We don't believe they were」（外していなかったとみられる・p.112）・試験深度の数は「just on the basis of cost」（p.122）・「there is not a tactical justification」（p.124）・SUBSAFE の元＝「June 3, 1963, directed the establishment within the Bureau of a submarine safety program」（p.97）・潜水艦安全センター 1964-02-18（p.94）・トリエステは1963年に「a total of 10 dives」・1963-08-28 に真鍮の管を回収（p.169）・「no part of Thresher's pressure hull was sighted or photographed」（p.169・1964-02 の資料）・「the Thresher is a warning made at great sacrifice of life」（p.127）
- 係A（第3回・第8回）＝報告 `reading_A_R03_R08.md`（約37万トークン・約23分）。**第8回（文字の層）の要所11か所を自分で grep して全部あった**：捜索の指揮官 Andrews「imagine being up in an airplane 8500 feet high with a string and a camera on the end of it」（R08 p.66）・「I advised him that he must resist that pressure」（p.77＝新艦長への助言）・「three Executive Officers since commissioning in August, 1961」（p.70）・人事局長 Smedberg「the pressure placed on the Bureau of Naval Personnel to furnish experienced commanding officers for the POLARIS submarines」（p.107）・元設計部長 Jackson「this would not be prudent」（p.33＝深い所の全力の吹き出しの試験）・意見45「no normal main propulsion power available until after the 7.1 minutes」（p.212）・認定80「ten thousand pound charges at ranges varying from 1180 feet to 370 feet」（p.194＝**第1回では塗られている数が第8回では読める**）・ティノサ「clogging of the strainers with frost and ice」（p.175）・Worzel「approximately 1500 photographs」「it was indeed our camera weight」（p.170〜171）・「dropping of the submarine hull TORO」（p.67＝第17次 PDF p.250 に TORO (SS 422) を試験の標的に沈める決定）。第3回は OCR＝**Rickover の証言は PDF p.165〜185（記録 690〜709・1963-04-29・p.168 から非公開）**・衝撃試験 Riley 大佐 p.2〜13（キーウェスト沖・水深約300フィート・潜望鏡深度・6発・日付は認定79 と月が割れる）・Hecker 以外の「9時13分」の文面・「約5%を検査・約10%が要修理」（p.169）＝どれも原寸で確かめてから使う
- ⚠️ 係A の頁の対応：R03 の記録 p.≒PDF p.＋525（p.34〜211）／R08 の記録 p.＝PDF p.＋1498。**R08 p.181〜220 に認定・意見・勧告が再録**（V1 p.＝R08 p.−147）＝V1 より塗りが少ない所がある
- ⚠️ 査問会の閉廷＝1963-06-05 09時21分（R08 p.180）。最後の証言は6月1日の Heller 大佐（Smedberg は最後ではない）

### 5-5. 🔴 ①の判定の訂正（legend の本文は①の記録として残し、ここに直しを書く）
| ①の判定 | ②で分かったこと | 直した判定 |
|---|---|---|
| legend #25・L8：第18回 p.69 の「1300」は**塗られておらず、白塗りが右にずれた塗り損じ**（画素の実測） | 🔴 原寸で見ると、**見える頁は「the depth of which had been set at b(1)［白い空白］. During the」＝1300 は見えない**。絵のインクは x=70〜352pt に「a deep dive, the depth of which had been set at」、352〜415pt が白塗り。**文字の層（見えない OCR の文字）は同じ文を70〜313pt に縮めて持ち、その右に「1300 fe」を残す**＝塗りの箱は絵の「1300 feet」を正しく消したが、文字の層では別の語（et. During th）を消した。①の画素の測定は**文字の層の座標**で測ったため、実際は絵の「set at」の上を測っていた | **見える頁では「消えている」＝旧版 c103 の言い方は一致**。1300 は**見えない文字の層の塗り残し**（推測：OCR を塗る前の絵で作った）。🔴 **台本で「海軍の公開文書に1300フィートと出ている」とは言わない**。数を言うなら帰属＝Rule（2013）・Friedman（AP 2021）・JCAE の付録の新聞の推測は「約1,000フィート」 |
| legend #20・#9 ほか：「8,400フィート」は査問会側の文字で**見つからない** | 🔴 **ある**：第1回 PDF p.147（問い「in approximately 8400 feet of water」）・**p.183（査問会の長の問い「if that submarine is in 8400 feet of water?」→ スカイラーク艦長 Hecker 少佐「None, sir. … I could not even plant a buoy.」＝記録 p.110・1963-04-15）**・第3回 OCR p.166（問い）・JCAE の海軍長官の発表（1963-06-20「She came to rest on the ocean floor, 8,400 feet beneath the surface」）・1964-02 の資料・1963年の写真の説明文（330-PSA-110-63）・ユニバーサル・ニュース映画の説明書き・Stierman が引く新聞の見出し「Crushed 8400 Feet Down」 | **割れる数**＝認定14 と法務総監の要旨は「about 8,500 feet」／海軍の1963年の発表と問いは「8,400 feet」。**メートルではどちらも約2,600メートル**（2,560〜2,591）＝台本は「約2,600メートル」で割れを避けられる |
| legend #23：1964-10-01 の発表の本文は**未照合** | 原寸で読んだ（§5-3）＝旧版の「220マイル・6〜8月・トリエステ2世／ミザー／ホイスト・5回で計37時間・電動機の不調で1か月遅れ・試験の標的・世界で最も徹底的に調べられた海」は**一致**。ただし旧版の「約1万フィート」は**能力の話**（現場の深さではない） | **一致**（1万フィートの言い方だけ注意） |
| legend §4-1：第13回に「DOE の機密解除の指針」（試験深度の扱いが書いてあるかも） | OCR の文字で見つからない | 未解決（画像だけの頁の OCR の崩れの可能性は残る） |
| sources §1：第8回 300頁のところ「220」・第13回「文字の層がある見込み」 | 300頁・文字の層は0 | 上の §5-1 のとおり |
