# -*- coding: utf-8 -*-
"""make_plan24.py — 24本目の章ファイル（tools/cuts/c1〜c9・ca・cb・cc）の**骨組み PLAN** を作る（2026-10-22 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（17本目の `ref/ep17/make_plan17.py` を写して24本目の一覧の列と種類に替えた）。
  ① 了承②ずみの映像方針の一覧 `ref/ep24/eizou_build/list24.tsv`（`make_list24.py` の出力＝E 0・秒は narration.json の実測〈⑤b-1〉・
     扉は c2〜cc の頭の11枚・フリー素材は素材の長さと倍率つき）＝種類・素材・見せ方・副題・動き・見る向き・見た目の型・合図・
     権利・時期・人・出典の行・注・映像方針の新しい画
  ② 台本 第2版 `ref/ep24/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典` の**出典の欄だけ**（242カット・つかみ＋11章）
  🔴 **台本の画の欄は写さない**（17本目の型・narration.py の頭の注と同じ約束）＝元の画は台本 §4・一覧 `ref/ep24/eizou_list24.md`
画面の種類（一覧 → PLAN の kind）：
  実写（この発電所・この事故の写真と衛星写真）→ 写真／
  参考（同じ型のほかの発電所の炉＝副題で「同じ型の炉（〇〇原発）」と名乗る）→ 写真
     （フリー素材ではない＝出典つきの実物の写真。⚠️ 門番 check_text_screens の「写真」の数には入る＝20% の数〈この発電所・この事故の写真〉は
      映像方針の 実写＋頁＝99 で見る。PLAN の plan の頭に「関連（参考＝…）」と書く＝17本目の「関連」と同じ扱い＝門番の印 REL_MARK「関連（」で
      束の台帳 assets.json の related と照らされる）／
  頁（報告書・会議録の紙面）→ 図・写真の頁（一覧の見た目の型が「文字の頁…」は 文字の頁）／
  イメージ（フリー素材）→ フリー素材／文字だけ（パネル）→ パネル／案C（見た目の型に「案C」＝再現イラスト）→ 再現イラスト／
  ほかの図の型（模式・地図・年表・札・流れ・暦・時刻表・時計・棒・比べ・帯・並べ・箱）→ 図解
書く前に照合する（違えば止まる）＝Vault の映像方針ノートの数（了承②）：
  写真＋頁 99（写真 実写73・頁26＝図の頁14・文字の頁12）・参考9・フリー素材8・文字だけ13（パネル1・文字の頁12）・続く最長1・
  3カット以上続く所0・案C（再現イラスト）6・図解119（図126＝案C 6＋図解119＋パネル1）・合計242
  ⚠️ 案C の6＝台本 §7（承認①）の「案C1 炉の断面 c208・案C2 止める棒 c615／c905・案C3 出力の時刻表 c303／c403・案C4 避難のバス c707」。
     映像方針ノートは案C の数を書いていない＝初めは見た目の型の欄の4行（案C1・案C2×2・案C4）から 4 と見込んで止まった（時刻表の2行は
     種類が「時刻表」で見た目の型に「案C3」）＝台本の決めに合わせた（10-22 ⑤b-1）

    python ref/ep24/make_plan24.py          # 照合して数を出すだけ（書かない）
    python ref/ep24/make_plan24.py --write  # 章ファイル12本を書く（🔴 24本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 一覧の秒は書き写さない＝絵は `audio/narration.json` の実測の秒で組む。映像（フリー素材）の倍率（素材の秒÷扉を除いた
   カットの秒）だけは区間の長さを決める数なので plan に書く。
"""
import csv
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
LIST = HERE / "ref" / "ep24" / "eizou_build" / "list24.tsv"
SCRIPT = HERE / "ref" / "ep24" / "daihon_v2.md"
CUTS = HERE / "tools" / "cuts"
FROM_SHA = "2cc5e5ab"      # 17本目の章ファイルが残っている最後の版（git show <sha>:tools/cuts/c1.py）＝24本目 ⑤b-1 の移し替えの merge

