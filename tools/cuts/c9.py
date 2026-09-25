# -*- coding: utf-8 -*-
"""第9章 その後 c901–c920（20カット）。13本目（トルコ航空981便）。⑤b-4（2026-09-25）で書いた。

⚠️ 12本目の中身は `git show 3832147:tools/cuts/c9.py`（⑤b-1 で空にした）。
⚠️ 見出し・副題に章名「その後」を入れない（§5b-46）。

■ 写真 5/20（官報 p4301・AD p4101・p4201・p4001＝米国の職務著作＝額装・原色／石碑 B4＝額装パネル）
■ 決め所 c911（仏 p107）はなぞる型（trace）
■ 断面（section）＝c908（床の空気の逃げ道＝AD 75-15-05・`vent="open"`）。錠（latch）＝c916（ふり返り）
■ 台本 §7 から替えたところ（⑤b-4 の決め）
  c901：官報 p4301 の紙面 → 日付の図（moment）。官報の頁は次の c902 に当てた（同じ紙面を2カット続けない＝§5b-59）
  c902：官報 p4301 の**2段目**（「Install a support and plate on the aft cargo door … SB 52-37」「Prior to each flight,
        a flight crewmember shall — Check each cargo door … by visual check through inspection ports」）＝ナレーションそのもの
  c908：FedEx の動く映像（取るにはダウンロードの許可が要る）→ 断面の床の逃げ道。題に【映像あり】は付けない回（台本 §1-1）
  c914：🔧 §7 の「図に」→ AD 74-08-04 の頁（改正の履歴の4行＝39-1811 に 2013・2112・2399・2443 を書き足し）
■ c920＝コメントの問い（共通エンディング ed01 の直前・13本目から）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
NOTE_FR = "出典：フランスの最終報告書"
NOTE = "模式図：4つのフックのうち1つ。形と大きさは実物どおりではない（報告書の図7の順番）"
SEC_NOTE = "模式図：機体を後ろから見た断面。形と大きさは実物どおりではない"

SPEC = {

    # 事故の4日後の電報の命令（官報 p4301「telegrams dated March 7, 1974」）。1年9か月＝台本 §9
    "c901": dict(
        t="電報で出た命令",
        s="パリの事故のあと",
        fig=("moment", dict(
            clock="3月7日", label="1974年　事故の4日後",
            facts=[dict(t="FAAの命令", v="電報で航空会社へ", c=J.ALERT),
                   dict(t="ウィンザーの事故から", v="1年9か月", c=J.AMBER)],
            sub="出典：官報 1974年4月2日（11992頁）")),
    ),

    # 官報 p4301 の2段目＝引用（米国の職務著作）＝額装・原色
    "c902": dict(
        t="初めての命令",
        s="官報に載った命令の本文（1974年4月2日の号）",
        photo=ss.page(4301), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="SB 52-37", d="支えと板も命令に", dc=J.AMBER),
             dict(t="毎回の飛行の前", d="乗員がのぞき窓で確かめる", dc=J.ALERT),
             dict(t="命令になったSB", v="7つ", vc=J.TICK, d="のちの改正も含めて")],
    ),

    # 3/3 パリ → 3/7 電報 → 3/27・28 運輸省の答弁（facts_japan C5）→ 4/2 官報（p4301「effective as to those persons April 2, 1974」）
    "c903": dict(
        t="だれにでも効く日",
        s="1974年3〜4月",
        fig=("timeline", dict(
            events=[dict(t=3, top="3月3日", t2="パリ", c=J.ALERT),
                    dict(t=7, top="3月7日", t2="電報で命令", c=J.AMBER),
                    dict(t=27.5, top="3月27〜28日", t2="運輸省の答弁", c=J.LINE),
                    dict(t=33, top="4月2日", t2="官報に載る", c=J.AMBER, big=True)],
            t0=0, t1=36,
            ticks=[(1, "3月1日"), (16, "3月16日"), (32, "4月1日")],
            src="官報 1974年4月2日・国会会議録（1974年3月27日・28日）")),
    ),

    # AD 74-12-07（p4101＝改正 39-1923 の版）＝引用＝額装・原色。7月に5つの SB（AD p4101〜p4102）
    "c904": dict(
        t="通気扉とのぞき窓も",
        s="1974年7月の命令（のちの改正の版）",
        photo=ss.page(4101), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="命令の番号", v="AD 74-12-07", vc=J.AMBER),
             dict(t="義務になったSB", v="さらに5つ", vc=J.ALERT)],
    ),

    # AD 75-15-05（p4201＝改正 39-2739 の版・「compliance is required on or before December 31, 1977」）＝引用＝額装・原色
    "c905": dict(
        t="床にも命令",
        s="床を強くする命令（1975年）",
        photo=ss.page(4201), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="求めたこと", d="床が崩れない", dc=J.AMBER),
             dict(t="期限", d="1977年の終わり（改正のあと）", dc=J.ALERT)],
    ),

    # 穴の大きさ（AD p4202「20 square feet」×0.0929＝1.86㎡＝台本 §9）
    "c906": dict(
        t="床に開く穴の大きさ",
        s="命令が考えた穴",
        fig=("panel", dict(
            blocks=[dict(k="考える穴", t="約1.86平方メートル", v="20平方フィート", c=J.AMBER),
                    dict(k="くらべると", t="畳1枚より少し大きい", c=J.LINE)],
            note="出典：AD 75-15-05 PDF 2頁", cols=2)),
    ),

    # 対象の4機種（p4201「McDonnell Douglas Model DC-10 Series, Lockheed Model L-1011 Series, Boeing Model B-747
    #   Series, and Airbus Industrie Model A-300 Series Airplanes」）。数を合わせる
    "c907": dict(
        t="4つの機種に及ぶ",
        s="床の命令の対象",
        fig=("icons", dict(
            n=4, on=[0], kind="plane", cols=4, oncol=J.AMBER,
            labels=["DC-10", "L-1011", "747", "A300"],
            lead="ダグラス・ロッキード・ボーイング・エアバス",
            note="出典：AD 75-15-05 PDF 1頁　色＝事故と同じ型")),
    ),

    # 🔴 断面：床の空気の逃げ道（AD 75-15-05＝vent open）。ドアが外れて貨物室の空気が抜けても、床は落ちない
    #   NTSB の2つ目の勧告（1972年・上院 p2047）も客室と貨物室のあいだの逃げ道
    "c908": dict(
        t="床に逃げ道を",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            start=dict(vent="open"),
            steps=[dict(state=dict(door="gone", air="out"),
                        tag=dict(t="床の空気の逃げ道", d="上と下の気圧をそろえる")),
                   dict(tag=dict(t="1972年のNTSBの勧告", d="2つ目も、この逃げ道"))],
            note=SEC_NOTE, src="AD 75-15-05 PDF 2頁・米上院の報告 PDF 47頁")),
    ),

    # フランスの報告書の勧告（仏 p106〜p108）
    "c909": dict(
        t="フランスの5つの勧告",
        s="1976年の最終報告",
        fig=("panel", dict(
            blocks=[dict(k="勧告の数", t="5つ", c=J.INST),
                    dict(k="1つ目", t="改修を義務に", v="同じ型の全機に早く", c=J.AMBER)],
            note=f"{NOTE_FR} PDF 106〜108頁", cols=2)),
    ),

    # ウィンザーのあとの対応（仏 p107「les mesures préconisées n'étaient pas impératives et l'attention des intéressés
    #   n'a pas été convenablement attirée」）。3つとも「無い」＝ledger
    "c910": dict(
        t="欠けていた3つ",
        s="勧告の振り返り",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="AD", d="使われず", ok=False, c=J.ALERT),
                   dict(t="対策", d="義務にならず", ok=False, c=J.ALERT),
                   dict(t="関係者への注意", d="足りず", ok=False, c=J.ALERT)],
            lead="ウィンザーのあとの対応",
            note=f"{NOTE_FR} PDF 107頁")),
    ),

    # 🔴 決め所⑯（台本 §2 #16・仏 p107）。2行のナレーション＝pre=0
    #   行の矩形は文字の層（語の箱）：「la procédure impérative des "con-」＋「signes de navigabilité", quelles qu'en soient
    #   les incidences」＋「financières, soit choisie」。切り口＝段落の上下の白い行（0.7192〜0.7344・0.8218〜0.8370）の真ん中
    "c911": dict(
        t="費用より安全を",
        s="フランスの最終報告書の勧告",
        fig=("trace", dict(
            page=ss.page(107),
            lines=[(0.5785, 0.7395, 0.9087, 0.7578), (0.2886, 0.7607, 0.8891, 0.7790),
                   (0.2878, 0.7819, 0.5384, 0.8002)],
            phrase="費用がどうであれ、強制の命令を選ぶこと",
            doc="原文（PDF 107頁）",
            crop=(0.27, 0.7268, 0.93, 0.8294))),
    ),

    # ほかの勧告（仏 p106〜p107）。「pouvait ne pas être suffisante」の留保を残す（§5b-27b）
    "c912": dict(
        t="ほかの勧告",
        s="訓練と、操縦の通り道",
        fig=("panel", dict(
            blocks=[dict(k="訓練", t="国が認めた細かい計画で", c=J.INST),
                    dict(k="二重の操縦", t="壊れうる場所に集まると", v="足りないことがある", c=J.ALERT)],
            note=f"{NOTE_FR} PDF 106〜107頁", cols=2)),
    ),

    # 検査のはんこ（上院 p2053）
    "c913": dict(
        t="はんこの見直し",
        s="ダグラス社の対策",
        fig=("panel", dict(
            blocks=[dict(k="はんこの数", t="減らす", c=J.AMBER),
                    dict(k="持つ人", t="半年ごとに署名", c=J.INST)],
            note="出典：米上院の報告 PDF 53頁", cols=2)),
    ),

    # AD 74-08-04（p4001＝改正 39-2443 の版）の改正の履歴＝引用＝額装・原色。52-37 の遅れ＝上院 p2055
    "c914": dict(
        t="重ねられた改正",
        s="貨物ドアの命令の改正の記録",
        photo=ss.page(4001), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="書き足し", v="4回", vc=J.AMBER, d="1975年の終わりまで"),
             dict(t="52-37が遅れた機体", d="アメリカにも少なくとも1機", dc=J.ALERT)],
    ),

    # 森の中の石碑（B4・CC BY 3.0・729px＝額装パネル）
    "c915": dict(
        t="森に立つ石碑",
        s="森の中の慰霊碑　2010年",
        photo=P("monument_2010"), **ss.kind(P("monument_2010")),
    ),

    # ふり返り①：錠（第3章 c316・c317 の絵が戻る）
    "c916": dict(
        t="見かけだけの「閉」",
        s="ふり返り　1つ目",
        fig=("latch", dict(
            start=dict(hook="short"),
            steps=[dict(state=dict(handle="down", pin="butt", tube="bent", vent="closed"),
                        tag=dict(t="係員の目には「閉」", at="handle")),
                   dict(state=dict(lamp="off"), tag=dict(t="操縦室の灯りも消える", at="lamp"))],
            note=NOTE, src="仏の報告書 PDF 104頁")),
    ),

    # ふり返り②
    "c917": dict(
        t="見えていた弱点",
        s="ふり返り　2つ目",
        fig=("beforeafter", dict(
            a=dict(k="2年近く前", t="弱点が見えた", lines=["ウィンザーの事故"], v="", c=J.AMBER),
            b=dict(k="直す手立て", t="約束に任せた", lines=["命令にしなかった"], v="", c=J.ALERT),
            arrow=True)),
    ),

    # ふり返り③
    "c918": dict(
        t="記録と実物",
        s="ふり返り　3つ目",
        fig=("panel", dict(
            blocks=[dict(k="記録", t="板は付いていたはず", c=J.LINE),
                    dict(k="実物", t="板は無かった", v="調整にも誤り", c=J.ALERT)],
            cols=2)),
    ),

    # ふり返り④：346人（仏 p18）・日本人と確かめられた乗客48人（国会 3/5）。数を合わせる
    "c919": dict(
        t="346人、それぞれの旅",
        s="ふり返り　4つ目",
        fig=("icons", dict(
            n=346, on=48, kind="person", cols=35, oncol=J.AMBER,
            lead="乗っていた346人　色＝日本人と確かめられた乗客（48人）",
            note="出典：フランスの最終報告書 PDF 18頁・国会会議録（1974年3月5日）")),
    ),

    # コメントの問い（13本目から・ed01 の直前）。「この動画」は楽屋の言葉＝画面に出さない
    "c920": dict(
        t="あなたなら、どうする",
        s="コメント欄で聞かせてください",
        fig=("panel", dict(
            blocks=[dict(k="問い1", t="どこで防げたか", c=J.AMBER),
                    dict(k="問い2", t="命令か、約束か", v="あなたが決めるなら", c=J.ALERT)],
            cols=2)),
    ),

}
