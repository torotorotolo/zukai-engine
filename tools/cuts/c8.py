# -*- coding: utf-8 -*-
"""第8章　観客席の62分 c801–c822（22カット）。15本目（リノ・エアレース2011）。

■ 🔴 2026-09-30（⑤b-1）：14本目（セウォル号）の中身を空にした＝git の `dc6ecf4`（`git show dc6ecf4:tools/cuts/c8.py`）。
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
    "c801": dict(kind='写真',
               plan='台本の画：実写 E70 ピットの機体の奥の満員の観客席（遠景・2011-09-16 の昼＝13:19 は推定の時刻＝副題に分を書かない・観客の撮影・額装）',
               src='AAB p19'),
    "c802": dict(kind='再現イラスト',
               plan='【案C 戻り】絵（案C）を戻す：D の機体に「操縦していた人」の名前と歳の札（人は描かない）／D の機体でエンジンとプロペラに札／A を動かさずに戻す（×・人なし・数は字幕だけ）（映像方針 §11-2＝案B）｜台本の画：panel 人数｜⚠️ A の×を動かさずに出すだけ（人数を絵で名乗らない・数は字幕だけ）（映像方針 §11-2）',
               src='AAB p10 注4'),
    "c803": dict(kind='パネル',
               plan='台本の画：panel 資料で割れる数（札：報告書＝少なくとも16人／勧告書の仮の数＝66人）',
               src='AAB p10 注4・勧告書 A-12-08 p1・報道'),
    "c804": dict(kind='図解',
               plan='【帯】時間の帯（秒・分・日＝c312 の帯を広げる）：横転の約8秒前／9秒を並べた資料（写真・映像・テレメトリー）／3時間と3回／約23分と「終えた」／午後4時26分〜62分／実況の担当（マイクの印・人は描かない）／6月2日の机上訓練／5月25日の訓練（映像方針 §11-2＝案B）｜台本の画：panel 午後4時26分',
               src='AAB p20'),
    "c805": dict(kind='図・写真の頁',
               plan='台本の画：図 p19（#33 図14＝大会の救護の配置〈事前の計画・当日の動きではない〉・頁ごと）',
               src='#33 p19・AAB p20'),
    "c806": dict(kind='図解',
               plan='【帯】時間の帯（秒・分・日＝c312 の帯を広げる）：横転の約8秒前／9秒を並べた資料（写真・映像・テレメトリー）／3時間と3回／約23分と「終えた」／午後4時26分〜62分／実況の担当（マイクの印・人は描かない）／6月2日の机上訓練／5月25日の訓練（映像方針 §11-2＝案B）｜台本の画：panel 実況の担当',
               src='AAB p20'),
    "c807": dict(kind='パネル',
               plan='台本の画：panel 毛布と幕',
               src='AAB p21 注26'),
    "c808": dict(kind='パネル',
               plan='台本の画：panel 携帯と無線',
               src='AAB p20'),
    "c809": dict(kind='図解',
               plan='【帯】時間の帯（秒・分・日＝c312 の帯を広げる）：横転の約8秒前／9秒を並べた資料（写真・映像・テレメトリー）／3時間と3回／約23分と「終えた」／午後4時26分〜62分／実況の担当（マイクの印・人は描かない）／6月2日の机上訓練／5月25日の訓練（映像方針 §11-2＝案B）｜台本の画：panel 3か月半前の訓練',
               src='AAB p21'),
    "c810": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='AAB p21'),
    "c811": dict(kind='図解',
               plan='【地図】地図 drift：3つの距離（152・228・266メートル）と命令・通達（152／305メートル）＝どちらの内か／オカラ・アリゾナ・テキサス・ミンデン／オカラから半径約161キロと機体の居場所／州道395号を止める／その後の配置（コースを北へ・燃料車を約2.4キロ先へ）（映像方針 §4）｜台本の画：panel 州道395号',
               src='AAB p21'),
    "c812": dict(kind='図解',
               plan='【地図】地図 drift：3つの距離（152・228・266メートル）と命令・通達（152／305メートル）＝どちらの内か／オカラ・アリゾナ・テキサス・ミンデン／オカラから半径約161キロと機体の居場所／州道395号を止める／その後の配置（コースを北へ・燃料車を約2.4キロ先へ）（映像方針 §4）｜台本の画：panel 決めごとの実行',
               src='AAB p21'),
    "c813": dict(kind='図解',
               plan='【帯】時間の帯（秒・分・日＝c312 の帯を広げる）：横転の約8秒前／9秒を並べた資料（写真・映像・テレメトリー）／3時間と3回／約23分と「終えた」／午後4時26分〜62分／実況の担当（マイクの印・人は描かない）／6月2日の机上訓練／5月25日の訓練（映像方針 §11-2＝案B）｜台本の画：panel 5月25日の総合訓練',
               src='AAB p21'),
    "c814": dict(kind='図・写真の頁',
               plan='台本の画：図 p15（#33 図13＝駐機場の斜めの空撮・燃料車・頁ごと）',
               src='#33 p14・p15・AAB p19・p46'),
    "c815": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='AAB p46'),
    "c816": dict(kind='再現イラスト',
               plan='【案C】C（柵だけ）：駐機場の側から低い位置で、ボックス席の前のパイプと幕・ピットの前の低い金属の柵。人の高さより下で切る｜人：なし（映像方針 §3-2）｜⚠️ p20（柵の場所）・p21 注26（幕の色）',
               src='AAB p20・p46'),
    # 🔴 ⑤b-6（2026-09-30 カズヤくん「地図に替える」）：Googleアースは使わない → 地図（c819・c820 の地図の最初の段）
    "c817": dict(kind='図解',
               plan='【地図】駐機場・ショーライン・ボックス席（c819・c820 の地図 drift の最初の段）｜元の画＝実写 Googleアース 駐機場とボックス席のあった場所（現在・別の角度）＝09-30 カズヤくん「地図に替える」',
               src='AAB p17・p19'),
    "c818": dict(kind='文字の頁',
               plan='台本の画：図 p17（報告書の頁・2つの資料の食い違い・頁ごと）',
               src='AAB p17'),
    "c819": dict(kind='図解',
               plan='【地図】地図 drift：3つの距離（152・228・266メートル）と命令・通達（152／305メートル）＝どちらの内か／オカラ・アリゾナ・テキサス・ミンデン／オカラから半径約161キロと機体の居場所／州道395号を止める／その後の配置（コースを北へ・燃料車を約2.4キロ先へ）（映像方針 §4）｜台本の画：panel 1990年から改められていない通達',
               src='AAB p17・p19'),
    "c820": dict(kind='図解',
               plan='【地図】地図 drift：3つの距離（152・228・266メートル）と命令・通達（152／305メートル）＝どちらの内か／オカラ・アリゾナ・テキサス・ミンデン／オカラから半径約161キロと機体の居場所／州道395号を止める／その後の配置（コースを北へ・燃料車を約2.4キロ先へ）（映像方針 §4）｜台本の画：panel 266メートルと228メートルは、どちらの内か',
               src='勧告書 A-12-08 p3・AAB p17・p19'),
    "c821": dict(kind='パネル',
               plan='台本の画：panel NTSBが求めたこと',
               src='AAB p46'),
    "c822": dict(kind='パネル',
               plan='台本の画：panel 橋',
               src='—'),
}

SPEC = {

    # ── 🔴 ⑤b-6（2026-09-30）：写真と頁の束（`qa_out/ep15_assets.py`）──
    # E70＝事故の日の昼（9/16 現地）・ピットのジェット機「67」の奥に満員のスタンド（遠景＝§9 の「遠景の観客席は可」）。
    #   ⚠️ 13:19 は EXIF から推した時刻＝副題に分を書かない（PLAN）。640px のシートで見て、手前の主役はジェット機と分かった
    "c801": dict(
        t="満員の観客席",
        s="2011年9月16日の昼　ピットの機体と奥のスタンド（観客の撮影）",
        photo=P("stands_0916"), panel=True, color=1.0,
        card_mix=0,     # 🔴 ⑤c'：BY-SA は扉の地に混ぜない（染める・拡大する＝翻案・左端の私人も大きくなる）＝ss.check_card_mix・§5b-110
    ),
    # #33 図14（p19＝p2019）＝大会の救護の配置（事前の計画＝当日の動きではない）
    "c805": dict(
        t="救護の配置",
        s="NTSB 資料の図14（大会の前に決めた配置）",
        photo=ss.page(2019), trim=ss.ptrim("c805"), panel=True, color=1.0,
    ),
    # #33 図13（p15＝p2015）＝駐機場の斜めの空撮（燃料車・ピット・ボックス席・事故の地点）
    "c814": dict(
        t="駐機場の空撮",
        s="NTSB 資料の図13（燃料車・ピット・ボックス席）",
        photo=ss.page(2015), trim=ss.ptrim("c814"), panel=True, color=1.0,
    ),
    # 報告書（p17）＝FAA の2つの手引きの食い違い（「…require a distance of 500 feet…」の行を真ん中に＝1,000フィートの行も入る）
    "c818": dict(
        t="2つの手引き",
        s="報告書 1.5　命令と通達の比べ",
        photo=ss.page(17), trim=ss.ptrim("c818"), panel=True, color=1.0,
    ),

    # ── 🔴 ⑤b-5（2026-09-30）：型の使い回し（14本目の `axis` 時刻の帯・年表／`boxes` 流れ図）──
    # 午後4時26分の宣言（時刻の帯）：事故（16:24＝台本 c317 の 4時24分38秒ごろ・AAB p28 の表）は沈んで残り、1行目＝16:26 の宣言。
    #   2行目（言葉の意味）は字幕だけ
    "c804": dict(
        t="午後4時26分",
        s="救急の組織の判断",
        fig=("axis", dict(**ss.AX_EMS, past=[ss.ax("t1624")], start=dict(cur="16:24"),
                          steps=[dict(add=ss.ax("t1626"), cur="16:26"), dict()],
                          note="時刻の帯（報告書の値）", src=ss.src(["AAB p20・p28"]))),
    ),
    # 実況の担当（流れ図・人の形は描かない）：1行目＝観客へ避難の案内／2行目＝救護の人を手伝う・医療の応援を頼む（AAB p20）
    "c806": dict(
        t="落ち着いた案内",
        s="事故のすぐ近くで",
        fig=("boxes", dict(view="flow", layout=ss.MC,
                           steps=[dict(add=[ss.MCP["a_evac"], dict(k="edge", fr="mc", to="a_evac")]),
                                  dict(add=[ss.MCP["a_help"], ss.MCP["a_med"], dict(k="edge", fr="mc", to=["a_help", "a_med"])])],
                           note="報告書の文を短くしたもの", src=ss.src(["AAB p20"]))),
    ),
    # 3か月半前の訓練（年表 AX_DRILL）：1行目（聞き役）＝事故の点だけ／2行目＝2011年6月2日の机上訓練と事故までの括弧／
    #   3行目＝参加した機関の札（主催の団体・FAA・消防・警察・病院など）
    "c809": dict(
        t="備えはあった",
        s="大事故の対応の練習",
        fig=("axis", dict(**ss.AX_DRILL, start=dict(cur="2011-09-16"),
                          steps=[dict(add=ss.ax("d_acc")),
                                 dict(add=[ss.ax("tabletop"), ss.ax("drill_br")], cur="2011-06-02"),
                                 dict(add=dict(k="chips", at="2011-06-02", chips=["主催の団体・FAA", "消防・警察・病院など"],
                                               rec="AAB p21"))],
                          note="年表（報告書の値）", src=ss.src(["AAB p10・p21"]))),
    ),
    # 5月25日の総合訓練（同じ年表）：机上訓練（沈む）の前に、リノの別の空港での訓練（AAB p21）
    "c813": dict(
        t="その前の週にも",
        s="3年に1度の大きな訓練",
        fig=("axis", dict(**ss.AX_DRILL, past=[ss.ax("tabletop"), ss.ax("d_acc")], start=dict(cur="2011-06-02"),
                          steps=[dict(add=ss.ax("fullscale"), cur="2011-05-25")],
                          note="年表（報告書の値）", src=ss.src(["AAB p10・p21"]))),
    ),

    # ── 🔴 ⑤b-2（2026-09-30）：案C の戻り（`tools/illu.py` の RA＝15本目）──
    # A を動かさずに戻す：×とボックス席だけ（人なし・亡くなった方とけがの人の数は字幕だけ＝映像方針 §11-2・§5b-9）。
    #   カメラはごくゆっくり引くだけ（1.06→1.0＝2.36〜2.5メートル／画素）。航跡・点線は出さない（数の話＝落ちた道は c101・c102）
    "c802": dict(
        fig=("illu", dict(
            place="RA", at="16:24", start=dict(view="near", x="on", box="on", cam=1.06), camc="x",
            rec="AAB p19（観客のボックス席に落ちた）・p11（図1＝事故地点）",
            steps=[dict(tag=dict(t="観客席（ボックス席）", at="box", off=(60, -110), keep=True)),
                   dict(state=dict(cam=1.03), dur=3.0), dict(state=dict(cam=1.0), dur=3.0)])),
    ),

    # ── 🔴 ⑤b-3（2026-09-30）：C の柵だけ（`tools/illu.py` の RC＝fences）──
    # 2つの柵の寄りを低い位置から（左＝ピットの前の低い金属の柵・右＝ボックス席の前の幕を付けたパイプ＝AAB p20・幕の色 p21 注26）。
    #   落ちたあとの章＝人を描かない（線2）。柵の奥は**ぼかした面**（人も物も描かない＝空っぽの席にも見せない）。
    #   柵の形・高さ・幕の色の並びは模式（左下の断り）。2・3行目は報告書の結論＝ごくゆっくり寄るだけ
    "c816": dict(
        fig=("illu", dict(
            place="RC", start=dict(view="fences"),
            # ⚠️ 下見：札を柵の上に置き、寄り（cam）で札が上へ動くと、左上の見え方の名・右上の章の札に重なった
            #    ＝札は柵の下（手前の舗装の上）・寄りはしない
            steps=[dict(tag=[dict(t="低い金属の柵（ピットの前）", at="fence", off=(-360, 350), keep=True, delay=0.4),
                             dict(t="幕を付けたパイプ（ボックス席の前）", at="curtain", off=(-420, 300), keep=True, delay=0.4)]),
                   dict(), dict()])),
    ),

    # ── 🔴 ⑤b-7（2026-09-30）：パネル・決め所・地図（`ss.town_map`・`ss.ramp_map`）──
    # 資料で割れる数（AAB p10 注4＝少なくとも16人・4つの病院のうち1つなどから限られた情報／勧告書 A-12-08 p1（2012年4月）
    #   「based on preliminary information, 66 people sustained serious injuries」）。🔴 66人は札だけ（語りで読まない＝16と66の
    #   聞き違えを避ける＝台本 §1-5）。報道の数（56・69・70人超）は出さない（「日を追って変わった」だけ）
    "c803": dict(
        t="重いけがの人数",
        s="資料で割れる数",
        fig=("panel", dict(
            blocks=[dict(k="報告書（2012年8月）", t="少なくとも16人", v="限られた情報から", c=J.DOC),
                    dict(k="勧告書（2012年4月）", t="66人", v="仮の数", c=J.INST),
                    dict(k="報道", t="日を追って変わった", c=J.LINE)],
            cols=3)),
    ),
    # 毛布と幕（AAB p21 注26）
    "c807": dict(
        t="その場にあった物",
        s="報告書 21頁の注26",
        fig=("panel", dict(
            blocks=[dict(k="空港の車から", t="黄色の毛布", c=J.AMBER),
                    dict(k="ボックス席から", t="青と赤の幕", c=J.INST)],
            cols=2)),
    ),
    # 携帯と無線（AAB p20「some loss of service for about 15 to 20 minutes」・救護は無線で影響なし）
    "c808": dict(
        t="連絡の手段",
        s="報告書 20頁",
        fig=("panel", dict(
            blocks=[dict(k="携帯電話", t="つながりにくい", v="15〜20分ほど", c=J.AMBER),
                    dict(k="救護の連絡", t="無線", v="影響なし", c=J.OK)],
            cols=2)),
    ),
    # 決め所⑭（台本 §2 #14）。AAB p21 §1.9.2「The scenario for the exercise had been for 23 fatalities with an additional
    #   46 injured」（机上訓練＝2011年6月2日）。死の語は「亡くなる人」（§B2-4）
    "c810": dict(
        t="机上訓練",
        s="2011年6月2日",
        fig=("quote", dict(
            phrase=["訓練の想定は", "亡くなる人23人、負傷46人"],
            rows=[("記録", "NTSB 事故報告 AAB-12/01（2012年）", J.INK_W),
                  ("頁", "PDF 21頁（1.9.2）", J.TICK)], paper=True)),
    ),
    # 地図：州道395号（AAB p21「State Highway 395 would be shut down to allow better travel time for multiple ambulances」）。
    #   1行目＝空港と町を結ぶ線（道の形は記録に無い＝直線の模式）と札／2行目＝点が空港から町へ動く（行き来しやすく）
    "c811": dict(
        t="救急車の道",
        s="訓練のあとの決めごと",
        fig=ss.town_map([
            dict(route=dict(via=["reno_stead", "reno_city"], col=J.AMBER, sw=5), tag=dict(at="hw_mid", t="州道395号", side="right")),
            dict(move=[dict(kind="path", via=["reno_stead", "reno_city"], sec=3.0)])],
            note="模式図：道の線は空港と町を直線で結んだもの（実際の道の形ではない）", recs=("AAB p21", "#17 p7008")),
    ),
    # 地図：事故の日に使われた（AAB p21「this decision was put into practice for the accident response」・#33 p2021）
    "c812": dict(
        t="事故の日",
        s="決めごとの実行",
        fig=ss.town_map([
            dict(route=dict(via=["reno_stead", "reno_city"], col=J.AMBER, sw=5), tag=dict(at="hw_mid", t="州道395号", side="right")),
            dict(move=[dict(kind="path", via=["reno_stead", "reno_city"], sec=3.0)],
                 tag=dict(at="reno_stead", t="2011年9月16日", side="left"))],
            note="模式図：道の線は空港と町を直線で結んだもの（実際の道の形ではない）", recs=("AAB p21", "#33 p2021", "#17 p7008")),
    ),
    # 決め所⑮（台本 §2 #15）。AAB p46 §2.6.4「although the fuel truck parked on the ramp was not hit by any debris from the
    #   accident airplane, the outcome could easily have been different」
    "c815": dict(
        t="燃料車",
        s="報告書の注意",
        fig=("quote", dict(
            phrase="燃料車は、たやすく別の結果になり得た",
            rows=[("記録", "NTSB 事故報告 AAB-12/01（2012年）", J.INK_W),
                  ("頁", "PDF 46頁（分析）", J.TICK)], paper=True)),
    ),
    # 地図（Googleアースの代わり＝09-30 カズヤくん）：駐機場とショーライン（c819・c820 の最初の段と同じ絵）
    "c817": dict(
        t="駐機場とショーライン",
        s="事故の日の配置",
        fig=ss.ramp_map([ss.R_BASE, dict()]),
    ),
    # 地図：2つの端の距離（AAB p19 のピット 748フィート・ボックス席 874フィート）。1行目＝配置／2行目＝2本の寸法線
    "c819": dict(
        t="2つの端",
        s="事故の日の配置",      # ⚠️ 「ショーラインから南へ」「南への距離」は図の札・注と重なる＝check_dup
        fig=ss.ramp_map([ss.R_BASE, ss.R_DIMS]),
    ),
    # 地図：どちらの内か（勧告書 A-12-08 p3＝どちらも命令〈500フィート〉は満たし、通達〈1,000フィート〉には届かない・AAB p17）
    "c820": dict(
        t="どちらの内か",
        s="命令と通達の距離",
        fig=ss.ramp_map([
            ss.merge(ss.R_BASE, ss.R_DIMS,
                     dict(route=dict(via=["o_w", "o_e"], col=J.INST, sw=4), tag=dict(at="o_e", t="命令 152メートル", side="right")),
                     dict(route=dict(via=["a_w", "a_e"], col=J.DOC, sw=4), tag=dict(at="a_w", t="通達 305メートル", side="left"))),
            dict()],
            recs=("AAB p17", "AAB p19", "勧告書 p6003")),
    ),
    # NTSBが求めたこと（AAB p46）：2つの資料（命令と通達）の誤りと食い違いを直すよう FAA に
    "c821": dict(
        t="NTSBの求め",
        s="勧告 A-12-08",
        fig=("panel", dict(
            blocks=[dict(k="直す先", t="FAAの命令と通達", c=J.INST),
                    dict(k="直す中身", t="誤りと食い違い", c=J.AMBER)],
            cols=2)),
    ),
    # 橋（最後の章へ）：その求めが片づくまで、どれだけかかったか
    "c822": dict(
        t="片づくまで",
        s="勧告 A-12-08 の行方",
        fig=("panel", dict(
            blocks=[dict(k="求めた先", t="FAA", c=J.INST),
                    dict(k="かかった時間", t="？", v="最後の章で", c=J.AMBER)],
            cols=2)),
    ),
}
