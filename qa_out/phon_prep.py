# -*- coding: utf-8 -*-
"""音素の網（再発防止策1の試作）── 行ごとの音（出荷する音）と送信文を1つにまとめる（API 不使用・2026-09-24）。

  python qa_out/phon_prep.py ep13                   … この作業ツリーの audio/<cid>.wav（＝出荷する音）を行に切る
  python qa_out/phon_prep.py ep12r04 [--main <本線>] … 12本目 r04（試写1回目の音＝陽性対照）を本線の git（4ec4fd0）から
  python qa_out/phon_prep.py ep13raw --ids c303-1,…   … 速さを上げる前の音（合成キャッシュ・TEMPO 1.0）。判定に迷う行の聞き直し

流れ: phon_prep → modal run qa_out/phon_asr_modal.py --tag <tag> → phon_review（全行の一覧）／phon_verify（直した行）
陽性対照の実測（2026-09-24・12本目 r04）: 誤読 9行中 8行を捕まえた。記録＝audio/el_qa/ep12r04_phon_validation.txt

出力（git の外）: out/phon/<tag>_wav16.npz（行ID → 16kHz int16）／out/phon/<tag>_texts.json（行ID → {text, sent}）
🔴 行の切り方は el_build.build_cut と同じ（narration.json の subtitles の t・d）＝速さ・間の調整・フェードまで済んだ音。
🔴 12本目 r04 の送信文は**その commit の el_script** で作る（いまの辞書と混ぜない）。本線は読むだけ（git show / archive）。
"""
import io
import json
import os
import subprocess
import sys
import tarfile
import wave
from math import gcd
from pathlib import Path

import numpy as np
from scipy.signal import resample_poly

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out" / "phon"
R04 = "4ec4fd0"      # 12本目 r04 を焼いた commit（audio/opus は 1019899＝⑤a の音のまま）


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def to16k(x, sr):
    g = gcd(16000, sr)
    y = resample_poly(x.astype(np.float32), 16000 // g, sr // g)
    return np.clip(np.round(y), -32768, 32767).astype(np.int16)


def cut_rows(x, sr, rows, cid, wavs, texts, sent_of):
    for i, r in enumerate(rows, 1):
        lid = f"{cid}-{i}"
        a, b = int(round(r["t"] * sr)), int(round((r["t"] + r["d"]) * sr))
        seg = x[a:b]
        if len(seg) < sr * 0.2:
            raise SystemExit(f"🔴 {lid} の音が短すぎる（{len(seg) / sr:.2f}秒）")
        wavs[lid] = to16k(seg, sr)
        texts[lid] = {"text": r["text"], "sent": sent_of(lid, r["text"])}


def prep_ep13():
    sys.path.insert(0, str(ROOT / "tools"))
    import el_script as E
    nj = json.loads((ROOT / "audio" / "narration.json").read_text(encoding="utf-8"))
    by = {l.lid: l.text for l in E.lines()}

    def sent_of(lid, text):
        if by.get(lid) != text.strip():
            raise SystemExit(f"🔴 {lid}: narration.json の字幕と台本が違う（版ずれ）")
        return E.el_text(by[lid])

    wavs, texts = {}, {}
    for cid, rows in nj["subtitles"].items():
        with wave.open(str(ROOT / "audio" / f"{cid}.wav"), "rb") as w:
            sr = w.getframerate()
            x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
        dur = len(x) / sr
        if abs(dur - nj["durations"][cid]) > 0.02:
            raise SystemExit(f"🔴 {cid}: wav {dur:.3f}秒 ≠ narration.json {nj['durations'][cid]}秒（版ずれ）")
        cut_rows(x, sr, rows, cid, wavs, texts, sent_of)
    if len(wavs) != len(by):
        raise SystemExit(f"🔴 行の数が合わない: 音 {len(wavs)} ／ 台本 {len(by)}")
    return wavs, texts


def prep_ep13raw():
    """速さを上げる前の音（合成キャッシュの pcm＝TEMPO 1.0）。出荷する音で判定しきれない行を、ゆっくりの音でもう一度聞く。"""
    sys.path.insert(0, str(ROOT / "tools"))
    import el_script as E
    by = E.by_id()
    ids = E.resolve_ids(arg("--ids", ""))
    wavs, texts = {}, {}
    for lid in ids:
        t = by[lid].text
        sent = E.el_text(t)
        p = E.cache_path(sent)
        if not p.exists():
            raise SystemExit(f"🔴 {lid}: 合成キャッシュが無い（{p.name}）")
        x = np.frombuffer(p.read_bytes(), dtype=np.int16)
        wavs[lid] = to16k(x, 24000)
        texts[lid] = {"text": t, "sent": sent}
    return wavs, texts


def git_bytes(main, spec):
    return subprocess.run(["git", "-C", str(main), "show", spec], capture_output=True, check=True).stdout


def prep_ep12r04():
    main = Path(arg("--main", str(ROOT.parent / "zukai-engine")))
    src = OUT / "ep12r04_src"
    src.mkdir(parents=True, exist_ok=True)
    tar = subprocess.run(["git", "-C", str(main), "archive", R04, "tools"], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as tf:
        tf.extractall(src)
    nj = json.loads(git_bytes(main, f"{R04}:audio/narration.json").decode("utf-8"))
    code = ("import json,sys; sys.path.insert(0, r'%s'); import el_script as E; "
            "print(json.dumps({l.lid: [l.text, E.el_text(l.text)] for l in E.lines()}, ensure_ascii=False))"
            ) % (src / "tools")
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, cwd=str(src), env=env)
    if r.returncode:
        raise SystemExit("🔴 r04 の送信文を作れない:\n" + r.stderr.decode("utf-8", "replace")[-2000:])
    sent = json.loads(r.stdout.decode("utf-8").strip().splitlines()[-1])

    def sent_of(lid, text):
        t, s = sent.get(lid, [None, None])
        if t is None or t.strip() != text.strip():
            raise SystemExit(f"🔴 {lid}: r04 の字幕と、その commit の台本が違う")
        return s

    wavs, texts = {}, {}
    for cid, rows in nj["subtitles"].items():
        ob = git_bytes(main, f"{R04}:audio/opus/{cid}.opus")
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", "pipe:0", "-f", "s16le", "-ac", "1", "-ar", "24000",
                              "pipe:1"], input=ob, capture_output=True, check=True).stdout
        x, sr = np.frombuffer(pcm, dtype=np.int16), 24000
        dur = len(x) / sr
        if abs(dur - nj["durations"][cid]) > 0.06:
            print(f"⚠️ {cid}: opus {dur:.3f}秒 ／ narration.json {nj['durations'][cid]}秒")
        cut_rows(x, sr, rows, cid, wavs, texts, sent_of)
    return wavs, texts


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else ""
    if tag == "ep13":
        wavs, texts = prep_ep13()
    elif tag == "ep12r04":
        wavs, texts = prep_ep12r04()
    elif tag == "ep13raw":
        wavs, texts = prep_ep13raw()
    else:
        raise SystemExit("使い方: python qa_out/phon_prep.py ep13|ep12r04")
    OUT.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(OUT / f"{tag}_wav16.npz", **wavs)
    (OUT / f"{tag}_texts.json").write_text(json.dumps(texts, ensure_ascii=False, indent=0), encoding="utf-8")
    secs = sum(len(v) for v in wavs.values()) / 16000
    print(f"✓ {tag}: {len(wavs)}行・発話 {secs / 60:.1f}分 → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
