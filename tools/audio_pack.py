# -*- coding: utf-8 -*-
"""ナレーション音声を**リポジトリに載せられる形**に詰め替える。

## なぜ必要か

クラウドの `render-jiko.yml` は `tools/audio_mix.py` を実行し、そこは
`audio/{cid}.wav` を Python の `wave` で直接読む。**つまり音声がリポジトリに
無いとクラウドで焼けない。** ところが wav は 1本34分ぶんで **156 MB** ある。

**git は履歴を消せない。** 開発中はナレーションを何度も作り直すので、
wav をそのまま入れると作り直すたびに156MBが積み上がる
（2026-07-31 は1日で3回作り直した＝そのまま入れていたら450MB増えていた）。
話数が増えればさらに効く。**public リポジトリでこれは持たない。**

## やり方

- **リポジトリに入れるのは `audio/opus/{cid}.opus`**（96kbps モノラル・**合計約22MB**）
- **`audio/*.wav` は gitignore**（ローカルの生成物。いつでも `narration.py build` で作り直せる）
- クラウドは焼く前に `python tools/audio_pack.py unpack` で wav に戻す。
  `audio_mix.py` は**一切変更しなくてよい**

## 音質について

Opus 96kbps モノラルは、話し声1人には十分すぎる（音楽ではないので帯域が要らない）。
最終的に YouTube 用に AAC 192k へ再エンコードされるが、
**ナレーションで聞き分けられる差は出ない。**
どうしても無圧縮で通したい回が出たら、その回だけ `pack --flac`（可逆・約半分）にする。

    python tools/audio_pack.py pack     … wav → opus（コミット前にローカルで実行）
    python tools/audio_pack.py unpack   … opus → wav（クラウドが焼く前に実行）
    python tools/audio_pack.py check    … 台本のカットと opus がそろっているか
"""
import subprocess
import sys
import wave
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent.parent
AUDIO = HERE / "audio"
OPUS = AUDIO / "opus"
BITRATE = "96k"


def _cids():
    sys.path.insert(0, str(HERE / "tools"))
    import narration
    return [cid for cid, _ in narration.SCRIPT]


def _run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print(f"🔴 {' '.join(args[:3])} … {r.stderr.strip()[:200]}")
    return r.returncode == 0


def pack(flac=False):
    OPUS.mkdir(parents=True, exist_ok=True)
    ext = "flac" if flac else "opus"
    cids, ok, src, dst = _cids(), 0, 0, 0
    # 台本から消えたカットの残骸を先に掃除する（歯抜けの逆＝ゴミが残る事故を防ぐ）
    for f in list(OPUS.glob("*.opus")) + list(OPUS.glob("*.flac")):
        if f.stem not in cids:
            f.unlink()
            print(f"（台本に無い {f.name} を削除）")
    for cid in cids:
        w = AUDIO / f"{cid}.wav"
        if not w.exists():
            print(f"🔴 {cid}.wav が無い。先に narration.py build を通すこと。")
            return 1
        o = OPUS / f"{cid}.{ext}"
        # 中身が変わっていないものは焼き直さない（build resume と同じ考え方）
        if o.exists() and o.stat().st_mtime >= w.stat().st_mtime:
            ok += 1
            src += w.stat().st_size
            dst += o.stat().st_size
            continue
        args = (["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(w)]
                + (["-c:a", "flac"] if flac else ["-c:a", "libopus", "-b:a", BITRATE, "-ac", "1"])
                + [str(o)])
        if not _run(args):
            return 1
        ok += 1
        src += w.stat().st_size
        dst += o.stat().st_size
    print(f"{ok} カット  wav {src/1e6:.0f} MB → {ext} {dst/1e6:.1f} MB "
          f"（{dst/src*100:.0f}%）")
    print(f"→ コミットするのは audio/opus/ のほう。audio/*.wav は gitignore 済み。")
    return 0


def unpack():
    """クラウドが焼く前に実行する。opus → wav に戻して audio_mix.py に渡す。"""
    cids, n = _cids(), 0
    for cid in cids:
        w = AUDIO / f"{cid}.wav"
        if w.exists():
            continue
        src = next((OPUS / f"{cid}.{e}" for e in ("opus", "flac")
                    if (OPUS / f"{cid}.{e}").exists()), None)
        if src is None:
            print(f"🔴 {cid} の音声が audio/opus/ に無い。pack し忘れている。")
            return 1
        # 元は 44100Hz モノラル16bit。audio_mix.py がその前提で読む
        if not _run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
                     "-ar", "44100", "-ac", "1", "-c:a", "pcm_s16le", str(w)]):
            return 1
        n += 1
    print(f"✓ {n} カットを wav に戻した（既存 {len(cids)-n} 本はそのまま）")
    return 0


def check():
    cids = _cids()
    have = {f.stem for f in OPUS.glob("*.opus")} | {f.stem for f in OPUS.glob("*.flac")}
    missing = [c for c in cids if c not in have]
    extra = sorted(have - set(cids))
    print(f"台本 {len(cids)} カット ／ audio/opus {len(have)} 本")
    if missing:
        print(f"🔴 足りない: {missing[:10]}{' …' if len(missing) > 10 else ''}")
    if extra:
        print(f"⚠️ 台本に無い: {extra[:10]}")
    if not missing and not extra:
        print("✓ 過不足なし")
    # 尺が一致しているかも見る（詰め替えで壊れていないことの確認）
    bad = 0
    for cid in cids[:5] + cids[-5:]:
        w = AUDIO / f"{cid}.wav"
        if not w.exists():
            continue
        with wave.open(str(w)) as f:
            sec = f.getnframes() / f.getframerate()
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(OPUS / f"{cid}.opus")],
                           capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip():
            d = float(r.stdout.strip())
            if abs(d - sec) > 0.06:      # Opus は端に数msの余白が付く
                print(f"🔴 {cid}: wav {sec:.2f}s vs opus {d:.2f}s")
                bad += 1
    print("✓ 抜き取りした尺は一致" if not bad else f"🔴 尺のずれ {bad} 件")
    return 1 if (missing or extra or bad) else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    if cmd == "pack":
        sys.exit(pack(flac="--flac" in sys.argv))
    sys.exit(unpack() if cmd == "unpack" else check())
