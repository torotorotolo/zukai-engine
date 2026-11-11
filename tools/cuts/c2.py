# -*- coding: utf-8 -*-
"""第1章　ラガーディア空港、滑走路4 c201–c217（17カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/c2.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep32/make_plan32.py` で
  映像方針の一覧（`ref/ep32/eizou_build/make_list32.py`＝了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep32/eizou_list32.md`＝⑤b は一覧に従う）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  🔴 額装・帯の写真は静止（`build_jiko.FRAME_STILL_EP` に ep32）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。
  🔴 写真は画面いっぱい・色は原本（`build_jiko.PHOTO_KEEP_EP` に ep32）・BY-SA は額装・紙面と調査の写真も額装。説明カットの地は写真を暗くするだけ（8:1・衛星と夜の写真は地にしない）。
  🔴 VTS（沿岸警備隊の監視カメラ）は等速・止めなし・頭から使う・同じ秒を2回使わない（区間は一覧の動きの欄＝make_list32 の門番）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  🔴 この回の線＝語りと画面に名前を出すのは機長と副操縦士だけ（初出 c203・c205）・客室乗務員・管制官・救助の人は立場だけ・乗客は名前なし・
     NTSB・FAA・議員・知事・監督・俳優は役職で・「犠牲」「死亡」は言わない・「208秒」は使わず「約3分半」・映画は c517〜c518・c520 だけ
     ＝図でも同じ（紙面・写真に名前の字が写る＝親が絵を見て切る・船の名も読ませない）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c201': dict(kind='図解',
               plan='SAT:ラガーディア空港｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：ラガーディア空港〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`The flight was en route to Charlotte Douglas International Airport (CLT), Charlotte, North Carolina`）'),
    'c202': dict(kind='写真',
               plan='C52｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：ラガーディア空港の出発の図〈FAA〉｜動き：静止｜見た目の型：11-10 640px＝出発の図と滑走路の図｜権利：PD（FAA）｜時期：2009-01-15（題）｜人：なし｜出典の行：図：FAA（public domain）／Wikimedia Commons｜注：379×612＝額装｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`The accident flight was the last flight of a 4-day trip sequence for the flight and cabin crewmembers`）・報p18（`This was the first trip sequence that the captain and first officer had been paired to fly together`）'),
    'c203': dict(kind='図解',
               plan='地：C50（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：機長の札＝名前・57歳・飛んだ時間 1万9,663時間・うち A320 4,765時間・顔は描かない｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p23（`The captain, age 57`）・報p24（`the captain had accumulated 19,663 total flight hours`…`4,765 hours of which were in A320 airplanes`）・ド#6p8（`Total A320 flying time 4,765 hours`）'),
    'c204': dict(kind='フリー素材',
               plan='X204｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：晴れた空を飛ぶ旅客機の遠景〈社名と機種は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p23（`was hired by Pacific Southwest Airlines on February 25, 1980`…`Before this, he flew McDonnell Douglas F-4 airplanes for the U.S. Air Force`）・報p23（`Pacific Southwest Airlines merged with USAir Group in 1988`）'),
    'c205': dict(kind='図解',
               plan='地：C50（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：副操縦士の札＝名前・49歳・飛んだ時間 1万5,643時間・A320 は37時間・A320 の資格 2008年12月31｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p25（`The first officer, age 49`…`the first officer had accumulated 15,643 total flight hours`…`The first officer had 37 hours in A320 airplanes`）'),
    'c206': dict(kind='フリー素材',
               plan='X206｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：旅客機の操縦室の計器〈機種は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p25（`The first officer received his initial A320 type rating on December 31, 2008`）・報p69（`because he had just completed training, he immediately recognized that the event was an ECAM exception`）'),
    'c207': dict(kind='図解',
               plan='地：C50（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：客室乗務員3人の札＝51・58・57歳・座る位置〈前に2人・後ろに1人〉・名前と顔は描かない｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p26（`Flight attendant A, age 51, was located at the aft-facing, forward jumpseat`…`Flight attendant B, age 58, was located at the forward-facing, “direct-view” jumpseat (aft, center aisle)`…`Flight attendant C, age 57, was located at the aft-facing, forward jumpseat`）・計（初めの訓練の年から2009年1月まで＝26年・38年・28年）'),
    'c208': dict(kind='写真',
               plan='🔧 C41｜一覧の種類：写真｜見せ方：全面｜副題：引き上げたあとの機体〈2009年1月〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝夜・はしけの上の機体・柵と街灯｜権利：CC BY 2.0｜時期：2009-01-18 17:48（EXIF・頁の説明＝引き上げたあと）・夜｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：夜の写真＝全面は可・地にしない｜新しい画（映像方針）：🔧 副題を写っているものに｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p27（`The airplane was configured with 12 first-class passenger seats; 138 economy-class passenger seats`）・報p18（`The 150 passengers, including a lap-held child`）'),
    'c209': dict(kind='図解',
               plan='🔧 地：C21（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：この機体の装備＝前と後ろの扉に、救命いかだを兼ねたすべり台が4つ・座席の下に救命胴衣｜注：—｜新しい画（映像方針）：🔧 地 [41]（夜）→ [21]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p53（`Each of these exits was equipped with a door-mounted, automatically inflating Type II slide/raft`）・報p55（`an EOW-equipped airplane must be equipped with a life vest for each airplane occupant`）'),
    'c210': dict(kind='図解',
               plan='🔧 地：C21（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：割合｜副題：75機のうち20機＝この装備の機｜注：—｜新しい画（映像方針）：🔧 地 [41]（夜）→ [21]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p54（`The accident airplane was 1 of 20 A320s equipped as an EOW airplane in the US Airways fleet of 75 A320s`）・報p55（`The accident flight was a non-EOW flight`）・報p54（`Non-EOW airplanes are not required to carry passenger life vests, slide/rafts, or survival kits`）'),
    'c211': dict(kind='フリー素材',
               plan='X211｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：雪の残る冬の街と晴れた空〈場所は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='ド#7p6（`It had been snowing earlier in the day`…`The weather cleared up and it was sunny`）・報p41（`The 1451 Central Park surface weather observation indicated the following: winds 290° at 8 kts, visibility 10 miles`…`temperature -6° C`）'),
    'c212': dict(kind='図解',
               plan='SAT:滑走路4｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：滑走路4〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：現在｜人：なし｜出典の行：同上｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`at 1524:54, the LGA air traffic control tower (ATCT) local controller cleared the flight for takeoff from runway 4`）'),
    'c213': dict(kind='図解',
               plan='地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：操縦の役＝操縦する人〈副操縦士〉と見守る人〈機長〉の2つの札｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`At this time, the first officer was the pilot flying (PF), and the captain was the pilot monitoring (PM)`）'),
    'c214': dict(kind='図解',
               plan='🔧 地：GS1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：帯｜副題：上昇の帯＝約210メートルで出発の管制へ・約4,600メートルまで上がる指示｜注：—｜新しい画（映像方針）：🔧 地 衛星（Google を暗く）→ イメージ〈冬の空〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`The captain contacted the departure controller at 1525:51, advising him that the airplane was at 700 feet`…`The controller then instructed the flight to climb to and maintain 15,000 feet`）'),
    'c215': dict(kind='フリー素材',
               plan='X215｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：雲の上へ上がる旅客機の遠景〈社名と機種は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p18（`the takeoff and initial portion of the climb were uneventful`）'),
    'c216': dict(kind='フリー素材',
               plan='X216｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：紙に包んだサンドイッチ〈店名なし〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p25（`because they had a quick turnaround at LGA, he purchased a sandwich to eat on the airplane after departure`）'),
    'c217': dict(kind='写真',
               plan='🔧 D101-1｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：エンジンのファンから試料を取る調査官〈NTSB の調査の写真〉｜動き：静止｜権利：同上｜時期：2009-01（凡例）｜人：調査官（後ろ姿・公的な任務）｜出典の行：写真：NTSB 公開ドケット DCA09MA026（野生動物の報告 写真1）｜注：② で見た（dk_068_101）｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#101 写真1）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p19（`at 1527:10.4, the captain stated, “birds.”`）・計（15:25:51 から 15:27:10 まで＝79秒）'),
}

SPEC = {}

# 🆕 ⑤b-3b（2026-11-10）：衛星写真（額装・静止・型は c1.py の同じ節）。c201＝G02 空港とマンハッタンの東（ズーム13・章の頭＝card_mix=0）・
#   c212＝G03 滑走路の寄り（ズーム14）＝離陸の向きの矢印（滑走路4 の端から滑走路22 の端へ＝FAA の端の座標）
SPEC.update({
    "c201": dict(
        **ss.sat("G02", steps=[
            [dict(k="pt", at="lga", c="INK_W", t="出発した空港", lab=(24, 10, "start"))]]),
        card_mix=0, t="市の中の空港", s="ニューヨーク市のクイーンズ〈現在の衛星写真〉"),   # 空港の名は章の札（ラガーディア空港、滑走路4）にある＝門番 dup
    "c212": dict(
        **ss.sat("G03", steps=[
            [dict(k="arrow", fr="lga04", to="lga22", c="INK_W", t="離陸の向き", u=0.8, lab=(-30, 0, "end"))]],   # 右は Google の「ラガーディア空港」の字（試し焼きの原寸）
            note="矢印は FAA の滑走路の端の座標から描いた向き"),
        t="飛び立った滑走路", s="滑走路4〈現在の衛星写真〉"),
})

# 🆕 ⑤b-4a（2026-11-10）：イメージの写真（Pexels＝`stock/`・git に入れない・焼くときに `footage.stock_photos` が取り直して md5 を照らす）＝
#   全面・ゆっくり寄る・見出しと副題なし・原色（31本目 ⑤b-3a の型）。窓＝(fx, fy, zoom) の2つ（`ss.mvz`）。中身は `sources32.psv` の title（640px と原寸で見た）
_X204, _X206, _X211, _X215, _X216 = (P(f"stock/{c}") for c in ("x204", "x206", "x211", "x215", "x216"))
SPEC.update({
    # c204＝真下から見た旅客機の影絵と2本の飛行機雲（印は写らない）
    "c204": dict(photo=_X204, **ss.mvz(_X204, (0.5, 0.48, 1.0), (0.5, 0.46, 1.12)), side="none", color=1.0, t="", s=""),
    # c206＝操縦室の計器（ピントの浅い寄り・画面の字は原寸でぼけて読めない）
    "c206": dict(photo=_X206, **ss.mvz(_X206, (0.55, 0.55, 1.0), (0.6, 0.58, 1.12)), side="none", color=1.0, t="", s=""),
    # c211＝雪をかぶった木と晴れた冬の空（語りは天気）
    "c211": dict(photo=_X211, **ss.mvz(_X211, (0.5, 0.5, 1.0), (0.5, 0.55, 1.1)), side="none", color=1.0, t="", s=""),
    # c215＝高い空を飛ぶ旅客機（真下から・遠い）＝機体の方へ寄る
    "c215": dict(photo=_X215, **ss.mvz(_X215, (0.48, 0.45, 1.0), (0.48, 0.44, 1.15)), side="none", color=1.0, t="", s=""),
    # c216＝紙に包んで紐でしばったサンドイッチ（店の名なし）
    "c216": dict(photo=_X216, **ss.mvz(_X216, (0.5, 0.5, 1.0), (0.55, 0.5, 1.1)), side="none", color=1.0, t="", s=""),
})

# 🆕 ⑤b-5（2026-11-11）：模式（`tools/mech32.py`＝札の型 FU と見え方の表 VIEWS）。地は写真を暗くするだけ（`ss.gr`・値は `ss.GROUND`＝check_ground --suggest）。
#   地の名は一覧の「地」の欄（PLAN の plan の頭）。図の中身は台本の画の欄と出典の欄の字の範囲だけ（mech32 の頭）
import mech32 as _m32  # noqa: E402
SPEC.update({
    "c203": _m32.fu_spec("c203", ss.gr("c50")),
    "c205": _m32.fu_spec("c205", ss.gr("c50")),
    "c207": _m32.zu_spec("c207", ss.gr("c50")),
    "c209": _m32.zu_spec("c209", ss.gr("c21")),
    "c213": _m32.fu_spec("c213", ss.gr("stock/gk1")),
})
# 🆕 ⑤b-6（2026-11-11）：型の図（割合・帯）＝mech32 の「⑤b-6」の節。地は一覧の「地」の欄
SPEC.update({
    "c210": _m32.zu_spec("c210", ss.gr("c21")),
    "c214": _m32.zu_spec("c214", ss.gr("stock/gs1")),
})

# 🆕 ⑤b-7（2026-11-11）：写真の束の残り（型は c1.py の同じ節）
_C52, _C41, _D101_1 = P("c52"), P("c41"), P("d101_1")
SPEC.update({
    # c202＝[52] FAA の出発の図（379×612＝縦長・小さい＝額装）
    #   🔧 試し焼き（Actions 43026909564）：既定のぼかしでは図の大きな字（MASPETH CLIMB・LGA）が見出しの後ろで読めた＝紙面と同じ強さ（PAGE_BLUR）
    "c202": dict(photo=_C52, panel=True, ptall=True, ground=dict(photo=_C52, blur=ss.PAGE_BLUR), color=1.0,
                 t="4日間の乗務", s="ラガーディア空港の出発の図〈FAA〉"),
    # c208＝[41] 夜・はしけの上の機体（EXIF 1月18日 17:48）＝機体へ寄る
    "c208": dict(photo=_C41, **ss.mv(_C41, "in", fx=0.4, fy=0.6), side="none", color=1.0,
                 t="機体と乗客", s="引き上げたあとの機体〈2009年1月〉"),
    # c217＝#101 写真1 エンジンのファンから試料を取る調査官（横顔の中景・公的な任務＝そのまま）
    "c217": dict(photo=_D101_1, panel=True, ptall=True, ground=dict(photo=_D101_1), color=1.0,
                 t="約80秒後", s="試料を取る調査官〈NTSB の調査の写真〉"),   # 🔧 一覧の副題は額（左の端 x736）にかかる＝縮めた（門番 fmove）
})
