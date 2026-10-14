# -*- coding: utf-8 -*-
"""22本目 映像方針：図に「色を多く」（10-13 カズヤくん）の見本を焼く＝同じ図を「いまの色」と「色を増やした版」で上下に並べる。
本番の描き手（tools/ の SVG）ではなく、相談のための手描きの見本（PIL）。色の値は tools/jiko_style.py の定数を写した＝いまの色は本番に近い。

  python -I color22.py <出力フォルダ>   → sample_map.png・sample_band.png・sample_mech.png・sample_illu.png（各 1280×1440）

色の役（色を増やした版）：米沿岸警備隊＝青・米運輸安全委員会＝緑・カナダの調べ＝紫・会社＝橙・母船＝水色・潜水艇＝白・海＝深さで濃くなる青の段・陸＝くすんだ緑。
意味の色は据え置き＝赤は破壊・欠陥／黄は数字（jiko_style の ALERT・AMBER）。
"""
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding='utf-8')
W, H = 1280, 720
FONTP = 'C:/Windows/Fonts/meiryo.ttc'
F = {s: ImageFont.truetype(FONTP, s) for s in (20, 24, 28, 34, 40)}
FB = {s: ImageFont.truetype(FONTP, s, index=1) for s in (28, 34, 40)}   # meiryo の太字

# いまの色（jiko_style の navy）
BG, BG2, GRID, LINE, LINE_DIM, TICK, INK_W = '#0f1922', '#16232e', '#22333f', '#8fb6c9', '#41606f', '#7fa0b0', '#eaf2f6'
ALERT, AMBER = '#e0503c', '#e8b33c'
# 色を増やした版の役の色
USCG, NTSB, TSB = '#4f9be0', '#5fbf8f', '#ac93d4'
COMPANY, SHIP, SUB = '#f0903c', '#7fc8e8', '#f4f6f8'
LAND, LAND_EDGE = '#5e7a4f', '#9fbf88'
SEA_TOP, SEA_DEEP = (58, 128, 176), (10, 32, 54)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def grid(d):
    d.rectangle([0, 0, W, H], fill=BG)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=GRID, width=1)


def title(d, s, sub, color=INK_W):
    d.text((40, 24), s, font=FB[34], fill=color)
    d.text((40, 70), sub, font=F[20], fill=TICK)


def tag(d, s, colored):
    d.rounded_rectangle([W - 300, 20, W - 24, 62], radius=8, fill='#2b3b47' if not colored else '#3b2f4f')
    d.text((W - 288, 26), s, font=F[24], fill=INK_W)


# ── ① 地図：セントジョンズ → 現場（c219・c304） ───────────────
NF = [(-59.4, 47.6), (-59.0, 48.5), (-58.6, 49.1), (-57.9, 49.9), (-57.4, 50.7), (-56.5, 51.6), (-55.5, 51.5), (-55.6, 50.0),
      (-54.5, 49.6), (-53.6, 49.0), (-53.0, 48.5), (-52.8, 47.8), (-52.6, 47.5), (-52.9, 46.7), (-53.6, 46.6), (-53.9, 47.4),
      (-54.2, 47.0), (-55.0, 46.9), (-55.9, 47.1), (-56.0, 47.6), (-57.5, 47.6), (-58.5, 47.6)]
NS = [(-66.0, 43.6), (-64.0, 44.6), (-61.0, 45.4), (-60.0, 46.2), (-60.5, 47.0), (-61.5, 45.9), (-63.5, 45.4), (-65.5, 44.6), (-66.2, 44.2)]
LON0, LON1, LAT0, LAT1 = -62.0, -44.0, 39.5, 52.5


def pj(lon, lat):
    x = 60 + (lon - LON0) / (LON1 - LON0) * (W - 120)
    y = 110 + (LAT1 - lat) / (LAT1 - LAT0) * (H - 150)
    return x, y


