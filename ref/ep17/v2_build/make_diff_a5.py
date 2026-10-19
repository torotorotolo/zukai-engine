# -*- coding: utf-8 -*-
"""17本目⑤a-1（2026-10-19）：⑤a-1 の前の第2版（git の版）→ いまの第2版の対照を diff_a5.md に書く（読むだけ）。
make_diff.py（第1版→第2版）と同じ型＝変わったカットは前と後の全行を並べ、カットの外（§1・§2）は行ごとの差を並べる。
§0（門番の結果＝final17.py が書き直す）は比べない。
    python ref/ep17/v2_build/make_diff_a5.py [前の版＝8cc8dd47]
"""
import difflib, hashlib, re, subprocess, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
R = S.parent
REV = sys.argv[1] if len(sys.argv) > 1 else "8cc8dd47"
old = subprocess.run(["git", "show", f"{REV}:ref/ep17/daihon_v2.md"], cwd=R, capture_output=True).stdout.decode("utf-8")
new = (R / "daihon_v2.md").read_text(encoding="utf-8")
md5 = lambda s: hashlib.md5(s.encode("utf-8")).hexdigest()
MK = "## 1. 🔴 ④で決めたこと"
ob, nb = old[old.index(MK):], new[new.index(MK):]
CUT = re.compile(r"^\*\*(c[1-9ab]\d{2})\*\*[^\n]*\n(?:>[^\n]*\n)+", re.M)
cuts = lambda t: {m.group(1): m.group(0) for m in CUT.finditer(t.split("## 4. 台本", 1)[1].split("\n## 5.", 1)[0])}
a, b = cuts(ob), cuts(nb)
PUN = re.compile(r"[、。？！「」（）・\s]")
bare = lambda blk: sum(len(PUN.sub("", re.sub(r"^>\s?(Q:\s)?★?", "", l))) for l in blk.splitlines() if l.startswith(">"))
ch = [k for k in a if a[k] != b.get(k)]
out = ["# ⑤a-1 の前 → いまの第2版の対照（17本目・2026-10-19）", "",
       f"- 前＝`git show {REV}:ref/ep17/daihon_v2.md`（改行を LF にそろえた中身の md5 `{md5(old)}`）／いま＝`daihon_v2.md`（同 `{md5(new)}`）",
       "- 差し替え表＝`v2_post_a5.txt`（`build_v2.py` の「後の直し」の段）。§0 は final17.py が書き直す＝ここでは比べない",
       f"- 変わったカット {len(ch)}／句読点なし {sum(bare(a[k]) for k in a)} → {sum(bare(b[k]) for k in b)}字（{sum(bare(b[k]) - bare(a[k]) for k in ch):+d}）", ""]
for k in ch:
    out += [f"## {k}（句読点なし {bare(a[k])}→{bare(b[k])}）", "", "前：", "```", a[k].rstrip("\n"), "```", "後：", "```", b[k].rstrip("\n"), "```", ""]
# カットの外（§1〜§3・§5 以降）の差＝本文からカットを除いて行で比べる
strip = lambda t: CUT.sub("", t).splitlines()
d = [l for l in difflib.unified_diff(strip(ob), strip(nb), "前", "後", n=0, lineterm="") if not l.startswith(("---", "+++"))]
out += ["## カットの外（§1・§2）", "", "```diff"] + d + ["```", ""]
(S / "diff_a5.md").write_text("\n".join(out), encoding="utf-8")
print("→", S / "diff_a5.md", "変わったカット", len(ch), "・カットの外の差の行", sum(1 for l in d if l[:1] in "+-"))
