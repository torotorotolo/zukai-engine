---
title: 19本目 素材の在庫（機関・PD を先に）— 写真・記録映像・一次資料の追加
created: 2026-10-05
tags: [project/jiko-kensho, ep19]
---

# 19本目 素材の在庫（機関・PD を先に）

> **取得はしていない（動画・写真のダウンロードなし）・画像は開いていない・人の写りは頁の説明文から（2026-10-05）。**
> 大きさは頁・API の記載：DVIDS＝画像頁の Resolution（原寸）／Commons＝API の imageinfo／NIST の写真＝2026-09-04 の実測（`analytics/materials/nist_surfside.json`・2800px 上限の配信の大きさ）／Kaltura＝公開 API の width・height（動画は取らずメタデータだけ）／YouTube＝watch 頁の playerResponse。
> HTTP の状態は 2026-10-05 に取った値（DVIDS 29頁・Commons 43頁・NIST の写真 75点＝すべて 200。Kaltura 29本＝status 2（公開中）。YouTube＝playability OK）。
> 中身・人の写りは**説明文の文字から**。説明に人の記載が無いものは「記載なし」、私人の有無が説明から分からないものは「不明＝要目視」。**推測は「推定」と書いた**。
> 私人（住民・犠牲者・遺族・理事・弁護士）の実名は書いていない。撮影者名は**クレジットに要る分だけ**（連邦・郡の職員のクレジットと CC の作者）。
> 道具（scratchpad・一時）：`dvids_pages.py`（DVIDS の頁を読む）・`commons_inv.py`／`commons_files.py`（Commons API）・`kaltura_meta.py`（Kaltura の公開メタデータ）・`yt_channel_search.py`／`yt_meta.py`（YouTube の頁の文字）。UA はブラウザ風・連絡先なし。

## §0 凡例

- **根拠**：A＝米連邦 §105（合衆国政府の職員の職務の著作）／B＝所有者の自主宣言（PDM・CC0）／C＝更新されなかった米国著作物／D＝撮影国の短い保護期間／CC BY＝可（クレジット）／**CC BY-SA＝原則不可**（額装なら可の例外あり＝ここでは判断せず印だけ）／**PD-FLGov の可能性（要判断）**＝フロリダ州の郡・町の公開記録（§105 の外。州の公記録法と Microdecisions v. Skinner（Fla. 2d DCA 2004）を根拠に Commons は {{PD-FLGov}} を使う。**断定しない**）／報道・私人＝不可（引用の要件で検討するものは「引用の候補」）。
- **人の写り**（物差し）：公的な任務の人（消防・捜索隊・NIST の調査員・FEMA）の顔＝可／私人の顔＝不可（CC BY・PD は顔だけモザイクで可）／血・傷・損傷のある遺体＝不可／覆われた遺体・担架＝遠景だけ。
- **場面**：崩落前／直後（6/24）／捜索（6/25〜7/23）／残った棟／解体（7/4〜5）／跡地（解体・撤去の後）／証拠／試験／図／解説（調査団の発表）／追悼。
- 旧版の物差し：materials.md §0（NIST の方針・量の規則）と同じ。

---

## §1 写真（この事故）

### §1-1 FEMA ほか（DVIDS）29点 — 旧版の「事故そのもの」の DVIDS 25点を含む

- 頁の権利欄＝29点とも「**PUBLIC DOMAIN** … must comply with the restrictions shown on https://www.dvidshub.net/about/copyright」。
- **撮影者が FEMA の職員か（頁で確かめた結果）**：頁の「Photo by」は28点が FEMA の掲載者（所属欄＝Federal Emergency Management Agency・`/unit/FEMA`）、1点が米空軍（927th Air Refueling Wing）。**説明文の中に別の撮影者のクレジットがある**ものが12点：「FEMA Photo by Ricardo Agosto Castro」7点・「FEMA/Aaron Levy」1点・「FEMA Photo by US&R PIO Frank Salomon」2点（＝**US&R の隊の広報官**）・「Photo by FEMA」1点・「U.S. Air Force photo」1点。**職員か請負かは頁に書かれていない**（所属の表示まで）。
- CDN の `2000w_q95.jpg` は小さい原本を引き伸ばして返す（09-04 実測・10点）＝**実効の幅は頁の Resolution**。1920 未満の横長（1560・1744・1856・1952）は全画面で拡大になる。
- ⚠️ 旧版の「事故そのもの」の DVIDS 25点（幅1280以上）は、**会議・公人 5・休息（客船）1・空軍の牧師の肖像（基地）1 を含んだ数**。説明文で「現場の救助隊」と言える横長1280以上は **18点**。

| # | ID・頁 | 題（頁） | 撮影日（頁）／掲載 | 撮影者（Photo by／所属）・説明の中のクレジット | 大きさ（頁） | 権利の根拠 | 人の写り（説明文から） | 何が写るか（説明文から） | 19本目で効く場面 | HTTP |
|---:|---|---|---|---|---|---|---|---|---|:-:|
| 1 | 6718327 https://www.dvidshub.net/image/6718327/fema-assists-recovery-surfside-building-collapse | FEMA assists recovery in Surfside Building Collapse [Image 1 of 8] | 2021-06-27／07-06 | Lameen Witter／FEMA・説明にクレジットなし | 2776x2082 | A（所属 FEMA・頁に PUBLIC DOMAIN） | 救助隊（公務）。私人は記載なし＝不明＝要目視 | 崩落の後に集まる救助隊（"Rescue workers gather at the build[ing]"） | 捜索 | 200 |
| 2 | 6718324 https://www.dvidshub.net/image/6718324/fema-assists-recovery-surfside-building-collapse | 同 [Image 6 of 8] | 2021-06-27／07-06（⚠️説明は「July 27, 2021」＝頁内で食い違い） | Lameen Witter／FEMA・説明＝FEMA Photo by Ricardo Agosto Castro | 2776x2082 | A | 救助隊（公務）。私人は不明＝要目視 | 救助隊が集まる | 捜索 | 200 |
| 3 | 6718320 https://www.dvidshub.net/image/6718320/fema-assists-recovery-surfside-building-collapse | 同 [Image 5 of 8] | 2021-06-27／07-06 | Lameen Witter／FEMA・説明＝FEMA Photo by Ricardo Agosto Castro | 2184x1457 | A | FEMA 長官（公人）と救助隊 | FEMA 長官が救助隊と会う | 捜索（公人の視察） | 200 |
| 4 | 6718319 https://www.dvidshub.net/image/6718319/fema-assists-recovery-surfside-building-collapse | 同 [Image 4 of 8] | 2021-06-27／07-06 | Lameen Witter／FEMA・説明にクレジットなし | 2776x2082 | A | FEMA 第4地域の長（公人）と救助隊 | 地域の長が救助隊と会う | 捜索（公人の視察） | 200 |
| 5 | 6718318 https://www.dvidshub.net/image/6718318/fema-assists-recovery-surfside-building-collapse | 同 [Image 3 of 8] | 2021-06-27／07-06（⚠️説明は「July 1, 2021」） | Lameen Witter／FEMA・説明＝FEMA Photo by Ricardo Agosto Castro | 1952x1302 | A | FEMA と救助隊（公務） | FEMA が救助隊に加わる | 捜索 | 200 |
| 6 | 6718317 https://www.dvidshub.net/image/6718317/fema-assists-recovery-surfside-building-collapse | 同 [Image 2 of 8] | 2021-06-27／07-06（⚠️説明は「July 1」） | Lameen Witter／FEMA・説明にクレジットなし | 1560x1171 | A | FEMA 長官（公人）と救助隊 | 長官が救助隊と会う | 捜索（公人の視察） | 200 |
| 7 | 6718311 https://www.dvidshub.net/image/6718311/fema-assists-recovery-surfside-building-collapse | 同 [Image 8 of 8] | 2021-06-27／07-06（⚠️説明は「July 1」） | Lameen Witter／FEMA・説明＝FEMA Photo by Ricardo Agosto Castro | 2184x1457 | A | FEMA 長官（公人）と救助隊 | 長官が救助隊と会う | 捜索（公人の視察） | 200 |
| 8 | 6718309 https://www.dvidshub.net/image/6718309/fema-assists-recovery-surfside-building-collapse | 同 [Image 7 of 8] | 2021-06-27／07-06（⚠️説明は「July 1」） | Lameen Witter／FEMA・説明にクレジットなし | 2776x2082 | A | FEMA 長官（公人）と救助隊 | 長官と救助隊 | 捜索（公人の視察） | 200 |
| 9 | 6717687 https://www.dvidshub.net/image/6717687/fema-assists-recovery-surfside-building-collapse | 同 [Image 5 of 5] | 2021-07-01／07-01 | Lameen Witter／FEMA・説明にクレジットなし | 1239x1856（縦） | A | FEMA の US&R 隊員と消防（公務） | US&R が初動の隊に加わる | 捜索（縦長＝全画面に不向き） | 200 |
| 10 | 6717686 https://www.dvidshub.net/image/6717686/fema-assists-recovery-surfside-building-collapse | 同 [Image 4 of 5] | 2021-07-01／07-01 | 同 | 1856x1239 | A | US&R 隊員（公務） | がれきの撤去（"clearing debris"） | 捜索 | 200 |
| 11 | 6717685 https://www.dvidshub.net/image/6717685/fema-assists-recovery-surfside-building-collapse | 同 [Image 3 of 5] | 2021-07-01／07-01 | 同 | 1856x1239 | A | US&R 隊員（公務） | がれきの撤去 | 捜索 | 200 |
| 12 | 6717684 https://www.dvidshub.net/image/6717684/fema-assists-recovery-surfside-building-collapse | 同 [Image 2 of 5] | 2021-07-01／07-01 | 同 | 1744x1310 | A | US&R 隊員（公務） | がれきの撤去 | 捜索 | 200 |
| 13 | 6717683 https://www.dvidshub.net/image/6717683/fema-assists-recovery-surfside-building-collapse | 同 [Image 1 of 5] | 2021-07-01／07-01 | Lameen Witter／FEMA・説明＝Photo by FEMA | 1238x1856（縦） | A | US&R 隊員（公務） | がれきの撤去 | 捜索（縦長） | 200 |
| 14 | 6717639 https://www.dvidshub.net/image/6717639/fema-assists-recovery-surfside-building-collapse | FEMA assists recovery in Surfside Building Collapse | 2021-07-01／07-01 | Lameen Witter／FEMA・説明にクレジットなし | 1856x1239 | A | US&R 隊員（公務） | がれきの撤去 | 捜索 | 200 |
| 15 | 6717995 https://www.dvidshub.net/image/6717995/fema-assists-recovery-surfside-building-collapse | FEMA assists recovery in Surfside Building Collapse | 2021-07-01／07-01 | 同 | 2184x1457 | A | FEMA 長官・州知事・郡長・連邦議員ら（公人）と US&R | 公人の一行が救助隊と会う | 捜索（公人の視察） | 200 |
| 16 | 6722815 https://www.dvidshub.net/image/6722815/president-biden-visits-surfside-building-recovery-operations | President Biden visits Surfside building recovery operations | 2021-07-01／07-06 | Lameen Witter／FEMA・説明＝FEMA/Aaron Levy | 3264x2448 | A | 大統領・大統領夫人・州知事夫妻・副知事・連邦議員・州の危機管理局長（公人） | 州の危機管理局長が大統領らに状況を説明（場所の記載は「MIAMI, FL」） | 捜索（大統領の訪問） | 200 |
| 17 | 6722707 https://www.dvidshub.net/image/6722707/urban-search-and-rescue-teams-continue-surfside-support | Urban Search and Rescue teams continue to Surfside support | 2021-07-02／07-06 | Kenneth Wilsey／FEMA・説明にクレジットなし | 2184x1457 | A | US&R 隊員（公務） | 0時〜12時の交代を終えた隊が客船（Royal Caribbean Explorer of the Seas）へ休みに戻る＝**現場ではない** | 捜索（隊の休息） | 200 |
| 18 | 6725022 https://www.dvidshub.net/image/6725022/rescue-officials-discuss-recovery-resources-surfside-building-collapse | Rescue officials discuss recovery resources for Surfside building collapse [Image 2 of 2] | 2021-07-04／07-08 | Lameen Witter／FEMA・説明＝FEMA Photo by Ricardo Agosto Castro | 2184x1457 | A | 連邦議員・FEMA・SBA・**NIST の調査責任者**（公人・公務） | NIST の調査責任者による円卓の説明（室内） | 捜索の体制／調査の始まり | 200 |
| 19 | 6725021 https://www.dvidshub.net/image/6725021/rescue-officials-discuss-recovery-resources-surfside-building-collapse | 同 [Image 1 of 2] | 2021-07-04／07-08 | 同 | 2184x1457 | A | 同 | 同 | 同 | 200 |
| 20 | 6741409 https://www.dvidshub.net/image/6741409/reserve-chaplain-supports-surfside-condo-collapse-victims-first-responders | Reserve Chaplain supports Surfside condo collapse victims, first responders | 2021-07-20／07-20 | Staff Sgt. Bradley Tipton／927th Air Refueling Wing（米空軍） | 3795x3479 | A（米空軍）だが **DoD（現 Department of War）の断り書きの義務**＝使わない（旧版どおり） | 従軍牧師の肖像（公務） | マクディル空軍基地の礼拝堂の前の肖像＝**現場ではない** | （使わない） | 200 |
| 21 | 6725107 https://www.dvidshub.net/image/6725107/rescue-teams-meet-with-local-officials-surfside-building-collapse-recovery | Rescue teams meet with local officials for Surfside building collapse recovery | 2021-07-05／07-08 | Lameen Witter／FEMA・説明＝FEMA Photo by Ricardo Agosto Castro | 2184x1457 | A | US&R と地元の幹部（公務） | 統合指揮の幹部会議（"Alpha United Command and General Staff Meeting"・室内） | 捜索の体制 | 200 |
| 22 | 6729455 https://www.dvidshub.net/image/6729455/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery | Urban Search and Rescue teams continue to support Surfside Building Collapse recovery [Image 2 of 2] | 2021-07-05／07-12 | Lameen Witter／FEMA・説明＝**FEMA Photo by US&R PIO Frank Salomon** | 768x1024（縦・小） | **A と推定・要判断**（撮影＝US&R の隊の広報官） | US&R 隊員（公務） | がれきの山（pile）の交代に戻る隊 | 捜索（小さい） | 200 |
| 23 | 6729454 https://www.dvidshub.net/image/6729454/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery | 同 [Image 1 of 2] | 2021-07-05／07-12 | 同 | 718x957（縦・小） | **A と推定・要判断** | 同 | 同 | 捜索（小さい） | 200 |
| 24 | 6723298 https://www.dvidshub.net/image/6723298/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery | 同 [Image 1 of 6] | 2021-07-03／07-07 | Lameen Witter／FEMA・説明にクレジットなし | 2056x1544 | A | ペンシルベニア第1隊（PA-TF1）の隊員（公務） | 12時間の交代に入る準備（現場が写るかは記載なし） | 捜索（隊） | 200 |
| 25 | 6723300 https://www.dvidshub.net/image/6723300/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery | 同 [Image 3 of 6] | 2021-07-03／07-07 | 同 | 2056x1543 | A | 同 | 同 | 捜索（隊） | 200 |
| 26 | 6723299 https://www.dvidshub.net/image/6723299/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery | 同 [Image 2 of 6] | 2021-07-03／07-07 | 同 | 2573x1715 | A | 同 | 同 | 捜索（隊） | 200 |
| 27 | 6723297 https://www.dvidshub.net/image/6723297/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery | 同 [Image 6 of 6] | 2021-07-03／07-07 | 同 | 2184x1457 | A | 同 | 同 | 捜索（隊） | 200 |
| 28 | 6723296 https://www.dvidshub.net/image/6723296/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery | 同 [Image 5 of 6] | 2021-07-03／07-07 | 同 | 2184x1501 | A | 同 | 同 | 捜索（隊） | 200 |
| 29 | 6723295 https://www.dvidshub.net/image/6723295/urban-search-and-rescue-teams-continue-support-surfside-building-collapse-recovery | 同 [Image 4 of 6] | 2021-07-03／07-07 | 同 | 2184x1457 | A | 同 | 同 | 捜索（隊） | 200 |

