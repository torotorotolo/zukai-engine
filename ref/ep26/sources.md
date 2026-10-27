
# 26本目（タイタニック号沈没事故・1912-04-14〜15・北大西洋・ホワイト・スター・ライン）一次資料の台帳と芯の照合

**2026-10-27（26本目の2本目のチャット＝②③）で作った。** ①の詳細＝[legend_2026-10-26.md](legend_2026-10-26.md)（通説の判定・数の割れ）。このファイルは①を**引き写さず**、取り直した原本で自分で当てた結果（道具＝`probe/head26.py`・`pages26.py`・`ocrdiff26.py`・`crops26.py`・`table26.py`・`sd726grep26.py`／出力＝`src/`＝**git の外**）。
素材＝[materials.md](materials.md)／尺の骨＝[kousei.md](kousei.md)

- 凡例：**G**＝国の機関の公式の置き場のファイル／**T**＝有志の書き起こし（titanicinquiry.org・**保存していない**＝読んだだけ）／**N**＝米国海洋大気庁（NOAA）の頁／**U**＝米国沿岸警備隊（USCG）の頁／**A**＝米国立公文書館（NARA）の目録
- 頁＝**印刷の頁**。英国の報告（G1）は **PDF＝印刷**（8頁目以降の頁の頭の数字で確認）。MAIB 1992（G2）は **PDF＝印刷＋4**（本文 p.1＝PDF 5頁）・Annex 1〜4＝PDF 24〜30頁
- ⚠️ 「0件」は「この綴りでは出ない」であって「無い」ではない
- 🔴 **リポは公開**＝乗客（楽団員を含む）と会社の人（社長・副社長・造船所の技師）は**役職だけ**。名前を出すのは公の任務の人＝タイタニック号・カリフォルニアン号・カルパチア号の船長・航海士・通信士・見張り・操舵手・見習いと、審問の長（英＝難破調査委員の Mersey 卿／米＝上院の小委員長 William Alden Smith）。カリフォルニアン号の機関部の乗組員（ドンキーマン）はここでは役職で書く（名前は MAIB p.5 にある・ルール B2-1 では乗員は実名の側＝画面に名前を出すかは④で決める）

---

## 1. 資料（1件1行）

保存先＝`ref/ep26/src/`（**git の管理外**）。大きさ・md5＝`src/fetch_log.tsv`。
🆕 **① の scratchpad は消えていなかった**（別のセッションのフォルダに残っていた）＝6件を写し、**10-27 にサーバの大きさと全件一致**（`probe/head26.py`・NIST のサーバは HEAD にだけ 404 を返す＝1バイトの GET で測った）＝落とし直していない。

| 記号 | 資料 | URL | 保存先（md5 の頭8字） | 権利・使い方 |
|---|---|---|---|---|
| **G1** | 英国の審問の報告（難破調査委員の正式調査・1912-07-30）の米国上院の公式の刷り直し **S. Doc. 933**（62d Cong. 2d Sess.・88頁） | https://www.govinfo.gov/content/pkg/SERIALSET-06179_00_00-019-0933-0000/pdf/SERIALSET-06179_00_00-019-0933-0000.pdf | `gov/SERIALSET-06179_00_00-019-0933-0000.pdf`（1600f6a6）・頁ごとの文字＝`sd933_pages/` | 米国の公文書＝PD。元の英国の報告も1912年の刊行（英国の国王の著作権は刊行物で50年＝切れている見込み・推定）。文字の層は OCR＝表は段組みが崩れる（§7 は頁の画像で確認） |
| **G2** | 英国運輸省 海難調査局（MAIB）『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』（HMSO・送り状 1992-03-12・30頁＝スキャン＋OCR） | https://assets.publishing.service.gov.uk/media/54c15bf240f0b6158d000027/MAIBReport_ReappraisalOfEvidence-SSCalifornian-Titanic-1992.pdf | `gov/maib1992.pdf`（530e9c2d）・頁の画像＝`maib_pages/`・OCR＝`maib_ocr.txt` | gov.uk の頁は OGL v3.0（"except where otherwise stated"）／PDF の表紙裏は "Crown copyright 1992 / Applications for reproduction should be made to HMSO"＝**どちらが効くか未確定**→紙面は引用の型（出典・主従・必要最小限・無加工の額装）で。🔴 **文字の層は緯度経度が全部欠ける**（§2-0） |
| G3 | NIST-IR 6118（1998-02）『Metallurgy of the RMS Titanic』 | https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir6118.pdf | `gov/nistir6118.pdf`（f129a9b4） | 米国の公文書＝PD。⚠️ 図6・図8は第三者の本から（①） |
| G4 | 米国の法 37 Stat. 199（1912-07-23・無線の装置と当直の改正） | https://www.govinfo.gov/link/statute/37/199 | `gov/stat37_199.pdf`（31a619c6） | PD。条文「two or more persons skilled in the use of such apparatus, one or the other of whom shall be on duty at all times while the vessel is being navigated」（文字の層 89〜91行で確認） |
| G5 | 米国の法 37 Stat. 302（Radio Act・1912-08-13） | https://www.govinfo.gov/link/statute/37/302 | `gov/stat37_302.pdf`（d93daedb） | PD（遭難の通信が最優先＝①） |
| G6 | 米国の法 36 Stat. 629（1910年の Wireless Ship Act） | https://www.govinfo.gov/link/statute/36/629 | `gov/stat36_629.pdf`（00a4798d） | PD（通信士は1人でよかった＝①） |
| **G7** | 米国上院 商務委員会の小委員会の公聴会 **S. Doc. 726**（1,170頁・495,755,489 bytes） | https://www.govinfo.gov/content/pkg/SERIALSET-06167_00_00-002-0726-0000/pdf/SERIALSET-06167_00_00-002-0726-0000.pdf | 🔴 **`F:\jiko_src\ep26\`**（C: の空きが 500MB の線を割るため＝10-27 カズヤくん「F: に置く」） | PD。証言の公式の印刷＝§4-3 で書き起こしと照合 |
| T1 | 英国の審問の証言（Day 1〜36・問の番号 Q） | https://www.titanicinquiry.org/ （BOTInq） | **保存していない**（10-26〜27 係A がメモリで読んだ） | **書き起こし**（有志）。引用は「書き起こし」と断る |
| T2 | 米国上院の公聴会の証言（Day 1〜18） | https://www.titanicinquiry.org/ （USInq・例 AmInq08Lord01） | 同上 | 書き起こし＝G7 で照合（§4-3） |
| T3 | 米国上院の報告 S. Rept. 806（1912-05-28）の書き起こし（AmInqRep06「Steamship "Californian's" Responsibility」） | https://www.titanicinquiry.org/ （USInq の AmInqRep） | 同上 | 🔴 **公的な写しと未照合**（govinfo に無い・senate.gov と loc.gov は 403） |
| N1 | NOAA Ocean Exploration の保管の頁（2003年・2004年の残骸の調査） | https://archive.oceanexplorer.noaa.gov/explorations/03titanic/welcome.html ・ https://archive.oceanexplorer.noaa.gov/explorations/04titanic/welcome.html ・ https://archive.oceanexplorer.noaa.gov/titanic/welcome.html | 保存していない（係B） | 点ごとの権利＝[materials.md](materials.md) §2。⚠️ 旧 URL（oceanexplorer.noaa.gov/explorations/…）は 404＝保管のサブドメインへ移っていた |
| N2 | NOAA Ocean Exploration の使い方の方針（Usage and Credit） | https://oceanexplorer.noaa.gov/about/media-kit/ | — | "If the image caption includes the word “copyright,” additional permissions are required for use." |
| N3 | NOAA 海洋保護区（Sanctuaries）の歴史の頁 | https://sanctuaries.noaa.gov/maritime/titanic/past_expeditions.html ・ …/expedition_results.html | — | 歴史のまとめ＝二次（発見の日・§9） |
| U1 | USCG 歴史室の年表・記事 | https://www.history.uscg.mil/Complete-Time-Line/Time-Line-1900-2000/ ・ https://www.mycg.uscg.mil/News/Article/4372186/ | — | 国際氷山監視の始まり（§8） |
| A1 | NARA の目録（naId 278334・278335・278331・278332・278337・278338・278339・5729534・5722336・595107・278329） | https://catalog.archives.gov/id/{naId} | 保存していない（JSON を読んだ） | 使用の制限＝"Unrestricted"（係B）。物は 0.1MB の GIF が多い＝大きい版は Commons（materials.md） |
| — | （取れなかった）米国議会図書館（LOC）の映像の目録・British Pathé・www.noaa.gov の法務室の頁・navcen（USCG） | — | — | 403 か確認画面＝突破しない（LOC はカズヤくんが確認を通す段取り＝materials.md §4） |

