# -*- coding: utf-8 -*-
"""check_axis.py — 軸の型（年表・時間の帯・交信の帯＝`tools/axis.py`）の**値・画素・割れる時刻・交信の文字**を照合する
（2026-09-29 新設・14本目 ⑤b-5）。

■ なぜ要るか
  年表と時間の帯は「位置」が情報そのもの。点が1か月・1分ずれても字幕と画面が食い違う。
  🔴 §5b-88：門番が型の定数を正解として読むと、型を壊しても通る＝**記録の値はこの門番の側に持つ**（`REC_AXIS`）。
     値の読み方（年月日→年・時刻→分）も型（axis.val）を使わず、ここで別に書く。

■ 測るもの（本番の関数 `axis.axis()` が置いた部品の画素＝`f.mech` から）
  ① 値が記録の表 `REC_AXIS` にあり、部品の rec（頁）の1つが表の頁と合う（目盛りは記録でなく物差し＝照らさない）
  ② 画素：目盛りの画素の x と目盛りの文字（ここで読む）から一次式を当て、部品の x を値へ戻す＝書いた細かさの幅に入る
     （分＝±0.3分・日＝±0.6日・月＝その月の中・年＝その年の中）。目盛りの文字が目盛りの値の書き方と合うかも見る
  ③ 割れる時刻：split は1カットに2つ以上・値が2つ以上・形が同じ（色・大きさを変えない＝どれが正しいと描かない）。
     `cuts/ss.ILLU_SPLIT_TIMES` の時刻の点（pt）は出典の名を添える（by=True）
  ④ 交信の帯：link に文字が無い・段の名は `LANES_OK` だけ（私人の言葉を帯に書かない）
  ⑤ カーソルは記録の値（その段までに描いた部品の x）か軸の左端にだけ止まる

■ 使い方
    python tools/check_axis.py              # 全カット
    python tools/check_axis.py --selftest   # 物差しの検算（陽性対照＝型の定数を壊す・記録と違う頁・一つだけの割れ）
"""
from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

# ══════════════════════════════════════════════════════════
#  🔴 §0b（題材を替えるとき空にする場所）：記録の値と頁（この回）。
#     🔴 2026-09-30（15本目 リノ ⑤b-1）：**空にした**。14本目（セウォル号）の表は selftest の見本 `tools/fixture_ep14.py`
#        （GATES["check_axis"]・値は1つも変えていない）。15本目の年表・時間の帯を書くチャットで、値と頁を
#        ref/ep15/src/ep15_pages.txt で当てて入れる（空のあいだ、軸のカットは「記録に無い値」で止まる＝fail closed）
#     🔴 2026-10-01（16本目 バイオントダム災害 ⑤b-1）：15本目の表（秒の帯・年表・時刻の帯・横転の前の秒）も**空にした**。
#        selftest の見本 `tools/fixture_ep15.py`（GATES["check_axis"]・値は1つも変えていない＝git の `c646174`）。
#        16本目の値は、軸の型を初めて使う ⑤b のチャットで、値と頁を ref/ep16/src/ep16_pages.txt で当てて入れる
#        （空のあいだ、軸のカットは「記録に無い値」で止まる＝fail closed）
# ══════════════════════════════════════════════════════════
#     🆕 2026-10-01（16本目 ⑤b-5）：16本目の値を入れた＝10月9日の時刻の帯（場面4）。原文 ref/ep16/src/ep16_pages.txt で当てた
#        （S1＝議会の調査委員会の最終報告 PDF の頁・S9＝バイオント財団の年表 PDF の頁 p2001〜）
REC_AXIS = {
    "9:45": {"S1 p98"},                    # p98「Il successivo 9 ottobre alle ore 9,45 del mattino … tutte le 35 famiglie … sistemandosi provvisoriamente a Casso」
    "12:00": {"S9 p2016"},                 # p2016「Ore 12. Durante la pausa pranzo alcuni operai ENEL fermi sul coronamento della diga vedono …」
    "13:00": {"S9 p2016"},                 # 「Ore 13. Dietro le baracche degli operai in sponda sinistra, si apre una crepa larga 50 centimetri e lunga 5 metri」
    "16:00": {"S9 p2016"},                 # 「Dopo tre ore la crepa ha progredito di 40-50 centimetri」（13時＋3時間）／「Ore 15-16.」の尻
    "15:00": {"S9 p2016"},                 # 「Ore 15-16. un operaio attraversando la zona del Massalezza … vede alberi cadere」
    "17:00": {"S9 p2016", "S1 p228"},      # 「Ore 17. Caruso riceve da Venezia le direttive …」・S1 p228（少数派「ma non per fare sgomberare la popolazione」）
    "17:50": {"S9 p2016"},                 # 「Ore 17.50. Biadene telefona a Penta … per la prima volta, informa Penta degli esperimenti su modello … quota 700」
    "20:00": {"S9 p2016", "S1 p228"},      # 「Ore 20. I camion non sono più in grado di transitare … La strada per il Toc viene sbarrata」・p228「Alle ore 20 …」
    "22:00": {"S9 p2017"},                 # 割れる時刻 S9「Ore 22. Rittmeyer telefona a Biadene, a Venezia」
    "22:15": {"S1 p228"},                  # 割れる時刻 S1 p228（少数派）「Alle 22,15 — come hanno affermato le telefoniste di Longarone」
    "22:39": {"S1 p98", "S9 p2017"},       # S9 p2017「Ore 22.39. La frana si stacca」・S1 p98
}
LANES_OK = set()


