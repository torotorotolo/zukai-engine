# -*- coding: utf-8 -*-
r"""el_check_heard.py — 文字起こし（el_yomi.tsv）を**一致率でない物差し**で洗う（2026-09-05 新設）。

  python tools/el_check_heard.py            … 3つの検査を全部
  python tools/el_check_heard.py --selftest

なぜ要るか（feedback-audio-yomi-zero・reference-elevenlabs-tts）:
  一致率は表記のゆれに引きずられ、意味が変わる誤読ほど埋もれる（ep009「275→175」は 98.3%）。
  数は check_numbers_heard が見る。ここは**それ以外**の、行を並べて聞くべき当たりを機械で出す:
   ① 同形異音語 … 台本にある 話・歳・方・間・日・人・上・下・目・生・表・家・物・事・角・一 ほかが、聞取に**同じ字で**現れていない行
                （Scribe は音から字を当てるので、読みが変わると字も変わる。「話です→わです」の型を字で捕まえる）
   ② 頭欠け     … 台本と聞取の**先頭1文字**が食い違う行（文頭の数字・1モーラ語が落ちる型。大半は表記違いなので当たりに留める）
   ③ 字の欠け   … 台本にある漢字で、聞取に1つも現れない字が**2字以上**ある行（語ごと落ちた・別語に化けた疑い）
  ⚠️ どれも当たり付け。0件でも誤読ゼロの証明ではない。出た行は el_probe_words（秒数）と el_take2（2テイク）で決める。

出力: audio/el_qa/<SLUG>_heard_flags.tsv（行 / 検査 / 何が / 台本 / 聞取）。1件でもあれば exit 1
"""
import re
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_numbers_heard import kan2int, KANNUM  # noqa: E402  漢数字→数（同じ物差しを2か所に持たない）

# 同形異音語＝読みが複数ある常用の字（ep034 で「話・歳」を漏らした反省＋この台本の語）
# ＋この台本で**意味を決める字**（方角・部位・材料）。1字でも聞取から消えたら当たりにする
#   （2026-09-05 実測：c504-1「北側」→聞取「西側」は一致率 95% で、字の欠け（2字以上）にも掛からなかった）
HOMOGRAPH = set("話歳方間日人上下目生表家物事角一門側量前後中段柱床"
                "北南東西左右塔板壁錆塩筋層面赤黄門隙")
KANJI_RE = re.compile(r"[一-鿿々]")
NUM_KANJI = set("〇一二三四五六七八九十百千万")


def _n(s):
    return unicodedata.normalize("NFKC", s)


def _lead_num(s):
    """先頭の数（算用でも漢数字でも）を int で。無ければ None。"""
    m = re.match(r"[0-9]+", s)
    if m:
        return int(m.group())
    m = re.match(f"[{KANNUM}]+", s)
    return kan2int(m.group()) if m else None


