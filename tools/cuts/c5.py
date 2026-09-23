# -*- coding: utf-8 -*-
"""第5章 1500万トン c501–c522（22カット）。12本目（キャッスル・ブラボー）。⑤b-3（2026-09-23）で書いた。

■ 実写 17/22（写真8・報告書の頁6・動く映像5）。章の色＝赤銅（赤へ寄せる）。爆発の実写は原色（`color=1.0`）。
■ 🔴 閃光は爆発の瞬間だけ＝c501（DOE 16.6秒の1コマの光。`(16.6−14.0)/0.68`≒3.8）
■ 🔴 動く模式図（drift）＝**冒頭の地図（NEAR）が戻る**：c509 光はロンゲリック（東へ250キロ）と船から見えた／
   c510 音は船へ7、8分後・ロンゲリックへ11分後。位置は `cuts/ss.py` の `MAP_*`（DNA p212・p217）
■ c515 は報告書の実物をなぞる型（DNA p217「…pinhead-sized white and gritty snow.」）
■ c519・c520 は降灰の再現図（報告書の実物）を**カメラでなぞる**（左のビキニから東へ）＝灰の形は描き起こさない
■ ⚠️ c512 と c422 の入れ替え（⑤b-3）：c422＝明るいきのこ雲（#04）／c512＝雲の塊と水平線（#03・30分後の雲）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
SRC_DNA = ss.SRC_DNA
NOTE_DNA = "出典：国防原子力局の報告書（1982年）"
# 降灰の再現図は左にビキニ・右へ東の島々＝左から右へなぞる（寄って動く余地を作る）
# ⚠️ 1.5倍だと終わりのコマで等値線が画面の外へ出て、島の名前と白い紙だけになった（試し焼き c519）＝1.25倍
EASTWARD = {"from": (0.0, 0.5, 1.25), "to": (1.0, 0.5, 1.25)}

SPEC = {

    # DOE 14.0〜24.4秒（0.68倍）。🔴 閃光は爆発の瞬間だけ
    "c501": dict(
        t="その瞬間",
        s="夜明け前の火球　1954年3月1日",
        **ss.vid("c501"),
        color=1.0,
        flash=3.8,
        side="right", ann_y=330,
        ann=[dict(t="現地の時刻", v="午前6時45分", vc=J.AMBER),
             dict(t="起爆", d="指令所からの信号", dc=J.INST),
             dict(t="日本の時計", v="午前3時45分", vc=J.TICK)],
    ),

    # 4K 8.0〜16.0秒（c102 と別の秒）
    "c502": dict(
        t="数秒で、巨大な火の玉",
        s="艦から見た火球　1954年3月1日",
        **ss.vid("c502"),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="火の玉の直径", v="約4.8キロ", vc=J.AMBER),
             dict(t="たとえると", d="歩いて1時間の道のり", dc=J.TICK)],
    ),

    # NARA #01（空撮・雲の上の火球と輪の雲）
    "c503": dict(
        t="1分で、空の上へ",
        s="空から見た雲の上の火球　1954年3月1日",
        photo=P("fb_aerial_b"), **ss.kind(P("fb_aerial_b")),
        color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="1分後の高さ", v="13.7キロ", vc=J.AMBER),
             dict(t="くらべると", d="旅客機より上", dc=J.TICK),
             dict(t="1分後の雲の幅", v="4.8キロ", vc=J.AMBER)],
    ),

    # Commons「Castle Bravo nuclear test」（遠くの火球と輪の雲）
    "c504": dict(
        t="アメリカ最大の爆発",
        s="遠くから見た火球と輪の雲　1954年3月1日",
        photo=P("fb_color_b"), **ss.kind(P("fb_color_b")),
        color=1.0,
        side="right", ann_y=356,
        ann=[dict(t="TNT火薬に直すと", v="1500万トン", vc=J.AMBER),
             dict(t="アメリカの核実験で", d="いちばん大きい", dc=J.ALERT)],
    ),

    # 幅（キロ）と深さ（メートル）は単位が違う＝棒で比べない（bar=False）。断面の形は描き起こさない
    "c505": dict(
        t="サンゴ礁に、巨大な穴",
        s="爆心にできた穴の大きさ",
        fig=("compare", dict(
            items=[dict(v=1.6, t="穴の幅", disp="1.6", unit="キロ", c=J.AMBER),
                   dict(v=60, t="穴の深さ", disp="60超", unit="メートル", c=J.ALERT)],
            bar=False, note=NOTE_DNA)),
    ),

    # DOE 41.0〜47.0秒（立ちのぼる柱）
    "c506": dict(
        t="サンゴが、灰になる",
        s="立ちのぼる雲　1954年3月1日",
        **ss.vid("c506"),
        color=1.0,
        side="right", ann_y=356,
        ann=[dict(t="雲に吸い上げられた", d="砕けたサンゴ", dc=J.LINE),
             dict(t="あとで", d="降ってくる灰に", dc=J.ALERT)],
    ),

    # NARA #43。⚠️ DNA 第56図（p216 の上）と同じ写真の疑い＝c508 は第57図だけに切る（二重使用を避ける）
    "c507": dict(
        t="無人のキャンプも",
        s="エネマン島の建物の被害　1954年",
        photo=P("dmg_eneman"), **ss.kind(P("dmg_eneman")),
        cam="pull",
        side="right", ann_y=356,
        ann=[dict(t="近くの島々", d="木をはぎ取る爆風", dc=J.ALERT),
             dict(t="爆心からの距離", v="20キロあまり", vc=J.AMBER)],
    ),

    # 報告書の第57図（p216 の下だけ。上の第56図は c507 の写真と同じ疑い＝切り落とす）
    "c508": dict(
        t="火事も、起きた",
        s="報告書の第57図　エネマン島の火事の跡",
        photo=ss.page(216), panel=True, trim=(0.07, 0.555, 0.97, 0.995),
        side="right",
        ann=[dict(t="火事の原因", d="電線のショート", dc=J.ALERT),
             dict(t="焼けたもの", d="観測の機械の多く", dc=J.ALERT)],
    ),

    # 🔴 drift（冒頭の地図が戻る）。ロンゲリック＝爆心から東へ250キロ・船＝ビキニから東北東へ157キロ（DNA p212）
    "c509": dict(
        t="光は、遠くからも",
        s="光が見えた場所",
        # ⚠️ 爆心→ロンゲリックの線が上に置いたロンゲラップの札を貫いた（試し焼き）＝札は全部下（MAP_PLACES_LINE）
        fig=("drift", ss.drift_map([
            dict(dim=dict(a="gz", b="rongerik", t="250キロ", d="東"),
                 tag=dict(at="rongerik", t="1分近く", side="above"),
                 move=[dict(kind="sight", a="rongerik", b="gz")]),
            dict(ship=dict(at="ship", t="第五福竜丸"),
                 dim=dict(a="bikini", b="ship", t="157キロ", d="東北東"),
                 move=[dict(kind="sight", a="ship", b="gz")])],
            places=ss.MAP_PLACES_LINE)),
    ),

    # 🔴 drift（同じ地図）。音＝爆心から船へ7、8分・ロンゲリックへ11分（DNA p217）。点は音の届く向き
    "c510": dict(
        t="音は、遅れて届く",
        s="爆発の音が届くまで",
        # ⚠️ 線の出どころに印が無いと、どこから届く音か分からない（試し焼き）＝1段目に「爆心」の札
        fig=("drift", ss.drift_map([
            dict(ship=dict(at="ship", t="第五福竜丸"),
                 tag=[dict(at="gz", t="爆心", side="above"),
                      dict(at="ship", t="7、8分後", side="below")],
                 move=[dict(kind="path", via=["gz", "ship"], sec=2.5)]),
            dict(),
            dict(tag=dict(at="rongerik", t="11分後", side="above"),
                 move=[dict(kind="path", via=["gz", "rongerik"], sec=3.0)])],
            places=ss.MAP_PLACES_LINE,
            note="模式図：点は音の届く向き。島は環礁の中心・船はビキニから東北東へ157キロ（報告書の値）")),
    ),

    # 報告書の第58図（雲の大きさ）。⚠️ 台本 §7 は c511/c512 が逆（§4 が正）
    "c511": dict(
        t="ふくらみ続ける雲",
        s="報告書の第58図　雲の大きさの変化",
        photo=ss.page(218), panel=True, trim=(0.05, 0.075, 0.99, 0.935),
        side="right",
        ann=[dict(t="10分後の雲の幅", v="100キロ超", vc=J.AMBER),
             dict(t="てっぺんの高さ", v="35キロ超", vc=J.AMBER, d="富士山の約10倍")],
    ),

    # NARA #03（艦エステスから・雲の塊と水平線・暗い）。⑤b-3 で c422 と入れ替えた
    "c512": dict(
        t="雲から、何かが",
        s="艦エステスから見た雲と水平線　1954年3月1日",
        photo=P("fb_estes_b"), **ss.kind(P("fb_estes_b")),
        color=1.0,
        side="right", ann_y=380,
        ann=[dict(t="およそ30分後", d="雲から落ちるもの", dc=J.ALERT)],
    ),

    # 報告書の第59図（p219 の上だけ。下の段落は第6章 c611 の頁）
    "c513": dict(
        t="指令所の外は",
        s="報告書の第59図　1時間後の放射線",
        photo=ss.page(219), panel=True, trim=(0.02, 0.04, 0.99, 0.63),
        side="right",
        ann=[dict(t="1時間後", d="指令所のまわりで強まる", dc=J.ALERT),
             dict(t="外と中の差", v="約7000倍", vc=J.AMBER),
             dict(t="中の班", d="壁の内側", dc=J.OK)],
    ),

    # NARA #44（艦モララが別の艦を洗う）
    "c514": dict(
        t="艦隊にも、灰",
        s="艦モララが別の艦を洗う　1954年",
        photo=P("dc_molala"), **ss.kind(P("dc_molala")),
        side="right", ann_y=330,
        ann=[dict(t="艦隊に灰", v="午前8時", vc=J.AMBER),
             dict(t="57キロ先の空母", d="ビキニへ戻る支度", dc=J.TICK),
             dict(t="ヘリコプター", d="呼び戻し", dc=J.ALERT)],
    ),

    # 🔴 決め所。報告書の実物をなぞる型（DNA p217）。文は2行＝読む順に塗る（§5b-36）
    "c515": dict(
        t="降ってきたもの",
        s="午前8時の艦隊の記録",
        fig=("trace", dict(
            page=ss.page(217),
            lines=[(0.1509, 0.5612, 0.8296, 0.58), (0.1133, 0.5848, 0.3839, 0.6037)],
            phrase="灰：ピンの頭ほどの白くざらざらした雪のよう",
            doc=f"{SRC_DNA} 217頁の原文",
            # 切り口は行と行のすきま（「At 0800」の段落の頭から4行）
            crop=(0.08, 0.549, 0.92, 0.651))),
    ),

    # NARA #38（YAG-40 の放水）＝甲板に水を流す装置
    "c516": dict(
        t="水を流しながら、南へ",
        s="艦 YAG-40 の放水　1954年",
        photo=P("dc_yag40_spray"), **ss.kind(P("dc_yag40_spray")),
        side="right", ann_y=356,
        ann=[dict(t="甲板に水", d="流し続ける装置", dc=J.LINE),
             dict(t="下がった先", v="93キロ", vc=J.AMBER, d="全速力で南へ")],
    ),

    # 報告書の第65図（24時間後の艦の位置・横長の頁）
    "c517": dict(
        t="空母の甲板で",
        s="報告書の第65図　24時間後の艦の位置",
        photo=ss.page(230), panel=True, trim=(0.01, 0.05, 0.99, 0.84),
        side="right",
        ann=[dict(t="甲板の排水口", d="灰がたまる", dc=J.ALERT),
             dict(t="早く止めた換気", d="船の中へは多く入らず", dc=J.OK),
             dict(t="洗い終えた日", v="3月4日", vc=J.AMBER)],
    ),

    # NARA #14（艦カーチスで服を脱いだあとの測定）＝縦長＝額装
    "c518": dict(
        t="指令所から、救出",
        s="艦カーチスで服を脱いだあとの測定　1954年",
        photo=P("dc_curtis"), **ss.kind(P("dc_curtis")),
        side="right",
        ann=[dict(t="助け出された班", d="起爆の班", dc=J.INST),
             dict(t="時刻", v="12時半", vc=J.AMBER, d="爆発から6時間近く")],
    ),

    # 報告書の第60図（3時間後の降灰の再現）をカメラで東へなぞる。「とみられている」＝推定と札に残す
    # ⚠️ 見出しに「東へ」と書くと注記の答えを先に言う（check_wording A）
    "c519": dict(
        t="灰を運ぶ雲の行方",
        s="報告書の第60図　3時間後の降灰の再現",
        photo=ss.page(221), panel=True, trim=(0.02, 0.02, 0.99, 0.55),
        cam=EASTWARD,
        side="right",
        ann=[dict(t="雲の向き", d="東へ", dc=J.AMBER),
             dict(t="雲の幅（推定）", v="約160キロ", vc=J.AMBER),
             dict(t="艦隊", d="2度目の灰", dc=J.ALERT)],
    ),

    # 報告書の第61図（6時間後の降灰の再現）。同じくカメラで東へ
    "c520": dict(
        t="灰の先頭は、島を越えた",
        s="報告書の第61図　6時間後の降灰の再現",
        photo=ss.page(223), panel=True, trim=(0.02, 0.52, 0.99, 0.995),
        cam=EASTWARD,
        side="right",
        ann=[dict(t="ロンゲラップまで", v="約190キロ", vc=J.AMBER),
             dict(t="あとの計算", d="昼すぎに灰の先頭が通過", dc=J.ALERT)],
    ),

    # ⚠️ 見出しと札・副題と札で同じ語を持たない（check_dup）
    "c521": dict(
        t="灰の出どころ",
        s="島の灰は、どこから",
        fig=("panel", dict(
            blocks=[dict(k="問い", t="島に降った灰", c=J.LINE),
                    dict(k="2013年の報告書", t="高く昇った雲の上の部分", c=J.AMBER),
                    dict(k="予報", t="上の部分の灰を見込めず", c=J.ALERT)])),
    ),

    # 4K 48.0〜56.0秒（海の上に広がる雲・c110 と別の秒）。章の終わり＝尻で暗転（自動）
    "c522": dict(
        t="空の下に、人がいた",
        s="艦から見た、海に広がる雲　1954年3月1日",
        **ss.vid("c522"),
        color=1.0,
        side="right", ann_y=356,
        ann=[dict(t="灰の向き", d="東へ", dc=J.AMBER),
             dict(t="その空の下", d="漁船と島の人々", dc=J.ALERT)],
    ),

}