- 頁の「Photo by」が FEMA の掲載者で、説明にクレジットが無い17点は、クレジットを「FEMA」とするのが安全（撮影者の個人名は頁に無い）。
- DVIDS の新しい点は見つからなかった（ギャラリーのつながり＝29点で閉じる）。検索頁は **WAF（202・405）で読めず**＝09-04 のブラウザ実測（画像29点・動画0本）を超える再測はできていない。

### §1-2 Wikimedia Commons — カテゴリ3つ（22ファイル）＋カテゴリの外

- 「Champlain Towers South collapse」という名のカテゴリは**無い**（API の allcategories・カテゴリ名の検索で確認）。実在するのは次の3つ。
- カテゴリ：`Category:Surfside condominium building collapse`（13）・`Category:Champlain Towers South`（2）・`Category:IDF Aid Mission to Surfside condominium building collapse, 2021`（7）＝**22ファイル**（下位は IDF だけ）。うち動く映像4（IDF の webm 2・CC0 の作図 webm と gif）は §2 へ。ここは **写真18**。
- ライセンスは wikitext の `== {{int:license-header}} ==` の節のテンプレートで確かめた。
- **カテゴリの外で見つかったもの**：DHS（国土安全保障省）の Flickr の写真15点（2021-08-19 の視察）＝連邦＝A。旧版の実測（09-04）には無い。ほかに崩落前の建物が写るかもしれない地理タグの写真3点（写っているかは**要目視**）。

