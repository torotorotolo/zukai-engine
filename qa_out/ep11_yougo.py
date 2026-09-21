# -*- coding: utf-8 -*-
r"""ep11_yougo.py — 概要欄に載せる用語の下書きを、**本文で裏を取りながら**作る物差し（11本目）。

  python qa_out/ep11_yougo.py         … 候補語ごとに「本文に何行出るか・初出カット・初出行の全文」
  python qa_out/ep11_yougo.py --spec  … ref/ep11/yougo.md の「貼る本文」に並ぶ語を、同じ目で検算

🔴 なぜ要るか（feedback-jiko-description-glossary の「下書きが必ず外す3つの型」）:
  ① 本文に1行も出ない語を並べてしまう（9.11 で EDT ほか4語が0行だった）
  ② ④' が言い換えたのに、概要欄が古い語のまま追いつけていない
  ③ 下書きから語が漏れる（読み辞書を作るとき全語を1回通るので、そこで拾う）
⚠️ これは門番ではなく当たり。**0行の語は必ず落とすか、本文の言い回しへ直す。**

⚠️ 11本目の特徴＝**台本がそもそも専門語をほとんど使っていない**
   （[[feedback-jiko-plain-language]] を ④ が徹底したため。カタカナ語 44種のうち技術語は
   「ノズル」「ボルト」だけで、残りは人名・地名）。
   ＝ 候補は **§1-9 の言い換えの表**（報告書の語 → 本文での言い方）が中心になる。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402

# 候補＝台本 §1-9（言い換えの表）＋ 本文を機械で通して拾った技術語
CAND = [
    # §1-9 の言い換えの表（報告書の語 → 本文の言い方）
    "補助ロケット", "継ぎ目", "ゴムの輪", "燃料タンク", "断熱材",
    "打ち上げを止める札", "区分1", "運用管理", "安全担当官",
    # 本文から機械で拾った技術語
    "ノズル", "液体水素", "液体酸素", "固体燃料", "推力", "マッハ",
    "東部標準時", "発射台", "回収", "パテ", "圧力", "信号", "望遠鏡",
    # 組織・制度
    "委員会", "報告書", "勧告", "技術部門", "上級副社長", "宇宙輸送部門",
]


def variants(label):
    """「継ぎ目（つぎめ）」→ ['継ぎ目', 'つぎめ']。丸括弧の中も別表記として数える。"""
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
    """ref/ep11/yougo.md の「貼る本文」から、行頭の見出し語を取る。"""
    p = ROOT / "ref" / "ep11" / "yougo.md"
    if not p.exists():
        raise SystemExit("🔴 まだ ref/ep11/yougo.md がありません（--spec は下書きを書いてから）")
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^[・･]\s*(.+?)\s*[…:：]", line)
        if m:
            out.append(m.group(1).strip())
    if not out:
        raise SystemExit("🔴 貼る本文から語を1件も取れない＝書式が変わった（fail closed）")
    return out


if __name__ == "__main__":
    if "--spec" in sys.argv:
        labels = spec_labels()
        sys.exit(1 if show(scan(labels), "ref/ep11/yougo.md の貼る本文から %d 語" % len(labels)) else 0)
    show(scan(CAND), "候補 %d 語（台本 §1-9 ＋ 本文から機械で拾った語）" % len(CAND))
