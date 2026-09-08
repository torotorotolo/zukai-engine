# -*- coding: utf-8 -*-
"""章ファイルが**本当に読めていて、台本と1対1か**を見る（2026-09-08 新設・6本目 ⑤b）。

■ なぜ要るか（この日に実際に踏んだ）
  `cuts/ss.py` から `scene_jiko` を import したせいで循環参照になり、
  **`cuts/pr.py` と `cuts/c1.py` が丸ごと読めなくなった。**
  ところが `cuts/__init__.py` は例外を握って `BROKEN` に入れるだけなので、
  `check_layout.py` は**空の SPEC を調べて「✓ 全部おさまっている」**を出した。
  ＝ [[feedback-gates-blind-to-the-new-material]] の「0件を調べて合格」そのもの。

■ 見るもの（どれか1つでも欠けたら exit 2）
  1. 🔴 `cuts.BROKEN` が空（章ファイルが1つも落ちていない）
  2. 🔴 カットIDが `audio/narration.json` と**過不足なく一致**する
     ＝ 台本にあって画が無い／画があって台本に無い、を両方向で見る
     ⚠️ カットIDは題材をまたいでぶつかるので、**前の題材の図が黙って出る**のを
        ここで止める（[[project-jiko-rules-index]] §0b）
  3. 🔴 写真映像の割合が **45〜50%**（事故検証chの規則。[[feedback-jiko-photo-ratio]]）
     写真映像＝`photo=` を持つカット（実写・報告書の図・地に敷いた図解のすべて）

■ 使い方
    python tools/check_cuts.py
    python tools/check_cuts.py --selftest    # 物差しの検算（陽性対照つき）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
NARRATION = HERE / "audio" / "narration.json"

# 事故検証ch の規則（2026-08-03 カズヤくん）。⚠️ ここを緩めるときは記憶のほうも直す
PHOTO_MIN, PHOTO_MAX = 0.45, 0.50


def script_cuts():
    """台本のカットID（`narration.json` の順）。**画の側ではなく音の側を正とする。**"""
    d = json.loads(NARRATION.read_text(encoding="utf-8"))
    ids = list(d.get("durations") or {})
    if not ids:
        raise RuntimeError(f"{NARRATION} からカットIDを取り出せない（鍵＝{list(d)}）")
    return ids


def check(spec=None, broken=None, want=None):
    """(見つけたことの一覧, 最悪の exit) を返す。"""
    import cuts
    spec = cuts.SPEC if spec is None else spec
    broken = cuts.BROKEN if broken is None else broken
    want = script_cuts() if want is None else want
    out, code = [], 0

    # 1. 章ファイルが読めているか
    if broken:
        for name, e in broken.items():
            out.append(f"🔴 cuts/{name}.py が読めていない: {e}")
        code = 2
    else:
        out.append(f"✓ 章ファイルは全部読めている（{len(spec)}カット）")

    # 2. 台本と1対1か
    miss = [c for c in want if c not in spec]           # 台本にあって画が無い
    extra = [c for c in spec if c not in want]          # 画があって台本に無い
    if miss:
        out.append(f"🔴 画が無いカット {len(miss)}件: {miss[:12]}"
                   + ("…" if len(miss) > 12 else ""))
        code = 2
    if extra:
        out.append(f"🔴 台本に無いカットID {len(extra)}件: {extra[:12]}"
                   + ("…" if len(extra) > 12 else ""))
        code = 2
    if not miss and not extra:
        out.append(f"✓ 台本と1対1（{len(want)}カット）")

    # 3. 写真映像の割合
    #    ⚠️ 台本と1対1でないうちは割合を出しても意味が無いので、そのときは測るだけ
    photo = [c for c, s in spec.items() if s.get("photo")]
    r = len(photo) / max(1, len(spec))
    ok = PHOTO_MIN <= r <= PHOTO_MAX
    mark = "✓" if ok else ("⚠️" if miss or extra else "🔴")
    out.append(f"{mark} 写真映像 {len(photo)}/{len(spec)} ＝ {r * 100:.1f}%"
               f"（規則 {PHOTO_MIN * 100:.0f}〜{PHOTO_MAX * 100:.0f}%）")
    if not ok and not (miss or extra) and not broken:
        code = max(code, 2)
    return out, code


def selftest():
    """🔴 物差しそのものを検算する。**陽性対照＝わざと壊した入力で鳴ること**。"""
    ok = []

    def chk(name, got):
        ok.append(bool(got))
        print(f"  {'✓' if ok[-1] else '🔴'} {name}")

    want = ["a1", "a2", "a3", "a4"]
    good = {c: dict(photo="x.jpg") for c in want[:2]}
    good.update({c: dict(fig=("panel", {})) for c in want[2:]})
    _o, c = check(spec=good, broken={}, want=want)
    chk("陽性対照：50%ちょうどは通る", c == 0)

    _o, c = check(spec=good, broken={"c1": ValueError("boom")}, want=want)
    chk("陽性対照：章ファイルが落ちていたら止まる", c == 2)

    short = {c_: v for c_, v in list(good.items())[:3]}
    _o, c = check(spec=short, broken={}, want=want)
    chk("陽性対照：台本より画が少なければ止まる", c == 2)

    lean = {c: dict(fig=("panel", {})) for c in want}
    lean["a1"] = dict(photo="x.jpg")
    _o, c = check(spec=lean, broken={}, want=want)
    chk("陽性対照：写真25%は止まる", c == 2)

    chk("台本のカットIDが読める（本番の narration.json）", len(script_cuts()) > 0)
    good_all = all(ok)
    print("  " + (f"✓ 検算 {len(ok)}/{len(ok)}" if good_all
                  else f"🔴 検算 {sum(ok)}/{len(ok)} で落ちた"))
    return good_all


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(0 if selftest() else 1)
    rows, rc = check()
    print("■ 章ファイルと台本の照合")
    for r in rows:
        print("  " + r)
    print("  " + ("✓ 通った" if rc == 0 else "🔴 落ちた"))
    sys.exit(rc)
