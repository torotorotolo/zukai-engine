# -*- coding: utf-8 -*-
r"""ep13_yougo.py — 概要欄に載せる用語の下書きを、**本文で裏を取りながら**作る物差し（13本目・2026-09-24）。

  python qa_out/ep13_yougo.py         … 候補語ごとに「本文に何行出るか・初出カット・初出行の全文」
  python qa_out/ep13_yougo.py --spec  … ref/ep13/yougo.md の「貼る本文」に並ぶ語を、同じ目で検算

12本目の `qa_out/ep12_yougo.py` を写した（変えたのは候補語と md の場所だけ）。
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

SPEC = ROOT / "ref" / "ep13" / "yougo.md"
# 候補＝台本第2版 §8 の下書き ＋ ⑤a で本文（数を読み替えた148行と §6-2 の語）から拾った語
CAND = [
    # §8 の下書き（④'）
    "貨物ドア", "与圧", "減圧", "フック", "ラッチ", "ロックピン", "通気扉", "ベント・ドア", "のぞき窓",
    "航空機関士", "SB", "サービス・ブレティン", "AD", "耐空性改善命令", "FAA", "連邦航空局",
    "NTSB", "国家運輸安全委員会", "ボイスレコーダー", "CVR", "紳士協定", "昇降舵", "確定の注文",
    # ⑤a で本文から拾った語（中学生に噛み砕きが要りそうなもの）
    "貨物室", "警告灯", "登録記号", "製造番号", "停留", "供述", "副職長", "検査員", "入社内定者",
    "添乗員", "官報", "公聴会", "上院", "長官", "世界時", "梢", "勧告", "改正", "義務", "汚職",
    "はんこ", "事故調査委員会", "最終報告", "補償", "慰霊", "証人", "商社", "三井物産", "全日空",
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
    """ref/ep13/yougo.md の「貼る本文」から、行頭の見出し語を取る。"""
    if not SPEC.exists():
        raise SystemExit("🔴 まだ ref/ep13/yougo.md がありません（--spec は下書きを書いてから）")
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
        sys.exit(1 if show(scan(labels), "ref/ep13/yougo.md の貼る本文から %d 語" % len(labels)) else 0)
    show(scan(CAND), "候補 %d 語（台本 §8 ＋ ⑤a で本文から拾った語）" % len(CAND))
