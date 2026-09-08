# -*- coding: utf-8 -*-
"""切り出し窓が**空っぽ**になっていないかの門番（2026-09-07 新設・工程の新設計 §9-3）。

■ なぜ要るか（2026-09-06・4本目サーフサイド ⑤c'）
    `tf_p076_bars.jpg` は**右半分に何も描かれていない**のに、`xbias` が白紙側を向いていて
    **1ファイルで5カットぶん壊れた**。机上検査5種は1つも鳴らない（重なりも複写も無く、
    貼り位置は「正しい」ため）。→ [[feedback-measure-the-source-before-choosing-the-crop]]

■ 🔴 「白紙率 80%」はやめた（2026-09-07・この道具を作った日に実測して捨てた）
    設計ノート §9-3 は「白紙率 80% 超で 🔴」と書いてあったが、**そのままでは使えなかった**。
    白い紙に描いた図面は**もともと 75〜90% が白**で、本番 94カットに当てると
    **公開ずみ・目視ずみの回で 12件が 🔴** になった。分布にも切れ目が無い
    （0.75〜0.80 に 9件・0.80〜0.85 に 6件と連続）。
    事故の再現（旧 p076 の右半分）は 92〜99% で、**本番の上位と重なる**。
    ＝ 白紙率では「白い紙」と「空っぽ」が分けられない。
    → [[feedback-verify-your-own-instrument]]「壊れようのない量に乗り換えられないかを先に考える」

■ 何で測るか（本番と事故で切れているのはこの2つ。実測 2026-09-07）
    | | 本番 94カット（公開ずみ） | 事故の再現（旧 p076 の右半分） |
    |---|---|---|
    | **インク率**（白でない画素の割合） | 最小 0.045・1%点 0.052 | **0.007〜0.038** |
    | **空白帯**（窓の端から続く無インクの帯の割合） | 最大 0.392 | **0.47〜0.80** |
    | 白紙率（捨てた） | 12件が 80%超 | 92〜99%（重なる） |
    しきい値は**この切れ目の間**に置いた（[[feedback-gate-threshold-from-ledger-split]]）。
    白紙率は 🔴 には使わないが、**表には必ず出す**（設計ノートの数字を消さないため）。

■ ⚠️ この道具が**見ていない**もの
    1. **絵はあるが意味が無い**（表題カードなど）＝ `footage.py` の `until=` の担当
    2. 動画を当てたカット（スライドが映らない）＝ そもそも見ない
    3. 「インクはあるが読めない」＝ `check_slide.py` の担当

■ 使い方
    python tools/check_blank.py                 # 検査
    python tools/check_blank.py --hist          # 分布（しきい値を決め直すとき）
    python tools/check_blank.py --all           # 惜しい物も出す
    python tools/check_blank.py --check         # 🔴 陽性対照（旧 tf_p076_bars.jpg を git から取る）
"""
from __future__ import annotations

import io
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.stdout.reconfigure(encoding="utf-8")

import check_slide as CS      # noqa: E402  幾何（crop_rect）と本番の入力はここ1本から借りる

HERE = Path(__file__).resolve().parent.parent
REF = HERE / "ref"

INK_DARK = 200     # R,G,B のどれかがこれ未満なら「インク」
INK_MIN = 0.040    # 🔴 窓のインク率がこれ未満（本番の最小 0.045／事故 0.007〜0.038）
EMPTY_COL = 0.004  # 「その列（行）にインクが無い」とみなす割合
BAND_MAX = 0.45    # 🔴 端から続く無インクの帯がこの割合以上（本番の最大 0.392／事故 0.47〜0.80）
WHITE = 240        # 参考に出す「白紙率」の白（🔴 の判定には使わない）
SAMPLE = 4         # 画素の間引き（面の性質なので間引いても値は変わらない）

Image.MAX_IMAGE_PIXELS = None
_CACHE: dict[str, np.ndarray] = {}


def load_arr(name):
    if name not in _CACHE:
        p = REF / name
        if not p.exists():
            raise SystemExit(f"🔴 素材が無い: {p}")   # fail closed（0 で埋めない）
        with Image.open(p) as im:
            _CACHE[name] = np.asarray(im.convert("RGB"), dtype=np.uint8)
    return _CACHE[name]


def edge_band(v):
    """端から続く「インクの無い」帯が、その辺の何割か（左右／上下の大きいほう）。"""
    e = v < EMPTY_COL
    n = len(v)
    lo = 0
    while lo < n and e[lo]:
        lo += 1
    hi = 0
    while hi < n and e[n - 1 - hi]:
        hi += 1
    return max(lo, hi) / n if n else 0.0


