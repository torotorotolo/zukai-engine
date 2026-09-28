# -*- coding: utf-8 -*-
"""make_plan.py — 14本目の章ファイル（tools/cuts/c1〜c9・ca〜cd）の**骨組み PLAN** を作る（2026-09-28 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2〜⑤b-7 で書く。
**手で写さない**：3つの正本から機械で組む。
  ① 台本 `ref/ep14/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典`（195カット）
  ② 承認ずみの絵コンテ Vault `事故検証-14本目-映像方針-案Cと競合の画面-20260926.md` §4-1・§4-2（案C の画と動き・人・出典）
     ＋ §2-2 の動く模式図（断面F・地図 drift）のカット
  ③ 追補 Vault `事故検証-14本目-映像方針-追補-文字の画面-20260926.md` §4（替える74カット＋断面F の具体化2＝76行の「変えたあと」）
     ＋ §7 の申し送り（カットごとの注意）
画面の種類（kind）は Vault `Resources/事故検証ch-案C見本/count_text_screens.py` の preset `ep14add`（追補で承認＝34/195・最長2）と
**同じ関数**で決める（数え直しの道具と同じ答えになることを、書く前にここで照合する＝違えば止まる）。

    python ref/ep14/make_plan.py          # 照合して数を出すだけ（書かない）
    python ref/ep14/make_plan.py --write  # 章ファイル 13本を書く（🔴 SPEC が空でない章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
"""
import importlib.util
import re
import sys
from collections import OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
SCRIPT = HERE / "ref" / "ep14" / "daihon_v2.md"
VAULT = Path(r"C:\Users\konar\Documents\Obsidian Vault")
POLICY = VAULT / "Projects" / "事故検証-14本目-映像方針-案Cと競合の画面-20260926.md"
ADDENDUM = VAULT / "Projects" / "事故検証-14本目-映像方針-追補-文字の画面-20260926.md"
COUNTER = VAULT / "Resources" / "事故検証ch-案C見本" / "count_text_screens.py"
CUTS = HERE / "tools" / "cuts"

KINDS = ("写真", "図・写真の頁", "再現イラスト", "図解", "混ざり", "文字の頁", "パネル", "決め所")
TEXT = ("パネル", "決め所", "文字の頁")
CHAPTER_OF = {"c1": 1, "c2": 2, "c3": 3, "c4": 4, "c5": 5, "c6": 6, "c7": 7, "c8": 8, "c9": 9,
              "ca": 10, "cb": 11, "cc": 12, "cd": 13}

# 承認ずみ §2-2 の動く模式図（案B の延長・通常の ⑤b）。追補 §4 に行があるカットは追補が勝つ
F_CUTS = "c401 c402 c403 c404 c405 c502 c503 c504 c505 c506 c613 c712 c815 c914".split()
F_CUTS = [c for c in F_CUTS if c not in ("c505",)]          # c505 は決め所（§2-2 の「c502〜c506」の中の決め所は除く）
MAP_CUTS = "c111 c604 c605 c606 c607 c608 c609 c610 c611 c812".split()

# 追補 §7 の申し送り（カットごと）。plan の末尾に「⚠️」で足す
NOTES = {
    "c702": "⚠️ 人の数は判決の原文で照合（甲板部8人が操舵室＝c712・c911 と合うか）。合わなければ人を描かない（追補 §7-2）",
    "c813": "⚠️ 人の数は判決の原文で照合（甲板部8人が操舵室＝c712・c911 と合うか）。合わなければ人を描かない（追補 §7-2）",
    "c916": "⚠️ D（123艇の場面）を試す＝救助された5人を描かずに成り立つか。成り立てば kind を再現イラストへ（追補 §7-3）",
    "cc04": "⚠️ 海審 p1083 は見出しで選んだ＝原寸で見て語り（航跡と模擬）に合うか。合わなければ c609 の図8の頁を戻す（追補 §7-4）。出典は「海審 p1083・p1091〜1092」（§7-5）",
    "cc10": "⚠️ 出典は「裁決 p2088〜2089」（写真は p2089・追補 §7-5）",
    "c109": "⚠️ 候補＝海審 p1015（〔그림1〕2014-04-15 インチョン港・〔그림2〕事故のときの船）に替える＝原寸で見て私人の顔が無ければ（追補 §7-6）",
    "c204": "⚠️ 人の形＝顔の無い同じ形を1つ＝1人で476個（生徒325・先生14・一般104・船で働く人33〈船員15・係8・ほか10〉）。描いた形の数を描く側と同じ関数で数えて記録と照合。亡くなった方の数には使わない（追補 §7-7・ルール §C-1 #59）",
    "c205": "⚠️ 人の形は c204 と同じ並び（追補 §7-7）",
    "c206": "⚠️ 人の形は c204 と同じ並び（追補 §7-7）",
}
for _c in "cb02 cb04 cb08 cb09 cb12 cb13 cb14".split():
    NOTES[_c] = "⚠️ 流れ図は役職名だけ（名前は出さない）・人の影と顔を使わない・罪名と刑は箱の中の文字で（追補 §7-8）"


