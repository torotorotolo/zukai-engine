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
import re

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
    """図1枚ぶん。build 側はこの6つしか見ない。

    holds … 段ごとの「いつ出すか」。既定（None）はナレーションの行頭に貼る。
            **"with_last"** … 🔴 **最後の行を読み"始める"のと同時**に出はじめ、
              その行を読み終えるころに出そろう（引用の決め所。2026-08-03）。
              **声と文字が重なる**のが肝。読み終えてから出すと、視聴者は
              もう答えを聞いてしまっているので**何の意外性もない**。
              ⚠️ 同時に出るぶん、その行の字幕は消さないと二重表示になる。
                 `scene_jiko.SUB_MUTE` が最後の行を落とし、
                 `build_jiko.meta_of` が `"mute"` として持ち回る。
              🔴 したがって**台本側で「決め所そのものを最後の行に置く」**必要がある。
                 前振りを最後の行にすると、関係ない行の字幕が消える。
            **"after_last"** … 最後の行を読み終えてから出す。
              ⚠️ **2026-08-03 に撤回。新規に使わない**（既存カットの再現用にだけ残す）。
    labk  … 骨格（lab）を描くのにカットの何割を使うか（既定 0.30）。
            段が1つしかない型は、骨格をゆっくり描かないと途中で画が止まる。
    """

    def __init__(self, lab, stages=None, hot="", span=None, holds=None, labk=None):
        self.lab = lab
        keep = [i for i, s in enumerate(stages or []) if s]
        self.stages = [(stages or [])[i] for i in keep]
        # holds は stages と同じ長さに揃える（空の段を捨てたぶんもここで合わせる）
        self.holds = ([((holds or [])[i] if i < len(holds or []) else None)
                       for i in keep] if holds else [None] * len(self.stages))
        self.hot = hot
        self.span = span or (BX0, BX1)
        self.labk = labk


# ── 文字の置き方（すべて実測で収める） ─────────────────────
XML = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def esc(t):
    return "".join(XML.get(c, c) for c in str(t))


# 🔴 沈める色を**文字に使わない**ための振り替え（2026-08-02）。
#    r13 の試写「目盛りの文字が背景と同化して読めない」で TICK を足したが、
#    直したのは型の内部だけだった。**カット側が `c=J.LINE_DIM` を渡すと、
#    その色がそのまま文字に使われていた**（実測 27か所）。
#    線・面は沈めたままでよいので、**文字のときだけ**読める色へ振り替える。
#    ⚠️ `ALERT_DIM` は引用の大きな「」など**わざと沈めた飾り**に使うので入れない。
DIM_INK = {J.LINE_DIM: J.TICK, J.GRID: J.TICK}


_DIGIT = re.compile(r"[0-9０-９]")


def numfam(t, fam):
    """**Dela は数字のための書体**。漢字を入れると画がつぶれて読めない。

    🔴 2026-08-02（r25 の拡大目視）：Dela Gothic One は極太の見出し書体で、
       画数の多い漢字を入れると**線が互いに埋まって字の中の空きが消える**。
       実測した3例：
         c407 「機械」          … 124px でも塊にしか見えない
         c301 「円筒（炭素繊維）」… 「繊維」がつぶれる
         c604 「液体」「固体」   … **同じ箱の中の「水」「氷」（Noto）は読める**
       ＝ 書体の選択がまちがっているだけで、級数の問題ではない。

    → 数字を含まない文字列は Noto に落とす（数字は Dela のまま）。

    ⚠️ 級数は呼び出し側が **Dela の字幅で測ってから**渡してくる。
       漢字・かなは Dela と Noto で字幅がほぼ同じなので入れ替えてもはみ出さないが、
       **「・」だけは Dela 0.351 / Noto 1.000 と違う**ので その字を含むものは触らない。

    🔴 2026-08-05（r07 の目視）：`c435`「発見に時間を要したのはやむを得ない」が
       40px の Dela のまま焼かれ、漢字がつぶれて読めなかった。
       ⚠️ **許容差 0.001 を 0.01 に緩める直し方は採らなかった。**
         「は」だけが Dela 1.003 / Noto 1.000 で網に掛かっていたのは事実だが、
         緩めると `moment` の決め所 11件が Dela→Noto に変わる。実物を見ると
         そのうち10件（63〜99px）は Dela のままで読めていて、太い決め所という
         見え方をわざと作っている場所だった。つぶれていたのは 40px の1件だけ。
       → 書体の規則ではなく**入れるものが間違っていた**（決め所に一文を入れた）。
         `moment` の `v` は短い決め語にする。長い文は `t` 側か副題へ。
         再発は `check_layout` の「小さい Dela に漢字の句」が止める。
    """
    if fam != "Dela" or not t:
        return fam
    s = str(t)
    if _DIGIT.search(s):
        return fam
    if any(abs(fm.adv(c, "Dela") - fm.adv(c, "Noto")) > 0.001 for c in s):
        return fam
    return "Noto"


def txt(x, y, t, size=32, col=None, fam="Noto", anchor="start", ol=0):
    """1行。`ol` にフチの太さを渡すと写真や図の上でも読める。"""
    col = DIM_INK.get(col, col)
    fam = numfam(t, fam)
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
    """全角換算 cols 字で折る。読点・句点を優先して折る。

    🔴 2026-08-05（r10 の拡大目視）：**最後の行に1〜2字だけ残る**箇所が10あった。
       いちばんひどいのは c505「サイド・スキャン・ソナ／**ー**」＝長音符だけの行。
       原因はここが**字数で折っている**こと（`balance()` と違って禁則も
       語中の切れも見ていない）。同じ轍は決め所で一度踏んでいて、
       そのとき作ったのが `balance()` なのに、こちらへは回していなかった。
       → **尻切れになったときだけ** `balance()` に投げ直す。
          行が増えると箱の高さが変わるので、増えるときは元のまま返す。
    """
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
    if len(out) > 1 and sum(fm.adv(c, "Noto") for c in out[-1]) <= 2.0:
        b = balance(t, cols)
        if len(b) <= len(out):
            return b
    return out


def balance(t, cols):
    """決め所の言葉を**行の長さがそろうように**折る。

    🔴 幅だけで折ると最後の行に2字だけ残る。実際に
       「船体が受け台の中でず／れた」「もう一度潜ってどうな／るか見よう」と割れた
       （r5 の目視で発見。机上の検算では出ない）。
       行数を先に決めて、その行数で等分する。
    """
    t = str(t)
    n = sum(fm.adv(c, "Noto") for c in t)
    rows = max(1, math.ceil(n / cols))
    if rows == 1:
        return [t]
    per = n / rows
    # 切ってよい位置を点数づけする。
    #   ＋ 読点・句点の**後ろ**（意味の切れ目）
    #   ＋ 助詞の後ろ（「船体が｜受け台」のように語の切れ目になりやすい）
    #   − 行頭に 、。」 が来る位置（禁則）
    BONUS_AFTER = "、。はがをにでとのもへや"
    # 行頭に来てはいけない字（禁則）。小書きのかなと長音符もここに入れる
    NG_HEAD = "、。」）ァィゥェォャュョッーぁぃぅぇぉゃゅょっ"

    def kata(c):
        return "ァ" <= c <= "ヶ" or c == "ー"

    def hira(c):
        return "ぁ" <= c <= "ゖ"
    out, start, acc, ideal = [], 0, 0.0, per
    for i, ch in enumerate(t):
        acc += fm.adv(ch, "Noto")
        if len(out) >= rows - 1:
            continue
        if acc < ideal * 0.55:
            continue
        best = None
        for j in range(i, min(len(t) - 1, i + 4) + 1):
            w = sum(fm.adv(c, "Noto") for c in t[start:j + 1])
            if w > ideal * 1.45:
                break
            sc = abs(w - ideal)
            if t[j] in BONUS_AFTER:
                sc -= 1.2
            if j + 1 < len(t) and t[j + 1] in NG_HEAD:
                sc += 5.0
            # 語の途中で切らない。カタカナ語の途中はとくに読めなくなる
            #（「21フ／ィートの潜水艦」が実際に出た）
            if j + 1 < len(t) and kata(t[j]) and kata(t[j + 1]):
                sc += 4.0
            if j + 1 < len(t) and hira(t[j]) and hira(t[j + 1])                     and t[j] not in BONUS_AFTER:
                sc += 1.6
            if best is None or sc < best[0]:
                best = (sc, j)
        if best and (acc >= ideal or best[0] < 0):
            j = best[1]
            out.append(t[start:j + 1])
            start, acc = j + 1, 0.0
    if start < len(t):
        out.append(t[start:])
    return out


def para(x, y, t, cols=28, size=34, col=None, lh=1.5, anchor="start", ol=0, fam="Noto"):
    """折り返す本文。戻り値は (svg, 最終行のベースライン y)。"""
    g = []
    yy = y
    for ln in wrap(t, cols):
        g.append(txt(x, yy, ln, size, col, fam, anchor, ol))
        yy += size * lh
    return "".join(g), yy - size * lh


