# -*- coding: utf-8 -*-
"""31本目 ⑤b-3b：地図の門番（check_sat・satmap.check）が31本目の新しい部品（ぼかした円 soft・帯 zone・札の数 J11L と 5海里）で鳴るかの陽性対照。
  python -P ref/ep31/eizou_build/helpers/satpc31.py   # 陰性1＋陽性7（2026-11-08 合格）。⚠️ 31本目の SPEC を読む＝回を替えたら見本の側で
⚠️ 帯のはみ出しは「額のはっきり外の点」で試す（最初に東経140.70 で試したら G08 の額の中だった＝試し方の誤りで鳴らなかった）
"""
import copy
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))
import cuts  # noqa: E402
import check_sat as C  # noqa: E402
import satmap as M  # noqa: E402

base = {c: s for c, s in cuts.SPEC.items() if s.get("sat")}
ok = True


def case(name, bad, want):
    global ok
    hit = [b for b in bad if want in b]
    print(("✓" if hit else "🔴"), name, "→", hit[0][:120] if hit else "鳴らない")
    ok &= bool(hit)


b0 = M.check(base)[0] + C.num_check(base)
print(("✓" if not b0 else "🔴"), "陰性：31本目の地図", len(base), "カット", len(b0), "件")
ok &= not b0
s = copy.deepcopy(base)
s["c408"]["sat"]["steps"][1][1]["t"] = "最高裁の推認：西側6海里の内"
case("札の数を替える（6海里）", C.num_check(s), "REC_SAT_NUM に無い")
rec = copy.deepcopy(C.REC_SAT_NUM)
rec["c408"]["最高裁の推認：西側5海里の内"] = (("抜き書き p1", "J11Lの西側六海里内"),)
case("記録の句を原文に無い句に", C.num_check(base, rec) if C._rec_page("抜き書き p1") is not None else ["（原文が手元に無い）抜き書き p1 に無い"], "抜き書き p1 に無い")
s = copy.deepcopy(base)
s["c206"]["sat"]["steps"][0][0]["t"] = "J11X"
case("J11L の札を替える", C.num_check(s), "REC_SAT_NUM に無い")
s = copy.deepcopy(base)
s["c408"]["sat"]["steps"][1][0]["path"] = tuple(list(s["c408"]["sat"]["steps"][1][0]["path"]) + [(39.69, 140.20)])
case("帯を額の外の点まで広げる", M.check(s)[0], "額の内側")
s = copy.deepcopy(base)
s["c105"]["sat"]["steps"][2][0]["r"] = 400
case("ぼかした円を額からはみ出させる", M.check(s)[0], "額の内側")
s = copy.deepcopy(base)
s["c308"]["sat"]["steps"][0][3]["at"] = "nowhere"
case("円の真ん中を表に無い場所に", M.check(s)[0], "GEO に無い")
s = copy.deepcopy(base)
s["c201"]["sat"]["note"] = "線は点を結んだ概略"
case("一般の座標の断りを消す", M.check(s)[0], "一般の座標")
print("■ 31本目の陽性対照", "合格" if ok else "🔴 不合格")
sys.exit(0 if ok else 1)
