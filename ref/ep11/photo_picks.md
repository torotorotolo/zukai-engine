# 11本目 ── 写真70点の当て先（⑤c-2 の下見。**まだ1枚も落としていない**）

**作った日＝2026-09-21（⑤c-2）。**
⚠️ **ここは「候補の当たり」であって在庫ではありません。**採否は⑤c-3 でシートを見てから。
→ 記憶 [[feedback-inventory-is-not-usable-material]]

---

## 0. 🔴🔴 いちばん大事なこと ── 写真は1枚も落ちていません

⑤b の「素材完了」は**出どころを決めたところまで**で、`ref/ep11/` にある画像は
**報告書の3頁（`img/v1p102.jpg` `v1p112.jpg` `v1p113.jpg`）だけ**です。

**これが写真カット90件を書けない理由です**（実測で確かめました）：

```
ss.kind("ep11/nonexistent.jpg") → FileNotFoundError
```

`cuts/ss.py` の `kind()` は写真を PIL で開き、**縦横比から額装にするかどうかを決めます**
（「目で決めない」という決まりのため）。＝ **ファイルが無いと章ファイルが1行も書けません。**

---

## 1. 90件の内わけ

| | 件数 | どこから |
|---|---:|---|
| 動く映像から（8件は動画・12件は静止画で抜く） | **20** | `footage_map.md`／`clips.json`／`shots.json` |
| 置き場の写真で**当てが付いた** | **約50** | Commons（`commons_ep11.txt`）／NASA画像庫（`nasa_ep11.json`） |
| 🔴 **当てが付いていない** | **約20** | 下の §3 |
| **合計** | **90** | |

---

## 2. 動く映像から取る20件（⑤c-2 で設計）

🔴 **`until` は「ショットの終わり −1.0秒」**（`tools/cuts/README.md` §5 の決まり）。
🔴 **ショットの境目をまたがない**（またぐと `footage.outside_shot()` が exit 3 で止める）。

### 2-1. 動画にする8件（`footage.USE` に入れる）

`rate` ＝ 使える秒 ÷ カットの尺。**0.6 を下回るものは動画にしない**
（4秒を12秒に引き伸ばすと、ほぼ止まって見えます）。

| カット | 欄 | 尺 | 帯 | 局所 start–until | 元の秒 | rate | 絵の幅 |
|---|---|---:|---|---|---|---:|---|
| `c307` | smoke_liftoff | 7.3s | `smoke` | 6–16 | **1454–1464** | 1.0 | ✅ 705 |
| `c413` | srb_destruct | 13.1s | `accident` | 41–57 | 703–719 | 1.0 | ✅ 703 |
| `pr02` | launch_liftoff | 8.1s | `launch` | 16–22 | 614–620 | 0.74 | ✅ |
| `c603` | thiokol_plant | 11.9s | `srb` | 30–43 | 1023–1036 | 1.0 | ✅ 703 |
| `pr07` | srb_oring | 14.1s | `joint` | 24–35 | 1562–1573 | 0.78 | ✅ 704 |
| `c503` | srb_field_joint | 7.4s | `joint` | 36–47 | 1574–1585 | 1.0 | ✅ 704 |
| `c101` | pad_39b | 8.2s | `pad` | 30–57 | 1174–1201 | 1.0 | ✅ 704 |
| `c709` | commission_testimony | 9.1s | `commission` | 4–9 | **59–64** | 0.55 | ✅ 698 |

⚠️ `c709` の `until` を **元64秒**で切っているのは、**64〜66秒に `ROBERT R…` の名札が大きく読める**
　 から（人物が特定できていない）。**66秒まで伸ばさないこと。**

### 2-2. 静止画で抜く12件（`USE` に入れない。`ref/ep11/fb_<cid>.jpg`）

ショットが2〜6秒しかないのにカットが10〜13秒あり、**動画にすると 0.25〜0.45倍速＝ほぼ静止**
になるものです。**止め絵として抜くほうが素直**で、実写の数は変わりません。

