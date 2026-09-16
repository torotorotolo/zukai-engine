# -*- coding: utf-8 -*-
"""9本目 テネリフェ ⑤a：台本第2版 §4 を tools/narration.py の SCRIPT へ**機械で**写す（2026-09-16）。

  python qa_out/ep9_script_copy.py          … 写して、写した結果を import し直して突き合わせる
  python qa_out/ep9_script_copy.py --check  … 写さずに突き合わせだけ（食い違いがあれば exit 1）

🔴 切り方は check_script.py の parse / clean を**そのまま呼ぶ**（物差しを2か所に持たない）。
   8本目（33d4ad6）と同じ作法。写したあと、md と SCRIPT が1文字も違わないことを assert する。
⚠️ 台本の文言の正本は、ここから先は narration.SCRIPT（字幕も音もここから作る）。
"""
import importlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import check_script as CSC  # noqa: E402

MD = Path.home() / "Documents" / "Obsidian Vault" / "Projects" / "事故検証-テネリフェ-台本第2版-20260916.md"
NARR = ROOT / "tools" / "narration.py"
WANT = {"cuts": 215, "lines": 495, "chars": 12515, "quotes": 14}


def from_md():
    text = MD.read_text(encoding="utf-8")
    cuts = CSC.parse(text)
    # 章の見出し（§4 の中の ### 行）を、次に来るカットIDに結びつける
    heads, on, pending = {}, False, None
    for raw in text.split("\n"):
        line = raw.rstrip()
        if line.startswith("## 4. 台本"):
            on = True
            continue
        if on and re.match(r"^## \d", line):
            break
        if not on:
            continue
        if line.startswith("### "):
            pending = line[4:].strip()
            continue
        m = CSC.CUT_RE.match(line)
        if m and pending:
            heads[m.group(1)] = pending
            pending = None
    nq = sum(1 for _, _, ls in cuts if any(CSC.STAR_RE.match(l) for l in ls))
    out = [(cid, pic, [CSC.clean(l) for l in ls]) for cid, pic, ls in cuts]
    return out, heads, nq


def block(cuts, heads):
    q = lambda s: json.dumps(s, ensure_ascii=False)  # noqa: E731  Python の文字列リテラルとしても正しい
    rows = ["SCRIPT = ["]
    for cid, pic, ls in cuts:
        if cid in heads:
            rows.append(f"    # ── {heads[cid]} ────────────")
        rows.append(f"    # {cid} ／ {pic}")
        pad = " " * (len(f'    ("{cid}", ['))
        body = f"    ({q(cid)}, [" + q(ls[0])
        for l in ls[1:]:
            body += ",\n" + pad + q(l)
        rows.append(body + "]),")
    rows.append("]")
    return "\n".join(rows) + "\n"


def compare(cuts, nq):
    sys.modules.pop("narration", None)
    import narration
    importlib.reload(narration)
    got = [(cid, [t.strip() for t in ls]) for cid, ls in narration.SCRIPT]
    want = [(cid, ls) for cid, _, ls in cuts]
    bad = []
    if len(got) != len(want):
        bad.append(f"カット数 SCRIPT {len(got)} ／ md {len(want)}")
    for (gc, gl), (wc, wl) in zip(got, want):
        if gc != wc or gl != wl:
            bad.append(f"{wc}: SCRIPT {gc} {gl!r} ／ md {wl!r}")
    n_lines = sum(len(ls) for _, ls in got)
    n_chars = sum(len(t) for _, ls in got for t in ls)
    print(f"SCRIPT: {len(got)}カット／{n_lines}行／{n_chars}字（md の決め所 {nq}）")
    real = {"cuts": len(got), "lines": n_lines, "chars": n_chars, "quotes": nq}
    if real != WANT:
        bad.append(f"数が第2版の実測と違う: {real} ／ 期待 {WANT}")
    if bad:
        print("🔴 食い違い:\n  " + "\n  ".join(bad[:20]))
        return 1
    print("✓ md と SCRIPT は1文字も違わない（215／495／12,515／14）")
    return 0


def main():
    cuts, heads, nq = from_md()
    if "--check" not in sys.argv:
        src = NARR.read_text(encoding="utf-8")
        a = src.index("\nSCRIPT = [\n") + 1
        b = src.index("\n]\n", a) + 3          # SCRIPT の閉じ括弧の行まで
        assert src[b:].lstrip("\n").startswith("GAP = "), "SCRIPT の直後が GAP でない（切る位置を誤っている）"
        NARR.write_text(src[:a] + block(cuts, heads) + src[b:], encoding="utf-8")
        print(f"写した: {NARR.name}（章の見出し {len(heads)}件）")
    return compare(cuts, nq)


if __name__ == "__main__":
    sys.exit(main())
