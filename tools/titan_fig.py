# -*- coding: utf-8 -*-
"""タイタン号の図解テンプレート。226カットをこの部品で組む。

■ なぜテンプレートにするか
  カットごとに手描きの関数を書くと、34分＝226カットで1万行を超え、
  **カットごとに見た目がばらつく**。34分の動画でいちばん効くのは
  「同じ意味の情報がいつも同じ形で出る」ことなので、型を先に決めて中身を差し替える。

■ 全カット共通の約束（[[事故検証-テスト映像-余白を詰めた記録-20260730]] §3 の型）
  枠   … MG=72 / RIGHT=1848 / BAND_T=210 / BAND_B=892
  見出し … 左上（J.title）。右上に章マーカー（J.chapter）
  字幕 … y=900 以下。**ここには何も置かない**
  級数 … **推定しない。** fontmetrics で実測して収める（fm.fit / fm.width / fm.ink）

■ 1つの図が返すもの（Fig）
  lab    … 図の骨格。カット頭から**左→右へワイプで現れる**（＝「描かれていく」）
  stages … ナレーションの行に同期して足される段。build_jiko の `_aN` になる
  hot    … 脈打たせる強調（省略可）。図が早く描き終わるカットの動きを埋める
  span   … ワイプを進める x 範囲。**図が実際に占める幅**を返す
           （全幅にするとワイプの travel が空白に費やされて図が動き出すのが遅れる。
             これはテスト映像の11巡目に実際に起きた）

■ 図に書いてよいこと・いけないこと
  🔴 **ナレーションで話している文をそのまま図に書かない。**
     図が持つのは「数値・部位名・単位・関係」。文はナレーションと字幕が持つ。
     テスト映像では c3 に「円周の約55%」と書いてナレーションと重複した（違反1件）。
"""
import math

import jiko_style as J
import fontmetrics as fm

W, H = 1920, 1080
BX0, BX1 = J.MG, J.RIGHT              # 本体の左右 72 / 1848
BY0, BY1 = J.BAND_T, J.BAND_B         # 本体の上下 210 / 892
BW, BH = BX1 - BX0, BY1 - BY0         # 1776 × 682
BCX = (BX0 + BX1) / 2                 # 960

_uid = [0]


def uid(p="g"):
    _uid[0] += 1
    return f"{p}{_uid[0]}"


class Fig:
    """図1枚ぶん。build 側はこの4つしか見ない。"""

    def __init__(self, lab, stages=None, hot="", span=None):
        self.lab = lab
        self.stages = [s for s in (stages or []) if s]
        self.hot = hot
        self.span = span or (BX0, BX1)


# ── 文字の置き方（すべて実測で収める） ─────────────────────
XML = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def esc(t):
    return "".join(XML.get(c, c) for c in str(t))


def txt(x, y, t, size=32, col=None, fam="Noto", anchor="start", ol=0):
    """1行。`ol` にフチの太さを渡すと写真や図の上でも読める。"""
    o = ""
    if ol:
        o = (f' stroke="{J.BG}" stroke-width="{ol}" stroke-linejoin="round"'
             f' paint-order="stroke fill"')
    return (f'<text x="{x:.0f}" y="{y:.0f}" font-family="{fam}" font-size="{size:.0f}" '
            f'fill="{col or J.LINE}" text-anchor="{anchor}"{o}>{esc(t)}</text>')


def txtfit(x, y, t, maxw, cap=40, col=None, fam="Noto", anchor="start", ol=0, floor=16):
    """**その幅に必ず収める。** 級数を先に決めて祈らない（それで2回事故っている）。"""
    return txt(x, y, t, fm.fit(str(t), maxw, fam, cap=cap, floor=floor), col, fam,
               anchor, ol)


def wrap(t, cols):
    """全角換算 cols 字で折る。読点・句点を優先して折る。"""
    t = str(t)
    out, line, n = [], "", 0.0
    for i, ch in enumerate(t):
        line += ch
        n += fm.adv(ch, "Noto")
        brk = ch in "、。）」"
        if n >= cols or (brk and n >= cols * 0.55):
            out.append(line)
            line, n = "", 0.0
    if line:
        out.append(line)
    return out


def para(x, y, t, cols=28, size=34, col=None, lh=1.5, anchor="start", ol=0, fam="Noto"):
    """折り返す本文。戻り値は (svg, 最終行のベースライン y)。"""
    g = []
    yy = y
    for ln in wrap(t, cols):
        g.append(txt(x, yy, ln, size, col, fam, anchor, ol))
        yy += size * lh
    return "".join(g), yy - size * lh


def rect(x, y, w, h, fill="none", stroke=None, sw=4, rx=0, op=None):
    o = f' opacity="{op}"' if op is not None else ""
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{max(0, w):.0f}" '
            f'height="{max(0, h):.0f}" rx="{rx}" fill="{fill}"{s}{o}/>')


def line(x1, y1, x2, y2, col=None, sw=None, dash=None, op=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<path d="M{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f}" stroke="{col or J.LINE}" '
            f'stroke-width="{sw or J.LW}"{d}{o} fill="none"/>')


def poly(pts, fill="none", stroke=None, sw=None, close=False, dash=None, op=None):
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + (" Z" if close else "")
    s = f' stroke="{stroke}" stroke-width="{sw or J.LW}"' if stroke else ""
    da = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{op}"' if op is not None else ""
    return (f'<path d="{d}" fill="{fill}"{s}{da}{o} stroke-linejoin="round" '
            f'stroke-linecap="round"/>')


def circ(cx, cy, r, fill="none", stroke=None, sw=None, op=None):
    s = f' stroke="{stroke}" stroke-width="{sw or J.LW}"' if stroke else ""
    o = f' opacity="{op}"' if op is not None else ""
    return f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}" fill="{fill}"{s}{o}/>'


def arrow(x1, y1, x2, y2, col=None, sw=None, head=18):
    """矢印。角度をちゃんと計算する（水平専用にすると工程図で使えない）。"""
    c = col or J.LINE
    a = math.atan2(y2 - y1, x2 - x1)
    p = [(x2, y2),
         (x2 - head * math.cos(a - 0.42), y2 - head * math.sin(a - 0.42)),
         (x2 - head * math.cos(a + 0.42), y2 - head * math.sin(a + 0.42))]
    return (line(x1, y1, x2 - head * 0.6 * math.cos(a), y2 - head * 0.6 * math.sin(a),
                 c, sw or J.LW)
            + poly(p, fill=c, close=True))


def chip(x, y, t, col=None, size=28, pad=16, h=None, fill=None, anchor="start"):
    """小さな見出し札。**幅は実測**なので文字がはみ出さない。"""
    c = col or J.LINE
    w = fm.width(str(t), size, "Noto") + pad * 2
    hh = h or size + 20
    x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x)
    return (rect(x0, y, w, hh, fill or "none", c, 3, rx=6)
            + txt(x0 + pad, y + hh - (hh - size * 0.72) / 2, t, size, c))


def capline(x, y, w, t, col=None, size=26):
    """図の下に置く小見出し（罫＋文字）。"""
    c = col or J.LINE_DIM
    return line(x, y, x + w, y, c, 3) + txt(x, y + size + 12, t, size, col or J.LINE)


def num(x, y, v, unit="", cap="", col=None, size=104, anchor="middle", capsize=28):
    """大きな数字1つ。単位は数字より小さく、**同じ行のうしろ**に置く。

    🔴 テスト映像で「196pxの数字＋51pxのDelaの『回』」が豆腐の箱に見えた。
       単位は Dela で大きく打たない。Noto で数字の 0.34 倍・ベースライン揃え。
    """
    c = col or J.AMBER
    nw = fm.width(str(v), size, "Dela")
    us = size * 0.34
    uw = fm.width(unit, us, "Noto") + (size * 0.10 if unit else 0)
    tot = nw + uw
    x0 = x - tot / 2 if anchor == "middle" else (x - tot if anchor == "end" else x)
    g = [txt(x0, y, v, size, c, "Dela")]
    if unit:
        g.append(txt(x0 + nw + size * 0.10, y, unit, us, c))
    if cap:
        g.append(txtfit(x0 + tot / 2, y + capsize + 22, cap, tot + 260, cap=capsize,
                        col=J.LINE, anchor="middle"))
    return "".join(g)


def hatch(x, y, w, h, col=None, gap=18, op=0.5):
    """斜線の網掛け。「無い」「調べていない」領域を示す。"""
    c = col or J.LINE_DIM
    gid = uid("h")
    return (f'<pattern id="{gid}" width="{gap}" height="{gap}" '
            f'patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<path d="M0 0 V{gap}" stroke="{c}" stroke-width="3"/></pattern>'
            + rect(x, y, w, h, f"url(#{gid})", op=op))


def watertone(x, y, w, h, top_op=0.10, bot_op=0.42):
    """海。上が薄く下が濃い。深さを面で感じさせる。"""
    gid = uid("w")
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{J.LINE}" stop-opacity="{top_op}"/>'
            f'<stop offset="1" stop-color="{J.LINE}" stop-opacity="{bot_op}"/>'
            f'</linearGradient>' + rect(x, y, w, h, f"url(#{gid})"))


