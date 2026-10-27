# -*- coding: utf-8 -*-
"""第2章　氷の知らせ c301–c323（23カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c3.py`）。
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
    'c301': dict(kind='写真',
               plan='S3-352:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：タイタニック号の通信士ジャック・フィリップス｜動き：静止｜権利：PD｜時期：前｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：撮影年は分からない（本人の個人の写真）＝副題に年を書かない｜新しい画（映像方針）：台本どおり（縦長＝高さいっぱいの額・静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.36（`There were two Marconi operators in the Marconi room`）'),
    'c302': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：無線室と電波の輪・陸の無線局・眠ると誰も聞かない船（顔の無い影）｜合図：🔁 上から→横から（前の図 c218）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.1（`in 1912 many ships did not have wireless and those that did, did not necessarily keep continuous watch`）'),
    'c303': dict(kind='図解',
               plan='一覧の種類：時計｜見る向き：正面｜見た目の型：東西に離れた2隻の時計（針の数字なし）｜合図：🔁 横から→正面（前の図 c302）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.6（`It was customary in 1912 for ships to adjust their clocks so that the sun would be approximately on the meridian each day at 1200 hrs`）'),
    'c304': dict(kind='写真',
               plan='S1-013:全体｜一覧の種類：実写｜見せ方：全面｜副題：サウサンプトンのタイタニック号〈1912年4月〉｜動き：寄る｜権利：PD｜時期：前｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S1-008 は同じ写真＝c415 は S1-017 に替えた｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.6（`the possible difference in times between TITANIC and CALIFORNIAN is only likely to have been a few minutes`）'),
    'c305': dict(kind='写真',
               plan="🔧 S4-242:12時35分の行｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：カルパチア号の船長の報告〈1912年4月27日・LOC〉｜動き：静止｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：米国議会図書館（LOC）｜注：✅ 10-27 原寸で読んだ＝1行目「At 12.35 a.m. (ship's time) April 15th (Monday), 1912」・右上「R.M.S. Carpathia … At Sea April 27th 1912」。頁の頭の「The Modern Historic Records Association」の刷りは切り出しの外｜新しい画（映像方針）：🔧 字に寄る → 静止の切り出し（「At 12.35 am (ships time)」の行のまわり＝939px の原本の y250〜330 あたり）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）",
               src='materials.md §1-5 S4-242（見本帳で「At 12.35 am (ships time) April 15th」の字を読んだ）'),
    'c306': dict(kind='図解',
               plan='🔧 GS-ice｜一覧の種類：衛星｜見せ方：衛星（帰属の行）｜動き：寄る（5つの印へ）｜見る向き：上から｜見た目の型：氷の知らせの5つの印と航路（衛星写真・ニューファンドランドを左上に）｜合図：🔁 正面→上から（前の図 c303）｜権利：Google の地図の利用（帰属の行を出し続ける）｜時期：今｜人：なし｜出典の行：Google の地図（衛星写真）＋描き足し｜注：5隻の名の札（カロニア号・バルティック号・アメリカ号・カリフォルニアン号・メサバ号）｜新しい画（映像方針）：🔧 図の氷域 → 衛星写真＋描き足し（地図の既定）・印は報告書の緯度経度｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.35（`at 9 a. m. (Titanic time) on that day a wireless message from the steamship Caronia was received by Capt. Smith`）'),
    'c307': dict(kind='写真',
               plan='🔧 S5-358:全体｜一覧の種類：実写｜見せ方：全面｜副題：1912年4月、この海域の氷山〈ミニア号の船長が持っていた写真〉｜動き：左へ｜権利：PD｜時期：氷｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 額装 → 全面（715px＝約2.7倍・ぼけは差し替えの理由にしない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.35（`West-bound steamers report bergs, growlers, and field ice in 42° N., from 49° to 51° W., April 12`）'),
    'c308': dict(kind='写真',
               plan='🔧 S8-N01:全体｜一覧の種類：実写｜見せ方：全面｜副題：バルティック号〈1904年・ベルファスト〉｜動き：右へ｜権利：PD｜時期：別の年｜人：なし｜出典の行：出典：北アイルランド国立博物館（Harland & Wolff Collection）｜注：🆕 了承②。✅ 10-27 何の絵か確かめた（2本煙突・4本マスト・下に「THE BALTIC.」と整理番号「4880 R.W.」＝整理番号は寄りで外す）｜新しい画（映像方針）：🔧 S5-361（氷山・1912年の本）→ バルティック号（語りの船＝氷の写真が続くのを散らす）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.36（`At 1.42 p. m., a wireless message from the steamship Baltic was received by Capt. Smith`…`Greek steamer Athenai reports passing icebergs and large quantities of field ice`）'),
    'c309': dict(kind='写真',
               plan="🔧 S4-N06:本文｜一覧の種類：実写｜見せ方：額装（幅いっぱい）｜副題：タイタニック号を経て届いたアメリカ号の電報〈1912年4月・米国海軍水路部が受けた〉｜動き：静止｜権利：PD｜時期：文書｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：🆕 了承②。✅ 10-27 原寸で読んだ＝「S S Amerika via S S Titanic and Cape Race N.E. April,14,1912／Hydrographic Office, Washington DC／Amerika passed two large icebergs in 41 27 N 50 8 W on the 14th of April」・受付の印「HYDRO. OFFICE Rec'd APR 15 1912」。切り出し＝本文と受付の印（1920px の版の x280〜1720・y560〜900 あたり）＝用紙の頭の電信会社の社長の名（小さな刷り）は切り出しの外｜新しい画（映像方針）：🔧 日報（S4-228）→ アメリカ号の電報そのもの（語り＝アメリカ号が氷山2つをワシントンの海軍の役所へ送った・タイタニック号が中継する知らせ）＝c310 と入れ替えた｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）",
               src='G1 p.36（`about 1.45 p. m. (Titanic time) on the 14th a message was sent from the German steamer Amerika to the Hydro`…`because she was nearest to Cape Race`）・A1 naId 595107（日報の「TITANIC (Br ss)」の行＝materials.md §1-5）'),
    'c310': dict(kind='写真',
               plan="🔧 S4-228:衝突とアメリカ号の行｜一覧の種類：実写｜見せ方：全面（切り出し）｜副題：米国海軍水路部の日報〈1912年4月15日・NARA〉｜動き：下へ（衝突の行からアメリカ号の行へ）｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：米国立公文書館（NARA）｜注：✅ 10-27 原寸で読んだ（1920px の版の x150〜1620・y1530〜1830）＝「COLLISION WITH ICEBERG - Apr 14 - Lat 41° 46', lon 50° 14', the British steamer TITANIC collided with an iceberg…」・「The German steamer AMERIKA reported by radio telegraph passing two large icebergs in lat 41° 27', lon 50° 08',--TITANIC (Br ss).」・手書きのレ点と括弧。頁の末の水路部長の署名は切り出しの外｜新しい画（映像方針）：🔧 S4-300（陸の無線局の塔＝別の局）→ 日報の衝突とアメリカ号の行（語り＝その知らせは船橋に届いたか＝ワシントンには届き、同じ頁にタイタニック号の衝突が並ぶ）＝c309 と入れ替えた｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）",
               src='G1 p.36（`Being a message affecting navigation, it should in the ordinar`…`have been taken to the bridge`）'),
    'c311': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：アメリカ号の知らせの道すじ（無線室で脇に置く・船橋へ届かない線）｜合図：🔁 上から→横から（前の図 c306）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.36（`it was put aside by Phillips to wait until the Titanic would be within call of Cape Race`…`it was never handed to any officer`）'),
    'c312': dict(kind='写真',
               plan='🔧 S8-N02:全体｜一覧の種類：実写｜見せ方：全面｜副題：メサバ号〈1898〜1909年ごろ・テムズ川〉｜動き：左へ｜権利：PD｜時期：別の年｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：🆕 了承②｜新しい画（映像方針）：🔧 S5-364（氷山）→ メサバ号（語りの船＝氷の写真が続くのを散らす）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.37（`there was a fifth message received in the Marconi room of the Titanic at 9.40 p. m.`…`saw much heavy pack ice and great number large icebergs. Also field ice`）'),
    'c313': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：乗客の電報に追われる通信士の影とケープ・レース・船橋へ届かない線｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.37（`it does not appear to have been delivered to the master or to any of the officers`…`transmitting messages via Cape Race for passengers`）'),
    'c314': dict(kind='写真',
               plan='🔧 S5-357:全体｜一覧の種類：実写｜見せ方：全面｜副題：4月15日の朝に撮られた氷山〈プリンツ・アダルベルト号の司厨長〉｜動き：上へ（根もとの黒い帯から頂へ）｜権利：PD｜時期：氷｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 額装 → 全面｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='legend §2-1 #2（よく語られる話＝競合の「7回もの氷山警告・無視」）・G1 p.37（`there was a fifth message`）'),
    'c315': dict(kind='写真',
               plan='🔧 S2-085:全体｜一覧の種類：実写｜見せ方：全面｜副題：ボート甲板の船長〈1912年4月11日〉｜動き：右へ｜権利：PD｜時期：前｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：左の事務長は乗員＝副題に名を出さない｜新しい画（映像方針）：🔧 額装 → 全面（1667px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.40（`the other was to reduce speed materially as night approached. He did neither`）'),
    'c316': dict(kind='写真',
               plan='🔧 S8-630:全体｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号〈1907年〉｜動き：右へ｜権利：PD｜時期：別の年｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S8-630 は3回まで（c316・c520・c640）｜新しい画（映像方針）：🔧 額装 → 全面（1475px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.56（`At 7.30 p. m., ship's time, on April 14, a wireless message was sent from this ship to the Antill`）"),
    'c317': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：2隻の横の姿を同じ縮尺で（会社の名の札）｜新しい画（映像方針）：台本どおり（c202 の棒と別の絵）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`the steamship Californian, of the Leyland Line`…`was on her passage from London`…`to Boston`・`She had a passenger certificate, but was not carrying any passengers at the time`）'),
    'c318': dict(kind='写真',
               plan='S5-362:全体｜一覧の種類：実写｜見せ方：全面｜副題：氷原と氷山〈1912年4月・カルパチア号の乗客が撮ったと1912年の本は書く〉｜動き：左へ｜権利：PD｜時期：氷｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S5-362 は c817 と2回｜新しい画（映像方針）：台本どおり（本の頁の字は外す）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`Three large bergs, 5 miles to southward of us`）'),
    'c319': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：3隻の小さな姿と、アンティリアン号への電波をタイタニック号も受ける線｜合図：🔁 横から→上から（前の図 c317）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`The message was intercepted by the Titanic`…`It is all right. I heard you sending it to the Antillian, and I have got it`）'),
    'c320': dict(kind='再現イラスト',
               plan='一覧の種類：案C-3｜見る向き：横から｜見た目の型：カリフォルニアン号の無線室・夜11時ごろ・電鍵を打つ通信士の影｜合図：🔁 上から→横から（前の図 c319）｜注：形のもと＝了承②｜新しい画（映像方針）：台本どおり（モールスの字は描かない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.57（`At about 11 p. m. a steamer's light was seen approaching`…`I think the Titanic is near us. I have got her`…`We are stopped and surrounded by ice`）"),
    'c321': dict(kind='写真',
               plan='🔧 S2-206:手元｜一覧の種類：実写｜見せ方：全面｜副題：タイタニック号の無線室とされる写真〈1912年4月〉｜動き：寄る（ヘッドホンの人へ）｜権利：PD｜時期：前｜人：乗員（後ろ姿）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 額装 → 全面・c220 と別の寄り｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.57（`The Titanic replied: Keep out`）'),
    'c322': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：近くの強い電波が遠いケープ・レースの弱い電波をかき消す輪｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.57（`The Titanic was in communication with Cape Race`…`as from her proximity the message from the Cali`…`was much stronger than any message being taken in by the Titanic from Cape Race`）'),
    'c323': dict(kind='写真',
               plan='S9-648:全体｜一覧の種類：実写｜見せ方：全面｜副題：米国上院の公聴会〈1912年4月・LOC〉｜動き：寄る｜権利：PD｜時期：後・審問｜人：遠景（⑤b で原寸）｜出典の行：出典：米国議会図書館（LOC）｜注：語りは公聴会での証言（G7 p.739＝公式の印刷）＝書き起こしの断りは要らない・場面は公聴会（時期の門番の例外）｜時期の門番の例外＝語りは米国上院の公聴会での証言（G7 p.739）＝場面は公聴会｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G7 p.739（`Shut up, shut up, I am busy; I am working Cape Race`）・G1 p.57（`up to the time he turned in at 11.30 p. m.`）'),
}

SPEC = {}
