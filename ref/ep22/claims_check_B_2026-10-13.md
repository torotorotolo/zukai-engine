# 旧版タイタン号の主張照合 係B（第4章〜エピローグ・まとめ）2026-10-13

- 対象：`ref/ep22/src/old/old_script_224e259.md` の第4章・第5章・第6章・エピローグ・まとめと問いかけ（124カット＝c4xx 32・c5xx 38・c6xx 43・ep 11）＋ `tools_cuts_c4.py`／`c5`／`c6`／`ep` の図の値
- 一次資料：USCG MBI 報告（`uscg_mbi_pages.txt`・2025-08-04）／NTSB MIR-25-36（`ntsb_mir2536_pages.txt`・2025-10-02）。TSB の文字は使っていない
- 出典の書き方：USCG は「PDF p.N〈印字 p.X〉」（印字＝PDF−8。要旨の頁はローマ数字）。NTSB は PDF の頁だけ（印字の自動の読みが粗いため）
- 判定：一致／言いすぎ／ずれ／逆／見つからない／一次資料の外。「（軽）」＝直すのは1語程度。「§4」＝2冊で値が割れる（§4 に両方の値）
- ⚠️ 写真の中身は見ていない（文字の層だけ）。写真について書いた所は `old/ref_CREDITS.md` の記述による
- 表の形・判定の言葉は前半（`claims_check_A_2026-10-13.md`）にそろえた

## §1 集計

- 数え方：§3 の1行＝1主張。語り・見出し・図で同じ主張をくり返す所は1行にまとめた。問いだけの文（ep08c の後半）と、事実を含まない受けの文（c416 の後半など）は数えていない。集計は §3 の「判定」の列を機械で数えた値（124カットすべてに1行以上ある）

| 判定 | 件数 | 内訳 |
|---|---|---|
| 一致 | 113 | うち16行は §4 の印つき（片方の報告書とは合うが、もう一方とは値が割れる） |
| 言いすぎ | 31 | うち（軽）22。原文に無い評価・まとめ（§5 (b)）を含む |
| ずれ | 28 | うち（軽）8。名称「海難審判部」4行・写真の取り違えの疑い3行を含む |
| 逆 | 3 | c503（図の札）・c642（図の枕）・ep08b（副題・図） |
| 見つからない | 1 | c538（図の「実際」のヒット数） |
| 一次資料の外 | 0 | — |
| **計** | **176** | 第4章44／第5章53／第6章57／エピローグ・まとめ22。§4 の印つきは全体で25行 |

章ごと：第4章＝一致32・言いすぎ8・ずれ4／第5章＝一致35・言いすぎ10・ずれ6・逆1・見つからない1／第6章＝一致35・言いすぎ8・ずれ13・逆1／エピローグ・まとめ＝一致11・言いすぎ5・ずれ5・逆1

**傾向**
- 第4〜6章の語りはほぼ NTSB の筋どおりで、事実の誤りは少ない。誤りは**図**（2冊に無い深さの線・時刻の山の位置・地図の距離）と**写真の取り違えの疑い**（回収片と切り落とし部、事故の殻と1号殻）に集まる
- 2冊で割れる値（模型1の日付と深さ・窓の認証・警告の線・曳航の距離）は、すべて断りなく NTSB の側だけで言った。逆に事故の深さだけは USCG の 3,346m を使い、NTSB の結論の図（c631）にまで入れた（前半と同じ「混ぜ」）
- 第6章の後半とまとめは、USCG の「主たる要因」と「寄与要因」の区別を崩し（c637a・c639・c640）、締め（ep08b）で原因を会社の外へ移した。2冊の結論の重みと合わない
- 限定語（likely・about・could have・nominally）の落ちが多い（言いすぎ（軽）22行）

**前半の係が見つけた型の、後半での有無**
- 名の誤り「海難審判部」：あり。4か所（c634・c635・c636・ep09 の図の札・注）
- 送った時刻と届いた時刻の取り違え：後半は通信の時刻を扱わないので該当なし。ただし「いつ」の付け違い（c516 の札の日付・c602 と c603 の保管の日付・ep08c の「11か月」）はある
- 2冊で割れる数を断りなしに片方だけ：あり。§4 の新しい16行のうち、旧版が断りを入れていた所は0

## §2 重い順の上位15

1. **ep08b（副題・図）逆／（語り）ずれ** — 「人も、装置も、そろっていた。足りなかったのは外から確かめる仕組みのほう」。NTSB は「殻の状態を見る手段は限られていた」（PDF p.64）・推定原因は会社の技術プロセスと監視データの読み違い（p.74）。USCG は「データを読める人がいなかった」「3個のセンサーが動かないまま＝無謀」（p.290〈282〉・p.282〈274〉）。締めの言葉が2冊と逆向き。
2. **c627（写真）ずれ（要確認）** — 「回収された1層の破片」の写真が、CREDITS では NTSB 図18（左）＝**1号殻**の切り落とし部の剥離（NTSB p.45）。事故の殻の証拠として別の殻を見せている疑い（前半 c3xx でも同じ写真）。c422・c429 も回収片と切り落とし部が入れ替わっている疑い。
3. **c639・c640（語り・副題・図）ずれ（分類）** — 「寄与した要因」として並べた解雇の圧力・不具合を調べない・整備しないは、USCG では**主たる要因8つ**の7・6・8番目（USCG p.7〈vii〉）。c637a も要旨の文で、寄与要因の一覧の項目ではない。原因の重みを1段下げた。
4. **c503（図）逆** — 海底の札「ここまでは何も起きていない」。USCG は80回目に艇がタイタニックの階段に引っかかったと書く（p.233〈225〉・p.309〈301〉）。「浮上している途中」の印も1,600m（2冊とも「海面の近く」）。
5. **c642（図）逆／c641 言いすぎ** — 「別々に調べ、同じ結論へ」。NTSB の調査で USCG は主導機関かつ当事者、NTSB は MBI の聴聞に加わり、USCG の工学分析は NTSB の材料試験に拠る（NTSB p.17 脚注10・p.77）。「NTSB＝材料と設計／USCG＝会社の中」も、USCG の主たる要因の半分が設計・試験・殻の作りで成り立たない。
6. **ep08c（図）ずれ** — 「冬のあいだ屋外に置いたとき　11か月」。屋外は2022-07-26〜2023-02-06の約7か月（USCG p.236〈228〉・p.294〈286〉）。11か月は82回目→88回目。副題「報告書が指摘した、4つの場面」も報告書の言葉ではない。
7. **c606（図）ずれ** — セントジョンズ〜沈没地点の1本の線に「およそ2,900マイル」。2,900は2023年の全航海の合計で、片道は約370海里（USCG p.5〈v〉）。単位も割れる（NTSB "miles" p.60／USCG "NM" p.294〈286〉）。
8. **c629（語り・見出し・図）ずれ** — 「報告書の結論は3つ」。NTSB の所見は10項目（p.73〜74）で、船体の話が1〜3。likely も落ちた。
9. **c510（図）ずれ** — 水深2,200mに「数えるのはここから下だけ」。原文は「海面にいるあいだは数えない」だけ（NTSB p.31）。2冊に無い線。
10. **c405（語り・図）割れる数を片方だけ** — 「製造元は1,000mまでしか認証しなかった」は NTSB（p.30）。USCG は「945 psi＝わずか650m」（p.278〈270〉）。
11. **c408・c410（語り・見出し・図）割れる数を片方だけ／言いすぎ** — 模型1「7月26日・2,800mで爆縮」は NTSB（p.27）。USCG は「7月27日・約3,000m」（p.177〈169〉）。c410「どちらも壊れている」は、NTSB では模型2は壊れる前に止めた（c409 と食い違う）。
12. **c514・c515（図）ずれ** — 音の山を15:16と15:20、ひずみの跳びを15:16と15:18に別々に、聞いた時刻を15:16:30に描く。USCG は15:26:45に音とひずみ（2組）が同時に跳んだ（p.283〜286〈275〜278〉）。前半 pr06 と同じ型。
13. **c604（語り・図）言いすぎ** — 「水が凍れば…材料は傷む」・図「船体のどこかに入り込む」。2冊とも仮定と可能性（NTSB "If ... could have" p.60／USCG "plausible ... potentially" p.294〈286〉）。
14. **「海難審判部」（c634・c635・c636・ep09 の図の札・注）ずれ（名称）** — 前半と同じ。4か所まとめて「海難調査委員会（MBI）」に。
15. **c616〜c618・c631（語り・図）帰属のずれ・言いすぎ** — NTSB の筋の中で USCG の 3,346m を使い、c631 の「NTSB の結論」の図にも 3,346m（NTSB は 3,363m p.58）。c618「この差が意味することは、ひとつしかない」は原文 "indicated"。

次点：c428 図（層の中の気孔を接着面に描く）／c538 図（「実際」のヒット数11〜14は2冊に無い。USCG は83回目に1センサー40件の記録）／c524「自然な描き方」（2冊とも flawed）／c536「データはどこにも無かった」（主語は会社）／ep03 図「9隻はすべて研究・調査」（2隻はロシア海軍）／ep07「残ったのは、これだけ」／c508 中止の線（USCG は黄で中止と証言・文書なし）／c516 札の日付／c522「客を運んだ」（回ごとの記述なし）／c534「壊れている」（NTSB は damaged）

## §3 全件の表

### 第4章 二度目の船体（c401〜c432）

