# -*- coding: utf-8 -*-
"""measure_map16.py — 16本目の形のもと（#100 イタリア軍地理院 1934年の地形図・PD）を測る道具の**骨組み**（2026-10-01 ⑤b-1）。

映像方針 §7（Vault `Projects/事故検証-16本目-映像方針-絵コンテ-20261001.md`）：谷の平面（VA）と2本の断面（VB・VC）の地形は
#100 から起こす。⑤b-1 で原寸を見て「機械で測れるか」を決めた＝**方眼だけ機械・湖の700m の線は目で読んで記録で照らす**：
  ・1,600×845px の JPEG・茶と灰の単色刷り（青みの画素は全体で約285個＝川・道・等高線が色で分かれない）
  ・等高線は細い線で、森の記号（小さな丸）・崖の毛羽・道の二重線・標高の数字で何度も途切れる＝1本を機械で追えない
  ・1 km 方眼の縦線は列の明るさのくぼみとして約185画素おきに取れる（x≈118・303・487・670・854・1041・1227・1415・横線 y≈430）
    ＝1画素≈5.4m の見込み（1 km 方眼なら。地点の座標〈Wikidata〉で照らして決める）
→ 形を起こすのは ⑤b-2（置き場 VA）から。この道具は3つの仕事だけ持つ：

    python ref/ep16/measure_map16.py grid             # 方眼を機械で取る（くぼみ・間隔・ずれ）＝縮尺
    python ref/ep16/measure_map16.py sheet X0 Y0      # 原寸2倍＋10画素の目盛りの切り出し（目で読む用・qa_out/ep16_b1/）
    python ref/ep16/measure_map16.py check            # 目で読んだ点（ref/ep16/map16.json）を記録の距離で照らす

🔴 #100 の取得はカズヤくんの許可のあと（ファイル名・出どころ・大きさ）。置き場＝`ref/ep16/src/igm1934.jpg`（git の外）。
   無いあいだは止まる（黙って0件で通さない）。
⚠️ 目で読んだ点は「目で読んだ」と JSON に書く（`how`）。画面の出典の行は「地形＝1934年の地形図（イタリア軍地理院）から」・
   読めなかった所は「地形は模式」（映像方針 §7）。S8 の図・BY-SA・CC BY・Google Earth はなぞらない
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
SRC = HERE / "ref" / "ep16" / "src" / "igm1934.jpg"          # #100（git の外）
POINTS = HERE / "ref" / "ep16" / "map16.json"                # 目で読んだ点（画素）＝⑤b-2 で作る
SHEETS = HERE / "qa_out" / "ep16_b1"
GRID_SPACING_GUESS = 185        # ⑤b-1 にブラウザの表示で測った見当（画素）。grid が実測で上書きする
DIP = 12                        # 列（行）の平均の明るさが全体より これ以上暗い所＝線の候補

# 記録の距離（照らす相手＝映像方針 §7 の 5b-109②・範囲ごとに記録の値を1つ以上）
REC_DIST = [
    dict(a="dam", b="tunnel_in", km=2.5, tol=0.25, rec="S1 PDF85（迂回トンネルの入口＝ダムの約2.5キロ上流）"),
    dict(a="dam", b="north_1100", km=1.1, tol=0.15, rec="S1 PDF146（北の岸の印＝ダムの真横と約1.1キロ上流）"),
    dict(a="slide_w", b="slide_e", km=1.7, tol=0.2, rec="S1 PDF144（崩れた斜面の幅およそ1.7キロ）"),
]


def load():
    if not SRC.exists():
        raise SystemExit(f"🔴 {SRC.relative_to(HERE)} が無い＝#100 の取得はカズヤくんの許可のあと"
                         "（Mappa_Vajont_IGM_1934.jpg・Wikimedia Commons・1,600×845・579KB・PD）")
    from PIL import Image
    return Image.open(SRC).convert("RGB")


def dips(means, dip=DIP):
    """平均の明るさの列（行）から、まわりより暗い極小の位置を返す。"""
    avg = sum(means) / len(means)
    return [i for i, v in enumerate(means)
            if v < avg - dip and (i == 0 or v <= means[i - 1]) and (i == len(means) - 1 or v <= means[i + 1])]


def lattice(pos, guess=GRID_SPACING_GUESS):
    """くぼみの位置から等間隔の並び（方眼）を選ぶ＝隣どうしの差が見当の±10%の鎖。(間隔の平均, 線の位置)"""
    best = []
    for start in pos:
        chain = [start]
        for p in pos:
            if p > chain[-1] and abs((p - chain[-1]) - guess) <= guess * 0.1:
                chain.append(p)
        best = max(best, chain, key=len)
    if len(best) < 3:
        return None, best
    gaps = [b - a for a, b in zip(best, best[1:])]
    return sum(gaps) / len(gaps), best


def grid():
    im = load()
    w, h = im.size
    px = im.load()
    lum = [[0.299 * px[x, y][0] + 0.587 * px[x, y][1] + 0.114 * px[x, y][2] for x in range(w)] for y in range(h)]
    cols = [sum(lum[y][x] for y in range(h)) / h for x in range(w)]
    rows = [sum(lum[y]) / w for y in range(h)]
    sx, vx = lattice(dips(cols))
    sy, vy = lattice(dips(rows))
    print(f"■ #100 {w}×{h}px")
    print(f"  縦の線 {len(vx)}本 {vx} 間隔 {sx and round(sx, 1)}px")
    print(f"  横の線 {len(vy)}本 {vy} 間隔 {sy and round(sy, 1)}px")
    if not sx or not sy or abs(sx - sy) > 0.05 * sx:
        raise SystemExit("🔴 方眼が等間隔に取れない（縦と横の間隔が5%より違う）＝目で確かめてから")
    print(f"✓ 方眼の間隔 {round((sx + sy) / 2, 1)}px（1 km 方眼なら 1画素≈{1000 / ((sx + sy) / 2):.2f}m＝地点の座標で照らして決める）")
    return (sx + sy) / 2, vx, vy


def sheet(x0, y0, size=(400, 300), k=2):
    """原寸 k 倍の切り出しに 10画素（原寸）ごとの目盛りを足す（目で読む用・qa_out/ep16_b1/）。"""
    from PIL import ImageDraw
    im = load().crop((x0, y0, x0 + size[0], y0 + size[1])).resize((size[0] * k, size[1] * k), 0)
    d = ImageDraw.Draw(im)
    for i in range(0, size[0] + 1, 10):
        d.line([(i * k, 0), (i * k, 12 if i % 50 else 24)], fill=(220, 0, 0), width=1)
        if i % 50 == 0:
            d.text((i * k + 2, 26), str(x0 + i), fill=(220, 0, 0))
    for j in range(0, size[1] + 1, 10):
        d.line([(0, j * k), (12 if j % 50 else 24, j * k)], fill=(220, 0, 0), width=1)
        if j % 50 == 0:
            d.text((26, j * k + 2), str(y0 + j), fill=(220, 0, 0))
    SHEETS.mkdir(parents=True, exist_ok=True)
    out = SHEETS / f"igm1934_x{x0}_y{y0}_k{k}.png"
    im.save(out)
    print(f"✓ {out.relative_to(HERE)}（原寸 {size[0]}×{size[1]}px を {k} 倍・10画素の目盛り）")


def check():
    """目で読んだ点（画素）を km に直し、記録の距離と照らす。⑤b-2 で map16.json を作ってから。"""
    if not POINTS.exists():
        raise SystemExit(f"🔴 {POINTS.relative_to(HERE)} が無い＝⑤b-2 で目で読んだ点を書いてから（how＝目で読んだ）")
    pts = json.loads(POINTS.read_text(encoding="utf-8"))
    m_per_px = pts["m_per_px"]          # grid と地点の座標で決めた値（JSON に根拠と一緒に書く）
    bad = []
    for r in REC_DIST:
        a, b = pts["points"][r["a"]], pts["points"][r["b"]]
        km = ((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2) ** 0.5 * m_per_px / 1000
        ok = abs(km - r["km"]) <= r["tol"]
        print(f"  {'✓' if ok else '🔴'} {r['a']}→{r['b']} {km:.2f}km（記録 {r['km']}km±{r['tol']}・{r['rec']}）")
        if not ok:
            bad.append(r)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "grid"
    if cmd == "grid":
        grid()
    elif cmd == "sheet":
        sheet(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "check":
        check()
    else:
        raise SystemExit(__doc__)
