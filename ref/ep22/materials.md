# 22本目 タイタン号（リメイク）── 素材の棚卸し（① 素材の係）

- 作成：2026-10-13（① 棚卸し）／**取得はしていない**（頁・凡例・API の JSON・HEAD・ffprobe の頭だけで判定）
- 画像・動画は**1枚も開いていない**。中身（写っている物・焼き込み・顔・遺体の有無）の目視は後のチャットで人がやる
- 生のメモ・機械の出力：`ref/ep22/src/materials_raw/`（§7 に一覧）

## 記号

| 記号 | 意味 |
|---|---|
| **A** | 米連邦の職員が職務で作った物（17 U.S.C. §105）＝最初から著作権が無い |
| **B** | 持ち主が自分で手放した（PDM・CC0） |
| **C** | 更新されなかった米国の著作物（PD US not renewed） |
| **D** | 撮影国の短い保護期間で切れた物 |
| **第三者** | 機関の報告書・機関の頁に載っていても、撮った人が機関の外（OceanGate・Pelagic・報道・個人など）。**サムネに使わない・本編は引用の要件でだけ**（出典を明記・解説が主・必要最小限・改変しない＝色も切り出しもせず額装） |
| **Crown** | カナダ政府の著作物（Crown copyright）。条件は §1-5 |
| ◎ | 権利の根拠がはっきり（A/B など）・使える |
| ○ | 使える（根拠に弱い所あり、または第三者だが引用で使える主役の絵） |
| △ | 引用の要件でだけ／イメージ扱い／中身か権利が未確認 |
| × | 使わない（理由を書く） |
| 器 | 器の札（ffprobe・HLS の一覧・API が名乗る幅×高）。**実効の幅は未測定**（周波数の崖・黒帯の幅は映像方針で測る） |

---

## §0 先に結論

1. 🔴 **冒頭（約1分）を実写の動く映像で組めるか → 組める見込み。** 事故そのものの実写＝**2023-06-22 に残骸を見つけたときの ROV の映像（2本・器 1920×1080）**があり、捜索と発表の実写＝**米沿岸警備隊（USCG）の記者会見と捜索の B-roll（A・器 1280〜2720）**がある。
   - ⚠️ ただし主役の ROV 映像は **第三者（Pelagic Research Services の ROV「Odysseus」）**。NTSB のドケットも「Source: Pelagic Research Services, Odysseus ROV」と書く＝A ではない。**引用の要件（切らない・色を変えない・額装）で使う**と、左上の焼き込み **「Depth (m): 3775.x」** が画面に残る（台本の「水深3,346メートルで消えた」と別の数字。§6 で扱う）
   - ⚠️ **事故の瞬間の映像は存在しない**（MBI「There were no witnesses to the implosion or video evidence recovered of the implosion」・タイタンの外部カメラの SD カードは最後の記録が 2023-05-16＝NTSB の Underwater Camera 報告）
2. **【映像あり】の札**：**付けられる見込み**（器 1920×1080 の動く実写が、ROV 2本＋USCG の A が7本以上）。**条件＝映像方針で上位3本の実効の幅を測り 1280 以上を確かめること**（今は器の札だけ）。
3. 旧版の写真 26点の判定し直し：**◎15・○1・△9・×1**（§3）。旧版の誤り＝**ROV の静止画2点を画面で「パブリックドメイン」と出していた**／**第三者の図（OceanGate・Comber・Harvey・Taragel・Pelagic）を暗幕＋図の重ねで「地」に敷いていた＝今の決まりでは改変**／「A. Harvey（個人）」は**会社の見込み（A. Harvey の港湾基地）**／図4は**上が NTSB の線画**で Comber の写真は下だけ／図22は「記載なし」でなく **Data source: MTS** の注あり／rov_tailcone の Commons ファイルの出どころは **テレビ局（6abc）の YouTube の再アップ**

---

## §1 冒頭の実写の候補（順位つき）

### §1-1 順位表（冒頭に使えるか）

