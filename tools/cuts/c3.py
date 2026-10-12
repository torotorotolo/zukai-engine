# -*- coding: utf-8 -*-
"""第2章　乗っ取りの「常識」 c301–c320（20カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c3.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep21/make_plan21.py` で
  映像方針の一覧 `ref/ep21/eizou_build/list21.tsv`（了承②ずみ・E 0）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット（台本の画は元の予定）。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c301': dict(kind='写真',
               plan='F15A｜副題：ニューヨーク上空を警戒するオーティス基地のF-15（2001年11月）｜動き：右へ流す｜権利：A（米空軍の職務）｜出典の行：米空軍｜台本の画：実写 F-15 オーティス基地（102戦闘航空団 101戦闘飛行隊・尾翼「MA」・A・VIRIN で 2001-11-06・全画面・右へ流す＝副題「オーティス基地のF-15（2001年11月）」）',
               src='—'),
    'c302': dict(kind='図解',
               plan='台本の画：図 模式 乗員の手引きの年表（1960年代から2001年まで）',
               src='委員会報告 p85（`The FAA-approved "Common Strategy" had been elaborated over decades of experience with scores of hijackings, beginning in the 1960s`）'),
    'c303': dict(kind='図解',
               plan='台本の画：図 模式 昔ながらの乗っ取り（要求・着陸・あとは警察と軍の3つの箱）',
               src='委員会報告 p85（`accommodate their demands, get the plane to land safely, and then let law enforcement or the military handle the situation`・`the longer a hijacking persisted, the more likely it was to end peacefully`）'),
    'c304': dict(kind='図解',
               plan='台本の画：図 模式 同じ箱（「要求」に亡命・仲間の釈放の札）',
               src="委員会報告 p85（`hijackers issue negotiable demands (most often for asylum or the release of prisoners)`・`suicide wasn't in the game plan`）"),
    'c305': dict(kind='図解',
               plan='台本の画：図 模式 同じ箱（「暴力が起きたら」の箱だけ空白）',
               src='委員会報告 p85（`FAA training material provided no guidance for flight crews should violence occur`）'),
    'c306': dict(kind='図解',
               plan='台本の画：図 模式 操縦室の扉（金庫の扉の絵記号）',
               src='委員会報告 p85（`proposals were made in early 2001 to install reinforced cockpit doors`）'),
    'c307': dict(kind='図解',
               plan='台本の画：図 模式 同じ扉（鍵が外れる）',
               src="委員会報告 p85（`Even if you make a vault out of the door, if they have a noose around my flight attendant's neck, I'm going to open the door`）"),
    'c308': dict(kind='図解',
               plan='台本の画：図 模式 同じ扉と箱（「要求に従う」の矢印）',
               src='委員会報告 p85（`even a hardened cockpit door would have made little difference in a hijacking`）'),
    'c309': dict(kind='図解',
               plan='台本の画：図 模式 年表（1986年の印から2001年まで）',
               src='委員会報告 p85（`no terrorist had hijacked a U.S. commercial aircraft anywhere in the world since 1986`）'),
    'c310': dict(kind='図解',
               plan='台本の画：図 模式 機内の座席（保安官の席に印が無い）',
               src='委員会報告 p85（`only 33 armed and trained federal air marshals as of 9/11`・`They were not deployed on U.S. domestic flights`）'),
    'c311': dict(kind='図解',
               plan='台本の画：図 模式 手順の段（管制官→上司→FAA 本部→国防総省の指揮所→国防長官の許し→NORAD→戦闘機）',
               src='委員会報告 p17（`Controllers would notify their supervisors, who in turn would inform management all the way up to FAA headquarters in Washington`）'),
    'c312': dict(kind='図解',
               plan='台本の画：図 模式 同じ段（下の段へ光が進む）',
               src="委員会報告 p18（`to contact the Pentagon's National Military Command Center`・`seek approval from the Office of the Secretary of Defense`・`transmitted down NORAD's chain of command`）"),
    'c313': dict(kind='図解',
               plan='台本の画：図 模式 乗っ取られた機と後ろの戦闘機（約8キロの間隔）',
               src='委員会報告 p18（`five miles directly behind the hijacked aircraft`・`The protocols did not contemplate an intercept`）'),
    'c314': dict(kind='図解',
               plan='台本の画：図 模式 同じ（段と後ろの戦闘機を1枚に）',
               src='—'),
    'c315': dict(kind='図解',
               plan='台本の画：図 模式 3つの前提の箱（1つ目に印＝すぐに見分けがつき、姿を消そうとはしない）',
               src='委員会報告 p18（`the hijacked aircraft would be readily identifiable and would not attempt to disappear`）'),
    'c316': dict(kind='図解',
               plan='台本の画：図 模式 3つの前提の箱（2つ目と3つ目に印）',
               src='委員会報告 p18（`there would be time to address the problem through the appropriate FAA and NORAD chains of command`・`the hijacking would take the traditional form`）'),
    'c317': dict(kind='図解',
               plan='台本の画：図 模式 待機の基地の数（冷戦の最大26か所から7か所への棒）',
               src='委員会報告 p16（`reduced from its Cold War high of 26`）・p17（`only seven alert sites left in the United States, each with two fighter aircraft on alert`）'),
    'c318': dict(kind='図解',
               plan='台本の画：図 模式 北東部の地図（NEADS のあるローム・オーティス・ラングレー・ニューヨーク・ワシントン）',
               src='委員会報告 p17（`Northeast Air Defense Sector (also known as NEADS), which is based in Rome, New York`・`NEADS could call on two alert sites, each with one pair of ready fighters`）'),
    'c319': dict(kind='図解',
               plan='台本の画：図 模式 同じ地図（海の外から来る矢印だけ）',
               src='委員会報告 p352（`only aircraft that were coming from overseas`）・p17（`was not recognized by NORAD before 9/11`）'),
    'c320': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（7:59 から先が空白のまま伸びる）',
               src='委員会報告 p18（`unsuited in every respect`）'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-12）：図解 第2章（19カット）＝模式図 `tools/mech21.py`・年表と時間の帯（axis）・棒（qty）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「乗っ取りの「常識」」と4字以上同じ並び（「乗っ取り」）を見出し・副題に入れない（門番 dup）。人は描かない・言葉の引用は語りと字幕だけ
N_OLD = "箱の並びは模式（言葉は委員会報告から）"
SPEC.update({
    # c302（2行）＝年表（1958〜2006）。2行目で 1960年代の帯と、9.11 までの括弧（数十年の経験＝p85）
    "c302": dict(
        t="乗員の手引き", s="FAA が認めたやり方",
        fig=("axis", dict(ss.AX_HIST, steps=[dict(), dict(add=[ss.ax("cs60"), ss.ax("cs_all")])],
                          note="年は委員会報告の記録（1960年代＝年代の帯）", src=ss.src(["委員会報告 p85", "委員会報告 p1"]))),
    ),
    # c303（2行）＝昔ながらのやり方の3つの箱（要求をのむ→無事に着陸→警察や軍）。2行目で3つ目と「長引くほど」
    "c303": dict(
        t="昔のやり方", s="乗員が教わっていた動き",
        fig=("m21", dict(view="old", steps=[dict(state=dict(b1="on", b2="on")), dict(state=dict(b3="on", long="on"))],
                         note=N_OLD, src=ss.src(["委員会報告 p85"]))),
    ),
    # c304（2行）＝要求の中身（亡命・仲間の釈放）→ FAA の職員の言葉（引用は語りと字幕＝札は短く）
    "c304": dict(
        t="要求の中身", s="手引きが想定した犯人",
        fig=("m21", dict(view="old", start=dict(b1="on", b2="on", b3="on", long="on"),
                         steps=[dict(state=dict(chips="on")), dict(tag=dict(t="自殺は筋書きに無い", d="FAA の職員の言葉", at="why"))],
                         note=N_OLD, src=ss.src(["委員会報告 p85"]))),
    ),
    # c305（2行）＝「暴力が起きたら」の箱だけ空白（教材に手引きが無い）
    "c305": dict(
        t="空白の箱", s="FAA の教材",
        fig=("m21", dict(view="old", start=dict(b1="on", b2="on", b3="on", chips="on", long="on"),
                         steps=[dict(), dict(state=dict(b4="on"), tag=dict(t="手引きなし", at="none"))],
                         note=N_OLD, src=ss.src(["委員会報告 p85"]))),
    ),
    # c306（2行）＝扉を頑丈にする案（金庫の扉の絵記号）→ 操縦士の組合の保安委員長（役職だけ）
    "c306": dict(
        t="頑丈な扉の案", s="2001年の初めの提案",
        fig=("m21", dict(view="door", start=dict(lock="on"),
                         steps=[dict(state=dict(vault="on"), tag=dict(t="金庫のような扉", at="vault")),
                                dict(tag=dict(t="組合の保安委員長", at="who"))],
                         note="扉の形は模式", src=ss.src(["委員会報告 p85"]))),
    ),
    # c307（2行）＝委員長の言葉（語りと字幕だけ）。2行目で鍵が外れて扉が開く
    "c307": dict(
        t="委員長の言葉", s="操縦士の組合の保安委員長",
        fig=("m21", dict(view="door", start=dict(lock="on", vault="on"),
                         steps=[dict(), dict(state=dict(lock="open", door="open"))],
                         note="扉の形は模式（言葉の引用は画面に出さない）", src=ss.src(["委員会報告 p85"]))),
    ),
    # c308（2行）＝要求に従う決まりなら、扉が丈夫でも違いはほとんど無い（委員会＝p85）
    "c308": dict(
        t="丈夫な扉でも", s="手引きどおりなら扉は開く",
        fig=("m21", dict(view="door", start=dict(lock="open", vault="on", door="open"),
                         steps=[dict(), dict(state=dict(comply="on"), tag=dict(t="違いはほとんど無い", d="委員会の見立て", at="comply"))],
                         note="扉の形は模式", src=ss.src(["委員会報告 p85"]))),
    ),
    # c309（2行）＝同じ年表に 1986年（最後のテロによる旅客機の事件）と 9.11 までの空白（p85）
    "c309": dict(
        t="テロの空白", s="アメリカの旅客機の事件",
        fig=("axis", dict(ss.AX_HIST, past=[ss.ax("cs60"), ss.ax("cs_all", t="")],      # ⚠️ geom_gap：括弧の札が1986年の札に触れた＝沈めた括弧は札なし
                          steps=[dict(add=ss.ax("day911")), dict(add=[ss.ax("last86"), ss.ax("quiet86")])],
                          note="年は委員会報告の記録", src=ss.src(["委員会報告 p85", "委員会報告 p1"]))),
    ),
    # c310（3行）＝上から見た客室（座席の並びは模式）。2行目で全米で33人・3行目で保安官の席の印が無い（国内線に配置なし）
    "c310": dict(
        t="機内の警備", s="ボーイング767 の客室",
        fig=("m21", dict(view="cabin", steps=[dict(), dict(tag=dict(t="全米で33人", d="連邦航空保安官", at="n33")),
                                              dict(state=dict(legend="on"), tag=dict(t="国内線に配置なし", at="none"))],
                         rel=[dict(t="33人", src="委員会報告 p85")], note="座席の並びは模式", src=ss.src(["委員会報告 p85"]))),
    ),
    # c311（2行）＝手順の段（管制官→…→戦闘機）。1行目で NORAD の箱・2行目で管制官から FAA の本部まで灯す
    "c311": dict(
        t="伝わる順", s="管制から軍へ知らせが伝わる決まり",
        fig=("m21", dict(view="chain", steps=[dict(state=dict(norad="on")), dict(state=dict(lit="3"))],
                         note="段の形は模式（順は委員会報告）", src=ss.src(["委員会報告 p17", "委員会報告 p18"]))),
    ),
    # c312（3行）＝本部→国防総省の指揮所→国防長官の許し（1行目）→ NORAD→戦闘機（2行目）
    "c312": dict(
        t="命令の段", s="国防総省から NORAD へ",
        fig=("m21", dict(view="chain", start=dict(lit="3"), steps=[dict(state=dict(lit="5")), dict(state=dict(lit="7")), dict()],
                         note="段の形は模式（順は委員会報告）", src=ss.src(["委員会報告 p18"]))),
    ),
    # c313（2行）＝上から見た2機。約8キロ（5マイル）後ろの戦闘機 → そばに寄せない（手順に無い）
    "c313": dict(
        t="後ろから見守る", s="手順が決めていた戦闘機の付き方",
        fig=("m21", dict(view="escort", steps=[dict(state=dict(fighter="on", dim="on"), tag=dict(t="約8キロ（5マイル）", at="dim")),
                                               dict(state=dict(near="on"), tag=dict(t="そばに寄せない", d="手順に無い", at="near"))],
                         rel=[dict(t="約8キロ（5マイル）", src="委員会報告 p18")], note="間隔と機の大きさは模式（8キロは縮めて描いた）",
                         src=ss.src(["委員会報告 p18"]))),
    ),
    # c314（2行）＝段と後ろの戦闘機を1枚に（全部灯した段の右下に小窓）
    "c314": dict(
        t="2つの決まり", s="段を上がる知らせと、後ろの戦闘機",
        fig=("m21", dict(view="chain", start=dict(lit="7"), steps=[dict(state=dict(esc="on")), dict()],
                         note="段と機の形は模式", src=ss.src(["委員会報告 p17", "委員会報告 p18"]))),
    ),
    # c315（1行）＝3つの前提の箱（1つ目を灯す）
    "c315": dict(
        t="1つ目の前提", s="委員会が挙げた手順の前提",
        fig=("m21", dict(view="premise", steps=[dict(state=dict(p1="on"))], note="箱の並びは模式（言葉は委員会報告から）",
                         src=ss.src(["委員会報告 p18"]))),
    ),
    # c316（2行）＝2つ目・3つ目を灯す
    "c316": dict(
        t="残る2つ", s="時間と、昔ながらの形",
        fig=("m21", dict(view="premise", start=dict(p1="on"), steps=[dict(state=dict(p2="on")), dict(state=dict(p3="on"))],
                         note="箱の並びは模式（言葉は委員会報告から）", src=ss.src(["委員会報告 p18"]))),
    ),
    # c317（3行）＝待機の基地の数（冷戦のころの最大 → 事件の朝）。🔴 数字は画面に書かない（目盛りだけ）
    "c317": dict(
        t="減った基地", s="全米の防空の備え",
        fig=("qty", dict(view="bar", groups=[ss.QG["alert"]], steps=[dict(), dict(add=ss.qb("alert_cw")), dict(add=ss.qb("alert_911"))],
                         note="数は委員会報告の記録", src=ss.src(["委員会報告 p16", "委員会報告 p17"]))),
    ),
    # c318（3行）＝北東部の地図。1行目でローム（NEADS）・3行目でオーティスとラングレー
    "c318": dict(
        t="防空の受け持ち", s="NEADS と、すぐ呼べた2か所",
        fig=("m21", dict(view="ne", steps=[dict(state=dict(neads="on")), dict(), dict(state=dict(bases="on"), tag=dict(t="2か所に2機ずつ", at="bases"))],
                         rel=[dict(t="2か所に2機ずつ", src="委員会報告 p17")], note="陸の形は Natural Earth・地点は緯度経度から＝模式",
                         src=ss.src(["委員会報告 p17"]))),
    ),
    # c319（2行）＝同じ地図に、海の外から来る矢印（想定）と、国内の便（想定の外）
    "c319": dict(
        t="想定の向き", s="NORAD が考えていた脅威",
        fig=("m21", dict(view="ne", start=dict(neads="on", bases="on"),
                         steps=[dict(state=dict(sea="on"), tag=dict(t="海の外から来る機", at="sea")),
                                dict(state=dict(dom="on"), tag=dict(t="国内の旅客機は想定の外", at="dom"))],
                         note="陸の形は Natural Earth・矢印は向きだけ＝模式", src=ss.src(["委員会報告 p17", "委員会報告 p352"]))),
    ),
    # c320（2行）＝芯の帯（7:59 の11便だけ・その先は空白のまま＝台本の画の欄）。⚠️ カーソルは記録の点の上だけ（門番 axis）＝7:59 のまま
    "c320": dict(
        t="合わない手順", s="手順と、その朝の出来事",
        fig=("axis", dict(ss.AX_MORN, past=[ss.ax("dep11")], start=dict(cur="7:59"), steps=[dict(), dict()],
                          note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p4", "委員会報告 p18"]))),
    ),
})
