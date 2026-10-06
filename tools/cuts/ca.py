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

SPEC = {}
