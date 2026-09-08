# -*- coding: utf-8 -*-
r"""el_ab_verdict.py — A/B（el_ab_yomi）の結果から「その候補を EL_YOMI に入れてよいか」を機械で決める。

  python tools/el_ab_verdict.py            … audio/el_qa/<SLUG>_yomi_ab.tsv を読んで判定
  python tools/el_ab_verdict.py --selftest … 対照（API 不使用・無料）

🔴🔴 **一致率で採否を決めない**（feedback-ear-beats-the-meter）。実際に 2026-09-08・キー橋で:
   - `2769メートル` は **前も後も一致率 100.0%** なのに、前の聞取は「二七六九」＝**1桁ずつ読んでいる疑い**、
     後は「二千七百六十九」。一致率は正規化で「千百十」を落とすので、この差が消える。
   - `34121台` は **▲悪化（96.0→91.7%）** と出たが、悪化の中身は「2023年→二千二十三年」という**表記**で、
     肝心の数はどちらも合っていた。
   - `径間→けいかん` は **⭐良化（87.0→91.3%）** と出たが、前「三計観」も後「三径間」も**読みは ケイカン で同じ**
     ＝音は変わっておらず、Scribe が字を当て直しただけ。**入れてはいけない候補**。

⭐ 代わりに見るのは1つ:「**狙った語の読みが、後の聞取に現れ、前の聞取には無い**」か。
   ＝候補の値（かな）の読みを、前後の聞取の読みの中から探す。
     - 前に無く後に有る          → **採用**（音が変わった）
     - 前にも有る                → **見送り**（もともと正しく読めている＝Scribe の字の当て違い）
     - 前にも後にも無い          → **効かなかった**（別の手＝取り直し・空白でアクセント句を切る、へ）
   ⚠️ さらに「**別の語が崩れていないか**」を必ず見る（ep005「測り方を直したら同じ行の『定義』が『重力』に化けた」）。
      後の聞取にだけ現れた食い違いを「巻き添え」として並べる。判断は人（Claude）。

出力: audio/el_qa/<SLUG>_ab_verdict.tsv（行 / key / val / 判定 / 巻き添えの疑い / 前の聞取 / 後の聞取）
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_script as ES              # noqa: E402
from el_reading_diff import canon, reading, compare, MATCH, DIFFER, UNKNOWN  # noqa: E402

ADOPT, SKIP, NOEFFECT, UNSURE = "採用", "見送り（もともと正しい）", "効かなかった", "読みが取れない"


def key_reading(val: str):
    """候補の値（かな混じり）から、狙っている音を作る。読みが取れなければ None。"""
    r, unk = reading(val)
    return None if unk else canon(r)


def _nums(s):
    from check_numbers_heard import heard_numbers
    return heard_numbers(s)


def extra_signals(text: str, key: str, before: str, after: str):
    """🔴 「狙った音が聞取に現れたか」だけでは**2つの型を取りこぼす**（2026-09-08 実測）。

    ① **Scribe が狙いどおりの字を書いた**のに、janome がその語を読めず「効かなかった」に落ちる。
       実例＝c427-3「船首の尾栓」→「船首の**右舷**」／c916-2「七張橋」→「**斜張橋**」。
       ＝ **key の字そのものが、後にだけ現れた**なら直っている。
    ② **数**は reading() が落とす（名詞,数）ので、音の側では永久に見つからない。
       実例＝c809-2「75人」→「**35人**」／c308-2「六百ボルト」→「**六千六百**ボルト」。
       ＝ **台本の数が、後には全部あって前には無い**なら直っている（check_numbers_heard と同じ物差し）。
    """
    sig = []
    if key in after and key not in before:
        sig.append("字が直った")
    import re
    want = set(re.findall(r"\d+(?:\.\d+)?", text.replace("¾", "4分の3")))
    if want:
        nb, na = _nums(before), _nums(after)
        ok = lambda got: all({m, m.rstrip("0").rstrip(".") if "." in m else m} & got for m in want)
        if ok(na) and not ok(nb):
            sig.append("数が直った")
    return sig


def verdict(val: str, before: str, after: str, text: str = "", key: str = ""):
    want = key_reading(val)
    if not want:
        return UNSURE, want, None, None
    rb, ub = reading(before)
    ra, ua = reading(after)
    inb = want in canon(rb) if not ub else None
    ina = want in canon(ra) if not ua else None
    if not inb and extra_signals(text, key, before, after):
        return ADOPT, want, inb, True
    # 🔴 順番が大事。「前にもう在る」なら**後を読めなくても見送り**と言い切れる
    #    （径間の後の聞取「三径間」は辞書に無くて読めないが、前の「三計観」が ケイカン だと分かれば足りる）。
    if inb is None:
        return UNSURE, want, inb, ina
    if inb:
        return SKIP, want, inb, ina
    if ina is None:
        return UNSURE, want, inb, ina
    return (ADOPT if ina else NOEFFECT), want, inb, ina


def collateral(text: str, before: str, after: str):
    """後の聞取にだけ出た食い違い＝巻き添えの疑い。"""
    _, _, _, db = compare(text, before)
    _, _, _, da = compare(text, after)
    return [d for d in da if d not in db]


# ── 対照（2026-09-08・キー橋の実測をそのまま使う）────────────────────────────
_CASES = [
    # (val, 前の聞取, 後の聞取, 期待, 台本, key)
    ("けいかん", "走路の上の三計観だけが", "高炉の上の三径間だけが", SKIP,
     "航路の上の3径間だけが、鋼のトラスで組まれていた。", "径間"),                  # 前も ケイカン
    ("そうだポンプ", "そしてソーダポンプ三台", "そしてそうだ、ポンプ三台", SKIP,
     "そして操舵ポンプ3台のうち2台である。", "操舵ポンプ"),                          # 前も ソオダポンプ
    ("みずさき人", "上級推薦人が", "上級みずさき人が", ADOPT,
     "上級水先人が、", "水先人"),                                                    # 前は スイセンニン
    ("ちからの道筋", "からの道筋から", "ちからの道筋から", ADOPT,
     "力の道筋から、支点そのものが抜けた。", "力の道筋"),
    # ① 字が直った型（janome が「右舷」を読めず、音では見つからない）
    ("うげん", "船首の尾栓が十七番橋脚に当たった。", "船首の右舷が十七番橋脚に当たった。", ADOPT,
     "船首の右舷が、17番橋脚に当たった。", "右舷"),
    # ② 数が直った型（reading は数を落とすので、音では永久に見つからない）
    ("サンジュウゴにん", "75人が亡くなった。", "35人が亡くなっ", ADOPT,
     "35人が亡くなった。", "35人"),
    ("ろくせんろっぴゃくボルト", "六百ボルトの高圧の母線", "六千六百ボルトの高圧の母線", ADOPT,
     "6600ボルトの高圧の母線、", "6600ボルト"),
]


def selftest() -> int:
    bad = []
    for val, b, a, want, text, key in _CASES:
        got = verdict(val, b, a, text, key)[0]
        if got != want:
            bad.append(f"「{val}」 期待 {want} → 出た {got}（前「{b}」／後「{a}」）")
    if bad:
        print("selftest 失敗:\n  " + "\n  ".join(bad))
        return 1
    print(f"selftest: {len(_CASES)}/{len(_CASES)} 合格（⚠️ 判定は当たり。最後は聞取の全文を読んで決める）")
    return 0


def main() -> int:
    ES.gate_args({"--selftest"}, paid=False)
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():
        return 1
    p = ES.qa_path("yomi_ab.tsv")
    if not p.exists():
        print(f"★{p} がありません（先に el_ab_yomi.py）", file=sys.stderr)
        return 2
    by = ES.by_id()
    rows, cnt = [], {}
    for l in p.read_text(encoding="utf-8").splitlines()[1:]:
        f = l.split("\t")
        if len(f) < 7:
            continue
        lid, key, val, _, _, before, after = f[:7]
        v, want, inb, ina = verdict(val, before, after, by[lid].text if lid in by else '', key)
        col = collateral(by[lid].text, before, after) if lid in by else []
        cnt[v] = cnt.get(v, 0) + 1
        rows.append((lid, key, val, v, want, col, before, after))
    out = ES.qa_path("ab_verdict.tsv")
    out.write_text("行\tkey\tval\t判定\t狙った音\t巻き添えの疑い\t前の聞取\t後の聞取\n" +
                   "\n".join(f"{a}\t{b}\t{c}\t{d}\t{e}\t{'／'.join(g)}\t{h}\t{i}"
                             for a, b, c, d, e, g, h, i in rows) + "\n", encoding="utf-8")
    for want in (ADOPT, NOEFFECT, UNSURE, SKIP):
        sel = [r for r in rows if r[3] == want]
        if not sel:
            continue
        print(f"\n=== {want}（{len(sel)}件）===")
        for lid, key, val, v, wnt, col, b, a in sel:
            print(f"  {lid:<8} 「{key}」→「{val}」  狙った音 {wnt}"
                  + (f"   ⚠️巻き添え {'／'.join(col)}" if col else ""))
            print(f"      前: {b}")
            print(f"      後: {a}")
    print(f"\n{len(rows)}件 {cnt} -> {out}")
    print("⚠️ 『採用』でも巻き添えの列が空でない候補は、入れる前に本文を読む")
    return 0


if __name__ == "__main__":
    sys.exit(main())