def check_row(text, heard):
    """1行ぶんの所見 [(検査, 何が)]。"""
    t, h = _n(text), _n(heard)
    flags = []
    # ① 同形異音語：台本の字が聞取に無い
    miss_h = sorted({c for c in t if c in HOMOGRAPH and c not in h})
    if miss_h:
        flags.append(("同形異音語", "".join(miss_h)))
    # ② 頭欠け：先頭が数なら**値**で比べる（36→6 の型。漢数字化は許す）。
    #    数でなければ先頭1文字を比べる。ただし漢字↔漢字は同音別字（群/郡）の可能性が高いので当てない
    #    （そちらは ①③ が見る）。捕まえたいのは 漢字/かな→別のかな（「走らせる→しらせる」の型）。
    ts = re.sub(r"^[「『（\s]+", "", t)
    hs = re.sub(r"^[「『（\s]+", "", h)
    if ts and hs:
        nt, nh = _lead_num(ts), _lead_num(hs)
        kana_num = re.match(r"(ひと|ふた|みっ|よっ|いつ|むっ|なな|やっ|ここの|とお)", ts)   # 「ひとつ」→聞取「一つ」は表記
        if nt is not None or nh is not None:
            if nt != nh and not (nt is None and kana_num):
                flags.append(("頭欠け", f"{nt}→{nh}"))
        else:
            a, b = ts[0], hs[0]
            hira = lambda c: chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c      # カナ→かな（ひ→ヒ は同じ音）
            a2, b2 = hira(a), hira(b)
            ka, kb = bool(KANJI_RE.match(a)), bool(KANJI_RE.match(b))
            # 当てるのは ①漢字→かな（読みが崩れて字にならない：崩→ス・瓦→グ） ②かな→別のかな。
            # 漢字→漢字（群/郡）と かな→漢字（あと→後・なか→中）は表記のゆれなので当てない
            if a2 != b2 and ((ka and not kb) or (not ka and not kb)):
                flags.append(("頭欠け", f"{a}→{b}"))
    # ③ 字の欠け：台本の漢字（数字の漢数字は除く）で聞取に無いものが2字以上
    miss_k = sorted({c for c in KANJI_RE.findall(t) if c not in h and c not in NUM_KANJI and c not in HOMOGRAPH})
    if len(miss_k) >= 2:
        flags.append(("字の欠け", "".join(miss_k)))
    return flags


def selftest() -> int:
    cases = [
        # ep034 の型：「話です」→「わです」＝聞取に「話」が無い
        ("これは、昔の話です。", "これは昔のわです。", {"同形異音語"}),
        # ep007 の型：文頭の数字が落ちる
        ("36人は、同じ8分間を過ごしました。", "六人は同じ八分間を過ごしました。", {"頭欠け"}),
        # 表記違いは当てない（漢数字化・句読点）
        ("2021年6月24日、午前1時22分ごろ。", "二〇二一年六月二十四日、午前一時二十二分ごろ。", set()),
        # 語ごと化けた：「積荷」→「罪人」（積・荷 が無い）
        ("船の積荷を調べた。", "船の罪人を調べた。", {"字の欠け"}),
        # 同音別字1字だけなら当てない（郡/群 の型）
        ("群を比べた。", "郡を比べた。", set()),
    ]
    bad = []
    for text, heard, want in cases:
        got = {k for k, _ in check_row(text, heard)}
        if got != want:
            bad.append(f"「{text}」／「{heard}」→ {got}（期待 {want}）")
    if bad:
        print("selftest 失敗:\n  " + "\n  ".join(bad))
        return 1
    print(f"selftest: {len(cases)}/{len(cases)} 合格")
    return 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():                      # 検査そのものが壊れていたら判定を出さない
        return 1
    import el_script as ES
    p = ES.qa_path("el_yomi.tsv")
    if not p.exists():
        print(f"★{p} がありません。先に el_check_yomi.py を回してください（fail closed）")
        return 2
    rows = [l.split("\t") for l in p.read_text(encoding="utf-8").splitlines()[1:] if l.strip()]
    out, counts = [], {}
    for f in rows:
        lid, text, heard = f[0], f[2], f[3]
        for kind, what in check_row(text, heard):
            counts[kind] = counts.get(kind, 0) + 1
            out.append(f"{lid}\t{kind}\t{what}\t{text}\t{heard}")
            print(f"{kind:<6} {lid:<8} {what:<8} 台本: {text}")
            print(f"{'':<24} 聞取: {heard}")
    op = ES.qa_path("heard_flags.tsv")
    op.write_text("行\t検査\t何が\t台本\t聞取\n" + "\n".join(out) + "\n", encoding="utf-8")
    print(f"\n検査 {len(rows)}行 → 所見 {len(out)}件 {counts} -> {op}")
    print("⚠️ 当たり付け。0件でも誤読ゼロの証明ではない")
    return 1 if out else 0


if __name__ == "__main__":
    sys.exit(main())
