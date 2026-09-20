# -*- coding: utf-8 -*-
"""⑤c-2 机上で全数：札（字の外接矩形）と、線・ほかの札との最短距離。描画はしない。

■ なぜ要るか
  記憶 `feedback-sheet-cannot-judge-three-types`（型③＝札が切れている／重なっている）。
  640px のシートでは決められない。**原寸を見る前に、式で全数に当てる**（9本目の教訓）。
  9本目は `qa_out/ep9_label_line_all.py` が mapfig・graph だけを見ていたが、
  10本目は mapfig が 1カットしか無く、panel/process/timeline/punch/layers/compare が主なので
  **図の型を問わず全カットに当てる**ように書き直した。

■ 9本目から変えた4点（どれも「見落とす向き」の誤差を潰すため）
  1. 字の外接矩形は fm.ink()（フォントの実測）。9本目の [-0.80em, +0.10em] は近似だった
  2. **塗りつぶしの三角（矢じり）も線として測る**。9本目は fill="none" のものしか見ていない
  3. **抜き板**（字の下に敷く BG 色の rect）を見て、線が板に隠れる組を分ける
  4. **札どうしの近接**も測る（check_layout は「重なった」しか鳴らない。c415 は近接）

■ 出し方
  すき間 ＝ 最短距離 − 線の太さ/2 − 字のフチの太さ/2。負＝線が字の外接矩形に入る。
"""
import re
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import fontmetrics as fm  # noqa: E402
fm.measured()                                    # 🔴 フォントを先に読む（check_layout と同じ理由）
import jiko_style as J  # noqa: E402
import scene_jiko as S  # noqa: E402
import check_layout as CL  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")

GRIDCOL = {"#22333f", "#41606f", "#1c2a35"}      # 方眼・沈めた罫。線として数えない
MINSW = 4.0                                      # これより細い罫は目盛り扱い
NEAR_LINE = 4.0                                  # 札と線：これ未満を出す
NEAR_TEXT = 10.0                                 # 札と札：これ未満を出す
ATTR = re.compile(r'([\w-]+)="([^"]*)"')

LAYER_ORDER = ["bg", "base", "lab"] + [f"a{i}" for i in range(1, 12)] + ["hot"]


def layer_rank(suffix):
    return LAYER_ORDER.index(suffix) if suffix in LAYER_ORDER else 99


def flatten(d):
    """path の d を折れ線の列に。M/L/H/V/h/l/v/Z だけ（この回はこれしか出ない）。"""
    toks = re.findall(r"([MLHVZmlhvz])|(-?[\d.]+)", d)
    polys, cur, x, y, start = [], [], 0.0, 0.0, None
    i, cmd = 0, None
    nums = []
    seq = []
    for c, n in toks:
        if c:
            seq.append(("c", c))
        else:
            seq.append(("n", float(n)))
    k = 0
    while k < len(seq):
        kind, v = seq[k]
        if kind == "c":
            cmd = v
            k += 1
            if cmd in "Zz":
                if start and cur:
                    cur.append(start)
                if len(cur) >= 2:
                    polys.append(cur)
                cur, start = [], None
            continue
        need = {"M": 2, "L": 2, "H": 1, "V": 1, "m": 2, "l": 2, "h": 1, "v": 1}.get(cmd, 2)
        nums = []
        while k < len(seq) and seq[k][0] == "n" and len(nums) < need:
            nums.append(seq[k][1])
            k += 1
        if cmd == "M":
            if len(cur) >= 2:
                polys.append(cur)
            x, y = nums
            cur, start = [(x, y)], (x, y)
            cmd = "L"
        elif cmd == "m":
            if len(cur) >= 2:
                polys.append(cur)
            x, y = x + nums[0], y + nums[1]
            cur, start = [(x, y)], (x, y)
            cmd = "l"
        elif cmd == "L":
            x, y = nums
            cur.append((x, y))
        elif cmd == "l":
            x, y = x + nums[0], y + nums[1]
            cur.append((x, y))
        elif cmd == "H":
            x = nums[0]
            cur.append((x, y))
        elif cmd == "h":
            x = x + nums[0]
            cur.append((x, y))
        elif cmd == "V":
            y = nums[0]
            cur.append((x, y))
        elif cmd == "v":
            y = y + nums[0]
            cur.append((x, y))
    if len(cur) >= 2:
        polys.append(cur)
    return polys


