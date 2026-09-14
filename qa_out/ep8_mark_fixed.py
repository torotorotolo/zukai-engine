# -*- coding: utf-8 -*-
"""④' で直したカットの見出しに 🔧 を付ける。
⚠️ 付ける前に「そのカットが実在するか」を全件見て、1つでも無ければ1件も付けない（fail closed）。
⚠️ すでに 🔧 が付いている見出しは二重に付けない。
"""
import io
import re
import sys

PATH = r"C:\Users\konar\Documents\Obsidian Vault\Projects\事故検証-コロンビア号-台本第2版-20260914.md"

FIXED = [
    "pr05", "pr06", "c112", "c117", "c201", "c218", "c315", "c401", "c407", "c413",
    "c417", "c419", "c508", "c705", "c713", "c722", "c725", "c729", "c808",
    "c810", "c901", "c907",
]

HDR = re.compile(r"^\*\*([a-z]{1,2}\d{2,3})\*\*(\s*)(🔧\s*)?(／.*)$")

raw = io.open(PATH, encoding="utf-8").read().split("\n")
found = {}
for i, line in enumerate(raw):
    m = HDR.match(line)
    if m:
        found[m.group(1)] = i

missing = [c for c in FIXED if c not in found]
if missing:
    print("🔴 見出しが見つからないので1件も付けていません: %s" % " ".join(missing))
    sys.exit(1)

n = 0
for cid in FIXED:
    i = found[cid]
    m = HDR.match(raw[i])
    if m.group(3):
        continue
    raw[i] = "**%s** 🔧 %s" % (cid, m.group(4))
    n += 1

io.open(PATH, "w", encoding="utf-8").write("\n".join(raw))
print("🔧 を付けた: %d件 / 指定 %d件" % (n, len(FIXED)))