def measure(arr, r):
    """その窓の (インク率, 空白帯, 白紙率)。⚠️ 窓は原画からはみ出しうるので切り詰める。"""
    h, w = arr.shape[:2]
    x0 = max(0, int(round(r["left"])))
    y0 = max(0, int(round(r["top"])))
    x1 = min(w, int(round(r["left"] + r["cw"])))
    y1 = min(h, int(round(r["top"] + r["ch"])))
    if x1 - x0 < 8 or y1 - y0 < 8:
        return None
    win = arr[y0:y1:SAMPLE, x0:x1:SAMPLE]
    ink = win.min(axis=2) < INK_DARK
    band = max(edge_band(ink.mean(axis=0)), edge_band(ink.mean(axis=1)))
    white = float((win.min(axis=2) >= WHITE).mean())
    return float(ink.mean()), float(band), white


def scan(spec_map, photo_of, box_of, skip):
    """🔴 本番も陽性対照もこの1本を通る（判定を2か所に書かない）。

    返すのは (cid, 素材名, k, インク率, 空白帯, 白紙率, 粗の理由)。理由が空なら合格。
    ⚠️ **両端 k=0/k=1 のうち「いちばん悪いほう」**を採る（片端だけ空になることがある）。
    """
    rows = []
    for cid in sorted(spec_map):
        if cid in skip:
            continue
        name = photo_of.get(cid)
        if not name:
            continue
        spec = spec_map[cid]
        arr = load_arr(name)
        sh, sw = arr.shape[0], arr.shape[1]
        worst = None
        for k in (0.0, 1.0):
            r = CS.crop_rect(sw, sh, box_of[cid], k, spec.get("bias", 0.5),
                             spec.get("xbias", 0.5), spec.get("zoom", 1.0))
            got = measure(arr, r)
            if got is None:
                continue
            ink, band, white = got
            why = []
            if ink < INK_MIN:
                why.append(f"インク率 {ink:.1%}（下限 {INK_MIN:.1%}）")
            if band >= BAND_MAX:
                why.append(f"端の {band:.0%} が無地の帯（上限 {BAND_MAX:.0%}）")
            row = (cid, Path(name).name, k, ink, band, white, "／".join(why))
            # 「悪い」の順＝粗ありが優先、次にインクの薄いほう
            key = (0 if why else 1, ink)
            if worst is None or key < worst[0]:
                worst = (key, row)
        if worst is None:
            rows.append((cid, Path(name).name, None, None, None, None,
                         "切り出し窓が原画の外（測れない）"))
        else:
            rows.append(worst[1])
    return rows


# ── 🔴 承知のうえで薄いカット（2026-09-07・5本目 SL-1）─────────────
# ⚠️ **しきい値は動かさない。**5本目の本番77件に当てても分布の切れ目は同じ場所に在る
#    （0.00〜0.04 に 7件・0.04〜0.05 に 0件・0.05〜0.07 に 14件）。動かすと
#    「白紙側を向いた xbias」を二度と拾えなくなる。→ [[feedback-gates-go-stale-when-upstream-changes]]
# 🔴 代わりに**カットを名指しで、理由つきで**外す。理由の無い名前は置けない（下の検算で落ちる）。
# ⚠️ 外した件も**数字ごと必ず表に出す**（黙って消さない）。
#
# 🔴🔴 2026-09-09（6本目 ⑤b-5）── **ここに5本目の除外が4件そのまま残っていた。**
#    `c704`＝「AEC 調査委員会報告の表紙」`c908`＝「ANL-6692 の表紙」は **SL-1（5本目）の素材**で、
#    6本目（キー橋）の c704／c705／c903／c908 とは中身がまったく別のカット。
#    カットIDは題材をまたいでぶつかるので、**前の題材の除外が黙って効き続ける**。
#    ＝ 6本目で本当に真っ白なカットが出ても、この4つのIDなら門番は黙っていた。
#    → [[feedback-gates-go-stale-when-upstream-changes]]（門番は壊れず、黙って間違った合格を出す）
#    → [[project-jiko-rules-index]] §0b（カットIDの題材またぎ）
#    この門番自身の「陳腐化した除外」の検査が鳴って気づけた。**その検査は消さないこと。**
# ⚠️ 題材を替えたら、まずここを空にする。載せるときは**その題材の素材名**を理由に書く。
ON_PURPOSE = {
}


