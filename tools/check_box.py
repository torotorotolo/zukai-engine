# -*- coding: utf-8 -*-
"""**枠の内側**が空いていないかを机上で測る。

🔴 なぜ要るか（2026-08-01 カズヤくん試写指摘「枠内の余白が多い」5枚）
   `check_space.py` は **画面全体に対する占有率**を測る道具で、
   **箱の内側は見ていない**。`beforeafter` の箱は下 2/3 が空洞なのに、
   枠線と地の塗りぶんが「使っている」に数えられて**数字の上では通ってしまう**。
   1例を直しても他の11枚を見落とす。だから**箱そのものを測る物差し**を別に作る。

■ 何を測るか
   1 全レイヤーの SVG から、**枠（`fill="none"` で `stroke` のある大きな rect）**を拾う
   2 同じカットの全レイヤーから、**その枠の内側に入る中身**を拾う
       文字 … fontmetrics の実測外接矩形（check_layout と同じ）
       線・曲線 … path を歩いて**線上の点**を拾う（外接矩形では塗り潰しになるので使わない）
       円・塗り矩形・写真 … その形のまま
   3 枠の内側を 24px のセルに畳み、**中身が触れたセル**を数える
       内側占有率   = 触れたセル / 内側の全セル
       最大の空き   = 内側で連続して空いているいちばん大きい長方形（内側面積比）
       下の空き帯   = 中身の下端から枠の下端まで（**いちばん多い症状がこれ**）

■ 判定
   内側占有率 28% 以上 ／ 最大の空き矩形が内側の 30% 未満 ／ 下の空き帯が高さの 22% 未満
   ⚠️ しきい値は**実測から決めた**（下の CAL を参照）。推定で置いていない。

■ 使い方
     python tools/check_box.py                 … 全カット
     python tools/check_box.py --only=c5       … 章だけ
     python tools/check_box.py --cut=c505      … 1カットを詳しく（枠ごとに内訳）
     python tools/check_box.py --kind=process  … 型で絞る

⚠️ これは机上の物差しであって**目視の代わりではない**。
   ここを通しても必ずクラウドで焼いて拡大目視する。
"""
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import fontmetrics as fm
import jiko_style as J
import scene_jiko as S

CELL = 24                # 内側を畳むセル（px）
MIN_W, MIN_H = 200, 150  # これより小さい rect は「枠」とみなさない（チップ・印は対象外）
INSET = 10               # 枠線の内側から何 px 入ったところを「内側」とするか
STEP = 5.0               # path を歩くときの刻み（px）

HOLE_MAX = 0.30          # 最大の空き矩形（内側面積比）の上限 ★主たる判定
FILL_MIN = 0.08          # 内側占有率の下限（中身が散っていて空き矩形では出ない箱を拾う）

# ── しきい値をどう決めたか（★推定で置かないこと） ─────────────
# `--hist` で 111枠の実測分布を出し、**カズヤくんが名指しした型が全部落ち、
# 名指しされていない型が巻き込まれない**ところに置いた（2026-08-01）。
#
#   型            枠数  内側占有  空き矩形  ← 空き矩形がいちばんよく分かれる
#   beforeafter    24     7%      71%   🔴 指摘された型
#   process        48    11%      65%   🔴 指摘された型
#   breakdown       8     7%      43%   🔴（指摘は無いが同じ症状）
#   quote          16    28%      27%   （作り直す型）
#   graph          14    22%      14%   ✓ 通る
#   mapfig          3    45%       1%   ✓ 通る
#
# ⚠️ 「文字の下の空洞」は**判定に使わない**。`graph` は目盛りの文字が上にあって
#    下は折れ線なので 87% と出るが、これは空洞ではない。診断として表示だけする。
# ⚠️ `compare` の棒と `absent` の箱は `is_container` で先に外している（下記）。
CAL = ("111枠の実測分布から、beforeafter(71%)・process(65%) が落ちて "
       "graph(14%)・mapfig(1%) が通る 30% に置いた（--hist で取り直せる）")

