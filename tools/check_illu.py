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
SEC = re.compile(r"(約)?\s*(\d+(?:\.\d+)?)\s*秒")          # 15本目：秒の札（「0.27秒」「約9.1秒」）
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


HMS = re.compile(r"(\d{1,2})\s*[時:：]\s*(\d{1,2})(?:\s*[分:：]\s*(\d{1,2}(?:\.\d+)?))?")


def _hms(s, end):
    """場面の時刻 at・群れの上限 until を秒まで（15本目 ⑤b-3）。秒が無い書き方は、at（end=True）はその分の終わり（59.99秒）
    ＝その分のどこかもしれない＝**遅い側に倒す**（fail closed）、上限（end=False）はその分の頭。14本目（"9:46" < "9:47"）は前と同じ答え"""
    m = HMS.search(str(s or ""))
    if not m:
        return None
    sec = float(m.group(3)) if m.group(3) else (59.99 if end else 0.0)
    return (int(m.group(1)), int(m.group(2)), sec)


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


def judge_scene(sc, where, docs=None, pages=None, split=None, until=None, sec_ok=None, clock_ok=None, counts=None,
                roles=None):
    """場面1つを測る。返り値＝(食い違いの一覧, 照合した件数)。
    15本目 ⑤b-2 から：sec_ok（秒の札の表）・clock_ok（時計の札の表）・counts（描いてよい数）＝その回の表が空なら測らない
    15本目 ⑤b-3 から：roles（その回に置いてよい役割＝dict(sprite=(…), crowd=(…))・`cuts.ss.ILLU_ROLES`）。空なら型の既定
       （illu.ROLES・CROWD_ROLES＝14本目の船）"""
    ss = _ss()
    docs = docs if docs is not None else ss.REC_DOCS
    pages = pages if pages is not None else _pages()
    split = split if split is not None else ss.ILLU_SPLIT_TIMES
    until = until if until is not None else ss.ILLU_CROWD_UNTIL
    sec_ok = sec_ok if sec_ok is not None else (getattr(ss, "ILLU_SEC_OK", None) or {})
    clock_ok = clock_ok if clock_ok is not None else tuple(getattr(ss, "ILLU_CLOCK_OK", None) or ())
    counts = counts if counts is not None else (getattr(ss, "ILLU_COUNTS", None) or {})
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
    #   🔴 15本目 ⑤b-3：置いてよい役割は回ごとの表（`ss.ILLU_ROLES`）＝15本目は型紙（1人ずつ数えられる影）0・群れは観客だけ
    #      （パイロット・審判・救護・検査員・整備の仲間を置くと止まる＝映像方針 §6②）。時刻は秒まで（`_hms`）
    roles = roles if roles is not None else (getattr(ss, "ILLU_ROLES", None) or {})
    sprite_ok = tuple(roles["sprite"]) if "sprite" in roles else IL.ROLES
    crowd_ok = tuple(roles["crowd"]) if "crowd" in roles else CROWD_ROLES
    at = _hms(sc.get("at"), end=True)
    for p in sc["parts"]:
        role = p.get("role")
        if role is None:
            continue
        n += 1
        if p.get("kind") == "sprite":
            if role not in sprite_ok:
                bad.append(f"②{where}：型紙の影（1人ずつ数えられる形）の役割「{role}」は {sprite_ok} だけ"
                           "（群れの人は群れの型でだけ＝1人を抜き出さない）")
        elif role in crowd_ok:
            if not p.get("crowd"):
                bad.append(f"②{where}：群れの部品 {p['id']} が群れの型（crowd_layout）で描かれていない")
            for c in p.get("crowd") or []:
                bad += [f"②{where}：{b}" for b in IL.crowd_uncountable(c["layout"], c["x0"], c["x1"])]
            shown = any(float(k.get("a", 1.0)) > 0.0 for k in p["keys"])
            if shown:
                lim = _hms(until, end=False)
                if at is None:
                    bad.append(f"②{where}：群れを出す場面なのに時刻 at が無い")
                elif lim is None or at >= lim:
                    bad.append(f"②{where}：群れを {sc['at']} の場面に出した（{until} より前だけ＝§5b-74②。"
                               "秒の無い時刻はその分の終わりとみなす）")
        else:
            bad.append(f"②{where}：この回に置けない役割「{role}」（型紙 {sprite_ok}・群れ {crowd_ok}）")
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
            # 15本目〜：秒の札は表の値だけ（#42 の 5.3秒・EXIF から推した時刻を出さない＝映像方針 §6 ⑤）
            if sec_ok:
                for m in SEC.finditer(txt):
                    n += 1
                    if m.group(2) not in sec_ok:
                        bad.append(f"⑤{where}：札「{txt}」の「{m.group(0)}」は表の値でない（AAB p28 の表＝"
                                   f"{sorted(sec_ok, key=float)}）")
                if hm and f"{hm[0]}:{hm[1]:02d}" not in clock_ok:
                    n += 1
                    bad.append(f"⑤{where}：札「{txt}」の時刻は表の時刻でない（{clock_ok}＝写真の EXIF から推した時刻は出さない）")
    # ③' 15本目〜：描いた物の数（部品の obj の合計＝描く側の部品そのもの）＝記録の数（`cuts.ss.ILLU_COUNTS`）
    if counts:
        drawn_obj = {}
        for p in sc["parts"]:
            for k, v in (p.get("obj") or {}).items():
                drawn_obj[k] = drawn_obj.get(k, 0) + int(v)
        for k, v in drawn_obj.items():
            n += 1
            if k not in counts:
                bad.append(f"③{where}：{k} を {v} 描いたのに記録の数（cuts.ss.ILLU_COUNTS）が無い")
            elif v != counts[k][0]:
                bad.append(f"③{where}：{k} を {v} 描いた（記録は {counts[k][0]}＝{counts[k][1]}）")
            else:
                bad += check_recs([counts[k][1]], where, docs, pages)
    # ⑧ 上から見た絵の縮尺
    #   🔴 ⑤b-3：小さく戻す絵（illu_pair の枠 box）は、全面の絵を枠の幅へ縮めて置く（build_jiko.illu_minis）＝画面の上の縮尺は
    #      scale × 1920 ÷ 枠の幅（本番と同じ幾何で測る。c109 問い3 を寄せて×を読めるようにした＝枠 560 で 1.5÷2.4×3.43＝2.1）
    if "上から" in (sc.get("view") or ""):
        n += 1
        eff = float(sc["scale"]) * (IL.W / float(sc["box"][2])) if sc.get("scale") and sc.get("box") else sc.get("scale")
        if not eff or float(eff) < 1.5:
            bad.append(f"⑧{where}：上から見た絵の画面の上の縮尺 {eff} メートル／画素（1.5 以上＝人が1画素に満たない縮尺だけ）")
    # 15本目 ⑤b-2：空の中の事故機（RB）は地面に触れて見えない（下見：90度前後の翼の下の先が地平線より下＝「翼が地面に触れた」絵
    #   ＝記録を越える＝落ちたのは約9.1秒）。後ろから見た段ごとに、描く側と同じ幾何（_rb_anchors）で翼の先が地平線より上か
    if sc["place"] == "RB":
        for i, st in enumerate([sc["start"]] + sc["states"]):
            if st["view"] == "rear":
                n += 1
                an = IL._rb_anchors(st)
                low = max(an["lwing"][1], an["rwing"][1])
                # 🔴 ⑤b-3：余白 8画素では、地平線の16画素上の翼の先が手前の丘と砂漠の境に乗って「触れた」絵に見えた（c307 の
                #    試し焼き）＝すき間の下限 RB_GAP（50画素）
                if low > IL.RB_HZ - IL.RB_GAP:
                    bad.append(f"⑨{where}：段{i}の傾き {st['roll']}度で翼の下の先 y={low:.0f} が地平線 {IL.RB_HZ:.0f} の"
                               f"{IL.RB_HZ - low:.0f}画素上（{IL.RB_GAP:.0f}画素未満＝地面に触れた絵に見える＝落ちたのは約9.1秒）")
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
    # 冒頭の絵（intro の illu）＝画面ごと入れ替える（重ねない）。15本目 ⑤b-2 から、あとに来てよいのは
    #   決め所（quote＝14本目 c102・15本目 c104）・全面の絵（illu＝c101 B→A）・時間の帯（axis＝c312 A→帯）
    #   ⑤b-3：尾翼の模式図（tail＝c302 D→模式図）も（14本目の「写真→図」と同じ画面ごとの入れ替え）
    if it and fig[0] not in ("quote", "illu", "axis", "tail"):
        bad.append(f"⑦{cid}：冒頭の絵（intro の illu）のあとは 決め所（quote）・全面の絵（illu）・時間の帯（axis）・尾翼の模式図（tail）だけ")
    elif it and fig[0] == "illu" and kind != "再現イラスト":
        bad.append(f"⑦{cid}：冒頭の絵のあとが全面の絵なら画面の種類は「再現イラスト」（いまは「{kind}」）")
    elif it and fig[0] in ("quote", "axis", "tail") and kind != "混ざり":
        bad.append(f"⑦{cid}：冒頭の絵のあとが決め所・時間の帯・模式図なら画面の種類は「混ざり」（いまは「{kind}」）")
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


