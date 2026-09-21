# -*- coding: utf-8 -*-
"""第3章 七十三秒 c301–c322（22カット）。11本目（チャレンジャー号）。

■ 実写 11/22（50%）。`c303` は動く映像からの止め絵、`c307` は動画（`footage.USE`）。

■ 🔴 この章で気をつけたこと
  1. **`c313` は「それまでの打ち上げ」のカット。**51-L 自身の絵を出すと言っていることと違う。
     1984年 41-C（同じチャレンジャー号の別の飛行）を当てた。副題で年と飛行を名乗る
     → [[feedback-subtitle-must-match-what-is-visible]]
  2. **`c311` は「ほぼ同じ」を見せるカット。**`compare` は差が小さいと例外で止まるので
     `bar=False`（数字に語らせる）→ `tools/cuts/README.md` §5-3
  3. **`c314` は二つの見方を並べたまま**にする。どちらかに寄せない（報告書がそうしている）。
  4. ⚠️ **`c308` の図に、カメラの位置を描かない。**報告書に配置図が無いので、
     置くと「実測の位置」に見える。工程（2台が動かない→別のカメラを集める→計算）で見せる。
  5. ⚠️ `c303` に当てた止め絵（元607秒）が**主エンジンの点火の瞬間かは未確認**。
     ⑤c-3 のシートで確かめる → `ref/ep11/photo_picks.md`
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC3 = "報告書 第I巻 第III章"
SRC4 = "報告書 第I巻 第IV章"

SPEC = {

    "c301": dict(
        t="摂氏二・二度で、飛んだ",
        s="STS-51-L の打ち上げ　1986年1月28日",
        photo=P("launch_pad_morning"), **ss.kind(P("launch_pad_morning")),
        bias=0.45,
    ),

    "c302": dict(
        t="二つの記録から読み直した",
        s="この七十三秒を調べた材料",
        fig=("panel", dict(
            blocks=[dict(k="見る", t="NASAのカメラ", v="1コマずつ", c=J.LINE),
                    dict(k="測る", t="機体から届いた信号", v="1000分の1秒",
                         c=J.AMBER)],
            cols=2, note=SRC3)),
    ),

    "c303": dict(
        t="六・六秒前に、火がつく",
        s="主エンジンの点火　記録映像より",
        **ss.still("ssme_ignition", "launch", 9),
    ),

    "c304": dict(
        t="機体は、前へしなって戻る",
        s="点火から浮き上がるまでの動き",
        fig=("beforeafter", dict(
            a=dict(k="点火のとき", t="前へしなる",
                   lines=["主エンジンの力で"], v="", c=J.LINE),
            b=dict(k="そのあと", t="まっすぐに戻る",
                   lines=["現場では「はじく」と呼んだ"], v="", c=J.AMBER),
            arrow=True,
            note=SRC3)),
    ),

    "c305": dict(
        t="いちばん強く引かれる瞬間",
        # ⚠️ 副題に図の札と同じ語を入れない（`check_dup` が2件鳴った）
        s="時刻でたどる、点火のあと",
        fig=("timeline", dict(
            events=[dict(t=-6.6, top="主エンジンの点火", t2="", c=J.LINE),
                    dict(t=0.0, top="ボルトが外れる", t2="はね返りの途中",
                         c=J.ALERT, big=True)],
            band=[dict(a=-1.2, b=0.9, t="継ぎ目にかかる力が、飛行中でいちばん大きい",
                       c=J.ALERT)],
            t0=-7.4, t1=1.6,
            ticks=[(-6.6, "−6.6秒"), (0, "0秒"), (1, "+1秒")],
            src=SRC3)),
    ),

    # 🔴 決め所④
    "c306": dict(
        t="浮いた直後に、もう出ていた",
        s="打ち上げ直後の記録",
        fig=("quote", dict(
            phrase="打ち上げから0.678秒。すでに煙が出ていた",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=SRC3)),
    ),

    # 動画（footage.USE）。⚠️ ナレーションはカメラの話、絵は煙そのもの
    "c307": dict(
        t="そこを狙った二台が、止まっていた",
        s="継ぎ目から出た煙　記録映像より",
        **ss.vid("c307", 1440, clip="smoke", t=11),
    ),

    # ⚠️ カメラの位置を図に描かない（報告書に配置図が無い）
    "c308": dict(
        t="別の角度から、逆に計算した",
        s="煙の出どころを割り出した手順",
        fig=("process", dict(
            # ⚠️ 「✕」は Noto に無い＝豆腐になる（`check_layout` が鳴った）
            steps=[dict(t="狙ったカメラ", d="2台とも動いていない", v="",
                        c=J.ALERT),
                   dict(t="別の場所のカメラ", d="映像を集める", v="", c=J.LINE),
                   dict(t="計算で割り出す", d="出どころの位置", v="", c=J.AMBER)],
            note=SRC3)),
    ),

    "c309": dict(
        t="タンクを向いた面から出ていた",
        s="煙が噴き出した向き",
        fig=("people", dict(
            nodes=[dict(x=0.22, y=0.34, t="右の補助ロケット", d="ある一方の面",
                        kind="part", c=J.ALERT),
                   dict(x=0.72, y=0.34, t="まん中の燃料タンク", d="大きいほう",
                        kind="part", c=J.LINE)],
            edges=[dict(a=0, b=1, t="ここから出た", c=J.ALERT)],
            note=SRC3)),
    ),

    "c310": dict(
        t="そのあと、八回くりかえした",
        s="くりかえし出た煙　1986年1月28日",
        photo=P("smoke_puffs"), **ss.kind(P("smoke_puffs")),
    ),

    # ⚠️ 「ほぼ同じ」を見せる＝棒にすると図が「同じだ」と言ってしまう。bar=False
    "c311": dict(
        t="揺れと、ぴったり合っていた",
        s="出る回数と、継ぎ目が動く回数",
        fig=("compare", dict(
            items=[dict(v=4, t="煙の出方", disp="約4", unit="回/秒", c=J.ALERT),
                   dict(v=4, t="継ぎ目の開け閉め", disp="約4", unit="回/秒",
                        c=J.LINE)],
            bar=False, note=SRC3)),
    ),

    "c312": dict(
        t="黒さが、焼けている印だった",
        s="煙の色が意味するもの",
        fig=("panel", dict(
            blocks=[dict(k="焼けた①", t="継ぎ目のグリース", v="", c=J.AMBER),
                    dict(k="焼けた②", t="断熱材", v="", c=J.AMBER),
                    dict(k="焼けた③", t="ゴムの輪", v="", c=J.ALERT)],
            cols=3, note=SRC3)),
    ),

    # ⚠️ 51-L ではなく、それまでの飛行の絵
    "c313": dict(
        t="この日にしか、出ていない",
        s="チャレンジャー号 41-C の打ち上げ　1984年4月",
        photo=P("past_launch"), **ss.kind(P("past_launch")),
    ),

    # ⚠️ どちらかに寄せない
    "c314": dict(
        t="見えなくなった理由は、二つある",
        s="3.375秒より後について",
        fig=("beforeafter", dict(
            a=dict(k="見方①", t="漏れは続いていた",
                   lines=["噴煙にまぎれただけ"], v="", c=J.ALERT),
            b=dict(k="見方②", t="いったん ふさがった",
                   lines=["燃えかすが 栓になった"], v="", c=J.LINE),
            arrow=False,
            note=f"{SRC3}・{SRC4}（報告書は並べたままにしている）")),
    ),

    "c315": dict(
        t="ここから先が、荒れていた",
        s="上昇するチャレンジャー号　1986年1月28日",
        photo=P("ascent_1"), **ss.kind(P("ascent_1")),
        bias=0.45,
    ),

    "c316": dict(
        t="見こんだ範囲には収まっていた",
        s="上昇中の機体　1986年1月28日",
        photo=P("ascent_2"), **ss.kind(P("ascent_2")),
        bias=0.42,
    ),

    "c317": dict(
        t="強調して、やっと見える大きさ",
        s="58.788秒の炎　1986年1月28日",
        photo=P("flame_plume"), **ss.kind(P("flame_plume")),
        bias=0.45,
    ),

    "c318": dict(
        t="片方の圧力だけ、下がった",
        s="育っていく炎　1986年1月28日",
        photo=P("flame_plume_2"), **ss.kind(P("flame_plume_2")),
    ),

    # 🔴 決め所⑤
    "c319": dict(
        t="色と形が、急に変わった",
        s="64.660秒からの数秒",
        fig=("quote", dict(
            phrase="打ち上げから73.124秒。タンクが壊れはじめた",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=SRC3)),
    ),

    "c320": dict(
        t="ここで、底が抜けた",
        s="燃料タンクの破れ　1986年1月28日",
        photo=P("et_breach"), **ss.kind(P("et_breach")),
        bias=0.45,
    ),

    "c321": dict(
        t="下半分が、上へ突き上げた",
        s="タンクの中で起きた順番",
        fig=("process", dict(
            steps=[dict(t="ふたが落ちる", d="タンクのいちばん下", v="", c=J.ALERT),
                   dict(t="下半分が上がる", d="噴き出した液体水素の反動", v="",
                        c=J.AMBER),
                   dict(t="継ぎ目に食いこむ", d="同じころ 右の補助ロケットも当たる",
                        v="", c=J.ALERT)],
            note=SRC3)),
    ),

    "c322": dict(
        t="七十三・一三七秒で、壊れた",
        s="空中分解　1986年1月28日",
        photo=P("breakup_moment"), **ss.kind(P("breakup_moment")),
        bias=0.45,
    ),

}