TAG = re.compile(r"<(text|path|rect|circle|image|g|/g)\b([^>]*?)(/?)>", re.S)
TEXTC = re.compile(r'<text\s([^>]*)>([^<]*)</text>')
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
NUM = re.compile(r"[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?")
CMD = re.compile(r"([MmLlHhVvCcSsQqTtAaZz])([^MmLlHhVvCcSsQqTtAaZz]*)")
TRANS = re.compile(r"translate\(\s*([-\d.]+)[ ,]+([-\d.]+)\s*\)")
UNESC = {"&amp;": "&", "&lt;": "<", "&gt;": ">"}


def unesc(t):
    for k, v in UNESC.items():
        t = t.replace(k, v)
    return t


def _f(a, k, d=0.0):
    try:
        return float(a.get(k, d))
    except (TypeError, ValueError):
        return d


# ══════════════════════════════════════════════════════════
# path を歩く。**外接矩形は使わない**（線1本で箱が埋まったことになるため）
# ══════════════════════════════════════════════════════════
def path_points(d):
    """path データ上の点を STEP px おきに拾う。曲線は制御点を通る折れ線で近似する。"""
    pts, cur, start, prev_c = [], (0.0, 0.0), (0.0, 0.0), None
    for cmd, body in CMD.findall(d):
        v = [float(x) for x in NUM.findall(body)]
        rel = cmd.islower()
        c = cmd.upper()
        i = 0
        if c == "Z":
            pts += walk(cur, start)
            cur = start
            continue
        while True:
            if c == "M":
                if i + 2 > len(v):
                    break
                p = (v[i] + (cur[0] if rel else 0), v[i + 1] + (cur[1] if rel else 0))
                if i == 0:
                    start = p
                    pts.append(p)
                else:
                    pts += walk(cur, p)
                cur, i = p, i + 2
                c = "L"                       # M のあとの連番は L 扱い（SVG の規則）
            elif c == "L":
                if i + 2 > len(v):
                    break
                p = (v[i] + (cur[0] if rel else 0), v[i + 1] + (cur[1] if rel else 0))
                pts += walk(cur, p)
                cur, i = p, i + 2
            elif c == "H":
                if i + 1 > len(v):
                    break
                p = (v[i] + (cur[0] if rel else 0), cur[1])
                pts += walk(cur, p)
                cur, i = p, i + 1
            elif c == "V":
                if i + 1 > len(v):
                    break
                p = (cur[0], v[i] + (cur[1] if rel else 0))
                pts += walk(cur, p)
                cur, i = p, i + 1
            elif c in ("C", "S", "Q", "T"):
                need = {"C": 6, "S": 4, "Q": 4, "T": 2}[c]
                if i + need > len(v):
                    break
                ox, oy = (cur if rel else (0.0, 0.0))
                raw = [(v[i + k] + ox, v[i + k + 1] + oy) for k in range(0, need, 2)]
                if c == "S":
                    raw = [reflect(cur, prev_c)] + raw
                elif c == "T":
                    raw = [reflect(cur, prev_c)] + raw
                elif c == "Q":
                    raw = raw
                pts += bez(cur, raw)
                prev_c = raw[-2] if len(raw) >= 2 else None
                cur, i = raw[-1], i + need
                continue
            elif c == "A":
                if i + 7 > len(v):
                    break
                p = (v[i + 5] + (cur[0] if rel else 0), v[i + 6] + (cur[1] if rel else 0))
                # 弧は端どうしを結ぶ折れ線で近似する（内側の空きを測るには十分）
                pts += walk(cur, p)
                cur, i = p, i + 7
            else:
                break
            if c not in ("C", "S", "Q", "T"):
                prev_c = None
            if i >= len(v):
                break
    return pts


def reflect(cur, prev_c):
    if prev_c is None:
        return cur
    return (2 * cur[0] - prev_c[0], 2 * cur[1] - prev_c[1])


def walk(a, b):
    n = max(1, int(math.dist(a, b) / STEP))
    return [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n)
            for k in range(n + 1)]


