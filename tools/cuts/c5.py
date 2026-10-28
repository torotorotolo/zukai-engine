# -*- coding: utf-8 -*-
"""第4章　遭難の信号 c501–c520（20カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c5.py`）。
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
    'c501': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：CQD のモールスの点と線・電鍵・四方への電波の輪｜合図：🔁 時間の線→正面（前の図 c416）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`At 12.15 a. m. the distress signal CQD was sent. This was heard by several steamships and by Cape Race`）'),
    'c502': dict(kind='写真',
               plan='S3-784:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：四等航海士ジョセフ・ボックスホール｜動き：静止｜権利：PD｜時期：別の年｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：撮影の年は ⑤b で（船員の登録の写真）。出典の「書き起こし」は語らない（語りは G1 p.54・G7 p.23）＝断りは要らない｜新しい画（映像方針）：台本どおり（縦長・小さい＝高さいっぱいの額・静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`By 12.25 Mr. Boxall, the fourth officer, had worked out the correct position of the Titanic`…`Come at once, we have struck a berg`）・G7 p.23（`requiring immediate assistance and giving me his position`）・T1 Day 13 Q15391（書き起こし `I submitted the position to the Captain first, and he told me to take it to the marconi room`）'),
    'c503': dict(kind='写真',
               plan='🔧 S10-905:地図｜一覧の種類：実写｜見せ方：全面（切り出し）｜副題：1912年の新聞の地図〈船の位置は当時の報道の見立て〉｜動き：寄る（タイタニック号の印へ）｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：オランダ国立公文書館（Spaarnestad Photo）｜注：S10-905 は c814 と2回｜新しい画（映像方針）：🔧 額装 → 全面の切り出し（3508px の地図の部分）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`had worked out the correct position of the Titanic`）・G2 p.2（`discovered the wreck of TITANIC, in a position some 13 miles from that accepted by the 1912 Inquiry`）'),
    'c504': dict(kind='写真',
               plan='🔧 S8-N03:全体｜一覧の種類：実写｜見せ方：全面｜副題：カルパチア号｜動き：右へ｜権利：PD｜時期：別の年｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：🆕 了承②。✅ 10-27 何の絵か確かめた（1本煙突・4本マスト・右下に番号「2349」＝寄りで外す）。⚠️ 撮影年は ⑤b（出どころの頁で分かれば副題に年）｜新しい画（映像方針）：🔧 S3-753（船長の肖像）→ 海上のカルパチア号（語り＝船そのもの・行き先と距離。船長の肖像は c709）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`This was heard by the Cunard steamer Carpathia, which was at this time bound from New York to Liverpool and 58 miles away. The Carpathia answered, saying that she was coming to the a`）'),
    'c505': dict(kind='図解',
               plan='一覧の種類：航路｜見る向き：上から｜見た目の型：カルパチア号の向かい方（北52度西へ約107キロ・途中の氷山の印）｜合図：🔁 正面→上から（前の図 c501）｜新しい画（映像方針）：台本どおり（札は「カルパチア号の時計」）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G7 p.23（`Yes, 12.35; that was our apparent time`…`Immediately on getting the message, I gave the order to turn the ship around`）・G7 p.24（`The course was north 52 degrees west true 58 miles from my position`）'),
    'c506': dict(kind='再現イラスト',
               plan='一覧の種類：案C-3｜見る向き：横から｜見た目の型：カリフォルニアン号の無線室・寝台で眠る通信士・机の上のヘッドホン｜合図：🔁 上から→横から（前の図 c505）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`The Californian heard none of the`…`she had only one Marconi operator on board and he was asleep`）'),
    'c507': dict(kind='写真',
               plan='🔧 S4-320:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：ビルマ号が受けたタイタニック号の遭難の電報〈1912年4月15日・英国立公文書館〉｜動き：静止｜権利：PD｜時期：文書｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：🔴 字は ⑤b で原寸（台本 §0-5）・⚠️ 権利は英国立公文書館の頁の条件を ⑤b で｜新しい画（映像方針）：🔧 「We are sinking fast」の行に寄る → 静止（額装は動かさない）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='materials.md §1-5 S4-320（見本帳で「SOS SOS CQD CQD - MGY」「We are sinking fast passengers being put into boats」の字を読んだ）'),
    'c508': dict(kind='再現イラスト',
               plan='一覧の種類：案C-4｜見る向き：横から｜見た目の型：タイタニック号のボート甲板・0時45分ごろ・1号艇のそばの筒から信号弾・白い星｜新しい画（映像方針）：台本どおり（乗客は顔の無い群れ）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`sent off at intervals from a socket by No. 1 emergency boat on the boat deck. They were the ordinary distress signals, exploding in the air and throwing off white stars`）'),
    'c509': dict(kind='写真',
               plan='🔧 S2-054:ダビット｜一覧の種類：実写｜見せ方：全面｜副題：ボート甲板の救命ボート〈1912年4月11日〉｜動き：寄る（ダビットへ）｜権利：PD｜時期：前｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S2-070 は c518（2号艇の語り）へ｜新しい画（映像方針）：🔧 S2-070（副題が2号艇・語りは7号艇）→ ボート甲板の写真の寄り（番号を名乗らない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`began about the time that No. 7 boat was lowered (12.45 a. m.), and it continued until Mr. Boxall left the ship at about 1.45`）'),
    'c510': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：信号弾の数の2つの札（報告書 約8発・四等航海士 6発から12発）と5分の札｜合図：🔁 横から→正面（前の図 c508）｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`In all, Mr. Boxall fired about eight rockets`）・T1 Day 13 Q15395（書き起こし `between half a dozen and a dozen`）・T1 Day 13 Q15399（書き起こし `probably five minutes`）'),
    'c511': dict(kind='写真',
               plan='🔧 S3-424:全体｜一覧の種類：実写｜見せ方：全面｜副題：生き残った4人の航海士〈1912年〉｜動き：寄る（四等航海士へ）｜権利：PD｜時期：後・審問｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：語りは米国の公聴会（G7 p.914＝公式の印刷）。寄る先の人の並びは ⑤b で原寸｜新しい画（映像方針）：🔧 S3-784 の2回目 → 4人の航海士の写真（四等航海士を含む）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G7 p.914（`Just white stars, bright. I do not know whether they were stars or bright balls`…`They were the regulation distress signals`…`Oh, no; not red`）'),
    'c512': dict(kind='再現イラスト',
               plan='🔧 一覧の種類：案C-4｜見る向き：横から｜見た目の型：同じボート甲板・モールス灯で前の左の灯を呼ぶ四等航海士・小さな白い点と赤い点｜合図：🔁 正面→横から（前の図 c510）｜新しい画（映像方針）：🔧 モールス灯は船橋の脇の屋根の上に描く（G1 p.16・p.54＝台本 §0-5）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`Mr. Boxall was also using a Morse light`…`a ship whose lights he saw about half a point on the port bow of the Titanic at a distance, as he thought, of about 5 or 6 miles`）'),
    'c513': dict(kind='写真',
               plan='🔧 S3-736:二等航海士｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：二等航海士と一等航海士〈1912年4月11日・クイーンズタウン〉｜動き：静止｜権利：PD｜時期：前｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜注：c402 と同じ写真・同じ副題（額の中の寄りだけ替える＝静止）｜新しい画（映像方針）：🔧 S3-424（c511 へ）→ 二等航海士の写真（語り＝二等航海士の証言）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`He got no answer`）・T1 Day 12 Q14138（書き起こし `A white light about two points on the port bow`）'),
    'c514': dict(kind='文字の頁',
               plan='P-G1-054｜一覧の種類：頁｜見せ方：頁｜副題：英国の審問の報告 p.54｜動き：寄る（「There appears to be no doubt」の一文へ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：英国の審問の報告（米国上院の刷り直し S. Doc. 933）p.54｜新しい画（映像方針）：台本どおり（There の行から入れる）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`There appears to be no doubt that the vessel whose lights he saw was the Californian`）'),
    'c515': dict(kind='写真',
               plan='N04:C｜映像の素材 7.60秒・倍率 1.02（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（70.0〜77.6秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：台本どおり（区間＝舷側の手すりに沿って）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.12（`What is significant, however, is that no ship was seen by TITANIC until well after the collision`）'),
    'c516': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：遭難の信号の色（白い星と、色とりどりの信号を並べる）｜合図：🔁 横から→正面（前の図 c512）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.18（`such signals could be of any colour`…`there was therefore nothing immediately to distinguish them from other rockets`）'),
    'c517': dict(kind='フリー素材',
               plan='X-flare-white｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 8.37秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜空に上がる白い光｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：⑤b で1本ずつ（月なし・白一色）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.14（`rockets were much more used than is now the case for reasons other than indicating distress`）'),
    'c518': dict(kind='写真',
               plan='🔧 S2-070:全体｜一覧の種類：実写｜見せ方：全面｜副題：タイタニック号の左舷の前のボート〈1912年4月〉｜動き：寄る｜権利：PD｜時期：前｜人：後ろ姿｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：置き場の説明は「2号艇」＝副題では番号を名乗らない。S6-427 は c714 へ｜新しい画（映像方針）：🔧 S6-427（カルパチア号の甲板＝後の場面）→ 左舷の前のボート（語り＝2号艇で船を離れた）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`until Mr. Boxall left the ship at about 1.45`）・G1 p.55（`a green flare which, as the evidence shows, was being sent up by Mr. Boxall in No. 2 boat`）'),
    'c519': dict(kind='写真',
               plan='🔧 S2-045:ボート｜一覧の種類：実写｜見せ方：全面｜副題：二等の遊歩甲板とボート甲板〈1912年4月11日〉｜動き：右へ（ボートの列へ）｜権利：PD｜時期：前｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：c207 と同じ写真・同じ副題・別の寄り｜新しい画（映像方針）：🔧 S6-384（カルパチア号に吊り上げたボート＝後の場面）→ ボート甲板の寄り（語り＝下ろす場面）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.50（`at about 12.45 Mr. Murdoch gave the order to lower No. 7 boat`）・G1 p.52（`No. 7 left with only 27, and No. 6 with only 28`…`must have left only partly filled`）'),
    'c520': dict(kind='写真',
               plan='🔧 S8-630:船体｜一覧の種類：実写｜見せ方：全面｜副題：カリフォルニアン号〈1907年〉｜動き：寄る｜権利：PD｜時期：別の年｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 S8-625 の2回目 → S8-630（S8-625 を4回までにする）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.54（`The evidence from the Californian speaks of eight rockets`）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-10-27）：フリー素材（Pexels・イメージ）＝`ss.vid`（見出し・副題は書かない＝左上の「イメージ」と出典だけ）。
#   区間（白い筋が上がる所だけ・0.6倍）は `qa_out/ep26_assets.py` の STOCK_WINDOW → footage.USE
SPEC.update({
    "c517": ss.vid("c517"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-27）：案C-3 無線室＝K3（c506）／案C-4 タイタニック号のボート甲板＝K4（c508 deck・c512 wing）
#  （`tools/illu26.py`・門番 check_illu ㊽）
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c506（2行・6.5秒）＝1行目の問い → 2行目「聞いていない。その船の通信士は1人だけで、眠っていた。」で寝台の通信士と机の上のヘッドホンに札
    "c506": dict(fig=("illu", dict(
        place="K3", start=dict(k3op="sleep", ksw="side"), at="23:30",
        rec="G1 p57（Evans heard the Titanic continuing to communicate with Cape Race up to the time he turned in at 11.30 p. m.）",
        people=dict(crew=(1, "G1 p54（she had only one Marconi operator on board and he was asleep）")),
        steps=[dict(state=dict()),
               dict(state=dict(), rec="G1 p54（The Californian heard none of the…she had only one Marconi operator on board and he was asleep）",
                    # 🔧 試し焼き 40594842436：左上へ出した「ヘッドホン」の字が機械の目盛りに重なった＝右上へ
                    tag=[dict(t="通信士", at="sleep", off=(60, -60)), dict(t="ヘッドホン", at="phones", off=(60, -90))])]))),
    # c508（2行・8.1秒）＝1行目「無線のほかに、目で見える合図も使った。信号弾だ。」で時計の札 → 2行目「ボート甲板の筒から打ち上げると、
    #   空で破裂して、白い星を散らす。」で筒から上がる筋と、空で破裂して白い星。乗客は顔の無い群れ（数えられない形）
    #   🔧 試し焼き 40594842436：破裂を3つ目の段（行の途中に挟まる）にしたら終わりのコマでも小さく薄かった＝2行目の段で筋→破裂
    "c508": dict(fig=("illu", dict(
        place="K4", start=dict(view="deck", k4crowd="on", ksw="titanic"), at="0:45",
        rec="G1 p54（The firing of these signals began about the time that No. 7 boat was lowered (12.45 a. m.)）",
        steps=[dict(state=dict(), rec="G1 p54（The firing of these signals began about the time that No. 7 boat was lowered (12.45 a. m.)）",
                    tag=dict(t="0:45ごろ（タイタニック号の時計）", xy=(640, 210), keep=True)),
               dict(state=dict(k4rocket="burst"),
                    rec="G1 p54（sent off at intervals from a socket by No. 1 emergency boat on the boat deck. They were the ordinary distress signals, "
                        "exploding in the air and throwing off white stars）",
                    # 🔧 geom_gap：右上 (40, -90) では「信号弾の筒」の字を筋が横切った＝筋の下の右へ
                    tag=[dict(t="1号艇", at="boat", off=(40, -70)), dict(t="信号弾の筒", at="socket", off=(40, -10))])]))),
    # c512（3行・11.9秒）＝1行目「四等航海士は、モールス灯も使った。光を点けたり消したりして、」で屋根の上の灯が点いたり消えたり →
    #   2行目「…前の左の方に、船の灯りが見えていた。」で遠くの白い点と赤い点 → 3行目「本人の見立てで、約9キロから11キロ（5か6マイル）先」で点線と札
    #   （モールス灯は船橋の端の屋根の上＝G1 p16・p54＝台本 §0-5。遠くの船は灯の点だけ＝名乗らない）
    "c512": dict(fig=("illu", dict(
        place="K4", start=dict(view="wing", ksw="side"), at="0:45",
        people=dict(crew=(1, "G1 p54（Mr. Boxall was also using a Morse light from the bridge）")),
        steps=[dict(state=dict(k4lamp="blink"), rec="G1 p54（Mr. Boxall was also using a Morse light from the bridge）",
                    tag=dict(t="四等航海士", at="off4", off=(60, -40))),
               dict(state=dict(k4far="on"), rec="G1 p54（a ship whose lights he saw about half a point on the port bow of the Titanic）",
                    tag=dict(t="船の灯り", at="far", off=(50, -80))),
               dict(state=dict(k4dist="on"), rec="G1 p54（at a distance, as he thought, of about 5 or 6 miles）",
                    tag=dict(t="約9〜11キロ（本人の見立て）", at="dist", off=(-40, -90)))]))),
})

# 🆕 ⑤b-5（2026-10-28）：図解（`tools/mech26.py`・fig=("m26", …)）。段の数＝語りの行の数・画面の数は全部 rel に（門番 check_mech の judge_m26）
SPEC.update({
    # c501（3行）＝1行目の問い → 2行目「タイタニック号の時計で0時15分、遭難の合図CQDを打った」→ 3行目「いくつもの船と、陸のケープ・レースが…聞いた」
    "c501": dict(
        t="助けを呼ぶ無線", s="タイタニック号の無線室から",
        fig=("m26", dict(view="cqd", steps=[dict(state=dict(q="on")), dict(state=dict(code="on")), dict(state=dict(out="on"))],
                         rel=[dict(t="0:15", src="G1 p54")], note="符号の点と線は国際の決まり・電波の線は模式", src=ss.src(["G1 p54"])))),
    # c505（2行）＝1行目「カルパチア号の時計で0時35分に受けると、」→ 2行目「すぐ船を回せ…北西へ、約107キロ先の位置を目指した」
    "c505": dict(
        t="向かったカルパチア号", s="知らせを受けて、すぐに",
        fig=("m26", dict(view="carp", steps=[dict(state=dict(get="on")), dict(state=dict(turn="on"))],
                         rel=[dict(t="0:35", src="G7 p20023"), dict(t="北から西へ52度", src="G7 p20024"), dict(t="約107キロ", src="G7 p20024")],
                         note="向きは記録の値（距離の線の長さと氷山の場所は模式）", src=ss.src(["G7 p20023", "G7 p20024"])))),
    # c510（3行）＝1行目の問い → 2行目「報告書は、約8発とみる。」→ 3行目「6発から12発、間隔はたぶん5分」（四等航海士の証言）
    "c510": dict(
        t="何発打ったのか", s="報告書と証言",
        fig=("m26", dict(view="rockets_n", steps=[dict(state=dict(q="on")), dict(state=dict(rep="on")), dict(state=dict(say="on"))],
                         rel=[dict(t="約8発", src="G1 p54"), dict(t="6発から12発", src="T1 p15395"), dict(t="間隔は たぶん5分", src="T1 p15399")],
                         note="証言の言葉は英国の審問の書き起こし（有志のサイト）による", src=ss.src(["G1 p54", "T1 p15395", "T1 p15399"])))),
    # c516（3行）＝1行目の問い → 2行目「遭難の信号の色は、何色でもよかった」→ 3行目「タイタニック号のは白…見分けがつかない」
    "c516": dict(
        t="白い光の意味", s="1912年の遭難の信号",
        fig=("m26", dict(view="colors", steps=[dict(state=dict(q="on")), dict(state=dict(any="on")), dict(state=dict(white="on"))],
                         rel=[], note="色の並びは模式", src=ss.src(["G2 p2022"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-28）：写真・頁・NOAA の映像（第4章の12カット）＝書き方は c2.py の ⑤b-7 の注と同じ
# ══════════════════════════════════════════════════════════
#   NOAA 2004 の映像（c515）＝`ss.vid`（footage.USE の EP26_USE＝`qa_out/ep26_assets.py use`・ひかえの静止画 `ref/ep26/fb_c515.jpg`＝`… fb`）
_S3784, _S10905, _S8N03, _S4320, _S2054, _S3424 = P("s3_784"), P("s10_905"), P("s8_n03"), P("s4_320"), P("s2_054"), P("s3_424")
_S3736, _PG1054, _S2070, _S2045, _S8630 = P("s3_736"), P("p_g1_054"), P("s2_070"), P("s2_045"), P("s8_630")
SPEC.update({
    "c502": dict(photo=_S3784, panel=True, ground=dict(photo=_S3784), color=1.0,
                 t="位置を計算した", s="四等航海士ジョセフ・ボックスホール"),
    # c503（2行）＝新聞の地図の「TITANIC」の船の印（x 0.74・y 0.69）へ寄る（c814 はほかの船の印を右へ）。
    #   寄り 1.0 から寄ると、字幕の帯の上の辺と窓の辺が地名の行を切った（門番 edges・slide G-10）＝寄り 1.4 の窓から 1.7 へ（scratchpad `fit_cam2.py`）
    "c503": dict(photo=_S10905, **ss.mvz(_S10905, (0.68, 0.64, 1.4), (0.73, 0.70, 1.7)), side="none", color=1.0,
                 t="ずれていた位置", s="1912年の新聞の地図〈船の位置は当時の報道の見立て〉"),
    # c504（3行）＝船（y 0.15〜0.75）＝右へ。右下の番号「2349」（x 0.95・y 0.86〜0.90）は寄り 1.2・上寄せで窓の外（縦の窓 83%＝y 0〜0.83）
    "c504": dict(photo=_S8N03, **ss.mv(_S8N03, "r", fy=0.35, z=1.2, span=(0.2, 0.75)), side="none", color=1.0,
                 t="約107キロ先の船", s="カルパチア号"),
    "c507": dict(photo=_S4320, panel=True, ground=dict(photo=_S4320), color=1.0,
                 t="残っている電報", s="ビルマ号が受けたタイタニック号の遭難の電報〈1912年4月15日・英国立公文書館〉"),
    # c509（2行）＝左のダビットとボート（x 0.0〜0.2・y 0.3〜0.6）へ寄る（c208 と同じ写真・同じ副題・もう一段）
    "c509": dict(photo=_S2054, **ss.mv(_S2054, "in", fx=0.14, fy=0.45, z=1.4), side="none", color=1.0,
                 t="打ち上げの始まり", s="ボート甲板の救命ボート〈1912年4月11日〉"),
    # c511（2行）＝4人の航海士。⚠️ どの人が四等航海士かは束の出どころ（Commons の題）に無い＝特定の1人へ寄らず、4人の顔の高さへ少し寄る
    "c511": dict(photo=_S3424, **ss.mv(_S3424, "in", fx=0.5, fy=0.4), side="none", color=1.0,
                 t="白い信号弾", s="生き残った4人の航海士〈1912年〉"),
    # c513（3行）＝c402 と同じ写真・同じ副題＝額の中の切り口を2人の顔の高さ（y 0.28〜0.72）に替える（静止）。
    #   ⚠️ どちらが二等航海士かは出どころの題に無い＝1人に切らない
    "c513": dict(photo=_S3736, trim=(0.0, 0.28, 1.0, 0.72), panel=True, ground=dict(photo=_S3736), color=1.0,
                 t="答えの無い灯り", s="二等航海士と一等航海士〈1912年4月11日・クイーンズタウン〉"),
    # c514（2行）＝報告書 p.54「…There appears to be no doubt that the vessel whose lights he saw was the Californian.」の3行
    #   切り口＝`pbox P-G1-054 "got no answer" "The evidence from"`
    "c514": dict(photo=_PG1054, trim=(0.007, 0.788, 0.970, 0.840), panel=True, pw=1640, color=1.0,
                 t="灯りの船の正体", s="見えた灯りの船についての一文"),
    # c515（2行）＝NOAA 2004 の映像 70.0〜77.6秒（舷側の手すりに沿って）
    "c515": dict(**ss.vid("c515", t="問い直される一文", s="海の底のタイタニック号〈2004年・NOAA ほか〉"), side="none"),
    # c518（2行）＝ダビットに吊ったボート（x 0.35〜0.95・y 0.2〜0.7）へ寄る。左の人は後ろ姿
    "c518": dict(photo=_S2070, **ss.mv(_S2070, "in", fx=0.65, fy=0.42, z=1.2), side="none", color=1.0,
                 t="2号艇で離れる", s="タイタニック号の左舷の前のボート〈1912年4月〉"),
    # c519（3行）＝c207 と同じ写真・同じ副題＝右のボートの列（x 0.8〜1.0）へ寄りながら流す
    "c519": dict(photo=_S2045, **ss.mvz(_S2045, (0.62, 0.5, 1.25), (0.85, 0.45, 1.4)), side="none", color=1.0,
                 t="空きのあるボート", s="二等の遊歩甲板とボート甲板〈1912年4月11日〉"),
    "c520": dict(photo=_S8630, **ss.mv(_S8630, "in", fx=0.45, fy=0.6, z=1.2), side="none", color=1.0,
                 t="見ていた人たち", s="カリフォルニアン号〈1907年〉"),
})
