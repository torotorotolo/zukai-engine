# -*- coding: utf-8 -*-
"""締め その後に残ったもの ep01–ep13（13カット）。11本目（チャレンジャー号）。

■ 🔴 **9カットしか書けていません。**次の4つは**まだ写真の当てが無い**：
     `ep02` joint_redesign／`ep03` joint_test_new／`ep04` srm_vertical_test／
     `ep07` oring_data_chart
   どれも**報告書の図でしか見たことのない主題**。→ `ref/ep11/photo_picks.md` §3-1

■ 実写 7/13（54%）。

■ ✅ `ed01`（共通エンディング）は**この章の末尾に書いてあります**（2026-09-22 ⑤c-3）。
   ⚠️ 以前ここには「⑥で足される」と書いてありましたが、**それは音の話**です
   （`tools/narration.py` が台詞を持ち、`audio/narration.json` に 7.4秒で入っている）。
   **画は章ファイルに要る**＝`check_cuts` は音の側（191カット）を正として数えるので、
   書かないと「画が無いカット」で鳴り続けます。⑤c-2 の「残り15件」は**写真の欄だけ**を
   数えていて、`ed01` が抜けていました。
   🔴🔴 **11本目から並べ替え**＝高評価（左）／アイコン（中央・少し大きく）／登録（右）。
   `titan_fig.ending()` の並びをここで変えてあります → 記憶 [[project-jiko-common-ending]]

■ ⚠️ `ep10`・`ep11` は**乗員7人の実名を置くカット**。会議の出席者とは扱いが違う。
"""
import jiko_style as J
import cuts.ss as ss

P = ss.P

SRC4 = "報告書 第I巻 第IV章"
SRC5 = "報告書 第I巻 第V章"
SRC6F = "報告書 第I巻 第VI章 Findings"
REC = "報告書 第I巻 勧告"

