# -*- coding: utf-8 -*-
"""第10章　疑われたもの cb01–cb16（16カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/cb.py`）。
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
    'cb01': dict(kind='写真',
               plan='B2@12–14（ss_b2_87park の秒）｜副題：南どなりの 87パーク と現場（2021年）｜権利：A推定｜注：札「言われていた話」・重機の CAT はもとから在る字。2秒の区間＝9.0秒は伸ばしすぎ＝13秒のコマ（ss_b2_87park）を静止画で受けるか、走査で 87パーク の写る別の秒',
               src='TR0454（`87 Park is an 18-story luxury condominium built just south of CTS and completed in 2019.`）'),
    'cb02': dict(kind='図解',
               plan='模式図（台本のまま）｜差し込み（head）：1 S#38  5.1秒 S#38（基礎の工事の現場と重機）｜副題：イメージ｜札：イメージ（差し込み）｜権利：Pixabay Content License｜注：杭打ち機の素材は0本＝基礎の工事の重機',
               src='TR0455（`The northern boundary of the soil excavation for the construction of 87 Park was close to the southern boundary of CTS.`）・TR0456（`approximately 9 feet away from the south basement wall of CTS`）'),
    'cb03': dict(kind='図解',
               plan='図 模式図（同じ・揺れの波）｜権利：自作',
               src='TR0457'),
    'cb04': dict(kind='写真',
               plan='N#43（建物の計算機モデルを見る調査団）｜副題：計算機モデルを見る調査団（2023年4月）｜権利：A｜注：—',
               src='TR0460'),
    'cb05': dict(kind='図解',
               plan='図 模式図（揺れの矢印が、地下の壁と鋼の壁で小さくなり、継ぎ目へ届く前にさらに小さく）｜権利：自作',
               src='TR0461'),
    'cb06': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0462（`Vibrations at the critical slab-column connections were too small to have caused structural damage.`）'),
    'cb07': dict(kind='図・写真の頁',
               plan='図 p185 TF のスライド185（札の文＝印字185）',
               src='TF p185（`too small to damage even the distressed connections`）'),
    'cb08': dict(kind='写真',
               plan='B1@⑤b-1（現場の近くの建物の列）｜副題：現場の近くの建物（2021年6〜7月）｜権利：A推定｜注：—',
               src='TR0463・TR0464'),
    'cb09': dict(kind='図解',
               plan='図 一覧（アイコン：基礎・陥没と沈み・ハリケーンと高潮・車の衝突・爆発・クレーンの落下物・屋上の工事＝TF p189 の形）｜権利：自作',
               src='TR0465・TF p189'),
    'cb10': dict(kind='図解',
               plan='図 一覧（同じ・後半を光らせる）｜権利：自作',
               src='TR0465（`accidental loads or overloads caused by the roof repair and roof anchor project ongoing at the time of the collapse`）'),
    'cb11': dict(kind='図解',
               plan='図 模式図【上から】人工衛星で地面の沈みを見る（5年分・沈みの色は無し）｜権利：自作',
               src='A06（`None was seen in the area in the five years before the partial collapse, nor was localized sinking observed near the building in the days leading up to the tragedy.`）'),
    'cb12': dict(kind='図解',
               plan='図 模式図【横から】石灰岩の地面と空洞（水に溶けてできる空洞の説明＝この建物の下には無い）｜権利：自作',
               src='A06（`no evidence of karst in the limestone on which the foundation sits`・`features that actually inhibit the formation of karst`）'),
    'cb13': dict(kind='図解',
               plan="模式図【横から】くいと地下の床（札「くい：強さは足りていた（計算と試験）」）｜副題：—｜権利：自作｜注：🔁 台本は実写（地下の床の写真は在庫に無い）＝§0' の「cb13 のくいを示す図か札」",
               src='A06（`the foundation pile capacity shown on the design drawings was sufficient`・`the basement slab did not show any distress`）'),
    'cb14': dict(kind='図解',
               plan='図 一覧（崩れの起こり＝プールデッキの継ぎ目の余裕の少なさ／大きくは関わっていない＝となりの工事の揺れ・地面・嵐など）｜権利：自作',
               src='TR0476・TR0454・TR0465・TR0474'),
    'cb15': dict(kind='写真',
               plan='N#18 は c702 → N#24（ライダーの撮像を相談する連邦職員）か B2 の別の秒｜副題：—｜権利：A｜注：⑤b-1 で同じ絵を2回使わない',
               src='TR0454（`Things that most probably did not contribute significantly to the collapse include vibrations from the construction of 87 Park.`）'),
    'cb16': dict(kind='写真',
               plan='B1@74–77.8（鉄筋の出た床とコーン）｜副題：崩落の現場の床（2021年6〜7月）｜権利：A推定｜注：—',
               src='—（橋）'),
}

SPEC = {}
