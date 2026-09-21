# 11本目 ── 写真の当て先（⑤c-2 の実績と、残り15件）

**作った日＝2026-09-21（⑤c-2）。最終更新＝同日。**
⚠️ **ここに出ている「当て」は、まだ絵を見て決めたものではありません。**採否は⑤c-3 でシートを見てから。
→ 記憶 [[feedback-inventory-is-not-usable-material]]

---

## 0. いまの数（⑤c-2 の実績）

| | 件数 |
|---|---:|
| 台本が要求する欄 | **90** |
| ✅ 落として、カットも書けた | **75** |
| 🔴 **まだ当てが無い** | **15**（§3） |

- `ref/ep11/` にある画像＝**75点**（写真55点＋動く映像からの止め絵20点）
- カットは **175/190** 書けている。**欠けている15件は全部 実写の欄**
  ＝ 埋まれば写真映像は **90/190 ＝ 47.4%** に戻る
  （いまの `check_cuts` が出す 42.9% は**未完のせい**で、設計の問題ではない）

---

## 1. 🔴🔴 ⑤c-2 でいちばん大事だったこと ── 題名も説明も嘘をつく

`ep01`（報告書の表紙）に当てていた Commons の **`Rogers-report-front-page.png`** は、
**題も説明も「Cover of final report for the Rogers Commission」**なのに、
**絵は米上院の公聴会記録の表紙**でした。

```
SPACE SHUTTLE ACCIDENT
HEARINGS BEFORE THE SUBCOMMITTEE ON SCIENCE, TECHNOLOGY, AND SPACE
UNITED STATES SENATE ／ FEBRUARY 18, JUNE 10 AND 17, 1986
```

⚠️ **題名と説明だけでは落とせません**（どちらも「ロジャース委員会の報告書」と言うので）。
見つけたきっかけは **`check_blank` の「インク率2.0%＝白紙98%」**でした。
白すぎるのを鳴らす門番が、**中身の取り違え**を連れてきたことになります。

→ `cuts/ss.py` の `NG_PHOTOS` に理由ごと登録ずみ（使うと読み込みで止まります）。
→ **本物の表紙は Commons に無い**（3通りの語で0件）。⑤c-3 で別の置き場を当たること。

---

## 2. 動く映像から取る20件 ── **落としてあります**

🔴 **`until` は「ショットの終わり −1.0秒」**／**ショットの境目をまたがない**。
🔴 **`rate` は「使える秒 ÷ 音の尺」。**音の尺は間（gap）を含むので、
　 切り上げると尻が出ます（実測：0.74 だと `pr02` が +0.59秒 はみ出した）。

### 2-1. 動画にした7件（`footage.USE` に書いてあります・`fetch --check` ✓）

| カット | 欄 | 帯 | 局所 start–until | 元の秒 | rate |
|---|---|---|---|---|---:|
| `pr02` | launch_liftoff | `launch` | 16–22 | 614–620 | 0.67 |
| `pr07` | srb_oring | `joint` | 24–35 | 1562–1573 | 0.73 |
| `c101` | pad_39b | `pad` | 30–57 | 1174–1201 | 1.0 |
| `c307` | smoke_liftoff | `smoke` | 6–16 | **1454–1464** | 1.0 |
| `c413` | srb_destruct | `accident` | 41–57 | 703–719 | 1.0 |
| `c503` | srb_field_joint | `joint` | 36–47 | 1574–1585 | 1.0 |
| `c603` | thiokol_plant | `srb` | 30–43 | 1023–1036 | 1.0 |

⚠️ **`c709` は動画にしていません。**使える帯が **元59〜64 の5秒**しかなく
　 （64〜66秒に未特定の `ROBERT R…` の名札）、尺9.92秒だと **0.50倍速**になるためです。
　 **自分で決めた「0.6 を下回るものは動画にしない」**に当たるので、止め絵にしました。

### 2-2. 止め絵で抜いた13件（`ss.still()`。実写の数は変わりません）

| 欄 | 帯・局所秒 | 元の秒 | 中身 |
|---|---|---:|---|
| `ice_icicle`（pr01） | t_ice 14 | 1119 | 氷に覆われた配管 |
| `ice_trough`（c105） | t_ice 9 | 1114 | **水受けの厚い氷**。🔴 額入り 470×479 |
| `ice_icicle_2`（c107） | t_ice 23 | 1128 | 霜の付いた梁 |
| `ice_box`（c109） | t_ice 18 | 1123 | 🔴 **氷でふさがった通信箱** |
| `ssme_ignition`（c303） | launch 9 | 607 | 主エンジンの点火 ⚠️ 点火の瞬間かは未確認 |
| `srb_stack`（c501） | srb 48 | 1041 | 積み上げ |
| `oring_physical`（c506） | joint 2 | 1540 | ゴムの輪の現物 |
| `oring_channel`（c522） | joint 8 | 1546 | 溝 |
| `commission_hearing`（c911） | commission 2 | 57 | 机の上のシャトル模型 |
| `commission_testimony`（c709） | commission 6 | 61 | 木の壁の委員会室 |
| `commission_room`（c819） | commission 12 | 67 | 青い幕の公聴会場 |
| `commission_members`（c912） | commission 14 | 69 | **壇上に並ぶ委員** |
| `commission_hearing_2`（c710） | commission 19 | 74 | 公聴会の席 |

