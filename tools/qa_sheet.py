# -*- coding: utf-8 -*-
"""⑤c 検品【シート】用の見取り図を焼く（2026-09-07・道具チャットで新設）。

検品画像 240枚（1920×1080）を **1コマ 640×360 の 6コマ組**にまとめ、40枚にする。
40枚＝ちょうど1チャットぶん（1メッセージ4枚 × 10）。

■ なぜ 640px か（工程の新設計 §6・2026-09-07 カズヤくん決定）
    事故検証chで縮小が見逃したのは**文字**で、それは門番（`check_slide`）の担当。
    絵の粗（構図・欠け・貼り位置）は 640px で見える。原寸は「疑い」だけに使う。
    ⚠️ 心理chの「縮小シート禁止」は**別プロジェクトの規則**。ここには持ち込まない
       （[[feedback-channels-are-independent-projects]]）。

■ 🔴 なぜ既定が 3列×2行 ではなく **2列×3行** なのか（2026-09-07 に決め直した）
    設計ノートは「1920×1080 の 3×2」と書いてあるが、そのまま組むと**長辺が 1920px** になる。
    読み手（私）に画像が渡るとき、長辺が 1568px を超えると**縮小されて届く**規約なので、
    3列だと 1920 → 1568（0.817倍）＝ **1コマは 640px ではなく 523px** になる。
    ＝「640px で全数見た」が嘘になる（[[feedback-verify-your-own-instrument]]）。

    2列×3行にすると **1280×1164**。長辺 1280 ≤ 1568 なので縮まず、1コマは**本当に 640px**。
    ⭐ しかも総画素は 3×2（1920×776）と **完全に同じ 1,489,920px**＝費用も同じ。
      1枚6コマ・40枚も変わらない。**縮小の規約が無かったとしても損をしない**ので既定にした。
    `--grid 3x2` と書けば設計ノートどおりにも焼ける（下の「読み手に届く寸法」の行で実寸が出る）。

■ ⚠️ これは検品の網であって、原寸の代わりではない
    シートで拾うのは「気になった所」。所見を確定させるのは ⑤c-2（疑いを原寸で見る）。
    疑いの記録は `tools/qa_seen.py` の `suspect add` で残す。

■ 使い方
    python tools/qa_sheet.py ss                     # 既定＝いちばん新しい qa_ss-r* から焼く
    python tools/qa_sheet.py ss --src out/jiko/qa_ss-r05
    python tools/qa_sheet.py ss --grid 3x2          # 設計ノートどおりの並べ方
    python tools/qa_sheet.py ss --check             # 焼かずに枚数と順番だけ確かめる
    python tools/qa_sheet.py --selftest             # 物差しの検算（画像は焼かない）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
OUT = HERE / "out" / "jiko"

TILE_W, TILE_H = 640, 360      # 🔴 ここは動かさない（「640px で全数」の根拠）
BAR = 28                       # コマの上に置くカット名の帯
BG = (20, 20, 22)
FG = (255, 226, 140)
LONG_EDGE_MAX = 1568           # 読み手に渡るときに縮められない長辺の上限

# 日本語も出せる Windows のフォント（無ければ ASCII だけの既定フォントに落ちる）
FONT_CANDIDATES = ["C:/Windows/Fonts/meiryob.ttc", "C:/Windows/Fonts/YuGothB.ttc",
                   "C:/Windows/Fonts/meiryo.ttc", "C:/Windows/Fonts/msgothic.ttc",
                   "C:/Windows/Fonts/arialbd.ttf"]


def load_font(size=19):
    for p in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(p, size), True
        except Exception:      # noqa: BLE001  フォントが無い環境でも止めない
            continue
    return ImageFont.load_default(), False


def parse_grid(s):
    m = re.fullmatch(r"(\d+)x(\d+)", s.strip().lower())
    if not m:
        raise SystemExit(f"🔴 --grid は 列x行 の形で書く（例 2x3）。もらった値: {s}")
    cols, rows = int(m.group(1)), int(m.group(2))
    if cols < 1 or rows < 1:
        raise SystemExit("🔴 --grid の列・行は1以上")
    return cols, rows


def sheet_size(cols, rows):
    """シート1枚の寸法と、**読み手に届く実寸**（長辺 1568px で縮められた後）。"""
    w, h = cols * TILE_W, rows * (TILE_H + BAR)
    scale = min(1.0, LONG_EDGE_MAX / max(w, h))
    return (w, h), (round(w * scale), round(h * scale)), round(TILE_W * scale)


def find_src(slug, src):
    if src:
        p = Path(src)
        if not p.is_absolute():
            p = HERE / p
        if not p.is_dir():
            raise SystemExit(f"🔴 --src が無い: {p}")
        return p
    # 既定＝いちばん新しい qa_<slug>-r*（`r05` が `r5` より後に来るよう数で並べる）
    cands = sorted((d for d in OUT.glob(f"qa_{slug}-r*") if d.is_dir()),
                   key=lambda d: (int(re.sub(r"\D", "", d.name.split("-r")[-1]) or 0), d.name))
    if not cands:
        raise SystemExit(f"🔴 out/jiko/qa_{slug}-r* が1つも無い。--src で場所を書く")
    return cands[-1]


def cuts_of(src):
    """検品画像のカット名。**並べ方は `qa_seen.py`（旧 ss_seen.py）とまったく同じ**
    ＝ファイル名の昇順（c101…→ep…→pr…）。⚠️ ここを変えると「見た枚」の記録とずれる。"""
    names = sorted(f.name[4:-4] for f in src.glob("cut_*.jpg"))
    if not names:
        raise SystemExit(f"🔴 {src} に cut_*.jpg が無い")
    return names


def bake(src, dst, cuts, cols, rows, font, dry=False):
    per = cols * rows
    (full, seen_wh, seen_tile) = sheet_size(cols, rows)
    pages = [cuts[i:i + per] for i in range(0, len(cuts), per)]
    if not dry:
        dst.mkdir(parents=True, exist_ok=True)
        for old in dst.glob("sheet_*.jpg"):
            old.unlink()
    made = []
    for pi, page in enumerate(pages, 1):
        out = dst / f"sheet_{pi:02d}_{page[0]}-{page[-1]}.jpg"
        made.append((out, page))
        if dry:
            continue
        sh = Image.new("RGB", full, BG)
        d = ImageDraw.Draw(sh)
        for i, cid in enumerate(page):
            c, r = i % cols, i // cols
            x, y = c * TILE_W, r * (TILE_H + BAR)
            n = cuts.index(cid) + 1
            d.text((x + 6, y + 4), f"{cid}   {n}/{len(cuts)}", font=font, fill=FG)
            with Image.open(src / f"cut_{cid}.jpg") as im:
                sh.paste(im.convert("RGB").resize((TILE_W, TILE_H), Image.LANCZOS),
                         (x, y + BAR))
            d.rectangle([x, y + BAR, x + TILE_W - 1, y + BAR + TILE_H - 1],
                        outline=(70, 70, 74))
        sh.save(out, quality=90, subsampling=0)
    return made, full, seen_wh, seen_tile


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?", default="")
    ap.add_argument("--src", default="", help="検品画像のフォルダ（既定＝いちばん新しい qa_<slug>-r*）")
    ap.add_argument("--out", default="", help="出す先（既定＝out/jiko/sheet_<ver>）")
    ap.add_argument("--grid", default="2x3", help="列x行（既定 2x3。設計ノートどおりなら 3x2）")
    ap.add_argument("--check", action="store_true", help="焼かずに枚数と順番だけ見る")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return 0 if selftest() else 1
    if not a.slug:
        raise SystemExit("🔴 slug を書く（例: python tools/qa_sheet.py ss）")

    cols, rows = parse_grid(a.grid)
    src = find_src(a.slug, a.src)
    ver = src.name[3:] if src.name.startswith("qa_") else src.name
    dst = Path(a.out) if a.out else (OUT / f"sheet_{ver}")
    if not dst.is_absolute():
        dst = HERE / dst
    cuts = cuts_of(src)
    font, jp = load_font()

    made, full, seen_wh, seen_tile = bake(src, dst, cuts, cols, rows, font, dry=a.check)

    print(f"■ {src.relative_to(HERE)} → {dst.relative_to(HERE)}"
          f"{'（--check ＝焼いていない）' if a.check else ''}")
    print(f"   カット {len(cuts)} ／ 1枚 {cols * rows}コマ（{cols}列×{rows}行）"
          f" ／ シート {len(made)}枚")
    print(f"   先頭 {cuts[0]} ／ 末尾 {cuts[-1]}")
    print(f"   シートの寸法 {full[0]}x{full[1]}"
          f"（総画素 {full[0] * full[1]:,}）")
    ng = []
    if seen_wh != full:
        print(f"   🔴 読み手に届く寸法 {seen_wh[0]}x{seen_wh[1]}"
              f"＝1コマ **{seen_tile}px**（長辺 {LONG_EDGE_MAX}px で縮む）")
        ng.append(f"1コマが {seen_tile}px まで縮む（640px で全数、と言えない）")
    else:
        print(f"   ✓ 読み手に届く寸法もそのまま＝1コマは**本当に {seen_tile}px**")
    if not jp:
        print("   ⚠️ 日本語の出せるフォントが見つからず既定フォントで書いた（カット名は ASCII なので読める）")
    if len(made) > 40:
        ng.append(f"シートが {len(made)}枚＝1チャット（40枚）に収まらない")
    for out, page in made[:2] + (made[-1:] if len(made) > 2 else []):
        print(f"     {out.name}  {' '.join(page)}")
    if len(made) > 3:
        print(f"     …（ほか {len(made) - 3}枚）")
    for x in ng:
        print("🔴", x)
    if ng:
        return 1
    print(f"✓ シート {len(made)}枚（1コマ {seen_tile}px）。"
          f"見た枚の記録は `python tools/qa_seen.py {a.slug} mark ...`")
    return 0


def selftest():
    """物差しの検算。⚠️ 画像は1枚も焼かない・読まない。"""
    ok = True

    def say(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '🔴'} {msg}")

    # 1) 既定（2列×3行）は縮まない＝1コマが本当に 640px
    full, seen, tile = sheet_size(2, 3)
    say(full == (1280, 1164), f"2x3 のシートは 1280x1164（実際 {full[0]}x{full[1]}）")
    say(seen == full and tile == 640, f"2x3 は縮まない＝1コマ {tile}px")

    # 2) 🔴 陽性対照：設計ノートどおりの 3列×2行だと**縮んで 640px を割る**
    full3, seen3, tile3 = sheet_size(3, 2)
    say(seen3 != full3 and tile3 < 640,
        f"3x2 は {full3[0]}x{full3[1]} → {seen3[0]}x{seen3[1]}＝1コマ {tile3}px（640px を割る）")

    # 3) ⭐ どちらも総画素は同じ（＝2x3 にしても費用は増えない）
    say(full[0] * full[1] == full3[0] * full3[1],
        f"総画素は同じ {full[0] * full[1]:,}px（費用は変わらない）")

    # 4) 240カットが 6コマ組でちょうど 40枚
    fake = [f"c{i:03d}" for i in range(240)]
    pages = [fake[i:i + 6] for i in range(0, len(fake), 6)]
    say(len(pages) == 40 and len(pages[-1]) == 6, f"240カット → {len(pages)}枚（端数なし）")

    # 5) 端数が出る数でも1枚も落とさない
    odd = [f"c{i:03d}" for i in range(241)]
    pg = [odd[i:i + 6] for i in range(0, len(odd), 6)]
    say(sum(len(p) for p in pg) == 241, f"241カットでも全部載る（{len(pg)}枚・最後は {len(pg[-1])}コマ）")

    # 6) 並べ方が qa_seen と同じ（ファイル名の昇順・pr は最後）
    order = sorted(["cut_pr10.jpg", "cut_c101.jpg", "cut_ep16.jpg", "cut_c701.jpg"])
    say([f[4:-4] for f in order] == ["c101", "c701", "ep16", "pr10"],
        "並べ方はファイル名の昇順（c→ep→pr）")

    # 7) 🔴 --grid の書き間違いは黙って既定に落ちず、止まる
    for bad in ("3", "3*2", "0x6", ""):
        try:
            parse_grid(bad)
            say(False, f"--grid「{bad}」を受け取ってしまった")
        except SystemExit:
            pass
    say(True, "--grid の書き間違いは止まる（既定に黙って落ちない）")

    print("  " + ("✓ 物差しは正しい" if ok else "🔴 物差しに落ちた"))
    return ok


if __name__ == "__main__":
    sys.exit(main())