def seg_rect_dist(xa, ya, xb, yb, r):
    """線分と矩形の最短距離（交われば 0）。201点で刻む（9本目と同じ刻み）。"""
    t = np.linspace(0, 1, 201)
    x = xa + (xb - xa) * t
    y = ya + (yb - ya) * t
    dx = np.maximum(np.maximum(r[0] - x, 0), x - r[2])
    dy = np.maximum(np.maximum(r[1] - y, 0), y - r[3])
    return float(np.min(np.hypot(dx, dy)))


def rect_gap(a, b):
    """矩形どうしのすき間。負＝重なり量（小さいほう）。"""
    dx = max(b[0] - a[2], a[0] - b[2])
    dy = max(b[1] - a[3], a[1] - b[3])
    if dx >= 0 or dy >= 0:
        return float(np.hypot(max(dx, 0), max(dy, 0)))
    return float(max(dx, dy))                       # どちらも負＝重なっている


def marks_of(svg, rank):
    """描かれた線・面を (種別, 折れ線, 太さ, 色, 順番) で返す。"""
    out = []
    for m in re.finditer(r"<(path|rect|circle|line)\s([^>]*)/?>", svg):
        i = m.start()            # 🔴 並び順は**文字位置**で持つ。要素の通し番号だと
        #                           plates_of（rect だけを数える）と比べられない
        tag, a = m.group(1), dict(ATTR.findall(m.group(2)))
        col = a.get("stroke")
        sw = float(a.get("stroke-width", 0) or 0)
        fill = a.get("fill", "none")
        op = float(a.get("opacity", 1) or 1)
        seqno = (rank, i)
        if tag == "path":
            polys = flatten(a.get("d", ""))
            if col and col not in GRIDCOL and sw >= MINSW and op > 0.25:
                for p in polys:
                    out.append(("線", p, sw, col, seqno))
            # 塗りつぶしの小さな多角形＝矢じり。線として扱う（9本目は見ていなかった）
            if fill and fill != "none" and op > 0.25:
                for p in polys:
                    xs = [q[0] for q in p]
                    ys = [q[1] for q in p]
                    if max(xs) - min(xs) <= 60 and max(ys) - min(ys) <= 60:
                        out.append(("矢じり", p + [p[0]], 0.0, fill, seqno))
        elif tag == "rect":
            x, y = float(a.get("x", 0)), float(a.get("y", 0))
            w, h = float(a.get("width", 0)), float(a.get("height", 0))
            if col and col not in GRIDCOL and sw >= MINSW and op > 0.25:
                out.append(("枠", [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)],
                            sw, col, seqno))
        elif tag == "circle":
            cx, cy, r = float(a.get("cx", 0)), float(a.get("cy", 0)), float(a.get("r", 0))
            if col and col not in GRIDCOL and sw >= MINSW and op > 0.25:
                th = np.linspace(0, 2 * np.pi, 33)
                out.append(("丸", list(zip(cx + r * np.cos(th), cy + r * np.sin(th))),
                            sw, col, seqno))
    return out


def plates_of(svg, rank):
    """抜き板＝地の色で塗った rect（この上に字を置くと下の線が隠れる）。"""
    out = []
    for m in re.finditer(r"<rect\s([^>]*)/?>", svg):
        a = dict(ATTR.findall(m.group(1)))
        fill = a.get("fill", "none")
        op = float(a.get("opacity", 1) or 1)
        if fill in (J.BG, "#0f1922") and op >= 0.85:
            x, y = float(a.get("x", 0)), float(a.get("y", 0))
            w, h = float(a.get("width", 0)), float(a.get("height", 0))
            out.append(((x, y, x + w, y + h), (rank, m.start())))
    return out


