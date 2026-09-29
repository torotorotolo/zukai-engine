# -*- coding: utf-8 -*-
"""check_illu.py — 案C の再現イラスト（`tools/illu.py`）の**守りの線**を機械で測る（2026-09-28 新設・14本目 ⑤b-2）。

■ なぜ要るか（ルール §5b-74・§5b-75＝規則を書いたら門番も＝[[feedback-rules-need-gates]]）
    再現イラストは「記録どおりに描いた絵」。記録を越えた物・人・数・時刻が1つでも混ざると、絵がそのまま嘘になり、
    亡くなった方の尊厳の線（乗客は顔の無い群れだけ・水が入った後の船内に乗客を描かない）も目で追うだけでは漏れる。

■ 測るもの（**描く側と同じ関数**＝`illu.scene` が組んだ部品・鍵・型紙の数・群れの並び＝SPEC の文字を読み比べない）
  ① 全部品に rec（出典の表 `cuts.ss.REC_DOCS` の資料名＋頁）・頁が資料の範囲にあり、原文（`cuts.ss.REC_PAGES`）に在る。
     記録の欄（傾き・波・コンテナ・群れ）を変える段と、出来事（board・rings）の段は rec を書く。頭を既定から変えたら場面の rec
  ② 人の影の役割＝船員・海洋警察・管制（型紙）／乗客は**群れの型だけ**（`crowd_layout`＝隣と2割以上重なる・枠の外まで続く
     ＝`illu.crowd_uncountable`）。群れを出す場面は時刻 `at` を宣言し、`cuts.ss.ILLU_CROWD_UNTIL` より前
  ③ 描いた人の数（型紙を置く inst の数）＝宣言（`people=`）＝記録（宣言の rec）。型紙の影どうしは重ならない（1人ずつ数えられる）
     ＝⑤b-3 から**部品をまたいで全部の組**を・型紙の背（`fig_h`）で測る（傾けた型紙は `fig_deg` の向きに戻して）
  ④ 「再現イラスト」の札と出典（`illu.overlay_svg`＝全面・冒頭の絵／`illu_pair` は段の層の札と骨格の出典）
  ⑤ 画面に出す文字（札）に、資料で割れる時刻（`cuts.ss.ILLU_SPLIT_TIMES`）が無い
  ⑦ 写真・頁・決め所・文字の頁のカットに絵が無い（混ざりは冒頭の絵か小さく戻す絵だけ）。「再現イラスト」の PLAN の
     カットは全面の絵（`illu`）で書く（SPEC が在るものだけ）
  ⑧ 上から見た絵（view に「上から」）は縮尺 `scale`（メートル／画素）が 1.5 以上（人が1画素に満たない＝15本目の申し送り）
  ほかに touch＝記録の「どの甲板が水面に届いたか」を、描く側と同じ幾何（`illu.contact_y`）で ±0.35 メートル
  ⑥ 陽性対照（わざと壊した場面で鳴るか）＝`--selftest`（本番の前に必ず回る）

■ 使い方
    python tools/check_illu.py              # 全カット（selftest のあと）
    python tools/check_illu.py --selftest   # 物差しの検算だけ
"""
from __future__ import annotations

import math
import re
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import titan_fig as F  # noqa: E402,F401  （illu より先に読む）
import illu as IL  # noqa: E402

TIME = re.compile(r"(\d{1,2})\s*[時:：]\s*(\d{1,2})")
CROWD_ROLES = ("passengers",)
NON_ILLU_KINDS = ("写真", "図・写真の頁", "決め所", "文字の頁", "図解", "パネル")


def _ss():
    import cuts.ss as ss
    return ss


@lru_cache(maxsize=1)
def _pages():
    ss = _ss()
    p = getattr(ss, "REC_PAGES", None)
    if not p or not Path(p).exists():
        return None
    return {int(m) for m in re.findall(r"^=== p(\d+) ===", Path(p).read_text(encoding="utf-8"), re.M)}


def _hm(s):
    m = TIME.search(str(s or ""))
    return (int(m.group(1)), int(m.group(2))) if m else None


