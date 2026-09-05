# -*- coding: utf-8 -*-
r"""el_script.py — ElevenLabs 経路の共通部（4本目サーフサイドから。2026-09-05 新設）。

台本の正本は `tools/narration.py` の SCRIPT（カットID → 字幕行）。**ElevenLabs は行ごとに合成する。**
心理chの道具は `config/<slug>.json` の scenes を読んでいたので、ここで「行」に読み替える。

  ここが持つもの:
    SLUG          … 題材の名前。合成キャッシュ audio/el_cache/<SLUG>/・検査の記録 audio/el_qa/<SLUG>_*.tsv
    SETTINGS      … voice_settings。None＝渡さない（既定の音）。キャッシュの鍵に入るので途中で変えない
    lines()       … Line(lid, cid, idx, text) を SCRIPT の順に。行ID＝"c101-2"（カットID-行番号）
    resolve_ids() … --ids の "c101,c102-1" を行IDに広げる。無いIDは止まる（fail closed）
    EL_YOMI       … ElevenLabs へ渡す文字列の読み替え。**字幕（SCRIPT）は変えない**
    el_text()     … 実際にエンジンへ送る文字列。**本番も検査も必ずこれを通す**（鍵がずれると直した行だけ検査から漏れる）

  python tools/el_script.py --selftest … 境界規則と行の列挙の検算（API 不使用）
  python tools/el_script.py --hits     … EL_YOMI がどの行に当たるかの棚卸し（feedback-yomi-dict-must-be-verified）

🔴 EL_YOMI の作法（reference-elevenlabs-tts）:
  - 類推で書かない。1語ずつ実際に鳴らして Scribe と A/B（tools/el_ab_yomi.py）で確かめてから入れる
  - かな書き＝正解とは限らない（「積荷」は かな も カナ も罪人。「積み荷」だけ通った）
  - 正しく読めている語をかな化しない（アクセントが壊れる）。キーは**その行だけに当たる長さ**で
  - 文頭の数字はカナで固定（"36人は": "サンジュウロクニンは"）／アクセント句は半角空白で切る（"いま動かせる": "いま 動かせる"）
  - 読点は足さない（ElevenLabs では読点が実際の「間」になる）／重複読みは句点のあとに半角空白
  - 🔴 キーは台本の実文に当たること。当たらないキーは import 時の門番が止める（黙って素通りさせない）
"""
import re
import sys
from collections import namedtuple
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import narration  # noqa: E402  台本の正本

SLUG = "surfside"
SETTINGS = None
QA_DIR = ROOT / "audio" / "el_qa"

Line = namedtuple("Line", "lid cid idx text")


def lines():
    out = []
    for cid, ls in narration.SCRIPT:
        for i, t in enumerate(ls, 1):
            out.append(Line(f"{cid}-{i}", cid, i, t.strip()))
    return out


def by_id():
    return {l.lid: l for l in lines()}


def resolve_ids(spec):
    """"c101,c102-1" → 行IDの一覧。カットIDなら全行。無いIDは ValueError（fail closed）。"""
    if not spec:
        return []
    all_ = lines()
    lids = {l.lid for l in all_}
    cids = {l.cid for l in all_}
    out = []
    for s in [x.strip() for x in spec.split(",") if x.strip()]:
        if s in lids:
            out.append(s)
        elif s in cids:
            out += [l.lid for l in all_ if l.cid == s]
        else:
            raise ValueError(f"台本に無いID: {s}")
    return out


def qa_path(name):
    QA_DIR.mkdir(parents=True, exist_ok=True)
    return QA_DIR / f"{SLUG}_{name}"


_NO = object()


def cache_path(sent, settings=_NO):
    """その送信文の合成キャッシュ（pcm）の場所。鍵は el_tts と同じ関数で作る。"""
    import el_tts
    st = SETTINGS if settings is _NO else settings
    return el_tts._cache_dir(SLUG) / f"{el_tts._cache_key(sent, st)}.pcm"


