# -*- coding: utf-8 -*-
"""ep7_refetch.py — ⑤c' で**差し替える12欄**の素材を探し直す（2026-09-14 新設）。

■ なぜ要るか
    ⑤c-2 の原寸検品で **15欄・12種**が「名乗っているものと写っているものが違う」と分かった
    （台帳 `qa_out/ep7_qa_look2.md` §A）。既存の候補の帳（`assets_cand.json`）を見ると、
    12欄のうち3欄は**候補40点が全部同じ粗**だった（security_now は40点すべてが
    長官の記者会見・cabin_phone は38点に電話が1台も無い・apron_day は 2001年の該当なし）。
    ＝ [[feedback-inventory-is-not-usable-material]]「権利・幅・年しか見ていない網は別物を1位に出す」。

■ 何をするか
    欄ごとに**当てる語を作り直して**もう一度探し、題名と説明を人が読める形で出す。
    網（幅1920・bitdepth>=8・PD/CC BY）は `ep7_assets` のものをそのまま使う。

■ 使い方
    python qa_out/ep7_refetch.py search            # 探して帳に足す
    python qa_out/ep7_refetch.py search --only=f16_alert
    python qa_out/ep7_refetch.py report            # 帳から題名＋説明を出す（選ぶための表）
    python qa_out/ep7_refetch.py --selftest

■ 🔴 守っていること
    出力はファイルへ。`| tail` でつながない（[[feedback-pipes-mask-exit-codes]]）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.path.insert(0, str(HERE / "qa_out"))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import commons_probe as CP                                      # noqa: E402
import ep7_assets as A                                          # noqa: E402

OUT = HERE / "analytics" / "materials" / "ep7" / "refetch_cand.json"

# ══════════════════════════════════════════════════════════
#  当てる語（⑤c-2 の所見から作り直した）
# ══════════════════════════════════════════════════════════
# 🔴 いままでの語が何を釣ってしまったかを各欄に書く。同じ轍を踏まないため。
QUERIES: dict[str, list[str]] = {
    # pr10 ＝「降ろされた旅客機 2001年9月11日」。前回は Alaska の 737 MAX（2024年）
    #   9/11 当日に降ろされた機体の写真は、カナダの Operation Yellow Ribbon が本命
    "apron_day": [
        "Operation Yellow Ribbon",
        "Gander International Airport September 2001",
        "Halifax Stanfield International Airport September 2001",
        "grounded airliners September 11 2001",
        "cat:Operation Yellow Ribbon",
        "cat:Aviation in the aftermath of the September 11 attacks",
    ],
    # c901 c902 ＝「今の空港の保安検査場」。前回は長官3人の広報写真
    #   → 人が主役でない検査場そのもの。TSA の装置・列・レーンで当てる
    "security_now": [
        "TSA checkpoint lane passengers screening",
        "airport security checkpoint queue passengers",
        "advanced imaging technology scanner airport",
        "cat:Airport security checkpoints in the United States",
        "cat:Transportation Security Administration",
    ],
    # c309 c614 ＝「客室の座席にある電話」。前回は A220 の現代の客室（電話ゼロ）
    "cabin_phone": [
        "Airfone",
        "seatback telephone aircraft",
        "in-flight telephone handset seat",
        "cat:Airfone",
        "cat:In-flight telephones",
    ],
    # c412 ＝「ペンタゴンの中庭」。前回はマスクの制服2人（2020年）
    "pentagon_court_pre": [
        "Pentagon center courtyard",
        "Pentagon courtyard aerial",
        "Ground Zero Cafe Pentagon",
        "cat:Pentagon Center Courtyard",
    ],
    # c622 c623 ＝「墜落現場（何も無い野原）」。前回は防護服の手元の寄り
    "shanksville_day": [
        "Flight 93 crash site aerial Shanksville",
        "United Flight 93 crater field Pennsylvania",
        "Flight 93 National Memorial field",
        "cat:United Airlines Flight 93 crash site",
    ],
    # c707 ＝「待機するF-16」。前回は隊員1人（F-16 なし）
    "f16_alert": [
        "F-16 parked flightline",
        "F-16 Fighting Falcon on the ramp",
        "F-16 alert hangar",
        "cat:Static aircraft of General Dynamics F-16 Fighting Falcon",
    ],
    # c711 ＝「離陸するF-16」。前回は有刺鉄線が全面
    "f16_takeoff": [
        "F-16 takeoff afterburner runway",
        "F-16 Fighting Falcon departs runway",
        "F-16 rotate takeoff",
        "cat:General Dynamics F-16 Fighting Falcon in flight",
    ],
    # c717 ＝「首都上空を飛ぶ戦闘機」。前回はほぼ無地の灰色
    "fighter_dc": [
        "Operation Noble Eagle fighter patrol",
        "F-16 over Washington DC flyover",
        "F-15 Eagle in flight banking",
        "cat:Operation Noble Eagle",
    ],
    # pr09 ＝「航空路管制センターの画面 2001年ごろ」。前回は現代の事務室（AFCENT）
    "artcc_screen_pre": [
        "air route traffic control center radar scope",
        "FAA en route control center controllers",
        "ARTCC radar display controller",
        "cat:Air traffic control centers in the United States",
        "cat:Air traffic control radar displays",
    ],
    # c302 ＝「離陸するボーイング767」。前回は FedEx の貨物機・しかも巡航中
    "b767_takeoff": [
        "Boeing 767 takeoff rotation runway",
        "United Airlines Boeing 767 takeoff",
        "American Airlines Boeing 767 departure",
        "cat:Boeing 767 taking off",
    ],
    # c809 ＝「航空の記録簿」。前回はロシア語のグライダー耐空記録簿
    "logbook": [
        "pilot logbook page handwritten",
        "aircraft flight log book page",
        "military duty log sheet",
        "cat:Logbooks",
    ],
    # c320 ＝「空港の出発案内板」。前回はジュネーブ（欧州）の板
    "fids_pre": [
        "flight information display board airport departures United States",
        "Solari board airport departures",
        "airport departure board split flap",
        "cat:Flight information display systems",
    ],
}


# ══════════════════════════════════════════════════════════
#  2周目の語（1周目で在庫が空だった5欄）
# ══════════════════════════════════════════════════════════
# 🔴 1周目で分かったこと＝**「その出来事そのもの」を当てにいくと空になる**。
#   9/11 当日に降ろされた機体・墜落現場の野原・電話つきの座席は、
#   自由に使える写真が1点も無い。→ **画が支えられる言い方に寄せて探す**
#   （副題からは年と主題の主張を落とし、実際に写っているものを書く）。
QUERIES2: dict[str, list[str]] = {
    # pr10 ＝ 出来事でなく「並んで駐まっている旅客機」で当てる
    "apron_day": [
        "airliners parked at terminal gates row",
        "airport ramp parked aircraft lineup",
        "cat:Aircraft at airport gates",
        "cat:Aprons (airport)",
    ],
    # c901 c902 ＝ 人でなく「検査場の装置と列」で当てる
    "security_now": [
        "cat:Airport security",
        "airport security screening line travelers",
        "millimeter wave body scanner airport passenger",
        "x-ray baggage screening belt airport",
    ],
    # c622 c623 ＝ 「野原・丘・記念碑の原野」で当てる
    "shanksville_day": [
        "Shanksville Pennsylvania",
        "cat:Shanksville, Pennsylvania",
        "cat:Flight 93 National Memorial",
        "Somerset County Pennsylvania field meadow",
    ],
    # c412 ＝ 中庭が写る俯瞰
    "pentagon_court_pre": [
        "cat:Aerial photographs of The Pentagon",
        "Pentagon aerial view courtyard",
    ],
    # c309 ＝ 電話は無いので「ボーイング767の客室」で当てる（c614 と別の絵にする）
    "cabin_phone": [
        "Boeing 767 cabin interior seats",
        "cat:Aircraft cabin interiors",
        "wide-body airliner cabin economy seats",
    ],
}


def _slot(name):
    return next(s for s in A.SLOTS if s["name"] == name)


def cmd_search(only=None, limit=60, rnd=1):
    db = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    tbl = QUERIES2 if rnd == 2 else QUERIES
    names = [n for n in tbl if not only or n in only]
    print(f"■ {len(names)}欄を探し直します（{rnd}周目・幅>={A.W_MIN}"
          f"・bitdepth>={A.BD_MIN}・PD/CC BY）")
    for name in names:
        s = _slot(name)
        titles = []
        for q in tbl[name]:
            try:
                if q.startswith("cat:"):
                    got, _ = CP.cat_files(q[4:], depth=2, limit=400)
                    titles += got
                else:
                    titles += CP.search_files(q, limit=limit)
            except Exception as e:                              # noqa: BLE001
                print(f"  🔴 {name}: 検索が落ちた（{q}）: {e}")
        titles = [t for t in dict.fromkeys(titles)
                  if re.search(r"\.(jpe?g|png|tiff?)$", t, re.I)]
        rows = A._imageinfo2(titles) if titles else []
        keep, why = A._keep(s, rows, A.W_MIN)
        key = name if rnd == 1 else f"{name}#2"
        db[key] = dict(want=s["want"], era=s["era"], cuts=s["cuts"],
                       tried=len(titles), kept=len(keep), rows=keep[:40])
        print(f"  {name:20} 候補 {len(titles):4}点 → 通った {len(keep):3}点"
              f"（時点が合う {sum(1 for r in keep if r.get('era_ok') is True):3}点）"
              f"  落ちた 小{why['small']} 2値{why['bit']} 権利{why['lic']}")
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
        time.sleep(0.2)
    print(f"\n帳 → {OUT}")
    return 0


def cmd_report(only=None, n=14):
    db = json.loads(OUT.read_text(encoding="utf-8"))
    for name, d in db.items():
        if only and name not in only:
            continue
        print(f"\n### {name}  want={d['want']}  era={d['era']}  "
              f"cuts={d['cuts']}  通った={d['kept']}")
        for r in d["rows"][:n]:
            ds = re.sub(r"\s+", " ", (r.get("desc") or ""))[:150]
            print(f"  [{r.get('year')}] {r['w']}x{r['h']} {r['lic_kind']:6} {r['title'][5:][:88]}")
            if ds:
                print(f"        - {ds}")
    return 0


def selftest():
    ok = True

    def chk(what, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  🔴 ") + what)
        ok = ok and bool(cond)

    chk("12欄ぶんの語がある", len(QUERIES) == 12)
    chk("欄の名前が SLOTS に全部ある",
        all(any(s["name"] == n for s in A.SLOTS) for n in QUERIES))
    # 陽性対照＝網が「落とす」ことを数で見る（[[feedback-verify-your-own-instrument]]）
    s = _slot("logbook")
    fake = [dict(title="File:small.jpg", w=100, h=100, bitdepth=8,
                 license="Public domain", usageterms="Public domain"),
            dict(title="File:bad_lic.jpg", w=4000, h=3000, bitdepth=8,
                 license="CC BY-SA 4.0", usageterms="CC BY-SA 4.0"),
            dict(title="File:ok.jpg", w=4000, h=3000, bitdepth=8,
                 license="Public domain", usageterms="Public domain", date="2010")]
    keep, why = A._keep(s, fake, A.W_MIN)
    chk(f"陽性対照：3点中1点だけ通る（実測 {len(keep)}点・小{why['small']} 権利{why['lic']}）",
        len(keep) == 1 and why["small"] == 1 and why["lic"] == 1)
    print("  " + ("✓ selftest 通過" if ok else "🔴 selftest 失敗"))
    return 0 if ok else 1


def main():
    p = argparse.ArgumentParser()
    p.add_argument("cmd", nargs="?", default="report", choices=["search", "report"])
    p.add_argument("--only", default=None)
    p.add_argument("--round", type=int, default=1)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    only = set(a.only.split(",")) if a.only else None
    return (cmd_search(only, rnd=a.round) if a.cmd == "search"
            else cmd_report(only))


if __name__ == "__main__":
    sys.exit(main())
