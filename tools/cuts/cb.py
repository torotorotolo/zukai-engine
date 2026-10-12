# -*- coding: utf-8 -*-
"""第10章　その後の空 cb01–cb19（19カット）。21本目（9.11 米国同時多発テロのリメイク）。

■ 🔴 2026-10-12（⑤b-1）：20本目（日本航空123便のリメイク）の中身を空にした＝git の `f0095bd`（`git show f0095bd:tools/cuts/cb.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep21/make_plan21.py` で
  映像方針の一覧 `ref/ep21/eizou_build/list21.tsv`（了承②ずみ・E 0）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット（台本の画は元の予定）。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'cb01': dict(kind='写真',
               plan='W593｜区間 26.0〜34.0秒｜倍率 1.01（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜副題：当日の夜、ホワイトハウスでの演説｜動き：映像｜権利：A（WHCA の職務・NARA 6171390・use=Unrestricted）｜出典の行：Courtesy George W. Bush Presidential Library（NARA 6171390）｜注：大統領だけ・音は使わない｜台本の画：実写 当日の夜の演説（NARA 6171390・WHCA・A・720×486＝全画面・大統領だけ＝副題「当日の夜、ホワイトハウスでの演説」）',
               src='委員会報告 p326（`At 8:30 that evening, President Bush addressed the nation from the White House`）'),
    'cb02': dict(kind='図解',
               plan='台本の画：図 模式 全米の地図（9月13日・空港の点が戻り始める）',
               src='委員会報告 p327（`On the morning of September 13, the national airspace reopened for use by airports that met newly improvised security standards`）・p556（`effective 11:00 A.M. on September 13, 2001`）'),
    'cb03': dict(kind='写真',
               plan='🔧 DOD912｜副題：9月12日のペンタゴン（国防長官と現場を回る大統領）｜動き：左へ流す｜権利：A（国防総省の職務）｜出典の行：米国防総省｜注：🔧 WHTV 600（30分の未編集テープ）→ 国防総省の写真｜台本の画（🔧映像方針で替えた＝元の予定）：実写 WHTV 600 ペンタゴンを訪れる大統領（9月12日・WHCA・A・SD＝全画面＝副題「9月12日のペンタゴン」）',
               src='materials.md §1-2（WHTV 600＝9/12 のペンタゴン視察・未編集 30:29＝目録の説明。中身の秒は映像方針で）・委員会報告 p559 注61（`On the evening of September 12, the President was at the Pentagon`）'),
    'cb04': dict(kind='写真',
               plan='🔧 FEMA3905｜副題：9月14日の世界貿易センターの跡（救助の人たちに話す大統領）｜動き：ゆっくり寄る｜権利：A（米陸軍・FEMA の職務）｜出典の行：FEMA（SFC Thomas R. Roberts）｜注：🔧 WHTV 609 → FEMA の写真。消防士と作業員＝捜索の任務｜台本の画（🔧映像方針で替えた＝元の予定）：実写 WHTV 609 世界貿易センターの跡を訪れる大統領（9月14日・WHCA・A・消防と救助の人の顔＝職務・全画面＝副題「9月14日の世界貿易センターの跡」）',
               src='materials.md §1-2（WHTV 609・610／NARA 6171391＝9/14 の大統領と消防・警察・救助＝目録の説明。中身の秒は映像方針で）'),
    'cb05': dict(kind='図解',
               plan='台本の画：図 模式 年表（2001年11月の法律の印）',
               src='委員会報告 p391（`In November 2001, Congress passed and the President signed the Aviation and Transportation Security Act. This act created the Transportation Security Administration (TSA)`）・法律（`November 19, 2001`）'),
    'cb06': dict(kind='フリー素材',
               plan='TSA20｜副題：イメージ（2020年の空港の保安検査）｜動き：右へ流す｜権利：F（CC BY 2.0）｜出典の行：Tony Webster（CC BY 2.0）｜注：20%に数えない・顔の分かる客は顔だけモザイク｜台本の画：イメージ 現在の空港の保安検査（後年・フリー素材＝副題「イメージ（現在の空港）」）',
               src='法律（`the screening shall take place before boarding and shall be carried out by a Federal Government employee`・`except as otherwise provided in section 44919 or 44920`）・委員会報告 p2（`under a contract with American Airlines`）・p3（`had contracted out the work`）'),
    'cb07': dict(kind='図解',
               plan='台本の画：図 模式 年表（2001年11月の法律から1年の帯）',
               src='法律（`Not later than 1 year after the date of enactment of this Act, the Under Secretary of Transportation for Security shall deploy at all airports in the United States where screening is required`）'),
    'cb08': dict(kind='フリー素材',
               plan='DOOR15｜副題：イメージ（2015年の旅客機の操縦室の扉）｜動き：下へ流す｜権利：F（CC BY 2.0 de）｜出典の行：Mattes（CC BY 2.0 de）｜注：20%に数えない・縦長｜台本の画：イメージ 現在の旅客機の操縦室の扉（後年・フリー素材＝副題「イメージ」）',
               src='法律（`requiring the strengthening of the flight deck door and locks`・`to ensure that the door cannot be forced open from the passenger compartment`）'),
    'cb09': dict(kind='図解',
               plan='台本の画：図 模式 操縦室の扉（当時＝閉めて鍵の決まり・守られないこともあった→強い扉）',
               src='法律（`requiring that such flight deck doors remain locked while any such aircraft is in flight`）・委員会報告 p85（`required air crews to keep the cockpit door closed and locked in flight`・`This requirement was not always observed or vigorously enforced`）'),
    'cb10': dict(kind='図解',
               plan='台本の画：図 模式 同じ',
               src='委員会報告 p85（`even a hardened cockpit door would have made little difference in a hijacking`）'),
    'cb11': dict(kind='図解',
               plan='台本の画：図 模式 年表（2002年11月の法律・国土安全保障省の印）',
               src='委員会報告 p391（`which is now part of the Homeland Security Department`・`In November 2002, both the Homeland Security Act and the Maritime Transportation Security Act followed`）'),
    'cb12': dict(kind='図解',
               plan='台本の画：図 模式 年表（2002年11月 委員会・2004年7月 報告）',
               src='委員会報告 p.xv（`the Congress and the President created the National Commission on Terrorist Attacks Upon the United States`・`we held 19 days of hearings`）'),
    'cb13': dict(kind='図解',
               plan='台本の画：図 模式 委員会の勧告の箱（乗ってはいけない人の名簿・爆発物の検査）',
               src='委員会報告 p393（`Improved use of "no-fly" and "automatic selectee" lists should not be delayed`）'),
    'cb14': dict(kind='図解',
               plan='台本の画：図 模式 同じ箱（爆発物の検査に印）',
               src='委員会報告 p393（`The TSA and the Congress must give priority attention to improving the ability of screening checkpoints to detect explosives on passengers`）'),
    'cb15': dict(kind='写真',
               plan='🔧 FEMA3894｜副題：9月14日の世界貿易センターの跡｜動き：上へ流す｜権利：A（FEMA の職務）｜出典の行：FEMA（Andrea Booher）｜注：🔧 WHTV 610 → FEMA の写真（人は小さい）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 WHTV 610 世界貿易センターの跡（9月14日・WHCA・NARA 6171391・A・消防と救助の人の顔＝職務・全画面＝副題「9月14日の世界貿易センターの跡」）',
               src='—'),
    'cb16': dict(kind='図解',
               plan='台本の画：図 模式 2つの調べの箱（委員会＝空の側／NIST＝建物の側）',
               src='NIST（`Final Report on the Collapse of the World Trade Center Towers`）'),
    'cb17': dict(kind='写真',
               plan='🔧 PENT23｜副題：2023年のペンタゴン（空撮）｜動き：ゆっくり引く｜権利：A（国防総省の職務）｜出典の行：米国防総省｜注：🔧 ✅ 了承②（2026-10-12）＝2025年の中庭（無人機の展示が画面の大半）から替えた・語りの年も 2023年に（decide21.py R2-026 → make21.py）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 pentagon_court_pre（ペンタゴンの中庭・2025年7月・A・全画面・ゆっくり寄る＝副題「ペンタゴンの中庭（2025年）」。中庭に無人機の展示が写る＝映像方針で原寸を見て、締めに合わなければ別の点）',
               src='—'),
    'cb18': dict(kind='写真',
               plan='MEM24B｜副題：現在の93便の追悼の場（2024年の空撮）｜動き：ゆっくり寄る｜権利：C（CC0）｜出典の行：Designism（CC0）｜注：CC0｜台本の画：実写 93便の追悼の場（別の点・後年・全画面＝副題「現在の93便の追悼の場」）',
               src='国立公園局（`Flight 93 National Memorial`）'),
    'cb19': dict(kind='図解',
               plan='台本の画：図 模式 時間の帯（あの朝の4機）',
               src='—'),
}

SPEC = {}