def draw_map(d, colored):
    if colored:
        for y in range(110, H - 40):                       # 海＝沖へ行くほど深い青（模式）
            t = (y - 110) / (H - 150)
            d.line([(60, y), (W - 60, y)], fill=lerp(SEA_TOP, SEA_DEEP, min(1, t * 0.9 + 0.1)))
        for k in range(4):                                  # 等深の段（模式）
            pts = [pj(-58 + k * 0.6 + i * 0.5, 45.2 - k * 1.1 - 0.15 * math.sin(i)) for i in range(26)]
            d.line(pts, fill=lerp(SEA_TOP, SEA_DEEP, 0.3 + k * 0.18), width=3)
    else:
        grid(d)
        d.rectangle([60, 110, W - 60, H - 40], outline=LINE_DIM, width=2)
    for poly in (NF, NS):
        pts = [pj(*p) for p in poly]
        d.polygon(pts, fill=LAND if colored else BG2, outline=LAND_EDGE if colored else LINE)
    sj, ti = pj(-52.71, 47.56), pj(-49.95, 41.73)
    route = SHIP if colored else INK_W
    for i in range(0, 40, 2):                               # 母船の道すじ（点線）
        a, b = i / 40, (i + 1) / 40
        d.line([(sj[0] + (ti[0] - sj[0]) * a, sj[1] + (ti[1] - sj[1]) * a), (sj[0] + (ti[0] - sj[0]) * b, sj[1] + (ti[1] - sj[1]) * b)], fill=route, width=5)
    d.ellipse([sj[0] - 9, sj[1] - 9, sj[0] + 9, sj[1] + 9], fill=INK_W, outline=BG, width=2)
    d.text((sj[0] + 16, sj[1] - 18), 'セントジョンズ（母船の港）', font=F[24], fill=INK_W)
    c = ALERT
    d.line([(ti[0] - 14, ti[1] - 14), (ti[0] + 14, ti[1] + 14)], fill=c, width=6)
    d.line([(ti[0] - 14, ti[1] + 14), (ti[0] + 14, ti[1] - 14)], fill=c, width=6)
    d.text((ti[0] + 22, ti[1] - 16), 'タイタニックの眠る海', font=F[24], fill=INK_W)
    mid = ((sj[0] + ti[0]) / 2, (sj[1] + ti[1]) / 2)
    d.text((mid[0] + 18, mid[1] - 10), '約700〜800km', font=FB[28], fill=AMBER)
    d.text((pj(-61.5, 49.6)[0], pj(-61.5, 49.6)[1]), 'ニューファンドランド島', font=F[20], fill=TICK if not colored else '#e6f0dc')
    d.text((80, H - 36), '海岸線は見本のための手描き（本番は自然地形のデータ）', font=F[20], fill=TICK)


# ── ② 時刻の帯：2段の帯（c413） ─────────────────────────────
T0, T1 = 0.0, 36.0     # 10:47:00〜10:47:36


def tx(t):
    return 230 + (t - T0) / (T1 - T0) * (W - 300)


def draw_band(d, colored):
    grid(d)
    rows = [('米沿岸警備隊', USCG, 250, [(2.0, '送った', 'send'), (9.0, '壊れた（ごろ）', 'boom'), (26.0, '受けた', 'recv')]),
            ('カナダの調べ', TSB, 450, [(26.9, '画面に出た', 'recv'), (32.3, '壊れた', 'boom')])]
    for t in range(0, 37, 4):
        x = tx(t)
        d.line([(x, 170), (x, 560)], fill=GRID if not colored else '#2a3c4a', width=2)
        d.text((x - 34, 572), '10:47:%02d' % t, font=F[20], fill=TICK)
    for name, col, y, evs in rows:
        band = col if colored else LINE_DIM
        d.rounded_rectangle([230, y - 34, W - 70, y + 34], radius=12, fill=None, outline=band, width=4)
        if colored:
            d.rounded_rectangle([232, y - 32, W - 72, y + 32], radius=12, fill=lerp((15, 25, 34), tuple(int(col[i:i + 2], 16) for i in (1, 3, 5)), 0.22))
        d.text((40, y - 20), name, font=FB[28], fill=col if colored else INK_W)
        for t, lab, kind in evs:
            x = tx(t)
            if kind == 'boom':
                fc = ALERT
            elif kind == 'send':
                fc = SUB if colored else INK_W
            else:
                fc = SHIP if colored else INK_W
            d.ellipse([x - 14, y - 14, x + 14, y + 14], fill=fc, outline=BG, width=3)
            d.text((x - 40, y - 80 if kind != 'recv' else y + 40), lab, font=F[24], fill=fc if colored else (ALERT if kind == 'boom' else INK_W))
    d.text((40, 640), '「送った」は両方とも壊れる前。「受けた」の時刻は両方で合う。「壊れた」の時刻だけが離れる', font=F[24], fill=INK_W)


