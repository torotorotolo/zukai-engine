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
               plan='🔧 X13188726:覆い｜映像の素材 25.05秒・倍率 7.36（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ・1.0 未満は動きの欄の倍率で）｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：現在のチェルノブイリ（Pexels）｜動き：映像｜権利：Pexels License｜時期：イメージ｜人：なし｜出典の行：イメージ（Pexels）｜注：台本どおり（新しい覆いが写る区間を⑤b でコマから選ぶ）→ 第11章の扉｜⑤b-1（10-22）：同じ素材の別の区間を c927（覆いの写らない区間）に＝寄りの名を「覆い」に分けた｜🔧 ⑤b-2（10-22）：X13188723 は地平線の帯を原寸で4時刻（2・8・14・20秒）見て、新しい覆いが**どこにも写らない**＝覆いの写る区間が無い → 全時刻で左の地平線に覆いと排気筒が写る X13188726 の後のショット（c101 は前のショット）へ｜台本の画＝台本 §4・一覧 eizou_list24.md（写さない）',
               src='—'),
}

SPEC = {}

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-6（2026-10-23）：図解＝`tools/mech24.py`（fig=("m24", …)・門番 check_mech の judge_m24）。🔴 人の形は使わない（数の札・積み木・面積）
#   🔴 数の流れ（台本 §1-5）：9人（5月の国会）→ 28人（7月初め・ソ連の報告＝写真のカット）→ 31人（ソ連の発表）→ 30人（2000年）→ 31人（フォーラム＝写真のカット）。
#   cb08「うち29」の札は外す・cb12 は図（60万人の内わけ）・cb13 の札は語りの言い方（映像方針 §2）。各カットは語りの数だけ（次のカットの数を先に出さない）
# ══════════════════════════════════════════════════════════
import cuts.ss as ss  # noqa: E402
from mech24 import rr  # noqa: E402