def gv(view, s):
    """門番の読み方（型とは別に書く）＝(下限, 上限)。date は年（小数）・clock は分・sec は秒（15本目〜）。"""
    s = str(s).strip()
    if view == "sec":
        # 🆕 15本目 ⑤b-5（c218）：負の秒＝0 の時点より前（"約-8"）
        m = re.fullmatch(r"(?:約)?(-)?(\d+)(?:\.(\d+))?", s)
        v = float(m[2] + ("." + m[3] if m[3] else "")) * (-1 if m[1] else 1)
        tol = 0.5 * 10 ** -len(m[3]) if m[3] else 0.05        # 書いた桁の半分（整数は ±0.05＝目盛りの 0秒）
        return v - tol, v + tol
    if view == "date":
        p = [int(x) for x in s.split("-")]
        if len(p) == 1:
            return float(p[0]), p[0] + 0.999
        if len(p) == 2:
            y, m = p
            a = datetime.date(y, m, 1)
            b = datetime.date(y + (m == 12), m % 12 + 1, 1)
        else:
            a = datetime.date(*p)
            b = a + datetime.timedelta(days=1)
        yl = (datetime.date(a.year + 1, 1, 1) - datetime.date(a.year, 1, 1)).days

        def yr(d):
            return d.year + (d - datetime.date(d.year, 1, 1)).days / yl
        if len(p) == 3:
            v = yr(a)
            return v - 0.6 / yl, v + 0.6 / yl
        return yr(a) - 1e-6, yr(b) + 1e-6
    nxt = s.startswith("翌")
    h, m = s.replace("翌", "").split(":")
    v = (1440 if nxt else 0) + int(h) * 60 + int(m)
    return v - 0.3, v + 0.3


def _mid(view, s):
    a, b = gv(view, s)
    if view == "date" and len(str(s).split("-")) < 3:
        return a          # 年・月の目盛りはその頭に立つ
    return (a + b) / 2


def _texts(view, s):
    """値 s を画面に出してよい文字（門番の書き方）。date は日まで・年月まで・年だけのどれか（語りの細かさに合わせてよい）。"""
    if view == "date":
        p = [int(x) for x in s.split("-")]
        forms = [f"{p[0]}年"]
        if len(p) > 1:
            forms.append(f"{p[0]}年{p[1]}月")
        if len(p) > 2:
            forms.append(f"{p[0]}年{p[1]}月{p[2]}日")
        return set(forms)
    if view == "sec":
        return {_sec_word(s)}
    return {s.replace("翌", "")}


def _sec_word(s):
    """門番の秒の書き方（型とは別に書く）：負は「N秒前」。"""
    if s.startswith(("-", "約-")):
        return s.replace("-", "", 1) + "秒前"
    return s + "秒"


def _tick_text(view, s):
    if view == "date":
        p = s.split("-")
        return f"{int(p[1])}月" if len(p) > 1 else p[0]
    if view == "sec":
        return _sec_word(s)
    return s.replace("翌", "")


