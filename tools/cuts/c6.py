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
    'c606': dict(kind='写真',     # ⑤b-7c：絵は NIST の動画の区間（スライド71）＝ca12 と同じ数え方
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

TR_SRC = "NIST の技術的知見の動画（2026年6月）"

SPEC = {
    # ── 🆕 ⑤b-7c（2026-10-07）：NIST の動画のスライド71（TFV 1870〜1878.4秒）──
    #   題「Observations: ~4-5 min before tower collapse」＝語り（約5分前の目撃・TR0181〜0183）と同じ場面。プールデッキの3D に
    #   目撃の印（a〜e）・右上「Source: NIST」・© の部分なし。動きの無い図＝崩れが南から北へ進む絵ではない＝副題は写っているもの
    #   （「推定」の札は付けない＝筋書きの絵ではなく観察の図）
    "c606": ss.vid("c606", t="約5分前の目撃", s="プールデッキの3D と目撃の印（NIST のスライド71）", panel=True),   # try2：額装（題の帯は USE の寄せで外す）
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
    # c618＝混ざり（1行目 A1 → 2行目から尻の頁 A01 p.47＝⑤b-7c）。1行目の終わりで真ん中の部分の屋上の線が約1階分下がる
    #   （TR0317・0318＝最初のコマ・K と L の近く）。
    #   🔴 ⑤b-7c（10-07）：尻の頁＝諮問委員会の資料 p.47（決め②＝頁ごと・額装・無加工・色を変えない）。頁のコマは南東の防犯カメラの
    #   1:22:19 AM（真ん中の部分が崩れ東の部分へ進む）＝語りの「最初のコマ」そのものではない＝見出しで「最初のコマ」と名乗らない・
    #   約2.5m の印は頁に無い＝頁の上の印（hl）は置かない。絵の2行目の札「約2.5m」は頁の下に隠れる＝外した（語りと字幕で伝える）
    "c618": dict(
        fig=("illu", dict(
            place="A1", start=dict(a1deck="fell"), rec="TR p1330（プールデッキは塔が崩れる数分前に崩れた）",
            steps=[dict(state=dict(a1mid="drop"), delay=2.4, rec=IL_REC["drop"],
                        tag=dict(t="屋上の線が下がる", at="roof_mid", off=(70, -60)))])),
        # ⑤c'（10-07）：頁の書き方「p.47」→「47頁」（諮問委員会の資料は印字＝PDF の頁・c917 の札「61頁」と同じ）
        tail=dict(t="崩れる真ん中の部分", s="防犯カメラのコマに NIST が柱の印（NIST の資料 47頁）",
                  photo=P("ncst_p047"), panel=True, color=1.0, still=True, at=1),
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
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）──
    # c607（5.89秒＝0〜3.61／4.10〜5.89）＝ロビーの風と音（TR0187・0188）・見えた範囲（TR0184〜0186・TF p9069 の緑）
    "c607": dict(
        t="ロビーの風と音", s="目撃の手がかり",
        fig=("m19", dict(view="sight",
                         steps=[dict(state=dict(vis="on", lobby="on"), delay=0.3,
                                     tag=[dict(t="目撃した人に見えた範囲", at="vis", to="vis"), dict(t="ロビー：急な風", at="lobby", to="lobby")]),
                                dict(state=dict(sound="on"), delay=0.3, tag=dict(t="大きな音", at="sound", to="lobby"))],
                         note="見えた範囲は NIST の図の形（風と音の印は模式・人は描かない）", src=TR_SRC + "の語りとスライド")),
    ),
    # c610（8.32秒＝0〜4.19／4.68〜8.32）＝北から撮った動画の1コマ（TR0203〜0207）。映像そのものは出さない
    "c610": dict(
        t="北から撮った動画", s="1コマを鮮明に",
        fig=("m19", dict(view="north",
                         steps=[dict(state=dict(eye="on"), delay=0.3, tag=dict(t="1:18:18", d="北にいた人の動画（見た向きは模式）", at="eye", to="eye")),
                                dict(state=dict(debris="on"), delay=0.3, tag=dict(t="駐車場の床：がれき", at="debris", to="debris"))],
                         rel=[dict(t="1:18:18", src="TR p1204（1:18 and 18 seconds a.m.）")],
                         note="撮った人の位置と見通しは模式（映像そのものは出さない）・落ちた範囲は推定", src=TR_SRC + "の語り")),
    ),
    # c611（9.25秒＝0〜1.90／2.39〜4.76／5.24〜9.25）＝デッキが塔の南の面まで崩れ・継ぎ目を2か所傷めた（TR0330・0089・TF p9111）
    "c611": dict(
        t="崩れの行き着いた所", s="デッキと塔の境",
        fig=("m19", dict(view="edge",
                         steps=[dict(tag=dict(t="塔の南の面（9.1 の線）", at="face", to="face")),
                                dict(state=dict(fall="full"), delay=0.3, tag=dict(t="プールデッキが崩れ落ちた", at="deck", to="deck")),
                                dict(state=dict(pull="on", joint="hurt"), delay=0.3,
                                     tag=dict(t="継ぎ目を2か所", d="K と L の線（横からは重なる）", at="joint", to="joint"))],
                         rel=[dict(t="9.1", src="TR p1287（gridline 9.1）"), dict(t="2か所", src="TR p1089（two critical structural connections）")],
                         note="床の落ち方・梁の長さは NIST の図の形の模式", src=TR_SRC + "の語りとスライド")),
    ),
    # c612（8.68秒＝0〜3.25／3.75〜6.38／6.87〜8.68）＝継ぎ目が押しつぶされ柱が下がる（TR0312・0332・0333）
    "c612": dict(
        t="数分後の継ぎ目", s="塔の柱の足もと",
        fig=("m19", dict(view="edge", start=dict(fall="full", pull="on", joint="hurt"),
                         steps=[dict(state=dict(load="on"), delay=0.3, tag=dict(t="最初は支えた", at="hold")),
                                dict(state=dict(joint="crush"), delay=0.3, tag=dict(t="ひび→押しつぶれ", at="crush", to="joint")),
                                dict(state=dict(drop="on"), delay=0.3, tag=dict(t="上の柱が下がり始めた", at="drop", to="face"))],
                         note="NIST の考え（模式）・下がりは大きく描いた", src=TR_SRC + "の語り")),
    ),
    # c613（9.00秒＝0〜3.81／4.30〜9.00）＝11 の列の部屋のカメラ（TR0335〜0345・TF p9127・p9134）。映像そのものは出さない
    "c613": dict(
        t="部屋の防犯カメラ", s="床の動きを測った",
        fig=("m19", dict(view="cam",
                         steps=[dict(state=dict(unit="on"), delay=0.3,
                                     tag=dict(t="11 の列の部屋のカメラ", d="向きは北（位置は模式）", at="unit", to="eye")),
                                dict(state=dict(move="on"), delay=0.3,
                                     # ⑥ の前（10-07・周2の注意）：札は上下の順のまま的は上下が逆（カメラ 925,570・L の柱 880,510）＝2本の線が交差
                                     #   → この札をカメラの札の上へ（線が交差しない）
                                     tag=dict(t="1:22:04〜1:22:15", d="L の線の柱の辺りが下がった", at=(1250.0, 330.0, "start", 560.0), to="l8"))],
                         rel=[dict(t="11 の列", src="TR p1335（the 11 stack）"), dict(t="1:22:04", src="TR p1345"),
                              dict(t="1:22:15", src="TR p1345")],
                         note="部屋の位置は NIST の図（カメラの位置は模式・映像そのものは出さない）", src=TR_SRC + "の語りとスライド")),
    ),
    # c614（6.64秒＝0〜3.79／4.28〜6.64）＝上の階の廊下のカメラ（TR0349〜0356・TF p9134）。I は動かない（スライド123）
    "c614": dict(
        t="上の階の廊下のカメラ", s="床がたわみ始めた",
        fig=("m19", dict(view="hall",
                         steps=[dict(state=dict(ref="on"), delay=0.3, tag=dict(t="1:21:55 のコマ", d="白い線＝床の基準の線", at="ref", to="ref")),
                                dict(state=dict(sag="on"), delay=0.3,
                                     tag=[dict(t="床がたわむ（K と L の辺り）", at="sag", to="sag"), dict(t="I の辺りは動かない", at="still", to="i")])],
                         rel=[dict(t="1:21:55", src="TR p1353（from 1:21:55 a.m.）")],
                         note="廊下の長さ・柱の間隔・たわみの大きさは模式（映像そのものは出さない）", src=TR_SRC + "の語りとスライド")),
    ),
    # ── 🆕 ⑤b-5（2026-10-06）：時刻の帯（`tools/axis.py`・門番 check_axis）。NIST の「約○分前」は時計に直さない＝基準 1:22（町の頁）
    #   からの位置に置き、札は「約7分前」。秒まである時刻（1:16:27）はそのまま。右の端の 1:22 は前の章からの続き（沈めた色）──
    # c602（7.03秒＝0〜3.91／4.40〜7.03）＝1行目「約8分から9分前…気になる音」の点／2行目「パチパチという音」の札。最後の車（約9分前）は c601
    "c602": dict(
        t="最後の数分", s="6月24日 午前1時台",
        fig=("axis", dict(ss.AX_NIGHT, past=[ss.ax("n9"), ss.ax("n22")], start=dict(cur="約-9"), steps=[
            dict(add=ss.ax("n89"), cur="約-9〜-8"),
            dict(add=dict(k="chips", at="約-9〜-8", chips=["パチパチという音"], rec="TR p1167"))],
            note=ss.TL_NOTE + "・「約○分前」は塔が崩れた 1:22 からの目安", src=ss.src(["TR p1161・p1167・p1168", "A12 p5101"]))),
    ),
    # c603（6.59秒＝0〜3.77／4.26〜6.59）＝1行目「約7分前。火災報知器が『トラブル信号』を記録」／2行目「どこの何のトラブルかは、記録に残っていない」
    "c603": dict(
        t="火災報知器の記録", s="最後の数分",
        # ⚠️ 門番 check_axis：約7分前の線が「約8〜9分前」の札（右へ振った）を貫いた＝この札を左へ振り、最後の車（約9分前）は出さない
        fig=("axis", dict(ss.AX_NIGHT, past=[ss.ax("n89", anchor="end"), ss.ax("n22")], start=dict(cur="約-9〜-8"), steps=[
            dict(add=ss.ax("n7"), cur="約-7"),
            dict(add=dict(k="chips", at="約-7", chips=["中身の記録なし"], rec="TR p1169"))],
            note=ss.TL_NOTE + "・「約○分前」は塔が崩れた 1:22 からの目安", src=ss.src(["TR p1161・p1167・p1169", "A12 p5101"]))),
    ),
    # c605（9.82秒＝聞き役 0〜1.41／1.90〜6.19／6.67〜9.82）＝2行目「1時16分27秒、最初の緊急の電話」／3行目「地震が起きたと思っていた」。
    #   約6分前（地上の駐車場）は c604 の語り
    "c605": dict(
        t="外への知らせ", s="建物の中から",      # ⚠️ echo：「最初の緊急の電話」は字幕の切り取り
        # ⚠️ 門番 check_axis：前の点を全部残すと札が3段目まで積み上がり、見出しの下線に触れた＝直前の2つ（約7分前・約6分前）だけ
        fig=("axis", dict(ss.AX_NIGHT, past=[ss.ax("n7"), ss.ax("n6"), ss.ax("n22")],
                          start=dict(cur="約-6"), steps=[
            dict(),
            dict(add=ss.ax("n1627"), cur="1:16:27"),
            dict(add=dict(k="chips", at="1:16:27", chips=["地震と思った"], rec="TR p1177"))],
            note=ss.TL_NOTE + "・「約○分前」は塔が崩れた 1:22 からの目安",
            src=ss.src(["TR p1161・p1167・p1169・p1170・p1177", "A12 p5101"]))),
    ),
    # c608（9.68秒＝0〜5.36／5.85〜9.68）＝1行目「1時17分49秒、2回目の電話」／2行目「その数秒後…見張る会社が建物へ電話」（1:17:55）。
    #   約5分前（デッキが崩れていく）は c606 の語り。最後の車（約9分前）はこのカットでは出さない（札が詰まる）
    "c608": dict(
        t="続く電話", s="1時17分台",
        # ⚠️ 門番 check_axis：AX_NIGHT のままでは札が3段に収まらなかった（6秒差の2点）＝1時16分〜19分の帯（AX_CALL）・前の点は1回目の電話だけ
        fig=("axis", dict(ss.AX_CALL, past=[ss.ax("n1627")], start=dict(cur="1:16:27"), steps=[
            dict(add=ss.ax("n1749"), cur="1:17:49"),
            dict(add=ss.ax("n1755"), cur="1:17:55")],
            note=ss.TL_NOTE, src=ss.src(["TR p1177・p1189・p1190"]))),
    ),
    # c622（6.75秒＝聞き役 0〜2.23／2.72〜6.75）＝第5・6章のまとめ＝NIST のスライドと同じ並び。1行目で週と時間の合図／
    #   2行目「この夜、塔へ届いた」で分と秒の出来事（約9分前〜1:22:14）
    "c622": dict(
        t="崩れまでの並び", s="何週間も前から",
        fig=("axis", dict(view="order", stops=ss.ALL_SIGNS, end="塔が崩れる", steps=[
            dict(add=[ss.ax("s3w"), ss.ax("s1w"), ss.ax("s17h"), ss.ax("s9h")], cur="約9時間前"),
            dict(add=[ss.ax("s9m"), ss.ax("s6m"), ss.ax("s1627"), ss.ax("s1749"), ss.ax("s2214")], cur="1:22:14")],
            note=ss.ORDER_NOTE,
            src=ss.src(["TR p1156・p1157・p1158・p1159・p1161・p1170・p1177・p1189・p1347", "TF p9061"]))),
    ),
    # ── 🆕 ⑤b-6（2026-10-06）：床の下がり（模式図 m19 の drop）・沈みの大きさ（量の型 qty）──
    # c615（6.32秒＝0〜3.75／4.24〜6.32）＝前日のコマと比べた床の下がり（TR0340・TR0344〜0347）。数の比べ → 模式図（下がりの大小と動かない列を
    #   見せる＝数は次の c616 の決め所と c617）。1行目で基準の床・2行目で下がった床
    "c615": dict(
        t="床の下がりを測る", s="前の日のコマと比べて",
        fig=("m19", dict(view="drop",
                         steps=[dict(state=dict(ref="on"), delay=0.3, tag=dict(t="前日のコマの床（基準）", at="ref", to="ref")),
                                dict(state=dict(now="on"), delay=0.3,
                                     tag=[dict(t="L-9.1 の近くが大きく下がる", at="l91", to="l91"),
                                          dict(t="L-8 の近くも下がる", at="l8", to="l8"),
                                          dict(t="M の列は動かない", at="m", to="m")])],
                         rel=[dict(t="L-9.1・L-8", src="TR p1344（L-9.1 and L-8）")],
                         note="下がりの大きさと床の形は模式（比べるのは大小だけ）", src=TR_SRC + "の語り")),
    ),
    # c617（13.09秒＝0〜3.90／4.39〜10.05／10.54〜13.09 聞き役）＝前日から 1:22:14 までの沈み（TR0348＝約18〜27インチ）。1行目で2本の棒
    #   （🔴 ひざ・机は記録の値ではない＝棒にしない・目盛りの45・70 に置いて注で「目安」）／2行目「もとの数字は…」は字幕だけ
    "c617": dict(
        t="沈みの大きさ", s="ひざから机の高さほど",
        fig=("qty", dict(view="bar", groups=[ss.QG["sink"]], steps=[
            dict(add=[ss.qb("s_lo"), ss.qb("s_hi")]), dict(), dict()],
            note="目盛りの45＝大人のひざ・70＝学校の机（目安）・記録は約18〜27インチ", src=ss.src(["TR p1348"]))),
    ),
    # ── 🆕 ⑤b-7a（2026-10-06）：写真・映像 ──
    # c621＝郡の消防の空撮（決め①・決め⑤＝引き・1024×768＝額装）
    "c621": dict(t="崩れが止まった境", s="崩れた所と残った西の部分（2021年6月24日・郡の消防）",
                 photo=P("c04_mdfr4"), **ss.kind(P("c04_mdfr4"))),
    "c623": ss.vid("c623", t="捜索の始まり", s="がれきの上の捜索（2021年6〜7月）"),
    # ── 🆕 ⑤b-8（2026-10-07）：決め所 ──
    # c616＝TR0348「The total drop near grid point L-9.1 from the day before the collapse to 1:22:14 a.m. was about 18-27 inches.」
    #   （18〜27インチ＝45.7〜68.6センチ）。語りの文字起こしは頁が無い＝頁の欄なし
    "c616": dict(
        t="床の沈み", s="傷んだ継ぎ目の近くの床",
        fig=("quote", dict(phrase=["床は前日から", "約46から69センチ沈んだ"],    # 既定の折り方は「約46｜から69」で割れる
                           rows=ss.qrows("TR", None, ("箇所", "発表の語り")), paper=True)),
    ),
}
