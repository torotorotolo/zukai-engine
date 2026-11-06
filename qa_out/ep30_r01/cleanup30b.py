# -*- coding: utf-8 -*-
"""30本目 ⑥：片づけの2回目（11-06 カズヤくん「はい、移して」＝1回目の返答でお見せした「まだ移していないもの」）。
⑤b の頃の検品フォルダ 12個と、`ref/ep30/src` の写真・映像・PDF・データの圧縮ファイルを
削除待ちの箱 `out/_削除待ち_20261106/C_30本目素材/` へ移す（Claude は完全には消さない）。

- 29本目の線と同じ＝`src` の mp4／jpg／png／pdf（＋この回の webm・zip）を移し、文字の記録（txt・tsv・json・md・py・html・log）は残す
- `src/_gshot_profile`（衛星写真を撮ったブラウザの控え）は丸ごと
- 1つずつの一覧は箱の `_manifest.tsv`・リポの控えはフォルダごとの集計だけ（`cleanup_manifest_20261106_2.tsv`）

    python -P qa_out/ep30_r01/cleanup30b.py --dry   … 数えるだけ
    python -P qa_out/ep30_r01/cleanup30b.py         … 移す
"""
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[2]
JIKO = ROOT / "out" / "jiko"
SRC = ROOT / "ref" / "ep30" / "src"
BOX = ROOT / "out" / "_削除待ち_20261106" / "C_30本目素材"
QA_DIRS = ["qa_ep30_b1_wiring", "qa_ep30_b2_modal", "qa_ep30_b2_open", "qa_ep30_b2_open2", "qa-ep30_b2_open", "qa-ep30_b3_map",
           "qa_ep30_b3_stock", "qa_ep30_b3_stock2", "qa_ep30_b3_stock3", "qa_ep30_b4", "qa_ep30_b5", "qa_ep30_b6"]
WHOLE = ["_gshot_profile"]
MEDIA_DIRS = ["eizou", "footage", "ksj", "shuki", "hanrei", "shobo", "sheets", "pages", "stock", "look_eizou"]
MEDIA_EXT = {".jpg", ".jpeg", ".png", ".mp4", ".webm", ".pdf", ".zip"}


def files_of(p):
    return [f for f in p.rglob("*") if f.is_file()] if p.is_dir() else [p]


def main():
    dry = "--dry" in sys.argv
    groups = [(f"out/jiko/{d}", [JIKO / d]) for d in QA_DIRS if (JIKO / d).exists()]     # qa_ep30_b2_modal は1つのファイル
    groups += [(f"ref/ep30/src/{d}（丸ごと）", [SRC / d]) for d in WHOLE if (SRC / d).is_dir()]
    for d in MEDIA_DIRS:
        fs = sorted(f for f in (SRC / d).rglob("*") if f.is_file() and f.suffix.lower() in MEDIA_EXT) if (SRC / d).is_dir() else []
        if fs:
            groups.append((f"ref/ep30/src/{d}（写真・映像・PDF・zip）", fs))
    rows, tot_n, tot_b = [], 0, 0
    for label, items in groups:
        fl = [f for p in items for f in files_of(p)]
        n, b = len(fl), sum(f.stat().st_size for f in fl)
        rows.append((label, n, b))
        tot_n, tot_b = tot_n + n, tot_b + b
        print(f"{label}\t{n}個\t{b / 1e6:.1f}MB")
    print(f"計\t{tot_n}個\t{tot_b / 1e6:.1f}MB")
    keep = [f for f in SRC.rglob("*") if f.is_file() and not any(f.is_relative_to(SRC / w) for w in WHOLE) and f.suffix.lower() not in MEDIA_EXT]
    print(f"残す（src の文字の記録）\t{len(keep)}個\t{sum(f.stat().st_size for f in keep) / 1e6:.1f}MB")
    if dry:
        return 0
    BOX.mkdir(parents=True, exist_ok=True)
    man = []
    for label, items in groups:
        for p in items:
            man += [(str(f.relative_to(ROOT)).replace("\\", "/"), f.stat().st_size) for f in files_of(p)]
            dst = BOX / p.relative_to(ROOT)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(dst))
    (BOX / "_manifest.tsv").write_text("path\tbytes\n" + "".join(f"{a}\t{b}\n" for a, b in man), encoding="utf-8")
    ctl = ROOT / "qa_out" / "ep30_r01" / "cleanup_manifest_20261106_2.tsv"
    ctl.write_text("group\tfiles\tMB\tmoved_to\n" + "".join(f"{l}\t{n}\t{b / 1e6:.1f}\tout/_削除待ち_20261106/C_30本目素材\n" for l, n, b in rows)
                   + f"計\t{tot_n}\t{tot_b / 1e6:.1f}\t\n", encoding="utf-8")
    left = [l for l, items in groups if any(p.exists() for p in items)]
    print(f"移した → {BOX}（一覧 {len(man)} 行）・残り {left or 'なし'}")
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main())
