# 26本目 ②：見た画像を1枚ずつ src/seen_log.tsv に残す（md5・大きさ・何のために）。数え間違いを防ぐ＝手で数えない
# 使い方: python -P ref/ep26/probe/seen26.py <画像> "<何のために>"  → 通しの番号と合計を出す（40枚まで）
import datetime, hashlib, os, sys

from PIL import Image

LOG = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "seen_log.tsv"))
LIMIT = 40


def main():
    path, why = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else ""
    with open(path, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    w, h = Image.open(path).size
    n = 0
    if os.path.exists(LOG):
        with open(LOG, encoding="utf-8") as f:
            n = sum(1 for line in f if line.strip() and not line.startswith("n\t"))
    else:
        with open(LOG, "w", encoding="utf-8", newline="\n") as f:
            f.write("n\twhen\tpath\tmd5\tsize\twhy\n")
    n += 1
    with open(LOG, "a", encoding="utf-8", newline="\n") as f:
        f.write(f"{n}\t{datetime.datetime.now():%Y-%m-%d %H:%M}\t{path}\t{md5}\t{w}x{h}\t{why}\n")
    print(f"seen {n}/{LIMIT}  {w}x{h}  {os.path.basename(path)}")
    return 2 if n > LIMIT else 0


if __name__ == "__main__":
    sys.exit(main())
