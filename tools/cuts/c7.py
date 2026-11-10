# -*- coding: utf-8 -*-
"""第6章　最後の30メートル c701–c724（24カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/c7.py`）。
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
    'c701': dict(kind='写真',
               plan='🔧 D76-9｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：後ろの胴体の下の裂け〈NTSB の調査の写真〉｜動き：静止｜権利：同上｜時期：2009-01（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（構造の写真 写真9）｜注：△ 絵は ⑤b で原寸｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#76 写真9）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p39（`According to Airbus, the ditching certification criteria also assumed that engine power was available, that the descent rate was 3.5 feet per second (fps), and that the airplane landed longitudinal to any water swells`）'),
    'c702': dict(kind='写真',
               plan='R40｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）表2｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p40（`Pitch attitude (in °) 11 9.5 Airspeed (in knots) 118 125`…`Descent rate (in fps) 3.5 12.5`）'),
    'c703': dict(kind='図解',
               plan='🔧 地：GF1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：フラップ＝翼のうしろから出す板・ゆっくり飛べるようになる絵｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈翼のうしろの板〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p20（`At 1529:44, the first officer stated, “no relight,” and the captain replied, “ok let’s go put the flaps out, put the flaps out.”`）・報p198（`15:29:45.4 HOT-1 ok lets go put the flaps out`）・報p64（`At 1529:49, as the airplane was descending through 270 feet, the flap lever was moved to the CONF 2 position`）'),
    'c704': dict(kind='フリー素材',
               plan='X704｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：翼のうしろの板が出た旅客機の翼〈社名と機種は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p21（`at 1530:17, stated, “got flaps two, you want more?” The captain replied, “no, let’s stay at two,”`）・報p108（`The NTSB concludes that the captain’s decision to use flaps 2 for the ditching, based on his experience and perception of the situation, was reasonable`）'),
    'c705': dict(kind='図解',
               plan='🔧 地：GK2（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：速さの札＝いちばん遠くまで滑れる速さ・機体が示す下限の速さ・実際の速さの線｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈速さの計器〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p106（`FDR data indicated that the airplane was below green dot speed and at VLS or slightly less for most of the descent, and about 15 to 19 knots below VLS during the last 200 feet`）'),
    'c706': dict(kind='フリー素材',
               plan='X706｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：操縦室の速さの計器〈機種は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p106（`the captain stated during postaccident interviews that he thought that he had obtained green dot speed immediately after the bird strike`）・報p106（`maintained that speed until the airplane was configured for landing, and, after deploying the flaps, maintained a speed “safely above VLS,”`）・報p107（`The NTSB concludes the captain’s difficulty maintaining his intended airspeed during the final approach resulted, in part, from high workload, stress, and task saturation`）'),
    'c707': dict(kind='図解',
               plan='地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：警報の札＝遅すぎる警報より地面の警報が優先される・地面の警報は約85秒で15回｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p107（`the low-speed warning was inhibited by the GPWS warnings, so that the flight crew was not made aware of the low-speed state`）・報p20（`From 1529:14.9 to 1530:40.1, the two systems transmitted a total of 15 alerts`）'),
    'c708': dict(kind='写真',
               plan='R201｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録B｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p21（`and then asked the first officer, “got any ideas?” The first officer responded, “actually not.”`）'),
    'c709': dict(kind='図解',
               plan='🔧 地：GK1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：警報の札「地面、地面、機首を上げろ」｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈操縦室〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p21（`At 1530:24, the GPWS issued a “terrain, terrain” warning followed by “pull up,” which repeated to the end of the CVR recording`）・報p201（`["pull up" repeats until the end of the recording]`）'),
    'c710': dict(kind='フリー素材',
               plan='X710｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：操縦席の横の操縦の棒〈サイドスティック｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p65（`Starting at 1530:36, when the airplane was at a radio altitude of about 100 feet, the FDR recorded a progressive pull aft on the left sidestick`）・報p65（`At 1530:39, as the airplane descended through 50 feet, the sidestick moved aft more abruptly, reaching its aft limit (16°) at 1530:41`）'),
    'c711': dict(kind='図解',
               plan='🔧 地：GF1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：迎え角＝翼が空気に当たる角度の絵・角度が大きくなりすぎないよう機体が操縦をおさえる「迎え角の守り」｜注：—｜新しい画（映像方針）：🔧 地 衛星 → イメージ〈翼のうしろの板〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p65（`Airbus performed a simulation of the last 300 feet of the accident flight, which indicated that the airplane was performing as designed and was in alpha-protection mode from 150 feet to touchdown`）'),
    'c712': dict(kind='図解',
               plan='🔧 地：C31（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：帯｜副題：高さと守りの帯＝約45メートルから下で守りが働く・約30メートルから下で機首を上げる操縦の効きが弱まる｜注：—｜新しい画（映像方針）：🔧 模式 → 帯（高さの帯＝約45メートルと約30メートル）・地 衛星 → [31]＝模式の連続を切る｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p114（`airspeed in the last 150 feet of the descent was low enough to activate the alpha-protection mode`）・報p65（`was in alpha-protection mode from 150 feet to touchdown`）・報p65（`the flight control system attenuated the effect of the pilot’s airplane nose-up (ANU) sidestick inputs below 100 feet radio altitude`）'),
    'c713': dict(kind='図解',
               plan='🔧 地：C31（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：守りの両面の札＝いちばんの性能を出した・失速の心配なく引けた・その一方で機首を上げる効きを弱めた｜注：—｜新しい画（映像方針）：🔧 地 衛星 → [31]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p115（`the airplane did provide maximum performance for the weight and configuration at that time`）・報p115（`The flight envelope protections allowed the captain to pull full aft on the sidestick without the risk of stalling the airplane`）'),
    'c714': dict(kind='写真',
               plan='R202｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）付録B｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src="報p202（`HOT-1 we're gonna brace.`）・報p21（`The first officer was referring to the cabin emergency notification switch, which provides a signal to the cabin crewmembers indicating that an emergency has occurred`）"),
    'c715': dict(kind='図解',
               plan='🔧 地：C31（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：着水の姿＝機首9.5度・時速約230キロ・沈む速さ 毎秒約3.8メートル｜注：—｜新しい画（映像方針）：🔧 地 衛星 → [31]（着水の直後の機体）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p65（`the airplane touched down on the Hudson River at an airspeed of 125 KCAS with a pitch angle of 9.5°`）・報p65（`the airplane ditched with a descent rate of 12.5 fps`）'),
    'c716': dict(kind='図解',
               plan='🔧 地：C31（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：棒｜副題：沈む速さ＝前提 毎秒約1.1メートル・1549便 毎秒約3.8メートル｜注：—｜新しい画（映像方針）：🔧 地 衛星 → [31]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p95（`the airplane’s descent rate at the time it impacted the water was 12.5 fps, more than three times the descent rate of 3.5 fps assumed during ditching certification, resulting in external pressures on the aft fuselage`）'),
    'c717': dict(kind='写真',
               plan='🔧 C68｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：保管中のこの機体の底の壊れ｜動き：静止｜見た目の型：11-10 640px＝はがれた底の外板・骨組み｜権利：CC BY-SA 3.0｜時期：2011-02-25（EXIF＝博物館へ移す前の保管中）｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 3.0）・無加工｜注：BY-SA＝額装・無加工｜新しい画（映像方針）：🔧 副題「後ろの胴体の中〈2010年〉」→ 写っているもの（頁の説明＝着水で壊れた機体の底）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p40（`Average external pressure (in psi) 7.3 15.1 Maximum external pressure (in psi) 10.9 22.6`）・計（15.1÷7.3＝2.07・22.6÷10.9＝2.07）'),
    'c718': dict(kind='写真',
               plan='🔧 D49-42｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：床を突き破った梁〈NTSB の調査の写真〉｜動き：静止｜権利：同上｜時期：2009（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（生存の写真 写真42）｜注：② で見た（dk_049）｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#49 写真42）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p49（`The FR65 vertical beam had punctured through the cabin floor in front of the direct-view jumpseat`）・報p139（`Flight attendant B was injured by the frame 65 vertical beam after it punctured the cabin floor during impact`）'),
    'c719': dict(kind='図解',
               plan='🔧 地：C21（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：傷の札＝左のすね・長さ12センチ・深さ5センチ・手術で閉じた｜注：—｜新しい画（映像方針）：🔧 地 衛星 → [21]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p52（`Flight attendant B sustained a V-shaped, 12-centimeter-long 5-centimeter-deep laceration to her lower left leg that required surgery to close`）'),
    'c720': dict(kind='フリー素材',
               plan='X720｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：シミュレーターの装置の外観〈機種と社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p67（`a total of 14 runs were performed in the engineering simulator in which pilots attempted to touch down on the water within a target flightpath angle of -0.5°`…`In 11 of the 12 runs, the touchdown flightpath angle ranged between -1.5° and -3.6°`…`a -0.2° touchdown flightpath angle was achieved by an Airbus test pilot`）'),
    'c721': dict(kind='図解',
               plan='地：GM1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：所見の札＝前提をすべて満たすのは、ありえなくはないが見込みは低い｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p138（`During an actual ditching, it is possible but unlikely that pilots will be able to attain all of the Airbus ditching parameters because it is exceptionally difficult for pilots to meet such precise criteria when no engine power is available, and this difficulty contributed to the fuselage damage`）'),
    'c722': dict(kind='写真',
               plan='R140｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）推定原因｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p140（`the probable cause of this accident was the ingestion of large birds into each engine`）・報p140（`Contributing to the fuselage damage and resulting unavailability of the aft slide/rafts were (1) the Federal Aviation Administration’s approval of ditching certification without determining whether pilots could attain the ditching parameters without engine thrust`）'),
    'c723': dict(kind='図解',
               plan='🔧 地：C21（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：並べ｜副題：損傷に関わった3つの札＝認証・訓練と指針・速さ｜注：—｜新しい画（映像方針）：🔧 地 衛星 → [21]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p140（`(2) the lack of industry flight crew training and guidance on ditching techniques, and (3) the captain’s resulting difficulty maintaining his intended airspeed on final approach due to the task saturation resulting from the emergency situation`）・報p140（`approval of ditching certification without determining whether pilots could attain the ditching parameters without engine thrust`）・報p112（`contain very little guidance to pilots on flying techniques to use during a ditching`）'),
    'c724': dict(kind='写真',
               plan='🔧 D79-1｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：胴体の外板の壊れ〈NTSB の調査の写真〉｜動き：静止｜権利：同上｜時期：2009（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（構造の追記の写真 写真1）｜注：△ 絵は ⑤b で原寸｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#79 写真1＝外板の区画 16/17）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p124（`two slide/rafts on the accident airplane were unavailable because of water entry in the aft cabin`）・報p139（`significant aft fuselage breaching and subsequent water entry into the aft area of the airplane, which prevents the aft slide/rafts from being available for use during an evacuation`）'),
}

SPEC = {}
