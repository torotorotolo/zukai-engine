# -*- coding: utf-8 -*-
"""図解を作るときの入力を1か所から出す。`python tools/dump_script.py c1`

台本の文言の正本は `tools/narration.py` の SCRIPT、尺は `audio/narration.json`。
図を書く人（人でもエージェントでも）が、この2つを別々に読んで食い違うのを防ぐ。
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent


def main(prefix):
    d = json.loads((HERE / "audio" / "narration.json").read_text(encoding="utf-8"))
    dur, subs = d["durations"], d["subtitles"]
    ids = [k for k in dur if k.startswith(prefix)]
    tot = sum(dur[k] for k in ids)
    print(f"# {prefix}: {len(ids)}カット／発話 {tot:.1f}秒"
          f"（完成尺 {tot + len(ids) * 0.85:.1f}秒）\n")
    for k in ids:
        rows = subs[k]
        print(f'{k}  尺{dur[k] + 0.85:.1f}秒  段は{len(rows)}個が既定')
        for i, r in enumerate(rows, 1):
            print(f'   {i}: {r["text"]}')
        print()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "pr")
