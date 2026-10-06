# -*- coding: utf-8 -*-
"""make_plan19.py — 19本目の章ファイル（tools/cuts/c1〜c9・ca・cb・cc）の**骨組み PLAN** を作る（2026-10-06 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（14〜18本目の `ref/ep1x/make_plan.py` と同じ役目）。
  ① 承認ずみの映像方針の一覧 `ref/ep19/eizou_build/list19.tsv`（`make_list19.py` の出力＝決め①〜⑩こみ・E0）
     ＝種類・素材と使う秒・差し込み・副題・権利・札・注
  ② 台本 第2版 `ref/ep19/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典` の出典（237カット・12の区切り）
画面の種類（一覧 → PLAN の kind）：
  実写 → 写真／図・図動 → 図解／再現 → 再現イラスト／頁 → 図・写真の頁／文字の頁 → 文字の頁／panel → パネル／
  quote → 決め所／フリー → フリー素材（この事故の写真に数えない＝ルール §2-5c）
  差し込み（頭・尻）は種類を変えない（一覧と同じ数え方＝20% に数えない）。
書く前に照合する（違えば止まる）＝映像方針ノート §1「決め⑩」・§2 の数：
  写真（この事故）66・文字だけ31・続く最長2・3カット以上続く所0・フリー素材8・合計237

    python ref/ep19/make_plan19.py          # 照合して数を出すだけ（書かない）
    python ref/ep19/make_plan19.py --write  # 章ファイル12本を書く（🔴 19本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 一覧の秒（÷365 の見込み）は書き写さない＝絵は `audio/narration.json` の実測の秒で組む（c105 の終わり 39.0秒）。
"""
import csv
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
LIST = HERE / "ref" / "ep19" / "eizou_build" / "list19.tsv"
SCRIPT = HERE / "ref" / "ep19" / "daihon_v2.md"
CUTS = HERE / "tools" / "cuts"
FROM_SHA = "b11797a"       # 18本目の章ファイルが残っている最後の版（git show <sha>:tools/cuts/c1.py）

N_CUTS = 237
WANT = dict(photo=66, text=31, run=2, run3=0, stock=8)
KIND = {"実写": "写真", "図": "図解", "図動": "図解", "再現": "再現イラスト", "頁": "図・写真の頁",
        "文字の頁": "文字の頁", "panel": "パネル", "quote": "決め所", "フリー": "フリー素材"}
KINDS = ("写真", "図・写真の頁", "再現イラスト", "図解", "混ざり", "文字の頁", "パネル", "決め所", "フリー素材")
TEXT = ("パネル", "決め所", "文字の頁")
# 台本の区切り（§4 の見出し）＝章ファイル。つかみ（c1）は章の印を出さない（scene_jiko.CHAPTERS に入れない）
TITLE = OrderedDict([
    ("c1", "つかみ"), ("c2", "第1章　海辺の12階建て"), ("c3", "第2章　25年前から見えていた"), ("c4", "第3章　29か月"),
    ("c5", "第4章　最後の3週間"), ("c6", "第5章　午前1時22分"), ("c7", "第6章　がれきの下で"),
    ("c8", "第7章　プールデッキから"), ("c9", "第8章　見えなかったもの"), ("ca", "第9章　塔へ渡り、西で止まった"),
    ("cb", "第10章　疑われたもの"), ("cc", "終章　その後"),
])
HEAD = re.compile(r"^\*\*(c[1-9a-c]\d{2})\*\*(.*)$")


def sources():
    """台本 §4 の見出し行の最後の欄（出典）。"""
    out = {}
    for ln in SCRIPT.read_text(encoding="utf-8").splitlines():
        m = HEAD.match(ln)
        if m:
            parts = [p.strip() for p in m.group(2).split(" ／ ")]
            out[m.group(1)] = parts[-1] if len(parts) >= 3 else ""
    return out


def plan_text(r):
    bits = [f"{r['main']}"]
    if r["ins_pos"]:
        bits.append(f"差し込み（{r['ins_pos']}）：{r['ins_k']} {r['ins_code']} {r['ins_rng']} {r['ins_secs']}秒 {r['ins_text']}".strip())
    if r["sub"]:
        bits.append(f"副題：{r['sub']}")
    if r["label"]:
        bits.append(f"札：{r['label']}")
    if r["rights"]:
        bits.append(f"権利：{r['rights']}")
    if r["note"]:
        bits.append(f"注：{r['note']}")
    return "｜".join(b.replace("\n", " ") for b in bits)


