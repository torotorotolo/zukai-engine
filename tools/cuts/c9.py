# -*- coding: utf-8 -*-
"""第9章 その後 c901–c920（20カット）。12本目（キャッスル・ブラボー）。⑤b-4（2026-09-23）で書いた。

■ 実写 11/20（写真10・報告書の頁1）。章の色＝紺（11本目までの様式）。爆発の実写は原色（`color=1.0`）。
■ 🔴 c903 に報告書の第67図（p240）を出さない＝第67図は c108（NARA #49）と**同じ場面の別のコマ**（⑤b-3 で頁を見た）
   → NARA #29 `rongelap_booties`（小屋のそばの調査の人・第67図とは別の写真）
■ c912 は第4章 c402 の東の地図（ウトリックまで）が戻る
■ c908 → c909 は同じ時間軸（灰を浴びてからの日数）が戻り、旗が増える
■ ⚠️ 隅の章名が「その後」＝見出し・副題に「その後」を入れると同じ言葉が二度出る（check_dup・c602 と同じ形）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
SRC_DNA = ss.SRC_DNA
NOTE_DNA = "出典：国防原子力局の報告書（1982年）"
NOTE_WT = "出典：医師団の報告書（1954年）"
# 灰を浴びてからの日数（WT p1004・p1022・p1023・p1072）。c908 と c909 で同じ軸
DAYS = dict(t0=-3, t1=80, ticks=[(0, "0"), (20, "20"), (40, "40"), (60, "60"), (80, "80")],
            title="灰を浴びてからの日数", src=NOTE_WT)
EV_NAUSEA = dict(t=1.5, top="吐き気", t2="1日か2日", c=J.AMBER)
# ⚠️ 「髪が抜ける・皮膚の傷」は漢字5字で 34〜44px に縮みつぶれた（check_layout）＝短く
EV_HAIR = dict(t=14, top="髪と肌", t2="2週間ほど", c=J.ALERT)


SPEC = {

    # NARA #05（ロメオのきのこ雲・縦長＝額装）。原色
    "c901": dict(
        t="作戦は、止まらない",
        s="ロメオのきのこ雲　1954年3月27日",
        photo=P("romeo_cloud"), **ss.kind(P("romeo_cloud")),
        color=1.0,
        side="right",
        ann=[dict(t="次の爆発", v="26日後", vc=J.AMBER, d="ブラボーの穴の上で")],
    ),

    # NARA #11（ネクター・雲の中の光）。原色
    "c902": dict(
        t="最後の爆発",
        s="ネクターの爆発　1954年5月14日",
        photo=P("nectar_cloud"), **ss.kind(P("nectar_cloud")),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="場所", d="エニウェトク環礁", dc=J.AMBER),
             dict(t="作戦の爆発", v="6回", vc=J.AMBER)],
    ),

    # 🔴 第67図ではなく NARA #29（小屋のそばの調査の人・焼き付けの白い縁は `ss.TRIM` で落とした）
    "c903": dict(
        t="靴に、覆い",
        s="ロンゲラップの調査の人　1954年",
        photo=P("rongelap_booties"), **ss.kind(P("rongelap_booties")),
        side="right",
        ann=[dict(t="残った放射線", d="船で島々を回って調べる", dc=J.TICK),
             dict(t="調べ直し", d="4月のはじめまで", dc=J.AMBER)],
    ),

    # NARA #26（艦の前の甲板を洗う・白い服と雨具の人）
    "c904": dict(
        t="部隊の中にも",
        s="艦の前の甲板を洗う　1954年",
        photo=P("dc_ship_scrub"), **ss.kind(P("dc_ship_scrub")),
        cam="pan_l",
        side="right", ann_y=330,
        ann=[dict(t="やけどのような傷", v="37人", vc=J.ALERT, d="2隻の船"),
             dict(t="傷", d="すべて回復", dc=J.OK)],
    ),

    # NARA #42（防護服をこすって洗う・顔はフードとマスクで見えない）
    "c905": dict(
        t="浴びてよい量の上限",
        s="防護服をこすって洗う　1954年",
        photo=P("suits_scrub"), **ss.kind(P("suits_scrub")),
        cam="pull",
        side="right", ann_y=330,
        ann=[dict(t="いちばん多い兵士", d="上限の20倍超", dc=J.ALERT),
             dict(t="特別な許可", d="上限の2倍まで", dc=J.AMBER)],
    ),

    # WT p1006（医師団の報告書）
    "c906": dict(
        t="備えのない医師団",
        s="集められた医師たち",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="人の体を調べる計画", d="もともと無し", ok=False, c=J.ALERT),
                   dict(t="医師たちの備え", d="何も無いまま", ok=False, c=J.ALERT)],
            lead="キャッスル作戦",
            note=NOTE_WT)),
    ),

    # 割合を棒の長さに（3人に2人＝67・4人に1人超＝25）
    "c907": dict(
        t="はじめの数日",
        # ⚠️ 副題「ロンゲラップの人々」は字幕の文の頭の切り取り（check_echo）
        s="島の住民の体",
        fig=("compare", dict(
            items=[dict(v=67, t="吐き気", disp="3人に2人", unit="", c=J.ALERT),
                   dict(v=25, t="目や皮膚のかゆみ", disp="4人に1人超", unit="", c=J.AMBER)],
            note=NOTE_WT + "　棒の長さは割合")),
    ),

    "c908": dict(
        t="次に出た変化",
        s="ロンゲラップの人々の経過",
        fig=("timeline", dict(
            events=[dict(EV_NAUSEA), dict(EV_HAIR, big=True)],
            **DAYS)),
    ),

    # 同じ時間軸が戻る。血小板の値そのものは描かない（曲線を描き起こさない）＝いちばん少ない期間の帯と76日目の旗
    "c909": dict(
        t="減り続けた血小板",
        s="ロンゲラップの人々の経過",
        fig=("timeline", dict(
            events=[dict(EV_NAUSEA), dict(EV_HAIR),
                    dict(t=76, top="ふつうの値に届かず", t2="76日目", c=J.TICK, big=True)],
            band=[dict(a=25, b=30, t="血小板がいちばん少ない", c=J.ALERT)],
            **DAYS)),
    ),

    # WT の第5.2図（ロンゲラップの雨水の槽）。人は写っていない（⑤b-3 で見た）
    "c910": dict(
        t="体の中に入ったもの",
        s="報告書の第5.2図　ロンゲラップの雨水の槽",
        photo=ss.page(1082), panel=True, trim=(0.10, 0.47, 0.90, 0.815),
        side="right",
        ann=[dict(t="飲み水", d="雨水をためる槽", dc=J.TICK),
             dict(t="1954年の見立て", d="長く続く害は無い", dc=J.TICK)],
    ),

    "c911": dict(
        t="調査は、続いた",
        s="住民の体の調査",
        fig=("panel", dict(
            blocks=[dict(k="1956年から", t="国立の研究所", c=J.INST),
                    dict(k="1982年の時点", t="まだ続く", c=J.AMBER)],
            cols=2)),
    ),

    # 🔴 drift（東の地図が戻る＝c402）。年は DNA p194
    "c912": dict(
        t="先に戻った島",
        s="島へ戻った年",
        fig=("drift", ss.drift_map(
            steps=[dict(tag=dict(at="utirik", t="1954年6月", side="above"))],
            view=ss.MAP_VIEW_EAST, places=ss.MAP_PLACES_EAST, src="DNA p194",
            note="模式図：島は環礁の中心（緯度経度の表）。年は報告書の値")),
    ),

    # 🔴 決め所（DNA p194）
    "c913": dict(
        t="マジュロへ移った人々",
        s="ロンゲラップの人々の行き先",
        fig=("quote", dict(
            phrase="ロンゲラップの住民は、1957年に戻った",
            who="国防原子力局",
            when="1982年",
            doc="報告書（島の人々のこと）")),
    ),

    # Commons「HD.10.290」（雲に包まれたブラボーの火球）。原色
    "c914": dict(
        t="威力と、島の灰",
        s="雲に包まれた火球　1954年3月1日",
        photo=P("fb_close_b"), **ss.kind(P("fb_close_b")),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="2013年の報告書", d="予定の威力でも汚染の見込み", dc=J.ALERT),
             dict(t="威力が外れた理由", d="いまも定まらず", dc=J.TICK)],
    ),

    # NARA #41（採取器の濾紙の枠と鉛の箱・縦長＝額装）
    "c915": dict(
        t="何が灰を運んだか",
        s="採取器の濾紙の枠　1954年",
        photo=P("fo_rolled"), **ss.kind(P("fo_rolled")),
        side="right",
        ann=[dict(t="よく語られる説", d="高さ6キロの風", dc=J.TICK),
             dict(t="2013年の報告書", d="高く昇った雲の灰", dc=J.ALERT)],
    ),

    # NARA #45（アドリカン島で器材を回収する防護服の人・暗い額）
    "c916": dict(
        t="予期しない被曝",
        s="アドリカン島の器材の回収　1954年",
        photo=P("suits_adrikan"), **ss.kind(P("suits_adrikan")),
        side="right",
        ann=[dict(t="支えた兵士の一部", d="アメリカ兵", dc=J.TICK),
             dict(t="外国の漁師", d="第五福竜丸", dc=J.AMBER),
             dict(t="島の人々", d="マーシャル諸島", dc=J.ALERT)],
    ),

    # 船の行き先（B8）。⚠️ 副題に「その後」を入れない（隅の章名と同じ）
    # ⚠️ 見出し「名前を変えた船」は段の札「名前を変えて」が覆った（check_dup）
    "c917": dict(
        t="船の行方",
        s="1954年から1967年",
        fig=("process", dict(
            steps=[dict(t="水産大学の船", d="名前を変えて", c=J.LINE),
                   dict(t="役目を終える", d="1967年", c=J.TICK),
                   dict(t="夢の島", d="ゴミの埋め立て地", c=J.ALERT)],
            note="出典：都立第五福竜丸展示館")),
    ),

    "c918": dict(
        t="展示館の船",
        s="船の公開",
        fig=("moment", dict(
            clock="1976年", label="東京都",
            facts=[dict(t="夢の島", v="展示館で公開", c=J.AMBER),
                   dict(t="いま", v="見に行ける船", c=J.OK)],
            sub="出典：都立第五福竜丸展示館")),
    ),

    # NARA #34（白い服の2人が長い棒を持ち上げる・鉛の容器と台車）
    "c919": dict(
        t="見込めなかった灰",
        s="棒で鉛の容器を扱う　1954年",
        photo=P("fo_pig_lift"), **ss.kind(P("fo_pig_lift")),
        cam="pan_r",
        side="right", ann_y=330,
        ann=[dict(t="高く昇った雲の灰", d="落ち方は推測だけ", dc=J.TICK),
             dict(t="灰が降った所", d="海の上と島の上", dc=J.ALERT)],
    ),

    # DOE 記録映像の1コマ（止め絵・傘の広がったきのこ雲）。`rate` が 0.4 未満の欄＝動画にしない（footage.py の注）。原色
    "c920": dict(
        t="雲の下にいた人々",
        s="遠くから見たきのこ雲　記録映像の1コマ",
        photo=P("doe_cloud_cap"), **ss.kind(P("doe_cloud_cap")),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="1954年3月1日", v="午前6時45分", vc=J.AMBER),
             dict(t="雲の下", d="漁船・島の人々・兵士", dc=J.ALERT)],
    ),

}
