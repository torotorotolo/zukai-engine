# -*- coding: utf-8 -*-
"""第7章　1986年8月、ウィーン c801–c824（24カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

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
    'c801': dict(kind='写真',
               plan='I45｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：ルイシコフ閣僚会議議長の視察（1986年）｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（語りが名指し・公人）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'c802': dict(kind='写真',
               plan='I56｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：事故後検討会議の記者会見（1986年8月・ウィーン）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.1（`held in Vienna from 25 to 29 August 1986`）'),
    'c803': dict(kind='写真',
               plan='I61｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：会議の議長と IAEA 事務局長の席（1986年8月）｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（語りがブリクスの名札を名指し）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.21／~17（`More than 500 highly qualified experts from 62;countries and 21 international organizations`）'),
    'c804': dict(kind='写真',
               plan='I60｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：ソ連の専門家団の長の名札（1986年8月）｜動き：額ごと上へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（名札＝寄らない・語りが名指し）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.7／~2（`leading Soviet scientists and nuclear engineers presented a report`）'),
    'c805': dict(kind='文字の頁',
               plan='S3p26｜一覧の種類：頁｜見せ方：頁｜副題：1986年のソ連の報告 第4章の違反の表｜動き：寄る（表へ）｜見た目の型：文字の頁（表）｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：ソ連の報告 Part I（1986年8月）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.26／22（`lists the most dangerous violations of the operating rules committed by the staff`）'),
    'c806': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：3つの列（違反・動機・結果）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.26／22（`Operator error in switching off local automatic control`）'),
    'c807': dict(kind='写真',
               plan='I58｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：会議のソ連側の席（1986年8月）｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（名札の名は副題に出さない＝承認①）｜責める行の門番の例外＝会議のソ連側の席（ソ連の専門家団の長の名札）＝語りはソ連の報告が「職員の動機」をどう説明したか＝説明した側の写真｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.26／22（`Meeting the requirements of the tests`）・S3 p.27／23（`The chief motive of the staff was to complete the tests as expeditiously as possible.`）'),
    'c808': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：重なり（6つの札が1か所）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.27／23（`the prime cause of the accident was an extremely improbable combination of violations`）'),
    'c809': dict(kind='写真',
               plan='I57｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：事故後検討会議の記者会見の別の1枚（1986年8月）｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（副題を c811・c814 と書き分ける＝⑤b で原寸）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.27／23（`since they considered such a conjunction of events to be impossible`・`did not provide for protective safety systems capble of preventing an accident`）'),
    'c810': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：札を運ぶ手（主語は職員）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.27／23（`the positive void coefficient of reactivity was able substantially to enhance the power excursion`）'),
    'c811': dict(kind='写真',
               plan='I59｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：記者会見の壇上（1986年8月・ウィーン）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（副題は⑤b で原寸から＝同じ副題を避ける）｜責める行の門番の例外＝記者会見の壇上＝語りは「主語は職員」というソ連の説明の書き方＝説明した側の写真｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.2（`30 August - 5 September 1986`）'),
    'c812': dict(kind='文字の頁',
               plan='S2p18｜一覧の種類：頁｜見せ方：頁｜副題：1986年の報告（INSAG-1）の要約の頁｜動き：寄る（原因の文へ）｜見た目の型：文字の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：GC(SPL.I)/3＝INSAG-1 の本文｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.18／~13（`the accident was eaused by a remarkable range of human errors`・`in combination with specific reactor features which compounded and amplified the effects of the errors`・`led to the reactivity excursion`）'),
    'c813': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：大小の札（人の誤りと炉の性質）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src="S2 p.112／~105（`is to be found in the so-called 'human element'`）"),
    'c814': dict(kind='写真',
               plan='I62｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：議長と事務局長の名札（1986年8月）｜動き：額ごと上へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.110／~103（`the course of events described as having taken place is entirely plausible`・`This is not to say that questions do not remain`）'),
    'c815': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：扉（閉じたまま）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.47／~42（`no attempt has been made to find alternative explanations`）'),
    'c816': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：3つの輪（安全文化）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.18／~13（`supplemented by the creation and maintenance of a "nuclear safety culture"`）'),
    'c817': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：札（誤りに強い作り）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.50／~45（`Nuclear plant designs must be as far as possible invulnerable to operator error`）'),
    'c818': dict(kind='写真',
               plan='🔧 I13｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：3・4号機の屋根での作業（1986年）｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：遠景｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：🔧 1986年の4号炉-エ → c702 から移した（語り＝1986年の報告の重心＝事故のあとの年の写真は合う）。人は小さい遠景｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'c819': dict(kind='写真',
               plan='I40｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：事故のあとの溶接の作業（1986年）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.11／1（`made no attempt to generate alternative scenarios`・`although it was recognized that there were other possible explanations`）'),
    'c820': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：机の札（棒の特徴が無い）｜注：🔧 1986年の4号炉-オ → 図（1986年の壊れた炉の写真がもう無い）｜新しい画（映像方針）：🔧 模式（1986年の会議の机＝止める棒の特徴の札が無い・1992年の報告の「明かされていたら」の札）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.27／17（`Certainly the account in INSAG-1 would have been different had the features of the control`）'),
    'c821': dict(kind='文字の頁',
               plan='🔧 S3p28｜一覧の種類：頁｜見せ方：頁｜副題：1986年のソ連の報告の改造の計画の頁｜動き：寄る（棒の一文へ）｜見た目の型：文字の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：ソ連の報告 Part I（1986年8月）｜注：🔧 1986年の4号炉-カ → 語りが「一文がある」と名指しする頁｜新しい画（映像方針）：🔧 頁（S3 p.28／24＝改造の計画の中の止める棒の一文）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.28／24（`a continuing increase in the multiplying characteristics of the core in its lower part`）'),
    'c822': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：棒の立体（いつも1.2m 差す）｜合図：🔁 上から→横から（前の図 c713）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.28／24（`as the rods move down from the upper stops`）'),
    'c823': dict(kind='写真',
               plan='I48｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：遠隔操作の盤（1986年）｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（操作員の名は言わない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'c824': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：問いの札（止める棒の形は？）｜注：🔧 1986年の4号炉-サ → 図（→ 第8章の扉）｜新しい画（映像方針）：🔧 模式（問い＝その止める棒は、どんな形？＝棒の影だけ・次の章へ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}
