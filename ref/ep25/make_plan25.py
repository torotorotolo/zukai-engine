# -*- coding: utf-8 -*-
"""make_plan25.py — 25本目の章ファイル（tools/cuts/c1〜c9・ca・cb）の**骨組み PLAN** を作る（2026-10-25 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（24本目の `ref/ep24/make_plan24.py` を写して25本目の一覧の列と種類に替えた）。
  ① 了承②ずみの映像方針の一覧 `ref/ep25/eizou_build/list25.tsv`（`make_list25.py` の出力＝E 0・秒は narration.json の実測〈⑤b-1〉・
     扉は c201〜cb01 の頭の10枚・フリー素材は素材の長さと倍率〈素材は未取得＝⑤b で取ってから〉）＝種類・素材・見せ方・副題・動き・見る向き・
     見た目の型・合図・権利・時期・人・出典の行・注・映像方針の新しい画
  ② 台本 第2版 `ref/ep25/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典` の**出典の欄だけ**（242カット・つかみ＋10章）
  🔴 **台本の画の欄は写さない**（24本目・17本目の型・narration.py の頭の注と同じ約束）＝元の画は台本 §4・一覧 `ref/ep25/eizou_list25.md`
画面の種類（一覧 → PLAN の kind）：
  実写（この事故の写真・事故の現場の今の写真・衛星写真と空中写真＝全面の衛星写真 c101・c328・ca23・cb03 を含む）→ 写真／
  頁（報告書・発表・判決・建議の紙面と図の頁）→ 図・写真の頁（一覧の見た目の型が「文字の頁…」は 文字の頁）／
  イメージ（フリー素材）→ フリー素材／文字だけ（パネル）→ パネル（25本目は0）／
  案C-A〜案C-F（一覧の種類が「案C」で始まる＝再現イラスト）→ 再現イラスト／
  ほかの図の型（模式・地図〈c517＝衛星写真に線を描き足す〉・路線・年表・札・流れ・暦・時刻表・時計・棒・比べ・並べ・箱）→ 図解
  （17本目の衛星写真の地図 c727・c804 ほかも 図解＝同じ扱い）
書く前に照合する（違えば止まる）＝期待値は**決めた紙の数**（24本目 ⑤b-1 の落とし穴＝見た目の型の欄から数えない）：
  Vault の映像方針ノート §1（了承②）＝写真68・頁46（うち文字の頁18＝「文字だけ（文字の頁）18（7.4%）・3つ続く所 0」）・フリー素材18・
  模式78・図110（＝写真・頁・イメージ・文字だけでない画）・合計242／台本 第2版 §7 の案C（再現イラスト）＝「A 曲線と速度（c301・c317）・
  B ブレーキの段（c304・c318）・C 交信の流れ（c306・c314）・D ATS の照査（c703・c719）・E 付け替えの前後（c603）・F 宝塚の分岐器（c207）
  ＝6場面すべて」＝10カット。→ 図・写真の頁＝46−18＝28・図解＝110−10＝100・パネル0
  ⚠️ 続く最長（文字の頁が続く数）は紙に数が無い＝「3つ続く所 0」だけを照らす（2 以下）

    python ref/ep25/make_plan25.py          # 照合して数を出すだけ（書かない）
    python ref/ep25/make_plan25.py --write  # 章ファイル11本を書く（🔴 25本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 一覧の秒は書き写さない＝絵は `audio/narration.json` の実測の秒で組む。映像（フリー素材）の倍率（素材の秒÷扉を除いた
   カットの秒）だけは区間の長さを決める数なので plan に書く（25本目は素材が未取得＝⑤b で取って `make_list25.py` を回し直してから）。
⚠️ 24本目の章ファイル cc.py は25本目に無い（つかみ＋10章）＝この道具は消さない（`git rm tools/cuts/cc.py` と `CHAPTER_FILES` は手で）。
"""
import csv
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
LIST = HERE / "ref" / "ep25" / "eizou_build" / "list25.tsv"
SCRIPT = HERE / "ref" / "ep25" / "daihon_v2.md"
CUTS = HERE / "tools" / "cuts"
FROM_SHA = "7ae693a1"      # 24本目の章ファイルが残っている最後の版（git show <sha>:tools/cuts/c1.py）＝25本目 ⑤b-1 の移し替えの merge

