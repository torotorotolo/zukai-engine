# -*- coding: utf-8 -*-
"""⚠️ 2026-09-07：この道具は `tools/qa_seen.py` に一般化した。**新しい題材では使わない。**
   ここは 4本目サーフサイドの記録（`surfside_seen.txt`）を読むためだけに残してある。
   🔴 比べるフォルダ名（`qa_ss-r01`）が**本文に焼き付いている**ので、焼き直すと
      黙って前の絵を見る。新しい道具はフォルダを `qa_out/<slug>_qa.json` に置き、
      見た時点の md5 を1枚ずつ持つ。

⑤c 検品【見る】の「見た枚」を機械で記録する（手で数えると必ず間違える）。

使い方（repo 直下で）:
  python qa_out/ss_seen.py mark c101 c102 c103 c104   # 見た枚を追記
  python qa_out/ss_seen.py check                        # 見た枚数・次の4枚・残り
  python qa_out/ss_seen.py unmark c104                  # 取り消し
  python qa_out/ss_seen.py check --photo                # 案2（2026-09-05）＝写真カットだけの残りと次の4枚
⚠️ Git Bash では出力が文字化けする＝ PYTHONIOENCODING=utf-8 を付けて読む。
順番＝ `ls out/jiko/qa_ss-r01/cut_*.jpg` の順（c101→…→ep16→pr01…）。pr は最後。
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
QA_DIR = os.path.join(ROOT, "out", "jiko", "qa_ss-r01")
SEEN = os.path.join(HERE, "surfside_seen.txt")
PHOTO = os.path.join(HERE, "surfside_photo_rest.txt")   # 案2＝写真カットだけ見る順番（`check --photo`）
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
    if "--photo" in sys.argv:
        # 2026-09-05 カズヤくん決定（案2）＝残りの目視は写真カットだけ。順番は surfside_photo_rest.txt
        with open(PHOTO, encoding="utf-8") as f:
            photo = [l.strip() for l in f if l.strip()]
        prest = [c for c in photo if c not in s]
        print(f"写真カットの残り {len(prest)}／{len(photo)}（型カットは門番に任せる）")
        print("次の4枚:", " ".join(prest[:4]) if prest else "（写真カット完了）")
        return
    print("次の4枚:", " ".join(rest[:4]) if rest else "（全数完了）")


if __name__ == "__main__":
    main()
