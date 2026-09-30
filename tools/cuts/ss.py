# -*- coding: utf-8 -*-
"""15本目（2011年9月16日 リノ・エアレース墜落事故・米国ネバダ州リノ ステッド空港・11名）の章ファイルが共通で使う小道具。

**14本目（セウォル号）の中身は git の `dc6ecf4` にある**（`git show dc6ecf4:tools/cuts/ss.py`）。
13本目（トルコ航空981便）は `b54ee4f`、12本目（キャッスル・ブラボー）は `3832147`、11本目（チャレンジャー号）は `61039d2`、
10本目（三豊百貨店）は `46f11b3`、9本目（テネリフェ）は `e18b8f1`、8本目は `4c71bf0`、7本目は `ae30d49`。

🔴 **⑤b-1（2026-09-30）で空にした**＝§0b。14本目の束の定数（写真の切り出し TRIM 2点・私人を外した範囲 PRIVATE_OUT 2点）は外した。
14本目の型の値（案C の出典の表・割れる時刻・軸・地図・量・箱）は、門番の selftest の見本 `tools/fixture_ep14.py` へ移した
（値は1つも変えていない）。15本目の束は写真の束のチャットで作る（`qa_out/ep14_assets.py` を写して `qa_out/ep15_assets.py`）。

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
REF = HERE / "ref" / "ep15"
EP = "ep15/"
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
NEEDS_MASK: dict[str, str] = {
    # 🔴 2026-09-30（15本目 ⑤b-6・カズヤくん「顔面のみのモザイク加工」）：CC BY の2010年の2点（jeggernot）＝整備の人・観客（私人）の
    #    **顔だけモザイク**。範囲は `qa_out/ep15_assets.py` の MASK（原寸で2倍の拡大と目盛りで読んだ）＝`build` が元画像に当てる
    f"{EP}gg_nose_2010.jpg": "整備の人と周りの人の顔（4か所）＝顔だけモザイク",
    f"{EP}gg_pit_2010.jpg": "手前の人・ジープの人・テントの人・右端の人の顔（11か所）＝顔だけモザイク",
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
# 🔴🔴 2026-09-30（15本目 リノ・エアレース2011 ⑤b-1）：**空にした**（§0b）。14本目の値（下の軸・地図・量・箱も全部）は
#    門番の selftest の見本 `tools/fixture_ep14.py` へ移した（値は1つも変えていない＝git の `dc6ecf4` と同じ）。
#    15本目の値は、その型を初めて使う ⑤b のチャットで入れる（空のあいだ、その型を使うカットは門番・型が止まる＝fail closed）：
#      REC_DOCS … 台本 §10 の出典（NTSB AAB-12/01・ドケットの #14・#33・#37・#40・#42・#53・CAROL ほか）＝⑤b-2（案C A・B）
#                  頁の番号は ④ の make_pages.py が `ep15_pages.txt` に振った番号で範囲を書く
#      ILLU_SPLIT_TIMES … 台本 §1-5 の割れる時刻（#42 の「5.3秒」は起点が違う・写真の EXIF から推した時刻は札にしない）
#      ILLU_CROWD_UNTIL … 観客の群れは「落ちる瞬間（崩れ始めから約9.1秒＝16:24:38ごろ）」より前（映像方針 §10-1「ゆるめる」）
#        ⚠️ 14本目は時計の時刻（"9:47"）で比べる作り＝15本目は秒の札（AAB p28 の経過の表）で書く場面がある
#           ＝check_illu ② の役割（{観客の群れ}）と時刻の条件を ⑤b-2 で広げる（ルール §5b-75・映像方針 §6）
REC_PAGES = REF / "src" / "ep15_pages.txt"      # ④ の make_pages.py の出力（261頁・git の外＝手元だけ）
# 🔴 2026-09-30（15本目 ⑤b-2）：15本目の値を入れた。頁の番号は `ref/ep15/v1_build/make_pages.py` が振った通し番号
#    （AAB＝PDF の頁のまま p1〜p52・#40 p1001〜・#33 p2001〜・#14 p3001〜・#53 p4001〜・CAROL p5008〜p5017・勧告書 p6001〜・
#     #17 p7001〜）。画面の出典は「PDF N頁」（base を引く）。⚠️ 台本の出典欄の「#33 p9」は #33 の PDF の頁＝ここでは p2009
REC_DOCS = {
    "AAB": dict(range=(1, 52), name="NTSB 事故報告 AAB-12/01", page="pdf", base=0),
    "#40": dict(range=(1001, 1061), name="NTSB 資料 #40（材料の試験）", page="pdf", base=1000),
    "#33": dict(range=(2001, 2022), name="NTSB 資料 #33（生存と運営）", page="pdf", base=2000),
    "#14": dict(range=(3001, 3040), name="NTSB 資料 #14（データの記録）", page="pdf", base=3000),
    "#53": dict(range=(4001, 4029), name="NTSB 資料 #53（性能の解析）", page="pdf", base=4000),
    "CAROL": dict(range=(5008, 5017), name="NTSB 勧告の記録（CAROL）", page=None, base=0),
    "勧告書": dict(range=(6001, 6207), name="NTSB 勧告書（A-12-08〜17）", page=None, base=0),
    "#17": dict(range=(7001, 7029), name="NTSB 資料 #17（耐空性）", page="pdf", base=7000),
}
# 資料で割れる時刻（時計）＝15本目は無い（割れるのは秒の起点＝#42 の「5.3秒」と AAB の「4.6秒」＝台本 §1-5）。
#   秒の札は下の ILLU_SEC_OK（AAB p28 の表の値だけ）で止める＝5.3秒・写真の EXIF から推した時刻は札に出せない
ILLU_SPLIT_TIMES = ()
# 🆕 ⑤b-3（2026-09-30）：観客の群れ（置き場 RC）は**落ちる瞬間より前**だけ（映像方針 §10-1「ゆるめる」＝9秒のあいだも可）。
#   落ちる瞬間＝崩れ始め 16:24:28.9（AAB p28 の表の 0秒）＋約9.1秒＝16:24:38.0。場面の時刻 at は秒まで書く（秒の無い "16:24" は
#   その分の終わりとみなす＝遅い側に倒す＝群れを出せない）。c212・c726 は at="16:24:28"（0秒のころ＝観客はピットとボックス席にいた）
ILLU_CROWD_UNTIL = "16:24:38"
# 🆕 ⑤b-3：この回に置いてよい役割（門番 check_illu ②）＝型紙（1人ずつ数えられる影）は無し・群れは観客だけ
#   （パイロット・審判・救護・検査員・整備の仲間は描かない＝映像方針 §1 線2・§6②）
ILLU_ROLES = dict(sprite=(), crowd=("spectators",))
# 🆕 15本目：画面に出してよい秒（札の「N秒」「約N秒」）＝AAB p28 の経過の表の値だけ（映像方針 §6 ⑤）。門番 check_illu ⑤
ILLU_SEC_OK = {s: "AAB p28" for s in ("0", "0.27", "0.56", "0.83", "1.3", "1.44", "3.1", "4.6", "9.1")}
# 🆕 15本目：札に出してよい時計の時刻＝表の時刻（16時24分台）だけ（EXIF から推した時刻を出さない）
ILLU_CLOCK_OK = ("16:24",)
# 🆕 15本目：描いてよい数（部品の obj の合計＝その場面に描いた数）と記録（映像方針 §6 ③）。門番 check_illu ③
ILLU_COUNTS = dict(aircraft=(1, "AAB p10"), fuel_truck=(1, "AAB p19"), stands=(3, "AAB p20"), pylons=(12, "AAB p17"))

# 🔴 §0b：軸の型（`tools/axis.py`・14本目 ⑤b-5）の「割れる時刻の印」に添える出典の名（`rec=` の資料名 → 画面の名）。
#   語りが資料を呼ぶ名に合わせる（海審の特別調査報告＝語りは「報告書」）。ILLU_SPLIT_TIMES の時刻は、軸の型では
#   **出典の名つきでだけ**出してよい（門番 check_axis ②＝点に by=True か split）
# 🔴 2026-09-30（15本目 ⑤b-1）：空にした（14本目の値＝`tools/fixture_ep14.py`）。15本目の年表（1944→2011 の機体の歩み・
#    勧告 A-12-08 が閉じるまで）と時間の帯（9秒・試験飛行・観客席の62分）は ⑤b（映像方針 §11-2＝新しい型4つ）で入れる。
#    ⚠️ 語りが資料を呼ぶ名に合わせる（15本目の語りは NTSB の報告を「報告書」と呼ぶ）
# 🔴 2026-09-30（15本目 ⑤b-5）：15本目の値を入れた（割れる時刻の印は使わない＝ILLU_SPLIT_TIMES が空）
AXIS_DOCS = {"AAB": "報告書", "CAROL": "勧告の記録"}

# 軸（カットをまたいで同じ軸を使う＝前のカットの点を past で沈めて続ける）。回ごとに `AX_<名> = dict(view, span, ticks)` を足す
# 🆕 15本目 ⑤b-5（値と頁は ref/ep15/src/ep15_pages.txt で当てた）
#   HIST＝機体の歩み 1944→2011（c324・c404・c408・c410・c411・c412＝第3〜4章）
#   LATE＝その寄り 2006→2012（c607・c615＝第6章・改造のあとの初飛行と2010年の出場）
#   A08 ＝勧告 A-12-08 が閉じるまで（c913・c915・c916＝CAROL の記録 p5008）
#   DRILL＝2011年の訓練と事故（c809・c813＝AAB p21）／EMS＝事故と多数傷病者事故の宣言（c804＝AAB p20・p28）
#   UPSET＝横転の前の秒（c218＝負の秒・AAB p29）／NINE＝その9秒（c220＝AAB p28 の経過の表）
AX_HIST = dict(view="date", span=("1942", "2013"), ticks=("1950", "1960", "1970", "1980", "1990", "2000", "2010"))
AX_LATE = dict(view="date", span=("2006", "2012"), ticks=("2007", "2008", "2009", "2010", "2011", "2012"))
# ⚠️ ⑤b-5 の layout：左の端の点（事故）の札が右へ伸びると、すぐ右の点の縦の線が札を貫いた＝左に余白を取り、事故の札は左へ
AX_A08 = dict(view="date", span=("2010-01", "2022-03"), ticks=("2010", "2012", "2014", "2016", "2018", "2020", "2022"))
# ⚠️ ⑤b-5 の layout：5月25日の札（左へ）が枠の左の端を越えた＝4月1日から
AX_DRILL = dict(view="date", span=("2011-04-01", "2011-10-05"),
                ticks=("2011-04", "2011-05", "2011-06", "2011-07", "2011-08", "2011-09", "2011-10"))
AX_EMS = dict(view="clock", span=("16:20", "16:32"), ticks=("16:20", "16:22", "16:24", "16:26", "16:28", "16:30", "16:32"))
AX_UPSET = dict(view="sec", span=("-10", "1"), ticks=("-10", "-8", "-6", "-4", "-2", "0"))
AX_NINE = dict(view="sec", span=("0", "10"), ticks=("0", "2", "4", "6", "8", "10"))

# 部品（記録の頁つき。値と頁は門番 check_axis の REC_AXIS と照らされる）。t は項目名だけ（§5b-9）
#   ⚠️ 年だけの値（"1983"）は年の真ん中に置く（span の両端も）＝1983〜1989 のレースは 1983.5〜1989.5 の帯
#   ⚠️ 事故の時刻は台本 c317 の「午後4時24分38秒ごろ」（AAB p28 の表）＝16:24。本文の要約の「about 1625」（p8・p10）は丸めた値
AXI = {
    # ── 機体の歩み（AAB p12「delivered to the Army Air Forces on December 23, 1944 … in July 1946, it was declared surplus
    #    and sold … acquired by the accident pilot in July 1983 … raced … from 1983 through 1989 before placing it in storage
    #    until 2007 … Between 2007 and 2009 … overhaul and further modifications」・p35「August 17, 1983 … special
    #    airworthiness certificate」・p36「completion of its major modifications occurred on September 21, 2009」「the 2010 NCAR」）
    "deliver": dict(k="pt", at="1944-12-23", t="軍へ引き渡し", rec="AAB p12"),
    "sold": dict(k="pt", at="1946-07", t="売却", rec="AAB p12"),
    "owner": dict(k="pt", at="1983-07", t="パイロットが取得", rec="AAB p12", anchor="end"),
    "exp": dict(k="pt", at="1983-08-17", t="FAAの許可", rec="AAB p35", anchor="start", fmt="ym"),
    "race8389": dict(k="span", a="1983", b="1989", t="リノのレース", rec="AAB p12", c="INST"),
    "store": dict(k="span", a="1989", b="2007", t="保管", rec="AAB p12", c="TICK"),
    "store_br": dict(k="br", a="1989", b="2007", rec="AAB p12"),
    # ⚠️ 2年の帯は札の幅が 164画素まで＝7字は小さくなる → 5字
    "rebuild": dict(k="span", a="2007", b="2009", t="分解と改造", rec="AAB p12", c="AMBER"),
    "first": dict(k="pt", at="2009-09-21", t="初飛行", rec="AAB p36"),
    "race10": dict(k="pt", at="2010", t="出場", rec="AAB p36"),
    "acc": dict(k="pt", at="2011-09-16", t="事故", rec="AAB p10", c="ALERT", fmt="y"),
    "life_br": dict(k="br", a="1944-12-23", b="2011-09-16", rec=["AAB p12", "AAB p10"]),
    # ── 勧告 A-12-08（CAROL p5008：NTSB の評価 2012-07-25・2016-11-30・2020-07-22＝OPEN—ACCEPTABLE RESPONSE／
    #    2020-02-27 命令 8900.1 を改めた・2020-11-03 通達 AC 91-45C を廃止（守らせる言い方が 49 CFR 5.25 で禁じられた）／
    #    2021-07-13 CLOSED—ACCEPTABLE ALTERNATE ACTION）
    "a08_acc": dict(k="pt", at="2011-09-16", t="事故", rec="CAROL p5008", c="ALERT", fmt="ym", anchor="end"),
    # ⚠️ ⑤b-5 の layout：「2020年7月」の札（右へ）が枠の右の端を越えた＝3回の評価は年だけ（語りも「3回」とだけ言う）
    "a08_1": dict(k="pt", at="2012-07-25", t="まだ閉じない", rec="CAROL p5008", fmt="y"),
    "a08_2": dict(k="pt", at="2016-11-30", t="まだ閉じない", rec="CAROL p5008", fmt="y"),
    "a08_3": dict(k="pt", at="2020-07-22", t="まだ閉じない", rec="CAROL p5008", fmt="y", anchor="start"),
    "a08_order": dict(k="pt", at="2020-02-27", t="命令を改めた", rec="CAROL p5008", c="INST", fmt="ym", anchor="end"),
    "a08_ac": dict(k="pt", at="2020-11-03", t="通達の廃止", rec="CAROL p5008", c="INST"),
    "a08_close": dict(k="pt", at="2021-07-13", t="閉じた", rec="CAROL p5008", c="OK", anchor="end"),
    "a08_br": dict(k="br", a="2011-09-16", b="2021-07-13", rec="CAROL p5008"),
    # ── 2011年の訓練（AAB p21「tabletop exercise had been conducted on June 2, 2011」「full-scale emergency exercise on
    #    May 25, 2011」）
    "d_acc": dict(k="pt", at="2011-09-16", t="事故", rec="AAB p10", c="ALERT"),
    "tabletop": dict(k="pt", at="2011-06-02", t="机上訓練", rec="AAB p21", anchor="start"),
    "fullscale": dict(k="pt", at="2011-05-25", t="総合訓練", rec="AAB p21", anchor="end"),
    "drill_br": dict(k="br", a="2011-06-02", b="2011-09-16", rec=["AAB p21", "AAB p10"]),
    # ── 事故と宣言（AAB p28 の表＝16:24:28.9 に崩れ始め・約9.1秒後に落ちた／p20「declared a mass-casualty incident at 1626」）
    "t1624": dict(k="pt", at="16:24", t="事故", rec="AAB p28", c="ALERT"),
    "t1626": dict(k="pt", at="16:26", t="多数傷病者事故の宣言", rec="AAB p20"),
    # ── 横転の前（AAB p29「About 8 seconds before the beginning of the upset, there was a noticeable reduction in engine
    #    manifold pressure and rpm」）・0秒＝横転の始まり（p28 の表の 0秒）
    "u0": dict(k="pt", at="0", t="横転の始まり", rec="AAB p28", c="ALERT"),
    "u8": dict(k="pt", at="約-8", t="圧力と回転が下がる", rec="AAB p29"),
    # ── その9秒（AAB p28 の経過の表の秒＝ILLU_SEC_OK と同じ9つ）。札を出さない点（lab=False）＝秒の単位で並んだことだけ
    **{f"s{s}": dict(k="pt", at=s, t="", lab=False, rec="AAB p28")
       for s in ("0", "0.27", "0.56", "0.83", "1.3", "1.44", "約3.1", "4.6", "約9.1")},
    "nine": dict(k="span", a="0", b="約9.1", t="崩れ始めから落ちるまで", rec="AAB p28", c="LINE"),
}
NINE_PTS = ("s0", "s0.27", "s0.56", "s0.83", "s1.3", "s1.44", "s約3.1", "s4.6", "s約9.1")


def ax(name, **kw):
    """AXI の部品の写し（同じカットで past と add に同じ物を2回入れても別の部品になる）。"""
    return dict(AXI[name], **kw)


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
#  🆕 15本目 ⑤b-7（2026-09-30）：地図（drift）＝5つの範囲（映像方針 §4・09-30 カズヤくん「Googleアースは地図に替える」）
# ══════════════════════════════════════════════════════════
#   RAMP  … 駐機場（c213・c817・c819・c820）＝ショーライン・ピットとボックス席の端・許可と命令の152メートル・通達の305メートル
#   FIELD … 飛行場のまわり（c904 の2行目から）＝燃料車を約2.4キロ先へ・コースを北へ（矢印だけ）・より頑丈な柵
#   TOWN  … リノの町とステッド空港（c201・c811・c812）＝風の向き・州道395号（道の線は模式）
#   FLA   … フロリダ州オカラ（c602）＝基地から半径約161キロ
#   USA   … アメリカ（c413・c603・c917）＝アリゾナ→テキサス→ミンデン／オカラの円と機体の居場所／リノ→ロズウェル
#   地点＝`titan_fig.GEO`（Wikidata・`reno_` の頭）と、報告書の値で置く点（下の pts）。照合（rel）は範囲ごと：
#     空港の点＝NTSB 資料 #17 p7008 の座標（±2キロ）・駐機場＝AAB p19 と p17 の南北の距離・燃料車＝AAB p46・円＝AAB p35
#   🔴 駐機場と飛行場の線（ショーライン・ピット・ボックス席・燃料車・柵）の**長さと東西の並びは模式**＝報告書の値は
#      ショーラインからの南北の距離と、燃料車の距離だけ（注に書く）。コースを北へ移した距離は記録に無い＝矢印だけ（映像方針 §4）
#   ⚠️ 距離の札は語りと同じ「約228メートル」の形（門番 check_drift は⑤b-7 から「メートル」も読む＝描いた2点と ±5%）
import jiko_style as _J  # noqa: E402  （地図の線の色。ss は章ファイルより先に読まれる＝ここで読む）

_FT = 0.0003048            # 1フィート（キロ）
RENO_TAB = (39 + 39 / 60 + 50 / 3600, -(119 + 52 / 60 + 36 / 3600))
RENO_REL = [dict(a="reno_stead", lat=RENO_TAB[0], lon=RENO_TAB[1], tol_km=2.0,
                 src="NTSB 資料 #17 p7008（左の板の一片が見つかった所＝滑走路8-26 の北側・ホームパイロンの近く）")]
_SLAT, _SLON = 39.667222, -119.876111          # ステッド空港（Wikidata）＝駐機場と飛行場の模式の原点

# 駐機場（1キロ＝約993画素）。ショーライン＝滑走路8/26 の南の縁（AAB p17）・ピットの端は南へ748フィート・
#   ボックス席の端は874フィート（AAB p19）・許可の条件と命令＝500フィート（p17）・通達＝1,000フィート（p17・勧告書 A-12-08 p3）
RAMP_VIEW = dict(lon=(_SLON - 0.00997, _SLON + 0.00997), lat=(_SLAT - 0.0040, _SLAT + 0.0013))
RAMP_PTS = dict(
    sl_w=dict(of="reno_stead", km=0.40, deg=270), sl_e=dict(of="reno_stead", km=0.40, deg=90),
    sl_pit=dict(of="reno_stead", km=0.25, deg=270), sl_box=dict(of="reno_stead", km=0.05, deg=90),
    pit=dict(of="sl_pit", km=748 * _FT, deg=180), box=dict(of="sl_box", km=874 * _FT, deg=180),
    pit_w=dict(of="pit", km=0.10, deg=270), pit_e=dict(of="pit", km=0.10, deg=90),
    box_w=dict(of="box", km=0.13, deg=270), box_e=dict(of="box", km=0.13, deg=90),
    o_w=dict(of="sl_w", km=500 * _FT, deg=180), o_e=dict(of="sl_e", km=500 * _FT, deg=180),
    a_w=dict(of="sl_w", km=1000 * _FT, deg=180), a_e=dict(of="sl_e", km=1000 * _FT, deg=180),
    rn=dict(of="sl_e", km=0.06, deg=0),
)
RAMP_REL = [
    # ⚠️ 注の字にもメートル法の換算を添える（門番 wording＝§B1：フィート・マイルだけの字を置かない）
    dict(a="sl_pit", b="pit", km=748 * _FT, dir="南", src="AAB p19（ピットの端はショーラインの南 748フィート＝約228メートル）"),
    dict(a="sl_box", b="box", km=874 * _FT, dir="南", src="AAB p19（ボックス席の端は南 874フィート＝約266メートル）"),
    dict(a="sl_w", b="o_w", km=500 * _FT, dir="南", src="AAB p17（許可の条件・命令＝500フィート＝約152メートル）"),
    dict(a="sl_w", b="a_w", km=1000 * _FT, dir="南", src="AAB p17（通達＝1,000フィート＝約305メートル）"),
]
RAMP_NOTE = "模式図：線の長さと東西の並びは模式。ショーラインから南への距離は報告書の値"
# 段の部品（語りの行に合わせて `_merge` で足す）
R_BASE = dict(route=[dict(via=["sl_w", "sl_e"], col=_J.INK_W, sw=5, dash=None),
                     dict(via=["pit_w", "pit_e"], col=_J.LINE, sw=7, dash=None),
                     dict(via=["box_w", "box_e"], col=_J.LINE, sw=7, dash=None)],
              # ⚠️ 下見（09-30）：ボックス席の札を線の左に置くとピットの線の真下に来て、どちらの線の札か紛らわしかった＝右へ
              tag=[dict(at="sl_e", t="ショーライン", side="right"), dict(at="rn", t="滑走路8/26", side="right"),
                   dict(at="pit_w", t="ピットの端", side="left"), dict(at="box_e", t="ボックス席の端", side="right")])
R_DIMS = dict(dim=[dict(a="pit", b="sl_pit", t="約228メートル"), dict(a="sl_box", b="box", t="約266メートル")])
# 許可の条件・命令（152メートル）の線の札は右の端・通達（305メートル）は左の端（右はボックス席の札に近い＝下見）
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


def ramp_map(steps, note=RAMP_NOTE, recs=("AAB p17", "AAB p19")):
    """駐機場の地図（c213・c817・c819・c820）。steps は段の list（`merge` で部品を足して作る）。"""
    return ("drift", dict(view=RAMP_VIEW, places=[], pts=RAMP_PTS, rel=list(RAMP_REL), steps=steps, note=note,
                          src=src(list(recs)), scale_km=0.1, grid=0.002))


# 飛行場のまわり（c904 の2行目から・1キロ＝約173画素）。燃料車は「ピットの近くの駐機場」（AAB p19）→ 2012年から
#   「飛行場の南東の側・主な観客席から約1.5マイル」（AAB p46）。柵は「ピットの西の端からボックス席を通って一般の観客席まで」
#   （p46）。コースと選手を「北へ移した」（p46・CAROL A-12-14＝距離の記録は無い）。燃料車の距離だけ宣言（向きは模式）
FIELD_VIEW = dict(lon=(_SLON - 0.0523, _SLON + 0.0623), lat=(_SLAT - 0.0215, _SLAT + 0.0090))
FIELD_PTS = dict(RAMP_PTS,
                 fuel0=dict(of="pit", km=0.25, deg=270),
                 fuelm=dict(of="fuel0", km=0.60, deg=180),   # ⑤c'：燃料車の道の曲がり角（模式）＝札「観客席」の下を通す
                 fuel1=dict(of="box", km=1.5 * 1.609344, deg=135),
                 pbw=dict(of="pit", km=0.10, deg=270), grand=dict(of="box", km=0.40, deg=90),
                 cn1=dict(of="reno_stead", km=0.80, deg=0))
FIELD_REL = [dict(a="box", b="fuel1", km=1.5 * 1.609344, src="AAB p46（主な観客席から約1.5マイル＝約2.4キロ）")]
FIELD_NOTE = "模式図：場所の並びと線の長さは模式（燃料車の距離だけ報告書の値）。コースを動かした距離は記録に無い"


def field_map(steps):
    return ("drift", dict(view=FIELD_VIEW, places=[], pts=FIELD_PTS, rel=list(FIELD_REL), steps=steps,
                          note=FIELD_NOTE, src=src(["AAB p19", "AAB p46"]), scale_km=0.5, grid=0.01))


# リノの町とステッド空港（1キロ＝約24画素）。州道395号の線は町と空港を直線で結んだ模式（道の形は記録に無い）
TOWN_VIEW = dict(lon=(-120.257, -119.432), lat=(39.49, 39.71))
TOWN_PTS = dict(hw_mid=dict(mid=["reno_stead", "reno_city"]),
                wind0=dict(of="reno_stead", km=5.0, deg=240))   # 風上（AAB p16「wind was from 240°」）＝流れの起点（模式）
TOWN_PLACES = [dict(k="reno_stead", side="above"), "reno_city"]


def town_map(steps, note="模式図：地点は緯度経度から（リノは町の中心）", recs=("#17 p7008",)):
    return ("drift", dict(view=TOWN_VIEW, places=TOWN_PLACES, pts=TOWN_PTS, rel=list(RENO_REL), steps=steps,
                          note=note, src=src(list(recs)), scale_km=5, grid=0.1))


# フロリダ州オカラ（1キロ＝約1.39画素）。運用の制限＝基地（オカラの飛行場）から半径100マイル（AAB p35）。
#   円の中心はオカラの町の中心（基地の飛行場の位置は報告書に無い）。外へ出る矢印＝レースへ向かう途中（向きはリノの方角 298.9度）
FLA_VIEW = dict(lon=(-88.44, -75.84), lat=(27.3, 31.1))
FLA_PTS = dict(ocala_r=dict(of="reno_ocala", km=100 * 1.609344, deg=90),
               fl_out=dict(of="reno_ocala", km=300, deg=298.9))
FLA_REL = [dict(a="reno_ocala", b="ocala_r", km=100 * 1.609344, src="AAB p35（半径100マイル＝約161キロ）")]
CIRCLE = dict(circle=dict(at="reno_ocala", through="ocala_r"))


def fla_map(steps):
    return ("drift", dict(view=FLA_VIEW, places=["reno_ocala"], pts=FLA_PTS, rel=list(FLA_REL), steps=steps,
                          note="模式図：円の中心はオカラの町の中心（基地の飛行場の位置ではない）",
                          src=src(["AAB p35"]), scale_km=100, grid=1.0))


# アメリカ（1キロ＝約0.28画素）。ミンデンと空港は約80キロ＝約23画素（輪が重なる＝札は空港を上・ミンデンを下）
USA_VIEW = dict(lon=(-133.1, -67.9), lat=(25.5, 44.0))


def usa_map(steps, places, note, recs, rel=(), extra=""):
    """extra＝出典の行に足す字（`REC_DOCS` に無い資料＝主催の団体の発表など）。"""
    return ("drift", dict(view=USA_VIEW, places=places, pts=dict(FLA_PTS), rel=list(RENO_REL) + list(rel),
                          steps=steps, note=note, src=src(list(recs)) + extra, scale_km=500, grid=5.0))


# ══════════════════════════════════════════════════════════
#  14本目 ⑤b-6（2026-09-29）：量の型（`tools/qty.py`・門番 check_qty）と箱の型（`tools/boxes.py`・門番 check_boxes）
# ══════════════════════════════════════════════════════════
# 🔴 §0b（題材を替えるとき空にする場所）：下の QG・QB・PEOPLE_*・CT・CTP・RUD・FORM_PRE・CAUSE はこの回の記録（値と頁）。
#    記録の値は門番の側にも別に持つ（check_qty.REC_*／check_boxes.REC_*＝§5b-88）＝回を替えたら両方を替える。
#    🔴 2026-09-30（15本目 ⑤b-1）：14本目の値は `tools/fixture_ep14.py` へ移した＝ここも門番の表も空。
#       15本目の棒（c206・c217・c616・c620・c622・c907）と書類の再現図（c415・c524・c617・c621・c704・c705・c905）は
#       ⑤b（映像方針 §11-2）で、回の値と頁を ref/ep15/src/ep15_pages.txt に当てて入れる
# 棒の群（尺は 0 から・項目名に単位）。数字は棒に書かない（§5b-9＝数は字幕）
# 🔴 2026-09-30（15本目 ⑤b-5）：15本目の値を入れた（値と頁は ref/ep15/src/ep15_pages.txt で当てた）
#   speed＝c206（AAB p10「about 445 knots as it passed pylon 8」＝時速約824キロ／新幹線の営業の最高 時速320キロ＝一般の事実）
#   lap  ＝c217（AAB p29「maximum 458-knot GPS ground speed between pylons 6 and 7 … the fastest that the airplane had flown
#          on the course by about 35 knots」＝848 と、そこから約65キロ〈35ノット〉を引いた 783＝🔴 783 は報告書の差から引いた値
#          ＝注で言う。⚠️ #14 p3008 の「記録した GPS の最高 431ノット（2010-09-14）」は9回の飛行の全体＝物差しが違う）
#   test ＝c606・c609・c612（AAB p36「3 hours of flight time」・p50「all five flights … 20 minutes … only 1 hour 40 minutes」・
#          p36／p49「about 23 minutes」）
#   hours＝c620（AAB p12「“2,700±” hours」＝2011年の参加の書類・p15 注15／p16「1,453.6 hours」）
#   recent＝c622（AAB p51「about 25 total hours between its assembly in 2009 and its July 2011 inspection … about 200 flight
#          hours in it since the previous year」）
#   g    ＝c907（CAROL p5011・p5012「normally between 3 and 4 g」＝棒は上の端 4／AAB p28 の表 17.3G）
#   ⚠️ c616（2010年の速さ＝公式の平均の速さ 325ノット未満＝AAB p36 注41）は棒にしない：同じ物差し（周の平均）の2011年の値が
#      記録に無い＝「その瞬間の速さ」と並べると物差しが違う → 箱の型（2010年の成績の流れ）にした
QG = {
    "speed": dict(id="speed", t="速さ（時速・キロ）", ticks=(0, 200, 400, 600, 800, 1000)),
    "lap": dict(id="lap", t="コースでの速さ（時速・キロ）", ticks=(0, 200, 400, 600, 800, 1000),
                rows=("それまでの最高", "事故の周")),
    "test": dict(id="test", t="試験の飛行の時間（分）", ticks=(0, 30, 60, 90, 120, 150, 180),
                 rows=("求められた", "多く見積もっても", "テレメトリーの記録")),
    "hours": dict(id="hours", t="この機体での時間（時間）", ticks=(0, 500, 1000, 1500, 2000, 2500, 3000),
                  rows=("参加の書類", "記録簿の総時間")),
    "recent": dict(id="recent", t="この機体での時間（時間）", ticks=(0, 50, 100, 150, 200),
                   rows=("書類：前の年から", "記録簿：組み立てから")),
    "g": dict(id="g", t="かかったG（重さの何倍か）", ticks=(0, 5, 10, 15, 20), rows=("ふつうのコース", "事故の最大")),
}
QB = {
    "shinkansen": dict(k="bar", g="speed", t="新幹線（営業の最高）", v=320, rec="一般の事実"),
    "plane824": dict(k="bar", g="speed", t="事故機", v=824, rec="AAB p10", c="AMBER"),
    "lap_prev": dict(k="bar", g="lap", t="それまでの最高", v=783, rec="AAB p29"),
    "lap_acc": dict(k="bar", g="lap", t="事故の周", v=848, rec="AAB p29", c="AMBER"),
    "test_req": dict(k="bar", g="test", t="求められた", v=180, rec="AAB p36"),
    "test_max": dict(k="bar", g="test", t="多く見積もっても", v=100, rec="AAB p50", c="AMBER"),
    "test_tele": dict(k="bar", g="test", t="テレメトリーの記録", v=23, rec="AAB p36", c="ALERT"),
    "hours_form": dict(k="bar", g="hours", t="参加の書類", v=2700, rec="AAB p12", c="AMBER"),
    "hours_log": dict(k="bar", g="hours", t="記録簿の総時間", v=1453.6, rec="AAB p16"),
    "recent_form": dict(k="bar", g="recent", t="書類：前の年から", v=200, rec="AAB p51", c="AMBER"),
    "recent_log": dict(k="bar", g="recent", t="記録簿：組み立てから", v=25, rec="AAB p51"),
    "g_course": dict(k="bar", g="g", t="ふつうのコース", v=4, rec="CAROL p5011"),
    "g_acc": dict(k="bar", g="g", t="事故の最大", v=17.3, rec="AAB p28", c="ALERT"),
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
CAUSE = {}


def cause(name, **kw):
    return dict(CAUSE[name], **kw)


# ══════════════════════════════════════════════════════════
#  🆕 15本目 ⑤b-5（2026-09-30）：箱の型の15本目の表（門番 check_boxes の REC_MECH・REC_OTHER_ROLE・REC_CHIP・REC_FORM と照らす）
# ══════════════════════════════════════════════════════════
# 報告書の鎖（c106・c723・c725）＝AAB p52 の推定原因「deteriorated locknut inserts → screws to become loose → reduced
#   stiffness → flutter at racing speeds → failure of the left trim tab link assembly → elevator movement, high flight loads」。
#   箱は動かない（基図）＝段で矢印（つなぎ）が出る。c106 は第1章＝「リンク」の語がまだ出ていない＝「棒が折れる」（台本 c106 の画）
_CX = ((85, 335), (385, 635), (685, 935), (985, 1235), (1285, 1535), (1585, 1835))
CHAIN_Y = (400, 500)


def _chain(words):
    return dict(heads=[dict(id=f"n{i + 1}", t=w, kind="node", x=_CX[i], y=CHAIN_Y, rec="AAB p52")
                       for i, w in enumerate(words)])


CHAIN1 = _chain(("ナットの劣化", "ねじのゆるみ", "かたさが落ちる", "板の震え", "棒が折れる", "機首上げ"))
CHAIN2 = _chain(("ナットの劣化", "ねじのゆるみ", "かたさが落ちる", "板の震え", "リンクが折れる", "機首上げ"))


def chain_links(**kw):
    """鎖の5本の矢印（n1→n2 … n5→n6）。"""
    return [dict(k="edge", fr=f"n{i}", to=f"n{i + 1}", rec="AAB p52", **kw) for i in range(1, 6)]


# 重なった要因（c725）＝AAB p52「Contributing to the accident were the undocumented and untested major modifications … and
#   the pilot's operation of the airplane in the unique air racing environment without adequate flight testing」＝鎖の下に
#   区切りの線を引いて並べるだけ（鎖のどの輪につながるかは報告書が言っていない＝矢印でつながない）
FACTORS = {
    "f_mod": dict(k="role", id="f_mod", t="記録も試験も無い改造", y=700, pos=(160, 860), rec="AAB p52"),
    "f_ops": dict(k="role", id="f_ops", t="十分な試験なしのレース", y=700, pos=(1060, 1760), rec="AAB p52"),
}
# 🆕 ⑤b-7（2026-09-30）：3つの問いの答え（c918）＝台本 c918「先に折れたリンク、ゆるんだねじ、食い違った2つの資料」
#   （AAB p52 の推定原因＝リンクの破損とねじのゆるみ・p17 の2つの手引きの食い違い）と、事故の前にあった手がかり
#   （26年以上のナット＝p41・「ねじが短すぎる」＝p37 の検査の用紙・記録簿の「終えた」＝p15）。上の段＝c109 の問いの名
#   （台本 c109 の画）。🔴 答えと手がかりを矢印でつながない（台本は組にしていない）＝区切りの線の下に並べるだけ
#   ⚠️ 下見（09-30）：問いの箱を node（38px）にすると答えの箱（28px）より目立った＝問いは head（34px・低い箱）に
ANS = dict(heads=[dict(id="q1", t="9秒に何が起きたか", kind="head", x=(110, 650), y=(320, 380), rec="AAB p28"),
                  dict(id="q2", t="なぜ板は震えたか", kind="head", x=(690, 1230), y=(320, 380), rec="AAB p41"),
                  dict(id="q3", t="観客席との距離", kind="head", x=(1270, 1810), y=(320, 380), rec="AAB p19")])
ANSP = {
    "a1": dict(k="role", id="a1", t="先に折れたリンク", y=480, pos=(160, 600), rec="AAB p52"),
    "a2": dict(k="role", id="a2", t="ゆるんだねじ", y=480, pos=(740, 1180), rec="AAB p52"),
    "a3": dict(k="role", id="a3", t="食い違った2つの資料", y=480, pos=(1320, 1760), rec="AAB p17"),
    "k1": dict(k="role", id="k1", t="26年以上のナット", y=690, pos=(160, 600), rec="AAB p41"),
    "k2": dict(k="role", id="k2", t="「ねじが短すぎる」", y=690, pos=(740, 1180), rec="AAB p37"),
    "k3": dict(k="role", id="k3", t="記録簿の「終えた」", y=690, pos=(1320, 1760), rec="AAB p15"),
}


def ans_links():
    """問い → 答え の3本の矢印。"""
    return [dict(k="edge", fr=f"q{i}", to=f"a{i}", rec=ANSP[f"a{i}"]["rec"]) for i in (1, 2, 3)]


# 実況の担当（c806）＝AAB p20「The NCAR announcing team … remained calm and provided clear evacuation procedures guidance to the
#   crowd, assisted first responders, and requested additional help from medical staff on scene」。人の形は描かない（文字の箱だけ）
MC = dict(heads=[dict(id="mc", t="実況の担当", kind="node", x=(150, 560), y=(470, 570), rec="AAB p20")])
MCP = {
    "a_evac": dict(k="role", id="a_evac", t="観客へ避難の案内", y=380, pos=(900, 1500), rec="AAB p20"),
    "a_help": dict(k="role", id="a_help", t="救護の人を手伝う", y=520, pos=(900, 1500), rec="AAB p20"),
    "a_med": dict(k="role", id="a_med", t="医療の応援を頼む", y=660, pos=(900, 1500), rec="AAB p20"),
}
# 2010年の成績（c616）＝AAB p38「started in the last place in the lowest heat in the class. The airplane won a series of races
#   and qualified to run the unlimited class gold race in 2010, but that race was cancelled due to wind」
HEAT = dict(heads=[dict(id="h1", t="いちばん下の組", kind="node", x=(150, 610), y=(430, 530), rec="AAB p38"),
                   dict(id="h2", t="勝ち上がる", kind="node", x=(730, 1190), y=(430, 530), rec="AAB p38"),
                   dict(id="h3", t="ゴールドのレース", kind="node", x=(1310, 1770), y=(430, 530), rec="AAB p38")])

# 書類の再現図（c415・c524・c617・c621・c704・c705・c905）。🔴 本物の書類の写しではない＝「再現」の札と出典・書いてある字は
#   報告書に引かれた文だけ（様式は抽象）。欄の値は記録の値だけ（門番 REC_FORM の values）
#   c415＝AAB p15 注15・p16（2011-07-29 のエンジンの記録簿の総時間 1,453.6＝機体の記録簿の 1,447.2 は 6.4時間の書き違い）
#   c524＝AAB p15（2009-09-22・本人の署名「The prescribed flight test hours have been completed」）
#   c617＝AAB p37（2009年の参加の書類の問い〈前に出たあとの大きな改造〉に「yes」の丸）
#   c621＝AAB p12 注7（2009年と2010年の書類の年齢「59」）
#   c704＝AAB p37（「Remarks」の欄「elev trim tab screws too short …」・2011-09-12 に承認・書面で確かめる手順は無かった）
#   c705＝AAB p37（付録E：技術委員会の承認は「機体の状態や耐空性を表すものではない」＝規則の文を1行に＝様式は抽象）
#   c905＝CAROL p5010（A-12-10：用紙に「指摘」と「直した中身」の書面・再検査まで出さない）
FORM_LOG11 = dict(title="記録簿（2011年7月29日）", rec="AAB p15",
                  fields=[dict(t="機体の総時間", v="1,453.6時間", rec="AAB p16")],
                  paper=(560, 1360, 330, 690), lw=260)
FORM_LOG09 = dict(title="記録簿（2009年9月22日）", rec="AAB p15",
                  fields=[dict(t="試験飛行の時間", v="終えた", rec="AAB p15"),
                          dict(t="署名", v="パイロット本人", rec="AAB p15")],
                  paper=(560, 1360, 300, 740), lw=260)
FORM_ENTRY09 = dict(title="参加の書類（2009年）", rec="AAB p37",
                    fields=[dict(t="大きな改造をしたか", v="はい", rec="AAB p37", late=True)],
                    paper=(460, 1460, 330, 690), lw=340)
FORM_AGE = dict(title="参加の書類（2009年・2010年）", rec="AAB p12",
                fields=[dict(t="年齢", v="59", rec="AAB p12")],
                paper=(560, 1360, 330, 690), lw=200)
FORM_TECH = dict(title="技術検査の用紙", rec="AAB p37",
                 fields=[dict(t="備考", v="トリムタブのねじが短すぎる", rec="AAB p37"),
                         dict(t="承認の日付", v="2011年9月12日", rec="AAB p37")],
                 ends=dict(office=dict(t="レースのコース", rec="AAB p37")),
                 paper=(520, 1300, 300, 740), lw=200)
FORM_RULE = dict(title="技術検査の決まり（付録E）", rec="AAB p37",
                 fields=[dict(t="技術委員会の承認", v="機体の状態や、飛べるかを表さない", rec="AAB p37")],
                 paper=(360, 1560, 330, 690), lw=300)
FORM_NEW = dict(title="技術検査の用紙（事故のあと）", rec="CAROL p5010",
                fields=[dict(t="指摘", rec="CAROL p5010"), dict(t="直した中身", rec="CAROL p5010"),
                        dict(t="再検査", rec="CAROL p5010")],
                ends=dict(office=dict(t="レースのコース", rec="CAROL p5010")),
                paper=(520, 1300, 280, 800), lw=220)
