# -*- coding: utf-8 -*-
r"""el_reading_diff.py — 台本と聞取を「**読み（音）**」で突き合わせ、Scribe の字の当て違いと本物の誤読を分ける。

  python tools/el_reading_diff.py              … 所見のある行（heard_flags.tsv）を仕分ける
  python tools/el_reading_diff.py --all        … 全443行
  python tools/el_reading_diff.py --selftest   … 陽性・陰性対照（API 不使用・無料）

🔴 なぜ要るか（2026-09-08・6本目キー橋 ⑤a）:
    el_check_heard の所見が **165行**出た。ところが中身の多くは
    「遮断器→遮断機」「既設→季節」「航海→後悔」「操舵→ソーダ」「径間→警官」のように
    **読みは同じで字だけが違う**もの＝Scribe が音から字を当てそこねただけで、音は正しい。
    一方「指針→地震」「水先人→推薦人」「補修班→保守班」「35人→75人」は**読みそのものが違う**＝本物の疑い。
    字で見ているかぎりこの2つは混ざる。**読みに直してから比べれば機械で分けられる。**

⚠️⚠️ これは**門番ではありません。仕分けの道具です。**
    - janome（形態素解析器）の読みは**辞書に無い専門語で外れる**（径間・防衝工・端子台など）。
      辞書に無い語は字ごとに切られて音読みが当てられるので、**当たっていても偶然のことがある**。
    - したがって「読みが一致した」は **“ほぼ表記のゆれ”という当たり**であって、合格証ではない。
      決めるのは取り直し（el_retake）・A/B（el_ab_yomi）・語の時刻（el_probe_words）。
    - 「読みが違う」側は**取りこぼしが少ない**（本物はほぼ全部ここに来る）。まずこちらから潰す。

出力: audio/el_qa/<SLUG>_reading_diff.tsv（行 / 判定 / 台本の読み / 聞取の読み / 台本 / 聞取）
"""
import difflib
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_script as ES  # noqa: E402  ★stdout/stderr の utf-8 化もここで効く

_TOK = None


def tokenizer():
    global _TOK
    if _TOK is None:
        from janome.tokenizer import Tokenizer
        _TOK = Tokenizer()
    return _TOK


KATA = str.maketrans({chr(c): chr(c + 0x60) for c in range(0x3041, 0x3097)})   # ひら→カタ


def reading(text: str):
    """文を (カタカナの読み, 読みが取れなかった語) にする。

    🔴 **数（名詞,数）は落とす。** 台本は「1500」、聞取は「千五百」と書かれるので、
       読みのまま比べると全部が食い違う。数は check_numbers_heard が別に見ている（同じ物差しを2つ持たない）。
    ⚠️ **辞書に無い語（径間・防衝工・端子台…）は読みを返さない。** そのときは第2の戻り値に積み、
       その行は「判定できない」に落とす（推測で埋めない＝fail closed）。
    """
    out, unknown = [], []
    for t in tokenizer().tokenize(text):
        if t.part_of_speech.startswith("名詞,数"):
            continue
        r = t.reading
        if r == "*":
            if re.search(r"[一-鿿々]", t.surface):     # 漢字なのに読みが無い＝辞書に無い語
                unknown.append(t.surface)
                continue
            out.append(t.surface.translate(KATA))
        else:
            out.append(r)
    return "".join(out), unknown


_VOW = {"ア": "ア", "カ": "ア", "サ": "ア", "タ": "ア", "ナ": "ア", "ハ": "ア", "マ": "ア", "ヤ": "ア", "ラ": "ア",
        "ワ": "ア", "ガ": "ア", "ザ": "ア", "ダ": "ア", "バ": "ア", "パ": "ア", "ャ": "ア",
        "イ": "イ", "キ": "イ", "シ": "イ", "チ": "イ", "ニ": "イ", "ヒ": "イ", "ミ": "イ", "リ": "イ",
        "ギ": "イ", "ジ": "イ", "ヂ": "イ", "ビ": "イ", "ピ": "イ",
        "ウ": "ウ", "ク": "ウ", "ス": "ウ", "ツ": "ウ", "ヌ": "ウ", "フ": "ウ", "ム": "ウ", "ユ": "ウ", "ル": "ウ",
        "グ": "ウ", "ズ": "ウ", "ヅ": "ウ", "ブ": "ウ", "プ": "ウ", "ュ": "ウ",
        "エ": "エ", "ケ": "エ", "セ": "エ", "テ": "エ", "ネ": "エ", "ヘ": "エ", "メ": "エ", "レ": "エ",
        "ゲ": "エ", "ゼ": "エ", "デ": "エ", "ベ": "エ", "ペ": "エ",
        "オ": "オ", "コ": "オ", "ソ": "オ", "ト": "オ", "ノ": "オ", "ホ": "オ", "モ": "オ", "ヨ": "オ", "ロ": "オ",
        "ゴ": "オ", "ゾ": "オ", "ド": "オ", "ボ": "オ", "ポ": "オ", "ョ": "オ"}


