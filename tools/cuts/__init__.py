# -*- coding: utf-8 -*-
"""226カットの「画」の割り当て。章ごとにファイルを分けてある。

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
    "pr01": dict(t="…", s="…", photo="titan_rov_aft.jpg", bias=0.5, side="right",
                 ann=[dict(t="水深", v="3,346 m")])

■ 守ること
  1 **ナレーションの文を図にそのまま書かない。** 図が持つのは数値・部位名・関係。
    引用カットは「言葉」ではなく**出どころ**（誰が・誰に・いつ・どこに）を図にする。
  2 見出しは 22 字まで（Dela 62px で 1,364px。RIGHT=1848 に収まる）。
  3 段（figの stages）の数は**ナレーションの行数に近づける**。
    行より多い段は行の間に挟まれる。少ない場合は最後の段が長く描かれる。
"""
import importlib
import sys

# 章ごとに1ファイル。**1章が壊れていても他章は読めるようにする**
# （章を並行して書いているあいだ、片方の書きかけで全部の検査が止まらないように）。
CHAPTER_FILES = ("pr", "c1", "c2", "c3", "c4", "c5", "c6", "ep")

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
# 🔴 2026-08-04：**1本目（タイタン号）の割り当てを全部捨てた。**
#    カットIDが201件ぶつかるので、残すと潜水艇の写真が123便のカットに黙って出る。
#    中身は git の `57e6c16` にある。
#
# 🔴 2本目の素材は `ref/ja123/`（報告書から切り出した168枚。台帳＝`ref/ja123/INDEX.md`）。
#    ⚠️ **原本は1ビット（2値・JBIG2）**なので、1920px へ伸ばすと砂目が出る。
#      取り出しの時点で長辺1200pxへ落としてぼかしてあるので、
#      **額装パネル（`panel=True`）で出す**のが既定。全画面には置かない。
#    ⚠️ 付図（`f001`〜`f038`）は線画なので2値が最適。劣化しないので自由に使える。
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
#    見た目は派手になるが、写真がその場面を写しているかのように読めてしまう。
#    出典表記は地に敷いた場合も必ず出す（`fig_base(ground=False)` が出す）。
#
# 🔴 2026-08-04：タイタン号の14カットを捨てた。以下は123便の割り当て。
#
# ⚠️ **付図（線画）は地に敷かない。** 白地に細い線なので暗幕0.84 を掛けると
#    線ごと沈んで「画が無いのと同じ」になる。付図は `panel=True` で前に出す。
#    地に敷けるのは**写真**だけ。
#
# ⚠️ 第4章・第5章・第6章に敷いているカットが少ないのは、素材が足りないからではなく
#    **「そのカットで話している対象そのもの」に当たる写真が無いから**。
#    時刻の札や「空白」の図の後ろに残骸を壁紙として敷くのは、上の原則に正面から反する。
BACKDROP = {
    # プロローグ：32分のあいだに撮られた1枚
    "pr04": dict(photo="ja123/p124.jpg", bias=0.50),

    # 第1章：操縦系統の部品そのもの／記録装置そのもの
    "c117": dict(photo="ja123/p011.jpg", bias=0.50),
    "c132": dict(photo="ja123/p101.jpg", bias=0.50),

    # 第2章：調べた残骸そのもの、L18接続部の調査写真
    "c205": dict(photo="ja123/p021.jpg", bias=0.50),
    "c207": dict(photo="ja123/p022.jpg", bias=0.50),
    "c208": dict(photo="ja123/p017.jpg", bias=0.50),
    "c210": dict(photo="ja123/p018.jpg", bias=0.50),
    "c211": dict(photo="ja123/p019.jpg", bias=0.50),
    "c214": dict(photo="ja123/p044.jpg", bias=0.50),
    "c219": dict(photo="ja123/p012.jpg", bias=0.50),
    "c225": dict(photo="ja123/p087.jpg", bias=0.50),
    "c226": dict(photo="ja123/p085.jpg", bias=0.50),
    "c227": dict(photo="ja123/p086.jpg", bias=0.50),
    "c228": dict(photo="ja123/p089.jpg", bias=0.50),
    "c231": dict(photo="ja123/p043.jpg", bias=0.50),
    "c235": dict(photo="ja123/p090.jpg", bias=0.50),

    # 第3章：隔壁を通った空気／与圧室の外で見つかった断熱材
    "c320": dict(photo="ja123/p066.jpg", bias=0.50),
    "c332": dict(photo="ja123/p096.jpg", bias=0.50),
    "c335": dict(photo="ja123/p095.jpg", bias=0.50),

    # エピローグ：L18スティフナの破壊／疲労破面／噴き出した空気が壊した部位
    "ep07": dict(photo="ja123/p119.jpg", bias=0.50),
    "ep08": dict(photo="ja123/p107.jpg", bias=0.50),
    "ep12": dict(photo="ja123/p033.jpg", bias=0.50),
}

for _cid, _ov in BACKDROP.items():
    if _cid not in SPEC:
        print(f"⚠️ BACKDROP の {_cid} が台本にありません", file=sys.stderr)
        continue
    if "fig" not in SPEC[_cid]:
        raise RuntimeError(f"{_cid} は図を持っていないので地に敷けません（実写カット）")
    SPEC[_cid] = dict(SPEC[_cid], **_ov)
