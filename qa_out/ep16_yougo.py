# -*- coding: utf-8 -*-
r"""ep16_yougo.py — 概要欄に載せる用語の下書きを、**本文で裏を取りながら**作る物差し（16本目・2026-10-02 ⑥）。

  python qa_out/ep16_yougo.py         … 候補語ごとに「本文に何行出るか・初出カット・初出行の全文」
  python qa_out/ep16_yougo.py --spec  … ref/ep16/yougo.md の「貼る本文」に並ぶ語を、同じ目で検算

15本目の `qa_out/ep15_yougo.py` を写した（変えたのは候補語と md の場所だけ）。
🔴 なぜ要るか（feedback-jiko-description-glossary の「下書きが必ず外す3つの型」）:
  ① 本文に1行も出ない語を並べてしまう ② ④' の言い換えに概要欄が追いつかない ③ 下書きから語が漏れる
⚠️ これは門番ではなく当たり。**0行の語は必ず落とすか、本文の言い回しへ直す。**
⚠️ 16本目の下書き＝台本第2版 §1-6「用語の言いかえ（初出で一言）」の24項目。⑥で本文に当てて決める。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402

SPEC = ROOT / "ref" / "ep16" / "yougo.md"
# 候補＝台本第2版 §1-6 の下書き（④'）＋ ⑥で本文から拾った語（中学生に噛み砕きが要りそうなもの）
CAND = [
    # §1-6 の下書き（④'）
    "予見", "越流", "決壊", "水位", "標高", "調査委員会", "学術の総説", "公社", "アーチダム",
    "二重のアーチ", "天端", "地質学者", "すべり面", "多数派", "少数派", "ダムを検査する国の委員",
    "水理模型", "土木局", "憲兵隊", "時効", "一審", "予審", "最高裁判所", "破毀院", "控訴審",
    "恩赦", "世界の記憶",
    # ⑥で本文から拾った語
    "地すべり", "立方メートル", "峡谷", "等高線", "亀裂", "測量", "地下水", "粘土", "石灰岩",
    "電力", "国営", "エネル", "サーデ", "発電", "貯水", "放流", "水を抜く", "トンネル", "迂回",
    "模型", "縮尺", "起訴", "有罪", "無罪", "過失", "重い過失", "予見可能性", "刑事", "民事",
    "賠償", "議会", "ユネスコ", "共和国", "国のダム局", "公共事業", "大臣", "技術の責任者",
    "地盤", "専門家", "斜面", "塊", "傾き", "崩落", "クリープ", "速さ", "許可", "試験",
]


def variants(label):
    """「ゆるみ止めのナット（ロックナット）」→ ['ゆるみ止めのナット', 'ロックナット']。丸括弧の中も別表記として数える。"""
    m = re.match(r"^(.+?)（(.+?)）$", label)
    return [m.group(1), m.group(2)] if m else [label]


def scan(labels):
    ls = ES.lines()
    rows = []
    for label in labels:
        vs = variants(label)
        hits = [l for l in ls if any(v in l.text for v in vs)]
        n = sum(sum(l.text.count(v) for v in vs) for l in hits)
        # 「多数派・少数派」のように2語を1行にまとめた見出しは、**どちらの語も**本文に出ることを求める
        #   （まとめた形のままでは本文に出ない＝0行と出て、語そのものの有無を言えない）
        parts = []
        if "（" not in label:
            if "・" in label:
                parts = label.split("・")
            elif "と" in label:
                parts = [p for p in label.split("と") if p]
        if parts and len(parts) > 1 and all(any(p in l.text for l in ls) for p in parts):
            hits = [l for l in ls if any(p in l.text for p in parts)]
            n = sum(sum(l.text.count(p) for p in parts) for l in hits)
        rows.append((label, len(hits), n, hits[0] if hits else None))
    return rows


def show(rows, why):
    print(why)
    for label, nl, n, first in rows:
        if first is None:
            print("  🔴 0行/ 0回  %s ← **本文に1行も出ない。落とすか本文の言い回しへ直す**" % label)
        else:
            print("  %4d行/%3d回  %-14s %-8s %s" % (nl, n, label, first.lid, first.text))
    zero = [r[0] for r in rows if r[3] is None]
    print()
    print("🔴 本文に出ない語 %d件: %s" % (len(zero), "／".join(zero)) if zero else "✅ 全語が本文に出ます")
    return len(zero)


def spec_labels():
    """ref/ep16/yougo.md の「貼る本文」から、行頭の見出し語を取る。"""
    if not SPEC.exists():
        raise SystemExit("🔴 まだ ref/ep16/yougo.md がありません（--spec は下書きを書いてから）")
    out = []
    for line in SPEC.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^[・･]\s*(.+?)\s*[…:：]", line)
        if m:
            out.append(m.group(1).strip())
    if not out:
        raise SystemExit("🔴 貼る本文から語を1件も取れない＝書式が変わった（fail closed）")
    return out


if __name__ == "__main__":
    if "--spec" in sys.argv:
        labels = spec_labels()
        sys.exit(1 if show(scan(labels), "ref/ep16/yougo.md の貼る本文から %d 語" % len(labels)) else 0)
    show(scan(CAND), "候補 %d 語（台本 §1-6 ＋ ⑥で本文から拾った語）" % len(CAND))