def rect(x, y, w, h, fill="none", stroke=None, sw=4, rx=0, op=None, dash=None):
    o = f' opacity="{op}"' if op is not None else ""
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<rect x="{x:.0f}" y="{y:.0f}" width="{max(0, w):.0f}" '
            f'height="{max(0, h):.0f}" rx="{rx}" fill="{fill}"{s}{d}{o}/>')


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
        g.append(txt(ax - 28, y + 11, f"{d:,}", 26, J.TICK, "Noto", "end"))
        d += stepm
    g.append(txt(ax - 28, top + 28, axis_t, 26, J.TICK, "Noto", "end"))
    if seabed is not None:
        y = dy(seabed)
        g.append(poly([(BX0, y)] + [(BX0 + i * 74, y + (12 if i % 2 else -6))
                                    for i in range(1, 25)], stroke=J.LINE_DIM, sw=4))
        g.append(txt(BX1, y + 40, "海底", 28, J.TICK, "Noto", "end"))
    if note:
        # ⚠️ 右下に置くと「海底」ラベル（同じく右下）と必ず重なる。
        #    seabed を渡すカットは全部これに当たった（c113a c114 c115b c121 c130）。
        g.append(txtfit(BX0, BY1 - 6, note, BW - 300, cap=28, col=J.TICK))

    # 500m ごとの細い目盛り。線1本だけの海にしない
    dd = stepm // 2
    while dd <= dmax:
        if dd % stepm:
            yy = dy(dd)
            g.append(line(ax - 9, yy, ax + 9, yy, J.LINE_DIM, 2))
        dd += stepm // 2

    # 🔴 2026-08-02（r21 の目視・c616）：印が縦に近いと、**上の印の潜水艇の絵が
    #    下の印の数字の頭を削る**。c616 は 3,346（big）と 3,840 が 60px しか離れて
    #    おらず、カプセル（y±22）が「3,840」の上を 108×8px 覆っていた。
    #    ⚠️ 机上検査もこれを 1px の差で見逃していた（`iy <= 8` のしきい値）。
    #    → 近すぎる印は、下側の数字を**絵の下へ**逃がす。
    NEED = 78.0                       # 絵の下端(y+22) と 数字の字面上端 が離れる量
    lab_dy = {}
    order_ = sorted(range(len(marks)), key=lambda i: marks[i]["d"])
    for a_, b_ in zip(order_, order_[1:]):
        gap_ = dy(marks[b_]["d"]) - dy(marks[a_]["d"])
        if marks[a_].get("big") and gap_ < NEED:
            lab_dy[b_] = NEED - gap_

    stages = []
    for mi, m in enumerate(marks):
        y = dy(m["d"])
        ldy = lab_dy.get(mi, 0.0)
        c = m.get("c", J.AMBER)
        big = m.get("big", False)
        s = [line(ax, y, BX1 - 8, y, c, 6 if big else 4,
                  dash=None if big else "14 10")]
        s.append(circ(ax, y, 11 if big else 8, c))
        # ⚠️ いちばん大事な印には**潜水艇そのもの**を置く。
        #    印が1つだけのカットが「線1本の海」になっていた（c408 c409 c420 ほか）。
        if big:
            # 🔴 2026-08-02：潜水艇の絵を軸の中心（ax±92）に置いていたので、
            #    **軸の左に出している目盛りの数字（ax-28 で右寄せ）を覆っていた**
            #    （c130・c420・c510・c610・c121 の「4,000」「2,000」「水深」が消えていた）。
            #    新しく作った「図形が文字を横切る」検査が拾った。絵を軸の右へ寄せる。
            s.append(rect(ax - 20, y - 22, 168, 44, J.BG2, rx=22))
            s.append(rect(ax - 20, y - 22, 168, 44, "none", c, 5, rx=22))
            s.append(line(ax + 104, y - 22, ax + 118, y - 42, c, 4))
        size = 76 if big else 48
        # ⚠️ 文字は絵の外から始める（r19 の目視で数字と札が絵に重なっていた）
        lx = ax + (164 if big else 40)
        s.append(txt(lx, y - 16 + ldy, f'{m["d"]:,}', size, c, "Dela"))
        nw = fm.width(f'{m["d"]:,}', size, "Dela")
        s.append(txt(lx + nw + 10, y - 16 + ldy, unit, size * 0.36, c))
        if m.get("t"):
            s.append(txtfit(lx, y + (44 if big else 34) + ldy, m["t"],
                            BX1 - lx - 20, cap=40 if big else 32, col=c))
        if m.get("sub"):
            s.append(txtfit(BX1, y - 16 + ldy, m["sub"], 620, cap=34, col=J.TICK,
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
def compare(items, unit="", note="", bar=True, ratio="", vmax=None, ref=""):
    """2〜4個の数値を、棒の長さで比べる。

    items … [dict(v=13200, t="計算が示した爆縮深度", c=J.LINE, disp="13,200")]
    vmax  … 棒の基準。**渡さないと、その場の最大値が満杯になる。**
            🔴 2026-08-02（r19 の一覧を目視）：c611 は「85回目と86回目は10メートル」
            なのに、10 と 10 が最大値なので**2本とも満杯の棒**になっていた。
            数字は 10 と書いてあるのに絵は「いっぱい」と言う ＝ 図が嘘をつく。
            外の基準（タイタニックの深さ 3,840m）で測ればそのまま「ほとんど無い」になる。
    ref   … その基準の名前（薄い枠で満杯の棒を1本置き、そこに書く）
    """
    n = len(items)
    gap = 40
    cw = (BW - gap * (n - 1)) / n
    # 🔴 2026-08-02（r21 の目視）：c611 の裏返しの嘘があった。
    #    値どうしが**ほとんど同じ**カットでは、棒が全部同じ長さになる。
    #    見出しは「22メートル違う」「想定より厚かった」と言うのに、
    #    絵は「まったく同じ」と言っていた（c115d 0.5%差・c423 3.5%差・c126 4.5%差）。
    #    ⚠️ これは vmax では直らない。**棒という見せ方がこの数値に合っていない**。
    #      差が5%を切ったら棒をやめ、数字に語らせる（bar=False）。
    #    ⚠️ しきい値5%は実測で決めた。c421（3,840 対 4,200＝8.6%差）は
    #      「棒の長さの差が、余裕のすべて」と言うカットで、棒が主役として効いている。
    #      10%にすると、この生きているカットまで落ちる。
    if bar and not ref:
        vs = [abs(i["v"]) for i in items if i.get("v")]
        if len(vs) >= 2 and min(vs) / max(vs) > 0.95:
            raise ValueError(
                f"compare: 値の差が {100 * (1 - min(vs) / max(vs)):.1f}% しかないので、"
                f"棒は全部同じ長さになる（図が『同じだ』と言ってしまう）。"
                f"bar=False で数字に語らせるか、ref= で外の基準を渡すこと。値={vs}")
    vmax = vmax or max(abs(i["v"]) for i in items) or 1
    top = BY0 + 34
    # ⚠️ 棒の高さ300では枠を使い切れず、値の小さい側の柱が空だった（c202 35.7%）。
    #    数字の下から枠の底まで使う。比の小さい棒も**最低限の高さ**を持たせて
    #    「柱がそこにある」ことは見せる（0.8pxの棒は消えているのと同じ）。
    # 比の一行を出すカットは、その場所も先に空けておく（あとから足すと必ずはみ出す）
    barb = BY1 - (108 if ratio else (74 if note else 34))   # 棒の底
    barh = barb - (top + 250)
    # 🔴 2026-08-04（r05 の拡大目視）：bar=False のカットは、棒の代わりに
    #    **枠いっぱいの空の板**を全項目に立てていた（旧 c208 対策）。
    #    bar=False は「棒にすると全部同じ長さに見えて、絵が『同じだ』と嘘をつく」から
    #    棒をやめた入口なのに、その代わりに置いたのが**全項目まったく同じ大きさの面**で、
    #    避けたはずの嘘がそのまま戻っていた。しかも中身が無い。
    #    実害：6カット（c107 c320 c321 c509 c510 c515）で約1分間、空の長方形が並ぶ。
    #      c320 は 19.6m² と 10m/秒 という**単位の違う2つ**が同じ大きさの板で並んでいた。
    #      c321 と c510 は項目が1つなので、空の板が1枚ぽつんと出るだけだった。
    #    → 面をやめ、**数字を大きくして空いた高さを数字自身で埋める**。
    #      「数字に語らせる」はもともとそういう意味。列は下の罫だけで作る。
    def numfit(disp, u, w, cap):
        """**数字＋単位を合わせた幅**で級数を決める。

        `num()` は単位を数字のうしろ・同じ行に置くので、数字だけで測ると
        単位のぶんだけはみ出す。cap を 112 から 208 へ上げたとき、
        c320「m/秒」と c515「時間」が実際に画面の右（1848）を越えた。
        """
        s = fm.fit(str(disp), w, "Dela", cap=cap, floor=40)
        while s > 40:
            nw = fm.width(str(disp), s, "Dela")
            uw = fm.width(u, s * 0.34, "Noto") + (s * 0.10 if u else 0)
            if nw + uw <= w:
                break
            s -= 4
        return s

    if not bar:
        _ns = max(numfit(it.get("disp") or f'{it["v"]:,}', it.get("unit", unit),
                         cw * 0.86, 208) for it in items)
        nb = (top + barb) / 2 - (130 - _ns * 0.72) / 2
    g = []
    stages = []
    for i, it in enumerate(items):
        x = BX0 + i * (cw + gap)
        c = it.get("c", J.LINE)
        disp = it.get("disp") or f'{it["v"]:,}'
        u = it.get("unit", unit)
        s = []
        if bar:
            if ref:
                # 基準の高さを薄い枠で先に見せる（棒がどれだけ小さいかが読める）
                s.append(rect(x + cw * 0.16, barb - barh, cw * 0.68, barh, "none",
                              J.LINE_DIM, 3, dash="16 12"))
            h = max(barh * 0.045, barh * abs(it["v"]) / vmax)
            s.append(rect(x + cw * 0.16, barb - h, cw * 0.68, h, c, op=0.30))
            s.append(rect(x + cw * 0.16, barb - h, cw * 0.68, h, "none", c, 4))
            s.append(line(x + cw * 0.16, barb, x + cw * 0.84, barb, c, 5))
        ns = (fm.fit(disp, cw * 0.86, "Dela", cap=112, floor=40) if bar
              else numfit(disp, u, cw * 0.86, 208))
        ny = top + 118 if bar else nb
        s.append(num(x + cw / 2, ny, disp, u, "", c, ns))
        s.append(txtfit(x + cw / 2, ny + 58, it["t"], cw * 0.98, cap=34,
                        col=J.LINE, anchor="middle"))
        if it.get("sub"):
            s.append(txtfit(x + cw / 2, ny + 100, it["sub"], cw * 0.98, cap=28,
                            col=J.TICK, anchor="middle"))
        stages.append("".join(s))
        if bar:
            g.append(line(x + cw * 0.16, barb, x + cw * 0.84, barb, J.LINE_DIM, 3))
        else:
            # 棒が無いので、柱の代わりに**下の罫だけ**を置いて列を作る。
            # 面を張らないので「どれも同じ大きさ」とは言わない。
            g.append(line(x + cw * 0.08, barb, x + cw * 0.92, barb, J.LINE_DIM, 3))
    # ⚠️ ratio と note を同じ y に置いていたので、両方あるカットで必ず重なった（c115d）。
    #    ratio は棒のすぐ下、note はいちばん下に離す。
    if ratio and n >= 2:
        g.append(txtfit(BCX, barb + 56, ratio, BW * 0.8, cap=44, col=J.AMBER,
                        anchor="middle"))
    if note:
        g.append(txtfit(BX0, BY1 - 16, note, BW, cap=28, col=J.TICK))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
#  3. quote — 引用
# ══════════════════════════════════════════════════════════
def quote(phrase, who="", when="", doc="", ctx="", to="", size=104, rows=None,
          paper=None):
    """引用カット。**この動画には引用が20カットある。作りを間違えると全部死ぬ。**

    🔴 引用の言葉そのものは、**ナレーションが読み上げ、字幕にも出ている。**
       それを図にも大きく書くと、同じ文が「音・字幕・図」で三重になる。
       画面が持つべきなのは、字幕が持てないもの＝**その言葉の出どころ**である。
         誰が（who）／誰に（to）／いつ（when）／何に書かれていたか（doc）
       図に出す言葉は**短い決め所だけ**（`phrase`）にして、文は字幕に任せる。

    ⚠️ `phrase` が長いと結局は字幕の複写になる。20字を超えたら短くする。

    rows … 🔴 2026-08-04（r02 の拡大目視）：**札の見出しと中身が合っていなかった。**
       欄が「誰が／誰に／いつ／どこに」に固定されているので、
       当てはまらない情報を無理に入れると**画面が嘘の見出しを出す**。
       11カット中8カットで起きていた。実例：
         c306「**いつ**：現役の操縦士による」　c602「**いつ**：発言そのものが確認できない」
         c339「**どこに**：機器が常に正常であれば説明できない事象ではあっても」
         CVR の5カット「**誰に**：操縦室の会話記録（CVR）に残る」（＝場所であって相手ではない）
       → `rows=[("見出し", "中身", 色), …]` を渡せば、その札の見出しごと差し替える。
          渡さなければ従来どおり。**欄に入らないものは、欄の名前のほうを変える。**
    """
    g = []
    # 出どころの札（文書 or 会話）を左に立てる
    card_x, card_y, card_w = BX0 + 20, BY0 + 30, 470
    card_h = BH - 70
    g.append(rect(card_x, card_y, card_w, card_h, J.BG2, op=0.72))
    g.append(rect(card_x, card_y, card_w, card_h, "none", J.LINE_DIM, 3))
    # 書類の角折れ。会話（doc なし）のときは吹き出しの尻尾にする。
    # ⚠️ rows= を使うと doc が空になるので、そのときは `paper=` で明示する。
    if doc if paper is None else paper:
        g.append(poly([(card_x + card_w - 74, card_y), (card_x + card_w, card_y + 74),
                       (card_x + card_w - 74, card_y + 74)], fill=J.LINE_DIM,
                      close=True, op=0.6))
    else:
        g.append(poly([(card_x + card_w, card_y + card_h * 0.42),
                       (card_x + card_w + 46, card_y + card_h * 0.50),
                       (card_x + card_w, card_y + card_h * 0.58)], fill=J.BG2,
                      close=True))
    # 🔴 2026-08-01：札の中身を上から詰めていたので、**項目が3つのカットは
    #    札の下が丸ごと空いていた**（check_box：16枠中7枠が空き矩形 33〜58%）。
    #    項目数はカットによって 2〜4 と変わるので、**空いたぶんを行間に配り直す**。
    #    ⚠️ 数字を上げるために意味のない飾りを足さない。**間隔だけを広げる。**
    fields = [(lb, v, c) for lb, v, c in
              (rows or (("誰が", who, J.INK_W), ("誰に", to, J.LINE),
                        ("いつ", when, J.LINE), ("どこに", doc, J.LINE))) if v]
    ctx_h = 0
    if ctx:
        _, y_ctx = para(0, 0, ctx, cols=int((card_w - 60) / 26), size=26)
        ctx_h = y_ctx + 40
    # ① まず既定の間隔（62）で組んで、どれだけ余るかを測る
    y = card_y + 88
    for lb, v, c in fields:
        _, y2 = para(0, y + 44, v, cols=int((card_w - 60) / 32), size=32)
        y = y2 + 62
    slack = (card_y + card_h - 34 - ctx_h) - y
    # ② 余りを項目の数で割って、行間に足す（詰まっているときは足さない）
    gap = 62 + max(0.0, slack) / max(1, len(fields))
    y = card_y + 88
    for lb, v, c in fields:
        g.append(txt(card_x + 30, y, lb, 24, J.TICK))
        body, y2 = para(card_x + 30, y + 44, v, cols=int((card_w - 60) / 32), size=32,
                        col=c)
        g.append(body)
        # 🔴 2026-08-02：札は 470×612 あるのに、値が短い項目（「CEO」など）は
        #    行の右が丸ごと空いていた（16枠中8枠が空き矩形 30〜53%・占有 11〜36%）。
        #    飾りで埋めるのではなく、**書類の罫**を引く。札は書類なのだから、
        #    罫があるほうが図として正しく、空きも横に割れる。色は DOC（書類の色）。
        g.append(line(card_x + 30, y2 + 22, card_x + card_w - 30, y2 + 22,
                      J.DOC_DIM, 2))
        y = y2 + gap
    if ctx:
        g.append(line(card_x + 30, y - 24, card_x + card_w - 30, y - 24, J.LINE_DIM, 2))
        body, _ = para(card_x + 30, y + 16, ctx, cols=int((card_w - 60) / 26), size=26,
                       col=J.TICK)
        g.append(body)
    # ══ 右に決め所 ══════════════════════════════════════
    # 🔴 2026-08-01 作り直し（r13 試写で5つ指摘）。前の作りは
    #    **1行＝1段**だったので、段はナレーションの行頭に貼られ、
    #      ① 引用を読み上げる**前**に決め所が出て、続きを予測されていた
    #      ② 行ごとに少しずつ出るので「時間差で出す」演出になっていた
    #      ③ 出ている言葉が字幕にもそのまま出て、二重表示になっていた
    #    → 決め所は段を1つにまとめる（ここは維持）。
    #
    # 🔴🔴 2026-08-03 カズヤくん指摘で**出すタイミングを変えた**。
    #    上の作りは `holds="after_last"`＝**読み終えてから**出していたが、
    #    「ナレーションが読み終わってから表示されるため、視聴者としては
    #      **何の意外性もなく意味をなしていなかった**」。
    #    → **`holds="with_last"`＝最後の行を読み"始める"のと同時**に出はじめ、
    #      その行を読み終えるころに出そろう。**声と文字が重なる。**
    #    ⚠️ 声と同時に出るぶん、その行の字幕は**消さないと二重表示になる**。
    #      `scene_jiko.SUB_MUTE` が最後の行を落とす。
    #    🔴 したがって**台本側で「決め所そのものを最後の行に置く」**必要がある。
    #      前振りを最後の行にすると、関係ない行の字幕が消える。
    px0 = card_x + card_w + 70
    pw = BX1 - px0
    g.append(txt(px0, BY0 + 150, "「", 120, J.ALERT_DIM, "Noto"))
    g.append(txt(BX1 - 46, BY1 - 40, "」", 120, J.ALERT_DIM, "Noto", "end"))
    lines = balance(phrase, 10) if isinstance(phrase, str) else list(phrase)
    # 決め所は**枠の縦を使い切る大きさ**にする。1行なら大きく、行数が増えたら詰める
    size = min(size, int((BH - 150) / max(1, len(lines)) / 1.34))
    lh = size * 1.34
    top = BY0 + (BH - len(lines) * lh) / 2 + size * 0.72
    # ⚠️ 行に分けても**1つの段にまとめる**（分けると時間差表示に戻る）
    block = "".join(txtfit(px0 + 78, top + i * lh, ln, pw - 130, cap=size,
                           col=J.INK_W)
                    for i, ln in enumerate(lines))
    # 骨格（出どころの札）は、決め所が出るまでのあいだ**ゆっくり描く**。
    # 既定の 0.30 だとカットの前半で描き終わり、そのあと画が止まる。
    return Fig("".join(g), [block],
               rect(card_x, card_y, 9, card_h, J.ALERT), (px0, BX1),
               holds=["with_last"], labk=0.62)


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
    # 🔴 2026-08-02（r21 の目視・c122）：**フチでは足りなかった。**
    #    目盛りは base、旗は stages なので、旗のほうが必ず**あとから上に**描かれる。
    #    6px のフチは細い罫には勝てても、**字の真ん中を貫く 4〜5px の軸**には勝てない。
    #    c122 は赤い軸が「18:00」のコロンを潰して「18|00」に見えていた。
    #    ⚠️ 新しく作った「図形が文字を覆う」検査もこれを通した。フチ付きの文字を
    #      無条件に「守られている」と見なしていたため（＝道具のほうの穴）。
    #    → 旗の軸のほうを、目盛りの字のところで**切る**。
    tick_boxes = []                      # (x中心, 半幅) …下向きの旗はここを避ける
    for t in (ticks or []):
        x = tx(t if not isinstance(t, (list, tuple)) else t[0])
        lb = tfmt(t) if tfmt else (t[1] if isinstance(t, (list, tuple)) else f"{t}")
        g.append(line(x, ax - 12, x, ax + 12, J.LINE_DIM, 3))
        g.append(txt(x, ax + 46, lb, 26, J.TICK, "Noto", "middle", ol=6))
        tick_boxes.append((x, fm.width(str(lb), 26, "Noto") / 2 + 5))
    LAB_T, LAB_B = ax + 46 - 26 * 0.86, ax + 46 + 26 * 0.30   # 字面の上下（実測比）
    if title:
        g.append(txtfit(BX0, BY1 - 8, title, BW, cap=30, col=J.TICK))
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
        # 下向きの旗は、目盛りの字の高さに来る。字にかかるなら軸を2本に割って
        # **字のぶんだけ空ける**（旗が目盛りの上を素通りしない）。
        cross = dy > 0 and any(abs(x - bx) < bw for bx, bw in tick_boxes)
        if cross:
            s = [line(x, ax, x, LAB_T - 4, c, 5 if big else 4),
                 line(x, LAB_B + 4, x, ax + dy * stem, c, 5 if big else 4)]
        else:
            s = [line(x, ax, x, ax + dy * stem, c, 5 if big else 4)]
        s.append(circ(x, ax, 12 if big else 8, c))
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
    # 🔴 2026-08-04（r05 の拡大目視）：時刻を持たないカット（章の橋渡し・言い換え）は
    #    `clock="—"` と書いていた。これを 232px の Dela で打つと、画面に
    #    **説明のない大きな白い横棒**が焼かれる。`c239` で「白い矩形が1個だけ浮いている」
    #    として上がったが、**同じ書き方が23カット（動画の約1割）にある**。
    # → ダッシュや空文字は「時刻が無い」の意味なので、時計を描かず label を大きく出す。
    blank = str(clock).strip() in ("", "—", "―", "-", "‐", "－", "ー")
    if blank:
        if label:
            g.append(txtfit(BX0 + 20, cy, label, BW * 0.52, cap=96, col=J.INK_W))
        g.append(line(BX0 + 20, cy + 46, BX0 + BW * 0.52, cy + 46, J.ALERT, 8))
        if sub:
            g.append(txtfit(BX0 + 20, cy + 112, sub, BW * 0.52, cap=36, col=J.TICK))
    else:
        cs = fm.fit(clock, BW * 0.54, "Dela", cap=232, floor=60)
        g.append(txt(BX0 + 20, cy, clock, cs, J.INK_W, "Dela"))
        g.append(line(BX0 + 20, cy + 46, BX0 + BW * 0.52, cy + 46, J.ALERT, 8))
        if label:
            g.append(txtfit(BX0 + 20, cy + 118, label, BW * 0.52, cap=46, col=J.AMBER))
        if sub:
            g.append(txtfit(BX0 + 20, cy + 176, sub, BW * 0.52, cap=32, col=J.TICK))
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
            g.append(txt(x, y + 38, f"{h}時", 22, J.TICK, "Noto", "middle"))
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
        g.append(txtfit(BX0, BY1 - 8, note, BW, cap=26, col=J.TICK))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
#  7. graph — XY 折れ線（第5章の核心）
# ══════════════════════════════════════════════════════════
def _emptiest_corner(series, px, py, gx0, gy0, gx1, gy1, taken=()):
    """折れ線がいちばん通っていない隅（"tl"/"tr"/"bl"/"br"）を返す。

    🔴 2026-08-02（カズヤくん指摘「graph の直線1本のカットが続く」）。
       直線1本のグラフは、線の上か下の**三角が必ず空く**。そこに何も置かないから
       「直線が1本あるだけの画」に見えていた。凡例と注記はその空いた隅に置く。
    ⚠️ どの隅が空くかは形で変わる。**推定で決めずに、線上の点を数える。**
    ⚠️ 帯（band）の見出しも隅を占める。数えないと凡例とぶつかる
       （c529 で実際にぶつかった。線だけ数えていたのが原因）。`taken` に渡す。
    """
    hw, hh = (gx1 - gx0) / 2, (gy1 - gy0) / 2
    box = {"tl": (gx0, gy0), "tr": (gx0 + hw, gy0),
           "bl": (gx0, gy0 + hh), "br": (gx0 + hw, gy0 + hh)}
    cnt = dict.fromkeys(box, 0)
    for x, y in taken:
        for nm, (bx, by) in box.items():
            if bx <= x <= bx + hw and by <= y <= by + hh:
                cnt[nm] += 200                 # 帯の見出しは線より強く隅を塞ぐ
    for s in series:
        p = [(px(a), py(b)) for a, b in s["pts"]]
        for i in range(len(p) - 1):            # 線分を刻んで、通った隅を数える
            for k in range(21):
                x = p[i][0] + (p[i + 1][0] - p[i][0]) * k / 20
                y = p[i][1] + (p[i + 1][1] - p[i][1]) * k / 20
                for nm, (bx, by) in box.items():
                    if bx <= x <= bx + hw and by <= y <= by + hh:
                        cnt[nm] += 1
    order = ["tl", "bl", "tr", "br"]           # 同点なら左上を好む（視線の始まり）
    return min(order, key=lambda k: (cnt[k], order.index(k)))


def graph(series, xlab="", ylab="", xticks=None, yticks=None, xr=(0, 1), yr=(0, 1),
          note="", legend=True, marks=None, band=None, area=False, gap=None,
          axis_map=None, x2=None):
    """折れ線グラフ。**左から描かれていく**のがこの動画の主要な動きになる。

    series … [dict(pts=[(x,y),...], t="ダイブ80", c=..., dash=None, sw=None,
                   area=True, dot=True)]
    area     … 折れ線の下を薄く塗る（系列ごとに指定してもよい）。**面を持たせる**
    gap      … (i, j) 2つの系列のあいだを塗る。**ずれそのものが主張のとき**に使う
    axis_map … [("深さ（m）", "かかる力")] 軸の対応表を空いた隅に置く
    x2       … dict(lab="", ticks=[(v, "表示")]) 第2の横軸（下にもう1本）
    """
    gx0, gx1 = BX0 + 150, BX1 - 40
    # ⚠️ 第2の横軸を出すカットは、**軸2本＋目盛り2段＋注記**が下に積まれる。
    #    高さを 96 のままにしたら 3か所ぶつかった（check_layout が実測で検出）。
    gy0, gy1 = BY0 + 46, BY1 - (200 if x2 else 96)
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
        g.append(txt(px(v), gy1 + 40, lb, 26, J.TICK, "Noto", "middle"))
    for t in (yticks or []):
        v, lb = t if isinstance(t, (list, tuple)) else (t, f"{t:,}")
        g.append(line(gx0, py(v), gx1, py(v), J.GRID, 2))
        g.append(txt(gx0 - 18, py(v) + 10, lb, 26, J.TICK, "Noto", "end"))
    for b in (band or []):
        g.append(rect(px(b["a"]), gy0, px(b["b"]) - px(b["a"]), gy1 - gy0,
                      b.get("c", J.ALERT), op=b.get("op", 0.14)))
        if b.get("t"):
            g.append(txtfit((px(b["a"]) + px(b["b"])) / 2, gy0 + 40, b["t"],
                            max(200, px(b["b"]) - px(b["a"]) + 200), cap=30,
                            col=b.get("c", J.ALERT), anchor="middle"))
    g.append(rect(gx0, gy0, gx1 - gx0, gy1 - gy0, "none", J.LINE, 4))
    if xlab:
        # 軸名はふつう右下。⚠️ 第2の横軸があるカットだけは**目盛りの行の左**へ回す
        #    （右下は第2の軸の名前が使うため）。
        if x2:
            g.append(txtfit(gx0 - 18, gy1 + 40, xlab, gx0 - BX0 - 24, cap=28,
                            col=J.LINE, anchor="end"))
        else:
            g.append(txt(gx1, gy1 + 78, xlab, 30, J.LINE, "Noto", "end"))
    if ylab:
        g.append(txt(gx0 - 18, gy0 - 16, ylab, 30, J.LINE, "Noto", "end"))
    if x2:
        # 第2の横軸。**同じ横軸が別の量でも読めること**を見せるために引く
        y2 = gy1 + 92
        g.append(line(gx0, y2, gx1, y2, J.DOC, 4))
        for v, lb in x2.get("ticks", []):
            # ⚠️ 右端の目盛りは中央寄せなので**枠の外へ出る**（実測で 1870 まで出た）。
            #    端の2つだけ内側へ寄せる。
            anch = ("end" if px(v) > gx1 - 60 else
                    ("start" if px(v) < gx0 + 60 else "middle"))
            g.append(line(px(v), y2 - 10, px(v), y2 + 10, J.DOC, 3))
            g.append(txt(px(v), y2 + 48, lb, 26, J.DOC, "Noto", anch))
        if x2.get("lab"):
            g.append(txt(gx1, y2 - 18, x2["lab"], 28, J.DOC, "Noto", "end"))
    if note:
        g.append(txtfit(BX0, BY1 - 8, note, BW, cap=26, col=J.TICK))

    # 凡例・対応表は**線が通っていない隅**に置く（直線1本のカットの空きを埋める）
    taken = [((px(b["a"]) + px(b["b"])) / 2, gy0 + 40)
             for b in (band or []) if b.get("t")]
    corner = _emptiest_corner(series, px, py, gx0, gy0, gx1, gy1, taken)
    lft = corner in ("tl", "bl")
    top_c = corner in ("tl", "tr")
    lx = (gx0 + 26) if lft else (gx1 - 26)
    anch = "start" if lft else "end"
    nleg = sum(1 for s in series if legend and s.get("t"))
    ly = (gy0 + 48) if top_c else (gy1 - 34 - 44 * (nleg - 1))

    stages = []
    if axis_map:
        # 軸の意味の対応表。「別の図と軸がそろっている」ことは、線では言えない
        ax = gx0 + 40 if lft else gx1 - 40 - 470
        ay = gy0 + 56 if top_c else gy1 - 56 - 62 * len(axis_map)
        s = [rect(ax - 22, ay - 52, 514, 62 * len(axis_map) + 46, J.BG, J.DOC_DIM, 3,
                  rx=8, op=0.86)]
        for i, (a, b) in enumerate(axis_map):
            yy = ay + 62 * i
            s.append(txtfit(ax, yy, a, 240, cap=32, col=J.LINE))
            s.append(txt(ax + 258, yy, "＝", 30, J.DOC, "Noto", "middle"))
            s.append(txtfit(ax + 296, yy, b, 190, cap=32, col=J.DOC))
        stages.append("".join(s))
        # ⚠️ 対応表と凡例は同じ隅に来る。**凡例を対応表の下へ押し下げる**
        #    （ぶつけたまま焼くと、対応表の枠の中に凡例の字が入る）
        if top_c:
            ly = ay + 62 * len(axis_map) + 30
        else:
            ly = ay - 62 - 44 * nleg
    if gap and len(series) > max(gap):
        a, b = series[gap[0]], series[gap[1]]
        # 🔴 2026-08-02（r21 の目視・c531）：2本の x の範囲がずれていると、
        #    塗りが**端で閉じて**「そこだけ差がゼロ」に見える。c531 は
        #    片方が 3,600 で終わっていたので、いちばん深いところで2本が
        #    1点に合流した絵になり、注記「どの深さでも上へずれる」と
        #    真っ向から食い違っていた。**塗りは端を勝手に閉じる**ので気付きにくい。
        ax_, bx_ = [p[0] for p in a["pts"]], [p[0] for p in b["pts"]]
        if abs(ax_[0] - bx_[0]) > 1e-6 or abs(ax_[-1] - bx_[-1]) > 1e-6:
            raise ValueError(
                f"graph(gap=): 塗る2本の x の範囲が違う（{ax_[0]}〜{ax_[-1]} と "
                f"{bx_[0]}〜{bx_[-1]}）。端で塗りが閉じて『差がゼロ』に見える。"
                f"両方を同じ x まで伸ばすこと。")
        pa = [(px(u), py(v)) for u, v in a["pts"]]
        pb = [(px(u), py(v)) for u, v in b["pts"]]
        stages.append(poly(pa + list(reversed(pb)),
                           fill=b.get("c", J.ALERT), close=True, op=0.20))
    for s in series:
        c = s.get("c", J.LINE)
        pts = [(px(a), py(b)) for a, b in s["pts"]]
        seg = []
        if s.get("area", area):
            # 折れ線の下を塗る。**装飾ではなく「そこまで積み上がった量」**を面で読ませる
            seg.append(poly(pts + [(pts[-1][0], py(y0)), (pts[0][0], py(y0))],
                            fill=c, close=True, op=0.14))
        if not s.get("dots_only"):
            seg.append(poly(pts, stroke=c, sw=s.get("sw", 6), dash=s.get("dash")))
        if s.get("dot") or s.get("dots_only"):
            seg += [circ(x, y, s.get("dotr", 7), c) for x, y in pts]
        if legend and s.get("t"):
            # ⚠️ 凡例は**その系列の描かれ方**を出す。点だけの系列に実線を出すと
            #    凡例が嘘になる（r19 の目視で c527 に出た）。
            # ⚠️ 凡例の下を折れ線が通ることがある（c525 で実測）。**地を敷いてから**置く
            lw_ = 64 + fm.width(str(s["t"]), 30, "Noto") + 16
            seg.append(rect(lx - (10 if lft else lw_ - 10), ly - 34, lw_, 46,
                            J.BG, rx=6, op=0.82))
            if s.get("dots_only"):
                seg += [circ(lx + (12 + k * 19 if lft else -12 - k * 19), ly - 10,
                             6, c) for k in range(3)]
            else:
                seg.append(line(lx, ly - 10, lx + (50 if lft else -50), ly - 10, c,
                                6, dash=s.get("dash")))
            seg.append(txtfit(lx + (64 if lft else -64), ly, s["t"], 460, cap=30,
                              col=c, anchor=anch))
            ly += 44
        stages.append("".join(seg))
    for m in (marks or []):
        # dx/dy/anchor … 近い2点に印を打つカット（c525）は、そのままだと札が重なる
        mx, my = px(m["x"]), py(m["y"])
        a = m.get("anchor", "start")
        stages.append(circ(mx, my, 14, "none", m.get("c", J.ALERT), 5)
                      + txtfit(mx + m.get("dx", 26), my + m.get("dy", -18),
                               m.get("t", ""), 460, cap=32,
                               col=m.get("c", J.ALERT), anchor=a))
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
            g.append(txt(gx0 - 26, y + 10, f"{d:,}", 24, J.TICK, "Noto", "end"))
        g.append(txt(gx0 - 26, top + 34, ylab, 24, J.TICK, "Noto", "end"))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.TICK))
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
    g.append(txt(gx0 - 26, bot + 40, "潜航", 24, J.TICK, "Noto", "end"))
    return Fig("".join(g), stages, hot, (gx0 - 40, gx1))