| カット | 種類 | 旧版の主張（短く） | 判定 | 原文の抜き書き（英語25語まで） | 出典 | 直し方の当たり |
|---|---|---|---|---|---|---|
| c401 | 語り・見出し・副題・図 | 2020年、2代目の技術部長のもとで2号殻の設計が始まった | 一致 | "Under a new (second) director of engineering, in 2020, OceanGate embarked on a second stress analysis and testing program" | NTSB PDF p.27 | — |
| c402 | 語り・見出し・図 | 2度目の応力解析の爆縮深度は、およそ7,500m | 一致（NTSB）・§4 | "The second stress analysis predicted an implosion depth for the carbon fiber cylinder of about 7,500 meters" | NTSB PDF p.27／USCG に7,500mは無い（Collier の安全率で書く PDF p.173〈165〉） | 「NTSB によると」を付ける |
| c402 | 語り・見出し | 1回目の13,200mから「半分近くまで下がった」 | 言いすぎ（軽） | "with all results (both v1 and v2 designs) indicating that a carbon fiber composite pressure vessel would have significant safety margin" | NTSB PDF p.25・p.62〜63 | 1号殻と2号殻は別の設計の計算で、「下がった」は同じ物が弱ったように聞こえる。NTSB は2つとも「十分な余裕」と出たと書く。数を並べるだけに |
| c403 | 語り・見出し・副題・図 | 潜れる深さは4,200mに制限。理由は円筒でなく前のチタンドーム | 一致 | "the depth of the Titan was limited to 4,200 meters ... due to the potential for deformation of the titanium forward dome around the viewport" | NTSB PDF p.27・p.30 | 「前の」は「前方の」に（「以前の」とも読める） |
| c404 | 語り・見出し・副題 | のぞき窓のまわりが変形するおそれ | 一致 | "the potential for deformation of the titanium forward dome around the viewport" | NTSB PDF p.27 | — |
| c404 | 図 | 印「変形」を窓そのものに付ける | ずれ（軽） | "deformation of the titanium forward dome around the viewport" | NTSB PDF p.27 | 変形するのは窓のまわりのチタンのドーム。印を窓の縁へ |
| c405 | 語り・見出し・副題 | 窓は標準でない形（中央が厚く縁が薄い）。十分に研究されていない | 一致 | "a non-standard design—it was thick in the middle and thinner toward the edge ... the design had not been studied thoroughly" | NTSB PDF p.30（脚注28） | — |
| c405 | 語り・図 | 製造元は1,000mまでしか認証しなかった | 一致（NTSB）・§4 | "the manufacturer (Hydrospace) would only certify it to 1,000 meters" | NTSB PDF p.30／USCG PDF p.278〈270〉は「945 psi＝わずか650m」 | 2冊で割れる。断りなしに片方を使っている。両方を出すか「NTSB によると」 |
| c406 | 語り・見出し・副題・図 | 1号殻は巻きながら樹脂を含ませた。2号殻は樹脂を含ませた炭素繊維をロールで買った | 一致 | "pre-preg) purchased in rolls instead of using the wet winding method ... as had been done for the v1 cylinder" | NTSB PDF p.27・p.28 | — |
| c407 | 語り・見出し・副題・図 | 幅0.5インチのテープに切り、機械で鋼鉄の芯に巻いた | 一致 | "slit the rolls into 0.5-inch-wide reels (tows) and built the cylinder by winding the tows onto a cylindrical carbon steel mandrel" | NTSB PDF p.27・p.28 | — |
| c408 | 語り・見出し・副題・図 | 2020年7月26日、縮尺模型1はしわが出て2,800mで爆縮 | 一致（NTSB）・§4 | "began testing the sub-scale model on July 26, 2020 ... developed wrinkles ... and imploded at 2,800 meters" | NTSB PDF p.27／USCG PDF p.177〈169〉は「7月27日・約3,000m」 | 日付も深さも2冊で割れる。断りを付ける |
| c409 | 語り・見出し・副題・図 | 8月20日、縮尺模型2は2,500mで「壊れる」と分かり試験を止めた | 一致（NTSB）・§4 | "OceanGate stopped the test at 2,500 meters ... when pressure vessel integrity monitoring data made it clear that the model pressure vessel was going to fail" | NTSB PDF p.27／USCG はこの試験を書かない | — |
| c410 | 語り・見出し・図 | どちらも必要な深さのはるか手前で「壊れている」 | 言いすぎ（軽）・§4 | "either imploded or nearly imploded at depths less than 3,000 meters ... significantly less than the depth needed to reach the Titanic wreckage" | NTSB PDF p.62 | 模型2は壊れる前に止めた（c409 と食い違う）。「1つは爆縮、1つは爆縮の寸前で止めた」。USCG は「2つとも早く爆縮」と書く（§4） |
| c411 | 語り・見出し・図 | 会社は、しわが原因だと判断した（図「しわ＝壊れた原因」） | 言いすぎ（軽） | "OceanGate identified wrinkles in the cylinder as a likely cause of failure." | NTSB PDF p.27・p.62 | likely が落ちた。「原因の可能性が高いと見た」 |
| c411 | 語り・副題・図 | しわを減らす方法としてコボンドを選んだ | 一致 | "decided to use a co-bonding process to construct the cylinder to mitigate the development of wrinkles" | NTSB PDF p.27／USCG PDF p.178〈170〉 | — |
| c412 | 語り・見出し・副題・図 | まず1インチ巻いて、オートクレーブで焼き固める | 一致 | "five co-bonded, nominally 1-inch-thick composite layers ... the assembly was cured in an autoclave" | NTSB PDF p.28 | — |
| c413 | 語り・見出し・副題・図 | 布をはがし、接着フィルムを貼り、また1インチ巻いて焼く | 一致 | "the peel ply was removed and an adhesive film was applied to the cylinder surface. The build ply sequence was then repeated" | NTSB PDF p.28／USCG PDF p.179〈171〉 | — |
| c414 | 語り・見出し・図 | 5回繰り返して厚さ5インチの円筒にした | 言いすぎ（軽） | "the assembly was autoclaved until the cylinder was (nominally) 5 inches thick" | NTSB PDF p.28 | 「設計上5インチ」。実物は5.17インチほどになって削った（c423〜c426） |
| c415 | 語り・見出し・副題・図 | 1層＝133枚。円周方向2枚と長手方向1枚の繰り返し | 一致 | "Each layer consisted of 133 pre-preg plies ... two cylindrical plies followed by one longitudinal ply" | NTSB PDF p.28／USCG PDF p.177〜178〈169〜170〉 | 原文は cylindrical（USCG は「わずかに斜めのらせん」）。「ほぼ円周方向」なら安全 |
| c416 | 語り・見出し・副題・図 | 5つの層のあいだに接着剤の面が4つ | 一致 | "the v2 Titan composite pressure vessel contained four adhesive interfaces" | NTSB PDF p.63 | — |
| c417 | 語り・見出し・副題・図 | 2020年11月〜2021年1月に実物大の2号殻を作った | 一致 | "using the co-bonding process between November 2020 and January 2021" | NTSB PDF p.28／USCG PDF p.180〈172〉 | — |
| c418 | 語り・見出し・図 | 会社はコボンドで縮尺模型を1つも作らなかった（前の作り方は2個） | 一致 | "OceanGate did not build or test any new sub-scale models using the co-bonding process" | NTSB PDF p.62／USCG PDF p.177〈169〉 "None of the one-third scale models were multicured." | — |
| c418 | 語り・副題 | 報告書が「最も強く」指摘した点 | 言いすぎ | — | （2冊とも指摘に順位を付けていない） | 「NTSB はこう指摘した」に |
| c419 | 語り・見出し・副題・図 | この作り方で世の中に存在した物は、人を乗せる実物ただ1つ | 言いすぎ（軽）・§4 | "the only article produced using the co-bonding process was the v2 full-scale cylinder ultimately used in the casualty dive" | NTSB PDF p.62 | 原文は「会社がこの作り方で作った物」。コボンド自体は航空で一般的。USCG には「5インチの試し切り（multicure）」の申し出と輪の断面の写真の話がある（§4 参考） |
| c420 | 語り・見出し・副題・図 | 2021年2〜3月、メリーランドで4,200m相当の水圧試験。通っている | 一致 | "successfully pressure-tested it, demonstrating that it was capable of reaching a depth of 4,200 meters" | NTSB PDF p.30・p.58／USCG PDF p.183〜185〈175〜177〉 | USCG では4,200mは3月1日の1回・20分（ほかは4,000m×2回・3,840m×2回）。施設の地名は前半 §4 と同じ（「メリーランド」なら安全） |
| c421 | 語り・見出し・副題・図 | 必要な深さは3,840m。試験はそれをわずかに上回るだけ | 一致 | "4,200 meters (13,780 feet), marginally greater than the 3,840-meter (12,598-foot) dive depth required to reach the Titanic" | NTSB PDF p.58 | — |
| c422 | 語り・見出し・副題・図 | 事故のあと NTSB が、製造のときに切り落とされた部分を調べた | 一致 | "We also examined end pieces that had been trimmed from the v2 full-scale cylinder during the construction/production process" | NTSB PDF p.42／USCG PDF p.180〈172〉 | — |
| c422 | 語り・図 | 実物の円筒と同じ工程で作られ、同じ釜で焼かれた部分 | 一致（言い換え） | "The cylinder was manufactured with excess material at both ends, which was subsequently trimmed off." | NTSB PDF p.29／USCG PDF p.180〈172〉 | 原文は「実物の円筒の両端の余り」＝実物の一部。「同じ釜」は原文に無い言い換えなので「実物の円筒の端の余り」と言う |
| c422 | 写真 | 切り落とし部の写真（画面の札は「NTSB 図15　切り落とされた部分の側面」） | ずれ（写真・要確認） | "Figure 13. ... Recovered carbon fiber composite pressure hull outer surface and inner surface." | NTSB PDF p.41／ref_CREDITS.md 51行（titan_hull_inner.jpg＝図13（下）） | CREDITS では回収片（事故の破片）の内面。札の図番号と中身が食い違う。④で原寸を見て、図15に替えるか札を直す |
| c423 | 語り・見出し・副題・図 | 1層の想定は0.9975インチ、実測は1.019〜1.033インチ | 一致 | "Instead of 0.9975 inches thick (the expected thickness), the layers were between 1.019 inches and 1.033 inches thick." | NTSB PDF p.43 | — |
| c424 | 語り・見出し・副題・図 | 接着層を足した端部の厚さは5.166と5.175インチ | 一致・§4 | "the two trimmed cylinder ends were 5.166 inches and 5.175 inches thick" | NTSB PDF p.43／USCG PDF p.275〈267〉は「平均約5.16（計算値5.02）」 | — |
| c425 | 語り・見出し・副題・図 | リングの溝には5インチの円筒しか入らない | 一致 | "the annular C-channels on the titanium rings, which could only accommodate a 5-inch-thick cylinder" | NTSB PDF p.43 | — |
| c426 | 語り・見出し・副題・図 | 外側を削って入るようにした | 一致 | "The excess thickness necessitated trimming the outer diameter of the cylinder in order for it to fit" | NTSB PDF p.43 | — |
| c427 | 語り・見出し・図 | 余分な厚みの正体は空隙 | 一致（NTSB）・§4 | "The excess porosity resulted in an increase in layer thickness." | NTSB PDF p.43／USCG PDF p.275〈267〉は「接着剤の過多・空隙・しわが原因の可能性が高い」 | 原因の挙げ方が2冊で違う。NTSB の語は porosity（気孔）で、接着剤の voids（空隙）とは別。訳し分ける |
| c427 | 語り・副題・図 | 円筒全体の空隙率は平均2.7% | 言いすぎ（軽） | "the average porosity content of the composite cylinder was about 2.7%" | NTSB PDF p.43 | 「約2.7%」 |
| c428 | 語り・見出し・副題 | 空隙は散らばらず、薄い炭素繊維のあいだに層をなして集まっていた | 一致 | "the porosity was localized in layers between the composite plies" | NTSB PDF p.43 | — |
| c428 | 図 | 空隙を5つの層のあいだの接着面4つすべてに描く | ずれ（図） | "the porosity was localized in layers between the composite plies" | NTSB PDF p.43 | 語りは各層の中（133枚の薄い繊維のあいだ）の気孔。図は接着面の空隙（c431 の話）を描いている。層の中に細かく描く |
| c429 | 語り・見出し・図 | 切り落とし部にしわとうねり。外側のしわのいくつかは工具で削って平らに | 一致 | "Wrinkles and waviness ... were observed on the trimmed end pieces, and multiple wrinkles ... had been leveled flush ... using a grinding tool" | NTSB PDF p.43／USCG PDF p.179〈171〉 | — |
| c429 | 写真・副題 | 写真は「切り落とされた部分」 | ずれ（写真・要確認） | "Figure 14. From top: Recovered carbon fiber composite cylinder machined end face, and mid-span fractured face." | NTSB PDF p.42／ref_CREDITS.md 50行（titan_hull_edge.jpg＝図14（下）） | CREDITS では回収片（事故の破片）の中央の破断面。切り落とし部ではない疑い。図16（しわの削り跡）などに替える |
| c430 | 語り・見出し・副題・図 | 厚さ方向のせん断強さは6.92〜12.05 ksi で大きくばらつく（図：低い側は57%） | 一致 | "V-notch shear tests in the through-thickness direction showed significant variability, ranging from 6.92 to 12.05 kilopounds per square inch" | NTSB PDF p.43 | 57%は計算（6.92÷12.05）で合う |
| c431 | 語り・見出し・副題・図 | 接着剤の空隙はすべての層のあいだにあったが、1-2と3-4が特に大きく多い | 一致 | "The voids were present in all layers but were significantly greater in size and number at the interface between the first and second layers ..." | NTSB PDF p.43／USCG PDF p.277〈269〉 | — |
| c432 | 語り・図 | 0.6インチと0.4インチの空隙 | 一致 | "two voids, one from the layer 1/2 interface and one from the layer 3/4 interface, measured 0.6 inches and 0.4 inches in length" | NTSB PDF p.43〜44 | — |
| c432 | 語り・見出し | 「長いものでは」「長い空隙が、2か所」 | 言いすぎ（軽） | "For example, two voids ..." | NTSB PDF p.43 | 原文は「例として2つ」。長い空隙は2つに限らない（p.59 は1-2と3-4の面に「長く伸びた空隙」） |
| c432 | 語り | この2つの境目が、のちに剥離する場所になる | 一致 | "One delamination occurred between the first and second layers, and the other delamination occurred between the third and fourth layers." | NTSB PDF p.59 | 3-4の剥離は一部が繊維の中（p.40）。強めるなら「おもに」 |

