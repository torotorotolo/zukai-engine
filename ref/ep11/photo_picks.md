# 11本目 ── 写真の当て先（⑤c-3 で**全部埋まりました**）

**作った日＝2026-09-21（⑤c-2）。最終更新＝2026-09-22（⑤c-3）。**
⚠️ ここに出ている当ては、**すべてシートで絵を見てから決めたもの**です（⑤c-3）。
→ 記憶 [[feedback-inventory-is-not-usable-material]]

---

## 0. いまの数（⑤c-3 の実績）

| | 件数 |
|---|---:|
| 台本が要求する欄 | **90** |
| ✅ 写真を当てた | **80** |
| ✅ 動く映像にした（`footage.USE`） | **7** |
| 🔵 **写真を当てず、図で描く** | **3**（§4） |
| 🔴 まだ当てが無い | **0** |

- カットは **191/191** 書けています（`check_cuts` ✓）。
- 写真映像は **87/191 ＝ 45.5%**（規則 45〜50%）。**余裕は1カットぶんだけ**なので、
  ⑤c-4 以降で写真カットを図に替えると**下限を割ります**。

### 🔴🔴 ⑤c-2 の「残り15件」は数え落としがありました

`check_cuts` は**音の側**（`audio/narration.json`＝**191カット**）を正として数えます。
⑤c-2 が数えた「15件」は**写真の欄だけ**で、**共通エンディング `ed01`（7.4秒）が抜けて**いました。
＝ 本当の宿題は **16件**でした。`ed01` は `tools/cuts/ep.py` の末尾に書いてあります。

---

## 1. 🔴🔴 ⑤c-3 で見つけた「題名と説明の嘘」── 3種類あります

### 1-1. 説明が**別物**（⑤c-2 の型）

`ep01` に当てていた Commons の `Rogers-report-front-page.png` は、
**題も説明も「Cover of final report for the Rogers Commission」**なのに、
**絵は米上院の公聴会記録の表紙**でした（`check_blank` のインク率2.0%で発覚）。

✅ **本物を見つけました**＝ Internet Archive の蔵書スキャン **`reporttopreside00unit`** の表紙。
絵を見て確かめています（大統領章＋青い表紙＋`Report of the PRESIDENTIAL COMMISSION on
the Space Shuttle Challenger Accident`）。**インク率 97.8%。**
取り込み口は `qa_out/ep11_assets.py` の **`IA()`**（⑤c-3 で新設）。

### 1-2. 説明が**短すぎる**（⑤c-3 で踏んだ新しい型）

`c519` に当てた NASA画像庫 **`86pc0081`** の説明は
**「KENNEDY SPACE CENTER, FLA. -- STS-51-L: Challenger」だけ**でした。
日付も場所も正しいのに、**絵は打ち上げの瞬間**で、c519 が要る「射点に立つ機体」ではありません。

⚠️ **説明が短いほど危ない。**「間違っていない説明」は「合っている絵」を意味しません。

### 1-3. 🔴🔴 題名と絵が**逆**（⑤c-3 で2組）

| ID | 題名・説明 | 実際の絵 | 当てた先 |
|---|---|---|---|
| `7997301` | 「Qualification Motor-1」＝**認証試験** | **砂漠の試験台に横たわる全尺モーター** | 🔴 **c804**（横に寝かせて燃やす） |
| `8777958` | 「TPTA **field joint**」＝継ぎ目 | **クレーンで吊って縦に降ろす** | 🔴 **ep04**（立てた状態で燃やす） |

→ **絵が正本。**題名どおりに当てると、言っていることと絵が逆になっていました。

---

## 2. 動く映像から取る24件 ── **落としてあります**

🔴 `until` は「ショットの終わり −1.0秒」／**ショットの境目をまたがない**。
🔴 `rate` は「使える秒 ÷ 音の尺」。音の尺は間（gap）を含むので、切り上げると尻が出ます。

### 2-1. 動画にした7件（`footage.USE`・`fetch --check` ✓）

| カット | 欄 | 帯 | 局所 start–until | 元の秒 | rate |
|---|---|---|---|---|---:|
| `pr02` | launch_liftoff | `launch` | 16–22 | 614–620 | 0.67 |
| `pr07` | srb_oring | `joint` | 24–35 | 1562–1573 | 0.73 |
| `c101` | pad_39b | `pad` | 30–57 | 1174–1201 | 1.0 |
| `c307` | smoke_liftoff | `smoke` | 6–16 | **1454–1464** | 1.0 |
| `c413` | srb_destruct | `accident` | 41–57 | 703–719 | 1.0 |
| `c503` | srb_field_joint | `joint` | 36–47 | 1574–1585 | 1.0 |
| `c603` | thiokol_plant | `srb` | 30–43 | 1023–1036 | 1.0 |

