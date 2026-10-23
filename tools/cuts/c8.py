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
               plan='I45｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：ルイシコフ閣僚会議議長の視察｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（語りが名指し・公人）｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
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
               plan='I40｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：事故のあとの溶接の作業｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
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
               plan='I48｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：遠隔操作の盤｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（操作員の名は言わない）｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'c824': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：問いの札（止める棒の形は？）｜注：🔧 1986年の4号炉-サ → 図（→ 第8章の扉）｜新しい画（映像方針）：🔧 模式（問い＝その止める棒は、どんな形？＝棒の影だけ・次の章へ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。🔴 色は報告の色・画面の字の数は全部 rel に
#   🔴 c806 の表＝1986年のソ連の報告の違反の表（3つの列・6つの行＝字は省いた）。「運転員の誤り」は2行目（0時28分の急落）の動機の欄だけ（S3 p2026）
#   🔴 c822＝改造の計画の一文（1.2m）だけ。押しのけ棒（第8章）はまだ描かない
# ══════════════════════════════════════════════════════════
from mech24 import rr  # noqa: E402

SPEC.update({
    # c806（2行）＝違反の表。1行目：列の名（違反・動機・結果）・1986年のソ連の報告／2行目：2行目の動機の欄「運転員の誤り」・0時28分の急落
    "c806": dict(
        t="違反の表", s="中身と動機と結果",
        fig=("m24", dict(view="table6", steps=[dict(state=dict(cols="on")), dict(state=dict(mark="on"))],
                         rel=[dict(t="0時28分", src="S3 p2026")] + rr("s86"), note="表の作り（行の中身の字は省いた）", src=ss.src(["S3 p2026"])))),
    # c808（2行）＝6つの札が1か所に重なる。1行目：1986年のソ連の報告「主な原因：違反の重なり」／2行目：説明の芯
    "c808": dict(
        t="ソ連の説明の芯", s="原因の結び",
        fig=("m24", dict(view="pile", steps=[dict(state=dict(pile="on")), dict(state=dict(core="on"))],
                         rel=rr("s86"), note="札の形は模式（6つ＝表の行の数）", src=ss.src(["S3 p2027", "S3 p2026"])))),
    # c810（2行）＝1行目：正のボイド係数が急上昇を大きく／2行目：職員 → 規則の外の状態・1986年のソ連の報告「持ち込んだのは職員」
    "c810": dict(
        t="主語は職員", s="炉の性質の書き方",
        fig=("m24", dict(view="carry", steps=[dict(state=dict(void="on")), dict(state=dict(staff="on"))],
                         rel=rr("s86"), note="炉と矢印は模式", src=ss.src(["S3 p2027"])))),
    # c813（2行）＝1行目は聞き役（原因の文の大小の札）／2行目：根本：人的要素
    "c813": dict(
        t="根本の原因", s="原因の文の重み",
        fig=("m24", dict(view="sizes", steps=[dict(), dict(state=dict(root="on"))],
                         rel=rr("r86"), note="札の大きさは模式", src=ss.src(["S2 p1018", "S2 p1112"])))),
    # c815（1行）＝閉じた扉「ほかの説明」→ 錠・1986年の報告「探さなかった」
    "c815": dict(
        t="閉じた扉", s="別の筋書き",
        fig=("m24", dict(view="door", steps=[dict(state=dict(shut="on"))],
                         rel=rr("r86"), note="扉は模式", src=ss.src(["S2 p1047"])))),
    # c816（2行）＝1行目：重なる3つの輪（決まり・人・組織）と安全文化・1986年の報告／2行目：育てて保つ
    "c816": dict(
        t="報告が出した言葉", s="決まりの先にあるもの",
        fig=("m24", dict(view="venn3", steps=[dict(state=dict(ring="on")), dict(state=dict(keep="on"))],
                         rel=rr("r86"), note="3つの輪は模式", src=ss.src(["S2 p1018"])))),
    # c817（2行）＝1行目：発電所に向かう赤い矢印（運転員の誤り）／2行目：盾「誤りに強い作り」・1986年の報告
    "c817": dict(
        t="設計への求め", s="人の側だけでなく",
        fig=("m24", dict(view="shield", steps=[dict(state=dict(err="on")), dict(state=dict(r86="on"))],
                         rel=rr("r86"), note="発電所と盾は模式", src=ss.src(["S2 p1050"])))),
    # c820（2行）＝1986年の会議の机。1行目：止める棒の特徴が無い（空いた所）・1992年の報告／2行目：報告は違ったものに
    "c820": dict(
        t="明かされなかった特徴", s="会議に出なかった話",       # 🔧 門番 echo：「1986年の会議」は字幕の1行の切り取り
        fig=("m24", dict(view="table86", steps=[dict(state=dict(cards="on")), dict(state=dict(r92="on"))],
                         rel=rr("r92"), note="机と紙は模式", src=ss.src(["S1 p27"])))),
    # c822（2行）＝横から見た制御棒。1行目：いつも 1.2m 差しておく（炉の高さ 7m に比例）・1986年のソ連の報告／2行目：炉の下の方で強まるのを防ぐ
    "c822": dict(
        t="1.2メートル", s="対策の中の一文",
        fig=("m24", dict(view="rod12", steps=[dict(state=dict(ins="on")), dict(state=dict(why="on"))],
                         rel=[dict(t="1.2m", src="S3 p2028"), dict(t="高さ 7m", src="S1 p16")] + rr("s86"),
                         note="深さは炉の高さ 7m に比例（棒の数は模式）", src=ss.src(["S3 p2028", "S1 p16"])))),
    # c824（2行）＝1行目：止める棒の影（下は破線と「？」）／2行目：第8章の札・事故の山場
    "c824": dict(
        t="事故の山場へ", s="止める棒の形",
        fig=("m24", dict(view="rodq", steps=[dict(), dict(state=dict(next="on"))],
                         rel=[dict(t="第8章", src="台本 §4 第8章")], note="棒の影は模式", src=ss.src(["S1 p27"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-23）：写真と頁（第7章の14）＝c2.py の ⑤b-7 の塊と同じ書き方
#   ⚠️ 記者会見の3枚（c809・c811・c814）と会議の写真の副題は、試し焼きを原寸で見て書き分ける（映像方針 §6-3）。名札の名は語りが名指しするときだけ
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c801（3行・1行目は聞き役の問い）＝IAEA 02790045（ルイシコフ閣僚会議議長の視察＝語りが名指し・公人）＝額ごと右へ
    "c801": dict(photo=P("i45"), panel=True, color=1.0, fmove=ss.fm("r"), card_mix=0,     # 扉の地に混ぜない（BY-SA）
                 t="政府の動き", s="ルイシコフ閣僚会議議長の視察"),
    # c802（2行）＝IAEA 02790056（事故後検討会議の記者会見）＝額ごと寄る
    "c802": dict(photo=P("i56"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="原因の説明の場", s="事故後検討会議の記者会見（1986年8月・ウィーン）"),
    # c803（2行）＝IAEA 02790061（議長と IAEA 事務局長の席＝語りがブリクスの名札を名指し）＝額ごと左へ
    "c803": dict(photo=P("i61"), panel=True, color=1.0, fmove=ss.fm("l"),
                 t="集まった専門家", s="会議の議長と IAEA 事務局長の席（1986年8月）"),
    # c804（2行）＝IAEA 02790060（ソ連の専門家団の長の名札＝語りが名指し）＝額ごと上へ
    "c804": dict(photo=P("i60"), panel=True, color=1.0, fmove=ss.fm("u"),
                 t="説明した人", s="ソ連の専門家団の長の名札（1986年8月）"),
    # c805（3行・1行目は聞き役の問い）＝ソ連の報告 Part I p.26（第4章「CAUSES OF THE ACCIDENT」）の「The table below lists…」から表の頁の下まで
    "c805": dict(photo=P("s3p26"), trim=(0.004, 0.557, 0.998, 0.998), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="ソ連の説明", s="1986年のソ連の報告 第4章の違反の表"),
    # c807（2行）＝IAEA 02790058（会議のソ連側の席＝名札の名は副題に出さない）＝額ごと右へ
    "c807": dict(photo=P("i58"), panel=True, color=1.0, fmove=ss.fm("r"),
                 t="違反の動機", s="会議のソ連側の席（1986年8月）"),
    # c809（3行・1行目は聞き役の問い）＝IAEA 02790057（記者会見の別の1枚＝c811・c814 と副題を書き分ける）＝額ごと左へ
    "c809": dict(photo=P("i57"), panel=True, color=1.0, fmove=ss.fm("l"),
                 t="設計への言及", s="事故後検討会議の記者会見の別の1枚（1986年8月）"),
    # c811（3行・1行目は聞き役）＝IAEA 02790059（記者会見の壇上）＝額ごと寄る
    "c811": dict(photo=P("i59"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="1週間でまとめた報告", s="記者会見の壇上（1986年8月・ウィーン）"),
    # c812（2行）＝INSAG-1 p.18 の (5)（原因の文）から次の段落の「…disciplinary measures.」まで
    "c812": dict(photo=P("s2p18"), trim=(0.094, 0.210, 0.892, 0.550), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="原因の文", s="1986年の報告（INSAG-1）の要約の頁"),
    # c814（2行）＝IAEA 02790062（議長と事務局長の名札）＝額ごと上へ
    "c814": dict(photo=P("i62"), panel=True, color=1.0, fmove=ss.fm("u"),
                 t="もっともらしい説明", s="議長と事務局長の名札（1986年8月）"),
    # c818（2行・1行目は聞き役）＝IAEA 02790013（3・4号機の屋根での作業・人は小さい遠景＝c702 から移した）＝額ごと右へ
    "c818": dict(photo=P("i13"), panel=True, color=1.0, fmove=ss.fm("r"),
                 t="報告の重心", s="3・4号機の屋根での作業（1986年）"),
    # c819（3行）＝IAEA 02790040（事故のあとの溶接の作業）＝額ごと寄る
    "c819": dict(photo=P("i40"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="6年後の振り返り", s="事故のあとの溶接の作業"),
    # c821（2行）＝ソ連の報告 Part I p.28 の第5章の見出しから最初の段落の終わり（止める棒の下の端を 1.2m 差し込む改造）まで
    "c821": dict(photo=P("s3p28"), trim=(0.002, 0.087, 1.000, 0.658), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="対策の中の一文", s="1986年のソ連の報告の改造の計画の頁"),
    # c823（2行・1行目は聞き役）＝IAEA 02790048（遠隔操作の盤・操作員の名は言わない）＝額ごと左へ
    "c823": dict(photo=P("i48"), panel=True, color=1.0, fmove=ss.fm("l"),
                 t="原因の章に無い話", s="遠隔操作の盤"),
})
