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

SPEC = {}