| 順 | 候補 | 長さ | 器（幅×高） | 撮影日 | 撮った人 | 権利 | 焼き込み・透かし | 人 | 冒頭 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **ROV「尾部コーン」**（NTSB ドケット「Pelagic video 1 of 2」＝`04_ROV SNIPS-Rel.mp4`。DVIDS 936977 が同じ中身の見込み＝題と長さ 1:00 が一致） | 60.7秒 | 1920×1080・30p・SAR は札なし・音声あり | **2023-06-22**（NTSB 508） | Pelagic Research Services の ROV「Odysseus」 | **第三者**（USCG・NTSB が公開。説明は "U.S. Coast Guard video courtesy of Pelagic Research Services"） | 左上「OceanGate／Dive: 01／Depth (m): 3775.x」・下に日付・HDG・Alt・左端に ROV の腕（旧版の実測） | なし（海底） | **○** 事故そのものの実写。10秒目から尾部が見える（NTSB 508）。引用＝額装なら深度の数字が出る |
| 2 | **ROV「前部ドーム→後部ドーム」**（「Pelagic video 2 of 2」＝`07_ROV SNIPS-Rel.mp4`。DVIDS 937093 が同じ中身の見込み＝長さ・コマ数 3,219 が一致） | 107.3秒 | 1920×1080・30p・SAR 1:1 | **2023-06-22** | 同上 | **第三者** | 同上（深度 3,774.4m） | なし | **○** 前部ドーム（凹面を上）→左へ振って後部ドーム（リング付き・炭素繊維の破片で満ちる）（NTSB 508） |
| 3 | **USCG 記者会見「残骸の発見」**（DVIDS 888022） | 17:58 | HLS 1920×1080 | 2023-06-22 | USCG 2等兵曹 Ronald Hodges | **A** | 未確認（演台の会見） | Mauger 少将ほか＝公的な任務 | **○** 発見を発表する実写。発言は事実の強さで使える |
| 4 | **USCG 第1管区 指令センターの B-roll**（DVIDS 887734「Watchstanders work to coordinate search efforts…」） | 1:37 | HLS **2720×1530**（器が大きすぎる＝引き伸ばしの疑い・要測定） | 2023-06-20 | USCG 3等兵曹 Logan Kaczmarek | **A** | 未確認 | 当直の隊員＝公的な任務 | **○** 捜索の実写（ボストンの指令センター） |
| 5 | **NY 州空軍 第106救難航空団 HC-130J の B-roll**（DVIDS 888012／888011） | 3:35／3:06 | HLS 1920×1080（20000k） | 2023-06-21 | Capt. Cheran Campbell（州空軍） | **A**（州空軍＝連邦の扱い。弱い所） | 未確認 | 隊員＝公的な任務 | **○** 捜索に出る機体（基地での撮影・海上ではない） |
| 6 | **ROV「引き揚げ」**（DVIDS 937600／937609／937622） | 2:07／30:00／2:19 | 1920×1080（937609 の DVIDS は HLS 720×480 だけ・archive の写しは 1920×1080） | **2023-06-26** | Pelagic（"Video courtesy of Pelagic Research Services"） | **第三者** | ROV の焼き込みの見込み | なし（遺体の一部の恐れは目視で確認＝§5） | **△** 事故の後の作業。旧版の目視メモ＝937622 は「全編ほぼ白濁」、937609 は「13分以降は籠が昇るだけ」 |
| 7 | USCG 記者会見 06-19／06-20／06-21／06-25（DVIDS 887597／887718／887852／888248） | 12:49／12:02／17:26／12:54 | 1920／1920／**1280**／**1280**（HLS） | 各日 | USCG 3等兵曹 Briana Carter | **A** | 未確認 | 公的な任務 | ○ 捜索の経過の実写（06-25 は MBI 招集） |
| 8 | **OceanGate の通信班の映像**（MBI 証拠 CG 141・DVIDS 963844） | 2:34 | **1440×1080（4:3）**・SAR 1:1 | 2023-06-18（事故の当日） | **OceanGate**（説明 "Video courtesy of OceanGate, Inc."。⚠️ DVIDS のクレジット欄は「Video by CWO Melissa Leake」＝札が嘘） | **第三者** | 冒頭に "Provided by OceanGate Inc."（旧版の目視メモ） | 🔴 **CEO の妻（遺族）と私人の顔**（説明に実名） | **△** 爆縮のときの船上（通信班）を写した唯一の実写（24秒目の音＝海面に届いた爆縮の音と見られる）。艇そのものは写らない。使うかはカズヤくん（§5） |
| 9 | NOAA の音響記録（DVIDS 951839） | 23.7秒 | 1440×1080（4:3） | 2023-06-18 | NOAA の係留式受動音響記録器（約900マイル離れた所） | **A**（NOAA が MBI に提供・公開を承認） | 画の中身は未確認（波形などの見込み） | なし | △ **音は実録**として使える見込み・画は実写でない見込み |
| 10 | MBI 公聴会の生配信（USCG の YouTube・2024-09-16〜27）／公聴会前の記者会見（2024-09-15） | 各 6〜9時間 | 1920×1080 | 2024-09 | USCG | **A** | 画面に映る証拠に第三者の物が混ざる | 証人＝元社員など私人が多い | △ 事故そのものではない |
| 11 | TSB カナダの解説動画（YouTube `FPBax7atIeA`「TSB of Canada's investigation into the Titan submersible implosion…」） | 80秒 | 器 3840×2160 | 2026-06-17 公開 | TSB | **Crown** | 中身未確認（図解の見込み） | 未確認 | △／× 中身が未確認・営利の再配布は許可が要る（§1-5） |
| 12 | カナダ空軍 CP-140 オーロラの捜索の映像（「Canadian Forces/Handout via REUTERS」の静止画が報道に出た） | ― | ― | 2023-06-20 | カナダ軍 | **Crown（国防省）** | ― | ― | △ 国防省の公式の置き場が見つからない＝未確認 |
| 13 | MBI の模型アニメ（DVIDS 936788 ＝ `CG 001_1 TITAN_Animation 20240915_v2.2.mp4`） | 10:56 | 1280×720 | 2024-09-16 | **USCG 補助隊**（Auxiliary＝ボランティア）／艇の3D模型は Sketchfab の dylanheyes「OceanGate Titan Submersible」**CC BY 4.0** を改変 | 要確認 | ― | ― | **×** アニメ（冒頭は実写の決まり） |
| 14 | NTSB ドケットの天気図アニメ（`attachment1_SFCchartanimation-Rel.mp4`） | 21秒 | 1920×1080 | ― | NTSB | A | ― | ― | × アニメ |
| 15 | NOAA の 2004 年タイタニック調査の映像（NOAA Ocean Exploration「R.M.S. Titanic: June 2004」） | 5:53 | **480×320** | 2004-05〜06 | クレジット「RMS Titanic Team Expedition 2004, ROI, IFE, NOAA Ocean Exploration」＝共同 | A の見込みは弱い（IFE などは連邦の外） | 未確認 | ― | × 幅 480（事故の前の絵としても全画面に耐えない） |
| 16 | 公聴会後の聞き取り（DVIDS 947680・ダイブ87 の客2人） | 1:52:22 | 1920×1080 | 2024-12-06 | USCG（MBI） | A | ― | 私人2人（実名） | × 私人・事故そのものではない |
| 17 | 報道局の再アップ（例：6abc Philadelphia の YouTube `zthE22b9JHk`＝尾部コーンの ROV） | 59秒 | 1920×1080 | 2024-09-17 | 報道局が USCG の公開を再アップ | 第三者＋局の権利 | 局の字幕・ロゴの恐れ | ― | × 一次の出どころ（NTSB・DVIDS）から取る |

**上位3つ（冒頭）**＝①② **ROV 2本（第三者・器 1920×1080・2023-06-22）**／③ **USCG「残骸の発見」の記者会見（A・器 1920×1080）**。A だけで組むなら ③＋④指令センター（A・器 2720×1530）＋⑤HC-130J（A・器 1920×1080）。

### §1-2 旧版の `DOD_*.mp4` 6本と ROV 映像 04・07 の正体（特定ずみ）

archive.org の `uscg-titan-submersible-hearings`（USCG の公開資料を**個人の利用者が写した**アーカイブ）に同梱の `DVIDS_VIDIEOS.txt` で DVIDS の ID を引き、DVIDS の頁・NTSB のドケットで確かめた。

| ファイル（archive の写し） | 何か | 撮影日 | 撮った人（説明の文） | 器（ffprobe） |
|---|---|---|---|---|
| `Testimony Media/04_ROV Titan Submersible Tail Cone.mp4` | **NTSB ドケット「6- SURVIVAL FACTORS – PELAGIC VIDEO 1 OF 2」（`04_ROV SNIPS-Rel.mp4`）と同じファイル**（64,361,286 バイトで一致）。DVIDS 936977（2024-09-17 公開・1:00・"tail cone"）が同じ中身の見込み（ファイルの照合はしていない） | 2023-06-22 | **Pelagic Research Services, Odysseus ROV**（NTSB 508 の説明） | 1920×1080・30p・60.69秒・1,819コマ・音声 aac 2ch |
| `Testimony Media/07_ROV … Aft Dome Aft Ring Hull Remnants.mp4` | **「PELAGIC VIDEO 2 OF 2」（`07_ROV SNIPS-Rel.mp4`）と同じファイル**（89,833,780 バイトで一致） | 2023-06-22 | 同上 | 1920×1080・30p・107.35秒・3,219コマ |
| `DOD_109728593.mp4` | DVIDS **888248**「U.S. Coast Guard convenes a Marine Board of Investigation…」＝ボストンの記者会見（Mauger 少将・Neubauer 大佐） | 2023-06-25（⚠️ 説明文は "June 25, 2025" と誤記） | USCG 3等兵曹 Briana Carter | 1280×720・59.94p・774.6秒 |
| `DOD_110564587.mp4` | DVIDS **936788**「Model animation for the MBI Titan submersible hearing」＝`CG 001_1 TITAN_Animation…mp4` と同じ（656.67秒・19,700コマで一致） | 2024-09-16 | USCG 補助隊のアニメ（3D 模型は CC BY 4.0 の改変） | 1280×720・30p |
| `DOD_110571004.mp4` | DVIDS **937093**＝ROV「後部ドーム・後部リング・船体の残り・炭素繊維の破片」。🔴 **中身は 07 と同じ見込み**（長さ 107.3秒・**コマ数 3,219 が一致**。旧版は `rov_debris` と `rov_aftdome` を別物として当てていた） | DVIDS の撮影日欄は 2024-09-18（＝公開日）。実際は 2023-06-22 | "U.S. Coast Guard video courtesy of Pelagic Research Services" | 1920×1080・30p |
| `DOD_110579329.mp4` | DVIDS **937600**＝引き揚げの ROV 映像（Commons のコマの題「Forward dome salvage operation」） | 2023-06-26 | "Video courtesy of Pelagic Research Services" | 1920×1080・30p・127.2秒 |
| `DOD_110579532-1920x1080-9000k.mp4` | DVIDS **937609**＝同（30分） | 2023-06-26 | 同上 | 1920×1080・30p・1800秒（DVIDS の HLS は 720×480 だけ） |
| `DOD_110579650.mp4` | DVIDS **937622**＝同（Commons のコマの題「Forward endcap (dome) recovery operation」） | 2023-06-26 | 同上 | 1920×1080・29.97p・139.9秒 |
| （2025 追加）`DOD_111016570.mp4` | DVIDS **963844**＝MBI 証拠 CG 141（通信班の映像） | 2023-06-18 | **OceanGate**（DVIDS のクレジット欄は CWO Melissa Leake＝掲載した人） | 1440×1080・4:3 |
| （2025 追加）`DOD_110804017.mp4` | DVIDS **951839**＝NOAA の音響記録（爆縮と見られる音） | 2023-06-18 | NOAA | 1440×1080・4:3・23.7秒 |
| （2025 追加）`DOD_110745570.mp4` | DVIDS **947680**＝ダイブ87 の客2人の聞き取り | 2024-12-06 | USCG（MBI） | 1920×1080 |

