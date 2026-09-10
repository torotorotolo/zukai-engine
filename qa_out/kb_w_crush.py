# -*- coding: utf-8 -*-
"""**Dela で焼かれる漢字**を、本番と同じ級数・書体で全部並べる（⚠️ 読める／読めないは決めない）。

■ 旧版の3つの穴（2026-09-10・台帳 §Y-3-2 で見つけた）
    1. **級数 96px の決め打ち**。本番の級数は **18〜232px**。`c911`「直径24インチ」は 73px。
    2. **Noto を「安全な基準」にしていた**（式＝`消えた穴 = Noto の穴 − Dela の穴`）。
       80px を切ると Noto 側の穴も消えて差が 0 になり、道具は「安全」と出す。
    3. `numfam(v,"Dela") != "Dela"` で**漢字だけの答えを走査外**にしていた。
       ⚠️ しかも前提が誤り ── **`photo_ann` は `numfam()` を通していない**
       （`scene_jiko.py` の `J.outlined(..., family="Dela")`）ので、
       **漢字だけの答えでも Dela のまま焼かれる**（例＝`c916`「斜張橋」80px Dela）。

■ 🔴🔴 作り直して分かったこと ── **この粗は機械では判定できない**
  台帳が絵で下した判定に、字形の物差しを4通り当てて**1つも分離しなかった**。

    ・囲まれた穴の数／面積 … 🔴「種」は期待の 84% を残す。✅「前」は 78% しか残らない
    ・墨率・線の最大の太さ … 🔴「種」86.6% ／ ✅「間」92.3%（読めるほうが黒い）
    ・Dela と Noto の白の比 … 🔴「種」55% ／ ✅「機」53%・✅「間」35%
    ・**決め手**：台帳は**同じ「径」を 73px で「読めない」（`c911`）・76px で「読める」（`c108`）**
      と判定している。白の残りは 20.3% と 22.2% で**ほぼ同じ**。
      ＝ 判定は字形だけの関数ではない（下地の写真・色・周りの語・読む努力が入る）。

  → **この道具は「決める門番」ではない。**「Dela に漢字が入っている所」を全部並べるだけ。
    採否は原寸の絵で決める（[[feedback-desk-checks-dont-see-pictures]]）。
    ⚠️ 数を「0件」と読まない。0件になるのは Dela から漢字が消えたときだけ。

■ 測り方
  級数・書体は SPEC から推し量らず、`scene_jiko.build_layers()` が作る**本番の SVG**の
  `font-size` / `font-family` をそのまま読む（[[feedback-gates-must-share-the-production-geometry]]）。
  並べ替えは「白の残り」（字面の枠の中で墨でない画素の割合）の**小さい順**＝黒い順。
  ⚠️ これは**順位を付けるためだけの数**。読める／読めないの線ではない（上のとおり）。

    python -u qa_out/kb_w_crush.py              # 見出し以外（＝答え・札）だけ
    python -u qa_out/kb_w_crush.py --title      # 見出し（Dela 62px・216カット）も出す
    python -u qa_out/kb_w_crush.py --selftest   # 物差しの検算（陽性対照つき）

  exit 0 ＝ 一覧を出した／3 ＝ 対照が通らない（＝測れていない。0件と数えない）。
"""
import io
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S                                       # noqa: E402

KJ = re.compile(r"[一-鿿]")
TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')
FSIZE = re.compile(r'font-size="([0-9.]+)"')
FFAM = re.compile(r'font-family="([^"]*)"')
TITLE_SIZE = 62.0                    # J.title が使う級数（見出しは様式として Dela）
FILES = {"Dela": "DelaGothicOne.woff2", "Noto": "NotoSansJP-Black.woff2"}

# 台帳が**絵で**下した判定（§X-2-1・§Y-3-3）。この道具の出力に付けて表示する。
LEDGER = {("種", 76): "🔴読めない", ("径", 73): "🔴読めない", ("線", 76): "🔴読めない",
          ("個", 96): "🔴読めない", ("斜", 80): "✅読める", ("張", 80): "✅読める",
          ("橋", 80): "✅読める", ("者", 88): "✅読める", ("緊", 76): "✅読める",
          ("急", 76): "✅読める", ("基", 76): "✅読める", ("径", 76): "✅読める",
          ("間", 76): "✅読める", ("第", 76): "✅読める"}


def _ttf(family):
    """woff2 を ttf に戻して PIL に渡す。⚠️ 落ちたら止める（0 で埋めない）。"""
    from fontTools.ttLib import TTFont
    f = TTFont(ROOT / "fonts" / FILES[family])
    buf = io.BytesIO()
    f.flags = 0
    f.save(buf)
    buf.seek(0)
    return buf


_FONT, _RAW = {}, {}


def font(family, size):
    key = (family, int(size))
    if key not in _FONT:
        if family not in _RAW:
            _RAW[family] = _ttf(family).getvalue()
        _FONT[key] = ImageFont.truetype(io.BytesIO(_RAW[family]), int(size))
    return _FONT[key]


_WHITE = {}


