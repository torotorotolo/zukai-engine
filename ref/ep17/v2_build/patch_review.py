# -*- coding: utf-8 -*-
"""17本目④'（15本目の道具を写した）：照合し直し（R1・R2＝4'-18）の直しの案を差し替え表・役割表・節の表に当てる。
14本目 ref/ep14/v2_build/patch_review.py を写し、案を手で書き写さず review_result.json の patch（file・old・new）から当てる形にした。
  - 当てないもの＝review_not.json（[["c909", "指摘の頭の数文字", "不採用：理由"], …]）に書いたもの
  - 手で足す直し＝review_extra.json（[{"file":…, "old":…, "new":…, "why":…}, …]）
  - 元の文がちょうど1回なければ止まる（当て損ないを黙って通さない）。2回目に回すと「元の文が0回」で止まる＝二重に当てない
    python ref/ep17/v2_build/patch_review.py
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
        # 17本目：1件に差し替えを複数持てる（聞き役の文を直すと roles_G*.tsv の文も直す）＝patches（配列）か patch（1つ）
        ps = [p for p in (x.get("patches") or [x.get("patch") or {}]) if p.get("file") and p.get("old") not in (None, "")]
        if not ps:
            continue
        w = re.sub(r"\s+", " ", x["what"])
        if any(c == x["cut"] and k in w[:60] for c, k, _ in NOT):
            continue
        P += [(p["file"], p["old"], p["new"], f"{h['half'][:2]} {x['cut']}") for p in ps]
P += [(e["file"], e["old"], e["new"], "extra " + e.get("why", "")[:30]) for e in EXTRA]

err = 0
for f, old, new, who in P:
    if not OK_FILE.match(f):
        print("E 当ててよいファイルでない", f, who); err += 1; continue
    p = S / f
    t = p.read_text(encoding="utf-8")
    # 🔴 17本目：新しい文が元の文を含む直し（元の文のうしろに足す形）は、2回目も元の文が1回あるので二重に当たった
    #    ＝新しい文がもうあれば「済み」として当てない
    if old in new and new in t:
        print("済み（もう当たっている）", f, who); err += 1; continue
    n = t.count(old)
    if n != 1:
        print("E", n, "回", f, who, repr(old[:50])); err += 1; continue
    p.write_text(t.replace(old, new), encoding="utf-8")
print("当てた", len(P) - err, "／ 当て損ない", err)
sys.exit(2 if err else 0)