# ══════════════════════════════════════════════════════════
#  9. layers — 積層（剥離・空隙・接着面）
# ══════════════════════════════════════════════════════════
def layers(n=5, bonds=None, delam=None, voids=None, note="", labels=True,
           split=None, dims=None, bondlab="", fiber=True):
    """重なった板の断面。

    bonds … 面の番号(1..n-1)に注記 [dict(i=1, t="1-2", c=..., big=True)]
    delam … 剥離させる面の番号
    voids … 空隙を描く面の番号
    labels … True なら「1層」「2層」…／**文字列のリストを渡すとその名前**になる
    bondlab … 面そのものの凡例（右下）。**渡さなければ出さない**
    fiber … 層の中に繊維の向きの細線を引くか

    🔴 2026-08-04（r01 の拡大目視）：`labels=True` に
       **「接着剤の面」という凡例が焼き込まれていた。**
       123便の c231・c332 は**断熱材**のカットで、接着剤は関係が無い。
       しかも同じ緑帯を、カット側が渡した「断熱材の面」と、
       この凡例の「接着剤の面」の**両方が指していて矛盾**していた。
       段も「1層/2層/3層/4層」の無名のままで、1本目の積層の見た目が残っていた。
    → 凡例は `bondlab`、段の名前は `labels` のリストでカット側から渡す。
    """
    # 段に名前を付けるときは、左の余白を広げる。
    # ⚠️ 190px は「1層」（2字）ぶんしか無く、名前を入れると txtfit が
    #    14px まで潰して読めなくなる（推定で置かず、字幅から逆算した）。
    gut = 330 if isinstance(labels, (list, tuple)) else 190
    x0, x1 = BX0 + gut, BX1 - 240
    # ⚠️ 62+16 だと5層で374pxしかなく、枠(682)の下半分が空いた（c415 空き40.7%）。
    #    層は「厚み」を見せる図なので、**枠の縦を使い切る厚さ**にする。
    bt = 22                                # 接着面の厚み
    lh = (BH - 150 - bt * (n - 1)) / n     # 1層の厚み（枠から逆算）
    tot = n * lh + (n - 1) * bt
    top = BY0 + 62
    g = []
    y = top
    ys = []
    names = labels if isinstance(labels, (list, tuple)) else None
    if names is not None and len(names) != n:
        raise ValueError(f"layers: labels の数が層の数と合っていません "
                         f"（labels={len(names)} / n={n}）")
    for i in range(n):
        g.append(rect(x0, y, x1 - x0, lh, J.LINE, op=0.20))
        g.append(rect(x0, y, x1 - x0, lh, "none", J.LINE, 4))
        # 繊維の向きが分かるよう細い線を入れる（層であることが一目で分かる）
        if fiber:
            for k in range(1, 6):
                g.append(line(x0 + 6, y + lh * k / 6, x1 - 6, y + lh * k / 6,
                              J.LINE_DIM, 1.6))
        if names is not None:
            # 名前は「1層」より長いので、左の余白（190px）に収まるまで詰める
            g.append(txtfit(x0 - 22, y + lh / 2 + 12, names[i], x0 - BX0 - 30,
                            cap=34, col=J.LINE, anchor="end"))
        elif labels:
            g.append(txt(x0 - 22, y + lh / 2 + 13, f"{i + 1}層", 34, J.LINE,
                         "Noto", "end"))
        ys.append(y)
        y += lh
        if i < n - 1:
            g.append(rect(x0, y, x1 - x0, bt, J.OK, op=0.55))
            y += bt
    if bondlab:
        g.append(txt(x1 + 16, top + tot + 44, bondlab, 28, J.OK))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.TICK))

    def bond_y(i):
        """接着面 i（**1 が 1層と2層のあいだ**）の y。

        🔴 2026-08-02（r21 の目視で3人が同じ指摘）：ここが **0 始まり**だったのに、
           docstring も章ファイルも **1 始まり**で書かれていた。結果：
             ・c431 c432 c625 … 「1-2」の札が付いた赤帯が **2層と3層のあいだ**に、
               「3-4」の札が **4層と5層のあいだ**に描かれていた。
               ＝**この動画の結論そのもの**（1-2面と3-4面が剥離した）が
                 1層ずれた場所を指していた。
             ・c428 … voids=[1,2,3,4] の 4 が範囲外で、**積層の下**に空隙の帯が
               1本はみ出していた（5層なら接着面は4つしかない）。
           実測：lh=88.8 / bt=22 / top=272 のとき、旧 bond_y(1)=471.6 で
           これは 2層(382.8-471.6) と 3層(493.6-582.4) のあいだ。
        """
        if not 1 <= i <= n - 1:
            raise ValueError(
                f"layers: 接着面の番号は 1〜{n - 1}（1 が1層と2層のあいだ）。i={i}")
        return top + (i - 1) * (lh + bt) + lh

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
#  形の根拠：NTSB/MIR-25-36 **図3（外形図・内部図）を画素で実測**（2026-08-02）。
#  `ref/ntsb_titan_MIR2536.pdf` の 12 ページ目から図を取り出して測った。
#
#  🔴 2026-08-02：前の版は**自分で書いた実測メモと実装が食い違っていた**。
#     コメントには「ドーム突出 / 外径 = 約 0.55」と書いてあるのに、
#     実装は `A{R*0.62} {R}`（＝突出 / 外径 0.31）で、**ドームが半分の厚みしか
#     無かった**。r5 の目視で出ていた「ドームが平らに見えて形が崩れた」の正体がこれ。
#     さらに **尾部コーンが1本も描かれていなかった**。実機は尾部コーンが
#     全長の3割を占める最大の外形要素なので、無いと「タイタンに見えない」。
#
#  ■ 図3から測った値（画素・1737×1946 の取り出し画像）
#      耐圧殻 上端 y=1272 / 下端 y=1641      → 直径 369px（半径 185）
#      円筒部（チタンリングのあいだ）x 700〜1340 → 640px
#      前ドームの頂点 x≒1520 ／ 後ドームの頂点 x≒505
#      → 円筒長/耐圧殻長 = 640/1015 = 0.63
#         ドーム突出/半径 = 180/185 = 0.97、195/185 = 1.05  ＝**ほぼ半球**
#      機体全長（尾部コーンの先〜のぞき窓）≒1535px
#      → 耐圧殻長/全長 = 0.66 ／ 半径/全長 = 0.121
#  ■ 実機との突き合わせ
#      全長22フィート＝6.7m、円筒部 8.1フィート＝2.47m、外径 約1.7m。
#      全長/直径 = 3.94 に対し、図3の実測は 4.15。図の見出しにも
#      「scale approximate」とあるので、**図3の比を採る**（作図の下敷きは図3）。
#  ⚠️ 向きは**機首を左**にする（`icons` の潜水艇の絵と同じ向きにそろえる）。
#     図3 は機首が右なので、左右を反転して起こしてある。
TT_L = 1520.0            # 画面上の全長（既定・尾部コーンの先まで含む）
TT_R = 0.121             # 半径 / 全長
TT_NOSE = 0.026          # のぞき窓の出っぱりぶん（機首の余白）
TT_CYL = 0.417           # 円筒長 / 全長
TT_DOME = 0.97           # ドーム突出 / 半径（＝ほぼ半球）


