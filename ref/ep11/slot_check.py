# -*- coding: utf-8 -*-
"""台本が要求している「実写の欄」を数え、②の在庫と突き合わせる。

🔴 記憶 feedback-inventory-is-not-usable-material＝候補N点は在庫ではない。
   ④の時点で「何枚要るか」を出しておかないと、⑤bで足りないことに気づく。
"""
import collections
import re
import sys

PATH = ("C:/Users/konar/Documents/Obsidian Vault/Projects/"
        "事故検証-チャレンジャー号-台本第1版-20260921.md")

# ②の実測（ref/ep11/materials.md §2）。欄名 → 候補点数
STOCK = {
    "mcauliffe": 51, "training": 44, "debris": 23, "memorial": 17, "crew": 12,
    "accident": 10, "recovery": 8, "srb": 8, "commission": 7, "launch": 5,
    "pad": 2, "ice": 3, "mcc": 1, "smoke": 1, "reagan": 6,
}
# 台本のスロット名 → ②の欄（どの欄から引くか）
MAP = {
    "ice_icicle": "ice", "ice_pad": "ice", "ice_trough": "ice", "ice_icicle_2": "ice",
    "ice_egress": "ice", "ice_box": "ice", "ice_team": "ice",
    "launch_liftoff": "launch", "launch_pad_morning": "launch", "past_launch": "launch",
    "launch_51c": "launch", "pad_39b": "pad", "rockwell_orbiter": "pad",
    "accident_breakup": "accident", "fireball": "accident", "fireball_wide": "accident",
    "breakup_sections": "accident", "breakup_moment": "accident", "srb_trails": "accident",
    "srb_destruct": "accident", "hydrogen_burn": "accident", "et_breach": "accident",
    "smoke_liftoff": "smoke", "smoke_puffs": "smoke",
    "ascent_1": "launch", "ascent_2": "launch", "flame_plume": "accident",
    "flame_plume_2": "accident", "ssme_ignition": "launch",
    "crew_portrait": "crew", "crew_portrait_2": "crew", "crew_portrait_3": "crew",
    "crew_scobee": "crew", "crew_smith": "crew", "crew_onizuka": "crew",
    "crew_resnik": "crew", "crew_mcnair": "crew", "crew_jarvis": "crew",
    "crew_breakfast": "crew", "crew_whiteroom": "crew",
    "mcauliffe_class": "mcauliffe", "mcauliffe_training": "mcauliffe",
    "mcauliffe_morgan": "mcauliffe", "training_zero_g": "training",
    "srb_oring": "srb", "srb_stack": "srb", "srb_field_joint": "srb",
    "oring_physical": "srb", "joint_test": "srb", "oring_resilience_test": "srb",
    "srb_sun_shade": "srb", "oring_channel": "srb", "joint_qual_test": "srb",
    "srm_horizontal": "srb", "joint_redesign": "srb", "joint_test_new": "srb",
    "srm_vertical_test": "srb",
    "oring_soot": "debris", "oring_erosion_photo": "debris", "oring_erosion": "debris",
    "srm_nozzle_51b": "debris", "srb_burn_hole": "debris", "srb_burn_hole_2": "debris",
    "srb_inside": "debris", "rudder_burn": "debris", "frustum_compare": "debris",
    "debris_hangar": "debris", "debris_et": "debris", "mads_tape": "debris",
    "recovery_ship": "recovery",
    "commission_hearing": "commission", "commission_members": "commission",
    "commission_testimony": "commission", "commission_hearing_2": "commission",
    "mulloy_testimony": "commission", "commission_room": "commission",
    "commission_report": "commission", "commission_oversight": "commission",
    "oring_data_chart": "commission", "safety_panel": "commission",
    "astronaut_manager": "commission",
    "memorial_service": "memorial", "flag_half_mast": "memorial",
    "memorial_wreath": "memorial", "reagan_address": "reagan",
    "mmt_meeting": "mcc", "marshall_center": "pad", "thiokol_plant": "pad",
    "nasa_hq": "pad", "telecon_room": "mcc", "thiokol_telefax": "commission",
}
CUT = re.compile(r'^\*\*([a-z]{1,2}\d{2,3})\*\*\s*／\s*実写\s+([A-Za-z0-9_]+)')


def main():
    on = False
    used = collections.Counter()
    where = collections.defaultdict(list)
    unknown = []
    for raw in open(PATH, encoding="utf-8"):
        line = raw.rstrip()
        if line.startswith("## 4. 台本"):
            on = True
            continue
        if on and re.match(r'^## \d', line):
            break
        if not on:
            continue
        m = CUT.match(line)
        if not m:
            continue
        cid, slot = m.group(1), m.group(2)
        col = MAP.get(slot)
        if col is None:
            unknown.append((cid, slot))
            continue
        used[col] += 1
        where[col].append(slot)

    print("== 台本が要求する枚数 vs ②の候補（同じ欄から引くもの）")
    print("  %-12s %5s %5s  %s" % ("欄", "要求", "候補", "判定"))
    short = 0
    for col in sorted(STOCK, key=lambda k: -used[k]):
        need, have = used[col], STOCK[col]
        if need == 0:
            continue
        ok = "OK" if need <= have else "🔴 不足 %d" % (need - have)
        short += max(0, need - have)
        print("  %-12s %5d %5d  %s" % (col, need, have, ok))
        if need > have:
            print("        使っている名前: %s" % "、".join(sorted(set(where[col]))))
    print("\n  合計 要求 %d / 候補 %d / 🔴 不足の合計 %d"
          % (sum(used.values()), sum(STOCK[c] for c in used), short))
    if unknown:
        print("\n== ⚠️ ②の欄に無いスロット（⑤bで当て直しが要る）")
        for cid, s in unknown:
            print("  %s %s" % (cid, s))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
