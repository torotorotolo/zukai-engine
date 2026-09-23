# -*- coding: utf-8 -*-
"""12本目⑤a：c512-1「およそ30分後」だけを、**1テイクにつき聞取2回**の厳しめの基準で取り直す（2026-09-23）。

なぜ要るか:
  c512-1 は5通りの書き方が1回の聞取でどれも『三分後』。「さんじゅうふんご」だけ1回目『30分後』だったが、
  **同じ音（出荷する音＝ES.shipped）を2回目に起こすと『三分後』**＝音が 3 と 30 の境目にある。
  ⚠️ 最初「生の音と出荷する音の違い」と見立てたが、el_probe_words も el_check_yomi も ES.shipped を通していた＝**見立ては誤り**。
  → 行頭の数語が弱い型（v3 は 0ms から声が始まる）への定番の手＝頭に「　、」を足して振り直す。
    ただし合格は**2回の聞取が2回とも 30 を書いたテイク**だけ（1回の観測で決めない＝5a-11）。
試す順: 標準の読み さんじゅっぷんご（2テイク）→ だめなら さんじゅうふんご（2テイク）。合格した送信文と音を採る。
出力: 画面（採ったテイクと聞取2回）。キャッシュは合格したテイクで書き換える（不合格なら最後のテイクが残るので、
      el_script の EL_YOMI をどちらの送信文にするかは結果を見て決める）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402
import el_tts           # noqa: E402
from el_check_yomi import stt  # noqa: E402

LID = "c512-1"
PREFIX = "　、"
TAIL = "、雲を撮る飛行機から、何かが落ちてくるのが見えた。"
CANDS = ["およそさんじゅっぷんご" + TAIL, "およそさんじゅうふんご" + TAIL]
OK30 = re.compile(r"30分|三十分")


N_STT = 3        # 🔴 2026-09-23 2回目の実行: 2回そろった take1 が、el_check_yomi の3回目で『三分後』＝2回では足りなかった
MAX_TAKES = 3


def main():
    for sent in CANDS[:1] if "--std" in sys.argv else CANDS:
        for t in range(1, MAX_TAKES + 1):
            pcm = el_tts.synth(sent, LID, slug=ES.SLUG, settings=ES.SETTINGS, refresh=True, send_text=PREFIX + sent)
            hs = [stt(ES.shipped(pcm)) for _ in range(N_STT)]
            ok = all(OK30.search(h) for h in hs)
            print(f"{'✓' if ok else '✗'} {sent[:14]}… take{t}\n" + "\n".join(f"    {i+1}回目: {h}" for i, h in enumerate(hs)),
                  flush=True)
            if ok:
                ES.cache_path(sent).write_bytes(pcm)      # 念のため合格テイクを明示して書く（refresh でも書かれている）
                print(f"\n採用: 送信文「{sent}」（take{t}・聞取2回とも 30）")
                return 0
    print("\n🔴 4テイクとも2回そろって 30 にならなかった＝書き方ではなく**台本の言い回し**で直す段")
    return 1


if __name__ == "__main__":
    sys.exit(main())
