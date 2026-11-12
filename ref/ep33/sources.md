# 33本目（グレンフェルタワー火災・2017-06-14・英国ロンドン）の事実の確認 ── ②の台帳

**2026-11-12（33本目の2本目のチャット＝②③）で作った。** ①＝Vault `Projects/事故検証-33本目-①芯の確認と数の表-20261112.md`（年表・数の表・説の仕分け・決め11点）／素材＝[materials.md](materials.md)／章立て＝[kousei.md](kousei.md)

> 🔴 **リポは公開**＝住民（亡くなった人・生き残った人・出火した部屋の住人）・消防士・社員・証人・専門家・役人の**個人名を書かない**（立場で書く）。会社・団体・役所の名前は書く（① の決め①＝報告が名指しした結論の範囲）。名前の網＝`v2_build/namecheck33.py`（網は git の外の `src/names_private.txt`・`src/names_commons.txt`）
> 頁＝PDF の頁（しおりの頁・印刷の頁とずれる巻がある）。段落＝¶。**原文の句は親が PDF と保存した頁の文字で照合した**（NFKC・小文字・引用符を揃え・空白とハイフンを消して部分一致）。係の表の句226個＝すべて原文に在る（頁の書き違い23個は段落で引く）
> 報告の略号＝P1ES（第1段階の要約）・P1V1〜4（第1段階 2019-10-30・HC 49）・P2V1〜7（第2段階 2024-09-04・HC 19）

## 0. 先に結論（④で効くこと）
1. 🔴 **「死はすべて避けられた」**＝報告の本文（12冊）には無い（語の当たり0件）。ただし**首相の議会での声明（2024-09-04・gov.uk）が「委員長が今朝こう結論づけた」として引用**＝"the simple truth is that the deaths that occurred were all avoidable" ✓。言葉の主は委員長（公表の日の声明＝調査のサイトは robots で読めない）→ 🆕 **2026-11-12 カズヤくん「帰属つきで使う（推奨）」**＝① の決め⑨を変えた（§6）
2. 報告の言い方は「**戦後の英国で最悪の災害の1つ**」（P2V7 ¶98.1 "one of the worst post-war civil disasters in the UK" ✓）＝「英国史上最悪」は使わない（⑨のまま）
3. **制圧は翌15日**（ロンドン市長の発表・2017-06-15 "Today the fire has been brought under control" ✓）。完全に消えた日時は報告にも公的な発表にも無い＝「60時間燃えた」は使わない（⑨のまま）
4. 🔴 **「部屋で待て」**＝撤回は "by 01.30 at the earliest and by 01.50 at the latest" にすべきだった（P1V4 ¶28.6 ✓）・実際は 02.35 ごろ（指令室）／02.47（現場）・**02.35 以降に逃げたのは46人**（¶28.81 の脚注72 ✓）・02.53〜08.07 に約36人（¶28.81 ✓）
5. **外壁の額は「いつ・誰から誰へ」の額かで食い違う**＝台本は1〜2つに絞る（§4-4）
6. 🔴 **刑事**＝容疑の数は 58人・19団体（2024-05-22）→ 57人・20団体（2026-05-19）→ **54人・20団体（2026-09-30＝すべての書類を検察へ）**。検察は2027年6月（10年）より前に判断の約束＝⑥の頭と公開の直前に当て直す
7. **政府の勧告の実施**＝追っている61件（第2段階58件＋第1段階の残り3件）のうち **2026-02 に12件・2026-09 に30件が済み**（表の "Total 61 49 12"・"Total 61 31 30" ✓）
8. 塔の取り壊し＝2025-02-07 に決定・**2025年9月に始まる**（日は無い）・終わりの見込みは「2027年」→「早くて2027年春」に延びた

## 1. 読んだもの（2026-11-12・保存は `src/`＝git の外）
| 資料 | 発行・日付 | 保存 | 読み方 |
|---|---|---|---|
| 調査の報告（第1段階 要約＋4巻・第2段階 7巻） | 調査・2019-10-30／2024-09-04 | `src/inquiry/`（① で取得・49MB） | しおりで章の地図（§3-5）・語の当たり・係が結論の章を読んだ（§3） |
| 政府の応答（CP 1248） | MHCLG・2025-02-26 | `src/web/govuk/` | 係が全体・親は「残りの9件は原則」の文と番号を照合 |
| 年次報告（CP 1512）／進捗報告（第6回） | MHCLG・2026-02-25／2026-09-10 | `src/web/govuk/` | 表の数を照合 |
| 独立レビュー 中間（Cm 9551）／最終（Cm 9607） | 2017-12-18／2018-05-17 | `src/web/`（PDF） | 決め所の文を照合 |
| 建築安全法 2022（第2条・第31条・第65条・前文） | 議会・2022-04-28 裁可 | `src/web/leg/`（HTML・`data.pdf` は robots で拒否＝取らない） | 照合 |
| 塔の将来の発表／計画の承認の発表／住民向けお知らせ（2025-09） | MHCLG・2025-02-07／計画審査庁 2026-08-25 | `src/web/tower/` | 照合 |
| 警視庁の発表 3本 | 2024-05-22／2026-05-19／2026-09-30 | `src/web/met/`（news.met.police.uk の HTML） | 照合 |
| 首相の議会での声明 | 2024-09-04 | `src/web/avoid/` | 照合 |
| ロンドン市長の発表 | 2017-06-15 | `src/web/lfb/` | 照合（ロンドン消防の2017年の速報3本は 404） |
| 香港 警察の発表／独立委員会の報告 第1巻／政府の発表 | 2026-01-15／2026-10-29 | `src/web/hk/`（第2巻 62MB は取らない＝合計100MB 超の決まり） | 照合 |
| 国交省 審議会の資料（2017-10-06）／建築基準整備促進事業 F11 の報告 | 国交省 | `src/web/jp/`・`src/inquiry/` | 照合 |