# ── ③ 模式：筒の断面の5つの層（c610） ────────────────────────
def draw_mech(d, colored):
    grid(d)
    cols = ['#5aa0d8', '#4fb3a5', '#8f86d9', '#d98a5a', '#c9a46a']
    x0, x1, ytop = 200, W - 200, 160
    th = 72
    for i in range(5):
        y = ytop + (4 - i) * (th + 8)
        fill = cols[i] if colored else BG2
        d.rectangle([x0, y, x1, y + th], fill=fill, outline=LINE if not colored else '#0f1922', width=3)
        d.text((x0 - 150, y + 18), '%d枚目' % (i + 1), font=FB[28], fill=INK_W if not colored else cols[i])
    for gap in (0, 2):                                      # 分かれ目＝1と2・3と4のあいだ
        y = ytop + (4 - gap) * (th + 8) - 4
        d.line([(x0, y), (x1, y)], fill=ALERT, width=8)
        d.text((x1 + 16, y - 18), 'はがれ', font=FB[28], fill=ALERT)
    d.text((x0, ytop - 50), '外側（海）', font=F[24], fill=TICK)
    d.text((x0, ytop + 5 * (th + 8) + 4), '内側（人が乗る所）', font=F[24], fill=TICK)
    d.text((40, 640), '筒の壁を切った断面（模式）＝5つの層・分かれ目は1と2、3と4のあいだ', font=F[24], fill=INK_W)


# ── ④ 再現イラスト：台が沈む3段（c314） ──────────────────────
def lars(d, cx, top, colored, sub=True):
    frame = '#c8ccd0' if colored else LINE
    float_c = '#eef2f4' if colored else INK_W
    d.rectangle([cx - 120, top, cx + 120, top + 18], fill=frame)
    for k in (-100, 100):
        d.rounded_rectangle([cx + k - 22, top - 34, cx + k + 22, top + 2], radius=10, fill=float_c, outline=BG, width=2)
    if sub:
        d.rounded_rectangle([cx - 80, top - 46, cx + 70, top - 4], radius=20, fill=SUB if colored else BG2, outline=LINE if not colored else '#9aa6ae', width=3)
        d.ellipse([cx + 54, top - 44, cx + 92, top - 6], fill='#2a3a46' if colored else BG2, outline=LINE, width=3)


def draw_illu(d, colored):
    if colored:
        d.rectangle([0, 0, W, 300], fill='#9cc3dc')
        for y in range(300, H):
            d.line([(0, y), (W, y)], fill=lerp(SEA_TOP, SEA_DEEP, (y - 300) / (H - 300)))
        d.rectangle([60, 236, 300, 296], fill='#2f5d9a')           # 母船（青い船体）
        d.rectangle([150, 196, 230, 236], fill='#eef2f4')
        d.line([(250, 236), (300, 170)], fill='#f0903c', width=8)  # 橙の起重機
    else:
        grid(d)
        d.line([(0, 300), (W, 300)], fill=LINE, width=3)
        d.rectangle([60, 236, 300, 296], outline=LINE, width=3)
    labels = ['① 浮きに水を入れる', '② 台ごと水面の下へ', '③ 潜水艇を切り離す']
    for i, cx in enumerate((470, 780, 1090)):
        top = (300 if i == 0 else 420)
        lars(d, cx, top, colored, sub=(i < 2))
        if i == 2:
            d.rounded_rectangle([cx - 80, 520, cx + 70, 562], radius=20, fill=SUB if colored else BG2, outline=LINE if not colored else '#9aa6ae', width=3)
            d.line([(cx, 570), (cx, 626)], fill=AMBER if colored else LINE, width=5)
            d.polygon([(cx - 14, 620), (cx + 14, 620), (cx, 644)], fill=AMBER if colored else LINE)
        d.text((cx - 120, 676), labels[i], font=F[24], fill=INK_W)


def main(out):
    os.makedirs(out, exist_ok=True)
    jobs = [('map', draw_map, '地図（c219・c304 の型）', '母船の港から現場まで'),
            ('band', draw_band, '時刻の帯（c413 の型）', '2つの調べの「送った・受けた・壊れた」'),
            ('mech', draw_mech, '模式図（c610 の型）', '筒の断面の5つの層'),
            ('illu', draw_illu, '再現イラスト（c314 の型）', '台が沈んで潜水艇を出す3段')]
    for key, fn, ttl, sub in jobs:
        sheet = Image.new('RGB', (W, H * 2 + 8), '#000000')
        for k, colored in enumerate((False, True)):
            im = Image.new('RGB', (W, H), BG)
            d = ImageDraw.Draw(im)
            fn(d, colored)
            title(d, ttl, sub)
            tag(d, '色を増やした版' if colored else 'いまの色（navy）', colored)
            sheet.paste(im, (0, k * (H + 8)))
        p = os.path.join(out, 'sample_%s.png' % key)
        sheet.save(p)
        print(p)


if __name__ == '__main__':
    main(sys.argv[1])