### 第5章 大きな音（c501〜c538）

| カット | 種類 | 旧版の主張（短く） | 判定 | 原文の抜き書き（英語25語まで） | 出典 | 直し方の当たり |
|---|---|---|---|---|---|---|
| c501 | 語り・見出し・副題・図 | 2021年と2022年の遠征2回で、タイタニックへの到達は合わせて13回 | 一致 | "During the 2021 and 2022 expeditions, the Titan successfully dove to the Titanic wreck site 13 times." | NTSB PDF p.58／USCG PDF p.229〈221〉（2021年6回）・p.235〈227〉（2022年7回） | — |
| c502 | 語り・見出し・副題・図 | 2022年7月14日に79回目、15日に80回目。どちらも3,840m | 一致 | 表5 "79 7/14/2022 3,840 ... 80 7/15/2022 3,840" | NTSB PDF p.35 | — |
| c503 | 語り・見出し・副題 | 問題が起きたのは帰り。タイタニックを見終えて浮上している途中 | 一致（音）・§4 | "heard a 'loud bang' as the Titan ascended after successfully reaching the Titanic wreckage (3,840 meters)" | NTSB PDF p.36／USCG PDF p.233〈225〉 | 主語を「大きな音がしたのは」に。傷んだ時点は前半 §4 と同じ（NTSB は「浮上した後」） |
| c503 | 図 | 「浮上している途中」の印を水深1,600mに置く | ずれ（図）・§4 | "I think we were fairly close to the surface, though still underwater, when there was a large bang" | USCG PDF p.233〈225〉／NTSB PDF p.59 | 前半の pr04 と同じ誤り。2冊とも深さは書かない。海面のすぐ下に置く |
| c503 | 図 | 海底（3,840m）の札「ここまでは何も起きていない」 | 逆 | "As the TITAN descended for a closer view of TITANIC's interior, the TITAN became entangled in the TITANIC's stairwell." | USCG PDF p.233〈225〉・p.309〈301〉 | 80回目は海底で残骸に引っかかっていた（NTSB はこの件を書かない）。札を消す |
| c504 | 語り・見出し・副題・図 | 潜水艇の中の客と、海面の小さなボートの乗組員が、同時に大きな音を聞いた | 一致 | "mission specialists inside the Titan and the crew of a small boat on the surface heard a 'loud bang'" | NTSB PDF p.36／USCG PDF p.233〜234〈225〜226〉 | — |
| c505 | 語り・見出し・副題・図 | 耐圧殻を見張る装置。会社はリアルタイム監視装置と呼んだ | 一致 | "OceanGate called it the 'real-time monitoring (RTM) system.'" | NTSB PDF p.31 | — |
| c506 | 語り・見出し・副題・図 | 音のセンサー8個、円周方向のひずみ計8個、長手方向8個 | 一致 | "eight acoustic emission sensors, eight circumferential (hoop) strain gages, and eight longitudinal (axial) strain gages" | NTSB PDF p.31／USCG PDF p.183〈175〉 | — |
| c507 | 語り・見出し・副題・図 | しきい値を超える音を1ヒットと数える。細かい割れの合図 | 一致 | "if an acoustic event exceeded a predetermined threshold, the event was counted as a 'hit,' indicating that micro-cracking was occurring" | NTSB PDF p.31 | — |
| c508 | 語り・見出し・副題・図 | 1回の潜航で30ヒットなら黄、50なら赤。赤で潜航は中止することになっていた | 一致（NTSB）・§4 | "30 hits during a dive ... yellow display warning. If 50 hits were detected, a red warning was issued, and the dive was to be aborted" | NTSB PDF p.31／USCG PDF p.136〜137〈128〜129〉 | NTSB は「第3代技術部長によると」。USCG は「黄＝30〜50で中止と社員は言うが文書は無く、RTM の警告で中止した潜航は一度も無い」。出どころを付ける |
| c509 | 語り・見出し・副題・図 | ヒットの数は潜航ごとにゼロに戻る | 一致 | "Hit counts did not accumulate between successive dives" | NTSB PDF p.31／USCG PDF p.282〈274〉 | 図のヒット数（22〜27）は模式（§5） |
| c510 | 語り・見出し・副題 | 海面にいるあいだのヒットは数えない | 一致 | "hits while at the surface were not counted" | NTSB PDF p.31 | — |
| c510 | 図 | 水深2,200mに「数えるのはここから下だけ」 | ずれ（図） | "hits while at the surface were not counted" | NTSB PDF p.31 | 2,200mの線は2冊のどちらにも無い。印を海面に置く |
| c511 | 語り・見出し・副題・図 | 装置は潜航中しか動かない。陸に置いているとき・引かれているときは記録なし | 一致 | "the RTM system was only operational during dives, meaning any impacts or damage sustained by the submersible between dives went unrecorded" | NTSB PDF p.31／USCG PDF p.282〈274〉・p.291〈283〉 | — |
| c512 | 語り・見出し・副題・図 | 8個のうち3個は、2022年のすべての潜航で一度も反応していない | 一致・§4 | "Three of the eight acoustic sensors (channels 1, 3, and 5) did not register acoustic events for any of the 2022 dives." | NTSB PDF p.51／USCG PDF p.139〈131〉（75〜83回目）・p.283〈275〉 | 記録が全部残るのは75・76・79〜83回目（NTSB p.51）。「記録の残る2022年の潜航で」が安全 |
| c513 | 語り・副題・図 | 80回目、午後3時15分〜3時30分に装置は変化を捉えた | 言いすぎ（軽）・§4 | "a burst of acoustic activity and a sudden jump in some of the strain gages between about 1515 and 1530" | NTSB PDF p.51〜52 | 「ごろ」を付ける（about）。USCG の時刻は前半 §4 と同じ |
| c514 | 語り・見出し・副題 | 音の活動が急に増えた | 一致 | "showed a burst of acoustic activity" | NTSB PDF p.52／USCG PDF p.283〈275〉 | — |
| c514 | 図 | 音の山を15:16と15:20に描く | ずれ（図）・§4 | "a significant escalation beginning at 3:25:56 p.m. At 3:26:45 p.m., the TITAN's RTM system recorded a major acoustic emission event" | USCG PDF p.283〈275〉 | 前半 §4 と同じ。山は15:26ごろ（増え始めは15:17ごろ） |
| c515 | 語り・見出し・副題 | 同時にいくつかのひずみ計が階段のように跳んだ。人が音を聞いたのと同じ時刻 | 一致 | "These shifts in strain ... occurred in a fraction of a second and coincided with the large amplitude acoustic event on Dive 80 at 3:26:45 p.m." | USCG PDF p.286〈278〉／NTSB PDF p.58 は "about the same time" | — |
| c515 | 図 | 2本のひずみ計が15:16と15:18に別々に跳び、音を聞いた時刻を15:16:30に置く | ずれ（図）・§4 | "At the same time as the RTM system was recording the significant acoustic emissions - 3:26:45 p.m. - the strain readings for Group 4 ... showed abrupt changes" | USCG PDF p.284〈276〉・p.286〈278〉 | 2つの組（4と5）は同じ瞬間（15:26:45）に跳んだ。前半 pr06 と同じ型 |
| c516 | 語り | 社員と客には「船体が金属の受け台の中でずれた」と説明された | 一致 | "staff and mission specialists were told the hull had shifted in its metal cradle" | NTSB PDF p.36／USCG PDF p.233〈225〉 | — |
| c516 | 見出し | 原因は取り付け方だと説明した | 言いすぎ（軽） | "OceanGate subsequently concluded that the 'loud bang' heard during the dive was caused by a shift in the TITAN's position within its frame." | USCG PDF p.233〈225〉 | 原文は「枠（受け台）の中で位置がずれた」まで。「取り付け方」は原文に無い |
| c516 | 図 | 引用の札「2022年7月15日」（説明した日） | ずれ（軽） | "during the debrief for Dive 80, which was held at 9:00 a.m. the following morning after the dive (July 16, 2022)" | USCG PDF p.233〈225〉 | 説明した日は書かれていない（反省会は7月16日、CEO の説明は「その後の反省会」 p.234〈226〉）。日付を外す。副題「浮上したあとの説明」は合う（"after we got on the ship"） |
| c517 | 語り・見出し・副題・図 | CEO はひずみと音のデータを見たあと運航を続けたいと考え、技術部長に言った | 一致（NTSB）・§4 | "The CEO wanted to continue operations and, after inspecting the strain and acoustic emission data, told the director of engineering" | NTSB PDF p.36／USCG PDF p.289〈281〉 | USCG ではデータを見たのは技術部長で、CEO に報告した。割れる |
| c518 | 語り・図 | 「もう一度潜って、どうなるか見よう」 | 一致 | "Let's dive again and see what happens" | NTSB PDF p.36 | USCG にこの言葉は無い。出どころは NTSB |
| c518 | 見出し | 原因を調べずに、また潜った | 一致（USCG） | "OceanGate's failure to conduct any meaningful investigative efforts to determine the actual cause of the unidentified noise" | USCG PDF p.290〈282〉 | 外からの簡単な点検はした（p.289〈281〉）。「十分に調べずに」が安全 |
| c519 | 語り・見出し・副題・図 | 4日後の7月19日、81回目、3,840m | 一致 | "On July 19, 2022, the TITAN and its crew commenced Dive 81 to a depth of 3,840 m" | NTSB PDF p.35／USCG PDF p.235〈227〉 | — |
| c520 | 語り・見出し・副題・図 | 7月22日、82回目、3,840m | 一致 | 表5 "82 7/22/2022 3,840 Exploration" | NTSB PDF p.35 | — |
| c521 | 語り・見出し・副題・図 | 7月23日、83回目、2,954m（別の海域） | 一致・§4 | "dive 83 took place on July 23, 2022, but at a different dive location and to a depth of only 2,954 meters" | NTSB PDF p.51／USCG PDF p.235〈227〉 | NTSB p.60 は「7月25日」＝NTSB の中で割れる |
| c522 | 語り・見出し・副題 | 音のあと3回潜り、そのうち2回はタイタニックの深さへ | 一致 | "The Titan completed three additional dives following dive 80 ... the submersible reached 3,840 meters ... on dives 81 and 82" | NTSB PDF p.36 | — |
| c522 | 語り・見出し・図 | 81・82回目は客を運んだ（図の札「客」） | 言いすぎ（軽） | "OceanGate staff, content managers, and mission specialists embarked on subsequent TITAN dives without OceanGate having a clear understanding of the RTM data" | USCG PDF p.290〈282〉 | 回ごとの乗員は書かれていない。「そのあとの潜航にも客が乗った」まで |
| c523 | 語り・見出し・副題・図 | ここからは事故後の NTSB によるデータの読み直し | 一致 | "after the implosion, the NTSB evaluated the Titan strain data against the vessel's depth" | NTSB PDF p.64 | — |
| c524 | 語り・見出し・副題・図 | 会社はひずみを時刻に対して並べていた | 一致 | "OceanGate analyzed hull strain by plotting it side-by-side with dive depth as a function of time." | NTSB PDF p.51 | — |
| c524 | 語り・図 | 潜航の記録としては自然な描き方 | 言いすぎ（評価） | "OceanGate analyzed data from the strain gages against time. However, analyzing strain data in this way was flawed" | NTSB PDF p.64／USCG PDF p.290〈282〉 | 2冊とも「欠陥のある読み方」と書く。会社寄りの評価は削る |
| c525 | 語り・見出し・副題・図 | この描き方では潜航どうしを比べにくい | 一致 | "it was difficult for OceanGate to compare data between dives" | NTSB PDF p.64 | — |
| c526 | 語り・見出し・副題 | NTSB は深さに対して描き直した。外の圧力は深さで決まるから | 一致 | "evaluate it against depth, since the external pressure acting on the pressure vessel is a direct result of the vessel's depth" | NTSB PDF p.53・p.64 | — |
| c526 | 図 | 第2の横軸「かかる圧力の目安」1〜約385気圧 | 一致（目安） | "The TITAN was tested to a maximum depth of approximately 3,840 m (5,627 psi)" | USCG PDF p.185〈177〉 | 5,627 psi≈383気圧。目安として合う |
| c527 | 語り・見出し・副題・図 | 材料を調べるときに使う図と「同じ形」になる。標準的なやり方 | 言いすぎ（軽） | "This method of analysis is akin to a stress/strain plot, which is a standard method used in evaluating the mechanical properties of materials" | NTSB PDF p.53（脚注37）・p.64 | 「同じ形」→「似た形」（akin／similar） |
| c528 | 語り・見出し・副題・図 | 80回目までは、どの深さでも線はまっすぐ。材料としてふつうの振る舞い | 一致 | "Through dive 80, the strain response of the hull was linear at all depths (a typical mechanical behavior)." | NTSB PDF p.53／USCG PDF p.287〈279〉 | — |
| c529 | 語り・見出し・副題・図 | 81・82・83回目は水深500mより浅い所で線が曲がる | 一致 | "The strain for dives 81, 82, and 83 show non-linear behavior below 500 meters (1,640 feet) depth." | NTSB PDF p.53（図21）／USCG PDF p.288〈280〉 | 図21は円周方向の1組（gage group 4）。USCG は別の組で0〜800m・0〜400mとも書く（p.289〈281〉） |
| c530 | 語り・見出し・副題 | 深い所では、まっすぐのまま | 一致 | "The strain response at greater depths remained linear, similar to previous dives" | NTSB PDF p.59（脚注42） | — |
| c530 | 図 | 浅い所で開いた差が、深い所でも平行に続く | ずれ（軽・図） | "The curves have been aligned using the linear portion of the descent phase of the trip." | NTSB PDF p.53（図21） | NTSB の図は直線の部分で重ねてある＝深い所では線が重なる。差を残さず重ねて描く |
| c531 | 語り・見出し・副題・図 | 全体が弱っていたなら、どの深さでも線は変わる「はず」 | 言いすぎ（軽） | "If the strain response had changed at all depths, it could have indicated the pressure vessel had sustained significant compressive damage" | NTSB PDF p.59 | 原文は「どの深さでも変わっていれば、大きな損傷を示した可能性」。向きと強さを原文に寄せる |
| c532 | 語り・見出し・副題・図 | 浅い所だけ変わる＝層が剥がれた場合に「現れる形だった」 | 言いすぎ（軽） | "This change in strain response is more consistent with a delamination between layers." | NTSB PDF p.59 | 「剥離と考えると、よく説明がつく」 |
| c533 | 語り・見出し・副題・図 | そのひずみ計は円筒の前の端。剥離は前端まで届いていた | 一致 | "The sensor ... was located at the forward end of the composite cylinder, indicating that the damage extended to the forward end of the cylinder." | NTSB PDF p.59 | 原文は damage（損傷）。図の印は前のチタンの継ぎ目から約3.75インチの円筒の上（USCG p.283〈275〉） |
| c534 | 語り・見出し・副題・図 | 装置は3回とも「耐圧殻は壊れている」と言っていた | 言いすぎ（軽） | "the company was unable to identify that the pressure vessel was damaged after dive 80" | NTSB PDF p.65／USCG PDF p.290〈282〉 "clear indicators of a material failure" | NTSB の読み直しの文脈なので「傷んでいる（damaged）」。USCG に帰属させるなら「材料が壊れていた」も可 |
| c535 | 語り・見出し・副題・図 | 赤が出なかったのは、警告の基準が1号殻と縮尺模型の音から決められていたから | 一致（NTSB）・§4 | "The warning levels were based on the acoustic activity of the v1 pressure vessel ... and of the sub-scale pre-preg pressure vessels" | NTSB PDF p.31・p.64 | USCG は「閾値は CEO が決め、根拠を説明できる社員はいない」（p.281〈273〉）。割れる |
| c536 | 語り | 1号殻と模型は作り方が違い、内部の欠陥の種類も違った | 一致 | "manufactured using a different method and produced different acoustic activity due to anomalies in their structures—anomalies that were different" | NTSB PDF p.64〜65 | — |
| c536 | 見出し | 作り方が違えば、壊れ方も違う | 言いすぎ（軽） | "produced different acoustic activity due to anomalies in their structures" | NTSB PDF p.64〜65 | 原文は「出す音が違った」。「壊れ方」は言っていない |
| c536 | 語り・副題・図 | コボンドの耐圧殻がどう壊れていくか、データは「どこにも無かった」（図「どこにも無い」） | 言いすぎ（軽） | "Therefore, they had no data on how a co-bonded structure would deteriorate and fail" | NTSB PDF p.65 | 主語は会社（they）。「会社は持っていなかった」。図は「データが何も無い」に読めるので「壊れ方のデータ」に限る |
| c537 | 語り・見出し・副題・図 | 会社は、弱っていけば昔の試作品と同じような音を出し始めるはずだと考えた | 一致 | "OceanGate assumed that ... it would gradually transition ... to one that produced acoustic events of a similar amplitude and frequency as their previous test articles" | NTSB PDF p.65 | 図のヒット数（12→24→40→56）は模式（§5） |
| c538 | 語り・見出し・副題 | そうはならず、音は拾い続けたが、警告を出す形の音は一度も出なかった | 一致 | "produced activity on the dives that followed dive 80 but never produced the type of acoustic emission signal that would have triggered an alert" | NTSB PDF p.65 | — |
| c538 | 図 | 「実際」のヒット数11〜14。注「実際は黄にも届いていない」 | 見つからない | "there were 40 total acoustic incidents recorded per sensor" | USCG PDF p.235〈227〉（83回目の記録） | 実際のヒット数は2冊に無い。USCG の記録では83回目に1センサーあたり40件（ヒットと同じ量かは不明）。数を消す |

