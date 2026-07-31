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
#  写真に差し替えるカット（2026-07-31 カズヤくん指示「写真を最大限」）
# ══════════════════════════════════════════════════════════
# **どのカットを写真にするかは章をまたぐ編集判断**なので、章ファイルではなくここに置く。
# 章ファイル側の図の定義はそのまま残してあるので、`PHOTO_OVERRIDE` から消せば図に戻る。
#
# 🔴 写真が7枚しかないのが制約だったが、**NTSB報告書の図13〜18は出所表記が無い
#    ＝NTSB自身の研究室撮影＝PD** と確認できたので、報告書から6枚取り出した
#    （`ref/CREDITS.md` に図番号と根拠を記録）。どれも第3〜4章の内容そのものの写真。
#
# ⚠️ これらは 1431×325 のように**細長い**ので `band=True`（帯）で置く。
#    全画面にすると3.3倍に引き伸ばして左右を切り落とすことになり、
#    「層が並んでいる」という写真の意味そのものが消える。
PHOTO_OVERRIDE = {
    # 第3章：剥離とは何か ＝ 層で作られた材料（図13：外面と内面）
    "c308": dict(photo="titan_hull_pair.jpg", band=True, bias=0.5, ann_y=790,
                 ann=[dict(t="上が外側の面　下が内側の面　白い部分は繊維の破断",
                           ts=38)]),
    # 第4章：しわ（図16上）
    "c411": dict(photo="titan_ntsb16_wrinkle.jpg", band=True, bias=0.5, ann_y=800,
                 ann=[dict(t="しわの上で、接着の層に空隙ができている", ts=40)]),
    # 第4章：層と層のあいだの接着剤（図17上）
    "c416": dict(photo="titan_ntsb17_layers.jpg", band=True, bias=0.5, ann_y=790,
                 ann=[dict(t="1層と2層のあいだに、接着剤の面が1つ", ts=40)]),
    # 第4章：切り落とされた部分（図15）
    "c422": dict(photo="titan_ntsb15_endpiece.jpg", band=True, bias=0.5, ann_y=830,
                 ann=[dict(t="実物の円筒と同じ工程で作られ、同じ釜で焼かれた", ts=38)]),
    # 第4章：機械加工した端面（図14上）
    "c424": dict(photo="titan_ntsb14_endface.jpg", band=True, bias=0.5, ann_y=830,
                 ann=[dict(t="接着層を含めた端部を、この面で測っている", ts=38)]),
    # 第4章：★空隙そのもの（図17下）。この章の核心の写真
    "c427": dict(photo="titan_ntsb17_voids.jpg", band=True, bias=0.5, ann_y=790,
                 ann=[dict(t="白い丸で囲まれているのが空隙", c="#e0503c", ts=42)]),
    # 第4章：外に出たしわを工具で削った跡（図16下）
    "c429": dict(photo="titan_ntsb16_grind.jpg", band=True, bias=0.5, ann_y=800,
                 ann=[dict(t="外側の繊維が削り取られている", c="#e0503c", ts=42)]),
    # 第6章：円筒はほぼ全周にわたって層に分かれていた（図13下＝内面）
    "c624": dict(photo="titan_hull_inner.jpg", bias=0.5, side="right", ann_y=372,
                 ann=[dict(t="白い部分は、繊維が破断したところ", c="#e0503c",
                           ts=44)]),
}

for _cid, _ov in PHOTO_OVERRIDE.items():
    if _cid not in SPEC:
        continue
    _keep = {k: SPEC[_cid][k] for k in ("t", "s") if k in SPEC[_cid]}
    SPEC[_cid] = dict(_keep, **_ov)
