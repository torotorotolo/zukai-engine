# -*- coding: utf-8 -*-
"""check_qty.py — 量の型（棒・マス目・人の形＝`tools/qty.py`）の**長さ・数・色**を記録と照らす（2026-09-29 新設・14本目 ⑤b-6）。

■ なぜ要るか
  棒の長さ・マスの数・人の形の数は、数字を画面に書かない（§5b-9）ぶん**形そのものが数**になる。1割長い棒・1人欠けた並びは
  字幕と画面が食い違う。🔴 §5b-88・§5b-93：記録の値は**この門番の側に持つ**（`REC_*`）・読み方も型と別に書く。
  🔴 焼く直前の SVG を読む（型が置いた `data-q`／`data-p` の要素の画素と色＝描く側と同じ関数 `qty.qty()` の出力）。

■ 測るもの
  棒   ① 目盛りの線の画素と**画面の目盛りの文字**から一次式 → 棒の右端を値へ戻す＝`REC_QTY`（±1.2画素ぶん）
       ② 棒の左端＝0 の目盛り・最初の目盛りの文字が「0」 ③ 破線の枠（もとの長さ）＝`REC_GHOST` ④ 部品の rec の頁
  マス目 ⑤ マスの数・✓・✕ の数＝`REC_GRID`・「1マス＝1項目」
  人の形 ⑥ 形の数（`data-p` の数）＝`REC_PEOPLE["乗っていた人"]`・全部同じ大きさ・重ならない・枠の中・「1つ＝1人」
       ⑦ 段ごとに、凡例の色の形の数（章の色に置き換えたあと・後から描いた色が勝つ）＝凡例の名の記録の数
       ⑧ 子の凡例の形は親の形の内・灯した色どうしと沈んだ色が取り違えない距離（ΔE 25＝check_color.DE_MIN）
       ⑨ 🔴 `PEOPLE_CUTS` の外で使わない（亡くなった方の数に使わない＝ルール §C-1 #59）・凡例に死の言葉を使わない
  全部  ⑩ 画面の数字は目盛り・単位の札・注（出典）の中だけ（棒やマスに数字を書かない＝§5b-9）

■ 使い方
    python tools/check_qty.py              # 全カット
    python tools/check_qty.py --selftest   # 物差しの検算（陽性対照＝型の定数や描き方を壊す・記録と違う値や頁）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

# ══════════════════════════════════════════════════════════
#  🔴 §0b（題材を替えるとき空にする場所）：記録の値と頁（この回）。
#     🔴 2026-09-30（15本目 リノ ⑤b-1）：**空にした**。14本目（セウォル号）の表は selftest の見本 `tools/fixture_ep14.py`
#        （GATES["check_qty"]・値は1つも変えていない）。15本目の棒（速さ・時間・G ほか＝映像方針 §11-2）を書くチャットで、
#        値と頁を ref/ep15/src/ep15_pages.txt で当てて入れる（空のあいだ、量のカットは「記録に無い値」で止まる）
#     🔴 2026-10-01（16本目 バイオントダム災害 ⑤b-1）：15本目の表（棒＝速さ・時間・G ほか）も**空にした**。
#        selftest の見本 `tools/fixture_ep15.py`（GATES["check_qty"]・値は1つも変えていない＝git の `c646174`）＝
#        いまの selftest（14本目の見本）は15本目の棒を使わない。16本目の棒を書くチャットで、値と頁を
#        ref/ep16/src/ep16_pages.txt で当てて入れる（空のあいだ、量のカットは「記録に無い値」で止まる）
#     🔴 2026-10-04（18本目 スレッシャー号 ⑤b-1）：16本目の表（棒＝ダムの高さ・量・波・日ごとに動いた距離・犠牲者・刑ほか）も**空にした**。
#        selftest の見本 `tools/fixture_ep16.py`（GATES["check_qty"]の REC_QTY・REC_GHOST・値は1つも変えていない＝git の `b044b56`）＝
#        いまの selftest（14本目の見本）は16本目の棒を使わない。18本目の棒を書くチャットで、値と頁を
#        ref/ep18/src/ep18_pages.txt で当てて入れる（空のあいだ、量のカットは「記録に無い値」で止まる）
#        ⚠️ 16本目の棒の教訓（日付を名にした行だけ同じ色でよい＝`_is_date_row`・見積もりの幅の上の端は REC_GHOST の破線の枠）は
#           この門番の型の側（下の `_digits_ok`・`judge_bar`）に残してある
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-06（19本目 ⑤b-1・§0b）：18本目の表（棒＝仕事の量・距離・乗っていた人・深さ・継手・割合）も**空にした**。selftest の見本
#    `tools/fixture_ep18.py`（GATES["check_qty"]・値は1つも変えていない＝git の `2d627a2`）。19本目の棒を書くチャットで、値と頁を
#    ref/ep19/src/ep19_pages.txt で当てて入れる（空のあいだ、量のカットは「記録に無い値」で止まる＝fail closed）
# 🔴 2026-10-08（20本目 ⑤b-1・§0b）：19本目の表（棒＝直す工事の額・部屋ごとの額・床の沈み・柱にかけた重さ）も**空にした**。selftest の見本
#    `tools/fixture_ep19.py`（GATES["check_qty"]・値は1つも変えていない＝git の `70c7e51`）。20本目の棒を書くチャットで、値と頁を
#    ref/ep20/src/ep20_pages.txt で当てて入れる（空のあいだ、量のカットは「記録に無い値」で止まる＝fail closed）。
#    換算（台本 §9 の式を門番の側でも持つ＝語りの「約」の丸めで描くと鳴る）の書き方は移した注の側にある＝fixture_ep19 の REC_QTY
# 🆕 2026-10-10（20本目 ⑤b-5）：c523 捜索に出た人＝p26（2.14.1.3 警察「8月12日 約2,500名 8月13日 約3,500名」）・
#    p27（2.14.1.4 防衛庁「8月12日 約1,000名 … 8月13日 約3,200名」）。行の名＝12日は「事故の夜」・13日は「翌日」（日付の数字を書かない）
REC_QTY = {("警察（人）", "事故の夜"): (2500, {"報告書 p26"}), ("警察（人）", "翌日"): (3500, {"報告書 p26"}),
           ("防衛庁（人）", "事故の夜"): (1000, {"報告書 p27"}), ("防衛庁（人）", "翌日"): (3200, {"報告書 p27"})}   # (群の項目名＝画面の文字, 行の名＝画面の文字) → (値, 頁)
# 🆕 2026-10-10（20本目 ⑤b-6）：c708 回数の比べ＝p105（3.2.3.1(1)「これらの疲労亀裂進展に要する内圧の負荷回数は1万回程度と推定され、これは、
#    昭和53年に行われた後部圧力隔壁の修理後の飛行回数(2.7.1参照)12,319回とほぼ一致する」）・p18（修理後の着陸回数 12,319回）
REC_QTY.update({("回数（回）", "亀裂の伸び（推定）"): (10000, {"報告書 p105"}),
                ("回数（回）", "修理後の飛行"): (12319, {"報告書 p105", "報告書 p18"})})
REC_GHOST = {}        # 「後」の行に「前」の長さを薄く残す棒
REC_GRID = {}         # マス目（項目名 → n・ok・ng・頁）
REC_PEOPLE = {}       # 人の形（14本目 c204〜c206 だけの例外＝§C-1 #59）
REC_PEOPLE_PAGES = set()
PEOPLE_CUTS = set()   # 🔴 ルール §C-1 #59（型の側の ss.PEOPLE_CUTS とは別に持つ）＝15本目は人の形を使わない
UNIT_PEOPLE, UNIT_GRID = "1つ＝1人", "1マス＝1項目"
DEATH = ("亡", "犠牲", "死", "行方", "遺体", "不明")
TOL_PX = 1.2          # 棒の端（rect は整数画素に丸めて書かれる＝x と幅で ±0.5 ずつ）
DE_MIN = 25.0

EL = re.compile(r'<(\w+) data-q="([^"]*)"([^>]*?)/?>(?:([^<]*)</\1>)?')
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
PERSON = re.compile(r'<path data-p="(\d+)" d="([^"]*)" fill="([^"]*)"/>')
TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')


def _els(svg):
    out = []
    for m in EL.finditer(svg):
        a = dict(ATTR.findall(m[3]))
        out.append(dict(tag=m[1], q=m[2], a=a, text=(m[4] or "")))
    return out


def _path_x(d):
    return float(re.match(r"M\s*([-\d.]+)", d)[1])


def _recs(r):
    return set(r) if isinstance(r, (list, tuple)) else {r}


def _unesc(s):
    return s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")


# 🆕 2026-10-01（16本目 ⑤b-6a）：行の名がまるごと日付（「9月2日」「10月2〜3日」「1963年」）＝同じ物差しの値の時間の並び（c611・c613）。
#   日付は棒の値（長さ）ではない＝行の名に書いてよい（数は字幕＝§5b-9 の網は値の数字に効く）。⚠️ 日付の形だけ（「6.5ミリ」は止まる）
DATE_ROW = re.compile(r"(?=.)(?:\d{4}年)?(?:\d{1,2}月)?(?:\d{1,2}(?:〜\d{1,2})?日)?")


def _is_date_row(t):
    return bool(DATE_ROW.fullmatch(t or ""))


def _digits_ok(svg):
    """⑩ 画面の数字は目盛り（tlab）・単位の札（kind）・注（note）の中だけ（🆕 行の名がまるごと日付なら、その行の名は通す）。"""
    bad = []
    for m in TEXT.finditer(svg):
        q = dict(ATTR.findall(m[1])).get("data-q", "")
        if q.startswith("rlab|") and _is_date_row(_unesc(m[2])):
            continue
        if re.search(r"[0-9０-９]", m[2]) and not (q.startswith("tlab|") or q in ("kind", "note")):
            bad.append(f"画面に数字「{_unesc(m[2])}」（{q or '印なし'}）＝数は字幕に（§5b-9）")
    return bad


# ══════════════════════════════════════════════════════════
#  棒
# ══════════════════════════════════════════════════════════
def judge_bar(f, pal=None):
    import jiko_style as J
    from check_color import de
    svg = f.lab + "".join(f.stages)
    els = _els(J.remap(svg, pal) if pal else svg)
    bad, n = [], 0
    # ⑪ 同じ群の灯した棒どうしの色（章の色に置き換えたあと）＝前と後を取り違えない距離（§5b-94①）。
    #    ⑤b-6 の下見で「改造の前」TICK と「改造の後」LINE が紺の地でほぼ同じ色に見えた（ΔE 約8）
    dim = (J.palette(pal)["LINE_DIM"] if pal else J.LINE_DIM).lower()
    lit = {}
    for e in els:
        kq = e["q"].split("|")
        if kq[0] == "bar" and e["a"].get("stroke", "").lower() != dim:
            lit.setdefault(kq[1], []).append((kq[2], e["a"]["stroke"].lower()))
    for gid, bs in lit.items():
        for i, (ta, ca) in enumerate(bs):
            for tb, cb in bs[i + 1:]:
                n += 1
                # 🆕 16本目 ⑤b-6a：日付を名にした行どうし（同じ物差しの時間の並び＝c611）は同じ色でよい。
                #   前と後・別の物の比べ（行の名が日付でない）は今までどおり ΔE 25 以上（同じ色も止める）
                if ca == cb and _is_date_row(ta) and _is_date_row(tb):
                    continue
                if de(ca, cb) < DE_MIN:
                    bad.append(f"群 {gid} の棒「{ta}」{ca} と「{tb}」{cb} の色が近い（ΔE {de(ca, cb):.1f}＜{DE_MIN}）＝前と後を取り違える")
    title = {e["q"].split("|")[1]: _unesc(e["text"]) for e in els if e["q"].startswith("gt|")}
    rlab = {tuple(e["q"].split("|")[1:3]): _unesc(e["text"]) for e in els if e["q"].startswith("rlab|")}
    fit = {}
    for gid in title:
        tx = {e["q"].split("|")[2]: _path_x(e["a"]["d"]) for e in els if e["q"].startswith(f"tick|{gid}|")}
        tv = {e["q"].split("|")[2]: _unesc(e["text"]) for e in els if e["q"].startswith(f"tlab|{gid}|")}
        pts = []
        for k, x in tx.items():
            n += 1
            s = tv.get(k, "")
            if not re.fullmatch(r"\d+", s):
                bad.append(f"群「{title[gid]}」の目盛りの文字「{s}」が数でない")
                continue
            pts.append((float(s), x))
        if len(pts) < 2:
            bad.append(f"群「{title[gid]}」の目盛りが {len(pts)} 本（2本以上ないと画素から値へ戻せない）")
            continue
        pts.sort()
        if pts[0][0] != 0:
            bad.append(f"群「{title[gid]}」の最初の目盛りが {pts[0][0]:g}（棒は 0 から＝途中から始まる軸は長さが嘘をつく）")
        k_ = len(pts)
        mv, mx = sum(v for v, _ in pts) / k_, sum(x for _, x in pts) / k_
        b = sum((v - mv) * (x - mx) for v, x in pts) / sum((v - mv) ** 2 for v, _ in pts)
        a = mx - b * mv
        for v, x in pts:
            if abs(a + b * v - x) > 1.0:
                bad.append(f"群「{title[gid]}」の目盛り {v:g} が一直線に並ばない（x={x}）")
        fit[gid] = (a, b)
    parts = {(p["g"], p.get("t") or p.get("row"), p["k"]): p for p in f.mech["parts"]}
    for e in els:
        kq = e["q"].split("|")
        if kq[0] not in ("bar", "ghost") or kq[1] not in fit:
            continue
        a, b = fit[kq[1]]
        x, w = float(e["a"]["x"]), float(e["a"]["width"])
        v = (x + w - a) / b
        tt = title[kq[1]]
        lab = rlab.get((kq[1], kq[2]), kq[2]) if kq[0] == "bar" else kq[2]
        table = REC_QTY if kq[0] == "bar" else REC_GHOST
        n += 3
        if abs(x - a) > TOL_PX:
            bad.append(f"「{tt}／{lab}」の{('棒' if kq[0] == 'bar' else '破線の枠')}の左端 x={x} が 0 の目盛り {a:.1f} と違う")
        if (tt, lab) not in table:
            bad.append(f"「{tt}／{lab}」は記録の表に無い（{kq[0]}）")
            continue
        want, pages = table[(tt, lab)]
        if abs(v - want) > TOL_PX / abs(b):
            bad.append(f"「{tt}／{lab}」の{('棒' if kq[0] == 'bar' else '破線の枠')}の端は {v:.1f} に当たる（記録 {want:g}）")
        p = parts.get((kq[1], kq[2], kq[0]))
        if not p or not (_recs(p["rec"]) & pages):
            bad.append(f"「{tt}／{lab}」の rec {p and p['rec']} が記録の頁 {sorted(pages)} と合わない")
    bad += _digits_ok(svg)
    return bad, n


# ══════════════════════════════════════════════════════════
#  マス目
# ══════════════════════════════════════════════════════════
def judge_grid(f):
    svg = f.lab + "".join(f.stages)
    els = _els(svg)
    bad, n = [], 4
    title = next((_unesc(e["text"]) for e in els if e["q"] == "gt|grid"), "")
    kind = next((_unesc(e["text"]) for e in els if e["q"] == "kind"), "")
    if kind != UNIT_GRID:
        bad.append(f"単位の札が「{kind}」（「{UNIT_GRID}」のはず）")
    r = REC_GRID.get(title)
    if not r:
        return bad + [f"マス目の項目名「{title}」が記録の表に無い"], n
    cells = sum(1 for e in els if e["q"] == "cell")
    ok = svg.count('<g data-q="ok">')
    ng = svg.count('<g data-q="ng">')
    if cells != r["n"]:
        bad.append(f"マスが {cells} 個（記録 {r['n']}）")
    if ok not in (0, r["ok"]):
        bad.append(f"✓ が {ok} 個（記録 {r['ok']}）")
    if ng not in (0, r["ng"]):
        bad.append(f"✕ が {ng} 個（記録 {r['ng']}）")
    for mk in f.mech["marks"]:
        n += 1
        if not (_recs(mk["rec"]) & r["rec"]):
            bad.append(f"印 {mk['k']} の rec {mk['rec']} が記録の頁 {sorted(r['rec'])} と合わない")
    bad += _digits_ok(svg)
    return bad, n


# ══════════════════════════════════════════════════════════
#  人の形
# ══════════════════════════════════════════════════════════
def _bbox(d):
    xs, ys = [], []
    for seg in re.findall(r"[ML]\s*([-\d.]+)\s+([-\d.]+)", d):
        xs.append(float(seg[0]))
        ys.append(float(seg[1]))
    return min(xs), min(ys), max(xs), max(ys)


def judge_people(f, cid, pal=None):
    import jiko_style as J
    from check_color import de
    remap = (lambda s: J.remap(s, pal)) if pal else (lambda s: s)
    layers = [remap(f.lab)] + [remap(s) for s in f.stages]
    bad, n = [], 0
    if cid not in PEOPLE_CUTS:
        bad.append(f"人の形は {sorted(PEOPLE_CUTS)} だけ（ルール §C-1 #59＝亡くなった方の数に使わない・後の章で戻して灰色にしない）")
    kind = next((_unesc(e["text"]) for e in _els(layers[0]) if e["q"] == "kind"), "")
    n += 1
    if kind != UNIT_PEOPLE:
        bad.append(f"単位の札が「{kind}」（「{UNIT_PEOPLE}」のはず＝1つ＝1人）")
    dim = J.palette(pal)["LINE_DIM"].lower() if pal else J.LINE_DIM.lower()
    col, shape = {}, {}
    for m in PERSON.finditer(layers[0]):
        col[int(m[1])] = m[3].lower()
        shape[int(m[1])] = _bbox(m[2])
    n += 1
    if len(col) != REC_PEOPLE["乗っていた人"]:
        bad.append(f"人の形が {len(col)} 個（記録 {REC_PEOPLE['乗っていた人']}＝1つ＝1人）")
    if set(col.values()) != {dim}:
        bad.append(f"基図の形の色が沈んだ色（LINE_DIM）だけでない {sorted(set(col.values()))}")
    ws = [b[2] - b[0] for b in shape.values()]
    hs = [b[3] - b[1] for b in shape.values()]
    n += 2
    # 座標は小数1桁で書かれる＝両端の丸めで ±0.1 ずつ＝0.25 までは同じ大きさ（⑤b-6 の最初の版は 19.8 と 19.9 を別と数えた）
    if ws and (max(ws) - min(ws) > 0.25 or max(hs) - min(hs) > 0.25):
        bad.append(f"人の形の大きさが揃っていない（幅 {min(ws):.1f}〜{max(ws):.1f}・高さ {min(hs):.1f}〜{max(hs):.1f}）＝1つが1人でなくなる")
    bs = sorted(shape.values())
    for i, b in enumerate(bs):
        for c in bs[i + 1:]:
            if c[0] >= b[2]:
                break
            if c[1] < b[3] and b[1] < c[3]:
                bad.append(f"人の形が重なる（{b[:2]} と {c[:2]}）＝数えられない")
                break
        if b[0] < 72 or b[2] > 1848 or b[1] < 210 or b[3] > 892:
            bad.append(f"人の形が枠の外 {b}")
    lits = f.mech["lits"]
    label_state = {}
    for j, lay in enumerate(layers[1:]):
        for m in PERSON.finditer(lay):
            i = int(m[1])
            if i not in col:
                bad.append(f"段{j + 1} に基図に無い形 {i}")
            col[i] = m[3].lower()
            if _bbox(m[2]) != shape.get(i):
                bad.append(f"段{j + 1} の形 {i} が基図と違う場所・大きさ")
        els = _els(lay)
        keys = {e["q"].split("|", 1)[1]: e["a"]["fill"].lower() for e in els if e["q"].startswith("key|")}
        labs = {e["q"].split("|", 1)[1]: _unesc(e["text"]) for e in els if e["q"].startswith("klab|")}
        for nm, c in keys.items():
            n += 2
            t = labs.get(nm, "")
            if any(w in t for w in DEATH):
                bad.append(f"凡例「{t}」に死の言葉（人の形は乗っていた人の内わけだけ）")
            if t not in REC_PEOPLE:
                bad.append(f"凡例「{t}」が記録の表に無い")
                continue
            got = {i for i, v in col.items() if v == c}
            label_state[t] = (c, got)
            if len(got) != REC_PEOPLE[t]:
                bad.append(f"段{j + 1}：凡例「{t}」の色の形が {len(got)} 個（記録 {REC_PEOPLE[t]}）")
            p = next((q for q in lits if q["who"] == nm), None)
            if not p or not (_recs(p["rec"]) & REC_PEOPLE_PAGES):
                bad.append(f"凡例「{t}」の rec {p and p['rec']} が記録の頁と合わない")
            if p and p.get("parent"):
                par = label_state.get(p["parent"])
                if not par or not got <= par[1]:
                    bad.append(f"凡例「{t}」の形が親「{p['parent']}」の形の内にない")
    # ⑧ 最後の状態で見えている色どうし・沈んだ色との距離
    live = sorted({v for v in col.values()})
    for i, a in enumerate(live):
        for b in live[i + 1:]:
            n += 1
            if de(a, b) < DE_MIN:
                bad.append(f"人の形の色 {a} と {b} が近い（ΔE {de(a, b):.1f}＜{DE_MIN}）＝取り違える")
    bad += _digits_ok("".join(layers))
    return bad, n


def judge(cid, kw, pal=None):
    import qty as Q
    f = Q.qty(**kw)
    v = kw["view"]
    if v == "bar":
        return judge_bar(f, pal)
    if v == "grid":
        return judge_grid(f)
    return judge_people(f, cid, pal)


# ══════════════════════════════════════════════════════════
#  物差しの検算
# ══════════════════════════════════════════════════════════
def selftest_ep18():
    """🆕 2026-10-04（18本目 ⑤b-6a）：18本目の棒（REC_QTY と ss.QG／QB）の検算＝**見本 `fixture_ep18`（18本目の表）を差し込んで**回す。
    ✅ 2026-10-06（19本目 ⑤b-1・§0b）：本番の表（この門番の REC_QTY）は19本目の空の器にした＝18本目の値は
       `fixture_ep18.GATES["check_qty"]`（15・16本目と同じ作り）。ss の側（QG・QB）と GEO も18本目の見本になる＝落ちても終わっても
       `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep18`"""
    import fixture_ep18
    fixture_ep18.apply(sys.modules[__name__])
    try:
        return _selftest_ep18()
    finally:
        fixture_ep18.restore()


def _selftest_ep18():
    """18本目の検算の本体（`fixture_ep18` を差し込んだ中で呼ぶ）。陽性対照＝語りの丸めで描く・群を混ぜる・頁違い・棒を1割長く描く（型を壊す）"""
    import titan_fig as F
    from cuts import ss
    QG, qb = ss.QG, ss.qb
    ok = True
    dist = dict(view="bar", groups=[QG["dist"]], steps=[dict(add=[qb("d_far"), qb("d_near")])], src="s")
    pct = dict(view="bar", groups=[QG["rej15"], QG["fix15"]], src="s",
               steps=[dict(add=[qb("q_court"), qb("q_jcae")]), dict(add=qb("q_rick"))])
    crew = dict(view="bar", groups=[QG["aboard"], QG["others"]], src="s",
                steps=[dict(add=[qb("a_crew"), qb("a_oth")]), dict(add=[qb("o_yard"), qb("o_ct"), qb("o_st")])])

    def run(name, cid, kw, want, pal):
        nonlocal ok
        try:
            bad, _ = judge(cid, kw, pal)
        except ValueError as e:
            bad = [f"型が止まった：{e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} 18本目 {name}: {'合格' if got else '不合格'}（{'合格' if want else '不合格'}のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    run("正しい距離（c207＝フィートをメートルに直した長さ）", "c207", dist, True, "sepia")
    run("正しい割合（c626＝不合格の群と、修理か交換の群）", "c626", pct, True, "mono")
    run("正しい乗っていた人（c302）", "c302", crew, True, None)
    run("🔴 陽性対照：語りの丸め（約110メートル）で描く", "c207",
        dict(dist, steps=[dict(add=[qb("d_far"), qb("d_near", v=110)])]), False, "sepia")
    run("🔴 陽性対照：中将の約10%を不合格の群に入れる（測り方の違う割合を混ぜる）", "c626",
        dict(pct, steps=[dict(add=[qb("q_court"), qb("q_jcae"), qb("q_rick", g="rej")])]), False, "mono")
    run("🔴 陽性対照：13.8% を語りの「14」に丸めて描く（査問会の行）", "c626",
        dict(pct, steps=[dict(add=[qb("q_court", v=14), qb("q_jcae")])]), False, "mono")
    run("🔴 陽性対照：頁違い（請け負った会社を p.183）", "c302",
        dict(crew, steps=[dict(add=[qb("a_crew"), qb("a_oth")]), dict(add=[qb("o_yard"), qb("o_ct", rec="R08 p4183"),
                                                                         qb("o_st")])]), False, None)
    rect0 = F.rect
    F.rect = lambda x, y, w, h, *a, **k: rect0(x, y, w * 1.1, h, *a, **k)
    try:
        bad, _ = judge("c626", pct, "mono")
    finally:
        F.rect = rect0
    ok &= bool(bad)
    print(f"  {'OK' if bad else '🔴 NG'} 🔴 18本目 陽性対照（型を壊す）：棒を1割長く描く（F.rect）: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    return ok


def selftest():
    # 🆕 2026-10-04（18本目 ⑤b-6a）：先に18本目を検算する（14本目の見本の差し込みより前）
    #    （2026-10-06〜：18本目も見本 fixture_ep18 の表＝selftest_ep18 が差し込んで・終わったら戻す）
    ok18 = selftest_ep18()
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（本番の表は回ごとに空にする＝§0b）＝この処理の中だけ14本目にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    import qty as Q
    import titan_fig as F
    from cuts import ss
    ok = True
    QG, qb = ss.QG, ss.qb
    bar = dict(view="bar", groups=[QG["cargo"]], steps=[dict(add=[qb("cargo_before"), qb("cargo_after")]),
                                                         dict(add=dict(k="ghost", g="cargo", row="改造の後", v=2437,
                                                                       rec="海審 p1018"))], src="s")
    grid = dict(view="grid", n=9, title="判定の項目", steps=[dict(add=dict(k="ok", n=5, rec="海審 p1080"))], src="s")
    ppl = dict(view="people", order=ss.PEOPLE_ORDER, sets=ss.PEOPLE_SETS,
               steps=[dict(add=[ss.pp("乗客", "LINE"), ss.pp("船で働く人", "DOC")]),
                      dict(add=[ss.pp("生徒", "AMBER", parent="乗客"), ss.pp("先生", "OK", parent="乗客")])], src="s")

    def run(name, cid, kw, want, pal="night"):
        nonlocal ok
        try:
            bad, _ = judge(cid, kw, pal)
        except ValueError as e:
            bad = [f"型が止まった：{e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}（{'合格' if want else '不合格'}のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    run("正しい棒（2437→987・もとの長さの枠）", "c407", bar, True)
    run("正しいマス目（9マス・✓5）", "c515", grid, True)
    run("正しい人の形（476・乗客443／船で働く人33 → 生徒325・先生14）", "c204", ppl, True)
    run("🔴 陽性対照：棒の値が記録と違う（2400）", "c407",
        dict(bar, steps=[dict(add=[qb("cargo_before", v=2400), qb("cargo_after")])]), False)
    run("🔴 陽性対照：棒の頁が違う（海審 p1017）", "c407",
        dict(bar, steps=[dict(add=[qb("cargo_before", rec="海審 p1017"), qb("cargo_after")])]), False)
    run("🔴 陽性対照：前と後の棒がほぼ同じ色（TICK と LINE＝⑤b-6 の最初の版）", "c407",
        dict(bar, steps=[dict(add=[qb("cargo_before", c="TICK"), qb("cargo_after", c="LINE")])]), False, pal=None)
    run("🔴 陽性対照：棒の名が記録に無い（改造中）", "c407",
        dict(bar, steps=[dict(add=[qb("cargo_before", t="改造中"), qb("cargo_after")])]), False)
    run("🔴 陽性対照：✓ が4つ", "c515", dict(grid, steps=[dict(add=dict(k="ok", n=4, rec="海審 p1080"))]), False)
    run("🔴 陽性対照：マス目の頁が違う", "c515", dict(grid, steps=[dict(add=dict(k="ok", n=5, rec="海審 p1079"))]), False)
    run("🔴 陽性対照：人の形を c106（亡くなった方の数）で使う", "c106", ppl, False)
    run("🔴 陽性対照：凡例の色が近い（night の LINE と INST）", "c204",
        dict(ppl, steps=[dict(add=[ss.pp("乗客", "LINE"), ss.pp("船で働く人", "INST")])]), False)
    run("🔴 陽性対照：乗客の数が違う並び（生徒324）", "c204",
        dict(ppl, order=(("生徒", 324),) + tuple(ss.PEOPLE_ORDER[1:])), False)
    # 🆕 16本目 ⑤b-6a：日付の行の名と、日付の並びの同じ色（狭めた2つの網が、狭めた外では今までどおり鳴るか）
    run("🔴 陽性対照：前と後の棒を同じ色（LINE と LINE・行の名が日付でない）", "c407",
        dict(bar, steps=[dict(add=[qb("cargo_before", c="LINE"), qb("cargo_after", c="LINE")])]), False, pal=None)
    for name, t, want in (("行の名がまるごと日付（9月2日）", "9月2日", True), ("行の名がまるごと日付（10月2〜3日）", "10月2〜3日", True),
                          ("🔴 陽性対照：行の名に値の数（6.5ミリ）", "6.5ミリ", False),
                          ("🔴 陽性対照：日付のあとに値（9月2日に6.5ミリ）", "9月2日に6.5ミリ", False)):
        got = not _digits_ok(f'<text data-q="rlab|g|{t}">{t}</text>')
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}（{'合格' if want else '不合格'}のはず）")

    def broken(name, obj, attr, val, cid, kw):
        nonlocal ok
        keep = getattr(obj, attr)
        setattr(obj, attr, val)
        try:
            bad, _ = judge(cid, kw, "night")
        except (ValueError, ZeroDivisionError) as e:
            bad = [f"型が止まった：{e}"]
        finally:
            setattr(obj, attr, keep)
        ok &= bool(bad)
        print(f"  {'OK' if bad else '🔴 NG'} 🔴 陽性対照（型を壊す）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    # 描く関数を壊す＝棒の四角を1割長く描く（目盛りは線なので変わらない）
    rect0 = F.rect

    def wide_rect(x, y, w, h, *a, **k):
        return rect0(x, y, w * 1.1, h, *a, **k)
    broken("棒を1割長く描く（F.rect）", F, "rect", wide_rect, "c407", bar)
    broken("単位の札を「1つ＝10人」と書く（UNIT）", Q, "UNIT", "1つ＝10人", "c204", ppl)
    broken("灯していない形を灰色（TICK）で描く（DIM）", Q, "DIM", "TICK", "c204", ppl)
    broken("人の形を大きく描いて隣と重ねる（person）", Q, "person",
           lambda cx, top, cw, ch, _p=Q.person: _p(cx, top, cw * 2.2, ch), "c204", ppl)
    broken("人の形を1つおきに大きく描く（person）", Q, "person",
           lambda cx, top, cw, ch, _p=Q.person: _p(cx, top, cw * (1.3 if int(cx) % 2 else 1.0), ch), "c204", ppl)
    broken("マス目の単位の札を消す（KIND_GRID）", Q, "KIND_GRID", "", "c515", grid)
    slots0 = Q.slots
    broken("並びから1人落とす（slots）", Q, "slots", lambda order, cols=Q.PCOLS: slots0(order, cols)[:-1], "c204", ppl)
    ok = ok and ok18
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
    import scene_jiko as S
    targets = {c: s["fig"][1] for c, s in sorted(cuts.SPEC.items()) if s.get("fig") and s["fig"][0] == "qty"}
    if not targets:
        print("⚠️ qty のカットが0件（この回に棒・マス目・人の形が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
        return 0
    bad_all, n_all = 0, 0
    for cid, kw in targets.items():
        bad, n = judge(cid, kw, S.palette_of(cid))
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {cid}（qty・{kw['view']}）: {b}")
        else:
            print(f"✓ {cid}（qty・{kw['view']}）: 長さ・数・色 {n}件が記録と合う")
    print(f"\n{'✓' if not bad_all else '🔴'} 量の型 {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
