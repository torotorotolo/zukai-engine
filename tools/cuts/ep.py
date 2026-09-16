# -*- coding: utf-8 -*-
"""締め 言葉が変わった ep01–ep10（10カット）。9本目（テネリフェ）。

■ 写真9カット（台本の画の欄どおり）＝オランダの追悼（Anefo・1977年）と国際追悼碑。
  ⚠️ 私人の顔が主役の写真は `NG_PHOTOS`（使うと止まる）。ep03 の葬列は顔が中くらい＝⑤c で原寸を見る。
  ⚠️ ep10 の `memorial_03` は**名前を刻んだ碑**＝原寸で名前が読めるかを見ていない（⑤b-1 §4-7）。
     寄らない（額装で小さく出す）。⑤c で読めたら差し替える。
■ 根本の原因4つ・寄与した要因3つ・外側の3つ・勧告3つは**ナレーションが読む**＝注記に文を写さない
  （数だけを出す）。ep09 の決め所だけが言葉を出す。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SPEC = {

    "ep01": dict(
        t="根本の原因は、機長の四つの行動",
        s="スキポール空港での追悼式の棺　1977年撮影",
        photo=P("nl_mourning_06"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("nl_mourning_06")),
        ann=[dict(t="報告書が挙げた根本の原因", v="4つ", vc=J.ALERT, vs=110)],
    ),

    "ep02": dict(
        t="やめなかった、強く肯定した",
        s="オランダ国会（第二院）の黙祷　1977年撮影",
        photo=P("nl_mourning_10"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("nl_mourning_10")),
        ann=[],
    ),

    "ep03": dict(
        t="30秒足らずに、止まる機会が四つ",
        s="ウェストガールデ墓地への葬列　1977年撮影",
        photo=P("nl_funeral_02"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("nl_funeral_02")),
        ann=[],
    ),

    "ep04": dict(
        t="報告書は、誤りの背景を問うた",
        s="KLMの危機対策センター　1977年撮影",
        photo=P("nl_crisis_01"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("nl_crisis_01")),
        ann=[dict(t="報告書が立てた問いへの答え", v="3つ", vc=J.AMBER, vs=110)],
    ),

    "ep05": dict(
        t="三つの答えは、寄与した要因",
        s="スキポール空港での追悼式　1977年撮影",
        photo=P("nl_mourning_01"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("nl_mourning_01")),
        ann=[dict(t="報告書の分け方", d="根本の原因／寄与した要因", dc=J.DOC, ds=34)],
    ),

    "ep06": dict(
        t="機長の外側で、起きていたこと",
        s="KLMの危機対策センター　1977年撮影",
        photo=P("nl_crisis_03"), bias=0.50, side="right", ann_y=356,
        **ss.kind(P("nl_crisis_03")),
        ann=[dict(t="報告書が並べた別の要因", v="3つ", vc=J.AMBER, vs=110)],
    ),

    "ep07": dict(
        t="報告書は、KLMの外も見ている",
        s="テネリフェの国際追悼碑　2015年撮影",
        photo=P("memorial_01"), panel=True, side="right", ann_y=330,
        ann=[dict(t="パンナム", d="位置の報告は2回", dc=J.INK_W, ds=32),
             dict(t="管制官の「オーケー」", d="適切ではなかった", dc=J.AMBER, ds=32)],
    ),

    # ⚠️ 銘板の文に「583」がある（碑の文＝報告書の数として出すのではない）。
    "ep08": dict(
        t="報告書の勧告は、三つ",
        s="国際追悼碑の銘板　2015年撮影",
        # 🔴 check_slide G-13：全画面だと銘板の文字が字幕帯に入った＝額装（帯より上に収まる）
        photo=P("memorial_02"), panel=True, side="right", ann_y=356,
        ann=[dict(t="勧告", v="3つ", vc=J.AMBER, vs=110)],
    ),

    "ep09": dict(
        t="残したのは、許可の出し方の決まり",
        s="勧告の三つ目",
        fig=("quote", dict(
            phrase="許可に「離陸」という語を使わない",
            rows=[("中身", "ATCの許可と離陸の許可を、時間で十分に離す", J.INK_W),
                  ("出どころ", "事故報告書 p41", J.DOC)],
            paper=True)),
    ),

    # ⚠️ 名前を刻んだ碑＝寄らない（額装で小さく）。原寸で名前が読めるかは ⑤c で見る。
    "ep10": dict(
        t="声は、機体を止められなかった",
        s="名前を刻んだ追悼の碑　2009年撮影",
        photo=P("memorial_03"), panel=True, side="right", ann_y=330,
        ann=[dict(t="1977年3月27日", v="17:06:50", vc=J.ALERT, vs=88),
             dict(t="生きて出た人", v="61人", vc=J.INK_W, vs=88)],
    ),
}
