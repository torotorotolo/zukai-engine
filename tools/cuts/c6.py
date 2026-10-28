# -*- coding: utf-8 -*-
"""第5章　カリフォルニアン号の甲板で c601–c641（41カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c6.py`）。
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
    'c601': dict(kind='写真',
               plan='🔧 S3-675:全体｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号の船長スタンリー・ロード〈1912年5月・英国の審問のころ〉｜動き：寄る｜権利：PD｜時期：後・審問｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S3-675 は4回まで（c601・c622・c824・cb01）｜新しい画（映像方針）：🔧 額装 → 全面（1906px の横長）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`the steamship Californian, of the Leyland Line, Mr. Stanley Lord, master`）'),
    'c602': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：氷原の手前で止まる船（機関を逆に・北と南に続く氷原）｜合図：🔁 正面→上から（前の図 c516）｜新しい画（映像方針）：台本どおり（地図ではない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`obliged to stop and reverse engines`…`she was running into field ice, which stretched as far as could then be seen to the northward and southward`）'),
    'c603': dict(kind='文字の頁',
               plan='P-G1-056:位置｜一覧の種類：頁｜見せ方：頁｜副題：英国の審問の報告 p.56｜動き：寄る（「I am satisfied that this position is not accurate」の一文へ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：英国の審問の報告（米国上院の刷り直し S. Doc. 933）p.56｜書き起こしの断り：札の緯度経度は英国の審問の書き起こし（有志のサイト）による｜新しい画（映像方針）：台本どおり（船長の位置の札を添える）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`fixed by dead reckoning and verified by observations`…`I am satisfied that this position is not accurate`）・T1 Day 7 Q6704（書き起こし `Forty-two deg five min N, and 50 deg 7 min. W`）'),
    'c604': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：推測の位置と海の流れに押された位置が離れていく矢印｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`It is a position about 19 miles N. by E. of the position of the`…`when he foundered`）・G2 p.9（`a current setting about south by west`…`existed in the area of the accident`）'),
    'c605': dict(kind='写真',
               plan='🔧 S8-625:船尾｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号〈カルパチア号の甲板から撮られたとみられる・NARA〉｜動き：左へ（船尾から船首へ）｜権利：PD｜時期：後・救助｜人：なし｜出典の行：出典：米国立公文書館（NARA）｜新しい画（映像方針）：🔧 S8-E03 → S8-625 の別の寄り（S8-E03 を3回までにする）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`she remained approximately stationary until 5.15`…`The ship was slowly swinging around to starboard during the night`）'),
    'c606': dict(kind='再現イラスト',
               plan='一覧の種類：案C-1｜見る向き：横から｜見た目の型：カリフォルニアン号の船橋・夜11時ごろ・東から近づく船の灯・三等航海士の影｜合図：🔁 上から→横から（前の図 c604）｜新しい画（映像方針）：台本どおり（遠くの船の形は描き分けない・タイタニック号と名乗らない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.57（`At about 11 p. m. a steamer's light was seen approaching from the eastward`）"),
    'c607': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：舷灯の色（右に緑・左に赤・マストに白）と見る人の目｜合図：🔁 横から→上から（前の図 c606）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.57（`and also her green side light`…`at some time between 11 and 11.30 he first saw her green light; she was then about 5 miles`）'),
    'c608': dict(kind='写真',
               plan='S3-749:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：スタンリー・ロード〈1908年・別の船の船長だったころ〉｜動き：静止｜権利：PD｜時期：別の年｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S3-749 は3回まで（c608・c624・c934）｜新しい画（映像方針）：台本どおり（縦長・小さい＝高さいっぱいの額・静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.57（`He noticed that about 11.30 she stopped`…`something like ourselves`）'),
    'c609': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：マストの灯が1つの船と2つの船を並べる｜合図：🔁 上から→正面（前の図 c607）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.57（`Mr. Groves made out two masthead lights`…`She is evidently a passenger steamer`）'),
    'c610': dict(kind='フリー素材',
               plan='X-ship-lights｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 7.51秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜の海の遠い船の灯り｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：機関部の乗組員は役職だけ（承認①）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.57（`who was on deck at midnight, said, referring to this steamer`…`It could not have been anything but a passenger boat, she was too large`）'),
    'c611': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：モールス灯の短い光と長い光｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.57（`Call her up on the Morse lamp, and see if you can get any answer`）'),
    'c612': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見る向き：横から｜見た目の型：2人の見立て（船長「客船には見えない」・三等航海士「客船です」）と、止まると灯りが消えたように見える灯りの列｜合図：🔁 正面→横から（前の図 c611）｜新しい画（映像方針）：🔧 S8-630 の2回目 → 模式（語りは2人の見立ての違い＝写真の使い回しを減らす）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.57（`That does not look like a passenger steamer`…`It is, sir. When she stopped her lights seemed to go out`）'),
    'c613': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：時間の線｜見た目の型：3つの当直と、交代の前の1つの鐘｜合図：🔁 横から→時間の線（前の図 c612）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.57（`Mr Groves states that these lights went out at 11.40`…`because one bell was struck to call the middle watch`）'),
    'c614': dict(kind='再現イラスト',
               plan='🔧 一覧の種類：案C-1｜見る向き：横から｜見た目の型：同じ船橋・0時すぎ・三等航海士のモールス灯に答えなし・二等航海士が上がってくる影｜合図：🔁 時間の線→横から（前の図 c613）｜新しい画（映像方針）：🔧 S8-625 の3回目 → 案C-1（c615 と1つの場面で続ける）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.58（`Mr. Groves's Morse signaling appears to have been ineffectual`…`he gave it up`…`relieved by Mr. Stone, the second officer, just after midnight`）"),
    'c615': dict(kind='再現イラスト',
               plan='🔧 一覧の種類：続き｜見た目の型：（c614 の続き）｜新しい画（映像方針）：🔧 案C-1 の2回目 → c614 の絵の続き（三等航海士が遠くの止まった船の灯りを指さして引き継ぐ）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.58（`she has been stopped since 11.40`…`At about the moment she stopped she`）'),
    'c616': dict(kind='写真',
               plan='🔧 S2-E01:全体｜一覧の種類：実写｜見せ方：全面｜副題：1912年の船の無線室〈姉妹船オリンピック号・1912年の本の写真〉｜動き：寄る（ヘッドホンへ）｜権利：PD｜時期：別の船｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜注：S2-E01 は ca01 と2回（同じ副題）｜新しい画（映像方針）：🔧 副題で「1912年の船の無線室」と断る（カリフォルニアン号の無線室ではない）・額装 → 全面｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='T1 Day 8 Q8289・Q8285（書き起こし `between 12.15 and 12.20`・`Nothing at all`）'),
    'c617': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：方位（羅針盤の目盛りと相手の船の向き）｜合図：🔁 横から→上から（前の図 c614）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.58（`pointed out the steamer to him with instructions to tell him if her bearings altered or if she got any closer`）'),
    'c618': dict(kind='再現イラスト',
               plan='一覧の種類：案C-7｜見る向き：横から｜見た目の型：カリフォルニアン号の船橋・0時20分ごろ・双眼鏡の見習い・マストの白い灯と赤い舷灯と甲板の灯りの群れ｜合図：🔁 上から→横から（前の図 c617）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.58（`an apprentice named Gibson, whose attention was`…`to the steamer's lights at about 12.20 a. m.`…`glare of white lights on her afterdeck`）"),
    'c619': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：モールスの光とただの瞬きを並べる｜合図：🔁 横から→正面（前の図 c618）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.58（`He first thought her masthead light was flickering and next thought it was a Morse light`…`finally came to the conclusion that it was, as he had first supposed, the masthead light flickering`）'),
    'c620': dict(kind='図解',
               plan='一覧の種類：断面｜見る向き：横から｜見た目の型：カリフォルニアン号の前の断面（船橋とその下の海図室・伝声管）｜合図：🔁 正面→横から（前の図 c619）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.58（`Sometime after 12.30 a. m.`…`states that he saw two rockets fired from the ship which he had been observing, and about 1.10 a. m., Mr. Stone reported to the captain by voice pipe, that he had seen five white rockets from the direction of the steamer`）'),
    'c621': dict(kind='再現イラスト',
               plan='一覧の種類：案C-2｜見る向き：横から｜見た目の型：海図室・1時10分ごろ・横になる船長の影・伝声管の口｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`remembered Gibson opening and closing the chart-room door`・`he went down to the chart room`）・T1 Day 7 Q6784（書き起こし `just below the upper bridge`）'),
    'c622': dict(kind='写真',
               plan='S3-675:顔｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号の船長スタンリー・ロード〈1912年5月・英国の審問のころ〉｜動き：寄る（顔へ）｜権利：PD｜時期：後・審問｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（2回目・顔に寄る）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.58（`Are they company's signals`…`I do not know, but they appear to me to be white rockets`）"),
    'c623': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：会社ごとの夜の合図の光と、遭難の信号を並べる｜合図：🔁 横から→正面（前の図 c621）｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="T1 Day 28 Q25394（書き起こし `White Star Company's night signal`）・G2 p.14（`it has been suggested that these were Company signals from the other ship`）"),
    'c624': dict(kind='写真',
               plan='🔧 S3-749:顔｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：スタンリー・ロード〈1908年・別の船の船長だったころ〉｜動き：静止｜権利：PD｜時期：別の年｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 S8-625 の4回目 → 船長の写真（語り＝船長の言葉）・額の中の寄りを替える（静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.58（`The master told him to go on Morsing, and, when he received any information, to send the apprentice down to him with it`）・G2 p.15（`no action was taken save to make further attempts to raise her with the morse lamp`）'),
    'c625': dict(kind='再現イラスト',
               plan='一覧の種類：案C-7｜見る向き：横から｜見た目の型：同じ船橋・見習いがモールス灯で呼ぶ・その船の上に低く白い信号弾が3発（数えられる形）｜合図：🔁 正面→横から（前の図 c623）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.58（`This witness thinks the time was 12.55`…`He got no reply, but the vessel fired three more white rockets; these rockets were also seen by Mr. Stone`）'),
    'c626': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：信号弾の高さ（マストの灯の半分くらい・遠いと低く見える）｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="T1 Day 7 Q7921（書き起こし `they were only about half the height of the steamer's masthead light`）・G2 p.13（`described as low-lying (quoted as rising to less than mast-head height)`）"),
    'c627': dict(kind='再現イラスト',
               plan='🔧 一覧の種類：案C-8｜見る向き：横から｜見た目の型：カリフォルニアン号の船橋・1時から1時40分・双眼鏡の2人の影・遠くの灯りが変に見える｜新しい画（映像方針）：🔧 S8-E03 の3回目 → 案C-8（記録＝G1 p.58「Look at her now…her lights look queer」）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.58（`Between 1 o'clock and 1.40 some conversation passed between them`…`Look at her now, she looks very queer out of water, her lights look queer`）"),
    'c628': dict(kind='文字の頁',
               plan='P-G1-058｜一覧の種類：頁｜見せ方：頁｜副題：英国の審問の報告 p.58｜動き：寄る（「A ship is not going to fire rockets at sea for nothing」の行へ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：英国の審問の報告（米国上院の刷り直し S. Doc. 933）p.58｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.58（`A ship is not going to fire rockets at sea for nothing`…`admits himself that he may possibly have used that expression`）'),
    'c629': dict(kind='写真',
               plan='🔧 S9-674:全体｜一覧の種類：実写｜見せ方：全面｜副題：英国の審問の会場〈ロンドン・1912年〉｜動き：寄る｜権利：PD｜時期：後・審問｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜注：打ち方（1発ずつ・短い間）は c516・ca10 の模式と語りで足りる。S9-674 は3回まで（c629・c802・c823）｜新しい画（映像方針）：🔧 模式（打ち方の目盛り）→ 英国の審問の会場（語り＝のちの審問で認めた・写真の無い画面が6つ続くのを切る）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='T1 Day 7 Q8033（書き起こし `I knew that rockets shown at short intervals, one at a time, meant distress signals, yes`）・Q8034（書き起こし `that those rockets were signals of distress?`…`No.`）・Q7993（書き起こし `I did not think the ship was in distress at the time.`）'),
    'c630': dict(kind='再現イラスト',
               plan='一覧の種類：案C-2｜見る向き：横から｜見た目の型：海図室・2時5分ごろ・戸が開いて見習いの影・横になった船長の影｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.58（`he saw the last of the rockets fired at about 1.40, and after watching the steamer for some 20 minutes more he sent Gibson down to the master`…`altogether we had seen eight of these white lights like white rockets`）・G1 p.59（`that this steamer was disappearing in the southwest`）'),
    'c631': dict(kind='再現イラスト',
               plan='🔧 一覧の種類：続き｜見た目の型：（c630 の続き）｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜新しい画（映像方針）：🔧 S3-675 の3回目 → c630 の絵の続き（船長が「全部白か」と時刻を聞く＝記録 G1 p.59）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`the master asked him if all the rockets were white, and also asked him the time`…`Gibson stated that at this time the master was awake. It was five minutes past two`）・T1 Day 7 Q7565（書き起こし `Five minutes past two by the wheelhouse clock`）'),
    'c632': dict(kind='再現イラスト',
               plan='一覧の種類：案C-8｜見る向き：横から｜見た目の型：同じ船橋・2時すぎ・南西の遠い灯りがだんだん消えていく・双眼鏡の2人の影｜新しい画（映像方針）：台本どおり（c627 と時刻の札を替える）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`A gradual disappearing of all her lights, which would be perfectly natural with a ship steaming away from us`）'),
    'c633': dict(kind='再現イラスト',
               plan='🔧 一覧の種類：案C-9｜見る向き：横から｜見た目の型：カリフォルニアン号の船橋・2時40分ごろ・伝声管の口の前に立つ二等航海士の影・「南西に消えた」の札｜注：🆕 了承②（案C の場面を1つ足す）｜新しい画（映像方針）：🔧 模式（方位の目盛り）→ 案C-9（記録＝G1 p.59「Stone again called up the master by voice pipe」）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`At about 2.40 a. m. Mr`…`Stone again called up the master by voice`…`I again assured him they were all white, just white`）'),
    'c634': dict(kind='図解',
               plan='一覧の種類：並べ｜見る向き：正面｜見た目の型：2人の記憶の2列（二等航海士・船長）｜合図：🔁 横から→正面（前の図 c633）｜新しい画（映像方針）：台本どおり（札は「カリフォルニアン号の時計」）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`considerable discrepancy between the evidence of Mr. Stone and that of the master`…`he went to the voice pipe at about 1.15, but was told then of a white rocket (not five white rockets)`）'),
    'c635': dict(kind='文字の頁',
               plan='P-G1-059｜一覧の種類：頁｜見せ方：頁｜副題：英国の審問の報告 p.59｜動き：寄る（「considerable discrepancy」の段落へ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：英国の審問の報告（米国上院の刷り直し S. Doc. 933）p.59｜注：語りは G1 p.59 の事実だけ（書き起こしの「half awake」は語らない）＝断りは要らない｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`between 1.30 and 4.30, when`…`he had no recollection of anything being reported to him at`…`although he remembered Gibson opening and closing the chart-room door`）・T1 Day 7 Q7288（書き起こし `I very likely was half awake`）'),
    'c636': dict(kind='写真',
               plan='🔧 S3-671:全体｜一覧の種類：実写｜見せ方：全面｜副題：英国の審問の長マージー卿〈1912年〉｜動き：寄る｜権利：PD｜時期：後・審問｜人：公的な任務（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S3-671 は c801 と2回（同じ副題）｜新しい画（映像方針）：🔧 S8-E03 の4回目 → 英国の審問の長（語り＝英国の報告書が食い違いを書いた）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`There are contradictions and inconsistencies in the story as told by the different witnesses`）'),
    'c637': dict(kind='図解',
               plan='一覧の種類：帯｜見る向き：時間の線｜見た目の型：カリフォルニアン号の時計の夜の帯（10:20ごろ〜2:40ごろ・〈二等航海士の話〉の札）｜合図：🔁 正面→時間の線（前の図 c634）｜注：c416 の帯と色と並びを替える｜新しい画（映像方針）：台本どおり（1:10ごろ と 2:40ごろ に〈二等航海士の話〉の札＝台本 §0-5・タイタニック号の時刻は並べない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56〜59（`until 10.20`・`went out at 11.40`・`about 1.10 a. m.`・`at about 1.40`・`five minutes past two`・`At about 2.40 a. m.`）・G1 p.59（`He, however, had the wireless operator called`）・G7 p.740（`When were you awakened`…`About 3.30 a. m.`…`New York time`…`And who awakened you`…`The chief officer`）'),
    'c638': dict(kind='フリー素材',
               plan='🔧 X-dawn｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 10.16秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜明け前の海｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：⑤b で1本ずつ（月なし）｜新しい画（映像方針）：🔧 S8-625 の5回目 → イメージ（語り＝4時と4時半）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`Mr. Stewart relieved Mr. Stone at 4 a. m.`…`At 4.30 he called the master and informed him that Mr. Stone had told him he had seen rockets in the middle watch. The master said, Yes, I know; he has been telling me`）'),
    'c639': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：朝4時ごろの新しい船（マストの白い灯2つ）と前の船を並べる｜合図：🔁 時間の線→横から（前の図 c637）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`a steamer came in sight with two white masthead lights`…`apparently took the fresh steamer for the one which had fired rockets, and said, She looks all right; she is not making any signals now. This mistake was not corrected`）'),
    'c640': dict(kind='写真',
               plan='🔧 S8-630:船首｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号〈1907年〉｜動き：寄る（船首へ）｜権利：PD｜時期：別の年｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 S8-E03 の5回目 → S8-630 の別の寄り（語り＝全速で氷原へ）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`He, however, had the wireless operator called. At about`…`a. m. Capt. Lord heard from the Virginian that the`…`Titanic had struck a berg, passengers in boats, ship sinking`…`he at once started through the field ice at full speed for the position`）'),
    'c641': dict(kind='写真',
               plan='S6-480:帆のボート｜一覧の種類：実写｜見せ方：全面｜副題：4月15日の朝、海の上のボート〈1912年・BnF〉｜動き：寄る（帆を張ったボートへ）｜権利：PD｜時期：後・救助｜人：遠景（⑤b で原寸）｜出典の行：出典：フランス国立図書館（BnF）｜注：S6-480 は3回まで（c104・c641・cb04）｜新しい画（映像方針）：台本どおり（2回目・別の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.60（`At 2.20 a. m. the Titanic had foundered`）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-10-27）：フリー素材（Pexels・イメージ）＝`ss.vid`（見出し・副題は書かない＝左上の「イメージ」と出典だけ）。
#   区間（c610＝船がいちばん遠い頭）は `qa_out/ep26_assets.py` の STOCK_WINDOW → footage.USE
SPEC.update({
    "c610": ss.vid("c610"),
    "c638": ss.vid("c638"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-27）：案C-1・7・8・9 カリフォルニアン号の船橋＝K1／案C-2 海図室＝K2（`tools/illu26.py`・門番 check_illu ㊽）
#  🔴 遠くの船は灯の点だけ（形を描かない・タイタニック号と名乗らない）・人は顔の無い影と役職の札だけ・心の中は描かない
# ══════════════════════════════════════════════════════════
_P58 = "G1 p58（Mr. Stone had with him during the middle watch an apprentice）"
_PIPE58 = "G1 p58（Mr. Stone reported to the captain by voice pipe）"
_PIPE59 = "G1 p59（At about 2.40 a. m. Mr. Stone again called up the master by voice pipe）"
SPEC.update({
    # c606（2行・6.7秒）＝1行目の問い → 2行目「夜11時ごろ、東の方から、近づいてくる船の灯りが見えた。」で遠くに灯（段3で近づく）と時計の札
    "c606": dict(fig=("illu", dict(
        place="K1", start=dict(kg="stand", ksw="side"), at="23:00",
        rec="G1 p57（Mr. Groves, third officer of the Californian, who was the officer of the first watch）",
        people=dict(crew=(1, "G1 p57（it would appear that the master was not actually on the bridge when the steamer was sighted）")),
        steps=[dict(state=dict(), tag=dict(t="三等航海士", at="A", off=(50, -50), keep=True)),
               dict(state=dict(kship="far"), rec="G1 p57（At about 11 p. m. a steamer's light was seen approaching from the eastward）",
                    tag=dict(t="23:00ごろ（カリフォルニアン号の時計）", xy=(640, 210), keep=True)),
               dict(state=dict(kship="near"), dur=2.2, rec="G1 p57（the steamer was changing her bearing slowly as she got closer）")]))),
    # c614（2行・8.5秒）＝1行目「三等航海士のモールス灯に、答えは無かったようだ。」で腕を上げて灯が点いたり消えたり →
    #   2行目「0時すぎ、当直は、…二等航海士…に替わった。」で腕を下ろし、二等航海士が階段から上がってくる・時計の札
    "c614": dict(fig=("illu", dict(
        place="K1", start=dict(kg="stand", kship="stop", ksw="side"), at="0:00",
        rec="G1 p57（Her steaming lights were still visible and also her port side light）",
        people=dict(crew=(2, "G1 p58（He remained on the bridge until relieved by Mr. Stone, the second officer, just after midnight）")),
        steps=[dict(state=dict(kgarm="lamp", klamp="blink"), rec="G1 p58（Mr. Groves's Morse signaling appears to have been ineffectual）",
                    tag=dict(t="三等航海士", at="A", off=(50, -50), keep=True)),
               dict(state=dict(kgarm="down", klamp="off", ks="up"),
                    rec="G1 p58（He remained on the bridge until relieved by Mr. Stone, the second officer, just after midnight）",
                    tag=[dict(t="0:00すぎ（カリフォルニアン号の時計）", xy=(640, 210), keep=True),
                         dict(t="二等航海士", at="B", off=(50, -50), delay=2.8, keep=True)])]))),
    # c615（1行・4.4秒）＝c614 の絵の続き。「三等航海士は、引き継ぎで、止まっている客船だ、と伝えた。」で遠くの灯を指さす
    "c615": dict(fig=("illu", dict(
        place="K1", start=dict(kg="stand", ks="stand", kship="stop"), at="0:00",
        rec="G1 p58（relieved by Mr. Stone, the second officer, just after midnight）",
        people=dict(crew=(2, "G1 p58（In turning the Californian over to him, he pointed out the steamer）")),
        steps=[dict(state=dict(kgarm="point"), rec="G1 p58（In turning the Californian over to him, he pointed out the steamer and said: she has been stopped since 11.40）",
                    tag=[dict(t="三等航海士", at="A", off=(50, -50), keep=True), dict(t="二等航海士", at="B", off=(50, -50), keep=True)])]))),
    # c618（2行・9.2秒）＝1行目「二等航海士と当直に立ったのは、見習い…」で2人の札 → 2行目「0時20分ごろ、その船のマストの灯と赤い舷灯、
    #   後ろの甲板の白い灯りの群れを見た。」で時計の札と灯の3つの札（見習いは双眼鏡＝with glasses）
    "c618": dict(fig=("illu", dict(
        place="K1", start=dict(ks="stand", kj="binoc", kship="glare", ksw="side"), at="0:20",
        rec="G1 p58（He could see a masthead light, her red light (with glasses), and a glare of white lights on her afterdeck）",
        people=dict(crew=(2, _P58)),
        steps=[dict(state=dict(), rec=_P58,
                    tag=[dict(t="見習い", at="A", off=(50, -50), keep=True), dict(t="二等航海士", at="B", off=(50, -50), keep=True)]),
               dict(state=dict(), rec="G1 p58（whose attention was first drawn to the steamer's lights at about 12.20 a. m.）",
                    tag=[dict(t="0:20ごろ（カリフォルニアン号の時計）", xy=(640, 210), keep=True),
                         dict(t="マストの灯", at="mast", off=(40, -90)), dict(t="赤い舷灯", at="red", off=(-30, 120), anchor="end"),
                         dict(t="白い灯りの群れ", at="glare", off=(60, 110))])]))),
    # c621（2行・7.5秒）＝1行目「伝声管って、何？」で管の札 → 2行目「管を通して、声を別の部屋に届ける道具だ。船長は、船橋の下の海図室にいた。」
    #   で管の口から輪・船長の札・上の船橋への札。時計の札は出さない（1:10 は船長の話 1:15 と割れる＝ss.ILLU_SPLIT_TIMES）
    "c621": dict(fig=("illu", dict(
        place="K2", at="1:10",
        people=dict(crew=(1, "T1 p7280（書き起こし I do not know; I was asleep）")),
        steps=[dict(state=dict(), tag=dict(t="伝声管", at="pipe", off=(60, -40), keep=True)),
               dict(state=dict(), rings_in=2, rec="G1 p58（Mr. Stone reported to the captain by voice pipe）・T1 p6784（書き起こし just below the upper bridge）",
                    tag=[dict(t="船長", at="cap", off=(-60, -70), anchor="end"), dict(t="上の船橋へ", at="pipe_up", off=(60, 20))])]))),
    # c625（2行・9.1秒）＝1行目「見習いはモールス灯で、もう一度呼んだ。答えは無い。だがその船から、」で腕を上げて灯が点いたり消えたり →
    #   2行目「さらに3発、白い信号弾が上がった。二等航海士も見ている。」で低い白い信号弾が3発（数えられる形）
    "c625": dict(fig=("illu", dict(
        place="K1", start=dict(ks="binoc", kj="stand", kship="glare", ksw="side"), at="0:55",
        rec="G1 p58（Both Mr. Stone and the apprentice kept the steamer under observation, looking at her from time to time with their glasses）",
        people=dict(crew=(2, _P58)),
        steps=[dict(state=dict(kjarm="lamp", klamp="blink"), rec="G1 p58（he at once proceeded again to call the steamer up by Morse）",
                    tag=dict(t="見習い", at="A", off=(50, -50), keep=True)),
               dict(state=dict(klamp="off", kflares="on"), rec="G1 p58（He got no reply, but the vessel fired three more white rockets; these rockets were also seen by Mr. Stone）",
                    tag=[dict(t="白い信号弾 3発", at="flares", off=(60, -80), delay=2.4), dict(t="二等航海士", at="B", off=(50, -50))])]))),
    # c627（3行・12.2秒）＝1行目「1時から1時40分のあいだ、2人は双眼鏡で見ながら話した。」で時計の札と2人の札（2行目・3行目の言葉は語りに任せる）
    "c627": dict(fig=("illu", dict(
        place="K1", start=dict(ks="binoc", kj="binoc", kship="glare"), at="1:00",
        rec="G1 p58（Both Mr. Stone and the apprentice kept the steamer under observation, looking at her from time to time with their glasses）",
        people=dict(crew=(2, _P58)),
        steps=[dict(state=dict(), rec="G1 p58（Between 1 o'clock and 1.40 some conversation passed between them）",
                    tag=[dict(t="1:00〜1:40（カリフォルニアン号の時計）", xy=(640, 210), keep=True),
                         dict(t="見習い", at="A", off=(50, -50), keep=True), dict(t="二等航海士", at="B", off=(50, -50), keep=True)])]))),
    # c630（3行・14.0秒）＝1行目「…最後の信号弾を見たのは、1時40分ごろ。」は海図室の船長 → 2行目「その20分ほどあと、見習いを船長のもとへ行かせた。」で
    #   戸が開いて見習い → 3行目「全部で8発…南西へ消えていく、と。」で見習いから輪。時計の札は出さない（2:00 と 2:05 で割れる＝c631 で見習いの話として）
    "c630": dict(fig=("illu", dict(
        place="K2", at="2:05",
        people=dict(crew=(2, "G1 p58（after watching the steamer for some 20 minutes more he sent Gibson down to the master）")),
        steps=[dict(state=dict(), tag=dict(t="船長", at="cap", off=(-60, -70), anchor="end", keep=True)),
               dict(state=dict(k2door="open"), rec="G1 p59（although he remembered Gibson opening and closing the chart-room door）",
                    tag=dict(t="見習い", at="app", off=(-140, 0), anchor="end", delay=1.3, keep=True)),   # 🔧 geom_gap：戸の枠にかかった＝枠の左へ
               dict(state=dict(), rings=2, rec="G1 p58（altogether we had seen eight of these white lights like white rockets in the direction）・"
                                                "G1 p59（that this steamer was disappearing in the southwest）")]))),
    # c631（3行・10.2秒）＝c630 の絵の続き。2行目「全部白かと聞かれ、時刻も聞かれた。」で船長の問いの印 → 3行目「2時5分。操舵室の時計だった、
    #   と見習いは言う。」で札（見習いの話＝書き起こし Q7565）
    "c631": dict(fig=("illu", dict(
        place="K2", start=dict(k2door="open"), at="2:05",
        rec="G1 p59（Gibson states that he went down to the chart room and told the master）",
        people=dict(crew=(2, "G1 p59（Gibson states that he went down to the chart room and told the master）")),
        steps=[dict(state=dict(), tag=[dict(t="船長", at="cap", off=(-60, -70), anchor="end", keep=True),
                                       dict(t="見習い", at="app", off=(-140, 0), anchor="end", keep=True)]),
               dict(state=dict(), asks=2, rec="G1 p59（the master asked him if all the rockets were white, and also asked him the time）"),
               dict(state=dict(), rec="T1 p7565（書き起こし Five minutes past two by the wheelhouse clock）・G1 p59（It was five minutes past two）",
                    tag=dict(t="2:05（見習いの話・操舵室の時計）", xy=(640, 210), keep=True))]))),
    # c632（2行・8.6秒）＝海図室から船橋へ（切り替えの字「船橋では」）。1行目「2人は、その船が見えなくなるまで見ていた。…」から遠くの灯が
    #   だんだん消えていく（2行目の終わりまで）
    "c632": dict(fig=("illu", dict(
        place="K1", start=dict(ks="binoc", kj="binoc", kship="glare", ksw="bridge"), at="2:05",
        rec="G1 p59（They both continued to keep the ship under observation until she disappeared）",
        people=dict(crew=(2, "G1 p59（Gibson returned to the bridge to Mr. Stone and reported）")),
        steps=[dict(state=dict(kship="fade"), dur=6.5, rec="G1 p59（A gradual disappearing of all her lights, which would be perfectly natural with a ship steaming away from us）",
                    tag=[dict(t="見習い", at="A", off=(50, -50), keep=True), dict(t="二等航海士", at="B", off=(50, -50), keep=True)])]))),
    # c633（2行・11.9秒）＝1行目「二等航海士の話では、2時40分ごろ、また伝声管で伝えた。あの船は南西に消えた。」で時計の札・伝声管へ輪・
    #   見えなくなった方角の札 → 2行目「船長は、灯りに色は無かったか、と聞いた。全部白でした。…」（言葉は語りに任せる）
    "c633": dict(fig=("illu", dict(
        place="K1", start=dict(ks="pipe", kship="gone"), at="2:40",
        rec="G1 p59（had disappeared bearing SW.）",
        people=dict(crew=(1, _PIPE59)),
        steps=[dict(state=dict(), rings=2, rec=_PIPE59,
                    tag=[dict(t="2:40ごろ（カリフォルニアン号の時計）", xy=(640, 210), keep=True),
                         dict(t="二等航海士", at="P", off=(-50, -50), anchor="end", keep=True),
                         dict(t="見えなくなった方角：南西", at="sw", off=(40, -110), keep=True)]),
               # 🔧 試し焼き 40594842436：左上の「伝声管」が「二等航海士」の札に接した＝右上（操舵室の屋根の下）へ
               dict(state=dict(), rec="G1 p59（the master again asked him if he was certain there was no color in the lights）",
                    tag=dict(t="伝声管", at="pipe", off=(40, -170)))]))),
})

# 🆕 ⑤b-5（2026-10-28）：図解（`tools/mech26.py`・fig=("m26", …)）。段の数＝語りの行の数・画面の数は全部 rel に（門番 check_mech の judge_m26）
SPEC.update({
    # c602（2行）＝1行目「夜10時20分ごろ…機関を逆に回して止まった」→ 2行目「氷原は、北にも南にも、見える限り」
    "c602": dict(
        t="行く手をふさぐ氷", s="カリフォルニアン号は止まった",
        fig=("m26", dict(view="field", steps=[dict(state=dict(stop="on")), dict(state=dict(ice="on"))],
                         rel=[dict(t="22:20ごろ", src="G1 p56")], note="船と氷原の形は模式", src=ss.src(["G1 p56"])))),
    # c604（3行）＝1行目「当時タイタニック号が沈んだとされた位置の、」→ 2行目「約35キロ（19マイル）北…推測の位置は、」→ 3行目「海の流れなどで、ずれる」
    "c604": dict(
        t="止まった位置", s="報告書が記した数",
        fig=("m26", dict(view="drift", steps=[dict(state=dict(pts="on")), dict(state=dict(dist="on")), dict(state=dict(cur="on"))],
                         rel=[dict(t="約35キロ（19マイル）", src="G1 p56")],
                         note="位置と流れは模式（流れの向きは南微西＝1992年の調べ直し）", src=ss.src(["G1 p56", "G2 p2013"])))),
    # c607（3行）＝1行目「船長は、甲板の灯りと、緑の舷灯を見た」→ 2行目「右側が緑、左側が赤…色で船の向きが分かる」→ 3行目「11時から11時半…約9キロ（5マイル）」
    "c607": dict(
        t="緑の灯", s="舷灯のしくみ",
        fig=("m26", dict(view="sidelights", steps=[dict(state=dict(green="on")), dict(state=dict(two="on")), dict(state=dict(seen="on"))],
                         rel=[dict(t="約9キロ（5マイル）", src="G1 p57"), dict(t="23:00〜23:30", src="G1 p57")],
                         note="船の形と灯の見える範囲は模式", src=ss.src(["G1 p57"])))),
    # c609（2行）＝1行目「三等航海士…の見方は違った」→ 2行目「マストの灯が2つ見えた。明らかに客船だ、と船長に伝えた」
    "c609": dict(
        t="もう1つの見方", s="当直の航海士",
        fig=("m26", dict(view="masts2", steps=[dict(state=dict(who="on")), dict(state=dict(two="on"))],
                         rel=[dict(t="マストの灯 1つ・2つ", src="G1 p57")], note="船の形と灯の高さは模式", src=ss.src(["G1 p57"])))),
    # c611（1行）＝「モールス灯で呼んで、答えがあるか見てみよ」
    "c611": dict(
        t="呼んでみよ", s="船長の指示",
        fig=("m26", dict(view="morse", steps=[dict(state=dict(call="on"))], rel=[], note="光の長さと並びは模式", src=ss.src(["G1 p57"])))),
    # c612（3行）＝1行目「船長は…客船には見えない、と言った」→ 2行目「客船です。止まったとき、灯りが消えたように」→ 3行目「見立てが違った」
    "c612": dict(
        t="2人の見立て", s="船橋でのやりとり",
        fig=("m26", dict(view="views2", steps=[dict(state=dict(a="on")), dict(state=dict(b="on")), dict(state=dict(diff="on"))],
                         rel=[], note="灯りの列は模式", src=ss.src(["G1 p57"])))),
    # c613（2行）＝1行目「灯りが消えたのは11時40分、と三等航海士は覚えている」→ 2行目「真夜中からの当直を起こす、1つの鐘」
    "c613": dict(
        t="覚えていた時刻", s="鐘の合図",
        fig=("m26", dict(view="watches", steps=[dict(state=dict(out="on")), dict(state=dict(bell="on"))],
                         rel=[dict(t="23:40", src="G1 p57"), dict(t="0:00", src="G1 p58"), dict(t="4:00", src="G1 p59"), dict(t="鐘1つ", src="G1 p57")],
                         note="横は時刻に比例（外の端の時刻は出さない）", src=ss.src(["G1 p57", "G1 p58", "G1 p59"])))),
    # c617（2行）＝1行目「方位が変わるか、近づいてきたら知らせよ」→ 2行目「方位とは、自分の船から見た、相手の向き」
    "c617": dict(
        t="方位とは", s="船長が二等航海士に",
        fig=("m26", dict(view="bearing", steps=[dict(state=dict(watch="on")), dict(state=dict(mean="on"))],
                         rel=[], note="羅針盤と船の位置は模式", src=ss.src(["G1 p58"])))),
    # c619（2行）＝1行目「見習いは一度、灯の瞬きをモールスかと思って答えたが、」→ 2行目「ただの瞬きだと考え直した」
    "c619": dict(
        t="モールスか、瞬きか", s="見習いの見立て",
        fig=("m26", dict(view="flicker", steps=[dict(state=dict(think="on")), dict(state=dict(fix="on"))],
                         rel=[], note="光の並びは模式", src=ss.src(["G1 p58"])))),
    # c620（2行）＝1行目「0時30分すぎには、機関室の乗組員が、信号弾を2発」→ 2行目「1時10分ごろ、伝声管で船長に…白い信号弾が5発」
    "c620": dict(
        t="真夜中すぎの信号弾", s="知らせはどう伝わったか",
        fig=("m26", dict(view="section", steps=[dict(state=dict(two="on")), dict(state=dict(pipe="on"))],
                         rel=[dict(t="0:30すぎ", src="G1 p58"), dict(t="機関室の乗組員が 2発", src="G1 p58"), dict(t="1:10ごろ", src="G1 p58"),
                              dict(t="白い信号弾 5発", src="G1 p58")],
                         note="船の中の並びは模式", src=ss.src(["G1 p58"])))),
    # c623（3行）＝1行目「会社の信号とは…夜の合図の光」→ 2行目「ホワイト・スター・ラインは緑、とカルパチア号の船長」→ 3行目「決まった合図」
    "c623": dict(
        t="会社の信号", s="夜の光の決まり",
        fig=("m26", dict(view="company", steps=[dict(state=dict(what="on")), dict(state=dict(ws="on")), dict(state=dict(vs="on"))],
                         rel=[], note="証言の言葉は英国の審問の書き起こし（有志のサイト）による・光の形は模式",
                         src=ss.src(["T1 p25394", "G2 p2018", "G1 p54"])))),
    # c626（2行）＝1行目「高さは、その船のマストの灯の半分くらい」→ 2行目「低い光…のちの調べ直しで論点になる」
    "c626": dict(
        t="どのくらいの高さか", s="記録に残る見え方",
        fig=("m26", dict(view="height", steps=[dict(state=dict(half="on")), dict(state=dict(topic="on"))],
                         rel=[dict(t="1992年の調べ直し", src="G2 p2017")],
                         note="証言の言葉は英国の審問の書き起こし（有志のサイト）による・絵は模式", src=ss.src(["T1 p7921", "G2 p2017"])))),
    # c634（2行）＝1行目「船長の記憶は違う。伝声管で聞いたのは1時15分ごろで、」→ 2行目「白い信号弾が1発だけ」（左の列は c620 の続き＝頭から）
    "c634": dict(
        t="食い違う記憶", s="伝声管の知らせ",
        fig=("m26", dict(view="memory2", start=dict(l="on"), steps=[dict(state=dict(r="on")), dict(state=dict(one="on"))],
                         rel=[dict(t="1:10ごろ・白い信号弾 5発", src="G1 p58"), dict(t="1:15ごろ・白い信号弾 1発", src="G1 p59")],
                         note="2人の話の写し", src=ss.src(["G1 p58", "G1 p59"])))),
    # c637（2行）＝1行目「カリフォルニアン号の時計で並べると」で夜の出来事 → 2行目「通信士は11時半に寝て、朝…起こされるまで眠っていた」
    "c637": dict(
        t="その夜の出来事", s="船の時計で並べると",
        fig=("m26", dict(view="cfband", steps=[dict(state=dict(ev="on")), dict(state=dict(sleep="on"))],
                         rel=[dict(t="22:20ごろ", src="G1 p56"), dict(t="23:40", src="G1 p57"), dict(t="1:10ごろ・白い信号弾5つ", src="G1 p58"),
                              dict(t="2:05・全部で8つ", src="G1 p59"), dict(t="2:40ごろ", src="G1 p59"), dict(t="23:30", src="G1 p57")],
                         note="縦は時刻に比例", src=ss.src(["G1 p56", "G1 p57", "G1 p58", "G1 p59"])))),
    # c639（3行）＝1行目「新しく見えた別の船を、信号弾の船と思ったらしい」→ 2行目「大丈夫そうだ…取り違えは、正されなかった」→ 3行目の問い
    "c639": dict(
        t="明け方の取り違え", s="船長の言葉",
        fig=("m26", dict(view="swap", steps=[dict(state=dict(think="on")), dict(state=dict(said="on")), dict(state=dict(q="on"))],
                         rel=[dict(t="4:00ごろ", src="G1 p59"), dict(t="マストの白い灯 2つ", src="G1 p59")],
                         note="船の形は模式", src=ss.src(["G1 p59"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-28）：写真と頁（第5章の15カット）＝書き方は c2.py の ⑤b-7 の注と同じ
# ══════════════════════════════════════════════════════════
_S3675, _PG1056, _S8625, _S3749, _S2E01, _PG1058 = P("s3_675"), P("p_g1_056"), P("s8_625"), P("s3_749"), P("s2_e01"), P("p_g1_058")
_S9674, _PG1059, _S3671, _S8630, _S6480 = P("s9_674"), P("p_g1_059"), P("s3_671"), P("s8_630"), P("s6_480")
SPEC.update({
    # c601（2行）＝船長（顔 x 0.58・y 0.28・右は別の人の背）へ少し寄る（c622 は顔へ・c824 は下から顔へ・cb01 は引く）
    "c601": dict(photo=_S3675, **ss.mv(_S3675, "in", fx=0.55, fy=0.4), side="none", color=1.0,
                 t="ここから相手の船", s="カリフォルニアン号の船長スタンリー・ロード〈1912年5月・英国の審問のころ〉"),
    # c603（2行）＝報告書 p.56「It is a position about 19 miles…」〜「I am satisfied that this position is not accurate.」
    #   切り口＝`pbox P-G1-056 "position about 19 miles" "is not accurate"`
    #   一覧「船長の位置の札を添える」＝右に注記（数は英国の審問の書き起こし T1 Day 7 Q6704＝断りは出典の行＝PLAN から）・頁の額は左（pw 1100）
    "c603": dict(photo=_PG1056, trim=(0.059, 0.833, 0.997, 0.901), panel=True, pw=1100, color=1.0,
                 ann=[dict(t="船長が計算した位置", d="北緯42度5分・西経50度7分")],
                 t="正確ではない位置", s="止まった位置についての一文"),
    # c605（2行）＝船尾（右）から船首（左）へ（c102 は右へ・c811 は煙突とマスト・cb06 は引く）
    "c605": dict(photo=_S8625, **ss.mv(_S8625, "l", fy=0.55), side="none", color=1.0,
                 t="止まったままの船", s="カリフォルニアン号〈カルパチア号の甲板から撮られたとみられる・NARA〉"),
    # c608（2行）＝縦長・小さい（467×793）＝額の中の切り口＝上の 6割（帽子から腰）・静止（c624 は顔・c934 はまるごと）
    "c608": dict(photo=_S3749, trim=(0.0, 0.0, 1.0, 0.60), panel=True, ground=dict(photo=_S3749), color=1.0,
                 t="自分の船くらい", s="スタンリー・ロード〈1908年・別の船の船長だったころ〉"),
    # c616（2行）＝ヘッドホンの通信士（頭 x 0.6・y 0.5）へ寄る（ca01 は機器から通信士へ流す）
    "c616": dict(photo=_S2E01, **ss.mv(_S2E01, "in", fx=0.62, fy=0.5, z=1.4), side="none", color=1.0,
                 t="何も聞こえない", s="1912年の船の無線室〈姉妹船オリンピック号・1912年の本の写真〉"),
    "c622": dict(photo=_S3675, **ss.mv(_S3675, "in", fx=0.58, fy=0.3, z=1.6), side="none", color=1.0,
                 t="会社の信号か", s="カリフォルニアン号の船長スタンリー・ロード〈1912年5月・英国の審問のころ〉"),
    # c624（2行）＝c608 と同じ写真・同じ副題＝額の中の切り口を顔（x 0.25〜0.95・y 0.04〜0.40）に替える（静止）
    "c624": dict(photo=_S3749, trim=(0.25, 0.04, 0.95, 0.40), panel=True, ground=dict(photo=_S3749), color=1.0,
                 t="呼び続けよ", s="スタンリー・ロード〈1908年・別の船の船長だったころ〉"),
    # c628（3行）＝報告書 p.58（束の段で機関部の乗組員の名前の行を外した「Both Mr. Stone and the apprentice…」から頁の終わり）＝まるごと額装
    "c628": dict(photo=_PG1058, panel=True, pw=1640, color=1.0,
                 t="理由なく打たない", s="二等航海士と見習いの話の段落"),
    # c629（3行）＝会場の真ん中の少し上へ寄る（y 0.5 だと窓の下の辺が席の札「COUNSEL」を半分に切った＝門番 edges）
    "c629": dict(photo=_S9674, **ss.mv(_S9674, "in", fx=0.5, fy=0.4), side="none", color=1.0,
                 t="知っていた合図", s="英国の審問の会場〈ロンドン・1912年〉"),
    # c635（2行）＝報告書 p.59「There is considerable discrepancy…」〜「…opening and closing the chart-room door.」
    #   切り口＝`pbox P-G1-059 "considerable" "chart-room door"`
    "c635": dict(photo=_PG1059, trim=(0.003, 0.301, 0.932, 0.439), panel=True, pw=1640, color=1.0,
                 t="覚えていない船長", s="二等航海士と船長の話の食い違いの段落"),
    "c636": dict(photo=_S3671, **ss.mv(_S3671, "in", fx=0.55, fy=0.45), side="none", color=1.0,
                 t="食い違う証言", s="英国の審問の長マージー卿〈1912年〉"),
    # c640（3行）＝船首（右・x 0.85〜0.95・y 0.5〜0.7）へ寄る（c316 は右へ・c520 は船体）
    "c640": dict(photo=_S8630, **ss.mv(_S8630, "in", fx=0.84, fy=0.6, z=1.35), side="none", color=1.0,
                 t="朝6時の知らせ", s="カリフォルニアン号〈1907年〉"),
    # c641（2行）＝帆を張ったボート（右・x 0.68・y 0.45）へ寄る（c104 は右へ・cb04 は漕ぐボートへ）。
    #   ガラス乾板の黒い縁（左 2.1%）＝引いた側の寄り lo 1.08・寄った側の真ん中 x 0.65（右の縁に窓を当てない＝門番 photo_edge）
    "c641": dict(photo=_S6480, **ss.mv(_S6480, "in", fx=0.65, fy=0.45, z=1.5, lo=1.08), side="none", color=1.0,
                 t="何時間も前に", s="4月15日の朝、海の上のボート〈1912年・BnF〉"),
})
