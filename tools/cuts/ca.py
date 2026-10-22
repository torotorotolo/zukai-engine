# -*- coding: utf-8 -*-
"""第9章　書き直された結論 ca01–ca23（23カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

■ 🆕 2026-10-22（⑤b-1）：新しいファイル。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep24/make_plan24.py` で
  映像方針の一覧 `ref/ep24/eizou_build/list24.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep24/eizou_list24.md`）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  ⚠️ 「関連（参考＝…）」と書いたカットは同じ型のほかの発電所の炉の写真（種類は写真・20% の数〈この発電所・この事故の写真〉には入れない・
     門番 check_text_screens が束の台帳 assets.json の related と照らす）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'ca01': dict(kind='文字の頁',
               plan='S1p41｜一覧の種類：頁｜見せ方：頁｜副題：1991年の委員会の報告（INSAG-7 付属書I）の頁｜動き：寄る（語りの行へ）｜見た目の型：文字の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 付属書I｜注：台本どおり｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.41／31（`some of the engineering defects in the RBMK-1000 reactor design`・`had already been realized by the end of May or beginning of June 1986`）'),
    'ca02': dict(kind='写真',
               plan='🔧 I44｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：毎日届いた新聞を読む作業員｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：🔧 1986年の4号炉-キ → ca06 から空いた点（語り＝IAEA に出した資料・責める行でない）。新聞の字は⑤b で原寸｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.41／31（`They were also not included in the papers presented to the IAEA.`）'),
    'ca03': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：矢印の流れ（研究所→国の指導者）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.70／60（`V.P. Volkov, head of the I.V. Kurchatov Institute Research Group on the Reliability and Safety`・`not to the actions of the operating personnel, but to the design of the reactor`）'),
    'ca04': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：札が1枚に（職員の誤り）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.70／60（`At two meetings of the Interdepartmental Science and Technology Council`・`all the causes of the accident were reduced exclusively to personnel errors`）'),
    'ca05': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：道の矢印（一方的な説明へ）｜注：🔧 IAEA 02790055（ブリクス事務局長）→ 図。「一方的な説明に道を開いた」の行に事務局長の写真を置くと責めに読める。02790055 は ca09 へ｜新しい画（映像方針）：🔧 模式（6月の2回の会議の決定 → ウィーンなどでの一方的な説明＝道の矢印・字は少なく）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.70／60（`paved the way for the one-sided presentation of information`）'),
    'ca06': dict(kind='写真',
               plan='🔧 関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）｜IGB｜一覧の種類：参考｜見せ方：全面｜副題：同じ型の炉のイグナリナ原発（リトアニア・2008年）｜動き：寄る｜権利：CC0｜時期：他所｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC0｜注：🔧 （画の欄＝人の顔の写らない写真）→ ほかの原発の写真（語り＝ほかの原発の職員と比べて）。CC0｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.41／31（`They were no better, but no worse, than the personnel at other nuclear plants.`）'),
    'ca07': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：札（わざと・原因ではない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.81／71（`The Commis-sion assumes that the personnel deliberately violated this requirement.`・`this violation was not die cause of the accident`）'),
    'ca08': dict(kind='写真',
               plan='🔧 T157｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：4号機の排気筒（2010年）｜動き：額ごと上へ｜権利：CC BY-SA 2.0｜時期：今・跡｜人：なし｜出典の行：IAEA Imagebank（CC BY-SA 2.0）・撮影者は作者欄のとおり｜注：🔧 （画の欄＝人の顔の写らない写真）→ 排気筒（人なし）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.39／29（`which was initiated by erroneous actions on the part of the operating personnel`・`had disproportionately disastrous consequences because of deficiencies in the design of the reactor`）'),
    'ca09': dict(kind='写真',
               plan='🔧 I55｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：ブリクス IAEA 事務局長の訪問（1988年5月）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：🔧 イメージ（Pexels）→ ca05 から移した（語り＝国際原子力機関の専門家グループの結論・責める行でない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.33／23（`shift the emphasis to the contributions of parti-cular design features`）'),
    'ca10': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：重なり（3つ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.33／23（`not specified by procedures or investigated by an independent safety body`）'),
    'ca11': dict(kind='写真',
               plan='🔧 関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）｜LENN｜一覧の種類：参考｜見せ方：全面｜副題：同じ型の炉のレニングラード原発の1号機と2号機（2010年）｜動き：右へ｜権利：Public domain｜時期：他所｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／Public domain｜注：🔧 現在の4号炉-セ → 語り「この発電所だけではない」＋次の ca12 が名指しするレニングラード1号機（PD）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.33／23（`not only at the Chernobyl plant, but throughout the Soviet design, operating and`）'),
    'ca12': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：矢印の流れ（1975→1986）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.33／23（`is even considered by some to have been a precursor`・`were not aware of the nature and causes of the accident at Leningrad Unit 1`）'),
    'ca13': dict(kind='写真',
               plan='🔧 C3309｜一覧の種類：実写｜見せ方：全面｜副題：建設中の新しい覆いの骨組みと4号炉（2013年）｜動き：寄る｜権利：CC BY 2.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 2.0｜注：🔧 1986年の4号炉-ク → c304 から移した（人なし＝責める行でも可）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`laid blame almost entirely on actions of the operating staff, is thereby lessened`）'),
    'ca14': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：天秤のもう一方｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`critical actions of the operators were most ill judged`・`the human factor has still to be considered as a major element`）'),
    'ca15': dict(kind='フリー素材',
               plan='X13188717｜映像の素材 17.09秒・倍率 1.58（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のプリピャチ（Pexels）｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：台本どおり（場面で選ぶ＝⑤b でコマを見る）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`does not retract INSAG-1, nor does it alter the conclusions of that report`）'),
    'ca16': dict(kind='図解',
               plan='🔧 一覧の種類：箱｜見た目の型：箱（7つの評価・4色）｜注：§0-5（箱の印）。ca17〜ca19 の語りと突き合わせた｜新しい画（映像方針）：🔧 箱（7つの「違反」の1992年の評価＝違反ではない〈②承認があれば許された・④禁止なし・⑥手順どおり〉／誤りとは言えないようだ〈③＝「ようだ」の留保を札に残す〉／形の上の違反〈⑤〉／違反〈⑦残した棒・①その場で承認なく計画を変えた〉＝4色・字は少なく・この1枚だけ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.20〜22／10〜12（`blocking of the ECCS was in fact permissible at Chernobyl if authorized`）'),
    'ca17': dict(kind='写真',
               plan='🔧 C488｜一覧の種類：実写｜見せ方：全面｜副題：森の向こうの4号炉と排気筒（2006年）｜動き：左へ｜権利：CC BY 2.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 2.0｜注：🔧 1986年の4号炉-ケ → c313 から移した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`no operator error as such`）'),
    'ca18': dict(kind='写真',
               plan='C496｜一覧の種類：実写｜見せ方：全面｜副題：吹雪の中の石棺（2016年）｜動き：寄る｜権利：CC BY 2.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 2.0｜注：台本＝現在の4号炉-ソ → c501 から移した（CC BY）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.22／12（`protection at the lower steam drum level remained effective throughout the event`）'),
    'ca19': dict(kind='写真',
               plan='🔧 C1｜一覧の種類：実写｜見せ方：全面｜副題：石棺の鉄骨（2008年）｜動き：上へ｜権利：CC BY 3.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 3.0｜注：🔧 イメージ（Pexels）→ 石棺の寄り（CC BY 3.0）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`it is likely that the operator did not know the value of the ORM`・`during the critical part of the test`）・S1 p.34／24（`Most reprehensibly, unapproved changes in the test procedure were deliberately made`）'),
    'ca20': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：2つの札に×（無実でもうそでもない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`operating rules were violated`・`does not retract INSAG-1`）'),
    'ca21': dict(kind='写真',
               plan='H06｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：新しい覆いと送電線（2018年）｜動き：額ごと右へ｜権利：CC BY-SA 4.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：台本＝現在の4号炉-タ｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.26／16（`It is reprehensible that such a deficiency had been known of for so long`）'),
    'ca22': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：2つの矢印（設計と運転）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書II p.120／110（`reactor instability caused both by design faults and the operating regime`）'),
    'ca23': dict(kind='写真',
               plan='🔧 T138｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：冷却水路に映る4号機と排気筒（2010年）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：今・跡｜人：なし｜出典の行：IAEA Imagebank（CC BY-SA 2.0）・撮影者は作者欄のとおり｜注：🔧 c27（森のバス）→ 冷却水路の4号機。c27 は cb19 へ → 第10章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}