### 第6章 11か月の空白（c601〜c642・c637a）

| カット | 種類 | 旧版の主張（短く） | 判定 | 原文の抜き書き（英語25語まで） | 出典 | 直し方の当たり |
|---|---|---|---|---|---|---|
| c601 | 語り・見出し・副題・図 | 2022年の遠征は7月25日に終わり、潜水艇はセントジョンズに残された | 一致 | "The 2022 expedition began on June 12, 2022, and ended on July 25, 2022" | NTSB PDF p.35〜36／USCG PDF p.235〈227〉 | — |
| c602 | 語り・見出し・図 | 置かれたのは屋外の駐車場。覆いも無し | 一致 | "It was left in a parking lot, outside, uncovered" | NTSB PDF p.36／USCG PDF p.236〈228〉 | — |
| c602 | 副題 | 「2022年7月25日から」 | ずれ（軽）・§4 | "On July 26, 2022, the TITAN, the LARS, and associated equipment were demobilized ... subsequently placed in the parking lot" | USCG PDF p.236〈228〉 | 7月26日から（NTSB は日付を書かない） |
| c603 | 語り・見出し・副題 | 2023年の初めに大学の施設の屋内へ。冬のあいだ外にあった | 一致・§4 | "In early 2023, the submersible was moved to storage at an indoor bay dedicated for ROVs at Memorial University's Marine Institute" | NTSB PDF p.36／USCG PDF p.240〈232〉（2023年2月6日） | 日付を出すなら2月6日（USCG）。NTSB p.60 は「2023年の早春まで」と書き、NTSB の中でも揺れる |
| c603 | 図 | 年表で、屋内へ移った印を「2023年1月」の目盛りに置く・始まりの札「7月25日」 | ずれ（軽・図） | "On February 6, 2023, the TITAN was loaded onto a flatbed and transported to building W1002 at the Marine Institute" | USCG PDF p.240〈232〉 | 2月6日の位置へ。始まりは7月26日 |
| c604 | 語り・副題 | セントジョンズの冬は氷点下になる | 一致 | "The Titan was stored outside after the 2022 expedition until the early spring of 2023, subjecting it to freezing temperatures." | NTSB PDF p.60／USCG PDF p.238〈230〉（最低 1.4°F） | — |
| c604 | 語り・見出し・図 | 水が入り込んで凍れば、膨張で材料は「傷む」（図「船体のどこかに入り込む」） | 言いすぎ・§4 | "If water had penetrated any part of the pressure vessel and frozen, the expansion ... could have caused additional damage." | NTSB PDF p.60／USCG PDF p.294〈286〉 "it is plausible that moisture entered" | 2冊とも仮定と可能性。「傷んだ可能性がある」。図の「入り込む」も「もし入れば」に |
| c605 | 語り・見出し・副題・図 | 2023年は甲板積みから、母船の後ろから引く曳航に変えた | 一致 | "towed on the LARS behind the support vessel instead of on the support vessel as had been done for previous expeditions" | NTSB PDF p.60（p.37 も） | — |
| c606 | 語り・見出し・副題 | 外洋で引かれた距離は合わせておよそ2,900マイル | 一致（NTSB）・§4 | "about 2,900 miles total in open ocean" | NTSB PDF p.60／USCG PDF p.294〈286〉 "more than 2,900 NM" | 単位が割れる（mile／海里）。NTSB は現場までも「370 miles」（USCG は370海里）と書くので、NTSB の miles は海里の意味の可能性。④は「2,900海里を超える（USCG）」か断り付き |
| c606 | 図 | セントジョンズ〜沈没地点の1本の線に「およそ 2,900 マイル」 | ずれ（図） | "was towed approximately 370 nautical miles into international waters to the TITANIC wreck site" | USCG PDF p.5〈v〉 | 2,900は2023年の全航海の曳航の合計。片道は約370海里。線の札を「全航海の合計」にするか地図をやめる |
| c607 | 語り・副題 | 引かれているあいだ、振動と断続的な衝撃を受け続ける | 一致 | "the Titan would have been subjected to vibrations, impulse loads, and upset events" | NTSB PDF p.60 | — |
| c607 | 語り・見出し・図 | 曲げ・せん断・横からの打撃（図「曳かれているあいだに加わる力」） | 言いすぎ（軽） | "which could have caused bending/flexing, shear, and lateral impacts" | NTSB PDF p.60 | 「起こしえた」（could have） |
| c608 | 語り・見出し・副題・図 | 会社は調べていなかった。だから影響の大きさは今も分からない | 一致（NTSB）・§4 | "because OceanGate did not study the effects of vibrations and impulse loads on the Titan, their actual effects are unknown" | NTSB PDF p.60／USCG PDF p.294〜295〈286〜287〉 | USCG は「繰り返しの衝撃で弱った可能性が高い」まで言う。割れる |
| c609 | 語り・見出し・副題・図 | 2023年の遠征は5月12日に始まった。1回目の航海では潜航なし | 一致 | "The 2023 expedition began on May 12, 2023 ... Mission 1 did not include any dives." | NTSB PDF p.37 | — |
| c610 | 語り・見出し・副題・図 | 5月22日、84回目。無人で深さ8m | 一致 | "an unmanned descent to 8 m (Dive 84)" | USCG PDF p.250〈242〉／NTSB PDF p.37 | — |
| c611 | 語り・見出し・副題・図 | 5月31日と6月5日、85回目と86回目。どちらも10m | 一致 | 表6 "85 5/31/2023 10 Test ... 86 6/5/2023 10 Test" | NTSB PDF p.37／USCG PDF p.256〈248〉 | — |
| c612 | 語り・見出し・副題・図 | 6月12日、87回目は装置の不具合で中止 | 一致 | "the dive was aborted due to ballast issues and a malfunction with the LARS" | NTSB PDF p.37／USCG PDF p.261〜262〈253〜254〉 | USCG は、このとき艇が台に約45分打ちつけられ、傷みを深めたとする（p.295〈287〉）。④で触れるか検討 |
| c613 | 語り・見出し・副題・図 | 2023年に潜った深さは、ここまですべて10m以下 | 一致 | "None of the dives exceeded 33 feet (10 meters) depth." | NTSB PDF p.14／USCG PDF p.256〈248〉 | — |
| c614 | 語り・見出し・副題・図 | 最後にタイタニックの深さに達したのは82回目。88回目まで11か月 | 一致 | "the pressure vessel must have sustained additional damage after dive 82 and before the casualty dive 11 months later (dive 88)" | NTSB PDF p.60 | — |
| c615 | 語り・見出し・副題 | 6月18日、88回目。2023年で最初で最後の本格的な潜航 | 一致 | "first dive of the 2023 expedition to descend below 33 feet (10 meters)" | NTSB PDF p.16／USCG PDF p.295〈287〉 | — |
| c615 | 図 | 札「2023年の潜航　84・85・86・88」 | ずれ（軽・図） | 表6 "87 6/12/2023 10 Aborted dive" | NTSB PDF p.37 | 87回目（中止・10m）が抜けている |
| c616 | 語り・見出し・副題・図 | 必要な深さは3,840m、壊れたのは3,346m | 一致（USCG）・§4 | "the weakened carbon fiber pressure hull failed catastrophically while subject to extreme pressures at a depth of 3,346 m (10,978 feet)" | USCG PDF p.295〈287〉／NTSB PDF p.58 は 3,363 m | 前半 §4 と同じ。この章は NTSB の筋（c634「ここまでが NTSB」）なので、3,346m は帰属がずれる。断りを付ける |
| c617 | 語り・見出し・副題・図 | 4,200mの水圧試験に通った殻が、その約80%の深さで壊れた | 一致（計算） | "demonstrating that it was capable of reaching a depth of 4,200 meters" | NTSB PDF p.58 | 3,346÷4,200＝79.7%、3,363÷4,200＝80.1%。どちらでも約80% |
| c618 | 語り・見出し・副題・図 | この差が意味することは「ひとつしかない」＝殻の状態が悪くなっていた | 言いすぎ | "The loss of capability indicated that the condition of the Titan pressure vessel had deteriorated." | NTSB PDF p.58 | 「ひとつしかない」を削る（indicated） |
| c619 | 語り・見出し・副題・図 | 層で作られた材料が圧縮で壊れる道筋は3つ | 一致 | "Three compressive failure modes are possible for laminated composite structures like the Titan pressure vessel" | NTSB PDF p.60 | — |
| c620 | 語り・見出し・副題・図 | 座屈とは形を保てず曲がること。曲がった先で強さを超えれば壊れる | 一致 | "becomes unstable under compressive loads ... If the strength of the material is exceeded in this new shape, the object will fail" | NTSB PDF p.60 | — |
| c621 | 語り・見出し・副題・図 | 剥離は局所座屈の「よく知られた」原因 | 言いすぎ（軽） | "Delaminations are a known cause of local buckling failures." | NTSB PDF p.61 | 「よく」を削る（known） |
| c622 | 語り・見出し・副題・図 | 剥離で厚い1枚が薄い2枚に。薄い板は座屈にはるかに弱い | 一致 | "The delamination divides a single thicker composite layer into two thinner layers ... a significant reduction in resistance to buckling" | NTSB PDF p.61 | — |
| c623 | 語り・見出し・副題・図 | 剥がれた部分が座屈すると縁から皮をむくように離れ、大きな破断になる | 一致 | "it produces a peeling separation at the edge of the delamination. The delamination expands, resulting in large delamination fractures." | NTSB PDF p.61 | — |
| c624 | 語り・見出し・副題・図 | 海底の残骸はこの形と一致。円筒はほぼ全周で層に分かれていた | 一致 | "the carbon fiber composite cylinder had delaminated into multiple layers nearly around the entire circumference" | NTSB PDF p.40・p.61 | 写真（titan_rov_aft.jpg）は CREDITS では「後部ドームと潰れた船体」。円筒の層が写っているかは④で原寸確認（§5） |
| c625 | 語り・見出し・副題・図 | 剥離は1-2層と3-4層のあいだ。切り落とし部で大きな空隙が並んでいた同じ2つの面 | 一致 | "these adhesive interfaces contained long extended voids while the other two adhesive interfaces ... did not" | NTSB PDF p.59 | 3-4は一部が繊維の中（p.40）。「おもにその2つの面」 |
| c626 | 語り・見出し・副題・図 | 残骸の中央で見つかった破片に、S字に曲がった座屈の跡 | 一致 | "On Piece D, which was found in the center of the wreckage ... investigators identified a sigmoidal buckle" | NTSB PDF p.40 | — |
| c627 | 語り・見出し・副題 | 回収された1層の破片の接着剤が擦れて平ら、削れた粉が空隙に溜まる | 一致 | "The adhesive regions were rubbed flat and adhesive wear debris was found collecting in the voids." | NTSB PDF p.44 | — |
| c627 | 写真・副題・札 | 写真は「回収された1層の破片」 | ずれ（写真・要確認） | "Figure 18. From left to right: Centerline delamination in trimmed end piece of first full-scale Titan pressure vessel" | NTSB PDF p.45／ref_CREDITS.md 52行（titan_delam_ruler.jpg＝図18（左）） | CREDITS では事故の殻でなく**1号殻**の切り落とし部の写真。図17（1-2層の空隙）などに替える。前半（c3xx）でも同じ写真を使っている |
| c628 | 語り・見出し・副題・図 | 擦れるには面が前から離れている必要＝剥離は爆縮より前にあった | 一致 | "showed evidence of rubbing and accumulated wear debris in the voids, indicating that the delamination existed before the implosion" | NTSB PDF p.59 | p.44 は "likely failed before the casualty" |
| c629 | 語り・見出し・副題・図 | NTSB の報告書の結論は3つ | ずれ | "3.1 Findings 1. The Titan pressure vessel likely sustained damage ... 10. International standards for pressure vessels" | NTSB PDF p.73〜74 | 所見は10項目。船体の壊れ方が1〜3。「結論のうち、船体についての3つ」 |
| c629 | 語り・図 | 1つ目＝80回目の潜航の直後に剥離という形で傷んだ | 言いすぎ（軽） | "The Titan pressure vessel likely sustained damage after it surfaced at the end of dive 80 in the form of one or more delaminations" | NTSB PDF p.73 | likely が落ちた。「浮上した後に…可能性が高い」 |
| c630 | 語り・見出し・副題・図 | 82回目のあと原因の分からない別の損傷が加わり、タイタニックの深さに耐えられないまで弱った | 一致 | "After dive 82, the Titan sustained additional damage—of unknown origin—that ... weakened the pressure vessel to a point where it could not survive" | NTSB PDF p.73 | — |
| c631 | 語り・見出し・副題 | その状態が局所座屈を引き起こし、爆縮に至った | 言いすぎ（軽） | "likely resulted in a local buckling failure that led to the implosion of the Titan" | NTSB PDF p.73 | likely が落ちた |
| c631 | 図 | NTSB の結論の図に「爆縮　水深3,346メートル」 | ずれ（帰属）・§4 | "the Titan imploded at a depth of 3,363 meters" | NTSB PDF p.58 | NTSB の結論なら3,363m。前半 §4 と同じ |
| c632 | 語り・見出し・副題・図 | 推定原因＝オーシャンゲートの技術プロセスが不十分だった | 一致 | "the probable cause of the hull failure and implosion of the submersible Titan was OceanGate's inadequate engineering process" | NTSB PDF p.74 | — |
| c633 | 語り・見出し・副題・図 | 本当の強さと耐久性を確かめないまま、剥離を負った船を運航し続けた | 一致 | "failed to establish the actual strength and durability ... and resulted in the company operating a carbon fiber composite vessel that sustained delamination damage" | NTSB PDF p.74 | 推定原因の後半（規則と指針の不足・監視データの読み違いも寄与）が落ちている。c641 の言い分に響く |
| c634 | 語り・見出し・副題 | NTSB の報告書はここまで。もう一通、沿岸警備隊の報告書（335ページ） | 一致 | — | USCG PDF 全335頁 | c616〜c618・c631 は USCG の値（3,346m）なので「ここまでが NTSB」は厳密でない |
| c634 | 図 | 札「アメリカ沿岸警備隊　海難審判部の報告書」 | ずれ（名称） | "Marine Board of Investigation" | USCG PDF p.1 | 海難調査委員会（MBI）。前半と同じ誤り |
| c635 | 語り・見出し・副題 | 沿岸警備隊はこの事故を「防ぐことができた悲劇」と呼ぶ | 一致 | "Five people died when the commercial submersible TITAN imploded on June 18, 2023, in what is considered to be a preventable tragedy." | USCG PDF p.5〈v〉 | — |
| c635 | 図 | 引用の札「アメリカ沿岸警備隊　海難審判部」 | ずれ（名称） | "U.S. Coast Guard's Marine Board of Investigation" | USCG PDF p.5〈v〉 | 同上 |
| c636 | 語り・見出し・図 | 主たる原因＝安全・試験・整備について、確立された技術の手順に従わなかった | 一致 | "OceanGate's failure to follow established engineering protocols for safety, testing, and maintenance of their submersible, was the primary causal factor" | USCG PDF p.5〈v〉 | 副題は無し（台本の md の「None」は表記） |
| c636 | 図 | 注「出どころ：アメリカ沿岸警備隊　海難審判部　報告書」 | ずれ（名称） | "Marine Board of Investigation" | USCG PDF p.1 | 同上 |
| c637 | 語り・見出し・副題・図 | 寄与した要因の1つ目＝書かれた安全手順と実際の著しい隔たり | 一致 | "Other contributing causal factors include: 1) ... glaring disparities between their written safety protocols and their actual practices" | USCG PDF p.7〈vii〉 | — |
| c637a | 語り・見出し・図 | 規制の混乱と監督の隙を意図的に作って利用し、確立された深海の手順の外で動かした。その手順は商業用の潜水艇の安全の土台 | 一致 | "By strategically creating and exploiting regulatory confusion and oversight challenges, OceanGate was ultimately able to operate TITAN completely outside of the established deep-sea protocols" | USCG PDF p.5〈v〉 | — |
| c637a | 語り・副題 | これを「寄与した要因」として並べる | ずれ（分類・軽） | "Other contributing causal factors include: ... 4) the lack of comprehensive and effective regulations for the oversight and operation of manned submersibles" | USCG PDF p.5〈v〉・p.8〈viii〉 | 要旨の文で、寄与要因の一覧の項目ではない。一覧の4つ目は「規則の不足」で主語が違う |
| c638 | 語り・見出し・副題・図 | CEO はタイタンを壊れないものとして示し続けた | 一致 | "Chief Executive Officer's sustained efforts to misrepresent TITAN as indestructible due to unconfirmed safety margins" | USCG PDF p.7〈vii〉 | 原文は「偽って（misrepresent）」。旧版は弱めてある |
| c639 | 語り・見出し・副題・図 | 上級社員の解雇と解雇の圧力で、安全上の懸念を口に出させなかった（寄与要因として） | ずれ（分類） | "used firings of senior staff members and the looming threat of being fired to dissuade employees and contractors from expressing safety concerns" | USCG PDF p.7〈vii〉 | USCG では「主たる要因（8つ）」の7番目で、寄与要因ではない。dissuade＝思いとどまらせる（「口に出させなかった」はやや強い） |
| c640 | 語り・見出し・副題・図 | 事故の前の不具合を詳しく調べず、予防の整備をしていなかった（寄与要因として） | ずれ（分類） | "6) OceanGate's failure to conduct a detailed investigations after the TITAN experienced mishaps ... 8) ... failure to conduct preventative maintenance on the TITAN's hull" | USCG PDF p.7〈vii〉 | 主たる要因の6番目と8番目。8番目は「長い休みのあいだの船体の」整備（と風雨からの保護）に限る |
| c641 | 語り・見出し・副題・図 | NTSB は材料と設計から、沿岸警備隊は会社の中で起きていたことから原因を書いた | 言いすぎ（単純化） | "1) OceanGate's design and testing processes for TITAN did not adequately address many of the fundamental engineering principles" | USCG PDF p.7〈vii〉／NTSB PDF p.74 | USCG の主たる要因8つのうち4つ（設計・試験、寿命、監視装置、殻の作り）は材料と設計の話。NTSB の推定原因も会社の技術プロセスと規則を挙げる。分け方は削る |
| c642 | 語り・見出し・副題 | 2つの報告書は違うところを見て、同じ場所に着いた | 言いすぎ（軽） | — | — | c641 と同じ |
| c642 | 図 | 枕「別々に調べ、同じ結論へ」 | 逆 | "The US Coast Guard was the lead federal agency in this investigation." / "The US Coast Guard ... were parties to the investigation." | NTSB PDF p.17（脚注10）・p.77／USCG PDF p.275〈267〉（NTSB の材料試験の報告に拠る） | 2つの調査は証拠・聴聞・材料試験を共有した。「別々に」を削る |