N_CUTS = 242
WANT = dict(photo=68, page=28, textpage=18, panel=0, text=18, run3=0, stock=18, illu=10, fig=100, model=78, figs_all=110)
PIC = {"実写": "写真", "頁": "図・写真の頁", "イメージ": "フリー素材", "文字だけ": "パネル"}
TEXT = ("パネル", "決め所", "文字の頁")
CHAP = re.compile(r"^(つかみ|第\d+章)　?(.*?)（.*）$")
HEAD = re.compile(r"^\*\*(c[1-9ab]\d{2})\*\*(.*)$")
WANT_CH = ("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "ca", "cb")
MARK = "25本目（JR福知山線脱線事故"


def kind_of(r):
    if r["kind"] in PIC:
        k = PIC[r["kind"]]
        if k == "図・写真の頁" and r["look"].startswith("文字"):
            k = "文字の頁"
        return k
    if r["kind"].startswith("案C"):
        return "再現イラスト"
    return "図解"


def sources():
    """台本 §4 の見出し行の最後の欄（出典）。画の欄（真ん中）は読まない。"""
    out = {}
    for ln in SCRIPT.read_text(encoding="utf-8").splitlines():
        m = HEAD.match(ln)
        if m:
            parts = [p.strip() for p in m.group(2).split(" ／ ")]
            out[m.group(1)] = parts[-1] if len(parts) >= 3 else ""
    return out


def plan_text(r, changed):
    bits = []
    if r["code"]:
        bits.append(r["code"] + ((":" + r["part"]) if r["part"] else ""))
    if r["src_len"]:
        bits.append(f"映像の素材 {r['src_len']}秒・倍率 {float(r['rate']):.2f}（素材の秒÷扉を除いた中身の秒＝narration.json の実測・"
                    f"1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）")
    elif r["kind"] == "イメージ":
        bits.append(f"映像の素材は未取得（⑤b で1本ずつ原寸で見てから取る・要る秒＝扉を除いた中身 {float(r['cont']):.2f}秒＝narration.json の実測）")
    for k, lab in (("kind", "一覧の種類"), ("frame", "見せ方"), ("sub", "副題"), ("motion", "動き"), ("view", "見る向き"), ("look", "見た目の型"),
                   ("signal", "合図"), ("rights", "権利"), ("era", "時期"), ("people", "人"), ("credit", "出典の行"), ("note", "注")):
        if r[k]:
            bits.append(f"{lab}：{r[k]}")
    if r["ga_new"] and r["ga_new"] != "台本どおり":
        bits.append("新しい画（映像方針）：" + r["ga_new"])
    if r["card"] and float(r["card"]) > 0:
        bits.append("このカットの前に章の扉")
    bits.append("台本の画＝台本 §4・一覧 eizou_list25.md（写さない）")
    return ("🔧 " if changed else "") + "｜".join(b.replace("\n", " ") for b in bits)


def build():
    rows = list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))
    src = sources()
    plan, title = OrderedDict(), OrderedDict()
    for r in rows:
        m = CHAP.match(r["chap"])
        if not m:
            raise SystemExit(f"🔴 {r['cid']}: 章の見出し「{r['chap']}」が読めない")
        title.setdefault(r["cid"][:2], m.group(1) + ("　" + m.group(2) if m.group(2) else ""))
        changed = "🔧" in r["note"] or "🔧" in r["ga_new"]
        plan[r["cid"]] = dict(kind=kind_of(r), plan=plan_text(r, changed), src=src.get(r["cid"], ""))
    return plan, title, rows