def titan(mode="side", s=1.0, cx=None, cy=None, marks=None, note="",
          bolts=False, window=False, cut=False):
    """潜水艇の側面／断面。marks は [dict(at="cyl"|"fore"|"aft"|"ring", t=..., c=...)]。

    mode … "side"（外形）／"section"（縦断面。中の人と耐圧殻が見える）
    """
    L = TT_L * s
    cx = BCX if cx is None else cx
    cy = (BY0 + BH * 0.44) if cy is None else cy
    R = L * TT_R                       # 外径の半分（図3の実測 半径/全長 = 0.121）
    cyl = L * TT_CYL                   # 円筒部の長さ
    x0 = cx - L / 2                    # 機首（のぞき窓の外面）側の端
    dm = R * TT_DOME                   # ドームの突出（ほぼ半球）
    xc0 = x0 + L * TT_NOSE + dm        # 円筒の前端（前のチタンリング）
    xc1 = xc0 + cyl                    # 円筒の後端（後のチタンリング）
    xhull = xc1 + dm                   # 後ドームの頂点
    xtail = x0 + L                     # 尾部コーンの先
    g = []
    # ── 尾部コーン。**全長の3割を占める最大の外形要素**（前の版には無かった）──
    #    図3どおり、上の縁は船体の上面線をそのまま延ばし、下の縁が持ち上がる。
    #    塗らずに輪郭だけにする（図3も輪郭だけで描かれている）。
    g.append(f'<path d="M{xc1:.1f} {cy - R:.1f} L{xtail:.1f} {cy - R * 0.96:.1f} '
             f'C{xtail - L * 0.11:.1f} {cy + R * 0.12:.1f} '
             f'{xc1 + L * 0.16:.1f} {cy + R:.1f} '
             f'{xc1 + L * 0.02:.1f} {cy + R:.1f}" fill="{J.BG2}" opacity="0.45" '
             f'stroke="{J.LINE}" stroke-width="4" stroke-linejoin="round"/>')
    # 外形：前後のドーム＋円筒（＝耐圧殻。ここだけが圧力を受ける本体）
    body = (f'M{xc0:.1f} {cy - R:.1f} H{xc1:.1f} '
            f'A{dm:.1f} {R:.1f} 0 0 1 {xc1:.1f} {cy + R:.1f} '
            f'H{xc0:.1f} A{dm:.1f} {R:.1f} 0 0 1 {xc0:.1f} {cy - R:.1f} Z')
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
        # 🔴 2026-08-02（r21 の目視・c533）：**丸＋縦棒だと「人」に見えない。**
        #    黄色い丸から線が下がった形が5つ並ぶので、ひずみ計やセンサーの
        #    印のように読めた（このカットは「そのひずみ計」の話をしているので、
        #    印だと思うと数が合わなくなる）。
        #    → people 型と同じ人型（`_glyph`）を使い、絵の語彙をそろえる。
        for i in range(5):
            px_ = xc0 + cyl * (0.17 + i * 0.165)
            g.append(_glyph("person", px_, cy + R * 0.28, R * 0.86, J.AMBER))
    else:
        g.append(f'<path d="{body}" fill="{J.BG2}" stroke="{J.INK_W}" '
                 f'stroke-width="5"/>')
    # チタンのリング（円筒の両端）
    for x in (xc0, xc1):
        g.append(rect(x - L * 0.012, cy - R * 1.04, L * 0.024, R * 2.08, J.AMBER,
                      op=0.55))
        g.append(rect(x - L * 0.012, cy - R * 1.04, L * 0.024, R * 2.08, "none",
                      J.AMBER, 3))
    # 推進器。図3では**円筒の上**と**船体の後ろ端**に付いている。
    # ⚠️ 前の版は船体から離して置いていたので**宙に浮いた灰色の四角**に見えた
    #    （r8 の目視。titan を使う14カット全部に出ていた）。船体に接して描く。
    # 🔴 r19 の目視：後ろの1つを `cy + R*0.30` に置いたら**船体の中**に入り、
    #    ハッチのように見えた。図3どおり**後ドームの頂点から後ろへ**出す。
    g.append(rect(xc0 + cyl * 0.62 - L * 0.016, cy - R - L * 0.030,
                  L * 0.032, L * 0.030, J.LINE, J.LINE, 3, op=0.6))
    g.append(rect(xc0 + cyl * 0.62 - L * 0.024, cy - R - L * 0.042,
                  L * 0.048, L * 0.012, J.LINE, J.LINE, 3, op=0.6))
    g.append(rect(xhull - L * 0.004, cy - L * 0.016, L * 0.030, L * 0.032,
                  J.LINE, J.LINE, 3, op=0.6))
    g.append(rect(xhull + L * 0.026, cy - L * 0.024, L * 0.012, L * 0.048,
                  J.LINE, J.LINE, 3, op=0.6))
    # 着底フレーム。図3どおり、2本の柱と1本のそり
    fy = cy + R + L * 0.055
    for px_ in (xc0, xc1):
        g.append(rect(px_ - L * 0.006, cy + R, L * 0.012, fy - cy - R, J.LINE_DIM,
                      op=0.85))
    g.append(rect(xc0 - L * 0.05, fy, (xc1 - xc0) + L * 0.10, L * 0.014,
                  J.LINE_DIM, op=0.85))
    if window:
        # のぞき窓。**前ドームの頂点に付く出っぱり**（宙に浮かせない）
        g.append(rect(x0 + L * 0.004, cy - R * 0.30, L * 0.024, R * 0.60, J.BG2,
                      J.OK, 4, rx=6))
        g.append(circ(x0 + L * 0.026, cy, R * 0.22, J.BG, J.OK, 5))
    if bolts:
        # 🔴 2026-08-02（r25 の目視）：**10個しか描いていなかった。**
        #    使っているのは c205 ただ1カットで、その画面には「18 本」と大きく出ていて
        #    ナレーションも「18本のボルトで留められる」と言う。
        #    数えられる絵で数が合わないのは、図が嘘をつくのと同じ。
        #    → `bolts=True` は 18、数を渡せばその数を描く。
        #    リングを真横から見ているので、点は縦1列に並ぶ（x はほとんど動かない）。
        #    ⚠️ 数が増えると点が重なるので、**半径は間隔から決める**（推定で置かない）。
        n_b = 18 if bolts is True else int(bolts)
        span = R * 0.92 * 2                      # 上端から下端までの実距離
        r_b = max(3.0, min(7.0, span / n_b * 0.42))
        for i in range(n_b):
            a = math.pi * (i / (n_b - 1.0)) - math.pi / 2
            g.append(circ(xc0 + math.cos(a) * 6, cy + math.sin(a) * R * 0.92, r_b,
                          J.AMBER))
    if cut:
        mid = (xc0 + xc1) / 2
        g.append(line(mid, cy - R * 1.5, mid, cy + R * 1.5, J.ALERT, 4, dash="16 10"))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.TICK))

    xmid = (xc0 + xc1) / 2
    anchor = {"fore": (x0 + L * TT_NOSE + dm * 0.45, cy), "aft": (xhull - dm * 0.45, cy),
              "cyl": (xmid, cy - R), "cylb": (xmid, cy + R),
              "ring": (xc0, cy - R), "ring2": (xc1, cy - R),
              "win": (x0 + L * 0.026, cy)}
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
    #    （c109 c115 など17カット全部）。そこで**枠の縦を使い切る**ようにしたが、
    # 🔴 2026-08-01（r14 を焼いて目視）：今度は**箱の中**が空洞になっていた。
    #    字を大きくしても埋まらない。**箱の高さが中身の3倍ある**のが原因だった
    #    （中身は「見出し＋説明1行」だけ。48枠のうち41枠は値を持たない）。
    #    → **中身を先に測って箱をその高さに合わせ、枠の縦の中央に置く。**
    #    ⚠️ 数字を埋めるために飾りを足さない。器のほうを中身に合わせる。
    top0 = BY0 + 62
    bh_max = BY1 - top0 - (78 if note else 34)
    # 🔴 2026-08-02：箱の高さは中身から出していたのに、**中身の置き場所は
    #    箱の割合（bh*0.30 / 0.48 / 0.88）**で決めていた。だから高さを詰めても
    #    中身は箱の上のほうに固まったままで、下が空いた（check_box：48枠中12枠が
    #    空き矩形 32〜55%・文字の下が 39〜58% 空洞）。
    #    → **中身の高さを段ごとに積算し、その積算どおりの絶対位置に置く。**
    PAD_T, GAP1, LH, GAP2, PAD_B = 40.0, 24.0, 58.0, 28.0, 34.0

    def _mm(st):
        """その段の (見出しの級数, 説明の行, 値の級数, 中身の高さ)。"""
        ts = fm.fit(str(st["t"]), cw - 40, "Noto", cap=84, floor=18)
        lines = wrap(str(st["d"]), max(6, int((cw - 40) / 42))) if st.get("d") else []
        vs = fm.fit(str(st["v"]), cw - 40, "Dela", cap=124) if st.get("v") else 0
        h = PAD_T + ts + PAD_B
        if lines:
            h += GAP1 + LH * len(lines)
        if vs:
            h += GAP2 + vs
        return ts, lines, vs, h

    mm = [_mm(st) for st in steps]
    bh = max(230.0, min(bh_max, max(m[3] for m in mm)))
    # ⚠️ 幅も中身から抑える。段が2つのカットは1枠 836px あり、
    #    中身が「機械」（248px）だけの段は左右がまとめて空いた（実測 35%）。
    each = []
    for (ts_, dl_, vs_, _), st in zip(mm, steps):
        n_ = fm.width(str(st["t"]), ts_, "Noto")
        for ln in dl_:
            n_ = max(n_, fm.width(ln, 42, "Noto"))
        if vs_:
            n_ = max(n_, fm.width(str(st["v"]), vs_, "Dela"))
        each.append(n_ + 60)
    # ⚠️ 下限（360）を先に効かせてはいけない。段が5つのカット（c414）は
    #    枠いっぱいでも1枠 272px しかないので、360 を下限にすると**列が枠から溢れる**
    #    （実測：左が -124px、右が 2003px）。**必ず元の幅で頭打ちにする。**
    cw = min(cw, max(360.0, min(max(each) + 90, max(min(each) * 2.0, 360.0))))
    # 🔴 2026-08-02（r21 の目視・c407）：**級数を測ったあとに箱を詰めていた。**
    #    `_mm` は「そのときの cw」に合わせて字を詰めるので、あとから cw を
    #    小さくすると、**字はもとの幅のまま**になり箱からはみ出す。
    #    c407 は 796px 幅で測った「幅0.5インチ」（694px）を 616px の箱に入れて
    #    いたので、左右に 39px ずつ溢れていた。
    #    ⚠️ check_layout は「画面から出ているか」しか見ないので、
    #      **箱から出ているだけ**のはみ出しは通ってしまう。
    #    → 幅を決め直したら、級数と高さを**測り直す**。
    mm = [_mm(st) for st in steps]
    bh = max(230.0, min(bh_max, max(m[3] for m in mm)))
    top = top0 + (bh_max - bh) / 2
    x_left = BCX - (cw * cols + (gap + aw) * (cols - 1)) / 2   # 詰めた列を中央に
    g = []
    stages = []
    for i, st in enumerate(steps):
        x = x_left + i * (cw + gap + aw)
        c = st.get("c", J.LINE)
        ts, dlines, vs, ch = mm[i]
        s = [rect(x, top, cw, bh, c, op=0.14), rect(x, top, cw, bh, "none", c, 4)]
        if numbered:
            s.append(circ(x + 34, top - 2, 26, J.BG, c, 4))
            s.append(txt(x + 34, top + 12, i + 1, 34, c, "Dela", "middle"))
        # 段ごとの中身を、その段の高さぶんだけ**箱の縦中央に置く**。
        # 1920×1080 で見出し48pxは小さすぎるので上限は 84 のまま
        # （`fm.fit` が幅に合わせて縮めるので、長い見出しは今までどおり）。
        cy = top + (bh - ch) / 2
        yy = cy + PAD_T + ts * 0.78
        s.append(txt(x + cw / 2, yy, st["t"], ts, J.INK_W, "Noto", "middle"))
        yy = cy + PAD_T + ts
        if dlines:
            yy += GAP1
            for ln in dlines:
                s.append(txt(x + cw / 2, yy + 42 * 0.78, ln, 42, J.LINE, "Noto",
                             "middle"))
                yy += LH
        if vs:
            yy += GAP2
            s.append(txt(x + cw / 2, yy + vs * 0.78, st["v"], vs, c, "Dela",
                         "middle"))
        if i < n - 1:
            s.append(arrow(x + cw + 12, top + bh * 0.42, x + cw + gap + aw - 12,
                           top + bh * 0.42, J.LINE_DIM, 5, 22))
        stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 8, note, BW, cap=30, col=J.TICK))
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
        # 🔴 2026-08-04：**k の幅を実測して本文の左端を決める。**
        #    それまで「150px あれば足りる」と決め打っていたので、
        #    k が2文字以上のカットで**本文が k の上に乗った**（123便で45件検出）。
        #    k は "1" のような1桁とはかぎらない（"噂" "原文" "2.13.1" など）。
        #    ⚠️ 幅は**実際に使う書体**で測る。`numfam()` が数字を含まない文字列を
        #      Noto に落とすので、Dela 固定で測ると漢字の k を測り違える。
        ks = min(72, h * 0.46)
        kw = max((fm.width(str(b["k"]), ks, numfam(str(b["k"]), "Dela"))
                  for b in blocks if b.get("k")), default=0.0)
        kcol = 34 + (kw + 40 if kw else 0)
        for i, b in enumerate(blocks):
            y = top + i * h
            c = b.get("c", J.LINE)
            s = [rect(BX0, y, 9, h - 22, c)]
            if b.get("k"):
                s.append(txt(BX0 + 34, y + h * 0.52, b["k"], ks, c, "Dela"))
            tx0 = BX0 + (kcol if b.get("k") else 34)
            # ⚠️ v の場所（右540px）を、v が無いときまで空けていた。
            rsv = 540 if b.get("v") else 0
            avail = BX1 - tx0 - rsv
            # 🔴 器を広げても**中身が短いカットは埋まらない**（c208「圧縮」の2字など）。
            #    1行で収まる短い文は、幅を使い切る級数まで上げる。
            #    34分をスマホで見る動画なので、字が大きいこと自体が読みやすさになる。
            one = fm.fit(str(b["t"]), avail, "Noto", cap=int(min(96, h * 0.52)),
                         floor=16)
            bs = one if fm.width(str(b["t"]), one, "Noto") <= avail else                 min(52, h * 0.34)
            # 🔴 2026-08-04：**折り返したときの高さを見ていなかった。**
            #    本文は「幅に収まる級数」だけで決めていたので、2行に折れると
            #    2行目が段の外（＝いちばん下の段では枠の外）へ落ちた。
            #    → 行数を数えて、段の真ん中で上下に振り分ける。
            #      それでも収まらなければ級数を落とす（幅ではなく**高さ**で決める）。
            nl = len(wrap(str(b["t"]), max(6, int(avail / bs))))
            while nl > 1 and nl * bs * 1.5 > h * 0.86 and bs > 18:
                bs *= 0.88
                nl = len(wrap(str(b["t"]), max(6, int(avail / bs))))
            body, _ = para(tx0, y + h * 0.52 - (nl - 1) * bs * 0.75, b["t"],
                           cols=max(6, int(avail / bs)), size=bs, col=J.INK_W)
            s.append(body)
            if b.get("v"):
                s.append(txt(BX1, y + h * 0.54, b["v"],
                             fm.fit(b["v"], 500, "Dela", cap=min(76, h * 0.50)),
                             c, "Dela", "end"))
            stages.append("".join(s))
    else:
        # 🔴 2026-08-01 作り直し（r13「要点の4項目が小さい。要点なので大きく」）。
        #    4件以上（または長文）だとこちらの格子に落ちるが、**本文が34px固定**だった。
        #    1920×1080 で 873×321 のセルに 34px は小さすぎる。
        #    ⚠️ ここは結論・要点を出す場所なので、**いちばん大きく出てよい**。
        #    → セルの大きさから級数を決め、`v`（数値）も出せるようにする。
        cols = max(1, min(cols, n))          # 件数より多い列を作らない（ep09 が2件で3列だった）
        rows = max(1, math.ceil(n / cols))
        cw = (BW - 30 * (cols - 1)) / cols
        rh = (BY1 - top - (44 if note else 0)) / rows
        for i, b in enumerate(blocks):
            x = BX0 + (i % cols) * (cw + 30)
            y = top + (i // cols) * rh
            c = b.get("c", J.LINE)
            s = [line(x, y, x + cw - 20, y, c, 5)]
            kx = 0
            if b.get("k"):
                ks = min(84, rh * 0.34)
                # 🔴 ここも「1文字ぶん（ks×1.5）で足りる」と決め打っていた。実測する。
                s.append(txt(x, y + ks * 0.92, b["k"], ks, c, "Dela"))
                kx = fm.width(str(b["k"]), ks, numfam(str(b["k"]), "Dela")) + ks * 0.5
            # 数値は右下に置く。場所は数値があるときだけ空ける
            vs = min(96, rh * 0.34) if b.get("v") else 0
            avail = cw - 20 - kx
            bs = fm.fit(str(b["t"]), avail, "Noto",
                        cap=int(min(72, rh * 0.26)), floor=18)
            body, _ = para(x + kx, y + (rh * 0.30 if b.get("k") else rh * 0.26),
                           b["t"], cols=max(6, int(avail / bs)), size=bs,
                           col=J.INK_W)
            s.append(body)
            if b.get("v"):
                s.append(txt(x + cw - 20, y + rh * 0.86, b["v"],
                             fm.fit(str(b["v"]), cw * 0.6, "Dela", cap=int(vs)),
                             c, "Dela", "end"))
            stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.TICK))
    return Fig("".join(g), stages, "", (BX0, BX1))


