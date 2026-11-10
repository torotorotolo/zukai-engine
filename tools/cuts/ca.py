# -*- coding: utf-8 -*-
"""第9章　報告書が書いた「偶然」 ca01–ca15（15カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/ca.py`）。
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
    'ca01': dict(kind='写真',
               plan='🔧 C40｜一覧の種類：写真｜見せ方：全面｜副題：夜の岸壁のそばの機体〈2009年1月17日〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝夜の照明の中の機体・奥の建物の明かり｜権利：CC BY 2.0｜時期：2009-01-17 00:07（EXIF）・夜｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜新しい画（映像方針）：🔧 副題「夕方の機体〈2009年1月15日〉」→ EXIF 1月17日 0:07＝夜｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='聞（州知事の会見＝報道の帰属・CNN の書き起こしは robots で拒否＝未読）'),
    'ca02': dict(kind='文字の頁',
               plan='R96｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`Consequently, this accident has been portrayed as a “successful” ditching. However, the investigation revealed that the success of this ditching mostly resulted from a series of fortuitous circumstances`）・計（報告書の文字の層で「miracle」0件）'),
    'ca03': dict(kind='フリー素材',
               plan='Xa03｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：冬の晴れた日の静かな川面〈場所は名乗らない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`including that the ditching occurred in good visibility conditions on calm water`）'),
    'ca04': dict(kind='図解',
               plan='地：GR2（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：偶然の札の1つ目と2つ目＝よい見通しと穏やかな水面・とても経験のある乗員｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`and was executed by a very experienced flight crew`）'),
    'ca05': dict(kind='文字の頁',
               plan='🔧 R140｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）推定原因｜注：枠＝「(1) the decision-making of the flight crewmembers and their crew resource management」から（c722 と別の枠）｜新しい画（映像方針）：🔧 模式（生き残れた理由の札・地＝夜の [40]）→ 報告書 p140 の「生き残れた理由」の段（実物）＝模式の連続を切る｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p140（`Contributing to the survivability of the accident was (1) the decision-making of the flight crewmembers and their crew resource management during the accident sequence`）'),
    'ca06': dict(kind='写真',
               plan='🔧 D49-56｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：すべり台を兼ねた救命いかだ〈NTSB の調査の写真〉｜動き：静止｜印：△｜権利：同上｜時期：2009（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（生存の写真 写真56）｜注：△ いかだの全体が写るかは ⑤b で原寸｜新しい画（映像方針）：🔧 [38]（c915 へ）→ #49 写真56（すべり台いかだ）＝語り「海の上の装備」｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`that the airplane was EOW equipped even though it was not required to be so equipped for this particular flight`）'),
    'ca07': dict(kind='写真',
               plan='🔧 VC｜一覧の種類：映像｜見せ方：額装（高さいっぱい）｜副題：機体に近づくフェリー〈沿岸警備隊の監視カメラ〉｜動き：映像 383.00〜395.00秒｜見た目の型：11-10 原寸 383・395秒＝×25.8・手前からもう1隻のフェリー・翼の上の人｜権利：PD（PD-USCG）｜時期：2009-01-15 15:30ごろ〜（🔴 焼き込みのカメラの時計は約20秒進む＝語りと副題に使わない）｜人：翼の上の人（遠景・顔は分からない）｜出典の行：映像：U.S. Coast Guard（public domain）／Wikimedia Commons｜注：—｜新しい画（映像方針）：🔧 模式（偶然の札の4つ目）→ VTS（語り「船の近くに降りた」）＝模式の連続を切る｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`and that the airplane was ditched near vessels immediately available to rescue the passengers and crewmembers`）'),
    'ca08': dict(kind='図解',
               plan='🔧 地：C36（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：生き残れた理由の4つの札＝乗員の判断と連携・海の上の装備があった偶然・客室乗務員の速い誘導・救助の人たちの近さと早さ｜注：—｜新しい画（映像方針）：🔧 地 [40]（夜）→ [36]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p140（`(2) the fortuitous use of an airplane that was equipped for an extended overwater flight`…`(3) the performance of the cabin crewmembers while expediting the evacuation of the airplane; and (4) the proximity of the emergency responders to the accident site and their immediate and appropriate response to the accident`）'),
    'ca09': dict(kind='フリー素材',
               plan='Xa09｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：操縦席から見た晴れた空〈機種と社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p137（`The professionalism of the flight crewmembers and their excellent crew resource management during the accident sequence contributed to their ability to maintain control of the airplane`）'),
    'ca10': dict(kind='図解',
               plan='🔧 地：C36（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：所見の札＝川を選んだ判断〈所見15〉・APU を先に回した〈所見14〉・フラップ2 は妥当〈所見18〉｜注：—｜新しい画（映像方針）：🔧 地 [40]（夜）→ [36]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p137（`The captain’s decision to ditch on the Hudson River rather than attempting to land at an airport provided the highest probability`）・報p137（`the captain started the auxiliary power unit, which improved the outcome of the ditching`）・報p105（`Starting the APU early in the accident sequence proved to be critical`）・報p137（`The captain’s decision to use flaps 2 for the ditching, based on his experience and perception of the situation, was reasonable`）'),
    'ca11': dict(kind='写真',
               plan='🔧 C57｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：保管中の機体を調べる人〈2010年・ニュージャージー州〉｜動き：静止｜見た目の型：11-10 640px＝天幕の中の胴体と外した翼・技術者の後ろ姿｜権利：CC BY-SA 3.0｜時期：2010（題・頁の説明＝ニュージャージー州での保管）｜人：技術者（後ろ姿・中景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 3.0）・無加工｜注：BY-SA＝額装・無加工｜新しい画（映像方針）：🔧 [12]（夜の岸壁で話す3人＝作業でない・顔が主役）→ [57]（語り「改めるべき所」）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p96（`The investigation revealed several areas where safety improvements are needed`）・報p96（`engine bird-ingestion certification testing, emergency and abnormal checklist design, dual-engine failure and ditching training`）・報p96（`validation of operational procedures and requirements for airplane ditching certification`）・報p96（`life vest stowage, retrieval, and donning`）'),
    'ca12': dict(kind='図解',
               plan='🔧 地：C36（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：委員の意見の札＝時間がほとんど無かった｜注：—｜新しい画（映像方針）：🔧 地 [12]（夜）→ [36]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p146（`In the case of US Airways 1549, there was insufficient time for much of anything`）・報p146（`defy the NTSB’s own criteria for use of the term. Those criteria state that a ditching allows “some time” for preparation`）'),
    'ca13': dict(kind='フリー素材',
               plan='Xa13｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：救命胴衣〈社名は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p146（`had more time existed, and had the occupants been made aware of the impending water landing, many more – if not all - would have located and donned the life preservers`）'),
    'ca14': dict(kind='図解',
               plan='🔧 地：C18（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：偶然の4つの札を並べ、その下に「次も重なるとは限らない」の札｜注：—｜新しい画（映像方針）：🔧 地 [40]（夜）→ [18]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（3つ目の問いの答えの前半）'),
    'ca15': dict(kind='文字の頁',
               plan='🔧 R141｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD｜時期：2010｜人：なし｜出典の行：出典：NTSB「NTSB/AAR-10/03」（2010）勧告｜注：枠＝見出し「Recommendations」と最初の段（c627 と別の枠）｜新しい画（映像方針）：🔧 [11]（夜の作業＝cb04 の [9] と似た写真）→ 報告書の勧告の頁の頭（語り「残りの半分は、勧告にある」）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（橋の1行）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-11-10）：紙面（型は c1.py の同じ節）
_Ra02, _Ra05, _Ra15 = P("r96_ca02"), P("r140_ca05"), P("r141_ca15")
SPEC.update({
    # ca02＝報告書 p96 の段（「a series of fortuitous circumstances」を含む）。1497×510＝幅いっぱい
    "ca02": dict(photo=_Ra02, panel=True, pw=1776, ground=dict(photo=_Ra02, blur=ss.PAGE_BLUR), color=1.0,
                 t="一連の偶然", s="報告書の分析の段"),
    # ca05＝報告書 p140 の「Contributing to the survivability…」の段（c722 と別の枠）。1497×384＝幅いっぱい
    "ca05": dict(photo=_Ra05, panel=True, pw=1776, ground=dict(photo=_Ra05, blur=ss.PAGE_BLUR), color=1.0,
                 t="生き残れた理由", s="報告書の結論の段"),
    # ca15＝報告書 p141 の見出し「4. Safety Recommendations」と最初の段（c627 と別の枠）。1497×432＝幅いっぱい
    "ca15": dict(photo=_Ra15, panel=True, pw=1776, ground=dict(photo=_Ra15, blur=ss.PAGE_BLUR), color=1.0,
                 t="勧告", s="報告書の勧告の頁の頭"),
})
