# -*- coding: utf-8 -*-
"""つかみ c101–c109（9カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c1.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep22/make_plan22.py` で
  映像方針の一覧 `ref/ep22/eizou_build/list22.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典から
  機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット（台本の画は元の予定）。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c101': dict(kind='写真',
               plan='🔧 R04｜区間 8.0〜18.52秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：海の底で見つかった尾部（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：🔧 区間＝何も無い海の底から尾部が現れて近づく（④の「10秒目から」→8秒から＝尾部は10秒ごろ遠くに見え始める）。焼き込み Depth (m): 3775 は残る＝語り「約3,800メートル」と合う｜台本の画（🔧映像方針で替えた＝元の予定）：実写 ROV「尾部」（NTSB ドケットの Pelagic video 1 of 2＝`04_ROV SNIPS-Rel.mp4`・2023-06-22・撮影は Pelagic Research Services の ROV＝第三者＝引用・額装・改変なし・出典「映像：Pelagic Research Services（米沿岸警備隊・NTSB 公開）」・左上の焼き込み「Depth (m): 3775」は残る＝語りは「約3,800メートル」・冒頭の区間は前半（10秒目から尾部）・秒は映像方針で＝副題「2023年6月22日の海の底」）',
               src='USCG p.7〈vii〉（`discovered the aft tail cone and other debris of the TITAN on the seafloor.`）・TSB（`to approximate the depth of the ocean floor at the location of the Titanic’s bow`）'),
    'c102': dict(kind='写真',
               plan='U022｜区間 249.0〜257.5秒｜倍率 1.01（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：6月22日の記者会見（米沿岸警備隊）｜動き：映像｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 888022）｜注：第1管区の司令官が話す・254〜255秒にカメラが少し揺れる（1秒1コマで見た）｜台本の画：実写 USCG の記者会見「残骸の発見」（DVIDS 888022・2023-06-22・A・登壇は公的な任務の人・語りは会見の発言を引かない＝副題「6月22日の記者会見（米沿岸警備隊）」）',
               src='USCG p.7〈vii〉（`which occurred at approximately 10:47 a.m. on June 18, 2023`）・TSB §1.3.3（`The U.S. Coast Guard indicated that the debris field was conclusive evidence of a catastrophic loss of the submersible.`）'),
    'c103': dict(kind='写真',
               plan='🔧 U012｜区間 186.0〜192.2秒｜倍率 0.92（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：捜索に加わった米空軍州兵の救難機（6月21日）｜動き：映像｜権利：A（米空軍州兵＝第106救難航空団の職務・連邦の任務の扱いが弱い所）｜出典の行：米空軍州兵 第106救難航空団（DVIDS 888012）｜注：🔧 副題「米軍の輸送機」→「米空軍州兵の救難機」（HC-130J＝捜索救難機・DVIDS の説明「沿岸警備隊の捜索を支援」）。誘導路を進む機体（1秒1コマで見た）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 HC-130J の B-roll（DVIDS 888012・2023-06-21・A・基地での撮影＝副題「捜索に出た米軍の輸送機（6月21日）」）',
               src='NTSB p.9（`All five persons on board the vessel died.`）・USCG p.35〈27〉（`suffered a catastrophic implosion`）'),
    'c104': dict(kind='写真',
               plan='🔧 R07｜区間 94.44〜101.7秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：海の底に残った前のドーム（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：🔧 副題を見えている物に・区間は④の「前半」→後半（前のドームに近づく＝遠い前半より絵がはっきり）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 ROV「前のドーム」（NTSB ドケットの Pelagic video 2 of 2＝`07_ROV SNIPS-Rel.mp4` の前半・第三者＝引用・額装＝副題「海の底の残骸（6月22日）」）',
               src='NTSB p.36（`mission specialists inside the Titan and the crew of a small boat on the surface heard a “loud bang”`）'),
    'c105': dict(kind='写真',
               plan='🔧 R07｜区間 30.0〜36.44秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：残骸が詰まった後ろのドーム（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：🔧 副題を見えている物に（後ろのドームと炭素繊維の破片）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 ROV「後ろのドーム」（07 の後半・第三者＝引用・額装＝副題「海の底の残骸（6月22日）」）',
               src='USCG p.233〈225〉（`was caused by a shift in the TITAN’s position within its frame`）・TSB §2.1.1（`4 days before the subsequent dive on 19 July 2022`）'),
    'c106': dict(kind='写真',
               plan='U022｜区間 342.0〜349.5秒｜倍率 1.02（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：6月22日の記者会見（米沿岸警備隊）｜動き：映像｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 888022）｜注：司令官（正面→下を向いて読む）・334〜341秒のカメラの動きのあと（1秒1コマで見た）｜台本の画：実写 USCG の記者会見 888022（別の区間）',
               src='NTSB p.36（`The Titan completed three additional dives following dive 80`）・NTSB p.36（`the submersible reached 3,840 meters (12,598 feet) on dives 81 and 82`）'),
    'c107': dict(kind='写真',
               plan='🔧 U734｜区間 92.3〜97.0秒｜倍率 0.60（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：捜索の指令センター（6月20日・ボストン）｜動き：映像｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 887734）｜注：🔧 区間＝表紙「Submersible TITAN / R/V POLAR PRINCE / 18 June 2023」の書類（3つの問いの背に事件そのものの記録）・倍率0.66（1秒1コマで見た）｜台本の画（🔧映像方針で替えた＝元の予定）：実写 指令センターの B-roll（DVIDS 887734・2023-06-20・ボストンの第1管区・当直の隊員＝公的な任務・A・器 2720×1530 の実効の幅は映像方針で測る＝副題「捜索の指令センター（6月20日・ボストン）」）',
               src='—'),
    'c108': dict(kind='写真',
               plan='R04｜区間 28.61〜35.25秒｜倍率 1.00（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：額装（第三者）｜副題：海の底で見つかった尾部（6月22日）｜動き：映像（等速）｜権利：第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22。米沿岸警備隊と米運輸安全委員会が公開）｜出典の行：映像：Pelagic Research Services（米沿岸警備隊・米運輸安全委員会 公開）｜注：尾部の切れ口に寄る→横から（26秒の照明の変わり目より後）｜台本の画：実写 ROV「尾部」（04 の後半・冒頭の c101 と別の区間・第三者＝引用・額装）',
               src='USCG p.1（`Report of the Marine Board of Investigation`）・NTSB p.76（`Report Date: October 2, 2025`）・TSB §4.2.4（`It was officially released on 17 June 2026.`）'),
    'c109': dict(kind='写真',
               plan='U022｜区間 902.0〜906.1秒｜倍率 1.05（区間の秒÷扉を除いた中身の秒＝narration.json の実測）｜見せ方：全面｜副題：6月22日の記者会見（米沿岸警備隊）｜動き：映像｜権利：A（米沿岸警備隊の職員の職務・DVIDS）｜出典の行：米沿岸警備隊（DVIDS 888022）｜注：→ 第1章の扉（頭の c201 が共同の写真＝扉の地は方眼だけ card_mix=0）｜台本の画：実写 USCG の記者会見 888022（別の区間）→ 第1章の扉',
               src='—'),
}

SPEC = {}
