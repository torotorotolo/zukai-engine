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
    dict(name="cabin_phone", cuts=["c309", "c614"], era="any",
         want="客室の座席にある電話（2001年以前）",
         q=["airphone seatback telephone", "in-flight telephone seat"]),
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
    dict(name="f15_alert", cuts=["c123", "c702"], era="any",
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
PICK: dict[str, str] = {}


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


def _fetch_one(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": CP.UA})
    with urllib.request.urlopen(req, timeout=60) as rs:
        dest.write_bytes(rs.read())


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
        row = next((r for r in db.get(name, {}).get("rows", [])
                    if r["title"] == title), None)
        if not row:
            print(f"  🔴 {name}: 台帳に {title} が無い"); ng += 1; continue
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


def cmd_credits():
    """`scene_jiko.PHOTO_CREDIT` に貼る行と、`ref/CREDITS.md` の表を作る。"""
    if not OUT.exists():
        print("🔴 台帳が無い。まず search"); return 2
    db = json.loads(OUT.read_text(encoding="utf-8"))
    print("# scene_jiko.PHOTO_CREDIT に足す行")
    for name, title in PICK.items():
        row = next((r for r in db.get(name, {}).get("rows", [])
                    if r["title"] == title), None)
        if not row:
            print(f'    # 🔴 {name}: 台帳に無い'); continue
        kind = row["lic_kind"]
        who = (row.get("author") or "撮影者不明")[:60]
        tail = "／パブリックドメイン" if kind == "PD" else f"／撮影 {who}／{row['license']}"
        head = "出典：" + (who if kind == "PD" else "ウィキメディア・コモンズ")
        print(f'    "ep7/{name}.jpg": "{head}{tail}",')
    return 0


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
                    choices=["search", "local", "report", "count", "fetch", "credits"])
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
    if a.cmd == "credits":
        return cmd_credits()
    return cmd_count()


if __name__ == "__main__":
    sys.exit(main())
