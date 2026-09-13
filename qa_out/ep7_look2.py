"""7本目「9.11」 ⑤c-2（疑いを原寸で見る）の物差し。

⚠️ この回だけの道具（6本目キー橋 C7 の反省で `qa_out/` に置く）。
⚠️ 目で見た所見を**画素で裏を取る**ためのもの。目の代わりではない。

使い方（どれも `PYTHONIOENCODING=utf-8` を付けて回す）:
    python qa_out/ep7_look2.py bars  c110 c216 c217   … 色の付いた箱の幾何を実測
    python qa_out/ep7_look2.py pr11                   … 積み上げ棒の区画と字の位置を計算＋実測
    python qa_out/ep7_look2.py ink   c223 c315 ...    … インク率（ほぼ白一色か）
    python qa_out/ep7_look2.py band  c511 c512 c514   … 上端/下端に残る帯（焼き込みのメニュー）
    python qa_out/ep7_look2.py blank c813 ...          … いちばん広い空白の帯
    python qa_out/ep7_look2.py crop  c114 300 100 700 400 … 切り出して保存（原寸のまま）
    python qa_out/ep7_look2.py selftest               … 陽性対照（物差しが生きているか）
"""
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent.parent
QA = HERE / "out" / "jiko" / "qa_ep7-r01"
CROP = HERE / "qa_out" / "ep7_crop2"

BG = (15, 25, 34)          # J.BG   #0f1922
COLS = {
    "ALERT": (224, 80, 60),    # 赤
    "LINE": (143, 182, 201),   # 青
    "DOC": (194, 164, 120),    # 砂
    "INST": (172, 147, 212),   # 紫
    "AMBER": (232, 179, 60),
    "OK": (95, 191, 143),
}


def load(cid):
    p = QA / f"cut_{cid}.jpg"
    if not p.exists():
        raise SystemExit(f"E: {p} が無い")
    return Image.open(p).convert("RGB")


def _mask(im, rgb, tol=26):
    """rgb に近い画素の集合を {x: [y,...]} で返す（線の色＝純色だけ拾う）。"""
    px = im.load()
    w, h = im.size
    cols = {}
    r0, g0, b0 = rgb
    for x in range(w):
        ys = []
        for y in range(h):
            r, g, b = px[x, y]
            if abs(r - r0) <= tol and abs(g - g0) <= tol and abs(b - b0) <= tol:
                ys.append(y)
        if ys:
            cols[x] = ys
    return cols


def _runs(xs, gap=6):
    """x の並びを、間が gap 超で切れる塊に分ける。"""
    xs = sorted(xs)
    out, cur = [], [xs[0]]
    for x in xs[1:]:
        if x - cur[-1] <= gap:
            cur.append(x)
        else:
            out.append(cur)
            cur = [x]
    out.append(cur)
    return out


def cmd_bars(cids):
    """色の付いた縦の箱を見つけて、上端・下端・高さ・幅を実測する。"""
    for cid in cids:
        im = load(cid)
        print(f"\n■ {cid}  {im.size}")
        for name, rgb in COLS.items():
            cols = _mask(im, rgb)
            # 箱の線は太さ4px。字や小さな印を捨てるため、縦に80px 以上ある列だけ残す
            tall = {x: ys for x, ys in cols.items() if max(ys) - min(ys) >= 80}
            if len(tall) < 8:
                continue
            for run in _runs(tall.keys(), gap=10):
                if len(run) < 8:
                    continue
                y0 = min(min(tall[x]) for x in run)
                y1 = max(max(tall[x]) for x in run)
                print(f"   {name:6s} x {run[0]:4d}〜{run[-1]:4d}"
                      f"（幅 {run[-1] - run[0] + 1:4d}）"
                      f"  y {y0:4d}〜{y1:4d}（高さ {y1 - y0 + 1:4d}）"
                      f"  列数 {len(run)}")