## 2. ① の未確認を埋めた（① §11 の番号）
| ① §11 | 結果 | 原文（✓＝照合） | 出典 |
|---|---|---|---|
| 4 鎮火の時刻 | **制圧＝2017-06-15**（市長）。完全に消えた日時は無い。ロンドン消防の当時の速報は 404・検索の抜粋 "under control by 0114" は原本なし＝**使わない** | "Today the fire has been brought under control" ✓ | london.gov.uk の市長の発表（頁に Created on 15 June 2017） |
| 4 亡くなった子どもの数 | 報告の語の当たりで**見つからない**（"of whom were children" はラカナル・ハウスの文だけ）＝報道の数は使わない | — | — |
| 4 "all avoidable" | **委員長の言葉**（首相が議会で引用） | "the simple truth is that the deaths that occurred were all avoidable" ✓・"concluded this morning" ✓ | gov.uk `prime-ministers-statement-on-grenfell-tower-inquiry-final-report-4-september-2024` |
| 5 政府の応答の後半 | 49件を全面・**9件を原則**（係の読み＝勧告1・13・14・25・28・29・30・43・48＝規制者の一本化・建材の適合証明・試験の結果を全部出す・勧告の記録の公開を法で義務・ガスの弁を3年ごとに点検・消防の学校・その学校の職員と施設・ボランティアとの協力・訓練を外から確かめる）。主な期日＝2つ目の階段 "coming into force in 2026" ✓・危ない外壁 "By the end of 2029" ✓・スプリンクラー 30m→11m は実施ずみ | "As regards the remaining 9, which are all directed at government, the government accepts them in principle" ✓（番号は7つを機械で照合・29と48は文の近くに番号が無く未照合） | gov.uk `grenfell-tower-inquiry-phase-2-report-government-response` |
| 5 年次報告（2026-02） | 2026-02-25・CP 1512。61件のうち**12件が済み** | "Total 61 49 12" ✓ | gov.uk `grenfell-tower-inquiry-government-annual-report-february-2026` |
| 5 進捗報告（2026-09） | 2026-09-10・第6回。61件のうち**30件が済み**（さらに9件）・実施は2029年末まで | "Total 61 31 30" ✓・"sixth progress update" ✓・"completed a further 9" ✓ | gov.uk `grenfell-tower-inquiry-government-progress-report-september-2026` |
| 5 独立レビュー | 中間（2017-12）＝規制の仕組みは "not fit for purpose"／最終（2018-05）＝"race to the bottom" | "the current regulatory system for ensuring fire safety in high-rise and complex buildings is not fit for purpose" ✓／"can be described as a 'race to the bottom' caused either through ignorance, indifference, or because the system does not facilitate good practice" ✓ | gov.uk の PDF（中間 p.9・¶1.6／最終 p.5） |
| 5 建築安全法 | 裁可 2022-04-28 ✓・**高リスクの建物＝高さ18m 以上か7階以上で住戸2つ以上**（第65条）✓・規制者は第2条（成立時は安全衛生庁）・⚠️ 2026-01-27 から独立した「建築安全規制者」に書き換え（S.I. 2026/20＝係の読み） | "at least 18 metres in height or has at least 7 storeys" ✓・"contains at least 2 residential units" ✓ | legislation.gov.uk（HTML） |
| 6 国交省の外壁の実験 | 結果＝**国内で一般に使う断熱材と外装材は、ロンドンの火災と比べて極めて危険とは認められない**（F11 の報告 p.24・PDF の作成 2018-04-24＝国交省が載せた日は不明） | 「ロンドン火災との比較において極めて危険という状況は認められない」✓／計画（2017-10-06）「ロンドンの火災に遭った共同住宅の外壁を再現した仕様」✓ | mlit.go.jp `001234641.pdf`・`001205300.pdf` |
| 6 消防庁のグレンフェル後の通知 | 2017年の通知の一覧に関係の題は**無い**（係） | — | fdma.go.jp の通知の一覧（2017） |
| 7 香港 | **死者168人**（警察 2026-01-15）・原因＝たばこと見られる火種が平屋根の紙に（報告 第1巻 ¶491）・広がり＝防炎の網を防炎でない網に替えた疑い（政府 2026-10-29）＝**一言だけ**（決め⑧） | "a total of 168 deceased persons confirmed" ✓・"the fire was most likely caused by a glowing source, likely a cigarette" ✓・"suspected substitution of fire-retardant scaffolding nets with non-fire-retardant ones" ✓ | info.gov.hk・gov.hk（報告 第1巻） |
| 8 取り壊しの始まり | 決定 2025-02-07・**始まり 2025年9月**・終わりは「2027年」→「早くて2027年春」 | "will be carefully taken down to the ground" ✓・"around two years" ✓・"commenced in September 2025" ✓・"We expect work to complete in 2027" ✓・"until at least spring 2027" ✓ | gov.uk の発表・計画審査庁の発表・住民向けお知らせ（2025-09）・年次報告 |
| 8 前の容疑者数 | 2024-05-22＝58人・19団体／2026-05-19＝**57人・20団体**（原文は "people"） | "19 companies or organisations and 58 individuals, as suspects" ✓・"57 people and 20 organisations are suspects" ✓ | news.met.police.uk |
| 9 Commons の動画1本目 | 火災の夜ではない＝ロンドンの空撮と焼けたあとの塔 | — | materials.md §2 |

