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
    # 🔴 **stderr も**（2026-09-08）。Windows の標準エラーは cp932 のままなので、
    #    門番の「🔴 知らない引数」がそのまま文字化けして読めなかった（el_probe_words / el_artifact_words で実測）。
    #    ここは全部の el_*.py が import するので、1か所直せば全部に効く
    #    （reference-elevenlabs-tts の「ログへリダイレクトすると cp932 で落ちる」と同じ穴）。
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import narration  # noqa: E402  台本の正本

SLUG = "keybridge"          # 6本目 キー橋 崩落（2026-09-08）。5本目 "sl1"・4本目 "surfside"
# 🔴 話速 1.0 を**明示して送る**（2026-09-07 カズヤくん指示）。渡さないと声に保存された既定
#    speed 1.14 で読まれる。speed 以外の4つは /v1/voices/<id>/settings の実測をそのまま写した
#    （2026-09-07 に API で取り直し＝stability 0.85 / similarity_boost 1.0 / style 0.0 /
#     use_speaker_boost True）。部分的に送ると残りが API 既定に落ちるので**5つ全部**送る。
# ⚠️ 4本目の実測では「eleven_v3 は speed を無視する」（0.8/0.9/1.0/なしで 3.28〜3.60秒＝ばらつきの範囲）。
#    ⑤a の頭で1行 A/B して、効いたかどうかを実測で確かめる（効かなくても害は無い）。
# ⚠️ SETTINGS はキャッシュの鍵に入る＝途中で変えると全行が別物（＝全編もう一度課金）になる。
SETTINGS = {"stability": 0.85, "similarity_boost": 1.0, "style": 0.0,
            "speed": 1.0, "use_speaker_boost": True}
QA_DIR = ROOT / "audio" / "el_qa"

Line = namedtuple("Line", "lid cid idx text")

# 🔴 台本の実測値（カット／行／字）。**上流（narration.SCRIPT）を替えたらここも取り直す。**
#    門番は壊れず「黙って間違った合格」を出すので、回ごとに数を書き留めて selftest で突き合わせる
#    （feedback-gates-go-stale-when-upstream-changes）。出所＝check_script.py の集計。
#    quotes＝決め所（★）の数。clean() が ★ を外すので narration.SCRIPT からは数えられない＝ここに書く。
#    md＝台本の正本（Vault）。★の付いたカットIDを**そこから機械で取る**ためだけに使う。
EXPECT = {
    "surfside": {"cuts": 240, "lines": 486, "chars": 11027, "quotes": 12, "why": "サーフサイド 台本第3版",
                 "md": "事故検証-サーフサイド-台本第3版-20260905.md"},
    "sl1":      {"cuts": 212, "lines": 435, "chars": 10553, "quotes": 17, "why": "SL-1 台本第2版",
                 "md": "事故検証-SL1-台本第2版-20260907.md"},
    "keybridge": {"cuts": 216, "lines": 443, "chars": 11117, "quotes": 22, "why": "キー橋 台本第2版",
                  "md": "事故検証-キー橋-台本第2版-20260908.md"},
}
VAULT = Path.home() / "Documents" / "Obsidian Vault" / "Projects"


def quote_cuts():
    """決め所（★）の付いたカットIDの集合を**台本の md から**取る（2026-09-08 新設）。

    🔴 なぜ要るか: el_ledger.py はこれを `Q = {"c112", "c126", …}` と**4本目サーフサイドのIDで直書き**
       していた。カットIDは題材をまたいでぶつかる／ぶつからないので、回が替わると
       **黙って間違った秒**（要耳一覧の頭出し）を出す（feedback-gates-go-stale-when-upstream-changes）。
    fail closed: md が無い・★の数が EXPECT と食い違うときは例外で止める（0 で埋めない）。
    """
    import check_script as CSC
    p = VAULT / EXPECT[SLUG]["md"]
    if not p.exists():
        raise SystemExit(f"🔴 台本の md が無い: {p}（el_script.EXPECT[{SLUG!r}]['md']）")
    cuts = CSC.parse(p.read_text(encoding="utf-8"))
    q = {cid for cid, _, ls in cuts if any(CSC.STAR_RE.match(l) for l in ls)}
    want = EXPECT[SLUG]["quotes"]
    if len(q) != want:
        raise SystemExit(f"🔴 決め所の数が食い違う: md {len(q)} ／ EXPECT {want}（上流を替えたら定数を取り直す）")
    return q


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


