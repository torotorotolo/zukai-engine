# -*- coding: utf-8 -*-
r"""el_verdicts.py — 検査台帳の「扱い」列（audio/el_qa/<SLUG>_verdicts.tsv）を記録から組む（2026-09-05 新設）。

  python tools/el_verdicts.py            → <SLUG>_verdicts.tsv を書き直し、続けて el_ledger を回す

扱いの出どころ（あとのものが先のものを上書きする）:
  ① EL_YOMI が当たる行 … 「直した（EL_YOMI …）」＝読みを固定した行
  ② retake_gate.tsv     … 「取り直し（文字起こし合格）」／「要耳（全テイク落ち）」
  ③ <SLUG>_verdicts_manual.tsv … 人（Claude）が1行ずつ書いた判断（行ID\t扱い\t理由）。表記のゆれ・要耳の理由など
⚠️ 未判定の疑いが残れば el_ledger が exit 1 で止まる。「全部OK」を機械が言うための道具ではない。
"""
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_script as ES  # noqa: E402


def main():
    v = {}
    # ① EL_YOMI
    for ln in ES.lines():
        hits = []
        ES.el_text(ln.text, hits)
        if hits:
            v[ln.lid] = ("直した（EL_YOMI）", "／".join(f"{k}→{val}" for k, val, _ in hits))
    # ② 取り直し
    p = ES.qa_path("retake_gate.tsv")
    if p.exists():
        for l in p.read_text(encoding="utf-8").splitlines()[1:]:
            f = l.split("\t")
            if len(f) < 3:
                continue
            base = v.get(f[0], ("", ""))[1]
            if f[2].startswith("採用"):
                v[f[0]] = ("取り直し（文字起こし合格）", f"{f[1]}テイク" + (f"／{base}" if base else ""))
            else:
                v[f[0]] = ("要耳（取り直し全テイク落ち）", f"{f[1]}テイク／" + f[3][:80])
    # ③ 手書きの判断
    m = ES.qa_path("verdicts_manual.tsv")
    if m.exists():
        for l in m.read_text(encoding="utf-8").splitlines():
            if not l.strip() or l.startswith("#") or l.startswith("行"):
                continue
            f = l.split("\t")
            if len(f) >= 2:
                v[f[0]] = (f[1], f[2] if len(f) > 2 else "")
    # ④ 一致率 90% 未満だが、数・同形異音語・頭欠け・字の欠け・重複・異音のどの所見も無い行＝表記のゆれ。
    #    ⚠️ これは「一致率が低い＝誤読」ではない側の既定値。2026-09-05 は 76行を一覧で目視して全部 かな⇄漢字・漢数字・同音の別字だった。
    from el_check_yomi import load_tsv
    yomi = load_tsv(ES.qa_path("el_yomi.tsv"))
    fl = ES.qa_path("heard_flags.tsv")
    flagged = {l.split("\t")[0] for l in fl.read_text(encoding="utf-8").splitlines()[1:] if l.strip()} if fl.exists() else set()
    for lid, (text, heard, r, sent) in yomi.items():
        if r < 0.9 and lid not in flagged and lid not in v:
            v[lid] = ("表記のゆれ（所見なし・一覧で目視ずみ）", f"一致率 {r*100:.0f}%")
    order = [l.lid for l in ES.lines()]
    out = ES.qa_path("verdicts.tsv")
    out.write_text("行\t扱い\t理由\n" + "\n".join(f"{i}\t{v[i][0]}\t{v[i][1]}" for i in order if i in v) + "\n",
                   encoding="utf-8")
    kinds = {}
    for k, _ in v.values():
        kinds[k] = kinds.get(k, 0) + 1
    print(f"扱い {len(v)}行 → {out}  {kinds}")
    import el_ledger
    return el_ledger.main()


if __name__ == "__main__":
    sys.exit(main())