## 3. 報告の筋（係が結論の章を読み・親が句を照合した要点）
係の表の全文＝`src/suji/suji33.md`（git の外・名前なし）。ここには台本の骨になる所だけ。

### 3-1 燃える外壁は、誰が・なぜ選んだのか（P2V4 55章・67章＝案A）
| いつ | 何が（立場と会社） | ¶ |
|---|---|---|
| 2012 | 外装の第一案は**亜鉛**（区の都市計画の担当官も受け入れ可） | 55.5 |
| 2013-01〜02 | 施工の候補（Leadbitter）がコスト削減として**亜鉛→アルミ**を提案（削減 £250,000 → £300,000） | 55.11 |
| 2013-02 | 設計事務所（Studio E）は、改修を管理した組織（TMO）から亜鉛より安い材料への強い圧力 | 55.12 |
| 2013-09-27 | 設計事務所と外装の施工会社（Harley）の会合＝"the fire safety of the panels was not discussed at all" ✓ | 55.23 |
| 2014-03 | 施工会社（Rydon）が「face-fixed ACM route」で進めたいと伝える・記録の無い会合（03-18） | 55.51・55.54・55.57 |
| 2014-03 | 施工会社は見積りの誤り（"approximately £212,000"）を、TMO に低い削減額を示した差で埋めようとした・TMO は "kept entirely in the dark" ✓ | 55.43・55.59・55.60 |
| 2014-04-01 | TMO への説明は "clearly false and was known by Rydon to be false" ✓ | 55.72 |
| 2014-07-31／09-25 | カセット留めの承認／色（smoke silver）を含む正式な許可（別の段落は「2014年5〜10月」と書く） | 55.77・55.74 |
| 結論 | 関わった全員が見た目に集中し、防火の性能を外していた・BBA の証明書の「Class 0」を誤って信じた・多くの関係者の能力不足と一部の製造会社の "outright dishonesty"・TMO はコスト削減にこだわりすぎたが、**選定の責任は製品の性質を知りうる者が負う** | 55.33・55.14・67.13・67.21 |
| 前ぶれ | 2012-01 の別の建物の火災（Taplow House）で施工会社は ACM が燃えると知りえた・2015-03-27 のメール "the ACM will be gone rather quickly in a fire!" ✓・2014-11-12 に TMO の担当がラカナル・ハウスを引いて照会＝答えなし | 55.79〜80・55.84・55.87〜89 |

### 3-2 製造会社・試験と認証（P2V2 29章＝案A）
- 試験機関（BRE）＝仕事が非専門的で科学的な厳密さを欠いた（¶29.27）・その甘さを突いて断熱材の会社（Celotex）が試験を操作した（¶29.30）・別の断熱材の会社（Kingspan）の2007年の惨憺たる試験の結果をぼかした（¶29.31）
- 認証（BBA）＝外装の板（Reynobond）を、カセット形の試験の証拠なしに「Class 0 の表面とみなせる」と書いた（¶29.42）・断熱材（K15）の証明書は何も評価せずに出した（¶29.43）・製造会社（Arconic）は製品の形の区別を故意にぼかした（¶29.46）
- 認証（LABC）＝顧客に合わせ、証明書に頼る人を犠牲にした（¶29.48）・断熱材の2社は LABC を欺こうとした（¶29.51）
- ① で照合ずみ＝製造3社の "systematic dishonesty"（P2V1 ¶2.19）・試験機関も "complicit"（¶2.29）

