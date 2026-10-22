# -*- coding: utf-8 -*-
"""第2章　延期された試験 c301–c317（17カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

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
    'c301': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：針の計器（出力の針・画面の時刻「1:06」）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.20／16（`at exactly 1:00 hours`）・S2 p.28／~25（`At 01:00 on 25 April`）・S1-表I-I p.63／53（`Start of reactor power reduction`）'),
    'c302': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：物差し（棒の本数＝30・26・15）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.89／79（`When the ORM falls to 15 rods, the reactor should be shut down immediately`）'),
    'c303': dict(kind='再現イラスト',
               plan='一覧の種類：時刻表｜見た目の型：時刻表（前半・案C3）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.89／79（`not less than 26-30 rods`）'),
    'c304': dict(kind='図・写真の頁',
               plan='🔧 S1p127｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告の図（出力の時間の変化）｜動き：寄る（上の図 II-3＝3200→1600 の線へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 付属書II の図 II-3・II-4｜注：🔧 実写 c3309（2013年の覆いの骨組み）→ 1992年の報告の図（語り＝4時前に1,600MW）。⚠️ 下の図 II-4（残した棒の数）は計算の線で、語りの「31本」〈表I-I〉と始まりの値が少し違う＝寄るのは上の図 II-3 だけ（⑤b で寄りの範囲を決める）。c3309 は ca13 へ｜新しい画（映像方針）：🔧 頁（INSAG-7 付属書II p.127／117 の図 II-3・II-4）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-表I-I p.63／53（`ORM equals 31`・`Reactor thermal power is 1600 MW`）'),
    'c305': dict(kind='文字の頁',
               plan='🔧 S1p63｜一覧の種類：頁｜見せ方：頁｜副題：1991年の委員会の表（INSAG-7 付属書I の表I-I）｜動き：寄る（7時10分の行へ）｜見た目の型：文字の頁（表）｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 付属書I 表I-I｜注：🔧 現在の4号炉-シ → 語りが「委員会の報告の表に…残っている」と名指しする表の頁｜新しい画（映像方針）：🔧 頁（表I-I p.63／53＝7:10 ORM 13.2 の行）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-表I-I p.63／53（`ORM equals 13.2 manual control rods`）'),
    'c306': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：線のグラフ（棒の数が15を下にくぐる）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`claim that this minimum ORM was also violated for several hours on 25 April`）'),
    'c307': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：機械（タービン2台）｜注：🔧 現在の4号炉-イ → 図。2013年のタービン建屋の写真は2013年2月の屋根の崩れ＝1986年の跡と取り違える＝使わない｜新しい画（映像方針）：🔧 模式（2台のタービン＝7号タービンを止める・試験に使う8号タービンだけが残る＝羽根の絵2つ・字は少なく）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.35／~32（`Turbo-generator No. 7 switched off`）'),
    'c308': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：管と弁（非常用の冷却）｜合図：🔁 上から→横から（前の図 c224）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-表I-I p.63／53（`Disconnection of the ECCS`）'),
    'c309': dict(kind='図・写真の頁',
               plan="🔧 GCp142｜一覧の種類：頁｜見せ方：頁｜副題：1986年の報告の図（非常用の冷却の仕組み）｜動き：寄る（水槽と弁へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：GC(SPL.I)/3＝INSAG-1 の Fig.11｜注：🔧 現在の4号炉-ウ → 語り「1986年の報告は…安全の原則に反するとした」＝その報告の非常用の冷却の図｜新しい画（映像方針）：🔧 頁（GC(SPL.I)/3＝INSAG-1 の Fig.11 Schematic drawing of the reactor's emergency cooling system）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）",
               src='S2 p.35／~32（`blocked ECCS played no role in transient to point of core disruption`・`ECCS remained isolated`）'),
    'c310': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：承認の印（手順書）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.20／10（`blocking of the ECCS was in fact permissible at Chernobyl if authorized`）'),
    'c311': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：時間の帯（冷却を切った時間）｜注：🔧 イメージ（Pexels）→ 図（発電所の中の配管の素材がフリー素材に無い）｜新しい画（映像方針）：🔧 模式（非常用の冷却を切っていた時間＝14:00 から 1:23 まで、およそ11時間の帯・「計画の外」の札・字は少なく）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.20／10（`which it clearly was not`・`are indicative of an absence of safety culture`・`This could be viewed as no violation only if`）'),
    'c312': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：3つの欄（報告ごとの見方）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.82／72（`taking the ECCS out of operation is a violation of Section 2.10.5`）・S1-付属書I p.88／78（`the switching off of the ECCS did not affect the initiation and scale`）'),
    'c313': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：札と×（引き金ではない）｜注：🔧 実写 c488（2006年の石棺）→ 図（§0-5）。c488 は ca17 へ｜新しい画（映像方針）：🔧 模式（「非常用の冷却を切った」の札が事故の引き金の印から外れる＝×・その横に「同じ午後2時 試験は延期」の札）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.88／78（`did not affect the initiation and scale of the accident`）'),
    'c314': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：矢印の流れ（キエフ→発電所）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-表I-I p.63／53（`Postponement of testing programme requested by Kiev power grid controller`）'),
    'c315': dict(kind='写真',
               plan='🔧 関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）｜LENW｜一覧の種類：参考｜見せ方：全面｜副題：同じ型の炉の発電所（レニングラード原発の3・4号機・2010年）｜動き：右へ｜権利：Public domain｜時期：他所｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／Public domain｜注：🔧 現在の4号炉-フ → 同じ型の炉の発電所の空撮（PD・壊れていない姿）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-表I-I p.63／53（`ORM equals 26`）'),
    'c316': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：時間の帯（延期）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.20／16（`At 23:10 hours, the power reduction was resumed`）・S2 p.28／~25（`not resumed until approximately 9 h later`）'),
    'c317': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：暦の札（日付の変わり目）｜注：🔧 現在の4号炉-エ → 図｜新しい画（映像方針）：🔧 模式（日付が変わる＝25日→26日の札・出力の針が下がりつつある）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-22）：案C3 出力の時刻表（前半）＝置き場 N3 view am（`tools/illu24.py`・門番 check_illu ㊵）
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c303（2行・9.6秒）＝1行目で 25日の札5つが左から順に（1:06 残した棒31本・3:47 1,600MW・7:10 13.2本・14:00 非常用の冷却と延期〈琥珀の印＝違反かは割れる〉・
    #   23:10 再開と26本）／2行目「ふだんは、少なくとも26本から30本は残す。15本まで減ったら、すぐ炉を止める」＝決まりの札と、残した棒の色（13.2本＝赤）
    "c303": dict(fig=("illu", dict(
        place="N3", start=dict(view="am"),
        steps=[dict(state=dict(n3a="on"), rec="S1 p63（表I-I＝25日の時刻と値）"),
               dict(state=dict(n3b="on"),
                    rec="S1 p89（not less than 26-30 rods・When the ORM falls to 15 rods, the reactor should be shut down immediately）")]))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。🔴 色は報告の色・画面の字の数は全部 rel に
#   🔴 c302 の目盛り（30・26・15）・c303 の時刻表（案C3）・c306 の線のグラフは別の絵（同じ値を同じ形で繰り返さない）
# ══════════════════════════════════════════════════════════
from mech24 import rr  # noqa: E402

SPEC.update({
    # c301（3行）＝1行目は聞き役の問い（針は右の端＝最大の出力）／2行目：4月25日 1:06・針が下がり始める（動く部品）／3行目：1986年の報告 1:00
    "c301": dict(
        t="出力を下げ始めた時刻", s="点検の前の準備",
        fig=("m24", dict(view="dial", steps=[dict(), dict(state=dict(clock="on")), dict(state=dict(r86="on"))],
                         rel=[dict(t="4月25日", src="S1 p63"), dict(t="1:06", src="S1 p63"), dict(t="1:00", src="S2 p1028")] + rr("r86"),
                         note="針の位置は模式（数は無い）", src=ss.src(["S1 p63", "S2 p1028", "S3 p2020"])))),
    # c302（2行）＝1行目：差したまま残す制御棒（深さはまちまち）／2行目：物差し「残した棒」（目盛り 30・26・15＝色は分けない＝決まりは c303）
    "c302": dict(
        t="「残した棒」という物差し", s="制御棒の数え方",
        fig=("m24", dict(view="ruler", steps=[dict(state=dict(rods="on")), dict(state=dict(scale="on"))],
                         rel=[dict(t="30・26・15", src="S1 p89")],
                         note="棒の数と深さは模式", src=ss.src(["S1 p89"])))),
    # c306（2行）＝1行目：15本の線と表I-I の点（1:06 31本・7:10 13.2本）・くぐる所を赤く／2行目：1992年の報告が引く新しい報告（何時間も）
    "c306": dict(
        t="前の日の朝にも", s="表の値と15本の線",
        fig=("m24", dict(view="orm", steps=[dict(state=dict(pts="on")), dict(state=dict(r92="on"))],
                         rel=[dict(t="15本", src="S1 p89"), dict(t="1:06 31本・7:10 13.2本", src="S1 p63"), dict(t="25日・26日", src="S1 p63")]
                         + rr("r92"),
                         note="点のあいだは直線（記録は表の点だけ）", src=ss.src(["S1 p63", "S1 p21"])))),
    # c307（2行）＝1行目：13:05 7号タービンを止める／2行目：試験に使う8号タービンだけ
    "c307": dict(
        t="2台のうち1台を止める", s="午後の切り替え",
        fig=("m24", dict(view="turbine", steps=[dict(state=dict(stop7="on")), dict(state=dict(keep8="on"))],
                         rel=[dict(t="7号・8号", src="S1 p63"), dict(t="13:05", src="S1 p63")],
                         note="タービンの形は模式", src=ss.src(["S1 p63", "S2 p1035"])))),
    # c308（2行）＝横から見た水の通り道（🔁 上から c224 → 横から）。1行目：非常用炉心冷却系と 14:00・右上の札②／2行目：弁を閉じて切り離す（×）
    "c308": dict(
        t="2つ目の「違反」", s="午後2時の操作",
        fig=("m24", dict(view="eccs", steps=[dict(state=dict(sys="on")), dict(state=dict(cut="on"))],
                         rel=[dict(t="14:00", src="S1 p63")],
                         note="槽・管・弁の形と数は模式", src=ss.src(["S1 p63"])))),
    # c310（3行）＝1行目は聞き役の問い（試験の手順の書類）／2行目：技師長の承認の印＋1992年の報告／3行目：承認された一歩（✓）
    "c310": dict(
        t="切ってよかったのか", s="承認と手順",
        fig=("m24", dict(view="stamp", steps=[dict(), dict(state=dict(stamp="on")), dict(state=dict(step="on"))],
                         rel=rr("r92"), note="書類の形と行は模式", src=ss.src(["S1 p20"])))),
    # c311（2行）＝1行目：14:00（25日）→ 事故（26日）約11時間・半分の出力・計画の外／2行目：1992年の報告「安全文化の欠け」
    "c311": dict(
        t="切りっぱなしの長さ", s="25日の午後から事故まで",
        fig=("m24", dict(view="off11", steps=[dict(state=dict(band="on")), dict(state=dict(r92="on"))],
                         rel=[dict(t="14:00", src="S1 p63"), dict(t="25日・26日", src="S1 p63"), dict(t="約11時間", src="S1 p20")] + rr("r92"),
                         note="帯の長さは時間に比例", src=ss.src(["S1 p20"])))),
    # c312（2行）＝1行目：違反か（1991年の委員会を太く）／2行目：割れる（黄の括弧）・どれも効いていない（緑の1枚）
    "c312": dict(
        t="割れる所と、そろう所", s="報告ごとの答え",
        fig=("m24", dict(view="grid3", steps=[dict(state=dict(row1="on")), dict(state=dict(row2="on"))],
                         rel=rr("r86", "c91", "r92"), note="札の言葉は要約", src=ss.src(["S2 p1035", "S1 p82", "S1 p88", "S1 p20"])))),
    # c313（2行）＝1行目：非常用の冷却を切った → 事故の引き金から外れる（×）／2行目：同じ 14:00 試験は延期
    "c313": dict(
        t="冷却を切ったことの重さ", s="午後2時のもう1つの出来事",
        fig=("m24", dict(view="trigger", steps=[dict(state=dict(cut="on")), dict(state=dict(post="on"))],
                         rel=[dict(t="14:00", src="S1 p63")], note="印の形は模式", src=ss.src(["S1 p88", "S1 p63"])))),
    # c314（2行）＝1行目：キエフの電力の指令所 → 4号炉「待って」／2行目：半分の出力のまま夜まで
    "c314": dict(
        t="待ってほしいという連絡", s="試験の延期の理由",
        fig=("m24", dict(view="kiev", steps=[dict(state=dict(ask="on")), dict(state=dict(night="on"))],
                         rel=[dict(t="4号炉", src="S1 p63")], note="建物の形は模式", src=ss.src(["S1 p63"])))),
    # c316（2行）＝1行目は聞き役（25日の24時間の輪）／2行目：14:00 → 23:10 の弧を赤く・約9時間
    "c316": dict(
        t="延びた待ち時間", s="出力を下げる作業",
        fig=("m24", dict(view="ring", steps=[dict(), dict(state=dict(arc="on"))],
                         rel=[dict(t="4月25日", src="S1 p63"), dict(t="14:00・23:10", src="S1 p63"), dict(t="約9時間", src="S2 p1028")],
                         note="輪の角度は時刻に比例（上＝真夜中）", src=ss.src(["S1 p63", "S2 p1028"])))),
    # c317（2行）＝1行目：4月25日・出力をゆっくり下げながら真夜中へ／2行目：4月26日・日付が変わってすぐ急に落ちる（？＝数は c402・c403）
    "c317": dict(
        t="その夜の入り口", s="25日から26日へ",
        fig=("m24", dict(view="day", steps=[dict(state=dict(d25="on")), dict(state=dict(d26="on"))],
                         rel=[dict(t="4月25日・26日", src="S1 p63")], note="出力の線は模式（数は無い）", src=ss.src(["S1 p63"])))),
})
