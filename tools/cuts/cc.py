# -*- coding: utf-8 -*-
"""終章　その後 cc01–cc30（30カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/cc.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep19/make_plan19.py` で
  映像方針の一覧 `ref/ep19/eizou_build/list19.tsv`（承認ずみ・決め①〜⑩）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」と「フリー素材」を数える）。
  ⚠️ plan の「⑤b-1」は1秒1コマの走査で区間を選ぶ所・秒（÷365 の見込み）は書き写さない＝narration.json の実測で組む。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P
from illu import A1_REC as IL_REC  # noqa: E402  🆕 ⑤b-2：A1 の部品の出典（描く側と同じ文）
from illu import A4_REC as A4R, A5_REC as A5R  # noqa: E402  🆕 ⑤b-3：A4・A5

PLAN = {
    'cc01': dict(kind='写真',
               plan='D（DHS・撤去の後の現場の引き）｜副題：撤去の後の現場（2021年8月19日）｜権利：A（DHS）｜注：決め⑥＝引きだけ（肖像・遺族・花の寄りが写らないコマ）',
               src='A16（2021-12-15）・GJ p.1'),
    'cc02': dict(kind='文字の頁',
               plan='図 p3004 大陪審の報告 p.1（文字の頁・`failings at every level` の段）',
               src='GJ p.1（`we decided to look at the policies, procedures, protocols, systems and practices`・`there were failings at every level and for all of the participants`）'),
    'cc03': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='GJ p.18（`There was sufficient information, provided early enough to put everyone on notice of a major problem.`）'),
    'cc04': dict(kind='写真',
               plan='B1@⑤b-1（現場の引き・残った西の部分＝決め⑤で引きの秒だけ）｜副題：崩落の現場（2021年6〜7月）｜権利：A推定｜注：—',
               src='GJ p.18（`none of the participants acted quickly enough to avert this tragedy`）・GJ p.1（`We cannot let this happen again!`）'),
    'cc05': dict(kind='図解',
               plan='図 一覧（大陪審の勧告の6つのねらい＝アイコン：役所が早く見つけて動く・海辺の傷み・傷みを見つけて直す・報告を期限どおりに・役所の力・住民がネットで読める）｜権利：自作',
               src='GJ p.1（`Our recommendations included below are designed to`）'),
    'cc06': dict(kind='写真',
               plan='C13 は c923 → D の別のコマ（決め⑥＝引きだけ・ca21・cc01 と別のコマ）｜副題：撤去の後の現場（2021年8月19日）｜権利：A（DHS）｜注：—',
               src='GJ p.3（`we believe the 40-year recertification should [occur] much earlier`＝OCR で1語落ち）・GJ p.32（`we predict that the Champlain South Condominium building will not be the last partial building collapse in our community`）'),
    'cc07': dict(kind='図解',
               plan='図 地図【上から】サーフサイドとノースマイアミビーチ市（位置だけ）｜権利：自作',
               src='GJ p.20（`the City of North Miami Beach`・`decided to conduct an audit of all buildings and structures five stories or higher`）'),
    'cc08': dict(kind='図解',
               plan='図 数の比べ（10階建て・156戸・40年の点検の期限＝2012年 → 9年半の遅れ）｜権利：自作',
               src='GJ p.20（`Crestview Towers is a 10-story, 156-unit condominium building.`・`9½ years overdue`）'),
    'cc09': dict(kind='決め所',
               plan='quote（決め所・技師の手紙の1行＝GJ p.20 が引く文・名前は出さない）｜権利：自作',
               src='GJ p.20（`on July 2, 2021, officials in the Building and Zoning Department received a letter`・`Structurally no (sic) safe for the specified use for continued occupancy.`）'),
    'cc10': dict(kind='再現イラスト',
               plan='図 再現イラスト（同じ建物・赤い札＝危険の印・人は描かない）｜権利：自作',
               src='GJ p.20（`ordered that the building be red-tagged, and all occupants ordered to evacuate the building immediately`）'),
    'cc11': dict(kind='図解',
               plan='図 流れ図（報告が理事会の手元に止まる → 市は知らない／市が点検の遅れを調べる → 報告が市へ → すぐに退去）｜権利：自作',
               src='GJ p.22（`no notification at all was provided to the Local Building Official regarding Crestview Towers`）'),
    'cc12': dict(kind='図解',
               plan='図 流れ図（技師の報告 → 48時間以内に市へ写し＝アベンチュラ市の決まり・GJ p.21 の形）｜権利：自作',
               src='GJ p.21（`provide a copy of any engineering report concerning structural, electrical, life-safety concerns of a building they are responsible for to the City within forty-eight hours of receiving such a report`）'),
    'cc13': dict(kind='フリー素材',
               plan='S#4（夕方の海辺の高層の空撮・2021年9月の投稿）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：🔁 台本は実写（B2）＝州の法律の話は海辺のマンション全体＝フリー素材に。跡地が写らないか⑤b-1',
               src='A14 p.1（`An act relating to building safety`）'),
    'cc14': dict(kind='図解',
               plan='法律の要点（台本のまま）｜差し込み（head）：1 S#1  6.2秒 S#1（海辺の白いコンクリートの建物の空撮）｜副題：イメージ｜札：イメージ（差し込み）｜権利：Pexels License｜注：跡地・屋上の看板の字を⑤b-1で',
               src='A14 p.8（`three stories or more in height by December 31 of the year in which the building reaches 30 years of age`・`within 3 miles of a coastline`）・A14 p.9（`reaches 25 years of age`・`every 10 years thereafter`）'),
    'cc15': dict(kind='図解',
               plan='図 法律の要点（同じ・直すお金の備えの調べ＝10年ごと・2024年の終わりから積み立て無しは不可）｜権利：自作',
               src='A14 p.37（`structural integrity reserve study completed at least every 10 years`）・A14 p.35（`Effective December 31, 2024, the members of a unit-owner controlled association may not determine to provide no reserves or less reserves`）'),
    'cc16': dict(kind='写真',
               plan='B1@⑤b-1（現場の引き）｜副題：崩落の現場（2021年6〜7月）｜権利：A推定｜注：—',
               src='A14 p.9（`on or before July 1, 1992`・`before December 31, 2024`）・今の条文 553.899 (3)(b)（p9811・`proximity to salt water`）'),
    'cc17': dict(kind='図解',
               plan='時間の帯（6月24日 1:22 にともす → 7月20日 20:03 に消す）｜副題：—｜権利：自作｜注：🔁 台本は実写（町の追悼の灯の写真は在庫に無い）＝決め⑥で時間の帯の図に',
               src='A12（`the symbolic remembrance torch lit at 1:22 am on June 24`・`July 20th at 8:03 pm`）'),
    'cc18': dict(kind='図解',
               plan='図 地図【上から】記念の場所（88番通りの端の公園・現場のすぐそば）｜権利：自作',
               src='A13（`At the Special Commission Meeting held on August 6`・`the street end park at 88 th Street`）・A12（`88th Street just a few feet away from the Champlain building site`）・A13（`For five years, the Committee worked in close partnership with victims’ families, survivors, first responders, and residents`）'),
    'cc19': dict(kind='再現イラスト',
               plan='図 再現イラスト（光の柱の並び・人は描かない＝A13 の設計の形）｜権利：自作',
               src='A13（`The 13 Pillars of Light`・`incorporate rebar and debris from the building within the columns`・`The proposed image of the collapsed building was replaced with the image of hands`）'),
    'cc20': dict(kind='図解',
               plan='図 時間の帯（2022年6月1日 土地を売る命令〈1億2,000万ドル〉→ 6月24日 和解の最終の命令＝崩落から1年 → 7月27日 売却を終えたと報告）｜権利：自作',
               src='A18 p.2・p.4（`$120,000,000`・`to fund the Allocation Settlement Agreement`）・A17 p.1・p.15（`DONE and ORDERED in Chambers at Miami-Dade County, Florida on this 24th day of June`）・A19'),
    'cc21': dict(kind='写真',
               plan='N#28（新しい倉庫の柱の標本）｜副題：倉庫の証拠（2023年5月）｜権利：A｜注：—',
               src='AC p.16・AC p.79（予定の図）・A04（`The team will now focus on writing its final report`）'),
    'cc22': dict(kind='図解',
               plan='図 一覧（勧告の題目の候補＝アイコン：設計と工事の質・決まりを守らせること・新しい建物の決まり・記録の保管と点検・今ある建物の診断と手入れ・教育と訓練＝AC p.17）｜権利：自作',
               src='AC p.17・A05（`potential topics for its recommendations, including quality and design of construction; code enforcement and records retention policies; and building inspections`）'),
    'cc23': dict(kind='写真',
               plan='TL の別の秒 か N#71（試験中の MAST）｜副題：実物大の試験（ミネソタ大学）｜権利：A推定／A｜注：—',
               src='AC p.61（`further research could lead to improvements in the ACI 318 code requirements for punching shear capacity`）'),
    'cc24': dict(kind='パネル',
               plan='panel この動画の3つの問い（①に印）｜権利：自作',
               src='—（c107）'),
    'cc25': dict(kind='再現イラスト',
               plan='図 再現イラスト A1【正面から】プールデッキ → 塔の下の継ぎ目 → 真ん中と東（流れの矢印・「推定」の札）｜札：推定｜権利：自作',
               src='TR0475・TR0476（`it was insufficient strength and reinforcement detailing at the connection between the pool deck and the tower that caused the deadly partial collapse of the tower`）'),
    'cc26': dict(kind='パネル',
               plan='panel 3つの問い（②に印）｜権利：自作',
               src='TR0474（`Loads added to the structure over its 40-year life and lack of durability of the structure and waterproofing system eroded the very low margins of safety to the point of failure by early June 2021.`）'),
    'cc27': dict(kind='写真',
               plan='N#53（試験のあとの標本＝プールデッキの継ぎ目の壊れ方）｜副題：試験のあとの継ぎ目（2025年）｜権利：A｜注：—',
               src='TR0473（`Champlain Towers South was, therefore, a very vulnerable building from its earliest days.`）'),
    'cc28': dict(kind='パネル',
               plan='panel 3つの問い（③に印）｜権利：自作',
               src='GJ p.18・AC p.61・TR0281'),
    'cc29': dict(kind='写真',
               plan='TFV@最後の言葉（調査を率いた1人が話す区間）｜副題：NIST の技術的知見の動画（2026年6月）｜権利：A｜注：公務の人の顔は可・名前は出さない。代わり＝S#27（夜の窓の明かり・イメージ）',
               src='TR0480・TR0481（`No one in the U.S. should ever have to go to bed wondering if their building will collapse during the night.`）'),
    'cc30': dict(kind='パネル',
               plan='panel コメントの問い｜権利：自作',
               src='—（§B3-7b）'),
}

SPEC = {
    # ── 🆕 ⑤b-3（2026-10-06）：A4 別の建物（cc10）・A5 記念の光の柱（cc19）＝`tools/illu.py` の「A4・A5」の節 ──
    # cc10（4.14秒・1行）＝大陪審の報告 p.20：市は建物に危険の赤い札を貼り、住民全員にすぐ出るよう命じた（建物の名は出さない・人は描かない）
    "cc10": dict(
        fig=("illu", dict(
            place="A4", rec="GJ p3023（別の建物＝10階建て）",
            steps=[dict(state=dict(a4red="on"), delay=0.6, rec=A4R["red"],
                        tag=dict(t="危険の赤い札", at="red", off=(90, -90)))])),
    ),
    # cc19（13.48秒）＝町の発表（A13）。1行目：13本の光の柱（柱の中に鉄筋とがれき）／2行目：案の崩れた建物の絵 → 手の絵／
    #   3行目（費用・工事）：寄るだけ（費用の数は語りと字幕）
    "cc19": dict(
        fig=("illu", dict(
            place="A5", rec="A13 p5102（町が8月に最終的に認めた記念の場所）",
            steps=[dict(state=dict(a5pil="on", a5rebar="on"), delay=0.3, dur=2.0, rec=A5R["pillar"],
                        tag=dict(t="鉄筋とがれきを中に", at="mid", off=(90, -120))),
                   dict(state=dict(a5panel="hands"), delay=0.2, rec=A5R["hands"],
                        tag=dict(t="手の絵", at="panel", off=(-40, -70), anchor="end", delay=2.4)),
                   dict(state=dict(cam=1.05), delay=0.2, dur=4.0)])),
    ),
    # ── 🆕 ⑤b-2（2026-10-06）：案C の置き場 A1（南から見た塔）＝まとめ（冒頭の問いへ戻す型）。秒は narration.json の実測（0〜4.25／4.74〜8.88）
    # cc25＝「推定」。1行目：プールデッキが崩れ → 流れの矢印（デッキ → 塔の下の継ぎ目 → 塔）→ 真ん中が落ち、1秒遅れて東（順番＝TR0093）／
    #   2行目：継ぎ目へ寄る（強さと鉄筋の組み方が足りなかった＝TR0475・0476）
    "cc25": dict(
        fig=("illu", dict(
            place="A1", rec="TR p1475・p1476（塔の部分的な崩れは、プールデッキと塔の継ぎ目の強さと鉄筋の組み方の不足による）",
            assume="推定（NIST の見立て）",
            steps=[dict(state=dict(a1deck="fell", a1flow="on", a1mid="fall", a1east="fall"), delay=0.3, rec=IL_REC["flow"],
                        # ⑤b-2 の下見：札が左下の出典の行（y884）に重なった＝崩れたあとに空く右の空へ
                        tag=dict(t="プールデッキ → 継ぎ目 → 塔", at="deck", off=(260, -260))),
                   dict(state=dict(cam=1.08), delay=0.2, dur=3.2, rec="TR p1476",
                        tag=dict(t="継ぎ目の強さ・鉄筋", at="joint", off=(140, -150)))], camc="joint")),   # ⑤b-2 の echo：複写にしない
    ),
    # ── 🆕 ⑤b-5（2026-10-06）：時間の帯（`tools/axis.py`・門番 check_axis）──
    # cc20（13.78秒＝0〜5.02／5.51〜10.59／11.09〜13.78）＝1行目「2022年6月1日、土地を売ることを認めた」（売却の命令 p.4）／2行目「1億2,000万
    #   ドル」の札（同 p.2）／3行目「和解が、最終的に認められた」で6月24日（最終の命令 p.15）と、予定の一覧の「売却を終えたと報告」（7月27日）
    "cc20": dict(
        t="裁判所の命令", s="崩落の翌年",
        fig=("axis", dict(ss.AX_SALE, steps=[
            dict(add=ss.ax("sale"), cur="2022-06-01"),
            dict(add=dict(k="chips", at="2022-06-01", chips=["1億2,000万ドル"], rec="A18 p7104")),
            dict(add=[ss.ax("final"), dict(k="chips", at="2022-06-24", chips=["崩落からちょうど1年"], rec="A17 p7015"), ss.ax("sold")],
                 cur="2022-06-24")],
            note="", src=ss.src(["A18 p7102・p7104", "A17 p7015", "A19 p7201"]))),
    ),
}
