# -*- coding: utf-8 -*-
"""215カットの「画」の割り当て。章ごとにファイルを分けてある。

■ 直すところ
  図を変えたいときは、その章のファイルの1カットぶんの dict だけを直す。
  `tools/titan_fig.py` の型を増やすのは、**同じ形が3カット以上で要るときだけ**。

■ 1カットの書き方
    "c103": dict(
        t="乗っていたのは42人",              # 見出し（左上・Dela 62px）
        s="ポーラープリンス　2023年6月18日",   # 副題（省略可）
        fig=("breakdown", dict(total=42, parts=[...])),
    )
  実写カットは fig の代わりに photo を書く：
    "pr01": dict(t="…", s="…", photo="surfside/tf_p003_model.jpg", bias=0.5, side="right",
                 ann=[dict(t="高さ", v="33.8 m")])

■ 守ること
  1 **ナレーションの文を図にそのまま書かない。** 図が持つのは数値・部位名・関係。
    引用カットは「言葉」ではなく**出どころ**（誰が・誰に・いつ・どこに）を図にする。
  2 見出しは 22 字まで（Dela 62px で 1,364px。RIGHT=1848 に収まる）。
  3 段（figの stages）の数は**ナレーションの行数に近づける**。
    行より多い段は行の間に挟まれる。少ない場合は最後の段が長く描かれる。

■ 🔴🔴 2026-09-16：**9本目（テネリフェ空港衝突事故）へ差し替え。**
  カットIDは題材をまたいでぶつかる（**215中203件**が8本目 コロンビア号と同じID）。
  8本目の章ファイル・ss.py・BACKDROP は git の `4c71bf0` にある
  （`git show 4c71bf0:tools/cuts/c1.py`）。7本目は `ae30d49`。
  検算：`python -c "import cuts; print(len(cuts.SPEC))"` が**台本のカット数（215）**であること。
  ⚠️ 始める前に **0** になっていること（→ [[project-jiko-rules-index]] §0b）。
"""
import importlib
import sys

import jiko_style as J

import cuts.ss as ss          # BACKDROP が写真の名前を使う（`ss` は `scene_jiko` を読まない）

# 章ごとに1ファイル。**1章が壊れていても他章は読めるようにする**
# （章を並行して書いているあいだ、片方の書きかけで全部の検査が止まらないように）。
# 🔴 9本目も 冒頭＋**9章**＋締め（台本第2版 §3・`ref/ep9/kousei.md` §1）。
CHAPTER_FILES = ("pr", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "ep")

SPEC = {}
BROKEN = {}
for _name in CHAPTER_FILES:
    try:
        _m = importlib.import_module(f".{_name}", __name__)
        _dup = set(SPEC) & set(_m.SPEC)
        if _dup:
            raise RuntimeError(f"カットIDが重複しています: {sorted(_dup)}")
        SPEC.update(_m.SPEC)
    except Exception as e:                      # noqa: BLE001
        BROKEN[_name] = e
        print(f"⚠️ cuts/{_name}.py を読めませんでした: {e}", file=sys.stderr)


# ══════════════════════════════════════════════════════════
#  写真に差し替えるカット（図の代わりに写真そのものを出す）
# ══════════════════════════════════════════════════════════
# **どのカットを写真にするかは章をまたぐ編集判断**なので、章ファイルではなくここに置く。
# 章ファイル側の図の定義はそのまま残るので、ここから消せば図に戻る。
#
# 🔴 2026-09-05：**3本目（スレッシャー号）の割り当てを全部捨てた。** 中身は git の `ad6882a`。
#    4本目以降は、写真カットを**章ファイルに直接 `photo=` で書く**（台本 §4 の画の欄と1対1で
#    照合できるように）。ここは空のまま。上書きが要る判断が出たときだけ使う。
PHOTO_OVERRIDE = {
}

for _cid, _ov in PHOTO_OVERRIDE.items():
    if _cid not in SPEC:
        continue
    _keep = {k: SPEC[_cid][k] for k in ("t", "s") if k in SPEC[_cid]}
    SPEC[_cid] = dict(_keep, **_ov)


# ══════════════════════════════════════════════════════════
#  ★写真を「地」に敷いて、その上に図解を重ねるカット
# ══════════════════════════════════════════════════════════
# `photo` と `fig` を**両方**持たせると、写真が地になり、暗幕を挟んで図が乗る。
# （上の PHOTO_OVERRIDE は図を写真に**差し替える**。こちらは図を**残す**。）
#
# ⚠️ **全カットに敷かない。** 敷いた瞬間に「図解チャンネル」である意味が消える。
#    競合との差は図があることなので、退屈になりやすいカットだけに絞る。
#
# 🔴 選び方の原則（このチャンネルの性格＝一次資料で検証する、を壊さないため）
#    **その写真が、そのカットで話している対象そのものであること。**
#    「時刻の札の後ろに、関係のない残骸の写真を壁紙として敷く」のはやらない。
#    出典表記は地に敷いた場合も必ず出す（`fig_base(ground=False)` が出す）。
#
# ⚠️ 付図・線図（自作の模式図）は、白地の細い線が暗幕で沈む。敷くなら暗幕を焼いて確かめる。
# ⚠️ 総数の規則（写真映像 45〜50%）だけ見ると章ごとの偏りが残る
#    ＝[[feedback-verify-design-against-the-spec]]。**章ごとにも見る。**
# ⚠️ 既定の暗幕 0.84 が足りない写真がある（7本目 c804 は 0.88 に上げた）
#    ＝[[feedback-settings-may-not-reach-the-picture]]。焼いたあと `check_slide` G-16 を見る。
# ⚠️ 写真に焼き込まれた英字は、地に敷くと `check_slide` G-13／G-14 が**参考（・）に落とす**
#    ので鳴らない（8本目 ⑤c'' で `strike_wide` の英字が 904×76px 出ていた）。
#    → 素材を先に OCR と原寸で見て、`trim` で外へ出す
#    （→ [[feedback-gates-dont-see-text-burned-into-the-picture]]）。
#
# 🔴🔴 2026-09-16（9本目 テネリフェ ⑤b-1）**8本目の割り当て31件を全部捨てた。**
#    中身は git の `4c71bf0`（`git show 4c71bf0:tools/cuts/__init__.py`）。
#    ⚠️ カットIDは 215中203件が8本目とぶつかる。**残したまま始めると
#       コロンビア号の写真が黙って地に敷かれる。**
BACKDROP = {
}

for _cid, _ov in BACKDROP.items():
    if _cid not in SPEC:
        print(f"⚠️ BACKDROP の {_cid} が台本にありません", file=sys.stderr)
        continue
    if "fig" not in SPEC[_cid]:
        raise RuntimeError(f"{_cid} は図を持っていないので地に敷けません（実写カット）")
    SPEC[_cid] = dict(SPEC[_cid], **_ov)