N_CUTS = 242
WANT = dict(photo=82, real=73, ref=9, page=14, textpage=12, panel=1, text=13, run=1, run3=0, stock=8, illu=6, fig=119)
PIC = {"実写": "写真", "参考": "写真", "頁": "図・写真の頁", "イメージ": "フリー素材", "文字だけ": "パネル"}
TEXT = ("パネル", "決め所", "文字の頁")
CHAP = re.compile(r"^(つかみ|第\d+章)　?(.*?)（.*）$")
HEAD = re.compile(r"^\*\*(c[1-9a-c]\d{2})\*\*(.*)$")
WANT_CH = ("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "ca", "cb", "cc")
MARK = "24本目（チェルノブイリ原発事故"


def kind_of(r):
    if r["kind"] in PIC:
        k = PIC[r["kind"]]
        if k == "図・写真の頁" and r["look"].startswith("文字"):
            k = "文字の頁"
        return k
    if "案C" in r["look"]:
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
    # 頭の「関連（」＝門番 check_text_screens.REL_MARK（17本目 ⑤b-2 の「関連」の写真の札＝束の台帳 assets.json の related と照らす）。
    # 24本目の映像方針の種類は「参考」＝同じ扱い（事故そのものではない実物の写真・20% の数に入れない）なので、門番が読む印で書く
    bits = ["関連（参考＝同じ型〈RBMK〉のほかの発電所の炉の写真・20% の数に入れない）"] if r["kind"] == "参考" else []
    if r["code"]:
        bits.append(r["code"] + ((":" + r["part"]) if r["part"] else ""))
    if r["src_len"]:
        bits.append(f"映像の素材 {r['src_len']}秒・倍率 {float(r['rate']):.2f}（素材の秒÷扉を除いた中身の秒＝narration.json の実測・"
                    f"1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）")
    for k, lab in (("kind", "一覧の種類"), ("frame", "見せ方"), ("sub", "副題"), ("motion", "動き"), ("view", "見る向き"), ("look", "見た目の型"),
                   ("signal", "合図"), ("rights", "権利"), ("era", "時期"), ("people", "人"), ("credit", "出典の行"), ("note", "注")):
        if r[k]:
            bits.append(f"{lab}：{r[k]}")
    if r["ga_new"]:
        bits.append("新しい画（映像方針）：" + r["ga_new"])
    if r["card"] and float(r["card"]) > 0:
        bits.append("このカットの前に章の扉")
    bits.append("台本の画＝台本 §4・一覧 eizou_list24.md（写さない）")
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
    got = dict(photo=cnt["写真"], real=lk["実写"], ref=lk["参考"], page=cnt["図・写真の頁"], textpage=cnt["文字の頁"], panel=cnt["パネル"],
               text=text, run=best, run3=run3, stock=cnt["フリー素材"], illu=cnt["再現イラスト"], fig=cnt["図解"])
    if got != WANT:
        errs.append(f"数が映像方針と違う: {got}（期待 {WANT}）")
    if lk["実写"] + lk["頁"] != 99:
        errs.append(f"写真＋頁（実写＋頁）{lk['実写'] + lk['頁']}（映像方針 99）")
    return cnt, got, ch, errs


def write(plan, title):
    for name, ttl in title.items():
        cids = [c for c in plan if c.startswith(name)]
        f = CUTS / f"{name}.py"
        old = f.read_text(encoding="utf-8") if f.exists() else ""
        if MARK in old and "\nSPEC = {}\n" not in old:
            raise SystemExit(f"🔴 {f} は24本目の SPEC が入っている（`SPEC = {{}}` の行が無い）＝上書きしない")
        # 24本目の章ファイルを PLAN だけ書き直すときは、`SPEC = {}` の行から後ろ（SPEC.update…＝書いた図）をそのまま残す（make_plan17 の型）
        keep = old.split("\nSPEC = {}\n", 1)[1] if MARK in old else ""
        was = (f"■ 🔴 2026-10-22（⑤b-1）：17本目（中華航空140便墜落事故）の中身を空にした＝git の `{FROM_SHA}`"
               f"（`git show {FROM_SHA}:tools/cuts/{name}.py`）。") if (old and MARK not in old) else \
              "■ 🆕 2026-10-22（⑤b-1）：新しいファイル。"
        if keep:
            m = re.search(r"\n(■ (?:🔴|🆕) 2026-10-22（⑤b-1）：.*?。)\n", old)
            was = m.group(1) if m else was
        body = [
            "# -*- coding: utf-8 -*-",
            f'"""{ttl} {cids[0]}–{cids[-1]}（{len(cids)}カット）。{MARK}・1986-04-26）。',
            "",
            was,
            "■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep24/make_plan24.py` で",
            "  映像方針の一覧 `ref/ep24/eizou_build/list24.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から",
            "  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep24/eizou_list24.md`）。",
            "  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**",
            "     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。",
            "  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。",
            "  ⚠️ 「関連（参考＝…）」と書いたカットは同じ型のほかの発電所の炉の写真（種類は写真・20% の数〈この発電所・この事故の写真〉には入れない・",
            "     門番 check_text_screens が束の台帳 assets.json の related と照らす）",
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
    cnt, got, ch, errs = check(plan, title, rows)
    print(f"カット {len(plan)}・章 {dict(ch)}")
    print("章の見出し " + "／".join(f"{k}={v}" for k, v in title.items()))
    print(f"種類 {dict(cnt)}")
    print(f"写真 {got['photo']}（実写 {got['real']}＋参考 {got['ref']}）・図・写真の頁 {got['page']}・文字の頁 {got['textpage']}・パネル {got['panel']}・"
          f"文字だけ {got['text']}＝{got['text'] / len(plan):.1%}・続く最長 {got['run']}・3連続 {got['run3']}・フリー素材 {got['stock']}・"
          f"再現イラスト {got['illu']}・図解 {got['fig']}・🔧替えた {sum(1 for c in plan if plan[c]['plan'].startswith('🔧'))}")
    if errs:
        for e in errs:
            print("🔴", e)
        sys.exit(1)
    print("✓ 映像方針の数と一致")
    if "--write" in sys.argv:
        write(plan, title)