⚠️ `c709` は動画にしていません（使える帯が5秒しかなく 0.50倍速になるため。止め絵に変更）。

### 2-2. 止め絵で抜いた17件

⑤c-2 の13件に、**⑤c-3 で4件足しました**（下の 🆕）。

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
| 🆕 `srb_sun_shade`（c519） | pad 12 | **1156** | **射点39Bに立つ機体**（日なた・日かげが見える） |
| 🆕 `oring_soot`（c606 の地） | joint 16 | **1554** | 継ぎ目の上端と黄色い治具 |
| 🆕 `joint_test`（c513 の地） | joint 22 | **1560** | 継ぎ目の縁の寄り |
| 🆕 `oring_resilience_test`（c517 の地） | joint 58 | **1596** | 継ぎ目の寄り・留め金の帯 |

### 2-3. 🔴 `joint.mpg` で**採ってはいけないコマ**（⑤c-3 で実測）

| 元の秒 | なぜ |
|---:|---|
| 1548 | 焼き込みの英字が下端に走る |
| 1551 | 焼き込みの**タイムコード** `6114:03-04-10.__` |
| 1592 | **ベル形の噴射口が2つ**写るが、前後を見ても**何の機体のどこか確定できない**。推測で採らない |
| 1594 | **画面に描き足した白い丸印**が乗る（1596 は印なし） |

### 2-4. ⚠️ `burn.mpg` の未確認が1件、解けました

⑤c が「2604 までしか見ていない」と残した **元2615 の「黄色い丸＋`291°`」**を見ました。

- **黄色い丸＝画面に描き足した解説の印**（元2612・2615 に乗る。**元2608 と 元2619 は印なし**）
- **`291°` `307°` `316°` ＝現物に置いた紙の札**（焼き込みではない）
- 中身は **51-L の右側補助ロケットの焼け抜けた跡**。
  ⚠️ **51-C（c606）や 51-B（c810）に当ててはいけません。**

---

## 3. ⑤c-3 で当てた12カット

| カット | 欄 | 当て | 出どころ | ⚠️ |
|---|---|---|---|---|
| `c513` | joint_test | 継ぎ目の縁の寄り（**地**） | 記録映画 元1560 | 図が 0.74／0.43ミリを言う |
| `c517` | oring_resilience_test | 継ぎ目の寄り（**地**） | 記録映画 元1596 | 図は**縦軸に数字を置かない** |
| `c519` | srb_sun_shade | 射点39Bに立つ機体 | 記録映画 元1156 | `86pc0081` は落とした（§1-2） |
| `c605` | launch_51c | **51-C の打ち上げ** | Commons `STS-51C launch.jpg` | 原寸で「Discovery」を確認 |
| `c606` | oring_soot | 継ぎ目の上端（**地**） | 記録映画 元1554 | 跡そのものは図が描く |
| `c613` | marshall_center | 看板と第4200棟 | Commons `Marshall Space Flight Center Bldg. 4200.jpg` | 🔴 **2013年撮影**。副題で名乗る |
| `c803` | joint_qual_test | 全尺モーターの燃焼試験 | NASA `8776671`（1987） | 事故の後。副題で年を名乗る |
| `c804` | srm_horizontal | **横たわる全尺モーター** | NASA `7997301`（1979） | 事故の前。§1-3 で入れ替えた |
| `ep01` | commission_report | **報告書の本物の表紙** | IA `reporttopreside00unit` | 左上のバーコードを `trim` で外す |
| `ep02` | joint_redesign | 作り直したモーターの試験体 | NASA `8448351`（1988） | 894×1110＝額装に回る |
| `ep03` | joint_test_new | TPTA の燃焼試験 | NASA `8886217`（1988） | 温度・圧力・外力を掛ける試験台 |
| `ep04` | srm_vertical_test | **吊って縦に降ろす** | NASA `8777958`（1987） | §1-3 で入れ替えた |

🔴 **NASA画像庫の MSFC「Space Shuttle Projects」は題名が全部同じ**で、中身は `description`
にしかありません。**ID で採ること**（→ `tools/nasa_probe.py` §1）。

---

## 4. 🔵 写真を当てず、図で描く3欄（`AS_FIG`）

どれも**報告書の図でしか見たことのない主題**で、`cuts/ss.py` の決まり
「報告書から取り出した図は画面に出さない（英字が焼き込まれている）」に当たります。

| カット | 欄 | 下敷きにした報告書の図 | 描いた型 |
|---|---|---|---|
| `c716` | thiokol_telefax | 第I巻 97頁（送られたファクスの写し） | `people`（どこからどこへ渡ったか） |
| `c810` | srm_nozzle_51b | ― | `process`（一次→二次→打ち上げを止める札） |
| `ep07` | oring_data_chart | 第I巻 第VI章 図6・図7 | `absent`（`pair`。記録は在った／調べは無かった） |

