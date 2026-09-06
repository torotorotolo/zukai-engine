# -*- coding: utf-8 -*-
"""第4章 図面と、実物 c401–c434（34カット）。

■ この章の役目
  **追うのは、かぶり厚さの ¾インチと2インチ。設計と施工の2つだけを扱う。**
  決め所は c412「図面は¾インチ、実物は2インチ」と c426「4本のはずが、2本だった」。

■ 出どころ
  技術的知見 p16・p75・p76（写真は NIST、図面は Town of Surfside 提供と明記）・p86／
  B-Roll #2・#3・#4・#5／NIST 更新 2021-07（警察の護衛）。
  🔴 p16 の赤黄の点は**色に意味がある**ので `color=` で原色を残す（build_jiko.tone）。
"""
import jiko_style as J
import cuts.ss as ss

SPEC = {

    # ── c401 原因の5つの箱 ─────────────────────────
    "c401": dict(
        t="5つの理由を、同じ重さでは扱わない",
        s="つなぎ目が壊れた原因と要因（p86）",
        photo=ss.P086, panel=True, pw=1500,
    ),

    # ── c402 左2つの波括弧 ────────────────────────
    "c402": dict(
        t="括弧に入るのは、左の2つ",
        s="p86 の下の波括弧",
        photo=ss.P086, side="right", ann_y=330,
        # 🔴 2026-09-06（⑤c' 直す #2）：D-02：注記が括弧の外の箱3に載り、左端で英文が語の途中で切れていた
        #    切り方は `check_slide.py` の粗の数がいちばん少ない値を総当たりで探した
        xbias=0.35, bias=0.575, zoom=2.15,
        ann=[dict(t="括弧の中", d="左の2つだけ", dc=J.ALERT, ds=34)],
    ),

    # ── c403 左の2つ ────────────────────────────
    "c403": dict(
        t="設計の不足と、施工の逸脱",
        s="括弧の中の2つ（p86）",
        fig=("panel", dict(
            lead="括弧でくくられた2つ",
            blocks=[dict(k="1", t="設計の耐力不足（Design understrength）", c=J.ALERT),
                    dict(k="2", t="施工の逸脱（Deviations in as-built construction）", c=J.ALERT)],
            cols=2)),
    ),

    # ── c404 NIST の問い ────────────────────────
    "c404": dict(
        t="なぜ、40年たったその日に",
        s="NIST の問い（p16）",
        photo=ss.P016_Q, band=True, side="right",
        ann=[dict(t="問い", d="建設完了から40年後の2021年6月24日に、なぜ崩れたのか",
                  dc=J.INK_W, ds=34)],
    ),

    # ── c405 赤と黄の点の地図 ────────────────────
    "c405": dict(
        t="答えの片方が、この地図",
        s="プールデッキと街路駐車場の床の地図（p16）",
        photo=ss.P016_MAP, side="right", ann_y=330, color=0.7,
        **ss.focus(ss.P016_MAP, 0.42, 0.45, 1.05),
        ann=[dict(t="床を上から見た図", d="印＝基準を満たしていなかった場所", dc=J.LINE, ds=30)],
    ),

    # ── c406 凡例 ────────────────────────────
    "c406": dict(
        t="赤は重い不足、黄は中くらい",
        s="凡例（p16）",
        # 🔴 2026-09-06（D-04）：凡例は `tf_p016_legend.jpg` に切り出した。
        #    地図（c405）と同じファイルを寄り違いで使っていたので、
        #    c405 の右下に凡例が、c406 の裏に地図のキャプションが透けていた（D-07）
        photo=ss.P016_LEGEND, side="left", ann_y=330, color=0.7,
        **ss.focus(ss.P016_LEGEND, 0.5, 0.5, 1.0),
        ann=[dict(t="severe", d="赤＝重い不足", dc=J.ALERT, ds=34),
             dict(t="moderate", d="黄＝中くらいの不足", dc=J.AMBER, ds=34)],
    ),

    # ── c407 印の多さ ────────────────────────
    # 🔴 数えられる絵は数を合わせる：p16 の地図の印を色で機械的に数えた（下の note の数）。
    "c407": dict(
        t="印は、床のほぼ全体に",
        s="印の数（p16 の地図を機械で数えた）",
        fig=("icons", dict(
            n=ss.P016_DOTS_RED + ss.P016_DOTS_YEL, on=ss.P016_DOTS_RED, kind="dot",
            cols=12, oncol=J.ALERT, offcol=J.AMBER,
            lead="基準を満たしていなかった場所の印",
            note=f"赤（重い不足）{ss.P016_DOTS_RED}か所・黄（中くらい）{ss.P016_DOTS_YEL}か所"
                 "　※ 地図の色の塊を機械で数えた値。重なった印は1つに数えている")),
    ),

    # ── c408 この図の意味 ───────────────────────
    "c408": dict(
        t="弱さは、床の全体にあった",
        s="この図の意味",
        fig=("absent", dict(
            mode="pair", lead="弱いつなぎ目は",
            items=[dict(t="たまたま1つ", d="ではない", ok=False, c=J.LINE),
                   dict(t="広い範囲で足りない", d="建てた時点から", ok=True, c=J.ALERT)],
            note="原文 pervasive（広範）")),
    ),

    # ── c409 スラブ断面の実物 ───────────────────
    "c409": dict(
        t="計算ではなく、実物",
        s="回収されたスラブの断面（p75）",
        photo=ss.P075, side="right", ann_y=330, color=0.5,
        # 2026-09-06（6）G-10：見出し「As-Built Conditions」が左端で 165px 欠けていた（k=1）。
        #   xbias を下げると寄りのぶん右の札「2 in. cover as built」が右端で切れるので、zoom も少し戻す
        xbias=0.05, bias=0.883, zoom=1.08,
        # 2026-09-06（6）G-09：注記が画面の見出し「As-Built Conditions」の写しだった
        ann=[dict(t="実際に建った状態", d="回収されたスラブの現物", dc=J.LINE, ds=30)],
    ),

    # ── c410 黄色い線＝鉄筋の深さ ──────────────────
    "c410": dict(
        t="上の線が図面、下の線が実物",
        s="黄色い2本の線（p75）",
        photo=ss.P075, side="left", ann_y=330, color=0.7,
        **ss.focus(ss.P075, 0.45, 0.30, 2.0),
        ann=[dict(t="上の線", d="図面どおりなら鉄筋がある深さ", dc=J.AMBER, ds=30),
             dict(t="下の線", d="実際に鉄筋があった深さ", dc=J.ALERT, ds=30)],
    ),

    # ── c411 かぶりとは ────────────────────────
    "c411": dict(
        t="かぶりは、錆から守る厚み",
        s="用語",
        fig=("panel", dict(
            lead="かぶり（cover）",
            blocks=[dict(k="何", t="鉄筋の上のコンクリート層の厚さ", c=J.INK_W),
                    dict(k="役目", t="錆を防ぐ。意図した厚み", c=J.LINE)],
            cols=2)),
    ),

    # ── c412 ★決め所「図面は¾インチ、実物は2インチ」──────────
    "c412": dict(
        t="図面の値と実物とで、違っていた",
        s="かぶりの2つの札（p75）",
        fig=("quote", dict(
            phrase="図面は¾インチ、実物は2インチ",
            rows=[("誰が", "NIST（回収した床の断面の実測）", J.INST),
                  ("いつ", "2026年6月22日 公表", J.LINE),
                  ("どこに", "技術的知見 スライド75", J.DOC)],
            ctx="原文 ¾ in. cover as shown on design drawings ／ 2 in. cover as built",
            paper=True)),
    ),

    # ── c413 ¾インチと2インチ ─────────────────────
    "c413": dict(
        t="3.2センチ、実物のほうが厚い",
        s="かぶりの厚み",
        fig=("compare", dict(
            items=[dict(v=1.9, t="図面", disp="1.9", unit="cm", sub="¾インチ", c=J.AMBER),
                   dict(v=5.1, t="実物", disp="5.1", unit="cm", sub="2インチ", c=J.ALERT)],
            note="※ どちらも NIST の札の値（p75）。差は 3.2cm")),
    ),

    # ── c414 厚いほうが良さそうに見える ────────────────
    "c414": dict(
        t="厚いほうが良い、とは限らない",
        s="厚いかぶりは、良いことか",
        fig=("panel", dict(
            lead="かぶりが厚いと",
            blocks=[dict(k="○", t="錆に対しては、有利", c=J.OK),
                    dict(k="？", t="ところが、押し抜きに対しては…", c=J.ALERT)],
            cols=2)),
    ),

    # ── c415 スラブ断面・鉄筋の深さ ─────────────────
    "c415": dict(
        t="かぶりが厚いぶん、鉄筋が下がる",
        s="スラブの断面（模式）",
        fig=("layers", dict(
            n=2, labels=["かぶり（上の鉄筋まで）", "鉄筋から板の下面まで"],
            bonds=[dict(i=1, t="上の鉄筋", c=J.AMBER)], fiber=False,
            note="板の厚みは同じ。かぶりが厚いほど、下の層が薄くなる（模式図・寸法は書いていない）")),
    ),

    # ── c416 設計の鉄筋位置と実物 ───────────────────
    "c416": dict(
        t="板は同じ。鉄筋だけが沈む",
        s="設計と実物（p75）",
        fig=("beforeafter", dict(
            a=dict(k="設計", t="かぶり ¾インチ", lines=["鉄筋から下面まで、長い"], c=J.AMBER),
            b=dict(k="実物", t="かぶり 2インチ", lines=["鉄筋から下面まで、短い"], c=J.ALERT),
            note="厚み同一・鉄筋の深さだけ違う（p75）")),
    ),

    # ── c417 有効せい ───────────────────────
    "c417": dict(
        t="この距離が、耐える力を決める",
        s="用語・2つめ",
        fig=("panel", dict(
            lead="有効せい（有効高さ）",
            blocks=[dict(k="何", t="鉄筋から、板の下面までの距離", c=J.INK_W),
                    dict(k="効き", t="縮むほど、耐える力が落ちる", c=J.ALERT)],
            cols=2)),
    ),

    # ── c418 有効な厚みの目減り ────────────────────
    "c418": dict(
        t="厚さは同じで、構造は薄い床",
        s="有効な厚みの目減り",
        fig=("compare", dict(
            items=[dict(v=0, t="板の厚み", disp="±0", unit="", sub="変わらない", c=J.LINE),
                   dict(v=-3.2, t="有効せい", disp="−3.2", unit="cm", sub="かぶりの差のぶん",
                        c=J.ALERT)],
            bar=False, note="※ 3.2cm＝2インチ − ¾インチ（p75）")),
    ),

    # ── c419 実物を測って出た数字 ───────────────────
    "c419": dict(
        t="机の上でなく、測って出た数字",
        s="証拠倉庫の実物部材（NIST 記録映像）",
        # ⚠️ D-11：side="right" だと注記が右の人物（マスク・眼鏡）のベストの上に載り、
        #    部材でなく人を指して見えた。左は奥の棚で無地に近い
        photo=ss.fb("c419"), bias=0.5, side="left", ann_y=360,
        ann=[dict(t="回収した部材", d="実際に測る", dc=J.LINE, ds=34)],
    ),

    # ── c420 設計図の抜粋 ───────────────────────
    "c420": dict(
        t="設計図に、手書きの注記",
        s="当時の設計図の抜粋（p76・図面は Town of Surfside 提供）",
        photo=ss.P076, side="right", ann_y=330, color=0.4,
        # 🔴 2026-09-06（⑤c' 直す #2）：D-12：p76 を抜き直したので、図面と赤枠が枠に入る値へ
        xbias=0.0, bias=0.0, zoom=1.6,
        # 2026-09-06（6）G-09：注記が画面の「From design drawings」の写しだった
        ann=[dict(t="設計図から起こした", d="図面は町（Town）の保管分", dc=J.DOC, ds=30),
             dict(t="赤枠", d="手書きの注記", dc=J.ALERT, ds=30)],
    ),

    # ── c421 赤枠の注記 ────────────────────────
    "c421": dict(
        t="25%以上を、柱の真上に集めよ",
        s="赤枠の注記（p76）",
        photo=ss.P076, side="left", ann_y=330, color=0.5,
        # 🔴 2026-09-06（⑤c' 直す #2）：D-13：赤枠（原画 x 125〜1364・y 234〜343）が枠外だった。c420 と寄りで分ける
        xbias=0.0, bias=0.0, zoom=2.0,
                # 2026-09-06（6）G-14：注記が焼き込みの英文の上に載っていた。dy で逃がす（枠外にならないことは check_layout の実測箱で確認）
        ann=[dict(t="注記", dy=120, d="AT LEAST 25% OF ALL COLUMN STRIP REINF.", dc=J.INK_W, ds=26),
             dict(t="", d="SHALL BE CENTERED OVER THE COLUMN", dc=J.INK_W, ds=26)],
    ),

    # ── c422 注記の意味 ───────────────────────
    "c422": dict(
        t="効くのは、柱の真上を通る鉄筋",
        s="この注記の意味",
        fig=("panel", dict(
            lead="設計者がわざわざ書いた理由",
            blocks=[dict(k="効く", t="柱の真上の鉄筋", c=J.OK),
                    dict(k="だから", t="そこに集めろ、と注記した", c=J.LINE)],
            cols=2)),
    ),

    # ── c423 実物の柱標本 ───────────────────────
    "c423": dict(
        t="では、実物はどうだったか",
        s="回収された柱の標本（p76）",
        photo=ss.P076, side="right", ann_y=330, color=0.4,
        # 🔴 2026-09-06（⑤c' 直す #2）：D-14：柱標本の写真（原画 x 480〜970・y 950〜1350）が枠外だった
        # 2026-09-06（6）G-10：札「2 slab top / reinforcement」が左端で 25/175px 欠けていた（k=1）
        xbias=0.07, bias=0.9, zoom=1.8,
        # 2026-09-06（6）G-09：注記が画面の「Example column specimen」の写しだった
                # 2026-09-06（6）G-14：注記が焼き込みの英文の上に載っていた。dy で逃がす（枠外にならないことは check_layout の実測箱で確認）
        ann=[dict(t="柱の試験体", dy=40, d="床の断面が付いたまま残っていた", dc=J.LINE, ds=30)],
    ),

    # ── c424 2本の矢印 ────────────────────────
    "c424": dict(
        t="残っていた上端の鉄筋を、数えた",
        s="標本を指す2本の矢印（p76）",
        photo=ss.P076, side="left", ann_y=330, color=0.4,
        # 🔴 2026-09-06（⑤c' 直す #2）：D-15：札「2 slab top reinforcement bars」2つ（原画 x 144〜1492）が枠外だった
        xbias=0.0, bias=1.0, zoom=1.6,
        # 2026-09-06（6）G-09：d が画面の札「2 slab top reinforcement bars」の写しだった
        ann=[dict(t="矢印", d="上端の鉄筋2本を指している", dc=J.ALERT, ds=30)],
    ),

    # ── c425 4本と2本 ─────────────────────────
    "c425": dict(
        t="あるべき4本のうち、2本",
        s="数えた本数（p76）",
        fig=("icons", dict(
            n=4, on=[0, 1], kind="dot", cols=4, oncol=J.ALERT, offcol=J.LINE_DIM,
            lead="柱の真上を通る上端筋（片方向）",
            labels=["有", "有", "無", "無"],
            note="塗り＝数えて出てきた本数（2）。薄い＝あるべき本数との差（p76）")),
    ),

    # ── c426 ★決め所「4本のはずが、2本だった」────────────
    "c426": dict(
        t="縦横どちらの向きでも、同じ",
        s="p76 の説明文",
        fig=("quote", dict(
            phrase="4本のはずが、2本だった",
            rows=[("誰が", "NIST（回収した柱の標本を数えた）", J.INST),
                  ("いつ", "2026年6月22日 公表", J.LINE),
                  ("どこに", "技術的知見 スライド76", J.DOC)],
            ctx="原文 only 2 rather than 4 top bars were centered over the column in each direction",
            paper=True)),
    ),

    # ── c427 半分 ──────────────────────────
    "c427": dict(
        t="いちばん効く場所の鉄筋が、半分",
        s="半分ということ",
        fig=("compare", dict(
            items=[dict(v=4, t="あるべき本数", disp="4", unit="本", c=J.LINE),
                   dict(v=2, t="実物", disp="2", unit="本", sub="柱の真上を通る鉄筋", c=J.ALERT)],
            note="※ 片方向あたり（p76）")),
    ),

    # ── c428 NIST の書き方は慎重 ───────────────────
    "c428": dict(
        t="言い切りを、避けている",
        s="NIST の書き方（p76）",
        photo=ss.P076, side="left", ann_y=330, color=0.4,
        # 🔴 2026-09-06（⑤c' 直す #2）：D-16：引用「At this location, only 2 rather than 4…」が枠外だった
        xbias=0.4, bias=0.925, zoom=2.2,
        # 2026-09-06（6）G-09：d が画面の引用の写しだった。書き方のどこが慎重かを言う
        ann=[dict(t="原文の言い方", d="「この場所では」と、場所を限っている", dc=J.INK_W, ds=32),
             dict(t="", d="断りが、はっきり付いている", dc=J.LINE, ds=30)],
    ),

    # ── c429 一般化しない ───────────────────────
    "c429": dict(
        t="書いてあるのは「通例だった」まで",
        s="一般化しない（p76）",
        fig=("absent", dict(
            mode="pair", lead="NIST が書いたこと・書いていないこと",
            items=[dict(t="建物じゅうがそうだった", d="書いていない", ok=False, c=J.LINE),
                   dict(t="プールデッキでは通例", d="指定より少ない本数", ok=True, c=J.ALERT)],
            note="原文 Typically, fewer than the specified number …")),
    ),

    # ── c430 証拠として取っておいた ──────────────────
    "c430": dict(
        t="捨てずに、証拠として取っておいた",
        s="倉庫に並ぶ部材（NIST 記録映像）",
        photo=ss.fb("c430"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="崩れた部材", d="倉庫に並べて保管", dc=J.LINE, ds=32)],
    ),

    # ── c431 梱包・搬送・護衛 ───────────────────────
    "c431": dict(
        t="番号をふり、記録し、倉庫へ",
        s="部材の搬送（NIST 記録映像）",
        photo=ss.fb("c431"), bias=0.5, side="right", ann_y=360,
        ann=[dict(t="運ぶとき", d="警察の護衛（NIST 更新 2021年7月）", dc=J.INST, ds=30)],
    ),

    # ── c432 左2つ・再掲 ────────────────────────
    "c432": dict(
        t="設計が足りず、施工はさらに外れた",
        s="括弧の中の2つ・再掲（p86）",
        photo=ss.P086, side="left", ann_y=330,
        # 🔴 2026-09-06（⑤c' 直す #2）：D-19：注記が箱1の英文の上に載り、箱2の1行目が見出しの裏だった
        #    切り方は `check_slide.py` の粗の数がいちばん少ない値を総当たりで探した
        xbias=0.0, bias=0.55, zoom=2.05,
        ann=[dict(t="1", d="設計の耐力不足", dc=J.ALERT, ds=32),
             dict(t="2", d="施工の逸脱", dc=J.ALERT, ds=32)],
    ),

    # ── c433 括弧の外 ────────────────────────
    "c433": dict(
        t="括弧の外は、重さと時間",
        s="残る3つ（p86）",
        photo=ss.P086, side="left", ann_y=330,
        **ss.focus(ss.P086, 0.74, 0.60, 2.0),
                # 2026-09-06（6）G-14：注記が焼き込みの英文の上に載っていた。dy で逃がす（枠外にならないことは check_layout の実測箱で確認）
        ann=[dict(t="あとから足された", dy=80, d="重さ", dc=J.AMBER, ds=34),
             dict(t="そして", d="時間", dc=J.AMBER, ds=34)],
    ),

    # ── c434 40年立っていた（空撮）─────────────────
    "c434": dict(
        t="この状態で、40年立っていた",
        s="海岸線の空撮（NIST 記録映像）",
        photo=ss.fb("c434"), bias=0.4, side="right", ann_y=360,
        ann=[dict(t="竣工", v="1981", vc=J.INK_W, vs=88),
             dict(t="崩落", v="2021", vc=J.ALERT, vs=88),
             dict(t="", d="では、最後の3週間は？", dc=J.LINE, ds=30)],
    ),
}
