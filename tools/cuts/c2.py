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
                    # 試し焼き 39791009342：指し線がドラムの上を斜めに横切った＝ドラムの下の真ん中から短く
                    tag=[dict(t="蒸気ドラム", at="drum", off=(-10, 70)), dict(t="タービンへ", at="steam", off=(-40, 80), anchor="end")])]))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。地図 c203 は ⑤b-6
#   🔴 色は報告の色（1986年の報告＝桃・1986年のソ連の報告＝橙・1991年の委員会＝紫・1992年の報告＝青）。画面の字の数は全部 rel に
#   （報告の名の年は `rr(...)`）。🔴 段の数＝語りの行の数（聞き役の問いの行は dict()＝何も足さない）
# ══════════════════════════════════════════════════════════
from mech24 import rr  # noqa: E402

SPEC.update({
    # c205（2行）＝1行目「主に3つの報告である。1986年の報告、」＝8月のソ連の報告（細い点）と9月の1986年の報告／2行目＝1991年・1992年と「改めた」の弧
    "c205": dict(
        t="追いかける報告の順番", s="事故のあとに出た報告と、その年",
        fig=("m24", dict(view="years", steps=[dict(state=dict(s86="on", r86="on")), dict(state=dict(c91="on", r92="on", arc="on"))],
                         rel=rr("r86", "s86", "c91", "r92") + [dict(t="INSAG-1・INSAG-7", src="S1 p1"), dict(t="主に3つ", src="S1 p34")],
                         note="点の間隔は時間に比例しない（順と年だけ）", src=ss.src(["S3 p2003", "S2 p1001", "S1 p39", "S1 p1"])))),
    # c206（3行）＝1行目は聞き役の問い／2行目で7つの札（①〜⑦＝台本 §4 の画の欄の順）／3行目で各札に「？」と1992年の報告の札（評価と比べる）
    "c206": dict(
        t="事故の年の「違反」", s="このあと1つずつ見ていく",
        fig=("m24", dict(view="cards7", steps=[dict(), dict(state=dict(cards="on")), dict(state=dict(ask="on"))],
                         rel=[dict(t="0時28分", src="S1 p63"), dict(t="700メガワット", src="S2 p1025")] + rr("r92"),
                         note="札の言葉は要約", src=ss.src(["S2 p1027", "S1 p34"])))),
    # c209（2行）＝1行目：炉が出す熱 3,200MW → 電気 1,000MW（S2 p1008）／2行目：ウラン → 速い中性子 → 黒鉛で遅く → 次のウランが割れる → 続く
    "c209": dict(
        t="炉の大きさと黒鉛の役目", s="RBMK という型の炉",
        fig=("m24", dict(view="neutron", steps=[dict(state=dict(power="on")), dict(state=dict(chain="on"))],
                         rel=[dict(t="4号炉", src="S2 p1008"), dict(t="3,200", src="S2 p1008"), dict(t="1,000", src="S2 p1008")],
                         note="粒の大きさと動きは模式", src=ss.src(["S2 p1008", "S1 p113"])))),
    # c210（2行）＝1行目：水の管（泡と吸われる中性子）＋輪の上と右（沸く・泡 → 吸う水が減る）／2行目：下と左（反応が強まる → 熱が増える）と名前
    "c210": dict(
        t="泡が反応を強める", s="RBMK の炉の性質",
        fig=("m24", dict(view="void", steps=[dict(state=dict(tube="on", n12="on")), dict(state=dict(n34="on", name="on"))],
                         rel=[], note="輪の矢印は性質の順（模式）", src=ss.src(["S1 p13"])))),
    # c211（3行）＝1行目は聞き役の問い（目盛りだけ）／2行目：およそ20%より下を赤く＋1986年の報告／3行目：上がると、さらに上がる
    "c211": dict(
        t="低い出力の弱点", s="出力の大きさと、炉の向き",
        fig=("m24", dict(view="power20", steps=[dict(), dict(state=dict(low="on")), dict(state=dict(loop="on"))],
                         rel=[dict(t="およそ20%", src="S2 p1009")] + rr("r86"),
                         note="目盛りは割合だけ（模式）", src=ss.src(["S2 p1009"])))),
    # c214（3行）＝1行目：外の電気が止まる（×）・ディーゼル発電機が動くまでの「このあいだ」／2行目：止まりかけのタービン → 電気 → ポンプ／
    #   3行目：試験で確かめる（？）
    "c214": dict(
        t="電気が途切れるあいだ", s="4号炉の試験の中身",
        fig=("m24", dict(view="flow4", steps=[dict(state=dict(cut="on")), dict(state=dict(chain="on")), dict(state=dict(test="on"))],
                         rel=[], note="流れは模式", src=ss.src(["S3 p2019", "S2 p1009"])))),
    # c215（2行）＝横から見た燃料の管（1本）。1行目：止めた炉でも燃料は熱を出す（赤い波）／2行目：ポンプで冷やす水を送り続ける
    "c215": dict(
        t="止めた炉も熱い", s="燃料の熱とポンプ",
        fig=("m24", dict(view="decay", steps=[dict(state=dict(heat="on")), dict(state=dict(pump="on"))],
                         rel=[], note="管と棒の形と数は模式", src=ss.src(["S1 p121"])))),
    # c216（3行）＝暦 1982〜1986年。1行目：1982年 3号機／2行目：1984年・1985年（改良した装置）／3行目：1983年12月 4号機の運転の始まり
    #   （この試験をしないまま）と 1986年4月（この夜の試験）
    "c216": dict(
        t="前にもあった同じ試験", s="試験が行われた年",
        fig=("m24", dict(view="cal", steps=[dict(state=dict(y82="on")), dict(state=dict(y8485="on")), dict(state=dict(y83="on", y86="on"))],
                         rel=[dict(t="1982年・3号機", src="S1 p61"), dict(t="1984年・1985年", src="S1 p61"), dict(t="1983年12月・4号機", src="S1 p61"),
                              dict(t="1986年4月", src="S1 p63")],
                         note="暦の印は年と月だけ", src=ss.src(["S1 p61"])))),
    # c219（2行）＝試験の計画の書類（安全の手当ての欄が薄い）。1行目：1991年の委員会「十分でなかった」／2行目：1986年のソ連の報告「形だけ」
    "c219": dict(
        t="計画の弱いところ", s="2つの報告の見方",
        fig=("m24", dict(view="plan", steps=[dict(state=dict(c91="on")), dict(state=dict(s86="on"))],
                         rel=rr("c91", "s86"), note="書類の形は模式", src=ss.src(["S1 p62", "S3 p2019"])))),
    # c220（3行）＝1行目は聞き役の問い（1992年の報告の札）／2行目「計画そのもの」（薄い）／3行目「計画を変えた」（赤い印）＋承認なし・その場で・わざと
    "c220": dict(
        t="責めたのは「変え方」", s="書き直した報告の見方",
        fig=("m24", dict(view="blame", steps=[dict(state=dict(hdr="on")), dict(state=dict(plan="on")), dict(state=dict(chg="on"))],
                         rel=rr("r92"), note="札の言葉は要約（模式）", src=ss.src(["S1 p34"])))),
    # c222（2行）＝1行目：試験の計画の中の「非常用の冷却を切る」／2行目：試験のあいだ炉の安全が大きく下がる（1986年のソ連の報告）。🔴 約4時間は書かない（§1-5）
    "c222": dict(
        t="計画にあった危うさ", s="計画の一行と、その意味",
        fig=("m24", dict(view="cut", steps=[dict(state=dict(item="on")), dict(state=dict(band="on"))],
                         rel=rr("s86"), note="安全の線の高さは模式（数は無い）", src=ss.src(["S3 p2019"])))),
    # c224（2行）＝上から見た発電所の4つの号機（🔁 横から c215 → 上から）。2行目：4号機に黄の輪「ここから」4月25日
    "c224": dict(
        t="事故の前の日へ", s="チェルノブイリ原子力発電所",
        fig=("m24", dict(view="site", steps=[dict(), dict(state=dict(mark="on"))],
                         rel=[dict(t="1号機・2号機・3号機・4号機", src="S2 p1008"), dict(t="4月25日", src="S1 p63")],
                         note="号機の並びと形は模式", src=ss.src(["S2 p1008", "S1 p63"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-23）：地図 c203＝`tools/mech24.py` の ussr（Natural Earth の国の形＝`ref/ep24/make_map24.py`・衛星写真は使わない）
#   🔴 1986年の境＝クリミア半島はウクライナ（共和国）の色。点（町と発電所）は一般の座標＝注に断る
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c203（2行）＝左＝ソ連の全体（ウクライナはからし色）・右＝ウクライナの北の拡大（キエフ・チェルノブイリの町・プリピャチ・発電所）／
    #   1行目＝176人（当直の職員と作業員）／2行目＝＋268人（建設中の新しい号機の現場・夜の仕事）（S3 p2016）
    "c203": dict(
        t="あの夜、現場にいた人", s="キエフの北の原子力発電所",
        fig=("m24", dict(view="ussr", steps=[dict(state=dict(staff="on")), dict(state=dict(night="on"))],
                         rel=[dict(t="176人", src="S3 p2016"), dict(t="268人（第3期の工事）", src="S3 p2016")],
                         note="国の形＝Natural Earth（1:50m）・1986年の境（クリミアはウクライナ）・点の位置は一般の座標",
                         src=ss.src(["S3 p2016"])))),
})
