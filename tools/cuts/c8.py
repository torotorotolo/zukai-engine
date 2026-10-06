# -*- coding: utf-8 -*-
"""第7章　プールデッキから c801–c820（20カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c8.py`）。
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
    'c801': dict(kind='図解',
               plan='図 模式図【横から】柱と床の板（床の重さの矢印が下・柱の矢印が上＝TR0062〜0064 の図の型）｜権利：自作',
               src='TR0062〜0064'),
    'c802': dict(kind='図解',
               plan='GIF（NIST の押し抜きせん断の動く図）｜副題：NIST のアニメーション｜権利：A｜注：🔁 台本は模式図。c801 の模式図の次',
               src='TR0065・TR0066'),
    'c803': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0070（`It is as though the column punches through the slab.`）・TR0021・TR0069・TR0071'),
    'c804': dict(kind='図解',
               plan='図 模式図（はさみで紙を切る絵 → 柱が床をずらして押し抜く絵・柱の頭にフックの形の鉄筋が残る）｜権利：自作',
               src='TR0072・TR0020・TR0021（用語の説明）'),
    'c805': dict(kind='図解',
               plan='図 模式図【上から】最初の2か所（K-13.1・L-13.1 の札・まわりの継ぎ目に色＝TR0095 の図の型）｜権利：自作',
               src='TR0023・TR0075・TR0067・TR0068・TR0015（`We examined two dozen possible scenarios for where and how the failure started.`）'),
    'c806': dict(kind='図解',
               plan='図 流れ図（3つの道具：コンピュータの模型・実物大の試験・ひびの理論）｜権利：自作',
               src='TR0257'),
    'c807': dict(kind='図解',
               plan='図 模式図【上から】コンピュータの模型（継ぎ目ごとの重さとたわみの色＝TR0258 の図の型）｜権利：自作',
               src='TR0258'),
    'c808': dict(kind='写真',
               plan='B8@129〜（ワシントン大学の区間・⑤b-1）｜副題：実物大の試験（ワシントン大学）｜権利：A推定（撮影者の記載なし）｜注：128秒の表題カードの後だけ。2:08 より前はミネソタ大学＝使わない',
               src='TR0260（`build and load-test to failure eight full-scale replicas`）・A06（`slab-column connection test at the University of Washington`）・TR0262（`built as faithfully as possible to replicate the conditions existing in CTS at the time of failure`）'),
    'c809': dict(kind='写真',
               plan='B8@188–198（真上から見た試験体の床・ワシントン大学）｜副題：試験体の床（ワシントン大学）｜権利：A推定｜注：梯子の商標 WERNER／LEANSAFE はもとから在る字',
               src='TR0261（`10 foot, 6 inches square`）・TR0263・§9'),
    'c810': dict(kind='写真',
               plan='B8@⑤b-1（129〜187・199〜207 のうち油圧ジャッキの見える秒＝188〜198 は c809）｜副題：試験体と油圧ジャッキ（ワシントン大学）｜権利：A推定｜注：🔁 台本の型 fb_c327（80〜88秒）はミネソタ大学＝使わない',
               src='TR0263（`loaded by eight hydraulic jacks arranged around the slab perimeter`）'),
    'c811': dict(kind='図・写真の頁',
               plan='tf_p084_salt（TF スライド84＝塩水の槽と電極）｜副題：NIST の技術的知見のスライド84｜権利：A｜注：🔁 台本の型 fb_c328（ミネソタ大学）→ スライド',
               src='TR0266・TR0267'),
    'c812': dict(kind='写真',
               plan='N#70（床の上面のひび・ワシントン大学）｜差し込み（tail）：2 N#66  4.1秒 N#66（床を切った断面の斜めのひび・1430x804＝額装）｜副題：試験のあとの床（ワシントン大学・2025年）｜権利：A｜注：—',
               src='TR0265・A06（`The cut reveals shear cracking and failure at the surface.`）'),
    'c813': dict(kind='写真',
               plan='N#69（わざと錆びさせた鉄筋の標本）｜副題：錆びさせた鉄筋の標本（ワシントン大学・2025年）｜権利：A｜注：—',
               src='TR0268・TR0448（`moderate corrosion can significantly reduce the capacity of connections`）'),
    'c814': dict(kind='図解',
               plan='図 模式図【横から】ひびの幅（柱のまわりの斜めのひび・幅が限界に届くと壊れる＝TR0271 の図の型）｜権利：自作',
               src='TR0269〜0272'),
    'c815': dict(kind='図解',
               plan='図 グラフ（青い線＝継ぎ目にかかる力・赤い線＝耐えられる限界・交わる所に印＝TR0273〜0276 の図の型）｜権利：自作',
               src='TR0272〜0276'),
    'c816': dict(kind='図解',
               plan='図 数の比べ（決まりどおりの継ぎ目＝赤い線が青い線のずっと上・大きな余裕）｜権利：自作',
               src='TR0073'),
    'c817': dict(kind='図解',
               plan='図 数の比べ（プールデッキの継ぎ目＝2本の線が重なる・余裕ゼロ）｜権利：自作',
               src='TR0074（`those margins against failure were zero at the time of failure`）'),
    'c818': dict(kind='写真',
               plan='N#61（床と柱の継ぎ目のせん断破壊）｜副題：実物大の試験で壊れた継ぎ目（ワシントン大学・2025年）｜権利：A｜注：—',
               src='TR0074・TR0474'),
    'c819': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0019（`In the case of Champlain Towers South, these margins against failure were too narrow from the start.`）'),
    'c820': dict(kind='写真',
               plan='B2@46–49.5（デッキの床面を歩く作業員・上から）｜副題：プールデッキの跡（崩落の後・2021年）｜権利：A推定｜注：顔は小さい（台帳）',
               src='—（橋）'),
}

SPEC = {}
