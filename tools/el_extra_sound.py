# -*- coding: utf-8 -*-
r"""el_extra_sound.py — 聞取の**末尾に台本に無い塊**が付いている行を出す（＝台本に無い音が鳴っている疑い）。

  python tools/el_extra_sound.py            … 全行
  python tools/el_extra_sound.py --selftest … 陽性・陰性の対照（API 不使用・無料）

🔴 なぜ要るか（2026-09-20 ⑤a で見つけた穴）:
   `c213-2` は台本が 6.02秒で終わるのに、**6.48秒から「トントのたん」という台本に無い音**が続いていた
   （`el_probe_words` の語の時刻で確認）。既存の網は3つとも素通りした:
     ⚠️ 異音の門番 `el_artifacts` は **0件**。物差しが「本文と同じかそれ以上に大きい、80ms以上の無音に
        挟まれた**短い**塊」なので、**語のように読まれた余分な音**は拾えない
     ⚠️ 一致率は 85%。460行中53行が 85%以下なので順位で埋もれる
     ⚠️ 🔴 **字/秒でも出ない。**数字の多い行は字が少なくてもモーラが多く、遅い順の上位14行は
        **13行が数字の行＝全部が誤報**だった（「502人のうち258人が21歳から30歳」は20字で約45モーラ）
   ⭐ 決め手は「**聞取の末尾に、台本と合わない塊が残るか**」。重複読みの門番（`el_check_dup`）が
      「同じ句が2回」を見るのに対し、こちらは「**台本に無い句が1回**」を見る。

⚠️ 門番ではなく当たり。Scribe の幻聴（音が無いのに字を書く）もあるので、疑いは
   `el_probe_words --ids <行>` の語の時刻で裏を取ってから直す。
"""
import csv
import difflib
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402

DROP = "、。，．,.「」『』（）()・…—-　 　"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    return re.sub(f"[{re.escape(DROP)}]", "", s)


def tail_extra(script: str, heard: str) -> str:
    """聞取の末尾にある、台本と合わない塊を返す（無ければ空）。"""
    a, b = norm(script), norm(heard)
    if not a or not b:
        return ""
    ops = difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes()
    tag, i1, i2, j1, j2 = ops[-1]
    if tag in ("insert", "replace") and i2 == len(a):
        return b[j1:j2] if (j2 - j1) - (i2 - i1) >= 3 else ""
    return ""


def selftest() -> int:
    cases = [
        # (台本, 聞取, 鳴るべきか, 何の例)
        ("1994年には地下1階を672平方メートル増やしたうえ、",
         "1994年には地下1階を672平方メートル増やした上、トントのたん", True, "c213-2 の実物＝台本に無い音"),
        ("はっきり書いている。", "はっきり書いている。", False, "ぴったり一致"),
        ("けがをした人が937人。あわせて1,439人である。",
         "怪我をした人が九百三十七人、合わせて千四百三十九人である。", False, "漢数字化と かな⇄漢字だけ"),
        ("報道は使わない。", "行動は使わない。", False, "先頭の誤読（この道具の担当ではない）"),
        ("その上に床をじかに載せている。", "その上に床を直に乗せている", False, "字の当て違いだけ"),
        ("崩れた1995年6月も、店はふつうに営業していた。",
         "崩れた1995年6月も、店は普通に営業していた。ありがとうございました", True, "末尾に挨拶が付いた型"),
    ]
    ok = True
    for s, h, want, why in cases:
        got = bool(tail_extra(s, h))
        good = got == want
        ok &= good
        print(f"  {'OK ' if good else '🔴 '} 期待{'鳴る' if want else '静か'} 実際{'鳴った' if got else '静か'}"
              f"  「{tail_extra(s, h) or '—'}」  … {why}")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    rows = [r for r in csv.reader(ES.qa_path("el_yomi.tsv").open(encoding="utf-8"), delimiter="\t")][1:]
    heard = {r[0]: r[3] for r in rows}
    hit = []
    for ln in ES.lines():
        ex = tail_extra(ln.text, heard.get(ln.lid, ""))
        if ex:
            hit.append((ln.lid, ex, ln.text, heard[ln.lid]))
    print(f"検査 {len(list(ES.lines()))}行 → 末尾に台本に無い塊 {len(hit)}行")
    for lid, ex, s, h in hit:
        print(f"\n🔴 {lid}  余分「{ex}」")
        print(f"   台本: {s}")
        print(f"   聞取: {h}")
    if not hit:
        print("✅ 0行（⚠️ 0件でも『台本に無い音は無い』の証明ではない。Scribe が書かない音は見えない）")
    return 1 if hit else 0


if __name__ == "__main__":
    sys.exit(main())
