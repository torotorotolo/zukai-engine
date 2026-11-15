# -*- coding: utf-8 -*-
"""第1章　ロンドンの24階建ての塔 c201–c217（17カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/c2.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep33/make_plan33.py` で
  映像方針の一覧（`ref/ep33/eizou_build/make_list33.py`＝了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep33/eizou_list33.md`＝⑤b は一覧に従う）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。公的な機関の頁（訳の札つき）は最初から「文字の頁」。
  🔴 額装・帯の写真は静止（`build_jiko.FRAME_STILL_EP` に ep33）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。
  🔴 写真は画面いっぱい・色は原本（`build_jiko.PHOTO_KEEP_EP` に ep33）・BY-SA は額装・報告の図と頁も額装。説明カットの地は昼の写真を暗くするだけ（8:1・衛星・夜・BY-SA は地にしない）。
  🔴 #15（Commons の映像）は等速・止めなし・頭から使う・同じ秒を2回使わない・場面の切れ目をまたがない（区間は一覧の動きの欄＝make_list33 の門番）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針（と ⑤b-1 の c526）で台本の画の欄から替えたカット。
  🔴 この回の線＝住民（亡くなった人・生き残った人・出火した部屋の住人）は名前なし（人数だけ）・消防士と指揮者は立場・調査の委員長と大臣と区の幹部は役職・
     会社と団体は報告が名指しした結論の範囲で名前・社員と専門家は役職・刑事は警視庁の発表の数と日付だけ・「見捨てた」「英国史上最悪」「60時間」は使わない・
     追悼の場と支援の掲示は使わない＝図でも同じ（報告の図・頁・写真に名前の字が写る＝親が絵を見て切る）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c201': dict(kind='写真',
               plan='🔧 V15｜一覧の種類：映像｜見せ方：全面｜副題：ロンドンの空撮〈2017年7月公開の映像〉｜動き：映像 21.03〜28.28秒｜見た目の型：240p を11-15に見た｜権利：CC BY 3.0｜時期：2017-07（Vimeo の公開 2017-07-10＝撮影の日は分からない）｜人：なし（人の写る秒は外す＝75〜82.5 歩く人・187.75〜194.75 窓の作業の人）｜出典の行：映像：{作者}／Wikimedia Commons（CC BY 3.0）｜注：住宅地の上の空撮（地平に高いビル）＝場所は言わない・人なし｜新しい画（映像方針）：🔧 副題の時点（Vimeo の公開）・区間＝11-15（台本の「川と高いビル」は都心＝語りの「ロンドンの西」と合わない＝住宅地の空撮に）・⑤b-1（11-15）＝28.327秒が硬いカット（次は公園の場面）＝実測 7.22秒が収まるよう頭を 21.30→21.03 へ（場面 20.967〜28.327）｜🔴 #15（Commons の映像・CC BY 3.0）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（頭と尻の黒・ビルの広告の幕・歩く人の顔・建物の名の看板・窓の作業の人）に触れない・場面の切れ目をまたがない＝make_list33 の門番｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶3.1（`It is located in the Lancaster West Estate in North Kensington, London W11`）'),
    'c202': dict(kind='図解',
               plan='SAT:ランカスター・ウェスト団地｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：塔のある団地〈現在の衛星写真〉｜動き：静止｜権利：Google｜時期：撮影の時点は ⑤b で｜人：なし｜出典の行：Google の表示（絵のそば）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・撮影の時点は副題に書かない・帰属は地図の右下・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src="P1V1¶3.2（`The walkways extend 150 metres south from the tower and enclose two green spaces`）・P1V1¶3.4（`approximately 200 metres' walking distance from the entrance to the tower`）"),
    'c203': dict(kind='図・写真の頁',
               plan='F:P1V1-3.2｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：改修の前の外壁｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第1巻 図3.2（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶3.1（`building work commenced in 1972 and was completed by 1974`）・P1V1¶3.9（`just over 67 metres tall and has 25 storeys, including a basement and ground floor to floor 23`…`central reinforced concrete core, reinforced concrete floors and perimeter reinforced concrete columns`）'),
    'c204': dict(kind='図解',
               plan='地：C32（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：立面｜副題：塔の階の札＝地上の階を0階・住戸は主に4階から23階・下の階には保育園などと、改修で足した9戸｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶3.13（`Floors 4 to 23 were designed to accommodate residential flats, with six flats on each floor`）'),
    'c205': dict(kind='図解',
               plan='地：C32（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：1つの階の間取り＝真ん中に階段1つとエレベーター2基・まわりに6つの住戸｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶3.18（`Within the central core of the building was a single staircase and two lifts serving each floor of the tower`）'),
    'c206': dict(kind='図・写真の頁',
               plan='F:P1V2-10.5｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：塔の入口｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.5（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶3.2（`the only access to the tower for residents was through the entrance at ground level on the south side`）'),
    'c207': dict(kind='写真',
               plan='C61｜一覧の種類：写真｜見せ方：全面｜副題：塔と隣の建物〈2017年6月26日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-26 18:20｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V2¶10.130（`people in 129 flats in the tower, including visitors`…`Seven flats were empty on that night`…`Sixty-seven of those present were children under the age of 18`）'),
    'c208': dict(kind='図解',
               plan='地：C61（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：持ち主と管理の札＝ケンジントン・アンド・チェルシー区 → 管理の組織 TMO → 住人｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src="P1V1¶3.1（`Grenfell Tower is owned by RBKC`）・P1V1¶3.6（`The vast majority of the residential flats in the tower were part of RBKC's provision of social housing within the borough`）・P1V1¶3.8（`RBKC entered into a Management Agreement with the TMO`）"),
    'c209': dict(kind='写真',
               plan='C29｜一覧の種類：写真｜見せ方：全面｜副題：焼けた塔〈2017年6月17日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-17 08:06・朝｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶3.7（`Some had grown up in North Kensington`…`Others had come to this country as refugees`…`Together they formed a vibrant community with a strong sense of identity and considerable social cohesion`）'),
    'c210': dict(kind='図・写真の頁',
               plan='F:P1V1-6.1｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：改修のあとの外壁｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第1巻 図6.1（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶6.1（`the refurbishment carried out between 2012 and 2016`…`the over-cladding of every storey of the existing building with a new insulation and rainscreen cladding system`）'),
    'c211': dict(kind='図解',
               plan='地：C29（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：断面｜副題：外壁の断面＝外から外装の板〈アルミ複合板〉・すき間・断熱材・元のコンクリートの壁の順｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶6.7（`At floors 4 to 23 they comprised insulation materials, new windows, new window infill panels and outer aluminium composite material (ACM) rainscreen panels`）'),
    'c212': dict(kind='図解',
               plan='地：C29（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：アルミ複合板の断面＝2枚の薄いアルミの板と、あいだのポリエチレン｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.21（`They were an ACM product made of two thin sheets of aluminium with a polyethylene core`…`Polyethylene burns fiercely`）'),
    'c213': dict(kind='図・写真の頁',
               plan='F:P1V1-6.11｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：屋上の飾りの設計図｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第1巻 図6.11（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶6.35（`The fins and the associated structure at the crown had no functional purpose and were purely aesthetic`）'),
    'c214': dict(kind='写真',
               plan='C71｜一覧の種類：写真｜見せ方：全面｜副題：焼けた塔の上部〈2017年6月20日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-20 16:38｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶6.4（`The Department of Building Control at RBKC acted as building control authority`…`The Building Certificate for completion of the works was signed by RBKC on 7 July 2016`）・計（2016-07-07 から 2017-06-14 まで＝11か月）'),
    'c215': dict(kind='写真',
               plan='C55｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：焼けた塔〈2017年6月16日〉｜動き：静止｜権利：CC BY 2.0｜時期：2017-06-16 15:16｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.16（`they did not adequately resist the spread of fire having regard to the height, use and position of the building`…`On the contrary, they actively promoted it`）'),
    'c216': dict(kind='写真',
               plan='C62｜一覧の種類：写真｜見せ方：全面｜副題：焼けた塔〈2017年6月26日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-26 18:17｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（第5章へのつなぎ）'),
    'c217': dict(kind='写真',
               plan='C19｜一覧の種類：写真｜見せ方：全面｜副題：焼けた塔とクレーン〈2017年6月20日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-20 16:27｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.10（`organised into 11 separate periods between 00.54`…`when the last survivor left the tower`）'),
}

SPEC = {}

# 🆕 ⑤b-2（2026-11-15）：#15 の欄だけ先に書いた（USE と章ファイルを両側から照らす門番 check_footage_slots のため）。ほかのカットは ⑤b-3 以降
#   c201＝住宅地の空撮（場面 20.967〜28.327＝硬いカットの内・頭 21.03秒・等速・読む 7.22秒〈〜28.25〉・ゆとり 0.03秒＝焼いたら頭と尻のコマを見る）
SPEC.update({
    "c201": ss.vid("c201", t="塔のある団地", s="ロンドンの空撮〈2017年7月公開の映像〉"),
})
