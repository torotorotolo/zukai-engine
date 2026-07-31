# -*- coding: utf-8 -*-
"""フォントの字幅と字面を**フォントファイルから直接読む**。推定しない。

■ なぜ要るか（同じ事故を2回やっている）
  1回目 … Dela の数字を 0.72em と見積もり、c7 の「75,000」を 760px と判定して通した。
          実物は約880pxで、隣の「89,680」と接触し**「75,00089,680」に読める画**を
          クラウドまで通してしまった（14巡目）。
  2回目 … サムネで Noto Black のインク高を 0.72em と見積もり、
          赤が上に27px・黄が下に27pxはみ出した。

  そのあと「Dela の数字は 0.84em」「Noto Black のインクは 0.95em」と実測し直したが、
  🔴 **それも平均でしかなかった。** フォントを開いて全字の送り幅を出すと：

      Dela の数字 … 0.588（1）〜 0.924（4）。**最大と最小で 1.57 倍ちがう**
      Noto の数字 … 0.590（Bold・全数字で一定）
      Noto の欧文 … A=0.641 / m=0.964 / W=0.915（「0.56em」は m で 1.7 倍の過小評価）

  「4,444」を 0.84em で見ると 3.66em ＝ 実物 3.97em より **8%狭く**出る。
  狭く出るのがいちばん悪い（通してしまう向きの誤差）。**推定はここで終わりにする。**

■ 何を返すか
  adv(ch, family)          … 1文字の送り幅（em）
  width(text, size, family)… 文字列の幅（px）
  ink(text, size, family)  … (上端, 下端) をベースラインからの px で。字面の実寸
  fit(text, max_px, ...)   … その幅に収まる最大の級数

■ クラウドでも同じ数字が出ること
  woff2 を読むのに fontTools と brotli が要る（requirements.txt に入れた）。
  読めない環境では `fonts/_metrics.json`（このファイルが書き出すキャッシュ）に落ちる。
  キャッシュも無ければ例外にする。**黙って推定に戻さない**（それが事故の元だった）。
"""
import json
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).parent.parent
FONTS = Path(__file__).parent.parent / "fonts"
CACHE = FONTS / "_metrics.json"

# SVG の font-family 名 → フォントファイル
FAMILY_FILE = {
    "Dela": "DelaGothicOne.woff2",
    "Noto": "NotoSansJP-Bold.woff2",
    "NotoM": "NotoSansJP-Medium.woff2",
    "Black": "NotoSansJP-Black.woff2",
}

_FONTS = {}
_CACHE = None


def _load(family):
    """woff2 を開く。fontTools が無ければ None（キャッシュに落ちる）。"""
    if family in _FONTS:
        return _FONTS[family]
    try:
        from fontTools.ttLib import TTFont
        ft = TTFont(FONTS / FAMILY_FILE[family], lazy=True)
        upm = ft["head"].unitsPerEm
        _FONTS[family] = (ft, ft.getBestCmap(), ft["hmtx"], upm, ft.getGlyphSet())
    except Exception:
        _FONTS[family] = None
    return _FONTS[family]


def _cache():
    global _CACHE
    if _CACHE is None:
        _CACHE = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    return _CACHE


def _glyph(ch, family):
    f = _load(family)
    if not f:
        return None
    _, cmap, _, _, _ = f
    return cmap.get(ord(ch))


@lru_cache(maxsize=200000)
def adv(ch, family="Noto"):
    """1文字の送り幅（em）。**フォントの hmtx をそのまま読む。**"""
    f = _load(family)
    if f:
        _, cmap, hmtx, upm, _ = f
        g = cmap.get(ord(ch))
        if g:
            return hmtx[g][0] / upm
        # 字が無い＝豆腐になる。全角幅で見ておく（見落とさないよう missing() で拾う）
        return 1.0
    c = _cache().get(family, {})
    if not c:
        raise RuntimeError(
            f"フォントの実測ができません（fontTools/brotli も {CACHE.name} も無い）。"
            f"pip install -r requirements.txt を実行してください。推定には戻しません。")
    return c["adv"].get(ch, c.get("default", 1.0))


