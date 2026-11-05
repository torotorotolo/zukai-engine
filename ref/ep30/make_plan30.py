# -*- coding: utf-8 -*-
"""make_plan30.py — 30本目の章ファイル（tools/cuts/c1〜c9・ca〜cc）の**骨組み PLAN** を作る（2026-11-05 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（29本目の `ref/ep29/make_plan29.py` を写して30本目の数と注に替えた）。
  ① 了承②ずみの映像方針の一覧＝`ref/ep30/eizou_build/make_list30.py` の入力と門番（E 0・秒は narration.json の実測〈⑤b-1〉・扉は c201〜cc01 の頭の12枚）＝
     種類・素材・地・見せ方・副題・動き・見た目の型・注・印・映像方針の新しい画＋出どころの表 `sources30.psv` の権利・時期・人・出典の行
     （30本目の `list30.tsv` には権利の列が無い＝道具を直に呼ぶ）
  ② 台本 第2版 `ref/ep30/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典` の**出典の欄だけ**（238カット・つかみ＋12章）
  🔴 **台本の画の欄は写さない**（17・24〜29本目の型・narration.py の頭の注と同じ約束）＝元の画は台本 §4・一覧 `ref/ep30/eizou_list30.md`
画面の種類（一覧 → PLAN の kind）：
  陸自・引用・映像（防衛省の記録 M6）・公立＝この事件の写真と映像／場所（語りに出る場所の写真）・公的（公的な機関の紙面＝額装）→ 写真／
  イメージ（Pexels のフリー素材＝⑤b で1本ずつ）→ フリー素材／
  衛星（Google の衛星写真＋描き足しの地図＝27本目と同じ扱い）・札・模式・無線帯・言葉ほかの図の型 → 図解（地はすべて PDL1.0・CC BY・CC0・PD・Pexels の写真を暗くするだけ）／
  文字だけ → パネル（30本目は0）
書く前に照合する（違えば止まる）＝期待値は**決めた紙の数**（24本目 ⑤b-1 の落とし穴＝見た目の型の欄から数えない）：
  Vault の映像方針の引き継ぎ §1-1（了承②）＝「237カット・この事件の写真と映像 49＝陸自 20・引用 20・映像 6・公立 3／実写の全部 77＝＋紙面 7・衛星 12・語りに出る場所 9／
  イメージ 31・図 129（札の型 76・模式 20・言葉 11・無線帯 8・ほか 14）・文字だけ 0」＋⑤a-2 で足した c108（場所）＝238カット・場所 10。
  → 写真 66（陸自 20・引用 20・映像 6・公立 3・公的 7・場所 10）・フリー素材 31・図解 141（衛星 12＋図 129）・文字の頁 0・パネル 0・再現イラスト 0

    python -P ref/ep30/make_plan30.py          # 照合して数を出すだけ（書かない）
    python -P ref/ep30/make_plan30.py --write  # 章ファイル12本を書く（🔴 30本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 一覧の秒は書き写さない＝絵は `audio/narration.json` の実測の秒で組む。
⚠️ 29本目の章ファイルは7本（c1〜c7）＝c8・c9・ca・cb・cc は新しいファイル（29本目の中身は git の `dc72dd8a`）。
"""
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
SCRIPT = HERE / "ref" / "ep30" / "daihon_v2.md"
CUTS = HERE / "tools" / "cuts"
FROM_SHA = "dc72dd8a"      # 29本目の章ファイルが残っている最後の版（git show <sha>:tools/cuts/c1.py）＝30本目 ⑤b-1 の移し替えの merge
sys.path.insert(0, str(HERE / "ref" / "ep30" / "eizou_build"))
import make_list30 as ML  # noqa: E402

N_CUTS = 238
WANT = dict(photo=66, gsdf=20, quote=20, video=6, koritsu=3, public=7, place=10, stock=31, fig=141, sat=12, card=76, drawn=20, radio=8, words=11,
            textpage=0, panel=0, illu=0, text=0)
