# -*- coding: utf-8 -*-
"""25本目②：頁の文字（txt/<名前>.json）を語で探し、印刷頁と前後の字を出す。HTML も字にして探す。
使い方: python grep25.py <src> <出力> <名前>:<語>[:<前後の字数>[:<印刷頁の範囲 a-b>]] ...
  例: RA07-3-1-1:急い  RA07-3-1-1:低いもの:120:222-222  html:jrw/outline.html:106名"""
import html as H, json, os, re, sys, unicodedata


def norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


def html_text(p):
    b = open(p, "rb").read()
    for enc in ("utf-8", "cp932", "euc-jp"):
        try:
            t = b.decode(enc)
            break
        except Exception:
            continue
    else:
        t = b.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return [{"pdf": 1, "printed": 1, "norm": norm(H.unescape(t))}]


def main():
    src, out = sys.argv[1], sys.argv[2]
    lines = []
    for spec in sys.argv[3:]:
        if spec.startswith("html:"):
            _, rel, rest = spec.split(":", 2)
            parts = rest.split(":")
            doc = html_text(os.path.join(src, rel))
            name = rel
        else:
            name, *parts = spec.split(":")
            doc = json.load(open(os.path.join(src, "txt", name + ".json"), encoding="utf-8"))
        word = parts[0]
        ctx = int(parts[1]) if len(parts) > 1 and parts[1] else 60
        lo, hi = -999, 9999
        if len(parts) > 2 and parts[2]:
            lo, hi = (int(x) for x in parts[2].split("-"))
        nw = norm(word)
        hits = []
        for pg in doc:
            pr = pg["printed"] if pg["printed"] is not None else pg["pdf"]
            if not (lo <= pr <= hi):
                continue
            t = pg["norm"]
            for m in re.finditer(re.escape(nw), t):
                a, b = max(0, m.start() - ctx), min(len(t), m.end() + ctx)
                hits.append(f"   p{pr}(PDF{pg['pdf']}) {t[a:m.start()]}【{t[m.start():m.end()]}】{t[m.end():b]}")
        lines.append(f"### {name} [{word}] 件数={len(hits)}")
        lines.extend(hits[:12])
        if len(hits) > 12:
            lines.append(f"   …ほか{len(hits) - 12}件")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("done", len(sys.argv) - 3)


if __name__ == "__main__":
    main()
