# -*- coding: utf-8 -*-
"""make_plan20.py — 20本目の章ファイル（tools/cuts/c1〜c9・ca・cb・cc）の**骨組み PLAN** を作る（2026-10-08 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（14〜19本目の `ref/ep1x/make_plan*.py` と同じ役目・形は19本目の make_plan19.py）。
  ① 了承②ずみの映像方針の一覧 `ref/ep20/eizou_build/list20.tsv`（`make_list20.py` の出力＝E 0・秒と倍率は narration.json の実測）
     ＝種類・素材・映像の倍率・副題・写真の動き・見る向き・合図・権利・出典の行・注・台本の画の欄
  ② 台本 第2版 `ref/ep20/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典` の出典（234カット・12の区切り）
画面の種類（一覧 → PLAN の kind）：
  実写 → 写真／模式 → 図解／再現 → 再現イラスト／頁 → 図・写真の頁／文字の頁 → 文字の頁
  （20本目は決め所・パネル・フリー素材が無い＝決め所の画面は作らない〈10-07〉・フリー素材は使わない〈映像方針〉）
書く前に照合する（違えば止まる）＝映像方針ノート §3 の数：
  写真・実写（この事故）63・文字だけ6・続く最長1・3カット以上続く所0・フリー素材0・合計234
🔴 映像方針で台本の画の欄から替えたカット（assign20.tsv）は「台本の画」が元の予定のまま＝plan の頭に🔧と「替えた」を出す。

    python ref/ep20/make_plan20.py          # 照合して数を出すだけ（書かない）
    python ref/ep20/make_plan20.py --write  # 章ファイル12本を書く（🔴 20本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 一覧の秒は書き写さない＝絵は `audio/narration.json` の実測の秒で組む（c106 の終わり 44.8秒・c108 の終わり 61.5秒）。
   映像の倍率だけは素材の区間の長さを決める数なので plan に書く（0.6 未満は止め絵＝make_list20.py が E で止める）。
"""
import csv
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
LIST = HERE / "ref" / "ep20" / "eizou_build" / "list20.tsv"
ASSIGN = HERE / "ref" / "ep20" / "eizou_build" / "assign20.tsv"
SCRIPT = HERE / "ref" / "ep20" / "daihon_v2.md"
CUTS = HERE / "tools" / "cuts"
FROM_SHA = "0dcaa9c"       # 19本目の章ファイルが残っている最後の版（git show <sha>:tools/cuts/c1.py）

N_CUTS = 234
WANT = dict(photo=63, text=6, run=1, run3=0, stock=0)
KIND = {"実写": "写真", "模式": "図解", "再現": "再現イラスト", "頁": "図・写真の頁", "文字の頁": "文字の頁"}
TEXT = ("パネル", "決め所", "文字の頁")
CHAP = re.compile(r"^(つかみ|第\d+章|終章)　?(.*?)（\d+カット）$")
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


def assigned():
    lines = [ln for ln in ASSIGN.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    return {r["cid"] for r in csv.DictReader(lines, delimiter="\t")}


def plan_text(r, changed):
    bits = [r["main"]]
    if r["speed"]:
        bits.append(f"倍率 {r['speed']}（素材の秒÷扉を除いた中身の秒＝narration.json の実測）")
    for k, lab in (("sub", "副題"), ("motion", "動き"), ("view", "見る向き"), ("signal", "合図"),
                   ("rights", "権利"), ("credit", "出典の行"), ("note", "注")):
        if r[k]:
            bits.append(f"{lab}：{r[k]}")
    bits.append(("台本の画（🔧映像方針で替えた＝元の予定）：" if changed else "台本の画：") + r["ga"])
    return ("🔧 " if changed else "") + "｜".join(b.replace("\n", " ") for b in bits)


def build():
    rows = list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))
    src = sources()
    chg = assigned()
    plan, title = OrderedDict(), OrderedDict()
    for r in rows:
        k = KIND.get(r["kind"])
        if k is None:
            raise SystemExit(f"🔴 {r['cid']}: 一覧の種類「{r['kind']}」の当て先が無い")
        m = CHAP.match(r["chap"])
        if not m:
            raise SystemExit(f"🔴 {r['cid']}: 章の見出し「{r['chap']}」が読めない")
        title.setdefault(r["cid"][:2], (m.group(1) + ("　" + m.group(2) if m.group(2) else "")))
        plan[r["cid"]] = dict(kind=k, plan=plan_text(r, r["cid"] in chg), src=src.get(r["cid"], ""))
    return plan, title


def check(plan, title):
    errs = []
    if len(plan) != N_CUTS:
        errs.append(f"カット数 {len(plan)}（期待 {N_CUTS}）")
    nos = [c for c in plan if not plan[c]["src"]]
    if nos:
        errs.append(f"台本に出典の欄が無い: {nos[:8]}")
    ch = Counter(c[:2] for c in plan)
    want_ch = ("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "ca", "cb", "cc")
    if tuple(title) != want_ch or set(ch) != set(want_ch):
        errs.append(f"章の組が違う: {list(title)}")
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


def write(plan, title):
    for name, ttl in title.items():
        cids = [c for c in plan if c.startswith(name)]
        f = CUTS / f"{name}.py"
        old = f.read_text(encoding="utf-8") if f.exists() else ""
        if "20本目（日本航空123便" in old and "SPEC = {}" not in old:
            raise SystemExit(f"🔴 {f} は20本目の SPEC が入っている＝上書きしない")
        body = [
            "# -*- coding: utf-8 -*-",
            f'"""{ttl} {cids[0]}–{cids[-1]}（{len(cids)}カット）。20本目（日本航空123便のリメイク）。',
            "",
            f"■ 🔴 2026-10-08（⑤b-1）：19本目（サーフサイドのマンション崩壊のリメイク）の中身を空にした＝git の `{FROM_SHA}`"
            f"（`git show {FROM_SHA}:tools/cuts/{name}.py`）。",
            "■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep20/make_plan20.py` で",
            "  映像方針の一覧 `ref/ep20/eizou_build/list20.tsv`（了承②ずみ・E 0）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。",
            "  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**",
            "     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。",
            "  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット（台本の画は元の予定）。",
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
    plan, title = build()
    cnt, got, ch, errs = check(plan, title)
    print(f"カット {len(plan)}・章 {dict(ch)}")
    print("章の見出し " + "／".join(f"{k}={v}" for k, v in title.items()))
    print(f"種類 {dict(cnt)}")
    print(f"写真（この事故）{got['photo']}＝{got['photo'] / len(plan):.1%}・文字だけ {got['text']}＝{got['text'] / len(plan):.1%}・"
          f"続く最長 {got['run']}・3連続 {got['run3']}・フリー素材 {got['stock']}・🔧替えた {sum(1 for c in plan if plan[c]['plan'].startswith('🔧'))}")
    if errs:
        for e in errs:
            print("🔴", e)
        sys.exit(1)
    print("✓ 映像方針の数と一致")
    if "--write" in sys.argv:
        write(plan, title)
