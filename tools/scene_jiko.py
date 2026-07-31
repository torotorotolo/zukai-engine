# -*- coding: utf-8 -*-
"""本番1本目「潜水艇タイタン号」226カット・34分06秒のレイヤー書き出し。

■ 何がどこにあるか
  台本の文言   … `tools/narration.py` の SCRIPT（**正本はあちら**。ここには写さない）
  カットの尺   … `audio/narration.json`（合成後の実測秒）
  カットの「画」… `tools/cuts/*.py`（章ごと。この場所だけを直せば図が変わる）
  図の部品     … `tools/titan_fig.py`（型。226カットをこの部品で組む）

■ レイヤーの命名（build_jiko がこの名前で拾う）
  {cid}_base … 地＋見出し＋章マーカー。カット頭から出ている（動かない）
  {cid}_lab  … 図の骨格。**カット前半で左→右に描かれる**
  {cid}_aN   … 図の N 段目。**その段の持ち時間いっぱいをかけて左→右に描かれる**
  {cid}_hot  … 脈打つ強調（省略可）
  実写カットは {cid}_bg（地・写真に覆われる）と {cid}_lab（写真の上）＋{cid}_aN

■ 🔴 3秒以上の静止を禁止（映像ルール4）を**構造で満たす**
  段の持ち時間 ＝ その段が出てから次の段が出るまで（最後の段はカット終わりまで）。
  段はその持ち時間いっぱいをかけて描かれるので、**カットの頭から終わりまで常に何かが動く**。
  テスト映像のようにカットごとに MOTION を手で書く必要が無くなった
  （手書きだと図を動かすたびに直し忘れる。実際 c3 のワイプ範囲で1度やっている）。

■ 🔴 写真より上に出すものは `_lab` に置く
  build_jiko は bg の上に写真を貼るので、`_bg` に置いた文字は全画面写真に丸ごと覆われる
  （21巡目に見出しが完全に消えた）。
"""
import base64
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J
import titan_fig as F
import fontmetrics as fm
import render

W, H = 1920, 1080
HERE = Path(__file__).parent.parent
FONTS = Path(os.environ.get("ZUKAI_FONTS", HERE / "fonts"))
OUT = HERE / "out" / "jiko"
CSS = ""

# ── 章（章マーカーに出す名前） ────────────────────────────
CHAPTERS = {
    "c1": (1, "その日、10時47分"),
    "c2": (2, "炭素繊維という選択"),
    "c3": (3, "一度目の船体"),
    "c4": (4, "二度目の船体"),
    "c5": (5, "大きな音"),
    "c6": (6, "11か月の空白"),
}
NCH = 6


def chapter_of(cid):
    """プロローグ（pr*）とエピローグ（ep*）は章マーカー無し。"""
    return CHAPTERS.get(cid[:2])


# ── 出典表記（ref/CREDITS.md の台帳と1対1） ───────────────
CR_NTSB = "出典：NTSB（米国運輸安全委員会）／パブリックドメイン"
CR_USCG_ROV = "出典：アメリカ沿岸警備隊／ROV撮影／パブリックドメイン"
CR_USCG_L = "出典：アメリカ沿岸警備隊／撮影 M. Leake／パブリックドメイン"
CR_NOAA = "出典：NOAA／海洋探査研究所／ロードアイランド大学／パブリックドメイン"

PHOTO_CREDIT = {
    "titan_hull_edge.jpg": CR_NTSB,
    "titan_hull_inner.jpg": CR_NTSB,
    "titan_delam_ruler.jpg": CR_NTSB,
    "titan_rov_aft.jpg": CR_USCG_ROV,
    "titan_rov_tailcone.jpg": CR_USCG_ROV,
    "titan_cf_evidence.jpg": CR_USCG_L,
    "titan_titanic_bow.jpg": CR_NOAA,
}
# ⚠️ ref/titan_hull_pair.jpg は CREDITS.md に出所が無い。**どのカットにも割り当てない。**
BANNED_PHOTOS = {"titan_hull_pair.jpg"}


def face_css(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


def page(inner, w=W, h=H):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}">{inner}</svg>')
    return (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{CSS}'
            f'body{{width:{w}px;height:{h}px;overflow:hidden}}</style></head>'
            f'<body>{svg}</body></html>')


# ── 字幕 ─────────────────────────────────────────────────
# 黒帯の上・38px・NotoSansJP-Bold・全カット統一（映像ルール1）。帯は y=900〜1080。
SUB_Y, SUB_H = 900, 180
SUB_SIZE = 38
SUB_MAXW = 1560          # 字幕1行に許す最大の幅（px）。**実測で折る**
XML = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def esc(t):
    return "".join(XML.get(c, c) for c in t)


