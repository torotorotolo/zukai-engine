# -*- coding: utf-8 -*-
"""16本目（1963年 バイオントダム災害・イタリア・約1,910人）の章ファイルが共通で使う小道具。

**15本目（リノ・エアレース2011）の中身は git の `c646174` にある**（`git show c646174:tools/cuts/ss.py`）。
14本目（セウォル号）は `dc6ecf4`、13本目（トルコ航空981便）は `b54ee4f`、12本目（キャッスル・ブラボー）は `3832147`、
11本目（チャレンジャー号）は `61039d2`、10本目（三豊百貨店）は `46f11b3`、9本目（テネリフェ）は `e18b8f1`、8本目は `4c71bf0`、
7本目は `ae30d49`。

🔴 **⑤b-1（2026-10-01・16本目）で空にした**＝§0b。15本目の束の定数（顔だけモザイクの CC BY 写真2点 NEEDS_MASK）は外した。
15本目の型の値（案C の出典の表・時計と秒の札・軸の型・地図5範囲・棒・書類の再現図・鎖と箱）は、門番の selftest の見本
`tools/fixture_ep15.py` へ移した（値は1つも変えていない＝git の `c646174` と同じ）。14本目の型の値は `tools/fixture_ep14.py`
（2026-09-30 に移した・git の `dc6ecf4`）。16本目の束は写真の束のチャットで作る。
⚠️ 下の「素材の名前」「人が写る点の扱い」は**15本目の書きぶりのまま**＝16本目の束のチャットで `ref/ep16/` の名前と人の扱いに書き替える。

■ 素材の名前（`ref/ep15/`。選び方と出どころは台本 `ref/ep15/daihon_v2.md` §7・②の台帳 `ref/ep15/materials.md`）
  `ep15/<欄の名>.jpg` … 写真（Commons 19点＝⑤b-6・`qa_out/ep15_assets.py build`）
  `ep15/pg<頁>_fig<NN>.jpg` … 報告書の courtesy の写真＝**紙面の引用**（図・説明の行・撮影者の行まで・`frame=True`＝額装だけ）
  `ep15/pg<頁>.png`   … NTSB の報告書 AAB-12/01・ドケットの頁（台本の頁番号）＝切り口はカットごと（下の `ptrim`）
  🔴 空にした直後は**未作成**＝`_assets()` が止める（権利を確かめずに焼かない）。
     ⚠️ 写真を1点も当てていないうちは `cuts/__init__.py` が額装の網を呼ばない（照合する点が無い）。1点でも当てたら要る

■ 🔴 人が写る点の扱い（この回）＝ルール §B2-1・§B2-2・台本 §1-3／§7
  ・観客は私人＝**顔と名前は出さない**（事故の日の写真・報告書の courtesy の写真に写る人）
  ・報告書の courtesy の写真（図4〜10・15〜17）は**紙面の引用**＝頁ごと・額装・無加工・撮影者名と NTSB（ルール §2-6c）
  ・事故の日の事故機の写真（CC BY-SA 2.0）ほか BY-SA の点は**額装・1点1カット**（映像方針 §1 線3）
  ・パイロットの実名は c107・c408 だけ（09-26 承認）→ [[feedback-jiko-photo-people-policy]]

■ 寄せ方（focus）
  `build_jiko.fit()` は「箱を覆う」切り出しで、`xbias`/`bias` は**余ったぶんの寄せ**（0〜1）。
  🔴 画像の縦横比が要るので**実物を開いて測る**（推定で置かない）。
  ⚠️ **切ったあとの寸法で測る**。切る前の寸法で逆算すると、寄せが全部ずれる。
"""
import json
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
REF = HERE / "ref" / "ep16"
EP = "ep16/"
W, H = 1920, 1080

# 画面の縦横比。これより縦長／横長の図は額装パネルに回す。
# 🔴 上限と下限は対。片側だけにすると粗が反対側へ移る（[[feedback-kinsoku-needs-both-ends]]）。
SCREEN_AR = W / H
# ✅ 2026-09-24（13本目 ⑤b-2）に**13本目の束で取り直した**（→ [[feedback-per-episode-constants-go-stale]]）。
#    `python qa_out/ep13_assets.py panel` の22点の並びで、いちばん大きな切れ目は AR 0.992（finnair_dc10）→
#    1.263（dc10_cabin・dc10_flight_1971）の 27ポイント＝その中点 1.1275 を丸めて 1.13。
#    （12本目は 1.049→1.200 の中点 1.12。値が近いのは偶然）
#    ⚠️ BY-SA の点は縦横比にかかわらず額装だけ（下の `FRAME_ONLY`）。
#    ✅ 2026-09-29（14本目 ⑤b-7a）に**14本目の束（22点）で取り直した**。`python qa_out/ep14_assets.py panel` の並びで、
#       16:9 より縦長の側のいちばん大きな切れ目は AR 1.517（search_divers_0504）→ 1.650（search_ship21_0419）の 13ポイント
#       ＝中点 1.58（次は 1.351→1.473 の 12ポイント）。4:3 の3点（学校2・ソウル広場）と K1 は額装、3:2 の BY-SA は額装だけ（権利）。
#       WIDE_AR＝2.00＝site_0418（2.21・PD）は額装（横に 19.5% 切れるのを避ける）。gwanghwamun_2018 は切り出しのあと 1.97＝全画面
#    ✅ 2026-09-30（15本目 ⑤b-6）に**15本目の束（写真19点＋courtesy の紙面8点）で取り直した**。
#       `python qa_out/ep15_assets.py panel` の並びで、16:9 より縦長の側のいちばん大きな切れ目は AR 1.505（事故の週の
#       tataquax の5点・3:2）→ 1.700（damage_1970）の 19.5ポイント＝中点 1.60（次は 1.353→1.385 の 3.2ポイント）。
#       ⚠️ 27点のうち額装だけでない（`kind()` が効く）のは CC BY の3点だけ（gg_nose_2010・gg_pit_2010・seminar_2016）
PANEL_AR = 1.60                     # これ未満＝縦長すぎ（上下が切れる）
WIDE_AR = round(SCREEN_AR * SCREEN_AR / PANEL_AR, 2)   # ＝1.98。これ超＝横長すぎ

# 報告書の頁から切る図の矩形（写真と頁の束のチャットで作る `ref/<回>/pages.json`＝15本目は `ref/ep15/pages.json`）。
_PAGES_FILE = REF / "pages.json"
PAGES: dict[str, dict] = (json.loads(_PAGES_FILE.read_text(encoding="utf-8"))
                          if _PAGES_FILE.exists() else {})
BANDS = {k: v for k, v in PAGES.items() if v.get("fig_box")}

# 画素で測った切り出し。⚠️ **原寸を見てから足す**（推定で置かない）。
#   12本目の4点（fo_tray・fo_tank・rongelap_booties・jp_fish_sign）は git の `3832147`。
#   🔴 2026-09-28（14本目 ⑤b-1）：13本目の23点（仏の報告書・上院・SB・AD の頁と、人の顔を外した写真2点）は
#      git の `b54ee4f`（`git show b54ee4f:tools/cuts/ss.py`）。次の回にも効く教訓だけ残す：
#     ・頁の切り口は「その近くでインクが最も少ない行」＝行の途中で切らない。寄り（窓が尺の間に縮む）で端の行が
#       欠けるので、切り口は寄りの掃きが届かない所へ（13本目 c504・c520＝門番 `edges` が拾った）
#     ・写真の頁は写真だけ（頁番号・印・説明文を落とす）。斜めの写真は水平の切り口で分けきれない（13本目 p95）
#     ・人の顔を外す切り出しは 16:9 ちょうどに（13本目 dc10_cabin・klm_cockpit_1972）
#   🔴 2026-09-29（14本目 ⑤b-7a）：**頁の切り出しは `pages.json` の `trim` から読む**（下の update＝手で写さない）。
#      `qa_out/ep14_assets.py pages` が、文字の頁は目印の語の行（`ANCHOR`）から、図の頁は測った行・画像の位置（`FIGVEC`）
#      から決めて書く。ここに手で書くのは写真の切り出しだけ
#   🔴 2026-09-30（15本目 ⑤b-1）：14本目の写真の切り出し2点（私人の顔と名前を外した光化門 2018・救命胴衣の列 2017）は
#      git の `dc6ecf4`。残す教訓＝**私人の顔と名前は 640px のシートでは見えない**（原寸の切り出しで見つけた＝§5b-97）。
#      切り出しで外したら、外した範囲を下の `PRIVATE_OUT` にも書く（門番 photomask が全カットの窓と照らす）
TRIM: dict[str, tuple] = {
}
TRIM.update({f"{EP}{k}.png": tuple(v["trim"]) for k, v in PAGES.items() if v.get("trim")})
# 🔴 2026-09-30（15本目 ⑤b-6）：**頁の切り口はカットごと**（同じ頁を2カットで別の所を切る＝p15 c507・c611／p32 c105・c708／
#    p35 c409・c601／p37 c618・c703）。`qa_out/ep15_assets.py pages` が `pages.json` の `cuts` に書く＝章ファイルは
#    `photo=ss.page(N), trim=ss.ptrim("c…")`（頁ごとの `TRIM` は置かない＝どのカットにも黙って効く切り口を作らない）
PAGE_CUT_TRIM: dict[str, tuple] = {cid: tuple(t) for v in PAGES.values() for cid, t in (v.get("cuts") or {}).items()}


