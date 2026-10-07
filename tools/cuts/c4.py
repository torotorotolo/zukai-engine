# -*- coding: utf-8 -*-
"""第3章　29か月 c401–c419（19カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c4.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep19/make_plan19.py` で
  映像方針の一覧 `ref/ep19/eizou_build/list19.tsv`（承認ずみ・決め①〜⑩）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」と「フリー素材」を数える）。
  ⚠️ plan の「⑤b-1」は1秒1コマの走査で区間を選ぶ所・秒（÷365 の見込み）は書き写さない＝narration.json の実測で組む。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c401': dict(kind='図解',
               plan='図 時間の帯（2018-10-08 報告 → 2018-11-15 会議 → 2021-04 手紙 → 2021-06-24・「29か月」の帯は報告から2021年4月まで）｜権利：自作',
               src='MIN18 p.6〜7・GJ p.17'),
    'c402': dict(kind='文字の頁',
               plan='図 p3020 大陪審の報告 p.17（文字の頁・`as early as October 8, 2018` の段）',
               src='GJ p.17（`as early as October 8, 2018 the Champlain South condo board was aware of significant necessary repairs and maintenance`）'),
    'c403': dict(kind='図解',
               plan='図 書類の再現図 議事録の段（2018-11-15・`Structural engineer report was reviewed …`・名前は出さない）｜権利：自作',
               src='MIN18 p.7'),
    'c404': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='MIN18 p.7（`it appears the building is in very good shape`）・GJ p.17'),
    'c405': dict(kind='フリー素材',
               plan='S#16（書類とペンの手元）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：紙の字が読めない秒・寄りで',
               src='MIN18 p.7'),
    'c406': dict(kind='写真',
               plan='B2@99–108（片づいたデッキの床面と重機）｜副題：プールデッキの跡（崩落の後・2021年）｜権利：A推定｜注：—',
               src='GJ p.17〜18'),
    'c407': dict(kind='文字の頁',
               plan='図 p3021 大陪審の報告 p.18（文字の頁・`routine repairs and maintenance` の段）',
               src='GJ p.18'),
    'c408': dict(kind='図解',
               plan='図 数の比べ（1,400万ドル超 → 約15億円 → 136戸で割ると1戸あたり約1,100万円）｜権利：自作',
               src='GJ p.18（`more than $14,000,000`）・§9'),
    'c409': dict(kind='図解',
               plan='図 時間の帯（2018年秋 報告 → 2021年4月＝「29か月あまり」）｜権利：自作',
               src="GJ p.18（`more than 29 months after the engineer's report was received`）"),
    'c410': dict(kind='文字の頁',
               plan='図 p3021 大陪審の報告 p.18（文字の頁・29か月の段の切り出し）',
               src='GJ p.18'),
    'c411': dict(kind='フリー素材',
               plan='S#8（白い壁のひび）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：—',
               src='GJ p.18'),
    'c412': dict(kind='図解',
               plan='図 書類の再現図 手紙の抜粋（大陪審の報告 p.18 が引く文・名前は出さない）｜権利：自作',
               src='GJ p.18'),
    'c413': dict(kind='図解',
               plan='図 模式図【上から】はがす範囲（プールデッキ・入口の車道・地上の駐車場・プランター）｜権利：自作',
               src='GJ p.18（`we must pull up almost the entire ground level of the lot`）'),
    'c414': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='GJ p.18（`The concrete deterioration is accelerating.`）'),
    'c415': dict(kind='図解',
               plan='図 時間の帯（2021年4月 → 入札を開く予定の会議 → 13日 → 6月24日）｜権利：自作',
               src='GJ p.18'),
    'c416': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='GJ p.18（`Thirteen days after the Board was to hold a meeting to open the bids …, the building collapsed.`）'),
    'c417': dict(kind='写真',
               plan='B1@198–203.5（高い所からの現場と海）｜副題：崩落の現場と海（2021年6〜7月）｜権利：A推定｜注：204秒〜の表題カードを避ける（until）',
               src='GJ p.18・MIN18 p.7'),
    'c418': dict(kind='図解',
               plan='図 年表（2018年10月 報告 → 11月 会議 → 2021年4月 手紙・29か月 → 入札の会議 → 13日後）｜権利：自作',
               src='GJ p.1（題 `RECOMMENDATIONS TO MAKE BUILDINGS SAFER`・`policies, procedures, protocols, systems and practices`）・GJ p.17〜18'),
    'c419': dict(kind='写真',
               plan='B2@⑤b-1（110〜113.25 の現場の引きとその前）｜副題：現場の空撮（崩落の後・2021年）｜権利：A推定｜注：3.25秒を2.7倍に伸ばさない＝走査で続きの秒・無ければ 111秒のコマを静止画で受ける。114秒〜の表題カードを避ける',
               src='—（橋）'),
}

SPEC = {
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）──
    # c413（8.77秒＝0〜1.74／2.23〜4.98／5.47〜8.77）＝はがす範囲（GJ p.18「pull up almost the entire ground level of the lot」）
    "c413": dict(
        t="直す工事の広さ", s="地面の高さの床をほぼ全部",
        fig=("m19", dict(view="dig",
                         steps=[dict(state=dict(under="on"), delay=0.3, tag=dict(t="工事の多くは地面の下", at="under", to="cols")),
                                dict(state=dict(strip="on"), delay=0.3, tag=dict(t="ほとんど全部はがす", at="strip", to="deck")),
                                dict(state=dict(name="on"), delay=0.2,
                                     tag=[dict(t="プールデッキ", at="deck", to="deck"), dict(t="入口の車道", at="drive", to="drive"),
                                          dict(t="地上の駐車場", at="park", to="park")])],
                         note="範囲の線は模式（入口の車道の位置は空から見た写真の形）", src=ss.src(["GJ p3021"]))),     # ⑤b-6：出典の行を手で書かない（年の誤り「2022年」を直した）
    ),
    # ── 🆕 ⑤b-5（2026-10-06）：時間の帯・年表（`tools/axis.py`・門番 check_axis）──
    # c401（12.38秒＝聞き役 0〜1.54／2.04〜7.15／7.63〜12.38）＝この章の帯（予定の一覧＝報告・会議・手紙・崩落と「29か月」の括弧）。
    #   1行目で報告と章の帯／2行目「2018年11月15日。管理組合が会議を開いた」で理事会／3行目で招かれた町の建築担当者の札
    "c401": dict(
        t="報告のあと", s="管理組合の動き",      # ⚠️ echo：「1か月あまりあと」は字幕の切り取り・dup：「2018年の秋」は出典の行の写し
        fig=("axis", dict(ss.AX_REP, steps=[
            dict(add=[ss.ax("rep", fmt="ym", anchor="end"), ss.ax("m29"), ss.ax("letter"), ss.ax("fall_d", fmt="ym")], cur="2018-10-08"),
            dict(add=ss.ax("mtg"), cur="2018-11-15"),
            dict(add=dict(k="chips", at="2018-11-15", chips=["町の担当者が出席"], rec="GJ p3020"))],
            note="", src=ss.src(["MC18 p4001", "MIN18 p4106", "GJ p3020・p3021", "A12 p5101"]))),
    ),
    # c409（9.20秒＝聞き役 0〜2.23／2.72〜6.49／6.97〜9.20）＝2行目「報告から29か月あまりたった2021年4月」で括弧と手紙の点／
    #   3行目「補修の工事は、何も始まっていなかった」で項目の札（GJ p.18「had not begun any repair work」）
    "c409": dict(
        t="始まらない工事", s="報告から2021年4月まで",
        fig=("axis", dict(ss.AX_REP, past=[ss.ax("rep", fmt="ym", anchor="end"), ss.ax("mtg")], start=dict(cur="2018-11-15"), steps=[
            dict(),
            dict(add=[ss.ax("m29"), ss.ax("letter")], cur="2021-04"),
            dict(add=dict(k="chips", at="2021-04", chips=["工事は手つかず"], rec="GJ p3021"))],
            note="", src=ss.src(["MC18 p4001", "MIN18 p4106", "GJ p3020・p3021"]))),
    ),
    # c415（9.89秒＝聞き役 0〜2.19／2.68〜7.07／7.56〜9.89）＝2021年だけの帯。2行目「入札。それを開く会議が予定されていた」で会議の点
    #   （GJ p.18 は「崩れる13日前」としか書かない＝日付の札を出さない）／3行目「その結末を」で13日の括弧と崩落（数は次の c416 の決め所＝出さない）
    "c415": dict(
        t="工事の手前", s="手紙から崩落まで",      # ⚠️ dup：「2021年」は目盛りの年と同じ
        fig=("axis", dict(ss.AX_21, past=[ss.ax("letter")], start=dict(cur="2021-04"), steps=[
            dict(),
            dict(add=ss.ax("bid"), cur="2021-06-11"),
            dict(add=[ss.ax("d13"), ss.ax("fall_d")], cur="2021-06-24")],
            note="会議の日は「崩れる13日前」の記録から置いた", src=ss.src(["GJ p3021", "A12 p5101"]))),
    ),
    # c418（8.61秒＝0〜3.42／3.91〜8.61）＝大陪審の報告の題。この章の帯をまとめて並べる（予定の一覧＝報告→会議→手紙・29か月→入札の会議→13日後）
    "c418": dict(
        t="大陪審のまとめ", s="報告から崩落まで",
        fig=("axis", dict(ss.AX_REP, steps=[
            dict(add=[ss.ax("rep", fmt="ym", anchor="end"), ss.ax("mtg"), ss.ax("m29"), ss.ax("letter"), ss.ax("bid"),
                      ss.ax("d13"), ss.ax("fall_d", fmt="ym", anchor="start")], cur="2021-06-24"),
            dict()],
            # ⑤c'（10-07）：資料が4つ＋注で出典の行が 16px に縮んだ＝注を短く（c415 は資料が2つ＝元の注のまま）
            note="会議の日は記録の「13日前」",
            src=ss.src(["MC18 p4001", "MIN18 p4106", "GJ p3020・p3021", "A12 p5101"]))),
    ),
    # ── 🆕 ⑤b-6（2026-10-06）：書類の再現図（箱の型）・数の比べ（量の型 qty）──
    # c403（9.11秒＝0〜4.65／5.14〜9.11）＝議事録 p.7。1行目で「見たもの」と「書式」・2行目で「判断」。「とても良い状態に見える」は次の c404＝書かない
    "c403": dict(
        t="会議での判断", s="町の建築の担当者",
        fig=("boxes", dict(view="form", form=ss.FORM_MIN15, steps=[
            dict(add=[dict(k="paper"), dict(k="fill", f="書式")]),
            dict(add=dict(k="fill", f="判断"))],
            note="欄の字は原文のまま・様式は再現・名前は出さない", src=ss.src(["MIN18 p4107"]))),
    ),
    # c408（11.01秒＝0〜3.60／4.09〜8.85／9.34〜11.01）＝1行目で全体（1,400万ドル超＝約15億円）・3行目で136戸で割った額（台本 §9 の式）
    "c408": dict(
        t="大陪審が書いた額", s="円に直して比べる",
        fig=("qty", dict(view="bar", groups=[ss.QG["cost"], ss.QG["unit"]], steps=[
            dict(add=ss.qb("c_all")),
            dict(),
            dict(add=ss.qb("c_unit"))],
            note="記録は1,400万ドル超・1ドル約109円で換算", src=ss.src(["GJ p3021", "MC18 p4001"]))),
    ),
    # c412（8.36秒＝0〜3.95／4.44〜8.36）＝理事長の手紙（大陪審の報告 p.18 が引く）。1行目で目に見える傷み・2行目でこれから
    "c412": dict(
        t="手紙の中身", s="傷みは進んでいる",
        fig=("boxes", dict(view="form", form=ss.FORM_LET21, steps=[
            dict(add=[dict(k="paper"), dict(k="fill", f="目に見える傷み")]),
            dict(add=dict(k="fill", f="これから"))],
            note="欄の字は原文のまま（大陪審の報告が引く手紙）・様式は再現・名前は出さない", src=ss.src(["GJ p3021"]))),
    ),
    # ── 🆕 ⑤b-7a（2026-10-06）：写真・映像（list19 の区間と副題＝写っているもの・見出しは語りの写しにしない）──
    "c406": ss.vid("c406", t="議事録と報告のずれ", s="プールデッキの跡（崩落の後・2021年）"),
    "c417": ss.vid("c417", t="3度の知らせ", s="崩落の現場と海（2021年6〜7月）"),
    # c419＝束で上（重機の字）と右（奥の人の列）を切った＝縦横 1.24 の額装
    "c419": dict(t="崩れる前の合図", s="運び出す前の柱を調べる調査員（2021年7月6日）",
                 photo=P("n10_column_before"), **ss.kind(P("n10_column_before"))),
    # ── 🆕 ⑤b-7b（2026-10-06）：大陪審の報告の頁（スキャン＝OCR の行で切った・副題に年を書かない＝表の撮影年は資料の年）──
    # フリー素材（イメージ）：c405＝会議の机で書類に署名する手元（紙はぼけて読めない）・c411＝白い壁のひび
    "c405": ss.vid("c405"),
    "c411": ss.vid("c411"),
    "c402": dict(t="理事会が知っていたこと", s="節V の書き出しの段落",
                 photo=ss.page(3020), trim=ss.ptrim("c402"), bias=ss.pbias("c402"), panel=True, color=1.0),
    "c407": dict(t="手入れの不足", s="技術者の報告から読んだことの段落",     # ⑤c'：2018年の報告を書いた人は語りで「技術者」（c212・c308・c403）
                 photo=ss.page(3021), trim=ss.ptrim("c407"), bias=ss.pbias("c407"), panel=True, color=1.0),
    "c410": dict(t="動かなかった町", s="29か月の段落",
                 photo=ss.page(3021), trim=ss.ptrim("c410"), bias=ss.pbias("c410"), panel=True, color=1.0),
    # ── 🆕 ⑤b-8（2026-10-07）：決め所 ──
    # c404＝2018-11-15 の会議の議事録 PDF p.7「it appears the building is in very good shape」（話したのは町の建築担当者・名前は出さない）。
    #   大陪審は「議事録が正しいとすれば」の条件つきで扱う＝c406
    "c404": dict(
        t="会議の記録", s="招かれた町の担当者の判断",
        fig=("quote", dict(phrase=["議事録「建物は、", "とても良い状態に見える」"],    # 既定の折り方は「とても｜良い」で割れる
                           rows=ss.qrows("MIN18", "7頁", ("話した人", "町の建築担当者")), paper=True)),
    ),
    # c414＝大陪審の報告 印字 p.18 の太字の1行「concrete deterioration is accelerating.」（2021年4月の理事長の手紙を引く・名前は出さない）
    "c414": dict(
        t="悪くなる傷み", s="部屋の持ち主たちへの手紙",    # dup：決め所の1行目「理事長の手紙」と同じ見出しだった
        # 最後の焼き（ep19_b8 シート3）：既定の折り方は「「劣化は｜加速している」」＝かぎ括弧の中で割れた
        fig=("quote", dict(phrase=["理事長の手紙", "「劣化は加速している」"],
                           rows=ss.qrows("GJ", "18頁", ("書いた人", "管理組合の理事長"), ("日付", "2021年4月")), paper=True)),
    ),
    # c416＝同じ頁「Thirteen days after the Board was to hold a meeting to open the bids …, the building collapsed.」（予定の＝was to hold）
    "c416": dict(
        t="入札の会議", s="見積もりを開く予定の会議",
        fig=("quote", dict(phrase="入札を開く予定の会議の13日後に崩れた",
                           rows=ss.qrows("GJ", "18頁"), paper=True)),
    ),
}
