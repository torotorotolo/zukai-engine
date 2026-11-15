# -*- coding: utf-8 -*-
"""冒頭 c101–c113（13カット）。33本目（グレンフェルタワー火災・2017-06-14・ロンドン・公開調査の報告は 2019-10-30〈第1段階〉と 2024-09-04〈第2段階〉）。

■ 🔴 2026-11-15（⑤b-1）：32本目（USエアウェイズ1549便のハドソン川への着水）の中身を空にした＝git の `139227a3`（`git show 139227a3:tools/cuts/c1.py`）。
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
    'c101': dict(kind='写真',
               plan='🔧 F:P1V2-10.9｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：台所の窓から外へ出た炎〈1:09〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:09｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.9（2019）｜注：焼き込みの時刻 01:09:31・01:09:36・高さいっぱいの額＋同じ紙面のぼかしの地 ［冒頭］｜新しい画（映像方針）：🔧 図22.8（粗い寄り）→ 図10.9（01:09:31・01:09:36 の2コマ＝炎が大きく明るい・本文の「01.05、01.06、01.08、01.09」の最後）＝22.8 は c310 へ｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`Fire breaks out of Flat 16 into exterior cladding and starts to climb the east facade rapidly`）'),
    'c102': dict(kind='写真',
               plan='F:P1V2-10.14｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：外壁を上る炎〈1:19〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:19｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.14（2019）｜注：焼き込みの時刻 01:19:04（本文 ¶10.73 の stills at 01.19.04）・2コマのあいだは黒 ［冒頭］｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.12（`The fire had entered the cladding before firefighters opened the kitchen door in Flat 16 for the first time at 01.14`）'),
    'c103': dict(kind='写真',
               plan='F:P1V2-10.22｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：屋上に届いた炎〈1:27ごろ〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 01:27｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図10.22（2019）｜注：本文 ¶10.119（after 01.27.42 の冠の炎）・札 L23 と Parapet/crown は図の札（紙面のまま） ［冒頭］｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V4¶28.14（`very top of the building by 01.26, i.e. in under 20 minutes`）・P1ES¶2.11（`Fire reaches the roof and starts to spread horizontally`）'),
    'c104': dict(kind='写真',
               plan='F:P1V2-14.1｜一覧の種類：紙面｜見せ方：額装（高さいっぱい）｜副題：警察のヘリコプターから〈2:06〉｜動き：静止｜見た目の型：図を11-14に見た｜権利：OGL v3.0（第三者のコマ・図を含む）｜時期：2017-06-14 02:06｜人：なし（⑤b で原寸）｜出典の行：グレンフェル・タワー調査 第1段階の報告 第2巻 図14.1（2019）｜注：警視庁のヘリのコマ（本文の 02.06）・警察の印と焼き込みの字は紙面のまま ［冒頭］｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 公開調査の報告の図＝額装・無加工・図の番号と題の行ごと切る・出典の行・第三者のコマや図を含む（OGL v3.0 の外の部分）＝報告の図として引用の形・🔴 名前の字を入れない＝親が絵を見て切る｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.13（`The principal reason why the flames spread so rapidly up, down and around the building was the presence of the aluminium composite material (ACM) rainscreen panels with polyethylene cores, which acted as a source of fuel`）'),
    'c105': dict(kind='写真',
               plan='C7｜一覧の種類：写真｜見せ方：全面｜副題：燃える塔〈2017年6月14日の夜明け〉｜動き：ゆっくり寄る｜見た目の型：原寸を11-15に見た｜権利：CC BY 4.0｜時期：2017-06-14・夜明け｜人：なし（11-15 に見た＝はしご車の放水・人は写らない）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 4.0・改変：切出）｜注：夜明けの空（11-15 に見た）・引きの終わり 43.7秒（46秒まで 2.3秒）・4:3 を 16:9 に切る＝改変：切出（CC BY 4.0）・「夜明け」は取得のあと原寸で確かめる ［冒頭］｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V4¶55.33（`everyone involved concentrated on the appearance of the rainscreen panels to the complete exclusion of their fire performance`）'),
    'c106': dict(kind='写真',
               plan='🔧 C12｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：煙を上げる塔〈2017年6月14日〉｜動き：静止｜権利：CC BY 4.0｜時期：2017-06-14・夜明け｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 4.0）｜注：縦＝高さいっぱいの額＋同じ写真のぼかしの地 ［冒頭］｜新しい画（映像方針）：🔧 副題を約20字に（夜明けは c105 の副題と絵で分かる）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1ES¶2.11（`the fire starts to spread to the north elevation of the tower`…`Flames start to spread to south elevation`…`Fire starts to spread across the west elevation of tower`）・P1ES¶2.13（`enveloping the entire building in under three hours`）・警1（`took the lives of 72 people`）'),
    'c107': dict(kind='写真',
               plan='🔧 C3｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：空を流れる煙〈2017年6月14日の朝〉｜動き：静止｜権利：CC BY-SA 4.0｜時期：2017-06-14 04:51（題）・夜明け・朝｜人：なし（遠景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 4.0・無加工）｜注：BY-SA＝額装・無加工・丸ごと（2:1）＋同じ写真のぼかしの地・題の時刻 4:51 ［冒頭］｜新しい画（映像方針）：🔧 副題を約20字に｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V7¶98.1（`The Grenfell Tower fire was one of the worst post-war civil disasters in the UK`）'),
    'c108': dict(kind='写真',
               plan='C8｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：朝の塔と放水〈2017年6月14日〉｜動き：静止｜権利：CC BY 4.0｜時期：2017-06-14・朝｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 4.0）｜注：縦＝高さいっぱいの額＋同じ写真のぼかしの地 ［冒頭］｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶4.3（`the occupants are advised to remain within their own flats unless they are directly affected by fire, heat or smoke`）・P1V4¶28.6（`the best part of an hour had been lost without any evacuation plan having been considered`）'),
    'c109': dict(kind='写真',
               plan='🔧 V15｜一覧の種類：映像｜見せ方：全面｜副題：焼けた塔〈2017年7月公開の映像〉｜動き：映像 176.30〜187.45秒｜見た目の型：240p を11-15に見た｜権利：CC BY 3.0｜時期：2017-07（Vimeo の公開 2017-07-10＝撮影の日は分からない）｜人：なし（人の写る秒は外す＝75〜82.5 歩く人・187.75〜194.75 窓の作業の人）｜出典の行：映像：{作者}／Wikimedia Commons（CC BY 3.0）｜注：T1 遠くの塔（176.0〜182.25・止まった絵）→ T2 外壁の寄り（182.25〜187.75）＝区間の中で場面が1回替わる・人なし ［冒頭］｜新しい画（映像方針）：🔧 副題の時点＝Commons の日付は Vimeo の公開（2017-07-10）＝撮影の日は分からない・区間＝11-15｜🔴 #15（Commons の映像・CC BY 3.0）＝等速・止めなし・頭から使う・同じ秒を2回使わない・音は使わない（-an）・外す秒（頭と尻の黒・ビルの広告の幕・歩く人の顔・建物の名の看板・窓の作業の人）に触れない・場面の切れ目をまたがない＝make_list33 の門番｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（この動画の問い）'),
    'c110': dict(kind='写真',
               plan='C40｜一覧の種類：写真｜見せ方：全面｜副題：消防の車と焼けた塔〈2017年6月18日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-18 13:14｜人：消防の車（人は小さく遠い＝⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：消防の車（人は小さく遠い） ［冒頭］｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（この動画の問い）'),
    'c111': dict(kind='写真',
               plan='🔧 C28｜一覧の種類：写真｜見せ方：全面｜副題：青空の下の焼けた塔〈2017年6月16日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-16 14:34｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：［冒頭］｜新しい画（映像方針）：🔧 副題を写っているものに（[55] と書き分け）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='計（報告の PDF＝12冊・2,582頁＝第1段階 2019-10-30 の要約と4巻・第2段階 2024-09-04 の7巻・火事から第2段階の報告まで＝7年3か月）'),
    'c112': dict(kind='写真',
               plan='🔧 C70｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：下の階が白い塔〈2017年6月20日〉｜動き：静止｜権利：CC BY 2.0｜時期：2017-06-20 16:31｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：縦＝高さいっぱいの額 ［冒頭］｜新しい画（映像方針）：🔧 副題を写っているものに（[69] と書き分け＝火は4階から上）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（#15 も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P2V1¶2.4（`the fire at Grenfell Tower was the culmination of decades of failure by central government and other bodies in positions of responsibility in the construction industry`）'),
    'c113': dict(kind='写真',
               plan='C32｜一覧の種類：写真｜見せ方：全面｜副題：家並みの奥の塔〈2017年6月20日〉｜動き：ゆっくり寄る｜権利：CC BY 2.0｜時期：2017-06-20 14:35｜人：なし（⑤b で原寸）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：［冒頭］｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・追悼の場と支援の掲示は使わない・副題の日付と夜明け・夕方は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list33.md（写さない）',
               src='P1V1¶3.1（`Grenfell Tower is a residential tower block built in 1974`）'),
}

SPEC = {}
