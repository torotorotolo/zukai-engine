# -*- coding: utf-8 -*-
r"""ep14_yougo.py — 概要欄に載せる用語の下書きを、**本文で裏を取りながら**作る物差し（14本目・2026-09-29）。

  python qa_out/ep14_yougo.py         … 候補語ごとに「本文に何行出るか・初出カット・初出行の全文」
  python qa_out/ep14_yougo.py --spec  … ref/ep14/yougo.md の「貼る本文」に並ぶ語を、同じ目で検算

13本目の `qa_out/ep13_yougo.py` を写した（変えたのは候補語と md の場所だけ）。
🔴 なぜ要るか（feedback-jiko-description-glossary の「下書きが必ず外す3つの型」）:
  ① 本文に1行も出ない語を並べてしまう ② ④' の言い換えに概要欄が追いつかない ③ 下書きから語が漏れる
⚠️ これは門番ではなく当たり。**0行の語は必ず落とすか、本文の言い回しへ直す。**
⚠️ 14本目は ⑤a で下書きを作っていない（台本第2版 §8 の16語だけ）＝⑥で本文に当てて決める。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402

SPEC = ROOT / "ref" / "ep14" / "yougo.md"
# 候補＝台本第2版 §8 の下書き（④'）＋ ⑥で本文から拾った語（中学生に噛み砕きが要りそうなもの）
CAND = [
    # §8 の下書き（④'）
    "退船", "大法院", "海洋安全審判院", "中央海洋安全審判院", "裁決", "主文",
    "海上交通管制センター", "VTS", "123艇", "喫水", "重心", "復原力", "バラスト", "固縛",
    "変針", "操舵手", "ソレノイド弁", "傾斜試験", "不作為による殺人", "社会的惨事特別調査委員会",
    # ⑥で本文から拾った語
    "海洋警察", "警備艇", "特別調査報告", "全員合議体", "無期懲役", "待機", "船内放送",
    "救命いかだ", "救命胴衣", "増築", "積みすぎ", "引き揚げ", "固着", "航海士", "機関長",
    "甲板部", "機関部", "被告人", "起訴", "業務上過失", "虚偽", "日誌", "行政訴訟",
    "海審", "特調委", "判決", "無罪", "有罪", "懲役", "舵", "油圧", "ポンプ", "外力",
    "固定", "貨物", "コンテナ", "満載", "旅客", "修学旅行", "海里", "ノット",
]


def variants(label):
    """「海上交通管制センター（VTS）」→ ['海上交通管制センター', 'VTS']。丸括弧の中も別表記として数える。"""
    m = re.match(r"^(.+?)（(.+?)）$", label)
    return [m.group(1), m.group(2)] if m else [label]


def scan(labels):
    ls = ES.lines()
    rows = []
    for label in labels:
        vs = variants(label)
        hits = [l for l in ls if any(v in l.text for v in vs)]
        n = sum(sum(l.text.count(v) for v in vs) for l in hits)
        # 「重心・復原力」のように2語を1行にまとめた見出しは、**どちらの語も**本文に出ることを求める
        #   （まとめた形のままでは本文に出ない＝0行と出て、語そのものの有無を言えない）
        parts = label.split("・") if "・" in label and "（" not in label else []
        if parts and all(any(p in l.text for l in ls) for p in parts):
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
    """ref/ep14/yougo.md の「貼る本文」から、行頭の見出し語を取る。"""
    if not SPEC.exists():
        raise SystemExit("🔴 まだ ref/ep14/yougo.md がありません（--spec は下書きを書いてから）")
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
        sys.exit(1 if show(scan(labels), "ref/ep14/yougo.md の貼る本文から %d 語" % len(labels)) else 0)
    show(scan(CAND), "候補 %d 語（台本 §8 ＋ ⑥で本文から拾った語）" % len(CAND))