- 🔴 **USCG 自身の Titan 頁（Wayback 2026-05-12）も 04・07 の下に "Videos courtesy of Pelagic Research Services"**＝USCG の頁・NTSB の 508・MBI 図41・NTSB 図11/12 の4か所が Pelagic と書く
- 🔴 **DVIDS の頁は全部「PUBLIC DOMAIN」と出る**（クレジットが "courtesy of Pelagic" "courtesy of OceanGate" の物にも）＝**札は嘘をつく**。根拠は説明の末尾の括弧で決める
- 器の札は SAR 1:1 か札なし・field は progressive か札なし（ffprobe の頭だけ。04 と模型アニメは SAR・field の札が無い）。**実効の幅（引き伸ばし・黒帯）は未測定**。ROV 2本は旧版が原寸 1920×1080 のコマで焼き込みの位置を実測している（黒帯の記録なし）＝1920 近い見込み
- ROV の焼き込み（旧版 `tools_footage.py` の実測・1920×1080 原寸）：左上 "OceanGate"(y≈40)・"Dive: 01"(y≈75)・"Depth (m): 3775.5"(y≈110)＝右端 x≈310 まで／下 日付(y≈1000)・"HDG" "Alt"(y≈1035)／左端 ROV の腕（x≈120 まで）

### §1-3 冒頭に使えない・存在しない物（事実）

- **爆縮の瞬間の映像は無い**：MBI 報告「There were no witnesses to the implosion or video evidence recovered of the implosion」（PDF p.269・印字 p.261。`uscg_mbi_pages.txt` 8638行）
- **タイタンの外部カメラ（SubC Rayfin）**：NTSB が SD カードの暗号を解いて静止画12・動画9を取り出したが、**時刻のある最後の記録は 2023-05-16**（ホリールードの岸壁・訓練）＝事故の潜航の記録は無い（NTSB ドケット「7 - UNDERWATER CAMERA - SPECIALIST'S FACTUAL REPORT」）
- **事故の潜航の前の5人の映像**：MBI「OceanGate videos showed mission specialists for Dive 88 signing the liability waiver on the POLAR PRINCE」＝OceanGate の映像は存在するが**公開は未確認**（第三者）
- MBI 1.9：多くの映像証拠は外国籍の持ち主にあり MBI は提出を強制できなかった

### §1-4 米海軍・NOAA・NTSB の動く映像

- **米海軍**：FADOSS（深海引き揚げ装置）はセントジョンズまで運ばれたが**使われなかった**（2023-06-25 海軍発表・報道）。DVIDS の検索頁は人の確認（CAPTCHA）が出るので**引けなかった**＝海軍の動画は未確認。報道に出た FADOSS の写真は「U.S. Navy Office of Information」提供（日付なし）
- **NTSB**：YouTube／Flickr の B-roll は**見つからない**（NTSB の Flickr `68618467@N03` の中で「Titan」「DCA23FM036」「OceanGate」＝0件）。ドケットの動画は ROV 2本（Pelagic）と天気図アニメだけ
- **NOAA**：2004 年タイタニックの映像は 480×320（上の15）。2003 年調査の写真は Commons に2点（作者 Lori Johnston＝§4）

### §1-5 カナダ政府の物の条件（原文で確認）

| 置き場 | 原文（抜き書き） | 収益化した動画で使えるか（事実だけ） |
|---|---|---|
| canada.ca の利用条件（Terms and conditions） | "Unless otherwise specified you may reproduce the materials in whole or in part for non-commercial purposes" ／ "you may not reproduce materials on this site, in whole or in part, for the purposes of commercial redistribution without prior written permission from the copyright administrator" | 非営利は許可なしで可。**営利の再配布は書面の許可が要る**。OGL の記載は無い |
| 国防省・カナダ軍（Crown copyright protected works managed by National Defence） | 非営利は "You do not need permission…" ／ 営利は "You always need permission when the reproduction will be used commercially and the anticipated gross annual revenue generated from the use of the copyright protected work(s) exceeds $10,000" ／ ライセンスが要る2条件＝「revising, adapting, modifying or translating」か「$10,000 を超える営利」／"photographs and videos at Combat Camera" を例に挙げる | 年 $10,000 以下の営利なら許可なしの読みもできるが、**切る・色・字を重ねる＝modifying はライセンスが要る** |
| Open Government Licence – Canada 2.0 | "including for commercial purposes"・"Copy, modify, publish…"／除外＝Personal Information・third party rights・official symbols | **OGL と明示された情報にだけ**当たる。TSB・国防省の写真・映像に OGL の表示は**見つけていない** |
| TSB（運輸安全委員会）の利用条件（tsb.gc.ca は 403＝**Wayback 2026-08-14 の写し**で原文を読んだ・`materials_raw/tsb/wb_terms.txt`） | "Unless otherwise specified, you may reproduce the materials in whole or in part for non-commercial purposes, and in any format, without charge or further permission, provided you do the following…"（正確さ・題と作者・元の URL を示す）／"you may not reproduce materials on this site, in whole or in part, for the purposes of commercial redistribution without prior written permission from the Government of Canada's copyright administrator, Public Works and Government Services Canada (PWGSC)"／"Some of the content on this site may be subject to the copyright of another party" | 非営利は条件つきで可。**営利の再配布は PWGSC の書面の許可が要る**（収益化した動画がこれに当たるかの読みはカズヤくんの判断）。OGL の記載は無い |

### §1-6 TSB カナダ（M23A0169・最終報告 2026-06-17 公表）

- YouTube：TSB のチャンネル（`UC_EZaZtZR0h0Uw4GDndgEZw`）の 2026-06-17 の動画は**1本だけ**＝`FPBax7atIeA`「TSB of Canada's investigation into the Titan submersible implosion and safety recommendations」（80秒・器は最大 3840×2160・CC 表示なし・説明「This video provides an overview of the … investigation」）。**記者会見の映像はチャンネルに無い**（RSS の最新15本に無し）
- Flickr（`tsbcanada`＝`76842644@N02`）：**M23A0169 の写真は見つからない**（アルバム一覧3頁・最新20枚の公開フィード・Flickr 内検索「M23A0169」「Polar Prince」＝0件・「Titan」＝別件 M16P0162 の3件）＝未確認
- 報告の HTML（Wayback の 2026-06-18 の写し）の図の出どころ → §3-3・§4

---

## §2 そのほかの映像（冒頭以外・本編で使えるか）