def main():
    jobs, _ = S.build_layers()
    rows_line, rows_text = [], []
    n_cut_with_fig = 0
    for cid in S.ORDER:
        keys = [k for k in jobs if k.startswith(cid + "_")]
        if not keys:
            continue
        spec = S.SPEC.get(cid) or {}
        if spec.get("fig"):
            n_cut_with_fig += 1
        texts, marks, plates = [], [], []
        for k in keys:
            suf = k[len(cid) + 1:]
            rank = layer_rank(suf)
            # 🔴 字の並び順も**文字位置**で持つ（CL.boxes と同じ順・同じ飛ばし方で拾う）
            pos = [m.start() for m in CL.TEXT.finditer(jobs[k])
                   if CL.unesc(m.group(2)).strip()]
            bs = CL.boxes(jobs[k], k)
            assert len(pos) == len(bs), f"{k}: 字の数が合わない {len(pos)}≠{len(bs)}"
            for j, b in enumerate(bs):
                x0, y0, x1, y1, t, _, fam, outl = b
                texts.append(dict(r=(x0, y0, x1, y1), t=t, lay=suf, seq=(rank, pos[j]),
                                  outl=outl, fam=fam))
            marks += marks_of(jobs[k], rank)
            plates += plates_of(jobs[k], rank)
        # ── (A) 札 × 線 ────────────────────────────────
        for tx in texts:
            r = tx["r"]
            for kind, pts, sw, col, seq in marks:
                # 🔴 その札自身の器（丸や角の台座）は除く。
                #    除かないと「1」「2」「3」の記番と台座が全部 -2.0px で鳴り、
                #    本物（c113・c415）が埋もれる（記憶 feedback-gates-blind-spot-is-the-scan-direction
                #    「鳴りすぎる門番は鳴らない門番より危ない」）。
                xs = [q[0] for q in pts]
                ys = [q[1] for q in pts]
                if min(xs) <= r[0] and min(ys) <= r[1] and max(xs) >= r[2] and max(ys) >= r[3]:
                    continue
                d = min(seg_rect_dist(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], r)
                        for i in range(len(pts) - 1))
                gap = d - sw / 2 - (2.5 if tx["outl"] else 0.0)
                if gap >= NEAR_LINE:
                    continue
                # 抜き板が、線より後・字より先に敷かれて字の箱を覆っていれば線は隠れる
                hidden = any(p[0] <= r[0] and p[1] <= r[1] and p[2] >= r[2] and p[3] >= r[3]
                             and seq < ps < tx["seq"] for p, ps in plates)
                rows_line.append((cid, tx["t"], round(gap, 1), kind, col, sw, tx["lay"],
                                  "後" if seq > tx["seq"] else "先", tx["outl"], hidden))
        # ── (B) 札 × 札 ────────────────────────────────
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                a, b = texts[i], texts[j]
                g = rect_gap(a["r"], b["r"])
                if g < NEAR_TEXT:
                    rows_text.append((cid, a["t"], b["t"], g, a["lay"], b["lay"]))

    rows_line = sorted(set(rows_line), key=lambda x: (x[2], S.ORDER.index(x[0])))
    rows_text = sorted(set(rows_text), key=lambda x: (x[3], S.ORDER.index(x[0])))

    live = [r for r in rows_line if not r[9]]
    print(f"■ (A) 札と線のすき間 {NEAR_LINE}px 未満 … {len(live)} 件 ／ "
          f"{len({r[0] for r in live})} カット　（抜き板で隠れる分 {len(rows_line) - len(live)} 件は除外）")
    for cid, t, gap, kind, col, sw, lay, order, outl, hid in live:
        tag = []
        if outl:
            tag.append("字にフチ")
        tag.append(f"線は札より{order}")
        print(f"  {cid} 「{t[:26]}」 すき間 {gap:7.1f}px  {kind} {col} 幅{sw:.1f} "
              f"[{lay}] " + "・".join(tag))

    print(f"\n■ (B) 札と札のすき間 {NEAR_TEXT}px 未満 … {len(rows_text)} 件 ／ "
          f"{len({r[0] for r in rows_text})} カット　（負＝重なっている）")
    for cid, a, b, g, la, lb in rows_text:
        print(f"  {cid} 「{a[:20]}」×「{b[:20]}」 すき間 {g:7.1f}px  [{la}]×[{lb}]")

    print(f"\n（当てた範囲＝全 {len(S.ORDER)} カット。うち図を持つのは {n_cut_with_fig}）")


