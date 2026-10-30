# -*- coding: utf-8 -*-
"""27本目：地図のカット（9カット＝c104・c202・c212・c213・c216・c504・c511・c601・c617）の「Google マップの衛星写真」を撮る
（映像方針＝一覧 eizou_list27.md の衛星 G1・G2・G3・G7・G9・撮るのは ⑤b-5＝⑤b-1 では撮っていない）。
標準ライブラリ＋PIL だけ。26本目の `ref/ep26/eizou_build/helpers/gshot26.py` の道具の部分を import して使う（表 GMAP と置き場だけ27本目）。

  python -I gshot27.py shot [記号,…] [--out <フォルダ>]   # 下の表 GMAP を撮る → ref/ep27/photo/<file>（1920×1080）。--out は2回撮って比べる用
  python -I gshot27.py px <記号> <緯度> <経度>            # その画の上の画素の位置（描き足す点・札の座標）を印字

🔴 撮るたびに読み込みの途中の継ぎ目が出ることがある＝**2回撮って `ref/ep22/eizou_build/helpers/gseam22.py <A> <B>` で比べ、線の無い方を採る**。
🔴 撮った PNG は公開リポに置かない（`ref/ep27/photo/` は git の外）＝Modal の保管庫 `jiko-assets` の `ref/ep27/photo/…` へ入れ、取り戻して md5 を照らす。

■ 表（中心・ズームの決め＝⑤b-5・2026-10-30。点の座標は `tools/cuts/ss.GEO`＝出どころつき＝住所検索 msearch.gsi.go.jp の町の代表点・OpenStreetMap）
  🔴 事件の交差点の正確な位置は確かめていない（報道は「別府市野口原の県道交差点」まで・県警の動画の地図〈YT-A 59〜82秒〉は 403 で取れず引用もしない）
     ＝交差点に印を置かない。G2 は「野口原」の町の代表点を中心に撮る（副題も「野口原付近」）
  G1（c212 経路・c617 全体）＝ズーム16（横 約2.6キロ）。中心は野口原と北浜のヨットハーバーのまん中（2地点の間 約2.0キロ）
  G2W（c104＝広め）＝ズーム17（横 約1.3キロ）・G2N（c202＝寄る）＝ズーム18（横 約640メートル）。中心はどちらも野口原の代表点
  G3（c213）＝ズーム17。中心は青山町と上田の湯町の代表点のまん中（2点の間 約370メートル）
  G7N（c216＝寄り）＝ズーム17・G7W（c601＝海まで広く）＝ズーム15（横 約5キロ）。中心は北浜のヨットハーバー（OpenStreetMap 33.27823,131.50798）
  G9（c504・c511＝日本全体）＝ズーム5（横 約56度＝日本列島が全部入る）
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'ep26', 'eizou_build', 'helpers'))
import gshot26 as G  # noqa: E402

YACHT = (33.27823, 131.50798)
NOGUCHI = (33.284962, 131.486786)
G.GMAP = {
    'G1': dict(ll=(33.2816, 131.4974), z=16, file='ref/ep27/photo/gmap_g1_route.png'),
    'G2W': dict(ll=NOGUCHI, z=17, file='ref/ep27/photo/gmap_g2w_noguchibaru.png'),
    'G2N': dict(ll=NOGUCHI, z=18, file='ref/ep27/photo/gmap_g2n_noguchibaru.png'),
    'G3': dict(ll=(33.27805, 131.49375), z=17, file='ref/ep27/photo/gmap_g3_aoyama.png'),
    'G7N': dict(ll=YACHT, z=17, file='ref/ep27/photo/gmap_g7n_yacht.png'),
    'G7W': dict(ll=YACHT, z=15, file='ref/ep27/photo/gmap_g7w_bay.png'),
    'G9': dict(ll=(36.5, 136.0), z=5, file='ref/ep27/photo/gmap_g9_japan.png'),
}
# 道具の置き場（プロファイル・一時の html）を27本目の src/ へ（gshot26 は自分の回の src/ を使う）
G.EP = os.path.dirname(os.path.dirname(HERE))
G.REPO = os.path.dirname(os.path.dirname(G.EP))

if __name__ == '__main__':
    if sys.argv[1] == 'shot':
        args = [a for a in sys.argv[2:] if not a.startswith('--')]
        o = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
        args = [a for a in args if a != o]
        sys.exit(G.shot(args[0] if args else None, o))
    elif sys.argv[1] == 'px':
        r = G.GMAP[sys.argv[2]]
        print('%.1f %.1f' % G.px(float(sys.argv[3]), float(sys.argv[4]), *r['ll'], r['z']))
