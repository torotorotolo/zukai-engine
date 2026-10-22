# 24本目 ④' 当て直し R2（後半 c805〜cc21・カットの外）

> 第2版（`ref/ep24/daihon_v2.md`）で**直したことで新しく生まれたずれ**だけを見た（第1版から変わっていない行の照合はやり直していない）。所見は `review_R2.json`（R2-001〜R2-022＝🟡7・🟢15）。
> 試し組み＝`fcheck24.py --allfix review_R2.json --tag R2`＝当てた 194・当て損ない 0・句読点なし 13,412字＋ed01 46＝13,458字（patches_g0 の c504・cc13・§1 は入らない）・**E 0 件**。R2 の案の字の差し引き＝+13字（1本あたり最大 +5）。

## 1. 直したカットの全部

| カット | 当てた原文 | 判定 | 一言 |
|---|---|---|---|
| c805 | S3 p.26／22・p.27／23 | OK | 「〜だ、と。」で問い（ソ連は何と説明したの）に答える・帰属が通る |
| c812 | S2 p.18／~13（features which compounded and amplified … and led to the reactivity excursion） | OK | 性質が暴走を招いた＝原文の関係詞のとおり。c103 と同じ形 |
| c813 | S2 p.112／~105 | OK | 3行目を消しても「そう。」は残る・重心は c818 で初めて言う |
| c815 | S2 p.47／~42（no attempt has been made to find alternative explanations） | OK | 1行で足りる |
| c819 | S1 p.11／1（although it was recognized that there were other possible explanations） | OK | 「知りつつ」＝原文の受け身の範囲 |
| c822 | S3 p.28／24（eliminate the possibility of） | OK | 「おそれ」が戻った |
| c902 | S1 p.14／4（A graphite rod termed a 'displaced is attached） | OK | 片は文字の層にある |
| c903 | S1 p.14／4・p.16／6（height 7 m）・図1 | OK | 4.5＋1.25×2＝7 |
| c904 | S1-付属書I p.53／43 | OK | 片は文字の層にある |
| c906 | S1 p.14／4（The magnitude … depended on）・付属書I p.49／39 | OK | 下の方で強まる（局所）は言い切り・全体の逆の働きは「ことがある」＝原文どおり |
| c907 | S1 p.14／4 | ずれ | 反応が c906 の「ことがある」を落とした（R2-007） |
| c908 | S1 p.37／27（INSAG has been informed that … reduced from 18 s to 12 s） | OK | 伝聞の「とされる」 |
| c910 | S1 p.28／18・p.21／11 | OK | 片は文字の層にある |
| c911 | S1-付属書I p.53／43（physical startup） | OK | c105「起動の試験」とそろった |
| c913 | S1 p.23／13（had first been identified at the Ignalina） | OK | 「最初に」が戻った |
| c914 | S1-付属書I p.96／86（The personnel were unaware of some of） | ずれ | 「一部」は合う。personnel を「運転員」（R2-008） |
| c916 | S1 p.25／15（apparently the matter was forgotten） | OK | 反応が断定に戻らない |
| c919 | S1 p.26／16（most likely final event … conditions already prevailing because of the positive power coefficient） | OK | 炉の性質の半分が戻った・「いちばんありそう」 |
| c920 | S1 p.33／23（It is not known for certain） | OK | 2行目を消して c921 の帰属が通る |
| c921 | S1 p.24／14（actual cause） | OK | 「実際の原因」 |
| c922 | S2 p.10／~5（100 times the nominal power within four seconds）・付属書II p.131／121（3.5 times the initial value … approximately 80 times） | OK | 「およそ」は80倍だけ＝語りは合う（§1-5 の行は R2-020） |
| c926 | S1 p.33／23（the concurrence of the following major factors） | ずれ | 聞き役が語りの字をそのままくり返す（R2-009） |
| ca01 | S1-付属書I p.41／31（some of the engineering defects … by the end of May or beginning of June 1986） | OK | 「一部」「か」 |
| ca03 | S1-付属書I p.70／60（not to the actions of the operating personnel） | OK | 問い→「いた。」がそのまま答える・5日後＝4月26日→5月1日 |
| ca04 | S1-付属書I p.70／60（Interdepartmental Science and Technology Council） | OK | 「研究所の所長」と言わない |
| ca05 | S1-付属書I p.70／60（The decisions … paved the way for the one-sided presentation） | OK | 「決定」「一方的な」＝原文どおり（「ウィーンなど」は IAEA・専門家・一般の言い換え＝許す） |
| ca06 | （画の欄だけ） | OK | 人の顔の写らない写真へ |
| ca07 | S1-付属書I p.81／71（the ORM fell to 15 … should be shut down … deliberately … this violation was not die cause） | ずれ | 3行目に主語が無く、職員の違反の全部に広がって聞こえる（R2-006）。§1-5・§5 の「7時ごろ15本は言わない」と食い違う（R2-018・R2-019） |
| ca08 | S1-付属書I p.39／29（disproportionately disastrous consequences） | OK | 「始まりに釣り合わないほど」 |
| ca10 | S1 p.33／23（reactor control elements） | OK | 「止める棒」 |
| ca12 | S1 p.33／23（is even considered by some to have been a precursor） | OK | 伝聞が戻った（§5 の行は R2-016） |
| ca13 | S1 p.34／24（The weight given in INSAG-1 … to the Soviet view … almost entirely） | OK | 「ソ連の見方」・cc18 とそろう |
| ca14 | S1 p.34／24（INSAG remains of the opinion） | OK | 「と見る」で帰属 |
| ca17 | S1 p.21／11（Recent reports suggest） | OK | 「ようだ」（結びの cc16 は R2-003） |
| ca19 | S1 p.21／11（it is likely … during the critical part of the test）・p.34／24（unapproved changes in the test procedure were deliberately made） | ずれ | 「試験の」が落ちて「手順」＝運転の手順に聞こえうる（R2-004） |
| ca20 | S1 p.34／24（operating rules were violated・does not retract INSAG-1） | OK | 聞き役に数の語が無い |
| ca21 | S1 p.34／24（almost entirely） | OK | 「ほとんど」 |
| cb01 | （問いの替え） | OK | 「答えは1つではない」が答える・問いは反応ではない |
| cb03 | S3 p.43／39（among personnel stood at 28） | OK | 「作業員」 |
| cb05 | K1（三十一名） | OK | 「31人」 |
| cb06 | L2 p.5／453 | OK | 呼び名だけ |
| cb08 | S2 p.115／~108（the fatal outcome of the disease in 29 victims） | ずれ | 画の欄に足した29に出典の片が無い（R2-012） |
| cb09 | L2 p.40／488 | OK | 呼び名だけ |
| cb11 | L1 p.13／15（made projections to provide a rough estimate） | OK | 片は文字の層にある・3行目を消しても cb12〜cb14 で通る |
| cb12 | L1 p.14／16（might eventually … up to four thousand … in addition to the approximately 100 000 … due to all other causes） | OK | 「加え」「最終的に」「最大」「かもしれない」 |
| cb13 | L8 p.5（these cancers） | OK | 語りは合う。図の札が cb14 の絞りに合わない（R2-001） |
| cb14 | L3 p.24／64 第98段落（in populations exposed to low radiation doses） | OK | 語りは合う。§1-5 の行が広いまま（R2-002） |
| cb15 | L1 p.13／15（such as the survivors of the atomic bombing in Hiroshima and Nagasaki） | ずれ | 2行目を消して問い「どの推計が正しいの」に答えなくなった（R2-010）。IARC（L8 p.1）は other populations までだが「など」で通る |
| cb16 | S2 p.100／~93 | OK | 薬の行を消しても通る |
| cb17 | L4 p.7／v（The Committee estimated）・p.20／12（0.6 and 0.25） | OK | 帰属が通る |
| cb19 | L2 p.25／473（somewhat lower than the figure of 135,000 that was cited by the Committee） | OK | 「まとめ直している」は原文どおり |
| cb20 | L2 p.5／453（about 240,000 workers … in 1986 and 1987） | OK | 「避難した人とは別に」 |
| cc01 | （問いの替え） | OK | 「違う。」がそのまま答える |
| cc03 | S2 p.11／~6（At the same time, Unit 3 … was shut down・Units 1 and 2 … 27 April）・S3 p.32／28（05.00 on 26 April） | OK | cc04「3号機も」の前提が通る |
| cc06 | L10 p.12／1（seven levels … Below Scale/Level 0） | OK | 「出来事」「0から7の段」 |
| cc11 | WEB 事業者（G0 が確かめた） | OK | 「発電所へ」 |
| cc12 | WEB（G0 が確かめた） | 要確認 | 3月31日が戻した日に聞こえる（R2-021＝親へ・ウェブは見ていない） |
| cc13 | S1-図1 p.15／5・付属書II p.135／125（the manual control rods were replaced） | OK | 片は文字の層にある・「話を棒に戻そう」で橋が通る |
| cc14 | S1 p.35／25・p.33／23（flowed from deficient safety culture） | OK | 問いに答える |
| cc15 | S1 p.21／11・p.22／12 | OK | 2つの時刻に限った |
| cc16 | S1 p.26／16・p.21／11 | ずれ | 1行目が言い切り＝ca17「ようだ」とずれる（R2-003） |
| cc17 | S1 p.34／24（Most reprehensibly … deliberately）・p.26／16 | ずれ | 人の側の「わざと」が落ちた（R2-005） |
| cc18 | S1 p.34／24・S2 p.18／~13 | ずれ | かぎ括弧を外して言い切りになった（R2-011） |
| cc19 | — | OK | 字を返しただけ |
| cc20 | S1 p.33／23・p.34／24 | OK | 「読み比べた答え」 |
| cc21 | — | OK | 語順だけ |

