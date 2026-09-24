# -*- coding: utf-8 -*-
"""音素の網（再発防止策1の試作）── 直した行だけを確かめる（API 不使用・2026-09-24）。

  python qa_out/phon_verify.py ep13 c101-1,c303-1,…     … 行ごとに「読みの食い違い（雑音の型を除く）」「句読点の無い所の間」を出す

合否の目安（13本目 ⑤a' で決めた・人が最後に読む）:
  ✗ 読み … 雑音の型（phon_review.benign）でない食い違い。ただし鼻濁音（g→n）・「ドア」の w・pyopenjtalk の読み違いは人が外す
  ✗ 間   … 句読点の無い所で 0.30秒以上（数の前後は 0.20秒以上）。「は・が・も」の直後は 0.45秒以上だけ
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phon_check as P  # noqa: E402
import phon_review as V  # noqa: E402

NUM = re.compile(r"[0-9一二三四五六七八九十百千万]|^(いっ|いち|にじゅう|さん|よん|ご|ろく|ろっ|なな|しち|はち|はっ|きゅう|じゅう|じゅっ|ひゃく|せん|まん)"
                 r"|(ねん|がつ|にち|じ|ふん|ぷん|びょう|にん|びん)$")


def main():
    tag = sys.argv[1]
    ids = [x for x in sys.argv[2].split(",") if x]
    rows = {r["lid"]: r for r in P.analyse(tag)}
    bad_lines = 0
    for lid in ids:
        r = rows[lid]
        out = []
        for h in r["bad"]:
            if V.benign(h, r):
                continue
            g = min((r["tg"].get(i, 0.0) for i in h["tok"]), default=0.0)
            out.append(f"読み「{P.surf(r, h['tok'])}」{h['exp'] or '∅'}→{h['rec'] or '∅'}{('[' + h['pos'] + ']') if h['pos'] else ''} GOP{g:.1f}")
        for p in r["pauses"]:
            if p[3] == "句読点":
                continue
            a, b = V.ctx(r, p[2]).split("｜")
            if a == b:
                continue
            num = bool(NUM.search(a) or NUM.search(b))
            lim = 0.45 if a in ("は", "が", "も") else (0.20 if num else 0.30)
            if p[1] >= lim:
                out.append(f"間「{a}｜{b}」{p[1]:.2f}s")
        mark = "✗" if out else "✓"
        bad_lines += bool(out)
        print(f"{mark} {lid}  " + ("／".join(out) if out else "") + f"\n    {r['sent']}")
    print(f"\n確かめた {len(ids)}行／所見のある行 {bad_lines}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