def bez(p0, rest):
    """制御点つきの曲線を de Casteljau で刻む。"""
    ps = [p0] + list(rest)
    n = max(2, int(sum(math.dist(ps[k], ps[k + 1]) for k in range(len(ps) - 1)) / STEP))
    out = []
    for k in range(n + 1):
        t = k / n
        q = list(ps)
        while len(q) > 1:
            q = [(q[j][0] + (q[j + 1][0] - q[j][0]) * t,
                  q[j][1] + (q[j + 1][1] - q[j][1]) * t) for j in range(len(q) - 1)]
        out.append(q[0])
    return out


# ══════════════════════════════════════════════════════════
# SVG から「枠」と「中身」を拾う
# ══════════════════════════════════════════════════════════
def parse(svg, layer):
    """(枠の一覧, 中身の一覧) を返す。

    枠   … (x, y, w, h)
    中身 … ("box", x0,y0,x1,y1) か ("pts", [(x,y), …])
    """
    frames_, marks, texts = [], [], []
    stack = [(0.0, 0.0)]
    for m in TAG.finditer(svg):
        tag, raw, selfclose = m.group(1), m.group(2), m.group(3)
        if tag == "/g":
            if len(stack) > 1:
                stack.pop()
            continue
        a = dict(ATTR.findall(raw))
        dx, dy = stack[-1]
        if tag == "g":
            t = TRANS.search(a.get("transform", ""))
            stack.append((dx + float(t.group(1)), dy + float(t.group(2))) if t else (dx, dy))
            continue
        if tag == "rect":
            x, y = _f(a, "x") + dx, _f(a, "y") + dy
            w, h = _f(a, "width"), _f(a, "height")
            fill, stroke = a.get("fill", "none"), a.get("stroke", "none")
            if fill == "none" and stroke not in ("none", "") and w >= MIN_W and h >= MIN_H:
                frames_.append((x, y, w, h))
            else:
                marks.append(("box", x, y, x + w, y + h))
            continue
        if tag == "image":
            x, y = _f(a, "x") + dx, _f(a, "y") + dy
            marks.append(("box", x, y, x + _f(a, "width"), y + _f(a, "height")))
            continue
        if tag == "circle":
            cx, cy, r = _f(a, "cx") + dx, _f(a, "cy") + dy, _f(a, "r")
            if a.get("fill", "none") not in ("none", ""):
                marks.append(("box", cx - r, cy - r, cx + r, cy + r))
            else:                              # 輪だけ。中は空いている
                marks.append(("pts", [(cx + r * math.cos(t), cy + r * math.sin(t))
                                      for t in [k * STEP / max(r, 1) for k in
                                                range(int(2 * math.pi * max(r, 1) / STEP) + 1)]]))
            continue
        if tag == "path":
            p = path_points(a.get("d", ""))
            if p:
                marks.append(("pts", [(x + dx, y + dy) for x, y in p]))
            continue
    # 文字は fontmetrics で実測する（check_layout と同じ測り方）
    for m in TEXTC.finditer(svg):
        a = dict(ATTR.findall(m.group(1)))
        t = unesc(m.group(2))
        if not t.strip():
            continue
        x, y = _f(a, "x"), _f(a, "y")
        size, fam = _f(a, "font-size", 32), a.get("font-family", "Noto")
        w = fm.width(t, size, fam)
        up, dn = fm.ink(t, size, fam)
        anc = a.get("text-anchor", "start")
        x0 = x - w / 2 if anc == "middle" else (x - w if anc == "end" else x)
        marks.append(("box", x0, y - up, x0 + w, y + dn))
        texts.append((x0, y - up, x0 + w, y + dn, t))
    return frames_, marks, texts


def scaffold(mark):
    """地の足場（方眼・全画面の帯）なら True。中身に数えない。

    `_base` を外したあとも、`grid_only`（写真を敷くカット）や全画面の暗幕が
    別レイヤーに入ることがある。**画面の9割を跨ぐものは中身ではない**。
    """
    kind, *v = mark
    xs = [p[0] for p in v[0]] if kind == "pts" else [v[0], v[2]]
    ys = [p[1] for p in v[0]] if kind == "pts" else [v[1], v[3]]
    if not xs:
        return True
    return (max(xs) - min(xs) > 1728) or (max(ys) - min(ys) > 972)