def gate_args(known, paid=True):
    """🔴 知らない `--` 引数で本番に落ちない（fail closed）。**有料の道具には必ず付ける。**

    2026-09-08 に実際に踏んだ事故: `el_check_yomi.py --selftest`（この道具に無い旗）を付けたら、
    警告も出さずに 443行の Scribe が走り出し、止めるまでに 433クレジット（約$0.07）を捨てた。
    「無い旗は無視して本番」は fail open（feedback-parsers-fail-closed／feedback-rules-need-gates）。
    ⚠️ 物差しを2か所に持たないため、各道具は自前で書かずにこれを呼ぶこと。
    """
    known = set(known)
    unknown = [a for a in sys.argv[1:] if a.startswith("--") and a.split("=")[0] not in known]
    if unknown:
        raise SystemExit(f"🔴 知らない引数: {unknown}（使えるのは {sorted(known)} だけ）"
                         + ("\n   ⚠️ この道具は**走らせると課金されます**。旗を確かめてから呼び直してください。"
                            if paid else ""))


_NO = object()


def cache_path(sent, settings=_NO):
    """その送信文の合成キャッシュ（pcm）の場所。鍵は el_tts と同じ関数で作る。

    🔴 ここに入っているのは **atempo（el_build.TEMPO）を掛ける**前の pcm です。
       出荷する音は el_build.retempo() を通ったあとの音なので、**検査は必ず retempo を通すこと**
       （feedback-checks-read-cached-narration＝検査はキャッシュを読む）。
       ＝ 鍵に TEMPO を入れない代わりに、読み出す側が全員 retempo する約束です。
    """
    import el_tts
    st = SETTINGS if settings is _NO else settings
    return el_tts._cache_dir(SLUG) / f"{el_tts._cache_key(sent, st)}.pcm"


def shipped(pcm: bytes) -> bytes:
    """**出荷する音**（＝動画に入る音）にそろえる。cache_path の pcm はこれを通してから測る。

    2026-09-08・6本目キー橋で `el_build.TEMPO = 1.05`（合成後の atempo）が入ったため、
    キャッシュの pcm と出荷音は**別物**になった。el_check_yomi 以外の検査は
    キャッシュを素で読んでいた＝「動画に入っていない音」を検査していた。
    ⚠️ TEMPO が 1.0 の回（5本目まで）は素通り＝1バイトも変わらない。
    """
    import el_build
    return el_build.retempo(pcm)


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


# ── EL_YOMI（6本目 キー橋）─────────────────────────────────────────
# 🔴 **空から始める。** 台本第2版 §6 の「怪しい語」は**怪しいだけ**で、読みの正解は入っていない。
#    1語ずつ鳴らして（el_probe_words / el_ab_yomi）確かめた語だけ、根拠を1行添えて足す
#    （feedback-yomi-dict-must-be-verified＝辞書が誤ると検査は全段素通りする）。
# ⚠️ 5本目 SL-1 の13件は**引き継がない**。短いキーの一括置換は、登録した回では正しくても
#    別の回の別の文脈で誤読を作る。旧辞書が要るときは git の 560f626（tools/el_script.py）から読む。
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
    e = EXPECT[SLUG]
    why = e["why"]
    print(f"台本: {n_cuts}カット／{len(ls)}行／{n_chars}字（{why} の実測は "
          f"{e['cuts']}／{e['lines']}／{e['chars']:,}・決め所 {e['quotes']}）")
    ok = (n_cuts, len(ls), n_chars) == (e["cuts"], e["lines"], e["chars"])
    print("  " + (f"✓ {why}と一致" if ok else f"🔴 {why}と食い違う"))
    # 🔴 pr01 の行数は回によって違う（サーフサイド3行・SL-1 2行）ので、台本から作った答えと突き合わせる
    r = resolve_ids("pr01,c101-2")
    want2 = [l.lid for l in ls if l.cid == "pr01"] + ["c101-2"]
    print(f"resolve_ids('pr01,c101-2') → {r}")
    ok2 = r == want2
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
    ok4 = _gate_shipped()
    ok5 = _gate_args_selftest()
    return 0 if (ok and ok2 and ok3 and ok4 and ok5) else 1


