# -*- coding: utf-8 -*-
"""第3章　衝突 c401–c416（16カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c4.py`）。
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
    'c401': dict(kind='フリー素材',
               plan='X-sea-stars｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 9.27秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：星の夜の海｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：⑤b で1本ずつ原寸｜新しい画（映像方針）：台本どおり（月の写らないもの）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.40（`There was no moon, the stars were out`）・G1 p.39（`there is not much wind`…`a flat calm`）'),
    'c402': dict(kind='写真',
               plan='S3-736:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：二等航海士と一等航海士〈1912年4月11日・クイーンズタウン〉｜動き：静止｜権利：PD｜時期：前｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S3-736 は c513 と2回｜新しい画（映像方針）：台本どおり（縦長・小さい＝高さいっぱいの額・静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.39（`if it becomes at all doubtful let me know at once`…`at 9.30 the master went to his room`…`to keep a sharp lookout for ice, particularly small ice and growlers`）'),
    'c403': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：船橋と見張り台の当直（航海士・操舵手・見張り・鐘と電話の線）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.39（`at 10 o'clock Mr. Lightoller handed over the watch to Mr. Murdoch, the first officer`…`we might be up around the ice any time now`）"),
    'c404': dict(kind='写真',
               plan='🔧 S1-076:全体｜一覧の種類：実写｜見せ方：全面｜副題：クイーンズタウンに着くタイタニック号〈1912年4月11日〉｜動き：左へ｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S1-017 は c415 へ｜新しい画（映像方針）：🔧 S1-017（岸壁に止まった船）→ 海を進む船（語り＝全速のまま）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.80（`about 22 knots`）・G2 p.4（`normal full speed (about 22 knots) was maintained`）'),
    'c405': dict(kind='写真',
               plan='🔧 S3-810:全体｜一覧の種類：実写｜見せ方：全面｜副題：見張りのフレデリック・フリート｜動き：寄る（顔へ）｜権利：PD｜時期：後・審問｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：撮影の時と所は ⑤b で（分かれば副題に年）｜時期の門番の例外＝見張り本人の肖像（審問のころの写真）＝場面の写真ではない（衝突の場面は c406〜c411 の模式）｜新しい画（映像方針）：🔧 額装 → 全面（2560px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.41（`three blows on the gong`…`Iceberg right ahead`）・G2 p.1（`at about 2340 hrs ship's time`）"),
    'c406': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：舵の号令（ハード・ア・スターボード）と左へ回る船首の矢印｜合図：🔁 横から→上から（前の図 c403）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.41（`almost simultaneously with the three-gong signal Mr. Murdoch, the officer of the watch, gave the order`）・G2 p.4（`because of the helm orders then in use, was to direct the ship's head to port`）"),
    'c407': dict(kind='写真',
               plan='S1-020:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：タイタニック号の船首〈1912年4月4日・サウサンプトン〉｜動き：静止｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（縦長＝高さいっぱいの額・静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.41（`Stop. full speed astern`…`the ship's head had fallen off about two points to port, when she collided with an iceberg well forward on her starboard side`）"),
    'c408': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：37秒の見積もり（オリンピック号の試験・約430メートル・約460メートル手前）｜新しい画（映像方針）：台本どおり（札に「見積もり」）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.41（`from various experiments subsequently made with the steamship Olympic, a sister ship to the Titanic`…`about 37 seconds would be required`）'),
    'c409': dict(kind='写真',
               plan='🔧 S5-365:全体｜一覧の種類：実写｜見せ方：全面｜副題：1912年4月20日の氷山〈ブレーメン号の船員が撮った〉｜動き：右へ｜権利：PD｜時期：氷｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 額装 → 全面｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.41（`500 yards was about the distance at which the`）'),
    'c410': dict(kind='写真',
               plan='🔧 S2-724:全体｜一覧の種類：実写｜見せ方：全面｜副題：船橋の船長〈1912年4月10日の朝〉｜動き：寄る｜権利：PD｜時期：前｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 額装 → 全面（2040px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.41（`The master rushed out onto the bridge`…`I hard-a-starboarded and reversed the engines, and I was going to hard-a-port round it, but she was too close`）'),
    'c411': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：船首から約90メートルの傷の範囲と前から6つの区画の名・10秒の帯｜合図：🔁 上から→横から（前の図 c408）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.42（`the damage extended over a length of about 300 feet`…`she would have passed through 300 feet in less than 10 seconds`）'),
    'c412': dict(kind='写真',
               plan='🔧 S10-871:全体｜一覧の種類：実写｜見せ方：全面｜副題：1912年の本の図〈An Unsinkable Titanic・p.129〉＝裂け目の札は本の見立て｜動き：右へ（区画に沿って）｜権利：PD｜時期：文書｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：⚠️ 「裂け目」は1912年の本の見立て（NIST は継ぎ目の開き＝legend §3-2）＝副題で断る｜新しい画（映像方針）：🔧 額装 → 全面（3170px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.45（`water came into the five forward compartments to a height of about 14 feet above the keel in the first 10 minutes`…`the ship's pumps could not possibly have coped`）"),
    'c413': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：壁で仕切った区画の並び・前の5つに水・壁を越えて後ろへ｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.45（`and so on in succession to the other boiler rooms till the ship would ultimately fill and sink`）'),
    'c414': dict(kind='フリー素材',
               plan='X-sea-calm｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 8.10秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：静かな夜の海｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜新しい画（映像方針）：台本どおり（月の写らないもの）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.4（`Between collision and foundering the ship lay stopped`）・G2 p.7（`the ship must have drifted some distance before she foundered`…`it is an important feature in this reappraisal`）'),
    'c415': dict(kind='写真',
               plan='🔧 S1-017:全体｜一覧の種類：実写｜見せ方：全面｜副題：サウサンプトンのタイタニック号〈1912年4月9日〉｜動き：右へ｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 S1-008（c304 の S1-013 と同じ写真）→ S1-017（別の写真）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.60（`The Titanic collided with the berg at 11.40`）・G1 p.49（`The collision took place at 11.40 p. m. (ship’s time)`）・G2 p.1（`at about 2340 hrs ship's time`）・G2 p.3（`struck the iceberg at 2345 hrs`）"),
    'c416': dict(kind='図解',
               plan='一覧の種類：帯｜見る向き：時間の線｜見た目の型：タイタニック号の時計の夜の帯（11:40・0:15・0:45ごろ・2:20）｜合図：🔁 横から→時間の線（前の図 c413）｜新しい画（映像方針）：台本どおり（札は「タイタニック号の時計」・ほかの船の時刻は並べない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.49（`at about 12.05 the order was given to uncover the 14 boats under davits`）・G1 p.54（`At 12.15 a. m. the distress signal CQD was sent`）・G1 p.85（`Two twenty a. m. (ship's time) April 15`）"),
}

SPEC = {}

# 🆕 ⑤b-2（2026-10-27）：c404 だけ先に書いた＝字幕の試し焼き（聞き役の赤「速さは、落としていたの？」と括弧つきの行「時速約41キロ（22ノット）」が
#   1カットにそろう＝冒頭 c101〜c107 に括弧の行が無い）。一覧どおり（全面・左へ・副題は list26 の sub）。⚠️ ⑤b-7 で写真をつなぐときに動きと寄せを見直してよい
_S1076 = P("s1_076")
SPEC.update({
    # c404（2行・4.6秒）＝クイーンズタウンに着くタイタニック号（船は y 0.30〜0.65）＝船の高さで左へ
    "c404": dict(photo=_S1076, **ss.mv(_S1076, "l", fy=0.47), side="none", color=1.0,
                 t="全速のまま", s="クイーンズタウンに着くタイタニック号〈1912年4月11日〉"),
})

# 🆕 ⑤b-3（2026-10-27）：フリー素材（Pexels・イメージ）＝`ss.vid`（見出し・副題は書かない＝左上の「イメージ」と出典だけ）。
#   区間と寄せは `qa_out/ep26_assets.py` の STOCK_WINDOW・STOCK_GEOM → footage.USE（月・人・字の無いことは 640px のシートで見た）
SPEC.update({
    "c401": ss.vid("c401"),
    "c414": ss.vid("c414"),
})

# 🆕 ⑤b-5（2026-10-28）：図解（`tools/mech26.py`・fig=("m26", …)）。段の数＝語りの行の数・画面の数は全部 rel に（門番 check_mech の judge_m26）
SPEC.update({
    # c403（2行）＝1行目「夜10時、当直は一等航海士…に替わった」→ 2行目「いつ氷のあたりに来てもおかしくない」で鐘と電話の線・「氷が近い」
    "c403": dict(
        t="当直の交代", s="4月14日の夜",
        fig=("m26", dict(view="watch", steps=[dict(state=dict(hand="on")), dict(state=dict(ice="on"))],
                         rel=[dict(t="22:00", src="G1 p39"), dict(t="見張り 2人", src="G1 p39")],
                         note="船の形と人の場所は模式", src=ss.src(["G1 p39"])))),
    # c406（2行）＝1行目「ほとんど同時に号令をかけた。ハード・ア・スターボード」→ 2行目「船首を左へ回す号令」で船が左へ回る
    "c406": dict(
        t="とっさの号令", s="見張りの知らせと、ほぼ同時に",
        fig=("m26", dict(view="helm", steps=[dict(state=dict(order="on")), dict(state=dict(turn="on"))],
                         rel=[], note="回る角度は模式（報告書は約2点＝約22度）", src=ss.src(["G1 p41", "G2 p2008"])))),
    # c408（3行）＝1行目の問い → 2行目「姉妹船オリンピック号の試験から見積もっている」→ 3行目「約22度…約37秒…約430メートル（466ヤード）」
    "c408": dict(
        t="ぶつかるまでの時間", s="姉妹船での試験から",
        fig=("m26", dict(view="olympic", steps=[dict(state=dict(q="on")), dict(state=dict(test="on")), dict(state=dict(path="on"))],
                         rel=[dict(t="約37秒", src="G1 p41"), dict(t="約22度", src="G1 p41"), dict(t="約430メートル", src="G1 p41"),
                              dict(t="466ヤード", src="G1 p41")],
                         note="見積もり（船の長さと道のりは同じ縮尺・回り方は模式）", src=ss.src(["G1 p41", "G1 p11"])))),
    # c411（2行）＝1行目「傷は、船の前の約90メートル（300フィート）の範囲に」→ 2行目「10秒もかからずに付いた傷」
    "c411": dict(
        t="右舷の底の傷", s="前から6つの区画",
        fig=("m26", dict(view="damage", steps=[dict(state=dict(dmg="on")), dict(state=dict(sec="on"))],
                         rel=[dict(t="約90メートル", src="G1 p42"), dict(t="300フィート", src="G1 p42"), dict(t="10秒たらず", src="G1 p42"),
                              dict(t="20ノットより速く", src="G1 p42"), dict(t="区画 前・1・2・3・6・5", src="G1 p42"),
                              dict(t="1〜3＝船倉　6と5＝ボイラー室", src="G1 p42")],
                         note="区画の境は模式（傷の長さは船の長さに比例）", src=ss.src(["G1 p42", "G1 p11"])))),
    # c413（3行）＝1行目の問い → 2行目「1つに水が入っても、ほかは守られる」→ 3行目「前の5つに入ると…順に後ろへ」
    "c413": dict(
        t="区画とは", s="水を止める作り",
        fig=("m26", dict(view="tray", steps=[dict(state=dict(q="on")), dict(state=dict(one="on")), dict(state=dict(five="on"))],
                         rel=[dict(t="1つに水", src="G1 p45"), dict(t="前の5つ", src="G1 p45")],
                         note="区画の数と形は模式", src=ss.src(["G1 p45"])))),
    # c416（2行）＝1行目「救命ボートを下ろす用意が始まり」で 0:05ごろ → 2行目「助けを呼ぶ通信が打たれる」で 0:15・0:45ごろ
    "c416": dict(
        t="船の中では", s="衝突から沈没まで",
        fig=("m26", dict(view="ttband", steps=[dict(state=dict(boat="on")), dict(state=dict(radio="on"))],
                         rel=[dict(t="23:40", src="G1 p42"), dict(t="0:05ごろ", src="G1 p49"), dict(t="0:15", src="G1 p54"),
                              dict(t="0:45ごろ", src="G1 p54"), dict(t="2:20", src="G1 p85")],
                         note="横は時刻に比例", src=ss.src(["G1 p42", "G1 p49", "G1 p54", "G1 p85"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-28）：写真（第3章の7カット）＝書き方は c2.py の ⑤b-7 の注と同じ
# ══════════════════════════════════════════════════════════
_S3736, _S3810, _S1020, _S5365, _S2724, _S10871, _S1017 = (P("s3_736"), P("s3_810"), P("s1_020"), P("s5_365"), P("s2_724"),
                                                           P("s10_871"), P("s1_017"))
SPEC.update({
    # c402（3行）＝戸口の2人（縦長・小さい 544×700）＝高さいっぱいの額・静止（c513 は2人の顔の高さの切り口）
    "c402": dict(photo=_S3736, panel=True, ground=dict(photo=_S3736), color=1.0,
                 t="見張りへの指示", s="二等航海士と一等航海士〈1912年4月11日・クイーンズタウン〉"),
    # c405（2行）＝見張りの顔（x 0.5・y 0.25）へ寄る
    "c405": dict(photo=_S3810, **ss.mv(_S3810, "in", fx=0.5, fy=0.3, z=1.3), side="none", color=1.0,
                 t="真正面に氷山", s="見張りのフレデリック・フリート"),
    "c407": dict(photo=_S1020, panel=True, ground=dict(photo=_S1020), color=1.0,
                 t="右舷の前がぶつかる", s="タイタニック号の船首〈1912年4月4日・サウサンプトン〉"),
    "c409": dict(photo=_S5365, **ss.mv(_S5365, "r"), side="none", color=1.0,
                 t="約460メートル手前", s="1912年4月20日の氷山〈ブレーメン号の船員が撮った〉"),
    # c410（3行）＝船橋の船長（x 0.2〜0.4・帽子 y 0.02）＝上半身へ寄る
    "c410": dict(photo=_S2724, **ss.mv(_S2724, "in", fx=0.32, fy=0.35, z=1.25), side="none", color=1.0,
                 t="近すぎた", s="船橋の船長〈1912年4月10日の朝〉"),
    # c412（2行）＝1912年の本の図の上の段（横から見た船・区画 1〜6・「LENGTH OF RENT IN SIDE PLATING」＝y 0.02〜0.50）。
    #   🔧 一覧は「全面・右へ」＝白い紙の線画を全面にすると見出し・章の札が図の線と字に重なる（25本目 ⑤b-7 の所見）＝額装・静止。下の2段（平面図）は外
    "c412": dict(photo=_S10871, trim=(0.0, 0.02, 1.0, 0.50), panel=True, pw=1640, color=1.0,
                 t="前の5区画に水", s="1912年の本の図〈An Unsinkable Titanic・p.129〉＝裂け目の札は本の見立て"),
    "c415": dict(photo=_S1017, **ss.mv(_S1017, "r"), side="none", color=1.0,
                 t="11時40分か45分か", s="サウサンプトンのタイタニック号〈1912年4月9日〉"),
})
