# -*- coding: utf-8 -*-
"""第3章 閉まったように見えるドア c301–c322（22カット）。13本目（トルコ航空981便）。

⚠️ 12本目の中身は `git show 3832147:tools/cuts/c3.py`（⑤b-1 で空にした）。
🔴 ⑤b-2（2026-09-24）：錠の動く模式図（latch）の型見本3カット（c305・c306・c316）を先に書いた。
🔴 ⑤b-3（2026-09-25）：残りの19カットを書いた。
   **錠（latch）**＝c305→c306→c307→c308→c309→c312→c313→c316→c317（同じ錠の絵が状態を変えて戻る）
   **胴体の断面（section）**＝c303（与圧）・c319〜c321（外れる→減圧→床が落ちる）。c109 と同じ絵
   報告書の写真と図＝p90（c301）・p92（c302）・p91（c304）・p94（c310）・p95（c311）・p88 図7（c314）
     ＝引用＝額装・原色。切り出しは `ss.TRIM`（画素で測った）
   筋＝仏 p88 図7（FERMETURE FORCÉE）・上院 p2017〜p2018・p2024。門番＝`tools/check_mech.py`
■ 決め所④ c315 は引用札（quote）：図7の矢印の言葉「BROCHE EN BUTÉE SUR LE FLASQUE」は文字の層で崩れていて
  （「FLASCUE」）なぞる型の行を取れない。図そのものは c314 で見せる
"""
import jiko_style as J
import cuts.ss as ss

NOTE = "模式図：4つのフックのうち1つ。形と大きさは実物どおりではない（報告書の図7の順番）"
SRC = "仏の報告書 図7（p88）・米上院の報告 p2017〜p2018"
SEC_NOTE = "模式図：機体を後ろから見た断面。形と大きさは実物どおりではない"
SEC_SRC = "仏の報告書 p96〜p105"
NOTE_FR = "出典：フランスの最終報告書"

