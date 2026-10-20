# -*- coding: utf-8 -*-
"""make_c4path.py — 17本目 ⑤b-4：再現イラスト C4（進入の断面図＝横から）の**進入の線と時刻の位置**を、報告書の付図4「航跡概略図」
（印刷 p.109＝`ref/ep17/src/jtsb_96-5_ja_04.pdf` の 32 頁目・走査の画像＝文字の層なし）の画素から機械で読む。

■ なぜ（映像方針 17本目 §5-2＝付図4・5 はなぞってよい〈PDL1.0＝加工して作成〉・ルール §5b-74①＝描く物は1つずつ出典）
  付図4 は「横軸は距離で、縦軸は補正計算した対地高度」（図の注）。上の帯＝滑走路から 24〜12km・下の帯＝12〜0km・格子の縦線＝1km ごと・
  縦の目盛り＝0・500・1000m（上の帯に字・下の帯も同じ線）。線の形と、時刻の矢印（⇩）の位置を読む。

■ やり方（`python ref/ep17/make_c4path.py`）
  ① 格子＝帯の中で、列の暗い画素が高さの8割以上の列（縦線 13本）・行の暗い画素が幅の約4割以上の行のうち上・下・真ん中（横線＝1000・0・500m）
     🔴 上の帯の平らな進入の線（約760m）は幅の4割以上ある＝格子と取り違えない（上・下・真ん中の位置だけを格子にする）
  ② 線＝列ごとに、格子の行（±5画素）を除いた暗い画素の一番長い塊の真ん中 → 横 9画素の中央値から 25m 以上はずれる点を捨てる
  ③ 頂点のあたり（0.45〜0.70km）は線が 500m の横線に重なる＝横線のすぐ下の最初の塊の真ん中で読む（頂点は横線の下の端に接する）
  ④ 時刻の矢印＝帯のすぐ上の行の、縦に細長い暗い塊（高さ 40画素以上・幅 12〜60画素）の真ん中。順に図の字の時刻を当てる（下の TIMES）
  ⑤ 頂点＝線の一番高い点（本文 p6・p49「15分31秒 … 最高点」＝時刻は本文）。🔴 線は頂点で止める（急降下は描かない＝映像方針 §5-4）
  ⑥ 下り道（3°＝報告書 p54「3°のILS進入経路」）＝h＝tan3°×(距離＋d0) の d0 を、ゴー・レバーの前（6〜12km）の線に最小二乗で合わせる
  → `ref/ep17/c4_path.json`（元の PDF の md5・格子の画素・線〈km・m〉・時刻の位置・頂点・下り道の d0・残差）。元の PDF はリポに入れない
"""
from __future__ import annotations

import hashlib
import io
import json
import math
from pathlib import Path

import fitz
import numpy as np
from PIL import Image
from scipy import ndimage

HERE = Path(__file__).resolve().parent
SRC = HERE / "src" / "jtsb_96-5_ja_04.pdf"
OUT = HERE / "c4_path.json"
PAGE = 31                                    # 0 から数えた頁（印刷 p.109＝付図4）
DARK = 110
# 付図4 の矢印の字（世界共通の時刻）＝帯ごとに、滑走路から遠い順
TIMES = dict(up=("11:10:04", "11:11:35"),
             lo=("11:12:42", "11:12:56", "11:13:16", "11:14:05", "11:14:18", "11:14:37", "11:14:49", "11:15:03", "11:15:11",
                 "11:15:25"))
APEX_T = "11:15:31"                          # 本文 p6・p49（最高点）
KM0 = dict(up=24, lo=12)                     # 帯の左端の格子の km（上の帯の字「20」「15」・下の帯の字「10」「5」と合う）


def jst(t):
    h, m, s = (int(v) for v in t.split(":"))
    return f"{h + 9}:{m:02d}:{s:02d}"


def runs(idx, gap=2):
    out = []
    for v in idx:
        if not out or v - out[-1][-1] > gap:
            out.append([v])
        else:
            out[-1].append(v)
    return out