| 素材 | 置き場 | 器・長さ | 権利 | 本編での当て先の見込み | 判定 |
|---|---|---|---|---|---|
| ROV 2本（06-22・§1 の1・2） | NTSB ドケット（一次）／DVIDS 936977・937093／archive の写し／Commons の webm 2本（札は PD・説明は courtesy of Pelagic） | 1920×1080 | 第三者（Pelagic） | 発見（6月22日）・残骸と破片・座屈の跡 | ○（引用＝額装・焼き込みは残る） |
| ROV 引き揚げ（06-26・3本） | DVIDS 937600／937609／937622（Commons にコマの PNG 2点＝「Forward dome salvage operation」「Forward endcap (dome) recovery operation」） | 1920×1080 | 第三者（Pelagic） | 回収・証拠の確保 | △（旧版の目視＝937622 白濁・937609 後半は籠） |
| USCG 記者会見 5本（06-19〜06-25） | DVIDS（§1 の7） | 1280〜1920 | A | 捜索の経過・発見の発表・MBI 招集 | ○（公的な任務の顔は使える） |
| USCG 指令センター B-roll（06-20） | DVIDS 887734／Commons の webm（2720×1530） | 器 2720×1530・1:37 | A | 捜索の調整 | ○（器の大きさは要測定） |
| 第106救難航空団 HC-130J B-roll（06-21） | DVIDS 888012・888011 | 1920×1080 | A（州空軍） | 捜索の航空機 | ○ |
| OceanGate 通信班（06-18・CG 141） | DVIDS 963844 | 1440×1080・4:3 | 第三者（OceanGate） | 通信が途絶えた瞬間・音 | △（遺族と私人の顔＝§5） |
| NOAA の音響記録（06-18） | DVIDS 951839／Commons の webm（「NOAA-NPS Noise Reference Recording」） | 23.7秒 | A | 爆縮と見られる音（約900マイル先の記録器） | ○（音）／画は未確認 |
| MBI 公聴会の生配信（2024-09-16〜27・9日） | **USCG の YouTube 再生リスト `PLgOje37c-b1NswzbM8kMEGRrdup_xwlW9`**（USCG の Titan 頁に掲載・動画の作者欄「U.S. Coast Guard」・10本＝公聴会9日＋2024-09-15 の記者会見 `oTQ7wBSlFJs` 12:15）。ID：`avp_-wN3ekA`・`B9tqlpARlqQ`・`V8mmRNTBRiM`・`hOaatO7CBOw`・`Xw0rnBv-Pa8`・`jjadrR8TLmo`・`YupblW5tgiM`・`2OQ7q84t1OU`・`AvAw9YFW2i0`／archive の写し（字幕は Whisper で利用者が作成＝公式でない）／Commons の webm 8本 | 1920×1080・各 6〜9時間 | A | 「公聴会で証言した」場面 | △（証人の多くは私人＝§5） |
| 公聴会前の記者会見（2024-09-15・Neubauer 委員長） | Commons の webm（USCG の YouTube から） | 1920×1080 | A | MBI の説明 | ○ |
| ダイブ87 の客2人の聞き取り（2024-12-06） | DVIDS 947680 | 1920×1080・1:52:22 | A | ― | ×（私人） |
| MBI 模型アニメ | DVIDS 936788 | 1280×720・10:56 | USCG 補助隊＋CC BY 4.0 の模型 | ― | ×（アニメ・本編でも図は自作で） |
| NTSB 天気図アニメ | NTSB ドケット | 1920×1080・21秒 | A | ― | × |
| OceanGate「Cyclops Submersible Development Program」（2015） | Commons の webm／ogg（OceanGate の YouTube。札 CC BY 3.0） | 1280×720 | CC BY 3.0（YouTube 側の表示は未確認＝Commons に「YouTube review needed」の印が1点） | Cyclops 1（別の艇）・CEO の顔 | △（別の艇・人の顔＝§5） |
| TSB の解説動画（2026-06-17） | YouTube `FPBax7atIeA` | 器 3840×2160・80秒 | Crown | TSB の結論 | △（中身が未確認・営利の再配布は許可が要る） |
| NOAA 2004 年タイタニック | NOAA Ocean Exploration | 480×320・5:53 | 共同（ROI・IFE・NOAA） | 事故の前のタイタニック | × |

---

## §3 旧版の写真の判定し直し（26点）

旧版の台帳 `ref_CREDITS.md`「## タイタン号」以下と「2026-08-02 PD 限定をやめて戻した図」の全点。図の凡例は NTSB MIR-25-36 の文字の層で全部引き直した（`materials_raw/ntsb_captions.tsv`）。

### §3-1 判定表

| # | ファイル | 出どころ（凡例・説明の原文） | 撮った人 | 根拠 | 判定 | 旧版の扱いとの差 |
|---|---|---|---|---|---|---|
| 1 | `titan_hull_edge.jpg` | NTSB 図14（下）"mid-span fractured face"・出どころの注なし | NTSB（研究室） | A | ◎ | 同じ |
| 2 | `titan_hull_inner.jpg` | 図13（下）"inner surface"・注なし | NTSB | A | ◎ | 同じ |
| 3 | `titan_delam_ruler.jpg` | 図18（左）・注なし | NTSB | A | ◎ | 同じ（英字の焼き込みは可読性の問題） |
| 4 | `titan_titanic_bow.jpg`（1480×1036） | Commons「Titanic wreck bow.jpg」"Courtesy of NOAA/Institute for Exploration/University of Rhode Island"（2004） | 共同（IFE・URI は連邦の外） | A の見込み（弱い） | ○ | 旧版は「米連邦の著作物＝PD」と断定＝**共同の弱い所を書いていない** |
| 5 | `titan_rov_tailcone.jpg`（1909×1080） | Commons「Titan submersible on the ocean floor.jpg」＝説明 "Image taken by Pelagic Research Services 6000, a remotely operated vehicle"・**出どころは 6abc Philadelphia（テレビ局）の YouTube `zthE22b9JHk`**（2024-09-17 の再アップ）／MBI 図41 "Source: Pelagic Research Services, June 2023" | Pelagic | 第三者（札は「PD US Coast Guard」＝嘘） | **×（このファイル）** | 🔴 旧版は画面に「アメリカ沿岸警備隊／ROV撮影／**パブリックドメイン**」。幅 1909 は局の版の切り出しの見込み＝**一次（NTSB ドケットの 04）から取り直せば △** |
| 6 | `titan_rov_aft.jpg`（1920×1080） | 同じ中身の Commons＝「Wreckage of Titan submersible aft section.png」（DVIDS 937093 のコマ・札 PD-Mark）／DVIDS "courtesy of Pelagic" | Pelagic | 第三者 | △ | 🔴 画面に「**パブリックドメイン**」と出していた（旧版 `footage.py` の注は「PD と書いてはいけない」と書いていたのに静止画の出典の行は PD のまま） |
| 7 | `titan_cf_evidence.jpg`（1500×1000） | DVIDS 9057369「Titan submersible carbon fiber debris」"(U.S. Coast Guard photo)"・クレジット CWO Melissa Leake | USCG 職員 | A | ◎ | 同じ |
| 8 | `titan_hull_pair.jpg`（1609×1490） | 図13（上下）・注なし（PDF の埋め込み 1609×1490 と一致） | NTSB | A | ◎ | 同じ |
| 9 | `titan_ntsb14_endface.jpg` | 図14（上）・注なし | NTSB | A | ◎ | 同じ |
| 10 | `titan_ntsb15_endpiece.jpg` | 図15・注なし | NTSB | A | ◎ | 同じ |
| 11 | `titan_ntsb16_wrinkle.jpg` | 図16（上）・注なし | NTSB | A | ◎ | 同じ |
| 12 | `titan_ntsb16_grind.jpg` | 図16（下）・注なし | NTSB | A | ◎ | 同じ |
| 13 | `titan_ntsb17_layers.jpg` | 図17（上）・注なし | NTSB | A | ◎ | 同じ |
| 14 | `titan_ntsb17_voids.jpg` | 図17（下）・注なし | NTSB | A | ◎ | 同じ |
| 15 | `titan_f18_delam.png` | 図18・注なし | NTSB | A | ◎ | 同じ |
| 16 | `titan_f01_descend.jpg` | 図1 "Submersible Titan descending **on unknown date**. (Source: OceanGate)" | OceanGate | 第三者 | △ | 旧版は c110「台から切り離された」の地＝**撮影日不明**の絵を当日の場面に敷いていた（副題に注意） |
| 17 | `titan_f04_lars.png` | 図4 "From top: Top-down view of Titan on LARS (scale approximate), and Titan secured on LARS in 2022. (Source **[bottom]**: Garry Comber)" | 上＝NTSB の線画／下＝Garry Comber | 上なら A | ◎（上の線画なら・要確認） | 🔴 旧版の台帳は「G. Comber」＝**Comber は下の写真だけ**。旧版の目視メモ（線画・"Forward dome and viewing port" の字）からは上の線画の見込み。実写には数えない |
| 18 | `titan_f08_launch.png` | 図8 "(Source: Garry Comber)"・2022 年・Arctic Horizon | 個人 | 第三者 | △ | 同じ（地に敷いた＝改変） |
| 19 | `titan_f09_parking.png` | 図9 "(Source: A. Harvey)" ＝ MBI 図218 "Overhead photo of the **A Harvey Marine Base** … Source: A Harvey" | **会社の見込み**（MBI 図218 は「A Harvey Marine Base」の写真で出どころ「A Harvey」・USCG の証拠一覧に「CG_116_A_HARVEY_EMAILS_AND_DOCS」） | 第三者 | △ | 🔴 旧版は「A. Harvey（**個人**）」＝会社の見込み |
| 20 | `titan_f10_mishap.png` | 図10 "(Source: Steven Taragel)"（2023-05-20・05-27 の LARS の傾き） | 個人 | 第三者 | △ | 同じ |
| 21 | `titan_f11_wreck.png` | 図11 "(Background source: Pelagic Research Services)"＋NTSB の注記 | Pelagic | 第三者 | △ | 同じ |
| 22 | `titan_f12_wreck.png` | 図12 "(Background source: Pelagic Research Services)" | Pelagic | 第三者 | △ | 同じ |
| 23 | `titan_f02_cylinder.png` | 図2 "(Background source: OceanGate)" | OceanGate | 第三者 | △ | 同じ（線画） |
| 24 | `titan_f07_cobond.png` | 図7・注なし（差し込みは実物の断面写真） | NTSB | A | ◎ | 同じ |
| 25 | `titan_f22_production.png` | 図22 "(**Data source**: Marine Technology Society)" | NTSB が MTS の数で作図 | A（数は事実） | ◎ | 旧版は「記載なし」＝**注はある**（結論は同じ） |
| 26 | `titan_f23_population.png` | 図23 "(**Background source**: Marine Technology Society)" | MTS | 第三者 | △ | 同じ |

