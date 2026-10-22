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
