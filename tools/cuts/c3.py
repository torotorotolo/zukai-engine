# -*- coding: utf-8 -*-
"""第3章 閉まったように見えるドア c301–c322（22カット）。13本目（トルコ航空981便）。

⚠️ 12本目の中身は `git show 3832147:tools/cuts/c3.py`（⑤b-1 で空にした）。
🔴 ⑤b-2（2026-09-24）：**錠の動く模式図（latch）の型見本3カットだけ**先に書いた（型ごとに1枚焼いて見る §5b-28）。
   残りの19カットは ⑤b-3 で書く。c305→c306→（c307〜c313）→c316→c317 と**同じ錠の絵が状態を変えて戻る**。
   筋＝仏 p88 図7（FERMETURE FORCÉE）・上院 p2017〜p2018。門番＝`tools/check_mech.py`
"""
import cuts.ss as ss  # noqa: F401

NOTE = "模式図：4つのフックのうち1つ。形と大きさは実物どおりではない（報告書の図7の順番）"
SRC = "仏の報告書 図7（p88）・米上院の報告 p2017〜p2018"

SPEC = {

    # 閉める手順①：スイッチ → モーターがフックを回して受けに掛ける
    "c305": dict(
        t="まず、フックが掛かる",
        s="閉める手順の1つ目",
        fig=("latch", dict(
            steps=[dict(tag=dict(t="スイッチ", at="motor")),
                   dict(state=dict(hook="closed", motor="run"), tag=dict(t="フックが受けに掛かる", at="hook"))],
            note=NOTE, src=SRC)),
    ),

    # 閉める手順②：ハンドルを倒す＝ピン・通気扉・灯りをひと動きで
    "c306": dict(
        t="ハンドル1本で、3つ",
        s="閉める手順の2つ目",
        fig=("latch", dict(
            start=dict(hook="closed"),
            steps=[dict(state=dict(handle="down", pin="in", vent="closed", lamp="off"),
                        tag=dict(t="ハンドルを倒す", at="handle")),
                   dict(tag=[dict(t="① ピン", at="pin"), dict(t="② 通気扉", at="vent"),
                             dict(t="③ 灯り", at="lamp")])],
            note=NOTE, src=SRC)),
    ),

    # 見かけは「閉」：フックが回りきらず、ピンは縁で止まる。ハンドルは軸がたわんで収まり、通気扉も閉まる
    #   ⚠️ 灯りはまだ点いたまま（灯りが消えるのは次の c317「たわんだ仕組みに押されて」）
    "c316": dict(
        t="見かけは「閉」",
        s="フックが回りきらないまま閉めると",
        fig=("latch", dict(
            start=dict(hook="short"),
            steps=[dict(state=dict(handle="down", pin="butt", tube="bent", vent="closed"),
                        tag=dict(t="ハンドルは収まる", at="handle")),
                   dict(tag=dict(t="通気扉も閉まる", at="vent")),
                   dict(tag=dict(t="ピンは縁で止まったまま", at="pin"))],
            note=NOTE, src=SRC)),
    ),

}
