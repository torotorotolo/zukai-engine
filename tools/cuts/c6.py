# -*- coding: utf-8 -*-
"""第5章　1時23分 c601–c621（21カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

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
    'c601': dict(kind='写真',
               plan='🔧 CR4｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：4号機の制御室（2021年）｜動き：額ごと右へ｜権利：CC BY-SA 4.0｜時期：今・中｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：🔧 CC0 の2025年の写真（学生が真ん中に立つ＝運転員に見える）→ 4号機の制御室（人なし）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.21／17（`At 1:22:30, the operator saw from a printout of the fast reactivity evaluation program`）'),
    'c602': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：印字の紙（即時停止の印）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.21／17（`the available excess reactivity had reached a level requiring immediate shutdown of the reactor`）・S3 p.21／17（`Nevertheless, the staff were not stopped by this and began with the experiments.`）'),
    'c603': dict(kind='図解',
               plan='🔧 一覧の種類：比べ｜見た目の型：比べ（残した棒の数）｜注：§0-5｜新しい画（映像方針）：🔧 比べ（残した棒の数＝決まり15本ですぐ止める／1986年のソ連の報告 6〜8本＝「15本のおよそ半分」の札・事故のあとの計算の8本の札は外す＝出典の欄だけ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.23／19（`At 1:22:30 the excess reactivity was only 6-8 rods`）・S1-表I-I p.64／54（`ORM proved to be equal to 8 manual control rods`）'),
    'c604': dict(kind='図・写真の頁',
               plan='🔧 S1p129｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告の図（1時22分30秒の、制御棒の差し込みの深さ）｜動き：寄る（炉心の図へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 付属書II の図 II-6｜注：🔧 現在の4号炉-ク → 語り「棒の大部分を抜いた」の物証＝01:22:30 の再現（頁の本文に時刻）｜新しい画（映像方針）：🔧 頁（INSAG-7 付属書II p.129／119 の図 II-6＝炉心の平面に棒の深さ〈cm〉・ほとんどが0）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.10／~5（`the operators deliberately and in violation of rules withdrew most control and safety rods`）'),
    'c605': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：重さの札（小と大）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.22／12（`the ORM is much greater than was indicated in the INSAG-1 report`）'),
    'c606': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：計算機の画面（？）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`it is likely that the operator did not know the value of the ORM`・`the computer SKALA, which was used to calculate the ORM, became unreliable`・`Probably he was aware that continued operation`）・S1 p.16／6（`This data system required about 10-15 min`）'),
    'c607': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：2つの言い方（左右）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.74／64（`did not know the calculated parameters, including the ORM, at this time`）'),
    'c608': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：頭の中の札（分布のため／安全のため）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`were not aware that it had safety significance`）'),
    'c609': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：時計の札（1:23:04 試験の始まり）｜注：🔧 現在の4号炉-ケ → 図｜新しい画（映像方針）：🔧 模式（1時23分4秒＝試験の始まりの札・8号タービンへの蒸気が止まる前の時刻）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'c610': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：機械（8号タービン・弁）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.21／17（`At 1:23:04, the emergency regulating valves of turbogenerator No. 8 shut.`）'),
    'c611': dict(kind='図・写真の頁',
               plan='🔧 GCp43｜一覧の種類：頁｜見せ方：頁｜副題：1986年の報告の図（出力などの記録の線・ソ連の資料から）｜動き：寄る（出力の線へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：GC(SPL.I)/3＝INSAG-1 の図1｜注：🔧 模式（出力の線がゆっくり上がる）→ 1986年の報告の図そのもの（語り＝1986年のソ連の報告の言い方）。図の頁＝文字だけに数えない｜新しい画（映像方針）：🔧 頁（INSAG-1 の図1＝出力・反応度・圧力の線・カラーのスキャン）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.21／17（`Shortly after the beginning of the experiment the reactor power began to rise slowly.`）'),
    'c612': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：線（流れが下がる・出力は平ら）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.75／65（`During the rundown of turbogenerator No. 8 there was no increase in reactor power.`・`Thirty-five seconds after the start of the transient it had fallen by 10-15%`）'),
    'c613': dict(kind='写真',
               plan='🔧 AZ5｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：AZ-5 のボタンのある制御盤（3号機・2019年）｜動き：額ごと寄る｜権利：CC BY-SA 4.0｜時期：今・中｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：🔧 現在の4号炉-コ → 語りが「AZ-5 のボタン」と名指し。白衣の腕だけ（顔なし）。3号機の盤＝4号機と名乗らない｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.24／20（`this was the circumstance which triggered the pressing of button AZ-5`）・S3 p.21／17（`the unit shift foreman gave the order to press button AZ-5`）'),
    'c614': dict(kind='図解',
               plan='一覧の種類：時計｜見た目の型：時計（1:23:40）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.76／66（`The Commission was unable to establish why the button was pressed.`）'),
    'c615': dict(kind='再現イラスト',
               plan='一覧の種類：案C2｜見る向き：横から｜見た目の型：棒の立体（前触れ・案C2）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.21／17（`The rods fell, but after a few seconds a number of shocks were felt`）'),
    'c616': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：針の計器（530MW を超える）｜注：🔧 頁 p.65 → 図。表の頁は c619（語りが日誌の1行を引く）へ＝同じ頁を2回出さない｜新しい画（映像方針）：🔧 模式（1時23分43秒＝出力が急に上がった信号・針が530MWを超える）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-表I-I p.65／55（`power exceeded 530 MW(th)`）'),
    'c617': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：棒の立体（途中で止まる）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-表I-I p.65／55（`the RCPS rods stopped moving before they reached the lower limit stop switches`）・S3 p.21／17（`He then cut off the current to the sleeves of the servo drives`）'),
    'c618': dict(kind='写真',
               plan='🔧 MX7｜一覧の種類：実写｜見せ方：全面｜副題：壊れた4号炉の模型（チェルノブイリの展示・2006年）｜動き：寄る（ずれた炉のふたへ）｜権利：CC BY 2.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 2.0｜注：🔧 1986年の4号炉-ア → 爆発のあとの4号炉の模型（CC BY 2.0＝全面で寄る）。1986年の壊れた炉の写真は IAEA の4点しかない（冒頭と石棺で使う）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.21／17（`burning lumps of material and sparks shot into the air above the reactor`）'),
    'c619': dict(kind='文字の頁',
               plan='🔧 S1p65｜一覧の種類：頁｜見せ方：頁｜副題：1991年の委員会の表（INSAG-7 付属書I の表I-I）｜動き：寄る（「01:24 激しい衝撃」の行へ）｜見た目の型：文字の頁（表）｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 付属書I 表I-I｜注：🔧 1986年の4号炉-イ → 語りが引く日誌の1行そのもの｜新しい画（映像方針）：🔧 頁（表I-I p.65／55＝1:23:43 と 01:24 の行）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-表I-I p.65／55（`Severe shocks`）'),
    'c620': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：問いの札（棒の影・第8章へ）｜注：🔧 イメージ Pexels 12191470（観覧車）→ 図。観覧車は c621 へ｜新しい画（映像方針）：🔧 模式（問い＝止めるボタンのあとに、なぜ爆発？＝棒の影だけ・「第8章」の札）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'c621': dict(kind='フリー素材',
               plan='🔧 X12191470｜映像の素材 5.84秒・倍率 0.83（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のプリピャチ（Pexels）｜動き：映像（0.83倍）｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：🔧 1986年の4号炉-コ → 次の章（3キロ先の町）の予告＝町の今。→ 第6章の扉｜⑤b-1（10-22）：実測のカット 7.02秒＞素材 5.84秒＝0.83倍（決まり 0.6 以上の内・観覧車は語りに合う＝替えない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-22）：案C2 止める棒（前触れ）＝置き場 N2 view top（`tools/illu24.py`・門番 check_illu ㊴）
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c615（2行・6.8秒）＝1行目「ボタンで、抜いてあった棒が、いっせいに下り始めた」＝炉の上の方で棒がいっせいに下り始める（炉は不透明の塊＝
    #   下の水と押しのけ棒はまだ見せない）／2行目「炉を止めるための棒である。ところが、その3秒後。」＝そこで止める。下がる長さは記録の速さ
    #   （毎秒0.4m＝S1 p113）×3秒（1:23:40→1:23:43＝表I-I p65）＝120cm まで（門番 ㊴）
    "c615": dict(fig=("illu", dict(
        place="N2", start=dict(view="top"),
        steps=[dict(state=dict(n2dy=60.0, n2arrow="on"), dur=3.0,
                    rec="S1 p113（inserted into the core at a speed of 0.4 m/s when the EPS is triggered）・S1 p65（01:23:40 EPS-S button was pressed）",
                    tag=dict(t="制御棒", at="rod", off=(60, -60))),
               dict(state=dict(n2dy=120.0), dur=3.0, rec="S1 p65（01:23:43 Power excursion rate emergency protection system signals on）")]))),
})