### 3-3 国は知っていた（P2V2 29章・P2V1 11章＝案A）
- 1999-12 の議会の特別委員会の警告（死者が出る前に手を打て）は無視（¶29.4〜5）・2001年の ACM PE の試験の結果を公表しなかった（¶29.6）・2016-02 までに高層での ACM PE の常用の懸念を知りながら動かなかった（¶29.9）・**下位の担当の官僚1人の判断に任せた**（¶29.12 "to depend on the judgment of one relatively junior official" ✓）・政府が責任を負う（¶29.21）
- 2016-02-24（中東の高層の火災のあとの照会）への答え＝報告 "The honest response would have been that the risk did exist" ✓（P2V1 ¶11.77）
- ① で照合ずみ＝2013年の検視官の書簡（ラカナル・ハウス）は "not treated with any sense of urgency"（P2V1 ¶2.12）

### 3-4 「部屋で待て」と指揮（P1V4 28章・P2V5 83章＝案C）
- 01.26 ごろ火が最上部へ（¶28.14）→ 撤回は 01.30〜01.50 にすべきだった（¶28.6）→ 02.00 までに全館の避難を始めていれば死者は減った（¶28.63）→ 02.35 ごろ指令室が「とにかく出て」に切り替え（¶28.75）→ 02.47 に現場で撤回＝"the best part of an hour had been lost"（¶28.6 ✓）
- 失敗の中身＝主な失敗は**指揮**（¶28.8）・全館避難に切り替える判断の**訓練が無かった**（¶28.45・28.59）・stay put が "article of faith" だった（¶28.54）・大量の救助の求めの通報（FSG）への**備えが無かった**（¶28.97）
- 隊員＝"enormous courage and selfless devotion to duty"（¶28.1 ✓）・ただし指揮と作戦の欠陥は覆わない（¶28.5）／第2段階＝"their bravery and commitment to duty is only a part (albeit a significant part) of the picture"（P2V5 ¶83.1・p207 ✓）
- 第2段階の結論＝欠陥はラカナル・ハウスの火災（2009-07-03）で予告されていた（¶83.1・83.13）・慢性的な指導力の欠如と慢心の文化（¶83.3）・指令室の再訓練は無かった（¶83.6）・資金不足は原因ではない（¶83.12）

### 3-5 章の地図（しおり・④ で読む所）
| 芯 | 巻・章（PDF の頁） |
|---|---|
| 夜の年表 | P1ES ¶2.11（p8）・P1V2 10〜14章・P1V3 15〜20章（時刻ごとの図あり） |
| 案B 燃え広がり | P1V4 21章（出火）・22章（部屋から外へ p18〜41）・23章（その後の広がり p42〜61） |
| 案C 指揮 | P1V4 27章（準備）・28章（現場 p96〜135）・29章（指令室 p136〜189）／P2V5 69〜83章 |
| 案A 外壁 | P2V4 55章（ACM p113〜136）・56章（断熱材）・62章（建築確認）・67章（結論） |
| 案A 製造と認証 | P2V2 16〜21章（Arconic）・22〜23章（Kingspan）・24〜25章（Celotex）・29章（仕組みの失敗） |
| 案A 国 | P2V1 4〜11章（規則・試験・BRE・ラカナル・ハウス・2013〜2017・警告） |
| その後 | P2V7 98〜107章（対応と復旧）・113章（勧告）・P2V6（亡くなった人の階ごと＝読み方に注意） |