def report(rows, show_all=False, hist=False):
    bad = [r for r in rows if r[6] and r[0] not in ON_PURPOSE]
    knew = [r for r in rows if r[6] and r[0] in ON_PURPOSE]
    print(f"■ スライドが映るカット {len(rows)} 件を、k=0 と k=1 の両端で見た"
          f"（インク＝R,G,B のどれかが {INK_DARK} 未満）")
    for cid, name, k, ink, band, white, why in sorted(bad, key=lambda r: (r[3] or 0)):
        kk = f"k={k:.0f}" if k is not None else "—"
        extra = f"  白紙率 {white:.0%}" if white is not None else ""
        print(f"  🔴 {cid}  {why}（{kk}・{name}）{extra}")
    for cid, name, k, ink, band, white, why in sorted(knew, key=lambda r: (r[3] or 0)):
        print(f"  ⚠️ {cid}  {why}（{name}）  白紙率 {white:.0%}")
        print(f"      承知のうえ：{ON_PURPOSE[cid]}")
    if show_all or hist:
        near = [r for r in rows if not r[6] and r[3] is not None
                and (r[3] < INK_MIN * 2 or r[4] > BAND_MAX * 0.75)]
        for cid, name, k, ink, band, white, _ in sorted(near, key=lambda r: r[3]):
            print(f"  ・ {cid}  インク率 {ink:.1%}・空白帯 {band:.0%}"
                  f"（k={k:.0f}・{name}）  白紙率 {white:.0%}")
    if hist:
        ok = [r for r in rows if r[3] is not None]
        for label, idx, edges in (
                ("インク率", 3, [0, .04, .05, .07, .10, .15, .25, .50, 1.01]),
                ("空白帯", 4, [0, .05, .15, .25, .35, .40, .45, .60, 1.01]),
                ("白紙率（参考・🔴 には使わない）", 5,
                 [0, .40, .60, .70, .80, .85, .90, 1.01])):
            print(f"  ── {label} の分布")
            for a, b in zip(edges, edges[1:]):
                n = sum(1 for r in ok if a <= r[idx] < b)
                print(f"     {a:.2f}〜{b:.2f}  {'#' * min(n, 60)} {n}")
        w80 = sum(1 for r in ok if r[5] > 0.80)
        print(f"  ⚠️ 参考：白紙率 80% 超は {w80}件"
              f"（設計ノートの旧しきい値。**白い紙の図面がここに入る**ので 🔴 にしない）")
    # 🔴 名指しの例外に、いま鳴っていないカットが残っていたら**それも粗**（陳腐化した除外）
    stale = sorted(set(ON_PURPOSE) - {r[0] for r in rows if r[6]})
    for cid in stale:
        print(f"  🔴 {cid} は `ON_PURPOSE` に載っているが、いまは鳴っていない。"
              f"除外を消すこと（陳腐化した除外は、次の粗を黙って通す）")
    if bad or stale:
        print(f"🔴 切り出し窓が空っぽのカットが {len(bad)} 件"
              + (f"／陳腐化した除外 {len(stale)} 件" if stale else ""))
    else:
        thin = min((r[3] for r in rows if r[3] is not None and r[0] not in ON_PURPOSE),
                   default=0)
        wide = max((r[4] for r in rows if r[4] is not None and r[0] not in ON_PURPOSE),
                   default=0)
        print(f"✓ どのカットの切り出し窓にも中身がある"
              f"（いちばん薄いインク率 {thin:.1%}／いちばん広い空白帯 {wide:.0%}）"
              + (f"／承知のうえで薄い {len(knew)} 件" if knew else ""))
    return bool(bad or stale)
    return len(bad)


def main(show_all=False, hist=False):
    sm, po, bo, skip = CS.production_inputs()
    return 1 if report(scan(sm, po, bo, skip), show_all, hist) else 0


# ── 陽性対照 ─────────────────────────────────────────────
OLD_COMMIT = "431474d"
OLD_FILE = "ref/surfside/tf_p076_bars.jpg"