---

## 2. 案B の芯＝MAIB 1992 を頁の画像で照合

### 2-0 どう照合したか
- PDF 30頁を 300dpi の画像に描き（`probe/pages26.py`）、Windows の OCR で読み直して、PDF の文字の層と1行ずつ突き合わせた（`probe/ocrdiff26.py`＝1,117行のうち117行が食い違い）。食い違いのうち**数字・座標・色の語の31行を頁の画像から切り出して原寸で見た**（`probe/crops26.py`→`src/look/maib_coords.png`＝見た1枚目）
- 🔴 **文字の層の欠け**＝**緯度経度がすべて空白**（p.3・p.7・p.8・p.10・p.11）・p.18 の「**red**」・p.9 の「ENE」「1¼」・p.10 の「(308°T)」・p.11 の「49°W」「41°20′N」「field ice」「3½」。下の表の値は**頁の画像**で読んだもの
- 本文は通しで読んだ（`src/txt/maib_bypage.txt`）。PDF 24頁＝Annex 1（英国海軍の航路図の抜粋・594×840 の8ビット画像＝文字の層なし）・PDF 25〜28頁＝Annex 2（1912年の英国の報告のカリフォルニアン号の節の写し・欄外に問の番号）・PDF 29頁＝Annex 3（位置の図＝文字の層なし・OCR で札の字は読めた）・PDF 30頁＝Annex 4（異常屈折の説明＝航海の手引きの写し）

### 2-1 位置（頁の画像で読んだ値）
| 何 | 値 | 印刷の頁 | 誰の見方 |
|---|---|---|---|
| 衝突の位置（推定） | **41°47′N 49°55′W**（14日 2345） | p.3・p.7 | 2人とも（沈んだ位置から海流で逆算） |
| 沈んだ位置（ボイラーと船尾の位置＝1985年の発見） | **41°43′.6N 49°56′.9W** | p.3・p.7 | 2人とも |
| 1912年の審問が採った位置＝タイタニック号が無線で送った位置 | **41°46′N 50°14′W** | p.7（英国の報告 Q23 p.85 と同じ） | — |
| 残骸と1912年の位置のずれ | 約13マイル | p.2 | — |
| カリフォルニアン号の14日正午（観測） | 42°05′N 47°25′W | p.7 | — |
| 北極星の緯度（19:30・一等航海士） | 42°05′N（正午と同じ＝西へ真っすぐ進んだ証し） | p.8・p.10 | 次長の論拠 |
| アンティリアン号への電報（18:30 の推測航法の位置） | 原文「42.3N 49.9W」＝42°3′・49°9′／船長はのちに 42°05′ と言った（「5」を「3」と読み違えたかもしれない） | p.8・p.10 | — |
| 止まった位置（22:21・船長の推測） | **42°05′N 50°07′W** | p.8 | 1912年の法廷は「正確でない」（英国の報告 p.56） |
| 15日正午の位置（観測）／漂流物の位置（推定） | 41°33′N 50°09′W／41°33′N 50°01′W | p.8 | — |
| 衝突のときのカリフォルニアン号（調査官） | **41°50′N 50°07′W** あたり・ただし「probably further East and only 5 to 7 miles off」 | p.3 | 外部の調査官 |
| 同（次長） | **42°00′N 50°09′W** あたりかやや北・**17〜20マイル・most likely about 18 miles**・タイタニック号から NW by N | p.3・p.11 | 次長 |
| 海流 | 南へ・約196°（真方位）・約1.3ノット／「something like 1¼ knots」 | p.9 | 2人とも（流れの有無ではなく「いつから効いたか」で割れる） |
| マウント・テンプル号が西経50°を越えた緯度 | 41°20′N（氷を見ていない） | p.11 | — |
| 氷原の東の端 | 49°W より東に氷山の報告なし・カルパチア号は氷山の中でも氷原の東 | p.11 | — |
| カルパチア号の針路 | N 52 W（308°T）・58マイル・約2時間後に左舷の少し前に灯（2:40） | p.10 | 次長（北へ流された論拠） |