**数**：◎15（#17 は要確認）／○1／△9／×1。

### §3-2 旧版のやり方で今の決まりに合わない所（事実）

1. **第三者の写真を「地」に敷いていた**（c109＝図8 Comber・c602＝図9 Harvey・c607＝図10 Taragel・c110＝図1 OceanGate・ROV 静止画を c115a ほか）。地は暗幕 0.84＋図の重ね＝**色を変え・切り・上に重ねる＝改変**。今の決まり（第三者は額装・改変しない）では、このやり方は使えない
2. **ROV の静止画の出典の行が「パブリックドメイン」**（`scene_jiko.CR_*`）。動画の出典の行（「ROV撮影：Pelagic Research Services」）は正しかった
3. ROV 動画は**切り出しと拡大（zoom 1.42）で焼き込みを隠していた**。第三者の映像を額装で使うなら、焼き込み（「OceanGate」「Depth (m): 3775.x」）は画面に残る
4. `rov_debris`（DVIDS 937093）と `rov_aftdome`（07）を**別の素材として扱っていた**が、長さとコマ数が一致＝**同じ素材の見込み**（絵の照合は映像方針で）
5. ROV の深度の焼き込み（3,774〜3,775m＝海底）と台本の「水深3,346メートルで消えた」（爆縮の深さ）は**別の数字**。旧版は焼き込みを切って見せなかった

### §3-3 TSB カナダ 最終報告（M23A0169）の図（旧版は未使用・参考）

出どころは報告の HTML（Wayback の 2026-06-18 の写し・`materials_raw/tsb/wb_report_20260618.txt`）。**TSB 撮影の物も Crown＝営利の再配布は PWGSC の書面の許可が要る**（TSB の利用条件・§1-5）。

| 図 | 中身 | 出どころ（原文） | 判定 |
|---|---|---|---|
| 1 | 2023年5月のタイタン | "Source: **Third party, with permission**" | △（第三者・撮影者不明） |
| 2 | 船室を上から | OceanGate | △ |
| 3 | LARS（2023年5月） | OceanGate, with TSB annotations | △ |
| 4 | ポーラープリンス | **TSB** | △（Crown・営利の再配布は許可が要る） |
| 5 | 地図＋差し込み | 本図＝カナダ水路部 海図 4001＋TSB の注記／差し込み＝TSB | △（Crown） |
| 6 | 耐圧殻の分解図 | TSB, based on OceanGate drawings | △（Crown・自作の図で代えられる） |
| 7 | 外骨格の図 | OceanGate, with TSB annotations | △ |
| 8 | 1/3 模型の加圧試験 | OceanGate | △ |
| 9〜13 | 1/3 模型・端のドーム・1号殻の円筒 | **Patrick Loomis**（個人） | △ |
| 14 | のぞき窓の設計 | TSB | △（Crown） |
| 15 | 端材の試料の写真 A〜D | **TSB**（研究所） | △（Crown） |
| 16 | 危険度の評価の画面 | OceanGate | △ |
| 17 | ホライゾン・アークティック | Transport Canada | △（Crown・別の省） |
| 18 | ポーラープリンスが LARS とタイタンを引く | OceanGate | △ |

付録 A＝通信の逐語の記録（Titan と海面の支援チームの文字のやりとり）＝事実の記録（§5）。

---

## §4 新しい写真の候補（数の当たりだけ・取得しない）

🔴 **題名・凡例で中身を仕分けてから数えた**（記者会見・公聴会と、事故そのものの絵を分ける）。⚠️ どれも**まだ目で見ていない**＝「写っているはず」の数。

### §4-1 事故そのものに関わる絵（A が中心）

