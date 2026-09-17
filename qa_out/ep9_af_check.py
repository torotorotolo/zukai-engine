# -*- coding: utf-8 -*-
"""9本目 ⑥ 本編 mp4 の通し検品（機械でわかる分）を1本で出す。

  ① md5 ／ ② 映像と音の尺・コマ数（`scene_jiko.CUTS` の和と突合）／ ③ ラウドネス（ebur128）
  ④ 通しの6コマ（640×360 のシート1枚。指紋が一致しても合成の段で絵が崩れていないかの見張り）
  ⑤ 語りの無い区間が無音か → `qa_out/ep9_nobgm_gaps.py` を別に回す（重いので分けた）

    python qa_out/ep9_af_check.py out/jiko/titan_audio-ep9-r03.mp4 <シートの出力先.jpg>
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402

FPS = 30
SHEET = ["pr01", "c308", "c614", "c713", "ep03", "ep10"]   # 真ん中の秒を切り出す


def main():
    mp4, out = Path(sys.argv[1]), Path(sys.argv[2])
    h = hashlib.md5()
    with open(mp4, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    print(f"① md5 {h.hexdigest()} ／ {mp4.stat().st_size:,} バイト")

    r = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-show_entries",
                        "stream=codec_type,codec_name,width,height,r_frame_rate,duration,"
                        "nb_read_packets,sample_rate,channels", "-of", "json", str(mp4)],
                       capture_output=True, text=True)
    st = {s["codec_type"]: s for s in json.loads(r.stdout)["streams"]}
    v, a = st["video"], st["audio"]
    total = sum(s for _, s in S.CUTS)
    want = round(total * FPS)
    vd, ad = float(v["duration"]), float(a["duration"])
    print(f"② 映像 {v['codec_name']} {v['width']}×{v['height']} {v['r_frame_rate']} "
          f"{vd:.3f}秒 {int(v['nb_read_packets']):,}コマ（カットの和 {total:.3f}秒＝{want:,}コマ）")
    print(f"   音声 {a['codec_name']} {a['sample_rate']}Hz {a['channels']}ch {ad:.3f}秒 "
          f"／ 音ズレ {abs(vd - ad):.3f}秒")

    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-vn",
                        "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    summ = r.stderr[r.stderr.rfind("Summary:"):]
    val = {k: re.search(pat, summ) for k, pat in
           (("I", r"I:\s+(-?[\d.]+) LUFS"), ("LRA", r"LRA:\s+(-?[\d.]+) LU"),
            ("TP", r"Peak:\s+(-?[\d.]+) dBFS"))}
    if not all(val.values()):
        raise SystemExit("🔴 ebur128 の結果が読めない（fail closed）\n" + summ[-600:])
    print(f"③ 全体 {val['I'].group(1)} LUFS ／ LRA {val['LRA'].group(1)} LU ／ "
          f"True peak {val['TP'].group(1)} dBFS")

    from PIL import Image, ImageDraw, ImageFont
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = (t, sec)
        t += sec
    W, H = 640, 360
    sheet = Image.new("RGB", (W * 2, H * 3), "black")
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 22)
    tmp = out.with_suffix(".frame.png")
    for i, cid in enumerate(SHEET):
        t0, sec = starts[cid]
        at = t0 + sec / 2
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", str(mp4),
                        "-frames:v", "1", str(tmp)], check=True)
        im = Image.open(tmp).convert("RGB").resize((W, H), Image.LANCZOS)
        x, y = (i % 2) * W, (i // 2) * H
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + 250, y + 30], fill="black")
        d.text((x + 6, y + 2), f"{cid} {int(at // 60)}:{at % 60:04.1f}", font=font, fill="yellow")
    tmp.unlink(missing_ok=True)
    sheet.save(out, quality=88)
    print(f"④ 通しの6コマ → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