### エピローグ・まとめと問いかけ（ep01〜ep09・ep08a〜c）

| カット | 種類 | 旧版の主張（短く） | 判定 | 原文の抜き書き（英語25語まで） | 出典 | 直し方の当たり |
|---|---|---|---|---|---|---|
| ep01 | 語り・見出し・副題・図 | 2023年の時点で、4,000mより深く潜れる有人潜水艇はタイタンのほかに9隻 | 一致 | "nine known PVHOs, excluding the Titan, could dive to 4,000 meters (13,123 feet), exceeding the depth of the Titanic wreck" | NTSB PDF p.54・p.55（表8） | 出どころは海洋技術学会（MTS）で「知られている9隻」。年は表7に "as of 2023"（表8には年が無い） |
| ep02 | 語り・見出し・副題・図 | 9隻すべてが船級協会の審査か軍の基準のもとで作られ、運用されていた（図「タイタンだけが外にいた」） | 一致 | "All these submersibles were designed and operated under review of a classification society or in accordance with a military standard" | NTSB PDF p.54／p.70（脚注49） | — |
| ep03 | 語り・見出し・副題 | 9隻の中に、料金を取って乗客を乗せるものは1隻も無い | 一致 | "none were passenger-carrying submersibles" | NTSB PDF p.54 | — |
| ep03 | 図 | 「研究・調査のための潜水艇　9隻はすべてこちら」 | ずれ（図） | 表8 "Consul AS-37 Russian Navy Russia 6,000 ... RUS AS-37 Russian Navy Russia 6,000" | NTSB PDF p.55 | 2隻はロシア海軍。原文は「乗客を乗せる艇ではない」まで。札を「乗客を乗せない艇」に |
| ep03 | 図 | 枕「タイタンがしていたことは、他のどこにも無かった」 | 言いすぎ | "From 1994 to 2017, 68% of submersibles produced were 'other,' while 18% were tourist" | NTSB PDF p.55 | 範囲は「4,000m級の9隻の中で」。客を乗せる観光の潜水艇は浅い所に別にある |
| ep04 | 語り・見出し・図 | 乗客を乗せる潜水艇の指針は1993年に作られた | 一致 | "In July 1993, the Coast Guard released Navigation and Vessel Inspection Circular (NVIC) 05-93, 'Guidance for Certification of Passenger Carrying Submersibles.'" | NTSB PDF p.56 | — |
| ep04 | 語り・副題・図 | 同じ1993年に法律が変わり、6人以下を乗せる潜水艇も検査の対象に | 一致 | "the definition of a small passenger vessel changed to include any submersible less than 100 gross tons carrying at least one passenger for hire" | NTSB PDF p.57 | 正確には「料金を払う客を1人でも乗せる100総トン未満の潜水艇」 |
| ep04 | 語り・見出し・図 | 指針はその変更を反映しないまま今日まで残る | 一致 | "The NVIC has not been updated since its release to reflect this change" | NTSB PDF p.69 | 「NTSB の報告（2025年10月）の時点で」 |
| ep06 | 語り・見出し・図 | 報告書は沿岸警備隊に4件の勧告（専門家・規則・指針・国際機関へ義務化の提案） | 一致 | "Commission a panel of experts ... Implement US regulations ... Revise Navigation and Vessel Inspection Circular 05-93 ... Propose that the International Maritime Organization make MSC.1/Circ. 981 mandatory" | NTSB PDF p.75 | 「報告書」は NTSB と明記（USCG の報告書にも別の勧告がある＝8.1 Safety Recommendations PDF p.332〈324〉） |
| ep06 | 語り・図 | 1つ目＝「専門家の会議を開くこと」 | ずれ（軽） | "Commission a panel of experts to study current pressure vessel for human occupancy (PVHO) operations ... and disseminate findings of the study to industry" | NTSB PDF p.75 | 「専門家に調べさせ、結果を業界に広めること」 |
| ep07 | 語り | 2022年7月15日、浮上中の潜水艇の中と海面のボートの上で同じ音が聞こえた | 一致 | "mission specialists inside the Titan and crewmembers aboard a small boat on the surface heard a 'loud bang' as the Titan ascended" | NTSB PDF p.58 | — |
| ep07 | 見出し | 残ったのは、これだけだった（回収した炭素繊維の破片の写真） | 言いすぎ | "retrieving the aft dome and an external camera among the wreckage" | NTSB PDF p.77 | 回収品は後部ドームなども含み、海底に残った物もある（窓は見つかっていない USCG p.281〈273〉）。「回収された破片の一部」 |
| ep08 | 語り・見出し・副題・図 | 聞いた人は1人ではない。装置もそのあと3回同じことを記録し続けた | 一致 | "During dive 81 ... the strain response at low depth was non-linear. The same non-linear response was observed for dives 82 and 83" | NTSB PDF p.53 | — |
| ep08a | 語り・見出し・副題・図 | とつぜん壊れたのではない。壊れる11か月前から船体はそれを伝えていた | 言いすぎ（軽） | "After dive 82, the Titan sustained additional damage—of unknown origin—that further deteriorated and weakened the pressure vessel" | NTSB PDF p.73 | 11か月前に記録に出ていたのは「傷み（剥離）」。最後の弱りは82回目のあとの原因不明の損傷（NTSB）。「傷みを伝えていた」 |
| ep08b | 語り・見出し | 音を聞いた人も、数字を残した装置もあった。足りなかったのは外から確かめる仕組みの「ほう」 | ずれ（原因の置き場所） | "the probable cause ... was OceanGate's inadequate engineering process ... Also contributing was OceanGate's flawed analysis of their pressure vessel monitoring system data" | NTSB PDF p.74／USCG PDF p.5〈v〉 | 2冊とも主因は会社自身（技術の手順・データの読み違い）。外の仕組みの不足は寄与要因の1つ。「のほう」で主因を外へ移さない |
| ep08b | 副題・図 | 「人も、装置も、そろっていた」「事故の前に、材料はそろっていた」 | 逆 | "OceanGate had limited means to monitor the pressure vessel's integrity" | NTSB PDF p.64／USCG PDF p.290〈282〉（データを読める人がいなかった）・p.282〈274〉（3個のセンサーが動かず「無謀」） | 2冊の言うことと逆。この札は削る |
| ep08c | 語り | この11か月のあいだに引き返せる場面はいくつもあった | 一致 | "should have been a red flag to stop all dive operations" | USCG PDF p.290〈282〉／NTSB PDF p.73（所見6 "needed to be immediately removed from service"） | — |
| ep08c | 副題 | 報告書が指摘した、4つの場面 | 言いすぎ（帰属） | — | （2冊とも「4つの場面」とは書かない） | 「4つの場面」は旧版のまとめ。報告書の名で言わない |
| ep08c | 図 | 3つ目「冬のあいだ屋外に置いたとき　11か月」 | ずれ（数） | "placed in the parking lot of the facility for approximately 7 months of storage" | USCG PDF p.236〈228〉 | 屋外は約7か月（2022-07-26〜2023-02-06）。11か月は82回目→88回目の間 |
| ep09 | 語り・見出し・副題・図 | NTSB（2025年10月2日・87頁）と USCG（2025年8月4日・335頁）の報告書にもとづく | 一致 | "Report Date: October 2, 2025" ／ "August 4, 2025" | NTSB PDF p.76／USCG PDF p.5〈v〉 | — |
| ep09 | 図 | 札「アメリカ沿岸警備隊　海難審判部　報告書」 | ずれ（名称） | "Marine Board of Investigation" | USCG PDF p.1 | 海難調査委員会 |
| ep09 | 図 | 注「数値・時刻・引用は、すべてこの2冊による」 | 言いすぎ | — | — | §5 の物（2冊に無い図の数・線）を直すまで言えない。前半の pr10 と同じ |

