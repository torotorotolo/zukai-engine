# -*- coding: utf-8 -*-
"""check_photo_edge.py — 全画面の写真の窓が、**スライドの台紙の黒い縁**に入っていないか（2026-10-13 新設・21本目 ⑤b-7）。

■ なぜ要るか
  議会図書館のスライド（LC-A05 のロール・item 210）・EPA DOCUMERICA・Korab のスライドの走査は、四辺に台紙の黒い縁がある
  （21本目の束で 下 0.6〜3.7%・左右 0〜1.6%）。全画面で「流す」「寄る」と、寄せの端（xbias・bias が 0 か 1）や寄り 1.0 で縁が画面に入る。
  冒頭 c102 は手で避けた（寄り 1.12・寄せ 0.2→0.8＝`cuts/c1.py` の注「pan_r は寄せ 0→1＝端の黒い縁が入る」）が、**門番が無かった**。
  ⑤b-7 で同じ型の写真が11カットに増えた（流す・寄る・2点）。門番 blank は紙の図の空の窓、slide は焼き込みの文字＝どちらも縁を見ない。
  → [[feedback-rules-need-gates]]

■ 測るもの（fail closed）
  1. 縁のある写真＝`cuts/ss.py` の SLIDE_MOUNT。縁の幅は**絵から毎回測る**（定数に書かない＝束を作り直しても腐らない）：
     辺から EDGE_CAP 以内で、辺の中ほど 60% の帯の輝度の 80 パーセンタイルが EDGE_DARK 未満の行（列）のうち、いちばん内側までの幅。
     ⚠️ 作った日に一度、「辺から続く暗い行」で測って**外した**：暗いビル街（LC-A10 の下 38%）・cc03 の暗がり（右 56%）まで縁に数え、
        陰性対照の c102 が鳴った。台紙は一様に真っ黒（95 パーセンタイル 8〜22・幅は最大 4% 未満）・絵の暗がりは 27 以上＝辺から 5% までに限る
        （辺の1列目が明るい写真＝LC-A03 の右があるので「続く」でなく「いちばん内側」）→ [[feedback-verify-your-own-instrument]]
  2. その写真を当てた**全画面**のカットの窓を、本番の切り方（`check_slide.cam_rects`＝cam の3点・cam が無ければ既定の寄りの2点）で出し、
     4辺それぞれ「縁の幅＋GUARD」より内側か。
  ⚠️ 見ないもの：額装（panel）・額ごと動かす（fmove）の写真＝台紙ごと見せる。映像（`footage.USE` の欄）。SLIDE_MOUNT に無い写真の暗い所（夜空など）。
  3. 🆕 2026-10-14（22本目 ⑤b-2）：**SLIDE_MOUNT が空の回**（スライドの走査が無い回）＝束の全点の四辺を同じ物差しで測り、MIN_EDGE 以上の暗い帯が
     ある点が `ss.SLIDE_NOT_MOUNT`（暗いが台紙でないと絵と数で決めた点・理由つき）に全部あれば ✓。載っていない点・束に無い名は止める。
     両方とも空なら今までどおり「名簿が読めていない」で止める（21本目 ⑤b-1 の宿題＝「無い」を名簿の注で言える形）

■ 使い方
    python tools/check_photo_edge.py
    python tools/check_photo_edge.py --selftest    # 陽性対照（c102 の写真をプリセットの pan_r＝寄せ 0→1 で流すと鳴る）・陰性対照（c102 の本番）
"""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

EDGE_DARK = 32      # 縁の行（列）＝帯の輝度の 80 パーセンタイルがこれ未満（台紙は 8〜23・暗いビル街は 38 以上＝⑤b-7 の実測）
EDGE_CAP = 0.05     # 縁を探す深さ（画像の割合）＝台紙の幅は 21本目の束で最大 4% 未満。これより内の暗がりは絵
GUARD = 0.003       # 縁の幅に足す余白（画像の割合）
MIN_EDGE = 0.012    # 名簿の写真の縁の下限＝暗さで測れない辺がある（LC-A01・A05・B20 の上・A01・A05・A06 の左＝台紙が緑がかって明るい）


