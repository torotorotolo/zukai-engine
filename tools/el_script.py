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

SLUG = "ep11"               # 11本目 チャレンジャー号（2026-09-21）。10本目 "ep10"・9本目 "ep9"・8本目 "ep8"・7本目 "ep7"・6本目 "keybridge"・5本目 "sl1"・4本目 "surfside"
# 🔴 話速 1.0 を**明示して送る**（2026-09-07 カズヤくん指示）。渡さないと声に保存された既定
#    speed 1.14 で読まれる。speed 以外の4つは /v1/voices/<id>/settings の実測をそのまま写した
#    （2026-09-07 に API で取り直し＝stability 0.85 / similarity_boost 1.0 / style 0.0 /
#     use_speaker_boost True）。部分的に送ると残りが API 既定に落ちるので**5つ全部**送る。
# ⚠️ 4本目の実測では「eleven_v3 は speed を無視する」（0.8/0.9/1.0/なしで 3.28〜3.60秒＝ばらつきの範囲）。
#    ⑤a の頭で1行 A/B して、効いたかどうかを実測で確かめる（効かなくても害は無い）。
# ⚠️ SETTINGS はキャッシュの鍵に入る＝途中で変えると全行が別物（＝全編もう一度課金）になる。
# 🔴🔴 2026-09-13（7本目）: 声を **Koichi-Deep Calm Japanese Narrator** に替えたので、
#    speed 以外の4つも **Koichi に保存された既定**へ取り直した（/v1/voices/<id>/settings・API 実測）:
#        Koichi … stability 0.64 / similarity_boost 0.89 / style 0.0 / speaker_boost True（speed 1.02）
#        Hiro   … stability 0.85 / similarity_boost 1.00 / style 0.0 / speaker_boost True（speed 1.14）
#    ⚠️ **Hiro の値をそのまま Koichi に当てない。**声ごとに作者が合わせた値で、別の声に流用すると
#       その声の持ち味から外れる（規則は「その声の既定を写す」＝2026-09-07 と同じ。値だけが変わる）。
#    ⚠️ stability が 0.85 → 0.64 に下がる＝**表情は出るが振れも大きくなる**。
#       ⑤a の頭で1行 A/B して、読み間違い・余計な音が増えていないかを実測で見る。
# 🔴🔴 2026-09-19（10本目）: 声を **Sho - Japanese Male** に替えた（el_tts.VOICE_NAME）。
#    値は「声の既定」ではなく **カズヤくんが画面で試聴した音の実際の値**を写した:
#    /v1/history（Sho・2026-09-19 22:14〜22:16 の18件）＝ model eleven_v3 / **stability 1.0**（つまみ右端「安定」）/
#    **similarity 0.75**。⚠️ 声に保存された既定は similarity_boost **0.7**（stability 0.8）で、試聴の音とは違う。
#    画面の v3 には style・speaker_boost の項目が無いので、この2つは声の既定（0.0・True）を写した。
#    speed は v3 が見ない（3回再現）が、従来どおり 1.0 を明示する。
#    ⚠️ 画面の「距離：近く」は API に項目が無い＝ここには入れていない（el_tts.py の注記・判断待ち）。
# 🔴🔴 2026-09-21（10本目⑥）: 声を **Otani** に替えた（カズヤくん指示）。値は次のとおり。
#    similarity_boost 0.75 / style 0.0 / speed 1.0 / speaker_boost True … **Otani の既定をそのまま写した**
#      （`/v1/history` に Otani の記録は0件＝試聴した値を写す道が無く、2026-09-07 の規則に戻る）
#    🔴 stability だけ既定 **0.5 → 1.0** に上げた。**全編を焼く前に A/B して実測で決めた**
#      （`qa_out/ep10_ab_stability.py`＝転びやすい10行 × 2設定 × 2周・340クレジット）:
#        一致率の平均 … 0.5＝77.85% ／ **1.0＝81.14%**
#        🔴 0.5 は `c614-1` の2周目が **`[outro jingle]`**＝**台本に無い音**として起こされた
#        🔴 0.5 は `c404-2` で異音の警告（3.51秒地点に**振幅が本文の2.0倍**の浮いた音 210ms）
#        0.5 は同じ音を2周起こすと3行でぶれる／1.0 はほぼ全行で同じ結果
#      ⚠️ `pr06-1` だけ一致率は 0.5 が上だが、**読みは 1.0 が正しい**（「二十七点六」／0.5「二七．六」）
#         ＝一致率で採否を決めない（[[feedback-ear-beats-the-meter]]）
#    ⚠️ 値はキャッシュの鍵に入る＝変えると全行が別物になり**全編もう一度課金**。ここから先は触らない。
SETTINGS = {"stability": 1.0, "similarity_boost": 0.75, "style": 0.0,
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
    # 🔴 7本目 9.11（2026-09-13 ④' 承認ずみ）。出所＝check_script.py を自分で回した出力
    #    「カット 202 / 字幕行 454 / 本文 11157字 / 決め所 22」＝E 0件 / W 1件（W は尺の3通りの開き）
    "ep7":      {"cuts": 202, "lines": 454, "chars": 11157, "quotes": 22, "why": "9.11 台本第2版",
                 "md": "事故検証-9.11-台本第2版-20260913.md"},
    # 🔴 8本目 コロンビア号（2026-09-14 ④' 承認ずみ）。出所＝check_script.py を自分で回した出力
    #    「カット 216 / 字幕行 489 / 本文 12235字 / 決め所 14」＝E 0件 / W 3件
    "ep8":      {"cuts": 216, "lines": 489, "chars": 12235, "quotes": 14, "why": "コロンビア号 台本第2版",
                 "md": "事故検証-コロンビア号-台本第2版-20260914.md"},
    # 🔴 9本目 テネリフェ（2026-09-16 ④' 承認ずみ）。出所＝check_script.py を⑤aで自分で回した出力
    #    「カット 215 / 字幕行 495 / 本文 12515字 / 決め所 14」＝E 0件 / W 5件
    #    ⚠️ 台本 §0 の「12511字」は4字古い（④' の最後の直しの前の数）。⑤a の実測を正とする
    "ep9":      {"cuts": 215, "lines": 495, "chars": 12515, "quotes": 14, "why": "テネリフェ 台本第2版",
                 "md": "事故検証-テネリフェ-台本第2版-20260916.md"},
    # 🔴 10本目 三豊百貨店（2026-09-20 ④' 完了）。出所＝check_script.py を⑤aで自分で回した出力
    #    「カット 195 / 字幕行 460 / 本文 11537字 / 決め所 14」＝E 0件 / W 4件
    #    ⚠️ 11,537字は ⑤a で `ep05` の月数を「6月／10月」→「6か月／10か月」に直したあとの数（④' は 11,533字）。
    #       TTS が「6月」を **ろくがつ** と読むため。字幕にも出る語なので辞書ではなく台本側で直した。
    #    ⚠️ 11,541字は ⑤b-1 で `ep12` を「手抜きの工事で」→「**わざと**手を抜いた工事で」に直したあと（+4字）。
    #       無期／3年以上が掛かるのは**故意**の罪（建築法 제77조의2）で、三豊の被告は**業務上過失**。
    #       「わざと」が無いと、直前まで三豊の話を聞いてきた人が**自分たちの刑だと受け取る**（§1-8）。
    #       同じ回で `c802` の「延べ」→「のべ」も直した（`c807` とそろえた。字数は変わらない）。
    "ep10":     {"cuts": 195, "lines": 460, "chars": 11541, "quotes": 14, "why": "三豊百貨店 台本第2版",
                 "md": "事故検証-三豊百貨店-台本第2版-20260920.md"},
    # 🔴 11本目 チャレンジャー号（2026-09-21 ④' 完了・カズヤくん承認ずみ）。
    #    出所＝check_script.py を⑤aで自分で回した出力
    #    「カット 190 / 字幕行 470 / 本文 11497字 / 決め所 18」＝E 0件 / W 6件（W は全部 章ごとの写真映像）
    #    ⚠️ 11,497字は ⑤a で**新設した門番**（裸の「N度」）が出した E 1件と W 2件を直したあとの数
    #       （④' の 11,491字 +6）。`c607` の★・`c301`・`c619` に「摂氏」を足した（各+2字）。
    #       ★は画面にそれだけ出るので、11.7度が摂氏か華氏か分からないまま出ていた。
    "ep11":     {"cuts": 190, "lines": 470, "chars": 11497, "quotes": 18, "why": "チャレンジャー号 台本第2版",
                 "md": "事故検証-チャレンジャー号-台本第2版-20260921.md"},
}
# 🔴🔴 **全回で共通の末尾**（2026-09-21・⑤a 新設）。`narration.SCRIPT` には入るが、
#    **Vault の台本 md には無い**（④ が書くものではなく、⑥ で足した全回共通の資産だから）。
#    ＝ 上の EXPECT と `md_vs_script()` は**ここを外して**数える。
#    ⚠️ これを入れずに ⑥ が `ed01` を足した結果、**10本目の --selftest は 09-21 からずっと落ちていた**
#       （narration.SCRIPT 196 対 EXPECT 195・md 460行 対 .py 463行）。
#       [[feedback-gates-go-stale-when-upstream-changes]]＝上流を替えたら門番の幾何も取り直す。
COMMON_TAIL = ("ed01",)
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


