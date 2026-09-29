# -*- coding: utf-8 -*-
"""第12章　舵は、まだ決まっていない cc01–cc16（16カット）。14本目（セウォル号）。

■ 🔴 2026-09-28（⑤b-1）：13本目（トルコ航空981便）の中身を空にした＝git の `b54ee4f`（`git show b54ee4f:tools/cuts/cc.py`）。
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
    "cc01": dict(kind='混ざり',
               plan='【混ざり】`c105` の型で左（なぜ傾いたか）を灯す（追補 §4）',
               src='—'),
    "cc02": dict(kind='図解',
               plan='【年表】原因の年表（2014）（追補 §4）',
               src='海審 p1009・p1125'),
    "cc03": dict(kind='文字の頁',
               plan='台本の画：図 p1091（海審の84頁・舵角を確かめる資料は無い）',
               src='海審 p1091・p1092'),
    "cc04": dict(kind='図・写真の頁',
               plan='【図の頁】海審 p1083〔그림4〕舵角の場合ごとの傾き（模擬の結果）（追補 §4）｜⚠️ 海審 p1083 は見出しで選んだ＝原寸で見て語り（航跡と模擬）に合うか。合わなければ c609 の図8の頁を戻す（追補 §7-4）。出典は「海審 p1083・p1091〜1092」（§7-5）',
               src='海審 p1091〜1092'),
    "cc05": dict(kind='図解',
               plan='【流れ】舵を動かす仕組み（操舵台→電気→弁→油→舵・模式）（追補 §4）',
               src='海審 p1118〜1119'),
    "cc06": dict(kind='図解',
               plan='【年表】2015（追補 §4）',
               src='船員2審 p5007・判決 p33〜34'),
    "cc07": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='船員2審 p5007'),
    "cc08": dict(kind='パネル',
               plan='台本の画：panel 刑事裁判のきまり',
               src='船員2審 p5007'),
    "cc09": dict(kind='写真',
               plan='台本の画：実写 Googleアース モッポ新港（現在）',
               src='裁決 p2050・p2088'),
    "cc10": dict(kind='図・写真の頁',
               plan='【図の頁】裁決 p2089〔사진5〕弁の鉄の芯の固着の写真（出典は p2088〜2089）（追補 §4）｜⚠️ 出典は「裁決 p2088〜2089」（写真は p2089・追補 §7-5）',
               src='裁決 p2088'),
    "cc11": dict(kind='図解',
               plan='【年表】2018（2つに分かれる）（追補 §4）',
               src='特調委 p3073'),
    "cc12": dict(kind='図解',
               plan='【流れ】`cc05` の仕組みの図で弁に「可能性は非常に低い」（追補 §4）',
               src='特調委 p3088'),
    "cc13": dict(kind='図解',
               plan='【並べ】`c615` の並べ図に「外からの力」（追補 §4）',
               src='特調委 p4161〜4162'),
    "cc14": dict(kind='文字の頁',
               plan='台本の画：図 p2003（2026年の裁決の主文）',
               src='裁決 p2001・p2003〜2004'),
    "cc15": dict(kind='図解',
               plan='【年表】2026（追補 §4）',
               src='裁決 p2003・p2087〜2088・p2094・p2129'),
    "cc16": dict(kind='混ざり',
               plan='【混ざり】`c105` の型＝2つの問いに答え（左＝決まっていない・右＝主文）（追補 §4）',
               src='裁決 p2003〜2004'),
}

SPEC = {
    # ── 🔴 ⑤b-5（2026-09-29）：軸の型＝`tools/axis.py`（門番 check_axis）──
    # 原因の年表（2014→2026）。🔴 原因は決まっていない＝場面にせず、機関の名と、その機関が挙げた原因の項目の札を並べるだけ。
    #   札の項目は c615・cc13 の並べ図と同じ言葉（舵の使い方／装置の故障／外からの力）
    "cc02": dict(
        t="最初の結論",
        s="原因の年表",
        fig=("axis", dict(ss.AX_CAUSE,
                          steps=[dict(add=ss.ax("kmst"), cur="2014-12-29"),
                                 dict(add=dict(k="chips", at="2014-12-29", chips=["舵の使い方"], rec=["海審 p1001", "海審 p1125"],
                                               c="INST"))],
                          note=ss.CAUSE_NOTE, src=ss.src(["海審 p1001", "海審 p1125"]))),
    ),

    # 2015年＝2審（2015-04-28）・大法院（2015-11-12）＝船員の2審 p5007。年だけで置く（年の真ん中）
    "cc06": dict(
        t="2015年の裁判",
        s="原因の年表",
        fig=("axis", dict(ss.AX_CAUSE, past=[ss.ax("kmst")], start=dict(cur="2014-12-29"),
                          steps=[dict(add=ss.ax("court"), cur="2015"),
                                 dict(add=dict(k="chips", at="2015", chips=["装置の故障？"], rec=["船員の2審 p5007", "判決 p33"],
                                               c="INST"))],
                          note=ss.CAUSE_NOTE, src=ss.src(["船員の2審 p5007", "判決 p33〜34"]))),
    ),

    # 2018年8月 船体調査委（特調委 p3073）＝内側の原因の案と、外からの力を否定しきれない案に分かれた
    "cc11": dict(
        t="2018年の委員会",
        s="原因の年表",
        fig=("axis", dict(ss.AX_CAUSE, past=[ss.ax("kmst"), ss.ax("court"), ss.ax("raise")], start=dict(cur="2017-03-23"),
                          steps=[dict(), dict(add=ss.ax("hull18"), cur="2018-08"),
                                 dict(add=dict(k="chips", at="2018-08", chips=["内側の原因", "外からの力"], rec="特調委 p3073",
                                               c="INST"))],
                          note=ss.CAUSE_NOTE, src=ss.src(["特調委 p3061", "特調委 p3073"]))),
    ),

    # 2026年1月28日 中央海審の裁決（裁決 p2001）。主文に原因の項目は無い＝1行目は点だけ・2行目で理由の部分の項目
    "cc15": dict(
        t="2026年の裁決",
        s="主文と理由の部分",
        fig=("axis", dict(ss.AX_CAUSE, past=[ss.ax("kmst"), ss.ax("court"), ss.ax("raise"), ss.ax("hull18"), ss.ax("sccc")],
                          start=dict(cur="2022-09"),
                          steps=[dict(add=ss.ax("kmst26", big=True), cur="2026-01-28"),
                                 dict(add=dict(k="chips", at="2026-01-28", chips=["舵の使い方", "装置の故障"],
                                               rec=["裁決 p2001", "裁決 p2087〜2088"], c="INST")), dict()],
                          note=ss.CAUSE_NOTE, src=ss.src(["裁決 p2001", "裁決 p2003", "裁決 p2087〜2088"]))),
    ),

    # ── 🔴 ⑤b-6（2026-09-29）：箱の型＝`tools/boxes.py`（門番 check_boxes）──
    # 舵を動かす仕組み（模式）＝海審 p1118 の注60（操舵の電気の信号 → 弁が油の流れを切りかえる → 舵）。
    #   固着の説は報告書が退けた（p1118 5.3.4〜5.3.5）。部品の形・位置は描かない（役目のつながりだけ）
    "cc05": dict(
        t="舵を動かす仕組み",
        s="2014年の検討",
        fig=("boxes", dict(view="flow", layout=ss.RUD,
                           steps=[dict(add=ss.rud("q_valve")), dict(add=[ss.rud("e_elec"), ss.rud("e_oil")]),
                                  dict(add=ss.rud("c_kmst"))],
                           note="部品の形と位置は描いていない（役目のつながりだけ）", src=ss.src(["海審 p1118"]))),
    ),

    # 2022年 特別調査委＝弁の固着が急な右旋回と傾きを起こした可能性は非常に低い（特調委 p3013。PLAN の p3088 は外からの力の頁）
    "cc12": dict(
        t="固まった弁の見方",
        s="国の委員会の調べ",
        fig=("boxes", dict(view="flow", layout=ss.RUD,
                           past=[ss.rud("q_valve"), ss.rud("e_elec"), ss.rud("e_oil"), ss.rud("c_kmst")],
                           steps=[dict(), dict(add=ss.rud("c_sccc"))],
                           note="部品の形と位置は描いていない（役目のつながりだけ）", src=ss.src(["特調委 p3013"]))),
    ),

    # 並べ図に3つめ（外からの力？）＝特調委 p3013・特調委小 p4161（外からの衝撃の可能性を打ち消せない・沈んだとは確認されない）。
    #   c615 の2つは沈めない（同じ形で並べるだけ＝どれかを目立たせない）
    "cc13": dict(
        t="船体の傷",
        s="2022年の報告",
        fig=("boxes", dict(view="row", slots=3, past=[ss.cause("rudder", keep=True), ss.cause("fault", keep=True)],
                           steps=[dict(add=ss.cause("outer")), dict(), dict()],
                           src=ss.src(["特調委 p3013", "特調委小 p4161"]))),
    ),
}
