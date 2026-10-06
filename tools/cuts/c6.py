# -*- coding: utf-8 -*-
"""第5章　午前1時22分 c601–c623（23カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c6.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep19/make_plan19.py` で
  映像方針の一覧 `ref/ep19/eizou_build/list19.tsv`（承認ずみ・決め①〜⑩）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」と「フリー素材」を数える）。
  ⚠️ plan の「⑤b-1」は1秒1コマの走査で区間を選ぶ所・秒（÷365 の見込み）は書き写さない＝narration.json の実測で組む。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P
from illu import A1_REC as IL_REC  # noqa: E402  🆕 ⑤b-2：A1 の部品の出典（描く側と同じ文＝2か所に書かない・illu は cuts を読まない＝循環しない）
from illu import A2_REC as A2R, A3_REC as A3R  # noqa: E402  🆕 ⑤b-3：A2・A3

PLAN = {
    'c601': dict(kind='再現イラスト',
               plan='図 再現イラスト A3【横から】夜の駐車場・最後の車が入る（人は描かない）｜権利：自作',
               src='TR0161・TR0166'),
    'c602': dict(kind='図解',
               plan='図 時間の帯（約9分前・約8〜9分前・約7分前・約6分前・1:16:27・約5分前・1:17:49・1:18:18・1:22）｜権利：自作',
               src='TR0167・TR0168'),
    'c603': dict(kind='図解',
               plan='図 時間の帯（約7分前に印）｜権利：自作',
               src='TR0169'),
    'c604': dict(kind='再現イラスト',
               plan='図 再現イラスト A2【上から】地上の駐車場の床が落ちる（車は傾く・「推定」の札・人は描かない）｜札：推定｜権利：自作',
               src='TR0170〜0174'),
    'c605': dict(kind='図解',
               plan='図 時間の帯（1:16:27 に印）｜権利：自作',
               src='TR0177'),
    'c606': dict(kind='図解',
               plan='TFV@TR0191〜0195（プールデッキが南から北へ崩れる NIST の3D とアニメ）｜副題：NIST のアニメーション（技術的知見の動画）｜札：推定｜権利：A｜注：🔁 台本は再現イラスト。NIST の「推定の筋書き」の札を添える。©2021 の部分が画面に無い秒だけ',
               src='TR0181〜0183'),
    'c607': dict(kind='図解',
               plan='図 模式図【上から】目撃した人から見えた範囲（NIST の図の型を描き起こし・名前は出さない）｜権利：自作',
               src='TR0184〜0188'),
    'c608': dict(kind='図解',
               plan='図 時間の帯（1:17:49・1:17:55 に印）｜権利：自作',
               src='TR0189・TR0190'),
    'c609': dict(kind='再現イラスト',
               plan='図 再現イラスト A2 の地【上から】ロビーと地上の駐車場（沈んだ車の位置・人は描かない）｜権利：自作',
               src='TR0200〜0202'),
    'c610': dict(kind='図解',
               plan='図 模式図【上から】建物の北からの見通し（1:18:18 のコマの位置・映像そのものは出さない）｜権利：自作',
               src='TR0203〜0207'),
    'c611': dict(kind='図解',
               plan='図 模式図【横から】塔の南の面とプールデッキの継ぎ目（2か所・梁が外れて継ぎ目が傷む）｜権利：自作',
               src='TR0330・TR0089・TR0292・TR0293'),
    'c612': dict(kind='図解',
               plan='図 模式図（同じ・継ぎ目のひびが育つ）｜権利：自作',
               src='TR0312・TR0332・TR0333'),
    'c613': dict(kind='図解',
               plan='図 模式図【上から】部屋の中の防犯カメラの位置（塔の東寄りの部屋の列・映像そのものは出さない）｜権利：自作',
               src='TR0335〜0345'),
    'c614': dict(kind='図解',
               plan='図 模式図【横から】上の階の廊下のカメラ（1:21:55 のコマの基準の線・床のたわみ）｜権利：自作',
               src='TR0349〜0356'),
    'c615': dict(kind='図解',
               plan='図 数の比べ（前日のコマ → 1:22:14 の床の沈み・柱の札）｜権利：自作',
               src='TR0344〜0346'),
    'c616': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0348（`The total drop near grid point L-9.1 from the day before the collapse to 1:22:14 a.m. was about 18-27 inches.`）'),
    'c617': dict(kind='図解',
               plan='図 数の比べ（46〜69センチ：大人のひざ〈約45センチ〉から学校の机〈約70センチ〉ほど）｜権利：自作',
               src='TR0347・§9'),
    'c618': dict(kind='混ざり',       # ⑤b-2：2行目から尻の頁（A01 p.47〜51＝決め②）＝本物の側のつなぎ待ち（ss.ILLU_MIX_TODO・⑤b-7b）
               plan='A1 屋上の線が約1階分下がる｜差し込み（tail）：2 A01  5.4秒 A01 p.47〜51 の頁（監視カメラのコマに NIST が印）｜副題：NIST の資料の頁（映像のコマ＝© 2021 Used with permission）｜権利：紙面の引用｜注：決め②＝🅰：動く映像は使わない・頁ごと・額装・無加工・出典に「NIST の資料（映像のコマ © 2021 Used with permission）」',
               src='TR0314・TR0317・TR0318'),
    'c619': dict(kind='再現イラスト',
               plan='図 再現イラスト A1（真ん中の部分が南から北へ崩れる）｜権利：自作',
               src='TR0329・TR0363'),
    'c620': dict(kind='再現イラスト',
               plan='図 再現イラスト A1（東の部分が西へ揺れ、下の階の柱が耐えきれず落ちる）｜権利：自作',
               src='TR0091〜0093・TR0406〜0424'),
    'c621': dict(kind='写真',
               plan='B1@⑤b-1（残った西の部分が立っている秒＝138〜143 は使わない）｜副題：崩れた所と残った西の部分（2021年6〜7月）｜権利：A推定｜注：🔁 B2@12–14 から（B2 は片づいた後の空撮＝解体〈7月4日〉の後なら西の部分は写らない）。決め⑤＝引きの秒だけ。代わり＝C1・C2（郡の消防＝決め①で使う）',
               src='TR0369'),
    'c622': dict(kind='図解',
               plan='図 時間の帯（約3週間前 → 1週間前 → 17時間前 → 9時間前 → 9分前 → 6分前 → 1:16:27 → 1:17:49 → 1:22:14 → 崩落）｜権利：自作',
               src='TR0016・TR0095・TR0330'),
    'c623': dict(kind='写真',
               plan='B1@115–118.5（がれきの上の捜索隊と柱）｜副題：がれきの上の捜索（2021年6〜7月）｜権利：A推定｜注：顔は判別できない（台帳）',
               src='—（橋）'),
}

SPEC = {
    # ── 🆕 ⑤b-3（2026-10-06）：A3（地下の駐車場）と A2（上から）──
    # c601（8.92秒）＝1行目は聞き役の問い／2行目（2.69〜）：約9分前に最後の車が入る（TR0161・左の外から入って止まる＝模式）／
    #   3行目：このとき落ちた床はまだ誰も見ていない（TR0166）＝落ちた床は描かない
    "c601": dict(
        fig=("illu", dict(
            place="A3", start=dict(a3cars="on", a3carin="go"), rec="TR p1162（その夜、何台かの車が止められていた）",
            steps=[dict(),
                   dict(state=dict(a3carin="in"), delay=0.8, dur=2.6, rec=A3R["carin"],
                        tag=dict(t="最後に入った車", at="carin", off=(60, -130))),
                   dict(state=dict(cam=1.06), delay=0.2, dur=2.4)])),
    ),
    # c604（11.67秒）＝上から（直前の A3〈c601〉は横から＝切り替えの字）。「崩れた範囲は推定」（何人もの目撃・TR0170〜0174）。
    #   1行目：地上の駐車場の床が落ちていく／2行目：落ちきって車が下へ傾く／3行目（音）：寄るだけ（音の印は描かない）
    "c604": dict(
        fig=("illu", dict(
            place="A2", start=dict(switch="on", a2cars="on"), rec="TR p1170（約6分前・何人もの目撃）",
            assume="崩れた範囲は推定",
            steps=[dict(state=dict(a2park="fall"), delay=1.4, dur=2.2, rec=A2R["park_fall"],
                        tag=dict(t="地上の駐車場", at="hole", off=(-260, 130), anchor="end")),
                   dict(state=dict(a2park="fell"), delay=1.6, rec=A2R["cars"],
                        tag=dict(t="傾いた車", at="cars", off=(-200, -60), anchor="end")),
                   dict(state=dict(cam=1.08), delay=0.2, dur=3.0)],
            camc=(785.0, 560.0))),
    ),
    # c609（7.30秒）＝上から。ロビー（塔の1階の南の帯・位置は概略＝TF p9096）と、外へ出て見に行った沈んだ車（TR0200・0201）。
    #   デッキの南の一部もこのころ崩れていた（TR0203）＝落ちた範囲は推定の札
    "c609": dict(
        fig=("illu", dict(
            place="A2", start=dict(a2cars="on", a2park="fell", a2deck="part"), rec="TR p1203（デッキの一部が崩れた映像）",
            assume="崩れた範囲は推定",
            steps=[dict(state=dict(a2lobby="on"), delay=0.8, rec=A2R["lobby"],
                        tag=dict(t="ロビー（塔の1階）", at="lobby", off=(-40, -110), anchor="end")),
                   dict(state=dict(a2lobby="walk"), delay=1.2, rec=A2R["lobby"],
                        tag=dict(t="沈んだ車", at="cars", off=(-230, 70), anchor="end"))])),
    ),
    # ── 🆕 ⑤b-2（2026-10-06）：案C の置き場 A1（南から見た塔・`tools/illu.py` の「19本目 ⑤b-2」の節）──
    #   人・窓の灯りは描かない。プールデッキは塔が崩れる数分前に崩れている（TR0330）＝この章の A1 は頭から a1deck="fell"。
    #   秒は narration.json の実測（c618 0〜4.29／4.78〜9.15・c619 0〜3.24／3.73〜7.84・c620 0〜4.79／5.28〜8.43／8.92〜11.60）
    # c618＝混ざり（1行目 A1 → 2行目から尻の頁 A01 p.47〜51＝⑤b-7b）。1行目の終わりで真ん中の部分の屋上の線が約1階分下がる
    #   （TR0317・0318＝最初のコマ・K と L の近く）。2行目の札は尻の頁をつなぐまでの仮（つないだら頁の上の印で見せる）
    "c618": dict(
        fig=("illu", dict(
            place="A1", start=dict(a1deck="fell"), rec="TR p1330（プールデッキは塔が崩れる数分前に崩れた）",
            steps=[dict(state=dict(a1mid="drop"), delay=2.4, rec=IL_REC["drop"],
                        tag=dict(t="屋上の線が下がる", at="roof_mid", off=(70, -60))),
                   # ⑤b-2 の qa_all（layout）：1行目の札と同じ所で重なった＝下げて出す
                   dict(rec=IL_REC["drop"], tag=dict(t="約2.5m（ほぼ1階分）", at="roof_mid", off=(70, 30), keep=True))])),
    ),
    # c619＝「推定」。1行目：3階より下の柱（K と L）の印／2行目：真ん中の部分が南から北へ（奥へ）次々と抜け落ちる
    "c619": dict(
        fig=("illu", dict(
            place="A1", start=dict(a1deck="fell", a1mid="drop"), rec="TR p1330・TR p1318",
            assume="推定（NIST の見立て）",
            steps=[dict(state=dict(a1low3="on"), delay=0.5, rec=IL_REC["low3"],
                        tag=dict(t="3階より下の柱", at="low3", off=(80, -40))),
                   dict(state=dict(a1low3="off", a1mid="fall"), delay=0.3, rec=IL_REC["mid_fall"],
                        tag=dict(t="南から北へ（奥へ）次々と", at="mid_heap", off=(-40, -330), anchor="end"))])),
    ),
    # c620＝「推定」。1行目：東の部分が西へ揺れる（揺れは大きく描く＝左下の断り）／2行目：下の階の柱が耐えきれず東も落ちる／3行目（聞き役）：そのまま
    "c620": dict(
        fig=("illu", dict(
            place="A1", start=dict(a1deck="fell", a1mid="fell"), rec="TR p1417（真ん中の部分のほとんどが崩れた）",
            assume="推定（NIST の見立て）",
            # ⑤b-2 の下見：根元の真ん中で回す形＝角が浮く（40画素で約16画素）→ 30画素（浮き約11画素＝前のデッキの板に隠れる）
            steps=[dict(state=dict(a1sway=-30.0), delay=0.6, dur=1.4, rec=IL_REC["sway"],
                        tag=dict(t="西へ揺れる", at="east12", off=(-40, -90), anchor="end")),
                   dict(state=dict(a1east="fall"), delay=0.4, rec=IL_REC["east_fall"],
                        tag=dict(t="下の階の柱", at="heap", off=(140, -200))),       # ⑤b-2 の echo：語りの複写にしない＝名詞だけ
                   dict(state=dict(cam=1.06), delay=0.2, dur=2.4)])),
    ),
}
