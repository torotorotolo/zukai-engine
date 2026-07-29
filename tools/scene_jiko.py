# -*- coding: utf-8 -*-
"""事故検証×図解様式のテスト映像。8カット・42.2秒。

題材＝**アロハ航空243便**（1988-04-28・ボーイング737-200・N73711）。
巡航中に胴体上部の外板が飛行中に剥離した。原因は重ね継手の接着剥離と疲労亀裂。

■ 素材はすべてパブリックドメイン（`ref/CREDITS.md` に出典と作者を記録）
  米連邦機関（NTSB / FAA / NASA / NARA）の著作物なので権利問題が起きない。

■ 設計の根拠（Vault `Projects/新チャンネル-事故検証ジャンル再測定-20260729.md`）
  最大手の画面を89コマ数えた実測：**図解は約7%**、実写＋アーカイブ写真が約18%。
  → 図解を80%以上に上げる（密度で差をつける）。
  → **実写は競合と同水準の18%を最初から設計に入れる**（静止画が続くと飽きるため）。
     実測：実写7.6秒 / 全体42.2秒 = **18.0%**。写真は3点使い、1枚を長く映さない。

■ カット構成
  p1 実写   事故機の左側面（屋根が消えている）      … 掴み
  p2 実写   事故前の N73711 本人                    … 同じ機体だと示す
  c2 図解   機体側面図と剥離範囲                    … どこが
  c3 図解   胴体断面（事故前／剥離後）              … どれだけ
  c4 図解   重ね継手の平面図・疲労亀裂              … どこから
  c5 図解   重ね継手の A-A 断面・接着剥離            … なぜ
  c6 図解   高度の時系列                            … 何が起きたか
  c7 図解   設計寿命と実際の回数                    … 背景
"""
import base64
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J
import render

W, H = 1920, 1080
HERE = Path(__file__).parent.parent
# フォントはリポジトリに同梱する。クラウドとローカルで字形を一致させるため
# base64 で SVG に埋め込む（システムフォントに依存させない）。
FONTS = Path(os.environ.get("ZUKAI_FONTS", HERE / "fonts"))
CSS = ""

# 機体側面図の置き場所。(x, y) は**機首先端・胴体上面線**（jiko_style の座標系）
AC_X, AC_Y, AC_S = 170, 560, 1.5


def ax(u):
    """機体座標の x（単位）→ 画面 x"""
    return AC_X + u * AC_S


def ay(u):
    return AC_Y + u * AC_S


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


def photo_frame(x, y, w, h, credit):
    """写真の枠と出典。**出典は必ず画面に出す。**"""
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" '
         f'stroke="{J.LINE}" stroke-width="6"/>']
    for cx, cy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
        g.append(f'<path d="M{cx - 26} {cy} h52 M{cx} {cy - 26} v52" stroke="{J.INK_W}" '
                 f'stroke-width="6"/>')
    g.append(J.label(x, y + h + 42, credit, J.LINE_DIM, 25))
    return "".join(g)


# ── p1：実写（事故機の左側面） ────────────────────────────
# 屋根が5.5mにわたって無くなった機体。この1枚で掴む。
P1_BOX = (140, 258, 1080, 592)


def p1_bg():
    """写真の下に敷く地。**注記は別レイヤーにする**（初稿は注記側にも背景を塗って写真が消えた）。"""
    return J.frame(W, H) + J.title("飛行中に、屋根が消えた",
                                   "アロハ航空243便　1988年4月28日　ボーイング737-200")


def p1_over():
    x, y, w, h = P1_BOX
    g = [photo_frame(x, y, w, h, "出典：NTSB（米国運輸安全委員会）／パブリックドメイン")]
    g.append(J.leader(700, 360, 1290, 322, J.ALERT))
    g.append(J.label(1310, 308, "客室の天井と外板が", J.ALERT, 44))
    g.append(J.label(1310, 362, "5.5 m にわたって消失", J.ALERT, 44))
    g.append(J.label(1310, 462, "高度 7,300 m を巡航中に発生", J.INK_W, 32))
    g.append(J.label(1310, 508, "乗員乗客 95人", J.INK_W, 32))
    g.append(J.label(1310, 554, "客室乗務員1名が機外へ", J.INK_W, 32))
    g.append(J.label(1310, 700, "▼ この機体に何が起きたのか", J.AMBER, 34))
    return "".join(g)


# ── p2：実写（事故前の N73711 本人） ──────────────────────
# 同じ機体の事故前が残っている。「この機体です」と示せると一気に近くなる。
P2_BOX = (900, 268, 880, 598)


def p2_bg():
    return J.frame(W, H) + J.title("この機体は、19年間飛んでいた",
                                   "事故を起こした N73711　1969年製")


