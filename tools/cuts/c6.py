# -*- coding: utf-8 -*-
"""第6章 第五福竜丸 c601–c626（26カット）。12本目（キャッスル・ブラボー）。⑤b-4（2026-09-23）で書いた。

■ 実写 5/26（動く映像3・写真1・報告書の頁1）。章の色＝セピア。爆発の実写は原色（`color=1.0`）。
■ 🔴 動く模式図（drift）＝**冒頭の地図（NEAR）が戻る**：
   c605 夜明け前の船（157キロの1隻。🔴 注で「日本政府の記録の位置では約135キロ」と断る＝`MAP_PTS_JP`・`MAP_REL_JP`）／
   c611 甲板に降りはじめる灰／c616 捜索の飛行機が引き返した所（DNA p220＝爆心から真東へ120キロ）／
   c626 島に降る灰（ロンゲラップとロンゲリックに寄った範囲＝第7章 c702 で同じ地図が戻る）
   ⚠️ 「止まっては進む船」（c610）は地図に描かない＝進んだ距離も向きも報告書に無い（報告書に無い位置を描かない §5b-10）
   ⚠️ 降りはじめの時刻の食い違い（日本「約3時間後」・DNA「1時間半後」）は時計を出さない。c611 は両方の札を並べる
■ 焼津〜マーシャル諸島（3,000キロ超）は drift に載せない：drift は環礁の輪しか描かず、縮尺は緯度11〜12度の帯を
   前提にしている（緯度8〜37度だと東西の縮尺が±10%狂い、`check_drift` の許し5%を超える）→ c601・c621 は位置関係の略図（mapfig）
■ c618 は報告書の実物をなぞる型（DNA p219「The ship proceeded north toward its separate destiny, unobserved by the task force.」）
■ ⚠️ 台本 §7 の c626 = p241（第68図）は**頁の写真の部分が白紙**（PDF の走査に写真が残っていない＝⑤b-4 で頁を見た）→ drift に替えた
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
SRC_DNA = ss.SRC_DNA
NOTE_DNA = "出典：国防原子力局の報告書（1982年）"
NOTE_JP = "出典：日本政府の覚え書き（1954年3月27日・報告書の付録）"
MAP_NOTE_JPN = "模式図：位置関係だけ（縮尺と角度は正確ではない）"


def japan_map(scale, c1, c2, d2):
    """焼津とマーシャル諸島の略図（c601・c621 で同じ図が戻る）。南北・東西の向きだけ合わせる。"""
    return ("mapfig", dict(
        points=[dict(x=0.16, y=0.20, t="焼津港", d="静岡県", c=c1),
                dict(x=0.84, y=0.78, t="マーシャル諸島", d=d2, c=c2)],
        link=(0, 1), scale=scale, note=MAP_NOTE_JPN))


SPEC = {

    # 焼津（北西）とマーシャル諸島（南東）＝向きだけ（台本 c601「南東の海へ」）
    "c601": dict(
        t="焼津から、南の海へ",
        s="マグロ漁への出港",
        fig=japan_map("1月22日に出港", J.LINE, J.AMBER, "南東の海"),
    ),

    # 23人＝点の数を合わせる（§5b-6「数えられる絵は数を合わせる」）
    # ⚠️ 副題を「第五福竜丸」にすると画面の隅の章名と同じ言葉が二度出る（check_dup）
    "c602": dict(
        t="木造の漁船",
        s="漁船のあらまし",
        fig=("icons", dict(
            n=23, on=23, kind="person", cols=12, oncol=J.AMBER,
            lead="乗っていた人　23人",
            note="長さ30メートルほど・木造（日本政府の覚え書き）")),
    ),

    "c603": dict(
        t="縄と釣り針の漁",
        s="はえ縄漁のしくみ",
        fig=("process", dict(
            steps=[dict(t="流す", d="釣り針を下げた長い縄", c=J.LINE),
                   dict(t="巻き上げる", d="時間をおいて", c=J.AMBER),
                   dict(t="マグロ", d="かかった魚をとる", c=J.OK)])),
    ),

    # 日付は日本政府の覚え書き（DNA p476）。t＝1月1日から数えた日
    "c604": dict(
        t="漁場を移しながら",
        s="1954年1月から3月",
        fig=("timeline", dict(
            events=[dict(t=22, top="焼津を出港", t2="1月22日", c=J.LINE),
                    dict(t=34, top="漁の始まり", t2="2月3日", c=J.AMBER),
                    dict(t=54, top="マーシャル諸島の近く", t2="2月23日", c=J.AMBER),
                    dict(t=60, top="ブラボー", t2="3月1日", c=J.ALERT, big=True)],
            t0=18, t1=64,
            ticks=[(32, "2月"), (60, "3月")],
            src=NOTE_JP)),
    ),

    # 🔴 drift（冒頭の地図が戻る）。船は DNA p212 の157キロの1隻。日本政府の位置（約135キロ）は描かずに注で断る
    #    `MAP_PTS_JP`・`MAP_REL_JP` を足す＝門番が「約135キロ」と緯度経度から測った距離を照合する（§5b-38）
    "c605": dict(
        t="夜明け前、海の上で",
        s="3月1日の夜明け前の船",
        fig=("drift", ss.drift_map(
            steps=[dict(ship=dict(at="ship", t="第五福竜丸"),
                        dim=dict(a="bikini", b="ship", t="157キロ", d="東北東")),
                   dict(tag=dict(at="ship", t="止まって漂う", side="below"))],
            pts=ss.MAP_PTS_JP, rel=ss.MAP_REL_JP, src="DNA p212・p477",
            note="模式図：船はビキニから東北東へ157キロ（米国の報告書）。日本政府の記録の位置では約135キロ")),
    ),

    # 4K 16.0〜25.0秒（c502 の続きの秒・水平線の火球）＝c102・c324・c502 と同じ副題
    "c606": dict(
        t="漁船も、光を見た",
        s="艦から見た火球　1954年3月1日",
        **ss.vid("c606"),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="ビキニ環礁から", v="157キロ", vc=J.AMBER),
             dict(t="方角", d="東北東", dc=J.AMBER)],
    ),

    # DOE 26.0〜34.0秒（真っ白→火球＝乗組員が見た「光」）。⚠️ 副題に色の名前を書かない（§5b-24）
    "c607": dict(
        t="色を変える光",
        s="遠くから見た火球　1954年3月1日",
        **ss.vid("c607"),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="見えた方角", d="西南西の空", dc=J.AMBER),
             dict(t="光の色", d="赤→白っぽい黄→赤", dc=J.ALERT)],
    ),

    # DOE 47.0〜53.0秒（輪の雲が広がる・c506 と別の秒）
    "c608": dict(
        t="雲が、空に広がる",
        s="広がる輪の雲　1954年3月1日",
        **ss.vid("c608"),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="光から音まで", v="7、8分", vc=J.AMBER),
             dict(t="音の数", v="2回", vc=J.AMBER)],
    ),

    "c609": dict(
        t="危ない、と考えた",
        s="乗組員が思い出したこと",
        fig=("process", dict(
            steps=[dict(t="光を見る", d="夜明け前", c=J.AMBER),
                   dict(t="原爆の実験かも", d="新聞の記事から", c=J.ALERT),
                   dict(t="縄を引き上げる", d="20分ほどあと", c=J.LINE)])),
    ),

    # ⚠️ 「進んでは止まる」は地図に描かない（報告書に距離も向きも無い）＝札だけ
    "c610": dict(
        t="乗組員の持ち場",
        s="縄の引き上げ",
        fig=("panel", dict(
            blocks=[dict(k="縄", t="機械で巻く", c=J.LINE),
                    dict(k="甲板と操舵室", t="ほぼ全員", c=J.AMBER),
                    dict(k="船の動き", t="進んでは止まる", c=J.TICK)])),
    ),

    # 🔴 drift（同じ地図）。降る灰は点の真上に落ちる＝札は左と下（線の無い側）
    #    日本「約3時間後」・DNA「1時間半後」の両方を札に（どちらかを時計で描かない）
    "c611": dict(
        t="甲板に、灰",
        s="灰の降りはじめ",
        fig=("drift", ss.drift_map(
            steps=[dict(ship=dict(at="ship", t="第五福竜丸"),
                        tag=dict(at="ship", t="日本の記録：約3時間後", side="left"),
                        move=[dict(kind="fall", at="ship")]),
                   dict(tag=dict(at="ship", t="米国の報告書：1時間半後", side="below")),
                   dict()],
            src="DNA p219・p477")),
    ),

    # NARA #23（YAG-40 の甲板を洗う白い服の乗組員）。灰の写真ではない＝副題は写っているものだけ
    # 🔴 ⑤c'（09-23）：見出しで**写真がアメリカの艦だと先に言う**。見出し「雪のような灰」と札1「第五福竜丸」の組で、
    #    米艦の甲板が第五福竜丸の甲板に見えた（⑤c 原寸 p06・台帳 §7-6 A2）。写真は声の2行目（米艦隊にも同じ灰）そのもの＝残す。
    #    札2「同じ灰／アメリカの艦隊にも」は見出しと重なる＝灰のようす（声の2行目の後半）へ言い換えた
    "c612": dict(
        t="アメリカの艦にも、同じ灰",
        s="艦 YAG-40 の甲板を洗う　1954年",
        photo=P("dc_yag40_deck"), **ss.kind(P("dc_yag40_deck")),
        cam="pull",
        side="right", ann_y=330,
        ann=[dict(t="第五福竜丸", d="甲板が一面の灰", dc=J.ALERT),
             dict(t="灰のようす", d="ざらざら・雪のよう", dc=J.TICK)],
    ),

    # 🔴 決め所（DNA p478 の覚え書き「The ashes kept falling until about noon」・時刻は日本の標準時と前書きが断る）
    "c613": dict(
        t="6時間の引き上げ",
        s="3月1日の朝から昼",
        fig=("quote", dict(
            phrase="灰は、日本の時計で昼ごろまで降り続けた",
            who="日本政府",
            to="アメリカ大使",
            when="1954年3月27日",
            doc="外務次官が渡した覚え書き")),
    ),

    # 速さは覚え書き（DNA p478「(7) nautical miles per hr」）。向きは DNA p219「proceeded north」
    "c614": dict(
        t="灰から離れる",
        s="その後の船の進路",
        fig=("process", dict(
            steps=[dict(t="縄を上げ終える", d="およそ6時間", c=J.LINE),
                   dict(t="北へ", d="灰の降らない方", c=J.AMBER),
                   dict(t="時速13キロほど", d="およそ7ノット", c=J.OK)])),
    ),

    # 報告書の第53図（捜索の向きと第五福竜丸の航跡・横長の頁）。下の黒い罫の手前で切る
    "c615": dict(
        t="同じころ、空では",
        s="報告書の第53図　捜索の向きと漁船の航跡",
        # ⑤c'（09-23）：寄りの終わりで図の注の2行目「…Aide Memoire of 27 March 1956).」が窓の下の辺に切られていた＝注「Figure 53.」は副題が名乗るので外す（台帳 §7-4）
        photo=ss.page(211), panel=True, trim=(0.05, 0.13, 0.96, 0.74),
        side="right",
        ann=[dict(t="捜索の飛行機", d="東北東の海へ", dc=J.AMBER),
             dict(t="追加が決まった", d="前の夜", dc=J.TICK)],
    ),

    # 🔴 drift（同じ地図）。引き返した所＝爆心から真東へ120キロ（DNA p220 の「記録のひとつ」）
    #    ⚠️ 札「引き返した」を下に置くとロンゲラップの名札（上）とぶつかる＝環礁の札は全部下（MAP_PLACES_LINE）
    #    ⚠️ 飛行機の道筋は描かない（クェゼリンから来た。爆心から飛んだのではない）＝点と寸法線だけ
    "c616": dict(
        t="船の手前で、引き返す",
        # ⚠️ 副題に「引き返した」を入れると札と同じ語（check_dup）
        s="捜索の飛行機の記録",
        fig=("drift", ss.drift_map(
            # ⚠️ 線の出どころに印が無いと、どこから測った120キロか分からない（試し焼き）＝「爆心」の札（c510 と同じ）
            steps=[dict(dim=dict(a="gz", b="abort", t="120キロ", d="東"),
                        tag=[dict(at="gz", t="爆心", side="above"),
                             dict(at="abort", t="午前9時49分", side="above")]),
                   dict(tag=dict(at="abort", t="引き返した", side="below")),
                   dict(ship=dict(at="ship", t="第五福竜丸"))],
            places=ss.MAP_PLACES_LINE, pts=ss.ABORT_PTS, rel=ss.ABORT_REL, src="DNA p212・p220",
            note="模式図：引き返した所は記録のひとつ（爆心から東へ120キロ）。船はビキニから東北東へ157キロ")),
    ),

    # 委員長の発言（DNA p480 の日本大使館の覚え書きが引く・1954年3月31日）。「〜ようだ」の留保は札に残す
    "c617": dict(
        t="委員長の見方",
        s="1954年3月31日の発言",
        fig=("panel", dict(
            blocks=[dict(k="述べた人", t="原子力委員会の委員長", c=J.INST),
                    dict(k="船について", t="捜索から漏れたらしい", c=J.ALERT)],
            cols=2)),
    ),

    # 🔴 決め所。報告書の実物をなぞる型（DNA p219）。文は2行＝読む順に塗る（§5b-36）
    "c618": dict(
        t="北へ去った漁船",
        s="漁船についての一文",
        fig=("trace", dict(
            page=ss.page(219),
            lines=[(0.5643, 0.7453, 0.8013, 0.7635), (0.1108, 0.7687, 0.6786, 0.7868)],
            phrase="船は、部隊の誰にも気づかれなかった",
            doc=f"{SRC_DNA} 219頁の原文",
            # 切り口は行と行のすきま（「wave passed.」の行から船の名の行まで4行。PDF の文字の層で測った）
            crop=(0.08, 0.7195, 0.92, 0.8115))),
    ),

    # 対比なので矢印を消す。どちらの見方かを書き、答え（第8章 c811・c813）はまだ言わない
    "c619": dict(
        t="内側か、外側か",
        s="危険区域と船の位置",
        fig=("beforeafter", dict(
            a=dict(k="アメリカ側", t="区域の内側？", lines=["のちの委員長の発言"], v="", c=J.ALERT),
            b=dict(k="日本側", t="区域の外側？", lines=["日本政府の覚え書き"], v="", c=J.AMBER),
            arrow=False)),
    ),

    "c620": dict(
        t="警告の形跡",
        s="3月1日の朝",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="船への警告", d="形跡なし", ok=False, c=J.ALERT),
                   dict(t="飛行機の音", d="聞いた人なし", ok=False, c=J.ALERT),
                   dict(t="ほかの船への警告", d="形跡なし", ok=False, c=J.ALERT)],
            lead="日本政府の記録",
            note=NOTE_JP)),
    ),

    # 略図が戻る（c601）。帰り道＝北西へ（DNA p477）
    "c621": dict(
        t="焼津へ、北西へ",
        s="3月2日からの帰り道",
        fig=japan_map("12日かけて", J.AMBER, J.ALERT, "灰を浴びた海"),
    ),

    # 日数は灰を浴びた日から（DNA p478）
    "c622": dict(
        t="体に出た変化",
        s="乗組員の体",
        fig=("timeline", dict(
            events=[dict(t=0, top="灰を浴びる", t2="3月1日", c=J.ALERT),
                    dict(t=2.5, top="頭痛・吐き気", t2="2、3日のうち", c=J.AMBER, big=True)],
            t0=-1, t1=14,
            ticks=[(0, "0"), (7, "7"), (14, "14")],
            title="灰を浴びてからの日数",
            src=NOTE_JP)),
    ),

    # 人の体は描かない＝場所の名前だけ
    "c623": dict(
        t="やけどのような痛み",
        s="灰がついた肌",
        fig=("panel", dict(
            blocks=[dict(k="痛みが出た所", t="首・顔・耳", c=J.ALERT),
                    dict(k="同じく", t="鉢巻きを巻いた所", c=J.ALERT),
                    dict(k="出はじめ", t="7、8日後", c=J.AMBER)])),
    ),

    # c604 の時間軸が戻る（1月22日→3月14日）。t＝1月1日から数えた日
    "c624": dict(
        t="51日の航海",
        s="焼津を出てから戻るまで",
        fig=("timeline", dict(
            events=[dict(t=22, top="出港", t2="1月22日", c=J.LINE),
                    dict(t=60, top="灰を浴びる", t2="3月1日", c=J.ALERT),
                    dict(t=73, top="焼津港に戻る", t2="3月14日　朝6時", c=J.AMBER, big=True)],
            t0=18, t1=77,
            ticks=[(32, "2月"), (60, "3月")],
            band=[dict(a=22, b=73, t="51日", c=J.AMBER)],
            src=NOTE_JP)),
    ),

    # 委員長の言い分（DNA p480）と日本側の答え。対比＝矢印なし
    "c625": dict(
        t="診察をめぐって",
        s="3月の診察",
        fig=("beforeafter", dict(
            a=dict(k="委員長の言い分", t="十分に診察できず", lines=["乗組員の体について"], v="", c=J.ALERT),
            b=dict(k="日本側の答え", t="3月19日・20日", lines=["東京と焼津で診察", "アメリカの機関の医師"], v="", c=J.OK),
            arrow=False)),
    ),

    # 🔴 drift（島に寄った地図＝第7章 c702 で戻る）。人数は WT 1004頁・DNA p223（c402 と同じ値）
    #    降る灰の柱の上に札を置かない＝降る島の札は左・降らない島（ロンゲリック）の札は上
    "c626": dict(
        t="灰は、島の人々にも",
        s="マーシャル諸島の北部",
        fig=ss.isles_map([
            dict(tag=[dict(at="rongelap", t="64人", side="left"),
                      dict(at="ailinginae", t="18人", side="left")],
                 move=[dict(kind="fall", at="rongelap"), dict(kind="fall", at="ailinginae")]),
            dict(tag=dict(at="rongerik", t="アメリカ兵28人", side="above"))]),
    ),

}