⚠️ `c810` は「写真が無いから図」であって「図にしたかったから図」ではありません。
　 **51-B のノズル継ぎ目の写真は、NASA画像庫にも Commons にも0件**でした。

---

## 5. 原文で照合した数字（⑤c-3 で全件当たり直し）

| カット | 数字 | 原文 |
|---|---|---|
| `c513` | 0.74ミリ／0.43ミリ | 第IV章 Findings 8「.017 and .029 inches at the secondary and primary O-rings」 |
| `c513` | 0.6秒 | 同 8-a「begins upon ignition … essentially complete at 600 milliseconds」 |
| `c517` | 0.2〜0.3秒で最も速い | 同 8-a「reaches its maximum rate of opening at about 200-300 milliseconds」 |
| `c519` | 摂氏10度 | 同 6-b「the opposite side … facing the sun … about 50 degrees Fahrenheit」 |
| `c605` | 摂氏11.7度 | 第IV章の一覧「51-C FWD LH 163 **53**」（51-L の28°Fを除くと最低） |
| `c606` | 110度 | 第V章「SRM-15B [Right SRM, Flight 51-C] had a **110 degree arc of black grease**」 |
| `c606` | 10月の飛行は狭い | 同「SRM-22 [Flight 61-A, October, 1985] had … **less**」（**角度は原文に無い**） |
| `c716` | 午後11時15分 | 第V章「The conference was then terminated at approximately **11:15**」 |
| `c803` | 縮めた装置 | 第V章「a full-scale O-ring, full-scale groove, **in a scaled test device**」 |
| `c810` | 51-B のノズル | 第VI章「put on after we saw the **secondary O-ring erosion on the [51-B] nozzle**」 |
| `ep07` | 10件／150回 | 第IV章「10 instances of distress in a total of **150 flight exposures**」 |

---

## 6. 落としてある87点の台帳

正本＝`ref/ep11/assets.json` と `ref/ep11/credits.json`。
一覧は `ref/CREDITS.md` の §スペースシャトル・チャレンジャー号（**87行**）。

```
python qa_out/ep11_assets.py check                 # 台本の欄・PICK・台帳・ファイルの4つを突き合わせる
python qa_out/ep11_assets.py sheet <名の頭 …>       # 640px のシート（2列×3行）
python qa_out/ep11_assets.py credits --write --md  # 🆕 CREDITS.md の表ごと入れ替える
```

🆕 **`credits --md` を⑤c-3 で足しました。**今までは表を画面に出すだけで、
`ref/CREDITS.md` への反映が手作業でした。その結果、写真を12点足したときに
表が75行のまま残り、`check_credits` が12件止めました。**書き出しと表を1本につないであります。**

⚠️ **小さい点が29件あります**（動く映像の640×480が24点ほか）。`ss.kind()` が額装に回します。

⚠️ **同じ1枚を2カットで使っている組が2つ**あります。⑤c-4 で**2コマ並べて、
別の絵に見えるか**を確かめてください：
`fireball`＝`hydrogen_burn`（c406／c403）・`oring_erosion_photo`＝`srb_inside`（c705／c905）。

---

## 7. ⚠️ この機械の制約（⑤c-4 に引き継ぐ）

- 🔴 **コミットの空きが 0.35GB**（物理の空きは 2.86GB あるので**物理では分かりません**）。
  `check_blank` は**全87点を回すと MemoryError で門番ごと落ちます**。
  → **新しく足した点だけを本体に通す道具**を作ってあります：`qa_out/ep11_blank_new.py`。
  ⚠️ 判定は書き直していません（`check_blank.scan` と `report` をそのまま呼ぶ）。
- 🔴 `check_blank --check` の**絵を使う陽性対照は飛ばされます**（4本目の素材が手元に無い）。
  ⑤c-3 では**ほぼ白紙の絵を作って自分で当て直しました**＝
  本物の表紙 **インク率97.8%**／白紙 **0.0%（下限4.0%で鳴る）**。**物差しは生きています。**
- 🔴 `check_twin` は**焼いた静止画が要る**ので、このチャットでは回せません（⑤c-4 で）。

---

## 8. 関連
- [footage_map.md](footage_map.md)（動く映像の正本）／[slot_fill.md](slot_fill.md)（⑤bの台帳）
- [materials.md](materials.md)（②の置き場の実測）／`commons_ep11.txt`・`nasa_ep11.json`
- 道具＝[parse_script.py](parse_script.py)・[sweep_box.py](sweep_box.py)・[make_clips.py](make_clips.py)
  ／`qa_out/ep11_assets.py`（写真の束）／`qa_out/ep11_blank_new.py`（新しい点だけの白紙検査）