| 欄 | 点数 | 置き場・ID | 器 | 根拠 | メモ |
|---|---|---|---|---|---|
| 捜索の空撮（HC-130 から・2023-06-21） | **3〜4** | DVIDS 7875444・7875448・7875471（"Coast Guard air crew conducts overflight search…" 1〜3 of 3）／Commons「Coast Guard HC-130 and L'Atalante searching for Titan.jpg」（1600×1200・DVIDS の ID 未特定＝3枚と重なる恐れ） | 4032×3024 ほか | **A**（USCG 1等兵曹 Amber Howie） | 機内の乗員＝公的な任務 |
| 捜索の図（search pattern） | 2 | DVIDS 7871940（1542×942）／Commons「Search pattern … (DVIDS 7873645)」（1920×1080・DVIDS の頁は 404） | ― | A | 図＝実写に数えない |
| 回収・証拠（2023-09-30 の2回目の引き揚げ・10-04 の調査） | **4**（新3＋旧版で使用1） | DVIDS **9057342**（Gary Chouest の甲板で残骸を調べる隊員・3024×4032・説明は "photo by Lt. Cmdr. Katie Williams"／クレジット欄は CWO Leake）／**9057368**（「タイタニック遠征のステッカーと名刺の一部」・6192×4128）⚠️§5／9057369（＝旧版 `titan_cf_evidence`）／Commons「U.S. Coast Guard marine safety engineers conduct a survey of the aft titanium endcap…」（2023-10-04・2048×1536・CWO Leake） | 2048〜6192 | **A** | USCG の報道頁の igphoto 2003747271〜73（同じ 09-30）は 403＝重なり未確認 |
| 1号殻の保管（エバレット） | 1 | DVIDS **9057367**（4032×3024） | ― | **A** | ⚠️ DVIDS の撮影日欄「05.29.2019」は**亀裂を見つけた日**。MBI 図132「Photo of the first TITAN hull taken by the MBI on August 2, 2023」と同じ絵の見込み＝撮影日は要確認 |
| MBI が撮った写真（MBI 報告の凡例「taken by the MBI」） | **16**（場面9・航海日誌の写真4・CYCLOPS I 3）＋日誌1（図18） | 報告 PDF に埋め込み（図3 ポーラープリンスの入港 06-25／図5・109・112・115 LARS／図21 格納庫／図24 RHIB の MAX と STEWIE／図31 通信班のいた船橋の事務室／図132 1号殻） | 埋め込みは幅 **約780〜1590**（多くは約1200） | **A**（MBI＝USCG） | 全画面には小さい＝額装向き |
| FBI 証拠対応チームの残骸写真 | **3** | MBI 図157（後部セグメント・2023-07-05）・図159（前部セグメント）・図270（前部ドーム＝のぞき窓の留めボルト16本が切れている） | 埋め込み 556〜1333 | **A**（FBI） | 回収後の残骸 |
| USCG の残骸写真 | 1 | MBI 図268「Aft segment with remaining adhesive. Source: USCG.」 | 675×841 | A | |
| NTSB 研究室の写真（MIR 図13〜18 のもと） | **多数**（埋め込み画像の数） | NTSB ドケット：**Materials Laboratory Factual Report 24-011**（79頁・埋め込み77・長辺1280以上72）／**24-012**（55頁・埋め込み38・1280以上24・図1〜24＝残骸と破片の写真・図25〜39＝グラフ・図40＝Steven Taragel＝第三者）／**CG-107 NTSB の MBI 向け発表**（67頁・埋め込み218・1280以上161・一部に "Source: OceanGate Titan Archive GitHub Repository"・"Source: Senevirtane et al"（論文）＝第三者） | 多くは 1280 以上 | **A**（凡例に他の出どころが無い物） | ⚠️ 24-012 図1〜4「as discovered」、24-011 図1e「as found on the ocean floor」＝**海底の絵は凡例に注が無くても Pelagic の見込み**（MIR 図11 は同じ種類で Pelagic と書く） |
| デブリの分布図（Pelagic 作成・3頁） | 3 | NTSB ドケット CG-103／Commons「Titan Debris Field Chart Page 1〜3 of 3」（4961×3508・札は PD-Mark） | ― | **第三者**（作者欄 Pelagic Research Services LLC） | 図＝自作で起こせる |
| TSB 最終報告の TSB 撮影 | 3 | 図4 ポーラープリンス・図15 端材の試料 A〜D・図5 の差し込み | 未確認 | **Crown**（営利の再配布は許可が要る） | §3-3 |
| TSB の Flickr | **0** | `tsbcanada`（§1-6） | ― | ― | 3つの経路で見つからない＝未確認 |
| NTSB の Flickr | **0** | `68618467@N03` で「Titan」「DCA23FM036」「OceanGate」＝0件 | ― | ― | |

### §4-2 記者会見・公聴会・式典（事故そのものではない）

| 欄 | 点数 | 置き場 | 根拠 | 人 |
|---|---|---|---|---|
| 公聴会の写真（2024-09・USCG 撮影） | **72**（Commons「Witnesses testify at U S Coast Guard Marine Board of Investigation…」）＋DVIDS 特集頁の4（重なりの見込み） | Commons／DVIDS `feature/titanMBI` | A | 証人＝元社員など**私人が実名**で写る・USCG の職員 |
| 公聴会の動画 | 9日分（Commons の webm 8） | USCG の YouTube／archive／Commons | A | 同上 |
| 記者会見の動画（2023-06-19〜25・2024-09-15） | 6 | DVIDS／Commons | A | 公的な任務 |

### §4-3 船・タイタニック（事故の前後の絵）

| 欄 | 点数 | 根拠 | メモ |
|---|---|---|---|
| **ポーラープリンス（支援船＝1959年建造・IMO 5329566・元 CCGS Sir Humphrey Gilbert）** | **7**（Commons「Polar Prince (ship, 1959)」5＋「CCGS Sir Humphrey Gilbert (ship, 1959)」1＋**別の分類に入っていた**「2024-06-10 POLAR PRINCE - IMO 5329566 - Halifax」1） | CC BY 2.0×1・CC BY 4.0×1・CC BY-SA 3.0×4・CC BY-SA 4.0×1 | 撮影は 2010・2015・2018・2024 など＝**事故の年の写真は無い**。「CanadaC3.jpg」の日付 2015 は要確認 |
| 🔴 **同じ名前の別の船「Polar Prince」（1999年・IMO 9181481・ノルウェー）** | **25**（Commons「Polar Prince (ship, 1999)」＝リバプールの写真など） | CC BY／BY-SA | **×（別の船）**。1959年の船の1点がこの分類に混ざっている |
| ホライゾン・アークティック（IMO 9732838） | 3 | CC BY-SA 4.0（2019・2022-08-21） | 2021・22年の遠征の支援船／2023 年の ROV の母船 |
| タイタニックの残骸（事故の前） | Commons「Titanic wreck」8 のうち写真4（NOAA の船首＝旧版で使用・Lori Johnston 2003×2〈札は PD US NOAA・作者は調査の参加者＝弱い〉・CC0 の救命胴衣） | ― | NOAA 2004 の映像は 480×320 |

### §4-4 使わない見込みの物（数だけ）

- 有志の CG・模型（Commons・CC BY-SA 4.0）6点＝推定の絵（実写でない）
- 地図 6点（CC）＝自作で起こす
- 報道局の再アップ・報道写真（6abc・Reuters・Canadian Press など）＝一次の出どころがある物は一次から

---

## §5 人・音・遺体の扱いの事実（使う／使わないは書かない＝カズヤくんが決める）

### §5-1 亡くなった5人（MBI 報告 表2・PDF p.12・印字 p.4）

| 立場（報告の表記） | 年齢・国籍 |
|---|---|
| "Chief" Pilot / CEO / OceanGate の取締役会書記 | 61・米国 |
| Content Expert（タイタニックの専門家） | 77・フランス |
| Passenger / Mission Specialist #1 | 48・英国とパキスタン |
| Passenger / Mission Specialist #2 | 19・英国とパキスタン |
| Passenger / Mission Specialist #3 | 58・英国 |

⚠️ このリポは公開＝私人の名前は書かない。5人の名前は Vault `Projects/事故検証-22本目-旧版の棚卸し-ノート-20261013.md` §2（2026-10-13 に親が移した）

**5人の顔が写る（写る恐れのある）素材**：