| # | ファイル（頁） | 説明（頁） | 撮影日 | 作者・出どころ | 大きさ | ライセンス（wikitext） | 人の写り（説明から） | 場面 | 19本目 | HTTP |
|---:|---|---|---|---|---|---|---|---|---|:-:|
| C1 | https://commons.wikimedia.org/wiki/File:Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_1.jpg | 崩落の後。がれきと**残った棟**がはっきり写る | 2021-06-24 | Miami-Dade Fire Rescue Department（MDFR の X 投稿 1408074745258680327 から） | 1024x768 | `{{PD-FLGov}}` | 人の記載なし | 直後・残った棟 | **PD-FLGov の可能性（要判断）**・小さい | 200 |
| C2 | https://commons.wikimedia.org/wiki/File:Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_2.jpg | がれきと残った棟を見上げる寄り | 2021-06-24 | MDFR（同じ投稿） | 1200x1600（縦） | `{{PD-FLGov}}`＋LicenseReview | 人の記載なし | 直後・残った棟 | 要判断・縦長 | 200 |
| C3 | https://commons.wikimedia.org/wiki/File:Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_3.jpg | MDFR の消防士ががれきの中で生存者を探す | 2021-06-24 | MDFR（投稿 1408075822246809604） | 1600x1200 | `{{PD-FLGov}}`＋LicenseReview | 消防士（公務） | 直後（捜索） | 要判断・旧版の「PD 1280以上」3点の1 | 200 |
| C4 | https://commons.wikimedia.org/wiki/File:Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_4.jpg | 崩れた棟の別の向き。地上に救助隊 | 2021-06-24 | MDFR（投稿 1408021153415892992） | 1024x768 | `{{PD-FLGov}}`＋LicenseReview | 救助隊（公務） | 直後・残った棟 | 要判断・小さい | 200 |
| C5 | https://commons.wikimedia.org/wiki/File:Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_5.jpg | がれきと、救助犬を連れて入る準備の MDFR 隊員 | 2021-06-24 | MDFR（投稿 1408075822246809604） | 1512x1512 | `{{PD-FLGov}}`＋LicenseReview | 隊員（公務）・犬 | 直後（捜索） | 要判断・旧版の3点の1 | 200 |
| C6 | https://commons.wikimedia.org/wiki/File:Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_6.jpg | 昼の地上からの全景。車と屋外の食事の場の損傷。がれきの中の救助隊と犬 | 2021-06-24 | MDFR（投稿 1408077429013454855） | 2048x1536 | `{{PD-FLGov}}`＋LicenseReview | 救助隊（公務）・犬 | 直後（捜索） | 要判断・旧版の3点の1・**一番大きい** | 200 |
| C7 | https://commons.wikimedia.org/wiki/File:Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_2_(cropped).jpg | C2 の切り出し | 2021-06-24 | MDFR | 661x882 | `{{PD-FLGov}}` | 人の記載なし | 直後・残った棟 | 小さい（C2 の派生） | 200 |
| C8 | https://commons.wikimedia.org/wiki/File:Fire_personnel_-_Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_3_(cropped).jpg | C3 の切り出し（消防士） | 2021-06-24 | MDFR | 559x746 | `{{PD-FLGov}}` | 消防士（公務） | 直後 | 小さい（派生） | 200 |
| C9 | https://commons.wikimedia.org/wiki/File:Dog_and_handler_-_Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_6_(cropped).jpg | C6 の切り出し（犬と指導手） | 2021-06-24 | MDFR | 713x950 | `{{PD-FLGov}}` | 隊員（公務）・犬 | 直後 | 小さい（派生） | 200 |
| C10 | https://commons.wikimedia.org/wiki/File:Dogs_and_Handlers_at_Surfside_condominium_collapse_photo_from_Miami-Dade_Fire_Rescue_5_(cropped).jpg | C5 の切り出し | 2021-06-24 | MDFR | 796x1061 | `{{PD-FLGov}}` | 隊員（公務）・犬 | 直後 | 小さい（派生） | 200 |
| C11 | https://commons.wikimedia.org/wiki/File:Champlain_Towers_South_(Surfside,_Miami,_FL).jpg | 崩落前の建物（道路からの眺め） | 2015-02-14 | Mapillary の利用者「Microsoft」（Microsoft StreetSide） | 795x545 | `{{Cc-by-sa-4.0}}`＋LicenseReview | 記載なし（通行人の有無は要目視） | 崩落前 | **BY-SA＝原則不可**・小さい | 200 |
| C12 | https://commons.wikimedia.org/wiki/File:Champlain_Towers_South_(87th_Terrace_view,_Surfside,_Miami,_FL).png | 崩落前（87th Terrace の東端から） | 2015-02-14 | 同（Mapillary の画面写し） | 857x566 | `{{Cc-by-sa-4.0}}`＋LicenseReview | 同 | 崩落前 | **BY-SA**・小さい | 200 |
| C13 | https://commons.wikimedia.org/wiki/File:Remains_of_the_Collapsed_Florida_Surfside_Condo_(2021-10-04).jpg | "with uprooted rebar"（跡地と抜けた鉄筋） | 2021-10-04 | Steve Jurvetson（Flickr: jurvetson・https://www.flickr.com/photos/jurvetson/51566340466/） | 4032x2086 | `{{cc-by-2.0}}`＋FlickreviewR passed | 記載なし | 跡地 | **CC BY 2.0＝可（クレジット）**・旧版未使用 | 200 |
| C14 | https://commons.wikimedia.org/wiki/File:IDF_Aid_Mission_to_Surfside_condominium_building_collapse,_June_2021._III.jpg | イスラエル国防軍の銃後司令部と外務省の救助団（3D モデルで捜索を支えた・説明はヘブライ語） | 2021-06-30 | IDF Spokesperson's Unit（https://www.idf.il/ の記事） | 1600x1066 | `{{cc-by-sa-3.0}}`（VRT の許諾） | 外国の救助隊（公務と推定）＝要目視。軍の記章の可能性 | 捜索 | **BY-SA**＝原則不可 | 200 |
| C15 | https://commons.wikimedia.org/wiki/File:IDF_Aid_Mission_to_Surfside_condominium_building_collapse,_June_2021._IV.jpg | 同 | 2021-06-30 | 同 | 1600x1012 | `{{cc-by-sa-3.0}}` | 同 | 捜索 | BY-SA | 200 |
| C16 | https://commons.wikimedia.org/wiki/File:IDF_Aid_Mission_to_Surfside_condominium_building_collapse,_June_2021._V.jpg | 同（英語の説明あり） | 2021-06-30 | 同 | 1600x1068 | `{{cc-by-sa-3.0}}` | 同 | 捜索 | BY-SA | 200 |
| C17 | https://commons.wikimedia.org/wiki/File:IDF_Aid_Mission_to_Surfside_condominium_building_collapse,_June_2021._VI.jpg | 同 | 2021-06-30 | 同 | 1600x1066 | `{{cc-by-sa-3.0}}` | 同 | 捜索 | BY-SA | 200 |
| C18 | https://commons.wikimedia.org/wiki/File:%D7%9E%D7%A9%D7%9C%D7%97%D7%AA_%D7%94%D7%97%D7%99%D7%9C%D7%95%D7%A5_%D7%A9%D7%9C_%D7%94%D7%99%D7%97%D7%A6%22%27%D7%90_%D7%91%D7%A1%D7%A8%D7%A4%D7%A1%D7%99%D7%99%D7%93_%D7%9E%D7%99%D7%90%D7%9E%D7%99.jpg | 銃後司令部の救助団（サーフサイド） | 頁の日付 2022-12-26（撮影日の記載なし） | 同 | 1583x710 | `{{IDF}}`→ CC BY-SA 3.0 | 同 | 捜索 | BY-SA・横に細長い | 200 |
| D1〜D15 | 下の表（DHS） | — | — | — | — | — | — | — | — | — |

**DHS（国土安全保障省）の写真15点**（カテゴリの外・`File:DHS Secretary Alejandro Mayorkas Visits Surfside Condo Collapse Site (<Flickr ID>).jpg`）
- 説明（15点とも同じ）：2021-08-19、国土安全保障長官・連邦下院議員・郡長が**崩落の現場を訪れ、約100人の犠牲者に弔意を表す**。作者欄＝DHSgov（撮影者名なし）。出どころ＝`https://www.flickr.com/photos/dhsgov/<Flickr ID>`。ライセンス＝`{{PD-USGov-DHS}}`＋FlickreviewR（Commons のカテゴリに「review needed」の印あり）。
- 根拠＝**A**（連邦）。人の写り＝公人（長官・議員・郡長）。⚠️ **追悼の場**＝犠牲者の写真（私人の顔）や遺族が写る可能性＝**要目視**。場面＝**跡地**（8月＝撤去の後と推定・説明に「site」とだけ）。

| # | 頁 | 撮影時刻（Commons の DateTimeOriginal） | 大きさ | HTTP |
|---|---|---|---|:-:|
| D1 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390531311).jpg | 2021-08-19 16:23:50 | 2500x1740 | 200 |
| D2 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51389767967).jpg | 16:26:54 | 2500x1727 | 200 |
| D3 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390783308).jpg | 16:27:34 | 2500x1897 | 200 |
| D4 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390783173).jpg | 16:30:09 | 2500x1742 | 200 |
| D5 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390531001).jpg | 16:31:03 | 2500x1688 | 200 |
| D6 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390782983).jpg | 16:31:33 | 2500x1667 | 200 |
| D7 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390782948).jpg | 16:31:48 | 2500x1667 | 200 |
| D8 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390782873).jpg | 16:32:06 | 2500x1828 | 200 |
| D9 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51389767287).jpg | 16:32:16 | 2500x1764 | 200 |
| D10 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51391263849).jpg | 16:32:32 | 2500x1814 | 200 |
| D11 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390530346).jpg | 16:32:45 | 2500x1667 | 200 |
| D12 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51389766977).jpg | 16:33:10 | 2500x1790 | 200 |
| D13 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51391544170).jpg | 17:19:42 | 2500x1751 | 200 |
| D14 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390782198).jpg | 17:21:44 | 2500x1757 | 200 |
| D15 | https://commons.wikimedia.org/wiki/File:DHS_Secretary_Alejandro_Mayorkas_Visits_Surfside_Condo_Collapse_Site_(51390782128).jpg | 17:25:34 | 2500x1788 | 200 |

**崩落前の候補（建物名の記載なし＝写っているかは要目視）**：Commons の地理検索（CTS から半径1km）で拾った。

| # | 頁 | 説明・場所 | 撮影日 | 作者 | 大きさ | ライセンス | 人の写り | 19本目 | HTTP |
|---|---|---|---|---|---|---|---|---|:-:|
| P1 | https://commons.wikimedia.org/wiki/File:Surfside,_FL,_USA_-_panoramio.jpg | 「Surfside, FL, USA」。撮影位置 25.874149,-80.12136（Collins Ave・CTS の約160m北） | 2012-11-24 | Gervacio Rosales（Panoramio） | 4000x3000 | `{{cc-by-3.0}}` | 不明＝要目視 | **CC BY＝可**・CTS が写るかを要目視 | 200 |
| P2 | https://commons.wikimedia.org/wiki/File:Surfside_Florida_Banner.jpg | P1 の切り出し（Wikivoyage の帯） | 2012-11-24 | 同 | 4000x571 | `{{cc-by-3.0}}` | 同 | P1 の派生 | 200 |
| P3 | https://commons.wikimedia.org/wiki/File:Looking-down-the-beach.jpg_-_panoramio.jpg | 「looking-down-the-beach」。撮影位置 25.869264,-80.119944（浜・CTS の約400m南） | 2013-01-07 | Good Free Photos（Panoramio） | 2500x1667 | `{{cc-by-3.0}}` | 浜の人（私人）の可能性＝要目視 | CC BY・写るかを要目視 | 200 |
| P4 | https://commons.wikimedia.org/wiki/File:MIAMI_BEACH_FROM_N901AN_FLIGHT_MIA-DCA_(7393180966).jpg | 機窓からのマイアミビーチ | 2010-05-21 | Eric Salard（Flickr） | 3264x2177 | `{{cc-by-sa-2.0}}` | 記載なし | **BY-SA**・写るかを要目視 | 200 |

- 見たが対象外：`File:Surfside Condo (5974601963).jpg`（2011・612x612・CC BY 2.0・説明「Noguchi coffee table」＝別の室内）／`File:Surfside-Florida-2014.jpg`（町の標識・CC BY-SA 3.0）。
- Commons の全文検索「Biden Surfside」ほか（ホワイトハウスの写真）＝0件。

### §1-3 NIST の写真（news-and-updates の Photo Gallery 75点）

- 頁：https://www.nist.gov/disaster-and-failure-studies/champlain-towers-south-collapse/news-and-updates （2026-10-05 に 200）。75点の URL は下の「元の置き場」（`/sites/default/files/images/…`）で、**75点とも HEAD 200**。
- 根拠＝**A**（説明の末尾に「Credit: NIST」67点・「Credit: R. Eskalis/NIST」6点・「Credit: L. Gerskovic/NIST」2点＝重なりなしで75点。NIST の方針は materials.md §0）。大学での試験の写真も **Credit は NIST**（頁の記載）。
- 大きさ＝09-04 の実測（2800px 上限の配信）。GIF だけ 1920x1080・167コマ（materials.md §2 の ss_gif＝**既出**）。
- 旧版の区分＝09-04 の実測（現場18＝#9〜#26。うち「事故そのもの」8＝全景3〔#17・#18・#13〕＋部材5〔#23・#20・#22・#9・#11〕）。

