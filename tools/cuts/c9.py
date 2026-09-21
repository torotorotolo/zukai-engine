# -*- coding: utf-8 -*-
"""第9章 海から上がったもの c901–c916（16カット）。11本目（チャレンジャー号）。

■ 実写 14/16（88%）＝**この動画でいちばん写真が濃い章**（第2章と並ぶ）。
  `c911`・`c912` は動く映像からの止め絵。

■ 🔴 この章で気をつけたこと
  1. ⚠️ **`c905` は `c705` と同じ1枚**（O-Ring Tracks）。寄りを変えて使う。
     🔴 ⑤c-3 で2コマ並べて、別の絵に見えるか確かめる。
  2. ⚠️ **`c915` に写っているのは半旗**であって、乗員ではない。副題で半旗と名乗る
     → [[feedback-subtitle-must-match-what-is-visible]]
  3. 🔴 **`c913`（追悼式）は報告書 第I巻の外**。画面に出るのは写真の出典（NASA）で、
     話の裏取りは第I巻に無い。⚠️ 出典が取れなければカットごと落とす（台本の指示）。
  4. **`c916` は「書いていないことは書かない」と宣言するカット。**
     亡くなり方を図にしない。空欄として見せる。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC3 = "報告書 第I巻 第III章"
SRC4 = "報告書 第I巻 第IV章"
SRC4F = "報告書 第I巻 第IV章 Findings"
PREF = "報告書 第I巻 序文・委員名簿"

SPEC = {

    "c901": dict(
        t="海底から、確かめていった",
        s="回収にあたった艦船　1986年",
        photo=P("recovery_ship"), **ss.kind(P("recovery_ship")),
        bias=0.45,
    ),

    "c902": dict(
        t="建物の中に、並べていく",
        s="回収されたかけら　1986年",
        photo=P("debris_hangar"), **ss.kind(P("debris_hangar")),
        bias=0.5,
    ),

    "c903": dict(
        t="下の継ぎ目が、見つかった",
        s="回収された右の補助ロケット　1986年",
        photo=P("srb_burn_hole"), **ss.kind(P("srb_burn_hole")),
        bias=0.45,
    ),

    "c904": dict(
        t="煙が出たのと、同じあたり",
        s="引き上げられた左の補助ロケット　1986年",
        photo=P("srb_burn_hole_2"), **ss.kind(P("srb_burn_hole_2")),
        bias=0.45,
    ),

    # ⚠️ c705 と同じ1枚。こちらは寄り
    "c905": dict(
        t="外からも、焼き抜けていた",
        s="継ぎ目に残った焼け跡　1986年",
        photo=P("srb_inside"), **ss.kind(P("srb_inside")),
        bias=0.40, xbias=0.62, zoom=1.30,
    ),

    "c906": dict(
        t="右だけが、焼けていた",
        s="回収された尾翼の部品　1986年",
        photo=P("rudder_burn"), **ss.kind(P("rudder_burn")),
        bias=0.45,
    ),

    "c907": dict(
        t="二本で、残り方が違った",
        s="回収された先端部　1986年",
        photo=P("frustum_compare"), **ss.kind(P("frustum_compare")),
        bias=0.45,
    ),

    # 🔴 決め所⑰
    "c908": dict(
        t="人の手かどうかも、調べた",
        s="非公開の会合で確かめられたこと",
        fig=("quote", dict(
            phrase="妨害された跡は、どこにもなかった",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=f"{SRC4F} 2")),
    ),

    "c909": dict(
        t="どれも、原因ではなかった",
        s="回収された燃料タンクのかけら　1986年",
        photo=P("debris_et"), **ss.kind(P("debris_et")),
        bias=0.45,
    ),

    "c910": dict(
        t="三基とも、燃料切れで止まった",
        s="引き上げられた主エンジン　1986年",
        photo=P("ssme_salvage"), **ss.kind(P("ssme_salvage")),
        bias=0.45,
    ),

    "c911": dict(
        t="委員長の名で、呼ばれている",
        s="委員会の席　記録映像より",
        **ss.still("commission_hearing", "commission", 2),
    ),

    "c912": dict(
        t="月を歩いた人も、加わった",
        s="壇上に並ぶ委員　記録映像より",
        **ss.still("commission_members", "commission", 14),
    ),

    # 🔴 第I巻の外。画面に出るのは写真の出典
    "c913": dict(
        t="三日後、家族と会った",
        s="追悼式　ヒューストン・1986年1月31日",
        photo=P("memorial_service"), **ss.kind(P("memorial_service")),
        bias=0.45,
    ),

    "c914": dict(
        t="生中継が、記憶を残した",
        s="国民への演説　1986年1月28日",
        photo=P("reagan_address"), **ss.kind(P("reagan_address")),
        bias=0.38,
    ),

    # ⚠️ 写っているのは半旗。乗員ではない
    "c915": dict(
        t="書かれたのは、それだけだった",
        s="半旗の掲揚　ヒューストン",
        photo=P("flag_half_mast"), **ss.kind(P("flag_half_mast")),
    ),

    "c916": dict(
        # ⚠️ 「この動画」は楽屋の言葉＝画面に出さない（`check_wording` B型）
        t="無いものは、足さない",
        s="報告書に書かれていないこと",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="亡くなった時刻", d="第1巻に出てこない", ok=False,
                        c=J.LINE),
                   dict(t="そのときの機内の様子", d="第1巻に出てこない", ok=False,
                        c=J.LINE)],
            lead="調べた範囲の外にあるもの",
            note=f"{SRC3}・{SRC4}")),
    ),

}
