# -*- coding: utf-8 -*-
"""**画像そのものに焼き込まれた文字**を、こちらが画面に出す文字と突き合わせる。

■ なぜ要るか（2026-08-04 に実害が出て新設）
  `check_dup.py` は **こちらが描いた文字どうし**しか見ていない。
  解説書から切り出した図と表は、**画像の中に日本語のタイトルとセルが入っている**ので、
  その隣に置いた `ann` が同じ言葉を書いても、机上検査5種は**全部通る**。

  r01 の拡大目視で実際に出たもの：

  | カット | 何が二重だったか |
  |---|---|
  | `c514` | 画像は**3行しかない諸元表**なのに、ann がそのうち2行
  |        | （撮影幅 約1.5m／えい航速度 約2kt）を**そのまま写して**いた。100%一致 |
  | `c526` | 副題が図の焼き込みタイトルと同じ（＋額の下の出典で三重）／ann 2つが備考欄の写し |
  | `c513` | ann「えい航式深海カメラ」＝ 図のタイトルと100%一致 |
  | `c325` | ann「温度回復のシミュレーション」＝ 図のタイトルと100%一致 |
  | `c508` | ann「SMS960」「1.1 × 1.3 m」＝ 表のセルの写し |

■ 何を「複写」とするか
  🔴 **数値の言い直しは複写ではない。**（映像ルール §1「図の中は数値・部位名・関係・出どころ」）
     図の中の小さな数字を ann が大きく出すのは、このチャンネルの設計そのもの。
     例：c310 の ann「約2.9秒」は、図1 の中では曲線に埋もれた小さな青字で、
     0.445倍に縮めた額装ではまず読めない。**大きく出すのが仕事。**
  → 数字と単位だけで出来た文字列は見ない（`DATAISH`）。
     **語・句・文**が5字以上つながって一致し、こちらの文字列の6割以上を覆ったときだけ言う。

■ どこから読むか
  `extract_kaisetsu.CROP` を**そのまま**使う（切り出しの定義を二重に書かない）。
  元PDF はテキストPDFなので、矩形の中のテキスト層を読めば
  「その画像に何が写っているか」が**OCRなしで正確に**分かる。
  ⚠️ 報告書の写真（`p*.jpg`）と付図（`f*.jpg`）はスキャンなのでテキスト層が無い。
     こちらは機械では読めないので、**目視で見るしかない**（この道具の守備範囲外）。

使い方：
    python tools/check_burned.py          # 一覧
    python tools/check_burned.py --all    # 5字未満・6割未満も出す（道具の検算）
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import fitz

import cuts
import extract_kaisetsu as EK

MINLEN = 5          # 連続一致がこれ以上
COVER = 0.60        # かつ、こちらの文字列のこの割合以上を覆う

# check_echo と同じ考え方。数字・単位・記号だけで出来た文字列は「複写」と見なさない。
DATAISH = re.compile(r"^[0-9０-９,.，．%％\s"
                     r"a-zA-Zａ-ｚＡ-Ｚ×"
                     r"年月日時分秒回本個名人隻機層枚倍度円件"
                     r"メートルインチフィートポンドマイルパーセントキロミリ"
                     r"ノットヘクタール平方立方約"
                     r"／/・:：〜~\-−－(（)）]+$")


def norm(s):
    return re.sub(r"[、。，．\s「」『』（）()【】・…]", "", str(s))


def longest_common(a, b):
    """いちばん長い**連続**一致。飛び飛びの共通部分列で測ると、
    日本語は助詞と常用漢字が共通なので誤検出だらけになる（check_echo と同じ轍）。"""
    best = ""
    for i in range(len(a)):
        for j in range(i + len(best) + 1, len(a) + 1):
            if a[i:j] in b:
                best = a[i:j]
            else:
                break
    return best


def burned_text():
    """切り出した画像ごとに、その矩形の中の焼き込み文字を返す。"""
    doc = fitz.open(str(EK.src_pdf()))
    out = {}
    for name, page_no, rect, _credit, _what in EK.CROP:
        out[name] = re.sub(r"\s+", "",
                           doc[page_no - 1].get_text("text", clip=fitz.Rect(*rect)))
    return out


def fields(spec):
    yield "見出し", spec.get("t")
    yield "副題", spec.get("s")
    for k, a in enumerate(spec.get("ann") or []):
        for f in ("t", "v", "d"):
            if a.get(f):
                yield f"ann{k + 1}.{f}", a[f]


def main(show_all=False):
    burned = burned_text()
    seen = bad = 0
    for cid in sorted(cuts.SPEC):
        spec = cuts.SPEC[cid]
        key = str(spec.get("photo", "")).split("/")[-1]
        if key not in burned:
            continue
        seen += 1
        text = burned[key]
        hits = []
        for label, value in fields(spec):
            if not value:
                continue
            v = norm(value)
            m = longest_common(v, text)
            cov = len(m) / max(1, len(v))
            if not m:
                continue
            if DATAISH.match(m) and not show_all:
                continue                       # 数値の言い直しは複写ではない
            if show_all or (len(m) >= MINLEN and cov >= COVER):
                hits.append((label, value, m, cov,
                             len(m) >= MINLEN and cov >= COVER
                             and not DATAISH.match(m)))
        for label, value, m, cov, hot in hits:
            if hot:
                bad += 1
            print(f"  {'🔴' if hot else '・'} {cid}  {label:9s}"
                  f"「{value}」← 画像に焼き込み「{m}」({cov:.0%})")
    print(f"\n照合したカット {seen}／複写 {bad}件")
    if bad:
        print("  → 図がすでに持っている言葉は、ann と副題からは外す。"
              "\n     ann は「その画像に無いもの」（数値の読み・出どころ・見るところ）を持つ。")
        return 1
    print("  ✓ 画像の焼き込みと二重になっている言葉は無い")
    print("  ⚠️ 報告書の写真と付図はスキャンで文字が拾えない。**そこは目視で見る。**")
    return 0


if __name__ == "__main__":
    sys.exit(main("--all" in sys.argv))