def wrap2(text):
    """字幕は**2行まで**。折る位置は読点。無ければ幅の中央に近い文字境界。

    🔴 「26字」で折っていたのを**実測幅（px）**に変えた。
       字幕は漢字・かな・数字が混ざるので、字数で折ると1行の長さが 1.6 倍ぶれる
       （「2023年6月18日、午前10時47分。」は16字だが数字が多く、
         「潜水艇は、原型をとどめていなかった。」の18字より狭い）。
    """
    if fm.width(text, SUB_SIZE, "Noto") <= SUB_MAXW:
        return [text]
    half = fm.width(text, SUB_SIZE, "Noto") / 2
    best, acc = None, 0.0
    cands = []
    for i, ch in enumerate(text):
        acc += fm.adv(ch, "Noto") * SUB_SIZE
        if ch in "、。":
            cands.append((abs(acc - half), i + 1))
        if best is None or abs(acc - half) < best[0]:
            best = (abs(acc - half), i + 1)
    cut = min(cands)[1] if cands else best[1]
    return [text[:cut], text[cut:]]


def sub_row(text, w=W, h=SUB_H):
    """字幕1枚。黒帯＋太いフチ。1行なら下寄せ、2行なら上下に振り分ける。"""
    lines = wrap2(text)
    ys = [h * 0.64] if len(lines) == 1 else [h * 0.42, h * 0.78]
    g = [f'<linearGradient id="subbg" x1="0" y1="1" x2="0" y2="0">'
         f'<stop offset="0" stop-color="#000" stop-opacity="0.78"/>'
         f'<stop offset="0.62" stop-color="#000" stop-opacity="0.70"/>'
         f'<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
         f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#subbg)"/>']
    for t, y in zip(lines, ys):
        g.append(f'<text x="{w / 2:.0f}" y="{y:.0f}" font-family="Noto" '
                 f'font-size="{SUB_SIZE}" fill="{J.INK_W}" text-anchor="middle" '
                 f'stroke="#000" stroke-width="7" stroke-linejoin="round" '
                 f'paint-order="stroke fill">{esc(t)}</text>')
    return "".join(g)


def sub_strip(lines):
    return "".join(f'<g transform="translate(0,{i * SUB_H})">{sub_row(t)}</g>'
                   for i, t in enumerate(lines))


# ── 実写カットの型：全画面 ────────────────────────────────
PHOTO_FULL = (0, 0, W, H)
SCRIM_TOP = 300
CRED_Y = 872


def full_bg():
    """全画面写真カットの地。**ここには何も置けない**（写真が全面で乗る）。"""
    return J.frame(W, H)


def full_top(cid, spec):
    """写真の上に載せる一式（暗幕・見出し・章マーカー・出典）。`_lab` に入れる。"""
    side = spec.get("side", "right")
    g = [J.scrim(0, 0, W, SCRIM_TOP, "top", 0.80)]
    if side == "right":
        g.append(J.scrim(1150, 0, W - 1150, H, "right", 0.62))
    else:
        g.append(J.scrim(0, 0, 770, H, "left", 0.62))
    g.append(J.title(spec["t"], spec.get("s", "")))
    ch = chapter_of(cid)
    if ch:
        g.append(J.chapter(ch[0], NCH, ch[1]))
    g.append(J.outlined(J.MG, CRED_Y, PHOTO_CREDIT[spec["photo"]], J.LINE, 24, sw=5))
    return "".join(g)


def photo_ann(spec):
    """実写カットの注記。**4〜6ブロックまで**（全画面では多いと邪魔になる）。

    ann … [dict(t="巡航高度", v="7,300 m", c=J.AMBER)] を上から積む。
    """
    side = spec.get("side", "right")
    x = J.RIGHT if side == "right" else J.MG
    anchor = "end" if side == "right" else "start"
    maxw = 700
    y = spec.get("ann_y", 340)
    out = []
    for a in spec.get("ann", []):
        s = []
        if a.get("t"):
            size = fm.fit(a["t"], maxw, "Noto", cap=a.get("ts", 46), floor=24)
            s.append(J.outlined(x, y, a["t"], a.get("c", J.INK_W), size, anchor,
                                sw=max(6, size * 0.17)))
            y += size + 18
        if a.get("v"):
            size = fm.fit(a["v"], maxw, "Dela", cap=a.get("vs", 96), floor=30)
            s.append(J.outlined(x, y + size * 0.20, a["v"], a.get("vc", J.AMBER),
                                size, anchor, sw=max(7, size * 0.15), family="Dela"))
            y += size + 26
        if a.get("d"):
            size = fm.fit(a["d"], maxw, "Noto", cap=a.get("ds", 34), floor=22)
            s.append(J.outlined(x, y, a["d"], a.get("dc", J.LINE), size, anchor,
                                sw=max(5, size * 0.17)))
            y += size + 16
        y += 22
        out.append("".join(s))
    return out


# ── 図解カットの地 ────────────────────────────────────────
def fig_base(cid, spec):
    g = [J.frame(W, H), J.title(spec["t"], spec.get("s", ""))]
    ch = chapter_of(cid)
    if ch:
        g.append(J.chapter(ch[0], NCH, ch[1]))
    return "".join(g)


# ── カット表を読み込む ────────────────────────────────────
def _load_spec():
    """`tools/cuts/*.py` の SPEC を1つに束ねる。章ごとにファイルを分けてある。"""
    import cuts
    return cuts.SPEC


SPEC = _load_spec()

# ── 尺と字幕（audio/narration.json の実測） ───────────────
LEAD, TAIL = 0.35, 0.50


def _narration():
    p = HERE / "audio" / "narration.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    dur = d["durations"]
    cuts = [(c, round(dur[c] + LEAD + TAIL, 2)) for c in dur]
    return cuts, d.get("subtitles", {})


CUTS, SUBS = _narration()
ORDER = [c for c, _ in CUTS]

# 全画面の実写カット。(枠, ファイル名, 縦方向の寄せ)
PHOTO_CUTS = {cid: (PHOTO_FULL, s["photo"], s.get("bias", 0.5))
              for cid, s in SPEC.items() if s.get("photo")}
INSETS = {}


# ── 段の持ち時間 ─────────────────────────────────────────
def stage_times(cid, nstage):
    """段 i が「出はじめる秒」と「描き終える秒」を返す。

    段はナレーションの行に合わせて出す。行より段が多ければ余った段を等間隔で挟む。
    **描き終える秒 ＝ 次の段が出る秒**（最後の段はカット終わりまで）。
    こうすると、カットのどの瞬間にも必ず「描いている途中の段」が1つある。
    """
    sec = dict(CUTS)[cid]
    rows = SUBS.get(cid, [])
    starts = [r["t"] + LEAD for r in rows]
    if not starts:
        starts = [0.25]
    if nstage <= len(starts):
        st = starts[:nstage]
    else:
        # 行の切れ目を優先しつつ、足りないぶんは行の間に等間隔で挟む
        st = list(starts)
        bounds = starts + [sec]
        while len(st) < nstage:
            widest = max(range(len(bounds) - 1), key=lambda i: bounds[i + 1] - bounds[i])
            mid = (bounds[widest] + bounds[widest + 1]) / 2
            st.append(mid)
            bounds = sorted(bounds + [mid])
        st = sorted(st)[:nstage]
    ends = st[1:] + [sec]
    # 描き終わりが早すぎると止まって見える。最低でも 1.1 秒はかける
    return [(a, max(b, a + 1.1)) for a, b in zip(st, ends)]


# ── レイヤーの組み立て ────────────────────────────────────
def build_layers(allow_missing=False):
    """cid → {レイヤー名: SVG} と、ワイプの x 範囲を返す。

    allow_missing … 章を1つずつ作っている途中は True で回す（未定義カットを飛ばす）。
    """
    jobs, spans = {}, {}
    for cid in ORDER:
        spec = SPEC.get(cid)
        if spec is None:
            if allow_missing:
                continue
            raise SystemExit(f"カット {cid} の画が定義されていません（tools/cuts/）")
        if spec.get("photo"):
            if spec["photo"] in BANNED_PHOTOS:
                raise SystemExit(f"{cid}: {spec['photo']} は出所が無いので使えません")
            jobs[f"{cid}_bg"] = full_bg()
            jobs[f"{cid}_lab"] = full_top(cid, spec)
            for i, a in enumerate(photo_ann(spec)):
                jobs[f"{cid}_a{i + 1}"] = a
            spans[cid] = (0, W)
            continue
        kind, kw = spec["fig"]
        fig = getattr(F, kind)(**kw)
        jobs[f"{cid}_base"] = fig_base(cid, spec)
        lab, stages = fig.lab, list(fig.stages)
        if not stages:
            # 段が無いと「描いている途中」が作れず、カットが丸ごと静止する。
            # 骨格を段に格上げして、カット全体をかけて描かせる。
            lab, stages = "", [lab]
        if lab:
            jobs[f"{cid}_lab"] = lab
        for i, s in enumerate(stages):
            jobs[f"{cid}_a{i + 1}"] = s
        if fig.hot:
            jobs[f"{cid}_hot"] = fig.hot
        # 🔴 ワイプ範囲は**必ず本体枠を含める**。
        #    型が返す span は「図の実体」しか指していないことがあり
        #    （例：icons は絵の並びだけで 640〜1280）、そのままだと枠の左右に置いた
        #    見出し・注記・出典が**ワイプの外に出て永久に現れない**。
        spans[cid] = (min(fig.span[0], F.BX0), max(fig.span[1], F.BX1))
    return jobs, spans


def layer_index():
    """build_jiko が読む索引。{cid: dict(kind, layers, span, stages)}"""
    jobs, spans = build_layers()
    idx = {}
    for cid in ORDER:
        names = [k for k in jobs if k.startswith(cid + "_")]
        ns = len([k for k in names if re.fullmatch(rf"{cid}_a\d+", k)])
        idx[cid] = {"photo": bool(SPEC[cid].get("photo")), "span": spans[cid],
                    "stages": ns, "layers": sorted(names)}
    return idx, jobs


def render_all(force=False, only=None, jobs_workers=4):
    """SVG → PNG。**Chrome を1レイヤーにつき1回起動する**ので並列で回す。

    226カット × 平均5レイヤー ＋ 字幕226枚 ＝ 約1,350回。直列だと20分近い。
    """
    from concurrent.futures import ThreadPoolExecutor
    OUT.mkdir(parents=True, exist_ok=True)
    ensure_css()
    jobs, _ = build_layers(allow_missing=True)
    jobs["_empty"] = J.frame(W, H)        # 余白測定の基準（check_space.py が使う）
    todo = []
    for k, svg in jobs.items():
        if only and not k.startswith(only):
            continue
        p = OUT / f"{k}.png"
        if p.exists() and not force:
            continue
        todo.append((k, svg, p, W, H))
    for cid, rows in SUBS.items():
        if only and not cid.startswith(only):
            continue
        p = OUT / f"sub_{cid}.png"
        if p.exists() and not force:
            continue
        h = SUB_H * len(rows)
        todo.append((f"sub_{cid}", sub_strip([r["text"] for r in rows]), p, W, h))
    print(f"書き出すレイヤー {len(todo)} 枚（並列 {jobs_workers}）", flush=True)
    done = [0]

    def one(t):
        k, svg, p, w, h = t
        render.png(page(svg, w, h), p, w, h)
        done[0] += 1
        if done[0] % 50 == 0:
            print(f"  {done[0]}/{len(todo)}", flush=True)

    with ThreadPoolExecutor(max_workers=jobs_workers) as ex:
        list(ex.map(one, todo))
    print(f"done {len(todo)}", flush=True)


def ensure_css():
    """フォントの base64 は4MB超。合成側では要らないので遅延で読む。"""
    global CSS
    if not CSS:
        CSS = (face_css("Dela", "DelaGothicOne.woff2")
               + face_css("Noto", "NotoSansJP-Bold.woff2")
               + face_css("NotoM", "NotoSansJP-Medium.woff2"))


def report():
    """焼く前に机上で見る要約。カット数・尺・図の種類の分布。"""
    from collections import Counter
    total = sum(s for _, s in CUTS)
    kinds = Counter(SPEC[c]["fig"][0] if not SPEC[c].get("photo") else "photo"
                    for c in ORDER)
    print(f"カット {len(ORDER)} ／ 完成尺 {total:.1f}秒 = "
          f"{int(total // 60)}分{total % 60:04.1f}秒")
    print(f"字幕 {sum(len(v) for v in SUBS.values())} 枚")
    print("図の種類:")
    for k, v in kinds.most_common():
        print(f"   {k:<12} {v:>3}")
    miss = [c for c in ORDER if c not in SPEC]
    if miss:
        print(f"🔴 画が未定義: {miss}")
    extra = [c for c in SPEC if c not in ORDER]
    if extra:
        print(f"🔴 台本に無いカット: {extra}")
    return not (miss or extra)


if __name__ == "__main__":
    if "--report" in sys.argv:
        sys.exit(0 if report() else 1)
    render_all(force="--force" in sys.argv,
               only=next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")),
                         None))
