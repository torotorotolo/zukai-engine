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
    """(x0, y0, x1, y1, 文字, レイヤー名, 書体, フチの有無) を返す。**すべて実測値**。"""
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
        # フチ（paint-order="stroke fill"）が付いていれば、下を線が通っても読める
        out.append((x0, y - up, x0 + w, y + dn, t, layer, fam,
                    "paint-order" in a))
    return out


def main(only=None):
    jobs, _ = S.build_layers(allow_missing=True)
    if only:
        jobs = {k: v for k, v in jobs.items() if k.startswith(only)}
    bad = ov = tofu = 0

    print(f"── 画面から出ている文字（{len(jobs)}レイヤー） ──")
    for k in sorted(jobs):
        for x0, y0, x1, y1, t, _, _, _ in boxes(jobs[k], k):
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
        for _, _, _, _, t, _, fam, _ in boxes(jobs[k], k):
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

    # ── 🔴 図形が文字を横切っていないか（2026-08-02 追加） ──────────
    #    この道具は**文字どうし**しか見ていなかったので、
    #      ・depth の潜水艇の絵が「浮上している途中」の上に乗る
    #      ・absent/seat の ✗ が枕の文字に重なる
    #    を2回とも通してしまい、焼いて目で見て初めて分かった。
    #    ⚠️ 判定は「**部分的に**重なるもの」だけ。文字をすっぽり含む塗りは
    #       札やパネルの地なので正しい（含む場合は数えない）。
    # 🔴 最初これを重ね順を見ずに書いたら **40件以上**出た。ほとんどが
    #    「先に引いた罫や帯の上に、あとから文字を載せた」＝正しい絵だった。
    #    （[[feedback-verify-your-own-instrument]]：全部NGと出たら道具を疑う）
    #    → 合成は base → lab → a1 → a2 … → hot の順に重なるので、
    #      **文字より「あと」に描かれる図形が覆う場合だけ**を数える。
    def order(layer):
        tail = layer.rsplit("_", 1)[-1]
        if tail == "base":
            return 0
        if tail == "lab":
            return 1
        if tail == "hot":
            return 999
        return 1 + int(tail[1:]) if tail[:1] == "a" and tail[1:].isdigit() else 1

    # 🔴 2回目の作り直し：「幾何が交わるか」ではなく「**読めなくなるか**」を測る。
    #    フチが付いた文字（`paint-order`）と、同じレイヤーで地を敷いた文字は守られている。
    import check_box as CB
    cross = 0
    guard = defaultdict(list)                  # レイヤーごとの「地」の矩形
    for k, svg in jobs.items():
        for fx, fy, fw, fh, op, col in CB.parse(svg, k)[3]:
            if col.lower() in CB.GROUND_FILLS and op >= 0.55 and fw > 40:
                guard[k].append((fx, fy, fx + fw, fy + fh))
    print("\n── 図形が文字を横切っている ──")
    bymark = defaultdict(list)
    for k, svg in jobs.items():
        if k.endswith("_base"):
            continue
        cid = k.rsplit("_", 1)[0]
        for m in CB.parse(svg, k)[1]:
            kind, *v = m
            xs = [p[0] for p in v[0]] if kind == "pts" else [v[0], v[2]]
            ys = [p[1] for p in v[0]] if kind == "pts" else [v[1], v[3]]
            if not xs or max(xs) - min(xs) > 1400 or max(ys) - min(ys) > 800:
                continue                       # 地の方眼・全画面の帯は対象外
            # 🔴 曲線を**外接矩形**で見ていたら、離れて弧を描く引き出し線が
            #    文字を横切っていることになった（c101 の地図の航路）。
            #    線は**線上の点**で判定する。塗り・箱だけ矩形で見てよい。
            bymark[cid].append(("pts" if kind == "pts" else "box",
                                v[0] if kind == "pts" else (v[0], v[1], v[2], v[3]),
                                k))
    for cid in sorted(bycut):
        for t in bycut[cid]:
            if t[7]:
                continue                       # フチ付き＝下を線が通っても読める
            if any(gx0 <= t[0] + 2 and gy0_ <= t[1] + 2 and gx1 >= t[2] - 2
                   and gy1_ >= t[3] - 2
                   for gx0, gy0_, gx1, gy1_ in guard.get(t[5], [])):
                continue                       # 同じレイヤーで地を敷いてある
            for kind, geo, mk in bymark.get(cid, []):
                if order(mk) <= order(t[5]):
                    continue                   # 文字のほうがあとに乗る＝隠れない
                if kind == "pts":
                    hit = sum(1 for px_, py_ in geo
                              if t[0] + 4 < px_ < t[2] - 4 and t[1] + 4 < py_ < t[3] - 4)
                    if hit < 3:
                        continue
                    cross += 1
                    print(f"  🔴 {cid}: 「{t[4][:16]}」({t[5]}) の中を {mk} の線が "
                          f"{hit}点ぶん通る")
                    continue
                mx0, my0, mx1, my1 = geo
                ix = min(t[2], mx1) - max(t[0], mx0)
                iy = min(t[3], my1) - max(t[1], my0)
                if ix <= 8 or iy <= 8:
                    continue
                if mx0 <= t[0] + 2 and my0 <= t[1] + 2 and mx1 >= t[2] - 2 \
                        and my1 >= t[3] - 2:
                    continue                   # 文字をすっぽり含む＝札の地
                cross += 1
                print(f"  🔴 {cid}: 「{t[4][:16]}」({t[5]}) を {mk} の図形が "
                      f"{ix:.0f}×{iy:.0f}px 覆う")
    if not cross:
        print("  ✓ 横切っている図形は無い")

    n = bad + ov + tofu + cross
    print(f"\n{'🔴 直すところあり' if n else '✓ 机上の検算はすべて通った'}"
          f"（画面外 {bad}件・重なり {ov}件・豆腐 {tofu}件・図形が横切る {cross}件）")
    return 1 if n else 0


if __name__ == "__main__":
    only = next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")), None)
    sys.exit(main(only))
