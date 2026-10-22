# -*- coding: utf-8 -*-
"""第10章　31人と30人 cb01–cb23（23カット）。24本目（チェルノブイリ原発事故・1986-04-26）。

■ 🆕 2026-10-22（⑤b-1）：新しいファイル。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep24/make_plan24.py` で
  映像方針の一覧 `ref/ep24/eizou_build/list24.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep24/eizou_list24.md`）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  ⚠️ 「関連（参考＝…）」と書いたカットは同じ型のほかの発電所の炉の写真（種類は写真・20% の数〈この発電所・この事故の写真〉には入れない・
     門番 check_text_screens が束の台帳 assets.json の related と照らす）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'cb01': dict(kind='写真',
               plan='🔧 C2｜一覧の種類：実写｜見せ方：全面｜副題：4号炉と石棺（2007年）｜動き：寄る｜権利：Public domain｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／Public domain｜注：🔧 IAEA 02790011（健康診断の職員の顔）→ 人の写らない写真（§0-5＝亡くなった人の数の行に顔を置かない）。02790011 は cb20 へ｜このカットの前に章の扉｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'cb02': dict(kind='図解',
               plan='一覧の種類：年表｜見た目の型：年表（亡くなった人の数）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='K1 1986-05-15 参院 内閣委・今村治 室長（`合計九名が死亡していると聞いております`）'),
    'cb03': dict(kind='写真',
               plan='🔧 T155｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：4号機の排気筒と配管（2010年）｜動き：額ごと右へ｜権利：CC BY-SA 2.0｜時期：今・跡｜人：なし｜出典の行：IAEA Imagebank（CC BY-SA 2.0）・撮影者は作者欄のとおり｜注：🔧 記念碑-ア → 発電所の今（人なし）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.43／39（`among personnel stood at 28 at the beginning of July`）'),
    'cb04': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：数の札（300人・31人）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.118／~111（`of whom 31 have so far died`）'),
    'cb05': dict(kind='文字の頁',
               plan='🔧 K19861127｜一覧の種類：頁｜見せ方：頁｜副題：衆議院 科学技術委員会の会議録（1986年11月27日）｜動き：寄る（答弁の行へ）｜見た目の型：文字の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：国会会議録 1986-11-27 衆議院 科学技術委員会｜注：🔧 記念碑-イ → 語りが引く国会の答弁の頁｜新しい画（映像方針）：🔧 頁（国会会議録の頁の画像）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='K1 1986-11-27 衆院 科学技術委・佐々木壽康 局長（`ソ連から発表されております数字でございますが、死亡者は三十一名`・`その辺の内訳はソ連から出されておりません`）'),
    'cb06': dict(kind='図解',
               plan='一覧の種類：棒｜見た目の型：棒グラフ（2つの数の内わけ）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.5／453（`30 power plant employees and firemen (including 28 deaths that were due to radiation exposure)`）'),
    'cb07': dict(kind='写真',
               plan='T158｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：石棺と排気筒（2010年・IAEA）｜動き：額ごと左へ｜権利：CC BY-SA 2.0｜時期：今・跡｜人：なし｜出典の行：IAEA Imagebank（CC BY-SA 2.0）・撮影者は作者欄のとおり｜注：台本＝現在の4号炉-チ（白黒の写真＝原本の色のまま）。チェルノブイリ・フォーラムの会議の写真は名札に人の名前が読める＝使わない｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L1 p.12／14（`one additional death was thought to have been due to a coronary thrombosis`）'),
    'cb08': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：2つの31（中身の違い）｜注：§0-5｜新しい画（映像方針）：🔧 模式（同じ31でも中身が違う＝ソ連の発表の31〈1986年の報告が書いた数・内訳はソ連から出されていない〉とフォーラムの31〈放射線28＋けが2＋心臓1〉＝「うち29」の札は外す）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.115／~108（`the fatal outcome of the disease in 29 victims`）'),
    'cb09': dict(kind='図解',
               plan='一覧の種類：箱｜見た目の型：箱（237→134→28）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.40／488（`a total of 237 were initially examined for signs and symptoms of acute radiation sickness`）'),
    'cb10': dict(kind='写真',
               plan='🔧 MIT｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：モスクワ・ミチノ墓地の慰霊碑（2013年）｜動き：額ごと寄る｜権利：CC BY-SA 3.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 3.0｜注：🔧 記念碑-ウ → 亡くなった人たちが葬られた墓地の慰霊碑（語り＝28人は、この人たちである）。墓の名は⑤b で原寸（BY-SA＝ぼかせない＝読めるなら別の点）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.40／488（`Among the 134 cases, 28 died within the first four months of the accident.`）'),
    'cb11': dict(kind='図・写真の頁',
               plan="L1p8｜一覧の種類：頁｜見せ方：頁｜副題：チェルノブイリ・フォーラムの図1（ヨーロッパのセシウム137）｜動き：寄る｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：チェルノブイリ・フォーラム『Chernobyl's Legacy』2006 の図1｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）",
               src='L1 p.13／15（`An international expert group has made projections to provide a rough estimate`）'),
    'cb12': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：数の箱（60万人の内わけ）｜注：🔧 RIVM #02（オランダ）→ 図（§0-5＝60万人はソ連の側の人たち）｜新しい画（映像方針）：🔧 模式（フォーラムの推計の作り＝60万人のうち、ほかの原因のがん約10万人に加えて、放射線で最大4,000人＝箱の大きさで・字は少なく）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L1 p.14／16（`This might eventually represent up to four thousand fatal cancers`・`in addition to the approximately 100 000`・`to be expected due to all other causes`）'),
    'cb13': dict(kind='図解',
               plan='🔧 一覧の種類：比べ｜見た目の型：比べ（3つの推計）｜注：§0-5｜新しい画（映像方針）：🔧 比べ（長い年月の推計＝フォーラム 最大4,000人〈60万人〉／国際がん研究機関 約1万6,000人〈ヨーロッパ40か国・2065年まで〉／国連の科学委員会 2008〈浴びた放射線の少ない人たちの数は出さない〉＝札は語りの言い方）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L8 p.5／5（`about 16,000 deaths (95% UI 6,700 – 38,000) from these cancers may occur`）・L8 p.2／2（`The present analysis focused on 40 European`）'),
    'cb14': dict(kind='写真',
               plan='WBG｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：西ベルリンの草の放射線写真（1986年5月14日）｜動き：額ごと寄る｜権利：CC BY-SA 4.0｜時期：後｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY-SA 4.0｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L3 p.24／64（`decided not to use models to project absolute numbers of effects`）'),
    'cb15': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：流れ（経験→計算→推計）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L1 p.13／15（`These predictions were based on the experience of other populations exposed to radiation`・`such as the survivors of the atomic bombing in Hiroshima and Nagasaki`）'),
    'cb16': dict(kind='図・写真の頁',
               plan='L1p15｜一覧の種類：頁｜見せ方：頁｜副題：チェルノブイリ・フォーラムの図3（子どもの甲状腺がん）｜動き：寄る｜見た目の型：図の頁｜権利：引用（頁）｜時期：文書｜人：なし｜出典の行：出典：チェルノブイリ・フォーラム 図3｜注：台本どおり｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S2 p.100／~93（`accumulation of radionuclides of iodine in the thyroid glands`）'),
    'cb17': dict(kind='図解',
               plan='一覧の種類：模式｜見た目の型：帯（2万例と見積もりの幅）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L4 p.7／v（`registered in the period 1991−2015 in males and females, who were under 18 in 1986`・`The uncertainty range of the estimated attributable fraction extends at least from 0.07 to 0.5`）・L4 p.20／12（`0.6 and 0.25 for the evacuated and non-evacuated children and adolescents`）'),
    'cb18': dict(kind='図・写真の頁',
               plan='CIA｜一覧の種類：頁｜見せ方：頁｜副題：CIA の地図（1996年）｜動き：寄る｜見た目の型：図の頁｜権利：Public domain｜時期：文書｜人：なし｜出典の行：CIA（Public domain）｜注：台本どおり（PD＝英字に日本語の札）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.5／453（`evacuation of about 116,000 people from areas sur-rounding the reactor during 1986`）・L2 p.67／515（`the relocation, after 1986, of about 220,000 people from Belarus, the Russian Federation and Ukraine`）'),
    'cb19': dict(kind='写真',
               plan='🔧 C27｜一覧の種類：実写｜見せ方：全面｜副題：雪の森に残るバス（2018年）｜動き：寄る｜権利：CC BY 2.0｜時期：今・跡｜人：なし｜出典の行：写真：作者欄のとおり（src/credits_private.tsv）／CC BY 2.0｜注：🔧 RIVM #03（オランダ）→ 雪の森のバス（語り＝避難の数・§0-5）。ca23 から移した｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='S3 p.42／38（`135 000 people were evacuated`）・L2 p.25／473（`is somewhat lower than the figure of 135,000 that was cited by the Committee`）'),
    'cb20': dict(kind='写真',
               plan='🔧 I11｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：交替のあとの健康診断（1986年）｜動き：額ごと寄る｜権利：CC BY-SA 2.0｜時期：後｜人：顔｜出典の行：IAEA Imagebank／Photo: USFCRFC（CC BY-SA 2.0）｜注：🔧 現在の4号炉-ツ → cb01 から移した（語り＝片づけにあたった大勢の人＝職員は公的な任務）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='L2 p.5／453（`about 240,000 workers`・`were called upon in 1986 and 1987 to take part in major mitigation activities`）'),
    'cb21': dict(kind='図解',
               plan='🔧 一覧の種類：模式｜見た目の型：3つの札（誰が・いつ・何を）｜注：🔧 記念碑-エ → 図｜新しい画（映像方針）：🔧 模式（数を言うときの3つの札＝誰が・いつ・何を数えたか）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'cb22': dict(kind='フリー素材',
               plan='X13183773｜映像の素材 5.97秒・倍率 0.86（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のプリピャチ（Pexels）｜動き：映像（0.86倍）｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：台本どおり（場面で選ぶ＝⑤b でコマを見る）｜⑤b-1（10-22）：実測のカット 6.94秒＞素材 5.97秒＝0.86倍（決まり 0.6 以上の内）｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
    'cb23': dict(kind='フリー素材',
               plan='X13188723:覆い｜映像の素材 22.06秒・倍率 6.48（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のチェルノブイリ（Pexels）｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：台本どおり（新しい覆いが写る区間を⑤b でコマから選ぶ）→ 第11章の扉｜⑤b-1（10-22）：同じ素材の別の区間を c927（覆いの写らない区間）に＝寄りの名を「覆い」に分けた｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}
