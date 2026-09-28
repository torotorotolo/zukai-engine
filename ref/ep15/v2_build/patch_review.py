# -*- coding: utf-8 -*-
"""15本目④'：照合し直し（R1・R2＝4'-18）の直しの案を差し替え表・役割表・節の表に当てる。
14本目 ref/ep14/v2_build/patch_review.py を写し、案を手で書き写さず review_result.json の patch（file・old・new）から当てる形にした。
  - 当てないもの＝review_not.json（[["c909", "指摘の頭の数文字", "不採用：理由"], …]）に書いたもの
  - 手で足す直し＝review_extra.json（[{"file":…, "old":…, "new":…, "why":…}, …]）
  - 元の文がちょうど1回なければ止まる（当て損ないを黙って通さない）。2回目に回すと「元の文が0回」で止まる＝二重に当てない
    python ref/ep15/v2_build/patch_review.py
"""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
rv = json.load(open(S / "review_result.json", encoding="utf-8"))
NOT = json.load(open(S / "review_not.json", encoding="utf-8")) if (S / "review_not.json").exists() else []
EXTRA = json.load(open(S / "review_extra.json", encoding="utf-8")) if (S / "review_extra.json").exists() else []
OK_FILE = re.compile(r"^(v2_cuts_G[1-6]\.txt|roles_G[1-6]\.tsv|v2_sect_(G[1-6]|Z)\.txt|v2_head\.md)$")

P = []
for h in rv:
    for x in h["issues"]:
        p = x.get("patch") or {}
        if not p.get("file") or p.get("old") in (None, ""):
            continue
        w = re.sub(r"\s+", " ", x["what"])
        if any(c == x["cut"] and k in w[:60] for c, k, _ in NOT):
            continue
        P.append((p["file"], p["old"], p["new"], f"{h['half'][:2]} {x['cut']}"))
P += [(e["file"], e["old"], e["new"], "extra " + e.get("why", "")[:30]) for e in EXTRA]

err = 0
for f, old, new, who in P:
    if not OK_FILE.match(f):
        print("E 当ててよいファイルでない", f, who); err += 1; continue
    p = S / f
    t = p.read_text(encoding="utf-8")
    n = t.count(old)
    if n != 1:
        print("E", n, "回", f, who, repr(old[:50])); err += 1; continue
    p.write_text(t.replace(old, new), encoding="utf-8")
print("当てた", len(P) - err, "／ 当て損ない", err)
sys.exit(2 if err else 0)