| カット | 欄 | 抜く秒（元） | 中身 | 絵の幅 |
|---|---|---:|---|---|
| `pr01` | ice_icicle | 1119 | 氷に覆われた配管 | ✅ 705 |
| `c105` | ice_trough | 1114 | **水受けにぶら下がる厚い氷** | 🔴 **470×479＝額装パネル** |
| `c107` | ice_icicle_2 | 1128 | 霜の付いた梁の寄り | ✅ 705 |
| `c109` | ice_box | 1123 | 🔴 **氷でふさがった通信箱** | ✅ 705 |
| `c303` | ssme_ignition | 607 | 主エンジンの点火 | ✅ |
| `c501` | srb_stack | 1041 | 積み上げ | ✅ |
| `c506` | oring_physical | 1540 | ゴムの輪の現物 | ✅ 705 |
| `c522` | oring_channel | 1546 | 溝 | ✅ 704 |
| `c710` | commission_hearing_2 | 74 | 公聴会の席 | ✅ |
| `c819` | commission_room | 67 | 青い幕の公聴会場 | ✅ 697 |
| `c911` | commission_hearing | 57 | 机の上のシャトル模型 | ✅ |
| `c912` | commission_members | 69 | **壇上に並ぶ委員** | ✅ 697 |

⚠️ **`pr01` は動画の1カット目**です。⑤cの表では `ice_icicle` に 1119 を当てていますが、
　 台本の言葉は「**発射塔に下がったつらら**」。1133（構造材のつらら）のほうが言葉に合いますが
　 **1133 は額入り（473×479）**です。**⑤c-3 で2コマを並べて決めてください。**

---

## 3. 🔴🔴 当てが付いていない約20件（⑤c-3 の本題）

**2つの型**があります。どちらも「探し方が足りない」のではなく、**置き場に無い**可能性があります。

### 3-1. 報告書の図しか無いもの（11件）

`slot_fill.md` §7 が「**報告書の図版は使えません**」と結論しています。
その図でしか見たことのない主題が、台本に11件あります。

| カット | 欄 | 台本が求めるもの |
|---|---|---|
| `c513` | joint_test | 継ぎ目の試験（すきま 0.74mm / 0.43mm） |
| `c517` | oring_resilience_test | 弾力の試験 |
| `c519` | srb_sun_shade | 日なたと日かげ |
| `c803` | joint_qual_test | 継ぎ目の認証試験 |
| `c804` | srm_horizontal | 横に寝かせた試験 |
| `c810` | srm_nozzle_51b | 1985年のノズル継ぎ目の焼け |
| `ep02` | joint_redesign | 作り直された継ぎ目 |
| `ep03` | joint_test_new | 新しい試験 |
| `ep04` | srm_vertical_test | 立てて燃やす試験 |
| `c606` | oring_soot | 51-C の黒い跡（110度ぶん） |
| `c605` | launch_51c | 1985年1月の打ち上げ |

🔴 **`burn.mpg`（元2494〜2626）を先に当ててください。**⑤cが「`debris` は足りているので予備」
　 として残した帯で、**焼けた継ぎ目・床に並べた残骸・焼け抜けた跡の大きな板**が入っています。
　 §2 の作り方（止め絵で抜く）がそのまま使えます。**全画面が 2497–2580（83秒）と 2596–2622（26秒）**
　 で続いていることは `boxes.json` で測ってあります。
　 ⚠️ ただし **2544 は「試験装置の図と赤い印の並ぶ表」**＝図なので採らない。
　 ⚠️ **2615 の「黄色い丸＋`291°`」は誰も見ていません**（⑤cは 2604 まで）。

### 3-2. 置き場にはあるが **1280px に足りない**もの（9件）

②の網は「幅1280以上」で切っているので、**小さい実物は候補の表に出ていません**。
`commons_ep11.txt` の「小」印の行に実体があります。

