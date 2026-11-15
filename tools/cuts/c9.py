# -*- coding: utf-8 -*-
"""第8章　よく言われる話を、報告に当てる c901–c913（13カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/c9.py`）。
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
    'c901': dict(kind='図解',
               plan='地：C35（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：「よく言われる話 → 報告」の札の型〈事実の図と見た目を分ける〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（第8章の型）'),
    'c902': dict(kind='文字の頁',
               plan='P:c902｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「外壁は、規則の求めを満たしていなかった」｜動き：静止｜見た目の型：P2V4 ¶63.10 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第4巻 ¶63.10（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶63.10（`As a consequence, the external wall did not comply with functional requirement B4(1)`）・P1V4¶26.4（`there is compelling evidence that requirement B4(1) was not met in this case`）'),
    'c903': dict(kind='図解',
               plan='地：C35（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：2つの札＝外壁は規則の求めを満たさない・国の指針そのものにも根本的な欠陥｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.120（`was fundamentally defective`）'),
    'c904': dict(kind='フリー素材',
               plan='X904｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：建物の中のガスの管｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶34.15（`Although the supply of gas allowed fires within individual flats to continue to burn until it was shut off at 23.40 that day, its contribution to the fire which consumed the tower appears to have been minimal`）'),
    'c905': dict(kind='図解',
               plan='地：X904（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：火を大きくしたものの札＝外壁の板の芯〈いちばん〉・断熱材・ガス〈ごく小さい〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.13（`The principal reason why the flames spread so rapidly`）'),
    'c906': dict(kind='フリー素材',
               plan='X906｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：パソコンの画面のブログ｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V3¶42.41（`On 20 November 2016`…`posted an article on the Grenfell Action Group blog`…`he criticised the TMO for failing to take fire safety seriously`）'),
    'c907': dict(kind='文字の頁',
               plan='P:c907｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「火事を予言してはいなかった。だが、聞き流してはいけない知らせだった」｜動き：静止｜見た目の型：P2V3 ¶42.42 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第3巻 ¶42.42（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V3¶42.42（`it did not in fact predict the fire at Grenfell Tower, much less what turned out to be its cause`…`it was a message that the TMO could not afford to ignore`）'),
    'c908': dict(kind='図解',
               plan='🔧 地：C20（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：報告の認めたことの札〈文字は小さく・人は描かない〉｜新しい画（映像方針）：🔧 地＝[20]（覆われた塔と緑のハート＝台本どおり・亡くなった人の話に直前のガスの管のイメージは合わない）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.102（`all those whose bodies were destroyed by the fire were dead or unconscious when the fire reached them`）'),
    'c909': dict(kind='文字の頁',
               plan='P:c909｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「第1段階では調べていない」｜動き：静止｜見た目の型：P1ES ¶33.26 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第1段階の報告 要約 ¶33.26（2019）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶33.26（`whether such a system would be likely to have suppressed the fire in Flat 16 or prevented it from escaping into the cladding before the firefighters could extinguish it is not something that was investigated in Phase 1`）'),
    'c910': dict(kind='写真',
               plan="🔧 C25｜一覧の種類：写真｜見せ方：全面｜副題：足場の組まれた塔〈2018年1月〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2018-01-05 12:20｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：白黒の原本＝色は原本のまま｜新しい画（映像方針）：🔧 模式 → [25]（第8章の実写が文字の頁だけ＝Commons の全画面を1つ・④' の宿題）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）",
               src='計（この動画の書き方）'),
    'c911': dict(kind='図解',
               plan='地：C25（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：「安さで選んだ」の札＝費用は主な理由・根にあったのは力不足が生んだ誤りの重なり｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.73（`largely on the grounds of cost`）・P2V1¶2.74（`a series of errors caused by the incompetence of the organisations and individuals involved in the refurbishment`）'),
    'c912': dict(kind='写真',
               plan='🔧 C40｜一覧の種類：写真｜見せ方：全面｜副題：消防の車と焼けた塔〈2017年6月18日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-18 13:14｜人：消防の車（人は小さく遠い＝⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜新しい画（映像方針）：🔧 模式 → [40]（消防の対応の話・c110 と2回）＝模式の続きを切る｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.91（`chronic lack of effective management and leadership`）・P1V4¶28.8（`the principal failure was one of command`）・P1ES¶2.18（`LFB incident commanders had received no training in how to recognise the need for an evacuation or how to organise one`）・P1V4¶28.1（`displayed enormous courage and selfless devotion to duty`）'),
    'c913': dict(kind='フリー素材',
               plan='X913｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夕暮れのロンドンの街並み｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（第9章へのつなぎ）'),
}

SPEC = {}