# ══════════════════════════════════════════════════════════
# 13. absent — 「無い」ことを見せる
# ══════════════════════════════════════════════════════════
def _tick_mark(x, y, r, col):
    """✓。「有る」側にだけ付ける。"""
    return poly([(x - r, y), (x - r * 0.25, y + r * 0.72), (x + r, y - r * 0.80)],
                stroke=col, sw=max(5, r * 0.42))


def _cross_mark(x, y, r, col):
    """✗。**小さく打つ。** 大きな✗は「無い」ものをいちばん重く見せてしまう。"""
    return (line(x - r, y - r, x + r, y + r, col, max(4, r * 0.38))
            + line(x + r, y - r, x - r, y + r, col, max(4, r * 0.38)))


def _absent_ledger(items, lead, note):
    """台帳の行が空欄。**制度・登録・記録が「そこに書かれていない」**ことを見せる。

    構図は**横に長い行が縦に積まれる**（他の3つの見せ方と重ならないように）。
    記入欄は「有る」なら実線の枠に値が入り、「無い」なら破線の枠が空のまま。
    """
    n = len(items)
    top = BY0 + (100 if lead else 26)
    bot = BY1 - (54 if note else 12)
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 64, lead, BW - 40, cap=46, col=J.INK_W))
        g.append(line(BX0, BY0 + 82, BX1, BY0 + 82, J.DOC, 4))
    rh = (bot - top) / n
    # 記入欄の幅は**いちばん長い結果の文字から実測**して決める（推定で置かない）
    res = [str(it.get("d") or ("有り" if it.get("ok") else "無し")) for it in items]
    rs = min(48, min(fm.fit(t, 520, "Noto", cap=48, floor=26) for t in res))
    ew = max(fm.width(t, rs, "Noto") for t in res) + 150      # ✓／✗ と左右の余白
    ew = min(ew, BW * 0.44)
    ex = BX1 - ew
    eh = min(140.0, rh * 0.52)
    # 用紙の罫（骨格）。行の切れ目をここで作っておく
    for i in range(n):
        g.append(line(BX0, top + (i + 1) * rh - rh * 0.04, BX1,
                      top + (i + 1) * rh - rh * 0.04, J.DOC_DIM, 2))
    stages = []
    for i, it in enumerate(items):
        ok = it.get("ok", False)
        c = J.OK if ok else J.ALERT
        cy = top + rh * (i + 0.5) - rh * 0.02
        s = [txt(BX0 + 4, cy + rh * 0.10, f"{i + 1}", min(40, rh * 0.20), J.DOC,
                 "Dela")]
        # 項目名。**行の高さから級数を決める**（1920×1080 で小さい字は読めない）
        # `c` を渡すとその色で出る（制度・第三者機関の名前は J.INST）
        ns = int(min(96, rh * 0.42))
        ns = fm.fit(str(it["t"]), ex - BX0 - 120, "Noto", cap=ns, floor=20)
        s.append(txt(BX0 + 62, cy + rh * 0.12, it["t"], ns, it.get("c", J.INK_W)))
        # 🔴 r19 の目視：項目名の右端から記入欄まで 1,100px 空いていた。
        #    目次と同じ**点リーダー**で結ぶ。台帳という見立てにも合う。
        lead_x0 = BX0 + 62 + fm.width(str(it["t"]), ns, "Noto") + 40
        if ex - 30 - lead_x0 > 80:
            s.append(line(lead_x0, cy + rh * 0.12 - ns * 0.22, ex - 30,
                          cy + rh * 0.12 - ns * 0.22, J.DOC_DIM, 4, dash="4 20"))
        # 記入欄
        if ok:
            s.append(rect(ex, cy - eh / 2, ew, eh, J.OK, J.OK, 4, rx=8, op=0.14))
        else:
            # 🔴 「無い」側は**塗らない・網掛けにしない**。破線の枠が空のまま、が正しい
            s.append(rect(ex, cy - eh / 2, ew, eh, "none", J.LINE_DIM, 4, rx=8,
                          dash="18 12"))
        mr = min(20.0, eh * 0.20)
        s.append(_tick_mark(ex + 46, cy, mr, c) if ok
                 else _cross_mark(ex + 46, cy, mr, c))
        s.append(txt(ex + 46 + mr + 26, cy + rs * 0.36, res[i], rs, c))
        stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.TICK))
    return Fig("".join(g), stages, "", (BX0, BX1))


def _absent_seat(items, lead, note):
    """並んだ席のうち、空いているものがある。**候補を当たって、当てはまらない。**

    構図は**棚の上に小さな器が横に並ぶ**。器は台帳より小さく、名前は棚の下。
    「有る」器だけが中身（記録の帯）を持ち、「無い」器は破線の輪郭だけ。
    """
    n = len(items)
    lead_h = 92 if lead else 24
    note_h = 46 if note else 6
    top = BY0 + lead_h
    bot = BY1 - note_h
    # 下に名前と補足を置くぶんを先に取る（あとから足すと必ずはみ出す）
    has_d = any(it.get("d") for it in items)
    cap_h = 56 + (64 if has_d else 0)
    shelf = bot - cap_h
    # ⚠️ 340 で頭打ちにしていたので、器の上に 100px 以上の空きが残った（r19 の目視）。
    #    棚の上は全部使う。
    bh = max(180.0, shelf - top - 12)
    slot = BW / n
    bw = min(slot * 0.74, 400.0)
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 62, lead, BW, cap=48, col=J.INK_W))
    # 棚。器がそこに「置かれている」ことを作る線
    g.append(line(BX0, shelf, BX1, shelf, J.LINE, 5))
    stages = []
    for i, it in enumerate(items):
        cx = BX0 + slot * (i + 0.5)
        ok = it.get("ok", False)
        c = J.OK if ok else J.ALERT
        x, y = cx - bw / 2, shelf - bh
        s = []
        # 🔴 有る／無いの差は「器の中身」で見せる。**同じ場所に同じ数の段**を置き、
        #    有るほうは詰まっていて、無いほうは段だけが破線で残っている。
        #    （r19 の目視：空の器の中に短い破線が1本だけあって意味不明だった）
        # ⚠️ ✓／✗ は**器の中の上**に置く。器の外（上）に出したら、器を高くしたぶん
        #    枕の文字に重なった（r20 の目視。機械は文字どうししか見ないので出ない）。
        mr = min(24.0, bh * 0.11)
        s0 = y + mr * 2 + 34
        step = (y + bh - 22 - s0) / 5
        slots = [(s0 + step * k, min(step * 0.60, bh * 0.085)) for k in range(5)]
        if ok:
            s.append(rect(x, y, bw, bh, J.OK, J.OK, 4, rx=6, op=0.16))
            for by, hh in slots:
                s.append(rect(x + bw * 0.12, by, bw * 0.76, hh, J.OK, op=0.55))
            s.append(_tick_mark(cx, y + mr + 16, mr * 0.9, c))
        else:
            # 空の器。**破線の輪郭と、空のままの段だけ**。網掛けも塗りも入れない
            s.append(rect(x, y, bw, bh, "none", J.LINE_DIM, 4, rx=6, dash="20 14"))
            for by, hh in slots:
                s.append(rect(x + bw * 0.12, by, bw * 0.76, hh, "none", J.LINE_DIM,
                              2, dash="12 10"))
            s.append(_cross_mark(cx, y + mr + 16, mr, c))
        s.append(txtfit(cx, shelf + 50, it["t"], slot * 0.96, cap=40,
                        col=it.get("c", c), anchor="middle"))
        if it.get("d"):
            sub, _ = para(cx, shelf + 100, it["d"], cols=max(6, int(slot / 30)),
                          size=30, col=J.TICK, anchor="middle")
            s.append(sub)
        stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.TICK))
    return Fig("".join(g), stages, "", (BX0, BX1))