### 2-2 頁の対応（本文）
| 節 | 印刷の頁（PDF） | 中身 |
|---|---|---|
| 送り状 | （PDF 3） | 首席調査官 1992-03-12。外部から任命した調査官（「recently retired from a post as Principal Nautical Surveyor」・経験豊かな船長）→首席は「I do not fully agree with all the Inspector's findings」→次長にさらに調べさせた→「I full[y] endorse the Deputy Chief Inspector's report and conclusions.」 |
| 1 Introduction | p.1〜2（PDF 5〜6） | 2340・1490 lives・カルパチア号は0400ごろ・カリフォルニアン号の通信士は1人で最初の遭難の通信の少し前に当直を終えていた・問24(b) の写し・船長は再審を求めたが退けられた（正式の告発が無く免状にも処分が無い＝控訴の道も無い）・1950年代の本と映画・2度の請願・1985年の残骸・1990年に運輸大臣が再評価を命じた |
| 2 Terms・結論・背景 | p.3〜6（PDF 7〜10） | 結論の要約（§2-1）・背景（22ノット・2340 に氷山・「hard to starboard」は当時の号令で船首は左へ・0220 沈没・衝突から沈没まで船は止まっていた・「the lights of another vessel were seen」→火箭とモールス灯）・「It is of course no part of this reappraisal to consider the conduct of TITANIC … leading up to the collision」（p.4）・「It is both wrong and misleading to refer to the FI proceedings … as a "Board of Trade Inquiry"」（p.5）・時計の注（p.6） |
| 3 位置 | p.7〜11（PDF 11〜15） | §2-3 の距離と海流 |
| 4 見えたか | p.12〜13（PDF 16〜17） | §2-3 |
| 5 火箭 | p.14（PDF 18） | §2-3 |
| 6 船長の行い | p.15〜17（PDF 19〜21） | §2-3 |
| 7 結びの注 | p.18〜19（PDF 22〜23） | 動いていたら・火箭の色・その後の船長・「no villains」 |

### 2-3 🔴 2人の見方を対で（距離・見え方・火箭・時計・動いた場合）
| 論点 | 外部の調査官（Inspector） | 次長（Deputy Chief Inspector）＝首席が支持 | 頁 |
|---|---|---|---|
| 止まっていた間の距離 | 「between 5 and 10 miles apart … and probably nearer five」・個人の見方は「between 5 and 7 miles」＝1912年の法廷は正しい | 「substantially greater, probably about 18 miles」・「between 17 and 20 miles」 | p.3・p.7・p.11 |
| 船長の位置がずれた理由 | 13日か14日の正午から南へ流され続け、それを入れていなかった（だから実は8〜10マイル） | 南への流れが効いたのは氷原の近くの数時間だけ。理由＝①北大西洋海流の区域で南へ流れるのは異例 ②正午と19:30 の北極星の緯度が同じ（42°05′N） ③アンティリアン号への電報（作り得ない記録）④カルパチア号は北へ流された（灯が左舷に見えた）⑤氷原より東に氷が無い（⚠️ 10-27 ④で訂正＝原文は「西経49度より東に、孤立した氷山の知らせも無い」`no reports even of isolated bergs east of`＋OCR「49°W」＝氷原の東にはタイタニック号とカルパチア号のいた氷山がある）＝流されたのは最大3½マイル | p.9〜11 |
| タイタニック号は見えたか | 見えた（23時ごろから沈むまで・船長と2人の当直の航海士の証言と、タイタニック号の動きの一致が強い） | 「I think it possible that she was seen, due to abnormal refraction … but more likely that she was not seen.」。決め手＝**タイタニック号の側は衝突のあと（0030ごろ）まで船を見ていない**（見張りも船橋も居た）＝カリフォルニアン号が見ていた船は23時ごろからずっと見えていたのに | p.3・p.12 |
| 見えた船は何か | （タイタニック号） | たぶん第三の船（東から来て氷で止まり、すき間を探して去った）か、異常屈折で見えたタイタニック号。⚠️ ノルウェーのアザラシ猟船の後年の話は「fairly obvious weaknesses」 | p.13・p.14 |
| 灯の色と方位 | — | 船長は最初に緑（右舷）の灯、のちに赤（左舷）＝止まってから右へ回った／二等航海士は方位が変わったのを見た＝止まったままのタイタニック号とは合わない（ただし重くは見ない） | p.13 |
| 火箭は見えたか | 見えた | 「I entirely agree」・ほかの船の会社の信号という見込みは「quite unrealistic」・低く見えたのは遠かったから | p.14 |
| 正しい対応をしたか | していない | 同意。「Merely attempting to call by morse lamp fell far short of what was needed.」 | p.15 |
| あるべきだった手 | — | ①船長を呼び、すぐ応じなければ二等航海士が自分で行く ②機関室に「Stand By Engines」 ③通信士を起こす ④船長は船橋へ行き、機関と通信士を確かめて火箭の方へ向かう | p.15〜16 |
| なぜしなかったか | — | 酔っていた・冷淡・氷が怖かった、の説は退ける（船長はほとんど酒を飲まない・あとで氷原を2回越えた）。「I think the message from the Bridge simply did not get through.」（深く眠っていて呼ばれても目が覚めない状態＝推し量り）・二等航海士は「seriously at fault」（自分で降りて行くべきだった） | p.16〜17 |
| 動いていたら | — | 最初の火箭（0045ごろ・タイタニック号の時計）で真っすぐ向かえば、最短17マイルなら沈むころに着いた＝ただし現実的でない。正しく動けば船長が0055ごろ船橋へ・氷で慎重に・無線で誤った位置を受けて迷う→着くのは沈んだあと＝カルパチア号の役目（救助）を担っただけ。「I do not think any reasonably probable action by Captain Lord could have led to a different outcome of the tragedy.」🔴 **条件つき**＝直前に「if I am right as to the distance apart」・直後に「This of course does not alter the fact that the attempt should have been made.」 | p.18 |
| 時計 | — | 船ごとに違うが、タイタニック号とカリフォルニアン号の差は「only likely to have been a few minutes」＝時刻は各船の時計のまま使う | p.6 |
| 結び | — | 船長はレイランド社の職を失ったが別の会社でまもなく船長に戻り、第一次大戦を越えて1920年代まで海に・1962年に亡くなった・正式の処分は無かった・「there are no villains in this story: just human beings with human characteristics.」 | p.19 |

