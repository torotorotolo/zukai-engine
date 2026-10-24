# -*- coding: utf-8 -*-
"""25本目②：見た画像を機械で記録して数える（1チャット40枚まで・1メッセージ4枚まで）。src/seen_log.tsv（git の外）。
使い方: python seen25.py add <画像> <何を見たか>   /   python seen25.py count"""
import hashlib, os, sys, time

LOG = r"C:\Users\konar\Desktop\zukai-engine\ref\ep25\src\seen_log.tsv"


def main():
    if sys.argv[1] == "add":
        p, what = sys.argv[2], sys.argv[3]
        # ブラウザの画面写しなど、手元にファイルが無いものは p に「screen:<説明>」と書く
        md5 = "--------" if p.startswith("screen:") else hashlib.md5(open(p, "rb").read()).hexdigest()[:8]
        n = sum(1 for _ in open(LOG, encoding="utf-8")) if os.path.exists(LOG) else 0
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{n + 1}\t{time.strftime('%Y-%m-%d %H:%M')}\t{md5}\t{os.path.basename(p)}\t{what}\n")
        print(f"seen #{n + 1} / 40  {os.path.basename(p)}")
    else:
        n = sum(1 for _ in open(LOG, encoding="utf-8")) if os.path.exists(LOG) else 0
        print(f"seen {n} / 40")


if __name__ == "__main__":
    main()
