# -*- coding: utf-8 -*-
"""第2章 その日のオルリー c201–c222（22カット）。13本目（トルコ航空981便）。⑤b-3（2026-09-25）で書いた。

⚠️ 12本目の中身は `git show 3832147:tools/cuts/c2.py`（⑤b-1 で空にした）。

■ 写真 5/22（事故機 A1＝BY-SA 額装・同型機 D5・D6・C2・1970年ごろの出発ロビー O1＝BY-SA 額装）
■ 🔴 Googleアース（台本の c201・c204）は使わない（⑤b-3 の決め）：取り方・表示の置き方が未定
   ＝1通目「決まらなければ地図か紙面で代える」。c201＝動く地図（`ss.europe_map`）・c204＝時刻の型（moment）
■ 🔴 地上係員と同乗の整備士は**役割だけ**（台本 §1-2）。供述の紙面（p144〜p149）は出さない
   ＝決め所 c212・c214 は引用札（quote）。供述の中身は工程（c210）と柱（c211）で
■ 画面の時刻は「11:02」の形・パリの時刻（ルール B1・台本 §1-4）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
NOTE_FR = "出典：フランスの最終報告書"
# 🔴 ⑤b-3（09-25）：画面の頁は**PDF の頁**（自動の出典の札「PDF 91頁」と同じ書き方）。台本の通し番号は出さない
NOTE_FRP = NOTE_FR + " PDF"

SPEC = {

    # 🔴 動く地図（Googleアースの代わり）：イスタンブール→パリ（オルリー）→ロンドン（仏 p9）
    "c201": dict(
        t="パリは、途中の空港",
        s="981便の経路",
        fig=ss.europe_map([
            dict(move=[dict(kind="path", via=["istanbul", "orly"], sec=3.0)],
                 tag=dict(at="istanbul", t="出発", side="above")),
            dict(move=[dict(kind="path", via=["orly", "london"], sec=1.2)],   # r03：1.5秒だと92%の1枚でまだ着いていない
                 tag=dict(at="london", t="行き先", side="right"))]),
    ),

    # 事故機 TC-JAV の地上走行（CC BY-SA 2.0＝額装・原色・1点1カット・注記を重ねない）
    "c202": dict(
        t="まだ新しい機体",
        s="事故機 TC-JAV の地上走行　1973年・ロンドン",
        photo=P("tcjav_taxi"), panel=True, color=1.0,
    ),

    # 姉妹機 TC-JAU（CC BY 3.0・1054px＝額装パネル）。事故の後の写真（1974年7月）＝副題に年月
    # ⚠️ 見出しに「3機」を入れない（注記の答えと同じ＝check_wording A）
    "c203": dict(
        t="同じ型を、まとめて",
        s="同じ型のトルコ航空機 TC-JAU　1974年7月・フランクフルト",
        photo=P("tcjau_fra_1974"), **ss.kind(P("tcjau_fra_1974")),
        side="right", ann_y=330,
        ann=[dict(t="トルコ航空の注文", v="3機", vc=J.AMBER)],
    ),

    # 🔴 Googleアースの代わり＝時刻の型。3行＝時計・札2つ（仏 p9）
    "c204": dict(
        t="時刻表どおりの到着",
        s="3月3日の午前（パリの時刻）",
        fig=("moment", dict(
            clock="11:02", label="981便　パリに着く",
            facts=[dict(t="止めた場所", v="南ターミナルの西　A2", c=J.AMBER),
                   dict(t="パリで降りた人", v="50人", c=J.TICK)],
            sub=f"{NOTE_FRP}9頁")),
    ),

    # 2行＝柱2本。「200人あまり」＝仏 p9（217）と p46（216）が割れる（台本 §1-4）
    "c205": dict(
        t="満席に近づく",
        s="パリで新たに加わった客",
        fig=("panel", dict(
            blocks=[dict(k="乗った人", t="200人あまり", c=J.AMBER),
                    dict(k="回ってきた客", t="英国航空・エールフランスの便から", c=J.LINE)],
            note=f"{NOTE_FRP}9頁・46頁", cols=2)),
    ),

    # 同型機と乗客（フィンエアー・CC BY 4.0・縦長＝額装パネル）。⚠️ 撮影年は不明＝副題に年を書かない
    "c206": dict(
        t="停留が延びた日",
        s="同じ型の機体と乗客（フィンエアー）",
        photo=P("finnair_dc10"), **ss.kind(P("finnair_dc10")),
        side="right", ann_y=330,
        ann=[dict(t="ふだんの停留", v="1時間", vc=J.TICK),
             dict(t="この日", v="1時間30分", vc=J.AMBER),
             dict(t="客室の席", v="ほぼ満席", vc=J.AMBER)],
    ),

    # 駐機場の同型機と荷物車（KLM・1972年・CC0・全画面）
    # ⚠️ 副題は②の見本（640px）の記録から。⑤c で原寸で見て確かめる（§5b-19）
    "c207": dict(
        t="出発までの作業",
        s="駐機場の同じ型の機体（KLM）　1972年・アムステルダム",
        photo=P("klm_apron_1972"), **ss.kind(P("klm_apron_1972")),
        side="right", ann_y=330,
        ann=[dict(t="荷物", d="積み下ろし", dc=J.TICK),
             dict(t="燃料", d="補給", dc=J.TICK),
             dict(t="後ろの左の貨物室", d="下ろすだけ", dc=J.AMBER)],
    ),

    # 床下の貨物ドア3つ（SB 52-37 の本文「forward, center, and aft cargo doors」p5003）
    #   後ろが左側なのは仏の報告書（porte cargo arrière gauche）。前と真ん中の左右は資料に無い＝描かない
    "c208": dict(
        t="ドアは3つ",
        s="機体の床下にある荷物の部屋",
        fig=("panel", dict(
            lead="貨物室のドアの位置",
            blocks=[dict(k="1", t="前", c=J.LINE),
                    dict(k="2", t="真ん中", c=J.LINE),
                    dict(k="3", t="後ろの左側", c=J.ALERT)],
            note="出典：ダグラス社のSB 52-37（1972年）・フランスの最終報告書")),
    ),

    # 1970年ごろの出発ロビー（CC BY-SA 4.0＝額装・原色・1点1カット・注記を重ねない）
    "c209": dict(
        t="閉めたのは、荷物の係員",
        s="1970年ごろのパリの空港の出発ロビー",
        photo=P("orly_hall_1970"), panel=True, color=1.0,
    ),

    # 係員の供述（1974年3月6日・仏 p144〜p145）。紙面は出さない（台本 §1-2）＝手順を工程で
    "c210": dict(
        t="3日後の供述",
        s="ドアを閉めた係員の話（1974年3月6日）",
        fig=("process", dict(
            steps=[dict(t="ボタンを押す", d="電気でドアが下りる", c=J.LINE),
                   dict(t="カチッと鳴る", d="ドアが収まる", c=J.LINE),
                   dict(t="レバーを倒す", d="錠をかける", c=J.AMBER)],
            note=f"{NOTE_FR}の付属書（供述）")),
    ),

    # 補足の供述（仏 p147〜p148「sans plus d'effort que d'habitude」）
    "c211": dict(
        t="立つ位置を変えた",
        s="係員の供述の補足",
        fig=("panel", dict(
            blocks=[dict(k="はじめ", t="立つ位置が悪かった", c=J.TICK),
                    dict(k="そこで", t="少し動いてから閉めた", c=J.LINE),
                    dict(k="力", t="いつもより強くはない", c=J.AMBER)],
            note=f"{NOTE_FR}の付属書")),
    ),

    # 🔴 決め所②（台本 §2 #2・仏 p145「Je suis formel, la porte était bien fermée」）
    "c212": dict(
        t="閉めた本人の確信",
        s="事故の3日後の供述",
        fig=("quote", dict(
            phrase="断言する、ドアはきちんと閉まっていた",
            who="ドアを閉めた係員",
            when="1974年3月6日",
            doc="供述の記録（報告書の付属書）")),
    ),

    # のぞき窓（仏 p94・上院 p2035）。窓の写真は第3章 c310（p94）＝ここは柱で
    "c213": dict(
        t="ピンを見る、のぞき窓",
        s="貨物ドアの錠の確かめ方",
        fig=("panel", dict(
            blocks=[dict(k="場所", t="ドアの下", c=J.LINE),
                    dict(k="見えるもの", t="中のピン", c=J.AMBER)],
            note=f"{NOTE_FRP}94頁・米上院の報告 PDF 35頁", cols=2)),
    ),

    # 🔴 決め所③（台本 §2 #3・仏 p149「Je ne savais pas à quoi cet oeil servait」）。日付は文字の層に無い＝「いつ」を置かない
    "c214": dict(
        t="係員と、のぞき窓",
        s="補足の供述",
        fig=("quote", dict(
            phrase="あの小窓が何のためか、知らなかった",
            who="ドアを閉めた係員",
            doc="供述の補足（報告書の付属書）")),
    ),

    # 有る（閉め方は見せて教わった）／無い（文書の指示・のぞき窓）＝仏 p148・p149
    "c215": dict(
        t="教わっていないこと",
        s="係員が受けていた指示",
        fig=("absent", dict(
            mode="pair",
            items=[dict(t="閉め方", d="職長が見せて教えた", ok=True, c=J.LINE, n=1),
                   dict(t="のぞき窓のこと", d="誰からも教わらず", ok=False, c=J.ALERT, n=0)],
            note=f"{NOTE_FR}の付属書（供述の補足）")),
    ),

    # 仏 p46・p156〜p157（主任整備士の話）。名前は出さない（役割だけ）
    "c216": dict(
        t="窓を見ていた人",
        s="ふだんの手順",
        fig=("panel", dict(
            blocks=[dict(k="確かめる人", t="トルコ航空の主任整備士", v="オルリーに駐在", c=J.INST),
                    dict(k="本人の話", t="毎便確かめていた", c=J.LINE),
                    dict(k="窓の中のピン", t="白く光り、よく見える", c=J.AMBER)],
            note=f"{NOTE_FRP}46頁・付属書")),
    ),

    # 仏 p23・p46・p151
    "c217": dict(
        t="確かめ役の、いない日",
        s="職長の話と、当日の勤務",
        fig=("panel", dict(
            blocks=[dict(k="荷物の会社の職長", t="確かめはときどき", c=J.TICK),
                    dict(k="3月3日", t="主任整備士は不在", v="研修でイスタンブール", c=J.ALERT)],
            note=f"{NOTE_FRP}23頁・46頁・付属書", cols=2)),
    ),

    # 仏 p23・p46（「整備士も、ほかの乗員も、確かめるのを見た人はいない」＝確かめなかったとは書いていない）
    "c218": dict(
        t="代わりの整備士",
        s="イスタンブールから乗ってきた乗員",
        fig=("panel", dict(
            blocks=[dict(k="代わり", t="同乗の整備士", v="同じ機体で来ていた", c=J.LINE),
                    dict(k="閉めたあと", t="窓の確かめ", v="見た人はいない", c=J.ALERT)],
            note=f"{NOTE_FRP}23頁・46頁", cols=2)),
    ),

    # 仏 p46・p18。「はず」の留保は答えに残す（§5b-27b）
    "c219": dict(
        t="足場が要る窓",
        s="報告書の本文の指摘",
        fig=("panel", dict(
            blocks=[dict(k="報告書", t="作業のあとで窓をのぞく", v="足場が要ったはず", c=J.AMBER),
                    dict(k="同乗の整備士", t="981便の乗員", v="乗員12人の1人", c=J.LINE)],
            note=f"{NOTE_FRP}18頁・46頁", cols=2)),
    ),

    # 時刻の流れ（仏 p9・p10）。軸は11:00からの分
    "c220": dict(
        t="昼、東へ飛び立つ",
        s="3月3日の時刻（パリの時刻）",
        fig=("timeline", dict(
            events=[dict(t=2, top="11:02", t2="着く", c=J.LINE),
                    dict(t=35, top="11:35ごろ", t2="ドアを閉める", c=J.AMBER),
                    dict(t=90.5, top="12:30:30", t2="離陸", c=J.ALERT, big=True)],
            t0=-4, t1=100,
            ticks=[(0, "11:00"), (30, "11:30"), (60, "12:00"), (90, "12:30")],
            band=[dict(a=35, b=90.5, t="およそ55分", c=J.AMBER)],
            src=f"{NOTE_FRP}9頁・10頁")),
    ),

    # 仏 p46（本文が記す係員の言葉）
    "c221": dict(
        t="本人の手ごたえ",
        s="報告書の本文が記す係員の言葉",
        fig=("panel", dict(
            blocks=[dict(k="閉め方", t="いつもどおり", c=J.LINE),
                    dict(k="困ったこと", t="特に無し", c=J.LINE),
                    dict(k="おかしな所", t="気づかなかった", c=J.AMBER)],
            note=f"{NOTE_FRP}46頁")),
    ),

    # 章の橋（副題は10本目からの型「ここまでと、この先」）
    "c222": dict(
        t="閉まって見えた理由へ",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="係員", t="いつもの閉め方", c=J.LINE),
                    dict(k="鍵", t="錠の仕組み", v="第3章", c=J.AMBER)],
            cols=2)),
    ),

}
