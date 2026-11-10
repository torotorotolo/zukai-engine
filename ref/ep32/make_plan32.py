# -*- coding: utf-8 -*-
"""make_plan32.py — 32本目の章ファイル（tools/cuts/c1〜c9・ca〜cc）の**骨組み PLAN** を作る（2026-11-10 ⑤b-1・1回だけ）。

PLAN＝その章の全カットの {kind（画面の種類）・plan（画の予定）・src（出典）}。図の中身（SPEC）は ⑤b-2 以降で書く。
**手で写さない**：正本から機械で組む（31本目の `ref/ep31/make_plan31.py` を写して32本目の数と注に替えた）。
  ① 了承②ずみの映像方針の一覧＝`ref/ep32/eizou_build/make_list32.py` の入力と門番（E 0・秒は narration.json の実測〈⑤b-1〉・扉は c201〜cc01 の頭の11枚）＝
     種類・素材・地・見せ方・副題・動き・見た目の型・注・印・映像方針の新しい画＋出どころの表 `sources32.psv` の権利・時期・人・出典の行
     （`list32.tsv` には権利の列が無い＝道具を直に呼ぶ）
  ② 台本 第2版 `ref/ep32/daihon_v2.md` §4 の見出し行 `**c101** ／ 画 ／ 出典` の**出典の欄だけ**（236カット・冒頭＋11章）
  🔴 **台本の画の欄は写さない**（17・24〜31本目の型・narration.py の頭の注と同じ約束）＝元の画は台本 §4・一覧 `ref/ep32/eizou_list32.md`
     （🔴 32本目は台本の画の欄が一覧と食い違う所がある＝⑤b は一覧に従う＝映像方針の引き継ぎ §4 の7）
画面の種類（一覧 → PLAN の kind）：
  映像（沿岸警備隊の監視カメラ VTS＝Commons の3本・PD-USCG）・写真（Commons）・調査（NTSB のドケットの写真）・公的（報告書・連邦官報ほかの紙面＝額装）→ 写真／
  イメージ（Pexels のフリー素材＝⑤b で1本ずつ）→ フリー素材／
  衛星（Google の衛星写真＋描き足しの地図）・模式・札・帯・年表・比べ・並べ・流れ・表・棒・線・割合・時計・言葉・箱 → 図解
  （地は CC BY 2.0・CC0・PD・Pexels の写真を暗くするだけ＝🔴 Google の衛星写真と夜の写真は地にしない）／
  文字だけ → パネル（32本目は0）
書く前に照合する（違えば止まる）＝期待値は**決めた紙の数**（24本目 ⑤b-1 の落とし穴＝見た目の型の欄から数えない）：
  Vault の映像方針の引き継ぎ §1・§6（了承②）＝「236カット・写真・映像・紙面 100＝映像13・写真38・調査13・衛星15・紙面21／
  イメージ 46・図 90（模式67・ほか23）」。
  → 写真 85（映像13・写真38・調査13・公的21）・フリー素材 46・図解 105（衛星 15＋図 90）・文字の頁 0・パネル 0・再現イラスト 0
  （⚠️ 衛星は §2-1 の 20% に数える〈一覧の 42.4%〉が、画面の種類は31本目と同じ「図解」＝描き足しのある地図。PLAN の写真の割合は 85/236＝36.0%）

    python -P ref/ep32/make_plan32.py          # 照合して数を出すだけ（書かない）
    python -P ref/ep32/make_plan32.py --write  # 章ファイル12本を書く（🔴 32本目の SPEC が入った章ファイルは上書きしない）

⚠️ 1回だけ回す道具。**書いたあとは章ファイルの PLAN を手で直す**（種類を変えたら PLAN の kind を直す）。
⚠️ 一覧の秒は書き写さない＝絵は `audio/narration.json` の実測の秒で組む。
⚠️ 31本目の章ファイルも12本（c1〜c9・ca〜cc）＝同じ名のファイルを32本目の器に替える（31本目の中身は git の `f4bd0a9a`）。
"""
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[2]
SCRIPT = HERE / "ref" / "ep32" / "daihon_v2.md"
CUTS = HERE / "tools" / "cuts"
FROM_SHA = "f4bd0a9a"      # 31本目の章ファイルが残っている最後の版（git show <sha>:tools/cuts/c1.py）＝32本目 ⑤b-1 の移し替えの merge
sys.path.insert(0, str(HERE / "ref" / "ep32" / "eizou_build"))
import make_list32 as ML  # noqa: E402