def dedupe(frames_):
    """同じ枠が塗りと線で2回描かれるので、近いものは1つにまとめる。"""
    out = []
    for f in frames_:
        if not any(all(abs(f[i] - g[i]) < 6 for i in range(4)) for g in out):
            out.append(f)
    return out


# ══════════════════════════════════════════════════════════
# 内側を畳んで測る
# ══════════════════════════════════════════════════════════
def is_container(frame_, texts):
    """その rect が「中身を入れる枠」か、「棒・面などの図形そのもの」かを分ける。

    🔴 最初これを分けずに測って、`compare` の**棒**を枠として数えた（26個すべて
       「内側占有 0%・空き 100%」と出た）。棒は中が空なのが正しい形なので、
       枠として測ると意味の無い赤が26個出る。
    → **文字を1つ以上抱えているものだけを枠とみなす。**
       `compare` の数値は棒の**上**（top+118）に置かれていて棒の中には無いので、
       この規則で棒は自動的に外れる。`process` `beforeafter` の箱は文字を抱えるので残る。

    ⚠️ `absent` の箱は**わざと空**で、説明は箱の**下**（top+bh+52）に置いてある。
       この規則だと枠から外れるが、それが正しい（「無いことを見せる」型なので、
       中が空いていることは症状ではない）。
    """
    x, y, w, h = frame_
    return any(x <= (t[0] + t[2]) / 2 <= x + w and y <= (t[1] + t[3]) / 2 <= y + h
               for t in texts)


def text_extent(frame_, texts):
    """枠の中にある**文字だけ**の上端・下端を返す（無ければ None）。

    ⚠️ 占有率は `hatch()` の斜線や地の塗りでも埋まるので、
       「中身は上端の文字だけで下が空洞」という症状を**占有率では捕まえられない**
       （`absent` は斜線で 100% と出る）。文字だけを別に測る。
    """
    x, y, w, h = frame_
    inside = [t for t in texts
              if x <= (t[0] + t[2]) / 2 <= x + w and y <= (t[1] + t[3]) / 2 <= y + h]
    if not inside:
        return None
    return min(t[1] for t in inside), max(t[3] for t in inside)


def occupancy(frame_, marks):
    x, y, w, h = frame_
    ix0, iy0 = x + INSET, y + INSET
    ix1, iy1 = x + w - INSET, y + h - INSET
    cx, cy = max(1, int((ix1 - ix0) / CELL)), max(1, int((iy1 - iy0) / CELL))
    grid = [[False] * cx for _ in range(cy)]

    def hit(px, py):
        if not (ix0 <= px < ix1 and iy0 <= py < iy1):
            return
        i, j = int((px - ix0) / CELL), int((py - iy0) / CELL)
        if 0 <= i < cx and 0 <= j < cy:
            grid[j][i] = True

    for kind, *v in marks:
        if kind == "pts":
            for px, py in v[0]:
                hit(px, py)
        else:
            bx0, by0, bx1, by1 = v
            # 枠そのもの（内側いっぱいを覆う塗り）は中身に数えない
            if bx0 <= x + 2 and by0 <= y + 2 and bx1 >= x + w - 2 and by1 >= y + h - 2:
                continue
            px = bx0
            while px <= bx1:
                py = by0
                while py <= by1:
                    hit(px, py)
                    py += CELL / 2
                px += CELL / 2
    return grid, cx, cy, (ix0, iy0, ix1, iy1)


# 空きが「穴」と言えるための最低の形（枠の幅・高さに対する比）。
# 🔴 2026-08-01：形を見ずに面積だけで測っていたら、**引用の札（470px幅）で
#    行末のギザギザ（ragged right）を穴として数えた**（16枠中8枠が33〜53%）。
#    左揃えの短い行が並べば右端は必ず空くので、あれは余白ではなく普通の組版。
#    → **細長い帯は穴と呼ばない。** 縦にも横にも枠の35%以上ある塊だけを穴とする。
HOLE_MIN_W, HOLE_MIN_H = 0.35, 0.35


