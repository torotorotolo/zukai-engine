# -*- coding: utf-8 -*-
"""22本目 タイタン号（リメイク）⑤a-1：台本第2版 §4 を tools/narration.py の SCRIPT へ**機械で**写す（2026-10-14）。

  python ref/ep22/script_copy.py          … 写して、写した結果を import し直して突き合わせる
  python ref/ep22/script_copy.py --check  … 写さずに突き合わせだけ（食い違いがあれば exit 1）

21本目の `ref/ep21/script_copy.py` を写した（20本目・19本目・18本目・16本目・15本目・14本目・13本目の `qa_out/ep13_script_copy.py` が元）。変えたのは2点:
  ① 台本の md ＝ `ref/ep22/daihon_v2.md`（第2版・10-14 承認①＝`228653e`・md5 f391543f…〈LF〉）
  ② 期待値（236カット／540行／14,904字／決め所0・聞き役67＝⑤a-1 の頭で check_script を自分で回した値。字は印を除く）
  最後のカット cd09 の問いは承認ずみ（10-14 承認①＝C「あなたは、もし乗れるとしたら、深い海の底を自分の目で見てみたいですか。」）
  🔴 c207 の〈CEOの名前〉は、写すときに**名前に置き換える**（2026-10-14 ⑤a-1 カズヤくん「リポに名前を入れる」＝名前は SCRIPT
     〈声と字幕〉と読み一覧にだけ。台本 md と設計図は置き場のまま）。置き換えの表は tools/el_script.py の MD_SUBS（md と SCRIPT の
     突き合わせ md_vs_script と同じ表）＝ここでは import せず、ファイルの字から ast で読む（写す前の SCRIPT で el_script を
     読み込まない）。字は md の14,904＋3＝14,907
以下は14本目の注のまま:
  ③ 🔴 **聞き役の印 `Q: ` を付けたまま写す**（話者の正本は SCRIPT。外すのは使う側が tools/speaker.py を通して）。
     `check_script.clean()` は 14本目⑤aから印も外すので、そのまま写すと**話者が消える**＝印だけ付け直す
共通エンディング（ed01）を残す仕組みは13本目のまま（いまの SCRIPT から字面のまま切り出して末尾へ戻す）。

🔴 切り方は check_script.py の parse / clean を**そのまま呼ぶ**（物差しを2か所に持たない）。
⚠️ 台本の文言の正本は、ここから先は narration.SCRIPT（字幕も音もここから作る）。
"""
import importlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import check_script as CSC  # noqa: E402
import speaker  # noqa: E402

MD = ROOT / "ref" / "ep22" / "daihon_v2.md"
NARR = ROOT / "tools" / "narration.py"
WANT = {"cuts": 236, "lines": 540, "chars": 14907, "quotes": 0, "q_lines": 67}   # 字＝md 14,904＋名前の置き換え +3


