# -*- coding: utf-8 -*-
"""第6章 塔へ渡った c601–c629（29カット）。

■ この章の役目
  **追うのは、下端筋の線図（p139）。NIST が刺激の強さを断っている範囲なので、絵は図で組む。**
  決め所は c614「下端筋が、下から抜けていく」。
  🔴 p133 は全カットで**左の平面図側**（右の断面写真＝室内が見える）は出さない。ファイルの時点で切ってある。

■ 出どころ
  技術的知見 p3・p29・p133・p139・section 4／NIST ニュース 2026-06-22／B-Roll #1・#8。
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── c601 大きな疑問 ───────────────────────
    "c601": dict(
        t="疑問が、ひとつ残る",
        s="6月初旬から6月24日まで（section 2）",
        fig=("timeline", dict(
            t0=0, t1=30, title="単位は日（2021年6月）",
            ticks=[(3, "6月初旬"), (10, "6月10日"), (17, "6月17日"), (24, "6月24日")],
            events=[dict(t=3, top="押し抜き", t2="柱2本と床のつなぎ目", c=J.ALERT),
                    dict(t=24, top="塔の崩落", t2="なぜ、塔まで？", c=J.INK_W, big=True)])),
    ),

    # ── c602 プールデッキは本体ではない ──────────────
    "c602": dict(
        t="住んでいたのは、12階建てのほう",
        s="プールデッキと塔の位置（p3）",
        photo=ss.P003, side="left", ann_y=330, color=0.35,
        **ss.focus(ss.P003, 0.52, 0.50, 1.3),
        ann=[dict(t="塔", d="12階建て・人が住む", dc=J.INK_W, ds=32),
             dict(t="プールデッキ", d="建物の本体ではない", dc=J.ALERT, ds=32)],
    ),

    # ── c603 問いの立て方 ─────────────────────
    "c603": dict(
        t="屋外の床が落ちて、なぜ塔が倒れるか",
        s="問いの立て方",
        fig=("panel", dict(
            lead="この章の問い",
            blocks=[dict(k="落ちた", t="屋外の平らな床（プールデッキ）", c=J.AMBER),
                    dict(k="倒れた", t="人の住んでいた建物（塔）", c=J.ALERT)],
            cols=2, note="この2つは、どうつながっていたのか")),
    ),

    # ── c604 つながっていたから ───────────────────
    "c604": dict(
        t="答えは、つながっていたから",
        s="デッキと塔の接続（p29）",
        photo=ss.P029, side="right", ann_y=330, color=0.35,
        **ss.focus(ss.P029, 0.52, 0.62, 1.5),
        ann=[dict(t="プールデッキ", d="塔に直結（一体）", dc=J.ALERT, ds=30)],
    ),

    # ── c605 接合の模式 ──────────────────────
    "c605": dict(
        t="床の端が、壁と柱にそのまま続く",
        s="デッキと塔の接合（模式）",
        fig=("people", dict(
            lead="隣り合った別々の建物、ではない",
            nodes=[dict(x=0.24, y=0.50, t="プールデッキの床", d="平らな床の端", kind="part",
                        c=J.AMBER),
                   dict(x=0.74, y=0.50, t="塔の壁と柱", d="建物本体", kind="part", c=J.INK_W)],
            edges=[dict(a=0, b=1, t="そのまま続いている（一体）", c=J.ALERT)],
            note="模式図。NIST の3D（p29）にもとづく関係だけを描いた")),
    ),

    # ── c606 落ちるときに引く ──────────────────
    "c606": dict(
        t="つながっている側を、引きながら落ちる",
        s="落ちるときに起きること",
        fig=("absent", dict(
            mode="pair", lead="床が落ちるとき",
            items=[dict(t="ただ下に落ちる", d="つながっていなければ", ok=False, c=J.LINE),
                   dict(t="つながっている側を引く", d="この建物では、こちら", ok=True, c=J.ALERT)])),
    ),

    # ── c607 実物大で作ったのはこの部分 ───────────────
    "c607": dict(
        t="作ったのは、まさにこの境目",
        s="試験の全景（NIST 記録映像・ミネソタ大学）",
        photo=ss.fb("c607"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="レプリカ", d="デッキと塔の境目（interface）", dc=J.ALERT, ds=32)],
    ),

    # ── c608 試験の名前 ───────────────────────
    "c608": dict(
        t="落ちる側と残る側を、両方作った",
        s="試験の名前（NIST／ミネソタ大学）",
        fig=("panel", dict(
            lead="Replicas of the CTS Pool-Deck and Tower Interface",
            blocks=[dict(k="名", t="接続部（interface）の試験", c=J.INST),
                    dict(k="中身", t="落ちる側（デッキ）と残る側（塔）を、まとめて再現", c=J.LINE)],
            cols=2, note="表題は B-Roll #8 の冒頭カードの原文")),
    ),

    # ── c609 柱D・E・H・I の線図 ─────────────────
    "c609": dict(
        t="柱が4本、D・E・H・I",
        s="起きたことの線図（p139）",
        photo=ss.P139, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P139, 0.48, 0.45, 1.0),
        ann=[dict(t="D E H I", d="4本の柱の記号", dc=J.LINE, ds=32)],
    ),

    # ── c610 残る側 ──────────────────────
    "c610": dict(
        t="左の床は、水平に残る",
        s="残る側（p139）",
        photo=ss.P139, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P139, 0.25, 0.50, 1.7),
        ann=[dict(t="D〜E", d="そのまま水平", dc=J.OK, ds=32),
             dict(t="E から右", d="ここから変わる", dc=J.ALERT, ds=32)],
    ),

    # ── c611 傾く床 ──────────────────────
    "c611": dict(
        t="右の床は、外れて斜めに下がる",
        s="傾く床（p139）",
        photo=ss.P139, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P139, 0.72, 0.55, 1.7),
        ann=[dict(t="H・I の側", d="端に行くほど、深く落ちる", dc=J.ALERT, ds=32)],
    ),

    # ── c612 つなぎ目で切れる ──────────────────
    "c612": dict(
        t="折れたのではない。柱で切れた",
        s="p139 の線図から",
        fig=("absent", dict(
            mode="pair", lead="板が切れた場所",
            items=[dict(t="真ん中", d="折れていない", ok=False, c=J.LINE),
                   dict(t="柱のあるところ", d="ここで切れている", ok=True, c=J.ALERT)])),
    ),

    # ── c613 下端筋の破断 ──────────────────
    "c613": dict(
        t="札が指すのは、板の下側の鉄筋",
        s="NIST の札（p139）",
        photo=ss.P139, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P139, 0.42, 0.66, 2.2),
        ann=[dict(t="札", d="Bottom reinforcement tears out of bottom of slab", dc=J.ALERT, ds=26)],
    ),

    # ── c614 ★決め所「下端筋が、下から抜けていく」──────────
    "c614": dict(
        t="切れた、ではなく、抜けた",
        s="p139 の札",
        fig=("quote", dict(
            phrase="下端筋が、下から抜けていく",
            rows=[("誰が", "NIST（進行の機構の線図）", J.INST),
                  ("いつ", "2026年6月22日 公表", J.LINE),
                  ("どこに", "技術的知見 スライド139", J.DOC)],
            ctx="原文 Bottom reinforcement tears out of bottom of slab",
            paper=True)),
    ),

    # ── c615 抜けるということ ────────────────
    "c615": dict(
        t="埋まっていた鉄筋が、引き出された",
        s="抜けるということ",
        fig=("beforeafter", dict(
            a=dict(k="切れる", t="鉄筋そのものが破断", lines=["NIST の書き方ではない"], c=J.LINE),
            b=dict(k="抜ける", t="コンクリートから引き出される", lines=["tears out（p139）"], c=J.ALERT))),
    ),

    # ── c616 鉄筋の定着 ────────────────────
    "c616": dict(
        t="埋まりが足りなければ、そのまま抜ける",
        s="鉄筋の定着（模式）",
        fig=("layers", dict(
            n=2, labels=["コンクリート", "鉄筋が埋まっている長さ"], fiber=False,
            bonds=[dict(i=1, t="定着（埋まり）", c=J.AMBER)],
            note="模式図。埋まりが足りないと、引かれたときに抜ける（寸法は書いていない）")),
    ),

    # ── c617 進む向きの矢印 ─────────────────
    "c617": dict(
        t="抜けたところで、止まらない",
        s="進む向きの矢印（p139）",
        photo=ss.P139, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P139, 0.55, 0.50, 1.5),
        ann=[dict(t="支えていた重さ", d="隣のつなぎ目へ移る", dc=J.ALERT, ds=32)],
    ),

    # ── c618 隣へ、また隣へ ────────────────
    "c618": dict(
        t="壊れ方が、隣で繰り返される",
        s="隣へ、また隣へ（p139）",
        fig=("process", dict(
            steps=[dict(t="つなぎ目 1", d="抜ける", c=J.ALERT),
                   dict(t="重さが移る", d="隣のつなぎ目へ", c=J.AMBER),
                   dict(t="つなぎ目 2", d="同じ設計・同じ施工", c=J.LINE),
                   dict(t="同じように", d="抜ける", c=J.ALERT)])),
    ),

    # ── c619 連鎖 ────────────────────────
    "c619": dict(
        t="壊れるたびに、残った柱の重さが増える",
        s="連鎖ということ",
        fig=("panel", dict(
            lead="ひとつ壊れると",
            blocks=[dict(k="次", t="隣のつなぎ目が壊れる", c=J.ALERT),
                    dict(k="増", t="残った柱にかかる重さが増える", c=J.ALERT)],
            cols=2)),
    ),

    # ── c620 崩落範囲の平面図 ───────────────
    "c620": dict(
        t="青いところが、崩れた範囲",
        s="崩落範囲の平面図（p133・左）",
        photo=ss.P133, side="right", ann_y=330, color=0.6,
        **ss.focus(ss.P133, 0.55, 0.40, 1.0),
        ann=[dict(t="Extent of Collapse", d="中央部の崩れた範囲", dc=J.ALERT, ds=30)],
    ),

    # ── c621 ZoneA と ZoneB ─────────────────
    "c621": dict(
        t="範囲は、2つに分けられている",
        s="Zone A と Zone B（p133）",
        photo=ss.P133, side="right", ann_y=330, color=0.6,
        **ss.focus(ss.P133, 0.58, 0.40, 1.5),
        ann=[dict(t="Zone A", d="ゾーンA", dc=J.OK, ds=32),
             dict(t="Zone B", d="ゾーンB", dc=J.LINE, ds=32)],
    ),

    # ── c622 ZoneA＝壁 ─────────────────────
    "c622": dict(
        t="Aは壁、Bは床と柱",
        s="2つのゾーンの違い（p133）",
        photo=ss.P133, side="left", ann_y=330, color=0.6,
        **ss.focus(ss.P133, 0.55, 0.62, 1.9),
        ann=[dict(t="Zone A", d="Concrete Wall＝コンクリートの壁があった側", dc=J.OK, ds=28),
             dict(t="Zone B", d="Slabs & Columns＝床と柱だけの側", dc=J.LINE, ds=28)],
    ),

    # ── c623 壁と柱の違い ──────────────────
    "c623": dict(
        t="壁と柱では、力の逃げ道が違う",
        s="壁と柱の違い",
        fig=("beforeafter", dict(
            a=dict(k="壁", t="面で支える", lines=["力の逃げ道が多い"], c=J.OK),
            b=dict(k="柱", t="点で支える", lines=["逃げ道が少ない"], c=J.ALERT))),
    ),

    # ── c624 境目の形（平面図側） ────────────────
    "c624": dict(
        t="境目の形に、その差が出ている",
        s="Zone A と Zone B の境目（p133・平面図）",
        photo=ss.P133, side="left", ann_y=330, color=0.6,
        **ss.focus(ss.P133, 0.60, 0.36, 2.2),
        ann=[dict(t="壁のあった側", d="まっすぐに切れる", dc=J.OK, ds=30),
             dict(t="柱だけの側", d="段になって出入りする", dc=J.ALERT, ds=30)],
    ),

    # ── c625 中央部と東側 ─────────────────
    "c625": dict(
        t="破壊は、塔のなかをどう広がったか",
        s="NIST 第4章の見出し（p29）",
        photo=ss.P029, side="left", ann_y=330, color=0.35,
        **ss.focus(ss.P029, 0.60, 0.40, 1.35),
        ann=[dict(t="Middle Part", d="中央部（崩落）", dc=J.ALERT, ds=30),
             dict(t="East Part", d="東側（崩落）", dc=J.ALERT, ds=30),
             dict(t="West Part", d="西側（残って解体）", dc=J.LINE, ds=30)],
    ),

    # ── c626 中央から東へ ──────────────────
    "c626": dict(
        t="まず中央部、そのあとで東側",
        s="section 4 の要約（NIST ニュース 2026年6月22日）",
        fig=("process", dict(
            steps=[dict(t="プールデッキ", d="外れる", c=J.AMBER),
                   dict(t="塔のつなぎ目", d="2つが傷つく", c=J.ALERT),
                   dict(t="中央部", d="破壊が通る", c=J.ALERT),
                   dict(t="東側", d="そのあと進む", c=J.ALERT)])),
    ),

    # ── c627 分けられていなかったもの ─────────────
    "c627": dict(
        t="そこで止まる区切りが、無かった",
        s="この建物に無かったもの",
        fig=("absent", dict(
            mode="single", lead="壊れをそこで止める仕組み",
            items=[dict(t="区切り（縁切り）", d="この建物には無かった", ok=False, c=J.ALERT)],
            note="推論の根拠＝NIST の進行の線図（p139）と平面図（p133）")),
    ),

    # ── c628 残った棟の断面 ───────────────────
    "c628": dict(
        t="刃物で切ったように、まっすぐ",
        s="残った棟の断面（NIST 記録映像）",
        photo=ss.fb("c628"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="床が切れているのは", d="柱のあるところ＝線図と同じ", dc=J.ALERT, ds=30)],
    ),

    # ── c629 章の閉じ ────────────────────
    "c629": dict(
        t="24通りのうち、最後に残った1つ",
        s="章の閉じ（p133）",
        photo=ss.P133, side="left", ann_y=330, color=0.6,
        **ss.focus(ss.P133, 0.52, 0.50, 1.2),
        ann=[dict(t="検討された筋書き", v="24", vc=J.LINE, vs=110),
             dict(t="残ったもの", v="1", vc=J.ALERT, vs=110)],
    ),
}