| カット | 欄 | 見つかっている実物 | 大きさ |
|---|---|---|---:|
| `c110` | ice_team | `Photograph of Space Shuttle Ice and Frost Inspection - NARA - 593693.gif` | **481×600** |
| `c318` | flame_plume_2 | `STS51L-flame.jpg` ／ `STS51L-58.788sec.jpg` | 714×222 ／ 369×334 |
| `c310` | smoke_puffs | `STS51L-10144 black smoke.jpg` ／ NASA `51l-10096` | 751×523 ／ 要実測 |
| `c715` | telecon_room | `STS-51-L mcc 01.jpg` | 630×450 |
| `ep07` | oring_data_chart | `Defaillance joint Challenger vs temperature.svg` | 388×179（CC0） |
| `ep10` | memorial_wreath | `Memorial of the Challenger.jpg` | 546×714 |
| `c915` | flag_half_mast | 未発見 | — |
| `c905` | srb_inside | 未発見 | — |
| `c403` | hydrogen_burn | 未発見 | — |

🔴 **`ice_team`（c110）は特に効きます。**⑤cが「氷点検チーム（人）は動く映像に1枚も無い」と
　 確かめており、**この 481×600 の1点が唯一の実物**です。
　 ⚠️ **NASA画像庫の原寸を当て直してください**（Commons の版が縮んでいるだけの可能性）。

⚠️ **図に振り替えるのは最大4カットまで**です（写真映像 90/190＝47.4%。下限45%＝85.5カット）。

---

## 4. 当てが付いた約50件（⑤c-3 は**この表の確認から**）

⚠️ **題名だけで採らないこと。**出どころの説明文まで読み、シートで絵を見てから採る
（9本目は「KLMの747」がパンナム機だった）→ 記憶 [[feedback-inventory-is-not-usable-material]]