SPEC = {

    # ✅ 2026-09-22 ⑤c-3 で書いた。**実写カット**。
    # 🔴🔴 ⑤c-2 が当てた Commons の `Rogers-report-front-page.png` は題も説明も
    #    「ロジャース委員会の報告書の表紙」と言うのに、**絵は米上院の公聴会記録の表紙**だった
    #    （`cuts/ss.py` の `NG_PHOTOS` に登録ずみ）。
    # ✅ **本物は Internet Archive の蔵書スキャン**（`reporttopreside00unit` の表紙）。
    #    絵を見て確かめた＝大統領章＋青い表紙＋「Report of the PRESIDENTIAL COMMISSION
    #    on the Space Shuttle Challenger Accident」。
    # ⚠️ 左上に図書館のバーコードが写るので `trim` で落とす（画素で測った値）。
    "ep01": dict(
        t="報告書が、出た",
        s="大統領委員会の報告書　1986年6月6日",
        photo=P("commission_report"), panel=True,
        trim=(0.052, 0.062, 0.962, 0.985),
        side="right", ann_y=330,
        ann=[dict(t="最後に置かれたもの", v="9つの勧告", vc=J.ALERT)],
    ),

    # ✅ 2026-09-22 ⑤c-3 で書いた。**実写カット**（NASA画像庫・MSFC）。
    # ⚠️ 894x1110＝幅が足りないので `ss.kind()` が額装に回す。
    "ep02": dict(
        t="まず、あの継ぎ目を作り直す",
        s="作り直したモーターの試験体を据える　1988年",
        photo=P("joint_redesign"), **ss.kind(P("joint_redesign")),
        side="left", ann_y=300,
        # ⚠️ 長い句を注記の数値欄に入れない（Dela・48px 未満に漢字4字以上＝つぶれる）。
        ann=[dict(t="釘を刺された点", v="設計の選択肢", vs=56, vc=J.ALERT,
                  d="日程や費用を理由に、先に消さないこと")],
    ),

    # ✅ 2026-09-22 ⑤c-3 で書いた。**実写カット**。
    # ⚠️ この試験台（TPTA）は NASA の説明に「**温度・圧力・外力**を掛ける」とある。
    #    ep03 の「温度の幅も全部ためす」に、絵のほうから合っている。
    "ep03": dict(
        t="試し方も、書きこまれた",
        s="新しい試験台での燃焼試験　1988年・マーシャル",
        photo=P("joint_test_new"), **ss.kind(P("joint_test_new")),
        side="left", ann_y=300,
        ann=[dict(t="飛ぶときと同じ形で", v="温度の幅も、全部", vc=J.ALERT)],
    ),

    # ✅ 2026-09-22 ⑤c-3 で書いた。**実写カット**。
    # 🔴🔴 **題名で採ると逆になった。**NASA画像庫 `8777958` は題が「継ぎ目」だが、
    #    **絵はクレーンで吊って縦に降ろすところ**で、ep04 が言う「立てた状態」そのもの。
    #    → [[feedback-inventory-is-not-usable-material]]（絵が正本）
    # ⚠️ c804（横たわる試験台）と対になるカット。**向きの対比が画面で分かる**。
    "ep04": dict(
        t="向きも、考え直すこと",
        s="立てた試験台へ降ろす　1987年・マーシャル",
        photo=P("srm_vertical_test"), **ss.kind(P("srm_vertical_test")),
        side="left", ann_y=300,
        # ⚠️ 長い句を注記の数値欄に入れない（Dela・48px 未満に漢字4字以上＝つぶれる）。
        ann=[dict(t="勧告が言ったこと", v="向きを変える", vs=56, vc=J.ALERT,
                  d="立てて燃やす試験も、じゅうぶんに検討する")],
    ),

    "ep05": dict(
        t="外に、見る目を置く",
        s="委員会の公聴会　1986年",
        photo=P("commission_oversight"), **ss.kind(P("commission_oversight")),
        bias=0.45,
    ),

    # 🔴 決め所⑱。この動画の最後の決め所
    "ep06": dict(
        t="いちばん重いのは、そこではない",
        s="設計より前に、あったもの",
        fig=("quote", dict(
            phrase="記録を調べていれば、分かったはずだった",
            who="大統領委員会",
            to="",
            when="1986年6月6日",
            doc=f"{SRC6F} 6")),
    ),

    # ✅ 2026-09-22 ⑤c-3 で書いた。**図で描く**（写真は当てない）。
    # 🔴🔴 報告書 第I巻 第VI章の図6・図7（温度と異常の分布）は**英字が焼き込まれている**ので
    #    画面に出さない＝ `cuts/ss.py` の決まり。
    # ⚠️🔴 **c808 と同じ Findings 6 を指すカット**（c808＝「やった人が、いなかった」・
    #    `absent` の `ledger`）。同じ見せ方を二度やらないよう、ここは **`pair`** にして
    #    「記録は**在った**／調べは**無かった**」の対にする。
    #    10件／150回は第IV章の一覧の集計（"10 instances of distress in a total of
    #    150 flight exposures"）＝原文で照合ずみ。
    "ep07": dict(
        t="材料は、そろっていた",
        s="報告書が、続けて書いたこと",
        fig=("absent", dict(
            mode="pair",
            items=[dict(t="飛行ごとの記録", d="残っていた", ok=True, c=J.DOC, n=10),
                   dict(t="それを並べ直す作業", d="どちらもしていない", ok=False,
                        c=J.ALERT)],
            lead="150回ぶんの飛行のうち、10件に跡があった",
            note=f"{SRC6F} 6")),
    ),

    "ep08": dict(
        t="飛ぶ人を、決める側へ",
        s="委員がケネディ宇宙センターに着く　1986年",
        photo=P("astronaut_manager"), **ss.kind(P("astronaut_manager")),
        bias=0.45,
    ),

    "ep09": dict(
        t="助言の場も、求めている",
        s="委員会の到着　ケネディ宇宙センター・1986年",
        photo=P("safety_panel"), **ss.kind(P("safety_panel")),
        bias=0.45,
    ),

    "ep10": dict(
        t="名前を、もう一度",
        s="追悼式　ヒューストン・1986年",
        photo=P("memorial_wreath"), **ss.kind(P("memorial_wreath")),
        bias=0.45,
    ),

    "ep11": dict(
        t="生中継で、二回の予定だった",
        s="STS-51-L の乗員　1986年",
        photo=P("crew_portrait_3"), **ss.kind(P("crew_portrait_3")),
        bias=0.44,
    ),

    "ep12": dict(
        t="冷たさが、道をふさいだ",
        s="一つ目の問いへの答え",
        fig=("process", dict(
            steps=[dict(t="冷えて硬くなる", d="ゴムの輪", v="", c=J.ALERT),
                   dict(t="つぶれきる", d="押す空気も入らない", v="", c=J.ALERT),
                   dict(t="間に合わない", d="開いていくすきまに", v="",
                        c=J.AMBER)],
            note=SRC4)),
    ),

    "ep13": dict(
        t="その夜だけ、逆さまだった",
        s="二つ目の問いへの答え",
        fig=("beforeafter", dict(
            a=dict(k="ふだん", t="飛べると示す側",
                   lines=["示せなければ飛ばない"], v="", c=J.OK),
            b=dict(k="その夜", t="飛べないと示す側",
                   lines=["示せなければ飛ぶ"], v="", c=J.ALERT),
            arrow=False,
            note=SRC5)),
    ),

    # ── 共通エンディング（全回で同じ。2026-09-21 新設・2026-09-22 に並べ替え）──────
    # 🔴 構想＝2026-09-19 カズヤくん決定（記憶 project-jiko-common-ending）:
    #    暗転なし／高評価・アイコン・登録を**同じ1枚**に／グッドは押されて色が付く／
    #    登録は押されて「登録済み」に変わる／**文字は極力使わない**。
    # 🔴🔴 **11本目から並べ替えた**＝高評価（左）／アイコン（中央・少し大きく）／登録（右）。
    #    並びは `titan_fig.ending()` が持っている（10本目は公開ずみなので直さない）。
    # ⚠️ 見出しは190カット全部に付いている（型の決まり）ので、ここだけ無しにはできない。
    #    ⚠️ 見出しを「ご視聴ありがとうございました」にすると `check_echo` が
    #    「字幕の1文と句点を除いて丸ごと同一」で落ちる（＝画面に出した言葉を字幕にも出している）。
    #    礼はナレーションが言うので、見出しは**画面が何かを言うだけ**の一語にする。
    # ⚠️ 「この動画」は楽屋の言葉（B型）＝**画面には出さない**（ナレーションでは言う）。
    "ed01": dict(
        t="おわり",
        fig=("ending", dict()),
    ),

}