def p2_over():
    x, y, w, h = P2_BOX
    g = [photo_frame(x, y, w, h,
                     "出典：米国国立公文書館（NARA）／撮影 Charles O'Rear／パブリックドメイン")]
    g.append(J.label(150, 360, "N 7 3 7 1 1", J.AMBER, 62))
    g.append(J.label(150, 428, "ハワイ諸島を結ぶ短距離路線を", J.LINE, 32))
    g.append(J.label(150, 474, "1日に十数往復していた", J.LINE, 32))
    g.append(J.label(150, 560, "1回の飛行は短い。だが", J.LINE, 30))
    g.append(J.label(150, 604, "離陸と着陸の回数だけが、", J.INK_W, 32))
    g.append(J.label(150, 648, "同型機の倍の速さで積み上がっていた。", J.INK_W, 32))
    return "".join(g)


# ── c2：機体側面図 ────────────────────────────────────────

def c2_base():
    g = [J.frame(W, H), J.title("消えたのは、前方扉のすぐ後ろから",
                                "ボーイング737-200　側面図（NTSB調査資料の三面図から作図）")]
    g.append(J.b737_side(AC_X, AC_Y, AC_S))
    # 機首からの距離。**実在しない station 番号を振ると図が嘘になる**ので、
    # 実測できる「機首からの m」で目盛る（全長30.53m = 720単位）。
    for m in range(0, 31, 5):
        u = m * 720 / 30.53
        g.append(f'<path d="M{ax(u):.0f} 330 V800" stroke="{J.GRID}" stroke-width="2.4"/>')
        g.append(J.label(ax(u), 836, f"{m} m", J.LINE_DIM, 22, "middle"))
    return "".join(g)


def c2_tear():
    return J.b737_tear(AC_X, AC_Y, AC_S)


def c2_anno():
    g = [J.dim(ax(120), ax(249.5), 452, "5.5 m")]
    g.append(J.leader(ax(200), ay(6), 1330, 300, J.ALERT))
    g.append(J.label(1350, 286, "剥離した範囲", J.ALERT, 42))
    g.append(J.label(1350, 336, "天井から窓の下まで、外板が", J.LINE, 28))
    g.append(J.label(1350, 374, "一続きに裂けて飛散した", J.LINE, 28))
    g.append(J.dim(ax(0), ax(720), 900, "全長 30.5 m"))
    g.append(J.leader(ax(330), ay(96), 1350, 520, J.LINE))
    g.append(J.label(1370, 506, "胴体直径 3.76 m", J.INK_W, 32))
    g.append(J.label(1370, 552, "与圧された客室の内側は", J.LINE, 28))
    g.append(J.label(1370, 590, "外気より 0.5 気圧ぶん高い", J.LINE, 28))
    g.append(J.label(150, 1020, "剥離は前方扉の直後から始まり、主翼の付け根の手前で止まった",
                     J.LINE, 30))
    return "".join(g)


# ── c3：胴体断面 ──────────────────────────────────────────

def c3_base():
    g = [J.frame(W, H), J.title("失われたのは、上半分だった", "胴体断面（客室1〜4列目）")]
    g.append(J.b737_section(600, 620, 1.5, floor=True))
    g.append(J.b737_section(1400, 620, 1.5, upper=(-165, -15), floor=True))
    for cx in (600, 1400):
        for dx in (-116, -78, 78, 116):
            g.append(f'<rect x="{cx + dx - 15}" y="{620 + 44}" width="30" height="46" rx="5" '
                     f'fill="none" stroke="{J.LINE_DIM}" stroke-width="4"/>')
    return "".join(g)


def c3_anno():
    g = [J.label(600, 960, "事故前", J.LINE, 40, "middle"),
         J.label(1400, 960, "剥離後", J.ALERT, 40, "middle"),
         J.label(600, 690, "客室", J.LINE, 28, "middle"),
         J.label(600, 806, "貨物室", J.LINE, 28, "middle"),
         J.label(600, 758, "床", J.LINE_DIM, 24, "middle")]
    g.append(J.dim(600 - 300, 600 + 300, 380, "3.76 m"))
    g.append(J.leader(1400, 320, 1660, 250, J.ALERT))
    g.append(J.label(1680, 236, "ここが消えた", J.ALERT, 38))
    g.append(J.label(1680, 282, "円周の約 55%", J.LINE, 28))
    g.append(J.label(1000, 620, "→", J.INK_W, 72, "middle"))
    g.append(J.label(150, 1020, "与圧された筒が一度裂けると、裂け目は一気に広がる", J.LINE, 30))
    return "".join(g)


# ── c4：重ね継手の平面図 ──────────────────────────────────

LJ_X, LJ_Y, LJ_S = 720, 610, 0.95