def biggest_hole(grid, cx, cy):
    """空きセルだけで作れるいちばん大きい長方形（check_space と同じヒストグラム法）。

    ただし **HOLE_MIN_W × HOLE_MIN_H より細い帯は数えない**（上の注記）。
    """
    mw, mh = max(1, int(cx * HOLE_MIN_W)), max(1, int(cy * HOLE_MIN_H))
    best, up = (0, 0, 0, 0, 0), [0] * cx
    for j in range(cy):
        for i in range(cx):
            up[i] = 0 if grid[j][i] else up[i] + 1
        st = []
        for i in range(cx + 1):
            hh = up[i] if i < cx else 0
            start = i
            while st and st[-1][1] >= hh:
                s, ph = st.pop()
                if ph >= mh and (i - s) >= mw and ph * (i - s) > best[0]:
                    best = (ph * (i - s), s, j - ph + 1, i - s, ph)
                start = s
            st.append((start, hh))
    return best


def foot(grid, cx, cy):
    """下から数えて、まるごと空いている行が何行あるか（＝箱の底の空き帯）。"""
    n = 0
    for j in range(cy - 1, -1, -1):
        if any(grid[j]):
            break
        n += 1
    return n


def head(grid, cx, cy):
    n = 0
    for j in range(cy):
        if any(grid[j]):
            break
        n += 1
    return n


# ══════════════════════════════════════════════════════════
def measure(only=None, cut=None, kind=None, hist=False, verbose=False):
    jobs, _ = S.build_layers(allow_missing=True)
    bycut = defaultdict(list)
    for k, svg in jobs.items():
        bycut[k.rsplit("_", 1)[0]].append((k, svg))

    kinds = {c: (v["fig"][0] if v.get("fig") else ("写真" if v.get("photo") else "?"))
             for c, v in S.SPEC.items()}

    cids = sorted(bycut, key=lambda c: list(S.ORDER).index(c) if c in S.ORDER else 9999)
    if cut:
        cids = [c for c in cids if c in cut.split(",")]
    elif only:
        cids = [c for c in cids if c.startswith(only)]
    if kind:
        cids = [c for c in cids if kinds.get(c) == kind]

    rows, bad = [], []
    for cid in cids:
        frames_, marks, texts = [], [], []
        for k, svg in bycut[cid]:
            # 🔴 `_base` は地（`J.frame` の方眼 1920×1080）＋見出し＋章マーカー。
            #    方眼は 60px ごとに全画面を走るので、**中身に数えると全部の箱が
            #    「詰まっている」と出る**（実測：どの型も内側占有 62〜73%・空き矩形 1%）。
            #    最初これで丸ごと騙された。地は中身ではない。
            if k.endswith("_base"):
                continue
            f, m, t = parse(svg, k)
            frames_ += f
            marks += [x for x in m if not scaffold(x)]
            texts += t
        frames_ = dedupe(frames_)
        if not frames_:
            continue
        for bi, fr in enumerate(frames_):
            if not is_container(fr, texts):
                continue                       # 棒・面などの図形そのもの。枠ではない
            x, y, w, h = fr
            grid, cx, cy, inner = occupancy(fr, marks)
            total = cx * cy
            fill = sum(sum(r) for r in grid) / total
            area, hx, hy, hw, hh = biggest_hole(grid, cx, cy)
            hole = area / total
            ft, hd = foot(grid, cx, cy) / cy, head(grid, cx, cy) / cy
            te = text_extent(fr, texts)
            # 文字の下端から枠の下端まで。斜線や地の塗りに影響されない物差し
            tfoot = (y + h - te[1]) / h if te else 1.0
            tuse = (te[1] - te[0]) / h if te else 0.0
            why = []
            if hole > HOLE_MAX:
                why.append(f"空き矩形 {hole * 100:.0f}%")
            if fill < FILL_MIN:
                why.append(f"内側占有 {fill * 100:.0f}%")
            rows.append(dict(cid=cid, kind=kinds.get(cid, "?"), i=bi, fr=fr,
                             fill=fill, hole=hole, foot=ft, head=hd, why=why,
                             tfoot=tfoot, tuse=tuse,
                             hx=hx, hy=hy, hw=hw, hh=hh, cx=cx, cy=cy))
            if why:
                bad.append(rows[-1])

    if hist:
        show_hist(rows)
        return 0

    print(f"■ 枠の内側の余白  枠 {len(rows)}個 / {len(set(r['cid'] for r in rows))}カット")
    print(f"  基準：空き矩形 {HOLE_MAX*100:.0f}%未満／内側占有 {FILL_MIN*100:.0f}%以上"
          f"（文字下空洞は診断のみ・判定には使わない）")
    print(f"{'カット':<8}{'型':<12}{'枠':>3}{'内側占有':>9}{'空き矩形':>9}{'文字下空洞':>10}  枠(px)")
    for r in rows:
        if not verbose and not r["why"]:
            continue
        x, y, w, h = r["fr"]
        print(f"{r['cid']:<8}{r['kind']:<12}{r['i']:>3}{r['fill']*100:>8.0f}%"
              f"{r['hole']*100:>8.0f}%{r['tfoot']*100:>9.0f}%  "
              f"{x:.0f},{y:.0f} {w:.0f}×{h:.0f}"
              + ("  🔴 " + "／".join(r["why"]) if r["why"] else ""))

    per = defaultdict(lambda: [0, 0])
    for r in rows:
        per[r["kind"]][0] += 1
        if r["why"]:
            per[r["kind"]][1] += 1
    print("\n── 型ごと（枠の数 / うち基準外）──")
    for k in sorted(per, key=lambda k: -per[k][1]):
        n, b = per[k]
        print(f"  {k:<14} {n:>3}枠  基準外 {b:>3}" + ("  🔴" if b else ""))

    cuts_bad = sorted(set(r["cid"] for r in bad),
                      key=lambda c: list(S.ORDER).index(c) if c in S.ORDER else 9999)
    print(f"\n{'🔴' if bad else '✓'} 基準外の枠 {len(bad)}個 / {len(rows)}個"
          f"（カットにすると {len(cuts_bad)}）")
    if cuts_bad:
        print("  " + "、".join(cuts_bad))
    print(f"\n⚠️ しきい値の根拠：{CAL}")
    return 1 if bad else 0


