# -*- coding: utf-8 -*-
"""第6章　がれきの下で c701–c720（20カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c7.py`）。
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
    'c701': dict(kind='写真',
               plan='B1@100–104（がれきの山と重機の腕）｜副題：がれきの山（2021年6〜7月）｜権利：A推定｜注：×2.1＝走査で 99〜105 へ広げられるか・無ければ静止画で受ける。代わり＝C1（郡の消防・6月24日＝決め①で使う）',
               src='B05 p.2（`06/24/2021 at 0120 hours`・`Officers responded to a call of a fire alarm and encountered a partially collapsed condominium building.`）'),
    'c702': dict(kind='写真',
               plan='N#18（南どなりのバルコニーから見た現場）｜副題：現場と残った西の部分（2021年7月）｜権利：A｜注：決め⑤＝🅰 引きだけ：⑤b-1 で原寸を見て、家具・写真・服が見分けられる住戸に寄せない（見分けられれば C1・C2 か B1 の引きに替える）',
               src='B06 p.2（`rescuing residents from the part of the building still standing`・`Cherry pickers were used to go floor-by-floor to rescue residents still trapped on their balconies.`）'),
    'c703': dict(kind='写真',
               plan='C6（昼の地上からの全景・救助隊と犬）｜副題：崩れた現場の救助隊（2021年6月24日・郡の消防）｜権利：フロリダ州の公記録（PD-FLGov の可能性）｜注：決め①＝使う。出典の行は「PD」と書かず「マイアミ・デイド郡消防（フロリダ州の公記録）」。代わり＝F:6717686',
               src="B04（`rescuing 37 occupants from the structure and rubble`・`the largest non-hurricane Search and Rescue mission in Florida's history`）"),
    'c704': dict(kind='図解',
               plan='図 地図【上から】町の中の位置（現場 → 町のコミュニティセンター・道の線だけ）｜権利：自作',
               src='B05 p.2（`residents were escorted to the Surfside Community Center which later become the Family Reunification Center`）'),
    'c705': dict(kind='写真',
               plan='B1@50–56（がれきの山と捜索の列）｜副題：がれきの山と捜索の列（2021年6〜7月）｜権利：A推定｜注：隣家の屋根あり',
               src='GJ p.1（`two-story tall pile of rubble`）'),
    'c706': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='GJ p.1（`Except for a 14-year-old child, who was discovered near the top of the two-story tall pile of rubble, first responders were not successful in rescuing any survivors.`）'),
    'c707': dict(kind='写真',
               plan='F:6717686（都市捜索救助隊ががれきを除く）｜副題：国の都市捜索救助隊（2021年7月1日）｜権利：A（FEMA）｜注：—',
               src='GJ p.1・B02 p.1（`Within hours of the building collapse, FEMA Urban Search & Rescue (US&R) placed multiple task forces on alert`・`On June 25, President Biden signed an Emergency Declaration authorizing federal assistance`）'),
    'c708': dict(kind='写真',
               plan='F:6723299（ペンシルベニア第1隊が12時間の交代に入る準備）｜副題：国の救助隊（2021年7月3日）｜権利：A（FEMA）｜注：決め③＝BY-SA は使わない＝差し込みなし。3行目「外国からも」に合う連邦の写真（DVIDS の外国の隊）があれば⑤b-1 で',
               src='B02 p.1（`each with 70-80 members`・`Teams worked 12-hour shifts in a round-the-clock operation at the site.`）・B01 p.3・B06 p.8（`Israeli, Mexican`）'),
    'c709': dict(kind='写真',
               plan='F:6717685（がれきを除く隊員）｜副題：がれきを除く救助隊（2021年7月1日）｜権利：A（FEMA）｜注：—',
               src='B02 p.1（`hand tools such as jack-hammers, metal and concrete saws, shovels and buckets to peel away multiple layers of rubble`）'),
    'c710': dict(kind='図解',
               plan='図 模式図【横から】がれきの山と残った西の部分（見張りの印＝陸軍工兵隊の構造の専門家）｜権利：自作',
               src='B02 p.2（`monitored the rubble pile to ensure safety of search teams`）・B07 p.1（`the unstable remaining structure`）・B01 p.3（`monitor the rubble pile and standing structure`）'),
    'c711': dict(kind='写真',
               plan='B1@⑤b-1（残った西の部分が大きく写る秒＝138〜143 は使わない）｜副題：残った西の部分（2021年6〜7月）｜権利：A推定｜注：🔴 138〜143（fb_c709）は手前に「MIAMI DADE HOMICIDE」の字のシャツ・手持ちで歩くぼけ（実効 736）＝使わない（チャット4 で見た）。決め⑤＝引きの秒だけ。代わり＝C1・C2（郡の消防＝決め①で使う）か B1@159〜160（重機の銘 ALPI）',
               src='B07 p.1（`authorized the controlled demolition of the remaining structure of the building to eliminate further risk to health and safety`）'),
    'c712': dict(kind='図解',
               plan='図 地図【上から】取り壊しの区域（爆破の区域＝半径約90メートル〈300フィート〉の赤・屋内にいる区域の黄＝B03 の地図の形）｜権利：自作',
               src='B03（`Between 10 p.m. on Sunday, July 4, 2021 and 3 a.m. on Monday, July 5`・`a 300-foot radius around the center of the demolition`）'),
    'c713': dict(kind='写真',
               plan='F:6723297（交代の隊・⑤b-1 で昼か夜か）｜副題：救助の隊（2021年7月3日）｜権利：A（FEMA）｜注：副題は写っている時刻で（夜でなければ「夜の」と書かない）。候補 W1（大統領への説明の映像）',
               src='B07 p.1（`searching for human remains to bring closure to grieving families`）・GJ p.1（`Our community will forever be in debt to the first responders, both local and from abroad`）'),
    'c714': dict(kind='図解',
               plan='図 時間の帯（6月24日 1:22 → 7月20日 20:03＝26日後）｜権利：自作',
               src='A12（`July 20th at 8:03 pm marks the end of the heroic search and recovery efforts when the final person was recovered.`）・GJ p.1（`recovered and identified remains for 98 known persons`）・B04（`until every victim was identified`）'),
    'c715': dict(kind='写真',
               plan='N#16（柱に札）｜副題：証拠の柱に付けた札（2021年7月6日）｜権利：A｜注：—',
               src='A07（`collected more than 200 building elements including columns, beams and pieces of concrete slab`）'),
    'c716': dict(kind='写真',
               plan='N#19（現場を走査するカメラとライダー）｜副題：現場を測る機械（2021年7月）｜権利：A｜注：—',
               src='B02 p.2（`NIST has been conducting remote sensing of the debris pile to determine where pieces of evidence were located.`・`drones and LiDAR`）'),
    'c717': dict(kind='写真',
               plan='N#20（札を付けた部材を警察の護衛で保管所へ）｜副題：警察に守られて運ぶ部材（2021年7月）｜権利：A｜注：🔁 台本の型は B4（2023年の搬送）＝語りの「警察の車に守られて」と年が合う N#20 に',
               src='A07（`transported by police escort to an offsite storage facility`）'),
    'c718': dict(kind='写真',
               plan='B5@11–16.3 は c312 で使う → B5@⑤b-1（倉庫の部材の別の秒）｜差し込み（tail）：2 PC  5.6秒 PC（倉庫の部材の点群のフライスルー）｜副題：倉庫の証拠（2023年）／点群（約17億点）｜権利：A推定｜注：—',
               src='B08（`By the end of July 2021, all of the evidence was moved to secure locations, where it was carefully cataloged`・`1,700,569,894 points`）'),
    'c719': dict(kind='図解',
               plan='図 時間の帯（6月25日 NIST の6人が現地へ → 6月30日 本格的な調査を発表 → 2022年1月28日 証拠を NIST が預かる・札「建設安全チーム法（National Construction Safety Team Act）による調査」）｜権利：自作',
               src='B02 p.2（`On June 25, NIST initially deployed a team of six scientists and engineers`・`On June 30, the agency announced it would support a full technical investigation.`）・B08（`transferred to NIST on Jan. 28, 2022`）・TR0467（`to determine the most likely technical cause or causes of the failure, to recommend specific improvements to building standards, codes and practices`）・B01 p.5（`On June 30, 2021, NIST announced that it was launching a full investigation under the authority of the National Construction Safety Team Act.`）'),
    'c720': dict(kind='写真',
               plan='N#44（現場の空中写真を見る調査団）｜副題：空中写真を見る NIST の調査団｜権利：A｜注：公務の人の顔は可',
               src='—（橋）'),
}

SPEC = {
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）──
    # c710（9.22秒＝0〜4.94／5.43〜9.22）＝不安定な残りの部分・がれきの山の見張り（B07 p.1・B02 p.2・B01 p.3）。人は描かない
    "c710": dict(
        t="不安定な残りの部分", s="がれきの山を見張る",
        fig=("m19", dict(view="rubble",
                         steps=[dict(state=dict(unst="on"), delay=0.3, tag=dict(t="残った西の部分（不安定）", at="bld", to="bld")),
                                dict(state=dict(watch="on"), delay=0.3,
                                     tag=dict(t="陸軍工兵隊が見張る", d="捜索の安全のため", at="watch", to="pile"))],
                         note="建物とがれきの形・見張りの印は模式（人は描かない）",
                         src="FEMA の発表（2021年7月17日） p.2・郡長のメモ（2023年10月26日） p.1・GAO の報告（2024年） p.3")),
    ),
    # ── 🆕 ⑤b-5（2026-10-06）：時間の帯（`tools/axis.py`・門番 check_axis）──
    # c714（10.76秒＝0〜5.10／5.59〜8.49／8.98〜10.77）＝1行目「最後の1人が見つかったのは7月20日…26日後」で点と括弧
    #   （町の頁「8:03p.m., the exact time when the final person was recovered on July 20, 2021」）／2行目「98人、全員の身元」の札
    #   （GJ p.1「recovered and identified remains for 98 known persons」）／3行目（聞き役）はそのまま。午後8時3分は字幕だけ
    "c714": dict(
        t="捜索の終わり", s="2021年6月〜7月",
        fig=("axis", dict(ss.AX_SEARCH, past=[ss.ax("f624", keep=True)], start=dict(cur="2021-06-24"), steps=[
            dict(add=[ss.ax("d26"), ss.ax("last")], cur="2021-07-20"),
            dict(add=dict(k="chips", at="2021-07-20", chips=["98人全員の身元を確認"], rec=["A12 p5101", "GJ p3004"])),
            dict()],
            note=ss.TL_NOTE, src=ss.src(["A12 p5101", "GJ p3004"]))),
    ),
    # c719（12.92秒＝0〜3.54／4.03〜7.52／8.01〜12.92）＝1行目「崩れた次の日に、6人」（FEMA p.2）／2行目「6月30日、本格的な調査を
    #   始めると発表」／3行目「建物の大事故を調べる法律による調査」で法律の名の札（GAO p.5）と、予定の一覧の「証拠を NIST が預かる」（B08）
    "c719": dict(
        t="調査の始まり", s="崩れた次の日から",      # ⚠️ dup：「NIST の調査」は出典の行と札に埋もれた
        fig=("axis", dict(ss.AX_NIST, steps=[
            dict(add=ss.ax("team"), cur="2021-06-25"),
            dict(add=ss.ax("ann"), cur="2021-06-30"),
            dict(add=[dict(k="chips", at="2021-06-30", chips=["建設安全チーム法による調査", "National Construction Safety Team Act"],
                           rec="B01 p5605"), ss.ax("evid")], cur="2022-01-28")],
            note="", src=ss.src(["B02 p5702", "B01 p5605", "B08 p5005"]))),
    ),
    # ── 🆕 ⑤b-6（2026-10-06）：地図 → 箱の型（🔴 ルール §5b-116①＝資料に位置の値〈距離・方角・座標〉が無い・drift は門番 check_drift ③ を
    #    正直には通せない）──
    # c704（6.58秒＝0〜3.45／3.94〜6.58）＝流れ図（町の警察の会報 p.2）。1行目で避難の矢印・2行目で再会の場所の札
    "c704": dict(
        t="避難した先", s="町の施設へ",      # ⚠️ dup：「町の警察の記録」は出典の行・「残った部分から」は箱の写し
        fig=("boxes", dict(view="flow", layout=ss.FL_EMPTY, steps=[
            dict(add=[ss.fl("e_res"), ss.fl("e_cc"), ss.ce("e_res", "e_cc", lab="避難")]),
            dict(add=dict(k="chip", at="e_cc", t="のちに家族の再会の場所", rec="B05 p5302", dy=60))],
            src=ss.src(["B05 p5302"]))),
    ),
    # c712（9.87秒＝0〜4.62／5.11〜9.87）＝書類の再現図（郡の発表＝記録は時刻と半径の数だけ・屋内にいる区域〈黄〉は地図の画像だけ）。
    #   1行目で取り壊しの時刻・2行目で近づけない区域
    "c712": dict(
        t="取り壊しの知らせ", s="時刻と区域",
        fig=("boxes", dict(view="form", form=ss.FORM_B03, steps=[
            dict(add=[dict(k="paper"), dict(k="fill", f="取り壊し")]),
            dict(add=dict(k="fill", f="近づけない区域"))],
            note="欄の字は原文のまま・様式は再現・300フィート＝約91メートル", src=ss.src(["B03 p5201"]))),
    ),
    # ── 🆕 ⑤b-7a（2026-10-06）：写真・映像（救助の人は公務・決め⑤＝住戸の中は引きだけ）──
    "c701": dict(t="未明の通報", s="がれきの山と救助の重機（2021年7月）",
                 photo=P("n18_from_south"), **ss.kind(P("n18_from_south"))),
    "c702": dict(t="残った部分からの救助", s="残った西の部分と消防車（2021年6月24日・郡の消防）",
                 photo=P("c01_mdfr1"), **ss.kind(P("c01_mdfr1"))),
    # c703＝灰色の車のナンバーを束でモザイク（PD＝§B2-2b の考え方）
    "c703": dict(t="郡の消防の救助", s="崩れた現場の救助隊（2021年6月24日・郡の消防）",
                 photo=P("c06_mdfr6"), **ss.kind(P("c06_mdfr6"))),
    "c705": ss.vid("c705", t="真ん中と東のがれき", s="崩れたがれきの山（2021年6〜7月）"),
    # c707＝束で左を切った（重機の「CAT 336E」）
    "c707": dict(t="国の救助隊の出動", s="機材を運ぶ救助隊員（2021年7月1日）",
                 photo=P("f6717686_debris"), **ss.kind(P("f6717686_debris"))),
    "c708": dict(t="5つの救助隊", s="交代の前にひざ当てを付ける救助隊員（2021年7月3日）",
                 photo=P("f6723299_pa_tf1"), **ss.kind(P("f6723299_pa_tf1"))),
    "c709": dict(t="手作業の捜索", s="がれきをバケツで運び出す救助隊（2021年7月1日）",
                 photo=P("f6717685_debris"), **ss.kind(P("f6717685_debris"))),
    "c711": ss.vid("c711", t="取り壊しの決定", s="残った西の部分（2021年6〜7月）"),
    "c713": dict(t="続く捜索", s="打ち合わせをする救助隊（2021年7月3日）",
                 photo=P("f6723297_team"), **ss.kind(P("f6723297_team"))),
    # c715＝束で上（テントの「Milwaukee」）と右（Hyundai）を切った
    "c715": dict(t="集められた証拠", s="証拠の柱に付けた札（2021年7月6日）",
                 photo=P("n16_column_tag"), **ss.kind(P("n16_column_tag"))),
    "c716": dict(t="証拠の位置の記録", s="海に面したバルコニーに並べた測量の機械（2021年7月）",
                 photo=P("n19_lidar"), **ss.kind(P("n19_lidar"))),
    # c717＝束で上を切った（奥のトラックの会社名と電話番号）
    "c717": dict(t="倉庫への運び出し", s="番号を書いて並べた床版と柱（2021年7月）",
                 photo=P("n20_police_escort"), **ss.kind(P("n20_police_escort"))),
    # c718＝2行目（点群のフライスルー PC）は尻の映像の差し込み＝⑤b-7c
    "c718": ss.vid("c718", t="記録された証拠", s="倉庫の証拠（2023年）",
                   tail=ss.tailv("c718", at=1, t="測った証拠の形", s="証拠の部材の点群（約17億点）")),
    "c720": dict(t="ここからは原因", s="空中写真を見る NIST の調査団",
                 photo=P("n44_aerial_photos"), **ss.kind(P("n44_aerial_photos"))),
}
