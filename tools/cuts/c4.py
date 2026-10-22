# -*- coding: utf-8 -*-
"""第3章　0時28分 c401–c421（21カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

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
    'c401': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：針の計器（0:05 の 720MW）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-表I-I p.63／53（`Reactor thermal power was 720 MW`）・S3 p.20／16（`was to be carried out at a reactor power of 700-1000 MW(th)`）・S2 p.28／~25（`reduction of power to between 700 and 1000 MW(th)`）'),
    'c402': dict(kind='図解',
               plan='一覧の種類：時計｜見た目の型：時計（0:28）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`the precipitous fall in power to 30 MW(th) as being due to an operator error`）'),
    'c403': dict(kind='再現イラスト',
               plan='一覧の種類：時刻表｜見た目の型：時刻表（後半・案C3）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.20／16（`the power fell below 30 MW(th)`）'),
    'c404': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：札（3つ目の違反＝1986年の報告の言い方）｜注：🔧 実写 NASA 2018（宇宙から＝新しい覆い）→ 図（§0-5）。NASA は c904 へ｜新しい画（映像方針）：🔧 模式（3つ目の札「0時28分の急落」に1986年の報告の言い方＝「出力を保つ指示を入れなかった」の札・字は少なく）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src="S2 p.36／~33（`Operator error with transfer`）・S2 p.28／~25（`a 'hold power' request was not entered`）"),
    'c405': dict(kind='写真',
               plan='🔧 CR3B｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：3号機の制御室（2021年）｜動き：額ごと左へ｜権利：CC BY-SA 4.0｜時期：今・中｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：🔧 現在の4号炉-ヘ → 壊れていない3号機の制御室（人は写らない＝右下の端に服の一部だけ・顔なし）。責める行＝人の写真は置かない決まりに合う｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.20／16（`the operator was unable to eliminate the resultant unbalance`）'),
    'c406': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：札の入れ替え（1986→1992）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`Recent reports suggest that there was no operator error as such`）'),
    'c407': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：2つの札（確かめられない・保てなかった）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`refers to an unknown cause and inability to control the power`）'),
    'c408': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：封筒（私信）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`former Deputy Chief Engineer for Operations at the Chernobyl plant`・`in a private communication refers to the system not working properly`）'),
    'c409': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：書類の一行（本文の文に線）｜注：🔧 イメージ（Pexels）→ 図（責める行＝人の写真を置かない・フリー素材に発電所の中が無い）｜新しい画（映像方針）：🔧 模式（1991年の委員会の報告の本文の1行＝「上級の運転員が素早く直せなかった」に線・字は少なく・頁の絵は使わない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.73／63（`failed to eliminate fast enough the imbalance`）'),
    'c410': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：3つの言い方（札の並び）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`no operator error as such`）'),
    'c411': dict(kind='図・写真の頁',
               plan='🔧 S1p128｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告の図（キセノンがたまるあいだの、炉の高さごとの中性子）｜動き：寄る（図 II-5 へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 付属書II の図 II-5｜注：🔧 現在の4号炉-ホ → 語り＝キセノン＝図の題に「xenon transient」｜新しい画（映像方針）：🔧 頁（INSAG-7 付属書II p.128／118 の図 II-5＝0:00・7:00・22:00・24:30 の4本の線）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.20／16（`stabilizing it at 200 MW(th)`）'),
    'c412': dict(kind='図解',
               plan='一覧の種類：棒｜見た目の型：棒グラフ（熱出力）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.25／~22（`continuous operation below 700 MW(th) is forbidden by normal safety procedures`）'),
    'c413': dict(kind='写真',
               plan='🔧 関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）｜R94｜一覧の種類：参考｜見せ方：額装（BY-SA）｜副題：同じ型の炉の上を見る職員（レニングラード原発・2011年）｜動き：額ごと右へ｜権利：CC BY-SA 3.0｜時期：他所｜人：背中｜出典の行：RIA Novosti archive（CC BY-SA 3.0）・撮影者は作者欄のとおり｜注：🔧 現在の4号炉-オ → 同じ型の炉（職員は後ろ姿・顔なし）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`was not proscribed, either in design, in regula-tory limitations or in operating instructions`）'),
    'c414': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：頁の札（強調は当たらない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.21／11（`The emphasis placed on this statement in INSAG-1 was not warranted.`）・S1 p.20／10（`was based on oral statements made by Soviet experts`）'),
    'c415': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：線（あとで決まった下限）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.28／18（`There should have been such a proscription, but there was none at the time.`）・S1 p.38／28（`sets a lower limit of 700 MW(th) for steady operation`）'),
    'c416': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：3つの欄（設計・規制・指示書）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.87／77（`there were no safe operating limits in terms of minimum permissible thermal reactor power`）'),
    'c417': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：計器（炉の中と外・上と下が見えない）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.15／5（`they were all located at the mid-plane of the core`・`a reactor operator had to rely mainly on experience and intuition`）'),
    'c418': dict(kind='写真',
               plan='🔧 I35｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：炉心の見取り盤の前の運転員｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：前｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：🔧 現在の4号炉-マ → c207 から移した（語り＝1時間に1,000回の操作＝運転の手間・責める行でない）。何号機の制御室かは記録に無い＝名乗らない｜⑤b-2（10-22）：年は原文に無い＝外した。⚠️ 説明は c213 と同じ「…worked around the clock」＝事故のあとかもしれない（⑤b-7 で）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.15／5（`perform manipulations at a rate of up to 1000 per hour`）'),
    'c419': dict(kind='図・写真の頁',
               plan='🔧 GCp140｜一覧の種類：頁｜見せ方：頁｜副題：1986年の報告の図（2つの系統と8台の循環ポンプ）｜動き：寄る（循環ポンプの列へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：GC(SPL.I)/3＝INSAG-1 の Fig.9｜注：🔧 模式（ポンプ8台）→ 1986年の報告の系統図（語り＝ポンプが8台とも動いていた）｜新しい画（映像方針）：🔧 頁（GC(SPL.I)/3＝INSAG-1 の Fig.9＝Loop 1・Loop 2 に4台ずつの Circulation Pumps・Turbine 7＋8）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.74／64（`eight instead of the usual six MCPs were in operation`）'),
    'c420': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：温度計（入口の水）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.18／8（`The use of all eight pumps increased the coolant flow rate above that under nominal`・`owing to the lower reactor power level at that time`）'),
    'c421': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：2つの札（違反／暴走を妨げたかも）｜注：🔧 現在の4号炉-ヒ → 図｜新しい画（映像方針）：🔧 模式（1991年の委員会の2つの見方＝一部のポンプの流れすぎは違反・8台のポンプはむしろ暴走を妨げたかもしれない＝2つの札）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.88／78（`if anything hindered the reactor runaway`）・S1-付属書I p.87／77（`the flow rates of certain MCPs actually exceeded the limit`）'),
}

SPEC = {}
