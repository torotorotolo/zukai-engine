# -*- coding: utf-8 -*-
"""第1章　タイタニックへの観光潜航 c201–c219（19カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c2.py`）。
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
    'c201': dict(kind='写真',
               plan='C201｜見せ方：額装（共同）｜副題：タイタニックの船首（2004年の調査）｜動き：額ごと寄る｜権利：共同（NOAA と Institute for Exploration・University of Rhode Island＝連邦の外の機関を含む＝A の見込みは弱い）｜出典の行：NOAA/Institute for Exploration/University of Rhode Island（2004年）｜注：2004年6月 ROV「Hercules」が撮影（Commons の説明）・NOAA と連邦の外の機関の共同＝額装・サムネに使わない｜台本の画：実写 タイタニックの船首（Commons「Titanic wreck bow.jpg」・2004年の調査・クレジット「Courtesy of NOAA/Institute for Exploration/University of Rhode Island」＝A の見込みは弱い＝出典の書き方と額装か全面かは映像方針で＝副題「タイタニックの船首（2004年の調査）」）',
               src='TSB §1.3（`a descent of approximately 3800 m`）'),
    'c202': dict(kind='図解',
               plan='台本の画：図 模式 富士山（3,776m）を逆さにした高さと、タイタニックの深さ（約3,800m）の比べ・横に1円玉と乗用車の札（式は §9）',
               src='NTSB p.10（`At the depth of the Titanic wreckage site, water pressure is 5,554.5 pounds per square inch.`）'),
    'c203': dict(kind='図解',
               plan='台本の画：図 再現 3つの報告書（表紙の題と日付だけを並べた図＝米沿岸警備隊の海難調査委員会 2025年8月／米国の運輸安全委員会 2025年10月／カナダの運輸安全委員会 2026年6月）',
               src='USCG p.5〈v〉（`August 4, 2025`）・NTSB p.76（`Report Date: October 2, 2025`）・TSB §4.2.4（`It was officially released on 17 June 2026.`）'),
    'c204': dict(kind='図解',
               plan='🔧 G01｜注：🔧 自作の地図→衛星写真（了承② 10-14 カズヤくん「衛星写真・撮るのは⑤b-1」）｜新しい画（映像方針）：図 地図 Google マップの衛星写真 G01（北米の東半分）＋描き足し＝会社の本社エバレット（白の点）・母船の港セントジョンズ（白の点）・タイタニックの位置（赤の×）の3点だけ・副題「現在の衛星写真」・右下の帰属の行を残す｜台本の画（🔧映像方針で替えた＝元の予定）：図 地図 北米の東半分（会社の本社＝米国ワシントン州エバレット・母船の港＝カナダのセントジョンズ・タイタニックの位置の3点だけ）',
               src='TSB §1.23（`OceanGate was first established as a limited liability company in 2009`）・§1.23（`OceanGate was headquartered in Everett, Washington`）'),
    'c205': dict(kind='図解',
               plan='台本の画：図 線 タイタンの横から見た線画（NTSB 図3 をなぞる・全長6.7m と「5人まで」の札だけ）',
               src='NTSB p.10（`The 22-foot-long submersible Titan was designed, built, and operated by OceanGate Inc.`）・TSB §1.2.1（`designed to accommodate up to 5 people`）'),
    'c206': dict(kind='図解',
               plan='台本の画：図 線 同じ線画（人が乗る部分＝筒と両端のドームを明るく・札「炭素繊維の筒」「チタンのドーム」）',
               src='TSB §1.10.1（`The Titan’s pressure hull consisted of a carbon fibre cylinder that was capped at either end by titanium domes.`）・§1.2.1（`Two hemispherical domes made of titanium were fitted to either end of the cylinder.`）'),
    'c207': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3 職の表）｜新しい画（映像方針）：図 模式 組織の図（2023年の上級の8つの職を席の箱で並べる＝埋まった席は会社の橙・空いた席は灰の点線・CEO の席を明るく・TSB 表4 の値・英字の表は画面に出さない）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 TSB 表4（2023年の上級の8つの職と、その席が埋まっていたか＝欄は英字のまま・CEO の行を明るく）',
               src='TSB §1.3（`the Titan’s pilot, who was OceanGate’s chief executive officer (CEO)`）・§1.9.1（`had piloted it on numerous previous dives, including dives to the Titanic in 2021 and 2022`）・§1.23.1（`As a small company, OceanGate was led primarily by the CEO.`）・§1.23.1（`The CEO was integrated into all aspects of the company, including human resources, finance, operations, and submersible design and construction.`）'),
    'c208': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3）｜新しい画（映像方針）：図 模式 同じ組織の図＋社員の人の印15（数は黄）と「実験的」の札｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表4（2023年の潜航の季節の初めの社員の数「15」の札を足す）',
               src='TSB §1.23（`At the beginning of the 2023 operating season, OceanGate had 15 employees`）・§1.23.1（`viewed the design, development, and operation of the Titan as being experimental`）・§1.23.1（`There was no precedent for diving a human-occupied carbon fibre submersible to the deep ocean`）'),
    'c209': dict(kind='図解',
               plan='台本の画：図 再現 同意書の要点（USCG p.71 の箇条の英字＝`experimental submersible vessel`・`not been certified by any regulatory body`・「death」の数え＝9）',
               src='USCG p.71〈63〉（`The submersible had not been certified by any regulatory body.`）・p.71〈63〉（`A portion of the expedition would be conducted inside an experimental submersible vessel.`）・p.71〈63〉（`The liability waiver mentions death 9 times`）'),
    'c210': dict(kind='図解',
               plan='台本の画：図 棒 参加費（2021年 105,129ドル → 2022年・2023年 25万ドル＝円は1ドル140円で計算と左下に）',
               src='USCG p.64〈56〉（`rising from $105,129 in 2021 to $250,000 for both 2022 and 2023.`）・TSB §1.23（`the cost for 1 passenger to join was up to 250 000 U.S. dollars`）'),
    'c211': dict(kind='図解',
               plan='台本の画：図 再現 会社の計画書の一節（NTSB 脚注8 が引く `guests who help fund OceanGate expeditions` の英字＋訳は字幕）',
               src='NTSB p.15（`OceanGate referred to its clients as “mission specialists.”`）・USCG p.300〈292〉（`reclassifying their passengers as “mission specialists” to conceal their illegal passenger operations`）・USCG p.317〈309〉（`to conceal that their mission specialists were actually paying passengers`）'),
    'c212': dict(kind='図解',
               plan='台本の画：図 再現 TSB 付録B の表（27行・欄は英字のまま＝日付・深さ・時間・人数・母船・目的・備考）',
               src='TSB 付録B（`The term “dive” refers to dives to any depth where there were people on board the submersible and the submersible was on life support.`）・付録B（`Dives made by the Titan between 2021 and the occurrence at the Titanic wreck site, in Canadian waters, or in Canada’s exclusive economic zone`）'),
    'c213': dict(kind='図解',
               plan='🔧 注：🔧 再現→模式（§0-3 潜航の表は c212 の1回だけ）｜新しい画（映像方針）：図 模式 点の並び（付録B の潜航を1回1点で年ごとに並べ、深さ3,840m に届いた13回を海の青で明るく・届かなかった回は灰）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表（深さ「3840」の13行を明るく）',
               src='NTSB p.14（`only successfully completed 13 dives to the wreck`）'),
    'c214': dict(kind='図解',
               plan='🔧 注：🔧 再現→帯（§0-3）｜新しい画（映像方針）：図 帯 2021年の潜航の年表（1つ目の点に赤の印「回収のときに前のドームが外れた」→「留めるボルトを18本に」の札）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表（1行目の備考 `Forward dome fell off the submersible during recovery` を明るく）',
               src='TSB 付録B（`Forward dome fell off the submersible during recovery`）・TSB（`Following this dive, OceanGate began using 18 securing bolts.`）'),
    'c215': dict(kind='図解',
               plan='🔧 注：🔧 再現→帯（§0-3）｜新しい画（映像方針）：図 帯 同じ年表（赤の印「電池が切れた」・「27時間」は黄）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表（`Batteries died on approach to LARS`・時間「27」を明るく）',
               src='TSB 付録B（`Batteries died on approach to LARS`）・NTSB p.36（`so the Titan remained on the surface with occupants aboard overnight.`）'),
    'c216': dict(kind='図解',
               plan='🔧 注：🔧 再現→帯（§0-3）｜新しい画（映像方針）：図 帯 同じ年表（推進器・重り・通信の不具合の赤の印が並ぶ）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 同じ表（推進器・重り・追跡と通信の備考を明るく）',
               src='TSB 付録B（`Starboard thrusters failed`）・付録B（`Incident with drop weight`）・TSB §1.23.1（`OceanGate primarily used a trial-and-error approach to operations`）'),
    'c217': dict(kind='写真',
               plan='M65｜見せ方：全面｜副題：前の艇 サイクロプス1 の操縦の道具（2023年10月撮影）｜動き：右へ｜権利：A（MBI が撮影）｜出典の行：米沿岸警備隊 海難調査委員会の報告書 図65｜注：MBI 図65 の凡例＝2023-10-26 に MBI が撮影（Logitech のゲーム機用のコントローラー）｜台本の画：実写 MBI 図65 前の艇 Cyclops I の中のコントローラーとキーボード（USCG 報告 p.103・2023年10月に MBI が撮影・A＝副題「前の艇 サイクロプス1 の操縦の道具（2023年10月撮影）」）',
               src='TSB §1.10.5（`The pilot operated the thrusters using a handheld wireless controller`）・NTSB p.11（`a wireless, battery-operated controller that communicated with control software`）・USCG p.103〈95〉（`the CYCLOPS I being operated with a PlayStation® controller`）・USCG p.103〈95〉（`Photo of the Logitech PlayStation controller inside CYCLOPS I taken by the MBI`）'),
    'c218': dict(kind='写真',
               plan='C218｜見せ方：額装（BY-SA）｜副題：2021・22年の遠征の母船（写真は2022年）｜動き：額ごと寄る（写真は常に全部見える）｜権利：BY-SA 4.0｜出典の行：（撮影者＝src/credits_private.tsv）／CC BY-SA 4.0｜注：CC BY-SA 4.0＝無加工・切らない・色も重ねもしない・寄り0（額ごと動かす）。Commons の 2022-08-21 02（01 は船尾に橙の物）｜台本の画：実写 ホライゾン・アークティック（Commons・CC BY-SA 4.0・2022年＝第三者＝額装・改変なし・サムネに使わない＝副題「2021・22年の遠征の母船」）',
               src='TSB §1.2.2（`In previous years, OceanGate had chartered another vessel, the Horizon Arctic`）'),
    'c219': dict(kind='図解',
               plan='🔧 G02｜注：🔧 自作の地図→衛星写真（了承②）｜新しい画（映像方針）：図 地図 衛星写真 G02（セントジョンズ→タイタニックの眠る海）＋水色の点線（母船）・白の点・赤の×・黄の「約700〜800km」＝見本 sat_c219 の形｜台本の画（🔧映像方針で替えた＝元の予定）：図 地図 セントジョンズからタイタニックの現場まで（約685km の線）',
               src='TSB §1.2.2（`OceanGate first chartered the Polar Prince in March 2023.`）・USCG p.5〈v〉（`approximately 370 nautical miles`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-14）：地図のカット＝衛星写真の額装＋描き足し（`tools/satmap.py`・門番 `tools/check_sat.py`）
# ══════════════════════════════════════════════════════════
#   🔴 衛星写真は公開リポに置かない（Modal の保管庫）＝Actions では理由を出して飛ばす・検品画像は Modal の qa。
#      額は帯より上（ロゴと帰属の行を字幕の帯の下に入れない）・色を変えない・寄らない。場所は `ss.GEO`（確かめていない所に点を置かない）
_N_SITE = "点は一般の座標・×は最後に受けた位置（米沿岸警備隊）"
_N_ROUTE = "セントジョンズは一般の座標・×は最後に受けた位置・線は2点を結んだだけ（実際の航路ではない）"
SPEC.update({
    # c204（2行）＝1行目で遠征の港と事故の現場（タイタンが潜った海）・2行目で本社（ワシントン州エバレット）
    "c204": dict(**ss.sat("G01", note=_N_SITE, steps=[
        [dict(k="x", at="site", t="タイタニックの眠る海", lab=(0, 52, "middle")),
         dict(k="pt", at="stjohns", c="INK_W", t="セントジョンズ", lab=(-18, -20, "end"))],
        [dict(k="pt", at="everett", role="company", t="本社（エバレット）", lab=(18, 46, "start"))]]),
        t="会社と現場", s="北アメリカ（現在の衛星写真）"),
    # c219（2行）＝1行目で母船の港（地図の側に「セント・ジョンズ」の地名がある＝札は船の名）・2行目で現場までの線と道のり（数は黄）
    "c219": dict(**ss.sat("G02", note=_N_ROUTE, steps=[
        [dict(k="pt", at="stjohns", role="ship", t="ポーラープリンス", lab=(60, -30, "start"))],
        [dict(k="line", path=("stjohns", "site"), role="ship", dash=True, t="約700〜800キロ", lc="AMBER", lab=(30, 12, "start")),
         dict(k="x", at="site", t="事故の現場", lab=(24, 12, "start"))]]),
        t="現場までの海", s="セントジョンズから現場へ（現在の衛星写真）"),
})

# ── 🆕 ⑤b-3（2026-10-14）：写真のカット（映像方針の一覧＝了承②・副題は焼いた絵を原寸で見てから最終に）──
#   額装だけ（共同＝c201・BY-SA＝c218）は panel=True・color=1.0・寄り0・1点1カット＝`ss.check_frame_only`・動きは額ごと（fmove）
#   報告書の図の幅 1280 未満は kind() が額装を返す＝映像方針で「全面」（幅 1000 以上）の図は panel を書かずに全面（c217）
_BOW = P("commons_titanic_wreck_bow")
_CTL = P("mbi_fig065_cyclops_controller")
_HAR = P("commons_horizon_arctic_2022_02")
SPEC.update({
    # c201（8.5秒）＝聞き役の問い＋答え。タイタニックの船首（2004年 ROV Hercules・NOAA と連邦の外の機関の共同＝額装だけ）・額ごと寄る
    #   章の扉の地は方眼だけ（card_mix=0＝額装だけの点を扉の地に染めて混ぜない・映像方針 §4「扉を方眼だけ」）
    "c201": dict(photo=_BOW, panel=True, color=1.0, fmove=ss.fm("in"), card_mix=0, t="深い海の底", s="タイタニックの船首（2004年の調査）"),
    # c217（11.3秒）＝MBI 図65（前の艇サイクロプス1 の中のコントローラー・2023-10-26 に MBI が撮影）・幅 1200＝映像方針で全面・右へ
    "c217": dict(photo=_CTL, **ss.mv(_CTL, "r"), side="none", t="操縦の道具", s="前の艇 サイクロプス1 の操縦の道具（2023年10月撮影）"),
    # c218（4.4秒）＝ホライゾン・アークティック（CC BY-SA 4.0＝額装・無加工・寄り0）・額ごと寄る
    "c218": dict(photo=_HAR, panel=True, color=1.0, fmove=ss.fm("in"), t="前の年の母船", s="2021・22年の遠征の母船（写真は2022年）"),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3b（2026-10-14）：図解 第1章（14カット）＝模式図 `tools/mech22.py`（fig=("m22", …)）・棒（qty）
# ══════════════════════════════════════════════════════════
#   🔴 色は役の色（会社＝橙・潜水艇＝白・米沿岸警備隊＝青・米運輸安全委員会＝緑・カナダ＝紫）。章の札「タイタニックへの観光潜航」と4字以上同じ並びを
#      見出し・副題に入れない（門番 dup）。CEO の名前は画面に出さない（語りだけ）。段の数＝語りの行の数
#   🔧 c213〜c216：映像方針の「帯」（2021年の年表）→ **点の並び（dives）**＝付録B を読むと「電池が切れて27時間」は 2022-06-20・推進器と通信は
#      2022年にも並ぶ＝2021〜22年の日付の軸では夏ごとに点が固まって読めない。点の色は映像方針の「海の青」→ **潜水艇の白**（青は米沿岸警備隊の役の色と取り違える）
_N_TT = "形は NTSB 図3 の比（模式）"
SPEC.update({
    # c202（2行）＝深さの物差し（逆さの富士山とタイタニックの深さ）→ 水の重さ → 1円玉と乗用車（約1.2トン＝台本 §9 の式＝5,554.5 psi × 1円玉の面積）
    "c202": dict(
        t="水圧", s="深い海の底で",          # ⚠️ 門番 dup：「水の重さ」は図の札・「約3,800メートル」は図の札の写し
        fig=("m22", dict(view="fuji", steps=[dict(state=dict(press="on")),
                                             dict(state=dict(coin="on"), tag=dict(t="約1.2トン", at="t"))],
                         rel=[dict(t="約1.2トン", src="NTSB p1010（5,554.5 psi×1円玉の面積＝台本 §9）")],
                         note="富士山は国土地理院の値・形と1円玉の大きさは模式", src=ss.src(["NTSB p1010", "TSB §1.3"]))),
    ),
    # c203（3行）＝3つの報告書の表紙（題と年月だけ）。2行目で米国の2つ・3行目でカナダ
    "c203": dict(
        t="3つの報告書", s="調べた3つの機関",          # ⚠️ 門番 wording：「この動画」は楽屋の言葉
        fig=("m22", dict(view="reports", steps=[dict(), dict(state=dict(r1="on", r2="on")), dict(state=dict(r3="on"))],
                         note="表紙は模式（題と年月だけ）", src=ss.src(["USCG p5", "NTSB p1076", "TSB §4.2.4"]))),
    ),
    # c205（2行）＝横から見たタイタン（NTSB 図3 の比）・全長6.7メートル・5人まで
    "c205": dict(
        t="潜水艇タイタン", s="横から見た形",
        fig=("m22", dict(view="side", steps=[dict(state=dict(dim="on"), tag=dict(t="5人まで", at="cap")), dict()],
                         rel=[dict(t="5人", src="TSB §1.2.1"), dict(t="6.7メートル", src="NTSB p1010（22-foot）")],
                         note=_N_TT, src=ss.src(["NTSB p1010", "NTSB p1012", "TSB §1.2.1"]))),
    ),
    # c206（2行）＝人が乗る部分（炭素繊維の筒と両端のチタンのドーム＝耐圧殻）
    "c206": dict(
        t="人が乗る部分", s="2つの材料",
        fig=("m22", dict(view="side", steps=[dict(state=dict(hull="on", mat="on")), dict(tag=dict(t="耐圧殻", at="tag", to="hull"))],
                         note=_N_TT, src=ss.src(["TSB §1.10.1", "TSB §1.2.1"]))),
    ),
    # c207（3行）＝2023年の上級の8つの職の席（TSB 表4＝空席は技術部長だけ）。2行目で CEO の席・3行目で CEO から全部へ
    "c207": dict(
        t="会社の顔ぶれ", s="事故のときの会社",          # ⚠️ 門番 dup：「2023年の上級の職」は図の札の写し
        fig=("m22", dict(view="org", steps=[dict(state=dict(seats="on")), dict(state=dict(ceo="on"), tag=dict(t="操縦も自分で", at="ra")),
                                            dict(state=dict(all="on"), tag=dict(t="すべてに関わる", at="rb"))],
                         note="席の並びは模式（職と空席はカナダの報告書の表4）", src=ss.src(["TSB §1.23", "TSB §1.9.1", "TSB §1.23.1"]))),
    ),
    # c208（3行）＝同じ席＋社員の印15（数は黄）・「実験的」・前例が無い
    "c208": dict(
        t="小さな会社", s="2023年の季節の初め",
        fig=("m22", dict(view="org", start=dict(seats="on", ceo="on", all="on"),
                         steps=[dict(state=dict(staff="on")), dict(tag=dict(t="実験的", at="ra")), dict(tag=dict(t="それまで例が無い", at="rb"))],
                         note="席の並びは模式（社員の印は1つ＝1人）", src=ss.src(["TSB §1.23", "TSB §1.23.1"]))),
    ),
    # c209（3行）＝同意書の要点（米沿岸警備隊の報告書の箇条＝英字のまま）・「death」の数え 9
    "c209": dict(
        t="同意書", s="参加の前の署名",
        fig=("m22", dict(view="paper", start=dict(doc="waiver"),
                         steps=[dict(), dict(state=dict(hl1="on", hl2="on")), dict(state=dict(n9="on"))],
                         note="句は米沿岸警備隊の報告書の要点（英字のまま・模式）", src=ss.src(["USCG p71"]))),
    ),
    # c210（3行）＝参加費の棒（2021年 105,129ドル → 2022年・2023年 25万ドル）。円は左下の注（1ドル140円）
    "c210": dict(
        t="参加費", s="1人あたり",
        fig=("qty", dict(view="bar", groups=[ss.QG["fee"]],
                         steps=[dict(), dict(add=[ss.qb("fee21"), ss.qb("fee22"), ss.qb("fee23")]), dict()],
                         note="円の換算は1ドル＝140円", src=ss.src(["USCG p64", "TSB §1.23"]))),   # ⚠️ 門番 echo：円の額は字幕の写し
    ),
    # c211（3行）＝計画書の一節（NTSB 脚注8 が引く英字）・呼び名・米沿岸警備隊の見立て（青）
    "c211": dict(
        t="客の呼び名", s="会社の計画書",
        fig=("m22", dict(view="paper", start=dict(doc="plan"),
                         steps=[dict(), dict(state=dict(hl1="on", name="on")), dict(state=dict(uscg="on"))],
                         note="一節は米運輸安全委員会の報告書の脚注8 の引用（英字のまま・模式）",
                         src=ss.src(["NTSB p1015", "USCG p300", "USCG p317"]))),
    ),
    # c212（2行）＝付録B の表（27行・英字のまま）。2行目で年のまとまりと「27回」
    "c212": dict(
        t="潜航の記録", s="人が乗った潜航",
        fig=("m22", dict(view="table", steps=[dict(), dict(state=dict(yr="on"), tag=dict(t="27回", at="n27"))],
                         rel=[dict(t="27回", src="TSB §付録B")],
                         note="表はカナダの報告書の付録B（英字は原文のまま）", src=ss.src(["TSB §付録B"]))),
    ),
    # c213（2行）＝🔧 点の並び（1回＝1点）。届いた13回を潜水艇の白
    "c213": dict(
        t="届いた回数", s="27回のうち",
        fig=("m22", dict(view="dives", steps=[dict(state=dict(reach="on"), tag=dict(t="13回", at="t")), dict()],
                         rel=[dict(t="13回", src="NTSB p1014")],
                         note="点の並びは模式（届いた＝付録Bの深さ3,840メートルの行）", src=ss.src(["TSB §付録B", "NTSB p1014"]))),
    ),
    # c214（3行）＝🔧 同じ点＋1つ目の赤の輪（回収のときに前のドームが外れた）→ ボルトを18本に
    "c214": dict(
        t="備考の欄", s="不具合の記録",
        fig=("m22", dict(view="dives", start=dict(reach="on"),
                         steps=[dict(), dict(state=dict(dome="on"), tag=dict(t="前のドームが落ちた（回収のとき）", at="low")),
                                dict(tag=dict(t="ボルトを18本に", at="low2"))],
                         rel=[dict(t="18本", src="TSB §脚注39")],
                         note="点の並びは模式（赤の輪＝付録Bの備考）", src=ss.src(["TSB §付録B", "TSB §脚注39"]))),
    ),
    # c215（2行）＝🔧 同じ点＋電池が切れた回（2022-06-20・27時間）
    "c215": dict(
        t="海の上で一晩", s="潜航が長引いた回",
        fig=("m22", dict(view="dives", start=dict(reach="on", dome="on"),
                         steps=[dict(state=dict(batt="on"), tag=dict(t="電池が切れた", at="low")), dict(tag=dict(t="27時間", at="low2"))],
                         rel=[dict(t="27時間", src="TSB §付録B")],
                         note="点の並びは模式（赤の輪＝付録Bの備考）", src=ss.src(["TSB §付録B", "NTSB p1036"]))),
    ),
    # c216（3行）＝🔧 同じ点＋推進器・重り・通信の赤の輪 → カナダの報告書の言葉（紫）
    "c216": dict(
        t="不具合の数々", s="潜航ごとの不具合",
        fig=("m22", dict(view="dives", start=dict(reach="on", dome="on", batt="on"),
                         steps=[dict(state=dict(thr="on", wt="on", com="on")), dict(),
                                dict(tag=dict(t="やってみて直すやり方", d="カナダの報告書の見方", at="low", col=J.INST))],
                         note="点の並びは模式（赤の輪＝付録Bの備考）", src=ss.src(["TSB §付録B", "TSB §1.23.1"]))),
    ),
})
