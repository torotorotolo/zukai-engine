# -*- coding: utf-8 -*-
"""24本目：このチャットで「読んだ画像」を機械で数える（手で数えると必ず間違える）。
使い方: seen.py add <チャット番号> <画像の道> <何を見たか>   ＝ md5 つきで1行足す
        seen.py count [<チャット番号>]                   ＝ 枚数（チャットごと・40枚まで）
帳＝ref/ep24/src/seen_log.tsv（git の外）"""
import hashlib, os, sys, time

LOG = r"C:\Users\konar\Desktop\zukai-engine\ref\ep24\src\seen_log.tsv"


def main():
    cmd = sys.argv[1]
    if cmd == "add":
        chat, path, what = sys.argv[2], sys.argv[3], " ".join(sys.argv[4:])
        md5 = hashlib.md5(open(path, "rb").read()).hexdigest()
        new = not os.path.exists(LOG)
        with open(LOG, "a", encoding="utf-8") as f:
            if new:
                f.write("time\tchat\tfile\tmd5\twhat\n")
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{chat}\t{os.path.basename(path)}\t{md5}\t{what}\n")
    rows = [l.rstrip("\n").split("\t") for l in open(LOG, encoding="utf-8")][1:] if os.path.exists(LOG) else []
    chat = sys.argv[2] if len(sys.argv) > 2 else None
    n = sum(1 for r in rows if chat is None or r[1] == chat)
    print(f"seen: {n} 枚（チャット {chat or '全部'}）／40枚まで")


if __name__ == "__main__":
    main()
