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
               plan='I17｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：応急の救護所｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：後｜人：背中｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり（私人は背中だけ＝⑤b で原寸）｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
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
               plan='I27｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：事故のあとのプリピャチ｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜⑤b-2（10-22）：説明「Pripyat after the accident」・年は無い＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.24／472（`began at 14:00 and finished at 17:00`）'),
    'c709': dict(kind='写真',
               plan='I25｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：放射能の標識｜動き：額ごと上へ｜権利：CC BY-SA 2.0｜時期：後｜人：なし｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
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
               plan='I19｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：車の除染｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：遠景｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：台本どおり｜⑤b-2（10-22）：年は原文に無い（撮影日の欄は取り込みの日）＝外した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-22）：案C4 避難のバス＝置き場 N4（`tools/illu24.py`・門番 check_illu ㊶）
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c707（2行・7.6秒）＝1行目「夜のうちに、およそ1,200台のバスが手配された」＝夜の町の通りへバスの列が右から入る（両端の外まで続く＝数は描かない）／
    #   2行目「次の日、27日の正午ごろ、町に避難の知らせが流れる」＝昼になり知らせの輪（模式）→ 住民の顔の無い群れ（避難 14:00〜17:00＝L2 p24・c708 の語り）
    "c707": dict(fig=("illu", dict(
        place="N4", at="14:00",
        steps=[dict(state=dict(n4bus="on"),
                    rec="L2 p3024（During the night, arrangements were made for nearly 1,200 buses）",
                    tag=dict(t="バス 約1,200台（夜のうちに）", at="bus", off=(-40, -150), delay=2.4)),
               dict(state=dict(n4day="on", n4call="on", n4crowd="on"),
                    rec="L2 p3024（Around noon on 27 April the evacuation order was broadcast to the people・the evacuation began at 14:00 and finished at 17:00）",
                    tag=[dict(t="避難の知らせ（27日 正午ごろ）", at="town", off=(80, -60)),
                         dict(t="避難 14:00〜17:00", at="crowd", off=(40, -170), delay=2.6)])]))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-5（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。c713（日本の地図）は ⑤b-6
#   🔴 c706 の帯は26日の朝と22:00まで（27日の正午・14:00〜17:00 は c707 の再現イラストと c708 の語り＝ここに書かない）
#   🔴 c714＝札の型（相方 c206 の7枚の札と別＝掲示の紙と絵の札）。出典は国会会議録（REC_DOCS の外＝出典の行は手で書く・句は会議録の本文で門番が当てる）
# ══════════════════════════════════════════════════════════
from mech24 import rr  # noqa: E402

SPEC.update({
    # c701（3行）＝上から見た4号機とタービンの建屋。1行目は聞き役（建屋だけ）／2行目：燃える塊と火花が屋根へ・火の印／3行目：1986年のソ連の報告
    "c701": dict(
        t="発電所の火事", s="4号機のとなり",                # 🔧 門番 dup：「屋根に落ちた火」を札「屋根に落ち、火事に」が71%覆った
        fig=("m24", dict(view="roof", steps=[dict(), dict(state=dict(fall="on")), dict(state=dict(s86="on"))],
                         rel=[dict(t="4号機", src="S3 p2021")] + rr("s86"), note="建屋の配置と火の位置は模式", src=ss.src(["S3 p2021"])))),
    # c706（2行）＝26日の24時間の帯（時刻に比例）。1行目：朝・窓と戸を閉めた家／2行目：22:00 避難を決める
    "c706": dict(
        t="家の中で待った町", s="避難の決定",
        fig=("m24", dict(view="dayband", steps=[dict(state=dict(indoor="on")), dict(state=dict(decide="on"))],
                         rel=[dict(t="26日・27日", src="L2 p3024"), dict(t="22:00", src="L2 p3024")], note="帯は時刻に比例（家の位置は「朝」・家の絵は模式）",
                         src=ss.src(["S2 p1082", "L2 p3024"])))),
    # c714（3行）＝掲示の紙と絵の札。1行目：注意・5月4日 早朝・放射能対策本部／2行目：雨水をじかに飲むなら木炭でこす／3行目：水道水・井戸水・牛乳＝心配ない
    "c714": dict(
        t="国からの注意", s="5月4日の早朝",
        fig=("m24", dict(view="notice", steps=[dict(state=dict(head="on")), dict(state=dict(rain="on")), dict(state=dict(tap="on"))],
                         rel=[dict(t="5月4日", src="K1 19860507")], note="絵は模式（言葉は要約）",
                         src="国会会議録 1986-05-07 参議院 科学技術特別委員会 第6号"))),
})
