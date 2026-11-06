# -*- coding: utf-8 -*-
"""30本目 ⑥：公開ずみの回の片づけ（11-06 カズヤくん「はい、移して」）＝検品の絵・本編の mp4・層・使わなくなった映像を
削除待ちの箱 `out/_削除待ち_20261106/B_30本目/` へ移す（Claude は完全には消さない＝記憶 feedback-c-drive-cleanup-rules）。

- 移すのは返答でお見せした表の物だけ（検品の絵 7 フォルダ・本編 r01 の mp4・層 `out/jiko/c…_*.png`・`ref/ep30/src/eizou/Xb20.mp4`）
- 残す＝文字の記録（`ref/ep30/src` の表と網）・`out/thumb/ep30`・`_svghash.json`・`_geom_jobs.pkl`・器のフォルダ
- 1つずつの一覧は箱の `_manifest.tsv`（ファイル名）・リポの控えはフォルダごとの集計だけ（`cleanup_manifest_20261106.tsv`）

    python -P qa_out/ep30_r01/cleanup30.py --dry   … 数えるだけ（動かさない）
    python -P qa_out/ep30_r01/cleanup30.py         … 移す
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
JIKO = ROOT / "out" / "jiko"
BOX = ROOT / "out" / "_削除待ち_20261106" / "B_30本目"
DIRS = ["qa_ep30_b7", "qa-ep30_b7_full", "qa_ep30_c", "ep30_r01_frames", "qa-ep30_c2", "sheet_ep30_c", "qa_ep30_c2"]
FILES = [JIKO / "titan_audio-ep30-r01.mp4", ROOT / "ref" / "ep30" / "src" / "eizou" / "Xb20.mp4"]
LAYERS = sorted(JIKO.glob("c*_*.png"))


def size(p):
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.is_dir() else p.stat().st_size


def count(p):
    return sum(1 for f in p.rglob("*") if f.is_file()) if p.is_dir() else 1


def main():
    dry = "--dry" in sys.argv
    groups = [(f"out/jiko/{d}", [JIKO / d]) for d in DIRS if (JIKO / d).is_dir()]
    groups += [(str(p.relative_to(ROOT)).replace("\\", "/"), [p]) for p in FILES if p.exists()]
    groups += [("out/jiko/c…_*.png（層）", LAYERS)] if LAYERS else []
    rows, tot_n, tot_b = [], 0, 0
    for label, items in groups:
        n, b = sum(count(p) for p in items), sum(size(p) for p in items)
        rows.append((label, n, b))
        tot_n, tot_b = tot_n + n, tot_b + b
        print(f"{label}\t{n}個\t{b / 1e6:.1f}MB")
    print(f"計\t{tot_n}個\t{tot_b / 1e6:.1f}MB")
    if dry:
        return 0
    BOX.mkdir(parents=True, exist_ok=True)
    man = []
    for label, items in groups:
        for p in items:
            rel = p.relative_to(ROOT)
            dst = BOX / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            if p.is_dir():
                for f in p.rglob("*"):
                    if f.is_file():
                        man.append((str(f.relative_to(ROOT)).replace("\\", "/"), f.stat().st_size))
            else:
                man.append((str(rel).replace("\\", "/"), p.stat().st_size))
            shutil.move(str(p), str(dst))
    (BOX / "_manifest.tsv").write_text("path\tbytes\n" + "".join(f"{a}\t{b}\n" for a, b in man), encoding="utf-8")
    ctl = ROOT / "qa_out" / "ep30_r01" / "cleanup_manifest_20261106.tsv"
    ctl.write_text("group\tfiles\tMB\tmoved_to\n" + "".join(f"{l}\t{n}\t{b / 1e6:.1f}\tout/_削除待ち_20261106/B_30本目\n" for l, n, b in rows)
                   + f"計\t{tot_n}\t{tot_b / 1e6:.1f}\t\n", encoding="utf-8")
    left = [l for l, items in groups if any(p.exists() for p in items)]
    print(f"移した → {BOX}（一覧 {len(man)} 行）・残り {left or 'なし'}")
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main())