def c4_base():
    g = [J.frame(W, H), J.title("始まりは、リベット1列の亀裂",
                                "外板の重ね継手（ラップジョイント）を外から見た図")]
    g.append(J.lap_joint(LJ_X, LJ_Y, LJ_S, cracks=0))
    return "".join(g)


def c4_crack():
    return J.lap_joint(LJ_X, LJ_Y, LJ_S, cracks=15, only_cracks=True)


def c4_anno():
    """注記は必ず図の外へ。図の上に載せると読めない（初稿の失敗）。"""
    g = [J.label(300, 356, "外板（上）", J.INK_W, 32),
         J.label(300, 900, "外板（下）", J.LINE, 32)]
    # 重ね幅は**縦に測る寸法**。横に引くと図が嘘になる
    g.append(J.vdim(LJ_Y - 62 * LJ_S, LJ_Y + 62 * LJ_S, LJ_X - 480 * LJ_S - 40, "76 mm"))
    g.append(J.leader(LJ_X + 180, LJ_Y - 40 * LJ_S, 1330, 330, J.ALERT))
    g.append(J.label(1350, 316, "最上列のリベット穴から", J.ALERT, 36))
    g.append(J.label(1350, 360, "疲労亀裂が発生", J.ALERT, 36))
    g.append(J.label(1350, 430, "1本ずつは短い。", J.LINE, 28))
    g.append(J.label(1350, 468, "だが隣とつながると", J.LINE, 28))
    g.append(J.label(1350, 506, "一続きの裂け目になる", J.LINE, 28))
    g.append(J.label(1350, 590, "この機体では 24 か所で", J.INK_W, 30))
    g.append(J.label(1350, 628, "亀裂が確認された", J.INK_W, 30))
    # A-A の切断線。次のカットの断面がどこを切ったものか示す
    cx = LJ_X + 300 * LJ_S
    g.append(f'<path d="M{cx} 300 V920" stroke="{J.AMBER}" stroke-width="3" '
             f'stroke-dasharray="26 14"/>')
    g.append(J.label(cx, 286, "A", J.AMBER, 34, "middle"))
    g.append(J.label(cx, 952, "A", J.AMBER, 34, "middle"))
    g.append(J.label(150, 1020, "この面を A-A で切ると、なぜ折れたのかが見える", J.AMBER, 30))
    return "".join(g)


# ── c5：重ね継手の A-A 断面 ───────────────────────────────

SEC_X, SEC_Y, SEC_S = 900, 560, 1.55


def c5_base():
    g = [J.frame(W, H), J.title("荷重を分け合う相手が、いなくなった",
                                "重ね継手 A-A 断面（板厚は誇張している）")]
    g.append(J.lap_joint_section(SEC_X, SEC_Y, SEC_S, crack=False))
    return "".join(g)


def c5_crack():
    return J.lap_joint_section(SEC_X, SEC_Y, SEC_S, crack=True)


def c5_anno():
    hl = 95 * SEC_S
    g = [J.label(SEC_X - 480, 470, "外板（上）", J.INK_W, 30, "end"),
         J.label(SEC_X + 520, 640, "外板（下）", J.LINE, 30)]
    g.append(J.dim(SEC_X - hl, SEC_X + hl, 400, "76 mm"))
    g.append(J.leader(SEC_X, SEC_Y, 1330, 300, J.OK))
    g.append(J.label(1350, 286, "接着層", J.OK, 40))
    g.append(J.label(1350, 336, "設計では、この接着面と", J.LINE, 28))
    g.append(J.label(1350, 374, "リベットで荷重を分け合う", J.LINE, 28))
    g.append(J.leader(SEC_X - 62 * SEC_S, SEC_Y - 20 * SEC_S, 1330, 500, J.ALERT))
    g.append(J.label(1350, 486, "皿もみの縁は刃のように薄い", J.ALERT, 32))
    g.append(J.label(1350, 532, "接着が剥がれると、荷重は", J.LINE, 28))
    g.append(J.label(1350, 570, "この縁だけに集中する", J.LINE, 28))
    g.append(J.leader(SEC_X + 95 * SEC_S, SEC_Y, 1330, 700, J.AMBER))
    g.append(J.label(1350, 686, "段差", J.AMBER, 32))
    g.append(J.label(1350, 730, "外から見えるのはここだけ", J.LINE, 26))
    g.append(J.label(150, 970, "この機体は潮風の中を19年飛んだ。接着面には湿気が入り、腐食が進んでいた。",
                     J.LINE, 30))
    g.append(J.label(150, 1020, "外板の下で起きたことは、外からは見えない。", J.INK_W, 30))
    return "".join(g)


# ── c6：高度の時系列 ──────────────────────────────────────

PTS = [(0.00, 0.00), (0.13, 0.86), (0.30, 0.92), (0.36, 0.92),
       (0.41, 0.60), (0.57, 0.28), (0.78, 0.09), (1.00, 0.00)]