### 2-4 2人とも認めること／言い切らないこと
- ✅ **2人とも認める**＝火箭は見えた（p.14）・正しい対応をしなかった（p.15）・海流は南へ流れていた（p.9）・沈んだ位置は残骸の位置（p.7）
- 🔴 **割れていること**＝距離（5〜10／17〜20）・タイタニック号が見えたか・見えた船は何か → **題・サムネ・絵で「救えなかった」「見えていなかった」「別の船だった」と言い切らない**（ルール B4-5）。語りは「調査官は〜と見た。次長は〜と見た。首席は次長の報告を支持した」と帰属つきで並べる
- 🔴 「結果は変わらなかったと思う」は**次長の意見・距離が正しければの条件つき**・すぐあとに「それでも向かうべきだった」
- ⚠️ 1912年の法廷は船長を名指ししていない（「the CALIFORNIAN」＝p.15）。責任の重心を「船橋からの知らせが届かなかった」（p.17）と二等航海士（p.17）へ動かしたのは次長の見方

---

## 3. 1912年の英国の報告（G1＝S. Doc. 933）の決め所（親が頁の文字で確かめた）

| 頁 | 原文（OCR の崩れは直して読む） | 使い道 |
|---|---|---|
| p.5 | "the loss of 1,490 lives"・"brought about by the excessive speed"（①が grep・行105・113） | N・原因の正式の結論 |
| p.25 | 救命艇14隻×65人・カッター2隻×40人・折りたたみ艇4隻×47人＝"a total of 11,327.9 cubic feet for 1,178 persons." | 案C |
| p.32 | 乗員885（甲板66・機関325・司厨494）・乗客1,316（一等325・二等285・三等706）・「Eight bandsmen were included in the second-class passenger list.」・子ども109・「In all, 2,201 persons were on board.」＝**頁の画像で確認**（§7） | c2 |
| p.40 | "perfectly clear and fine. There was no moon, the stars were out" | c4（月の写る素材を使わない） |
| p.40〜41 | 速度約22ノット（p.40・問14 p.80「About 22 knots.」）・慣行と船長の過失（①の grep） | c8（案A） |
| p.45 | "water came into the five forward compartments" | c4 |
| p.51〜52 | "No. 1 certainly left with only 12; this was an emergency boat with a carrying capacity of 40. No. 7 left with only 27, and No. 6 with only 28; these were lifeboats with a carrying capacity of 65 each" | c7（案C） |
| p.54 | "At 12.15 a. m. the distress signal CQD was sent."・"By 12.25 Mr. Boxall, the fourth officer, had worked out the correct position"・カルパチア号は58マイル・"exploding in the air and throwing off white stars"・"began about the time that No. 7 boat was lowered (12.45 a. m.), and it continued until Mr. Boxall left the ship at about 1.45"・Morse light・"about 5 or 6 miles"・"He got no answer."・"In all, Mr. Boxall fired about eight rockets."・"There appears to be no doubt that the vessel whose lights he saw was the Californian."・"eight rockets having been seen between 12.30 and 1.40"・"she had only one Marconi operator on board and he was asleep." | c5・c6 |
| p.55 | カルパチア号＝"(17½ knots)"・"At about 2.40 a. m. he saw a green flare"・"he stopped his ship at 4.05"・"He sighted the first boat (No. 2) and picked her up at 4.10."・13隻＋2隻＋2隻・"712 persons, one of whom died shortly afterwards"・"it was 8 a. m. before they had all been picked up"・"The court desires to record its great admiration of Capt. Rostron's conduct." | c7 |
| p.56 | 19:30 の電報（"latitude 42° 3' N., longitude 49° 9' W. Three large bergs, 5 miles to southward of us."）・タイタニック号の返事 "It is all right. I heard you sending it to the Antillian, and I have got it."・"S. 89° W. true until 10.20 p. m."・船長の位置 42°5′N 50°7′W（文字の層は「57° 7」＝崩れ）・"about 19 miles N. by E. of the position of the Titanic when she foundered"・"I am satisfied that this position is not accurate."・"remained approximately stationary until 5.15 a. m." | c6 |
| p.57 | 23時ごろ東から近づく灯・"I think the Titanic is near us. I have got her."・"We are stopped and surrounded by ice."・"The Titanic replied: "Keep out.""（理由＝ケープ・レース局の弱い信号がかき消された）・"Evans heard the Titanic continuing to communicate with Cape Race up to the time he turned in at 11.30 p. m."・船長「6 or 7 miles」「about 5 miles」「something like ourselves」・三等航海士「She is evidently a passenger steamer.」・"these lights went out at 11.40"・"one bell was struck to call the middle watch" | c6 |
| p.58 | 三等航海士の問答（"Most decidedly I do, but I do not put myself as being an experienced man."）・見習い 12.20・"Sometime after 12.30 a. m., ［ドンキーマン］, the donkey man, states that he saw two rockets"・"about 1.10 a. m., Mr. Stone reported to the captain by voice pipe, that he had seen five white rockets"・"Are they company's signals?"・"go on Morsing"・"three more white rockets"・"A ship is not going to fire rockets at sea for nothing"・"he saw the last of the rockets fired at about 1.40"・"altogether we had seen eight of these white lights like white rockets" | c6 |
| p.59 | "the master asked him if all the rockets were white"・"It was five minutes past two"・"A gradual disappearing of all her lights"・"At about 2.40 a. m. … disappeared bearing SW. ½ W."・"I again assured him they were all white, just white rockets."・船長は「1.15ごろ白い火箭1つ」・"between 1.30 and 4.30 … he had no recollection of anything being reported to him at all"・4.30 "Yes, I know; he has been telling me."・"She looks all right; she is not making any signals now."・"This mistake was not corrected."・"At about 6 a. m. Capt. Lord heard from the Virginian"・7.30 マウント・テンプル号・漂流物の位置 41°33′N 50°1′W | c6・c7 |
| p.60 | "S. 16° W. (true), 19 miles"・"There are contradictions and inconsistencies in the story as told by the different witnesses. But the truth of the matter is plain."・"The Titanic collided with the berg at 11.40."・"The number sent up by the Titanic was about eight. The Californian saw eight."・"from about 12.45 to 1.45 o'clock"・"At 2.20 a. m. the Titanic had foundered."・"But no other ship to fit this theory has ever been heard of."・"I am advised that the distance was probably greater, though not more than 8 to 10 miles."・"loose ice extending for a distance of not more than 2 or 3 miles"・"Had she done so she might have saved many if not all of the lives that were lost." | c1・c8 |
| p.62 | "a provision for 962 persons"・"1,178 persons, a number far in excess of the requirements of the table" | c2（案C） |
| p.85 | 問23 "Two twenty a. m. (ship's time) April 15. Latitude 41° 46' N., longitude 50° 14' W."・問24(b) "The Californian. She could have reached the Titanic if she had made the attempt when she saw the first rocket. She made no attempt." | c8 |

