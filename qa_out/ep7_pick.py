# -*- coding: utf-8 -*-
"""ep7_pick.py — 写真の候補が「欄の中身を写しているか」を測る門番（2026-09-13 ⑤b-2 新設）。

■ 🔴🔴 なぜ要るか（⑤b-1 の穴）
    `ep7_assets.py` の網は **権利・幅・bitdepth・撮影年**しか見ていない。
    Commons の全文検索はあいまいに当てるので、**中身がまるで違う点が上位に並ぶ**。
    ⑤b-2 の頭で `report` を読んで実際に出ていたもの：

      b767_cruise（巡航するボーイング767） 1位 … 1876年の『ラ・フォンテーヌ寓話』
      b767      （ボーイング767）          1位 … ボーイング**757**の写真
      artcc_screen_pre（管制画面2001年）    1位 … 1965年の空母の艦載機
      apron_day （当日の駐機場の旅客機）    1位 … DARPA の無人機 X-47A のロールアウト
      wtc_smoke_day（北棟から上がる煙）     1位 … **2001年8月**の無傷のツインタワー

    ＝ `count` の「候補 N点」は**在庫ではない**。[[feedback-measure-visibility-not-presence]]
    ⚠️ とくに `wtc_smoke_day` は era="day"（2001年）を**通ってしまう**。
       撮影月まで見ないと「事故の前の絵」が当日の欄に入る
       （[[feedback-fallback-stills-must-match-the-era]]。門番は1本も鳴らない）。

■ 何を測るか
    題名＋説明＋物件名を1つの藁（hay）にして、
      MUST … このどれか1つに当たること（当たらなければ**その欄の中身ではない**）
      NG   … これに当たったら落とす（図・地図・模型・記念式典など「写っていない」もの）
    ⚠️ **MUST を緩めて数を作らない。** 数が足りないなら図に振り替えるのが正しい
       （[[feedback-subtitle-must-match-what-is-visible]]）。

■ 使い方
    python qa_out/ep7_pick.py audit              # 欄ごとに「中身も合う」候補数
    python qa_out/ep7_pick.py rank --only=b767   # 通った候補だけ出す（選ぶための表）
    python qa_out/ep7_pick.py hunt --only=b767   # 分類を歩いて足す（4周目）
    python qa_out/ep7_pick.py --selftest         # 🔴 陽性・陰性の対照を**値**で見る
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "qa_out"))
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import ep7_assets as A                                          # noqa: E402
import commons_probe as CP                                      # noqa: E402

# ══════════════════════════════════════════════════════════
#  欄ごとの「中身」の網
# ══════════════════════════════════════════════════════════
# 🔴 MUST は **or**（どれか1つ）。NG は **or**（1つでも当たれば落とす）。
#    小文字化した「題名 + 説明 + 物件名」に対して正規表現で当てる。
NG_ALL = [
    r"\bmap\b", r"\bdiagram\b", r"\bchart\b", r"\bposter\b", r"\bmontage\b",
    r"\btimeline\b", r"\blogo\b", r"\bcoat of arms\b", r"\bstamp\b",
    r"\bmodel of\b", r"\bscale model\b", r"\bmemorial\b", r"\bmuseum\b",
    r"\bcemetery\b", r"\bgrave\b", r"\bpatch\b", r"\binsignia\b",
]

SLOT_RULES = {
    # ── 街と世界貿易センター ───────────────────────────
    "manhattan_pre": dict(
        must=[r"world trade cent", r"lower manhattan", r"manhattan skyline",
              r"twin towers"],
        ng=[r"empire state", r"brooklyn bridge", r"ground ?zero", r"9-11", r"september 11", r"attack", r"smoke",
            r"construction", r"chicago", r"willis tower", r"sears tower"],
        cat=["cat:World Trade Center (1973-2001)",
             "cat:Lower Manhattan in the 1990s"]),
    "commute_pre": dict(
        must=[r"subway", r"commut", r"pedestrian", r"street.*crowd",
              r"crowd.*street", r"sidewalk", r"path (train|station)"],
        ng=[r"chicago", r"london", r"tokyo", r"paris"],
        cat=["cat:New York City Subway in the 1990s",
             "cat:Pedestrians in New York City"]),
    "wtc_far": dict(
        must=[r"world trade cent", r"twin towers"],
        ng=[r"ground ?zero", r"attack", r"smoke", r"construction", r"1 world trade",
            r"one world trade", r"4 world trade", r"3 world trade", r"8 spruce"],
        cat=["cat:World Trade Center (1973-2001)"]),
    "wtc_twin": dict(
        must=[r"world trade cent", r"twin towers"],
        ng=[r"ground ?zero", r"attack", r"smoke", r"bombing", r"construction",
            r"perpetrator", r"events montage"],
        cat=["cat:World Trade Center (1973-2001)"]),
    "wtc_base": dict(
        must=[r"world trade cent.*(plaza|entrance|base|lobby|concourse)",
              r"(plaza|entrance|lobby|concourse).*world trade cent",
              r"austin j\.? tobin plaza", r"wtc plaza"],
        ng=[r"ground ?zero", r"attack", r"aerial", r"flag"],
        cat=["cat:World Trade Center (1973-2001)"]),
    "wtc_south": dict(
        must=[r"(2|two|south) world trade cent", r"south tower"],
        ng=[r"ground ?zero", r"attack", r"smoke", r"2 wtc august 20[12]",
            r"aerial photo of wtc"],
        cat=["cat:2 World Trade Center (1973-2001)"]),
    "wtc_under": dict(
        must=[r"world trade cent.*(concourse|mall|underground|station|shopping)",
              r"(concourse|underground mall).*world trade",
              r"cortlandt street", r"world trade center (path|station)"],
        ng=[r"ground ?zero", r"attack", r"exterior", r"plaza"],
        cat=["cat:World Trade Center (1973-2001)"]),
    # ── 空港（2001年以前） ─────────────────────────────
    "lobby_pre": dict(
        must=[r"(airport|terminal).*(lobby|concourse|check-?in|departure hall|interior)",
              r"(lobby|concourse|check-?in|departure hall).*(airport|terminal)",
              r"ticket counter"],
        ng=[r"lounge", r"demolition", r"cargo"],
        cat=["cat:Airport terminals in the 1990s",
             "cat:Interiors of airport terminals in the United States"]),
    "security_pre": dict(
        must=[r"(security|screening).*(checkpoint|airport|passenger)",
              r"(airport|passenger).*(security|screening)",
              r"metal detector", r"x-?ray.*(baggage|carry)"],
        ng=[r"customs", r"border protection", r"canine"],
        cat=["cat:Airport security checkpoints",
             "cat:Aviation security in the United States"]),
    "gate_pre": dict(
        must=[r"(boarding|departure) gate", r"gate area", r"jet ?bridge",
              r"jetway", r"passengers? board", r"boarding"],
        ng=[r"cargo", r"military"],
        cat=["cat:Airport gates"]),
    "fids_pre": dict(
        must=[r"(flight|departure|arrival).*(board|display|information)",
              r"(board|display).*(flight|departure|arrival)", r"solari", r"split-?flap"],
        ng=[r"memorial", r"troops"],
        cat=["cat:Flight information display systems"]),
    "logan": dict(
        must=[r"logan (international )?airport", r"boston.*airport",
              r"airport.*boston"],
        ng=[r"wildlife", r"seattle"],
        cat=["cat:Logan International Airport"]),
    "logan_apron": dict(
        must=[r"logan.*(airport|terminal|ramp|apron|gate)",
              r"boston.*(ramp|apron|gate|terminal)"],
        ng=[r"wildlife", r"children play"],
        cat=["cat:Logan International Airport"]),
    "logan_takeoff": dict(
        must=[r"(logan|boston).*(takeoff|take-?off|depart|runway|climb)",
              r"(takeoff|departing|runway).*(logan|boston)"],
        ng=[r"\bhomes?\b", r"houses", r"beach", r"observation deck", r"beach", r"wildlife"],
        cat=["cat:Logan International Airport"]),
    "dulles": dict(
        must=[r"dulles"],
        ng=[r"lounge", r"capital one", r"food", r"drink", r"buffet"],
        cat=["cat:Washington Dulles International Airport",
             "cat:Main Terminal of Washington Dulles International Airport"]),
    "dulles_rwy": dict(
        must=[r"dulles.*(runway|taxiway|apron|ramp|aerial|airfield)",
              r"(runway|taxiway|apron|aerial).*dulles"],
        ng=[r"lounge", r"marine one", r"arado"],
        cat=["cat:Washington Dulles International Airport"]),
    "reagan": dict(
        must=[r"(reagan|washington) national airport", r"national airport.*washington",
              r"\bdca\b.*airport"],
        ng=[r"193[0-9]", r"194[0-9]", r"washington airport", r"baggage claim"],
        cat=["cat:Ronald Reagan Washington National Airport"]),
    "newark_757": dict(
        must=[r"(newark|ewr).*(757|departing|takeoff|take-?off|runway)",
              r"757.*(newark|ewr)"],
        ng=[r"scrap", r"boston", r"belfast"],
        cat=["cat:Newark Liberty International Airport"]),
    # ── 機体と機内 ─────────────────────────────────────
    "b767": dict(
        must=[r"\b767\b", r"boeing 767"],
        ng=[r"\b757\b", r"\b747\b", r"\b777\b", r"scrap", r"cockpit", r"cabin"],
        cat=["cat:Boeing 767"]),
    "b757": dict(
        must=[r"\b757\b", r"boeing 757"],
        ng=[r"\b767\b", r"\b747\b", r"scrap", r"cockpit", r"cabin"],
        cat=["cat:Boeing 757"]),
    "b767_cruise": dict(
        must=[r"\b767\b.*(flight|flying|air-?to-?air|cruis|sky)",
              r"(in flight|flying|air-?to-?air).*\b767\b", r"\b767\b"],
        ng=[r"\b757\b", r"scrap", r"cockpit", r"cabin", r"la fontaine", r"biblia",
            r"gate", r"ramp", r"parked"],
        cat=["cat:Boeing 767 in flight"]),
    "b767_takeoff": dict(
        must=[r"\b767\b.*(takeoff|take-?off|departing|rotation|climb)",
              r"(takeoff|departing).*\b767\b"],
        ng=[r"\b757\b", r"\b787\b", r"landing", r"approach"],
        cat=["cat:Boeing 767 taking off"]),
    "b757_takeoff": dict(
        must=[r"\b757\b.*(takeoff|take-?off|departing|rotation|climb)",
              r"(takeoff|departing).*\b757\b"],
        ng=[r"\b767\b", r"\b787\b", r"\b777\b", r"landing", r"approach", r"embraer"],
        cat=["cat:Boeing 757 taking off"]),
    "airliner_cruise": dict(
        must=[r"(airliner|airbus a3|boeing 7).*(in flight|flying|air-?to-?air|cruis)",
              r"(in flight|flying|air-?to-?air).*(airliner|airbus|boeing)"],
        ng=[r"fighter", r"military", r"\bnasa\b", r"convair", r"vacuum", r"heritage"],
        cat=["cat:Airliners in flight"]),
    "refuel": dict(
        must=[r"(refuel|fuel(l)?ing|fuel truck|bowser).*(aircraft|airliner|airplane|plane|boeing|airbus)",
              r"(aircraft|airliner|airplane|boeing|airbus).*(refuel|fuel(l)?ing)"],
        ng=[r"\bb-1b\b", r"lancer", r"bomber", r"saber strike", r"aerial refuel", r"air-?to-?air refuel", r"tanker.*boom", r"\bb-1\b",
            r"saber strike"],
        cat=["cat:Aircraft refuelling"]),
    "cabin_pre": dict(
        must=[r"(cabin|aisle|interior).*(air(craft|liner|plane)|boeing|douglas|dc-|747|727|737)",
              r"(air(craft|liner|plane)|boeing|747|727|737).*(cabin|interior|aisle)",
              r"passenger cabin"],
        ng=[r"cockpit", r"flight deck", r"cards", r"immigration", r"removal"],
        cat=["cat:Aircraft cabins"]),
    "cockpit_door_pre": dict(
        must=[r"cockpit door", r"flight deck door"],
        ng=[r"pedestal", r"museum"],
        cat=["cat:Cockpit doors"]),
    "cabin_phone": dict(
        must=[r"(seat ?back|in-?flight|airfone|air ?phone|seat).*(phone|telephone)",
              r"(phone|telephone).*(seat|cabin|in-?flight|aircraft)"],
        ng=[r"\b1918\b", r"first class", r"mobile phone", r"smartphone"],
        cat=["cat:Telephones in aircraft", "cat:Airfone"]),
    "cockpit_pre": dict(
        must=[r"(cockpit|flight deck).*(boeing|airliner|747|767|757|737|727|dc-|md-)",
              r"(boeing|airliner|747|767|757|737|727).*(cockpit|flight deck)"],
        ng=[r"fighter", r"helicopter", r"defence force", r"military", r"c-130"],
        cat=["cat:Aircraft cockpits of Boeing aircraft"]),
    "window_cruise": dict(
        must=[r"(window|porthole).*(aircraft|airliner|airplane|plane|cabin|flight)",
              r"(aircraft|airliner|cabin|in-?flight).*(window|porthole)",
              r"view from.*(window|plane|aircraft)"],
        ng=[r"beechcraft", r"cockpit", r"museum", r"at-11"],
        cat=["cat:Views from aircraft windows"]),
    "window_sky": dict(
        must=[r"(window|porthole).*(sky|cloud|wing)", r"(sky|cloud).*(window|porthole)",
              r"view from.*(window|plane|aircraft)"],
        ng=[r"cockpit", r"museum"],
        cat=["cat:Views from aircraft windows"]),
    # ── 管制 ───────────────────────────────────────────
    "artcc_screen_pre": dict(
        must=[r"(radar|air traffic).*(scope|screen|display|console)",
              r"(scope|screen|display|console).*(radar|air traffic)",
              r"air route traffic control"],
        ng=[r"korridor", r"luftkorridore", r"berlin", r"aircraft carrier", r"uss ", r"f-4", r"skyhawk", r"seasprite",
            r"firefighter", r"live fire"],
        cat=["cat:Air traffic control centers in the United States",
             "cat:Radar displays"]),
    "radar_scope_pre": dict(
        must=[r"radar (scope|screen|display|console)", r"(scope|screen).*radar",
              r"plan position indicator"],
        ng=[r"\buss\b", r"combat information", r"amphibious", r"\bship\b", r"firefighter", r"live fire", r"contingency response", r"world war"],
        cat=["cat:Radar displays"]),
    "controller_pre": dict(
        must=[r"air traffic controller", r"controller.*(console|scope|position)",
              r"(radar|approach) controller"],
        ng=[r"president", r"strike", r"rose garden", r"patco", r"statement", r"kyrgyzstan", r"marine", r"rokaf", r"carrier", r"sailor directs"],
        cat=["cat:Air traffic controllers"]),
    "artcc_screen2": dict(
        must=[r"(radar|air traffic).*(scope|screen|display|console)",
              r"(scope|screen|display|console).*(radar|air traffic)",
              r"air route traffic control"],
        ng=[r"aircraft carrier", r"uss ", r"f-4", r"skyhawk", r"seasprite"],
        cat=["cat:Air traffic control centers in the United States"]),
    "artcc_alt": dict(
        must=[r"(radar|air traffic).*(scope|screen|display|console)",
              r"(scope|screen|display|console).*(radar|air traffic)"],
        ng=[r"aircraft carrier", r"uss ", r"avenger"],
        cat=["cat:Air traffic control centers in the United States"]),
    "artcc_seat": dict(
        must=[r"air traffic control.*(center|centre|room|position|console|sector)",
              r"(controller|operator).*(console|position|sector)"],
        ng=[r"tower cab", r"aircraft carrier"],
        cat=["cat:Air traffic control centers in the United States"]),
    "aoc_pre": dict(
        must=[r"(dispatch|operations cent|operations room|control cent).*(airline|flight|air)",
              r"(airline|flight).*(dispatch|operations cent)"],
        ng=[r"military", r"navy", r"army"],
        cat=["cat:Airline operations centers"]),
    # ── ペンタゴン ─────────────────────────────────────
    "pentagon_ext_pre": dict(
        must=[r"pentagon"],
        ng=[r"0112\d\d", r"0110\d\d", r"0109\d\d", r"december 2001", r"october 2001", r"november 2001", r"attack", r"september 11", r"9-11", r"smoke", r"damage", r"repair",
            r"memorial", r"national airport in the foreground"],
        cat=["cat:The Pentagon in the 20th century"]),
    "pentagon_aerial_pre": dict(
        must=[r"pentagon.*aerial", r"aerial.*pentagon", r"pentagon.*(from the air|overhead)",
              r"pentagon"],
        ng=[r"attack", r"september 11", r"smoke", r"damage", r"repair", r"memorial"],
        cat=["cat:Aerial photographs of the Pentagon"]),
    "pentagon_court_pre": dict(
        must=[r"pentagon.*(courtyard|center court|inner court)",
              r"(courtyard|center court).*pentagon"],
        ng=[r"attack", r"september 11", r"smoke", r"damage", r"eisenhower"],
        cat=["cat:Center Court of the Pentagon"]),
    "pentagon_west_day": dict(
        must=[r"pentagon.*(attack|smoke|fire|damage|burn|impact|september 11|9-11)",
              r"(attack|smoke|fire|damage|september 11).*pentagon"],
        ng=[r"memorial", r"ceremony", r"anniversar", r"wreath", r"tour", r"old guard"],
        cat=["cat:Attack on the Pentagon"]),
    # ── 軍 ─────────────────────────────────────────────
    "f15_alert": dict(
        must=[r"f-15.*(alert|otis|ramp|parked|hangar|barn)",
              r"(otis|alert).*f-15", r"f-15"],
        ng=[r"in flight", r"takeoff", r"landing", r"cockpit"],
        cat=["cat:McDonnell Douglas F-15 Eagle on the ground"]),
    "f15_takeoff": dict(
        must=[r"f-15.*(takeoff|take-?off|departing|afterburner|launch|scramble)",
              r"(takeoff|departing|scramble).*f-15"],
        ng=[r"embraer", r"f-16", r"f-22", r"landing"],
        cat=["cat:McDonnell Douglas F-15 Eagle taking off"]),
    "f16_alert": dict(
        must=[r"f-16.*(alert|langley|ramp|parked|hangar|line)",
              r"(langley|alert).*f-16", r"f-16"],
        ng=[r"in flight", r"takeoff", r"f-22", r"change of command", r"red flag"],
        cat=["cat:General Dynamics F-16 Fighting Falcon on the ground"]),
    "f16_takeoff": dict(
        must=[r"f-16.*(takeoff|take-?off|departing|afterburner|launch|scramble)",
              r"(takeoff|departing|scramble).*f-16"],
        ng=[r"f-22", r"kc-135", r"tanker", r"landing", r"flyover"],
        cat=["cat:General Dynamics F-16 Fighting Falcon taking off"]),
    "base_rwy": dict(
        must=[r"(air force base|air (national guard|base)|airfield).*(runway|flight ?line|ramp|apron)",
              r"(runway|flight ?line|ramp).*(air force base|airfield|air base)"],
        ng=[r"indochina", r"tourane", r"wildlife", r"aphis"],
        cat=["cat:Runways in the United States"]),
    "fighter_dc": dict(
        must=[r"(f-15|f-16|f-22|fighter).*(washington|capitol|white house|district of columbia|dc)",
              r"(washington|capitol|white house).*(f-15|f-16|f-22|fighter)"],
        ng=[r"memorial", r"museum"],
        cat=["cat:Military aircraft over Washington, D.C."]),
    "andrews": dict(
        must=[r"andrews"],
        ng=[r"air show", r"airshow"],
        cat=["cat:Joint Base Andrews"]),
    # ── 当日 ───────────────────────────────────────────
    "wtc_smoke_day": dict(
        must=[r"(world trade|twin towers|north tower|wtc).*(smoke|burn|fire|attack|impact|september 11)",
              r"(smoke|burning|attack|september 11).*(world trade|twin towers|north tower)"],
        ng=[r"lccn2015645969", r"restoration", r"highsmith", r"august 2001", r"ground ?zero", r"collapse", r"rubble", r"debris", r"august 2001",
            r"memorial", r"anniversar"],
        cat=["cat:September 11 attacks in New York City"]),
    "fire_trucks_day": dict(
        must=[r"(fire ?truck|fire engine|fire ?fighter|fdny|ladder company|apparatus)"],
        ng=[r"memorial", r"anniversar", r"parade", r"museum"],
        cat=["cat:Fire department response to the September 11 attacks"]),
    "shanksville_day": dict(
        must=[r"(shanksville|flight 93|somerset county).*(crash|site|field|impact|crater)",
              r"(crash site|impact).*(shanksville|flight 93)"],
        ng=[r"bandana", r"artifact", r"\bflag\b", r"memorial", r"panetta", r"ceremony", r"anniversar", r"visitor cent"],
        cat=["cat:United Airlines Flight 93"]),
    "apron_day": dict(
        must=[r"(gander|halifax|yellow ribbon|grounded|diverted).*(aircraft|airliner|plane|apron|ramp|tarmac)",
              r"(aircraft|airliner|plane).*(grounded|diverted|yellow ribbon|gander)"],
        ng=[r"x-47", r"darpa", r"rollout", r"military"],
        cat=["cat:Operation Yellow Ribbon"]),
    "apron_lined_day": dict(
        must=[r"(gander|halifax|yellow ribbon|grounded|diverted).*(aircraft|airliner|plane|apron|ramp|tarmac)",
              r"(aircraft|airliner|plane).*(grounded|diverted|yellow ribbon|gander)"],
        ng=[r"x-47", r"darpa", r"rollout", r"military"],
        cat=["cat:Operation Yellow Ribbon"]),
    "stopped_day": dict(
        must=[r"(gander|halifax|yellow ribbon|grounded|diverted).*(aircraft|airliner|plane|apron|ramp|tarmac)",
              r"(aircraft|airliner|plane).*(grounded|diverted|yellow ribbon|gander)"],
        ng=[r"x-47", r"darpa", r"rollout", r"military"],
        cat=["cat:Operation Yellow Ribbon"]),
    "stranded_day": dict(
        must=[r"(stranded|stuck|waiting|passengers).*(passenger|airport|terminal|traveler)",
              r"(airport|terminal).*(stranded|crowd|waiting)"],
        ng=[r"shuttle bus", r"wattay", r"\bbus\b", r"x-47", r"customs", r"border protection", r"lounge", r"schiphol"],
        cat=["cat:Operation Yellow Ribbon"]),
    # ── 記録・書類 ─────────────────────────────────────
    "report_cover": dict(
        must=[r"(9/11|9-11|september 11).*(commission|report)",
              r"(commission|report).*(9/11|september 11)", r"book cover"],
        ng=[r"\busip\b", r"\bbpc\b", r"navy", r"army", r"convention"],
        cat=["cat:9/11 Commission"]),
    "report_page": dict(
        must=[r"(report|document|book).*(page|open|spread|text)",
              r"(page|spread).*(report|document|book)", r"printed page"],
        ng=[r"camp life", r"reader", r"workbook", r"drawing", r"plan", r"icesat", r"geographical cards", r"drawing", r"plan"],
        cat=["cat:Open books"]),
    "hearing": dict(
        must=[r"(hearing|testimony|testif|commission).*(congress|senate|house|committee|witness|panel)",
              r"(congress|senate|committee).*(hearing|testimony|witness)"],
        ng=[r"navy", r"marine", r"defense\.gov photo essay"],
        cat=["cat:9/11 Commission", "cat:United States congressional hearings"]),
    "library_reports": dict(
        must=[r"(bookshelf|book ?case|library|shelves|shelf).*(book|volume|report)",
              r"(book|volume|report).*(shelf|shelves|bookcase|library)"],
        ng=[r"charité", r"hospital", r"fortepan"],
        cat=["cat:Bookshelves"]),
    "nist_report": dict(
        must=[r"(nist|national institute of standards)",
              r"(ncstar|building.*investigation.*report)"],
        ng=[r"19[0-5][0-9]", r"beer meter", r"corrosive soils"],
        cat=["cat:National Institute of Standards and Technology"]),
    "recorder": dict(
        must=[r"(flight|cockpit|voice|data) recorder", r"black ?box.*(flight|aircraft)",
              r"\bfdr\b.*recorder", r"\bcvr\b"],
        ng=[r"dust cloud", r"training cent"],
        cat=["cat:Flight recorders"]),
    "atc_tape": dict(
        must=[r"(tape|reel|recorder|recording).*(audio|voice|sound|radio)",
              r"(audio|voice).*(tape|reel|recorder)", r"reel-to-reel"],
        ng=[r"discimage", r"video", r"studio.*music"],
        cat=["cat:Reel-to-reel audio tape recorders"]),
    "logbook": dict(
        must=[r"log ?book", r"(duty|watch|station|operations).*(log|journal|register)",
              r"(log|register).*(entry|page|book)"],
        ng=[r"bicycl", r"wellcome"],
        cat=["cat:Logbooks"]),
    # ── 「今」 ─────────────────────────────────────────
    "security_now": dict(
        must=[r"(tsa|security|screening).*(checkpoint|airport|passenger|lane)",
              r"(airport|passenger).*(security|screening) (checkpoint|lane)"],
        ng=[r"customs", r"border protection"],
        cat=["cat:Transportation Security Administration"]),
    "cockpit_door_hard": dict(
        must=[r"(cockpit|flight deck) door"],
        ng=[r"douglas m-2", r"193[0-9]", r"museum"],
        cat=["cat:Cockpit doors"]),
    "artcc_now": dict(
        must=[r"air (route )?traffic control.*(center|centre|room|position|console)",
              r"(controller|operator).*(console|position|radar)"],
        ng=[r"tower cab", r"carrier"],
        cat=["cat:Air traffic control centers in the United States"]),
    "lobby_now": dict(
        must=[r"(airport|terminal).*(lobby|concourse|check-?in|departure hall|hall|interior)",
              r"(lobby|concourse|check-?in|departure hall).*(airport|terminal)"],
        ng=[r"motorvej", r"viby", r"truck", r"balancer"],
        cat=["cat:Interiors of airport terminals in the United States"]),
    # ── 空 ─────────────────────────────────────────────
    "clear_sky": dict(
        must=[r"(blue sky|clear sky|cloudless)", r"sky.*(clear|blue|cloudless)"],
        ng=[r"drongo", r"\bbird\b", r"perched", r"pole", r"basketball", r"basketball", r"abandoned", r"building", r"garden", r"telescope",
            r"\balma\b"],
        cat=["cat:Blue skies"]),
}


# 🔴 図に振り替えた4欄（その建物そのものの写真が Commons に無い。⑤b-1 §4）。
#    **網を書かないのが正しい状態**なので、取りこぼしの検算から外す。
FIG_SLOTS = {"boston_artcc_ext", "indy_artcc", "cleveland_artcc", "atcscc"}

# ══════════════════════════════════════════════════════════
#  🔴 4周目に歩く分類（**実在する名前**）
# ══════════════════════════════════════════════════════════
# ⚠️ 上の `cat=` は推測で書いたもので、**15欄中6欄が「0点」＝分類そのものが無かった**。
#    （例：`World Trade Center (1973-2001)` は実在せず、正しくは **1970–2001・ダッシュはエヌ**）
#    分類名は `list=search&srnamespace=14` で引いて実在を確かめてある（`qa_out/_cats*.txt`）。
#    🔴 **「0点」を「素材が無い」と読まない**（[[feedback-absence-of-a-word-is-not-absence]]）。
WTC = "cat:World Trade Center (1970–2001)"
ACC = "cat:Area control center"
CAT = {
    "manhattan_pre": [WTC, "cat:World Trade Center (New York City)"],
    "commute_pre": ["cat:Pedestrians in Manhattan, New York City",
                    "cat:New York City Subway in the 1990s"],
    "wtc_far": [WTC], "wtc_twin": [WTC], "wtc_base": [WTC],
    "wtc_south": ["cat:Two World Trade Center (South Tower)", WTC],
    "wtc_under": ["cat:World Trade Center (PATH station)", WTC],
    "lobby_pre": ["cat:Airport terminals in the United States", "cat:Airport check-ins"],
    "security_pre": ["cat:Aviation security"],
    "gate_pre": ["cat:Airport gates", "cat:Jet bridges"],
    "fids_pre": ["cat:Flight information displays", "cat:Flight departure boards"],
    "logan": ["cat:Logan International Airport"],
    "logan_apron": ["cat:Logan International Airport"],
    "logan_takeoff": ["cat:Logan International Airport"],
    "dulles": ["cat:Washington Dulles International Airport"],
    "dulles_rwy": ["cat:Washington Dulles International Airport"],
    "reagan": ["cat:Ronald Reagan Washington National Airport"],
    "newark_757": ["cat:Boeing 757 at Newark Liberty International Airport",
                   "cat:Newark Liberty International Airport"],
    "b767": ["cat:Boeing 767"], "b757": ["cat:Boeing 757"],
    "b767_cruise": ["cat:Boeing 767 in flight"],
    "b767_takeoff": ["cat:Boeing 767"], "b757_takeoff": ["cat:Boeing 757"],
    "airliner_cruise": ["cat:Airliners in flight"],
    "refuel": ["airliner refuelling apron", "aircraft fuel truck airport"],
    "cabin_pre": ["cat:Aircraft cabins by decade", "cat:Aircraft cabins"],
    "cockpit_door_pre": ["cat:Aircraft cockpits"],
    "cabin_phone": ["seatback telephone aircraft", "Airfone seat telephone"],
    "cockpit_pre": ["cat:Aircraft cockpits"],
    "window_cruise": ["cat:Views from aircraft by country"],
    "window_sky": ["cat:Views from aircraft by country"],
    "artcc_screen_pre": [ACC, "cat:Radar screen display types"],
    "radar_scope_pre": ["cat:Radar screen display types", ACC],
    "controller_pre": ["cat:Air traffic controllers"],
    "artcc_screen2": [ACC], "artcc_alt": [ACC],
    "artcc_seat": [ACC, "cat:Air traffic controllers"],
    "aoc_pre": ["airline operations control center", "airline dispatch center"],
    "pentagon_ext_pre": ["cat:The Pentagon"],
    "pentagon_aerial_pre": ["cat:Aerial photographs of the Pentagon"],
    "pentagon_court_pre": ["cat:The Pentagon"],
    "pentagon_west_day": ["cat:September 11 attacks at the Pentagon",
                          "cat:Aerial photographs of the Pentagon damaged by the "
                          "September 11 attacks"],
    "f15_alert": ["cat:Otis Air National Guard Base", "cat:F-15 Eagle"],
    "f15_takeoff": ["cat:F-15 Eagle"],
    "f16_alert": ["cat:Langley Air Force Base", "cat:F-16 Fighting Falcon"],
    "f16_takeoff": ["cat:F-16 Fighting Falcon"],
    "base_rwy": ["cat:Runways in the United States"],
    "fighter_dc": ["cat:Military aircraft in flight over Washington, D.C."],
    "andrews": ["cat:Joint Base Andrews"],
    "wtc_smoke_day": ["cat:September 11 attacks"],
    "fire_trucks_day": ["cat:September 11 attacks"],
    "shanksville_day": ["cat:United Airlines Flight 93"],
    "apron_day": ["cat:Operation Yellow Ribbon", "cat:Gander International Airport"],
    "apron_lined_day": ["cat:Operation Yellow Ribbon", "cat:Gander International Airport"],
    "stopped_day": ["cat:Operation Yellow Ribbon", "cat:Gander International Airport"],
    "stranded_day": ["cat:Operation Yellow Ribbon"],
    "report_cover": ["cat:9/11 Commission Report", "cat:9/11 Commission"],
    "report_page": ["cat:9/11 Commission Report"],
    "hearing": ["cat:9/11 Commission", "cat:United States congressional hearings"],
    "library_reports": ["cat:Library bookshelves", "cat:Books on shelves"],
    "nist_report": ["cat:National Institute of Standards and Technology NCSTAR"],
    "recorder": ["cat:Flight data recorders", "cat:Cockpit voice recorders"],
    "atc_tape": ["cat:Reel to reel tape recorders"],
    "logbook": ["cat:Logbooks"],
    "security_now": ["cat:Transportation Security Administration"],
    "cockpit_door_hard": ["cat:Aircraft cockpits"],
    "artcc_now": [ACC],
    "lobby_now": ["cat:Airport terminals in the United States", "cat:Airport check-ins"],
    "clear_sky": ["cat:Skies"],
}


def hay_of(row, wide=True):
    """当てる藁。

    🔴🔴 2026-09-13（⑤b-2・2回目の直し）**MUST は題名だけで当てる。**
      1回目は題名＋説明＋撮影者＋物件名を1本にしていたので、**説明の中の語で誤当たり**した。
      自動で選ばせた65欄を1行ずつ見て実際に出ていたもの：

        apron_day（当日の駐機場）   → **1985年 Arrow Air 墜落機の残骸**（説明に "Gander Airport"）
        wtc_smoke_day（北棟の煙）   → **2001年8月の無傷のツインタワー**（説明に "September 11"）
        controller_pre（管制官）    → **PATCO ストのローズガーデン会見**（説明に "air traffic controllers"）
        radar_scope_pre（管制卓）   → **強襲揚陸艦 USS Nassau の戦闘指揮所**
        clear_sky（よく晴れた空）   → **青空を背にした鳥**（説明に "clear blue sky"）
        refuel（給油中の旅客機）    → **B-1B 爆撃機**

      ＝ 説明文は「その語が出てくる」だけで、**写っているもの**とは限らない。
      → **MUST は `title`（＋物件名）だけ**に当てる。NG は説明も見る（落とす側は広くてよい）。
      ⚠️ 取りこぼしは増えるが、**間違った絵を選ぶより取りこぼすほうが安い**
         （[[feedback-subtitle-must-match-what-is-visible]]）。
    """
    keys = ("title", "desc", "objname", "credit") if wide else ("title", "objname")
    return " ".join(str(row.get(k) or "") for k in keys).lower()


def verdict(slot_name, row):
    """(通ったか, 理由) を返す。理由は落ちたときだけ意味がある。"""
    r = SLOT_RULES.get(slot_name)
    if not r:
        return None, "網が無い"
    for pat in r.get("ng", []) + NG_ALL:
        if re.search(pat, hay_of(row, wide=True)):
            return False, f"NG:{pat}"
    title = hay_of(row, wide=False)
    for pat in r["must"]:
        if re.search(pat, title):
            return True, pat
    return False, "題名に MUST が1つも当たらない"


def _db():
    if not A.OUT.exists():
        print("🔴 台帳が無い"); sys.exit(2)
    return json.loads(A.OUT.read_text(encoding="utf-8"))


def cmd_audit():
    """🔴 欄ごとに「権利・幅・年」を通った数と「**中身も合う**」数を並べる。"""
    db = _db()
    print(f"{'欄':24}{'網を通った':>10}{'中身も合う':>10}{'うち時点も':>10}  中身")
    bad = []
    for s in A.SLOTS:
        d = db.get(s["name"]) or dict(rows=[])
        rows = d.get("rows", [])
        ok = [r for r in rows if verdict(s["name"], r)[0]]
        era = [r for r in ok if r.get("era_ok") is not False]
        fig = s["name"] in FIG_SLOTS
        mark = "図" if fig else ("🔴" if not ok else ("⚠️" if not era else "  "))
        if not era and not fig:
            bad.append(s["name"])
        print(f"{mark}{s['name']:22}{len(rows):>10}{len(ok):>10}{len(era):>10}  {s['want']}")
    print(f"\n■ 欄 {len(A.SLOTS)} ／ **中身も時点も合う候補が0の欄 {len(bad)}**")
    if bad:
        print("   " + " ".join(bad))
    return 2 if bad else 0


def cmd_rank(only=None, n=6, show_ng=False):
    db = _db()
    for s in A.SLOTS:
        if only and s["name"] not in only:
            continue
        d = db.get(s["name"]) or dict(rows=[])
        print(f"\n■ {s['name']}  ({s['era']})  {s['want']}  → {','.join(s['cuts'])}")
        shown = 0
        for r in d.get("rows", []):
            ok, why = verdict(s["name"], r)
            if not ok and not show_ng:
                continue
            e = {True: "✓", False: "🔴年", None: "?年"}[r.get("era_ok")]
            flag = "  " if ok else "✗ "
            print(f"   {flag}{e} {r['w']}x{r['h']} {r['lic_kind']:6} {str(r.get('year')):>5} "
                  f"{r['title'][5:88]}")
            if ok and r.get("desc"):
                print(f"       説明 {r['desc'][:110]}")
            if not ok:
                print(f"       ✗ {why}")
            shown += 1
            if shown >= n:
                break
        if not shown:
            print("   🔴 通った候補なし")
    return 0


def cmd_hunt(only=None, wmin=None):
    """4周目＝**分類を歩く**（全文検索より当たりが固い）。台帳に足す。"""
    wmin = wmin or A.W_MIN
    db = json.loads(A.OUT.read_text(encoding="utf-8")) if A.OUT.exists() else {}
    slots = [s for s in A.SLOTS
             if (not only or s["name"] in only) and s["name"] in CAT]
    print(f"■ {len(slots)}欄を分類から探します（幅>={wmin}）")
    for s in slots:
        titles = []
        for q in CAT[s["name"]]:
            try:
                if q.startswith("cat:"):
                    got, _ = CP.cat_files(q[4:], depth=2, limit=600)
                    titles += got
                else:
                    titles += CP.search_files(q, limit=80)
            except Exception as e:                              # noqa: BLE001
                print(f"  🔴 {s['name']}: 検索が落ちた（{q}）: {e}")
        titles = [t for t in dict.fromkeys(titles)
                  if re.search(r"\.(jpe?g|png|tiff?)$", t, re.I)]
        rows = A._imageinfo2(titles) if titles else []
        keep, why = A._keep(s, rows, wmin)
        # 🔴 **ここで中身の網も当てる**（権利・幅だけの点を台帳に積み増さない）
        fit = [r for r in keep if verdict(s["name"], r)[0]]
        d = db.setdefault(s["name"], dict(want=s["want"], era=s["era"],
                                          cuts=s["cuts"], tried=0, kept=0, rows=[]))
        have = {r["title"] for r in d["rows"]}
        add = [r for r in fit if r["title"] not in have]
        d["rows"] = sorted(d["rows"] + add,
                           key=lambda r: (verdict(s["name"], r)[0] is not True,
                                          r.get("era_ok") is not True,
                                          r.get("era_ok") is False,
                                          -(r["w"] * r["h"])))[:40]
        d["tried"] += len(titles)
        d["kept"] = len(d["rows"])
        print(f"  {s['name']:22} 分類 {len(titles):4}点 → 権利と幅 {len(keep):3}"
              f" → **中身も合う {len(fit):3}**（足した {len(add):2}）"
              f"  落ちた内訳 小{why['small']} 2値{why['bit']} 権利{why['lic']}")
        A.OUT.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(0.2)
    print(f"\n台帳 → {A.OUT}")
    return 0


def selftest():
    """🔴 物差しの検算。**陽性・陰性の対照を「値」で見る**。

    ⚠️ 「件数」だけの対照は、もともと全件該当の指標では動かない
       （[[feedback-verify-your-own-instrument]]）。ここは **1行ごとの可否**を見る。
    """
    cases = [
        # (欄, 題名, 説明, 期待)
        ("b767_cruise", "File:Bajki La Fontaine 1876 (109015449).jpg", "", False),
        ("b767_cruise", "File:ANA Boeing 767-300 JA602F in flight.jpg", "", True),
        ("b767", "File:American Airlines Boeing 757 at Punta Cana.jpg", "", False),
        ("b767", "File:Delta Boeing 767-300ER N1604R.jpg", "", True),
        ("artcc_screen_pre", "File:F-4B of VF-21 returns to USS Midway.jpg", "", False),
        ("artcc_screen_pre", "File:Air traffic control radar scope 1998.jpg", "", True),
        ("apron_day", "File:X-47A rollout.jpg", "", False),
        ("apron_day", "File:Grounded airliners at Gander during Operation Yellow Ribbon.jpg",
         "", True),
        # 🔴🔴 いちばん危ない型：**当日の欄に「事故の前」の絵**が年で通ってしまう
        ("wtc_smoke_day",
         "File:LOC Lower Manhattan New York City World Trade Center August 2001.jpg", "",
         False),
        ("wtc_smoke_day", "File:North Tower of the World Trade Center burning.jpg", "", True),
        ("wtc_twin", "File:1993 World Trade Center bombing timeline of perpetrators.png",
         "", False),
        ("wtc_twin", "File:World Trade Center twin towers from the Hudson 1999.jpg", "", True),
        ("logan", "File:Wildlife Inspector in Seattle dons protective gear.jpg", "", False),
        ("logan", "File:Logan International Airport terminal 1998.jpg", "", True),
        ("lobby_now", "File:BC82273 (18.05.02, Motorvej 501, Viby J).jpg", "", False),
        ("lobby_now", "File:Departure hall of the airport terminal 2019.jpg", "", True),
    ]
    ok = fail = 0
    print("■ 対照（1行ごとの可否を値で見る）")
    for slot, title, desc, want in cases:
        got, why = verdict(slot, dict(title=title, desc=desc))
        good = got is want
        ok, fail = (ok + 1, fail) if good else (ok, fail + 1)
        print(f"  {'✓' if good else '🔴'} {slot:18} 期待 {str(want):5} 実測 {str(got):5} "
              f"({why[:34]})  {title[5:64]}")
    # 🔴 網そのものの取りこぼし：欄の数と網の数が合っているか
    miss = [s["name"] for s in A.SLOTS
            if s["name"] not in SLOT_RULES and s["name"] not in FIG_SLOTS]
    print(f"\n■ 網が無い欄 {len(miss)}: {' '.join(miss) if miss else '（無し）'}")
    print(f"■ 対照 {ok}/{len(cases)} 通過")
    return 0 if (fail == 0 and not miss) else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", nargs="?", default="audit",
                    choices=["audit", "rank", "hunt"])
    ap.add_argument("--only", default="")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--ng", action="store_true", help="落ちた候補も理由つきで出す")
    ap.add_argument("--w", type=int, default=0)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    only = set(x for x in a.only.split(",") if x) or None
    if a.cmd == "audit":
        return cmd_audit()
    if a.cmd == "rank":
        return cmd_rank(only, a.n, a.ng)
    return cmd_hunt(only, a.w or None)


if __name__ == "__main__":
    sys.exit(main())
