# -*- coding: utf-8 -*-
"""第6章 前の夜、あの部屋で c601–c622（22カット）。11本目（チャレンジャー号）。

■ 🔴🔴 **19カットしか書けていません。**次の3つは**まだ写真の当てが無い**：
     `c605` launch_51c（1985年1月の飛行）／`c606` oring_soot（黒く焼けた継ぎ目）／
     `c613` marshall_center（マーシャル宇宙飛行センター）
   → `ref/ep11/photo_picks.md` §3
   ⚠️ `c613` は Commons の HAER 航空写真が候補だが、**撮影年が取れていない**
      （LoC が403）。「問題なし」ではなく「未確定」として扱う
      → [[feedback-parsers-fail-closed]]

■ 実写 4/22（18.2%）＝**この動画でいちばん写真が薄い章**。会議の章なので絵が少ない。
  `c603` は動画（`footage.USE`）＝記録映画の「運ぶ・積む工程」（2026-09-21 カズヤくん決定）。

■ 🔴🔴 **会議の出席者は名前を出しません。**役で呼ぶ（2026-09-21 の決めごと）。
  「技術部門の副社長」「作った会社の責任者」「補助ロケットを見ていた部長」
  「補助ロケットの計画を率いていた責任者」。**乗員7人と委員だけが実名。**

■ ⚠️ `c622` の決め所は「**本人が『自分はこう読んだ』と紹介した版**」。
  本人の言葉として認めてはいない（台本 §2 の訂正）。副題でそう断る。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC5 = "報告書 第I巻 第V章"

SPEC = {

    "c601": dict(
        t="議題は、一つだけだった",
        s="三つの場所をつないだ電話会議",
        fig=("moment", dict(
            clock="17:45",
            label="1986年1月27日",
            facts=[dict(t="かけた側", v="補助ロケットを作った会社", c=J.INST),
                   dict(t="決めること", v="翌朝の可否", c=J.ALERT)],
            sub=SRC5)),
    ),

    "c602": dict(
        t="三つの州を、線でつないだ",
        s="電話でつながれた場所",
        fig=("mapfig", dict(
            # ⚠️ 正式名称をそのまま札にすると字幕の切り取りになる（`check_echo` 100%）。
            #    札は短い呼び名＋州にして、正式名称はナレーションに持たせる
            points=[dict(x=0.78, y=0.72, t="ケネディ", d="フロリダ", c=J.LINE),
                    dict(x=0.62, y=0.58, t="マーシャル", d="アラバマ", c=J.INST),
                    dict(x=0.20, y=0.34, t="工場", d="ユタ", c=J.ALERT)],
            note=f"{SRC5}（模式図。位置と縮尺は正確ではない）")),
    ),

    # 動画（footage.USE）。2026-09-21 カズヤくん決定で「運ぶ・積む工程」に変えた
    "c603": dict(
        t="心配したのは、作った側",
        s="輪切りの筒を積む工程　記録映像より",
        **ss.vid("c603", 1440, clip="srb", t=36),
    ),

    "c604": dict(
        t="そろっていない資料だった",
        s="その夜、二度かかった電話",
        fig=("timeline", dict(
            events=[dict(t=17.75, top="一度目", t2="もう延期を勧めている",
                         c=J.LINE),
                    dict(t=20.75, top="二度目", t2="資料を順に説明した",
                         c=J.ALERT, big=True)],
            t0=17.2, t1=22.0,
            ticks=[(18, "午後6時"), (20, "午後8時"), (22, "午後10時")],
            src=SRC5)),
    ),

    # 🔴 c605 は写真の当てが無い（launch_51c）
    # 🔴 c606 は写真の当てが無い（oring_soot）

    # 🔴 決め所⑩。この章の柱
    "c607": dict(
        t="紙にして、出した",
        s="その夜、文書で出された線",
        fig=("quote", dict(
            phrase="継ぎ目が摂氏11.7度より下では飛ばせない",
            who="技術部門の副社長",
            to="NASA と会社の経営側",
            when="1986年1月27日 夜",
            doc=SRC5)),
    ),

    "c608": dict(
        t="外へ出るな、という線",
        s="十一・七度がどこから来た数字か",
        fig=("beforeafter", dict(
            a=dict(k="これまでの内側", t="経験のある範囲",
                   lines=[], v="", c=J.OK),
            b=dict(k="その外側", t="分かっていない",
                   lines=["華氏でいえば53度"], v="", c=J.ALERT),
            arrow=False,
            note=SRC5)),
    ),

    "c609": dict(
        t="線の、はるか下だった",
        s="その夜に届いていた数字",
        fig=("compare", dict(
            items=[dict(v=11.7, t="技術者が引いた線", disp="11.7", unit="℃",
                        c=J.OK),
                   dict(v=-3.0, t="翌朝の予報", disp="−3", unit="℃", c=J.ALERT)],
            vmax=14, ref="摂氏",
            note=SRC5)),
    ),

    "c610": dict(
        t="この時点まで、ゼロだった",
        s="一度目からここまでの記録",
        fig=("absent", dict(
            mode="single",
            items=[dict(t="賛成した発言", d="一つも出ていない", ok=False,
                        c=J.ALERT)],
            lead="電話がはじまってから",
            note=f"{SRC5}（反対しつづけた技術者の証言）")),
    ),

    "c611": dict(
        t="会社としての答えも、同じだった",
        s="やりとりの向き",
        fig=("people", dict(
            # ⚠️ 同じ2点のあいだに辺を2本引くと札が重なる（実測 204×31px）。1本にまとめる
            nodes=[dict(x=0.20, y=0.36, t="NASA側", d="会社としてどうするのか",
                        kind="org", c=J.LINE),
                   dict(x=0.74, y=0.36, t="作った会社の責任者",
                        d="技術部門が勧めないから", kind="person", c=J.INST)],
            edges=[dict(a=0, b=1, t="問われ、断った", c=J.ALERT)],
            note=SRC5)),
    ),

    "c612": dict(
        t="ここで終わる はずだった",
        s="勧告が出たあとの向き",
        fig=("beforeafter", dict(
            a=dict(k="本来なら", t="ここで延期になる",
                   lines=["作った側が勧めていない"], v="", c=J.OK),
            b=dict(k="この夜", t="押し返された",
                   lines=[], v="", c=J.ALERT),
            arrow=True,
            note=SRC5)),
    ),

    # 🔴 c613 は写真の当てが無い（marshall_center）

    # 🔴 決め所⑪
    "c614": dict(
        t="その場で、強い言葉が返った",
        s="言われた相手は、だれか",
        fig=("quote", dict(
            phrase="あなたがたの勧告には、あきれている",
            who="補助ロケットを見ていた部長",
            to="補助ロケットを作った会社",
            when="1986年1月27日 夜",
            doc=SRC5)),
    ),

    "c615": dict(
        t="一度では、なかった",
        s="この発言について証言されたこと",
        fig=("panel", dict(
            blocks=[dict(k="別の出席者", t="何度もくり返された", v="", c=J.DOC),
                    dict(k="言われた側", t="空気が変わったと感じた", v="",
                         c=J.ALERT)],
            cols=2, note=SRC5)),
    ),

    "c616": dict(
        t="同じ人が、こうも言っている",
        s="あきれていると言った部長の、もう一つの発言",
        fig=("beforeafter", dict(
            a=dict(k="一方で", t="勧告にあきれている",
                   lines=[], v="", c=J.ALERT),
            b=dict(k="他方で", t="勧めないなら 飛ばさない",
                   lines=[], v="", c=J.OK),
            arrow=False,
            note=SRC5)),
    ),

    "c617": dict(
        t="もう一人の言い分",
        s="NASA側で発言した、二人目",
        fig=("panel", dict(
            blocks=[dict(k="だれが", t="計画を率いた側", v="", c=J.INST),
                    dict(k="言い分", t="新しい基準を今夜つくるのか", v="",
                         c=J.ALERT),
                    dict(k="力点", t="打ち上げの前の晩に", v="", c=J.AMBER)],
            cols=3, note=SRC5)),
    ),

    "c618": dict(
        t="いまの基準のままで来た",
        s="それまでの打ち上げの回数",
        fig=("icons", dict(
            n=24, on=24, kind="dot", cols=8,
            lead="いまの基準で成功してきた回数",
            note=SRC5)),
    ),

    "c619": dict(
        t="先が、見えなくなる",
        s="十一・七度を基準にした場合",
        fig=("timeline", dict(
            events=[dict(t=0, top="いま", t2="25回目の前の晩", c=J.LINE),
                    dict(t=4, top="次に飛べるのは", t2="何か月も先になりうる",
                         c=J.ALERT, big=True)],
            band=[dict(a=0, b=4, t="この あいだ 飛べない", c=J.ALERT)],
            t0=-0.5, t1=5.0,
            ticks=[(0, "0"), (2, "2か月"), (4, "4か月")],
            src=SRC5)),
    ),

    "c620": dict(
        t="二時間、押し問答がつづいた",
        s="だれが、いつ話したか",
        fig=("radio", dict(
            lanes=["ケネディ", "マーシャル", "ユタの工場"],
            events=[dict(lane=2, a=0, b=2, t="勧告を出す", c=J.INST),
                    dict(lane=1, a=2, b=4, t="押し返す", c=J.ALERT),
                    dict(lane=0, a=4, b=5, t="問いただす", c=J.LINE),
                    dict(lane=2, a=5, b=7, t="答える", c=J.INST)],
            t0=0, t1=8,
            note=f"{SRC5}（順番だけ。秒の資料は無い）")),
    ),

    "c621": dict(
        t="短い一言としても、残った",
        s="この言い分が伝わった道すじ",
        fig=("process", dict(
            steps=[dict(t="委員が引く", d="活字になった版", v="", c=J.DOC),
                   dict(t="本人が読み上げる", d="委員会の場で", v="", c=J.INST),
                   dict(t="断りを付ける", d="切り取られた引用だ", v="",
                        c=J.ALERT)],
            note=SRC5)),
    ),

    # 🔴 決め所⑫。⚠️ 本人の言葉として認めてはいない
    "c622": dict(
        t="相手を名指しした",
        s="本人が「自分はこう読んだ」と紹介した版",
        fig=("quote", dict(
            phrase="いつ打ち上げろというのか。来年の4月か",
            who="補助ロケットの計画を率いた責任者",
            to="補助ロケットを作った会社",
            when="1986年1月27日 夜",
            doc=SRC5)),
    ),

}