def md_vs_script():
    """🔴🔴 **台本の md と `narration.SCRIPT` の文を、1行ずつ突き合わせる**（2026-09-20 ⑤b-1 新設）。

    なぜ要るか: 音を焼くのは `narration.SCRIPT` だが、**人が直すのは Vault の md のほう**。
    それまでの `--selftest` は `narration.SCRIPT` を**直書きの定数**（cuts/lines/chars/quotes）と
    比べていただけなので、**md だけを直すと「✓ 台本と一致」と出たまま、音は古い文のまま**になる。
    実際 ⑤b-1 で md の2行（`ep12` `c802`）を直したら、selftest は**そのまま ✓ を出した**。
    → [[feedback-gates-go-stale-when-upstream-changes]]（黙って間違った合格）

    ⚠️ md は決め所を `★**…**` で囲む。`narration.SCRIPT` は素の文を持つので、**そこだけ外して**比べる。
    fail closed: md が無ければ例外（0件を合格にしない）。
    """
    import check_script as CSC
    p = VAULT / EXPECT[SLUG]["md"]
    if not p.exists():
        raise SystemExit(f"🔴 台本の md が無い: {p}")
    md = [(cid, t.strip()) for cid, _, ls in CSC.parse(p.read_text(encoding="utf-8")) for t in ls]
    py = [(l.cid, l.text) for l in lines() if l.cid not in COMMON_TAIL]   # 🔴 共通の末尾は md に無い
    strip = re.compile(r"^★\*\*(.*)\*\*$")
    bad = []
    if len(md) != len(py):
        bad.append(f"行数が違う: md {len(md)}行 ／ narration.SCRIPT {len(py)}行")
    for (mc, mt), (pc, pt) in zip(md, py):
        m = strip.match(mt)
        if m:
            mt = m.group(1)
        if mc != pc or mt != pt:
            bad.append(f"{mc}: md「{mt}」／ .py「{pt}」")
    return bad


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


