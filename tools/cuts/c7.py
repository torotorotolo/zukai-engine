# -*- coding: utf-8 -*-
"""第7章 77秒 c701–c722（22カット）。13本目（トルコ航空981便）。⑤b-4（2026-09-25）で書いた。

⚠️ 12本目の中身は `git show 3832147:tools/cuts/c7.py`（⑤b-1 で空にした）。
⚠️ 見出し・副題に章名「77秒」を入れない（§5b-46＝check_dup が鳴る）。

■ 写真 5/22（事故機 A4＝BY-SA 額装／同型機の操縦室 C3・飛行中の同型機 D2／仏の写真の頁 p16・p63＝引用＝額装・原色）
■ 決め所 c706（仏 p53）・c708（仏 p141＝音声の記録の書き起こし）はなぞる型（trace）
■ 地図＝c707・c717 は `ss.route_map`（c101 と同じ範囲にオルリーとサン・パテュスを足した地図）。**Googleアースの代わり**
■ 断面（section）＝c710（床が崩れる）・c711（ケーブル）＝第1・3章と同じ絵
■ 台本 §7 から替えたところ（⑤b-4 の決め）
  c707：Googleアース（サン・パテュスの畑）→ 経路の地図（取り方・表示の置き方が未定のまま＝§5b-61）
  c708：音声の記録は p141（付属書2 第22葉・トルコ語の原文とフランス語の訳）をなぞる
  c720：p17（森に開いた空間）→ p63（森に散った残骸）。p17 は頁の上で写真が横倒し＝写真の型に回す仕組みが無い
  c721：p63 → 道すじの図（process）。p63 は c720 に使った
■ 時刻は画面では「12:39:56」の形（報告書の世界時に1時間足したパリの時刻＝c112 で断っている）
■ 実名＝乗員3人（公的な任務・仏 p19〜p21）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
NOTE_FR = "出典：フランスの最終報告書"
SEC_NOTE = "模式図：機体を後ろから見た断面。形と大きさは実物どおりではない"

SPEC = {

    # 着陸する事故機（A4・CC BY-SA 4.0＝額装・原色・1点1カット・札を重ねない）。離陸 12:30:30・346人（仏 p10・p18）
    "c701": dict(
        t="346人を乗せて、12:30:30",
        s="着陸する事故機 TC-JAV　1973年（白黒）",
        photo=P("tcjav_landing"), panel=True, color=1.0,
    ),

    # 乗員3人（仏 p19〜p21・公的な任務＝実名可）
    "c702": dict(
        t="操縦室の3人",
        s="981便の乗員",
        fig=("panel", dict(
            blocks=[dict(k="機長", t="ネジャット・ベルキョズ", v="44歳", c=J.AMBER),
                    dict(k="副操縦士", t="オラル・ウルスマン", v="38歳", c=J.LINE),
                    dict(k="航空機関士", t="エルハン・オゼル", v="37歳", c=J.LINE)],
            note=f"{NOTE_FR} PDF 19〜21頁")),
    ),

    # 飛んだ時間（仏 p19〜p22：7003時間10分・5589時間25分・2113時間25分＝台本 §9）。棒は値に比例（差は5%より大きい）
    "c703": dict(
        t="飛んだ時間",
        s="乗員3人の経歴",
        fig=("compare", dict(
            items=[dict(v=7003, t="機長", c=J.AMBER),
                   dict(v=5589, t="副操縦士", c=J.LINE),
                   dict(v=2113, t="航空機関士", c=J.LINE)],
            unit="時間",
            note=f"{NOTE_FR} PDF 19〜22頁　空軍の出身＝機長と副操縦士")),
    ),

    # 同型機の操縦室（C3・CC0・全画面）。英 p1010・仏 p11・p104・p121
    #   ⑤c'（09-25）：国立公文書館の記録（926-1073）に人名の欄が無い＝右の席の男性が乗員か来賓か決まらない
    #   → 顔を外して計器盤と操縦席へ（`ss.TRIM` の klm_cockpit_1972）
    "c704": dict(
        t="北へ上っていく",
        s="同じ型の機体の操縦室（KLM）　1972年・アムステルダム",
        photo=P("klm_cockpit_1972"), **ss.kind(P("klm_cockpit_1972")),
        side="right", ann_y=330,
        ann=[dict(t="上り方", d="自動操縦", dc=J.TICK),
             dict(t="ドアの警告灯", d="消えたまま（報告書の見方）", dc=J.AMBER)],
    ),

    # 仏 p11・p55（1万1500フィート×0.3048＝3505m・300ノット×1.852＝556km/h＝台本 §9）
    "c705": dict(
        t="上昇の途中",
        s="減圧の直前",
        fig=("moment", dict(
            clock="9分あまり", label="離陸から",
            facts=[dict(t="高さ", v="約3500メートル", c=J.AMBER),
                   dict(t="速さ", v="時速約560キロ", c=J.AMBER)],
            sub=f"{NOTE_FR} PDF 11頁・55頁")),
    ),

    # 🔴 決め所⑫（台本 §2 #12・仏 p53「décompression entendu à 11.39'56"」＝世界時）。2行のナレーション＝pre=0
    #   行の矩形は文字の層（語の箱）。切り口＝その行と次の段（与圧の警報が25秒弱）＝文字の層の行のすきま
    "c706": dict(
        t="ボイスレコーダーの時刻",
        s="フランスの最終報告書（1976年）",
        fig=("trace", dict(
            page=ss.page(53),
            lines=[(0.3794, 0.2906, 0.7297, 0.3082)],
            phrase="12:39:56、減圧の音",
            doc="原文（PDF 53頁）　報告書の時刻は世界時（パリの時刻の1時間前）",
            crop=(0.27, 0.278, 0.87, 0.3825))),
    ),

    # 経路の地図：オルリー → サン・パテュス（仏 p12・p64）。Googleアースの代わり
    "c707": dict(
        t="北東の村の上空で",
        s="オルリーからの経路",
        fig=ss.route_map([
            dict(move=[dict(kind="path", via=["orly", "stpathus"], sec=3.0)],
                 tag=dict(at="orly", t="12:30:30　離陸", side="below")),
            dict(tag=dict(at="stpathus", t="12:39:56　ドアが外れる", side="right"))]),
    ),

    # 🔴 決め所⑬（台本 §2 #13・仏 p141＝付属書2 第22葉）。CAM 2「…kabin patladı」＝「…la carlingue a éclaté」
    #   ⚠️ 頁は横向き（2347×1654）の表。縦の罫線が行のあいだも通る＝インク0の行が無い＝罫線だけの行（インク11〜12）で切る
    #   ナレーションは2行（機長の問い＋決め所）＝pre=0。蛍光ペンは答えの行（原文→訳の順）
    "c708": dict(
        t="副操縦士の答え",
        s="音声の記録の書き起こし",
        fig=("trace", dict(
            page=ss.page(141),
            lines=[(0.2050, 0.3330, 0.3250, 0.3596), (0.5880, 0.3324, 0.7650, 0.3598)],
            phrase="機体が破裂した",
            doc="付属書2（PDF 141頁）　左＝トルコ語の原文・右＝フランス語の訳",
            crop=(0.03, 0.120, 0.97, 0.4075))),
    ),

    # 管制官が聞いたもの（仏 p11・p53・p141）
    "c709": dict(
        t="管制官が聞いたもの",
        s="地上に届いた無線",
        fig=("panel", dict(
            blocks=[dict(k="交信", t="乱れていた", c=J.LINE),
                    dict(k="声", t="トルコ語", c=J.LINE),
                    dict(k="音", t="警報", c=J.ALERT)],
            note=f"{NOTE_FR} PDF 11頁・53頁", cols=3)),
    ),

    # 🔴 断面：床が押され → 崩れる（仏 p18・p64・p99・p104）。6人＝仏 p18・p64
    "c710": dict(
        t="床が抜けた",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            start=dict(door="gone", air="out"),
            steps=[dict(state=dict(floor="push"), tag=dict(t="床が崩れる", d="上からの圧力")),
                   dict(state=dict(floor="down"), tag=dict(t="6人が機体の外へ", d="座席の一部とともに"))],
            rel=[dict(t="6人", src="仏 p18・p64（乗客6人）")],
            note=SEC_NOTE, src="仏の報告書 PDF 18頁・64頁・99頁")),
    ),

    # 🔴 断面：床下のケーブル（仏 p104）。真ん中のエンジン＝尾翼の根元の2番エンジン
    "c711": dict(
        t="操縦の線と、エンジン",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            start=dict(door="gone", air="out", floor="down"),
            steps=[dict(state=dict(cable="hurt"), tag=dict(t="床下のケーブルが傷む", d="床と一緒に落ちる")),
                   dict(tag=dict(t="エンジンが1つ止まる", d="尾翼の根元（真ん中）"))],
            note=SEC_NOTE, src="仏の報告書 PDF 104頁")),
    ),

    # 昇降舵（仏 p99・p104）。台本の画は「模式図」＝伝わる道すじを流れで
    "c712": dict(
        t="きかなくなった昇降舵",
        s="操縦が伝わる道すじ",
        fig=("process", dict(
            steps=[dict(t="ケーブル", d="床とともに傷む", c=J.ALERT),
                   dict(t="尾翼の昇降舵", d="機首を上げ下げ", c=J.AMBER),
                   dict(t="立て直せない", d="操縦がきかない", c=J.ALERT)],
            note=f"{NOTE_FR} PDF 99頁・104頁")),
    ),

    # 飛行中の同型機（D2・PD US no notice・ダグラスの広報写真 1971年・全画面）。仏 p11〜p12・p55〜p56
    "c713": dict(
        t="消えた便名",
        s="飛行中の同じ型の機体　1971年（ダグラスの広報写真）",
        photo=P("dc10_flight_1971"), **ss.kind(P("dc10_flight_1971")),
        side="right", ann_y=330,
        ann=[dict(t="レーダーの画面", d="981便の便名が消える", dc=J.ALERT)],
    ),

    # 減圧から22秒後（仏 p55〜p56：362ノット×1.852＝670km/h＝台本 §9）
    "c714": dict(
        t="傾く機首、上がる速さ",
        s="飛行の記録から",
        fig=("panel", dict(
            blocks=[dict(k="減圧から", t="22秒後", c=J.TICK),
                    dict(k="機首", t="約20度下向き", c=J.AMBER),
                    dict(k="速さ", t="時速670キロ", v="362ノット", c=J.ALERT)],
            note=f"{NOTE_FR} PDF 55〜56頁")),
    ),

    # 速すぎる警報（仏 p53「audition de l'alarme survitesse vers 11.40'23" … pendant une durée de l'ordre de 50 secondes」）
    "c715": dict(
        t="鳴りつづけた警報",
        s="音声の記録から",
        fig=("panel", dict(
            blocks=[dict(k="鳴りだした警報", t="速すぎる", c=J.ALERT),
                    dict(k="鳴った長さ", t="約50秒", v="記録の終わりまで", c=J.AMBER)],
            note=f"{NOTE_FR} PDF 53頁", cols=2)),
    ),

    # 仏 p121（乗員の反応）
    "c716": dict(
        t="取り乱さなかった乗員",
        s="報告書の見立て",
        fig=("panel", dict(
            blocks=[dict(k="事態", t="すぐに見抜いた", c=J.LINE),
                    dict(k="乗員の様子", t="取り乱していない", c=J.AMBER)],
            note=f"{NOTE_FR} PDF 121頁", cols=2)),
    ),

    # 経路の地図：サン・パテュス → 森（仏 p12「environ 15 kilomètres du village de Saint-Pathus」＝check_drift が照合）
    "c717": dict(
        t="森まで、およそ15キロ",
        s="ドアが外れた村と、森",
        fig=ss.route_map([
            dict(move=[dict(kind="path", via=["stpathus", "crash"], sec=2.5)],
                 dim=dict(a="stpathus", b="crash", t="約15キロ"))]),
    ),

    # 12:39:56 減圧 → 12:40:23ごろ 速すぎる警報 → 12:41:13 記録が止まる（仏 p53）。77秒＝台本 §9
    #   ⚠️ 目盛りは素の秒（旗の時刻と同じ語にしない＝check_dup ①）
    "c718": dict(
        t="記録が途切れた時刻",
        s="音声の記録の最後",
        fig=("timeline", dict(
            events=[dict(t=0, top="12:39:56", t2="減圧", c=J.ALERT),
                    dict(t=27, top="12:40:23ごろ", t2="速すぎる警報", c=J.AMBER),
                    dict(t=77, top="12:41:13", t2="記録が止まる", c=J.ALERT, big=True)],
            t0=-8, t1=88,
            ticks=[(0, "0秒"), (30, "30秒"), (60, "60秒")],
            band=[dict(a=0, b=77, t="約77秒", c=J.ALERT)],
            src="仏の報告書 PDF 12頁・53頁")),
    ),

    # 仏 p16（衝突した場所の寄りの写真・東を向いて撮影・矢印は機体が来た向き）＝引用＝額装・原色。姿勢は仏 p12
    "c719": dict(
        t="森に突っこんだ姿勢",
        s="衝突した場所の寄りの写真（東を向いて撮影）",
        photo=ss.page(16), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="矢印", d="機体が来た向き", dc=J.TICK),
             dict(t="左への傾き", v="約17度", vc=J.AMBER),
             dict(t="速さ", v="時速約800キロ", vc=J.ALERT)],
    ),

    # 仏 p63（残骸の散らばり）＝引用＝額装・原色。⑤b-4 で1011px（原寸の0.72倍）で見た：遺体・負傷は写っていない
    #   木の高さ・火は仏 p12・p60
    "c720": dict(
        t="森に散った機体",
        s="報告書の写真　残骸の散らばり",
        photo=ss.page(63), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="当たった木の高さ", v="約10メートル", vc=J.AMBER),
             dict(t="火", d="出なかった", dc=J.TICK)],
    ),

    # 仏 p64（最後のかけらは最初に木に触れた所から700メートル）
    "c721": dict(
        t="かけらが散った長さ",
        s="残骸が散った道すじ",
        fig=("process", dict(
            steps=[dict(t="梢に触れる", d="最初の場所", c=J.LINE),
                   dict(t="森を切り開く", d="かけらが散る", c=J.AMBER),
                   dict(t="最後のかけら", d="約700メートル先", c=J.ALERT)],
            note=f"{NOTE_FR} PDF 64頁")),
    ),

    # 章の橋（副題は10本目からの型「ここまでと、この先」）。仏 p64
    "c722": dict(
        t="346人のほうへ",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="翌朝の畑", t="ドアの一部と6人", c=J.AMBER),
                    dict(k="次は", t="乗っていた人たち", v="第8章", c=J.LINE)],
            cols=2)),
    ),

}
