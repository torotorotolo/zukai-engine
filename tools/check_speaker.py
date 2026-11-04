# -*- coding: utf-8 -*-
"""check_speaker.py — **話す人が次々に変わる所の「役職の札」が一覧どおりか**（29本目 ⑤b-4・映像方針 §4 の7）。

■ 何を見るか
  映像方針の一覧の note「札「話した人：役職」」（`ref/{EP}/eizou_build/assign{NN}.psv`・mark「札」）と、章ファイルの SPEC の `speaker`
  （`scene_jiko.speaker_chip`＝画面の左上の札）を1カットずつ突き合わせる。
  ①一覧に札があるのに SPEC に無い ②SPEC に札があるのに一覧に無い ③役職の字が1字でも違う ④札の字に「話した人」と同じ言葉が二重にある、を止める。
  🔴 札に出してよいのは役職だけ（名前は書かない＝ルール §B2-11）。役職の字は一覧が正本＝直すなら `assign{NN}.psv` → SPEC の順。
  ⚠️ 図のカット（c505・c511・c513）は図の中に役職を書く＝札なし（`speaker` を付けない）。これは①②で見ている（一覧に札が無いから）。

■ なぜ門番にしたか
  `speaker` は SPEC に手で書く字。⑤b-3 は1回だけ突き合わせて（違い0）門番にしなかった＝後で一覧か SPEC を直すと、黙ってずれる。

■ 一覧が無い回（`speaker` を使わない回）
  `speaker` が SPEC に1件も無く、一覧の札も0件なら「0件」と出して通す（**0件を調べて合格にしていないかは出力の件数で見る**）。

■ 陽性対照：`--selftest`（毎回まず回す）＝札を抜く・札を足す・役職を1字変える、がそれぞれ止まるか。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

WANT = re.compile(r"札「話した人：([^」]+)」")


def want_of(ep):
    """一覧の当て方 assign{NN}.psv から {カット: 役職}。無ければ None（fail closed は呼ぶ側）。"""
    nn = ep.strip("/").replace("ep", "")
    p = ROOT / "ref" / ep.strip("/") / "eizou_build" / f"assign{nn}.psv"
    if not p.exists():
        return None
    out = {}
    for ln in p.read_text(encoding="utf-8").splitlines():
        c = ln.split("|")
        if len(c) >= 10 and re.match(r"c\d{3}$", c[0]):
            m = WANT.search(c[9])
            if m:
                out[c[0]] = m.group(1)
    return out


def judge(want, got):
    """{カット: 役職} 2つを比べて、理由の列を返す。"""
    bad = []
    for c in sorted(set(want) | set(got)):
        w, g = want.get(c), got.get(c)
        if w and not g:
            bad.append(f"① {c}: 一覧に札「{w}」があるのに SPEC に speaker が無い")
        elif g and not w:
            bad.append(f"② {c}: SPEC に札「{g}」があるのに一覧に無い")
        elif w != g:
            bad.append(f"③ {c}: 役職の字が一覧「{w}」と SPEC「{g}」で違う")
        if g and "話した人" in g:
            bad.append(f"④ {c}: 札の字「{g}」に「話した人」が入っている（札が前に足す＝二重になる）")
    return bad


def selftest():
    w = {"c1": "副社長", "c2": "代表"}
    cases = [("正しい", w, dict(w), None), ("札を抜く", w, {"c1": "副社長"}, "①"), ("札を足す", w, dict(w, c3="社長"), "②"),
             ("役職を1字変える", w, {"c1": "副社長", "c2": "代表者"}, "③"), ("字が二重", {"c1": "話した人：代表"}, {"c1": "話した人：代表"}, "④")]
    ok = True
    for name, a, b, reason in cases:
        bad = judge(a, b)
        good = (not bad) if reason is None else any(x.startswith(reason) for x in bad)
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} {name}: {'不合格' if bad else '合格'}" + (f"（不合格のはず・理由「{reason}」）" if reason else ""))
    return ok


def main():
    if not selftest():
        print("selftest: 🔴 落ちた")
        return 2
    print("selftest: 通った")
    if "--selftest" in sys.argv:
        return 0
    import cuts
    import cuts.ss as ss
    want = want_of(ss.EP)
    got = {c: s["speaker"] for c, s in cuts.SPEC.items() if s.get("speaker")}
    if want is None:
        if got:
            print(f"🔴 一覧の当て方が無いのに SPEC に speaker が {len(got)}件ある（{ss.EP}）")
            return 1
        print(f"⚠️ {ss.EP} に一覧の当て方が無く speaker も0件＝見るものが無い")
        return 0
    bad = judge(want, got)
    for b in bad:
        print("🔴", b)
    for c in sorted(got):
        if got[c] == want.get(c):
            print(f"✓ {c}: {got[c]}")
    print(f"\n{'✓' if not bad else '🔴'} 役職の札 一覧 {len(want)}件・SPEC {len(got)}件・違い {len(bad)}件")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
