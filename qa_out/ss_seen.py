# -*- coding: utf-8 -*-
"""⑤c 検品【見る】の「見た枚」を機械で記録する（手で数えると必ず間違える）。

使い方（repo 直下で）:
  python qa_out/ss_seen.py mark c101 c102 c103 c104   # 見た枚を追記
  python qa_out/ss_seen.py check                        # 見た枚数・次の4枚・残り
  python qa_out/ss_seen.py unmark c104                  # 取り消し
順番＝ `ls out/jiko/qa_ss-r01/cut_*.jpg` の順（c101→…→ep16→pr01…）。pr は最後。
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
QA_DIR = os.path.join(ROOT, "out", "jiko", "qa_ss-r01")
SEEN = os.path.join(HERE, "surfside_seen.txt")
PER_CHAT = 40


def all_cuts():
    names = sorted(f[4:-4] for f in os.listdir(QA_DIR) if f.startswith("cut_") and f.endswith(".jpg"))
    return names


def seen():
    if not os.path.exists(SEEN):
        return []
    with open(SEEN, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    cuts = all_cuts()
    s = seen()
    if cmd == "mark":
        for c in sys.argv[2:]:
            if c not in cuts:
                print(f"!! {c} は検品画像に無い"); sys.exit(2)
            if c in s:
                print(f"!! {c} は記録ずみ"); sys.exit(2)
        with open(SEEN, "a", encoding="utf-8") as f:
            for c in sys.argv[2:]:
                f.write(c + "\n")
        s = seen()
    elif cmd == "unmark":
        s = [c for c in s if c not in sys.argv[2:]]
        with open(SEEN, "w", encoding="utf-8") as f:
            f.write("".join(c + "\n" for c in s))
    rest = [c for c in cuts if c not in s]
    n_chat = len(s) % PER_CHAT or (PER_CHAT if s else 0)
    print(f"全 {len(cuts)} ／ 見た {len(s)}（このチャット {n_chat}/{PER_CHAT}）／ 残り {len(rest)}")
    print("次の4枚:", " ".join(rest[:4]) if rest else "（全数完了）")


if __name__ == "__main__":
    main()
