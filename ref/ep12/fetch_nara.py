# -*- coding: utf-8 -*-
"""12本目⑤b：NARA のキャッスル作戦の写真51点（`nara_sizes.json`）を手元に落とす。

2026-09-23 カズヤくんの許可のうえで実行（④'までは題名しか見ていない＝絵と人の顔を⑤bで見るため）。
置き場＝`ref/ep12/img/nara/<naId>.jpg`（`ref/ep12/img/` は .gitignore＝git に入らない）。

⚠️ 落としかけのファイルを測らない（記憶 feedback-download-size-is-not-completion）：
   ① `.part` に書いてから名前を変える ② Content-Length と実バイト数を突き合わせる
   ③ PIL で開いて、`nara_sizes.json` に測ってある縦横と一致するかを見る。どれか外れたら「NG」と出して残す。

    python ref/ep12/fetch_nara.py            # 無いものだけ落とす（何度回してもよい）
"""
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
DST = HERE / "img" / "nara"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def check(p, it):
    try:
        with Image.open(p) as im:
            ok = im.size == (it["w"], it["h"])
            return ok, im.size
    except Exception as e:
        return False, repr(e)[:80]


def main():
    DST.mkdir(parents=True, exist_ok=True)
    items = json.loads((HERE / "nara_sizes.json").read_text(encoding="utf-8"))
    rows, bad = [], 0
    for i, it in enumerate(items, 1):
        p = DST / f"{it['naId']}.jpg"
        if not (p.exists() and check(p, it)[0]):
            for attempt in range(3):
                try:
                    req = urllib.request.Request(it["url"], headers={"User-Agent": UA})
                    with urllib.request.urlopen(req, timeout=180) as r:
                        want = int(r.headers.get("Content-Length") or -1)
                        data = r.read()
                    if want >= 0 and len(data) != want:
                        raise IOError(f"short read {len(data)}/{want}")
                    tmp = p.with_suffix(".part")
                    tmp.write_bytes(data)
                    tmp.replace(p)
                    break
                except Exception as e:
                    print(f"  retry {attempt + 1} {it['naId']}: {e!r}"[:160], flush=True)
                    time.sleep(5 * (attempt + 1))
            time.sleep(1.0)
        ok, size = check(p, it) if p.exists() else (False, "missing")
        md5 = hashlib.md5(p.read_bytes()).hexdigest() if p.exists() else "-"
        nb = p.stat().st_size if p.exists() else 0
        bad += 0 if ok else 1
        rows.append(f"{it['naId']}\t{nb}\t{md5}\t{'OK' if ok else 'NG ' + str(size)}\t{it['scope']}")
        print(f"{i:2d}/{len(items)} {'OK' if ok else 'NG'} {nb/1e6:6.2f}MB {it['naId']} {it['scope'][:60]}",
              flush=True)
    (DST / "index.tsv").write_text("naId\tbytes\tmd5\tcheck\tscope\n" + "\n".join(rows) + "\n",
                                   encoding="utf-8")
    tot = sum(int(r.split("\t")[1]) for r in rows)
    print(f"== {len(rows)} 点・NG {bad}・計 {tot/1e6:.1f}MB → {DST / 'index.tsv'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
