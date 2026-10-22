# -*- coding: utf-8 -*-
"""第6章　3キロ先の町 c701–c717（17カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

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
    'c701': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見る向き：上から｜見た目の型：建屋の屋根（上から・火の印）｜合図：🔁 横から→上から（前の図 c617）｜注：🔧 1986年の4号炉-ウ → 図（夜の火事の写真は無い）｜新しい画（映像方針）：🔧 模式（燃える塊と火花がタービン建屋の屋根に落ちる＝屋根に火の印・「ソ連の報告の言い方」の札）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.21／17（`fell onto the roof of the machine room and started a fire`）'),
    'c702': dict(kind='写真',
               plan='🔧 MEMF｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：消防士たちの碑（チェルノブイリの町・2021年）｜動き：額ごと寄る｜権利：CC BY-SA 4.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：🔧 IAEA 02790013（片づけの屋根の作業）→ 消防士の碑（§0-5＝夜の屋根の火に片づけの写真を当てない）。02790013 は c818 へ｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.29／25（`Fire had broken out in over 30 places`）・S2 p.68／~63（`localized at 02:10 and 02:20 respectively`・`the fire was quenched at 05:00`）'),
    'c703': dict(kind='写真',
               plan='I17｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：応急の救護所（1986年）｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：背中｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（私人は背中だけ＝⑤b で原寸）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.43／39（`also suffered burns during their efforts to extinguish the fire`・`108 people had been hospitalized`・`a further 24 persons out of those examined were admitted to hospital`）'),
    'c704': dict(kind='写真',
               plan='C486｜一覧の種類：実写｜見せ方：全面｜副題：発電所の記念碑と新しい覆い（2017年）｜動き：寄る｜権利：CC BY 2.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 2.0｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L3 p.7／47（`Two workers died in the immediate aftermath`）・S3 p.43／39（`died from severe burns`・`one of those working at the damaged unit was not found`）'),
    'c705': dict(kind='写真',
               plan='🔧 P84:町｜一覧の種類：実写｜見せ方：全面｜副題：事故の2年前のプリピャチの町と発電所（1984年1月・アメリカの偵察衛星）｜動き：右へ（町から発電所へ）｜権利：Public domain｜時期：前｜人：なし｜出典の行：アメリカの偵察衛星の写真（USGS EarthExplorer・Public domain）｜注：🔧 IAEA 02790026 → 町と発電所が1枚に写る衛星写真（語り＝炉から3キロ）。02790026 は c221 へ｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.24／472（`the town of Pripyat, located just 3 km from the damaged reactor`・`49,360 persons`）'),
    'c706': dict(kind='図解',
               plan='一覧の種類：帯｜見た目の型：帯（避難までの時間）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.82／~77（`people were instructed to remain indoors with windows and doors shut`）・L2 p.24／472（`the decision to evacuate the residents of the town was taken at 22:00`）'),
    'c707': dict(kind='再現イラスト',
               plan='一覧の種類：案C4｜見た目の型：避難のバス（案C4）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.24／472（`nearly 1,200 buses`・`Around noon on 27 April the evacuation order was broadcast`）'),
    'c708': dict(kind='写真',
               plan='I27｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：事故のあとのプリピャチ（1986年）｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.24／472（`began at 14:00 and finished at 17:00`）'),
    'c709': dict(kind='写真',
               plan='I25｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：放射能の標識（1986年）｜動き：額ごと上へ｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.24／472（`Yanov (254 persons)`）・L2 p.24／472（`was carried out from 30 April through 3 May`）・L2 p.25／473（`were evacuated from 3 May through 7 May.`）・L2 p.14／462（`the 30-km-radius area surrounding the reactor`）'),
    'c710': dict(kind='写真',
               plan='U2｜一覧の種類：実写｜見せ方：額装（小さい）｜副題：事故から3日後の衛星写真（1986年4月29日・USGS）｜動き：額の中で寄る｜権利：PD｜時期：後｜人：なし｜出典の行：USGS（Public domain）｜注：台本どおり（1000×807＝小さい）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='U2（USGS「1986 Landsat 5 image Chernobyl after」）'),
    'c711': dict(kind='図・写真の頁',
               plan='🔧 U4F12｜一覧の種類：頁｜見せ方：頁｜副題：冷却池の熱の写真（USGS の報告の図12）｜動き：寄る（4月22日と29日へ）｜見た目の型：図の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：USGS（Public domain）｜注：🔧 U3（600×410＝小さい）→ 図12の頁。英字の日付に日本語の札を重ねる（PD）｜新しい画（映像方針）：🔧 頁（USGS Bulletin 1785 の図12＝1985年6月6日・1986年4月22日・4月29日・5月8日の4つ＝PD・日付は頁の画像で確かめた）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='U3・U4（USGS Bulletin 1785 の図12＝熱のバンドの4つの日）'),
    'c712': dict(kind='写真',
               plan='🔧 R1｜一覧の種類：実写｜見せ方：全面｜副題：オランダでの放射線の測定（1986年5月1日）｜動き：寄る｜権利：CC0｜時期：後｜人：顔｜出典の行：RIA Novosti archive（CC0）・撮影者は作者欄のとおり｜注：🔧 SPOT（衛星）→ オランダの測定（語り＝国境を越えた）。衛星写真が c710・c711 と3つ続かないように。§0-5＝日本の場面（c715）には当てない｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='K1 1986-05-15 参院 内閣委・今村治 室長（`スウェーデン、フィンランド等北欧諸国を中心にソ連の国境を越えて拡散し`）'),
    'c713': dict(kind='図解',
               plan='🔧 一覧の種類：地図｜見る向き：上から｜見た目の型：地図（日本・色を多く）｜注：§0-5｜新しい画（映像方針）：🔧 地図（日本＝東京・千葉・神奈川に印「5月3日」・「5月14日までに29の都道府県」は札だけ〈都道府県を塗らない〉・色を多く）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='K1 1986-05-07 参院 科学技術特別委・河野洋平 科学技術庁長官（`五月三日に至り、東京都、千葉県、神奈川県におきまして`）・K1 1986-05-15 参院 内閣委・今村治 室長（`二十九都道府県にわたり`）'),
    'c714': dict(kind='図解',
               plan='一覧の種類：札｜見た目の型：札（5月4日の注意）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='K1 1986-05-07 参院 科学技術特別委・河野洋平 科学技術庁長官（`直接雨水を摂取する場合はできるだけ木炭等でこして使用することが望ましい`・`水道水、井戸水及び牛乳については心配ない`）'),
    'c715': dict(kind='文字の頁',
               plan='🔧 K19860507｜一覧の種類：頁｜見せ方：頁｜副題：参議院 科学技術特別委員会の会議録（1986年5月7日）｜動き：寄る（答弁の行へ）｜見た目の型：文字の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：国会会議録 1986-05-07 参議院 科学技術特別委員会 第6号｜注：🔧 RIVM #01（オランダ）→ 語りが引く国の答弁の頁（§0-5＝オランダの写真を日本の場面に当てない）｜新しい画（映像方針）：🔧 頁（国会会議録の頁の画像）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='K1 1986-05-07 参院 科学技術特別委・河野洋平 科学技術庁長官（`念のため十分に洗浄して摂取することが望ましい`・`国民の健康に影響を与えるような放射能は検出されておらず`）'),
    'c716': dict(kind='写真',
               plan='I14｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：キエフの通りの除染（1986年5月1日）｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：遠景｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L3 p.43／83（`of streets in Kiev decreased the collective external dose`）'),
    'c717': dict(kind='写真',
               plan='I19｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：車の除染（1986年）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：遠景｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}