def judge_fig(kw, split_times=()):
    """(食い違いの list, 照合した件数)。"""
    import axis as A
    f = A.axis(**kw)
    m = f.mech
    view = m["view"]
    vk = view if view in ("date", "sec") else "clock"
    bad, n = [], 0
    tk = m["ticks"]
    if len(tk) < 2:
        return [f"目盛りが {len(tk)} 本（2本以上ないと画素から値へ戻せない）"], 1
    for t in tk:
        n += 1
        if t["lab"] != _tick_text(vk, t["at"]):
            bad.append(f"目盛り {t['at']} の文字が「{t['lab']}」")
    # 一次式（最小二乗）
    xs = [t["x"] for t in tk]
    vs = [_mid(vk, t["at"]) for t in tk]
    k = len(xs)
    mx, mv = sum(xs) / k, sum(vs) / k
    sxx = sum((v - mv) ** 2 for v in vs)
    p = sum((v - mv) * (x - mx) for v, x in zip(vs, xs)) / sxx
    q = mx - p * mv
    for t in tk:
        if abs(p * _mid(vk, t["at"]) + q - t["x"]) > 1.0:
            bad.append(f"目盛り {t['at']} が一直線に並ばない（{t['x']}）")

    def back(x):
        return (x - q) / p

    placed = [m["x0"]]
    splits = []
    for part in m["parts"]:
        recs = part["rec"] if isinstance(part["rec"], (list, tuple)) else [part["rec"]]
        vals = [(part["at"], part["x"])] if "at" in part else [(part["a"], part["xa"]), (part["b"], part["xb"])]
        for s, x in vals:
            n += 2
            if s not in REC_AXIS:
                bad.append(f"{s} は記録の表 REC_AXIS に無い（{part['k']}「{part.get('t', '')}」）")
            elif not any(r in REC_AXIS[s] for r in recs):
                bad.append(f"{s} の rec {recs} が記録の頁 {sorted(REC_AXIS[s])} と合わない")
            lo, hi = gv(vk, s)
            v = back(x)
            eps = 0.5 / abs(p)            # 画素は小数2桁に丸めて記録する＝0.5画素ぶんは丸めの誤差として許す
            if not lo - eps <= v <= hi + eps:
                bad.append(f"{s} の画素 x={x} は値 {v:.4f} に当たる（{lo:.4f}〜{hi:.4f} の外）")
            placed.append(x)
        if part.get("top"):
            n += 1
            if part["top"] not in _texts(vk, part["at"]):
                bad.append(f"{part['at']} の画面の文字が「{part['top']}」（値と合わない）")
        if part["k"] == "split":
            splits.append(part)
            n += 1
            if not part.get("d"):
                bad.append(f"割れる時刻 {part['at']} に出典の名が無い")
        if part["k"] == "pt" and vk == "clock" and part["at"].replace("翌", "") in split_times:
            n += 1
            if not (part.get("by") and part.get("d")):
                bad.append(f"割れる時刻 {part['at']} の点に出典の名が無い（by=True にする＝ss.ILLU_SPLIT_TIMES）")
        if part["k"] == "link":
            n += 2
            if part.get("t") or part.get("chips"):
                bad.append(f"交信 {part['at']} に文字（私人の言葉を帯に書かない）")
            if not {part["fr"], part["to"]} <= LANES_OK:
                bad.append(f"交信 {part['at']} の段の名 {part['fr']}／{part['to']} が決まった名（{sorted(LANES_OK)}）でない")
    # 🆕 ⑤b-5：上の段へ伸びる縦の線が、それより下の段の札を貫かない（前のカットの点どうし＝同じ層でも）。
    #   門番 layout は層どうしの横切りしか見ない＝c408 の「1946年」の線が「1944年」の札を貫いたのを素通りした（試し焼きで見つけた）
    labs = [p for p in m["parts"] if p.get("lx") and "at" in p]
    for b in m["parts"]:
        if "at" not in b or b["k"] in ("chips", "link"):
            continue
        for a in labs:
            if a is b:
                continue
            n += 1
            if b.get("row", 0) > a.get("row", 0) and a["lx"][0] + 2 < b["x"] < a["lx"][1] - 2:
                bad.append(f"{b['at']} の縦の線（段{b.get('row', 0)}）が {a['at']} の札（段{a.get('row', 0)}）を貫く")
    if view == "lanes":
        for nm in m["lanes"]:
            n += 1
            if nm not in LANES_OK:
                bad.append(f"段の名「{nm}」が決まった名でない")
    if splits:
        n += 1
        if len(splits) < 2 or len({s["at"] for s in splits}) < 2:
            bad.append("割れる時刻の印が1つだけ（2つ以上を並べる）")
        if len({(s["c"], s["big"]) for s in splits}) > 1:
            bad.append("割れる時刻の印の形が揃っていない（どれが正しいと描かない）")
    if m["cur_on"]:
        for i, x in enumerate(m["cur"]):
            n += 1
            if not any(abs(x - y) < 0.6 for y in placed):
                bad.append(f"カーソル（段{i}）x={x} が記録の値に止まっていない")
    return bad, n


