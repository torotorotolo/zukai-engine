# -*- coding: utf-8 -*-
"""第1章　処女航海 c201–c220（20カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c2.py`）。
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
    'c201': dict(kind='写真',
               plan='S1-042:全体｜一覧の種類：実写｜見せ方：全面｜副題：ベルファストを出るタイタニック号〈1912年4月2日・北アイルランド国立博物館〉｜動き：寄る（船へ）｜権利：PD｜時期：前｜人：なし｜出典の行：出典：北アイルランド国立博物館（Harland & Wolff Collection）｜注：左下の整理番号「H1721 H.W.」は寄りで外す｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.11（`a three-screw vessel of 46,328 tons gross`…`for the White Star Line service between Southampton and New York`）'),
    'c202': dict(kind='図解',
               plan='🔧 一覧の種類：比べ｜見る向き：横から｜見た目の型：トン数の2本の棒（タイタニック号 46,328・カリフォルニアン号 6,223・2色）｜新しい画（映像方針）：🔧 「2隻の写真の小さな切り抜きを添える」→ 棒だけ（写真の切り抜きを図に重ねない＝S8-625 の使い回しを増やさない・船の形は c317）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.11（`46,328 tons gross`）・G1 p.56（`a vessel of 6,223 tons`）'),
    'c203': dict(kind='写真',
               plan='S1-016:全体｜一覧の種類：実写｜見せ方：全面｜副題：サウサンプトンを出るタイタニック号〈1912年4月10日〉｜動き：左へ｜権利：PD｜時期：前｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.33（`The Titanic left Southampton on Wednesday, April 10`）・G2 p.1（`on her maiden voyage from Southampton towards New York`）'),
    'c204': dict(kind='写真',
               plan='S1-053:全体｜一覧の種類：実写｜見せ方：全面｜副題：最初の寄港地へ〈1912年4月10日〉｜動き：右へ｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：台本どおり（動きを右へ＝「寄る」に偏らせない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.33（`after calling at Cherbourg, proceeded to Queenstown`）'),
    'c205': dict(kind='写真',
               plan='S1-084:全体｜一覧の種類：実写｜見せ方：全面｜副題：クイーンズタウンのタイタニック号〈1912年4月11日・オランダ国立公文書館〉｜動き：寄る（船尾の字へ）｜権利：PD｜時期：前｜人：小さい（⑤b で原寸）｜出典の行：出典：オランダ国立公文書館（Spaarnestad Photo）｜注：✅ 船尾の「TITANIC」「LIVERPOOL」の字は 10-27 に原寸で読めた（1920px の版の x1350〜1800・y680〜980）。字は小さい＝寄りは船尾の全体まで（拡大しすぎない）。手すりの乗客は小さい（⑤b で原寸）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.33（`from which port she sailed on the afternoon of Thursday, April 11`）・G1 p.11（`registered as a British steamship at the port of Liverpool`）'),
    'c206': dict(kind='図解',
               plan='一覧の種類：棒｜見る向き：横から｜見た目の型：乗っていた人の4本の棒（一等・二等・三等・乗員・合計 2,201）｜新しい画（映像方針）：台本どおり（人の形は使わない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.32（`In all, 2,201 persons were on board`）・「乗員885・乗客1,316・子ども109」（p.32＝頁の画像で確認＝sources.md §3・§7）'),
    'c207': dict(kind='写真',
               plan='S2-045:全体｜一覧の種類：実写｜見せ方：全面｜副題：二等の遊歩甲板とボート甲板〈1912年4月11日〉｜動き：右へ｜権利：PD｜時期：前｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：乗客は小さい＝顔が分かれば顔だけモザイク（PD）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='「一等325・二等285・三等706」（G1 p.32＝頁の画像で確認＝sources.md §7）'),
    'c208': dict(kind='写真',
               plan='S2-054:全体｜一覧の種類：実写｜見せ方：全面｜副題：ボート甲板の救命ボート〈1912年4月11日〉｜動き：寄る｜権利：PD｜時期：前｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S2-054 は c509（ダビットの寄り）と2回｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.25（`for 1,178 persons`）'),
    'c209': dict(kind='図解',
               plan='🔧 一覧の種類：箱｜見る向き：上から｜見た目の型：ボート20隻を大きさの違う3種の箱で（14・2・4）｜合図：🔁 横から→上から（前の図 c206）｜新しい画（映像方針）：🔧 札＝語りの呼び方「大きなボート（65人乗り）14隻・小さめのボート（40人乗り）2隻・折りたたみ式（47人乗り）4隻」（救命艇・カッターの語は札に出さない＝台本 §0-5）・人の形は使わない｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.25（`a total of 11,327.9 cubic feet for 1,178 persons`）・「救命艇14隻×65人・カッター2隻×40人・折りたたみ艇4隻×47人」（p.25＝sources.md §3）'),
    'c210': dict(kind='図解',
               plan='一覧の種類：比べ｜見る向き：横から｜見た目の型：ボートの量の3本の棒（962・1,178・2,201）｜合図：🔁 上から→横から（前の図 c209）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.62（`a provision for 962 persons`…`1,178 persons, a number far in excess of the requirements of the table`）'),
    'c211': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：正面｜見た目の型：1894年の規則の表の段と、表の外へ伸びる 4万6,328トンの印｜合図：🔁 横から→正面（前の図 c210）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.64（`Those regulations were last revised in 1894`）・G1 p.63（`made in 1894 for vessels of 10,000 tons and upward`）'),
    'c212': dict(kind='写真',
               plan='S1-089:全体｜一覧の種類：実写｜見せ方：全面｜副題：試運転の日のタイタニック号〈1912年4月2日〉｜動き：右へ｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.76（`to revise the rules of 1894 and this, I think, was blameable`…`doubtful whether even if the rules had been revised`）'),
    'c213': dict(kind='写真',
               plan='S1-032:全体｜一覧の種類：実写｜見せ方：全面｜副題：航海の途中の港で〈1912年4月〉｜動き：右へ｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜注：撮影者がタイタニック号の乗客（クイーンズタウンで降りた）＝来歴でタイタニック号（オリンピック号はその場にいない）。港は名乗らない｜新しい画（映像方針）：台本どおり（港は名乗らない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='T1 Day 16 Q18755（書き起こし `the ship was looked upon as practically unsinkable`）'),
    'c214': dict(kind='写真',
               plan='🔧 S4-264:見出し｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：英国の新聞〈1912年4月16日〉｜動き：静止｜権利：PD｜時期：文書｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：✅ 10-27 原寸で読んだ＝見出し「THE VESSEL UNSINKABLE.」・「(CENTRAL NEWS TELEGRAM.) NEW YORK, MONDAY.」。🔴 本文の頭の行（y286〜）に会社の人の名前と肩書（International Mercantile Marine Company の vice president＝台本は「会社の副社長」と簡単にした形）＝名前の行は切り出しの外（肩書は語りで言う）｜新しい画（映像方針）：🔧 寄る → 静止（額装の写真は動かさない＝10-26）・切り出し＝見出しから日付の行まで（1300px の原本の y100〜280）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='materials.md §1-5 S4-264（The Manchester Guardian 1912-04-16 p.9＝見出しの字は見本帳で読んだ）'),
    'c215': dict(kind='文字の頁',
               plan='P-G1-076｜一覧の種類：頁｜見せ方：頁｜副題：英国の審問の報告 p.76｜動き：寄る（「unsinkable」と「for all on board」の一文へ）｜見た目の型：文字の頁｜権利：PD｜時期：文書｜人：なし｜出典の行：出典：英国の審問の報告（米国上院の刷り直し S. Doc. 933）p.76｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.76（`When naval architects have devised practical means`…`rendering ships unsinkable`…`be carried for all on board`）'),
    'c216': dict(kind='写真',
               plan='🔧 S3-714:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：タイタニック号の船長エドワード・スミス〈1912年4月・ニューヨーク・タイムズに載った写真〉｜動き：静止｜権利：PD｜時期：前｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜新しい画（映像方針）：🔧 副題に名前（語りが名前を言う）・縦長＝高さいっぱいの額・静止｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.32（`the master, Edward Charles Smith, held an extra master's certificate`）・「乗員885＝甲板66・機関325・司厨494」（p.32＝sources.md §7）"),
    'c217': dict(kind='写真',
               plan='S2-033:船橋｜一覧の種類：実写｜見せ方：全面｜副題：船橋と見張り台〈1912年4月10日〉｜動き：上へ（船橋から見張り台へ）｜権利：PD｜時期：前｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S1-002（c101・cb07）の一部を拡大した版＝離して使う（c922 で見張り台の寄り）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.41（`a telephone message to the bridge`）・G2 p.4（`the lookouts saw an iceberg ahead`）'),
    'c218': dict(kind='図解',
               plan='🔧 GS-route｜一覧の種類：衛星｜見せ方：衛星（帰属の行）｜動き：左へ（大西洋を西へ）｜見る向き：上から｜見た目の型：北大西洋の航路の線（衛星写真・3つの寄港地と4月14日の位置の帯）｜合図：🔁 正面→上から（前の図 c211）｜権利：Google の地図の利用（帰属の行を出し続ける）｜時期：今｜人：なし｜出典の行：Google の地図（衛星写真）＋描き足し｜注：帰属の行を絵の近くに出し続ける・色を変えない（⑤b-1 で撮る）｜新しい画（映像方針）：🔧 図の航路 → 衛星写真＋描き足し（25本目からの既定＝記憶 feedback-jiko-maps-use-satellite）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.35（`The Titanic followed the outward southern track until Sunday, April 14, in the usual way`）'),
    'c219': dict(kind='写真',
               plan='S1-057:全体｜一覧の種類：実写｜見せ方：全面｜副題：タイタニック号の甲板から〈1912年4月10日〉｜動き：下へ｜権利：PD｜時期：前｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：人は小さい（⑤b で原寸）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.35（`At 11.40 p m. on that day she struck an iceberg`）・G1 p.39（`all knew on the Sunday evening that the vessel was entering a region where ice might be expected`）'),
    'c220': dict(kind='写真',
               plan='🔧 S2-206:全体｜一覧の種類：実写｜見せ方：全面｜副題：タイタニック号の無線室とされる写真〈1912年4月〉｜動き：寄る（机へ）｜権利：PD｜時期：前｜人：乗員（後ろ姿）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S2-206 は c321 と2回｜新しい画（映像方針）：🔧 額装 → 全面（1280px の横長＝写真は画面いっぱい）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.35（`a wireless message from the steamship Caronia was received by Capt. Smith`）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-10-27）：地図（衛星写真＋描き足し＝`ss.sat`・寄らない・色を変えない）。札に数字を置かない（日付は語り）
SPEC.update({
    # c218（2行・8.2秒）＝1行目「いつもの航路で、大西洋を西へ」で港と航路 → 2行目「4月14日…氷山にぶつかる」で×
    #   航路＝G1 p.33：寄港（サウサンプトン → シェルブール → クイーンズタウン）→ ファストネット灯台から曲がり角まで大圏 → その先はニューヨークへ（破線＝行き着かなかった）
    "c218": dict(
        **ss.sat("G01", steps=[
            [dict(k="line", path=("southampton", "cherbourg", "queenstown") + ss.SAT_LINES["gc"] + ("collision",), role="ship",
                  t="いつもの航路", u=0.7, lab=(0, -26, "middle")),
             dict(k="line", path=("collision", "newyork"), role="ship", dash=True),
             # ヨーロッパは Google の地名が多い（イギリス・アイルランド・フランス）＝港の札は 26px で、地名の字と重ねない向きへ（確かめ用の重ね絵で見た）
             dict(k="pt", at="southampton", c="INK_W", t="サウサンプトン", size=26, lab=(6, -46, "start")),
             dict(k="pt", at="cherbourg", c="INK_W", t="シェルブール", size=26, lab=(6, 34, "start")),
             dict(k="pt", at="queenstown", c="INK_W", t="クイーンズタウン", size=26, lab=(-40, -24, "end")),
             dict(k="pt", at="newyork", c="INK_W", t="ニューヨーク", lab=(0, 46, "middle"))],
            [dict(k="x", at="collision", t="氷山にぶつかった所", lab=(0, 50, "middle"))]],
            note="港は一般の座標・" + ss.SAT_LINE_NOTE),
        t="大西洋を西へ", s="北大西洋（現在の衛星写真）"),
})
