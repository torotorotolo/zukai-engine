# -*- coding: utf-8 -*-
r"""aq_kana.py — 台本の文を **AquesTalk の音声記号列** に変える（2026-09-25・14本目⑤a 新設）。

  python tools/aq_kana.py "9時50分、最後の放送も船内で待つように"   … 1文を変換（語ごとの内訳つき）
  python tools/aq_kana.py --sheet          … narration.SCRIPT の全行 → ref/<SLUG>/aq/yomi_sheet.tsv
  python tools/aq_kana.py --selftest       … 答えの分かっている入力で検算（陽性・陰性対照）

■ なぜ作ったか
  14本目から声がゆっくり（AquesTalk・AquesTalkPlayer のコマンド）。AquesTalkPlayer に漢字かな文を渡すと、
  中の変換器（AqKanji2Koe）が読みを決めるが、**どう読んだかをコマンドで取り出せない**＝音になるまで誤読が見えない。
  ElevenLabs の時代は、聞取（Scribe）が誤読を正しい字で書き戻すため、読みの網が試写の耳だけになっていた
  （記憶 feedback-scribe-writes-the-right-word-for-misreadings）。
  → **読みとアクセントをこちらで音声記号列に書き切って渡す**（`#>` を付けると AquesTalkPlayer はそのまま読む）。
    合成の前に、全行の読みが**文字で**見える＝機械の門番（数の台帳・音節の表）と人の目で確かめられる。
  ⚠️ ライセンス：DLL は呼ばない（開発ライセンスが要る）。変換は pyopenjtalk-plus（オープンソース）、
     合成は AquesTalkPlayer（アプリ）＝使用ライセンスの範囲（記憶 project-jiko-yukkuri-voice-trial）。

■ 音声記号列（AquesTalk 音声記号列仕様書 v2.0・2025-04-03）
  読み＝ひらがな（無声化とガ行鼻濁音は AquesTalk が自動で付ける）／アクセント核の読み記号の**直後**に `'`
  （無ければ平板）／アクセント句の区切り `/`／句切り `、`（間）`。`（文末）`？`（文末を上げる）。
  1つのアクセント句に `'` は1つまで。使える音節は仕様書の表だけ（ぢ・づ・ゔ は無い）。

■ 作り（pyopenjtalk-plus の run_frontend＝アクセント句とアクセント型を付けたあとの語の並び）
  - chain_flag が 1 の語は前のアクセント句に続く。句の先頭の語の acc が**句の**アクセント型（句頭から数えた核の位置）
  - pron の `’` は**無声化の印**（アクセントではない）＝外す（ひらがなで渡せば AquesTalk が自動で無声化する）
  - 🔴 数は桁ごとに別の句に割れる（「ひゃ'く/にじゅ'ー/さんてー」＝下がり目が3回）→ **1つの句にまとめる**
    （MERGE_NUMBERS。核は最後の小さな句の核を使う）。聞き比べは⑤a-2 で
  - 記号は元の字で振り分ける（pyopenjtalk は 。「」★・ を全部「、」にする）
  - 回ごとの利用者辞書 `ref/<SLUG>/aq/userdict.csv`（pyopenjtalk の利用者辞書＝MeCab の CSV）と、
    行ごとの手書き `ref/<SLUG>/aq/override.tsv`（行ID<TAB>音声記号列）を読む
"""
import csv
import hashlib
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import speaker  # noqa: E402

MERGE_NUMBERS = True     # 桁ごとに割れた数を1つのアクセント句にまとめる（⑤a-2 で聞き比べて決める）

# ── 仕様書 §5「読み記号表」（v2.0）。ひらがなで持つ（カタカナは同じ音で無声化・鼻濁音を自動で付けない）
_BASE = ("あいうえお かきくけこ さしすせそ たちつてと なにぬねの はひふへほ まみむめも やゆよ らりるれろ わ を "
         "がぎぐげご ざじずぜぞ だでど ばびぶべぼ ぱぴぷぺぽ ん っ ー").split()
