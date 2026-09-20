# -*- coding: utf-8 -*-
r"""ep10_verdicts.py — 台帳の「疑い」行に**扱い**を付ける下書きを機械で作る。

  python qa_out/ep10_verdicts.py            … 分類して audio/el_qa/ep10_verdicts.tsv を書く
  python qa_out/ep10_verdicts.py --dry      … 書かずに内訳だけ出す

🔴 これは「全部OK」を言う道具ではない。**分類できない行を残して、人（Claude）に読ませる**ためのもの。
   分類できた行だけ扱いを付け、残りは `要耳` にして試写へ送る（feedback-no-ear-checks-until-shisha）。

分類（上から順に当てる）:
  A 辞書で直した … EL_YOMI が当たる行で、`ep10_verify_fix.py` が狙った音を確認ずみ
  B 表記違い    … 台本と聞取を**読み**に直すと一致する（el_reading_diff の「読み一致」）
  C 漢数字化    … 所見が「頭が違う」だけで、台本の頭が数字・聞取の頭が漢数字
  D 数は合う    … numbers_missing が空（＝数の値は全部聞き取れている）かつ一致率 85%以上
  E 要耳       … 上のどれにも当たらない
"""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES                      # noqa: E402
from el_ledger import numbers_missing       # noqa: E402

KAN = "〇一二三四五六七八九十百千万億"

# 🔴 機械で分類できなかった行を、**1行ずつ聞取を読んで**判定したもの（2026-09-20 ⑤a）。
#    ⚠️ ここに書くのは「読んだ」行だけ。読んでいない行を静かにさせるために使わない。
#    ⚠️ 一致率が低いのは**ほぼ全部が表記**（漢数字化・かな⇄漢字・同音の字当て）。
#       一致率で採否を決めない（feedback-ear-beats-the-meter）。
MANUAL = {
    "c114-2": ("表記違い", "『朝九時頃・十時頃』＝算用数字の漢数字化だけ。数の照合は通っている"),
    "c403-2": ("表記違い", "『百三十六点五トン・九十台分』＝漢数字化。小数の点も残っている"),
    "c506-2": ("表記違い", "『張りがなくて』＝梁を **はり** と正しく読んでいる（Scribe の字の当て違い）"),
    "c611-1": ("表記違い", "『幹部が朝九時頃、社長が十時頃』＝漢数字化と句点→読点だけ"),
    "c612-2": ("表記違い", "『行う・取り掛かった』＝かな→漢字だけ"),
    "c705-2": ("表記違い", "『隣の柱の方へ』＝かな→漢字だけ。音は となり／ほう"),
    "c906-2": ("表記違い", "『怪我・九百三十七人・千四百三十九人』＝かな→漢字と漢数字化"),
    "c915-3": ("表記違い", "『一千三億ウォン』＝1,003億。数の照合は通っている"),
    "ep05-2": ("表記違い", "『禁錮一年、懲役一年六ヶ月、懲役十ヶ月』＝⑤aで「6月→6か月」に直した行。正しく読めている"),
    "ep08-2": ("表記違い", "『崩壊との間に』＝台本のかな「あいだ」をそのまま送っている。字だけ漢字"),
    "c405-2": ("対照（辞書に入れなかった）",
               "🔴『白書→はくしょ』を一括で当てると、この行だけ **『博士』に悪化**した（A/B 94.7→87.7%）。"
               "だから白書は**行ごとのキー**にして、この行には当てていない。いまの聞取は『白書』で正しい"),
}


def tsv(p, keyi=0):
    if not Path(p).exists():
        return {}
    rows = [r for r in csv.reader(open(p, encoding="utf-8"), delimiter="\t") if r]
    return {r[keyi]: r for r in rows[1:]}


def main():
    yomi = tsv(ES.qa_path("el_yomi.tsv"))
    rdiff = tsv(ES.qa_path("reading_diff.tsv"))
    out, counts = [], {}
    for l in ES.lines():
        y = yomi.get(l.lid)
        if not y:
            continue
        rate, script, hrd = float(y[1]), y[2], y[3]
        miss = numbers_missing(script, hrd)
        hits = []
        ES.el_text(l.text, hits)
        sus = bool(miss) or rate < 0.90 or l.lid in rdiff
        # ⚠️ MANUAL に書いた行は、こちらの「疑い」の網に掛からなくても必ず出す
        #    （台帳は A/B の記録がある行も疑いに数えるので、網が食い違うと未判定が残る）
        if not sus and not hits and l.lid not in MANUAL:
            continue

        if l.lid in MANUAL:
            v = MANUAL[l.lid]
        elif hits:
            keys = "／".join(a for a, _, _ in hits)
            v = ("直した（辞書）", f"EL_YOMI「{keys}」。狙った音が出ていることを ep10_verify_fix.py で確認ずみ")
        elif l.lid in rdiff and rdiff[l.lid][1] == "読み一致":
            v = ("表記違い", "台本と聞取を読みに直すと一致（el_reading_diff）。音は正しい")
        elif not miss and script and hrd and script[0].isdigit() and hrd[0] in KAN:
            v = ("表記違い", "行頭の算用数字を聞取が漢数字で書いただけ。数の照合は通っている")
        elif not miss and rate >= 0.85:
            v = ("表記違い", f"数は全部聞き取れており一致率 {rate*100:.0f}%。差は かな⇄漢字・同音の字当て")
        else:
            v = ("要耳", f"一致率 {rate*100:.0f}%" + (f"／数が無い {','.join(miss)}" if miss else ""))
        counts[v[0]] = counts.get(v[0], 0) + 1
        out.append((l.lid, v[0], v[1]))

    print("／".join(f"{k} {n}" for k, n in sorted(counts.items(), key=lambda x: -x[1])))
    if "--dry" in sys.argv:
        for lid, k, why in out:
            if k == "要耳":
                y = yomi[lid]
                print(f"\n🔴 {lid} {why}")
                print(f"   台本: {y[2]}")
                print(f"   聞取: {y[3]}")
        return 0
    p = ES.qa_path("verdicts.tsv")
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["行", "扱い", "理由"])
        w.writerows(out)
    print(f"{len(out)}行 → {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
