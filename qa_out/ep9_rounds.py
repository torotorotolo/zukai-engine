# -*- coding: utf-8 -*-
r"""ep9_rounds.py — 9本目 ⑤a：全文起こしの1周目と2周目を突き合わせ、「2周とも崩れた行」を機械で出す（2026-09-16）。

  python qa_out/ep9_rounds.py            … 表を qa_out/ep9_rounds.txt へ（API 不使用）

■ なぜ要るか（7本目・8本目の作法）
    Scribe は**同じ音を2回起こすと結果が変わる**。1回の観測で「誤読だ」と決めると、揺れを直して別の所を壊す。
      ・2周とも崩れた（音が同じ行） → 本物の疑いが強い。直す（行頭なら取り直し／語なら A/B）
      ・片方だけ崩れた（音が同じ行） → 揺れの疑い。記録だけ（ただし数と行頭は念のため読む）
      ・**音が変わった行**（辞書が当たった行） → 2周目が新しい音の1回目の観測。A/B の「後」と合わせて2回
■ 物差し（1周目と2周目で**同じ関数**を使う。片方だけ緩めない）
    ①数＝聞取に台本の数が無い（「06分」を『六分』と読む先頭ゼロは除く＝1周目で24行すべて誤報と確かめた）
    ②el_check_heard の所見 ③el_reading_diff の「読みが違う」
⚠️ 当たり付け。最後は台本と聞取を行ごと読んで決める。
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
Q = ROOT / "audio" / "el_qa"

ROUNDS = {
    1: {"yomi": "ep9_el_yomi_round1.tsv", "flags": "ep9_heard_flags_round1.tsv", "rd": "ep9_reading_diff_round1.tsv"},
    2: {"yomi": "ep9_el_yomi.tsv", "flags": "ep9_heard_flags.tsv", "rd": "ep9_reading_diff.tsv"},
}


def load(rnd):
    import el_script as ES
    from check_numbers_heard import heard_numbers
    f = ROUNDS[rnd]
    for k in f.values():
        if not (Q / k).exists():
            raise SystemExit(f"🔴 {rnd}周目の記録が無い: {k}")
    yomi = {r["場面"]: r for r in csv.DictReader(open(Q / f["yomi"], encoding="utf-8"), delimiter="\t")}
    rd = {r["行"]: r for r in csv.DictReader(open(Q / f["rd"], encoding="utf-8"), delimiter="\t")}
    flags = {}
    for r in csv.DictReader(open(Q / f["flags"], encoding="utf-8"), delimiter="\t"):
        flags.setdefault(r["行"], []).append(f"{r['検査']}:{r['何が']}")
    out = {}
    for l in ES.lines():
        y = yomi.get(l.lid)
        if y is None:
            raise SystemExit(f"🔴 {rnd}周目に {l.lid} が無い")
        heard = y["聞こえた文"]
        want = re.findall(r"\d[\d,]*", l.text)
        # ⚠️ check_numbers_heard はカンマで数を割る（25,725 → 25 と 725）ので、正しい『二万五千七百二十五』でも鳴る。
        #    ここは台本側も聞取側もカンマを外して「数そのもの」で比べる（1周目 c103-2 の A/B 後で確かめた誤報）
        got = set(n.replace(",", "") for n in heard_numbers(re.sub(r"(?<=\d)[,，](?=\d{3})", "", heard)))
        miss = [n for n in want if n.replace(",", "") not in got and not re.fullmatch(r"0\d", n)]
        sig = []
        if miss:
            sig.append("数" + ",".join(miss))
        if rd.get(l.lid, {}).get("判定") == "読みが違う":
            sig.append("読:" + (rd[l.lid].get("食い違い") or "")[:24])
        sig += flags.get(l.lid, [])
        out[l.lid] = {"sig": sig, "heard": heard, "ratio": float(y["一致率"]), "num": bool(miss),
                      "head": any(s.startswith("頭欠け") for s in sig)}
    return out


def main():
    import el_script as ES
    r1, r2 = load(1), load(2)
    changed = {l.lid for l in ES.lines() if ES.el_text(l.text) != l.text}
    both, only1, only2, newaudio = [], [], [], []
    for l in ES.lines():
        a, b = r1[l.lid], r2[l.lid]
        row = (l, a, b)
        if l.lid in changed:
            if b["sig"]:
                newaudio.append(row)
        elif a["sig"] and b["sig"]:
            both.append(row)
        elif a["sig"]:
            only1.append(row)
        elif b["sig"]:
            only2.append(row)

    def show(title, rows, full=True):
        print(f"\n===== {title}: {len(rows)}行 =====")
        for l, a, b in rows:
            print(f"{l.lid} 1周目[{'/'.join(a['sig'])[:60]}] 2周目[{'/'.join(b['sig'])[:60]}]")
            if full:
                print(f"  台: {l.text}\n  1: {a['heard']}\n  2: {b['heard']}")

    print(f"辞書で音が変わった行 {len(changed)}（2周目が新しい音の観測）")
    show("A. 音が同じで2周とも疑い（本物の疑いが強い）", both)
    show("B. 音が変わった行で、2周目に疑い（A/B の後と合わせて2回目の観測）", newaudio)
    show("C. 音が同じで1周目だけ疑い（揺れの疑い）", only1, full=False)
    show("D. 音が同じで2周目だけ疑い（揺れの疑い）", only2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