_COMBO = ("くぁ くぃ くぇ くぉ すぃ てゅ てぃ とぅ ふぁ ふぃ ふゅ ふぇ ふぉ いぇ つぁ つぃ つぇ つぉ うぃ うぇ うぉ "
          "ぐぁ ぐぃ ぐぇ ぐぉ ずぃ でゅ でぃ どぅ "
          "きゃ きゅ きぇ きょ しゃ しゅ しぇ しょ ちゃ ちゅ ちぇ ちょ にゃ にゅ にぇ にょ ひゃ ひゅ ひぇ ひょ "
          "みゃ みゅ みぇ みょ りゃ りゅ りぇ りょ ぎゃ ぎゅ ぎぇ ぎょ じゃ じゅ じぇ じょ びゃ びゅ びぇ びょ "
          "ぴゃ ぴゅ ぴぇ ぴょ").split()
ALLOWED = set("".join(_BASE)) | set(_COMBO)
ALLOWED -= {" "}
# ⚠️ v2.0 で足された・実装しだいの音節（仕様書の表の注「実装有無はライブラリ依存」）＝使ったら W（⑤a-2 で音を確かめる）
V2_RISKY = {"ふゅ", "ぐぃ", "きぇ", "にぇ", "ひぇ", "みぇ", "りぇ", "ぎぇ", "びぇ", "ぴぇ"}
_SMALL = set("ぁぃぅぇぉゃゅょゎ")
# 表に無い字の置き換え（音が同じ）。ゔ は近い音へ（⑤a-2 で確かめる）
_MAP = {"ぢ": "じ", "づ": "ず", "ゔぁ": "ば", "ゔぃ": "び", "ゔぇ": "べ", "ゔぉ": "ぼ", "ゔ": "ぶ"}

DELIM = {"。": "。", "．": "。", "！": "。", "!": "。", "？": "？", "?": "？",
         "、": "、", "，": "、", ",": "、"}
DROP = set("★「」『』【】〈〉《》\"'“”‘’*")          # 読まない記号（括弧は中身だけ読む）
PAREN_OPEN, PAREN_CLOSE = set("（("), set("）)")      # 開き＝間（、）・閉じ＝何もしない


class AqError(ValueError):
    """音声記号列にできない（fail closed＝黙って読みを作らない）。"""


def kata2hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)


def moras(kana):
    """ひらがな列を読み記号（音節）に切る。小さい字は前に付ける（「じゅ」は1つ）。"""
    for a, b in sorted(_MAP.items(), key=lambda kv: -len(kv[0])):
        kana = kana.replace(a, b)
    out = []
    for ch in kana:
        if ch in _SMALL and out and out[-1] not in ("っ", "ー", "ん"):
            out[-1] += ch
        else:
            out.append(ch)
    return out


def check_moras(ms, where=""):
    """表に無い音節・並びの制限（仕様書 §3.8）を調べる。(E の一覧, W の一覧)。"""
    E, W = [], []
    for i, m in enumerate(ms):
        if m not in ALLOWED:
            E.append(f"表に無い音節「{m}」{where}")
        elif m in V2_RISKY:
            W.append(f"v2.0 の音節「{m}」（実装しだい）{where}")
        if m == "っ" and i + 1 < len(ms) and ms[i + 1] in ("っ", "ー"):
            E.append(f"「っ{ms[i + 1]}」は並べられない{where}")
    if ms and ms[0] == "ー":
        E.append(f"アクセント句の頭に「ー」{where}")
    if ms and ms[-1] == "っ":
        # 仕様書 v2.0（2025-04）で許された。AquesTalkPlayer 1.1.1.1（2025-06）が受け付けなければ合成が
        # エラーコードで止まる＝黙っては通らない。⑤a-2 で確かめる（14本目 c808「えっ、」）
        W.append(f"アクセント句の最後が「っ」{where}（v2.0 で可・⑤a-2 で音を確かめる）")
    return E, W


