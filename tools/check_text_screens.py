# -*- coding: utf-8 -*-
"""check_text_screens.py — **文字だけの画面は2割まで・3カット以上続けない**（ルール §5b-79）。🆕 2026-09-29（14本目 ⑤b-7b）

■ 何を数えるか
  台本の順（`scene_jiko.ORDER`＝narration.json の並び）に全カットの「画面の種類」を並べ、文字だけ（パネル・決め所・文字の頁）の
  数・割合・続く長さを数える。種類の正本＝章ファイルの `PLAN`（`cuts/__init__.py` が SPEC に写す＝§5b-81）。
  🔴 **札（kind）でなく絵で確かめる**：SPEC の図の型と種類が食い違えば E（「図解」と名乗ってパネルを描いている、など）
     決め所＝fig "quote"（冒頭の絵 intro つきは「混ざり」）／パネル＝"panel"／再現イラスト＝"illu"／混ざり＝"illu_pair"・intro つきの
     quote・写真を地に敷いた図／文字の頁・図・写真の頁＝頁の画像（`ss.page`＝`/pg` の名）で fig なし／写真＝頁でない写真（映像の
     ひかえの静止画を含む）／図解＝それ以外の図の型（hull・axis・qty・boxes・drift・lash …）
  画の無いカット（SPEC が無い）は PLAN の種類で数え、W で名指しする（書き終えたら 0＝cuts の門番と同じ数）
■ 決まり（§5b-79）＝E：文字だけ > 20%／3カット以上続く所がある／種類と図の型の食い違い／PLAN に無いカット（ed01 を除く）
  時間の割合（実測の秒）は参考に出す（決まりはカットの数）
■ 陽性対照（`--selftest`・毎回まず回す）
  ① **15本目の案B**（`ref/ep15/daihon_v2.md` を Vault の数え方で読んだ＝59/192・31%・最長5）を**決まり**で数えると E が出ること
  ② 2割の内でも3カット続けば E  ③ 札の嘘（種類＝図解・図＝panel）で E  ④ 14本目の承認ずみの並び（34/195・最長2）で出ないこと
  ⑤ 15本目の案B を**この回の承認**で数えると通る ⑥ 承認より1カット多いと E ⑦ 承認の区間の外で3カット続くと E
■ 🔴 回ごとの例外（2026-09-30 15本目 ⑤b-1）＝`EXCEPTIONS`
  15本目は決まり（§5b-79＝16本目の ④ から）の前に案B（文字だけ 59/192＝30.7%・続く最長5・3連続以上4か所）で承認ずみ
  （09-26 カズヤくん・映像方針 §11・ルール §A0b 0b-24）。**承認の数だけ**を許す＝文字だけは59まで・3カット以上続くのは承認の
  4区間の中だけ（1カットでも増えれば E）。16本目からは例外なし（決まりのまま）。
使い方： python tools/check_text_screens.py [--selftest] [--ids]
"""
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

TEXT = ("パネル", "決め所", "文字の頁")
LIMIT, RUN_MAX = 0.20, 2
REPO = Path(__file__).resolve().parent.parent
# 🔴 回ごとの例外＝承認ずみの数だけ（増えたら E）。鍵は el_script.SLUG。16本目からは例外なし＝決まり（2割・最長2）
EXCEPTIONS = {
    "ep15": dict(max_text=59, runs_ok=("c313〜c316", "c517〜c519", "c821〜c903", "c908〜c912"),
                 why="15本目は案B（文字だけ 59/192＝30.7%・続く最長5・3連続以上4か所）＝09-26 カズヤくん承認"
                     "（映像方針 §11・ルール §5b-79・§A0b 0b-24）"),
}


def pic_kinds(s):
    """SPEC の1カットの図から、あり得る画面の種類（集合）。None＝画が無い。"""
    fig, photo = s.get("fig"), s.get("photo")
    if fig:
        k = fig[0]
        if k == "quote":
            return {"混ざり"} if s.get("intro") else {"決め所"}
        if k == "panel":
            return {"パネル"}
        if k == "illu":
            return {"再現イラスト"}
        if k == "illu_pair":
            return {"混ざり"}
        return {"混ざり", "図解"} if photo else {"図解"}
    if photo:
        return {"文字の頁", "図・写真の頁"} if "/pg" in str(photo) else {"写真"}
    return None


def _inside(span, allowed, pos):
    """span「cA〜cB」が allowed の区間「cX〜cY」のどれかの中か（pos＝台本の順の位置）。"""
    a, b = span.split("〜")
    for x in allowed:
        lo, hi = x.split("〜")
        if lo in pos and hi in pos and pos[lo] <= pos[a] and pos[b] <= pos[hi]:
            return True
    return False


