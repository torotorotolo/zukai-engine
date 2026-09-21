# -*- coding: utf-8 -*-
"""第5章 継ぎ目の、ゴムの輪 c501–c522（22カット）。11本目（チャレンジャー号）。

■ 🔴🔴 **19カットしか書けていません。**次の3つは**まだ写真の当てが無い**：
     `c513` joint_test（継ぎ目の試験）／`c517` oring_resilience_test（弾力の試験）／
     `c519` srb_sun_shade（日なたと日かげ）
   どれも**報告書の図でしか見たことのない主題**で、報告書の図版は使えない
   （英字が焼き込まれている）。→ `ref/ep11/photo_picks.md` §3-1

■ 実写 7/22（31.8%）。`c503` は動画、`c501`・`c506`・`c522` は動く映像からの止め絵。

■ 🔴 この章で気をつけたこと
  1. **図が決め所より先に答えを出さない。**
     `c515` に「5倍」を書かない（`c516` の決め所）。`c505` に「0.1ミリ」を書かない（`c520`）。
     `c512` に「0.74ミリ・0.6秒」を書かない（`c513`）。
  2. ⚠️ **継ぎ目の断面の型が `titan_fig` に無い。**c504・c505・c510・c512・c520・c522 の
     6カットで要るので型を足す値打ちはあるが、⑤c-2 では**在る型で組んである**。
     🔴 ⑤c-3 で「型を足すか、このままか」を決める。
  3. **単位はメートル法**（門番＝`check_script.py`）。ミリ・メートル・摂氏でそろえる。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC1 = "報告書 第I巻 第I章"
SRC4 = "報告書 第I巻 第IV章"
SRC6 = "報告書 第I巻 第VI章"
FIND = "報告書 第I巻 第IV章 Findings"

SPEC = {

    "c501": dict(
        t="一本の筒では、なかった",
        s="積み上げる補助ロケット　記録映像より",
        **ss.still("srb_stack", "srb", 48),
    ),

    "c502": dict(
        t="工場で、四つにまとめる",
        s="作られてから運ばれるまで",
        fig=("process", dict(
            steps=[dict(t="ユタ州の工場", d="部品を作る", v="", c=J.LINE),
                   dict(t="四つに組む", d="燃料を流しこむ単位", v="4", c=J.AMBER),
                   dict(t="鉄道で運ぶ", d="フロリダまで", v="", c=J.LINE)],
            note=f"{SRC4}・{SRC1}")),
    ),

    # 動画（footage.USE）
    "c503": dict(
        t="一本につき、三か所できる",
        s="現地で組む継ぎ目　記録映像より",
        **ss.vid("c503", 1440, clip="joint", t=42),
    ),

    "c504": dict(
        t="はしとはしが、かみ合う",
        s="上下の筒のつなぎ方",
        fig=("panel", dict(
            blocks=[dict(k="上の筒", t="下のはしが出っぱる", v="出っぱり",
                         c=J.INK_W),
                    dict(k="下の筒", t="上のはしが二またになる", v="はさむ側",
                         c=J.LINE)],
            cols=2, note=SRC4)),
    ),

    # ⚠️ 「0.1ミリ」は c520 が出す。ここでは数字を書かない
    "c505": dict(
        t="ここのすきまが、効いてくる",
        s="二つの筒が触れるところ",
        fig=("people", dict(
            nodes=[dict(x=0.22, y=0.36, t="出っぱり", d="上の筒", kind="part",
                        c=J.INK_W),
                   dict(x=0.74, y=0.36, t="はさむ側", d="下の筒", kind="part",
                        c=J.LINE)],
            edges=[dict(a=0, b=1, t="わずかなすきま", c=J.AMBER)],
            note=SRC4)),
    ),

    "c506": dict(
        t="太さ七ミリ、直径三メートル超",
        s="実物の太さと直径",
        **ss.still("oring_physical", "joint", 2),
    ),

    "c507": dict(
        t="二本あるから安全、という前提",
        s="一次と二次の受け持ち",
        fig=("panel", dict(
            blocks=[dict(k="一次", t="燃えるガスに近いほう", v="先にふさぐ",
                         c=J.ALERT),
                    dict(k="二次", t="遠いほう", v="だめなら受け持つ", c=J.LINE)],
            cols=2, note=f"{SRC4}・{SRC6}")),
    ),

    "c508": dict(
        t="熱を、じかに当てないため",
        s="継ぎ目に塗られるもの",
        fig=("process", dict(
            steps=[dict(t="パテを塗る", d="ガスが当たる側", v="", c=J.AMBER),
                   dict(t="熱をさえぎる", d="ゴムの輪に直接あてない", v="",
                        c=J.OK),
                   dict(t="空気が残る", d="パテとゴムの輪のあいだ", v="",
                        c=J.LINE)],
            note=SRC4)),
    ),

    "c509": dict(
        t="ふたではなく、押す道具",
        s="パテがしていたこと",
        fig=("beforeafter", dict(
            a=dict(k="思われていた役目", t="熱をふさぐ ふた",
                   lines=[], v="", c=J.LINE),
            b=dict(k="もう一つの役目", t="へこんで 空気を押す",
                   lines=["ピストンのように"], v="", c=J.AMBER),
            arrow=True,
            note=SRC4)),
    ),

    "c510": dict(
        t="後ろから押されて、動く",
        s="空気が輪を動かす順番",
        fig=("process", dict(
            steps=[dict(t="溝へ回りこむ", d="押しこまれた空気", v="", c=J.AMBER),
                   dict(t="輪を後ろから押す", d="溝の中で", v="", c=J.AMBER),
                   dict(t="すきまに食いこむ", d="ここでようやくふさがる", v="",
                        c=J.OK)],
            note=SRC4)),
    ),

    # 🔴 決め所⑦。この章の柱
    "c511": dict(
        t="動かなければ、ふさがらない",
        s="ふさぐ仕組みの、かんじんな点",
        fig=("quote", dict(
            phrase="ゴムの輪は、押されてはじめてふさぐ",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=SRC4)),
    ),

    # ⚠️ 開く量と秒は c513 が出す。ここでは向きだけ
    "c512": dict(
        t="ふさぐ相手が、広がっていく",
        s="内側から圧力がかかると",
        fig=("beforeafter", dict(
            a=dict(k="点火の前", t="すきまは狭い",
                   lines=[], v="", c=J.LINE),
            b=dict(k="点火のあと", t="内側の圧力で開く",
                   lines=[], v="", c=J.ALERT),
            arrow=True,
            note=f"{FIND} 8")),
    ),

    # 🔴 c513 は写真の当てが無い（joint_test）

    "c514": dict(
        t="まばたき一回ぶんの勝負",
        s="ふさぐまでに許された時間",
        fig=("timeline", dict(
            events=[dict(t=0.0, top="点火", t2="", c=J.LINE),
                    dict(t=0.15, top="ここまでにふさぐ", t2="間に合わなければ負け",
                         c=J.ALERT, big=True)],
            band=[dict(a=0.1, b=0.2, t="すきまが大きく開く", c=J.ALERT)],
            t0=-0.03, t1=0.32,
            ticks=[(0, "0秒"), (0.1, "0.1秒"), (0.2, "0.2秒"), (0.3, "0.3秒")],
            src=f"{FIND} 11")),
    ),

    # ⚠️ 「5倍」は c516 の決め所。ここでは数字を書かない
    "c515": dict(
        t="戻る速さが、まるで違う",
        s="つぶされたゴムの戻り方",
        fig=("beforeafter", dict(
            a=dict(k="温かいゴム", t="すぐ戻る",
                   lines=["やわらかい"], v="", c=J.OK),
            b=dict(k="冷えたゴム", t="戻りが遅い",
                   lines=["かたくなる"], v="", c=J.ALERT),
            arrow=False,
            note=f"{FIND} 9")),
    ),

    # 🔴 決め所⑧
    "c516": dict(
        t="実験が出した差",
        s="摂氏24度と、摂氏マイナス1度でくらべた",
        fig=("quote", dict(
            phrase="温かい輪は、冷たい輪より5倍速く戻る",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=f"{FIND} 9-b")),
    ),

    # 🔴 c517 は写真の当てが無い（oring_resilience_test）

    "c518": dict(
        t="気温より、さらに冷えていた",
        s="その日、二か所で測った温度",
        fig=("compare", dict(
            items=[dict(v=2.2, t="発射台の気温", disp="2.2", unit="℃", c=J.LINE),
                   dict(v=-2.0, t="壊れた継ぎ目",
                        disp="−2", unit="℃", c=J.ALERT)],
            vmax=6, ref="摂氏で測った値",
            note=f"{FIND} 6-a")),
    ),

    # 🔴 c519 は写真の当てが無い（srb_sun_shade）

    "c520": dict(
        t="もとが狭く、そこから開く",
        s="組んだときのすきまと、開く量",
        fig=("compare", dict(
            items=[dict(v=0.1, t="組んだときの すきま", disp="0.1", unit="mm",
                        c=J.LINE),
                   dict(v=0.74, t="点火のあとに開く量", disp="0.74", unit="mm",
                        c=J.ALERT)],
            vmax=0.9, ref="組み立てたときの実測（平均）",
            note=f"{FIND} 5-c")),
    ),

    # 🔴 決め所⑨
    "c521": dict(
        t="確実にふさげる下の線",
        s="委員会が書いた試験の結果",
        fig=("quote", dict(
            phrase="すきま0.1ミリで、確実にふさいだのは摂氏12.8度から",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=f"{FIND} 10-b")),
    ),

    "c522": dict(
        t="溝に貼りついて、出られない",
        s="ゴムの輪がはまる溝　記録映像より",
        **ss.still("oring_channel", "joint", 8),
    ),

}