# ── 回ごとの辞書と手書き ─────────────────────────────────────────────
def ep_dir(slug=None):
    if slug is None:
        import el_script
        slug = el_script.SLUG
    return ROOT / "ref" / slug / "aq"


_LOADED = {"dict": None}


def load_userdict(slug=None):
    """ref/<SLUG>/aq/userdict.csv を pyopenjtalk に読ませる（中身の md5 が変わったときだけ作り直す）。
    戻り値＝読んだ語数（ファイルが無ければ 0）。"""
    import pyopenjtalk
    d = ep_dir(slug)
    src = d / "userdict.csv"
    if not src.exists():
        return 0
    body = src.read_bytes()
    rows = [r for r in csv.reader(body.decode("utf-8").splitlines()) if r and not r[0].startswith("#")]
    if not rows:
        return 0
    h = hashlib.md5(body).hexdigest()[:12]
    if _LOADED["dict"] == h:
        return len(rows)
    cache = d / ".cache"
    cache.mkdir(exist_ok=True)
    tmp = cache / f"userdict_{h}.csv"          # 注の行を外した CSV（MeCab は # を知らない）
    dic = cache / f"userdict_{h}.dic"
    if not dic.exists():
        with open(tmp, "w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(rows)
        pyopenjtalk.mecab_dict_index(str(tmp), str(dic))
    pyopenjtalk.update_global_jtalk_with_user_dict(str(dic))
    _LOADED["dict"] = h
    return len(rows)


def load_override(slug=None):
    """ref/<SLUG>/aq/override.tsv（行ID<TAB>音声記号列<TAB>理由）。"""
    p = ep_dir(slug) / "override.tsv"
    out = {}
    if p.exists():
        for ln in p.read_text(encoding="utf-8").splitlines():
            if not ln.strip() or ln.startswith("#"):
                continue
            parts = ln.split("\t")
            if len(parts) < 2:
                raise AqError(f"override.tsv の行の形が違う（行ID<TAB>記号列<TAB>理由）: {ln!r}")
            out[parts[0].strip()] = parts[1].strip()
    return out


# ── 変換 ─────────────────────────────────────────────────────────────
def _pre(text):
    """読まない記号を外し、括弧を間にする（中身は読む）。"""
    t = speaker.bare(text).replace("**", "")
    t = "".join("、" if c in PAREN_OPEN else ("" if c in PAREN_CLOSE or c in DROP else c) for c in t)
    t = re.sub(r"、{2,}", "、", t).strip("、 ")
    return t


def _is_num(w):
    return w["pos"] == "名詞" and (w.get("pos_group1") == "数" or w["string"] in ("．", "."))


def _is_counter(w):
    return w.get("pos_group1") == "接尾" and w.get("pos_group2") == "助数詞"


_ALNUM = re.compile(r"[A-Za-zＡ-Ｚａ-ｚ0-9０-９]")
_KANA = re.compile(r"[ァ-ヴー]")
_KANJI = re.compile(r"[一-鿿]")
_LONG_O = re.compile(r"([オコソトノホモヨロゴゾドボポョ])ウ")


def phrases(text, dropped=None):
    """文 → [(読み記号の列, 核の位置 0=平板, 句切り記号 or None, 語の表層)]
    dropped（list）を渡すと、読みが付かずに落ちた英数字の語をそこへ入れる（to_aq が E にする）。"""
    import pyopenjtalk
    t = _pre(text)
    if not t:
        raise AqError(f"読む字が無い: {text!r}")
    out, cur = [], None
    prev_digit = prev_numeric = False
    for w in pyopenjtalk.run_frontend(t):
        s = w["string"]
        readable = bool(w["pron"]) and w["pron"] not in ("、", "？", "。") and bool(_KANA.search(w["pron"]))
        if not readable:
            # 記号と、読みの付かない語。🔴 読みの付いた語を先に語として扱う＝小数点「．」（テン）はここへ来ない
            #    （先に DELIM を引いていたら「約1.7メートル」が「やく/いっ。ななめーとる」＝文が切れた・14本目⑤a）
            d = DELIM.get(s) or ("/" if s in ("・", "･") else None)     # 中黒＝間を置かない句の区切り
            if d is None:
                # 🔴 英数字なら落とさず E（「A甲板」の A が黙って消えた＝14本目⑤a）
                if _ALNUM.search(s) and dropped is not None:
                    dropped.append(s)
            elif cur is not None:
                cur["delim"] = d
                out.append(cur)
                cur = None
            elif out and d != "/":
                out[-1]["delim"] = d if out[-1]["delim"] in (None, "/") else out[-1]["delim"]
            prev_digit = prev_numeric = False
            continue
        pron = w["pron"].replace("’", "").replace("'", "")
        # 🔴 漢字の名詞の「オ段＋ウ」は伸ばす音（表＝ヒョウ→ヒョー・量＝リョウ→リョー）。AquesTalk は「う」を別の母音として
        #    読む（仕様書 §2.1「長音は ー を指定」）。カタカナ語（ソウル）と動詞（追う）は本当に「う」＝触らない（14本目⑤a）
        if w["pos"] == "名詞" and _KANJI.search(s):
            pron = _LONG_O.sub(r"\1ー", pron)
        ms = moras(kata2hira(pron))
        digit = _is_num(w)                                           # 数字1つ（と小数点）
        numeric = digit or bool(re.match(r"[0-9０-９]", s))           # 「４月」「１等航海士」のように数字で始まる語も
        chained = w["chain_flag"] == 1
        # 🔴 数の前では句を切る（14本目 c813「そのころ2等航海士」が「そのころに、とうこうかいし」と聞こえる形で
        #    1つの句につながっていた）。接頭詞（約・第など）のあとは pyopenjtalk の決めたとおり
        if numeric and not prev_numeric and cur is not None and cur["words"] and not cur.get("prefix"):
            chained = False
        # 桁ごとに割れた数を1つの句に＝**数字どうしと、数字のあとの助数詞だけ**（「４月」と「十六日」はつなげない）
        merge = MERGE_NUMBERS and prev_digit and (digit or _is_counter(w)) and cur is not None
        if cur is None or not (chained or merge):
            if cur is not None:
                cur["delim"] = cur["delim"] or "/"
                out.append(cur)
            cur = {"ms": [], "acc": w["acc"], "sub": None, "delim": None, "words": []}
        elif merge and not chained:
            cur["sub"] = len(cur["ms"]) + w["acc"] if w["acc"] > 0 else 0   # 割れた小さな句の核（最後のものを採る）
        cur["ms"] += ms
        cur["words"].append(s)
        cur["prefix"] = w["pos"] == "接頭詞"
        prev_digit, prev_numeric = digit, numeric
    if cur is not None:
        out.append(cur)
    res = []
    for p in out:
        acc = p["sub"] if p["sub"] is not None else p["acc"]
        acc = max(0, min(acc, len(p["ms"])))
        res.append((p["ms"], acc, p["delim"], "".join(p["words"])))
    return res


def to_aq(text, where=""):
    """文 → (音声記号列, E の一覧, W の一覧)。E があれば記号列は使ってはいけない。"""
    E, W = [], []
    dropped = []
    ps = phrases(text, dropped)
    for s in dropped:
        E.append(f"読みの付かない英数字「{s}」が落ちた（{where}）＝利用者辞書に入れる")
    buf = []
    for i, (ms, acc, delim, words) in enumerate(ps):
        e, w = check_moras(ms, f"（{where}「{words}」）")
        E += e
        W += w
        body = "".join(ms[:acc]) + ("'" if acc else "") + "".join(ms[acc:])
        if delim is None:
            delim = "/" if i + 1 < len(ps) else None
        buf.append(body + (delim or ""))
    s = "".join(buf)
    if not s or s[-1] not in "。？、":
        s = s.rstrip("/") + "。"             # 文の最後は必ず句切り記号（仕様書 §3.7）
    return s, E, W


def plain(aq):
    """音声記号列から読みだけ（人が読む用）。"""
    return re.sub(r"['/]", "", aq)


def validate(aq, where=""):
    """手書きの記号列（override）を仕様の形で調べる。"""
    E, W = [], []
    if not aq or aq[-1] not in "。？、":
        E.append(f"文の最後が句切り記号でない{where}")
    for seg in re.split(r"[/、。？,;+]", aq):
        if not seg:
            continue
        if seg.count("'") > 1:
            E.append(f"1つのアクセント句に「'」が2つ「{seg}」{where}")
        if seg.startswith("'"):
            E.append(f"「'」が読み記号の前「{seg}」{where}")
        e, w = check_moras(moras(seg.replace("'", "")), where)
        E += e
        W += w
    return E, W


# ── 全行の一覧 ───────────────────────────────────────────────────────
def sheet(write=True):
    """narration.SCRIPT の全行 → [(行ID, 話者, 文, 記号列, 読み, 出どころ, E, W)]。"""
    import narration
    n_dict = load_userdict()
    ov = load_override()
    rows, seen = [], set()
    for cid, ls in narration.SCRIPT:
        for i, t in enumerate(ls, 1):
            lid = f"{cid}-{i}"
            who, body = speaker.split(t)
            if lid in ov:
                aq, src = ov[lid], "override"
                E, W = validate(aq, f"（{lid}）")
                seen.add(lid)
            else:
                aq, E, W = to_aq(body, lid)
                src = "auto"
            rows.append((lid, who or "", body, aq, plain(aq), src, E, W))
    stale = sorted(set(ov) - seen)
    if write:
        d = ep_dir()
        d.mkdir(parents=True, exist_ok=True)
        with open(d / "yomi_sheet.tsv", "w", encoding="utf-8", newline="") as f:
            f.write("行ID\t話者\t文\t音声記号列\t読み\t出どころ\n")
            for lid, who, body, aq, pl, src, _, _ in rows:
                f.write(f"{lid}\t{who}\t{body}\t{aq}\t{pl}\t{src}\n")
    return rows, n_dict, stale


def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %s %-30s 期待 %-26r 実際 %r" % ("OK " if good else "🔴NG", name, want, got))

    chk("じゅ は1つの音節", moras("じゅんび"), ["じゅ", "ん", "び"])
    chk("っ・ー・ん は1つずつ", moras("がっこーせん"), ["が", "っ", "こ", "ー", "せ", "ん"])
    chk("づ→ず・ぢ→じ", moras("つづく ちぢむ".replace(" ", "")), ["つ", "ず", "く", "ち", "じ", "む"])
    chk("ゔぁ→ば", moras("ゔぁいおりん"), ["ば", "い", "お", "り", "ん"])
    chk("🔴表に無い音節で止める", bool(check_moras(["しぃ"])[0]), True)
    chk("🔴句の頭の ー で止める", bool(check_moras(["ー", "か"])[0]), True)
    chk("🔴っー で止める", bool(check_moras(["え", "っ", "ー"])[0]), True)
    chk("表にある音節は通す", check_moras(["て", "ぃ"][:1] + ["じゅ", "ー"])[0], [])
    chk("v2.0 の音節は W", bool(check_moras(["ふゅ"])[1]), True)
    chk("手書き: 句に ' が2つで止める", bool(validate("ひと'つのあくせんと'くです。")[0]), True)
    chk("手書き: 仕様書の例は通る", validate("こ'んどは、もーすこ'し/ふくざつな/おんせーき'ごーです。")[0], [])
    chk("手書き: 最後に句切りが無ければ止める", bool(validate("これわ")[0]), True)
    chk("括弧は間・閉じは消す", _pre("約2.4メートル（8フィート）の箱"), "約2.4メートル、8フィートの箱")
    chk("★と「」は読まない", _pre("★「その場で待機」"), "その場で待機")
    chk("聞き役の印は読まない", _pre("Q: 船長たちは？"), "船長たちは？")
    # 本番の変換（pyopenjtalk）で形を確かめる
    s, E, W = to_aq("船長たちは？")
    chk("聞き役の問いは ？ で終わる", s[-1], "？")
    chk("句の中に ' は1つまで", all(seg.count("'") <= 1 for seg in re.split(r"[/、。？]", s)), True)
    s2, _, _ = to_aq("9時50分、最後の放送も船内で待つように")
    chk("句点の無い文は。で閉じる", s2[-1], "。")
    chk("読み：くじごじゅっぷん", plain(s2).startswith("くじごじゅっぷん、"), True)
    s3, _, _ = to_aq("進水した。")
    chk("無声化の印 ’ を外す", "’" in s3, False)
    # 🔴 14本目⑤a で足した3つ（陽性対照）
    s4, _, _ = to_aq("そのころ2等の部屋")
    chk("🔴数の前で句を切る", "ころ/に" in s4 or "ころ'/に" in s4 or "ろ/に" in s4, True)
    s5, _, _ = to_aq("約79度")
    chk("接頭詞「約」のあとは pyopenjtalk のまま", plain(s5).startswith("やくななじゅー"), True)
    _, E6, _ = to_aq("Ｘ甲板の端")          # 辞書に無い英字（ここは辞書を読まない）
    chk("🔴読みの無い英数字は E（黙って落とさない）", bool(E6) or "えっくす" in plain(to_aq("Ｘ甲板の端")[0]), True)
    chk("句の最後の「っ」は W", (check_moras(["え", "っ"])[0], bool(check_moras(["え", "っ"])[1])), ([], True))
    s7, _, _ = to_aq("天井を約1.7メートル高くした。")
    chk("🔴小数点は文を切らない（てん と読む）", ("。" in s7[:-1], "いってんなな" in plain(s7)), (False, True))
    chk("漢字の名詞のオ段＋ウは ー（表）", "ひょー" in plain(to_aq("報告書の表1では")[0]), True)
    chk("カタカナ語はそのまま（ソウル）", "そうる" in plain(to_aq("ソウルの広場")[0]), True)
    chk("動詞はそのまま（追う）", "おう" in plain(to_aq("この動画で追う")[0]), True)
    s8, _, _ = to_aq("4月16日の朝。")
    chk("月と日は別の句（数字どうしだけまとめる）", "しがつ" in s8.split("/")[0] and "じゅー" not in s8.split("/")[0], True)
    print("aq_kana selftest:", "PASS" if ok else "🔴FAIL")
    return ok


def main():
    if "--selftest" in sys.argv:
        return 0 if selftest() else 1
    if "--sheet" in sys.argv:
        rows, n_dict, stale = sheet()
        nE = sum(len(r[6]) for r in rows)
        nW = sum(len(r[7]) for r in rows)
        for r in rows:
            for e in r[6]:
                print("🔴 E", e)
            for w in r[7]:
                print("⚠️ W", w)
        for lid in stale:
            print(f"🔴 E override.tsv の行ID {lid} は台本に無い（前の版のまま残っていないか）")
        n_ov = sum(1 for r in rows if r[5] == "override")
        print(f"行 {len(rows)}（手書き {n_ov}）・利用者辞書 {n_dict}語 → {ep_dir() / 'yomi_sheet.tsv'}")
        print(f"E {nE + len(stale)}件 / W {nW}件")
        return 1 if nE or stale else 0
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    load_userdict()
    s, E, W = to_aq(args[0])
    print(s)
    print("読み:", plain(s))
    for ms, acc, delim, words in phrases(args[0]):
        print(f"  {words:<12} {''.join(ms):<14} 核 {acc}  {delim or ''}")
    for e in E:
        print("🔴 E", e)
    for w in W:
        print("⚠️ W", w)
    return 1 if E else 0


if __name__ == "__main__":
    sys.exit(main())
