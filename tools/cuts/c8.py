# -*- coding: utf-8 -*-
"""第8章 二十四回、うまくいっていた c801–c820（20カット）。11本目（チャレンジャー号）。

■ 🔴 **17カットしか書けていません。**次の3つは**まだ写真の当てが無い**：
     `c803` joint_qual_test／`c804` srm_horizontal／`c810` srm_nozzle_51b
   → `ref/ep11/photo_picks.md` §3-1

■ 実写 6/20（30%）。`c819` は動く映像からの止め絵。

■ 🔴 この章で気をつけたこと
  1. **委員は実名**（`c816` のリチャード・ファインマン）。会議の出席者とは扱いが違う。
  2. ⚠️ **`c817` を回転式の弾倉の絵にしない。**型としては `icons` で描けるが、
     7人が亡くなった事故で**遊びに見える絵**は置かない。工程として言葉で見せる。
  3. ⚠️ **`c807` に散布図を描かない。**報告書の点をこちらで打ち直すことになり、
     実測でない形が数字のように見える → [[feedback-charts-lie-with-their-defaults]]。
     ここは「並べ方を変えると見える」という**やり方の話**なので、対比で見せる。
  4. `c806` の決め所が数字を出すので、`c807` はその数字を繰り返さない。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC4F = "報告書 第I巻 第IV章 Findings"
SRC6 = "報告書 第I巻 第VI章"
SRC6F = "報告書 第I巻 第VI章 Findings"
SRC7F = "報告書 第I巻 第VII章 Findings"

SPEC = {

    "c801": dict(
        t="もっと前から、続いていた",
        s="報告書が見にいった範囲",
        fig=("beforeafter", dict(
            a=dict(k="ここまで読むと", t="一晩の判断の話に見える",
                   lines=[], v="", c=J.LINE),
            b=dict(k="報告書は", t="もっと前までさかのぼる",
                   lines=[], v="", c=J.ALERT),
            arrow=False,
            note=SRC6)),
    ),

    "c802": dict(
        # ⚠️ 見出し・副題が段の答え（v）をそのまま含むと `check_wording` A型が鳴る
        t="設計まで、さかのぼった",
        s="報告書が置いた題と、その中身",
        fig=("panel", dict(
            blocks=[dict(k="章の題", t="歴史に根ざした事故", v="第6章", c=J.DOC),
                    dict(k="さかのぼった先", t="継ぎ目の設計と、その扱い方",
                         v="十数年", c=J.INST)],
            cols=2, note=SRC6)),
    ),

    # ✅ 2026-09-22 ⑤c-3 で書いた。**実写カット**（NASA画像庫・MSFC）。
    # ⚠️ **1987年＝事故の後の撮影**。試験そのものの絵は当時と同じだが、年は副題で名乗る
    #    → [[feedback-subtitle-must-match-what-is-visible]]
    "c803": dict(
        t="問われたのは、試験のやり方",
        s="固体ロケットの燃焼試験　1987年・ユタ州",
        photo=P("joint_qual_test"), **ss.kind(P("joint_qual_test")),
        side="left", ann_y=300,
        # ⚠️ 長い句を注記の数値欄に入れない（Dela・48px 未満に漢字4字以上＝つぶれる）。
        # ⚠️ **ナレーションの文を写さない**（`check_echo` が85%一致で止めた）。
        #    代わりに、台本が言っていない**具体**を置く＝第V章の証言で照合ずみ：
        #    「It is a full-scale O-ring, full-scale groove, **in a scaled test device**」
        ann=[dict(t="試験に使ったもの", v="縮めた装置", vs=56, vc=J.ALERT,
                  d="実物大だったのは、ゴムの輪と溝だけ")],
    ),

    # ✅ 2026-09-22 ⑤c-3 で書いた。**実写カット**。この章でいちばん絵が効くカット。
    # 🔴🔴 **題名で採ると逆になった。**NASA画像庫 `7997301` は題も説明も
    #    「Qualification Motor-1」＝認証試験だが、**絵は砂漠の試験台に横たわる全尺モーター**で、
    #    まさに c804 が言う「横に寝かせて燃やしていた」そのものだった。
    #    → [[feedback-inventory-is-not-usable-material]]（絵が正本。題名で決めない）
    # ⚠️ 1979年＝**事故の前**の撮影。c804 が言う当時の試験のやり方と年が合う。
    "c804": dict(
        t="飛ぶ向きと、試す向きが違った",
        s="試験台に横たわる補助ロケット　1979年・ユタ州",
        photo=P("srm_horizontal"), **ss.kind(P("srm_horizontal")),
        side="right", ann_y=300,
        # ⚠️ **ナレーションの文を写さない**（`check_echo` が100%一致で止めた）。
        #    「同じ条件で確かめたことにはならない」はナレーションが言うので、図は向きだけ持つ。
        ann=[dict(t="飛ぶとき", v="立てて燃やす", vc=J.LINE),
             dict(t="試験のとき", v="横に寝かせて燃やす", vc=J.ALERT)],
    ),

    "c805": dict(
        t="毎回ではない。だが、たびたび",
        s="回収された継ぎ目の焼け跡　1986年",
        photo=P("oring_erosion"), **ss.kind(P("oring_erosion")),
    ),

    # 🔴 決め所⑮
    "c806": dict(
        t="気温で並べ直すと、出てきた",
        s="過去の打ち上げを、摂氏の温度順に見る",
        fig=("quote", dict(
            phrase="摂氏16.1度未満は、全部に跡があった",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=f"{SRC4F} 12")),
    ),

    # ⚠️ 数字は c806 が出した。ここは「並べ方」の話
    "c807": dict(
        t="並べ方を変えると、見えた",
        s="どの飛行を並べるか",
        fig=("beforeafter", dict(
            a=dict(k="跡が出た飛行だけ", t="関係が見えない",
                   lines=[], v="", c=J.LINE),
            b=dict(k="無事だった飛行も入れる", t="寒いほど跡が出ている",
                   lines=[], v="", c=J.ALERT),
            arrow=False,
            note=f"{SRC6F} 6")),
    ),

    "c808": dict(
        t="やった人が、いなかった",
        s="この並べ直しをした組織",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="NASA", d="並べ直していない", ok=False, c=J.ALERT),
                   dict(t="作った会社", d="並べ直していない", ok=False,
                        c=J.ALERT)],
            lead="事故が起きるまでに",
            note=f"{SRC6F} 6")),
    ),

    "c809": dict(
        t="慣れが、基準を動かした",
        s="くりかえされるうちに起きたこと",
        fig=("beforeafter", dict(
            a=dict(k="はじめ", t="出てはいけない跡",
                   lines=[], v="", c=J.ALERT),
            b=dict(k="くりかえすうち", t="出てもよい跡",
                   lines=["機体は無事に帰ってくる"], v="", c=J.AMBER),
            arrow=True,
            note=f"{SRC6F} 3")),
    ),

    # ✅ 2026-09-22 ⑤c-3 で書いた。**図で描く**（写真は当てない）。
    # 🔴🔴 **51-B のノズル継ぎ目の写真は、どの置き場にも無い**（NASA画像庫・Commons とも0件）。
    #    記録映画 元1592 に「ベル形の噴射口が2つ」写るコマがあるが、
    #    **前後のコマを見ても何の機体のどこかを確定できなかった**ので採らなかった
    #    → [[feedback-dont-state-inferences-as-findings]]（推測で副題を書かない）
    # 原文で照合ずみ（第VI章）：「the launch constraint was "put on after we saw the
    #    **secondary O-ring erosion on the [51-B] nozzle**"」
    # ⚠️ 継ぎ目は2種類ある＝**現地で組む継ぎ目**（c503・c505）と**噴射口の継ぎ目**（ここ）。
    #    第5章までずっと前者の話だったので、ここで**別の場所だと分かる図**にする。
    "c810": dict(
        t="焼けたのは、別の継ぎ目",
        s="噴射口の側にある継ぎ目　1985年",
        fig=("process", dict(
            steps=[dict(t="一次のゴムの輪", d="ふさげなかった", v="",
                        c=J.ALERT),
                   dict(t="二次のゴムの輪", d="控えのはずが、焼けた", v="",
                        c=J.ALERT),
                   dict(t="打ち上げを止める札", d="この継ぎ目に掛けられた", v="",
                        c=J.INST)],
            note=SRC6)),
    ),

    "c811": dict(
        t="掛かっているあいだの決まり",
        s="打ち上げを止める札の意味",
        fig=("panel", dict(
            blocks=[dict(k="いつ", t="可否を決める会議", v="毎回", c=J.INST),
                    dict(k="なにを", t="片づくまで説明する", v="", c=J.ALERT)],
            cols=2, note=SRC6)),
    ),

    "c812": dict(
        t="掛けたのは、自分だと述べた",
        s="委員会での証言　1986年",
        photo=P("mulloy_testimony"), **ss.kind(P("mulloy_testimony")),
        bias=0.45,
    ),

    "c813": dict(
        t="六回つづけて、外した",
        s="札が掛かったあとの打ち上げ",
        fig=("icons", dict(
            n=6, on=6, kind="dot", cols=6,
            lead="同じ人が免除した回数",
            note=SRC6)),
    ),

    "c814": dict(
        t="書面には、残っていた",
        s="作った会社の関係者の証言と、手紙",
        fig=("panel", dict(
            blocks=[dict(k="証言", t="札のことは知らない", v="全員", c=J.LINE),
                    dict(k="書面", t="番号が引かれていた", v="", c=J.ALERT)],
            cols=2, note=SRC6)),
    ),

    "c815": dict(
        t="三か月後、決まりを外した",
        s="区分を変えた年から",
        fig=("timeline", dict(
            events=[dict(t=0, top="区分を変える", t2="いちばん重い区分へ",
                         c=J.INST),
                    dict(t=3, top="決まりを外す", t2="必ず控えを持て、のほう",
                         c=J.ALERT, big=True)],
            t0=-0.6, t1=4.2,
            ticks=[(0, "1982年"), (3, "3か月後")],
            src=SRC6)),
    ),

    # 🔴 決め所⑯。委員は実名
    "c816": dict(
        t="積み重ね方を、こう呼んだ",
        s="委員会に加わった物理学者の言葉",
        fig=("quote", dict(
            phrase="ロシアンルーレットのようなものだ",
            who="リチャード・ファインマン",
            to="大統領委員会",
            when="1986年",
            doc=f"{SRC6F} 3")),
    ),

    # ⚠️ 弾倉の絵にしない。工程として言葉で見せる
    "c817": dict(
        t="前がうまくいったから、と下げる",
        s="この言葉が指していた手つき",
        fig=("process", dict(
            steps=[dict(t="引き金を引く", d="弾は一発だけ入っている", v="",
                        c=J.LINE),
                   dict(t="何も起きない", d="飛ばしても無事に帰る", v="",
                        c=J.AMBER),
                   dict(t="基準を下げる", d="前回うまくいったから", v="",
                        c=J.ALERT)],
            note=f"{SRC6F} 3")),
    ),

    "c818": dict(
        t="そこに、線を置いた",
        s="うまくいったこと と、くりかえすこと",
        fig=("panel", dict(
            blocks=[dict(k="認めたこと", t="今回は、うまくいった", v="",
                         c=J.OK),
                    dict(k="認めなかったこと", t="何度もやってよいこと", v="",
                         c=J.ALERT)],
            cols=2, note=f"{SRC6F} 3")),
    ),

    "c819": dict(
        t="見る人数は、減っていた",
        s="委員会の公聴会場　記録映像より",
        **ss.still("commission_room", "commission", 12),
    ),

    "c820": dict(
        t="自分の上司を、自分が検査する",
        s="ケネディとマーシャルでの置かれ方",
        fig=("people", dict(
            nodes=[dict(x=0.50, y=0.22, t="確かめられる側の組織", kind="org",
                        c=J.LINE),
                   dict(x=0.50, y=0.68, t="安全を確かめる部署", d="その下に置かれた",
                        kind="org", c=J.ALERT)],
            # ⚠️ 同じ2点のあいだに辺を2本引くと札が重なる（実測 170×26px）。1本にまとめる
            edges=[dict(a=1, b=0, t="下から上を検査する", c=J.ALERT)],
            note=f"{SRC7F} 2")),
    ),

}