def _absent_single(items, lead, note):
    """1件だけ。**箱を作らない。**

    🔴 2026-08-02 カズヤくん指摘「1項目だけの c612 は箱が巨大で空」。
       件数が1でも横一列の器を1つ作っていたので、幅1,776px の箱が
       中身ゼロで居座っていた。1件のときは器そのものをやめる。
       構図は**左に大きな見出し、右に空欄の罫、その上に斜めの判**。
    """
    it = items[0]
    ok = it.get("ok", False)
    c = J.OK if ok else J.ALERT
    g = []
    # 🔴 r19 の目視：上半分だけを使っていて、下 300px が丸ごと空いていた。
    #    枠（210〜892）の**縦を使い切る**ように置き直す。
    top = BY0 + (76 if lead else 24)
    bot = BY1 - (48 if note else 16)
    mid = (top + bot) / 2
    if lead:
        g.append(txtfit(BX0, BY0 + 56, lead, BW * 0.7, cap=36, col=J.TICK))
    ts = fm.fit(str(it["t"]), BW * 0.44, "Dela", cap=150, floor=52)
    g.append(txt(BX0 + 10, mid + ts * 0.30, it["t"], ts, J.INK_W, "Dela"))
    g.append(line(BX0 + 10, mid + ts * 0.30 + 46,
                  BX0 + 10 + fm.width(str(it["t"]), ts, "Dela"),
                  mid + ts * 0.30 + 46, c, 8))
    # 右：本来そこに記録が入るはずだった欄。**罫だけを引いて、何も書かない**
    fx = BX0 + BW * 0.50
    fw = BX1 - fx
    g.append(txt(fx, top + 34, "記録", 30, J.DOC))
    rows = 5
    step = (bot - top - 70) / rows
    for k in range(rows):
        g.append(line(fx, top + 70 + step * (k + 0.5), BX1,
                      top + 70 + step * (k + 0.5), J.DOC_DIM, 3, dash="20 14"))
    stages = []
    # 斜めの判。空欄の上を横切らせる（「ここは埋まらなかった」を1枚で言う）
    d = str(it.get("d") or ("有り" if ok else "無し"))
    ds = fm.fit(d, fw - 190, "Dela", cap=104, floor=40)
    dw = fm.width(d, ds, "Dela")
    scx, scy = fx + fw / 2, mid
    bw_, bh_ = dw + 130, ds * 1.66
    stages.append(
        f'<g transform="rotate(-7 {scx:.0f} {scy:.0f})">'
        + rect(scx - bw_ / 2, scy - bh_ / 2, bw_, bh_, J.BG, c, 7, rx=12)
        + txt(scx, scy + ds * 0.36, d, ds, c, "Dela", "middle")
        + '</g>')
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.TICK))
    return Fig("".join(g), stages, "", (BX0, BX1), labk=0.52)