def ptrim(cid):
    """カットの頁の切り口（頁の割合 x0,y0,x1,y1）。`pages.json` に無ければ止める（黙って頁全体を出さない）。"""
    if cid not in PAGE_CUT_TRIM:
        raise KeyError(f"{cid} の頁の切り口が無い（`qa_out/{EP[:-1]}_assets.py` の PAGE_CUTS に足して pages）")
    return PAGE_CUT_TRIM[cid]


def page(pr):
    """台本の頁番号 → 頁の画像のパス。

    🔴 章ファイルは**台本の頁番号だけ**を書く（`ss.page(N)`）。台本 §7 と1対1で照合できる。
    ⚠️ `PAGES` に無い頁を呼んだら止まる（黙って別の頁を出さない）。
    """
    key = f"pg{pr}"
    if key not in PAGES:
        raise KeyError(f"頁 p{pr} は焼いていない（`qa_out/{EP[:-1]}_assets.py` の PAGES_PICK に足して pages）")
    return f"{EP}{key}.png"


def P(name):
    """欄の名前 → `ref/` から見た写真のパス。"""
    return f"{EP}{name}.jpg"


def fb(cid):
    """動く映像を当てたカットの**ひかえの静止画**（`footage.USE` が取れなかったとき）。

    ⚠️ 取れなかったことは**黙って静止画に落ちる**＝⑥で `✓ 切り出し完了 N/N` を数える
    → [[feedback-fetch-failure-falls-back-to-a-still]]
    """
    return f"{EP}fb_{cid}.jpg"


# ══════════════════════════════════════════════════════════
#  🔴🔴 継承（ShareAlike）つきの点＝**額装だけ**（13本目・10本目の決めと同じ）
# ══════════════════════════════════════════════════════════
#   13本目の②は継承つきを外していない（事故機 TC-JAV の4点は全部 CC BY-SA）＝台帳 §10-2「額装で進める」。
#   ⚠️ 11・12本目の「継承つきは1点も入れない」網のままだと、TC-JAV を当てた時点で読み込みが止まる
#      ＝⑤b-2（09-24）で**額装の網へ戻した**（10本目 `edaf66c` の `FRAME_ONLY`／`check_frame_only`）。
#   🔴 10本目との違い：**色を変えない（`color=1.0` 必須）とカメラ（`cam=`）も止める**。
#      10本目は額装でもデュオトーンをかけていた（`build_jiko.tone()`＝色の置き換え＝改変）。
#      記憶 [[reference-cc-by-sa-unmodified-in-video]]「無加工・丸ごと・色を変えない・上に重ねない」に合わせた。
#   🔴 **1点1カット**（切れない＝寄りを変えて同じ点を2回使う逃げ道が無い）。
#   額装専用かは `assets.json` の権利から**起動時に読む**（表を手で写さない）。
#   ⚠️ `assets.json` が読めなければ**止める**（0点にして素通りさせない）→ [[feedback-parsers-fail-closed]]
@lru_cache(maxsize=None)
def _assets():
    p = REF / "assets.json"
    if not p.exists():
        raise RuntimeError(
            f"ref/{EP}assets.json が無い（⑤b-2 で `python qa_out/{EP[:-1]}_assets.py build`）。"
            "権利を確かめずに焼かない → feedback-parsers-fail-closed")
    return json.loads(p.read_text(encoding="utf-8"))


def _is_sa(lic):
    return "SA" in str(lic or "").upper().replace("-", " ").split()


def frame_only():
    """額装だけの点 {`ep14/<名>.jpg`: 権利}＝継承つき（BY-SA）と**引用**（`assets.json` の `frame`）。
    1点も読めなければ止める（14本目は捜索11点・J1・M1・AN74 の BY-SA と H1 の引用がある）。
    🔴 2026-09-29（14本目 ⑤b-7a）：引用（当日の沈む船 H1＝Commons の表示に根拠が無い）も「改変しない＝色も切り出しもせず
       額装で置く」（ルール §2-5b）＝BY-SA と同じ網に入れた。読む側＝門番 `check_frame_only`・合成 `build_jiko.meta_of`（寄りとディゾルブを止める）"""
    out = {P(n): r["lic"] for n, r in _assets().items() if _is_sa(r.get("lic")) or r.get("frame")}
    if not out:
        raise RuntimeError("assets.json から継承つきの点が1つも読めない（14本目は捜索の11点ほかがある＝fail closed）")
    return out


def uses_photo(spec):
    """SPEC が写真を1点でも当てているか（`photo=` か `intro=dict(photo=…)`）。"""
    return any(s.get("photo") or (s.get("intro") or {}).get("photo") for s in spec.values())


def frame_only_for(spec):
    """🔴 2026-09-28（14本目 ⑤b-1）：**写真を1点も当てていなければ {}（台帳 `assets.json` を読まない）**。
    1点でも当てたら `frame_only()`＝台帳が無ければ止まる（fail closed のまま）。

    回を切り替えた直後は台帳（⑤b-2 で作る）が無い。ここを通さずに `frame_only()` を呼ぶと、
    `import cuts`（`check_frame_only`）と合成（`build_jiko.meta_of`）が落ち、写真を使わない試し焼きも門番も全部止まった
    （14本目 ⑤b-1 の Actions で合成の側が落ちた＝呼び出し元は2か所・ここに1か所でまとめた）。
    """
    return frame_only() if uses_photo(spec) else {}


# 額装の約束を破る書き方（10本目の一覧＋`cam`）。🔴 `zoom` は 1.0 ちょうどなら可・`panel=True` と `color=1.0` は必須
_BREAKS_FRAME = ("trim", "veil", "vignette", "focus", "xbias", "bias", "ann", "mark", "blur", "cam", "intro")


def check_frame_only(spec):
    """継承つきの点を、切る・色を変える・重ねる型に渡しているカット／2回使っているカットを挙げる（空なら合格）。

    ⚠️ `intro=dict(photo=…)`（冒頭の秒だけ写真を全画面）も**全画面＝切る**ので、継承つきの点を渡したら止める。
    ⚠️ 写真を1点も当てていなければ照合する点が無い＝台帳を読まずに合格（`frame_only_for`）。
    """
    fo = frame_only_for(spec)
    bad, seen = [], {}
    for cid, s in sorted(spec.items()):
        ph = s.get("photo")
        intro_ph = (s.get("intro") or {}).get("photo")
        if intro_ph in fo:
            bad.append(f"{cid}＝intro の {intro_ph}（{fo[intro_ph]}）: 冒頭の全画面は切る＝継承つきは使えない")
        lic = fo.get(ph)
        if lic is None:
            continue
        seen.setdefault(ph, []).append(cid)
        why = [k for k in _BREAKS_FRAME if s.get(k) is not None]
        if not s.get("panel"):
            why.append("panel=True が無い（全画面＝上下左右が切れる）")
        if float(s.get("zoom") or 1.0) != 1.0:
            why.append(f"zoom={s.get('zoom')}（1.0 以外は切る）")
        if float(s.get("color") or 0.0) < 1.0:
            why.append(f"color={s.get('color')}（1.0 未満はデュオトーンで色を置き換える＝改変）")
        if why:
            bad.append(f"{cid}＝{ph}（{lic}）: " + "・".join(why))
    for ph, cids in sorted(seen.items()):
        if len(cids) > 1:
            bad.append(f"{ph}（{fo[ph]}）を {len(cids)}カットで使っている（{'・'.join(cids)}）＝1点1カット")
    return bad


def check_card_mix(spec, heads, fo=None):
    """🔴 2026-09-30（15本目 ⑤c'・ルール §5b-110）：章の扉の地（`build_jiko.card_frame`）は、頭のカットの写真を章の色で
    **染めて全画面に拡大して**混ぜる（既定 0.36）＝額装だけの点（BY-SA・courtesy の紙面の引用＝`frame_only`）を頭に持つ章は、
    カットの SPEC に `card_mix=0` を**書く**（書かなければ既定で混ざる＝止める）。空なら合格。
    15本目 c300card（報告書の図5＝courtesy）・c400card・c800card（BY-SA）＝640px のシートで見つけた（門番は扉を見ていなかった）。
    12〜14本目の扉も同じ作り（公開ずみ＝直さない）。呼ぶ側＝`scene_jiko`（扉の一覧 CARD_HEADS が決まった直後・読み込みで止める）
    fo＝額装だけの点の表（selftest が見本を渡す＝回の台帳に左右されない）。本番は渡さない＝assets.json から読む"""
    fo = frame_only_for(spec) if fo is None else fo
    bad = []
    for cid in sorted(heads):
        s = spec.get(cid) or {}
        ph = s.get("photo") or (s.get("intro") or {}).get("photo")
        if ph in fo and float(s.get("card_mix", 1.0)) > 0:
            bad.append(f"{cid}＝{ph}（{fo[ph]}）: 扉の地に染めて拡大して混ぜる（card_mix={s.get('card_mix', '未記入＝既定 0.36')}）"
                       "＝額装の約束（無加工・丸ごと・色を変えない）を外れる → SPEC に card_mix=0")
    return bad


