# -*- coding: utf-8 -*-
"""第5章 4,500時間 c501–c529（29カット）。

■ この章の役目
  噂③「引き揚げないのは、見せられないものがあるからではないか」。
  答えは**道具の性能**で出す。隠したかどうかではなく、**探せたかどうか**の話にする。
  🔴 c527「これは道具の限界であって、意思の問題ではない」が章の着地。

■ 数字の出どころ（すべて実測で確かめた）
  17箇所 … 本文2.4.4.2 ／ 調査期間 昭和60年11月1日〜20日 … 本文1.2.2
  分解能 1.1m×1.3m・必要な大きさ 5.5m×6.5m・撮影幅1.5m・2kt・4,500時間・750日
      … 解説書 §10（表4）
  落下物の重さ（APU 250kg／アクチュエータ 40kg／トーション・ボックス 900kg）
      … 解説書 §10 表5
"""
import jiko_style as J

SPEC = {

    "c501": dict(
        t="垂直尾翼の一部は海に落ちた",
        s="写真-23　垂直尾翼展開",
        photo="ja123/p023.jpg", panel=True, side="right",
        ann=[dict(t="落ちた先", v="相模湾", vc=J.INK_W, vs=76),
             dict(t="いまも", d="引き揚げられていない", dc=J.ALERT, ds=34)],
    ),

    "c502": dict(
        t="こう言われることがある",
        s="出どころは書籍やネット上の投稿",
        fig=("panel", dict(blocks=[
            dict(k="噂", c=J.ALERT, t="隠したいものが沈んでいる")],
            lead="言われていること")),
    ),

    "c503": dict(
        t="調査は事故の年に行われた",
        s="付図-21　相模湾海底調査区域",
        photo="ja123/f021.jpg", panel=True, side="right",
        ann=[dict(t="いつ", v="1985年", vc=J.INK_W, vs=84),
             dict(t="範囲", d="残骸が沈んでいる可能性のある海域", dc=J.LINE,
                  ds=32)],
    ),

    "c504": dict(
        t="11月1日から20日まで",
        s="本文1.2.2　昭和60年",
        fig=("panel", dict(blocks=[
            dict(k="船", c=J.INST, t="海上保安庁", v="測量船"),
            dict(k="船", c=J.INST, t="海洋科学技術センター", v="海中作業船")],
            lead="1985年11月1日〜20日　相模湾海底調査")),
    ),

    "c505": dict(
        t="広く探し、次に撮る",
        s="本文2.4.4.2　調査の方法",
        fig=("process", dict(steps=[
            dict(t="音波で広く探す", d="サイド・スキャン・ソナー", c=J.INK_W),
            dict(t="反応を絞る", d="不自然な反応があった場所", c=J.AMBER),
            dict(t="カメラで撮る", d="えい航式深海カメラ", c=J.INK_W)])),
    ),

    "c506": dict(
        t="17か所すべてを撮影している",
        s="本文2.4.4.2",
        fig=("icons", dict(n=17, on=17, kind="dot", cols=9,
                           lead="不自然な反応があった地点",
                           note="17か所の位置は 付図-21 に示されている")),
    ),

    "c507": dict(
        t="調べて、見つからなかった",
        s="本文2.4.4.2",
        fig=("absent", dict(mode="single", items=[
            dict(t="残骸とみられる物体", d="発見されなかった", ok=False)],
            lead="17か所すべてを撮影した結果")),
    ),

    "c508": dict(
        t="ではなぜ、見つからないのか",
        s="解説書 §10　ここも数字で説明されている",
        fig=("moment", dict(clock="—", label="道具の性能を見る",
                            facts=[dict(t="まず", v="音波", c=J.LINE),
                                   dict(t="次に", v="カメラ", c=J.AMBER)])),
    ),

    "c509": dict(
        t="見分けられる細かさ",
        s="解説書 §10、表4　サイド・スキャン・ソナー（SMS960）",
        fig=("compare", dict(bar=False, items=[
            dict(v=1.1, disp="1.1 × 1.3", unit="m", t="当時の分解能（500mレンジ）",
                 c=J.LINE),
            dict(v=5, disp="5", unit="点", t="物として判別するのに要る反応",
                 c=J.AMBER)],
            note="分解能とは、判別できる一つの点の大きさ")),
    ),

    "c510": dict(
        t="これ以下は探知できない",
        s="解説書 §10",
        fig=("compare", dict(bar=False, items=[
            dict(v=5.5, disp="5.5 × 6.5", unit="m", t="探知に必要な大きさ",
                 c=J.ALERT)],
            note="これより小さいものは、そもそも音波にかからない")),
    ),

    "c511": dict(
        t="落ちたものは、それより小さい",
        s="写真-14　海上から回収されたAPU空気取り入れダクト（解説書 表5）",
        photo="ja123/p014.jpg", panel=True, side="right",
        ann=[dict(t="補助動力装置（APU）", v="約250 kg", vc=J.AMBER, vs=62,
                  d="1.9 × 1.4 × 1.0 m", dc=J.LINE, ds=28),
             dict(t="方向舵を動かす装置 ×2", v="約40 kg", vc=J.AMBER, vs=62,
                  d="0.7 × 0.5 m", dc=J.LINE, ds=28)],
    ),

    "c512": dict(
        t="大きいものでも900キロ",
        s="付図-27　垂直尾翼損壊図（左側）（解説書 表5）",
        photo="ja123/f027.jpg", panel=True, side="right",
        ann=[dict(t="トーション・ボックス", v="約900 kg", vc=J.AMBER, vs=68),
             dict(t="解説書の見方", d="数個に破損して分散している可能性",
                  dc=J.ALERT, ds=30)],
    ),

    "c513": dict(
        t="ではカメラで端から見れば",
        s="解説書 §10　その計算も示されている",
        fig=("moment", dict(clock="—", label="えい航式深海カメラ",
                            facts=[dict(t="問い", v="端から全部撮れないか",
                                        c=J.AMBER)])),
    ),

    "c514": dict(
        t="一度に写せる幅は1.5メートル",
        s="解説書 §10　えい航式深海カメラ",
        fig=("compare", dict(bar=False, items=[
            dict(v=1.5, disp="約1.5", unit="m", t="一度に写せる幅", c=J.INK_W),
            dict(v=2, disp="約2", unit="kt", t="進む速さ", c=J.LINE)])),
    ),

    "c515": dict(
        t="網羅すると4,500時間",
        s="解説書 §10　25km² ÷ 1.5m ÷ 2kt の試算",
        fig=("compare", dict(bar=False, items=[
            dict(v=25, disp="約25", unit="km²", t="調査区域", c=J.LINE),
            dict(v=4500, disp="4,500", unit="時間", t="網羅にかかる時間",
                 c=J.ALERT)],
            note="解説書の試算　25 ÷ 0.0015 ÷ 1.852 ÷ 2 でおよそ4,500")),
    ),

    "c516": dict(
        t="1日6時間でも750日かかる",
        s="解説書 §10",
        fig=("compare", dict(bar=True, vmax=750, items=[
            dict(v=750, disp="750", unit="日", t="1日6時間で網羅する日数",
                 c=J.ALERT),
            dict(v=365, disp="365", unit="日", t="1年", c=J.LINE)],
            ref="750日を上限として比べている",
            note="2年以上かかる計算になる")),
    ),

    "c517": dict(
        t="しかも一度では足りない",
        s="解説書 §10",
        fig=("absent", dict(mode="ledger", items=[
            dict(t="任意の地点への移動", d="自走できないのでできない", ok=False),
            dict(t="同じ場所の撮り直し", d="何度も必要になる", ok=True)],
            lead="当時の深海カメラ")),
    ),

    "c518": dict(
        t="1985年の技術では届かない",
        s="付図-21　相模湾海底調査区域",
        photo="ja123/f021.jpg", panel=True, side="left", bias=0.62,
        ann=[dict(t="隠したのではない", d="見つけられなかった", dc=J.OK, ds=34),
             dict(t="記録に残っていること", d="探せなかったという事実", dc=J.LINE,
                  ds=32)],
    ),

    "c519": dict(
        t="ただし、続きがある",
        s="30年後のこと",
        fig=("moment", dict(clock="—", label="この話は1985年で終わらない",
                            facts=[dict(t="次", v="2015年", c=J.AMBER)])),
    ),

    "c520": dict(
        t="2015年、もう一度調べた",
        s="報道（情報公開請求で得た資料をもとに）",
        fig=("timeline", dict(t0=1985, t1=2015,
                              ticks=[(1985, "1985"), (2000, "2000"),
                                     (2015, "2015")],
                              events=[dict(t=1985, top="海底調査（国）", c=J.LINE),
                                      dict(t=2015, top="テレビ局が調査",
                                           c=J.AMBER, big=True)])),
    ),

    "c521": dict(
        t="東伊豆町の沖、水深160メートル",
        s="報道",
        fig=("mapfig", dict(
            points=[dict(x=0.32, y=0.44, t="東伊豆町", c=J.INK_W),
                    dict(x=0.56, y=0.52, t="沖 約2.5 km", c=J.AMBER,
                         kind="wreck")],
            link=(0, 1), scale="水深 約160 m",
            note="海岸線の形は位置関係を示すための略図")),
    ),

    "c522": dict(
        t="部品かもしれない物体",
        s="報道　2015年8月12日",
        fig=("panel", dict(blocks=[
            dict(k="何が", c=J.DOC, t="123便の部品の可能性"),
            dict(k="調べたのは", c=J.LINE, t="テレビ局（情報公開請求の資料）")],
            note="この章でここだけは、出どころが報告書ではなく報道")),
    ),

    "c523": dict(
        t="調べれば分かる余地がある",
        s="海底で見つかった物体についての報道",
        fig=("quote", dict(phrase="より詳細に分かる可能性がある",
                           who="当時の事故調査官",
                           to="報道に対して",
                           when="2015年",
                           doc="※ 公的文書ではなく報道による")),
    ),

    "c524": dict(
        t="確定したわけではない",
        s="報道のあとに分かっていること",
        # ⚠️ 2つとも「無い」なので `pair` ではなく `ledger`。
        #    `pair` は有る側が1つ以上ないと**画面が破線の輪郭だけ**になる
        #    （型の側でエラーにしてある。README §2 の r21 目視の教訓）。
        fig=("absent", dict(mode="ledger", items=[
            dict(t="123便の部品だという確定", d="していない", ok=False),
            dict(t="引き揚げ", d="行われていない", ok=False)],
            lead="2015年に見つかった物体について")),
    ),

    "c525": dict(
        t="30年で、道具は変わった",
        s="解説書 §10（現在の性能は参考値）",
        fig=("beforeafter", dict(
            a=dict(k="1985年", t="探せなかった", lines=["分解能 1.1m × 1.3m"],
                   c=J.ALERT),
            b=dict(k="2015年", t="見つかるところまで来た",
                   lines=["水深160mの海底で"], c=J.OK))),
    ),

    "c526": dict(
        t="いまも落ちたままのものがある",
        # 🔴 2026-08-04：付図-20 から**解説書 表5**へ差し替えた。
        #    ナレーションが読み上げる4つ（補助動力装置・方向舵を動かす装置・
        #    胴体の最後部・方向舵）が、表5 の列そのもの。
        s="解説書 表5　推定される落下物",
    ),

    "c527": dict(
        t="道具の限界であって意思ではない",
        s="この章の答え",
        fig=("panel", dict(blocks=[
            dict(k="×", c=J.ALERT, t="隠したから見つからなかった"),
            dict(k="○", c=J.OK, t="道具が届いていなかった")])),
    ),

    "c528": dict(
        t="道具は、まだ良くなっていく",
        s="この章の終わりに",
        fig=("moment", dict(clock="—", label="探す道具の進み方",
                            facts=[dict(t="変わったもの", v="探す道具", c=J.AMBER),
                                   dict(t="変わらないもの", v="海底にある物",
                                        c=J.LINE)])),
    ),

    "c529": dict(
        t="4つの疑問を見てきた",
        s="次の章で見ること",
        fig=("panel", dict(blocks=[
            dict(k="第2章", c=J.OK, t="ミサイル"),
            dict(k="第3章", c=J.OK, t="急減圧"),
            dict(k="第4章", c=J.AMBER, t="15時間半"),
            dict(k="第5章", c=J.OK, t="海の底")], cols=2)),
    ),
}