### カットの外

| 所 | 当てた原文 | 判定 | 一言 |
|---|---|---|---|
| §1-1〜§1-3（G0） | S1 p.33／23 | 要確認 | B' の題が棒の欠陥を爆発の原因に読ませうる（R2-022＝承認①） |
| §1-5 ドラムの保護・1:22:30（G0） | S1 p.85／75・p.88／78・S3 p.26／22 | OK | c505・c603 と合う |
| §1-5 出力の倍数（G0） | 付属書II p.131／121 | ずれ | 「およそ」の位置（R2-020＝G0 の足しの上） |
| §1-5 25日の残した棒 | 付属書I p.81／71（1-4.7.1） | ずれ | ca07 と食い違う（R2-018） |
| §1-5 長期の推計（G0） | L1 p.14／16・L3 p.24／64 | ずれ | UNSCEAR 2008 の範囲（R2-002） |
| §1-5 2022年・2025年（G0） | decisions §3 の19 | 要確認 | R2-021 と同じ件 |
| §5 | 付属書I p.81／71・S1 p.33／23 | ずれ | 25日の行（R2-019）・ca12 の行（R2-016）。覆いの大きさ・全員が去った・最大4,000人の「一生」は合う |
| §6 | — | ずれ | UNSCEAR の行（R2-013）・被爆者の行（R2-014）。足した読み（人的要素・私信・事故後検討会議・鉛・1.2メートル・20分の1・0から7の段・ほかの3つの号機）は語りと合う |
| §8 | S3 p.3／-1・S1 p.39／29・p.66／56・p.125／115・L8 p.7・L10 p.12／1 | ずれ | ポジティブ・スクラムの「数秒」（R2-017）。足した4語と INES の段の呼び分けは原文と合う |
| §9 | S2 p.1・p.2・表I-I p.65／55 | ずれ | ca05 の行が残る（R2-015）。c603・cc05・cc11 と足した換算は合う |
| §10 | decisions §3 の19 | OK | URL 9本が書き写されている |
| 章の見出し | — | OK | カットの数（24・27・23・23・21）は第2版の数と合う |