def white(ch, family, size):
    """字面の枠の中で、墨でない画素の割合（小さいほど黒い塊に近い）。"""
    key = (ch, family, int(round(size)))
    if key in _WHITE:
        return _WHITE[key]
    n = max(4, int(round(size)))
    pad = max(8, n // 4)
    im = Image.new("L", (n * 2 + pad * 2, n * 2 + pad * 2), 255)
    ImageDraw.Draw(im).text((pad, pad), ch, font=font(family, n), fill=0)
    ink = np.asarray(im) < 128
    if not ink.any():
        raise SystemExit(f"🔴 {family} {n}px で「{ch}」が1画素も出ない（0件と数えない）")
    ys, xs = np.where(ink)
    box = ink[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    _WHITE[key] = 1.0 - box.sum() / box.size
    return _WHITE[key]


def rendered():
    """本番の SVG に出る文字を (カット, 字面, 級数, 書体) で全部返す。"""
    jobs, _ = S.build_layers(allow_missing=True)
    out, seen = [], set()
    for k, svg in jobs.items():
        cid = k.split("_")[0]
        for m in TEXT.finditer(svg):
            t = m.group(2)
            if not t.strip():
                continue
            fs, ff = FSIZE.search(m.group(1)), FFAM.search(m.group(1))
            if not fs or not ff or ff.group(1) not in FILES:
                continue
            row = (cid, t, float(fs.group(1)), ff.group(1))
            if row not in seen:
                seen.add(row)
                out.append(row)
    return out


def main(argv):
    with_title = "--title" in argv
    print(f"■ 読んだ字形: {ROOT / 'fonts' / FILES['Dela']}")
    print(f"■ 画は本番と同じ経路: {Path(S.__file__).resolve()} の build_layers()")
    rows = rendered()
    dela = [r for r in rows if r[3] == "Dela" and KJ.search(r[1])]
    body = [r for r in dela if r[2] != TITLE_SIZE]
    print(f"■ 本番の文字列 {len(rows)} 件／うち Dela で漢字入り {len(dela)} 件"
          f"／うち見出し（{TITLE_SIZE:.0f}px）を除くと **{len(body)} 件**")
    print(f"■ 級数の幅 {min(r[2] for r in rows):.0f}〜{max(r[2] for r in rows):.0f}px")

    use = dela if with_title else body
    out = []
    for cid, t, size, fam in use:
        ws = [(white(ch, fam, size), ch) for ch in sorted(set(KJ.findall(t)))]
        w, ch = min(ws)
        out.append((w, ch, size, cid, t))
    out.sort()
    print(f"\n{'字':2}{'白の残り':>8}{'級数':>6}  {'台帳':10} カット  文字列（黒い順）")
    for w, ch, size, cid, t in out:
        print(f"  {ch} {w * 100:>7.1f}%{size:>6.0f}  "
              f"{LEDGER.get((ch, int(size)), ''):10} {cid:6} 「{t[:26]}」")
    print(f"\n■ Dela に漢字が入っている所 ＝ {len(out)} 件"
          f"{'（見出しを含む）' if with_title else '（見出しは除く）'}")
    print("  ⚠️ **これは「読めない」の一覧ではない。** 白の残りは順位を付けるための数で、")
    print("     台帳の判定（🔴／✅）とは一致しない。上の docstring の実測を読む。")
    print("  ⚠️ 0件になるのは Dela から漢字が消えたときだけ。**安全の合図ではない。**")
    return 0


def selftest():
    """物差しの検算。⚠️ 「鳴った」ことを数字で見る（[[feedback-verify-your-own-instrument]]）。"""
    ok = True

    def say(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '🔴'} {msg}")

    # 陽性対照①：同じ字なら Dela のほうが Noto より必ず黒い
    pairs = [(white(c, "Dela", 76), white(c, "Noto", 76)) for c in "種線径個間"]
    say(all(d < n for d, n in pairs),
        "陽性対照①：同じ字・同じ級数で Dela < Noto（白が少ない）"
        f"／{['%.3f<%.3f' % p for p in pairs]}")

    # 🔴 陽性対照②：級数を落とすと白は減る……**が、本番の級数の幅では動かない**。
    #    実測（線・Dela）：240px 21.0 ／160 20.0 ／120 19.6 ／96 19.8 ／76 20.8 ／
    #                      62 21.4 ／48 18.9 ／32 19.5 ／**24 12.3 ／16 9.9 ／12 3.0**
    #    ＝ 32px までは**ほぼ平ら**。つまり 44〜120px の本番では、つぶれは
    #      「小さく焼いたから」ではなく**その字が Dela でもともと黒い**から起きている。
    #    ⚠️ 対照は、実際に動く 12px との差で取る（120px との比較では鳴らない）。
    big, small = white("線", "Dela", 120), white("線", "Dela", 12)
    say(small < big * 0.5,
        f"陽性対照②：120px {big * 100:.1f}% → 12px {small * 100:.1f}%"
        "（⚠️ 32px までは平ら＝本番の級数では動かない）")

    # 陰性対照：同じ字・同じ級数を2回測ったら同じ値
    say(white("種", "Dela", 76) == white("種", "Dela", 76), "陰性対照：同じ条件は同じ値")

    # 🔴🔴 いちばん大事な検算 ── **この物差しは台帳の判定を再現しない**。
    #    再現すると書いてしまうと、次のチャットが「0件だから安全」と読む。
    r73, r76 = white("径", "Dela", 73), white("径", "Dela", 76)
    say(abs(r73 - r76) < 0.03,
        f"⚠️ 台帳が🔴とした 径73px（{r73 * 100:.1f}%）と ✅とした 径76px"
        f"（{r76 * 100:.1f}%）は**ほぼ同じ値**＝この物差しでは決められない")
    print(f"\n{'✓ 物差しは通った（ただし判定はできない）' if ok else '🔴 物差しが壊れている'}")
    return 0 if ok else 3


if __name__ == "__main__":
    a = sys.argv[1:]
    raise SystemExit(selftest() if "--selftest" in a else main(a))
