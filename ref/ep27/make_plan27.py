# -*- coding: utf-8 -*-
"""make_plan27.py — 27本目の章ファイル（tools/cuts/c1〜c7）の**骨組み PLAN** を作る（2026-10-30 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（26本目の `ref/ep26/make_plan26.py` を写して27本目の一覧の列と種類に替えた）。
  ① 了承②ずみの映像方針の一覧＝`ref/ep27/eizou_build/make_list27.py` の `build()`（E 0・秒は narration.json の実測〈⑤b-1〉・扉は c201〜c701 の頭の6枚・
     県警の動画は区間と止め）＝種類・素材・地・見せ方・副題・動き・見た目の型・注・印・映像方針の新しい画＋出どころの表 `sources27.psv` の権利・時期・人・出典の行
     （27本目の `list27.tsv` には章と権利の列が無い＝道具を直に呼ぶ）
  ② 台本 第2版 `ref/ep27/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典` の**出典の欄だけ**（107カット・つかみ＋6章）
  🔴 **台本の画の欄は写さない**（17・24〜26本目の型・narration.py の頭の注と同じ約束）＝元の画は台本 §4・一覧 `ref/ep27/eizou_list27.md`
画面の種類（一覧 → PLAN の kind）：
  実写（この事件の Commons の写真）・引用（県警・警察庁の映像と画像＝額装・無加工・話している秒だけ）→ 写真／
  イメージ（Pexels のフリー素材の写真）→ フリー素材／
  衛星（Google の衛星写真＋描き足しの地図＝26本目と同じ扱い）・模式ほかの図の型・SNS のカード → 図解（地はすべて CC BY・CC0 の写真を暗くするだけ）／
  文字だけ → パネル（27本目は0）
書く前に照合する（違えば止まる）＝期待値は**決めた紙の数**（24本目 ⑤b-1 の落とし穴＝見た目の型の欄から数えない）：
  Vault の映像方針の引き継ぎ §1-1（了承②）＝「107カット・この事件の写真と映像 60（56.1%＝実写 49・引用 11）・衛星写真 9・イメージ 4・
  図 34（地はすべて写真）・文字だけ 0」・§2-3＝県警の動画 YT-A 5区間・YT-C 1区間。
  → 写真 60（引用 11・うち県警の動画 6）・フリー素材 4・図解＝衛星 9＋図 34＝43（SNS のカード 3）・文字の頁 0・パネル 0・再現イラスト 0

    python -P ref/ep27/make_plan27.py          # 照合して数を出すだけ（書かない）
    python -P ref/ep27/make_plan27.py --write  # 章ファイル7本を書く（🔴 27本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 一覧の秒は書き写さない＝絵は `audio/narration.json` の実測の秒で組む。県警の動画の区間と止めだけは区間の長さを決める数なので plan に書く
   （区間＋止め ≧ 扉を除いた中身の秒＝`make_list27.py` の門番）。
⚠️ 26本目の章ファイルは11本（c1〜c9・ca・cb）・27本目は7本（c1〜c7）＝c8・c9・ca・cb は `git rm`（26本目は git の `54b15e5e`）・`CHAPTER_FILES` から外す。
"""
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
SCRIPT = HERE / "ref" / "ep27" / "daihon_v2.md"
CUTS = HERE / "tools" / "cuts"
FROM_SHA = "54b15e5e"      # 26本目の章ファイルが残っている最後の版（git show <sha>:tools/cuts/c1.py）＝27本目 ⑤b-1 の移し替えの merge
sys.path.insert(0, str(HERE / "ref" / "ep27" / "eizou_build"))
import make_list27 as ML  # noqa: E402

N_CUTS = 107
WANT = dict(photo=60, real=49, quote=11, police_video=6, stock=4, fig=43, sat=9, figs_paper=34, sns=3, textpage=0, panel=0, illu=0, text=0)
PIC = {"実写": "写真", "引用": "写真", "イメージ": "フリー素材", "文字だけ": "パネル"}
TEXT = ("パネル", "決め所", "文字の頁")
CHAP = re.compile(r"^(つかみ|第\d+章)　?(.*?)（.*）$")
HEAD = re.compile(r"^\*\*(c[1-7]\d{2})\*\*(.*)$")
WANT_CH = ("c1", "c2", "c3", "c4", "c5", "c6", "c7")
MARK = "27本目（八田與一容疑者の事件"