@lru_cache(maxsize=None)
def margins(name):
    """写真（`ref/` から見た名）の四辺の縁の幅（画像の割合）＝dict(l, t, r, b)。読めなければ例外（fail closed）"""
    a = np.asarray(Image.open(HERE / "ref" / name).convert("L"), dtype=np.float32)
    h, w = a.shape
    y0, y1, x0, x1 = int(h * .2), int(h * .8), int(w * .2), int(w * .8)
    rows = np.percentile(a[:, x0:x1], 80, axis=1)
    cols = np.percentile(a[y0:y1, :], 80, axis=0)

    def run(seq):
        n = int(len(seq) * EDGE_CAP)
        dark = [i for i in range(n) if seq[i] < EDGE_DARK]
        return dark[-1] + 1 if dark else 0
    return dict(t=run(rows) / h, b=run(rows[::-1]) / h, l=run(cols) / w, r=run(cols[::-1]) / w)


def window_fracs(r, sw, sh):
    """check_slide.crop_rect の窓 → 4辺の内側への距離（画像の割合）"""
    return dict(l=r["left"] / sw, t=r["top"] / sh, r=1 - (r["left"] + r["cw"]) / sw, b=1 - (r["top"] + r["ch"]) / sh)


def sweep(not_mount, db=None):
    """🆕 2026-10-14（22本目 ⑤b-2）：名簿 SLIDE_MOUNT が空の回＝「台紙の縁のある写真は無い」の確かめ。束（`ss._assets()`）の全点の四辺を
    margins で測り、MIN_EDGE 以上の暗い帯がある点が SLIDE_NOT_MOUNT（暗いが台紙でないと見て決めた点）に全部あるか。(所見, 悪い数)
    ⚠️ 束が空・読めないなら止める（0点を「縁は無い」にしない）。名簿に載っていて束に無い名も止める（古い名簿）"""
    import cuts.ss as ss
    db = ss._assets() if db is None else db
    if not db:
        return ["🔴 束（assets.json）が空＝何も測っていない（fail closed）"], 1
    out, bad, dark = [], 0, 0
    names = {ss.P(n) for n in db if not n.startswith("fb_")}        # 映像のひかえ（fb_）は見ない＝映像は門番の外（上の「見ないもの」）
    for name in sorted(names):
        m = margins(name)
        if max(m.values()) < MIN_EDGE:
            continue
        dark += 1
        if name not in not_mount:
            out.append(f"🔴 {name}: 四辺に暗い帯（左 {m['l'] * 100:.1f}%・上 {m['t'] * 100:.1f}%・右 {m['r'] * 100:.1f}%・下 {m['b'] * 100:.1f}%）"
                       "があるのに、台紙の縁か（SLIDE_MOUNT）写真の中身か（SLIDE_NOT_MOUNT）を決めていない＝絵を見て名簿に書く")
            bad += 1
    for name in sorted(set(not_mount) - names):
        out.append(f"🔴 {name}: SLIDE_NOT_MOUNT にあるが束に無い（古い名簿）")
        bad += 1
    if not bad:
        out.append(f"✓ 台紙の縁のある写真は0点（SLIDE_MOUNT は空）＝束 {len(names)}点を測り、暗い帯のある {dark}点はどれも写真の中身と"
                   "決めてある（SLIDE_NOT_MOUNT）")
    return out, bad