def c6_base():
    g = [J.frame(W, H), J.title("剥離から着陸まで、13分", "高度の推移")]
    g.append(J.alt_graph(230, 330, 1460, 520, PTS, mark=3))
    return "".join(g)


def c6_anno():
    g = [J.label(210, 350, "7,300 m", J.AMBER, 30, "end"),
         J.label(210, 592, "3,600 m", J.LINE_DIM, 26, "end"),
         J.label(210, 856, "0", J.AMBER, 30, "end"),
         J.label(230, 902, "離陸　ヒロ", J.LINE, 28),
         J.label(1690, 902, "着陸　マウイ島カフルイ", J.LINE, 28, "end")]
    mx = 230 + 1460 * 0.36
    g.append(J.leader(mx, 330 + 520 * 0.08, 1120, 236, J.ALERT))
    g.append(J.label(1140, 222, "ここで剥離", J.ALERT, 38))
    g.append(J.label(1140, 268, "操縦室の扉も吹き飛び、", J.LINE, 26))
    g.append(J.label(1140, 302, "機長は客室の空を直接見ていた", J.LINE, 26))
    g.append(J.label(660, 640, "緊急降下", J.INK_W, 34))
    g.append(J.dim(mx, 1690, 990, "13分"))
    return "".join(g)


# ── c7：数字 ──────────────────────────────────────────────

def c7_base():
    g = [J.frame(W, H), J.title("設計の想定を、超えて飛んでいた",
                                "この機体が経験した離着陸の回数")]
    g.append(f'<path d="M960 330 V900" stroke="{J.LINE_DIM}" stroke-width="4"/>')
    g.append(J.label(960, 1010, "1969年製・19年間・ハワイ諸島間の短距離を1日十数往復",
                     J.LINE, 30, "middle"))
    return "".join(g)


def c7_num(k):
    n = int(89680 * k)
    g = [J.bignum(520, 640, "75,000", "回", "設計上の想定", J.LINE),
         J.bignum(1400, 640, f"{n:,}", "回", "実際に飛んだ回数", J.ALERT)]
    if k >= 0.999:
        g.append(J.label(1400, 760, "想定の 1.20 倍", J.ALERT, 40, "middle"))
        g.append(J.label(520, 760, "この回数で点検する前提だった", J.LINE, 28, "middle"))
    return "".join(g)


# ── カットの並びと尺 ──────────────────────────────────────
# 実写 p1+p2 = 7.6秒 / 全体 42.2秒 = 18.0%（競合の実測値と同水準）
CUTS = [("p1", 4.8), ("p2", 2.8), ("c2", 6.0), ("c3", 5.4),
        ("c4", 6.0), ("c5", 6.4), ("c6", 5.4), ("c7", 5.4)]
PHOTO_CUTS = {"p1": (P1_BOX, "aloha_left.jpg"), "p2": (P2_BOX, "aloha_normal.jpg")}


def render_all(force=False):
    out = HERE / "out" / "jiko"
    out.mkdir(parents=True, exist_ok=True)
    jobs = {"p1_bg": p1_bg(), "p1_over": p1_over(),
            "p2_bg": p2_bg(), "p2_over": p2_over(),
            "c2_base": c2_base(), "c2_tear": c2_tear(), "c2_anno": c2_anno(),
            "c3_base": c3_base(), "c3_anno": c3_anno(),
            "c4_base": c4_base(), "c4_crack": c4_crack(), "c4_anno": c4_anno(),
            "c5_base": c5_base(), "c5_crack": c5_crack(), "c5_anno": c5_anno(),
            "c6_base": c6_base(), "c6_anno": c6_anno(),
            "c7_base": c7_base()}
    for k, svg in jobs.items():
        p = out / f"{k}.png"
        if p.exists() and not force:
            continue
        render.png(page(svg), p, W, H)
        print(k, flush=True)
    p = out / "c7_num.png"
    if force or not p.exists():
        cols, rows, cw, ch = 4, 3, W // 2, H // 2
        cells = "".join(
            f'<g transform="translate({(i % cols) * cw},{(i // cols) * ch}) scale(0.5)">'
            f'{c7_num(min(1.0, (i / 11) ** 0.55))}</g>' for i in range(12))
        render.png(page(cells, cw * cols, ch * rows), p, cw * cols, ch * rows)
        print("c7_num", flush=True)
    print("done")


def ensure_css():
    """フォントの base64 は 4MB 超になる。合成側（build_jiko）では不要なので遅延で読む。"""
    global CSS
    if not CSS:
        CSS = (face_css("Dela", "DelaGothicOne.woff2")
               + face_css("Noto", "NotoSansJP-Bold.woff2"))


if __name__ == "__main__":
    ensure_css()
    render_all(force="--force" in sys.argv)
