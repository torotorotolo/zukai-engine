# -*- coding: utf-8 -*-
"""第10章　9年たっても出ない答え cb01–cb17（17カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/cb.py`）。
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
    'cb01': dict(kind='文字の頁',
               plan='P:cb01｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「すべての書類を検察へ」｜動き：静止｜見た目の型：警1｜権利：引用（頭の1文だけ・罪名と名前を入れない）｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：ロンドン警視庁の発表（2026年9月30日）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='警1（`The Met has now submitted all files to the Crown Prosecution Service to allow them to make charging decisions in relation to the Grenfell Tower fire`）'),
    'cb02': dict(kind='図解',
               plan='地：Xa13（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：容疑の数の札＝2024年 19の会社や団体と58人・名前は出さない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='警3（`Identified and are investigating 19 companies or organisations and 58 individuals, as suspects`）'),
    'cb03': dict(kind='フリー素材',
               plan='Xb03｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：積み上げた書類の箱｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='警3（`Interviewed under caution over 50 suspects for a total of more than 300 hours`）'),
    'cb04': dict(kind='図解',
               plan='地：Xb03（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：警視庁の見込みの札＝2024年5月の時点で、報告を読みこみ書類を仕上げるのは、少なくとも2025年の終わりまで｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src="警3（`at least until the end of 2025 to fully assess the public inquiry's phase 2 report and finalise evidential files`）"),
    'cb05': dict(kind='図解',
               plan='地：Xb03（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：調べた範囲の札＝1万5,000人と700の組織・容疑者は20の会社や団体と57人〈2026年5月〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='警2（`The role of 15,000 individuals and 700 organisations have been examined of which 57 people and 20 organisations are suspects for criminal offences`）'),
    'cb06': dict(kind='文字の頁',
               plan='P:cb06｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「20の会社と団体、54人」｜動き：静止｜見た目の型：警1｜権利：引用（頭の1文だけ・罪名と名前を入れない）｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：ロンドン警視庁の発表（2026年9月30日）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='警1（`The 20 files relate to 20 companies and organisations and 54 individuals`）'),
    'cb07': dict(kind='フリー素材',
               plan='Xb07｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：棚に並んだ書類のファイル｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='警1（`As well as the 20 files, the submission to the CPS also includes 14 overarching evidence files`）'),
    'cb08': dict(kind='図解',
               plan='地：Xb07（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：誰が決めるかの札＝警視庁は証拠の書類を送る → 起訴するかを決めるのは検察｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='警1（`to allow them to make charging decisions in relation to the Grenfell Tower fire`）'),
    'cb09': dict(kind='図解',
               plan='地：Xb07（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：暦｜副題：2027年6月の札＝火事から10年・それより前に起訴するかを決める約束｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='警1（`The CPS has committed to making the charging decisions before the 10th anniversary of the fire in June 2027`）'),
    'cb10': dict(kind='図解',
               plan='地：Xb07（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：名前を出さない札＝警視庁の発表に容疑者の名は無い・この動画も、容疑の対象の会社や人を言わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（この回の線）'),
    'cb11': dict(kind='フリー素材',
               plan='Xb11｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜明けの空と街の遠景｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='警1（`has had a significant impact on those waiting for answers`…`it has necessarily taken this long to ensure our investigation is meticulous`）'),
    'cb12': dict(kind='図解',
               plan='SAT:取り壊し中の塔｜一覧の種類：衛星｜見せ方：額装（衛星）｜副題：塔のあたり〈衛星写真〉｜動き：静止｜権利：Google｜時期：撮影の時点は ⑤b で｜人：なし｜出典の行：Google の表示（絵のそば）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 Google の衛星写真＝描き足しは公の場所だけ・撮影の時点は副題に書かない・帰属は地図の右下・🔴 説明カットの地にしない（暗くしない）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（2017-06-14 から 2026-11 まで＝9年5か月）'),
    'cb13': dict(kind='文字の頁',
               plan='P:cb13｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「2009年の火事が予告した欠けが、2017年6月14日の夜に、ふたたび現れた」｜動き：静止｜見た目の型：P2V5 ¶83.13 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第5巻 ¶83.13（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V5¶83.13（`the Lakanal House fire in July 2009 forewarned the LFB about the existence of the shortcomings which revealed themselves once more on the night of 14 June 2017`）'),
    'cb14': dict(kind='フリー素材',
               plan='🔧 X802｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：ロンドンの議会の建物｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜新しい画（映像方針）：🔧 模式 → イメージ（1999年の議会の委員会・c802 と同じ絵）＝模式の続きを切る｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V2¶29.5（`it should not take a serious fire in which people were killed before steps were taken to minimise the risks posed by some external cladding systems`…`Unfortunately, that warning was ignored`）'),
    'cb15': dict(kind='図解',
               plan='地：X802（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：「部屋で待て」の答えの札＝改めるべき時は1時30分から1時50分・取りやめは2時47分・欠けは備えと訓練と指揮｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.6（`That point had been reached by 01.30 at the earliest and by 01.50 at the latest`）'),
    'cb16': dict(kind='図解',
               plan='地：X802（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：まだ出ていない答えの札＝罪に問われるか〈2027年6月より前〉・勧告の残り〈2029年の終わりまで〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（2026年11月の時点）'),
    'cb17': dict(kind='写真',
               plan='🔧 V15｜一覧の種類：映像｜見せ方：全面｜副題：ロンドンの空撮〈2017年7月公開の映像〉｜動き：映像 125.30〜131.70秒｜見た目の型：240p を11-15に見た｜権利：CC BY 3.0｜時期：2017-07（Vimeo の公開 2017-07-10＝撮影の日は分からない）｜人：なし（人の写る秒は外す＝75〜82.5 歩く人・187.75〜194.75 窓の作業の人）｜出典の行：映像：{作者}／Wikimedia Commons（CC BY 3.0）｜注：高層住宅の並び・人なし｜新しい画（映像方針）：🔧 副題の時点（Vimeo の公開）・区間＝11-15｜🔴 #15（Commons の映像・CC BY 3.0）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（頭と尻の黒・ビルの広告の幕・歩く人の顔・建物の名の看板・窓の作業の人）に触れない・場面の切れ目をまたがない＝make_list33 の門番｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（第11章へのつなぎ）'),
}

SPEC = {}

# 🆕 ⑤b-2（2026-11-15）：#15 の欄だけ先に書いた（USE と章ファイルを両側から照らす門番 check_footage_slots のため）。ほかのカットは ⑤b-3 以降
#   cb17＝高層住宅の空撮（場面 125.087〜132.127 の内・建物の名の看板の場面〈118.207〜125.087〉の外・等速・読む 4.89秒〈125.30〜130.19〉）
SPEC.update({
    "cb17": ss.vid("cb17", t="日本の高い建物", s="ロンドンの空撮〈2017年7月公開の映像〉"),
})