| # | 元の置き場（URL） | 説明の要約・時期（頁） | Credit | 大きさ | 人の写り（説明から） | 場面 | 旧版の区分 |
|---:|---|---|---|---|---|---|---|
| 0 | https://www.nist.gov/sites/default/files/images/2022/06/14/Werehouse.jpg | 崩れた部分と**爆破解体した部分**の両方の部材を保管する倉庫（2022年1月） | NIST | 2198x2800 | 記載なし | 証拠（倉庫） | 試験・調査 |
| 1 | https://www.nist.gov/sites/default/files/images/2022/06/15/David%20Goodman%203.jpg | 証拠保全の共同責任者が非破壊の方法を評価（2022年1月） | NIST | 2100x2800 | NIST の調査員（公務） | 証拠（倉庫） | 同 |
| 2 | https://www.nist.gov/sites/default/files/images/2022/06/15/MerisaMalcolm%26David.jpg | 調査員3人が部材を調べてデータベースに（2022年1月） | NIST | 2800x2596 | 調査員3人（公務） | 証拠（倉庫） | 同 |
| 3 | https://www.nist.gov/sites/default/files/images/2022/06/15/Ruthie%20Corzo.jpg | 携帯の分析器で塩化物を測る手順を評価（2022年1月） | NIST | 2738x2800 | 調査員（公務） | 証拠（倉庫） | 同 |
| 4 | https://www.nist.gov/sites/default/files/images/2022/06/15/Malcolm2.jpg | 部材の情報を記録（2022年1月） | NIST | 2100x2800 | 調査員（公務） | 証拠（倉庫） | 同 |
| 5 | https://www.nist.gov/sites/default/files/images/2022/06/15/Merisa%20Measuring.jpg | 柱の鉄筋を測る（2022年1月） | NIST | 2100x2800 | 調査員（公務） | 証拠（倉庫） | 同 |
| 6 | https://www.nist.gov/sites/default/files/images/2022/06/15/Daniel%20Sawyer%20_3D%20scanner.jpg | 3D スキャンの手順を評価（2022年1月） | NIST | 2800x2100 | 調査員（公務） | 証拠（倉庫） | 同 |
| 7 | https://www.nist.gov/sites/default/files/images/2022/06/15/Malcolm%20and%20Stephanie%20Ultrasonic.jpg | 駐車場の1層柱で非破壊の測定（2022年1月） | NIST | 2084x1206 | 調査員2人（公務） | 証拠（倉庫） | 同 |
| 8 | https://www.nist.gov/sites/default/files/images/2022/06/15/Kam%20Saidi.jpg | 部材の3D スキャンを処理（2022年2月） | NIST | 1920x1080 | 共同責任者（公務） | 証拠（室内） | 同 |
| 9 | https://www.nist.gov/sites/default/files/images/2021/07/15/IMG_0090%20%28scott%20071221%29.jpeg | 証拠の仮置き場の NIST 職員 | NIST | 2800x2100 | NIST 職員（公務） | 証拠（現場） | **事故そのもの（部材）** |
| 10 | https://www.nist.gov/sites/default/files/images/2021/08/25/KAM_3717%28July6th%29.JPG | 現場から運び出す前の柱を調べる（2021-07-06） | NIST | 2800x1867 | NIST の技術者（公務） | 証拠（現場） | 調査の様子 |
| 11 | https://www.nist.gov/sites/default/files/images/2021/08/25/KAM_3753%20%28july7th%29.JPG | がれきの山から柱を札付けの場へ移す（2021-07-07） | NIST | 2800x1867 | 記載なし | 証拠（現場） | **事故そのもの（部材）** |
| 12 | https://www.nist.gov/sites/default/files/images/2021/08/25/NIST%20team%20July1.jpg | がれきから取り出したコンクリート片を調べる（2021-07-01） | NIST | 2800x1613 | NIST 職員（公務） | 証拠（現場） | 調査の様子 |
| 13 | https://www.nist.gov/sites/default/files/images/2021/08/25/NIST%20team%20July2.jpg | 仮置き場で部材に札を付け撮影（2021-07-02） | NIST | 2800x1477 | NIST 職員（公務） | 証拠（現場） | **事故そのもの（全景）**（09-04 の実見＝潰れた車と瓦礫） |
| 14 | https://www.nist.gov/sites/default/files/images/2021/08/25/KAM_3706%28July6th%29.JPG | 柱を撮影し札を付ける（2021-07-06） | NIST | 2800x1867 | NIST の技術者（公務） | 証拠（現場） | 調査の様子 |
| 15 | https://www.nist.gov/sites/default/files/images/2021/08/25/KAM_3698%28July6th%29.JPG | 同（2021-07-06） | NIST | 2800x1867 | 同 | 証拠（現場） | 調査の様子 |
| 16 | https://www.nist.gov/sites/default/files/images/2021/08/25/KAM_3691%28July6th%29.JPG | 柱に札（2021-07-06） | NIST | 2800x1867 | 同 | 証拠（現場） | 調査の様子 |
| 17 | https://www.nist.gov/sites/default/files/images/2021/06/30/IMG_6362.JPG | 崩落の現場（頁の置き場の日付 2021-06-30） | NIST | 2800x2100 | 記載なし（09-04 の実見＝捜索隊） | 捜索・**残った棟**（09-04 実見＝せん断された断面＋残った棟） | **事故そのもの（全景）** |
| 18 | https://www.nist.gov/sites/default/files/images/2021/07/19/IMG_0122-%28Jonathan-070721%29.jpg | 南の隣の建物のバルコニーから見た現場。NIST の撮影機材を置いた | NIST | 2800x2100 | 記載なし | 捜索（現場の俯瞰） | **事故そのもの（全景）** |
| 19 | https://www.nist.gov/sites/default/files/images/2021/07/15/Lidar%20and%20other%20instruments%20.jpg | 現場を走査するカメラとライダー | NIST | 2800x2100 | 記載なし | 捜索（計測） | 調査の様子 |
| 20 | https://www.nist.gov/sites/default/files/images/2021/07/15/IMG_0428.JPG | 柱・梁・床版を選び出し札を付け、**警察の護衛**で保管所へ | NIST | 2800x2100 | 記載なし | 証拠（現場） | **事故そのもの（部材）** |
| 21 | https://www.nist.gov/sites/default/files/images/2021/07/15/Scott%20Jones%20measuring.jpg | 超音波パルス速度（UPV）で柱を調べる | NIST | 2800x2100 | 技術者（公務） | 証拠（現場） | 調査の様子 |
| 22 | https://www.nist.gov/sites/default/files/images/2021/07/14/IMG_0154%20%28Jonathan%20070721%29.jpg | #20 と同じ説明 | NIST | 2100x2800 | 記載なし | 証拠（現場） | **事故そのもの（部材）** |
| 23 | https://www.nist.gov/sites/default/files/images/2021/07/15/IMG_0357.JPG | #20 と同じ説明 | NIST | 2800x2100 | 記載なし | 証拠（現場） | **事故そのもの（部材）** |
| 24 | https://www.nist.gov/sites/default/files/images/2021/07/15/Image%20from%20iOS%20%281%29.jpg | NIST と国立科学財団の職員がライダーでの撮像を相談 | NIST | 2100x2800 | 連邦職員（公務） | 捜索（計測） | 調査の様子 |
| 25 | https://www.nist.gov/sites/default/files/images/2021/07/15/Scott%20Jones%20measuring2.jpg | #21 と同じ説明 | NIST | 2100x2800 | 技術者（公務） | 証拠（現場） | 調査の様子 |
| 26 | https://www.nist.gov/sites/default/files/images/2021/07/01/Champlain_NIST%20Team4.jpg | NIST と陸軍工兵隊が部材を調べる | NIST | 2100x2800 | 連邦職員（公務） | 証拠（現場） | 調査の様子 |
| 27 | https://www.nist.gov/sites/default/files/images/2023/05/31/image1.jpg | 新しい倉庫へ移す作業を見守る（2023年5月） | NIST | 1512x2016 | 調査団（公務） | 証拠（倉庫） | 試験・調査 |
| 28 | https://www.nist.gov/sites/default/files/images/2023/05/31/image8.jpg | 新しい倉庫の柱の標本（2023年5月） | NIST | 2800x2100 | 記載なし | 証拠（倉庫） | 同 |
| 29 | https://www.nist.gov/sites/default/files/images/2023/05/31/image6_0.jpg | 部材を新しい倉庫へ運ぶ（2023年春） | NIST | 2160x1620 | 記載なし | 証拠（搬送） | 同 |
| 30 | https://www.nist.gov/sites/default/files/images/2023/05/31/IMG_2666-%281%29.jpg | 打音検査（2023年5月） | NIST | 2800x2100 | 作業の手元（人の有無は記載から不明） | 証拠（倉庫） | 同 |
| 31 | https://www.nist.gov/sites/default/files/images/2023/05/31/image5_0.jpg | もろい部材を鋼の梁で補強しフォークリフトで動かす（2023年5月） | NIST | 2800x2100 | 記載なし | 証拠（倉庫） | 同 |
| 32 | https://www.nist.gov/sites/default/files/images/2023/05/31/image4.jpg | 証拠の管理の連続を保つための記録（2023年5月） | NIST | 1512x2016 | 記載なし | 証拠（倉庫） | 同 |
| 33 | https://www.nist.gov/sites/default/files/images/2023/09/06/Coring%20and%20MOA%20tests%20%20%28Sep2023%29.jpg | プールデッキの床版からコアを抜く（2023年9月） | NIST | 2800x2100 | 記載なし | 試験（材料） | 同 |
| 34 | https://www.nist.gov/sites/default/files/images/2023/09/06/Coring%20and%20MOA%20tests%20%20%28July2023%29.jpg | 試験を待つコア（2023年7月） | NIST | 2800x1583 | 記載なし | 試験（材料） | 同 |
| 35 | https://www.nist.gov/sites/default/files/images/2023/09/06/Coring%20and%20MOA%20tests1%20%20%20%28July2023%29.jpg | 調査員がコアを調べる（2023年7月） | NIST | 2800x1602 | 調査員（公務） | 試験（材料） | 同 |
| 36 | https://www.nist.gov/sites/default/files/images/2023/09/06/Coring%20and%20MOA%20tests3%20%20%28July2023%29.jpg | 圧縮・弾性係数の試験の前の確認（2023年7月） | NIST | 2800x1575 | 調査員（公務） | 試験（材料） | 同 |
| 37 | https://www.nist.gov/sites/default/files/images/2023/09/06/Coring%20and%20MOA%20tests2%20%20%28July2023%29.jpg | 陸軍工兵隊の職員が圧縮試験の準備（2023年7月） | NIST | 2800x1860 | 連邦職員（公務） | 試験（材料） | 同 |
| 38 | https://www.nist.gov/sites/default/files/images/2023/09/06/Coring%20and%20MOA%20tests5%20%20%28July2023%29.jpg | 圧縮試験の後のコアを調べる（2023年7月） | NIST | 2764x2160 | 連邦職員・調査団（公務） | 試験（材料） | 同 |
| 39 | https://www.nist.gov/sites/default/files/images/2023/09/06/Coring%20and%20MOA%20tests4%20%20%28July2023%29.jpg | コアを壊れるまで圧縮（陸軍工兵隊・2023年7月） | NIST | 2800x1752 | 記載なし | 試験（材料） | 同 |
| 40 | https://www.nist.gov/sites/default/files/images/2024/09/12/NCSTInvestigation_BrollReel08_v04.00_05_01_02.Still009.jpg | 鉄筋の標本を試験機に入れる前に調べる（2024年2月） | R. Eskalis/NIST | 2800x1575 | 技術者（公務） | 試験（材料） | 同 |
| 41 | https://www.nist.gov/sites/default/files/images/2024/09/12/NCSTInvestigation_BrollReel07_v01.00_00_34_13.Still006%20%281%29.jpg | 湿ったコアの電気の通しやすさ（2024年2月） | R. Eskalis/NIST | 2800x1575 | 記載なし | 試験（材料） | 同 |
| 42 | https://www.nist.gov/sites/default/files/images/2024/09/12/NCSTInvestigation_BrollReel07_v01.00_00_14_16.Still005.jpg | 吸水の試験（2024年8月） | R. Eskalis/NIST | 2800x1575 | 記載なし | 試験（材料） | 同 |
| 43 | https://www.nist.gov/sites/default/files/images/2024/11/21/CNST%20CTS%20Update%20Dec.jpg | 調査団3人が建物の計算機モデルを見る（2023年4月） | L. Gerskovic/NIST | 2800x1669 | 調査団（公務） | 調査（室内） | 同 |
| 44 | https://www.nist.gov/sites/default/files/images/2024/11/21/CNST%20CTS%20Update%20Dec-2.jpg | 現場の空中写真を見る。回収した部材は600点超 | L. Gerskovic/NIST | 2800x1473 | 調査団2人（公務） | 調査（室内） | 同 |
| 45 | https://www.nist.gov/sites/default/files/images/2024/11/21/CNST%20CTS%20Update%20Dec-4.jpg | 現場から回収したハードディスクを拡大鏡で調べる（2024年11月） | R. Eskalis/NIST | 2800x1575 | 研究者（公務） | 証拠（ハードディスク） | 同 |
| 46 | https://www.nist.gov/sites/default/files/images/2024/11/21/CNST%20CTS%20Update%20Dec-5.jpg | 壊れたハードディスクから円盤を外す。回収25台 | R. Eskalis/NIST | 2800x1539 | 研究者（公務） | 証拠（ハードディスク） | 同 |
| 47 | https://www.nist.gov/sites/default/files/images/2024/11/21/CNST%20CTS%20Update%20Dec-7.jpg | ハードディスクの顕微鏡像を見る（2024年11月） | R. Eskalis/NIST | 2800x1503 | 調査団3人（公務） | 証拠（ハードディスク） | 同 |
| 48 | https://www.nist.gov/sites/default/files/images/2025/02/04/Lidar_Data_from_Leica_C10_July-14-2021.jpg | 崩落の数週間後のライダーの走査（2021-07-14 のデータ） | NIST | 2800x1731 | 記載なし | 捜索（点群） | 同 |
| 49 | https://www.nist.gov/sites/default/files/images/2025/02/04/MAST%20select.png | ミネソタ大 MAST での実物大の複製に力をかける | NIST | 2800x1730 | 記載なし | 試験（実物大） | 同 |
| 50 | https://www.nist.gov/sites/default/files/images/2025/02/04/UW%20select%20.JPG | ワシントン大 SETL で柱の複製を壊れるまで圧縮 | NIST | 2800x2100 | 記載なし | 試験（実物大） | 同 |
| 51 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2841%20of%204%29.jpg | 重ね継手が短い柱の複製（ワシントン大） | NIST | 2108x2800 | 記載なし | 試験（実物大） | 同 |
| 52 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%288%20of%2038%29.jpg | 試験の後の複製を研究者が調べる（ミネソタ大・2025年1月） | NIST | 2800x1575 | 研究者（公的調査の任務） | 試験（実物大） | 同 |
| 53 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%289%20of%2038%29.jpg | 試験の後の標本＝プールデッキの床版・梁・柱の接合の壊れ方 | NIST | 2800x1654 | 記載なし | 試験（実物大） | 同 |
| 54 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2810%20of%2038%29.jpg | 調査責任者と共同責任者らの打合せ（2025年1月） | NIST | 2800x1575 | 調査団3人（公務） | 調査（打合せ） | 同 |
| 55 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2814%20of%2038%29.jpg | 床版・梁・柱の接合の試験を見る（ミネソタ大） | NIST | 2800x1575 | 調査団（公務） | 試験（実物大） | 同 |
| 56 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2818%20of%2038%29.jpg | MAST の試験の結果（床版と梁） | NIST | 2800x1575 | 記載なし | 試験（実物大） | 同 |
| 57 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2819%20of%2038%29.jpg | MAST の試験の結果（右の梁） | NIST | 2800x1643 | 記載なし | 試験（実物大） | 同 |
| 58 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2828%20of%2038%29.jpg | 試験の前の標本（ミネソタ大） | NIST | 2800x1905 | 記載なし | 試験（実物大） | 同 |
| 59 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2829%20of%2038%29.jpg | 試験の前の床版・梁・柱の複製（MAST） | NIST | 2800x1570 | 記載なし | 試験（実物大） | 同 |
| 60 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2831%20of%2038%29.jpg | 試験の後＝壊れた床版の接合（MAST・2025年1月） | NIST | 2800x1577 | 記載なし | 試験（実物大） | 同 |
| 61 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2839%20of%204%29.jpg | 床版と柱の接合の「せん断破壊」（ワシントン大・2025年2月） | NIST | 2800x2108 | 記載なし | 試験（実物大） | 同 |
| 62 | https://www.nist.gov/sites/default/files/images/2025/04/10/NCST%20Investigation%20April25%20%2842%20of%204%29.jpg | 設計どおりでない柱の複製を壊す（ワシントン大） | NIST | 1717x2800 | 記載なし | 試験（実物大） | 同 |
| 63 | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%281%20of%201%29.jpg | 試験の後の床版のひびを調べる（ワシントン大・2025年6月） | NIST | 2800x2483 | 専門家（公的調査の任務） | 試験（実物大） | 同 |
| 64 | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%2820%20of%201%29.jpg | 床版・梁・柱の試験の進み具合を見守る（ミネソタ大） | NIST | 2800x1761 | 調査員（公務） | 試験（実物大） | 同 |
| 65 | https://www.nist.gov/sites/default/files/images/2025/06/20/NCST%20Investigation%20Update%20June%202025%20%282%20of%207%29.jpg | プールデッキの床版・梁と下がり梁の接合の壊れ方（ミネソタ大） | NIST | 2800x1669 | 記載なし | 試験（実物大） | 同 |
| 66 | https://www.nist.gov/sites/default/files/images/2025/06/20/June%20CTS%20Update%20Concrete%20Slab.jpg | 試験の後の床版を切って断面のせん断ひびを見せる（ワシントン大） | NIST | 1430x804 | 研究者（公的調査の任務） | 試験（実物大） | 同 |
| 67 | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%285%20of%207%29.jpg | 床版のひびを調べる（ワシントン大） | NIST | 2800x1536 | 専門家（同） | 試験（実物大） | 同 |
| 68 | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%286%20of%207%29.jpg | 同 | NIST | 2800x1575 | 専門家（同） | 試験（実物大） | 同 |
| 69 | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%287%20of%207%29.jpg | わざと腐食させた鉄筋の標本（ワシントン大） | NIST | 2800x1709 | 専門家（同） | 試験（実物大） | 同 |
| 70 | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%288%20of%207%29.jpg | 床版の上面のひび（ワシントン大） | NIST | 2800x1608 | 専門家（同） | 試験（実物大） | 同 |
| 71 | https://www.nist.gov/sites/default/files/images/2025/06/23/NCST%20Investigation%20Update%20June%202025%20%283%20of%207%29.jpg | 床版・梁・柱の試験中（ミネソタ大 MAST） | NIST | 2800x1948 | 記載なし | 試験（実物大） | 同 |
| 72 | https://www.nist.gov/sites/default/files/images/2025/06/20/NCST%20Investigation%20Update%20June%202025%20%2810%20of%201%29.jpg | 試験の後の標本の裏側を調べる（ミネソタ大） | NIST | 2800x1676 | 調査員（公務） | 試験（実物大） | 同 |
| 73 | https://www.nist.gov/sites/default/files/images/2026/06/22/Slide_34.png | 押し抜きせん断の図（床版が柱のまわりで曲がり割れる） | NIST | 2800x1575 | なし（図） | 図 | 同 |
| 74 | https://www.nist.gov/sites/default/files/styles/2800_x_2800_limit/public/images/2026/06/22/PunchingShear_001.gif | 押し抜きせん断の動く図（**既出＝materials.md §2 ss_gif**） | NIST | 1920x1080・167コマ | なし（図） | 図 | — |

