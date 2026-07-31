# -*- coding: utf-8 -*-
"""★レイヤーPNGの指紋を出す（2026-07-31 追加）。

■ なぜ要るか
  本編mp4の製造を GitHub Actions から Modal へ移した（規約のため。`modal_app.py` 参照）。
  ところが図は **Chrome headless が SVG から焼いている**ので、
  ブラウザのビルドが変わると**折返し位置や字送りが変わりうる**。

  226カットの検品は **9巡すべて Actions の出力を見て**やった。
  移設先で1画素でも違えば、その9巡は無効になる。
  だから「同じ画になっているか」を機械で確かめられるようにしておく。

■ 何を出すか
  PNG のファイルそのものではなく **画素データ**を hash する
  （PNG のバイト列にはエンコーダ由来の差が乗るので、比較に使えない）。

    ① 全レイヤーをまとめた1個の指紋 … これが一致すれば完全一致
    ② 代表20枚の指紋              … ずれたときにどこかを絞るため

■ 使い方
    python tools/layer_hash.py              … out/jiko/*.png を測る
    python tools/layer_hash.py --dir=out/jiko

  Actions と Modal の両方で走らせて、**ログの数字を見比べる**。
"""
import hashlib
import sys
from pathlib import Path

from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent.parent


def digest(p):
    """画素そのものの指紋。PNGのバイト列ではなく中身を見る。"""
    with Image.open(p) as im:
        return hashlib.sha256(im.convert("RGBA").tobytes()).hexdigest()


def sample(names):
    """代表として必ず見るレイヤー。**章ごと・種類ごとに散らす。**"""
    want = []
    for pre in ("pr", "c1", "c2", "c3", "c4", "c5", "c6", "ep"):
        ids = sorted({n.split("_")[0] for n in names
                      if n.startswith(pre) and not n.startswith("sub_")})
        if not ids:
            continue
        for cid in (ids[0], ids[len(ids) // 2]):
            want += [n for n in names if n.startswith(cid + "_")][:2]
    want += [n for n in names if n.startswith("sub_")][:3]
    want += [n for n in names if n == "_empty"]
    # 重複を消しつつ順番は固定する（両側で同じ並びになるように）
    return sorted(dict.fromkeys(want))


def main():
    d = next((a.split("=")[1] for a in sys.argv[1:] if a.startswith("--dir=")),
             str(HERE / "out" / "jiko"))
    files = sorted(Path(d).glob("*.png"))
    if not files:
        print(f"🔴 {d} に PNG が無い。先に scene_jiko.py --force を通すこと。")
        return 1
    names = [f.stem for f in files]
    by = {f.stem: f for f in files}

    whole = hashlib.sha256()
    total = 0
    for n in names:                       # sorted 済み＝両側で同じ順
        h = digest(by[n])
        whole.update(n.encode())
        whole.update(bytes.fromhex(h))
        total += by[n].stat().st_size
    print(f"レイヤー {len(names)} 枚 ／ 合計 {total / 1e6:.1f} MB")
    print(f"★全体の指紋  {whole.hexdigest()}")
    print("\n代表（ずれたときに場所を絞るため）")
    for n in sample(names):
        print(f"  {n:<16} {digest(by[n])[:32]}")
    print("\n⚠️ Actions と Modal で**★全体の指紋が一致すれば**、"
          "9巡の検品はそのまま生きている。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
