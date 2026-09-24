# -*- coding: utf-8 -*-
"""13本目 ⑤a：**送信文字列に生の数字が残っていないか**を全行で数える（API 不使用・2026-09-24）。

  python qa_out/ep13_num_left.py            … 残った数字の行だけ出す（0行なら exit 0）
  python qa_out/ep13_num_left.py --sent     … 読み替わった行の「台本 → 送信」を全部出す（目で読む台帳）

12本目の `qa_out/ep12_num_left.py` を写し、行ごとに**位置の印**を足した（記憶 feedback-tts-misreads-are-positional）:
  [頭] 行の1字目から数が始まる ／ [尾] 数（＋助数詞）で行が終わる ／ [に][は] 助詞の直後に数が来る（5a-20）
🔴 なぜ要るか: EL_YOMI の境界規則は「漢字で終わる鍵は、直後が漢字なら当てない」。鍵が黙って当たらない所を
   **どんな数字でも**残れば落とす形で拾う（check_yomi_numbers の型の外も含む）。
⚠️ 漢数字（十分・一人・二つ など）は字として残るのが正しい語もあるので、ここでは数えない（--sent で目で見る）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as E  # noqa: E402

DIGIT = re.compile(r"[0-9０-９]+(?:[.．,，][0-9０-９]+)*")


def marks(sent, m):
    out = []
    if m.start() == 0:
        out.append("頭")
    rest = sent[m.end():]
    if re.fullmatch(r"[^\s、。]{0,4}[。」]?", rest):
        out.append("尾")
    if m.start() > 0 and sent[m.start() - 1] in "には":
        out.append(sent[m.start() - 1])
    return out


def main():
    bad, changed = [], []
    for l in E.lines():
        sent = E.el_text(l.text)
        if sent != l.text:
            changed.append((l.lid, l.text, sent))
        ms = list(DIGIT.finditer(sent))
        if ms:
            tags = []
            for m in ms:
                mk = marks(sent, m)
                tags.append(m.group(0) + (f"[{'・'.join(mk)}]" if mk else ""))
            bad.append((l.lid, sent, tags))
    if "--sent" in sys.argv:
        for lid, a, b in changed:
            print(f"{lid}\n   台本: {a}\n   送信: {b}")
        print(f"\n読み替わった行 {len(changed)}")
        return 0
    for lid, sent, tags in bad:
        print(f"{lid}  {' '.join(tags)}\n    {sent}")
    n = sum(len(t) for _, _, t in bad)
    print(f"\n送信文に生の数字が残る行 {len(bad)}（数 {n}）／読み替わった行 {len(changed)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