## §4 2つの報告書で割れる数

前半と重ならない16行（うち参考4＝量が違う・記述が片方だけ・同じ量か不明）。1冊の中でも割れるもの3（警告の線＝USCG、83回目の日付・屋外保管の終わり＝NTSB）。旧版が断りを入れていた所は0

| 項目 | USCG | NTSB | 旧版の扱い |
|---|---|---|---|
| 縮尺模型1の試験 | 2020-07-27、Collier の解析で約3,000mで破壊 PDF p.177〈169〉 | 2020-07-26、2,800mで爆縮 PDF p.27 | NTSB（断りなし）c408・c410 |
| 縮尺模型2の結末 | 2つ目は「作り手不明」（Electroimpact は1つしか作っていないと言う）。試験の記述なし。まとめでは「2つの試作がしわのため早く爆縮」 PDF p.177〜178〈169〜170〉 | 8月20日、2,500mで壊れる前に止めた PDF p.27。「爆縮か、爆縮の寸前」 p.62 | c409 は NTSB、c410「どちらも壊れている」は USCG の言い方（断りなし） |
| 窓の認証 | Hydrospace は 945 psi＝650m で認証。PVHO の正式の認証は取れていない PDF p.278〈270〉 | 1,000m まで PDF p.30（脚注28） | NTSB（断りなし）c405 |
| 2度目の応力解析（参考：量が違う） | Collier の安全率：材料4.6〜8.2（4,500m・1.25倍を足して）、座屈5.6（3,800m）。7,500mの記述なし PDF p.173〈165〉 | 爆縮深度 約7,500m PDF p.27 | NTSB（断りなし）c402 |
| 余分な厚みの原因と端の厚さ | 計算5.02インチ、端の平均約5.16インチ。差は「接着剤の過多・空隙・しわ」が原因の可能性が高い PDF p.275〈267〉 | 端は5.166と5.175インチ。気孔（porosity）が層を厚くした PDF p.43 | NTSB（断りなし）c424・c427 |
| コボンドで作った物（参考：記述が片方だけ） | Electroimpact が「5インチの試し切り（multicure）」を無料で作ると申し出、2020-10-23 に「5インチの輪の断面」の写真が Collier へ送られた PDF p.177〈169〉 | 実物の円筒ただ1つ PDF p.62 | NTSB をさらに「世の中に」と広げた c419 |
| 警告の色と中止の線 | 黄＝30〜50、赤＝50超。社員の証言では黄で中止（文書なし）、RTM の警告で中止した潜航は一度も無い PDF p.136〜137〈128〜129〉。分析の節では赤で中止 p.281〈273〉＝USCG の中で揺れる | 30で黄、50で赤、赤で中止（第3代技術部長の証言） PDF p.31 | NTSB（出どころなし）c508・c535 の図 |
| 警告の基準の出どころ | 閾値は CEO が決め、根拠を説明できる社員はいない。RTM の試験は縮尺模型と、実物大の各殻の DOTF 1回分 PDF p.281〈273〉 | 1号殻の DOTF 試験（亀裂の後）と縮尺模型の音 PDF p.31・p.64 | NTSB c535 |
| 音が出なかった3個のセンサーの範囲（軽） | 75〜83回目 p.139〈131〉（図の注は76〜83回目）、分析では「2022年の遠征の全期間」 p.283〈275〉 | 2022年のどの潜航でも PDF p.51（記録が全部残るのは75・76・79〜83回目） | NTSB c512 |
| 80回目のあとデータを見た人 | 技術部長がデータを見て CEO に報告。CEO は「枠の中でずれた」と結論し、これ以上調べなくてよいと指示 PDF p.289〜290〈281〜282〉 | CEO がデータを見たうえで技術部長に「もう一度潜って…」 PDF p.36 | NTSB c517 |
| 83回目の日付 | 7月23日 PDF p.235〈227〉 | 表5と p.51 は7月23日、p.60 は7月25日＝NTSB の中で割れる | 7月23日（多数側）c521 |
| 屋外保管の期間 | 2022-07-26〜2023-02-06（約7か月） PDF p.236〈228〉・p.240〈232〉・p.294〈286〉 | 「遠征の後」〜「2023年の初め」 p.36、「2023年の早春まで」 p.60＝NTSB の中で揺れる | 「7月25日から」「2023年の初め」（図は1月）c602・c603。ep08c の図は「11か月」 |
| 冬の傷み方（参考：仕組みの挙げ方） | 凍結と融解のくり返しで水分が膨らみ縮み、気孔を広げた可能性（plausible／potentially／likely） PDF p.294〈286〉。熱の変化も p.291〈283〉 | 入った水が凍って膨らめば傷んだ可能性（If ... could have） PDF p.60 | NTSB の仕組みを断定に c604 |
| 曳航の距離 | 2,900 NM（海里）を超える PDF p.294〈286〉。現場まで約370海里 p.5〈v〉 | about 2,900 miles PDF p.60。現場まで 370 miles p.53 | NTSB（マイル・断りなし）c606・c607 |
| 曳航の影響 | 繰り返しの衝撃で弱った可能性が高い（likely）。87回目に台へ約45分打ちつけられたことも挙げる PDF p.294〜295〈286〜287〉 | 会社が調べていないので影響は不明 PDF p.60 | NTSB c608 |
| 音の記録の件数（参考：同じ量か不明） | 83回目の記録に1センサーあたり40件の acoustic incidents、2022年の遠征で120件 PDF p.235〈227〉。2021年は0件 p.229〈221〉 | 警告を出す形の信号は一度も出なかった PDF p.65 | c538 の図「実際は黄にも届いていない」（ヒット数11〜14） |

