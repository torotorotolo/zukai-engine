# -*- coding: utf-8 -*-
"""第11章　石棺のその後 cc01–cc21（21カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

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
    'cc01': dict(kind='写真',
               plan='I50｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：石棺を据える準備（1986年）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.21／469（`construction of the sarcophagus (May-November 1986)`）'),
    'cc02': dict(kind='写真',
               plan='I18｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：ヘリコプターの乗員｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（名前は言わない）｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.31／27（`About 5000 t in all were dropped between 27 April and 10 May`）'),
    'cc03': dict(kind='写真',
               plan='🔧 I35｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：炉心の見取り盤の前の運転員｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：前｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：🔧 現在の4号炉-テ → また動き始めたほかの号機（3号機は2000年まで動いた）。⑤b-7（10-23）：CR3A → I35（炉心の見取り盤の前の運転員・事故の記録の組＝事故のあとの章に合う・語りに責める語なし・何号機かは記録に無い＝名乗らない）。CR3A は c213 へ｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.11／~6（`Units 1 and 2 were shut down early in the morning of 27 April`）・S3 p.32／28（`was shut down at 05.00 on 26 April`）'),
    'cc04': dict(kind='図解',
               plan='一覧の種類：帯｜見た目の型：帯（その後の年）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='WEB chnpp.gov.ua（「December 4, 1987 - post-accident commissioning of 3rd Power Unit.」）'),
    'cc05': dict(kind='写真',
               plan='🔧 C3｜一覧の種類：実写｜見せ方：全面｜副題：冷却水路と発電所（2013年）｜動き：右へ（パノラマを流す）｜権利：CC BY 2.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 2.0｜注：🔧 現在の4号炉-ト → 発電所のパノラマ（CC BY 2.0・横長）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='WEB chnpp.gov.ua（「Chornobyl NPP officially stopped generation of electricity on 15th of December, 2000.」）'),
    'cc06': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：段（INES の0〜7）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L10 p.12／1（`The scale was developed in 1990 by international experts convened by the IAEA`）・L10 p.13／2（`accident at the Chernobyl nuclear power plant is rated at Level 7 on INES.`）'),
    'cc07': dict(kind='写真',
               plan='🔧 C3305｜一覧の種類：実写｜見せ方：全面｜副題：記念碑と新しい覆い（2018年）｜動き：寄る｜権利：CC0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC0｜注：🔧 c3319 → c3305（語り＝いちばん重いレベル7）。c3319 は cc10 へ｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L10 p.163／152（`Major accident Level 7 Chernobyl, 1986.`）'),
    'cc08': dict(kind='図解',
               plan='一覧の種類：並べ｜見た目の型：並べ（7の段に2つ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='WEB 内閣府 防災白書 平成23年版（「４月１２日にはレベル７（広範囲な影響を伴う事故）に引き上げ」）'),
    'cc09': dict(kind='写真',
               plan='C3290｜一覧の種類：実写｜見せ方：全面｜副題：プリピャチの団地と新しい覆い（2018年）｜動き：右へ｜権利：CC0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC0｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'cc10': dict(kind='写真',
               plan='🔧 C3319｜一覧の種類：実写｜見せ方：全面｜副題：組み立て中の新しい覆い（2016年6月）｜動き：左へ｜権利：CC BY 2.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 2.0｜注：🔧 c3305 → c3319（語り＝離れた場所で組み立て・2016年11月にすべらせた）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='WEB EBRD 2016-11-29（「was moved over a distance of 327 metres from its assembly point to its final resting place」）'),
    'cc11': dict(kind='写真',
               plan='🔧 H01｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：冷却水路の先の新しい覆い（2018年）｜動き：額ごと寄る｜権利：CC BY-SA 4.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：🔧 イメージ（Pexels）→ 新しい覆いの写真（語り＝2019年に引き渡し）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='WEB chnpp.gov.ua（「On July 10, in the Exclusion Zone the NSC was officially handed-over from JV NOVARKA」）'),
    'cc12': dict(kind='写真',
               plan='🔧 H11｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：新しい覆い（2018年）｜動き：額ごと右へ｜権利：CC BY-SA 4.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：🔧 イメージ Pexels 30560422（観覧車）→ 新しい覆い（§0-5＝2022年・2025年の語りに観覧車を当てない・2025年に無人機が当たったのはこのアーチ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='WEB IAEA Update 38（World Nuclear News 2022-04-01 の写し）（「transferred control of Chernobyl nuclear power plant to Ukrainian personnel」）・WEB 国連ニュース 2025-02-14（「could see a breach of the outer layer of the NSC」）・WEB NucNet 2025-12-08＝IAEA の評価の写し（「lost its primary safety functions, including the confinement capability」）'),
    'cc13': dict(kind='図・写真の頁',
               plan='🔧 S1p138｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告の図（昔の棒と、改良した棒）｜動き：寄る（(c) 改良した棒へ）｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7 付属書II の図 II-13｜注：🔧 模式（改良・12秒）→ 1992年の報告の図（c903 の模式・c901 の図1 と別の絵＝改良の (c) に寄る）。12秒は語りだけ｜新しい画（映像方針）：🔧 頁（INSAG-7 付属書II p.138／128 の図 II-13＝(a) 昔の棒・(b) 入れておく昔の棒・(c) 改良した棒・寸法 cm）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.28／24（`as the rods move down from the upper stops`）・S1-図1 p.15／5（`(a) before and (b) after the improvements made in response to the Chernobyl accident`）・S1-付属書II p.135／125（`the manual control rods were replaced with ones of improved design`）'),
    'cc14': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：2つの段（国の段階と現場）｜注：🔧 現在の4号炉-ナ → 図（語り＝報告の結論の言い方）｜新しい画（映像方針）：🔧 模式（1992年の報告＝安全文化の欠け＝国の段階〈設計・運転・規制の組織〉と現場の2つの段に印・字は少なく）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.35／25（`lack of safety culture in nuclear matters, at the national level as well as locally`）・S1 p.33／23（`The accident can be said to have flowed from deficient safety culture`）'),
    'cc15': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：表と裏の札（時刻は同じ・意味が変わる）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'cc16': dict(kind='写真',
               plan='🔧 CR4B:上の盤｜一覧の種類：実写｜見せ方：額装（小さい）｜副題：4号機の制御室（2025年）｜動き：額の中で寄る｜権利：CC0｜時期：今・中｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC0｜注：🔧 現在の4号炉-ニ → 4号機の制御室（CC0＝学生の写らない左の盤だけ切り出す）。語り＝0時28分とボタンの意味の書き直し｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'cc17': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：天秤（人と設計）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`Most reprehensibly, unapproved changes in the test procedure were deliberately made`）・S1 p.26／16（`It is reprehensible that such a deficiency had been known of for so long`）'),
    'cc18': dict(kind='写真',
               plan='🔧 C0｜一覧の種類：実写｜見せ方：全面｜副題：4号機の石棺と排気筒（2008年）｜動き：右へ｜権利：CC BY 3.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 3.0｜注：🔧 現在の4号炉-ヌ → 4号機の石棺（CC BY 3.0・1600×1200＝全面で軽く流す）。c907 から移した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`laid blame almost entirely on actions of the operating staff, is thereby lessened`）'),
    'cc19': dict(kind='写真',
               plan='🔧 NSC17｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：4号機を覆った新しい覆い（2017年10月）｜動き：額ごと寄る｜権利：CC BY-SA 4.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：🔧 現在の4号炉-ネ → 新しい覆いの中の4号炉（語り＝いまも新しい覆いの中にある）。cc11 から移した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1（https://www-pub.iaea.org/MTCD/Publications/PDF/Pub913e_web.pdf）・S2（https://www.iaea.org/sites/default/files/gc/gc-spl1-3.pdf）'),
    'cc20': dict(kind='フリー素材',
               plan='🔧 X13188723:団地｜映像の素材 22.06秒・倍率 1.94（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のプリピャチ（Pexels）｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：🔧 場面で選ぶ → 30560421（c517 から移した・プリピャチの空撮）｜🔧 ⑤b-2（10-22）：30560421 は頁が Cloudflare の Turnstile（人の操作が要る）で取れない → 手元の X13188723（プリピャチの団地の空撮・覆いは写らない）の後ろの区間（c927 は前の区間）＝了承② の素材の内｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`laid blame almost entirely on actions of the operating staff, is thereby lessened`・`critical actions of the operators were most ill judged`）'),
    'cc21': dict(kind='パネル',
               plan='一覧の種類：文字だけ｜見た目の型：問い（パネル）｜注：台本どおり（問い A）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。
#   🔴 帯の相方 cc04＝号機ごとの月の帯（c706 の24時間の空の帯と別の絵）・並べの相方 cc08＝いちばん上の段に2つ（c918 の演台と別の絵）。
#   cc06 にチェルノブイリの印は付けない（次の写真のカット cc07 の語り）・cc15 は意味の中身を書かない（次の cc16 の語り）
# ══════════════════════════════════════════════════════════
from mech24 import rr  # noqa: E402

SPEC.update({
    # cc04（2行）＝1行目：1号機 1986年10月・2号機 11月・3号機 1987年12月に動き出す（月に比例）／2行目：4号炉のすぐ隣で発電は続いた（事業者の年表）
    "cc04": dict(
        t="再び動いた号機", s="壊れた炉の隣で",
        fig=("m24", dict(view="gantt", steps=[dict(state=dict(run="on")), dict(state=dict(next="on"))],
                         rel=[dict(t="1号機 1986年10月・2号機 11月・3号機 1987年12月", src="WEB 事業者の年表"), dict(t="4号炉", src="S2 p1008")],
                         note="帯の始まりは月に比例", src="事業者（チェルノブイリ原子力発電所）の年表"))),
    # cc06（2行）＝1行目：0から7の段（高さは段の数に比例）／2行目：INES・1990年にできた（L10）
    "cc06": dict(
        t="出来事の重さを測る", s="国際的な物差し",
        fig=("m24", dict(view="ines", steps=[dict(state=dict(steps="on")), dict(state=dict(name="on"))],
                         rel=[dict(t="0・1・2・3・4・5・6・7（段）", src="L10 pdf13"), dict(t="1990年", src="L10 pdf12")],
                         note="段の高さは数に比例（色は模式）", src="INES の手引き（IAEA・2008年）p.1・p.2"))),
    # cc08（2行）＝基図：レベル7の段とチェルノブイリ（1986年）／1行目：福島第一（2011年）／2行目：4月12日にレベル7へ引き上げ（防災白書）
    "cc08": dict(
        t="同じ段のもう1つ", s="2011年の事故",
        fig=("m24", dict(view="lvl7", steps=[dict(state=dict(fk="on")), dict(state=dict(up="on"))],
                         rel=[dict(t="レベル7", src="L10 pdf13"), dict(t="1986年", src="L10 pdf13"), dict(t="2011年・4月12日", src="WEB 防災白書 平成23年版")],
                         note="段と札は模式", src="内閣府 防災白書 平成23年版／INES の手引き（IAEA・2008年）p.2"))),
    # cc14（3行）＝1行目は聞き役（2つの段）／2行目：国の段階に「欠けていた」・1992年の報告／3行目：現場にも（S1 p35・p33）
    "cc14": dict(
        t="事故の根っこ", s="どの段の問題か",
        fig=("m24", dict(view="tiers", steps=[dict(), dict(state=dict(nat="on")), dict(state=dict(loc="on"))],
                         rel=rr("r92"), note="段は模式", src=ss.src(["S1 p35", "S1 p33"])))),
    # cc15（2行）＝1行目：0:28 と 1:23:40＝時刻は変わらない／2行目：札の裏＝意味が変わった（中身は次の cc16）
    "cc15": dict(
        t="読み直された時刻", s="事故の夜の2つ",
        fig=("m24", dict(view="flip", steps=[dict(state=dict(same="on")), dict(state=dict(mean="on"))],
                         rel=[dict(t="0:28", src="S1 p63"), dict(t="1:23:40", src="S1 p65")] + rr("r86", "r92"),
                         note="札の表と裏は模式", src=ss.src(["S1 p63", "S1 p65"])))),
    # cc17（3行）＝1行目は聞き役（空の皿）／2行目：承認なしに計画をわざと変えた・1992年の報告／3行目：棒の欠陥を長く残した・どちらも責められるべき（S1 p34・p26）
    "cc17": dict(
        t="人と設計の両方", s="報告の結び",
        fig=("m24", dict(view="tray", steps=[dict(), dict(state=dict(human="on")), dict(state=dict(design="on"))],
                         rel=rr("r92"), note="皿と札は模式", src=ss.src(["S1 p34", "S1 p26"])))),
})

# 🆕 2026-10-22（⑤b-1）：コメントの問い（承認①＝問い A・台本 §1-3）。字幕の配線（2行の字幕・y968／1044）を本編のカットで確かめるため
#    束の要らないパネルを先に書いた（23本目 ⑤b-1 の cd09 と同じ型）。パネルの字は字幕の文と12字以上重ねない（門番 echo）
SPEC.update({
    "cc21": dict(
        t="チェルノブイリの事故", s="コメント欄で聞かせてください",     # 「チェルノブイリ原発事故」は字幕の1文の切り取り（門番 echo）
        fig=("panel", dict(blocks=[dict(k="問い", t="事故の原因は何だと思っていましたか", v="見る前は", c=J.AMBER)], cols=1)),
    ),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-23）：写真・頁・映像（第11章の14）＝c2.py・c6.py の ⑤b-7 の塊と同じ書き方
# ══════════════════════════════════════════════════════════
_C3, _C3305, _C3290, _C3319, _C0 = P("c3"), P("c3305"), P("c3290"), P("c3319"), P("c0")
SPEC.update({
    # cc01（3行・1行目は聞き役の問い）＝IAEA 02790050（石棺を据える準備）＝額ごと寄る
    "cc01": dict(photo=P("i50"), panel=True, color=1.0, fmove=ss.fm("in"), card_mix=0,    # 扉の地に混ぜない（BY-SA）
                 t="壊れた炉のその後", s="石棺を据える準備（1986年）"),
    # cc02（2行）＝IAEA 02790018（ヘリコプターの乗員・名前は言わない）＝額ごと右へ
    "cc02": dict(photo=P("i18"), panel=True, color=1.0, fmove=ss.fm("r"),
                 t="空から落とした物", s="ヘリコプターの乗員"),
    # cc03（2行）＝🔧 IAEA 02790035（炉心の見取り盤の前の運転員＝⑤b-7 に c418 から移した・何号機かは名乗らない）＝額ごと左へ
    "cc03": dict(photo=P("i35"), panel=True, color=1.0, fmove=ss.fm("l"),
                 t="ほかの号機", s="炉心の見取り盤の前の運転員"),
    # cc05（2行）＝🔧 C3（冷却水路と発電所のパノラマ・3840×797・CC BY 2.0）＝全面で右へ流す（映像方針「C3 は横に流す」）。
    #   高さを画面に合わせると横は約5,200px＝寄せ 0.3→0.7（6.9秒で約1,560px＝秒およそ220px）。0.2→0.8 は秒およそ500px で速すぎる
    "cc05": dict(photo=_C3, **ss.mv(_C3, "r", z=1.0, span=(0.3, 0.7)), side="none", color=1.0,
                 t="発電の終わり", s="冷却水路と発電所（2013年）"),
    # cc07（2行・2行目は聞き役の問い）＝🔧 C3305（記念碑と新しい覆い・CC0）＝全面で寄る
    "cc07": dict(photo=_C3305, **ss.mv(_C3305, "in"), side="none", color=1.0,
                 t="事故の重さ", s="記念碑と新しい覆い（2018年）"),
    # cc09（3行・1行目は聞き役）＝C3290（プリピャチの団地と新しい覆い・CC0）＝全面で右へ
    "cc09": dict(photo=_C3290, **ss.mv(_C3290, "r"), side="none", color=1.0,
                 t="外からの覆い", s="プリピャチの団地と新しい覆い（2018年）"),
    # cc10（2行）＝🔧 C3319（組み立て中の新しい覆い・CC BY 2.0）＝全面で左へ
    "cc10": dict(photo=_C3319, **ss.mv(_C3319, "l"), side="none", color=1.0,
                 t="すべらせたアーチ", s="組み立て中の新しい覆い（2016年6月）"),
    # cc11（2行・2行目は聞き役の問い）＝🔧 H01（冷却水路の先の新しい覆い・BY-SA 4.0）＝額ごと寄る
    "cc11": dict(photo=P("h01"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="引き渡し", s="冷却水路の先の新しい覆い（2018年）"),
    # cc12（3行）＝🔧 H11（新しい覆い・BY-SA 4.0＝2025年に無人機が当たったアーチ）＝額ごと右へ
    "cc12": dict(photo=P("h11"), panel=True, color=1.0, fmove=ss.fm("r"),
                 t="2022年と2025年", s="新しい覆い（2018年）"),
    # cc13（2行）＝INSAG-7 付属書II の図 II-13（昔の棒と改良した棒）＝頁の上から図の題の下まで（寄るのは (c)＝試し焼きで寄せを決める）
    "cc13": dict(photo=P("s1p138"), trim=(0.000, 0.000, 1.000, 0.475), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="改められた棒", s="1992年の報告の図（昔の棒と、改良した棒）"),
    # cc16（2行）＝🔧 CR4B の上の盤（4号機の制御室・CC0・学生の頭より上だけを切り出した）＝額の中で寄る
    "cc16": dict(photo=P("cr4b"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="書き直された意味", s="4号機の制御室の壁の盤（2025年）"),   # 試し焼きで見た＝寄りの終わりは壁の盤のガラスだけ
    # cc18（2行）＝🔧 C0（4号機の石棺と排気筒・CC BY 3.0・1600×1200）＝全面で右へ（軽く流す）
    "cc18": dict(photo=_C0, **ss.mv(_C0, "r"), side="none", color=1.0,
                 t="6年後の書き直し", s="4号機の石棺と排気筒（2008年）"),
    # cc19（2行）＝🔧 NSC17（4号機を覆った新しい覆い・BY-SA 4.0）＝額ごと寄る
    "cc19": dict(photo=P("nsc17"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="いまも覆いの中", s="4号機を覆った新しい覆い（2017年10月）"),
    # cc20（2行・11.4秒）＝Pexels 13188723 の後ろの区間（覆いの写らない団地＝STOCK_WINDOW 9.60〜21.70・30560421 の代わり）
    "cc20": ss.vid("cc20"),
})