def main():
    raw = SRC.read_bytes()
    doc = fitz.open(stream=raw, filetype="pdf")
    A = np.asarray(Image.open(io.BytesIO(doc.extract_image(doc[PAGE].get_images()[0][0])["image"])).convert("L"))
    H, W = A.shape
    dark = A < DARK
    S = W / 900.0
    res = dict(src=str(SRC.relative_to(HERE.parent.parent)).replace("\\", "/"), md5=hashlib.md5(raw).hexdigest(), page=PAGE + 1,
               printed="p109", size=[W, H], strips={})
    allpts, times = [], {}
    for nm, (y0, y1) in dict(up=(int(255 * S), int(340 * S)), lo=(int(445 * S), int(522 * S))).items():
        rows = np.where(dark[y0:y1, :].sum(axis=1) > 0.43 * W)[0] + y0
        hl = [float(np.mean(g)) for g in runs(rows, 3)]
        top, bot = min(hl), max(hl)
        hl = [h for h in hl if min(abs(h - top), abs(h - bot), abs(h - (top + bot) / 2)) < 8]
        inner = dark[int(top) + 4:int(bot) - 3, :]
        vl = [float(np.mean(g)) for g in runs(np.where(inner.sum(axis=0) > 0.80 * inner.shape[0])[0], 3)]
        if len(vl) != 13 or len(hl) != 3:
            raise SystemExit(f"格子が読めない（{nm}：縦 {len(vl)} 本・横 {len(hl)} 本）＝止める")

        def km(x):
            for i in range(len(vl) - 1):
                if vl[i] <= x <= vl[i + 1]:
                    return KM0[nm] - i - (x - vl[i]) / (vl[i + 1] - vl[i])
            return None

        def mm(y):
            return (bot - y) / (bot - top) * 1000.0
        ban = {k for h in hl for k in range(int(h) - 5, int(h) + 6)}
        xr = int(vl[-2]) + 20                                   # 横線だけが通る列（進入の線より左＝下の帯の 0.9km あたり）
        line_lo = max(y for y in range(int(hl[1]) - 6, int(hl[1]) + 7) if dark[y, xr])
        line_hi = min(y for y in range(int(hl[1]) - 6, int(hl[1]) + 7) if dark[y, xr])
        vban = {k for v in vl for k in range(int(v) - 5, int(v) + 6)}
        pts = []
        for x in range(int(vl[0]) + 6, int(vl[-1]) - 5):
            if x in vban:
                continue
            k = km(x)
            if nm == "lo" and k < 0.70:
                # ③ 頂点のあたり＝線が 500m の横線に重なって1つの塊になる（頂点では上の端が横線に隠れる）＝線の真ん中は
                #    「横線の下にある最初の塊の下の端 − 2.5画素」（線の太さ約6画素＝重ならない列の塊の幅で確かめた）
                ys = [y for y in range(line_hi, int(bot) - 2) if dark[y, x]]
                rr = runs(ys, 1)
                if not rr:
                    continue
                r = rr[0] if rr[0][-1] > line_lo else (rr[1] if len(rr) > 1 else None)
                if r is None:
                    continue
                pts.append((k, mm(r[-1] - 2.5), x))
                continue
            ys = [y for y in range(int(top) + 2, int(bot) - 1) if dark[y, x] and y not in ban]
            if not ys:
                continue
            r = max(runs(ys), key=len)
            if len(r) > 14:
                continue
            pts.append((k, mm(float(np.mean(r))), x))
        # ② 中央値から 25m 以上はずれる点（矢印・字のかけら）を捨てる
        ms = np.array([p[1] for p in pts])
        keep = []
        for i, p in enumerate(pts):
            med = float(np.median(ms[max(0, i - 4):i + 5]))
            if abs(p[1] - med) < 25.0:
                keep.append(p)
        # ④ 時刻の矢印
        band = dark[int(top) - 95:int(top) - 12, :]
        lab, _n = ndimage.label(band)
        xs = []
        for sl in ndimage.find_objects(lab):
            h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
            if h >= 40 and 12 <= w <= 60:
                xs.append((sl[1].start + sl[1].stop) / 2)
        ks = sorted((km(x) for x in xs), reverse=True)
        if len(ks) != len(TIMES[nm]):
            raise SystemExit(f"時刻の矢印の数が字と合わない（{nm}：矢印 {len(ks)}・字 {len(TIMES[nm])}）＝止める")
        for t, k in zip(TIMES[nm], ks):
            times[jst(t)] = round(k, 3)
        res["strips"][nm] = dict(hlines=[round(v, 1) for v in hl], vlines=[round(v, 1) for v in vl], n=len(keep))
        allpts += [(k, m) for k, m, _x in keep]
    allpts.sort(key=lambda p: -p[0])
    # ⑤ 頂点（0.3〜1.0km で一番高い点）＝線はここで止める
    near = [p for p in allpts if 0.3 < p[0] < 1.0]
    top_m = max(p[1] for p in near)
    flat = [p for p in near if p[1] >= top_m - 1.5]               # 頂点は横線の下の端に接して平ら＝その真ん中
    apex = (float(np.mean([p[0] for p in flat])), float(np.mean([p[1] for p in flat])))
    allpts = [p for p in allpts if p[0] >= apex[0] - 1e-9]
    times[jst(APEX_T)] = round(apex[0], 3)
    # 0.05km おきに（その幅の点の平均）
    out, k = [], math.floor(allpts[0][0] * 20) / 20
    while k > apex[0]:
        seg = [m for kk, m in allpts if k - 0.025 < kk <= k + 0.025]
        if seg:
            out.append([round(k, 3), round(float(np.mean(seg)), 1)])
        k = round(k - 0.05, 3)
    out.append([round(apex[0], 3), round(apex[1], 1)])
    # ⑥ 下り道の d0
    tan3 = math.tan(math.radians(3.0))
    fit = [(kk, m) for kk, m in out if 6.0 <= kk <= 12.0]
    d0 = float(np.mean([m / 1000.0 / tan3 - kk for kk, m in fit]))
    resid = [m - tan3 * (kk + d0) * 1000.0 for kk, m in fit]
    res.update(pts=out, times=dict(sorted(times.items())), apex=[round(apex[0], 3), round(apex[1], 1)],
               glide=dict(deg=3.0, d0=round(d0, 3), rms=round(float(np.sqrt(np.mean(np.square(resid)))), 1),
                          rec="報告書 p54（3°のILS進入経路）・d0＝6〜12km の線に合わせた"),
               note="付図4（航跡概略図・横軸は距離・縦軸は補正計算した対地高度）を画素から読んだ。時刻は図の字＋9時間（日本の時刻）")
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{OUT.name}：線 {len(out)} 点・時刻 {len(times)}・頂点 {res['apex']}・d0 {d0:.3f}km（残差 {res['glide']['rms']}m）")
    for t, kk in res["times"].items():
        print(f"  {t}  {kk:.3f}km")


if __name__ == "__main__":
    main()
