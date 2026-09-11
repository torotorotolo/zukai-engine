# -*- coding: utf-8 -*-
"""⑥ 焼けた mp4 を「声の区間」と「声の無い区間（BGM だけ）」に分けてラウドネスで測る＋試写の時刻表（2026-09-11・キー橋）。

なぜ：`audio_mix` の自己申告は全体の LUFS 1つだけ。ナレと BGM の釣り合いは出ない。
      ローカルで audio_mix を回して素材ごとに測るのは 34 分ぶんの配列を数本持つので避け、
      **出荷する mp4 そのもの**を ffmpeg の ebur128 で 0.1 秒ごとに測って、時刻で振り分ける。

    python -u qa_out/kb_af_loud.py                         … 時刻表だけ（章の頭・全カットの頭を TSV へ）
    python -u qa_out/kb_af_loud.py <mp4> [--cuts=c520,c720] … ＋ラウドネスの分割

- 積み方は `audio_mix.main` / `build_jiko.build_full` と同じ＝`scene_jiko.CUTS` を順に足す。
  声の行＝カットの頭＋LEAD＋字幕の t 〜 +d
- M＝400ms 窓の瞬時ラウドネス。窓がまるごと声の行の内側なら「声」、まるごと外側なら「声なし」
- 「声なし」は声の終わりからの経過秒で分ける（サイドチェインの戻りが 1.10 秒＝直後は BGM がまだ下がっている）
- 心拍カットと衝撃音の直後 3 秒は「声なし」から外す（BGM 以外が鳴っている）
- 平均はエネルギー平均（10^(M/10) の平均）。−70 LUFS 未満は捨てる（R128 の絶対ゲートと同じ）
⚠️ ebur128 のログが読めなければ止める（0 で埋めない）
"""
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402

WIN = 0.4


def timeline():
    starts, spans, t = {}, [], 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        for r in S.SUBS.get(cid, []):
            a = t + S.LEAD + r["t"]
            spans.append((a, a + r["d"], cid))
        t += sec
    return starts, spans, t


def mmss(x):
    return f"{int(x // 60)}:{x % 60:04.1f}"


def emean(v):
    v = np.asarray([x for x in v if x > -70.0])
    return (float(10 * np.log10(np.mean(10 ** (v / 10)))), len(v)) if len(v) else (None, 0)