## 4. 数の食い違いと、台本で使う数
| # | 数 | 資料ごとの値 | 台本で使う（推奨・決めるのは ④） |
|---|---|---|---|
| 4-1 | 亡くなった人 | 72（P2・警視庁・政府）＝**塔から逃げられずに70人**（P1V4 ¶32.1 p228 "70 people failed to escape from the building" ✓）＋**死産の1人**＋**7か月後に病院で1人**（P1V1 ¶1.3 は「その夜塔にいた71人＋のちの1人」）／審問は70件（P2V6 ¶84.2）／2017-06-19 の警視庁の推定79（国交省） | **72人**（内訳は1回だけ）。79は使わない |
| 4-2 | 在館と脱出 | 00.54 に **297人**・01.31 までに110人・01.50 までに168人（P1ES ¶2.11）・**脱出は合わせて227人**（住民と訪問者・P1V1 ¶1.3）・02.35 以降に46人（P1V4 脚注72） | 297人・227人・46人 |
| 4-3 | 建物と階 | 高さ "just over 67 metres"・**25層＝地下と地上階〜23階**（P1V1 ¶3.9）・住戸は4〜23階に各6戸（120戸）／国交省＝24階建・68m・出火は「8階（居住フロアの4階）」 | 「**地上24階・地下1階・高さ約67m**」。階は**英国の数え方**（地上階＝0階）で通し、出火は「住戸のある一番下の4階」（日本の数え方への換算は言わない＝国交省の「8階」と食い違う） |
| 4-4 | 外壁の額（P2V4 55章） | 亜鉛→アルミ（2013）＝£250,000（01-18）→ **£300,000**（02-01）（¶55.11）／施工会社への提示（2014-03-14）＝ACM・カセット £419,627・ACM・リベット **£576,973**（¶55.48）／TMO への提示（2014-03-20）＝£293,368・**£376,175**（¶55.58）／見積りの誤り 約£212,000（¶55.43） | 「約30万ポンドの節約」（2013）と、**同じ板の削減額が施工会社には約58万・TMO には約38万ポンドで示された**（2014）の2つまで。円は ④（換算の日と出典つき） |
| 4-5 | 時刻 | 最後の生存者 **08.07**（¶2.11 の表）／08.10（¶2.10）・建物全体を包むまで "under three hours"（¶2.13）・許可 2014-07-31／09-25（¶55.77）と「5〜10月」（¶55.74） | 「朝8時すぎ」・「3時間足らず」 |
| 4-6 | 容疑 | 58人・19団体（2024-05-22）→ 57人・20団体（2026-05-19）→ 54人・20団体（2026-09-30） | 54人・20団体（日付つき）。会社の名は言わない（決め②） |
| 4-7 | 勧告 | 58件（第2段階）＝49件を全面・9件を原則（2025-02-26）／追う表は61件＝済み12（2026-02）→ 30（2026-09）。第2段階の58件だけなら10 → 28（係が各勧告の頁から数えた・親は未照合） | 「58の勧告」「2026年9月の時点で、61件のうち30件が済み」（表の数＝照合ずみ） |
| 4-8 | 香港 | 168人（警察 2026-01-15） | 一言だけ（決め⑧） |
| 4-9 | 建物の規制 | 高リスクの建物＝18m 以上か7階以上・住戸2つ以上（建築安全法 第65条）・スプリンクラー＝新築の 30m 超 → 11m 超（実施ずみ）・2つ目の階段＝18m 超の新築（2026年から） | 日本の入口（終章）で使う |

## 5. 換算（計算）
- 高さと寸法はもともとメートル（67m・床の面積 約22m×22m・各階の高さ 2.6m＝P1V1 ¶3.9・3.15）
- 時刻は英国の夏時間（BST＝日本時間 −8時間）＝00.54 は日本の 08:54。台本は現地の時刻で言う（画面の時刻は「1:25:59」の形＝ルール B1）
- ポンド→円は ④ で決める（換算の日と出典を画面に・2013〜2014年の額を今の円で言うか当時の円で言うかも ④）

## 6. 広く語られる話の当て直し（① §5 の最後の行・語の当たり＝12冊）
| 話 | ① | ② で分かったこと | 推奨 |
|---|---|---|---|
| 「英国史上最悪の住宅火災」 | 報告に無い | 報告の言い方は「**戦後の英国で最悪の災害の1つ**」（P2V7 ¶98.1 ✓） | 使うなら報告の言い方で（⑨ のまま） |
| 「60時間燃えた」 | 報告に無い | 制圧は15日（市長）・消えた日時は公的な資料に無い | 使わない（⑨ のまま） |
| 「死はすべて避けられた」 | 報告に無い | **委員長が公表の日に述べた**（首相が議会で引用＝gov.uk ✓）・報告の本文には無い | 🆕 **帰属つきで使う**（2026-11-12 カズヤくん「推奨どおり」＝⑨ を変えた）＝「調査の委員長は、報告の公表の日に『亡くなった人の死は、すべて避けられた』と述べた（首相の議会での声明が引用）」＝報告の本文の言葉としては言わない |

## 7. 名前の網（`src/names_private.txt`・`src/names_commons.txt`＝git の外）
- `names_private.txt`＝① の13語＋**2,219語**（第1段階 第4巻の付録2〈証人の一覧〉・12冊の敬称と階級の後ろ・第4巻32章から機械で拾った＝名前は画面に出していない。普通の英単語として小文字で2回以上出る語は外した）。① の版は `names_private_c1.txt` に残した
- `names_commons.txt`＝Commons の作者の表示名 33語（`src/commons/cand33.json` の author から）
- ⚠️ 網は字のファイルしか見ない＝写真の中の字（追悼の場の名前）は見本帳で見る（materials.md）

## 8. 未達・残っている粗
- 完全に消えた日時・ロンドン消防の2017年の速報（404）は見つからない＝「60時間」は使わない
- 亡くなった子どもの数は報告の語の当たりで見つからない（報道の数は使わない）
- 委員長の公表の日の声明の原文（調査のサイト＝robots で拒否）は読んでいない＝首相の引用が根拠
- 政府の応答の9件のうち勧告29と48の番号・第2段階の58件だけの済みの数（10 → 28）は係の読み（親は未照合）
- 建築安全法の 2026-01-27 の書き換え（独立した規制者）は係の読み（親は未照合）＝終章で使うなら ④ で原文へ
- 国交省 F11 の報告を国交省が載せた日と頁は見つからない（PDF の作成日 2018-04-24）
- 香港の報告の第2巻（62MB）は取っていない
- 報告の通し読みはしていない＝④ は §3-5 の章を読む。係の表の頁の書き違い23個（隣の頁18・離れた頁5）＝段落で引く
- 🟡 ① の Commons の数え（`cmonth.py`）と Wikidata の分類名（`p373.py`）は **`/w/api.php`＝robots の拒否の内側**を使っていた（② で気づいた＝② からは `/wiki/Category:` と `/wiki/File:` の頁の HTML だけ）