def build():
    rows = list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))
    src = sources()
    plan = OrderedDict()
    for r in rows:
        k = KIND.get(r["kind"])
        if k is None:
            raise SystemExit(f"🔴 {r['cid']}: 一覧の種類「{r['kind']}」の当て先が無い")
        plan[r["cid"]] = dict(kind=k, plan=plan_text(r), src=src.get(r["cid"], ""))
    return plan


def check(plan):
    errs = []
    if len(plan) != N_CUTS:
        errs.append(f"カット数 {len(plan)}（期待 {N_CUTS}）")
    nos = [c for c in plan if not plan[c]["src"]]
    if nos:
        errs.append(f"台本に出典の欄が無い: {nos[:8]}")
    ch = Counter(c[:2] for c in plan)
    if set(ch) != set(TITLE):
        errs.append(f"章の組が違う: {sorted(ch)}")
    kinds = [plan[c]["kind"] for c in plan]
    cnt = Counter(kinds)
    text = sum(cnt[k] for k in TEXT)
    run = best = run3 = 0
    for k in kinds:
        run = run + 1 if k in TEXT else 0
        best = max(best, run)
        if run == 3:
            run3 += 1
    got = dict(photo=cnt["写真"], text=text, run=best, run3=run3, stock=cnt["フリー素材"])
    if got != WANT:
        errs.append(f"数が映像方針と違う: {got}（期待 {WANT}）")
    return cnt, got, ch, errs


def write(plan):
    for name, title in TITLE.items():
        cids = [c for c in plan if c.startswith(name)]
        f = CUTS / f"{name}.py"
        if f.exists() and re.search(r"19本目（サーフサイド", f.read_text(encoding="utf-8")) and "SPEC = {}" not in f.read_text(encoding="utf-8"):
            raise SystemExit(f"🔴 {f} は19本目の SPEC が入っている＝上書きしない")
        body = [
            "# -*- coding: utf-8 -*-",
            f'"""{title} {cids[0]}–{cids[-1]}（{len(cids)}カット）。19本目（サーフサイドのマンション崩壊のリメイク）。',
            "",
            f"■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `{FROM_SHA}`（`git show {FROM_SHA}:tools/cuts/{name}.py`）。",
            "■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep19/make_plan19.py` で",
            "  映像方針の一覧 `ref/ep19/eizou_build/list19.tsv`（承認ずみ・決め①〜⑩）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。",
            "  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**",
            "     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」と「フリー素材」を数える）。",
            "  ⚠️ plan の「⑤b-1」は1秒1コマの走査で区間を選ぶ所・秒（÷365 の見込み）は書き写さない＝narration.json の実測で組む。",
            '"""',
            "import jiko_style as J  # noqa: F401",
            "import cuts.ss as ss  # noqa: F401",
            "",
            "P = ss.P",
            "",
            "PLAN = {",
        ]
        for c in cids:
            p = plan[c]
            body.append(f"    {c!r}: dict(kind={p['kind']!r},")
            body.append(f"               plan={p['plan']!r},")
            body.append(f"               src={p['src']!r}),")
        body += ["}", "", "SPEC = {}", ""]
        f.write_text("\n".join(body), encoding="utf-8", newline="\n")
        print(f"  書いた {f.relative_to(HERE)}（{len(cids)}カット）")


if __name__ == "__main__":
    plan = build()
    cnt, got, ch, errs = check(plan)
    print(f"カット {len(plan)}・章 {dict(ch)}")
    print(f"種類 {dict(cnt)}")
    print(f"写真（この事故）{got['photo']}＝{got['photo'] / len(plan):.1%}・文字だけ {got['text']}＝{got['text'] / len(plan):.1%}・"
          f"続く最長 {got['run']}・3連続 {got['run3']}・フリー素材 {got['stock']}")
    if errs:
        for e in errs:
            print("🔴", e)
        sys.exit(1)
    print("✓ 映像方針の数と一致")
    if "--write" in sys.argv:
        write(plan)
