# -*- coding: utf-8 -*-
"""`ref/ep11/clips.json` を **ffprobe の実測から** 書き出す（手で書かない）。

11本目（チャレンジャー号）。抜いた帯の正本＝`ref/ep11/footage_map.md` §1。

■ 🔴🔴 SAR（画素の縦横比）を必ず持たせる
  12本とも格納は **720×480・SAR 8:9・DAR 4:3**（＝正方画素に直すと **640×480**）。
  **1:1 のまま拡大すると横に12.5%太ります。**`footage._cut_stream()` は SAR を見ないので、
  `sar` をここに実測で書き出し、切り出し側が `scale=iw*sar:ih,setsar=1` を当てられるようにする。
  → `ref/ep11/footage_map.md` §2-1／記憶 [[feedback-container-labels-lie-about-the-picture]]

■ ⚠️ 器の「720×480」は**絵の幅ではない**
  解説の章の帯には**青い帯で左右を埋めた額入り**が混じっていて、実効の絵は **470×479**（幅65%）
  しかないコマがある。**器を見る門番は1本も鳴らない。**使うコマごとに `measure_box.py` で測る。
  → `footage_map.md` §2-2

■ 出どころ（画面に焼く。11本目は実名を出す回なので出典も出す）
  | 鍵 | もと | 権利 |
  |---|---|---|
  | `doc_*` | NASA 記録映画「Space Shuttle Challenger Accident Investigation」44分44秒 | 実質 NASA 製作（§105）。archive.org の札は投稿者の PD マーク |
  | `usia_*` | NARA／USIA「REPORT ON THE SPACE SHUTTLE CHALLENGER ACCIDENT - KEEL, 1986」（Local ID 306-WNET-239） | **米連邦 §105**（根拠A＝強い） |

使い方:
    python ref/ep11/make_clips.py            # 書き出す
    python ref/ep11/make_clips.py --check    # 書き出さずに差分だけ見る
"""
from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
CLIPS = HERE / "ref" / "ep11" / "vid" / "clips"
OUT = HERE / "ref" / "ep11" / "clips.json"

DOC_URL = "https://archive.org/details/ChallengerAccidentandInvestigation"
USIA_URL = "https://archive.org/details/gov.archives.arc.59811"

DOC_CREDIT = "出典：NASA「Space Shuttle Challenger Accident Investigation」"
USIA_CREDIT = "出典：米国立公文書館（USIA 306-WNET-239）"

# 🔴 帯の「元の秒」＝もとの1本の中での開始秒。`footage_map.md` §1 の表がこの値の正本。
#    ⚠️ ⑤c で「抜いた版と手元の版で秒は1対1」を6点で確かめてある（同 §1）。
BANDS = {
    "crew":       dict(src="doc",  at=18,   what="乗員のバス／1:34 射点の機体（カラー）／白い部屋の頭"),
    "white":      dict(src="doc",  at=380,  what="白い部屋＝乗り込み（長い1ショットの中ほど）"),
    "launch":     dict(src="doc",  at=598,  what="点火・上昇（印の無いきれいな版）"),
    "accident":   dict(src="doc",  at=662,  what="破壊・火球・SRBの飛行・落ちる残骸（同上）"),
    "srb":        dict(src="doc",  at=993,  what="輪切りの筒を貨車で運ぶ・吊る・積む・ETの到着"),
    "rollout":    dict(src="doc",  at=1061, what="クローラ・射点へ運ぶ・空撮（焼き込み 163）"),
    "t_ice":      dict(src="doc",  at=1105, what="水受けの氷・氷の配管・通信箱・霜の梁・機首"),
    "pad":        dict(src="doc",  at=1144, what="機首 Challenger・射点の機体"),
    "smoke":      dict(src="doc",  at=1448, what="🔴 黒い煙（使えるのは 1454〜1465 の11秒だけ）"),
    "joint":      dict(src="doc",  at=1538, what="継ぎ目・Oリングの溝・金具の接写"),
    "burn":       dict(src="doc",  at=2494, what="焼けた継ぎ目・黄色い丸（debris は足りているので予備）"),
    "commission": dict(src="usia", at=55,   what="🔴 公聴会の記録映像（USIA 57分のうち、ここだけ）"),
}


def probe(path: Path) -> dict:
    """🔴 読めなければ止める（0 で埋めない）→ [[feedback-parsers-fail-closed]]。"""
    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0",
           "-show_entries",
           "stream=width,height,r_frame_rate,sample_aspect_ratio,display_aspect_ratio",
           "-show_entries", "format=duration", "-of", "json", str(path)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"🔴 ffprobe が落ちた: {path.name}\n{p.stderr[:400]}")
    j = json.loads(p.stdout)
    st = (j.get("streams") or [None])[0]
    if not st:
        raise SystemExit(f"🔴 映像の筋が読めない: {path.name}")
    for k in ("width", "height", "r_frame_rate", "sample_aspect_ratio"):
        if not st.get(k):
            raise SystemExit(f"🔴 {k} が読めない: {path.name}（fail closed）")
    dur = (j.get("format") or {}).get("duration")
    if not dur:
        raise SystemExit(f"🔴 尺が読めない: {path.name}（fail closed）")
    return dict(w=int(st["width"]), h=int(st["height"]),
                fps=round(float(Fraction(st["r_frame_rate"])), 3),
                sar=st["sample_aspect_ratio"], dar=st.get("display_aspect_ratio", ""),
                sec=round(float(dur), 3))


def main():
    if not CLIPS.is_dir():
        raise SystemExit(f"🔴 {CLIPS} が無い（`ref/ep11/grab_clips.py` で抜く）")
    out, bad = {}, []
    for name, b in sorted(BANDS.items()):
        hit = [p for p in CLIPS.iterdir() if p.stem == name]
        if not hit:
            bad.append(name)
            continue
        p = hit[0]
        m = probe(p)
        # 正方画素に直した見かけの幅（絵の比を測るときはこちら）
        sw, sh = (int(x) for x in m["sar"].split(":"))
        m["square_w"] = round(m["w"] * sw / sh)
        src = b["src"]
        out[name] = dict(
            file=f"ep11/vid/clips/{p.name}",
            url=DOC_URL if src == "doc" else USIA_URL,
            credit=DOC_CREDIT if src == "doc" else USIA_CREDIT,
            src=src,
            at=b["at"],              # もとの1本の中での開始秒
            what=b["what"],
            date="1986-01-28" if src == "doc" else "1986",
            **m)
    if bad:
        raise SystemExit(f"🔴 帯が見つからない: {bad}（fail closed）")
    if len(out) != len(BANDS):
        raise SystemExit(f"🔴 {len(out)}/{len(BANDS)} 本しか読めていない（fail closed）")

    if "--check" in sys.argv:
        old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
        print("差分あり" if old != out else "差分なし")
    else:
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"✓ {OUT} に {len(out)} 本")
    for k, v in sorted(out.items()):
        print(f"  {k:11} {v['w']}x{v['h']} SAR {v['sar']}→{v['square_w']}x{v['h']} "
              f"{v['sec']:7.2f}秒  元の{v['at']}秒〜")
    return 0


if __name__ == "__main__":
    sys.exit(main())