def show_hist(rows):
    import statistics as st
    print("■ 分布（しきい値を決めるときはここを見る）")
    for key, name in (("fill", "内側占有率"), ("hole", "最大の空き矩形"),
                      ("tfoot", "文字の下の空洞"), ("tuse", "文字が使う縦幅")):
        v = sorted(r[key] for r in rows)
        if not v:
            continue
        q = [v[int(len(v) * p)] for p in (0.1, 0.25, 0.5, 0.75, 0.9)]
        print(f"  {name:<14} 最小{v[0]*100:5.0f}%  "
              + "  ".join(f"{p}%={x*100:.0f}%" for p, x in zip((10, 25, 50, 75, 90), q))
              + f"  最大{v[-1]*100:5.0f}%  平均{st.mean(v)*100:.0f}%")
    per = defaultdict(list)
    for r in rows:
        per[r["kind"]].append(r)
    print("\n  型ごとの中央値")
    print(f"  {'型':<14}{'枠数':>5}{'内側占有':>10}{'空き矩形':>10}{'文字下空洞':>11}")
    for k in sorted(per, key=lambda k: st.median([r["fill"] for r in per[k]])):
        rs = per[k]
        print(f"  {k:<14}{len(rs):>5}"
              f"{st.median([r['fill'] for r in rs])*100:>9.0f}%"
              f"{st.median([r['hole'] for r in rs])*100:>9.0f}%"
              f"{st.median([r['tfoot'] for r in rs])*100:>10.0f}%")


if __name__ == "__main__":
    g = lambda p: next((a.split("=", 1)[1] for a in sys.argv if a.startswith(p)), None)
    sys.exit(measure(only=g("--only="), cut=g("--cut="), kind=g("--kind="),
                     hist="--hist" in sys.argv, verbose="--all" in sys.argv))