# ══════════════════════════════════════════════════════════
#  1. depth — 深度目盛り
# ══════════════════════════════════════════════════════════
def depth(marks, dmax=4400, unit="m", axis_t="水深", seabed=None, note="", right=True):
    """海面から下へ伸びる深度目盛り。**この動画でいちばん多く使う図。**

    marks … [dict(d=3346, t="爆縮", c=J.ALERT, big=True, sub="10:47:09")]
    dmax  … 目盛りの下限。**カットごとに変えない**（比較できなくなる）
    """
    ax = BX0 + 250                       # 目盛り軸の x
    # ⚠️ 注記を出すカットは、目盛りの底を上げて**注記の場所を空ける**。
    #    空けないと、目盛りの数字（4,000）や印のラベルと必ず重なる。
    top = BY0 + 54
    bot = BY1 - (78 if note else 34)     # 海面 / 目盛りの底
    span = bot - top

    def dy(d):
        return top + span * min(1.0, d / dmax)

    g = [watertone(BX0, top, BX1 - BX0, bot - top)]
    # 海面
    g.append(line(BX0, top, BX1, top, J.INK_W, 5))
    g.append(txt(BX0 + 8, top - 18, "海面", 30, J.INK_W))
    # 目盛り軸
    g.append(line(ax, top, ax, bot, J.LINE_DIM, 3))
    stepm = 1000 if dmax > 2500 else 500
    d = stepm
    while d <= dmax:
        y = dy(d)
        g.append(line(ax - 16, y, ax + 16, y, J.LINE_DIM, 3))
        g.append(txt(ax - 28, y + 11, f"{d:,}", 26, J.LINE_DIM, "Noto", "end"))
        d += stepm
    g.append(txt(ax - 28, top + 28, axis_t, 26, J.LINE_DIM, "Noto", "end"))
    if seabed is not None:
        y = dy(seabed)
        g.append(poly([(BX0, y)] + [(BX0 + i * 74, y + (12 if i % 2 else -6))
                                    for i in range(1, 25)], stroke=J.LINE_DIM, sw=4))
        g.append(txt(BX1, y + 40, "海底", 28, J.LINE_DIM, "Noto", "end"))
    if note:
        # ⚠️ 右下に置くと「海底」ラベル（同じく右下）と必ず重なる。
        #    seabed を渡すカットは全部これに当たった（c113a c114 c115b c121 c130）。
        g.append(txtfit(BX0, BY1 - 6, note, BW - 300, cap=28, col=J.LINE_DIM))

    stages = []
    for m in marks:
        y = dy(m["d"])
        c = m.get("c", J.AMBER)
        big = m.get("big", False)
        s = [line(ax, y, BX1 - 8, y, c, 6 if big else 4,
                  dash=None if big else "14 10")]
        s.append(circ(ax, y, 11 if big else 8, c))
        size = 76 if big else 48
        lx = ax + 40
        s.append(txt(lx, y - 16, f'{m["d"]:,}', size, c, "Dela"))
        nw = fm.width(f'{m["d"]:,}', size, "Dela")
        s.append(txt(lx + nw + 10, y - 16, unit, size * 0.36, c))
        if m.get("t"):
            s.append(txtfit(lx, y + (44 if big else 34), m["t"], BX1 - lx - 20,
                            cap=40 if big else 32, col=c))
        if m.get("sub"):
            s.append(txtfit(BX1, y - 16, m["sub"], 620, cap=34, col=J.LINE_DIM,
                            anchor="end"))
        stages.append("".join(s))
    hot = ""
    for m in marks:
        if m.get("hot"):
            y = dy(m["d"])
            hot = circ(ax, y, 26, "none", m.get("c", J.ALERT), 5)
    return Fig("".join(g), stages, hot, (BX0, BX1))


# ══════════════════════════════════════════════════════════
#  2. compare — 数値をならべて比べる
# ══════════════════════════════════════════════════════════
def compare(items, unit="", note="", bar=True, ratio=""):
    """2〜4個の数値を、棒の長さで比べる。

    items … [dict(v=13200, t="計算が示した爆縮深度", c=J.LINE, disp="13,200")]
    """
    n = len(items)
    gap = 40
    cw = (BW - gap * (n - 1)) / n
    vmax = max(abs(i["v"]) for i in items) or 1
    top = BY0 + 34
    # ⚠️ 棒の高さ300では枠を使い切れず、値の小さい側の柱が空だった（c202 35.7%）。
    #    数字の下から枠の底まで使う。比の小さい棒も**最低限の高さ**を持たせて
    #    「柱がそこにある」ことは見せる（0.8pxの棒は消えているのと同じ）。
    # 比の一行を出すカットは、その場所も先に空けておく（あとから足すと必ずはみ出す）
    barb = BY1 - (108 if ratio else (74 if note else 34))   # 棒の底
    barh = barb - (top + 250)
    g = []
    stages = []
    for i, it in enumerate(items):
        x = BX0 + i * (cw + gap)
        c = it.get("c", J.LINE)
        disp = it.get("disp") or f'{it["v"]:,}'
        u = it.get("unit", unit)
        s = []
        if not bar:
            # 棒を描かないカットは、代わりに枠いっぱいの面で柱を立てる。
            # 何も置かないと下半分が丸ごと空く（c208 空き45.7%）。
            s.append(rect(x + cw * 0.08, top + 230, cw * 0.84, barb - top - 230,
                          c, op=0.16))
            s.append(rect(x + cw * 0.08, top + 230, cw * 0.84, barb - top - 230,
                          "none", c, 4))
        if bar:
            h = max(barh * 0.045, barh * abs(it["v"]) / vmax)
            s.append(rect(x + cw * 0.16, barb - h, cw * 0.68, h, c, op=0.30))
            s.append(rect(x + cw * 0.16, barb - h, cw * 0.68, h, "none", c, 4))
            s.append(line(x + cw * 0.16, barb, x + cw * 0.84, barb, c, 5))
        ns = fm.fit(disp, cw * 0.86, "Dela", cap=112, floor=40)
        s.append(num(x + cw / 2, top + 118, disp, u, "", c, ns))
        s.append(txtfit(x + cw / 2, top + 176, it["t"], cw * 0.98, cap=34,
                        col=J.LINE, anchor="middle"))
        if it.get("sub"):
            s.append(txtfit(x + cw / 2, top + 218, it["sub"], cw * 0.98, cap=28,
                            col=J.LINE_DIM, anchor="middle"))
        stages.append("".join(s))
        g.append(line(x + cw * 0.16, barb, x + cw * 0.84, barb, J.LINE_DIM, 3))
    # ⚠️ ratio と note を同じ y に置いていたので、両方あるカットで必ず重なった（c115d）。
    #    ratio は棒のすぐ下、note はいちばん下に離す。
    if ratio and n >= 2:
        g.append(txtfit(BCX, barb + 56, ratio, BW * 0.8, cap=44, col=J.AMBER,
                        anchor="middle"))
    if note:
        g.append(txtfit(BX0, BY1 - 16, note, BW, cap=28, col=J.LINE_DIM))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
