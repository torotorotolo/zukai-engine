# -*- coding: utf-8 -*-
r"""ep10_yougo.py — 概要欄に載せる用語の下書きを、**本文で裏を取りながら**作る物差し。

  python qa_out/ep10_yougo.py            … 候補語ごとに「本文に何行出るか・初出カット・初出行の全文」
  python qa_out/ep10_yougo.py --spec     … ref/ep10/yougo.md の「貼る本文」に並ぶ語を、同じ目で検算

🔴 なぜ要るか（feedback-jiko-description-glossary の「下書きが必ず外す3つの型」）:
  ① 本文に1行も出ない語を並べてしまう（9.11 で EDT ほか4語が0行だった）
  ② ④' が言い換えたのに、概要欄が古い語のまま追いつけていない
  ③ 下書きから語が漏れる（読み辞書を作るとき全語を1回通るので、そこで拾う）
⚠️ これは門番ではなく当たり。**0行の語は必ず落とすか、本文の言い回しへ直す。**
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402

# 候補＝台本 §1-9（言い換えの表）＋ §6-1（読みの候補）＋ ⑤a で本文を通して拾ったもの
CAND = [
    "梁", "ドロップパネル", "せん断", "引張", "耐力壁", "定着", "スラブ",
    "冷却塔", "押えコンクリート", "防水層", "請負限度制", "仮使用", "竣工",
    "監理", "設計事務所", "下請け", "増築", "用途変更",
    "大法院", "業務上過失致死傷", "共同正犯", "禁錮", "執行猶予", "控訴", "上告",
    "災難管理法", "国政監査", "白書", "瑞草区", "ウォン", "坪",
    "焼香所", "戸籍", "貴金属", "のべ", "延べ",
]


def variants(label):
    """「監理（かんり）」→ ['監理', 'かんり']、「のべ（延べ）」→ ['のべ', '延べ']。

    🔴 2026-09-20 に踏んだ穴: 括弧ごと本文を探していたので、**18語中10語が偽の「0行」**になった。
       概要欄の見出しは「語（読み）」や「語／別表記」の形を取るので、**当てる前にほどく**。
       どれか1つでも本文に在れば在るとみなす（読み仮名だけが本文に無いのは当たり前）。
    """
    label = label.strip()
    m = re.match(r"^(.+?)\s*[（(](.+?)[）)]\s*$", label)
    cands = [m.group(1), m.group(2)] if m else [label]
    out = []
    for c in cands:
        out += [x.strip() for x in re.split(r"[／/]", c) if x.strip()]
    return out


def scan(words):
    ls = list(ES.lines())
    rows = []
    for w in words:
        vs = variants(w)
        hit = [l for l in ls if any(v in l.text for v in vs)]
        n_o = sum(sum(l.text.count(v) for v in vs) for l in hit)
        rows.append((w, len(hit), n_o, hit[0] if hit else None))
    return rows


def main():
    spec = "--spec" in sys.argv
    words = CAND
    if spec:
        p = ROOT / "ref" / "ep10" / "yougo.md"
        if not p.exists():
            raise SystemExit(f"🔴 まだありません: {p}")
        body = p.read_text(encoding="utf-8")
        m = re.search(r"```\n(.*?)\n```", body, re.S)
        if not m:
            raise SystemExit("🔴 「貼る本文」のコードブロックが見つからない（fail closed）")
        words = [x.group(1).strip() for x in re.finditer(r"^・(.+?)\s*…", m.group(1), re.M)]
        print(f"ref/ep10/yougo.md の貼る本文から {len(words)} 語")

    zero = []
    for w, n_l, n_o, first in scan(words):
        mark = "🔴 0行" if n_l == 0 else f"{n_l:3}行/{n_o:3}回"
        head = f"{first.lid} {first.text}" if first else "—"
        print(f"  {mark}  {w:12} {head}")
        if n_l == 0:
            zero.append(w)
    print()
    if zero:
        print(f"🔴 本文に出てこない語 {len(zero)}件: {'／'.join(zero)}")
        print("   → 概要欄から落とすか、本文の言い回しに直すこと（型①）")
        return 1 if spec else 0
    print("✅ 全語が本文に出ます")
    return 0


if __name__ == "__main__":
    sys.exit(main())