# ── 🔴 門番: 「検査が出荷する音を見ているか」を**機械で**確かめる（2026-09-08 新設）─────────
#    なぜ要るか: TEMPO（合成後の atempo）が入った日、el_check_yomi だけが直され、ほかの7本は
#    キャッシュ（atempo 前）を素で読んだままだった＝**出荷しない音を検査していた**。
#    規則を書いたら門番も足す（feedback-rules-need-gates）。次に道具を1本足したときにここが鳴る。
_PCM_EXEMPT = {
    "el_build.py": "本番の組み立て。retempo() の定義元＝ここが素で読むのが正しい",
    "el_tts.py": "キャッシュ層。保存するのは素の pcm（鍵に TEMPO を入れない約束）",
    "el_script.py": "この file 自身（shipped() の定義元）",
    "el_speed_probe.py": "API の speed が効くかを測る道具。**素の合成**を測るのが目的",
}


def _gate_shipped() -> bool:
    """合成 pcm を触る el_*.py は、全部 ES.shipped() を通していること（例外は _PCM_EXEMPT）。"""
    d = Path(__file__).resolve().parent
    bad = []
    for f in sorted(d.glob("el_*.py")):
        src = f.read_text(encoding="utf-8")
        if "cache_path(" not in src and "el_tts.synth(" not in src:
            continue
        if f.name in _PCM_EXEMPT:
            continue
        if "shipped(" not in src:
            bad.append(f.name)
    # 陽性対照＝shipped が本当に長さを変える（TEMPO 1.0 の回は素通りが正しいので、そのときは飛ばす）
    import el_build
    n = 24000 * 2 * 2                      # 2秒ぶんの無音
    got = len(shipped(b"\x00\x00" * (n // 2)))
    if abs(el_build.TEMPO - 1.0) > 1e-9:
        r = n / max(got, 1)
        if not (el_build.TEMPO * 0.97 <= r <= el_build.TEMPO * 1.03):
            bad.append(f"陽性対照: shipped() が縮めていない（比 {r:.3f}／TEMPO {el_build.TEMPO}）")
    elif got != n:
        bad.append("陽性対照: TEMPO 1.0 なのに shipped() が音を変えた")
    print("  " + ("✓ 検査は出荷する音（atempo 後）を見ている"
                  if not bad else f"🔴 出荷しない音を見ている／対照が落ちた: {bad}"))
    return not bad


def _gate_args_selftest() -> bool:
    """gate_args が知らない旗で止まり、知っている旗では止まらないこと（陰性対照つき）。"""
    import sys as _s
    keep = _s.argv
    bad = []
    try:
        _s.argv = ["x", "--ids", "c101", "--worst", "5"]
        gate_args({"--ids", "--worst"})            # 止まってはいけない
        for argv in (["x", "--selftest"], ["x", "--ids", "c101", "--dry"]):
            _s.argv = argv
            try:
                gate_args({"--ids", "--worst"})
                bad.append(f"知らない旗が素通りした: {argv[1:]}")
            except SystemExit:
                pass
    except SystemExit as e:
        bad.append(f"正しい旗で止まった: {e}")
    finally:
        _s.argv = keep
    print("  " + ("✓ 知らない引数で止まる（有料の道具 6本に設置）" if not bad else f"🔴 {bad}"))
    return not bad


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
