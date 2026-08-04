# -*- coding: utf-8 -*-
"""読みの候補を**エンジンに実際に投げて**、どれが割れないかを見る道具。

🔴 なぜ要るか（2026-08-04）
   AivisSpeech は数詞を句で割ることがある。「15人」が **ジュウ／ゴニン** と割れると
   「10、5人」に聞こえる。「4560ミリメートル」は **ヨンセン／ゴヒャク／ロクジュウ** と
   3つに割れる。これは誤読ではなく**区切りの事故**なので、
   FORBIDDEN のような文字列一致では捕まらない。**候補を投げて数えるしかない。**

⚠️ **割れ方は前後の文で変わる。**（同じ「13回」でも他の行では割れない）
   だから候補は**その行の全文**に埋めて投げる。単語だけで試すと当てにならない。

    python tools/try_yomi.py            … 下の CASES を全部試す
    python tools/try_yomi.py 15人       … 語で絞る
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import narration as N

# (見出し, その行の全文, [候補の置換文字列 …])
#   候補の1つめは**素**（置換しない）。素が正しければ辞書に入れないのがいちばん安全。
CASES = []


def kana(text):
    q = json.loads(N.post("audio_query", None,
                          f"speaker={N.SPEAKER}&text={urllib.parse.quote(text)}").read())
    return N.kana_of(q)


def run(cases):
    """🔴 候補は **辞書の「値」としてそのまま**書くこと。

    `apply_yomi` はエンジンへ渡す直前に `to_kata()` を通すので、
    **ひらがなの値は必ずカタカナになる**。ここで to_kata を通さずに試すと、
    「ひらがなだと割れなかった」という**production では再現しない結論**が出る
    （実際に1度それで 17人 の候補を選びかけた）。
    ひらがなのまま渡したいときは、値に**漢字を1文字混ぜて** to_kata を素通りさせる。
    """
    for word, line, cands in cases:
        print(f"\n■ {word}   {line}")
        for c in cands:
            t = N.apply_yomi(line if c is None else line.replace(word, N.to_kata(c)))
            k = kana(t)
            print(f"   {'素' if c is None else c:<26} → {N.to_kata(c) if c else '':<24} {k}")


if __name__ == "__main__":
    pick = sys.argv[1] if len(sys.argv) > 1 else None
    run([c for c in CASES if not pick or pick in c[0]])
