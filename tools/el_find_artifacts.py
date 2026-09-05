# -*- coding: utf-8 -*-
r"""el_find_artifacts.py — 合成音に紛れ込んだ「余計な音」を波形から探す。

  python el_find_artifacts.py ep005
  python el_find_artifacts.py ep005 --dump out/ep005_artifacts   （疑わしい行を wav で書き出す）

なぜ要るか（2026-08-26 カズヤくん指摘）:
    ElevenLabs（eleven_v3）は、文の末尾や先頭に**台本に無い音**を付けてくることがある。
    しゃっくりのような音、息、言いかけの音節など。文字起こしには出ないので
    el_check_yomi では捕まらない。**波形で探すしかない。**

探し方:
    10ms ごとの実効値（RMS）で「声がある/ない」の帯を作り、
      ① 末尾: 250ms 以上の無音のあとに、短い（400ms 以下）音の塊が付いている
      ② 先頭: 短い音の塊のあと、250ms 以上の無音を挟んで本文が始まる
      ③ 途中: 700ms を超える不自然に長い無音（読点では説明がつかない間）
    を疑わしいとして挙げる。

⚠️ これは「疑い」を挙げる道具。**消してよいかは耳で確かめること。**
   「、」の間や、意味のある溜めを誤って消すと、喋りが不自然になる。
"""
import json
import struct
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_tts  # noqa: E402
import el_script as ES  # noqa: E402  行の列挙・EL_YOMI・キャッシュの場所
el_text = ES.el_text

# 🔴 2026-09-02: 物差し（閾値・envelope・runs・inspect）は el_artifacts.py へ移した。
#    el_tts.py の「検出→振り直し」の門番と同じ関数を使うため（2か所に持つと黙ってずれる）。
#    閾値の由来（2026-08-26 の実測 s020/s058/s054/s114）は el_artifacts.py の冒頭に書いてある。
from el_artifacts import (WIN, LEVEL, TAIL_SILENCE, TAIL_BLIP, MID_SILENCE,  # noqa: F401,E402
                          envelope, runs, inspect)
assert el_tts.SR == 24000, "el_artifacts.SR(24000) と el_tts.SR が食い違っている"


# envelope / runs / inspect は el_artifacts.py にある（上の import）。ここには置かない。


def main():
    dump = None
    if "--dump" in sys.argv:
        dump = Path(sys.argv[sys.argv.index("--dump") + 1])
        dump.mkdir(parents=True, exist_ok=True)
    hit = miss = 0
    rows = []
    for ln in ES.lines():
        sent = el_text(ln.text)
        p = ES.cache_path(sent)
        if not p.exists():
            miss += 1
            continue
        pcm = p.read_bytes()
        flags = inspect(pcm)
        if flags:
            hit += 1
            print(f"\n{ln.lid}  {len(pcm)/2/el_tts.SR:.2f}秒")
            print(f"   {ln.text[:52]}")
            for f in flags:
                print(f"   ⚠️ {f}")
                rows.append(f"{ln.lid}\t{f}\t{ln.text}")
            if dump:
                el_tts.write_wav(pcm, dump / f"{ln.lid}.wav")
    out = ES.qa_path("el_artifacts.tsv")
    out.write_text("行\t所見\t本文\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"\n疑わしい行 {hit} 件 -> {out}")
    if miss:
        print(f"⚠️ キャッシュが無くて調べられなかった行 {miss} 件 — 『全部OK』とは言えません")
        sys.exit(1)


if __name__ == "__main__":
    main()