def check_recs(recs, where, docs, pages):
    bad = []
    for r in recs:
        got = IL.parse_rec(r, docs)
        if not got:
            bad.append(f"①{where}：rec「{r}」に資料名と頁が無い（`資料 p頁` の形・資料名は cuts.ss.REC_DOCS）")
            continue
        for doc, ps in got:
            lo, hi = docs[doc]["range"]
            for p in ps:
                if not lo <= p <= hi:
                    bad.append(f"①{where}：rec「{r}」の p{p} が {doc} の頁の範囲（p{lo}〜p{hi}）の外")
                elif pages is not None and p not in pages:
                    bad.append(f"①{where}：rec「{r}」の p{p} が原文（REC_PAGES）に無い")
    return bad


def judge_scene(sc, where, docs=None, pages=None, split=None, until=None):
    """場面1つを測る。返り値＝(食い違いの一覧, 照合した件数)。"""
    ss = _ss()
    docs = docs if docs is not None else ss.REC_DOCS
    pages = pages if pages is not None else _pages()
    split = split if split is not None else ss.ILLU_SPLIT_TIMES
    until = until if until is not None else ss.ILLU_CROWD_UNTIL
    bad, n = [], 0
    # ① 部品の rec・段の rec
    for p in sc["parts"]:
        n += 1
        if not p.get("rec"):
            bad.append(f"①{where}：部品 {p['id']} に rec が無い")
    bad += check_recs([p["rec"] for p in sc["parts"] if p.get("rec")], where, docs, pages)
    prev = sc["start"]
    base = IL.FIELDS[sc["place"]]
    if any(sc["start"].get(k) != base.get(k) for k in IL.REC_FIELDS if k in base) and not sc.get("rec"):
        bad.append(f"①{where}：頭の状態を既定から変えた（{[k for k in IL.REC_FIELDS if sc['start'].get(k) != base.get(k)]}）"
                   "のに場面の rec が無い")
    for i, (st, sp) in enumerate(zip(sc["states"], sc["steps"])):
        n += 1
        changed = [k for k in IL.REC_FIELDS if k in st and st[k] != prev.get(k)]
        events = [k for k in IL.EVENTS if sp.get(k)]
        if (changed or events) and not sp.get("rec"):
            bad.append(f"①{where}：段{i + 1}で {changed + events} を変えた／起こしたのに rec が無い")
        prev = st
    bad += check_recs([sp["rec"] for sp in sc["steps"] if sp.get("rec")] + ([sc["rec"]] if sc.get("rec") else []),
                      where, docs, pages)
    # ② 人の役割・群れの型・群れの時刻
    at = _hm(sc.get("at"))
    for p in sc["parts"]:
        role = p.get("role")
        if role is None:
            continue
        n += 1
        if p.get("kind") == "sprite":
            if role not in IL.ROLES:
                bad.append(f"②{where}：型紙の影（1人ずつ数えられる形）の役割「{role}」は {IL.ROLES} だけ"
                           "（乗客は群れの型でだけ＝1人を抜き出さない）")
        elif role in CROWD_ROLES:
            if not p.get("crowd"):
                bad.append(f"②{where}：乗客の部品 {p['id']} が群れの型（crowd_layout）で描かれていない")
            for c in p.get("crowd") or []:
                bad += [f"②{where}：{b}" for b in IL.crowd_uncountable(c["layout"], c["x0"], c["x1"])]
            shown = any(float(k.get("a", 1.0)) > 0.0 for k in p["keys"])
            if shown:
                if at is None:
                    bad.append(f"②{where}：乗客の群れを出す場面なのに時刻 at が無い")
                elif at >= _hm(until):
                    bad.append(f"②{where}：乗客の群れを {sc['at']} の場面に出した（{until} より前だけ＝水が入った後の船内に"
                               "乗客を描かない）")
        else:
            bad.append(f"②{where}：知らない役割「{role}」")
    # ③ 描いた人の数＝宣言＝記録
    #   ⑤b-3：重なりは**部品をまたいで**全部の組で・型紙の背の高さ（fig_h＝置き場ごとに違う）で測る
    #   （ゴムボートの海洋警察と乗り移る船員は別の部品＝部品の中だけ見ると重なりを見逃す）
    #   船内で傾けた型紙（fig_deg）は、影の立つ向き＝床に沿う向きに戻して測る（画面の縦横で測ると 45度の並びが全部「重なる」）
    drawn, ends = {}, []
    for p in sc["parts"]:
        if p.get("kind") == "sprite":
            drawn[p.get("role")] = drawn.get(p.get("role"), 0) + len(p.get("inst") or [])
            ends += [(tuple(i["path"][-1]), float(p.get("fig_h") or IL.FIG_H), float(p.get("fig_deg") or 0.0))
                     for i in p.get("inst") or []]

    def _near(a, fa, da, b, fb):
        r = math.radians(-da)
        dx, dy = b[0] - a[0], b[1] - a[1]
        u, v = dx * math.cos(r) - dy * math.sin(r), dx * math.sin(r) + dy * math.cos(r)
        return abs(u) < max(fa, fb) * 0.55 and abs(v) < max(fa, fb) * 0.5
    hit = next(((a, b) for j, (a, fa, da) in enumerate(ends) for (b, fb, _db) in ends[j + 1:] if _near(a, fa, da, b, fb)),
               None)
    if hit:
        bad.append(f"③{where}：型紙の影の立つ所 {hit[0]}・{hit[1]} が重なる（1人ずつ数えられない＝数の照合が目で出来ない）")
    decl = sc.get("people") or {}
    for role in set(drawn) | set(decl):
        n += 1
        d = decl.get(role)
        want = d[0] if isinstance(d, (tuple, list)) else d
        if want is None:
            bad.append(f"③{where}：{role} を {drawn.get(role)} 人描いたのに宣言（people=）が無い")
        elif drawn.get(role, 0) != want:
            bad.append(f"③{where}：{role} の描いた数 {drawn.get(role, 0)} ≠ 宣言 {want}")
        if d is not None and not (isinstance(d, (tuple, list)) and len(d) > 1 and d[1]):
            bad.append(f"③{where}：宣言 {role} に記録（rec）が無い＝people=dict({role}=(数, \"資料 p頁\"))")
        elif d is not None:
            bad += check_recs([d[1]], where, docs, pages)
    # ⑤ 札の時刻
    for t in sc["tags"]:
        for txt in t.get("texts") or []:
            hm = _hm(txt)
            if hm and f"{hm[0]}:{hm[1]:02d}" in split:
                n += 1
                bad.append(f"⑤{where}：札「{txt}」の時刻は資料で割れる（{split}）＝画面に出さない")
    # ⑧ 上から見た絵の縮尺
    if "上から" in (sc.get("view") or ""):
        n += 1
        if not sc.get("scale") or float(sc["scale"]) < 1.5:
            bad.append(f"⑧{where}：上から見た絵の縮尺 {sc.get('scale')} メートル／画素（1.5 以上＝人が1画素に満たない縮尺だけ）")
    # touch：記録の「どの甲板が水面に」を同じ幾何で
    for i, (st, sp) in enumerate(zip(sc["states"], sc["steps"])):
        if sp.get("touch"):
            n += 1
            if sp["touch"] not in IL.CONTACTS:
                bad.append(f"touch {where}：段{i + 1}の「{sp['touch']}」は知らない点（{tuple(IL.CONTACTS)}）")
                continue
            h = IL.contact_y(sp["touch"], float(st["heel"]))
            if abs(h) > 0.35:
                bad.append(f"touch {where}：段{i + 1}の傾き {st['heel']}度で「{sp['touch']}」は水面から {h:+.2f} メートル"
                           "（記録は水面に届いた）")
    return bad, n


