# -*- coding: utf-8 -*-
"""25本目 ⑥：本編の mp4 の**字幕の全段**で、出るはずの行数と、本編のコマに出た行数を突き合わせる（24本目 `ep24_r01_subscan.py` の写し）。

なぜ：24本目の本編 r01 の c207 の2段目は、2行のはずが**1行目しか出ていなかった**（Modal の書き出しで2行目が抜けた・焼くたびに起きたり起きなかったり）。
     `tools/sub_layer_check.py` は 24本目の ⑥（e60a743b）で「行がまるごと無い」も測るようになったが、照合（`ep25_r01_vs_qa.py`）は
     1カットに静止画1枚＝そのカットの字幕1段しか見ない＝**本編のあとに字幕の全段を走査する**（記憶 feedback-whole-element-dropout-passes-partial-checks）。
測る：段ごとに、表示の真ん中の時刻のコマを原寸で1枚引き、字幕の帯（y900〜1080）の行の帯ごとに字の色の画素を数える。
     行の帯＝`scene_jiko.sub_ys`（56px：1行 基線 1000／2行 968・1044）の基線の 50px 上〜10px 下。字の色＝語り `SUB_COLOR`・聞き役 `SUB_Q_COLOR`。
     出るはずの行数＝`scene_jiko.wrap2`（描く道と同じ折り）。
⚠️ 見ないもの：字の形そのもの（化け）・行の一部の欠け（sub_layer_check と sub_center の担当）。

    python qa_out/ep25_r01_subscan.py [--mp4=titan_audio-ep25-r01.mp4]   → qa_out/ep25_r01/subscan.tsv と要約
    python qa_out/ep25_r01_subscan.py --selftest [--mp4=…]                … 陽性対照（2行目を消したコマ）・陰性対照
"""
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
MIN_INK = 500            # 1行ありと数える字の色の画素（4字の行でも 2,000 を超える）


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def ink(band, rgb):
    """字の色に近い画素（RGB の差の和が 120 未満）。"""
    d = np.abs(band.astype(np.int16) - np.array(rgb, np.int16)).sum(axis=2)
    return d < 120


def count_lines(band, rgb, ys):
    """band＝字幕の帯（180×1920×3）・ys＝行の基線（帯の上端から）→ 行ごとの字の色の画素の数。"""
    m = ink(band, rgb)
    return [int(m[max(0, int(y) - 50):int(y) + 10].sum()) for y in ys]


def grab(mp4, t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1",
                        "-vf", "crop=1920:180:0:900", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    if r.returncode or len(r.stdout) != 1920 * 180 * 3:
        return None
    return np.frombuffer(r.stdout, np.uint8).reshape(180, 1920, 3)


def plan():
    import scene_jiko as S
    card = getattr(S, "card_of", lambda _c: 0.0)
    rows, t = [], 0.0
    for cid, sec in S.CUTS:
        for i, r in enumerate(S.SUBS.get(cid, [])):
            n = len(S.wrap2(r["text"]))
            mid = t + S.LEAD + card(cid) + r["t"] + r["d"] / 2
            col = S.SUB_Q_COLOR if r.get("who") == "q" else S.SUB_COLOR
            rows.append((cid, i + 1, mid, n, hexrgb(col), r["text"]))
        t += sec
    return rows, S.sub_ys(1), S.sub_ys(2)


def mp4_of():
    return HERE / "out" / "jiko" / next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mp4=")),
                                        "titan_audio-ep25-r01.mp4")


def selftest():
    """陽性対照：2行の字幕のコマの2行目の帯を黒く塗る → 1行と数えるか。陰性対照：そのまま → 2行。"""
    rows, y1, y2 = plan()
    two = next(r for r in rows if r[3] == 2)
    b = grab(mp4_of(), two[2])
    neg = sum(c >= MIN_INK for c in count_lines(b, two[4], y2))
    cut = b.copy()
    cut[int(y2[1]) - 50:int(y2[1]) + 10] = 0
    pos = sum(c >= MIN_INK for c in count_lines(cut, two[4], y2))
    print(f"selftest {two[0]}-{two[1]}：そのまま {neg} 行（2 のはず）・2行目を消すと {pos} 行（1 のはず）")
    return neg == 2 and pos == 1


def main():
    if "--selftest" in sys.argv:
        return 0 if selftest() else 1
    mp4 = mp4_of()
    rows, y1, y2 = plan()
    out = HERE / "qa_out" / "ep25_r01" / "subscan.tsv"
    out.parent.mkdir(parents=True, exist_ok=True)
    bad, lines = [], ["cut\trow\tt_mp4\twant\tgot\tink"]
    for k, (cid, i, mid, n, rgb, text) in enumerate(rows):
        b = grab(mp4, mid)
        if b is None:
            bad.append((cid, i, mid, n, -1, "コマが取れない"))
            continue
        c = count_lines(b, rgb, y1 if n == 1 else y2)
        got = sum(x >= MIN_INK for x in c)
        lines.append(f"{cid}\t{i}\t{mid:.2f}\t{n}\t{got}\t{','.join(map(str, c))}")
        if got != n:
            bad.append((cid, i, mid, n, got, text))
        if (k + 1) % 100 == 0:
            print(f"  {k + 1}/{len(rows)}", flush=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"字幕の段 {len(rows)}（2行のはず {sum(r[3] == 2 for r in rows)}）・行の数が合わない {len(bad)}")
    for cid, i, mid, n, got, text in bad:
        print(f"  🔴 {cid}-{i}  {int(mid // 60)}:{mid % 60:05.2f}  出るはず {n} 行・出た {got} 行「{text}」")
    print(f"→ {out.relative_to(HERE)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