# ── 置換の境界（心理ch gen_audio.py から写した。2026-08-26 の事故15件を防ぐ規則） ──────
# ★文字クラスは \u 表記で書く（漢字そのものを並べると、編集で範囲記号「-」が壊れても気づけない）
_KANJI = "々一-鿿㐀-䶿豈-﫿"   # 々 + CJK統合漢字 + 拡張A + 互換漢字
_DIGIT = "0-9０-９"                               # 半角数字 + 全角数字


def _is_kanji(ch: str) -> bool:
    o = ord(ch)
    return (ch == "々" or 0x4E00 <= o <= 0x9FFF
            or 0x3400 <= o <= 0x4DBF or 0xF900 <= o <= 0xFAFF)


def yomi_pattern(key: str, open_left: bool = False, open_right: bool = False):
    """キーの端の文字種から「複合語・長い数の内部には当たらない」正規表現を作る。
    数字で始まるキーは直前が数字（や小数点）なら当てない／漢字で終わるキーは直後が漢字なら当てない。
    open_left / open_right を立てた側だけ、境界なしで当てる。"""
    pre = post = ""
    head, tail = key[0], key[-1]
    if head.isdigit() or head == ".":
        pre = f"(?<![{_DIGIT}.．])"
    elif _is_kanji(head) and not open_left:
        pre = f"(?<![{_KANJI}])"
    if tail.isdigit():
        post = f"(?![{_DIGIT}])(?![.．][{_DIGIT}])"
    elif _is_kanji(tail) and not open_right:
        post = f"(?![{_KANJI}])"
    # ★re.escape は必須（"0.34" の "." が任意の1文字になり「0で34」にまで当たる）
    return re.compile(pre + re.escape(key) + post)


def _compile_yomi(rules: dict, open_right=frozenset(), open_left=frozenset()):
    order = sorted(rules, key=len, reverse=True)
    return order, {k: yomi_pattern(k, k in open_left, k in open_right) for k in order}


def apply_yomi(text: str, order, patterns, rules, hits=None) -> str:
    """読み替えを長い語から順に当てる。hits にリストを渡すと (キー, 値, 当たった回数) が記録される。"""
    for a in order:
        if hits is None:
            text = patterns[a].sub(lambda m, _v=rules[a]: _v, text)
        else:
            text, n = patterns[a].subn(lambda m, _v=rules[a]: _v, text)
            if n:
                hits.append((a, rules[a], n))
    return text


# ── EL_YOMI（サーフサイド）─────────────────────────────────────────
# ⚠️ 空から始める。台本第3版 §6-1 の「怪しい語」は**怪しいだけ**で、読みの正解はまだ入っていない。
#    1語ずつ鳴らして（el_ab_yomi / el_probe_words）確かめた語だけ、根拠を1行添えて足す。
EL_YOMI = {
}
EL_YOMI_OPEN_RIGHT = frozenset()
EL_YOMI_OPEN_LEFT = frozenset()
EL_YOMI_ORDER, EL_YOMI_RE = _compile_yomi(EL_YOMI, EL_YOMI_OPEN_RIGHT, EL_YOMI_OPEN_LEFT)


def el_text(text: str, hits=None) -> str:
    """ElevenLabs へ実際に送る文字列（本番と検査で同じ関数）。読点・句点は足さない。"""
    return apply_yomi(text, EL_YOMI_ORDER, EL_YOMI_RE, EL_YOMI, hits)


# ── 門番（import しただけで必ず走る・fail closed）────────────────────────
# ① 境界規則そのものの検算（心理chで実測した事故と、直しすぎを両側から）
_T_RULES = {"話は": "ハナシは", "話です": "ハナシです", "二人": "ふたり", "3年前": "さんねんまえ",
            "1件": "いっけん", "0.34": "れいてんさんよん", "1500人": "せんごひゃくにん", "数百": "すうひゃく"}
