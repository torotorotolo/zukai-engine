# -*- coding: utf-8 -*-
"""22本目 ⑥：サムネ（H 型 v1）の地の候補を1枚に並べる（カズヤくんに先に写真を選んでもらう＝記憶 feedback-jiko-thumbnail-rival-format の 10-12）。

候補＝米国の機関が撮った写真だけ（DVIDS＝米沿岸警備隊・海難調査委員会の報告書の FBI の写真）。
🔴 使わない＝ROV（Pelagic＝第三者）・NTSB 図8／図10（個人の写真）・ホライゾン・アークティック（CC BY-SA）・船首（共同）（10-14 の決め）

    python qa_out/ep22_thumb_ground_sheet.py   → out/thumb/ep22-ab/_ground_candidates.jpg
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")
CAND = ["dvids9057342_deck_survey", "dvids9057367_first_hull", "mbi_fig157_aft_segment",
        "mbi_fig159_fwd_segment", "mbi_fig270_viewport_ring", "dvids7875448_sea_from_aircraft",
        "dvids7875444_hc130_cockpit", "dvids7875471_hc130_hangar", "commons_uscg_mbi_8668382"]
CW, CH, COLS = 640, 360, 3
OUT = HERE / "out" / "thumb" / "ep22-ab" / "_ground_candidates.jpg"


def main():
    cred = json.loads((HERE / "ref" / "ep22" / "credits.json").read_text(encoding="utf-8"))
    font = ImageFont.truetype(str(HERE / "assets" / "fonts" / "NotoSansJP-Bold.ttf"), 24) \
        if (HERE / "assets" / "fonts" / "NotoSansJP-Bold.ttf").exists() else ImageFont.load_default()
    rows = -(-len(CAND) // COLS)
    sheet = Image.new("RGB", (CW * COLS, CH * rows), "#111")
    d = ImageDraw.Draw(sheet)
    for i, stem in enumerate(CAND):
        p = next((q for q in (HERE / "ref" / "ep22" / "photo" / f"{stem}.jpg", HERE / "ref" / "ep22" / f"{stem}.jpg") if q.exists()), None)
        x, y = (i % COLS) * CW, (i // COLS) * CH
        if p is None:
            d.text((x + 10, y + 10), f"{i + 1} {stem}（無い）", fill="#f44", font=font)
            continue
        with Image.open(p) as im:
            im = im.convert("RGB")
            s = max(CW / im.width, CH / im.height)
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
            l, t = (im.width - CW) // 2, (im.height - CH) // 2
            sheet.paste(im.crop((l, t, l + CW, t + CH)), (x, y))
        c = cred.get(f"ep22/{stem}.jpg", "")
        lab = f"{i + 1}  {stem}"
        d.rectangle((x, y, x + CW, y + 34), fill="#000")
        d.text((x + 8, y + 3), lab, fill="#ff0", font=font)
        print(f"{i + 1}\t{stem}\t{p.relative_to(HERE)}\t{c}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT, quality=88)
    print(f"→ {OUT}  {sheet.size}")


if __name__ == "__main__":
    main()
