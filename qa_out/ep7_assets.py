# -*- coding: utf-8 -*-
"""ep7_assets.py — 7本目（9.11）の**写真の束**を作る（2026-09-13 ⑤b-1 新設）。

■ なぜ要るか
    ②③は「事故の前 幅1920以上 475点」まで**数えた**だけで、**束は1点も作っていない**
    （②の引き継ぎ §9「写真の『使う束』は作っていません」）。
    `ref/ep7/` には画像が1枚も無く、台本の**実写79カット**（＋RG237動画19カット）が
    全部空のままです。→ ここで「探す・選ぶ・落とす・出典を作る」を1本にまとめます。

■ ⚠️ この回だけの道具（`qa_out/`）
    [[project-jiko-6th-keybridge-lessons]]＝回ごとの道具は `qa_out/` に置き、
    恒久化するのは横断で効くものだけ。

■ 使い方
    python qa_out/ep7_assets.py search            # 候補を探して実測（Commons API）
    python qa_out/ep7_assets.py search --only=f15 # 欄を絞る
    python qa_out/ep7_assets.py report            # 欄ごとに候補を出す（選ぶための表）
    python qa_out/ep7_assets.py report --only=f15
    python qa_out/ep7_assets.py count             # 欄ごとの候補数だけ（在庫の測定）
    python qa_out/ep7_assets.py fetch             # PICK を ref/ep7/ に落とす
    python qa_out/ep7_assets.py credits           # 出典の文字列を作る
    python qa_out/ep7_assets.py --selftest        # 物差しの検算（陽性対照つき）

■ 🔴 守っていること
    1. **PD と CC BY だけ**（CC BY-SA の継承は動画全体に波及するので採らない。6本目と同じ）
    2. **幅1920以上・bitdepth>=8**（連続階調）。1ビットのスキャンは全画面に使えない
    3. **`date` を必ず取る** ＝ [[feedback-fallback-stills-must-match-the-era]]
       「事故の前」の欄に事故の後の写真が入ると、**門番は1件も鳴らない**
    4. 出力はファイルへ。`| tail` でつながない（[[feedback-pipes-mask-exit-codes]]）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import commons_probe as CP                                     # noqa: E402

OUT = HERE / "analytics" / "materials" / "ep7" / "assets_cand.json"
REF = HERE / "ref" / "ep7"
W_MIN, BD_MIN = 1920, 8
MAXW = 2400                    # 落とすときの上限（原寸のままだと git が太る）

# ── 使えるライセンスだけ通す ───────────────────────────────
#    ⚠️ `classify_license` は "SA" を含む語を CC BY-SA に落とすので、そこを信じる。
OK_LIC = ("PD", "CC BY")


def lic_ok(row):
    k = CP.classify_license(row.get("license"), row.get("usageterms"))
    return k in OK_LIC, k


def year_of(row):
    """撮影年（取れなければ None）。⚠️ 「事故の前／後」の判定に使う。"""
    for k in ("datetimeoriginal", "date"):
        v = row.get(k)
        if not v:
            continue
        m = re.search(r"(1[89]\d\d|20[0-4]\d)", str(v))
        if m:
            return int(m.group(1))
    return None


# ══════════════════════════════════════════════════════════
#  欄（slot）＝ ref/ep7/<name>.jpg 1枚と、それを使うカット
# ══════════════════════════════════════════════════════════
# 🔴 `era` … その欄に入れてよい撮影年の範囲。**ここが命**
#    "pre"  … 2001-09-10 まで（＝ 〜2001年）
#    "day"  … 2001年（当日）
#    "post" … 2002年以降（「今の」欄）
#    "any"  … 年を問わない（空・書類・記録装置など時点が画に出ないもの）
SLOTS = [
    # ── 街と世界貿易センター ───────────────────────────
    dict(name="manhattan_pre", cuts=["pr01"], era="pre",
         want="2001年以前のローワーマンハッタン（朝の街並み）",
         q=["Lower Manhattan skyline 1990s", "Manhattan skyline World Trade Center 1990s",
            "New York skyline 2000 World Trade Center"]),
    dict(name="commute_pre", cuts=["c218"], era="pre",
         want="朝の通勤（2001年以前のマンハッタン）",
         q=["New York City subway station 1990s", "Manhattan street crowd 1990s",
            "World Trade Center PATH station"]),
    dict(name="wtc_far", cuts=["c213"], era="pre",
         want="世界貿易センター（遠景・2001年以前）",
         q=["World Trade Center 1990s skyline", "World Trade Center from Brooklyn"]),
    dict(name="wtc_twin", cuts=["c214"], era="pre",
         want="ツインタワー（2001年以前）",
         q=["World Trade Center twin towers 1990s", "World Trade Center 1993"]),
    dict(name="wtc_base", cuts=["c215"], era="pre",
         want="世界貿易センターの足元（2001年以前）",
         q=["World Trade Center plaza", "World Trade Center base facade"]),
    dict(name="wtc_south", cuts=["c311"], era="pre",
         want="ツインタワーの南棟（2001年以前）",
         q=["Two World Trade Center South Tower", "World Trade Center south tower 1990s"]),
    dict(name="wtc_under", cuts=["c801"], era="pre",
         want="世界貿易センターの地下（2001年以前）",
         q=["World Trade Center concourse mall", "World Trade Center parking garage 1993",
            "World Trade Center bombing 1993 crater"]),
    # ── 空港（2001年以前）─────────────────────────────
    dict(name="lobby_pre", cuts=["pr05"], era="pre",
         want="2001年以前の空港ロビー",
         q=["airport terminal 1990s passengers", "airport concourse 1995"]),
    dict(name="security_pre", cuts=["c111"], era="pre",
         want="2001年以前の保安検査場",
         q=["airport security checkpoint 1990s", "airport metal detector 1990s",
            "x-ray baggage screening airport 1990s"]),
    dict(name="gate_pre", cuts=["c114", "c204"], era="pre",
         want="空港の搭乗口（2001年以前）",
         q=["airport boarding gate 1990s", "airport departure gate jetway 1990s"]),
    dict(name="fids_pre", cuts=["c320"], era="pre",
         want="空港の出発案内板（2001年以前）",
         q=["airport flight information display 1990s", "airport departure board 1990s"]),
    dict(name="logan", cuts=["c106"], era="pre",
         want="ボストン・ローガン空港（2001年以前）",
         q=["Logan International Airport 1990s", "Boston Logan Airport terminal 2000"]),
    dict(name="logan_apron", cuts=["c116"], era="pre",
         want="ローガン空港の駐機場",
         q=["Logan Airport apron aircraft", "Boston Logan Airport ramp"]),
    dict(name="logan_takeoff", cuts=["c115"], era="pre",
         want="ローガン空港を離陸する旅客機",
         q=["Logan Airport takeoff Boeing", "aircraft departing Logan Airport"]),
    dict(name="dulles", cuts=["c107"], era="pre",
         want="ワシントン・ダレス空港（2001年以前）",
         q=["Dulles International Airport main terminal 1990s",
            "Washington Dulles terminal Saarinen"]),
    dict(name="dulles_rwy", cuts=["c117"], era="pre",
         want="ダレス空港の滑走路",
         q=["Dulles Airport runway", "Dulles International Airport aerial"]),
    dict(name="reagan", cuts=["c415"], era="pre",
         want="レーガン・ナショナル空港（2001年以前）",
         q=["Ronald Reagan Washington National Airport 1990s",
            "Washington National Airport terminal"]),
    dict(name="newark_757", cuts=["c602"], era="pre",
         want="ニューアーク空港を離陸する757",
         q=["Newark International Airport Boeing 757", "United Airlines 757 takeoff"]),
    # ── 機体と機内 ───────────────────────────────────
    dict(name="b767", cuts=["c108"], era="pre",
         want="ボーイング767（2001年以前）",
         q=["American Airlines Boeing 767-200", "Boeing 767-200ER American Airlines"]),
    dict(name="b757", cuts=["c109"], era="pre",
         want="ボーイング757（2001年以前）",
         q=["American Airlines Boeing 757-200", "United Airlines Boeing 757-200 1990s"]),
    dict(name="b767_cruise", cuts=["c201"], era="any",
         want="巡航するボーイング767",
         q=["Boeing 767 in flight", "Boeing 767 airborne"]),
    dict(name="b767_takeoff", cuts=["c302"], era="any",
         want="離陸するボーイング767",
         q=["Boeing 767 takeoff rotate", "Boeing 767 departing runway"]),
    dict(name="b757_takeoff", cuts=["c402"], era="any",
         want="離陸するボーイング757",
         q=["Boeing 757 takeoff", "Boeing 757 departing runway"]),
    dict(name="airliner_cruise", cuts=["c403"], era="any",
         want="巡航する旅客機",
         q=["airliner in flight cruise altitude", "jet airliner in flight above clouds"]),
    dict(name="refuel", cuts=["c119"], era="any",
         want="給油中の旅客機（2001年以前）",
         q=["aircraft refuelling airport fuel truck", "airliner refueling apron"]),
    dict(name="cabin_pre", cuts=["c205"], era="pre",
         want="旅客機の客室（2001年以前）",
         q=["airliner cabin economy class 1990s", "Boeing 767 cabin interior"]),
    dict(name="cockpit_door_pre", cuts=["c202"], era="pre",
         want="旅客機の操縦室の扉（2001年以前）",
         q=["airliner cockpit door", "flight deck door airliner"]),
    dict(name="cabin_phone", cuts=["c614"], era="any",
         want="旅客機の客室（c614）",
         q=["airphone seatback telephone", "in-flight telephone seat"]),
    # 🔴 2026-09-14（⑤c'）**c309 を別の欄に割った。**
    #   c309 と c614 は `cabin_phone.jpg` を共有していて、⑤c-2 で
    #   **画素の差 0＝まったく同じ絵**と分かった（`ep7_qa_look2.md` §E-1）。
    #   ⚠️ 「座席にある電話」の写真は Commons に**1点も無い**
    #     （唯一の `Flight 93 GTE Airfone` は PD だが **600×390** で使えない）。
    #   → 副題から電話の主張を落とし、**767 の客室**にする（11便・175便と同じ型）。
    dict(name="cabin_767", cuts=["c309"], era="any",
         want="ボーイング767の客室（c614 と別の絵）",
         q=["Boeing 767 cabin interior seats", "wide-body airliner cabin economy seats"]),
    dict(name="cockpit_pre", cuts=["c605"], era="pre",
         want="旅客機の操縦室（2001年以前）",
         q=["Boeing 757 cockpit", "Boeing 767 flight deck"]),
    dict(name="window_cruise", cuts=["c304"], era="any",
         want="巡航する旅客機の窓",
         q=["airliner window view wing", "view from airplane window wing"]),
    dict(name="window_sky", cuts=["c909"], era="any",
         want="飛行機の窓から見た空",
         q=["view from airplane window clouds", "airplane window sky above clouds"]),
    # ── 管制 ────────────────────────────────────────
    dict(name="artcc_screen_pre", cuts=["pr09"], era="pre",
         want="航空路管制センターの画面（2001年当時）",
         q=["air route traffic control center radar display",
            "FAA air traffic control center 1990s"]),
    dict(name="radar_scope_pre", cuts=["c210"], era="pre",
         want="管制卓のレーダー画面（2001年当時）",
         q=["air traffic control radar scope", "ARTS radar display controller"]),
    dict(name="controller_pre", cuts=["c306"], era="pre",
         want="管制卓に着く管制官（2001年当時）",
         q=["air traffic controller at console", "FAA controller radar position"]),
    dict(name="artcc_screen2", cuts=["c509"], era="pre",
         want="管制卓の画面（2001年当時）",
         q=["en route air traffic control display", "air traffic control sector console"]),
    dict(name="artcc_alt", cuts=["c608"], era="any",
         want="管制卓の画面（高度の表示）",
         q=["air traffic control data block altitude", "radar data block aircraft altitude"]),
    dict(name="artcc_seat", cuts=["ep03"], era="any",
         want="航空路管制センターの席",
         q=["air route traffic control center workstation",
            "air traffic control center empty console"]),
    dict(name="boston_artcc_ext", cuts=["c212"], era="any",
         want="ボストンの航空路管制センター（外観）",
         q=["Boston Air Route Traffic Control Center Nashua",
            "air route traffic control center building exterior"]),
    dict(name="indy_artcc", cuts=["c406"], era="any",
         want="インディアナポリスの管制センター",
         q=["Indianapolis Air Route Traffic Control Center",
            "air route traffic control center Indiana"]),
    dict(name="cleveland_artcc", cuts=["c606"], era="any",
         want="クリーブランドの管制センター",
         q=["Cleveland Air Route Traffic Control Center Oberlin",
            "air route traffic control center Ohio"]),
    dict(name="atcscc", cuts=["c502"], era="any",
         want="連邦航空局コマンドセンター（外観）",
         q=["FAA Air Traffic Control System Command Center Herndon",
            "FAA Command Center Warrenton"]),
    dict(name="aoc_pre", cuts=["c310", "c408", "c603"], era="any",
         want="航空会社の運航管理室（2001年以前）",
         q=["airline operations control center dispatcher",
            "airline dispatch center flight dispatcher"]),
    # ── ペンタゴン ───────────────────────────────────
    dict(name="pentagon_ext_pre", cuts=["c409"], era="pre",
         want="ペンタゴン（外観・2001年以前）",
         q=["The Pentagon exterior 1990s", "Pentagon building Arlington 1998"]),
    dict(name="pentagon_aerial_pre", cuts=["c410"], era="pre",
         want="ペンタゴンの空撮（2001年以前）",
         q=["Pentagon aerial view 1998", "The Pentagon aerial photograph 1990s"]),
    dict(name="pentagon_court_pre", cuts=["c412"], era="pre",
         want="ペンタゴンの中庭（2001年以前）",
         q=["Pentagon center courtyard", "Pentagon courtyard ground zero cafe"]),
    dict(name="pentagon_west_day", cuts=["c421"], era="day",
         want="ペンタゴン西側（当日・遠景）",
         q=["Pentagon September 11 2001 west side", "Pentagon 9/11 damage exterior"]),
    # ── 軍 ─────────────────────────────────────────
    # 🔴 2026-09-14（⑤c'）**c702 を別の欄に割った。**
    #   c123 と c702 は `f15_alert.jpg` を共有していて、⑤c の A-6 で
    #   **画素の差 0＝まったく同じ絵**と分かった（`ep7_qa_look1.md` §A-6）。
    dict(name="f15_alert2", cuts=["c702"], era="any",
         want="駐機中のF-15（c123 と別の絵）",
         q=["F-15 Eagle flight line parked", "F-15 Strike Eagle sits on the flight line"]),
    dict(name="f15_alert", cuts=["c123"], era="any",
         want="待機中のF-15（オーティス基地）",
         q=["F-15 Eagle alert hangar 102nd Fighter Wing",
            "F-15 Eagle Otis Air National Guard Base"]),
    dict(name="f15_takeoff", cuts=["c703"], era="any",
         want="離陸するF-15",
         q=["F-15 Eagle takeoff afterburner", "F-15 Eagle departing runway"]),
    dict(name="f16_alert", cuts=["c707"], era="any",
         want="待機中のF-16（ラングレー基地）",
         q=["F-16 Langley Air Force Base 1st Fighter Wing",
            "F-16 Fighting Falcon alert ramp"]),
    dict(name="f16_takeoff", cuts=["c711"], era="any",
         want="離陸するF-16",
         q=["F-16 Fighting Falcon takeoff", "F-16 departing runway afterburner"]),
    dict(name="base_rwy", cuts=["c708"], era="any",
         want="基地の滑走路（2001年以前）",
         q=["Air Force Base runway aerial", "air base runway empty"]),
    dict(name="fighter_dc", cuts=["c717"], era="any",
         want="首都上空を飛ぶ戦闘機",
         q=["F-16 over Washington DC Noble Eagle",
            "fighter aircraft over Washington Monument"]),
    dict(name="andrews", cuts=["c719"], era="any",
         want="アンドルーズ基地（2001年以前）",
         q=["Andrews Air Force Base aerial", "Andrews Air Force Base flight line"]),
    # ── 当日（2001-09-11）────────────────────────────
    dict(name="wtc_smoke_day", cuts=["c313"], era="day",
         want="北棟から上がる煙（遠景・2001-09-11）",
         q=["World Trade Center smoke September 11 2001 distant",
            "World Trade Center north tower smoke skyline"]),
    dict(name="fire_trucks_day", cuts=["c314"], era="day",
         want="現場へ向かう消防車（2001-09-11）",
         q=["FDNY fire trucks September 11 2001", "fire apparatus World Trade Center 2001"]),
    dict(name="shanksville_day", cuts=["c622"], era="day",
         want="シャンクスビルの野原（当日・遠景）",
         q=["United Airlines Flight 93 crash site Shanksville 2001",
            "Flight 93 crash site field Pennsylvania 2001"]),
    dict(name="apron_day", cuts=["pr10"], era="day",
         want="駐機場に降りた旅客機（2001-09-11）",
         q=["grounded aircraft September 11 2001 airport",
            "airliners parked ramp September 2001"]),
    dict(name="apron_lined_day", cuts=["c516", "ep05"], era="day",
         want="駐機場に並んだ旅客機（2001-09-11）",
         q=["aircraft parked tarmac ground stop 2001",
            "airliners lined up apron September 2001"]),
    dict(name="stopped_day", cuts=["c505"], era="day",
         want="空港で止まった旅客機（2001-09-11）",
         q=["airliner stopped taxiway 2001", "grounded airliner terminal September 2001"]),
    dict(name="stranded_day", cuts=["c517"], era="day",
         want="空港で足止めされた人たち（2001-09-11）",
         q=["stranded passengers airport September 2001",
            "airport passengers waiting terminal 2001"]),
    # ── 記録・書類 ──────────────────────────────────
    dict(name="report_cover", cuts=["pr07"], era="any",
         want="委員会報告の表紙",
         q=["9/11 Commission Report cover", "National Commission Terrorist Attacks report"]),
    dict(name="report_page", cuts=["c817"], era="any",
         want="委員会報告のページ",
         q=["9/11 Commission Report page", "open book page report text"]),
    dict(name="hearing", cuts=["c807"], era="any",
         want="委員会の公聴会（2003〜2004年）",
         q=["9/11 Commission hearing 2004", "National Commission hearing witnesses 2003"]),
    dict(name="library_reports", cuts=["c815"], era="any",
         want="図書館に並ぶ報告書",
         q=["government documents library shelves", "bound reports library shelf"]),
    dict(name="nist_report", cuts=["c813"], era="any",
         want="建物側の報告書（NIST NCSTAR 1）",
         q=["NIST NCSTAR report cover", "NIST World Trade Center investigation report"]),
    dict(name="recorder", cuts=["c805"], era="any",
         want="記録装置（ブラックボックス）",
         q=["flight data recorder orange", "cockpit voice recorder unit"]),
    dict(name="atc_tape", cuts=["c803"], era="any",
         want="管制施設の録音装置（2001年当時）",
         q=["multichannel tape recorder rack", "reel to reel logging recorder"]),
    dict(name="logbook", cuts=["c809"], era="any",
         want="当直の記録簿（書式の見本）",
         q=["military duty log book page", "watch log book handwritten"]),
    # ── 「今」の5枚（🔴 ⑤a の宿題 #2）──────────────────
    dict(name="security_now", cuts=["c901"], era="post",
         want="今の空港の保安検査場",
         q=["TSA airport security checkpoint", "airport security screening passengers TSA"]),
    # 🔴 2026-09-14（⑤c'）**c902 の地を別の絵にした。**
    #   c901 と c902 は `security_now.jpg` を共有していて、⑤c-2 で
    #   **3人が肩を組んでカメラへ笑う広報写真**（中央は公人）と分かった。
    #   ⚠️ 米国の検査場で PD／CC BY の写真は **171点あるが全部** 長官の視察・会見。
    #     → 「人が主役でない検査の場面」で探し直し、**列**（c901）と
    #       **X線の監視**（c902）に割った。副題からは国名の主張を落とす。
    #   ⚠️ `cuts` は空（c902 は `cuts/__init__.py` の BACKDROP で地に敷く欄）。
    dict(name="security_screen", cuts=[], era="post",
         want="X線の画面を見る検査員（c902 の地）",
         q=["x-ray baggage screening belt airport", "airport security screener monitor"]),
    dict(name="cockpit_door_hard", cuts=["c903"], era="post",
         want="強化された操縦室の扉",
         q=["reinforced cockpit door", "hardened flight deck door airliner"]),
    dict(name="artcc_now", cuts=["c905"], era="post",
         want="今の航空路管制センター",
         q=["air route traffic control center ERAM", "FAA en route center modern displays"]),
    dict(name="lobby_now", cuts=["c907"], era="post",
         want="今の空港の出発ロビー",
         q=["airport departure hall modern", "airport check-in hall passengers"]),
    # ── 空 ─────────────────────────────────────────
    dict(name="clear_sky", cuts=["ep01"], era="any",
         want="よく晴れた空",
         q=["clear blue sky", "blue sky cirrus clouds"]),
]

ERA_RANGE = {"pre": (1960, 2001), "day": (2001, 2001), "post": (2002, 2030),
             "any": (1900, 2030)}

# ══════════════════════════════════════════════════════════
#  2周目（1周目で候補0だった31欄）
# ══════════════════════════════════════════════════════════
# 🔴 1周目の結果（`qa_out/ep7_assets_count.txt`）＝**73欄のうち31欄が0点**。
#    落ちた理由は「素材が無い」ではなく**探し方**だった：
#      ・題名の全文検索は Commons の**分類（Category）を見ない**
#      ・管制室・空港の内部・報告書は**米連邦の職務著作**で、分類に固まって入っている
#      ・当日の写真は ②が数えた 9,283行のプール（`material_photo_rows.json`）に**もう在る**
#        ＝ API を1単位も使わずに引ける（`local` で引く）
# `cat:` で始める語は**分類の中を歩く**（`commons_probe.cat_files`）。
Q2 = {
    "wtc_under": ["cat:Category:World Trade Center bombing (1993)",
                  "World Trade Center concourse 1990s"],
    "lobby_pre": ["cat:Category:Airport terminals in the United States",
                  "airport terminal interior 1990s"],
    "security_pre": ["cat:Category:Airport security", "airport security 1998"],
    "gate_pre": ["cat:Category:Airport gates", "airport jet bridge 1990s"],
    "fids_pre": ["cat:Category:Flight information display systems",
                 "airport information board"],
    "reagan": ["cat:Category:Ronald Reagan Washington National Airport"],
    "cabin_pre": ["cat:Category:Aircraft cabins", "aircraft cabin 1990s"],
    "cabin_phone": ["cat:Category:Airphone", "seatback telephone aircraft"],
    "artcc_screen_pre": ["cat:Category:Air traffic control in the United States",
                         "cat:Category:Air traffic control radar"],
    "radar_scope_pre": ["cat:Category:Radar displays", "air traffic control display"],
    "artcc_screen2": ["cat:Category:Air route traffic control centers"],
    "artcc_alt": ["cat:Category:Air traffic control", "radar display aircraft target"],
    "artcc_seat": ["cat:Category:Air traffic controllers",
                   "air traffic control workstation"],
    "boston_artcc_ext": ["cat:Category:Boston Air Route Traffic Control Center",
                         "Nashua New Hampshire FAA center"],
    "indy_artcc": ["cat:Category:Indianapolis Air Route Traffic Control Center",
                   "FAA Indianapolis center"],
    "cleveland_artcc": ["cat:Category:Cleveland Air Route Traffic Control Center",
                        "Oberlin Ohio FAA center"],
    "atcscc": ["cat:Category:Air Traffic Control System Command Center",
               "FAA Herndon Virginia command center"],
    "pentagon_ext_pre": ["cat:Category:The Pentagon", "Pentagon building 1990s photo"],
    "wtc_smoke_day": ["cat:Category:World Trade Center on 9/11"],
    "apron_day": ["cat:Category:Aviation on September 11 attacks",
                  "airport September 11 2001 grounded"],
    "apron_lined_day": ["cat:Category:Aircraft on the ground",
                        "parked airliners apron many"],
    "stopped_day": ["cat:Category:Airliners at airports", "airliner on taxiway"],
    "stranded_day": ["cat:Category:Airport waiting areas", "airport passengers waiting"],
    "report_cover": ["cat:Category:9/11 Commission", "9/11 Commission Report"],
    "report_page": ["cat:Category:Book pages", "open report page text"],
    "hearing": ["cat:Category:9/11 Commission", "congressional hearing witness table"],
    "library_reports": ["cat:Category:Library shelves",
                        "cat:Category:Government publications"],
    "nist_report": ["cat:Category:National Institute of Standards and Technology",
                    "NIST World Trade Center"],
    "atc_tape": ["cat:Category:Reel-to-reel tape recorders",
                 "cat:Category:Magnetic tape data storage"],
    "logbook": ["cat:Category:Logbooks", "handwritten log page"],
    "artcc_now": ["cat:Category:Air traffic control in the United States",
                  "FAA en route center 2010s"],
}

# ══════════════════════════════════════════════════════════
#  3周目（2周目でも候補0だった12欄）
# ══════════════════════════════════════════════════════════
# 🔴 2周目で 31→12欄。残った12欄は**同じ被写体の別の欄が当たっている**ことが多い
#    （`artcc_seat` 274点・`artcc_alt` 119点・`apron_lined_day` 93点が当たっている）。
#    ＝ 「素材が無い」ではなく「その欄の語だけが当たらなかった」。
#    → 当たっている欄の語を借りる。⚠️ **借りるのは語だけ。写真は欄ごとに別の1枚を採る**
#      （同じ絵を別のカットで使い回すと、視聴者には同じ絵に見える
#       → [[feedback-duplicate-art-needs-pixel-comparison]]）。
# ⚠️ 施設の外観4欄（ボストン／インディアナポリス／クリーブランド／コマンドセンター）は
#    **その建物そのものの写真が Commons に無い**。よその管制センターを出して
#    「ボストンの」と名乗るのは**写っていないものを名乗る**ことになるので採らない
#    → [[feedback-subtitle-must-match-what-is-visible]]。**図に振り替える**（⑤b-2 で決める）。
Q3 = {
    "artcc_screen_pre": ["cat:Category:Air traffic controllers",
                         "cat:Category:Air traffic control", "radar display aircraft target"],
    "artcc_screen2": ["cat:Category:Air traffic controllers",
                      "cat:Category:Air traffic control"],
    "artcc_now": ["cat:Category:Air traffic controllers",
                  "air traffic control workstation"],
    "atc_tape": ["cat:Category:Tape recorders", "cat:Category:Sound recording",
                 "multitrack tape recorder"],
    "cabin_phone": ["cat:Category:Aircraft seats", "aircraft seat back",
                    "aircraft cabin seat row"],
    "apron_day": ["cat:Category:Aircraft on the ground",
                  "parked airliners apron many"],
    "stopped_day": ["cat:Category:Airliners at airports",
                    "cat:Category:Aircraft on the ground"],
    "library_reports": ["cat:Category:Bookshelves", "cat:Category:Bookcases",
                        "library shelves books"],
}

# ── ②が数えた 9,283行のプール（API を1単位も使わない）────────────
_POOL = (HERE / "analytics" / "materials" / "ep7" / "material_photo_rows.json")
# 欄 → プールの題・説明に当てる語（どれか1つでも入っていれば候補）
LOCAL_Q = {
    "wtc_smoke_day": ["smoke", "burning", "skyline"],
    "wtc_under": ["concourse", "mall", "plaza", "lobby"],
    "wtc_far": ["skyline", "from brooklyn", "manhattan skyline"],
    "wtc_twin": ["twin towers", "world trade center"],
    "wtc_base": ["plaza", "base", "facade"],
    "wtc_south": ["south tower", "2 world trade"],
    "manhattan_pre": ["skyline", "lower manhattan"],
    "commute_pre": ["subway", "path station", "street"],
    "fire_trucks_day": ["fire", "fdny", "engine", "apparatus"],
    "shanksville_day": ["shanksville", "flight 93", "crash site", "field"],
    "pentagon_west_day": ["pentagon"],
    "pentagon_aerial_pre": ["pentagon aerial", "aerial view pentagon"],
    "hearing": ["commission", "hearing"],
    "recorder": ["recorder", "black box", "fdr", "cvr"],
    "report_cover": ["report", "commission"],
}


def era_ok(slot, row):
    """撮影年が欄の時点に合っているか。年が取れない行は `None`（判定できない）。"""
    y = year_of(row)
    if y is None:
        return None
    lo, hi = ERA_RANGE[slot["era"]]
    return lo <= y <= hi


# ══════════════════════════════════════════════════════════
#  選んだ1枚（`report` を見て手で書く）
# ══════════════════════════════════════════════════════════
# 🔴🔴 2026-09-13（⑤b-2）**1枚ずつ題名と説明を読んで手で決めた。**
#   自動で「中身の網を通った先頭」を採らせたら、65欄のうち十数件が別物だった
#   （`qa_out/ep7_pick.py` の docstring に実例）。網は**候補を絞る道具**であって、
#   選ぶ道具ではない。
#
# 🔴 副題に「2001年以前」と書けるのは **撮影年が実際にそうだと台帳で確かめられた欄だけ**。
#   確かめられない欄は、副題から年の主張を落として**撮影年をそのまま書く**
#   （例「ボーイング767　2025年撮影」）。画面に嘘を出さないための線。
#   → 該当する欄は `ref/CREDITS.md` §9.11 と各章ファイルの注に書いてある。
#
# 🔴 写真が1点も無く**図に振り替えた欄**（`ep7_pick.FIG_SLOTS` と1対1）:
#   boston_artcc_ext / indy_artcc / cleveland_artcc / atcscc … その建物の写真が無い
#   aoc_pre … 航空会社の運航管理室の写真が無い（出てくるのは天文台・原子炉の制御室）
#   cockpit_door_hard … 「強化された扉」と分かる写真が無い（操縦室の写真はあるが別物）
#   report_cover / report_page / nist_report … 報告書そのものの写真が無い
PICK: dict[str, str] = {
    # ── 街と世界貿易センター ───────────────────────────
    "manhattan_pre": "File:World Trade Center towers, New York, LCCN2015645969.jpg",
    "commute_pre": "File:Downfolders-downfolder34-2011 02 02 00 10 05.jpg",
    "wtc_far": "File:World Trade Center, New York. Exterior. Twilight view from harbor - LCCN2021636615.jpg",
    "wtc_twin": "File:View of the New World Trade Center, 1971.jpg",
    "wtc_base": "File:World Trade Center Exterior Entrance arches with Sphere at Plaza Fountain sculpture - LCCN2021638448.jpg",
    "wtc_south": "File:World Trade Center, New York. Exterior. View from plaza - LCCN2020714989.jpg",
    "wtc_under": "File:World Trade Center, New York. Exterior. Night view - LCCN2021636612.jpg",
    # ── 空港（2001年以前） ─────────────────────────────
    "lobby_pre": "File:Memphis-international-airport-1970s.jpg",
    "security_pre": "File:Orange County Airport, security officer, Sept. 1970.jpg",
    "gate_pre": "File:Boarding Southwest Airways B737-700 N242WN at Long Island MacArthur Airport, February 20, 2023.jpg",
    # 🔴 ⑤c'：ジュネーブ（欧州）の板 → **シカゴ・オヘア**の板（米国の地名が並ぶ）
    "fids_pre": "File:Departure Board at ORD.jpg",
    "logan": "File:LOGAN AIRPORT-CONTROL TOWER AND RUNWAYS SEEN FROM 16TH FLOOR OBSERVATION DECK - NARA - 548428.jpg",
    "logan_apron": "File:Eastern Air Lines terminal at Logan Airport, 1969.jpg",
    "logan_takeoff": "File:United 737-800 N73283 takeoff roll Boston Dec 2024.jpg",
    "dulles": "File:Aerial view of Dulles Airport, June 1985.JPEG",
    "dulles_rwy": "File:Aerial view of Dulles Airport 03.jpg",
    "reagan": "File:E Concourse DCA National Airport 2025-10-22 15-05-36 1.jpg",
    "newark_757": "File:United 757-200 at EWR (37116055471).jpg",
    # ── 機体と機内 ─────────────────────────────────────
    "b767": "File:Delta Boeing 767-300ER N194DN at Boston May 2025.jpg",
    "b757": "File:Delta 757-200 N710TW taxiing at Boston Nov 2024.jpg",
    "b767_cruise": "File:Lufthansa A350-900 and United 767-300ER above Boston.jpg",
    # 🔴 ⑤c'：FedEx の**貨物機**（しかも巡航中）→ アメリカン航空の 767（出発滑走）
    "b767_takeoff": "File:N352AA (15113637598).jpg",
    "b757_takeoff": "File:Delta Boeing 757-200 N702TW departing Boston April 2025 1.jpg",
    "airliner_cruise": "File:Aircraft crossing paths.jpg",
    "refuel": "File:Fueling Boeing 757-200 N58101 at Boston January 2026.jpg",
    "cabin_pre": "File:Airplane aisle during flight (Unsplash).jpg",
    "cockpit_door_pre": "File:Puerto Rico — A 320 JetBlue — Open cockpit door during boarding.jpg",
    "cabin_phone": "File:A220 Main Cabin (43799968340).jpg",
    # 🔴 ⑤c'：c309 用。c614（A220）と**別の絵**にする
    "cabin_767": "File:Delta 767-400ER Economy Cabin.jpg",
    "cockpit_pre": "File:Avelo Airlines B737 Cockpit.jpg",
    "window_cruise": "File:20250928 View from aircraft in Turkey 01 (31935).jpg",
    "window_sky": "File:20250928 View from aircraft in Egypt 01 (21624).jpg",
    # ── 管制 ───────────────────────────────────────────
    # 🔴 ⑤c'：AFCENT の現代の事務室（画面はウェブページ）→ **ワシントン航空路管制センター**
    "artcc_screen_pre": "File:AirTraffic-8.jpg",
    "radar_scope_pre": "File:SR&T Plan position indicator.jpg",
    "controller_pre": "File:Air traffic controllers of the 1961st Communications Group man their duty stations in the base tower. The 1961st recently won the Major General Harold M. McClelland Award for commun - DPLA - 6a16bbcae66aff3a8a8616188e1d2e07.jpeg",
    "artcc_screen2": "File:378th EOSS Air Traffic Controller Demonstration (8829390).jpg",
    "artcc_alt": "File:Kingpin and Controllers Maintain Aircraft and Airspace DVIDS265967.jpg",
    "artcc_seat": "File:ATC aids TBM Avenger pilot (6666391).jpeg",
    # ── ペンタゴン ─────────────────────────────────────
    "pentagon_ext_pre": "File:The Pentagon US Department of Defense building.jpg",
    "pentagon_aerial_pre": "File:An aerial view of the Pentagon - DPLA - 2bad8af340141770c277509bf649c466.jpeg",
    # 🔴 ⑤c'：マスクの制服2人と旗（中庭が1画素も無い）→ **中庭そのもの**
    "pentagon_court_pre": "File:XQ-58A Valkrie displayed at the Pentagon Center Courtyard.jpg",
    "pentagon_west_day": "File:DM-SD-02-03925.JPEG",
    # ⚠️ 2026-09-13（⑤b-2）DoD の `010911-M-CI426-*` は **8点とも本体が切れている**
    #   （Commons 側の不良。1〜13バイト足りず PIL が開けない）。読めたのはこの1点だけ。
    #   撮影 CPL JASON INGERSOLL, USMC／2001-09-11／「煙が晴れたあとのペンタゴン」
    # ── 軍 ─────────────────────────────────────────────
    "f15_alert": "File:Fond Farewell to F-15C A5095 (8605970).jpg",
    # 🔴 ⑤c'：c702 用。c123 と**別の絵**にする（いまは画素の差 0）
    "f15_alert2": ("File:A 494th EFS F-15E Strike Eagle sits on the flight line "
                   "prior to a sortie at Prince Sultan Air Base.jpg"),
    "f15_takeoff": "File:391st FS F-15E prepares for takeoff at MCAS Iwakuni during Northern Edge 23-2.jpg",
    # 🔴 ⑤c'：隊員が1人立つだけ（F-16 が無い）→ **駐機した F-16 が主役**
    "f16_alert": "File:F-16s Arrive at NATO Air Base Geilenkirchen (8403619).jpg",
    # 🔴 ⑤c'：有刺鉄線が全面（機体はぼけた影）→ **滑走路を離れた瞬間の F-16**
    "f16_takeoff": ("File:Colorado and Massachusetts Air National Guard fighter jets "
                    "depart Lithuania during exercise Air Defender 2023 (7867984).jpg"),
    "base_rwy": "File:Aerial view of Tan Son Nhut Air Base down main runway.jpg",
    # 🔴 ⑤c'：ほぼ無地の灰色（戦闘機が見えない）→ **2001年10月の飛行中の F-16**
    "fighter_dc": "File:F-16C NJ ANG in flight Oct 2001.jpg",
    "andrews": "File:76th AS Last C-40 on ramp.jpg",
    # ── 当日 ───────────────────────────────────────────
    "wtc_smoke_day": "File:Skyline of Manhattan with smoke billowing from the Twin Towers (29385426736).jpg",
    "fire_trucks_day": "File:LOC unattributed Ground Zero photos, September 11, 2001 - item 210.jpg",
    # 🔴🔴 ⑤c'：**この1枚はシャンクスビルですらなかった。**元の説明は
    #   「A worker at the crash site takes a break ... **at the Pentagon** on Sept. 14, 2001」
    #   ＝ペンタゴンの復旧作業の写真。⑤c-2 は「防護服の手元」までは見たが、
    #   **場所が違うこと**は出どころを読むまで分からなかった（画には地名が写らない）。
    #   → 93便が落ちた野原（いまは追悼施設）。副題の年は 2015 に直す。
    "shanksville_day": "File:Flight 93 Memorial - panoramio (1).jpg",
    # 🔴🔴 ⑤c'：Alaska の 737-9 MAX（2024年・胴体の `Alaska` が読める）→
    #   搭乗橋に並んで駐まった旅客機。⚠️ 9/11 当日に降ろされた機体の写真は
    #   PD／CC BY に**1点も無い**（Operation Yellow Ribbon も0点）。副題から日付を落とす。
    "apron_day": "File:Southwest 737s parked at Terminal A at DCA (39815401742).jpg",
    "apron_lined_day": "File:At gate B24 at Boston Logan International Airport January 2026.jpg",
    "stopped_day": "File:United Boeing 737 at Gate B25 at Boston September 2023.jpg",
    "stranded_day": "File:Philadelphia Airport Lounge (36335419103).jpg",
    # ── 記録・書類 ─────────────────────────────────────
    "hearing": "File:Congressional Hearing - Jul. 24, 2012 (7748554726).jpg",
    "library_reports": "File:Books, Community Languages, Takapuna Library.jpg",
    "recorder": "File:Miami Air Flight 293 flight recorder (32830135147).jpg",
    "atc_tape": "File:Studer B67 reel-to-reel audio tape recorder, ca. 1978 (cropped and edited, larger 10 inch tapes).jpg",
    # 🔴 ⑤c'：ロシア語のグライダー耐空記録簿（キリル文字が大きく読める）→
    #   英語の飛行記録簿（英空軍・1943年の手書き）
    "logbook": "File:Billy Strachan log book.jpg",
    # ── 「今」 ─────────────────────────────────────────
    # 🔴🔴 ⑤c'：3人が肩を組む広報写真（中央は公人）→ **検査を待つ列**。
    #   ⚠️ 米国の検査場の PD／CC BY はすべて長官の視察・会見だった（171点）。
    #     副題からは国名を落とし「空港の保安検査　2016年撮影」とだけ書く。
    "security_now": "File:0083 Domodedovo International Airport 16th of August 2016.jpg",
    "security_screen": "File:2016 04 19 Airport Security-5 (26744283185).jpg",
    "artcc_now": "File:378th EOSS Air Traffic Controller Demonstration (8829389).jpg",
    "lobby_now": "File:Gillette–Campbell County Airport terminal interior in Campbell County, Wyoming (2).jpg",
    # ── 空 ─────────────────────────────────────────────
    "clear_sky": "File:20250928 View from aircraft in Turkey 01 (79961).jpg",
}


# ── Commons を叩く ────────────────────────────────────────
def _imageinfo2(titles):
    """`commons_probe.imageinfo` ＋ **撮影日**。年を取らないと時点の食い違いが見えない。"""
    out = []
    for i in range(0, len(titles), CP.BATCH):
        part = titles[i:i + CP.BATCH]
        d = CP._get({"action": "query", "prop": "imageinfo", "titles": "|".join(part),
                     "iiprop": "url|size|bitdepth|mime|extmetadata"})
        for pg in d.get("query", {}).get("pages", []):
            ii = (pg.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata") or {}

            def g(k, em=em):
                return (em.get(k) or {}).get("value")

            out.append({
                "title": pg.get("title"), "w": ii.get("width"), "h": ii.get("height"),
                "bitdepth": ii.get("bitdepth"), "mime": ii.get("mime"),
                "license": g("LicenseShortName"), "usageterms": g("UsageTerms"),
                "author": _plain(g("Artist")), "credit": _plain(g("Credit")),
                "date": _plain(g("DateTimeOriginal")) or _plain(g("DateTime")),
                "desc": _plain(g("ImageDescription")),
                "url": ii.get("url"),
            })
    return out


def _plain(s):
    if not s:
        return None
    s = re.sub(r"<[^>]+>", " ", str(s))
    return re.sub(r"\s+", " ", s).strip() or None


def _keep(s, rows, wmin):
    """網に掛ける。**通った理由と落ちた理由を数で残す**（0点の欄の原因が分かるように）。"""
    keep, why = [], dict(small=0, bit=0, lic=0)
    for r in rows:
        if not r.get("w") or r["w"] < wmin:
            why["small"] += 1; continue
        if (r.get("bitdepth") or 0) < BD_MIN:
            why["bit"] += 1; continue
        ok, kind = lic_ok(r)
        if not ok:
            why["lic"] += 1; continue
        r["lic_kind"] = kind
        r["era_ok"] = era_ok(s, r)
        r["year"] = year_of(r)
        keep.append(r)
    keep.sort(key=lambda r: (r["era_ok"] is not True, r["era_ok"] is False,
                             -(r["w"] * r["h"])))
    return keep, why


def cmd_local(only=None, wmin=None):
    """🔴 ②が数えた 9,283行のプールから引く（**API を1単位も使わない**）。

    ⚠️ プールは 9/11 の分類だけなので、当日・WTC・ペンタゴンの欄にしか効かない。
       効かない欄に当てて 0点が出ても「素材が無い」ではない
       （[[feedback-absence-of-a-word-is-not-absence]]）。
    """
    if not _POOL.exists():
        print(f"🔴 プールが無い: {_POOL}"); return 2
    wmin = wmin or W_MIN
    pool = json.loads(_POOL.read_text(encoding="utf-8"))["rows"]
    print(f"■ プール {len(pool)}行 から引きます（幅>={wmin}）")
    db = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    for s in SLOTS:
        if only and s["name"] not in only:
            continue
        words = LOCAL_Q.get(s["name"])
        if not words:
            continue
        hit = []
        for r in pool:
            hay = f"{r.get('title', '')} {r.get('desc', '')} {r.get('objname', '')}".lower()
            if any(w in hay for w in words):
                hit.append(dict(r))
        keep, why = _keep(s, hit, wmin)
        d = db.setdefault(s["name"], dict(want=s["want"], era=s["era"],
                                          cuts=s["cuts"], tried=0, kept=0, rows=[]))
        have = {r["title"] for r in d["rows"]}
        add = [r for r in keep if r["title"] not in have]
        d["rows"] = (d["rows"] + add)[:24]
        d["tried"] += len(hit)
        d["kept"] = len(d["rows"])
        print(f"  {s['name']:22} 当たり {len(hit):4}行 → 通った {len(keep):3}"
              f"（足した {len(add):2}）  落ちた内訳 小{why['small']} 2値{why['bit']} 権利{why['lic']}")
    OUT.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n台帳 → {OUT}")
    return 0


def cmd_search(only=None, limit=60, wmin=None, use_q2=False):
    """欄ごとに候補を探して実測し、**通ったものだけ**を台帳に足す。"""
    db = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    wmin = wmin or W_MIN
    slots = [s for s in SLOTS if not only or s["name"] in only]
    if use_q2:
        _tbl = Q3 if use_q2 == 3 else Q2
        slots = [s for s in slots if s["name"] in _tbl]
    print(f"■ {len(slots)}欄を探します（幅>={wmin}・bitdepth>={BD_MIN}・{'/'.join(OK_LIC)}"
          f"{'・2周目の語' if use_q2 else ''}）")
    for s in slots:
        titles = []
        qs = ((Q3.get(s["name"], []) if use_q2 == 3 else Q2.get(s["name"], [])) if use_q2 else s["q"])
        for q in qs:
            try:
                if q.startswith("cat:"):
                    # 🔴 分類の中を歩く（題名の全文検索は分類を見ない）
                    got, cats = CP.cat_files(q[4:], depth=2, limit=400)
                    titles += got
                else:
                    titles += CP.search_files(q, limit=limit)
            except Exception as e:                              # noqa: BLE001
                print(f"  🔴 {s['name']}: 検索が落ちた（{q}）: {e}")
        titles = [t for t in dict.fromkeys(titles)
                  if re.search(r"\.(jpe?g|png|tiff?)$", t, re.I)]
        rows = _imageinfo2(titles) if titles else []
        keep, why = _keep(s, rows, wmin)
        d = db.setdefault(s["name"], dict(want=s["want"], era=s["era"],
                                          cuts=s["cuts"], tried=0, kept=0, rows=[]))
        have = {r["title"] for r in d["rows"]}
        add = [r for r in keep if r["title"] not in have]
        # 🔴 時点が合っているものを先に（`_keep` が並べ替えてある）
        d["rows"] = sorted(d["rows"] + add,
                           key=lambda r: (r.get("era_ok") is not True,
                                          r.get("era_ok") is False,
                                          -(r["w"] * r["h"])))[:24]
        d["tried"] += len(titles)
        d["kept"] = len(d["rows"])
        print(f"  {s['name']:22} 候補 {len(titles):4}点 → 通った {len(keep):3}点"
              f"（足した {len(add):2}／時点が合う "
              f"{sum(1 for r in d['rows'] if r.get('era_ok') is True):3}点）"
              f"  落ちた内訳 小{why['small']} 2値{why['bit']} 権利{why['lic']}")
        # 🔴🔴 **1欄ごとに保存する。** 2026-09-13 に、最後に1回だけ書く作りで
        #    3周目が途中で止まり、**ログには出ているのに台帳には1件も残らなかった**
        #    （`count` が 0点のまま＝「探したのに無い」に見えた）。
        #    ＝ **ログの緑と台帳の中身を混ぜない**。`ep7_shots_run.py` と同じ作りにする。
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(0.2)
    print(f"\n台帳 → {OUT}")
    return 0


def cmd_count():
    """欄ごとの在庫だけ出す。🔴 **0点の欄を先に見せる**（図へ振り替える判断のため）。"""
    if not OUT.exists():
        print("🔴 台帳が無い。まず search"); return 2
    db = json.loads(OUT.read_text(encoding="utf-8"))
    rows = []
    for s in SLOTS:
        d = db.get(s["name"])
        if not d:
            rows.append((s["name"], -1, -1, s["era"], s["want"])); continue
        fit = sum(1 for r in d["rows"] if r["era_ok"] is True)
        rows.append((s["name"], d["kept"], fit, s["era"], s["want"]))
    rows.sort(key=lambda r: (r[2], r[1]))
    print(f"{'欄':24}{'通った':>6}{'時点も合う':>10}  時点  中身")
    zero = 0
    for n, k, f, era, want in rows:
        mark = "🔴" if k <= 0 else ("⚠️" if f == 0 else "  ")
        if k <= 0:
            zero += 1
        print(f"{mark}{n:22}{k:>6}{f:>10}  {era:4}  {want}")
    print(f"\n■ 欄 {len(rows)} ／ 候補0の欄 {zero}")
    return 2 if zero else 0


def cmd_report(only=None, n=6):
    if not OUT.exists():
        print("🔴 台帳が無い。まず search"); return 2
    db = json.loads(OUT.read_text(encoding="utf-8"))
    for s in SLOTS:
        if only and s["name"] not in only:
            continue
        d = db.get(s["name"])
        print(f"\n■ {s['name']}  ({s['era']})  {s['want']}  → {','.join(s['cuts'])}")
        if not d or not d["rows"]:
            print("   🔴 候補なし"); continue
        for r in d["rows"][:n]:
            e = {True: "✓", False: "🔴年", None: "?年"}[r["era_ok"]]
            print(f"   {e} {r['w']}x{r['h']} {r['lic_kind']:6} {str(r['year']):>5} "
                  f"{r['title'][5:90]}")
            if r.get("author"):
                print(f"       撮影 {r['author'][:80]}")
    return 0


def _fetch_one(url, dest, tries=4):
    """🔴 2026-09-13（⑤b-2）**長さを突き合わせてから保存する。**

    もとは `rs.read()` の戻りをそのまま書いていたので、**途中で切れた本体を
    「落とせた」として保存**していた（PIL が `image file is truncated` で落ちて
    はじめて分かる。DoD の 3600x2362 の系列で3回とも再現した）。
    ⚠️ 落ちたから気づけただけで、**画像として開けてしまう切れ方なら黙って通る**
       → [[feedback-parsers-fail-closed]]。長さで見る。
    """
    last = None
    for k in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": CP.UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as rs:
                want = int(rs.headers.get("Content-Length") or 0)
                buf = rs.read()
            if want and len(buf) < want:
                last = f"本体が短い（{len(buf)}/{want} バイト）"
                time.sleep(2 * (k + 1))
                continue
            dest.write_bytes(buf)
            return
        except Exception as e:                                  # noqa: BLE001
            last = f"{type(e).__name__}: {e}"
            time.sleep(2 * (k + 1))
    raise RuntimeError(f"{tries}回とも落とせなかった（{last}）")


def cmd_fetch(only=None):
    """PICK を `ref/ep7/` に落として、幅 MAXW に縮める。"""
    from PIL import Image
    if not OUT.exists():
        print("🔴 台帳が無い。まず search"); return 2
    db = json.loads(OUT.read_text(encoding="utf-8"))
    REF.mkdir(parents=True, exist_ok=True)
    ng = 0
    for name, title in PICK.items():
        if only and name not in only:
            continue
        dest = REF / f"{name}.jpg"
        if dest.exists():
            print(f"  ・{name} は在る（{dest.stat().st_size // 1024}KB）"); continue
        # 🔴 2026-09-13（⑤b-2）**題名は台帳ぜんたいから引く。**
        #   欄ごとの `rows` だけを見る作りだったので、「別の欄の一覧で見つけた1枚」を
        #   選ぶと「台帳に無い」で落ちた（14欄／実際には台帳に在る）。
        #   ⚠️ それでも無いときは **API で引き直す**（黙って別の絵を出さない）。
        row = next((r for r in db.get(name, {}).get("rows", [])
                    if r["title"] == title), None)
        if not row:
            row = next((r for d in db.values() for r in d.get("rows", [])
                        if r["title"] == title), None)
        if not row:
            got = _imageinfo2([title])
            row = got[0] if got and got[0].get("url") else None
            if row:
                ok, kind = lic_ok(row)
                if not ok:
                    print(f"  🔴 {name}: {title} は使えない権利（{kind}）"); ng += 1; continue
                row["lic_kind"] = kind
        if not row:
            print(f"  🔴 {name}: 台帳にも Commons にも {title} が無い"); ng += 1; continue
        tmp = REF / f"_{name}.bin"
        try:
            _fetch_one(row["url"], tmp)
            with Image.open(tmp) as im:
                im = im.convert("RGB")
                if im.width > MAXW:
                    im = im.resize((MAXW, round(im.height * MAXW / im.width)),
                                   Image.LANCZOS)
                im.save(dest, "JPEG", quality=88, optimize=True)
            print(f"  ✓ {name}  {dest.stat().st_size // 1024}KB")
        except Exception as e:                                  # noqa: BLE001
            print(f"  🔴 {name}: {e}"); ng += 1
        finally:
            tmp.unlink(missing_ok=True)
    return 2 if ng else 0


def _who(row):
    """撮影者の表記を1行にする。

    🔴 2026-09-13（⑤b-2）**HTML と引用符が混ざる。**
      `Artist` は Commons の wikitext がそのまま入るので
      `<div class="fn value"><a rel="nofollow" …` や
      `"DoD photo by Master Sgt. Ken Hammond, U.S. Air Force."` のような値が来る。
      そのまま Python の文字列に貼ると**行が壊れる**（実際に2件壊れた）。
      → タグを落とし、前後の引用符と句点を落とし、二重引用符を全角に置き換える。
    """
    s = _plain(row.get("author")) or _plain(row.get("credit")) or "撮影者不明"
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"\s+", " ", s).strip().strip('"“”').strip().rstrip("。.")
    s = s.replace('"', "”").replace("\\", "／")
    # 「Unknown author Unknown author」のような二重を1つに畳む
    s = re.sub(r"^(.*?)\s+\1$", r"\1", s)
    return (s or "撮影者不明")[:60]


def cmd_credits():
    """`scene_jiko.EP7_PHOTO` に貼る行と、`ref/CREDITS.md` の表を作る。"""
    if not OUT.exists():
        print("🔴 台帳が無い。まず search"); return 2
    db = json.loads(OUT.read_text(encoding="utf-8"))
    # 🔴 題名は**台帳ぜんたい**から引く（欄ごとの rows だけだと9欄が「無い」になる）。
    index = {r["title"]: r for d in db.values() for r in d.get("rows", [])}
    print("# scene_jiko.EP7_PHOTO に貼る行")
    ng = 0
    resolved = {}          # 🔴 下の表でも使い回す（台帳に無くても Commons から引けた行）
    for name, title in PICK.items():
        row = index.get(title)
        if not row:
            got = _imageinfo2([title])
            row = got[0] if got else None
            if row:
                row["lic_kind"] = lic_ok(row)[1]
                # 🔴🔴 2026-09-14（⑤c'）**ここで `year` を入れ忘れていた。**
                #    台帳に在る欄は `_keep()` が `year` を付けるが、Commons から引き直した欄は
                #    付かないまま表に出るので、**撮影年が全部「不明」**になっていた
                #    （差し替えた13欄のうち8欄）。年は副題の主張と突き合わせる根拠そのもの
                #    ＝ここが空だと `check_credits.py` が何も測れない（[[feedback-parsers-fail-closed]]）。
                row["year"] = year_of(row)
        if not row:
            print(f'    # 🔴 {name}: 台帳にも Commons にも無い'); ng += 1; continue
        resolved[name] = row
        kind = row.get("lic_kind") or lic_ok(row)[1]
        who = _who(row)
        lic = _plain(row.get("license")) or ""
        tail = "／パブリックドメイン" if kind == "PD" else f"／撮影 {who}／{lic}"
        head = "出典：" + (who if kind == "PD" else "ウィキメディア・コモンズ")
        print(f'    "ep7/{name}.jpg": "{head}{tail}",')
    print("\n# ref/CREDITS.md §9.11 の表")
    print("| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 元の題名 |")
    print("|---|---|---:|---|---|---|")
    for name, title in PICK.items():
        # 🔴🔴 2026-09-13（⑤b-2b）：ここは `index.get` だけを見て `continue` していた。
        #    ＝**台帳に無い欄を黙って表から落としていた**（`andrews` の1行が消え、
        #    64欄あるのに表は63行だった。数えるまで誰も気づかない）。
        #    クレジットの欠落は権利の話で、CC BY は撮影者名が使用条件そのもの。
        #    → 上の loop が Commons から引いた行を使い回し、それでも無ければ
        #      **🔴 を出して exit を上げる**（[[feedback-parsers-fail-closed]]）。
        row = index.get(title) or resolved.get(name)
        if not row:
            print(f"| `{name}` | 🔴 出どころが引けない（黙って落とさずここで止める） |")
            ng += 1
            continue
        s = next((x for x in SLOTS if x["name"] == name), {})
        print(f"| `{name}` | {' '.join(s.get('cuts', []))} | {row.get('year') or '不明'} "
              f"| {row.get('lic_kind')}（{_plain(row.get('license'))}） | {_who(row)} "
              f"| {title[5:]} |")
    return 2 if ng else 0


def cmd_fb():
    """`footage.USE` の各欄から**ひかえの静止画** `ref/ep7/fb_<cid>.jpg` を焼く。

    🔴 `footage._cut_stream()` は「URL から要る区間だけをコマに切り出す（落とさない）」作りで、
       手元に mp4 は残らない。→ **URL から直接1コマ抜く**（6本目 `keybridge_assets.fb` と同じ）。
    🔴 **SAR を直す。** RG237 の 32点中27点が SAR=10:11 で、そのまま抜くと横に10%ふくらむ
       （[[feedback-container-labels-lie-about-the-picture]]）。`scale=iw*sar:ih,setsar=1`。
    ⚠️ 焼けた枚数だけでなく**作れなかった欄を必ず名前で出す**（黙って0枚で通さない）。
    ⚠️ 続けて投げると素材の側が絞るので、1枚ごとに間を空けて3回まで試す。
    """
    import subprocess
    import footage as FO
    REF.mkdir(parents=True, exist_ok=True)
    n, miss = 0, []

    def made(q):
        return q.exists() and q.stat().st_size > 0

    for cid, u in sorted(FO.USE.items()):
        at = min(float(u["start"]) + 0.4, float(u["until"]) - 0.2)
        dest = REF / f"fb_{cid}.jpg"
        if made(dest):
            n += 1
            continue
        c = FO.CLIPS[u["clip"]]
        vf = ["scale=iw*sar:ih", "setsar=1"] if int(c.get("dispw") or c["w"]) != int(c["w"]) else []
        for attempt in range(3):
            for src in FO.urls_of(u["clip"]):
                cmd = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
                       "-user_agent", FO.UA, "-ss", f"{at:.2f}", "-i", src,
                       "-frames:v", "1", "-q:v", "2"]
                if vf:
                    cmd += ["-vf", ",".join(vf)]
                cmd.append(str(dest))
                subprocess.run(cmd, capture_output=True, timeout=900)
                if made(dest):
                    break
            if made(dest):
                break
            print(f"  ⚠️ {cid}: 焼けなかった（{attempt + 1}回目）", flush=True)
            time.sleep(6 * (attempt + 1))
        if made(dest):
            n += 1
            print(f"  ✓ {cid}  {dest.stat().st_size // 1024}KB", flush=True)
            time.sleep(1.5)
        else:
            miss.append(cid)
    print(f"■ ひかえの静止画 {n} 枚／{len(FO.USE)} 欄"
          + (f"　🔴 作れなかった {len(miss)}欄: {miss}" if miss else "　✓ 全欄"))
    return 2 if miss else 0


def selftest():
    """🔴 物差しの検算。**陽性対照＝わざと外れる入力で落ちること**を値で見る。"""
    ok = []

    def chk(name, got):
        ok.append(bool(got))
        print(f"  {'✓' if ok[-1] else '🔴'} {name}")

    chk("陰性：CC BY-SA は通さない",
        lic_ok({"license": "CC BY-SA 4.0", "usageterms": "CC BY-SA 4.0"})[0] is False)
    chk("陽性：PD は通る", lic_ok({"license": "Public domain",
                                  "usageterms": "Public domain"})[0] is True)
    chk("陽性：CC BY は通る", lic_ok({"license": "CC BY 4.0",
                                     "usageterms": "CC BY 4.0"})[0] is True)
    chk("年を拾う（1998）", year_of({"date": "Taken on 3 May 1998"}) == 1998)
    chk("年が無ければ None", year_of({"date": "unknown"}) is None)
    s_pre = dict(name="x", era="pre", cuts=[], want="", q=[])
    chk("陽性対照：pre の欄に 2011年の写真は落ちる",
        era_ok(s_pre, {"date": "2011-05-02"}) is False)
    chk("陽性対照：pre の欄に 1998年の写真は通る",
        era_ok(s_pre, {"date": "1998-05-02"}) is True)
    chk("年が取れない行は None（合格にも不合格にもしない）",
        era_ok(s_pre, {"date": None}) is None)
    chk("欄の数とカットの数", sum(len(s["cuts"]) for s in SLOTS) == 79)
    dup = [c for s in SLOTS for c in s["cuts"]]
    chk("カットIDが重複していない", len(dup) == len(set(dup)))
    print(f"\n{'✓ 物差しは通った' if all(ok) else '🔴 物差しが壊れている'}"
          f"（{sum(ok)}/{len(ok)}）")
    return 0 if all(ok) else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="count",
                    choices=["search", "local", "report", "count", "fetch", "credits", "fb"])
    ap.add_argument("--only", default="")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--w", type=int, default=0, help="幅の下限（既定 1920）")
    ap.add_argument("--q2", type=int, nargs="?", const=2, default=0,
                    help="2＝2周目の語（分類を歩く）／3＝3周目の語")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    only = [x for x in a.only.split(",") if x]
    if a.cmd == "local":
        return cmd_local(only, a.w or None)
    if a.cmd == "search":
        return cmd_search(only, wmin=a.w or None, use_q2=a.q2)
    if a.cmd == "report":
        return cmd_report(only, a.n)
    if a.cmd == "fetch":
        return cmd_fetch(only)
    if a.cmd == "fb":
        return cmd_fb()
    if a.cmd == "credits":
        return cmd_credits()
    return cmd_count()


if __name__ == "__main__":
    sys.exit(main())
