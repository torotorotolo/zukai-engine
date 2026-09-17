# -*- coding: utf-8 -*-
"""第6章 滑走路を、逆向きに走る c601–c624（24カット）。9本目（テネリフェ）。

■ 🔴 この章は**場所の話**（どこを走ったか）。図が主役＝`runway` 型（ref/ep9/kousei.md §1）。
  ⚠️ **報告書に空港全体の平面図が無い**＝道の位置と角度は模式（note で毎回断る）。
  🔴 C-3 を「148度」に描かない／ILS がどちらの滑走路か描かない。
  向き＝左が12側の端（北西・駐機場の側）、右が30側の端（南東）、誘導路は北東側（上）。
  KLM は12側から滑走路に入り、30側の端まで走って向きを変えた（報告書 p3・p4）。
  パンナムは同じく12側から入り、「三番目の道で左へ」出るよう指示された。
■ 時刻は報告書 p3・p4 と操縦室の録音の書き起こし。**秒が無いやりとりは順番だけ**で描く（c602・c613）。
■ 台本の写真6カットのうち4カットを図にし、地に写真を敷いた（写真映像の数は変わらない）
  c601（地 klm_747_1973_01 の寄り）／c606（地 losrodeos_now_08）／c619（地 losrodeos_now_08 の寄り）
  ／c624（地 losrodeos_now_02 の寄り）。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
RW = "模式図（道の位置と角度は正確ではない）"
CVR = "操縦室の録音の書き起こし"
KLM = dict(on="rwy", head=0, t="KLM", c=J.AMBER, s=0.9)
PAA = dict(on="rwy", head=0, t="パンナム", c=J.INK_W, s=0.9)


def plane(base, at, **kw):
    return dict(base, at=at, **kw)


SPEC = {

    # 図＋地（BACKDROP＝klm_747_1973_01 の寄り）
    "c601": dict(
        t="16:56、最後の10分が始まる",
        s="KLMから管制塔への無線",
        fig=("moment", dict(
            clock="16:56", label="KLMが管制塔を呼んだ",
            facts=[dict(t="求めたもの", v="地上を走る許可", c=J.INK_W),
                   dict(t="答え", v="すぐに出た", c=J.OK)],
            sub="事故報告書 p3")),
    ),

    "c602": dict(
        t="16:58、KLMの申し出",
        s="KLMと管制塔のやりとり",
        fig=("radio", dict(
            lanes=["KLM", "管制塔"],
            events=[dict(lane=0, a=1.0, t="地上を走りたい", c=J.LINE, pre=True),
                    dict(lane=1, a=2.0, t="許可", c=J.OK, pre=True),
                    dict(lane=0, a=3.0, b=4.6, t="12をバックタクシー",
                         d="離陸は滑走路30から", c=J.AMBER)],
            t0=0.4, t1=5.6, ticks=[(1.0, "16:56"), (3.0, "16:58")],
            note="順番だけ（間隔は正確ではない）", src="事故報告書 p3")),
    ),

    "c603": dict(
        t="バックタクシーとは",
        s="KLM機が走る道すじ",
        fig=("runway", dict(
            steps=[dict(planes=[plane(KLM, 0.06)]),
                   dict(path=[dict(on="rwy", a=0.10, b=0.95, c=J.AMBER)],
                        mark=[dict(at=0.52, y="below", t="離陸とは逆の向き", c=J.AMBER)]),
                   dict(turn=dict(at=0.975, t="端で向きを変える", c=J.AMBER))],
            exits=False, note=RW, src=CVR)),
    ),

    "c604": dict(
        t="本来は、誘導路を通る",
        s="平行誘導路",
        fig=("runway", dict(
            steps=[dict(path=[dict(on="twy", a=0.06, b=0.95, c=J.LINE)],
                        mark=[dict(at=0.66, y="top", t="この日は使えない", c=J.ALERT)])],
            exits=False, note=RW, src="事故報告書 p32")),
    ),

    "c605": dict(
        t="C-1とC-2から、入れなかった",
        s="駐機場と、誘導路へつなぐ道",
        fig=("runway", dict(
            steps=[dict(planes=[dict(at=f, on="apron", head=0, s=0.5, c=J.LINE)
                                for f in (0.02, 0.10, 0.18, 0.26, 0.34)]),
                   dict(block=["C-1", "C-2"]),
                   dict(mark=[dict(at=0.20, y="below", t="駐機場に機体が集まった",
                                   c=J.ALERT)])],
            note=RW, src="事故報告書 p32")),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_08＝島の北東部の衛星画像）
    "c606": dict(
        t="二機とも、滑走路の上へ",
        s="管制官が選んだやり方",
        fig=("runway", dict(
            # ⚠️ 2026-09-17（⑤c' E-09）：見出し「二機とも」なのに札が KLM だけだった（lab=False）
            steps=[dict(planes=[plane(KLM, 0.14), plane(PAA, 0.04)]),
                   dict(path=[dict(on="rwy", a=0.19, b=0.95, c=J.AMBER)],
                        mark=[dict(at=0.60, y="below", t="ふだんは着陸機の道",
                                   c=J.AMBER)])],
            exits=False, note=RW, src="事故報告書 p32・p40")),
    ),

    "c607": dict(
        t="規則の内側、でも標準ではない",
        s="報告書の書き方",
        fig=("quote", dict(
            phrase="滑走路を、誘導路の代わりに使った",
            rows=[("規則", "内側だった", J.OK),
                  ("やり方", "標準ではない", J.ALERT),
                  ("出どころ", "事故報告書 p40", J.DOC)],
            paper=True)),
    ),

    "c608": dict(
        t="危うくなりうる",
        s="報告書の言葉",
        fig=("panel", dict(
            blocks=[dict(k="何が", t="使用中の滑走路での地上走行", v="", c=J.DOC),
                    dict(k="報告書の評価", t="場合によっては危うい", v="", c=J.ALERT)],
            note="事故報告書 p40", cols=2)),
    ),

    "c609": dict(
        t="最初の指示は「三番目」",
        s="KLMが走るように言われた道",
        fig=("runway", dict(
            steps=[dict(planes=[plane(KLM, 0.06)]),
                   dict(path=[dict(a=0.10, b=0.92, via="C-3", c=J.AMBER)],
                        mark=[dict(at=0.90, y="above", t="滑走路30の待機の位置",
                                   c=J.INK_W)]),
                   dict(hot=[("C-3", J.AMBER)],
                        mark=[dict(at=0.62, y="top", t="三番目の道で左へ", c=J.AMBER)])],
            note=RW, src=CVR + "／事故報告書 p3")),
    ),

    "c610": dict(
        t="最初の食い違いは、ここ",
        s="管制官の指示と、KLMの答え",
        fig=("runway", dict(
            steps=[dict(hot=[("C-3", J.AMBER)],
                        mark=[dict(at=0.62, y="top", t="指示＝三番目", c=J.AMBER)]),
                   dict(hot=[("C-1", J.ALERT)],
                        mark=[dict(at=0.10, y="below", t="答え＝最初の道", c=J.ALERT)])],
            note=RW, src=CVR + "／事故報告書 p3")),
    ),

    "c611": dict(
        t="訂正、まっすぐ端まで",
        s="管制官がすぐに出した訂正",
        fig=("runway", dict(
            steps=[dict(planes=[plane(KLM, 0.06, lab=False)],
                        path=[dict(on="rwy", a=0.10, b=0.95, c=J.AMBER)],
                        mark=[dict(at=0.55, y="below", t="まっすぐ滑走路の端まで", c=J.AMBER)]),
                   dict(turn=dict(at=0.975, t="そこで向きを変える", c=J.AMBER))],
            exits=False, note=RW, src=CVR + "／事故報告書 p3")),
    ),

    "c612": dict(
        t="KLMの理解は、まだC-1",
        s="KLMの二度目の問い",
        fig=("runway", dict(
            steps=[dict(hot=[("C-1", J.ALERT)],
                        mark=[dict(at=0.10, y="below", t="C-1で左に？", c=J.ALERT)]),
                   dict(mark=[dict(at=0.62, y="top", t="30秒ほど前に同じ話", c=J.TICK)])],
            note=RW, src=CVR + "／事故報告書 p4")),
    ),

    "c613": dict(
        t="どこで出るのか、二度たずねた",
        s="16時58分台のKLMと管制塔のやりとり",
        fig=("radio", dict(
            lanes=["管制塔", "KLM"],
            events=[dict(lane=0, a=1.0, t="三番目で出よ", c=J.LINE, pre=True),
                    dict(lane=1, a=2.0, t="最初の道で出る", c=J.AMBER, pre=True),
                    dict(lane=0, a=3.0, t="端まで行け", c=J.LINE, pre=True),
                    dict(lane=1, a=4.0, t="C-1で左？", c=J.AMBER, pre=True),
                    dict(lane=0, a=5.0, t="否定、否定。端まで", c=J.ALERT),
                    dict(lane=1, a=6.0, t="オーケー", c=J.OK)],
            t0=0.4, t1=7.0,
            note="順番だけ（間隔は正確ではない）　黄＝KLMが出る場所を口にした二度",
            src="事故報告書 p3・p4")),
    ),

    "c614": dict(
        t="17:02、パンナムが確かめた",
        s="パンナムの747　1970年撮影（スキポール空港）",
        photo=P("panam_ams1970_03"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("panam_ams1970_03")),
        ann=[dict(t="確かめたこと", d="滑走路を走る、という指示", dc=J.INK_W, ds=32)],
    ),

    "c615": dict(
        t="パンナムにも「三番目」",
        s="管制官がパンナムに出した指示",
        fig=("runway", dict(
            steps=[dict(planes=[plane(PAA, 0.06)],
                        path=[dict(a=0.10, b=0.66, via="C-3", c=J.INK_W)]),
                   dict(hot=[("C-3", J.AMBER)],
                        mark=[dict(at=0.62, y="top", t="三番目を左へ（二度くり返した）",
                                   c=J.AMBER)])],
            note=RW, src=CVR + "／事故報告書 p4")),
    ),

    "c616": dict(
        t="復唱は、三番目",
        s="パンナムの復唱と、そのあと",
        fig=("process", dict(
            steps=[dict(t="管制官", d="三番目を左へ", c=J.LINE),
                   dict(t="パンナム", d="三番目を左へ", c=J.AMBER),
                   dict(t="そのすぐあと", d="機内で食い違い", c=J.ALERT)],
            note=CVR)),
    ),

    "c617": dict(
        t="パンナム機の中でも、聞き方が割れた",
        s="無線を聞いた二人の言葉",
        fig=("people", dict(
            nodes=[dict(x=0.50, y=0.18, t="管制塔の無線", d="", c=J.DOC, kind="doc"),
                   dict(x=0.18, y=0.66, t="航空機関士", d="三番目と言った", c=J.OK,
                        kind="person"),
                   dict(x=0.82, y=0.66, t="機長", d="一番目と聞こえた", c=J.ALERT,
                        kind="person")],
            edges=[dict(a=0, b=1, t="", c=J.LINE), dict(a=0, b=2, t="", c=J.LINE)],
            note=CVR + "（パンナム機）／事故報告書 p33")),
    ),

    "c618": dict(
        t="分からないことを、残さなかった",
        s="あいまいさの、片づけ方",
        fig=("beforeafter", dict(
            a=dict(k="機内", t="三番目か、一番目か", lines=["食い違い"], c=J.ALERT),
            b=dict(k="副操縦士", t="もう一度聞く", lines=["管制塔に確かめる"], c=J.OK),
            note=CVR + "（パンナム機）")),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_08 の寄り）
    "c619": dict(
        t="17:03:29、パンナムが確かめた",
        s="パンナムから管制塔へ",
        fig=("moment", dict(
            clock="17:03:29", label="パンナムの問い",
            facts=[dict(t="確かめたこと", v="三番目の交差点で左", c=J.AMBER)],
            sub=CVR)),
    ),

    "c620": dict(
        t="数え方まで、はっきり伝えた",
        s="パンナムの問いへの答え",
        fig=("quote", dict(
            phrase="一、二、三、三番目です",
            rows=[("誰が", "管制官", J.INK_W),
                  ("誰に", "パンナム1736便", J.LINE),
                  ("出どころ", CVR + "／事故報告書 p32", J.DOC)],
            paper=False)),
    ),

    "c621": dict(
        t="言葉は伝わり、数え方が残った",
        s="報告書が書いた、このときの状態",
        fig=("beforeafter", dict(
            a=dict(k="晴れた疑い", t="三番目という言葉", lines=["正しく伝わった"], c=J.OK),
            b=dict(k="残った問題", t="どれが三番目か", lines=["出口の数え方"], c=J.ALERT),
            arrow=False, note="事故報告書 p38")),
    ),

    "c622": dict(
        t="手元の図で、場所を追った",
        s="フランクフルトの747の操縦室　1973年撮影",
        photo=P("cockpit_747_16"), side="right", ann_y=356,
        **ss.kind(P("cockpit_747_16")),
        ann=[dict(t="パンナムの乗員", d="見つけにくい出口", dc=J.INK_W, ds=32)],
    ),

    "c623": dict(
        t="一つ目、二つ目、そして三番目",
        s="パンナムが確認した道",
        fig=("runway", dict(
            steps=[dict(path=[dict(on="rwy", a=0.03, b=0.12, c=J.INK_W)],
                        hot=[("C-1", J.OK)],
                        mark=[dict(at=0.08, y="below", t="17:04:26　一つ目（90度）", c=J.OK,
                                   anchor="start")]),
                   dict(path=[dict(on="rwy", a=0.12, b=0.32, c=J.INK_W)],
                        hot=[("C-2", J.OK)],
                        mark=[dict(at=0.30, y="low", t="17:05:22　二つ目", c=J.OK)]),
                   dict(path=[dict(on="rwy", a=0.32, b=0.54, c=J.INK_W)],
                        hot=[("C-3", J.ALERT)],
                        planes=[plane(PAA, 0.58, lab=False)],
                        mark=[dict(at=0.62, y="top", t="三番目を通り過ぎた", c=J.ALERT)])],
            note=RW, src=CVR + "／事故報告書 p38")),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_02 の寄り）
    "c624": dict(
        t="三番目を過ぎ、二機は向き合う",
        s="報告書が挙げた二つの見方と、二機の位置",
        fig=("runway", dict(
            steps=[dict(hot=[("C-3", J.ALERT)],
                        mark=[dict(at=0.46, y="top", t="取り違えた？", c=J.ALERT,
                                   anchor="end")]),
                   dict(hot=[("C-4", J.AMBER)],
                        mark=[dict(at=0.66, y="top", t="四番目が出やすい？", c=J.AMBER,
                                   anchor="start")]),
                   dict(planes=[plane(PAA, 0.56), dict(KLM, at=0.975, head=180)],
                        mark=[dict(at=0.80, y="gap", t="向かい合う", c=J.ALERT)])],
            note=RW, src="事故報告書 p38")),
    ),
}
