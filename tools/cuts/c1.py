# -*- coding: utf-8 -*-
"""つかみ c101–c107（7カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

■ 🆕 2026-10-22（⑤b-1）：新しいファイル。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep24/make_plan24.py` で
  映像方針の一覧 `ref/ep24/eizou_build/list24.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep24/eizou_list24.md`）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  ⚠️ 「関連（参考＝…）」と書いたカットは同じ型のほかの発電所の炉の写真（種類は写真・20% の数〈この発電所・この事故の写真〉には入れない・
     門番 check_text_screens が束の台帳 assets.json の related と照らす）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c101': dict(kind='フリー素材',
               plan='X13188726｜映像の素材 25.05秒・倍率 3.00（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のチェルノブイリ原発（Pexels）｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：台本どおり。森の向こうの地平線に新しい覆い（②③ の見本帳）。⑤b で使う区間を焼いて字と人を見る｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='K1 1986-05-07 参院 科学技術特別委・河野洋平 科学技術庁長官（`五月三日に至り、東京都、千葉県、神奈川県におきまして`）・K1 1986-05-08 衆院 農林水産委・今村治 室長（`五月三日以降採取した浮遊じん、雨水等の核種分析の結果`）'),
    'c102': dict(kind='写真',
               plan='U1｜一覧の種類：実写｜見せ方：全面｜副題：事故の前（4月22日）と後（4月29日）の衛星写真（USGS）｜動き：寄る（2枚を重ねて切り替える）｜権利：PD｜時期：前｜人：なし｜出典の行：USGS（Public domain）｜注：台本どおり。PD＝全面で寄る｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='U1（USGS「Landsat Chernobyl」）・S3 p.21／17（`at about 1:24 there occurred two explosions one after the other`）'),
    'c103': dict(kind='写真',
               plan='I15｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：壊れた4号炉（1986年4月）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり。Commons の大きい版（1328×2040）。撮影日は Flickr「翌日にヘリから」と Commons「4月26日」が割れる＝副題は「4月」まで｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src="S2 p.18／~13（`the accident was eaused by a remarkable range of human errors`・`in combination with specific reactor features which compounded and amplified the effects of the errors`）・S2 p.112／~105（`is to be found in the so-called 'human element'`）"),
    'c104': dict(kind='文字の頁',
               plan='S1p34｜一覧の種類：頁｜見せ方：頁｜副題：1992年の報告（INSAG-7）の結論の頁｜動き：寄る（「違反ではなかった」の行へ）｜見た目の型：文字の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：INSAG-7（IAEA 1992）｜注：台本どおり＝語りが名指しする所｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`were in fact not violations`）'),
    'c105': dict(kind='写真',
               plan='I36｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：壊れた4号炉とヘリコプター（1986年）｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1-付属書I p.53／43（`during the physical startup of Ignalina Unit 1 and that of Chernobyl Unit 4`・`almost two-and-a-half years before the Chernobyl accident`）'),
    'c106': dict(kind='写真',
               plan='I24｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：壊れた4号機と排気筒（1986年）｜動き：額ごと上へ｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（人は写らない＝責める行でも可）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.34／24（`critical actions of the operators were most ill judged`）'),
    'c107': dict(kind='フリー素材',
               plan='X13188720｜映像の素材 7.89秒・倍率 1.19（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のプリピャチ（Pexels）｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：台本どおり → 第1章の扉（頭の c201 が BY-SA＝扉は方眼だけ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S1 p.33／23（`It is not known for certain what started the power excursion`）'),
}

SPEC = {}
