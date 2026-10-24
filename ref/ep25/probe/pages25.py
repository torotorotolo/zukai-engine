# -*- coding: utf-8 -*-
"""25本目②：頁の文字をそのまま（改行を詰めて）書き出す。節を通しで読むため・付図の文字の層を見るため。
使い方: python pages25.py <src> <出力> <名前>:<印刷頁 a-b | p1,p2,…> ...   （名前:find:<語> で、その語を含む頁を全部）"""
import json, os, re, sys, unicodedata


def main():
    src, out = sys.argv[1], sys.argv[2]
    lines = []
    for spec in sys.argv[3:]:
        name, sel = spec.split(":", 1)
        doc = json.load(open(os.path.join(src, "txt", name + ".json"), encoding="utf-8"))
        if sel.startswith("find:"):
            w = re.sub(r"\s+", "", unicodedata.normalize("NFKC", sel[5:]))
            want = [d for d in doc if w in d["norm"]]
        else:
            if "-" in sel:
                a, b = (int(x) for x in sel.split("-"))
                rng = set(range(a, b + 1))
            else:
                rng = {int(x) for x in sel.split(",")}
            want = [d for d in doc if (d["printed"] if d["printed"] is not None else d["pdf"]) in rng]
        for d in want:
            t = unicodedata.normalize("NFKC", d["raw"])
            t = re.sub(r"[ \t　]+", " ", t)
            t = re.sub(r"\n\s*\n+", "\n", t)
            lines.append(f"===== {name} p{d['printed']} (PDF{d['pdf']}) garble={d['garble']} images={d['images']}")
            lines.append(t.strip())
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("done", len(lines) // 2)


if __name__ == "__main__":
    main()
