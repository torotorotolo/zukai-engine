# -*- coding: utf-8 -*-
"""第4章　船の上に客室を足した c401–c416（16カット）。14本目（セウォル号）。

■ 🔴 2026-09-28（⑤b-1）：13本目（トルコ航空981便）の中身を空にした＝git の `b54ee4f`（`git show b54ee4f:tools/cuts/c4.py`）。
  ⚠️ 第10〜13章（ca〜cd）は14本目で初めてのファイル（13本目までは9章）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep14/make_plan.py` で
  台本 §4・承認ずみの絵コンテ（映像方針 §2-2・§4）・追補 §4・§7 から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2〜⑤b-7 で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝⑤b-7 の門番 check_text_screens が「文字だけ2割まで・3カット以上続けない」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所（ルール §5b-79）
  記号＝【案C】再現イラスト（置き場 A〜E）・【F】断面F・【地図】drift・【年表】【帯】【棒】【マス】【人の形】【書類】【流れ】【並べ】（追補 §3）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    "c401": dict(kind='図解',
               plan='【F】断面F（承認ずみ §2-2＝動く模式図）｜台本の画：図 改造の前と後（船尾の上に客室を足す）',
               src='海審 p1016'),
    "c402": dict(kind='図解',
               plan='【F】断面F（承認ずみ §2-2＝動く模式図）｜台本の画：図 A甲板の船尾（天井を約1.7メートル上げて2層に）',
               src='海審 p1016'),
    "c403": dict(kind='図解',
               plan='【F】断面F（承認ずみ §2-2＝動く模式図）｜台本の画：図 上＝展示室／下＝客室114人',
               src='海審 p1016'),
    "c404": dict(kind='図解',
               plan='【F】断面F（承認ずみ §2-2＝動く模式図）｜台本の画：図 B甲板の船尾（車の置き場 → 運転手の客室56人）と車の渡し板（ランプ）の撤去',
               src='海審 p1016'),
    "c405": dict(kind='図解',
               plan='【F】断面F（承認ずみ §2-2＝動く模式図）｜台本の画：図 重心と復原力（模式図）',
               src='—'),
    "c406": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='海審 p1018'),
    "c407": dict(kind='図解',
               plan='【棒】改造の前と後（貨物の上限）（追補 §4）',
               src='海審 p1018'),
    "c408": dict(kind='図解',
               plan='台本の画：図 バラスト（船の底のタンクに入れる重しの水）',
               src='海審 p1017・p1018'),
    "c409": dict(kind='図解',
               plan='【F】荷を減らす（↓）・底のタンクに水（↑）（追補 §4）',
               src='海審 p1017'),
    "c410": dict(kind='図解',
               plan='【棒】同じ「前と後」の棒に定員（追補 §4）',
               src='海審 p1017・p1018'),
    "c411": dict(kind='図解',
               plan='【F】長さ・幅・深さの矢印は変わらない・足したのは上の客室（数字なし・模式）（追補 §4）',
               src='海審 p1017'),
    "c412": dict(kind='写真',
               plan='台本の画：実写 M1 モッポ新港のセウォル号の船体（2017年8月2日・CC BY-SA 4.0・額装・船尾の上の階に枠）',
               src='裁決 p2050'),
    "c413": dict(kind='図解',
               plan='【年表】改造と就航のあいだの点（追補 §4）',
               src='海審 p1022'),
    "c414": dict(kind='図解',
               plan='【F】展示室に大理石の印（「検査のあと」）（追補 §4）',
               src='海審 p1017・p1024'),
    "c415": dict(kind='パネル',
               plan='台本の画：panel 軽く見積もられた船',
               src='海審 p1017'),
    "c416": dict(kind='図解',
               plan='【F】空の甲板に「？」→第5章の写真へ（追補 §4）',
               src='—'),
}

SPEC = {
    # ── 🔴 ⑤b-4（2026-09-29）：断面F＝`tools/hull.py`（門番 check_mech の judge_hull）──
    # 形のもと＝海審 p1013（要目）・p1018〜p1020（甲板の並びと天井の高さ）。改造＝p1016 2.2.4〜2.2.6。
    # 🔴 部屋の前後の位置と長さ・通路の幅は記録に無い＝模式（note に書く）。長さ・高さの数は記録の値（門番が画素で測る）。
    #   札に出す数は rel に宣言。人は描かない。「改造の前」の札は付けない（段の札は残る＝変わったあとも「前」と読める）
    "c401": dict(
        t="船尾の上に足した部屋",
        s="2012年10月〜2013年2月の改造",
        fig=("hull", dict(view="side", start=dict(aroof="low", aext="off", bcab="off", hl="new"),
                          steps=[dict(tag=dict(m=(3.0, 33.0), t="船の後ろ（船尾）", to=(9.0, 27.0))),
                                 dict(state=dict(aroof="high", aext="on", bcab="on"),
                                      tag=dict(m=(40.0, 33.0), t="上に部屋を足した", to=(26.0, 27.2)))],
                          note=ss.HULL_NOTE, src=ss.src(["海審 p1013", "海審 p1016", "海審 p1018・p1019・p1020"]))),
    ),

    # 船尾の寄り：天井を約1.7メートル上げる → 下の階（A甲板）を約5.6・上の階（船橋甲板）を約2.6 延ばして2層に（p1016 2.2.4）
    "c402": dict(
        t="A甲板の船尾の部屋",
        s="天井を上げて、上と下の2つの階に",
        fig=("hull", dict(view="stern", start=dict(aroof="low", aext="off", bcab="off", hl="new"),
                          steps=[dict(state=dict(aroof="high"), dim=dict(kind="rise", t="約1.7メートル"),
                                      tag=dict(m=(19.0, 29.6), t="天井を上げた")),
                                 dict(state=dict(aext="on"), dim=dict(kind="ext", ta="約5.6メートル", tb="約2.6メートル"),
                                      tag=dict(m=(36.0, 29.6), t="延ばして2つの階に"))],
                          rel=[dict(t="約1.7メートル", src="海審 p1016"), dict(t="約5.6メートル", src="海審 p1016"),
                               dict(t="約2.6メートル", src="海審 p1016")],
                          note=ss.HULL_NOTE, src=ss.src(["海審 p1016", "海審 p1018・p1019"]))),
    ),

    # 上の階＝展示室・下の階＝客室（定員114人＝p1016。人数は字幕だけ）。B甲板の運転手の客室は次の c404 で足す
    "c403": dict(
        t="展示室と客室",
        s="改造でできた2つの階",
        fig=("hull", dict(view="stern", start=dict(bcab="off", hl="new"),
                          steps=[dict(tag=[dict(m=(24.5, 24.9), t="展示室", cap=40),
                                           dict(m=(24.5, 22.3), t="客室", cap=40)])],
                          note=ss.HULL_NOTE, src=ss.src(["海審 p1016"]))),
    ),

    # B甲板の船尾の乗用車の置き場 → 運転手の客室（長さ約10.5・定員56人＝p1016 2.2.5）／船首の右側の渡し板（約50トン）を外した（2.2.6）
    "c404": dict(
        t="車の置き場を客室に・渡し板を外す",
        s="B甲板の船尾と、船首の右側",
        fig=("hull", dict(view="side", start=dict(bcab="off", ramp="on", hl="new"),
                          steps=[dict(state=dict(bcab="on"), tag=dict(m=(3.0, 33.0), t="運転手の客室", to=(7.0, 20.4))),
                                 dict(state=dict(ramp="gone"),
                                      tag=dict(m=(99.0, 33.0), t="右側の渡し板を外した", to=(91.5, 17.4)))],
                          note=ss.HULL_NOTE + "。渡し板の位置と大きさは模式", src=ss.src(["海審 p1016"]))),
    ),

    # 重心と復原力（台本の画「模式図」）＝足す前と足したあとを並べる。重心の上がり方は大きく描く（記録＝約51センチ・表1）
    "c405": dict(
        t="重心と復原力",
        s="足す前と、足したあと",
        fig=("hull", dict(view="pair",
                          steps=[dict(tag=[dict(at="lh", t="足す前"), dict(at="rh", t="足したあと"),
                                           dict(at="gl", t="重心", cap=34, to_px=(496, 545))]),
                                 dict(state=dict(add="on", g="high", up="on"),
                                      tag=dict(at="gr", t="重心が上がる", cap=34, to_px=(1250, 509))),
                                 dict(state=dict(heel=15.0, up="off", force="on"),
                                      tag=dict(at="top", t="復原力（戻す力）"))],
                          rel=[dict(heel=15.0, src="模式（傾けて見せるための角度）")],
                          note="模式図：重心の上がり方と力の大きさは大きく描いた（記録は重心が約51センチ上がった）",
                          src=ss.src(["海審 p1017・p1018"]))),
    ),

    # 認められた条件＝積める荷 2,437→987トン・平衡水 370→1,703トン（p1017 2.2.9・p1018 表1）。量は表1の値の比で描く
    "c409": dict(
        t="認められた条件",
        s="積み荷と重しの水",
        fig=("hull", dict(view="hold", start=dict(cargo="load", ballast="before"),
                          steps=[dict(state=dict(cargo="less", ballast="req", arrows="on"),
                                      tag=[dict(m=(46.5, 17.2), t="荷を減らす"),
                                           dict(m=(46.5, -3.0), t="底のタンクに水を足す")]),
                                 dict(tag=dict(m=(62.0, 17.2), t="改造のあとの積み方"))],
                          note=ss.HULL_NOTE + "。荷と水の量は表の値の比", src=ss.src(["海審 p1017・p1018"]))),
    ),

    # 許可が要るのは長さ・幅・深さ・使い道が変わるとき（p1017 2.2.10・注5）＝足したのは上の部屋だけ（数字は書かない）
    "c411": dict(
        t="許可の要らなかった改造",
        s="船舶安全法の事前の許可",
        fig=("hull", dict(view="side", start=dict(hl="new"),
                          steps=[dict(tag=dict(m=(3.0, 33.0), t="足したのは上の部屋", to=(14.0, 26.0))),
                                 dict(dim=[dict(kind="len"), dict(kind="dep"), dict(kind="bre")],
                                      tag=dict(m=(58.0, 33.0), t="長さ・幅・深さは変わらない"))],
                          note=ss.HULL_NOTE, src=ss.src(["海審 p1013", "海審 p1017"]))),
    ),

    # 検査のあとに足した展示室の大理石 約37トン（p1024 2.4.8）が計算に入っていない（p1017 注2）
    "c414": dict(
        t="計算に入らなかった重さ",
        s="検査のあとに足した大理石",
        fig=("hull", dict(view="stern", start=dict(bcab="on"),
                          steps=[dict(tag=dict(m=(19.0, 29.6), t="計算に入っていない重さ")),
                                 dict(state=dict(marble="on"),
                                      tag=dict(m=(36.0, 28.6), t="展示室の大理石", d="検査のあと・約37トン",
                                               to=(23.0, 25.3)))],
                          # 🔴 ⑤b-7b：門番 check_mech の数の単位に「トン」を足したら宣言漏れで鳴った（値は p1024 2.4.8 で正しい）
                          rel=[dict(t="約37トン", src="海審 p1024")],
                          note=ss.HULL_NOTE + "。大理石の置き場所は模式", src=ss.src(["海審 p1017", "海審 p1024"]))),
    ),

    # 積み荷の甲板（トゥイーン・C・D・E＝裁決 p2031 の「적재할 수 있는 장소」と同じ並び）に「？」
    "c416": dict(
        t="積み荷は？",
        s="事故の前の晩",
        fig=("hull", dict(view="side", start=dict(cargo="none"),
                          steps=[dict(tag=[dict(m=(52.0, 9.2), t="？", cap=64), dict(m=(22.0, 15.4), t="？", cap=52),
                                           dict(m=(74.0, 3.0), t="？", cap=52), dict(m=(112.0, 15.6), t="？", cap=52)])],
                          note=ss.HULL_NOTE, src=ss.src(["海審 p1018・p1019・p1020"]))),
    ),

    # ── 🔴 ⑤b-5（2026-09-29）：軸の型＝`tools/axis.py`（門番 check_axis）──
    # 傾斜試験＝2013年1月24日・モッポ港（海審 p1022）＝改造の終わり（2月12日）の前・初めての運航（3月16日）の前
    "c413": dict(
        t="モッポ港で",
        s="韓国船級が立ち会い",
        fig=("axis", dict(ss.AX_KAIZO,
                          past=[ss.ax("import"), ss.ax("kaizo"), ss.ax("first")],
                          start=dict(cur="2013-02-12"),
                          steps=[dict(add=ss.ax("incline", big=True), cur="2013-01-24"), dict(), dict()],
                          note="年表：月の寄り", src=ss.src(["海審 p1016", "海審 p1022", "海審 p1026"]))),
    ),

    # ── 🔴 ⑤b-6（2026-09-29）：量の型（棒）＝`tools/qty.py`（門番 check_qty）。表1（海審 p1018）＝数は字幕だけ ──
    # 貨物の上限 2437→987（4割ほど＝「改造の後」の行に、改造の前の長さの破線の枠）
    "c407": dict(
        t="改造で減ったもの",
        s="報告書の表1",
        fig=("qty", dict(view="bar", groups=[ss.QG["cargo"]],
                         steps=[dict(add=[ss.qb("cargo_before"), ss.qb("cargo_after")]),
                                dict(add=dict(k="ghost", g="cargo", row="改造の後", v=2437, rec="海審 p1018")),
                                dict()],
                         src=ss.src(["海審 p1018"]))),
    ),

    # 定員 840→956（c407 の貨物の棒を沈めて上に残す＝貨物は減り、人は増えた）
    "c410": dict(
        t="改造で増えたもの",
        s="報告書の表1",
        fig=("qty", dict(view="bar", groups=[ss.QG["cargo"], ss.QG["pax"]],
                         past=[ss.qb("cargo_before"), ss.qb("cargo_after")],
                         steps=[dict(add=[ss.qb("pax_before"), ss.qb("pax_after")])],
                         src=ss.src(["海審 p1017", "海審 p1018"]))),
    ),

    # ── 🔴 ⑤b-7a（2026-09-29）：写真 ──
    # M1（CC BY-SA 4.0＝額装・無改変・1点1カット）。2017年8月2日・モッポ新港（Commons の撮影日）。
    #   ⚠️ PLAN の「船尾の上の階に枠」は描かない＝BY-SA に重ねない（§5b-52）。しかも**どちらが船首かを写真だけで決められない**
    #   （原寸で見た・09-29）＝額の外の向きの札も付けない。語りの「後ろの上の階」は ⑤c で見て相談（引き継ぎ §4）
    "c412": dict(
        t="陸に上がった船体",
        s="2017年8月2日　モッポ新港",
        photo=P("mokpo_2017"), panel=True, color=1.0,
    ),

    # ── 🔴 ⑤b-7b（2026-09-29）：決め所・台本の図・パネル ──
    # 決め所④（台本 §2 #4）。海審 p1018〔표1〕「무게중심 11.27미터 → 11.78미터 0.51미터 상승」（p1017 2.2.9「약 51㎝」）
    "c406": dict(
        t="改造と重心",
        s="報告書の表1",
        fig=("quote", dict(
            phrase="改造で、船の重心が51センチ上がった",
            rows=[("記録", "海洋安全審判院の特別調査報告", J.INK_W),
                  ("頁", "PDF 18頁（2014年12月公表）", J.TICK)], paper=True)),
    ),

    # バラスト＝改造の前 370トン → 改造のあとの条件 1,703トン（海審 p1018 表1）。底のタンクの水の高さは容量の比（p1044 表7）
    "c408": dict(
        t="バラストの量",
        s="改造の前と、あとの条件",
        fig=("hull", dict(view="hold", start=dict(ballast="before"),
                          steps=[dict(tag=dict(m=(22.0, -3.0), t="底のタンクの水（バラスト）", to=(30.0, 0.3))),
                                 dict(state=dict(ballast="req"))],
                          note=ss.HULL_NOTE + "。水の量は表1・表7の値の比", src=ss.src(["海審 p1018", "海審 p1044"]))),
    ),

    # 海審 p1017 注2「선미가 잠기는 깊이를 잘못 계산하여 과소 산정된 무게」＝経下重量（空の船の重さ）。差を絵にすると記録に無い量を
    #   描く（追補 §5）＝パネル
    "c415": dict(
        t="軽く見積もられた船",
        s="改造のあとの計算",
        fig=("panel", dict(blocks=[dict(k="誤り", t="船尾の喫水の計算", c=J.AMBER),
                                   dict(k="結果", t="空の船の重さが少なく出た", c=J.ALERT)])),
    ),
}