#  3. quote — 引用
# ══════════════════════════════════════════════════════════
def quote(phrase, who="", when="", doc="", ctx="", to="", size=104):
    """引用カット。**この動画には引用が20カットある。作りを間違えると全部死ぬ。**

    🔴 引用の言葉そのものは、**ナレーションが読み上げ、字幕にも出ている。**
       それを図にも大きく書くと、同じ文が「音・字幕・図」で三重になる。
       画面が持つべきなのは、字幕が持てないもの＝**その言葉の出どころ**である。
         誰が（who）／誰に（to）／いつ（when）／何に書かれていたか（doc）
       図に出す言葉は**短い決め所だけ**（`phrase`）にして、文は字幕に任せる。

    ⚠️ `phrase` が長いと結局は字幕の複写になる。20字を超えたら短くする。
    """
    g = []
    # 出どころの札（文書 or 会話）を左に立てる
    card_x, card_y, card_w = BX0 + 20, BY0 + 30, 470
    card_h = BH - 70
    g.append(rect(card_x, card_y, card_w, card_h, J.BG2, op=0.72))
    g.append(rect(card_x, card_y, card_w, card_h, "none", J.LINE_DIM, 3))
    # 書類の角折れ。会話（doc なし）のときは吹き出しの尻尾にする
    if doc:
        g.append(poly([(card_x + card_w - 74, card_y), (card_x + card_w, card_y + 74),
                       (card_x + card_w - 74, card_y + 74)], fill=J.LINE_DIM,
                      close=True, op=0.6))
    else:
        g.append(poly([(card_x + card_w, card_y + card_h * 0.42),
                       (card_x + card_w + 46, card_y + card_h * 0.50),
                       (card_x + card_w, card_y + card_h * 0.58)], fill=J.BG2,
                      close=True))
    y = card_y + 88
    for lb, v, c in (("誰が", who, J.INK_W), ("誰に", to, J.LINE),
                     ("いつ", when, J.LINE), ("どこに", doc, J.LINE)):
        if not v:
            continue
        g.append(txt(card_x + 30, y, lb, 24, J.LINE_DIM))
        body, y2 = para(card_x + 30, y + 44, v, cols=int((card_w - 60) / 32), size=32,
                        col=c)
        g.append(body)
        y = y2 + 62
    if ctx:
        g.append(line(card_x + 30, y - 24, card_x + card_w - 30, y - 24, J.LINE_DIM, 2))
        body, _ = para(card_x + 30, y + 16, ctx, cols=int((card_w - 60) / 26), size=26,
                       col=J.LINE_DIM)
        g.append(body)
    # 右に決め所。**短い言葉だけ**
    px0 = card_x + card_w + 70
    pw = BX1 - px0
    g.append(txt(px0, BY0 + 150, "「", 120, J.ALERT_DIM, "Noto"))
    g.append(txt(BX1 - 46, BY1 - 40, "」", 120, J.ALERT_DIM, "Noto", "end"))
    lines = wrap(phrase, 10) if isinstance(phrase, str) else list(phrase)
    # 決め所は**枠の縦を使い切る大きさ**にする。1行なら大きく、行数が増えたら詰める
    size = min(size, int((BH - 150) / max(1, len(lines)) / 1.34))
    lh = size * 1.34
    top = BY0 + (BH - len(lines) * lh) / 2 + size * 0.72
    stages = []
    for i, ln in enumerate(lines):
        stages.append(txtfit(px0 + 78, top + i * lh, ln, pw - 130, cap=size,
                             col=J.INK_W))
    return Fig("".join(g), stages,
               rect(card_x, card_y, 9, card_h, J.ALERT), (px0, BX1))


# ══════════════════════════════════════════════════════════
#  4. timeline — 横の時間軸
# ══════════════════════════════════════════════════════════
def timeline(events, t0, t1, ticks=None, tfmt=None, title="", band=None):
    """横に伸びる時間軸。events=[dict(t=..., top="10:47", t2="重り2つ", c=...)]

    t は t0..t1 と同じ単位（分でも時間でも秒でもよい）。
    """
    # ⚠️ 軸を BY0+330 に固定していたので下が空いた（c120 c122 c124 ほか15カット）。
    #    枠の縦中央に置き、旗の高さを伸ばして上下を使い切る。
    # 0.50 だと下向きの旗の t2 が字幕帯（906）に食い込む（実測で5件出た）。
    ax = BY0 + BH * 0.45
    x0, x1 = BX0 + 60, BX1 - 60
    sp = max(1e-6, t1 - t0)

    def tx(t):
        return x0 + (x1 - x0) * (t - t0) / sp

    g = []
    if band:
        for b in band:
            g.append(rect(tx(b["a"]), ax - 250, tx(b["b"]) - tx(b["a"]), 500,
                          b.get("c", J.ALERT), op=b.get("op", 0.16)))
            if b.get("t"):
                g.append(txtfit((tx(b["a"]) + tx(b["b"])) / 2, ax - 268, b["t"],
                                max(180, tx(b["b"]) - tx(b["a"]) + 260), cap=30,
                                col=b.get("c", J.ALERT), anchor="middle"))
    g.append(line(x0, ax, x1, ax, J.LINE, 5))
    g.append(arrow(x1 - 4, ax, x1 + 34, ax, J.LINE, 5))
    for t in (ticks or []):
        x = tx(t if not isinstance(t, (list, tuple)) else t[0])
        lb = tfmt(t) if tfmt else (t[1] if isinstance(t, (list, tuple)) else f"{t}")
        g.append(line(x, ax - 12, x, ax + 12, J.LINE_DIM, 3))
        g.append(txt(x, ax + 46, lb, 26, J.LINE_DIM, "Noto", "middle"))
    if title:
        g.append(txtfit(BX0, BY1 - 8, title, BW, cap=30, col=J.LINE_DIM))
    stages = []
    up = True
    for e in events:
        x = tx(e["t"])
        c = e.get("c", J.AMBER)
        big = e.get("big", False)
        dy = -1 if e.get("up", up) else 1
        up = not up
        # ⚠️ 旗の高さは**上と下で許される長さが違う**。
        #    上は見出しの副題（字面の下端 190）に、下は字幕帯（906）にぶつかる。
        #    伸ばしすぎて実測で9件ぶつけたので、軸からの余地で頭打ちにする。
        stem = 196 if not big else 268
        stem = min(stem, (ax - BY0 - 96) if dy < 0 else (874 - ax))
        s = [line(x, ax, x, ax + dy * stem, c, 5 if big else 4),
             circ(x, ax, 12 if big else 8, c)]
        ty = ax + dy * (stem + 12)
        anch = "middle"
        w = 420 if big else 320
        if x - w / 2 < BX0:
            anch, tx0 = "start", x - 20
        elif x + w / 2 > BX1:
            anch, tx0 = "end", x + 20
        else:
            tx0 = x
        s.append(txtfit(tx0, ty + (0 if dy < 0 else 34), e.get("top", ""), w,
                        cap=52 if big else 40, col=c, anchor=anch, fam="Dela"))
        if e.get("t2"):
            s.append(txtfit(tx0, ty + (dy < 0 and -44 or 78), e["t2"], w,
                            cap=32, col=J.LINE, anchor=anch))
        stages.append("".join(s))
    return Fig("".join(g), stages, "", (x0 - 40, x1 + 40))


# ══════════════════════════════════════════════════════════
#  5. moment — 時刻を主役にする（第1章の骨）
# ══════════════════════════════════════════════════════════
def moment(clock, label="", facts=None, day=None, dayspan=None, sub=""):
    """大きな時刻＋その時の事実。第1章は時計が主役なので専用の型にする。

    day/dayspan を渡すと、下に「その日のどこか」を示す細い帯が出る。
    """
    facts = facts or []
    # ⚠️ 時計を上に寄せていたので、その下 y520〜800 が丸ごと空いた（10カット全部）。
    #    時計を大きくして枠の縦中央へ置き、下に太い罫を渡して面を作る。
    cy = BY0 + 300
    g = []
    cs = fm.fit(clock, BW * 0.54, "Dela", cap=232, floor=60)
    g.append(txt(BX0 + 20, cy, clock, cs, J.INK_W, "Dela"))
    g.append(line(BX0 + 20, cy + 46, BX0 + BW * 0.52, cy + 46, J.ALERT, 8))
    if label:
        g.append(txtfit(BX0 + 20, cy + 118, label, BW * 0.52, cap=46, col=J.AMBER))
    if sub:
        g.append(txtfit(BX0 + 20, cy + 176, sub, BW * 0.52, cap=32, col=J.LINE_DIM))
    # 右に事実を積む
    stages = []
    fx = BX0 + BW * 0.58
    # 右の柱も縦を使い切る。件数に応じて開始位置と間隔を決める
    nf = max(1, len(facts))
    fspan = (BY1 - 120) - (BY0 + 90)
    fstep = max(120, fspan / nf)
    fy = BY0 + 96
    for i, f in enumerate(facts):
        s = [line(fx, fy - 34, fx, fy + 42, J.ALERT, 5)]
        s.append(txtfit(fx + 26, fy, f.get("t", ""), BX1 - fx - 50, cap=40,
                        col=J.INK_W))
        if f.get("v"):
            # 62 だと大きな値（Dela 76px）の字面が上の見出しに 7px 食い込む（実測）
            s.append(txt(fx + 26, fy + 82, f["v"],
                         fm.fit(f["v"], BX1 - fx - 60, "Dela", cap=76, floor=30),
                         f.get("c", J.AMBER), "Dela"))
        fy += fstep
        stages.append("".join(s))
    if day and dayspan:
        y = BY1 - 40
        a, b = dayspan
        g.append(line(BX0 + 20, y, BX1 - 20, y, J.LINE_DIM, 4))
        for h in range(int(a), int(b) + 1, 2):
            x = BX0 + 20 + (BX1 - BX0 - 40) * (h - a) / max(1e-6, b - a)
            g.append(line(x, y - 8, x, y + 8, J.LINE_DIM, 3))
            g.append(txt(x, y + 38, f"{h}時", 22, J.LINE_DIM, "Noto", "middle"))
        x = BX0 + 20 + (BX1 - BX0 - 40) * (day - a) / max(1e-6, b - a)
        g.append(circ(x, y, 13, J.ALERT))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
