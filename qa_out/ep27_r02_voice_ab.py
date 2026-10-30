# -*- coding: utf-8 -*-
"""27本目 ⑥'：試写で聞き比べる「声の A/B」を作る（いまの音／2〜4kHz を下げた音・聞こえの大きさをそろえる）。28本目 ⑤a の直しの材料。

なぜ：競合3本（ゆっくり事故検証・ゆっくり暗闇の事件簿・おしえて!オカルト先生）と同じ物差しで比べると、うちの声は 2〜4kHz（全体に対する dB）
     だけが 3.4〜4.2dB 強い（`qa_out/ep27_r02/voiceq_rivals.tsv`）。下げると「耳が痛い」が和らぐかは**耳でしか決まらない**＝試写で聞く。
     ⚠️ 大きい方が良く（悪く）聞こえるので、B は聞こえの大きさ（ebur128 の I）を A にそろえる（差 0.1 LU 以内）。
作るもの（out/jiko/ep27_voice_ab/＝git の外）：A＝本編の区間そのまま／B＝`equalizer=f=3000:t=o:w=1:g=-4`（3kHz を中心に1オクターブ幅で −4dB）
     ＝本編 r01 の 5:00〜6:00 で 2〜4kHz が −13.6 → −16.4dB（競合 −16.8〜−17.6）。AAC 192k・モノラル（本編と同じ）

    python -P qa_out/ep27_r02_voice_ab.py <mp4> [--ss=300] [--t=30] [--eq=equalizer=f=3000:t=o:w=1:g=-4]
"""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
OUT = HERE / "out" / "jiko" / "ep27_voice_ab"


def opt(name, default):
    return next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith(f"--{name}=")), default)


def lufs(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.findall(r"I:\s+(-?\d+(?:\.\d+)?) LUFS", r.stderr)
    if not m:
        raise SystemExit(f"🔴 ebur128 の I が読めない: {path}（読めないのに通さない）")
    return float(m[-1])


def make(src, ss, t, af, dst):
    args = ["ffmpeg", "-v", "error", "-y", "-ss", ss, "-t", t, "-i", str(src), "-vn", "-ac", "1", "-ar", "44100"]
    if af:
        args += ["-af", af]
    subprocess.run(args + ["-c:a", "aac", "-b:a", "192k", str(dst)], check=True)


def main():
    mp4 = Path(next(a for a in sys.argv[1:] if not a.startswith("--")))
    ss, t, eq = opt("ss", "300"), opt("t", "30"), opt("eq", "equalizer=f=3000:t=o:w=1:g=-4")
    OUT.mkdir(parents=True, exist_ok=True)
    a = OUT / "27本目_声A_いま.m4a"
    b = OUT / "27本目_声B_2〜4kHzを下げた.m4a"
    make(mp4, ss, t, "", a)
    la = lufs(a)
    make(mp4, ss, t, eq, b)
    lb = lufs(b)
    gain = la - lb
    make(mp4, ss, t, f"{eq},volume={gain:+.2f}dB", b)          # 聞こえの大きさを A にそろえる
    lb2 = lufs(b)
    if abs(lb2 - la) > 0.1:
        raise SystemExit(f"🔴 B の聞こえの大きさが A とそろわない（A {la:.1f}・B {lb2:.1f} LUFS）")
    print(f"A {a.name}：{la:.1f} LUFS（{mp4.name} の {ss}秒から {t}秒・そのまま）")
    print(f"B {b.name}：{lb2:.1f} LUFS（{eq}・利得 {gain:+.2f}dB で A にそろえた）")
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