def judge(order, plan, spec, secs=None, exc=None):
    """order＝台本の順のカットID・plan＝PLAN・spec＝SPEC・exc＝この回の例外（EXCEPTIONS の値）。
    戻り＝(E の list, W の list, 数の dict)。"""
    E, W = [], []
    kinds = []
    for c in order:
        if c not in plan:
            if c != "ed01":
                E.append(f"{c}: PLAN に無い（画面の種類が決まっていない）")
            continue
        k = plan[c]["kind"]
        s = spec.get(c)
        if s is None:
            W.append(f"{c}: 画が無い（PLAN の種類「{k}」で数えた）")
        else:
            got = pic_kinds(s)
            if got is None:
                E.append(f"{c}: SPEC に図も写真も無い")
            elif k not in got:
                E.append(f"{c}: 種類は「{k}」なのに、図は「{'／'.join(sorted(got))}」（札でなく絵で数える＝PLAN を直す）")
        kinds.append((c, k))
    n = len(kinds)
    tc = sum(1 for _, k in kinds if k in TEXT)
    best = run = runs = 0
    span, spans = "", []
    for i, (c, k) in enumerate(kinds):
        if k in TEXT:
            run += 1
            if run > best:
                best, span = run, f"{kinds[i - run + 1][0]}〜{c}"
        else:
            if run > RUN_MAX:
                runs += 1
                spans.append(f"{kinds[i - run][0]}〜{kinds[i - 1][0]}")
            run = 0
    if run > RUN_MAX:
        runs += 1
        spans.append(f"{kinds[-run][0]}〜{kinds[-1][0]}")
    ratio = tc / n if n else 0.0
    if exc:
        pos = {c: i for i, (c, _) in enumerate(kinds)}
        if tc > exc["max_text"]:
            E.append(f"文字だけ {tc}/{n}＝{ratio * 100:.1f}%（この回の承認は {exc['max_text']} まで）")
        out = [sp for sp in spans if not _inside(sp, exc["runs_ok"], pos)]
        if out:
            E.append(f"文字だけが3カット以上続く所が承認の区間の外に {len(out)} か所：{'・'.join(out)}"
                     f"（承認＝{'・'.join(exc['runs_ok'])}）")
    else:
        if ratio > LIMIT:
            E.append(f"文字だけ {tc}/{n}＝{ratio * 100:.1f}%（2割まで）")
        if runs:
            E.append(f"文字だけが3カット以上続く所 {runs} か所：{'・'.join(spans)}（2まで）")
    ts = tot = 0.0
    if secs:
        for c, k in kinds:
            tot += secs.get(c, 0.0)
            ts += secs.get(c, 0.0) if k in TEXT else 0.0
    cnt = Counter(k for _, k in kinds)
    return E, W, dict(n=n, tc=tc, ratio=ratio, best=best, span=span, time=(ts / tot if tot else None), cnt=cnt,
                      ids={k: [c for c, kk in kinds if kk == k] for k in TEXT})


# ══════════════════════════════════════════════════════════
#  陽性対照
# ══════════════════════════════════════════════════════════
# 15本目 案B＝Vault `Resources/事故検証ch-案C見本/count_text_screens.py` の preset ep15B（2026-09-26 15本目 映像方針）を写した
EP15_TEXTPAGES = set('c102 c110 c304 c402 c409 c503 c507 c601 c608 c611 c618 c624 c703 c724 c818 c901 c902 c904'.split())
EP15_B = {k: '再現イラスト' for k in 'c101 c102 c108 c109 c212 c215 c216 c305 c307 c312 c701 c726 c816'.split()}
EP15_B.update({'c205': '写真', 'c104': '混ざり', 'c904': '混ざり', 'c302': '図解'})
EP15_B.update({k: '図解' for k in ('c106 c502 c505 c509 c510 c511 c513 c514 c607 c609 c709 c712 c715 c716 c717 '
                                   'c719 c720 c213 c602 c603 c811 c812 c819 c820 c918').split()})
EP15_B.update({k: '再現イラスト' for k in 'c107 c414 c802'.split()})
EP15_B.update({k: '図解' for k in ('c324 c404 c408 c410 c411 c412 c615 c913 c916 c206 c217 c616 c620 c622 c907 '
                                   'c415 c524 c617 c621 c704 c705 c905 c218 c220 c606 c612 c804 c806 c809 c813 '
                                   'c321 c322 c508 c516 c522 c721 c722 c723 c725').split()})


def ep15_plan():
    """15本目の台本の画の欄を Vault の数え方で種類にする（案B）。無ければ None。"""
    p = REPO / "ref" / "ep15" / "daihon_v2.md"
    if not p.exists():
        return None
    hdr = re.compile(r'^\*\*(c[0-9a-z]\d{2})\*\*\s*(?:🔧)?\s*／\s*(.*?)\s*／\s*(.*)$')
    plan = {}
    for ln in p.read_text(encoding="utf-8").split("\n"):
        m = hdr.match(ln)
        if not m:
            continue
        c, pic = m.group(1), m.group(2)
        if c in EP15_B:
            k = EP15_B[c]
        elif pic.startswith("quote"):
            k = "決め所"
        elif pic.startswith("panel"):
            k = "パネル"
        elif pic.startswith("実写"):
            k = "写真"
        elif re.match(r"図\s*p\d", pic):
            k = "文字の頁" if c in EP15_TEXTPAGES else "図・写真の頁"
        else:
            k = "図解"
        plan[c] = dict(kind=k)
    return plan


