# -*- coding: utf-8 -*-
"""ep7_shotscan.py — RG237 のショット58本の中身を**機械で**読み分ける（2026-09-13 ⑤b-1）。

■ なぜ要るか
    `footage.USE` に (start, until) を書くには「そのショットに何が写っているか」が要る。
    ⑤b は画像を読まない工程なので、**目で見ずに**次の3つを機械で採る：
      1. **焼き込まれた文字**（表題カード・凡例）… OCR（`tools/ocr_win.ps1`）
         → [[feedback-gates-dont-see-text-burned-into-the-picture]]（目視の前に OCR）
      2. **動きの大きさ** … `shots.json` の `motion`（1秒ごとの署名の距離の中央値）
      3. **絵の明るさ・色の広がり** … 真っ黒／真っ白／ほぼ単色のショットを落とす

■ 🔴 OCR は `powershell.exe`（Windows PowerShell 5.1）で回す
    この環境の `pwsh`（PowerShell 7）は WinRT を読めず、**全ページ null のまま exit 0**。
    ＝「通ったのに0行」になる（[[feedback-parsers-fail-closed]]）。

■ 使い方
    python qa_out/ep7_shotscan.py grab      # ショットの真ん中のコマを1枚ずつ切り出す
    python qa_out/ep7_shotscan.py ocr       # 切り出したコマを OCR
    python qa_out/ep7_shotscan.py report    # 表にして出す（USE を書くための材料）
    python qa_out/ep7_shotscan.py cuts      # 1ショットのクリップの「本当に切れ目が無いか」
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import footage as F                                            # noqa: E402

SHOTS = HERE / "ref" / "ep7" / "shots.json"
SCRATCH = Path(os.environ.get("EP7_SCRATCH") or (HERE / "out" / "ep7_shotscan"))
OCR_PS1 = HERE / "tools" / "ocr_win.ps1"
OUT = HERE / "qa_out" / "ep7_shotscan.json"


def shot_rows():
    d = json.loads(SHOTS.read_text(encoding="utf-8"))
    for k in sorted(d):
        for i, s in enumerate(d[k]["shots"]):
            mid = (float(s["start"]) + float(s["until"])) / 2
            yield dict(clip=k, i=i, start=s["start"], until=s["until"],
                       motion=s["motion"], mid=round(mid, 1))


def _name(r):
    return f"{r['clip'].rsplit('.', 1)[0]}__s{r['i']:02d}.png"


def cmd_grab(only=None):
    """🔴 ショットの真ん中のコマを1枚だけ。**SAR の直しを本番と同じに当てる**
    （[[feedback-gates-must-share-the-production-geometry]]）。"""
    SCRATCH.mkdir(parents=True, exist_ok=True)
    rows = [r for r in shot_rows() if not only or r["clip"] in only]
    print(f"■ ショット {len(rows)}本の真ん中のコマを切り出す → {SCRATCH}")
    ng = 0
    for n, r in enumerate(rows, 1):
        c = F.CLIPS[r["clip"]]
        dest = SCRATCH / _name(r)
        if dest.exists():
            continue
        vf = []
        if int(c.get("dispw") or c["w"]) != int(c["w"]):
            vf += ["scale=iw*sar:ih", "setsar=1"]
        cmd = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
               "-user_agent", F.UA, "-ss", f"{r['mid']:.2f}", "-i", c["url"],
               "-an", "-frames:v", "1", *(["-vf", ",".join(vf)] if vf else []),
               str(dest)]
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        if p.returncode != 0 or not dest.exists():
            print(f"  🔴 {n}/{len(rows)} {dest.name}: "
                  f"{(p.stderr or '').strip()[-140:]}", flush=True)
            ng += 1
            continue
        print(f"  ✓ {n}/{len(rows)} {dest.name}  {r['start']:.0f}〜{r['until']:.0f}秒"
              f"（真ん中 {r['mid']:.0f}）", flush=True)
    print(f"\n■ 切り出せなかった {ng}本")
    return 2 if ng else 0


def cmd_ocr():
    """🔴 `powershell.exe` で回す。`pwsh` は WinRT を読めず黙って0行になる。"""
    pngs = sorted(SCRATCH.glob("*.png"))
    if not pngs:
        print("🔴 コマが無い。まず grab"); return 2
    out = SCRATCH / "ocr.txt"
    err = SCRATCH / "ocr.err"
    # ⚠️⚠️ **`text=True, encoding="utf-8"` にしてはいけない。**
    #    `powershell.exe`（Windows PowerShell 5.1）は**コンソールの cp932** で書くので、
    #    utf-8 で読むと `UnicodeDecodeError` で落ち、**出力が丸ごと 0バイト**になる。
    #    2026-09-13 に実際に踏んだ（55枚とも「読めていない」）。
    #    → **バイトで受けて、utf-8 → cp932 の順に試す**（[[feedback-parsers-fail-closed]]）。
    def _dec(b):
        for enc in ("utf-8", "cp932", "mbcs"):
            try:
                return b.decode(enc)
            except (UnicodeDecodeError, LookupError):
                continue
        return b.decode("utf-8", errors="replace")

    # ⚠️ 一度に全部渡すと引数が長くなりすぎるので 40枚ずつ
    with out.open("w", encoding="utf-8") as fo, err.open("w", encoding="utf-8") as fe:
        for i in range(0, len(pngs), 40):
            part = pngs[i:i + 40]
            p = subprocess.run(
                ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass",
                 "-File", str(OCR_PS1), "-Files", ",".join(str(x) for x in part)],
                capture_output=True, timeout=1800)
            fo.write(_dec(p.stdout or b""))
            fe.write(_dec(p.stderr or b""))
            print(f"  …{min(i + 40, len(pngs))}/{len(pngs)}枚", flush=True)
    got = sum(1 for ln in out.read_text(encoding="utf-8").splitlines()
              if ln.startswith("##"))
    print(f"■ OCR → {out}（読めた画像 {got}/{len(pngs)}枚）")
    # 🔴 fail closed：1枚も読めていないのに 0件で通さない
    if got < len(pngs):
        print(f"🔴 {len(pngs) - got}枚が読めていない（`pwsh` で回していないか）")
        return 2
    return 0


def load_ocr():
    """{画像名: [行…]}。"""
    p = SCRATCH / "ocr.txt"
    if not p.exists():
        return {}
    d, cur = {}, None
    for ln in p.read_text(encoding="utf-8", errors="replace").splitlines():
        if ln.startswith("##"):
            cur = Path(ln.split()[1]).name
            d[cur] = []
        elif cur and ln.startswith("["):
            d[cur].append(ln.split("] ", 1)[-1])
    return d


def _stats(path):
    """明るさの中位・色の広がり・インクの割合（真っ黒／単色のショットを落とす）。"""
    from PIL import Image
    import numpy as np
    with Image.open(path) as im:
        a = np.asarray(im.convert("RGB")).astype(float)
    g = a.mean(axis=2)
    return dict(med=round(float(np.median(g)), 1),
                sd=round(float(g.std()), 1),
                ink=round(float((g < 200).mean()), 3))


def cmd_report(only=None):
    rows = [r for r in shot_rows() if not only or r["clip"] in only]
    ocr = load_ocr()
    print(f"{'クリップ':44}{'#':>3}{'始':>6}{'終':>6}{'動き':>6}"
          f"{'明':>6}{'散':>6}  焼き込まれた文字（OCR）")
    save = []
    for r in rows:
        f = SCRATCH / _name(r)
        st = _stats(f) if f.exists() else dict(med=-1, sd=-1, ink=-1)
        words = [w for w in ocr.get(_name(r), []) if len(w.strip()) >= 2]
        txt = " / ".join(words)[:110]
        print(f"{r['clip'][:42]:44}{r['i']:>3}{r['start']:>6.0f}{r['until']:>6.0f}"
              f"{r['motion']:>6.1f}{st['med']:>6.1f}{st['sd']:>6.1f}  {txt}")
        save.append(dict(**r, **st, ocr=words))
    OUT.write_text(json.dumps(save, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {OUT}（{len(save)}ショット）")
    return 0


def cmd_cuts(only=None):
    """🔴 「ショット1本」のクリップが**本当に切れ目が無い**のかを値で見る。

    `shots.boundaries()` は距離が `CUT=14` を超えた秒を境目にする。1本しか出ない
    クリップは「切れ目が無い」のか「**測れていない**」のか、件数では区別できない。
    → **最大距離**を出す。14 に遠く届かないなら切れ目が無い、という実測になる。
       → [[feedback-verify-your-own-instrument]]（件数でなく値で見る）
    """
    import numpy as np
    import shots as SH
    d = json.loads(SHOTS.read_text(encoding="utf-8"))
    one = [k for k, v in d.items() if len(v["shots"]) <= 1 and (not only or k in only)]
    print(f"■ ショットが1本のクリップ {len(one)}本（しきい値 CUT={SH.CUT}）")
    for k in sorted(one):
        sig = SH.signatures(F.CLIPS[k]["url"])
        dd = np.abs(np.diff(sig, axis=0)).mean(axis=(1, 2))
        print(f"  {k[:52]:54} 最大 {dd.max():6.2f}  9割目 {np.percentile(dd, 90):6.2f}"
              f"  中位 {np.median(dd):6.2f}  → "
              f"{'切れ目なし（実測）' if dd.max() < SH.CUT else '🔴 しきい値を超える点がある'}")
    return 0


def cmd_motion(only=None):
    """🔴🔴 「動き 0.0」が本当かを**別の解像度**で測り直す。

    `shots.signatures()` は 64×36 に縮めて署名を採る。レーダーの機影は数画素なので、
    **縮めた署名では動いていても 0.0 に見える**。＝ 件数でなく**値**で、しかも
    **別の物差し**で見る（[[feedback-verify-your-own-instrument]]）。
    ⚠️ ここで 0 に近いなら「動かない絵」＝`still=True` にすべきショット。
       5秒を超えて静止させてはいけない（[[project-jiko-rules-index]] §2）。
    """
    import numpy as np
    import shots as SH
    d = json.loads(SHOTS.read_text(encoding="utf-8"))
    keys = [k for k in sorted(d) if not only or k in only]
    keep = (SH.W, SH.H)
    print(f"{'クリップ':46}{'64x36':>9}{'320x240':>10}{'変わった画素%':>14}  判定")
    try:
        SH.W, SH.H = 320, 240
        for k in keys:
            sig = SH.signatures(F.CLIPS[k]["url"])
            dd = np.abs(np.diff(sig.astype(np.int16), axis=0))
            adj = dd.mean(axis=(1, 2))
            ch = (dd > 12).mean(axis=(1, 2)) * 100        # 12 階調を超えて変わった画素
            # 本編で使う「中の区間」だけを見る（表題カードと End of Recording を外す）
            sh = d[k]["shots"]
            mid = max(sh, key=lambda s: s["until"] - s["start"])
            a, b = int(mid["start"]), min(int(mid["until"]), len(adj))
            seg, segc = adj[a:b], ch[a:b]
            m64 = mid["motion"]
            v = float(np.median(seg)) if len(seg) else 0.0
            c = float(np.median(segc)) if len(segc) else 0.0
            verdict = ("止まっている＝still" if c < 0.3
                       else ("わずかに動く" if c < 2.0 else "動いている"))
            print(f"{k[:44]:46}{m64:>9.1f}{v:>10.2f}{c:>14.2f}  {verdict}"
                  f"（{a}〜{b}秒）")
    finally:
        SH.W, SH.H = keep
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["grab", "ocr", "report", "cuts", "motion"])
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = [x for x in a.only.split(",") if x]
    return dict(grab=cmd_grab, ocr=lambda _o: cmd_ocr(), report=cmd_report,
                cuts=cmd_cuts, motion=cmd_motion)[a.cmd](only)


if __name__ == "__main__":
    sys.exit(main())
