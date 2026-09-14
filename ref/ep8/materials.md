# 8本目（コロンビア号）の素材 ── ②の実測

**2026-09-14 に測った。**①の「候補N点」を全部測り直した版。
数字の正本はここ。台帳の JSON は `analytics/materials/ep8_*.json`。

> ⚠️ **ここに出る点数は「候補」であって在庫ではない。**
> 網（MUST／NG）は絞る道具であって選ぶ道具ではないので、⑤bで
> `python tools/nasa_probe.py list <db> --key <key> --slot <欄>` を**1行ずつ読んでから採る**。
> → [[feedback-inventory-is-not-usable-material]]

---

## 0. 🔴 結論（先に書く）

| | 数 |
|---|---|
| 2003年・幅1280以上の写真（3つの出どころ・重複を潰した） | **1,006点** |
| うち NASA 画像庫（`images.nasa.gov`）＝中央値 **3000px** | 847点 |
| うち archive.org の NASA 束（`humanspaceflightcollection`）＝一律 **1536px** | 177点 |
| 動く映像 | **9本**（うち**実効で幅1280以上は2本**）＋ archive.org の NASA 動画 **60本以上**（256〜400px） |
| 一次資料 | CAIB Vol.I 248頁・**1,111,856字**（`ref/ep8/CAIB_vol1.pdf`・10.3MB） |

### 🔴 ①からの訂正が3つある

1. **「幅1280以上の動く映像が3本」→ 実効では2本。**
   `fdcomm`（器は1280×720）は40コマ全部が **984px**、`sts1` は **948px**。
   4:3の絵を16:9の黒帯で埋めたもので、**器の札は絵について嘘をつく**
   → [[feedback-container-labels-lie-about-the-picture]]
2. **「CAIB の衝突試験の映像が見つからない」→ 見つかった。**
   `archive.org` の `humanspaceflightcollection`（NASA の旧 spaceflight.nasa.gov の保存）に
   **`HSF-mov-mlgd5oblique / side / side2 / side3` の4本**（2003-05-14・SwRI・256〜400px）。
   さらに**試験の写真が 1536×1017 で7点**（`jsc2003e40558` ほか・6月6日のRCC板）。
3. **「打ち上げ81.7秒の追跡カメラ映像が見つからない」→ 動画は無いが、コマが2点ある。**
   `KSC-03pd0242`（2254×2646）と `KSC-03pd0243`（3000×2458）。
   キャプションに「**At approximately 81-82 seconds after T-0**」と書いてある NASA 公式のコマ。
   ⚠️ **動画そのものは今日の探索では出なかった**（§4 の未達）。

🔴🔴 **いちばん大きい発見＝`images.nasa.gov` を全部当たっても 0件だった素材が、
archive.org の NASA 束には在った。**「NASA の画像庫を当たった」は「NASA の画像を当たった」ではない。

---

## 1. NASA 画像庫（`images-api.nasa.gov`）── 2003年に絞って850点

道具＝`tools/nasa_probe.py`（この回で新設）。台帳＝`analytics/materials/ep8_nasalib.json`。

- 検索語7本（`STS-107` / `Columbia debris` / `Columbia reconstruction` / `Columbia accident` /
  `Columbia Debris Hangar` / `Columbia crew` / `Columbia launch 2003`）を `year=2003` で当て、
  `nasa_id` で重複を潰して **850点**。
- **850点ぜんぶ実寸を測った。幅1280以上は 847点**（中央値 **3000px**・最大 3975px）。
  測り方＝原本 JPEG の先頭192KBだけ Range で取って SOF マーカーから w×h を読む。

### ⚠️ この束の構造（読んで分かったこと）

| 欄 | 網が拾った数 | 読んだ結果 |
|---|---:|---|
| 🔴 衝突のコマ | **2** | ✅ 本物（`KSC-03pd0242` `KSC-03pd0243`） |
| 打ち上げ（機体が写る） | **20** | ✅ 本物。「Spewing flames…」「hurtles through a perfect blue Florida sky」 |
| 射点・搬出（機体が地上に） | **29** | ✅ 本物。Rotating Service Structure のロールバックなど |
| 乗員（KSC 到着） | **10**〜75 | ✅ 本物。「waves to spectators as he arrives at KSC」 |
| 🔴 格納庫の再構成 | **395** | ✅ 本物。RLV Hangar・Reconstruction Project Team。**余るほどある** |
| 残骸がトラックで着く | **6** | ✅ 本物（Barksdale 空軍基地から KSC へ） |
| CAIB の視察・会見 | **143** | ✅ 本物（Gehman 委員長の KSC 視察・2月12〜13日） |
| 東テキサスの捜索（野外） | 6 | 🔴 **読むと全部が格納庫の写真＝実質0点**（`field` が地名に当たっていた） |
| 再突入・空中分解 | 56 | 🔴 **読むと全部が2月12日以降の CAIB 視察＝0点** |
| 衝突試験 | 22 | 🔴 **読むと全部が Return to Flight のタイル取り付け作業＝0点** |
| 軌道上（機内） | 12 | 🔴 **読むと STS-118 など別ミッション＝0点** |