def selftest():
    ok = True

    def run(name, order, plan, spec, want_e, exc=None):
        nonlocal ok
        E, _, st = judge(order, plan, spec, exc=exc)
        got = bool(E)
        ok &= got == want_e
        print(f"  {'OK' if got == want_e else '🔴 NG'} {name}: {'E' if got else '合格'}（{'E' if want_e else '合格'}のはず）"
              f"  ← {st['tc']}/{st['n']}＝{st['ratio'] * 100:.1f}%・最長{st['best']}" + (f"・{E[0]}" if E else ""))
    p15 = ep15_plan()
    if p15 is None:
        print("  🔴 NG ① 15本目の台本（ref/ep15/daihon_v2.md）が無い＝陽性対照を作れない")
        ok = False
    else:
        run("① 15本目の案B を決まり（2割・最長2）で数える（31%・最長5）", list(p15), p15, {}, True)
        run("⑤ 15本目の案B をこの回の承認（59・4区間）で数える", list(p15), p15, {}, False, EXCEPTIONS["ep15"])
        # ⑥ 承認より1カット多い＝文字だけでない最初のカットを1つパネルにする（区間の外で続かない所）
        p60 = {c: dict(v) for c, v in p15.items()}
        extra = next(c for c in ("c206", "c407", "c605") if p60[c]["kind"] not in TEXT)
        p60[extra] = dict(kind="パネル")
        run(f"⑥ 承認より1カット多い（{extra} をパネルに＝60）", list(p60), p60, {}, True, EXCEPTIONS["ep15"])
    ids = [f"c{i:03d}" for i in range(100, 200)]
    plan = {c: dict(kind="図解") for c in ids}
    for c in ids[10:13]:
        plan[c] = dict(kind="パネル")
    run("② 2割の内（3%）でも3カット続く", ids, plan, {}, True)
    plan2 = {c: dict(kind="図解") for c in ids}
    run("③ 札の嘘（種類＝図解・図＝panel）", ids, plan2, {ids[5]: dict(fig=("panel", {}))}, True)
    plan3 = {c: dict(kind="図解") for c in ids}
    for c in ids[10:12] + ids[20:22]:
        plan3[c] = dict(kind="決め所")
    run("④ 4%・最長2・札と絵が合う", ids, plan3, {ids[10]: dict(fig=("quote", {})), ids[11]: dict(fig=("quote", {}))}, False)
    # ⑦ 例外の回でも、承認の区間の外で3カット続けば E（区間の中なら通る）
    exc7 = dict(max_text=10, runs_ok=(f"{ids[10]}〜{ids[12]}",), why="見本")
    run("⑦a 承認の区間の中で3カット続く", ids, plan, {}, False, exc7)
    plan7 = {c: dict(kind="図解") for c in ids}
    for c in ids[50:53]:
        plan7[c] = dict(kind="パネル")
    run("⑦b 承認の区間の外で3カット続く", ids, plan7, {}, True, exc7)
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import cuts
    import el_script
    import scene_jiko as SJ
    secs = dict(SJ.CUTS)
    exc = EXCEPTIONS.get(el_script.SLUG)
    E, W, st = judge(list(SJ.ORDER), cuts.PLAN, cuts.SPEC, secs, exc)
    print(f"\n== {el_script.SLUG} の画面の種類（{st['n']}カット・台本の順）")
    if exc:
        print(f"  ⚠️ この回の例外：{exc['why']}＝文字だけ {exc['max_text']} まで・3連続以上は {'・'.join(exc['runs_ok'])} の中だけ")
    print("  " + "・".join(f"{k} {st['cnt'][k]}" for k in ("写真", "図・写真の頁", "再現イラスト", "図解", "混ざり",
                                                          "文字の頁", "パネル", "決め所")))
    tm = f"・時間 {st['time'] * 100:.1f}%（実測の秒）" if st["time"] is not None else ""
    print(f"  ◆ 文字だけ {st['tc']}/{st['n']}＝{st['ratio'] * 100:.1f}%{tm}・続く最長 {st['best']}（{st['span']}）")
    if "--ids" in sys.argv:
        for k in TEXT:
            print(f"  {k} {len(st['ids'][k])}: " + " ".join(st["ids"][k]))
    for w in W:
        print("  W " + w)
    for e in E:
        print("  🔴 E " + e)
    if not st["n"]:
        print("🔴 数えたカットが0件＝台本の順か PLAN が読めていない（0件で合格にしない）")
        return 1
    print(f"\n{'✓' if not E else '🔴'} 文字だけの画面：{st['n']}カットを数えた・E {len(E)}件・W {len(W)}件（画の無いカット）")
    return 1 if E else 0


if __name__ == "__main__":
    sys.exit(main())
