# -*- coding: utf-8 -*-
r"""ep12_yougo.py — 概要欄に載せる用語の下書きを、**本文で裏を取りながら**作る物差し（12本目・2026-09-23）。

  python qa_out/ep12_yougo.py         … 候補語ごとに「本文に何行出るか・初出カット・初出行の全文」
  python qa_out/ep12_yougo.py --spec  … ref/ep12/yougo.md の「貼る本文」に並ぶ語を、同じ目で検算

11本目の `qa_out/ep11_yougo.py` を写した（変えたのは候補語と md の場所だけ）。
🔴 なぜ要るか（feedback-jiko-description-glossary の「下書きが必ず外す3つの型」）:
  ① 本文に1行も出ない語を並べてしまう ② ④' の言い換えに概要欄が追いつかない ③ 下書きから語が漏れる
⚠️ これは門番ではなく当たり。**0行の語は必ず落とすか、本文の言い回しへ直す。**
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402

SPEC = ROOT / "ref" / "ep12" / "yougo.md"
# 候補＝台本第2版 §8 の下書き ＋ ⑤a で本文を通しで読んで拾った語（中学生に噛み砕きが要るもの）
CAND = [
    # §8 の下書き（④）
    "水素爆弾", "原子爆弾", "環礁", "放射性降下物", "被曝", "TNT火薬に直して",
    "重水素化リチウム", "リチウム6", "リチウム7", "三重水素", "トリチウム", "乾式",
    "線量計", "原爆傷害調査委員会", "原子力委員会", "国防脅威削減局",
    # ⑤a で本文から拾った語
    "灰", "核融合", "中性子", "日付変更線", "危険区域", "第7合同任務部隊", "キャッスル作戦",
    "ロスアラモス科学研究所", "国防総省", "医師団", "はえ縄漁", "無線長", "原爆マグロ",
    "血小板", "慰謝料", "原水爆禁止", "駆逐艦", "爆心", "バッジ", "計器",
]


def variants(label):
    """「三重水素（トリチウム）」→ ['三重水素', 'トリチウム']。丸括弧の中も別表記として数える。"""
    m = re.match(r"^(.+?)（(.+?)）$", label)
    return [m.group(1), m.group(2)] if m else [label]


def scan(labels):
    ls = ES.lines()
    rows = []
    for label in labels:
        vs = variants(label)
        hits = [l for l in ls if any(v in l.text for v in vs)]
        n = sum(sum(l.text.count(v) for v in vs) for l in hits)
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
    """ref/ep12/yougo.md の「貼る本文」から、行頭の見出し語を取る。"""
    if not SPEC.exists():
        raise SystemExit("🔴 まだ ref/ep12/yougo.md がありません（--spec は下書きを書いてから）")
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
        sys.exit(1 if show(scan(labels), "ref/ep12/yougo.md の貼る本文から %d 語" % len(labels)) else 0)
    show(scan(CAND), "候補 %d 語（台本 §8 ＋ ⑤a で本文から拾った語）" % len(CAND))