SPEC.update({
    # cb02（2行）＝1行目：1986年5月の半ば・日本の国会の答弁＝9人／2行目：そのあと増えていく（先の段は「？」）（K1 19860515）
    "cb02": dict(
        t="移り変わる数", s="最初に聞こえた数",
        fig=("m24", dict(view="stairs", steps=[dict(state=dict(may="on")), dict(state=dict(more="on"))],
                         rel=[dict(t="9人", src="K1 19860515"), dict(t="1986年5月", src="K1 19860515")],
                         note="段は模式（高さは数に比例しない）", src="国会会議録 1986-05-15 参議院 内閣委員会"))),
    # cb04（2行）＝1行目：1986年の報告（9月）・これまでに31人（病院に運ばれた300人のうち）／2行目：ソ連が発表した数（S2 p1118）
    "cb04": dict(
        t="報告に書かれた数", s="秋の時点",
        fig=("m24", dict(view="num31", steps=[dict(state=dict(n31="on")), dict(state=dict(sov="on"))],
                         rel=[dict(t="31人", src="S2 p1118"), dict(t="300人", src="S2 p1118")] + rr("r86"),
                         note="数の札は模式", src=ss.src(["S2 p1118"])))),
    # cb06（2行）＝1行目：30個の積み木（1つ＝1人）・国連の科学委員会（2000年）／2行目：そのうち放射線による28人を色で（L2 p3005）
    "cb06": dict(
        t="のちの数", s="2つに分けると",
        fig=("m24", dict(view="blocks30", steps=[dict(state=dict(all="on")), dict(state=dict(rad="on"))],
                         rel=[dict(t="30人（そのうち28人）", src="L2 p3005"), dict(t="2000年", src="L2 p3005")],
                         note="積み木の数は人数と同じ（並べ方は模式）", src=ss.src(["L2 p3005"])))),
    # cb08（3行）＝1行目は聞き役（左＝ソ連の発表の31・右＝フォーラムの31＝28＋2＋1）／2行目：左が「この動画の31人」／3行目：1986年の報告が書いた数（S2 p1118・L1 p4012）
    "cb08": dict(
        t="同じ31でも", s="中身の違い",
        fig=("m24", dict(view="two31", steps=[dict(), dict(state=dict(ours="on")), dict(state=dict(r86="on"))],
                         rel=[dict(t="31人", src="S2 p1118"), dict(t="2006年のフォーラム", src="L1 p4012"), dict(t="放射線28＋けが2＋心臓1", src="L1 p4012")] + rr("r86"),
                         note="札は模式（内わけの帯は人数に比例）", src=ss.src(["S2 p1118", "L1 p4012"])))),
    # cb09（2行）＝1行目：急性放射線障害の説明（大きな円は破線だけ）／2行目：237人を調べ・134人と確かめられた・国連の科学委員会（L2 p3040）
    "cb09": dict(
        t="大量に浴びた人の病気", s="調べた人と、確かめられた人",
        fig=("m24", dict(view="circles", steps=[dict(state=dict(**{"def": "on"})), dict(state=dict(n="on"))],
                         rel=[dict(t="237人・134人", src="L2 p3040")], note="円の面積は人数に比例", src=ss.src(["L2 p3040"])))),
    # cb12（3行）＝1行目：多く放射線を浴びた60万人・2006年のフォーラム／2行目：ほかの原因のがん およそ10万人／3行目：加えて最大4,000人（推計）（L1 p4014）
    "cb12": dict(
        t="推計の作り", s="もとから起きる分と、増える分",
        fig=("m24", dict(view="area60", steps=[dict(state=dict(pop="on")), dict(state=dict(base="on")), dict(state=dict(add="on"))],
                         rel=[dict(t="60万人・およそ10万人・最大4,000人", src="L1 p4014"), dict(t="2006年のフォーラム", src="L1 p4014")],
                         note="四角の面積は人数に比例", src=ss.src(["L1 p4014"])))),
    # cb13（2行）＝1行目：国際がん研究機関・ヨーロッパの40か国で・2065年までに／2行目：およそ1万6,000人（左はフォーラム＝前のカットの続き）（L8 pdf2・pdf5）
    "cb13": dict(
        t="別の推計", s="範囲を広げると",
        fig=("m24", dict(view="scope2", steps=[dict(state=dict(who="on")), dict(state=dict(n="on"))],
                         rel=[dict(t="2006年のフォーラム・60万人・最大4,000人", src="L1 p4014"), dict(t="40か国（ヨーロッパ）・2065年", src="L8 pdf2"),
                              dict(t="およそ1万6,000人", src="L8 pdf5")],
                         note="札は模式（2つの推計は範囲が違う＝並べて足さない）", src="国際がん研究機関 2006 p.2・p.5／チェルノブイリ・フォーラム（2006年）p.16"))),
    # cb15（3行）＝1行目は聞き役（計算の機械）／2行目：広島と長崎の被爆者など・ほかで浴びた人たちの経験／3行目：推計の数＝実際に数えた人数ではない（L1 p4013）
    "cb15": dict(
        t="推計のもと", s="数えた数との違い",
        fig=("m24", dict(view="machine", steps=[dict(), dict(state=dict(**{"in": "on"})), dict(state=dict(out="on"))],
                         rel=[], note="機械は模式", src=ss.src(["L1 p4013"])))),
    # cb17（3行）＝1行目：18歳未満・1991年から2015年・およそ2万例（升目）／2行目：放射線による分 およそ4分の1（25升）／3行目：幅は少なくとも7%から50%（L4）
    "cb17": dict(
        t="子どもの甲状腺がん", s="見積もりの幅",
        fig=("m24", dict(view="waffle", steps=[dict(state=dict(all="on")), dict(state=dict(quarter="on")), dict(state=dict(range="on"))],
                         rel=[dict(t="2万例（1991〜2015年・18歳未満）", src="L4 pdf7"), dict(t="およそ4分の1", src="L4 pdf7"),
                              dict(t="7%から50%", src="L4 pdf7")],
                         note="升目1つ＝およそ200例（幅の帯は割合に比例）", src="UNSCEAR 白書 2018（甲状腺がん）p.v・p.12"))),
    # cb21（2行）＝1行目は聞き役（「数」の札）／2行目：誰が・いつ・何を数えたか
    "cb21": dict(
        t="数の出どころ", s="この章のまとめ",
        fig=("m24", dict(view="tags3", steps=[dict(), dict(state=dict(tags="on"))],
                         rel=[], note="札と糸は模式", src="この動画の語り"))),
})

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-7（2026-10-23）：写真・頁・映像（第10章の13）＝c2.py・c6.py・c7.py の ⑤b-7 の塊と同じ書き方
# ══════════════════════════════════════════════════════════
_C2, _C27 = P("c2"), P("c27")
SPEC.update({
    # cb01（2行・1行目は聞き役の問い・亡くなった人の数の行＝人の写らない写真）＝🔧 C2（4号炉と石棺・PD）＝全面で寄る
    "cb01": dict(photo=_C2, **ss.mv(_C2, "in"), side="none", color=1.0,
                 t="数え方で変わる数", s="4号炉と石棺（2007年）"),
    # cb03（2行）＝🔧 T155（4号機の排気筒と配管・2010年・人なし）＝額ごと右へ
    "cb03": dict(photo=P("t155"), panel=True, color=1.0, fmove=ss.fm("r"),
                 t="7月の初めまで", s="4号機の排気筒と配管（2010年）"),
    # cb05（2行）＝国会会議録 1986-11-27 衆議院 科学技術委員会 第4号の1頁目の下の段（佐々木局長の答弁＝「死亡者は三十一名」
    #   「（内訳は）出されておりません」）＝OCR の行の箱 x 540〜865・y 1695〜2215（元の画像の画素）
    #   🔧 ⑤b-7：上の辺 0.717 は段の区切りの横線（束の割合 0.7180〜0.7198）を入れていた＝線と字（0.7254〜）のあいだ 0.7226 に
    #   （下の辺 0.941 は字の終わり 0.9337 と線 0.9423〜 のあいだ＝そのまま）。束の絵の行ごとのインクで測った
    "cb05": dict(photo=P("k19861127"), trim=(0.332, 0.7226, 0.532, 0.941), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="11月の国会", s="1986年11月27日の国会の会議録（衆議院）"),
    # cb07（2行）＝T158（石棺と排気筒・白黒＝原本の色のまま）＝額ごと左へ
    "cb07": dict(photo=P("t158"), panel=True, color=1.0, fmove=ss.fm("l"),
                 t="フォーラムの数え方", s="石棺と排気筒（2010年・IAEA）"),
    # cb10（2行）＝🔧 MIT（モスクワ・ミチノ墓地の慰霊碑・BY-SA 3.0＝ぼかせない＝墓の名が読めるかを試し焼きを原寸で）＝額ごと寄る
    "cb10": dict(photo=P("mit"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="両方の数に入る人", s="モスクワ・ミチノ墓地の慰霊碑（2013年）"),
    # cb11（2行・1行目は聞き役の問い）＝チェルノブイリ・フォーラムの図1（ヨーロッパのセシウム137・左の段の地図）＝地図の画像ブロックと題（2段組みの左だけ）。
    #   🔧 試し焼き 39912142820：右の辺 0.459 は右の段の本文の頭（束の絵の OCR x 0.417〜）を縦に切っていた・上の写真（頁の画像ブロック1）は図1でない
    #   ＝頁の割合 x 0.02〜0.415・y 0.428〜0.665（地図＝画像ブロック2 と題の3行・題の右の端は x 0.416）
    "cb11": dict(photo=P("l1p8"), trim=(0.001, 0.372, 0.403, 0.633), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="長い年月の数", s="チェルノブイリ・フォーラムの図1（ヨーロッパのセシウム137）"),
    # cb14（2行）＝WBG（西ベルリンの草の放射線写真・縦長・BY-SA 4.0）＝額ごと寄る
    "cb14": dict(photo=P("wbg"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="出さないと決めた推計", s="西ベルリンの草の放射線写真（1986年5月14日）"),
    # cb16（2行）＝チェルノブイリ・フォーラムの図3（子どもの甲状腺がん）＝図の上の本文の下から題の下まで
    "cb16": dict(photo=P("l1p15"), trim=(0.075, 0.230, 0.853, 0.580), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="数えて分かった増加", s="チェルノブイリ・フォーラムの図3（子どもの甲状腺がん）"),   # 「はっきり増えたもの」は語りの写し（echo）
    # cb18（2行）＝CIA の地図（1996年・PD・頁の扱い）＝額ごと寄る。凡例の訳は横の札（ann・凡例の字＝束の絵の OCR）。
    #   ⚠️ 英字をそのまま札に写すと門番 slide G-09（焼き込みの写し）＝札は凡例の行の順だけを名乗る
    "cb18": dict(photo=P("cia"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="避難と移住", s="CIA の地図（1996年）",   # 「住む所を離れた人」は語りの写し（echo）
                 ann=[dict(t="凡例の1つ目", d="閉ざされた区域"), dict(t="2つ目", d="常に管理する区域"), dict(t="3つ目", d="ときどき管理する区域")]),
    # cb19（2行）＝🔧 C27（雪の森に残るバス・CC BY 2.0）＝全面で寄る
    "cb19": dict(photo=_C27, **ss.mv(_C27, "in"), side="none", color=1.0,
                 t="避難の数", s="雪の森に残るバス（2018年）"),
    # cb20（3行・1行目は聞き役）＝🔧 IAEA 02790011（交替のあとの健康診断＝片づけにあたった人・公的な任務）＝額ごと寄る
    "cb20": dict(photo=P("i11"), panel=True, color=1.0, fmove=ss.fm("in"),
                 t="片づけにあたった人", s="交替のあとの健康診断（1986年）"),
    # cb22（2行・6.9秒）＝Pexels 13183773（プリピャチの今・6.0秒＝0.86倍）
    "cb22": ss.vid("cb22"),
    # cb23（1行・3.4秒）＝Pexels 13188726 の後のショット（覆いが写る＝STOCK_WINDOW 17.00〜20.45）→ 第11章の扉
    "cb23": ss.vid("cb23"),
})
