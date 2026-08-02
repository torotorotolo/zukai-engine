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
    # ⚠️ 注記が**ナレーションの文そのまま**だったので check_echo に 100% 一致で
    #    引っかかった（映像ルール6違反）。図が持つのは「部位名と出どころ」であって
    #    文ではない。話している内容は音と字幕がすでに持っている。
    "c422": dict(photo="titan_ntsb15_endpiece.jpg", band=True, bias=0.5, ann_y=830,
                 ann=[dict(t="円筒の端から切り落とされた部分の側面　NTSB 図15", ts=38)]),
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


# ══════════════════════════════════════════════════════════
#  ★写真を「地」に敷いて、その上に図解を重ねるカット（2026-07-31 試写の指摘④）
# ══════════════════════════════════════════════════════════
# カズヤくん：「時刻をグラフで出すだけのカットが多く、競合と比べて退屈」。
# → `photo` と `fig` を**両方**持たせると、写真が地になり、暗幕を挟んで図が乗る。
#   （上の PHOTO_OVERRIDE は図を写真に**差し替える**。こちらは図を**残す**。）
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
# ⚠️ 全画面に耐える写真は**この6枚だけ**（実測。ほかは拡大率が2倍を超えて眠くなる）
#      titan_rov_aft 1920×1080 ／ titan_rov_tailcone 1909×1080
#      titan_titanic_bow 1480×1036 ／ titan_cf_evidence 1500×1000
#      titan_hull_pair 1609×1490 ／ titan_hull_inner 1609×805
#    ✗ titan_hull_edge(1830×552) と NTSB の帯写真は、16:9 に切ると2倍に拡大される
#
# 暗幕の濃さ（veil）は `tools/check_veil.py` の実測から 0.84 を既定にしてある。
#   α=0.72 図が読めない ／ 0.84 読みやすさ0.55・写真L*14 ／ 0.92 写真が消える
#
# 🔴 USCG の ROV 画像（rov_aft / rov_tailcone）は **zoom と xbias が必須**。
#    左上に "OceanGate / Dive: 01 / Depth (m): 3774.9"、左下に日付、
#    下中央に "HDG" と "Alt" が**焼き込まれている**。
#    実写カットではこれが出所の証拠になるので残すが、地に敷くと話が別で、
#    c115a（水深3,346メートルを図で出すカット）の真上に **3774.9 という
#    別の数字**が出た（実際に焼いて発見した）。
#    zoom=1.30・xbias=0.95・bias≦0.45 で、焼き込みが4辺とも画面外に出る。
#      横 … 切り出し幅 1477 → 左端 421px から。焼き込みは 340px で終わる
#      縦 … 切り出し高 831・bias0.45 → 下端 943px。焼き込みは 960px から
ROV = dict(zoom=1.30, xbias=0.95)
BACKDROP = {
    # 第1章：落ちていく先＝海底。尾部コーンは海底に立った実物
    "c110": dict(photo="titan_rov_tailcone.jpg", bias=0.45, **ROV),
    # 第1章：★最後の位置（3,346m）で見つかった残骸そのもの。いちばん強く効く場所
    "c115a": dict(photo="titan_rov_aft.jpg", bias=0.40, **ROV),
    "c116": dict(photo="titan_rov_aft.jpg", bias=0.45, **ROV),
    "c117": dict(photo="titan_rov_tailcone.jpg", bias=0.30, **ROV),
    # 第1章：8時間、誰も知らなかった＝その間ずっと在った深さ
    "c124": dict(photo="titan_titanic_bow.jpg", bias=0.46),
    # 第3章：応力解析にかけられた炭素繊維の円筒の実物（外面と内面）
    "c301": dict(photo="titan_hull_pair.jpg", bias=0.50),
    # 第3章：亀裂が見つかった円筒の面
    "c323": dict(photo="titan_hull_inner.jpg", bias=0.50),
    # 第6章：その88回目に使われた機体
    "c615": dict(photo="titan_rov_aft.jpg", bias=0.35, **ROV),
    # 第6章：剥離＝層が離れている面そのもの
    "c628": dict(photo="titan_hull_inner.jpg", bias=0.42),
    # ── ★2026-08-02 追加（カズヤくん指示「実写の比率を上げる」）──────
    # 🔴 素材を増やしたのではなく、**その対象を写した映像がある2カット**を足した。
    #    どちらも `tools/footage.py` で ROV の動画を当てている（静止画は落ちたとき用）。
    # 第1章：「無人探査機を現場に入れるまで2週間かかるところを4日で」
    #   … 映っているのは Pelagic の ROV ＝ 6月22日に残骸を見つけたのと同じ運用者の機体。
    #   ⚠️ 残骸が見つかる前の c129・c131・c133 には**当てない**（先に答えが出てしまう）。
    "c134": dict(photo="titan_rov_aft.jpg", bias=0.45, **ROV),
    # 第6章：「残骸の中央で見つかった破片には、S字に曲がった座屈の跡」
    "c626": dict(photo="titan_rov_aft.jpg", bias=0.45, **ROV),
}

for _cid, _ov in BACKDROP.items():
    if _cid not in SPEC:
        print(f"⚠️ BACKDROP の {_cid} が台本にありません", file=sys.stderr)
        continue
    if "fig" not in SPEC[_cid]:
        raise RuntimeError(f"{_cid} は図を持っていないので地に敷けません（実写カット）")
    SPEC[_cid] = dict(SPEC[_cid], **_ov)