def canon(kana: str) -> str:
    """読みを比べるための正規化。**長音の書き方の違いだけ**を吸収する（音は変えない）。
      ソーダ ⇄ ソウダ ⇄ ソオダ／ケイカン ⇄ ケーカン／ジュウ ⇄ ジュー
    ⚠️ ここを凝りすぎると本物の誤読まで吸収する。やるのは長音と記号だけ。"""
    s = unicodedata.normalize("NFKC", kana)
    s = re.sub(r"[^ァ-ヺーッ]", "", s)          # 記号・数字・アルファベットは落とす（数は別の検査が見る）
    out = []
    for ch in s:
        if ch == "ー" and out:
            out.append(_VOW.get(out[-1], "ー"))
            continue
        out.append(ch)
    s = "".join(out)
    s = re.sub(r"([コソトノホモヨロゴゾドボポョオ])ウ", r"\1オ", s)      # オ段＋ウ → 長音
    s = re.sub(r"([ケセテネヘメレゲゼデベペエ])イ", r"\1エ", s)          # エ段＋イ → 長音
    return s


MATCH, DIFFER, UNKNOWN = "読み一致", "読みが違う", "判定できない"

# 数の読み。⚠️ 台本「1時27分」の 1 は 名詞,数 で落ちるのに、聞取「一時」は janome が
#    〈一時＝イチジ〉と1語で採るので落ちない＝「—→イチ」という**数だけの食い違い**が量産される。
#    数そのものは check_numbers_heard が見ているので、**両側とも数の読みだけの食い違いは無視する**。
#    ⚠️ 片側にでも数でない音が混じっていたら無視しない（「ニ→カ」＝積荷→住処 は残す）。
_NUMW = ("イチ|ニ|サン|ヨン|シチ|ゴ|ロク|ナナ|ハチ|キュウ|ジュウ|ジュッ|ジッ|ヒャク|ビャク|ピャク|"
         "セン|ゼン|マン|オク|レイ|ゼロ|ヒト|フタ|ミッ|ヨッ|イツ|ムッ|ヤッ|ココノ|トオ|ジ|ップ")
_NUM_ONLY = re.compile(f"^(?:{_NUMW})+$")


def _numeric_noise(a: str, b: str) -> bool:
    """食い違いの両側が「空」か「数の読みだけ」なら、数の表記違いとして無視してよい。"""
    return all(x == "" or _NUM_ONLY.match(x) for x in (a, b))


def compare(text: str, heard: str):
    """(判定, 台本の読み, 聞取の読み, 食い違った所／辞書に無い語) を返す。

    判定は3つ。**「読み一致」以外を2つに分けるのが肝**で、辞書に無い専門語を
    「読みが違う」に混ぜると、本物の誤読がその中に埋もれる（この回は径間23行・端子台3行…）。
    """
    ra, ua = reading(text)
    rb, ub = reading(heard)
    a, b = canon(ra), canon(rb)
    if ua or ub:
        return UNKNOWN, a, b, sorted(set(ua) | set(ub))
    if a == b:
        return MATCH, a, b, []
    diff = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag == "equal" or _numeric_noise(a[i1:i2], b[j1:j2]):
            continue
        diff.append(f"{a[i1:i2] or '—'}→{b[j1:j2] or '—'}")
    return (DIFFER, a, b, diff) if diff else (MATCH, a, b, [])


# ── 対照（2026-09-08・6本目キー橋の実データから取った）────────────────────────
# 陽性＝**本物の疑い**（読みが違う）。陰性＝**Scribe の字の当て違い**（読みは同じ）。
_POS = [("2009年の指針の計算、方法2は", "二〇〇九年の地震の計算方法には"),      # ししん→じしん
        ("上級水先人と", "上級推薦人と"),                                        # みずさきにん→すいせんにん
        ("亡くなった補修班6人", "亡くなった保守派6人"),                          # ほしゅうはん→ほしゅは
        ("点検員は、橋を歩いて渡っていた。", "弁慶院は橋を歩いて渡っていた。"),   # てんけんいん→べんけいいん
        ("端子台は、船に数千個あった", "唐時代は船に数千個あった")]               # たんしだい→とうじだい
_NEG = [("この遮断器には", "この遮断機には"),                                    # しゃだんき（同じ）
        ("協会は、既設の橋についても", "協会は季節の橋についても"),              # きせつ（同じ）
        ("航海データ記録装置への勧告である。", "後悔データ記録装置への勧告である。"),  # こうかい（同じ）
        ("操舵ポンプ3台が全部止まった。", "ソーダポンプ三台が全部止まった。"),   # そうだ／ソーダ（長音の書き方）
        ("1時28分10秒、船首が泥に乗り上げはじめる。",
         "一時二十八分十秒。船首が泥に乗り上げ始める。"),                        # 数の表記だけの違い
        ("中央の橋桁3つが川へ落ちた。", "中央の橋桁三つが川へ落ちた。")]         # 3つ／三つ
