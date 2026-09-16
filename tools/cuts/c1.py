# -*- coding: utf-8 -*-
"""第1章 その日、二つのジャンボ機 c101–c120（20カット）。9本目（テネリフェ）。

■ 写真は13カット（台本の画の欄どおり）。割り当ては `ref/ep9/photos.md` §4-2 の推奨から。
  - c111 は台本の欄が「747のエンジン」だが、語っているのは**航空機関士の役目**
    → `cockpit_747_02`（三人の操縦室・1971年）にした（photos.md §4-2）
  - c105 は図（乗員と乗客）。スキポールの写真は pr05 で使ったので地に敷く（BACKDROP）
■ 🔴 人数の合算（394・644）を大きな数として出さない。印字されている数（14・234・16・378・2）だけ。
■ 乗員の名前の出どころは**操縦室の録音の書き起こしの凡例**（報告書本文ではない）。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P
SRC_CREW = "事故報告書 p7・p8／名前は操縦室の録音の書き起こし"

SPEC = {

    "c101": dict(
        t="1970年に飛び始めた大型機",
        s="パンナムの747の命名式　1970年撮影",
        photo=P("jumbo_era_01"), side="left", ann_y=356,
        **ss.kind(P("jumbo_era_01")),
        ann=[dict(t="呼ばれ方", d="ジャンボ機", dc=J.INK_W, ds=48)],
    ),

    "c102": dict(
        t="KLM機は、1971年製の747",
        s="KLMの747（事故機と同じ型）　1971年撮影",
        photo=P("klm_747_1971_01"), bias=0.50, side="right", ann_y=330,
        **ss.kind(P("klm_747_1971_01")),
        ann=[dict(t="事故機の登録記号", v="PH-BUF", vc=J.AMBER, vs=80),
             dict(t="飛んだ時間", v="21,195時間", vc=J.INK_W, vs=64),
             dict(t="着陸", v="5,202回", vc=J.INK_W, vs=64)],
    ),

    # ⚠️ 幅1280（寄れない）＝額装。撮影年は不明なので年を名乗らない。
    "c103": dict(
        t="パンナム機は、1970年製",
        s="パンナムの事故機（シドニー・撮影年は不明）",
        photo=P("panam_n736pa_01"), panel=True, side="right", ann_y=330,
        ann=[dict(t="登録記号", v="N736PA", vc=J.AMBER, vs=80),
             dict(t="作られた", v="1970年1月", vc=J.INK_W, vs=64),
             dict(t="飛んだ時間", v="25,725時間", vc=J.INK_W, vs=64)],
    ),

    "c104": dict(
        t="定期便ではなく、借り切りの便",
        s="KLM 4805便の予定",
        fig=("process", dict(
            steps=[dict(t="アムステルダム", d="出発", c=J.LINE),
                   dict(t="ラスパルマス", d="行き先", c=J.AMBER),
                   dict(t="アムステルダム", d="戻る予定", c=J.LINE)],
            note="チャーター便（借り手はオランダの旅行会社）　事故報告書 p3")),
    ),

    # 図＋地（BACKDROP＝schiphol_1977_01）。⚠️ 合算の数を出さない。
    "c105": dict(
        t="KLM機に乗っていた人",
        s="出発はスキポール空港　3月27日 9:00",
        fig=("compare", dict(
            items=[dict(v=14, t="乗員", disp="14", unit="人", c=J.LINE),
                   dict(v=234, t="乗客", disp="234", unit="人", c=J.AMBER)],
            vmax=260, note="事故報告書 p3・p6")),
    ),

    "c106": dict(
        t="KLMの機長は、経験の長い操縦士",
        s="フェルトハイゼン・ファン・ザンテン機長の経歴",
        fig=("compare", dict(
            items=[dict(v=11700, t="飛んだ時間", disp="11,700", unit="時間", c=J.LINE),
                   dict(v=1545, t="そのうち747", disp="1,545", unit="時間", c=J.AMBER)],
            vmax=12000, note=SRC_CREW)),
    ),

    "c107": dict(
        t="KLMの訓練で、いちばん上の立場",
        s="スキポールからローマへ飛ぶ747の操縦室　1971年撮影",
        photo=P("cockpit_747_03"), side="right", ann_y=356,
        **ss.kind(P("cockpit_747_03")),
        ann=[dict(t="教官の仕事", v="10年以上", vc=J.AMBER, vs=88)],
    ),

    # 🔴 95/9,200 は 1% ほど＝既定の棒の下限（4.5%）だと太く描かれて嘘になる → floor を下げる。
    "c108": dict(
        t="副操縦士の747は、95時間",
        s="ミュールス副操縦士の経歴",
        fig=("compare", dict(
            items=[dict(v=9200, t="飛んだ時間", disp="9,200", unit="時間", c=J.LINE),
                   dict(v=95, t="そのうち747", disp="95", unit="時間", c=J.ALERT)],
            vmax=10000, floor=0.008, note=SRC_CREW)),
    ),

    # ⚠️ 引き算・割り算した数（何倍）を出さない。
    "c109": dict(
        t="747の経験の差",
        s="二人の747での時間",
        fig=("compare", dict(
            items=[dict(v=1545, t="機長", disp="1,545", unit="時間", c=J.AMBER),
                   dict(v=95, t="副操縦士", disp="95", unit="時間", c=J.ALERT)],
            vmax=1600, ref="副操縦士が747の資格を取った日　1977年1月19日",
            note="事故報告書 p7")),
    ),

    "c110": dict(
        t="試験官は、同じ操縦室にいた",
        s="副操縦士の747の資格",
        fig=("quote", dict(
            phrase="その資格を出したのは、この機長だった",
            rows=[("資格を取った人", "KLMの副操縦士", J.INK_W),
                  ("試験をした人", "KLMの機長", J.ALERT),
                  ("出どころ", "事故報告書 p28", J.DOC)],
            paper=True)),
    ),

    # 台本の欄は「747のエンジン」。語っているのは航空機関士の役目＝三人の操縦室の写真。
    "c111": dict(
        t="操縦室の三人目は、航空機関士",
        s="スキポールからローマへ飛ぶ747の操縦室　1971年撮影",
        photo=P("cockpit_747_02"), side="right", ann_y=356,
        **ss.kind(P("cockpit_747_02")),
        ann=[dict(t="航空機関士", d="スフルーダー", dc=J.INK_W, ds=40),
             dict(t="747での時間", v="543時間", vc=J.AMBER, vs=80)],
    ),

    "c112": dict(
        t="パンナム機は、ロサンゼルスから",
        s="パンナムの747-121（事故機と同じ型）　1974年撮影",
        photo=P("panam_747_same_type_05"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("panam_747_same_type_05")),
        ann=[dict(t="ロサンゼルスを出た", v="1:29", vc=J.AMBER, vs=96,
                  d="3月26日（世界共通の時計）", dc=J.LINE, ds=30)],
    ),

    # ⚠️ スライドの黒い枠が四辺にある＝寄って枠の外へ出す（zoom）。
    "c113": dict(
        t="ケネディ空港で、乗員が代わった",
        s="ケネディ空港のパンナムの747　1973年撮影",
        photo=P("panam_747_same_type_06"), bias=0.50, xbias=0.50, zoom=1.16,
        side="right", ann_y=356,
        **ss.kind(P("panam_747_same_type_06")),
        ann=[dict(t="着いた", v="6:17", vc=J.INK_W, vs=88),
             dict(t="離陸", v="7:42", vc=J.AMBER, vs=88)],
    ),

    "c114": dict(
        t="パンナムの機長の飛行時間",
        s="飛行中の747-121の操縦室（パンナム機と同じ型）　1989年撮影",
        photo=P("cockpit_747_17"), side="left", ann_y=330,
        **ss.kind(P("cockpit_747_17")),
        ann=[dict(t="機長", d="グラブス", dc=J.INK_W, ds=40),
             dict(t="飛んだ時間", v="21,043時間", vc=J.INK_W, vs=64),
             dict(t="747", v="564時間", vc=J.AMBER, vs=64)],
    ),

    "c115": dict(
        t="副操縦士と機関士の747の時間",
        s="ミュンヘン・リーム空港のパンナムの747　1970年撮影",
        photo=P("panam_747_same_type_01"), bias=0.50, side="right", ann_y=330,
        **ss.kind(P("panam_747_same_type_01")),
        ann=[dict(t="副操縦士　ブラッグ", v="2,796時間", vc=J.AMBER, vs=64,
                  d="全体では10,800時間", dc=J.LINE, ds=28),
             dict(t="航空機関士　ワーンズ", v="559時間", vc=J.AMBER, vs=64)],
    ),

    "c116": dict(
        t="直前の飛行は、この一本だけ",
        s="チューリッヒのパンナムの747-121　1984年撮影",
        photo=P("panam_747_same_type_07"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("panam_747_same_type_07")),
        ann=[dict(t="直前の24時間で飛んだ", v="6時間33分", vc=J.AMBER, vs=80),
             dict(t="飛んでいた区間", d="ニューヨーク→テネリフェ", dc=J.INK_W, ds=34)],
    ),

    # ⚠️ 合算（394）を出さない。
    "c117": dict(
        t="乗客は、パンナム機のほうが多い",
        s="パンナム1736便に乗っていた人",
        fig=("compare", dict(
            items=[dict(v=16, t="乗員", disp="16", unit="人", c=J.LINE),
                   dict(v=378, t="乗客", disp="378", unit="人", c=J.INK_W)],
            vmax=400, floor=0.035, note="事故報告書 p6")),
    ),

    # ⚠️ 合算（644）を出さない。印字されている数だけを並べる。
    "c118": dict(
        t="補助席に、航空会社の従業員",
        s="二機に乗っていた人の内訳",
        fig=("panel", dict(
            blocks=[dict(k="KLM機", t="乗員・乗客", v="14・234", c=J.AMBER),
                    dict(k="パンナム機", t="乗員・乗客", v="16・378", c=J.INK_W),
                    dict(k="補助席", t="航空会社の従業員", v="2", c=J.OK)],
            note="事故報告書 p6　補助席の2人はテネリフェでパンナム機に乗った", cols=3)),
    ),

    # 写真に「KLM ROYAL DUTCH AIRLINES」「BOEING 747」の文字＝主題そのもの（模型と名乗る）。
    "c119": dict(
        t="大きいぶん、地上で場所を取る",
        s="KLMの747の模型　1969年撮影",
        photo=P("jumbo_era_02"), side="right", ann_y=356,
        **ss.kind(P("jumbo_era_02")),
        ann=[dict(t="地上で要るもの", d="広い置き場所", dc=J.AMBER, ds=40)],
    ),

    "c120": dict(
        t="北と西から、一つの空港へ",
        s="現在のグランカナリア空港　2010年撮影",
        photo=P("laspalmas_now_07"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("laspalmas_now_07")),
        ann=[dict(t="KLM", d="アムステルダムから南へ", dc=J.AMBER, ds=32),
             dict(t="パンナム", d="ニューヨークから東へ", dc=J.INK_W, ds=32)],
    ),
}
