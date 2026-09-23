# -*- coding: utf-8 -*-
"""第1章 予想をはるかに超えた爆発 c101–c114（14カット）。12本目（キャッスル・ブラボー）。

■ 実写 9/14（64%・台本 §3 の配分どおり）。c101・c102・c110 は動く映像（`footage.USE`）。
■ 🔴 冒頭は葦の分析を受けた決定（案B）の**最初の適用**（記憶 project-jiko-visual-variety-from-ep12）
  c103＝報告書の実物をなぞる型（`trace`）：DNA p212 の英文に蛍光ペン→和訳（決め所の扱いは quote と同じ）
  c104＝NARA の空撮を約3秒（`intro`）→ 地図。爆心から東へ点の列が流れ、「第五福竜丸」で船の輪郭と札
  c105＝同じ地図。ビキニから東北東へ157キロの寸法線 → 船から西へ視線の線とその先の光 → 「数時間後」
       の札 → 船の上に白い点が降りはじめる（**人は描かない・灰の広がりの形は描かない**）
  位置と距離は DNA p212「a Japanese fishing boat 85 nmi (157 km) east-northeast of Bikini」／
  「Rongerik, 135 nmi (250 km) east of the burst」。門番＝`tools/check_drift.py`
■ 🔴 爆発の実写は原色（`color=1.0`）＝c101・c102・c104 の空撮・c114（09-23 決定 §5b-33b）
■ ⚠️ 閃光は爆発の瞬間だけ（c101・c501）。c101 は DOE の 4.85秒（射点の小屋→火球の切り替わり）
  ＝`rate` 0.63 で中身の頭から 1.43秒（`footage.USE` の注）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC_DNA = ss.SRC_DNA
# 地図（c104・c105 で同じ1枚。第4〜7章でも戻る＝葦の「冒頭の物が戻る」を事実の地図で）
# ⑤b-3（2026-09-23）で定数を `cuts/ss.py` の `MAP_*` へ移した（ここは `ss.drift_map()` を呼ぶだけ）

SPEC = {

    # 夜明け前の射点 → 閃光。動く映像（DOE 4.0〜13.0秒・0.63倍）
    "c101": dict(
        t="夜明け前の、実験場",
        s="射点の小屋から、火球へ　1954年3月1日",
        **ss.vid("c101"),
        color=1.0,
        flash=1.43,
    ),

    # 艦から見た火球（4K 37〜48秒）。数字は注記が持つ
    "c102": dict(
        t="見込みを、大きく超えた",
        s="艦から見た火球　1954年3月1日",
        **ss.vid("c102"),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="TNT火薬に直すと", v="1500万トン", vc=J.AMBER),
             dict(t="いちばんありそうな値", v="600万トン", vc=J.TICK)],
    ),

    # 🔴 決め所①。報告書の実物をなぞる型（DNA p212 の原文「This yield was much greater than expected.」）
    #    ⚠️ 文は2行にまたがる（1行目の右端→2行目の左端）＝蛍光ペンは**読む順に**行ごとに塗る
    "c103": dict(
        t="原文は、こう書いていた",
        # ⚠️ 副題に「国防原子力局」「212頁」を書かない＝図の出どころの行と同じ語（check_dup）
        s="爆発の威力について",
        fig=("trace", dict(
            page=ss.page(212),
            lines=[(0.7010, 0.5510, 0.8866, 0.5697), (0.1599, 0.5744, 0.3726, 0.5931)],
            phrase="爆発の威力は、予想よりはるかに大きかった",
            doc=f"{SRC_DNA} 212頁の原文",
            crop=(0.12, 0.50, 0.92, 0.645))),
    ),

    # 空撮を約3秒 → 地図。爆心から東へ点の列（灰の**向き**だけ）→ 船の輪郭と札
    "c104": dict(
        t="その先の海に、一隻の漁船",
        # ⚠️ 副題に「ビキニ環礁」を書かない＝地図の札と同じ語（check_dup）
        s="爆発のあと、東の海では",
        intro=dict(photo=P("fb_aerial_a"), sec=3.0, color=1.0),
        fig=("drift", ss.drift_map(
            steps=[dict(move=[dict(kind="stream", a="gz", dir="東", km=190)]),
                   dict(ship=dict(at="ship", t="第五福竜丸"))])),
    ),

    # 同じ地図。寸法線 → 視線の線とその先の光 → 「数時間後」→ 白い点が降りはじめる
    "c105": dict(
        t="見ていた光、降ってきた灰",
        s="3月1日の夜明け前から",
        fig=("drift", ss.drift_map(
            steps=[dict(ship=dict(at="ship", t="第五福竜丸"),
                        dim=dict(a="bikini", b="ship", t="157キロ", d="東北東")),
                   dict(move=[dict(kind="sight", a="ship", b="gz")]),
                   # ⚠️ 札は船の下＝左は寸法線と視線の線が入ってくる（試し焼きで重なった）
                   dict(tag=dict(at="ship", t="数時間後", side="below"),
                        move=[dict(kind="fall", at="ship")])])),
    ),

    # 🔴 ⑤c'（09-23）：写真（米艦の甲板で浮きを下ろす水兵＝fo_buoy）をやめて図にした。見出し「乗組員の体に」と
    #    並べると、米兵が第五福竜丸の乗組員に見えた（⑤c 原寸 p05・台帳 §7-6 A1）。23人＝点の数を合わせる（§5b-6）。
    #    c602 と同じ部品＝**色（ALERT）と言葉を変えて**同じ絵に見せない。出典は台本 c106 の DNA p476・p478（覚え書き）
    "c106": dict(
        t="乗組員の体に、何が起きたか",
        s="第五福竜丸に乗っていた人",
        fig=("icons", dict(
            n=23, on=23, kind="person", cols=12, oncol=J.ALERT,
            lead="灰を浴びた人　23人",
            note="痛みが出るまで　1週間ほど（日本政府の覚え書き）")),
    ),

    # ⚠️ 実名は久保山愛吉さんだけ（台本 §1-2）
    "c107": dict(
        t="半年後の、秋に",
        s="第五福竜丸の無線長",
        fig=("panel", dict(
            blocks=[dict(k="無線長", t="久保山愛吉さん", v="", c=J.INK_W),
                    dict(k="亡くなった日", t="1954年9月23日", v="", c=J.ALERT)],
            cols=2, note="出典：焼津市・広島平和記念資料館ほかの公開資料")),
    ),

    # ロンゲラップに上がる調査の一行（米海軍の乗組員と測定係＝原寸で私人なしを確認）
    "c108": dict(
        t="灰は、島々にも降った",
        s="ロンゲラップに上がる調査の一行　1954年",
        photo=P("rongelap_landing"), **ss.kind(P("rongelap_landing")),
        side="right", ann_y=356,
        ann=[dict(t="島の住民", v="239人", vc=J.AMBER),
             dict(t="アメリカ兵", v="28人", vc=J.AMBER)],
    ),

    "c109": dict(
        t="確かめたいのは、二つ",
        s="このあと確かめること",
        fig=("panel", dict(
            blocks=[dict(k="問い1", t="威力の外れ", v="島まで灰が届いた理由か", c=J.AMBER),
                    dict(k="問い2", t="灰の運び手", v="人の住む島へ向かわせたもの", c=J.ALERT)],
            cols=2)),
    ),

    # 艦から見た雲（4K 25〜37秒・寄り 1.6）
    "c110": dict(
        t="広く語られてきた説",
        s="艦から見た雲　1954年3月1日",
        **ss.vid("c110"),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="よく語られる答え", v="高さ6キロの風", vc=J.TICK),
             dict(t="2013年の報告書", v="違う答え", vc=J.ALERT)],
    ),

    # 報告書の表紙（頁の実物・額装）
    "c111": dict(
        t="英語の原文で、確かめた",
        s="国防原子力局の報告書の表紙　1982年",
        photo=ss.page(1), panel=True,
        side="right", ann_y=300,
        ann=[dict(t="国防総省の機関", v="1982年・2013年", vc=J.DOC, vs=64),
             dict(t="医師団の報告書", v="1954年", vc=J.DOC, vs=64),
             dict(t="日本側", v="政府と国会", vc=J.DOC, vs=64)],
    ),

    "c112": dict(
        t="日付は、現地のもの",
        s="日付変更線をはさんで",
        fig=("panel", dict(
            blocks=[dict(k="この動画", t="ビキニの現地", v="3月1日", c=J.AMBER),
                    dict(k="アメリカ本土", t="日付変更線の東", v="2月28日", c=J.TICK),
                    dict(k="公式の一覧", t="世界の標準時", v="2月28日", c=J.TICK)],
            cols=3)),
    ),

    # 射点の小屋の装置と作業の人たち（米国側の作業員＝公的な任務）
    "c113": dict(
        t="爆発した装置の名",
        s="射点の小屋の中の装置と作業の人たち　1954年",
        photo=P("dev_shrimp_men"), **ss.kind(P("dev_shrimp_men")),
        side="left", ann_y=356,
        ann=[dict(t="呼び名", v="シュリンプ", vc=J.AMBER, vs=72),
             dict(t="めざした形", d="飛行機で運べる大きさ", dc=J.TICK)],
    ),

    # ブラボーの火球（色のまま）。章の終わり＝尻で暗転（自動）
    "c114": dict(
        t="問いは、ここから",
        s="ブラボーの火球　1954年3月1日",
        photo=P("fb_color_a"), **ss.kind(P("fb_color_a")),
        color=1.0,
    ),

}
