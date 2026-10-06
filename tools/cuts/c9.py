# -*- coding: utf-8 -*-
"""第8章　見えなかったもの c901–c923（23カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c9.py`）。
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
    'c901': dict(kind='写真',
               plan='B3@40–46（倉庫で部材の鉄筋を測る）｜副題：倉庫で証拠を測る（2022年）｜権利：A推定｜注：調査員の顔＝公務',
               src='TR0213'),
    'c902': dict(kind='図解',
               plan='図 模式図 2つの物差し（建てた当時の決まり／今の決まり）｜権利：自作',
               src='TR0213・TR0214'),
    'c903': dict(kind='図解',
               plan='図 模式図【上から】強さが足りない所（黄＝中くらい・赤＝ひどい＝TR0215〜0216 の図の型）｜権利：自作',
               src='TR0215・TR0216'),
    'c904': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0219（`In some locations, the design provided less than half of the code-required strength.`）'),
    'c905': dict(kind='図解',
               plan='図 模式図 2つの物差し（同じ・当時の決まりの物差しにも欠けた所＝決まりの限界）｜権利：自作',
               src="TR0279（`design understrength caused by severe and widespread deviations in the building's original structural design from the codes and standards of the day, but also some limitations in those codes and standards`）"),
    'c906': dict(kind='図・写真の頁',
               plan='tf_p075_cover（TF スライド75＝かぶり・床の断面の写真）｜副題：NIST の技術的知見のスライド75｜権利：A｜注：🔁 台本は実写（NIST の写真）→ 同じ中身のスライドに',
               src='TR0220'),
    'c907': dict(kind='図解',
               plan='図 模式図【横から】鉄筋の上のコンクリートの厚さ（図面＝約1.9センチ〈4分の3インチ〉／実際＝約5センチ〈2インチ〉・上の鉄筋が下がる）｜権利：自作',
               src='TR0221（`the cover was generally about 2 inches rather than 3/4 of an inch shown on the drawings`）'),
    'c908': dict(kind='図解',
               plan='図 模式図（同じ・ずれの分だけ強さが下がる矢印）｜権利：自作',
               src='TR0222（`This deviation, while seemingly minor, significantly diminishes the strength`）'),
    'c909': dict(kind='図・写真の頁',
               plan='tf_p076_bars（印字は77）｜副題：NIST のスライド77（図面＝サーフサイド町）｜権利：A＋町の図面｜注：紙面の引用（頁ごと・額装・無加工・色を変えない・出典に「図面：Town of Surfside」）',
               src='TR0223・TR0226・TR0227・TF p77'),
    'c910': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0228（`only two bars in each direction passed over the columns, half the number required`）・TF p77（`only 2 rather than 4 top bars were centered over the column in each direction`）'),
    'c911': dict(kind='図解',
               plan='図 模式図【上から】鉄筋の間隔（図面の間隔 → 実際は約20から40%広い・柱のまわりの本数が減る）｜権利：自作',
               src='TR0224・TR0229（`about 20% to 40% wider than required by the structural design drawings`）・TR0230'),
    'c912': dict(kind='写真',
               plan='B5@102–109（倉庫の部材のあいだを歩く）｜副題：倉庫に並ぶ証拠（2023年）｜権利：A推定｜注：NIST のヘルメットに寄らない',
               src='TR0231（`Records of whether these changes were approved by the design engineer or observed by inspectors in the field are not available.`）'),
    'c913': dict(kind='図解',
               plan='図 数の比べ（原因の5つ：設計の強さの不足〈いちばん大きい・広い〉・図面とのずれ〈広い〉・重いプランター・足した砂と敷石・年月の傷み＝AC p.54 の形）｜権利：自作',
               src='AC p.54（`Design understrength (largest, pervasive)`）・TR0277〜0280'),
    'c914': dict(kind='図解',
               plan='図 数の比べ（同じ・5つを順に光らせる）｜権利：自作',
               src='AC p.54・TR0280'),
    'c915': dict(kind='写真',
               plan='N#42（吸水の試験）｜副題：コンクリートの吸水の試験（2024年8月）｜権利：A｜注：—',
               src='TR0280（`the most significant factor for which was likely corrosion of the reinforcement, exacerbated by porous concrete, concrete cracks that leaked, and ineffective waterproofing`）'),
    'c916': dict(kind='写真',
               plan='N#3（携帯の分析器で塩化物を測る）｜副題：塩化物を測る（2022年1月）｜権利：A｜注：縦横ほぼ同じ＝額装',
               src='TR0042（`The final factor that brought the critically low margins of safety to the point of failure was most likely long-term degradation from corrosion.`）・TR0280・MC18 p.7'),
    'c917': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='AC p.61（`Degradation was a comparatively small contributor to the strength and deformation capacity deficiencies responsible for the CTS failure.`）'),
    'c918': dict(kind='図解',
               plan='図 年表（1979〜81年 設計と建設＝赤い印「住む前から」 → 1981年 完成 → 2021年 崩落）｜権利：自作',
               src='TR0281（`caused the bulk of the critically low margins against failure from the time construction was complete`）'),
    'c919': dict(kind='図解',
               plan='図 年表（同じ）｜権利：自作',
               src='TR0278（`baked in before the building was even occupied`）'),
    'c920': dict(kind='写真',
               plan='B6@47–51.75（圧縮試験機の中のコア）｜副題：コンクリートのコアの試験（2024年）｜権利：A推定｜注：51.75 から顔の寄り＝until',
               src='TR0441・TR0281'),
    'c921': dict(kind='図解',
               plan='図 流れ図（40年の再認証＝傷みを見る → 建てたときの設計と工事は確かめない＝AC p.61 の1c）｜権利：自作',
               src='AC p.61（`The requirements for recertification of structures in Florida are laudable, but they contain no requirements for establishing confidence in the original design and construction.`）'),
    'c922': dict(kind='写真',
               plan='B5@39–46.5（コア抜きの刃と水）｜副題：コア抜き（2023年）｜権利：A推定｜注：絵が柔らかい（実効 約512px）＝別の秒も⑤b-1で',
               src='TR0472（`Problems in its pool deck structure stemming from the time of original design and construction`）'),
    'c923': dict(kind='写真',
               plan='C13（跡地と抜けた鉄筋）｜副題：崩落の跡地（2021年10月4日）｜権利：CC BY 2.0（Steve Jurvetson）｜注：色や切り出しを変えたら「改変」の表示',
               src='—（橋）'),
}

SPEC = {}
