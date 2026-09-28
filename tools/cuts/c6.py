# -*- coding: utf-8 -*-
"""第6章 29号機に付いていなかった板 c601–c622（22カット）。13本目（トルコ航空981便）。⑤b-4（2026-09-25）で書いた。

⚠️ 12本目の中身は `git show 3832147:tools/cuts/c6.py`（⑤b-1 で空にした）。

■ 写真 6/22（SB 52-37 の頁2枚＝p5003・p5002＝引用＝額装・原色／工場の同型機 C6・D1／事故機 A3＝BY-SA 額装）
   切り出しは `ss.TRIM`（SB の頁は文字の層で行のすきま）
■ 決め所 c616（上院 p2051）・c621（仏 p80）はなぞる型（trace）
■ 錠（latch）＝c602（あの軸を支える板）・c620（ピンが7.95ミリ手前）＝第3章の見本の続き。
   ⚠️ 錠の型に「板」の部品は無い（型に部品を足すと過去の回の絵の照合が要る）＝**軸を札で指す**
■ 台本 §7 から替えたところ（⑤b-4 の決め）
  c601：SB p5002（題と一覧）→ p5003 の「改修の中身」の段（ナレーションの中身がこの段）
  c602：SB p5003 の紙面 → 錠の模式図（「図7でたわんでいた**あの軸**」＝軸がたわむ絵を戻して指す）
  c604：一覧の panel → SB p5002 の対象機の表そのもの（一覧に無いことを実物で見せる）
  c614：上院 p2051 の紙面 → 29号機の年表。2カット後の c616 が同じ頁をなぞる＝同じ紙面を2度見せない（§5b-59）
■ 国会の記録（1976年6月9日 衆議院 ロッキード問題に関する調査特別委員会）＝`ref/ep13/facts_japan.md` C4
   証人（三井物産の顧問）の名は出さない（台本のナレーションも役割だけ）
■ 実名＝ダグラス社の社長ブリゼンディン（ナレーションが名を言う・公的な証言）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
NOTE_SEN = "出典：米上院の報告"
NOTE_KK = "出典：国会会議録（1976年6月9日・衆議院の委員会の証言）"
NOTE = "模式図：4つのフックのうち1つ。形と大きさは実物どおりではない（報告書の図7の順番）"

SPEC = {

    # SB p5003（Description：(1) 3つのドアの strike plate の取り替えとピン・スイッチの調整）＝引用＝額装・原色
    "c601": dict(
        t="3つのドアの錠を直す",
        s="ダグラス社のSB 52-37（改修の中身）",
        photo=ss.page(5003), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="出した日", v="1972年7月3日", vc=J.AMBER),
             dict(t="直すドア", d="前・真ん中・後ろの貨物ドア", dc=J.TICK)],
    ),

    # 錠：図7の無理な閉め方で軸がたわむ → その軸を支える板（SB p5003「(2) Installs support and plate on aft
    #   cargo door」・仏 p67・p80「Le palier supplémentaire prévu en application du SB 52-37 … a précisément
    #   pour but de s'opposer à cette déformation」）。扱い＝「D. Compliance: Recommended.」
    #   ⚠️ 板の部品は型に無い＝2段目の札で軸を指す（札は軸の上の空き＝ハンドルと通気扉のあいだ）
    "c602": dict(
        t="たわむ軸に、支えの板",
        s="後ろのドアだけに足す改修",
        fig=("latch", dict(
            start=dict(hook="short"),
            steps=[dict(state=dict(handle="down", pin="butt", tube="bent", vent="closed"),
                        tag=dict(t="図7でたわんだ軸", at="tube")),
                   dict(tag=dict(t="この軸を板で支える", d="SBの扱いは「推奨」", at=(640, 360, "start", 400)))],
            note=NOTE, src="SB 52-37 PDF 3頁・仏の報告書 PDF 80頁・88頁")),
    ),

    # 上院 p2051（社長の証言「250 pounds rather than the 150 pounds or 120 pounds」）。3行＝前後の2つの柱
    #   ⚠️ 前の値は「150か120」＝どちらの条件かは書いていない＝2つを並べて書く（幅にしない）
    "c603": dict(
        t="改修の効き目",
        s="1974年の議会での証言",
        fig=("beforeafter", dict(
            a=dict(k="調整の前", t="約54／68キロ", lines=["120／150ポンド"], v="", c=J.LINE),
            b=dict(k="52-37の調整のあと", t="約113キロ", lines=["250ポンド"], v="", c=J.AMBER),
            lead="ピンが入らないまま、倒すのに要る力",
            note=f"{NOTE_SEN} PDF 51頁")),
    ),

    # SB p5002（対象機の表）＝引用＝額装・原色。胴体番号の欄に 29 は無い（上院 p2041・SB p5003「Affected
    #   aircraft other than those listed above will be modified prior to delivery or included in a subsequent revision」）
    "c604": dict(
        t="トルコへ渡る機体は対象外",
        s="SB 52-37の対象の一覧",
        # ⑤c'（09-25）：寄りの掃き 54px を上の余白 19px・下の余白 48px に分ける（bias 0.23＝上 12・下 42）
        photo=ss.page(5002), panel=True, color=1.0, bias=0.23,
        side="right", ann_y=330,
        ann=[dict(t="胴体の番号の欄", d="29番は載っていない", dc=J.ALERT),
             dict(t="載らない機体", d="引き渡しの前に改修", dc=J.TICK)],
    ),

    # ロングビーチの工場の同型機（C6・CC BY 3.0・全画面）。上院 p2051「would not have been subject to in-service
    #   modifications … as the aircraft was still on the Douglas assembly line at Long Beach」
    "c605": dict(
        t="1972年6月は、まだ工場に",
        s="ダグラスの工場の同じ型の機体（大韓航空・1974年）",
        photo=P("kal_longbeach_1974"), **ss.kind(P("kal_longbeach_1974")),
        side="right", ann_y=330,
        ann=[dict(t="改修の場所", d="工場（引き渡しの前）", dc=J.AMBER)],
    ),

    # 事故機 TC-JAV の尾部（A3・CC BY-SA 2.0＝額装・原色・1点1カット・札を重ねない）。番号は仏 p27・p65
    "c606": dict(
        t="29号機、製造番号46704",
        # ⑤c'（09-25）：年と場所を消した。Commons の日付は「1974年3月3日より前」だけ＝出典表の撮影年は不明（⑤c-1 の R1）。
        #   登録記号 TC-JAV は枠に写る（⑤c-2 の原寸）＝「登録記号」は残す
        s="事故機 TC-JAV の尾部と登録記号",
        photo=P("tcjav_tail"), panel=True, color=1.0,
    ),

    # 1976年6月9日 衆議院 ロッキード問題に関する調査特別委員会（facts_japan C4）
    "c607": dict(
        t="もう一つの来歴",
        s="日本の国会の記録",
        fig=("moment", dict(
            clock="6月9日", label="1976年",
            facts=[dict(t="場", v="衆議院の委員会", c=J.INST),
                   dict(t="調べていたこと", v="ロッキード事件", c=J.AMBER)],
            sub="出典：国会会議録（1976年6月9日）")),
    ),

    # 三井物産の確定注文6機（facts_japan C4 #63「三井物産の判断でファーム、確定注文を六機に」）
    "c608": dict(
        t="商社が押さえた6機",
        s="1976年の国会での証言",
        fig=("people", dict(
            nodes=[dict(x=0.22, y=0.30, t="三井物産", d="日本の商社", kind="org", c=J.AMBER),
                   dict(x=0.78, y=0.30, t="ダグラス社", d="メーカー", kind="org", c=J.INST),
                   dict(x=0.22, y=0.78, t="全日空", d="売る先のつもり", kind="org", c=J.LINE)],
            edges=[dict(a=0, b=1, t="確定の注文", c=J.AMBER), dict(a=0, b=2, t="", c=J.LINE)], pair=True,
            note=NOTE_KK)),
    ),

    # 全日空は発注していない（#246）／全日空も知っていて好ましく見ていた（#282 ほか）
    "c609": dict(
        t="全日空は注文していない",
        s="証人の説明",
        fig=("absent", dict(
            mode="pair",
            # ⑤c'（09-25）：左の n=1 は数える物が無いのに「1」が出ていた（⑤c-1 の W4）＝n を外して面1枚に
            items=[dict(t="全日空の側", d="知っていて、好ましく見ていた", ok=True, c=J.LINE),
                   dict(t="全日空の発注", d="一度も無い", ok=False, c=J.ALERT, n=0)],
            note=NOTE_KK)),
    ),

    # 納期と導入の予定（#105 書簡：納期は1972年3月から／#83：全日空の導入は1974年・1971年5月から転売先を探す）
    "c610": dict(
        t="早すぎた納期",
        s="証言が語る時期のずれ",
        fig=("timeline", dict(
            events=[dict(t=1971.37, top="1971年5月", t2="買い手を探す", c=J.AMBER),
                    dict(t=1972.17, top="1972年3月〜", t2="機体ができる", c=J.LINE),
                    dict(t=1974.0, top="1974年", t2="全日空の予定", c=J.LINE)],
            t0=1970.9, t1=1974.5,
            ticks=[(1971, "1971"), (1972, "1972"), (1973, "1973"), (1974, "1974")],
            band=[dict(a=1972.17, b=1974.0, t="早すぎる", c=J.ALERT)],
            src="国会会議録（1976年6月9日・証言と、証人が認めた1971年5月の書簡）")),
    ),

    # 転売先（#247・#248「トルコ航空の方は三機とも一緒に四十七年の九月」）。数を合わせる
    "c611": dict(
        t="3機ずつ、2社へ",
        s="6機の転売先",
        fig=("breakdown", dict(
            total=6, unit="機",
            parts=[dict(v=3, t="レーカー航空（イギリス）", c=J.LINE),
                   dict(v=3, t="トルコ航空", c=J.AMBER)],
            note=NOTE_KK)),
    ),

    # 製造番号（#199 議員の読み上げ「四六七〇四、七〇五、七二七、それから四六九〇五、九〇六、九〇七」）。
    #   事故機は仏 p27「n° de série 46.704」。証人は5桁の番号を「存じておりません」（#192）＝結び付けは議員の読み上げ
    "c612": dict(
        t="読み上げられた番号",
        s="議員の質問と証人の答え",
        fig=("icons", dict(
            n=6, on=[0], kind="plane", cols=6, oncol=J.AMBER,      # 3列2段だと下の段の番号が枠の下（927）を越えた
            labels=["46704", "46705", "46727", "46905", "46906", "46907"],
            lead="色の番号＝事故機の製造番号（仏の報告書）",
            note=NOTE_KK)),
    ),

    # #172「日本向けにつくられた仕様を一部トルコ向けに」／1972-03-24 衆院予算委第五分科会（議員）「二十九番、三十三番…」
    "c613": dict(
        t="日本向けの仕様",
        s="証言と、1972年の国会",
        fig=("panel", dict(
            blocks=[dict(k="仕様", t="改装してトルコへ", v="証人の話", c=J.AMBER),
                    dict(k="1972年3月", t="「29番」の機体", v="議員の質問", c=J.LINE)],
            note="出典：国会会議録（1976年6月9日・1972年3月24日）", cols=2)),
    ),

    # 29号機の年表：SB 52-37（1972-07-03）→ トルコ航空に決まる（1972-09・国会）→ 引き渡し（1972-12-10・仏 p27）→ パリ
    "c614": dict(
        t="引き渡しは1972年12月",
        s="事故機の歩み",
        fig=("timeline", dict(
            events=[dict(t=1972.50, top="1972年7月", t2="SB 52-37", c=J.AMBER),
                    dict(t=1972.69, top="9月", t2="トルコ航空に決まる", c=J.LINE),
                    dict(t=1972.94, top="12月", t2="引き渡し", c=J.ALERT, big=True),
                    dict(t=1974.17, top="1974年3月", t2="パリ", c=J.ALERT)],
            t0=1972.3, t1=1974.4,
            ticks=[(1973, "1973"), (1974, "1974")],
            src="SB 52-37・国会会議録（1976年）・仏の報告書 PDF 27頁")),
    ),

    # 上院 p2051「It has been reported from Paris that a key part of one of the modifications … was found missing」
    "c615": dict(
        t="パリから届いた知らせ",
        s="社長の証言の前置き",
        fig=("people", dict(
            nodes=[dict(x=0.22, y=0.45, t="パリからの報告", d="現場の後ろの貨物ドア", kind="org", c=J.INST),
                   dict(x=0.78, y=0.45, t="ダグラス社の社長", d="ブリゼンディン", kind="person", c=J.AMBER)],
            edges=[dict(a=0, b=1, t="大事な部品が1つ無い", c=J.ALERT)], pair=True,
            note=f"{NOTE_SEN} PDF 51頁")),
    ),

    # 🔴 決め所⑩（台本 §2 #10・上院 p2051）。1行のナレーション＝pre=0
    #   行の矩形は文字の層（語の箱）・上下は行のあいだでインクが0の行（0.3778・0.3898・0.4022・0.4142）＝§5b-58
    #   切り口：上＝段落の上の白い行 0.3171（「Mr. John Brizendine … explained it this way:」から）・下＝0.4142
    "c616": dict(
        t="書類の上では、済み",
        s="議会での社長の言葉",
        fig=("trace", dict(
            page=ss.page(2051),
            lines=[(0.1150, 0.3778, 0.8520, 0.3898), (0.0950, 0.3898, 0.8530, 0.4022),
                   (0.0962, 0.4022, 0.5641, 0.4142)],
            phrase="製造の記録では、改修はすべて済んでいた",
            doc="米上院の報告 PDF 51頁の原文",
            crop=(0.075, 0.3171, 0.875, 0.4142))),
    ),

    # ロングビーチの工場の同型機（D1・CC BY 3.0・全画面）。上院 p2051「we are continuing to investigate」／
    #   Senator Cannon「with Douglas certifying that its own service bulletin 52-37, had been accomplished,
    #   when in fact it had not」
    "c617": dict(
        t="説明できない食い違い",
        # ⑤c'（09-25）：Commons の説明は「N1826U・製造番号 46625/169・初飛行 1974年8月7日・引き渡し 1975年2月27日」、
        #   撮影 1974年8月・ロングビーチ空港＝**工場とは書いていない**（c605 は「DC-10 plant in Long Beach」と明記）。
        #   出典に書いてある「引き渡し前」に直した（機首の 169 は製造の通し番号）
        s="引き渡し前の同じ型の機体（ユナイテッド航空）　1974年",
        photo=P("ua_longbeach_1974"), **ss.kind(P("ua_longbeach_1974")),
        side="right", ann_y=330,
        ann=[dict(t="社長の答え", d="調べている途中", dc=J.TICK),
             dict(t="上院の議員", d="書類は済み、実物は未了", dc=J.ALERT)],
    ),

    # 隣のレーカー航空の機体（上院 p2051「the other aircraft belonged to the Laker Airways」・p2052・p2055・国会）
    "c618": dict(
        t="隣の機体も同じ",
        s="引き渡しの前の工程",
        fig=("icons", dict(
            n=2, on=[0, 1], kind="plane", cols=2, oncol=J.AMBER,
            labels=["トルコ航空へ", "レーカー航空へ"],
            lead="工程で隣どうしの2機",
            note=f"{NOTE_SEN} PDF 51〜52頁・55頁　2機とも、52-37は全部は済んでいない")),
    ),

    # はんこの2人と、特定できない作業員（上院 p2053）。役割だけ（名前は出さない）
    "c619": dict(
        t="板を付けた、という印",
        s="工場の書類の記録",
        fig=("icons", dict(
            n=3, on=[0, 1], kind="person", cols=3, oncol=J.ALERT,
            labels=["品質の検査員", "製造の副職長", "作業員（特定できず）"],
            lead="色の2人＝はんこを押した人",
            note=f"{NOTE_SEN} PDF 53頁")),
    ),

    # 錠：仏 p67（改修の抜け＝メーカーの見落とし）・p78〜p80（事故機の調整を新しいドアに写した試験）。
    #   「réglage du lock tube insuffisant de 7,95 mm」＝ピンは縁で止まる（図7の無理な閉め方）
    #   ⚠️ 1段目に動き（1行目が長い＝止まる時間を作らない）
    "c620": dict(
        t="板の抜けと、調整の誤り",
        s="フランスの報告書の見方",
        fig=("latch", dict(
            start=dict(hook="short"),
            steps=[dict(state=dict(handle="down", pin="butt", tube="bent", vent="closed"),
                        tag=dict(t="支えの板が無い軸", d="メーカーの見落とし", at="tube")),
                   dict(tag=dict(t="調整も誤り", d="事故機の調整を写して試す", at="handle")),
                   dict(tag=dict(t="ピンの調整が7.95ミリ不足", at="pin"))],
            rel=[dict(t="7.95ミリ", src="仏 p80「réglage du lock tube insuffisant de 7,95 mm」")],
            note=NOTE, src="仏の報告書 PDF 67頁・78〜80頁")),
    ),

    # 🔴 決め所⑪（台本 §2 #11・仏 p80）。2行のナレーション＝pre=0
    #   行の矩形は文字の層（語の箱）：「la poignée a pu être ainsi fermée」＋「avec un effort de 22 daN」
    #   切り口＝段落「Lors des essais effectués …（fig. 7).」の上下の白い行（文字の層 0.3341〜0.3588・0.4418〜0.4665）
    "c621": dict(
        t="試験で閉まったハンドル",
        s="フランスの最終報告書の試験",
        fig=("trace", dict(
            page=ss.page(80),
            lines=[(0.4839, 0.3775, 0.8204, 0.4005), (0.5849, 0.4015, 0.8315, 0.4204)],
            phrase="ハンドルは、約22キロの力で閉まった",
            doc="原文（PDF 80頁）",
            crop=(0.27, 0.345, 0.94, 0.454))),
    ),

    # 章の橋（副題は10本目からの型「ここまでと、この先」）。仏 p80（正しい調整なら板が無くても倒れない）・p104（のぞき窓）
    "c622": dict(
        t="飛び立つ日へ",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="正しい調整なら", t="板が無くても倒れない", c=J.LINE),
                    dict(k="外から分かる手", t="のぞき窓だけ", c=J.AMBER),
                    dict(k="次は", t="その日の空", v="第7章", c=J.ALERT)],
            cols=3)),
    ),

}