**前半 §4 と同じもの**（値は前半の表を見る）

| 項目 | 後半で出る所 | 旧版の扱い |
|---|---|---|
| 事故の深さ（3,346m／3,363m） | c616〜c618・c631 の図 | USCG の 3,346m。NTSB の結論を語る場面（c631 の図・c634「ここまでが NTSB」）でも USCG の値 |
| ダイブ80の音の時刻 | c513〜c515 | 語りは NTSB の幅（「ごろ」なし）。図の山と跳びの位置はどちらとも合わない |
| ダイブ80で傷んだ時点 | c503 | 「浮上している途中」。図は1,600m |
| 試験の施設の地名（Annapolis／Bethesda） | c420（2号殻の試験も同じく割れる NTSB p.30／USCG p.183〈175〉） | 「メリーランド」で安全 |

## §5 一次資料の外・見つからないもの（④で裏を取るべき物）

**(a) 一次資料の外・見つからない**

| カット | 中身 | 判定 | ④でやること |
|---|---|---|---|
| c538 | 図「実際」のヒット数11〜14・注「実際は黄にも届いていない」 | 見つからない | 数を消す。USCG の83回目の記録（1センサーあたり40件 p.235〈227〉）がヒットと同じ量かを確かめる |

**(b) 原文に無い解釈・評価（判定は言いすぎ・ずれ・逆。④で削るか言い換える）**

