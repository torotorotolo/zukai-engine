# -*- coding: utf-8 -*-
"""第3章 小さな空港に、5機が並んだ c301–c322（22カット）。9本目（テネリフェ）。

■ 🔴 いちばん効く図＝ c304（滑走路と誘導路 C-1〜C-4）と c316（滑走路の高さの断面）
  - c304 … `runway` 型。⚠️ **報告書に空港全体の平面図が無い**（p59 は事故現場付近の
    1:2000 の詳細図で、C-1・C-2 が描かれていない）＝道の位置と角度は模式と断る。
    🔴 C-3 を「148度」に描かない（道は全部、滑走路に直角の短い帯）。
  - c316 … 報告書 p16「30側の端 2,001フィート（610m）・12側の端 2,064フィート（629m）・
    いちばん高い所は C-3 の出口のあたり」。⚠️ **いちばん高い所の数値は書かれていない**
    ＝数を出さない。高さは強めて描く（note で断る）。
■ 台本の写真12カットのうち3カットを図にした（写真の欄に当てる写真が無い／話が図のもの）
  - c307 … 「通り道が駐車場になる」＝図。地に `losrodeos_now_14`（BACKDROP）
  - c310 … 5機→2機＝図。地に `losrodeos_now_06`（BACKDROP）
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
RW_NOTE = "模式図（道の位置と角度は正確ではない）"


def five(dim=False):
    """誘導路に並んだ5機（左＝滑走路の入り口の側が前）。報告書 p3・p28。"""
    small = J.LINE_DIM if dim else J.LINE
    return [dict(at=0.06, on="twy", head=180, t="KLM", c=J.AMBER, s=0.9),
            dict(at=0.15, on="twy", head=180, t="737", c=small, s=0.5),
            dict(at=0.23, on="twy", head=180, t="727", c=small, s=0.56),
            dict(at=0.32, on="twy", head=180, t="DC-8", c=small, s=0.64),
            dict(at=0.43, on="twy", head=180, t="パンナム", c=J.INK_W, s=0.9)]


SPEC = {

    # 主題（機体）は右上＝注記は左。群衆は1930年の見物人。
    "c301": dict(
        t="1930年に、最初の飛行機が降りた",
        s="本土からカナリア諸島への最初の商業飛行　1930年撮影",
        photo=P("losrodeos_1930_01"), bias=0.30, side="left", ann_y=356,
        **ss.kind(P("losrodeos_1930_01")),
        ann=[dict(t="場所", d="テネリフェ島の北側", dc=J.INK_W, ds=36)],
    ),

    # c207 と同じ写真＝寄って山を見せる（別の絵にする）。
    "c302": dict(
        t="山にはさまれた、谷の底の空港",
        s="現在のテネリフェ北空港と山（丘の上から）　2012年撮影",
        photo=P("losrodeos_now_01"), bias=0.30, xbias=0.60, zoom=1.40,
        side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_01")),
        ann=[dict(t="空港の標高", v="632メートル", vc=J.AMBER, vs=80)],
    ),

    "c303": dict(
        t="滑走路は1本、向きで2つの名前",
        s="ロス・ロデオス空港の滑走路",
        fig=("runway", dict(
            steps=[dict(dim=[dict(a=0.0, b=1.0, t="3,400 × 45メートル")]),
                   dict(path=[dict(on="rwy", a=0.06, b=0.94, c=J.AMBER)],
                        mark=[dict(at=0.5, y="above", t="12＝およそ120度へ進む", c=J.AMBER)]),
                   dict(mark=[dict(at=0.5, y="below", t="逆から入れば30＝およそ300度",
                                   c=J.INK_W)])],
            taxiway=False, note="模式図", src="事故報告書 p16")),
    ),

    # 🔴 この回でいちばん効く図の1枚目。
    "c304": dict(
        t="誘導路と、つなぐ道が4本",
        s="滑走路のわきの道を、上から見る",
        fig=("runway", dict(
            steps=[dict(mark=[dict(at=0.80, y="above", t="平行誘導路", c=J.INK_W)]),
                   dict(mark=[dict(at=0.80, y="below", t="滑走路", c=J.INK_W)]),
                   dict(hot=[("C-1", J.AMBER), ("C-2", J.AMBER), ("C-3", J.AMBER),
                             ("C-4", J.AMBER)])],
            note=RW_NOTE + "　駐機場に近いほうから C-1〜C-4",
            src="事故報告書 p16・p59")),
    ),

    "c305": dict(
        t="駐機場は、すっかり埋まった",
        s="現在のテネリフェ北空港の駐機場　2009年撮影",
        photo=P("losrodeos_now_10"), bias=0.80, side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_10")),
        ann=[dict(t="入りきらない機体", d="誘導路に並ぶ", dc=J.AMBER, ds=40)],
    ),

    "c306": dict(
        t="ジャンボ機の2機は、列の両端",
        s="誘導路に並んだ機体（左が滑走路の入り口の側）",
        fig=("runway", dict(
            steps=[dict(planes=five(dim=True)),
                   dict(mark=[dict(at=0.25, y="gap", t="747は、KLMとパンナムの2機",
                                   c=J.AMBER)])],
            exits=False, note=RW_NOTE, src="事故報告書 p28")),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_14 の別の寄り）
    "c307": dict(
        t="通り道が、駐車場になる",
        s="平行誘導路の、二つの使われ方",
        fig=("beforeafter", dict(
            a=dict(k="ふだん", t="通り道", lines=["機体が走って出ていく"], c=J.LINE),
            b=dict(k="この日", t="駐車場", lines=["機体が停まったまま"], c=J.ALERT),
            note="事故報告書 p28")),
    ),

    # 🔴 2026-09-17（⑤c B-05）：グランカナリア空港の管制塔の写真だと、**呼んだ相手の塔**に
    #    見えた（呼んだのはロス・ロデオスの塔。その塔の写真は0点＝`photos.md` l.70）。
    #    → 写真をやめ、誰が誰を呼んだかを無線の図で見せる（c602 と同じ作り・順番だけ）。
    "c308": dict(
        t="パンナムが、管制塔を呼んだ",
        s="パンナムから管制塔への無線",
        fig=("radio", dict(
            lanes=["パンナム", "管制塔"],
            events=[dict(lane=0, a=1.0, b=2.2, t="エンジンをかけたい", c=J.LINE),
                    dict(lane=1, a=3.0, t="許可", c=J.OK)],
            t0=0.4, t1=5.6,
            note="順番だけ（間隔は正確ではない）", src="事故報告書 p28")),
    ),

    # 🔴 2026-09-17（⑤c B-12）：レーダーの鉄塔の写真＝語りに「レーダー」は0回。c308 の図の続き。
    "c309": dict(
        t="許可は出ても、動けるとは限らない",
        s="管制塔が付けた注意",
        fig=("radio", dict(
            lanes=["パンナム", "管制塔"],
            events=[dict(lane=0, a=1.0, b=2.2, t="エンジンをかけたい", c=J.LINE, pre=True),
                    dict(lane=1, a=3.0, t="許可", c=J.LINE, pre=True),
                    dict(lane=1, a=3.8, b=5.2, t="地上走行での問題", d="前にKLM機がいる",
                         c=J.ALERT)],
            t0=0.4, t1=5.6,
            note="順番だけ（間隔は正確ではない）", src="事故報告書 p28")),
    ),

    # 図＋地（BACKDROP＝losrodeos_now_06 の別の寄り）
    "c310": dict(
        t="残ったのは、747の2機だけ",
        s="誘導路の5機が、どう減ったか",
        fig=("process", dict(
            steps=[dict(t="並んでいた", v="5機", c=J.LINE),
                   dict(t="先に出ていった", v="3機", c=J.LINE),
                   dict(t="残った", v="2機", d="前にKLM、うしろにパンナム",
                        c=J.ALERT)],
            note="事故報告書 p3・p28")),
    ),

    # 左に走査のごみ（x 0.1〜0.2）＝右へ寄って外へ出す。
    "c311": dict(
        t="パンナムの2人が、機体を降りた",
        s="パンナムの747　1970年撮影（スキポール空港）",
        photo=P("panam_ams1970_06"), bias=0.50, xbias=1.0, zoom=1.30,
        side="left", ann_y=356,
        **ss.kind(P("panam_ams1970_06")),
        ann=[dict(t="降りた人", d="副操縦士と航空機関士", dc=J.INK_W, ds=36)],
    ),

    "c312": dict(
        t="通れるかは、地面で確かめた",
        s="二機のあいだのすき間",
        fig=("quote", dict(
            phrase="降りて、すき間を測った",
            rows=[("誰が", "パンナムの副操縦士と航空機関士", J.INK_W),
                  ("何を", "KLM機が空けていたすき間", J.LINE),
                  ("出どころ", "事故報告書 p3", J.DOC)],
            paper=True)),
    ),

    "c313": dict(
        t="結果は、通れない",
        s="測ったすき間",
        fig=("absent", dict(
            mode="single",
            items=[dict(t="747が通れる幅", d="足りなかった", ok=False, c=J.ALERT)],
            lead="KLM機が動くまで、出られない", note="事故報告書 p3")),
    ),

    "c314": dict(
        t="KLMの準備まで、およそ1時間",
        s="パンナムの747　1970年撮影（スキポール空港）",
        photo=P("panam_ams1970_05"), bias=0.55, side="right", ann_y=356,
        **ss.kind(P("panam_ams1970_05")),
        ann=[dict(t="KLMが準備を始めた", v="約1時間後", vc=J.AMBER, vs=80),
             dict(t="パンナムの乗客", d="機内で待ち続けた", dc=J.INK_W, ds=34)],
    ),

    # pr09 と同じ写真＝寄って滑走路の面を見せる。
    "c315": dict(
        t="滑走路にも、高い所と低い所",
        s="現在のテネリフェ北空港の滑走路　2012年撮影",
        photo=P("losrodeos_now_02"), bias=0.62, xbias=0.30, zoom=1.50,
        side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_02")),
        ann=[],
    ),

    # 🔴 いちばん高い所の数値は報告書に無い＝目盛りに出さない。高さは強めて描いた略図。
    "c316": dict(
        t="真ん中が、ふくらんでいる",
        s="滑走路の高さを、横から見る",
        fig=("graph", dict(
            # ⚠️ 頂は空港の標高（632m）を超えない高さに置く（数値は出さない）。
            series=[dict(pts=[(0, 629), (800, 631), (1700, 632), (2500, 625),
                              (3400, 610)],
                         t="", c=J.INK_W, sw=6, area=True)],
            xr=(-150, 3550), yr=(600, 640),
            xticks=[(0, "12側の端"), (1700, "C-3のあたり"), (3400, "30側の端")],
            yticks=[(610, "610"), (629, "629")],
            legend=False,
            # ⚠️ 2026-09-17（⑤c' E-14）：線は左上から 610 の点へ下りてくる＝札を点の左上に置くと
            #    線が「ートル」を貫いた。→ 線の下（面の中）へ。629 も線まで 1.7px だったので 6px 上げる
            marks=[dict(x=3400, y=610, t="610メートル", c=J.AMBER, anchor="end", dx=-26,
                        dy=44),
                   dict(x=0, y=629, t="629メートル", c=J.AMBER, dx=26, dy=-30),
                   dict(x=1700, y=632, t="いちばん高い", c=J.ALERT, anchor="middle",
                        dx=0, dy=-30)],
            note="事故報告書 p16　たて軸＝高さ（メートル）。高さを強めた略図（線の形は模式）")),
    ),

    "c317": dict(
        t="雲が降りると、見えなくなる",
        s="管制塔と滑走路",
        fig=("runway", dict(
            steps=[dict(cloud=dict(a=0.0, b=1.0, t="地面につく雲"),
                        planes=[dict(at=0.80, on="rwy", head=0, c=J.LINE_DIM, lab=False)],
                        mark=[dict(at=0.80, y="gap", t="管制塔から見えない", c=J.ALERT)])],
            tower=True, exits=False, note=RW_NOTE, src="事故報告書 p32")),
    ),

    "c318": dict(
        t="誘導路の代わりに、滑走路を走る",
        s="誘導路がふさがったときの通り道",
        fig=("runway", dict(
            steps=[dict(mark=[dict(at=0.66, y="top", t="誘導路が使えない", c=J.ALERT)]),
                   dict(path=[dict(on="rwy", a=0.08, b=0.95, c=J.AMBER)],
                        mark=[dict(at=0.50, y="below", t="着陸機と同じ1本を走る",
                                   c=J.AMBER)])],
            exits=False, note=RW_NOTE, src="事故報告書 p32・p40")),
    ),

    "c319": dict(
        t="走っているあいだ、誰も降りられない",
        s="現在のテネリフェ北空港に着陸する機体　2011年撮影",
        photo=P("losrodeos_now_12"), bias=0.50, side="left", ann_y=356,
        **ss.kind(P("losrodeos_now_12")),
        ann=[dict(t="管制官がしたいこと", d="早く滑走路から出す", dc=J.AMBER, ds=36)],
    ),

    "c320": dict(
        t="KLMは、燃料を足すと決めた",
        s="動き出す前の判断",
        fig=("moment", dict(
            clock="—", label="燃料を足す",
            facts=[dict(t="決めたのは", v="KLM", c=J.AMBER)],
            sub="事故報告書 p28")),
    ),

    "c321": dict(
        t="すぐ隣へ行くのに、ここで給油",
        s="博物館に保存された747の試作機のエンジン　2010年撮影",
        photo=P("engine_747_05"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("engine_747_05")),
        ann=[dict(t="給油する場所", d="テネリフェ", dc=J.AMBER, ds=44)],
    ),

    "c322": dict(
        t="なぜ、足したのか",
        s="次の章で見ること",
        fig=("panel", dict(
            blocks=[dict(k="理由", t="報告書が書き残している", v="", c=J.DOC),
                    dict(k="その結果", t="うしろの機体が止まり続ける", v="", c=J.ALERT)],
            note="事故報告書 p28", cols=2)),
    ),
}