def kind_of(r):
    return PIC.get(r["kind"], "図解")


def sources():
    """台本 §4 の見出し行の最後の欄（出典）。画の欄（真ん中）は読まない。"""
    out = {}
    for ln in SCRIPT.read_text(encoding="utf-8").splitlines():
        m = HEAD.match(ln)
        if m:
            parts = [p.strip() for p in m.group(2).split(" ／ ")]
            out[m.group(1)] = parts[-1] if len(parts) >= 3 else ""
    return out


def plan_text(r, s, changed):
    bits = []
    if r["main"]:
        bits.append(r["main"])
    if r["ji"]:
        bits.append(f"地：{r['ji']}（暗くするだけ・字と地の比 8:1 が下限＝了承② 決め1・色は原本）")
    vw = ML.video_window(r["motion"]) if r["kind"] == "引用" else None
    if vw:
        bits.append(f"県警の動画の区間 {vw[0]:.1f}〜{vw[1]:.1f}秒＋止め {vw[2]:.1f}秒（扉を除いた中身 {r['cont']:.2f}秒＝narration.json の実測・"
                    f"実時間で流す＝速さを変えない・音は使わない＝-an・「犯人」の字の秒 BAD にかけない）")
    for k, lab in (("kind", "一覧の種類"), ("frame", "見せ方"), ("sub", "副題"), ("motion", "動き"), ("look", "見た目の型"), ("mark", "印")):
        if r.get(k):
            bits.append(f"{lab}：{r[k]}")
    if s:
        for k, lab in (("rights", "権利"), ("era", "時期"), ("people", "人"), ("credit", "出典の行")):
            if s.get(k):
                bits.append(f"{lab}：{s[k]}")
    if r.get("note"):
        bits.append("注：" + r["note"])
    if r["ga_new"] and r["ga_new"] != "台本どおり":
        bits.append("新しい画（映像方針）：" + r["ga_new"])
    if r["frame"].startswith("額装"):
        bits.append("🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）")
    if r["kind"] == "引用":
        bits.append("🔴 引用＝加工しない・話している秒だけ・サムネに使わない（ルール §B2-10 ③）")
    if r["card"] and float(r["card"]) > 0:
        bits.append("このカットの前に章の扉")
    bits.append("台本の画＝台本 §4・一覧 eizou_list27.md（写さない）")
    return ("🔧 " if changed else "") + "｜".join(str(b).replace("\n", " ") for b in bits)


def build():
    res = ML.build()
    if res["E"]:
        raise SystemExit(f"🔴 一覧の門番が E {len(res['E'])}（先に make_list27.py を E 0 に）: {res['E'][:2]}")
    if res["tnote"] != "audio/narration.json の実測":
        raise SystemExit(f"🔴 一覧の秒が実測でない（{res['tnote']}）")
    rows, S = res["rows"], res["S"]
    src = sources()
    plan, title = OrderedDict(), OrderedDict()
    for r in rows:
        m = CHAP.match(r["chap"])
        if not m:
            raise SystemExit(f"🔴 {r['cid']}: 章の見出し「{r['chap']}」が読めない")
        title.setdefault(r["cid"][:2], m.group(1) + ("　" + m.group(2) if m.group(2) else ""))
        changed = r["ga_new"] not in ("", "台本どおり")
        s = S.get(ML.base(r["main"])) if r["main"] else None
        plan[r["cid"]] = dict(kind=kind_of(r), plan=plan_text(r, s, changed), src=src.get(r["cid"], ""))
    return plan, title, rows, S


