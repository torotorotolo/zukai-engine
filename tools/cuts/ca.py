# -*- coding: utf-8 -*-
"""第10章　裁判と議会 ca01–ca27（27カット）。16本目（バイオントダム災害）。

■ 🔴 2026-10-01（⑤b-1）：新しく作った（15本目は9章）。14本目の同じ名前の章ファイル（第10・11章＝別の中身）は
  git の `dc6ecf4`（`git show dc6ecf4:tools/cuts/ca.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep16/make_plan.py` で
  台本 §4・承認ずみの映像方針（§1-3 冒頭・§3 置き場・§4-2 合図・§5 案C・§6 図表・§8 替える画）から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  種類＝写真／図・写真の頁／再現イラスト／図解／混ざり／文字の頁／パネル／決め所（ルール §5b-79）
  記号＝【案C VA】上から見た谷・【案C VB】谷を横切る断面・【案C VC】谷に沿う断面（ダム）・【案C VD】正面から見た斜面（§3）・
        【冒頭】（§1-3）・【線の図】場面1・【帯】場面4 時間の帯・【断面の図解】・【地図】drift（§6）・【混ざり】（§9⑦）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    "ca01": dict(kind='写真',
               plan='台本の画：実写 #108 1968年11月のラクイラの法廷',
               src='S1 PDF178'),
    "ca02": dict(kind='図解',
               plan='台本の画：図 年表 議会と裁判（1964-05-22 法律で議会の調査委員会・1965 最終報告・1968-02-20 予審・1969-12-17 一審・1970-10-03 控訴審・1971-03-25 破毀院）（rec= PDF1・PDF26・S9 PDF17〜18・S10 PDF19〜20）',
               src='S1 PDF1'),
    "ca03": dict(kind='写真',
               plan='台本の画：実写 #116 下流から見た今のダム（現在）',
               src='S1 PDF26'),
    "ca04": dict(kind='図解',
               plan='台本の画：図 並べ図 議会の3つの報告（多数派・少数派1・少数派2）（rec= PDF26・PDF178・PDF207・PDF241）',
               src='S1 PDF26・PDF178'),
    "ca05": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='S1 PDF178'),
    "ca06": dict(kind='文字の頁',
               plan='台本の画：図 p178（議会の報告 PDF178 の段・頁ごと）',
               src='S1 PDF178'),
    "ca07": dict(kind='写真',
               plan='台本の画：実写 #117 真下から見た今のダム（現在・CC BY 3.0）',
               src='S1 PDF166・PDF179'),
    "ca08": dict(kind='文字の頁',
               plan='台本の画：図 p207（少数派の報告 PDF207 の段・頁ごと）',
               src='S1 PDF207'),
    "ca09": dict(kind='図解',
               plan='台本の画：図 書類の再現図 もう1つの少数派の報告の一文（rec= PDF241）',
               src='S1 PDF241'),
    "ca10": dict(kind='図解',
               plan='台本の画：図 並べ図（ca04 を戻す）',
               src='—'),
    "ca11": dict(kind='図解',
               plan='台本の画：図 年表（ca02 の図・1968年に印）',
               src='S9 PDF17・S10 PDF19'),
    "ca12": dict(kind='写真',
               plan='台本の画：実写 #108 1968年11月のラクイラの法廷（別の部分に寄る）',
               src='S9 PDF17・S10 PDF20'),
    "ca13": dict(kind='図解',
               plan='【地図】地図 drift：水の通り道（湖 → 発電所）・ベッルーノとラクイラ（映像方針 §6）｜台本の画：図 地図【上から】 ベッルーノとラクイラ（rec= S10 PDF19）'
                    '｜🆕 ⑤b-8（2026-10-02）：流れ図（箱の型）に替えた＝2つの町の距離・座標が資料に無い（門番 check_drift ③）＝映像方針 §18',
               src='S10 PDF19'),
    "ca14": dict(kind='図解',
               plan='台本の画：図 年表（ca02 の図・1968年11月に印）',
               src='S9 PDF17'),
    "ca15": dict(kind='図解',
               plan='台本の画：図 年表（1969-12-17 一審に印）',
               src='S9 PDF18'),
    "ca16": dict(kind='図解',
               plan='台本の画：図 年表（1970-10-03 控訴審に印）',
               src='S9 PDF18'),
    "ca17": dict(kind='図解',
               plan='台本の画：図 並べ図 控訴審の結果（有罪2人・無罪5人・裁判から外れた1人＝顔は描かない）（rec= S9 PDF18）',
               src='S9 PDF18・S1 PDF98'),
    "ca18": dict(kind='図解',
               plan='台本の画：図 年表（1971-03-25 破毀院に印）',
               src='S9 PDF18・S2 p.718'),
    "ca19": dict(kind='図解',
               plan='台本の画：図 書類の再現図 破毀院の判断（1つの災害・崩落も含めて、出来事を予見していながらの重い過失）（rec= S9 PDF18・S2 p.718）',
               src='S9 PDF18・S2 p.718'),
    "ca20": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='S10 PDF20'),
    "ca21": dict(kind='図解',
               plan='台本の画：図 年表（1971-04-09 の時効に印）',
               src='S9 PDF18・S10 PDF20'),
    "ca22": dict(kind='図解',
               plan='台本の画：図 数の比べ 刑の重さ（ビアデーネ 5年うち3年免除・センシドーニ 3年8か月うち3年免除）（rec= S9 PDF18・S10 PDF20）',
               src='S9 PDF18・S10 PDF20'),
    "ca23": dict(kind='写真',
               plan='台本の画：実写 #122 残った湖と崩れた山（現在・CC BY 4.0）',
               src='S10 PDF20'),
    "ca24": dict(kind='写真',
               plan='台本の画：実写 #121 すべり面の近景（現在・CC BY 2.5）',
               src='S9 PDF18'),
    "ca25": dict(kind='図解',
               plan='台本の画：図 年表 その後の裁判（1975 ラクイラの控訴院）',
               src='S9 PDF18'),
    "ca26": dict(kind='再現イラスト',
               plan='【案C VA 上から見た谷】🆕 ⑤b-7（2026-10-02 カズヤくん）：Google Earth → 地図（VA）に替えた＝ピアーヴェ川の下流'
                    '（SPEC は ⑤b-8）｜台本の画：実写 Googleアース⑥ ピアーヴェ川の下流（現在）',
               src='S10 PDF20'),
    "ca27": dict(kind='写真',
               plan='台本の画：実写 #118 ロンガローネから峡谷ごしに見る今のダム（現在・CC BY 3.0）',
               src='S10 PDF20'),
}

SPEC = {
    # ── 🆕 ⑤b-7（2026-10-02）：写真と頁の束（`qa_out/ep16_assets.py`）──
    # #108（1968年11月・ラクイラの法廷）。🔴 座っている人の横顔8人＝顔だけモザイク。章の頭（扉の地に混ざる＝PD・モザイクのまま）
    "ca01": dict(
        t="責任を問う",
        s="1968年11月　ラクイラの法廷",
        photo=P("trial_1968"), **ss.kind(P("trial_1968")),
    ),
    # #116（Riccardo Sartor・PD）＝下流の峡谷から見たいまのダム
    "ca03": dict(
        t="いまのダム",
        s="2008年2月　下流の峡谷から見たダム",
        photo=P("dam_now_downstream"), **ss.kind(P("dam_now_downstream")),
    ),
    # 多数派の本文（p178 右の段）＝「…non fu previsto da nessuno e che le previsioni formulate, anche considerate nella loro
    #   peggiore combinazione, escludevano pericoli per la pubblica incolumità.」（ca05 の★も同じ段）
    "ca06": dict(
        t="多数派の本文",
        s="当時の予測について書く段",
        photo=ss.page(178), trim=ss.ptrim("ca06"), panel=True, color=1.0,
    ),
    # #117（Stefano Petri・CC BY 3.0）＝真下から見たダム（縦）
    "ca07": dict(
        t="多数派の疑問",
        s="2003年4月　真下から見たダム",
        photo=P("dam_now_below"), **ss.kind(P("dam_now_below")),
    ),
    # 少数派の報告（p207 左の段）＝「…travolti da un evento prevedibile e probabile, e quindi evitabile…」（c910 と同じ頁・切り口は別）
    "ca08": dict(
        t="少数派の報告",
        s="「予見でき、避けられた」と書く段",
        photo=ss.page(207), trim=ss.ptrim("ca08"), panel=True, color=1.0,
    ),
    # #108 の右側（判事席と憲兵＝法廷の公務・モザイクの外）に寄る＝PLAN「別の部分に寄る」
    "ca12": dict(
        t="11人の被告",
        s="1968年11月　一審の法廷の判事席",
        photo=P("trial_1968"), trim=(0.38, 0.0, 1.0, 1.0), panel=True,
    ),
    # #122（Gianmarco139・CC BY 4.0）＝残った湖と崩れた山
    "ca23": dict(
        t="いまの湖",
        s="2015年5月　残った湖と崩れた山",
        photo=P("lake_now"), **ss.kind(P("lake_now")),
    ),
    # #121（Christian Thiergan・CC BY 2.5）＝トック山のすべり面の近景
    "ca24": dict(
        t="すべり面",
        s="2005年7月　トック山のすべり面",
        photo=P("slide_surface_now"), **ss.kind(P("slide_surface_now")),
    ),
    # #118（Stefano Petri・CC BY 3.0）を戻す（bias 0.6＝c111 の注）
    "ca27": dict(
        t="峡谷の奥のダム",
        s="2003年4月　ロンガローネから峡谷ごしに見たダム",
        photo=P("dam_gorge_now"), **ss.kind(P("dam_gorge_now")), bias=0.6,
    ),
    # ── 🆕 ⑤b-6b（2026-10-01）：年表（`axis` の date）・数の比べ（`qty`）・書類の再現図と並べ図（`boxes`）＝14本目の型 ──
    # 🔴 裁判の年表は c110 と同じ軸（ss.AX_ANS＝1963〜72年）で続ける。前のカットの点は札を消して沈める（ss.dot）・すぐ前の点だけ札を
    #   沈めて残す。一審・控訴審・破毀院の言葉は c719・ca16・ca18 で初めて説明する＝その前のカットの画面に出さない
    # ca02（9.60秒）＝議会の調査委員会（S1 p1「LEGGE 22 MAGGIO 1964, n. 370」・委員は senatore／deputato）。1行目「1964年5月の法律で」で
    #   点／2行目「委員は、上院と下院の議員たち」で項目の札
    "ca02": dict(
        t="議会が調べる", s="法律でつくられた委員会",
        fig=("axis", dict(**ss.AX_ANS, past=[ss.ax("a_fall", anchor="end")], start=dict(cur="1963-10-09"), steps=[
            dict(add=ss.ax("l_parl"), cur="1964-05-22"),
            dict(add=dict(k="chips", at="1964-05-22", chips=["上院と下院の議員"], rec="S1 p1"))],
            src=ss.src(["S1 p1", "S1 p98"]))),
    ),
    # ca04（9.66秒）＝議会の3つの報告（S1 p26＝多数派の報告を19対8で決め、2つの少数派の報告を添えた）。同じ形で並べるだけ（多数派の
    #   中身は語りと ca05 の決め所）。1行目（聞き役）で3つ／2〜3行目は足さない
    "ca04": dict(
        t="予見できたか", s="議会の3つの報告",
        fig=("boxes", dict(view="row", slots=3, steps=[
            dict(add=[ss.cause("rep_maj"), ss.cause("rep_min1"), ss.cause("rep_min2")]), dict(), dict()],
            src=ss.src(["S1 p26", "S1 p178", "S1 p207", "S1 p241"]))),
    ),
    # ca09（7.63秒）＝もう1つの少数派の報告の一文（S1 p241「la tesi, piuttosto affermata che dimostrata, secondo cui la sciagura del
    #   Vajont ha avuto tutti i caratteri della assoluta imprevedibilità」）。1行目で紙と「退ける説」／2行目「示されたというより、言い張られた
    #   もの」で「その説は」
    "ca09": dict(
        t="言い張られた説", s="イタリア語の原文",
        fig=("boxes", dict(view="form", form=ss.FORM_MIN2, steps=[
            dict(add=[dict(k="paper"), dict(k="fill", f="退ける説")]), dict(add=dict(k="fill", f="その説は"))],
            note="欄の字は原文のまま・様式は再現", src=ss.src(["S1 p241"]))),
    ),
    # ca10（5.03秒）＝ca04 を戻す（同じ3つ）
    "ca10": dict(
        t="見方が割れた", s="議会の3つの報告",
        fig=("boxes", dict(view="row", slots=3,
                           past=[ss.cause("rep_maj", keep=True), ss.cause("rep_min1", keep=True),
                                 ss.cause("rep_min2", keep=True)], steps=[dict(), dict()],
                           src=ss.src(["S1 p26", "S1 p178", "S1 p207", "S1 p241"]))),
    ),
    # ca11（7.58秒）＝予審（S9 p2017「20 febbraio. Il Giudice istruttore Mario Fabbri deposita la sentenza」）。1行目「まず、ベッルーノの
    #   予審判事…が調べた」で崩落から1968年2月までの括弧と点（札は括弧の右の端の上）／2行目（予審の説明）は足さない
    "ca11": dict(
        t="刑事の裁判", s="判事が調べる",          # ⚠️ ⑤b-6b の qa_all（echo）：「ベッルーノの予審判事」は語りの1文の一部と同じ
        fig=("axis", dict(**ss.AX_ANS, past=[ss.dot("a_fall"), ss.dot("l_parl"), ss.dot("a_parl")], start=dict(cur="1965"),
                          steps=[dict(add=[ss.ax("l_prebr"), ss.ax("l_pre")], cur="1968-02-20"), dict()],
                          src=ss.src(["S9 p2017", "S1 p98"]))),
    ),
    # ca14（8.31秒）＝一審が始まる（S9 p2017「29 novembre. Inizia all'Aquila il processo di primo grado」＝一審の言葉は c719 で説明ずみ）。
    #   1行目（聞き役）は足さない／2行目「裁判が始まるまでに、11人のうち3人が亡くなっていた」で点／3行目は足さない。
    #   亡くなった3人（S9 p2017）は語りだけ＝札にしない
    "ca14": dict(
        t="裁判の前に", s="ラクイラの裁判所",
        fig=("axis", dict(**ss.AX_ANS, past=[ss.dot("a_fall"), ss.dot("l_parl"), ss.dot("a_parl"), ss.ax("l_prebr"),
                                             ss.ax("l_pre")], start=dict(cur="1968-02-20"),
                          steps=[dict(), dict(add=ss.ax("l_start"), cur="1968-11-29"), dict()],
                          src=ss.src(["S9 p2017"]))),
    ),
    # ca15（9.77秒）＝一審の判決（S9 p2018「Non viene riconosciuta la prevedibilità della frana」・ビアデーネ・バティーニ・ヴィオリンの3人が
    #   有罪＝知らせず・避難を始めなかった）。1行目で点と札「予見できたとは認めず」／2行目で札「3人が有罪」
    "ca15": dict(
        t="最初の判決", s="予見をどう見たか",
        fig=("axis", dict(**ss.AX_ANS, past=[ss.dot("a_fall"), ss.dot("l_parl"), ss.dot("a_parl"), ss.dot("l_pre"),
                                             ss.ax("l_start", anchor="end")], start=dict(cur="1968-11-29"), steps=[
            dict(add=ss.ax("l_j1", chips=["予見できたとは認めず"]), cur="1969-12-17"),
            dict(add=dict(k="chips", at="1969-12-17", chips=["3人が有罪"], rec="S9 p2018", i0=1))],
            src=ss.src(["S9 p2018"]))),
    ),
    # ca16（11.18秒）＝控訴審の判決（S9 p2018「riconosciuti colpevoli di frana, inondazione e degli omicidi」）。1行目「2度目の裁判、控訴審」
    #   で点／2行目「崩落も、水があふれたことも、人々が亡くなったことも、罪とされた」で札／3行目（聞き役）は足さない
    "ca16": dict(
        t="判断が変わる", s="2度目の裁判",
        fig=("axis", dict(**ss.AX_ANS, past=[ss.dot("a_fall"), ss.dot("l_parl"), ss.dot("a_parl"), ss.dot("l_pre"),
                                             ss.dot("l_start"), ss.ax("l_j1", anchor="end")], start=dict(cur="1969-12-17"),
                          steps=[dict(add=ss.ax("l_j2"), cur="1970-10-03"),
                                 dict(add=dict(k="chips", at="1970-10-03", chips=["崩落もあふれた水も罪に"], rec="S9 p2018")),
                                 dict()],
                          src=ss.src(["S9 p2018"]))),
    ),
    # ca17（12.88秒）＝控訴審の結果（S9 p2018＝有罪2人〈ビアデーネ・センシドーニ〉・無罪5人〈フロジーニ・ヴィオリン・マリン・トニーニ・
    #   ゲッティ〉・病気で外れた1人〈バティーニ〉）。同じ形で並べる・名前は語りだけ・顔は描かない。1行目で有罪／3行目で無罪と外れた1人
    "ca17": dict(
        t="控訴審の結果", s="1970年10月",
        fig=("boxes", dict(view="row", slots=3, steps=[
            dict(add=ss.cause("ap_guilty")), dict(), dict(add=[ss.cause("ap_free"), ss.cause("ap_out")])],
            src=ss.src(["S9 p2018"]))),
    ),
    # ca18（10.88秒）＝破毀院の判決（S9 p2018「15-25 marzo. Processo di Cassazione a Roma: … colpevoli di un unico disastro: inondazione
    #   aggravata dalla previsione dell'evento compresa la frana e gli omicidi」）。🔴 PLAN の出典 S2 p.718 は照らせない＝S9 p2018。
    #   1行目「ローマの破毀院。イタリアの最高裁判所だ」で点／2行目で札「崩落も含めて1つの災害」／3行目で札「予見していた重い過失」
    #   （④' の G5-04＝「予見できた」でなく「予見していた」）
    "ca18": dict(
        t="最高裁判所の判断", s="ローマで",
        fig=("axis", dict(**ss.AX_ANS, past=[ss.dot("a_fall"), ss.dot("l_parl"), ss.dot("a_parl"), ss.dot("l_pre"),
                                             ss.dot("l_start"), ss.dot("l_j1"), ss.ax("l_j2", anchor="end")],
                          start=dict(cur="1970-10-03"), steps=[
            dict(add=ss.ax("l_j3"), cur="1971-03-25"),
            dict(add=dict(k="chips", at="1971-03-25", chips=["崩落も含めて1つの災害"], rec="S9 p2018")),
            dict(add=dict(k="chips", at="1971-03-25", chips=["予見していた重い過失"], rec="S9 p2018", i0=1))],
            src=ss.src(["S9 p2018", "S10 p3020"]))),
    ),
    # ca19（9.89秒）＝判決（財団の年表 S9 p2018 が記す＝伊語の原文）。1行目（聞き役）で紙／2行目「崩れることまで含めて、危ないと分かって
    #   いながら、という重い形だ」で破毀院の欄／3行目「最初の判決から、予見についての答えは、大きく変わった」で一審の欄（同じ頁の1969年）。
    #   🔴 PLAN の出典 S2 p.718 は照らせない（映像方針 §16）
    "ca19": dict(
        t="変わった答え", s="イタリア語の原文",
        fig=("boxes", dict(view="form", form=ss.FORM_JUDG, steps=[
            dict(add=dict(k="paper")), dict(add=dict(k="fill", f="破毀院")), dict(add=dict(k="fill", f="一審"))],
            note="欄の字は原文のまま・様式は再現", src=ss.src(["S9 p2018"]))),
    ),
    # ca21（4.66秒）＝時効（崩落の7年半後＝S9 p2018・S10 p3020）。崩落から時効までの括弧と点（札は点の下の項目の札「時効」＝破毀院の
    #   判決の点と約7画素しか離れない）。「あと15日で」＝2つの点が触れるほど近いことで見せる（数字は書かない）
    "ca21": dict(
        t="7年半の期限", s="時効まで",
        fig=("axis", dict(**ss.AX_ANS, past=[ss.dot("a_fall"), ss.dot("l_parl"), ss.dot("a_parl"), ss.dot("l_pre"),
                                             ss.dot("l_start"), ss.dot("l_j1"), ss.dot("l_j2"), ss.ax("l_j3")],
                          start=dict(cur="1971-03-25"),
                          steps=[dict(add=[ss.ax("l_presbr"), ss.ax("l_pres", chips=["時効"])], cur="1971-04-09")],
                          src=ss.src(["S9 p2018", "S10 p3020"]))),
    ),
    # ca22（9.28秒）＝刑の重さ（S9 p2018・S10 p3020＝ビアデーネ 5年うち3年免除・センシドーニ 3年8か月うち3年免除）。言い渡された刑と
    #   恩赦で免除の2つの群（尺は同じ）・人で色を分ける。1行目でビアデーネ／2行目でセンシドーニ／3行目（恩赦の説明）は足さない
    "ca22": dict(
        t="刑の重さ", s="破毀院の判決",
        fig=("qty", dict(view="bar", groups=[ss.QG["sentence"], ss.QG["pardon"]], steps=[
            dict(add=[ss.qb("j_bia"), ss.qb("p_bia")]), dict(add=[ss.qb("j_sen"), ss.qb("p_sen")]), dict()],
            note="3年8か月は約3.7年", src=ss.src(["S9 p2018", "S10 p3020"]))),
    ),
    # ca25（9.86秒）＝その後の裁判（S9 p2018「1975 16 dicembre. La Corte d'appello dell'Aquila rigetta la richiesta del comune di
    #   Longarone … condannando viceversa l'ENEL al risarcimento dei danni subiti dalle pubbliche amministrazioni」）。軸を1977年まで
    #   （ss.AX_CIV）＝罪を問う裁判（1968年11月〜1971年3月）を沈めて残す。1行目で点と札「エネルに償いを命じる」／2行目で札「町の訴えは退ける」
    "ca25": dict(
        t="その後の裁判", s="償いのお金をめぐって",
        fig=("axis", dict(**ss.AX_CIV, past=[ss.ax("v_crim")], start=dict(cur="1971-03-25"), steps=[
            dict(add=ss.ax("v_1975", chips=["エネルに償いを命じる"]), cur="1975-12-16"),
            dict(add=dict(k="chips", at="1975-12-16", chips=["町の訴えは退ける"], rec="S9 p2018", i0=1))],
            src=ss.src(["S9 p2018"]))),
    ),

    # ── 🆕 ⑤b-8（2026-10-02）：決め所 ca05・ca20・流れ図 ca13・Google Earth⑥ の替え ca26 ──
    # S1 p178（多数派の結論）「l'evento, così come si è manifestato, non fu previsto da nessuno」。19対8＝S1 p26（c110 と同じ）
    "ca05": dict(
        t="多数派の結論",
        s="19対8で決まった報告",
        fig=("quote", dict(phrase=["起きたとおりの形では、", "誰も予見しなかった"], rows=ss.qrows("S1", "PDF 178頁"), paper=True)),
    ),
    # ca13（9.54秒）＝裁判の場所。🔴 PLAN は地図 drift だったが、ベッルーノとラクイラの距離・座標は資料に無い（S1・S8・S9・S10 を
    #   「km・chilometri・座標」で引いた）＝門番 check_drift ③ を正直には通せない → 移った流れを流れ図で＝映像方針 §18。
    #   S10 p3019「Il processo, che avrebbe dovuto svolgersi a Belluno, fu invece sottratto al giudice naturale di quel Tribunale e
    #   trasferito per «rimessione» al Tribunale dell'Aquila su ordinanza della Cassazione adducendo il motivo di «legitima suspicione»,
    #   dovuta ad un'ipotesi di turbamento dell'ordine pubblico per esacerbazione degli stati d'animo della popolazione, e per
    #   conseguenza ad una mancata serenità dei giudici」。1行目＝ベッルーノ（地元）→ ラクイラ／2行目＝理由の箱「住民の気持ちの高ぶり」
    #   （esacerbazione degli stati d'animo della popolazione＝⚠️ ⑤b-8 の echo：「落ち着いた裁判ができないおそれ」は字幕の複写）／
    #   3行目＝理由の箱に「最高裁判所が挙げた理由」（語りの呼び名＝最高裁判所。破毀院と同じ）
    "ca13": dict(
        t="裁判の場所",
        s="移された裁判",
        fig=("boxes", dict(
            view="flow",
            steps=[dict(add=[dict(k="role", id="bl", t="ベッルーノの裁判所", pos=(160, 700), y=430, rec="S10 p3019"),
                             dict(k="role", id="aq", t="ラクイラの裁判所", pos=(1220, 1760), y=430, rec="S10 p3019"),
                             dict(k="edge", fr="bl", to="aq"),
                             dict(k="chip", at="bl", t="地元", dy=70, rec="S10 p3019")]),
                   dict(add=dict(k="role", id="why", t="住民の気持ちの高ぶり", pos=(660, 1260), y=650, rec="S10 p3019")),
                   dict(add=dict(k="chip", at="why", t="最高裁判所が挙げた理由", dy=72, rec="S10 p3019"))],
            src=ss.src(["S10 p3019"]))),
    ),
    # S10 p3020「la sentenza finale della Cassazione venne emessa nel marzo 1971, a soli 15 giorni dalla data che avrebbe fatto scattare
    #   la prescrizione dei reati」・「ritenne colpevoli soltanto due imputati su 11 che erano stati inizialmente rinviati a giudizio」
    "ca20": dict(
        t="最後の判決",
        s="1971年3月の破毀院",
        fig=("quote", dict(phrase=["時効の15日前。", "11人のうち有罪は2人"], rows=ss.qrows("S10", "PDF 20頁"), paper=True)),
    ),
    # ca26（5.09秒）＝Google Earth⑥ の替え。昼の VA west（峡谷の出口とロンガローネ＝次の ca27 はロンガローネから峡谷ごしに見る
    #   いまのダムの写真）。崩れたあとの塊と崩れた範囲・町の建物の面（建て直された町＝泥の色にしない・壊れる部品は使わない＝
    #   門番 ⑫）。1行目＝そのまま／2行目＝札（c823 と同じ位置）と峡谷の出口へゆっくり寄る。語りは判決の話＝谷の絵は場所の目印
    # 🔴 ⑤c'（2026-10-02）：寄りの中心を峡谷の出口（画面 808, 451）に置くと、1.06倍でカッソの村が上へ押され、縞の最上段が y148
    #   ＝右上の章の札の字の下端と同じ行に重なった（画素で測った）→ 中心を峡谷の出口の真上・カッソの上の端の高さ（808, 164）に＝
    #   村は上へ動かない（c717・c823 と同じ 16px のすき間）・峡谷の出口へは縦に寄る
    "ca26": dict(
        fig=("illu", dict(
            place="VA", start=dict(view="west", tod="day", block="on", slide="on"), camc=(808.4, 163.7),
            rec="S1 p147（1つの塊のまま）・S8 p1046（水平に300〜400m）",
            steps=[dict(),
                   dict(state=dict(cam=1.06), delay=0.2, dur=3.4,
                        tag=[dict(t="峡谷の出口", at="gorge_exit", off=(30, -80), keep=True),
                             dict(t="ロンガローネ", at="longarone", off=(-30, -80), anchor="end", keep=True)])])),
    ),
}
