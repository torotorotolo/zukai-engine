# -*- coding: utf-8 -*-
"""⑤b-3 の作業表：echo／dup が鳴ったカットの 見出し・副題・図の文字・ナレーション を章ごとに並べる。

使い方: python ws.py            … 2本を回して ws_<章>.txt を書き、章ごとの件数を出す
        python ws.py --no-run   … 直前の echo.txt／dup.txt を読むだけ
"""
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path("C:/Users/konar/Desktop/zukai-engine")
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools"))
os.chdir(ROOT)
ENV = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")


def run(name):
    p = subprocess.run([sys.executable, f"tools/check_{name}.py"], capture_output=True,
                       text=True, encoding="utf-8", env=ENV)
    (OUT / f"{name}.txt").write_text(p.stdout + p.stderr, encoding="utf-8")
    return p.returncode


def parse(path):
    recs = defaultdict(list)
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, ln in enumerate(lines):
        m = re.match(r"\s+🔴 (\w+) (.*)", ln)
        if m:
            det = lines[i + 1].strip() if i + 1 < len(lines) else ""
            recs[m.group(1)].append(f"{m.group(2)} ⇒ {det}")
    return recs


def chapter(cid):
    return cid[:2]          # pr / ep / c1..c9


def main():
    codes = {}
    if "--no-run" not in sys.argv:
        codes = {n: run(n) for n in ("echo", "dup")}
    echo, dup = parse(OUT / "echo.txt"), parse(OUT / "dup.txt")
    import scene_jiko as S
    import check_echo as E
    bych = defaultdict(list)
    for cid in S.SPEC:
        if cid in echo or cid in dup:
            bych[chapter(cid)].append(cid)
    total = 0
    for ch, cids in bych.items():
        buf = []
        for cid in cids:
            sp = S.SPEC[cid]
            fig = sp.get("fig")
            kind = fig[0] if fig else ("photo:" + Path(str(sp.get("photo", ""))).stem
                                       if sp.get("photo") else "-")
            buf.append(f"■ {cid}  [{kind}]")
            buf.append(f"  t({len(str(sp.get('t', '')))}): {sp.get('t', '')}")
            buf.append(f"  s({len(str(sp.get('s', '')))}): {sp.get('s', '')}")
            for where, txt in E.spec_strings(sp):
                buf.append(f"  図 {where}: {txt}")
            buf.append("  語り:")
            for j, r in enumerate(S.SUBS.get(cid, []), 1):
                buf.append(f"    {j}) {r['text']}")
            for r in echo.get(cid, []):
                buf.append(f"  🔴echo {r}")
            for r in dup.get(cid, []):
                buf.append(f"  🔴dup  {r}")
            buf.append("")
            total += len(echo.get(cid, [])) + len(dup.get(cid, []))
        (OUT / f"ws_{ch}.txt").write_text("\n".join(buf), encoding="utf-8")
    print("exit:", codes)
    for ch in sorted(bych):
        n = sum(len(echo.get(c, [])) + len(dup.get(c, [])) for c in bych[ch])
        print(f"  {ch}: {len(bych[ch])}カット {n}件")
    print(f"  計 {total}件（echo {sum(map(len, echo.values()))}・dup {sum(map(len, dup.values()))}）")


if __name__ == "__main__":
    main()
