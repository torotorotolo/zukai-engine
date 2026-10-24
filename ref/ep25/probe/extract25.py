# -*- coding: utf-8 -*-
"""25本目②：src/ の PDF を頁ごとの文字にする（src/txt/<名前>.json＝[{"pdf":頁,"printed":印刷頁,"raw":…,"norm":…}]）。
norm＝NFKC＋空白を全部つぶした形（照合用）。印刷頁は頁の頭と尻の短い行の数字から推し、PDF頁との差の最頻値で埋める。
文字化けの割合（私用領域・置換文字・制御文字）と最後の頁の字数も出す＝%%EOF の無い PDF の欠けの当たり。
使い方: python extract25.py <src のフォルダ> <報告の出力>"""
import json, os, re, sys, unicodedata
from collections import Counter

import fitz


def norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


def garble(s):
    if not s:
        return 0.0
    bad = sum(1 for c in s if (0xE000 <= ord(c) <= 0xF8FF) or c == "�" or (ord(c) < 32 and c not in "\n\r\t"))
    return bad / len(s)


NUMLINE = re.compile(r"^[-－‐ー―\s]*([0-9０-９]{1,3})[-－‐ー―\s]*$")


def printed_guess(text):
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for l in lines[-3:] + lines[:2]:
        m = NUMLINE.match(l)
        if m:
            return int(unicodedata.normalize("NFKC", m.group(1)))
    return None


def main():
    src, out = sys.argv[1], sys.argv[2]
    dst = os.path.join(src, "txt")
    os.makedirs(dst, exist_ok=True)
    rep = []
    for root, _, files in os.walk(src):
        if os.path.abspath(root).startswith(os.path.abspath(dst)):
            continue
        for fn in sorted(files):
            if not fn.lower().endswith(".pdf"):
                continue
            p = os.path.join(root, fn)
            try:
                doc = fitz.open(p)
            except Exception as e:
                rep.append(f"{fn}\tOPEN_ERR\t{e}")
                continue
            pages, offs = [], Counter()
            for i, pg in enumerate(doc, 1):
                t = pg.get_text("text")
                g = printed_guess(t)
                if g is not None:
                    offs[i - g] += 1
                pages.append({"pdf": i, "printed_guess": g, "raw": t, "norm": norm(t), "garble": round(garble(t), 3),
                              "images": len(pg.get_images(full=True))})
            off, cnt = (offs.most_common(1)[0] if offs else (None, 0))
            for d in pages:
                d["printed"] = (d["pdf"] - off) if off is not None else None
            name = os.path.splitext(fn)[0]
            with open(os.path.join(dst, name + ".json"), "w", encoding="utf-8") as f:
                json.dump(pages, f, ensure_ascii=False)
            gbad = sum(1 for d in pages if d["garble"] > 0.05)
            empty = sum(1 for d in pages if len(d["norm"]) < 20)
            last = pages[-1]["norm"][-60:] if pages else ""
            rep.append(f"{fn}\tpages={len(pages)}\toffset(pdf-printed)={off}x{cnt}\tgarbled>5%={gbad}\tnear_empty={empty}"
                       f"\trepaired={getattr(doc, 'is_repaired', '?')}\tlast_tail={last}")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(rep) + "\n")
    print("done", len(rep))


if __name__ == "__main__":
    main()
