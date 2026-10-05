# -*- coding: utf-8 -*-
"""18本目 ⑥：本番 r01（Modal）の mp4 を、検品の焼き `ep18_c3fix`（Actions・同じ版 f8f92f2）の静止画 243 枚と画素で照らす。

なぜ：★全体の指紋が Actions（bf89fcfe…）と Modal（7cbfc052…）で合わなかった（層 1,327 枚・74.2MB・代表 28 層の md5 は
     すべて一致）＝14本目 r02 と同じ型（ルール 6-62「本番の mp4 を直接測って決着」）。層を比べる手段は無い
     （Modal の層は残らない）ので、**出荷する mp4 のコマ**が**見た静止画**と同じかを全カットで測る。

やり方：mp4 を頭から 320×180 で読み流し、カットごとに「静止画を撮った時刻の 0.5 秒前〜カットの終わり」の窓の中で、
       静止画（同じ大きさに縮めた）との差がいちばん小さいコマを探す。差は全体の平均（MAD）と、
       16×16 の升目ごとの平均の最大（局所＝字や札の違いを拾う）の2つ。
⚠️ JPEG（静止画）と H.264（mp4）の圧縮の揺れがあるので 0 にはならない。外れたカットだけを原寸で見る。

    python qa_out/ep18_r01_vs_qa.py      → qa_out/ep18_r01_vs_qa.tsv と要約
"""
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import scene_jiko as S  # noqa: E402

MP4 = HERE / "out" / "jiko" / "titan_audio-ep18-r01.mp4"
QA = HERE / "out" / "jiko" / "qa_ep18_c3fix"
OUT = HERE / "qa_out" / "ep18_r01_vs_qa.tsv"
W, H, FPS = 320, 180, 30


def shot_at(cid, sec, at=0.92):
    """build_jiko.qa_shots の時刻（保持段の分は窓をカットの終わりまで取って吸収する）。"""
    rows = S.SUBS.get(cid)
    if not rows:
        return sec * at
    last = rows[-1]
    full_until = last["t"] + last["d"] + S.LEAD + 0.12 - 0.14
    return max(min(sec * at, full_until), min(sec * 0.70, full_until))


def small(p):
    im = Image.open(p).convert("RGB").resize((W, H), Image.BILINEAR)
    return np.asarray(im, np.float32)


def blockmax(d):
    """16×16 の升目ごとの平均の最大（局所の違い）。"""
    hh, ww = (H // 16) * 16, (W // 16) * 16
    b = d[:hh, :ww].reshape(hh // 16, 16, ww // 16, 16).mean(axis=(1, 3))
    return float(b.max())


def main():
    win, t = {}, 0.0
    for cid, sec in S.CUTS:
        off = S.card_of(cid)
        p = QA / f"cut_{cid}.jpg"
        if p.exists():
            t0 = t + off + shot_at(cid, sec - off)
            win[cid] = (max(t, t0 - 0.5), t + sec - 0.02, small(p))
        t += sec
    print(f"静止画 {len(win)} 枚 ／ 設計の尺 {t:.2f}秒", flush=True)
    best = {c: (1e9, 0.0, 0.0) for c in win}
    order = sorted(win.items(), key=lambda kv: kv[1][0])
    cmd = ["ffmpeg", "-v", "error", "-i", str(MP4), "-vf", f"scale={W}:{H}:flags=bilinear",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n, fb = 0, W * H * 3
    act = []
    oi = 0
    while True:
        buf = pr.stdout.read(fb)
        if len(buf) < fb:
            break
        ts = n / FPS
        while oi < len(order) and order[oi][1][0] <= ts:
            act.append(order[oi])
            oi += 1
        act = [kv for kv in act if kv[1][1] >= ts]
        if act:
            fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
            for cid, (a, b, ref) in act:
                d = np.abs(fr - ref).mean(axis=2)
                mad = float(d.mean())
                if mad < best[cid][0]:
                    best[cid] = (mad, ts, blockmax(d))
        n += 1
        if n % 9000 == 0:
            print(f"  {n} コマ（{ts / 60:.1f}分）", flush=True)
    pr.wait()
    print(f"読んだコマ {n}（{n / FPS:.2f}秒）", flush=True)
    rows = sorted(((c,) + v for c, v in best.items()), key=lambda r: -r[3])
    with OUT.open("w", encoding="utf-8") as f:
        f.write("cut\tmad\tt_mp4\tblock_max\n")
        for c, mad, ts, bm in rows:
            f.write(f"{c}\t{mad:.2f}\t{ts:.3f}\t{bm:.1f}\n")
    mads = np.array([r[1] for r in rows])
    bms = np.array([r[3] for r in rows])
    print(f"MAD 中央値 {np.median(mads):.2f}・最大 {mads.max():.2f}／局所の最大 中央値 {np.median(bms):.1f}・最大 {bms.max():.1f}")
    print("局所の差が大きい順 12:")
    for c, mad, ts, bm in rows[:12]:
        print(f"  {c:6s} MAD {mad:5.2f}  局所 {bm:5.1f}  mp4 {int(ts // 60)}:{ts % 60:05.2f}")
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()
