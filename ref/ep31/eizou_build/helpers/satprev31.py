# -*- coding: utf-8 -*-
"""31本目 ⑤b-3b：地図のカットの確かめ用の重ね絵（Modal の前に札と線を決める＝30本目 ⑤b-3 の型）。

  python -P ref/ep31/eizou_build/helpers/satprev31.py <出力のフォルダ> c105 c201 …   # カットごとに 1920×1080 の PNG＋並べ（2列×2行・1枚 960px）

撮った PNG を base64 で HTML に入れ、`satmap.layers`（本番の描き手の SVG＝全部の段を重ねる）と額の箱・見出し・副題・額の下の断りを置き、
画面なしの Chrome で撮る。⚠️ 本番の絵ではない（章の色・地の方眼・字幕の帯・フェードは無い）＝札と線の置き場と重なりを見るだけ。
⚠️ 出力は絶対の道で（作業の置き場は出力のフォルダの中）。🔴 撮った絵を含む＝公開リポに置かない
"""
import base64
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def page(cid, s, M, J):
    bx, by, bw, bh = M.box()
    src = os.path.join(REPO, "ref", s["photo"])
    b64 = base64.b64encode(open(src, "rb").read()).decode()
    lay = "".join(M.layers(s))
    keep = "".join(
        f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" fill="none" stroke="#ff00ff" stroke-width="1" stroke-dasharray="4 4"/>'
        for x0, y0, x1, y1 in (M.ibox_to_screen(b) for b in M.keep_of(__import__("cuts.ss", fromlist=["SAT"]).SAT[s["sat"]["code"]]).values()))
    cr = s.get("credit") or __import__("cuts.ss", fromlist=["SAT"]).SAT[s["sat"]["code"]]["credit"]
    head = J.outlined(J.MG, 92, s.get("t", ""), J.INK_W, 56, sw=8) + J.outlined(J.MG, 140, s.get("s", ""), J.TICK, 30, sw=6)
    foot = J.outlined(J.RIGHT, J.BAND_B - 4, cr, J.TICK, M.SUBTLE, "end", sw=5)
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;width:1920px;height:1080px;overflow:hidden;background:{J.BG}}}</style></head>'
            f'<body><div style="position:relative;width:1920px;height:1080px">'
            f'<img src="data:image/png;base64,{b64}" style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px">'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" style="position:absolute;left:0;top:0">'
            f'<line x1="0" y1="{J.BAND_B}" x2="1920" y2="{J.BAND_B}" stroke="#ff00ff" stroke-width="1"/>{keep}{lay}{head}{foot}'
            f'<text x="1900" y="40" fill="#ff00ff" font-size="28" text-anchor="end">{cid}</text></svg></div></body></html>')


def main():
    out = os.path.abspath(sys.argv[1])
    cids = sys.argv[2:]
    import cuts
    import jiko_style as J
    import satmap as M
    os.makedirs(out, exist_ok=True)
    pngs = []
    for cid in cids:
        s = cuts.SPEC[cid]
        html = os.path.join(out, f"{cid}.html")
        open(html, "w", encoding="utf-8").write(page(cid, s, M, J))
        png = os.path.join(out, f"{cid}.png")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--screenshot={png}", "--window-size=1920,1080",
                        "--virtual-time-budget=3000", "file:///" + html.replace("\\", "/")], check=True, capture_output=True, timeout=120)
        pngs.append(png)
        print(cid, "→", png)
    from PIL import Image
    for i in range(0, len(pngs), 4):
        sheet = Image.new("RGB", (1920, 1080), (40, 40, 40))
        for j, p in enumerate(pngs[i:i + 4]):
            im = Image.open(p).convert("RGB").resize((960, 540), Image.LANCZOS)
            sheet.paste(im, ((j % 2) * 960, (j // 2) * 540))
        sp = os.path.join(out, f"sheet{i // 4 + 1}.png")
        sheet.save(sp)
        print("並べ →", sp)
    return 0


if __name__ == "__main__":
    sys.exit(main())
