# -*- coding: utf-8 -*-
"""第5章　燃える外壁は、誰が、なぜ選んだのか c601–c630（30カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/c6.py`）。
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
    'c601': dict(kind='図解',
               plan='地：C23（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：年表｜副題：2012〜2014年の札＝2012 亜鉛の案・2013年2月 アルミへ・2013年9月 喫茶店の会合・2014年3月 元｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.73（`eventually an aluminium composite material (ACM), Reynobond 55 PE, was chosen, largely on the grounds of cost`）・P2V1¶2.74（`a series of errors caused by the incompetence of the organisations and individuals involved in the refurbishment`）'),
    'c602': dict(kind='図解',
               plan='地：C23（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：流れ｜副題：関わった会社と組織の札＝管理の組織 TMO・設計 スタジオE・元請け ライドン・外装の下請け ハーレー・板の加工 CEP｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶6.3（`The architect for the main refurbishment was Studio E`…`The cladding subcontractor to Rydon was Harley Facades Ltd`）・P1V1¶6.2（`in June 2014 Rydon Maintenance Limited (Rydon) was eventually appointed the design and build contractor`）・P2V1¶2.21（`Arconic Architectural Products manufactured and sold the Reynobond 55 PE rainscreen panels used in the external wall of Grenfell Tower`）'),
    'c603': dict(kind='写真',
               plan='🔧 C41｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：足場の組まれた塔の上部〈2018年5月〉｜動き：静止｜権利：CC BY-SA 4.0｜時期：2018-05-09 18:44｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 4.0・無加工）｜新しい画（映像方針）：🔧 副題を写っているものに（足場の上部の寄り）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.73（`Although Studio E had wanted to use zinc rainscreen panels`）・P2V4¶55.5（`which was considered by the planning officer present to be acceptable`）'),
    'c604': dict(kind='図解',
               plan='地：C23（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：比べ｜副題：亜鉛の板とアルミの板の札＝節約の見込み 2013年1月 25万ポンド → 2月 30万ポンド〈当時の円で約4,300万円｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.11（`resulting in a potential saving of £250,000`…`costed the saving to be made by using aluminium panels at £300,000`）・換（2013年2月の月平均＝1ポンド 144.08円）'),
    'c605': dict(kind='図解',
               plan='地：C23（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：圧力の札＝管理の組織 TMO → 設計事務所「亜鉛より安い材料を」｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.12（`it was under significant pressure from the TMO to specify a cheaper alternative to zinc`）'),
    'c606': dict(kind='フリー素材',
               plan='🔧 X606｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：昼の喫茶店の机｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜注：店の名・字・人は見せない｜新しい画（映像方針）：🔧 模式 → イメージ（2013年9月の喫茶店の会合）＝模式の続きを切る｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src="P2V4¶55.22（`at a coffee shop in Hays Galleria near London Bridge to discuss options, costs and technical details for the cladding of Grenfell Tower`…`Harley's clients were frequently forced to use ACM because it was the cheapest product available`）"),
    'c607': dict(kind='文字の頁',
               plan='P:c607｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「板の防火の安全は、まったく話されなかった」｜動き：静止｜見た目の型：P2V4 ¶55.23 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第4巻 ¶55.23（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.23（`price and aesthetics were the dominant considerations`…`the fire safety of the panels was not discussed at all`）'),
    'c608': dict(kind='図解',
               plan='地：X606（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：見た目の札が大きく、防火の札が欠けている〈報告の「まるで見なかった」〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.32（`Studio E did not investigate the fire performance of any of the proposed rainscreen panels`）・P2V4¶55.33（`everyone involved concentrated on the appearance of the rainscreen panels to the complete exclusion of their fire performance`）'),
    'c609': dict(kind='写真',
               plan='C39｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：駅から見た塔〈2024年6月〉｜動き：静止｜権利：CC BY-SA 4.0｜時期：2024-06-07 21:44・夕方｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 4.0・無加工）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.28（`Planning permission for the refurbishment`…`on 10 January 2014`…`a requirement that the materials to be used on the external face of the building be approved in writing by RBKC`）'),
    'c610': dict(kind='図解',
               plan='地：X606（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：入札の札＝3社・どれも予算をこえた・入札の途中で1社だけに見通しが伝わる｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.55（`only three tenders had been received and all exceeded the budget as it then stood`）・P2V4¶55.39（`Rydon was given an indication of the likely outcome of the tender process while it was still going on`）'),
    'c611': dict(kind='フリー素材',
               plan='X611｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜の会議室の机と椅子｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.72（`although the TMO had received advice from its lawyers that it would be`…`it entered into discussions with Rydon before the procurement process had been completed`）・P2V4¶55.50（`A meeting took place during the evening of Tuesday 18 March 2014`）・P2V4¶55.51（`We do not know exactly what was discussed at the meeting because no record was kept of it`）'),
    'c612': dict(kind='図解',
               plan='地：X606（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：見積りの誤りの札＝ライドンの入札に約21万2,000ポンドの不足〈当時の円で約3,600万円〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.43（`a shortfall of approximately £212,000 in its costing`）・換（2014年3月の月平均＝1ポンド 170.12円）'),
    'c613': dict(kind='図解',
               plan='地：X606（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：表｜副題：同じ板の削減額の表＝アルミ複合板・リベット留め・2014年3月＝下請け → 元請け 57万6,973ポンド〈約9,800｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.48（`£576,973`）・換（2014年3月の月平均＝1ポンド 170.12円）'),
    'c614': dict(kind='図解',
               plan='地：X606（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：差の札＝下請けが示した約58万ポンドと、元請けが管理の組織に示した約38万ポンド・差の約20万ポンドで見積りの不足を埋め｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.58（`£376,175`）・P2V4¶55.59（`Those figures were all lower than those that Harley had given Rydon on 14 March 2014`…`the purpose was to enable Rydon to retain the difference in order to make up the shortfall caused by the £212,000 error in costing`）'),
    'c615': dict(kind='文字の頁',
               plan='P:c615｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「議事録がうかがわせるように、この額がハーレーから得られる削減のすべてだと伝わったなら、明らかに偽りで、ライドンは偽りと知っていた」｜動き：静止｜見た目の型：P2V4 ¶55.72 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第4巻 ¶55.72（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.72（`the TMO was told that there was a potential saving of up to £376,175`…`if, as the minutes tend to suggest, the TMO was given to understand that the sum of £376,175 reflected the full amount of the reduction available from Harley, that was clearly false and was known by Rydon to be false`）'),
    'c616': dict(kind='図解',
               plan='地：X606（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：元請けの利益の札＝アルミ複合板を勧めると利益が増える・管理の組織は知らされていない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src="P2V4¶55.72（`Rydon did not tell the TMO that Harley was willing to reduce the cost of the rainscreen by as much as`）・P2V4¶55.60（`The TMO was kept entirely in the dark about Rydon's financial interest in recommending ACM`）"),
    'c617': dict(kind='写真',
               plan='C35｜一覧の種類：写真｜見せ方：全面｜副題：覆いのかかった塔〈2023年5月〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2023-05-24 11:52｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.71（`From March 2014 onwards`…`the only product that was proposed for use was Reynobond 55 PE ACM panels`）'),
    'c618': dict(kind='図解',
               plan='地：C35（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：燃えにくい芯の板もあった・下請けは認めた以上に知っていた｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.24（`Arconic did not consider withdrawing Reynobond 55 PE in favour of the fire-resistant version then available`）・P2V4¶55.83（`Harley knew more than it was willing to admit about the availability of a fire-resistant version of the Reynobond panel`）'),
    'c619': dict(kind='図・写真の頁',
               plan='🔧 F:P1V1-6.1｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：改修のあとの外壁｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第1巻 図6.1（2019）｜新しい画（映像方針）：🔧 模式 → 図6.1（区が色も含めて許可した外壁＝改修のあと・c210 と2回）＝模式の続きを切る｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.74（`The appearance and cost of the cladding, together with concerns about the programme, were the only matters considered by the council`）・P2V4¶55.77（`the planning department had approved ACM rainscreen cladding using cassette fixings`…`for those panels in "smoke silver" on 25 September 2014`）'),
    'c620': dict(kind='写真',
               plan='🔧 C64｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：木の奥の焼けた塔〈2017年6月26日〉｜動き：静止｜権利：CC BY 2.0｜時期：2017-06-26 18:12｜人：なし（右下に小さな重機）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：縦＝高さいっぱいの額＋同じ写真のぼかしの地｜新しい画（映像方針）：🔧 図6.8（窓の上の内側の写真＝語りの「認証の書類」と合わない）→ [64]（縦）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.14（`stated (wrongly) that the panels might be regarded as having a Class 0 surface`）・P2V4¶55.61（`Astonishingly, at no stage of the project did anyone at Rydon, Harley or Studio E examine the certificate with any care`）'),
    'c621': dict(kind='図解',
               plan='地：C64（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：前ぶれの札＝2012年1月 ロンドンの別の高層住宅の火事・下請けはアルミ複合板が燃えると知った｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.79（`16 January 2012 at Taplow House on the Chalcots Estate`）・P2V4¶55.80（`the fire at Taplow House had demonstrated to Harley that ACM would burn`）'),
    'c622': dict(kind='文字の頁',
               plan='P:c622｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「火事になれば、アルミ複合板は、すぐに無くなる！」｜動き：静止｜見た目の型：P2V4 ¶55.84 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第4巻 ¶55.84（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.84（`the ACM will be gone rather quickly in a fire!`）'),
    'c623': dict(kind='図解',
               plan='地：C64（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：2014年11月の問いの札＝管理の組織の担当者が、ラカナル・ハウスの火事を引いて「材料は燃えにくい必要があるか」と尋ねる｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.87（`whether in the light of the fire at Lakanal House there was any requirement for materials to be flame retardant`）・P2V4¶55.89（`no one in the design team gave any consideration to the question she had raised, despite the fact that it was of real importance`）'),
    'c624': dict(kind='フリー素材',
               plan='X624｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：ビルの外壁の工事と足場｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.73（`largely on the grounds of cost`）'),
    'c625': dict(kind='文字の頁',
               plan='P:c625｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「関わった組織と人の力不足による、いくつもの誤りの結果」｜動き：静止｜見た目の型：P2V1 ¶2.74 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.74（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.74（`The choice of combustible materials for the cladding of Grenfell Tower resulted from a series of errors caused by the incompetence of the organisations and individuals involved in the refurbishment`）'),
    'c626': dict(kind='図解',
               plan='地：X624（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：責任のたらい回しの札＝それぞれが、防火は誰かほかの人の責任と思う・防火の技術者に材料のことを尋ねた人はいない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.74（`in each case assumed that someone else was responsible for matters affecting fire safety`）・P2V4¶67.14（`no one asked for advice or confirmation from a fire engineer`）'),
    'c627': dict(kind='文字の頁',
               plan='P:c627｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「その悲惨な選択の責任を、TMO に負わせることはできない」｜動き：静止｜見た目の型：P2V4 ¶67.21 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第4巻 ¶67.21（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶67.21（`the TMO was unduly concerned with reducing costs`…`The decision to choose Reynobond PE was part of a "value engineering" exercise performed at the TMO\'s insistence and designed to keep costs down`…`cannot be laid at the door of the TMO`）'),
    'c628': dict(kind='図解',
               plan='地：X624（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：報告の67章の札＝多くの関係者の深刻な力不足・一部の建材の製造会社の明らかな不正｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶67.13（`a serious lack of competence on the part of many of those engaged on it and, in the case of some manufacturers of construction products, outright dishonesty`）'),
    'c629': dict(kind='図・写真の頁',
               plan='F:P1V1-6.7｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：窓のまわりの断熱材〈報告の図〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第1巻 図6.7（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（3つ目の問いの前半の答え）'),
    'c630': dict(kind='図・写真の頁',
               plan='F:P2V1-5.9｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：外壁の燃焼試験〈報告の図〉｜動き：静止｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：報告の図｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 図5.9（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.19（`One very significant reason why Grenfell Tower came to be clad in combustible materials was systematic dishonesty on the part of those who made and sold the rainscreen cladding panels and insulation products`）'),
}

SPEC = {}