# ══════════════════════════════════════════════════════════
#  🔴🔴 使わない写真（シートで見て落とした。**使うと `cuts` の読み込みで止まる**）
# ══════════════════════════════════════════════════════════
#   `cuts/__init__.py` が SPEC を組んだあとに照合し、当たれば RuntimeError にする。
#   ⚠️ ここに無い点は「まだ見ていない」だけで、「危険が無い」ではありません。
NG_PHOTOS: dict[str, str] = {}

# 🔴 元画像そのものを直してから焼く点（私人の顔・名前）。
#    ⚠️ **`blur=` は書けるように見えて誰も読まない**（10本目で私人の顔が素のまま焼けた）。
#       隠すなら元画像を直し、`ref/<回>/masked.json`（`REF` から引く）に md5 を記録する。
#    → [[feedback-settings-may-not-reach-the-picture]]／[[feedback-jiko-photo-people-policy]]
#    🔴 2026-09-28（14本目 ⑤b-1）：13本目の1点（慰霊の名前の壁 names_wall・c814）を外した＝git の `b54ee4f`。
#       ⚠️ CC BY-SA の点は隠すこと自体が翻案＝使わない（ルール §B2-2）。隠せるのは改変を許す権利の点だけ
#    🔴 2026-10-01（16本目 ⑤b-1）：15本目の2点（gg_nose_2010・gg_pit_2010＝顔だけモザイク）を外した＝git の `c646174`。
NEEDS_MASK: dict[str, str] = {
}

