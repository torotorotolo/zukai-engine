# -*- coding: utf-8 -*-
"""check_boxes.py — 箱の型（流れ図・書類の再現図・並べ図＝`tools/boxes.py`）の**言葉・つながり・形**を記録と照らす
（2026-09-29 新設・14本目 ⑤b-6）。

■ なぜ要るか
  流れ図は「誰が・どの罪で・どうなったか」を箱のつながりで言う＝**つなぎ違い1本で事実が変わる**（1等航海士に7年の箱を
  つなぐ・無罪の箱を2審でなく1審に置く）。第11章は名前を出さない・人の形を使わない・赤を使わない（責める形にしない）。
  🔴 §5b-88・§5b-93：記録の値（役職・罪名・結果・刑・席の数・欄の名・原因の項目）は**この門番の側に持つ**（`REC_*`）。
  🔴 焼く直前の SVG を読む（画面の文字は `<text>` を全部・席は `data-q="seat"` の四角を数える）。

■ 測るもの
  流れ図 ① 画面の文字が全部、記録の表の言葉（`allowed()`）＝名前・記録に無い言葉が紛れ込まない
         ② 役職→罪名→結果（列＝裁判所）のつながり＝`REC_VERDICT`・役職→刑（点線・大法院の列）＝`REC_SENT`
         ③ 席の数＝裁判官の数（`REC_SEATS`）・灯した席は 0 か全部（全員一致）④ 甲板部・機関部の役職の数と並び＝`REC_CREW`
         ⑤ 赤（ALERT）を使わない・円（人の頭に読める形）を使わない ⑥ 部品の rec の頁
  書類   ⑦ 表題・欄の名・行き来の箱＝`REC_FORM`（報告書の文にあるものだけ）・欄に値を書かない（記録が「未記入」）・「再現」の札
  並べ図 ⑧ 項目＝`REC_CAUSE`・2つ以上・全部同じ大きさと色（どれかを目立たせない）・項目のほかに絵を置かない（場面にしない）

■ 使い方
    python tools/check_boxes.py              # 全カット
    python tools/check_boxes.py --selftest   # 物差しの検算（陽性対照＝名前・つなぎ違い・席の数・赤・欄・形を壊す）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

from check_qty import ATTR, EL, _els, _recs, _unesc  # noqa: E402

# ══════════════════════════════════════════════════════════
#  🔴 §0b（題材を替えるとき空にする場所）：記録の言葉・値と頁（この回）
#     🔴 2026-09-30（15本目 リノ ⑤b-1）：**空にした**。14本目（セウォル号）の表は selftest の見本 `tools/fixture_ep14.py`
#        （GATES["check_boxes"]・値は1つも変えていない）。15本目の書類の再現図（記録簿・参加書類・検査の用紙）を書くチャットで、
#        欄の名と頁を ref/ep15/src/ep15_pages.txt で当てて入れる（空のあいだ、箱のカットは「記録に無い言葉」で止まる）
# ══════════════════════════════════════════════════════════
REC_CREW = {}
REC_ROLE_PAGES = set()
# 🆕 2026-09-30（15本目 ⑤b-5）：原文 ref/ep15/src/ep15_pages.txt で当てた（型の側 ss.FACTORS・MCP・FORM_* とは別に持つ）。
#   流れ図の「role」の箱＝15本目は役職でなく、報告書の文の言葉（重なった要因＝AAB p52・実況の担当がしたこと＝AAB p20）
REC_OTHER_ROLE = {
    "記録も試験も無い改造": {"AAB p52"},        # the undocumented and untested major modifications
    "十分な試験なしのレース": {"AAB p52"},      # operation … in the unique air racing environment without adequate flight testing
    "観客へ避難の案内": {"AAB p20"},            # provided clear evacuation procedures guidance to the crowd
    "救護の人を手伝う": {"AAB p20"},            # assisted first responders
    "医療の応援を頼む": {"AAB p20"},            # requested additional help from medical staff on scene
}
REC_CRIME = {}
REC_VERDICT = {}   # (役職, 罪名, 列) → (結果, 頁)
REC_SENT = {}      # 役職 → (確定した刑, 頁)
REC_SEATS = 0
REC_UNANIMOUS = set()
HEADS = set()
# 🆕 15本目：報告書の鎖（AAB p52 の推定原因）・実況の担当（p20）・2010年の成績（p38）の箱の言葉
REC_MECH = {"ナットの劣化", "ねじのゆるみ", "かたさが落ちる", "板の震え", "棒が折れる", "リンクが折れる", "機首上げ",
            "実況の担当", "いちばん下の組", "勝ち上がる", "ゴールドのレース"}
REC_CHIP = {"風で中止": {"AAB p38"}}           # that race was cancelled due to wind
# 🆕 15本目：書類の再現図（表題 → 欄の名・行き来の箱・欄の値＝記録の文にある値だけ・頁）
REC_FORM = {
    "記録簿（2011年7月29日）": dict(fields={"機体の総時間"}, ends=set(), values={"機体の総時間": "1,453.6時間"},
                                  rec={"AAB p15", "AAB p16"}),
    "記録簿（2009年9月22日）": dict(fields={"試験飛行の時間", "署名"}, ends=set(),
                                  values={"試験飛行の時間": "終えた", "署名": "パイロット本人"}, rec={"AAB p15"}),
    "参加の書類（2009年）": dict(fields={"大きな改造をしたか"}, ends=set(), values={"大きな改造をしたか": "はい"},
                             rec={"AAB p37"}),
    "参加の書類（2009年・2010年）": dict(fields={"年齢"}, ends=set(), values={"年齢": "59"}, rec={"AAB p12"}),
    "技術検査の用紙": dict(fields={"備考", "承認の日付"}, ends={"レースのコース"},
                        values={"備考": "トリムタブのねじが短すぎる", "承認の日付": "2011年9月12日"}, rec={"AAB p37"}),
    "技術検査の決まり（付録E）": dict(fields={"技術委員会の承認"}, ends=set(),
                                 values={"技術委員会の承認": "機体の状態や、飛べるかを表さない"}, rec={"AAB p37"}),
    "技術検査の用紙（事故のあと）": dict(fields={"指摘", "直した中身", "再検査"}, ends={"レースのコース"}, values={},
                                  rec={"CAROL p5010"}),
}
REC_CAUSE = {}
MARKS = {"？"}
EXTRA = {"模式図"}


def allowed():
    """流れ図の画面に出してよい言葉＝**いまの**記録の表から組む（2026-09-30 15本目 ⑤b-1）。
    ⚠️ 以前は読み込みの瞬間に組んだ定数（ALLOWED）だった＝表を selftest の見本に差し替えても空のまま残る形だった。"""
    return ({t for v in REC_CREW.values() for t in v} | set(REC_OTHER_ROLE) | set(REC_CRIME) | {"有罪", "無罪"}
            | {s for s, _ in REC_SENT.values()} | HEADS | REC_MECH | set(REC_CHIP) | MARKS | EXTRA)
ALERTS = None     # jiko_style の赤（読み込んでから埋める）
TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')


def _texts(svg):
    """画面の文字（注と出典の行を除く）。"""
    out = []
    for m in TEXT.finditer(svg):
        q = dict(ATTR.findall(m[1])).get("data-q", "")
        if q != "note":
            out.append((q, _unesc(m[2])))
    return out


def _alert_bad(svg):
    import jiko_style as J
    return [f"赤（{c}）を使っている＝責める形にしない" for c in (J.ALERT, J.ALERT_DIM) if c.lower() in svg.lower()]


# ══════════════════════════════════════════════════════════
#  流れ図
# ══════════════════════════════════════════════════════════
def judge_flow(f):
    svg = f.lab + "".join(f.stages)
    bad, n = [], 0
    ok_words = allowed()
    for q, t in _texts(svg):
        n += 1
        if t not in ok_words:
            bad.append(f"画面の文字「{t}」（{q or '印なし'}）が記録の表の言葉に無い＝名前・記録に無い言葉を書かない")
    bad += _alert_bad(svg)
    if "<circle" in svg:
        bad.append("円を使っている（人の頭に読める形＝人の形を使わない）")
    els = _els(svg)
    seats = sum(1 for e in els if e["q"] == "seat")
    on = sum(1 for e in els if e["q"] == "seat_on")
    n += 2
    if seats not in (0, REC_SEATS):
        bad.append(f"席が {seats} 個（裁判官は {REC_SEATS} 人＝判決 p79〜81）")
    if on not in (0, seats):
        bad.append(f"灯した席が {on}／{seats}（全員一致なら全部・そうでなければ灯さない）")
    parts = [p for p in f.mech["parts"]]
    nodes = {p["id"]: p for p in parts if p["k"] in ("role", "crime", "res")}
    edges = [p for p in parts if p["k"] == "edge"]
    ins = {}
    for e in edges:
        for t in (e["to"] if isinstance(e["to"], list) else [e["to"]]):
            ins.setdefault(t, []).append(e)
    # ⑥ 部品の頁
    for p in nodes.values():
        n += 1
        if p["k"] == "role":
            ok = (p["t"] in REC_OTHER_ROLE and _recs(p["rec"]) & REC_OTHER_ROLE[p["t"]]) or \
                 (p["t"] not in REC_OTHER_ROLE and _recs(p["rec"]) & REC_ROLE_PAGES)
        elif p["k"] == "crime":
            ok = _recs(p["rec"]) & REC_CRIME.get(p["t"], set())
        else:
            ok = True     # 結果の頁は ② で組ごとに見る
        if not ok:
            bad.append(f"箱「{p['t']}」の rec {p['rec']} が記録の頁と合わない")

    def up(nid, seen=()):
        """nid から矢印を逆にたどった（役職の list, いちばん近い罪名, 点線か）。"""
        roles, crime, lead = [], None, False
        for e in ins.get(nid, []):
            lead |= e.get("style") == "leader"
            for fr in (e["fr"] if isinstance(e["fr"], list) else [e["fr"]]):
                if fr in seen:
                    continue
                p = nodes.get(fr)
                if not p:
                    continue
                if p["k"] == "role":
                    roles.append(p["t"])
                else:
                    r2, c2, _ = up(fr, seen + (nid,))
                    roles += r2
                    crime = crime or (p["t"] if p["k"] == "crime" else c2)
        return roles, crime, lead

    unanimous = False
    for p in nodes.values():
        if p["k"] != "res":
            continue
        roles, crime, lead = up(p["id"])
        n += 1
        if not roles:
            bad.append(f"結果の箱「{p['t']}」（{p['col']}）に役職がつながっていない")
            continue
        for r in roles:
            n += 1
            if crime:
                want = REC_VERDICT.get((r, crime, p["col"]))
                if not want:
                    bad.append(f"「{r}→{crime}→{p['t']}（{p['col']}）」は記録の表に無い組")
                elif want[0] != p["t"] or not (_recs(p["rec"]) & want[1]):
                    bad.append(f"「{r}→{crime}」の{p['col']}の結果が「{p['t']}」（記録は「{want[0]}」{sorted(want[1])}）")
                unanimous |= (r, crime) in REC_UNANIMOUS and p["col"] == "c3"
            else:
                want = REC_SENT.get(r)
                if not want or want[0] != p["t"] or p["col"] != "c3" or not (_recs(p["rec"]) & want[1]):
                    bad.append(f"「{r}」の刑の箱が「{p['t']}」（{p['col']}）（記録は {want and want[0]}・大法院の列）")
                if not lead:
                    bad.append(f"「{r}」の刑は点線でつなぐ（罪名の矢印と読み分ける）")
    if on and not unanimous:
        bad.append("席が灯っているのに、全員一致の記録（REC_UNANIMOUS）の結果が無い")
    # ④ 甲板部・機関部の役職（cb02）
    grp = {}
    for p in parts:
        if p["k"] == "role" and p.get("grp"):
            grp.setdefault(p["grp"], []).append(p["t"])
    for g, ts in grp.items():
        n += 1
        if sorted(ts) != sorted(REC_CREW.get(g, [])):
            bad.append(f"{g}の役職 {len(ts)}人 {ts} が記録（判決 p2〜3）の {len(REC_CREW.get(g, []))}人と違う")
    for p in parts:
        if p["k"] == "chip":
            n += 1
            if not (_recs(p["rec"]) & REC_CHIP.get(p["t"], set())):
                bad.append(f"札「{p['t']}」の rec {p['rec']} が記録の頁と合わない")
    return bad, n


# ══════════════════════════════════════════════════════════
#  書類の再現図
# ══════════════════════════════════════════════════════════
def judge_form(f):
    svg = f.lab + "".join(f.stages)
    els = _els(svg)
    bad, n = [], 3
    title = next((_unesc(e["text"]) for e in els if e["q"] == "ftitle"), "")
    r = REC_FORM.get(title)
    if not r:
        return [f"書類の表題「{title}」が記録の表に無い"], n
    fields = {_unesc(e["text"]) for e in els if e["q"].startswith("field|")}
    ends = {_unesc(e["text"]) for e in els if e["q"].startswith("ntext|role|")}
    if not fields <= r["fields"]:
        bad.append(f"欄 {sorted(fields - r['fields'])} は報告書の文に無い（無い欄を描かない）")
    if not ends <= r["ends"]:
        bad.append(f"行き来の箱 {sorted(ends - r['ends'])} が記録に無い")
    for e in els:
        if e["q"].startswith("fval|"):
            n += 1
            nm = e["q"].split("|", 1)[1]
            if r["values"].get(nm) != _unesc(e["text"]):
                bad.append(f"欄「{nm}」に値「{_unesc(e['text'])}」（記録は {r['values'].get(nm) or '未記入'}）")
    tag = next((_unesc(e["text"]) for e in els if e["q"] == "reprot"), "")
    if tag != "再現":
        bad.append(f"「再現」の札が無い（「{tag}」）＝自作の用紙だと画面で言う")
    for p in f.mech["parts"]:
        n += 1
        rs = _recs(p["rec"])
        if not (rs & r["rec"]):
            bad.append(f"{p['k']} の rec {p['rec']} が記録の頁 {sorted(r['rec'])} と合わない")
        for fd in p.get("fields") or []:
            n += 1
            if not (_recs(fd["rec"]) & r["rec"]):
                bad.append(f"欄「{fd['t']}」の rec {fd['rec']} が記録の頁と合わない")
    bad += _alert_bad(svg)
    return bad, n


# ══════════════════════════════════════════════════════════
#  並べ図
# ══════════════════════════════════════════════════════════
def judge_row(f):
    svg = f.lab + "".join(f.stages)
    els = _els(svg)
    bad, n = [], 2
    items = [e for e in els if e["q"].startswith("item|")]
    if len(items) < 2:
        bad.append(f"並べる項目が {len(items)} つ（2つ以上を同じ形で並べる）")
    forms = {(e["a"].get("width"), e["a"].get("height"), e["a"].get("stroke")) for e in items}
    if len(forms) > 1:
        bad.append(f"項目の箱の形か色が揃っていない {sorted(forms)}＝どれかを目立たせない")
    for q, t in _texts(svg):
        n += 1
        if not (q.startswith("itext|") and t in REC_CAUSE):
            bad.append(f"画面の文字「{t}」（{q or '印なし'}）が原因の項目の表に無い＝並べ図に項目のほかを書かない")
    for e in els:
        if e["q"] not in ("note",) and not e["q"].startswith(("item|", "itext|")):
            bad.append(f"並べ図に項目のほかの部品（{e['q']}）＝場面にしない")
    if re.search(r"<(circle|path|polygon)\b", svg):
        bad.append("並べ図に線や絵（path・circle）がある＝場面にしない")
    for p in f.mech["parts"]:
        n += 1
        if not (_recs(p["rec"]) & REC_CAUSE.get(p["t"], set())):
            bad.append(f"項目「{p['t']}」の rec {p['rec']} が記録の頁と合わない")
    bad += _alert_bad(svg)
    return bad, n


def judge(kw):
    import boxes as B
    f = B.boxes(**kw)
    return {"flow": judge_flow, "form": judge_form, "row": judge_row}[kw["view"]](f)


# ══════════════════════════════════════════════════════════
#  物差しの検算
# ══════════════════════════════════════════════════════════
def selftest_ep15():
    """15本目（⑤b-5）の書類の再現図と鎖の検算＝**本番の表（この門番の REC_*＝15本目）**で回す。
    🔴 16本目の ⑤b-1 で本番の表を空にしたら、この見本を fixture_ep15 へ移して差し込む（14本目と同じ）"""
    from cuts import ss
    entry = dict(view="form", form=ss.FORM_ENTRY09, note="n", src="s",
                 steps=[dict(add=dict(k="paper")), dict(add=dict(k="fill", f="大きな改造をしたか"))])
    bad_v = dict(ss.FORM_ENTRY09, fields=[dict(ss.FORM_ENTRY09["fields"][0], v="いいえ")])
    bad_f = dict(ss.FORM_ENTRY09, fields=[dict(t="飛んだ時間", rec="AAB p37")])     # 型は通す＝門番が止めるか
    chain = dict(view="flow", layout=ss.CHAIN2, steps=[dict(add=ss.chain_links())], note="n", src="s")
    bad_w = dict(chain, layout=dict(heads=ss.CHAIN2["heads"][:5] + [dict(ss.CHAIN2["heads"][5], t="墜落の原因")]))
    cases = [("15本目 正しい参加の書類（後から「はい」）", entry, True),
             ("🔴 15本目 陽性対照：書き込む値が記録と違う（いいえ）", dict(entry, form=bad_v), False),
             ("🔴 15本目 陽性対照：報告書の文に無い欄", dict(entry, form=bad_f, steps=[dict(add=dict(k="paper"))]), False),
             ("15本目 正しい報告書の鎖", chain, True),
             ("🔴 15本目 陽性対照：鎖に記録の表に無い言葉", bad_w, False)]
    ok = True
    for name, kw, want in cases:
        try:
            bad, _ = judge(kw)
        except ValueError as e:
            bad = [f"型が止まった：{e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    return ok


def selftest():
    # 🔴 2026-09-30（15本目 ⑤b-5）：先に15本目の書類と鎖を本番の表で検算してから、14本目の見本に差し替える
    ok15 = selftest_ep15()
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（本番の表は回ごとに空にする＝§0b）＝この処理の中だけ14本目にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    import boxes as B
    from cuts import ss
    ok = True
    cap = [ss.ct("r_captain"), ss.ct("x_cap"), ss.ce("r_captain", "x_cap"), ss.ct("o_cap"), ss.ce("x_cap", "o_cap"),
           dict(k="seats_on", n=13, rec="判決 p39")]
    sent = [ss.ct("r_mate1"), ss.ct("s_mate1"), ss.ce("r_mate1", "s_mate1", style="leader")]
    flow = dict(view="flow", layout=ss.CT, steps=[dict(add=cap), dict(add=sent)], src="s")
    crew = dict(view="flow", layout=ss.CT, steps=[dict(add=ss.CREW15)], src="s")
    form = dict(view="form", form=ss.FORM_PRE, steps=[dict(add=[dict(k="end", id="ship"), dict(k="paper"),
                                                                dict(k="edge", fr="ship", to="paper")])], src="s")
    row = dict(view="row", slots=3, steps=[dict(add=[ss.cause("rudder"), ss.cause("fault")])], src="s")

    def run(name, kw, want):
        nonlocal ok
        try:
            bad, _ = judge(kw)
        except (ValueError, KeyError) as e:
            bad = [f"型が止まった：{type(e).__name__} {e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}（{'合格' if want else '不合格'}のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    run("正しい流れ図（船長→殺人・殺人未遂→有罪・13席・1等航海士→懲役12年）", flow, True)
    run("正しい船員15人（甲板部8・機関部7）", crew, True)
    run("正しい書類の再現図（乗船人員・貨物量・空欄）", form, True)
    run("正しい並べ図（舵の使い方？・装置の故障？）", row, True)
    run("🔴 陽性対照：役職の箱に名前（山田船長）", dict(flow, steps=[dict(add=[ss.ct("r_captain", t="山田船長")] + cap[1:])]), False)
    run("🔴 陽性対照：刑のつなぎ違い（1等航海士→懲役7年）",
        dict(flow, steps=[dict(add=cap), dict(add=[ss.ct("r_mate1"), ss.ct("s_mate2", row="1等航海士"),
                                                   ss.ce("r_mate1", "s_mate2", style="leader")])]), False)
    run("🔴 陽性対照：無罪の箱を1審の列に（舵の過失）",
        dict(flow, steps=[dict(add=[ss.ct("r_mate3"), ss.ct("x_rudder"), ss.ce("r_mate3", "x_rudder"),
                                    ss.ct("o_rud2", col="c1"), ss.ce("x_rudder", "o_rud2")])]), False)
    run("🔴 陽性対照：席が12", dict(flow, layout=dict(ss.CT, seats=dict(ss.CT["seats"], n=12))), False)
    run("🔴 陽性対照：甲板部の役職が1人欠ける", dict(crew, steps=[dict(add=ss.CREW15[:2] + ss.CREW15[3:])]), False)
    run("🔴 陽性対照：書類に報告書に無い欄（船長の署名）",
        dict(form, form=dict(ss.FORM_PRE, fields=list(ss.FORM_PRE["fields"]) + [dict(t="船長の署名", rec="海審 p1037")])),
        False)
    run("🔴 陽性対照：書類の欄に値（乗船人員 476）",
        dict(form, form=dict(ss.FORM_PRE, fields=[dict(t="乗船人員", rec="海審 p1037", v="476人")])), False)
    run("🔴 陽性対照：並べ図に記録に無い項目（爆発？）",
        dict(row, steps=[dict(add=[ss.cause("rudder"), dict(k="item", t="爆発？", rec="特調委 p3013")])]), False)
    run("🔴 陽性対照：並べ図の項目が1つ", dict(row, steps=[dict(add=[ss.cause("rudder")])]), False)

    def broken(name, obj, attr, val, kw):
        nonlocal ok
        keep = getattr(obj, attr)
        setattr(obj, attr, val)
        try:
            bad, _ = judge(kw)
        except (ValueError, KeyError) as e:
            bad = [f"型が止まった：{e}"]
        finally:
            setattr(obj, attr, keep)
        ok &= bool(bad)
        print(f"  {'OK' if bad else '🔴 NG'} 🔴 陽性対照（型を壊す）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    broken("結果の箱を赤で描く（KSTY）", B, "KSTY", dict(B.KSTY, res=("ALERT", 28, 40)), flow)
    broken("「再現」の札を書かない（REPRO）", B, "REPRO", "", form)
    import titan_fig as F
    rect0 = F.rect
    cnt = [0]

    def uneven(x, y, w, h, *a, **k):
        cnt[0] += 1
        return rect0(x, y, w + (40 if cnt[0] == 1 else 0), h, *a, **k)
    broken("並べ図の最初の箱だけ広く描く（F.rect）", F, "rect", uneven, row)
    ok = ok and ok15
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import fixture_ep14
    fixture_ep14.restore()       # 🔴 15本目 ⑤b-2：selftest で差し込んだ14本目の見本を本番の表に戻す（戻さないと14本目の表で本番を測る）
    import cuts
    targets = {c: s["fig"][1] for c, s in sorted(cuts.SPEC.items()) if s.get("fig") and s["fig"][0] == "boxes"}
    if not targets:
        print("⚠️ boxes のカットが0件（この回に流れ図・書類・並べ図が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
        return 0
    bad_all, n_all = 0, 0
    for cid, kw in targets.items():
        bad, n = judge(kw)
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {cid}（boxes・{kw['view']}）: {b}")
        else:
            print(f"✓ {cid}（boxes・{kw['view']}）: 言葉・つながり・形 {n}件が記録と合う")
    print(f"\n{'✓' if not bad_all else '🔴'} 箱の型 {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