def selftest():
    """陽性対照。**件数でなく値で見る**（記憶 feedback-verify-your-own-instrument）。

    ① 解析で答えが分かる形を作り、測った値が一致するか
    ② 線を既知の量だけ動かしたら、すき間が同じ量だけ動くか（＝物差しが効いているか）
    ③ 器（台座）の除外が、本物まで消していないか
    """
    ok = True
    size, base_y, x0 = 30.0, 500.0, 400.0
    body = "あいうえお"
    up, dn = fm.ink(body, size, "Noto")
    w = fm.width(body, size, "Noto")
    r = (x0, base_y - up, x0 + w, base_y + dn)
    txt = (f'<text x="{x0}" y="{base_y}" font-family="Noto" font-size="{size}" '
           f'fill="#e8b33c" text-anchor="start">{body}</text>')
    print(f"① 字の外接矩形 … 幅 {w:.1f}px・上 {r[1]:.1f}・下 {r[3]:.1f}（fm.ink 実測）")
    for off, want in ((60.0, None), (20.0, None), (0.0, None)):
        ly = r[3] + off                                   # 字の下端から off px 下に太さ8の横線
        svg = txt + f'<path d="M{x0} {ly} H{x0 + w}" stroke="#e8b33c" stroke-width="8" fill="none"/>'
        marks = marks_of(svg, 2)
        got = min(seg_rect_dist(p[0][0], p[0][1], p[1][0], p[1][1], r) for _, p, _, _, _ in marks)
        got -= 8 / 2
        want = off - 4.0
        flag = "✓" if abs(got - want) < 0.05 else "🔴"
        print(f"   {flag} 線を下へ {off:4.0f}px … すき間 実測 {got:6.2f} ／ 式 {want:6.2f}")
        ok &= abs(got - want) < 0.05
    # ③ 器の除外が本物を消していないか（札を囲む枠は除く／横切る線は残る）
    box = f'<rect x="{x0 - 20}" y="{r[1] - 20}" width="{w + 40}" height="{r[3] - r[1] + 40}" fill="none" stroke="#8fb6c9" stroke-width="4"/>'
    cross = f'<path d="M{x0 + w / 2} {r[1] - 40} V{r[3] + 40}" stroke="#e0503c" stroke-width="6" fill="none"/>'
    n_box = n_cross = 0
    for kind, pts, sw, col, seq in marks_of(box + cross, 2):
        xs, ys = [q[0] for q in pts], [q[1] for q in pts]
        contains = (min(xs) <= r[0] and min(ys) <= r[1] and max(xs) >= r[2] and max(ys) >= r[3])
        d = min(seg_rect_dist(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], r)
                for i in range(len(pts) - 1)) - sw / 2
        if contains:
            n_box += 1
        elif d < NEAR_LINE:
            n_cross += 1
            print(f"   ✓ 横切る線は残る … すき間 {d:.2f}px（式 {-6 / 2:.2f}）")
            ok &= abs(d + 3.0) < 0.05
    print(f"   {'✓' if n_box == 1 else '🔴'} 札を囲む枠は除かれる … 除いた {n_box} 本・残した {n_cross} 本")
    ok &= (n_box == 1 and n_cross == 1)
    # ④ 抜き板の判定。🔴 最初の版はここを試していなかったので、
    #    並び順を別々の通し番号で持っていた取り違えに気づけなかった（54件が誤って鳴った）。
    plate = (f'<rect x="{x0 - 20}" y="{r[1] - 12}" width="{w + 40}" height="{r[3] - r[1] + 24}" '
             f'fill="#0f1922"/>')
    line = f'<path d="M{x0 - 100} {(r[1] + r[3]) / 2} H{x0 + w + 100}" stroke="#8fb6c9" stroke-width="4" fill="none"/>'
    for label, svg, want in (("線→板→字（板が線を隠す）", line + plate + txt, True),
                             ("板→字→線（線が字の上を通る）", plate + txt + line, False)):
        marks = marks_of(svg, 2)
        plates = plates_of(svg, 2)
        tpos = [m.start() for m in CL.TEXT.finditer(svg) if CL.unesc(m.group(2)).strip()][0]
        tseq = (2, tpos)
        hid = None
        for kind, pts, sw, col, seq in marks:
            xs, ys = [q[0] for q in pts], [q[1] for q in pts]
            if min(xs) <= r[0] and min(ys) <= r[1] and max(xs) >= r[2] and max(ys) >= r[3]:
                continue
            hid = any(p[0] <= r[0] and p[1] <= r[1] and p[2] >= r[2] and p[3] >= r[3]
                      and seq < ps < tseq for p, ps in plates)
        flag = "✓" if hid is want else "🔴"
        print(f"   {flag} {label} … 隠れる判定 {hid}（あるべき {want}）")
        ok &= (hid is want)
    print("\n" + ("✓ 物差しは効いている" if ok else "🔴 物差しが合っていない。本番に当てるな"))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else (main() or 0))
