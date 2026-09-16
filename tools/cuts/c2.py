# -*- coding: utf-8 -*-
"""第2章 ラスパルマスの爆弾 c201–c220（20カット）。9本目（テネリフェ）。

■ 台本の写真12カットのうち、2カットを図にした（章の写真が60%で多いので）
  - c201 … 距離の話＝地図。地に `laspalmas_now_11`（BACKDROP）
  - c208 … 「上空で待てないか」とたずねた話＝写真（グランカナリアのタラップ）は対象そのものでない
  - c210 … 乗り継ぎのカード＝図。地に `losrodeos_now_07`（BACKDROP）
■ 5機の並び（c214・c216）は `runway` 型。KLM機が「パンナム機と滑走路の入り口のあいだ」
  （報告書 p3）＝入り口のある12側（左）から KLM・737・727・DC-8・パンナム。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
RW_NOTE = "模式図（道の位置と角度は正確ではない）"


def five(n=5):
    """誘導路に並んだ機体（左＝滑走路の入り口の側が前）。"""
    ps = [dict(at=0.06, on="twy", head=180, t="KLM", c=J.AMBER, s=0.9),
          dict(at=0.15, on="twy", head=180, t="737", c=J.LINE, s=0.5),
          dict(at=0.23, on="twy", head=180, t="727", c=J.LINE, s=0.56),
          dict(at=0.32, on="twy", head=180, t="DC-8", c=J.LINE, s=0.64),
          dict(at=0.43, on="twy", head=180, t="パンナム", c=J.INK_W, s=0.9)]
    return ps[:n]


SPEC = {

    # 図＋地（BACKDROP＝laspalmas_now_11）
    "c201": dict(
        t="テネリフェから、隣の島の空港まで",
        s="ラスパルマス空港の場所",
        fig=("mapfig", dict(
            points=[dict(x=0.26, y=0.32, t="テネリフェ島", d="ロス・ロデオス空港", c=J.INK_W),
                    dict(x=0.70, y=0.66, t="グランカナリア島", d="ラスパルマス空港",
                         c=J.AMBER)],
            link=(0, 1), scale="飛行機でおよそ25分",
            note="上が北・右が東（縮尺は正確ではない）　事故報告書 p28")),
    ),

    "c202": dict(
        t="旅客ターミナルで、爆弾が爆発",
        s="現在のグランカナリア空港の出発ホール　2010年撮影",
        photo=P("laspalmas_now_01"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("laspalmas_now_01")),
        ann=[dict(t="その日", v="3月27日", vc=J.ALERT, vs=88)],
    ),

    "c203": dict(
        t="仕掛けた人は、書かれていない",
        s="現在のグランカナリア空港の管制塔　2012年撮影",
        photo=P("laspalmas_now_08"), side="right", ann_y=356,
        **ss.kind(P("laspalmas_now_08")),
        ann=[dict(t="報告書が書いていること", d="爆発と閉鎖", dc=J.DOC, ds=40)],
    ),

    "c204": dict(
        t="爆発したのは、一つだけ",
        s="この時点で分かっていたこと",
        fig=("absent", dict(
            mode="pair",
            items=[dict(t="爆発した爆弾", d="旅客ターミナル", ok=True, n=1, c=J.ALERT),
                   dict(t="二つ目", d="この時点では知らせだけ", ok=False, c=J.TICK)],
            note="事故報告書 p3・p28")),
    ),

    "c205": dict(
        t="空港に届いた、別の知らせ",
        s="ラスパルマス空港",
        fig=("quote", dict(
            phrase="二つ目の爆弾の予告があった",
            rows=[("場所", "グランカナリア島のラスパルマス空港", J.INK_W),
                  ("そのあと", "空港は閉められた", J.LINE),
                  ("出どころ", "事故報告書 p3・p28", J.DOC)],
            paper=True)),
    ),

    "c206": dict(
        t="行き先を失った便",
        s="ラスパルマスへ向かっていた便",
        fig=("process", dict(
            steps=[dict(t="空港を閉める", d="ラスパルマス空港", c=J.ALERT),
                   dict(t="行き場を失う", d="空を飛んでいた便", c=J.LINE),
                   dict(t="行き先を変える", d="大部分がテネリフェ", c=J.AMBER)],
            note="事故報告書 p28")),
    ),

    "c207": dict(
        t="回された先は、ロス・ロデオス空港",
        s="現在のテネリフェ北空港（丘の上から）　2012年撮影",
        photo=P("losrodeos_now_01"), bias=0.55, side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_01")),
        ann=[dict(t="KLM機が着いた", v="13:38", vc=J.AMBER, vs=92),
             dict(t="パンナム機が着いた", v="14:15", vc=J.INK_W, vs=92)],
    ),

    # 台本の欄は写真（グランカナリアの搭乗口）。話は「上空で待てないか」＝図にした。
    "c208": dict(
        t="パンナムは、上空で待ちたかった",
        s="パンナムの乗員がたずねたことと、その結果",
        fig=("beforeafter", dict(
            a=dict(k="たずねたこと", t="上空で待てないか",
                   lines=["ラスパルマスが開くのを"], c=J.LINE),
            b=dict(k="結局", t="テネリフェに降りた", lines=["14:15に着陸"], c=J.AMBER),
            arrow=False, note="操縦室の録音の書き起こし／事故報告書 p3")),
    ),

    "c209": dict(
        t="KLMの乗客は、ターミナルへ",
        s="現在のテネリフェ北空港のターミナル　2003年撮影",
        photo=P("losrodeos_now_07"), side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_07")),
        ann=[dict(t="機内から出られるまで", v="約20分", vc=J.AMBER, vs=88),
             dict(t="運び方", d="バス", dc=J.INK_W, ds=40)],
    ),

    # 図＋地（BACKDROP＝losrodeos_now_07）
    "c210": dict(
        t="一人ずつ、カードを渡された",
        s="バスを降りたKLMの乗客",
        fig=("process", dict(
            steps=[dict(t="バスを降りる", d="ターミナルの前", c=J.LINE),
                   dict(t="カードを受け取る", d="4805便の乗り継ぎの客", c=J.AMBER)],
            note="事故報告書 p3")),
    ),

    "c211": dict(
        t="パンナムの乗客は、降りなかった",
        s="二機の乗客が待った場所",
        fig=("beforeafter", dict(
            a=dict(k="KLM機", t="ターミナル", lines=["バスで運ばれた", "カードを渡された"],
                   c=J.AMBER),
            b=dict(k="パンナム機", t="機内のまま", lines=["一人も降りていない",
                                                        "着陸から3時間近く"],
                   c=J.INK_W),
            arrow=False, note="事故報告書 p3")),
    ),

    "c212": dict(
        t="駐機場は、回された機体でいっぱい",
        s="現在のテネリフェ北空港の駐機場　2003年撮影",
        photo=P("losrodeos_now_06"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_06")),
        ann=[dict(t="報告書の言葉", d="「飽和した」", dc=J.DOC, ds=48)],
    ),

    "c213": dict(
        t="KLM機は、誘導路の端へ",
        s="現在のテネリフェ北空港の誘導路　2013年撮影",
        photo=P("losrodeos_now_14"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_14")),
        ann=[dict(t="停められた場所", d="平行誘導路の端", dc=J.AMBER, ds=40)],
    ),

    "c214": dict(
        t="うしろに、3機が並んだ",
        s="誘導路に停められた機体の順",
        fig=("runway", dict(
            steps=[dict(planes=five(2)),
                   dict(planes=five(4)[2:])],
            exits=False,
            note=RW_NOTE + "　737＝ブラーテンス／727＝スターリング／DC-8＝SATA",
            src="事故報告書 p28")),
    ),

    "c215": dict(
        t="いちばんうしろに、パンナム機",
        s="パンナムの747　1970年撮影（スキポール空港）",
        photo=P("panam_ams1970_01"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("panam_ams1970_01")),
        ann=[dict(t="並び", d="パンナム機の前にKLM機", dc=J.INK_W, ds=36)],
    ),

    "c216": dict(
        t="前が動かないと、出られない",
        s="誘導路の並び（左が滑走路の入り口の側）",
        fig=("runway", dict(
            steps=[dict(planes=five()),
                   dict(mark=[dict(at=0.25, y="gap", t="追い越せない一本道", c=J.ALERT)])],
            exits=False, note=RW_NOTE, src="事故報告書 p3・p28")),
    ),

    # ⚠️ 看板「Aeropuerto de Gran Canaria」が左上（主題そのもの）。見出しの帯とぶつかるなら ⑤c で寄せる。
    "c217": dict(
        t="ラスパルマス空港が、また開いた",
        s="現在のグランカナリア空港　2012年撮影",
        photo=P("laspalmas_now_14"), bias=0.90, side="right", ann_y=356,
        **ss.kind(P("laspalmas_now_14")),
        ann=[dict(t="開いた時刻", d="報告書に書かれていない", dc=J.TICK, ds=34)],
    ),

    "c218": dict(
        t="KLMの乗客は、機内に戻った",
        s="現在のテネリフェ北空港（ターミナルから駐機場）　2009年撮影",
        photo=P("losrodeos_now_11"), bias=0.60, side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_11")),
        ann=[dict(t="戻らなかった人", v="1人", vc=J.AMBER, vs=110)],
    ),

    "c219": dict(
        t="テネリフェに、1人だけ残った",
        s="KLM機に戻らなかった人",
        fig=("absent", dict(
            mode="single",
            items=[dict(t="この人の名前", d="報告書の写しで伏せてある", ok=False, c=J.TICK)],
            lead="旅行会社の添乗員　1人", note="事故報告書 p3")),
    ),

    "c220": dict(
        t="この時点では、まだ遅れだけ",
        s="二機が置かれていた状況",
        fig=("panel", dict(
            blocks=[dict(k="場所", t="回された先の空港", v="", c=J.INK_W),
                    dict(k="乗客", t="待たされている", v="", c=J.LINE),
                    dict(k="予定", t="狂っている", v="", c=J.AMBER)],
            note="事故報告書 p28", cols=3)),
    ),
}