---

## §2 記録映像（この事故の動く映像）— 機関・PD を先に

### §2-1 NIST（Kaltura 29本＋YouTube 5本〔頁の埋め込み2・チャンネルだけ3〕）

- 頁：news-and-updates（上記）＝27本（TF 1・記者会見 2・タイムラプス 2・B-Roll 8・NCST Insider 14〔Kaltura 12・YouTube 2〕）。ほかの NIST の頁に4本（Kaltura）。YouTube の NIST のチャンネル（@NIST）にだけある3本。
- 器の大きさ・長さ・登録日＝Kaltura の公開 API（2026-10-05）。Kaltura 29本とも status 2（公開中）。登録者はすべて nist.gov のアカウント（アドレスは書かない）。B-Roll #1 の tags に「pao」（広報室）。
- 根拠は全部「**A と推定**」（NIST が配る・撮影者の記載なし）。旧版の判断（materials.md §2・§3 #5）のとおり、大学の試験の区間は撮影者が大学の可能性＝未確認。

| # | 題（Kaltura／YouTube） | 頁・ID | 日付 | 長さ | 器 | 中身（頁の説明） | 人の写り | 場面 | 備考 |
|---:|---|---|---|---:|---|---|---|---|---|
| V1 | NCST Champlain Towers South Investigation \| Technical Findings (June 2026) | news-and-updates・`1_vezbt9jw` | 公表 2026-06-22（登録 06-09） | 77.3分 | 3840x2160 | 技術的知見の全編（共同責任者2人の説明） | 共同責任者（公務） | 解説・図 | **既出**（TF 動画＝スライドの出どころ）。©2021 Used with permission の頁あり（materials.md §2）。CONTENT WARNING＝第3・4章 |
| V2 | NIST Announces Expert Team to Investigate the Champlain Towers South Collapse | 同・`1_e2qn2w2y` | 頁に日付なし（登録 2021-08-25） | 41.1分 | 1280x720 | 調査団の顔ぶれの発表の記者会見 | NIST の幹部・調査員（公務） | 解説 | 中身は未見 |
| V3 | NIST Announces Full Investigation on Champlain Towers South Collapse | 同・`1_0sqily3j` | 本調査の発表 2021-06-30（B02）・登録 2021-07-02 | 6.3分 | 1920x1014 | 本調査の開始の発表 | NIST の幹部（公務） | 解説 | 器が B-Roll #1 と同じ 1920x1014（中身は未見） |
| V4 | NCST Slab-beam-column test timelapse | 同・`1_gvpcaamy` | 登録 2025-04-09 | 6.8秒 | 3840x2160 | ミネソタ大の床版・梁・柱の複製が壊れる | なし | 試験 | **既出**（ss_tl・NIST の透かし） |
| V5 | NCST Slab-beam-column test set-up timelapse | 同・`1_zno86q01` | 登録 2025-04-09 | 10.4秒 | 3840x2160 | ミネソタ大で複製を試験の前に据える | 研究者（説明から）＝公的調査の任務 | 試験 | 旧版未使用。大学の撮影の可能性＝未確認 |
| V6 | B-Roll Video Reel #1 | 同・`1_ju6nndhb` | 登録 2021-07-12 | 250.2秒 | 1920x1014 | 崩落現場・残った棟・捜索隊・証拠テント（materials.md §2） | 捜索隊（公務）・3:24以降インタビュー | 捜索・残った棟 | **既出**（ss_b1） |
| V7 | B-Roll Video Reel #2 | 同・`1_64zdekws` | 登録 2021-08-25 | 309.8秒 | 4096x2160 | 海岸線の空撮・現場・ドローン・インタビュー | 調査員（公務） | 捜索（空撮） | **既出**（ss_b2） |
| V8 | B-Roll Reel #3 | 同・`1_h4yeyz2f` | 登録 2022-02-01 | 74.3秒 | 1920x1080 | 倉庫で部材と鉄筋を測る | 調査員（公務） | 証拠 | **既出**（ss_b3） |
| V9 | B-Roll Reel #4 | 同・`1_jvdq95ze` | 登録 2023-05-10 | 216.3秒 | 1920x1080 | 部材の梱包・積み込み・搬送 | 不明＝要目視 | 証拠 | **既出**（ss_b4） |
| V10 | B-Roll Reel #5 \| Core Drilling | 同・`1_ecar0b6h` | 登録 2023-06-23 | 333.4秒 | 3840x2160 | 倉庫の部材・コア抜き | 調査員（公務） | 証拠 | **既出**（ss_b5） |
| V11 | B-Roll Reel #6 \| Concrete Core Testing | 同・`1_zdyysoml` | 登録 2024-03-01 | 263.2秒 | 3840x2160 | コアの試験 | 不明 | 試験 | **既出**（ss_b6） |
| V12 | B-Roll Reel #7 \| Rebar Testing | 同・`1_glesd05g` | 登録 2024-09-11 | 337.0秒 | 3840x2160 | 鉄筋の試験 | 不明 | 試験 | **既出**（ss_b7） |
| V13 | B-Roll Reel #8 \| Pool-Deck and Tower Interface … | 同・`1_lebmphjw` | 登録 2025-05-27 | 207.0秒 | 3840x2160 | 実物大の試験（2:08〜ワシントン大） | 研究者 | 試験 | **既出**（ss_b8） |
| V14 | NCST Insider \| feat. Emel Ganapati | 同・`1_vr8m18z6`（YouTube `ehlYSktF0uw`） | 登録 2022-02-09 | 80.5秒 | 1920x1080 | 社会科学チームの責任者の紹介 | 本人の顔（調査団＝公務） | 解説（人） | 顔の寄り |
| V15 | NCST Insider \| feat. Kamel Saidi | 同・`1_8eit9oeo`（YouTube `dri_sx0x6n8`） | 登録 2022-04-04 | 102.3秒 | 1920x1080 | 遠隔計測と可視化の共同責任者 | 同 | 解説（人） | 同 |
| V16 | NCST Insider \| feat. Malcolm Ammons | 同・`1_vtol0bpd`（YouTube `-TIAaOdmQp8`） | 登録 2022-09-12 | 102.2秒 | 1920x1080 | 複数のチームを支える調査員 | 同 | 解説（人） | 同 |
| V17 | NCST Insider \| feat. Christopher Segura | 同・`1_vmg67k8j`（YouTube `rTM2-IoSHrI`） | 登録 2023-05-10 | 103.9秒 | 3840x2160 | 証拠保全の共同責任者 | 同 | 解説（人） | 同 |
| V18 | NCST Insider \| feat. Marisa McCormick | 同・`1_vxgzbmhk`（YouTube `b5TJpwe3V08`） | 登録 2023-05-10 | 97.2秒 | 1920x1080 | 証拠保全と材料の調査員 | 同 | 解説（人） | 同 |
| V19 | NCST Insider \| feat. David Goodwin | 同・`1_ltiebacc`（YouTube `voIvgWfC9o8`） | 登録 2023-05-10 | 78.9秒 | 1920x1080 | 証拠保全の共同責任者 | 同 | 解説（人） | 同 |
| V20 | NCST Insider \| feat. Georgette Hlepas | 同・`1_rbma6too`（YouTube `9adwpPTAVCc`） | 登録 2023-06-14 | 91.5秒 | 1920x1080 | 遠隔計測と可視化の共同責任者 | 同 | 解説（人） | 同 |
| V21 | NCST Insider \| feat. Vincent Lee | 同・`1_gfz9h38y`（YouTube `_Nv_o2cBkHk`） | 登録 2023-06-14 | 109.1秒 | 3840x2160 | 遠隔計測と可視化の調査員 | 同 | 解説（人） | 同 |
| V22 | NCST Insider \| feat. Fahim Sadek | 同・`1_i1rzn8bc`（YouTube `OpgiCNvJ-xs`） | 登録 2024-02-26 | 104.9秒 | 3840x2160 | 構造の共同責任者 | 同 | 解説（人） | 同 |
| V23 | NCST Insider \| feat. Jim Harris | 同・`1_exr87xie`（YouTube `FpywuoHxxCw`） | 登録 2025-04-10 | 131.6秒 | 3840x2160 | 建物と規準の歴史の共同責任者 | 同 | 解説（人） | 同 |
| V24 | NCST Insider \| feat. Jack Moehle | 同・`1_uxc5w2y6`（YouTube `SZH3c9p4740`） | 登録 2025-03-12 | 104.3秒 | 3840x2160 | 構造の共同責任者 | 同 | 解説（人） | 同 |
| V25 | NCST Insider \| feat. Sissy Nikolaou | 同・YouTube `_nVns1FTP9A` https://www.youtube.com/watch?v=_nVns1FTP9A | — | 139秒 | 3840x2160 | 地盤の共同責任者 | 同 | 解説（人） | YouTube だけ |
| V26 | NCST Insider \| feat. Youssef Hashash | 同・YouTube `IBWezPN4Ep8` https://www.youtube.com/watch?v=IBWezPN4Ep8 | — | 119秒 | 3840x2160 | 地盤の共同責任者 | 同 | 解説（人） | YouTube だけ |
| V27 | NCST Insider \| feat. Ken Hover | 同・`1_22ham8xr`（YouTube `2OKOX0mjS5I`） | 登録 2026-06-03 | 214.1秒 | 3840x2160 | 材料の共同責任者 | 同 | 解説（人） | 同 |
| V28 | NCST Champlain Tower South Collapse Investigation \| Technical Update (June 2025) | https://www.nist.gov/news-events/news/2025/06/nist-releases-extensive-video-update-champlain-towers-south-investigation ・`1_v0mapuu4` | 登録 2025-06-12 | 89.6分 | 3840x2160 | 調査の歴史と進み具合・予備的な知見（責任者2人） | 調査責任者（公務） | 解説・図 | **旧版で未記録**。スライドに ©2021 の第三者部分がある可能性（TF と同じ型＝未確認） |
| V29 | NCST Insider \| feat. Jonathan Weigand | https://www.nist.gov/news-events/news/2026/09/nist-provides-updates-national-construction-safety-team-activities ・`1_1rrnx15n`（YouTube `dsyqwrFSOeU`） | 登録 2026-09-18（YouTube 09-29） | 108.1秒 | 3840x2160 | 建物と規準の歴史の共同責任者 | 本人の顔（公務） | 解説（人） | 新しい（旧版の後） |
| V30 | NCST Insider \| feat. Scott Jones | 同・`1_lcet6ouz`（YouTube `t02bQXzD4A0`） | 登録 2026-09-18（YouTube 09-29） | 108.7秒 | 3840x2160 | 材料の共同責任者 | 同 | 解説（人） | 新しい |
| V31 | 3D point cloud flythrough over Champlain Tower South building specimens | https://www.nist.gov/news-events/news/2024/11/nist-transfers-evidence-champlain-towers-south-miami-dade-police-department ・`1_sem63924` | 登録 2024-10-23 | 46.8秒 | 5344x3264 | 倉庫の部材の点群（約17億点・120回超の走査をつないだ）のフライスルー | なし（点群） | 証拠 | **旧版で未記録**。人のいない証拠の動く絵 |
| V32 | NCST Champlain Towers South Investigation \| Summary of Technical Findings (June 2026) | https://www.youtube.com/watch?v=derKcYl1-Hk | 2026-06-22 | 7分17秒 | 3840x2160 | TF の要約版 | 共同責任者（公務） | 解説・図 | YouTube だけ（Kaltura では未確認）。TF の ©2021 部分を含むかは未確認 |
| V33 | Champlain Tower South Collapse Investigation \| Public Meeting Summary (February 2025) | https://www.youtube.com/watch?v=05SNgaavuvY | 2025-02-05 | 4分19秒 | 3840x2160 | その年の進み具合の要約 | 調査責任者（公務） | 解説 | YouTube だけ |
| V34 | Champlain Towers South Collapse Investigation Update \| June 2025 | https://www.youtube.com/watch?v=aDBTOYvBi6o | 2025-06-23 | 2分00秒 | 2160x3840（縦） | 2025年6月の要約（縦型） | 不明 | 解説 | 縦型＝本編に不向き |

