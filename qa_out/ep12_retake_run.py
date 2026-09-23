# -*- coding: utf-8 -*-
"""12本目⑤a：取り直しの計画（qa_out/ep12_retake_plan.tsv）を1行ずつ el_retake に掛ける（2026-09-23）。

  python qa_out/ep12_retake_run.py              … 計画の全行
  python qa_out/ep12_retake_run.py c112-2,c209-1 … 指定の行だけ（計画にある行に限る）

なぜ要るか: el_retake の `--must` は1回に1行しか渡せない（行ごとに確かめたい語が違うため）。
🔴 課金の安全弁: 1行ごとに口座の使用量（/v1/user/subscription・無料）を読み、CAP を超えたら止める。
   CAP＝⑤aの上限 14,000クレジット（2026-09-23 カズヤくん）から、締めの検査ぶん約 700 を残した線。
   ⚠️ 使用量の反映は数十秒遅れることがある＝1行ぶん（最大3テイク≒100）はみ出しうる。だから余裕を残してある。
ログ: audio/el_qa/retake_ep12.log（行ごとの el_retake の出力を足していく）
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_tts  # noqa: E402

BASE = 135_544                 # ⑤a を始める前の使用量（2026-09-23 10:46 に実測）
CAP = BASE + 14_000 - 700      # ここを超えたら次の行へ進まない
PLAN = ROOT / "qa_out" / "ep12_retake_plan.tsv"
LOG = ROOT / "audio" / "el_qa" / "retake_ep12.log"


def plan():
    rows = []
    for ln in PLAN.read_text(encoding="utf-8").splitlines():
        if not ln.strip() or ln.startswith("#"):
            continue
        c = ln.split("\t")
        rows.append((c[0].strip(), c[1].strip(), int(c[2]), c[3].strip() if len(c) > 3 else ""))
    return rows


def main():
    rows = plan()
    if len(sys.argv) > 1:
        want = set(sys.argv[1].split(","))
        unknown = want - {r[0] for r in rows}
        if unknown:
            raise SystemExit(f"🔴 計画に無い行: {sorted(unknown)}")
        rows = [r for r in rows if r[0] in want]
    results = []
    with LOG.open("a", encoding="utf-8") as log:
        for lid, must, mx, why in rows:
            used, _ = el_tts.credits_used()
            if used >= CAP:
                print(f"🔴 使用量 {used:,} が上限の線 {CAP:,} に届いた（⑤aで {used - BASE:,}）。{lid} から先は回さない")
                break
            cmd = [sys.executable, "tools/el_retake.py", "--ids", lid, "--max", str(mx)]
            if must:
                cmd += ["--must", must]
            p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
            out = p.stdout + p.stderr
            log.write(f"\n===== {lid} must={must or '-'} max={mx} ｜ {why}\n{out}")
            log.flush()
            # el_retake の出力＝「  c112-2 take1: ✓  聞取の頭44字」と「c112-2: 2テイク → 採用（…）」
            verdict = "採用" if "採用（文字起こしが台本と合う）" in out else ("要耳" if "要耳" in out else f"?（exit {p.returncode}）")
            # 🔴 2026-09-23: 最初は「最後のテイク」の聞取を出していた＝c210-2 で**採られていない**正しいテイクを見せ、
            #    キャッシュに入った悪いテイク（1が落ちた take1）を隠した。採られたテイクの聞取は el_yomi.tsv に書き戻される
            heard = ""
            for row in (ROOT / "audio" / "el_qa" / "ep12_el_yomi.tsv").read_text(encoding="utf-8").splitlines():
                c = row.split("\t")
                if c[0] == lid:
                    heard = "採った聞取: " + c[3]
            if "少数派" in out:
                heard = "🔴少数派 " + heard
            results.append((lid, verdict, heard))
            print(f"{lid:8s} {verdict:4s} {heard[:70]}", flush=True)
    used, _ = el_tts.credits_used()
    ok = sum(1 for r in results if r[1] == "採用")
    print(f"\n回した {len(results)}行 ／ 採用 {ok} ／ 要耳ほか {len(results) - ok} ／ ⑤aの消費 {used - BASE:,}（上限の線 {CAP - BASE:,}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
