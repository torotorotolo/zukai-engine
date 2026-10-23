# -*- coding: utf-8 -*-
"""第8章　止める棒の先 c901–c927（27カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

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
    'c901': dict(kind='図・写真の頁',
               plan='S1p15｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告（INSAG-7）の図1＝止める棒｜動き：寄る（(a) 事故の前へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 の図1｜注：台本どおり（案C の形のもとの頁＝了承②）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.14／4（`with a water filled space of 1.25 m separating the displacer and the absorbing rod`）'),
    'c902': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：棒の立体（上下の作り）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src="S1 p.14／4（`A graphite rod termed a 'displaced is attached`）"),
    'c903': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：棒の立体（抜き切った状態・1.25m）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.14／4（`with 1.25 m of water at either end`）・S1 p.16／6（`height 7 m`）・S1-図1 p.15／5（図の中の寸法＝押しのけ棒 450cm・水 125cm＝頁の画像で確かめた）'),
    'c904': dict(kind='写真',
               plan='🔧 C3313｜一覧の種類：実写｜見せ方：全面｜副題：宇宙から見た発電所（2018年・NASA）｜動き：寄る｜権利：Public domain｜時期：今・跡｜人：なし｜出典の行：NASA（Public domain）｜注：🔧 IAEA 02790041（作業員の顔の寄り）→ 人の写らない写真（§0-5）。c404 から移した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.53／43（`the absorbing capacity of the graphite displacer`・`is lower than that of the water being forced out`）'),
    'c905': dict(kind='再現イラスト',
               plan='一覧の種類：案C2｜見る向き：横から｜見た目の型：棒の立体（本番・案C2）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.14／4（`caused a local insertion of positive reactivity in the lower part of the core`）'),
    'c906': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：炉の高さの色（下が赤・上が青）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.14／4（`depended on the spatial distribution of the power density and the operating regime`）・S1-付属書I p.53／43（`local introduction of positive reactivity in the lower part of the core occurs`）・S1-付属書I p.49／39（`predetermine an initial increase in positive reactivity`）'),
    'c907': dict(kind='図・写真の頁',
               plan='🔧 S1p133｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告の図（上から差す棒が反応を強める仕組み）｜動き：寄る（図 II-10 の (a)〜(c) へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 付属書II の図 II-10｜注：🔧 IAEA 02790047（作業員の顔の寄り）→ 語り「ポジティブ・スクラム」の図そのもの（§0-5＝顔を外す）。C0 は cc18 へ｜新しい画（映像方針）：🔧 頁（INSAG-7 付属書II p.133／123 の図 II-10＝吸収材・押しのけ棒・水と反応の±）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'c908': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：砂時計（18秒→12秒）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.14／4（`when starting from the upper limit stop switches, was 18 s`）・S1 p.37／27（`reduced from 18 s to 12 s`）'),
    'c909': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：3つの線（残した棒と効き方）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.49／39（`In the case of a non-regulation ORM of 7 control rods`・`the chain reaction is being accelerated rather than terminated`）'),
    'c910': dict(kind='図・写真の頁',
               plan='🔧 S1p141｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告の図（止める仕組みの効き方・1の線が1986年4月26日の4号炉）｜動き：寄る（1の線へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 付属書II の図 II-15｜注：🔧 IAEA 02790037（作業員の顔）→ 語り「残した棒が少ないほど危なかった」の物証（1の線だけが最初の数秒で反応が上がる）。c909 の模式はこの図を易しくしたもの＝続けて出す｜新しい画（映像方針）：🔧 頁（INSAG-7 付属書II p.141／131 の図 II-15＝1：ORM 7本の4号炉・2：15本・3：30本・4：改良）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.24／14（`made them crucially sensitive to the extent of insertion of the control and protection rods`）・S1 p.28／18（`INSAG now repeats that the violation took place`）・S1 p.21／11（`were not aware that it had safety significance`）'),
    'c911': dict(kind='図解',
               plan='一覧の種類：暦｜見た目の型：暦（1983→1986）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.53／43（`discovered experimentally in November/December 1983 during the physical startup of Ignalina Unit 1`）'),
    'c912': dict(kind='写真',
               plan='🔧 関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）｜IGA｜一覧の種類：参考｜見せ方：額装（BY-SA）｜副題：同じ型の炉のイグナリナ原発（リトアニア）｜動き：額ごと右へ｜権利：CC BY-SA 4.0｜時期：他所｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：🔧 現在の4号炉-サ → 語りが名指しするイグナリナ原発（1号機と2号機の2つの排気筒）。撮影年は⑤b で原寸と頁から｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.53／43（`and that of Chernobyl Unit 4`・`almost two-and-a-half years before the Chernobyl accident`）'),
    'c913': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：2つの札（本文と委員会の書き方）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.23／13（`Ignalina RBMK plant in the Lithuanian Republic in 1983`）'),
    'c914': dict(kind='写真',
               plan='🔧 T143｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：送電塔のあいだの4号機（2010年）｜動き：額ごと上へ｜権利：CC BY-SA 2.0｜時期：今・跡｜人：なし｜出典の行：IAEA Imagebank（CC BY-SA 2.0）・撮影者は作者欄のとおり｜注：🔧 IAEA 02790043（職長の寄り）→ 人の写らない写真（§0-5＝主任設計技師と職員の行）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.53／43（`The Chief Design Engineer [22] and the Scientific Manager knew about this effect`）・S1-付属書I p.96／86（`The personnel were unaware of some of the dangerous features of the reactor`）'),
    'c915': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：札と×（実行されず）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.54／44（`but none of them were implemented before the accident`）'),
    'c916': dict(kind='写真',
               plan='I32｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：片づけに使われた大型の運搬車｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.25／15（`Such restrictions were never imposed and apparently the matter was forgotten.`）'),
    'c917': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：時間の矢印（欠陥の印が残る）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.26／16（`It is reprehensible that such a deficiency had been known of for so long`）'),
    'c918': dict(kind='図解',
               plan='一覧の種類：並べ｜見た目の型：並べ（2つの会議）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.23／13（`first acknowledged by Soviet experts at the Conference on Nuclear Power Performance and Safety`）'),
    'c919': dict(kind='写真',
               plan='I30｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：片づけに加わった兵士｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（語り＝報告の慎重な書き方・責める行でない）｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.26／16（`most likely final event`・`the conditions already prevailing because of the positive power coefficient`）'),
    'c920': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：霧（確かには分からない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.33／23（`It is not known for certain what started the power excursion`）'),
    'c921': dict(kind='写真',
               plan='I42｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：現場の科学者たち｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（語り＝ほかの弱点・責める行でない）｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.23／13（`Any of these could just as well have caused the initiating event`）・S1 p.24／14（`Does it really matter which shortcoming was the actual cause`）'),
    'c922': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：2本の物差し（別々の目盛り）｜注：§0-5｜新しい画（映像方針）：🔧 模式（出力の倍数を別々の物差しで＝左：1986年の報告「定格の100倍・4秒以内」・右：のちの計算「はじめの出力の3.5倍から、およそ80倍」・それぞれに比べるもとの札・同じ目盛りに並べない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.10／~5（`the first power peak reached 100 times the nominal power within four seconds`）・S1-付属書II p.131／121（`ranging from 3.5 times the initial value in Model 2 to approximately 80 times`）'),
    'c923': dict(kind='写真',
               plan='🔧 C475｜一覧の種類：実写｜見せ方：全面｜副題：建設中の新しい覆いと4号機と排気筒（2013年）｜動き：左へ｜権利：CC BY 2.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 2.0｜注：🔧 IAEA 02790046（作業員の寄り）→ 人の写らない写真（§0-5）。c220 から移した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.56／46（`all the design deficiencies of the RCPS were in fact known before the accident`）'),
    'c924': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：封筒（1983年の書簡）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.54／44（`Triggering of the EPS in this case may lead to the introduction of positive reactivity.`）・S1-付属書I p.100／90（`Letter No. 33-08/67 of 23 December 1983`）'),
    'c925': dict(kind='写真',
               plan='I49｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：片づけに使われた装甲のブルドーザー｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.23／13（`he made no such changes, and the procedural measures he recommended`）'),
    'c926': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：4つの札が1つの炉に｜注：§0-5＝札は語りの4つ（低い出力・少ない残りの棒・炉の性質・棒の欠陥）のまま｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.33／23（`the concurrence of the following major factors`）'),
    'c927': dict(kind='フリー素材',
               plan='🔧 X13188723:町｜映像の素材 22.06秒・倍率 2.56（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：捨てられた町の今（Pexels）｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：🔧 台本どおり（c202 と同じ碑）→ ⑤b-1（10-22）：碑の映像 X12160827 は 3.52秒＝実測のカット 8.61秒の 0.41倍（0.6 未満＝止め絵）・頭の差し込み（1行目まで 5.62秒＝0.63倍）は2行目の写真が要る＝手元でいちばん残りの長い X13188723（22.06秒・cb23 は新しい覆いの写る区間だけ）の**覆いの写らない区間**へ。区間と副題は ⑤b-2 でコマを見て決める → 第9章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-22）：案C2 止める棒（本番）＝置き場 N2 view cut（`tools/illu24.py`・門番 check_illu ㊴）
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c905（2行・7.3秒）＝INSAG-7 図1 (a) の寸法（吸う棒の先は炉の上の端の 20cm 上・水 125cm・押しのけ棒 450cm・水 125cm）。
    #   1行目「抜き切った棒を、いっせいに下ろすと、どうなるか」＝棒が下り始める／2行目「炉の下の方では、まず水が押し出され、かわりに黒鉛が入ってくる」
    #   ＝125cm 下がって押しのけ棒の下の端が炉の下の端へ → 炉の下の方 125cm が赤く（門番 ㊴＝赤はこのカットの最後の段だけ）
    "c905": dict(fig=("illu", dict(
        place="N2", start=dict(view="cut"),
        steps=[dict(state=dict(n2dy=30.0, n2arrow="on"), dur=2.4,
                    rec="S1 p14（On receipt of a scram signal causing a fully withdrawn rod to fall）"),
               dict(state=dict(n2dy=125.0, n2red="on"), dur=2.4,
                    rec="S1 p14（the displacement of water from the lower part of the channel・caused a local insertion of positive reactivity in the lower part of the core）",
                    # ⚠️ qa_all の layout：off=(40, -120)・字 30 では右の端が 1894（上限 1848）＝左へ寄せて字を 28 に
                    tag=dict(t="水が押し出され、黒鉛が入る", at="lo", off=(-30, -130), cap=28, delay=2.0))]))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。🔴 色は報告の色・画面の字の数は全部 rel に
#   🔴 段の数＝語りの行の数（聞き役の問いの行は dict()）。暦の相方 c911＝月の升目（c216 の5枚の暦と別の絵）・並べ c918＝演台（cc08 と別の絵）
#   🔴 c922＝2本の物差しを縦と横に分ける（100倍は定格の・3.5〜80倍ははじめの出力の＝同じ目盛りに並べない＝映像方針 §2）・c926＝語りの4つのまま
# ══════════════════════════════════════════════════════════
from mech24 import rr  # noqa: E402

SPEC.update({
    # c902（2行）＝1行目：棒の本体＝中性子を吸う物／2行目：その下に黒鉛の押しのけ棒（S1 p14）
    "c902": dict(
        t="上と下で違う素材", s="本体と、その下",
        fig=("m24", dict(view="rodparts", steps=[dict(state=dict(abs="on")), dict(state=dict(disp="on"))],
                         rel=[], note="棒の形は模式（長さは比べない）", src=ss.src(["S1 p14"])))),
    # c903（3行）＝1行目：押しのけ棒 4.5m／2行目：炉の高さ 7m・上と下に 1.25m ずつ／3行目：水だけの部分（S1 p14・p16・図1）
    "c903": dict(
        t="黒鉛は炉の真ん中に", s="上と下に残る水",
        fig=("m24", dict(view="len7", steps=[dict(state=dict(disp="on")), dict(state=dict(core="on")), dict(state=dict(water="on"))],
                         rel=[dict(t="4.5m", src="S1 p15（図1＝450cm）"), dict(t="炉の高さ 7m", src="S1 p16"), dict(t="1.25m", src="S1 p14")],
                         note="模式（長さは原文の値に比例）", src=ss.src(["S1 p14", "S1 p15", "S1 p16"])))),
    # c906（2行）＝1行目：炉の下の方が赤＝水が減って反応がかえって強まる／2行目：止めるための棒が入り始めに逆の働き（S1 p14・p53）
    "c906": dict(
        t="下の方だけ強まる", s="棒が入り始めたとき",
        fig=("m24", dict(view="lowred", steps=[dict(state=dict(low="on")), dict(state=dict(rev="on"))],
                         rel=[], note="色の分け方は模式", src=ss.src(["S1 p14", "S1 p53"])))),
    # c908（2行）＝1行目：18秒の砂時計／2行目：事故のあと12秒に（とされる）（S1 p14・p37）
    "c908": dict(
        t="遅かった棒", s="事故のあとの改め",
        fig=("m24", dict(view="sand", steps=[dict(state=dict(t18="on")), dict(state=dict(t12="on"))],
                         rel=[dict(t="18秒", src="S1 p14"), dict(t="12秒", src="S1 p37")],
                         note="砂時計は模式（高さは秒に比例）", src=ss.src(["S1 p14", "S1 p37"])))),
    # c909（2行）＝1行目：30本ぶん・15本ぶん・1991年の委員会／2行目：7本ぶん＝最初の8秒は強まる（S1 p49）
    "c909": dict(
        t="残した棒と効き方", s="ボタンを押したあと",
        fig=("m24", dict(view="lines3", steps=[dict(state=dict(two="on")), dict(state=dict(seven="on"))],
                         rel=[dict(t="30本ぶん・15本ぶん・7本ぶん", src="S1 p49"), dict(t="最初の8秒", src="S1 p49")] + rr("c91"),
                         note="線の形は模式（8秒の位置だけ時間に比例）", src=ss.src(["S1 p49"])))),
    # c911（3行）＝1行目は聞き役（升目と 1986年4月）／2行目：1983年の11月と12月・1991年の委員会／3行目：起動の試験の中で見つかった（S1 p53）
    "c911": dict(
        t="事故の前から", s="欠陥が見つかった時期",
        fig=("m24", dict(view="months", steps=[dict(), dict(state=dict(found="on")), dict(state=dict(test="on"))],
                         rel=[dict(t="1983年11月・12月", src="S1 p53"), dict(t="1984年・1985年", src="暦（あいだの年）"),
                              dict(t="1986年4月", src="S1 p63")] + rr("c91"),
                         note="升目1つが1か月", src=ss.src(["S1 p53"])))),
    # c913（2行）＝1行目：1992年の報告（本文）＝イグナリナだけ／2行目：1991年の委員会＝イグナリナとこの4号炉（S1 p23・p53）
    "c913": dict(
        t="名を挙げたのはどちらか", s="本文と付属書の書き方",
        fig=("m24", dict(view="names2", steps=[dict(state=dict(r92="on")), dict(state=dict(c91="on"))],
                         rel=[dict(t="チェルノブイリ4号機", src="S1 p53")] + rr("r92", "c91"),
                         note="表の作り（✓＝その報告が挙げた）", src=ss.src(["S1 p23", "S1 p53"])))),
    # c915（2行）＝1行目：棒の形を変える・抜き切る棒の数を限る・など＝1991年の委員会／2行目：どれも「実行されず」（S1 p54）
    "c915": dict(
        t="出ていた対策", s="手つかずのまま",
        fig=("m24", dict(view="ideas", steps=[dict(state=dict(cards="on")), dict(state=dict(none="on"))],
                         rel=rr("c91"), note="札の言葉は要約（模式）", src=ss.src(["S1 p54"])))),
    # c917（2行）＝1行目：1983年11月 → 1986年4月の矢印に欠陥の印が残る・1992年の報告／2行目：取り除かれなかった＝責められるべきこと（S1 p26）
    "c917": dict(
        t="放っておかれた欠陥", s="見つかってから事故まで",
        fig=("m24", dict(view="longarrow", steps=[dict(state=dict(long="on")), dict(state=dict(blame="on"))],
                         rel=[dict(t="1983年11月", src="S1 p53"), dict(t="1986年4月", src="S1 p63")] + rr("r92"),
                         note="模式（矢印の長さは月に比例）", src=ss.src(["S1 p26"])))),
    # c918（2行）＝1行目：1987年のウィーンの会議＝ソ連の専門家が公に認めた／2行目：1986年8月のウィーンの会議＝同じウィーンの別の会議（S1 p23）
    "c918": dict(
        t="欠陥を認めた場", s="翌年の会議",
        fig=("m24", dict(view="lecterns", steps=[dict(state=dict(y87="on")), dict(state=dict(y86="on"))],
                         rel=[dict(t="1987年", src="S1 p23"), dict(t="1986年8月（ウィーンの会議）", src="S3 p2003")],
                         note="演台は模式", src=ss.src(["S1 p23"])))),
    # c920（1行）＝暴走の始まりが霧で見えない・1992年の報告「確かには分かっていない」（S1 p33）
    "c920": dict(
        t="始まりは見えない", s="同じ報告のもう一言",
        fig=("m24", dict(view="fog", steps=[dict(state=dict(fog="on"))],
                         rel=rr("r92"), note="線と霧は模式", src=ss.src(["S1 p33"])))),
    # c922（3行）＝1行目：2本とも空／2行目：左の縦の物差し＝1986年の報告「4秒以内に最大の出力（定格）の100倍」／
    #   3行目：右の横の物差し＝のちの計算「はじめの出力の3.5倍から、およそ80倍」・比べるもとが違う（S2 p1010・S1 p131）
    "c922": dict(
        t="出力の最高の値", s="計算ごとの答え",
        fig=("m24", dict(view="rulers2", steps=[dict(state=dict(q="on")), dict(state=dict(r86="on")), dict(state=dict(later="on"))],
                         rel=[dict(t="100倍・4秒以内", src="S2 p1010"), dict(t="3.5倍〜80倍", src="S1 p131")] + rr("r86"),
                         note="模式（2本の物差しは別の目盛り＝並べて比べない）", src=ss.src(["S2 p1010", "S1 p131"])))),
    # c924（2行）＝1行目：1983年12月・研究所の科学の責任者から・出力が半分に下がったときなどに／2行目：止める棒で反応が強まりうる・1991年の委員会（S1 p54・p100）
    "c924": dict(
        t="事故の前の警告", s="研究所からの手紙",
        fig=("m24", dict(view="memo", steps=[dict(state=dict(send="on")), dict(state=dict(risk="on"))],
                         rel=[dict(t="1983年12月", src="S1 p100"), dict(t="50%", src="S1 p54")] + rr("c91"), note="紙は模式（言葉は要約）", src=ss.src(["S1 p54", "S1 p100"])))),
    # c926（3行）＝1行目：4つの札／2行目：事故の夜、この炉に重なっていた／3行目は聞き役（S1 p33）
    "c926": dict(
        t="そろってしまった条件", s="あの夜の炉",
        fig=("m24", dict(view="four", steps=[dict(state=dict(cards="on")), dict(state=dict(join="on")), dict()],
                         rel=[dict(t="4号炉", src="S2 p1008")], note="札の言葉は語りのまま（炉は模式）", src=ss.src(["S1 p33"])))),
})
