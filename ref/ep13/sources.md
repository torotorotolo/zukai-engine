# 13本目（トルコ航空981便・1974-03-03）── 一次資料の台帳

**取った日＝2026-09-23（②③のチャット）。**置き場＝`ref/ep13/src/`。
⚠️ リポの `.gitignore` が `ref/*` を無視しているので、**PDF・本文テキスト・画像はコミットしない**（この台帳の URL と md5 で取り直す）。コミットするのは台帳と照合の記録だけ（`git add -f` で名指し）。

照合の記録（主張ごとに 判定・頁・原文の短い引用）：
- [facts_paris.md](facts_paris.md) … 仏の最終報告（原文＋英訳）で照合した A1〜A15
- [facts_us.md](facts_us.md) … 予兆（1970・1972）・紳士協定・SB・AD を上院資料と NTSB で照合した B1〜B11
- [facts_japan.md](facts_japan.md) … 国会会議録で照合した日本側 C1〜C6

---

## 0. 読み方（まずここ）

1. 🔴 **正本の順位＝仏の最終報告の原文（S1・付属書つき）＞英訳（S2・付属書は訳されていない）＞米上院の委員会資料（S6）＞NTSB（S4）＞FAA のまとめ（S17＝二次）。**
2. 🔴 **FAA のまとめ（S17）には誤りが4件**（負傷者「0」→ NTSB は軽傷11人／「Windsor-Locks」→ ウィンザー（オンタリオ州）付近／「パリの約1年前」→ 約21か月前／AD の SB の並べ方）。**数字の出典にしない。**（facts_us.md 別表1）
3. ⚠️ **報告書の中で数字が割れているものが5件**（乗客334／333・オルリーで乗った217／216・離陸 11:30:30／11:32 UTC・減圧から衝突まで約77秒／約70秒・高度 約11,500ft／約12,000ft）。④で1つに決め、画面にはその出典を出す（facts_paris.md）。
4. ⚠️ 報告書の時刻は **UTC**。現地（パリ）は **UTC＋1**（報告書の注で明記）。
5. ⚠️ 仏語原文（S1）の文字の層は BEA の2005年の電子化の OCR で、**音声記録（CVR）の頁などは崩れている**。「文字で検索して0件」は「原文に無い」ではない（例：英訳にある副操縦士の言葉 "the fuselage has burst" が、仏語の文字の層では0件）。**決め所は頁の画像で読む。**

---

## 1. 取得ずみ（1件1行）

