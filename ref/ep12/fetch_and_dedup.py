# -*- coding: utf-8 -*-
"""12本目②：段3を通った24点を落として、(a)同じ絵の重複を画素で潰し、(b)シートにする。

なぜ題名で重複を判定しないか
  → [[feedback-duplicate-art-needs-pixel-comparison]]
  『Castle Bravo nuclear test.jpg』『Castle Bravo (black and white).jpg』
  『Castle Bravo 005.jpg』『HD.10.290』は**どれも同じ火球の写真かもしれない**。
  題名も説明も違うので、名前では分からない。md5 と知覚ハッシュの両方で当たる。
  ⚠️ 平均差にしきい値を置いて機械で決め切らない。**最後は原寸で並べて目で決める**。
"""
import hashlib
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

UA = "zukai-engine-ep12/1.0 (research; konariri8@gmail.com)"
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "ref/ep12/img")
OUT.mkdir(parents=True, exist_ok=True)


def net3():
    """net4.py と同じ段1〜3を通す（同じ規則を2か所に書かないため import は使わない）。"""
    sys.path.insert(0, "ref/ep12")
    import net4
    rows = json.loads(Path("ref/ep12/commons_ep12.json").read_text(encoding="utf-8"))
    a = [r for r in rows if not net4.is_sa(r["license_short"])]
    a = [r for r in a if r["width"] >= 1280 and (r["bitdepth"] or 8) >= 8
         and r["mime"].startswith("image")]
    return [r for r in a if net4.year_of(r) == 1954]


def grab(r):
    name = r["title"][5:].replace("/", "_")
    p = OUT / name
    if not p.exists():
        url = ("https://commons.wikimedia.org/wiki/Special:FilePath/"
               + urllib.parse.quote(r["title"][5:].replace(" ", "_")))
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=180) as resp:
            p.write_bytes(resp.read())
        time.sleep(1.0)
    return p


def phash(p, n=16):
    """縮めて平均との大小で並べる知覚ハッシュ（回転・色調の違いを吸収）。"""
    im = Image.open(p).convert("L").resize((n, n), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float32)
    return (a > a.mean()).flatten()


def main():
    rows = net3()
    print("段3を通った %d 点を落とす\n" % len(rows))
    info = []
    for r in rows:
        try:
            p = grab(r)
        except Exception as e:
            print("🔴 落とせない %s (%s)" % (r["title"][5:][:50], str(e)[:40]))
            continue
        md5 = hashlib.md5(p.read_bytes()).hexdigest()
        info.append({"title": r["title"][5:], "path": str(p), "md5": md5,
                     "w": r["width"], "h": r["height"],
                     "ph": phash(p), "desc": r["desc"]})
        print("  %-60s %5dx%-5d %s" % (r["title"][5:][:60], r["width"], r["height"], md5[:8]))

    print("\n== md5 が同じ組 ==")
    seen = {}
    for x in info:
        seen.setdefault(x["md5"], []).append(x["title"])
    dup = {k: v for k, v in seen.items() if len(v) > 1}
    print(dup if dup else "  （無し）")

    print("\n== 知覚ハッシュが近い組（256ビット中の違い。小さいほど同じ絵）==")
    pairs = []
    for i in range(len(info)):
        for j in range(i + 1, len(info)):
            d = int(np.count_nonzero(info[i]["ph"] != info[j]["ph"]))
            pairs.append((d, info[i]["title"], info[j]["title"]))
    pairs.sort()
    for d, a, b in pairs[:12]:
        mark = "🔴 同じ絵の疑い" if d <= 40 else "  "
        print("%s %3d  %-42s ／ %s" % (mark, d, a[:42], b[:42]))
    print("\n⚠️ ここは当たりを付けただけ。採否は下のシートを目で見て決める。")

    # シート（2列×3行・1枚640px）
    info.sort(key=lambda x: -x["w"])
    for k in range(0, len(info), 6):
        chunk = info[k:k + 6]
        sheet = Image.new("RGB", (1280, 1080), (18, 18, 18))
        for i, x in enumerate(chunk):
            im = Image.open(x["path"]).convert("RGB")
            im.thumbnail((636, 336), Image.LANCZOS)
            box = Image.new("RGB", (640, 360), (18, 18, 18))
            box.paste(im, ((640 - im.width) // 2, (360 - im.height) // 2))
            d = ImageDraw.Draw(box)
            lab = "%d %s" % (k + i + 1, x["title"][:52])
            d.rectangle([0, 0, 640, 14], fill=(0, 0, 0))
            d.text((3, 2), lab, fill=(255, 220, 80))
            sheet.paste(box, ((i % 2) * 640, (i // 2) * 360))
        sp = OUT / ("sheet_%d.png" % (k // 6 + 1))
        sheet.save(sp)
        print("書いた %s（%d〜%d）" % (sp, k + 1, k + len(chunk)))

    Path("ref/ep12/commons24.json").write_text(
        json.dumps([{kk: vv for kk, vv in x.items() if kk != "ph"} for x in info],
                   ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