### §2-2 DVIDS の動画

- **0本**（09-04 のブラウザでの全頁走査「Surfside building collapse」「Champlain Towers」「Surfside」＝アメリア島の浚渫1本だけ＝無関係）。
- 2026-10-05 は検索頁・タグ頁が WAF で 202／405（読めない）＝**再測できていない**。FEMA の YouTube（@FEMA）のチャンネル内検索「Surfside」も該当なし（出たのは US&R の訓練など）。

### §2-3 ホワイトハウス（2021-07-01 の大統領の訪問）

- 動画は YouTube の「The Biden White House」（@WhiteHouse46）に2本。根拠＝**A と推定**（ホワイトハウスの職務の撮影・撮影者の記載なし）。
- 写真：ホワイトハウスの公式写真（Flickr）は**見つからず**（WebSearch・Commons 検索とも0件）。連邦の写真は DVIDS の 6722815（FEMA・§1-1 #16）がある。
- 文字の記録：大統領の発言の書き起こしは UCSB の American Presidency Project（例 https://www.presidency.ucsb.edu/documents/remarks-prior-briefing-the-surfside-residential-building-collapse-miami-beach-florida ）＝第三者の集成（一次は旧政権のホワイトハウスの頁＝未確認）。

| # | 題 | URL | 公開 | 長さ | 器 | 中身（説明） | 人の写り | 場面 |
|---:|---|---|---|---:|---|---|---|---|
| W1 | President Biden Receives a Command Briefing | https://www.youtube.com/watch?v=GIwDDurtIgE | 2021-07-01 | 8分08秒 | 1920x1080 | 「Incident Commander」の郡長・州知事・地元の幹部・救助隊から指揮の説明を受ける（Surfside, FL） | 公人・救助隊。私人は記載なし＝要目視 | 捜索（大統領の訪問） |
| W2 | President Biden Delivers Remarks | https://www.youtube.com/watch?v=wiQ6_b66tWY | 2021-07-01 | 14分34秒 | 1280x720 | 説明は「Miami, FL」だけ＝同じ日の公開でサーフサイドの件と**推定**（要確認） | 大統領（公人）。**聴衆に遺族がいるかは記載なし＝要目視** | 捜索（大統領の発言） |

