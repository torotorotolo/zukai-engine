# -*- coding: utf-8 -*-
"""台本第2版 §4 を機械で読み、カットごとの「型・欄・出典・字幕」を出す。

⚠️ **手で写さないための道具**です。190カットを目で拾うと必ず取りこぼします。
    → 記憶 [[feedback-scale-one-visual-finding-to-a-full-count]]

台本の1カットの形：

    **c101** ／ 実写 pad_39b 射点39Bに立つ機体 ／ ch3 L11　🔧
    > 話は、打ち上げの前の日の夕方からはじまる。
    > 1月27日、フロリダのケネディ宇宙センターである。

  - 1つめの区切り … カットID（`**` で囲む）
  - 2つめ … **画の指定**。`実写 <欄の名> <説明>` ／ `図 <説明>` ／
             `quote（決め所）` ／ `panel <説明>`
  - 3つめ … 出典（`ch3 L11` など）。末尾に 🔧 が付くことがある
  - `>` の行 … 字幕（＝ナレーションの1行）

使い方:
    python ref/ep11/parse_script.py            # 一覧（章ごとの数も）
    python ref/ep11/parse_script.py --json     # JSON で吐く
    python ref/ep11/parse_script.py --slots    # 欄ごとに何カットが要るか
    python ref/ep11/parse_script.py --cut c101 # 1カットだけ
"""
import json
import re
import sys
from pathlib import Path

VAULT = Path("C:/Users/konar/Documents/Obsidian Vault")
SCRIPT = VAULT / "Projects" / "事故検証-チャレンジャー号-台本第2版-20260921.md"

# 期待値（check_script.py と揃える。ずれたら止める＝fail closed）
EXPECT_CUTS = 190
EXPECT_LINES = 470

_HEAD = re.compile(r"^\*\*([a-z]{1,2}\d{2,3}[a-z]?)\*\*\s*／\s*(.*)$")
_BODY = re.compile(r"^>\s*(.*)$")
_CH = re.compile(r"^###?\s+(.*)$")


def _split_head(rest):
    """'実写 pad_39b 射点39Bに立つ機体 ／ ch3 L11　🔧' を分解する。"""
    parts = [p.strip() for p in rest.split("／")]
    art = parts[0] if parts else ""
    src = parts[1] if len(parts) > 1 else ""
    fix = "🔧" in rest
    src = src.replace("🔧", "").strip()
    art = art.replace("🔧", "").strip()

    kind, slot, desc = "fig", None, art
    if art.startswith("実写"):
        kind = "photo"
        body = art[2:].strip()
        m = re.match(r"^([a-z0-9_]+)\s*(.*)$", body)
        if m:
            slot, desc = m.group(1), m.group(2).strip()
        else:
            desc = body
    elif art.startswith("quote"):
        kind, desc = "quote", art
    elif art.startswith("panel"):
        kind, desc = "panel", art[5:].strip()
    elif art.startswith("図"):
        kind, desc = "fig", art[1:].strip()
    return kind, slot, desc, src, fix


def parse(path=SCRIPT):
    txt = path.read_text(encoding="utf-8")
    # §4 台本 から §5 まで
    a = txt.index("## 4. 台本")
    b = txt.index("## 5. ")
    body = txt[a:b]

    cuts, chapter = [], ""
    cur = None
    for raw in body.splitlines():
        line = raw.rstrip()
        mc = _CH.match(line)
        if mc and "台本" not in mc.group(1):
            chapter = mc.group(1).strip()
            continue
        mh = _HEAD.match(line)
        if mh:
            kind, slot, desc, src, fix = _split_head(mh.group(2))
            cur = dict(id=mh.group(1), chapter=chapter, kind=kind,
                       slot=slot, desc=desc, src=src, fixed=fix, lines=[])
            cuts.append(cur)
            continue
        mb = _BODY.match(line)
        if mb and cur is not None:
            t = mb.group(1).strip()
            if t:
                cur["lines"].append(t)
    return cuts


def main():
    args = sys.argv[1:]
    cuts = parse()
    nlines = sum(len(c["lines"]) for c in cuts)

    # 🔴 fail closed：数が合わなければ何も出さずに止める
    if len(cuts) != EXPECT_CUTS or nlines != EXPECT_LINES:
        print(f"🔴 読めた数が合わない: カット {len(cuts)}（期待 {EXPECT_CUTS}）"
              f" / 行 {nlines}（期待 {EXPECT_LINES}）", file=sys.stderr)
        return 2

    if "--json" in args:
        print(json.dumps(cuts, ensure_ascii=False, indent=1))
        return 0

    if "--cut" in args:
        want = args[args.index("--cut") + 1]
        for c in cuts:
            if c["id"] == want:
                print(json.dumps(c, ensure_ascii=False, indent=1))
                return 0
        print(f"🔴 {want} は無い", file=sys.stderr)
        return 2

    if "--slots" in args:
        from collections import Counter
        n = Counter(c["slot"] for c in cuts if c["slot"])
        print(f"欄 {len(n)} 種 / 実写カット {sum(n.values())}")
        for k, v in sorted(n.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {k:24} {v}")
        return 0

    from collections import Counter
    kinds = Counter(c["kind"] for c in cuts)
    print(f"カット {len(cuts)} / 字幕行 {nlines}   {dict(kinds)}")
    ch = Counter(c["id"][:2] for c in cuts)
    print("章ごと:", " ".join(f"{k}={v}" for k, v in sorted(ch.items())))
    for c in cuts:
        s = f"[{c['slot']}]" if c["slot"] else ""
        print(f"{c['id']:6} {c['kind']:6} {s:22} {c['desc'][:34]:36} {c['src'][:20]:22} "
              f"{len(c['lines'])}行")
    return 0


if __name__ == "__main__":
    sys.exit(main())