def check(plan, title, rows):
    errs = []
    if len(plan) != N_CUTS:
        errs.append(f"カット数 {len(plan)}（期待 {N_CUTS}）")
    nos = [c for c in plan if not plan[c]["src"]]
    if nos:
        errs.append(f"台本に出典の欄が無い: {nos[:8]}")
    ch = Counter(c[:2] for c in plan)
    if tuple(title) != WANT_CH or set(ch) != set(WANT_CH):
        errs.append(f"章の組が違う: {list(title)}")
    kinds = [plan[c]["kind"] for c in plan]
    cnt = Counter(kinds)
    lk = Counter(r["kind"] for r in rows)
    text = sum(cnt[k] for k in TEXT)
    run = best = run3 = 0
    for k in kinds:
        run = run + 1 if k in TEXT else 0
        best = max(best, run)
        if run == 3:
            run3 += 1
    got = dict(photo=cnt["写真"], page=cnt["図・写真の頁"], textpage=cnt["文字の頁"], panel=cnt["パネル"], text=text, run3=run3,
               stock=cnt["フリー素材"], illu=cnt["再現イラスト"], fig=cnt["図解"], model=lk["模式"],
               figs_all=sum(v for k, v in lk.items() if k not in ("実写", "頁", "イメージ", "文字だけ")))
    if got != WANT:
        errs.append(f"数が映像方針・台本 §7 と違う: {got}（期待 {WANT}）")
    if lk["実写"] + lk["頁"] != 114:
        errs.append(f"写真＋頁（実写＋頁）{lk['実写'] + lk['頁']}（映像方針 68＋46＝114）")
    illu = sorted(c for c in plan if plan[c]["kind"] == "再現イラスト")
    want_illu = ["c207", "c301", "c304", "c306", "c314", "c317", "c318", "c603", "c703", "c719"]
    if illu != want_illu:
        errs.append(f"再現イラストのカットが台本 §7 と違う: {illu}（期待 {want_illu}）")
    return cnt, got, ch, best, errs


def write(plan, title):
    for name, ttl in title.items():
        cids = [c for c in plan if c.startswith(name)]
        f = CUTS / f"{name}.py"
        old = f.read_text(encoding="utf-8") if f.exists() else ""
        if MARK in old and "\nSPEC = {}\n" not in old:
            raise SystemExit(f"🔴 {f} は25本目の SPEC が入っている（`SPEC = {{}}` の行が無い）＝上書きしない")
        # 25本目の章ファイルを PLAN だけ書き直すときは、`SPEC = {}` の行から後ろ（SPEC.update…＝書いた図）をそのまま残す（make_plan24 の型）
        keep = old.split("\nSPEC = {}\n", 1)[1] if MARK in old else ""
        was = (f"■ 🔴 2026-10-25（⑤b-1）：24本目（チェルノブイリ原発事故）の中身を空にした＝git の `{FROM_SHA}`"
               f"（`git show {FROM_SHA}:tools/cuts/{name}.py`）。") if (old and MARK not in old) else \
              "■ 🆕 2026-10-25（⑤b-1）：新しいファイル。"
        if keep:
            m = re.search(r"\n(■ (?:🔴|🆕) 2026-10-25（⑤b-1）：.*?。)\n", old)
            was = m.group(1) if m else was
        body = [
            "# -*- coding: utf-8 -*-",
            f'"""{ttl} {cids[0]}–{cids[-1]}（{len(cids)}カット）。{MARK}・2005-04-25）。',
            "",
            was,
            "■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep25/make_plan25.py` で",
            "  映像方針の一覧 `ref/ep25/eizou_build/list25.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から",
            "  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep25/eizou_list25.md`）。",
            "  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**",
            "     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。",
            "  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。",
            "  ⚠️ 人は役職だけ（①の承認）。名前の載る頁は注の「⚠️ …名前＝切り出しの外」のとおり寄る範囲から名前を外す",
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
        f.write_text("\n".join(body) + keep, encoding="utf-8", newline="\n")
        print(f"  書いた {f.relative_to(HERE)}（{len(cids)}カット{'・SPEC の部分 %d 字を残した' % len(keep) if keep else ''}）")


if __name__ == "__main__":
    plan, title, rows = build()
    cnt, got, ch, best, errs = check(plan, title, rows)
    print(f"カット {len(plan)}・章 {dict(ch)}")
    print("章の見出し " + "／".join(f"{k}={v}" for k, v in title.items()))
    print(f"種類 {dict(cnt)}")
    print(f"写真 {got['photo']}・図・写真の頁 {got['page']}・文字の頁 {got['textpage']}・パネル {got['panel']}・"
          f"文字だけ {got['text']}＝{got['text'] / len(plan):.1%}・続く最長 {best}・3連続 {got['run3']}・フリー素材 {got['stock']}・"
          f"再現イラスト {got['illu']}・図解 {got['fig']}（模式 {got['model']}）・🔧替えた {sum(1 for c in plan if plan[c]['plan'].startswith('🔧'))}")
    if errs:
        for e in errs:
            print("🔴", e)
        sys.exit(1)
    print("✓ 映像方針・台本 §7 の数と一致")
    if "--write" in sys.argv:
        write(plan, title)
