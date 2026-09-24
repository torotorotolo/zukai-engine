# -*- coding: utf-8 -*-
"""第4章 予兆 c401–c426（26カット）。13本目（トルコ航空981便）。⑤b-3（2026-09-25）で書いた。

⚠️ 12本目の中身は `git show 3832147:tools/cuts/c4.py`（⑤b-1 で空にした）。

■ 写真 4/26（N103AA 1977年・AA96 のドアの跡・NTSB の報告書の頭 p2017・AA の DC-10 1974年）
■ 台本 §7 から替えたところ（⑤b-3 の決め）
  c401：1971年の CM（動く素材・320×240）は**未取得**（取るのは許可が要る＋小窓の映像の作りが未検証）
        → N103AA そのものの写真（A5・1977年）。台本では c408 に当てていた点＝c408 は日付の柱に
  c403：上院 p2014 の紙面 → **胴体の断面**（次の c404 が同じ頁の同じ段をなぞる＝同じ紙面が2カット続くのを避けた）
  c412：Googleアース（取り方が未定）→ **AA96 の地図**（`ss.aa96_map`）。c418 で同じ地図が戻る（空港へ帰る）
■ 胴体の断面（section）＝c403・c405（1970年の地上の試験）・c416・c417（ウィンザー）・c426（床の逃げ道）
■ 決め所 c404（上院 p2014）・c423（上院 p2017＝NTSB の報告の再録）はなぞる型（trace）
■ 画面の時刻は**アメリカ東部の時刻**（上院 p2017 の注）＝c412 の副題で断る。形は「19:20」（ルール B1）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
NOTE_SEN = "出典：米上院の報告"
SEC_NOTE = "模式図：機体を後ろから見た断面。形と大きさは実物どおりではない"
SEC_NOTE_POS = "模式図：機体を後ろから見た断面。ドアの位置・形・大きさは実物どおりではない（この試験は前の貨物ドア）"
AA96_S = "96便の飛んだ道（アメリカ東部の時刻）"

SPEC = {

    # N103AA そのもの（CC BY 2.0・1977年＝2つの事故のあと＝副題に年）。台本 §7 は c408 に当てていた
    "c401": dict(
        t="のちの、ドアの事故の機体",
        s="N103AA そのもの　1977年・サンフランシスコ",
        photo=P("n103aa_1977"), **ss.kind(P("n103aa_1977")),
        side="right", ann_y=330,
        ann=[dict(t="アメリカン航空が受け取る", v="1971年7月28日", vc=J.AMBER)],
    ),

    # 年表：1970年の試験 → 1972年3月 → 1972年6月（ウィンザー）→ 1974年3月（パリ）
    "c402": dict(
        t="パリの前に、3回",
        s="貨物ドアの年表（1970〜1974年）",
        fig=("timeline", dict(
            events=[dict(t=1970.41, top="1970年5月", t2="地上の試験", c=J.AMBER),
                    dict(t=1972.17, top="1972年3月", t2="閉まらない", c=J.AMBER),
                    dict(t=1972.45, top="1972年6月", t2="ウィンザー", c=J.ALERT),
                    dict(t=1974.17, top="1974年3月", t2="パリ", c=J.ALERT, big=True)],
            t0=1969.8, t1=1974.6,
            ticks=[(1970, "1970"), (1971, "1971"), (1972, "1972"), (1973, "1973"), (1974, "1974")],
            src=f"{NOTE_SEN} 2014〜2015頁・2017頁")),
    ),

    # 🔴 断面：1970年の地上の試験（組み立て中の胴体1号機・前の貨物ドアが開く）。与圧 push ⇒ ドア on
    "c403": dict(
        t="地上で開いたドア",
        s="1970年5月29日の試験",
        fig=("section", dict(
            steps=[dict(state=dict(press="push"), tag=dict(t="空気を詰める", d="組み立て中の胴体1号機")),
                   dict(state=dict(press="none", door="gone", air="out"), tag=dict(t="前の貨物ドアが開く"))],
            note=SEC_NOTE_POS, src="米上院の報告 p2014")),
    ),

    # 🔴 決め所⑤（台本 §2 #5・上院 p2014）。切り口は画素の白い行（1970年の段＋設計の変更の段＋1行）
    "c404": dict(
        t="メーカーの説明",
        s="議会の報告に残る一文",
        fig=("trace", dict(
            page=ss.page(2014),
            lines=[(0.5729, 0.4702, 0.8920, 0.4848), (0.1398, 0.4826, 0.8496, 0.4972)],
            phrase="錠が不完全で、ドアは機内の圧力で開いた",
            doc="米上院の報告 2014頁の原文",
            crop=(0.12, 0.4555, 0.91, 0.5825))),
    ),

    # 🔴 断面：床が傷む → すべての貨物ドアに通気扉（上院 p2014「all cargo doors were redesigned to incorporate a vent door」）
    "c405": dict(
        t="試験のあとの設計の変更",
        s="1970年の試験で起きたこと",
        fig=("section", dict(
            start=dict(door="gone", air="out"),
            steps=[dict(state=dict(floor="push"), tag=dict(t="床が傷む", d="ドアの近くで")),
                   dict(tag=dict(t="通気扉を付ける", d="すべての貨物ドアに"))],
            note=SEC_NOTE_POS, src="米上院の報告 p2014")),
    ),

    # 立ち会いは無い（上院 p2014・西部地域局長の証言）
    "c406": dict(
        t="役所のいない試験",
        s="西部地域局長の証言",
        fig=("absent", dict(
            mode="single",
            items=[dict(t="FAAの立ち会い", d="無し", ok=False, c=J.ALERT)],
            lead="1970年5月の地上の試験",
            note=f"{NOTE_SEN} 2014頁")),
    ),

    # 2つ目（1972年3月3日・上院 p2015）
    "c407": dict(
        t="閉まらなかったドア",
        s="2つ目の出来事",
        fig=("moment", dict(
            clock="3月3日", label="1972年",
            facts=[dict(t="後ろの貨物ドア", v="電気で閉まらない", c=J.ALERT)],
            sub=f"{NOTE_SEN} 2015頁")),
    ),

    # その場の手当てと、日付の重なり（1972年3月3日＝パリの事故のちょうど2年前）
    "c408": dict(
        t="その場の手当て",
        s="N103AA の貨物ドアの直し",
        fig=("panel", dict(
            blocks=[dict(k="直し方", t="手で閉め、スイッチを調整", c=J.LINE),
                    dict(k="日付", t="1972年3月3日", v="パリの2年前の同じ日", c=J.AMBER)],
            note=f"{NOTE_SEN} 2015頁", cols=2)),
    ),

    # 配線を太くする SB（1972年5月30日・上院 p2015）
    "c409": dict(
        t="メーカーの手当て",
        s="閉まりにくさへの改修",
        fig=("panel", dict(
            blocks=[dict(k="報告", t="電気で閉まりにくい", v="ほかの航空会社からも", c=J.TICK),
                    dict(k="1972年5月30日", t="配線を太くする改修", v="メーカーのSB", c=J.AMBER)],
            note=f"{NOTE_SEN} 2015頁", cols=2)),
    ),

    # SB＝すすめるもの（上院 p2015・SB p5003「Compliance: Recommended.」・p2055「voluntary」）
    "c410": dict(
        t="知らせであって、命令ではない",
        s="SBのしくみ",
        fig=("panel", dict(
            # ⚠️ v は飾り書体（Dela）＝漢字の長い句はつぶれる（check_layout・§5b-13）→ 句は t へ
            blocks=[dict(k="SB", t="サービス・ブレティン", v="すすめる", c=J.LINE),
                    dict(k="従うか", t="航空会社しだい", c=J.ALERT)],
            note=f"{NOTE_SEN} 2015頁・2055頁・ダグラス社のSB 52-37", cols=2)),
    ),

    # 96便の経路（上院 p2017「New York, with intermediate stops at Detroit, Michigan and Buffalo」）
    "c411": dict(
        t="1972年6月12日の96便",
        s="アメリカン航空96便の経路",
        fig=("process", dict(
            steps=[dict(t="ロサンゼルス", d="出発", c=J.LINE),
                   dict(t="デトロイト", d="寄る", c=J.AMBER),
                   dict(t="バッファロー", d="寄る", c=J.LINE),
                   dict(t="ニューヨーク", d="行き先", c=J.LINE)],
            note=f"{NOTE_SEN} 2017頁")),
    ),

    # 🔴 AA96 の地図（Googleアースの代わり）。67人＝乗客56＋乗員11（台本 §9）
    "c412": dict(
        t="デトロイトを出る",
        s=AA96_S,
        fig=ss.aa96_map([
            dict(tag=dict(at="dtw", t="N103AA　67人", side="left")),
            dict(move=[dict(kind="path", via=["dtw", "windsor"], sec=3.0)],
                 tag=dict(at="dtw", t="19:20　離陸", side="below")),
            dict(tag=dict(at="dtw", t="警告灯は点かず", side="above"))]),
    ),

    # 出発の前（上院 p2017〜p2018・p2037）。ポンドはメートル法を先に（§1-6）
    "c413": dict(
        t="出発前の違和感",
        s="ドアを閉めた係員の気づき",
        fig=("panel", dict(
            blocks=[dict(k="出発の前", t="ハンドルが倒れない", v="ふつうの力では", c=J.ALERT),
                    dict(k="ふつうに倒れる力", t="約14キロ（30ポンド）", v="メーカーによる", c=J.AMBER)],
            note=f"{NOTE_SEN} 2017〜2018頁・2037頁", cols=2)),
    ),

    # ひざで押しこむ（上院 p2018・p2024）。54キロ＝120ポンド（台本 §9）
    "c414": dict(
        t="無理に閉めた、その日",
        s="96便の出発の前",
        fig=("panel", dict(
            blocks=[dict(k="ひざで", t="押しこまれたハンドル", v="通気扉は少し斜め", c=J.ALERT),
                    dict(k="整備士の判断", t="そのまま出発", c=J.TICK),
                    dict(k="ピンなしで収める力", t="約54キロ（120ポンド）", v="調べの値", c=J.AMBER)],
            note=f"{NOTE_SEN} 2018頁・2024頁")),
    ),

    # 時刻の型（上院 p2018）。高さ＝1万1750フィート×0.3048（台本 §9）
    "c415": dict(
        t="上昇の途中で",
        s="96便の操縦室（アメリカ東部の時刻）",
        fig=("moment", dict(
            clock="19:25ごろ", label="96便",
            facts=[dict(t="高さ", v="約3580メートル", c=J.AMBER),
                   dict(t="乗員が聞いた音", v="「ドン」", c=J.ALERT),
                   dict(t="顔に舞い上がったもの", v="ちり・ほこり", c=J.TICK)],
            sub=f"{NOTE_SEN} 2018頁")),
    ),

    # 🔴 断面：ウィンザーの近くで外れる → 床の一部が落ちる（上院 p2017）
    "c416": dict(
        t="カナダの上空で",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            start=dict(press="push"),
            steps=[dict(state=dict(press="none", door="gone", air="out"), tag=dict(t="空中で外れる", d="後ろの貨物ドア")),
                   dict(state=dict(floor="down"), tag=dict(t="床の一部が落ちこむ", d="下の貨物室へ"))],
            note=SEC_NOTE, src="米上院の報告 p2017")),
    ),

    # 🔴 断面：ケーブル（上院 p2018〜p2019）。2段目は札を2つ（row1・row2）
    "c417": dict(
        t="傷んだ操縦の系統",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            start=dict(door="gone", air="out", floor="down"),
            steps=[dict(state=dict(cable="hurt"), tag=dict(t="ケーブルが切れる", d="動きにくくなったものも")),
                   dict(tag=[dict(t="かじのペダル", d="左いっぱいで止まる"),
                             dict(t="真ん中のエンジン", d="レバーが動かない", at="row2")])],
            note=SEC_NOTE, src="米上院の報告 p2018〜p2019")),
    ),

    # 🔴 AA96 の地図が戻る：ウィンザーの近く → デトロイトの空港へ（上院 p2018〜p2019）
    "c418": dict(
        t="デトロイトへ戻る",
        s=AA96_S,
        fig=ss.aa96_map([
            dict(tag=dict(at="windsor", t="エンジンの力も借りる", side="right")),
            dict(move=[dict(kind="path", via=["windsor", "dtw"], sec=3.0)],
                 tag=dict(at="dtw", t="19:44　着陸", side="below"))]),
    ),

    # 上院 p2019
    "c419": dict(
        t="滑走路の上で",
        s="着陸のあと",
        fig=("panel", dict(
            blocks=[dict(k="着陸", t="右へそれて止まる", c=J.AMBER),
                    dict(k="全員", t="滑り台で外へ", c=J.OK)],
            note=f"{NOTE_SEN} 2019頁", cols=2)),
    ),

    # 67人のうち軽いけが11人（客室乗務員2＋乗客9・上院 p2017）。数を合わせる（§5b-6）
    "c420": dict(
        t="軽いけがの11人",
        s="96便に乗っていた67人",
        fig=("icons", dict(
            n=67, on=11, kind="person", cols=17, oncol=J.AMBER,
            lead="亡くなった人は無し　色の人＝軽いけが",
            note=f"{NOTE_SEN} 2017頁・2019頁")),
    ),

    # AA96 のドアの跡（PD・縦長＝額装パネル）。人は後ろ姿（顔は見えない＝②の見本の記録）
    "c421": dict(
        t="電気が弱かった",
        s="96便の胴体に残ったドアの跡　1972年",
        photo=P("aa96_door"), **ss.kind(P("aa96_door")),
        side="right", ann_y=330,
        ann=[dict(t="外れたドア", d="空港から何キロも先の畑で", dc=J.TICK),
             dict(t="フック", d="閉まりきっていない", dc=J.ALERT),
             dict(t="ピン", d="入っていない", dc=J.ALERT)],
    ),

    # 上院 p2017（NTSB の報告の表題の部分）＝引用＝額装・原色。切り出しは `ss.TRIM`
    "c422": dict(
        t="事故を調べた国の機関",
        s="事故報告書の頭（上院の報告に再録）",
        photo=ss.page(2017), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="NTSB", d="国家運輸安全委員会", dc=J.INST),
             dict(t="5月30日のSB", d="まだ入っていなかった", dc=J.ALERT)],
    ),

    # 🔴 決め所⑥（台本 §2 #6・上院 p2017）。左の段の3行＝読む順。3行のナレーション＝pre=1
    #   切り口は2段とも字の無い行（画素）。右の段は別の話（係員の話）＝実物のまま
    "c423": dict(
        t="設計そのものの弱点",
        s="ウィンザーの事故の報告書",
        fig=("trace", dict(
            page=ss.page(2017),
            lines=[(0.2793, 0.6009, 0.4769, 0.6126), (0.1208, 0.6141, 0.4780, 0.6255),
                   (0.1213, 0.6269, 0.2987, 0.6386)],
            phrase="閉まって見えたが、錠はかかっていなかった",
            doc="NTSB の報告（米上院の報告 2017頁）の原文",
            crop=(0.11, 0.5738, 0.89, 0.6777), pre=1)),
    ),

    # AA の DC-10（CC BY 3.0・1974年8月・全画面）
    "c424": dict(
        t="2つの事故をつなぐもの",
        s="アメリカン航空のDC-10　1974年8月",
        photo=P("aa_dc10_1974"), **ss.kind(P("aa_dc10_1974")),
        side="right", ann_y=330,
        ann=[dict(t="錠がかからなくても", d="ハンドルが倒れる", dc=J.ALERT)],
    ),

    # NTSB の勧告（1972年7月6日・上院 p2046〜p2047）
    "c425": dict(
        t="2つの勧告",
        s="NTSBからFAAへ（1972年7月）",
        fig=("panel", dict(
            blocks=[dict(k="7月6日", t="2つの改修の義務づけ", c=J.INST),
                    dict(k="1つ目", t="ピンなしでは閉まらない作り", c=J.AMBER)],
            note=f"{NOTE_SEN} 2046〜2047頁", cols=2)),
    ),

    # 🔴 断面：2つ目の勧告＝床の空気の逃げ道（上院 p2047・のちの AD 75-15-05）。逃げ道があれば床は落ちない（筋）
    "c426": dict(
        t="もう1つの勧告",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            start=dict(door="gone", air="out"),
            steps=[dict(state=dict(vent="open"), tag=dict(t="2つ目：空気の逃げ道", d="床にかかる力を小さく")),
                   dict(tag=dict(t="勧告より前に", d="直し方は決まっていた"))],
            note=SEC_NOTE, src="米上院の報告 p2047・p2048")),
    ),

}
