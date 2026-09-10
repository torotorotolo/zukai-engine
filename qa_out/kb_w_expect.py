# -*- coding: utf-8 -*-
"""この巡で**設計を変えたカット**を、git の差分から機械で出す。

■ なぜ要るか
  `kb_u_changed.py` の「予測」は `qa_out/kb_u_expect.txt`（前の巡に手で書いた一覧）を読む。
  巡が変わると**中身が古いまま残る**ので、🔴 が出ても意味がない
  （[[feedback-gates-go-stale-when-upstream-changes]]＝門番は黙って間違った合格・不合格を出す）。
  → **手で書かずに、差分から出す。**

■ 測り方
  `git diff <base>..HEAD -- tools/cuts/` で変わった行番号を取り、
  `qa_out/kb_w_show.py` の「1カット＝1ブロック」の行範囲と突き合わせる。
  ⚠️ **注釈（`#` の行）だけが変わったカットも「変えた」に数える。**
     絵は変わらないが、次の巡で「なぜ変わっていないのか」を調べる手間を省くため
     `注のみ` と印を付けて別に数える。

    python -u qa_out/kb_w_expect.py dd902e2
    python -u qa_out/kb_w_expect.py dd902e2 --write   # kb_u_expect.txt を書き替える
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "qa_out"))
sys.stdout.reconfigure(encoding="utf-8")

from kb_w_show import blocks                                # noqa: E402

HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def changed_lines(base, path):
    """そのファイルで**いまの版の**何行目が変わったか（新しい側の行番号）。"""
    out = subprocess.run(
        ["git", "diff", "-U0", f"{base}..HEAD", "--", str(path)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise SystemExit(f"🔴 git diff が落ちた（0件と数えない）: {out.stderr[:200]}")
    lines = set()
    for ln in out.stdout.splitlines():
        m = HUNK.match(ln)
        if m:
            a = int(m.group(1))
            n = int(m.group(2) or 1)
            lines.update(range(a, a + n))
    return lines


def main(base, write=False):
    print(f"■ base: {base} → HEAD")
    src = {}
    hit, note_only = [], []
    for p in sorted((ROOT / "tools" / "cuts").glob("*.py")):
        ch = changed_lines(base, p)
        if not ch:
            continue
        text = p.read_text(encoding="utf-8").splitlines()
        for cid, (a, b, _t) in blocks(p).items():
            inside = [n for n in ch if a <= n <= b]
            if not inside:
                continue
            src[cid] = p.name
            # 中身の行（`#` で始まらない行）が1行でも変わっていれば絵が変わる
            real = [n for n in inside
                    if n - 1 < len(text) and not text[n - 1].lstrip().startswith("#")]
            (hit if real else note_only).append(cid)
    print(f"■ 絵が変わるはず ＝ {len(hit)} カット")
    print("  " + " ".join(sorted(hit)))
    print(f"■ 注釈だけ変えた（絵は変わらない）＝ {len(note_only)} カット")
    print("  " + " ".join(sorted(note_only)))
    if write:
        f = ROOT / "qa_out" / "kb_u_expect.txt"
        f.write_text("\n".join(sorted(hit)) + "\n", encoding="utf-8")
        print(f"■ 書いた: {f}")
    return 0


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        raise SystemExit("🔴 base のコミットを渡す（例: dd902e2）")
    raise SystemExit(main(a[0], "--write" in sys.argv[1:]))
