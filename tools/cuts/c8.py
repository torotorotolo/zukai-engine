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

# 🆕 ⑤b-6（2026-10-28）：図解（`tools/mech26.py`・fig=("m26", …)）。段の数＝語りの行の数・画面の数は全部 rel に（門番 check_mech の judge_m26）
SPEC.update({
    # c804（3行）＝1行目の問い → 2行目「報告書は、そうは言わない。25年以上…」で帯 → 3行目「針路と速さを保ち、見張りに頼る」
    "c804": dict(
        t="この航路のやり方", s="晴れた夜の客船の進み方",
        fig=("m26", dict(view="custom25", steps=[dict(state=dict(q="on")), dict(state=dict(band="on")), dict(state=dict(way="on"))],
                         rel=[dict(t="25年以上", src="G1 p40")], note="船の絵と帯は模式（25年より前は点線＝「以上」）", src=ss.src(["G1 p40"])))),
    # c807（3行）＝1行目「タイタニック号では間違い」→ 2行目「これから同じことをすれば怠り」→ 3行目（聞き役）「もう許されない」
    "c807": dict(
        t="事故の前とあと", s="同じことの重さ",
        fig=("m26", dict(view="before_after", steps=[dict(state=dict(a="on")), dict(state=dict(b="on")), dict(state=dict(c="on"))],
                         note="線は模式（同じやり方の扱いが、事故を境に変わる）", src=ss.src(["G1 p41"])))),
    # c810（3行）＝1行目の問い → 2行目「2隻の記録を、それぞれの船の時計のまま並べた」で2列 → 3行目「本当のところは明らか」で行を結ぶ
    "c810": dict(
        t="2隻の記録", s="報告書の突き合わせ",
        fig=("m26", dict(view="match2", steps=[dict(state=dict(q="on")), dict(state=dict(cols="on")), dict(state=dict(pair="on"))],
                         rel=[dict(t="約8発・8発", src="G1 p60")], note="札の並びは模式（時刻は船ごとの時計のまま・1本の線にしない）", src=ss.src(["G1 p60"])))),
    # c812（2行）＝1行目「信号弾は0時45分ごろから1時45分ごろ。カリフォルニアン号もそのころ見た」で扇 → 2行目「時計の違う2隻の時刻を、そのまま並べた」
    "c812": dict(
        t="時刻の並べ方", s="2隻の時計",
        fig=("m26", dict(view="clocks_gap", steps=[dict(state=dict(range="on")), dict(state=dict(diff="on"))],
                         rel=[dict(t="0:45ごろ〜1:45ごろ", src="G1 p60"), dict(t="1992年", src="G2 p2010")],
                         note="時計の盤は模式（右の扇＝カリフォルニアン号の時計のそのころ）", src=ss.src(["G1 p54", "G1 p60", "G2 p2010"])))),
    # c815（2行）＝1行目の問い → 2行目「船長の話では約9キロ（5マイル）」で内の輪
    "c815": dict(
        t="2隻の間の距離", s="船長が言った距離",
        fig=("m26", dict(view="rings3", steps=[dict(state=dict(q="on")), dict(state=dict(cap="on"))],
                         rel=[dict(t="約9キロ（5マイル）", src="G1 p60"), dict(t="約15キロ（8マイル）・約19キロ（10マイル）", src="G1 p60")],
                         note="輪の半径は距離に比例・位置は模式（船の印は置かない）", src=ss.src(["G1 p60"])))),
    # c816（2行・c815 の続き）＝1行目「たぶん約9キロより遠い」で外の帯 → 2行目「約15キロから19キロより遠くはない」で外の輪
    "c816": dict(
        t="報告書の距離", s="助言を受けた見方",
        fig=("m26", dict(view="rings3", start=dict(q="on", cap="on"), steps=[dict(state=dict(far="on")), dict(state=dict(lim="on"))],
                         rel=[dict(t="約9キロ（5マイル）", src="G1 p60"), dict(t="約15キロ（8マイル）・約19キロ（10マイル）", src="G1 p60")],
                         note="輪の半径は距離に比例・位置は模式（船の印は置かない）", src=ss.src(["G1 p60"])))),
    # c822（3行）＝1行目「米国上院の報告は…すぐ助けに向かっていたか」→ 2行目「通信士が、あと数分、持ち場にいたなら」→ 3行目「救う誇りを得ていたかもしれない」
    "c822": dict(
        t="もし起きていたら", s="上院が書いたこと",
        fig=("m26", dict(view="few_min", steps=[dict(state=dict(sen="on")), dict(state=dict(few="on")), dict(state=dict(pride="on"))],
                         rel=[dict(t="23:30", src="G1 p57")], note="部屋は模式（米国上院の報告の文は書き起こし・公式の写しは未照合）",
                         src=ss.src(["T3 p1", "G1 p57"])))),
    # c825（2行）＝1行目「審問のやり直しを求めた。だが退けられた」→ 2行目「正式な告発も…不服を申し立てる道も無かった」
    "c825": dict(
        t="閉ざされた道", s="船長が求めたこと",
        fig=("m26", dict(view="appeal", steps=[dict(state=dict(ask="on")), dict(state=dict(none="on"))],
                         note="流れは模式", src=ss.src(["G2 p2005"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-28）：写真・頁・NOAA の映像（第7章の18カット）＝書き方は c2.py の ⑤b-7 の注と同じ
# ══════════════════════════════════════════════════════════
_S3671, _S9674, _PG1005, _S3714, _PG1041, _S7594 = P("s3_671"), P("s9_674"), P("p_g1_005"), P("s3_714"), P("p_g1_041"), P("s7_594")
_PG1085, _S8625, _S10905, _S5362, _PG1060, _S3698 = P("p_g1_085"), P("s8_625"), P("s10_905"), P("s5_362"), P("p_g1_060"), P("s3_698")
_S9648, _S9645, _S3675, _S11716 = P("s9_648"), P("s9_645"), P("s3_675"), P("s11_716")
# 本の頁の写真（S5-362）＝写真の枠の内だけ（c318 と同じ切り口＝下の題と説明文は外）
_S5362_IN = (0.065, 0.065, 0.91, 0.835)
SPEC.update({
    # c801（3行）＝真ん中の人（シルクハット・x 0.55・顔 y 0.3）へ寄る（c636 は少しだけ）。⚠️ 3人のうち長が真ん中の人かは ⑤c で出どころの題と照らす
    "c801": dict(photo=_S3671, **ss.mv(_S3671, "in", fx=0.55, fy=0.35, z=1.4), side="none", color=1.0,
                 t="国の正式な調べ", s="英国の審問の長マージー卿〈1912年〉"),
    # c802（3行）＝壁の大きな模型（x 0.1〜0.35・y 0.55〜0.6）へ寄る（c629 は真ん中・c823 は下の札を左へ）
    "c802": dict(photo=_S9674, **ss.mv(_S9674, "in", fx=0.22, fy=0.57, z=1.6), side="none", color=1.0,
                 t="2万5,000をこえる問い", s="英国の審問の会場〈ロンドン・1912年〉"),
    # c803（2行）＝報告書 p.5 の審問の判断「The court, having carefully…」〜「…was being navigated.」
    #   切り口＝`pbox P-G1-005 "The court, having carefully" "was being navigated"`
    "c803": dict(photo=_PG1005, trim=(0.003, 0.522, 0.939, 0.616), panel=True, pw=1640, color=1.0,
                 t="速さの出しすぎ", s="船が失われたわけを述べた判断"),
    # c805（2行）＝c216 と同じ写真・同じ副題＝額の中の切り口を顔（x 0.12〜0.88・y 0.12〜0.70）に替える（静止）
    "c805": dict(photo=_S3714, trim=(0.12, 0.12, 0.88, 0.70), panel=True, ground=dict(photo=_S3714), color=1.0,
                 t="競争と人々の望み", s="タイタニック号の船長エドワード・スミス〈1912年4月の新聞の写真〉"),   # c216 と同じ副題（短くした）
    # c806（2行）＝報告書 p.41（束の段で頁の頭の2行＝会社の人の名前を外した「The evidence shows…」の段落）＝まるごと額装
    "c806": dict(photo=_PG1041, panel=True, pw=1640, color=1.0,
                 t="責められない間違い", s="船長の判断についての段落"),
    # c808（2行）＝右へ（ガラス乾板の左の黒い縁 3.0%＝流す始めの寄せ 0.33）
    "c808": dict(photo=_S7594, **ss.mv(_S7594, "r", span=(0.33, 0.8)), side="none", color=1.0,
                 t="足された問い", s="ニューヨークのピアのカルパチア号〈1912年4月20日・BnF〉"),
    # c809（2行）＝報告書 p.85 の問24 と答え「(b) The Californian. She could have reached…She made no attempt.」
    #   切り口＝`pbox P-G1-085 "What was the cause of the loss" "She made no attempt"`
    "c809": dict(photo=_PG1085, trim=(0.015, 0.200, 0.997, 0.4105), panel=True, pw=1640, color=1.0,
                 t="名指しされた船", s="問24 と答え"),
    # c811（3行）＝煙突とマスト（x 0.43・y 0.4）へ寄る
    "c811": dict(photo=_S8625, **ss.mv(_S8625, "in", fx=0.45, fy=0.42, z=1.4), side="none", color=1.0,
                 t="8発と8発", s="カリフォルニアン号〈カルパチア号の甲板から撮られたとみられる・NARA〉"),
    # c813（2行）＝NOAA 2004 の映像 57.5〜67.0秒（船首の横）
    "c813": dict(**ss.vid("c813", t="2時40分に消えた船", s="海の底のタイタニック号〈2004年・NOAA ほか〉"), side="none"),
    # c814（3行）＝c503 と同じ地図・同じ副題＝ほかの船の印（PARISIAN x 0.38 → VIRGINIAN・CARPATHIA → BALTIC x 0.92）を右へ
    "c814": dict(photo=_S10905, **ss.mvz(_S10905, (0.40, 0.70, 1.5), (0.80, 0.66, 1.5)), side="none", color=1.0,
                 t="ほかの船ではない", s="1912年の新聞の地図〈船の位置は当時の報道の見立て〉"),
    # c817（3行）＝c318 と同じ写真・同じ副題＝手前の氷原（切り口の中の y 0.62）に沿って右へ
    "c817": dict(photo=_S5362, **ss.tcam(_S5362, _S5362_IN, (0.35, 0.62, 1.2), (0.65, 0.62, 1.2)), side="none", color=1.0,
                 t="氷はまばらだった", s="氷原と氷山〈1912年4月・カルパチア号の乗客が撮ったと1912年の本は書く〉"),
    # c818（2行）＝報告書 p.60「When she first saw the rockets…」〜「…if not all of the lives that were lost.」
    #   切り口＝`pbox P-G1-060 "When she first saw the rockets" "lost."`
    "c818": dict(photo=_PG1060, trim=(0.054, 0.570, 0.981, 0.651), panel=True, pw=1640, color=1.0,
                 t="全員の命の可能性", s="助けに行けたとする一文"),
    # c819（2行）＝束の段でネガの上の字（議員の名）を外した写真＝顔（x 0.6・y 0.25）の側へ寄る。
    #   ガラス乾板の黒い縁（左 4.3%・上 3.5%）＝引いた側の寄り lo 1.11・寄った側の真ん中 y 0.40（上の縁に窓を当てない）
    "c819": dict(photo=_S3698, **ss.mv(_S3698, "in", fx=0.58, fy=0.40, z=1.25, lo=1.11), side="none", color=1.0,
                 t="米国も責めた", s="米国上院の小委員会の長〈LOC〉"),
    "c820": dict(photo=_S9648, **ss.mv(_S9648, "r", fy=0.4), side="none", color=1.0,
                 t="応えなかった船", s="米国上院の公聴会〈1912年4月・LOC〉"),
    # c821（3行）＝真ん中の机を囲む議員の席（x 0.5・y 0.35）へ寄る（c705 は右へ）
    "c821": dict(photo=_S9645, **ss.mv(_S9645, "in", fx=0.5, fy=0.35, z=1.6), side="none", color=1.0,
                 t="船長に重い責任", s="米国上院の公聴会〈1912年・英国の新聞の絵〉"),
    # c823（2行）＝下の席の札（「COUNSEL」「RESERVED」・y 0.84〜0.95）に沿って左へ
    "c823": dict(photo=_S9674, **ss.mv(_S9674, "l", fy=0.75, z=1.3), side="none", color=1.0,
                 t="名指しはしない", s="英国の審問の会場〈ロンドン・1912年〉"),
    # c824（1行）＝c601・c622 と別の動き＝体から顔へ上がる
    "c824": dict(photo=_S3675, **ss.mv(_S3675, "u", fx=0.58, z=1.4), side="none", color=1.0,
                 t="船長への非難", s="カリフォルニアン号の船長スタンリー・ロード〈1912年5月・英国の審問のころ〉"),
    # c826（1行）＝正方形（全面の窓は縦 56%）＝左下の浴槽（y 0.65〜0.85）から上へ
    "c826": dict(photo=_S11716, **ss.mv(_S11716, "u"), side="none", color=1.0,
                 t="残った結論", s="海の底の船長室の浴槽〈2003年・NOAA ほか〉"),
})