- ⚠️ p.54 は位置を「**correct**」と書くが、MAIB は残骸から約13マイル違うとした（p.2・p.7）＝1912年の報告の言い方を画面に出すときは、のちに違うと分かったことを同じ章で言う
- ⚠️ カリフォルニアン号の時刻（p.56〜60）と タイタニック号の時刻（p.54・p.60）を、報告は同じ線に並べて「この時刻ごろ見た」と結んだ（p.60）＝各船の時計の差は §6

---

## 4. 証言（T1・T2＝書き起こし・係A＝2026-10-27）

係A が英国の審問の Day 2〜36 の証言の頁（276頁）と米国の公聴会の指定の証人の頁（58頁）・上院の報告をメモリで読んだ（約40万トークン・71回・29分）。頁は保存していない。英＝日と Q／米＝日と頁の名。英の日付＝Day 7（1912-05-14）・Day 8（05-15）・Day 13（05-22）・Day 15（05-24）・Day 16（06-04）・Day 28（06-21）。

### 4-1 決め所の証言（原文は書き起こしのまま）
| 項目 | 証人（役職） | 調べ | 原文 | 注 |
|---|---|---|---|---|
| 時計 | カリフォルニアン号 船長（Stanley Lord） | 英 Day 7 Q6691 | "Yes, ship's time for longitude 47° 25.'" | 船の時刻 |
| 時計 | 同 | 米 Day 8 Lord01 | "There is an hour and fifty minutes time between New York and my noon position on the 14th." | NY＋1時間50分 |
| 時計 | 同 通信士（Cyril Evans） | 英 Day 8 Q8935 | "One hour and fifty-five minutes." | 止まった所で NY＋1時間55分 |
| 時計 | タイタニック号 四等航海士（Joseph Boxhall） | 米 Day 10 Boxhall02 | "At 11.46 p.m., ship's time, it was 10.13 Washington time, or New York time." | NY＋1時間33分 |
| 時計 | カルパチア号 船長（Arthur Rostron） | 米 Day 1 Rostron01 | "Yes, 12:35; that was our apparent time." ／ "The New York time at 12:35 was 10:45 p. m. Sunday night." | NY＋1時間50分 |
| 停止 | カリフォルニアン号 船長 | 英 Day 7 Q6702・Q6704 | "10. 21 p.m." ／ "Forty-two deg five min N, and 50 deg 7 min. W." | 三等航海士は腕時計で 10.26（Q8117） |
| 距離 | 同 | 米 Day 8 Lord01 | "19 1/2 to 19 3/4 miles; south 16 west, sir, was the course." | 英 Q6983 "I thought we ought to have seen her signals at 19 miles" |
| 見えた船 | 同 | 英 Day 7 Q6752・Q6754 | "She was something like ourselves." ／ "A medium size steamer." | 米「This is not the Titanic; there is no doubt about it.」 |
| 見えた船 | カリフォルニアン号 三等航海士（Charles Groves） | 英 Day 8 Q8135・Q8172 | "About 11.10, ship's time, I made out a steamer …" ／ "Yes, she is evidently a passenger steamer coming up on us." | Q8203・8217 灯が消えたのは 11.40・one bell |
| 見えた船 | 同 二等航海士（Herbert Stone） | 英 Day 7 Q7814・Q7819 | "One masthead light and a red sidelight and two or three small indistinct lights." ／ "Approximately about five miles." | |
| 見えた船 | 同 見習い（James Gibson） | 英 Day 7 Q7545 | "I thought she was a tramp steamer, and I told him so." | |
| 見えた船 | 同 機関部の乗組員（ドンキーマン） | 英 Day 16 Q18136・米 Day 8（供述書） | "It could not have been anything but a passenger boat" ／ "saw the lights of a very large steamer about 10 miles away." | 上院の報告に名で出る |
| 火箭 | 二等航海士 | 英 Day 7 Q7832・Q7840 | "I saw one white flash in the sky, immediately above this other steamer." ／ "I saw four more then." | 1.10ごろ伝声管（Q7830） |
| 火箭 | 同 | 英 Day 7 Q7870・Q7871 | "He asked me, "Are they Company's signals?"" ／ "I said, "I do not know, but they appear to me to be white rockets."" | |
| 火箭 | 同 | 英 Day 7 Q7921 | "they were only about half the height of the steamer's masthead light" | 低かった（MAIB の論点） |
| 火箭 | 同 | 英 Day 7 Q8033 | "I knew that rockets shown at short intervals, one at a time, meant distress signals, yes." | |
| 火箭 | 見習い | 英 Day 7 Q7560・Q7565 | "He asked me were they all white?" ／ "Five minutes past two by the wheelhouse clock." | 操舵室の時計 |
| 火箭 | 船長 | 英 Day 7 Q6790・Q7280・Q7288 | "He said he saw a white rocket." ／ "I do not know; I was asleep." ／ "I very likely was half awake." | |
| 火箭 | 船長 | 米 Day 8 Lord03 | "At a quarter past he said, "I think she has fired a rocket."" | |
| 無線 | 通信士 | 英 Day 8 Q8991〜8993 | "Yes, 11 o'clock ship's time." ／ "I said, "We are stopped and surrounded by ice."" ／ "They said, "Keep out."" | |
| 無線 | 通信士 | 米 Day 8 EvansCF01 | "He turned around and said "Shut up, shut up, I am busy; I am working Cape Race," and at that I jammed him." | 🔴 英と米で文言が違う |
| 無線 | 通信士 | 英 Day 8 Q8927・Q9053・Q9056 | "Half-past eleven, ship's time."（寝た）／ "3.40 or 3.45, New York time."（起こされた）＝問い "3.45 New York time is 5.40 ship's time" に "Yes." | 米の報告は NY 3.30 |
| 無線 | 三等航海士 | 英 Day 8 Q8289・Q8285 | "between 12.15 and 12.20" ／ "Nothing at all."（通信室でヘッドホンを聞いた） | |
| 火箭（タイタニック号） | 四等航海士 | 英 Day 13 Q15395〜15399 | "between half a dozen and a dozen" ／ "The socket distress signal." ／ "probably five minutes"（間隔） | 報告は「about eight」 |
| 火箭（タイタニック号） | 同 | 英 Day 13 Q15409〜15410 | "I judged her to be between 5 and 6 miles when I Morsed to her" ／ "I did not see any answer whatever." | |
| 火箭（タイタニック号） | 操舵手（George Rowe） | 英 Day 15 Q17684 | "From about a quarter to one to about 1.25." | |
| 見えた灯（タイタニック号） | 二等航海士（Charles Lightoller） | 英 Day 12 Q14138・Q14140 | "A white light about two points on the port bow" ／ "certainly not over 5 miles away." | |
| カルパチア号 | 船長 | 米 Day 1 Rostron01 | "north 52 degrees west true 58 miles" ／ "At 2:40, I saw a flare" ／ "Ordered company's rockets to be fired at 2:45 a. m. and every quarter of an hour after" ／ "At 4:10 I got the first boat alongside." | 英 Q25394「green flare … White Star Company's night signal」 |
| カルパチア号 | 同 | 英 Day 28 Q25552 | "We saw masthead lights quite distinctly of another steamer between us and the "Titanic." That was about quarter-past three." | ほかの船が居た証言 |
| カルパチア号 | 同 | 英 Day 28 Q25551 | "The first time that I saw the 'Californian' was at about eight o'clock on the morning of 15th April." | |
| 「沈まない」 | ホワイト・スター・ライン社の会長（会社の人） | 英 Day 16 Q18755 | "the ship was looked upon as practically unsinkable; she was looked upon as being a lifeboat in herself." | 🔴 3隻の乗組員の口からは一度も出ない（Day 2〜36 を語で走査） |