#  6. breakdown — 全体を分ける
# ══════════════════════════════════════════════════════════
def breakdown(total, parts, unit="人", note="", horizontal=True):
    """total を parts に分ける積み上げ棒＋内訳。

    parts … [dict(v=17, t="船の乗組員", c=...)]
    """
    tot = total or sum(p["v"] for p in parts)
    y = BY0 + 96
    bh = 168
    g = [num(BX0 + 10, y - 20, f"{tot:,}", unit, "", J.INK_W, 96, "start")]
    g.append(line(BX0, y + 44, BX1, y + 44, J.LINE_DIM, 3))
    stages = []
    x = BX0
    ly = y + 288
    lstep = max(60, (BY1 - 30 - ly) / max(1, len(parts)))
    for i, p in enumerate(parts):
        w = BW * p["v"] / max(1, tot)
        c = p.get("c", J.LINE)
        s = [rect(x, y + 62, w, bh, c, op=0.32), rect(x, y + 62, w, bh, "none", c, 4)]
        vs = fm.fit(str(p["v"]), w * 0.7, "Dela", cap=64, floor=22)
        s.append(txt(x + w / 2, y + 62 + bh / 2 + vs * 0.36, p["v"], vs, c, "Dela",
                     "middle"))
        # 内訳の行（棒の下に縦に積む）
        s.append(rect(BX0, ly - 36, 44, 44, c, op=0.32))
        s.append(rect(BX0, ly - 36, 44, 44, "none", c, 3))
        s.append(txtfit(BX0 + 64, ly, p["t"], BW - 400, cap=46, col=J.INK_W))
        s.append(txt(BX1, ly, f'{p["v"]}{unit}', 54, c, "Dela", "end"))
        s.append(line(BX0, ly + 18, BX1, ly + 18, J.LINE_DIM, 2))
        stages.append("".join(s))
        x += w
        ly += lstep
    if note:
        g.append(txtfit(BX0, BY1 - 8, note, BW, cap=26, col=J.LINE_DIM))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
#  7. graph — XY 折れ線（第5章の核心）
# ══════════════════════════════════════════════════════════
def graph(series, xlab="", ylab="", xticks=None, yticks=None, xr=(0, 1), yr=(0, 1),
          note="", legend=True, marks=None, band=None):
    """折れ線グラフ。**左から描かれていく**のがこの動画の主要な動きになる。

    series … [dict(pts=[(x,y),...], t="ダイブ80", c=..., dash=None, sw=None)]
    """
    gx0, gx1 = BX0 + 150, BX1 - 40
    gy0, gy1 = BY0 + 46, BY1 - 96
    x0, x1 = xr
    y0, y1 = yr

    def px(v):
        return gx0 + (gx1 - gx0) * (v - x0) / max(1e-9, x1 - x0)

    def py(v):
        return gy1 - (gy1 - gy0) * (v - y0) / max(1e-9, y1 - y0)

    g = [rect(gx0, gy0, gx1 - gx0, gy1 - gy0, J.BG2, op=0.55)]
    for t in (xticks or []):
        v, lb = t if isinstance(t, (list, tuple)) else (t, f"{t:,}")
        g.append(line(px(v), gy0, px(v), gy1, J.GRID, 2))
        g.append(txt(px(v), gy1 + 40, lb, 26, J.LINE_DIM, "Noto", "middle"))
    for t in (yticks or []):
        v, lb = t if isinstance(t, (list, tuple)) else (t, f"{t:,}")
        g.append(line(gx0, py(v), gx1, py(v), J.GRID, 2))
        g.append(txt(gx0 - 18, py(v) + 10, lb, 26, J.LINE_DIM, "Noto", "end"))
    for b in (band or []):
        g.append(rect(px(b["a"]), gy0, px(b["b"]) - px(b["a"]), gy1 - gy0,
                      b.get("c", J.ALERT), op=b.get("op", 0.14)))
        if b.get("t"):
            g.append(txtfit((px(b["a"]) + px(b["b"])) / 2, gy0 + 40, b["t"],
                            max(200, px(b["b"]) - px(b["a"]) + 200), cap=30,
                            col=b.get("c", J.ALERT), anchor="middle"))
    g.append(rect(gx0, gy0, gx1 - gx0, gy1 - gy0, "none", J.LINE, 4))
    if xlab:
        g.append(txt(gx1, gy1 + 78, xlab, 30, J.LINE, "Noto", "end"))
    if ylab:
        g.append(txt(gx0 - 18, gy0 - 16, ylab, 30, J.LINE, "Noto", "end"))
    if note:
        g.append(txtfit(BX0, BY1 - 8, note, BW, cap=26, col=J.LINE_DIM))

    stages = []
    ly = gy0 + 44
    for s in series:
        c = s.get("c", J.LINE)
        pts = [(px(a), py(b)) for a, b in s["pts"]]
        seg = [poly(pts, stroke=c, sw=s.get("sw", 6), dash=s.get("dash"))]
        if s.get("dot"):
            seg += [circ(x, y, 7, c) for x, y in pts]
        if legend and s.get("t"):
            lx = gx1 - 24
            seg.append(line(lx - 74, ly - 10, lx - 24, ly - 10, c, 6,
                            dash=s.get("dash")))
            seg.append(txtfit(lx - 88, ly, s["t"], 460, cap=30, col=c, anchor="end"))
            ly += 44
        stages.append("".join(seg))
    for m in (marks or []):
        stages.append(circ(px(m["x"]), py(m["y"]), 14, "none", m.get("c", J.ALERT), 5)
                      + txtfit(px(m["x"]) + 26, py(m["y"]) - 18, m.get("t", ""), 460,
                               cap=32, col=m.get("c", J.ALERT)))
    return Fig("".join(g), stages, "", (gx0, gx1))


# ══════════════════════════════════════════════════════════
#  8. dives — 潜航ごとの深さ
# ══════════════════════════════════════════════════════════
def dives(items, dmax=4200, note="", ylab="深さ", show_axis=True):
    """潜航番号を横、到達深度を縦（下向き）に取る棒。第5〜6章の骨。

    items … [dict(n=79, d=3840, c=..., t="", hot=False)]
    """
    gx0, gx1 = BX0 + 130, BX1 - 30
    top, bot = BY0 + 66, BY1 - 92
    n = len(items)
    slot = (gx1 - gx0) / max(1, n)
    bw = min(96, slot * 0.62)
    g = [line(gx0 - 20, top, gx1, top, J.INK_W, 5),
         txt(gx0 - 26, top - 16, "海面", 26, J.INK_W, "Noto", "end")]
    if show_axis:
        for d in range(1000, dmax + 1, 1000):
            y = top + (bot - top) * d / dmax
            g.append(line(gx0 - 20, y, gx1, y, J.GRID, 2))
            g.append(txt(gx0 - 26, y + 10, f"{d:,}", 24, J.LINE_DIM, "Noto", "end"))
        g.append(txt(gx0 - 26, top + 34, ylab, 24, J.LINE_DIM, "Noto", "end"))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.LINE_DIM))
    stages, hot = [], ""
    for i, it in enumerate(items):
        x = gx0 + slot * (i + 0.5)
        h = (bot - top) * min(1.0, it["d"] / dmax)
        c = it.get("c", J.LINE)
        s = [rect(x - bw / 2, top, bw, h, c, op=0.30),
             rect(x - bw / 2, top, bw, h, "none", c, 4)]
        s.append(txt(x, bot + 40, it.get("nt", f'{it["n"]}'), min(34, slot * 0.5),
                     c, "Dela", "middle"))
        dl = f'{it["d"]:,}'
        s.append(txt(x, top + h + 34, dl, min(30, fm.fit(dl, bw + 26, "Dela", cap=30)),
                     c, "Dela", "middle"))
        if it.get("t"):
            s.append(txtfit(x, top + h / 2, it["t"], slot * 1.6, cap=28,
                            col=J.INK_W, anchor="middle"))
        stages.append("".join(s))
        if it.get("hot"):
            hot = rect(x - bw / 2 - 8, top - 8, bw + 16, h + 16, "none", J.ALERT, 5)
    g.append(txt(gx0 - 26, bot + 40, "潜航", 24, J.LINE_DIM, "Noto", "end"))
    return Fig("".join(g), stages, hot, (gx0 - 40, gx1))


