# -*- coding: utf-8 -*-
"""第2章 水素爆弾と、キャッスル作戦 c201–c220（20カット）。12本目（キャッスル・ブラボー）。⑤b-3（2026-09-23）で書いた。

■ 実写 14/20（写真12・報告書の頁2）。章の色＝白黒（暖かい白黒）。爆発の実写は原色（`color=1.0`）。
■ 🔴 台本 §4 の画から変えたところ（⑤b-3 で決めた・根拠つき）
  c205・c206 … 図 → **マイクの写真2点**（Commons・PD。カズヤくん許可で取得。`qa_out/ep12_assets.py` の mike_*）
                ＝記録映画の 900〜1000秒がブラボーの場面と確かめられず、c308・c310 を図に振り替えたぶんの割合を補う
  c207       … quote → **報告書の実物をなぞる型**（DNA p31「but MIKE was not a deliverable nuclear weapon.」）
  c208       … B-36 の除染（事故の**後**の写真）→ **作戦を認めた原子力委員会の手紙（1954年1月21日）**＝事故の前（§5b-20）
  c213       … 図 → **ビキニ環礁の海図**（米海軍水路部 H.O. 6032。余白の刊行年を原寸で読んだ＝1954年第3版の**1958年改訂**）
  c218・c219 … c218＝`dev_shrimp_men` の**使い回し**（c113 と同じ副題・寄りと向きを変える）／c219＝トラックから降ろす装置
                （記録映画 Commander's Report の装置の場面は、はしけへ積む**別の回の装置**とみられ、ブラボーと確かめられない）
  c210       … ヤンキーの1/3（色あせて火球がほぼ見えない）→ ヤンキーの火球と輪の雲（`yankee_cloud`）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
SRC_DNA = ss.SRC_DNA
NOTE_DNA = "出典：国防原子力局の報告書（1982年）"

SPEC = {

    # 1950 → 1952（マイク）→ 1954（ブラボー）。旗は行に合わせて左から
    "c201": dict(
        t="水爆への道のり",
        s="1950年からの4年",
        fig=("timeline", dict(
            events=[dict(t=1950.0, top="開発の始まり", t2="1950年", c=J.LINE),
                    dict(t=1952.83, top="マイク", t2="1952年11月", c=J.AMBER),
                    dict(t=1954.17, top="ブラボー", t2="1954年3月", c=J.ALERT, big=True)],
            t0=1949.3, t1=1954.8,
            ticks=[(1950, "1950"), (1951, "1951"), (1952, "1952"), (1953, "1953"), (1954, "1954")],
            src=NOTE_DNA)),
    ),

    # ⚠️ 副題を字幕の頭（「それまでの原子爆弾」）から切り取らない・札と同じ語を置かない（check_echo・check_dup）
    "c202": dict(
        t="割って、力を出す",
        s="原子爆弾のしくみ",
        fig=("process", dict(
            steps=[dict(t="重い原子", d="ウラン・プルトニウム", c=J.LINE),
                   dict(t="割れる", d="核分裂", c=J.AMBER),
                   dict(t="大きな力", d="広島・長崎の型", c=J.ALERT)])),
    ),

    # 対比なので矢印を消す（§beforeafter の arrow）
    "c203": dict(
        t="割るか、くっつけるか",
        s="2つの爆弾のちがい",
        fig=("beforeafter", dict(
            a=dict(k="原子爆弾", t="割る", lines=["重い原子を"], v="", c=J.LINE),
            b=dict(k="水素爆弾", t="くっつける", lines=["軽い原子どうしを", "太陽と同じ核融合"], v="", c=J.AMBER),
            arrow=False)),
    ),

    "c204": dict(
        t="火をつける仕掛け",
        s="水素爆弾が爆発するまで",
        fig=("process", dict(
            steps=[dict(t="原子爆弾", d="火つけ役", c=J.ALERT),
                   dict(t="高い温度と圧力", d="とてつもない", c=J.AMBER),
                   dict(t="核融合", d="軽い原子がくっつく", c=J.OK)])),
    ),

    # 🔴 ⑤b-3 で写真に（Commons「IvyMike2 HR.jpg」・米国防総省・PD）。爆発の実写は原色
    # ⚠️ 副題に「マイク」と書くので、注記の答えに「マイク」を置かない（check_wording A）
    "c205": dict(
        t="1952年の水爆",
        s="マイクのきのこ雲　エニウェトク環礁",
        photo=P("mike_cloud"), **ss.kind(P("mike_cloud")),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="爆発の日（現地）", v="1952年11月1日", vc=J.INK_W, vs=64),
             dict(t="TNT火薬に直すと", v="1040万トン", vc=J.AMBER),
             dict(t="場所", d="マーシャル諸島", dc=J.TICK)],
    ),

    # 🔴 ⑤b-3 で写真に（Commons「Ivy Mike Sausage device.jpg」・米エネルギー省・PD）。
    #    左に装置の筒・右に配管＝注記は右（配管の側）
    "c206": dict(
        t="冷やし続ける燃料",
        s="マイクの装置と設備　1952年",
        photo=P("mike_device"), **ss.kind(P("mike_device")),
        side="right", ann_y=356,
        ann=[dict(t="燃料", d="冷やした液体", dc=J.LINE),
             dict(t="装置の大きさ", v="3階建て", vc=J.AMBER, d="建物を占めた")],
    ),

    # 🔴 決め所。報告書の実物をなぞる型（DNA p31「…, but MIKE was not a deliverable nuclear weapon.」）
    #    行の矩形は PDF の文字の層から取った（1行）
    "c207": dict(
        t="兵器として見ると",
        s="マイクについての一文",
        fig=("trace", dict(
            page=ss.page(31),
            lines=[(0.2756, 0.4106, 0.7265, 0.4294)],
            phrase="マイクは、運んで使える兵器ではなかった",
            doc=f"{SRC_DNA} 31頁の原文",
            # 切り口は行と行のすきま（段落の頭「CASTLE was the culmination」から「an aircraft」の行まで）
            # ⚠️ 見出しの行まで入れると頁が縦に伸び、出どころの行と和訳が 29px 重なった（check_layout）
            #    ＝ trace の頁は横÷縦が約3.3以上（和訳と出どころの置き場）
            # ⚠️ この頁は文字が x 0.048 から始まる（頁ごとに余白が違う）＝左 0.10 で切ると「CASTLE」が「ASTLE」になった
            crop=(0.03, 0.3405, 0.82, 0.506))),
    ),

    # 🔴 ⑤b-3：B-36 の除染（事故の後）→ 作戦を認めた手紙（事故の前・§5b-20）。英文そのものが主題（§5b-5）
    "c208": dict(
        t="承認された作戦",
        s="作戦を認めた原子力委員会の手紙　1954年1月21日",
        photo=P("doc_aec_letter"), **ss.kind(P("doc_aec_letter")),
        side="right",
        ann=[dict(t="次のねらい", d="飛行機で運べる水爆", dc=J.AMBER),
             dict(t="作戦の名", v="キャッスル", vc=J.INK_W, vs=72)],
    ),

    # 報告書の表1（頁の中の表だけ）
    "c209": dict(
        t="作戦は、春の3か月",
        s="報告書の表1　作戦の爆発の一覧",
        # 表の終わり（NECTAR の行 0.667）と注（Notes: 0.675）のすきまで切る＝注の行を半分だけ見せない
        photo=ss.page(30), panel=True, trim=(0.10, 0.44, 0.95, 0.674),
        side="right",
        ann=[dict(t="爆発の回数", v="6回", vc=J.AMBER),
             dict(t="場所", d="ビキニ5回・エニウェトク1回", dc=J.TICK)],
    ),

    # ヤンキー（1350万トン）＝1000万トンを超えた3回のうちの1回
    "c210": dict(
        t="とびぬけて大きな回",
        s="ヤンキーの火球と輪の雲　1954年",
        photo=P("yankee_cloud"), **ss.kind(P("yankee_cloud")),
        color=1.0,
        side="right",
        ann=[dict(t="1000万トン級", v="3回", vc=J.AMBER),
             dict(t="最初の1回", v="3月1日", vc=J.ALERT)],
    ),

    "c211": dict(
        t="作戦を動かした部隊",
        s="パリー島の施設の空撮　1954年",
        photo=P("base_parry_aerial"), **ss.kind(P("base_parry_aerial")),
        side="right", ann_y=330,
        ann=[dict(t="つくった側", d="軍と原子力委員会", dc=J.INST),
             dict(t="バッジを配られた人", v="1万人超", vc=J.AMBER),
             dict(t="部隊の名", d="第7合同任務部隊", dc=J.INK_W)],
    ),

    "c212": dict(
        t="サンゴの島々",
        s="エニウェトクの飛行場　1954年",
        photo=P("base_airfield"), **ss.kind(P("base_airfield")),
        cam="pan_r",
        side="right", ann_y=356,
        ann=[dict(t="場所", d="太平洋・マーシャル諸島", dc=J.TICK),
             dict(t="地形", d="環礁", dc=J.AMBER)],
    ),

    # 🔴 ⑤b-3 で写真に。海図の写しは1958年の改訂版（出典の行も1958年）＝副題に年を書かない
    "c213": dict(
        t="2つの環礁",
        s="ビキニ環礁の海図",
        photo=P("doc_bikini_chart"), **ss.kind(P("doc_bikini_chart")),
        cam="pull",
        side="right", ann_y=356,
        ann=[dict(t="使われた環礁", d="ビキニ・エニウェトク", dc=J.AMBER),
             dict(t="1946年の夏", v="2回", vc=J.ALERT, d="原子爆弾の実験")],
    ),

    # DOE の記録映像の1コマ（止め絵）。爆発の前＝章の色のまま
    "c214": dict(
        t="装置を置いた場所",
        s="射点の小屋　記録映像の1コマ",
        photo=P("doe_shotcab_near"), **ss.kind(P("doe_shotcab_near")),
        side="right", ann_y=330,
        ann=[dict(t="置いた場所", d="ナム島の沖", dc=J.AMBER),
             dict(t="建物", d="サンゴ礁の上", dc=J.LINE),
             dict(t="据えつけの完了", v="2月22日", vc=J.AMBER)],
    ),

    # 報告書の第54図（観測の機械を置いた島々）
    "c215": dict(
        t="島じゅうに観測の機械",
        s="報告書の第54図　ビキニ環礁",
        photo=ss.page(213), panel=True, trim=(0.05, 0.255, 0.99, 0.875),
        side="right",
        ann=[dict(t="測るもの", d="爆風と放射線", dc=J.LINE),
             dict(t="国防総省の実験", v="29計画", vc=J.AMBER)],
    ),

    "c216": dict(
        t="浴びてよい量の上限",
        s="防護服　1954年",
        photo=P("suits_three"), **ss.kind(P("suits_three")),
        side="right", ann_y=356,
        ann=[dict(t="決まり", d="浴びた量の記録", dc=J.LINE),
             dict(t="作戦中に浴びてよい量", d="上限あり", dc=J.ALERT)],
    ),

    # ⚠️ 答えの d は12字未満に（「ロンゲリック・マジュロなど」13字は字幕と2か所で一致＝check_echo）
    "c217": dict(
        t="島を測るべきか",
        s="灰を集める採取器の針金を切る　1954年",
        photo=P("fo_wire"), **ss.kind(P("fo_wire")),
        side="right", ann_y=356,
        ann=[dict(t="部隊の考え", d="島を測る必要なし", dc=J.ALERT),
             dict(t="計器を置いた島", d="ロンゲリック・マジュロ", dc=J.INST)],
    ),

    # 🔴 c113 と同じ1枚（使い回し）。**副題は c113 と同じ**（§5b-19）。寄りと注記の側を変える
    "c218": dict(
        t="装置を作った研究所",
        s="射点の小屋の中の装置と作業の人たち　1954年",
        photo=P("dev_shrimp_men"), **ss.kind(P("dev_shrimp_men")),
        cam="pan_l",
        side="right", ann_y=356,
        ann=[dict(t="作った研究所", d="ロスアラモス", dc=J.INST),
             dict(t="予定の日", v="3月1日", vc=J.AMBER, d="天気がよければ")],
    ),

    # Commons「Operation Castle AW 1」＝"Shrimp device tested in Castle Bravo being unloaded from a truck."
    "c219": dict(
        t="新しい形の水爆",
        s="トラックから降ろすブラボーの装置　1954年",
        photo=P("dev_truck"), **ss.kind(P("dev_truck")),
        side="right", ann_y=356,
        ann=[dict(t="燃料の形", d="マイクと別物", dc=J.AMBER),
             dict(t="うまくいけば", d="飛行機で運べる", dc=J.OK)],
    ),

    # 章の橋（副題は10本目からの型「ここまでと、この先」）
    "c220": dict(
        t="最初の試験の中身へ",
        s="ここまでと、この先",
        fig=("panel", dict(
            # ⚠️ 札の k に「ここまで」「この先」を置くと副題と同語（check_dup）
            blocks=[dict(k="試験", t="運べる水爆への最初の一歩", c=J.LINE),
                    dict(k="鍵", t="燃料", v="第3章", c=J.AMBER)],
            cols=2)),
    ),

}
