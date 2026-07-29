# zukai-engine — 図解・サムネの描画基盤

新チャンネル（シニア向け健康解説）の映像素材を、**費用0円・SVG＋Chrome headless** で作るための基盤。
Node も Remotion も使わない（このPCは空きディスク6GB・メモリ4GBのため）。

## 動かし方

```bash
python tools/character.py       # キャラの検証シート3枚を out/ に出す
python tools/scene_char_demo.py # キャラ入りの本編フレーム1枚
python tools/scene_liver.py     # 臓器図の本編フレーム試作
python tools/thumb_photo.py     # PD写真＋文字のサムネ
python tools/_check_organs.py   # 腎臓・脳の形の検証シート1枚
python tools/scene_open30.py    # 冒頭30秒の本編フレーム8枚（引数でc1a等を指定すると部分再生成）
```

冒頭30秒を動画にするところまで：

```bash
python tools/scene_open30.py && cd out/open30 && ffmpeg -y -f concat -safe 0 -i concat.txt -t 29.6 -vf "fps=30,format=yuv420p" -c:v libx264 -crf 20 open30.mp4
```

※ `concat.txt` は `plan.json` から作る。**本番の動画レンダはクラウド**（ここは尺の検証用）。

Chrome/Edge の headless で SVG→PNG する。**追加インストールは一切不要**。

## ファイル

| ファイル | 役割 |
|---|---|
| `tools/character.py` | **キャラクター部品**。表情5種×ポーズ5種＋衣装3種。比率は参考動画の実測から起こした |
| `tools/scene_open30.py` | **冒頭30秒（4カット×2状態＝8枚）**。背景3種（キッチン／ラボ／リビング）と見出し・字幕・ボードの部品つき。尺の設計値は Vault `Resources/参考-HSS秒単位分解-20260728.md` の実測（1カット7.4秒） |
| `tools/scene_char_demo.py` | キャラ入り本編フレームの試作（リビング・見出し・黄色字幕・棒グラフ） |
| `tools/shading.py` | グラデーション／地紋／落ち影／周辺減光／手描き揺らぎの共通部品 |
| `tools/anatomy.py` | 人体と臓器。**形の根拠を各関数のコメントに明記**してある。`kidney()` `brain()` は原点中心の単体プロップで、場面に浮かせて使う |
| `tools/scene_liver.py` | 本編フレームの試作（砂糖をやめて7日目・肝臓） |
| `tools/thumb_photo.py` | サムネ生成器。写真＋文字4つを渡すだけ |
| `tools/render.py` | SVG→PNG（Chrome/Edge headless） |
| `tools/grab_frames.py` | ブラウザcanvasのbase64を画像に戻す（参考動画のフレーム抽出用） |
| `ref/` | 取り寄せた実物資料（PD解剖図・PD写真・PD表情図版・PD連続写真・参考動画のフレーム） |

### キャラクターの使い方

```python
import character as C
svg = f'<svg ...><defs>{C.defs()}</defs>{C.character("point", "smile", at=(700, 980))}</svg>'
C.character("hold", "normal").anchors["hand"]   # 小道具を置く座標が取れる
```

設計の正本は Vault `Resources/キャラクター設計-健康解説-20260728.md`。
実測値と「なぜその形なのか」は `tools/character.py` の冒頭に全部書いてある。

## 押さえておくべき技術

