# -*- coding: utf-8 -*-
"""第10章　35の勧告のその後 cb01–cb16（16カット）。32本目（USエアウェイズ1549便のハドソン川への着水・2009-01-15・ニューヨーク・報告書 NTSB/AAR-10/03 は2010-05-04 採択）。

■ 🔴 2026-11-10（⑤b-1）：31本目（全日空機雫石衝突事故）の中身を空にした＝git の `f4bd0a9a`（`git show f4bd0a9a:tools/cuts/cb.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep32/make_plan32.py` で
  映像方針の一覧（`ref/ep32/eizou_build/make_list32.py`＝了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（元の画は台本 §4・一覧 `ref/ep32/eizou_list32.md`＝⑤b は一覧に従う）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  🔴 額装・帯の写真は静止（`build_jiko.FRAME_STILL_EP` に ep32）＝`fmove`（額ごと動かす）・額の中の `cam` を書かない（門番 check_fmove が絵で測る）。
  🔴 写真は画面いっぱい・色は原本（`build_jiko.PHOTO_KEEP_EP` に ep32）・BY-SA は額装・紙面と調査の写真も額装。説明カットの地は写真を暗くするだけ（8:1・衛星と夜の写真は地にしない）。
  🔴 VTS（沿岸警備隊の監視カメラ）は等速・止めなし・頭から使う・同じ秒を2回使わない（区間は一覧の動きの欄＝make_list32 の門番）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  🔴 この回の線＝語りと画面に名前を出すのは機長と副操縦士だけ（初出 c203・c205）・客室乗務員・管制官・救助の人は立場だけ・乗客は名前なし・
     NTSB・FAA・議員・知事・監督・俳優は役職で・「犠牲」「死亡」は言わない・「208秒」は使わず「約3分半」・映画は c517〜c518・c520 だけ
     ＝図でも同じ（紙面・写真に名前の字が写る＝親が絵を見て切る・船の名も読ませない）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'cb01': dict(kind='図解',
               plan='🔧 地：C13（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：35本の札の束＝FAA 26・ヨーロッパの航空の当局 8・農務省 1｜注：—｜新しい画（映像方針）：🔧 地 [11]（夜）→ [13]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='報p145（`As a result of this investigation, the National Transportation Safety Board`）・計（勧告35本＝報告書の34本〈A-10-62〜95〉と先に出した1本〈A-09-112〉）'),
    'cb02': dict(kind='図解',
               plan='🔧 地：C13（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：箱｜副題：2026年11月の時点の状態の箱＝閉じた34〈受け入れられる対応 10・受け入れられる別の対応 7・受け入れられない対応｜注：—｜新しい画（映像方針）：🔧 地 [11]（夜）→ [13]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（CAROL の控え 2026-11-09 の数え＝閉34・開1・受け入れられない 16）'),
    'cb03': dict(kind='図解',
               plan='🔧 地：C13（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：勧告の評価の札＝NTSB が相手の対応を見て評価をつけて閉じる｜注：—｜新しい画（映像方針）：🔧 地 [11]（夜）→ [13]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（CAROL の状態の欄＝受け入れられる対応・受け入れられる別の対応・受け入れられない対応・NTSB が考え直して閉じた・開いている）'),
    'cb04': dict(kind='写真',
               plan='🔧 C9｜一覧の種類：写真｜見せ方：全面｜副題：夜の作業＝機体を岸壁につなぐ〈2009年1月・陸軍工兵隊〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝夜・工兵隊の作業員と警察の人｜権利：CC BY 2.0｜時期：2009-01（頁の説明＝機体を岸壁につなぐ作業）・夜｜人：工兵隊・警察（公的な任務・中景）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：夜の写真＝全面は可｜新しい画（映像方針）：🔧 副題を頁の説明に（機体を岸壁につなぐ作業）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='勧（`A-10-066 それに代わる対応 2014-07-23`）・勧（`A-10-067 受け入れられない対応 2014-07-23`）・勧（`A-10-069 受け入れられない対応 2014-07-23`）'),
    'cb05': dict(kind='図解',
               plan='🔧 地：C14（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：手順書の作り方の指針の勧告の札・2012年｜注：—｜新しい画（映像方針）：🔧 地 [9]（夜）→ [14]｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='勧（`A-10-068 受け入れられない対応 2012-07-18`）'),
    'cb06': dict(kind='写真',
               plan='🔧 C14｜一覧の種類：写真｜見せ方：全面｜副題：錨を下ろす作業船の人たち〈2009年1月・陸軍工兵隊〉｜動き：ゆっくり寄る｜見た目の型：11-10 640px＝甲板で綱を引く2人・錨｜権利：CC BY 2.0｜時期：2009-01（頁の説明）｜人：工兵隊の作業員（横顔・公的な任務）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY 2.0）｜注：—｜新しい画（映像方針）：🔧 副題「機体のまわりの作業」→ 写っているもの（機体は写っていない）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='勧（`A-10-072 受け入れられる対応 2025-12-02`）・報p142（`Require applicants for aircraft certification to demonstrate that their ditching parameters can be attained without engine power by pilots without the use of exceptional skill or strength`）'),
    'cb07': dict(kind='図解',
               plan='地：C14（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：事故から17年近くの帯の札｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（2009-01-15 から 2025-12-02 まで＝16年10か月17日＝§9）'),
    'cb08': dict(kind='写真',
               plan='🔧 D79-45｜一覧の種類：調査｜見せ方：額装（高さいっぱい）｜副題：65番の骨組みの床の穴〈NTSB の調査の写真〉｜動き：静止｜権利：同上｜時期：2009（凡例）｜人：なし｜出典の行：写真：NTSB 公開ドケット DCA09MA026（構造の追記の写真 写真45）｜注：△ 絵は ⑤b で原寸｜新しい画（映像方針）：🔧 調査の写真の番号を凡例から（#79 写真45）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 調査の写真（NTSB のドケット）＝額装・無加工・出典の行・人の写り（顔・名前の字・船の名）は原寸で（⑤b-2）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='勧（`A-10-077 受け入れられる対応 2019-05-29`）・報p143（`Require Airbus to redesign the frame 65 vertical beam on A318, A319, A320, and A321 series airplanes to lessen the likelihood that it will intrude into the cabin during a ditching or gear-up landing`）'),
    'cb09': dict(kind='文字の頁',
               plan='FR2023｜一覧の種類：公的｜見せ方：額装（高さいっぱい）｜動き：静止｜権利：PD（米国の連邦の業務）｜時期：2023｜人：なし｜出典の行：出典：連邦官報 2023-06413（FAA・2023年）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 公的な機関の紙面（報告書・ドケット・連邦官報ほか）＝額装・無加工・出典の行・🔴 名前の行を入れない＝親が絵を見て切る（名前を出すのは機長と副操縦士だけ）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='官（`ensure that turbofan engines can ingest`…`the largest medium flocking bird (MFB) into the engine core at climb or approach conditions`）・官（`DATES: Effective June 5, 2023`）'),
    'cb10': dict(kind='図解',
               plan='地：C61（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：規則の説明の札＝1549便の事故から研究が始まった｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='官（`As a result of the Flight 1549 accident, the FAA began studying how to improve engine durability related to core engine bird ingestion`）・勧（`A-10-064 それに代わる対応 2024-04-03`）'),
    'cb11': dict(kind='フリー素材',
               plan='Xb11｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：空を飛ぶ鳥の群れと旅客機の遠景〈社名と機種は見せない〉｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='勧（`A-10-087 開いている`）・報p144（`Develop and implement, in conjunction with the Federal Aviation Administration, innovative technologies that can be installed on aircraft that would reduce the likelihood of a bird strike`）'),
    'cb12': dict(kind='フリー素材',
               plan='Xb12｜一覧の種類：イメージ｜見せ方：全面｜副題：イメージ：救命胴衣の着け方の説明〈人の顔なし｜動き：ゆっくり寄る｜権利：Pexels｜時期：現在｜人：なし（顔・ナンバー・店の字なし）｜出典の行：イメージ（Pexels）｜🔴 イメージ＝Pexels を1本ずつ原寸で見る（人の顔・ナンバー・店の名前・読める画面の字・AI で作った絵が無いこと）・副題は「イメージ」から・等速が基本・音は使わない（-an）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='勧（`A-10-082 受け入れられない対応 2015-09-03`）・報p143（`be equipped with flotation seat cushions and life vests for each occupant on all flights, regardless of the route`）・勧（`A-10-083 受け入れられない対応 2017-08-31`）・報p143（`brief passengers on all flotation equipment installed on an airplane, including a full demonstration of correct life vest retrieval and donning procedures, before all flights, regardless of route`）'),
    'cb13': dict(kind='図解',
               plan='🔧 地：GL1（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：救命胴衣の勧告の札＝すばやく正しく着けられる決まりへ｜注：—｜新しい画（映像方針）：🔧 地 [11]（夜）→ イメージ〈救命胴衣〉｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='勧（`A-10-085 受け入れられる対応 2018-01-19`）・報p143（`Revise the life vest performance standards contained in Technical Standard Order-C13f to ensure that they result in a life vest that passengers can quickly and correctly don`）'),
    'cb14': dict(kind='図解',
               plan='🔧 地：C13（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：箱｜副題：ヨーロッパの当局あての8本の札＝受け入れられる 3・受け入れられる別の対応 1・受け入れられない 4｜注：—｜新しい画（映像方針）：🔧 模式 → 箱（3・1・4 本の状態）・地 [11]（夜）→ [13]＝模式の連続を切る｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（CAROL の控えの数え＝EASA 8本＝2・2・2・3・4・4・4・4）'),
    'cb15': dict(kind='図解',
               plan='🔧 地：C49（暗くするだけ・字と地の比 8:1 が下限＝了承②・色は原本・動かさない）｜一覧の種類：模式｜副題：手順書と訓練の勧告の札に「受け入れられない対応」の印｜注：—｜新しい画（映像方針）：🔧 地 [9]（夜）→ [49]（操縦室の天井＝手順書の話）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（3つ目の問いの答えの後半）'),
    'cb16': dict(kind='写真',
               plan='🔧 C45｜一覧の種類：写真｜見せ方：額装（高さいっぱい）｜副題：はしけの上の機体〈2009年1月18日〉｜動き：静止｜見た目の型：11-10 640px＝雪の公園・街灯・奥のはしけの機体｜権利：CC BY-SA 3.0｜時期：2009-01-18（頁の説明）｜人：はしけの人（遠景・小さい）｜出典の行：写真：{作者}／Wikimedia Commons（CC BY-SA 3.0）・無加工｜注：BY-SA＝額装・無加工｜新しい画（映像方針）：🔧 副題に撮影の日（頁の説明）｜🔴 額装は静止（fmove・cam を書かない＝門番 check_fmove が絵で測る・10-26 カズヤくん）・額の地は同じ写真のぼかし（VTS も同じ映像のぼかし）｜🔴 写真＝色は原本のまま・画面いっぱい（BY-SA は額装・無加工）・作者の名前は git の外の表（src/credits_private.tsv）から焼くときに差し込む・私人の顔は顔だけモザイク可（CC BY・PD だけ）・副題の日付と夕方・夜は頁の説明と EXIF のまま（gate_era）｜台本の画＝台本 §4・一覧 eizou_list32.md（写さない）',
               src='計（橋の1行）'),
}

SPEC = {}

# 🆕 ⑤b-3（2026-11-10）：紙面（型は c1.py の同じ節）
_Rb09 = P("fr2023_cb09")
SPEC.update({
    # cb09＝連邦官報の頁の頭（誌名・号・2023年4月4日）＋FAA の最終規則の頭（1頁目の右の段の下）＋2頁目の左の段の頭
    #   （SUMMARY の続き〜「DATES: Effective June 5, 2023.」）を縦につないだ。582×1284＝高さいっぱい
    "cb09": dict(photo=_Rb09, panel=True, ptall=True, ground=dict(photo=_Rb09, blur=ss.PAGE_BLUR), color=1.0,
                 t="鳥の試験の規則", s="連邦官報〈2023年4月4日〉"),
})

# 🆕 ⑤b-4b（2026-11-11）：イメージの写真（Pexels・全面・見出しと副題なし・原色＝c5.py の「⑤b-4a」の節の型）
_Xb11, _Xb12 = (P(f"stock/{c}") for c in ("xb11", "xb12"))
SPEC.update({
    # cb11＝青空を渡る鳥の群れと遠くの旅客機（機体は飛行機雲の先の点＝印は見えない）
    "cb11": dict(photo=_Xb11, **ss.mvz(_Xb11, (0.45, 0.5, 1.0), (0.4, 0.48, 1.12)), side="none", color=1.0, t="", s=""),
    # cb12＝救命胴衣を着けた客室乗務員の後ろ姿（顔なし・胴衣の字は使い方〈TOP・DESSUS〉だけ・制服に印なし＝原寸）
    "cb12": dict(photo=_Xb12, **ss.mvz(_Xb12, (0.5, 0.4, 1.0), (0.5, 0.38, 1.1)), side="none", color=1.0, t="", s=""),
})

# 🆕 ⑤b-5（2026-11-11）：模式（`tools/mech32.py`）＝地 gl1 の明るさを測るため ⑤b-6 から前倒し（左上の船の札は地の見える帯 y 0.31〜0.69 の外＝640px で確かめた）
import mech32 as _m32  # noqa: E402
SPEC.update({
    "cb13": _m32.fu_spec("cb13", ss.gr("stock/gl1")),
})
