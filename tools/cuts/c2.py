# -*- coding: utf-8 -*-
"""第2章 開店5年の、新しい百貨店 c201–c218（18カット）。10本目（三豊百貨店）。

■ 写真は11カット。割り当ての正本＝`ref/ep10/photos.md`。
  🔴 **この章の写真は1点残らず「崩れたあと」**（`sampoong_before_02` と `inside_store_01` を除く）。
     章の中身は「事故の前はこういう店だった」なので、**副題で時代を名乗り違えない**
     （→ [[feedback-subtitle-must-match-what-is-visible]]）。
  ⚠️ `sign_sampoong_05`（c212）は ②が「崩れていない側」と書いたが**崩れている側**。
  ⚠️ `sign_sampoong_07`（c201）はクレーンと消防車が写る＝**崩壊後**。
■ 公共ヌリ（寄れる）は `sampoong_before_02`（c205）と `inside_store_01`（c206）の2点だけ。
  残り9点は CC BY-SA ＝**額装だけ**（`panel=True` のみ）。
■ ⚠️ 見出し・副題・図の札に**ナレーションの文を写さない**（`check_echo`）。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC_K6R29 = "国政調査結果報告書 p.29"
SRC_SI = "ソウル市の報告 p.34"

SPEC = {

    "c201": dict(
        t="持ち主は、三豊建設産業",
        s="崩れずに残った南の棟　1995年撮影",
        photo=P("sign_sampoong_07"), panel=True,
    ),

    # 年表。**日付と出来事の名前だけ**を持たせる（文はナレーションと字幕が持つ）。
    "c202": dict(
        t="骨組みは、途中で止まった",
        s="着工から開店までの3年",
        fig=("timeline", dict(
            events=[dict(t=1987.20, top="1987年3月", t2="掘る工事", c=J.LINE),
                    dict(t=1987.65, top="1987年8月25日", t2="着工の届け", c=J.LINE),
                    dict(t=1988.87, top="1988年11月", t2="骨組みの打ち切り",
                         c=J.ALERT, big=True),
                    dict(t=1989.95, top="1989年12月", t2="開店", c=J.AMBER, big=True)],
            t0=1987.0, t1=1990.2,
            ticks=[(1987, "1987"), (1988, "1988"), (1989, "1989"), (1990, "1990")],
            src="K6-検 p.46・" + "国政調査結果報告書 p.31")),
    ),

    "c203": dict(
        t="敷地はサッカー場2面より広い",
        s="崩れた棟の全景　1995年撮影",
        photo=P("wreck_aerial_03"), panel=True,
    ),

    # 🔴 対比（A vs B）なので `arrow=False`（矢印は「A が B になる」と読める）。
    "c204": dict(
        t="A棟とB棟、中身は別もの",
        s="二つの棟の使いみち",
        fig=("beforeafter", dict(
            a=dict(k="A棟（北）", t="百貨店の売り場", lines=["地下1階から5階まで"],
                   v="崩れた棟", c=J.ALERT),
            b=dict(k="B棟（南）", t="売り場とスポーツ施設",
                   lines=["1〜3階　売り場", "4・5階　スポーツ施設"],
                   v="残った棟", c=J.LINE),
            arrow=False,
            note="同じ大きさの棟　" + SRC_SI)),
    ),

    # 公共ヌリ＝寄れる。「門のような形」が写る唯一の点なので、正面を丸ごと入れる。
    "c205": dict(
        t="正面は、門のような形だった",
        s="崩れる前の三豊百貨店　1995年撮影",
        photo=P("sampoong_before_02"),
        **ss.focus(P("sampoong_before_02"), 0.50, 0.50, 1.0),
    ),

    # ⚠️ 見出しに「524台」を書くと、注記の答えを先に言ってしまう（`check_wording` A型）。
    "c206": dict(
        t="客が入るのは、地下1階から上",
        s="1階の売り場　1995年撮影",
        photo=P("inside_store_01"), **ss.kind(P("inside_store_01")),
        side="right", ann_y=356,
        ann=[dict(t="地下2つの階", v="524台", vc=J.AMBER, vs=96, d="まるごと駐車場",
                  dc=J.TICK, ds=40)],
    ),

    # 「6つの階のうち5階だけが別」を、欄の並んだ帳面で見せる。
    "c207": dict(
        t="ひとつだけ、売り場ではない",
        s="客が入る6つの階",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="地下1階", d="売り場", ok=True),
                   dict(t="1階", d="売り場", ok=True),
                   dict(t="2階", d="売り場", ok=True),
                   dict(t="3階", d="売り場", ok=True),
                   dict(t="4階", d="売り場", ok=True),
                   dict(t="5階", d="食堂街", ok=False, c=J.ALERT)],
            note="5階は最上階　" + SRC_SI)),
    ),

    # 🔴 5階に特設の売り場があったことが、垂れ幕の字で分かる点。
    "c208": dict(
        t="最上階にも、売り場があった",
        s="垂れ幕の下がった売り場　1995年撮影",
        photo=P("banner_daily_02"), panel=True,
    ),

    "c209": dict(
        t="名前を登録した客が7万人台",
        s="崩れた棟と、集まった人　1995年撮影",
        photo=P("sign_sampoong_02"), panel=True,
    ),

    "c210": dict(
        t="全国でも、指折りの店",
        s="1994年度の位置",
        fig=("panel", dict(
            blocks=[dict(k="売り上げ", t="全国の百貨店のなか", v="7番目", c=J.AMBER),
                    dict(k="売り場の大きさ", t="1位はロッテ本店", v="2番目", c=J.AMBER)],
            cols=2,
            note="白書 p69")),
    ),

    "c211": dict(
        t="開いてから、まだ5年",
        s="崩れた棟をふくむ全景　1995年撮影",
        photo=P("sign_sampoong_01"), panel=True,
    ),

    # ⚠️ ②の「崩れていない側」は取り違え。**ガラスが割れ鉄骨がむき出しの側**。
    "c212": dict(
        t="地震も火事も、起きていない",
        s="割れたガラスと、むき出しの鉄骨　1995年撮影",
        photo=P("sign_sampoong_05"), panel=True,
    ),

    "c213": dict(
        t="開店のあとも、広げつづけた",
        s="崩れた棟の全景　1995年撮影",
        photo=P("wreck_aerial_09"), panel=True,
    ),

    "c214": dict(
        t="崩れた月も、ふつうに営業",
        s="残った棟に出ていた広告　1995年撮影",
        photo=P("street_cordon_03"), panel=True,
    ),

    "c215": dict(
        t="厨房にも客席にも、重い物",
        s="5階にあった店の中身",
        fig=("panel", dict(
            blocks=[dict(k="厨房", t="大きな冷蔵庫と調理台", c=J.LINE),
                    dict(k="客席", t="石でできた椅子", c=J.AMBER)],
            cols=2,
            note="白書 p85〜91")),
    ),

    "c216": dict(
        t="記録に、食い違いが残っている",
        s="二つの棟の断面と連結梁　1995年撮影",
        photo=P("wreck_ground_06"), panel=True,
    ),

    # 🔴 対比。どちらが正しいかはここでは言わない（c308 で中身を出す）。
    "c217": dict(
        t="二枚の図面が、合っていない",
        s="許可の図面と、工事の図面",
        fig=("beforeafter", dict(
            a=dict(k="役所に出した図面", t="許可を受けたもの", lines=["審査を通った中身"],
                   c=J.INST),
            b=dict(k="工事に使った図面", t="実際に建てたもの",
                   lines=["合わない箇所が複数"], c=J.ALERT),
            arrow=False,
            note=SRC_K6R29)),
    ),

    # 決め所。**言葉は字幕が持つ**ので、図は出どころだけを持つ。
    "c218": dict(
        t="始まりから、ずれていた",
        s="事業計画の出発点",
        fig=("quote", dict(
            phrase="はじめの計画は、百貨店ではなかった",
            rows=[("いつの計画", "1987年の事業計画", J.AMBER),
                  ("どう書かれていたか", "ショッピングセンター", J.INK_W),
                  ("書かれていた文書", "大法院 1996年8月23日 判決", J.DOC)],
            paper=True)),
    ),

}
