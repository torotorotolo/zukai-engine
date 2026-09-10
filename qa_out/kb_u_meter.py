# -*- coding: utf-8 -*-
"""⑤c' 2巡目の物差し ── **式を書き写さず、本当に描かせて SVG を読む**。

⚠️ `kb_look2_ansize.py` は `photo_ann()` の式を写していたので、**直しても同じ数字を出した**
   （2026-09-10 に実際にそうなった。直した直後に「62組」と出続けた）。
   [[feedback-verify-your-own-instrument]]。ここは全部 `<text font-size=...>` を読む。

  python qa_out/kb_u_meter.py ann    … 写真注記：答え < ラベル／1枚の中の答えの開き
  python qa_out/kb_u_meter.py panel  … panel：段の級数の割れ／問い→答えの横の空き
  python qa_out/kb_u_meter.py node   … people：題 対 小見出し
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import fontmetrics as fm                                   # noqa: E402
import scene_jiko as S                                     # noqa: E402
import titan_fig as T                                      # noqa: E402
from cuts import SPEC                                      # noqa: E402

TEXT = re.compile(r'<text[^>]*?x="([-0-9.]+)"[^>]*?font-size="([0-9.]+)"'
                  r'[^>]*?>([^<]*)</text>')
SIZE = re.compile(r'font-size="([0-9.]+)"')


def ann():
    """写真カットの注記。ラベル(t) と 答え(v または v の無い段の d) の級数。"""
    under, spread = [], []
    for cid, sp in SPEC.items():
        if not sp.get("ann") or sp.get("panel"):
            continue
        blocks = S.photo_ann(sp)
        answers = []
        for a, blk in zip(sp["ann"], blocks):
            sizes = [float(m) for m in SIZE.findall(blk)]
            if not sizes:
                continue
            i = 0
            ts = sizes[i] if a.get("t") else 0.0
            if a.get("t"):
                i += 1
            if a.get("v"):
                ansz = sizes[i]
            elif a.get("d"):
                ansz = sizes[i]
            else:
                continue
            answers.append(ansz)
            if ts and ansz < ts - 0.5:
                under.append((cid, ts, ansz, a["t"], a.get("v") or a["d"]))
        if len(answers) >= 2 and max(answers) - min(answers) >= 24:
            spread.append((cid, max(answers) - min(answers), answers))
    print(f"🔴 答えがラベルより小さい ＝ {len(under)} 組")
    for cid, ts, az, t, v in sorted(under, key=lambda r: r[1] - r[2], reverse=True):
        print(f"  {cid}  ラベル{ts:.0f} 対 答え{az:.0f}  「{t}」→「{v[:26]}」")
    spread.sort(key=lambda r: -r[1])
    print(f"\n1枚の中で答えの級数が 24px 以上ひらく ＝ {len(spread)} カット")
    for cid, g, a in spread[:8]:
        print(f"  {cid}  開き{g:3.0f}px  {'/'.join(f'{x:.0f}' for x in a)}")


def _panel_specs():
    for cid, sp in SPEC.items():
        f = sp.get("fig")
        if f and f[0] == "panel":
            yield cid, f[1]


def panel():
    """段の本文の級数がカットの中で割れていないか／問い→答えの横の空き。"""
    split, tight, mixed = [], [], []
    for cid, kw in _panel_specs():
        fig = T.panel(**kw)
        bl = kw["blocks"]
        # ⚠️ 横の空きは**柱の枝（3段まで・短い t）だけ**で測る。4段以上は格子に落ち、
        #    答えがセルの右下に付くので同じ物差しは当たらない
        #    （1版目はこれで `c310` を −125px ＝「重なっている」と誤って出した）。
        pillar = len(bl) <= 3 and all(len(str(b.get("t", ""))) <= 46 for b in bl)
        # 型⑭ ＝ 同じ画面に「答えのある段」と「無い段」が混じる
        # ⚠️ 型⑭ は**柱の枝だけ**の粗。格子の枝は答えをセルの右下に置き、
        #    本文の幅（`avail`）が `v` の有無で変わらないので、右端は揃ったまま
        #    （1版目はこれで `c310` を偽陽性で出した）。
        haz = [bool(str(b.get("v", "")).strip()) for b in bl]
        if pillar and any(haz) and not all(haz):
            mixed.append((cid, sum(haz), len(bl)))
        # 本文の級数 ＝ 各段の <text> のうち k と v を除いたもの
        per = []
        for st, b in zip(fig.stages, kw["blocks"]):
            hits = TEXT.findall(st)
            body = [(float(sz), tx, float(x)) for x, sz, tx in hits
                    if tx and tx != str(b.get("k", "\0")) and tx != str(b.get("v", "\0"))]
            if body:
                per.append(max(s for s, _, _ in body))
            if b.get("v") and pillar:
                # 問い（本文）の右端 と 答え（v・右詰め）の左端
                vhit = [(float(sz), tx, float(x)) for x, sz, tx in hits
                        if tx == str(b["v"])]
                if body and vhit:
                    vs, vt, vx = vhit[0]
                    vleft = vx - fm.width(vt, vs, T.numfam(vt, "Dela"))
                    tright = max(x + fm.width(tx, s, "Noto") for s, tx, x in body)
                    tight.append((cid, vleft - tright, b["t"][:18], vt[:12]))
        if len(per) >= 2 and max(per) - min(per) >= 8:
            split.append((cid, max(per) - min(per), per))
    split.sort(key=lambda r: -r[1])
    print(f"🔴 1枚の中で段の級数が 8px 以上割れる ＝ {len(split)} カット")
    for cid, g, per in split[:12]:
        print(f"  {cid}  開き{g:5.1f}px  {'/'.join(f'{x:.0f}' for x in per)}")
    tight.sort(key=lambda r: r[1])
    print(f"\n🔴 問い→答えの横の空きが 100px 未満 ＝ "
          f"{sum(1 for r in tight if r[1] < 100)} 組（全 {len(tight)} 組）")
    for cid, g, t, v in tight[:10]:
        print(f"  {cid}  {g:6.1f}px  「{t}」→「{v}」")
    print(f"\n🔴 型⑭ 同じ画面に「答えのある段」と「無い段」が混じる ＝ "
          f"{len(mixed)} カット")
    for cid, k, n in mixed:
        print(f"  {cid}  {n}段中 {k}段だけ答えがある")


def node():
    """people の箱。題(t) 対 小見出し(d)。"""
    bad = []
    for cid, sp in SPEC.items():
        f = sp.get("fig")
        if not f or f[0] != "people":
            continue
        fig = T.people(**f[1])
        ns = f[1]["nodes"]
        stages = fig.stages[len(f[1].get("edges") or []):]
        for st, n in zip(stages, ns):
            if not n.get("d"):
                continue
            sizes = [float(m) for m in SIZE.findall(st)]
            if len(sizes) >= 2 and sizes[1] > sizes[0] + 0.5:
                bad.append((cid, sizes[0], sizes[1], n["t"], n["d"]))
    print(f"🔴 people の箱で 小見出し > 題 ＝ {len(bad)} 組")
    for cid, ts, ds, t, d in bad:
        print(f"  {cid}  題{ts:.0f} 対 小見出し{ds:.0f}  「{t}」/「{d}」")


if __name__ == "__main__":
    {"ann": ann, "panel": panel, "node": node}[sys.argv[1]]()
