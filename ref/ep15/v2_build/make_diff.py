# -*- coding: utf-8 -*-
"""15本目④'：第1版→第2版の対照（変わったカットと節だけ）を diff_v1_v2.md に書く（読むだけ）。
当て直しの係（4'-18）が読む。カットは第1版と第2版の全行を並べ、節の差し替えは v2_sect_*.txt の OLD/NEW をそのまま並べる。
    python ref/ep15/v2_build/make_diff.py
"""
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
R = S.parent
v1 = (R / "daihon_v1.md").read_text(encoding="utf-8")
v2 = (R / "daihon_v2.md").read_text(encoding="utf-8")
CUT = re.compile(r"^\*\*(c[1-9]\d{2})\*\*[^\n]*\n(?:>[^\n]*\n)+", re.M)


def cuts(t):
    body = t.split("## 4. 台本", 1)[1].split("\n## 5.", 1)[0]
    return {m.group(1): m.group(0) for m in CUT.finditer(body)}


a, b = cuts(v1), cuts(v2)
bare = lambda blk: sum(len(re.sub(r"^>\s?(Q:\s)?★?", "", l)) for l in blk.splitlines() if l.startswith(">"))
out = ["# 第1版 → 第2版の対照（変わったカットだけ・当て直し用）", "",
       f"カット 第1版 {len(a)} ／ 第2版 {len(b)} ／ 変わった {sum(1 for k in a if a[k] != b.get(k))}", ""]
ch = None
for k in a:
    if a[k] == b.get(k):
        continue
    if k[:2] != ch:
        ch = k[:2]
        out += [f"## 第{ch[1]}章", ""]
    d = bare(b.get(k, "")) - bare(a[k])
    out += [f"### {k}（字 {d:+d}）", "第1版：", "```", a[k].rstrip("\n"), "```", "第2版：", "```", b.get(k, "（無い）").rstrip("\n"), "```", ""]
out += ["## 節の差し替え（v2_sect_*.txt）", ""]
for f in sorted(S.glob("v2_sect*.txt")):
    for m in re.finditer(r"@@@OLD\n(.*?)\n@@@NEW\n(.*?)\n@@@END", f.read_text(encoding="utf-8"), re.S):
        out += [f"### {f.name}", "前：", "```", m.group(1), "```", "後：", "```", m.group(2), "```", ""]
(S / "diff_v1_v2.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("→", S / "diff_v1_v2.md", "変わったカット", sum(1 for k in a if a[k] != b.get(k)))
