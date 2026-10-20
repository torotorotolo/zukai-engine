# -*- coding: utf-8 -*-
"""make_plan17.py — 17本目の章ファイル（tools/cuts/c1〜c9・ca・cb）の**骨組み PLAN** を作る（2026-10-20 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（23本目の `ref/ep23/make_plan23.py` を写して17本目の一覧の列と種類に替えた）。
  ① 了承②ずみの映像方針の一覧 `ref/ep17/eizou_build/list17.tsv`（`make_list17.py` の出力＝E 0・秒は narration.json の実測〈⑤b-1〉・
     扉は c109 のあと〈c110 の前〉と第2〜11章の頭・フリー素材と記録映像は素材の長さと倍率つき）＝種類・素材・見せ方・副題・動き・
     見る向き・見た目の型・合図・権利・出典の行・注・映像方針の新しい画
  ② 台本 第2版 `ref/ep17/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典` の**出典の欄だけ**（243カット・11章）
  🔴 **台本の画の欄は写さない**＝17本目の画の欄には撮影者の名前が入っている（④'・公開リポ）。一覧 list17.tsv も画の欄を持たない
     （make_list17 の注）。元の画は台本 §4 を読む
画面の種類（一覧 → PLAN の kind）：
  実写（この事故の写真・事故機・姉妹機・記録映像 V1・Googleアース）→ 写真／
  関連（事故そのものではない実物の写真＝同じ型の別の機体の操縦室・機関の建物・空港など＝副題で「イメージ」か「現在の〜」）→ 写真
     （フリー素材ではない＝出典つきの実物の写真。⚠️ 門番 check_text_screens の「写真」の数には入る＝20% の数〈この事故の写真〉は
      映像方針の 実写＋頁＝73 で見る。PLAN の plan の頭に「関連」と書く）／
  頁（報告書の付図・写真51 の頁・FAA・判決）→ 図・写真の頁（出どころの表の注に「文字の頁」があるものは 文字の頁）／
  イメージ（フリー素材）→ フリー素材／案C（再現イラスト）→ 再現イラスト／図 → 図解
書く前に照合する（違えば止まる）＝Vault の映像方針ノートの数：
  写真・実写（実写＋頁）73＝実写50・頁23（うち文字の頁6）・関連21・フリー素材14・案C 69・図66・文字だけ6・続く最長1・3カット以上続く所0・合計243

    python ref/ep17/make_plan17.py          # 照合して数を出すだけ（書かない）
    python ref/ep17/make_plan17.py --write  # 章ファイル11本を書く（🔴 17本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 一覧の秒は書き写さない＝絵は `audio/narration.json` の実測の秒で組む。映像（記録映像・フリー素材）の倍率（素材の秒÷扉を除いた
   カットの秒）だけは区間の長さを決める数なので plan に書く。
"""
import csv
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
LIST = HERE / "ref" / "ep17" / "eizou_build" / "list17.tsv"
SCRIPT = HERE / "ref" / "ep17" / "daihon_v2.md"
CUTS = HERE / "tools" / "cuts"
FROM_SHA = "b800dbdb"      # 23本目の章ファイルが残っている最後の版（git show <sha>:tools/cuts/c1.py）＝17本目 ⑤b-1 の移し替えの前の toro/main

