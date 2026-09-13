# -*- coding: utf-8 -*-
"""7本目（2001年9月11日 米国同時多発テロ）の章ファイルが共通で使う小道具。

**6本目（キー橋）の中身は git の `121d3be` にある**（`git show 121d3be:tools/cuts/ss.py`）。

■ 素材の名前（`ref/ep7/`。出どころは `ref/CREDITS.md` §9.11・取り出しは `qa_out/ep7_assets.py`）
  `ep7/<欄の名>.jpg` … Commons／NARA の写真（**PD と CC BY だけ**。CC BY-SA は採らない）
  `ep7/fb_<cid>.jpg` … RG237 の動画の**ひかえの静止画**（動画のコマが取れたら動画が勝つ）

■ 🔴🔴 この回は**報告書から取り出した図が1枚も無い**（`BANDS` が空）
  9/11委員会報告は**文章の報告書**で、画面に出すのは印字ページ番号だけ。
  数字の図（高度・搭乗率・時刻）は **`titan_fig` の型で自分で描く**
  （報告書の図を焼くと英字が焼き込まれて付いてくる＝
   [[reference-report-figures-have-burned-in-english]]）。
  ⚠️ だから `page()` は呼べない。呼んだら止まる。
  ⚠️ `check_cuts.py` の「4. 切り落とし」は**報告書の図版だけ**を見る検査なので、
     この回は測る対象が 0件になる。**門番の側で「BANDS が空ならそう名乗る」**ように直した
     （0件を黙って合格にしない。`check_cuts.py` の注記）。

■ 🔴 RG237（航跡レーダー・ARTCC 画面）は**額装パネル**
  表示幅が **655px**（720×480 の SAR 10:11 を正方形に直した幅）しか無く、
  1920 に伸ばすと3倍で眠くなる。`rg()` が `panel=True` ＋ `pw=PW_RG237` を付ける。
  ⚠️ **画素が正方形でない**ので、切り出しは `footage._cut_stream` が
     `scale=iw*sar:ih,setsar=1` で直す（2026-09-13 ⑤b で入れた）。
     ここを外すとレーダーの円が卵になる＝[[feedback-container-labels-lie-about-the-picture]]

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  「画像のこの点を画面の中央に置きたい」と書けるように、点（0〜1）から逆算する。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep7"
W, H = 1920, 1080

# 画面の縦横比。これより縦長／横長の図は額装パネルに回す。
# 🔴 上限と下限は対（どちらも切り落とし 12.8% が上限）。片側だけにすると粗が反対側へ移る
#    （[[feedback-kinsoku-needs-both-ends]]）。
SCREEN_AR = W / H
PANEL_AR = 1.55                     # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝2.04。これ超＝横長すぎ

# RG237 を額装で置くときの幅。②の実測＝655×480 を 1120×648 の箱に入れると z=1.35。
# ⚠️ ffmpeg は偶数に丸めるので切り出したコマは **654×480**。1px の差を粗と読まない。
# ⑤c の原寸目視で甘ければ 655（等倍）に落とす（②の申し送り）。
PW_RG237 = 983                      # ＝655 × 1.5

# 🔴 この回は報告書の図版を1枚も使わない。**空であることが正しい状態**。
BANDS = {}


def page(pr):
    """🔴 この回は報告書の図版を焼いていないので**呼べない**（黙って別の絵を出さない）。"""
    raise KeyError(
        f"印字 p{pr}: 7本目は報告書から取り出した図を1枚も使わない（BANDS が空）。"
        f"数字の図は `titan_fig` の型で描く")


def P(name):
    """欄の名前 → `ref/` から見た写真のパス。"""
    return f"ep7/{name}.jpg"


def fb(cid):
    """RG237 の動画を当てたカットの**ひかえの静止画**（コマが取れなかったときだけ出る）。"""
    return f"ep7/fb_{cid}.jpg"


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

    ⚠️ 縦長すぎ（< 1.55）だけでなく**横長すぎ（> 2.04）も額装**に回す。
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


def rg(cid, **kw):
    """RG237 の実写カット（額装パネル＋ひかえの静止画）を1行で書く。

    ⚠️ `footage.USE` に欄が無いと `scene_jiko.credit_of` が **RuntimeError で止まる**
       （ひかえの静止画は動画の出典を借りているので、欄が無ければ出せる出典が無い）。
    """
    return dict(photo=fb(cid), panel=True, pw=PW_RG237, **kw)


# ══════════════════════════════════════════════════════════
#  欄の名前（`qa_out/ep7_assets.py` の SLOTS と1対1）
# ══════════════════════════════════════════════════════════
# 🔴 ここに書いた名前が `ref/ep7/<名>.jpg` と `scene_jiko.EP7_PHOTO` の鍵になる。
#    3つが食い違うと出典が出ないか、写真が出ない。検算＝`python qa_out/ep7_assets.py count`。
# ── 街と世界貿易センター
MANHATTAN_PRE = P("manhattan_pre")
COMMUTE_PRE = P("commute_pre")
WTC_FAR = P("wtc_far")
WTC_TWIN = P("wtc_twin")
WTC_BASE = P("wtc_base")
WTC_SOUTH = P("wtc_south")
WTC_UNDER = P("wtc_under")
# ── 空港（2001年以前）
LOBBY_PRE = P("lobby_pre")
SECURITY_PRE = P("security_pre")
GATE_PRE = P("gate_pre")
FIDS_PRE = P("fids_pre")
LOGAN = P("logan")
LOGAN_APRON = P("logan_apron")
LOGAN_TAKEOFF = P("logan_takeoff")
DULLES = P("dulles")
DULLES_RWY = P("dulles_rwy")
REAGAN = P("reagan")
NEWARK_757 = P("newark_757")
# ── 機体と機内
B767 = P("b767")
B757 = P("b757")
B767_CRUISE = P("b767_cruise")
B767_TAKEOFF = P("b767_takeoff")
B757_TAKEOFF = P("b757_takeoff")
AIRLINER_CRUISE = P("airliner_cruise")
REFUEL = P("refuel")
CABIN_PRE = P("cabin_pre")
COCKPIT_DOOR_PRE = P("cockpit_door_pre")
CABIN_PHONE = P("cabin_phone")
COCKPIT_PRE = P("cockpit_pre")
WINDOW_CRUISE = P("window_cruise")
WINDOW_SKY = P("window_sky")
# ── 管制
ARTCC_SCREEN_PRE = P("artcc_screen_pre")
RADAR_SCOPE_PRE = P("radar_scope_pre")
CONTROLLER_PRE = P("controller_pre")
ARTCC_SCREEN2 = P("artcc_screen2")
ARTCC_ALT = P("artcc_alt")
ARTCC_SEAT = P("artcc_seat")
BOSTON_ARTCC_EXT = P("boston_artcc_ext")
INDY_ARTCC = P("indy_artcc")
CLEVELAND_ARTCC = P("cleveland_artcc")
ATCSCC = P("atcscc")
AOC_PRE = P("aoc_pre")
# ── ペンタゴン
PENTAGON_EXT_PRE = P("pentagon_ext_pre")
PENTAGON_AERIAL_PRE = P("pentagon_aerial_pre")
PENTAGON_COURT_PRE = P("pentagon_court_pre")
PENTAGON_WEST_DAY = P("pentagon_west_day")
# ── 軍
F15_ALERT = P("f15_alert")
F15_TAKEOFF = P("f15_takeoff")
F16_ALERT = P("f16_alert")
F16_TAKEOFF = P("f16_takeoff")
BASE_RWY = P("base_rwy")
FIGHTER_DC = P("fighter_dc")
ANDREWS = P("andrews")
# ── 当日
WTC_SMOKE_DAY = P("wtc_smoke_day")
FIRE_TRUCKS_DAY = P("fire_trucks_day")
SHANKSVILLE_DAY = P("shanksville_day")
APRON_DAY = P("apron_day")
APRON_LINED_DAY = P("apron_lined_day")
STOPPED_DAY = P("stopped_day")
STRANDED_DAY = P("stranded_day")
# ── 記録・書類
REPORT_COVER = P("report_cover")
REPORT_PAGE = P("report_page")
HEARING = P("hearing")
LIBRARY_REPORTS = P("library_reports")
NIST_REPORT = P("nist_report")
RECORDER = P("recorder")
ATC_TAPE = P("atc_tape")
LOGBOOK = P("logbook")
# ── 「今」
SECURITY_NOW = P("security_now")
COCKPIT_DOOR_HARD = P("cockpit_door_hard")
ARTCC_NOW = P("artcc_now")
LOBBY_NOW = P("lobby_now")
# ── 空
CLEAR_SKY = P("clear_sky")


def report():
    """在る写真を1枚ずつ出す（縦横比と額装／全画面の判定つき）。

        python -c "import sys;sys.path.insert(0,'tools');import cuts.ss as ss;ss.report()"
    """
    fs = sorted(REF.glob("*.jpg"))
    if not fs:
        print("🔴 ref/ep7/ に写真が1枚も無い（`python qa_out/ep7_assets.py fetch`）")
        return
    for f in fs:
        n = f"ep7/{f.name}"
        w, h = trimmed_size(n)
        a = aspect(n)
        print(f"  {f.stem:24} {w:>5}x{h:<5} 縦横比 {a:5.2f}  "
              f"{'額装' if (a < PANEL_AR or a > WIDE_AR) else '全画面'}  "
              f"切り落とし {crop_loss(n) * 100:4.1f}%  {f.stat().st_size // 1024}KB")
    print(f"  ── 計 {len(fs)}枚")
