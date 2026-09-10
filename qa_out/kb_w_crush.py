# -*- coding: utf-8 -*-
"""**Dela Gothic One でつぶれる漢字**を、字を焼いて機械で見つける。

■ なぜ要るか（2026-09-10・⑤c' 3巡目で見つけた）
  `c913`「56個」`c303`「4,679個」の **個** が、原寸で見ると
  **字の中の空きが埋まって読めない**。豆腐（.notdef）ではない
  （`fontmetrics.missing()` は0件＝Dela の cmap に 個 は在る）。
  `titan_fig.numfam()` の注がまさにこの症状を書いているが、
  **`numfam` は「数字を含む文字列」を Dela のまま残す**ので、
  「56個」のような**数字＋漢字**は守られない。＝規則の穴。

■ 測り方（⚠️ 式を書き写さない。**本物のフォントで字を焼いて画素を数える**）
  同じ級数で Dela と Noto に1字ずつ焼き、**囲まれた空き（counter＝字の中の穴）**の
  面積が Dela でどれだけ減るかを見る。
  ・「囲まれた空き」＝ 白い画素のうち、**外周とつながっていない**もの（塗りつぶしで判定）
  ・つぶれ率 ＝ 1 − (Dela の穴の面積 / Noto の穴の面積)

■ 陽性対照
  `--pos` … Noto の側も Dela で焼く。**つぶれ率が全部 0 に近づけば**測れている
  （同じ字を同じ書体で比べているのだから差が出てはいけない）。

    python -u qa_out/kb_w_crush.py            # SPEC の答えに出る漢字を全部
    python -u qa_out/kb_w_crush.py --pos
    python -u qa_out/kb_w_crush.py 個 機 械   # 字を指定
"""
import io
import re
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import titan_fig as T                                       # noqa: E402
from cuts import SPEC                                       # noqa: E402

KJ = re.compile(r"[一-鿿]")
SIZE = 96                                    # 画面で使う級数の中央あたり
PAD = 24
FILES = {"Dela": "DelaGothicOne.woff2", "Noto": "NotoSansJP-Black.woff2"}


def _ttf(family):
    """woff2 を ttf に戻して PIL に渡す。⚠️ 落ちたら止める（0 で埋めない）。"""
    from fontTools.ttLib import TTFont
    f = TTFont(ROOT / "fonts" / FILES[family])
    buf = io.BytesIO()
    f.flags = 0
    f.save(buf)
    buf.seek(0)
    return buf


_FONT = {}


def font(family):
    if family not in _FONT:
        _FONT[family] = ImageFont.truetype(_ttf(family), SIZE)
    return _FONT[family]


def _components(mask):
    """つながった塊ごとの画素数（大きい順）。"""
    h, w = mask.shape
    seen = np.zeros_like(mask)
    out = []
    for y0 in range(h):
        for x0 in range(w):
            if not mask[y0, x0] or seen[y0, x0]:
                continue
            n, q = 0, deque([(y0, x0)])
            seen[y0, x0] = True
            while q:
                y, x = q.popleft()
                n += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
            out.append(n)
    return sorted(out, reverse=True)


def holes(ch, family):
    """その字の「囲まれた空き」の画素数と、字面（インク）の画素数。"""
    im = Image.new("L", (SIZE + PAD * 2, SIZE + PAD * 2), 255)
    ImageDraw.Draw(im).text((PAD, PAD), ch, font=font(family), fill=0)
    a = np.asarray(im) < 128                                # True ＝ インク
    if not a.any():
        raise SystemExit(f"🔴 {family} で「{ch}」が1画素も出ない（0件と数えない）")
    white = ~a
    h, w = white.shape
    seen = np.zeros_like(white)
    q = deque()
    for x in range(w):                                      # 外周から塗る
        for y in (0, h - 1):
            if white[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if white[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and white[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    # 🔴 2026-09-10：**面積比では決まらなかった。**「年」65.9%・「日」64.9% と
    #    「個」68.6% がほぼ同じ値になり、絵では 年・日 は読めて 個 は読めない。
    #    Dela は極太の見出し書体なので、**どの字でも穴は等しく縮む**。
    #    → 見るのは面積ではなく **「まともな大きさの穴がいくつ残るか」**。
    #      個は 亻 の隙間・囗 の中・口 の中が**互いに埋まって1つになる**。
    inner = white & ~seen
    comps = _components(inner)
    big = [c for c in comps if c >= 40]                      # 40画素未満は穴に見えない
    return int(inner.sum()), int(a.sum()), len(big), (big[0] if big else 0)


def chars_in_spec():
    """SPEC の「答え」のうち **Dela で焼かれる** ものに入る漢字。"""
    out = {}
    for cid, sp in SPEC.items():
        vs = [a["v"] for a in (sp.get("ann") or []) if a.get("v")]
        f = sp.get("fig")
        if f and f[0] in ("panel", "moment"):
            vs += [b["v"] for b in (f[1].get("blocks") or []) if b.get("v")]
        for v in vs:
            v = str(v)
            if T.numfam(v, "Dela") != "Dela":
                continue
            for ch in KJ.findall(v):
                out.setdefault(ch, set()).add(cid)
    return out


def main(argv):
    pos = "--pos" in argv
    want = [a for a in argv if not a.startswith("--")]
    print(f"■ 焼いたフォント: {ROOT / 'fonts' / FILES['Dela']}／"
          f"{ROOT / 'fonts' / FILES['Noto']}")
    print(f"■ 級数 {SIZE}px／モード: {'陽性対照（両方 Dela）' if pos else '実測'}")
    table = ({c: set() for c in "".join(want)} if want else chars_in_spec())
    rows = []
    for ch, cids in table.items():
        hd, _ink_d, nd, _bd = holes(ch, "Dela")
        hn, _ink_n, nn, _bn = holes(ch, "Dela" if pos else "Noto")
        lost = max(0, nn - nd)                               # 消えた穴の数
        crush = 0.0 if hn == 0 else max(0.0, 1 - hd / hn)
        rows.append((lost, crush, ch, nd, nn, sorted(cids)))
    rows.sort(reverse=True)
    print(f"\n{'字':2} {'消えた穴':>6} {'Dela':>5} {'Noto':>5} {'面積比':>7}  カット")
    for lost, crush, ch, nd, nn, cids in rows:
        mark = "🔴" if lost >= 2 else ("⚠️" if lost == 1 else "  ")
        print(f"{mark}{ch}  {lost:>6} {nd:>5} {nn:>5} {crush * 100:>6.1f}%  "
              + " ".join(cids[:8]) + (" …" if len(cids) > 8 else ""))
    bad = [r for r in rows if r[0] >= 2]
    print(f"\n{'🔴' if bad else '✓'} 穴が2つ以上消える字 ＝ {len(bad)}"
          f"／測った {len(rows)} 字")
    print("  ⚠️ しきい値は**面積比では決まらなかった**（年 65.9%・日 64.9% と"
          "個 68.6% がほぼ同じで、絵では年・日は読める）。**穴の数**で見る。")
    if pos:
        print("  ⚠️ 陽性対照は**つぶれ率が全部 0%** になれば通り"
              "（同じ字を同じ書体で比べているので差が出てはいけない）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
