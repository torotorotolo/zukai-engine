# -*- coding: utf-8 -*-
"""第9章　塔へ渡り、西で止まった ca01–ca21（21カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/ca.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep19/make_plan19.py` で
  映像方針の一覧 `ref/ep19/eizou_build/list19.tsv`（承認ずみ・決め①〜⑩）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」と「フリー素材」を数える）。
  ⚠️ plan の「⑤b-1」は1秒1コマの走査で区間を選ぶ所・秒（÷365 の見込み）は書き写さない＝narration.json の実測で組む。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P
from illu import A1_REC as IL_REC  # noqa: E402  🆕 ⑤b-2：A1 の部品の出典（描く側と同じ文）

PLAN = {
    'ca01': dict(kind='再現イラスト',
               plan='図 再現イラスト A1【正面から】塔の南の面と崩れ落ちたプールデッキ（「推定」の札）｜札：推定｜権利：自作',
               src='TR0285・TR0286（`if the pool deck and street-level parking slab collapse had not spread into the tower, the disastrous part of this failure would not have occurred`）'),
    'ca02': dict(kind='図解',
               plan='図 模式図【横から】塔とプールデッキの境（2本の梁＝K と L の札・9.1 の線）｜権利：自作',
               src='TR0287〜0289'),
    'ca03': dict(kind='図解',
               plan='図 模式図（同じ・梁と床が外れ、継ぎ目から鉄筋とコンクリートを引き抜く）｜権利：自作',
               src='TR0292・TR0293（`bearing the load of 13 stories of structure from the column above`）'),
    'ca04': dict(kind='図解',
               plan='図 模式図【横から】継ぎ目の断面（柱＝緑・床＝灰色＝AC p.65 の形）｜権利：自作',
               src='TR0294〜0296・AC p.65（`Column concrete (green): Design compressive strength = 6000 psi`・`Floor concrete (grey): Design compressive strength = 4000 psi`）'),
    'ca05': dict(kind='図解',
               plan='図 模式図（同じ・柱の縦の鉄筋・輪の形の鉄筋が無い所＝AC p.71 の形）｜権利：自作',
               src='TR0297・AC p.71（`The absence of column ties in the joint left the column longitudinal reinforcement unbraced against buckling.`）・AC p.64（`The concentration of longitudinal column reinforcement exceeded ACI 318 limits.`）'),
    'ca06': dict(kind='写真',
               plan='TLS（ミネソタ大学の据え付けのタイムラプス）｜副題：試験体を据える（ミネソタ大学）｜権利：A推定（大学の撮影の可能性）｜注：🔁 台本の型 fb_c607',
               src='TR0298・TR0299・A06（`tested until failure at the University of Minnesota`）'),
    'ca07': dict(kind='図解',
               plan='図 数の比べ（約295トン＝20トンの大型トラック約15台分・式は§9）｜権利：自作',
               src='TR0302（`a vertical load of 650,000 pounds`・`representing the load in the column at the time of failure`）・§9'),
    'ca08': dict(kind='写真',
               plan='TL（試験体の床が柱から外れるタイムラプス）｜副題：試験体が壊れる（ミネソタ大学）｜権利：A推定｜注：右下の NIST の透かしを切る',
               src='TR0303・TR0306'),
    'ca09': dict(kind='写真',
               plan='N#72 か N#60（試験のあとの標本）か AC p.72 の頁｜副題：試験のあとの継ぎ目（ミネソタ大学・2025年）｜権利：A｜注：「外へ曲がった鉄筋」が写る物を⑤b-1で',
               src='TR0307〜0309・AC p.72（`Buckled Steel Reinforcement`）'),
    'ca10': dict(kind='図解',
               plan='図 模式図【横から】継ぎ目が押しつぶされ、柱が下がる（「推定」の札）｜札：推定｜権利：自作',
               src='TR0312・TR0313・AC p.73（`If the requirements of the current edition of the building code for structural concrete, ACI 318-25, had been in effect and followed at the time of original design and construction of CTS, the performance of the joint could have been improved.`）'),
    'ca11': dict(kind='図解',
               plan='図 模式図【正面から】南から北へ崩れる塔の真ん中（屋根が下がり、柱の頭が突き出す＝TR0365〜0367 の画の型・「推定」の札）｜札：推定｜権利：自作',
               src='TR0362・TR0363・TR0365〜0368'),
    'ca12': dict(kind='図・写真の頁',
               plan='TFV@TR0371（止まった境＝ゾーン A・B の図・青い真ん中の部分と点線）｜副題：NIST の技術的知見のスライド（止まった境 A・B）｜権利：A（右の写真〈TR0373〉は出どころを確かめる＝©2021 なら切る）｜注：🔁 台本は実写（B2 の空撮）＝解体の後の空撮に境は写らない・B1 の残った棟は c621・c711・cc04 で足りなくなる→ NIST の図に',
               src='TR0369〜0371'),
    'ca13': dict(kind='写真',
               plan='N#17（残った棟とせん断された断面）｜副題：残った西の部分の断面（2021年6月30日ごろ）｜権利：A｜注：決め⑤＝🅰 引きだけ：⑤b-1 で原寸を見て、家具・写真・服が見分けられる住戸に寄せない（見分けられれば C1・C2 か B1 の引きに替える）',
               src='TR0372・TR0373'),
    'ca14': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0376（`the strength of the concrete wall prevented the failure from spreading beyond it`）'),
    'ca15': dict(kind='写真',
               plan='TFV@TR0377（TF の写真のコマ）｜副題：—｜権利：要確認｜注：⑤b-1 で出どころの札を読む。©2021 なら使わず B1@159〜160',
               src='TR0377'),
    'ca16': dict(kind='図解',
               plan='図 模式図【横から】壁の無い境（床の板が先に折れる＝①／柱の継ぎ目の押し抜き＝②＝TR0384 の図の型）｜権利：自作',
               src='TR0374・TR0375・TR0382〜0385'),
    'ca17': dict(kind='写真',
               plan='TFV@TR0379（TF の写真のコマ）｜副題：—｜権利：要確認｜注：同上。代わり＝tf_p139_bars（図）',
               src='TR0379・TR0380・TR0385（`failure would occur at 1 before 2, and so the failure did not advance into the west part of the tower`）・TR0392'),
    'ca18': dict(kind='再現イラスト',
               plan='図 再現イラスト A1【正面から】東の部分が西へ傾く（12階が約53センチの札・「推定」の札）｜札：推定｜権利：自作',
               src='TR0406・TR0413・TR0421（`the 12th floor has moved west about 21 inches`）・TR0422'),
    'ca19': dict(kind='写真',
               plan='N#11（がれきの山から柱を移す）｜副題：がれきから運び出す柱（2021年7月7日）｜権利：A｜注：TF の TR0427 の写真が使えればそちら',
               src='TR0426〜0429'),
    'ca20': dict(kind='図解',
               plan='図 年表（1979〜81年 設計＝連鎖を止める定め無し → 1989年 連鎖に強くする鉄筋の決まり → 2025年 今の決まり）｜権利：自作',
               src='AC p.75・AC p.76（`did not include provisions to limit progressive collapse`・`Starting in 1989 ... required structural integrity reinforcement`・`limited in their ability to arrest progressive collapse in some structures`）・TR0396・TR0433'),
    'ca21': dict(kind='写真',
               plan='D（DHS の現場の写真・肖像の写らない引き）｜副題：撤去の後の現場（2021年8月19日）｜権利：A（DHS）｜注：決め⑥＝15点を全部取得し、犠牲者の写真・遺族・花の寄りが写らない引きだけ。代わり＝B2 の別の秒',
               src='—（橋）'),
}

TR_SRC = "NIST の技術的知見の動画（2026年6月）"

SPEC = {
    # ── 🆕 ⑤b-2（2026-10-06）：案C の置き場 A1（南から見た塔）。秒は narration.json の実測
    #   （ca01 0〜2.84／3.33〜6.91／7.40〜9.45・ca18 0〜5.41／5.90〜8.80）
    # ca01＝「推定」。1行目（聞き役）：プールデッキが地下へ崩れる／2行目：塔の南の面の継ぎ目へ寄る（NIST の大事な問い＝広がらなければ）／3行目：そのまま
    "ca01": dict(
        fig=("illu", dict(
            place="A1", rec="TR p1285・p1286（崩れが塔へ広がらなければ、惨事の部分は起きなかった）",
            assume="推定（NIST の見立て）",
            steps=[dict(state=dict(a1deck="fell"), delay=0.6, rec=IL_REC["deck_fell"],
                        # ⑤b-2 の下見（cc25 と同じ形）：下へ出すと左下の出典の行（y884）に重なる＝塔の左の空へ
                        tag=dict(t="プールデッキが崩れる", at="deck", off=(-470, -70), anchor="end")),
                   dict(state=dict(cam=1.10), delay=0.2, dur=3.0, rec="TR p1286",
                        tag=dict(t="塔の南の面の継ぎ目", at="joint", off=(120, -150))),
                   dict(delay=0.2)], camc="joint")),
    ),
    # ca18＝「推定」。1行目：揺さぶられたあと、東の部分の12階が西へずれる（札は記録の値＝約53cm・揺れの幅は大きく描く＝左下の断り）／
    #   2行目：下の階の柱の限りを超える（落ちるのは次のカットの語り＝ここでは落とさない）
    "ca18": dict(
        fig=("illu", dict(
            place="A1", start=dict(a1deck="fell", a1mid="fell"), rec="TR p1417（真ん中の部分のほとんどが崩れた）",
            assume="推定（NIST の見立て）",
            steps=[dict(state=dict(a1sway=-32.0), delay=0.8, dur=1.6, rec=IL_REC["sway"],       # ⑤b-2 の下見：浮きを抑える（c620 と同じ）
                        tag=dict(t="12階が西へ約53cm", at="east12", off=(-40, -90), anchor="end")),
                   dict(state=dict(cam=1.05), delay=0.2, dur=2.6, rec="TR p1422（揺れが下の階の柱の耐えられる限りを超えた）",
                        tag=dict(t="下の階の柱", at="heap", off=(160, -190)))])),
    ),
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）──
    # ca02（7.05秒＝0〜3.08／3.57〜7.05）＝崩れが塔との境へ・2本の梁 A（TR0287〜0289・TF p9111）
    "ca02": dict(
        t="崩れの北の端", s="2本の梁",
        fig=("m19", dict(view="edge", start=dict(fall="part"),
                         steps=[dict(state=dict(fall="full"), delay=0.3, tag=dict(t="塔との境（9.1 の線）", at="face", to="face")),
                                dict(state=dict(beam="on"), delay=0.3, tag=dict(t="梁（K と L の線に1本ずつ）", at="beam", to="beam"))],
                         rel=[dict(t="9.1", src="TR p1287（gridline 9.1）"), dict(t="1本ずつ", src="TR p1288（beams A at grid lines K and L）")],
                         note="床の落ち方・梁の長さは NIST の図の形の模式", src=TR_SRC + "の語りとスライド")),
    ),
    # ca03（7.85秒＝0〜4.42／4.92〜7.85）＝梁と床が継ぎ目から引き抜く・13階分の重さ（TR0292・0293）
    "ca03": dict(
        t="引き抜かれた継ぎ目", s="上の13階分を支える所",
        fig=("m19", dict(view="edge", start=dict(fall="full", beam="on"),
                         steps=[dict(state=dict(pull="on", joint="hurt"), delay=0.3,
                                     tag=dict(t="鉄筋ごと引き抜く", at="pull", to="joint")),
                                dict(state=dict(load="on"), delay=0.3, tag=dict(t="上の13階分の重さ", at="load", to="face"))],
                         rel=[dict(t="13階", src="TR p1293（13 stories of structure）")],
                         note="床の落ち方・梁の長さは NIST の図の形の模式", src=TR_SRC + "の語りとスライド")),
    ),
    # ca04（10.70秒＝0〜1.85／2.34〜7.70／8.19〜10.70）＝床のコンクリートの設計の強さ（AC p.65＝柱 6000・床 4000 psi）
    "ca04": dict(
        t="継ぎ目の弱さ（1つ目）", s="床と柱の材料",
        fig=("m19", dict(view="joint",
                         steps=[dict(tag=dict(t="柱と床が交わる所", at="q", to="zone")),
                                dict(state=dict(color="on"), delay=0.3,
                                     tag=[dict(t="柱のコンクリート", at="col", to="col"),
                                          dict(t="床のコンクリート", d="設計の強さが低い", at="floor", to="floor")]),
                                dict(state=dict(bar2="on"), delay=0.3, tag=dict(t="柱の約3分の2", at="ratio"))],
                         rel=[dict(t="3分の2", src="AC p2065（6000 psi・4000 psi）")],
                         note="断面は NIST の図の形の模式（棒の長さは設計の強さの比）", src="NIST の諮問委員会の資料（2026年9月） p.65")),
    ),
    # ca05（12.78秒＝0〜5.34／5.83〜8.85／9.34〜12.78）＝輪の形の鉄筋が無い・縦の鉄筋の詰め込み（TR0297・AC p.71・p.64）
    "ca05": dict(
        t="継ぎ目の弱さ（2つ目）", s="鉄筋の組み方",
        fig=("m19", dict(view="joint", start=dict(color="on"),
                         steps=[dict(state=dict(bars="on", ties="on"), delay=0.3, tag=dict(t="継ぎ目に輪の形の鉄筋が無い", at="ties", to="zone")),
                                dict(state=dict(buckle="on"), delay=0.3, tag=dict(t="縦の鉄筋が外へ曲がりやすい", at="buckle", to="bars")),
                                dict(state=dict(dense="on"), delay=0.3, tag=dict(t="上限を超えて詰め込み", at="dense", to="bars"))],
                         note="鉄筋の本数と曲がりは模式（輪の形の鉄筋が無い高さは NIST の図）",
                         src="NIST の諮問委員会の資料（2026年9月） p.64・p.71")),
    ),
    # ca10（8.19秒＝0〜3.63／4.12〜8.19）＝あの夜も押しつぶされた（推定＝TR0312・0313）・今の決まりなら（AC p.73）
    "ca10": dict(
        t="あの夜の継ぎ目", s="試験と同じ壊れ方",
        fig=("m19", dict(view="joint", start=dict(color="on", bars="on", ties="on"),
                         steps=[dict(state=dict(crush="on"), delay=0.3, tag=dict(t="押しつぶされた（推定）", at="crush", to="zone")),
                                dict(tag=dict(t="今の決まりなら良くなり得た", at="code"))],
                         note="推定（NIST の見立て）・つぶれ方は模式", src="NIST の諮問委員会の資料（2026年9月） p.73")),
    ),
    # ca11（10.89秒＝0〜3.52／4.01〜8.27／8.76〜10.89）＝屋根が下がり柱の頭が突き出す（TR0362〜0368・TF p9137）
    "ca11": dict(
        t="南から北へ", s="屋根と柱の頭",
        fig=("m19", dict(view="front",
                         steps=[dict(state=dict(q="on"), delay=0.3, tag=dict(t="同時か、どちらが先かは不明", at="q", to="q")),
                                dict(state=dict(roof="down"), delay=0.3, tag=dict(t="柱の頭（K-4・L-4）が突き出す", d="推定の模式", at="heads", to="heads")),
                                dict(state=dict(dir="on"), delay=0.3, tag=dict(t="南→北", at="dir"))],
                         rel=[dict(t="K-4・L-4", src="TR p1366（columns at grid points K-4 and L-4）")],
                         note="推定（NIST の見立て）・塔の形と崩れ方は模式（映像そのものは出さない）", src=TR_SRC + "の語りとスライド")),
    ),
    # ca16（11.56秒＝0〜3.72／4.21〜7.99／8.48〜11.56）＝Zone B（TR0374・0375・0382〜0385・TF p9144）
    "ca16": dict(
        t="壁の無い境", s="崩れが止まった所",
        fig=("m19", dict(view="zoneb",
                         steps=[dict(state=dict(zone="on"), delay=0.3, tag=dict(t="壁が無く、床と柱が続く所", at="zone")),
                                dict(state=dict(mark="on", brk="on"), delay=0.3,
                                     tag=[dict(t="① 床の板が先に折れた", at="one", to="one"), dict(t="② 継ぎ目は保つ", at="two", to="two")]),
                                dict(state=dict(bar="on"), delay=0.3, tag=dict(t="上の鉄筋が途切れる辺り", at="bar", to="bar"))],
                         note="柱の間隔・鉄筋の長さ・傾きは NIST の図の形の模式", src=TR_SRC + "の語りとスライド")),
    ),
    # ── 🆕 ⑤b-5（2026-10-06）：年表（`tools/axis.py`・門番 check_axis）──
    # ca20（11.26秒＝0〜3.17／3.66〜7.35／7.84〜11.26）＝AC p.76 の3つ（設計のころは連鎖を止める定め無し・1989年から鉄筋・ACI 318-25 でも
    #   止めきれない建物がある）を1行ずつ。2025＝ACI 318-25（2025年の版）
    "ca20": dict(
        t="決まりの移り変わり", s="崩れの連鎖への備え",
        fig=("axis", dict(ss.AX_CODE, steps=[
            dict(add=ss.ax("cd79"), cur="1981"),
            dict(add=ss.ax("cd89"), cur="1989"),
            dict(add=[ss.ax("cd25"), dict(k="chips", at="2025", chips=["止めきれない建物もある"], rec="AC p2076")], cur="2025")],
            note="年だけの記録はその年の真ん中に置いた・2025年は今の決まり（ACI 318-25）の版", src=ss.src(["AC p2023・p2075・p2076"]))),
    ),
    # ── 🆕 ⑤b-6（2026-10-06）：数の比べ（量の型 qty）──
    # ca07（10.88秒＝0〜3.79／4.28〜8.54／9.03〜10.88 聞き役）＝試験の柱にかけた重さ（TR0302＝65万ポンド）。1行目で棒・2行目は目盛り（20トンごと＝
    #   大型トラック1台の目安）で読む。🔴 トラックは記録の値ではない＝棒にしない
    "ca07": dict(
        t="試験でかけた重さ", s="崩れたときの柱の重さ",
        fig=("qty", dict(view="bar", groups=[ss.QG["load"]], steps=[
            dict(add=ss.qb("l_col")), dict(), dict()],
            note="目盛りの1つ＝20トン＝大型トラック1台の目安・記録は65万ポンド", src=ss.src(["TR p1302"]))),
    ),
}
