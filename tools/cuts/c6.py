# -*- coding: utf-8 -*-
"""第6章　書類の上の試験飛行 c601–c624（24カット）。15本目（リノ・エアレース2011）。

■ 🔴 2026-09-30（⑤b-1）：14本目（セウォル号）の中身を空にした＝git の `dc6ecf4`（`git show dc6ecf4:tools/cuts/c6.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep15/make_plan.py` で
  台本 §4・承認ずみの映像方針（§3 案C・§4 動く模式図と地図・§5 替える画・§11-2 案B）から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所（ルール §5b-79）
  記号＝【案C】再現イラスト（置き場 A 上から見た空港・B 空の中の事故機・C ボックス席とピット・D ピットの事故機）・
        【尾翼】【ねじ】【改造】【帯】【地図】（映像方針 §4）・【年表】【棒】【書類】【帯】【使い回し】【案C 戻り】（§11-2＝案B）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    "c601": dict(kind='文字の頁',
               plan='台本の画：図 p35（報告書の頁・運用の制限・頁ごと）',
               src='AAB p35'),
    "c602": dict(kind='図解',
               plan='【地図】地図 drift：3つの距離（152・228・266メートル）と命令・通達（152／305メートル）＝どちらの内か／オカラ・アリゾナ・テキサス・ミンデン／オカラから半径約161キロと機体の居場所／州道395号を止める／その後の配置（コースを北へ・燃料車を約2.4キロ先へ）（映像方針 §4）｜台本の画：panel 半径約161キロ',
               src='AAB p35'),
    "c603": dict(kind='図解',
               plan='【地図】地図 drift：3つの距離（152・228・266メートル）と命令・通達（152／305メートル）＝どちらの内か／オカラ・アリゾナ・テキサス・ミンデン／オカラから半径約161キロと機体の居場所／州道395号を止める／その後の配置（コースを北へ・燃料車を約2.4キロ先へ）（映像方針 §4）｜台本の画：panel 2007年4月から',
               src='AAB p49'),
    "c604": dict(kind='パネル',
               plan='台本の画：panel 大きな改造のあとの決まり',
               src='AAB p36'),
    "c605": dict(kind='パネル',
               plan='台本の画：panel 届けたのは冷却装置だけ',
               src='AAB p36・p49 注47'),
    "c606": dict(kind='図解',
               plan='【帯】時間の帯（秒・分・日＝c312 の帯を広げる）：横転の約8秒前／9秒を並べた資料（写真・映像・テレメトリー）／3時間と3回／約23分と「終えた」／午後4時26分〜62分／実況の担当（マイクの印・人は描かない）／6月2日の机上訓練／5月25日の訓練（映像方針 §11-2＝案B）｜台本の画：panel 3時間と3回',
               src='AAB p36'),
    "c607": dict(kind='図解',
               plan='【帯】時間の帯：報告書がつないだ鎖（ナット→ねじ→かたさ→震え→リンク→機首上げ）／9秒の順番（0.56→1.3→4.6）／試験飛行（5回・記録2回・約23分 vs 3時間）（映像方針 §4）｜台本の画：panel 2009年9月21日・22日',
               src='AAB p36'),
    "c608": dict(kind='文字の頁',
               plan='台本の画：図 p36（報告書の頁・約23分・頁ごと）',
               src='AAB p36 注40・p49'),
    "c609": dict(kind='図解',
               plan='【帯】時間の帯：報告書がつないだ鎖（ナット→ねじ→かたさ→震え→リンク→機首上げ）／9秒の順番（0.56→1.3→4.6）／試験飛行（5回・記録2回・約23分 vs 3時間）（映像方針 §4）｜台本の画：panel 1時間40分',
               src='AAB p49・p50'),
    "c610": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='AAB p15'),
    "c611": dict(kind='文字の頁',
               plan='台本の画：図 p15（報告書の頁・記録簿の引用・頁ごと）',
               src='AAB p15'),
    "c612": dict(kind='図解',
               plan='【帯】時間の帯（秒・分・日＝c312 の帯を広げる）：横転の約8秒前／9秒を並べた資料（写真・映像・テレメトリー）／3時間と3回／約23分と「終えた」／午後4時26分〜62分／実況の担当（マイクの印・人は描かない）／6月2日の机上訓練／5月25日の訓練（映像方針 §11-2＝案B）｜台本の画：panel 約23分と「終えた」',
               src='AAB p15・p36・p49'),
    "c613": dict(kind='パネル',
               plan='台本の画：panel 実験機の飛行試験（14 CFR 91.319(b)）',
               src='AAB p35・p50'),
    "c614": dict(kind='パネル',
               plan='台本の画：panel 届けていれば',
               src='AAB p50'),
    "c615": dict(kind='図解',
               plan='【年表】年表（動く年表）：1944→2011 の機体の歩み（売却・リノ・持ち主・保管18年・分解整備と改造・2010年の出場）／勧告 A-12-08 が閉じるまで（c915 自作と同じ線）（映像方針 §11-2＝案B）｜台本の画：panel 2010年の出場',
               src='AAB p36'),
    "c616": dict(kind='図解',
               plan='【棒】数の比べ（棒）：新幹線と事故機の速さ／この機の最高との差／2010年の平均の速さ／申告の約2,700時間と総時間 約1,453時間／約200時間と約25時間／コースの3〜4Gと17.3G（映像方針 §11-2＝案B）｜台本の画：panel 2010年の成績',
               src='AAB p36 注41・p38'),
    "c617": dict(kind='図解',
               plan='【書類】書類の再現図（自作の用紙＝本物の頁ではない・台本 §0-3 の「記録簿・参加書類の再現図」）：記録簿の総時間／「試験はどうだったのか」／参加書類の「大きな改造をしたか □はい □いいえ」／年齢の欄／検査の用紙の備考と合格・書面で確かめる欄が無い／新しい検査の用紙（映像方針 §11-2＝案B）｜台本の画：panel 参加の書類の問い',
               src='AAB p37'),
    "c618": dict(kind='文字の頁',
               plan='台本の画：図 p37（報告書の頁・参加書類の答え・頁ごと）',
               src='AAB p37'),
    "c619": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='AAB p50・p51'),
    "c620": dict(kind='図解',
               plan='【棒】数の比べ（棒）：新幹線と事故機の速さ／この機の最高との差／2010年の平均の速さ／申告の約2,700時間と総時間 約1,453時間／約200時間と約25時間／コースの3〜4Gと17.3G（映像方針 §11-2＝案B）｜台本の画：panel 飛んだ時間の食い違い',
               src='AAB p12・注7・p15 注15・p51'),
    "c621": dict(kind='図解',
               plan='【書類】書類の再現図（自作の用紙＝本物の頁ではない・台本 §0-3 の「記録簿・参加書類の再現図」）：記録簿の総時間／「試験はどうだったのか」／参加書類の「大きな改造をしたか □はい □いいえ」／年齢の欄／検査の用紙の備考と合格・書面で確かめる欄が無い／新しい検査の用紙（映像方針 §11-2＝案B）｜台本の画：panel 年齢の欄',
               src='AAB p12 注7'),
    "c622": dict(kind='図解',
               plan='【棒】数の比べ（棒）：新幹線と事故機の速さ／この機の最高との差／2010年の平均の速さ／申告の約2,700時間と総時間 約1,453時間／約200時間と約25時間／コースの3〜4Gと17.3G（映像方針 §11-2＝案B）｜台本の画：panel 前の年からの時間',
               src='AAB p51'),
    "c623": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='AAB p51'),
    "c624": dict(kind='文字の頁',
               plan='台本の画：図 p51（報告書の頁・不正確な情報の段・頁ごと）',
               src='AAB p51'),
}

SPEC = {

    # ── 🔴 ⑤b-6（2026-09-30）：頁（`qa_out/ep15_assets.py`・切り口はカットごと＝目印の語の行を真ん中に）──
    # 報告書 1.11.1（p35）＝「…based and maintained at Leeward Air Ranch Airport, Ocala, Florida」の行を真ん中に（c409 と同じ頁の下）
    "c601": dict(
        t="運用の制限",
        s="報告書 1.11.1（基地はフロリダ州オカラ）",
        photo=ss.page(35), trim=ss.ptrim("c601"), panel=True, color=1.0,
    ),
    # 報告書（p36）＝「Telemetry data showed that about 23 minutes of flight time…」の行を真ん中に
    "c608": dict(
        t="試験飛行の記録",
        s="報告書 1.11.1（テレメトリーの記録）",
        photo=ss.page(36), trim=ss.ptrim("c608"), panel=True, color=1.0,
    ),
    # 報告書（p15）＝本人が署名した記録簿の文の引用（「…controllable throughout its normal range of speeds…」）
    "c611": dict(
        t="記録簿の文",
        s="本人が署名した記録簿の文（報告書の引用）",
        photo=ss.page(15), trim=ss.ptrim("c611"), panel=True, color=1.0,
    ),
    # 報告書 1.11.3（p37）＝「On the 2010 and 2011 entry documents, "no" was circled」の行を真ん中に
    "c618": dict(
        t="参加の書類",
        s="大きな改造の問いへの答え（報告書）",
        photo=ss.page(37), trim=ss.ptrim("c618"), panel=True, color=1.0,
    ),
    # 報告書の分析（p51）＝「…submitted such inaccurate information to RARA」の行を真ん中に
    "c624": dict(
        t="不正確",
        s="報告書の分析　参加の書類の申告について",
        photo=ss.page(51), trim=ss.ptrim("c624"), panel=True, color=1.0,
    ),

    # ── 🔴 ⑤b-5（2026-09-30）：型の使い回し（14本目の `qty` 棒・`axis` 年表・`boxes` 流れ図と書類の再現図）──
    # 試験の飛行の時間（分）の棒＝c606（求められた 180）→ c609（多く見積もっても 100）→ c612（テレメトリーの記録 23）。
    #   行の並びは群で決めた（3行ぶんの場所を最初から取る＝カットをまたいで棒の位置が動かない）。数は字幕
    "c606": dict(
        t="届け出への返事",
        s="冷却装置を届けたとき",
        fig=("qty", dict(view="bar", groups=[ss.QG["test"]], steps=[dict(add=ss.qb("test_req"))],
                         note="3時間＝180分", src=ss.src(["AAB p36"]))),
    ),
    # 改造のあとの初飛行（AX_LATE＝2006→2012 の寄り）：1行目＝2009年9月21日の点／2行目（整備の仲間の話）は字幕だけ
    "c607": dict(
        t="改造を終えて",
        s="2009年の秋",
        fig=("axis", dict(**ss.AX_LATE, past=[ss.ax("rebuild"), ss.ax("acc")], start=dict(cur="2009"),
                          steps=[dict(add=ss.ax("first"), cur="2009-09-21"), dict()],
                          note="年表（寄り）：改造から事故まで", src=ss.src(["AAB p10・p12・p36"]))),
    ),
    "c609": dict(
        t="5回とも20分なら",
        s="3時間には届かない",
        fig=("qty", dict(view="bar", groups=[ss.QG["test"]], past=[ss.qb("test_req", keep=True)],
                         steps=[dict(add=ss.qb("test_max")), dict(), dict()],
                         note="1時間40分＝100分（報告書の見積もり）", src=ss.src(["AAB p49・p50"]))),
    ),
    "c612": dict(
        t="書類の上では",
        s="記録簿は「終えた」",
        fig=("qty", dict(view="bar", groups=[ss.QG["test"]], past=[ss.qb("test_req", keep=True), ss.qb("test_max")],
                         steps=[dict(add=ss.qb("test_tele")), dict()],
                         note="記録は2日で約23分（途中で欠けた）", src=ss.src(["AAB p15・p36・p49"]))),
    ),
    # 2010年の出場（AX_LATE）：1行目＝2010年の点と札「予選の記録なし」／2行目（主催の団体が加えられる決まり）は字幕だけ
    "c615": dict(
        t="それでもリノへ",
        s="主催の団体の決まりで",
        # ⚠️ 初飛行の札は左へ短く（2010年の点の縦の線が「2009年9月21日」を貫いた＝⑤b-5 の layout）
        fig=("axis", dict(**ss.AX_LATE, past=[ss.ax("rebuild"), ss.ax("first", fmt="ym", anchor="end"), ss.ax("acc")],
                          start=dict(cur="2009-09-21"),
                          steps=[dict(add=ss.ax("race10", chips=["予選の記録なし"]), cur="2010"), dict()],
                          note="年表（寄り）：改造から事故まで", src=ss.src(["AAB p10・p36"]))),
    ),
    # 2010年の成績（流れ図）：🔴 棒にしない＝公式のレースの速さ（周の平均）の2011年の値が記録に無い（その瞬間の速さと物差しが違う）。
    #   1行目（速さ）＝箱だけ・数は字幕と注／2行目＝勝ち上がりの矢印と「風で中止」（AAB p38）
    "c616": dict(
        t="2010年の成績",
        s="決まりで加えられた年",
        fig=("boxes", dict(view="flow", layout=ss.HEAT,
                           steps=[dict(), dict(add=[dict(k="edge", fr="h1", to="h2"), dict(k="edge", fr="h2", to="h3"),
                                                    dict(k="chip", id="c_wind", at="h3", t="風で中止", dy=60, rec="AAB p38")])],
                           note="レースの平均の速さ（公式）は、最も速い回でも時速約602キロ未満（報告書 注41）",
                           src=ss.src(["AAB p36・p38"]))),
    ),
    # 参加の書類（2009年）：1行目（聞き役）＝紙／2行目＝問いの欄／3行目＝「はい」を書き込む（late の欄＝fill）
    "c617": dict(
        t="参加の申し込み",
        s="前に出たあとの変化",
        fig=("boxes", dict(view="form", form=ss.FORM_ENTRY09,
                           steps=[dict(add=dict(k="paper")), dict(), dict(add=dict(k="fill", f="大きな改造をしたか"))],
                           note="再現（本物の頁ではない・書いてある字は報告書に引かれた文だけ）", src=ss.src(["AAB p37"]))),
    ),
    # 飛んだ時間の食い違い（棒）：1行目＝群だけ／2行目＝2011年の参加の書類「約2,700時間」／3行目＝記録簿の総時間 約1,453時間
    "c620": dict(
        t="合わない数字",
        s="申告と記録の差",
        fig=("qty", dict(view="bar", groups=[ss.QG["hours"]],
                         steps=[dict(), dict(add=ss.qb("hours_form")), dict(add=ss.qb("hours_log"))],
                         note="書類＝この機体で飛んだ時間の申告・記録簿＝機体が生まれてからの総時間", src=ss.src(["AAB p12・p15・p16・p51"]))),
    ),
    # 年齢の欄（2009年・2010年の書類＝「59」）。2行目（2011年は正しい）は字幕だけ
    "c621": dict(
        t="年齢の欄",
        s="2年続けて同じ数",
        fig=("boxes", dict(view="form", form=ss.FORM_AGE, steps=[dict(add=dict(k="paper")), dict()],
                           note="再現（本物の頁ではない・書いてある字は報告書に引かれた文だけ）", src=ss.src(["AAB p12"]))),
    ),
    # 前の年からの時間（棒）：1行目＝書類の約200時間／2行目＝記録簿の約25時間（2009年の組み立てから2011年7月まで）
    "c622": dict(
        t="前の年からの時間",
        s="書類と記録簿",
        fig=("qty", dict(view="bar", groups=[ss.QG["recent"]],
                         steps=[dict(add=ss.qb("recent_form")), dict(add=ss.qb("recent_log")), dict()],
                         note="記録簿の値は、組み立て（2009年）から2011年7月の検査までの合計", src=ss.src(["AAB p51"]))),
    ),

    # ── 🔴 ⑤b-7（2026-09-30）：地図（`ss.fla_map`・`ss.usa_map`）・決め所・パネル ──
    # 地図：運用の制限＝基地から半径100マイル（AAB p35「proficiency flights were to be conducted within a 100-mile radius of
    #   that airport, with a special allowance for proficiency flights to be conducted en route to air shows or air races」）。
    #   1行目＝円と半径の寸法線・「決められた基地」／2行目＝外へ出る矢印（向かう途中は例外・向きはリノの方角＝模式）
    "c602": dict(
        t="練習の飛行の範囲",
        s="運用の制限",
        fig=ss.fla_map([
            ss.merge(ss.CIRCLE, dict(dim=dict(a="reno_ocala", b="ocala_r", t="約161キロ"),
                                     tag=dict(at="reno_ocala", t="決められた基地", side="below"))),
            dict(arrow=dict(a="reno_ocala", b="fl_out"), tag=dict(at="fl_out", t="向かう途中は例外", side="left"))]),
    ),
    # 地図：機体の居場所（AAB p49「not been based in Ocala, Florida, since April 2007 … remained based in Minden, Nevada」）。
    #   1行目（聞き役の問い）＝オカラの円（半径100マイル・この縮尺では小さい）／2行目＝2007年4月から不在／3行目＝2009年からネバダ
    "c603": dict(
        t="機体の居場所",
        s="運用の制限と比べて",
        # ⚠️ 下見（09-30）：この縮尺の円は半径約46画素＝オカラを輪の地点にすると町の名と札が円の線に重なった
        #    ＝オカラは輪を描かず、円の下に名と札・円の上に「不在」
        fig=ss.usa_map([
            ss.merge(ss.CIRCLE, dict(tag=dict(at="reno_ocala", t="オカラ（決められた基地）", side="below"))),
            dict(tag=dict(at="reno_ocala", t="2007年4月〜 不在", side="above")),
            dict(tag=dict(at="reno_minden", t="2009年〜 ネバダ州", side="left"))],
            places=["reno_minden", dict(k="reno_stead", side="above")],
            note="模式図：町は緯度経度から。円は半径約161キロ（100マイル・オカラの町の中心から）",
            recs=("AAB p35", "AAB p49", "#17 p7008"), rel=ss.FLA_REL),
    ),
    # 大きな改造のあとの決まり（AAB p36）：基地を受け持つFAAの地方の事務所に届ける・書面の返事を受け取るまで飛ばない
    "c604": dict(
        t="大きな改造のあと",
        s="運用の制限（報告書 36頁）",
        fig=("panel", dict(
            blocks=[dict(k="届け先", t="FAAの地方の事務所", c=J.INST),
                    dict(k="飛べるのは", t="書面の返事のあと", c=J.AMBER)],
            cols=2)),
    ),
    # 届けたのは冷却装置だけ（AAB p36・p49 注47）：2009年の冷却装置の1件・届け先はリノの事務所／ほかは記録なし
    "c605": dict(
        t="届けの記録",
        s="報告書 36頁・49頁",
        fig=("panel", dict(
            blocks=[dict(k="2009年", t="冷却装置の1件", v="リノの事務所へ", c=J.OK),
                    dict(k="ほかの大きな改造", t="記録なし", c=J.ALERT)],
            cols=2)),
    ),
    # 決め所⑨（台本 §2 #9）。AAB p15「The prescribed flight test hours have been completed」（2009-09-22・本人の署名）
    "c610": dict(
        t="記録簿の署名",
        s="組み立てのあと",
        fig=("quote", dict(
            phrase=["記録簿「規定の", "試験飛行時間を終えた」"],
            rows=[("誰が", "パイロット本人（署名）", J.INK_W),
                  ("日付", "2009年9月22日", J.LINE),
                  ("頁", "報告書 PDF 15頁（引用）", J.TICK)], paper=True)),
    ),
    # 実験機の飛行試験（14 CFR 91.319(b)・AAB p35・p50）
    "c613": dict(
        t="実験機の決まり",
        s="14 CFR 91.319(b)",
        fig=("panel", dict(
            blocks=[dict(k="安全を示すまで", t="決められた空域の中", c=J.INST),
                    dict(k="事故機の飛行試験", t="レースの速さとG", v="確認なし", c=J.ALERT)],
            cols=2)),
    ),
    # 届けていれば（AAB p50）：取り入れ口・おもり・右の板の固定＝届けた記録なし／FAAはおそらく、もっと重い試験を求めた
    "c614": dict(
        t="届けていれば",
        s="報告書 50頁",
        fig=("panel", dict(
            blocks=[dict(k="届けていない改造", t="取り入れ口・おもり・右の板", c=J.ALERT),
                    dict(k="FAAは", t="重い試験を求めた", v="おそらく", c=J.AMBER)],
            cols=2)),
    ),
    # 決め所⑩（台本 §2 #10）。AAB p51 §2.7「should not have been eligible to race the airplane in the 2010 or 2011 NCAR」
    "c619": dict(
        t="出場の資格",
        s="報告書の分析",
        fig=("quote", dict(
            phrase="2010年と11年は、本来資格が無かった",
            rows=[("記録", "NTSB 事故報告 AAB-12/01（2012年）", J.INK_W),
                  ("頁", "PDF 51頁（分析）", J.TICK)], paper=True)),
    ),
    # 決め所⑪（台本 §2 #11）。AAB p51「it is unclear why he submitted such inaccurate information to RARA」
    "c623": dict(
        t="申告の食い違い",
        s="理由について",
        fig=("quote", dict(
            phrase=["なぜ不正確な情報を", "出したのかは、不明"],
            rows=[("記録", "NTSB 事故報告 AAB-12/01（2012年）", J.INK_W),
                  ("頁", "PDF 51頁（分析）", J.TICK)], paper=True)),
    ),
}
