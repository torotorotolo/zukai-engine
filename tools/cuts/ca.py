# -*- coding: utf-8 -*-
"""第9章　事故のあとの決まり ca01–ca13（13カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/ca.py`）。
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
    'ca01': dict(kind='写真',
               plan='S2-E01:通信士｜一覧の種類：実写｜見せ方：全面｜副題：1912年の船の無線室〈姉妹船オリンピック号・1912年の本の写真〉｜動き：寄る（通信士へ）｜権利：PD｜時期：別の船｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（2回目・c616 と別の寄り・同じ副題）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.85（`passenger and emigrant steamships`）・G1 p.87（`worked with a sufficient number of trained operators to secure a continuous service by night and day`）'),
    'ca02': dict(kind='文字の頁',
               plan='P-G4-2｜一覧の種類：頁｜見せ方：頁｜副題：米国の法 37 Stat. 199｜動き：寄る（「two or more persons」の行へ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：米国の法 37 Stat. 199（1912年7月23日）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G4（`two or more persons skilled in the use of such apparatus, one or the other of whom shall be`…`on duty at all times while the vessel is being navigated`…`approved, July 23, 1912`）'),
    'ca03': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：1910年の法と1912年の法（眠る1人の影と交代で起きている2人の影）｜合図：🔁 時間の線→横から（前の図 c940）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G6（`in charge of a person skilled in the use of such apparatus`）'),
    'ca04': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見る向き：横から｜見た目の型：無線室と船橋をつなぐ線（電話と伝声管・いつでも話せる）｜新しい画（映像方針）：🔧 S3-352（通信士の肖像）→ 模式（亡くなった通信士の肖像に条文の語りを重ねない＝台本 §0-5）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G4（`the operator in the radio room and the bridge shall be maintained at all times`）'),
    'ca05': dict(kind='写真',
               plan='S4-300:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：陸の無線局〈1912年4月18日の米国の新聞〉｜動き：静止｜権利：PD｜時期：文書｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S4-300 は1回（c310 は電報に替えた）・ケープ・レースとは名乗らない｜新しい画（映像方針）：台本どおり（ほぼ正方形の紙面＝高さいっぱいの額・静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G5（`All stations are required to give absolute priority to signals`…`and radiograms relating to ships in distress; to cease all sending on`…`hearing a distress signal`）'),
    'ca06': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：氷の知らせがあるときの夜の進み方（速さを落とす船と針路を変える船の2つの矢印）｜合図：🔁 横から→上から（前の図 ca04）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.87（`when ice is reported in or near the track the ship should proceed in the dark hours at a moderate speed or alter her course so as to go well clear of the danger zone`）'),
    'ca07': dict(kind='写真',
               plan='🔧 S6-377:全体｜一覧の種類：実写｜見せ方：全面｜副題：ニューヨークのピア54 のタイタニック号のボート〈1912年4月〉｜動き：右へ｜権利：PD｜時期：後・NY｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 S2-054 の2回目 → ニューヨークに残ったボート（語り＝全員のぶんのボート）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.86（`That the accommodation should be sufficient for all persons on board`）・G1 p.78（`Had a boat drill been held on board`…`No. (d) The carrying capacity`）'),
    'ca08': dict(kind='図解',
               plan='一覧の種類：年表｜見る向き：時間の線｜見た目の型：事故のあとの決まりの年表（1912年7月・8月・1913年・1914年・1948年）｜合図：🔁 上から→時間の線（前の図 ca06）｜新しい画（映像方針）：台本どおり（c902 の年表と色と並びを替える）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='U1（`RCS assumed the responsibility of monitoring iceberg activity from the U.S. Navy`…`officially established by the Safety of Life at Sea (SOLAS) Convention`・web）'),
    'ca09': dict(kind='写真',
               plan='S12-913:全体｜一覧の種類：実写｜見せ方：全面｜副題：国際氷山監視の会議〈1923年・LOC〉｜動き：寄る｜権利：PD｜時期：別の年｜人：公的な任務（顔可）｜出典の行：出典：米国議会図書館（LOC）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='U1（`The tragedy led to the creation of the International Ice Patrol`・web）'),
    'ca10': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：遭難の信号の色の2つの夜空（1912年は何色でもよい・1948年から赤）｜合図：🔁 時間の線→正面（前の図 ca08）｜新しい画（映像方針）：台本どおり（c516 の模式と別の絵）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.18（`it was not until 1948 that the rules for distress signals were amended`）・「red」（G2 p.18＝文字の層で欠け・頁の画像で確認＝sources.md §2-0）'),
    'ca11': dict(kind='フリー素材',
               plan='X-flare-red｜映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・月の写らないもの・要る秒＝扉を除いた中身 7.51秒＝narration.json の実測）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜空に上がる赤い光｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：⑤b で1本ずつ｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.18（`Had that rule been in force in 1912, when it was much more needed than now, Mr Stone would surely not have remained passive`）'),
    'ca12': dict(kind='写真',
               plan='S6-372:寄り｜一覧の種類：実写｜見せ方：全面｜副題：ニューヨークの桟橋のタイタニック号のボート〈1912年4月〉｜動き：左へ｜権利：PD｜時期：後・NY｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（2回目・c718 と別の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='—'),
    'ca13': dict(kind='写真',
               plan='🔧 N04:F｜映像の素材 3.90秒・倍率 1.03（素材の区間の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で・音は使わない＝-an）｜一覧の種類：実写｜見せ方：映像（全面＝上下を少し切る）｜副題：海の底のタイタニック号〈2004年・NOAA ほか〉｜動き：映像（139.5〜143.4秒）｜権利：courtesy（NOAA・copyright の語なし）｜時期：海底｜人：なし｜出典の行：Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.｜新しい画（映像方針）：🔧 S11-910 の2回目 → NOAA の甲板の区間｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.19（`A final word seems called for on the aftermath of the FI and its finding so far as Captain Lord is concerned`）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-10-27）：フリー素材（Pexels・イメージ）＝`ss.vid`（見出し・副題は書かない＝左上の「イメージ」と出典だけ）。
#   区間と寄せ（左の灯りの列と下の対岸の町の灯りを画面の外へ）は `qa_out/ep26_assets.py` の STOCK_WINDOW・STOCK_GEOM → footage.USE
SPEC.update({
    "ca11": ss.vid("ca11"),
})
