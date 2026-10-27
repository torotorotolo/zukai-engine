# -*- coding: utf-8 -*-
"""第7章　1912年の結論 c801–c826（26カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c8.py`）。
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
    'c801': dict(kind='写真',
               plan='🔧 S3-671:長｜一覧の種類：実写｜見せ方：全面｜副題：英国の審問の長マージー卿〈1912年〉｜動き：寄る（長へ）｜権利：PD｜時期：後・審問｜人：公的な任務（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 額装 → 全面・c636 と別の寄り｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.6（`the Wreck Commissioner appointed was Lord Mersey`…`The proceedings included 37 public sittings, beginning on 2 May 1912, and 97 witnesses were examined. The Court reported on 30 July 1912`）'),
    'c802': dict(kind='写真',
               plan='S9-674:模型｜一覧の種類：実写｜見せ方：全面｜副題：英国の審問の会場〈ロンドン・1912年〉｜動き：寄る（壁の模型へ）｜権利：PD｜時期：後・審問｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（c629 と別の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.6（`The Transcript, which includes over 25,000 questions and answers, has been invaluable to this reappraisal`）'),
    'c803': dict(kind='文字の頁',
               plan='P-G1-005｜一覧の種類：頁｜見せ方：頁｜副題：英国の審問の報告 p.5｜動き：寄る（「brought about by the excessive speed」の一文へ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：英国の審問の報告（米国上院の刷り直し S. Doc. 933）p.5｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.5（`the loss of the said ship was due to collision with an iceberg, brought about by the excessive speed at which the ship was being navigated`）'),
    'c804': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：時間の線｜見た目の型：25年あまりの慣行の年月の帯と船の絵（晴れた夜は針路と速さを保つ）｜合図：🔁 横から→時間の線（前の図 c712）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.40（`for a quarter of a century or more, the practice of liners using this track when in the vicinity of ice at night had been in clear weather to keep the course, to maintain the speed and to trust to a sharp lookout`）'),
    'c805': dict(kind='写真',
               plan='S3-714:顔｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：タイタニック号の船長エドワード・スミス〈1912年4月・ニューヨーク・タイムズに載った写真〉｜動き：静止｜権利：PD｜時期：前｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（2回目・額の中の寄りを替える＝静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.40（`the event has proved the practice to be bad`…`in competition and in the desire of the public for quick passages rather than in the judgment of naviga`）'),
    'c806': dict(kind='文字の頁',
               plan='P-G1-041｜一覧の種類：頁｜見せ方：頁｜副題：英国の審問の報告 p.41｜動き：寄る（「a very grievous mistake」の一文へ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：英国の審問の報告（米国上院の刷り直し S. Doc. 933）p.41｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.41（`He made a mistake, a very grievous mistake, but one in which, in face of the practice and of past experience, negligence can not be said to have had any part`）'),
    'c807': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：時間の線｜見た目の型：「これまで」と「これから」の線（事故の前は慣行・あとは怠り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.41（`What was a mistake in the case of the Titanic would without doubt be negligence in any similar case in the future`）'),
    'c808': dict(kind='写真',
               plan='🔧 S7-594:全体｜一覧の種類：実写｜見せ方：全面｜副題：ニューヨークのピアのカルパチア号〈1912年4月20日・BnF〉｜動き：右へ｜権利：PD｜時期：後・NY｜人：小さい（⑤b で原寸）｜出典の行：出典：フランス国立図書館（BnF）｜注：🔴 副題で「着いた」と言わない（着いたのは4月18日の夜）｜新しい画（映像方針）：🔧 S3-675 の4回目 → カルパチア号（語り＝なぜカルパチア号より先に助けが届かなかったか）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.1（`The Court was asked the specific question (which was added to the original list of questions during the hearing)`…`What vessels had the opportunity of rendering assistance to the`）'),
    'c809': dict(kind='文字の頁',
               plan='P-G1-085｜一覧の種類：頁｜見せ方：頁｜副題：英国の審問の報告 p.85｜動き：寄る（問24の答えへ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：英国の審問の報告（米国上院の刷り直し S. Doc. 933）p.85｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.85（`The Californian. She could have reached the Titanic if she had made the attempt when she saw the first rocket. She made no attempt`）'),
    'c810': dict(kind='図解',
               plan='一覧の種類：並べ｜見る向き：正面｜見た目の型：1912年の報告の突き合わせの2列（タイタニック号の記録・カリフォルニアン号の記録）｜合図：🔁 時間の線→正面（前の図 c807）｜新しい画（映像方針）：台本どおり（札は船ごとの時計・2列を1本の線にしない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`There are contradictions and inconsistencies in the story as told by the different witnesses. But the truth of the matter is plain`）'),
    'c811': dict(kind='写真',
               plan='🔧 S8-625:煙突とマスト｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号〈カルパチア号の甲板から撮られたとみられる・NARA〉｜動き：寄る（煙突とマストへ）｜権利：PD｜時期：後・救助｜人：なし｜出典の行：出典：米国立公文書館（NARA）｜新しい画（映像方針）：🔧 寄りを替える（3回目）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`The Titanic collided with the berg at 11.40. The vessel seen by the`…`stopped`…`The number sent up by the`…`was about eight. The`…`saw eight`）'),
    'c812': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：2つの時計の絵と「船ごとに時計が違う」・1992年の「差は数分ほど」の札｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.60（`was from about 12.45 to 1.45 o'clock. It was about this time that the Californian saw the rockets`）・G2 p.6（`only likely to have been a few minutes`）"),
    'c813': dict(kind='写真',
               plan='🔧 N04:B｜映像の素材 9.50秒・倍率 1.02（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（54.0〜63.5秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：🔧 S6-480 の3回目 → NOAA の船首の横の区間（語り＝2時20分に沈んでいる）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`At 2.40 Mr. Stone`…`the master that`…`the ship from which he had seen`…`rockets had disappeared. At 2.20 a. m. the Titanic had foundered`）'),
    'c814': dict(kind='写真',
               plan='S10-905:ほかの船｜一覧の種類：実写｜見せ方：全面（切り出し）｜副題：1912年の新聞の地図〈船の位置は当時の報道の見立て〉｜動き：右へ（ほかの船の印へ）｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：オランダ国立公文書館（Spaarnestad Photo）｜新しい画（映像方針）：台本どおり（2回目・別の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`It was suggested that the rockets seen by the Californian were from some other ship`…`But no other ship`…`theory has ever`…`been heard of`…`circumstances convince`…`Californian was the Titanic`）'),
    'c815': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：距離の物差しの輪（約9キロ・約15キロ・約19キロ・船の印は置かない）｜合図：🔁 正面→上から（前の図 c812）｜新しい画（映像方針）：台本どおり（見えたかどうかは描かない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`according to Capt. Lord, the`…`two vessels were about`…`5 miles apart at the time of the disaster`）'),
    'c816': dict(kind='図解',
               plan='🔧 一覧の種類：続き｜見た目の型：（c815 の続き）｜新しい画（映像方針）：🔧 S1-084 の2回目 → c815 の輪の続き（報告書の「9キロより遠く19キロより遠くない」の帯を明るくする）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`I am advised that the distance was probably greater, though not more than 8 to 10 miles`）'),
    'c817': dict(kind='写真',
               plan='🔧 S5-362:氷原｜一覧の種類：実写｜見せ方：全面｜副題：氷原と氷山〈1912年4月・カルパチア号の乗客が撮ったと1912年の本は書く〉｜動き：右へ（氷原に沿って）｜権利：PD｜時期：氷｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：c318 と同じ写真・同じ副題・別の寄り・本の頁の字は切り出しの外｜新しい画（映像方針）：🔧 S5-359 の2回目 → 氷原の写真（語り＝氷はまばら・晴れた夜・静かな海）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`was loose ice extending for a distance of not more than 2 or 3 miles in the direction of the`…`The night was clear and the sea was smooth. When she first saw the rockets, the Californian could have pushed through the ice to the open water without any serious risk`）'),
    'c818': dict(kind='文字の頁',
               plan='P-G1-060｜一覧の種類：頁｜見せ方：頁｜副題：英国の審問の報告 p.60｜動き：寄る（「might have saved many if not all of the lives」の一文へ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：英国の審問の報告（米国上院の刷り直し S. Doc. 933）p.60｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`Had she done so she might have saved many if not all of the lives that were lost`）'),
    'c819': dict(kind='写真',
               plan='🔧 S3-698:全体｜一覧の種類：実写｜見せ方：全面｜副題：米国上院の小委員会の長〈LOC〉｜動き：寄る｜権利：PD｜時期：後・審問｜人：公的な任務（顔可）｜出典の行：出典：米国議会図書館（LOC）｜書き起こしの断り：米国上院の報告の文は書き起こし（有志のサイト）による・公式の写しは未照合｜注：🔴 名前は語りに無い（役職だけ）・タイタニック号の船長と名字が同じ＝紛れる。✅ 10-27 ネガの字の場所を確かめた＝上の帯（3840px の版の y0〜450 あたり）に「SENATOR SMITH, MICH.」と番号「566-1」＝切り出しは y450 より下｜新しい画（映像方針）：🔧 額装 → 全面（5766px）・ネガの字（議員の名）を切り出しの外へ｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='T3 AmInqRep06（書き起こし）・G7 p.2（`May 28, 1912. Ordered, That the testimony of witnesses`＝証言の印刷を命じた日・報告の公式の写しは未照合）'),
    'c820': dict(kind='写真',
               plan='S9-648:議員の席｜一覧の種類：実写｜見せ方：全面｜副題：米国上院の公聴会〈1912年4月・LOC〉｜動き：右へ｜権利：PD｜時期：後・審問｜人：遠景（⑤b で原寸）｜出典の行：出典：米国議会図書館（LOC）｜書き起こしの断り：米国上院の報告の文は書き起こし（有志のサイト）による・公式の写しは未照合｜新しい画（映像方針）：台本どおり（2回目・別の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='T3 AmInqRep06（書き起こし `was nearer the Titanic than the 19 miles reported by her captain`…`failed to respond to them in accordance with the dictates of humanity, international usage, and the requirements of law`）'),
    'c821': dict(kind='写真',
               plan='🔧 S9-645:議員｜一覧の種類：実写｜見せ方：全面｜副題：米国上院の公聴会〈1912年・英国の新聞の絵〉｜動き：寄る（議員の席へ）｜権利：PD｜時期：後・審問｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜書き起こしの断り：米国上院の報告の文は書き起こし（有志のサイト）による・公式の写しは未照合｜注：c705 と別の寄り｜新しい画（映像方針）：🔧 模式 → 公聴会の絵の寄り（c821→c822 の模式の続きを切る＝台本 §0-5）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='T3 AmInqRep06（書き起こし `whether arising from indifference or gross carelessness, is most reprehensible, and places upon the commander`…`a grave responsibility`）'),
    'c822': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：無線室の時計の針と、夜11時半に寝た通信士の影・「あと数分」の札｜合図：🔁 上から→正面（前の図 c815）｜書き起こしの断り：米国上院の報告の文は書き起こし（有志のサイト）による・公式の写しは未照合｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='T3 AmInqRep06（書き起こし `Had assistance been promptly proffered, or had wireless operator of the Californian remained a few minutes longer at his post`…`that ship might have had the proud distinction of rescuing the lives of the passengers and crew of the Titanic`）'),
    'c823': dict(kind='写真',
               plan='🔧 S9-674:札｜一覧の種類：実写｜見せ方：全面｜副題：英国の審問の会場〈ロンドン・1912年〉｜動き：左へ｜権利：PD｜時期：後・審問｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：語りは MAIB p.15（書き起こしでない）＝断りは要らない（台本 §0-5 の c819〜c823 のうち c823 だけ）｜新しい画（映像方針）：🔧 S3-749 の2回目 → 英国の審問の会場（語り＝英国の報告書の答え）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.15（`the Court did not single him out personally for criticism but simply referred to 'the CALIFORNIAN'`）"),
    'c824': dict(kind='写真',
               plan='S3-675:寄り｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号の船長スタンリー・ロード〈1912年5月・英国の審問のころ〉｜動き：寄る｜権利：PD｜時期：後・審問｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（3回目・別の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G2 p.1（`it was upon him that the great weight of the extremely grave accusation implied by the Court's finding fell`）"),
    'c825': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：時間の線｜見た目の型：審問のあとの流れ（やり直しを求める→退けられる・告発なし→処分なし→申し立ての道なし）｜合図：🔁 正面→時間の線（前の図 c822）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.1（`he requested a re-hearing of that part of the Inquiry which concerned his ship; the request was rejected, and as no formal charge had been laid against him, and no action had been taken against his`）'),
    'c826': dict(kind='写真',
               plan='S11-716:全体｜一覧の種類：実写｜見せ方：全面｜副題：海の底の船長室の浴槽〈2003年・NOAA ほか〉｜動き：上へ｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Image courtesy of ［撮影者］, RMS Titanic Expedition 2003, NOAA-OE.（撮影者の名は ⑤b で src/credits_private.tsv）｜注：S11-716 は1回（c943 は NOAA の映像に替えた）｜新しい画（映像方針）：台本どおり（副題を写っている物に＝c903 と分ける）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.1（`For many years the matter rested`）'),
}

SPEC = {}
