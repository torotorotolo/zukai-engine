# -*- coding: utf-8 -*-
"""第1章　その朝、4つの便 c201–c217（17カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/c2.py`）。
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
    'c201': dict(kind='写真',
               plan='MAN01｜副題：事件の前のマンハッタン（2001年7月）｜動き：右へ流す｜権利：C＋D（Highsmith の献呈・米議会図書館蔵／知られた制限なし）｜出典の行：Carol M. Highsmith（米議会図書館蔵）｜台本の画：実写 manhattan_pre（事件の2か月前のマンハッタン・2001年7月・C＋D＝米議会図書館蔵／知られた制限なし・全画面・右へ流す＝副題「事件の前のマンハッタン（2001年7月）」）',
               src='委員会報告 p1（`nearly cloudless`）'),
    'c202': dict(kind='図解',
               plan='台本の画：図 模式 4便の経路の地図（出発の3つの空港と行き先の2つの街＝NTSB の4本の経路の図をなぞる・東から西へ線が伸びる）',
               src='委員会報告 p4（`four transcontinental flights`）'),
    'c203': dict(kind='写真',
               plan='LOGAN｜副題：ボストンのローガン空港（1973年）｜動き：ゆっくり寄る｜権利：A（EPA DOCUMERICA・NARA 548428）｜出典の行：米環境保護庁 DOCUMERICA（NARA 548428）｜台本の画：実写 logan（ボストンのローガン空港・1973年・EPA DOCUMERICA・A・全画面・ゆっくり寄る＝副題「ボストンのローガン空港（1973年）」）',
               src='委員会報告 p4（`turn them into large guided missiles, loaded with up to 11,400 gallons of jet fuel`）・第1章 注1 p451（`they simply booked heavily fueled east-to-west transcontinental flights`）・p245（`select planes departing on long flights because they would be full of fuel`）'),
    'c204': dict(kind='写真',
               plan='AA11｜副題：11便の機体（2001年4月）｜動き：額装・止め（寄り0）｜権利：F（CC BY-SA 3.0＝額装・無加工・寄り0）｜出典の行：（作者と許諾の表示は頁の通りに＝fetch21_meta.tsv）｜注：BY-SA 3.0＝額装・無加工（「写真は画面いっぱい」の例外）。登録記号 N334AA が写る｜台本の画：実写 AA11 N334AA（11便の機体の事件の前の写真・CC BY-SA 3.0・額装・無加工＝副題「11便の機体（事件の前）」）',
               src='委員会報告 p4（`Eighty-one passengers boarded the flight with them (including the five terrorists)`・`The plane took off at 7:59`・`It carried its full capacity of nine flight attendants`）'),
    'c205': dict(kind='写真',
               plan='TG99｜区間 214.0〜224.8秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：世界貿易センターの屋上から見た港（1999年）｜動き：額装・等速｜権利：F（CC BY-SA 3.0＋GFDL＝額装・無加工・速さも変えない）｜出典の行：（作者と許諾の表示は頁の通りに＝fetch21_meta.tsv）｜注：BY-SA 3.0＝額装・無加工・速さを変えない。もう一方の塔の屋上→港（自由の女神）。人は写らない（1秒1コマ）。⑤b-1：等速の約束＝区間をカットの実測の秒（10.751秒＝声＋前後の間）に合わせて 223.5→224.75 へ（ショット6＝173.4〜253.5 の中・伸ばした分は 224.0・224.7秒を原寸で見た＝港の遠景だけ）。台本の「720×576・額装・無加工」のまま。⑤b-7：試し焼き 38321787179 で副題「事件の前の世界貿易センター（1999年・屋上の展望台から）」と写っているもの（展望台から見た港）が合わない＝写っているものに｜台本の画：実写 Torri Gemelle（事件の前の世界貿易センター・1999年・CC BY-SA・720×576・額装・無加工＝副題「事件の前の世界貿易センター（1999年）」）',
               src='委員会報告 p7（`Fifty-six passengers boarded the flight`・`departed Logan Airport at 8:14`）'),
    'c206': dict(kind='写真',
               plan='DULLES｜副題：ワシントン・ダレス空港（1985年）｜動き：左へ流す｜権利：A（米海軍の職務）｜出典の行：米海軍（PH1 David C. Maclean）｜台本の画：実写 dulles（ワシントン・ダレス空港・1985年・A・全画面・左へ流す＝副題「ワシントン・ダレス空港（1985年）」）',
               src='委員会報告 p8（`the flight carried 58 passengers`・`took off at 8:20`・`There were four flight attendants`）'),
    'c207': dict(kind='写真',
               plan='UA93｜副題：93便の機体（1999年）｜動き：ゆっくり引く｜権利：F（CC BY 2.0）｜出典の行：（作者と許諾の表示は頁の通りに＝fetch21_meta.tsv）｜注：CC BY 2.0・幅1690｜台本の画：実写 UA93 N591UA（93便の機体の事件の前の写真・CC BY 2.0・全画面・ゆっくり寄る＝副題「93便の機体（事件の前）」）',
               src='委員会報告 p10（`At 8:42, United Airlines Flight 93 took off from Newark`・`Thirty-seven passengers, including the hijackers, boarded the plane`・`there were five flight attendants`）'),
    'c208': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（4機の離陸＝7:59・8:14・8:20・8:42＝この回の芯の帯の始まり）',
               src='委員会報告 p10（`Three of the flights had actually taken off within 10 to 15 minutes of their planned departure times`・`the flight was running more than 25 minutes late`）'),
    'c209': dict(kind='フリー素材',
               plan='B767｜副題：イメージ（2012年のアメリカン航空の767）｜動き：右へ流す｜権利：F（CC BY 2.0）｜出典の行：Valentin Hintikka（CC BY 2.0）｜注：20%に数えない｜台本の画：イメージ b767_takeoff（2012年のアメリカン航空の767・フリー素材＝副題「イメージ」）',
               src='委員会報告 p4（`The 19 men were aboard four transcontinental flights`）'),
    'c210': dict(kind='フリー素材',
               plan='SEC70｜副題：イメージ（1970年の空港）｜動き：上へ流す｜権利：F（CC BY）｜出典の行：Orange County Archives（CC BY）｜注：縦長・20%に数えない。⑤b-7：2倍で測った＝写っているのは制服の郡の保安係1人だけ（公務）＝モザイク不要｜台本の画：イメージ security_pre（1970年の空港の保安検査・CC BY・私人の顔だけモザイク＝副題「イメージ（1970年の空港）」）',
               src='委員会報告 p2（`operated by Globe Security under a contract with American Airlines`・`contracted with Huntleigh USA to perform the screening`）・p3（`had contracted out the work to Argenbright Security`）・p4（`operated under contract by Argenbright Security`）・p2（`calibrated to detect items with at least the metal content of a .22-caliber handgun`）'),
    'c211': dict(kind='図解',
               plan='台本の画：図 模式 保安検査の流れ（探知機の門・手持ちの探知機・通過＝人は影だけ）',
               src='委員会報告 p3（`set it off, a screener wanded him. He passed this inspection`・`set off the alarms for both the first and second metal detectors and was then hand-wanded before being passed`・`it was clear that he did not`）'),
    'c212': dict(kind='図解',
               plan='台本の画：図 模式 刃渡りの物差し（10センチの線と刃物の影・人は描かない）',
               src='委員会報告 p84（`knives with blades under 4 inches long`・`explicitly permitted them`）'),
    'c213': dict(kind='図解',
               plan='台本の画：図 模式 同じ物差し（3つの理由の札）',
               src='委員会報告 p84（`the agency did not consider such items to be menacing`・`most local laws did not prohibit individuals from carrying such knives`・`such knives would have been difficult to detect unless the sensitivity of metal detectors had been greatly increased`）'),
    'c214': dict(kind='図解',
               plan='台本の画：図 模式 機内からの電話が伝えた道具（刃物・スプレー・「爆弾」の札に「おそらく偽物」）',
               src="委員会報告 p7（`They used knives`）・p5（`I think there's Mace`）・p13（`we believe the bombs were probably fake`）"),
    'c215': dict(kind='図解',
               plan='台本の画：図 模式 操縦室の扉（閉めて鍵＝当時の決まり）',
               src='委員会報告 p85（`required air crews to keep the cockpit door closed and locked in flight`・`This requirement was not always observed or vigorously enforced`）'),
    'c216': dict(kind='写真',
               plan='APRON｜副題：ローガン空港のターミナル（1969年）｜動き：左へ流す｜権利：D（米議会図書館蔵／知られた制限なし）｜出典の行：Balthazar Korab（米議会図書館蔵）｜注：⑤b-7：試し焼き 38321787179 で写っているのはターミナルの建物（EASTERN の字）＝副題を写っているものに（元は「駐機場」）｜台本の画：実写 logan_apron（ローガン空港の駐機場・1969年・D＝米議会図書館蔵／知られた制限なし・全画面・ゆっくり引く＝副題「ローガン空港（1969年）」）',
               src='委員会報告 p4（`By 8:00 A.M. on the morning of Tuesday, September 11, 2001, they had defeated all the security layers`）'),
    'c217': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（8:00 の線）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-3（2026-10-12）：図解 第1章（8カット）＝模式図 `tools/mech21.py`（門番 check_mech の judge_m21）・時間の帯（axis・門番 check_axis）
# ══════════════════════════════════════════════════════════
#   🔴 人は描かない・記録の言葉（電話の逐語）は画面に出さない（語りと字幕だけ）。見出しは7字以内の名札・副題は図の中身（章の札
#      「その朝、4つの便」と4字以上同じ並びを入れない＝門番 dup）。時刻はアメリカ東部の夏の時間・画面は「8:46」の形
SPEC.update({
    # c202（3行）＝北アメリカの陸（Natural Earth）と出発の3つの空港 → 2行目で行き先の2つの街と線。線は出発と行き先を結んだだけ（実際の経路ではない）
    "c202": dict(
        t="大陸の横断", s="出発の3つの空港と、行き先の2つの街",
        fig=("m21", dict(view="us", steps=[dict(state=dict(east="on")), dict(state=dict(west="on", routes="on")), dict()],
                         note="陸の形は Natural Earth（国境なし）・線は出発と行き先を結んだだけ（実際の経路ではない）・地点は緯度経度から＝模式",
                         src=ss.src(["委員会報告 p4", "委員会報告 p7", "委員会報告 p8", "委員会報告 p10"]))),
    ),
    # c208（3行）＝この回の芯の帯（AX_MORN 7:50〜10:10）の始まり。1行目で3機（7:59・8:14・8:20）・2行目で93便（8:42）
    "c208": dict(
        t="離陸の時刻", s="4機が飛び立った順（アメリカ東部の夏の時間）",
        fig=("axis", dict(ss.AX_MORN, steps=[
            dict(add=[ss.ax("dep11"), ss.ax("dep175"), ss.ax("dep77")], cur="8:20"),
            dict(add=ss.ax("dep93"), cur="8:42"), dict()],
            note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p4", "委員会報告 p7", "委員会報告 p8", "委員会報告 p10"]))),
    ),
    # c211（2行）＝ダレス空港の保安検査（77便の2人）。1行目で探知機の門が2台とも鳴る・2行目で手持ちの探知機と通過（人は描かない）
    "c211": dict(
        t="鳴った探知機", s="ワシントン・ダレス空港の保安検査（77便）",
        fig=("m21", dict(view="gate", steps=[dict(state=dict(ring="on"), tag=dict(t="2台とも鳴る", at="ring")),
                                             dict(state=dict(wand="on", pass_="on"), tag=dict(t="鳴った物は確かめず", at="pass_"))],
                         rel=[dict(t="2台", src="委員会報告 p3")], note="人は描かない・門と探知機の形は模式",
                         src=ss.src(["委員会報告 p3"]))),
    ),
    # c212（3行）＝刃渡りの物差し（目盛りはセンチ・4インチ＝10.16センチの線）。2行目で線・3行目で「持ち込めた」
    "c212": dict(
        t="刃物の決まり", s="当時の保安検査（2001年9月まで）",
        fig=("m21", dict(view="blade", steps=[dict(), dict(state=dict(limit="on")),
                                              dict(state=dict(ok="on"), tag=dict(t="持ち込めた", d="航空会社の検査の手引き", at="ok"))],
                         rel=[dict(t="4インチ（10.16センチ）", src="委員会報告 p84")], note="刃物の形は模式（長さは物差しの目盛りどおり）",
                         src=ss.src(["委員会報告 p84"]))),
    ),
    # c213（3行）＝同じ物差しに FAA の3つの理由（p84）。⚠️ 3つ目は語りの写しにしない（門番 echo）＝「感度を大きく上げる必要」
    "c213": dict(
        t="3つの理由", s="FAA が挙げた理由",
        fig=("m21", dict(view="blade", start=dict(limit="on", ok="on"),
                         steps=[dict(state=dict(r1="on"), tag=dict(t="危ない物と見なさない", at="r1")),
                                dict(state=dict(r2="on"), tag=dict(t="多くの地域で持ち歩ける", at="r2")),
                                dict(state=dict(r3="on"), tag=dict(t="探知機の感度を大きく上げる必要", at="r3"))],
                         note="刃物の形は模式", src=ss.src(["委員会報告 p84"]))),
    ),
    # c214（3行）＝機内からの電話が伝えた道具（刃物・スプレー・「爆弾がある」）→ 3行目で「おそらく偽物」（委員会の見立て）
    "c214": dict(
        t="伝えられた道具", s="客室乗務員と乗客の通報",
        fig=("m21", dict(view="tools", steps=[dict(state=dict(knife="on")), dict(state=dict(spray="on", bomb="on")),
                                              dict(state=dict(fake="on"), tag=dict(t="委員会の見立て", at="fake"))],
                         note="形は模式（爆弾は犯人が「ある」と言っただけ）", src=ss.src(["委員会報告 p5", "委員会報告 p7", "委員会報告 p13"]))),
    ),
    # c215（2行）＝操縦室の扉（客室の側から）。1行目で鍵・2行目で「守られていないことも」
    "c215": dict(
        t="扉の決まり", s="2001年9月11日より前の決まり",
        fig=("m21", dict(view="door", steps=[dict(state=dict(lock="on"), tag=dict(t="飛行中は閉めて鍵", at="rule", to="lock")),
                                             dict(state=dict(loose="on"), tag=dict(t="いつも守られてはいない", at="loose"))],
                         note="扉の形は模式", src=ss.src(["委員会報告 p85"]))),
    ),
    # c217（3行）＝芯の帯に 8:00（19人が保安の関門を通り抜けていた＝p4）。4機の離陸は沈めて続ける（11便のほかは点だけ＝札が重なる）
    "c217": dict(
        t="朝8時の時点", s="保安の関門と4機の離陸",
        fig=("axis", dict(ss.AX_MORN, past=[ss.ax("dep11", off=3)] + [ss.ax(k, t="", lab=False) for k in ("dep175", "dep77", "dep93")],   # ⑤c'：geom_gap＝札の右端と 8:00 の縦の線が 3px＝off=3（18本目 c312 の型）
                          start=dict(cur="7:59"),
                          steps=[dict(add=ss.ax("gate8"), cur="8:00"), dict(), dict()],
                          note="時刻は委員会報告の記録", src=ss.src(["委員会報告 p4", "委員会報告 p7", "委員会報告 p8", "委員会報告 p10"]))),
    ),
})

# ── 🆕 ⑤b-7（2026-10-13）：写真・イメージ・映像（素材・副題・動き＝PLAN＝映像方針の一覧・了承②）──
#   全画面の写真は side="none"（注記なし＝右の暗幕を敷かない・⑤b-2 の型）。動きは `ss.mv`（PLAN の「動き」の語）・寄せの点は構図の下見
#   （⑤b-7 の scratchpad `plan_*.jpg`＝10% の目盛り）。台紙の縁のある写真（ss.SLIDE_MOUNT）は lo＝いちばん引いた側の寄りで縁を外す（門番 photo_edge）
_MAN = P("manhattan_2001_07")
_LOG = P("logan_1973")
_DUL = P("dulles_1985")
_UA93 = P("n591ua_1999")
_B767 = P("stock/n352aa_2012")
_SEC = P("stock/security_1970")
_APR = P("logan_apron_1969")
SPEC.update({
    # c201（9.5秒）＝事件の2か月前のマンハッタン（Highsmith・2001年7月）・右へ流す
    "c201": dict(photo=_MAN, **ss.mv(_MAN, "r"), side="none", t="4つの便と資料", s="事件の前のマンハッタン（2001年7月）"),
    # c203（11.3秒）＝ローガン空港（DOCUMERICA のスライド＝台紙の縁）・管制塔と並ぶ機へゆっくり寄る（下の縁 1.2%＝真ん中より少し下まで）
    "c203": dict(photo=_LOG, **ss.mv(_LOG, "in", 0.5, 0.55, lo=1.06), side="none", t="長い便を選ぶ", s="ボストンのローガン空港（1973年）"),
    # c204（13.3秒）＝11便の機体 N334AA（CC BY-SA 3.0＝額装・無加工・色そのまま・寄り0・止め＝ss.check_frame_only）
    "c204": dict(photo=P("n334aa_2001_04"), panel=True, color=1.0, t="1機目", s="11便の機体（2001年4月）"),
    # c205（9.9秒）＝1999年の塔の屋上の展望台から見た港（CC BY-SA 3.0 の映像 TG99＝額装・等速・地は無地＝USE の plain=True・寄り 1.0）。
    #   副題は写っているもの（試し焼き 38321787179：「事件の前の世界貿易センター」では塔が写っていると読める＝写るのは港）
    "c205": ss.vid("c205", color=1.0, t="2機目", s="世界貿易センターの屋上から見た港（1999年）"),
    # c206（10.5秒）＝ダレス空港（1985年・米海軍）・左へ流す
    "c206": dict(photo=_DUL, **ss.mv(_DUL, "l"), side="none", t="3機目", s="ワシントン・ダレス空港（1985年）"),
    # c207（9.6秒）＝93便の機体 N591UA（CC BY 2.0・幅 1690）・ゆっくり引く
    "c207": dict(photo=_UA93, **ss.mv(_UA93, "out"), side="none", t="4機目", s="93便の機体（1999年）"),
    # c209（8.7秒）＝イメージ（2012年のアメリカン航空の767・CC BY 2.0・16:9＝流す余地は寄りで作る）・右へ流す
    "c209": dict(photo=_B767, **ss.mv(_B767, "r"), side="none", t="乗っ取った側", s="イメージ（2012年のアメリカン航空の767）"),
    # c210（10.7秒）＝イメージ（1970年の空港・CC BY・縦長 1920×2802）。🔴 写っているのは制服の郡の保安係1人だけ＝公務（顔だけモザイクは
    #   不要＝⑤b-7 に2倍で測った・qa_out/ep21_assets.py の HOLD の注）。縦長は全画面で上へ流す（了承② 決め4）＝足もとから顔へ（顔が見出しの暗幕に
    #   沈まない 0.1 まで）。kind() は額装を返す（縦長）＝panel を書かない
    "c210": dict(photo=_SEC, **ss.mv(_SEC, "u", span=(0.1, 0.55)), side="none", t="保安検査", s="イメージ（1970年の空港）"),
    # c216（6.8秒）＝ローガン空港のターミナル（Korab のスライド＝四辺の縁 1.4〜2.0%・EASTERN の字の建物＝試し焼き 38321787179 で副題を
    #   「駐機場」から写っているものに）・左へ流す
    #   🔧 ⑤c'（10-13・原寸）：終わりで街灯の白い球が右上の章の札の下端に接した＝縦の寄せ 0.42（絵が約50px 下がる・縦の遊び 631px）
    "c216": dict(photo=_APR, **ss.mv(_APR, "l", fy=0.42), side="none", t="通り抜けた", s="ローガン空港のターミナル（1969年）"),
})
