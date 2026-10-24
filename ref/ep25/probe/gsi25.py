# -*- coding: utf-8 -*-
"""25本目②：国土地理院の年代別の写真タイルを同じ範囲で並べる（曲線の付け替え〈1996-12〉の前と後を見るため）。
z と中心の緯度経度から N×N のタイルを取り、1枚につなぐ。出力は src/gsi/（git の外）。
使い方: python gsi25.py <出力フォルダ> <緯度> <経度> <z> <N> <層,層,...>
  層＝seamlessphoto（全国最新写真）・airphoto（簡易空中写真 2004年〜）・gazo3（1984〜86）・gazo1（1974〜78）・ort_old10（1961〜69）"""
import math, os, sys, time, urllib.request, urllib.error
from io import BytesIO

from PIL import Image

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) zukai-engine research"
EXT = {"seamlessphoto": "jpg", "airphoto": "png", "gazo3": "jpg", "gazo1": "jpg", "ort_old10": "png", "ort": "jpg"}


def tile(lat, lon, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    la = math.radians(lat)
    y = (1 - math.log(math.tan(la) + 1 / math.cos(la)) / math.pi) / 2 * n
    return x, y


def main():
    outdir, lat, lon, z, N = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    layers = sys.argv[6].split(",")
    os.makedirs(outdir, exist_ok=True)
    fx, fy = tile(lat, lon, z)
    x0, y0 = int(fx - N / 2 + 0.5), int(fy - N / 2 + 0.5)
    log = []
    for L in layers:
        mos = Image.new("RGB", (256 * N, 256 * N), (128, 128, 128))
        got = 0
        for j in range(N):
            for i in range(N):
                url = f"https://cyberjapandata.gsi.go.jp/xyz/{L}/{z}/{x0 + i}/{y0 + j}.{EXT[L]}"
                try:
                    req = urllib.request.Request(url, headers={"User-Agent": UA})
                    with urllib.request.urlopen(req, timeout=60) as r:
                        b = r.read()
                    mos.paste(Image.open(BytesIO(b)).convert("RGB"), (256 * i, 256 * j))
                    got += 1
                except urllib.error.HTTPError as e:
                    log.append(f"{L} {x0 + i}/{y0 + j} http{e.code}")
                time.sleep(0.3)
        fn = os.path.join(outdir, f"gsi_{L}_z{z}_x{x0}_y{y0}_{N}x{N}.png")
        mos.save(fn)
        # 中心の点（指定の緯度経度）の画素の位置
        px, py = (fx - x0) * 256, (fy - y0) * 256
        log.append(f"{L}: {got}/{N * N} tiles -> {fn}  center_px=({px:.0f},{py:.0f})")
        print(log[-1], flush=True)
    open(os.path.join(outdir, "gsi_log.txt"), "a", encoding="utf-8").write("\n".join(log) + "\n")


if __name__ == "__main__":
    main()
