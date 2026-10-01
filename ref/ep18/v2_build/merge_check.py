# -*- coding: utf-8 -*-
"""18本目④'：照合の係の findings_G*.json を1つの check_result.json にまとめ、「ずれ」を1行ずつ短く出す（読むだけ）。
    python ref/ep18/v2_build/merge_check.py [--sev 🔴] [--g G3] [--full]
  --full＝台本の文・原文・問題・案まで出す（🔴 と⚠️の芯を G0 が原文に引き直すとき用）
"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
res = []
for f in sorted(S.glob("findings_G*.json")):
    res.append(json.load(open(f, encoding="utf-8")))
json.dump(res, open(S / "check_result.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sev = sys.argv[sys.argv.index("--sev") + 1] if "--sev" in sys.argv else None
g = sys.argv[sys.argv.index("--g") + 1] if "--g" in sys.argv else None
full = "--full" in sys.argv
from collections import Counter
c = Counter()
for r in res:
    for x in r["findings"]:
        c[(r["group"], x["severity"])] += 1
print("係ごと：", " ".join(f"{k[0]}{k[1]}{v}" for k, v in sorted(c.items())))
print("計", sum(c.values()), "件／items", sum(len(r.get("items", [])) for r in res), "件（ずれ", sum(1 for r in res for it in r.get("items", []) if not it["verdict"].startswith("OK")), "）")
for r in res:
    if g and r["group"] != g:
        continue
    for x in r["findings"]:
        if sev and x["severity"] != sev:
            continue
        print(f"{x['id']} {x['cut']} L{x.get('line')} {x['severity']} {x['face']} [{x['kind']}] {x['short']}")
        if full:
            for k in ("script_text", "source_page", "source_quote", "problem", "proposal"):
                print(f"    {k}: {x.get(k, '')}")
    if not sev:
        for it in r.get("items", []):
            if not it["verdict"].startswith("OK"):
                print(f"  item {r['group']} {it['cut']} {it['item'][:50]} → {it['verdict'][:160]}")