def judge_fig(kind, kw, where):
    """型（illu・illu_pair）から場面と上の層を組み、①〜⑤⑧と④を測る。"""
    f = getattr(F, kind)(**kw)
    bad, n = [], 0
    for k, sc in enumerate(f.illu["scenes"]):
        b, m = judge_scene(sc, f"{where}#{k + 1}")
        bad += b
        n += m
    n += 1
    if f.illu.get("full"):
        ov = IL.overlay_svg(f.illu.get("view", ""), f.illu.get("src", ""))
        if "再現イラスト" not in ov or not f.illu.get("src"):
            bad.append(f"④{where}：「再現イラスト」の札か出典が無い")
    else:
        stages = "".join(f.stages)
        if stages.count("再現イラスト") < len(f.illu["scenes"]) or "出典：" not in f.lab:
            bad.append(f"④{where}：小さく戻す絵の数だけ「再現イラスト」の札が無い／出典が無い")
    return bad, n


def judge_cut(cid, spec, kind_of):
    """カット1つ（SPEC）。⑦＝画面の種類と絵の置き方。"""
    bad, n = [], 0
    kind = kind_of.get(cid) or spec.get("kind")
    fig = spec.get("fig") or (None, None)
    it = (spec.get("intro") or {}).get("illu")
    has_full = fig[0] == "illu"
    has_mini = fig[0] == "illu_pair"
    n += 1
    if kind in NON_ILLU_KINDS and (has_full or has_mini or it):
        bad.append(f"⑦{cid}：画面の種類「{kind}」に再現イラストを置いた（写真・頁・決め所・文字の頁に絵を置かない）")
    if kind == "混ざり" and has_full:
        bad.append(f"⑦{cid}：混ざりに全面の絵（illu）＝画面の種類を「再現イラスト」にするか、冒頭の絵か小さく戻す絵に")
    if kind == "再現イラスト" and not has_full:
        bad.append(f"⑦{cid}：画面の種類「再現イラスト」なのに全面の絵（fig=(\"illu\", …)）で書いていない")
    if it and fig[0] != "quote":
        bad.append(f"⑦{cid}：冒頭の絵（intro の illu）は決め所の前だけ（fig は quote）")
    if has_full or has_mini:
        b, m = judge_fig(fig[0], fig[1], cid)
        bad += b
        n += m
    if it:
        sc = IL.scene(**it)
        b, m = judge_scene(sc, f"{cid}#冒頭")
        bad += b
        n += m + 1
        if "再現イラスト" not in IL.overlay_svg(sc["view"], sc["src"]) or not sc["src"]:
            bad.append(f"④{cid}#冒頭：「再現イラスト」の札か出典が無い")
        if any(t["texts"] for t in sc["tags"]):
            bad.append(f"④{cid}#冒頭：冒頭の絵に札を付けた（段の層は決め所のもの）")
    return bad, n