def _run(cases, kw):
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
    return ok


def _expect(name, bad, head):
    good = any(b.startswith(head) for b in bad)
    print(f"  {'OK' if good else '🔴 NG'} {name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    return good


def selftest_ep15():
    """15本目（リノ・⑤b-2）の置き場 RA・RB・RD の物差しの検算＝**本番の表（cuts.ss＝15本目）**で回す。
    🔴 16本目の ⑤b-1 で本番の表を空にしたら、この表（REC_DOCS・ILLU_SEC_OK・ILLU_CLOCK_OK・ILLU_COUNTS）を
       fixture_ep15 へ移して差し込む（14本目と同じ＝記憶 project-jiko-rules-index §0b）"""
    ss = _ss()
    kw = dict(docs=dict(ss.REC_DOCS), pages=_pages(), split=tuple(ss.ILLU_SPLIT_TIMES), until=ss.ILLU_CROWD_UNTIL,
              sec_ok=dict(ss.ILLU_SEC_OK), clock_ok=tuple(ss.ILLU_CLOCK_OK), counts=dict(ss.ILLU_COUNTS),
              roles=dict(ss.ILLU_ROLES))
    # ⑤b-3：RC（ボックス席とピット・地上から）＝観客の群れは落ちる瞬間（16:24:38）より前・役割は spectators だけ
    good_pits = dict(place="RC", at="16:24:28", start=dict(view="pits", crowd="on", fuel="on", cam=1.12, pan=-200.0),
                     rec="AAB p19（ピットのあたりにも多くの観客・燃料車）",
                     steps=[dict(state=dict(pan=200.0), dur=8.0), dict()])
    good_box = dict(place="RC", at="16:24:28", start=dict(view="box", crowd="on", cam=1.12), rec="AAB p19（観客のボックス席）",
                    steps=[dict(), dict()])
    good_fences = dict(place="RC", start=dict(view="fences"), steps=[dict(), dict(), dict()])
    good_near = dict(place="RA", at="16:24", start=dict(view="near", gg="p7"), rec="AAB p28",
                     steps=[dict(), dict(state=dict(gg="gone", path="on", x="on", box="on"), rec="AAB p28・p19",
                                         tag=[dict(t="パイロン8", at="p8"), dict(t="観客席（ボックス席）", at="box")])])
    good_trace = dict(place="RA", at="16:24", start=dict(view="near", gg="gone", path="on", x="on", box="on"), rec="AAB p28",
                      steps=[dict(state=dict(trace="on"), rec="AAB p28", tag=dict(t="崩れ始め 0秒", at="fall0")),
                             dict(tag=dict(t="約9.1秒", at="x"))])
    good_wide = dict(place="RA", at="16:24", start=dict(view="wide"),
                     steps=[dict(state=dict(laps="on", ring8="on"), rec="#14 p3014・AAB p29"),
                            dict(state=dict(seg67="on"), rec="AAB p29")])
    good_rear = dict(place="RB", at="16:24", start=dict(view="rear", roll=73.0), rec="AAB p28",
                     steps=[dict(state=dict(roll=77.0), rec="AAB p28", tag=dict(t="0秒", xy=(1300, 200))),
                            dict(state=dict(roll=81.0, ail="right"), rec="AAB p28", tag=dict(t="0.27秒", xy=(1300, 200)))])
    good_mix = dict(place="RB", at="16:24", start=dict(view="rear", ground="off", roll=86.0), rec="AAB p28",
                    steps=[dict(state=dict(roll=93.0), rec="AAB p28"),
                           dict(state=dict(view="side", pitch=32.0), rec="AAB p28", tag=dict(t="1.3秒 17.3G", xy=(1300, 200)))])
    good_tail = dict(place="RD", at="16:24", steps=[dict(state=dict(mark="on"), rec="AAB p14")])
    cases = [
        ("15本目 正しい RA near（印が7→8・消えて点線・×・ボックス席）", good_near, True),
        ("15本目 正しい RA near（琥珀の線・0秒と約9.1秒の札）", good_trace, True),
        ("15本目 正しい RA wide（3周の航跡・パイロン8の輪・6〜7の区間）", good_wide, True),
        ("15本目 正しい RB rear（73度から深まる・補助翼）", good_rear, True),
        ("15本目 正しい RB rear→side（93度→機首の上げ・17.3G）", good_mix, True),
        ("15本目 正しい RD tail（尾翼の輪）", good_tail, True),
        ("🔴 15本目 陽性対照⑤：札に表に無い秒（#42 の 5.3秒）",
         dict(good_trace, steps=[dict(state=dict(trace="on"), rec="AAB p28", tag=dict(t="5.3秒", at="x"))]), False),
        ("🔴 15本目 陽性対照⑤：札に表に無い時刻（16時25分）",
         dict(good_rear, steps=[dict(state=dict(roll=77.0), rec="AAB p28", tag=dict(t="16時25分", xy=(1300, 200)))]), False),
        ("🔴 15本目 陽性対照①：航跡を出した段に rec が無い", dict(good_wide, steps=[dict(state=dict(laps="on"))]), False),
        ("🔴 15本目 陽性対照①：傾きを変えた段に rec が無い", dict(good_rear, steps=[dict(state=dict(roll=80.0))]), False),
        ("🔴 15本目 陽性対照①：rec の資料名が表に無い（#42）", dict(good_tail, steps=[dict(state=dict(mark="on"), rec="#42 p5")]), False),
        ("🔴 15本目 陽性対照⑧：上から見た絵に寄りすぎ（cam 1.8＝1.39メートル／画素）",
         dict(good_near, start=dict(view="near", gg="p7", cam=1.8)), False),
        ("15本目 正しい RC pits（ピットの柵の奥の観客・燃料車1台・首振り）", good_pits, True),
        ("15本目 正しい RC box（ボックス席の幕の奥の観客・スタンド）", good_box, True),
        ("15本目 正しい RC fences（2つの柵の寄り・人なし・時刻なし）", good_fences, True),
        ("🔴 15本目 陽性対照②：観客の群れを落ちたあと（16:24:40）の場面に", dict(good_box, at="16:24:40"), False),
        ("🔴 15本目 陽性対照②：秒の無い時刻（16:24＝その分の終わりとみなす）", dict(good_box, at="16:24"), False),
        ("🔴 15本目 陽性対照②：群れを出すのに時刻 at が無い", dict(good_box, at=None), False),
        ("🔴 15本目 陽性対照①：群れを出したのに場面の rec が無い", dict(good_box, rec=None), False),
    ]
    ok = _run(cases, kw)
    # 🔴 陽性対照②（役割）：15本目に14本目の役割（乗客の群れ・船員の型紙）を置く＝回ごとの表で止まる
    sc = IL.scene(**good_box)
    next(p for p in sc["parts"] if p.get("role") == "spectators")["role"] = "passengers"
    ok &= _expect("🔴 15本目 陽性対照②：観客の群れの役割を passengers に（14本目の役割）", judge_scene(sc, "selftest", **kw)[0], "②")
    sc = IL.scene(**good_fences)
    sc["parts"].append(dict(IL._part("pilot", "", "AAB p11"), kind="sprite", role="crew", inst=[dict(path=[(900.0, 600.0)])]))
    ok &= _expect("🔴 15本目 陽性対照②：型紙の影（crew＝1人ずつ数えられる人）を置く", judge_scene(sc, "selftest", **kw)[0], "②")
    # 🔴 陽性対照②（形）：描く側の群れの間隔を壊す（1.15＝重ならない）＝1人ずつ数えられる群れ
    keep = IL.CROWD_STEP
    IL.CROWD_STEP = 1.15
    try:
        bad = judge_scene(IL.scene(**good_pits), "selftest", **kw)[0]
    finally:
        IL.CROWD_STEP = keep
    ok &= _expect("🔴 15本目 陽性対照②（描く側）：ピットの群れが重ならない（数えられる）", bad, "②")
    # 🔴 陽性対照③：RC の燃料車を2台に
    sc = IL.scene(**good_pits)
    g = next(q for q in sc["parts"] if (q.get("obj") or {}).get("fuel_truck"))
    g["obj"] = dict(g["obj"], fuel_truck=2)
    ok &= _expect("🔴 15本目 陽性対照③：RC の燃料車を2台描く", judge_scene(sc, "selftest", **kw)[0], "③")
    # 🔴 位置の正本（`ref/ep15/illu_reno.json`＝`ref/ep15/measure_reno.py` が図の画素から測った値）と `illu.py` の定数が同じか
    #    （写し間違い・手で動かした値を止める。⑤b-2 で scratchpad の手の丸めと 0〜1メートル違っていたのを直した）
    js = HERE / "ref" / "ep15" / "illu_reno.json"
    if js.exists():
        import json
        g = json.loads(js.read_text(encoding="utf-8"))
        diff = [k for k in IL.R_ORDER if tuple(float(x) for x in g["pylons"][k]) != IL.R_PYL[k]]
        diff += ["accident"] if tuple(float(x) for x in g["accident"]) != IL.R_ACC else []
        diff += ["S0"] if tuple(g["S0"]) != IL.R_S0 else []
        diff += [n for n in IL.R_LAPS if [tuple(p) for p in g["laps"][n]] != list(IL.R_LAPS[n])]
        diff += ["showline_deg"] if abs(g["showline_deg"] - IL.R_SHOW_DEG) > 1e-9 else []
        diff += ["R_GG・R_FALL の端"] if (IL.R_GG[-1] != tuple(float(x) for x in g["laps"]["lap3"][-1])
                                        or IL.R_FALL[0] != IL.R_GG[-1] or IL.R_FALL[-1] != IL.R_ACC) else []
        print(f"  {'OK' if not diff else '🔴 NG'} 15本目 位置の正本 illu_reno.json と illu.py の定数: "
              f"{'同じ' if not diff else '違う ' + str(diff)}")
        ok &= not diff
    else:
        print("  ⚠️ 15本目 位置の正本 ref/ep15/illu_reno.json が無い＝照合していない")
    # 🔴 陽性対照③（数）：事故機の印を2つ（部品を複写）・燃料車を2台（地面の obj を壊す）
    sc = IL.scene(**good_near)
    p = next(q for q in sc["parts"] if (q.get("obj") or {}).get("aircraft"))
    sc["parts"].append(dict(p, id="gg2"))
    ok &= _expect("🔴 15本目 陽性対照③：事故機を2つ描く", judge_scene(sc, "selftest", **kw)[0], "③")
    sc = IL.scene(**good_near)
    g = next(q for q in sc["parts"] if (q.get("obj") or {}).get("fuel_truck"))
    g["obj"] = dict(g["obj"], fuel_truck=2)
    ok &= _expect("🔴 15本目 陽性対照③：燃料車を2台描く", judge_scene(sc, "selftest", **kw)[0], "③")
    # 🔴 陽性対照⑧（描く側の定数を壊す）：near の縮尺を 1.2 メートル／画素に
    keep = IL.RA_VIEW["near"]["mpp"]
    IL.RA_VIEW["near"]["mpp"] = 1.2
    try:
        bad = judge_scene(IL.scene(**good_near), "selftest", **kw)[0]
    finally:
        IL.RA_VIEW["near"]["mpp"] = keep
    ok &= _expect("🔴 15本目 陽性対照⑧（描く側）：near の縮尺 1.2", bad, "⑧")
    # 🔴 陽性対照⑨（描く側）：後ろから見た機体を下げて大きく（⑤b-2 の下見の前の値）＝93度で翼の先が地平線に届く
    keep = (IL.RB_CR, IL.RB_KR)
    IL.RB_CR, IL.RB_KR = (960.0, 430.0), 62.0
    try:
        bad = judge_scene(IL.scene(**good_mix), "selftest", **kw)[0]
    finally:
        IL.RB_CR, IL.RB_KR = keep
    ok &= _expect("🔴 15本目 陽性対照⑨（描く側）：後ろから見た機体を下げる（翼の先が地平線に届く）", bad, "⑨")
    # 🔴 陽性対照⑦：冒頭の絵のあとがパネル／時間の帯なのに種類が「再現イラスト」
    for name, spec, kind in (("冒頭の絵のあとがパネル", dict(fig=("panel", dict(blocks=[])), intro=dict(illu=good_tail)), "混ざり"),
                             ("冒頭の絵→時間の帯なのに種類が「再現イラスト」",
                              dict(fig=("axis", dict()), intro=dict(illu=good_tail)), "再現イラスト")):
        bad = [b for b in judge_cut("x9", spec, {"x9": kind})[0] if b.startswith("⑦")]
        ok &= _expect(f"🔴 15本目 陽性対照⑦：{name}", bad, "⑦")
    bad = [b for b in judge_cut("x8", dict(fig=("illu", good_near), intro=dict(illu=good_mix)), {"x8": "再現イラスト"})[0]
           if b.startswith("⑦")]
    print(f"  {'OK' if not bad else '🔴 NG'} 15本目 正しい ⑦：冒頭の絵（B）→ 全面の絵（A）＝再現イラスト: "
          f"{'合格' if not bad else '不合格'}（合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    ok &= not bad
    return ok


def selftest():
    """物差しの検算。正しい場面が通り、わざと壊した場面（陽性対照）が落ちること。"""
    # 🔴 2026-09-30（15本目 ⑤b-2）：先に15本目（本番の表）で RA・RB・RD を検算してから、14本目の見本に差し替える
    ok15 = selftest_ep15()
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（置き場 A〜E の部品の既定の rec が14本目の資料を指す）。
    #    本番の表は回ごとに空にする（§0b）＝この処理の中だけ14本目の資料の表・原文・時刻にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    _pages.cache_clear()          # 🔴 原文の頁の読み込みは覚えている（lru_cache）＝15本目の原文を捨てて14本目を読み直す
    try:
        ok = _selftest_ep14() and ok15
    finally:
        # 🔴 2026-09-30（15本目 ⑤b-2）：selftest のあと本番の表に戻す（戻さないと、本番の照合が14本目の出典の表で15本目の絵を
        #    測る＝⑤b-1 から ⑤b-2 まで本番に案C が無かったので表に出なかった穴）
        fixture_ep14.restore()
        _pages.cache_clear()
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def _selftest_ep14():
    """14本目（セウォル号）の見本での検算（fixture_ep14 を差し込んだ中で呼ぶ）。"""
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
