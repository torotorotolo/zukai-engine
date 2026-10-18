# NotoSansKR-Hangul-Bold.woff2 の出どころ

- 元：Google Fonts 公式の置き場 `https://raw.githubusercontent.com/google/fonts/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf`
  （可変の書体・10,414,588 bytes・md5 `138709011225153288f260a9beacc90a`・2026-10-18 に取得・git の外 `ref/ep23/src/font/` に置いた）
- 許諾：SIL Open Font License 1.1（同じ置き場の `OFL.txt` を写した＝この置き場の `OFL.txt`・md5 `9e6561baca2756628871baf0c1e23539`）。
  予約された書体名は「Source」だけ＝縮めた版は Noto Sans KR の名前のまま（「Source」を名乗らない）
- 作り方：`python fonts/notosanskr-license/make_subset.py <元の ttf>`＝太さ 700 に固定（fontTools の instancer）→ ハングルの音節すべて
  （U+AC00〜D7A3・11,172字）＋空白だけに縮めた woff2（`fonts/NotoSansKR-Hangul-Bold.woff2`）。作り直すと時刻の欄などで bytes が少し変わる
  ＝リポの版の md5 は下の表で照らす
- なぜ：事故検証 23本目（三豊百貨店のリメイク）の画面の出典の行にハングル（ソウル研究院の「서울연구데이터서비스」・Commons の個人の作者欄の名前）が出る。
  NotoSansJP にハングルが無い＝豆腐になる（門番 `tools/check_layout.py`）→ 2026-10-18 カズヤくん了承で書体を足した。
  🔴 使う字だけに縮めない（作者の名前の字だけの書体にすると、公開リポから名前の字が読める＝「名前0」）
- 使い方：`tools/scene_jiko.ensure_css` が書体名「Noto」の @font-face をもう1つ `unicode-range: U+AC00-D7A3` で足す（図の SVG は直さない）。
  物差し＝`tools/fontmetrics.FALLBACK`（字幅・字面・無い字の判定でハングルはこの書体を引く）

| ファイル | bytes | md5 |
|---|---|---|
| `fonts/NotoSansKR-Hangul-Bold.woff2` | 540140 | `34b483f198f7e3fc3800477fa1e11ff8` |