# ══════════════════════════════════════════════════════════
#  9. layers — 積層（剥離・空隙・接着面）
# ══════════════════════════════════════════════════════════
def layers(n=5, bonds=None, delam=None, voids=None, note="", labels=True,
           split=None, dims=None):
    """炭素繊維の積層断面。5層＋接着面4つ。第4章と第6章の核心。

    bonds … 接着面の番号(1..n-1)に注記 [dict(i=1, t="1-2", c=..., big=True)]
    delam … 剥離させる接着面の番号
    voids … 空隙を描く接着面の番号
    """
    x0, x1 = BX0 + 190, BX1 - 240
    # ⚠️ 62+16 だと5層で374pxしかなく、枠(682)の下半分が空いた（c415 空き40.7%）。
    #    層は「厚み」を見せる図なので、**枠の縦を使い切る厚さ**にする。
    bt = 22                                # 接着面の厚み
    lh = (BH - 150 - bt * (n - 1)) / n     # 1層の厚み（枠から逆算）
    tot = n * lh + (n - 1) * bt
    top = BY0 + 62
    g = []
    y = top
    ys = []
    for i in range(n):
        g.append(rect(x0, y, x1 - x0, lh, J.LINE, op=0.20))
        g.append(rect(x0, y, x1 - x0, lh, "none", J.LINE, 4))
        # 繊維の向きが分かるよう細い線を入れる（層であることが一目で分かる）
        for k in range(1, 6):
            g.append(line(x0 + 6, y + lh * k / 6, x1 - 6, y + lh * k / 6,
                          J.LINE_DIM, 1.6))
        if labels:
            g.append(txt(x0 - 22, y + lh / 2 + 13, f"{i + 1}層", 34, J.LINE,
                         "Noto", "end"))
        ys.append(y)
        y += lh
        if i < n - 1:
            g.append(rect(x0, y, x1 - x0, bt, J.OK, op=0.55))
            y += bt
    if labels:
        g.append(txt(x1 + 16, top + tot + 44, "接着剤の面", 28, J.OK))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.LINE_DIM))

    def bond_y(i):
        return top + i * (lh + bt) + lh

    stages = []
    for b in (bonds or []):
        i = b["i"]
        c = b.get("c", J.AMBER)
        yy = bond_y(i)
        s = [rect(x0, yy, x1 - x0, bt, c)]
        s.append(line(x1 + 10, yy + bt / 2, x1 + 60, yy + bt / 2, c, 4))
        s.append(txtfit(x1 + 70, yy + bt / 2 + 12, b.get("t", f"{i}-{i + 1}"),
                        BX1 - x1 - 80, cap=34, col=c))
        stages.append("".join(s))
    for i in (voids or []):
        yy = bond_y(i)
        s = []
        for k in range(9):
            vx = x0 + 60 + k * (x1 - x0 - 140) / 9
            s.append(rect(vx, yy - 3, 44 + (k % 3) * 26, bt + 6, J.BG, rx=4))
            s.append(rect(vx, yy - 3, 44 + (k % 3) * 26, bt + 6, "none", J.ALERT, 3,
                          rx=4))
        stages.append("".join(s))
    for i in (delam or []):
        yy = bond_y(i)
        s = [poly([(x0, yy + bt / 2)] +
                  [(x0 + (x1 - x0) * k / 24,
                    yy + bt / 2 + math.sin(k * 0.9) * 13 - k * 0.7)
                   for k in range(1, 25)], stroke=J.ALERT, sw=6)]
        stages.append("".join(s))
    if split:
        yy = bond_y(split)
        stages.append(J.vdim(top, yy, x0 - 90, "厚い1枚")
                      + arrow(x0 - 140, yy, x0 - 140, yy + 60, J.ALERT, 4))
    for d in (dims or []):
        stages.append(J.dim(x0 + d.get("a", 0.1) * (x1 - x0),
                            x0 + d.get("b", 0.5) * (x1 - x0),
                            top + tot + 74, d["t"], J.AMBER, ext=0))
    hot = ""
    if delam:
        yy = bond_y(delam[0])
        hot = rect(x0 - 10, yy - 12, x1 - x0 + 20, bt + 24, "none", J.ALERT, 4)
    return Fig("".join(g), stages, hot, (x0 - 90, x1 + 40))


# ══════════════════════════════════════════════════════════
# 10. titan — 潜水艇そのもの
# ══════════════════════════════════════════════════════════
#  形の根拠：NTSB/MIR-25-36 図3（三面図・NTSB作成＝PD）を実測。
#  全長22フィート＝6.7m、円筒部 8.1フィート＝2.47m、外径 約1.7m。
#  🔴 記憶で描くと必ず形が狂う（[[feedback-drawing-from-reference]]）。
#     報告書の三面図に対する比で置いている：
#       円筒長 / 全長 = 2.47 / 6.70 = 0.369
#       ドーム突出 / 外径 = 約 0.55
# ⚠️ 1180 では枠(1776)に対して小さく、右側が空いた（c203 空き18.1%）。
#    三面図は横に伸びる図なので、**枠の横をほぼ使い切る**大きさにする。
TT_L = 1520.0            # 画面上の全長（既定）


def titan(mode="side", s=1.0, cx=None, cy=None, marks=None, note="",
          bolts=False, window=False, cut=False):
    """潜水艇の側面／断面。marks は [dict(at="cyl"|"fore"|"aft"|"ring", t=..., c=...)]。

    mode … "side"（外形）／"section"（縦断面。中の人と耐圧殻が見える）
    """
    L = TT_L * s
    cx = BCX if cx is None else cx
    cy = (BY0 + BH * 0.44) if cy is None else cy
    R = L * 0.128                      # 外径の半分
    cyl = L * 0.369                    # 円筒部の長さ
    x0 = cx - L / 2
    xc0, xc1 = cx - cyl / 2, cx + cyl / 2
    g = []
    # 外形：前後のドーム＋円筒＋尾部フェアリング
    body = (f'M{xc0:.1f} {cy - R:.1f} H{xc1:.1f} '
            f'A{R * 0.62:.1f} {R:.1f} 0 0 1 {xc1:.1f} {cy + R:.1f} '
            f'H{xc0:.1f} A{R * 0.62:.1f} {R:.1f} 0 0 1 {xc0:.1f} {cy - R:.1f} Z')
    if mode == "section":
        g.append(f'<path d="{body}" fill="{J.BG2}" stroke="{J.INK_W}" '
                 f'stroke-width="5"/>')
        # 耐圧殻の壁厚（5インチ＝127mm。外径1.7mに対する比で 0.075R）
        t = R * 0.15
        g.append(rect(xc0, cy - R, cyl, t, J.LINE, op=0.55))
        g.append(rect(xc0, cy + R - t, cyl, t, J.LINE, op=0.55))
        g.append(rect(xc0, cy - R, cyl, t, "none", J.LINE, 3))
        g.append(rect(xc0, cy + R - t, cyl, t, "none", J.LINE, 3))
        # 中の5人（小さい人型。大きさの実感を出す）
        for i in range(5):
            px_ = xc0 + cyl * (0.17 + i * 0.165)
            g.append(circ(px_, cy + R * 0.10, R * 0.10, J.AMBER))
            g.append(poly([(px_, cy + R * 0.22), (px_, cy + R * 0.60)],
                          stroke=J.AMBER, sw=5))
    else:
        g.append(f'<path d="{body}" fill="{J.BG2}" stroke="{J.INK_W}" '
                 f'stroke-width="5"/>')
    # チタンのリング（円筒の両端）
    for x in (xc0, xc1):
        g.append(rect(x - L * 0.012, cy - R * 1.04, L * 0.024, R * 2.08, J.AMBER,
                      op=0.55))
        g.append(rect(x - L * 0.012, cy - R * 1.04, L * 0.024, R * 2.08, "none",
                      J.AMBER, 3))
    # 尾部の推進器とフレーム
    for sgn in (-1, 1):
        g.append(rect(cx + L * 0.30, cy + sgn * R * 0.62 - L * 0.020, L * 0.055,
                      L * 0.040, J.LINE, op=0.5))
        g.append(rect(cx + L * 0.30, cy + sgn * R * 0.62 - L * 0.020, L * 0.055,
                      L * 0.040, "none", J.LINE, 3))
    g.append(rect(x0 + L * 0.10, cy + R * 0.96, L * 0.74, L * 0.030, J.LINE_DIM,
                  op=0.7))
    if window:
        g.append(circ(x0 + L * 0.045, cy, R * 0.30, J.BG, J.OK, 5))
    if bolts:
        for i in range(10):
            a = math.pi * (i / 9.0) - math.pi / 2
            g.append(circ(xc0 + math.cos(a) * 6, cy + math.sin(a) * R * 0.92, 7,
                          J.AMBER))
    if cut:
        g.append(line(cx, cy - R * 1.5, cx, cy + R * 1.5, J.ALERT, 4, dash="16 10"))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.LINE_DIM))

    anchor = {"fore": (x0 + L * 0.03, cy), "aft": (cx + L * 0.42, cy),
              "cyl": (cx, cy - R), "cylb": (cx, cy + R),
              "ring": (xc0, cy - R), "ring2": (xc1, cy - R),
              "win": (x0 + L * 0.045, cy)}
    stages = []
    used_up, used_dn = [], []
    for m in (marks or []):
        ax_, ay_ = anchor.get(m.get("at", "cyl"), (cx, cy))
        c = m.get("c", J.AMBER)
        up = m.get("up", True)
        ty = cy - R - 90 - 78 * len(used_up) if up else cy + R + 110 + 78 * len(used_dn)
        (used_up if up else used_dn).append(1)
        s = [J.leader(ax_, ay_, ax_, ty + (18 if up else -30), c)]
        s.append(txtfit(ax_ + 18, ty, m["t"], min(760, BX1 - ax_ - 30), cap=36, col=c))
        if m.get("v"):
            s.append(txt(ax_ + 18, ty + 48, m["v"],
                         fm.fit(m["v"], 640, "Dela", cap=46), c, "Dela"))
        stages.append("".join(s))
    return Fig("".join(g), stages, "", (x0 - 40, x0 + L + 40))