## 2. どちらかに寄せていないか（直しの積み重ね）

- 運転員の責めを弱める向きの直しが2つ：cc17 で「わざと」が落ちた（R2-005）・ca07 の「原因ではなかった」の範囲が職員の違反の全部に広がって聞こえる（R2-006）。逆向きに、cc18 はかぎ括弧を外して1986年の報告を「原因を運転員とした」と言い過ぎる（R2-011）。cc16 の推量の落ち（R2-003）も含め、1か所ずつは小さいが結び（cc16〜cc18）に集まる。
- 設計の側：c919・c926・ca08 の直しは原文の比べ（釣り合わない・すでにあった状態）を戻したもので寄せではない。B' の題（R2-022）は承認①で見る。

## 3. 読んだもの

- `ref/ep24/v2_build/decisions.md`（全部）・`diff_v1_v2.md` 505〜1183行（担当の範囲と前の c717）
- `ref/ep24/daihon_v2.md` 60〜180行（§1・§3）・735〜1412行（第7章〜第11章・§5〜§11）・c103〜c106・c212・c220・c303・c305・c311・c406・c415・c420〜c421・c605 の語り
- `python ref/ep24/v2_build/ledger24.py show --cover c8,c9,ca,cb,cc,§`（131件）・`ledger24.md` の担当の行の扱い
- `pg24.py`（find／re／page）：S1 p.11・14・16・21・23・25・26・28・33・34・37・39・41・49・53・62・66・70・81・96・125・131・135／S2 p.10・11・20・47・115／S3 p.3・32・43／L1 p.5・13・14／L2 p.5・25／L3 p.24／L4 p.7・20／L8 p.1・2・7／L10 p.12・13・26
- `fcheck24.py`・`build24_v2.py`（当て方）
