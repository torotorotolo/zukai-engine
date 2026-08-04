# -*- coding: utf-8 -*-
"""エピローグ 継ぎ方の図 ep01–ep20（20カット）。

■ この章の役目
  **別添1 付図-3「修正措置で指示された継ぎ方／実際の継ぎ方」に全部が描かれている。**
  この1枚を ep04 で全体、ep05 で左半分（指示）、ep06 で右半分（実際）と寄せていく。
  ⚠️ この図は**左右に2つ並んでいる**ので、切り出しの左右を間違えると意味が逆になる。
     実物で確かめた：**左＝修正措置で指示された継ぎ方／右＝実際の継ぎ方**。

■ 終わり方
  ep19・ep20 で**答えの出ていないものを残したまま**閉じる。
  警報音が1秒で止まった理由（第3章）と、あの夜に何ができたのか（第4章）を回収する。
  🔴 チャンネル名・登録の呼びかけは入れない。
"""
import jiko_style as J

# 別添1 付図-3 の左右を切り分ける割合（実物を等倍で見て測った）。
# 下端はノンブル（252）を落とす。
SPLICE_L = (0.02, 0.02, 0.53, 0.93)
SPLICE_R = (0.50, 0.02, 1.00, 0.93)

SPEC = {

    "ep01": dict(
        t="話は事故の7年前にさかのぼる",
        s="別添1　1978年6月2日 大阪空港",
        fig=("timeline", dict(t0=1978, t1=1985,
                              ticks=[(1978, "1978.6"), (1985, "1985.8")],
                              events=[dict(t=1978, top="しりもち事故", c=J.AMBER),
                                      dict(t=1985, top="この事故", c=J.ALERT,
                                           big=True)],
                              band=[dict(a=1978, b=1985, c=J.LINE, op=0.10,
                                         t="7年")])),
    ),

    "ep02": dict(
        t="機体の後ろを打ちつけた",
        s="別添1 写真-1　尾部胴体下面",
        photo="ja123/a1p001.jpg", panel=True, side="right",
        ann=[dict(t="何が起きたか", d="着陸のときに機首を上げすぎた", dc=J.LINE,
                  ds=32),
             dict(t="結果", d="機体の後ろを滑走路に打ちつけた", dc=J.ALERT,
                  ds=32)],
    ),

    "ep03": dict(
        t="後部圧力隔壁の下が損傷",
        s="別添1 付図-1　昭和53年6月の事故による損壊部位（1）",
        photo="ja123/a1f001.jpg", panel=True, side="right",
        ann=[dict(t="損傷した場所", d="後部圧力隔壁の下の部分", dc=J.ALERT,
                  ds=32),
             dict(t="このあと", d="修理が行われることになった", dc=J.LINE, ds=32)],
    ),

    # ── ep04 ★この1枚に全部がある ────────────────────────────
    "ep04": dict(
        t="この1枚に、すべてがある",
        s="別添1 付図-3　修正指示と実際の継ぎ方",
        photo="ja123/a1f003.jpg", panel=True, side="right",
        ann=[dict(t="左", d="修正措置で指示された継ぎ方", dc=J.OK, ds=32),
             dict(t="右", d="実際にどう継がれたか", dc=J.ALERT, ds=32)],
    ),

    # ── ep05 左半分＝指示された継ぎ方 ─────────────────────────
    "ep05": dict(
        t="1枚の板で上下をつなぐ",
        s="別添1 付図-3（左）　修正措置で指示された継ぎ方",
        photo="ja123/a1f003.jpg", panel=True, side="right", trim=SPLICE_L,
        ann=[dict(t="指示されていた方法", d="1枚の板で上下をつなぐ", dc=J.OK,
                  ds=32),
             dict(t="留め方", d="上下それぞれ2列のリベット", dc=J.OK, ds=32)],
    ),

    # ── ep06 右半分＝実際の継ぎ方 ────────────────────────────
    "ep06": dict(
        t="実際は、板が2枚だった",
        s="別添1 付図-3（右）　実際の継ぎ方",
        photo="ja123/a1f003.jpg", panel=True, side="right", trim=SPLICE_R,
        ann=[dict(t="実際", d="板が2枚に分けて使われた", dc=J.ALERT, ds=32),
             dict(t="その結果", d="片側でリベットが1列しか効かない", dc=J.ALERT,
                  ds=32)],
    ),

    "ep07": dict(
        t="2列で持つ力を1列で持つ",
        s="本文2.15.1.5",
        fig=("compare", dict(bar=True, vmax=2, items=[
            dict(v=2, disp="2", unit="列", t="指示されていたリベット", c=J.OK),
            dict(v=1, disp="1", unit="列", t="実際に効いていた列", c=J.ALERT)],
            ref="2列を上限として比べている",
            note="1か所にかかる負担は、大きくなる")),
    ),

    "ep08": dict(
        t="飛ぶたびに力がかかる",
        s="本文3.1.1",
        fig=("process", dict(steps=[
            dict(t="飛ぶ", d="気圧をかけられる", c=J.LINE),
            dict(t="降りる", d="気圧が戻される", c=J.LINE),
            dict(t="そのたびに", d="継ぎ目に力がかかる", c=J.ALERT)])),
    ),

    "ep09": dict(
        t="破断面に細かい縞が並ぶ",
        s="写真-109　リベット孔34番内舷（孔縁より0.28mm位置）",
        photo="ja123/p109.jpg", panel=True, side="right",
        ann=[dict(t="縞（ストライエーション）", d="1本が1回の飛行にあたる",
                  dc=J.ALERT, ds=30),
             dict(t="縞の幅", d="観察位置で平均 0.23 マイクロメートル", dc=J.AMBER,
                  ds=30)],
    ),

    "ep10": dict(
        t="そこからヤニが漏れていた",
        s="写真-92　L18接続部リベットNo.41付近のヤニの吹き出し",
        photo="ja123/p092.jpg", panel=True, side="left", bias=0.44,
        ann=[dict(t="意味", d="亀裂は事故の日より前からあった", dc=J.ALERT,
                  ds=32)],
    ),

    "ep11": dict(
        t="1985年8月12日 18時24分35秒",
        s="亀裂はついにつながった",
        fig=("moment", dict(clock="18:24", label="隔壁が壊れた",
                            day=18.41, dayspan=(18, 19),
                            facts=[dict(t="このとき", v="亀裂がつながった",
                                        c=J.ALERT)])),
    ),

    "ep12": dict(
        t="そこから先は、数秒だった",
        s="本文3.2.3.6",
        fig=("process", dict(steps=[
            dict(t="空気が噴き出す", d="隔壁の開口から", c=J.ALERT),
            dict(t="後ろの構造が壊れる", d="尾部胴体", c=J.ALERT),
            dict(t="垂直尾翼の大半を失う", d="数秒程度と考えられている",
                 c=J.ALERT)])),
    ),

    "ep13": dict(
        t="そこから、32分",
        s="—",
        fig=("moment", dict(clock="18:56", label="520人が亡くなった",
                            day=18.93, dayspan=(18, 19),
                            facts=[dict(t="異常発生から", v="32分", c=J.ALERT)])),
    ),

    "ep14": dict(
        t="この事故のあと、何が変わったか",
        s="本文5.1　報告書はそこまで書いている",
        fig=("moment", dict(clock="—", label="事故のあとに講じられた措置",
                            facts=[dict(t="出どころ", v="本文5.1", c=J.DOC)])),
    ),

    "ep15": dict(
        t="8件の勧告が出された",
        s="本文5.1.1　NTSB から FAA へ（A-85-133〜140）",
        fig=("icons", dict(n=8, on=8, kind="dot", cols=8,
                           lead="アメリカの事故調査機関からの勧告",
                           note="航空当局は、耐空性を改善する命令を出している")),
    ),

    "ep16": dict(
        t="点検用の穴が加えられた",
        s="本文5.1",
        fig=("process", dict(steps=[
            dict(t="垂直尾翼の内部", d="点検できるようにする", c=J.LINE),
            dict(t="加えられたもの", d="点検用の穴とカバー", c=J.OK)])),
    ),

    "ep17": dict(
        t="国内でも勧告と建議が出た",
        s="本文5.1　航空事故調査委員会 → 運輸大臣",
        fig=("panel", dict(blocks=[
            dict(k="勧告", c=J.INST, t="航空機の耐空性確保に関する勧告"),
            dict(k="建議", c=J.INST, t="修理の方法と、その確認の仕方の改善")],
            note="いずれも1987年6月19日")),
    ),

    "ep18": dict(
        t="同じ場所が順に点検された",
        s="付図-4　ボーイング式747SR-100型 三面図",
        photo="ja123/f004.jpg", panel=True, side="right", bias=0.58,
        ann=[dict(t="この機種", d="世界中で飛んでいた", dc=J.LINE, ds=32),
             dict(t="行われたこと", d="同じ場所が順に点検され、直された",
                  dc=J.OK, ds=32)],
    ),

    "ep19": dict(
        t="答えの出ていないものが残る",
        s="解説書 §7、§9",
        fig=("absent", dict(mode="ledger", items=[
            dict(t="警報音が1秒で止まった理由", d="示されていない", ok=False),
            dict(t="あの夜、何ができたのか", d="調べる仕組みが無かった",
                 ok=False)],
            lead="それでも残っているもの")),
    ),

    "ep20": dict(
        t="どちらも、そのまま伝える",
        s="40年がたった",
        fig=("panel", dict(blocks=[
            dict(k="分かったこと", c=J.OK, t="物証が示したこと"),
            dict(k="分からないまま", c=J.ALERT, t="記録が残らなかったこと"),
            dict(k="この動画", c=J.LINE, t="そのどちらも、そのまま伝えることを選んだ")],
            cols=1)),
    ),
}
