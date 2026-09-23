# -*- coding: utf-8 -*-
"""第4章 撃つ前の夜の風 c401–c422（22カット）。12本目（キャッスル・ブラボー）。⑤b-3（2026-09-23）で書いた。

■ 実写 8/22（写真4・報告書の頁3・記録映像の止め絵1）。章の色＝夜の藍。爆発の実写は原色（`color=1.0`）。
■ 🔴 動く模式図（drift）＝要所。**冒頭の地図が戻る**（葦の分析を受けた決定・案B）
  c402（東の地図）人の住む島々と人数／c408・c416（広い地図）前の2日間の北西の捜索 → 当日の東北東の捜索（同じ地図が戻る）／
  c412・c419（艦隊の地図）駆逐艦を西から南西へ・艦隊を南東の56キロと93キロへ
  位置は `cuts/ss.py` の `SEARCH_*`・`FLEET_*`＝**報告書の方位角（度）と距離そのもの**（DNA p208・p209）。門番＝`check_drift`
■ c414 は報告書の実物をなぞる型（DNA p209「Winds at 20,000 feet (6.10 km) were headed for Rongelap to the east.」）
■ ⚠️ c401 の警戒の区域は地図に描かない：p112 の脚注の境界（緯度経度）は OCR が欠け、しかも「300海里」と合わない値に読める
   ＝報告書に無い形を描かない（§5b-10）。縦と横の長さだけを棒で比べる
■ ⚠️ c410・c417 の写真はパリー島＝打ち合わせは旗艦エステスの上（DNA p118）。副題は写っている場所だけ（台本 §7）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
SRC_DNA = ss.SRC_DNA
NOTE_DNA = "出典：国防原子力局の報告書（1982年）"


def fleet_map(steps):
    """艦隊の地図（c412・c419）。ビキニの札は上＝下は札（tag）の置き場。"""
    return ("drift", ss.drift_map(steps, view=ss.MAP_VIEW_FLEET, places=[dict(k="bikini", side="above")],
                                  pts=ss.FLEET_PTS, rel=ss.FLEET_REL, note=ss.FLEET_NOTE,
                                  src="DNA p209", scale_km=50))


def wide_map(steps):
    """捜索の地図（c408・c416）。1,000キロを超えるので縮尺は500キロ。"""
    return ("drift", ss.drift_map(steps, view=ss.MAP_VIEW_WIDE, places=ss.MAP_PLACES_WIDE,
                                  pts=ss.SEARCH_PTS, rel=ss.SEARCH_REL, note=ss.SEARCH_NOTE,
                                  src="DNA p208・p209", scale_km=500))


SPEC = {

    # 縦と横の長さだけ（区域の位置と形は描かない＝上の注）
    "c401": dict(
        t="撃つ前の、海の区域",
        s="警戒の区域の大きさ",
        fig=("compare", dict(
            items=[dict(v=278, t="縦", disp="278", unit="キロ", c=J.LINE),
                   dict(v=556, t="横", disp="556", unit="キロ", c=J.AMBER)],
            note=f"{NOTE_DNA}　エニウェトクとビキニを囲む区域")),
    ),

    # 🔴 drift（東の地図）。札は島の名と重ならない側へ（ロンゲラップは名が上＝人数は左）
    "c402": dict(
        t="区域の外の、人の住む島",
        s="マーシャル諸島の北部",
        fig=("drift", ss.drift_map(
            view=ss.MAP_VIEW_EAST, places=ss.MAP_PLACES_EAST, src="WT 1004頁・DNA p223・p238",
            note="模式図：島は環礁の中心（緯度経度の表）。人数は報告書の値",
            steps=[dict(),
                   dict(tag=[dict(at="rongelap", t="64人", side="left"),
                             dict(at="ailinginae", t="18人", side="left"),
                             dict(at="utirik", t="157人", side="above")]),
                   dict(tag=dict(at="rongerik", t="アメリカ兵28人", side="above"))])),
    ),

    # 報告書の第17図（部隊の気象班のしくみ）
    "c403": dict(
        t="風を読む班",
        s="報告書の第17図　部隊の気象班",
        photo=ss.page(118), panel=True, trim=(0.08, 0.455, 0.95, 0.96),
        side="right",
        ann=[dict(t="灰の行き先", d="上空の風しだい", dc=J.TICK),
             dict(t="予報の班", d="本部と島々の観測所", dc=J.INST)],
    ),

    # 🔴 ⑤b-3：台本の DASA 第44図（p2074＝高さごとの風の線図）は**細い線だけで紙の白が97%**＝どう切っても
    #    インク率 2.6〜4.0%（check_blank の下限 4.0%）。下限をかわす切り方は採らない（feedback-dont-spell-around-a-gate）
    #    → 報告書 p114 の**本文の段**（「灰の予報はネバダの記録と、高さごとの風の図＝ホドグラフで作った」）に替えた。
    #    ⚠️ 同じ頁の上半分の第16図は第8章 c814 が使う＝ここは本文の段だけ（別の中身）
    "c404": dict(
        t="高さで変わる風",
        s="報告書の本文　灰の予報の作り方",
        photo=ss.page(114), panel=True, trim=(0.12, 0.68, 0.94, 0.945),
        side="right",
        ann=[dict(t="風の向きと強さ", d="高さごとに違う", dc=J.TICK),
             dict(t="予報のしかた", d="高さごとの風を重ねる", dc=J.AMBER)],
    ),

    "c405": dict(
        t="予報の弱点",
        s="灰の広がりの見積もり方",
        fig=("panel", dict(
            blocks=[dict(k="弱点", t="予報の土台", c=J.ALERT),
                    dict(k="もとの記録", t="ネバダの小さな実験", c=J.LINE),
                    dict(k="分かったこと", t="大きな爆発には足りない", c=J.ALERT)])),
    ),

    # 有る側（小さな実験の1回）と無い側（大きな威力）を数で比べる
    # ⚠️ 副題を字幕の頭（「地上で爆発させた実験」）から切り取らない（check_echo）
    "c406": dict(
        t="手もとにあった記録",
        s="地上爆発の灰の測定",
        fig=("absent", dict(
            mode="pair",
            items=[dict(t="小さな威力の実験", d="1951年に1回", ok=True, c=J.LINE, n=1),
                   dict(t="大きな威力の実験", d="記録なし", ok=False, c=J.ALERT, n=0)],
            note=NOTE_DNA)),
    ),

    "c407": dict(
        t="5日前の見通し",
        s="エニウェトクの金属の建物　1954年",
        photo=P("base_metal"), **ss.kind(P("base_metal")),
        cam="pan_r",
        side="right", ann_y=330,
        ann=[dict(t="撃つ5日前", d="本国と司令部へ", dc=J.DOC),
             dict(t="予報の灰の向き", d="北西から北東へ", dc=J.AMBER),
             dict(t="部隊の見方", d="都合のよい風", dc=J.OK)],
    ),

    # 🔴 drift（広い地図）。2日前＝300°・1,480キロ／前の日＝330°・1,110キロ（DNA p208）
    "c408": dict(
        t="北西の海を探す",
        s="前の2日間の捜索",
        fig=wide_map([
            dict(move=[dict(kind="path", via=["gz", "srch2"], sec=3.0)],
                 tag=dict(at="srch2", t="2日前", side="above")),
            dict(move=[dict(kind="path", via=["gz", "srch1"], sec=3.0)],
                 tag=dict(at="srch1", t="前の日", side="above")),
            # ⚠️ 下に置くと捜索の線が札を貫いた（試し焼き）＝線の来ない左へ
            dict(tag=dict(at="srch2", t="船は見つからず", side="left"))]),
    ),

    # 🔴 決め所（H-18 の予報の電文。DNA p208 が引用）
    "c409": dict(
        t="前日の予報",
        s="司令部へ送った電文",
        fig=("quote", dict(
            phrase="予報：人の住む島々に、大きな降灰なし",
            who="第7合同任務部隊",
            to="太平洋軍の司令部",
            when="撃つ前の日　午前11時",
            doc="予報の電文（報告書が引用）")),
    ),

    "c410": dict(
        t="夕方から、風が変わる",
        s="パリー島の天幕　1954年",
        photo=P("base_tents"), **ss.kind(P("base_tents")),
        cam="pull",
        side="right", ann_y=356,
        ann=[dict(t="変わりはじめ", d="撃つ前の日の夕方", dc=J.AMBER),
             dict(t="午後6時の打ち合わせ", d="予報の風が悪化", dc=J.ALERT)],
    ),

    # 🔴 決め所（DNA p209「nevertheless, the decision to shoot was reaffirmed」）
    "c411": dict(
        t="決定は変わらない",
        s="打ち合わせについての一文",
        fig=("quote", dict(
            phrase="それでも、撃つ決定は改めて確認された",
            who="国防原子力局",
            when="1982年",
            doc="報告書（午後6時の打ち合わせ）")),
    ),

    # 🔴 drift（艦隊の地図）。駆逐艦レンショー＝ビキニから270°・167キロ → 230°・167キロ（DNA p209）
    "c412": dict(
        t="西から、南西へ",
        s="艦の置き場所の変更",
        fig=fleet_map([
            # ⚠️ 左に置くと「ビキニ環礁」の札とくっついて1語に読めた（試し焼き）＝上へ
            dict(tag=dict(at="gz", t="真夜中に見直し", side="above")),
            dict(ship=dict(at="dd_new", t="駆逐艦"),
                 tag=dict(at="dd_old", t="予定の位置", side="above"),
                 move=[dict(kind="path", via=["dd_old", "dd_new"], sec=2.5)]),
            dict(tag=dict(at="bikini", t="雲の見張りは2時間後", side="below"))]),
    ),

    "c413": dict(
        t="さらに悪い風",
        s="午前0時の打ち合わせ",
        fig=("panel", dict(
            blocks=[dict(k="真夜中", t="風はさらに悪化", c=J.ALERT),
                    dict(k="悪くなった高さ", t="3キロから7.5キロ", c=J.AMBER)],
            cols=2)),
    ),

    # 🔴 決め所。報告書の実物をなぞる型（DNA p209）。文は2行にまたがる＝読む順に塗る（§5b-36）
    "c414": dict(
        t="島へ向かう風",
        s="真夜中の打ち合わせの記録",
        fig=("trace", dict(
            page=ss.page(209),
            lines=[(0.4705, 0.4635, 0.7626, 0.4821), (0.077, 0.4857, 0.4382, 0.5042)],
            phrase="高さ6キロの風が、ロンゲラップへ向かう",
            doc=f"{SRC_DNA} 209頁の原文",
            # 切り口は行と行のすきま（PDF の文字の層で測った。行の途中で切ると下の行が半分見える）
            crop=(0.05, 0.432, 0.95, 0.552))),
    ),

    # ⚠️「おそらく汚れる」の留保は「汚れそう」で残す（§5b-27b）
    "c415": dict(
        t="司令部の判断",
        s="真夜中の打ち合わせの結論",
        fig=("panel", dict(
            blocks=[dict(k="風の速さ", t="遅く、心配はいらない", c=J.OK),
                    dict(k="汚れそうな島", t="ビキニ島・エネマン島", c=J.ALERT),
                    dict(k="判断", t="撃つ決定を再び確認", c=J.ALERT)])),
    ),

    # 🔴 drift（広い地図が戻る）。前の2日間の捜索をもう一度引いてから、当日の65°・1,110キロ（DNA p209）
    "c416": dict(
        t="当日の、追加の捜索",
        s="船を探す飛行の向き",
        fig=wide_map([
            dict(move=[dict(kind="path", via=["gz", "srch2"], sec=1.5),
                       dict(kind="path", via=["gz", "srch1"], sec=1.5)],
                 tag=dict(at="srch1", t="前の2日間", side="above")),
            dict(move=[dict(kind="path", via=["gz", "srch0"], sec=3.0)],
                 tag=dict(at="srch0", t="爆発の当日", side="above")),
            dict(dim=dict(a="gz", b="srch0", t="約1100キロ", d="東北東"))]),
    ),

    # ⚠️ ⑤b-4：`check_slide` G-10 が「= 0 = 00 = 0 =」の行頭が左端で欠けると鳴った（pan_l の始まり）。
    #    その「行」は左の建物の**窓の並び**を OCR が読み違えたもの（`--draw c417 --boxes` で見た）＝文字ではない。
    #    門番に「文字ではない行」を登録する口が無い → 引き（pull）に替え、起点を左寄り（xbias=0.3）にした：
    #    中央の起点だと窓の左端が元画像の x≈491＝行の頭（x 451）が 47px 欠けた。0.3 なら頭・中・尻の3点とも行が窓に入る
    "c417": dict(
        t="夜明け前の、見直し",
        s="パリー島の桟橋　1954年",
        photo=P("base_dock"), **ss.kind(P("base_dock")),
        cam="pull", xbias=0.3,
        side="right", ann_y=330,
        ann=[dict(t="最後の見直し", v="午前4時30分", vc=J.AMBER),
             dict(t="全体の風", d="大きな変化なし", dc=J.OK),
             dict(t="ビキニの低い空", d="北寄り・西寄りの風へ", dc=J.ALERT)],
    ),

    # 報告書の第55図（爆発のときの艦の位置・横長の頁）
    "c418": dict(
        t="艦隊を、さらに遠くへ",
        s="報告書の第55図　爆発のときの艦の位置",
        photo=ss.page(214), panel=True, trim=(0.01, 0.05, 0.99, 0.84),
        side="right",
        ann=[dict(t="提案した係", d="放射線の安全の担当", dc=J.INST),
             dict(t="艦隊を下げる先", v="93キロ", vc=J.AMBER, d="いまは56キロ")],
    ),

    # 🔴 drift（艦隊の地図が戻る）。南東の56キロ（大きな船）と93キロ（小さく遅い船）＝DNA p209
    "c419": dict(
        t="残った大きな船",
        s="艦隊の置き場所",
        fig=fleet_map([
            dict(ship=dict(at="fl93", t="小さく遅い船"),
                 tag=dict(at="fl93", t="93キロ", side="below"),
                 move=[dict(kind="path", via=["fl56", "fl93"], sec=2.5)]),
            dict(ship=dict(at="fl56", t="大きな船"),
                 tag=dict(at="fl56", t="56キロ", side="left"))]),
    ),

    # DOE の記録映像の1コマ（止め絵・射点の小屋と土手道）
    "c420": dict(
        t="装置のそばに、わずか",
        s="射点の小屋と土手道　記録映像の1コマ",
        photo=P("doe_shotcab_far"), **ss.kind(P("doe_shotcab_far")),
        side="right", ann_y=356,
        ann=[dict(t="艦隊", d="環礁の外へ", dc=J.LINE),
             dict(t="装置のそば", d="起爆の班と警備", dc=J.AMBER)],
    ),

    # 位置関係だけ（距離は台本に無い＝描かない）
    "c421": dict(
        t="起爆は、海の向こう岸から",
        s="起爆の班の動き",
        fig=("people", dict(
            nodes=[dict(x=0.20, y=0.42, t="射点の小屋", d="装置", kind="part", c=J.ALERT),
                   dict(x=0.76, y=0.42, t="エニュー島の指令所", d="起爆の班が移る", kind="org", c=J.INST)],
            edges=[dict(a=0, b=1, t="環礁の内側の海", c=J.LINE)],
            note="模式図：位置関係だけ（距離は描いていない）")),
    ),

    # NARA #04（艦エステスから・海の上のきのこ雲・明るい）。原色。章の終わり＝尻で暗転（自動）
    "c422": dict(
        t="語られてきた夜",
        s="艦エステスから見たきのこ雲　1954年3月1日",
        photo=P("fb_estes_a"), **ss.kind(P("fb_estes_a")),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="のちの語られ方", d="島へ向かう風と知りつつ", dc=J.TICK),
             dict(t="2013年の報告書", d="6キロの風との直接の関係は否定", dc=J.ALERT),
             dict(t="予定どおり", v="午前6時45分", vc=J.AMBER)],
    ),

}
