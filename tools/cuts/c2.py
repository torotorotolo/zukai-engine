# -*- coding: utf-8 -*-
"""第1章　4号炉の試験 c201–c224（24カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

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
    'c201': dict(kind='写真',
               plan='I22｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：雪の中のチェルノブイリ原子力発電所｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：前｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり。事故の前の姿（説明の語「1986年の冬」まで）｜⑤b-2（10-22）：Commons の説明（API）に年も季節も無い＝副題は写っているもの（雪・送電塔）に｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.21／17（`at about 1:24 there occurred two explosions one after the other`）・S3 p.6／2（`The accident took place prior to shut-down of the unit for planned maintenance`）'),
    'c202': dict(kind='写真',
               plan='I28｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：チェルノブイリの町の碑｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：前｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（c927 が同じ碑の今）｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='R3 外務省 報道発表 2022-03-31（「首都以外の地名についても、ウクライナ語による読み方に基づく呼称に変更」）・R4 外交青書2022 第3章第1節4（「チョルノービリ原子力発電所」）'),
    'c203': dict(kind='図解',
               plan='一覧の種類：地図｜見る向き：上から｜見た目の型：地図（ソ連とウクライナ・色を多く）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.16／12（`On the night of 25-26 April 1986 there were 176 duty operational staff`）'),
    'c204': dict(kind='写真',
               plan='I23｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：発電所の入口の看板｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：前｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.118／~111（`300 power plant and fire-fighting personnel admitted to hospitals`…`of whom 31 have so far died`）'),
    'c205': dict(kind='図解',
               plan='🔧 一覧の種類：年表｜見た目の型：年表｜注：§0-5（報告3つ＋1986年8月のソ連の報告）｜新しい画（映像方針）：🔧 年表（4つの点＝1986年8月 ソ連の報告〈ウィーンの会議の資料〉・1986年9月 1986年の報告〈INSAG-1〉・1991年 ソ連の委員会の報告〈INSAG-7 の付属書I〉・1992年 書き直しの報告〈INSAG-7〉＝語りの「主に3つ」を太い点・8月のソ連の報告は細い点・色を多く）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`does not retract INSAG-1, nor does it alter the conclusions of that report`）'),
    'c206': dict(kind='図解',
               plan='一覧の種類：札｜見た目の型：札（7つの札）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.27／~24（`This series of wilful violations of procedure, extraordinary as they were`）'),
    'c207': dict(kind='写真',
               plan='🔧 関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）｜R15｜一覧の種類：参考｜見せ方：額装（BY-SA）｜副題：同じ型の炉の制御盤（レニングラード原発・2008年）｜動き：額ごと寄る｜権利：CC BY-SA 3.0｜時期：他所｜人：顔｜出典の行：RIA Novosti archive（CC BY-SA 3.0）・撮影者は作者欄のとおり｜注：🔧 IAEA 02790035（運転員の写真）→ c418 へ。語りは炉の型の紹介＝同じ型の炉の制御室。運転員は1人（公的な任務・責める行でない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書II p.113／103（`with a graphite moderator and a boiling light water coolant`）'),
    'c208': dict(kind='再現イラスト',
               plan='一覧の種類：断面｜見る向き：横から｜見た目の型：炉の断面（案C1）｜合図：🔁 上から→横から（前の図 c203）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書II p.113／103（`There were 1660 fuel channels in the vertical ducts of the graphite columns`）'),
    'c209': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：粒（中性子と黒鉛と水）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.8／~3（`with an operating power of 1000 MW(e), 3200 MW(th)`）'),
    'c210': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：輪の矢印（泡と反応）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.13／3（`the void and power coefficients of reactivity were both positive`）'),
    'c211': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：目盛り（出力の性質）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.9／~4（`becomes positive below approximately 20% of full power`）'),
    'c212': dict(kind='写真',
               plan='🔧 関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）｜R11｜一覧の種類：参考｜見せ方：額装（BY-SA）｜副題：同じ型の炉の上＝制御棒の頭が並ぶ（レニングラード原発・2008年）｜動き：額ごと上へ｜権利：CC BY-SA 3.0｜時期：他所｜人：遠景｜出典の行：RIA Novosti archive（CC BY-SA 3.0）・撮影者は作者欄のとおり｜注：🔧 模式（211本・18秒の砂時計）→ 写真。語り「止めるときに入る棒は、上から差し込む」＝炉の上の床。§0-5「主に上から」の札は不要に。18秒の砂時計は c908 だけ（同じ図を2回使わない）｜新しい画（映像方針）：🔧 実写（同じ型の炉の上の円い床）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書II p.113／103（`consists of 211 movable solid absorber rods`）・S1 p.14／4（`when starting from the upper limit stop switches, was 18 s`）'),
    'c213': dict(kind='写真',
               plan='I34｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：原発の当直の職員｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：前｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（語り＝試験の予定・責める行でない）｜⑤b-2（10-22）：年は原文に無い＝外した。⚠️ 説明「Atomic power plant personnel worked around the clock」（事故の記録の組）＝事故のあとの写真かもしれない＝爆発の前の章に置いてよいかは ⑤b-7 で｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.27／~24（`A special test was planned just prior to taking the Unit out of service for scheduled maintenance.`）・S3 p.19／15（`tests were to be carried out on turbogenerator No. 8`）'),
    'c214': dict(kind='図解',
               plan='一覧の種類：流れ｜見た目の型：流れ図（電気の流れ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.19／15（`to test the possibility of utilizing the mechanical energy of the rotor`）・S2 p.9／~4（`until the standby diesel generators could supply emergency power`）'),
    'c215': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：管と熱（燃料の熱と冷やす水）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書II p.121／111（`to verify whether cooldown of the core by forced cir-culation could be maintained`）'),
    'c216': dict(kind='図解',
               plan='一覧の種類：暦｜見た目の型：暦｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.61／51（`In 1982, the corresponding tests were carried out at Chernobyl Unit 3`・`Additional tests with a modernized rundown unit were performed in 1984 and 1985.`・`Chernobyl Unit 4 was com-missioned in December 1983 without having been tested under these conditions`）'),
    'c217': dict(kind='文字の頁',
               plan='S3p19+S1p62｜一覧の種類：頁｜見せ方：頁｜副題：1986年のソ連の報告（左）と1991年の委員会の報告（右）｜動き：寄る（左右の行へ）｜見た目の型：文字の頁（2枚）｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：ソ連の報告 Part I（1986年8月）p.19 と INSAG-7 付属書I p.62｜注：台本どおり＝語りが名指しする所｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.19／15（`was not properly prepared and had not received the requisite approval`）'),
    'c218': dict(kind='写真',
               plan='🔧 CR1｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：1号機の制御室（2011年）｜動き：額ごと右へ｜権利：CC BY-SA 3.0｜時期：今・中｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 3.0｜注：🔧 イメージ（Pexels）→ 壊れていない1号機の制御室（同じ型・人なし）｜新しい画（映像方針）：🔧 実写 1号機の制御室（壊れていない部屋・炉心の見取り盤と制御棒の計器・人なし）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.62／52（`there is nothing wrong with the programme itself`・`did not require the plant managers to obtain approval for such tests`・`from the aforementioned organizations`）・S1-付属書I p.61／51（`should be approved by the General Designer`）'),
    'c219': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：書類（安全の欄が薄い）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.62／52（`not entirely satisfactory, primarily in terms of its safety measures`）・S3 p.19／15（`the section on safety measures was drafted in a purely formal way`）'),
    'c220': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：札の比べ（〇と赤い印）｜注：🔧 実写 c475（2013年の石棺と覆い）→ 図。爆発の前の章に今の跡の写真を置かない（§0-5）。c475 は c923 へ｜新しい画（映像方針）：🔧 模式（書き直した報告のいちばん強い責め＝「計画そのもの」の札は薄く・「承認のないまま、その場でわざと変えた」の札に赤い印＝字は少なく）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`unapproved changes in the test procedure were deliberately made on the spot`）'),
    'c221': dict(kind='写真',
               plan='🔧 I26｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：事故の前のプリピャチ｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：前｜人：遠景｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：🔧 現在の4号炉-ア（2013年）→ 事故の前の町の写真（c705 から移した）。語り＝報告の見方の割れ（責める行でない）｜⑤b-2（10-22）：撮影日の欄「before 26 April 1986」＝年は分からない＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.29／19（`the test procedure was altered on an ad hoc basis`）'),
    'c222': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：帯と札（安全が下がる時間）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src="S3 p.19／15（`it called for shutting off the reactor's emergency core cooling system`）"),
    'c223': dict(kind='写真',
               plan='🔧 P84:発電所｜一覧の種類：実写｜見せ方：全面｜副題：事故の2年前の発電所（1984年1月・アメリカの偵察衛星）｜動き：寄る｜権利：Public domain｜時期：前｜人：なし｜出典の行：アメリカの偵察衛星の写真（USGS EarthExplorer・Public domain）｜注：🔧 現在の4号炉-ハ（2013年）→ 1984年の衛星写真（PD・原本から発電所を切り出す）。どの建屋が4号機かは絵で決められない＝印を付けない｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.19／15（`the staff departed from the programme and thereby created the conditions for the emergency situation`）'),
    'c224': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：発電所の配置（上から・4号炉に印）｜合図：🔁 横から→上から（前の図 c215）｜注：台本どおり（4月25日の夜明け前＝ここから）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.35／~32（`The start of reactor power`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-22）：案C1 炉の断面＝置き場 N1（`tools/illu24.py`・門番 check_illu ㊳）
# ══════════════════════════════════════════════════════════
#   全面の絵は見出し t・副題 s を書かない（§5b-83③）。🔁 前の図 c203（上から）→ 横から＝頭の切り替えの字（switch）
SPEC.update({
    # c208（2行・8.3秒）＝1行目「管の数は1,660本。下から入った水は、燃料の熱で沸いて蒸気になる」＝下から水の矢印 → 管の上の方が白く（沸く）→
    #   集め管からドラムへ／2行目「その蒸気でタービンを回して、電気をつくる」＝蒸気の管が画面の右の外へ（タービンは描かない＝2台は数を描かない）
    "c208": dict(fig=("illu", dict(
        place="N1", start=dict(switch="on"),
        steps=[dict(state=dict(n1flow="on", n1boil="on", n1rise="on"),
                    rec="S1 p113（Individual pipes supply subcooled water to each channel and remove the steam-water mixture）",
                    tag=[dict(t="燃料と水の管（1,660本）", at="ch", off=(70, -150)), dict(t="黒鉛", at="core", off=(-150, 40), anchor="end")]),
               dict(state=dict(n1steam="on"), rec="S1 p113（The saturated steam is sent to two turbines）",
                    tag=[dict(t="蒸気ドラム", at="drum", off=(-200, 130)), dict(t="タービンへ", at="steam", off=(-40, 80), anchor="end")])]))),
})