def md_subs(slug="ep22"):
    """tools/el_script.py の MD_SUBS[slug]（md の置き場 → SCRIPT の語）を、import せずにファイルの字から読む。"""
    import ast
    tree = ast.parse((ROOT / "tools" / "el_script.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "MD_SUBS" for t in node.targets):
            return ast.literal_eval(node.value).get(slug, {})
    raise SystemExit("🔴 tools/el_script.py に MD_SUBS が無い（置き場を名前に置き換えられない）")


SUBS = md_subs()
assert SUBS, "🔴 MD_SUBS['ep22'] が空"


def sub(t):
    for a, b in SUBS.items():
        t = t.replace(a, b)
    return t
TAIL = ("ed01",)            # el_script.COMMON_TAIL と同じ（el_script は narration を import するのでここでは読まない）
TAIL_MARK = "    # ── 共通エンディング"


def from_md():
    text = MD.read_text(encoding="utf-8")
    cuts = CSC.parse(text)
    # 章の見出し（§4 の中の ### 行）を、次に来るカットIDに結びつける
    heads, on, pending = {}, False, None
    for raw in text.split("\n"):
        line = raw.rstrip()
        if line.startswith("## 4. 台本"):
            on = True
            continue
        if on and re.match(r"^## \d", line):
            break
        if not on:
            continue
        if line.startswith("### "):
            pending = line[4:].strip()
            continue
        m = CSC.CUT_RE.match(line)
        if m and pending:
            heads[m.group(1)] = pending
            pending = None
    nq = sum(1 for _, _, ls in cuts if any(CSC.STAR_RE.match(l) for l in ls))
    # 🔴 聞き役の行だけ印を付け直す（clean は★・**・印を外す）・置き場を名前に（SUBS）
    out = [(cid, pic, [(speaker.Q_MARK if speaker.is_q(l) else "") + sub(CSC.clean(l)) for l in ls])
           for cid, pic, ls in cuts]
    # 置き場は台本に1回ずつ（〈CEOの名前〉＝c207 の1回）＝多くても少なくても止める
    for a in SUBS:
        n = sum(CSC.clean(l).count(a) for _, _, ls in cuts for l in ls)
        assert n == 1, f"🔴 置き場「{a}」が台本に {n}回（1回のはず）"
    return out, heads, nq


def block(cuts, heads, tail_src):
    q = lambda s: json.dumps(s, ensure_ascii=False)  # noqa: E731  Python の文字列リテラルとしても正しい
    rows = ["SCRIPT = ["]
    for cid, pic, ls in cuts:
        if cid in heads:
            rows.append(f"    # ── {heads[cid]} ────────────")
        rows.append(f"    # {cid} ／ {pic}")
        pad = " " * (len(f'    ("{cid}", ['))
        body = f"    ({q(cid)}, [" + q(ls[0])
        for l in ls[1:]:
            body += ",\n" + pad + q(l)
        rows.append(body + "]),")
    return "\n".join(rows) + "\n" + tail_src + "]\n"


def compare(cuts, nq, tail_want):
    sys.modules.pop("narration", None)
    import narration
    importlib.reload(narration)
    allgot = [(cid, [t.strip() for t in ls]) for cid, ls in narration.SCRIPT]
    got = [(c, ls) for c, ls in allgot if c not in TAIL]
    tail_got = [(c, ls) for c, ls in allgot if c in TAIL]
    want = [(cid, ls) for cid, _, ls in cuts]
    bad = []
    if [c for c, _ in allgot[-len(TAIL):]] != list(TAIL):
        bad.append(f"末尾が共通エンディング {TAIL} でない: {[c for c, _ in allgot[-3:]]}")
    if tail_got != tail_want:
        bad.append(f"共通エンディングの行が変わった: {tail_got!r} ／ 元 {tail_want!r}")
    if len(got) != len(want):
        bad.append(f"カット数 SCRIPT {len(got)} ／ md {len(want)}")
    for (gc, gl), (wc, wl) in zip(got, want):
        if gc != wc or gl != wl:
            bad.append(f"{wc}: SCRIPT {gc} {gl!r} ／ md {wl!r}")
    n_lines = sum(len(ls) for _, ls in got)
    n_chars = sum(len(speaker.bare(t)) for _, ls in got for t in ls)       # 印は数えない
    n_q = sum(1 for _, ls in got for t in ls if speaker.is_q(t))
    print(f"SCRIPT: {len(got)}カット／{n_lines}行（うち聞き役 {n_q}）／{n_chars}字（印を除く・md の決め所 {nq}）"
          f"＋共通エンディング {len(tail_got)}カット")
    real = {"cuts": len(got), "lines": n_lines, "chars": n_chars, "quotes": nq, "q_lines": n_q}
    if real != WANT:
        bad.append(f"数が第2版の実測と違う: {real} ／ 期待 {WANT}")
    if bad:
        print("🔴 食い違い:\n  " + "\n  ".join(bad[:20]))
        return 1
    print(f"✓ md と SCRIPT は1文字も違わない（{WANT['cuts']}／{WANT['lines']}／{WANT['chars']:,}／{WANT['quotes']}"
          f"・聞き役{WANT['q_lines']}）・ed01 は元のまま")
    return 0


def main():
    cuts, heads, nq = from_md()
    import narration
    tail_want = [(cid, [t.strip() for t in ls]) for cid, ls in narration.SCRIPT if cid in TAIL]
    if len(tail_want) != len(TAIL):
        print(f"🔴 いまの SCRIPT に共通エンディング {TAIL} が無い（{len(tail_want)}件）。止める")
        return 1
    if "--check" not in sys.argv:
        src = NARR.read_text(encoding="utf-8")
        a = src.index("\nSCRIPT = [\n") + 1
        b = src.index("\n]\n", a) + 3          # SCRIPT の閉じ括弧の行まで
        assert src[b:].lstrip("\n").startswith("GAP = "), "SCRIPT の直後が GAP でない（切る位置を誤っている）"
        body = src[a:b]
        t = body.index(TAIL_MARK)               # 共通エンディングの見出しコメントから
        tail_src = body[t:body.rindex("]")]     # 閉じ括弧の手前まで（字面のまま）
        assert all(f'("{c}"' in tail_src for c in TAIL), "共通エンディングの切り出しに ed01 が無い"
        NARR.write_text(src[:a] + block(cuts, heads, tail_src) + src[b:], encoding="utf-8")
        print(f"写した: {NARR.name}（章の見出し {len(heads)}件・共通エンディングを末尾に戻した）")
    return compare(cuts, nq, tail_want)


if __name__ == "__main__":
    sys.exit(main())
