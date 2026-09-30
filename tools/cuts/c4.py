# -*- coding: utf-8 -*-
"""第4章　1944年生まれのレーサー c401–c420（20カット）。15本目（リノ・エアレース2011）。

■ 🔴 2026-09-30（⑤b-1）：14本目（セウォル号）の中身を空にした＝git の `dc6ecf4`（`git show dc6ecf4:tools/cuts/c4.py`）。
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
    "c401": dict(kind='写真',
               plan='台本の画：実写 A6 前日の事故機（2011-09-15・地上を走る・観客の撮影・額装）',
               src='AAB p10'),
    "c402": dict(kind='文字の頁',
               plan='台本の画：図 p12（報告書の来歴の頁・頁ごと）',
               src='AAB p12'),
    "c403": dict(kind='決め所',
               plan='台本の画：quote（決め所）',
               src='AAB p12'),
    "c404": dict(kind='図解',
               plan='【年表】年表（動く年表）：1944→2011 の機体の歩み（売却・リノ・持ち主・保管18年・分解整備と改造・2010年の出場）／勧告 A-12-08 が閉じるまで（c915 自作と同じ線）（映像方針 §11-2＝案B）｜台本の画：panel 1946年7月（余った機体として売却）',
               src='AAB p12'),
    "c405": dict(kind='写真',
               plan='台本の画：実写 C1 1969年の「ミス・キャンディス」（白黒・Bill Larkins・CC BY-SA 2.0・額装）',
               src='AAB p12'),
    "c406": dict(kind='写真',
               plan='台本の画：実写 C2 1970年のタキシング（白黒・Bill Larkins・額装）',
               src='AAB p12'),
    "c407": dict(kind='写真',
               plan='台本の画：実写 C3 1970年・損傷のあと（白黒・Bill Larkins・額装）',
               src='Commons の題名・#17 p3'),
    "c408": dict(kind='図解',
               plan='【年表】年表（動く年表）：1944→2011 の機体の歩み（売却・リノ・持ち主・保管18年・分解整備と改造・2010年の出場）／勧告 A-12-08 が閉じるまで（c915 自作と同じ線）（映像方針 §11-2＝案B）｜台本の画：panel 1983年7月｜⚠️ パイロットの実名（09-26 承認）＝人の形は描かない（映像方針 §1 線2）',
               src='AAB p12・p35・#17 p4'),
    "c409": dict(kind='文字の頁',
               plan='台本の画：図 p35（報告書の頁・特別耐空証明・頁ごと）',
               src='AAB p35'),
    "c410": dict(kind='図解',
               plan='【年表】年表（動く年表）：1944→2011 の機体の歩み（売却・リノ・持ち主・保管18年・分解整備と改造・2010年の出場）／勧告 A-12-08 が閉じるまで（c915 自作と同じ線）（映像方針 §11-2＝案B）｜台本の画：panel 1983年から1989年',
               src='AAB p12 注9'),
    "c411": dict(kind='図解',
               plan='【年表】年表（動く年表）：1944→2011 の機体の歩み（売却・リノ・持ち主・保管18年・分解整備と改造・2010年の出場）／勧告 A-12-08 が閉じるまで（c915 自作と同じ線）（映像方針 §11-2＝案B）｜台本の画：panel 18年の保管',
               src='AAB p12'),
    "c412": dict(kind='図解',
               plan='【年表】年表（動く年表）：1944→2011 の機体の歩み（売却・リノ・持ち主・保管18年・分解整備と改造・2010年の出場）／勧告 A-12-08 が閉じるまで（c915 自作と同じ線）（映像方針 §11-2＝案B）｜台本の画：panel 2007年から2009年',
               src='AAB p12'),
    "c413": dict(kind='図解',
               plan='【地図】地図 drift：3つの距離（152・228・266メートル）と命令・通達（152／305メートル）＝どちらの内か／オカラ・アリゾナ・テキサス・ミンデン／オカラから半径約161キロと機体の居場所／州道395号を止める／その後の配置（コースを北へ・燃料車を約2.4キロ先へ）（映像方針 §4）｜台本の画：図 自作 地図（オカラ・アリゾナ・テキサス・ネバダ州ミンデン）',
               src='AAB p12'),
    "c414": dict(kind='再現イラスト',
               plan='【案C 戻り】絵（案C）を戻す：D の機体に「操縦していた人」の名前と歳の札（人は描かない）／D の機体でエンジンとプロペラに札／A を動かさずに戻す（×・人なし・数は字幕だけ）（映像方針 §11-2＝案B）｜台本の画：panel エンジンとプロペラ',
               src='AAB p13'),
    "c415": dict(kind='図解',
               plan='【書類】書類の再現図（自作の用紙＝本物の頁ではない・台本 §0-3 の「記録簿・参加書類の再現図」）：記録簿の総時間／「試験はどうだったのか」／参加書類の「大きな改造をしたか □はい □いいえ」／年齢の欄／検査の用紙の備考と合格・書面で確かめる欄が無い／新しい検査の用紙（映像方針 §11-2＝案B）｜台本の画：panel 機体の総飛行時間',
               src='AAB p15 注15'),
    "c416": dict(kind='写真',
               plan='台本の画：実写 C5 2010年の事故機（ピット・jeggernot・CC BY 2.0）',
               src='AAB p12・p36'),
    "c417": dict(kind='写真',
               plan='台本の画：実写 C4 2010年の事故機の機首（jeggernot・CC BY 2.0・右の人を切り落とす）',
               src='AAB p15'),
    "c418": dict(kind='パネル',
               plan='台本の画：panel 古い機械を直して動かす',
               src='—'),
    "c419": dict(kind='写真',
               plan='台本の画：実写 B5 事故の日の朝の機首（2011-09-16 07:59・観客の撮影・額装）',
               src='実写 B5 の撮影時刻・AAB p10'),
    "c420": dict(kind='パネル',
               plan='台本の画：panel 橋',
               src='AAB p42'),
}

SPEC = {

    # ── 🔴 ⑤b-6（2026-09-30）：写真と頁の束（`qa_out/ep15_assets.py`）──
    # A6＝前日（9/15 現地）・地上を走る事故機（「177」）。人物は操縦席だけ（顔は見えない＝②の台帳）
    "c401": dict(
        t="事故機",
        s="2011年9月15日　地上を走る事故機（観客の撮影）",
        photo=P("gg_taxi_0915"), panel=True, color=1.0,
    ),
    # 報告書 1.3「機体の情報」（p12）＝「The P-51D variant entered production in April 1944」の行を真ん中に
    "c402": dict(
        t="機体の来歴",
        s="報告書 1.3　機体の情報",
        photo=ss.page(12), trim=ss.ptrim("c402"), panel=True, color=1.0,
    ),
    # C1（Bill Larkins・BY-SA 2.0）＝1969年の「Miss Candace」「69」（撮影年は題名の「69」）
    "c405": dict(
        t="1969年の姿",
        s="1969年　番号69の「ミス・キャンディス」",
        photo=P("candace_1969"), panel=True, color=1.0,
    ),
    # C2＝1970年のタキシング（題名の「70」）
    "c406": dict(
        t="改造の歴史",
        s="1970年　地上を走る番号69の機体",
        photo=P("taxi_1970"), panel=True, color=1.0,
    ),
    # C3＝格納庫の中・胴体の下が壊れた状態（題名「after damage 1970」）。⚠️ 胴体着陸の損傷かは写真だけで決められない
    #   ＝副題は題名の言葉まで（④' の訂正＝materials.md §11）
    "c407": dict(
        t="壊れたあと",
        s="1970年　損傷のあとの機体（写真の題名から）",
        photo=P("damage_1970"), panel=True, color=1.0,
    ),
    # 報告書 1.11.1（p35）＝「received a special airworthiness certificate」の行を真ん中に
    "c409": dict(
        t="特別耐空証明",
        s="報告書 1.11.1　FAAの決まり",
        photo=ss.page(35), trim=ss.ptrim("c409"), panel=True, color=1.0,
    ),
    # C5（jeggernot・CC BY 2.0）＝2010年9月18日・ピットの事故機（「177」）。🔴 手前の人・テントの人の顔＝顔だけモザイク
    #   （09-30 カズヤくん・元画像を直す＝`ss.NEEDS_MASK`・`qa_out/ep15_assets.py` の MASK）
    "c416": dict(
        t="21年ぶりのリノ",
        s="2010年9月18日　ピットの事故機",
        photo=P("gg_pit_2010"), **ss.kind(P("gg_pit_2010")),
    ),
    # C4（jeggernot・CC BY 2.0）＝2010年9月18日・ピットの機首。🔴 整備の人と周りの人の顔＝顔だけモザイク（元画像を直す）
    "c417": dict(
        t="事故機の機首",
        s="2010年9月18日　ピットの事故機の機首",
        photo=P("gg_nose_2010"), **ss.kind(P("gg_nose_2010")),
    ),
    # B5＝事故の日の朝（9/16 現地 07:59）・ピットの機首「THE GALLOPING GHOST」
    "c419": dict(
        t="事故の日の朝",
        s="2011年9月16日の朝　ピットの機首（観客の撮影）",
        photo=P("gg_nose_0916"), panel=True, color=1.0,
    ),

    # ── 🔴 ⑤b-5（2026-09-30）：年表（14本目の `axis` date＝c324 と同じ軸 AX_HIST）と書類の再現図（`boxes` form）──
    # 前の点は沈んだ色で残す（past）。事故（2011年）は右の端にいつも沈んで残る
    "c404": dict(
        t="戦争のあと",
        s="軍から民間へ",
        # ⚠️ 1944年の点の札は出さない（1946年の点の縦の線が札を貫いた＝31画素しか離れていない・日付は c403 の決め所）
        fig=("axis", dict(**ss.AX_HIST, past=[ss.ax("deliver", lab=False, t=""), ss.ax("acc")], start=dict(cur="1944-12-23"),
                          steps=[dict(), dict(add=ss.ax("sold"), cur="1946-07")],
                          note="機体の歩み（報告書の来歴から）", src=ss.src(["AAB p10・p12"]))),
    ),
    # 1行目＝1983年7月にパイロットが取得／2行目＝翌月（8月17日）に FAA の特別な許可（AAB p35）＝点の下の札で。
    #   ⚠️ 8月17日を別の点にすると2点が2画素しか離れず、右の点の縦の線が左の札を貫いた（⑤b-5 の layout）
    #   ⚠️ 1946年の点の札は消して沈める（試し焼き 36676841212 で、1946年の縦の線が1944年の札を貫いた＝31画素しか離れていない）
    "c408": dict(
        t="持ち主が替わる",
        s="実験機という区分",
        fig=("axis", dict(**ss.AX_HIST, past=[ss.ax("deliver", fmt="y"), ss.ax("sold", lab=False, t=""), ss.ax("acc")],
                          start=dict(cur="1946-07"),
                          steps=[dict(add=ss.ax("owner"), cur="1983-07"),
                                 dict(add=dict(k="chips", at="1983-07", chips=["翌月：FAAの許可"], rec=["AAB p12", "AAB p35"]))],
                          note="機体の歩み（報告書の来歴から）", src=ss.src(["AAB p10・p12・p35"]))),
    ),
    # 1983年から1989年まで（年だけの記録＝帯は年の真ん中から真ん中）。2行目（番号と名前が変わった＝注9）は字幕だけ
    "c410": dict(
        t="持ち主の時代",
        s="レースに出た年月",
        fig=("axis", dict(**ss.AX_HIST, past=[ss.ax("deliver", fmt="y"), ss.ax("owner", fmt="y"), ss.ax("acc")],
                          start=dict(cur="1983-07"),
                          steps=[dict(add=ss.ax("race8389"), cur="1989"), dict()],
                          note="機体の歩み（報告書の来歴から）", src=ss.src(["AAB p10・p12"]))),
    ),
    # 1行目＝1989年から保管（帯）／2行目＝2007年に出された（18年＝括弧・数は書かない）
    "c411": dict(
        t="しまい込まれた機体",
        s="レースを離れて",
        fig=("axis", dict(**ss.AX_HIST, past=[ss.ax("deliver", fmt="y"), ss.ax("race8389"), ss.ax("acc")],
                          start=dict(cur="1989"),
                          steps=[dict(add=ss.ax("store")), dict(add=ss.ax("store_br"), cur="2007")],
                          note="機体の歩み（報告書の来歴から）", src=ss.src(["AAB p10・p12"]))),
    ),
    # 1行目（聞き役）そのまま／2行目＝2007年から2009年の分解整備と改造（アリゾナ・テキサス・ネバダ＝次の c413 の地図）
    "c412": dict(
        t="長い眠りのあと",
        s="3つの州で",
        fig=("axis", dict(**ss.AX_HIST, past=[ss.ax("deliver", fmt="y"), ss.ax("race8389"), ss.ax("store"), ss.ax("acc")],
                          start=dict(cur="2007"),
                          steps=[dict(), dict(add=ss.ax("rebuild"), cur="2009")],
                          note="機体の歩み（報告書の来歴から）", src=ss.src(["AAB p10・p12"]))),
    ),
    # 記録簿の総時間（書類の再現図）：1行目（聞き役）で紙・2行目で読む・3行目そのまま。値＝2011年7月29日の総時間 1,453.6時間
    #   （機体の記録簿の 1,447.2 は 6.4時間の書き違い＝エンジンの記録簿の値が正しい＝AAB p15 注15・p16）
    "c415": dict(
        t="この機体の飛行時間",
        s="生まれてからの合計",
        fig=("boxes", dict(view="form", form=ss.FORM_LOG11, steps=[dict(add=dict(k="paper")), dict(), dict()],
                           note="再現（本物の頁ではない・値はエンジンの記録簿の総時間＝報告書 注15）",
                           src=ss.src(["AAB p15・p16"]))),
    ),

    # ── 🔴 ⑤b-3（2026-09-30）：案C の戻り（`tools/illu.py` の RB＝15本目）──
    # B（横から・レース中の事故機）でエンジンとプロペラに札（AAB p13「Rolls-Royce Merlin V-1650-9A engine, which was modified
    #   for racing, and an unmodified Hamilton Standard 24D50 propeller」）。PLAN の予定は「D の機体」＝止まった機体はプロペラの
    #   羽根の数（記録に無い）を描くことになる＝回る翼の円で描ける B に付けた（c107 と同じ理由）。全面の絵＝見出し t・副題 s なし
    "c414": dict(
        fig=("illu", dict(
            place="RB", at="16:24", start=dict(view="side", ground="on"),
            rec="AAB p13（レース用に改造したロールス・ロイスのマーリン・手を加えていないプロペラ）",
            steps=[dict(pylon=1, delay=0.3, rec="AAB p10（パイロンを回るレース）",
                        # ⚠️ 下見：25字の札は字が縮み（約24px）遠い山並みに掛かった＝短くして砂漠の上へ（名前の全部は字幕）
                        tag=dict(t="エンジン：マーリン（レース用に改造）", at="engine", off=(-60, 220),
                                 anchor="end", keep=True, delay=0.8)),
                   dict(tag=dict(t="プロペラ：手を加えていない", at="prop", off=(60, -80), keep=True))])),
    ),
}