# ══════════════════════════════════════════════════════════
# 11. process — 工程を左から右へ
# ══════════════════════════════════════════════════════════
def process(steps, note="", numbered=True, cols=None):
    """N 段の工程図。steps=[dict(t="巻く", d="1インチぶん", c=...)]"""
    n = len(steps)
    cols = cols or n
    gap = 30
    aw = 74                                   # 矢印ぶん
    cw = (BW - gap * (cols - 1) - aw * (cols - 1)) / cols
    # ⚠️ 箱の高さを300に固定していたので、本体枠の下 y640〜880 が丸ごと空いた
    #    （c109 c115 など17カット全部）。**枠の縦を使い切る。**
    top = BY0 + 62
    bh = BY1 - top - (78 if note else 34)
    g = []
    stages = []
    for i, st in enumerate(steps):
        x = BX0 + i * (cw + gap + aw)
        c = st.get("c", J.LINE)
        s = [rect(x, top, cw, bh, c, op=0.14), rect(x, top, cw, bh, "none", c, 4)]
        if numbered:
            s.append(circ(x + 34, top - 2, 26, J.BG, c, 4))
            s.append(txt(x + 34, top + 12, i + 1, 34, c, "Dela", "middle"))
        s.append(txtfit(x + cw / 2, top + 120, st["t"], cw - 30, cap=48,
                        col=J.INK_W, anchor="middle"))
        if st.get("d"):
            sub, _ = para(x + cw / 2, top + 190, st["d"],
                          cols=max(6, int(cw / 30)), size=30, col=J.LINE,
                          anchor="middle")
            s.append(sub)
        if st.get("v"):
            s.append(txt(x + cw / 2, top + bh - 40, st["v"],
                         fm.fit(st["v"], cw - 30, "Dela", cap=72), c, "Dela",
                         "middle"))
        if i < n - 1:
            s.append(arrow(x + cw + 12, top + bh * 0.42, x + cw + gap + aw - 12,
                           top + bh * 0.42, J.LINE_DIM, 5, 22))
        stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 8, note, BW, cap=30, col=J.LINE_DIM))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
# 12. panel — 構造のある文字パネル（引用でない断定）
# ══════════════════════════════════════════════════════════
def panel(blocks, lead="", note="", cols=3):
    """箇条を「箱」でなく「柱」で見せる。**第2章・第6章の結論で使う。**

    blocks … [dict(k="1", t="…", c=...)]
    """
    g = []
    top = BY0 + 40
    if lead:
        s, y = para(BX0, top + 46, lead, cols=30, size=46, col=J.INK_W)
        g.append(s)
        top = y + 56
    n = len(blocks)
    stages = []
    if n <= 3 and all(len(str(b.get("t", ""))) <= 46 for b in blocks):
        # ⚠️ 150に頭打ちしていたので、3件でも枠の下200pxが空いた（c211 32%）。
        h = (BY1 - top - 10 - (44 if note else 0)) / max(1, n)
        for i, b in enumerate(blocks):
            y = top + i * h
            c = b.get("c", J.LINE)
            s = [rect(BX0, y, 9, h - 22, c)]
            ks = min(72, h * 0.46)
            if b.get("k"):
                s.append(txt(BX0 + 34, y + h * 0.52, b["k"], ks, c, "Dela"))
            tx0 = BX0 + (150 if b.get("k") else 34)
            # ⚠️ v の場所（右540px）を、v が無いときまで空けていた。
            rsv = 540 if b.get("v") else 0
            avail = BX1 - tx0 - rsv
            # 🔴 器を広げても**中身が短いカットは埋まらない**（c208「圧縮」の2字など）。
            #    1行で収まる短い文は、幅を使い切る級数まで上げる。
            #    34分をスマホで見る動画なので、字が大きいこと自体が読みやすさになる。
            one = fm.fit(str(b["t"]), avail, "Noto", cap=int(min(96, h * 0.52)),
                         floor=16)
            bs = one if fm.width(str(b["t"]), one, "Noto") <= avail else                 min(52, h * 0.34)
            body, _ = para(tx0, y + h * 0.52, b["t"],
                           cols=max(6, int(avail / bs)), size=bs, col=J.INK_W)
            s.append(body)
            if b.get("v"):
                s.append(txt(BX1, y + h * 0.54, b["v"],
                             fm.fit(b["v"], 500, "Dela", cap=min(76, h * 0.50)),
                             c, "Dela", "end"))
            stages.append("".join(s))
    else:
        cw = (BW - 30 * (cols - 1)) / cols
        for i, b in enumerate(blocks):
            x = BX0 + (i % cols) * (cw + 30)
            y = top + (i // cols) * ((BY1 - top) / max(1, math.ceil(n / cols)))
            c = b.get("c", J.LINE)
            s = [line(x, y, x + cw - 20, y, c, 5)]
            if b.get("k"):
                s.append(txt(x, y + 52, b["k"], 40, c, "Dela"))
            body, _ = para(x, y + (104 if b.get("k") else 54), b["t"],
                           cols=int(cw / 34), size=34, col=J.INK_W)
            s.append(body)
            stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.LINE_DIM))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
# 13. absent — 「無い」ことを見せる
# ══════════════════════════════════════════════════════════
def absent(items, lead="", note=""):
    """空欄・破線・×で「存在しない／受けていない」を見せる。

    第2章の「規格が無い」「登録が無い」「検査が無い」はこの型でしか強くならない。
    """
    n = len(items)
    gap = 40
    cw = (BW - gap * (n - 1)) / n
    top = BY0 + 128
    # ⚠️ 290 固定だと箱の下 y730〜892 が空いた。説明の行ぶんを残して枠を使い切る。
    bh = BY1 - top - 168
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 74, lead, BW, cap=48, col=J.INK_W))
    stages = []
    for i, it in enumerate(items):
        x = BX0 + i * (cw + gap)
        ok = it.get("ok", False)
        c = J.OK if ok else J.ALERT
        s = [rect(x, top, cw, bh, "none", J.LINE_DIM, 4,
                  rx=8)] if not ok else [rect(x, top, cw, bh, J.OK, 4, rx=8, op=0.14)]
        if not ok:
            s = [rect(x, top, cw, bh, J.BG2, op=0.5),
                 rect(x, top, cw, bh, "none", J.LINE_DIM, 4, rx=8)]
            s.append(hatch(x + 4, top + 4, cw - 8, bh - 8, J.LINE_DIM, 22, 0.35))
            s.append(line(x + cw * 0.30, top + bh * 0.30, x + cw * 0.70,
                          top + bh * 0.70, J.ALERT, 9))
            s.append(line(x + cw * 0.70, top + bh * 0.30, x + cw * 0.30,
                          top + bh * 0.70, J.ALERT, 9))
        s.append(txtfit(x + cw / 2, top + bh + 52, it["t"], cw + 20, cap=38,
                        col=c, anchor="middle"))
        if it.get("d"):
            sub, _ = para(x + cw / 2, top + bh + 96, it["d"], cols=int(cw / 26),
                          size=26, col=J.LINE_DIM, anchor="middle")
            s.append(sub)
        stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.LINE_DIM))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
# 14. icons — 個数を絵で見せる
# ══════════════════════════════════════════════════════════
def icons(n, on=None, kind="dot", cols=None, lead="", note="", oncol=None,
          offcol=None, labels=None):
    """n 個のうち on 個（または on のリスト）を強調する。

    kind … "dot"／"person"／"ship"／"sub"
    """
    on = list(range(on)) if isinstance(on, int) else (on or [])
    cols = cols or min(n, 12)
    rows = math.ceil(n / cols)
    # ⚠️ 120×150 に頭打ちしていたので、5個や9個のときに絵が小さく、
    #    下半分が丸ごと空いた（pr02 23%／ep01 25%／c501 28%／c512 28%）。
    #    **枠を使い切る大きさ**にする。
    lead_h = 96 if lead else 20
    note_h = 56 if note else 10
    cw = min(BW / cols, 300)
    ch = min((BH - lead_h - note_h) / max(1, rows), 340)
    x0 = BCX - cw * cols / 2
    top = BY0 + lead_h + ch * 0.42
    oc = oncol or J.ALERT
    fc = offcol or J.LINE_DIM
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 62, lead, BW, cap=52, col=J.INK_W))
    stages = []
    cur = []
    for i in range(n):
        x = x0 + (i % cols) * cw + cw / 2
        y = top + (i // cols) * ch
        c = oc if i in on else fc
        r = min(cw, ch) * 0.40
        if kind == "person":
            cur.append(circ(x, y, r * 0.52, c))
            cur.append(poly([(x - r * 0.62, y + r * 1.9), (x - r * 0.62, y + r * 0.95),
                             (x, y + r * 0.62), (x + r * 0.62, y + r * 0.95),
                             (x + r * 0.62, y + r * 1.9)], fill=c, close=True))
        elif kind == "ship":
            cur.append(poly([(x - r, y), (x + r, y), (x + r * 0.62, y + r * 0.72),
                             (x - r * 0.62, y + r * 0.72)], fill=c, close=True))
            cur.append(rect(x - r * 0.20, y - r * 0.86, r * 0.40, r * 0.86, c))
        elif kind == "sub":
            cur.append(rect(x - r, y - r * 0.44, r * 2, r * 0.88, c, rx=r * 0.44))
        else:
            cur.append(circ(x, y, r * 0.62, c))
        if labels and i < len(labels):
            cur.append(txtfit(x, y + r * 2.3, labels[i], cw * 0.98,
                              cap=max(24, int(cw * 0.20)), col=c, anchor="middle"))
    stages.append("".join(cur))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.LINE_DIM))
    return Fig("".join(g), stages, "", (x0 - 20, x0 + cw * cols + 20))


