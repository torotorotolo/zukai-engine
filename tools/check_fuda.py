# -*- coding: utf-8 -*-
"""札の型（`tools/mech30.py`・`fig=("m30", …)`／🆕 31本目 `tools/mech31.py`・`fig=("m31", …)`）の字数と字の大きさの門番。🆕 30本目 ⑤b-4（2026-11-05）。

■ なぜ要るか
  札の型は描き手が1つ＝表に字を足すだけで、読み切れない札がいくらでも作れる。門番 layout は「はみ出し」しか見ない（拡大率 k が字を縮めて収める）・
  check_box は枠の空きしか見ない＝**字が多すぎる／小さすぎる札を鳴らす物差しが無かった**（規則を書いたら門番も足す＝feedback-rules-need-gates）。

■ 測るもの（カットごと・どれか外れたら exit 1）
  F1 1行の字数   …… 本文 LINE_MAX 字まで・見出し札 HEAD_MAX 字まで・小さい字 SUB_MAX 字まで・黄色い数 BIG_MAX 字まで（「」は数えない）
  F2 札1枚の字数 …… CARD_MAX 字まで
  F3 画面の字数  …… 影の札を除いて、そのカットの秒 × CPS 字まで（語り 361字/分＝毎秒6字より速く読ませない）
  F4 字の大きさ  …… 焼く大きさ（拡大率のあと）で本文 BODY_MIN・見出し札 HEAD_MIN・小さい字 SUB_MIN・黄色い数 BIG_MIN 以上
  F5 札と矢印の数 … 影の札を除いて CARDS_MAX 枚・矢印 ARROWS_MAX 本まで（映像方針 §5-4＝札1〜4枚＋矢印0〜2本・まとめの cc15 だけ5枚＝EXC）
  F6 段と行      …… 段の数 ≥ 語りの行の数・札と矢印の出る段が段の数の内・mute の行が語りの行にある
  F7 無線帯の行  …… 🆕 ⑤b-5（2026-11-06）：見え方の表の無線帯（`mech30.VIEWS` の band）の前の段の語は BAND_MAX 字まで・字の大きさ BAND_MIN 以上
                     （帯は前のカットのおさらい＝短い語で残す。札の字数と画面の字の秒には数えない＝影の札と同じ扱い）

■ しきい値の根拠
  ⚠️ 87カットの実測（2026-11-05）から Claude が置いた最初の値＝カズヤくんの見本の承認はまだ（⑤c で読めない札が出たら直す）。
  F3 の毎秒6字は語りの実測 361.1字/分（⑤a-2）。

  python -P tools/check_fuda.py            … 全カット
  python -P tools/check_fuda.py --dist     … 実測の分布も出す
  python -P tools/check_fuda.py --selftest … 陽性対照
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

LINE_MAX, HEAD_MAX, SUB_MAX, BIG_MAX = 24, 18, 14, 11
CARD_MAX = 44
CPS = 6.0
BODY_MIN, HEAD_MIN, SUB_MIN, BIG_MIN = 44.0, 32.0, 32.0, 58.0
CARDS_MAX, ARROWS_MAX = 4, 2
# 🔴 2026-11-08（31本目 ⑤b-1・§0b）：札の枚数の例外は**カットIDの直書き**＝30本目の `{"cc15": dict(cards=5)}`（まとめの「反省は3つ」）は見本 `tools/fixture_ep30.py` の EXC へ移した
#    （git の `3d0ee6bc`）。31本目にも cc15 がある＝残すと31本目の cc15 の札が黙って5枚まで通る。31本目で例外が要るなら、そのカットを承認の数だけ書く
EXC = {}
BAND_MAX, BAND_MIN = 8, 34.0       # ⚠️ ⑤b-5 の最初の値（無線帯の語の実測は最大7字「ガソリンの匂い」・字は 38）


def _len(t):
    return len(t.replace("「", "").replace("」", ""))


def judge(cid, geo, sec, nlines):
    """(直すものの列, 測った値の辞書) を返す。"""
    bad = []
    total, cards = 0, 0
    lim = dict(head=HEAD_MAX, body=LINE_MAX, sub=SUB_MAX, big=BIG_MAX)
    low = dict(head=HEAD_MIN, body=BODY_MIN, sub=SUB_MIN, big=BIG_MIN)
    worst = dict(lines=0, card=0, size=999.0)
    for c in geo["cards"]:
        n_card = 0
        for kind, t, cap in c["rows"]:
            n = _len(t)
            n_card += n
            worst["lines"] = max(worst["lines"], n if kind == "body" else 0)
            if n > lim[kind]:
                bad.append(f"F1 {cid} 札 {c['id']} の「{t}」が {n}字（{kind} は {lim[kind]}字まで）")
            if not c["dim"] and cap < low[kind]:
                bad.append(f"F4 {cid} 札 {c['id']} の「{t}」の大きさ {cap:.0f}（{kind} は {low[kind]:.0f} 以上）")
            worst["size"] = min(worst["size"], cap if kind == "body" else 999.0)
        worst["card"] = max(worst["card"], n_card)
        if n_card > CARD_MAX:
            bad.append(f"F2 {cid} 札 {c['id']} が {n_card}字（{CARD_MAX}字まで）")
        if not c["dim"]:
            cards += 1
            total += n_card
    if total > sec * CPS:
        bad.append(f"F3 {cid} 画面の字 {total}字／{sec:.1f}秒＝毎秒 {total / max(sec, 0.1):.1f}字（{CPS:.0f}字まで）")
    cap_cards = EXC.get(cid, {}).get("cards", CARDS_MAX)
    if cards > cap_cards:
        bad.append(f"F5 {cid} 札 {cards}枚（{cap_cards}枚まで）")
    if geo["narrows"] > ARROWS_MAX:
        bad.append(f"F5 {cid} 矢印 {geo['narrows']}本（{ARROWS_MAX}本まで）")
    if geo["n"] < nlines:
        bad.append(f"F6 {cid} 段 {geo['n']}＜語りの行 {nlines}")
    for i in geo["mute"]:
        if not 0 <= int(i) < nlines:
            bad.append(f"F6 {cid} mute の行 {i} が語りの行（0〜{nlines - 1}）に無い")
    for tm, kw, cap in geo.get("band", ()):
        if _len(kw) > BAND_MAX:
            bad.append(f"F7 {cid} 無線帯の {tm} の語「{kw}」が {_len(kw)}字（{BAND_MAX}字まで）")
        if cap < BAND_MIN:
            bad.append(f"F7 {cid} 無線帯の {tm} の字の大きさ {cap:.0f}（{BAND_MIN:.0f} 以上）")
    return bad, dict(worst, total=total, cps=total / max(sec, 0.1), cards=cards)


def _inputs():
    import cuts
    import mech30 as M
    import scene_jiko as S
    # 🔧 2026-11-08（31本目 ⑤b-1・§0b）：秒の表を回の束（`ss.REF`）から引く＝30本目の `ref/ep30/eizou_build/list30.tsv` の直書きをやめた（回を替えるとき直し忘れない）
    import cuts.ss as _ss
    secs = {r["cid"]: float(r["sec"]) for r in csv.DictReader(open(_ss.REF / "eizou_build" / f"list{_ss.REF.name[2:]}.tsv", encoding="utf-8"), delimiter="\t")}
    # 🆕 31本目 ⑤b-4（2026-11-08）：札の型 m31（`tools/mech31.py`＝30本目の型を写した）も同じ物差しで測る＝カットごとに型のモジュールを引く
    import mech31 as M31
    # 🆕 32本目 ⑤b-5（2026-11-11）：m32（`tools/mech32.py`＝31本目の型の式を import）も同じ物差し
    import mech32 as M32
    mods = {"m30": M, "m31": M31, "m32": M32}
    targets = [c for c, s in sorted(cuts.SPEC.items()) if s.get("fig") and s["fig"][0] in mods]
    kinds = {c: mods[cuts.SPEC[c]["fig"][0]] for c in targets}
    return kinds, S, secs, targets


def selftest():
    M, _S, _secs, _t = _inputs()
    ok = True

    def control(name, geo, sec, nlines, want):
        nonlocal ok
        bad, _v = judge("c999", geo, sec, nlines)
        hit = any(b.startswith(want) for b in bad)
        ok = ok and hit
        print(f"  {'OK' if hit else '🔴 NG'} 陽性対照「{name}」→ {'鳴った' if hit else '鳴らなかった'}")

    def geo_of(rows, n=2, narrows=0, cards=1):
        return dict(cards=tuple(dict(id="abcdefgh"[i], dim=False, rows=rows) for i in range(cards)), narrows=narrows, n=n, mute=())

    good = geo_of((("body", "ふつうの長さの札", 56.0),))
    bad, _v = judge("c999", good, 10.0, 2)
    print(f"  {'OK' if not bad else '🔴 NG'} ふつうの札は黙る {bad[:1]}")
    ok = ok and not bad
    control("本文の1行が長い", geo_of((("body", "あ" * 30, 56.0),)), 10.0, 2, "F1")
    control("札1枚の字が多い", geo_of((("body", "あ" * 24, 56.0), ("body", "あ" * 24, 56.0))), 10.0, 2, "F2")
    control("短い尺に字が多い", geo_of((("body", "あ" * 24, 56.0),), cards=2), 5.0, 2, "F3")
    control("本文の字が小さい", geo_of((("body", "ふつう", 30.0),)), 10.0, 2, "F4")
    control("札が多い", geo_of((("body", "ふつう", 56.0),), cards=5), 30.0, 2, "F5")
    control("矢印が多い", geo_of((("body", "ふつう", 56.0),), narrows=3), 10.0, 2, "F5")
    control("段が語りの行より少ない", geo_of((("body", "ふつう", 56.0),), n=1), 10.0, 2, "F6")
    control("mute の行が無い", dict(geo_of((("body", "ふつう", 56.0),)), mute=(5,)), 10.0, 2, "F6")
    control("無線帯の語が長い", dict(geo_of((("body", "ふつう", 56.0),)), band=(("8:21", "あ" * 12, 38.0),)), 10.0, 2, "F7")
    control("無線帯の字が小さい", dict(geo_of((("body", "ふつう", 56.0),)), band=(("8:21", "病人2名", 24.0),)), 10.0, 2, "F7")
    return ok


def main():
    if "--selftest" in sys.argv:
        ok = selftest()
        print("selftest:", "通った" if ok else "🔴 落ちた")
        return 0 if ok else 1
    kinds, S, secs, targets = _inputs()
    if not targets:
        print("札の型のカットが0件（この回に m30・m31 が無いなら正しい）")
        return 0
    n_bad = 0
    vals = []
    for c in targets:
        geo = kinds[c].geo_of(c)
        nlines = len(S.SUBS.get(c) or [])
        bad, v = judge(c, geo, secs[c], nlines)
        vals.append((c, v))
        n_bad += len(bad)
        for b in bad:
            print("🔴", b)
    if "--dist" in sys.argv:
        for key in ("lines", "card", "total", "cps", "size", "cards"):
            xs = sorted((v[key], c) for c, v in vals)
            print(f"{key}: 最小 {xs[0][0]:.1f}（{xs[0][1]}）・中央 {xs[len(xs) // 2][0]:.1f}・最大 {xs[-1][0]:.1f}（{xs[-1][1]}）")
    print(f"✓ 札の型 {len(targets)}カット" if not n_bad else f"🔴 {n_bad}件（{len(targets)}カット）")
    return 0 if not n_bad else 1


if __name__ == "__main__":
    sys.exit(main())