## 9. ④ で足した確認（2026-11-12・チャット3＝④ 台本【書く】）
台本＝[daihon_v1.md](daihon_v1.md)。報告の15冊を頁の印つきの文字にした（`src/inquiry_txt/`＝git の外・`src/tools/c4txt.py`）。台本の出典の欄の原文の片は `v1_build/quotes33.py` が文字に当てる（NFKC・小文字・英数字とかなと漢字のほかを消して部分一致・段落の札が近くにあるかも見る）。
| 項目 | 原文（✓＝照合） | 出典 | 台本 |
|---|---|---|---|
| その夜の住戸と人 | "people in 129 flats in the tower, including visitors" ✓・"Seven flats were empty on that night" ✓・"Sixty-seven of those present were children under the age of 18" ✓ | P1V2 ¶10.130 | c207（⚠️ kousei.md の「120戸」は竣工時＝改修で下の階に9戸が増えた〈P1V1 ¶6.5〉＝台本は129） |
| 出火した部屋の映像 | 住人が近くに知らせて外へ出て、真下から携帯電話で撮った（"From that position he filmed the development of the fire using his mobile telephone" ✓）＝報告の図10.6〜10.9 のコマはこの映像 | P1V2 ¶10.36 | c305（名前なし） |
| 「部屋で待て」の考え方 | "the occupants are advised to remain within their own flats unless they are directly affected by fire, heat or smoke" ✓ | P1V1 ¶4.3 | c108・c317 |
| はしご車 | 報告の結論＝"could reach a maximum height of 32 metres, which meant that they could not reach beyond floor 10 of the tower" ✓（⚠️ ¶12.22 の「10階ほど」は地上で動かした隊員の記憶＝係の指摘で使わない） | P1V4 ¶28.133 | c414 |
| 燃える外装を知らされていない | "the fire brigade had never been informed that a combustible rainscreen system had been installed in the first place" ✓（専門家の補足の報告の引用） | P1V4 ¶28.3 | c416 |
| 72人の内訳 | "70 people failed to escape from the building and lost their lives" ✓・死産の子・"died seven months later" ✓ | P1V4 ¶32.1・P1V1 ¶1.3（⚠️ ¶1.3 の札は文字の層で見えない＝OK(¶?)） | c428 |
| 72人（数そのもの） | "took the lives of 72 people" ✓ | 警視庁 2026-09-30 | c106 |
| 規則に合わない | "As a consequence, the external wall did not comply with functional requirement B4(1)" ✓ | P2V4 ¶63.10 | c902 |
| スプリンクラー | 効き目は "not something that was investigated in Phase 1" ✓＝**¶33.26**（② の「¶2.26」は脚注の番号の読み違い） | P1ES ¶33.26 | c909 |
| 最期 | "all those whose bodies were destroyed by the fire were dead or unconscious when the fire reached them" ✓ | P2V1 ¶2.102 | c908（⚠️ 残すかは承認①） |
| 区の対応 | "muddled, slow, indecisive and piecemeal" ✓・地域の人とボランティア ✓ | P2V1 ¶2.103・¶2.114 | ca01〜ca03 |
| 勧告と政府の応答 | "The Inquiry made 58 recommendations, of which 37 were directed at the government and 21 were directed at other bodies and institutions" ✓・"49 of the recommendations are being accepted in full" ✓・スプリンクラー "lowered from over 30 metres to over 11 metres" ✓・2つ目の階段 "in all new buildings over 18 metres coming into force in 2026" ✓・"By the end of 2029, all buildings over 18 metres with unsafe cladding in a government funded scheme will have been remediated" ✓ | 政府の応答（CP 1248） | ca08・ca11〜ca13 |
| 実施の見込み | "We continue to expect that all recommendations will be implemented by the end of 2029" ✓ | 進捗報告（2026-09） | ca14 |
| 取り壊し | "We expect the work to continue until at least spring 2027" ✓ | 年次報告（2026-02） | ca15 |
| 首相の謝罪 | "an apology on behalf of the British state to each and every one of you" ✓・"It should never have happened" ✓ | 首相の議会での声明 2024-09-04 | ca10 |
| 警視庁 | "Interviewed under caution over 50 suspects for a total of more than 300 hours" ✓・"at least until the end of 2025 to fully assess the public inquiry's phase 2 report and finalise evidential files" ✓（2024）／"The role of 15,000 individuals and 700 organisations have been examined" ✓（2026-05）／"also includes 14 overarching evidence files" ✓・罪名 ✓・"before the 10th anniversary of the fire in June 2027" ✓（2026-09-30） | 警視庁の発表 | cb01〜cb09 |
| 円の換算 | イングランド銀行の月平均 XUMAJYS＝2013年2月 144.0829・2014年3月 170.1186（円／ポンド） | `src/web/boe/xumajys_2013_2014.html`（robots.txt は `/boeapps/database/_iadb-FromShowColumns.asp` などを拒否＝取ったのは許可の `fromshowcolumns.asp` の HTML・公的機関＝許可不要） | c604・c612〜c614 |
| 日本の比べ | 2つ以上の直通階段（居室200㎡超の階・6階以上の階）・スプリンクラー 11階以上（例外あり）・外装材そのものの規制は無く運用の指針・寒い地方の11階以上の共同住宅 279棟のうち外断熱 3棟 ✓ | 国交省 資料6（2017-10-06） | cc02〜cc04 |
- 名前の網の空鳴り（語の一部で鳴る）＝出典の片の英単語の中の5字の並び（5語）と、道具のコードの関数名の中＝片を割って避けた（台本は0件・① の道具 after33.py と namecheck33.py に3件＝コードの語＝直していない）。⚠️ 空鳴りした語を一覧で書くと、その一覧がまた鳴る＝語を並べて書かない

