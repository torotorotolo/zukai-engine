# -*- coding: utf-8 -*-
"""第2章 4インチの隙間 c201–c232（32カット）。

■ この章の役目
  **追うのは、目撃者が紙に書いた言葉。時間の刻みがここから急に細かくなる。**
  手書きの目撃メモ（p57・p58）が物証。決め所は c214「床に、4インチの隙間」・c225「配管ではない。天井からの漏れ」。

■ 出どころ
  技術的知見 p57・p58（手書きメモと注記だけが Source: NIST。写真と原図は管財人＝切ってある）・
  p62・p65・p67・section 2。
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── c201 数え方が変わる ───────────────────────────
    "c201": dict(
        t="刻みが、ここで細かくなる",
        s="NIST の数え方　section 2",
        fig=("timeline", dict(
            t0=-21, t1=0, title="単位は日。崩落を 0 とする（NIST は「〜週間前」「〜時間前」と数える）",
            ticks=[(-21, "3週間前"), (-7, "1週間前"), (0, "崩落")],
            events=[dict(t=-21, top="3週間前", c=J.LINE, up=True),
                    dict(t=-7, top="1週間前", c=J.LINE, up=True),
                    dict(t=-0.7, top="17時間前", t2="ここから時間で数える", c=J.ALERT, big=True,
                         up=False)])),
    ),

    # ── c202 17時間前の3D ──────────────────────────
    "c202": dict(
        t="次の記録は、17時間前",
        s="2021年6月23日 朝　NIST の3D（p57）",
        photo=ss.P057_3D, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P057_3D, 0.50, 0.55, 1.2),
        ann=[dict(t="~17 hours before collapse", d="6月23日（水）の朝", dc=J.ALERT, ds=30),
             dict(t="崩落", d="6月24日（木）午前1時22分", dc=J.LINE, ds=30)],
    ),

    # ── c203 プールデッキの床の上 ──────────────────────
    "c203": dict(
        t="場所は、人が歩く床の上",
        s="プールデッキ上の位置（p57）",
        photo=ss.P057_3D, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P057_3D, 0.60, 0.68, 1.7),
        ann=[dict(t="プールデッキ", d="タイル張りの面", dc=J.LINE, ds=32),
             dict(t="17時間前", d="この面の上で", dc=J.ALERT, ds=32)],
    ),

    # ── c204 その朝、歩いた人 ─────────────────────────
    "c204": dict(
        t="足元に、無かったものがあった",
        s="デッキ面の引き（NIST 記録映像）",
        photo=ss.fb("c204"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="6月23日 朝", d="プールデッキを歩いた人がいた", dc=J.LINE, ds=32)],
    ),

    # ── c205 手書きメモの引き ─────────────────────────
    "c205": dict(
        t="残っているのは、手書きの図と文",
        s="聞き取りのときに描かれたメモ（p57）",
        photo=ss.P057_MEMO, side="right", ann_y=330, color=0.3,
        **ss.focus(ss.P057_MEMO, 0.42, 0.50, 1.0),
        ann=[dict(t="Source", d="NIST（目撃者への聞き取り）", dc=J.INST, ds=30),
             dict(t="縮尺", d="not to scale（縮尺なし）", dc=J.TICK, ds=28)],
    ),

    # ── c206 走り書きであること ────────────────────────
    "c206": dict(
        t="清書ではない。走り書きである",
        s="手書きであること（p57）",
        fig=("panel", dict(
            lead="この紙の性格",
            blocks=[dict(k="×", t="清書された報告書の文章", c=J.LINE_DIM),
                    dict(k="○", t="聞き取りの場で、その場で書かれた図と文", c=J.DOC)],
            cols=2, note="not to scale（縮尺なし）")),
    ),

    # ── c207 13.1 と K ───────────────────────────
    "c207": dict(
        t="書き込みは、13.1 と K の近く",
        s="メモの位置と柱の記号（p57）",
        photo=ss.P057_MEMO, side="left", ann_y=330, color=0.3,
        **ss.focus(ss.P057_MEMO, 0.55, 0.40, 1.4),
        ann=[dict(t="Grid Point", v="K-13.1", d="プランターのひびと同じ柱", vc=J.ALERT,
                  vs=96, dc=J.LINE, ds=28)],
    ),

    # ── c208 同じ一点が3週間動いていた ─────────────────────
    "c208": dict(
        t="同じ一点が、3週間動いていた",
        s="3週間前の位置と17時間前の位置（p62・p57）",
        fig=("compare", dict(
            items=[dict(v=21, t="3週間前", disp="K-13.1", unit="", sub="プランターのひび",
                        c=J.AMBER),
                   dict(v=0.7, t="17時間前", disp="K-13.1", unit="", sub="床の隙間",
                        c=J.ALERT)],
            bar=False, note="※ 同じ柱の記号。棒でなく記号で見せる（差は場所でなく時間）")),
    ),

    # ── c209 排水の記号（自作）─────────────────────────
    "c209": dict(
        t="図には、排水口の記号が2種類",
        s="メモの凡例（p57）",
        fig=("icons", dict(
            n=2, on=[0], kind="dot", cols=2,
            lead="メモの凡例にある2つの記号",
            labels=["Pool Deck Drains", "Planter Drains"],
            note="プールデッキの排水口／プランターの排水口（p57 の凡例）")),
    ),

    # ── c210 なぜ排水が描かれたか ────────────────────────
    "c210": dict(
        t="水は、話に出ていた",
        s="なぜ排水が図に描き込まれたか",
        fig=("panel", dict(
            lead="聞き取りの図に排水口が描かれる、ということ",
            blocks=[dict(k="問", t="水がどこへ抜けていくか", c=J.LINE),
                    dict(k="答", t="排水口を描くほど、水が話題に", c=J.ALERT)],
            cols=2, note="推論。図に排水の凡例があるのは事実（p57）")),
    ),

    # ── c211 メモの前段（日付）────────────────────────
    "c211": dict(
        t="手書きの文は、日付から始まる",
        s="メモの拡大　前段（p57）",
        photo=ss.P057_MEMO, side="left", ann_y=330, color=0.3,
        **ss.focus(ss.P057_MEMO, 0.50, 0.50, 2.2),
        ann=[dict(t="書き出し", v="Morning June 23", vc=J.INK_W, vs=64)],
    ),

    # ── c212 メモの中段 ────────────────────────────
    "c212": dict(
        t="床のあたりに、あるものがあった",
        s="メモの拡大　中段（p57）",
        photo=ss.P057_MEMO, side="right", ann_y=330, color=0.3,
        **ss.focus(ss.P057_MEMO, 0.52, 0.56, 2.2),
        ann=[dict(t="続き", d="noticed in the floor area", dc=J.INK_W, ds=34)],
    ),

    # ── c213 気づいたものが何か ────────────────────────
    "c213": dict(
        t="ひびでも、たわみでもない",
        s="気づいたものが何か（p57）",
        fig=("absent", dict(
            mode="ledger", lead="メモに書かれていないもの",
            items=[dict(t="ひび割れ", d="書かれていない", ok=False, c=J.LINE),
                   dict(t="汚れ", d="書かれていない", ok=False, c=J.LINE),
                   dict(t="たわみ", d="書かれていない", ok=False, c=J.LINE),
                   dict(t="水たまり", d="書かれていない", ok=False, c=J.LINE)],
            note="書かれていたものは、次のカットで")),
    ),

    # ── c214 ★決め所「床に、4インチの隙間」──────────────────
    "c214": dict(
        t="幅まで、書き込まれている",
        s="目撃者の手書き（p57）",
        fig=("quote", dict(
            phrase="床に、4インチの隙間",
            rows=[("誰が", "目撃者（NIST の聞き取り）", J.INK_W),
                  ("いつ", "2021年6月23日 朝（崩落の約17時間前）", J.LINE),
                  ("どこに", "手書きの図と文　技術的知見 スライド57", J.DOC)],
            ctx="原文 Morning June 23 noticed in the floor area, a space or gap of 4 inches",
            paper=True)),
    ),

    # ── c215 4インチ＝約10センチ ────────────────────────
    "c215": dict(
        t="手のひらを縦に差し込める幅",
        s="4インチという長さ",
        fig=("compare", dict(
            items=[dict(v=10.2, t="床の隙間", disp="約10", unit="cm", sub="4インチ", c=J.ALERT),
                   dict(v=1.2, t="3週間前の門の沈み", disp="1.2", unit="cm", sub="½インチ未満",
                        c=J.AMBER)],
            note="※ 隙間 4インチ＝メモの値（p57）。門の沈みは p50")),
    ),

    # ── c216 10センチの意味 ────────────────────────
    "c216": dict(
        t="割れたのではない。離れていた",
        s="p57 のメモの言葉から",
        fig=("beforeafter", dict(
            a=dict(k="割れ", t="床が割れる", lines=["面は続いている"], c=J.LINE),
            b=dict(k="隙間", t="床が離れる", lines=["10センチぶん、面が離れる"], c=J.ALERT),
            note="推論。メモの語は space or gap（隙間）")),
    ),

    # ── c217 まだ17時間ある ────────────────────────
    "c217": dict(
        t="まる一日近くが、残っていた",
        s="現場の床面（NIST 記録映像）",
        photo=ss.fb("c217"), bias=0.5, side="right", ann_y=340,
        ann=[dict(t="残っていた時間", v="約17時間", vc=J.AMBER, vs=96)],
    ),

    # ── c218 9時間前 ─────────────────────────────
    "c218": dict(
        t="記録は、夕方から夜にも残る",
        s="6月23日 夕方から夜（section 2）",
        fig=("timeline", dict(
            t0=-20, t1=0, title="単位は時間。崩落（6月24日 01:22）を 0 とする",
            ticks=[(-17, "17時間前"), (-9, "9時間前"), (-3, "3時間前"), (0, "崩落")],
            events=[dict(t=-17, top="朝", t2="床の隙間", c=J.AMBER),
                    dict(t=-9, top="夕方〜夜", t2="9時間前", c=J.ALERT, big=True)])),
    ),

    # ── c219 場所が変わる・駐車場 ────────────────────────
    "c219": dict(
        t="今度は、床の下の駐車場",
        s="9時間前の3D（p58）",
        photo=ss.P058_3D, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P058_3D, 0.48, 0.60, 1.3),
        ann=[dict(t="~9 hours before collapse", d="プールデッキの下、車の停まる空間", dc=J.ALERT,
                  ds=30)],
    ),

    # ── c220 駐車場の区画図 ────────────────────────
    # ⚠️ 原図は管財人（CTS Receiver）。**付箋の周りだけ**を切ったファイル（p58）。
    "c220": dict(
        t="区画には、番号がふられている",
        s="駐車場の区画図に足された付箋（p58）",
        photo=ss.P058_NOTE, side="right", ann_y=330, color=0.3,
        **ss.focus(ss.P058_NOTE, 0.35, 0.55, 1.0),
        ann=[dict(t="区画番号", d="048 046 045 044 …", dc=J.LINE, ds=32),
             dict(t="原図", d="管財人の図面に NIST が注記", dc=J.TICK, ds=28)],
    ),

    # ── c221 付箋 ───────────────────────────────
    "c221": dict(
        t="付箋も、聞き取りで足された",
        s="付箋の位置（p58）",
        photo=ss.P058_NOTE, side="left", ann_y=330, color=0.3,
        **ss.focus(ss.P058_NOTE, 0.62, 0.45, 1.6),
        ann=[dict(t="Annotations", d="from an eyewitness interview", dc=J.INST, ds=30)],
    ),

    # ── c222 天井から水 ────────────────────────────
    "c222": dict(
        t="書かれているのは、天井の漏れ",
        s="駐車場での目撃（p58）",
        fig=("panel", dict(
            lead="付箋に書かれていること",
            blocks=[dict(k="1", t="天井から水が漏れていた", c=J.LINE),
                    dict(k="2", t="それだけでは、印にならない", c=J.TICK)],
            cols=2, note="次の1行が、この付箋の値打ち")),
    ),

    # ── c223 駐車場の水漏れはよくある ───────────────────────
    "c223": dict(
        t="地下駐車場の水漏れは、よくある",
        s="駐車場側の瓦礫（NIST 記録映像）",
        photo=ss.fb("c223"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="上にプール", d="配管も通っている", dc=J.LINE, ds=32),
             dict(t="水漏れ", d="それだけでは印にならない", dc=J.TICK, ds=30)],
    ),

    # ── c224 否定を書き足している ──────────────────────
    "c224": dict(
        t="わざわざ、否定を書き足した",
        s="書き手が否定したこと（p58）",
        fig=("absent", dict(
            mode="pair", lead="漏れの出どころ",
            items=[dict(t="配管", d="not the pipe", ok=False, c=J.LINE),
                   dict(t="天井（床の裏側）", d="from the ceiling", ok=True, c=J.ALERT)])),
    ),

    # ── c225 ★決め所「配管ではない。天井からの漏れ」──────────────
    "c225": dict(
        t="割れの深さまで、書いてある",
        s="付箋（p58）",
        fig=("quote", dict(
            phrase="配管ではない。天井からの漏れ",
            rows=[("誰が", "目撃者（NIST の聞き取り）", J.INK_W),
                  ("いつ", "2021年6月23日 夜（崩落の約9時間前）", J.LINE),
                  ("どこに", "駐車場の区画図の付箋　技術的知見 スライド58", J.DOC)],
            ctx="原文 Leak from the ceiling, not the pipe - 1/4 inch deep crack",
            paper=True)),
    ),

    # ── c226 4分の1インチ＝約6ミリ ──────────────────────
    "c226": dict(
        t="天井に、6ミリの深さの割れ",
        s="4分の1インチという深さ",
        fig=("compare", dict(
            items=[dict(v=6.4, t="天井の割れの深さ", disp="約6", unit="mm", sub="¼インチ", c=J.ALERT),
                   dict(v=102, t="床の隙間の幅（17時間前）", disp="約100", unit="mm", sub="4インチ",
                        c=J.AMBER)],
            note="※ 天井＝プールデッキの裏側。どちらも目撃メモの値（p57・p58）")),
    ),

    # ── c227 3時間前 ─────────────────────────────
    "c227": dict(
        t="3時間前、日付が変わる前",
        s="6月23日 22時すぎ（section 2）",
        fig=("timeline", dict(
            t0=-20, t1=0, title="単位は時間。崩落（6月24日 01:22）を 0 とする",
            ticks=[(-17, "17時間前"), (-9, "9時間前"), (-3, "3時間前"), (0, "崩落")],
            events=[dict(t=-17, top="朝", t2="床の隙間", c=J.AMBER),
                    dict(t=-9, top="夜", t2="天井の漏れ", c=J.AMBER),
                    dict(t=-3, top="22:22ごろ", t2="記録あり", c=J.ALERT, big=True)])),
    ),

    # ── c228 分の単位 ─────────────────────────────
    "c228": dict(
        t="刻みは、分の単位になる",
        s="崩落前の数分（section 2）",
        fig=("timeline", dict(
            t0=-10, t1=0, title="単位は分。崩落（01:22）を 0 とする",
            ticks=[(-9, "9分前"), (-6, "6分前"), (-3, "3分前"), (0, "崩落")],
            events=[dict(t=-9, top="9分前", c=J.AMBER, up=True),
                    dict(t=-6.5, top="6〜7分前", c=J.AMBER, up=False),
                    dict(t=-5.5, top="5〜6分前", c=J.ALERT, up=True),
                    dict(t=-4.5, top="4〜5分前", c=J.ALERT, up=False),
                    dict(t=0, top="01:22", t2="崩落", c=J.INK_W, big=True)])),
    ),

    # ── c229 9分前の駐車場3D ───────────────────────
    "c229": dict(
        t="9分前の駐車場は、模型にある",
        s="車と柱の3D（p65）",
        photo=ss.P065, side="left", ann_y=330, color=0.45,
        **ss.focus(ss.P065, 0.55, 0.45, 1.15),
        ann=[dict(t="~9 min before collapse", d="車が並び、柱が立つ", dc=J.LINE, ds=30),
             dict(t="柱の記号", d="K・L ／ 9.1・11.1・13.1", dc=J.AMBER, ds=30)],
    ),

    # ── c230 6〜7分前・たわみの色分け ────────────────────
    "c230": dict(
        t="床のたわみが、色で分けられる",
        s="6〜7分前の3D（p67）",
        photo=ss.P067, side="right", ann_y=330, color=0.5,
        **ss.focus(ss.P067, 0.42, 0.55, 1.25),
        ann=[dict(t="a / b / c", d="たわみの深さで3段階", dc=J.AMBER, ds=32),
             dict(t="~6-7 min before collapse", d="", dc=J.LINE, ds=28)],
    ),

    # ── c231 断面の凹み ────────────────────────────
    "c231": dict(
        t="沈みは、北側で深い",
        s="たわみの断面（p67 左下）",
        photo=ss.P067, side="right", ann_y=330, color=0.5,
        **ss.focus(ss.P067, 0.20, 0.86, 2.4),
        ann=[dict(t="浅い皿の形", d="北側（建物側）ほど深い", dc=J.ALERT, ds=32)],
    ),

    # ── c232 残っていないもの（出さない映像）──────────────────
    "c232": dict(
        t="その映像は、ここでは出さない",
        s="崩落の瞬間の映像（p119）について",
        fig=("absent", dict(
            mode="single", lead="このあとの数分",
            items=[dict(t="崩落の瞬間の映像", d="この動画では出さない", ok=False, c=J.LINE)],
            note="権利（©2021）と描写の線引きの両方で出さない")),
    ),
}
