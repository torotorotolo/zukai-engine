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
            vmax=36,
            note=f"実測　{SRC5}")),
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
        # 🔴🔴 2026-09-22 ⑤c'（10-5）：**19（元74）は使える帯 57〜71 の外**で、
        #    絵は WORLDNET のスタジオ座談だった（英字も30px級で出ていた）。
        #    10（元65）＝**公聴会の席で話す出席者の寄り**。副題「公聴会の席」に合う。
        # ⚠️ ショットの切れ目を自分で測った（1秒刻みの平均絶対差）：t=7 で 62.3 の変わり目、
        #    7〜11 は差 4〜14 の同じショット。c709（t=6）とは**平均差 62.5 ＝ 別の絵**。
        # ⚠️ 右端に `ROBERT …` の名札（部分・約30px）が写る。これは**委員の名札**で、
        #    記憶の規則は「乗員7人と委員は実名」なので画面に出てよい（⑤c' 判断）。
        #    名札は隣の席のもので、写っている人物の名を名乗ってはいない。
        # ⚠️ 2026-09-22 ⑤c''：焼いた絵から名札を切り出して読んだ。**読めるのは `ROBERT` の
        #    名だけで、姓は額の右端で切れている**＝「委員の名札」という ⑤c' の断定は
        #    ⑤c'' では裏が取れなかった（委員会にも Robert が2人いるが、
        #    サイオコールの技術部門副社長も Robert）。ただし**名が1語だけでは誰も特定できない**。
        # 🔴 切らずに残した理由（実測）：名札は額の x 0.756〜1.0、話している人は x 0.43〜0.73。
        #    右を 0.75 で切ると額の縦横比が変わり、**人物が右端に寄って絵が壊れる**。
        #    寄せ直すと元が記録映像（粒子が粗い）なので c902 と同じ壊し方になる。
        #    → **試写の要確認へ上げる**（[[feedback-jiko-qa-must-have-an-end]]）。
        **ss.still("commission_hearing_2", "commission", 10),
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

    # ✅ 2026-09-22 ⑤c-3 で書いた。**図で描く**（写真は当てない）。
    # 🔴🔴 送られた書面そのもの（報告書 第I巻 97頁）は**全文が英字の写し**なので画面に出さない
    #    ＝ `cuts/ss.py` の決まり。代わりに**どこからどこへ渡ったか**を図にする。
    #    原文で照合ずみ：「Hardy requested that it be sent in writing by telefax
    #    both to Kennedy and to Marshall, **and it was**」／
    #    「The conference was then terminated at **approximately 11:15**」（第V章）
    # ⚠️ **人の名前は出さない**（会議の出席者は役で呼ぶ・この回の決まり）。
    "c716": dict(
        t="口頭では、終わらせなかった",
        s="その夜、残った紙",
        fig=("people", dict(
            nodes=[dict(x=0.17, y=0.34, t="作った会社", d="打ち上げを勧める、と読み上げた",
                        kind="org", c=J.INST),
                   dict(x=0.50, y=0.64, t="ファクスの書面", d="午後11時15分ごろ、会議は終わった",
                        kind="doc", c=J.DOC),
                   dict(x=0.83, y=0.34, t="NASAの二か所", d="ケネディとマーシャルへ",
                        kind="org", c=J.LINE)],
            edges=[dict(a=0, b=1, t="書面にするよう求められた", c=J.ALERT),
                   dict(a=1, b=2, t="送られた", c=J.ALERT)],
            note=SRC5)),
    ),

}
