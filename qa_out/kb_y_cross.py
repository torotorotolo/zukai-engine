# -*- coding: utf-8 -*-
"""**線が札を貫いていないか**を、重ね順を見ずに全数で測る。

■ なぜ要るか（台帳 §X-1-4・§W-7-2）
  `check_layout` の「図形が文字を横切っている」は
  **文字があとの層に描かれると「読めるから良い」として飛ばす**（`order(mk) <= order(t)`）。
  ところが `mapfig` の `link` のように**札のすぐ横から伸びる線**は、
  文字の下を通っていても**取り消し線に見える**。門番は 0件のまま、目視が2回とも拾えなかった。

  実測（直す前の `c105`）：破線 M417.3 421.6 → L790.4 433.1／
  札「シーガート」の字面 x 451〜621・y 409〜424 ＝ **札の下側を線が通る**。

■ 測り方
  `scene_jiko.build_layers()` の SVG から
    ・`<text>` … `fontmetrics.ink()` で字面の箱（縁取りぶんは引く＝辛くしない）
    ・`<path d="M… L…">` `<line>` … 折れ線の頂点をつないだ線分
  を集め、**層をまたいで**「線分が字面の箱を通り抜けるか」を見る。

  ⚠️ 地紋（方眼）と全画面の帯は数えない。**枠の幅・高さの 8割を超える線**は地紋。
  ⚠️ 見出しの下の赤い罫のように、**字面の外を通る線**は交わらないので出ない。

■ 陽性対照 `--pos`
  すべてのカットの1つ目の札の**真ん中に**線を1本足す。
  **件数がカット数ぶん増えなければ測れていない。**

    python -u qa_out/kb_y_cross.py
    python -u qa_out/kb_y_cross.py --pos

  exit 0 ＝ 0件／1 ＝ 貫いている／3 ＝ 対照が通らない。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import fontmetrics as fm                                     # noqa: E402
import scene_jiko as S                                       # noqa: E402

TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')
PATH = re.compile(r'<path([^>]*\sd="[^"]+"[^>]*)>')
DPAT = re.compile(r'\sd="([^"]+)"')
# 地紋（方眼）の色。⚠️ 長さで切ると `mapfig` の縦の地紋（830px）が残るので、色で除く。
GRID_COLS = {"#22333f"}
LINE = re.compile(r'<line([^>]*)>')
NUM = re.compile(r"-?\d+(?:\.\d+)?")
W, H = 1920, 1080


def att(a, k, d=""):
    m = re.search(k + r'="([^"]*)"', a)
    return m.group(1) if m else d


def text_boxes(svg):
    out = []
    for m in TEXT.finditer(svg):
        a, t = m.group(1), m.group(2)
        if not t.strip():
            continue
        size = float(att(a, "font-size", "0") or 0)
        if not size:
            continue
        fam = att(a, "font-family", "Noto")
        w = sum(fm.adv(c, fam) for c in t) * size
        x, y = float(att(a, "x", "0")), float(att(a, "y", "0"))
        anc = att(a, "text-anchor", "start")
        x0 = x - w if anc == "end" else (x - w / 2 if anc == "middle" else x)
        top, bot = fm.ink(t, size, fam)
        out.append((t, x0, y - top, x0 + w, y + bot))
    return out


def polylines(svg):
    """(頂点の並び) を返す。⚠️ 曲線（C/Q/A）は端点だけ見る（近似）。"""
    out = []
    for m in PATH.finditer(svg):
        a = m.group(1)
        if att(a, "stroke").lower() in GRID_COLS:
            continue                                  # 地紋は線として数えない
        d = DPAT.search(a).group(1)
        pts, cur = [], None
        for seg in re.finditer(r"([MLHVmlhv])([^A-Za-z]*)", d):
            cmd, rest = seg.group(1), NUM.findall(seg.group(2))
            v = [float(x) for x in rest]
            if cmd in "Mm" and len(v) >= 2:
                cur = (v[0], v[1]) if cmd == "M" else (
                    (cur[0] + v[0], cur[1] + v[1]) if cur else (v[0], v[1]))
                pts.append(cur)
                for i in range(2, len(v) - 1, 2):
                    cur = (v[i], v[i + 1]) if cmd == "M" else (cur[0] + v[i], cur[1] + v[i + 1])
                    pts.append(cur)
            elif cmd in "Ll" and cur:
                for i in range(0, len(v) - 1, 2):
                    cur = (v[i], v[i + 1]) if cmd == "L" else (cur[0] + v[i], cur[1] + v[i + 1])
                    pts.append(cur)
            elif cmd in "Hh" and cur and v:
                cur = (v[0], cur[1]) if cmd == "H" else (cur[0] + v[0], cur[1])
                pts.append(cur)
            elif cmd in "Vv" and cur and v:
                cur = (cur[0], v[0]) if cmd == "V" else (cur[0], cur[1] + v[0])
                pts.append(cur)
        if len(pts) >= 2:
            out.append(pts)
    for m in LINE.finditer(svg):
        a = m.group(1)
        if att(a, "stroke").lower() in GRID_COLS:
            continue
        out.append([(float(att(a, "x1", "0")), float(att(a, "y1", "0"))),
                    (float(att(a, "x2", "0")), float(att(a, "y2", "0")))])
    return out


def ground(pts):
    """地紋・全画面の帯か（画面の8割を超えて伸びる線）。"""
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (max(xs) - min(xs)) > W * 0.8 or (max(ys) - min(ys)) > H * 0.8


def hits_box(pts, box):
    """折れ線が字面の箱の中を通るか（1点でも内側に入る／箱を横断する）。"""
    # 🔴 端を2pxだけ削る作りにしたら、`c404` の枠の罫（字面の下端から 5px）まで
    #    「貫いている」と出た。**かすめる線と貫く線を分ける**のがこの物差しの用途なので、
    #    字面の**真ん中6割**に入ったものだけを数える（`check_layout` の「字の芯」と同じ考え）。
    x0, y0, x1, y1 = box
    mx, my = (x1 - x0) * 0.2, (y1 - y0) * 0.2
    x0, y0, x1, y1 = x0 + mx, y0 + my, x1 - mx, y1 - my
    if x1 <= x0 or y1 <= y0:
        return False
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        # 線分と矩形の交差（媒介変数の区間で判定）
        t0, t1 = 0.0, 1.0
        dx, dy = bx - ax, by - ay
        for p, q in ((-dx, ax - x0), (dx, x1 - ax), (-dy, ay - y0), (dy, y1 - ay)):
            if p == 0:
                if q < 0:
                    break
            else:
                r = q / p
                if p < 0:
                    if r > t1:
                        break
                    t0 = max(t0, r)
                else:
                    if r < t0:
                        break
                    t1 = min(t1, r)
        else:
            if t0 <= t1:
                return True
    return False


def main(pos=False):
    print(f"■ 画は本番と同じ経路: {Path(S.__file__).resolve()} の build_layers()")
    print(f"■ 字面: {Path(fm.__file__).resolve()}／モード: "
          f"{'陽性対照（札の真ん中に線を1本足す）' if pos else '実測'}")
    jobs, _ = S.build_layers(allow_missing=True)
    bycut = {}
    for k, svg in jobs.items():
        cid = k.rsplit("_", 1)[0]
        t, p = bycut.setdefault(cid, ([], []))
        t.extend(text_boxes(svg))
        p.extend([q for q in polylines(svg) if not ground(q)])
    hits = []
    for cid, (texts, lines) in sorted(bycut.items()):
        if pos and texts:
            t0 = texts[0]
            cy = (t0[2] + t0[4]) / 2
            lines = lines + [[(t0[1] - 20, cy), (t0[3] + 20, cy)]]
        for t in texts:
            for pts in lines:
                if hits_box(pts, (t[1], t[2], t[3], t[4])):
                    hits.append((cid, t[0], t[1], t[2], t[3], t[4]))
                    break
    print(f"\n■ 測ったカット {len(bycut)}／札 {sum(len(v[0]) for v in bycut.values())}"
          f"／線 {sum(len(v[1]) for v in bycut.values())}")
    print(f"\n{'カット':6} 貫かれている札（字面の箱）")
    for cid, t, x0, y0, x1, y1 in hits:
        print(f"  🔴 {cid:6} 「{t[:24]}」 x {x0:.0f}〜{x1:.0f}／y {y0:.0f}〜{y1:.0f}")
    print(f"\n{'🔴' if hits else '✓'} 線が貫いている札 ＝ {len(hits)} 件")
    if pos:
        ok = len(hits) >= len(bycut) * 0.9
        print(f"  {'✓' if ok else '🔴'} 陽性対照：カット数（{len(bycut)}）に近い件数が出るはず"
              f"（出た: {len(hits)}）")
        return 0 if ok else 3
    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main("--pos" in sys.argv[1:]))