| # | 資料 | 取った URL（http） | 保存名 | 大きさ・頁 | md5 | 文字 | 画面に出すときの権利 |
|---|---|---|---|---|---|---|---|
| S1 | 🔴 **仏の最終報告（原文・付属書つき）**。Secrétariat d'État aux Transports, Commission d'enquête「Rapport final … accident survenu le 3 mars 1974 en forêt d'Ermenonville au DC-10 TC-JAV des Lignes aériennes turques」1976年2月。頁の上に `BEA REF: BEA tc_v740303`（BEA が2005年に電子化） | https://www.faa.gov/sites/faa.gov/files/2022-10/FinalAccidentReportinFrench.pdf（200） | `faa_FinalAccidentReportinFrench.pdf` | 6,069,902 B・158頁 | `1854311b962d2b90b9fa65c7ea0b5f57` | 層あり（仏語の当たり 0.232）・一部崩れ | 仏国（BEA）＝PD でない → **引用**（額装・改変しない・出典） |
| S2 | **英訳**＝英国 Department of Trade, Accidents Investigation Branch「Turkish Airlines DC-10 TC-JAV. Report on the accident in the Ermenonville Forest, France on 3 March 1974」（Aircraft Accident Report 8/76・HMSO）。p.2「Translation of the Report published by the French Secretariat of State for Transport／**No Appendices were published**／February 1976」 | https://assets.publishing.service.gov.uk/media/5422eedde5274a1317000247/8-1976_TC-JAV.pdf（200） | `aib_8-76_TC-JAV.pdf` → `aib_8-76_TC-JAV.ocr.txt` | 5,682,439 B・55頁 | `5a6b28d9730dd8677aad5f04dc59f945` | 画像のみ → Windows OCR 220dpi（英語の当たり 0.301＝良） | 英 Crown copyright（gov.uk は OGL v3.0）・中身は S1 の訳 → **引用**で扱う |
| S3 | 英訳の別スキャン（FAA 保管） | https://www.faa.gov/sites/faa.gov/files/2022-10/FinalReportinEnglish.pdf（200） | `faa_FinalReportinEnglish.pdf` | 3,645,149 B・55頁 | `74bde7acde22fe69a649ec277417ea80` | 一部だけ層あり | S2 と同じ |
| S4 | **NTSB AAR-73-02**「American Airlines, Inc., McDonnell Douglas DC-10-10, N103AA, near Windsor, Ontario, Canada, June 12, 1972」（1973-02-28 採択） | https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR7302.pdf（200） | `ntsb_AAR73-02_N103AA.pdf` → `.ocr.txt` | 5,409,377 B・43頁 | `61163392a57e1f4d078cede05d7c1660` | 画像のみ → OCR（当たり 0.162＝崩れ） | 米連邦 §105＝**PD（根拠A）** |
| S5 | 同じ報告書（ERAU 所蔵）。**FAA 保管の `Windsor-LocksReportAAR73-02.pdf` と md5 が一致＝同一ファイル** | http://libraryonline.erau.edu/online-full-text/ntsb/aircraft-accident-reports/AAR73-02.pdf（200）／https://www.faa.gov/sites/faa.gov/files/Windsor-LocksReportAAR73-02.pdf（200） | `ntsb_AAR73-02_N103AA_erau.pdf`／`faa_Windsor-LocksReportAAR73-02.pdf` | 1,687,290 B・45頁 | `c7f88665f93e06d0852b531f86cf4a86` | 一部だけ層（0.208） | PD（A）。⚠️ **p.17 ほかに手書きの丸・下線**＝紙面に出すなら S6 の再録を使う |
| S6 | 🔴 **米上院 商業委員会（委員長 Warren G. Magnuson）航空小委員会「Report on the oversight hearings and investigation of the DC-10 aircraft」**（93d Congress・Committee Print・1974年6月）。NTSB 報告の本文・SB 52-37・FAA の電報・証言（マクゴーエン社長ほか）を再録 | https://www.govinfo.gov/content/pkg/CPRT-93SPRT33379O/pdf/CPRT-93SPRT33379O.pdf（200） | `senate_cprt93_dc10.pdf` | 30,505,630 B・62頁 | `9338a0f328911e7131221d06ca71984b` | 層あり（0.340＝良）。12頁は層なし（表紙まわり・巻末） | **PD（A）** |
| S7 | FAA AD 74-08-04（R4）＝パリの事故のあとの耐空性改善命令（電報で 1974-03-07・03-22 発効） | https://www.faa.gov/sites/faa.gov/files/2022-10/AD74-08-04.pdf（200） | `faa_AD74-08-04.pdf` | 48,137 B・5頁 | `c796ba81a93a095b75131338ab250b73` | 層あり | PD（A） |
| S8 | FAA AD 74-12-07（R1）＝SB 5本（1974-07-06 発効） | https://www.faa.gov/sites/faa.gov/files/2022-10/AD74-12-07.pdf（200） | `faa_AD74-12-07.pdf` | 26,386 B・2頁 | `57fdb2bc7fa468c20a8f357943dd8e98` | 層あり | PD（A） |
| S9 | FAA AD 75-15-05（R1）＝床が20平方フィート（約1.86㎡）の穴でも崩れないように（DC-10・L-1011・747・A300／1975-08-11 発効） | https://www.faa.gov/sites/faa.gov/files/2022-10/AD75-15-05.pdf（200） | `faa_AD75-15-05.pdf` | 29,303 B・3頁 | `994724a6fee2b7ca1b0d482fe413d6c9` | 層あり | PD（A） |
| S10 | 官報 Federal Register 1974-04-02 pp.11992–11999（AD 74-08-04 の公示） | https://archives.federalregister.gov/issue_slice/1974/4/2/11992-11999.pdf（200） | `fr_1974-04-02_11992.pdf` | 2,225,479 B・8頁 | `65371586bffbd1dede32dbbb169501d9` | 層あり（日付の OCR 崩れ2件＝facts_us.md 別表2） | PD（A） |
| S11 | SB 52-27（ダグラス・1972-05-30＝ウィンザーの前） | https://www.faa.gov/sites/faa.gov/files/2022-10/SB52-27.pdf（200） | `faa_SB52-27.pdf` | 2,352,876 B・11頁 | `a10207b3a7591cfa4d3054dee4173bef` | **画像のみ・未 OCR** | ダグラス社の文書（FAA が掲載）→ 引用 |
| S12 | SB A52-35（**のぞき窓**。日付は資料で 6/16 と 6/19 に割れる） | https://www.faa.gov/sites/faa.gov/files/2022-10/SBA52-35.pdf（200） | `faa_SBA52-35.pdf` | 283,758 B・3頁 | `065fec97c7559a2f033531039253cf84` | **画像のみ・未 OCR** | 引用 |
| S13 | SB 52-37（**support and plate**＝支持板・ストライク・プレートの交換・ピンとスイッチの調整。1972-07-03／改訂1 08-05／改訂2 08-25）。🔴 **のぞき窓は入っていない** | https://www.faa.gov/sites/faa.gov/files/2022-10/SB52-37.pdf（200） | `faa_SB52-37.pdf` | 4,029,437 B・9頁 | `9c57b7340e4b24249377a55828dc7de1` | 層あり | 引用 |
| S14 | SB 52-38 | https://www.faa.gov/sites/faa.gov/files/2022-10/SB52-38.pdf（200） | `faa_SB52-38.pdf` | 4,968,479 B・11頁 | `8a0529ae6f9f2161aaddfe80ff726648` | 層あり | 引用 |
| S15 | FAA Advisory Circular 25.783-1 | https://www.faa.gov/sites/faa.gov/files/2022-10/AC25.783-1.pdf（200） | `faa_AC25.783-1.pdf` | 459,713 B・5頁 | `0220f3777824f5d382538fac72966dbe` | 層あり | PD（A） |
| S16 | FAA Transport Airplane Directorate Memorandum | https://www.faa.gov/sites/faa.gov/files/2022-10/Transport_Airplane_Directorate_Memorandum.pdf（200） | `faa_Transport_Airplane_Directorate_Memorandum.pdf` | 545,024 B・4頁 | `e8ad306db29c37416c6fe968313270ba` | 層あり | PD（A） |
| S17 | FAA Lessons Learned「McDonnell Douglas DC-10（TC-JAV）」のページ（**二次資料**・S1〜S16 の置き場の入口） | https://www.faa.gov/lessons_learned/transport_airplane/accidents/TC-JAV（WebFetch は 403／curl に User-Agent と Referer で 200） | `faa_ll_TC-JAV.html`・`.txt`・画像25点 `faa_img/` | 170,479 B | `31046810bb657f9484df0168ceb27f94` | — | 本文は PD（A）だが誤り4件。🔴 **写真の多くは「© BEA France – used with permission」「© Marc Neumann／Marc Lehmann／O. Ferrante／George W. Hamlin – used with permission」＝ルール§2-6c で画面に出さない**（`faa_img/` は照合用） |
| S18 | 国会会議録（1974年「トルコ航空」21件・発言全文） | https://kokkai.ndl.go.jp/api/speech?any=トルコ航空&from=1974-03-01&until=1974-12-31&recordPacking=json | `kokkai_1974_turkish.json` | 44,958 B | `d0c9d074a054b839051f7acab6bb1b18` | — | 国会での演説＝著作権法40条（利用自由）。発言者・日付・会議名を出す |
| S19 | 🔴 **国会会議録（追加）**＝照合役が検索51本＋会議単位21件で取った（引用した63発言の全文・関係する284発言）。**1974-03-04 運輸大臣の団体の内訳（#33）**・**1976-06-09 ロッキード特別委員会の三井物産顧問の宣誓証言（#63・#172・#236・#246・#248）**・1972-03-24 の「29番」の名指しを含む。⚠️ S18 の21件は「トルコ航空」を含む発言だけで、**直後の政府答弁が抜けていた** | 同 API（語と期間は facts_japan.md の記録） | `kokkai_extra.json` | 887,043 B | `f6fc7029888238417695c38a8c366ad4` | — | 同上（証人の証言も国会での陳述） |

