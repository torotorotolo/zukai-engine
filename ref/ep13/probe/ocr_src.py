"""画像だけのPDFを Windows 標準OCR（tools/ocr_win.ps1）で読む。
出力: ref/ep13/src/<name>.ocr.txt（'=== p N ===' 区切り）。標準出力に文書ごとの実測（よくある語の当たり率）。
fail closed: OCR の出力に頁ヘッダが揃わなければ NG と書く（0行で埋めない）。
"""
import os, re, subprocess, sys

import fitz

SRC = r"C:/Users/konar/Desktop/zukai-engine/ref/ep13/src"
PS1 = r"C:/Users/konar/Desktop/zukai-engine/tools/ocr_win.ps1"
TMP = r"C:/Users/konar/AppData/Local/Temp/claude/C--Users-konar-Documents-Obsidian-Vault/3febce82-d020-45c6-b4de-0b38ceece0fa/scratchpad/ocr"
DPI = 220
COMMON = set("the of and to in a is that for was on with as by at from this be it were or which an are not".split())

names = sys.argv[1:] or ["aib_8-76_TC-JAV", "ntsb_AAR73-02_N103AA"]
for name in names:
    doc = fitz.open(os.path.join(SRC, name + ".pdf"))
    d = os.path.join(TMP, name)
    os.makedirs(d, exist_ok=True)
    pngs = []
    for i, page in enumerate(doc, 1):
        p = os.path.join(d, f"p{i:03d}.png")
        if not os.path.exists(p):
            page.get_pixmap(dpi=DPI, colorspace=fitz.csGRAY).save(p)
        pngs.append(p)
    pages = {}
    for k in range(0, len(pngs), 8):
        batch = pngs[k:k + 8]
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", PS1,
                            "-Files", ",".join(batch)], capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        cur = None
        for line in r.stdout.splitlines():
            if line.startswith("## "):
                m = re.search(r"p(\d{3})\.png", line)
                cur = int(m.group(1)) if m else None
                pages.setdefault(cur, [])
            elif cur is not None:
                m = re.match(r"\[(\d+),(\d+)-(\d+),(\d+)\] (.*)", line)
                if m:
                    pages[cur].append((int(m.group(2)), int(m.group(1)), m.group(5)))
        if r.returncode != 0:
            print(f"  ps1 rc={r.returncode} batch={k} err={r.stderr[:300]}")
    missing = [i for i in range(1, len(pngs) + 1) if i not in pages]
    words = hits = 0
    with open(os.path.join(SRC, name + ".ocr.txt"), "w", encoding="utf-8") as f:
        for i in range(1, len(pngs) + 1):
            f.write(f"\n=== p {i} ===\n")
            for y, x, t in pages.get(i, []):  # OCR の返した順（読み順）のまま
                f.write(t + "\n")
                ws = re.findall(r"[A-Za-z]+", t.lower())
                words += len(ws)
                hits += sum(1 for w in ws if w in COMMON)
    tag = "OK" if not missing else "NG"
    print(f"{tag} {name} pages={len(pngs)} ocr_pages={len(pages)} missing={missing[:20]} "
          f"words={words} common={hits / words if words else 0:.3f}")
