# -*- coding: utf-8 -*-
"""ep7_glossary.py — 概要欄に載せる用語の下書きを**本文と突き合わせて**確定させる（この回かぎり）。

2026-09-13 カズヤくんの恒久ルール（[[feedback-jiko-description-glossary]]）:
    「トランスポンダのように一般的でない用語の簡単な説明を、概要欄にまとめて載せる」

ここで機械に見させるのは3つ。**目で決めない。**
  ① その語が**本文に本当に出るか**（出ない語を概要欄に並べない）
  ② **初出カットの全文**（説明を本文の言い回しと揃えるため。別語にしない）
  ③ **本文がその場で噛み砕いているか**（噛み砕きは省かない。概要欄は追加であって置き換えではない）

  python qa_out/ep7_glossary.py            … 語ごとに ①②③ を出す
  python qa_out/ep7_glossary.py --missing  … §11-5 の下書きのうち本文に出ない語だけ
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import el_script as ES  # noqa: E402
import narration  # noqa: E402

# §11-5 の下書き14語（見出し語 → 概要欄で使う候補の別名。別名は本文に無くてよい）
DRAFT = [
    ("トランスポンダ", []),
    ("応答符号", []),
    ("一次レーダー", []),
    ("二次レーダー", []),
    ("航空路管制センター", []),
    ("コマンドセンター", []),
    ("北東航空防衛セクター", ["防空司令部"]),
    ("連邦航空局", []),
    ("連邦航空保安官", []),
    ("共通戦略", []),
    ("緊急発進", ["スクランブル"]),
    ("音声記録装置", ["飛行記録装置", "ブラックボックス"]),
    ("大統領警護隊", ["シークレットサービス"]),
    ("EDT", ["東部夏時間"]),
]
# ④' の下書きに無いが、el_prelint と selfcheck で拾った語（入れるかをここで決める）
EXTRA = ["運航管理", "跳ね返り", "北棟", "南棟", "国防総省", "自動操縦", "世界貿易センター",
         "撃墜", "迎撃", "当直", "手引き", "西南西", "原則", "第1章"]

CUTS = [(cid, list(ls)) for cid, ls in narration.SCRIPT]
ORDER = {cid: i for i, (cid, _) in enumerate(CUTS)}


def find(term):
    return [(cid, ls) for cid, ls in CUTS if any(term in l for l in ls)]


def show(term, aliases, tag):
    hits = find(term)
    if not hits:
        alt = [a for a in aliases if find(a)]
        print(f"🔴 {tag} 「{term}」は本文に**1行も出ない**"
              + (f"（別名なら出る: {alt}）" if alt else "（別名も出ない）"))
        return
    cid, ls = hits[0]
    print(f"[{tag}] {term}  初出 {cid}（{len(hits)}カット・全体の {ORDER[cid]+1}/202 カット目）")
    for l in ls:
        print(f"      {l}")
    for a in aliases:
        h = find(a)
        print(f"      別名「{a}」: " + (f"{h[0][0]} に出る（{len(h)}カット）" if h else "本文に出ない"))


def main() -> int:
    only_missing = "--missing" in sys.argv
    ES.gate_args({"--missing"}, paid=False)
    print("══ §11-5 の下書き14語 ══════════════════════════")
    for t, al in DRAFT:
        if only_missing and find(t):
            continue
        show(t, al, "下書き")
        print()
    if only_missing:
        return 0
    print("══ 下書きに無い語（入れるかを決める）════════════════")
    for t in EXTRA:
        hits = find(t)
        print(f"  {t:<12} {len(hits):>2}カット  初出 {hits[0][0] if hits else '—'}"
              + (f"  「{hits[0][1][0]}」" if hits else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
