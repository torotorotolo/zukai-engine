# -*- coding: utf-8 -*-
"""15本目④'：台本 第1版（読むだけ）に差し替え表を当てて第2版を組む（14本目 ref/ep14/v2_build/build_v2.py を写して15本目のIDに合わせた）。
  - 第1版の「## 1. 🔴 ④で決めたこと」から後ろを本体にし、頭と §0 は v2_head.md に差し替える（@@GATES@@ に gates.md を差す）
  - v2_sect*.txt（@@@OLD/@@@NEW/@@@END）＝節の差し替え。OLD は本体にちょうど1回出ること（違えば止まる）
  - v2_cuts_*.txt（@@ c101 ／ @@ +c1xx after c1yy）＝カットの差し替え・追加。元のカットがちょうど1つ在ること
    カットID＝c101〜c9xx（15本目は9章）
  - 差し替えたカットの見出しに 🔧 が無ければ止める（出典欄だけの直しは 🔧 を付けない＝@@ cNNN noflag）
終了コード 0=組めた / 2=当て損ない
"""
import re, sys, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
R = S.parent
v1 = (R / "daihon_v1.md").read_text(encoding="utf-8")
md5_before = hashlib.md5(v1.encode("utf-8")).hexdigest()
err = []
cut_at = v1.index("## 1. 🔴 ④で決めたこと")
body = v1[cut_at:]
ID = r"c[1-9]\d{2}"
# 係が自分のぶんだけで試しに組む：--only G3 --out <置き場>（ほかの係の書きかけで止まらない・daihon_v2.md は書かない）
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
OUT = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else R / "daihon_v2.md"
mine = lambda f: ONLY is None or f.stem.endswith("_" + ONLY)

n_sect = 0
for f in [f for f in sorted(S.glob("v2_sect*.txt")) if mine(f)]:
    t = f.read_text(encoding="utf-8")
    for m in re.finditer(r"@@@OLD\n(.*?)\n@@@NEW\n(.*?)\n@@@END", t, re.S):
        old, new = m.group(1), m.group(2)
        c = body.count(old)
        if c != 1:
            err.append(f"節 {f.name}: OLD が {c} 回 → {old[:60]!r}")
            continue
        body = body.replace(old, new)
        n_sect += 1

CUT = r"^\*\*{id}\*\*[^\n]*\n(?:>[^\n]*\n)+"
n_rep = n_add = 0
ids_seen = []
for f in [f for f in sorted(S.glob("v2_cuts_*.txt")) if mine(f)]:
    t = f.read_text(encoding="utf-8")
    for blk in re.split(r"^@@ ", t, flags=re.M)[1:]:
        head, rest = blk.split("\n", 1)
        new = rest.strip("\n") + "\n"
        noflag = head.strip().endswith("noflag")
        m = re.match(r"\+(" + ID + r") after (" + ID + r")", head.strip())
        if m:
            nid, after = m.groups()
            if not new.startswith(f"**{nid}**"):
                err.append(f"追加 {nid}: 見出しのIDが違う"); continue
            pat = re.compile(CUT.format(id=after), re.M)
            hits = pat.findall(body)
            if len(hits) != 1:
                err.append(f"追加 {nid}: {after} が {len(hits)} 個"); continue
            body = pat.sub(lambda x: x.group(0) + "\n" + new, body, count=1)
            n_add += 1; ids_seen.append(nid)
            continue
        cid = head.strip().split()[0]
        if not re.fullmatch(ID, cid):
            err.append(f"見出しが読めない: {head!r}"); continue
        if not new.startswith(f"**{cid}**"):
            err.append(f"差し替え {cid}: 見出しのIDが違う"); continue
        if not noflag and not new.startswith(f"**{cid}** 🔧"):
            err.append(f"差し替え {cid}: 🔧 が無い（出典欄だけなら noflag）"); continue
        pat = re.compile(CUT.format(id=cid), re.M)
        hits = pat.findall(body)
        if len(hits) != 1:
            err.append(f"差し替え {cid}: 元のカットが {len(hits)} 個"); continue
        if hits[0] == new:
            err.append(f"差し替え {cid}: 中身が第1版と同じ"); continue
        body = pat.sub(lambda x: new, body, count=1)
        n_rep += 1; ids_seen.append(cid)

dup = sorted({i for i in ids_seen if ids_seen.count(i) > 1})
if dup:
    err.append(f"同じカットを2回差し替え: {dup}")
head = (S / "v2_head.md").read_text(encoding="utf-8")
if (S / "gates.md").exists():
    head = head.replace("@@GATES@@", (S / "gates.md").read_text(encoding="utf-8").strip("\n"))
out = head.rstrip("\n") + "\n\n---\n\n" + body
v1_after = (R / "daihon_v1.md").read_text(encoding="utf-8")
if hashlib.md5(v1_after.encode("utf-8")).hexdigest() != md5_before:
    err.append("第1版が変わっている")
print(f"節の差し替え {n_sect} ／ カットの差し替え {n_rep} ／ 追加 {n_add} ／ 🔧 の見出し {len(re.findall(r'^\*\*' + ID + r'\*\* 🔧', out, re.M))}")
print("第1版 md5", md5_before)
if err:
    print("\n".join("E " + e for e in err))
    sys.exit(2)
OUT.write_text(out, encoding="utf-8")
print("→", OUT, len(out), "字")