PIC = {"陸自": "写真", "引用": "写真", "映像": "写真", "公立": "写真", "場所": "写真", "公的": "写真", "イメージ": "フリー素材", "文字だけ": "パネル"}
TEXT = ("パネル", "決め所", "文字の頁")
CHAP = re.compile(r"^(つかみ|第\d+章)　?(.*?)（.*）$")
HEAD = re.compile(r"^\*\*(c[0-9a-c]\d{2})\*\*(.*)$")
WANT_CH = ("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "ca", "cb", "cc")
MARK = "30本目（地下鉄サリン事件"


def kind_of(a):
    return PIC.get(a["kind"], "図解")


def sources():
    """台本 §4 の見出し行の最後の欄（出典）。画の欄（真ん中）は読まない。"""
    out = {}
    for ln in SCRIPT.read_text(encoding="utf-8").splitlines():
        m = HEAD.match(ln)
        if m:
            parts = [p.strip() for p in m.group(2).split(" ／ ")]
            out[m.group(1)] = parts[-1] if len(parts) >= 3 else ""
    return out


def plan_text(a, s, changed):
    bits = []
    if a["main"]:
        bits.append(a["main"])
    if a["ji"]:
        bits.append(f"地：{a['ji']}（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）")
    for k, lab in (("kind", "一覧の種類"), ("frame", "見せ方"), ("sub", "副題"), ("motion", "動き"), ("look", "見た目の型"), ("mark", "印")):
        if a.get(k) and a[k] != "—":
            bits.append(f"{lab}：{a[k]}")
    if s:
        for k, lab in (("rights", "権利"), ("era", "時期"), ("people", "人"), ("credit", "出典の行")):
            if s.get(k):
                bits.append(f"{lab}：{s[k]}")
    if a.get("note"):
        bits.append("注：" + a["note"])
    if a["ga_new"] and a["ga_new"] != "台本どおり":
        bits.append("新しい画（映像方針）：" + a["ga_new"])
    if a["frame"].startswith("額装"):
        bits.append("🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし")
    if a["kind"] == "引用":
        bits.append("🔴 引用＝加工しない・話している秒だけ・本編だけ・サムネに使わない・出典の行に提供（ルール §2-39・§B2-12）")
    if a["kind"] == "公的":
        bits.append("🔴 公的な機関の紙面＝規約を読んでから・額装・無加工・🔴 名前の行と線の行を入れない＝親が絵を見て切る（台本 §0-4）")
    if a["kind"] == "映像":
        bits.append("🔴 防衛省の記録＝音は使わない（-an）・等速・上下を切って全面・秒は make_list30 の門番（使える秒の内）")
    if a["kind"] == "イメージ":
        bits.append("🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・等速が基本・音は使わない（-an）")
    bits.append("台本の画＝台本 §4・一覧 eizou_list30.md（写さない）")
    return ("🔧 " if changed else "") + "｜".join(str(b).replace("\n", " ") for b in bits)


def build():
    cuts = ML.read_cuts(ML.DAIHON)
    tnote = ML.measured(cuts)
    orows, obad = ML.load_psv(ML.OVER, ML.KEYS)
    srows, sbad = ML.load_psv(ML.SOURCES, ML.SKEYS)
    S = {r["code"]: r for r in srows}
    A, abad = ML.assemble(cuts, orows)
    ML.stock_rows(A, S)
    E, W = ML.gates(cuts, A, S, ML.words(ML.NAME_FILE), ML.words(ML.LINE_FILE))
    E = obad + sbad + abad + E
    ML.gate_video(cuts, A, S, E, W)
    if E:
        raise SystemExit(f"🔴 一覧の門番が E {len(E)}（先に make_list30.py を E 0 に）: {E[:2]}")
    if tnote != "audio/narration.json の実測":
        raise SystemExit(f"🔴 一覧の秒が実測でない（{tnote}）")
    src = sources()
    plan, title = OrderedDict(), OrderedDict()
    for c in cuts:
        cid, a = c["cid"], A[c["cid"]]
        m = CHAP.match(c["chap"])
        if not m:
            raise SystemExit(f"🔴 {cid}: 章の見出し「{c['chap']}」が読めない")
        title.setdefault(cid[:2], m.group(1) + ("　" + m.group(2) if m.group(2) else ""))
        s = S.get(ML.base(a["main"])) if a["main"] else None
        plan[cid] = dict(kind=kind_of(a), plan=plan_text(a, s, a["ga_new"].startswith("🔧")), src=src.get(cid, ""))
    return plan, title, cuts, A


def check(plan, title, cuts, A):
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
    lk = Counter(A[c["cid"]]["kind"] for c in cuts)
    text = sum(cnt[k] for k in TEXT)
    run = best = 0
    for k in kinds:
        run = run + 1 if k in TEXT else 0
        best = max(best, run)
    got = dict(photo=cnt["写真"], gsdf=lk["陸自"], quote=lk["引用"], video=lk["映像"], koritsu=lk["公立"], public=lk["公的"], place=lk["場所"],
               stock=cnt["フリー素材"], fig=cnt["図解"], sat=lk["衛星"], card=lk["札"], drawn=lk["模式"], radio=lk["無線帯"], words=lk["言葉"],
               textpage=cnt["文字の頁"], panel=cnt["パネル"], illu=cnt["再現イラスト"], text=text)
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
            raise SystemExit(f"🔴 {f} は30本目の SPEC が入っている（`SPEC = {{}}` の行が無い）＝上書きしない")
        # 30本目の章ファイルを PLAN だけ書き直すときは、`SPEC = {}` の行から後ろ（SPEC.update…＝書いた図）をそのまま残す（make_plan28 の型）
        keep = old.split("\nSPEC = {}\n", 1)[1] if MARK in old else ""
        was = (f"■ 🔴 2026-11-05（⑤b-1）：29本目（GMO不正アクセス問題）の中身を空にした＝git の `{FROM_SHA}`"
               f"（`git show {FROM_SHA}:tools/cuts/{name}.py`）。") if (old and MARK not in old) else \
              "■ 🆕 2026-11-05（⑤b-1）：新しいファイル。"
        if MARK in old:
            m = re.search(r"\n(■ (?:🔴|🆕) 2026-11-05（⑤b-1）：.*?。)\n", old)
            was = m.group(1) if m else was
        body = [
            "# -*- coding: utf-8 -*-",
            f'"""{ttl} {cids[0]}–{cids[-1]}（{len(cids)}カット）。{MARK}・1995-03-20・事件の回の4本目・判決が確定した事件）。',
            "",
            was,
            "■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep30/make_plan30.py` で",
            "  映像方針の一覧（`ref/ep30/eizou_build/make_list30.py`＝了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から",
            "  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep30/eizou_list30.md`）。",
            "  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**",
            "     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。",
            "  🔴 額装・帯の写真は静止（`build_jiko.FRAME_STILL_EP` に ep30）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。",
            "  🔴 第三者の写真（東京消防庁・東京地下鉄・地元の個人）は引用（高さいっぱいの額・加工しない・話している秒だけ・本編だけ）。公的な機関の紙面も額装。説明カットの地は写真を暗くするだけ（8:1）。",
            "  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。",
            "  🔴 この回の線（細部の一覧はルール §B2-12）を図にも画面にも出さない。紙面と写真に線の字が写る＝親が絵を見て切る。",
            "  ⚠️ 人＝語りと画面に出すのは教祖だけ（本名は c210 だけ）。被害者・遺族・第一通報者・手記の筆者・医師・幹部・実行役・答弁者は立場だけ・団体名は「アレフ」だけ。",
            "     「分かっていたのに放置」も「防ぎようがなかった」も言い切らない／「警察が犯人扱いした」と言い切らない＝図でも同じ。被害者が写る絵・教団の宣伝物・報道の写真と映像は使わない",
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
    plan, title, cuts, A = build()
    cnt, got, ch, best, errs = check(plan, title, cuts, A)
    print(f"カット {len(plan)}・章 {dict(ch)}")
    print("章の見出し " + "／".join(f"{k}={v}" for k, v in title.items()))
    print(f"種類 {dict(cnt)}")
    print(f"写真 {got['photo']}（陸自 {got['gsdf']}・引用 {got['quote']}・映像 {got['video']}・公立 {got['koritsu']}・公的 {got['public']}・場所 {got['place']}）・フリー素材 {got['stock']}・"
          f"図解 {got['fig']}（衛星 {got['sat']}・札 {got['card']}・模式 {got['drawn']}・無線帯 {got['radio']}・言葉 {got['words']}）・文字の頁 {got['textpage']}・パネル {got['panel']}・"
          f"文字だけ {got['text']}・再現イラスト {got['illu']}・🔧替えた {sum(1 for c in plan if plan[c]['plan'].startswith('🔧'))}")
    if errs:
        for e in errs:
            print("🔴", e)
        sys.exit(1)
    print("✓ 映像方針（了承②）の数と一致")
    if "--write" in sys.argv:
        write(plan, title)