### §2-4 マイアミ・デイド郡・MDFR・サーフサイド町

- 根拠＝**PD-FLGov の可能性（要判断）**（郡・町＝§105 の外。断定しない）。
- 町の YouTube は見つからず（@TownofSurfside・@TownOfSurfsideFL＝404）。郡の警察（@MiamiDadePD）のチャンネル内検索「Surfside」＝0本。
- 郡の記者会見の全編は**報道各社の YouTube だけ**（ABC News・WPLG・CBS Miami・NBC 6・Washington Post ほか＝報道＝不可）。郡のチャンネルには会見の動画が無い（チャンネル内検索の結果）。

| # | 題 | URL | 公開 | 長さ | 器 | 中身（説明） | 人の写り | 場面 |
|---:|---|---|---|---:|---|---|---|---|
| M1 | Surfside One Year Anniversary（MDFR） | https://www.youtube.com/watch?v=msJTZ7OVMbQ | 2022-06-24 | 3分58秒 | 1920x1080 | 1年の追悼。「崩落の後の数週間の救助隊の働き」に触れる＝**対応の映像を含むかは要目視** | 消防（公務）。私人は不明 | 追悼（捜索の回想の可能性） |
| M2 | Surfside Remembrance Ceremony（MDFR） | https://www.youtube.com/watch?v=BFeAFSPUqbc | 2023-06-24 | 55分44秒 | 1920x1080 | 2年の追悼式の中継 | **遺族・住民（私人）が写る可能性が高い（推定）** | 追悼 |
| M3 | Surfside Remembrance Ceremony（MDFR・中継の枠） | https://www.youtube.com/watch?v=PbdlSm43txk | 2023-06-24 | 0（LIVE_STREAM_OFFLINE） | — | 中身なし | — | — |
| M4 | 同 | https://www.youtube.com/watch?v=knkpPL864Pc | 2023-06-24 | 0（同） | — | 中身なし | — | — |
| M5 | #SurfsideStrong - English（郡） | https://www.youtube.com/watch?v=6C10HR7JeB4 | 2021-07-06 | 21秒 | 1920x1080 | 郡の呼びかけ（犠牲者・家族・救助隊に心を寄せて） | 不明＝要目視 | 追悼（当時） |
| M6 | #SurfsideStrong - Spanish（郡） | https://www.youtube.com/watch?v=3CfpdyBxlQc | 2021-07 ごろ（未測） | 21秒 | 未測 | M5 のスペイン語版 | 同 | 同 |
| M7 | #SurfsideStrong - Creole（郡） | https://www.youtube.com/watch?v=MVFXKyZ_pPk | 2021-07 ごろ（未測） | 21秒 | 未測 | M5 のクレオール語版 | 同 | 同 |
| M8 | #SurfsideStrong - 2 Year Remembrance（郡） | https://www.youtube.com/watch?v=pwT0PA_mzh8 | 2023-06-24 | 33秒 | 1920x1080 | 2年の追悼 | 不明 | 追悼 |
| M9 | Surfside 3 Year（郡） | https://www.youtube.com/watch?v=najxwXPZzZE | 2024-06-24 | 30秒 | 1080x1920（縦） | 3年の追悼 | 不明 | 追悼 |

### §2-5 Commons の動く映像

| # | ファイル | 中身 | 日付 | 作者 | 器 | ライセンス | 人の写り | 場面 |
|---:|---|---|---|---|---|---|---|---|
| I1 | https://commons.wikimedia.org/wiki/File:IDF_Aid_Mission_to_Surfside_condominium_building_collapse,_June_2021._I.webm | イスラエルの救助団の活動（説明はヘブライ語＝3D モデルで捜索を支えた） | 2021-06-30 | IDF Spokesperson's Unit | 1920x1080 | **CC BY-SA 3.0**（VRT の許諾） | 外国の救助隊（公務と推定）＝要目視 | 捜索（**現場の動く映像・1920幅**） |
| I2 | https://commons.wikimedia.org/wiki/File:IDF_Aid_Mission_to_Surfside_condominium_building_collapse,_June_2021._II.webm | 同 | 2021-06-30 | 同 | 1920x1080 | **CC BY-SA 3.0** | 同 | 捜索 |
| X1 | https://commons.wikimedia.org/wiki/File:Collapse_process_of_Champlain_Towers_South_2021-07-23.webm | 崩落の過程の大まかな再現（利用者の作図・NIST の知見の前） | 2021-07-23 | Asanagi（Commons 利用者） | 874x656 | **CC0**（B） | なし | 図（作図・正確さは未検証） |
| X2 | https://commons.wikimedia.org/wiki/File:Collapse_process_of_Champlain_Towers_South_2021-07-23.gif | X1 の GIF | 2021-07-23 | 同 | 320x240 | CC0 | なし | 図 |

### §2-6 崩落の瞬間・直前の映像（報道・私人＝使えるかは判断しない）

| # | 映像 | 出どころ（分かった範囲） | NIST の扱い | 判定の印 |
|---:|---|---|---|---|
| R1 | **崩落の瞬間の監視カメラ（南面）** | 報道（2021-06-24）＝「隣の建物（adjacent／nearby building）の監視カメラ」とだけ（ABC7 https://abc7chicago.com/building-collapse-video-surfside-miami-of/10827847/ ・NBC Miami https://www.nbcmiami.com/news/local/video-shows-wing-of-surfside-condo-building-collapse-in-seconds/2479955/ ）。**カメラの持ち主の建物名は報道の本文で確かめられず**。最初の配信は「WSVN 7News が入手」と検索結果の要約にある（Mediaite の本文は 403 で未確認） | TF の語り（TR 0314）「Footage from a security camera looking onto the south face of CTS」。A01 p.47・49・50・51＝「**© 2021, Used with permission. Annotated by NIST**」 | 報道・第三者＝**引用の候補**（のちの工程で検討） |
| R2 | 11スタックの住戸の中の防犯カメラ | 住戸の持ち主（私人）＝NIST の語り（TR 0335） | TF 3221〜3296秒のスライド（OCR に ©2021 … permission の痕） | 私人＝不可（引用の候補にするかは判断せず） |
| R3 | 上層階の廊下の防犯カメラ（2021-06-24 01:21:55 EDT〜） | 建物のカメラ（管理組合・私的）＝NIST の語り（TR 0349） | TF 3321〜3346秒「©2021 used with permission」（OCR） | 同上 |
| R4 | 北側の目撃者が撮ったプールデッキの崩落（01:18:18） | 私人＝NIST の語り（TR 0203〜0204） | TF で1コマを超解像して使用 | 私人＝不可 |
| R5 | 崩落の数分前にガレージへ水が流れ込む映像 | 近くのホテルの宿泊客（私人）・Storyful が配信（報道の要約） | — | 私人・報道＝不可 |
| R6 | 7階の住戸の動体カメラ（落下物） | 住民（私人）＝報道（R2 と同じ映像の可能性＝未確認） | — | 私人＝不可 |
| R7 | 警察のボディカメラ（初動） | 報道（WSVN・WFTV ほか 2021-08-03 ごろ）「警察がボディカメラの映像を公開」＝**どの警察か・一次の置き場は未確認** | — | 公的機関の記録の可能性＝要確認（PD-FLGov の可能性）。救助の場面に私人（生存者）が写る可能性が高い（推定） |
| R8 | 報道の「WEB EXTRA」（がれきの上の救助隊のドローン映像・MDFR の指揮所の中 ほか） | CBS Miami の YouTube（例 https://www.youtube.com/watch?v=BBGPbP-kzvM ・ https://www.youtube.com/watch?v=ppV2gyhNMEU ）＝**撮影元は未確認**（郡の提供か報道の撮影か） | — | 報道＝不可（撮影元が郡と分かれば M 系と同じ扱い） |

---

## §3 一次資料の追加（写しは `src/`・台帳は `sources_add_2026-10-05.md`）

| 問い | 一次で取れたこと | 取れなかったこと |
|---|---|---|
| **立ったまま残った棟から救出された人数** | 郡（2022 State of the County「Tragedy in Surfside」・B04）＝「rescuing **37 occupants from the structure and rubble**」（建物とがれきから合わせて37人）。町の広報誌（2021年8月・B06）p.2＝はしご車（cherry pickers）で**階ごとにバルコニーに取り残された住民を救った**（人数なし）。町の警察の月報（B05）＝残りの建物の住民を避難させ Community Center へ（人数なし） | 「残った棟から35人」は**報道どまり**（MDFR の副署長〔当時〕の 2021-06-24 の会見の発言として、「残った建物から35人・がれきから2人」）。会見の全編は報道各社の YouTube だけで、字幕の文字も取れなかった＝**一次の文字は未取得**。⚠️ 37 から大陪審の「がれきから14歳の子ども1人」を引いて 36 としない（報道は「がれきから2人・うち1人は病院で死亡」と伝える＝数え方が違う） |
| **残った棟の解体（2021-07-04 ごろ）** | 郡の発表（2021-07-04・B03）＝「Between 10 p.m. on Sunday, July 4, 2021 and 3 a.m. on Monday, July 5, … the vacant Champlain Towers South … structure that remains standing will be demolished.」（**予告**）・爆破区域＝半径300フィート。実施したこと＝町の広報誌 p.4「the controlled demolition of the remaining structure」（日付なし）・郡長のメモ（B07）「controlled demolition of the remaining structure」（日付なし）・NIST の写真の説明「collapsed and imploded sections」（§1-3 #0） | 実施の時刻（22時30分ごろ）は報道どまり（legend H07b のまま）。州知事の 2021-07-03 の発表（flgov.com）は 404 |
| **捜索の終了（2021-07-23 ごろ）** | 町（A12・既存）＝「July 20th at 8:03 pm marks the end of the heroic search and recovery efforts when the final person was recovered」。NIST（B08）＝「By the end of July 2021, all of the evidence was moved to secure locations」・証拠の管理が NIST へ移ったのは 2022-01-28 | **郡の 2021-07-23 の発表**（https://www.miamidade.gov/releases/2021-07-23-mayor-surfside-update.asp ＝今は 404）の写しは Wayback（20210725065033）にあるが **429（ボット判定）で読めず**、archive.today（20211012162908）は CAPTCHA＝読まない。**7/23 を一次で確かめられていない** |
| **GAO の報告** | **取れた**（B01・GAO-24-106558 の Accessible Version・17頁）。gao.gov は curl・requests で 403（Akamai）だったが、WebFetch の取得物（PDF）が残った＝md5 を取って保存。中身：98人・6/25 の緊急事態宣言・FEMA 約1億690万ドル（捜索ほか1,690万／個人支援110万／州と地元への補助8,470万＝がれき撤去・**残った棟の解体**を含む）・US&R 5隊（各70〜80人）＋支援チーム・陸軍工兵隊が「がれきの山と残った棟」を監視・NIST $15,389,750 | 救出の人数・解体と捜索終了の日付は**書かれていない** |
| （参考）崩落の時刻の表記 | 町＝1:22 a.m.（A12）／FEMA＝1:23 a.m.（B02）／町の警察＝0120 hours（B05）／郡の警察の発表＝approx. 1:20 a.m.（2021-06-26・保存せず＝犠牲者の実名を含む）／NIST の廊下の映像の時刻＝01:21:55 EDT〜（TF） | — |