def load_counter():
    spec = importlib.util.spec_from_file_location("count_text_screens", COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def md_rows(path, start_pat, stop_pat):
    """見出し start_pat から stop_pat の手前までの表の行（`|` で割った列）を返す。"""
    lines = path.read_text(encoding="utf-8").split("\n")
    s = next(i for i, ln in enumerate(lines) if re.match(start_pat, ln))
    e = next((i for i in range(s + 1, len(lines)) if re.match(stop_pat, lines[i])), len(lines))
    out = []
    for ln in lines[s:e]:
        if not ln.startswith("|") or set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        cols = [c.strip() for c in ln.strip().strip("|").split("|")]
        m = re.match(r"`?(c[0-9a-d]\d{2})`?", cols[0])
        if m:
            out.append((m.group(1), cols))
    return out


def clean(s):
    return re.sub(r"\s+", " ", s.replace("**", "")).strip()


def build():
    ct = load_counter()
    cuts = ct.parse(str(SCRIPT))
    if len(cuts) != 195:
        raise SystemExit(f"🔴 台本のカットが {len(cuts)}（195 のはず）")
    # 画と出典は「 ／ 」（前後に空白）で割る。⚠️ 画の中に空白の無い「／」がある（c105「傾いたきっかけ／なぜ…」）
    #   ＝数え直しの道具の parse（最初の「／」で割る）は画の欄を途中で切る＝種類の判定には効かないが、ここでは使わない
    src, pic = {}, {}
    for ln in SCRIPT.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^\*\*(c[0-9a-z]\d{2})\*\*", ln)
        if m:
            parts = ln.split(" ／ ")
            pic[m.group(1)], src[m.group(1)] = clean(parts[1]), clean(" ／ ".join(parts[2:]))
    if set(pic) != set(cuts):
        raise SystemExit(f"🔴 見出し行の読み方が2つで食い違う: {sorted(set(pic) ^ set(cuts))}")
    over, tp = ct.PRESETS["ep14add"]
    kind = {k: over.get(k, ct.base(k, c["pic"], tp)) for k, c in cuts.items()}
    bad = {k: v for k, v in kind.items() if v not in KINDS}
    if bad:
        raise SystemExit(f"🔴 種類が決まらないカット: {bad}")

    plan = {k: "台本の画：" + pic[k] for k in cuts}
    # ⚠️ §2-2 の範囲の書き方はゆるい（「c604〜c611」に決め所 c607・図の頁 c609・写真 c611 が入る）
    #    ＝種類が図解のカットにだけ付ける（決め所・頁・写真・案C は §4 と台本の画のまま）
    for k in F_CUTS:
        if kind[k] == "図解":
            plan[k] = "【F】断面F（承認ずみ §2-2＝動く模式図）｜台本の画：" + pic[k]
    for k in MAP_CUTS:
        if kind[k] == "図解":
            plan[k] = "【地図】drift（承認ずみ §2-2＝動く地図）｜台本の画：" + pic[k]
    # 承認ずみ §4-1（冒頭）：カット（秒）｜台本｜いまの画｜案C の画と動き｜人｜出典
    for k, cols in md_rows(POLICY, r"^### 4-1\.", r"^### 4-2\."):
        plan[k] = f"【案C】{clean(cols[3])}｜人：{clean(cols[4])}｜rec：{clean(cols[5])}"
    # 承認ずみ §4-2（第6〜9章）：カット｜台本の要点｜案C の画と動き｜人｜⚠️
    for k, cols in md_rows(POLICY, r"^### 4-2\.", r"^## 5\."):
        plan[k] = f"【案C】{clean(cols[2])}｜人：{clean(cols[3])}" + (f"｜⚠️ {clean(cols[4])}" if clean(cols[4]) not in ("", "—") else "")
    # 追補 §4：カット｜台本（要点）｜いまの画｜変えたあと｜理由（最も新しい＝勝つ）
    n_add = 0
    for k, cols in md_rows(ADDENDUM, r"^## 4\.", r"^## 5\."):
        plan[k] = f"{clean(cols[3])}（追補 §4）"
        n_add += 1
    for k, v in NOTES.items():
        plan[k] += "｜" + v
    unknown = sorted(set(plan) - set(cuts))
    if unknown:
        raise SystemExit(f"🔴 台本に無いカット: {unknown}")
    return cuts, kind, plan, src, n_add


def count(ids, kind):
    """数え直しの道具と同じ数え方（文字だけの数・続く最長・3カット以上続く所）。"""
    tc = sum(kind[k] in TEXT for k in ids)
    run = best = runs = 0
    for k in ids:
        if kind[k] in TEXT:
            run += 1
            best = max(best, run)
        else:
            runs += run >= 3
            run = 0
    runs += run >= 3
    return tc, best, runs


def chapter_file(ch, ids, kind, plan, src, name, n):
    rows = "\n".join(f'    "{k}": dict(kind={kind[k]!r},\n'
                     f'               plan={plan[k]!r},\n'
                     f'               src={src.get(k, "")!r}),' for k in ids)
    return f'''# -*- coding: utf-8 -*-
"""第{n}章　{name} {ids[0]}–{ids[-1]}（{len(ids)}カット）。14本目（セウォル号）。

■ 🔴 2026-09-28（⑤b-1）：13本目（トルコ航空981便）の中身を空にした＝git の `b54ee4f`（`git show b54ee4f:tools/cuts/{ch}.py`）。
  ⚠️ 第10〜13章（ca〜cd）は14本目で初めてのファイル（13本目までは9章）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep14/make_plan.py` で
  台本 §4・承認ずみの絵コンテ（映像方針 §2-2・§4）・追補 §4・§7 から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2〜⑤b-7 で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝⑤b-7 の門番 check_text_screens が「文字だけ2割まで・3カット以上続けない」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所（ルール §5b-79）
  記号＝【案C】再現イラスト（置き場 A〜E）・【F】断面F・【地図】drift・【年表】【帯】【棒】【マス】【人の形】【書類】【流れ】【並べ】（追補 §3）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {{
{rows}
}}

SPEC = {{
}}
'''


def main(write=False):
    cuts, kind, plan, src, n_add = build()
    ids = list(cuts)
    tc, best, runs = count(ids, kind)
    ct = load_counter()
    ratio, best_ct = ct.report(cuts, ct.PRESETS["ep14add"][0], ct.PRESETS["ep14add"][1], "照合：count_text_screens ep14add")
    print(f"■ PLAN：195カット・追補の行 {n_add}・文字だけ {tc}（{tc / 195 * 100:.1f}%）・続く最長 {best}・3カット以上続く所 {runs}")
    from collections import Counter
    print("  種類: " + "・".join(f"{k} {v}" for k, v in Counter(kind.values()).most_common()))
    if (tc, best) != (round(ratio * 195), best_ct) or (tc, best, runs) != (34, 2, 0):
        raise SystemExit(f"🔴 数え直しの道具と合わない（PLAN {tc}・{best}・{runs} ／ 道具 {round(ratio * 195)}・{best_ct}）")
    print("✓ 数え直しの道具（追補で承認＝34・最長2・3連続0）と同じ")
    # 章名＝台本 §4 の `### 第N章　名前（Nカット）`（`（` の手前まで）
    names = {}
    for ln in SCRIPT.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^###\s*第(\d+)章[　\s]+(.+?)（\d+カット）", ln)
        if m:
            names[int(m.group(1))] = m.group(2).strip()
    if len(names) != 13:
        raise SystemExit(f"🔴 台本の章見出しが {len(names)}（13 のはず）")
    groups = OrderedDict()
    for k in ids:
        groups.setdefault(k[:2], []).append(k)
    if list(groups) != list(CHAPTER_OF):
        raise SystemExit(f"🔴 章の並びが違う: {list(groups)}")
    for ch, cids in groups.items():
        n = CHAPTER_OF[ch]
        print(f"  {ch}.py 第{n}章　{names[n]}　{cids[0]}–{cids[-1]}（{len(cids)}）"
              f" 文字だけ {sum(kind[k] in TEXT for k in cids)}")
    if not write:
        print("（書いていない。書くなら --write）")
        return
    for ch, cids in groups.items():
        p = CUTS / f"{ch}.py"
        if p.exists():
            old = p.read_text(encoding="utf-8")
            m = re.search(r"^SPEC = \{(.*?)^\}", old, re.S | re.M)
            if "14本目（セウォル号）" in old and m and m.group(1).strip() and "--force" not in sys.argv:
                print(f"  ⚠️ {ch}.py は14本目の SPEC が入っている＝上書きしない（--force で上書き）")
                continue
        p.write_text(chapter_file(ch, cids, kind, plan, src, names[CHAPTER_OF[ch]], CHAPTER_OF[ch]),
                     encoding="utf-8", newline="\n")
        print(f"  ✓ 書いた {p.relative_to(HERE)}")


if __name__ == "__main__":
    main("--write" in sys.argv)