# ══════════════════════════════════════════════════════════
# 15. sound — 2点で同じ音を聞いた（プロローグと第5章の核心）
# ══════════════════════════════════════════════════════════
def sound(depth_m=3840, note="", rings=4, both=True, label_a="潜水艇の中",
          label_b="海面のボート"):
    """海面のボートと浮上中の潜水艇。**2点同時に届いた**ことが要点。"""
    top, bot = BY0 + 70, BY1 - 60
    g = [watertone(BX0, top, BW, bot - top, 0.08, 0.40),
         line(BX0, top, BX1, top, J.INK_W, 5)]
    bx, by = BCX - 380, top
    sx, sy = BCX + 240, top + (bot - top) * 0.52
    # 海面のボート
    g.append(poly([(bx - 74, by), (bx + 74, by), (bx + 48, by - 34), (bx - 48, by - 34)],
                  fill=J.INK_W, close=True))
    g.append(txtfit(bx, by - 60, label_b, 460, cap=32, col=J.INK_W, anchor="middle"))
    # 潜水艇
    g.append(rect(sx - 92, sy - 34, 184, 68, J.INK_W, rx=34))
    g.append(txtfit(sx, sy + 82, label_a, 460, cap=32, col=J.INK_W, anchor="middle"))
    g.append(arrow(sx, sy - 54, sx, sy - 130, J.LINE, 4, 16))
    g.append(txt(sx + 16, sy - 96, "浮上中", 28, J.LINE))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.LINE_DIM))
    stages = []
    ox, oy = (bx + sx) / 2, sy + 150
    for k in range(rings):
        r = 120 + k * 128
        stages.append(f'<path d="M{ox - r:.0f} {oy:.0f} A{r} {r} 0 0 1 '
                      f'{ox + r:.0f} {oy:.0f}" fill="none" stroke="{J.ALERT}" '
                      f'stroke-width="{6 - k * 0.8:.1f}" opacity="{0.95 - k * 0.16:.2f}"/>')
    if both:
        stages.append(circ(bx, by - 4, 22, "none", J.ALERT, 5)
                      + circ(sx, sy, 22, "none", J.ALERT, 5)
                      + txtfit(BCX, bot + 6, "同じ音を、同じときに", BW * 0.7, cap=40,
                               col=J.ALERT, anchor="middle"))
    return Fig("".join(g), stages, circ(ox, oy, 40, "none", J.ALERT, 4), (BX0, BX1))


# ══════════════════════════════════════════════════════════
# 16. gauge — 監視装置のしきい値
# ══════════════════════════════════════════════════════════
def gauge(hits=None, yellow=30, red=50, vmax=60, lead="", note="", marks=None):
    """ヒット数と黄・赤のしきい値。第5章の「なぜ赤が出なかったか」の土台。"""
    x0, x1 = BX0 + 60, BX1 - 60
    y = BY0 + 250
    h = 96
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 80, lead, BW, cap=46, col=J.INK_W))

    def px(v):
        return x0 + (x1 - x0) * v / vmax

    g.append(rect(x0, y, x1 - x0, h, J.BG2, op=0.7))
    g.append(rect(x0, y, px(yellow) - x0, h, J.OK, op=0.20))
    g.append(rect(px(yellow), y, px(red) - px(yellow), h, J.AMBER, op=0.28))
    g.append(rect(px(red), y, x1 - px(red), h, J.ALERT, op=0.30))
    g.append(rect(x0, y, x1 - x0, h, "none", J.LINE, 4))
    for v, c, t in ((yellow, J.AMBER, "黄"), (red, J.ALERT, "赤")):
        g.append(line(px(v), y - 26, px(v), y + h + 26, c, 5))
        g.append(txt(px(v), y - 40, f"{v}回", 38, c, "Dela", "middle"))
        g.append(txt(px(v), y + h + 62, t, 32, c, "Noto", "middle"))
    g.append(txt(x0, y + h + 62, "0", 30, J.LINE_DIM, "Dela"))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.LINE_DIM))
    stages = []
    if hits is not None:
        stages.append(rect(x0, y, px(hits) - x0, h, J.LINE, op=0.75)
                      + txt(px(hits) + 16, y + h / 2 + 14, f"{hits}", 46, J.INK_W,
                            "Dela"))
    for m in (marks or []):
        stages.append(txtfit(BX0, BY1 - 120 + 52 * len(stages), m, BW, cap=36,
                             col=J.LINE))
    return Fig("".join(g), stages, "", (x0, x1))


# ══════════════════════════════════════════════════════════
# 17. mapfig — 位置関係（Google Maps は使えないので自作）
# ══════════════════════════════════════════════════════════
def mapfig(points, note="", link=None, scale=None, lead=""):
    """北大西洋の簡略図。points=[dict(x=0.2,y=0.3,t="セントジョンズ",c=...,kind=)]

    x,y は本体枠に対する 0〜1。**地図の正確さではなく位置関係だけを持たせる。**
    """
    x0, y0 = BX0 + 40, BY0 + 40
    w, h = BW - 80, BH - 110
    g = [rect(x0, y0, w, h, J.BG2, op=0.55), rect(x0, y0, w, h, "none", J.LINE_DIM, 3)]
    # 海の地紋（緯線・経線）
    for i in range(1, 8):
        g.append(line(x0, y0 + h * i / 8, x0 + w, y0 + h * i / 8, J.GRID, 2))
    for i in range(1, 10):
        g.append(line(x0 + w * i / 10, y0, x0 + w * i / 10, y0 + h, J.GRID, 2))
    # ニューファンドランドの島影（形は似せない。陸だと分かればよい）
    g.append(poly([(x0 + w * 0.05, y0 + h * 0.10), (x0 + w * 0.26, y0 + h * 0.05),
                   (x0 + w * 0.33, y0 + h * 0.22), (x0 + w * 0.27, y0 + h * 0.40),
                   (x0 + w * 0.09, y0 + h * 0.36)],
                  fill=J.LINE_DIM, close=True, op=0.55))
    g.append(txt(x0 + w * 0.07, y0 + h * 0.50, "ニューファンドランド", 26, J.LINE_DIM))
    if lead:
        g.append(txtfit(BX0, BY0 + 16, lead, BW, cap=40, col=J.INK_W))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.LINE_DIM))

    def P(p):
        return (x0 + w * p["x"], y0 + h * p["y"])

    stages = []
    if link and len(points) >= 2:
        a, b = P(points[link[0]]), P(points[link[1]])
        s = [poly([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 60), b],
                  stroke=J.AMBER, sw=5, dash="18 12")]
        if scale:
            s.append(txtfit((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 76, scale, 620,
                            cap=34, col=J.AMBER, anchor="middle"))
        stages.append("".join(s))
    for p in points:
        x, y = P(p)
        c = p.get("c", J.AMBER)
        s = []
        if p.get("kind") == "wreck":
            s.append(line(x - 22, y - 22, x + 22, y + 22, c, 6))
            s.append(line(x + 22, y - 22, x - 22, y + 22, c, 6))
        else:
            s.append(circ(x, y, 13, c))
            s.append(circ(x, y, 26, "none", c, 4))
        anch = "start" if p.get("x", 0.5) < 0.7 else "end"
        s.append(txtfit(x + (34 if anch == "start" else -34), y + 12, p["t"], 560,
                        cap=34, col=c, anchor=anch))
        if p.get("d"):
            s.append(txtfit(x + (34 if anch == "start" else -34), y + 50, p["d"], 560,
                            cap=26, col=J.LINE_DIM, anchor=anch))
        stages.append("".join(s))
    return Fig("".join(g), stages, "", (x0, x0 + w))


# ══════════════════════════════════════════════════════════
# 18. people — 人と組織のあいだで起きたこと
# ══════════════════════════════════════════════════════════
def people(nodes, edges=None, note="", lead=""):
    """人・組織を箱で置き、あいだの出来事を矢印に書く。第3章の解雇の連鎖に使う。

    nodes … [dict(x=0.1, y=0.3, t="海洋運用部長", c=...)]（x,y は 0〜1）
    edges … [dict(a=0, b=1, t="1月19日 会話", c=...)]
    """
    x0, y0 = BX0 + 20, BY0 + 60
    w, h = BW - 40, BH - 150
    bw, bh = 460, 140
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 20, lead, BW, cap=40, col=J.INK_W))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.LINE_DIM))

    def C(i):
        n = nodes[i]
        return (x0 + w * n["x"], y0 + h * n["y"])

    stages = []
    for e in (edges or []):
        a, b = C(e["a"]), C(e["b"])
        c = e.get("c", J.LINE)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        a2 = (a[0] + math.cos(ang) * bw * 0.5, a[1] + math.sin(ang) * bh * 0.62)
        b2 = (b[0] - math.cos(ang) * bw * 0.54, b[1] - math.sin(ang) * bh * 0.66)
        s = [arrow(a2[0], a2[1], b2[0], b2[1], c, 5, 20)]
        if e.get("t"):
            mx, my = (a2[0] + b2[0]) / 2, (a2[1] + b2[1]) / 2
            tw = fm.width(e["t"], 30, "Noto") + 24
            s.append(rect(mx - tw / 2, my - 24, tw, 44, J.BG, rx=6))
            s.append(txtfit(mx, my + 8, e["t"], tw, cap=30, col=c, anchor="middle"))
        stages.append("".join(s))
    for n in nodes:
        x, y = x0 + w * n["x"], y0 + h * n["y"]
        c = n.get("c", J.LINE)
        s = [rect(x - bw / 2, y - bh / 2, bw, bh, c, op=0.16),
             rect(x - bw / 2, y - bh / 2, bw, bh, "none", c, 4, rx=6)]
        s.append(txtfit(x, y + (0 if not n.get("d") else -14), n["t"], bw - 26,
                        cap=36, col=J.INK_W, anchor="middle"))
        if n.get("d"):
            s.append(txtfit(x, y + 34, n["d"], bw - 26, cap=26, col=J.LINE_DIM,
                            anchor="middle"))
        stages.append("".join(s))
    return Fig("".join(g), stages, "", (x0, x0 + w))


