# -*- coding: utf-8 -*-
"""第7章　国は知っていた c801–c820（20カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/c8.py`）。
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
    'c801': dict(kind='文字の頁',
               plan='P:c801｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「1991年から2017年まで、危険に気づく機会は何度もあった」｜動き：静止｜見た目の型：P2V1 ¶2.5 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.5（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.5（`In the years between the fire at Knowsley Heights in 1991 and the fire at Grenfell Tower in 2017 there were many opportunities for the government to identify the risks posed by the use of combustible cladding panels and insulation`）'),
    'c802': dict(kind='フリー素材',
               plan='X802｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：ロンドンの議会の建物｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.5（`it failed to heed the warning of the Environment and Transport Select Committee in December 1999 that it should not take a serious fire in which people were killed before steps were taken to minimise the risks posed by some external cladding systems`）'),
    'c803': dict(kind='図解',
               plan='地：X802（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：1999年の委員会の勧め＝外壁は大規模な試験で確かめる・小さな試験の等級はやめる｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src="P2V1¶2.5（`It also failed to implement or keep under review the committee's recommendation that the large-scale test that had recently been developed should be substituted in Approved Document B`）・P2V2¶29.5（`Unfortunately, that warning was ignored`）"),
    'c804': dict(kind='図解',
               plan='地：X802（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：2001年の大規模な試験＝芯がふつうのポリエチレンのアルミ複合板は激しく燃えた・結果は公表されず｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.6（`the striking results of a large-scale test in 2001 involving aluminium composite panels with unmodified polyethylene cores, which burned violently`…`It failed even to publish the results of the test`）'),
    'c805': dict(kind='文字の頁',
               plan='P:c805｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「小さな試験の等級は外壁にふさわしくないと、何度も知らされていた」｜動き：静止｜見た目の型：P2V1 ¶2.7 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.7（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.7（`On many subsequent occasions the department was made aware that national Class 0 was an inappropriate standard by which to determine the suitability of external wall panels but allowed it to remain as part of the statutory guidance until after the Grenfell Tower fire`）'),
    'c806': dict(kind='フリー素材',
               plan='X806｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：ロンドンの古い高層住宅の遠景｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶8.1（`Six people died in the fire, three of whom were children`）・P2V1¶9.41（`On 28 March 2013, the coroner wrote a letter to the`）・P2V1¶2.12（`Following the fire at Lakanal House the coroner recommended that Approved Document B be reviewed`）'),
    'c807': dict(kind='図解',
               plan='地：X806（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：検死官の勧め → 国の省＝急ぐべきこととして扱わない・慢心し、ときに守りに入る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.12（`her recommendations were not treated with any sense of urgency`…`The department displayed a complacent and at times defensive attitude to matters affecting fire safety`）'),
    'c808': dict(kind='文字の頁',
               plan='P:c808｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「命の安全にかかわることまで、無視され、先送りされ、顧みられなかった」｜動き：静止｜見た目の型：P2V1 ¶2.13 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 ¶2.13（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src="P2V1¶2.13（`the government's deregulatory agenda`…`dominated the department's thinking to such an extent that even matters affecting the safety of life were ignored, delayed or disregarded`）"),
    'c809': dict(kind='フリー素材',
               plan='X809｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：夜の高層ビル群の遠景｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.9（`Between 2012 and 2017 the department received numerous warnings about the risks involved in using polymeric insulation and aluminium composite panels with unmodified polyethylene cores`…`It also became aware of several major cladding fires abroad`）'),
    'c810': dict(kind='図解',
               plan='地：X806（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：2016年2月の懸念＝高い建物で、燃える断熱材とアルミ複合板が、規則に反して当たり前に使われている｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.9（`by February 2016 it had become aware that some in the industry were worried that combustible insulation and aluminium composite material (ACM) panels with unmodified polyethylene cores were routinely being used on high-rise buildings in breach of functional requirement B4`）'),
    'c811': dict(kind='フリー素材',
               plan='🔧 X811｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：机の上のノートパソコンと書類｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜注：画面の字は読めない｜新しい画（映像方針）：🔧 模式 → イメージ（ある会社が国の役人に知らせた）＝模式の続きを切る｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶11.71（`none of the existing buildings in the UK over 18 metres in height that were clad in aluminium composite panels currently met functional requirement B4`）'),
    'c812': dict(kind='文字の頁',
               plan='P:c812｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「うわべだけで、急いだ、役に立たない答え」｜動き：静止｜見た目の型：P2V1 ¶11.71 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第1巻 ¶11.71（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶11.71（`superficial, hurried and unhelpful response to a serious question that required careful thought was clearly inadequate`）・P2V1¶2.10（`He failed to bring to the attention of more senior officials the serious risks of which he had become aware`）'),
    'c813': dict(kind='フリー素材',
               plan='X813｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：砂漠の都市の高層ビル群｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶11.77（`the fire at the Address Downtown on 31 December 2015`…`He asked whether similar panels were used in the UK and whether there was a risk of a similar fire occurring in this country`…`The honest response would have been that the risk did exist`…`gave the same response as he had given to`）'),
    'c814': dict(kind='フリー素材',
               plan='🔧 X814｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：役所の机と書類の山｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・社名・字・機種なし）｜出典の行：イメージ（Pexels）｜注：人は写さない｜新しい画（映像方針）：🔧 模式 → イメージ（ひとりの役人に任せた）＝模式の続きを切る｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.10（`It was a serious failure to allow such an important area of activity to remain in the hands of one relatively junior official`）'),
    'c815': dict(kind='図解',
               plan='地：X814（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：国の指針の札＝外壁の防火の指針に根本的な欠陥｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.120（`the statutory guidance on complying with functional requirement B4(1) of the Building Regulations was fundamentally defective`）'),
    'c816': dict(kind='写真',
               plan='🔧 C67｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：団地の奥の焼けた塔〈2017年6月26日〉｜動き：静止｜権利：CC BY 2.0｜時期：2017-06-26 18:11｜人：なし｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：縦＝高さいっぱいの額＋同じ写真のぼかしの地｜新しい画（映像方針）：🔧 [60]（囲いの掲示にデモの人の顔の写真＝11-15 に見た）→ [67]（控え）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V2¶29.21（`only a major fire in a high-rise building leading to a large number of casualties would prompt it to take the necessary action`）'),
    'c817': dict(kind='文字の頁',
               plan='P:c817｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜副題：訳の札「政府は、仕組みの失敗に責任を負わなければならない」｜動き：静止｜見た目の型：P2V2 ¶29.21 の頁｜権利：OGL v3.0｜時期：頁の日付｜人：なし（名前の行は入れない）｜出典の行：グレンフェル・タワー調査 第2段階の報告 第2巻 ¶29.21（2024）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公的な機関の頁（公開調査・政府・区・警視庁ほか）＝額装・無加工・訳の札・出典の行・🔴 名前の行を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V2¶29.21（`The government must take responsibility for the systemic failures that played a significant part in enabling the Grenfell Tower fire to occur`）'),
    'c818': dict(kind='写真',
               plan='🔧 C35｜一覧の種類：写真｜見せ方：全面｜副題：覆いのかかった塔〈2023年5月〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2023-05-24 11:52｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜新しい画（映像方針）：🔧 [58]（ca15 の取り壊しの話へ）→ [35]（c617 と2回）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（第7章のまとめ）'),
    'c819': dict(kind='図解',
               plan='地：C35（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：警告と火事の並び＝1991・1999・2001・2009・2013・2016 の札〈年は札の中〉｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（P2V1 ¶2.5〜¶2.12 と ¶11.71〜¶11.77 の年）'),
    'c820': dict(kind='写真',
               plan='🔧 V15｜一覧の種類：映像｜見せ方：全面｜副題：ロンドンの空撮〈2017年7月公開の映像〉｜動き：映像 132.30〜138.70秒｜見た目の型：240p を11-15に見た｜権利：CC BY 3.0｜時期：2017-07（Vimeo の公開 2017-07-10＝撮影の日は分からない）｜人：なし（人の写る秒は外す＝75〜82.5 歩く人・187.75〜194.75 窓の作業の人）｜出典の行：映像：{作者}／Wikimedia Commons（CC BY 3.0）｜注：川べりの新しい高層住宅（屋根が波の形）・人なし｜新しい画（映像方針）：🔧 副題の時点（Vimeo の公開）・区間＝11-15｜🔴 #15（Commons の映像・CC BY 3.0）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（頭と尻の黒・ビルの広告の幕・歩く人の顔・建物の名の看板・窓の作業の人）に触れない・場面の切れ目をまたがない＝make_list33 の門番｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（第8章へのつなぎ）'),
}

SPEC = {}
