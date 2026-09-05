# -*- coding: utf-8 -*-
"""第1章 開かなくなった門 c101–c131（31カット）。

■ この章の役目
  **追うのは、駐車場とプールデッキのあいだにある門ひとつ。ここでは原因の話をしない。**
  門の3段の絵（p50・p52）が物証。決め所は c112「門が開かなくなった」と c126「修理のあと、約1インチ沈んだ」。

■ 出どころ
  技術的知見 p3・p29・p48・p50・p52・p62（すべて Source: NIST の部分だけ。
  p50・p52 の右上の写真は ©2021 なので切り落としたファイルを使う）。
  ⚠️ 南北：プールデッキは塔の**南**（p3）。3週間前の門は「プールデッキと街路側駐車場のあいだ」。
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── c101 建物の形（3Dモデル・寸法）─────────────────────────
    "c101": dict(
        t="12階建て、高さは33.8メートル",
        s="NIST の3Dモデルに書き込まれた寸法（p3）",
        photo=ss.P003, side="right", ann_y=330, color=0.35,
        **ss.focus(ss.P003, 0.45, 0.42, 1.25),
        ann=[dict(t="高さ", v="33.8 m", d="12 stories　110'-10\"", vc=J.AMBER, vs=110,
                  dc=J.LINE, ds=28)],
    ),

    # ── c102 平面の寸法・竣工年 ─────────────────────────────
    "c102": dict(
        t="L字の平面、竣工は1981年",
        s="辺の長さ（p3）と、崩落までの年数",
        photo=ss.P003, side="left", ann_y=320, color=0.35,
        **ss.focus(ss.P003, 0.62, 0.30, 1.35),
        ann=[dict(t="辺の長さ", v="45.7 m", d="150'-0\"", vc=J.AMBER, vs=92, dc=J.LINE, ds=26),
             dict(t="", v="61.0 m", d="200'-0\"", vc=J.AMBER, vs=92, dc=J.LINE, ds=26),
             dict(t="竣工から崩落まで", v="40年", vc=J.INK_W, vs=80)],
    ),

    # ── c103 建物そのものではなく南側の床 ───────────────────────
    "c103": dict(
        t="覚えておくのは、南側の平らな床",
        s="プールデッキと街路側駐車場の位置（p3）",
        photo=ss.P003, side="right", ann_y=340, color=0.35,
        **ss.focus(ss.P003, 0.48, 0.74, 1.5),
        ann=[dict(t="Pool Deck", d="建物の南側に広がる床", dc=J.ALERT, ds=32),
             dict(t="Street-level Parking", d="街路側の駐車場（同じ高さ）", dc=J.LINE, ds=30)],
    ),

    # ── c104 プールデッキの張り出し ──────────────────────────
    "c104": dict(
        t="地面に載っていた床ではない",
        s="プールと、その周りのタイル張りの面（p3）",
        photo=ss.P003, side="left", ann_y=340, color=0.35,
        **ss.focus(ss.P003, 0.46, 0.80, 1.7),
        ann=[dict(t="Pool／Hot Tub", d="タイル張りの床の上", dc=J.LINE, ds=32),
             dict(t="その下", v="駐車場", vc=J.ALERT, vs=88)],
    ),

    # ── c105 断面の模式（自作。NIST の数値は書かない）───────────────
    "c105": dict(
        t="板一枚をはさんで、下は車",
        s="プールデッキと地下駐車場の断面（模式）",
        fig=("punch", dict(
            stage=1, lead="プールサイドの足の下（模式図・寸法は書いていない）",
            note="板＝鉄筋コンクリートのスラブ。柱が下から支える。上は人と土と舗装、下は車")),
    ),

    # ── c106 海沿いではふつうのつくり（空撮）────────────────────
    "c106": dict(
        t="駐車場の屋根を庭に使う",
        s="サーフサイドの海岸線（NIST 空撮）",
        photo=ss.fb("c106"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="土地の狭い海沿い", d="駐車場の上を屋外の床にする", dc=J.LINE, ds=32),
             dict(t="めずらしくない", d="このつくり自体は一般的", dc=J.INK_W, ds=32)],
    ),

    # ── c107 3つのつながり ───────────────────────────────
    "c107": dict(
        t="床・駐車場・建物本体の3つ",
        s="NIST の3D　方角と各部の名前（p29）",
        photo=ss.P029, side="left", ann_y=330, color=0.35,
        **ss.focus(ss.P029, 0.55, 0.55, 1.2),
        ann=[dict(t="1", d="平らな床（プールデッキ）", dc=J.ALERT, ds=32),
             dict(t="2", d="その下の駐車場", dc=J.AMBER, ds=32),
             dict(t="3", d="住んでいた建物本体（塔）", dc=J.INK_W, ds=32)],
    ),

    # ── c108 2021年5月の終わり ───────────────────────────
    "c108": dict(
        t="まだ何も起きていない",
        s="2021年5月末　崩落の約1か月前（p50）",
        fig=("timeline", dict(
            t0=-31, t1=0, title="単位は日。崩落（6月24日）を 0 とする",
            ticks=[(-31, "5月24日"), (-21, "6月3日"), (-7, "6月17日"), (0, "6月24日")],
            events=[dict(t=-30, top="1か月前", t2="門は正常", c=J.OK, big=True),
                    dict(t=0, top="崩落", c=J.INK_W)])),
    ),

    # ── c109 門の場所と、描き起こし ─────────────────────────
    "c109": dict(
        t="門は、目撃談から描き起こされた",
        s="3週間前の3D　門の位置（p50）",
        photo=ss.P050_3D, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P050_3D, 0.50, 0.62, 1.3),
        ann=[dict(t="門", d="プールデッキ ⇄ 街路側駐車場", dc=J.ALERT, ds=32),
             dict(t="描いたのは", d="NIST（artist rendering）", dc=J.LINE, ds=30)],
    ),

    # ── c110 1か月前の札（正常）────────────────────────────
    "c110": dict(
        t="1か月前は、正常だった",
        s="門の描き起こし　1段目（p50）",
        photo=ss.P050_GATE, side="right", ann_y=330, color=0.5,
        **ss.focus(ss.P050_GATE, 0.45, 0.30, 1.6),
        ann=[dict(t="1 MONTH BEFORE COLLAPSE", d="見た目・位置合わせとも正常", dc=J.OK, ds=30)],
    ),

    # ── c111 3週間前 ───────────────────────────────────
    "c111": dict(
        t="次の段は、6月のはじめ",
        s="崩落の3週間前（p50）",
        fig=("timeline", dict(
            t0=-31, t1=0, title="単位は日。崩落（6月24日）を 0 とする",
            ticks=[(-31, "5月24日"), (-21, "6月3日"), (-7, "6月17日"), (0, "6月24日")],
            events=[dict(t=-30, top="1か月前", t2="正常", c=J.OK, up=True),
                    dict(t=-21, top="3週間前", t2="同じ門が…", c=J.ALERT, big=True, up=True),
                    dict(t=0, top="崩落", c=J.INK_W, up=False)])),
    ),

    # ── c112 ★決め所「門が開かなくなった」──────────────────────
    "c112": dict(
        t="1.2センチで、扉は動かなくなる",
        s="3週間前の門　NIST の札（p50）",
        fig=("quote", dict(
            phrase="門が開かなくなった",
            rows=[("誰が", "NIST（目撃証言の描き起こし）", J.INST),
                  ("いつ", "崩落の3週間前（2021年6月初め）", J.LINE),
                  ("どこに", "技術的知見 スライド50", J.DOC)],
            ctx="原文 Less than 1/2\" vertical shift. Gate door is stuck and cannot be opened.",
            paper=True)),
    ),

    # ── c113 扉の隙間は数ミリ ────────────────────────────
    "c113": dict(
        t="支えが1センチ下がれば動かない",
        s="門の2段目　下向きの矢印（p50）",
        photo=ss.P050_GATE, side="left", ann_y=330, color=0.5,
        **ss.focus(ss.P050_GATE, 0.55, 0.72, 1.6),
        ann=[dict(t="扉と枠の隙間", v="数 mm", vc=J.LINE, vs=84),
             dict(t="支えが下がった量", v="約1.2 cm", vc=J.ALERT, vs=84)],
    ),

    # ── c114 1.2センチは人が気づく量ではない ──────────────────
    # 🔴 `vmax` を渡す（10メートルが2本とも満杯になった c611 の事故）。基準は「人の目で分かる段差」ではなく
    #    扉の隙間（数ミリ）＝ここでは 5mm を ref にして、1.2cm がその2倍強であることだけを見せる。
    "c114": dict(
        t="気づいたのは、人でなく扉",
        s="1.2センチという量",
        fig=("compare", dict(
            items=[dict(v=12, t="門の沈み（3週間前）", disp="1.2", unit="cm",
                        sub="2分の1インチ未満", c=J.ALERT),
                   dict(v=4, t="扉と枠の隙間", disp="数", unit="mm", sub="扉は数ミリで作られる",
                        c=J.LINE)],
            vmax=30, ref="人が床の段差として気づく量（目安）",
            note="※ 沈み 1.2cm は NIST の札（p50）。隙間は扉の一般的な作り")),
    ),

    # ── c115 3週間前に見えていたもう1つ ───────────────────────
    "c115": dict(
        t="プランターの傷みも見つかっていた",
        s="NIST のまとめ　3週間前の吹き出し（p62）",
        photo=ss.P062, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P062, 0.70, 0.25, 1.5),
        ann=[dict(t="~3 weeks before collapse", d="プランターの損傷", dc=J.ALERT, ds=30),
             dict(t="", d="門の損傷", dc=J.ALERT, ds=30)],
    ),

    # ── c116 K-13.1 ───────────────────────────────────
    "c116": dict(
        t="柱の記号は、K と 13.1",
        s="プールデッキの柱の記号（p48）",
        photo=ss.P048, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P048, 0.62, 0.62, 1.5),
        ann=[dict(t="Grid Point", v="K-13.1", d="プランターの近くの柱", vc=J.ALERT, vs=100,
                  dc=J.LINE, ds=30),
             dict(t="", d="第3章で、もう一度", dc=J.TICK, ds=28)],
    ),

    # ── c117 3週間前の2点 ─────────────────────────────
    "c117": dict(
        t="3週間前の時点で、2つ",
        s="NIST のまとめ（p62）",
        photo=ss.P062, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P062, 0.55, 0.45, 1.2),
        ann=[dict(t="1", d="ひび割れたプランター（K-13.1 付近）", dc=J.ALERT, ds=32),
             dict(t="2", d="開かなくなった門", dc=J.ALERT, ds=32)],
    ),

    # ── c118 受け取られ方 ────────────────────────────
    "c118": dict(
        t="壊れかけの印には見えない",
        s="このときの受け取られ方",
        fig=("panel", dict(
            lead="見えていたもの／見えたもの",
            blocks=[dict(k="門", t="開かない → 業者を呼んで直す", c=J.LINE),
                    dict(k="植木鉢", t="ひび → 傷んだ設備の1つ", c=J.LINE)],
            cols=2, note="どちらも「建物が沈んでいる」とは読まれなかった")),
    ),

    # ── c119 実際、そう受け取られた（門は直された）────────────────
    "c119": dict(
        t="門は、直された",
        s="プールデッキの床面（NIST ドローン）",
        photo=ss.fb("c119"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="修理", d="門は業者が直した", dc=J.LINE, ds=32),
             dict(t="記録", d="直したあとの様子も NIST が残している", dc=J.DOC, ds=30)],
    ),

    # ── c120 1週間前 ───────────────────────────────
    "c120": dict(
        t="直した門を、もう一度見る",
        s="崩落の1週間前　6月17日ごろ（p52）",
        fig=("timeline", dict(
            t0=-31, t1=0, title="単位は日。崩落（6月24日）を 0 とする",
            ticks=[(-31, "5月24日"), (-21, "6月3日"), (-7, "6月17日"), (0, "6月24日")],
            events=[dict(t=-30, top="1か月前", t2="正常", c=J.OK),
                    dict(t=-21, top="3週間前", t2="開かない → 修理", c=J.ALERT),
                    dict(t=-7, top="1週間前", t2="直した門を再び", c=J.ALERT, big=True),
                    dict(t=0, top="崩落", c=J.INK_W)])),
    ),

    # ── c121 3段目 ───────────────────────────────
    "c121": dict(
        t="描き起こしには、3段目がある",
        s="門の描き起こし　1週間前（p52）",
        photo=ss.P052_GATE, side="left", ann_y=330, color=0.5,
        **ss.focus(ss.P052_GATE, 0.55, 0.78, 1.5),
        ann=[dict(t="1 WEEK BEFORE COLLAPSE", d="矢印が、また下を向く", dc=J.ALERT, ds=30)],
    ),

    # ── c122 1.2 → 2.5 ────────────────────────────
    "c122": dict(
        t="1.2センチが、2.5センチに",
        s="沈んだ量の変化（p50 → p52）",
        fig=("compare", dict(
            items=[dict(v=12, t="3週間前", disp="1.2", unit="cm", sub="½インチ足らず", c=J.AMBER),
                   dict(v=25, t="1週間前", disp="2.5", unit="cm", sub="約1インチ", c=J.ALERT)],
            note="※ どちらも NIST の札の値（p50・p52）")),
    ),

    # ── c123 2週間で倍・直したあとの数字 ────────────────────
    "c123": dict(
        t="直したあとに測って、2.5センチ",
        s="門の描き起こし　3段目の矢印（p52）",
        photo=ss.P052_GATE, side="right", ann_y=330, color=0.5,
        **ss.focus(ss.P052_GATE, 0.45, 0.78, 1.5),
        ann=[dict(t="2週間で", v="2倍", vc=J.ALERT, vs=110),
             dict(t="", d="修理後に測られた値", dc=J.LINE, ds=32)],
    ),

    # ── c124 門ではなく床 ───────────────────────────
    "c124": dict(
        t="下がり続けていたのは、床",
        s="何が起きていたか",
        fig=("panel", dict(
            lead="ずれていたもの",
            blocks=[dict(k="×", t="門そのもの", c=J.LINE_DIM),
                    dict(k="○", t="門を載せている床（プールデッキ）", c=J.ALERT)],
            cols=2, note="直しても、床が下がれば同じことが起きる")),
    ),

    # ── c125 直す速さより下がる速さ ─────────────────────
    "c125": dict(
        t="直す速さより、沈む速さが速い",
        s="門の描き起こし　寄り（p52）",
        photo=ss.P052_GATE, side="left", ann_y=330, color=0.5,
        **ss.focus(ss.P052_GATE, 0.40, 0.55, 2.0),
        ann=[dict(t="直す", d="いったんは戻る", dc=J.OK, ds=32),
             dict(t="また下がる", d="戻ったあと、さらに沈む", dc=J.ALERT, ds=32)],
    ),

    # ── c126 ★決め所「修理のあと、約1インチ沈んだ」──────────────
    "c126": dict(
        t="NIST が3段目に書き添えた言葉",
        s="1週間前の門　NIST の札（p52）",
        fig=("quote", dict(
            phrase="修理のあと、約1インチ沈んだ",
            rows=[("誰が", "NIST（目撃証言の描き起こし）", J.INST),
                  ("いつ", "崩落の1週間前（2021年6月17日ごろ）", J.LINE),
                  ("どこに", "技術的知見 スライド52", J.DOC)],
            ctx="原文 Approx. 1\" vertical shift after repairs.",
            paper=True)),
    ),

    # ── c127 1週間前・駐車場のなか ─────────────────────
    "c127": dict(
        t="同じ週、駐車場のなかでも",
        s="NIST のまとめ　1週間前の吹き出し（p62）",
        photo=ss.P062, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P062, 0.85, 0.52, 1.5),
        ann=[dict(t="~1 week before collapse", d="門の損傷、ふたたび", dc=J.ALERT, ds=30),
             dict(t="", d="駐車場のなかで、あることが見られた", dc=J.LINE, ds=30)],
    ),

    # ── c128 見えていたのは水 ──────────────────────────
    "c128": dict(
        t="見えていたのは、水だった",
        s="現場の柱まわり（NIST 記録映像）",
        photo=ss.fb("c128"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="水", d="天井から滴る水ではない", dc=J.LINE, ds=32)],
    ),

    # ── c129 柱を伝う水（模式）─────────────────────────
    "c129": dict(
        t="水は柱に沿って、上から下へ",
        s="柱を伝って流れ落ちる水（模式）",
        fig=("process", dict(
            steps=[dict(t="天井と柱のつなぎ目", d="水が出てくる場所", c=J.ALERT),
                   dict(t="柱の面", d="沿って流れ落ちる", c=J.LINE),
                   dict(t="駐車場の床", d="水がたまる", c=J.LINE)],
            note="原文 Water funnels down column（p62）・模式図")),
    ),

    # ── c130 水が意味していたこと ────────────────────────
    "c130": dict(
        t="つなぎ目に、水の通る隙間",
        s="水が柱を伝うということ",
        fig=("panel", dict(
            lead="柱を伝う水が示すもの",
            blocks=[dict(k="上", t="天井（プールデッキの裏側）", c=J.LINE),
                    dict(k="間", t="つなぎ目の隙間（水の通り道）", c=J.ALERT),
                    dict(k="下", t="柱を伝って落ちる", c=J.LINE)],
            cols=3, note="推論。NIST は「柱を伝って水が流れ落ちた」とだけ書いている")),
    ),

    # ── c131 1週間前の要約（panel。見出しは立証したことを書く）──────
    "c131": dict(
        t="1週間前：水は柱を伝っていた",
        s="NIST のまとめ　1週間前（p62）",
        fig=("panel", dict(
            lead="~1 week before collapse（p62）",
            blocks=[dict(k="1", t="門に、ふたたび損傷", c=J.ALERT),
                    dict(k="2", t="駐車場の柱を、水が伝い落ちる", c=J.ALERT)],
            cols=2)),
    ),
}