| カット | 欄 | 当て（Commons の題名／NASA の ID） | 大きさ・年 |
|---|---|---|---|
| `pr03` | accident_breakup | `Challenger explosion.jpg` | 3555×2879 1986 |
| `pr05` | crew_portrait | `Challenger flight 51-l crew.jpg` | 3869×3095 1985 |
| `pr09` | ice_pad | `Ice on the Pad on the Day of STS-51-L's Launch - GPN-2004-00011.jpg` | 2244×2830 1986 |
| `c108` | ice_egress | NASA `51L-10147`（View of ice on the launch complex） | 1986 |
| `c113` | rockwell_orbiter | ⑤bの当て（Columbia の断熱タイル・1979年） | 1528×1187 |
| `c116` | mmt_meeting | `STS-51L riadiace stredisko.jpg` | 3520×2544 1986 |
| `c201` | crew_portrait_2 | `The STS-51L Crew (15871993874).jpg` | 3000×2400 1985 |
| `c206` | crew_mcnair | `Ronald McNair (S78-35300).jpg` | 4146×5183 1978 |
| `c207` | crew_jarvis | `Gregory Jarvis (NASA).jpg` | 6603×8252 1985 |
| `c209` | mcauliffe_training | `Christa McAuliffe in Training (28698549073).jpg` | 3997×2616 1986 |
| `c211` | mcauliffe_morgan | `Christa McAuliffe and Barbara Morgan - GPN-2002-000004.jpg` | 2240×2680 1985 |
| `c212` | training_zero_g | `Zero-G training for crew of 1985 and 1986 space shuttle missions.jpg` | 8224×5709 1985 |
| `c215` | crew_breakfast | `STS-51-L preflight breakfast.jpg` | 4365×2856 1986 |
| `c216` | crew_whiteroom | `51-L Challenger Crew in White Room - GPN-2000-001867.jpg` | 4176×2848 1986 |
| `c301` | launch_pad_morning | `STS-51-L.jpg` ／ NASA `51l-s-154` | 3000×2400 1986 |
| `c315` | ascent_1 | `70mm frame of Challenger during ascent.png` | 4096×4096 1986 |
| `c316` | ascent_2 | `Challenger - GPN-2000-001347.jpg` | 2308×3458 1986 |
| `c317` | flame_plume | `Booster Rocket Breach - GPN-2000-001425.jpg`（**58.778秒の炎**） | 2321×3000 1986 |
| `c320` | et_breach | `LOX Tank Rupture - GPN-2000-001426.jpg` | 3000×2314 1986 |
| `c322` | breakup_moment | `Challenger breakup.jpg` | 1552×2113 1986 |
| `c401` | fireball_wide | `SPACE SHUTTLE CHALLENGER DISASTER 1986 UNCORRECTED COLOR …` | 8172×6320 1986 |
| `c406` | fireball | `Challenger explosion (cropped).jpg` | 3555×2370 1986 |
| `c410` | breakup_sections | `Shuttle Destruction - GPN-2000-001423.jpg` | 2377×1746 1986 |
| `c412` | srb_trails | `Challenger Rocket Booster - GPN-2000-001422.jpg` | 2339×3000 1986 |
| `c705` | oring_erosion_photo | `STS-51-L Recovered Debris (O-Ring Tracks on Right SRB Joint) - GPN-2004-00010` | 2252×2258 1986 |
| `c805` | oring_erosion | `STS-51-L Recovered Debris (Burn Marks on the SRM) - GPN-2004-00004.jpg` | 2307×2281 1986 |
| `c812` | mulloy_testimony | NASA `S86-28749`／`S86-28750`／`S86-28751` | 1986 |
| `c901` | recovery_ship | `STS-51-L Debris Aboard the USGS Cutter Dallas - GPN-2004-00013.jpg` | 2845×3580 1986 |
| `c902` | debris_hangar | `ChallengerRemains.jpg` | 2018×1543 1986 |
| `c903` | srb_burn_hole | `STS-51-L Recovered Debris (Left Solid Rocket Booster) - GPN-2004-00009.jpg` | 2880×2303 1986 |
| `c904` | srb_burn_hole_2 | NASA `51L-10162`（left SRB first piece retrieval） | 1986 |
| `c906` | rudder_burn | `STS-51-L Recovered Debris (Lower Right Vertical Stabilizer) - GPN-2004-00005` | 2311×2297 1986 |
| `c907` | frustum_compare | `STS-51-L Recovered Debris (Forward Skirt) - GPN-2004-00006.jpg` | 2290×2276 1986 |
| `c909` | debris_et | `STS-51-L Recovered Debris (ET and SRBs) - GPN-2004-00003.jpg` | 2291×2288 1986 |
| `c910` | ssme_salvage | `STS-51-L Recovered Debris (SSME Close Up) - GPN-2004-00008.jpg` | 2244×2230 1986 |
| `c913` | memorial_service | `Charles Bolden at STS 51-L Memorial service - 1986.jpg` | 4122×4152 1986 |
| `c914` | reagan_address | `Presidents Speech to The Nation … in Oval Office` | 2713×4000 1986 |
| `ep01` | commission_report | `Rogers-report-front-page.png` | 2576×3320 |
| `ep05` | commission_oversight | NASA `S86-28889`／`s86-28888` | 1986 |
| `ep08` | astronaut_manager | NASA `51L-10166`（委員がKSCに着く） | 1986 |
| `ep09` | safety_panel | `Rogers Commission members arrive at Kennedy Space Center.jpg` | 2840×2231 1986 |
| `ep11` | crew_portrait_3 | `722342main challenger full full.jpg` | 4176×2848 1986 |
| `c313` | past_launch | NASA `51l-s-155`／`156`／`157` | 1986 |

🔴 **乗員の個人肖像が4件、置き場の一覧に出ていません**＝`c202` スコビー・`c203` スミス・
　 `c204` オニヅカ・`c205` レズニック。**`c206` マクネイアと `c207` ジャービスは在ります。**
　 ⚠️ **「無い」と決めないでください。**②の網は幅1280以上で切っており、
　 `Category:STS-51-L crew` のような別のカテゴリを当てていない可能性があります
　 → 記憶 [[feedback-absence-of-a-word-is-not-absence]]。`c208` mcauliffe_class（教室）も同じ。

---

## 5. 関連
- [footage_map.md](footage_map.md)（動く映像の正本）／[slot_fill.md](slot_fill.md)（⑤bの台帳）
- [materials.md](materials.md)（②の置き場の実測）／`commons_ep11.txt`・`nasa_ep11.json`（候補の原簿）
- 道具＝[parse_script.py](parse_script.py)・[sweep_box.py](sweep_box.py)・[make_clips.py](make_clips.py)
- 写す元＝`qa_out/ep10_assets.py`（10本目の写真の束を作った道具）
