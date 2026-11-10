# -*- coding: utf-8 -*-
"""第7章　冷たい川の上で c801–c822（22カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/c8.py`）。
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
    'c801': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：着水後の機体〈沿岸警備隊の監視カメラ〉｜動き：映像 186.00〜206.50秒｜見た目の型：11-10 原寸 185・206秒＝×19.2・尾翼と翼の上の人｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 区間 2分〜3分40秒 → 186.0秒から（カメラが落ち着いた 184〜207秒）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p57（`Within seconds after the ditching, the crewmembers and passengers initiated the evacuation of the airplane`）・報p58（`The captain and first officer assisted the flight attendants with the evacuation of the airplane`）'),
    'c802': dict(kind='図解',
               plan='地：C26（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：年表｜副題：扉が開いた順＝15:30:58 左の翼の非常口・15:31:06 前の左の扉・15:31:11 前の右の扉・15:31:｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p58（`1530:58 – left overwing exits opened, first passenger subsequently exited`…`1531:06 – door 1L opened`…`1531:11 – door 1R opened`）'),
    'c803': dict(kind='フリー素材',
               plan='X803｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：ふくらんだ救命いかだ〈社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p58（`she reported that the slide/raft did not inflate automatically when she opened the door. She stated that she pulled the manual inflation handle and that the slide/raft inflated`）・報p58（`about 20 seconds elapsed after flight attendant A opened door 1L and the slide/raft began to inflate`）・報p59（`one passenger jumped into water from door 1L`）'),
    'c804': dict(kind='図解',
               plan='地：C26（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：前の右の扉が閉まりかける絵と、扉を押さえる人の札〈顔は描かない〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p57（`she stated that door 1R started to close during the evacuation, intruding about 12 inches into the doorway and impinging on the slide/raft`）・報p57（`she assigned an “able-bodied” man to hold the door to keep it off of the slide/raft`）'),
    'c805': dict(kind='写真',
               plan='🔧 D49-21｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：後ろの左の扉〈NTSB の調査の写真〉｜動き：静止｜権利：同上｜時期：2009（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（生存の写真 写真21）｜注：△ 絵は ⑤b で原寸｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#49 写真21＝扉 2L とすべり台いかだ）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p58（`Door 2L was “cracked” open, but it was unclear by whom`）・報p139（`significant aft fuselage breaching and subsequent water entry into the aft area of the airplane`）'),
    'c806': dict(kind='写真',
               plan='🔧 C63｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：保管中のこの機体の座席｜動き：静止｜見た目の型：11-10 640px＝泥の跡の座席｜権利：CC BY-SA 3.0｜時期：2011-02-25（EXIF＝博物館へ移す前の保管中）｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 3.0）・無加工｜注：BY-SA＝額装・無加工｜新しい画（映像方針）：🔧 イメージ（座席の背）→ この機体の座席の写真（BY-SA・額装）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p58（`Flight attendant B stated that she began improvising commands and told “young, able-bodied” passengers to climb over the seats to get people away from the water`）'),
    'c807': dict(kind='図解',
               plan='地：C26（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：前へ向かう人の流れの矢印〈人は数えない形〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p58（`some of the passengers were bottle-necked at the overwing exits; therefore, the flight attendants called them forward`）・報p58（`Flight attendant B also exited from door 1R, at which time, she realized that her left leg was injured`）'),
    'c808': dict(kind='フリー素材',
               plan='X808｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：座席の下の救命胴衣の袋〈社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p58（`he and the first officer noted that a number of passengers had evacuated the airplane without life vests; therefore, they obtained some life vests from under the passenger seats in the cabin and passed them out to passengers outside of the airplane`）'),
    'c809': dict(kind='図解',
               plan='地：C26（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：客室を見て回る2人の札〈顔は描かない〉・前の左のすべり台へ｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p58（`following the evacuation, he and the first officer inspected the cabin to ensure that no more passengers or crewmembers were on board. Subsequently, the captain and first officer exited the airplane onto the 1L slide/raft`）'),
    'c810': dict(kind='図解',
               plan='地：C26（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：割合｜副題：前のすべり台 約64人・翼の上と翼のすべり台 約87人｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p124（`about 64 occupants were rescued from the forward slide/rafts, and about 87 occupants were rescued from the wings and off-wing ramp/slides`）・報p124（`the wings were very near to, if not at, standing capacity`）'),
    'c811': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：翼の上の人たち〈沿岸警備隊の監視カメラ〉｜動き：映像 210.00〜227.50秒｜見た目の型：11-10 原寸 209・227秒＝×26.9・尾翼と翼の上の人｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 引きの絵（約1分58秒）→ 寄りの絵（210秒〜）＝語り「腰まで水につかった」に翼の上の人・c801 と重ならない｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p120（`many of the passengers who evacuated onto the wings were exposed to water up to their waists within 2 minutes`）・報p127（`at least nine passengers unintentionally fell into the water from the wings`）'),
    'c812': dict(kind='写真',
               plan='🔧 C39｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：翼とすべり台〈2009年1月16日・沿岸警備隊〉｜動き：静止｜見た目の型：11-10 640px＝水に浮く翼・翼の上のふくらんだすべり台・奥に警察と沿岸警備隊の船｜印：△｜権利：PD（PD-USCG）｜時期：2009-01-16 11:31（EXIF＝11-10 の取得で確かめた）｜人：船の上の人（遠景）｜出典の行：写真：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：△ 翼のすべり台かは ⑤b で報告書の図と照らす（副題は「すべり台」まで）｜新しい画（映像方針）：🔧 模式（翼のすべり台の絵）→ 写真 [39]（PD）＝模式の連続を切る｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p53（`The off-wing ramp/slides did not have quick-release handles`）・報p53（`The off-wing ramp/slides were intended to be used in the event of a ground, not a water, evacuation`）'),
    'c813': dict(kind='図解',
               plan='🔧 地：C16（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：温度の札＝気温 マイナス7度〈15:51・セントラルパーク〉・水温 5.2度・風を受けた体の感じ方 約マイナス17度｜注：—｜新しい画（映像方針）：🔧 地 [26] → [16]（同じ地が続くのを減らす）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p41（`The 1551 observation indicated the following: winds 310° at 9 kts, visibility 10 miles, few clouds at 4,200 feet, temperature -7° C`）・報p41（`the water temperature of the Hudson River near the accident location about the time of the accident was 5.2° C (41.36° F)`）・報p120（`a 41° F water temperature and a 2° F wind chill factor`）'),
    'c814': dict(kind='写真',
               plan='C2｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：水につかっていく機体〈2009年1月15日・沿岸警備隊〉｜動き：静止｜見た目の型：11-10 640px＝消防艇と沈みかけの機体・右に沿岸警備隊の小舟｜権利：CC BY 2.0｜時期：2009-01-15（絵＝川の中ほどに浮かぶ機体と消防艇）｜人：乗り組みの人（遠景・小さい）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：822px＝額装｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p120（`Medical literature indicates that cold-water immersion causes cold shock, which can kill a person within 3 to 5 minutes, and swimming failure, which can kill a person within 5 to 30 minutes`）'),
    'c815': dict(kind='写真',
               plan='🔧 D49-54｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：座席の下の救命胴衣の袋〈NTSB の調査の写真〉｜動き：静止｜権利：同上｜時期：2009（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（生存の写真 写真54）｜注：△ 絵は ⑤b で原寸｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#49 写真54）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p61（`Two additional passengers retrieved and donned their life vests before impact`）・報p130（`two passengers realized that they would be landing in water and retrieved and donned their life vests before impact`）'),
    'c816': dict(kind='図解',
               plan='🔧 地：C16（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：表｜副題：救命胴衣と座席のクッション＝着水の前に着けた 2・座席の下から取り出した 10・人から渡された 21・クッションを持って｜注：—｜新しい画（映像方針）：🔧 地 [26] → [16]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p61（`5 passengers (3 percent) reported retrieving life vests from under their seats after impact`…`An additional 5 passengers (3 percent) reported retrieving a life vest from under a different seat after impact`）・報p61（`21 passengers (14 percent) reported being given a life vest`）・報p61（`77 passengers (53 percent) retrieved seat cushions during the evacuation`）'),
    'c817': dict(kind='フリー素材',
               plan='X817｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：救命胴衣の袋を開ける手〈社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p139（`Passenger behavior on the accident flight indicated that most passengers will not wait 7 to 8 seconds, the reported average life vest retrieval time, before abandoning the retrieval attempt and evacuating without a life vest`）・報p132（`confirm that many passengers may take at least 7 to 8 seconds to retrieve a life vest`）'),
    'c818': dict(kind='フリー素材',
               plan='X818｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：旅客機の座席の背の安全のしおり〈社名と字は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p55（`The CVR recorded flight attendant B orally brief the location and use of the flotation seat cushions; however, it did not record her brief the location of or the donning procedures for life vests`）・報p130（`the flight attendants were required by federal regulations to brief the passengers on their location and use`）・報p130（`a life vest demonstration was not required because the flight was not an EOW operation`）'),
    'c819': dict(kind='図解',
               plan='🔧 地：C16（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：札｜副題：安全の説明と、しおり＝実演をほとんど見た 25人・一部を見た 19人・しおりを読んだ 12人・聞き取りに答えた 146人｜注：—｜新しい画（映像方針）：🔧 地 [26] → [16]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p59（`The NTSB contacted 146 of the 150 passengers`）・報p61（`25 passengers (17 percent) reported watching most of the preflight safety demonstration`…`12 passengers (8 percent) reported reading the safety information card before or during the flight`）'),
    'c820': dict(kind='図解',
               plan='🔧 地：C16（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：前のすべり台が切り離されていかだになる絵＝1つ44人用｜注：—｜新しい画（映像方針）：🔧 地 [26] → [16]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p54（`Each slide/raft was rated to carry 44 passengers`）・報p124（`If the airplane had not been EOW equipped, the rafts that held those occupants would not have been available`）'),
    'c821': dict(kind='写真',
               plan='🔧 C16｜一覧の種類：写真｜見せ方：全面｜副題：機体のそばのフェリー〈2009年1月15日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2009-01-15（頁の説明）｜人：なし（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜新しい画（映像方針）：🔧 ⑤b-2：副題「機体に寄せたフェリー」→ 写っているもの（c105 と同じ＝門番 check_credits＝「寄せ」は作り手の言葉）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p139（`contributed to the lack of fatalities and the low number of serious cold-water immersion-related injuries because about 64 occupants used the forward slide/rafts after the ditching`）'),
    'c822': dict(kind='図解',
               plan='地：C16（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：川の上の機体と、近づく船の影〈数えない形〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（橋の1行）'),
}

SPEC = {}

# 🆕 ⑤b-3b（2026-11-10）：VTS（沿岸警備隊の監視カメラ・PD-USCG）＝額装（高さいっぱい・384 幅＝kind() が額装を返す＝panel を書かない）・等速・頭から。
#   区間は一覧の動きの欄＝`qa_out/ep32_assets.py use` が footage.USE に書く・ひかえの静止画＝`fb`（区間の頭のコマ）。型は c1.py の c101・c102
SPEC.update({
    # 副題は〈沿岸警備隊の監視カメラ〉の前を7字まで（額の左端 x738・副題は x72 から1字 32px＝門番 check_fmove）
    "c801": ss.vid("c801", ptall=True, t="避難の始まり", s="着水後の機体〈沿岸警備隊の監視カメラ〉"),
    "c811": ss.vid("c811", ptall=True, t="冷たい水", s="翼の上の人たち〈沿岸警備隊の監視カメラ〉"),
})