# 🔴 2026-09-29（14本目 ⑤b-7a）：**切り出し（`TRIM`）で外した私人の範囲**（元画像の割合 x0,y0,x1,y1・何か）。
#    門番 photomask が「その写真を使う全カットの窓（`trim` か `TRIM`・冒頭の写真は切らない＝全体）がこの範囲に
#    1画素も入らない」を見る（NEEDS_MASK は元画像を直す点だけ＝切り出しで外した点を見ていなかった）。範囲は原寸で見て測った
#    🔴 2026-09-30（15本目 ⑤b-1）：14本目の2点（光化門 2018 の板・救命胴衣の列 2017 の奥の人）を外した＝git の `dc6ecf4`。
#       15本目は観客（私人）が写る写真が多い（事故の日の BY-SA・courtesy の頁）＝外す範囲は写真の束で原寸で見て書く
PRIVATE_OUT: dict[str, list] = {
}


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
       （2026-09-08 に実際に起きた）→ [[feedback-gates-blind-to-the-new-material]]
    """
    sw, sh = size_of(name)
    t = TRIM.get(name)
    if t:
        x0, y0, x1, y1 = t
        return max(1, int(sw * (x1 - x0))), max(1, int(sh * (y1 - y0)))
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


# 画素が足りない点も額装に回す（伸ばせないものを伸ばさない）。
# ⚠️ 上限と下限は対（[[feedback-kinsoku-needs-both-ends]]）＝縦横比と画素の両方で見る。
MIN_FULL_W = 1280        # 全画面にしてよい最小の幅（②の網の敷居と同じ値）


def kind(name):
    """`dict(panel=True)` か `dict()` を返す。**縦横比と画素で決める。目で決めない。**"""
    if PANEL_AR is None:
        raise RuntimeError(f"cuts/ss.py の PANEL_AR が未測（この回の束で `qa_out/{EP[:-1]}_assets.py panel` から決める）")
    a = aspect(name)
    w, _ = trimmed_size(name)
    return (dict(panel=True)
            if (a < PANEL_AR or a > WIDE_AR or w < MIN_FULL_W) else dict())


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


# ══════════════════════════════════════════════════════════
#  動く映像（14本目＝米海軍の捜索の映像 PD・⑤b で決める。13本目は0本・12本目は2本）
# ══════════════════════════════════════════════════════════
@lru_cache(maxsize=None)
def _clips():
    p = REF / "clips.json"
    if not p.exists():
        raise RuntimeError(f"ref/{EP}clips.json が無い（動く映像を使うなら ⑤b で作る）")
    return json.loads(p.read_text(encoding="utf-8"))


def vid(cid, **kw):
    """動く映像のカット（ひかえの静止画つき）を1行で書く。秒は `footage.USE` が持つ。"""
    return dict(photo=fb(cid), **kw)


# ══════════════════════════════════════════════════════════
#  動く模式図（drift）の地図
# ══════════════════════════════════════════════════════════
#   🔴 12本目のもの（ビキニ・船・捜索・艦隊・島の表示範囲と照合の宣言 `*_REL`、`drift_map()`・`isles_map()`）は
#      ⑤b-1（2026-09-24）で外した＝git の `3832147`。
#   🔴 13本目のもの（PARIS・ROUTE・AA96・EUROPE の範囲・札の置き場・照合の宣言と `paris_map()`・`route_map()`・
#      `aa96_map()`・`europe_map()`）は ⑤b-1（2026-09-28）で外した＝git の `b54ee4f`。
#   14本目は ⑤b-4 で作る（承認ずみの地図6＝航路 c111・変針と航跡 c604〜c611・集まる船 c812＋追補の地図6）。
#   次の回にも効く教訓（13本目）：
#     ・札を線から逃がす（線が名札を貫く＝§5b-39）。札どうしがくっつくと1語に読める＝dx で離す
#     ・`view` の経度の幅は枠（1696×582）の縦横比に合わせる（経緯線が枠いっぱいに出る）
#     ・報告書の方角が8方位の言い方なら `sector=8` で照合（`check_drift`）
#     ・都市の位置が報告書に無いときは Wikidata の座標＝照合の宣言に入れない（地点は `titan_fig.GEO`）


# ══════════════════════════════════════════════════════════
#  案C の再現イラスト（`tools/illu.py`・門番 `check_illu`）── 14本目 ⑤b-2（2026-09-28）新設
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：次の回は下の4つを**その回の資料と時刻**に替える。
#   REC_PAGES … 部品の出典（`rec=`）を当てる原文（`=== p<N> ===` で頁を割った1ファイル＝④ の make_pages.py の出力）
#   REC_DOCS  … 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面に出す名前・頁の出し方（print＝印字の頁／pdf＝PDF の頁）
#   ILLU_SPLIT_TIMES … 資料で割れる時刻（台本 §1-5）＝**画面に時計・時刻の札として出さない**（ルール §5b-74①）
#   ILLU_CROWD_UNTIL … 乗客の群れを描いてよい場面の時刻の上限（この時刻**より前**だけ）。14本目＝3階の手すりが水に
#                      つかった 9時47分（判決 p18「09:47경 세월호의 3층 난간이」）＝水が入った後の船内に乗客を描かない（§5b-74②）
# 🔴 2026-10-01（16本目 バイオントダム災害 ⑤b-1・§0b）：15本目の値は selftest の見本 `tools/fixture_ep15.py` へ移した
#    （値は1つも変えていない＝git の `c646174`）。16本目の値は、その型を初めて使う ⑤b のチャットで入れる
#    （空のあいだ、その型を使うカットは門番・型が止まる＝fail closed）。
#   16本目の予定（映像方針 §9）：REC_DOCS＝S1 議会の調査委員会の最終報告（ep16_pages.txt の p1〜p248）・S8 学術の総説（p1041〜）・
#     S9（p2001〜）・S10（p3001〜）／ILLU_CLOCK_OK＝"22:39" だけ／ILLU_SPLIT_TIMES＝22:00・22:15（電話）／
#     ILLU_SEC_OK＝空（秒の札は出さない）／ILLU_ROLES＝住民の群れ（顔の無い影・数えない形）だけ／
#     ILLU_CROWD_UNTIL＝使わない（水の面が触れたら消す＝門番⑭・案）／
#     ILLU_COUNTS＝ダム1・塊1（模型の想定は2）・北の岸の印2・トンネル1・道の入口2
# 🆕 2026-10-01（16本目 ⑤b-2）：16本目の値を入れた（案C を初めて使うチャット）。頁の番号は台本 第2版の冒頭の表
#    （`ref/ep16/daihon_v2.md`「出典欄の略号と頁」）＝原文の通し頁ファイルの番号：S1＝PDF の頁のまま p1〜p248（PDF98＝印刷98・
#    🔴 PDF146＝印刷147・PDF147＝印刷146）・S8＝冊子の頁 41〜52＝p1041〜p1052・S9＝PDF の頁 p2001〜p2019・S10＝PDF の頁
#    p3001〜p3025（PDF20＝印刷21）。#100＝形のもと（1934年の地形図＝画像・原文の頁ファイルに無い＝`text=False` で頁の照合を飛ばす
#    ＝範囲 p1 だけ見る）。画面の名は語りの呼び名に合わせた（議会の調査委員会・学術の総説・バイオント財団の年表・歴史家）
REC_PAGES = REF / "src" / "ep16_pages.txt"      # ④ の make_pages.py の出力（git の外＝手元だけ）
REC_DOCS = {
    "S1": dict(range=(1, 248), name="イタリア議会 調査委員会 最終報告（1965年）", page="pdf", base=0),
    "S8": dict(range=(1041, 1052), name="学術の総説（Genevois・Ghirotti 2005）", page="print", base=1000),
    "S9": dict(range=(2001, 2019), name="バイオント財団の年表", page="pdf", base=2000),
    "S10": dict(range=(3001, 3025), name="歴史家 Reberschak ほか（2023年）", page="pdf", base=3000),
    "#100": dict(range=(1, 1), name="イタリア軍地理院 地形図（1934年）", page=None, base=0, text=False),
}
# 割れる時刻＝最後の電話（財団の年表 22時＝S9 PDF17／少数派の報告 22時15分＝S1 PDF228）＝画面に時計の札として出さない
ILLU_SPLIT_TIMES = ("22:00", "22:15")
ILLU_CROWD_UNTIL = None
ILLU_ROLES = dict(sprite=(), crowd=())      # 置いてよい役割（門番 check_illu ②）＝空の組なら、どの役割も置けない（fail closed）
# 🔴 秒の札は出さない（空＝全部止める＝門番 check_illu ⑤ `judge_labels`）。崩れて湖に入るまでの「45秒足らず」（S8 p.41）・
#    波が町に届くまでの時間（記録に無い）を札にしない＝冒頭は「動きの速さは縮めてある」と出典の行で断る（映像方針 §1-3）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）
# 時計の札は 22時39分だけ（S1 PDF98・PDF147・PDF207・S8 p.41・S9 PDF17 が一致＝資料が1つに決まる時刻）
ILLU_CLOCK_OK = ("22:39",)                  # 札に出してよい時計の時刻（門番 check_illu ⑤）
# 描いてよい数＝{部品の obj の名: (数, 出典)}（門番 check_illu ③'＝場面ごとに部品の obj を足した数が記録と同じ）。
#   🆕 16本目 ⑤b-2（置き場 VA）：ダム1・崩れたあとの塊1・北の岸の印2・迂回トンネル1・道の入口2。町と村と湖岸の集落は建物の面
#   （数えない形＝obj を持たない）。⚠️ 模型の想定の2つの塊（VB の c508・c509・c807）は別の名で足す（⑤b-3〜⑤b-4）
ILLU_COUNTS = dict(dam=(1, "S1 p171"), block=(1, "S1 p147"), north_marks=(2, "S1 p146"), tunnel=(1, "S1 p85"),
                   road_gates=(2, "S1 p98"),
                   # 🆕 ⑤b-4（VD）：模型の想定の2つの塊＝マッサレッツァの沢の東と西（実際の塊 block とは別の名）・1960年11月4日の崩落の2か所
                   model_blocks=(2, "S1 p224"), collapse1960=(2, "S1 p72"))
# 🆕 16本目 ⑤b-2：想定の札（起きた事ではない絵＝左上「再現イラスト」の下の琥珀の札）を出すカットと札の言葉（門番 check_illu ④＝
#   表のカットは札が要る・表に無いカットに札を出さない）。🆕 ⑤b-4：模型の想定（VD の c507〜c509・c513）。⚠️ c807 の左は
#   小さく戻す絵＝左上の札を出せない＝パネルの文「模型の想定」で言う（表に入れない）
ILLU_ASSUME = {"c316": "会社の説明（想定）", "c507": "模型の想定", "c508": "模型の想定", "c509": "模型の想定",
               "c513": "模型の想定"}
# 🆕 16本目 ⑤b-3：壊れる物の部品（町と集落の建物の面が消える＝VA の towns／shore が gone・mud／水が町を覆う＝flood／湖の岸の集落へ
#   届く波＝wave_e）を描いてよいカット（門番 check_illu ⑫＝ほかのカットで使えば止める・映像方針 §9 ⑫・10-01 カズヤくん「本編でも
#   町に届くまで描く」）。⚠️ wave_w（ダムを越えて峡谷へ＝町に届かない・c815）は入れない。空なら全部止める（fail closed）
ILLU_DESTROY_CUTS = ("c102", "c814", "c823")

# 🔴 §0b：軸の型（`tools/axis.py`・14本目 ⑤b-5）の「割れる時刻の印」に添える出典の名（`rec=` の資料名 → 画面の名）。
#   語りが資料を呼ぶ名に合わせる（海審の特別調査報告＝語りは「報告書」）。ILLU_SPLIT_TIMES の時刻は、軸の型では
#   **出典の名つきでだけ**出してよい（門番 check_axis ②＝点に by=True か split）
# 🔴 2026-10-01（16本目 ⑤b-1）：空にした（15本目の値＝`tools/fixture_ep15.py`）。REC_DOCS の資料名が決まってから、
#    語りが資料を呼ぶ名に合わせて入れる（軸の型を初めて使う ⑤b のチャットで）
# 🆕 2026-10-01（16本目 ⑤b-5）：語りの呼び名（c701「財団の年表」・c712「少数派の報告」）。"S1 p228"＝頁ごとの名が先（axis.doc_names）
# 🆕 ⑤b-6a：c518 の割れる日（模型の研究所の委員会の意見＝S9 p2012 は3月30日・S1 p225〈少数派〉は4月30日）
AXIS_DOCS = {"S1 p228": "少数派の報告", "S1 p225": "少数派の報告", "S1": "議会の報告書", "S9": "財団の年表"}

# 軸（カットをまたいで同じ軸を使う＝前のカットの点を past で沈めて続ける）。回ごとに `AX_<名> = dict(view, span, ticks)` を足す
# 🔴 2026-10-01（16本目 ⑤b-1）：15本目の軸（AX_HIST・AX_LATE・AX_A08・AX_DRILL・AX_EMS・AX_UPSET・AX_NINE）と
#    部品の並び NINE_PTS は `tools/fixture_ep15.py` へ移した（値は1つも変えていない）。16本目の軸は ⑤b で足す。
#    ⚠️ 軸の教訓は移した注の側にある（年だけの値は年の真ん中に置く・札が枠の端を越えた layout の直し＝fixture_ep15 の AX_*・AXI の上）

# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
# 🆕 2026-10-01（16本目 ⑤b-5）：場面4 10月9日の時刻の帯（c701〜c723 の9カット）。値と頁は ref/ep16/src/ep16_pages.txt で当てた
#   （S9 p2016〜2017＝財団の年表・S1 p98・p228）。🔴 22:00 と 22:15 は割れる時刻の印（split＝出典の名つき・カーソルを置かない）。
#   ⚠️ 目盛りは奇数の時（9〜23時）＝22時の目盛りの字が割れる時刻の印の横に出ない。時計の絵は描かない（映像方針 §6）
AX_DAY = dict(view="clock", span=("9:00", "23:00"),
              ticks=("9:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00", "23:00"))
# ⚠️ ⑤b-5 の門番：22:00・22:15・22:39 は一日の帯では約70画素に3つ＝札が3段に収まらない → 割れる時刻の印は夕方の寄り（c720）だけ。
#   目盛りに22時を置かない（割れる時刻の印の横に時刻の字を出さない）
AX_EVE = dict(view="clock", span=("20:00", "23:00"), ticks=("20:00", "21:00", "23:00"))
# ⚠️ 近い2点の札は左右に振る（§5b-93＝12時↔13時・17時↔17時50分）・札は短く（同じ段に並べる）
AXI = {
    "t0945": dict(k="pt", at="9:45", t="35家族が離れる", rec="S1 p98"),
    "t1200": dict(k="pt", at="12:00", t="動きが見える", rec="S9 p2016", anchor="end"),
    "t1300": dict(k="pt", at="13:00", t="割れ目", rec="S9 p2016", anchor="start"),
    "t1316": dict(k="span", a="13:00", b="16:00", rec="S9 p2016"),                       # 3時間で割れ目が広がる（札は c710 の項目の札）
    "t1516": dict(k="span", a="15:00", b="16:00", t="木が倒れる", rec="S9 p2016", c="ALERT"),
    "t1700": dict(k="pt", at="17:00", t="本部の指示", rec=["S9 p2016", "S1 p228"], anchor="end"),
    "t1750": dict(k="pt", at="17:50", t="電話", rec="S9 p2016", anchor="start"),
    "t2000": dict(k="pt", at="20:00", t="道をふさぐ", rec="S9 p2016"),
    "phone": dict(k="span", a="22:00", b="22:15", t="電話", rec=["S9 p2017", "S1 p228"]),   # 札に時刻を書かない（割れる時刻）
    "s2200": dict(k="split", at="22:00", rec="S9 p2017"),
    "s2215": dict(k="split", at="22:15", rec="S1 p228"),
    "nowarn": dict(k="span", a="20:00", b="22:39", t="下流の町に呼びかけなし", rec=["S1 p228", "S1 p98"], c="ALERT"),
    "t2239": dict(k="pt", at="22:39", t="崩落", rec=["S1 p98", "S9 p2017"], c="ALERT"),
    "day": dict(k="br", a="9:45", b="22:39", rec=["S1 p98", "S9 p2017"]),
}


# 🆕 2026-10-01（16本目 ⑤b-6a）：年表（date）＝第1〜6章の12カット。値と頁は ref/ep16/src/ep16_pages.txt で当てた＝門番
#   check_axis の REC_AXIS と照らす。札は語りの細かさまで（fmt="ym"／"y"＝§5b-93）・近い2点は左右に振る（anchor）
#   ANS＝答えの割れ方（c110）・ENEL＝サーデからエネルへ（c217・c218）・PERMIT＝許された水位（c318）・Y3＝3年の流れ（c322）・
#   EXP＝専門家の報告（c401・c402・c407）・MERLIN＝メルリンの記事（c421）・MODEL＝模型の歩み（c518・c523）・Y63＝1963年（c604）
AX_ANS = dict(view="date", span=("1963-01", "1972-06"), ticks=("1964", "1966", "1968", "1970", "1972"))
AX_ENEL = dict(view="date", span=("1962-10", "1963-06"), ticks=("1962-11", "1963-01", "1963-03", "1963-05"))
AX_PERMIT = dict(view="date", span=("1961-10", "1962-07"),
                 ticks=("1961-11", "1962-01", "1962-03", "1962-05", "1962-07"))
# ⚠️ ⑤b-6a の qa_all（layout）：1960年7月からだと左の端の点（崩落）の札が画面の左へはみ出した＝軸の左に余白（§5b-107④）
AX_Y3 = dict(view="date", span=("1960-01", "1963-07"), ticks=("1960", "1961", "1962", "1963"))
AX_EXP = dict(view="date", span=("1959-10", "1961-05"),
              ticks=("1960-01", "1960-04", "1960-07", "1960-10", "1961-01", "1961-04"))
AX_MERLIN = dict(view="date", span=("1959-01", "1961-04"), ticks=("1959", "1960", "1961"))
AX_MODEL = dict(view="date", span=("1960-09", "1963-12"), ticks=("1961", "1962", "1963"))
AX_Y63 = dict(view="date", span=("1962-05", "1963-11"), ticks=("1962-07", "1963-01", "1963-07"))
AXI.update({
    # ── c110 答えの割れ方（S1 p26＝19対8で多数派の報告を可決・通らなかった2つの案は最終報告に添える／S9 p2018＝判決3回）
    #    判決の名（一審・控訴審・破毀院）は後の章で初めて説明する＝ここは「判決」とだけ
    "a_fall": dict(k="pt", at="1963-10-09", t="崩落", rec=["S1 p98", "S9 p2017"], c="ALERT", fmt="y"),
    "a_parl": dict(k="pt", at="1965", t="議会の報告書", rec="S1 p26", c="INST"),
    "a_j1": dict(k="pt", at="1969-12-17", t="判決", rec="S9 p2018", fmt="y", anchor="end"),
    "a_j2": dict(k="pt", at="1970-10-03", t="判決", rec="S9 p2018", fmt="y"),
    "a_j3": dict(k="pt", at="1971-03", t="判決", rec=["S9 p2018", "S10 p3020"], fmt="y", anchor="start"),
    # ── c217・c218（S1 p90＝1962年12月6日の法律でエネルを設立・p91＝1963年3月14日の大統領令でサーデの事業をエネルへ）
    "n_enel": dict(k="pt", at="1962-12-06", t="エネルができる", rec="S1 p90", fmt="ym", c="INST"),
    "n_move": dict(k="pt", at="1963-03-14", t="事業がエネルへ", rec="S1 p91", fmt="ym", c="INST"),
    # ── c318 ダム局の許可（S9 p2011・p2012・S1 p92）＝札は水位だけ（月は目盛りで読む）・最後の700m だけ年月（語りが言う）
    "p640": dict(k="pt", at="1961-11-16", t="640m", rec="S9 p2011", lab=False),
    "p655": dict(k="pt", at="1961-12-23", t="655m", rec="S9 p2012", lab=False),
    "p675": dict(k="pt", at="1962-02-06", t="675m", rec="S9 p2012", lab=False),
    "p700": dict(k="pt", at="1962-06-08", t="700m", rec=["S1 p92", "S1 p33"], fmt="ym", big=True),
    # ── c322 3年の流れ（崩落 S1 p72・ミュラーの報告 p76・模型の報告 p89・715m を求める p92）
    "y_fall": dict(k="pt", at="1960-11-04", t="崩落", rec="S1 p72", c="ALERT", fmt="ym", anchor="end"),
    "y_mul": dict(k="pt", at="1961-02-03", t="ミュラーの報告", rec="S1 p76", fmt="ym", big=True, anchor="start"),
    "y_model": dict(k="pt", at="1962-07-03", t="模型の報告", rec="S1 p89", fmt="ym"),
    "y_715": dict(k="pt", at="1963-03-20", t="715mを求める", rec="S1 p92", fmt="ym"),
    # ── c401・c402・c407 崩落の前の専門家の報告（揺れで地下を調べた報告 S1 p36〈1960年2月4日〉・2人の地質学者 p73〈1960年6月〉・
    #    ミュラー p76〈1961年2月3日〉）。c407 の「1957年から」は S9 p2004（1957年8月6日＝会社が頼んだ2本目の報告）＝項目の札
    "e_caloi": dict(k="pt", at="1960-02-04", t="揺れで地下を調べる", rec=["S1 p36", "S9 p2006"], fmt="ym"),
    "e_geo": dict(k="pt", at="1960-06", t="2人の地質学者", rec="S1 p73", fmt="ym"),
    "e_fall": dict(k="pt", at="1960-11-04", t="崩落", rec="S1 p72", c="ALERT", fmt="ym"),
    "e_mul": dict(k="pt", at="1961-02-03", t="ミュラーの報告", rec="S1 p76", fmt="ym"),
    # ── c421 メルリンの記事（S1 p39＝1959年5月5日の記事・1960年11月30日 ミラノの裁判所で無罪／S9 p2005・S1 p220＝訴えの名）
    "m_art": dict(k="pt", at="1959-05-05", t="ウニタの記事", rec=["S1 p39", "S9 p2005"], fmt="ym"),
    "m_free": dict(k="pt", at="1960-11-30", t="無罪", rec="S1 p39", c="OK"),
    # ── c518・c523 模型の歩み（会社の記録 S1 p75・模型をつくる p89〈1961年の夏＝年の真ん中〉・委員会の意見＝🔴 月が割れる
    #    〈S9 p2012＝3月30日・S1 p225＝4月30日〉＝割れる日の印2つ・同じ札・出典の名つき・ゲッティの報告 p89）
    "md_note": dict(k="pt", at="1960-11-16", t="会社の記録", rec="S1 p75", fmt="ym"),
    "md_build": dict(k="pt", at="1961", t="模型をつくる", rec="S1 p89"),
    # ⚠️ ⑤b-6a の門番 check_axis：4月の印の札を右へ出すと、すぐ右のゲッティの報告（段が上）の縦の線が札を貫いた＝割れる日の札は
    #   2つとも左へ（段を分ける）・ゲッティの報告は年月まで（語りの c511 が日まで言う）で右へ＝札が 1963年3月の縦の線に届かない
    "md_s1": dict(k="split", at="1962-03-30", t="委員会の意見", rec="S9 p2012", fmt="ym", anchor="end"),
    "md_s2": dict(k="split", at="1962-04-30", t="委員会の意見", rec="S1 p225", fmt="ym", anchor="end"),
    "md_rep": dict(k="pt", at="1962-07-03", t="ゲッティの報告", rec="S1 p89", big=True, fmt="ym", anchor="start"),
    "md_715": dict(k="pt", at="1963-03-20", t="700mより上を求める", rec="S1 p92", fmt="y", big=True),
    "md_br": dict(k="br", a="1963-03-20", b="1963-10-09", rec=["S1 p92", "S1 p98"]),
    # ── c604 1963年（700m までの許可＝S1 p92〈1962年6月8日〉・715m を求める p92〈1963年3月20日〉）
    "q_700": dict(k="pt", at="1962-06-08", t="700mまでの許可", rec="S1 p92", fmt="ym"),
    "q_715": dict(k="pt", at="1963-03-20", t="715mを求める", rec=["S1 p92", "S1 p33"], big=True),
})


def ax(name, **kw):
    """AXI の部品の写し（同じカットで past と add に同じ物を2回入れても別の部品になる）。"""
    return dict(AXI[name], **kw)


# ══════════════════════════════════════════════════════════
#  🆕 16本目 ⑤b-5（2026-10-01）：場面1 水位と斜面の速さの線（`tools/lv16.py`・門番 check_mech の judge_lv）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の LV_*・LVP は16本目の値（次の回は見本へ移して空にする）。
#   値と頁は ref/ep16/src/ep16_pages.txt で当てた＝門番の側の表（check_mech.REC_LV）と照らされる（§5b-88）。
#   置く日＝月だけの記録は15日・「primi」＝5日・「metà」＝15日・「fine」＝28日（門番の窓の内）。
#   🔴 1962年12月の速さは台本どおり S8 p.46「1.5センチ超」（S1 p90 は「約1センチ」＝資料で割れる・台本の確かめ G2）。
#   🔴 10月8日の報告の「9月の終わりに1日5センチ」は描かない（c611 の26日22ミリと食い違って聞こえる＝台本の確かめ G3-21）
LV_T = "水位と斜面の速さ"      # 見出し＝c619 の合図（断面の図解からグラフへ戻る札・映像方針 §6）。図の札と4字以上の語を重ねない
LV_NOTE = "点＝記録の値・あいだは直線でつないだ模式"
LV_ALL = dict(span=("1960-01-01", "1963-11-01"), ticks=("1960", "1961", "1962", "1963"), zr=(560, 740), zt=(600, 650, 700))
LV_63 = dict(span=("1963-03-01", "1963-10-20"),
             ticks=("1963-03", "1963-04", "1963-05", "1963-06", "1963-07", "1963-08", "1963-09", "1963-10"),
             zr=(640, 730), zt=(650, 675, 700))
VR_LO = dict(vr=(0, 50), vt=(0, 10, 20, 30, 40, 50))       # 1963年10月3日まで（1960年の山＝4センチ近く）
VR_HI = dict(vr=(0, 210), vt=(0, 50, 100, 150, 200))        # 10月8日（約100ミリ）・9日（200ミリ）まで
LVP = {
    # ── 湖の水位（m）──
    "z6003": dict(k="pt", s="z", at="1960-03-15", v=580, rec="S1 p72"),
    "z6010": dict(k="pt", s="z", at="1960-10-05", v=630, rec="S1 p73"),
    "z6011": dict(k="pt", s="z", at="1960-11-04", v=650, rec="S1 p72"),
    "z6101": dict(k="pt", s="z", at="1961-01-08", v=600, rec="S8 p1046"),
    "z6110": dict(k="pt", s="z", at="1961-10-15", v=600, rec=["S1 p88", "S1 p90"]),
    "z6201": dict(k="pt", s="z", at="1962-01-28", v=655, rec="S1 p87"),
    "z6210": dict(k="pt", s="z", at="1962-10-28", v=690, rec="S1 p90"),
    "z6212": dict(k="pt", s="z", at="1962-12-15", v=700, rec=["S1 p90", "S8 p1046"]),
    "z6302": dict(k="pt", s="z", at="1963-02-15", v=680, rec="S1 p90"),
    "z6303": dict(k="pt", s="z", at="1963-03-15", v=650, rec=["S1 p93", "S8 p1046"]),
    "z6304": dict(k="pt", s="z", at="1963-04-10", v=647.5, rec="S1 p226"),
    "z6308": dict(k="pt", s="z", at="1963-08-14", v=705.5, rec="S1 p226"),
    "z6309": dict(k="pt", s="z", at="1963-09-01", v=709.4, rec="S9 p2014"),
    "z6326": dict(k="pt", s="z", at="1963-09-26", v=710, rec="S9 p2014"),
    "z6308o": dict(k="pt", s="z", at="1963-10-08", v=702.5, rec="S1 p96"),
    "z6309o": dict(k="pt", s="z", at="1963-10-09", v=700.4, rec=["S1 p96", "S9 p2017"]),
    # ── 斜面の目印が1日に動く距離（ミリ）。「ほぼ0」は 0 に置く ──
    "v6003": dict(k="pt", s="v", at="1960-03-15", v=0, rec="S1 p72"),
    "v6010": dict(k="pt", s="v", at="1960-10-05", v=0, rec="S1 p73"),
    "v6011": dict(k="pt", s="v", at="1960-11-04", v=40, rec="S1 p73"),
    "v6101": dict(k="pt", s="v", at="1961-01-08", v=0, rec="S1 p85"),
    "v6209": dict(k="pt", s="v", at="1962-09-01", v=0, rec="S1 p92"),
    "v6212": dict(k="pt", s="v", at="1962-12-15", v=15, rec="S8 p1046"),
    "v6303": dict(k="pt", s="v", at="1963-03-15", v=0, rec="S1 p93"),
    "v6302s": dict(k="pt", s="v", at="1963-09-02", v=6.5, rec="S9 p2014"),
    "v6315s": dict(k="pt", s="v", at="1963-09-15", v=12, rec="S9 p2014"),
    "v6326s": dict(k="pt", s="v", at="1963-09-26", v=22, rec="S9 p2014"),
    "v6302o": dict(k="pt", s="v", at="1963-10-02", v=40, rec="S9 p2014"),
    "v6308o": dict(k="pt", s="v", at="1963-10-08", v=100, rec="S1 p96"),
    "v6309o": dict(k="pt", s="v", at="1963-10-09", v=200, rec="S9 p2014"),
}
LV_BRK = dict(k="brk", s="v", a="1963-03-15", b="1963-09-02", rec="S1 p93")   # 3月〜9月2日＝数の記録が無い（「目立った速まり無し」）
LV_REF = {
    "model": dict(k="ref", s="z", v=700, t="700m（模型）", rec="S1 p89", c="DOC", lab="l"),
    # ⚠️ 札は線の左の端（5月4日の側）＝右の端だと c619 の縦の線の札「下げると決める」と横に並んで1つの言葉に読めた（下見）
    "permit": dict(k="ref", s="z", v=715, a="1963-05-04", t="715mの許可", rec="S1 p92", c="INST", lab="l"),
    "crest": dict(k="ref", s="z", v=725.5, t="天端725.5m", rec="S9 p2006", c="LINE"),
    # ALERT_DIM は文字に使わない。⚠️ qa_all の echo：「1960年11月の崩落のとき」は c614 の語りの写し → 短く
    "v1960": dict(k="ref", s="v", v=40, t="1960年の山", rec="S1 p73", c="TICK", lab="l"),
}
LV_REL = {"model": dict(t="700m（模型）", src="S1 p89"), "permit": dict(t="715mの許可", src="S1 p92"),
          "crest": dict(t="天端725.5m", src="S9 p2006")}
# 縦の線（出来事の日）と帯。⚠️ 札は図の上の端（top）か下の端（bot）・近い札は dy でずらす（715m の許可の札＝線の左の端）
LV_EV = {
    "fall60": dict(k="ev", at="1960-11-04", t="崩落", rec="S1 p72", c="ALERT"),
    "fill3": dict(k="ev", s="z", at="1963-04-10", t="3回目の水ため", rec="S1 p226", c="LINE", dy=34),
    "acc": dict(k="ev", s="v", at="1963-08-15", t="速まり始める", rec=["S1 p93", "S1 p96"], c="ALERT"),
    # ⚠️ 試し焼き（36857375434）：上の端の札が715m の許可の破線の真上に乗り「715m の札」に読めた → 上の段だけ・札は下の端
    "lower": dict(k="ev", s="z", at="1963-09-26", t="下げると決める", rec="S9 p2015", c="LINE", pos="bot"),
    "rep": dict(k="ev", at="1963-10-08", t="10月8日の報告", rec="S1 p96", c="DOC", pos="bot"),
}
LV_BAND = {"calm63": dict(k="band", s="v", a="1963-05-01", b="1963-08-31", t="大きな速まりなし", rec="S1 p93")}


def lvp(*names, **kw):
    """LVP の点の写し（名を並べた順）。"""
    return [dict(LVP[n], **kw) for n in names]


def lv_upto(date, rows="zv", skip=()):
    """date（その日を含む）までの点（日付の順・rows の段だけ）。前のカットまでに出した点＝past に使う。"""
    import axis as _A
    d = _A.val("date", date)[0]
    out = [n for n, p in LVP.items() if p["s"] in rows and _A.val("date", p["at"])[0] <= d + 1e-9 and n not in skip]
    return [dict(LVP[n]) for n in sorted(out, key=lambda n: _A.val("date", LVP[n]["at"])[0])]


def _rk(r):
    d, _, p = str(r).partition(" p")
    return ({"S1": 0, "S8": 1, "S9": 2}.get(d, 9), int(p) if p.isdigit() else 0)


def lv_fig(view, steps, past=(), vr=None, rows="zv", rel=()):
    """線の図の fig＝("lv", …)。出典の行は描いた部品の rec から組む（左下）。"""
    import titan_fig as _F
    items = list(past) + [x for st in steps for x in _F._many(st.get("add"))]
    recs = sorted({r for it in items for r in (it.get("rec") if isinstance(it.get("rec"), list) else [it.get("rec")]) if r},
                  key=_rk)
    vv = (vr or VR_LO) if "v" in rows else dict(vr=None, vt=())
    return ("lv", dict(view, **vv, rows=rows, past=list(past), steps=list(steps), rel=list(rel), note=LV_NOTE, src=src(recs)))


# ══════════════════════════════════════════════════════════
#  14本目 ⑤b-4（2026-09-29）：断面F（`tools/hull.py`）と地図（drift）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の MAP_* ・HULL_NOTE・`sewol_map()` はこの回の地図と資料。
#    画面の出典は `src()`（台本の頁「海審 p1016」→ 画面の頁「…PDF 16頁」＝門番 check_wording の I が通し番号を止める）
def src(recs):
    """出典の行（「出典：」を除く）。recs＝「海審 p1016・p1017」のような台本の頁の書き方（文字列か list）。"""
    import illu
    return illu.rec_line(recs if isinstance(recs, (list, tuple)) else [recs]).replace("出典：", "", 1)


# 🔴 2026-09-30（15本目 ⑤b-1）：14本目の注（HULL_NOTE）・地図の点（MAP_*・ROUTE）・地図の関数 `sewol_map()`・2つの問いを
#    戻す型（`q_pair()`・Q1_TILT・Q2_BOARD）は `tools/fixture_ep14.py` へ移した（値は1つも変えていない）。
#    15本目の3つの問い（c109）は案C の A・B・D を小さく戻す＝⑤b-2（14本目の q_pair の型を回の関数で）


# ══════════════════════════════════════════════════════════
#  地図（drift）の段の部品をつなぐ道具（`merge`＝回をまたいで同じ）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-01（16本目 ⑤b-1・§0b）：15本目の地図（5つの範囲＝RAMP・FIELD・TOWN・FLA・USA の表と、その関数 `ramp_map()`・
#    `field_map()`・`town_map()`・`fla_map()`・`usa_map()`・空港の点の照合 RENO_REL ほか）は `tools/fixture_ep15.py` へ移した
#    （値は1つも変えていない＝git の `c646174`）。16本目の地図は ⑤b で、回の表（`*_VIEW`・`*_PTS`・`*_REL`）と関数をここに足す。
#    地点は `titan_fig.GEO`（Wikidata・`vajont_` の頭）と報告書の値だけ。
#    ⚠️ 地図の教訓（線の長さと東西の並びは模式・距離の札は語りと同じ「約228メートル」の形ほか）は移した注の側にある
#       ＝fixture_ep15 の地図の節の上
_LISTS = ("route", "tag", "dim", "move", "circle", "arrow")


def _as_list(x):
    return [] if not x else (list(x) if isinstance(x, list) else [x])


def merge(*parts):
    """段の部品を1つの段にまとめる（route・tag・dim・move・circle・arrow は list をつなぐ）。"""
    out = {}
    for p in parts:
        for k, v in p.items():
            out[k] = _as_list(out.get(k)) + _as_list(v) if k in _LISTS else v
    return out


# ══════════════════════════════════════════════════════════
#  14本目 ⑤b-6（2026-09-29）：量の型（`tools/qty.py`・門番 check_qty）と箱の型（`tools/boxes.py`・門番 check_boxes）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の QG・QB・PEOPLE_*・CT・CTP・RUD・FORM_PRE・CAUSE はこの回の記録（値と頁）。
#    記録の値は門番の側にも別に持つ（check_qty.REC_*／check_boxes.REC_*＝§5b-88）＝回を替えたら両方を替える。
#    🔴 2026-09-30（15本目 ⑤b-1）：14本目の値は `tools/fixture_ep14.py` へ移した＝ここも門番の表も空。
#    🔴 2026-10-01（16本目 ⑤b-1）：15本目の値（棒＝QG・QB の速さ・時間・G ほか／箱の型の表＝鎖・答え・実況・成績・書類の再現図）は
#       `tools/fixture_ep15.py` へ移した（値は1つも変えていない＝git の `c646174`）＝ここも門番の表も空。
#       16本目の棒と箱は ⑤b で、回の値と頁を ref/ep16/src/ep16_pages.txt に当てて入れる
# 棒の群（尺は 0 から・項目名に単位）。数字は棒に書かない（§5b-9＝数は字幕）
# 🆕 2026-10-01（16本目 ⑤b-6a）：第1〜6章の棒（c205・c311・c410・c515・c611・c613）。値と頁は門番 check_qty.REC_QTY と照らす
#   ⚠️ 同じ群の灯した棒は色を分ける（ΔE 25 以上＝門番 ⑪）。日付を名にした行（同じ物差しの時間の並び＝c611）だけ同じ色でよい
#   ⚠️ 行の名に数字を書かない（⑩）＝日付だけ例外（「9月2日」）。「8階建てのビル」は数字＝棒にしない（c515 は語りだけ）
QG = {
    "dam_h": dict(id="dam_h", t="ダムの高さ（メートル）", ticks=(0, 50, 100, 150, 200, 250, 300), rows=("もとの計画", "変えた計画")),
    "lake_max": dict(id="lake_max", t="いちばん高い水位（メートル）", ticks=(0, 200, 400, 600, 800),
                     rows=("もとの計画", "変えた計画")),
    "vol": dict(id="vol", t="量（万立方メートル）", ticks=(0, 25, 50, 75, 100, 125), rows=("崩れた量", "東京ドーム")),
    # c410＝同じ群の尺を 2億まで（崩れた量と東京ドームは細い線になる＝300倍・160杯の差がそのまま見える）
    "vol_big": dict(id="vol", t="量（万立方メートル）", ticks=(0, 5000, 10000, 15000, 20000),
                    rows=("崩れた量", "東京ドーム", "動いている塊")),
    "wave": dict(id="wave", t="波の高さ（メートル）", ticks=(0, 5, 10, 15, 20, 25, 30)),
    # ⚠️ ⑤b-6a の門番 ⑩：群の名「1日に動いた距離」の「1」が数字の網に当たった＝言い方を変えた（1日あたりは注で言う）
    "speed": dict(id="speed", t="日ごとに動いた距離（ミリ）", ticks=(0, 10, 20, 30, 40, 50),
                  rows=("9月2日", "9月15日", "9月26日", "10月2〜3日")),
    # c613＝同じ群の尺を 200 まで（10月9日の棒を足す＝9月2日の30倍）
    "speed_hi": dict(id="speed", t="日ごとに動いた距離（ミリ）", ticks=(0, 50, 100, 150, 200),
                     rows=("9月2日", "9月15日", "9月26日", "10月2〜3日", "10月9日")),
}
QB = {
    # c205：S1 p63（1957年の変更＝高さ 202→266m・いちばん高い水位 677→722.50m）
    "h_old": dict(k="bar", g="dam_h", t="もとの計画", v=202, rec="S1 p63"),
    "h_new": dict(k="bar", g="dam_h", t="変えた計画", v=266, rec="S1 p63", c="AMBER"),
    "l_old": dict(k="bar", g="lake_max", t="もとの計画", v=677, rec="S1 p63"),
    "l_new": dict(k="bar", g="lake_max", t="変えた計画", v=722.5, rec="S1 p63", c="AMBER"),
    # c311・c410：崩れた量 70万（S1 p72）・東京ドーム 124万（一般の事実）・ミュラーの見積もり 2億（S1 p77）
    "v_fall": dict(k="bar", g="vol", t="崩れた量", v=70, rec="S1 p72", c="AMBER"),
    "v_dome": dict(k="bar", g="vol", t="東京ドーム", v=124, rec="一般の事実"),
    "v_mass": dict(k="bar", g="vol", t="動いている塊", v=20000, rec="S1 p77", c="ALERT"),
    # c515：模型の波 25m（S1 p97＝10月8日の国の監督の報告が引く）
    "w_model": dict(k="bar", g="wave", t="模型の波", v=25, rec="S1 p97", c="AMBER"),
    # c611・c613：1日に動いた距離（S1 p226・S9 p2014・S1 p93）
    "s0902": dict(k="bar", g="speed", t="9月2日", v=6.5, rec="S1 p226"),
    "s0915": dict(k="bar", g="speed", t="9月15日", v=12, rec="S1 p226"),
    "s0926": dict(k="bar", g="speed", t="9月26日", v=22, rec="S1 p226"),
    "s1002": dict(k="bar", g="speed", t="10月2〜3日", v=40, rec="S1 p226", c="AMBER"),
    "s1009": dict(k="bar", g="speed", t="10月9日", v=200, rec="S1 p93", c="ALERT"),
}


def qb(name, **kw):
    return dict(QB[name], **kw)


# 人の形（1つ＝1人）＝**14本目 c204〜c206 だけの例外**（ルール §C-1 #59・亡くなった方の数には使わない）。
#   15本目は使わない＝空のまま（門番 check_qty が PEOPLE_CUTS の外の人の形を止める）
PEOPLE_ORDER = ()
PEOPLE_SETS = {}
PEOPLE_REC = {}
PEOPLE_CUTS = ()     # 🔴 門番 check_qty がこの外の人の形を止める（亡くなった方の数に使わない）


def pp(who, c, parent=None):
    """人の形の部品（who の形を c の色に灯して凡例に1行）。"""
    return dict(k="lit", who=who, c=c, rec=PEOPLE_REC[who], **({"parent": parent} if parent else {}))


# 流れ図（14本目＝裁判の流れ図・第11章）。🔴 役職名だけ・名前を出さない・人の形を使わない・赤を使わない
#   🔴 2026-09-30（15本目 ⑤b-1）：14本目の CT・CTP・CREW15 は `tools/fixture_ep14.py` へ。15本目は流れ図を作らない
#   （映像方針 §11-3＝新しい型は作らない）＝空のまま。使う回は `layout=` に回の表を渡す（`tools/boxes.py` の説明）
CT = {}
CTP = {}


def ct(name, **kw):
    return dict(CTP[name], **kw)


def ce(fr, to, **kw):
    """流れ図の矢印（fr・to は部品の id か id の list）。"""
    return dict(k="edge", fr=fr, to=to, **kw)


# 仕組みの模式図の箱（14本目＝舵を動かす仕組み cc05・cc12）＝空。15本目の尾翼の板の模式図は ⑤b-3（映像方針 §4）
RUD = {}
RUDP = {}


def rud(name, **kw):
    return dict(RUDP[name], **kw)


# 書類の再現図（14本目＝c208 の出港前安全点検報告書＝fixture_ep14.FORM_PRE）。🔴 欄の名は報告書の文にあるものだけ・
#   欄に値を書かない（記録に無い値を作らない）・「再現」の札。15本目＝記録簿・参加書類・検査の用紙（c415・c524・c617・c621・
#   c704・c705・c905）＝⑤b で `FORM_<名> = dict(title, rec, fields, ends)` を回の名で足す（`form=` に渡す）
# 原因の並べ図（14本目＝c615・cc13）＝同じ形で並べるだけ（場面にしない）
# 🆕 16本目 ⑤b-6a：c419＝議会の中の2つの見方（S1 p179 多数派・p232 少数派）を同じ形で並べる（どちらかに決めない）
CAUSE = {
    "majority": dict(k="item", t="多数派「確認できない」", rec="S1 p179"),
    "minority": dict(k="item", t="少数派「隠した」", rec="S1 p232"),
}


def cause(name, **kw):
    return dict(CAUSE[name], **kw)


# 🔴 2026-10-01（16本目 ⑤b-1・§0b）：15本目の箱の型の表（報告書の鎖 CHAIN1・CHAIN2・重なった要因 FACTORS・3つの問いの答え ANS・ANSP・
#    実況の担当 MC・MCP・2010年の成績 HEAT・書類の再現図 FORM_LOG11 ほか7枚）と、その関数（`chain_links()`・`ans_links()`）は
#    `tools/fixture_ep15.py` へ移した（値は1つも変えていない＝git の `c646174`）。16本目の箱は ⑤b で足す
#    （門番 check_boxes の REC_MECH・REC_OTHER_ROLE・REC_CHIP・REC_FORM も、回の値を門番の側に別に持つ＝§5b-88）

# ══════════════════════════════════════════════════════════
#  🆕 2026-10-01（16本目 ⑤b-6a）：第1〜6章の箱（流れ図 c113・c207・c418・c510・c621／書類の再現図 c413・c422・c502・c512・c517・c617）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の FL_*・FLP・FORM_* は16本目の記録（言葉と頁＝門番 check_boxes の REC_* と照らす）。
#   流れ図は役職でなく報告書の文の言葉（16本目は名前を箱に書かない＝実名は語りだけ）・赤を使わない・人の形を使わない
# c113 資料のつながり（S1 p99＝公共事業大臣の令 1963年10月11日・エネルが 11月1日に別の委員会）
FL_SRC = dict(heads=[dict(id="parl", t="議会の報告書", kind="node", x=(1360, 1800), y=(450, 550), rec="S1 p99")])
# c207 計画を大きくすると（S1 p63＝容量と年間の発電量が上がった）。箱は基図・段で矢印が出る
FL_GROW = dict(heads=[dict(id="g1", t="ダムを高くする", kind="node", x=(120, 600), y=(470, 570), rec="S1 p63"),
                      dict(id="g2", t="ためる水が増える", kind="node", x=(720, 1200), y=(470, 570), rec="S1 p63"),
                      dict(id="g3", t="つくれる電気が増える", kind="node", x=(1320, 1800), y=(470, 570), rec="S1 p63")])
# c418 報告の行き先（S1 p179 多数派＝役所は知っていたが正式に送られたとは確認できない・p232 少数派＝役所・地方の長官・土木局に隠した）
FL_HIDE = dict(heads=[dict(id="co", t="会社", kind="node", x=(780, 1100), y=(470, 570), rec="S1 p232")])
# c510 模型の実験（S1 p89＝22回・2つの進め方・最も破局的な崩れ／S9 p2010＝水位680〜720m／S1 p224＝少数派「いつも2つの塊」）
FL_EXP = dict(heads=[dict(id="x22", t="22回の実験", kind="node", x=(110, 470), y=(430, 530), rec="S1 p89"),
                     dict(id="xw", t="波の高さ", kind="node", x=(1500, 1810), y=(430, 530), rec="S9 p2010")])
# c621 3回の比べ（左）と10月8日の報告（右＝S1 p96〜p97）。左の年は見出しの箱・右は縦の矢印（箱が真下＝§5b-110②）
FL_THREE = dict(heads=[dict(id="y60", t="1960年", kind="head", x=(110, 360), y=(300, 360), rec="S1 p85"),
                       dict(id="y62", t="1962年", kind="head", x=(110, 360), y=(440, 500), rec="S1 p93"),
                       dict(id="y63", t="1963年", kind="head", x=(110, 360), y=(580, 640), rec="S1 p96")],
                bounds=(990,), guide_y=(280, 820))
FLP = {
    # c113
    "c_state": dict(k="role", id="c_state", t="国の調査委員会", y=380, pos=(760, 1180), rec="S1 p99"),
    "c_enel": dict(k="role", id="c_enel", t="電力公社の調査委員会", y=620, pos=(760, 1180), rec="S1 p99"),
    "o_min": dict(k="role", id="o_min", t="公共事業大臣", y=380, pos=(160, 580), rec="S1 p99"),
    "o_enel": dict(k="role", id="o_enel", t="電力公社", y=620, pos=(160, 580), rec="S1 p99"),
    # c418
    "r_geo": dict(k="role", id="r_geo", t="2人の地質学者の報告", y=380, pos=(110, 560), rec="S1 p232"),
    "r_mul": dict(k="role", id="r_mul", t="ミュラーの報告", y=520, pos=(110, 560), rec="S1 p232"),
    "r_mod": dict(k="role", id="r_mod", t="模型の報告", y=660, pos=(110, 560), rec="S1 p232"),
    "g_gov": dict(k="role", id="g_gov", t="国の役所", y=380, pos=(1340, 1800), rec="S1 p232"),
    "g_pref": dict(k="role", id="g_pref", t="地方の長官", y=520, pos=(1340, 1800), rec="S1 p232"),
    "g_gc": dict(k="role", id="g_gc", t="土木局", y=660, pos=(1340, 1800), rec="S1 p232"),
    # c510
    "x_grav": dict(k="role", id="x_grav", t="重力で崩す", y=400, pos=(600, 980), rec="S1 p89"),
    "x_geo": dict(k="role", id="x_geo", t="地質の予想どおりに崩す", y=560, pos=(600, 980), rec="S1 p89"),
    "x_lvl": dict(k="role", id="x_lvl", t="水位680〜720m", y=480, pos=(1100, 1400), rec="S9 p2010"),
    # c621（左＝3回の比べ・右＝10月8日の報告の手当て）
    "t60": dict(k="role", id="t60", t="下げると止まった", y=330, pos=(460, 880), rec="S1 p85"),
    "t62": dict(k="role", id="t62", t="下げると止まった", y=470, pos=(460, 880), rec="S1 p93"),
    "t63": dict(k="role", id="t63", t="下げても速まった", y=610, pos=(460, 880), rec="S1 p96"),
    "k_co": dict(k="role", id="k_co", t="会社", y=360, pos=(1160, 1660), rec="S1 p96"),
    "k_off": dict(k="role", id="k_off", t="役所", y=480, pos=(1160, 1660), rec="S1 p96"),
    "k_may": dict(k="role", id="k_may", t="村長", y=600, pos=(1160, 1660), rec="S1 p96"),
    "k_ord": dict(k="role", id="k_ord", t="危ない区域から人を出す", y=720, pos=(1160, 1660), rec="S1 p97"),
}


def fl(name, **kw):
    return dict(FLP[name], **kw)


# 書類の再現図（16本目）。🔴 欄の値は**原文のイタリア語のまま**（日本語は字幕だけ＝映像方針の c413・c422 の決めを、書類の再現図の
#   6カットにそろえた）・欄の名は原文の文の言葉・「再現」の札（様式は抽象）。値は門番 check_boxes.REC_FORM の values と照らす
FORM_MUELLER = dict(title="ミュラーの報告（少数派の報告が引く）", rec="S1 p217",
                    fields=[dict(t="問い", v="se questi franamenti possono venire arrestati mediante misure artificiali",
                                 rec="S1 p217"),
                            dict(t="答え", v="deve essere risposto negativamente in linea generale", rec="S1 p217", late=True)],
                    paper=(140, 1780, 330, 690), lw=120)
FORM_UNITA = dict(title="ウニタの記事（1961年2月21日）", rec="S1 p39",
                  fields=[dict(t="見出し", rec="S1 p39", late=True,
                               v="Una enorme massa di 50 milioni di metri cubi minaccia la vita e gli averi degli abitanti di Erto")],
                  paper=(100, 1820, 360, 640), lw=130)
FORM_NOTE60 = dict(title="会社の記録（1960年11月16日）", rec="S1 p75",
                   fields=[dict(t="第一の心配", v="garantire l'incolumità delle persone che abitano nella valle", rec="S1 p75"),
                           dict(t="必要なこと", v="abbassare il livello del serbatoio", rec="S1 p75", late=True),
                           dict(t="波", v="non possano assolutamente raggiungere la zona abitata", rec="S1 p75", late=True)],
                   paper=(200, 1720, 300, 760), lw=220)
FORM_GHETTI = dict(title="ゲッティの報告（1962年7月3日）", rec="S1 p89",
                   fields=[dict(t="結論", v="la quota 700 può considerarsi di assoluta sicurezza", rec="S1 p89", late=True),
                           dict(t="何に対して", v="del più catastrofico prevedibile evento di frana", rec="S1 p89", late=True)],
                   paper=(240, 1680, 330, 690), lw=220)
# ⚠️ ⑤b-6a の qa_all（echo）：表題「模型の研究所の委員会（1962年の春）」は c517 の1行目と2か所に割れて 100% 一致＝日付は注へ
FORM_NOVE = dict(title="模型の研究所の委員会", rec="S1 p225",
                 fields=[dict(t="意見", v="almeno per il momento non siano da compiere ricerche", rec=["S1 p225", "S9 p2012"],
                              late=True),
                         dict(t="研究", v="propagarsi di una onda di piena a valle della diga", rec=["S1 p225", "S9 p2012"],
                              late=True)],
                 paper=(240, 1680, 330, 690), lw=160)
FORM_GC61 = dict(title="土木局の手紙（1961年1月7日）", rec="S1 p79",
                 fields=[dict(t="湖が満ちたとき", v="le acque, eventualmente infiltratesi nel terreno", rec="S1 p79", late=True),
                         dict(t="急に下げるとき", v="possano mettersi in pressione", rec="S1 p79", late=True),
                         dict(t="斜面", v="pregiudicando la stabilità del versante", rec="S1 p79", late=True)],
                 paper=(200, 1720, 300, 760), lw=280)
