# -*- coding: utf-8 -*-
"""第9章　その後 c901–c920（20カット）。15本目（リノ・エアレース2011）。

■ 🔴 2026-09-30（⑤b-1）：14本目（セウォル号）の中身を空にした＝git の `dc6ecf4`（`git show dc6ecf4:tools/cuts/c9.py`）。
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
    "c901": dict(kind='文字の頁',
               plan='台本の画：図 p43（報告書の頁・公聴会と勧告10件・頁ごと）',
               src='AAB p38・p43'),
    "c902": dict(kind='文字の頁',
               plan='台本の画：図 p1（勧告書 A-12-08 の1頁目の上だけ＝宛名と日付・速さ〈460ノット〉と人数の段落は映さない）',
               src='勧告書 A-12-08 p1・AAB p43'),
    "c903": dict(kind='パネル',
               plan='台本の画：panel 安全勧告とは',
               src='CAROL A-12-08'),
    "c904": dict(kind='混ざり',
               plan='【混ざり：頁 p46 → 地図 drift】1行目は頁のまま → 2行目から地図 drift（前と後）（映像方針 §5＝いまの画：図 p46（主催の団体の返事））',
               src='AAB p46・CAROL A-12-14・A-12-15'),
    "c905": dict(kind='図解',
               plan='【書類】書類の再現図（自作の用紙＝本物の頁ではない・台本 §0-3 の「記録簿・参加書類の再現図」）：記録簿の総時間／「試験はどうだったのか」／参加書類の「大きな改造をしたか □はい □いいえ」／年齢の欄／検査の用紙の備考と合格・書面で確かめる欄が無い／新しい検査の用紙（映像方針 §11-2＝案B）｜台本の画：panel 検査の用紙',
               src='CAROL A-12-10'),
    "c906": dict(kind='写真',
               plan='台本の画：実写 D5 2016年の講習会の駐機場（Don Ramey Logan・CC BY 4.0・副題に年）',
               src='CAROL A-12-11・A-12-16'),
    "c907": dict(kind='図解',
               plan='【棒】数の比べ（棒）：新幹線と事故機の速さ／この機の最高との差／2010年の平均の速さ／申告の約2,700時間と総時間 約1,453時間／約200時間と約25時間／コースの3〜4Gと17.3G（映像方針 §11-2＝案B）｜台本の画：panel Gスーツ',
               src='CAROL A-12-12・A-12-17'),
    "c908": dict(kind='パネル',
               plan='台本の画：panel 大きな改造をした機の評価',
               src='CAROL A-12-09・A-12-13'),
    "c909": dict(kind='パネル',
               plan='台本の画：panel 一から作った機との差',
               src='AAB p43'),
    "c910": dict(kind='パネル',
               plan='台本の画：panel FAA の毎年の計画書',
               src='AAB p50'),
    "c911": dict(kind='パネル',
               plan='台本の画：panel 10件のうち9件',
               src='CAROL A-12-09〜A-12-17'),
    "c912": dict(kind='パネル',
               plan='台本の画：panel 残る1件',
               src='CAROL A-12-08・AAB p46'),
    "c913": dict(kind='図解',
               plan='【年表】年表（動く年表）：1944→2011 の機体の歩み（売却・リノ・持ち主・保管18年・分解整備と改造・2010年の出場）／勧告 A-12-08 が閉じるまで（c915 自作と同じ線）（映像方針 §11-2＝案B）｜台本の画：panel 途中の3回と2020年2月',
               src='CAROL A-12-08'),
    "c914": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='CAROL A-12-08'),
    "c915": dict(kind='図解',
               plan='台本の画：図 自作 A-12-08 の経過（2012 → 2016 → 2020 → 2021・CAROL の記録から）',
               src='CAROL A-12-08'),
    "c916": dict(kind='図解',
               plan='【年表】年表（動く年表）：1944→2011 の機体の歩み（売却・リノ・持ち主・保管18年・分解整備と改造・2010年の出場）／勧告 A-12-08 が閉じるまで（c915 自作と同じ線）（映像方針 §11-2＝案B）｜台本の画：panel 2021年7月13日',
               src='CAROL A-12-08'),
    # 🔴 ⑤b-6（2026-09-30 カズヤくん「地図に替える」）：Googleアースは使わない → 地図（リノ → ロズウェル）
    "c917": dict(kind='図解',
               plan='【地図】リノ → ニューメキシコ州ロズウェル（大会の移転）｜元の画＝実写 Googleアース ステッド空港（現在）＝09-30 カズヤくん「地図に替える」',
               src='CAROL A-12-13・RARA 2024-05-23・RARA 2026-09-24'),
    "c918": dict(kind='図解',
               plan='台本の画：panel 3つの問いの答え → 事故の前にあった手がかり',
               src='AAB p15・p37・p41・p46・p52'),
    "c919": dict(kind='パネル',
               plan='台本の画：panel 報告書の言葉',
               src='AAB p41'),
    "c920": dict(kind='パネル',
               plan='台本の画：panel コメントの問い（§B3-7）',
               src='—'),
}

SPEC = {

    # ── 🔴 ⑤b-6（2026-09-30）：写真と頁の束（`qa_out/ep15_assets.py`）──
    # 報告書 2.6（p43）＝「…the NTSB's January 10, 2012, investigative hearing」の行を真ん中に（勧告10件の節）
    "c901": dict(
        t="公聴会",
        s="報告書 2.6　勧告10件の節",
        photo=ss.page(43), trim=ss.ptrim("c901"), panel=True, color=1.0,
        card_mix=0.14,  # ⑤c'（2026-09-30）：白い頁の扉は地が明るく「第9章」と題が英文に乗った（中央値 103）＝14本目 cb01 と同じ割合
    ),
    # 勧告書 A-12-08 の1頁目の上だけ（紋章・日付の欄・FAA の長官代行あての宛名）。460ノットと人数の段落は映さない（PLAN）
    "c902": dict(
        t="安全勧告",
        s="勧告書 A-12-08 の1頁目（FAAあて）",
        photo=ss.page(6001), trim=ss.ptrim("c902"), panel=True, color=1.0,
    ),
    # D5（Don Ramey Logan・CC BY 4.0）＝2016年6月17日・レースの講習会（Pylon Racing Seminar）の駐機場
    "c906": dict(
        t="選手の講習会",
        s="2016年6月　レースの講習会の駐機場",
        photo=P("seminar_2016"), **ss.kind(P("seminar_2016")),
    ),

    # ── 🔴 ⑤b-5（2026-09-30）：型の使い回し（書類の再現図・棒・年表）──
    # 新しい検査の用紙（CAROL p5010＝A-12-10）：1行目（聞き役の反応）はそのまま／2行目＝紙（指摘・直した中身・再検査の欄＝値なし）／
    #   3行目＝コースへの矢印（書面と再検査が済むまで出さない）
    "c905": dict(
        t="書面で確かめる",
        s="勧告 A-12-10 のあと",
        fig=("boxes", dict(view="form", form=ss.FORM_NEW,
                           steps=[dict(), dict(add=dict(k="paper")),
                                  dict(add=[dict(k="end", id="office"), dict(k="edge", fr="paper", to="office")])],
                           note="再現（本物の頁ではない・欄は勧告の記録の文から）", src=ss.src(["CAROL p5010"]))),
    ),
    # Gスーツ（棒）：1行目＝事故の最大 17.3G（AAB p28 の表）／2行目＝ふつうのコース 3〜4G の上の端（CAROL p5011・p5012）
    "c907": dict(
        t="Gスーツ",
        s="A-12-12・A-12-17 の答え",
        fig=("qty", dict(view="bar", groups=[ss.QG["g"]],
                         steps=[dict(add=ss.qb("g_acc")), dict(add=ss.qb("g_course"))],
                         note="ふつうのコースは3〜4G（棒は上の端）", src=ss.src(["AAB p28", "CAROL p5011・p5012"]))),
    ),
    # 勧告 A-12-08 が閉じるまで（年表 AX_A08・CAROL p5008）：事故の点は沈んで残る。1行目＝NTSB の評価3回（まだ閉じない）／
    #   2行目＝2020年2月に FAA が命令を改めた
    "c913": dict(
        t="途中の3回",
        s="NTSBの評価",
        fig=("axis", dict(**ss.AX_A08, past=[ss.ax("a08_acc")], start=dict(cur="2011-09-16"),
                          steps=[dict(add=[ss.ax("a08_1"), ss.ax("a08_2"), ss.ax("a08_3")], cur="2020-07-22"),
                                 dict(add=ss.ax("a08_order"), cur="2020-02-27")],
                          note="年表（勧告の記録から）", src=ss.src(["CAROL p5008"]))),
    ),
    # 通達の廃止の理由：2020年11月3日の点（決め所 c914 の日）と札「守らせる言い方」。2行目（新しい決まりで禁じられた＝
    #   49 CFR 5.25）は日付が記録に無い＝点にしない（字幕だけ）。前の点は札を消して沈める（札が3段に収まらない）
    "c915": dict(
        t="なぜ廃止か",
        s="通達の書き方",
        fig=("axis", dict(**ss.AX_A08,
                          past=[ss.ax("a08_acc"), ss.ax("a08_1", lab=False, t=""), ss.ax("a08_2", lab=False, t=""),
                                ss.ax("a08_3", lab=False, t=""), ss.ax("a08_order")],
                          start=dict(cur="2020-02-27"),
                          steps=[dict(add=ss.ax("a08_ac", chips=["守らせる言い方"]), cur="2020-11-03"), dict()],
                          note="年表（勧告の記録から）", src=ss.src(["CAROL p5008"]))),
    ),
    # 閉じた日：2021年7月13日の点／2行目＝事故から閉じるまでの括弧（約10年＝数は書かない）／3行目（聞き役）そのまま
    "c916": dict(
        t="勧告が閉じた日",
        s="NTSBの分類",
        fig=("axis", dict(**ss.AX_A08,
                          past=[ss.ax("a08_acc"), ss.ax("a08_1", lab=False, t=""), ss.ax("a08_2", lab=False, t=""),
                                ss.ax("a08_3", lab=False, t=""), ss.ax("a08_order", lab=False, t=""),
                                ss.ax("a08_ac", lab=False, t="")],
                          start=dict(cur="2020-11-03"),
                          steps=[dict(add=ss.ax("a08_close"), cur="2021-07-13"), dict(add=ss.ax("a08_br")), dict()],
                          note="年表（勧告の記録から）", src=ss.src(["CAROL p5008"]))),
    ),

    # ── 🔴 ⑤b-1（2026-09-30）：字幕の試し焼きに先に書いた4カット（案B で「文字のまま残す」パネル＝最終形）──
    #   選んだ理由＝字幕の型（まりさ 黄＋黒フチ／れいむ 赤＋白フチ・けいふぉんと・56px・2行 y968／1044）を
    #   語り1行・語り2行・聞き役・書体で折りが変わった行（qa_out/ep15_b1/15本目_字幕の折り_Noto→けいふぉんと.tsv）で焼いて見るため。
    #   中身は台本の言葉と数だけ（台本に無い事実を足さない）。語りの文をそのまま札にしない（check_echo）
    # c910-1＝書体で「折り目が動いた」行（AAB p50）
    "c910": dict(
        t="FAAの新しい決まり",
        s="事故の3か月後",
        fig=("panel", dict(
            blocks=[dict(k="出すもの", t="毎年の計画書", c=J.DOC),
                    dict(k="出す先", t="基地の事務所", c=J.INST)],
            cols=2)),
    ),
    # c911＝語り2行＋聞き役「つまり、ほとんどは早く片づいた？」（CAROL A-12-09〜A-12-17）
    "c911": dict(
        t="NTSBの勧告10件",
        s="その後の扱い",      # ⚠️ 最初の副題「受け入れられる対応として閉じたか」は語りの複写＝check_echo が止めた
        fig=("panel", dict(
            blocks=[dict(k="閉じた", t="9件", v="2013年までに", c=J.OK),
                    dict(k="残る", t="1件", c=J.AMBER)],
            cols=2)),
    ),
    # c912-2＝書体で「2行→1行」に変わった行（CAROL A-12-08・AAB p46）
    "c912": dict(
        t="残る1件",
        s="NTSBの勧告 A-12-08",
        fig=("panel", dict(
            blocks=[dict(k="資料1", t="FAAの命令", c=J.INST),
                    dict(k="資料2", t="FAAの通達", c=J.INST)],
            cols=2)),
    ),
    # コメントの問い（13本目から・ed01 の直前）。13本目 c920・14本目 cd08 と同じ形。「この動画」は楽屋の言葉＝画面に出さない
    "c920": dict(
        t="あなたなら、どうする",
        s="コメント欄で聞かせてください",
        fig=("panel", dict(
            blocks=[dict(k="問い1", t="どこで防げたか", c=J.AMBER),
                    dict(k="問い2", t="改造した機体に求めること", v="大会を開くなら", c=J.ALERT)],
            cols=2)),
    ),

    # ── 🔴 ⑤b-7（2026-09-30）：パネル・混ざり（頁→地図）・決め所・地図・3つの問いの答え ──
    # 安全勧告とは（CAROL A-12-08）：出す→見届ける→区切りがつくと閉じる
    "c903": dict(
        t="勧告の流れ",
        s="NTSBの安全勧告",
        fig=("panel", dict(
            blocks=[dict(k="1", t="出す", v="変えてほしいこと", c=J.INST),
                    dict(k="2", t="見届ける", v="対応", c=J.LINE),
                    dict(k="3", t="閉じる", v="区切りがつくと", c=J.OK)],
            cols=3)),
    ),
    # 混ざり：1行目＝頁 p46（主催の団体の返事・額装）のまま → 2行目から飛行場のまわりの地図（前と後）
    #   （映像方針 §4・§5＝c104 と同じ入れ替え。頁を残すので第9章の写真の割合は下がらない）。
    #   地図：コースを北へ＝矢印だけ（距離は AAB p46・CAROL A-12-14 に無い）／燃料車＝ピットの近く（AAB p19）→ 飛行場の南東の側・
    #   主な観客席から約1.5マイル（p46）／より頑丈な柵＝ピットの西の端からボックス席を通って一般の観客席まで（p46）
    "c904": dict(
        t="主催の団体の返事",
        s="2012年の大会から",
        fig=ss.field_map([
            dict(route=[dict(via=["sl_w", "sl_e"], col=J.INK_W, sw=4, dash=None),
                        dict(via=["pit_w", "pit_e"], col=J.LINE, sw=6, dash=None),
                        dict(via=["box_w", "box_e"], col=J.LINE, sw=6, dash=None)],
                 arrow=dict(a="reno_stead", b="cn1"),
                 tag=[dict(at="cn1", t="コースを北へ", side="right"), dict(at="box", t="観客席", side="below")]),
            # 🔴 ⑤c'（2026-09-30）：前→後を直線で結ぶと道が札「観客席」（ボックス席の下）の真ん中を斜めに通った（原寸）
            #    → 南へ回してから南東へ（途中の点 fuelm＝道の形は記録に無い＝注の「模式」のうち）。門番 check_drift ⑤
            dict(move=[dict(kind="path", via=["fuel0", "fuelm", "fuel1"], sec=2.5)],
                 dim=dict(a="box", b="fuel1", t="約2.4キロ"),
                 tag=[dict(at="fuel0", t="燃料車（前）", side="left"), dict(at="fuel1", t="燃料車（後）", side="right")]),
            dict(route=dict(via=["pbw", "grand"], col=J.OK, sw=9, dash=None),
                 tag=dict(at="grand", t="より頑丈な柵", side="right"))]),
        intro=dict(photo=ss.page(46), trim=ss.ptrim("c904"), panel=True, color=1.0, until=1),
    ),
    # 大きな改造をした機の評価（CAROL A-12-09・A-12-13）
    "c908": dict(
        t="改造した機体",
        s="勧告 A-12-09・A-12-13 のあと",
        fig=("panel", dict(
            blocks=[dict(k="出場の条件", t="技術の評価", c=J.OK),
                    dict(k="無制限クラスの団体", t="仕様の決まりを書き直し", c=J.OK)],
            cols=2)),
    ),
    # 一から作った機との差（AAB p43）
    "c909": dict(
        t="それまでの差",
        s="報告書 43頁",
        fig=("panel", dict(
            blocks=[dict(k="一から作った機体", t="フラッターの試験", v="対象", c=J.OK),
                    dict(k="改造した昔の戦闘機", t="対象の外", c=J.ALERT)],
            cols=2)),
    ),
    # 決め所⑯（台本 §2 #16）。NTSB から FAA への手紙（CAROL p5008・2021年7月13日）「on November 3, 2020, you cancelled
    #   AC 91-45C because it contained mandatory language」＝改訂でなく廃止
    "c914": dict(
        t="通達の行方",
        s="勧告 A-12-08 の結び",
        fig=("quote", dict(
            phrase="通達は直さず、2020年11月3日に廃止",
            rows=[("記録", "NTSB 安全勧告の記録（CAROL）", J.INK_W),
                  # ⑤c'：「NTSBからFAAへ（2021年／7月13日）」と日付が行で割れた＝日付を欄に分ける
                  ("手紙", "NTSBからFAAへ", J.LINE),
                  ("日付", "2021年7月13日", J.LINE)], paper=True)),
    ),
    # 地図（Googleアースの代わり＝09-30 カズヤくん）：大会の移転（翌年もリノ＝CAROL p5013／2024年5月に発表・2025年からロズウェル＝
    #   主催の団体 RARA の発表）。1行目＝2024年5月の発表／2行目＝ロズウェルへ動く点と「2025年から」
    "c917": dict(
        t="大会の移転",
        s="開かれる場所",
        fig=ss.usa_map([
            # ⚠️ 最初の札「2024年5月 移転の発表」は語りの複写＝check_echo が止めた
            dict(tag=dict(at="reno_stead", t="2024年5月に発表", side="left")),
            dict(route=dict(via=["reno_stead", "reno_roswell"]),
                 move=[dict(kind="path", via=["reno_stead", "reno_roswell"], sec=3.0)],
                 tag=dict(at="reno_roswell", t="2025年から", side="right"))],
            places=[dict(k="reno_stead", side="above"), "reno_roswell"],
            note="模式図：地点は緯度経度から（ロズウェルは町の中心）",
            recs=("CAROL p5013", "#17 p7008"), extra="・主催の団体 RARA の発表（2024年5月23日）"),
    ),
    # 3つの問いの答え（台本 c918）＝c109 の3つの問いの名を上に・1行目＝答え3つ／2行目＝区切りの線の下に、事故の前にあった
    #   手がかり3つ（答えとは矢印でつながない＝台本は組にしていない）／3行目＝手がかりの見出し。
    #   ⚠️ 映像方針 §4 の「模式図と2つの資料の頁を小さく戻す」は型が無い（新しい型は予算の外＝§11-3）＝箱の型の使い回しで
    #   ⚠️ 最初の見出し「3つの問いの答え」は語りの1行目の頭と同じ＝check_echo が止めた
    "c918": dict(
        t="答えと手がかり",
        s="3つの問いから",
        fig=("boxes", dict(view="flow", layout=ss.ANS,
                           steps=[dict(add=[ss.ANSP["a1"], ss.ANSP["a2"], ss.ANSP["a3"]] + ss.ans_links()),
                                  dict(add=[dict(k="rule", y=585), ss.ANSP["k1"], ss.ANSP["k2"], ss.ANSP["k3"]]),
                                  dict(add=dict(k="grp", t="事故の前の手がかり", x=160, y=640))],
                           note="箱は報告書の言葉を短くしたもの", src=ss.src(["AAB p15", "AAB p17", "AAB p37", "AAB p41", "AAB p52"]))),
    ),
    # 報告書の言葉（AAB p41）：傷んだ部品を見つけて替える機会はあった
    "c919": dict(
        t="報告書の言葉",
        s="41頁",
        fig=("panel", dict(
            blocks=[dict(k="傷んだ部品", t="見つけて替える機会", c=J.AMBER),
                    dict(k="報告書", t="あった", c=J.DOC)],
            cols=2)),
    ),
}