### 4-2 食い違う時刻・数・距離（係A の一覧から・要点）
1. **カリフォルニアン号の時計と NY の差**＝1時間50分（船長・正午の位置）／1時間55分（通信士・止まった位置）／約2時間（通信士・米）。タイタニック号は1時間33分（四等航海士）・カルパチア号は1時間50分（船長）。⚠️ 係の引き算（カリフォルニアン号の時計が約17〜22分進んでいた）は**証言ではない**。MAIB は「差は数分の見込み」（p.6）＝割れる。船どうしの差を直接言った証言は見つからない
2. **止まった時刻**＝10.21（船長・一等航海士・日誌）／10.26（三等航海士の腕時計）／「10.30から」（ドンキーマンの供述書）
3. **距離**＝船長 19½〜20マイル・漂流物まで約30マイル／見えた船まで 4〜7（船長・二等航海士・見習い・三等航海士）・約10（ドンキーマン）／上院の報告「19マイルより近い」
4. **見えた船**＝「自船ぐらい・普通の貨物船」（船長）・「明らかに客船」（三等航海士）・「不定期の貨物船（トランプ）」（見習い）・「とても大きい」（ドンキーマン）。マストの灯 1つ（船長・二等航海士・見習い）／2つ（三等航海士・ドンキーマン）。舷灯 緑（船長）／赤（ほか）
5. **火箭の数**＝8（二等航海士＝5＋3）・3（見習い）・1と聞いた（船長）・2（ドンキーマン）／タイタニック号の側「半ダースから1ダース」（四等航海士）・報告「about eight」
6. **知らせの時刻**＝1.10（二等航海士）／1.15（船長）。見習いが下りたのは 2.00（二等航海士）／2.05（見習い）
7. **タイタニック号の返事**＝「Keep out.」（英）／「Shut up, shut up, I am busy; I am working Cape Race」（米）
8. **通信士が寝た時刻**＝23.30（英）／23.35（米）。起こされた＝NY 3.30（米の報告）／NY 3.40〜3.45＝船 5.40（英）
9. **カルパチア号の朝**＝全員の収容 8.30（船長・米）／最後のボート 7.40〜7.45（船長・英）／報告「8 a. m.」
10. 「four-masted steamer with one funnel」の同じ言い回しが、カリフォルニアン号の一等航海士（4時・南）とカルパチア号の船長（5時・北）に出る＝同じ船かは資料で決まらない

### 4-3 公式の印刷（G7＝S. Doc. 726）での照合
- 取得＝`F:\jiko_src\ep26\SERIALSET-06167_00_00-002-0726-0000.pdf`（495,755,489 bytes＝① の記録と一致・md5 `47d272b5620e117787abcf0961b51688` を2回・末尾 %%EOF）。⚠️ C: に落とし始めたが、空きが 500MB の線を割る見込み（814MB→約420MB）で止め、10-27 カズヤくん「F: に置く」で F: へ移して続きから取った
- 照合＝`probe/sd726grep26.py`（句も本文も英小文字と数字だけに揃え、1頁ずつ・頁またぎも拾う）→ `src/sd726_grep.tsv`。**米国の公聴会の書き起こしから取った決め所 38句のうち 36句が公式の印刷にあった**（頁は **PDF の頁**＝印刷の頁とは数頁ずれる。例 PDF 1150＝印刷 1148・PDF 1163＝印刷 1156）

