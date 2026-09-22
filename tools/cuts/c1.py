# -*- coding: utf-8 -*-
"""第1章 発射台は、凍っていた c101–c119（18カット・c104 は無い）。11本目（チャレンジャー号）。

■ 実写は 8/18（44.4%）。`check_script` が W を出す章だが、**これは台本の配分**（E ではない）。
  `c101` は動画（`footage.USE`）、`c105`・`c107`・`c109` は動く映像からの止め絵。

■ 🔴 この章で気をつけたこと
  1. **`c105` は額入り**（実効 470×479）。`ss.still()` が `boxes.json` から `trim` を引く。
  2. **`c113` はコロンビア号・1979年**（チャレンジャーではない）。副題で機体名と年を名乗る
     → [[feedback-subtitle-must-match-what-is-visible]]／[[feedback-fallback-stills-must-match-the-era]]
  3. **`c116` は管制室であって、可否を決めた会議室ではない。**「運用管理チーム」と名乗らない。
  4. `c102` の気温は**曲線を描かない**（報告書にあるのは「底が摂氏マイナス6度・11時間」だけ）。
     勝手な折れ線を引くと、実測でない形が画面で数字のように見える
     → [[feedback-charts-lie-with-their-defaults]]
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC5 = "報告書 第I巻 第V章"

SPEC = {

    # 射点39Bの機体。動画（footage.USE）
    "c101": dict(
        # ⚠️ 見出しを「前の日の、夕方から」にしない＝字幕の切り取り100%で `check_echo` が鳴る
        t="機体は、もう立っていた",
        s="射点39B　1986年1月27日",
        **ss.vid("c101", 1440, clip="pad", t=44),
    ),

    # ⚠️ 折れ線を描かない。分かっているのは「底」と「長さ」だけ
    "c102": dict(
        t="フロリダには、めずらしい冷えこみ",
        s="前の日の夜に出ていた予報",
        fig=("timeline", dict(
            events=[dict(t=1.5, top="冷えこみはじめ", t2="", c=J.LINE),
                    dict(t=12.5, top="打ち上げの朝", t2="", c=J.ALERT, big=True)],
            band=[dict(a=1.5, b=12.5, t="氷点下が11時間　底は摂氏マイナス6度",
                       c=J.INST)],
            t0=0, t1=14,
            ticks=[(0, "27日 夕方"), (7, "深夜"), (14, "28日 朝")],
            src=SRC5)),
    ),

    "c103": dict(
        t="いつもの手が、使えなかった",
        s="発射台の水の配管　寒い日のあつかい",
        fig=("beforeafter", dict(
            a=dict(k="ふだんの寒い日", t="水を全部抜く",
                   lines=["配管が凍らない"], v="", c=J.OK),
            b=dict(k="この夜", t="抜けなかった",
                   lines=["翌朝が打ち上げだった"], v="", c=J.ALERT),
            arrow=False,
            note=SRC5)),
    ),

    # 🔴 額入り（実効 470×479）。ss.still が boxes.json から trim を引く
    "c105": dict(
        t="薬を入れても、凍った",
        s="発射台の下の水受け　1986年1月28日朝",
        **ss.still("ice_trough", "t_ice", 9),
    ),

    "c106": dict(
        t="三つが重なった",
        s="塔に氷がついた道すじ",
        fig=("people", dict(
            # ⚠️ 札が1行だけだと枠の内側が空く（`check_box` が 33% で鳴った）。d を足す
            nodes=[dict(x=0.14, y=0.20, t="細く流した水", d="配管を守るため",
                        kind="part", c=J.LINE),
                   dict(x=0.14, y=0.50, t="氷点下の気温", d="夜のあいだ",
                        kind="part", c=J.LINE),
                   dict(x=0.14, y=0.80, t="強い風", d="吹きつづけた",
                        kind="part", c=J.LINE),
                   dict(x=0.72, y=0.50, t="塔についた氷", d="大量", kind="part",
                        c=J.ALERT)],
            edges=[dict(a=0, b=3, c=J.LINE), dict(a=1, b=3, c=J.LINE),
                   dict(a=2, b=3, c=J.LINE)],
            # 🔴🔴 2026-09-22 ⑤c'（10-4）：節4つ・矢印3本だと段は「矢印を全部 →
            #    節を全部」の7つになり、**矢印3本が x≈1175 で切れて受け手が居ない**
            #    絵が長く出る（4つ目の節は最後の段）。9本目 `c718`（E-03）と同じ形。
            #    `pair=True` で矢印を**あとに出るほうの端**にぶら下げる＝段は4つ。
            pair=True,
            note=SRC5)),
    ),

    "c107": dict(
        t="地上二十九メートルから上",
        s="固定塔についた氷　1986年1月28日朝",
        **ss.still("ice_icicle_2", "t_ice", 23),
    ),

    "c108": dict(
        t="逃げ道の床が、凍っていた",
        s="発射台の氷　1986年1月28日",
        photo=P("ice_egress"), **ss.kind(P("ice_egress")),
        bias=0.5,
    ),

    "c109": dict(
        t="使えなくなった箱があった",
        s="地上の通信箱　1986年1月28日朝",
        **ss.still("ice_box", "t_ice", 18),
    ),

    # ⚠️ 481×600＝小さい。縦長なので ss.kind が額装に回す
    "c110": dict(
        t="見つけたのは、見まわる班",
        s="氷と霜の点検　ケネディ宇宙センター",
        photo=P("ice_team"), **ss.kind(P("ice_team")),
    ),

    # 🔴 決め所②
    "c111": dict(
        t="理屈は通っていた。ただ",
        s="配管を守るために水を流したこと",
        fig=("quote", dict(
            phrase="このやり方は、前例がなかった",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=SRC5)),
    ),

    "c112": dict(
        t="朝いちばんの会議にかかった",
        # ⚠️ 副題を「打ち上げの可否を決める会議」にしない＝字幕の切り取り100%
        s="氷が議題になった朝",
        fig=("moment", dict(
            clock="09:00",
            label="1986年1月28日",
            facts=[dict(t="かけられたこと", v="発射台の氷", c=J.ALERT),
                   dict(t="決める場", v="運用管理チーム", c=J.INST)],
            sub=SRC5)),
    ),

    # ⚠️ コロンビア号・1979年。チャレンジャーではない
    "c113": dict(
        t="心配したのは、作った会社",
        s="オービタの断熱タイル　コロンビア号・1979年",
        photo=P("rockwell_orbiter"), **ss.kind(P("rockwell_orbiter")),
        bias=0.5,
        # 🔴 2026-09-22 ⑤c'（10-6）：翼の上面の **`United` が文字高 約120px** で画面右上を
        #    占めていた。主役は副題どおり**断熱タイルを並べる作業**（下半分）なので、
        #    英字と星条旗の帯（元画像の y 0.15〜0.36）を**上から切り落とす**。
        # ⚠️ 切ったあと 1525x748（横長 2.04）で、覆いは横を 6.4% 落とすだけ＝作業の手元は残る。
        #    拡大は 1.44倍（`crop_probe` で実測）。
        trim=(0.0, 0.37, 1.0, 1.0),
    ),

    "c114": dict(
        t="当たり方は、三通り考えられた",
        s="氷が本体に当たる道すじ",
        fig=("panel", dict(
            blocks=[dict(k="一つ", t="風で飛ぶ", v="発射台の上の氷", c=J.LINE),
                    dict(k="二つ", t="点火で跳ねる", v="主エンジン", c=J.AMBER),
                    dict(k="三つ", t="吸いこまれる", v="補助ロケット", c=J.ALERT)],
            cols=3, note=SRC5)),
    ),

    "c115": dict(
        t="作った側が、会議に伝えた",
        # ⚠️ 副題に図の札と同じ語を入れない（`check_dup`）。ここは「どこからどこへ」だけ
        s="申し入れは、どこからどこへ",
        fig=("people", dict(
            nodes=[dict(x=0.17, y=0.36, t="ロックウェル", d="宇宙輸送部門の社長",
                        kind="org", c=J.INST),
                   dict(x=0.74, y=0.36, t="NASA", d="可否を決める側",
                        kind="org", c=J.LINE)],
            edges=[dict(a=0, b=1, t="この条件での打ち上げは初めてだ", c=J.ALERT)],
            note=SRC5)),
    ),

    # ⚠️ 管制室の写真。可否を決めた会議室ではない（副題で名乗らない）
    "c116": dict(
        t="立場は、副社長から伝わった",
        s="打ち上げの日の管制室　1986年1月28日",
        photo=P("mmt_meeting"), **ss.kind(P("mmt_meeting")),
        bias=0.46,
    ),

    "c117": dict(
        # ⚠️ 見出しが図の札の写しにならないようにする（実測で92%覆っていた）
        t="弱めるのを、自分でやめた",
        s="副社長が会議に伝えた言い方",
        fig=("beforeafter", dict(
            a=dict(k="はじめ", t="百パーセントは", lines=["という逃げ道があった"],
                   v="", c=J.LINE),
            b=dict(k="言いなおし", t="その七文字が消えた",
                   lines=["言い切る形になった"], v="", c=J.ALERT),
            arrow=True,
            note=SRC5)),
    ),

    "c118": dict(
        t="止めるとまでは、言わなかった",
        s="副社長の言い方について",
        fig=("panel", dict(
            blocks=[dict(k="言った", t="安全だとは請け合えない", v="", c=J.ALERT),
                    dict(k="言わなかった", t="打ち上げをやめろ", v="", c=J.LINE)],
            cols=2, note=f"{SRC5}（委員会は「あいまいだった」と書いている）")),
    ),

    "c119": dict(
        t="証明する向きが、逆だった",
        s="委員会が書いた、この朝のやり方",
        fig=("beforeafter", dict(
            a=dict(k="本来", t="安全だと示させる", lines=["示せなければ飛ばさない"],
                   v="", c=J.OK),
            b=dict(k="この朝", t="危険だと示させる", lines=["示せなければ飛ぶ"],
                   v="", c=J.ALERT),
            arrow=False,
            note=f"{SRC5}（氷そのものは原因ではない、とも書いている）")),
    ),

}
