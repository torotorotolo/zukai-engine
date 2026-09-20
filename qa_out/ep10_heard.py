# -*- coding: utf-8 -*-
r"""ep10_heard.py — 文字起こしの tsv を**パスを指定して**洗う（2周の突き合わせ用）。

  python qa_out/ep10_heard.py audio/el_qa/ep10_el_yomi_p1.tsv
  python qa_out/ep10_heard.py <p1> <p2>      … 2周を並べて「2周とも崩れた行」を出す

🔴 なぜ要るか: `el_check_heard` は `ES.qa_path("el_yomi.tsv")`（正本の1本）しか読まない。
   2周目を回すとそこが上書きされるので、**周ごとの控えを並べて比べる口**が無かった。
   物差しは自作せず `check_numbers_heard.heard_numbers` と `el_ledger.numbers_missing` を import する
   （同じ物差しを2か所に持たない＝feedback-verify-your-own-instrument）。
"""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from el_ledger import numbers_missing  # noqa: E402  台本の数のうち聞取に無いもの


# 🔴 el_check_yomi の tsv の列は **場面 / 一致率 / 送った文 / 聞こえた文 / 送信文**。
#    ⚠️ 2026-09-20 に踏んだ穴: (行ID, 台本, 聞取, 一致率) の順だと思い込み、**460行中459行が所見**になった。
#       「全部NGなら道具を疑う」（feedback-verify-your-own-instrument）。1行目で header を読んで固定する。
COLS = ("場面", "一致率", "送った文", "聞こえた文", "送信文")


def load(p):
    with open(p, encoding="utf-8") as f:
        rows = [r for r in csv.reader(f, delimiter="\t") if r]
    head = tuple(rows[0][:5])
    if head != COLS:
        raise SystemExit(f"🔴 tsv の列が変わった: {head}（期待 {COLS}）＝ fail closed")
    return {r[0]: r for r in rows[1:]}


def flags(row):
    """所見を出す。数は「台本 対 聞取」、頭は「実際に送った文 対 聞取」で見る。"""
    rate, script, heard = row[1], row[2], row[3]
    sent = row[4] if len(row) > 4 and row[4] else script
    out = []
    miss = numbers_missing(script, heard)
    if miss:
        out.append("数が無い:" + "/".join(str(m) for m in miss))
    if sent and heard and sent[0] != heard[0]:
        out.append(f"頭が違う:{sent[0]}→{heard[0]}")
    try:
        r = float(rate)
        if r <= 1.0:
            r *= 100          # 🔴 tsv は 0〜1 の比（feedback-verify-your-own-instrument）
        if r < 90.0:
            out.append(f"一致率{r:.1f}%")
    except ValueError:
        pass
    return out


def main():
    paths = [Path(a) for a in sys.argv[1:] if not a.startswith("--")]
    if not paths:
        raise SystemExit(__doc__)
    runs = [load(p) for p in paths]
    keys = list(runs[0])
    print(f"行 {len(keys)}／周 {len(runs)}")

    per = []
    for i, r in enumerate(runs, 1):
        n = sum(1 for k in keys if flags(r[k]))
        per.append(n)
        print(f"  {i}周目 所見のある行 {n}")
    if len(runs) == 1:
        for k in keys:
            fl = flags(runs[0][k])
            if fl:
                print(f"\n{k}  [{' / '.join(fl)}]")
                print(f"   台本: {runs[0][k][2]}")
                print(f"   聞取: {runs[0][k][3]}")
        return 0

    both, only = [], []
    for k in keys:
        a, b = flags(runs[0][k]), flags(runs[1].get(k, runs[0][k]))
        if a and b:
            both.append(k)
        elif a or b:
            only.append(k)
    print(f"\n🔴 2周とも所見 {len(both)}行  ／ 片方だけ {len(only)}行")
    for k in both:
        a, b = flags(runs[0][k]), flags(runs[1][k])
        print(f"\n{k}  1周[{' / '.join(a)}]  2周[{' / '.join(b)}]")
        print(f"   台本: {runs[0][k][2]}")
        print(f"   1周: {runs[0][k][3]}")
        print(f"   2周: {runs[1][k][3]}")
    print("\n── 片方だけ（引き直すと直る側の疑い。9本目の作法では弱い証拠）──")
    for k in only:
        a, b = flags(runs[0][k]), flags(runs[1][k])
        print(f"  {k}  1周[{' / '.join(a) or '—'}]  2周[{' / '.join(b) or '—'}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
