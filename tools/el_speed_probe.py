# -*- coding: utf-8 -*-
"""el_speed_probe.py — ElevenLabs の `speed` が**尺に何倍効くか**を実際に合成して測る（2026-09-08）。

■ なぜ要るか（6本目③・話速を 1.05 に上げるため）
    `check_script.CPS_FALLBACK = 5.37` は **6.12 × 1.0/1.14 の割り算による推定**であって実測ではない。
    同じ理屈で「1.05 なら 5.37 × 1.05 = 5.64」と書くと、**推定の上に推定を積む**ことになる。
    → [[feedback-dont-state-inferences-as-findings]]
    speed が尺に線形に効く保証はどこにも無いので、**同じ文を両方の速さで合成して割る**。

■ 何を測るか
    | 量 | 意味 |
    |---|---|
    | `ratio` | 1.05 の秒 ÷ 1.00 の秒。**線形なら 1/1.05 = 0.952** |
    | `cps_100` / `cps_105` | 文字 ÷ 秒（前後の無音は `el_tts._trim` が切ったあと） |
    | `jitter` | 同じ文・同じ設定を2回引いたときの秒のばらつき。**物差しの誤差** |

■ ⚠️ 物差しをまず疑う（[[feedback-verify-your-own-instrument]]）
    eleven_v3 は非決定的で、同じ文でもテイクごとに秒が動く。`jitter` を先に出して、
    **`ratio` の差が jitter より大きいこと**を確かめてから採る。小さければ「測れていない」と書く。

■ クレジット
    行数 × (2 + --jitter) 回の合成。既定 24行なら約 1,200〜1,700字。
    残量は `python -c "import sys;sys.path.insert(0,'tools');import el_tts;print(el_tts.credits_used())"`。

■ 使い方
    python tools/el_speed_probe.py --n 24 --speeds 1.0,1.05 --out analytics/el_speed_probe.json
    python tools/el_speed_probe.py --dry            … 何字投げるかだけ出す（API 不使用）
    python tools/el_speed_probe.py --show analytics/el_speed_probe.json
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import el_tts  # noqa: E402
import narration  # noqa: E402

SR = 24000
BASE = dict(el_tts_settings=None)


def sample_lines(n: int):
    """narration.SCRIPT から長さの分布をまたいで n 行を採る（先頭に固まらせない）."""
    ls = []
    for cid, lines in narration.SCRIPT:
        for i, t in enumerate(lines, 1):
            t = t.replace("★", "").strip()
            if 12 <= len(t) <= 60:
                ls.append((f"{cid}-{i}", t))
    ls.sort(key=lambda x: len(x[1]))
    if n >= len(ls):
        return ls
    step = len(ls) / n
    return [ls[int(i * step)] for i in range(n)]


def settings_for(speed: float):
    import el_script
    s = dict(el_script.SETTINGS)
    s["speed"] = speed
    return s


def sec_of(pcm: bytes) -> float:
    return len(pcm) / 2 / SR


def run(n: int, speeds, jitter: int, out: Path):
    rows = []
    picks = sample_lines(n)
    for lid, text in picks:
        rec = {"lid": lid, "chars": len(text), "text": text}
        for sp in speeds:
            pcm = el_tts.synth(text, scene_id=lid, slug=f"probe{int(sp*100)}",
                               settings=settings_for(sp))
            rec[f"s{sp}"] = round(sec_of(pcm), 3)
        rows.append(rec)
        print(f"  {lid:9s} {len(text):3d}字 " +
              " ".join(f"{sp}={rec['s'+str(sp)]:6.2f}s" for sp in speeds))
    # 物差しの誤差＝同じ文・同じ設定をもう一度引く
    jit = []
    for lid, text in picks[:jitter]:
        pcm = el_tts.synth(text, scene_id=lid + "-j", slug="probejit",
                           settings=settings_for(speeds[0]), refresh=True)
        base = next(r for r in rows if r["lid"] == lid)[f"s{speeds[0]}"]
        jit.append(abs(sec_of(pcm) - base) / base)
    res = {"speeds": speeds, "rows": rows,
           "jitter_pct": round(100 * st.median(jit), 2) if jit else None,
           "jitter_n": len(jit)}
    for sp in speeds:
        c = sum(r["chars"] for r in rows)
        s = sum(r[f"s{sp}"] for r in rows)
        res[f"cps_{sp}"] = round(c / s, 3)
    if len(speeds) == 2:
        r = [rows_r[f"s{speeds[1]}"] / rows_r[f"s{speeds[0]}"] for rows_r in rows]
        res["ratio_median"] = round(st.median(r), 4)
        res["ratio_mean"] = round(st.fmean(r), 4)
        res["ratio_sd"] = round(st.pstdev(r), 4)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    show(res)
    return res


def show(res):
    sp = res["speeds"]
    print("\n=== 実測")
    for s in sp:
        print(f"  speed {s}: {res[f'cps_{s}']} 文字/秒")
    if "ratio_median" in res:
        print(f"  秒の比 {sp[1]}÷{sp[0]} = 中央値 {res['ratio_median']} "
              f"／平均 {res['ratio_mean']} ／標準偏差 {res['ratio_sd']}"
              f"（線形なら {1/sp[1]*sp[0]:.4f}）")
    if res.get("jitter_pct") is not None:
        print(f"  物差しの誤差（同じ文の引き直し {res['jitter_n']}件）中央値 {res['jitter_pct']}%")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=24)
    ap.add_argument("--speeds", default="1.0,1.05")
    ap.add_argument("--jitter", type=int, default=6)
    ap.add_argument("--out", default="analytics/el_speed_probe.json")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--show")
    a = ap.parse_args()
    if a.show:
        show(json.loads(Path(a.show).read_text(encoding="utf-8")))
        return 0
    speeds = [float(x) for x in a.speeds.split(",")]
    picks = sample_lines(a.n)
    chars = sum(len(t) for _, t in picks)
    jc = sum(len(t) for _, t in picks[:a.jitter])
    print(f"行 {len(picks)}／1回ぶん {chars}字／投げる合計 "
          f"{chars*len(speeds)+jc}字（速さ {len(speeds)}通り＋引き直し {a.jitter}件）")
    print(f"クレジット残 {el_tts.credits_used()}")
    if a.dry:
        return 0
    run(a.n, speeds, a.jitter, ROOT / a.out)
    print(f"クレジット残（後）{el_tts.credits_used()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
