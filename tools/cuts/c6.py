# -*- coding: utf-8 -*-
"""第6章 噂はどこから来たのか c601–c633（33カット）。

■ この章の役目
  🔴 **説教にしない。人を責めない。**「そうやって出来るのか」で終える。
  c631「信じた人が軽率だった、という話ではない」がこの章の良心。

■ 🔴 c615 は quote にしない
  偽の文言（「撃たれた」）を画面いっぱいに出すと、**それ自体が拡散の材料になる**。
  図には**どう作られたか**（音声が途切れた箇所に字幕だけが載っていた）を置く。

■ 写真をほとんど使わない章
  ここで残骸の写真を敷くと、噂の話に事故の画が付いて「噂の裏づけ」に見える。
  出すのは**操縦室の記録が公開されている／音声は公開されていない**という
  対比の1枚だけにしてある（c626）。

■ 出どころ
  この章だけは報告書ではなく、**検証記事・ファクトチェック・報道**。
  画面の出典欄でそのことが分かるようにしてある。
"""
import jiko_style as J

SPEC = {

    "c601": dict(
        t="話がどう生まれたのかを見る",
        s="ここまでは、答えを当ててきた",
        fig=("moment", dict(clock="—", label="視点を変える",
                            facts=[dict(t="ここまで", v="語られてきたことへの答え",
                                        c=J.OK),
                                   dict(t="ここから", v="その話の生まれ方",
                                        c=J.AMBER)])),
    ),

    "c602": dict(
        t="よく引かれる言葉がある",
        s="この発言の出どころを追う",
        fig=("quote", dict(phrase="真実は墓場まで持っていく",
                           who="当時の総理大臣が語ったとされる",
                           to="出どころは特定されていない",
                           when="※ 発言そのものが確認できない",
                           doc="ジャーナリストによる検証記事")),
    ),

    "c603": dict(
        t="引用元に、その発言は無い",
        s="検証記事",
        fig=("absent", dict(mode="single", items=[
            dict(t="引用元とされた記事", d="見当たらない", ok=False)],
            lead="出どころを追った結果")),
    ),

    "c604": dict(
        t="150紙誌を検索しても出ない",
        s="検証記事",
        fig=("absent", dict(mode="ledger", items=[
            dict(t="新聞・雑誌 約150紙誌のデータベース", d="該当なし", ok=False)],
            lead="発言の出どころを探した範囲")),
    ),

    "c605": dict(
        t="国会にも、対談本にも無い",
        s="検証記事",
        fig=("absent", dict(mode="ledger", items=[
            dict(t="国会の会議録", d="無い", ok=False),
            dict(t="対談本", d="無い", ok=False)],
            lead="さらに探した範囲")),
    ),

    "c606": dict(
        t="否定以前に、確認できない",
        s="何が確かめられていないか",
        fig=("beforeafter", dict(
            a=dict(k="思われがち", t="報告書が否定している", c=J.LINE),
            b=dict(k="実際", t="発言そのものが確認できない", c=J.ALERT))),
    ),

    "c607": dict(
        t="もうひとつ、よく語られる話",
        s="検証記事",
        fig=("panel", dict(blocks=[
            dict(k="噂", c=J.ALERT, t="技術者が消されたという話")],
            lead="言われていること（2つめ）")),
    ),

    "c608": dict(
        t="技術者17人が乗っていた説",
        s="検証記事",
        fig=("panel", dict(blocks=[
            dict(k="噂", c=J.ALERT, t="基本ソフトの開発者", v="17人"),
            dict(k="噂", c=J.ALERT, t="貿易上の対立が背景")],
            lead="話の骨子")),
    ),

    "c609": dict(
        t="現れたのは2008年ごろ",
        s="検証記事　事故から23年後",
        fig=("timeline", dict(t0=1985, t1=2010,
                              ticks=[(1985, "1985"), (1995, "1995"),
                                     (2008, "2008")],
                              events=[dict(t=1985, top="事故", c=J.LINE),
                                      dict(t=2008, top="ネット上に現れる",
                                           c=J.ALERT, big=True)],
                              band=[dict(a=1985, b=2008, c=J.LINE, op=0.10,
                                         t="23年間")])),
    ),

    "c610": dict(
        t="17という数字の元がある",
        s="検証記事　新聞の見出し",
        fig=("panel", dict(blocks=[
            dict(k="元", c=J.DOC, t="ある電機グループの社員", v="17人"),
            dict(k="形", c=J.LINE, t="新聞の見出しの数字")])),
    ),

    "c611": dict(
        t="部署も場所も合わない",
        s="検証記事",
        fig=("mapfig", dict(
            points=[dict(x=0.24, y=0.72, t="大阪", d="基本ソフトの開発",
                         c=J.OK),
                    dict(x=0.74, y=0.24, t="東京", d="関連する事業部", c=J.LINE)],
            lead="亡くなった人の部署（映像・音響）",
            note="位置関係だけを示す略図（縮尺は正確ではない）")),
    ),

    "c612": dict(
        t="時期も合わない",
        s="検証記事",
        fig=("timeline", dict(t0=1985, t1=1995,
                              ticks=[(1985, "1985.8"), (1990, "1990年代")],
                              events=[dict(t=1985, top="まだ試作の段階",
                                           c=J.LINE),
                                      dict(t=1990, top="製品として世に出る",
                                           c=J.AMBER)])),
    ),

    "c613": dict(
        t="並べるだけで合わなくなる",
        s="この話の確かめ方",
        fig=("panel", dict(blocks=[
            dict(k="やること", c=J.OK, t="日付と場所を並べる"),
            dict(k="ただし", c=J.LINE, t="並べてみるまでは分からない")])),
    ),

    "c614": dict(
        t="3つめは、ごく最近のもの",
        s="ファクトチェック　2025年",
        fig=("moment", dict(clock="—", label="2025年に広まった話",
                            facts=[dict(t="いつ", v="2025年", c=J.ALERT)])),
    ),

    # ── c615 🔴 quote にしない。偽の文言を大きく出さない ────────────
    "c615": dict(
        t="録音に未公開部分がある説",
        s="ファクトチェック　2025年に拡散した紹介",
        fig=("panel", dict(blocks=[
            dict(k="噂", c=J.ALERT, t="操縦室の録音に、公開されていない部分がある"),
            dict(k="噂", c=J.ALERT, t="そこに機長の声が入っている、と紹介された")],
            lead="そう紹介された内容",
            note="この動画では、その文言そのものを画面に出さない")),
    ),

    "c616": dict(
        t="表示回数は600万を超えた",
        s="ファクトチェック",
        fig=("compare", dict(bar=True, vmax=6000000, items=[
            dict(v=6000000, disp="600万", unit="回超", t="投稿の表示回数",
                 c=J.ALERT),
            dict(v=400000, disp="40万", unit="回以上", t="作られた動画の再生",
                 c=J.AMBER)],
            ref="600万回を上限として比べている")),
    ),

    "c617": dict(
        t="判定は「根拠不明」だった",
        s="ファクトチェック団体",
        fig=("absent", dict(mode="single", items=[
            dict(t="公開された記録の中の該当発言", d="無い", ok=False)],
            lead="団体が出した判定")),
    ),

    "c618": dict(
        t="音が無い所に字幕があった",
        s="ファクトチェック　どう作られたか",
        fig=("process", dict(steps=[
            dict(t="問題の箇所を聴く", d="音声が途切れている", c=J.ALERT),
            dict(t="そこに字幕", d="字幕だけが載っていた", c=J.ALERT)])),
    ),

    "c619": dict(
        t="放送局は偽の動画と答えた",
        s="報道",
        fig=("people", dict(
            nodes=[dict(x=0.22, y=0.50, t="取材", kind="person", c=J.LINE),
                   dict(x=0.76, y=0.50, t="放送局", kind="org", c=J.INST)],
            edges=[dict(a=1, b=0, t="偽の動画である", c=J.OK)],
            note="だが、広まったあとだった")),
    ),

    "c620": dict(
        t="4つめは、噂についての噂",
        s="ファクトチェック　2025年",
        fig=("moment", dict(clock="—", label="国会に関する話",
                            facts=[dict(t="いつ", v="2025年", c=J.ALERT)])),
    ),

    "c621": dict(
        t="拡散の規模は46万回超",
        s="ファクトチェック",
        fig=("panel", dict(blocks=[
            dict(k="噂", c=J.ALERT, t="議員が撃墜を認めた"),
            dict(k="規模", c=J.AMBER, t="投稿の表示回数", v="46万回以上")])),
    ),

    "c622": dict(
        t="実際にしていたことは逆だった",
        s="ファクトチェック",
        fig=("beforeafter", dict(
            a=dict(k="紹介された内容", t="議員が撃墜を認めた", c=J.ALERT),
            b=dict(k="実際の場面", t="書籍で広がる主張を問題視",
                   lines=["読み上げていた場面だった"], c=J.OK))),
    ),

    "c623": dict(
        t="切り取れば意味は反転する",
        s="切り取りの効き方",
        fig=("panel", dict(blocks=[
            dict(k="本人の立場", c=J.OK, t="正反対である"),
            dict(k="起きたこと", c=J.ALERT, t="一部分だけを切り取ると意味が反転する")])),
    ),

    "c624": dict(
        t="生まれ方には4つの型がある",
        s="この章で見てきたもの",
        fig=("panel", dict(blocks=[
            dict(k="1", c=J.ALERT, t="存在しない発言"),
            dict(k="2", c=J.ALERT, t="見出しの読み違い"),
            dict(k="3", c=J.ALERT, t="途切れた音声"),
            dict(k="4", c=J.ALERT, t="切り取られた場面")], cols=2)),
    ),

    "c625": dict(
        t="なぜ、この事故で育つのか",
        s="この章の最後の問い",
        fig=("moment", dict(clock="—", label="育ちやすい理由",
                            facts=[dict(t="理由", v="公開と非公開の差",
                                        c=J.AMBER)])),
    ),

    "c626": dict(
        t="文字は1987年に公開された",
        s="付図-12　操縦室パネル配置図（本文 別添にCVR記録）",
        photo="ja123/f012.jpg", panel=True, side="right",
        ann=[dict(t="公開されているもの", d="文字に起こした記録", dc=J.OK, ds=32),
             dict(t="どこに", d="報告書 本文 別添", dc=J.LINE, ds=32)],
    ),

    "c627": dict(
        t="公開されていないのは音声",
        s="報道",
        fig=("absent", dict(mode="pair", items=[
            dict(t="何を話したか", d="文字で分かる", ok=True, n=1),
            dict(t="どんな声だったか", d="分からない", ok=False, n=0)],
            lead="操縦室の記録")),
    ),

    "c628": dict(
        t="2021年、開示を求める裁判",
        s="報道",
        fig=("people", dict(
            nodes=[dict(x=0.22, y=0.50, t="遺族2人", d="1人は副操縦士の親族",
                        kind="person", c=J.INK_W),
                   dict(x=0.76, y=0.50, t="音声の開示", kind="doc", c=J.DOC)],
            edges=[dict(a=0, b=1, t="2021年 提訴", c=J.AMBER)],
            note="求めたのは、文字ではなく音声そのもの")),
    ),

    "c629": dict(
        t="訴えは退けられた",
        s="報道",
        fig=("absent", dict(mode="single", items=[
            dict(t="音声の公開", d="いまも行われていない", ok=False)],
            lead="裁判の結果")),
    ),

    "c630": dict(
        t="ここに余地が生まれる",
        s="公開と非公開のあいだ",
        fig=("panel", dict(blocks=[
            dict(k="分かる", c=J.OK, t="何を話したか"),
            dict(k="聞けない", c=J.ALERT, t="どんな声だったか"),
            dict(k="隙間", c=J.AMBER, t="偽の音声が入り込む余地")],
            cols=1)),
    ),

    "c631": dict(
        t="軽率だった、という話ではない",
        s="責める話にしない",
        fig=("absent", dict(mode="single", items=[
            dict(t="信じた人の落ち度", d="そういう話ではない", ok=False)],
            lead="文字だけが手元にあるとき")),
    ),

    "c632": dict(
        t="分けて知っておくこと",
        s="できることは、ひとつだけ",
        fig=("absent", dict(mode="pair", items=[
            dict(t="公開されているもの", d="文字に起こした記録", ok=True, n=1),
            dict(t="公開されていないもの", d="音声そのもの", ok=False, n=0)],
            lead="操縦室の記録の公開状況")),
    ),

    "c633": dict(
        t="答えは図に描かれている",
        s="エピローグへ",
        fig=("moment", dict(clock="—", label="この事故は何によって起きたのか",
                            facts=[dict(t="答えの在りか", v="1枚の図",
                                        c=J.AMBER)])),
    ),
}