def loud(mp4, starts, spans, total):
    log = HERE / "qa_out" / (Path(mp4).stem + "_ebur128.txt")
    with open(log, "w", encoding="utf-8", errors="replace") as f:
        # ⚠️ framelog=verbose の 0.1 秒ごとの行は **-v verbose でないと出ない**（-v info だと Summary だけ＝M 0 行・09-11 実測）
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-v", "verbose", "-i", str(mp4), "-vn",
                            "-af", "ebur128=framelog=verbose:peak=true", "-f", "null", "-"],
                           stdout=f, stderr=subprocess.STDOUT)
    txt = log.read_text(encoding="utf-8", errors="replace")
    fr = re.findall(r"t:\s*([\d.]+)\s+TARGET:\S+ LUFS\s+M:\s*(-?[\d.]+|-inf).*?FTPK:\s*(-?[\d.]+|-inf)", txt)
    tail = txt[txt.rfind("Summary:"):] if "Summary:" in txt else ""
    I = re.search(r"I:\s*(-?[\d.]+) LUFS", tail)
    LRA = re.search(r"LRA:\s*([\d.]+) LU", tail)
    PK = re.search(r"Peak:\s*(-?[\d.]+|-inf) dBFS", tail)
    if r.returncode or not fr or not I:
        print(f"🔴 ebur128 が読めない（exit {r.returncode}・M {len(fr)} 行・Summary {'有' if I else '無'}）→ {log}")
        return 1
    print(f"ebur128 ログ → {log.relative_to(HERE)}（M {len(fr)} 行）")
    print(f"全体  I {I.group(1)} LUFS ／ LRA {LRA.group(1) if LRA else '?'} LU ／ True peak {PK.group(1) if PK else '?'} dBFS")
    # True peak（FTPK＝その 0.1 秒枠の真のピーク）が 0 dBFS を超えた枠と、そのカット
    order = sorted(starts.items(), key=lambda kv: kv[1])
    over = [(float(ts), float(pk)) for ts, _, pk in fr if pk != "-inf" and float(pk) > 0.0]
    by = {}
    for t, pk in over:
        cid = next((c for c, s in reversed(order) if s <= t), "?")
        by.setdefault(cid, []).append((t, pk))
    print(f"True peak が 0 dBFS を超えた 0.1秒枠 {len(over)} 個 ／ {len(by)} カット")
    for cid, v in sorted(by.items(), key=lambda kv: -max(p for _, p in kv[1]))[:12]:
        print(f"  {cid:<6} {len(v):3d} 枠  最大 {max(p for _, p in v):+.1f} dBFS  最初 {mmss(v[0][0])}")

    import audio_mix as A
    fx = [(starts[c], starts[c] + dict(S.CUTS)[c]) for c in getattr(A, "HEART_CUTS", ()) if c in starts]
    fx += [(starts[c] + off, starts[c] + off + 3.0) for c, off in getattr(A, "IMPACT_AT", {}).items() if c in starts]
    print(f"効果音の区間（声なしから外す）{len(fx)} 本")

    sa = np.array([s[0] for s in spans])
    sb = np.array([s[1] for s in spans])
    speech, quiet = [], {"0.0-0.5": [], "0.5-1.0": [], "1.0-2.0": [], "2.0+": []}
    for ts, ms, _ in fr:
        t1 = float(ts)
        t0 = t1 - WIN
        m = -120.0 if ms == "-inf" else float(ms)
        if t0 < 0 or t1 > total:
            continue
        inside = np.any((sa <= t0) & (sb >= t1))
        overlap = np.any((sa < t1) & (sb > t0))
        if inside:
            speech.append(m)
        elif not overlap:
            if any(a < t1 and b > t0 for a, b in fx):
                continue
            ended = sb[sb <= t0]
            since = t0 - ended.max() if len(ended) else 99.0
            k = "0.0-0.5" if since < 0.5 else "0.5-1.0" if since < 1.0 else "1.0-2.0" if since < 2.0 else "2.0+"
            quiet[k].append(m)
    v, n = emean(speech)
    print(f"声の区間      {v:6.1f} LUFS（窓 {n}）" if v is not None else "🔴 声の区間が0")
    for k, arr in quiet.items():
        q, nq = emean(arr)
        print(f"声なし {k:>7}秒 {q:6.1f} LUFS（窓 {nq}）" if q is not None else f"声なし {k:>7}秒  —（窓 0）")
    qa, _ = emean(sum(quiet.values(), []))
    if v is not None and qa is not None:
        print(f"声 − 声なし（全部） = {v - qa:.1f} LU")
    return 0


def main():
    starts, spans, total = timeline()
    print(f"カット {len(starts)} ／ 積んだ尺 {total:.2f}秒 = {mmss(total)}")
    tsv = HERE / "qa_out" / "kb_af_timeline.tsv"
    seen, rows = set(), []
    for cid, sec in S.CUTS:
        ch = S.CHAPTERS.get(cid[:2])
        name = f"{ch[0]}/{S.NCH} {ch[1]}" if ch else {"pr": "冒頭", "ep": "締め"}.get(cid[:2], cid[:2])
        rows.append(f"{cid}\t{mmss(starts[cid])}\t{starts[cid]:.2f}\t{sec:.2f}\t{name}")
        if name not in seen:
            seen.add(name)
            print(f"  {mmss(starts[cid]):>7}  {cid}  {name}")
    tsv.write_text("cid\tmm:ss\tstart\tsec\tchapter\n" + "\n".join(rows) + "\n", encoding="utf-8")
    print(f"全カットの頭 → {tsv.relative_to(HERE)}")
    want = next((a.split("=", 1)[1].split(",") for a in sys.argv[1:] if a.startswith("--cuts=")), [])
    for c in want:
        print(f"  {c}: {mmss(starts[c])}" if c in starts else f"  🔴 {c} は台本に無い")
    mp4 = next((a for a in sys.argv[1:] if not a.startswith("--")), None)
    return loud(mp4, starts, spans, total) if mp4 else 0


if __name__ == "__main__":
    sys.exit(main())