_T_ORDER, _T_RE = _compile_yomi(_T_RULES, open_right=frozenset({"数百"}))
_T_MUSTNOT = [("電話は長かった", "電話は長かった"), ("十二人の陪審員", "十二人の陪審員"),
              ("13年前の話です", "13年前のハナシです"), ("21件の報告", "21件の報告"),
              ("相関は10.34だった", "相関は10.34だった"), ("11500人が答えた", "11500人が答えた"),
              ("数百社をこえる", "すうひゃく社をこえる")]
_T_MUST = [("ここから、話は", "ここから、ハナシは"), ("二人が拾っている", "ふたりが拾っている"),
           ("3年前の話です", "さんねんまえのハナシです"), ("1件あたりの時間", "いっけんあたりの時間"),
           ("相関は0.34だった", "相関はれいてんさんよんだった"), ("1500人が答えた", "せんごひゃくにんが答えた"),
           ("数百人が集まった", "すうひゃく人が集まった")]


def _gate():
    bad = []
    for src, want in _T_MUSTNOT + _T_MUST:
        got = apply_yomi(src, _T_ORDER, _T_RE, _T_RULES)
        if got != want:
            bad.append(f"境界規則: 「{src}」→「{got}」（期待「{want}」）")
    # ② EL_YOMI の各キーは台本の実文に少なくとも1行当たる（当たらないキー＝書き損じ＝黙って素通り）
    ls = lines()
    for k in EL_YOMI:
        if not any(EL_YOMI_RE[k].search(l.text) for l in ls):
            bad.append(f"EL_YOMI のキー「{k}」は台本のどの行にも当たらない")
    # ③ 値に読点を足していないか（ElevenLabs では読点が実際の間になる）
    for k, v in EL_YOMI.items():
        if v.count("、") > k.count("、"):
            bad.append(f"EL_YOMI「{k}」の値に読点を足している（台本に無い間が入る）")
    # ④ 行IDの一意性
    lids = [l.lid for l in ls]
    if len(lids) != len(set(lids)):
        bad.append("行IDが重複している")
    if bad:
        raise RuntimeError("★el_script の門番が落ちた（本番も検査も止める）:\n  " + "\n  ".join(bad))


_gate()


def selftest() -> int:
    ls = lines()
    n_cuts = len(narration.SCRIPT)
    n_chars = sum(len(l.text) for l in ls)
    print(f"台本: {n_cuts}カット／{len(ls)}行／{n_chars}字（第3版の実測は 240／486／11,027）")
    ok = (n_cuts, len(ls), n_chars) == (240, 486, 11027)
    print("  " + ("✓ 第3版と一致" if ok else "🔴 第3版と食い違う"))
    r = resolve_ids("pr01,c101-2")
    print(f"resolve_ids('pr01,c101-2') → {r}")
    ok2 = r == ["pr01-1", "pr01-2", "pr01-3", "c101-2"]
    try:
        resolve_ids("zz99")
        ok3 = False
    except ValueError:
        ok3 = True
    print("  " + ("✓ 無いIDで止まる" if ok3 else "🔴 無いIDが素通り"))
    hits = []
    changed = sum(1 for l in ls if el_text(l.text, hits) != l.text)
    print(f"EL_YOMI: {len(EL_YOMI)}件 → 当たった行 {changed}／{len(ls)}")
    print(f"門番: 境界規則 {len(_T_MUSTNOT)+len(_T_MUST)}件 ✓（import 時に通過ずみ）")
    return 0 if (ok and ok2 and ok3) else 1


def show_hits() -> int:
    """棚卸し：どのキーがどの行に当たり、送信文がどう変わるか。"""
    n = 0
    for l in lines():
        hits = []
        sent = el_text(l.text, hits)
        if hits:
            n += 1
            print(f"{l.lid}  {', '.join(f'{k}→{v}×{c}' for k, v, c in hits)}")
            print(f"     台本: {l.text}")
            print(f"     送信: {sent}")
    print(f"\nEL_YOMI {len(EL_YOMI)}件 が当たる行: {n}")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--hits" in sys.argv:
        sys.exit(show_hits())
    print(__doc__)
