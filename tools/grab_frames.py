# -*- coding: utf-8 -*-
"""ブラウザのcanvasから吐いた base64 を画像ファイルに戻す。

javascript_tool の戻り値が大きいと tool-results のテキストに落ちるので、そこから復元する。
  python tools/grab_frames.py <tool-results.txt> <出力名.jpg>
"""
import base64
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

src, out = Path(sys.argv[1]), Path(sys.argv[2])
raw = src.read_text(encoding="utf-8")
try:
    txt = "".join(x["text"] for x in json.loads(raw))
except Exception:
    txt = raw
txt = re.sub(r"[^A-Za-z0-9+/=]", "", re.sub(r"^.*base64,", "", txt.strip().strip('"')))
out.parent.mkdir(parents=True, exist_ok=True)
out.write_bytes(base64.b64decode(txt + "=="))
print(out, out.stat().st_size, "bytes")