def cmd_edges(cids, minrun=240):
    """箱の**枠線**だけを測る。

    🔴 `bars` は色のマスクだけで塊を作るので、**同じ色で描かれた数字の文字**まで
       一緒に拾ってしまう（c217 で 411 の箱が y280〜819＝高さ540 と出たが、
       式では 565〜818＝高さ253。差の 285px は数字「411」の字だった）。
       枠は太さ4px の横線なので、**横に minrun 以上つながる行**だけを枠と見なす。
    """
    for cid in cids:
        im = load(cid)
        px = im.load()
        w, h = im.size
        print(f"\n■ {cid}  {im.size}  （横に {minrun}px 以上つながる色の行＝箱の枠）")
        for name, rgb in COLS.items():
            r0, g0, b0 = rgb
            rows = []
            for y in range(h):
                best = cur = 0
                x0 = bx0 = 0
                for x in range(w):
                    r, g, b = px[x, y]
                    if abs(r - r0) <= 30 and abs(g - g0) <= 30 and abs(b - b0) <= 30:
                        if cur == 0:
                            x0 = x
                        cur += 1
                        if cur > best:
                            best, bx0 = cur, x0
                    else:
                        cur = 0
                if best >= minrun:
                    rows.append((y, bx0, bx0 + best - 1, best))
            if not rows:
                continue
            # 続く行をまとめる（枠線は4〜5px ぶん続く）
            for run in _runs([r[0] for r in rows], gap=3):
                sel = [r for r in rows if r[0] in run]
                x0 = min(r[1] for r in sel)
                x1 = max(r[2] for r in sel)
                print(f"   {name:6s} y {run[0]:4d}〜{run[-1]:4d}"
                      f"  x {x0:4d}〜{x1:4d}（幅 {x1 - x0 + 1:4d}）")


def cmd_pr11():
    """積み上げ棒の区画と、区画の中に置いた数字の位置を計算する。"""
    sys.path.insert(0, str(HERE / "tools"))
    import fontmetrics as fm  # noqa
    BX0, BX1, BW = 72, 1848, 1776
    tot = 2973
    parts = [("世界貿易センター", 2749), ("ペンタゴン", 184), ("ペンシルベニア州", 40)]
    x = BX0
    print("■ pr11 計算（titan_fig.breakdown の式そのまま）")
    boxes = []
    for t, v in parts:
        w = BW * v / tot
        vs = fm.fit(str(v), w * 0.7, "Dela", cap=64, floor=22)
        vw = fm.width(str(v), vs, "Dela")
        vx = min(max(x + w / 2, BX0 + vw / 2), BX1 - vw / 2)
        print(f"   {t:9s} v={v:5d}  区画 x {x:7.1f}〜{x + w:7.1f}（幅 {w:6.1f}）"
              f"  字の大きさ {vs}  字幅 {vw:5.1f}"
              f"  字 x {vx - vw / 2:7.1f}〜{vx + vw / 2:7.1f}")
        boxes.append((t, v, x, x + w, vx - vw / 2, vx + vw / 2))
        x += w
    print("   ── 字どうしの重なり ──")
    for i in range(len(boxes) - 1):
        a, b = boxes[i], boxes[i + 1]
        ov = a[5] - b[4]
        print(f"   {a[0]}({a[1]}) と {b[0]}({b[1]})："
              f"{'重なり ' + format(ov, '.1f') + 'px' if ov > 0 else '空き ' + format(-ov, '.1f') + 'px'}")
    print("   ── 字が自分の区画から出た量 ──")
    for t, v, x0, x1, tx0, tx1 in boxes:
        out = max(0.0, x0 - tx0) + max(0.0, tx1 - x1)
        print(f"   {t}({v})：区画の外へ {out:.1f}px"
              f"（左 {max(0.0, x0 - tx0):.1f} / 右 {max(0.0, tx1 - x1):.1f}）")


def cmd_ink(cids, box=None):
    """インク率（地の色から離れた画素の割合）。ほぼ白一色かを数で見る。"""
    for cid in cids:
        im = load(cid)
        if box:
            im = im.crop(box)
        px = im.load()
        w, h = im.size
        n = ink = bright = 0
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                r, g, b = px[x, y]
                n += 1
                d = abs(r - BG[0]) + abs(g - BG[1]) + abs(b - BG[2])
                if d > 60:
                    ink += 1
                if r > 200 and g > 200 and b > 200:
                    bright += 1
        print(f"■ {cid}  インク率 {100 * ink / n:5.2f}%"
              f"  ほぼ白の画素 {100 * bright / n:5.2f}%  （標本 {n}）")


