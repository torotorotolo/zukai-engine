# -*- coding: utf-8 -*-
"""13本目 ⑤a'：数字で送る行の「数」を、音素の網の結果から台帳 qa_out/ep13_yomi_heard.tsv へ書く（API 不使用・2026-09-24）。

  python qa_out/ep13_yomi_phon_ledger.py          … 書く前に一覧だけ出す（phon にできる数／人が決める数）
  python qa_out/ep13_yomi_phon_ledger.py --write  … 台帳へ書く（既存の行は残し、無い (行ID, 語) だけ足す）

判定 phon ＝ その行の「読みの食い違い（雑音の型を除く）」に、**数の語が1つも入っていない**（qa_out/phon_check.py）。
🔴 耳ではない（check_yomi_numbers は耳の ok と分けて数える）。数の語に食い違いがある行は書かない＝人が決めて MANUAL に書く。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "qa_out"))
import check_yomi_numbers as CY  # noqa: E402
import el_script as E  # noqa: E402
import phon_check as P  # noqa: E402
import phon_review as V  # noqa: E402

NUMTOK = re.compile(r"[0-9０-９一二三四五六七八九十百千万]")
WHEN = "2026-09-24 ⑤a' 音素の網（qa_out/phon_verify.py）で数の語に食い違いなし＝耳ではない"
# 数の語に食い違いが出たが、人が読んで「どちらも正しい読み」と決めたもの（行ID, 語）→ 理由
MANUAL = {
    ("c412-1", "67人"): "2026-09-24 ⑤a' 網『ろくじゅうななにん』（pyopenjtalk は しち）＝どちらも正しい読み。耳ではない",
    ("c415-1", "1"): "2026-09-24 ⑤a' 網『いちまんいっせん』（pyopenjtalk は いちまんせん）＝どちらも正しい読み。耳ではない",
    ("c415-1", "1750"): "2026-09-24 ⑤a' 網『いちまんいっせんななひゃくごじゅう』（pyopenjtalk は せん）＝どちらも正しい読み。耳ではない",
    ("c415-1", "7時"): "2026-09-24 ⑤a' 網で数の語に食い違いなし（同じ行の 1万1750 の差で行ごと止まっただけ）。耳ではない",
    ("c415-1", "25分"): "2026-09-24 ⑤a' 同上。耳ではない",
    ("c415-1", "3580メートル"): "2026-09-24 ⑤a' 同上。耳ではない",
}


def main():
    rows = {r["lid"]: r for r in P.analyse("ep13")}
    heard = CY.load_heard("ep13")
    ok, manual, todo = [], [], []
    for ln in E.lines():
        sent = E.el_text(ln.text)
        for w in CY.risky(sent):
            if (ln.lid, w) in heard:
                continue
            if (ln.lid, w) in MANUAL:
                manual.append((ln.lid, w, MANUAL[(ln.lid, w)]))
                continue
            r = rows[ln.lid]
            hit = [h for h in r["bad"] if not V.benign(h, r) and NUMTOK.search(P.surf(r, h["tok"]))]
            (todo if hit else ok).append((ln.lid, w, hit))
    print(f"phon にできる {len(ok)}／人が決めた {len(manual)}／数の語に食い違い（書かない） {len(todo)}")
    for lid, w, hit in todo:
        print(f"  ✗ {lid} {w}: " + "／".join(f"{P.surf(rows[lid], h['tok'])} {h['exp']}→{h['rec']}" for h in hit))
    if "--write" in sys.argv:
        p = ROOT / "qa_out" / "ep13_yomi_heard.tsv"
        head = "" if p.exists() else ("# ep13 の「危ない数」の記録（tools/check_yomi_numbers.py が読む）\n"
                                      "# 行ID\t語\t判定\tいつ・だれが\n"
                                      "# 🔴 phon＝音素の網で読みを確かめた（耳ではない）。ok＝耳で通した。ng＝直す\n")
        with open(p, "a", encoding="utf-8") as f:
            f.write(head)
            for lid, w, _ in ok:
                f.write(f"{lid}\t{w}\tphon\t{WHEN}\n")
            for lid, w, why in manual:
                f.write(f"{lid}\t{w}\tphon\t{why}\n")
        print(f"→ {p} に {len(ok) + len(manual)} 件を足した")
    return 1 if todo else 0


if __name__ == "__main__":
    sys.exit(main())
