# -*- coding: utf-8 -*-
"""第10章　その後の空 cb01–cb19（19カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/cb.py`）。
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
    'cb01': dict(kind='写真',
               plan='W593｜区間 26.0〜34.0秒｜倍率 1.01（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：当日の夜、ホワイトハウスでの演説｜動き：映像｜権利：A（WHCA の職務・NARA 6171390・use=Unrestricted）｜出典の行：Courtesy George W. Bush Presidential Library（NARA 6171390）｜注：大統領だけ・音は使わない｜台本の画：実写 当日の夜の演説（NARA 6171390・WHCA・A・720×486＝全画面・大統領だけ＝副題「当日の夜、ホワイトハウスでの演説」）',
               src='委員会報告 p326（`At 8:30 that evening, President Bush addressed the nation from the White House`）'),
    'cb02': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（9月13日・空港の点が戻り始める）',
               src='委員会報告 p327（`On the morning of September 13, the national airspace reopened for use by airports that met newly improvised security standards`）・p556（`effective 11:00 A.M. on September 13, 2001`）'),
    'cb03': dict(kind='写真',
               plan='🔧 DOD912｜副題：9月12日のペンタゴン（国防長官と現場を回る大統領）｜動き：左へ流す｜権利：A（国防総省の職務）｜出典の行：米国防総省｜注：🔧 WHTV 600（30分の未編集テープ）→ 国防総省の写真｜台本の画（🔧映像方針で替えた＝元の予定）：実写 WHTV 600 ペンタゴンを訪れる大統領（9月12日・WHCA・A・SD＝全画面＝副題「9月12日のペンタゴン」）',
               src='materials.md §1-2（WHTV 600＝9/12 のペンタゴン視察・未編集 30:29＝目録の説明。中身の秒は映像方針で）・委員会報告 p559 注61（`On the evening of September 12, the President was at the Pentagon`）'),
    'cb04': dict(kind='写真',
               plan='🔧 FEMA3905｜副題：9月14日の世界貿易センターの跡（救助の人たちに話す大統領）｜動き：ゆっくり寄る｜権利：A（米陸軍・FEMA の職務）｜出典の行：FEMA（SFC Thomas R. Roberts）｜注：🔧 WHTV 609 → FEMA の写真。消防士と作業員＝捜索の任務｜台本の画（🔧映像方針で替えた＝元の予定）：実写 WHTV 609 世界貿易センターの跡を訪れる大統領（9月14日・WHCA・A・消防と救助の人の顔＝職務・全画面＝副題「9月14日の世界貿易センターの跡」）',
               src='materials.md §1-2（WHTV 609・610／NARA 6171391＝9/14 の大統領と消防・警察・救助＝目録の説明。中身の秒は映像方針で）'),
    'cb05': dict(kind='図解',
               plan='台本の画：図 模式 年表（2001年11月の法律の印）',
               src='委員会報告 p391（`In November 2001, Congress passed and the President signed the Aviation and Transportation Security Act. This act created the Transportation Security Administration (TSA)`）・法律（`November 19, 2001`）'),
    'cb06': dict(kind='フリー素材',
               plan='TSA20｜副題：イメージ（2020年の空港の保安検査）｜動き：右へ流す｜権利：F（CC BY 2.0）｜出典の行：Tony Webster（CC BY 2.0）｜注：20%に数えない・顔の分かる客は顔だけモザイク｜台本の画：イメージ 現在の空港の保安検査（後年・フリー素材＝副題「イメージ（現在の空港）」）',
               src='法律（`the screening shall take place before boarding and shall be carried out by a Federal Government employee`・`except as otherwise provided in section 44919 or 44920`）・委員会報告 p2（`under a contract with American Airlines`）・p3（`had contracted out the work`）'),
    'cb07': dict(kind='図解',
               plan='台本の画：図 模式 年表（2001年11月の法律から1年の帯）',
               src='法律（`Not later than 1 year after the date of enactment of this Act, the Under Secretary of Transportation for Security shall deploy at all airports in the United States where screening is required`）'),
    'cb08': dict(kind='フリー素材',
               plan='DOOR15｜副題：イメージ（2015年の旅客機の操縦室の扉）｜動き：下へ流す｜権利：F（CC BY 2.0 de）｜出典の行：Mattes（CC BY 2.0 de）｜注：20%に数えない・縦長｜台本の画：イメージ 現在の旅客機の操縦室の扉（後年・フリー素材＝副題「イメージ」）',
               src='法律（`requiring the strengthening of the flight deck door and locks`・`to ensure that the door cannot be forced open from the passenger compartment`）'),
    'cb09': dict(kind='図解',
               plan='台本の画：図 模式 操縦室の扉（当時＝閉めて鍵の決まり・守られないこともあった→強い扉）',
               src='法律（`requiring that such flight deck doors remain locked while any such aircraft is in flight`）・委員会報告 p85（`required air crews to keep the cockpit door closed and locked in flight`・`This requirement was not always observed or vigorously enforced`）'),
    'cb10': dict(kind='図解',
               plan='台本の画：図 模式 同じ',
               src='委員会報告 p85（`even a hardened cockpit door would have made little difference in a hijacking`）'),
    'cb11': dict(kind='図解',
               plan='台本の画：図 模式 年表（2002年11月の法律・国土安全保障省の印）',
               src='委員会報告 p391（`which is now part of the Homeland Security Department`・`In November 2002, both the Homeland Security Act and the Maritime Transportation Security Act followed`）'),
    'cb12': dict(kind='図解',
               plan='台本の画：図 模式 年表（2002年11月 委員会・2004年7月 報告）',
               src='委員会報告 p.xv（`the Congress and the President created the National Commission on Terrorist Attacks Upon the United States`・`we held 19 days of hearings`）'),
    'cb13': dict(kind='図解',
               plan='台本の画：図 模式 委員会の勧告の箱（乗ってはいけない人の名簿・爆発物の検査）',
               src='委員会報告 p393（`Improved use of "no-fly" and "automatic selectee" lists should not be delayed`）'),
    'cb14': dict(kind='図解',
               plan='台本の画：図 模式 同じ箱（爆発物の検査に印）',
               src='委員会報告 p393（`The TSA and the Congress must give priority attention to improving the ability of screening checkpoints to detect explosives on passengers`）'),
    'cb15': dict(kind='写真',
               plan='🔧 FEMA3894｜副題：9月14日の世界貿易センターの跡｜動き：上へ流す｜権利：A（FEMA の職務）｜出典の行：FEMA（Andrea Booher）｜注：🔧 WHTV 610 → FEMA の写真（人は小さい）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 WHTV 610 世界貿易センターの跡（9月14日・WHCA・NARA 6171391・A・消防と救助の人の顔＝職務・全画面＝副題「9月14日の世界貿易センターの跡」）',
               src='—'),
    'cb16': dict(kind='図解',
               plan='台本の画：図 模式 2つの調べの箱（委員会＝空の側／NIST＝建物の側）',
               src='NIST（`Final Report on the Collapse of the World Trade Center Towers`）'),
    'cb17': dict(kind='写真',
               plan='🔧 PENT23｜副題：2023年のペンタゴン（空撮）｜動き：ゆっくり引く｜権利：A（国防総省の職務）｜出典の行：米国防総省｜注：🔧 ✅ 了承②（2026-10-12）＝2025年の中庭（無人機の展示が画面の大半）から替えた・語りの年も 2023年に（decide21.py R2-026 → make21.py）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 pentagon_court_pre（ペンタゴンの中庭・2025年7月・A・全画面・ゆっくり寄る＝副題「ペンタゴンの中庭（2025年）」。中庭に無人機の展示が写る＝映像方針で原寸を見て、締めに合わなければ別の点）',
               src='—'),
    'cb18': dict(kind='写真',
               plan='MEM24B｜副題：現在の93便の追悼の場（2024年の空撮）｜動き：ゆっくり寄る｜権利：C（CC0）｜出典の行：Designism（CC0）｜注：CC0｜台本の画：実写 93便の追悼の場（別の点・後年・全画面＝副題「現在の93便の追悼の場」）',
               src='国立公園局（`Flight 93 National Memorial`）'),
    'cb19': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（あの朝の4機）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-13）：図解 第10章（11カット）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「その後の空」と4字以上同じ並びを見出し・副題に入れない（門番 dup）。人は描かない。
#   年表 AX_AFTER（2001年1月〜2004年12月）＝cb05・cb07・cb11・cb12（ca20 から続く）。「この朝」は左へ振る（右の法律の札と同じ段に並べる）
_ax = ss.ax
_YN = "年月は記録の値"
_DR = "扉は模式（決まりは法律と委員会報告）"
SPEC.update({
    # cb02（2行）＝全米の地図。止めた空港（輪）→ 9月13日 午前11時（p556）→ 2行目で基準を満たした空港から開く（p327）
    "cb02": dict(
        t="空が開く", s="新しい保安の基準と空港",
        fig=("m21", dict(view="us", start=dict(air="on", stop="on"),
                         steps=[dict(tag=dict(t="9月13日 午前11時", at="top")),
                                dict(state=dict(reopen="on"), tag=dict(t="基準を満たした空港", at="top2"))],   # ⚠️ geom_gap：「…空港から」は右の端がミネアポリスの輪に 4.4px
                         rel=[dict(t="9月13日 午前11時", src="委員会報告 p556")],
                         note="空港の点と、開いた空港は模式（どの空港が先かは描かない）", src=ss.src(["委員会報告 p327", "委員会報告 p556"]))),
    ),
    # cb05（2行）＝年表。2001年11月の法律（p391・法律）→ 2行目で運輸保安庁ができる
    "cb05": dict(
        t="法律と役所", s="法律でできた国の役所",
        fig=("axis", dict(ss.AX_AFTER, past=[_ax("day911", anchor="end")], start=dict(cur="2001-09-11"),
                          steps=[dict(add=_ax("law01"), cur="2001-11-19"),
                                 dict(add=dict(k="chips", at="2001-11-19", chips=["運輸保安庁（TSA）ができる"], rec="法律 p1"))],
                          note=_YN, src=ss.src(["法律 p1", "委員会報告 p391"]))),
    ),
    # cb07（2行）＝法律から1年の帯（期限＝法律の日から1年）→ 2行目（字幕だけ）
    "cb07": dict(
        t="1年の期限", s="国の検査員を置く期限",
        fig=("axis", dict(ss.AX_AFTER, past=[_ax("day911", anchor="end"), _ax("law01")], start=dict(cur="2001-11-19"),
                          steps=[dict(add=_ax("law01y"), cur="2002-11-19"), dict()],
                          note=_YN, src=ss.src(["法律 p1"]))),
    ),
    # cb09（2行）＝操縦室の扉。飛ぶあいだは鍵（法律）→ 2行目で事件の前も同じ決まり・守られないことも（p85）
    "cb09": dict(
        t="鍵の決まり", s="飛行中の扉の決まり",
        fig=("m21", dict(view="door", steps=[dict(state=dict(lock="on"), tag=dict(t="飛ぶあいだは鍵をかけたまま", at="rule")),
                                             dict(state=dict(loose="on"), tag=dict(t="事件の前：守られないことも", at="loose"))],
                         note=_DR, src=ss.src(["法律 p1", "委員会報告 p85"]))),
    ),
    # cb10（3行）＝問い（丈夫な扉）→ 2行目で「要求に従う」＝扉が開く → 3行目で委員会の見方（p85）
    "cb10": dict(
        t="扉の強さ", s="従うやり方が続くなら",
        fig=("m21", dict(view="door", start=dict(lock="on"),
                         steps=[dict(state=dict(vault="on"), tag=dict(t="丈夫な扉", at="vault")),
                                dict(state=dict(lock="open", door="open", comply="on")),
                                dict(tag=dict(t="違いはほとんど無い", d="委員会の見方", at="loose"))],
                         note=_DR, src=ss.src(["委員会報告 p85"]))),
    ),
    # cb11（2行）＝年表。2002年11月の国土安全保障省の法律（p391）→ 2行目で運輸保安庁もその一部に
    "cb11": dict(
        t="新しい省", s="運輸保安庁の行き先",
        fig=("axis", dict(ss.AX_AFTER, past=[_ax("day911", anchor="end"), _ax("law01"), _ax("law01y", t="")], start=dict(cur="2001-11-19"),
                          steps=[dict(add=_ax("dhs02"), cur="2002-11"),
                                 dict(add=dict(k="chips", at="2002-11", chips=["運輸保安庁もその一部に"], rec="委員会報告 p391"))],
                          note=_YN, src=ss.src(["委員会報告 p391"]))),
    ),
    # cb12（3行）＝年表。2002年11月 委員会（序文）→ 2004年7月 報告書（govinfo）→ 3行目で「この動画の主な資料」
    "cb12": dict(
        t="調べた委員会", s="委員会の設置と報告書",
        fig=("axis", dict(ss.AX_AFTER, past=[_ax("day911", anchor="end"), _ax("law01"), _ax("law01y", t=""), _ax("dhs02")],
                          start=dict(cur="2002-11"),
                          steps=[dict(add=_ax("com02"), cur="2002-11-27"), dict(add=_ax("rep04"), cur="2004-07-22"),
                                 dict(add=dict(k="chips", at="2004-07-22", chips=["この動画の主な資料"], rec="govinfo p1"))],
                          note=_YN, src=ss.src(["委員会報告の序文 p15", "govinfo p1"]))),
    ),
    # cb13（2行）＝勧告の箱。前置き → 2行目で名簿の勧告（p393）
    "cb13": dict(
        t="報告書の勧告", s="名簿の使い方と爆発物の検査",
        fig=("m21", dict(view="recom", steps=[dict(), dict(state=dict(c1="on"))], note="箱の並びは模式（勧告は委員会報告の記録）",
                         src=ss.src(["委員会報告 p393"]))),
    ),
    # cb14（2行）＝爆発物の勧告（p393）→ 2行目で「優先して」
    "cb14": dict(
        t="爆発物", s="乗客の身の回りの検査",
        fig=("m21", dict(view="recom", start=dict(c1="on"),
                         steps=[dict(state=dict(c2="on")), dict(state=dict(hl2="on"), tag=dict(t="優先して", at="under2"))],
                         note="箱の並びは模式（勧告は委員会報告の記録）", src=ss.src(["委員会報告 p393"]))),
    ),
    # cb16（2行）＝2つの調べ。空の側に印（この動画で追った側）→ 2行目で何を知り、何を知らなかったか
    "cb16": dict(
        t="2つの調べ", s="管制と軍の記録と建物の調べ",
        fig=("m21", dict(view="two", steps=[dict(state=dict(hl="on"), tag=dict(t="この動画で追った側", at="top")),
                                            dict(state=dict(k="on"))],
                         note="箱は模式", src=ss.src(["NIST p7001", "委員会報告 p1"]))),
    ),
    # cb19（2行）＝その朝の4機（衝突と墜落）→ 2行目（字幕だけ）
    "cb19": dict(
        t="あの朝の4機", s="衝突と墜落の時刻",
        fig=("axis", dict(ss.AX_ALL, steps=[dict(add=[_ax("hit11"), _ax("hit175"), _ax("hit77"), _ax("crash93")], cur="10:03:11"), dict()],
                          note="時刻は委員会報告の記録（資料で割れる時刻＝委員会報告の値）",   # ⚠️ 門番 dup：副題の「衝突と墜落の時刻」を注に書かない
                          src=ss.src(["委員会報告 p7", "委員会報告 p8", "委員会報告 p10", "委員会報告 p30"]))),
    ),
})

# ── 🆕 ⑤b-7（2026-10-13）：写真・イメージ・映像（PLAN＝映像方針の一覧・了承②／書き方は c2.py の ⑤b-7 の注）──
_D912 = P("dod_pentagon_visit_0912")
_F05 = P("fema_3905_0914")
_TSA = P("stock/tsa_checkpoint_2020")
_DOOR = P("stock/cockpit_door_2015")
_F94 = P("fema_3894_0914")
_P23 = P("pentagon_aerial_2023")
_M24B = P("flight93_memorial_aerial_2024_12")
SPEC.update({
    # cb01（7.1秒・章の頭）＝当日の夜の演説（NARA 6171390・WHCA・16:9＝全画面・大統領だけ・音は使わない）
    "cb01": ss.vid("cb01", side="none", t="夜の演説", s="当日の夜、ホワイトハウスでの演説"),
    # cb03（3.4秒）＝9月12日、国防長官と現場を回る大統領（国防総省）。右の2人から左へ短く流す（寄せ 0.9→0.5）
    "cb03": dict(photo=_D912, **ss.mv(_D912, "l", span=(0.5, 0.9)), side="none", t="12日の訪問",
                 s="9月12日のペンタゴン（国防長官と現場を回る大統領）"),
    # cb04（3.4秒）＝9月14日、拡声器で救助の人たちに話す大統領（FEMA・消防士と作業員＝捜索の任務）。大統領へゆっくり寄る
    "cb04": dict(photo=_F05, **ss.mv(_F05, "in", 0.45, 0.45, z=1.12), side="none", t="14日の訪問",
                 s="9月14日の世界貿易センターの跡（救助の人たちに話す大統領）"),
    # cb06（9.7秒）＝イメージ（2020年の空港の保安検査・CC BY 2.0）。🔴 手前の列の客（顔 30〜40px）は束の段階で切り落とした（2400×1000＝
    #   qa_out/ep21_assets.py の CROP）・中景の人は顔 約8〜11px の遠景・青い制服は職員（公務）。横長 2.4＝寄り 1.0 で右へ流す余地がある
    "cb06": dict(photo=_TSA, **ss.mv(_TSA, "r", z=1.0, span=(0.1, 0.9)), side="none", t="国の検査員",
                 s="イメージ（2020年の空港の保安検査）"),
    # cb08（7.3秒）＝イメージ（2015年の旅客機の操縦室の扉・CC BY 2.0 de・縦長 1920×2560）。下へ流す（扉は中ほど＝寄せ 0.25→0.6）
    "cb08": dict(photo=_DOOR, **ss.mv(_DOOR, "d", span=(0.25, 0.6)), side="none", t="扉の強化", s="イメージ（2015年の旅客機の操縦室の扉）"),
    # cb15（8.4秒）＝9月14日の世界貿易センターの跡（FEMA・がれきと傾いた外壁・重機・人は小さい）・上へ流す
    "cb15": dict(photo=_F94, **ss.mv(_F94, "u"), side="none", t="建物の調べ", s="9月14日の世界貿易センターの跡"),
    # cb17（2.1秒）＝2023年5月のペンタゴンの空撮（国防総省）・ゆっくり引く
    "cb17": dict(photo=_P23, **ss.mv(_P23, "out"), side="none", t="いまの姿", s="2023年のペンタゴン（空撮）"),
    # cb18（7.2秒）＝93便の追悼の場の空撮（2024年12月・CC0）。輪の形の場へゆっくり寄る（横 0.45・縦 0.5）
    "cb18": dict(photo=_M24B, **ss.mv(_M24B, "in", 0.45, 0.5), side="none", t="国立公園局", s="現在の93便の追悼の場（2024年の空撮）"),
})