def check(plan, title, rows, S):
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
    run = best = 0
    for k in kinds:
        run = run + 1 if k in TEXT else 0
        best = max(best, run)
    pv = sum(1 for r in rows if r["kind"] == "引用" and S.get(ML.base(r["main"]), {}).get("type") == "police-video")
    got = dict(photo=cnt["写真"], real=lk["実写"], quote=lk["引用"], police_video=pv, stock=cnt["フリー素材"], fig=cnt["図解"], sat=lk["衛星"],
               figs_paper=sum(v for k, v in lk.items() if k in ML.FIGS), sns=lk["SNS"], textpage=cnt["文字の頁"], panel=cnt["パネル"],
               illu=cnt["再現イラスト"], text=text)
    if got != WANT:
        errs.append(f"数が映像方針（了承②）と違う: {got}（期待 {WANT}）")
    if best > 0:
        errs.append(f"文字だけの画面の続く最長 {best}（映像方針は 0）")
    return cnt, got, ch, best, errs


def write(plan, title):
    for name, ttl in title.items():
        cids = [c for c in plan if c.startswith(name)]
        f = CUTS / f"{name}.py"
        old = f.read_text(encoding="utf-8") if f.exists() else ""
        if MARK in old and "\nSPEC = {}\n" not in old:
            raise SystemExit(f"🔴 {f} は27本目の SPEC が入っている（`SPEC = {{}}` の行が無い）＝上書きしない")
        # 27本目の章ファイルを PLAN だけ書き直すときは、`SPEC = {}` の行から後ろ（SPEC.update…＝書いた図）をそのまま残す（make_plan26 の型）
        keep = old.split("\nSPEC = {}\n", 1)[1] if MARK in old else ""
        was = (f"■ 🔴 2026-10-30（⑤b-1）：26本目（タイタニック号沈没事故）の中身を空にした＝git の `{FROM_SHA}`"
               f"（`git show {FROM_SHA}:tools/cuts/{name}.py`）。") if (old and MARK not in old) else \
              "■ 🆕 2026-10-30（⑤b-1）：新しいファイル。"
        if MARK in old:
            m = re.search(r"\n(■ (?:🔴|🆕) 2026-10-30（⑤b-1）：.*?。)\n", old)
            was = m.group(1) if m else was
        body = [
            "# -*- coding: utf-8 -*-",
            f'"""{ttl} {cids[0]}–{cids[-1]}（{len(cids)}カット）。{MARK}・2022-06-29・大分県別府市）。',
            "",
            was,
            "■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep27/make_plan27.py` で",
            "  映像方針の一覧（`ref/ep27/eizou_build/make_list27.py`＝了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から",
            "  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep27/eizou_list27.md`）。",
            "  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**",
            "     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。",
            "  🔴 額装・帯の写真は静止（`build_jiko.FRAME_STILL_EP` に ep27）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。",
            "  🔴 県警・警察庁の素材は引用（額装・加工しない・話している秒だけ・「犯人」の字の秒にかけない）。説明カットの地は CC BY・CC0 の写真を暗くするだけ（8:1）。",
            "  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。",
            "  ⚠️ 人＝被害者・遺族・けがをした人・目撃者・SNS の投稿者の名前は書かない・容疑者は必ず「八田與一容疑者」（ルール §B2-10）。",
            "     CC BY の写真で顔が分かる人は顔だけモザイク・BY-SA は遠い人と後ろ姿だけ（⑤b で原寸）",
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
    plan, title, rows, S = build()
    cnt, got, ch, best, errs = check(plan, title, rows, S)
    print(f"カット {len(plan)}・章 {dict(ch)}")
    print("章の見出し " + "／".join(f"{k}={v}" for k, v in title.items()))
    print(f"種類 {dict(cnt)}")
    print(f"写真 {got['photo']}（実写 {got['real']}・引用 {got['quote']}＝うち県警の動画 {got['police_video']}）・フリー素材 {got['stock']}・"
          f"図解 {got['fig']}（衛星 {got['sat']}・図 {got['figs_paper']}＝SNS のカード {got['sns']}）・文字の頁 {got['textpage']}・パネル {got['panel']}・"
          f"文字だけ {got['text']}・再現イラスト {got['illu']}・🔧替えた {sum(1 for c in plan if plan[c]['plan'].startswith('🔧'))}")
    if errs:
        for e in errs:
            print("🔴", e)
        sys.exit(1)
    print("✓ 映像方針（了承②）の数と一致")
    if "--write" in sys.argv:
        write(plan, title)
