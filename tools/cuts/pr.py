# -*- coding: utf-8 -*-
"""冒頭の引き pr01–pr11（11カット）。11本目（チャレンジャー号・STS-51-L）。

■ この11カットの役目
  **46秒より前に「氷」と「教師」を出す**（→ 記憶 [[feedback-jiko-plain-language]]・
  冒頭46秒で21〜42%が消える＝[[reference-jiko-third-video-numbers]]）。
  pr01 氷 → pr02 打ち上げ → pr03 壊れる → pr04 決め所 → pr05 教師、の順。

■ 実写は 6/11（55%）
  `pr01` は動く映像からの止め絵、`pr02`・`pr07` は動画（`footage.USE`）。
  ⚠️ **`pr01` に当てるコマは⑤c-3 で決め直す**＝いまは 元1119秒（氷に覆われた配管・全画面）。
     台本の言葉は「発射塔に下がったつらら」なので 元1133秒（構造材のつらら）のほうが近いが、
     **1133 は額入り（473×479）**。2コマ並べて決める → `ref/ep11/photo_picks.md` §2-2

■ ⚠️ 図が台本より先に答えを出さない
  `pr06` に「1985年7月」を書かない（`c209` が言う）。`pr08` に継ぎ目の温度を書かない（`c518`）。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC2 = "報告書 第I巻 第II章"
SRC3 = "報告書 第I巻 第III章"
SRC4 = "報告書 第I巻 第IV章"
SRC5 = "報告書 第I巻 第V章"

SPEC = {

    # 氷。**1カット目**。動く映像（カラーの記録映画）からの止め絵
    # ⚠️ 見出しに「発射台は、凍っていた」と書かない＝**第1章の章名と同じ**うえ、
    #    `check_echo` が「字幕の尻をそのまま切り取っている」で鳴る（実測30%）
    "pr01": dict(
        t="打ち上げの朝、氷がついた",
        s="打ち上げ当日の朝　1986年1月28日",
        **ss.still("ice_icicle", "t_ice", 14),
    ),

    # 打ち上げ。動画（footage.USE）
    "pr02": dict(
        t="二十五回目の打ち上げ",
        s="午前11時38分　ケネディ宇宙センター",
        **ss.vid("pr02", 1440, clip="launch", t=19),
    ),

    "pr03": dict(
        t="七十三秒しか、飛べなかった",
        s="空中で分解した機体　1986年1月28日",
        photo=P("accident_breakup"), **ss.kind(P("accident_breakup")),
        bias=0.45, side="right",
    ),

    # 🔴 決め所①。★の行と同時に出す（with_last）
    "pr04": dict(
        t="前の夜、反対されていた",
        s="打ち上げの可否を決めた電話会議",
        fig=("quote", dict(
            phrase="技術者は、ひとりも賛成しなかった",
            who="補助ロケットを作った会社の技術者",
            to="NASA と会社の経営側",
            when="1986年1月27日 夜",
            doc=SRC5)),
    ),

    "pr05": dict(
        t="七人のうち、二人は民間から",
        s="STS-51-L の乗員　公式肖像　1985年",
        photo=P("crew_portrait"), **ss.kind(P("crew_portrait")),
        bias=0.42,
    ),

    # ⚠️ 「1985年7月」は c209 が言う。ここでは長さだけ見せる
    "pr06": dict(
        t="教える人が、乗員になった",
        # ⚠️ 副題に「打ち上げ」を入れない＝図の札と同語で `check_dup` が鳴る
        s="七人目が決まってから、当日まで",
        fig=("timeline", dict(
            events=[dict(t=0, top="乗員に加わる", t2="中学・高校の教師", c=J.LINE),
                    dict(t=6, top="打ち上げ", t2="", c=J.ALERT, big=True)],
            t0=-0.7, t1=6.7,
            ticks=[(0, "0"), (3, "3か月"), (6, "6か月")],
            src=SRC2)),
    ),

    # 継ぎ目とゴムの輪。動画（footage.USE）
    "pr07": dict(
        t="太さ七ミリの、ゴムの輪",
        s="補助ロケットの継ぎ目　記録映像より",
        **ss.vid("pr07", 1440, clip="joint", t=30),
    ),

    # ⚠️ 継ぎ目の温度（c518）は書かない。ここは気温だけ
    "pr08": dict(
        t="いちばん寒い朝だった",
        s="打ち上げたときの気温　過去25回との比べ",
        fig=("compare", dict(
            items=[dict(v=2.2, t="この日", disp="2.2", unit="℃", c=J.ALERT),
                   dict(v=10.5, t="それまででいちばん低かった日",
                        disp="10.5", unit="℃", c=J.LINE)],
            vmax=14,
            note=f"摂氏。華氏では 36 と 51　{SRC3}・{SRC4}")),
    ),

    "pr09": dict(
        t="逃げる道まで、凍った",
        s="発射台にできた氷　1986年1月28日",
        photo=P("ice_pad"), **ss.kind(P("ice_pad")),
        bias=0.5,
    ),

    "pr10": dict(
        t="当たったのは、原文そのもの",
        s="画面に出す数字と言葉の出どころ",
        fig=("panel", dict(
            blocks=[dict(k="資料", t="大統領委員会の報告書", v="第I巻", c=J.DOC),
                    dict(k="出た日", t="1986年6月6日", v="", c=J.INST),
                    dict(k="読み方", t="英語の原文で全文", v="", c=J.LINE)],
            cols=3, note="Report of the Presidential Commission on the "
                         "Space Shuttle Challenger Accident, Vol. I")),
    ),

    "pr11": dict(
        t="この先、二つを追いかける",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="ひとつ", t="ゴムの輪", v="ふさげなかったわけ", c=J.ALERT),
                    dict(k="ふたつ", t="前の夜の会議", v="覆ったわけ", c=J.INST)],
            cols=2, note=f"{SRC4}・{SRC5}")),
    ),

}