### フォントは base64 で埋め込む
`Desktop\zankoku-sekkeizu\public\fonts\` から読む。
- **DelaGothicOne.woff2** … 超極太（SIL OFL）。サムネの見出しはこれ。
  Yu Gothic UI には本物のブラックウェイトが無く、`font-weight:900` と書いてもBold止まりになる
- NotoSansJP-Bold.woff2 / NotoSerifJP-SemiBold.woff2

埋め込むので Windows でもクラウド(Ubuntu)でも字形が一致する＝豆腐事故が起きない。

### 文字を太らせずに縁取る
`paint-order="stroke fill"` を使う。普通に stroke をかけると内側が食われて字が痩せる。

### 文字数が変わっても幅を揃える
`textLength` ＋ `lengthAdjust="spacingAndGlyphs"`。
級数は「狙う高さ」で決め打ちし、横は textLength で圧縮する（縦長のコンデンス化）。
これで**文字数に関係なく「幅いっぱい×縦もでかい」**が両立する。`thumb_photo.py` の `fit()` 参照。

### 素材はパブリックドメインだけ
Wikimedia Commons API で機械判定して落とす。
```
action=query&list=search&srnamespace=6           # 探す
prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1920   # LicenseShortName を見る
```
`Public domain` のものだけ使う。米連邦機関（NTSB/USCG/NASA/NOAA）は全てPD。
概要欄に出典を必ず入れる。

### 図は必ず実物を見てから描く
記憶で描くと形が狂う（肝臓が楕円になった実例あり）。`ref/` に資料を落としてから描く。

**資料は「形が分かる図」でなく「名前が振ってある図」を探す。**
脳は Gray728（葉が色分けされただけ）で描いて低品質になり、
Sobotta 1909 Plate 626（**脳溝脳回に名前が振ってある実物写生**）を取り直して作り直した。
名前が振ってあると、しわの**向き**まで決められる＝乱数で撒かずに済む。

### 生き物の表面（しわ・ひだ）の描き方 ← 脳で8回作り直して出た結論
1. **溝（谷）を細線で引くと「塗った縞」になる。** 谷1本につき「広い薄影／稜線ハイライト／
   反対側の影／深い谷」の4層で描く。**ずらす量は溝の幅から計算**すること
   （内側に置くと谷の線に覆われて消える）。ずらす向きは経路から機械判定する
2. **隆起を1本ずつ管として描くのも駄目。** 短い枝が「面に転がったマカロニ」になる
3. **手で十数本並べても面は埋まらない。** territory ごとに流れ場（基準線＋法線＋広がり）を
   定義して族を生成し、隣どうしを短い枝でつなぐ
4. 基準線は territory の**真ん中**に通す。端に通すと族が片側に寄る
5. **族ごとに縄張りをクリップする。** しないと隣の族と直交してカゴ編みになる
6. 間隔・長さ・太さは必ずばらす。ただし**端を境界に届かせたい族は縮め量を小さく**する
7. 下地は隆起と同色に。暗くすると隙間が穴に見える

詳細は `anatomy.py` の `_family()` `_sulci()` `_scallop()`。腸や皮膚のしわにもそのまま使える。

### 背景は「壁＋床＋家具3つ」では足りない
参考動画の背景には**小物が10個前後**ある。1画面あたり15点以上置く。置き場所の原則：
- キャラの立ち位置 ±150 に背の高い物を置かない（コンロが頭に隠れた）
- 画面上端 y<160 は見出しの帯。時計を置くと切られる
- **主役の図を置く区画は、あらかじめ無地の壁だけにして空けておく**
- 家具・鉢植えは必ず床に接地させる／壁の掲示物は作業台より上に置く
- ラグは楕円でなく台形にする（楕円は床の茶色い水たまりに見える）

### 首の無いキャラの姿勢
- 頭を横へずらして前傾を表してはいけない。首が無いので「頭が付いていない」に見える。
  **肩に沈める**（`hsink`）で表す
- 腕の付け根は肩の半幅より**外**に出す。内側だと手前の腕が胴に貼りつき、奥の腕が隠れて
  太さが左右で違って見える
- **奥の足のつま先は外向きにする。** 両足を同じ向きにすると奥足が体の中心を跨いで内股に見える
- 脚の間隔は脚の太さより広く取る。狭いと輪郭線どうしが接して「ズボン1本に線が入っただけ」になる

詳細は `character.py` の `_skeleton()` と `_shoe()`。

## 直したら必ず5回以上見直す（2026-07-28・ユーザー指示）
1回直して終わりにしない。**毎回レンダリングして拡大目視 → 直す**を繰り返す。
検証用シートを使う：`_check_organs.py`（臓器）／`_check_pose.py`（立ち姿・中心線つき）。
実際、脳は8回・背景は5回・脚は2回まわして、毎回別の欠陥が出た。

## 動画のレンダリング
**必ずクラウド（GitHub Actions）で行う**（ユーザー指示）。
ローカルは台本・音声・静止画の生成までに留める。