### 9-2. 係の点検（④・Workflow の係4本）で親が原文に当て直したこと
| 所見 | 原文（✓＝親が自分の道具で引いた） | 出典 | 台本の直し |
|---|---|---|---|
| 「お金が足りなかったわけではない」は誰の判断か | 調査の報告は "none of the witnesses from whom we heard told us that insufficient financial or other resources had caused or contributed to the failings" ✓＝「資金の不足ではない」は報告が引いた監察機関の報告の言葉 | P2V5 ¶83.12 | c524 |
| 「明らかに偽り」の条件 | "if, as the minutes tend to suggest, the TMO was given to understand that the sum of £376,175 reflected the full amount of the reduction available from Harley, that was clearly false and was known by Rydon to be false" ✓ | P2V4 ¶55.72 | c615・c616 |
| 板が1つだけになった時 | "From March 2014 onwards … From that time, the only product that was proposed for use was Reynobond 55 PE ACM panels" ✓ | P2V4 ¶55.71 | c617 |
| 扉が壊された目的 | "some doors to flats had to be broken down to enable firefighters to gain entry" ✓ | P1V4 ¶24.36 | c422 |
| 最初の消防車 | "The four appliances arrived within the targets set by the 2017 London Safety Plan" ✓（2台が 00:59・2台が 01:08） | P1V2 ¶10.22 | c306 |
| ドバイの火事のあとの問い | "He asked whether similar panels were used in the UK and whether there was a risk of a similar fire occurring in this country" ✓・役人は前と同じ答え ✓ | P2V1 ¶11.77 | c813 |
| 国の省の状態 | "made it likely that only a major fire in a high-rise building leading to a large number of casualties would prompt it to take the necessary action" ✓ | P2V2 ¶29.21 | c816 |
| 試験の機関の欠け | "from 1991 much of the work it carried out in relation to testing the fire safety of external walls was marred by …" ✓ | P2V1 ¶2.15 | c712 |
| 警視庁の見込み | "at least until the end of 2025" は m3 の2024年5月の発表 ✓・9月の発表（m4）は "at least 12-18 months" ✓ | 警視庁 | cb04 |
| ラカナル・ハウスの段落 | 片は ¶8.1（¶8.2 ではない）・検視官の手紙は "On 28 March 2013" ✓（P2V1 ¶9.41） | P1V1 ¶8.1・P2V1 ¶9.41 | c806 |
| 61の内訳 | 写しで確かめられない（② の係の読み）＝語らない（⚠️ ④' で誤りと分かった＝§9-3） | — | ca14 |

