# -*- coding: utf-8 -*-
"""第7章 重なった30秒 c701–c732（32カット）。9本目（テネリフェ）。

■ 🔴🔴 この章の主役は**無線の時間軸**（`radio` 型）。写真を足さない（1通目の指示）。
  秒は報告書 p4・p5 の KLM 機の CVR の時刻（17:00:00 からの秒で書く。画面は「17:06:20」の形）：
    341        17:05:41 出力を進める動き（p30）
    344.6–350.8 KLM「離陸の用意ができた、ATC の許可を待っている」
    353.4–363.1 管制塔「ATC の許可」
    369.6–377.8 KLM の復唱（最後に "we are now at take-off"）
    371        17:06:11 ブレーキを放した（p31）／373 およそ17:06:13 機長「行くぞ」
    378.2–381.8 管制塔「オーケー……離陸は待って、こちらから呼ぶ」
    379.4–382.1 甲高い音（⚠️ 報告書の中で長さが3通り＝画面は「およそ3秒」だけ）
    379.4–383.4 パンナム「まだ滑走路を走っている……クリッパー1736」
               （⚠️ 始まりは甲高い音の始まり＝二つ目の送信が重なった時刻として置いた）
    385.5–388.9 管制塔「滑走路を出たら知らせて」／389.6–390.7 パンナム「了解」
    392 航空機関士の問い／395 機長「いや、出た」（p33）
■ 台本の写真6カットのうち2カットを図にし、地に写真を敷いた（写真映像の数は変わらない）
  c701（地 losrodeos_now_12 の寄り）／c719（地 losrodeos_now_11 の寄り）。⚠️ 管制塔の写真は0点。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
CVR = "操縦室の録音の書き起こし"
RPT = "事故報告書 p4・p5（KLM機の録音の時刻）"
T3 = ["KLM", "管制塔", "パンナム"]
TK = [(370, "17:06:10"), (380, "17:06:20"), (390, "17:06:30")]
# 前のカットから続けて見せる帯（pre＝骨格に入れる）
READBACK = dict(lane=0, a=369.61, b=377.79, t="復唱", c=J.LINE, pre=True)
# ⚠️ 前から見せる札は短く＝同じ段の次の送信（c728 の 385.5 秒）の札と重ならない幅（約330px 未満）にする
TOWER_WAIT = dict(lane=1, a=378.19, b=381.79, t="離陸は待って", c=J.LINE, pre=True)
PAA_STILL = dict(lane=2, a=379.39, b=383.39, t="まだ滑走路を走っている", c=J.LINE, pre=True)
KLM_ROLL = dict(lane=0, a=371.0, b=395.0, t="走っている", c=J.ALERT, pre=True)

SPEC = {

    # 図＋地（BACKDROP＝losrodeos_now_12 の寄り）
    "c701": dict(
        t="滑走路の端で、747を回す",
        s="KLMが着いた滑走路の端",
        fig=("runway", dict(
            steps=[dict(path=[dict(on="rwy", a=0.10, b=0.92, c=J.AMBER)],
                        planes=[dict(at=0.94, on="rwy", head=0, t="KLM", c=J.AMBER, s=0.9)]),
                   dict(turn=dict(at=0.975, t="180度", c=J.AMBER),
                        mark=[dict(at=0.70, y="below", t="幅45メートルの上で", c=J.INK_W)])],
            exits=False, note="模式図（道の位置と角度は正確ではない）",
            src="事故報告書 p26・p27")),
    ),

    "c702": dict(
        t="幅も、見通しも、機体も不利",
        s="報告書が「難しい」と書いた旋回",
        fig=("panel", dict(
            blocks=[dict(k="滑走路の幅", t="狭い", v="45メートル", c=J.AMBER),
                    dict(k="まわり", t="霧の中", v="", c=J.LINE),
                    dict(k="機体", t="ボーイング", v="747", c=J.INK_W)],
            note="事故報告書 p26・p27", cols=3)),
    ),

    "c703": dict(
        t="その少し前、ワイパーを切った",
        s="録音に残った、小さな動作",
        fig=("process", dict(
            steps=[dict(t="乗員", d="ワイパーを切る", c=J.INK_W),
                   dict(t="記録", d="操縦室の録音", c=J.DOC),
                   dict(t="分かること", d="雨がやみ、一時よく見えた", c=J.OK)],
            note="事故報告書 p27・p29")),
    ),

    "c704": dict(
        t="旋回と、視界がよくなった時期",
        s="747の操縦室（NASAの機体）　2012年撮影",
        photo=P("cockpit_747_15"), side="right", ann_y=356,
        **ss.kind(P("cockpit_747_15")),
        ann=[dict(t="報告書の見方", d="二つは同じころ", dc=J.DOC, ds=34)],
    ),

    "c705": dict(
        t="空にいたい、という気持ち",
        s="報告書が書いた乗員の心理",
        fig=("panel", dict(
            blocks=[dict(k="旋回のあと", t="ほっとしたにちがいない", v="", c=J.DOC),
                    dict(k="強まった気持ち", t="地上の問題を終える", v="", c=J.AMBER),
                    dict(k="書き添え", t="やめる道も機長は考えた", v="", c=J.INK_W)],
            note="事故報告書 p27", cols=3)),
    ),

    "c706": dict(
        t="17:05:41、出力を進める動き",
        s="KLM機で残った記録と会話",
        fig=("radio", dict(
            lanes=["記録装置", "副操縦士", "機長"],
            events=[dict(lane=0, a=341.0, t="出力を進める動き", c=J.AMBER),
                    dict(lane=1, a=342.0, t="待って、まだATCの許可が無い", c=J.OK),
                    dict(lane=2, a=343.0, t="分かっている、聞いてくれ", c=J.INK_W)],
            t0=339.2, t1=347.5, ticks=[(341, "17:05:41")],
            note="発言の間隔は正確ではない", src="事故報告書 p30")),
    ),

    "c707": dict(
        t="17:05:44、離陸の用意ができた",
        s="KLMから管制塔への送信",
        fig=("radio", dict(
            lanes=["KLM", "管制塔"],
            events=[dict(lane=0, a=344.6, b=350.77, t="離陸の用意ができた",
                         d="ATCの許可待ち", c=J.AMBER)],
            t0=342.0, t1=358.0, ticks=[(345, "17:05:45"), (350, "17:05:50"),
                                       (355, "17:05:55")],
            src=RPT)),
    ),

    "c708": dict(
        t="ATCの許可は、飛んだあとの道順",
        s="一回の飛行を、三つに分けて見る",
        fig=("process", dict(
            steps=[dict(t="離陸の前", d="滑走路の端", c=J.LINE),
                   dict(t="離陸", d="滑走路を走って浮く", c=J.LINE),
                   dict(t="離陸したあと", d="どこをどう飛ぶか", c=J.INST)],
            note="事故報告書 p40・p41")),
    ),

    "c709": dict(
        t="名前が似た、別の許可",
        s="二つの許可",
        fig=("beforeafter", dict(
            a=dict(k="ATCの許可", t="離陸したあとの飛び方", lines=["経路と高さ"], c=J.INST),
            b=dict(k="離陸の許可", t="離陸してよいか", lines=["これとは別に出る"],
                   c=J.ALERT),
            arrow=False, note="事故報告書 p41")),
    ),

    "c710": dict(
        t="17:05:53、許可の読み上げ",
        s="博物館に保存された747-230の計器盤　2007年撮影",
        photo=P("cockpit_747_09"), side="right", ann_y=356,
        **ss.kind(P("cockpit_747_09")),
        ann=[dict(t="向かう先", d="パパという無線標識", dc=J.INK_W, ds=36),
             dict(t="フライトレベル", v="90", vc=J.AMBER, vs=110)],
    ),

    "c711": dict(
        t="中身は、離陸後の高さと向き",
        s="管制官が読み上げたこと",
        fig=("panel", dict(
            blocks=[dict(k="高さ", t="フライトレベル90", v="約2,750メートル", c=J.AMBER),
                    dict(k="離陸したら", t="右へ旋回", v="", c=J.LINE),
                    dict(k="そのあと", t="決められた方位へ", v="", c=J.LINE)],
            note=CVR, cols=3)),
    ),

    "c712": dict(
        t="離陸の許可は、出ていない",
        s="17:05:53からの管制官の送信",
        fig=("absent", dict(
            mode="single",
            items=[dict(t="「離陸してよい」という言葉", d="この送信の中に一つも無い", ok=False,
                        c=J.ALERT)],
            note="事故報告書 p40　離陸の許可は求められてもいない")),
    ),

    "c713": dict(
        t="17:06:09、復唱が始まる",
        s="KLMと管制塔の送信",
        fig=("radio", dict(
            lanes=["KLM", "管制塔"],
            events=[dict(lane=1, a=353.41, b=363.09, t="ATCの許可", c=J.LINE, pre=True),
                    dict(lane=0, a=369.61, b=377.79, t="復唱", d="パパへ、FL90、右旋回",
                         c=J.AMBER)],
            bands=[dict(a=369.61, b=375.5, t="ここまでは正しい", c=J.OK, st="ok")],
            t0=350.0, t1=380.0,
            ticks=[(355, "17:05:55"), (360, "17:06:00"), (365, "17:06:05"),
                   (370, "17:06:10"), (375, "17:06:15")],
            note="復唱＝聞いた指示の読み返し", src=RPT)),
    ),

    "c714": dict(
        t="復唱のあとに続いた、ひと言",
        s="KLMの副操縦士の復唱",
        fig=("moment", dict(
            clock="17:06:17", label="復唱の終わり",
            facts=[dict(t="英語", v="we are now at take-off", c=J.AMBER),
                   dict(t="日本語", v="われわれはいま、離陸中", c=J.INK_W)],
            sub=RPT)),
    ),

    "c715": dict(
        t="話す副操縦士と、動かす機長",
        s="KLM機の操縦室",
        fig=("beforeafter", dict(
            a=dict(k="副操縦士", t="復唱の最中", lines=["管制塔への無線"], c=J.LINE),
            b=dict(k="機長", t="出力を入れた", lines=["同じとき"], c=J.ALERT),
            arrow=False, note="事故報告書 p32")),
    ),

    "c716": dict(
        t="復唱を待たずに、ブレーキを放した",
        s="KLM機で残った記録と会話",
        fig=("radio", dict(
            lanes=["副操縦士", "機長", "記録装置"],
            events=[dict(lane=0, a=369.61, b=377.79, t="復唱", c=J.AMBER, pre=True),
                    dict(lane=1, a=373.0, t="行くぞ（オランダ語）", d="およそ17:06:13",
                         c=J.ALERT),
                    dict(lane=2, a=371.0, t="ブレーキを放した", d="17:06:11", c=J.ALERT),
                    dict(lane=0, a=377.79, t="復唱が終わる", d="17:06:17", c=J.LINE)],
            t0=366.0, t1=381.0, ticks=[(370, "17:06:10"), (375, "17:06:15"),
                                       (380, "17:06:20")],
            src="事故報告書 p31・p40／" + CVR)),
    ),

    "c717": dict(
        t="許可を求める言葉は、無かった",
        s="「離陸中」という送信の受け取られ方",
        fig=("quote", dict(
            phrase="誰も「離陸中」とは受け取らなかった",
            rows=[("管制官の受け取り方", "離陸位置に着いた", J.INK_W),
                  ("離陸の許可", "求められていない", J.LINE),
                  ("出どころ", "事故報告書 p32", J.DOC)],
            paper=True)),
    ),

    "c718": dict(
        t="三か国で、初めて一緒に聞いた",
        s="あとから行われた聞き取り",
        fig=("people", dict(
            nodes=[dict(x=0.50, y=0.16, t="管制塔の録音", d="", c=J.DOC, kind="doc"),
                   dict(x=0.14, y=0.66, t="スペイン", d="調査団", c=J.INST, kind="org"),
                   dict(x=0.50, y=0.70, t="アメリカ", d="調査団", c=J.INST, kind="org"),
                   dict(x=0.86, y=0.66, t="オランダ", d="調査団", c=J.INST, kind="org")],
            edges=[dict(a=1, b=0, t="", c=J.LINE), dict(a=2, b=0, t="", c=J.LINE),
                   dict(a=3, b=0, t="", c=J.LINE)],
            note="事故報告書 p32")),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_11 の寄り）。⚠️ 管制塔の写真は無い＝代用しない。
    "c719": dict(
        t="「離陸中」は、ほぼ伝わらなかった",
        s="報告書の注",
        fig=("absent", dict(
            mode="single",
            items=[dict(t="「離陸中」と気づいた人", d="0人か、ごくわずか",
                        ok=False, c=J.ALERT)],
            note="事故報告書 p32（注）")),
    ),

    "c720": dict(
        t="17:06:18、管制官の答え",
        s="管制塔からKLMへ",
        fig=("radio", dict(
            lanes=T3,
            events=[READBACK,
                    dict(lane=1, a=378.19, b=381.79, t="オーケー",
                         d="短い間のあと、止めるための言葉", c=J.AMBER)],
            t0=366.0, t1=394.0, ticks=TK, src=RPT)),
    ),

    "c721": dict(
        t="離陸は待って、こちらから呼ぶ",
        s="管制塔の送信と、そのときのKLM",
        fig=("radio", dict(
            lanes=T3,
            events=[READBACK,
                    dict(lane=1, a=378.19, b=381.79, t="離陸は待って、呼びます", c=J.AMBER),
                    dict(lane=0, a=371.0, b=393.0, t="", d="KLMはもう走っている", c=J.ALERT,
                         op=0.55)],
            t0=366.0, t1=394.0, ticks=TK, src=RPT)),
    ),

    "c722": dict(
        t="パンナムは、自分の位置を伝えた",
        s="パンナムから管制塔へ",
        fig=("radio", dict(
            lanes=T3,
            events=[KLM_ROLL, TOWER_WAIT,
                    dict(lane=2, a=379.39, b=383.39, t="まだ滑走路を走っている",
                         d="クリッパー1736", c=J.INK_W)],
            t0=366.0, t1=398.0, ticks=TK, src=RPT)),
    ),

    "c723": dict(
        t="二つの声が、一つの音に",
        s="同じ時刻の、二つの送信",
        fig=("quote", dict(
            phrase="操縦室では、甲高い音になった",
            rows=[("重なった送信", "管制塔とパンナム", J.INK_W),
                  ("聞いた場所", "KLM機の操縦室", J.LINE),
                  ("出どころ", "事故報告書 p38", J.DOC)],
            paper=True)),
    ),

    # 🔴 長さは画面に「およそ3秒」とだけ出す（報告書の中で3通り）。
    "c724": dict(
        t="およそ3秒の、甲高い音",
        s="重なっていた送信と、そのときのKLM",
        fig=("radio", dict(
            lanes=T3,
            events=[KLM_ROLL, TOWER_WAIT, PAA_STILL],
            bands=[dict(a=379.39, b=382.06, t="甲高い音　およそ3秒", c=J.ALERT, st="sq")],
            t0=366.0, t1=398.0, ticks=TK,
            note="その3秒に送られていた言葉＝離陸は待って", src="事故報告書 p5・p40")),
    ),

    "c725": dict(
        t="同じ3秒、出力は離陸の値",
        s="博物館に保存された747-136の操縦室　2015年撮影",
        photo=P("cockpit_747_11"), side="right", ann_y=356,
        **ss.kind(P("cockpit_747_11")),
        ann=[dict(t="出力が落ち着いた時刻", v="17:06:19", vc=J.ALERT, vs=88)],
    ),

    "c726": dict(
        t="報告書は、音だけのせいにしていない",
        s="報告書の書き方",
        fig=("beforeafter", dict(
            a=dict(k="甲高い音で", t="聞き取りにくくなった", lines=[], c=J.AMBER),
            b=dict(k="ただし", t="聞き取れる程度", lines=[], c=J.INK_W),
            arrow=False, lead="答えは、報告書の別の頁（p27）",
            note="事故報告書 p32")),
    ),

    "c727": dict(
        t="目に気を取られ、耳がおろそかに",
        s="報告書が別の場所で書いた答え",
        fig=("process", dict(
            steps=[dict(t="見ることに気を取られる", d="霧の中の滑走路", c=J.AMBER),
                   dict(t="聞くほうが落ちる", d="事故報告書 p27", c=J.ALERT),
                   dict(t="パンナムに届いたのは", d="管制官の最後の一音だけ", c=J.INK_W)],
            note="事故報告書 p27・p38")),
    ),

    "c728": dict(
        t="17:06:25、滑走路を出たら知らせて",
        s="管制塔からパンナムへ",
        fig=("radio", dict(
            lanes=T3,
            events=[KLM_ROLL, TOWER_WAIT, PAA_STILL,
                    dict(lane=1, a=385.47, b=388.89, t="滑走路を出たら知らせて",
                         d="＝まだ滑走路の上", c=J.AMBER)],
            t0=366.0, t1=398.0, ticks=TK, src=RPT)),
    ),

    "c729": dict(
        t="17:06:29、パンナムの答え",
        s="パンナムから管制塔へ",
        fig=("radio", dict(
            lanes=T3,
            events=[KLM_ROLL, TOWER_WAIT, PAA_STILL,
                    dict(lane=1, a=385.47, b=388.89, t="出たら知らせて", c=J.LINE, pre=True),
                    dict(lane=2, a=389.59, b=390.69, t="了解、出たら知らせる", c=J.INK_W)],
            bands=[dict(a=389.59, b=390.69, t="KLMにも届いた", c=J.OK, st="heard")],
            t0=366.0, t1=398.0, ticks=TK, src=RPT)),
    ),

    "c730": dict(
        t="動いたのは、航空機関士",
        s="走っているKLM機の、三人",
        fig=("people", dict(
            nodes=[dict(x=0.16, y=0.46, t="機長", d="反応しない", c=J.LINE, kind="person"),
                   dict(x=0.50, y=0.46, t="副操縦士", d="反応しない", c=J.LINE,
                        kind="person"),
                   dict(x=0.84, y=0.46, t="航空機関士", d="いちばんうしろの席", c=J.OK,
                        kind="person")],
            edges=[],
            note="事故報告書 p33")),
    ),

    "c731": dict(
        t="17:06:32、機関士が聞いた",
        s="747-200の機関士席の計器盤　2008年撮影",
        photo=P("cockpit_747_10"), side="right", ann_y=356,
        **ss.kind(P("cockpit_747_10")),
        ann=[dict(t="聞いた人", d="航空機関士", dc=J.OK, ds=40),
             dict(t="問いの中身", d="パンナムが滑走路を出たか", dc=J.INK_W, ds=32)],
    ),

    "c732": dict(
        t="17:06:35、強い肯定",
        s="三人目の問いと、機長の答え",
        fig=("quote", dict(
            phrase="いや、出た。機長はそう答えた",
            rows=[("問うた人", "航空機関士", J.INK_W),
                  ("答えた人", "KLMの機長", J.ALERT),
                  ("出どころ", CVR + "／事故報告書 p33", J.DOC)],
            paper=False)),
    ),
}
