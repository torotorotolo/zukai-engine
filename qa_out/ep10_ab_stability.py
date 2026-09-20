# -*- coding: utf-8 -*-
r"""Otani の stability を、**全編を焼く前に**難しい行だけで決める（2026-09-21・10本目⑥）。

■ なぜ要るか
  カズヤくん指示で声を Sho → **Otani** に替えた。ところが
    Sho の本番設定 … stability **1.0**（画面で試聴した実際の値を `/v1/history` から写した）
    Otani の既定   … stability **0.5**（声に保存された値。`/v1/history` に Otani の記録は0件）
  ＝**安定性が半分に下がる。**表情は出るが振れも大きく、読み間違いが増えうる。

  🔴 `SETTINGS` は**キャッシュの鍵に入る**（`el_script.py` §52）。
     全編を焼いたあとで値を変えると **11,541字ぶんをもう一度課金**することになる。
     口座の残りは 17,308 クレジット（合成1回で 6,348）＝**やり直す余裕は無い。**
     だから先に、いちばん転びやすい行だけで実測して決める。

■ 選んだ行（⑤a で EL_YOMI を当てた「転びやすい型」から）
  数のカナ書き（240キログラム・377時間・1,439人・7万1,136・396人・30分前）／
  固有名（三豊・瑞草区）／小数と単位（27.6メートル）／桁の大きい数（7万6,500人）

■ やること
  ① 各行を **stability 0.5 と 1.0 の2通り**で合成（`el_tts.synth(settings=...)`）
  ② それぞれ Scribe で文字起こし（`el_check_yomi.stt`）
  ③ 台本との一致率を並べ、**どちらが台本の数と語をそろえたか**を出す

⚠️ これは門番ではない。一致率だけで決めない（`el_check_yomi` の注意と同じ）。
   ⚠️ Scribe は同じ音を2回起こすと結果が変わる（キー橋 ⑤a 実測）。
      **1回の聞取で決めない**ので、各設定 `--rounds` 回ずつ起こして両方を出す。

■ 費用の見込み（口座の残り 17,308 クレジット）
  合成 = 選んだ行の字数 × 0.550 × 2通り ／ 聞取 = Scribe の実費
  既定の10行なら合成 ≈ 350 クレジット。**全編 6,348 の 6% 以下**で決められる。

    python qa_out/ep10_ab_stability.py            # 10行 × 2設定 × 2周
    python qa_out/ep10_ab_stability.py --dry      # 叩かずに、行と字数と見込みだけ出す
    python qa_out/ep10_ab_stability.py --rounds 1
"""
import difflib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import el_check_yomi as CY   # noqa: E402
import el_script as ES       # noqa: E402
import el_tts                # noqa: E402
import narration             # noqa: E402

# 🔴 ⑤a で EL_YOMI を当てた行＝この台本でいちばん転びやすい型
WANT = ["pr01-2",    # 瑞草区（ソチョく）
        "pr05-1",    # 三豊（サンプン）＝⑤a で「三分」に化けた行
        "pr06-1",    # 27.6メートル（小数＋単位）
        "pr07-1",    # 7万6,500人（桁の大きい数）
        "c304-2",    # 7万1,136平方メートル
        "c404-2",    # 240キログラム（ニヒャクヨンジュッキログラム）
        "c614-1",    # 1,439人
        "c814-2",    # 377時間
        "c910-1",    # 396人
        "c115-2"]    # その30分前（サンジュップン前）
A, B = 0.5, 1.0          # A＝Otani の既定 ／ B＝Sho と同じ安定側


def settings(stab):
    return dict(ES.SETTINGS, stability=stab)


def pick():
    out, d = [], {}
    for cid, lines in narration.SCRIPT:
        for i, t in enumerate(lines, 1):
            d[f"{cid}-{i}"] = t
    for lid in WANT:
        if lid not in d:
            raise SystemExit(f"🔴 行 {lid} が台本に無い。止める（行IDを取り直すこと）")
        out.append((lid, d[lid]))
    return out


def ratio(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio() * 100


def main():
    rows = pick()
    n = sum(len(ES.el_text(t)) for _, t in rows)
    print(f"行 {len(rows)}／送る字数 {n}／合成の見込み {round(n * 0.550) * 2} クレジット"
          f"（{A} と {B} の2通り）", flush=True)
    if "--dry" in sys.argv:
        for lid, t in rows:
            print(f"  {lid}  {len(ES.el_text(t)):3d}字  {ES.el_text(t)[:46]}")
        return 0
    rounds = 2
    if "--rounds" in sys.argv:
        rounds = int(sys.argv[sys.argv.index("--rounds") + 1])

    score = {A: 0.0, B: 0.0}
    out = ["場面\t安定性\t周\t一致率\t聞取"]
    for lid, text in rows:
        sent = ES.el_text(text)
        print(f"\n── {lid}\n   台本: {text}", flush=True)
        for stab in (A, B):
            pcm = el_tts.synth(sent, scene_id=f"{lid}@{stab}", slug="ep10ab",
                               settings=settings(stab))
            best = []
            for r in range(rounds):
                heard = CY.stt(pcm)
                best.append((ratio(text, heard), heard))
                out.append(f"{lid}\t{stab}\t{r + 1}\t{best[-1][0]:.1f}\t{heard}")
            avg = sum(x for x, _ in best) / len(best)
            score[stab] += avg
            mark = "A（既定 0.5）" if stab == A else "B（安定 1.0）"
            print(f"   {mark} 一致率 {avg:5.1f}%", flush=True)
            for i, (rt, h) in enumerate(best, 1):
                print(f"      {i}周目 {rt:5.1f}%  {h}", flush=True)

    p = HERE / "qa_out" / "ep10_ab_stability.tsv"
    p.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"\n■ 合計（{len(rows)}行の平均）")
    for stab in (A, B):
        print(f"   stability {stab} … {score[stab] / len(rows):5.2f}%")
    print(f"→ {p}")
    print("⚠️ 一致率だけで決めない。上の聞取を読んで、**台本の数と語がそろっているか**で決める。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