N_CUTS = 236
WANT = dict(photo=85, video=13, shashin=38, chosa=13, public=21, stock=46, fig=105, sat=15, drawn=67, other_fig=23,
            textpage=0, panel=0, illu=0, text=0)
PIC = {"映像": "写真", "写真": "写真", "調査": "写真", "公的": "写真", "イメージ": "フリー素材", "文字だけ": "パネル"}
TEXT = ("パネル", "決め所", "文字の頁")
CHAP = re.compile(r"^(冒頭|第\d+章)　?(.*?)（.*）$")
HEAD = re.compile(r"^\*\*(c[0-9a-c]\d{2})\*\*(.*)$")
WANT_CH = ("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "ca", "cb", "cc")
MARK = "32本目（USエアウェイズ1549便のハドソン川への着水"
OTHER_FIGS = ("札", "帯", "年表", "比べ", "並べ", "流れ", "表", "棒", "線", "割合", "時計", "言葉", "箱")


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
    if a["ga_new"] and a["ga_new"] not in ("台本どおり", "="):
        bits.append("新しい画（映像方針）：" + a["ga_new"])
    if a["frame"].startswith("額装"):
        bits.append("🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）")
    if a["kind"] == "映像":
        bits.append("🔴 VTS（沿岸警備隊の監視カメラ・PD-USCG）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・"
                    "外す秒（背景のコンコルド 410〜428秒）に触れない・焼き込みのカメラの時計は語りと副題に使わない（約20秒進む）＝make_list32 の門番")
    if a["kind"] == "公的":
        bits.append("🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）")
    if a["kind"] == "調査":
        bits.append("🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）")
    if a["kind"] == "写真":
        bits.append("🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・"
                    "私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）")
    if a["kind"] == "衛星":
        bits.append("🔴 Google の衛星写真＝描き足しは公の場所だけ・帰属は地図の右下（Google の表示を絵の近くに）・🔴 説明カットの地にしない（暗くしない）")
    if a["kind"] == "イメージ":
        bits.append("🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）")
    bits.append("台本の画＝台本 §4・一覧 eizou_list32.md（写さない）")
    return ("🔧 " if changed else "") + "｜".join(str(b).replace("\n", " ") for b in bits)


def build():
    cuts = ML.read_cuts(ML.DAIHON)
    tnote = ML.measured(cuts)
    orows, obad = ML.load_psv(ML.OVER, ML.KEYS)
    srows, sbad = ML.load_psv(ML.SOURCES, ML.SKEYS)
    S = {r["code"]: r for r in srows}
    A, abad = ML.assemble(cuts, orows)
    ML.stock_rows(A, S)
    E, W = ML.gates(cuts, A, S, ML.words(ML.NAME_FILES))
    ML.gate_video(cuts, A, E, W)
    E = obad + sbad + abad + E
    if E:
        raise SystemExit(f"🔴 一覧の門番が E {len(E)}（先に make_list32.py を E 0 に）: {E[:2]}")
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
    got = dict(photo=cnt["写真"], video=lk["映像"], shashin=lk["写真"], chosa=lk["調査"], public=lk["公的"],
               stock=cnt["フリー素材"], fig=cnt["図解"], sat=lk["衛星"], drawn=lk["模式"], other_fig=sum(lk[k] for k in OTHER_FIGS),
               textpage=cnt["文字の頁"], panel=cnt["パネル"], illu=cnt["再現イラスト"], text=text)
    if got != WANT:
        errs.append(f"数が映像方針（了承②）と違う: {got}（期待 {WANT}）")
    if best > 0:
        errs.append(f"文字だけの画面の続く最長 {best}（映像方針は 0）")
    unknown = sorted(set(lk) - set(PIC) - {"衛星", "模式"} - set(OTHER_FIGS))
    if unknown:
        errs.append(f"一覧の種類に知らない名: {unknown}")
    return cnt, got, ch, best, errs


def write(plan, title):
    for name, ttl in title.items():
        cids = [c for c in plan if c.startswith(name)]
        f = CUTS / f"{name}.py"
        old = f.read_text(encoding="utf-8") if f.exists() else ""
        if MARK in old and "\nSPEC = {}\n" not in old:
            raise SystemExit(f"🔴 {f} は32本目の SPEC が入っている（`SPEC = {{}}` の行が無い）＝上書きしない")
        # 32本目の章ファイルを PLAN だけ書き直すときは、`SPEC = {}` の行から後ろ（SPEC.update…＝書いた図）をそのまま残す（make_plan28 の型）
        keep = old.split("\nSPEC = {}\n", 1)[1] if MARK in old else ""
        was = (f"■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `{FROM_SHA}`"
               f"（`git show {FROM_SHA}:tools/cuts/{name}.py`）。") if (old and MARK not in old) else \
              "■ 🆕 2026-11-10（⑤b-1）：新しいファイル。"
        if MARK in old:
            m = re.search(r"\n(■ (?:🔴|🆕) 2026-11-10（⑤b-1）：.*?。)\n", old)
            was = m.group(1) if m else was
        body = [
            "# -*- coding: utf-8 -*-",
            f'"""{ttl} {cids[0]}–{cids[-1]}（{len(cids)}カット）。{MARK}・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。',
            "",
            was,
            "■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep32/make_plan32.py` で",
            "  映像方針の一覧（`ref/ep32/eizou_build/make_list32.py`＝了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から",
            "  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep32/eizou_list32.md`＝⑤b は一覧に従う）。",
            "  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**",
            "     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。",
            "  🔴 額装・帯の写真は静止（`build_jiko.FRAME_STILL_EP` に ep32）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。",
            "  🔴 写真は画面いっぱい・色は原本（`build_jiko.PHOTO_KEEP_EP` に ep32）・BY-SA は額装・紙面と調査の写真も額装。説明カットの地は写真を暗くするだけ（8:1・衛星と夜の写真は地にしない）。",
            "  🔴 VTS（沿岸警備隊の監視カメラ）は等速・止めなし・頭から使う・同じ秒を2回使わない（区間は一覧の動きの欄＝make_list32 の門番）。",
            "  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。",
            "  🔴 この回の線＝語りと画面に名前を出すのは機長と副操縦士だけ（初出 c203・c205）・客室乗務員・管制官・救助の人は立場だけ・乗客は名前なし・",
            "     NTSB・FAA・議員・知事・監督・俳優は役職で・「犠牲」「死亡」は言わない・「208秒」は使わず「約3分半」・映画は c517〜c518・c520 だけ",
            "     ＝図でも同じ（紙面・写真に名前の字が写る＝親が絵を見て切る・船の名も読ませない）",
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
    print(f"写真 {got['photo']}（映像 {got['video']}・写真 {got['shashin']}・調査 {got['chosa']}・公的 {got['public']}）・フリー素材 {got['stock']}・"
          f"図解 {got['fig']}（衛星 {got['sat']}・模式 {got['drawn']}・ほか {got['other_fig']}）・文字の頁 {got['textpage']}・パネル {got['panel']}・"
          f"文字だけ {got['text']}・再現イラスト {got['illu']}・🔧替えた {sum(1 for c in plan if plan[c]['plan'].startswith('🔧'))}")
    if errs:
        for e in errs:
            print("🔴", e)
        sys.exit(1)
    print("✓ 映像方針（了承②）の数と一致")
    if "--write" in sys.argv:
        write(plan, title)