---

## §4 集計

### 写真（§1）＝141行

| 出どころ | 点数 | A | A と推定・要判断 | A だが使わない（DoD） | PD-FLGov の可能性 | CC BY | CC BY-SA |
|---|---:|---:|---:|---:|---:|---:|---:|
| DVIDS（FEMA ほか） | 29 | 26 | 2（US&R の広報官） | 1（空軍の牧師） | — | — | — |
| Commons カテゴリ内の写真 | 18 | — | — | — | 10（MDFR・うち切り出し4） | 1（Jurvetson） | 7（崩落前2・IDF 5） |
| Commons カテゴリ外（DHS） | 15 | 15 | — | — | — | — | — |
| Commons 崩落前の候補（要目視） | 4 | — | — | — | — | 3 | 1 |
| NIST Photo Gallery | 75 | 75 | — | — | — | — | — |
| **計** | **141** | **116** | **2** | **1** | **10** | **4** | **8** |

- 根拠 B・C・D＝0点（写真）。報道の写真は在庫に入れていない。
- 1280幅以上の横長で「現場の救助」と説明にあるもの：DVIDS 18／MDFR 2（C3・C6。C5 は正方形1512）／IDF 5（1583〜1600幅・BY-SA）。

**人の写り（説明文から）**

| 区分 | 点数 | 内訳 |
|---|---:|---|
| 公務・公人（説明に明記） | 97 | DVIDS 29（救助隊・FEMA・公人・牧師）／MDFR 7（C3〜C6・C8〜C10＝消防・救助隊）／IDF 5（推定）／DHS 15（公人）／NIST 41（調査員・技術者・研究者） |
| 人の記載なし | 39 | MDFR 3（C1・C2・C7）／崩落前2（C11・C12）／Jurvetson 1／NIST 33 |
| 不明＝要目視 | 5 | 崩落前の候補4／NIST #30（手元） |
| 私人の顔が写ると説明にあるもの | **0** | （DVIDS の現場・DHS の追悼の場・W2 の聴衆は「私人の有無は不明＝要目視」） |
| 血・遺体の記載 | **0** | — |

- ⚠️ 「公務」の 97 のうち、**私人が背景に写るかは説明から分からない**（とくに DHS 15＝追悼の場・DVIDS の現場22）。
- NIST の「人の記載なし」33＝#0・11・17・18・19・20・22・23・28・29・31・32・33・34・39・41・42・48・49・50・51・53・56〜62・65・71・73・74（図2を含む）。

**場面ごと（写真141）**

| 場面 | 点数 | 内訳 |
|---|---:|---|
| 崩落前 | 6 | Commons BY-SA 4.0 2（1280未満）＋候補4（写っているか要目視） |
| 直後（6/24） | 10 | MDFR 6＋切り出し4（うち「残った棟」と説明にあるもの4＝C1・C2・C4・C7） |
| 捜索（6/25〜7/23） | 38 | DVIDS 28（現場22・公人と会議5・休息1）／IDF 5／NIST 5（#17・18・19・24・48） |
| 残った棟（再掲） | 5 | C1・C2・C4・C7＋NIST #17（09-04 の実見） |
| **解体（7/4〜5）** | **0** | 機関・PD の写真は見つからず |
| 跡地（撤去の後） | 16 | DHS 15（2021-08-19）＋Jurvetson 1（2021-10-04） |
| 証拠 | 35 | NIST 32（現場の仮置き場 14・倉庫と搬送 15・ハードディスク 3）＋調査の室内 3（#43・44・54） |
| 試験 | 33 | NIST（材料 10・実物大 23） |
| 図 | 2 | NIST #73・#74（#74 は既出） |
| 無関係 | 1 | DVIDS #20（空軍の牧師の肖像） |
| **計（再掲を除く）** | **141** | |

### 記録映像（§2）＝57行

| 出どころ | 本数 | 根拠 | 既出（materials.md §2） | 新しく記録 |
|---|---:|---|---:|---:|
| NIST（Kaltura 29・YouTube 5） | 34 | A と推定（第三者部分あり＝V1・V28〔推定〕・V32〔未確認〕） | 10（V1＝materials.md §2 の参考の行・V4・V6〜V13。ss_gif は §1-3 #74） | 24 |
| ホワイトハウス | 2 | A と推定 | 0 | 2 |
| 郡・MDFR | 9 | PD-FLGov の可能性（要判断） | 0 | 9 |
| Commons（IDF） | 2 | CC BY-SA 3.0 | 0 | 2 |
| Commons（作図） | 2 | CC0（B） | 0 | 2 |
| DVIDS | 0 | — | — | — |
| 報道・私人（R1〜R8） | 8 | 不可／引用の候補 | 0 | 8 |
| **計** | **57** | | | |

| 場面（動く映像） | 本数 | 内訳 |
|---|---:|---|
| 崩落の瞬間・直前 | 6 | R1〜R6（**全部 報道・私人**） |
| 直後（初動） | 1 | R7（警察のボディカメラ・要確認） |
| 捜索 | 7 | V6・V7（既出）／I1・I2（BY-SA）／W1・W2／R8 |
| 残った棟（再掲） | 1 | V6（既出） |
| **解体** | **0** | 機関・PD の動画は見つからず（報道の中継だけ＝未記録） |
| 証拠 | 4 | V8・V9・V10（既出）／V31（点群） |
| 試験 | 5 | V4・V11・V12・V13（既出）／V5 |
| 解説（調査団） | 23 | V1〜V3・V14〜V30・V32〜V34（Insider 16・会見2・TF 1・2025 更新 1・要約3） |
| 追悼 | 9 | M1〜M9（M3・M4 は中身なし） |
| 図（作図） | 2 | X1・X2 |
| **計（再掲を除く）** | **57** | |

---

## §5 判断が要るもの（ここでは決めない）

1. **PD-FLGov（郡・町の写真と動画）**：MDFR の写真10点（C1〜C10・最大 2048x1536）と郡・MDFR の YouTube 9本（M1〜M9）。郡・町は §105 の外。Commons は {{PD-FLGov}}（フロリダ州の公記録法・Microdecisions v. Skinner, Fla. 2d DCA 2004）。**使うかはカズヤくんの判断**。旧版は「Miami-Dade Fire Rescue の PD 3点」と書いた＝根拠の書き方を「PD-FLGov の可能性」に直す要あり（materials.md §4 の指摘どおり）。
2. **崩落の瞬間の監視カメラ（R1）**：持ち主の建物名は報道でも確かめられず。NIST は「© 2021, Used with permission. Annotated by NIST」で使う＝NIST の許諾はこちらに移らない。**引用の要件で検討**（のちの工程）。
3. **CC BY-SA**：IDF の写真5（C14〜C18）・**動画2（I1・I2＝1920x1080 の現場の動く映像）**・崩落前2（C11・C12・1280未満）・候補 P4。原則不可・額装の例外あり＝印だけ。IDF は外国軍の記章が写る可能性。
4. **崩落前の写真**：機関・PD は0点のまま。CC BY の候補3（P1〜P3）は**建物が写っているかを原寸で見る**まで使えるか分からない（P1 は 4000x3000）。
5. **DVIDS の US&R 広報官の写真2点（#22・#23）**：撮影者が FEMA の職員でなく隊の広報官＝§105 の「連邦の職員」に当たるかは要判断（どちらも 768 幅以下＝使い道も小さい）。
6. **DVIDS の空軍の牧師（#20）**：DoD の断り書きの義務＝使わない（旧版の判断どおり・現場でもない）。
7. **DHS の写真15点（D1〜D15）**：連邦＝A だが、**追悼の場＝犠牲者の写真・遺族が写る可能性**＝原寸で見てから。
8. **ホワイトハウスの W2・MDFR の M2（追悼式）**：遺族・住民（私人）が写る可能性。
9. **DVIDS の日付の食い違い**：#2（説明 July 27）・#5〜#8（説明 July 1）と頁の Date Taken（06.27・VIRIN 210627）が合わない＝画面に日付を出すなら頁の Date Taken か説明かを決める。
10. **35人**：一次の文字が無い。台本で数を言うなら「郡の発表＝建物とがれきから37人」の形か、帰属つきの報道（「消防によると…35人」）か。
11. **捜索の終了日**：町の「7/20 20:03＝最後の1人の収容」は一次で取れた。「7/23」は郡の発表が読めず＝言うなら報道どまり。
12. **GAO の図の写真**：p.4 の出典「Indiana Urban Search and Rescue Task Force 1 and FEMA (images)」＝GAO の文書は連邦だが**写真は隊（地方の消防の可能性）と FEMA**＝紙面の引用にするなら要判断。
13. **V28（2025年6月の技術更新・89.6分）・V32（2026年の要約版）**：TF と同じく ©2021 の第三者部分を含む可能性（未確認）＝使う区間を決めるときに頁ごとに確かめる。
14. **V5（据え付けのタイムラプス）・B-Roll #8・タイムラプス**：大学の撮影の可能性（materials.md §3 #5 のまま）。

## 関連
- `ref/ep19/materials.md`（旧版の69点と記録映像10本）／`ref/ep19/sources.md`（A01〜A19）／`ref/ep19/sources_add_2026-10-05.md`（B01〜B08）／`ref/ep19/legend_2026-10-05.md`（H07a・H07b）
- Vault `事故検証-サーフサイド-素材実測の全文-20260904`（§3〜§6）
