# -*- coding: utf-8 -*-
"""第8章 17時06分50秒 c801–c816（16カット）。9本目（テネリフェ）。

■ ここで初めて事故現場の写真を出す（`wreck_*`）。6点とも器具ごとの複写＝`cuts/ss.py` の
  `TRIM` がファイル単位で台紙と「PATERSON」を外す（章ファイルに trim を書かない）。
  ⚠️ Anefo の記録の日付は「1977年3月27日」（連作の名前）＝「翌日」と名乗らない。
  ⚠️ `wreck_both_*` はどちらの機体か決めない＝「二機のうちの一方」。
■ 🔴 「248」「326」「583」を出さない（印字されていない合算）。c815 は乗員と乗客を別々に出す。
■ 距離は報告書 p20・p21（約700メートル・約90メートル手前・150メートル先・300メートル・約450メートル）。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
WRECK = "1977年撮影（事故のあとの現場）"

SPEC = {

    "c801": dict(
        t="二人は、それ以上言わなかった",
        s="博物館に保存された747-206B（KLMと同じ系列）　2013年撮影",
        photo=P("cockpit_747_07"), side="right", ann_y=356,
        **ss.kind(P("cockpit_747_07")),
        ann=[dict(t="報告書が書いたもの", d="黙った理由の見方", dc=J.DOC, ds=36)],
    ),

    "c802": dict(
        t="これほどの人が、これほどの誤りを",
        s="報告書が書いた機長の立場",
        fig=("panel", dict(
            blocks=[dict(k="機長", t="会社でもっとも信望のある操縦士の一人", v="", c=J.INK_W),
                    dict(k="だから", t="誤りは考えにくかった", v="", c=J.AMBER)],
            note="事故報告書 p33", cols=2)),
    ),

    "c803": dict(
        t="もう一つ、教官という仕事",
        s="報告書が書いたもう一つのこと",
        fig=("moment", dict(
            clock="10年以上", label="機長が続けてきた仕事",
            facts=[dict(t="仕事", v="教官", c=J.AMBER)],
            sub="事故報告書 p27")),
    ),

    "c804": dict(
        t="訓練の飛行では",
        s="教官がすること",
        fig=("process", dict(
            steps=[dict(t="教官", d="管制官の役もやる", c=J.INK_W),
                   dict(t="離陸の許可", d="教官自身が出す", c=J.AMBER),
                   dict(t="模擬の飛行", d="無線を使わないことも", c=J.LINE)],
            note="事故報告書 p27")),
    ),

    "c805": dict(
        t="許可を待たないのが、日常だった",
        s="10年以上続けた訓練",
        fig=("quote", dict(
            phrase="訓練では、許可を出すのは自分だった",
            rows=[("誰の", "KLMの機長", J.INK_W),
                  ("続けた年数", "10年以上", J.AMBER),
                  ("出どころ", "事故報告書 p27", J.DOC)],
            paper=True)),
    ),

    # ⚠️ 写真は 737（2013年）。副題で写っているものを名乗る。
    "c806": dict(
        t="17:06:40ごろ、前方に灯り",
        s="現在のテネリフェ北空港（着陸灯をつけた機体）　2013年撮影",
        photo=P("losrodeos_now_17"), side="right", ann_y=356,
        **ss.focus(P("losrodeos_now_17"), 0.40, 0.45, zoom=1.0),
        **ss.kind(P("losrodeos_now_17")),
        ann=[dict(t="パンナムの機長が見た", d="KLM機の着陸灯", dc=J.INK_W, ds=36),
             dict(t="距離", v="約700メートル", vc=J.AMBER, vs=72)],
    ),

    "c807": dict(
        t="ぶつかる9秒ほど前",
        s="パンナムの機長が灯りを見たとき",
        fig=("runway", dict(
            steps=[dict(planes=[dict(at=0.575, on="rwy", head=0, t="パンナム", c=J.INK_W,
                                     s=0.9),
                                dict(at=0.78, on="rwy", head=180, t="KLM", c=J.AMBER,
                                     s=0.9)]),
                   dict(dim=[dict(a=0.575, b=0.78, t="約700メートル", c=J.AMBER)],
                        mark=[dict(at=0.68, y="top", t="残された時間のすべて", c=J.ALERT)])],
            exits=False, note="模式図（位置は正確ではない）", src="事故報告書 p31・p38")),
    ),

    "c808": dict(
        t="パンナムは、左へ逃げようとした",
        s="パンナムの747　1970年撮影（スキポール空港）",
        photo=P("panam_ams1970_10"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("panam_ams1970_10")),
        ann=[dict(t="出力を入れて", d="滑走路の外へ", dc=J.INK_W, ds=38),
             dict(t="結果", d="間に合わなかった", dc=J.ALERT, ds=38)],
    ),

    "c809": dict(
        t="17:06:43、V1",
        s="KLM機の操縦室",
        fig=("radio", dict(
            lanes=["副操縦士", "機体"],
            events=[dict(lane=0, a=403.0, t="V1", d="離陸をやめられない速さ", c=J.AMBER,
                         st="v1"),
                    dict(lane=1, a=404.0, t="機首を上げ始める", d="17:06:44", c=J.ALERT,
                         st="rot")],
            t0=398.0, t1=412.0,
            ticks=[(400, "17:06:40"), (405, "17:06:45"), (410, "17:06:50")],
            src="事故報告書 p31／操縦室の録音の書き起こし")),
    ),

    "c810": dict(
        t="尾が、滑走路をこすった",
        s="現在のテネリフェ北空港に着陸する機体　2011年撮影",
        photo=P("losrodeos_now_18"), bias=0.60, side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_18")),
        ann=[dict(t="こすった跡の始まり", v="約90メートル", vc=J.AMBER, vs=72,
                  d="ぶつかった場所の手前", dc=J.LINE, ds=30)],
    ),

    "c811": dict(
        t="17:06:47、機長の声",
        s="KLM機の操縦室の録音",
        fig=("moment", dict(
            clock="17:06:47", label="KLMの機長",
            facts=[dict(t="報告書の書き方", v="声を発した", c=J.ALERT)],
            sub="操縦室の録音の書き起こし／事故報告書 p31")),
    ),

    "c812": dict(
        t="17:06:50",
        s="焼けたKLM機　" + WRECK,
        photo=P("wreck_klm_03"), side="right", ann_y=356,
        **ss.kind(P("wreck_klm_03")),
        ann=[dict(t="KLM機", d="すでに完全に浮いていた", dc=J.INK_W, ds=34),
             dict(t="第1エンジン", d="パンナムの右の翼の先をかすめた", dc=J.ALERT, ds=32)],
    ),

    "c813": dict(
        t="主脚が、パンナムに激突した",
        s="二機のうちの一方の残骸　" + WRECK,
        photo=P("wreck_both_01"), side="right", ann_y=330,
        **ss.kind(P("wreck_both_01")),
        ann=[dict(t="KLM機の主脚", d="パンナムの右の内側のエンジンのあたり", dc=J.ALERT,
                  ds=30),
             dict(t="地面に当たった", v="150メートル先", vc=J.AMBER, vs=64)],
    ),

    "c814": dict(
        t="さらに300メートル滑って、燃えた",
        s="草地に転がったエンジン　" + WRECK,
        photo=P("wreck_engine_01"), side="right", ann_y=356,
        **ss.kind(P("wreck_engine_01")),
        ann=[dict(t="二つの残骸のあいだ", v="約450メートル", vc=J.AMBER, vs=72)],
    ),

    # ⚠️ 合算（248）を出さない。c105 の棒と同じ絵にしない＝柱で出す。
    "c815": dict(
        t="KLM機では、全員が亡くなった",
        s="KLM機に乗っていた人",
        fig=("panel", dict(
            blocks=[dict(k="乗員", t="亡くなった", v="14", c=J.ALERT),
                    dict(k="乗客", t="亡くなった", v="234", c=J.ALERT),
                    dict(k="生き残った人", t="いない", v="0", c=J.TICK)],
            note="事故報告書 p6", cols=3)),
    ),

    # ⚠️ 合算（326）を出さない。
    "c816": dict(
        t="外から見ていた人は、いない",
        s="二機のうちの一方の残骸　" + WRECK,
        photo=P("wreck_both_02"), side="right", ann_y=356,
        **ss.kind(P("wreck_both_02")),
        ann=[dict(t="パンナム機でその場で亡くなった人", d="乗員9人・乗客317人", dc=J.ALERT,
                  ds=36)],
    ),
}
