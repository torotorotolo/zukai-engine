# -*- coding: utf-8 -*-
"""第10章　304人 ca01–ca14（14カット）。14本目（セウォル号）。

■ 🔴 2026-09-28（⑤b-1）：13本目（トルコ航空981便）の中身を空にした＝git の `b54ee4f`（`git show b54ee4f:tools/cuts/ca.py`）。
  ⚠️ 第10〜13章（ca〜cd）は14本目で初めてのファイル（13本目までは9章）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep14/make_plan.py` で
  台本 §4・承認ずみの絵コンテ（映像方針 §2-2・§4）・追補 §4・§7 から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2〜⑤b-7 で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝⑤b-7 の門番 check_text_screens が「文字だけ2割まで・3カット以上続けない」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所（ルール §5b-79）
  記号＝【案C】再現イラスト（置き場 A〜E）・【F】断面F・【地図】drift・【年表】【帯】【棒】【マス】【人の形】【書類】【流れ】【並べ】（追補 §3）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    "ca01": dict(kind='写真',
               plan='台本の画：実写 映像 米海軍の捜索（2014年4月・DVIDS・PD）',
               src='海審 p1009・特調委 p3124・p3169・写真の記録（materials §3-1・§3-2）'),
    "ca02": dict(kind='写真',
               plan='台本の画：実写 #15 テントの前で簡易ベッドを組む兵士（2014年4月18日・韓国国防部・CC BY-SA 2.0・額装）',
               src='海審 p1061・p1062'),
    "ca03": dict(kind='写真',
               plan='台本の画：実写 #12 潜水員とゴムボート（2014年4月19日・CC BY-SA 2.0・額装）',
               src='海審 p1061・p1062'),
    "ca04": dict(kind='写真',
               plan='台本の画：実写 #6 韓国海軍の艦とゴムボート（2014年4月19日・CC BY-SA 2.0・額装）',
               src='海審 p1062'),
    "ca05": dict(kind='写真',
               plan='台本の画：実写 #8 荒れた海の潜水員（2014年4月20日・CC BY-SA 2.0・額装）',
               src='海審 p1062'),
    "ca06": dict(kind='写真',
               plan='台本の画：実写 #11 夕暮れのクレーンと沈んだ位置の浮標（2014年4月20日・CC BY-SA 2.0・額装）',
               src='海審 p1038・p1061・p1062'),
    "ca07": dict(kind='写真',
               plan='台本の画：実写 #13 夜の照明弾と潜水の艇（2014年4月20日・CC BY-SA 2.0・額装）',
               src='海審 p1055・p1061・p1062'),
    "ca08": dict(kind='図解',
               plan='【帯】沈んだあとの帯（追補 §4）',
               src='海審 p1060〜1061'),
    "ca09": dict(kind='写真',
               plan='台本の画：実写 #17 はしけから海へ入る潜水員（2014年5月4日・CC BY-SA 2.0・額装）',
               src='判決 p8・p18・p21〜22'),
    "ca10": dict(kind='写真',
               plan='台本の画：実写 #4 島を背に海を埋める捜索の船（2014年5月6日・CC BY-SA 2.0・額装）',
               src='—'),
    "ca11": dict(kind='写真',
               plan='台本の画：実写 映像 米海軍の航空機による捜索（2014年4月・PD）',
               src='—'),
    "ca12": dict(kind='写真',
               plan='台本の画：実写 #2 米海軍の艇と、はしけの幕（2014年5月4日・CC BY-SA 2.0・額装）',
               src='—'),
    "ca13": dict(kind='写真',
               plan='台本の画：実写 #19 水中の潜水員とボートの兵士（2014年5月4日・CC BY-SA 2.0・額装）',
               src='海審 p1091・特調委 p3169'),
    "ca14": dict(kind='写真',
               plan='台本の画：実写 #20 夜の海の照明弾と、明かりのはしけ（2014年5月1日・CC BY-SA 2.0・額装）',
               src='—'),
}

SPEC = {
    # ── 🔴 ⑤b-5（2026-09-29）：軸の型＝`tools/axis.py`（門番 check_axis）──
    # 沈んだ 10:31（海審 p1057）→ 特殊部隊 11:28（ヘリ＝p1061 注31）→ 救助隊 12:19（漁船＝p1060）
    "ca08": dict(
        t="沈んだあとの到着",
        s="ヘリと漁船で",
        fig=("axis", dict(view="clock", span=("10:20", "12:30"), ticks=("10:30", "11:00", "11:30", "12:00", "12:30"),
                          steps=[dict(add=dict(k="pt", at="10:31", t="沈む", rec="海審 p1057", c="ALERT"), cur="10:31"),
                                 dict(add=[dict(k="pt", at="11:28", t="特殊部隊", rec="海審 p1061"),
                                           dict(k="pt", at="12:19", t="救助隊", rec="海審 p1060"),
                                           dict(k="span", a="10:31", b="12:19", rec=["海審 p1057", "海審 p1060"], c="ALERT")],
                                      cur="12:19")],
                          note="時刻の帯：時刻は報告書", src=ss.src(["海審 p1057", "海審 p1060・p1061"]))),
    ),

    # ── 🔴 ⑤b-7a（2026-09-29）：捜索の写真11点と映像2本 ──
    # 写真＝韓国国防部の Flickr（Commons・CC BY-SA 2.0）＝**額装・無改変・1点1カット**（`ss.frame_only` が止める）。
    #   どれも4月18日以降＝「当日の救助」と名乗らない。日付＝Commons の撮影日（艦の名前は記録で確かめていない＝番号だけ）
    # 映像＝DVIDS（PD）。秒は `footage.USE`（ショットの中）・`ss.vid` はひかえの静止画つき（取れなければ黙って静止画＝⑥で数える）
    "ca01": ss.vid("ca01", t="捜索に向かうヘリ", s="2014年4月18日　強襲揚陸艦の甲板"),
    "ca02": dict(t="捜索の日々", s="4月18日　テントの前で簡易ベッドを組む兵士",
                 photo=P("search_tent_0418"), panel=True, color=1.0),
    "ca03": dict(t="潜水員を乗せたボート", s="4月19日　SSU のゴムボート",
                 photo=P("search_ssu_0419"), panel=True, color=1.0),
    "ca04": dict(t="艦とゴムボート", s="4月19日　艦番号21",
                 photo=P("search_ship21_0419"), panel=True, color=1.0),
    "ca05": dict(t="荒れた海", s="4月20日　高い波の中の潜水員",
                 photo=P("search_waves_0420"), panel=True, color=1.0),
    "ca06": dict(t="夜も続く作業", s="4月20日の夜　クレーンと大きな浮き",
                 photo=P("search_night_0420"), panel=True, color=1.0),
    "ca07": dict(t="照明弾の下で", s="4月20日の夜　SSU のボート",
                 photo=P("search_flare_0420"), panel=True, color=1.0),
    "ca09": dict(t="海へ入る潜水員", s="5月4日　送気式の潜水装備で",
                 photo=P("search_diver_0504"), panel=True, color=1.0),
    # 横長（3.51）＝額装でも横いっぱい。Commons の日時 05-06 01:31 は UTC の見込み（昼の写真）＝日付だけ
    "ca10": dict(t="沈んだ海域の船団", s="2014年5月6日",
                 photo=P("search_fleet_0506"), panel=True, color=1.0),
    "ca11": ss.vid("ca11", t="空から探す", s="2014年4月19日　ヘリの乗員と艦"),
    # 奥のはしけの幕「당신은 우리 아이들의 마지막 희망입니다」（語りが読む）。手前の艇＝米海軍の救難艦の乗員と韓国海軍の救助隊員（Flickr の説明）
    "ca12": dict(t="はしけの幕", s="5月4日　手前はアメリカ海軍と韓国海軍の隊員",
                 photo=P("search_banner_0504"), panel=True, color=1.0),
    "ca13": dict(t="水の中の潜水員", s="5月4日　海軍の潜水員とボート",
                 photo=P("search_divers_0504"), panel=True, color=1.0),
    "ca14": dict(t="夜の海", s="5月1日　照明弾と明かりのはしけ",
                 photo=P("search_flare_0501"), panel=True, color=1.0),
}