| 証人（役職） | 句（§4-1 の米の原文） | PDF の頁 |
|---|---|---|
| カリフォルニアン号 船長 | ship's time for 47 ／ an hour and fifty minutes time between New York ／ south 16 west, sir, was the course ／ the Virginian as the position where she struck an iceberg | 719・724・720・720 |
| 同 | Nineteen and one-half to twenty miles ／ This is not the Titanic; there is no doubt about it ／ I think she has fired a rocket ／ went to sleep ／ The officer on watch saw some signals, but he said they were not distress signals ／ Nineteen and a half miles is a long ways ／ an ordinary cargo steamer | 727・733・733・733・732・733・736 |
| 同 通信士 | we are stopped and surrounded by ice ／ New York time I called him up ／ **Shut up, shut up, I am busy; I am working Cape Race** ／ I put the phones down and took off my clothes and turned in ／ There is a ship that has been firing rockets in the night | 739・739・739・740・740 |
| 同 通信士 | 「I was answered by the Frankfurt」＝この綴りでは無い（印刷は「Frankfort」の綴り＝p.786・1102 に出る＝⑤a までに頁で当てる） | — |
| 同 機関部の乗組員（供述書） | the lights of a very large steamer about 10 miles away ／ I saw a white rocket about 10 miles away ／ pale blue, or white ／ At four minutes after 12 ／ It was no tramp | 714・714・716・717・717 |
| カルパチア号 船長 | that was our apparent time ／ The New York time at 12 ／ north 52 degrees west true 58 miles ／ I saw a flare, about half a point on the port bow ／ company's rockets to be fired ／ I got the first boat alongside ／ the Leyland Line steamer Californian hove up | 23・23・24・25・25・25・26 |
| タイタニック号 四等航海士 | it was 10.13 Washington time ／ I considered she was about 5 miles away ／ Just white stars, bright ／ I do not think we could see them 14 miles | 922・913・914・938 |
| 同 操舵手 | I judged it to be a stern light ／ 「five and twenty」（「five and twenty minutes after」の形では無い＝印刷の句読点の違いの見込み） | 528・523 |
| 同 二人目の通信士 | one was keeping New York time and the other was keeping ship's time | 910 |
| 同 二等航海士 | Two points on the port bow | 452 |
| カルパチア号 通信士 | About 11.20, sir, New York time | 499 |
- 🔴 **米国上院の報告（S. Rept. 806）は S. Doc. 726 に入っていない**（巻末 PDF 1160〜1170頁は「DIGEST OF TESTIMONY」＝証言の要約）。「grave responsibility」「dictates of humanity」「proud distinction」は 0件＝§5 は書き起こしのまま（HathiTrust も確認画面で止まった＝突破しない）
- ⚠️ 英国の証言（T1）は公式の写しが公的な機関の置き場に無い＝書き起こしのまま（英国の報告 G1 に同じ趣旨の文がある所は G1 を正本にする＝§3）

---

## 5. 米国上院の報告（T3＝書き起こし・AmInqRep06）
| 原文 | 注 |
|---|---|
| "was distant in a northerly direction 19 1/2 miles according to the Captain's figures (p. 717)." | 船長の数 |
| "There is no evidence that any rockets were fired by any vessel between the Titanic and the Californian" | |
| "the Californian, controlled by the same company, was nearer the Titanic than the 19 miles reported by her captain" | |
| "her officers and crew saw the distress signals of the Titanic and failed to respond to them in accordance with the dictates of humanity, international usage, and the requirements of law." | |
| "such conduct, whether arising from indifference or gross carelessness, is most reprehensible, and places upon the commander [of] the Californian a grave responsibility." | 書き起こしに "of" が無い＝脱字の見込み（推測） |
| "The wireless operator of the Californian was not aroused until 3.30 a.m., New York time, on the morning of the 15th" | (p. 736) |
| "had the wireless operator of the Californian remained a few minutes longer at his post … that ship might have had the proud distinction of rescuing the lives of the passengers and crew of the Titanic." | |
- 🔴 公的な写し（S. Rept. 806）と未照合＝画面に出すなら「上院の報告（書き起こし）」と断るか、④までに公的な写しを探す（HathiTrust などの非公的な置き場は落とす前にカズヤくんに聞く）

---

## 6. 🔴 時計と時刻の表（画面の時刻はこの表の値だけ・どの船の時計かを言う）
| 出来事 | 時刻 | どの時計 | 出どころ |
|---|---|---|---|
| カリフォルニアン号 アンティリアン号へ氷の電報 | 18:30 の位置・19:30 に送信 | カリフォルニアン号 | 英 p.56・MAIB p.7〜8 |
| カリフォルニアン号 氷原で停止 | 22:21（三等航海士 22:26） | カリフォルニアン号 | 英 Q6702・Q8117・MAIB p.8 |
| 東から近づく船の灯 | 23:00ごろ（三等航海士 23:10） | カリフォルニアン号 | 英 p.57・Q8135 |
| 「止まって氷に囲まれている」→「Keep out.」 | 23:00ごろ（NY 21:05） | カリフォルニアン号 | 英 p.57・Q8991〜8993 |
| 通信士が寝る | 23:30 | カリフォルニアン号 | 英 p.57 |
| 衝突 | 23:40（MAIB p.1 2340・p.3 2345） | タイタニック号 | 英 p.60 |
| 見えた船の灯が消えた（one bell） | 23:40 | カリフォルニアン号 | 英 p.57 |
| CQD | 0:15 | タイタニック号 | 英 p.54 |
| 位置を出し直し・「Come at once」 | 0:25 | タイタニック号 | 英 p.54 |
| カルパチア号が受けた | 0:35（NY 22:45） | カルパチア号（視太陽時） | 米 Rostron01 |
| 火箭 | 0:45ごろ〜1:45ごろ・約8発 | タイタニック号 | 英 p.54・p.60 |
| 二等航海士が伝声管で「白い火箭5つ」 | 1:10ごろ（船長は1:15） | カリフォルニアン号 | 英 p.58・Q6788 |
| 最後の火箭を見た | 1:40ごろ | カリフォルニアン号 | 英 p.58 |
| 見習いが海図室へ「全部で8つ・全部白」 | 2:05 | カリフォルニアン号（操舵室の時計） | 英 p.59・Q7565 |
| 沈没 | 2:20 | タイタニック号 | 英 Q23 p.85 |
| 見えた船が見えなくなった | 2:40 | カリフォルニアン号 | 英 p.59 |
| カルパチア号が緑の灯を見た | 2:40 | カルパチア号 | 英 p.55・米 Rostron01 |
| カルパチア号が止まる・最初のボート（2号艇） | 4:05・4:10（米の証言は4:00・4:10） | カルパチア号 | 英 p.55 |
| 一等航海士が二等航海士と交代・船長を起こす | 4:00・4:30 | カリフォルニアン号 | 英 p.59 |
| 通信士が起こされる | 5:40ごろ（NY 3:40〜3:45） | カリフォルニアン号 | 英 Q9053・Q9056 |
| カリフォルニアン号が動き出す | 6:00ごろ（機関は5:15に少し） | カリフォルニアン号 | 英 p.59・Q6713 |
| ボートを全部収容 | 8:00（英の報告）／8:30（船長・米） | カルパチア号 | 英 p.55 |
| カリフォルニアン号がカルパチア号のそばに | 8:30ごろ（船長）／7:45（三等航海士） | カリフォルニアン号 | 米 Lord01・英 Q8352 |
- 🔴 画面は「1:10」の形（ルール B1-3）。**船が違う時刻を1本の時間の線に並べない**（並べるなら船ごとに段を分け「時計が違う」と書く）