N_CUTS = 243
# 🆕 2026-10-20（⑤b-4）：案C 場面9 前例の年表（c314・c901・c903・c921）と場面10 時間の帯（ca01・ca10・ca17）の7カットを図（軸の型 axis）へ
#    替えた（年表に「再現イラスト」の札は合わない・軸の型の門番 check_axis が点の位置を画素で照らす）＝illu 69→62・fig 66→73
WANT = dict(photo=71, real=50, rel=21, page=17, textpage=6, text=6, run=1, run3=0, stock=14, illu=62, fig=73)
KIND = {"実写": "写真", "関連": "写真", "頁": "図・写真の頁", "イメージ": "フリー素材", "案C": "再現イラスト", "図": "図解"}
TEXT = ("パネル", "決め所", "文字の頁")
CHAP = re.compile(r"^(つかみ|第\d+章)　?(.*?)（.*）$")
HEAD = re.compile(r"^\*\*(c[1-9ab]\d{2})\*\*(.*)$")
WANT_CH = ("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "ca", "cb")
TITLE = {"c1": "つかみ（c101〜c109）と第1章　画面に出ていた文字（c110〜c117）"}   # c1 の中に扉（c110 の前）＝ファイルは1本


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
    bits = ["関連（事故そのものではない実物の写真・20% の数に入れない）"] if r["kind"] == "関連" else []
    if r["code"]:
        bits.append(r["code"] + ((":" + r["part"]) if r["part"] else ""))
    if r["src_len"] and "頭の差し込み" in r["motion"]:     # 10-20 c101＝推奨 A（映像はカットの頭の k 行だけ・あとは写真）
        bits.append(f"映像の素材 {r['src_len']}秒・倍率 {float(r['rate']):.2f}（素材の秒÷頭の差し込みが画面に出る秒＝scene_jiko.head_secs と同じ式・"
                    f"1.0 未満は動きの欄の倍率で）")
    elif r["src_len"]:
        bits.append(f"映像の素材 {r['src_len']}秒・倍率 {float(r['rate']):.2f}（素材の秒÷扉を除いた中身の秒＝narration.json の実測・"
                    f"1.0 以上は等速で区間を選ぶ）")
    for k, lab in (("kind", "一覧の種類"), ("frame", "見せ方"), ("sub", "副題"), ("motion", "動き"), ("view", "見る向き"), ("look", "見た目の型"),
                   ("signal", "合図"), ("rights", "権利"), ("credit", "出典の行"), ("note", "注")):
        if r[k]:
            bits.append(f"{lab}：{r[k]}")
    if r["ga_new"]:
        bits.append("新しい画（映像方針）：" + r["ga_new"])
    if r["card"] and float(r["card"]) > 0:
        bits.append("このカットの前に章の扉")
    if r["star"]:
        bits.append("★決め所だった行（決め所の画面は作らない＝10-07）")
    bits.append("台本の画＝台本 §4（撮影者の名前があるので写さない）")
    return ("🔧 " if changed else "") + "｜".join(b.replace("\n", " ") for b in bits)


def build():
    rows = list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))
    src = sources()
    plan, title = OrderedDict(), OrderedDict()
    for r in rows:
        k = KIND.get(r["kind"])
        if k is None:
            raise SystemExit(f"🔴 {r['cid']}: 一覧の種類「{r['kind']}」の当て先が無い")
        if k == "図・写真の頁" and r["textpage"] == "1":
            k = "文字の頁"
        m = CHAP.match(r["chap"])
        if not m:
            raise SystemExit(f"🔴 {r['cid']}: 章の見出し「{r['chap']}」が読めない")
        title.setdefault(r["cid"][:2], TITLE.get(r["cid"][:2]) or (m.group(1) + ("　" + m.group(2) if m.group(2) else "")))
        plan[r["cid"]] = dict(kind=k, plan=plan_text(r, "🔧" in r["note"]), src=src.get(r["cid"], ""))
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
    got = dict(photo=cnt["写真"], real=lk["実写"], rel=lk["関連"], page=cnt["図・写真の頁"], textpage=cnt["文字の頁"], text=text,
               run=best, run3=run3, stock=cnt["フリー素材"], illu=cnt["再現イラスト"], fig=cnt["図解"])
    if got != WANT:
        errs.append(f"数が映像方針と違う: {got}（期待 {WANT}）")
    if lk["実写"] + lk["頁"] != 73:
        errs.append(f"写真・実写（実写＋頁）{lk['実写'] + lk['頁']}（映像方針 73）")
    return cnt, got, ch, errs


def write(plan, title):
    for name, ttl in title.items():
        cids = [c for c in plan if c.startswith(name)]
        f = CUTS / f"{name}.py"
        old = f.read_text(encoding="utf-8") if f.exists() else ""
        if "17本目（中華航空140便" in old and "\nSPEC = {}\n" not in old:
            raise SystemExit(f"🔴 {f} は17本目の SPEC が入っている（`SPEC = {{}}` の行が無い）＝上書きしない")
        # 17本目の章ファイルを PLAN だけ書き直すときは、`SPEC = {}` の行から後ろ（SPEC.update…＝書いた図）をそのまま残す（make_plan23 の型）
        keep = old.split("\nSPEC = {}\n", 1)[1] if "17本目（中華航空140便" in old else ""
        was = (f"■ 🔴 2026-10-20（⑤b-1）：23本目（三豊百貨店崩壊事故のリメイク）の中身を空にした＝git の `{FROM_SHA}`"
               f"（`git show {FROM_SHA}:tools/cuts/{name}.py`）。") if old else \
              "■ 🆕 2026-10-20（⑤b-1）：新しいファイル。"
        if keep:
            m = re.search(r"\n(■ 🔴 2026-10-20（⑤b-1）：23本目.*?。)\n", old)
            was = m.group(1) if m else was
        body = [
            "# -*- coding: utf-8 -*-",
            f'"""{ttl} {cids[0]}–{cids[-1]}（{len(cids)}カット）。17本目（中華航空140便墜落事故）。',
            "",
            was,
            "■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep17/make_plan17.py` で",
            "  映像方針の一覧 `ref/ep17/eizou_build/list17.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から",
            "  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（撮影者の名前がある＝元の画は台本 §4）。",
            "  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**",
            "     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。",
            "  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。",
            "  ⚠️ 「関連」と書いたカットは事故そのものではない実物の写真（種類は写真・20% の数〈この事故の写真〉には入れない）",
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
    print(f"写真 {got['photo']}（実写 {got['real']}＋関連 {got['rel']}）・図・写真の頁 {got['page']}・文字の頁 {got['textpage']}・"
          f"文字だけ {got['text']}＝{got['text'] / len(plan):.1%}・続く最長 {got['run']}・3連続 {got['run3']}・フリー素材 {got['stock']}・"
          f"再現イラスト {got['illu']}・図解 {got['fig']}・🔧替えた {sum(1 for c in plan if plan[c]['plan'].startswith('🔧'))}")
    if errs:
        for e in errs:
            print("🔴", e)
        sys.exit(1)
    print("✓ 映像方針の数と一致")
    if "--write" in sys.argv:
        write(plan, title)
