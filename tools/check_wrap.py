# -*- coding: utf-8 -*-
"""**行が語の途中で割れていないか**の門番（5本目・2026-09-07 新設）。

■ なぜ要るか
  ⑤c-2（原寸）で L-15 として出た型。`titan_fig.wrap()` は**字幅だけで折る**ので、
  「アイダホ支所の報告書（20／8ページ）」＝**数字 208 が 20 と 8 に割れる**、
  「圧力容器（高さ約14.5フィ／ート）」＝カタカナ語が割れる、
  「9番は、炉から完／全に外れていた」＝熟語が割れる、が本番で **12件**出ていた。
  ⚠️ 机上検査は「文字がぶつかっていないか」しか見ないので、**1件も鳴らなかった**。
  ⚠️ 640px の検品シートでも読めない（原寸で初めて分かる）。＝**機械で止めるしかない**。

■ どうやって見るか（🔴 本番の経路をそのまま通す）
  `titan_fig.wrap` と `titan_fig.balance` を**包んで**から `scene_jiko.build_layers()` を
  呼ぶ。＝型が実際に折った行を、呼び出し元を1つも取りこぼさずに拾う。
  ⚠️ 「quote の rows と phrase を自分で拾い直す」書き方にすると、
     **型が増えたときに構造上見えない**（[[feedback-gates-blind-to-the-new-material]]）。

■ 判定
  境目の規則は `titan_fig._midword()` **1か所**に置いてある（門番と型で同じ規則を使う）。
  英字の語をまたぐ割れは `wrap()` 自身が直すので、ここでは見ない。

使い方:
    python tools/check_wrap.py
    python tools/check_wrap.py --all        # 通った行も全部出す
    python tools/check_wrap.py --check      # 陽性対照
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")


def collect():
    """本番の経路で折られた行を全部集める。[(どの関数, 元の文, 行)]"""
    import titan_fig as T
    import scene_jiko as S
    got = []
    orig_w, orig_b, orig_q = T.wrap, T.balance, T.quote_lines

    def wrap(t, cols):
        out = orig_w(t, cols)
        got.append(("wrap", str(t), list(out)))
        return out

    def balance(t, cols):
        out = orig_b(t, cols)
        got.append(("balance", str(t), list(out)))
        return out

    # 🔴 2026-09-17（9本目 ⑤c''）：`quote()` の決め所は `quote_lines()` で折るようにした。
    #    包まないと決め所が**この門番から消える**（[[feedback-gates-blind-to-the-new-material]]）。
    def quote_lines(t, cols=10):
        out = orig_q(t, cols)
        got.append(("quote", str(t), list(out)))
        return out

    T.wrap, T.balance, T.quote_lines = wrap, balance, quote_lines
    try:
        S.build_layers(allow_missing=True)
    finally:
        T.wrap, T.balance, T.quote_lines = orig_w, orig_b, orig_q
    # ⚠️ balance は wrap の中からも呼ばれる（投げ直し）。**採られた側だけ**を見たいので、
    #    同じ文で wrap と balance の両方が出たら wrap の返り値（＝実際に描かれた行）を採る。
    #    quote_lines も中で balance を呼ぶことがある＝quote の返り値を採る。
    best = {}
    for who, t, lines in got:
        if who in ("wrap", "quote") or t not in best:
            best[t] = (who, lines)
    return best


def bad_rows(best):
    import titan_fig as T
    out = []
    for t, (who, lines) in sorted(best.items()):
        for i in range(len(lines) - 1):
            a, b = lines[i].rstrip(), lines[i + 1].lstrip()
            if not a or not b:
                continue
            if T._midword(a[-1], b[0]):
                out.append((t, lines, a[-1], b[0], who))
            # 🔴 2026-09-17（9本目 ⑤c'' 台帳 §C）：決め所の行頭に助詞・「いう」＝前の語から
            #    切り離される（「の／は、」「と／は」「は／ず」「と／いう」が 🔴6件、この門番を通っていた。
            #    `_midword` は助詞のうしろを語の切れ目として通すので、決め所だけ別に見る）
            elif who == "quote" and (b[0] in T._QUOTE_HEAD_NG or b.startswith("いう")):
                out.append((t, lines, a[-1], b[0], "quote・行頭の助詞"))
    return out


def main(show_all=False):
    best = collect()
    # 🔴 fail closed：**1件も折っていないのに ✓ を出さない**
    if not best:
        print("🔴 折られた行が1件も取れなかった（型が wrap を呼んでいないか、包みが外れた）")
        return 1
    bad = bad_rows(best)
    print(f"■ 型が折った文 {len(best)}件・行 {sum(len(v[1]) for v in best.values())}行を見た")
    for t, lines, x, y, who in bad:
        print(f"  🔴 「{'／'.join(lines)}」  {x}|{y} で語の途中（{who}）")
    if show_all:
        for t, (who, lines) in sorted(best.items()):
            if len(lines) > 1:
                print(f"  ・ 「{'／'.join(lines)}」（{who}）")
    if bad:
        print(f"🔴 語の途中・禁則で割れた境目 {len(bad)}件")
    else:
        print("✓ 語の途中で割れた行は無い")
    return 1 if bad else 0


def selfcheck():
    """陽性対照。**判定に使う `_midword` と `wrap` そのもの**を鳴らす。"""
    import titan_fig as T
    ok = []

    def chk(name, got, want=True):
        ok.append(bool(got) == bool(want))
        print(f"  {'✓' if ok[-1] else '🔴'} {name}")

    chk("数字を割ったら鳴る（20|8＝208）", T._midword("0", "8"))
    chk("数と単位を離したら鳴る（21|時）", T._midword("1", "時"))
    chk("熟語を割ったら鳴る（完|全）", T._midword("完", "全"))
    chk("カタカナ語を割ったら鳴る（ィ|ー）", T._midword("ィ", "ー"))
    chk("ひらがな語を割ったら鳴る（ご|ろ）", T._midword("ご", "ろ"))
    chk("禁則（行頭の 、）で鳴る", T._midword("る", "、"))
    # 🔴 2026-09-07 r02 の原寸で見つけた3件（規則を足したら検算も足す）
    # ⚠️ 引数は (行末の字, 次の行の頭の字)。始め括弧が**行末に残る**のは x 側
    chk("行末に始め括弧を残したら鳴る（（|2）", T._midword("（", "2"))
    chk("小数点で数を割ったら鳴る（14.|5）", T._midword(".", "5"))
    chk("漢字＋活用のかなで鳴る（触|れ）", T._midword("触", "れ"))
    chk("漢字＋助詞では鳴らない（部|に）", T._midword("部", "に"), False)
    chk("閉じ括弧は行末に置いてよい（）|次）", T._midword("）", "次"), False)
    chk("助詞のうしろでは鳴らない（は|次）", T._midword("は", "次"), False)
    chk("読点のうしろでは鳴らない（、|次）", T._midword("、", "次"), False)
    chk("漢字＋活用のかなで鳴る（見|た＝「見た」は1語）", T._midword("見", "た"))
    chk("漢字＋助詞では鳴らない（棒|の）", T._midword("棒", "の"), False)
    # 🔴 2026-09-17（9本目 ⑤c B-48）
    chk("カタカナの名前を中黒で割ったら鳴る（ス・|ロ）", T._midword("・", "ロ"))
    chk("カタカナの名前の中黒を行頭に出したら鳴る（ス|・ロ）", T._midword("ス", "・"))
    lines = T.wrap("テネリフェ島のロス・ロデオス空港", int((470 - 60) / 32))
    chk(f"本番の文が名前の中黒で割れない「{'／'.join(lines)}」",
        not any(T._midword(lines[i].rstrip()[-1], lines[i + 1].lstrip()[0])
                for i in range(len(lines) - 1)))
    # 🔴 実際に本番で割れていた文で、**折り直しが効いている**ことを見る
    cols = int((470 - 60) / 32)
    cases = [("アイダホ支所の報告書（208ページ）", cols),
             ("圧力容器（高さ約14.5フィート）", cols),
             ("1961年1月3日 21時01分の時点", cols),
             ("0.9マイル北西の門衛所の人体汚染計", cols),
             ("制御棒の駆動部に手を触れるため", cols)]
    for t, c in cases:
        lines = T.wrap(t, c)
        bad = [1 for i in range(len(lines) - 1)
               if lines[i].rstrip() and lines[i + 1].lstrip()
               and T._midword(lines[i].rstrip()[-1], lines[i + 1].lstrip()[0])]
        chk(f"本番の文が語の途中で割れない「{'／'.join(lines)}」", not bad)
    # 決め所（balance）も同じ規則で見る
    for t in ("9番は、炉から完全に外れていた", "ふつうの火災警報のはずだった"):
        lines = T.balance(t, 10)
        bad = [1 for i in range(len(lines) - 1)
               if T._midword(lines[i][-1], lines[i + 1][0])]
        chk(f"決め所が語の途中で割れない「{'／'.join(lines)}」", not bad)
    # 🔴 2026-09-17（9本目 ⑤c''）：決め所の行頭の助詞。**判定を鳴らす対照**と**折り方の対照**の両方
    chk("決め所の判定が鳴る（旧 balance の「燃えていたの／は、二機だった」）",
        bad_rows({"x": ("quote", ["燃えていたの", "は、二機だった"])}))
    chk("決め所の判定が鳴る（「許可に「離陸」と／いう語を使わない」）",
        bad_rows({"x": ("quote", ["許可に「離陸」と", "いう語を使わない"])}))
    for t in ("その資格を出したのは、この機長だった", "誰も「離陸中」とは受け取らなかった",
              "二機とも、来るはずのない空港にいた", "許可に「離陸」という語を使わない",
              "降りて、すき間を測った", "超えたら、法律で裁かれる"):
        lines = T.quote_lines(t, 10)
        chk(f"決め所が意味の途中で割れない「{'／'.join(lines)}」",
            len(lines) == 2 and not bad_rows({t: ("quote", lines)}))
    # 🔴 本番の経路（包み）が本当に行を拾えているか
    best = collect()
    chk(f"本番の経路で行を拾える（{len(best)}件）", len(best) > 50)
    chk(f"本番の経路で決め所を拾える（{sum(1 for v in best.values() if v[0] == 'quote')}件）",
        sum(1 for v in best.values() if v[0] == "quote") >= 10)
    good = all(ok)
    print("  " + (f"✓ 陽性対照 {len(ok)}/{len(ok)}" if good
                  else f"🔴 陽性対照 {sum(ok)}/{len(ok)} で落ちた"))
    return good


if __name__ == "__main__":
    if "--check" in sys.argv or "--selftest" in sys.argv:
        sys.exit(0 if selfcheck() else 1)
    sys.exit(main(show_all="--all" in sys.argv))