def _absent_pair(items, lead, note):
    """有る側と無い側を2枚で比べる。**数が出せるときは数で比べる。**

    構図は左右2枚。⚠️ 矢印でつながない（前→後の変化ではなく、同時の対比なので）。
    """
    a, b = items[0], items[1]
    if a.get("ok") is not True and b.get("ok") is True:
        a, b = b, a                          # 「有る」側を必ず左に置く
    cw = (BW - 120) / 2
    lead_h = 84 if lead else 20
    top = BY0 + lead_h
    bot = BY1 - (48 if note else 10)
    cap_h = 52 + (62 if (a.get("d") or b.get("d")) else 0)
    # ⚠️ 372 で頭打ちにしていたので下が空いた（r19 の目視）。枠の縦を使い切る。
    bh = max(220.0, bot - cap_h - top)
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 58, lead, BW, cap=46, col=J.INK_W))
    # 対比の軸（中央の縦罫）。矢印にしない
    g.append(line(BCX, top, BCX, top + bh + 26, J.LINE_DIM, 3, dash="16 12"))
    stages = []
    for i, side in enumerate((a, b)):
        x = BX0 + i * (cw + 120)
        ok = side.get("ok", False)
        c = J.OK if ok else J.ALERT
        nn = side.get("n")
        s = []
        if ok:
            s.append(rect(x, top, cw, bh, J.OK, J.OK, 4, rx=8, op=0.14))
            # 中身を「個」で見せる。n が無ければ記録の帯で埋める
            if isinstance(nn, int) and 0 < nn <= 24:
                cols = min(nn, 5)
                rows = math.ceil(nn / cols)
                uw = min(cw / (cols + 1), bh / (rows + 2.2))
                ox = x + cw / 2 - uw * cols / 2
                oy = top + bh * 0.34 - uw * (rows - 1) / 2
                for k in range(nn):
                    s.append(circ(ox + uw * (k % cols) + uw / 2,
                                  oy + uw * (k // cols), uw * 0.30, J.OK))
            else:
                for k in range(5):
                    s.append(rect(x + cw * 0.12, top + bh * (0.16 + k * 0.13),
                                  cw * 0.76, bh * 0.07, J.OK, op=0.55))
        else:
            # 🔴 「無い」側は破線の輪郭と、**有る側と同じ場所の空の枠**だけ。塗らない
            s.append(rect(x, top, cw, bh, "none", J.LINE_DIM, 4, rx=8, dash="20 14"))
            # 有る側と同じ場所に、同じ数の**空の枠**を置く。さらに上下に空の罫を渡して
            # 「欄はあるのに、どこにも入っていない」を見せる
            # （r19 の目視＋check_box：丸だけだと箱の中が 11% しか埋まらなかった）。
            oc = a.get("n") if isinstance(a.get("n"), int) else 0
            for k in (0.16, 0.60):
                s.append(line(x + cw * 0.14, top + bh * k, x + cw * 0.86,
                              top + bh * k, J.LINE_DIM, 3, dash="14 10"))
            if 0 < oc <= 24:
                cols = min(oc, 5)
                rows = math.ceil(oc / cols)
                uw = min(cw / (cols + 1), bh / (rows + 2.2))
                ox = x + cw / 2 - uw * cols / 2
                oy = top + bh * 0.34 - uw * (rows - 1) / 2
                for k in range(oc):
                    s.append(circ(ox + uw * (k % cols) + uw / 2,
                                  oy + uw * (k // cols), uw * 0.30, "none",
                                  J.LINE_DIM, 3))
            else:
                s.append(line(x + cw * 0.14, top + bh * 0.38, x + cw * 0.86,
                              top + bh * 0.38, J.LINE_DIM, 3, dash="14 10"))
        if isinstance(nn, int):
            s.append(num(x + cw / 2, top + bh - 44, f"{nn}", side.get("unit", ""),
                         "", c, min(132, bh * 0.36)))
        elif not ok:
            s.append(_cross_mark(x + cw / 2, top + bh * 0.62, 34, c))
        s.append(txtfit(x + cw / 2, top + bh + 52, side["t"], cw + 40, cap=42,
                        col=c, anchor="middle"))
        if side.get("d"):
            sub, _ = para(x + cw / 2, top + bh + 104, side["d"],
                          cols=max(6, int(cw / 30)), size=30, col=J.TICK,
                          anchor="middle")
            s.append(sub)
        stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.TICK))
    return Fig("".join(g), stages, "", (BX0, BX1))


def absent(items, lead="", note="", mode=None):
    """「無い」ことを見せる。**無いものを重く描かない。**

    🔴 2026-08-02 作り直し（カズヤくん指摘「大きな網掛け＋✗が並ぶだけで単調。
       とくに1項目だけの c612 は箱が巨大で空」）。前の作りは16カットすべてが
       **網掛けの大きな箱＋巨大な✗**で、しかも「無い」ものがいちばん重く見えていた。
       図としても嘘で、無いものはそこに大きな塊としては無い。

    → 作り直しの原則（4つの見せ方に共通）
       **「無い」側は破線と罫だけ。実体（塗り・中身）を持つのは「有る」側だけ。**
       網掛け（`hatch`）はこの型では使わない。

    mode … "ledger" 台帳の行が空欄（制度・登録・記録が無い）＝横長の行が縦に積まれる
           "seat"   棚に並んだ器のうち空いている（候補を当たって当てはまらない）
           "single" 1件だけ（大きな見出し＋空欄の罫＋斜めの判）＝器を作らない
           "pair"   有る側と無い側を数で比べる（2件のとき）
           省略時は件数と ok の有無で自動で選ぶ。
    ⚠️ **同じ章で見せ方が続かないように、カット側で mode を名指しする**
       （自動任せにすると第6章の6カットが全部 ledger になる）。
    """
    items = list(items)
    n = len(items)
    if not mode:
        oks = sum(1 for it in items if it.get("ok"))
        mode = ("single" if n <= 1 else
                "pair" if (n == 2 and oks == 1) else
                "seat" if oks else "ledger")
    fn = {"ledger": _absent_ledger, "seat": _absent_seat,
          "single": _absent_single, "pair": _absent_pair}.get(mode)
    if fn is None:
        raise ValueError(f"absent の mode が不正です: {mode}")
    if mode == "single" and n != 1:
        raise ValueError(f"absent(mode='single') は1件のときだけ（いまは {n} 件）")
    if mode == "pair" and n != 2:
        raise ValueError(f"absent(mode='pair') は2件のときだけ（いまは {n} 件）")
    # 🔴 2026-08-02（r21 の目視）：**「有る」側が1つも無い seat / pair は画が空になる。**
    #    「無い側は破線と罫だけ」という原則を、有る側が存在しないカットに当てると、
    #    画面が破線の輪郭だけになって「作りかけ」に見える。実例：
    #      c224（2件）… 大きな破線の器が2つ、中の段も破線、✗が小さく浮くだけ
    #      c636（3件）… 同じ器が3つ並び、名前の下は3つとも「従っていない」
    #      c608（2件）… 同上
    #    ⚠️ ledger は同じ「全部無い」でも読めた（c230 c602 c630 c640）。
    #      **項目名が大きく左に立ち、点リーダーと記入欄が紙の骨格を作る**から。
    #      器の中身で語る seat と、行で語る ledger の差。
    #    → 有る側が無いなら seat/pair は使わせない。ledger へ倒す。
    if mode in ("seat", "pair") and not any(it.get("ok") for it in items):
        raise ValueError(
            f"absent(mode='{mode}') は「有る」側が1つ以上要る（いまは全部『無い』）。"
            f"全部『無い』なら mode='ledger' を使う（項目名で見せる）。")
    return fn(items, lead, note)


# ══════════════════════════════════════════════════════════
# 14. icons — 個数を絵で見せる
# ══════════════════════════════════════════════════════════
def icons(n, on=None, kind="dot", cols=None, lead="", note="", oncol=None,
          offcol=None, labels=None, offkind=None):
    """n 個のうち on 個（または on のリスト）を強調する。

    kind    … "dot"／"person"／"ship"／"sub"／"plane"
    offkind … **強調しない側だけ形を変える**（省略時は kind と同じ）

    🔴 2026-08-02（r21 の目視・c133）：`kind` が1つしか無かったので、
       「船11隻、航空機4機」のカットが **15個ぜんぶ船の絵**になっていた。
       注記には「灰色が航空機4機」と書いてあるので、**図が嘘をついていた**。
       色を変えるだけでは種類の違いは出ない。形が違うものは形で分ける。
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
        kind_i = kind if i in on else (offkind or kind)
        if kind_i == "plane":
            # 上から見た機体。胴＋後退翼＋尾翼（船と**輪郭で**見分けが付く形）
            cur.append(poly([(x, y - r * 0.95), (x + r * 0.16, y - r * 0.30),
                             (x + r * 0.16, y + r * 0.42), (x, y + r * 0.72),
                             (x - r * 0.16, y + r * 0.42),
                             (x - r * 0.16, y - r * 0.30)], fill=c, close=True))
            cur.append(poly([(x, y - r * 0.18), (x + r, y + r * 0.34),
                             (x + r, y + r * 0.54), (x, y + r * 0.22),
                             (x - r, y + r * 0.54), (x - r, y + r * 0.34)],
                            fill=c, close=True))
            cur.append(poly([(x, y + r * 0.44), (x + r * 0.40, y + r * 0.76),
                             (x + r * 0.40, y + r * 0.90), (x, y + r * 0.72),
                             (x - r * 0.40, y + r * 0.90),
                             (x - r * 0.40, y + r * 0.76)], fill=c, close=True))
        elif kind_i == "person":
            cur.append(circ(x, y, r * 0.52, c))
            cur.append(poly([(x - r * 0.62, y + r * 1.9), (x - r * 0.62, y + r * 0.95),
                             (x, y + r * 0.62), (x + r * 0.62, y + r * 0.95),
                             (x + r * 0.62, y + r * 1.9)], fill=c, close=True))
        elif kind_i == "ship":
            cur.append(poly([(x - r, y), (x + r, y), (x + r * 0.62, y + r * 0.72),
                             (x - r * 0.62, y + r * 0.72)], fill=c, close=True))
            cur.append(rect(x - r * 0.20, y - r * 0.86, r * 0.40, r * 0.86, c))
        elif kind_i == "sub":
            # 🔴 2026-08-01（r14 を焼いて目視）：角丸の棒を1本置いていただけなので、
            #    9隻・49回のカットが**ただの棒の列**に見えていた。潜水艇の形にする。
            #    前が丸く、後ろが細くなり、上に小さなフィン、前にのぞき窓。
            hh = r * 0.42
            cur.append(poly([(x - r, y), (x - r * 0.90, y - hh * 0.80),
                             (x + r * 0.26, y - hh), (x + r * 0.70, y - hh * 0.56),
                             (x + r, y - hh * 0.22), (x + r, y + hh * 0.22),
                             (x + r * 0.70, y + hh * 0.56), (x + r * 0.26, y + hh),
                             (x - r * 0.90, y + hh * 0.80)], fill=c, close=True))
            cur.append(poly([(x + r * 0.30, y - hh), (x + r * 0.54, y - hh * 1.86),
                             (x + r * 0.72, y - hh * 1.86), (x + r * 0.62, y - hh)],
                            fill=c, close=True))
            cur.append(circ(x - r * 0.62, y, hh * 0.34, J.BG))
        else:
            cur.append(circ(x, y, r * 0.62, c))
        if labels and i < len(labels):
            cur.append(txtfit(x, y + r * 2.3, labels[i], cw * 0.98,
                              cap=max(24, int(cw * 0.20)), col=c, anchor="middle"))
    stages.append("".join(cur))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.TICK))
    return Fig("".join(g), stages, "", (x0 - 20, x0 + cw * cols + 20))


# ══════════════════════════════════════════════════════════
# 15. sound — 2点で同じ音を聞いた（プロローグと第5章の核心）
# ══════════════════════════════════════════════════════════
def sound(depth_m=3840, note="", rings=4, both=True, label_a="潜水艇の中",
          label_b="海面のボート", moving="浮上中", scene="sea",
          caption="同じ音を、同じときに"):
    """1つの音が2点に届いたことを見せる。**2点同時**が要点。

    scene … "sea"    海面のボートと潜水艇（1本目）
            "record" 海を描かない。**2つの記録**を並べる（123便 c111）

    🔴 2026-08-02（r25 の目視）：`浮上中` を**この型に焼き込んでいた**。
       c115c は降下中の爆縮なので、図が「浮上中」と言い台本が「降下」と言っていた。
    → 向きはカット側から渡す。`moving=""` を渡せば矢印ごと消える。

    🔴 2026-08-04（r01 の拡大目視）：**上の直しでは足りていなかった。**
       123便の c111（高度24,000ft・上昇中の旅客機）に、
       **海のグラデーション地・水面線・船のシルエット・カプセル型の潜水艇・
       上向きの矢印「浮上中」**がそのまま描かれていた。
       語を1つ外に出しても、**絵そのものが1本目の事実を焼き込んでいれば同じこと**。
    → 海の道具立てごと `scene` で切り替える。
    """
    top, bot = BY0 + 70, BY1 - 60
    g = []
    if scene == "sea":
        g += [watertone(BX0, top, BW, bot - top, 0.08, 0.40),
              line(BX0, top, BX1, top, J.INK_W, 5)]
        bx, by = BCX - 380, top
        sx, sy = BCX + 240, top + (bot - top) * 0.52
        # 海面のボート
        g.append(poly([(bx - 74, by), (bx + 74, by),
                       (bx + 48, by - 34), (bx - 48, by - 34)],
                      fill=J.INK_W, close=True))
    else:
        # 記録どうし。海も乗り物も描かない。**同じ高さに並べる**
        # （上下に置くと「深さ」の意味が生まれてしまう）。
        # ⚠️ 0.30 に置いたら、輪の中心が上がって**いちばん外の輪の頂点が y≈80**
        #    ＝見出しの帯まで届いた（r02 の目視。c111 はたまたま見出しの右を通った）。
        #    輪は oy から半径 504 まで伸びるので、oy は 700 より下に置く。
        bx, by = BCX - 380, top + (bot - top) * 0.42
        sx, sy = BCX + 240, by
        for cx_ in (bx, sx):
            g.append(rect(cx_ - 122, by - 78, 244, 156, J.BG2, op=0.80, rx=8))
            g.append(rect(cx_ - 122, by - 78, 244, 156, "none", J.DOC, 4, rx=8))
            # 書類の角折れ
            g.append(poly([(cx_ + 122 - 46, by - 78), (cx_ + 122, by - 78 + 46),
                           (cx_ + 122 - 46, by - 78 + 46)],
                          fill=J.DOC, close=True, op=0.55))
            for k in range(1, 5):
                g.append(line(cx_ - 86, by - 40 + k * 28, cx_ + 60, by - 40 + k * 28,
                              J.DOC, 3))
    # 🔴 2026-08-02（r28 の拡大目視）：**音の輪が札の後ろを通る**ので、
    #    赤い線が字にかかって読みづらい。ep08 は札を短くしても、いちばん外の輪が
    #    「中」を横切っていた。輪は画面いっぱいに広がるので、**避ける場所が無い**。
    #    → 札にフチを付けて地から浮かせる（写真の上で読ませるのと同じ手）。
    g.append(txtfit(bx, by - (60 if scene == "sea" else 104), label_b, 460, cap=32,
                    col=J.INK_W, anchor="middle", ol=7))
    if scene == "sea":
        # 潜水艇
        g.append(rect(sx - 92, sy - 34, 184, 68, J.INK_W, rx=34))
    g.append(txtfit(sx, sy + (82 if scene == "sea" else 122), label_a, 460, cap=32,
                    col=J.INK_W, anchor="middle", ol=7))
    if moving and scene == "sea":
        # 札だけ替えると絵と逆になるので、矢印の向きも変える。
        # ⚠️ 下向きでも**場所は艇の上のまま**にする。艇の下は label_a（水深）が
        #    使っており、そこへ矢印を下ろすと図形が文字を貫く。
        up = moving != "降下中"
        y0, y1 = (sy - 54, sy - 130) if up else (sy - 130, sy - 54)
        g.append(arrow(sx, y0, sx, y1, J.LINE, 4, 16))
        g.append(txt(sx + 16, sy - 96, moving, 28, J.LINE, ol=6))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.TICK))
    stages = []
    ox, oy = (bx + sx) / 2, sy + 150
    for k in range(rings):
        r = 120 + k * 128
        stages.append(f'<path d="M{ox - r:.0f} {oy:.0f} A{r} {r} 0 0 1 '
                      f'{ox + r:.0f} {oy:.0f}" fill="none" stroke="{J.ALERT}" '
                      f'stroke-width="{6 - k * 0.8:.1f}" opacity="{0.95 - k * 0.16:.2f}"/>')
    if both:
        stages.append(circ(bx, by - (4 if scene == "sea" else 0), 22, "none",
                           J.ALERT, 5)
                      + circ(sx, sy, 22, "none", J.ALERT, 5)
                      + txtfit(BCX, bot + 6, caption, BW * 0.7, cap=40,
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
    g.append(txt(x0, y + h + 62, "0", 30, J.TICK, "Dela"))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.TICK))
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
def mapfig(points, note="", link=None, scale=None, lead="", coast=None, turn=None):
    """位置関係の略図。points=[dict(x=0.2,y=0.3,t="大島",c=...,kind=)]

    x,y は本体枠に対する 0〜1。**地図の正確さではなく位置関係だけを持たせる。**

    🔴 2026-08-04（r05 の拡大目視）：**「位置関係だけ」は方角まで免れる断りではない。**
       note に「縮尺は正確ではない」と書いてあるので角度の狂いは断ってあるつもりでいたが、
       **上下・左右の向きそのものが逆**になっていたカットが3枚あった。
       これは縮尺の話ではなく、図が事実と食い違っている（README §2 の最優先）。

       | カット | 描いていたもの | 報告書 |
       |---|---|---|
       | `c124` | 123便を横田の**南東**に置いていた | 「横田TACANから**305度**、35海里の地点に火災」＝**西北西** |
       | `c127` | 山中を大月市の**南西**に置いていた | 「奥多摩町付近上空から左へ変針し**西北西**に向かって」 |
       | `c115` | 大島を異常発生地点の**北**に置いていた | 大島は南（東京コントロールの指示は針路90度＝東） |

       → 決めた約束：**縮尺と角度は約束しない。上下（南北）と左右（東西）の
         「どちら側か」だけは必ず合わせる。** 置く前に一次資料で向きを確かめる。

    turn … dict(at=0, t="約3分間でほぼ360度", r=86, side="below")
       その点の上で旋回したことを、時計回りの破線の輪で見せる。
       ⚠️ 見出しが「大きく旋回」と言っているのに図が直線1本だと、
          **図が見出しを支えていない**（c127 が実際にそうだった）。

    🔴 2026-08-04（r01 の拡大目視）：**1本目（タイタン号）の
       「ニューファンドランドの島影」とラベルを、この型に焼き込んでいた。**
       123便の6カット（c101 c115 c124 c127 c521 c611）すべてに描かれていて、
       羽田→大阪の便も、東伊豆町も、大阪の事業所も、
       **ニューファンドランドの隣**に置かれていた。
       README §0-4「型に事実を焼き込まない」そのもの。**題材が変わると必ず嘘になる。**
    → 陸はカット側から渡す。渡さなければ描かない（既定）。

    coast … dict(x=0.30, t="陸（伊豆半島）", side="left")
       ⚠️ **海岸線の「形」は描かない。** 記憶で海岸線を描くと必ず形が狂うので、
          陸と海の境を **1本の直線**で示すだけにする。x は 0〜1。
    """
    x0, y0 = BX0 + 40, BY0 + 40
    w, h = BW - 80, BH - 110
    g = [rect(x0, y0, w, h, J.BG2, op=0.55), rect(x0, y0, w, h, "none", J.LINE_DIM, 3)]
    # 地紋（緯線・経線）
    for i in range(1, 8):
        g.append(line(x0, y0 + h * i / 8, x0 + w, y0 + h * i / 8, J.GRID, 2))
    for i in range(1, 10):
        g.append(line(x0 + w * i / 10, y0, x0 + w * i / 10, y0 + h, J.GRID, 2))
    if coast:
        cx_ = x0 + w * coast.get("x", 0.30)
        left = coast.get("side", "left") == "left"
        lx, lw = (x0, cx_ - x0) if left else (cx_, x0 + w - cx_)
        g.append(rect(lx, y0, lw, h, J.LINE_DIM, op=0.42))
        g.append(line(cx_, y0, cx_, y0 + h, J.LINE_DIM, 4))
        if coast.get("t"):
            g.append(txtfit(lx + lw / 2, y0 + h - 24, coast["t"],
                            max(140, lw - 24), cap=26, col=J.TICK, anchor="middle"))
    if lead:
        g.append(txtfit(BX0, BY0 + 16, lead, BW, cap=40, col=J.INK_W))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.TICK))

    def P(p):
        return (x0 + w * p["x"], y0 + h * p["y"])

    stages = []
    if link and len(points) >= 2:
        a, b = P(points[link[0]]), P(points[link[1]])
        s = [poly([a, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 60), b],
                  stroke=J.AMBER, sw=5, dash="18 12")]
        if scale:
            # 🔴 2026-08-04（r03 の拡大目視）：札を経路の頂点の 16px 上に置いていたが、
            #    経路は a →（中点の60px上）→ b の**折れ線**なので、
            #    b が頂点より上にあるカットでは、右半分の線が**札の文字を貫く**
            #    （c127「ここから山の中へ入っていった」の後ろ4字が取り消し線に見えた）。
            #    ⚠️ check_layout の「図形が文字を横切る」は層をまたぐと見えない（既知の穴）。
            # → ①折れ線のいちばん高いところより上へ置く ②フチを付けて線の上で読ませる
            #    （音の輪と同じ手。README §15 の「札にフチを付けて地から浮かせる」）。
            # 🔴 2026-08-04（r06）：逃がし幅 22px では足りなかった。点の札は
            #    点の 12px 下に 34px の級数で出るので、22px だとちょうど接する
            #    （c124 で接触、c127 では重なった）。46px 空ける。
            top_y = min(a[1], b[1], (a[1] + b[1]) / 2 - 60)
            s.append(txtfit((a[0] + b[0]) / 2, max(y0 + 46, top_y - 46), scale, 620,
                            cap=34, col=J.AMBER, anchor="middle", ol=7))
        stages.append("".join(s))
    if turn and 0 <= turn.get("at", 0) < len(points):
        cx, cy = P(points[turn.get("at", 0)])
        r = turn.get("r", 84)
        # 時計回り（右旋回）。画面は y が下向きなので、角度を増やすと時計回りに回る。
        # 1周ぶん閉じずに 0.88 周だけ描いて、終わりに矢印を付ける（向きが読める）。
        a0 = -math.pi / 2
        a1 = a0 + 2 * math.pi * turn.get("frac", 0.88)
        pts = [(cx + r * math.cos(a0 + (a1 - a0) * k / 48),
                cy + r * math.sin(a0 + (a1 - a0) * k / 48)) for k in range(49)]
        s = [poly(pts, stroke=J.AMBER, sw=5, dash="18 12"),
             arrow(*pts[-2], *pts[-1], J.AMBER, 5, 24)]
        if turn.get("t"):
            side = turn.get("side", "below")
            ty = cy + r + 46 if side == "below" else cy - r - 24
            s.append(txtfit(cx, min(ty, y0 + h - 12), turn["t"], 620, cap=32,
                            col=J.AMBER, anchor="middle", ol=7))
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
                            cap=26, col=J.TICK, anchor=anch))
        stages.append("".join(s))
    return Fig("".join(g), stages, "", (x0, x0 + w))


# ══════════════════════════════════════════════════════════
# 18. people — 人と組織のあいだで起きたこと
# ══════════════════════════════════════════════════════════
def _glyph(kind, cx, cy, s, col):
    """節の中に置く小さな絵。**箱に名前が書いてあるだけの図にしない。**

    kind … "person" 人 ／ "org" 組織・機関 ／ "doc" 書類・記録 ／ "part" 物・部品
    """
    if kind == "person":
        return (circ(cx, cy - s * 0.26, s * 0.22, col)
                + poly([(cx - s * 0.40, cy + s * 0.46), (cx - s * 0.40, cy + s * 0.10),
                        (cx, cy - s * 0.06), (cx + s * 0.40, cy + s * 0.10),
                        (cx + s * 0.40, cy + s * 0.46)], fill=col, close=True))
    if kind == "org":
        # 建物。屋根の帯＋窓の列（24pxでも「組織」と読める形にする）
        g = [rect(cx - s * 0.46, cy - s * 0.34, s * 0.92, s * 0.14, col, rx=3),
             rect(cx - s * 0.40, cy - s * 0.16, s * 0.80, s * 0.62, "none", col, 4)]
        for k in range(3):
            g.append(rect(cx - s * 0.26 + k * s * 0.26, cy - s * 0.02, s * 0.13,
                          s * 0.30, col, op=0.75))
        return "".join(g)
    if kind == "doc":
        # 書類。角を折る＋本文の罫3本
        w_, h_ = s * 0.66, s * 0.86
        x_, y_ = cx - w_ / 2, cy - h_ / 2
        g = [poly([(x_, y_), (x_ + w_ - s * 0.20, y_), (x_ + w_, y_ + s * 0.20),
                   (x_ + w_, y_ + h_), (x_, y_ + h_)], fill="none", stroke=col,
                  sw=4, close=True)]
        for k in range(3):
            g.append(line(x_ + s * 0.10, y_ + s * 0.42 + k * s * 0.17,
                          x_ + w_ - s * 0.10, y_ + s * 0.42 + k * s * 0.17, col, 3))
        return "".join(g)
    if kind == "part":
        # 物・部品（耐圧殻・模型）。円筒の側面
        return (rect(cx - s * 0.44, cy - s * 0.22, s * 0.88, s * 0.44, "none", col,
                     4, rx=s * 0.20)
                + line(cx - s * 0.16, cy - s * 0.22, cx - s * 0.16, cy + s * 0.22,
                       col, 3)
                + line(cx + s * 0.16, cy - s * 0.22, cx + s * 0.16, cy + s * 0.22,
                       col, 3))
    return ""


def _box_edge(cx, cy, bw, bh, tx, ty):
    """(cx,cy) の箱の**縁**のうち、(tx,ty) へ向かう向きにある点を返す。

    🔴 前は `bw*0.5` `bh*0.62` と楕円で近似していたので、矢印の根元が
       箱の中に食い込んだり、離れて浮いたりしていた（11カット全部）。
       「関係が読み取れない」の一因はここ。矩形なら交点は式で出る。
    """
    dx, dy = tx - cx, ty - cy
    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
        return (cx, cy)
    t = min(bw / 2 / abs(dx) if dx else 1e9, bh / 2 / abs(dy) if dy else 1e9)
    return (cx + dx * t, cy + dy * t)


def people(nodes, edges=None, note="", lead=""):
    """人・組織のあいだで起きたこと。第3章の解雇の連鎖に使う。

    nodes … [dict(x=0.1, y=0.3, t="海洋運用部長", d="", c=..., kind="person")]
    edges … [dict(a=0, b=1, t="1月19日 会話", c=...)]

    🔴 2026-08-02 作り直し（カズヤくん指摘「people がスカスカ」）。
       前は箱が **460×140 の固定**で、11カット中8カットは節が2つしか無い。
       1,736×532 の枠に小さな箱が2つ浮いているだけで、占有は 14% しかなかった。
       ⚠️ ただ大きくすると節どうしがぶつかる（位置はカット側が決めている）。
       → **ぶつからない最大の大きさを二分探索で出す**（推定で置かない）。
       あわせて ①矢印を箱の縁にきっちり当てる ②節に小さな絵を入れる
       （kind）ので、「箱に名前が書いてあるだけ」の図ではなくなる。
    """
    x0, y0 = BX0 + 20, BY0 + (76 if lead else 30)
    w = BW - 40
    h = (BY1 - (46 if note else 8)) - y0

    # 🔴 2026-08-02（r21 の目視）：節が**同じ高さに並ぶ**カットは、かたまりが
    #    帯の上のほうに置かれ、**下半分が丸ごと空いていた**（c215 c310 c316 c320 c401）。
    #    check_space も同じものを「x0〜1920 の帯が 22〜30% 空き」と出していたが、
    #    163件の並びに埋もれて読めていなかった。
    #    → 節のかたまりの中心を、帯の縦の中心へ寄せる。
    #    ⚠️ 位置はカット側が決めているので、**relative な並びは変えない**
    #      （ずらすのはかたまり全体。節どうしの上下関係は保つ）。
    _ys = [n["y"] for n in nodes]
    _shift = 0.5 - (min(_ys) + max(_ys)) / 2

    def C(i):
        n = nodes[i]
        return (x0 + w * n["x"], y0 + h * (n["y"] + _shift))

    # ── 節の大きさ ───────────────────────────────────────────
    # 🔴 高さは**中身から決める**（process と beforeafter で学んだのと同じ）。
    #    最初は幅も高さもいっしょに大きくしたら、`check_box` が people 26枠のうち
    #    16枠を「空き矩形 32〜33%」で落とした。**器だけ大きくしても中は埋まらない。**
    #    → 高さは 絵＋名前＋補足 の実寸に合わせ、**幅だけ**ぶつからない最大を探す。
    GS = 118.0                                   # 節の中に置く絵の大きさ
    PADY = 36.0
    # 🔴 節が1段しか無いカット（横に2つ並ぶだけ）は、縦に 640px 使えるのに
    #    190px の箱を置いていた。中心に寄せても**上下に 230px ずつ余る**。
    #    → 段が1つのときだけ、絵と字を大きくして箱ごと持ち上げる。
    #    ⚠️ 器だけ大きくしても中は埋まらない（people の作り直しで学んだ）。
    #      **絵の大きさ GS を上げる**＝中身が育つので、箱の高さは中身から出たまま。
    #    ⚠️ 段が2つ以上あるカットでは触らない（節どうしがぶつかる）。
    if max(_ys) - min(_ys) < 0.02:
        GS = min(190.0, (h - 96) * 0.42)
    TS_CAP = 56.0 * min(1.5, GS / 118.0)         # 名前の級数も絵に合わせる
    DS_CAP = 34.0 * min(1.5, GS / 118.0)
    PADY = PADY * min(1.4, GS / 118.0)
    bh = GS + PADY * 2
    if all(not n.get("d") for n in nodes):
        bh = GS + PADY * 1.7
    # 幅の上限は**いちばん中身が長い節**から出す。無闇に広げると、名前が短い節
    # （「2号殻」「NTSB」）の左右が穴になる（check_box が実測で落とした）。
    need = 0.0
    for n in nodes:
        gs_ = GS if n.get("kind") else 0.0
        need = max(need, 52 + (gs_ + 26 if gs_ else 0)
                   + max(fm.width(str(n["t"]), TS_CAP, "Noto"),
                         fm.width(str(n.get("d", "")), DS_CAP, "Noto")))
    BW_MAX, PAD = max(380.0, min(780.0, need + 200)), 44.0

    def fits(bw_):
        for i in range(len(nodes)):
            ax, ay = C(i)
            if not (BX0 <= ax - bw_ / 2 and ax + bw_ / 2 <= BX1):
                return False
            if not (y0 - 10 <= ay - bh / 2 and ay + bh / 2 <= y0 + h + 10):
                return False
            for j in range(i + 1, len(nodes)):
                bx, by = C(j)
                if (abs(ax - bx) < bw_ + PAD) and (abs(ay - by) < bh + PAD):
                    return False
        return True

    lo, hi = 300.0, BW_MAX
    if not fits(lo):
        hi = lo                                  # どうしても入らない配置は最小で置く
    else:
        for _ in range(26):
            mid = (lo + hi) / 2
            if fits(mid):
                lo = mid
            else:
                hi = mid
    bw = lo
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 62, lead, BW, cap=44, col=J.INK_W))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.TICK))

    stages = []
    for e in (edges or []):
        a, b = C(e["a"]), C(e["b"])
        c = e.get("c", J.LINE)
        a2 = _box_edge(a[0], a[1], bw + 16, bh + 16, b[0], b[1])
        b2 = _box_edge(b[0], b[1], bw + 30, bh + 30, a[0], a[1])
        s = []
        if e.get("t"):
            # 🔴 r19 の目視：札を矢印の真ん中に置いたら、**矢印が札に丸ごと隠れた**
            #    （節どうしが近いカットでは、あいだが札の高さより狭い）。
            #    → 札の手前で軸を切り、札の向こう側から矢羽根を出す。
            mx, my = (a2[0] + b2[0]) / 2, (a2[1] + b2[1]) / 2
            es = 34
            tw = fm.width(e["t"], es, "Noto") + 34
            th = 58.0
            ln = math.hypot(b2[0] - a2[0], b2[1] - a2[1]) or 1.0
            ux, uy = (b2[0] - a2[0]) / ln, (b2[1] - a2[1]) / ln
            # 札が矢印の向きに占める長さ（矩形なので、向きに応じて幅か高さで決まる）
            half = min(tw / 2 / abs(ux) if abs(ux) > 1e-6 else 1e9,
                       th / 2 / abs(uy) if abs(uy) > 1e-6 else 1e9) + 10
            # ⚠️ しきい値は**実測して決めた**。44 だと片側 22px しか残らず、
            #    c218 で軸が 32px になって矢印に見えなかった（r20 のあと実測）。
            #    片側 60px は要る。
            if ln - half * 2 >= 120:
                # あいだに軸が見える長さが残る → 札の手前で切り、向こう側から矢羽根
                s.append(line(a2[0], a2[1], mx - ux * half, my - uy * half, c, 6))
                s.append(arrow(mx + ux * half, my + uy * half, b2[0], b2[1], c, 6, 24))
            else:
                # 🔴 r20 の目視：**札のほうが隙間より広い**カットが5枚あった
                #    （c310 は隙間354pxに札508px）。線の上に置くと矢印が消えるので、
                #    矢印はそのまま引いて、**札を線と直角の向きへ逃がす**。
                #    逃がす量は節の箱を跨ぐぶん（bh/2 ＋ 札の半分 ＋ 余白）。
                s.append(arrow(a2[0], a2[1], b2[0], b2[1], c, 6, 24))
                d0 = bh / 2 + th / 2 + 16
                nx, ny = -uy, ux
                if abs(uy) > abs(ux):          # 縦向きの矢印は横へ逃がす
                    nx, ny = (1.0, 0.0) if mx + d0 + tw / 2 < BX1 else (-1.0, 0.0)
                    d0 = bw / 2 + tw / 2 + 16
                elif ny > 0:                   # 横向きは上へ（下は字幕帯が近い）
                    nx, ny = -nx, -ny
                mx, my = mx + nx * d0, my + ny * d0
            s.append(rect(mx - tw / 2, my - th / 2, tw, th, J.BG, c, 3, rx=8))
            s.append(txtfit(mx, my + 10, e["t"], tw - 20, cap=es, col=c,
                            anchor="middle"))
        else:
            s.append(arrow(a2[0], a2[1], b2[0], b2[1], c, 6, 24))
        stages.append("".join(s))
    for n in nodes:
        x, y = x0 + w * n["x"], y0 + h * (n["y"] + _shift)
        c = n.get("c", J.LINE)
        s = [rect(x - bw / 2, y - bh / 2, bw, bh, c, op=0.16),
             rect(x - bw / 2, y - bh / 2, bw, bh, "none", c, 4, rx=8)]
        # 絵は左、文字は右。**その2つを1組にして、箱の中で中央に置く。**
        # 🔴 最初は左詰めにしていたら、名前が短い節（「CEO」「2号殻」「NTSB」）で
        #    右半分が丸ごと空いた（check_box：26枠中13枠が空き矩形 32〜58%）。
        #    左詰めだと空きが片側にまとまるので「穴」になる。中央に置けば両側に割れる。
        gs = min(GS, bh - 48, bw * 0.34) if n.get("kind") else 0.0
        tw_max = bw - 52 - (gs + 26 if gs else 0)
        ts = fm.fit(str(n["t"]), tw_max, "Noto", cap=TS_CAP, floor=20)
        ds = fm.fit(str(n.get("d", "")), tw_max, "Noto", cap=DS_CAP, floor=18) if n.get("d") else 0
        tw = max(fm.width(str(n["t"]), ts, "Noto"),
                 fm.width(str(n.get("d", "")), ds, "Noto") if ds else 0)
        cw_ = (gs + 26 if gs else 0) + tw
        sx = x - cw_ / 2
        if gs:
            s.append(_glyph(n["kind"], sx + gs / 2, y, gs, c))
        cx = sx + (gs + 26 if gs else 0)
        s.append(txt(cx, y + (16 if not n.get("d") else -8), n["t"], ts, J.INK_W))
        if ds:
            s.append(txt(cx, y + 46, n["d"], ds, J.TICK))
        stages.append("".join(s))
    return Fig("".join(g), stages, "", (x0, x0 + w))


# ══════════════════════════════════════════════════════════
# 19. beforeafter — 前と後
# ══════════════════════════════════════════════════════════
def beforeafter(a, b, note="", lead=""):
    """左右2枚。a/b は dict(k="変更前", t="…", lines=[…], c=…)。"""
    cw = (BW - 90) / 2                       # 上限。下で中身に合わせて詰める
    # 🔴 2026-08-01（r14 を焼いて目視）。process と同じ症状。
    #    箱は 843×526 なのに中身は「見出し＋箇条1行」だけで、器が中身の3倍あった。
    #    実測：24枠すべて lines が1行以下・値は1つも無い。
    #    → **中身を測って箱をその高さにし、縦の中央に置く。**
    top0 = BY0 + 96
    bh_max = BY1 - top0 - 60
    # 🔴 2026-08-02：process とまったく同じ症状。高さは中身から出していたのに、
    #    中身は bh*0.30／+bh*0.20 と**箱の割合**で置いていたので、
    #    どの箱も下 4割が空洞のままだった（24枠中11枠が空き矩形 32〜60%）。
    PAD_T, GAP1, LH, GAP2, PAD_B = 44.0, 26.0, 60.0, 30.0, 38.0

    def _mm(side):
        ts = fm.fit(str(side.get("t", "")), cw - 40, "Noto", cap=78, floor=18)
        lines = list(side.get("lines", []))
        vs = fm.fit(str(side["v"]), cw - 50, "Dela", cap=110) if side.get("v") else 0
        h = PAD_T + ts + PAD_B
        if lines:
            h += GAP1 + LH * len(lines)
        if vs:
            h += GAP2 + vs
        return ts, lines, vs, h

    mm = [_mm(a), _mm(b)]
    bh = max(190.0, min(bh_max, max(m[3] for m in mm)))
    # 🔴 高さを詰めたら、今度は**横**が空いた（11枠が空き矩形 32〜60%）。
    #    見出しだけ中央寄せ・箇条は左寄せ、という不揃いのせいで、
    #    短い見出しの左右と、箇条の右が別々に大きく空いていた。
    #    → ①中身をすべて左寄せにそろえる ②箱の幅を中身に合わせて詰める。
    each = []
    for (ts_, lines_, vs_, _), side in zip(mm, (a, b)):
        n_ = fm.width(str(side.get("t", "")), ts_, "Noto") + 68
        for ln in lines_:
            n_ = max(n_, fm.width("・" + ln, 46, "Noto") + 68)
        if vs_:
            n_ = max(n_, fm.width(str(side["v"]), vs_, "Dela") + 68)
        each.append(n_)
    # ⚠️ 左右で中身の長さが違うカットがある（c426「5.166 / 5.175 インチ」対「5 インチ」）。
    #    長いほうに幅を合わせると、**短いほうの右が丸ごと空く**（実測 59%）。
    #    → 幅は短いほうからも抑える。中身は左右とも中央にそろえるので、
    #      空きは両側に割れる（片側にまとまると「穴」になる）。
    cw = max(440.0, min(cw, max(each) + 90, max(min(each) * 2.0, 440.0)))
    top = top0 + (bh_max - bh) / 2
    x_left = BCX - cw - 45                   # 詰めた2枚を画面の中央にそろえる
    g = []
    if lead:
        g.append(txtfit(BX0, BY0 + 62, lead, BW, cap=44, col=J.INK_W))
    g.append(arrow(BCX - 26, top + bh / 2, BCX + 26, top + bh / 2, J.AMBER, 6, 22))
    stages = []
    for i, side in enumerate((a, b)):
        x = x_left + i * (cw + 90)
        c = side.get("c", J.LINE if i == 0 else J.ALERT)
        s = [rect(x, top, cw, bh, c, op=0.12), rect(x, top, cw, bh, "none", c, 4)]
        # 🔴 2026-08-02（r21 の目視・c406 c605 c622 c633 c637）：札は箱の上辺に
        #    またがって置くのに **地を敷いていなかった**ので、箱の上辺の線が
        #    札の文字の**真ん中を横切って取り消し線に見えていた**（12カット全部）。
        #    ⚠️ check_layout は「文字のほうがあとに描かれる＝隠れない」で見逃す。
        #      線は字の隙間から見えるので、**あとに描いても読みにくさは消えない**。
        #      地を敷いて、線そのものを札の裏に隠す。
        s.append(chip(x + 20, top - 22, side.get("k", ""), c, 28, fill=J.BG))
        # 中身の積算どおりに、箱の縦中央から絶対位置で置く
        ts, lines, vs, ch = mm[i]
        cy = top + (bh - ch) / 2
        s.append(txtfit(x + cw / 2, cy + PAD_T + ts * 0.78, side.get("t", ""),
                        cw - 68, cap=ts, col=J.INK_W, anchor="middle"))
        y = cy + PAD_T + ts
        if lines:
            y += GAP1
            for ln in lines:
                s.append(txtfit(x + cw / 2, y + 46 * 0.78, "・" + ln, cw - 68,
                                cap=46, col=J.LINE, anchor="middle"))
                y += LH
        if vs:
            y += GAP2
            s.append(txt(x + cw / 2, y + vs * 0.78, side["v"], vs, c, "Dela",
                         "middle"))
        stages.append("".join(s))
    if note:
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=26, col=J.TICK))
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
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.TICK))
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
        g.append(txtfit(BX0, BY1 - 6, note, BW, cap=28, col=J.TICK))
    top = [(cx - R + i * 2 * R / 40,
            cy - TE / 2 - (TC - TE) / 2 * math.cos(math.pi * (i / 40 - 0.5) * 2 * 0.5))
           for i in range(41)]
    bot = [(x, 2 * cy - y) for x, y in reversed(top)]
    g.append(poly(top + bot, fill=J.OK, close=True, op=0.24))
    g.append(poly(top + bot, stroke=J.OK, close=True, sw=5))
    g.append(line(cx - R - 120, cy - 210, cx - R - 120, cy + 210, J.LINE_DIM, 3))
    g.append(txt(cx - R - 136, cy, "外", 30, J.TICK, "Noto", "end"))
    # ⚠️ 「縁は薄い」の寸法線が cx+R+190 に立つので、そのラベル（左へ伸びる）と
    #    重なっていた。内側のラベルは寸法線の外へ出す。
    g.append(txt(cx + R + 330, cy, "内", 30, J.TICK))
    stages = [J.vdim(cy - TC / 2, cy + TC / 2, cx - 34, "中央は厚い"),
              J.vdim(cy - TE / 2, cy + TE / 2, cx + R + 190, "縁は薄い")]
    for m in (marks or []):
        stages.append(txtfit(BX0, BY1 - 150 + 56 * len(stages), m, BW, cap=38,
                             col=J.ALERT))
    return Fig("".join(g), stages, "", (cx - R - 160, cx + R + 300))
