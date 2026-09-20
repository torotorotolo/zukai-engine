# -*- coding: utf-8 -*-
r"""ep10_yomi_adopted.py — A/B に掛けた候補が、**採用も不採用も決まっているか**を突き合わせる門番。

  python qa_out/ep10_yomi_adopted.py

🔴 なぜ要るか（2026-09-20 ⑤a で実際に踏んだ）:
   A/B で「効いた」と判断した `な店だったのか` と `行方不明者の` を、**EL_YOMI に書き忘れた**。
   ⚠️ `ep10_verify_fix.py` は「当たったキーが狙いどおりか」しか見ないので、
      **入れ忘れたキーは1件も鳴らない**（fail open）。焼き直しのあと、聞取をもう一度読んで初めて気づいた。
   → 「候補の一覧」と「辞書」を**件数で突き合わせる**層が要る
     （reference-elevenlabs-tts の『el_ab_yomi は黙って飛ばす＝件数を数えて突き合わせること』の一般化）。

判定: 計画に出した候補の id/key ごとに
  ① そのキー（または**そのキーを含むより長いキー**）が EL_YOMI に在る → 採用ずみ
  ② REJECTED に理由つきで在る                                   → 不採用の判断ずみ
  ③ どちらでもない                                             → 🔴 **未決**（止める）
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402

PLANS = sorted(Path(__file__).parent.glob("ep10_yomi_plan*.json"))

# 🔴 「入れない」と決めたもの。**理由を必ず書く**（空欄は未決と同じ）
REJECTED = {
    "地検": "「ちけん」も「チケン」も効かず（試験・治験）。⭐ 頁→ページ を当てた後の聞取が『治験』＝ちけん の音になった",
    "地検の報告は": "同上。カタカナでも直らなかった",
    "建て主": "かなを送っても聞取が変わらない＝**音は たてぬし で正しい**（正しく読める語をかな化しない）",
    "柱のまわりの床": "キーを「…床は、板」まで伸ばして採用（短いままだと崩れていない3行に当たる）",
}
# 対照として回した候補（崩れていない行に当てて「変化なし」を見るためのもの）＝採否の対象外
CONTROLS = {
    ("c110-3", "床"), ("c710-2", "床"), ("c112-2", "床"), ("c520-1", "床"), ("c417-2", "床"),
    ("c405-2", "白書"), ("c102-2", "北の棟"), ("c205-3", "の棟"),
    ("pr09-3", "瓦礫"), ("c716-1", "瓦礫"), ("ep03-2", "建ったあと"), ("c901-2", "数は、この"),
}


def main():
    cands = []
    for p in PLANS:
        for it in json.loads(p.read_text(encoding="utf-8")):
            cands.append((p.name, it["id"], it["key"]))
    keys = set(ES.EL_YOMI)
    undecided = []
    n_adopt = n_rej = n_ctl = 0
    for src, lid, key in cands:
        if (lid, key) in CONTROLS:
            n_ctl += 1
        elif key in keys or any(key in k for k in keys):
            n_adopt += 1
        elif key in REJECTED:
            n_rej += 1
        else:
            undecided.append((src, lid, key))
    print(f"計画 {len(PLANS)}本／候補 {len(cands)}件 ＝ 採用 {n_adopt}／不採用 {n_rej}／対照 {n_ctl}／"
          f"**未決 {len(undecided)}**")
    for src, lid, key in undecided:
        print(f"  🔴 {src} {lid} 「{key}」… EL_YOMI にも REJECTED にも無い")
    if not undecided:
        print("✅ 候補は全件、採用か不採用かが決まっています")
    print(f"\nEL_YOMI {len(keys)}件")
    return 1 if undecided else 0


if __name__ == "__main__":
    sys.exit(main())
