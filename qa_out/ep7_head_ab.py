# -*- coding: utf-8 -*-
"""ep7_head_ab.py — ⑤a の頭で1回だけ回す A/B（この回かぎりの道具）。

■ 何を確かめるか（②③ `ref/ep7/kousei.md` §4.5 の宿題）
    声が Hiro → **Koichi** に替わり、`stability` が **0.85 → 0.64** に下がった。
    「表情は出るが振れも大きくなる」ので、**6本目より悪くなっていないか**を全編を焼く前に測る。

■ 測るもの（3つ。どれも「件数」ではなく**値**で見る＝feedback-verify-your-own-instrument）
    | 量 | 見方 |
    |---|---|
    | 秒・文字/秒 | 中央値と**ばらつき（jitter）**。ばらつきより小さい差は「測れていない」 |
    | 異音（`el_artifacts.blips`） | **`el_tts.synth` を通さない**＝振り直しで隠れる前の**素の発生率** |
    | 聞取（Scribe） | 台本の字が出るか。⚠️ Scribe 自身が誤るので合否は決めない（当たりを付けるだけ） |

■ ⚠️ 物差しの注意
    - `el_tts.synth()` は異音があると最大3回振り直す。**それを通すと素の発生率が見えない**ので
      ここは `_post` → `_trim` を直に呼ぶ。キャッシュにも入れない（本番の鍵を汚さない）。
    - 陽性対照＝**stability 0.85（6本目 Hiro の値）を同じ文・同じ回数で引く**。
      0.64 だけ測って「問題なし」と書かない（比べる相手が無い数字は判断に使えない）。
    - ⚠️ 声は Koichi のまま両方引く。**声と stability を同時に動かさない**（どちらのせいか分からなくなる）。

■ クレジット
    6行 × 3テイク × 2設定 ＝ 約 940字 ≒ **520クレジット**（+ Scribe 12行 ≒ 10）。
    `--dry` で投げる字数だけ出す（API 不使用）。

  python qa_out/ep7_head_ab.py --dry
  python qa_out/ep7_head_ab.py --takes 3
"""
import json
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import el_artifacts as ART      # noqa: E402
import el_check_yomi as CY      # noqa: E402  stt()
import el_script as ES          # noqa: E402
import el_tts                   # noqa: E402

ES.gate_args({"--dry", "--takes"}, paid=True)
DRY = "--dry" in sys.argv
TAKES = int(sys.argv[sys.argv.index("--takes") + 1]) if "--takes" in sys.argv else 3

# 🔴 危ない型を1本ずつ（el_prelint の当たりから選んだ。全部この台本の実文）
PICK = ["c216-3",   # 小数「1.2倍」＝4本目の実測で「点が落ちる」型
        "c222-1",   # 文頭の数字「8時46分」＋ F-15 ＋ 基地名（オーティス）
        "c417-1",   # 全角括弧の単位換算「8キロ（5マイル）」＋ 西南西
        "c507-2",   # 「いま飛んでいる」＝ ep007「いま動かせる」と同じ型
        "c216-2",   # 文頭「委員会報告」＋ 桁区切り「1,350フィート」
        "c619-1"]   # 文頭「操縦室」＋「音声記録装置」
AB = [("本番 stability 0.64", dict(ES.SETTINGS)),
      ("対照 stability 0.85（6本目の値）", dict(ES.SETTINGS, stability=0.85))]


def main() -> int:
    by_id = ES.by_id()
    rows = [by_id[i] for i in PICK]
    chars = sum(len(ES.el_text(l.text)) for l in rows) * TAKES * len(AB)
    print(f"投げる字数 {chars:,}字 ≒ {chars * 0.55:,.0f} クレジット（{TAKES}テイク × {len(AB)}設定）")
    if DRY:
        for l in rows:
            print(f"  {l.lid}  {len(l.text):>3}字  {l.text}")
        return 0

    used0, lim = el_tts.credits_used()
    out = []
    for label, stg in AB:
        print(f"\n── {label} ─────────────────────────")
        for l in rows:
            sent = ES.el_text(l.text)
            secs, blips, best = [], [], None
            for t in range(TAKES):
                pcm = el_tts._trim(el_tts._post(sent, stg))
                pcm = ES.shipped(pcm)                  # 🔴 出荷する音（atempo 後）で測る
                sec = len(pcm) / 2 / ES_SR
                b = ART.blips(ART.inspect_struct(pcm))
                secs.append(sec)
                blips.append(len(b))
                if best is None or len(b) < best[1]:
                    best = (pcm, len(b))
                for x in b:
                    print(f"    ⚠️ 異音 {l.lid} take{t+1}: {x['msg']}")
            heard = CY.stt(best[0])
            med = st.median(secs)
            jit = (max(secs) - min(secs)) / med * 100
            print(f"  {l.lid}  {med:.2f}秒 ±{jit:.1f}%  {len(l.text)/med:.2f}字/秒  "
                  f"異音 {sum(blips)}/{TAKES}")
            print(f"      台本: {l.text}")
            print(f"      聞取: {heard}")
            out.append({"setting": label, "lid": l.lid, "text": l.text, "heard": heard,
                        "secs": [round(s, 3) for s in secs], "blips": blips,
                        "cps": round(len(l.text) / med, 3), "jitter_pct": round(jit, 2)})

    p = ROOT / "qa_out" / "ep7_head_ab.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {p}")
    print("\n── まとめ（値で比べる。件数だけで判断しない）──────────")
    for label, _ in AB:
        g = [r for r in out if r["setting"] == label]
        cps = [r["cps"] for r in g]
        print(f"  {label}: 文字/秒 中央値 {st.median(cps):.3f}（{min(cps):.2f}〜{max(cps):.2f}）"
              f"／ばらつき 中央値 {st.median([r['jitter_pct'] for r in g]):.1f}%"
              f"／異音 {sum(sum(r['blips']) for r in g)}/{len(g)*TAKES}テイク")
    used1, _ = el_tts.credits_used()
    print(f"クレジット {used0:,} → {used1:,}（消費 {used1-used0:,}／上限 {lim:,}）")
    return 0


ES_SR = el_tts.SR

if __name__ == "__main__":
    sys.exit(main())