# ── EL_YOMI（9本目 テネリフェ）───────────────────────────────
# 🔴 **空から始める**（8本目と同じ作法）。台本第2版 §6 は「危険の候補」であって、読みの正解は入っていない。
#    1語ずつ鳴らして（el_ab_yomi）確かめた語だけを、根拠を1行添えて入れる（feedback-yomi-dict-must-be-verified）。
# 🔴 7本目（git 27606de）・8本目（git 9c9e9a1）の辞書は**候補の出どころ**として当てる
#    （`qa_out/ep9_yomi_prior.py`＝この回の495行にどのキーが当たるかを数える）。**そのまま引き継がない**。
#    8本目の辞書の控え＝`audio/el_qa/ep8_el_yomi_dict.json`
# ⭐ A/B 1周目（97件・`audio/el_qa/ep9_yomi_ab.tsv`・計画と門番＝`qa_out/ep9_yomi_plan.py`）から入れた。
#    A/B の「前」は同じ音の**2回目の聞取**＝1周目の全文起こしと合わせて**2回の観測**で決めた（7本目・8本目の作法）。
#    根拠の書き方＝「前の聞取 → 後の聞取」。
EL_YOMI = {
    # 🔴🔴 **11本目（チャレンジャー号）で空にした**（2026-09-21・⑤a）。
    #    下にあった10本目（三豊百貨店）のキー約90件は、ep11 の本文に1行も当たらない。
    #    ＝ 残すと import 時の門番②「キーが台本のどの行にも当たらない」で止まる（fail closed）。
    #    旧版は git 履歴（`git show HEAD~1:tools/el_script.py`）に全部残っている。
    #
    # 🔴 ここは**焼く前に埋めない**。[[feedback-yomi-dict-must-be-verified]]＝類推で書かない。
    #    順番: ① 空のまま全編を焼く → ② `el_check_yomi.py` の Scribe 全文起こしで**実際の誤読**を採る
    #        → ③ `el_ab_yomi.py` の A/B で直る読みを確かめる → ④ ここへ入れる → ⑤ 焼き直す
    #    ⚠️ **入れる前に `--hits` で当たる行数を数える**（[[feedback-audio-yomi-zero]]）。
    #       1件直すつもりのキーが 40行に当たると、崩れていない行のアクセントまで壊す。
    #    ⚠️ 正しく読めている語をかな化しない（アクセントが壊れる）。
    #    ⚠️ 行頭にカナを置かない（例外＝取り直しでも崩れる行頭語）。
    #
    # 🔴 **会議の出席者7人（ボイジョリー／マロイ／ハーディ／メイソン／ランド／キルミンスター／
    #    マクドナルド）のキーは入れない。**2026-09-21 カズヤくん決定＝この回は名前を出さず役で呼ぶ。
    #    本文に1行も無いので、入れると門番②で止まる（④'の申し送り）。
    #
    # ℹ️ この回で読みが危ないと分かっているもの（④'の申し送り。**焼いてから Scribe で確かめる**）:
    #      小数の秒 … 0.678 / 3.375 / 0.836 / 58.788 / 64.660 / 73.124 / 73.137 / 73.618
    #      小数の度 … 2.2 / 8.3 / 11.7 / 12.8 / 16.1（全部「摂氏」が付いている）
    #      分数の秒 … 「1000分の1秒」（c302-3）／「100分の1秒」（c322-1）
    #      人名   … 乗員7人・モーガン・ファインマン・ロジャース
    #      ⚠️ ep10 のような「N万N,NNN」「NN,NNN」の数は **この回には1つも無い**
    #         （実測＝`1万4000`（c406-2）・`1000`・`7000` のみ）。
    #         [[feedback-notation-change-breaks-readings]] の型はこの回では起きない。
}
# 🔴 「三豊」は**必ず直後に漢字が来る**（三豊百貨店／三豊建設／三豊建設産業）。
#    既定の境界規則は「漢字で終わるキーは直後が漢字なら当てない」なので、開けないと1行も当たらない
#    （門番が「台本のどの行にも当たらない」で止めてくれた＝黙って素通りしない）。
#    ⚠️ 右を開けても巻き添えは起きない。台本に「三豊」で始まる別の語は無い（実測 8件すべて 百貨店／建設）。
EL_YOMI_OPEN_RIGHT = frozenset()   # 🔴 10本目の "三豊" を外した（2026-09-21・⑤a）。EL_YOMI と同時に空にする
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
    # 🔴 EXPECT は**台本（md）の数**＝共通の末尾 `ed01` を外して突き合わせる（COMMON_TAIL の注記）
    body = [l for l in ls if l.cid not in COMMON_TAIL]
    n_cuts = sum(1 for cid, _ in narration.SCRIPT if cid not in COMMON_TAIL)
    n_chars = sum(len(l.text) for l in body)
    e = EXPECT[SLUG]
    why = e["why"]
    print(f"台本: {n_cuts}カット／{len(body)}行／{n_chars}字（{why} の実測は "
          f"{e['cuts']}／{e['lines']}／{e['chars']:,}・決め所 {e['quotes']}）")
    print(f"  ＋共通の末尾 {len(ls) - len(body)}行（{'／'.join(COMMON_TAIL)}）"
          f"＝焼くのは {len(narration.SCRIPT)}カット／{len(ls)}行／{sum(len(l.text) for l in ls)}字")
    ok = (n_cuts, len(body), n_chars) == (e["cuts"], e["lines"], e["chars"])
    print("  " + (f"✓ {why}と一致（直書きの定数と）" if ok else f"🔴 {why}と食い違う"))
    # 🔴🔴 2026-09-20（⑤b-1）**定数と合っていても、md と .py がずれていれば意味が無い。**
    #    音を焼くのは narration.SCRIPT、人が直すのは Vault の md。ここで1行ずつ突き合わせる。
    drift = md_vs_script()
    ok_md = not drift
    print("  " + (f"✓ Vault の md と narration.SCRIPT の文が1行ずつ一致（{len(body)}行）"
                  if ok_md else f"🔴 md と narration.SCRIPT が {len(drift)}行 食い違う"
                                f"＝**焼く文と、人が読む台本が別物**"))
    for d in drift[:12]:
        print(f"     {d}")
    ok &= ok_md
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
