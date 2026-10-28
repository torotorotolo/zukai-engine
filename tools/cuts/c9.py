# -*- coding: utf-8 -*-
"""第8章　80年後の調べ直し c901–c944（44カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c9.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep26/make_plan26.py` で
  映像方針の一覧 `ref/ep26/eizou_build/list26.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep26/eizou_list26.md`）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  🔴 額装・帯の写真は静止（26本目から＝`build_jiko.FRAME_STILL`）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  ⚠️ 人＝乗員・ほかの船の船長と航海士と通信士・審問の長は名前＋役職／会社の人とドンキーマンは役職だけ／乗客は名前なし（①・承認①）。
     名前の載る紙面・頁は注の「…外」のとおり寄る範囲から名前を外す
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c901': dict(kind='写真',
               plan='N04:E｜映像の素材 10.90秒・倍率 1.02（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（100.0〜110.9秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：台本どおり（区間＝前甲板の巻き上げ機と錨の鎖）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.1（`in the mid-1950's the book`…`it was widely read and a successful film based upon it was made. The allegations against CALIFORNIAN were repeated`）"),
    'c902': dict(kind='図解',
               plan='一覧の種類：年表｜見る向き：時間の線｜見た目の型：1912年→1950年代→訴えと請願→1985年→1990年→1992年の年表｜新しい画（映像方針）：台本どおり（請願の年は書かない・船長の亡くなった年は入れない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.1（`this led Captain Lord, by then over 80 years old, to renew his plea for the matter to be re-examined`…`the body representing British shipmasters. In particular, two petitions were made to the Board of Trade asking for the Inquiry to be re-opened; both were rejected`）'),
    'c903': dict(kind='写真',
               plan='S11-910:全体｜一覧の種類：実写｜見せ方：全面｜副題：海の底のタイタニック号の残骸〈2003年・NOAA ほか〉｜動き：下へ（垂れ下がる錆に沿って）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Image courtesy of ［撮影者］, RMS Titanic Expedition 2003, NOAA-OE.（撮影者の名は ⑤b で src/credits_private.tsv）｜新しい画（映像方針）：台本どおり（副題を写っている物に＝c826 と分ける）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.2（`In 1985 an expedition`…`discovered the wreck of TITANIC, in a position some 13 miles from that accepted by the 1912 Inquiry`）・N1（NOAA 2003 の頁＝深さ「3,800 m」・web）'),
    'c904': dict(kind='文字の頁',
               plan='🔧 P-G2-01｜一覧の種類：頁｜見せ方：頁（引用・額装）｜副題：海難調査局の報告書の表紙〈1992年〉｜動き：静止｜見た目の型：文字の頁｜権利：引用（OGL v3.0 か Crown copyright か未確定）｜時期：文書｜人：なし｜出典の行：出典：英国運輸省 海難調査局『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』（1992年）より引用｜新しい画（映像方針）：🔧 引用の型＝無加工の額装・静止（MAIB の権利が未確定＝sources.md §1）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.2（`in 1990 the Secretary of State for Transport`…`determined that the Marine Accident Investigation Branch should make a reappraisal of the relevant evidence`）'),
    'c905': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：調べ直しの4つの問いの札｜合図：🔁 時間の線→正面（前の図 c902）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.3（`To establish so far as is now possible the positions of TITANIC`…`To consider whether TITANIC was seen by CALIFORNIAN`…`To consider whether distress signals from TITANIC were seen by`…`To assess the action taken by Captain Stanley Lord`）'),
    'c906': dict(kind='文字の頁',
               plan='🔧 P-G2-03:同意の行｜一覧の種類：頁｜見せ方：頁（引用・額装）｜副題：海難調査局の報告書の送り状〈1992年〉｜動き：静止｜見た目の型：文字の頁｜権利：引用（OGL v3.0 か Crown copyright か未確定）｜時期：文書｜人：なし｜出典の行：出典：英国運輸省 海難調査局『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』（1992年）より引用｜注：⚠️ 署名（首席の名前）は切り出しの外｜新しい画（映像方針）：🔧 寄る → 静止の切り出し（「I do not fully agree」と「I full endorse」の行・引用の型）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 送り状（`an Inspector from outside the Branch was appointed`…`had recently retired from a post as Principal Nautical Surveyor`…`is a very experienced Master Mariner`）'),
    'c907': dict(kind='写真',
               plan='N04:D｜映像の素材 8.10秒・倍率 1.01（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（87.5〜95.6秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：台本どおり（区間＝甲板の縁の手すり）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 送り状（`I do not fully agree with all the Inspector's findings but this does not mean that I have any doubt`…`the thoroughness of his enquiries`…`I instructed the Deputy Chief Inspector of Marine Accidents to undertake this and report to me`）"),
    'c908': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：1冊の中の調査官の結論と次長の結論・首席の「次長を支持」の札｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 送り状（`His report, which follows, incorporates his conclusions and those of the appointed Inspector`…`full endorse the Deputy Chief Inspector's report and conclusions`）"),
    'c909': dict(kind='図解',
               plan='🔧 GS-titanic｜一覧の種類：衛星｜見せ方：衛星（帰属の行）｜動き：寄る（広い図から事故の海域へ）｜見る向き：上から｜見た目の型：タイタニック号のぶつかった位置・沈んだ位置・1912年の無線の位置（衛星写真・外洋）｜合図：🔁 正面→上から（前の図 c908）｜権利：Google の地図の利用（帰属の行を出し続ける）｜時期：今｜人：なし｜出典の行：Google の地図（衛星写真）＋描き足し｜注：カリフォルニアン号の印はまだ置かない｜新しい画（映像方針）：🔧 図の地図 → 衛星写真＋描き足し（了承②の2択）・Annex 3 の配置にならう｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.3（`when she foundered`）・G2 p.9（`caused by the wrong distance being allowed along the course line from the last known position - a simple mistake to make under stress`）'),
    'c910': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：北から来る冷たい海流が南へ張り出す矢印（時速約2.4キロ）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.9（`There is no doubt that in 1912 the Labrador current extended further south and east than is usual`…`the direction of set was about 196`…`and the rate about 1.3 knots`）'),
    'c911': dict(kind='図解',
               plan='🔧 一覧の種類：続き｜見た目の型：（c910 の続き）｜新しい画（映像方針）：🔧 イメージ（氷山の写真）→ c910 の図の続き（聞き役の1行だけのカット＝台本 §0-5）・「2人とも同じ」の札を足す｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.9（`Labrador current extended further south and east than is usual`）'),
    'c912': dict(kind='図解',
               plan='一覧の種類：対照｜見る向き：正面｜見た目の型：調査官と次長の距離の2列（約9〜19キロ・約31〜37キロ）｜合図：🔁 上から→正面（前の図 c910）｜新しい画（映像方針）：台本どおり（どちらにも帰属の札）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.7（`the Inspector has found that the two ships were between 5 and 10 miles apart whilst they lay stopped, and probably nearer five; whereas in my opinion the distance was substantially greater, probably about 18 miles`）'),
    'c913': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：14日の昼から南へ流された船の線（計算の位置より南）｜合図：🔁 正面→上から（前の図 c912）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.9（`He considers that the current had set southerly since noon on 14 April; no allowance for this current was made`）・G2 p.3（`but was probably further East and only 5 to 7 miles off`）'),
    'c914': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見る向き：横から｜見た目の型：北極星の高さの角度＝緯度（夜7時半の観測）｜合図：🔁 上から→横から（前の図 c913）｜新しい画（映像方針）：🔧 S8-630 の3回目 → 北極星の観測の模式（台本 §0-5 の候補）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.10（`The Pole Star sight taken by the Chief Officer at 1930 hrs (and confirmed by him in Court) gave the same latitude`…`as that observed at noon on the same day, showing a course made good of west`）'),
    'c915': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：アンティリアン号への電報（夜6時半の位置と大きな氷山3つ・西へ進む線）｜合図：🔁 横から→上から（前の図 c914）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.10（`The one piece of evidence on CALIFORNIAN'S track which cannot have been fabricated is the signal sent to ANTILLIAN concerning the sighting of icebergs`…`it adds weight to the statement that CALIFORNIAN was steering westerly`）"),
    'c916': dict(kind='写真',
               plan='🔧 S3-753:顔｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：カルパチア号の船長アーサー・ロストロン〈1912年〉｜動き：静止｜権利：PD｜時期：後・NY｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：緑の灯の向きは c710 の模式で見せてある｜新しい画（映像方針）：🔧 3回目 → 2回目（c504 を船の写真に替えた）・額の中の寄りを替える（静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.10（`the boat which it came from must have been to the north of CARPATHIA's course line and it follows that during the two hours the ship must have been set to the north`）"),
    'c917': dict(kind='図解',
               plan='🔧 GS-californian｜一覧の種類：衛星｜見せ方：衛星（帰属の行）｜動き：寄る｜見る向き：上から｜見た目の型：カリフォルニアン号の位置の2つの見方（調査官・次長の別々の点・衛星写真・外洋）｜権利：Google の地図の利用（帰属の行を出し続ける）｜時期：今｜人：なし｜出典の行：Google の地図（衛星写真）＋描き足し｜注：どちらにも帰属の札・見えたかの線は描かない｜新しい画（映像方針）：🔧 図の地図 → 衛星写真＋描き足し（了承②の2択）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.11（`I do not believe that CALIFORNIAN will have been affected by the southerly set for more than at the most a few hours before she reached the ice field and stopped`…`I therefore consider that CALIFORNIAN was between 17 and 20 miles from TITANIC at the time of collision, bearing about NW by N from her`）・G2 p.3（`most likely about 18 miles`）'),
    'c918': dict(kind='写真',
               plan='N04:I1｜映像の素材 10.60秒・倍率 1.01（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（185.0〜195.6秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：台本どおり（区間＝甲板の構造物）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.13（`CALIFORNIAN'S lights`…`could certainly be seen on a night such as this at 5 miles or more range`）・G2 p.13（`she was well beyond the ordinary visible horizon`）"),
    'c919': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：地球の丸みと水平線に隠れる遠い船の灯り・見張りの目の高さ｜合図：🔁 上から→横から（前の図 c917）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.13（`well beyond the ordinary visible horizon`）・G2 p.11（`our respective opinions on position are undoubtedly coloured by this difference`）'),
    'c920': dict(kind='写真',
               plan='🔧 S1-089:船体｜一覧の種類：実写｜見せ方：全面｜副題：試運転の日のタイタニック号〈1912年4月2日〉｜動き：右へ（船体に沿って）｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S1-050（真横の全身）は 10-27 に原寸で見たが、1920px の版では A 甲板の前半の窓でオリンピック号と見分けきれず・出どころも弱い＝使わない（来歴で確かな試運転の日の写真に替えた）｜新しい画（映像方針）：🔧 S3-675 の6回目 → タイタニック号の全身（語り＝タイタニック号の姿が見えていたか）・c212 と別の寄り｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.12（`The Inspector considers that TITANIC was seen by CALIFORNIAN and indeed kept under observation from 2300 hrs or soon after on 14 April until she sank`…`the extent of coincidence between what they saw and what is known of TITANIC'S movements`…`which does not coincide with`…`strongly in favour of TITANIC having been the ship seen`）"),
    'c921': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：タイタニック号の船橋と見張り台・0時30分ごろまでほかの船の灯は見えない｜新しい画（映像方針）：台本どおり（札は「タイタニック号の時計」）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.12（`no ship was seen by TITANIC until well after the collision; the exact time is not recorded but seems to have been about 0030 hrs`…`watch was maintained with officers on the Bridge and seamen in the`…`which if review were to be confined to`…`I would not dissent from`）'),
    'c922': dict(kind='写真',
               plan='S2-033:見張り台｜一覧の種類：実写｜見せ方：全面｜副題：船橋と見張り台〈1912年4月10日〉｜動き：寄る（見張り台へ）｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（2回目・c217 と別の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.12（`It is in my view inconceivable that CALIFORNIAN or any other ship was within the visible horizon of TITANIC during that period; it equally follows that TITANIC cannot have been within CALIFORNIAN'S horizon`）"),
    'c923': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：第三の船（東から来て氷原で止まり、すき間を探して去る・形は描き分けない）｜合図：🔁 横から→上から（前の図 c921）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.13（`a third ship was present which approached from the East, stopped on meeting the field ice, and then after a period steamed away to seek a break in the ice`）'),
    'c924': dict(kind='写真',
               plan='🔧 S8-N05:桟橋｜一覧の種類：実写｜見せ方：全面｜副題：ニューヨークのホワイト・スター・ラインの桟橋〈1905年ごろの絵はがき〉｜動き：右へ｜権利：PD｜時期：別の年｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：🆕 了承②。✅ 10-27 何の絵か確かめた＝着色の絵はがき（Detroit Publishing・1905年）・桟橋の大型客船と船・馬車。下の題と「COPYRIGHT, 1905」の字・台紙の余白は切り出しの外（色は絵はがきの原本のまま）｜新しい画（映像方針）：🔧 S10-905 の3回目 → 1905年ごろの桟橋の船（語り＝1912年の北大西洋は船の行き来が多かった）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.13（`This is very far from unlikely; the North Atlantic trade was busy in 1912 and a number of other ships are known to have been in the area`）'),
    'c925': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：異常屈折（冷たい海の上の空気の層で光が曲がる）｜合図：🔁 上から→横から（前の図 c923）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.13（`is that CALIFORNIAN did actually see TITANIC but at a very much greater range than her horizon because of abnormal`）・G2 p.26（Annex 4＝異常屈折の説明の写し）'),
    'c926': dict(kind='写真',
               plan='N04:I2｜映像の素材 10.00秒・倍率 1.02（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（225.0〜235.0秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：台本どおり（区間＝甲板の構造物の別の所）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.13（`the rockets seen by CALIFORNIAN were described as low-lying`…`this could be because they actually rose to a height above the refracting layer`…`it requires a long period during which CALIFORNIAN could see TITANIC but not vice versa`…`This is not`…`impossible`）'),
    'c927': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：舷灯の色と向き（最初は緑・のちに赤＝止まってから向きを変えた船）｜合図：🔁 横から→上から（前の図 c925）｜新しい画（映像方針）：台本どおり（c607 の模式と別の絵＝向きの変わる船）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.13（`later her red (port) light came into view, arguing that after stopping she swung markedly to starboard`…`Her port sidelight would therefore not be seen`）'),
    'c928': dict(kind='図解',
               plan='一覧の種類：対照｜見る向き：正面｜見た目の型：「タイタニック号は見えたか」の2列（調査官・次長）｜合図：🔁 上から→正面（前の図 c927）｜新しい画（映像方針）：台本どおり（どちらにも帰属の札）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.13（`I do not consider that a definite answer to the question 'was TITANIC seen' can be given`…`More probably, in my view, the ship seen by CALIFORNIAN was another, unidentified, vessel`）"),
    'c929': dict(kind='写真',
               plan='N04:J｜映像の素材 10.40秒・倍率 1.02（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（249.5〜259.9秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：台本どおり（区間＝明るい甲板）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.14（`One possibility is that she was the Norwegian sealer SAMSON`…`There are fairly obvious weaknesses in this account`）'),
    'c930': dict(kind='文字の頁',
               plan='🔧 P-G2-18｜一覧の種類：頁｜見せ方：頁（引用・額装）｜副題：海難調査局の報告書 p.14〈1992年〉｜動き：静止｜見た目の型：文字の頁｜権利：引用（OGL v3.0 か Crown copyright か未確定）｜時期：文書｜人：なし｜出典の行：出典：英国運輸省 海難調査局『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』（1992年）より引用｜新しい画（映像方針）：🔧 寄る → 静止の切り出し（「I entirely agree with him」の行・引用の型）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.14（`The Inspector's answer is 'Yes', and I entirely agree with him`）"),
    'c931': dict(kind='写真',
               plan='🔧 S8-E03:船体｜一覧の種類：実写｜見せ方：全面｜副題：カルパチア号の乗客が撮ったとされるカリフォルニアン号〈1912年4月15日〉｜動き：右へ｜権利：PD｜時期：後・救助｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 S8-625 の7回目 → S8-E03 の3回目（寄りを替える）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.14（`it has been suggested that these were Company signals from the other ship seen by CALIFORNIAN, I think this possibility is quite unrealistic`…`it would explain their apparent low altitude`）'),
    'c932': dict(kind='写真',
               plan='N04:K1｜映像の素材 8.90秒・倍率 1.02（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（280.0〜288.9秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：台本どおり（区間＝暗い構造物）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.3（`The Inspector considers that TITANIC`…`distress signals were seen, and that proper action was not taken. I agree on both counts`）・G2 p.15（`Merely attempting to call by morse lamp fell far short of what was needed`）'),
    'c933': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：あるべきだった4つの手の順の矢印｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.15〜16（`The Master should have been called and if he did not immediately respond Mr`…`Stone should have reported to him in person`…`Stand By Engines`…`The Wireless Operator should have been called`…`got under way towards the apparent source of the rockets`）'),
    'c934': dict(kind='写真',
               plan='S3-749:引き｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：スタンリー・ロード〈1908年・別の船の船長だったころ〉｜動き：静止｜権利：PD｜時期：別の年｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（3回目・額の中の寄りを替える＝静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.16（`that Captain Lord lay drunk in his cabin, that he was entirely callous or that he was frightened to attempt to manoeuvre in the ice`…`Captain Lord was in fact almost tee-total`…`Captain Lord in fact took his ship through the ice twice once he learnt of TITANIC'S distress`）"),
    'c935': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：深い眠りの中の呼びかけ（返事はするのに届かない・顔の無い影）｜合図：🔁 正面→横から（前の図 c933）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.17（`there is a state of somnambulism quite often experienced in which the subject appears to respond to a call but the message given does not break the barrier between sleep and`…`I think the message from the Bridge simply did not get through`）'),
    'c936': dict(kind='再現イラスト',
               plan='🔧 一覧の種類：案C-9｜見る向き：横から｜見た目の型：カリフォルニアン号の船橋・1時10分ごろ・伝声管の口の前に立つ二等航海士の影｜注：c633 と時刻の札を替える｜新しい画（映像方針）：🔧 S8-E03 の6回目 → 案C-9（記録＝G1 p.58「Mr. Stone reported to the captain by voice pipe」・心の中は描かない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.17（`There is a natural tendency to reject the signals of disaster and to hope that all is well despite the evidence of one's`…`Mr Stone should have gone down himself to the`…`Master when there was no proper response from him`）"),
    'c937': dict(kind='文字の頁',
               plan='🔧 P-G2-21｜一覧の種類：頁｜見せ方：頁（引用・額装）｜副題：海難調査局の報告書 p.17〈1992年〉｜動き：静止｜見た目の型：文字の頁｜権利：引用（OGL v3.0 か Crown copyright か未確定）｜時期：文書｜人：なし｜出典の行：出典：英国運輸省 海難調査局『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』（1992年）より引用｜新しい画（映像方針）：🔧 寄る → 静止の切り出し（「I sympathise with Mr Stone」の行・引用の型）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.17（`he was in fact something of a martinet, and the young officer may have feared to leave the`…`I sympathise with Mr Stone, but it must be said that he was seriously at fault`）'),
    'c938': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：最初の信号弾で動いていたら（0時45分ごろ・約31キロ・沈むころに着く）｜合図：🔁 横から→上から（前の図 c936）｜新しい画（映像方針）：台本どおり（札は「タイタニック号の時計」と「現実的でない」）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.18（`The first rocket appears to have been fired at about 0045 hrs (TITANIC time)`…`given my minimum distance off of 17 miles, have reached the scene at just about the time of sinking. This however is unrealistic`）'),
    'c939': dict(kind='フリー素材',
               plan='🔧 X-meteor｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 6.99秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜空の流れ星｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：⑤b で1本ずつ（月なし・CG でないもの）｜新しい画（映像方針）：🔧 S5-359 の2回目 → イメージ（流れ星＝語りの言葉）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.18（`No officer would take such action on seeing a single distant flash which might be a shooting star or even a visual aberration`）'),
    'c940': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：時間の線｜見た目の型：正しく動いた場合の流れ（時刻の札は置かない）｜合図：🔁 上から→時間の線（前の図 c938）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.18（`Captain Lord would have been on the Bridge at perhaps 0055 hrs`…`would shortly receive TITANIC'S SOS with its incorrect position`…`CALIFORNIAN would arrive well after the sinking`）"),
    'c941': dict(kind='文字の頁',
               plan='🔧 P-G2-22｜一覧の種類：頁｜見せ方：頁（引用・額装）｜副題：海難調査局の報告書 p.18〈1992年〉｜動き：静止｜見た目の型：文字の頁｜権利：引用（OGL v3.0 か Crown copyright か未確定）｜時期：文書｜人：なし｜出典の行：出典：英国運輸省 海難調査局『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』（1992年）より引用｜新しい画（映像方針）：🔧 寄る → 静止の切り出し（「if I am right as to the distance apart」から「should have been made」まで・引用の型）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.18（`if I am right as to the distance apart`…`I do not think any reasonably probable action by Captain Lord could have led to a different outcome of the tragedy. This of course does not alter the fact that the attempt should have been made`）'),
    'c942': dict(kind='写真',
               plan='🔧 S7-598:全体｜一覧の種類：実写｜見せ方：全面｜副題：ニューヨークに入るカルパチア号〈1912年4月・LOC〉｜動き：左へ｜権利：PD｜時期：後・NY｜人：なし｜出典の行：出典：米国議会図書館（LOC）｜新しい画（映像方針）：🔧 S6-480 の4回目 → カルパチア号（語り＝カルパチア号がした救助）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.18（`the effect of CALIFORNIAN taking proper action would have been no more than to place on her the task actually carried out by CARPATHIA, that is the rescue of those who escaped`）'),
    'c943': dict(kind='写真',
               plan='🔧 N04:H｜映像の素材 7.40秒・倍率 1.03（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（170.0〜177.4秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：🔧 S11-716 の2回目 → NOAA の船室の窓の区間｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 送り状（`incorporates his conclusions and those of the appointed Inspector`…`full endorse the Deputy Chief Inspector's report and conclusions`）"),
    'c944': dict(kind='写真',
               plan='N04:K2｜映像の素材 4.00秒・倍率 1.04（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（325.0〜329.0秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：台本どおり（区間＝錆の構造物）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.18（`The TITANIC disaster led to a number of changes improving provisions for emergency at sea`）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-10-27）：フリー素材（Pexels・イメージ）＝`ss.vid`（見出し・副題は書かない＝左上の「イメージ」と出典だけ）。
#   区間（27秒の流れ星の筋を入れる）は `qa_out/ep26_assets.py` の STOCK_WINDOW → footage.USE
SPEC.update({
    "c939": ss.vid("c939"),
})

# 🆕 ⑤b-3（2026-10-27）：地図（衛星写真＋描き足し＝`ss.sat`・寄らない・色を変えない）＝外洋は一面の海に点と札（了承② 決め2）。
#   位置は G2（MAIB 1992）p.3・p.7・p.11 の頁の画像で読んだ値（`ref/ep26/sources.md` §2-1）。札に数字を置かない（距離は語り）・見えたかの線は描かない
SPEC.update({
    # c909（3行・12.7秒）＝1行目「同じ見方をしたところから」は地図だけ → 2行目「ぶつかった位置と沈んだ位置」→ 3行目「無線の位置のずれ」
    "c909": dict(
        **ss.sat("G03", steps=[
            [],
            [dict(k="x", at="collision", t="ぶつかった位置（推定）", lab=(20, -20, "start")),
             dict(k="pt", at="wreck", c="INK_W", t="沈んだ位置（残骸）", lab=(20, 30, "start"))],
            [dict(k="line", path=("cqd", "wreck"), c="AMBER", dash=True),
             dict(k="pt", at="cqd", c="AMBER", t="無線で送った位置", lab=(-14, -22, "end"))]],
            note="位置は英国海難調査局の調べ直しの値"),
        t="船の位置", s="事故の海域・北大西洋（現在の衛星写真）"),
    # c917（2行・9.4秒）＝カリフォルニアン号の位置の2つの見方を別々の点で（どちらにも帰属の札）。2行目は描き足さない（距離は語り）
    "c917": dict(
        **ss.sat("G04", steps=[
            [dict(k="x", at="collision", t="タイタニック号", lab=(20, 28, "start")),
             dict(k="pt", at="cal_dep", role="ntsb", t="次長の見方", lab=(-20, -16, "end")),            # 緑＝c306 のカリフォルニアン号と同じ色
             dict(k="pt", at="cal_inv", role="tsb", t="調査官の見方（たぶんもっと東）", lab=(20, -16, "start"))],   # 紫
            []],
            note="位置は英国海難調査局の調べ直しの値・どちらも「あたり」"),
        t="カリフォルニアン号の位置", s="事故の海域・北大西洋（現在の衛星写真）"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-27）：案C-9 伝声管の前の二等航海士＝K1（c936・`tools/illu26.py`・門番 check_illu ㊽）
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c936（2行・8.8秒）＝1行目「人には、悪い知らせを打ち消したくなる心がある、と次長は書く。」は伝声管の前の二等航海士（心の中は描かない）→
    #   2行目「二等航海士は、船長がちゃんと応えないなら、自分で行くべきだった、とも。」で伝声管へ輪。時計の札は出さない（1:10 は割れる）
    "c936": dict(fig=("illu", dict(
        place="K1", start=dict(ks="pipe", kship="glare"), at="1:10",
        rec="G1 p58（about 1.10 a. m., Mr. Stone reported to the captain by voice pipe）",
        people=dict(crew=(1, "G1 p58（about 1.10 a. m., Mr. Stone reported to the captain by voice pipe）")),
        steps=[dict(state=dict(), tag=dict(t="二等航海士", at="P", off=(-50, -50), anchor="end", keep=True)),
               dict(state=dict(), rings=2, rec="G2 p2021（Mr Stone should have gone down himself to the Master when there was no proper response from him）",
                    tag=dict(t="伝声管", at="pipe", off=(40, -170)))]))),     # 🔧 試し焼き 40594842436：左上では「二等航海士」の札の線と交わった
})

# 🆕 ⑤b-6（2026-10-28）：図解（`tools/mech26.py`・fig=("m26", …)）。段の数＝語りの行の数・画面の数は全部 rel に（門番 check_mech の judge_m26）
#   🔴 調査官＝紫・次長＝緑（c917 の地図と同じ）。カリフォルニアン号（緑）と同じ画面では次長を白い字に（c914・c915・c921・c938・c940）
SPEC.update({
    # c902（2行）＝1行目「80歳をこえていた船長は、もう一度調べてほしいと訴えた」→ 2行目「請願も2度出たが、どちらも退けられた」
    "c902": dict(
        t="80年のあいだ", s="調べ直しまでの年表",
        fig=("m26", dict(view="years6", steps=[dict(state=dict(plea="on")), dict(state=dict(pet="on"))],
                         rel=[dict(t="1912年", src="G2 p2006"), dict(t="1950年代", src="G2 p2005"), dict(t="80歳", src="G2 p2005"),
                              dict(t="2度", src="G2 p2005"), dict(t="1985年", src="G2 p2006"), dict(t="1990年", src="G2 p2006"), dict(t="1992年", src="G2送 p2003")],
                         note="並びは年の順・間の長さは模式（請願の年は記録に無い）", src=ss.src(["G2 p2005", "G2 p2006"])))),
    # c905（3行）＝1行目の問い → 2行目「2隻の位置と距離。タイタニック号は見えていたか」→ 3行目「遭難の信号は…正しく動いたか。そして、船長の行い」
    "c905": dict(
        t="問われたこと", s="1992年の報告の始まり",
        fig=("m26", dict(view="four_q", steps=[dict(state=dict(q="on")), dict(state=dict(a="on")), dict(state=dict(b="on"))],
                         rel=[dict(t="4つの問い", src="G2 p2007")], note="札の絵は模式", src=ss.src(["G2 p2007"])))),
    # c908（2行）＝1行目「首席は、次長の報告と結論を、全面的に支持する」→ 2行目（聞き役）「意見が分かれたんだね」
    "c908": dict(
        t="首席はどちらに", s="1冊の報告に2つの結論",
        fig=("m26", dict(view="book2", steps=[dict(state=dict(chief="on")), dict(state=dict(split="on"))],
                         note="本の形は模式", src=ss.src(["G2送 p2003"])))),
    # c910（2行）＝1行目「2人とも、海の流れが南へ向かっていたことは認める」→ 2行目「北から来る冷たい海流が、いつもより南まで」
    "c910": dict(
        t="張り出した流れ", s="1912年の北大西洋",
        fig=("m26", dict(view="current", steps=[dict(state=dict(flow="on")), dict(state=dict(far="on"))],
                         rel=[dict(t="時速約2.4キロ", src="G2 p2013")], note="海流の形は模式（向きは約196度・速さは約1.3ノット）", src=ss.src(["G2 p2013"])))),
    # c911（1行・c910 の続き）＝聞き役「流れの向きは、どちらも同じ考えなんだね」で2人の札
    "c911": dict(
        t="流れの向き", s="2人の考え",
        fig=("m26", dict(view="current", start=dict(flow="on", far="on"), steps=[dict(state=dict(both="on"))],
                         rel=[dict(t="時速約2.4キロ", src="G2 p2013"), dict(t="2人", src="G2 p2013")],
                         note="海流の形は模式（向きは約196度・速さは約1.3ノット）", src=ss.src(["G2 p2013"])))),
    # c912（3行）＝1行目「分かれた点の1つは…いつから船を押したか」で次長の帯 → 2行目「調査官は…約9キロから19キロ」→ 3行目「たぶん9キロに近い」
    "c912": dict(
        t="割れた見立て", s="調査官の見方と次長の見方",
        fig=("m26", dict(view="dist2col", steps=[dict(state=dict(dep="on")), dict(state=dict(insp="on")), dict(state=dict(near="on"))],
                         rel=[dict(t="約9〜19キロ（5〜10マイル）", src="G2 p2011"), dict(t="9キロに近い", src="G2 p2011"),
                              dict(t="約31〜37キロ（17〜20マイル）", src="G2 p2007"), dict(t="約33キロ（18マイル）", src="G2 p2011")],
                         note="横は距離に比例（止まっていたあいだの2隻の間）", src=ss.src(["G2 p2007", "G2 p2011"])))),
    # c913（2行）＝1行目「調査官によれば…14日の昼から南へ流されていたのに」→ 2行目「船長は計算に入れていない。だから、もっと近かった」
    "c913": dict(
        t="計算に入れなかった流れ", s="調査官が見た道すじ",
        fig=("m26", dict(view="drift_s", steps=[dict(state=dict(flow="on")), dict(state=dict(calc="on"))],
                         rel=[dict(t="14日の昼", src="G2 p2013")], note="道すじは模式", src=ss.src(["G2 p2007", "G2 p2013"])))),
    # c914（3行）＝1行目「次長は…1つは、星の観測だ」→ 2行目「夜7時半、北極星で測った緯度が」→ 3行目「昼の12時と同じ。真西へ」
    "c914": dict(
        t="真西へ進んだ証し", s="北極星で測る緯度",
        fig=("m26", dict(view="polaris", steps=[dict(state=dict(dep="on")), dict(state=dict(star="on")), dict(state=dict(same="on"))],
                         rel=[dict(t="19:30", src="G2 p2014")], note="星の高さと船は模式（角度は北緯42度5分の写し）", src=ss.src(["G2 p2014"])))),
    # c915（2行）＝1行目「アンティリアン号への電報。事故の前に打った知らせで」→ 2行目「あとから作りようがない…西へ進んでいたことと合う」
    "c915": dict(
        t="事故の前の電報", s="西へ進んでいたか",
        fig=("m26", dict(view="antillian", steps=[dict(state=dict(msg="on")), dict(state=dict(west="on"))],
                         rel=[dict(t="18:30", src="G2 p2011"), dict(t="大きな氷山3つ", src="G2 p2011")], note="位置は模式",
                         src=ss.src(["G2 p2011", "G2 p2014"])))),
    # c919（3行）＝1行目「地球は丸いので、遠い船は、水平線の向こうに隠れる」→ 2行目「2人の距離の見方は、見えたかどうかの考えに」→ 3行目「引っぱられている」
    "c919": dict(
        t="見えない遠さ", s="地球は丸い",
        fig=("m26", dict(view="horizon", steps=[dict(state=dict(hide="on")), dict(state=dict(two="on")), dict(state=dict(pull="on"))],
                         note="地球の丸みと高さは模式（大きく誇張）", src=ss.src(["G2 p2015", "G2 p2017"])))),
    # c921（3行）＝1行目「カリフォルニアン号から見えたことだけなら、次長も反対はしない」→ 2行目「その船の時計で0時30分ごろまで」→ 3行目「見張り台にも船橋にも、人がいた」
    "c921": dict(
        t="答えはこちら側に", s="見張りがいた船",
        fig=("m26", dict(view="tt_watch", steps=[dict(state=dict(cfok="on")), dict(state=dict(ans="on")), dict(state=dict(crew="on"))],
                         rel=[dict(t="0:30ごろ", src="G2 p2016")], note="船と目の届く先は模式", src=ss.src(["G2 p2016"])))),
    # c923（3行）＝1行目の問い → 2行目「次長は、2つの見方をあげる。1つは、第三の船だ」→ 3行目「東から来て氷原で止まり…すき間を探して去った」
    "c923": dict(
        t="見えていた船は", s="次長があげた見方",
        fig=("m26", dict(view="third", steps=[dict(state=dict(q="on")), dict(state=dict(one="on")), dict(state=dict(path="on"))],
                         note="道すじと氷原は模式（形は描き分けない）", src=ss.src(["G2 p2017"])))),
    # c925（3行）＝1行目「異常屈折だ。空気の温度の差で光が曲がり」→ 2行目「水平線の向こうの物が、見えることがある」→ 3行目「遠くのタイタニック号を見ていたことになる」
    "c925": dict(
        t="異常屈折", s="遠くが浮かぶしくみ",
        fig=("m26", dict(view="refract", steps=[dict(state=dict(bend="on")), dict(state=dict(ghost="on")), dict(state=dict(tt="on"))],
                         note="空気の層と光の道は模式（大きく誇張）", src=ss.src(["G2 p2017", "G2 p2030"])))),
    # c927（2行）＝1行目「船長が見たのは緑の舷灯。のちに赤の舷灯が見えた」で船が右へ回る → 2行目「止まったままのタイタニック号なら、赤い灯は見えないはず」
    "c927": dict(
        t="舷灯の色", s="緑から赤へ",
        fig=("m26", dict(view="swing", steps=[dict(state=dict(seen="on"), delay=2.2), dict(state=dict(tt="on"))],
                         note="船の向きと回り方は模式（右舷＝緑・左舷＝赤）", src=ss.src(["G2 p2017"])))),
    # c928（3行）＝1行目「はっきりした答えは出せない」→ 2行目「見えたのなら、異常屈折のせいだ」→ 3行目「名前の分からない別の船だろう」
    "c928": dict(
        t="はっきりしない答え", s="1992年の2つの見方",
        fig=("m26", dict(view="seen2col", steps=[dict(state=dict(a="on")), dict(state=dict(b="on")), dict(state=dict(c="on"))],
                         note="札の並びは模式", src=ss.src(["G2 p2017"])))),
    # c933（3行）＝1行目「二等航海士が船長を呼び」→ 2行目「すぐ応じなければ自分で行く。機関室に…」→ 3行目「通信士を起こす。そして船長は船橋へ」
    "c933": dict(
        t="船長を呼ぶところから", s="次長があげた4つ",
        fig=("m26", dict(view="four_steps", steps=[dict(state=dict(s1="on")), dict(state=dict(s2="on")), dict(state=dict(s3="on"))],
                         note="手の順は模式（Stand By Engines＝原文の言い方）", src=ss.src(["G2 p2019", "G2 p2020"])))),
    # c935（3行）＝1行目「深く眠っていて呼ばれると」→ 2行目「返事はしても、言われたことが頭に届かない」→ 3行目「船橋からの知らせは、ただ届かなかった」
    "c935": dict(
        t="届かなかった知らせ", s="深い眠りの中の呼びかけ",
        fig=("m26", dict(view="asleep", steps=[dict(state=dict(call="on")), dict(state=dict(reply="on")), dict(state=dict(nogo="on"))],
                         note="眠りと目覚めの境は模式（次長の見方）", src=ss.src(["G2 p2021"])))),
    # c938（3行）＝1行目の問い → 2行目「タイタニック号の時計で0時45分ごろの、最初の信号弾ですぐ全速で」→ 3行目「約31キロでも、着くのはたぶん沈むころ」
    #   🔧 一覧の見た目の型「札は…『現実的でない』」は置かない＝その語りは次の c939（前倒ししない・⑤b-6 §5-2・⑤c' で一覧と合わないことを記録）
    "c938": dict(
        t="全速で向かったなら", s="最初の信号弾で向かったとき",
        fig=("m26", dict(view="if_go", steps=[dict(state=dict(q="on")), dict(state=dict(go="on")), dict(state=dict(far="on"))],
                         rel=[dict(t="0:45ごろ", src="G2 p2022"), dict(t="約31キロ（17マイル）", src="G2 p2022")], note="位置は模式",
                         src=ss.src(["G2 p2022"])))),
    # c940（2行）＝1行目「船長が船橋に来るまで少しかかり、氷の中では慎重に」→ 2行目「ずれた位置の無線で迷い、着くのは、沈んだずっとあと」
    "c940": dict(
        t="正しく動いても", s="遅れが重なる",
        fig=("m26", dict(view="if_flow", steps=[dict(state=dict(a="on")), dict(state=dict(b="on"))],
                         note="道は模式（時刻の札は置かない）", src=ss.src(["G2 p2022"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-28）：写真・頁・NOAA の映像（第8章の21カット）＝書き方は c2.py の ⑤b-7 の注と同じ
# ══════════════════════════════════════════════════════════
#   🔴 海難調査局（MAIB）の頁は引用（assets.json の frame）＝額装だけ（`ss.check_frame_only`＝切る・地のぼかし・寄せ・色を変えるを止める）。
#      語りの段落だけにするのは束の段の切り出し（`qa_out/ep26_assets.py` の PAGE_CROP＝P-G2-03・18・21・22・23）
#   NOAA 2004 の映像（c901・c907・c918・c926・c929・c932・c943・c944）＝`ss.vid`（ひかえの静止画 `ref/ep26/fb_c9xx.jpg`）
_S11910, _PG201, _PG203, _S3753, _S1089, _S2033 = P("s11_910"), P("p_g2_01"), P("p_g2_03"), P("s3_753"), P("s1_089"), P("s2_033")
_S8N05, _PG218, _S8E03, _S3749, _PG221, _PG222, _S7598 = (P("s8_n05"), P("p_g2_18"), P("s8_e03"), P("s3_749"), P("p_g2_21"),
                                                         P("p_g2_22"), P("s7_598"))
_NOAA = "海の底のタイタニック号〈2004年・NOAA ほか〉"
# 絵はがき（S8-N05）＝絵の枠の内だけ（下の題「WHITE STAR LINE PIERS, NEW YORK.」と「COPYRIGHT, 1905…」と台紙の余白は外）
_S8N05_IN = (0.012, 0.035, 0.975, 0.665)
SPEC.update({
    "c901": dict(**ss.vid("c901", t="繰り返された非難", s=_NOAA), side="none"),
    "c903": dict(photo=_S11910, **ss.mv(_S11910, "d"), side="none", color=1.0,
                 t="1985年の残骸", s="海の底のタイタニック号の残骸〈2003年・NOAA ほか〉"),
    # c904（2行）＝報告書の表紙の題の4行（引用＝束の段で題だけを切り出した 778×742・額装・静止）
    "c904": dict(photo=_PG201, panel=True, color=1.0,
                 t="再評価の命令", s="海難調査局の報告書の表紙の題〈1992年〉"),
    # c906（2行）＝送り状（束の段で宛先の大臣の名前と首席の署名を外した「Clearly, the case…」〜「I full endorse…」）
    "c906": dict(photo=_PG203, panel=True, pw=1640, color=1.0,
                 t="外から来た調査官", s="調査官を外から呼んだわけと同意の行"),
    "c907": dict(**ss.vid("c907", t="次長がさらに調べる", s=_NOAA), side="none"),
    # c916（1行）＝c709 と同じ写真・同じ副題＝額の中の切り口を顔（x 0.2〜0.8・y 0.02〜0.40）に替える（静止）
    "c916": dict(photo=_S3753, trim=(0.2, 0.02, 0.8, 0.40), panel=True, ground=dict(photo=_S3753), color=1.0,
                 t="北へ流された船", s="カルパチア号の船長アーサー・ロストロン〈1912年〉"),
    "c918": dict(**ss.vid("c918", t="約9キロか約33キロか", s=_NOAA), side="none"),
    # c920（3行）＝c212 と同じ写真・同じ副題＝寄り 1.25 で船体に沿って右へ（c212 は寄り 1.12）
    "c920": dict(photo=_S1089, **ss.mv(_S1089, "r", z=1.25, span=(0.15, 0.85)), side="none", color=1.0,
                 t="調査官の見立て", s="試運転の日のタイタニック号〈1912年4月2日〉"),
    # c922（2行）＝c217 と同じ写真・同じ副題＝マストの見張り台（x 0.68・y 0.45）へ寄る
    "c922": dict(photo=_S2033, **ss.mv(_S2033, "in", fx=0.68, fy=0.45, z=1.4), side="none", color=1.0,
                 t="見えなければ見えない", s="船橋と見張り台〈1912年4月10日〉"),
    "c924": dict(photo=_S8N05, **ss.tcam(_S8N05, _S8N05_IN, (0.38, 0.5, 1.0), (0.62, 0.5, 1.0)), side="none", color=1.0,
                 t="第三の船がいた？", s="ニューヨークのホワイト・スター・ラインの桟橋〈1905年ごろの絵はがき〉"),
    "c926": dict(**ss.vid("c926", t="低く見えた信号弾", s=_NOAA), side="none"),
    "c929": dict(**ss.vid("c929", t="決まらない答え", s=_NOAA), side="none"),
    # c930（2行）＝p.14 の節の題「WERE TITANIC'S ROCKETS SEEN?」と段落の頭（束の段の切り出し）
    "c930": dict(photo=_PG218, panel=True, pw=1640, color=1.0,
                 t="信号弾は見えていた", s="信号弾は見えたか、の節"),
    # c931（2行）＝c106・c716 と同じ写真・同じ副題＝寄り 1.35 で船体に沿って右へ
    "c931": dict(photo=_S8E03, **ss.mvz(_S8E03, (0.35, 0.47, 1.35), (0.70, 0.45, 1.35)), side="none", color=1.0,
                 t="会社の信号ではない", s="カルパチア号の乗客が1912年4月15日に撮ったとされるカリフォルニアン号"),
    "c932": dict(**ss.vid("c932", t="とても足りない", s=_NOAA), side="none"),
    # c934（3行）＝c608・c624 と同じ写真・同じ副題＝まるごと（引き）・静止
    "c934": dict(photo=_S3749, panel=True, ground=dict(photo=_S3749), color=1.0,
                 t="退けられた説", s="スタンリー・ロード〈1908年・別の船の船長だったころ〉"),
    # c937（2行）＝p.17「…Of course, … should have gone down himself…」〜「seriously at fault.」（束の段の切り出し）
    "c937": dict(photo=_PG221, panel=True, pw=1640, color=1.0,
                 t="重い落ち度", s="二等航海士の落ち度を書いた文"),
    # c941（3行）＝p.18「It therefore seems clear that - if I am right as to the distance apart -…」〜「should have been made.」
    "c941": dict(photo=_PG222, panel=True, pw=1640, color=1.0,
                 t="結果は変わらない", s="前置きつきの結論の文"),
    "c942": dict(photo=_S7598, **ss.mv(_S7598, "l"), side="none", color=1.0,
                 t="救助を引き受けただけ", s="ニューヨークに入るカルパチア号〈1912年4月・LOC〉"),
    "c943": dict(**ss.vid("c943", t="支持されたのは次長", s=_NOAA), side="none"),
    "c944": dict(**ss.vid("c944", t="事故が変えたもの", s=_NOAA), side="none"),
})
