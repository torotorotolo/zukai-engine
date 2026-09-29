# けいふぉんと（keifont.ttf）の出どころとライセンス

- 書体：けいふぉんと（Keifont / Version 1.01・14,963字）
- 作者・配布元：Do-Font「すもももじ」 https://font.sumomo.ne.jp/font_1.html
- 取得：2026-09-29（事故検証ch 14本目 ⑥-2・カズヤくんの GO）
  - `https://font.sumomo.ne.jp/fontdata-c2157415/k-font.zip`（2,792,303 バイト・Last-Modified 2014-09-08・md5 `41cf4027dfafdd4d3da2f46c57611220`）
- `fonts/keifont.ttf` は zip の中の `keifont.ttf` を**手を加えずそのまま**置いたもの（4,348,192 バイト・md5 `3d8226e3dfaf3216220f31ced0ca61cd`）。形式の変換・サブセット化（使う字だけ抜き出すこと）もしていない

## ライセンス
- 配布ページの原文：「このフォントは、Apache License 2.0のもとで使用することができます。」「商用利用については特に制限しておりません」
- お願い（配布ページと同梱の説明書き）：ヒント元となった作品（『けいおん！』のロゴ）の名誉を傷つける場面での使用はご遠慮ください
- ひらがな・カタカナ以外の字は、源ノ角ゴシック（Adobe）・M+ OUTLINE FONTS（M+ FONTS PROJECT）・源真ゴシック（自家製フォント工房）に由来する（著作権の表示は同梱の説明書きのとおり）

## このフォルダの中身（zip に同梱のものをそのまま）
| ここでの名前 | zip の中の名前 | 中身 |
|---|---|---|
| `Apache-License-2.0.txt` | `【源真ゴシック・源ノ角ゴシック】Apache License 2.0.txt` | Apache License 2.0 の本文（バイト単位で同じ・名前だけ ASCII に） |
| `README-ja.txt` | `利用前にお読みください.txt` | 作者の説明書き（Shift-JIS のまま・バイト単位で同じ） |
| `README-ja.utf8.txt` | （同上） | 上の説明書きを UTF-8 に直しただけの写し（中身は同じ・GitHub で読めるように） |
| `mplus-TESTFLIGHT-058/` | `mplus-TESTFLIGHT-058/` | M+ FONTS のライセンスと説明書き（そのまま） |

## リポでの使い方
- 字幕の層だけに埋め込む（`tools/scene_jiko.py` の `sub_css`）。書体の名前は `Kei`（`tools/fontmetrics.py` の `FAMILY_FILE`・回ごとの設定 `tools/el_script.py` の `SUB_FONT`）
- 動画の字幕として画面に焼き込む（書体のファイルを動画と一緒に配るわけではない）
