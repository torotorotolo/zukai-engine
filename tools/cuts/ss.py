# -*- coding: utf-8 -*-
"""8本目（2003年2月1日 スペースシャトル・コロンビア号 空中分解事故）の
章ファイルが共通で使う小道具。

**7本目（9.11）の中身は git の `ae30d49` にある**（`git show ae30d49:tools/cuts/ss.py`）。

■ 素材の名前（`ref/ep8/`。選び方と出どころは `qa_out/ep8_assets.py` の `PICK`）
  `ep8/<欄の名>.jpg` … NASA 画像庫（`images.nasa.gov`）と
                       archive.org の NASA 束（`humanspaceflightcollection`）の写真。
                       **74点とも米連邦政府の職務著作＝パブリックドメイン。**
  `ep8/fb_<cid>.jpg` … 動く映像の**ひかえの静止画**（動画のコマが取れたら動画が勝つ）

■ 🔴🔴 この回も**報告書から取り出した図が1枚も無い**（`BANDS` が空）
  CAIB Vol.I の図版を実測したら **中央値 142px・最大 825px・幅1280以上は0点**
  （`ref/ep8/materials.md` §4）。焼くと英字が付いてくるうえ、画素が足りない
  （→ [[reference-report-figures-have-burned-in-english]]）。
  数字の図は **`titan_fig` の型で自分で描く**。
  ⚠️ だから `page()` は呼べない。呼んだら止まる。
  ⚠️ `check_cuts.py` の「4. 切り落とし」は報告書の図版だけを見る検査なので、
     この回も測る対象が 0件になる（門番の側が「BANDS が空」と名乗る）。

■ 🔴🔴 額装に回す敷居（`PANEL_AR`）は**この回の素材から取り直した**
  → [[feedback-per-episode-constants-go-stale]]

  7本目の 1.55 をそのまま当てると、**74点が74点とも額装**になった。
  NASA の写真は 3:2（1.50）が主で、1.55 の内側に1点も入らないため。

  ⚠️ **最初、私は「切り落とし 17.4% と 31.3% の間にはっきりした切れ目がある」と書いた。
     これは誤りだった。**上位14点と下位8点しか見ずに言っていて、74点を全部並べると
     18.6／20.6／21.5／24.1／28.2／29.2／31.3 と**間は埋まっている**。
     → [[feedback-dont-state-inferences-as-findings]]。台帳の切れ目で決める手
       （[[feedback-gate-threshold-from-ledger-split]]）は、**切れ目が実在するときだけ**使える。

  74点の切り落とし率の実測（小さい順）:
      13.4〜15.6% … 39点（3:2 の横位置）
      17.4%       … 14点（3032×2064 の機内写真）
      18.6／20.6／21.5／24.1／24.1 … 5点
      （+4.1 ＝ この帯でいちばん広い間）
      28.2〜63.3% … 16点（縦位置・正方形・4:3 より縦長）

  → 切れ目が無いので、**意味で決める**：**画の4分の1を超えて切るなら額装**。
    切り落とし 25% ＝ 縦横比 **4:3（1.333）**。ちょうど上の +4.1 の間に落ちる。
  ⚠️ 3:2 を全画面にすると上下が 15.6% 切れる。**⑤c の原寸目視で寄せを見ること**
     （→ [[feedback-measure-the-source-before-choosing-the-crop]]）。
  ⚠️ **`focus()` の寄せが効かない写真がある。**横が 16:9 より縦長な写真（この回の大半）は
     横幅を使い切るので `xbias` に遊びが無く、**いくら動かしても絵は同じ**。
     物差しだけ動いて絵が動かない罠 → [[feedback-video-qa-index]] §4。

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  「画像のこの点を画面の中央に置きたい」と書けるように、点（0〜1）から逆算する。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
  ⚠️ **寄せを変えても絵が変わらないことがある**（遊びが足りないとき）。
     → [[feedback-video-qa-index]] §4「切り出しの遊びを先に測る」
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep8"
W, H = 1920, 1080

# 画面の縦横比。これより縦長／横長の図は額装パネルに回す。
# 🔴 上限と下限は対（どちらも切り落とし 21.3% が上限）。片側だけにすると粗が反対側へ移る
#    （[[feedback-kinsoku-needs-both-ends]]）。
SCREEN_AR = W / H
# 🔴 **画の4分の1を超えて切るなら額装**（＝切り落とし 25%）。4:3 がちょうどその線。
PANEL_AR = round(4 / 3, 4)          # ＝1.3333。これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝2.37。これ超＝横長すぎ

# ── 額装で置くときの幅（②の実測。`ref/ep8/kousei.md` §3）─────────
# ⚠️ **器の札ではなく、黒帯を除いた「絵の幅」**。
#    [[feedback-container-labels-lie-about-the-picture]]
#    `fdcomm` は器 1280 で絵は 984、`sts1` は 948。ここを 1280 と信じると
#    1.3倍に伸ばして眠くなる。
PW_FDCOMM = 984
PW_STS1 = 948
PW_MC0201 = 969                     # ＝646 × 1.5
PW_FD16 = 921                       # ＝614 × 1.5
PW_GUNCAM = 960                     # ＝640 × 1.5
PW_CABIN = 945                      # ＝315 × 3.0（いちばん小さい。c411 だけ）

# 🔴 この回は報告書の図版を1枚も使わない。**空であることが正しい状態**。
BANDS = {}


def page(pr):
    """🔴 この回は報告書の図版を焼いていないので**呼べない**（黙って別の絵を出さない）。"""
    raise KeyError(
        f"印字 p{pr}: 8本目は CAIB の図版を1枚も使わない（BANDS が空／"
        f"実測で中央値142px・幅1280以上0点）。数字の図は `titan_fig` の型で描く")


def P(name):
    """欄の名前 → `ref/` から見た写真のパス。"""
    return f"ep8/{name}.jpg"


def fb(cid):
    """動く映像を当てたカットの**ひかえの静止画**（コマが取れなかったときだけ出る）。"""
    return f"ep8/fb_{cid}.jpg"


@lru_cache(maxsize=None)
def size_of(name):
    from PIL import Image
    with Image.open(HERE / "ref" / name) as im:
        return im.size


@lru_cache(maxsize=None)
def trimmed_size(name):
    """切り出しを当てたあとの寸法（画素）。切っていなければ原寸。

    ⚠️ **`scene_jiko` を import しない。** `scene_jiko` は起動時に `cuts` を読むので、
       ここから import すると循環参照になり、章ファイルが**丸ごと黙って読めなくなる**
       （2026-09-08 に実際に起きた。`check_layout` は空の SPEC を調べて
       「✓ 全部おさまっている」を出した）→ [[feedback-gates-blind-to-the-new-material]]
    """
    sw, sh = size_of(name)
    b = BANDS.get(name.split("/", 1)[-1].rsplit(".", 1)[0])
    if not b or not b.get("fig_box"):
        return sw, sh
    x0, y0, x1, y1 = b["fig_box"]
    return max(1, int(sw * (x1 - x0))), max(1, int(sh * (y1 - y0)))


def aspect(name):
    """切ったあとの縦横比（横÷縦）。"""
    w, h = trimmed_size(name)
    return w / h


def crop_loss(name):
    """全画面にしたとき、絵の**何割が枠の外へ出るか**（0〜1）。額装なら 0。"""
    a = aspect(name)
    return 1 - (a / SCREEN_AR if a < SCREEN_AR else SCREEN_AR / a)


def kind(name):
    """`dict(panel=True)` か `dict()` を返す。**縦横比で決める。目で決めない。**

    ⚠️ 縦長すぎ（< 1.40）だけでなく**横長すぎ（> 2.26）も額装**に回す。
    """
    a = aspect(name)
    return dict(panel=True) if (a < PANEL_AR or a > WIDE_AR) else dict()


def focus(name, fx, fy, zoom=1.0, box=(W, H)):
    """画像の点 (fx, fy)（0〜1・**切ったあとの絵の中での位置**）を画面中央に置く寄せ。

    `fit()`：z = max(w/sw, h/sh)*zoom ／ 切り出し幅 cw = w/z ／ 左端 l = (sw-cw)*xbias。
    中央に置く → l = fx*sw - cw/2 → xbias = (fx*sw - cw/2) / (sw - cw)。0〜1 に丸める。
    """
    sw, sh = trimmed_size(name)
    w, h = box
    z = max(w / sw, h / sh) * zoom
    cw, ch = min(sw, w / z), min(sh, h / z)
    xb = 0.5 if sw - cw < 1 else (fx * sw - cw / 2) / (sw - cw)
    yb = 0.5 if sh - ch < 1 else (fy * sh - ch / 2) / (sh - ch)
    return dict(xbias=round(min(1.0, max(0.0, xb)), 3),
                bias=round(min(1.0, max(0.0, yb)), 3), zoom=zoom)


@lru_cache(maxsize=None)
def _clips():
    return json.loads((REF / "clips.json").read_text(encoding="utf-8"))


def bars_trim(clip, tol=2):
    """器の左右の黒帯を、額の箱の**縦横比そのもの**から追い出す `trim`。無ければ None。

    🔴 **`zoom`（＝`PILLAR`）で追い出してはいけない。**`fit()` の zoom は縦横を
       同じ率で切るので、額装で 1/PILLAR を掛けると**上下も同じ率だけ落ちる**
       （`fdcomm` なら 720 → 553 ＝ 縦の23%が黙って消える）。
       全画面カットなら縦が切れても絵は生きるが、額装は箱ごと縮むので直しにならない。
    ⚠️ 幅は器の札ではなく **`clips.json` の `dispw`（②で測った絵の幅）**を使う
       → [[feedback-container-labels-lie-about-the-picture]]
    """
    c = _clips()[clip]
    w, dw = int(c["w"]), int(c.get("dispw") or c["w"])
    if dw >= w - tol:
        return None
    m = (w - dw) / 2 / w
    return (round(m, 4), 0.0, round(1 - m, 4), 1.0)


def vid(cid, pw, clip=None, **kw):
    """動く映像のカット（額装パネル＋ひかえの静止画）を1行で書く。

    `clip` を渡すと、その素材の**左右の黒帯**を `trim` で箱の外へ出す
    （`trim` を明に渡したときは、そちらが勝つ）。
    ⚠️ `footage.USE` に欄が無いと `scene_jiko.credit_of` が **RuntimeError で止まる**
       （ひかえの静止画は動画の出典を借りているので、欄が無ければ出せる出典が無い）。
    """
    t = kw.pop("trim", None) or (bars_trim(clip) if clip else None)
    d = dict(photo=fb(cid), panel=True, pw=pw, **kw)
    if t:
        d["trim"] = t
    return d


# ══════════════════════════════════════════════════════════
#  欄の名前（`qa_out/ep8_assets.py` の PICK と1対1）
# ══════════════════════════════════════════════════════════
# 🔴 ここに書いた名前が `ref/ep8/<名>.jpg` と `scene_jiko.EP8_PHOTO` の鍵になる。
#    3つが食い違うと出典が出ないか、写真が出ない。
#    検算＝`python qa_out/ep8_assets.py check` と `python tools/check_credits.py`。
#
# ⚠️ 末尾に年を書いた欄は**別の年・別の飛行の写真**。副題で必ずその年を名乗ること
#    （→ [[feedback-fallback-stills-must-match-the-era]]。門番は1件も鳴らない）。

# ── 射点と打ち上げ（KSC・2003年1月15〜16日）──────────────
PAD_RSS = P("pad_rss")                  # 回転式整備構台を開いた射点（縦）
PAD_STACK = P("pad_stack")              # 3つの部品が見える全景
ET_ORANGE = P("et_orange")              # オレンジ色の外部タンク
ET_SURFACE = P("et_surface")            # タンクと固体ロケットの表面（縦）
ET_TOP = P("et_top")                    # タンクの頂部（縦）
LAUNCH_WIDE = P("launch_wide")          # 木立の上へ
LAUNCH_FLAMES = P("launch_flames")      # 炎と煙（縦）
LAUNCH_SKY = P("launch_sky")            # 快晴の空へ

# ── 衝突のコマ（NASA 公式の追跡カメラ・2003年1月16日）─────
STRIKE_WIDE = P("strike_wide")          # 「T-0 から約80〜84秒」
STRIKE_NEAR = P("strike_near")          # 「約81〜82秒・バイポッド付近から」

# ── 乗員（地上）──────────────────────────────────
CREW_PORTRAIT = P("crew_portrait")      # 7人の記念写真（2002年7月）
CREW_ARRIVAL = P("crew_arrival")        # KSC 到着後（1月12日）
CREW_ASTROVAN = P("crew_astrovan")      # 射点へ向かう（1月16日）
SUIT_CHAWLA = P("suit_chawla")          # ホワイトルームでの着装
SUIT_CLARK = P("suit_clark")

# ── 軌道上（乗員が撮った電子スチル・3032×2064）────────────
ORB_CHAWLA = P("orb_chawla")
ORB_HUSBAND = P("orb_husband")
ORB_HUSBAND_SEAT = P("orb_husband_seat")
ORB_CLARK_ARMS = P("orb_clark_arms")
ORB_CHAWLA_HAB = P("orb_chawla_hab")
ORB_MCCOOL = P("orb_mccool")
ORB_CHAWLA_CLARK = P("orb_chawla_clark")
ORB_CLARK_HUSBAND = P("orb_clark_husband")
ORB_CLARK_WINDOW = P("orb_clark_window")
ORB_BROWN = P("orb_brown")
ORB_MCCOOL_AFD = P("orb_mccool_afd")
ORB_RAMON = P("orb_ramon")              # 縦
ORB_ANDERSON = P("orb_anderson")
ORB_CREW7 = P("orb_crew7")              # 7人が浮く恒例の記念写真（正方形）
ORB_ANDERSON_READ = P("orb_anderson_read")
ORB_EARTH = P("orb_earth")              # 機内から撮った日の出（1月22日）
COLUMBIA_ORBIT = P("columbia_orbit")    # 軌道のコロンビア号（地上望遠・1月28日・正方形）

# ── 管制室 ────────────────────────────────────
MCC_LAUNCH = P("mcc_launch")            # 打ち上げ当日の管制室（1月16日）
MCC_FEB1 = P("mcc_feb1")                # 🔴 2月1日の管制室
FD_CAIN = P("fd_cain")                  # 飛行主任（1月16日）
CAPCOM = P("capcom")                    # 乗員と話す席（1月16日）
FD_ENGELAUF = P("fd_engelauf")

# ── 東テキサスの捜索（archive.org にしか無い）────────────
SEARCH_LINE = P("search_line")          # 列を組んで野を歩く
SEARCH_BRIEF = P("search_brief")        # 出発前の説明
SEARCH_FOREST = P("search_forest")      # 森林局の捜索者
SEARCH_QUEUE = P("search_queue")        # 食事の列
SEARCH_MAP = P("search_map")            # 地図を見る
SEARCH_HOWELL = P("search_howell")      # 所長も捜索に加わる
EVIDENCE_CORSICANA = P("evidence_corsicana")
ENGINE_DIG = P("engine_dig")            # 掘る前の記録
ENGINE_FOUND = P("engine_found")        # 掘り出した主エンジン
BARKSDALE = P("barksdale")              # バークスデール基地の格納庫

# ── 格納庫での再構成（KSC・RLV Hangar）────────────────
HANGAR_FLOOR = P("hangar_floor")        # 床一面の破片
HANGAR_GRID = P("hangar_grid")          # 床の格子が埋まっていく
HANGAR_CAIB = P("hangar_caib")          # 委員が破片を見る
HANGAR_EXAM = P("hangar_exam")          # 破片を調べる
LE_FIXTURE = P("le_fixture")            # 前のふちを並べる治具（縦）
LE_FIXTURE2 = P("le_fixture2")
DEBRIS_TRUCK = P("debris_truck")        # 最後の輸送

# ── 衝突試験（SwRI・2003年6月6日）──────────────────
TEST_PANEL = P("test_panel")
TEST_PANEL2 = P("test_panel2")
TEST_HOLE = P("test_hole")

# ── 委員会と報告書 ───────────────────────────────
CAIB_HEARING = P("caib_hearing")        # 第3回公聴会（3月25日）
CAIB_GEHMAN = P("caib_gehman")
REPORT_COPY = P("report_copy")          # 出たばかりの報告書（8月26日・正方形）
REPORT_COPY2 = P("report_copy2")
REPORT_GEHMAN = P("report_gehman")
REPORT_MAIL = P("report_mail")          # 配るために積まれた報告書（11月6日）
HAM_CAIB = P("ham_caib")                # ミッション運営チーム議長（縦）
DITTEMORE = P("dittemore")              # シャトル計画責任者（4月23日）

# ── 記録装置 ─────────────────────────────────
OEX_RECORDER = P("oex_recorder")        # ⚠️ **1988年の同型**（正方形）

# ── 別の年のコロンビア号（⚠️ 副題で必ず年を名乗る）─────────
SLF_LANDING = P("slf_landing")          # 滑走路33に降りる（2002年3月）
SLF_APPROACH = P("slf_approach")        # 接地直前（2002年3月）
COLUMBIA_MIDDECK = P("columbia_middeck")  # コロンビア号の中デッキ（2002年3月）
CARGO_TOOL = P("cargo_tool")            # 貨物室で工具を確かめる（2002年3月）

# ── アトランティス号（救出案の相手）──────────────────
ATLANTIS_NOSE = P("atlantis_nose")      # 組立棟の機首（2月12日）
ATLANTIS_STACK = P("atlantis_stack")    # 固体ロケットと外部タンクを結合（2月13日・縦）

# ── そのほか ────────────────────────────────
RECOVERY_TEAM = P("recovery_team")      # 回収管理チームの作業（2月5日）
NEWS_CENTER = P("news_center")          # 2月1日、報道各社
