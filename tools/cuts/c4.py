# -*- coding: utf-8 -*-
"""第3章　10時47分 c401–c419（19カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c4.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep22/make_plan22.py` で
  映像方針の一覧 `ref/ep22/eizou_build/list22.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典から
  機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット（台本の画は元の予定）。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c401': dict(kind='図解',
               plan='🔧 注：🔧 再現→吹き出し（§0-3）｜新しい画（映像方針）：図 吹き出し 付録A の 10:11:55〜10:15:39 の4行（c317 と同じ形・10:12 の4行は除く）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 書類の再現図 TSB 付録A の表（10:11:55〜10:15:39 のうち4行＝10:12 の4行は除く・欄の値は英字のまま＝`lost system oand chat settings`・`yes`・`all good here`・`ack all good`・訳は字幕だけ）',
               src='TSB §1.3.2（`indicating that the communication system had temporarily stopped working`）・付録A（`10:14:35.5 T all good here`）'),
    'c402': dict(kind='図解',
               plan='台本の画：図 線 深さの線（記録の点だけ＝9:31 680m・10:11〜10:15 2,203→2,289m・10:40 3,149m・10:47:02 3,341m＝米沿岸警備隊の値。あいだは直線＝模式と左下で断る。10:23 と 10:29 の約2,833m は USCG の中で時刻が揺れる＝点を置かない）',
               src='USCG p.34〈26〉（`from 2,203 m (7,227 feet) to 2,289 m (7,509 feet)`）'),
    'c403': dict(kind='図解',
               plan='🔧 見る向き：上から｜合図：🔁 横から→上から（前の図 c315）＝左上に見る向きの札・替わる瞬間に「上から見ると」｜注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 上から見たタイタニックの船首と、母船（水色の点＝船首の真上へ）・潜水艇（白の点＝そこを目がける）・「東南東」「東北東」の札｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 付録A の表（10:23:33・10:25:46 の2行＝`poi orks we are east south east of the nbow`・`we see you east north east of the bow`）',
               src='USCG p.34〈26〉（`would act as the point of interest and place itself directly above the desired location`）・TSB 付録A（`we are east south east of the nbow`）'),
    'c404': dict(kind='図解',
               plan='🔧 見る向き：上から｜注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 同じ図（潜水艇の白の点が、送るたびに跳ぶ＝点の跡がばらける）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 付録A の表（10:29:12〜10:31:55 の6行）',
               src='TSB 付録A（`your position jumps significantly each ping`）・USCG p.34〈26〉（`generally considered to be an adequate signal`）'),
    'c405': dict(kind='写真',
               plan='M31｜見せ方：全面｜副題：母船の船橋の事務室（通信班の持ち場・事故のあとに委員会が撮影）｜動き：左へ｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図31｜注：人なし｜台本の画：実写 MBI 図31 船橋の事務室（通信班の持ち場・机と画面・人なし・USCG 報告 p.32・A・全画面には小さい＝寄り弱め＝副題「母船の船橋の事務室（通信班の持ち場・事故のあとに委員会が撮影）」）',
               src='TSB 付録A（`remember to write down the location and time of niskin deployment`）・USCG p.34〈26〉（`Niskin bottles are used for collecting water samples at various depths`）'),
    'c406': dict(kind='図解',
               plan='🔧 注：🔧 再現→吹き出し（§0-3）｜新しい画（映像方針）：図 吹き出し 付録A の 10:36:50〜10:40:56 の8行（打ち間違いのまま）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 付録A の表（10:36:50〜10:40:56 の8行・打ち間違いのまま＝`when? messages truncated`・`andn location`・`no niskin. never cleaned and string baf`）',
               src='TSB 付録A（`no niskin. never cleaned and string baf`）・USCG p.34〈26〉（`The depth of the TITAN was 3,149 m`）'),
    'c407': dict(kind='図解',
               plan='🔧 注：🔧 再現→帯（§0-3）｜新しい画（映像方針）：図 帯 時刻の帯（10:41:07「ニスキンは無し」・10:42:01「a」→ その先に5分あまりの空白の帯）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 付録A の表（10:41:07・10:42:01 の2行＝`ack no niskin`・`a`）',
               src='TSB 付録A（`ack no niskin`）・付録A（`a = received your last, end thread`）'),
    'c408': dict(kind='図解',
               plan='🔧 注：🔧 再現→吹き出し（§0-3）｜新しい画（映像方針）：図 吹き出し 付録A の最後の行（10:47:26.9 `dropped two wts`＝画面に出た時刻）と、米沿岸警備隊の青の札「10:47:02（送った）」｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 付録A の表の最後の行（10:47:26.9 `dropped two wts`＝画面に出た時刻）と、米沿岸警備隊の送った時刻の札「10:47:02（送った）」',
               src='USCG p.35〈27〉（`At approximately 10:47:02 a.m., the TITAN sent a message to the POLAR PRINCE, stating, “dropped two wts.”…The depth of the TITAN was 3,341 m.`）'),
    'c409': dict(kind='図解',
               plan='見る向き：横から｜合図：🔁 上から→横から（前の図 c404）＝左上に見る向きの札・替わる瞬間に「横から見ると」｜台本の画：図 模式 重りで降りる仕組み（降りる→重りを落として止まる→浮く・NTSB 図3 の艇の線画をなぞる・重りの数と場所は描かない）',
               src='USCG p.35〈27〉（`weights were released to slow the descent to the intended operating depth or begin the ascent back to the surface`）'),
    'c410': dict(kind='図解',
               plan='台本の画：図 帯 2段の札（上＝米国の2つの調べ「この深さのふつうのやり方」／下＝カナダ「海底まで約500m・いつもより早い・理由は分からない」）',
               src='NTSB p.17（`which was a standard procedure at this depth to slow its descent`）・USCG p.6〈vi〉（`As the TITAN approached the ocean floor, it followed standard procedure by releasing ballast weights to slow its descent.`）・TSB §1.3.2（`the submersible was approximately 500 m from the seabed`）・§2.1（`Dropping the 2 weights earlier than normal suggests`…`the reason for this is unknown`）'),
    'c411': dict(kind='図解',
               plan='台本の画：図 帯 時刻の帯（米沿岸警備隊の段＝10:47:02 送った→10:47:08 最後の位置→10:47:09ごろ 壊れた）',
               src='USCG p.35〈27〉（`At approximately 10:47:09 a.m., the TITAN submersible suffered a catastrophic implosion`）・p.35〈27〉（`resulting in the instantaneous death of all five occupants`）'),
    'c412': dict(kind='図解',
               plan='台本の画：図 帯 同じ帯（10:47:11「バン」・10:47:26 受けた を明るく）',
               src='USCG p.35〈27〉（`heard a sound described by the leader for communications and tracking as a “bang”`）・p.35〈27〉〜p.36〈28〉（`This was the last message that was sent from the TITAN.`）'),
    'c413': dict(kind='図解',
               plan='台本の画：図 帯 2段の帯（上＝米沿岸警備隊・下＝カナダ。「画面に出た」と「壊れた」の順が上下で逆）',
               src='TSB §1.3.2（`At 1047:26.903, when the submersible was at 3350 m, a message appeared on the surface support team’s computer`）・§2.1（`The pressure hull’s structural failure happened 5.397 seconds after the text message about dropping the 2 weights appeared`）'),
    'c414': dict(kind='図解',
               plan='台本の画：図 帯 2段の帯（下の段＝10:47:26.903 画面→10:47:32.066 最後の位置→10:47:32.3 壊れた→10:47:34.522 船体に音）',
               src='TSB 脚注19（`included a view of the computer being used by the surface support team`）・TSB §1.3.2（`a loud sound, which could be characterized as a thud or a bang, reverberated through the hull of the Polar Prince`）・§2.1（`5.397 seconds after the text message about dropping the 2 weights appeared`）'),
    'c415': dict(kind='図解',
               plan='台本の画：図 帯 2段の帯（「送った」は両段とも壊れる前・「受けた」10:47:26／10:47:32 は両段で合う・「壊れた」だけが離れる）',
               src='USCG p.37〈29〉（`At 10:47:32 a.m., the POLAR PRINCE received the ping that was sent at 10:47:08 a.m.`）・TSB §1.3.2（`At 1047:32.066, the surface support team’s computer received the last automated position update`）'),
    'c416': dict(kind='図解',
               plan='台本の画：図 帯 時刻の帯（10:48「受け取った」を返す・10:49「追跡を失った」を送る・どちらも返事なし）',
               src='NTSB p.17（`At 1048, the Polar Prince sent a message back to acknowledge the Titan’s message, but they received no response.`）・p.17（`At 1049, the Polar Prince sent the Titan a “lost tracking” message but received no response.`）'),
    'c417': dict(kind='写真',
               plan='M37｜見せ方：額装（報告書の図）｜副題：母船の航海日誌（事故のあとに委員会が撮影）｜動き：額ごと右へ｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図37｜注：頁の上の印＝「1047 lost communication with TITAN」の行｜台本の画：実写 MBI 図37 航海日誌（6/18 06:00〜12:00 の頁・額装・頁の上の印＝「1047 lost communication with TITAN」の1行・USCG 報告 p.38・A＝副題「母船の航海日誌（事故のあとに委員会が撮影）」）',
               src='USCG p.38〈30〉（`At 11:15 a.m., the Master of the POLAR PRINCE was advised that as of approximately 10:47 a.m., there was a loss of communication with the TITAN.`）・p.38〈30〉（`it stated “1047 lost communication with TITAN.”`）'),
    'c418': dict(kind='図解',
               plan='台本の画：図 線 深さの線（最後の点 10:47:08 3,346.28m で線が止まる・海底は約3,800m の破線）',
               src='TSB §1.7（`At its last-known depth of 3355 m, the Titan was calculated to be under 33.587 MPa of hydrostatic pressure. This is equivalent to a pressure of 342.49 kg per square cm.`）'),
    'c419': dict(kind='図解',
               plan='台本の画：図 線 同じ図（線の止まった点に寄る）',
               src='USCG p.269〈261〉（`There were no witnesses to the implosion or video evidence recovered of the implosion`）'),
}

SPEC = {}
