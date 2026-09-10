# -*- coding: utf-8 -*-
"""⑤c'【直す】3巡目・§V-8-1（`people` の節見出しの級数割れ 11/11）の真因を測る道具。

■ なぜ要るか
  引き継ぎは「真因は `titan_fig` が**字数で級数を決めている**こと」と書いていた。
  それは半分しか当たっていない可能性がある。`people()` は
    ① 節どうしがぶつからない最大の箱の幅 `bw` を二分探索で決め
    ② `tw_max = bw - 52 - 絵の幅` に**各節の題を別々に詰める**（`fm.fit`）
  ので、**`bw` が小さいカットほど字数の差が級数の差に化ける**。
  そして `bw` を小さくしている犯人は、**節の x が枠の端（0.06）にあること**かもしれない。
  （`c711` と `ca07` は 2026-09-09 に 0.06 → 0.13 へ内側に寄せてある。他は寄せていない。）

■ 測り方（⚠️ 式は書き写さない。`titan_fig.people()` を**本当に回して** SVG を読む）
  ・節の箱＝`<rect ... rx="8">` の width／height を拾う
  ・題の級数＝`<text>` の font-size を拾う
  ・**同じカットを2通りで回す**：現状の x ／ x を [INSET, 1-INSET] に線形で押し込んだもの
    → 「x を内側へ寄せるだけで級数の割れが減るか」が数字で出る

■ 陽性対照（⚠️ 件数では鳴らない指標なので**値**で見る）
  `--pos` … いちばん外側の節をさらに端（x=0.0 と 1.0）へ出す。
  箱の幅が縮み、題の級数が**下がれば**測れている。

    python -u qa_out/kb_w_people.py
    python -u qa_out/kb_w_people.py --pos
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import titan_fig as T                                      # noqa: E402
from cuts import SPEC                                      # noqa: E402

RECT = re.compile(r'<rect\b([^>]*)rx="8"([^>]*)/>')
W_ = re.compile(r'width="([0-9.]+)"')
H_ = re.compile(r'height="([0-9.]+)"')
TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')
SIZE = re.compile(r'font-size="([0-9.]+)"')

INSET = 0.13                      # 端の節をここまで内側へ寄せる


def render(nodes, kw):
    fig = T.people(**dict(kw, nodes=nodes))
    return "".join(fig.stages)


def boxw(svg):
    """節の箱（角丸 rx=8 の枠線）の幅・高さ。**描かれた値を読む**。"""
    ws, hs = [], []
    for m in RECT.finditer(svg):
        a = m.group(1) + m.group(2)
        w, h = W_.search(a), H_.search(a)
        if w and h:
            ws.append(float(w.group(1)))
            hs.append(float(h.group(1)))
    return (max(ws) if ws else 0.0), (max(hs) if hs else 0.0)


def sizes(svg, nodes):
    out = {}
    for m in TEXT.finditer(svg):
        s = SIZE.search(m.group(1))
        if s:
            out[m.group(2)] = float(s.group(1))
    return [(out.get(str(n["t"]).strip()), str(n["t"]).strip()) for n in nodes]


def inset(nodes, lo=INSET):
    """x を [lo, 1-lo] に線形で押し込む（**並びの前後は変えない**）。"""
    xs = [n["x"] for n in nodes]
    a, b = min(xs), max(xs)
    out = []
    for n in nodes:
        d = dict(n)
        d["x"] = lo if b - a < 1e-6 else lo + (1 - 2 * lo) * (n["x"] - a) / (b - a)
        out.append(d)
    return out


def main(pos=False):
    print(f"■ 読んだファイル: {Path(T.__file__).resolve()}")
    print(f"■ cuts: {Path(sys.modules['cuts'].__file__).resolve()}／SPEC {len(SPEC)} カット")
    print(f"■ モード: {'陽性対照（端へ出す）' if pos else '実測'}／内寄せ INSET={INSET}")
    print(f"{'カット':7} {'節':>3} {'いまの箱':>8} {'開き':>5} {'最小':>5} "
          f"{'内寄せの箱':>10} {'開き':>5} {'最小':>5}  x のいまの範囲")
    tot_now = tot_new = 0
    for cid, sp in SPEC.items():
        f = sp.get("fig")
        if not f or f[0] != "people":
            continue
        kw = dict(f[1])
        nodes = [dict(n) for n in kw.pop("nodes")]
        if len(nodes) < 2:
            continue
        cur = inset(nodes, 0.0) if pos else nodes
        a_svg = render(cur, kw)
        b_svg = render(inset(nodes), kw)
        aw, _ah = boxw(a_svg)
        bw_, _bh = boxw(b_svg)
        asz = [s for s, _ in sizes(a_svg, cur) if s]
        bsz = [s for s, _ in sizes(b_svg, inset(nodes)) if s]
        if not asz or not bsz:
            print(f"  🔴 {cid} 級数が読めなかった（fail closed）")
            continue
        ga, gb = max(asz) - min(asz), max(bsz) - min(bsz)
        tot_now += ga >= 8
        tot_new += gb >= 8
        xs = [n["x"] for n in nodes]
        print(f"  {cid:6} {len(nodes):>3} {aw:>8.0f} {ga:>5.0f} {min(asz):>5.0f} "
              f"{bw_:>10.0f} {gb:>5.0f} {min(bsz):>5.0f}  {min(xs):.2f}〜{max(xs):.2f}")
    print(f"\n  開きが 8px 以上のカット：いま {tot_now} → x を内側へ寄せると {tot_new}")
    if pos:
        print("  ⚠️ 陽性対照は**件数**でなく、上の「いまの箱」の幅と最小級数が"
              "実測より下がっていることで見る。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main("--pos" in sys.argv[1:]))