---

## 7. 数の表（英国の報告＝頁の画像で確認・`src/look/sd933_tables.png`＝見た2枚目）
| 区分 | 乗っていた | 助かった（%） |
|---|---|---|
| 一等 | 325（男180・女145） | 203（62.46%）＝成人男性57/175・成人女性140/144・男の子5（全員）・女の子1（全員） |
| 二等 | 285（男179・女106） | 118（41.40%）＝成人男性 **14/168（8.33%）**・成人女性80/93・男の子11（全員）・女の子13（全員） |
| 三等 | 706（男510・女196） | 178（25.21%）＝成人男性75/462・成人女性76/165・男の子13/48・女の子14/31 |
| 乗客 計 | 1,316 | 499（37.94%） |
| 乗員 | 885（甲板66・機関325・司厨494〈女性23〉） | 212（23.95%）＝甲板43・機関72・司厨97（女性20を含む） |
| **合計** | **2,201** | **711（32.30%）**＝亡くなった方 **1,490**（p.5） |
| 成人男性／成人女性／子ども | 1,667／425／109 | 338（20.27%）／316（74.35%）／57（52.29%） |
- 内訳の足し算はすべて合計と一致（文字の層の化け「¥」「£0」「1%」「16 out of 425」は頁の画像で 1・80・11・316）
- 米国の数（2,223／706／1,517・三等の男性 476↔486）は**書き起こしだけ**＝公的な写しと未照合（legend §2-2）

---

## 8. 事故のあとの決まり
| 何 | 原文・中身 | 出どころ |
|---|---|---|
| 米国の法（1912-07-23） | 無線の装置は2人以上の技能のある者が扱い、航行中は**どちらかが常に当直** | G4（条文を確認） |
| Radio Act（1912-08-13） | 遭難の通信に優先（①） | G5 |
| 国際氷山監視 | 1913年に巡視船 Seneca と Miami が北大西洋の航路を巡回（"RCS assumed the responsibility of monitoring iceberg activity from the U.S. Navy."）・1914年に SOLAS で正式に（"officially established by the Safety of Life at Sea (SOLAS) Convention"）・"The tragedy led to the creation of the International Ice Patrol." | U1（⚠️ 同じ USCG の記事に「1913年に設けた」と「1914年」の両方・大統領の指示の日も2通り＝画面は「1913年から巡回・1914年の条約で国際の仕組みに」まで） |
| SOLAS 1914 | 1914-01-20 ロンドンで署名・全員分のボートと救命胴衣・氷山監視。戦争で完全には発効しなかった（①＝英国立公文書館・米国の外交文書） | legend §3-3（②では原文を開いていない） |
| 遭難の信号の色 | 1948年から「red」（それまでは何色でもよく、タイタニック号のは白） | MAIB p.18 |

## 9. 残骸（NOAA）
| 何 | 原文 | 出どころ |
|---|---|---|
| 深さ | "3,800 m (12,467 feet)"（2003）／"3,840 meters (12,600 feet)"（2004 の映像の頁）／"12,500 feet"（2004 の写真の説明） | N1（🔴 NOAA の中で3通り＝画面は「約3,800メートル」） |
| 発見 | "Just before midnight on August 31, 1985, the first scattered debris … began to appear" ／ "in the early morning hours of September 1, the unmistakable form of a boiler" | N3（歴史のまとめ＝二次）。NOAA Ocean Exploration の頁は「1985」まで |
| 船首と船尾の距離 | 🔴 **NOAA の読めた頁に数字なし**（"the bow and stern tore apart and sank separately."） | N3。画面に距離を出さない |
| 1912年の位置とのずれ | 約13マイル | MAIB p.2 |

---

## 10. ④への注意（言い方）
1. 🔴 **距離の単位**＝原文の「miles」は航海の慣行で**海里（1.852km）**として換算する（原文に定義は無い＝推定）。5マイル≒9.3km・8〜10≒15〜19km・18≒33km・19½≒36km・58≒107km・13≒24km
2. 🔴 案B は言い切らない（§2-4）。「1912年はこう結論した→1992年に2人の見方が割れた→首席は次長を支持した」の順で、帰属つきで並べる（記憶 `feedback-famous-cause-may-be-legend`）
3. 「Keep out」は英国の報告（p.57）の言い方で出す。米国の証言の「Shut up…」は同じ人の別の言い方として1回だけ並べるか、使わない
4. 火箭の数は報告の「約8発」（p.54・p.60）。証言の「半ダースから1ダース」（四等航海士）は割れる例として使ってよい
5. 時刻は §6 の表の値だけ・どの船の時計か。🔴 係の引き算（約17〜22分）は画面に出さない（証言ではない・MAIB は数分と見る）
6. 二等航海士が言ったとされる「A ship is not going to fire rockets at sea for nothing」は**見習いの証言**で、本人は「言ったかもしれない」（p.58）＝帰属つきで
7. 船長の「全部白か」は見習いと二等航海士の証言（船長本人は「眠っていた」）＝帰属つきで
8. 「1,500人以上」は使わない（英 1,490／米 1,517）
9. 米国上院の報告は書き起こし（§5）＝公的な写しが見つかるまで「書き起こし」と断る
10. 「商務省の調査」と呼ばない（MAIB p.5）
