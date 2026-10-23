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

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。🔴 色は報告の色・画面の字の数は全部 rel に
#   🔴 ca10＝穴のあいた3枚の板（c816 の重なる輪と別の絵）・ca16＝この1枚だけの評価の一覧（4色＝③は水色の破線で「ようだ」の留保）・
#   ca20＝出さない言葉（無実・嘘）を札に使わない。人の名前は出さない（ca03 は役だけ）
# ══════════════════════════════════════════════════════════
import cuts.ss as ss  # noqa: E402
from mech24 import rr  # noqa: E402

SPEC.update({
    # ca03（3行）＝1行目は聞き役（運転員・炉の設計の2つの箱）／2行目：5月1日・研究所の研究グループの長／3行目：原因は炉の設計（✓）・1991年の委員会（S1 p70）
    "ca03": dict(
        t="早くからあった別の見方", s="事故の5日後",
        fig=("m24", dict(view="volkov", steps=[dict(), dict(state=dict(may1="on")), dict(state=dict(design="on"))],
                         rel=[dict(t="5月1日", src="S1 p70")] + rr("c91"), note="矢印と箱は模式", src=ss.src(["S1 p70"])))),
    # ca04（2行）＝1行目：6月の2回の会議で「職員の誤り」だけに絞られた／2行目：省庁をまたぐ科学技術の会議（S1 p70）
    "ca04": dict(
        t="1つに絞られた原因", s="6月の会議",
        fig=("m24", dict(view="funnel", steps=[dict(state=dict(narrow="on")), dict(state=dict(council="on"))],
                         rel=[dict(t="6月・2回の会議", src="S1 p70")] + rr("c91"), note="漏斗と札は模式", src=ss.src(["S1 p70"])))),
    # ca05（1行）＝会議の決定 → 道 → ウィーンなどでの説明・一方的・1991年の委員会（S1 p70）
    "ca05": dict(
        t="説明の向き", s="会議のあとに",
        fig=("m24", dict(view="road", steps=[dict(state=dict(open="on"))],
                         rel=[dict(t="6月の会議の決定", src="S1 p70")] + rr("c91"), note="道と標識は模式", src=ss.src(["S1 p70"])))),
    # ca07（3行）＝1行目：1991年の委員会も職員の違反を認める／2行目：25日の朝・残した棒 15本・止めなかった・わざと／3行目：事故の原因ではない（S1 p81）
    "ca07": dict(
        t="委員会も認めたこと", s="減っても続けた運転",
        fig=("m24", dict(view="notstop", steps=[dict(state=dict(viol="on")), dict(state=dict(rods="on")), dict(state=dict(notcause="on"))],
                         rel=[dict(t="15本", src="S1 p81"), dict(t="25日の朝", src="S1 p81")] + rr("c91"),
                         note="数の窓とボタンは模式", src=ss.src(["S1 p81"])))),
    # ca10（2行）＝1行目：炉の物理の性質・止める棒の設計（2枚）／2行目：手順に定めがなく調べてもいない状態へ（3枚目）・穴を通る矢印 → 事故・1992年の報告（S1 p33）
    "ca10": dict(
        t="重なりが事故に", s="事故の起き方",
        fig=("m24", dict(view="cheese", steps=[dict(state=dict(two="on")), dict(state=dict(three="on"))],
                         rel=[dict(t="3つが重なって起きた", src="S1 p33")] + rr("r92"), note="板と穴は模式（札の言葉は要約）", src=ss.src(["S1 p33"])))),
    # ca12（2行）＝1行目：1975年 レニングラード1号機・前触れと見る人もいる／2行目：切れた線・職員は知らなかった・1992年の報告（S1 p33）
    "ca12": dict(
        t="伝わらなかった前触れ", s="11年前の別の発電所",
        fig=("m24", dict(view="precursor", steps=[dict(state=dict(pre="on")), dict(state=dict(cut="on"))],
                         rel=[dict(t="1号機（レニングラード）・1975年", src="S1 p33"), dict(t="1986年（チェルノブイリ）", src="S1 p63")] + rr("r92"),
                         note="札と線は模式", src=ss.src(["S1 p33"])))),
    # ca14（2行）＝1行目：運転員の決定的な操作＝きわめて判断を誤っていた・1992年の報告／2行目：人の要素＝いまも大きな要素（S1 p34）
    "ca14": dict(
        t="それでも残る人の側", s="もう1つの見方",
        fig=("m24", dict(view="puzzle", steps=[dict(state=dict(ill="on")), dict(state=dict(human="on"))],
                         rel=rr("r92"), note="組み絵は模式（大きさは比べない）", src=ss.src(["S1 p34"])))),
    # ca16（2行）＝1行目は聞き役（7つの札）／2行目：1992年の評価の4色の枠と凡例（S1 p20〜22・p28・p34）
    "ca16": dict(
        t="最初の7つは、どうなったか", s="評価の一覧",
        fig=("m24", dict(view="bins4", steps=[dict(), dict(state=dict(sort="on"))],
                         rel=[dict(t="0時28分の急落", src="S1 p63"), dict(t="700メガワット", src="S2 p1025")] + rr("r92"),
                         note="評価の言葉は要約（③は「ようだ」のまま）", src=ss.src(["S1 p20", "S1 p21", "S1 p22", "S1 p28", "S1 p34"])))),
    # ca20（3行）＝1行目は聞き役／2行目：「運転員の責めは消えた」に×・1992年の報告／3行目：「1986年の報告は取り消し」に×（S1 p34）
    "ca20": dict(
        t="どちらでもない", s="言い過ぎに注意",
        fig=("m24", dict(view="twox", steps=[dict(), dict(state=dict(c1="on")), dict(state=dict(c2="on"))],
                         rel=rr("r86", "r92"), note="札の言葉は要約（模式）", src=ss.src(["S1 p34"])))),
    # ca22（2行）＝1行目：1989年の国際会議・設計の欠点 → 炉の不安定／2行目：運転の仕方 → 炉の不安定・おおむね合意（S1 p120）
    "ca22": dict(
        t="両方が原因", s="国際会議での合意",
        fig=("m24", dict(view="merge2", steps=[dict(state=dict(design="on")), dict(state=dict(oper="on"))],
                         rel=[dict(t="1989年の国際会議", src="S1 p120")], note="箱と矢印は模式", src=ss.src(["S1 p120"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-23）：写真・頁・映像（第9章の13）＝c2.py・c6.py の ⑤b-7 の塊と同じ書き方
# ══════════════════════════════════════════════════════════
_IGB, _LENN, _C3309, _C488, _C496, _C1 = P("igb"), P("lenn"), P("c3309"), P("c488"), P("c496"), P("c1")
SPEC.update({
    # ca01（2行）＝INSAG-7 付属書I p.41 の「…In sifting through…」から「…presented to the IAEA.」まで8行
    "ca01": dict(photo=P("s1p41"), trim=(0.004, 0.533, 0.993, 0.730), panel=True, color=1.0, fmove=ss.fm("in"), card_mix=0,   # 扉の地に混ぜない（引用）
                 t="早くから分かっていた欠陥", s="1991年の委員会の報告（INSAG-7 付属書I）の頁"),
    # ca02（2行）＝🔧 IAEA 02790044（毎日届いた新聞を読む作業員＝IAEA に出した資料の行・責める行でない）＝額ごと右へ。新聞の字は試し焼きを原寸で
    "ca02": dict(photo=P("i44"), panel=True, color=1.0, fmove=ss.fm("r"),
                 t="国際原子力機関への資料", s="毎日届いた新聞を読む作業員"),
    # ca06（3行・1行目は聞き役・評価の行＝人の写らない写真）＝IGB（同じ型の炉のイグナリナ原発・CC0・参考）＝全面で寄る
    "ca06": dict(photo=_IGB, **ss.mv(_IGB, "in"), side="none", color=1.0,
                 t="ほかの原発と比べて", s="同じ型の炉のイグナリナ原発（リトアニア・2008年）"),
    # ca08（2行・責める行＝人なし）＝T157（4号機の排気筒・2010年）＝額ごと上へ
    "ca08": dict(photo=P("t157"), panel=True, color=1.0, fmove=ss.fm("u"),
                 t="委員会のまとめ", s="4号機の排気筒（2010年）"),
    # ca09（2行）＝🔧 IAEA 02790055（ブリクス IAEA 事務局長の訪問・1988年5月・責める行でない）＝額ごと寄る
    "ca09": dict(photo=P("i55"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="1992年の結論", s="ブリクス IAEA 事務局長の訪問（1988年5月）"),
    # ca11（2行）＝LENN（同じ型の炉のレニングラード原発の1・2号機・PD・参考＝次の ca12 が名指し）＝全面で右へ
    "ca11": dict(photo=_LENN, **ss.mv(_LENN, "r"), side="none", color=1.0,
                 t="組織の全体", s="同じ型の炉のレニングラード原発の1号機と2号機（2010年）"),
    # ca13（3行・1行目は聞き役の問い）＝🔧 C3309（建設中の新しい覆いの骨組みと4号炉・CC BY 2.0・人なし）＝全面で寄る
    "ca13": dict(photo=_C3309, **ss.mv(_C3309, "in"), side="none", color=1.0,
                 t="減った重み", s="建設中の新しい覆いの骨組みと4号炉（2013年）"),
    # ca15（3行・10.8秒）＝Pexels 13188717（プリピャチの今）＝いちばん長いショット（6〜17秒）の真ん中
    "ca15": ss.vid("ca15"),
    # ca17（2行）＝🔧 C488（森の向こうの4号炉と排気筒・CC BY 2.0）＝全面で左へ
    "ca17": dict(photo=_C488, **ss.mv(_C488, "l"), side="none", color=1.0,
                 t="誤りとされない操作", s="森の向こうの4号炉と排気筒（2006年）"),   # 「書き直された…」は章の札に近い（dup）
    # ca18（2行）＝C496（吹雪の中の石棺・CC BY 2.0）＝全面で寄る
    "ca18": dict(photo=_C496, **ss.mv(_C496, "in"), side="none", color=1.0,
                 t="保護の見直し", s="吹雪の中の石棺（2016年）"),
    # ca19（3行）＝🔧 C1（石棺の鉄骨・CC BY 3.0・1600×1200）＝全面で上へ
    "ca19": dict(photo=_C1, **ss.mv(_C1, "u"), side="none", color=1.0,
                 t="いちばん強い責め", s="石棺の鉄骨（2008年）"),
    # ca21（2行）＝H06（新しい覆いと送電線・BY-SA 4.0）＝額ごと右へ
    "ca21": dict(photo=P("h06"), panel=True, color=1.0, fmove=ss.fm("r"),
                 t="変わったもの", s="新しい覆いと送電線（2018年）"),
    # ca23（2行）＝🔧 T138（冷却水路に映る4号機と排気筒・2010年）＝額ごと寄る → 第10章の扉
    "ca23": dict(photo=P("t138"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="亡くなった人の数", s="冷却水路に映る4号機と排気筒（2010年）"),
})
