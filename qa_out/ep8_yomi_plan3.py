# -*- coding: utf-8 -*-
r"""ep8_yomi_plan3.py — A/B の3周目。**2周目の全文起こしで新しく出た崩れ**に当てる。

  python qa_out/ep8_yomi_plan3.py [--show]

🔴 3周目が要る理由（2026-09-14）:
   1周目の全文起こしと2周目の全文起こしは**同じ音**（焼き直していない行はキャッシュから同じ pcm）
   を起こしている。それでも結果が変わる＝Scribe の揺れ。だから
     ・**2周とも崩れた行** → 本物。直す
     ・**片方だけ崩れた行** → 揺れの疑い。ただし**行頭が別語になる型**は音の側も怪しいので A/B で当たる
   🔴🔴 これで **c208-2「RCC→LCC」は2周とも崩れ**と分かった。A/B の1回だけ正しく出たので
        「揺れ」と判定して辞書から外していたが、**判定を取り消す**。
        → [[feedback-verify-your-own-instrument]]（1回の観測で決めない）
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PLAN = [
    # ── 2周とも崩れた＝本物 ──────────────────────────────
    ("c208-2", "RCCの板でいえば", "アールシーシーの板でいえば", 1,
     "🔴🔴 **1周目も2周目も LCC**。RCC はこの回の中心の語（§6の筆頭）。8行中この行だけ崩れる"),
    # ── 2周目に新しく出た「行頭が別語」（1周目は無事。音の側も怪しいので当たる）──────
    ("c214-1", "予算とカメラ", "よさんとカメラ", 1, "『ロサンと』。⚠️ 予算は2行あり、1周目は c905-1 が『助産』で崩れた"),
    ("c207-3", "差の分だけ", "さの分だけ", 1, "『浅野分だけ』"),
    ("c509-2", "記録には", "きろくには", 1, "『浩久には』"),
    ("c504-1", "軌道にいるコロンビア号の左", "きどうにいるコロンビア号の左", 1,
     "🔴『非道にいる』＝意味が反転する。⚠️「軌道にいる」は **pr08-1（無事）にも当たる**ので長くした"),
    ("c520-1", "前のふち用の式", "前のふち用の しき", 1, "『前のフチオの式』"),
]


def main():
    import el_script as ES
    lines = {l.lid: l.text for l in ES.lines()}
    allt = [l.text for l in ES.lines()]
    bad, out = [], []
    for lid, key, val, want, why in PLAN:
        t = lines.get(lid)
        if t is None:
            bad.append(f"{lid}: 台本に無い行ID")
            continue
        if key not in t:
            bad.append(f"{lid}: key「{key}」がその行に当たらない → {t}")
            continue
        hits = sum(1 for x in allt if key in x)
        if hits != want:
            bad.append(f"{lid}: key「{key}」の当たる行数 {hits}（想定 {want}）")
        if "、" in val and val.count("、") != key.count("、"):
            bad.append(f"{lid}: val に読点を足している: {val}")
        sent = ES.el_text(t)
        if key not in sent:
            bad.append(f"{lid}: key「{key}」は EL_YOMI 適用後の送信文に無い\n      送信文: {sent}")
        print(f"{'  ' if hits == want else '🔴'}{lid:<9}{hits:>3}/{want:>3}  「{key}」→「{val}」")
        out.append({"id": lid, "key": key, "val": val, "why": why})
    print(f"\n候補 {len(out)}件")
    if bad:
        print(f"\n🔴 直すところ {len(bad)}件:")
        for b in bad:
            print("   " + b)
        return 1
    if "--show" not in sys.argv:
        p = ROOT / "qa_out" / "ep8_yomi_plan3.json"
        p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"→ {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