# 判定できない＝辞書に無い専門語がある行。**「読みが違う」に混ぜてはいけない**
# （混ぜると本物がその中に埋もれる。この回は径間23行・端子台3行・防衝工…）
_UNK = [("崩れなかった径間のうち", "崩れなかった警官のうち"),                     # 「径間」が辞書に無い
        ("防衝工は壊れたが", "道承公は壊れたが")]                                 # 「防衝工」が辞書に無い
# ⚠️ **この道具が誤って鳴る型（既知）**＝janome の辞書上の読みが台本と聞取で違う字。
#    実例「橋まで」ハシ ／「端まで」ハ**ジ**＝音は同じ「はし」なのに『読みが違う』側に落ちる。
#    濁点1つの差は「指針→地震」のような**本物**でもあるので、ここを均すことはできない。
#    ＝ 誤って鳴るのは**安全な向き**（高い検査へ回るだけ）。0件を目標にしない。
_KNOWN_FALSE = [("橋まで1500フィート。", "端まで千五百フィート。")]


def selftest() -> int:
    bad = []
    for want, cases, name in ((DIFFER, _POS, "陽性"), (MATCH, _NEG, "陰性"), (UNKNOWN, _UNK, "判定不能")):
        for t, h in cases:
            got, a, b, d = compare(t, h)
            if got != want:
                bad.append(f"[{name}] 期待「{want}」→ 出た「{got}」: 「{t}」／「{h}」 {d}")
    # 既知の誤報が「まだ誤報のまま」であることも見る（黙って直っていたら物差しが変わった合図）
    for t, h in _KNOWN_FALSE:
        if compare(t, h)[0] != DIFFER:
            print(f"  ⚠️ 既知の誤報が鳴らなくなった（物差しが変わった？）: 「{t}」／「{h}」")
    if bad:
        print("selftest 失敗:\n  " + "\n  ".join(bad))
        return 1
    print(f"selftest: 陽性 {len(_POS)}件・陰性 {len(_NEG)}件・判定不能 {len(_UNK)}件 合格"
          "（⚠️ 合格しても『読み一致＝正しい』ではない。当たりの仕分けに使う道具）")
    return 0


def main() -> int:
    ES.gate_args({"--all", "--selftest"}, paid=False)
    if "--selftest" in sys.argv:
        return selftest()
    if selftest():                       # 物差しが壊れていたら仕分けを出さない（fail closed）
        return 1
    from el_check_yomi import load_tsv
    yomi = load_tsv(ES.qa_path("el_yomi.tsv"))
    if not yomi:
        print("★ el_yomi.tsv がありません。先に el_check_yomi.py を回してください", file=sys.stderr)
        return 2
    fl = ES.qa_path("heard_flags.tsv")
    flagged = {}
    if fl.exists():
        for l in fl.read_text(encoding="utf-8").splitlines()[1:]:
            f = l.split("\t")
            if len(f) >= 3:
                flagged.setdefault(f[0], []).append(f"{f[1]}:{f[2]}")
    targets = [l.lid for l in ES.lines()] if "--all" in sys.argv else \
              [l.lid for l in ES.lines() if l.lid in flagged]
    rows, cnt = [], {MATCH: 0, DIFFER: 0, UNKNOWN: 0}
    for lid in targets:
        if lid not in yomi:
            continue
        text, heard = yomi[lid][0], yomi[lid][1]
        v, a, b, d = compare(text, heard)
        cnt[v] += 1
        rows.append((lid, v, a, b, d, text, heard))
    out = ES.qa_path("reading_diff.tsv")
    out.write_text("行\t判定\t食い違い\t台本の読み\t聞取の読み\t台本\t聞取\n" +
                   "\n".join(f"{i}\t{v}\t{'／'.join(d)}\t{a}\t{b}\t{t}\t{h}"
                             for i, v, a, b, d, t, h in rows) + "\n", encoding="utf-8")
    for want, mark in ((DIFFER, "🔴"), (UNKNOWN, "⚠️")):
        print(f"\n=== {mark} {want}（{cnt[want]}行）===")
        for lid, v, a, b, d, text, heard in rows:
            if v != want:
                continue
            print(f"{mark} {lid}  {'／'.join(d)}   [{'／'.join(flagged.get(lid, [])) or '所見なし'}]")
            print(f"   台本: {text}")
            print(f"   聞取: {heard}")
    print(f"\n仕分け {len(rows)}行 → 読みが違う {cnt[DIFFER]}／判定できない {cnt[UNKNOWN]}／読み一致 {cnt[MATCH]}"
          f" -> {out}")
    print("⚠️ 『読み一致』は“ほぼ表記のゆれ”という当たり。合格証ではない（janome の読みは専門語で外れる）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
