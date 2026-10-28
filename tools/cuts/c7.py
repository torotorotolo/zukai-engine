# -*- coding: utf-8 -*-
"""第6章　沈没と救助 c701–c718（18カット）。26本目（タイタニック号沈没事故・1912-04-14〜15）。

■ 🔴 2026-10-27（⑤b-1）：25本目（JR福知山線脱線事故）の中身を空にした＝git の `ef33e02c`（`git show ef33e02c:tools/cuts/c7.py`）。
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
    'c701': dict(kind='再現イラスト',
               plan='一覧の種類：案C-5｜見る向き：上から｜見た目の型：1号艇の40の席の印と、埋まった12（残り28は空席）｜合図：🔁 横から→上から（前の図 c639）｜新しい画（映像方針）：台本どおり（人の形で数を名乗らない）｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.51〜52（`No. 1 certainly left with only 12`…`emergency boat with a carrying capacity of 40`…`No. 7 left with only 27, and No. 6 with only 28`）'),
    'c702': dict(kind='図解',
               plan='一覧の種類：箱｜見る向き：正面｜見た目の型：1,178人ぶんの箱と、使われた3分の2に届かない量｜合図：🔁 上から→正面（前の図 c701）｜新しい画（映像方針）：台本どおり（人の形は使わない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.48（`Thus the total boat accommodation was for 1,178 persons`）・G1 p.76（`boat accommodation was utilized to less than two-thirds of its capacity`）・G1 p.51（`of the 712 persons saved only 652 could have left the`…`in boats`）'),
    'c703': dict(kind='写真',
               plan='S4-254:1面｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：ニューヨーク・タイムズ〈1912年4月15日〉｜動き：静止｜権利：PD｜時期：文書｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：✅ 10-27 原寸で読んだ＝「NEW YORK, MONDAY, APRIL 15, 1912.—EIGHTEEN PAGES.」・見出し「NEW LINER TITANIC HITS AN ICEBERG;」＝4月15日の第一報（Commons の橙の枠は切る）｜新しい画（映像方針）：台本どおり（縦長の紙面＝高さいっぱいの額・静止・橙の枠は切る）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.85（`Two twenty a. m. (ship's time) April 15`）・G2 p.1（`She foundered less than two-and-three-quarter hours later`）"),
    'c704': dict(kind='図解',
               plan='一覧の種類：棒｜見る向き：横から｜見た目の型：英国の審問の数の3本の棒（2,201・711・1,490）｜合図：🔁 正面→横から（前の図 c702）｜新しい画（映像方針）：台本どおり（人の形は使わない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`711 out of 2,201, or 32.30 per cent`）・G1 p.5（`the loss of 1,490 lives`）'),
    'c705': dict(kind='写真',
               plan='🔧 S9-645:全体｜一覧の種類：実写｜見せ方：全面｜副題：米国上院の公聴会〈1912年・英国の新聞の絵〉｜動き：右へ｜権利：PD｜時期：後・審問｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜書き起こしの断り：米国上院の調査の数は報告の書き起こし（有志のサイト）による｜注：S9-645 は c821 と2回｜新しい画（映像方針）：🔧 額装 → 全面（1329px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='T3 AmInqRep03（書き起こし＝乗っていた2,223・助かった706・亡くなった1,517）・legend §2-2（英米の差＝乗員885と899・一等325と329・三等706と710）'),
    'c706': dict(kind='図解',
               plan='一覧の種類：割合｜見る向き：横から｜見た目の型：等級ごとの助かった人の割合の帯（62%・41%・25%・24%）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.56（`212 out of 885, or 23.95 per cent`）・「一等62.46%・二等41.40%・三等25.21%」（G1 p.55＝頁の画像で確認＝sources.md §7）'),
    'c707': dict(kind='写真',
               plan='S6-383:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：カルパチア号の横のボート〈1912年4月15日〉｜動き：静止｜権利：PD｜時期：後・救助｜人：小さい（⑤b で原寸）｜出典の行：出典：オランダ国立公文書館（Spaarnestad Photo）｜注：人は小さい（⑤b で原寸）｜新しい画（映像方針）：台本どおり（縦長＝高さいっぱいの額・静止）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.55（`14 out of 168, or 8.33 per cent`）・「子ども57/109・成人女性316/425」（G1 p.56＝頁の画像で確認＝文字の層は「16 out of 425」に化ける）'),
    'c708': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：横から｜見た目の型：船の中の等級ごとの部屋の場所とボート甲板までの道のり｜新しい画（映像方針）：台本どおり（人は描かない）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.53（`There appears to have been no truth in these suggestions`…`by the difficulty of getting them up from their quarters, which were at the extreme ends of the ship`）'),
    'c709': dict(kind='写真',
               plan='🔧 S3-753:全体｜一覧の種類：実写｜見せ方：額装（高さいっぱい）｜副題：カルパチア号の船長アーサー・ロストロン〈1912年〉｜動き：静止｜権利：PD｜時期：後・NY｜人：乗員（顔可）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S3-753 は c916 と2回｜新しい画（映像方針）：🔧 船長の肖像を初出のこのカットへ（c504 から移した）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.55（`immediately ordered the ship to be turned around and driven at her highest`…`in the direction of the Titanic`）・G1 p.55（`saw a green flare which, as the evidence shows, was being sent up by Mr. Boxall in No. 2 boat`）'),
    'c710': dict(kind='図解',
               plan='一覧の種類：模式｜見る向き：上から｜見た目の型：カルパチア号から見た緑の灯（前の少し左）とまわりの氷山｜合図：🔁 横から→上から（前の図 c708）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.55（`From this time until 4 a. m. Capt. Rostron was altering his course continually in order to avoid icebergs`）・G7 p.25（`we were passing icebergs on every side`）'),
    'c711': dict(kind='写真',
               plan='🔧 S3-577:全体｜一覧の種類：実写｜見せ方：全面｜副題：カルパチア号の船長と航海士たち〈1912年・LOC〉｜動き：寄る｜権利：PD｜時期：後・NY｜人：乗員（顔可）｜出典の行：出典：米国議会図書館（LOC）｜書き起こしの断り：証言の言葉は英国の審問の書き起こし（有志のサイト）による｜新しい画（映像方針）：🔧 S5-362 の2回目 → カルパチア号の船長の写真（語り＝船長の証言）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='T1 Day 28 Q25552（書き起こし `We saw masthead lights quite distinctly of another steamer between us and the`…`That was about quarter-past three`）'),
    'c712': dict(kind='再現イラスト',
               plan='🔧 一覧の種類：案C-6｜見る向き：横から｜見た目の型：カルパチア号・4時10分・夜明け・2号艇を横に着ける｜合図：🔁 上から→横から（前の図 c710）｜新しい画（映像方針）：🔧 S3-577 → 案C-6（c713 から移した＝記録 G1 p.55「picked her up at 4.10」）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.55（`he stopped his ship at 4.05`…`He sighted the first boat (No. 2) and picked her up at 4.10`）'),
    'c713': dict(kind='写真',
               plan='🔧 S6-619:1枚目｜一覧の種類：実写｜見せ方：全面（切り出し）｜副題：ボートを積んだカルパチア号〈1912年・LOC〉｜動き：寄る｜権利：PD｜時期：後・救助｜人：小さい（⑤b で原寸）｜出典の行：出典：米国議会図書館（LOC）｜注：⚠️ どちらの1枚かは ⑤b で原寸（台紙の字は外す）｜新しい画（映像方針）：🔧 案C-6（c712 へ）→ LOC の台紙の写真の1枚（語り＝ボートを全部引き上げた）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.55（`The boats were scattered over an area of 4 or 5 miles, and it was 8 a. m. before they had all been picked up`）・G7 p.26（`all the people up aboard by 8.30`）'),
    'c714': dict(kind='写真',
               plan='🔧 S6-427:全体｜一覧の種類：実写｜見せ方：全面｜副題：カルパチア号の甲板〈1912年4月・LOC〉｜動き：寄る｜権利：PD｜時期：後・救助｜人：後ろ姿｜出典の行：出典：米国議会図書館（LOC）｜注：顔は見えない（⑤b で原寸）｜新しい画（映像方針）：🔧 S6-379 → カルパチア号の甲板の生存者（後ろ姿・語り＝カルパチア号に上がった712人）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.55（`712 persons, one of whom died shortly after`）'),
    'c715': dict(kind='写真',
               plan='🔧 S8-N04:全体｜一覧の種類：実写｜見せ方：額装（幅いっぱい）｜副題：マウント・テンプル号〈1900年代はじめ・テムズ川〉｜動き：静止｜権利：PD｜時期：別の年｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：🆕 了承②。約3.4：1 の横長＝幅いっぱいの額（上下は写真のぼかし）｜新しい画（映像方針）：🔧 S8-E03 → マウント・テンプル号（語りの船）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G1 p.59（`Capt. Lord stated that about 7.30`…`he passed the`…`Temple, stopped, and that she was in the vicinity of the`…`He saw no wreckage there`）・G2 p.15（`then steamed through the ice field to join CARPATHIA`）'),
    'c716': dict(kind='写真',
               plan='🔧 S8-E03:ダビットと船｜一覧の種類：実写｜見せ方：全面｜副題：カルパチア号の乗客が撮ったとされるカリフォルニアン号〈1912年4月15日〉｜動き：左へ｜権利：PD｜時期：後・救助｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：c106 と別の動き・別の寄り｜新しい画（映像方針）：🔧 S8-625 → S8-E03（本来の場面＝カルパチア号の甲板から朝のカリフォルニアン号）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G7 p.26（`At 8 o'clock the Leyland Line steamer Californian hove up, and we exchanged messages`…`I gave them the notes by semaphore about the Titanic going down, and that I had got all the passengers from the boats`）"),
    'c717': dict(kind='写真',
               plan='🔧 S6-379:全体｜一覧の種類：実写｜見せ方：全面｜副題：タイタニック号のボートを積んだカルパチア号〈1912年4月18日・ニューヨーク着の夜〉｜動き：右へ｜権利：PD｜時期：後・NY｜人：小さい（⑤b で原寸）｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S7-594 は c808 へ（副題で「着いた」と言わない）｜新しい画（映像方針）：🔧 S7-594（4月20日の写真＝着いた日でない）→ ニューヨーク着の夜の写真（語り＝ニューヨークへ運ばれた）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src="G1 p.55（`The court desires to record its great admiration of Capt. Rostron's conduct`）"),
    'c718': dict(kind='写真',
               plan='🔧 S6-372:全体｜一覧の種類：実写｜見せ方：全面｜副題：ニューヨークの桟橋のタイタニック号のボート〈1912年4月〉｜動き：寄る｜権利：PD｜時期：後・NY｜人：なし｜出典の行：Wikimedia Commons（パブリックドメイン）｜注：S6-372 は ca12 と2回｜新しい画（映像方針）：🔧 額装 → 全面（1627px の横長）｜台本の画＝台本 §4・一覧 eizou_list26.md（写さない）',
               src='G2 p.6（`The FI into the loss of TITANIC was ordered on 30 April 1912`）・G7 p.5（`FRIDAY, APRIL 19, 1912`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-27）：案C-5 1号艇の40の席＝K5（c701）／案C-6 カルパチア号＝K6（c712）（`tools/illu26.py`・門番 check_illu ㊽）
# ══════════════════════════════════════════════════════════
SPEC.update({
    # c701（3行・11.2秒）＝1行目の問いで1号艇と40の席の印 → 2行目「報告書によれば、40人乗りの1号艇は、12人だけで離れた。」で12の席が埋まる
    #   （人の形で数を名乗らない＝席の印・埋まった席の場所は模式）。3行目の7号艇・6号艇は語りに任せる
    "c701": dict(fig=("illu", dict(
        place="K5", start=dict(ksw="top"),
        steps=[dict(state=dict(), rec="G1 p52（this was an emergency boat with a carrying capacity of 40）",
                    tag=dict(t="1号艇（40人乗り）", at="seats", off=(60, -70), keep=True)),
               dict(state=dict(k5fill="on"), rec="G1 p51（No. 1 certainly left with only 12）",
                    tag=dict(t="乗ったのは12人", at="fill", off=(40, 80), keep=True))]))),
    # c712（1行・4.8秒）＝「4時5分に船を止め、4時10分、最初のボート、2号艇を引き上げた。」で2号艇が船の横へ・時計の札（カルパチア号の時計）
    "c712": dict(fig=("illu", dict(
        place="K6", start=dict(ksw="side"), at="4:10",
        steps=[dict(state=dict(k6boat="along"), dur=2.4, rec="G1 p55（He sighted the first boat (No. 2) and picked her up at 4.10）",
                    # 🔧 geom_gap：(640, 210) では時計の札が煙突の角に・「2号艇」が丸窓の列にかかった＝札は左上・ボートの札は水の上
                    tag=[dict(t="4:10（カルパチア号の時計）", xy=(300, 230), keep=True), dict(t="2号艇", at="boat", off=(60, 90), delay=2.0)])]))),
})

# 🆕 ⑤b-6（2026-10-28）：図解（`tools/mech26.py`・fig=("m26", …)）。段の数＝語りの行の数・画面の数は全部 rel に（門番 check_mech の judge_m26）
SPEC.update({
    # c702（2行）＝1行目「乗せられる量の3分の2に届かなかった」で3分の2の線と使われた量 → 2行目「ボートで離れたのは、多くて652人」
    "c702": dict(
        t="ボートの使われ方", s="使い切れなかった席",
        fig=("m26", dict(view="boxfill", steps=[dict(state=dict(two3="on")), dict(state=dict(num="on"))],
                         rel=[dict(t="1,178人ぶん", src="G1 p48"), dict(t="3分の2", src="G1 p76"), dict(t="多くて652人", src="G1 p51")],
                         note="箱の高さは人数に比例（離れた人は、あとで海から拾い上げた人を除いた数）", src=ss.src(["G1 p48", "G1 p51", "G1 p76"])))),
    # c704（2行）＝1行目「乗っていた2,201人のうち、助かったのは711人」→ 2行目「1,490人が亡くなった」で上の段が割れて床へ
    "c704": dict(
        t="乗っていた人の内訳", s="数え方は英国の報告書",
        fig=("m26", dict(view="split2", steps=[dict(state=dict(live="on")), dict(state=dict(lost="on"))],
                         rel=[dict(t="2,201人", src="G1 p56"), dict(t="711人", src="G1 p56"), dict(t="1,490人", src="G1 p5")],
                         note="棒の高さは人数に比例（711＋1,490＝2,201）", src=ss.src(["G1 p5", "G1 p56"])))),
    # c706（2行）＝1行目「一等は62%、二等は41%」→ 2行目「三等は25%。乗員は24%」
    "c706": dict(
        t="等級で違った割合", s="英国の審問の数から",
        fig=("m26", dict(view="rates4", steps=[dict(state=dict(a="on")), dict(state=dict(b="on"))],
                         rel=[dict(t="62%・41%・25%", src="G1 p55"), dict(t="24%", src="G1 p56")],
                         note="帯の長さは割合に比例（語りの丸め＝62.46・41.40・25.21・23.95）", src=ss.src(["G1 p55", "G1 p56"])))),
    # c708（3行）＝1行目「道をふさがれた、とよく語られる」→ 2行目 報告書「本当のことは無いようだ」で赤い棒が消える → 3行目 低い理由
    "c708": dict(
        t="三等の客の道", s="報告書の答え",
        fig=("m26", dict(view="decks", steps=[dict(state=dict(q="on")), dict(state=dict(rep="on")), dict(state=dict(far="on"))],
                         note="部屋の場所と道のりは模式（人は描かない）", src=ss.src(["G1 p53"])))),
    # c710（2行）＝1行目「2号艇の四等航海士が上げた、合図の灯」→ 2行目「4時まで…何度も向きを変えた」
    "c710": dict(
        t="前に見えた緑の灯", s="氷山の中を進む",
        fig=("m26", dict(view="flare_bow", steps=[dict(state=dict(flare="on")), dict(state=dict(zig="on"))],
                         rel=[dict(t="2号艇", src="G1 p55"), dict(t="4:00まで", src="G1 p55")],
                         note="船と氷山の位置は模式", src=ss.src(["G1 p55", "G7 p20025"])))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-28）：写真（第6章の11カット）＝書き方は c2.py の ⑤b-7 の注と同じ
# ══════════════════════════════════════════════════════════
_S4254, _S9645, _S6383, _S3753, _S3577, _S6619 = P("s4_254"), P("s9_645"), P("s6_383"), P("s3_753"), P("s3_577"), P("s6_619")
_S6427, _S8N04, _S8E03, _S6379, _S6372 = P("s6_427"), P("s8_n04"), P("s8_e03"), P("s6_379"), P("s6_372")
SPEC.update({
    # c703（2行）＝ニューヨーク・タイムズの1面（縦長）＝Commons の版の橙の枠を切る・高さいっぱいの額・静止
    #   🔧 ⑤c'（10-28）：1面まるごと（額 355×648）は本文 約7px・見出し 約23px で読めない → 題字・日付・4段の見出しだけ（束 y 48〜557＝
    #   「…BLURRED」の行の下 547 と罫 570 のあいだで切る・左右と上の橙の枠も外す）＝額 約1120×632・見出し 約68px（scratchpad c2/r8 の原寸）
    "c703": dict(photo=_S4254, trim=(0.061, 0.028, 0.943, 0.319), panel=True, ground=dict(photo=_S4254), color=1.0,
                 t="2時20分に沈む", s="ニューヨーク・タイムズ〈1912年4月15日〉"),
    # c705（3行）＝公聴会の絵＝右へ。右下の絵描きの署名（x 0.8・y 0.75〜0.8）は寄り 1.3・上寄せで窓の外（縦の窓 75%）
    "c705": dict(photo=_S9645, **ss.mv(_S9645, "r", fy=0.35, z=1.3), side="none", color=1.0,
                 t="少しずつ違う数", s="米国上院の公聴会〈1912年・英国の新聞の絵〉"),
    "c707": dict(photo=_S6383, panel=True, ground=dict(photo=_S6383), color=1.0,
                 t="168人のうち14人", s="カルパチア号の横のボート〈1912年4月15日〉"),
    "c709": dict(photo=_S3753, panel=True, ground=dict(photo=_S3753), color=1.0,
                 t="全速で救助へ", s="カルパチア号の船長アーサー・ロストロン〈1912年〉"),
    # c711（2行）＝船長と航海士たち（ガラス乾板・左右の黒い縁 3.2%・4.8%）＝引いた側の寄り lo 1.13 から真ん中へ寄る。
    #   上のネガの字（y 〜0.07）は窓の外（縦の窓 68%）
    "c711": dict(photo=_S3577, **ss.mv(_S3577, "in", fx=0.5, fy=0.48, z=1.3, lo=1.13), side="none", color=1.0,
                 t="あいだに別の灯", s="カルパチア号の船長と航海士たち〈1912年・LOC〉"),
    # c713（3行）＝LOC の台紙の左の1枚（x 0.05〜0.43・y 0.33〜0.67）の中だけを窓にする（寄り 2.9〜3.1＝窓の横 0.35・縦 0.24）。
    #   台紙の番号と書き込み・右の1枚は窓の外。⚠️ SPEC の trim＋cam（ss.tcam）は門番 photo_edge が切り口を見ずに測る＝寄りだけで書いた
    #   試し焼き 40636765032 では y 0.50 の窓が煙突とマストに寄り、ボートを積んだ甲板が窓の下の端だった＝縦の真ん中を 0.53→0.55 へ下げた
    "c713": dict(photo=_S6619, **ss.mvz(_S6619, (0.24, 0.53, 2.9), (0.26, 0.55, 3.1)), side="none", color=1.0,
                 t="朝までの引き上げ", s="ボートを積んだカルパチア号〈1912年・LOC〉"),
    # c714（2行）＝甲板の生存者（顔は束の段で升目）＝寄る。上の題字（y 〜0.08）と右の端の書き込み（x 0.95〜）は窓の外・
    #   ガラス乾板の黒い縁（左 2.6%・右 3.3%）＝引いた側の寄り lo 1.09
    "c714": dict(photo=_S6427, **ss.mv(_S6427, "in", fx=0.5, fy=0.55, z=1.2, lo=1.09), side="none", color=1.0,
                 t="救われた712人", s="カルパチア号の甲板〈1912年4月・LOC〉"),
    # c715（2行）＝約3.4：1 の横長＝幅いっぱいの額（上下は同じ写真のぼかし）・静止
    "c715": dict(photo=_S8N04, panel=True, pw=1640, ground=dict(photo=_S8N04), color=1.0,
                 t="何も無い海", s="マウント・テンプル号〈テムズ川〉"),   # 撮影年は出どころの表に無い（門番 credits）＝年を書かない
    "c716": dict(photo=_S8E03, **ss.mv(_S8E03, "l", fy=0.47), side="none", color=1.0,
                 t="朝8時に姿を見せる", s="カルパチア号の乗客が1912年4月15日に撮ったとされるカリフォルニアン号"),
    "c717": dict(photo=_S6379, **ss.mv(_S6379, "r"), side="none", color=1.0,
                 t="ニューヨークへ", s="タイタニック号のボートを積んだカルパチア号〈1912年4月18日・ニューヨーク着の夜〉"),
    "c718": dict(photo=_S6372, **ss.mv(_S6372, "in", fx=0.55, fy=0.5), side="none", color=1.0,
                 t="調べが始まる", s="ニューヨークの桟橋のタイタニック号のボート〈1912年4月〉"),
})