| 素材 | 誰 | 権利 | 確かさ |
|---|---|---|---|
| MBI 図251「Inside of TITAN during Dive 87 incident … **Mr. Rush is sitting against the back wall** …」 | CEO（ダイブ87＝事故の前の潜航） | 第三者（Former OceanGate mission specialist） | 凡例に明記 |
| MBI 図26「Small boat STEWIE transporting **mission specialists to the LARS for Dive 88**」 | ダイブ88（事故の潜航）の乗員 | 第三者（OceanGate） | **写っている見込み**（目視していない） |
| MBI 図27「TITAN atop LARS moments before commencement of Dive 88」 | 不明 | 第三者（OceanGate） | 要目視 |
| OceanGate の映像（MBI 4.6.8.4.1「OceanGate videos showed mission specialists for Dive 88 signing the liability waiver」） | ダイブ88 の乗員 | 第三者 | 公開は未確認 |
| Commons「Stockton Rush.png」「Stockton Rush (cropped).png」「… (cropped 2).png」 | CEO（2015） | CC BY 3.0（OceanGate の YouTube） | 札どおりなら使える種類 |
| Commons「Richard S. Rush 1984.jpg」（533×685） | CEO（プリンストン大の卒業アルバム） | PD（**PD US no notice**＝1989年より前に著作権表示なしで発行。A〜D のどれでもない別の根拠） | |
| Commons の5人の分類 | タイタニックの専門家＝署名の画像だけ／客3人＝**分類が無いか空（0点）** | ― | |

**遺族・私人**：
- DVIDS 963844（CG 141）＝説明に**CEO の妻（遺族）と私人1人の実名**（「… monitor data and text communications」）＝事故の瞬間の通信班の映像に**遺族と私人の顔と実名**（第三者 OceanGate）。名前は Vault のノート §3
- 公聴会の写真72点・動画9日分＝元社員などの証人（私人・実名）と USCG の職員
- DVIDS 947680＝ダイブ87 の客2人（私人・実名＝名前は Vault のノート §3）
- 決まり（記憶 `feedback-jiko-photo-people-policy`）の当てはめ：公的な任務の人の顔＝使ってよい／私人の顔＝使わない（CC BY・PD は顔だけモザイク可・**第三者の物はモザイク＝改変**）

### §5-2 遺体・遺品

- 報告書の文字の層：**MBI・NTSB とも「presumed human remains」の語は0件**（「remains」は MBI 2件とも別の意味・NTSB 0件）。MBI の前書き（PDF p.10・印字 p.2）は技術支援の機関に **Armed Forces Medical Examiners System（AFMES）・Department of Defense DNA Identification Laboratory・Rhode Island Medical Examiner** を挙げる
- USCG の発表（2023-06-28＝最初の引き揚げ後、2023-10-10＝2回目）は報道の引用で「presumed human remains」を回収して医療の専門家に分析させると書く（**原文の頁は news.uscg.mil の 403 で未確認**）
- **ROV の引き揚げ映像（06-26・DVIDS 937600／937609／937622）**：説明に遺体の記述は無い。ただし遺体は「残骸の中から」回収されたと発表されている＝**写る恐れは否定できない（全数の目視が要る）**
- **DVIDS 9057368**「A Titanic expedition sticker and part of a **business card** recovered from the Titan submersible debris field」＝遺品の可能性・名刺の名前が読める恐れ（要目視）
- YouTube の広告の規約で効くのは「明らかな負傷や損傷のある遺体」だけ（記憶 `feedback-jiko-photo-people-policy`）

### §5-3 音の記録

| 音 | 何が残っているか | 公開 | 権利 |
|---|---|---|---|
| **ダイブ80 の「大きな音」（2022-07-15）** | 船内の客と海面の小舟の乗員が聞いた（NTSB PDF p.36・p.58／MBI PDF p.233）。RTM が**音響の急増とひずみの跳び**を記録（＝センサーの数値・グラフ） | **音声の録音は報告書に出てこない**（NTSB・MBI とも「audio」で該当なし） | グラフの元は OceanGate（MIR 図19・20 は Background source: OceanGate） |
| **爆縮の音（海面）** | OceanGate の通信班の映像（CG 141）の**24秒目の音**＝"believed to be the sound of the Titan's implosion reaching the surface"（DVIDS 963844）。船長は「船が震えたのを感じた」（MBI 4.1.53） | 公開（2025-05-22 DVIDS 掲載） | **第三者**（OceanGate） |
| **爆縮と見られる音（遠方）** | **NOAA の係留式受動音響記録器**（約900マイル先）の記録 23.7秒（DVIDS 951839・Commons では「NOAA-NPS Noise Reference Recording」） | 公開（2025-02-07）・"NOAA, which approved its use in the investigation and public release" | **A**（NOAA） |
| **最後の文字のやりとり** | 文字の記録（音声ではない）＝NTSB ドケット「EXTRACT OF EVOLOGICS CHAT」（8頁）／TSB 報告 付録 A の逐語の記録／MBI の再現アニメ（USCG 補助隊） | 公開 | 記録の文言は事実。再現アニメは補助隊＋CC BY 4.0 の模型 |
| **捜索中の「叩く音」（2023-06-20〜21）** | カナダの P-3（CP-140）のソノブイが拾ったと報道。USCG は後に事故と関係ないと説明（報道） | **MBI・NTSB の文字の層に記述なし**（banging／knocking／tapping＝捜索の文脈で0件）・**公開の録音は見つからない** | ― |
| CEO の声 | Commons「Stockton Rush voice.ogg」「… (Enhanced).wav」（2015 の OceanGate 動画から） | 公開 | CC BY 3.0（札） |

---

## §6 映像方針で確かめること（未確認の一覧・31件）

**実効の幅・中身**
1. ROV 04・07 の**実効の幅**（周波数の崖＋列ごとのばらつき）。器は 1920×1080
2. USCG 記者会見 888022（器 1920）・指令センター 887734（器 **2720×1530**＝引き伸ばしの疑い）・HC-130J 888012（器 1920）の実効の幅
3. 07 と DVIDS 937093（DOD_110571004）が**同じ絵か**（数コマを知覚ハッシュで）
4. ROV の焼き込みの全文と秒（「OceanGate」「Dive: 01」「Depth (m)」「日付」「HDG」「Alt」）＝額装で出す場合の見え方
5. DVIDS 951839（NOAA の音）の**画の中身**（波形か静止画か）
6. DVIDS 963844（CG 141）の頭の「Provided by OceanGate Inc.」の秒・人の顔の秒
7. TSB の YouTube `FPBax7atIeA`（80秒）の中身（図解か実写か・第三者の映像が混ざるか）
8. MBI 報告の埋め込み写真は幅 1300 前後が多い＝全画面にすると拡大（額装向き）
9. NTSB ラボ報告 24-011・24-012・CG-107 の写真のうち**海底の絵（Pelagic の見込み）**と研究室の絵（A）の仕分け

