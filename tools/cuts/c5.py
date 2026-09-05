# -*- coding: utf-8 -*-
"""第5章 上に載せたもの c501–c528（28カット）。

■ この章の役目
  **追うのは、25年以上進んでいた鉄筋の腐食と、床の上に足されたもの。**
  決め所は c515「25年以上、進み続けていた」。

■ 出どころ
  技術的知見 p29・p65・p75・p84・p86・p174・p191／B-Roll #2・#5・#6・#7。
  ⚠️ p86 のプランターの箱は `near north side of pool`、p191 は `pool deck`（c503 は結びの p191 に寄せた）。
  ⚠️ c506「二割から三割」は土の一般値で出典なし（台本 §0-5）。図の note に「一般値」と書く。
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── c501 括弧の外の3つ ───────────────────────
    "c501": dict(
        t="括弧の外の3つを、順に",
        s="プランター・盛土と舗装・時間による劣化（p86）",
        photo=ss.P086, side="right", ann_y=330,
        **ss.focus(ss.P086, 0.55, 0.62, 1.2),
        ann=[dict(t="3", d="プランター", dc=J.AMBER, ds=32),
             dict(t="4", d="盛土と舗装", dc=J.AMBER, ds=32),
             dict(t="5", d="時間による劣化", dc=J.AMBER, ds=32)],
    ),

    # ── c502 プランター ────────────────────────
    "c502": dict(
        t="ひとつめは、プランター",
        s="プランターの箱（p86）",
        photo=ss.P086, side="left", ann_y=330,
        **ss.focus(ss.P086, 0.50, 0.62, 2.6),
        ann=[dict(t="Heavier, more extensive planters", d="植木を植えるコンクリートの箱", dc=J.LINE,
                  ds=28)],
    ),

    # ── c503 プールデッキの北側 ───────────────────
    "c503": dict(
        t="より重く、より広く",
        s="プールデッキ上の配置（p29）",
        photo=ss.P029, side="right", ann_y=330, color=0.35,
        **ss.focus(ss.P029, 0.50, 0.68, 1.6),
        ann=[dict(t="場所", d="near north side of pool deck", dc=J.ALERT, ds=32),
             dict(t="出典", d="p191 の書き方に寄せた（p86 は north side of pool）", dc=J.TICK, ds=24)],
    ),

    # ── c504 北側という指定 ───────────────────────
    "c504": dict(
        t="北側は、建物本体に接する側",
        s="北側という指定（p86）",
        fig=("panel", dict(
            lead="プールデッキの北側",
            blocks=[dict(k="北", t="建物本体（塔）に接している側", c=J.INK_W),
                    dict(k="同じ", t="3週間前にプランターが割れていた場所（K-13.1）", c=J.ALERT)],
            cols=2)),
    ),

    # ── c505 重さは増えていく ───────────────────────
    "c505": dict(
        t="載る重さは、年ごとに増える",
        s="デッキの床面（NIST 記録映像）",
        photo=ss.fb("c505"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="プランターに入るもの", d="土・水・育つ植木", dc=J.LINE, ds=32)],
    ),

    # ── c506 土と水の重さ ────────────────────────
    "c506": dict(
        t="同じ体積でも、水を含むと重い",
        s="土の重さ（一般値・出典なし）",
        fig=("compare", dict(
            items=[dict(v=100, t="乾いた土", disp="×1.0", unit="", c=J.LINE),
                   dict(v=125, t="水を含んだ土", disp="×1.2〜1.3", unit="", sub="二割から三割",
                        c=J.ALERT)],
            note="※ 土の一般的な目安。NIST の値ではない")),
    ),

    # ── c507 盛土と舗装 ────────────────────────
    "c507": dict(
        t="ふたつめは、盛土と舗装",
        s="盛土と舗装の箱（p86）",
        photo=ss.P086, side="left", ann_y=330,
        **ss.focus(ss.P086, 0.70, 0.62, 2.6),
        ann=[dict(t="Added fill and paving", d="（variable＝ばらつきがある）", dc=J.LINE, ds=30)],
    ),

    # ── c508 舗装が重ねられる理由 ───────────────────
    "c508": dict(
        t="剥がすより、重ねるほうが安い",
        s="屋外の床の直し方",
        fig=("absent", dict(
            mode="pair", lead="傷んだ床を直すとき",
            items=[dict(t="剥がして貼り直す", d="高く、時間がかかる", ok=False, c=J.LINE),
                   dict(t="上から重ねる", d="安く、早い", ok=True, c=J.AMBER)],
            note="一般的な事情。この建物の工事記録ではない")),
    ),

    # ── c509 重ねられた舗装の断面 ──────────────────
    "c509": dict(
        t="重ねるたびに、重さが増える",
        s="重ねられた舗装の断面（模式）",
        fig=("layers", dict(
            n=4, labels=["舗装（新しい）", "舗装（古い）", "盛土", "スラブ"], fiber=False,
            bonds=[dict(i=3, t="あとから足された重さ", c=J.AMBER)],
            note="模式図。どれだけ増えたかは場所によってばらばら（p86 の variable）")),
    ),

    # ── c510 設計時に見込まれていた重さ ──────────────
    "c510": dict(
        t="見込みは、建てるときに決まる",
        s="設計時の想定",
        fig=("absent", dict(
            mode="pair", lead="荷重の見込み（設計）と、その後",
            items=[dict(t="設計で見込んだ重さ", d="あらかじめ決まっている", ok=True, c=J.LINE),
                   dict(t="あとから足された重さ", d="見込みの外", ok=False, c=J.ALERT)])),
    ),

    # ── c511 時間・鉄筋の標本 ───────────────────────
    "c511": dict(
        t="みっつめは、時間",
        s="腐食した鉄筋の標本（p174）",
        photo=ss.P174, side="left", ann_y=330, color=0.4,
        **ss.focus(ss.P174, 0.70, 0.55, 1.3),
        ann=[dict(t="Corrosion of Reinforcement", d="NIST は別の節を立てている", dc=J.INST, ds=30)],
    ),

    # ── c512 見出し ────────────────────────────
    "c512": dict(
        t="見出しは、鉄筋の腐食",
        s="p174 の見出しと箇条",
        photo=ss.P174, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P174, 0.25, 0.32, 1.8),
        ann=[dict(t="Most likely source", d="長期の劣化の最有力", dc=J.ALERT, ds=28)],
    ),

    # ── c513 鉄筋は錆びると体積が増える ──────────────
    "c513": dict(
        t="錆びると、体積が増える",
        s="鉄筋の標本（NIST 記録映像）",
        photo=ss.fb("c513"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="膨らんだ鉄筋", d="内側からコンクリートを割る", dc=J.ALERT, ds=30)],
    ),

    # ── c514 かぶりが割れる ────────────────────────
    "c514": dict(
        t="剥がれれば、錆はもっと速く",
        s="錆の繰り返し",
        fig=("process", dict(
            steps=[dict(t="鉄筋が膨らむ", d="錆で体積が増える", c=J.ALERT),
                   dict(t="かぶりが割れる", d="剥がれ落ちる", c=J.ALERT),
                   dict(t="さらに濡れる", d="錆が速く進む", c=J.ALERT)],
            note="次のカットで、その年数")),
    ),

    # ── c515 ★決め所「25年以上、進み続けていた」──────────
    "c515": dict(
        t="繰り返しは、四半世紀続いていた",
        s="p174 の箇条",
        fig=("quote", dict(
            phrase="25年以上、進み続けていた",
            rows=[("誰が", "NIST（鉄筋の標本の評価）", J.INST),
                  ("いつ", "2026年6月22日 公表", J.LINE),
                  ("どこに", "技術的知見 スライド174", J.DOC)],
            ctx="原文 Ongoing for more than 25 years",
            paper=True)),
    ),

    # ── c516 1981 → 1996 → 2021 ──────────────────
    "c516": dict(
        t="腐食の始まりは、1996年ごろ",
        s="建物の40年（p174）",
        fig=("timeline", dict(
            t0=1981, t1=2021, title="単位は年",
            ticks=[(1981, "1981"), (1991, "1991"), (2001, "2001"), (2011, "2011"), (2021, "2021")],
            events=[dict(t=1981, top="竣工", c=J.LINE),
                    dict(t=1996, top="1996ごろ", t2="腐食が始まる（25年以上前）", c=J.ALERT, big=True),
                    dict(t=2021, top="崩落", c=J.INK_W)])),
    ),

    # ── c517 残りの25年 ────────────────────────
    "c517": dict(
        t="40年のうち、後ろの25年",
        s="錆び続けていた期間",
        fig=("compare", dict(
            items=[dict(v=40, t="建物が立っていた年数", disp="40", unit="年", c=J.LINE),
                   dict(v=25, t="鉄筋が錆び続けた年数", disp="25", unit="年", sub="以上", c=J.ALERT)],
            note="※ 25年以上＝p174。竣工 1981・崩落 2021")),
    ),

    # ── c518 数百本 ────────────────────────────
    "c518": dict(
        t="標本は、数百本の単位",
        s="p174 の箇条",
        photo=ss.P174, side="right", ann_y=330, color=0.4,
        **ss.focus(ss.P174, 0.25, 0.50, 1.8),
        ann=[dict(t="hundreds of samples", d="鉄筋の標本＝数百本", dc=J.INK_W, ds=30)],
    ),

    # ── c519 コア抜き ────────────────────────
    "c519": dict(
        t="円柱の形に、抜き取る",
        s="コア抜き（NIST 記録映像）",
        photo=ss.fb("c519"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="コア抜き", d="現場のコンクリートを円柱で抜く", dc=J.LINE, ds=32)],
    ),

    # ── c520 コアの試験 ────────────────────────
    "c520": dict(
        t="割れるまで、押しつぶす",
        s="コアの圧縮試験（NIST 記録映像）",
        photo=ss.fb("c520"), bias=0.5, side="left", ann_y=360,
        ann=[dict(t="測るもの", d="どれだけの力で割れたか＝コンクリートの強さ", dc=J.LINE, ds=28)],
    ),

    # ── c521 倉庫の床一面 ───────────────────────
    "c521": dict(
        t="崩れた建物が、そのままの形で並ぶ",
        s="倉庫の床一面の部材（NIST 記録映像）",
        photo=ss.fb("c521"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="試験に回された部材", d="倉庫の床を埋めつくす", dc=J.LINE, ds=32)],
    ),

    # ── c522 塩水と電極の試験 ──────────────────────
    "c522": dict(
        t="塩水に浸し、電気を流す",
        s="腐食の試験（p84）",
        photo=ss.P084, side="right", ann_y=330, color=0.35,
        **ss.focus(ss.P084, 0.35, 0.55, 1.1),
        ann=[dict(t="Salt-Water Bath with Electrodes", d="塩水浴＋電極（p84）", dc=J.LINE,
                  ds=28)],
    ),

    # ── c523 なぜ塩水か ────────────────────────
    "c523": dict(
        t="塩は、波でも風でも霧でも来る",
        s="大西洋のすぐそば",
        fig=("icons", dict(
            n=3, on=3, kind="dot", cols=3, oncol=J.LINE,
            lead="塩が運ばれてくる道",
            labels=["波", "風", "霧"],
            note="建物が建っていたのは、海岸のすぐそば（p3 の Beach）")),
    ),

    # ── c524 塩がコンクリートを通る ─────────────────
    "c524": dict(
        t="鉄筋まで届くと、錆が始まる",
        s="塩の進み方（模式）",
        fig=("process", dict(
            steps=[dict(t="表面", d="塩が付く", c=J.LINE),
                   dict(t="コンクリートの中", d="何年もかけて進む", c=J.LINE),
                   dict(t="鉄筋", d="届くと錆が始まる", c=J.ALERT)],
            note="模式図。かかる年数は、かぶりの厚さで変わる")),
    ),

    # ── c525 かぶりと塩の到達 ─────────────────────
    "c525": dict(
        t="かぶりが厚いほど、塩は遅く届く",
        s="第4章のかぶりの話が戻ってくる（p75）",
        fig=("compare", dict(
            items=[dict(v=1.9, t="図面のかぶり", disp="1.9", unit="cm", sub="塩が早く届く", c=J.AMBER),
                   dict(v=5.1, t="実物のかぶり", disp="5.1", unit="cm", sub="塩が届くまで長い", c=J.OK)],
            note="※ 値は p75。錆に対しては、厚いほうが有利")),
    ),

    # ── c526 同じ数字が二度効く ──────────────────
    "c526": dict(
        t="同じ2インチが、逆に効く",
        s="かぶり 2インチの二つの顔",
        fig=("beforeafter", dict(
            a=dict(k="錆に対して", t="有利", lines=["塩が届くまで、時間がかかる"], c=J.OK),
            b=dict(k="押し抜きに対して", t="不利", lines=["有効せいが縮む"], c=J.ALERT),
            note="同じ一つの数字（p75 の 2 in. cover as built）")),
    ),

    # ── c527 5つの箱・全体 ──────────────────────
    "c527": dict(
        t="余裕が、少しずつ削られていった",
        s="5つの箱・全体（p86）",
        photo=ss.P086, side="left", ann_y=330,
        **ss.focus(ss.P086, 0.50, 0.62, 1.45),
        ann=[dict(t="足された", d="重さ", dc=J.AMBER, ds=32),
             dict(t="入った", d="塩", dc=J.AMBER, ds=32),
             dict(t="進んだ", d="時間", dc=J.AMBER, ds=32)],
    ),

    # ── c528 2021年6月のはじめ ──────────────────
    "c528": dict(
        t="2本のつなぎ目が、限界を越えた",
        s="9分前の駐車場3D（p65）",
        photo=ss.P065, side="right", ann_y=330, color=0.45,
        **ss.focus(ss.P065, 0.50, 0.50, 1.35),
        ann=[dict(t="2021年6月のはじめ", d="プールデッキの下の柱、2本", dc=J.ALERT, ds=32)],
    ),
}
