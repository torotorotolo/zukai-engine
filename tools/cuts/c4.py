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
               plan='🔧 CR4B:左の盤｜一覧の種類：実写｜見せ方：額装（小さい）｜副題：4号機の制御室の盤（2025年）｜動き：額の中で寄る｜権利：CC0｜時期：今・中｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC0｜注：🔧 ⑤b-7（10-23）：I35（見取り盤の前の運転員）→ 4号機の制御室の左の盤（CC0・学生の左の 0〜0.355 だけを切り出す＝学生は写らない・語り＝1時間に1,000回の操作）。I35 は c213 の I34 と同じ説明「…worked around the clock」＝事故のあとの見込みが高い＝爆発の前の章に置かない → cc03 へ｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
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

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-22）：案C3 出力の時刻表（後半）＝置き場 N3 view night（`tools/illu24.py`・門番 check_illu ㊵）
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c403（3行・9.2秒・3行目は聞き役の問い）＝頭に 0:05 720MW と、200MW で止まった時刻の割れ（1:00 ソ連の報告／1:03 INSAG-7 の表＝同じ形の目盛りに
    #   出典の名だけ・時刻の字は出さない＝台本 §1-5）／1行目「およそ500メガワットから、30メガワットを下回るところまで」＝0:28 の札と赤い下向きの矢印／
    #   2行目「試験の予定の、20分の1よりも低い出力である」＝試験の予定の札
    "c403": dict(fig=("illu", dict(
        place="N3", start=dict(view="night", n3a="on"),
        rec="S1 p63（00:05 Reactor thermal power was 720 MW）・S3 p2020（Only at 1:00 on 26 April）・S1 p64（01.03 Reactor thermal power increased to 200 MW）",
        steps=[dict(state=dict(n3b="on"),
                    rec="S1 p63（00:28 At reactor thermal power of about 500 MW transfer made）・S3 p2020（the power fell below 30 MW(th)）"),
               dict(state=dict(n3c="on"), rec="S3 p2020（was to be carried out at a reactor power of 700-1000 MW(th)）"),
               dict()]))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。🔴 色は報告の色・画面の字の数は全部 rel に
#   🔴 200MW で止まった時刻は「1時ごろ」（1:00 と 1:03 で割れる＝台本 §1-5）・「700MW 未満は禁止だった」と地の札で言わない（帰属つきの札だけ）
# ══════════════════════════════════════════════════════════
from mech24 import rr  # noqa: E402

SPEC.update({
    # c401（3行）＝1行目は聞き役の問い（目盛り 0〜3,200MW）／2行目：4月26日 0:05 の針 720MW／3行目：試験の予定 700〜1,000MW の帯（炉が出す熱）
    "c401": dict(
        t="予定の出力の帯", s="炉の熱の出力",
        fig=("m24", dict(view="meter", steps=[dict(), dict(state=dict(ptr="on")), dict(state=dict(plan="on"))],
                         rel=[dict(t="0・3,200", src="S2 p1008"), dict(t="720", src="S1 p63"), dict(t="4月26日", src="S1 p63"),
                              dict(t="0:05", src="S1 p63"), dict(t="700・1,000", src="S3 p2020")],
                         note="目盛りは出力に比例", src=ss.src(["S1 p63", "S3 p2020"])))),
    # c402（2行）＝時計 0:28。1行目：切り替え（炉の部分ごと → 全体をまとめて）／2行目：一気に落ちる（赤い矢印）
    "c402": dict(
        t="0時28分の操作", s="炉の自動の制御",       # 🔧 門番 dup：「切り替えの瞬間」を左上の札と注が71%覆った
        fig=("m24", dict(view="clock", steps=[dict(state=dict(sw="on")), dict(state=dict(drop="on"))],
                         rel=[dict(t="0:28", src="S1 p63")], note="絵は模式", src=ss.src(["S1 p63", "S1 p21"])))),
    # c404（2行）＝右上の札③。1行目：1986年の報告「運転員の誤り」／2行目：出力を保つ指示を、切り替えのときに入れなかった
    "c404": dict(
        t="3つ目の「違反」", s="事故の年の見方",
        fig=("m24", dict(view="hold", steps=[dict(state=dict(r86="on")), dict(state=dict(cmd="on"))],
                         rel=[dict(t="0時28分", src="S1 p63")] + rr("r86"), note="札の言葉は要約", src=ss.src(["S2 p1036", "S2 p1028"])))),
    # c406（2行）＝1行目：1986年の報告「運転員の誤り」／2行目：書き直し → 1992年の報告「誤りと言えるもの：無かったようだ」
    "c406": dict(
        t="書き直された見方", s="0時28分の急落について",
        fig=("m24", dict(view="swap", steps=[dict(state=dict(r86="on")), dict(state=dict(r92="on"))],
                         rel=rr("r86", "r92"), note="札の言葉は要約", src=ss.src(["S1 p21"])))),
    # c407（2行）＝1991年の委員会の見方（S1 p21 が引く）。1行目：原因＝確かめられない／2行目：出力＝保てなかった
    "c407": dict(
        t="委員会が書いたこと", s="原因と出力",
        fig=("m24", dict(view="two91", steps=[dict(state=dict(cause="on")), dict(state=dict(ctrl="on"))],
                         rel=rr("c91"), note="札の言葉は要約", src=ss.src(["S1 p21"])))),
    # c408（2行）＝1行目：私信の封筒（運転担当の元副技師長から）／2行目：開いた手紙「自動の仕組み 正しく働かなかった」＋1992年の報告の札
    "c408": dict(
        t="発電所の中からの声", s="私信の中身",
        fig=("m24", dict(view="letter", steps=[dict(state=dict(env="on")), dict(state=dict(open="on"))],
                         rel=rr("r92"), note="封筒と手紙の形は模式", src=ss.src(["S1 p21"])))),
    # c409（2行）＝1991年の委員会の報告の本文（模式）。1行目：1行に赤い下線「上級の運転員が 素早く直せず」／2行目：同じ報告に2つの言い方
    "c409": dict(
        t="同じ報告の別の一文", s="運転員について",
        fig=("m24", dict(view="docline", steps=[dict(state=dict(hl="on")), dict(state=dict(two="on"))],
                         rel=rr("c91") + [dict(t="2つの言い方", src="S1 p73")], note="頁の形と行は模式", src=ss.src(["S1 p73", "S1 p21"])))),
    # c410（3行）＝1行目：同じ急落に3つの言い方／2行目：出力は 200MW まで戻って止まる（1時ごろ）／3行目：それ以上は上がらない
    "c410": dict(
        t="割れたままの見方", s="急落のあとの出力",
        fig=("m24", dict(view="say3", steps=[dict(state=dict(cards="on")), dict(state=dict(p200="on")), dict(state=dict(cap="on"))],
                         rel=rr("r86", "c91") + [dict(t="0時28分", src="S1 p63"), dict(t="1時ごろ・200", src="S3 p2020")],
                         note="出力の線は模式", src=ss.src(["S1 p21", "S1 p73", "S3 p2020", "S1 p64"])))),
    # c412（2行）＝右上の札④。1行目：熱出力の棒（同じ縮尺）と 700MW の線／2行目：1986年の報告「ふだんの安全の手順で禁止」（帰属つき）
    "c412": dict(
        t="4つ目の「違反」", s="同じ物差しで見る出力",
        fig=("m24", dict(view="bars", steps=[dict(state=dict(bars="on")), dict(state=dict(r86="on"))],
                         rel=[dict(t="3,200", src="S2 p1008"), dict(t="25日 4時前 1,600", src="S1 p63"), dict(t="700", src="S2 p1025"),
                              dict(t="1時ごろ 200", src="S3 p2020"), dict(t="0時28分 30", src="S1 p63")] + rr("r86"),
                         note="棒の長さは出力に比例", src=ss.src(["S2 p1025", "S2 p1008", "S1 p63", "S3 p2020"])))),
    # c414（2行）＝1行目：口頭の説明（ソ連の専門家）→ 1986年の報告の頁の「禁止」の強調／2行目：1992年の報告「強調は当たらない」
    "c414": dict(
        t="強く書きすぎた一語", s="書き方の根拠",
        fig=("m24", dict(view="page86", steps=[dict(state=dict(oral="on")), dict(state=dict(r92="on"))],
                         rel=rr("r86", "r92"), note="頁の形は模式（頁の絵は使わない）", src=ss.src(["S1 p21", "S1 p20"])))),
    # c415（2行）＝1行目：1992年の報告「禁止は、あるべきだった」／2行目：事故のあと＝700MW の線（ふだんの運転の下限）
    "c415": dict(
        t="事故のあとに引いた線", s="700メガワットの線",
        fig=("m24", dict(view="limit", steps=[dict(state=dict(r92="on")), dict(state=dict(after="on"))],
                         rel=rr("r92") + [dict(t="700", src="S1 p38")], note="線の高さは出力に比例（模式）", src=ss.src(["S1 p28", "S1 p38"])))),
    # c416（2行）＝1行目は聞き役（3つの書類＝どれにも禁止の項目なし）／2行目：1991年の委員会も、事故の前は同じ見方
    "c416": dict(
        t="どこにも無かった禁止", s="設計・規制・指示書",
        fig=("m24", dict(view="pillars", steps=[dict(), dict(state=dict(c91="on"))],
                         rel=rr("c91"), note="書類の形は模式", src=ss.src(["S1 p87", "S1 p21"])))),
    # c417（2行）＝横から見た炉と計器（🔁 前の図は上下の向きなし）。1行目：炉の中の計器＝使えない・外の計器＝真ん中の高さ／2行目：上と下は見えない・経験と勘
    "c417": dict(
        t="手さぐりの運転", s="炉の計器の高さ",
        fig=("m24", dict(view="inst", steps=[dict(state=dict(det="on")), dict(state=dict(blind="on"))],
                         rel=rr("r92"), note="計器の数と位置は模式", src=ss.src(["S1 p15"])))),
    # c420（2行）＝温度計（模式）。1行目：出力が低い＋水の流れが増える（ポンプ8台）→ 沸く寸前／2行目：1992年の報告「事故の条件の1つ」
    "c420": dict(
        t="ぎりぎりの水", s="出力とポンプの組み合わせ",
        fig=("m24", dict(view="thermo", steps=[dict(state=dict(rise="on")), dict(state=dict(r92="on"))],
                         rel=[dict(t="ポンプ8台", src="S1 p74")] + rr("r92"), note="温度計の目盛りは模式（数は無い）", src=ss.src(["S1 p18", "S1 p74"])))),
    # c421（3行）＝1991年の委員会の天秤。1行目：一部のポンプ＝流れすぎ＝違反／2行目：8台のポンプ＝暴走を妨げたかも／3行目：見方は割れる
    "c421": dict(
        t="ポンプ8台の評価", s="違反か、助けか",
        fig=("m24", dict(view="balance", steps=[dict(state=dict(left="on")), dict(state=dict(right="on")), dict(state=dict(split="on"))],
                         rel=rr("c91") + [dict(t="8台", src="S1 p88")], note="天秤は水平（どちらにも寄せない）", src=ss.src(["S1 p87", "S1 p88"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-23）：写真と頁（第3章の5）＝c2.py の ⑤b-7 の塊と同じ書き方
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c405（2行・責める行＝人の写らない写真）＝CR3B（3号機の制御室・2021年・右下の端に服の一部だけ）＝額ごと左へ
    "c405": dict(photo=P("cr3b"), panel=True, color=1.0, fmove=ss.fm("l"),
                 t="ソ連の報告の見方", s="3号機の制御室（2021年）"),
    # c411（2行）＝INSAG-7 付属書II の図 II-5（キセノンがたまるあいだの炉の高さごとの中性子）＝図の題の下まで
    "c411": dict(photo=P("s1p128"), trim=(0.000, 0.019, 1.000, 0.512), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="上がらない出力", s="1992年の報告の図（キセノンがたまるあいだの、炉の高さごとの中性子）"),
    # c413（2行）＝R94（同じ型の炉の上を見る職員・背中＝顔なし・参考）＝額ごと右へ
    "c413": dict(photo=P("r94"), panel=True, color=1.0, fmove=ss.fm("r"),
                 t="書き直された点", s="同じ型の炉の上を見る職員（レニングラード原発・2011年）"),
    # c418（2行）＝🔧 CR4B の左の盤（4号機の制御室・CC0・学生の左だけを切り出した＝⑤b-7 に I35 から替えた）＝額の中で寄る
    "c418": dict(photo=P("cr4b2"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="手で合わせる運転", s="4号機の制御室の盤（2025年）"),
    # c419（3行）＝INSAG-1 の Fig. 9（2つの系統と8台の循環ポンプ・横長の頁）＝図の題の下まで
    "c419": dict(photo=P("gcp140"), trim=(0.038, 0.000, 1.000, 0.837), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="8台のポンプ", s="1986年の報告の図（2つの系統と8台の循環ポンプ）"),
})
