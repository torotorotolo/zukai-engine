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

# 🆕 ⑤b-3（2026-10-27）：地図（衛星写真＋描き足し＝`ss.sat`・寄らない・色を変えない）。印は G1 p.35〜37 の緯度経度（札に数字を置かない）
SPEC.update({
    # c306（2行・7.7秒）＝1行目「タイタニック号の時計だ。4月14日の朝9時、」で航路 → 2行目「カロニア号から、最初の氷の知らせ」で5つの印
    #   ⚠️ 映像方針の注「ニューファンドランドを左上に」はズーム6 でないと入らない＝5つの印が額の中で約80×35px に詰まる＝ズーム8 で氷の海域に寄せた（広い図は c218）
    "c306": dict(
        **ss.sat("G02", steps=[
            # 色は役の名で引く（role＝jiko_style.ROLE の鍵＝色の名札。意味は前の回の名のまま）：ship＝水色・bldg_a＝桃色・ntsb＝緑・uscg＝青・company＝橙
            [dict(k="line", path=("turning", "collision"), role="ship", t="タイタニック号の航路", u=0.35, lab=(0, 46, "middle"))],
            [dict(k="line", path=("ice_caronia_w", "ice_caronia_e"), c="AMBER", t="カロニア号", u=0.2, lab=(0, -22, "middle")),
             dict(k="line", path=ss.SAT_LINES["mesaba"], role="bldg_a", dash=True, t="メサバ号", u=0.42, lab=(16, 40, "start")),
             dict(k="pt", at="ice_californian", role="ntsb", t="カリフォルニアン号", lab=(16, -22, "start")),
             dict(k="pt", at="ice_baltic", role="uscg", t="バルティック号", lab=(-20, 6, "end")),
             dict(k="pt", at="ice_amerika", role="company", t="アメリカ号", lab=(-18, 36, "end"))]],
            note="印は英国の審問の報告の緯度経度"),
        t="船からの無線", s="4月14日の氷の知らせの位置・北大西洋（現在の衛星写真）"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-27）：案C-3 カリフォルニアン号の無線室＝K3（`tools/illu26.py`・門番 check_illu ㊽）
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c320（2行・9.4秒）＝1行目「夜11時ごろ、カリフォルニアン号は氷原の手前で止まっていた。」で時計の札 → 2行目「この船の船長に言われ、
    #   通信士はタイタニック号へ打った。…」で電鍵を打つ・空中線から輪（モールスの字は描かない）。船長は描かない（言った人＝語り）
    "c320": dict(fig=("illu", dict(
        place="K3", start=dict(ksw="side"), at="23:00",
        people=dict(crew=(1, "G1 p57（This Evans did, calling up the Titanic and sending）")),
        steps=[dict(state=dict(), rec="G1 p57（At about 11 p. m. a steamer's light was seen approaching from the eastward）",
                    tag=dict(t="23:00ごろ（カリフォルニアン号の時計）", xy=(640, 210), keep=True)),
               dict(state=dict(k3key="tap"), rings=3, rec="G1 p57（This Evans did, calling up the Titanic and sending: We are stopped and surrounded by ice）",
                    tag=dict(t="通信士", at="op", off=(70, -40)))]))),
})

# 🆕 ⑤b-5（2026-10-28）：図解（`tools/mech26.py`・fig=("m26", …)）。段の数＝語りの行の数・画面の数は全部 rel に（門番 check_mech の judge_m26）
SPEC.update({
    # c302（2行）＝1行目「無線の無い船も多かった」→ 2行目「いつも誰かが聞いているとは、限らなかった」で眠る影と ✕
    "c302": dict(
        t="聞く人がいなければ", s="1912年の海の無線",
        fig=("m26", dict(view="radio3", steps=[dict(state=dict(none="on")), dict(state=dict(deaf="on"))],
                         rel=[], note="絵は模式", src=ss.src(["G2 p2005"])))),
    # c303（2行）＝1行目「時計の話…当時の船は毎日、」で2つの時計 → 2行目「正午に太陽が真南に来るように…合わせていた」で太陽と針が12へ
    "c303": dict(
        t="船ごとの時計", s="1912年の決まり",
        fig=("m26", dict(view="clocks2", steps=[dict(state=dict(clk="on")), dict(state=dict(noon="on"))],
                         rel=[], note="絵は模式（時計に数字は描かない）", src=ss.src(["G2 p2010"])))),
    # c311（2行）＝1行目「ケープ・レースと話せる所まで来るのを待とうと、」で脇に置く → 2行目「どの航海士にも渡らなかった…報告書はそうみる」で ✕
    "c311": dict(
        t="脇に置かれた知らせ", s="無線室で止まった",
        fig=("m26", dict(view="aside", steps=[dict(state=dict(aside="on")), dict(state=dict(nope="on"))],
                         rel=[], note="船の中の部屋の並びは模式", src=ss.src(["G1 p36"])))),
    # c313（2行）＝1行目「この知らせも…届いていないようだ」で氷の知らせと ✕ → 2行目「8時から、乗客の電報を…送るのに追われていた」
    "c313": dict(
        t="乗客の電報に追われて", s="もう1つの氷の知らせ",
        fig=("m26", dict(view="busy", steps=[dict(state=dict(ice="on")), dict(state=dict(busy="on"))],
                         rel=[dict(t="20:00から", src="G1 p37")], note="部屋の形は模式", src=ss.src(["G1 p37"])))),
    # c317（2行）＝1行目「レイランド社の船で、ロンドンからアメリカのボストンへ」→ 2行目「客を乗せていなかった」で空の窓と「乗客 0人」
    #   🔧 一覧の「2隻の横の姿を同じ縮尺で」→ カリフォルニアン号1隻（記録の頁にカリフォルニアン号の長さが無い＝同じ縮尺にできない・大きさは c202 の総トン数）
    "c317": dict(
        t="近くにいた船", s="カリフォルニアン号（1912年4月）",
        fig=("m26", dict(view="cf_side", steps=[dict(state=dict(co="on")), dict(state=dict(empty="on"))],
                         rel=[dict(t="乗客 0人", src="G1 p56")], note="船の形は模式（記録に長さが無い）", src=ss.src(["G1 p56"])))),
    # c319（2行）＝1行目「これを横で聞いていた」→ 2行目「分かった…受け取った、と返した」
    "c319": dict(
        t="横で聞いていた", s="通信士どうしのやりとり",
        fig=("m26", dict(view="relay3", steps=[dict(state=dict(hear="on")), dict(state=dict(reply="on"))],
                         rel=[], note="船の位置は模式", src=ss.src(["G1 p56"])))),
    # c322（2行）＝1行目「陸のケープ・レースと交信中だった」で弱い電波 → 2行目「近くの船の強い電波が…かき消した」
    "c322": dict(
        t="かき消された電波", s="なぜ、そう返したのか",
        fig=("m26", dict(view="drown", steps=[dict(state=dict(talk="on")), dict(state=dict(loud="on"))],
                         rel=[], note="電波の輪と棒は模式", src=ss.src(["G1 p57"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-28）：写真と頁（第2章の17カット）＝書き方は c2.py の ⑤b-7 の注と同じ
# ══════════════════════════════════════════════════════════
_S3352, _S1013, _S4242, _S5358, _S8N01, _S4N06 = P("s3_352"), P("s1_013"), P("s4_242"), P("s5_358"), P("s8_n01"), P("s4_n06")
_S4228, _S8N02, _S5357, _S2085, _S8630, _S5362 = P("s4_228"), P("s8_n02"), P("s5_357"), P("s2_085"), P("s8_630"), P("s5_362")
_S2206, _S9648 = P("s2_206"), P("s9_648")
# 本の頁の写真（S5-362）＝写真の枠の内だけ（下の題と説明文「…the huge Iceberg with which the Titanic collided…」は外＝「衝突した氷山」と名乗らない）
_S5362_IN = (0.065, 0.065, 0.91, 0.835)
SPEC.update({
    "c301": dict(photo=_S3352, panel=True, ground=dict(photo=_S3352), color=1.0,
                 t="会社から来た通信士", s="タイタニック号の通信士ジャック・フィリップス"),
    "c304": dict(photo=_S1013, **ss.mv(_S1013, "in", fx=0.5, fy=0.55), side="none", color=1.0,
                 t="ずれる時計の差", s="サウサンプトンのタイタニック号〈1912年4月〉"),
    # c305（1行）＝手書きの報告の頭（右上の「R.M.S. Carpathia … At Sea April 27th 1912」と「At 12.35 a.m. (ship's time)」の段落）＝
    #   頁の頭の刷り「The Modern Historic Records Association」（y 〜0.035）は切り口の外・額装・静止
    "c305": dict(photo=_S4242, trim=(0.03, 0.04, 0.97, 0.30), panel=True, pw=1640, ground=dict(photo=_S4242), color=1.0,
                 t="船の時刻で", s="カルパチア号の船長の報告〈1912年4月27日・LOC〉"),
    "c307": dict(photo=_S5358, **ss.mv(_S5358, "l"), side="none", color=1.0,
                 t="12日の氷の知らせ", s="1912年4月、この海域の氷山〈ミニア号の船長が持っていた写真〉"),
    # c308（2行）＝船（y 0.4〜0.65）＝右へ。下の整理番号「4880 R.W.」と題「THE BALTIC.」（y 0.9〜）は窓の外（縦の窓 67%）
    "c308": dict(photo=_S8N01, **ss.mv(_S8N01, "r", fy=0.5), side="none", color=1.0,
                 t="昼に届いた知らせ", s="バルティック号〈1904年・ベルファスト〉"),
    # c309（2行）＝電報の本文と受付印（束の段で用紙の頭の枠＝電信会社の社長の名前の刷りを外した 1516×765）＝幅いっぱいの額・静止
    "c309": dict(photo=_S4N06, panel=True, pw=1640, ground=dict(photo=_S4N06), color=1.0,
                 t="アメリカ号の電報", s="タイタニック号を経て届いたアメリカ号の電報〈1912年4月・米国海軍水路部が受けた〉"),
    # c310（3行）＝日報の「COLLISION WITH ICEBERG…」と「The German steamer AMERIKA…」の2項（y 0.62〜0.74・手書きのレ点と括弧つき）。
    #   🔧 一覧は「全面（切り出し）・下へ」＝白い紙の字の頁を全面にすると見出し・章の札が頁の字に重なる（25本目 ⑤b-7 の所見）＝額装・静止にした。
    #   頁の末の水路部長の署名（y 0.78〜）は切り口の外
    "c310": dict(photo=_S4228, trim=(0.05, 0.612, 0.95, 0.747), panel=True, pw=1640, ground=dict(photo=_S4228), color=1.0,
                 t="船橋には届かず", s="米国海軍水路部の日報〈1912年4月15日・NARA〉"),
    "c312": dict(photo=_S8N02, **ss.mv(_S8N02, "l"), side="none", color=1.0,
                 t="メサバ号から", s="メサバ号〈1898〜1909年ごろ・テムズ川〉"),
    # c314（3行）＝横長（1.77）＝寄り 1.0 では縦が動かない＝寄り 1.25 で根もとの黒い帯から頂へ
    "c314": dict(photo=_S5357, **ss.mv(_S5357, "u", z=1.25), side="none", color=1.0,
                 t="2通は渡っていない", s="4月15日の朝に撮られた氷山〈プリンツ・アダルベルト号の司厨長〉"),
    "c315": dict(photo=_S2085, **ss.mv(_S2085, "r"), side="none", color=1.0,
                 t="進路も速さも変えず", s="ボート甲板の船長〈1912年4月11日〉"),
    "c316": dict(photo=_S8630, **ss.mv(_S8630, "r", fy=0.55), side="none", color=1.0,
                 t="北からの知らせ", s="カリフォルニアン号〈1907年〉"),
    # c318（2行）＝写真の枠の内を左へ（縦の寄せ 0.42＝y 0.45 だと字幕の帯の上の辺が氷原の模様を OCR が読んだ行に 8% かかった＝門番 edges）
    "c318": dict(photo=_S5362, **ss.tcam(_S5362, _S5362_IN, (0.62, 0.42, 1.15), (0.38, 0.42, 1.15)), side="none", color=1.0,
                 t="3つの氷山", s="氷原と氷山〈1912年4月・カルパチア号の乗客が撮ったと1912年の本は書く〉"),
    # c321（3行）＝ヘッドホンの人（後ろ姿・頭 x 0.38・y 0.55）へ寄る（c220 の机より一段寄る）
    "c321": dict(photo=_S2206, **ss.mv(_S2206, "in", fx=0.38, fy=0.6, z=1.5), side="none", color=1.0,
                 t="割り込むな", s="タイタニック号の無線室とされる写真〈1912年4月〉"),
    # c323（3行）＝公聴会の部屋（顔は束の段で升目 29か所）＝真ん中へ少し寄る
    "c323": dict(photo=_S9648, **ss.mv(_S9648, "in", fx=0.5, fy=0.5), side="none", color=1.0,
                 t="遮られた知らせ", s="米国上院の公聴会〈1912年4月・LOC〉"),
})
