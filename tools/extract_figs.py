# -*- coding: utf-8 -*-
"""NTSB 報告書から**まだ使っていない図**を取り出す（2026-08-02）。

■ なぜ要るか
  2026-08-01 に「素材はパブリックドメインだけ」という縛りを外した
  （[[引き継ぎ-事故検証-タイタン号-r13試写指摘-20260801]] §5）。
  ところが**解禁したまま、捨てた素材を戻していなかった**ので、
  実写の比率は 12.0% → 12.7% までしか動いていない。

  さらに調べると、**出所の記載が無い＝NTSB作成＝PD** の図が3枚
  （図7・図18・図22）残っていた。これは**従来の縛りでも使えたはず**の取りこぼし。

■ 使い方
  python tools/extract_figs.py          … ref/ へ書き出す
  python tools/extract_figs.py --list   … 取り出さずに一覧だけ

⚠️ 取り出せるのは**背景のビットマップ**だけ。NTSB が上に載せた矢印・英字ラベルは
   ベクタなので付いてこない。こちらで日本語の注記を当てるので、そのほうが都合が良い。
"""
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import pypdf
from PIL import Image

HERE = Path(__file__).parent.parent
PDF = HERE / "ref" / "ntsb_titan_MIR2536.pdf"

# (図番号, PDFのページ, 画像の番号, 出力名, 出所, 何の絵か)
#   出所が None＝報告書に出所の記載が無い＝NTSB作成＝パブリックドメイン
FIGS = [
    (7,  29, 0, "titan_f07_cobond.png",     None,
     "コボンド工程の図解（断面の拡大つき）"),
    (18, 45, 0, "titan_f18_delam.png",      None,
     "1号殻の端材に出た中心線の剥離"),
    (22, 56, 0, "titan_f22_production.png", None,
     "潜水艇の生産数（1960-1993 と 1994-2017）"),
    (1,   9, 0, "titan_f01_descend.jpg",    "OceanGate",
     "降下していくタイタン"),
    (2,  11, 0, "titan_f02_cylinder.png",   "OceanGate",
     "炭素繊維の円筒とチタンの端部"),
    (4,  13, 0, "titan_f04_lars.png",       "Garry Comber",
     "LARS に載ったタイタン（上から）"),
    (8,  34, 0, "titan_f08_launch.png",     "Garry Comber",
     "船尾のランプから降ろされる LARS とタイタン"),
    (9,  36, 0, "titan_f09_parking.png",    "A. Harvey",
     "セントジョンズの駐車場（屋外・覆い無しで保管）"),
    (10, 38, 0, "titan_f10_mishap.png",     "Steven Taragel",
     "2023年の遠征で起きた不具合"),
    (11, 39, 0, "titan_f11_wreck.png",      "Pelagic Research Services",
     "海底で見つかったときの残骸（後ドームとチタンリング）"),
    (12, 40, 0, "titan_f12_wreck.png",      "Pelagic Research Services",
     "海底の残骸（耐圧殻の破片 A〜D）"),
    (23, 57, 0, "titan_f23_population.png", "Marine Technology Society",
     "有人潜水艇の数の推移（1950-2017）"),
]


def main(list_only=False):
    r = pypdf.PdfReader(str(PDF))
    got = 0
    for fno, pg, idx, name, src, what in FIGS:
        imgs = r.pages[pg - 1].images
        if idx >= len(imgs):
            print(f"  ✗ 図{fno}: p{pg} に画像が {len(imgs)} 枚しかない")
            continue
        im = Image.open(io.BytesIO(imgs[idx].data))
        out = HERE / "ref" / name
        tag = "PD（出所の記載なし＝NTSB作成）" if src is None else f"出所：{src}"
        print(f"  図{fno:2d} {im.size[0]:5d}x{im.size[1]:<5d} {name:28s} {tag}")
        print(f"        {what}")
        if not list_only:
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            im.save(out, quality=92)
            got += 1
    if not list_only:
        print(f"\n✓ {got} 枚を ref/ へ書き出した")
    return 0


if __name__ == "__main__":
    sys.exit(main("--list" in sys.argv))
