# -*- coding: utf-8 -*-
"""27本目 ⑥（26本目 `ep26_r01_vs_qa.py` の写し・回の名前だけ直した＝照らす元は ⑤c' 周2 `qa_ep27_c2` と ⑤c `qa_ep27_c`）。
26本目 ⑥：本編（Modal）の mp4 のコマを、検品で見た静止画と画素で照らす（25本目 `ep25_r01_vs_qa.py` の写し・ルール 6-62）。

なぜ：NOAA 2003 の写真（courtesy・c826・c903）の出典の行は Actions では仮の字「〇〇〇」・Modal では作者欄の名前
     ＝その2カットは出典の行だけ必ず違う（局所の差に出る＝原寸で見る）。地図4カット（c218・c306・c909・c917）は
     Actions で焼けない＝⑤b-3 の Modal の qa の焼き（`qa-ep26_b3_map`・版 d0b15118＝描く側の差分なし）と照らす。
     ＝**出荷する mp4 のコマ**が**見た静止画**と同じかを全カットで測る。
照らす元：--qa=名1,名2,…（out/jiko の下のフォルダ・先に見つかった物を使う）＝⑤c' 周2 の組（`qa_ep26_c2_dl`＝版 3dc05235・231＋ed01＋扉10）。
窓：カット全体。章の扉＝card_<cid>.png を扉の区間（S.card_of）で照らす。
差：全体の平均（MAD）と、16×16 の升目ごとの平均の最大（局所＝字や札の違いを拾う）。
⚠️ JPEG（静止画）と H.264（mp4）の圧縮の揺れで 0 にはならない＝外れたカットだけを原寸で見る。

    python qa_out/ep27_r01_vs_qa.py --dump-win
    python qa_out/ep27_r01_vs_qa.py --mp4=titan_audio-ep27-r01.mp4 --qa=qa_ep26_c2_dl,qa-ep26_b3_map
      → qa_out/ep27_r01/vs_qa.tsv と要約
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

JIKO = HERE / "out" / "jiko"
W, H, FPS = 320, 180, 30
WIN = HERE / "qa_out" / "ep27_r01" / "windows.json"


def dump_windows():
    """⚠️ メモリ（コミットの空き）：設計の表（scene_jiko）は別のプロセスで読んで、カットの秒と扉の秒だけを書き出す。
    照合のプロセスは表を読まない＝`--dump-win` を先に1回。"""
    import scene_jiko as S
    WIN.parent.mkdir(parents=True, exist_ok=True)
    WIN.write_text(json.dumps([[cid, sec, S.card_of(cid)] for cid, sec in S.CUTS]), encoding="utf-8")
    print(f"→ {WIN}（{len(S.CUTS)} カット）")


def arg(k, d=""):
    return next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith(f"--{k}=")), d)


def small(p):
    # ⚠️ uint8 で持つ（float32 だと 249枚で約172MB＝22本目 10-15 の1回目は ffmpeg が「Cannot allocate memory」で8コマで止まった）
    with Image.open(p) as im:
        return np.asarray(im.convert("RGB").resize((W, H), Image.BILINEAR), np.uint8)


def blockmax(d):
    """16×16 の升目ごとの平均の最大（局所の違い）。"""
    hh, ww = (H // 16) * 16, (W // 16) * 16
    b = d[:hh, :ww].reshape(hh // 16, 16, ww // 16, 16).mean(axis=(1, 3))
    return float(b.max())


def find(dirs, name):
    for d in dirs:
        p = JIKO / d / name
        if p.exists():
            return d, p
    return None, None


def main():
    if "--dump-win" in sys.argv:
        dump_windows()
        return 0
    if not WIN.exists():
        print(f"🔴 {WIN} が無い＝先に --dump-win")
        return 1
    mp4 = JIKO / arg("mp4", "titan_audio-ep27-r01.mp4")
    dirs = [d for d in arg("qa").split(",") if d]
    out = HERE / "qa_out" / "ep27_r01" / arg("out", "vs_qa.tsv")
    out.parent.mkdir(parents=True, exist_ok=True)
    if not mp4.exists() or not dirs:
        print(f"🔴 mp4 か --qa が無い（{mp4}・{dirs}）")
        return 1
    win, src, miss, t = {}, {}, [], 0.0
    for cid, sec, off in json.loads(WIN.read_text(encoding="utf-8")):
        if off > 0:
            d, p = find(dirs, f"card_{cid}.png")
            if p:
                win[f"card_{cid}"] = (t + 0.05, t + off - 0.05, small(p))
                src[f"card_{cid}"] = d
            else:
                miss.append(f"card_{cid}")
        d, p = find(dirs, f"cut_{cid}.jpg")
        if p:
            win[cid] = (t + off, t + sec - 0.02, small(p))
            src[cid] = d
        else:
            miss.append(cid)
        t += sec
    print(f"静止画 {len(win)} 枚（扉を含む）／ 設計の尺 {t:.2f}秒 ／ 照らす元が無い {len(miss)}：{' '.join(miss) or 'なし'}", flush=True)
    for d in dirs:
        print(f"  {d}: {sum(1 for v in src.values() if v == d)} 枚", flush=True)
    best = {c: (1e9, 0.0, 0.0) for c in win}
    order = sorted(win.items(), key=lambda kv: kv[1][0])
    cmd = ["ffmpeg", "-v", "error", "-threads", "2", "-i", str(mp4), "-vf", f"scale={W}:{H}:flags=bilinear",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n, fb, act, oi = 0, W * H * 3, [], 0
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
            fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.int16)
            for cid, (a, b, ref) in act:
                d = np.abs(fr - ref.astype(np.int16)).mean(axis=2)
                mad = float(d.mean())
                if mad < best[cid][0]:
                    best[cid] = (mad, ts, blockmax(d))
        n += 1
        if n % 18000 == 0:
            print(f"  {n} コマ（{ts / 60:.1f}分）", flush=True)
    pr.wait()
    print(f"読んだコマ {n}（{n / FPS:.2f}秒）", flush=True)
    # 🔴 読めたコマが足りなければ止める（fail closed）。22本目 10-15 の1回目は8コマで終わり、MAD 10億の表を「結果」として書いた
    if pr.returncode or n < round(t * FPS) * 0.99:
        print(f"🔴 mp4 を読み切れていない（{n} コマ／設計 {round(t * FPS)}・ffmpeg {pr.returncode}）＝照合は無効。表は書かない")
        return 1
    rows = sorted(((c,) + v for c, v in best.items()), key=lambda r: -r[3])
    with out.open("w", encoding="utf-8") as f:
        f.write("cut\tmad\tt_mp4\tblock_max\tqa\n")
        for c, mad, ts, bm in rows:
            f.write(f"{c}\t{mad:.2f}\t{ts:.3f}\t{bm:.1f}\t{src[c]}\n")
    mads = np.array([r[1] for r in rows])
    bms = np.array([r[3] for r in rows])
    print(f"MAD 中央値 {np.median(mads):.2f}・最大 {mads.max():.2f}／局所の最大 中央値 {np.median(bms):.1f}・最大 {bms.max():.1f}")
    print("局所の差が大きい順 40:")
    for c, mad, ts, bm in rows[:40]:
        print(f"  {c:11s} MAD {mad:5.2f}  局所 {bm:5.1f}  mp4 {int(ts // 60)}:{ts % 60:05.2f}  {src[c]}")
    print(f"→ {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