⚠️ **`pr01` に当てるコマは⑤c-3 で決め直す。**いまは 元1119（配管・全画面）。
　 台本の言葉は「**発射塔に下がったつらら**」なので 元1133（構造材のつらら）のほうが近いが、
　 **1133 は額入り（473×479）**。**2コマ並べて決めること。**

---

## 3. 🔴🔴 まだ当てが無い15件 ── ⑤c-3 の本題

| カット | 欄 | 台本が求めるもの | なぜ無いか |
|---|---|---|---|
| `c513` | joint_test | 継ぎ目の試験（すきま 0.74mm / 0.43mm） | 報告書の図しか無い |
| `c517` | oring_resilience_test | 弾力の試験 | 同上 |
| `c519` | srb_sun_shade | 日なたと日かげ | 同上 |
| `c803` | joint_qual_test | 継ぎ目の認証試験 | 同上 |
| `c804` | srm_horizontal | 横に寝かせた試験 | 同上 |
| `c810` | srm_nozzle_51b | 1985年のノズル継ぎ目の焼け | 同上 |
| `ep02` | joint_redesign | 作り直された継ぎ目 | 同上 |
| `ep03` | joint_test_new | 新しい試験 | 同上 |
| `ep04` | srm_vertical_test | 立てて燃やす試験 | 同上 |
| `c606` | oring_soot | 51-C の黒い跡（円周110度ぶん） | **別の飛行**の絵が要る |
| `c605` | launch_51c | 1985年1月の飛行 | 同上 |
| `ep07` | oring_data_chart | 過去の飛行の記録 | 図。Commons の SVG は 388×179 |
| `c716` | thiokol_telefax | 送られた書面 | 文書 |
| `c613` | marshall_center | マーシャル宇宙飛行センター | ⚠️ HAER 航空写真が候補だが**撮影年が未確定**（LoC が403） |
| `ep01` | commission_report | 報告書の表紙 | 🔴 **§1 の取り違え**。本物は Commons に無い |

### 🔴 先に当たるべき場所

1. **`burn.mpg`（元2494〜2626）**＝⑤cが「`debris` は足りているので予備」として残した帯。
   **全画面が 2497〜2580（83秒）と 2596〜2622（26秒）**つづくことは `boxes.json` で測ってある。
   中身＝2504 構造材の寄り／2524 KSC の格納庫／2564 **床に並べた焼けた残骸**／
   2604 **焼け抜けた跡のある大きな板**。
   ⚠️ **2544 は「試験装置の図と赤い印の並ぶ表」＝図なので採らない。**
   ⚠️ **2584 は額入り（576×479＝80%）。**
   ⚠️ **2615 の「黄色い丸＋`291°`」は誰も見ていない**（⑤cは 2604 まで）。
   ⚠️ 🔴 **51-L の焼け跡を「51-C の黒い跡」に当てない**（`c606` は別の飛行）。
2. **②の網は幅1280以上で切っている**＝小さい実物は候補の表に出ていない。
   `commons_ep11.txt` の「小」印の行を当たること
   → 記憶 [[feedback-absence-of-a-word-is-not-absence]]
3. **図に振り替えてよいのは最大4カット**（写真映像 90/190＝47.4%。下限45%＝85.5カット）。

---

## 4. 落としてある75点の台帳

正本＝`ref/ep11/assets.json`（置き場に引き直した実測）と `ref/ep11/credits.json`。
一覧は `ref/CREDITS.md` の §スペースシャトル・チャレンジャー号（75行・手書きでなく書き出し）。

```
python qa_out/ep11_assets.py check     # 台本の欄・PICK・台帳・ファイルの4つを突き合わせる
python qa_out/ep11_assets.py sheet     # 640px のシート（2列×3行）
python qa_out/ep11_assets.py panel     # 切り落とし率の並び（PANEL_AR の材料）
```

⚠️ **小さい点が24件あります**（20件は動く映像の640×480＝元がこの大きさ／
4件は `ice_team` 481×600・`flame_plume_2` 477×621・`telecon_room` 630×450・
`smoke_puffs` 751×523）。`ss.kind()` が **幅1280未満は額装**に回します。

⚠️ **同じ1枚を2カットで使っている組が3つ**あります。⑤c-3 で**2コマ並べて、
別の絵に見えるか**を確かめてください：
`fireball`＝`hydrogen_burn`（c406／c403）・`oring_erosion_photo`＝`srb_inside`（c705／c905）。

---

## 5. 関連
- [footage_map.md](footage_map.md)（動く映像の正本）／[slot_fill.md](slot_fill.md)（⑤bの台帳）
- [materials.md](materials.md)（②の置き場の実測）／`commons_ep11.txt`・`nasa_ep11.json`（候補の原簿）
- 道具＝[parse_script.py](parse_script.py)・[sweep_box.py](sweep_box.py)・[make_clips.py](make_clips.py)
  ／`qa_out/ep11_assets.py`（写真の束）