def selftest():
    """物差しの検算。正しい場面が通り、わざと壊した場面（陽性対照）が落ちること。"""
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（置き場 A〜E の部品の既定の rec が14本目の資料を指す）。
    #    本番の表は回ごとに空にする（§0b）＝この処理の中だけ14本目の資料の表・原文・時刻にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    # 資料の表と原文の頁はこの回のもの（置き場の部品の既定の rec がこの回の資料を指すため）
    docs, pages = _ss().REC_DOCS, _pages()
    split = ("9:46", "9:48")
    until = "9:47"
    kw = dict(docs=docs, pages=pages, split=split, until=until)
    good_D = dict(place="D", at="9:46", start=dict(heel=61.2), rec="判決 p18",
                  people=dict(crew=(8, "判決 p11")),
                  steps=[dict(board=8, rec="判決 p18"), dict(state=dict(mark="on", crowd="on"), rec="判決 p18")])
    good_A = dict(place="A", at="9:34", start=dict(heel=52.2, wake="off"), rec="海審 p1057",
                  steps=[dict(touch="3階（B甲板）の左舷"),
                         dict(state=dict(heel=61.2), rec="海審 p1057", touch="船橋甲板の左舷")])
    good_B = dict(place="B", at="8:56", start=dict(view="cabin", heel=30.0, crowd="on"), rec="判決 p12",
                  steps=[dict(rings=2, rec="海審 p1053")])
    good_C = dict(place="C", at="9:25", start=dict(view="room", heel=45.0, crew=8), rec="判決 p14",
                  people=dict(crew=(8, "判決 p11")),
                  steps=[dict(asks=3, rec="判決 p14"), dict(walkie=3, rec="判決 p14"), dict()])
    good_E = dict(place="E", at="9:06", steps=[dict(state=dict(sel="on"), rings=2, rec="海審 p1059"),
                                               dict(rings=1, rec="海審 p1059")])
    good_far = dict(place="D", at="9:30", start=dict(view="far", heel=47.5), rec="艇長の判決 p5002",
                    steps=[dict(), dict(state=dict(binoc="on"), rec="艇長の判決 p5002")])
    good_rail = dict(place="D", at="9:39", start=dict(view="rail", rboat="on", cg="on"), rec="艇長の判決 p5002",
                     people=dict(coast_guard=(1, "艇長の判決 p5002"), crew=(7, "判決 p17")),
                     steps=[dict(board=7, rec="判決 p17"), dict()])
    cases = [
        ("正しい D（8人・群れ 9:46）", good_D, True),
        ("正しい A（52.2度で3階・61.2度で船橋甲板が水面）", good_A, True),
        ("正しい B（客室の群れ 8:56）", good_B, True),
        ("🔴 陽性対照①：傾きを変えた段に rec が無い", dict(good_A, steps=[dict(state=dict(heel=61.2))]), False),
        ("🔴 陽性対照①：rec の頁が資料の範囲の外（判決 p1018）", dict(good_B, rec="判決 p1018"), False),
        ("🔴 陽性対照②：群れを 9:48 の場面に出す", dict(good_D, at="9:48"), False),
        ("🔴 陽性対照③：描いた人 8 ≠ 宣言 7", dict(good_D, people=dict(crew=(7, "判決 p11"))), False),
        ("🔴 陽性対照③：宣言に記録が無い", dict(good_D, people=dict(crew=8)), False),
        ("🔴 陽性対照⑤：札に割れる時刻（9時46分）",
         dict(good_A, steps=[dict(touch="3階（B甲板）の左舷", tag=dict(t="9時46分", at="b_port"))]), False),
        ("🔴 陽性対照⑧：上から見た絵が細かすぎる（1.0 メートル／画素）", dict(good_B, view="上から見た図", scale=1.0), False),
        ("🔴 陽性対照 touch：45度で「3階の左舷が水面に」", dict(good_A, start=dict(heel=45.0, wake="off")), False),
        # ── ⑤b-3（2026-09-29）：置き場 C（操舵室）・E（管制センター）・D の見え方 far／rail ──
        ("正しい C（操舵室に8人・問いかけの印・3階からの無線機）", good_C, True),
        ("正しい E（管制の画面の点に印・交信の輪）", good_E, True),
        ("正しい D far（双眼鏡で甲板→海）", good_far, True),
        ("正しい D rail（立った海洋警察1人・機関部7人がボートへ）", good_rail, True),
        ("🔴 陽性対照①：問いかけの印（asks）の段に rec が無い",
         dict(good_C, steps=[dict(asks=3), dict(walkie=3, rec="判決 p14"), dict()]), False),
        ("🔴 陽性対照①：双眼鏡を上げた段に rec が無い", dict(good_far, steps=[dict(), dict(state=dict(binoc="on"))]), False),
        ("🔴 陽性対照③：操舵室の影 8 ≠ 宣言 9", dict(good_C, people=dict(crew=(9, "判決 p11"))), False),
        ("🔴 陽性対照③：ゴムボートの海洋警察（1人）を宣言しない", dict(good_rail, people=dict(crew=(7, "判決 p17"))), False),
        ("🔴 陽性対照②：乗客の群れを far（遠くの船）に置く",
         dict(good_far, start=dict(view="far", heel=47.5, crowd="on")), False),
    ]
    ok = True
    for name, spec, want in cases:
        try:
            sc = IL.scene(**spec)
            bad, _ = judge_scene(sc, "selftest", **kw)
        except Exception as e:                           # noqa: BLE001
            bad = [f"組めない：{e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照②（描く側の定数を壊す）：群れの間隔を広げて1人ずつ数えられる形にしたら落ちるか
    keep = IL.CROWD_STEP
    IL.CROWD_STEP = 1.15
    bad, _ = judge_scene(IL.scene(**good_B), "selftest", **kw)
    IL.CROWD_STEP = keep
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照②（描く側）：群れの間隔 1.15＝重ならない影の列: "
          f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照③（⑤b-3・部品をまたぐ重なり）：乗り移る船員の7人目の立つ所を、ボートで立った海洋警察（別の部品）に重ねる
    keep = IL.RAIL_SPOTS
    IL.RAIL_SPOTS = keep[:6] + ((IL.RAIL_CG[0] + 8.0, IL.RAIL_FLOOR),)
    bad, _ = judge_scene(IL.scene(**good_rail), "selftest", **kw)
    IL.RAIL_SPOTS = keep
    good = any(b.startswith("③") and "重なる" in b for b in bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照③（部品をまたぐ重なり）：船員の影を海洋警察の影に重ねる: "
          f"{'不合格' if good else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照③（⑤b-3・45度の床）：45度の操舵室で影を床に沿って 60画素ずつに詰めたら「重なる」で落ちるか
    #   （C の影は立てたまま＝fig_deg 0。fig_deg を持つ型紙〈傾けた影〉は、その向きに戻して測る）
    keep = IL.ROOM_FIG
    IL.ROOM_FIG = tuple((700.0 + 60.0 * j, 600.0) for j in range(8))
    bad, _ = judge_scene(IL.scene(**good_C), "selftest", **kw)
    IL.ROOM_FIG = keep
    good = any(b.startswith("③") and "重なる" in b for b in bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照③（45度の床）：影を床に沿って 60画素ずつに詰める: "
          f"{'不合格' if good else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照②（型紙の役割）：乗客を型紙（1人の影）で置いたら落ちるか
    sc = IL.scene(**good_D)
    for p in sc["parts"]:
        if p.get("kind") == "sprite":
            p["role"] = "passengers"
    bad, _ = judge_scene(sc, "selftest", **kw)
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照②：乗客を1人ずつの型紙で置く: "
          f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照⑦：決め所・写真のカットに絵
    for name, cid, spec, kind in (("決め所に全面の絵", "x1", dict(fig=("illu", good_B)), "決め所"),
                                  ("写真のカットに冒頭の絵", "x2", dict(photo="a.jpg", intro=dict(illu=good_B)), "写真"),
                                  ("「再現イラスト」の種類なのにパネルで書いた", "x3",
                                   dict(fig=("panel", dict(blocks=[]))), "再現イラスト")):
        bad = [b for b in judge_cut(cid, spec, {cid: kind})[0] if b.startswith("⑦")]
        good = bool(bad)
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照⑦：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照④：出典の無い場面（上の層に出典が出ない）
    f = F.illu(**dict(good_B))
    f.illu["src"] = ""
    ov = IL.overlay_svg(f.illu["view"], f.illu["src"])
    good = "出典" not in ov
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照④：出典を空にすると上の層に出典が出ない（門番が拾う前提）")
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import cuts
    kind_of = {c: p.get("kind") for c, p in cuts.PLAN.items()}
    targets = {c: s for c, s in sorted(cuts.SPEC.items())
               if (s.get("fig") or ("",))[0] in ("illu", "illu_pair") or (s.get("intro") or {}).get("illu")
               or kind_of.get(c) == "再現イラスト"}
    others = {c: s for c, s in cuts.SPEC.items() if c not in targets}
    if not targets:
        print("⚠️ 再現イラストのカットが0件（この回に案C が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
    bad_all, n_all = 0, 0
    for cid, spec in list(targets.items()) + list(others.items()):
        bad, n = judge_cut(cid, spec, kind_of)
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {b}")
        elif cid in targets:
            print(f"✓ {cid}（{kind_of.get(cid)}）: 照合 {n}件")
    miss = sorted(c for c, k in kind_of.items() if k == "再現イラスト" and c not in cuts.SPEC)
    print(f"\n（参考）PLAN が「再現イラスト」でまだ SPEC の無いカット {len(miss)}：{' '.join(miss)}")
    print(f"{'✓' if not bad_all else '🔴'} 再現イラスト {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
