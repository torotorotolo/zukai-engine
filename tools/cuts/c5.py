# -*- coding: utf-8 -*-
"""第4章　外された保護 c501–c517（17カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

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
    'c501': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：保護の仕組み（危ない値→自動で止める）｜注：🔧 実写 c496（2016年の吹雪の石棺）→ 図（§0-5）。c496 は ca18 へ｜新しい画（映像方針）：🔧 模式（保護とは＝危ない値になったら自動で炉を止める＝計器→止める信号→棒の流れ・字は少なく）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.27／~24（`This series of wilful violations of procedure`）'),
    'c502': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：筒（蒸気ドラム）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.17／7（`two parallel horizontal drum type separators in each loop`）'),
    'c503': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：保護の計器（水位と圧力）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.25／~22（`again a serious violation of normal station procedure`）'),
    'c504': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：2つの段（ドラムの保護）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.22／12（`as early as 00:36 on April 26 and not at 01:19:00 as stated`）・S1 p.22／12（`protection at the lower steam drum level remained effective throughout the event`）・S1-表I-I p.64／54（`The EPS trip point in response to a pressure drop in the steam separator drums was changed`）'),
    'c505': dict(kind='写真',
               plan='🔧 関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）｜R09｜一覧の種類：参考｜見せ方：額装（BY-SA）｜副題：同じ型の炉の原子炉の建屋（レニングラード原発・2008年）｜動き：額ごと上へ｜権利：CC BY-SA 3.0｜時期：他所｜人：遠景｜出典の行：RIA Novosti archive（CC BY-SA 3.0）・撮影者は作者欄のとおり｜注：🔧 現在の4号炉-カ → 同じ型の炉の原子炉の建屋（縦長・c309 から移した）。責める行＝職員は遠景で顔が判らない｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.22／12（`technically in violation of Item 9`）・S1-付属書I p.85／75（`These personnel actions were in violation of Section 9`）・S1-付属書I p.88／78（`were not the causes of the accident and did not affect its scale`）'),
    'c506': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：2つの印（形の上の違反・保護は効いた）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.28／18（`Disabling of the trip on steam drum water level would have been allowable`）'),
    'c507': dict(kind='図解',
               plan='一覧の種類：流れ｜見た目の型：流れ図（タービン→保護）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.39／~36（`two TGs-trip signal`）・S3 p.27／23（`Blocking of reactor protection system relying on shutdown signal from two turbogenerators`）'),
    'c508': dict(kind='文字の頁',
               plan='S2p39｜一覧の種類：頁｜見せ方：頁｜副題：1986年の報告（INSAG-1）の表｜動き：寄る（「保護が働けば炉は救われた」の行へ）｜見た目の型：文字の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：GC(SPL.I)/3＝INSAG-1 の本文｜注：台本どおり＝語りが名指しする所｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.39／~36（`This trip would have saved the reactor.`）'),
    'c509': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：やり直し（タービン2台を止めたまま）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.27／23（`Intention, if necessary, of repeating the experiment with turbogenerators switched off`）'),
    'c510': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：時刻の書き直し（×と印）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`The event occurred at 00:43:27 rather than at 01:23:04 as stated in INSAG-1`）'),
    'c511': dict(kind='写真',
               plan='🔧 関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）｜R96｜一覧の種類：参考｜見せ方：額装（BY-SA）｜副題：同じ型の炉の上で働く職員（クルスク原発・2008年）｜動き：額ごと寄る｜権利：CC BY-SA 3.0｜時期：他所｜人：背中｜出典の行：RIA Novosti archive（CC BY-SA 3.0）・撮影者は作者欄のとおり｜注：🔧 現在の4号炉-キ → 同じ型の炉の上（棒の頭が並ぶ床・c304 から移した）。職員は1人で背中（顔はヘルメットで隠れる）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`does not sup-port the apportionment of any blame to operating personnel`）'),
    'c512': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：棒の影（成り立たない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`seems not to be valid`）'),
    'c513': dict(kind='文字の頁',
               plan='S1p28｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告（INSAG-7）5.2.1 の頁｜動き：寄る（語りの行へ）｜見た目の型：文字の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7｜注：台本どおり＝語りが名指しする所（承認①で使う）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.28／18（`the occurrence of this trip might well have caused the destruction of the reactor`）'),
    'c514': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：天秤（運転員にも甘くない）｜注：🔧 イメージ（Pexels）→ 図（責める行）｜新しい画（映像方針）：🔧 模式（1992年の報告の天秤＝保護の話は運転員の側を軽く・ただし「運転員にも甘くない」の札が反対の皿に）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'c515': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：札（手順書と運転員）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.28／18（`disabling of reactor protection seems to have been regarded rather lightly`）'),
    'c516': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：出力の書き直し（700に×・200）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.29／19（`When the reactor power could not be restored to the intended level of 700 MW(th)`）・S1 p.29／19（`on the spot they modified the test conditions`）'),
    'c517': dict(kind='写真',
               plan='🔧 SEL｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：制御棒の位置を示す計器（1号機・2014年）｜動き：額ごと寄る｜権利：CC BY-SA 4.0｜時期：今・中｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：🔧 イメージ Pexels 30560421 → 「炉に残した、制御棒の数」＝棒の位置の計器（人なし）。30560421 は cc20 へ｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。🔴 色は報告の色・画面の字の数は全部 rel に
#   🔴 ドラムの保護の時刻は台本 §1-5＝1:19（1986年の報告・c503）／0:36（1991年の委員会の表＝圧力の保護の設定・c504）。
#      水位の設定の「形の上の違反・原因ではない」は c505（写真）の語り＝c506 の印は前のカットの続き。タービンの保護は 0時43分ごろ（秒は出さない）
# ══════════════════════════════════════════════════════════
from mech24 import rr  # noqa: E402

SPEC.update({
    # c501（3行）＝1行目は聞き役（保護の絵の基図）／2行目：残る2つの「違反」（⑤⑥の札）／3行目：危ない値 → 止める信号 → 棒が落ちる
    "c501": dict(
        t="炉を止める保護", s="残る2つの「違反」",
        fig=("m24", dict(view="guard", steps=[dict(), dict(state=dict(two="on")), dict(state=dict(auto="on"))],
                         rel=[], note="保護の絵は模式（計器と棒の数は模式）", src=ss.src(["S2 p1027"])))),
    # c502（2行）＝横から見た蒸気ドラム。1行目：1つのドラム（上が蒸気・下が水）／2行目：左右の系統に2つずつ・蒸気はタービンへ・水は炉へ
    "c502": dict(
        t="蒸気と水を分ける筒", s="炉とタービンのあいだ",
        fig=("m24", dict(view="drum", steps=[dict(state=dict(sep="on")), dict(state=dict(loop="on"))],
                         rel=[dict(t="2つずつ", src="S1 p17")], note="形と大きさは模式（数は記録）", src=ss.src(["S1 p17"])))),
    # c503（2行）＝右上の札⑤。1行目：1986年の報告「保護を外した」／2行目：1:19・線に×・重い違反
    "c503": dict(
        t="5つ目の「違反」", s="ドラムの2つの計器",          # 🔧 門番 echo：「ドラムの水位と圧力」は字幕の1行の切り取り
        fig=("m24", dict(view="drumtrip", steps=[dict(state=dict(r86="on")), dict(state=dict(off="on"))],
                         rel=[dict(t="1:19", src="S1 p22")] + rr("r86"), note="計器の形は模式（札の言葉は要約）",
                         src=ss.src(["S2 p1025", "S1 p22"])))),
    # c504（2行）＝ドラムの断面。1行目：1991年の委員会の表 0:36 圧力の保護の設定を変える／2行目：水位の保護の2つの段・下の段は最後まで効いた
    "c504": dict(
        t="もっと早い時刻", s="水位の保護の段",
        fig=("m24", dict(view="stage2", steps=[dict(state=dict(p036="on")), dict(state=dict(lv2="on"))],
                         rel=[dict(t="0:36", src="S1 p64")] + rr("c91"), note="ドラムの断面と段の高さは模式",
                         src=ss.src(["S1 p64", "S1 p22"])))),
    # c506（3行）＝1行目は聞き役（⑤の札と2つの印）／2行目：1992年の報告「外すことは許されたはず」／3行目：実際は外されず
    "c506": dict(
        t="外されなかった保護", s="ドラムの水位",
        fig=("m24", dict(view="marks5", steps=[dict(), dict(state=dict(ok92="on")), dict(state=dict(notdone="on"))],
                         rel=rr("r92"), note="札の言葉は要約", src=ss.src(["S1 p28", "S1 p88"])))),
    # c507（2行）＝右上の札⑥。1行目：2台のタービンが止まる → 止める信号 → 炉も止まる（上から下）／2行目：1986年の報告 1:23:04 に外した
    "c507": dict(
        t="6つ目の「違反」", s="2台のタービンと炉",
        fig=("m24", dict(view="tg2", steps=[dict(state=dict(flow="on")), dict(state=dict(r86="on"))],
                         rel=[dict(t="2台", src="S3 p2027"), dict(t="1:23:04", src="S1 p21")] + rr("r86"), note="流れの絵は模式",
                         src=ss.src(["S2 p1039", "S3 p2027", "S1 p21"])))),
    # c509（2行）＝1行目は聞き役（⑥ の札に×）／2行目：1986年のソ連の報告「必要なら、やり直す」＝2台を止めたまま・輪の矢印
    "c509": dict(
        t="外した理由", s="試験のくり返し",
        fig=("m24", dict(view="retry", steps=[dict(), dict(state=dict(s86="on"))],
                         rel=[dict(t="2台", src="S3 p2027")] + rr("s86"), note="タービンの絵は模式", src=ss.src(["S3 p2027"])))),
    # c510（2行）＝夜の時刻の線。1行目：1:23:04（1986年の報告）→ 0時43分ごろ（1992年の報告）／2行目：運転の手順と試験の手順に沿っていた
    "c510": dict(
        t="書き直された時刻", s="タービンの保護",
        fig=("m24", dict(view="shift", steps=[dict(state=dict(move="on")), dict(state=dict(proc="on"))],
                         rel=[dict(t="0時・1時", src="S1 p21"), dict(t="1:23:04", src="S1 p21"), dict(t="0時43分ごろ", src="S1 p21")] + rr("r86", "r92"),
                         note="時刻の線は時間に比例", src=ss.src(["S1 p21"])))),
    # c512（2行）＝1行目：1986年の報告の札「保護が働けば救われた」と1992年の報告／2行目：止める棒の影・成り立たないようだ
    "c512": dict(
        t="炉は救われたのか", s="棒の問題との関係",          # 🔧 門番 dup：図の札「止める棒」と同じ語
        fig=("m24", dict(view="shadow", steps=[dict(state=dict(card="on")), dict(state=dict(shade="on"))],
                         rel=rr("r86", "r92"), note="棒の影は模式（札の言葉は要約）", src=ss.src(["S2 p1039", "S1 p21"])))),
    # c514（2行）＝1992年の報告の天秤（板と支点）。1行目は聞き役（左＝この保護の件は運転員を責めない）／2行目：右＝運転員にも甘くない
    "c514": dict(
        t="運転員への見方", s="保護の件とその先",
        fig=("m24", dict(view="seesaw", start=dict(left="on"), steps=[dict(), dict(state=dict(right="on"))],
                         rel=rr("r92"), note="天秤は水平（札の言葉は要約）", src=ss.src(["S1 p21", "S1 p28"])))),
    # c515（2行）＝1行目：運転の手順と運転員の側の両方で「保護を外す」が軽い（破線・羽）／2行目：1992年の報告「どちらも軽く見ていた」
    "c515": dict(
        t="軽く扱われた操作", s="手順書と運転員",
        fig=("m24", dict(view="light", steps=[dict(state=dict(both="on")), dict(state=dict(r92="on"))],
                         rel=rr("r92"), note="書類と制御盤の形は模式", src=ss.src(["S1 p28"])))),
    # c516（2行）＝縦の出力の目盛り。1行目：予定 700MW に戻せず 200MW で止まる・その場で変更／2行目：200MW のまま試験へ
    "c516": dict(
        t="200メガワットの試験", s="その場の変更",
        fig=("m24", dict(view="test200", steps=[dict(state=dict(stuck="on")), dict(state=dict(go="on"))],
                         rel=[dict(t="0・200・700", src="S1 p29")], note="出力の高さは値に比例", src=ss.src(["S1 p29"])))),
})