def check(spec=None, mount=None, use=None, not_mount=None, db=None):
    """(所見の一覧, exit)。spec・mount・use・not_mount を渡さなければ本番（cuts.SPEC・ss.SLIDE_MOUNT・footage.USE・ss.SLIDE_NOT_MOUNT）"""
    import check_slide as CS
    import cuts.ss as ss
    if spec is None:
        import cuts
        spec = cuts.SPEC
    mount = ss.SLIDE_MOUNT if mount is None else mount
    not_mount = getattr(ss, "SLIDE_NOT_MOUNT", {}) if not_mount is None else not_mount
    if use is None:
        import footage
        use = footage.USE
    if not mount:
        # 🆕 2026-10-14（22本目 ⑤b-2）：名簿が空でも「暗い帯のある点を全部見て、台紙でないと決めた」なら、この回に縁のある写真は無いと言える
        if not not_mount:
            return ["🔴 SLIDE_MOUNT が空（縁のある写真の名簿が読めていない＝fail closed）。台紙の縁のある写真が無い回なら、"
                    "暗い帯のある点を ss.SLIDE_NOT_MOUNT に理由つきで書く（`qa_out/<回>_assets.py edges`）"], 2
        out, bad = sweep(not_mount, db)
        return out, (2 if bad else 0)
    import scene_jiko as S
    out, bad, seen = [], 0, 0
    for name in sorted(mount):
        if not (HERE / "ref" / name).exists():
            out.append(f"🔴 {name}: 名簿にあるが ref/ に無い")
            bad += 1
    for cid, s in spec.items():
        name = s.get("photo")
        if name not in mount or s.get("panel") or s.get("fmove") or cid in use:
            continue
        m = margins(name)
        sw, sh = ss.trimmed_size(name)
        box = S.photo_box(s)
        rects = CS.cam_rects(sw, sh, box, s)
        seen += 1
        worst = []
        for k, r in rects.items():
            f = window_fracs(r, sw, sh)
            for side in "ltrb":
                need = max(m[side], MIN_EDGE) + GUARD
                if f[side] + 1e-6 < need:
                    worst.append(f"{'頭中尻'[int(k * 2)] if s.get('cam') else ('寄る前' if k == 0 else '寄ったあと')}の{'左上右下'['ltrb'.index(side)]}"
                                 f"（窓の内側 {f[side] * 100:.1f}%＜縁 {m[side] * 100:.1f}%＋{GUARD * 100:.1f}）")
        if worst:
            out.append(f"🔴 {cid}: {name} の窓が台紙の縁に入る＝{'・'.join(worst[:4])}{'…' if len(worst) > 4 else ''}"
                       "（寄りを上げるか寄せを端から離す＝ss.mv の lo・span）")
            bad += 1
    if seen == 0:
        out.append("🔴 縁のある写真を当てた全画面のカットが0＝この検査は何も見ていない（名簿か SPEC の読み違い）")
        bad += 1
    else:
        out.append(f"{'✓' if not bad else '🔴'} 縁のある写真の全画面カット {seen}件を測った（名簿 {len(mount)}点）")
    return out, (2 if bad else 0)


def selftest():
    """🔴 2026-10-14（22本目 ⑤b-1・§0b）：21本目の実物（c102＝LC-A17・ss.SLIDE_MOUNT）は本番から見本 `tools/fixture_ep21.py` へ移した
    ＝見本の ss の表（SLIDE_MOUNT ほか）と21本目の章ファイル（apply_cuts＝git の `35fab37`）を差して回し、最後に restore（LIFO）"""
    import fixture_ep21
    import cuts.ss as ss
    ok_none = _selftest_none()          # 🆕 22本目 ⑤b-2：名簿が空の回の確かめ（本番の束のまま＝見本を差す前に）
    # 写真の権利の台帳（`ss._assets()`＝`ss.REF / "assets.json"`・起動時に1回読んで覚える）も21本目へ向ける＝見本の SPEC の写真の
    # 額装の網（frame_only）が21本目の台帳で引ける。REF・EP は束の道＝見本の SS_NAMES に入れない名なので、ここで差して戻す
    keep = (ss.REF, ss.EP)
    ss.REF, ss.EP = fixture_ep21.REF, "ep21/"
    ss._assets.cache_clear()
    fixture_ep21.apply()
    fixture_ep21.apply_cuts()
    try:
        rc = _selftest()
        return rc if ok_none else 2
    finally:
        fixture_ep21.restore()
        ss.REF, ss.EP = keep
        ss._assets.cache_clear()


