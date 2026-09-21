# -*- coding: utf-8 -*-
"""第7章 帽子を、かけかえる c701–c716（16カット）。11本目（チャレンジャー号）。

■ 🔴 **15カットしか書けていません。**`c716` thiokol_telefax（送られた書面）は
   **まだ写真の当てが無い**。→ `ref/ep11/photo_picks.md` §3

■ 実写 5/16（31.2%）。`c709` は動画（`footage.USE`）、`c710` は動く映像からの止め絵。

■ 🔴🔴 **会議の出席者は名前を出しません**（第6章と同じ）。
  「会社の上級副社長」「技術部門の副社長」「反対しつづけた技術者」。

■ ⚠️ `c707` の決め所は**この事故でもっともよく引かれる言葉**。章名も「帽子」なので、
   副題・図の札に「帽子」を重ねない（画面に三度出ることになる）。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC5 = "報告書 第I巻 第V章"

SPEC = {

    "c701": dict(
        t="音を消して、内だけで話す",
        s="作った会社の側が求めたこと",
        fig=("panel", dict(
            blocks=[dict(k="求めたこと", t="5分の中断", v="", c=J.INST),
                    dict(k="そのあいだ", t="工場の側だけで相談", v="", c=J.LINE)],
            cols=2, note=SRC5)),
    ),

    "c702": dict(
        t="求めた長さの、六倍",
        s="中断が実際につづいた長さ",
        fig=("compare", dict(
            items=[dict(v=5, t="求めた長さ", disp="5", unit="分", c=J.LINE),
                   dict(v=30, t="実際", disp="約30", unit="分", c=J.ALERT)],
            vmax=36, ref="実測",
            note=SRC5)),
    ),

    "c703": dict(
        t="切り出したのは、経営の側",
        s="中断のあいだ、部屋で起きたこと",
        fig=("process", dict(
            steps=[dict(t="音を消す", d="三つの場所から切れる", v="", c=J.LINE),
                   dict(t="上級副社長が切り出す", d="経営の判断だ、と", v="",
                        c=J.ALERT),
                   dict(t="話が移る", d="技術の話から", v="", c=J.AMBER)],
            note=f"{SRC5}（出席者の証言）")),
    ),

    "c704": dict(
        t="二人は、引かなかった",
        s="中断のあいだも反対した技術者",
        fig=("panel", dict(
            blocks=[dict(k="人数", t="反対しつづけた技術者", v="2人",
                         c=J.ALERT),
                    dict(k="理由", t="くつがえる理由が示されない", v="",
                         c=J.LINE)],
            cols=2, note=SRC5)),
    ),

    "c705": dict(
        t="焼けた跡を、持って前へ",
        s="回収された継ぎ目の焼け跡　1986年",
        photo=P("oring_erosion_photo"), **ss.kind(P("oring_erosion_photo")),
    ),

    "c706": dict(
        t="途中で、二人ともやめた",
        s="説明をやめた理由",
        fig=("beforeafter", dict(
            a=dict(k="はじめ", t="説明しようとした",
                   lines=["絵を描きなおし、写真を出した"], v="", c=J.LINE),
            b=dict(k="途中で", t="やめた",
                   lines=["届かないと悟った"], v="", c=J.ALERT),
            arrow=True,
            note=f"{SRC5}（本人たちの証言）")),
    ),

    # 🔴 決め所⑬。この動画でもっともよく引かれる言葉
    "c707": dict(
        t="いちばん有名な一言",
        # ⚠️ 副題に役の名を書くと、引用の札と同語になり `check_dup` が鳴る
        s="中断のあいだに、部屋で言われた",
        fig=("quote", dict(
            phrase="技術者の帽子を脱いでくれ",
            who="会社の上級副社長",
            to="技術部門の副社長",
            when="1986年1月27日 夜",
            doc=SRC5)),
    ),

    "c708": dict(
        t="ここから先は、経営だけで",
        s="この一言のあとに起きたこと",
        fig=("beforeafter", dict(
            a=dict(k="それまで", t="技術の側で組み立てる",
                   lines=[], v="", c=J.LINE),
            b=dict(k="ここから", t="経営の側だけで組み立てる",
                   lines=["続きは「経営者のほうをかぶれ」"], v="", c=J.ALERT),
            arrow=True,
            note=SRC5)),
    ),

    # ⚠️ 動画にしない＝使える帯が 元59〜64 の5秒だけ（64〜66秒に未特定の名札）で、
    #    尺 9.92秒だと 0.50倍速になる。止め絵で置く（実写の数は変わらない）
    "c709": dict(
        t="最後の資料づくりに、呼ばれない",
        s="委員会の証人席　記録映像より",
        **ss.still("commission_testimony", "commission", 6),
    ),

    "c710": dict(
        t="すぐには、答えなかった",
        s="公聴会の席　記録映像より",
        **ss.still("commission_hearing_2", "commission", 19),
    ),

    "c711": dict(
        t="いつもは、説明する側だった",
        s="ふだんの役まわり",
        fig=("people", dict(
            nodes=[dict(x=0.20, y=0.36, t="作った会社", d="飛べる状態だと説明する",
                        kind="org", c=J.INST),
                   dict(x=0.74, y=0.36, t="NASA側", d="納得する側", kind="org",
                        c=J.LINE)],
            edges=[dict(a=0, b=1, t="長いあいだ、この向き", c=J.OK)],
            note=SRC5)),
    ),

    "c712": dict(
        t="その夜だけ、様子が違った",
        s="返ってきた言葉のたぐい",
        fig=("beforeafter", dict(
            a=dict(k="いつも", t="聞き慣れた問い",
                   lines=[], v="", c=J.LINE),
            b=dict(k="その夜", t="聞いたことのない種類",
                   lines=[], v="", c=J.ALERT),
            arrow=False,
            note=SRC5)),
    ),

    "c713": dict(
        t="言い切れなければ、飛ぶ",
        s="その夜、負わされた側",
        fig=("process", dict(
            steps=[dict(t="役が入れ替わる", d="示す側が逆になる", v="",
                        c=J.ALERT),
                   dict(t="示しきれない", d="絶対に壊れるとは言えない", v="",
                        c=J.AMBER),
                   dict(t="打ち上げへ", d="止まらなくなる", v="", c=J.ALERT)],
            note=SRC5)),
    ),

    # 🔴 決め所⑭
    "c714": dict(
        t="気づくべきだった、と述べた",
        s="のちに委員会で問われて",
        fig=("quote", dict(
            phrase="証明する側が、入れ替わっていた",
            who="技術部門の副社長",
            to="大統領委員会",
            when="1986年",
            doc=SRC5)),
    ),

    "c715": dict(
        t="再開は、午後十一時ごろ",
        s="つながった会議室　1986年1月",
        photo=P("telecon_room"), **ss.kind(P("telecon_room")),
    ),

    # 🔴 c716 は写真の当てが無い（thiokol_telefax）

}
