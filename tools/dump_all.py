# -*- coding: utf-8 -*-
"""1カット＝1ブロックで「聞こえる文」と「見える文字」を全部並べる。

原文照合（人・エージェント）の入力にする。check_dup.collect() が
**実際に描かれる SVG から** 文字を拾うので、型の中で自動生成される
凡例・単位・注記まで漏れなく出る（SPEC を読むだけでは出ない）。

    python tools/dump_all.py            # 全カット
    python tools/dump_all.py c1         # 章で絞る
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import check_dup as D
import scene_jiko as S

HERE = Path(__file__).parent.parent


def main(only=None):
    d = json.loads((HERE / "audio" / "narration.json").read_text(encoding="utf-8"))
    dur, subs = d["durations"], d["subtitles"]
    bycut = D.collect(only)

    ids = [k for k in dur if not only or k.startswith(only)]
    print(f"# {len(ids)}カット\n")
    for cid in ids:
        spec = S.SPEC.get(cid, {})
        kind = spec.get("fig", ("photo",))[0] if spec.get("fig") else "photo"
        photo = spec.get("photo")
        head = f"===== {cid}  [{kind}]"
        if photo:
            head += f"  写真={photo}"
        print(head + f"  尺{dur[cid] + 0.85:.1f}秒")

        print("-- 聞こえる文（ナレーション／字幕）")
        for i, r in enumerate(subs[cid], 1):
            print(f"   {i}: {r['text']}")

        print("-- 見える文字（描画される全レイヤー）")
        seen = []
        for _lay, t in bycut.get(cid, []):
            if t not in seen:
                seen.append(t)
        for t in seen:
            print(f"   | {t}")
        print()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