SPEC = {

    # 仏 p90（写真：後部左の貨物ドアの位置）。写真の中の線が扉を指す
    "c301": dict(
        t="主役のドアの場所",
        s="報告書の写真　DC-10の後ろの左側",
        photo=ss.page(90), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="線の先", d="後ろの左の貨物ドア", dc=J.AMBER)],
    ),

    # 仏 p92（写真：開いた貨物ドア）
    "c302": dict(
        t="外へ大きく開く",
        s="報告書の写真　開いた貨物ドア",
        photo=ss.page(92), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="ここから", d="荷物の出し入れ", dc=J.TICK)],
    ),

    # 🔴 断面：与圧（c109 と同じ絵。c109 は「地上と空の上」・ここは言葉「与圧」と力の向き）
    "c303": dict(
        t="ドアを押し出す力",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            steps=[dict(state=dict(press="push"), tag=dict(t="与圧", d="高い空での機内の圧力")),
                   dict(tag=dict(t="外へ向かう力", d="ドアを押す"))],
            note=SEC_NOTE, src="米上院の報告 p2014")),
    ),

    # 仏 p91（写真：ドアの内側・フックと動かす仕組み）。数は仏 p64
    "c304": dict(
        t="力を受けとめるフック",
        s="報告書の写真　貨物ドアの内側",
        photo=ss.page(91), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="ドアの下の縁", v="4つ", vc=J.AMBER, d="フック"),
             dict(t="引っかける先", d="胴体の側", dc=J.TICK)],
    ),

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

    # ①ロックピン（1行）。ひと動きなので、ピンだけでなく全部が動く＝札はピンだけ
    "c307": dict(
        t="フックを止めるピン",
        s="ハンドルの役目の1つ目",
        fig=("latch", dict(
            start=dict(hook="closed"),
            steps=[dict(state=dict(handle="down", pin="in", vent="closed", lamp="off"),
                        tag=dict(t="① ロックピン", d="フックを動かなくする", at="pin"))],
            note=NOTE, src=SRC)),
    ),

    # ②通気扉 → ③警告灯（2行＝2段。灯りは2段目で消す）
    "c308": dict(
        t="小さな扉と、灯り",
        s="ハンドルの役目の2つ目と3つ目",
        fig=("latch", dict(
            start=dict(hook="closed"),
            steps=[dict(state=dict(handle="down", pin="in", vent="closed"),
                        tag=dict(t="② 通気扉が閉まる", at="vent")),
                   dict(state=dict(lamp="off"), tag=dict(t="③ 警告灯が消える", at="lamp"))],
            note=NOTE, src=SRC)),
    ),

    # 設計のねらい（上院 p2014）：錠がかからなければハンドルは途中で止まり、通気扉は開いたまま＝空気が逃げる
    "c309": dict(
        t="飛ばせないための扉",
        s="通気扉のねらい",
        fig=("latch", dict(
            start=dict(hook="short"),
            steps=[dict(state=dict(handle="part", pin="butt"), tag=dict(t="ピンが入らない", at="pin")),
                   dict(state=dict(air="leak"), tag=dict(t="開いたまま＝空気が逃げる", at="vent"))],
            note=NOTE, src="米上院の報告 p2014・p2017〜p2018")),
    ),

    # 仏 p94（写真：のぞき窓からピンを確かめる人＝職務中の実演）。窓を全機に付けたのは上院 p2035
    "c310": dict(
        t="全機に付いた窓",
        s="報告書の写真　貨物ドアの下の窓",
        photo=ss.page(94), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="取り付け", v="1972年の夏", vc=J.AMBER),
             dict(t="付けた機体", d="当時のDC-10すべて", dc=J.TICK)],
    ),

    # 仏 p95（写真：航空機関士の上のパネルの警告灯）
    "c311": dict(
        t="操縦室の警告灯",
        s="報告書の写真　操縦室の上のパネル",
        photo=ss.page(95), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="航空機関士", d="エンジンや電気の係", dc=J.TICK),
             dict(t="灯りが点く", d="閉まりきっていない合図", dc=J.ALERT)],
    ),

    # 3つがそろえば「閉まった」（ふつうに閉めた場合）
    "c312": dict(
        t="3つがそろえば",
        s="外から分かる「閉」の印",
        fig=("latch", dict(
            start=dict(hook="closed"),
            steps=[dict(state=dict(handle="down", pin="in", vent="closed", lamp="off"),
                        tag=[dict(t="倒れた", at="handle"), dict(t="閉まった", at="vent"),
                             dict(t="消えた", at="lamp")]),
                   dict(tag=dict(t="＝閉まっているように見える", at="tube"))],
            note=NOTE, src=SRC)),
    ),

    # フックが回りきらないとき（上院 p2015・p2025・仏 p97〜p98）。3行＝3段
    #   ⚠️ 札の置き場：hook2（上）と hook（下）を上下に重ねる。motor の置き場は幅100px＝長い札は縮む
    "c313": dict(
        t="回りきらないフック",
        s="閉める手順の弱点",
        fig=("latch", dict(
            steps=[dict(state=dict(hook="short", motor="run"), tag=dict(t="回りきらない", at="hook2")),
                   dict(tag=dict(t="電気が弱い（何度か報告）", at="hook")),
                   dict(state=dict(handle="part", pin="butt"),
                        tag=dict(t="ピンは入れない", d="本来はハンドルも倒れない", at="pin"))],
            note=NOTE, src="米上院の報告 p2015・p2025・仏の報告書 p97〜p98")),
    ),

    # 仏 p88 図7「FERMETURE FORCÉE」（引用＝額装・原色）
    "c314": dict(
        t="図7が描く、無理な閉め方",
        s="フランスの報告書の図7",
        photo=ss.page(88), panel=True, color=1.0,
        side="right", ann_y=330,
        ann=[dict(t="図の題", v="無理に閉めた", vc=J.ALERT),
             dict(t="たわむもの", d="ピンを動かす軸", dc=J.AMBER)],
    ),

    # 🔴 決め所④（台本 §2 #4・仏 p88「BROCHE EN BUTÉE SUR LE FLASQUE」・p80）
    "c315": dict(
        t="ハンドルだけが倒れる",
        s="図7の矢印の言葉",
        fig=("quote", dict(
            phrase="無理に閉めると、ピンは縁に当たって止まる",
            who="フランスの事故調査委員会",
            when="1976年",
            doc="最終報告書の図7")),
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

    # 灯りも消える（上院 p2024・p2028）。3ミリ＝8分の1インチ未満（台本 §9）
    #   2段目の札は操縦室の枠の下（lamp の置き場は1段目が使う）
    "c317": dict(
        t="灯りまで、消える",
        s="操縦室の灯りの仕組み",
        fig=("latch", dict(
            start=dict(hook="short", handle="down", pin="butt", tube="bent", vent="closed"),
            steps=[dict(state=dict(lamp="off"), tag=dict(t="たわんだ仕組みが押す", at="lamp")),
                   dict(tag=dict(t="3ミリ未満で入るスイッチ", at=(1530, 740, "middle", 440)))],
            rel=[dict(t="3ミリ", src="米上院の報告 p2024（8分の1インチ未満＝3.2ミリ未満）")],
            note=NOTE, src="米上院の報告 p2024・p2028")),
    ),

    # 仏 p104（本文）：見かけと実際（「ありえた」の留保を残す §5b-27b）
    "c318": dict(
        t="報告書も書いた弱点",
        s="フランスの報告書 104頁",
        fig=("beforeafter", dict(
            a=dict(k="見かけ", t="閉まっている", lines=["通気扉は閉まる", "錠もかかって見える"], v="", c=J.LINE),
            b=dict(k="実際には", t="錠はかかっていない", lines=["フックは閉まりきらない", "ピンも入らない", "ことがありえた"],
                   v="", c=J.ALERT),
            arrow=False, note=f"{NOTE_FR} 104頁")),
    ),

    # 🔴 断面：上るにつれて差が大きくなる → ドアが外へ飛ぶ（与圧 push ⇒ ドア on＝2段目で与圧の矢印は消す）
    "c319": dict(
        t="空の上で、押し開けられる",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            steps=[dict(state=dict(press="push"), tag=dict(t="上るほど", d="機内と外の差が大きくなる")),
                   dict(state=dict(press="none", door="gone"), tag=dict(t="ドアが外へ飛ぶ", d="フックが押し開けられる"))],
            note=SEC_NOTE, src=SEC_SRC)),
    ),

    # 🔴 断面：減圧 → 床に上から圧力
    "c320": dict(
        t="空気が抜ける",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            start=dict(door="gone"),
            steps=[dict(state=dict(air="out"), tag=dict(t="減圧", d="貨物室の気圧が外と同じに")),
                   dict(state=dict(floor="push"), tag=dict(t="床に上から圧力", d="客室の側が高いまま"))],
            note=SEC_NOTE, src="仏の報告書 p99・p104")),
    ),

    # 🔴 断面：床が落ちる → 床下のケーブル（札に「操縦のケーブル」と書かない＝絵の名札と同じ語）
    "c321": dict(
        t="床とともに落ちるもの",
        s="胴体を輪切りにした図",
        fig=("section", dict(
            start=dict(door="gone", air="out", floor="push"),
            steps=[dict(state=dict(floor="down"), tag=dict(t="床が落ちる", d="下の貨物室へ")),
                   dict(state=dict(cable="hurt"), tag=dict(t="ケーブルが傷む", d="床の下にまとめて通っていた"))],
            note=SEC_NOTE, src="仏の報告書 p104〜p105")),
    ),

    # 章の橋（副題は10本目からの型「ここまでと、この先」）
    "c322": dict(
        t="パリより前へ",
        s="ここまでと、この先",
        fig=("panel", dict(
            blocks=[dict(k="弱点", t="閉まって見えても、錠はかからない", c=J.ALERT),
                    dict(k="鍵", t="前にも起きていたこと", v="第4章", c=J.AMBER)],
            cols=2)),
    ),

}
