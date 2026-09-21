# -*- coding: utf-8 -*-
"""締め その後に残ったもの ep01–ep13（13カット）。11本目（チャレンジャー号）。

■ 🔴 **9カットしか書けていません。**次の4つは**まだ写真の当てが無い**：
     `ep02` joint_redesign／`ep03` joint_test_new／`ep04` srm_vertical_test／
     `ep07` oring_data_chart
   どれも**報告書の図でしか見たことのない主題**。→ `ref/ep11/photo_picks.md` §3-1

■ 実写 7/13（54%）。

■ 🔴 `ed01`（共通エンディング）は**ここには書きません。**
   `tools/narration.py` が持っていて、**⑥で足される**（`el_script.COMMON_TAIL`）。
   🔴🔴 **11本目から並べ替え**＝アイコン中央・少し大きく／高評価左／登録右
   → 記憶 [[project-jiko-common-ending]]。⑥で当てること。

■ ⚠️ `ep10`・`ep11` は**乗員7人の実名を置くカット**。会議の出席者とは扱いが違う。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC4 = "報告書 第I巻 第IV章"
SRC5 = "報告書 第I巻 第V章"
SRC6F = "報告書 第I巻 第VI章 Findings"
REC = "報告書 第I巻 勧告"

SPEC = {

    "ep01": dict(
        t="最後に、九つ置かれた",
        s="ロジャース委員会報告書　1986年6月6日",
        photo=P("commission_report"), **ss.kind(P("commission_report")),
    ),

    # 🔴 ep02 は写真の当てが無い（joint_redesign）
    # 🔴 ep03 は写真の当てが無い（joint_test_new）
    # 🔴 ep04 は写真の当てが無い（srm_vertical_test）

    "ep05": dict(
        t="外に、見る目を置く",
        s="委員会の公聴会　1986年",
        photo=P("commission_oversight"), **ss.kind(P("commission_oversight")),
        bias=0.45,
    ),

    # 🔴 決め所⑱。この動画の最後の決め所
    "ep06": dict(
        t="いちばん重いのは、そこではない",
        s="設計より前に、あったもの",
        fig=("quote", dict(
            phrase="記録を調べていれば、分かったはずだった",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=f"{SRC6F} 6")),
    ),

    # 🔴 ep07 は写真の当てが無い（oring_data_chart）

    "ep08": dict(
        t="飛ぶ人を、決める側へ",
        s="委員がケネディ宇宙センターに着く　1986年",
        photo=P("astronaut_manager"), **ss.kind(P("astronaut_manager")),
        bias=0.45,
    ),

    "ep09": dict(
        t="助言の場も、求めている",
        s="委員会の到着　ケネディ宇宙センター・1986年",
        photo=P("safety_panel"), **ss.kind(P("safety_panel")),
        bias=0.45,
    ),

    "ep10": dict(
        t="名前を、もう一度",
        s="追悼式　ヒューストン・1986年",
        photo=P("memorial_wreath"), **ss.kind(P("memorial_wreath")),
        bias=0.45,
    ),

    "ep11": dict(
        t="生中継で、二回の予定だった",
        s="STS-51-L の乗員　1986年",
        photo=P("crew_portrait_3"), **ss.kind(P("crew_portrait_3")),
        bias=0.44,
    ),

    "ep12": dict(
        t="冷たさが、道をふさいだ",
        s="一つ目の問いへの答え",
        fig=("process", dict(
            steps=[dict(t="冷えて硬くなる", d="ゴムの輪", v="", c=J.ALERT),
                   dict(t="つぶれきる", d="押す空気も入らない", v="", c=J.ALERT),
                   dict(t="間に合わない", d="開いていくすきまに", v="",
                        c=J.AMBER)],
            note=SRC4)),
    ),

    "ep13": dict(
        t="その夜だけ、逆さまだった",
        s="二つ目の問いへの答え",
        fig=("beforeafter", dict(
            a=dict(k="ふだん", t="飛べると示す側",
                   lines=["示せなければ飛ばない"], v="", c=J.OK),
            b=dict(k="その夜", t="飛べないと示す側",
                   lines=["示せなければ飛ぶ"], v="", c=J.ALERT),
            arrow=False,
            note=SRC5)),
    ),

}
