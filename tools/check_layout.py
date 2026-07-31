# -*- coding: utf-8 -*-
"""レンダリング前に、文字の位置を机上で検算する。

なぜ要るか：
  レンダリングはクラウドだけ。226カットを焼くと数分かかるうえ、
  「文字が画面外で切れる」「詰めたら注記どうしが重なった」は**字幅で分かる**ので、
  クラウドに投げる前にここで落とす。

🔴 字幅は**推定しない。フォントから実測する**（tools/fontmetrics.py）。
   推定して2回事故っている：
     ① Dela の数字を 0.72em と見て「75,00089,680」に読める画を通した
     ② Noto Black のインクを 0.72em と見てサムネの赤と黄が上下にはみ出した
   しかも「実測 0.84em」もまだ平均でしかなかった。
   **Dela の数字は 0.588（1）〜0.924（4）で 1.57 倍ちがう。**

やること：
  1 scene_jiko が組んだ全レイヤーの SVG から <text> を拾う
  2 実測の字幅と字面で外接矩形を出す
  3 画面（MG〜RIGHT・上52〜下906）から出ているものを名指しする
  4 **同じカットで同時に出ているレイヤー**どうしの重なりを名指しする
  5 フォントに無い字（豆腐になる字）を名指しする

⚠️ ここを通っても**必ずクラウドで焼いて拡大目視する**（この道具は目視の代わりではない）。
   重なり判定は矩形どうしなので、文字の隙間に入る飾り罫までは分からない。
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J
import fontmetrics as fm
import scene_jiko as S

TOP, BOT = 44, 906           # 字幕帯(900)より上。
# 見出しは全カット共通で y=104・Dela 62px。字面の上端は字によって 49〜54px に来る
# （実測。「残」「炭」のように背の高い字だと 51px）。ここは意図した位置なので下限を 44 に置く。
TEXT = re.compile(r'<text\s([^>]*)>([^<]*)</text>')
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
UNESC = {"&amp;": "&", "&lt;": "<", "&gt;": ">"}


def unesc(t):
    for k, v in UNESC.items():
        t = t.replace(k, v)
    return t


def boxes(svg, layer):
    """(x0, y0, x1, y1, 文字, レイヤー名, 書体) を返す。**すべて実測値**。"""
    out = []
    for m in TEXT.finditer(svg):
        a = dict(ATTR.findall(m.group(1)))
        t = unesc(m.group(2))
        if not t.strip():
            continue
        x, y = float(a["x"]), float(a["y"])
        size, fam = float(a["font-size"]), a.get("font-family", "Noto")
        w = fm.width(t, size, fam)
        up, dn = fm.ink(t, size, fam)
        anchor = a.get("text-anchor", "start")
        x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
        out.append((x0, y - up, x0 + w, y + dn, t, layer, fam))
    return out


def main(only=None):
    jobs, _ = S.build_layers(allow_missing=True)
    if only:
        jobs = {k: v for k, v in jobs.items() if k.startswith(only)}
    bad = ov = tofu = 0

    print(f"── 画面から出ている文字（{len(jobs)}レイヤー） ──")
    for k in sorted(jobs):
        for x0, y0, x1, y1, t, _, _ in boxes(jobs[k], k):
            why = []
            if x0 < J.MG - 4:
                why.append(f"左が {x0:.0f}（下限 {J.MG}）")
            if x1 > J.RIGHT + 4:
                why.append(f"右が {x1:.0f}（上限 {J.RIGHT}）")
            if y0 < TOP:
                why.append(f"上が {y0:.0f}")
            if y1 > BOT:
                why.append(f"下が {y1:.0f}")
            if why:
                bad += 1
                print(f"  🔴 {k}「{t[:22]}」… " + "／".join(why))
    if not bad:
        print("  ✓ 全部おさまっている")

    print("\n── フォントに無い字（豆腐になる） ──")
    for k in sorted(jobs):
        for _, _, _, _, t, _, fam in boxes(jobs[k], k):
            miss = fm.missing(t, fam)
            if miss:
                tofu += 1
                print(f"  🔴 {k}: {fam} に無い字 {miss}（「{t[:20]}」）")
    if not tofu:
        print("  ✓ 無い字は無い")

    print("\n── 同じカットで重なっている文字 ──")
    bycut = defaultdict(list)
    for k, svg in jobs.items():
        cid = k.rsplit("_", 1)[0]
        bycut[cid] += boxes(svg, k)
    for cid in sorted(bycut):
        bs = bycut[cid]
        for i in range(len(bs)):
            for j in range(i + 1, len(bs)):
                a, b = bs[i], bs[j]
                ix = min(a[2], b[2]) - max(a[0], b[0])
                iy = min(a[3], b[3]) - max(a[1], b[1])
                if ix > 6 and iy > 6:
                    ov += 1
                    print(f"  🔴 {cid}: 「{a[4][:16]}」({a[5]}) と "
                          f"「{b[4][:16]}」({b[5]}) が {ix:.0f}×{iy:.0f}px 重なる")
    if not ov:
        print("  ✓ 重なりなし")

    n = bad + ov + tofu
    print(f"\n{'🔴 直すところあり' if n else '✓ 机上の検算はすべて通った'}"
          f"（画面外 {bad}件・重なり {ov}件・豆腐 {tofu}件）")
    return 1 if n else 0


if __name__ == "__main__":
    only = next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")), None)
    sys.exit(main(only))