### 9-3. ④'（チャット4・2026-11-12）の係8本の所見で、④' が原文に当て直したこと
台本＝[daihon_v2.md](daihon_v2.md)（差し替え表 `v2_build/patches33.json`・台帳 `v2_build/ledger33.md`）。原文は `v2_build/src33.py` で段落と語の窓を引いた（窓は名前を伏せない＝写さない）。
| 所見 | 原文（✓＝④' が自分の道具で引いた） | 出典 | 第2版 |
|---|---|---|---|
| 住戸の階 | "Floors 4 to 23 were designed to accommodate residential flats, with six flats on each floor" ✓（建てた時の設計）・改修で "nine new flats on these lower floors" ✓ | P1V1 ¶3.13・¶6.5 | c204（主に4〜23階・画の札に改修の9戸） |
| 1:15 の外壁 | "By 01.15.36 the cladding can be seen to be burning with some intensity" ✓（外壁に移ったのは 1:09） | P1V4 ¶22.27 | c311 の副題 |
| 72人の言い方 | "The fire claimed the lives of 71 people who were present in the tower that night" ✓・7か月後の死は "not directly caused by the fire" ✓ | P1V1 ¶1.3 | c106（この災害で） |
| 1:25 の通報 | "At 01.24.57 the control room received the second call from a resident" ✓・"said that there was a fire in her kitchen" ✓（要約の表の 01.30「炎が部屋に入った初めての通報」と合わない） | P1V2 ¶10.90 | c314 |
| 逃げた人 | "A total of 112 people had left the tower in the 35 minutes that followed" ✓（要約の表の「01.31 に110人」と食い違う＝本文に合わせた） | P1V4 ¶28.14j | c316・c427・§1-5 |
| はしご車 | ロンドン消防のはしご車 "could reach a maximum height of 32 metres" ✓・隣の消防の1台 "from a height of 42 metres"・"not used until after the last casualty had been rescued" ✓ | P1V4 ¶28.133・P2V5 ¶82.3 | c414（ロンドン消防のはしご） |
| 専門家の言葉 | 委員長が "bear in mind the following words of"〈専門家〉✓＝"had never been informed" は引用の中 | P1V4 ¶28.3 | c416 |
| 2時までの避難 | "some lives might still have been lost" ✓・"I have little doubt that fewer people would have died" ✓ | P1V4 ¶28.63 | c514（まず間違いなく）・訳の札 |
| 168人の段落 | ¶28.19 の f ✓（¶28.20 ではない） | P1V4 ¶28.19 | c505 の出典 |
| 定期の学び直し | "In 2009, no structured or regular fire survival guidance refresher training was provided" ✓（2010年の学び直し・途切れ途切れの訓練はあった＝¶79.10・¶79.33） | P2V5 ¶83.6 | c524（「定期の」を戻した） |
| お金の不足 | "had caused or contributed to the failings that occurred on the night" ✓ | P2V5 ¶83.12 | c524（あの夜の失敗） |
| 差を残す狙い | 社員2人が "accepted (though not in so many words) that the purpose was to enable Rydon to retain the difference" ✓＝報告の地の結論ではない | P2V4 ¶55.59 | c614（元請けの社員は遠回しに認めた） |
| 板が決まったあと | "The only remaining questions were about colour and whether the fixing system should be cassette or rivet" ✓ | P2V4 ¶55.71 | c617 |
| 設計の側 | "We think that … no one in the design team gave any consideration" ✓（報告の推認） | P2V4 ¶55.89 | c623（とみられる） |
| 防火の技術者 | 外壁の材料の話 "no one asked for advice or confirmation from a fire engineer" ✓ | P2V4 ¶67.14 | c626（材料のこと） |
| 3月18日の夜 | "A meeting took place during the evening of Tuesday 18 March 2014" ✓ | P2V4 ¶55.50 | c611 の出典 |
| アルコニック | "determined to exploit what it saw as weak regulatory regimes" ✓・"That was not an oversight. It reflected a deliberate strategy" ✓ | P2V1 ¶2.23・¶2.25 | c705・c707 |
| キングスパン | "did not use the product currently on the market but used modified or trial versions. It dishonestly relied on the results" ✓ | P2V1 ¶2.37 | c717 |
| 1999年の警告 | "warned the government in unambiguous terms … risks posed by some external cladding systems. Unfortunately, that warning was ignored" ✓ | P2V2 ¶29.5 | c803・cb14（並べ替えのあとの番号） |
| 業界の懸念 | "some in the industry were worried" ✓ | P2V1 ¶2.9 | c810 |
| 規則に合わない | "there is compelling evidence that requirement B4(1) was not met in this case" ✓ | P1V4 ¶26.4 | c902 の出典 |
| 消防の組織 | "a chronic lack of effective management and leadership" ✓ | P2V1 ¶2.91 | c912 |
| 区と政府の1週間 | "In the first week after the fire at Grenfell Tower the response of the government and RBKC was muddled, slow, indecisive and piecemeal" ✓（家を失った人への対応に限らない） | P2V1 ¶2.103 | ca01 |
| 外壁の燃える材料の禁止 | "The use of combustible materials in and on external walls of buildings, including flats, hospitals and student accommodation over 18 metres in height, has been banned" ✓（イングランド） | 応 ¶23 | ca12（すでに禁じられた） |
| 61の内訳 | "all 58 Phase 2 recommendations and the 3 remaining Phase 1 recommendations" ✓（§9-2 の「写しで確かめられない」は誤り） | 進（2026-09-10） | ca14 |
| 何十年の失敗の主 | "culmination of decades of failure by central government and other bodies in positions of responsibility in the construction industry" ✓ | P2V1 ¶2.4 | cc11（国などの） |
| スプリンクラー | "whether such a system would be likely to have suppressed the fire in Flat 16 … is not something that was investigated in Phase 1" ✓ | P1ES ¶33.26 | c909（直さない） |
| 消防の第1段階の勧告 | 年次報告の写し3つと進捗報告に語を変えて25通り＝0件（消防の章の頁は文字の写しが無い） | 年・進 | 語らない（第2版 §5） |
