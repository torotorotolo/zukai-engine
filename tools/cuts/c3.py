# -*- coding: utf-8 -*-
"""第3章 見込みは、なぜ外れたのか c301–c324（24カット）。12本目（キャッスル・ブラボー）。⑤b-3（2026-09-23）で書いた。

■ 実写 8/24（写真6・報告書の頁1・4K 映像1）。章の色＝紺。爆発の実写は原色（`color=1.0`）。
■ 🔴 台本 §4 の画から変えたところ（⑤b-3 で決めた・根拠つき）
  c308・c310 … 記録映画（Commander's Report）→ 図。取得した 900〜1000秒（カズヤくん許可）の中身は
                夜の火球／司令官が話す場面（§5b-27）／B-29 型の機体／**はしけへ積む別の回の装置**／きのこ雲／輪の雲の火球で、
                **ブラボーの装置と確かめられる絵が無かった**（シート2枚で実見）。c308 は決め所なので quote、c310 は目盛りの図
  c309       … トラックの装置（c219 へ）→ **射点の小屋の外観**（「あの小さな建物の中で」）
  c315       … 別の回の火球＝色あせたヤンキー（明るさ 25〜125）を**濃淡補正**（levels）して出す（出典の行に「濃淡補正」）
■ 目盛りの図が戻る：c310（予想の幅）→ c311（いちばんありそうな値・実際）→ c320（備える上限）＝同じ 0〜1650万トンの目盛り
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
SRC_DNA = ss.SRC_DNA
NOTE_WEB = "出典：ロスアラモス研究所の説明（1954年）ほか　目盛り＝万トン"
# ⚠️ 目盛りは素の数字（単位は注）。「1500万トン」と書くと旗の札と同語になる（check_dup・c311）
MT = dict(t0=0, t1=1650, ticks=[(0, "0"), (500, "500"), (1000, "1000"), (1500, "1500")])
BAND = dict(a=400, b=800, t="予想の幅", c=J.AMBER)

SPEC = {

    "c301": dict(
        t="マイクの弱点",
        s="燃料の扱い",
        fig=("process", dict(
            steps=[dict(t="液体の燃料", d="重い水素", c=J.LINE),
                   dict(t="冷やし続ける", d="とても低い温度で", c=J.ALERT)])),
    ),

    "c302": dict(
        t="燃料を、固体に",
        s="ロスアラモスが選んだ燃料",
        fig=("process", dict(
            steps=[dict(t="重い水素", d="水素のなかま", c=J.LINE),
                   dict(t="リチウム", d="軽い金属", c=J.LINE),
                   dict(t="重水素化リチウム", d="白い固体", c=J.AMBER)])),
    ),

    # 対比（矢印なし）
    "c303": dict(
        t="冷やさずにすむ",
        s="液体の燃料と、固体の燃料",
        fig=("beforeafter", dict(
            a=dict(k="マイク", t="液体", lines=["冷やす設備が要る"], v="", c=J.LINE),
            b=dict(k="ブラボー", t="固体＝乾式", lines=["冷やす設備は要らない"], v="", c=J.OK),
            arrow=False)),
    ),

    # ⚠️ 天然の割合（7.5%・92.5%）は台本に無い数＝図に書かない（「わずか」「ほとんど」のまま）
    "c304": dict(
        t="2種類のリチウム",
        s="天然のリチウムの中身",
        fig=("panel", dict(
            blocks=[dict(k="リチウム6", t="天然にはわずか", c=J.AMBER),
                    dict(k="リチウム7", t="天然のほとんど", c=J.LINE)],
            cols=2)),
    ),

    "c305": dict(
        t="燃料を生む仕組み",
        s="爆弾の中でできる燃料",
        fig=("process", dict(
            steps=[dict(t="リチウム6", d="軽い金属", c=J.LINE),
                   dict(t="中性子", d="粒が当たる", c=J.AMBER),
                   dict(t="三重水素", d="燃料になる", c=J.OK)])),
    ),

    # 対比（矢印なし）。⚠️ 副題と同じ語を札に置かない（check_dup）
    "c306": dict(
        t="数の多いほうは",
        s="実験の前の見方",
        fig=("beforeafter", dict(
            a=dict(k="よい燃料", t="リチウム6", lines=["液体の重い水素も"], v="", c=J.OK),
            b=dict(k="ずっと劣る", t="リチウム7", lines=["数は多い"], v="", c=J.ALERT),
            arrow=False)),
    ),

    # Commons「Castle Bravo Shrimp Device 002.jpg」＝"The Shrimp device in its shot cab."
    "c307": dict(
        t="装置の名は、シュリンプ",
        s="射点の小屋の中の装置　1954年",
        photo=P("dev_shrimp"), **ss.kind(P("dev_shrimp")),
        side="right", ann_y=356,
        ann=[dict(t="燃料", d="重水素化リチウム", dc=J.TICK),
             dict(t="英語の意味", v="エビ", vc=J.AMBER)],
    ),

    # 🔴 決め所（DNA p31「…a device more powerful than MIKE was exploded that, although not a weapon,
    #    was capable of delivery by an aircraft」）。⚠️ 留保「兵器そのものではない」は札に残す（§5b-27b）
    "c308": dict(
        t="運べる水爆への一歩",
        s="ブラボーの装置についての一文",
        fig=("quote", dict(
            phrase="マイクより強力で、飛行機で運べる装置",
            who="国防原子力局",
            when="1982年",
            doc="キャッスル作戦の報告書",
            # ⚠️ ctx を字幕と同文にしない（check_echo）。12字未満で留保だけ残す
            ctx="兵器ではない、と前置き")),
    ),

    # Commons「BravoShotCab.jpg」＝"Operation Castle Bravo SHRIMP shot-cab"
    "c309": dict(
        t="落とさず、地上で",
        s="射点の小屋の外観　1954年",
        photo=P("dev_shotcab"), **ss.kind(P("dev_shotcab")),
        cam="pan_l",
        side="right", ann_y=380,
        ann=[dict(t="爆発させた場所", d="地上の小屋の中", dc=J.AMBER)],
    ),

    # 目盛りの図①（予想の幅）
    "c310": dict(
        t="撃つ前の見積もり",
        s="研究所の予想　TNT火薬に直した値",
        fig=("timeline", dict(
            events=[dict(t=400, top="400万トン", t2="予想の下", c=J.TICK),
                    dict(t=800, top="800万トン", t2="予想の上", c=J.TICK)],
            band=[BAND], src=NOTE_WEB, **MT)),
    ),

    # 目盛りの図②（同じ目盛りに、いちばんありそうな値と実際）
    # ⚠️ 帯の札「予想の幅」は帯の真ん中＝600万トンの旗と重なる（check_layout 120×14px）＝札は c310 で出したので外す
    "c311": dict(
        t="実際は、はるか上",
        s="予想と実際を同じ目盛りで",
        fig=("timeline", dict(
            events=[dict(t=600, top="600万トン", t2="いちばんありそう", c=J.TICK),
                    dict(t=1500, top="1500万トン", t2="実際", c=J.ALERT, big=True)],
            band=[dict(BAND, t="")], src=NOTE_WEB, **MT)),
    ),

    # 棒の長さは値に比例（vmax＝実際の値）
    "c312": dict(
        t="見込みの2.5倍",
        s="3つの値をくらべる",
        fig=("compare", dict(
            items=[dict(v=600, t="いちばんありそうな値", disp="600万", unit="トン", c=J.TICK),
                   dict(v=800, t="予想の幅の上", disp="800万", unit="トン", c=J.LINE),
                   dict(v=1500, t="実際", disp="1500万", unit="トン", c=J.ALERT)],
            vmax=1500, ratio="2.5倍／2倍近く", note=NOTE_WEB)),
    ),

    # Commons「Castle Bravo 005」（火球と輪の雲・近い）。原色
    # ⚠️ 見出しを章名「見込みは、なぜ外れたのか」の写しにしない（check_dup）
    "c313": dict(
        t="外れた理由は",
        s="ブラボーの火球と輪の雲　1954年3月1日",
        photo=P("fb_close_a"), **ss.kind(P("fb_close_a")),
        color=1.0,
    ),

    "c314": dict(
        t="リチウム7の、はたらき",
        s="当時からの説明",
        fig=("process", dict(
            steps=[dict(t="リチウム7", d="劣ると見ていた燃料", c=J.LINE),
                   dict(t="速い中性子", d="当たる", c=J.AMBER),
                   dict(t="三重水素", d="ここでもできる", c=J.ALERT)])),
    ),

    # 🔴 ヤンキー 2/3（NARA #06）は色あせて明るさが 25〜125 に縮んでいる＝階調を伸ばす（出典の行に「濃淡補正」）
    "c315": dict(
        t="ブラボーだけでなく",
        s="空から見たヤンキーの火球　1954年",
        photo=P("yankee_fb_2"), **ss.kind(P("yankee_fb_2")),
        color=1.0, levels=(24, 118),
        side="right", ann_y=380,
        ann=[dict(t="予想を超えた回", d="作戦のほとんど", dc=J.ALERT)],
    ),

    "c316": dict(
        t="広く語られる説明",
        s="大きすぎた威力の説明",
        fig=("panel", dict(
            blocks=[dict(k="よく聞く説", t="リチウム7の見込み違い", c=J.AMBER)])),
    ),

    # 🔴 決め所（2024年の査読論文の要旨＝台本の web:device A2-2）
    "c317": dict(
        t="同じ研究所からの反論",
        s="研究者2人が書いた一文",
        fig=("quote", dict(
            phrase="リチウム7の見込み違い説は、誤りである",
            who="ロスアラモスの研究者2人",
            when="2024年",
            doc="査読論文の要旨")),
    ),

    # Commons「Castle Bravo (black and white)」（白黒・雲の上の火球と輪の雲）
    "c318": dict(
        t="説明は、そろわない",
        s="白黒で撮った火球と輪の雲　1954年3月1日",
        photo=P("fb_bw"), **ss.kind(P("fb_bw")),
        color=1.0,
        side="right", ann_y=356,
        ann=[dict(t="当時からの説明", d="リチウム7の見込み違い", dc=J.TICK),
             dict(t="2024年の論文", d="見込み違い説を否定", dc=J.ALERT)],
    ),

    "c319": dict(
        t="もう一つの言い伝え",
        s="広く信じられてきた話",
        fig=("panel", dict(
            blocks=[dict(k="言い伝え", t="1500万トンは、想定の外", c=J.AMBER)])),
    ),

    # 目盛りの図③（同じ目盛りに「備える上限」）＝c311 の「実際」と同じ所に立つ
    "c320": dict(
        t="上限は、計算ずみ",
        s="研究所が現地へ送った数字",
        fig=("timeline", dict(
            events=[dict(t=1500, top="備える上限", t2="1500万トン規模", c=J.AMBER, big=True)],
            band=[BAND], src="出典：国防総省の機関の報告書（2013年）・2月18日の電報　目盛り＝万トン", **MT)),
    ),

    # 報告書の表20（爆発のときの飛行機の位置）
    "c321": dict(
        t="上限に合わせて守る",
        s="報告書の表20　爆発のときの飛行機",
        photo=ss.page(215), panel=True, trim=(0.02, 0.185, 0.99, 0.975),
        side="right",
        ann=[dict(t="守りの基準", d="上限の1500万トン", dc=J.AMBER),
             dict(t="前年12月の指示", d="飛行機を離す距離", dc=J.INST)],
    ),

    # 🔴 決め所（2013年の報告書＝台本の web:device A1-5）。「はず」の留保は決め所に残っている（§5b-27b）
    "c322": dict(
        t="予定どおりなら、無事か",
        s="2013年の報告書の答え",
        fig=("quote", dict(
            phrase="予定の威力でも、人の住む島は汚れたはずだ",
            who="国防総省の機関",
            when="2013年",
            doc="報告書")),
    ),

    "c323": dict(
        t="雲の高さは似ていた",
        s="ユニオンのきのこ雲　1954年",
        photo=P("union_cloud"), **ss.kind(P("union_cloud")),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="威力の大きさ", d="悪化させた側", dc=J.ALERT),
             dict(t="雲の高さと形", d="威力との関係は小さい", dc=J.TICK),
             dict(t="ユニオン", v="700万トン", vc=J.AMBER)],
    ),

    # 4K（艦から見た火球・1.0〜7.0秒）。章の終わり＝尻で暗転（自動）
    "c324": dict(
        t="灰を運んだのは",
        s="艦から見た火球　1954年3月1日",
        **ss.vid("c324"),
        color=1.0,
    ),

}