def _split_times():
    try:
        from cuts import ss
        return tuple(getattr(ss, "ILLU_SPLIT_TIMES", ()))
    except Exception:  # noqa: BLE001
        return ()


def selftest_ep15():
    """15本目（⑤b-2・⑤b-5）の秒の帯（sec）・年表・負の秒の検算＝**見本 `fixture_ep15`（15本目の表）を差し込んで**回す。
    🔴 2026-10-01（16本目 ⑤b-1）：本番の表（この門番の REC_AXIS）は16本目の空の器にした＝15本目の値は
       `fixture_ep15.GATES["check_axis"]`（14本目と同じ作り）。ss の側（AXIS_DOCS・AXI ほか）と GEO も15本目の見本になる
       ＝落ちても終わっても `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep15`"""
    import fixture_ep15
    fixture_ep15.apply(sys.modules[__name__])
    try:
        return _selftest_ep15()
    finally:
        fixture_ep15.restore()


def _selftest_ep15():
    """15本目の検算の本体（`fixture_ep15` を差し込んだ中で呼ぶ）。"""
    import axis as A
    sec = dict(view="sec", span=("0", "5"), ticks=("0", "1", "2", "3", "4", "5"),
               steps=[dict(add=[dict(k="pt", at="1.3", t="最大G", rec="AAB p28"),
                                dict(k="pt", at="4.6", t="一片が離れる", rec="AAB p28")], cur="4.6"),
                      dict(add=dict(k="pt", at="0.56", t="リンクが折れている", rec="AAB p24"), cur="0.56")],
               note="n", src="s")
    cases = [("15本目 正しい秒の帯（1.3→4.6→0.56）", sec, True),
             ("🔴 15本目 陽性対照：表に無い秒（#42 の 5.3）",
              dict(sec, span=("0", "6"), ticks=("0", "2", "4", "6"),
                   steps=[dict(add=dict(k="pt", at="5.3", t="一片", rec="AAB p28"))]), False),
             ("🔴 15本目 陽性対照：1.3秒の頁が違う（AAB p29）",
              dict(sec, steps=[dict(add=dict(k="pt", at="1.3", t="最大G", rec="AAB p29"))]), False)]
    # 🆕 ⑤b-5（c218）：負の秒（横転の約8秒前）＝札「約8秒前」・目盛り「10秒前」
    upset = dict(view="sec", span=("-10", "1"), ticks=("-10", "-8", "-6", "-4", "-2", "0"),
                 steps=[dict(add=dict(k="pt", at="0", t="横転の始まり", rec="AAB p28"), cur="0"),
                        dict(add=dict(k="pt", at="約-8", t="圧力と回転が下がる", rec="AAB p29"), cur="約-8")],
                 note="n", src="s")
    cases += [("15本目 正しい負の秒（約8秒前）", upset, True),
              ("🔴 15本目 陽性対照：約8秒前の頁が違う（AAB p28）",
               dict(upset, steps=[dict(add=dict(k="pt", at="約-8", t="圧力", rec="AAB p28"))]), False),
              ("🔴 15本目 陽性対照：記録に無い負の秒（約-7）",
               dict(upset, steps=[dict(add=dict(k="pt", at="約-7", t="圧力", rec="AAB p29"))]), False)]
    # 🆕 ⑤b-5：縦の線が別の札を貫く（試し焼きの c408＝前のカットの 1944年と1946年の点が31画素しか離れていない）
    hist = dict(view="date", span=("1942", "2013"), ticks=("1950", "1960", "1970", "1980", "1990", "2000", "2010"),
                steps=[dict(add=dict(k="pt", at="1983-07", t="パイロットが取得", rec="AAB p12", anchor="end"), cur="1983-07")],
                note="n", src="s")
    p44 = dict(k="pt", at="1944-12-23", t="軍へ引き渡し", rec="AAB p12", fmt="y")
    p46 = dict(k="pt", at="1946-07", t="売却", rec="AAB p12", fmt="y")
    cases += [("🔴 15本目 陽性対照：1946年の縦の線が1944年の札を貫く（直す前の c408）", dict(hist, past=[p44, p46]), False),
              ("15本目 正しい：1946年の札を消して沈める（直した c408）", dict(hist, past=[p44, dict(p46, lab=False, t="")]), True)]
    ok = True
    for name, kw, want in cases:
        bad, _ = judge_fig(kw, ())
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 型を壊す陽性対照（負の秒）：① 約付きの負の秒だけ半分の所に描く（画素）② 札の「前」を落とす（文字）
    keep_val, keep_txt = A.val, A._sec_text
    A.val = lambda view, s: ((keep_val(view, s)[0] / 2 if view == "sec" and str(s).startswith("約-") else keep_val(view, s)[0]),
                             keep_val(view, s)[1])
    try:
        bad, _ = judge_fig(upset, ())
    except ValueError as e:
        bad = [f"型が止まった：{e}"]
    finally:
        A.val = keep_val
    ok &= bool(bad)
    print(f"  {'OK' if bad else '🔴 NG'} 🔴 15本目 陽性対照（画素）：約8秒前を半分の所に描く型: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    A._sec_text = lambda s: s.replace("-", "") + "秒"
    try:
        bad, _ = judge_fig(upset, ())
    finally:
        A._sec_text = keep_txt
    ok &= bool(bad)
    print(f"  {'OK' if bad else '🔴 NG'} 🔴 15本目 陽性対照（文字）：「前」を落とす型（約8秒）: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    keep = A.val
    # 小数の秒だけ 0.3秒ずらして描く型（目盛り＝整数は正しい＝一様な伸び縮みは目盛りの物差しに吸われるので、部品だけずらす）
    A.val = lambda view, s: ((keep(view, s)[0] + (0.3 if "." in str(s) else 0.0), keep(view, s)[1]) if view == "sec"
                             else keep(view, s))
    try:
        bad, _ = judge_fig(sec, ())
    except ValueError as e:
        bad = [f"型が止まった：{e}"]
    finally:
        A.val = keep
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 15本目 陽性対照（画素）：小数の秒を 0.3秒ずらして描く型: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    return ok


def selftest():
    # 🔴 2026-09-30（15本目 ⑤b-2）：先に15本目の秒の帯を検算してから、14本目の見本に差し替える
    #    （2026-10-01〜：15本目も見本 fixture_ep15 の表＝selftest_ep15 が差し込んで・終わったら戻す）
    ok = selftest_ep15()
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（本番の表は回ごとに空にする＝§0b）＝この処理の中だけ14本目にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    import axis as A
    ST = ("8:52", "8:58", "9:46", "9:48")
    night = dict(view="clock", span=("18:00", "翌10:00"), ticks=("18:00", "22:00", "翌2:00", "翌6:00", "翌10:00"),
                 steps=[dict(add=[dict(k="pt", at="18:30", t="出港", rec="海審 p1026"),
                                  dict(k="pt", at="翌9:10", t="着く", rec="海審 p1026")], cur="18:30"),
                        dict(add=dict(k="span", a="18:30", b="21:05", t="遅れ", rec=["海審 p1026", "海審 p1038"]),
                             cur="21:05")], note="n", src="s")
    years = dict(view="date", span=("2012-09", "2013-04"),
                 ticks=("2012-09", "2012-10", "2012-11", "2012-12", "2013-01", "2013-02", "2013-03", "2013-04"),
                 steps=[dict(add=[dict(k="pt", at="2012-10-08", t="導入", rec="海審 p1016"),
                                  dict(k="span", a="2012-10-12", b="2013-02-12", t="改造", rec="海審 p1016")],
                             cur="2013-02-12")], note="n", src="s")
    split = dict(view="clock", span=("9:40", "9:55"), ticks=("9:40", "9:45", "9:50", "9:55"),
                 steps=[dict(add=[dict(k="split", at="9:46", rec="判決 p18"), dict(k="split", at="9:48", rec="海審 p1055")])],
                 note="n", src="s")
    lanes = dict(view="lanes", span=("9:05", "9:40"), ticks=("9:10", "9:20", "9:30", "9:40"), lanes=("管制", "近くの船", "セウォル号"),
                 steps=[dict(add=dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="判決 p13"), cur="9:13")],
                 note="n", src="s")

    def mod(d, **kw):
        return dict(d, **kw)
    cases = [
        ("正しい夜の帯（18:30→翌9:10・21:05）", night, True),
        ("正しい改造の年表（2012-10-08・2012-10-12〜2013-02-12）", years, True),
        ("正しい割れる時刻（9:46 判決／9:48 海審）", split, True),
        ("正しい交信の帯（9:13 近くの船→セウォル号）", lanes, True),
        ("🔴 陽性対照：9:13 の頁が違う（海審 p1059）",
         mod(lanes, steps=[dict(add=dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="海審 p1059"))]), False),
        ("🔴 陽性対照：記録に無い時刻 9:15",
         mod(lanes, steps=[dict(add=dict(k="link", at="9:15", fr="近くの船", to="セウォル号", rec="判決 p13"))]), False),
        ("🔴 陽性対照：割れる時刻の印が1つだけ", mod(split, steps=[dict(add=dict(k="split", at="9:46", rec="判決 p18"))]), False),
        ("🔴 陽性対照：割れる時刻の片方だけ大きい",
         mod(split, steps=[dict(add=[dict(k="split", at="9:46", rec="判決 p18", big=True),
                                     dict(k="split", at="9:48", rec="海審 p1055")])]), False),
        ("🔴 陽性対照：割れる時刻 8:58 の点に出典の名が無い",
         dict(view="clock", span=("8:48", "9:02"), ticks=("8:50", "9:00"),
              steps=[dict(add=dict(k="pt", at="8:58", t="指示", rec="判決 p12"))], note="n", src="s"), False),
        ("🔴 陽性対照：段の名に私人の名",
         mod(lanes, lanes=("管制", "生徒", "セウォル号"),
             steps=[dict(add=dict(k="link", at="9:13", fr="管制", to="セウォル号", rec="判決 p13"))]), False),
        ("🔴 陽性対照：カーソルが記録の無い所（9:20）に止まる",
         mod(lanes, steps=[dict(add=dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="判決 p13"), cur="9:20")]),
         False),
    ]
    for name, kw, want in cases:
        bad, _ = judge_fig(kw, ST)
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 型の定数を壊す（§5b-88）：月の数え始め・翌日の足し分・軸の右端（部品だけずれる型は無いので目盛りの文字で捕まえる）
    for name, attr, val, kw in (("月を1つずらして描く型（MONTH0=0）", "MONTH0", 0, years),
                                ("翌日を12時間で描く型（NEXT_DAY=720）", "NEXT_DAY", 720, night)):
        keep = getattr(A, attr)
        setattr(A, attr, val)
        try:
            bad, _ = judge_fig(kw, ST)
        except ValueError as e:     # 範囲の外で型が止まるのも「捕まえた」
            bad = [f"型が止まった：{e}"]
        finally:
            setattr(A, attr, keep)
        good = bool(bad)
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照（画素）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    keep = A.label
    A.label = lambda view, s, fmt="": keep(view, s, fmt).replace("30", "03")   # 「18:30」を「18:03」と書く型
    try:
        bad, _ = judge_fig(night, ST)
    finally:
        A.label = keep
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照（文字）：18:30 を「18:03」と書く型: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    try:
        A.axis(**mod(lanes, steps=[dict(add=dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="判決 p13",
                                                  t="脱出すれば"))]))
        good = False
    except ValueError:
        good = True
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照：交信に言葉を書くと型が止まる: {'止まった' if good else '通った'}（止まるはず）")
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
    targets = {c: s["fig"] for c, s in sorted(cuts.SPEC.items()) if s.get("fig") and s["fig"][0] == "axis"}
    if not targets:
        print("⚠️ axis のカットが0件（この回に年表・時間の帯が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
        return 0
    st = _split_times()
    bad_all, n_all = 0, 0
    for cid, (_, kw) in targets.items():
        bad, n = judge_fig(kw, st)
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {cid}（axis）: {b}")
        else:
            print(f"✓ {cid}（axis・{kw['view']}）: 値・画素・割れる時刻 {n}件が合う")
    print(f"\n{'✓' if not bad_all else '🔴'} 軸の型 {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
