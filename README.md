# zukai-engine — 図解・サムネの描画基盤

事故検証チャンネル（1本目＝タイタン号）の映像素材を、
**費用0円・SVG＋Chrome headless** で作るための基盤。
Node も Remotion も使わない（このPCは空きディスク6GB・メモリ4GBのため）。

> 2026-08-01：**シニア向け健康解説チャンネルの資産を撤去した。**
> `character.py` `anatomy.py` `cartoon.py` と参考画像・生成物を消してある。
> 消したものは git 履歴に残っているので `git log --diff-filter=D --oneline -- tools/` から辿れる。
> 図解の作り方の知見は Vault `Resources/描画の知見-人体と首なしキャラ-20260801.md` に移した。

---

## 🔴 本編mp4を GitHub Actions で焼かないこと（2026-07-31）

GitHub の Actions 規約は、GitHub-hosted runner を
**そのリポジトリのソフトウェアプロジェクトと無関係な活動**に使うことを禁じている。
**34分・61,320コマの本編動画を毎本焼くのはここに当たる**（永久BANの報告あり）。
同一アカウント群に他チャンネルの制作基盤が全部載っているので、影響は動画1本では済まない。

| 工程 | どこで回すか |
|---|---|
| 検品画像（qa）・4つの機械検査 | ✅ GitHub Actions（`render-jiko.yml`。`mode=full` は入力ごと削除済み） |
| **本編mp4の製造** | ✅ **Modal**（`modal_app.py`。1本 約$0.25／無料枠 $30/月） |
| ナレーション合成 | ローカル（AivisSpeech。⚠️ 使うときだけ起動する） |

```bash
modal setup                                        # 最初の1回だけ
modal volume create jiko-assets                    # 最初の1回だけ（BGMの保管庫）
modal volume put jiko-assets assets/bgm.mp3 bgm.mp3
git push                                           # ★Modalは GitHub から clone する
modal run modal_app.py::full --note r11            # 本編を焼く
modal volume get jiko-out titan_audio-r11.mp4 out/jiko/
```

🔴 **BGM は保管庫（`/assets/bgm.mp3`）にしか無い。**
既製曲（DOVA-SYNDROME）は作者が再配布を禁止しており、このリポジトリは public なので置けない。
`audio_mix.find_bgm()` は見つからないと**黙って自作ドローンに戻る**ため、
`full` は焼き始める前に保管庫を見て、無ければ止める（`--allow-drone` で解除）。

移設で**画が変わっていないこと**は `tools/layer_hash.py` の指紋で機械確認する。
`full` がレイヤーを焼いた直後に指紋を出すので、Actions の "Layer fingerprint"
ステップのログと見比べればよい（本編を焼かずに指紋だけ欲しいときは
`modal run modal_app.py::layer_hash`）。

**2026-08-01 実測：Actions と Modal で一致（`4c5e87a4…c378fedb` ／ 1178枚・51.4MB）。**

## 動かし方

```bash
python tools/dump_script.py c3        # その章の台本と尺（図を書く前に必ず読む）
python tools/scene_jiko.py --report   # 226カット全部に画があるか
python tools/check_layout.py          # 画面外・重なり・豆腐（字幅はフォントから実測）
python tools/check_echo.py            # 図がナレーションの複写になっていないか
python tools/check_mask.py            # 語尾がBGMに埋もれていないか
python tools/thumb_jiko.py            # サムネ
python tools/brand_jiko.py --check    # アイコン／バナーを実寸で並べて見る
```

検品は**クラウドで焼いたものだけ**を見る（ローカルはフォントの折返しが変わる実績がある）。

```bash
gh auth switch -u torotorotolo
gh workflow run render-jiko.yml --repo torotorotolo/zukai-engine -f note=rN -f mode=qa
python tools/gc_artifacts.py --keep 2   # ★巡が終わるたびに。成果物枠は500MB
```

Chrome/Edge の headless で SVG→PNG する。**追加インストールは一切不要**。

## ファイル

| ファイル | 役割 |
|---|---|
| `tools/cuts/<章>.py` | **カットごとの「画」。ふだん直すのはここだけ** |
| `tools/cuts/README.md` | **型の一覧と守ること（仕様書）。書く前に読む** |
| `tools/titan_fig.py` | 図解の型21種 |
| `tools/jiko_style.py` | 色・級数・置き場所の定数 |
| `tools/scene_jiko.py` | レイヤー書き出しのエンジン（SVG→PNG） |
| `tools/build_jiko.py` | 合成（`qa`／`full`／`veil`／`shrink`） |
| `tools/fontmetrics.py` | **字幅と字面をフォントから実測**（推定値を置かないため） |
| `tools/narration.py` | 台本の文言の正本 |
| `tools/audio_pack.py` | wav ⇄ opus（wavはリポジトリに入れない） |
| `tools/audio_mix.py` | ナレーション＋BGM＋効果音 |
| `tools/thumb_photo.py` | サムネ生成器。写真＋文字4つを渡すだけ |
| `tools/thumb_jiko.py` `tools/brand_jiko.py` | 本番サムネ／チャンネルのアイコン・バナー |
| `tools/render.py` | SVG→PNG（Chrome/Edge headless） |
| `tools/layer_hash.py` | レイヤーPNGの指紋（Actions と Modal の突き合わせ） |
| `tools/gc_artifacts.py` | 成果物の掃除（500MB枠） |
| `ref/` | 一次資料（NTSB/USCG/NOAA の PD写真・報告書）。出所は `ref/CREDITS.md` |

`tools/palette.py` `tools/shading.py` は「まちがい探し喫茶」用で、
**どこからも import されていない**（残置）。

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

### 級数と余白を推定で置かない
`fontmetrics.py` が woff2 の hmtx と glyf を直接読んで**全字の送り幅**を出す。
「実測値」と言われている平均値でも足りない。Dela の数字は
**0.588（"1"）〜0.924（"4"）で 1.57倍ちがう**ので、平均 0.84em で「4,444」を見ると
実物より 8% 狭く出る＝**通してしまう向きの誤差**になる。

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
名前が振ってあると、しわの**向き**まで決められる＝乱数で撒かずに済む。

## 直したら必ず5回以上見直す（2026-07-28・ユーザー指示）
1回直して終わりにしない。**毎回レンダリングして拡大目視 → 直す**を繰り返す。
機械の検査（`check_layout` `check_echo` `check_space` `check_mask`）は
**目で見つかる粗を1件も出さない**。実際、検品9巡のうち目で見た2巡だけで
「引用の行分けが語の途中で割れる」「箱が大きいだけで中身が上端の文字だけ」が出た。

## 動画のレンダリング
🔴 **必ずクラウドで行う**（ローカルはメモリ4GB）。
**本編mp4は Modal、検品画像は GitHub Actions。**
ローカルは台本・音声・静止画の生成までに留める。
