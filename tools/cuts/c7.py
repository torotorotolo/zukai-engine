# -*- coding: utf-8 -*-
"""第7章 島に降った灰 c701–c722（22カット）。12本目（キャッスル・ブラボー）。⑤b-4（2026-09-23）で書いた。

■ 実写 12/22（写真7・報告書の頁5）。章の色＝青緑。
■ 🔴 動く模式図（drift）＝要所（午後2時半に島へ灰→知らせ→避難）
   c702 ロンゲリックに降る灰（第6章 c626 の「島に寄った地図」が戻る）／c705 知らせはエニウェトクの通信所へ（西の地図）／
   c718 28人をクェゼリンの基地へ（南の地図）。範囲は `cuts/ss.py` の `MAP_VIEW_ISLES`・`_WEST`・`_SOUTH`
   ⚠️ 司令部（旗艦）の位置は描かない＝報告書にこの時刻の位置が無い（§5b-10）
■ c711 は報告書の実物をなぞる型（DNA p227「It is clear that at this time Hq JTF 7 did not know where the cloud was,
   nor where it had been.」）＝⑤b-4 で頁 p227 を焼き足した（`qa_out/ep12_assets.py` の PAGES_PICK）
■ ⚠️ p229（台本 §7 の c701 第63図・c715 第64図）は使わない：
   第63図（配置図）は細い線だけで紙の白が96%＝`check_blank` のインク率 3.6%（下限4.0%）。**下限をかわす切り方はしない**（§5b-41）／
   第64図（観測所の写真）は **NARA #40 と同じ写真**（⑤b-4 で並べて見た）
   → c701＝NARA #40 の原版（`rongerik_station`・島そのもの）／c715＝時計の型（真夜中の命令）／c716＝放射線を測る写真（NARA #47）
■ ⚠️ c706：台本 §7 は c702 に DASA 第40図（p2069）を当てていたが、c702 を動く地図にしたので c706（司令部が知らなかった灰の量）へ移した
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
SRC_DNA = ss.SRC_DNA
NOTE_DNA = "出典：国防原子力局の報告書（1982年）"
# 降灰の再現図は左にビキニ・右へ東の島々＝左から右へなぞる（c519・c520 と同じ）
EASTWARD = {"from": (0.0, 0.5, 1.25), "to": (1.0, 0.5, 1.25)}
# ロンゲリックの夜（時刻は DNA p224・p227・p228）。t＝3月1日の0時からの時間
NIGHT = dict(t0=14.0, t1=25.0, ticks=[(18, "午後6時"), (21, "午後9時"), (24, "0時")], src=NOTE_DNA)
EV_OFF = dict(t=14.83, top="針が振り切れる", t2="午後2時50分", c=J.ALERT)


SPEC = {

    # NARA #40（ロンゲリックの気象観測所・金属の建物と天幕とアンテナ）。p229 の第64図と同じ写真の原版
    "c701": dict(
        t="観測の島",
        s="ロンゲリックの気象観測所　1954年",
        photo=P("rongerik_station"), **ss.kind(P("rongerik_station")),
        cam="pan_r",
        side="right", ann_y=330,
        ann=[dict(t="爆心から東へ", v="250キロ", vc=J.AMBER),
             dict(t="アメリカ兵", v="28人", vc=J.AMBER),
             dict(t="仕事", d="天気などの観測", dc=J.TICK)],
    ),

    # 🔴 drift（島に寄った地図が戻る＝c626）。降る灰の柱の上に札を置かない＝ロンゲリックの札は左
    #    ⚠️ ロンゲラップに灰を降らせない＝ロンゲラップのほうが早かった（段の順に降らせると順番が逆に見える）
    "c702": dict(
        t="ロンゲリックにも、灰",
        s="灰が降りはじめた時刻",
        fig=ss.isles_map([
            dict(tag=dict(at="rongerik", t="午後2時半ごろ", side="left"),
                 move=[dict(kind="fall", at="rongerik")]),
            dict(),
            dict(tag=dict(at="rongelap", t="2時間近く早く", side="above"))],
            src="DNA p223"),
    ),

    # ⚠️ 見出し「島の記録計」は札「放射線の記録計」が80%を覆った（check_dup）
    "c703": dict(
        t="島に置いた計器",
        s="観測所の計器",
        fig=("panel", dict(
            blocks=[dict(k="置いてあった計器", t="放射線の記録計", c=J.INST),
                    dict(k="測る強さ", t="ごく弱い放射線", c=J.TICK),
                    dict(k="係との約束", t="振り切れたら連絡", c=J.ALERT)])),
    ),

    # 🔴 決め所（DNA p224）
    "c704": dict(
        t="計器の知らせ",
        s="午後の観測所",
        fig=("quote", dict(
            phrase="記録計の針が、振り切れた",
            who="国防原子力局",
            when="1982年",
            doc="報告書（3月1日　午後2時50分）")),
    ),

    # 🔴 drift（西の地図）。線は知らせの向きだけ（電波の道筋ではない）
    "c705": dict(
        t="知らせの行き先",
        s="ロンゲリックからの知らせ",
        fig=("drift", ss.drift_map(
            steps=[dict(tag=dict(at="rongerik", t="午後3時15分", side="above"),
                        move=[dict(kind="sight", a="rongerik", b="enewetak")]),
                   dict(tag=dict(at="enewetak", t="通信所", side="above")),
                   dict()],
            view=ss.MAP_VIEW_WEST, places=ss.MAP_PLACES_WEST, src="DNA p224",
            note="模式図：島は環礁の中心（緯度経度の表）。線は知らせの向きだけ")),
    ),

    # DASA 第40図（1時間後に換算した島々の放射線・北が左の図）。あとの調べで描いた図＝札でそう断る
    "c706": dict(
        t="司令部の知らないこと",
        s="報告書の第40図　1時間後に換算した島々の放射線",
        # ⑤c'（09-23）：寄りの終わりで図の題「Off-site dose … at H+1 hour」が窓の下の辺に切られていた＝題は副題が名乗るので外す（台帳 §7-4）
        photo=ss.page(2069), panel=True, trim=(0.08, 0.14, 0.92, 0.847),
        side="right",
        ann=[dict(t="上の司令部", d="ロンゲリックの灰の量を知らず", dc=J.ALERT),
             dict(t="図の値", d="あとの調べ", dc=J.TICK)],
    ),

    # NARA #37（汚れた服を着替える天幕・パリー島）。⚠️ ロンゲリックの写真ではない＝副題は写っている場所だけ
    "c707": dict(
        t="仕事は、そのまま",
        s="パリー島の着替えの天幕　1954年",
        photo=P("dc_tent"), **ss.kind(P("dc_tent")),
        cam="pan_r",
        side="right", ann_y=330,
        ann=[dict(t="ロンゲリックの兵士", d="ふだんの仕事", dc=J.TICK),
             dict(t="着がえ", d="長そで長ズボンへ", dc=J.AMBER)],
    ),

    # NARA #46（灰を受けるトレイを据える2人）。右のフィルムの縁は `ss.TRIM` で落とした
    "c708": dict(
        t="部屋の中にも、灰",
        s="灰を受けるトレイを据える　1954年",
        photo=P("fo_tray"), **ss.kind(P("fo_tray")),
        side="right", ann_y=330,
        ann=[dict(t="深いところで", v="1センチほど", vc=J.AMBER),
             dict(t="食堂や宿舎のテーブル", d="目に見える層", dc=J.ALERT)],
    ),

    # NARA #19（白い服の2人が長い棒で濾紙を扱う・鉛の箱）
    "c709": dict(
        t="灰を、のぞいてみる",
        s="長い棒で濾紙を扱う　1954年",
        photo=P("fo_roll_prep"), **ss.kind(P("fo_roll_prep")),
        cam="pull",
        side="right", ann_y=330,
        ann=[dict(t="顕微鏡で", d="灰の粒", dc=J.TICK),
             dict(t="ブラウン管", d="灰で光る", dc=J.AMBER)],
    ),

    # 報告書の第62図（12時間後の降灰の再現・雲を追った飛行 WILSON 2・3）をカメラで東へなぞる。下の黒い罫の手前で切る
    "c710": dict(
        t="夜の追跡",
        s="報告書の第62図　12時間後の降灰の再現",
        # ⑤c'（09-23）：窓の上の辺が札「WILSON 2 ／ INBOUND H+13」（2行で1つ）の1行目を横に切っていた（見えて22%）
        #    ＝窓を下げて2行とも外し、下の縮尺の数字「0 20 40…」を丸ごと入れる（台帳 §7-4）
        photo=ss.page(226), panel=True, trim=(0.05, 0.181, 0.97, 0.801),
        cam=EASTWARD,
        side="right",
        ann=[dict(t="雲を追う飛行機", d="東へ", dc=J.AMBER),
             dict(t="高さ3キロから", d="島の上でも弱い値", dc=J.TICK)],
    ),

    # 🔴 決め所。報告書の実物をなぞる型（DNA p227）。文は2行＝読む順に塗る（§5b-36）
    "c711": dict(
        t="夜の司令部",
        s="1982年の報告書の一文",
        fig=("trace", dict(
            page=ss.page(227),
            lines=[(0.1346, 0.4589, 0.7943, 0.4776), (0.0943, 0.4819, 0.3568, 0.5006)],
            phrase="司令部は、雲の行方も通り道も知らなかった",
            doc=f"{SRC_DNA} 227頁の原文",
            # 切り口は行と行のすきま（段落の頭「It is clear」から3行。PDF の文字の層で測った）
            crop=(0.08, 0.449, 0.92, 0.5249))),
    ),

    # NARA #31（翼端の筒から濾紙を取り出す）。焼き付けの余白と書き込みは `ss.TRIM` で落とした
    "c712": dict(
        t="追跡の取りやめ",
        s="翼の筒から濾紙を取り出す　1954年",
        photo=P("fo_tank"), **ss.kind(P("fo_tank")),
        side="right", ann_y=330,
        ann=[dict(t="前の水爆実験", d="灰の大半を追えず", dc=J.TICK),
             dict(t="当時の結果", d="何も起きず", dc=J.OK)],
    ),

    # ロンゲリックの夜（1）。針は午後2時50分から振り切れたまま
    "c713": dict(
        t="夜になっても",
        s="3月1日の夜",
        fig=("timeline", dict(
            events=[dict(EV_OFF),
                    dict(t=20.0, top="2通目の知らせ", t2="夜8時ごろ", c=J.AMBER, big=True)],
            band=[dict(a=14.83, b=20.0, t="振り切れたまま", c=J.ALERT)],
            **NIGHT)),
    ),

    # ロンゲリックの夜（2）＝同じ時間軸が戻る。送ったのは翌日＝0時から先の帯（時刻は描かない）
    "c714": dict(
        t="司令部の返事",
        s="3月1日の夜から翌日",
        fig=("timeline", dict(
            events=[dict(EV_OFF),
                    dict(t=20.0, top="2通目の知らせ", t2="夜8時ごろ", c=J.AMBER),
                    dict(t=22.0, top="返事を用意", t2="夜10時", c=J.OK, big=True)],
            band=[dict(a=24.0, b=25.0, t="送信は翌日", c=J.ALERT)],
            **NIGHT)),
    ),

    # 日付が変わるころ（DNA p228）。⚠️ 見出しを「日付が変わるころ」にすると字幕の文の頭の切り取り（check_echo）
    "c715": dict(
        t="真夜中の命令",
        s="ロンゲリックの夜",
        fig=("moment", dict(
            clock="0時ごろ", label="3月1日から2日へ",
            facts=[dict(t="別の上官の命令", v="作業をやめる", c=J.ALERT),
                   dict(t="入る先", v="金属の建物", c=J.AMBER)],
            sub=NOTE_DNA)),
    ),

    # NARA #47（白い服の係が F4U 戦闘機の放射線を測る・パリー島）。⚠️ ロンゲリックの写真ではない＝副題は写っているものだけ
    #   機体の「MARINES」「MN」は機体そのものの表記・「DANGER RADIATION」はその場の看板（§5b-5＝粗ではない）
    "c716": dict(
        t="係の判断",
        s="F4U 戦闘機の放射線を測る　1954年",
        photo=P("dc_f4u_test"), **ss.kind(P("dc_f4u_test")),
        side="right", ann_y=300,
        ann=[dict(t="3月2日の昼前", d="上空から低く測る", dc=J.INST),
             dict(t="決めたこと", d="島を空にする", dc=J.ALERT),
             dict(t="降りて測る", d="建物の中も外も強い", dc=J.ALERT)],
    ),

    # 28人のうち先に運ぶ8人＝点の数を合わせる
    # ⚠️ 注「名字のアルファベット順」は字幕の文の73%の写し（check_echo）
    "c717": dict(
        t="名字の順で",
        s="避難の順番",
        fig=("icons", dict(
            n=28, on=8, kind="person", cols=14, oncol=J.AMBER,
            lead="先に運ぶ8人",
            note="選んだ順：名字の頭文字")),
    ),

    # 🔴 drift（南の地図）。線は運んだ向きだけ（飛んだ道筋ではない）
    # ⚠️ 見出し「クェゼリンの基地へ」は字幕の文と近すぎた（check_echo）
    "c718": dict(
        t="28人の行き先",
        s="ロンゲリックからの避難",
        fig=("drift", ss.drift_map(
            steps=[dict(move=[dict(kind="path", via=["rongerik", "kwajalein"], sec=3.0)]),
                   dict(tag=dict(at="kwajalein", t="8人と20人", side="left")),
                   dict()],
            view=ss.MAP_VIEW_SOUTH, places=ss.MAP_PLACES_SOUTH, src="DNA p233・p234",
            note="模式図：島は環礁の中心（緯度経度の表）。線は運んだ向きだけ")),
    ),

    # 報告書の表22（島ごとの降灰のまとめ）の上の段だけ（Utirik の行まで）
    # 🔴 ⑤c'（09-23）：頁の走査が 1.106° 傾き、行と行のすき間が横に通らない＝どの高さで切っても升目が欠けた
    #    （寄りの終わりで Utirik の行が上半分＝原寸 p18）→ 頁を水平に回した（`qa_out/ep12_assets.py` の DESKEW）。
    #    下の辺は Utirik と Taka の行間（約7px）。寄りは下に固定（bias 1.0）＝既定の中央寄りだと下の辺が約15px 上がって行間を越える。
    #    幅を 0.92→0.81 に狭めて窓を低くし、上の辺を表の題（副題が名乗る）と列の見出しのあいだに置いた（台帳 §7-4・§8）
    "c719": dict(
        t="島の値を測る",
        s="報告書の表22　島ごとの降灰のまとめ",
        photo=ss.page(238), panel=True, trim=(0.05, 0.18, 0.86, 0.4645), bias=1.0,
        side="right",
        ann=[dict(t="3月2日の午後", d="ロンゲラップに強い値", dc=J.ALERT),
             dict(t="駆逐艦", d="すぐにロンゲラップへ", dc=J.AMBER)],
    ),

    # WT の第1.1図（ロンゲラップ島の住まい・写真2枚）。人は写っていない（⑤b-3・⑤b-4 で見た）
    "c720": dict(
        t="避難の始まり",
        s="報告書の第1.1図　ロンゲラップ島の住まい",
        # ⑤c'（09-23）：寄りの終わりで図の注「Fig. 1.1 The Living Area…」が窓の下の辺に切られていた（見えて22%）＝注は副題が名乗るので外す（台帳 §7-4）
        photo=ss.page(1015), panel=True, trim=(0.29, 0.13, 0.88, 0.77),
        side="right",
        ann=[dict(t="始まった時刻", v="3日の朝7時半", vc=J.AMBER),
             dict(t="爆発から", v="まる2日", vc=J.ALERT),
             dict(t="近くの環礁の18人", d="あとから駆逐艦へ", dc=J.TICK)],
    ),

    # 報告書の第66図（48時間後の艦の位置・横長の頁）
    "c721": dict(
        t="避難の終わり",
        s="報告書の第66図　48時間後の艦の位置",
        # ⑤c'（09-23）：寄りの終わりで図の注「Figure 66.」が窓の下の辺に切られていた＝注は副題が名乗るので外す。
        #    注と経度の数字のあいだが 0.018 しか無い＝寄りを少し下へ（bias 0.7）して、経度の数字を寄りの終わりまで入れる（台帳 §7-4）
        photo=ss.page(232), panel=True, trim=(0.04, 0.17, 0.99, 0.815), bias=0.7,
        side="right",
        ann=[dict(t="水上飛行機で", v="16人", vc=J.AMBER, d="年寄りや病人"),
             dict(t="ウトリック", v="157人", vc=J.AMBER, d="4日に島を離れる"),
             dict(t="避難した住民", v="239人", vc=J.ALERT)],
    ),

    # 報告書の第69図（96時間に浴びた放射線の見積もり）。章の終わり＝尻で暗転（自動）
    "c722": dict(
        t="浴びた量の差",
        s="報告書の第69図　96時間に浴びた放射線の見積もり",
        # ⑤c'（09-23）：寄りの終わりで出典の行「(source: Reference 88, p. 437).」が窓の下の辺に切られていた＝図の注「Figure 69.」ごと外す（台帳 §7-4）
        photo=ss.page(243), panel=True, trim=(0.05, 0.09, 0.97, 0.675),
        side="right",
        ann=[dict(t="いちばん多い", d="ロンゲラップ", dc=J.ALERT),
             dict(t="ウトリックの", v="約12倍", vc=J.AMBER),
             dict(t="ロンゲリック", d="ロンゲラップの半分近く", dc=J.TICK)],
    ),

}
