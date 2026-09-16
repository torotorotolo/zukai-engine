# -*- coding: utf-8 -*-
"""第9章 逃げた61人 c901–c918（18カット）。9本目（テネリフェ）。

■ ⚠️ 管制塔の写真は0点＝c901 は `fog_laguna_01`（空港の北東の山地・2025年）。代用しない名乗り。
■ `wreck_both` 2点に4欄（photos.md §4-2）：
  - c912 … `wreck_both_02` の**左の6割**（がれきの山と翼）を切り出す
  - c914 … `wreck_both_01` の**右の4割**（翼とエンジン）を切り出す＝手前の男性2人を窓の外へ
    （人物は焼き付けの横 0.09〜0.45＝元画像の x 0.226〜0.445。窓は x 0.47 から）
  - c916・c917 … 脱出の図＋地（BACKDROP＝wreck_both_02／wreck_both_01。暗幕の下）
  ⚠️ カットの `trim` はファイルの `TRIM` を**置き換える**＝窓は必ず焼き付けの内側で書く
    （wreck_both_01 の焼き付け x 0.1716〜0.7788・y 0.1865〜0.7469／wreck_both_02 は
    x 0.2008〜0.8413・y 0.1996〜0.7563）。
  ⚠️ どちらの機体か、どの翼かを名乗らない（「二機のうちの一方」）。
■ 人数：報告書 p6 の表＝パンナム機の乗員のうち助かった7人・乗客61人（うち9人があとで亡くなった）・
  補助席の2人。⚠️ 「70人」は足した数＝画面に出さない。「61人」は章名とナレーションの数。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
WRECK = "1977年撮影（事故のあとの現場）"
F20 = "事故報告書 p20"

SPEC = {

    "c901": dict(
        t="管制塔に届いたのは、音だけ",
        s="霧をかぶる、空港の北東の山地　2025年撮影",
        photo=P("fog_laguna_01"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("fog_laguna_01")),
        ann=[dict(t="管制塔に聞こえたもの", d="爆発の音が二度", dc=J.ALERT, ds=36)],
    ),

    "c902": dict(
        t="見えないので、確かめようがない",
        s="管制塔に分からなかったこと",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="どこで鳴ったか", d="分からない", ok=False, c=J.TICK),
                   dict(t="なぜ鳴ったか", d="分からない", ok=False, c=J.TICK),
                   dict(t="確かめる手立て", d="見えない", ok=False, c=J.ALERT)],
            note=F20)),
    ),

    "c903": dict(
        t="駐機場の機体が、火を見た",
        s="現在のテネリフェ北空港の誘導路の機体　2013年撮影",
        photo=P("losrodeos_now_13"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("losrodeos_now_13")),
        ann=[dict(t="知らせてきたこと", d="火が見える", dc=J.ALERT, ds=40),
             dict(t="まだ分からない", d="場所も、理由も", dc=J.INK_W, ds=36)],
    ),

    "c904": dict(
        t="場所の分からない、火の警報",
        s="管制塔が出した警報",
        fig=("process", dict(
            steps=[dict(t="管制塔", d="消防へ警報", c=J.ALERT),
                   dict(t="伝えたこと", d="火がある・すぐ出られるように", c=J.AMBER),
                   dict(t="まだ分からない", d="火の場所", c=J.TICK)],
            note=F20)),
    ),

    "c905": dict(
        t="最初の手がかり",
        s="人づてに届いた、火の場所",
        fig=("people", dict(
            nodes=[dict(x=0.18, y=0.42, t="空港で働く会社の人", d="", c=J.INK_W,
                        kind="person"),
                   dict(x=0.80, y=0.42, t="消防の詰所", d="", c=J.INST, kind="org")],
            edges=[dict(a=0, b=1, t="火は、駐機場の左のほう", c=J.AMBER)],
            note=F20)),
    ),

    # _06 は c212（写真）と c310（地）でも使う＝赤い車両のほうへ寄って別の絵にする。
    "c906": dict(
        t="混み合った駐機場を、横切る",
        s="現在のテネリフェ北空港の駐機場　2003年撮影",
        photo=P("losrodeos_now_06"), bias=0.70, xbias=0.70, zoom=1.35,
        side="left", ann_y=356,
        **ss.kind(P("losrodeos_now_06")),
        ann=[dict(t="消防車の進み", d="とても遅かった", dc=J.ALERT, ds=40)],
    ),

    "c907": dict(
        t="急ぎたくても、急げない",
        s="消防車が進んだ駐機場",
        fig=("beforeafter", dict(
            a=dict(k="見えないなか", t="ぶつかりうるもの", lines=["人・車・駐まっている機体"],
                   c=J.ALERT),
            b=dict(k="だから", t="そろそろ進む", lines=[], c=J.AMBER),
            note=F20)),
    ),

    "c908": dict(
        t="炎より先に、熱が届いた",
        s="消防が近づいたとき",
        fig=("process", dict(
            steps=[dict(t="雲ごしに", d="明るい光", c=J.AMBER),
                   dict(t="炎そのもの", d="まだ見えない", c=J.TICK),
                   dict(t="先に届いた", d="強い熱", c=J.ALERT)],
            note=F20)),
    ),

    "c909": dict(
        t="炎の上に、尾翼だけが立つ",
        s="立ったまま残ったKLM機の尾翼　" + WRECK,
        photo=P("wreck_klm_02"), side="right", ann_y=356,
        **ss.kind(P("wreck_klm_02")),
        ann=[dict(t="少し晴れたとき", d="機体の全体が炎の中", dc=J.ALERT, ds=36)],
    ),

    # pr03 と同じ写真＝右の胴の骨組みへ寄る（焼き付けの内側の窓）。
    "c910": dict(
        t="遠くに、もう一つの光",
        s="焼けたKLM機　" + WRECK,
        photo=P("wreck_klm_01"), trim=(0.50, 0.1986, 0.8286, 0.7652), panel=True,
        side="right", ann_y=356,
        ann=[dict(t="消防が最初に思ったこと", d="外れた部品が燃えている", dc=J.INK_W, ds=34)],
    ),

    "c911": dict(
        t="近づいて、はじめて分かった",
        s="二つ目の光へ向かった消防",
        fig=("beforeafter", dict(
            a=dict(k="消防", t="車を分ける", lines=["二つ目の光へ"], c=J.AMBER),
            b=dict(k="近づいて", t="何なのかが分かった", lines=["二つ目の光の正体"], c=J.ALERT),
            note=F20)),
    ),

    "c912": dict(
        t="光の正体は、飛行機だった",
        s="二機のうちの一方の残骸　" + WRECK,
        photo=P("wreck_both_02"), trim=(0.2008, 0.1996, 0.62, 0.7563), panel=True,
        side="right", ann_y=356,
        ann=[dict(t="二つ目の光", d="もう一機の飛行機", dc=J.ALERT, ds=40)],
    ),

    "c913": dict(
        t="消防は、ここで初めて知った",
        s="消火を始めたあとに分かったこと",
        fig=("quote", dict(
            phrase="燃えていたのは、二機だった",
            rows=[("知った人", "空港の消防", J.INK_W),
                  ("それまでの見方", "一機と、外れた部品", J.LINE),
                  ("出どころ", F20, J.DOC)],
            paper=True)),
    ),

    # 手前の男性2人（x 0.226〜0.445）を窓の外へ出す。
    "c914": dict(
        t="消防は、力の向け先を変えた",
        s="二機のうちの一方の残骸　" + WRECK,
        photo=P("wreck_both_01"), trim=(0.47, 0.1865, 0.7788, 0.7469), panel=True,
        side="right", ann_y=356,
        ann=[dict(t="理由", d="一つ目は手のつけようがない", dc=J.INK_W, ds=34)],
    ),

    "c915": dict(
        t="二階と、胴体の上が無くなった",
        s="パンナム機の中",
        fig=("absent", dict(
            mode="ledger",
            items=[dict(t="二階の部屋", d="無くなった", ok=False, c=J.ALERT),
                   dict(t="胴体の上側", d="ほとんど無くなった", ok=False, c=J.ALERT),
                   dict(t="床", d="抜けた", ok=False, c=J.ALERT)],
            note="事故報告書 p22")),
    ),

    # 図＋地（BACKDROP＝wreck_both_02）
    "c916": dict(
        t="出口は、左の壁の穴",
        s="パンナム機から外へ出た道",
        fig=("process", dict(
            steps=[dict(t="出口", d="左の壁に開いた穴", c=J.AMBER),
                   dict(t="前のほうの人", d="そこから外へ", c=J.INK_W),
                   dict(t="地面まで", v="約6メートル", d="（20フィート）", c=J.ALERT)],
            note="事故報告書 p22")),
    ),

    # 図＋地（BACKDROP＝wreck_both_01）
    "c917": dict(
        t="左の主翼から、草地へ",
        s="パンナム機から逃げた人たち",
        fig=("panel", dict(
            blocks=[dict(k="逃げ道", t="左の主翼の上から草地へ", v="", c=J.AMBER),
                    dict(k="主翼の下", t="火と、回り続けるエンジン", v="2つ", c=J.ALERT),
                    dict(k="空港の救急車", t="ほとんどすぐ現れた", v="5台", c=J.OK)],
            note="事故報告書 p22", cols=3)),
    ),

    "c918": dict(
        t="逃げるのに、およそ1分",
        s="アムステルフェーンのKLM本社前の半旗　1977年撮影",
        photo=P("nl_crisis_04"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("nl_crisis_04")),
        ann=[dict(t="あとで亡くなった人", v="9人", vc=J.ALERT, vs=88),
             dict(t="生き残った人", v="61人", vc=J.INK_W, vs=104)],
    ),
}