def cmd_band(cids, rows=14):
    """上端と下端に横いっぱいの帯が残っていないか（焼き込みのメニュー帯）。

    実写を敷いた欄の画像で、写真の箱の上端/下端の数行を見る。
    """
    for cid in cids:
        im = load(cid)
        px = im.load()
        w, h = im.size
        print(f"■ {cid}")
        for label, ys in (("上", range(0, rows)), ("下", range(h - rows, h))):
            for y in ys:
                dark = sum(1 for x in range(0, w, 3)
                           if sum(px[x, y]) < 150)
                print(f"   {label} y={y:4d}  暗い画素 {100 * dark / (w // 3):5.1f}%")


def cmd_blank(cids):
    """縦に見て、いちばん長く続く「ほぼ空」の帯（下が空くかを数で見る）。"""
    for cid in cids:
        im = load(cid)
        px = im.load()
        w, h = im.size
        empt = []
        for y in range(h):
            ink = sum(1 for x in range(0, w, 4)
                      if sum(abs(a - b) for a, b in zip(px[x, y], BG)) > 60)
            empt.append(ink / (w // 4) < 0.012)
        best = cur = 0
        bs = cs = 0
        for y, e in enumerate(empt):
            if e:
                if cur == 0:
                    cs = y
                cur += 1
                if cur > best:
                    best, bs = cur, cs
            else:
                cur = 0
        print(f"■ {cid}  いちばん長い空の帯 y {bs}〜{bs + best - 1}"
              f"（{best}px＝画面の {100 * best / h:.1f}%）")


def cmd_crop(args):
    cid, x0, y0, x1, y1 = args[0], *[int(v) for v in args[1:5]]
    CROP.mkdir(parents=True, exist_ok=True)
    im = load(cid).crop((x0, y0, x1, y1))
    out = CROP / f"{cid}_{x0}_{y0}_{x1}_{y1}.png"
    im.save(out)
    print(f"■ {cid} → {out}（{im.size[0]}×{im.size[1]}）")


def cmd_selftest():
    """陽性対照。⚠️ 件数でなく**値**で見る（[[feedback-verify-your-own-instrument]]）。"""
    print("■ 陽性対照1 bars：作った絵の箱を測って、仕込んだ値と一致するか")
    from PIL import ImageDraw
    im = Image.new("RGB", (400, 300), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([50, 40, 150, 250], outline=COLS["ALERT"], width=4)   # 高さ211
    d.rectangle([250, 140, 350, 250], outline=COLS["LINE"], width=4)  # 高さ111
    QA.mkdir(parents=True, exist_ok=True)
    p = QA / "cut_ZZTEST.jpg"
    im.save(p, quality=96)
    cmd_bars(["ZZTEST"])
    print("   期待＝ALERT 高さ 211／LINE 高さ 111（±3）")
    print("\n■ 陽性対照2 ink：真っ白と真っ黒")
    for nm, col, exp in (("白", (255, 255, 255), "100.00"), ("地の色", BG, "0.00")):
        Image.new("RGB", (200, 200), col).save(QA / "cut_ZZTEST.jpg", quality=96)
        print(f"   {nm}：", end="")
        cmd_ink(["ZZTEST"])
        print(f"     期待インク率 {exp}%")
    p.unlink()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "bars":
        cmd_bars(rest)
    elif cmd == "edges":
        cmd_edges(rest)
    elif cmd == "pr11":
        cmd_pr11()
    elif cmd == "ink":
        cmd_ink(rest)
    elif cmd == "band":
        cmd_band(rest)
    elif cmd == "blank":
        cmd_blank(rest)
    elif cmd == "crop":
        cmd_crop(rest)
    elif cmd == "selftest":
        cmd_selftest()
    else:
        raise SystemExit(f"E: 知らない命令 {cmd}")
