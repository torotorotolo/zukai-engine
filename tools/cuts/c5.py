# -*- coding: utf-8 -*-
"""第5章 電話1本の約束 c501–c524（24カット）。13本目（トルコ航空981便）。⑤b-3（2026-09-25）で書いた。

⚠️ 12本目の中身は `git show 3832147:tools/cuts/c5.py`（⑤b-1 で空にした）。

■ 写真 5/24（上院の頁4枚＝p2030・p2033・p2046・p2055＝引用＝額装・原色／着陸する同型機 C1）
   切り出しは `ss.TRIM`（上院の頁は行の箱が重なる＝インクが最も少ない行で切った）
■ 決め所 c508（p2030）・c513（p2032）・c517（p2034）はなぞる型（trace）
■ 台本 §7 から替えたところ（⑤b-3 の決め）
  c512：上院 p2032 の紙面 → 議員と元社長の関係図（people）。次の c513 が同じ頁の問いと答えをなぞる
        ＝同じ紙面が2カット続くのを避けた
■ 実名＝FAA 長官シェイファー・ダグラス社長マクゴーエン・西部地域局長バスナイト（台本 §1-2）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
NOTE_SEN = "出典：米上院の報告"

SPEC = {

    # FAA のしくみ（上院 p2031・p2030「FAA's Western Region in Los Angeles」）
    "c501": dict(
        t="旅客機の安全の役所",
        s="FAA（連邦航空局）のしくみ",
        fig=("people", dict(
            nodes=[dict(x=0.24, y=0.42, t="FAAの本部", d="ワシントン", kind="org", c=J.INST),
                   dict(x=0.76, y=0.42, t="西部地域局", d="ダグラスの工場の地域", kind="org", c=J.AMBER)],
            edges=[dict(a=0, b=1, t="", c=J.LINE)], pair=True,
            note=f"{NOTE_SEN} PDF 30〜31頁")),
    ),

    # AD（上院 p2031）。3行＝柱3本
    "c502": dict(
        t="国が出す命令",
        s="ADとは",
        fig=("panel", dict(
            blocks=[dict(k="FAAの手段", t="直さなければ飛ばせない", c=J.INST),
                    dict(k="呼び名", t="耐空性改善命令", v="英語の頭文字でAD", c=J.ALERT),
                    dict(k="期限まで", t="直さない機体は飛べない", c=J.AMBER)],
            note=f"{NOTE_SEN} PDF 31頁")),
    ),

    # SB と AD（上院 p2031・p2055「compliance with service bulletins is voluntary」）
    "c503": dict(
        t="2つの知らせの違い",
        s="SBとADをくらべる",
        fig=("beforeafter", dict(
            a=dict(k="SB", t="すすめる", lines=["メーカーが出す", "従うかは航空会社しだい"], v="", c=J.LINE),
            b=dict(k="AD", t="従わせる", lines=["国が出す", "法律と同じ力"], v="", c=J.ALERT),
            arrow=False, note=f"{NOTE_SEN} PDF 31頁・55頁")),
    ),

    # 上院 p2030（西部地域局が AD を準備していた段）＝引用＝額装・原色
    "c504": dict(
        t="命令の準備",
        s="上院の報告がまとめた経緯",
        photo=ss.page(2030), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="西部地域局", d="改修を義務にする命令", dc=J.AMBER),
             dict(t="きっかけ", d="ウィンザーの事故", dc=J.TICK)],
    ),

    # 3者の合意（上院 p2031・p2055「the Western Region, the Flight Standards Service and the Deputy Administrator」）
    "c505": dict(
        t="3者の合意",
        s="FAAの中の考え",
        fig=("people", dict(
            # r03：3つを縦一列に置くと箱どうしの間が足りず最小幅（300px）に落ち、長い名前が箱からあふれた。
            #   しかも段が「矢印3本→節4つ」の7段で、右の箱は92%の1枚でも出ていなかった
            #   → 横一列＋合意の箱を下に・pair=True（節と、その節に入る矢印を1段に）＝4段
            nodes=[dict(x=0.17, y=0.22, t="西部地域局", d="ロサンゼルス", kind="org", c=J.INST),
                   dict(x=0.50, y=0.22, t="安全の基準の部の長", d="ワシントンの本部", kind="person", c=J.INST),
                   dict(x=0.83, y=0.22, t="副長官", kind="person", c=J.INST),
                   dict(x=0.50, y=0.78, t="ADを出す", d="いったん合意", c=J.ALERT)],
            edges=[dict(a=0, b=3, t="", c=J.LINE), dict(a=1, b=3, t="", c=J.LINE),
                   dict(a=2, b=3, t="", c=J.LINE)], pair=True,
            note=f"{NOTE_SEN} PDF 31頁・55頁")),
    ),

    # 着陸する同型機（KLM・1972年12月・CC0・全画面）。電話の日付と人（上院 p2030）
    "c506": dict(
        t="3日後の電話",
        s="着陸する同じ型の機体（KLM）　1972年12月・アムステルダム",
        photo=P("klm_landing_1972"), **ss.kind(P("klm_landing_1972")),
        side="right", ann_y=330,
        ann=[dict(t="1972年6月15日", d="ウィンザーの3日後", dc=J.TICK),
             dict(t="かけた人", d="FAA長官 シェイファー", dc=J.AMBER),
             dict(t="受けた人", d="ダグラス社長 マクゴーエン", dc=J.AMBER)],
    ),

    # 西部地域局長の証言（上院 p2030）
    "c507": dict(
        t="局長の証言",
        s="上院の報告が記す電話の中身",
        fig=("panel", dict(
            blocks=[dict(k="証言した人", t="西部地域局長 バスナイト", c=J.INST),
                    dict(k="長官は", t="妥当な直し方を喜んだ", c=J.AMBER)],
            note=f"{NOTE_SEN} PDF 30頁", cols=2)),
    ),

    # 🔴 決め所⑦（台本 §2 #7・上院 p2030）。上の切り口はインクが最も少ない行（0.3345）・下は白い行（0.4402）
    "c508": dict(
        t="書面の無い約束",
        s="長官が社長に伝えたこと",
        fig=("trace", dict(
            page=ss.page(2030),
            lines=[(0.2594, 0.3806, 0.8893, 0.3974), (0.1361, 0.3952, 0.5326, 0.4124)],
            phrase="紳士協定で直せば、ADは出さずに済む",
            doc="米上院の報告 PDF 30頁の原文（西部地域局長の証言）",
            crop=(0.12, 0.3345, 0.91, 0.4402))),
    ),

    # 上院 p2030〜p2032
    "c509": dict(
        t="決まった進め方",
        s="電話のあと",
        fig=("panel", dict(
            blocks=[dict(k="改修の進め方", t="命令ではなくSB", c=J.AMBER),
                    dict(k="数日後", t="局長が長官に訴える", v="考え直してほしい", c=J.INST),
                    dict(k="長官", t="約束だけで返事なし", v="局長の証言", c=J.ALERT)],
            note=f"{NOTE_SEN} PDF 30〜32頁")),
    ),

    # 元長官の説明（1974年の公聴会・上院 p2031）
    "c510": dict(
        t="元長官の説明",
        s="1974年の公聴会",
        fig=("panel", dict(
            blocks=[dict(k="直し方", t="簡単な部品で直せる", c=J.LINE),
                    dict(k="当時の機体", t="およそ35機", c=J.AMBER),
                    dict(k="SBなら", t="手順・部品・人がそろう", c=J.LINE)],
            note=f"{NOTE_SEN} PDF 31頁")),
    ),

    # 上院の指摘（p2031〜p2032）
    "c511": dict(
        t="上院の見立て",
        s="長官の説明への指摘",
        fig=("panel", dict(
            blocks=[dict(k="上院", t="順番の取り違え", c=J.ALERT),
                    dict(k="電話のころの話", t="のぞき窓を付ける改修", c=J.LINE),
                    dict(k="部品の改修", t="まだ考え出されていない", c=J.AMBER)],
            note=f"{NOTE_SEN} PDF 31〜32頁")),
    ),

    # 議員の問い（上院 p2032）。紙面は次の c513 がなぞる＝ここは関係図
    "c512": dict(
        t="社長の側の答え",
        s="1974年の公聴会",
        fig=("people", dict(
            nodes=[dict(x=0.22, y=0.45, t="上院の議員", d="公聴会で問う", kind="person", c=J.INST),
                   dict(x=0.78, y=0.45, t="ダグラスの元社長", d="マクゴーエン", kind="person", c=J.AMBER)],
            edges=[dict(a=0, b=1, t="紳士協定を結んだのか", c=J.LINE)], pair=True,
            note=f"{NOTE_SEN} PDF 32頁")),
    ),

    # 🔴 決め所⑧（台本 §2 #8・上院 p2032）。1行のナレーション＝pre=0。問い（上の2行）ごと切る
    "c513": dict(
        t="元社長の答え",
        s="公聴会の記録",
        fig=("trace", dict(
            page=ss.page(2032),
            lines=[(0.3030, 0.3408, 0.8880, 0.3562), (0.1343, 0.3541, 0.1674, 0.3680)],
            phrase="紳士協定と呼ぶのかどうかは分からない",
            doc="米上院の報告 PDF 32頁の原文",
            crop=(0.12, 0.2757, 0.91, 0.4014))),
    ),

    # 上院 p2032（「work 24 hours a day to get those parts to the airlines」）
    "c514": dict(
        t="社長の約束の中身",
        s="公聴会での答え",
        fig=("panel", dict(
            blocks=[dict(k="約束したこと", t="のぞき窓の部品", v="休まず作って届ける", c=J.AMBER),
                    dict(k="元社長の話", t="航空会社はすぐに済ませた", c=J.LINE)],
            note=f"{NOTE_SEN} PDF 32頁", cols=2)),
    ),

    # 上院 p2033（6月16日の FAA の電報・For Official Use Only）＝引用＝額装・原色
    "c515": dict(
        t="役所からの電報",
        s="FAAの電報の頭",
        photo=ss.page(2033), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="1972年6月16日", d="FAAが打った", dc=J.TICK),
             dict(t="宛先", d="航空会社4社の社長", dc=J.AMBER),
             dict(t="扱い", d="部外秘", dc=J.ALERT)],
    ),

    # 表示の場所（上院 p2034「near the vent door closure handle on each lower cargo door」）
    "c516": dict(
        t="ハンドルのそばの表示",
        s="電報が求めたこと",
        fig=("panel", dict(
            blocks=[dict(k="付ける場所", t="通気扉のハンドルの近く", c=J.AMBER),
                    dict(k="付ける先", t="床下の貨物ドアすべて", c=J.LINE)],
            note=f"{NOTE_SEN} PDF 34頁", cols=2)),
    ),

    # 🔴 決め所⑨（台本 §2 #9・上院 p2034）。1行の文＝行の上下は白い行（画素）で切る
    "c517": dict(
        t="力の上限",
        s="表示の文言",
        fig=("trace", dict(
            page=ss.page(2034),
            lines=[(0.2021, 0.1543, 0.8930, 0.1690)],
            phrase="約23キロ（50ポンド）を超えて押すな",
            doc="FAAの電報（米上院の報告 PDF 34頁）の原文",
            crop=(0.12, 0.1188, 0.91, 0.2406))),
    ),

    # 表示のねらい（上院 p2034）
    "c518": dict(
        t="表示のねらい",
        s="電報の続き",
        fig=("panel", dict(
            blocks=[dict(k="約23キロまで", t="ふつうに閉める", c=J.LINE),
                    dict(k="それを超えるなら", t="錠を確かめる", c=J.ALERT)],
            note=f"{NOTE_SEN} PDF 34頁", cols=2)),
    ),

    # 2通目の電報と、法の力（上院 p2032・p2034）
    "c519": dict(
        t="守らせる力の無い電報",
        s="2通目の電報",
        fig=("panel", dict(
            blocks=[dict(k="6月19日", t="1通目に置き換わる", v="表示の項目は無し", c=J.TICK),
                    dict(k="求めたこと", t="配線とのぞき窓の改修", v="期限は飛行300時間", c=J.AMBER),
                    dict(k="法の力", t="無い", v="ADではない", c=J.ALERT)],
            note=f"{NOTE_SEN} PDF 32頁・34頁")),
    ),

    # 上院 p2046（NTSB の勧告の書簡の頭）＝引用＝額装・原色
    "c520": dict(
        t="新しいSBと勧告",
        s="勧告の書簡の頭（上院の報告に再録）",
        photo=ss.page(2046), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="7月3日", d="ダグラスが SB 52-37", dc=J.AMBER),
             dict(t="7月6日", d="NTSBの勧告が届く", dc=J.INST),
             dict(t="翌日のFAAの返事", d="52-37に触れず", dc=J.ALERT)],
    ),

    # 8月の時点（上院 p2035・p2036・p2048）
    "c521": dict(
        t="済んでいない改修",
        s="1972年8月の時点",
        fig=("panel", dict(
            blocks=[dict(k="8月7日", t="改修の済んだ機体", v="0機", c=J.ALERT),
                    dict(k="FAAの電報", t="求めた改修の外", c=J.AMBER),
                    dict(k="上院の批判", t="自分で確かめず", c=J.TICK)],
            note=f"{NOTE_SEN} PDF 35頁・36頁・48頁")),
    ),

    # 上院 p2055（委員会の結論）＝引用＝額装・原色
    "c522": dict(
        t="委員会の結論",
        s="上院の報告の結論の節（1974年）",
        photo=ss.page(2055), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="長官", d="正直に、善意で動いた", dc=J.TICK),
             dict(t="重大な危険には", d="ADを出すことだけが正しい", dc=J.ALERT)],
    ),

    # 上院 p2055「pursuant to an oral agreement with the president of Douglas Aircraft」
    "c523": dict(
        t="取り決めの呼び名",
        s="上院の委員会の言葉",
        fig=("panel", dict(
            blocks=[dict(k="長官と社長の取り決め", t="口頭の合意", v="oral agreement", c=J.AMBER)],
            note=f"{NOTE_SEN} PDF 55頁")),
    ),

    # 章の橋（副題は10本目からの型「ここまでと、この先」）
    "c524": dict(
        t="事故機へ",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="改修", t="メーカーのSBまかせ", c=J.LINE),
                    dict(k="鍵", t="パリの機体に入っていたか", v="第6章", c=J.AMBER)],
            cols=2)),
    ),

}