**＝ NASA 画像庫の2003年コロンビア関係は、ほぼ「KSC で撮られた写真」だけ。**
打ち上げ・乗員の到着・格納庫の再構成・委員会の視察は潤沢。
**軌道上・再突入・東テキサスの野外・衝突試験は1点も無い。**

### ⚠️ 網の作り直しで直した2つ（`ref/ep8/slots_nasa.json` に記録）

1. **題名が資産IDだった。** 850点のうち **543点（70%）は `title` が `KSC-03PD-0436` そのもの**で、
   写真の説明は `description` に入っている。Commons と構造が違うので
   「題名だけに当てる」を機械的に守ると**本物が全部落ちる**。
   → `nasa_probe.py` の `caption()`＝題名がIDのときだけ説明文を見る。
2. **短い語の部分一致。** `iss` が `mission` に当たって850点中366点を拾った。
   → 語境界（`(?<!\w)…(?!\w)`）で当てるようにした。7本目の `"ft"` が `left`/`shift` に
   当たったのと同じ型 → [[feedback-verify-your-own-instrument]]

---

## 2. archive.org の NASA 束（`humanspaceflightcollection`）── 1536px で298点

台帳＝`analytics/materials/ep8_nasa.json`（key `ep8ia`）と `ep8_ia2.json`（key `ep8ia2`）。
**NASA の旧 spaceflight.nasa.gov を保存した束。`images.nasa.gov` には入っていない写真がある。**

- 671点＋54点を拾い、うち**2003年は298点**。実寸は **一律 1536px**（長辺）。
  **幅1280以上は 177点**（動画55本は静止画の実寸が取れないので別勘定）。

### 🔴 ここにしか無いもの

| 中身 | 例 | 実寸 |
|---|---|---|
| 🔴 **CAIB の衝突試験の写真** | `jsc2003e40558` `40560` `40593` `40715_nr` `40732_nr` `40735_nr` `40736_nr`<br>「a Space Shuttle thermal protection panel made of Reinforced Carbon Carbon (RCC) **impacted by foam**」（2003-06-06） | **1536×1017** |
| 🔴 **試験体の組み立て** | `jsc2003e36299` `36302` `36303` `36305` `36306` `36309` `36310` `36311`<br>「technicians … assemble a test article to simulate the inboard leading edge」（2003-05-14・JSC） | **1536×1015** |
| 🔴 **東テキサスの捜索（野外）** | `jsc2003-00151`「Volunteer searchers … **systematically scour a Navarro County field**」<br>`jsc2003-00119/00120` Corsicana の集合前の説明／`00127` 森林局の捜索者<br>`00129`〜`00132` 食堂テント・給食車／`jsc2003e29065` 食事の列<br>`jsc2003e26420` JSC所長が捜索に加わる／`jsc2003e28823` `28831` 宇宙飛行士と森林局の地図 | **1536×1017** |
| 🔴 **掘り出された主エンジン** | `jsc2003e28147`（掘る前の記録写真）`28148` `28149`「Main Engine powerheads found on the grounds」 | **1536×1024** |
| 🔴 **Barksdale 空軍基地の格納庫** | `jsc2003e14383`「debris … in the hangar at Barksdale Air Force Base」`14384`〜`14387`（長官の視察） | **1536×1088** |
| 🔴 **証拠置き場（Corsicana）** | `jsc2003e28845` `28846` `28847` | **1536×1017** |
| 🔴 **軌道上の乗員（本人たちが撮った）** | `sts107-301-005/025/028`（アンダーソン）／`sts107-399-001/003/004/006/036`（クラーク・ハズバンド・ブラウン）／`sts107-401-006` `402-012/018/030`／**`sts107-735-032`＝7人が浮いている恒例の記念写真** | **1536×1024** |
| **記録装置（OEX レコーダ）** | `s88-44993`「an OEX recorder similar to the recorder that flew aboard…」 | 1536×1536 |
| 上昇中の合成画像 | `jsc2003e06822`「two composite images of Columbia during ascent on STS-107」 | ⚠️ 1168×888（1280未満） |

### 動く映像（`HSF-mov-*`）── 56本以上あるが**全部 400px 以下**

| key | 中身 | 実寸 |
|---|---|---|
| `mlgd5oblique` `mlgd5side` `mlgd5side2` `mlgd5side3` | 🔴 **CAIB の衝突試験**（2003-05-14・SwRI・主脚扉に断熱材を当てる） | .mov 256×192／.ogv **400×300**／512kb.mp4 320×240 |
| `sts107fd01a` `fd01b` `fd01c` | 打ち上げ日（搭乗・ホワイトルーム退避・**2分間の打ち上げ映像**） | 同上 |
| `sts107fd02a`〜`fd15*`（計50本前後） | 軌道上の各日（実験・シャロン首相との交信・記者会見・食事） | 同上 |
| `husband` `mccool` `chawla` `anderson` `brown` `clark` `ramon` | 🔴 **乗員1人ずつの紹介映像（打ち上げ前に作られたもの）** | 同上 |

