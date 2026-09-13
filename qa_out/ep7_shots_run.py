# -*- coding: utf-8 -*-
"""ep7_shots_run.py — RG237 32本のショットの境目を1秒刻みで採る（2026-09-13 ⑤b-1）。

`ref/ep7/shots.json` を作る。`footage.SHOTS` がここを読む（`footage.SHOT_FILE`）。

■ なぜ CLI（`tools/shots.py probe`）を使わないか
    🔴 `shots.py main()` は `shots_of(Path(a.target))` と**URL を Path に通す**。
       Windows では `https://…` が `https:\…` に潰れて ffmpeg に届かない。
       `shots_of()` の docstring 自身が「URL を Path() に通すと Windows で潰れる」と
       書いてあるのに、main がそれをやっている。→ ここでは `shots_of(url)` を直に呼ぶ。

■ 🔴 鍵は**拡張子つき**（②素材 §1-4）
    同じ naId に `.mp4` と `.mpg` の2点があるので、拡張子を落とすと1点消える。
    検算＝「**32点**」と「**10,740.9秒**」の両方。

■ 使い方
    python qa_out/ep7_shots_run.py            # 未取得のクリップだけ測る（続きから）
    python qa_out/ep7_shots_run.py --only=<鍵>
    python qa_out/ep7_shots_run.py --verify    # 台帳の検算だけ（網に出ない）
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import footage as F                                            # noqa: E402
import shots as SH                                             # noqa: E402

OUT = HERE / "ref" / "ep7" / "shots.json"
WANT_N, WANT_SEC = 32, 10740.9          # ②の実測（陽性対照）


def load():
    return json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}


def save(d):
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def verify(d):
    """🔴 台帳そのものを検算する。**件数だけでなく秒の合計でも見る**。"""
    ng = []
    if len(F.CLIPS) != WANT_N:
        ng.append(f"clips.json が {len(F.CLIPS)}点（②の実測は {WANT_N}点）")
    tot = sum(float(c["sec"]) for c in F.CLIPS.values())
    if abs(tot - WANT_SEC) > 1.0:
        ng.append(f"clips.json の秒の合計 {tot:.1f}（②の実測は {WANT_SEC}）")
    print(f"■ clips.json {len(F.CLIPS)}点／{tot:.1f}秒"
          f"（②の実測 {WANT_N}点・{WANT_SEC}秒）")
    done = 0
    for k, v in sorted(d.items()):
        if k not in F.CLIPS:
            ng.append(f"{k} は clips.json に無い鍵（拡張子を落としていないか）")
            continue
        want = float(F.CLIPS[k]["sec"])
        got = float(v["dur"])
        # ⚠️ 1秒刻みで数えた「コマ数」なので ±2秒は誤差。それ以上は読めていない
        if abs(got - want) > 2.5:
            ng.append(f"{k}: 測れた尺 {got:.1f}秒 ≠ 台帳 {want:.1f}秒")
        n = len(v["shots"])
        # 🔴 「長いのにショットが1本」は**2通りある**。分けないと正しいものを落とす。
        #   (a) 画面収録（ZOB-ARTCC・System の起動停止）＝**切り替えが無いのが正しい**。
        #       683秒の連続したレーダー画面に「20本未満なら読めていない」を当てると誤報。
        #       ここは**尺が合っているか**（上の ±2.5秒）で「読めた」を判定する。
        #   (b) 記録映画で1本＝ディゾルブを見落としている疑い（4本目で踏んだ型）。
        #   ⚠️ 動いているかは別の物差しで測る＝`qa_out/ep7_shotscan.py motion`
        #      （64×36 の署名では、数画素の機影は動いていても 0.0 に見える）。
        scr = "ARTCC" in k or "System-" in k
        if n < 2 and want > 60 and not scr:
            ng.append(f"{k}: {want:.0f}秒でショットが {n} 本＝読めていない疑い")
        done += 1
    n_sh = sum(len(v["shots"]) for v in d.values())
    print(f"■ ショットを測れたクリップ {done}/{len(F.CLIPS)}／ショットの合計 {n_sh}本")
    # 🔴 「0本を調べて合格」を出させない（fail closed）。
    #    ⚠️ `footage.unknown_clip()` は **USE に書いた欄のクリップ**しか見ないので、
    #       ここが素通りすると「まだ1本も測っていない」状態が緑に見える。
    if not done:
        ng.append("ショットを1本も測っていない＝この検算は何も見ていない")
    for m in ng:
        print(f"  🔴 {m}")
    print("✓ 台帳は整っている" if not ng else f"🔴 粗 {len(ng)}件")
    return 0 if not ng else 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--short", action="store_true",
                    help="200秒以下だけ（航跡レーダーの19本。ARTCC の画面収録を外す）")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    d = load()
    if a.verify:
        return verify(d)
    only = [x for x in a.only.split(",") if x]
    todo = [k for k in sorted(F.CLIPS) if (not only or k in only) and k not in d]
    if a.short:
        todo = [k for k in todo if float(F.CLIPS[k]["sec"]) <= 200]
    print(f"■ 測る {len(todo)}本（済み {len(d)}／全 {len(F.CLIPS)}）", flush=True)
    ng = 0
    for i, k in enumerate(todo, 1):
        c = F.CLIPS[k]
        t0 = time.time()
        # 🔴 `shots.MIN_CHOTS` の fail closed は**記録映画**のための網。
        #   ARTCC の画面収録（ZOB-ARTCC・システムの起動停止の tscc）は**切り替えが無いのが正しい**
        #   ＝ 25分の連続したレーダー画面。ここに「20本未満なら読めていない」を当てると、
        #      正しいものを落とす（→ [[feedback-verify-your-own-instrument]] 全部NGなら道具を疑う）。
        #   代わりの物差し＝**測れた尺が台帳の尺と合うか**（`verify()` の ±2.5秒）。
        #   こちらのほうが「ffmpeg が黙って0コマ返した」を強く見る。
        scr = "ARTCC" in k or "System-" in k
        keep_min = SH.MIN_CUTS
        try:
            if scr:
                SH.MIN_CUTS = 0
            shots, dur = SH.shots_of(c["url"])      # 🔴 URL は Path に通さない
        except SystemExit as e:                     # fail closed（境目が少なすぎる）
            print(f"  🔴 {i}/{len(todo)} {k}: {e}", flush=True); ng += 1; continue
        except Exception as e:                      # noqa: BLE001
            print(f"  🔴 {i}/{len(todo)} {k}: {e}", flush=True); ng += 1; continue
        finally:
            SH.MIN_CUTS = keep_min
        d[k] = dict(src=k, dur=round(dur, 2), shots=shots)
        save(d)                                     # 1本ずつ保存（落ちても続きから）
        print(f"  ✓ {i}/{len(todo)} {k}  {dur:.0f}秒／台帳 {float(c['sec']):.0f}秒  "
              f"ショット {len(shots)}本  {time.time() - t0:.0f}秒", flush=True)
    print(f"\n■ 測れなかった {ng}本")
    return verify(d) if not ng else 2


if __name__ == "__main__":
    sys.exit(main())
