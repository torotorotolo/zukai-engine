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

SLUG = "sl1"                # 5本目 SL-1 原子炉暴走事故（2026-09-07）。4本目は "surfside"
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
EXPECT = {
    "surfside": {"cuts": 240, "lines": 486, "chars": 11027, "quotes": 12, "why": "サーフサイド 台本第3版"},
    "sl1":      {"cuts": 212, "lines": 435, "chars": 10553, "quotes": 17, "why": "SL-1 台本第2版"},
}


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


# ── EL_YOMI（5本目 SL-1）───────────────────────────────────────────
# 🔴 **空から始める。** 台本第2版 §6 の「怪しい語」は**怪しいだけ**で、読みの正解は入っていない。
#    1語ずつ鳴らして（el_probe_words / el_ab_yomi）確かめた語だけ、根拠を1行添えて足す
#    （feedback-yomi-dict-must-be-verified＝辞書が誤ると検査は全段素通りする）。
# ⚠️ 4本目サーフサイドの21件は**引き継がない**。短いキーの一括置換は、登録した回では正しくても
#    別の回の別の文脈で誤読を作る（心理ch ep002 で11件中3件が辞書由来だった）。
#    旧辞書が要るときは git の a004666（tools/el_script.py）から読む。
EL_YOMI = {
    # ---- 2026-09-07 ⑤a：全435行 Scribe → 数の検査 → 字の検査 → 取り直し53行 → A/B 15件 で確かめた7件 ----
    # 🔴 採否は**一致率で決めていない**（feedback-audio-yomi-zero）。「聞取の中身が台本に寄ったか」で決めた。
    #
    # 「建屋」（10行）。**文頭・句点直後の3行だけ**が「手／手矢／手や」＝頭の「た」が落ちる。
    #    文中の建屋（c710-1）は聞取「タテヤ」＝正しく読めているので触らない（かな化はアクセントを壊す）。
    #    キーは**その行にだけ当たる長さ**にした（「建屋から」は c710-1・c805-1 にも当たってしまう）。
    #    ⚠️ c306-2 は A/B の一致率が 93.8→90.9 と**下がった**が、聞取は「手から」→「タテヤから」＝読みは直っている。
    "建屋から25フィート": "たてやから25フィート",
    "建屋を": "たてやを",
    "建屋は、切って": "たてやは、切って",
    # c404-2 文頭「放出を」。4テイクとも「凹凸を／応酬を」＝ほうしゅつ でない音。かなで聞取が「放出を」に。
    "放出を": "ほうしゅつを",
    # c216-2「5、始動確認表を通す」。数字＋読点のあとで頭が弱く「シード確認表」。かなで聞取「指導確認表」＝しどう と読めた。
    "始動確認表": "しどう確認表",
    # c316-2「継手のところで」。素は「小手／桂手／空手」＝つぎて でない音。かな「つぎて」は「ついて」に割れたので、
    #    **漢字を混ぜて1語で渡す**（4本目「耐圧殻→耐圧かく」と同じ型）。聞取が「継手」になった。
    "継手": "つぎ手",
    # c417-1「値が出た」。素は「苗が／名題が」＝あたい でない音。かなで聞取「値が」。
    #    ⚠️ 同じ行の「門衛所」が A/B の回で崩れた（猛営所）が、これはテイクのばらつき（前の回は正しい）。
    #    採用したうえで el_retake で振り直し、両方が通るテイクを採った。
    "値が": "あたいが",
    # c725-1「要旨には、こうある。」＝全435行で一致率 最下位（40%）。素は「用心／幼児／用事」＝**し が濁って ようじ**、
    #    かな「ようしには」は「凝視」・カナ「ヨウシには」は「表紙」＝**頭に子音が付く**（6テイク取り直しても落ちた）。
    #    ⭐ かな＋**半角空白でアクセント句を切る**と聞取「要旨にはこうある」100%（心理ch「いま 動かせる」と同じ型）。
    #    ⚠️ 文中の要旨（c712-1）は聞取「用紙」＝ようし と正しく読めているので触らない。
    "要旨には": "ようし には",
    # ---- 2026-09-07 ⑤a 第2巡：**「1字の入れ替え」の検査（el_check_heard の⑤）を足して見つけた分** ----
    # 🔴 ③「字の欠け」は2字以上でないと鳴らないので、1字で読みが変わる型を構造的に見ていなかった。
    #    下は取り直し（最大4テイク）では収束せず、A/B で書き方を変えて決着した4件。
    # c112-1 文頭「濃縮度は」→ 聞取『凝縮度』（ぎょうしゅく）。かなで聞取「濃縮度は」に。
    #    ⚠️ 一致率は 81.8%→81.8% と動かないが、**見るのは中身**（同じ回で「試験炉→試験の」が揺れただけ）。
    "濃縮度は": "のうしゅくどは",
    # c112-2「ホウ素を含んだ」→ 聞取『ホース』＝1語に潰れる。かなで 100%。
    "ホウ素を": "ほうそを",
    # c602-2「値は目に見えて」→ 聞取『熱は』。c417-1「値が→あたいが」と同じ型。かなで 100%。
    "値は": "あたいは",
    # c913-1「同じ節に」→ 聞取『同じ伏せに』。半角空白でアクセント句を切ると聞取『同じ説に』＝せつ と読めた。
    #    ⚠️ 同じ行の c912-1「同じ節は」は聞取『同じ説は』＝せつ で正しいので触らない。
    "同じ節に": "同じ せつに",
    # c709-1「番号は、アイ・ディー・オー、19311。320ページある。」＝台本第2版 §6-2 が名指しで
    #    「⚠️ 報告書番号は数として読ませない」と書いた箇所。
    # 🔴 文字起こしでは分からない（Scribe はどちらでも「19311」と書く）ので、**長さで見分けた**。
    #    同じ文を3テイクずつ合成した中央値＝素 6.32秒／1桁ずつ 5.03秒／数として 6.72秒
    #    ＝素は「数として（いちまんきゅうせんさんびゃくじゅういち）」に 0.40秒差、1桁ずつには 1.29秒差。
    #    モーラ数の差（11 対 16＝5モーラ≒1.25秒）とも合う。→ 1桁ずつに固定する。
    "19311": "いちきゅうさんいちいち",
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