⚠️ **同じ内容の高画質版が `archive.org` の `STS-107_Flight-Day-Highlights` に在る**
（飛行日ごと15本・**mp4 854×480**／MXF 1280×720）。ただし **MXF は1本 5〜18GB** なので現実的でない。
**854×480 も1280未満なので、どちらにせよ全画面では使えない＝額装パネル。**

---

## 3. 動く映像9本（落としてある：`ref/ep8/vid/*.webm`・合計918MB・全点PD）

実測の表は [kousei.md](kousei.md) §3。要点だけ再掲：

- **SAR は9本とも 1:1**（7本目の SAR 10:11 のような横のふくらみは無い）。
- **9本とも音声トラックあり → 切り出しに `-an`。**
- 実効の幅で1280以上は **`mct`（1918px）と `tank`（1280px）の2本だけ**。
- `guncam` は0〜9秒、`sts1` は0〜10秒が**表紙で使えない**。
- ショットの境目は `analytics/materials/ep8_shots.json`（`tools/shots.py` で1秒刻み）。

出どころ・権利・URL は `ref/ep8/vid/sources.json`（Commons の `extmetadata` をそのまま保存）。

---

## 4. 一次資料

| 資料 | ページ | 文字層 | 図版 | 入口 |
|---|---:|---:|---|---|
| **CAIB Vol.I**（2003-08） | 248 | **1,111,856字** | 🔴 **中央値142px・最大825px・幅1280以上0点** | `https://s3.amazonaws.com/akamai.netstorage/anon.nasa-global/CAIB/CAIB_lowres_full.pdf` |

- ⚠️ `nasa.gov/wp-content/uploads/2023/03/caib-report-volume1.pdf` は **404**。
  `govinfo` の `GPO-CAIB-VOL1.pdf` は **4ページのスタブ**（①が確かめた。今回は試していない）。
- 🔴 **実測した図版の大きさ**（`PyMuPDF` の `extract_image`）：
  - p.59（衝突のコマ 図3.4-1 / 3.4-2）＝ **156×146 と 149×149**。使えない。
  - p.82（パネル8の穴 図3.8-9）＝ **522×825**。この報告書でいちばん大きい図版。
  - → **図は日本語で描き直す前提**（7本目の NIST NCSTAR と同じ）。
- ページ番号は **PDFのページ＝報告書のページ**（ずれ0）。抜き出した本文は
  `PyMuPDF` で1ページ1ファイルに落とせる（この回は作業用の一時領域に置いた）。

### ④が使う主な節

| 節 | 頁 | 中身 |
|---|---:|---|
| 2.3 Launch Sequence | 32 | 81.7秒／81.9秒／破片の大きさ・速さ |
| 2.5 Debris Strike Analysis and Requests for Imagery | 37 | 3回の要求 |
| 2.6 De-Orbit Burn and Re-Entry Events | 38 | 再突入の時刻表 |
| 3.4 Image and Transport Analyses | 59 | カメラ E212（27km）・E208（42km） |
| 3.8 Impact Analysis and Testing | 78 | 衝突試験・パネル8の穴 |
| 6.3 Decision-Making During the Flight of STS-107 | 140 | 🔴 c5 の本体 |
| 6.4 Possibility of Rescue or Repair | 173 | 🔴 c6 の本体 |
| 7 / 8 Organizational Causes / History as Cause | 178 / 195 | c9 |
| 10.2 Crew Escape and Survival | 214 | ⚠️ ④で扱う範囲を決める |

---

## 5. ⚠️ 未達・確かめていないこと

1. 🔴 **打ち上げ81.7秒の追跡カメラの「動画」は、今日の探索では出なかった。**
   当たった先＝`images.nasa.gov`（`media_type=video` で7語・全部0件）／
   `archive.org`（8通りの検索式）／Commons（6通り）。
   **静止画のコマ2点（2254px・3000px）で代替できる**ので、④は図と静止画で組む前提。
   まだ当たっていない先＝NTRS（報告書の付録の動画）・CAIB Vol.II〜VI の付録。
2. **CAIB Vol.I の高解像版・Vol.II〜VI の付録は未取得**（①からの持ち越し）。
3. **NASA Crew Survival Investigation Report（2008）は落としていない。**④の判断待ち。
4. **`STS-107_Flight-Day-Highlights` の MXF（1280×720）は落としていない**（1本5〜18GB）。
   どうしても全画面が要るカットが出たら、⑤bでその1本だけ取る。
5. **網の当て方は完璧ではない。** 上の §1 の表のとおり、
   `debris_field` `reentry` `test` `orbit` の4欄は網が別物を拾っていた。
   ⑤bで欄ごとに `list` を読むこと（**読めば分かる。読まないと分からない**）。

---

## 関連
- [kousei.md](kousei.md) — 章立てと尺
- `analytics/materials/ep8_nasalib.json` / `ep8_nasa.json` / `ep8_ia2.json` / `ep8_shots.json`
- `ref/ep8/slots_nasa.json` — 欄の網（MUST／NG）
- `tools/nasa_probe.py` — この回で新設した道具