| カット | 中身 | ④でやること |
|---|---|---|
| c418 | 「報告書が最も強く指摘した点」 | 「NTSB はこう指摘した」 |
| c516 | 見出し「原因は取り付け方だと説明した」 | 「受け台（枠）の中でずれたと説明した」 |
| c524 | 「潜航の記録としては、自然な描き方」 | 削る（2冊とも flawed と書く） |
| c618 | 「この差が意味することは、ひとつしかない」 | 削る |
| c641・c642 | 「NTSB＝材料と設計／沿岸警備隊＝会社の中」「別々に調べ、同じ結論へ」 | 削るか「重みの置き方が違う」まで |
| ep03 | 枕「タイタンがしていたことは、他のどこにも無かった」 | 「4,000m級の9隻の中には無かった」 |
| ep07 | 見出し「残ったのは、これだけだった」 | 「回収された破片の一部」 |
| ep08b | 「人も、装置も、そろっていた」「足りなかったのは外の仕組みのほう」 | 締めの言葉ごと書き直す（2冊とも主因は会社自身） |
| ep08c | 副題「報告書が指摘した、4つの場面」 | 旧版のまとめとして言う |
| ep09 | 注「数値・時刻・引用は、すべてこの2冊による」 | (a)(c) を直すまで言えない |

**(c) 図の模式の数・線（値は2冊に無い。画面で実測値に見えないようにする）**

| カット | 中身 | ④でやること |
|---|---|---|
| c503 | 「浮上している途中」の印を1,600mに（判定はずれ） | 海面のすぐ下へ |
| c509 | ヒット数22〜27（潜航1〜4） | 「模式」と明記するか数の目盛りを外す |
| c510 | 2,200mの線「数えるのはここから下だけ」（判定はずれ） | 消す |
| c514・c515 | 音の山（15:16・15:20）、ひずみの跳び（15:16・15:18）、聞いた時刻15:16:30（判定はずれ） | USCG の15:17〜15:26:45 に合わせる |
| c524〜c531 | 時刻の山・深さとひずみの線（c530 は「差が平行に続く」） | 模式と明記。NTSB 図21 は直線の部分で重ねてある |
| c537・c538 | ヒット数12→56（想定）・11〜14（実際） | 実際の数は消す |

**(d) 写真の中身（CREDITS による。④で原寸を見て確かめる）**

| カット | 中身 | ④でやること |
|---|---|---|
| c422 | titan_hull_inner.jpg＝NTSB 図13（下）回収片の内面。画面の札は「図15（切り落とし部の側面）」 | 札か写真のどちらかが誤り |
| c429 | titan_hull_edge.jpg＝NTSB 図14（下）回収片の中央の破断面。副題は「切り落とされた部分」 | 図15・図16に替える |
| c624 | titan_rov_aft.jpg＝後部ドームと潰れた船体。副題「海底に残された円筒部」・札「層に分かれていた範囲　ほぼ全周」 | 円筒の層が写っているか |
| c627 | titan_delam_ruler.jpg＝NTSB 図18（左）1号殻の切り落とし部。副題「回収された1層の破片」 | 事故の殻の写真（図17 など）に替える |
| ep07 | titan_cf_evidence.jpg＝2023年に回収した炭素繊維の破片。札「2022年7月15日」 | 写真の日付に読めないか（回収は2023年） |
