# -*- coding: utf-8 -*-
"""第4章 それは「爆発」ではなかった c401–c414（14カット）。11本目（チャレンジャー号）。

■ 実写 6/14（42.9%）。`c413` は動画（`footage.USE`）。

■ 🔴 この章で気をつけたこと
  1. **`c402` に三つの段階を並べない。**一つ目は `c403`、二つ目は `c405`、
     三つ目が**決め所 `c408`** なので、図が先に答えを出すと決め所が死ぬ。
     数（三つ）だけを見せる。
  2. ⚠️ **`c403` と `c406` は同じ1枚**（置き場に「燃える水素」だけの絵が無い）。
     寄りを変えて使う。🔴 ⑤c-3 で**2コマ並べて、別の絵に見えるか**を確かめる
     → `ref/ep11/photo_picks.md` §3-2
  3. **「爆発ではない」と言い切らない。**`c409` で空軍の安全担当官の言葉を並べる
     （台本がそう書いている）。
  4. `c414` は**章の橋**＝副題は「ここまでと、この先」でそろえる
     → `tools/cuts/README.md` §5-2
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC2 = "報告書 第I巻 第II章"
SRC3 = "報告書 第I巻 第III章"
SRC4 = "報告書 第I巻 第IV章"

SPEC = {

    "c401": dict(
        t="この言葉で、記憶に残った",
        s="空に広がった火の玉　1986年1月28日",
        photo=P("fireball_wide"), **ss.kind(P("fireball_wide")),
        bias=0.42,
    ),

    # ⚠️ 三つの中身は書かない（c403・c405・c408 が出す）
    "c402": dict(
        t="報告書は、分けて書いている",
        s="起きたことの数えかた",
        fig=("icons", dict(
            n=3, on=0, kind="dot", cols=3,
            lead="報告書が分けた段階",
            note=SRC3)),
    ),

    # ⚠️ c406 と同じ1枚。寄りを変えている
    "c403": dict(
        t="噴き出した水素が、燃えた",
        s="タンクから漏れた水素　1986年1月28日",
        photo=P("hydrogen_burn"), **ss.kind(P("hydrogen_burn")),
        bias=0.32, xbias=0.38, zoom=1.35,
    ),

    "c404": dict(
        t="一瞬の破裂とは、分けている",
        s="報告書が使った言い方",
        fig=("beforeafter", dict(
            a=dict(k="爆弾なら", t="一瞬で破裂する",
                   lines=["ごく短い時間で終わる"], v="", c=J.LINE),
            b=dict(k="報告書の言い方", t="爆発的な燃焼",
                   lines=["ほとんど爆発に近い、とも書いている"], v="", c=J.ALERT),
            arrow=False,
            note=SRC3)),
    ),

    "c405": dict(
        t="三つをつなぐ、背骨だった",
        s="燃料タンクが受け持っていた役目",
        fig=("people", dict(
            nodes=[dict(x=0.50, y=0.30, t="まん中の燃料タンク", d="背骨にあたる",
                        kind="part", c=J.ALERT),
                   dict(x=0.16, y=0.74, t="左の補助ロケット", kind="part", c=J.LINE),
                   dict(x=0.84, y=0.74, t="右の補助ロケット", kind="part", c=J.LINE),
                   dict(x=0.50, y=0.74, t="人が乗る本体", kind="part", c=J.INK_W)],
            edges=[dict(a=0, b=1, c=J.LINE), dict(a=0, b=2, c=J.LINE),
                   dict(a=0, b=3, c=J.LINE)],
            note=f"{SRC3}・{SRC4}")),
    ),

    # ⚠️ c403 と同じ1枚。こちらは引き
    "c406": dict(
        t="高さ一万四千メートル",
        s="火の玉　1986年1月28日",
        photo=P("fireball"), **ss.kind(P("fireball")),
        bias=0.5,
    ),

    "c407": dict(
        t="支えを失って、壁に入った",
        s="音より速いときの空気の効き方",
        fig=("beforeafter", dict(
            a=dict(k="背骨があるうち", t="力を受けとめる",
                   lines=["三つがつながっている"], v="", c=J.OK),
            b=dict(k="失ったあと", t="受けとめられない",
                   lines=["空気は壁のように固い"], v="", c=J.ALERT),
            arrow=True,
            note=SRC3)),
    ),

    # 🔴 決め所⑥。この章の柱
    "c408": dict(
        # ⚠️ 見出し・副題を字幕から切り取らない（実測92%・89%で鳴った）
        t="三つ目が、いちばん大事",
        s="機体の壊れ方について",
        fig=("quote", dict(
            phrase="本体は、空気の力でばらばらになった",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=SRC3)),
    ),

    "c409": dict(
        t="政府の側も、その言葉を使った",
        s="事故の直後に出された報告",
        fig=("panel", dict(
            blocks=[dict(k="報告書の書き方", t="三つに分けて書く", v="", c=J.DOC),
                    dict(k="空軍の安全担当官", t="機体が爆発した", v="", c=J.ALERT)],
            # ⚠️ note に字幕の文を入れない（実測100%で鳴った）
            cols=2, note=SRC2)),
    ),

    "c410": dict(
        t="いくつもの塊が、出てきた",
        s="火の玉から出る機体のかけら　1986年1月28日",
        photo=P("breakup_sections"), **ss.kind(P("breakup_sections")),
        bias=0.45,
    ),

    "c411": dict(
        t="引きずっていたものがあった",
        s="映像と残骸が、そろえた順番",
        fig=("process", dict(
            steps=[dict(t="出てくる", d="前の胴体", v="", c=J.INK_W),
                   dict(t="引きずる", d="ちぎれた配管の束", v="", c=J.ALERT),
                   dict(t="そろう", d="海から上がったかけら", v="", c=J.OK)],
            note=SRC3)),
    ),

    "c412": dict(
        t="燃えたまま、飛びつづけた",
        s="二本の補助ロケット　1986年1月28日",
        photo=P("srb_trails"), **ss.kind(P("srb_trails")),
        bias=0.45,
    ),

    # 動画（footage.USE）
    "c413": dict(
        t="百十秒後、外から壊した",
        s="破壊されたあとの筋　記録映像より",
        **ss.vid("c413", 1440, clip="accident", t=49),
    ),

    # 章の橋
    "c414": dict(
        t="ここまでが、起きたこと",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="ここまで", t="打ち上げから2分足らず", v="第4章",
                         c=J.LINE),
                    dict(k="次に見ること", t="なぜ、そうなったのか", v="第5章",
                         c=J.ALERT)],
            cols=2, note=SRC4)),
    ),

}