**権利・出どころ**
10. Pelagic の映像の権利：2023-06-22・06-26 の作業は誰の契約か（OceanGate／Horizon Maritime／米海軍 SUPSALV／USCG）。"courtesy" の表記どおり第三者として扱うか
11. ROV の深度の焼き込み（3,774〜3,775m＝海底）と台本の「3,346メートル」（爆縮の深さ）の出し分け
12. USCG の Titan 頁（news.uscg.mil）は 403。Wayback の写し（2026-05-12）で**映像の一覧は確認**（951839・937600・937622・04/07 ROV＝USCG 自身も `Portals/11/…/04_ROV…mp4` を置き "Videos courtesy of Pelagic Research Services" と書く・963844・936788・947680・YouTube 再生リスト）。**頁の「Document Library」（CG115・CG116 ほか）の写真入りの証拠の全数は未確認**（展示物の PDF は media.defense.gov にもある＝例：CG-065 捜索の毎日のスライド）
13. USCG の発表文（2023-06-28・2023-10-10）の原文（遺体の語）
14. USCG の igphoto 2003747271〜73 と DVIDS 9057342 などの重なり
15. DVIDS の検索・タグ頁は人の確認（CAPTCHA）＝**DVIDS の全数（海軍・USCG の他の部隊）は数えていない**
16. DVIDS 9057367 の撮影日（2019-05-29 と書くが MBI 図132 は 2023-08-02 撮影）
17. Commons「Coast Guard HC-130 and L'Atalante…」の DVIDS ID と 7875444〜71 との重なり
18. 州空軍（第106救難航空団）の映像の §105 の扱い（Title 32 の州兵）
19. USCG 補助隊（Auxiliary）の作品の権利（アニメ・MBI 図32・35）
20. NOAA 2004・2003 のタイタニックの絵の共同のクレジット（IFE・URI・ROI・Lori Johnston）
21. OceanGate の 2015 年の YouTube 動画の CC BY 3.0 が今も YouTube 側で表示されるか（Commons に「YouTube review needed」の印）
22. TSB の利用条件は Wayback の写しで読めた（営利の再配布は PWGSC の書面の許可）＝**TSB 撮影の写真（図4・15）と YouTube の動画を収益化した動画で使うか**（許可を取るか・引用で額装か・使わないか）はカズヤくんの判断
23. TSB の Flickr に M23A0169 のアルバムがあるか（3つの経路で0）・TSB の 2026-06-17 記者会見の映像の置き場
24. カナダ国防省の CP-140 の映像の公式の置き場
25. USCG の Titan 頁の「Ch1_04」「Ch3_04」（引き揚げの ROV）と DVIDS 937600・937622 の対応、DVIDS の短いリンク `dvidshub.net/r/hopsmx`・`/r/opdabi` が 936977・937093 を指すか

**旧版の素材**
26. `titan_f04_lars.png` が図4の**上（NTSB の線画）**か下（Comber の写真）か
27. `titan_rov_tailcone.jpg`（Commons・1909×1080）にテレビ局の字・ロゴが残っていないか（一次から取り直すなら不要）

**人・遺体**
28. MBI 図26・27（ダイブ88 の直前）に5人の顔が写っているか
29. ROV 引き揚げ映像3本（06-26）に遺体の一部が写っていないか（全数）
30. DVIDS 9057368 の名刺の名前が読めるか
31. Commons のポーラープリンス（1959年の船）7点に本当にその船が写っているか（「Lunenburg Fishing Boat Yards」3点は題に船名が無い）・「CanadaC3.jpg」の撮影年（2015 と書くが、カナダ C3 の航海は 2017 の見込み）

---

## §7 調べ方の記録

### 使った置き場と結果

| 置き場 | URL・問い合わせ | 結果 |
|---|---|---|
| archive.org のメタデータ | `https://archive.org/metadata/uscg-titan-submersible-hearings` | 200・2,551ファイル（MPEG4 24）。アップロードは**個人の利用者**（作成者欄は United States Coast Guard）。`DVIDS_VIDIEOS.txt` で DOD 番号→DVIDS ID |
| ffprobe（頭だけ） | archive の mp4 12本 | 器・SAR・fps・コマ数・音声の有無（`ffprobe_ia.jsonl`） |
| DVIDS の頁 | `https://www.dvidshub.net/video/<ID>`・`/image/<ID>`・`/video/<ID>.m3u8`（HLS の一覧＝器の幅） | 頁は 200。🔴 **検索・タグ頁は AWS WAF の「Human Verification」**（CAPTCHA）＝使っていない。特集頁 `feature/titanMBI` は 200 |
| NTSB ドケット | `https://data.ntsb.gov/Docket/?NTSBNumber=DCA23FM036`（表を HTML から読んだ） | 69件。ROV 2本＝「6- SURVIVAL FACTORS – PELAGIC VIDEO 1/2・2/2」＋508 の説明 PDF。ラボ報告など5件の PDF を落として文字と埋め込み画像の寸法だけ取った |
| NTSB・MBI 報告の文字の層 | `ref/ep22/src/*_pages.txt` | 凡例を全部拾った（NTSB 24・MBI 273） |
| news.uscg.mil | Titan の頁 | **403**（curl・WebFetch とも）→ Wayback の写し（`web.archive.org/web/20260512123651id_/…/Titan-Submersible/`）で映像の一覧と "Videos courtesy of Pelagic Research Services" を確認 |
| YouTube（USCG） | 再生リスト `PLgOje37c-b1NswzbM8kMEGRrdup_xwlW9`・視聴頁のメタデータ | 10本・作者「U.S. Coast Guard」 |
| Wayback | CDX・`id_` 付きの写し | 断続的に「Temporarily Offline」(503)・429。TSB 報告の HTML（2026-06-18）は取れた |
| tsb.gc.ca・bst.gc.ca | 報告・調査の頁・PDF | **403**（HEAD も）→ Wayback の写しで報告の HTML（2026-06-18）と利用条件（2026-08-14）を読んだ。PDF（`bst.gc.ca/sites/default/files/2026-06/M23A0169-ENG.pdf`）は読んでいない |
| TSB の Flickr | アルバム一覧3頁・公開フィード（`photos_public.gne`）・Flickr 内検索 | M23A0169 は見つからない |
| TSB の YouTube | RSS `feeds/videos.xml?channel_id=UC_EZaZtZR0h0Uw4GDndgEZw`＋視聴頁のメタデータ | 2026-06-17 の動画1本 |
| NTSB の Flickr | Flickr 内検索（`68618467@N03`） | 0件 |
| Commons API | `list=categorymembers`・`prop=imageinfo|categories`（`clshow=hidden`）・2.5秒おき | 429 が2回（1回目は 1.1秒おきで止まった→2.5秒おきに変えて再開・2回目は26秒待って再開）。カテゴリ歩きは3回で合計 約4分（40分の上限の内） |
| canada.ca | 利用条件・国防省の Crown copyright・OGL | WebFetch で原文の抜き書き（canada.ca の curl は止まった） |
| NOAA Ocean Exploration | 動画の頁＋mp4 の ffprobe | 480×320 |

### つまずき
- DVIDS の撮影日欄・クレジット欄は**掲載した人・公開日**のことがある（937093 の撮影日欄＝2024-09-18、963844 のクレジット＝CWO Leake だが映像は OceanGate、9057367 の撮影日欄＝亀裂の発見日）
- Commons の「Polar Prince」は**同じ名前の2隻**（1959年＝支援船／1999年＝ノルウェーの別の船）。1999年の分類に 1959年の写真が1点混ざる
- `python -I` は `PYTHONIOENCODING` を無視する＝スクリプトの中で `sys.stdout.reconfigure(encoding="utf-8")`

### 生のメモ（`ref/ep22/src/materials_raw/`）
- `parse_captions.py`・`ntsb_captions.tsv`・`mbi_captions.tsv`・`mbi_captions_classified.tsv`（凡例の全部と出どころの分類）
- `ia_uscg_hearings_metadata.json`・`ia_DVIDS_VIDIEOS.txt`・`ffprobe_ia.jsonl`
- `dvids_parse.py`・`dvids_pages/`・`dvids_pages_img/`・`dvids_m3u8/`・`dvids_videos_known.json`・`dvids_batch2〜4.json`
- `ntsb_docket_page.html`・`ntsb_docket_pdf/`（508 説明・水中カメラ報告・ラボ報告 24-011／24-012・CG-107・CG-103・運航の事実報告＝**PDF は計 約124MB**＝コミットしない・要らなければ消してよい。`.txt` と `_imgs.tsv` が抜き書き）
- `pdf_figs.py`・`mbi_pdf_imgs.tsv`・`ntsb_pdf_imgs.tsv`（報告 PDF の埋め込み画像の寸法）
- `commons_walk.py`・`commons/*.json`・`commons/titan_cats.tsv`
- `tsb/`（Flickr・YouTube・Wayback の報告 HTML と文字の層）・`canada/`（OGL）・`noaa/`・`yt/`・`ntsb_flickr/`・`uscg_pages/`
