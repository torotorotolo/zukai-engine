# -*- coding: utf-8 -*-
"""第3章　29か月 c401–c419（19カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c4.py`）。
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
    'c401': dict(kind='図解',
               plan='図 時間の帯（2018-10-08 報告 → 2018-11-15 会議 → 2021-04 手紙 → 2021-06-24・「29か月」の帯は報告から2021年4月まで）｜権利：自作',
               src='MIN18 p.6〜7・GJ p.17'),
    'c402': dict(kind='文字の頁',
               plan='図 p3020 大陪審の報告 p.17（文字の頁・`as early as October 8, 2018` の段）',
               src='GJ p.17（`as early as October 8, 2018 the Champlain South condo board was aware of significant necessary repairs and maintenance`）'),
    'c403': dict(kind='図解',
               plan='図 書類の再現図 議事録の段（2018-11-15・`Structural engineer report was reviewed …`・名前は出さない）｜権利：自作',
               src='MIN18 p.7'),
    'c404': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='MIN18 p.7（`it appears the building is in very good shape`）・GJ p.17'),
    'c405': dict(kind='フリー素材',
               plan='S#16（書類とペンの手元）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：紙の字が読めない秒・寄りで',
               src='MIN18 p.7'),
    'c406': dict(kind='写真',
               plan='B2@99–108（片づいたデッキの床面と重機）｜副題：プールデッキの跡（崩落の後・2021年）｜権利：A推定｜注：—',
               src='GJ p.17〜18'),
    'c407': dict(kind='文字の頁',
               plan='図 p3021 大陪審の報告 p.18（文字の頁・`routine repairs and maintenance` の段）',
               src='GJ p.18'),
    'c408': dict(kind='図解',
               plan='図 数の比べ（1,400万ドル超 → 約15億円 → 136戸で割ると1戸あたり約1,100万円）｜権利：自作',
               src='GJ p.18（`more than $14,000,000`）・§9'),
    'c409': dict(kind='図解',
               plan='図 時間の帯（2018年秋 報告 → 2021年4月＝「29か月あまり」）｜権利：自作',
               src="GJ p.18（`more than 29 months after the engineer's report was received`）"),
    'c410': dict(kind='文字の頁',
               plan='図 p3021 大陪審の報告 p.18（文字の頁・29か月の段の切り出し）',
               src='GJ p.18'),
    'c411': dict(kind='フリー素材',
               plan='S#8（白い壁のひび）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：—',
               src='GJ p.18'),
    'c412': dict(kind='図解',
               plan='図 書類の再現図 手紙の抜粋（大陪審の報告 p.18 が引く文・名前は出さない）｜権利：自作',
               src='GJ p.18'),
    'c413': dict(kind='図解',
               plan='図 模式図【上から】はがす範囲（プールデッキ・入口の車道・地上の駐車場・プランター）｜権利：自作',
               src='GJ p.18（`we must pull up almost the entire ground level of the lot`）'),
    'c414': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='GJ p.18（`The concrete deterioration is accelerating.`）'),
    'c415': dict(kind='図解',
               plan='図 時間の帯（2021年4月 → 入札を開く予定の会議 → 13日 → 6月24日）｜権利：自作',
               src='GJ p.18'),
    'c416': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='GJ p.18（`Thirteen days after the Board was to hold a meeting to open the bids …, the building collapsed.`）'),
    'c417': dict(kind='写真',
               plan='B1@198–203.5（高い所からの現場と海）｜副題：崩落の現場と海（2021年6〜7月）｜権利：A推定｜注：204秒〜の表題カードを避ける（until）',
               src='GJ p.18・MIN18 p.7'),
    'c418': dict(kind='図解',
               plan='図 年表（2018年10月 報告 → 11月 会議 → 2021年4月 手紙・29か月 → 入札の会議 → 13日後）｜権利：自作',
               src='GJ p.1（題 `RECOMMENDATIONS TO MAKE BUILDINGS SAFER`・`policies, procedures, protocols, systems and practices`）・GJ p.17〜18'),
    'c419': dict(kind='写真',
               plan='B2@⑤b-1（110〜113.25 の現場の引きとその前）｜副題：現場の空撮（崩落の後・2021年）｜権利：A推定｜注：3.25秒を2.7倍に伸ばさない＝走査で続きの秒・無ければ 111秒のコマを静止画で受ける。114秒〜の表題カードを避ける',
               src='—（橋）'),
}

SPEC = {}
