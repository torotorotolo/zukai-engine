# -*- coding: utf-8 -*-
"""32本目 ⑤b-3b：地図の門番（check_sat・satmap.check）が32本目の地図（飛んだ道の線・向きの矢印・札の数・×）で鳴るかの陽性対照。
  python -P ref/ep32/eizou_build/helpers/satpc32.py   # 陰性1＋陽性9。⚠️ 32本目の SPEC を読む＝回を替えたら見本の側で
31本目の `satpc31.py` の型（壊した SPEC の写しを門番に通し、狙った文で鳴るか）。
⚠️ 「帰属の行に重なる」は札の箱を画面の画素で計算してから試す（額 (384, 210, 1152, 648)・帰属の行の箱 (984, 838)〜(1536, 858)）
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


def el(s, cid, i, j):
    return s[cid]["sat"]["steps"][i][j]


b0 = M.check(base)[0] + C.num_check(base)
print(("✓" if not b0 else "🔴"), "陰性：32本目の地図", len(base), "カット", len(b0), "件")
ok &= not b0
s = copy.deepcopy(base)
el(s, "c317", 0, 2)["t"] = "約950メートル"
case("高さの札の数を替える（950）", C.num_check(s), "REC_SAT_NUM に無い")
rec = copy.deepcopy(C.REC_SAT_NUM)
rec["c317"]["約930メートル"] = (("抜き書き p64", "highest altitude of about 3,160 feet"),)
case("記録の句を原文に無い句に", C.num_check(base, rec) if C._rec_page("抜き書き p64") is not None else ["（原文が手元に無い）抜き書き p64 に無い"], "抜き書き p64 に無い")
s = copy.deepcopy(base)
el(s, "c406", 0, 0)["t"] = "滑走路30"
case("滑走路の番号を替える（30）", C.num_check(s), "REC_SAT_NUM に無い")
s = copy.deepcopy(base)
el(s, "c902", 1, 0)["k"] = "x"
case("×を一般の座標の点（フェリー乗り場）に", M.check(s)[0], "×は報告書の座標の場所だけ")
s = copy.deepcopy(base)
el(s, "c401", 1, 0).pop("dir")
case("座標が尾の矢印から dir を外す", M.check(s)[0], "矢印の尾が場所の名でない")
s = copy.deepcopy(base)
s["c902"]["sat"]["note"] = "×は報告書の座標"
case("一般の座標の断りを消す", M.check(s)[0], "一般の座標")
s = copy.deepcopy(base)
el(s, "c109", 0, 0)["path"] = tuple(list(el(s, "c109", 0, 0)["path"]) + [(40.80, -74.40)])
case("線を額のはっきり外の点まで伸ばす", M.check(s)[0], "額の内側")
s = copy.deepcopy(base)
el(s, "c902", 0, 0)["lab"] = (300, 262, "start")   # ⚠️ 最初の (360, 205) は札の箱 y 752〜790＝帰属の行の箱 y 838〜858 の上＝試し方の誤りで鳴らなかった
case("札を右下の帰属の行の上へ", M.check(s)[0], "attrib の箱")
s = copy.deepcopy(base)
el(s, "c501", 0, 1)["at"] = "jfk"
case("表に無い場所に点", M.check(s)[0], "GEO に無い")
print("■ 32本目の陽性対照", "合格" if ok else "🔴 不合格")
sys.exit(0 if ok else 1)