def selfcheck():
    """🔴 旧 `tf_p076_bars.jpg`（右半分が白紙）を git から取り出し、**本番の scan()** に通す。

    ⚠️ ここは2026-09-07 に一度**空振りした**。旧版に差し替えただけでは鳴らない。
       直しは「ファイルの差し替え」ではなく **`xbias` を左半分へ向け直したこと**だったので、
       いまの spec の窓は旧版でも新版でも**まったく同じ絵**を見ている（インク率 12.5% で一致）。
       → 事故当時の状態は「**旧の絵 ＋ 白紙側を向いた xbias**」。両方を戻さないと復元にならない
         （[[feedback-verify-your-own-instrument]]「テスト入力が事故当時の状態を復元しているか」）。
    """
    ok = True

    def say(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '🔴'} {msg}")

    # 🔴 名指しの除外そのものの検算（本番の中身に依らない。ここは題材を替えても回る）
    #    ⚠️ 2026-09-07：`ON_PURPOSE` を足したので、**除外が何でも飲み込まないこと**を先に見る。
    fake = [("x01", "a.png", 0.0, 0.001, 0.9, 0.99, "インク率 0.1%"),
            ("c705", "b.png", 0.0, 0.008, 0.47, 0.99, "インク率 0.8%")]
    import io as _io
    import contextlib
    buf = _io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = report(fake)
    say(rc is True, "名指しに載っていない薄いカット（x01）は、除外があっても鳴る")
    say("⚠️ c705" in buf.getvalue(),
        "名指しに載っているカット（c705）は、数字ごと ⚠️ で表に出る")
    with contextlib.redirect_stdout(buf):
        rc2 = report([r for r in fake if r[0] == "c705"])
    say(rc2 is True, "🔴 除外が陳腐化していない（x01 が消えたら『載っているのに鳴っていない』で落ちる）")

    sm, po, bo, skip = CS.production_inputs()
    victims = sorted(c for c, n in po.items()
                     if Path(n).name == Path(OLD_FILE).name and c not in skip)
    if not victims:
        print(f"  ⚠️ {Path(OLD_FILE).name} を使うカットが1つも無い"
              f"（4本目の素材。題材を替えたので当てられない）"
              f"→ 絵を使う陽性対照は飛ばし、上の3項目だけで判定する")
        print("  " + ("✓ 陽性対照（除外の検算のみ）" if ok
                      else "🔴 陽性対照が落ちた"))
        return ok

    # 1) いまの本番の spec では黙る（鳴りすぎの検算）
    base = scan({c: sm[c] for c in victims}, po, bo, skip)
    say(not [r for r in base if r[6]],
        "いまの spec では黙る（" + "／".join(f"{r[0]} インク{r[3]:.1%}" for r in base) + "）")

    # 2) git から旧版を取る。取れなければ緑と言わない（fail closed）
    blob = subprocess.run(["git", "show", f"{OLD_COMMIT}:{OLD_FILE}"],
                          cwd=HERE, capture_output=True)
    if blob.returncode != 0 or len(blob.stdout) < 5000:
        print(f"  🔴 git から旧 {OLD_FILE} を取り出せない "
              f"(rc={blob.returncode}, {len(blob.stdout)}バイト)")
        return False
    old = np.asarray(Image.open(io.BytesIO(blob.stdout)).convert("RGB"), dtype=np.uint8)
    _CACHE["__old__"] = old
    new = load_arr(po[victims[0]])
    say(old.shape == new.shape and not np.array_equal(old, new),
        f"旧版と今版は同じ寸法で中身が違う（{old.shape[1]}x{old.shape[0]}）")

    # 3) 🔴 事故当時＝旧の絵 ＋ 白紙側（右）を向いた xbias。名指しで鳴るのを見る
    victim = victims[0]
    po2 = dict(po); po2[victim] = "__old__"
    crime = dict(sm[victim]); crime["xbias"] = 1.0
    got = scan({victim: crime}, po2, bo, skip)[0]
    say(bool(got[6]), f"事故当時の復元（旧の絵＋xbias=1.0）で {victim} が鳴る → {got[6] or '鳴らない'}")

    # 4) ⚠️ 片方だけ戻したら鳴ってはいけない（＝何にでも鳴る道具ではない）
    only_aim = scan({victim: crime}, po, bo, skip)[0]          # 今の絵＋白紙側を向く
    say(not only_aim[6], f"今の絵なら xbias=1.0 でも黙る（インク {only_aim[3]:.1%}）")
    only_img = scan({victim: sm[victim]}, po2, bo, skip)[0]    # 旧の絵＋今の向き
    say(not only_img[6], f"旧の絵でも今の向きなら黙る（インク {only_img[3]:.1%}）")

    # 5) 幾何（両端を見る意味があるか）
    a = CS.crop_rect(3200, 1570, (0, 0, 1920, 1080), 0.0, .5, .5, 2.0)
    b = CS.crop_rect(3200, 1570, (0, 0, 1920, 1080), 1.0, .5, .5, 2.0)
    say(b["cw"] < a["cw"], f"k=1 の窓は k=0 より狭い（{a['cw']:.0f}px → {b['cw']:.0f}px）")

    # 6) 物差しそのもの
    r = dict(left=0, top=0, cw=200, ch=200)
    half = np.concatenate([np.zeros((200, 100, 3), np.uint8),
                           np.full((200, 100, 3), 255, np.uint8)], axis=1)
    for name, a_, want in (("真っ白", np.full((200, 200, 3), 255, np.uint8), (0.0, 1.0)),
                           ("真っ黒", np.zeros((200, 200, 3), np.uint8), (1.0, 0.0)),
                           ("右半分だけ白", half, (0.5, 0.5))):
        ink, band, _ = measure(a_, r)
        good = abs(ink - want[0]) < .02 and abs(band - want[1]) < .03
        say(good, f"物差し：{name} → インク率 {ink:.0%}・空白帯 {band:.0%}"
                  f"（期待 {want[0]:.0%}・{want[1]:.0%}）")

    print("  " + ("✓ 陽性対照 9/9" if ok else "🔴 陽性対照に落ちた"))
    return ok


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(0 if selfcheck() else 1)
    sys.exit(main(show_all="--all" in sys.argv, hist="--hist" in sys.argv))