---

## 2. 探したが取れていない／無い（「無い」は「ここに無い」）

| 探したもの | 結果 | 次にやるなら |
|---|---|---|
| 米下院 州際・外国通商委員会 特別調査小委員会の公聴会「Review of procedures and policies of FAA and NTSB with respect to DC-10 cargo doors」（1974-03-27・04-09） | 書誌だけ確認（UNT の目録 mocat 976-08901）。HathiTrust の検索は機械では0件＝**未取得** | 上院資料（S6）で骨は足りる。④で要れば HathiTrust の全文表示を人が探す |
| 🔴 **アップルゲートのメモ**（コンベア社・1972-06-27） | **PD の置き場は無い。** 公になったのは事故後の訴訟の中（NYT 1975-03-12, R. Witkin「Engineer's Warning on DC-10 Reportedly Never Sent」）。全文は Fielder & Birsch 編『The DC-10 Case』（SUNY Press, 1992）p.165〜（Wikipedia「Dan Applegate」の出典表示による・**未入手**）。S1〜S17 の全テキストで「Applegate」「Convair」は **0件** | 🔴 **本（原文）を取るまで台本にも画面にも出さない**（孫引き禁止＝記憶 `feedback-secondhand-numbers-differ-from-the-original`）。使うなら④で本の該当頁を取る |
| 1969年の故障モード影響解析（FMEA） | S1〜S17 で **0件** | 使わない（出典が取れない） |
| NARA：米国務省の電報 `1974ISTANB00567`（1974-03-04・naId 110858748）／`1975PARIS27829`（1975-10-25・naId 110858584） | 題だけ見た・**未読** | 事故直後の米側の記録。④で要れば読む |
| SB 52-27・SB A52-35 の本文 | 画像のみ・**未 OCR** | 紙面として見せるだけなら OCR 不要 |
| 事故の記録映像 | **無い**（materials.md §4） | — |

---

## 3. 道具（再現用・`ref/ep13/probe/`）
- `fetch_src.py` … S1〜S6 と国会会議録を落として文字を抜く
- `ocr_src.py` … 画像だけの PDF を Windows 標準 OCR（`tools/ocr_win.ps1`）で読む（220dpi・グレー）
- `commons13.py`（`cats`／`pull`）・`net13.py` … Commons の網（権利→大きさ→撮影年）
- `footage13.py` … NARA・archive.org・Commons の動画
- `sheet13.py` … 640px のシート（2列×3行）

## 関連
- 素材の台帳＝[materials.md](materials.md)／尺と章立て＝[kousei.md](kousei.md)
- Vault `Projects/引き継ぎ-事故検証-13本目-20260923-②素材③尺.md`
