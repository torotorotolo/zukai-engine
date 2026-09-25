# -*- coding: utf-8 -*-
"""第8章 日本の48人と、報告書の結論 c801–c822（22カット）。13本目（トルコ航空981便）。⑤b-4（2026-09-25）で書いた。

⚠️ 12本目の中身は `git show 3832147:tools/cuts/c8.py`（⑤b-1 で空にした）。
⚠️ 見出し・副題に章名の語（「日本の48人」「報告書の結論」）を入れない（§5b-46）。

■ 写真 7/22（石碑 B3＝BY-SA 額装／同型機の客室 D3・タラップの乗客 C4／名前の壁 B2＝**名前にモザイク**／
   上院の表紙 p2005・英訳の表紙 p1001・付属書の表紙 p109＝引用＝額装・原色）
■ 決め所 c807（国会 p6007＝頁の画像なし）は引用札（quote）・c819（仏 p104）はなぞる型（trace）
■ 錠（latch）＝c820（錠がかからないまま、閉まって見える）＝第3章の c316・c317 の絵が戻る
■ 国会の記録＝`ref/ep13/facts_japan.md` C1〜C3。会社名は出さない（台本 §1-2・c105 と同じ）
■ c804 の写真（C4）：Commons の題名は「操縦室と操縦士」だが、絵は**タラップの乗客と機体**（⑤b-4 に1000pxで見た＝
   台帳の実見の記録が正しい）。人は遠景（顔は小さい）
■ c814（B2 名前の壁）：原寸で私人の名前が読める＝元画像の板の面に12画素のモザイク（`ss.NEEDS_MASK`・`ref/ep13/masked.json`）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
NOTE_FR = "出典：フランスの最終報告書"
NOTE = "模式図：4つのフックのうち1つ。形と大きさは実物どおりではない（報告書の図7の順番）"

SPEC = {

    # 森の中の石碑（B3・CC BY-SA 2.0 fr＝額装・原色・1点1カット・札を重ねない）。乗員12人の内訳は仏 p13・p18・p19〜p26
    "c801": dict(
        t="生存者なし",
        s="森の中の石碑（区画144）　2010年",
        photo=P("stele_2010"), panel=True, color=1.0,
    ),

    # 同型機の客室（D3・PD US no notice・ダグラスの広報写真・全画面）。仏 p19〜p26
    "c802": dict(
        t="客室の乗務員",
        s="同じ型の機体の客室（ダグラスの広報写真）",
        photo=P("dc10_cabin"), **ss.kind(P("dc10_cabin")),
        side="right", ann_y=330,
        ann=[dict(t="客室乗務員", v="8人", vc=J.AMBER),
             dict(t="内訳", d="チーフ1人・スチュワーデス7人", dc=J.TICK)],
    ),

    # 事故の翌日の国会（国会 p6005）
    "c803": dict(
        t="議員が呼んだ「史上最大」",
        s="1974年3月4日の衆議院",
        fig=("moment", dict(
            clock="3月4日", label="1974年",
            facts=[dict(t="議員の言葉", v="史上最大の死者", c=J.ALERT)],
            sub="出典：国会会議録（1974年3月4日）")),
    ),

    # タラップの乗客と同型機（C4・CC0・全画面・ニース 1973年）。立会人＝仏 p6〜p7「observateurs accrédités
    #   britanniques et japonais」
    "c804": dict(
        t="乗客に多かった2つの国",
        s="タラップの乗客と同じ型の機体（KLM）　1973年・ニース",
        photo=P("klm_nice_1973"), **ss.kind(P("klm_nice_1973")),
        side="right", ann_y=330,
        ann=[dict(t="調査の立会人", d="イギリスと日本", dc=J.AMBER)],
    ),

    # 日本人の乗客（facts_japan C1：3/5 運輸大臣「日本人が四十九名、一名はまだ確認されていない」＝確認ずみ48）。数を合わせる
    "c805": dict(
        t="日本人の乗客の人数",
        s="運輸大臣の答弁（事故の2日後）",
        fig=("icons", dict(
            n=49, on=48, kind="person", cols=10, oncol=J.AMBER,
            lead="3月5日の答弁　色＝確かめられた人（48人）",
            note="出典：国会会議録（1974年3月5日・衆議院 運輸委員会）")),
    ),

    # 同じ旅行の一行（facts_japan C2・3/4 運輸大臣）
    "c806": dict(
        t="まとまった一団",
        s="国会での説明",
        fig=("panel", dict(
            blocks=[dict(k="乗客の多く", t="同じ旅行の一行", c=J.AMBER),
                    dict(k="説明した人", t="運輸大臣", v="事故の翌日の国会", c=J.INST)],
            note="出典：国会会議録（1974年3月4日）", cols=2)),
    ),

    # 🔴 決め所⑭（台本 §2 #14・国会 p6007＝公式の文字データ・頁の画像なし）＝引用札
    "c807": dict(
        t="まだ入社前の人たち",
        s="事故の翌日の答弁",
        fig=("quote", dict(
            phrase="入社内定者の、ヨーロッパの研修旅行",
            who="運輸大臣 徳永正利",
            when="1974年3月4日",
            doc="国会会議録（予算委員会）")),      # 「（衆議院 予算委員会）」は語の途中で折り返した（check_wrap）
    ),

    # 一行の内訳（facts_japan C2：東海銀行16＋中央信託銀行6＝22・トーメン入社予定者15・千代田生命1＝台本 §9）。
    #   会社名は出さない。棒は値に比例（1：22＝下限 4.5% の内）
    "c808": dict(
        t="一行の内訳",
        s="大臣の答弁を足した数",
        fig=("compare", dict(
            items=[dict(v=22, t="銀行", c=J.AMBER),
                   dict(v=15, t="商社に入る人", c=J.LINE),
                   dict(v=1, t="生命保険", c=J.LINE)],
            unit="人",
            note="出典：国会会議録（1974年3月4日・運輸大臣の答弁）")),
    ),

    # 正式な社員でない（facts_japan C2・3/12 議員）
    "c809": dict(
        t="社員になる前",
        s="事故の9日後の国会",
        fig=("beforeafter", dict(
            a=dict(k="入社", t="決まっていた", lines=["内定"], v="", c=J.LINE),
            b=dict(k="身分", t="社員ではない", lines=["補償が難しい"], v="", c=J.ALERT),
            arrow=False, note="出典：国会会議録（1974年3月12日・議員の質問）")),
    ),

    # 補償の見通し（facts_japan C3：3/4・3/12 外務大臣）。⚠️「一切加盟していない」は言い過ぎ＝画面では言わない
    "c810": dict(
        t="補償の見通し",
        s="外務大臣の答弁",
        fig=("people", dict(
            nodes=[dict(x=0.22, y=0.32, t="遺族の側の弁護士", kind="person", c=J.INST),
                   dict(x=0.78, y=0.32, t="トルコ航空の側の弁護士", kind="person", c=J.AMBER),
                   dict(x=0.50, y=0.80, t="日本政府", d="大使館を通す", kind="org", c=J.LINE)],
            edges=[dict(a=0, b=1, t="運送契約", c=J.AMBER), dict(a=2, b=1, t="", c=J.LINE)], pair=True,
            note="出典：国会会議録（1974年3月4日・12日）")),
    ),

    # 政府の支え（facts_japan C3・3/4 外務大臣）
    "c811": dict(
        t="横からの支え",
        s="政府の答弁",
        fig=("panel", dict(
            blocks=[dict(k="政府", t="弁護士選びなどを支える", c=J.INST),
                    dict(k="パリの日本大使館", t="連絡事務所", c=J.AMBER)],
            note="出典：国会会議録（1974年3月4日）", cols=2)),
    ),

    # 羽田に帰った遺族（国会 p6028・3/12 議員）
    "c812": dict(
        t="羽田に帰った遺族",
        s="議員が伝えたこと",
        fig=("moment", dict(
            clock="3月11日", label="夜　羽田空港",
            facts=[dict(t="帰ってきた人たち", v="遺族", c=J.INST)],
            sub="出典：国会会議録（1974年3月12日・議員の発言）")),
    ),

    # 身元の確認（仏 p108）
    "c813": dict(
        t="備えの足りなさ",
        s="フランスの報告書から",
        fig=("panel", dict(
            blocks=[dict(k="身元の確認", t="大きな困難", c=J.ALERT),
                    dict(k="報告書の勧告", t="大型機の時代の備え", v="パリの設備の不足から", c=J.AMBER)],
            note=f"{NOTE_FR} PDF 108頁", cols=2)),
    ),

    # 慰霊の名前の壁（B2・CC BY 4.0・全画面）。🔴 名前にモザイク（元画像を直した＝`ss.NEEDS_MASK`）
    "c814": dict(
        t="刻まれた名前",
        s="慰霊の名前の壁　1997年",
        photo=P("names_wall"), **ss.kind(P("names_wall")),
    ),

    # 上院の報告の表紙（p2005・1974年6月）＝引用＝額装・原色。図書館の受け入れ印は切り出しで落とした
    "c815": dict(
        t="3か月後の報告",
        s="米上院の報告の表紙（1974年6月）",
        photo=ss.page(2005), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="題", d="DC-10の聞き取りと調査の報告", dc=J.TICK),
             dict(t="委員会", d="上院の商業委員会", dc=J.INST)],
    ),

    # 英訳の表紙（p1001・AIB 8/76）＝引用＝額装・原色
    "c816": dict(
        t="英語の訳",
        s="英訳の表紙（1976年）",
        photo=ss.page(1001), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="出した所", d="イギリスの事故調査局", dc=J.INST),
             dict(t="報告書の番号", v="8/76", vc=J.TICK)],
    ),

    # 付属書の表紙（仏 p109・1976年2月）＝引用＝額装・原色
    "c817": dict(
        t="音声と供述の記録",
        s="付属書の表紙",
        photo=ss.page(109), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="中身", d="音声の書き起こし・供述など", dc=J.AMBER),
             dict(t="日付", v="1976年2月", vc=J.TICK)],
    ),

    # 結論の節（仏 p104「5.2. CAUSES DE L'ACCIDENT」）。次の c819 が同じ頁をなぞる＝ここは頁を出さない（§5b-59）
    "c818": dict(
        t="調査委員会の答え",
        s="最終報告書（1976年2月）",
        fig=("panel", dict(
            blocks=[dict(k="まとめた所", t="フランスの事故調査委員会", c=J.INST),
                    dict(k="結論の節", t="5.2　事故の原因", c=J.ALERT)],
            note=f"{NOTE_FR} PDF 104頁", cols=2)),
    ),

    # 🔴 決め所⑮（台本 §2 #15・仏 p104）。1行のナレーション＝pre=0
    #   行の矩形は文字の層（語の箱）：「L'accident résulte de l'éjection en vol de la porte」＋「cargo arrière gauche」
    #   切り口＝見出し「5.2. CAUSES DE L'ACCIDENT」の上 〜 2行目の下の白い行（0.2109〜0.2182）
    "c819": dict(
        t="原因の一文",
        s="フランスの最終報告書（1976年）",
        fig=("trace", dict(
            page=ss.page(104),
            lines=[(0.3046, 0.1720, 0.8217, 0.1904), (0.3054, 0.1934, 0.5081, 0.2118)],
            phrase="原因は、飛行中に貨物ドアが外れたこと",
            doc="原文（PDF 104頁）　5.2 事故の原因",
            crop=(0.25, 0.10, 0.86, 0.2140))),
    ),

    # 錠：離陸の前に錠がかかっていない → それでも閉まって見える（仏 p104「ありえた」の留保＝§5b-27b）
    "c820": dict(
        t="離陸の前の錠",
        s="報告書が挙げたもと",
        fig=("latch", dict(
            start=dict(hook="short"),
            steps=[dict(state=dict(handle="down", pin="butt", tube="bent", vent="closed"),
                        tag=dict(t="錠がかかっていない", at="pin")),
                   dict(state=dict(lamp="off"), tag=dict(t="閉まって見えうる", d="設計の弱点", at="lamp"))],
            note=NOTE, src="仏の報告書 PDF 104頁")),
    ),

    # 重なった要因（仏 p104〜p105）
    "c821": dict(
        t="重なった要因",
        s="最終報告書の見立て",
        fig=("panel", dict(
            blocks=[dict(k="SB 52-37", t="一部だけ", c=J.AMBER),
                    dict(k="改修と調整", t="誤り", c=J.ALERT),
                    dict(k="オルリー", t="のぞき窓の確認なし", v="当時の窓は小さい", c=J.ALERT)],
            note=f"{NOTE_FR} PDF 104〜105頁", cols=3)),
    ),

    # 章の橋（副題は10本目からの型「ここまでと、この先」）。仏 p105
    "c822": dict(
        t="何が変わったか",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="報告書が挙げた危険", t="床の逃げ道が小さい", v="ケーブルは全部床下", c=J.ALERT),
                    dict(k="鍵", t="パリのあと、変わったこと", v="第9章", c=J.AMBER)],
            cols=2)),
    ),

}