def _selftest():
    import cuts
    import cuts.ss as ss
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(f"{'✓' if cond else '🔴'} {label}")
        ok &= bool(cond)
    a17, a10 = "ep21/lc_a05_a17.jpg", "ep21/lc_a05_a10.jpg"     # 21本目の束の名（見本＝ss.P は今の回の名を作る）
    base = cuts.SPEC.get("c102")
    chk("見本 c102 が SPEC にある（冒頭の LC-A17）", bool(base) and base.get("photo") == a17)
    chk("見本の名簿 SLIDE_MOUNT に LC-A17 がある（fixture_ep21）", a17 in ss.SLIDE_MOUNT)
    m = margins(a17)
    chk(f"物差し：LC-A17 の下の縁が 1.5% 以上（測った値 {m['b'] * 100:.1f}%＝⑤b-7 の borders.py は 2.5%）", m["b"] >= 0.015)
    m10 = margins(a10)
    chk(f"物差し：LC-A10 の下の暗いビル街を縁に数えない（測った値 {m10['b'] * 100:.1f}%＜{EDGE_CAP * 100:.0f}%・作った日の物差しは 38%）",
        0.01 <= m10["b"] < EDGE_CAP)
    pos = dict(base, cam="pan_r")
    out, code = check({"c102": pos}, use={})
    chk("陽性対照：c102 の写真をプリセットの pan_r（寄せ 0→1・寄り 1.22）で流すと鳴る", code == 2 and any("c102" in o for o in out))
    out, code = check({"c102": base}, use={})
    chk("陰性対照：c102 の本番（寄り 1.12・寄せ 0.2→0.8）は鳴らない", code == 0)
    out, code = check({"c102": dict(base, cam=None)}, use={})
    chk("陽性対照：c102 の写真を寄り 1.0 の既定の寄り（cam なし）で出すと鳴る（左右の縁が入る）", code == 2)
    out, code = check({}, use={})
    chk("陽性対照：測る対象が0件なら鳴る（空の SPEC で合格を出さない）", code == 2)
    return 0 if ok else 2


def _selftest_none():
    """🆕 2026-10-14（22本目 ⑤b-2）：名簿が空の回（SLIDE_MOUNT={}）の確かめ＝本番の束（22本目）と ss.SLIDE_NOT_MOUNT で回す"""
    import cuts.ss as ss
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(f"{'✓' if cond else '🔴'} {label}")
        ok &= bool(cond)
    nm = dict(ss.SLIDE_NOT_MOUNT)
    if not nm:
        print("・本番の SLIDE_NOT_MOUNT が空＝名簿が空の回の確かめは見本が無い（飛ばす）")
        return True
    out, code = check({}, mount={}, use={}, not_mount=nm)
    chk(f"陰性対照：本番（SLIDE_MOUNT 空・暗い帯の {len(nm)}点を決めてある）は通る", code == 0)
    drop = sorted(nm)[0]
    out, code = check({}, mount={}, use={}, not_mount={k: v for k, v in nm.items() if k != drop})
    chk(f"陽性対照：暗い帯のある {drop} を名簿から外すと鳴る（見ていない点を通さない）", code == 2 and any(drop in o for o in out))
    out, code = check({}, mount={}, use={}, not_mount=dict(nm, **{f"{ss.EP}no_such_photo.jpg": "古い名"}))
    chk("陽性対照：束に無い名が名簿に残ると鳴る（古い名簿）", code == 2)
    out, code = check({}, mount={}, use={}, not_mount={})
    chk("陽性対照：SLIDE_MOUNT も SLIDE_NOT_MOUNT も空なら鳴る（fail closed）", code == 2)
    out, code = check({}, mount={}, use={}, not_mount=nm, db={})
    chk("陽性対照：束が空なら鳴る（0点を「縁は無い」にしない）", code == 2)
    return ok


def main():
    if "--selftest" in sys.argv:
        return selftest()
    out, code = check()
    for o in out:
        print(o)
    return code


if __name__ == "__main__":
    sys.exit(main())
