# -*- coding: utf-8 -*-
"""12本目②：NARA の写真の**実寸**を測る（API の byteSize が 0 で返るため）。

⚠️ 「点数がある」は「全画面に使える」ではない。網の2段目（大きさ）は
   配信物の寸法ではなく**原本の画素**で測る → [[feedback-inventory-is-not-usable-material]]
   8本目は TWA800 の NTSB 写真 2,009点が **640x480** で全滅した。

測り方：先頭の数十KBだけ落として PIL に寸法を読ませる（全部は落とさない）。
"""
import io
import json
import sys
import time
from pathlib import Path

import requests
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

UA = ("zukai-engine/1.0 (accident-documentary research; "
      "https://github.com/torotorotolo/zukai-engine; konariri8@gmail.com)")


def size_of(url):
    """頭だけ読んで寸法を返す。読めなければ落とす（0で埋めない）。"""
    try:
        r = requests.get(url, headers={"User-Agent": UA, "Range": "bytes=0-262143"},
                         timeout=60)
        if r.status_code not in (200, 206):
            return None, "HTTP %s" % r.status_code
        im = Image.open(io.BytesIO(r.content))
        return (im.width, im.height), im.mode
    except Exception as e:
        return None, str(e)[:40]


def main():
    rows = []
    for f in sys.argv[1:]:
        rows += json.load(open(f, encoding="utf-8"))
    print("測る %d 点\n" % len(rows))
    ok = big = 0
    out = []
    for r in rows:
        objs = r.get("objects") or []
        if not objs:
            print("%-9s 物なし %s" % (r["naId"], r["title"][:50]))
            continue
        u = objs[0].get("url")
        wh, mode = size_of(u)
        if wh is None:
            print("🔴 %-9s 読めない（%s） %s" % (r["naId"], mode, (r["scope"] or "")[:40]))
        else:
            ok += 1
            if wh[0] >= 1280:
                big += 1
            print("%-9s %5dx%-5d %-4s %s"
                  % (r["naId"], wh[0], wh[1], mode, (r["scope"] or r["title"])[:70]))
        out.append({"naId": r["naId"], "scope": r["scope"], "url": u,
                    "w": wh[0] if wh else None, "h": wh[1] if wh else None,
                    "mode": mode})
        time.sleep(0.3)
    print("\n寸法が読めた %d / %d ・ 幅1280以上 **%d点**" % (ok, len(rows), big))
    Path("ref/ep12/nara_sizes.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