# ══════════════════════════════════════════════════════════
# 19. beforeafter — 前と後
# ══════════════════════════════════════════════════════════
def beforeafter(a, b, note="", lead=""):
    """左右2枚。a/b は dict(k="変更前", t="…", lines=[…], c=…)。"""
    cw = (BW - 90) / 2
    top = BY0 + 96
    bh = BY1 - top - 60
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 62, lead, BW, cap=44, col=J.INK_W))
    g.append(arrow(BCX - 26, top + bh / 2, BCX + 26, top + bh / 2, J.AMBER, 6, 22))
    stages = []
    for i, side in enumerate((a, b)):
        x = BX0 + i * (cw + 90)
        c = side.get("c", J.LINE if i == 0 else J.ALERT)
        s = [rect(x, top, cw, bh, c, op=0.12), rect(x, top, cw, bh, "none", c, 4)]
        s.append(chip(x + 20, top - 22, side.get("k", ""), c, 28))
        y = top + 82
        s.append(txtfit(x + cw / 2, y, side.get("t", ""), cw - 30, cap=44,
                        col=J.INK_W, anchor="middle"))
        y += 66
        for ln in side.get("lines", []):
            s.append(txtfit(x + 24, y, "・" + ln, cw - 44, cap=32, col=J.LINE))
            y += 46
        if side.get("v"):
            s.append(txt(x + cw / 2, top + bh - 30, side["v"],
                         fm.fit(side["v"], cw - 40, "Dela", cap=70), c, "Dela",
                         "middle"))
        stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.LINE_DIM))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
# 20. buckle — 座屈のしくみ（第6章）
# ══════════════════════════════════════════════════════════
def buckle(kind="local", note="", lead="", labels=True):
    """圧縮での壊れ方。kind … "crush"／"global"／"local"／"peel"／"s"。"""
    cx, cy = BCX, BY0 + BH * 0.46
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 56, lead, BW, cap=46, col=J.INK_W))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.LINE_DIM))
    L, T = 1240, 170
    stages = []
    if kind == "crush":
        g.append(rect(cx - L / 2, cy - T / 2, L, T, J.LINE, op=0.24))
        g.append(rect(cx - L / 2, cy - T / 2, L, T, "none", J.LINE, 5))
        stages.append("".join(arrow(cx - L / 2 + i * L / 6, cy - T / 2 - 92,
                                    cx - L / 2 + i * L / 6, cy - T / 2 - 16,
                                    J.ALERT, 5) for i in range(7)))
        stages.append(rect(cx - L / 2, cy - T / 2, L, T, J.ALERT, op=0.32)
                      + txtfit(cx, cy + T + 60, "材料そのものが潰れる", 900, cap=40,
                               col=J.ALERT, anchor="middle"))
    elif kind in ("global", "local", "s"):
        amp = 120 if kind == "global" else 88
        seg = (0.0, 1.0) if kind == "global" else (0.34, 0.66)

        def wavy(t):
            if kind == "s":
                return math.sin(t * math.pi * 2) * amp
            if not (seg[0] <= t <= seg[1]):
                return 0.0
            u = (t - seg[0]) / (seg[1] - seg[0])
            return math.sin(u * math.pi) * amp
        base = [(cx - L / 2 + L * i / 60, cy) for i in range(61)]
        bent = [(cx - L / 2 + L * i / 60, cy + wavy(i / 60)) for i in range(61)]
        g.append(poly(base, stroke=J.LINE_DIM, sw=4, dash="14 10"))
        stages.append(poly(bent, stroke=J.ALERT, sw=9))
        stages.append("".join(arrow(cx - L / 2 - 90, cy, cx - L / 2 - 16, cy,
                                    J.AMBER, 6, 20)
                              + arrow(cx + L / 2 + 90, cy, cx + L / 2 + 16, cy,
                                      J.AMBER, 6, 20)))
        if labels:
            t = {"global": "全体が座屈を起こす", "local": "一部だけが座屈を起こす",
                 "s": "S字に曲がった座屈の跡"}[kind]
            stages.append(txtfit(cx, cy + amp + 130, t, 1100, cap=42, col=J.ALERT,
                                 anchor="middle"))
    elif kind == "peel":
        y = cy
        g.append(rect(cx - L / 2, y, L, 46, J.LINE, op=0.24))
        g.append(rect(cx - L / 2, y, L, 46, "none", J.LINE, 4))
        pts = [(cx - L / 2 + L * i / 40,
                y - 4 - (0 if i > 22 else (22 - i) ** 1.7 * 0.62)) for i in range(41)]
        stages.append(poly(pts, stroke=J.ALERT, sw=8))
        # ⚠️ 注記を上に置くと lead（BY0+56）とぶつかる。**帯の下**へ回す。
        stages.append(arrow(cx - L / 2 + 60, y + 196, cx + L * 0.10, y + 74,
                            J.ALERT, 5, 20)
                      + txtfit(cx - L / 2 + 60, y + 240, "縁からめくれて広がる", 720,
                               cap=36, col=J.ALERT))
    return Fig("".join(g), stages, "", (cx - L / 2 - 100, cx + L / 2 + 100))


# ══════════════════════════════════════════════════════════
# 21. window — のぞき窓の断面（第4章）
# ══════════════════════════════════════════════════════════
def window(note="", marks=None, lead=""):
    """中央が厚く縁が薄い、標準でない形の窓。1,000m しか認証されなかった。"""
    cx, cy = BCX - 120, BY0 + BH * 0.48
    R, TC, TE = 300, 190, 74          # 半径・中央の厚み・縁の厚み
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 56, lead, BW, cap=44, col=J.INK_W))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.LINE_DIM))
    top = [(cx - R + i * 2 * R / 40,
            cy - TE / 2 - (TC - TE) / 2 * math.cos(math.pi * (i / 40 - 0.5) * 2 * 0.5))
           for i in range(41)]
    bot = [(x, 2 * cy - y) for x, y in reversed(top)]
    g.append(poly(top + bot, fill=J.OK, close=True, op=0.24))
    g.append(poly(top + bot, stroke=J.OK, close=True, sw=5))
    g.append(line(cx - R - 120, cy - 210, cx - R - 120, cy + 210, J.LINE_DIM, 3))
    g.append(txt(cx - R - 136, cy, "外", 30, J.LINE_DIM, "Noto", "end"))
    # ⚠️ 「縁は薄い」の寸法線が cx+R+190 に立つので、そのラベル（左へ伸びる）と
    #    重なっていた。内側のラベルは寸法線の外へ出す。
    g.append(txt(cx + R + 330, cy, "内", 30, J.LINE_DIM))
    stages = [J.vdim(cy - TC / 2, cy + TC / 2, cx - 34, "中央は厚い"),
              J.vdim(cy - TE / 2, cy + TE / 2, cx + R + 190, "縁は薄い")]
    for m in (marks or []):
        stages.append(txtfit(BX0, BY1 - 150 + 56 * len(stages), m, BW, cap=38,
                             col=J.ALERT))
    return Fig("".join(g), stages, "", (cx - R - 160, cx + R + 300))
