# -*- coding: utf-8 -*-
r"""el_earcheck.py — 耳で確かめたい行だけを mp3 に切り出す。

  python tools\el_earcheck.py ep008 --ids s025,s030,s133
  python tools\el_earcheck.py ep008 --ids s025 --context   … 前後1行もつなげて出す

なぜ要るか:
  ElevenLabs には「どう読んだか」を返す口が無いので、**合否はカズヤくんの耳**です
  （[[feedback-ear-beats-the-meter]]）。本編 wav を毎回頭出しして聴くのは現実的でないので、
  合成キャッシュ（audio_cache/<slug>/*.pcm）から**その行だけ**を取り出します。

🔴 キャッシュの鍵は **EL_YOMI を当てたあとの文**で作られています。
   生の台本から鍵を作ると、読みを直した行だけが「見つからない」ことになって
   検査から漏れます（el_check_yomi.py で実際に踏んだ事故）。必ず el_text を通すこと。

fail closed: キャッシュが1つでも欠けたら **exit 1**。無い行を黙って飛ばしません。

出力: out/<slug>_earcheck/<場面ID>.mp3 ＋ 一覧の index.txt
"""
import json
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_tts                                   # noqa: E402
import el_script as ES                          # noqa: E402  ★本番と同じ置換（el_text）とキャッシュの場所
from el_build import GAP                        # noqa: E402  行と行の間（本番と同じ）
el_text = ES.el_text


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    slug = ES.SLUG
    ids = ES.resolve_ids(arg("--ids"))          # 行ID（c112-2）かカットID（c112＝全行）。無いIDは止まる
    if not ids:
        print(__doc__)
        print("[FATAL] --ids で行IDを指定してください（例 --ids c112-2,c116）", file=sys.stderr)
        return 2
    ctx = "--context" in sys.argv

    scenes = ES.lines()
    by_id = {l.lid: i for i, l in enumerate(scenes)}

    outdir = ROOT / "out" / f"{slug}_earcheck"
    outdir.mkdir(parents=True, exist_ok=True)
    index, missing = [], []

    for sid in ids:
        k = by_id[sid]
        span = [k - 1, k, k + 1] if ctx else [k]
        span = [j for j in span if 0 <= j < len(scenes)]
        pcm = b""
        texts = []
        for j in span:
            sc = scenes[j]
            sent = el_text(sc.text)
            cache = ES.cache_path(sent)
            if not cache.exists():
                missing.append(f"{sc.lid}（{cache.name}）")
                continue
            if pcm:
                pcm += b"\x00\x00" * int(el_tts.SR * GAP)   # 本番の行間と同じ
            pcm += cache.read_bytes()
            texts.append(f"{sc.lid}: {sc.text}")
        if not pcm:
            continue
        wav = outdir / f"{sid}.wav"
        el_tts.write_wav(pcm, wav)
        mp3 = outdir / f"{sid}.mp3"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav),
                        "-codec:a", "libmp3lame", "-b:a", "128k", str(mp3)], check=True)
        wav.unlink()
        sec = len(pcm) / 2 / el_tts.SR
        print(f"  {mp3.name}  {sec:5.2f}秒  {texts[0][:52]}")
        index.append(f"{mp3.name}\t{sec:.2f}秒\t" + " / ".join(texts))

    (outdir / "index.txt").write_text("\n".join(index) + "\n", encoding="utf-8")
    print(f"\n{len(index)}本 -> {outdir}")
    if missing:
        print(f"🔴 合成キャッシュが無い行 {len(missing)}件: {', '.join(missing[:10])}", file=sys.stderr)
        print("   （el_build.py を回していないか、EL_YOMI を直して鍵が変わっています）", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