def width(text, size, family="Noto"):
    """文字列の幅（px）。SVG の letter-spacing は使っていないので送り幅の総和でよい。"""
    return sum(adv(c, family) for c in text) * size


@lru_cache(maxsize=100000)
def _ink_em(ch, family):
    """1文字の字面（em）。(ベースラインより上, ベースラインより下) を正の値で返す。"""
    f = _load(family)
    if f:
        from fontTools.pens.boundsPen import BoundsPen
        ft, cmap, _, upm, gs = f
        g = cmap.get(ord(ch))
        if not g:
            return (0.0, 0.0)
        pen = BoundsPen(gs)
        try:
            gs[g].draw(pen)
        except Exception:
            return (0.0, 0.0)
        if not pen.bounds:
            return (0.0, 0.0)          # 空白など
        _, ymin, _, ymax = pen.bounds
        return (ymax / upm, -ymin / upm)
    c = _cache().get(family, {})
    v = c.get("ink", {}).get(ch)
    return tuple(v) if v else (0.74, 0.22)


def ink(text, size, family="Noto"):
    """文字列の字面（px）。(上端, 下端) をベースラインからの距離で返す。

    ⚠️ `<text y=...>` の y は**ベースライン**。字面の上端は y - ink()[0]、
       下端は y + ink()[1]。ここを 0.74/0.22 と決め打ちにしていたのが
       サムネの「上下27pxはみ出し」だった。
    """
    vals = [_ink_em(c, family) for c in text if not c.isspace()]
    if not vals:
        return (0.0, 0.0)
    return (max(v[0] for v in vals) * size, max(v[1] for v in vals) * size)


def fit(text, max_px, family="Noto", cap=999, floor=12, step=1):
    """`max_px` に収まる最大の級数を返す（cap を超えない）。

    「この幅に必ず入れたい」場面はこれを使う。**級数を先に決めて祈らない。**
    """
    if not text:
        return cap
    per = sum(adv(c, family) for c in text)
    s = int(max_px / per) if per else cap
    return max(floor, min(cap, s - (s % step)))


def missing(text, family="Noto"):
    """フォントに無い文字（＝豆腐になる字）を返す。"""
    f = _load(family)
    if not f:
        return []
    _, cmap, _, _, _ = f
    return [c for c in text if not c.isspace() and ord(c) not in cmap]


def dump_cache():
    """fontTools が使えない環境のための実測キャッシュを書き出す。

    台本と図解で実際に使う文字だけでは足りない（あとで文字を足したときに落ちる）ので、
    ASCII・かな・記号は全部入れ、漢字は台本に出るものを入れる。
    """
    import narration
    used = set()
    for _, lines in narration.SCRIPT:
        used |= set("".join(lines))
    for i in range(0x20, 0x7F):
        used.add(chr(i))
    for i in range(0x3000, 0x30FF):
        used.add(chr(i))
    for i in range(0xFF00, 0xFF60):
        used.add(chr(i))
    used |= set("／：・…　○●◯□■◆▲△▶←→↑↓")
    out = {}
    for fam in FAMILY_FILE:
        if not _load(fam):
            sys.exit(f"{fam} を開けませんでした。fontTools と brotli を入れてください。")
        out[fam] = {"adv": {c: round(adv(c, fam), 5) for c in sorted(used)},
                    "ink": {c: [round(v, 5) for v in _ink_em(c, fam)]
                            for c in sorted(used)},
                    "default": 1.0}
    CACHE.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")),
                     encoding="utf-8")
    n = len(out["Noto"]["adv"])
    print(f"{CACHE} に {n}字 × {len(out)}書体を書き出した "
          f"({CACHE.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--dump" in sys.argv:
        dump_cache()
    else:
        for fam in FAMILY_FILE:
            print(f"── {fam} ({FAMILY_FILE[fam]}) ──")
            print(f"   数字 0〜9 : {[round(adv(c, fam), 3) for c in '0123456789']}")
            print(f"   「4,444」 : {width('4,444', 100, fam):.1f}px @100px")
            print(f"   漢字      : {adv('事', fam)}")
            up, dn = ink("事故0Ag", 100, fam)
            print(f"   字面      : 上 {up:.1f}px ／ 下 {dn:.1f}px @100px")
