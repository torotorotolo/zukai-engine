# -*- coding: utf-8 -*-
"""第6章　炭素繊維の筒 c701–c719（19カット）。22本目（タイタン号のリメイク）。

■ 🔴 2026-10-14（⑤b-1）：21本目（9.11 米国同時多発テロのリメイク）の中身を空にした＝git の `35fab37`（`git show 35fab37:tools/cuts/c7.py`）。
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
    'c701': dict(kind='図解',
               plan='見る向き：横から｜台本の画：図 線 タイタンの横の線画（NTSB 図3 をなぞる＝筒・チタンの輪・ドームの位置）',
               src='TSB §1.13（`Carbon fibre is widely used in commercial aviation because of its high strength, low weight, and ability to be moulded.`）'),
    'c702': dict(kind='図解',
               plan='台本の画：図 模式 引っ張りと圧縮（左＝旅客機の胴体・中の空気が外へ押す＝引っ張り／右＝深海の殻・外から押しつぶす＝圧縮。🔴 旧版 c208 の札「強＝圧縮」は逆＝札は米沿岸警備隊の書くとおり）',
               src='USCG p.274〈266〉（`Carbon fiber has demonstrated its effectiveness in other applications where the material is primarily under tension`）・p.274〈266〉（`a scenario for which carbon fiber has no established track record and is generally understood to be less effective`）'),
    'c703': dict(kind='図解',
               plan='台本の画：図 模式 ふつうの深海の潜水艇の殻（鋼かチタンの球）とタイタンの殻（炭素繊維の筒）の並べ図',
               src='TSB §1.13（`submersibles used for deep-ocean diving are typically constructed of steel or titanium,`…`and the pressure hull for human occupancy is typically spherical in shape`）・TSB 脚注53（`With the exception of the Titan, the TSB is not aware of any other carbon-fibre pressure hulls for human occupancy used for deep-ocean diving.`）'),
    'c704': dict(kind='図解',
               plan='台本の画：図 模式 同じ並べ図（タイタンの側に「軽い」「中が広い」の札）',
               src='TSB §1.13（`which creates cost savings when it comes to systems for transporting and launching and recovering the submersible.`）・§1.13（`OceanGate’s decision to use carbon fibre in the construction of the Titan was largely based on these factors.`）'),
    'c705': dict(kind='図解',
               plan='🔧 注：🔧 人の言葉＝輪郭＋吹き出し（§0-3）｜新しい画（映像方針）：図 再現 人の輪郭（元運航部長＝顔は描かない）＋吹き出しの英字 `better in compression than tension`・訳は字幕｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 元運航部長の証言の一節（NTSB p.25 が引く英字＝`better in compression than tension`・訳は字幕）',
               src='NTSB p.25（`the CEO chose carbon fiber because he believed it was “better in compression than tension.”`）'),
    'c706': dict(kind='図解',
               plan='🔧 注：🔧 再現→棒（§0-3）｜新しい画（映像方針）：図 棒 2015年の設計書の数（望み6,000m・受け入れ3,000m の深さの棒＝海の青・安全率の目標2.25＝黄）｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 2015年の設計書の要点（2015年6月25日・望み6,000m・受け入れ3,000m・安全率の目標2.25）',
               src='TSB §1.12.1（`On 25 June 2015, this company produced a design document that showed that OceanGate wanted a submersible made primarily of carbon fibre rated up to 6000 m`）・§1.12.1（`OceanGate had a goal of 2.25 for the safety factor, but that it was willing to accept 1.5.`）'),
    'c707': dict(kind='図解',
               plan='台本の画：図 棒 安全率のしくみ（潜ってよい深さの棒と、壊れる深さの棒・その比＝安全率）',
               src='NTSB p.24（`Safety factor in submersible design is the ratio between the failure depth and the maximum allowable operational depth.`）'),
    'c708': dict(kind='図解',
               plan='台本の画：図 棒 設計書の安全率（2.19・2.21 の棒・目標2.25 と下限1.5 の線）',
               src='TSB §1.12.1（`had a safety factor of 2.19 with grade 5 titanium end domes and a safety factor of 2.21 with carbon fibre end domes.`）・TSB 脚注45（`At the time, OceanGate was basing its safety factor on the American Society for Mechanical Engineers standard`…`that required a minimum safety factor of 1.5.`）'),
    'c709': dict(kind='図解',
               plan='台本の画：図 棒 深さの比べ（約1万3,200m＝壊れる深さの計算・6,000m＝目標・約3,800m＝タイタニック＝縮尺どおり）',
               src='NTSB p.25（`the analysis indicated an implosion depth about 13,200 meters (43,307 feet)`）'),
    'c710': dict(kind='図解',
               plan='台本の画：図 再現 NTSB p.63 の要点（「完全な形と繊維の向きを仮定した、理論の模型」の英字の一節）',
               src='NTSB p.63（`were based on theoretical models of composite structures that assumed perfect geometry and fiber orientation`）・p.63（`To rely on the models, OceanGate should have validated them through physical testing`）'),
    'c711': dict(kind='図解',
               plan='台本の画：図 模式 3分の1の模型（炭素繊維の筒と炭素繊維のドーム・加圧の矢印）',
               src='TSB §1.12.1（`In December 2015, OceanGate conducted a pressure test on this one-third scale model at the UW-APL`…`One of the carbon fibre end domes failed at pressures equivalent to depths of around 3000 m.`）'),
    'c712': dict(kind='図解',
               plan='🔧 注：🔧 人の言葉＝輪郭＋吹き出し（§0-3）｜新しい画（映像方針）：図 再現 人の輪郭（CEO＝顔は描かない）＋吹き出しの英字（USCG p.111 が引く手紙）・訳は字幕｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 CEO の手紙の一節（USCG p.111 が引く英字＋訳は字幕）',
               src='USCG p.111〈103〉（`Fortunately, there was no damage to the main cylindrical section, which is the critical part and a shape that is far better understood.`）'),
    'c713': dict(kind='図解',
               plan='台本の画：図 棒 模型の試験の深さと目標（4,500m の線に届かない・回ごとの値は3冊で割れる＝棒にしない・目標の線と「届かず」の札だけ）',
               src='USCG p.114〈106〉（`which was less than the 4,500 m (14,764 feet) that was the target max pressure depth for TITAN’s operations.`）・NTSB p.25（`According to the CEO, that model had a delamination in the carbon fiber cylinder.`）'),
    'c714': dict(kind='図解',
               plan='台本の画：図 模式 船級のしくみ（船の持ち主→民間の団体が設計を見る・工事に立ち会う・試験を確かめる→証明書→定期の検査）',
               src='NTSB p.22（`Classification societies are nongovernmental organizations that establish and maintain standards for shipbuilding and operations.`）・p.22（`To maintain a valid certificate of classification, a vessel must undergo additional periodic surveys`）'),
    'c715': dict(kind='図解',
               plan='台本の画：図 帯 船級の年表（2016年 船級の相談→2018年 あきらめる→2019年2月 ブログ）',
               src='NTSB p.22（`the company planned to class the submersible through Lloyd’s Register or DNV.`）・NTSB p.23（`the OceanGate CEO ultimately decided classing the Titan would take too long`…`In 2018, OceanGate abandoned classing efforts.`）'),
    'c716': dict(kind='図解',
               plan='台本の画：図 再現 会社のブログの題「Why Isn’t Titan Classed?」と一節（英字＋訳は字幕）',
               src='TSB §1.26.3.1（`On 21 February 2019, OceanGate posted a blog entitled “Why Isn’t Titan Classed?”.`）・NTSB p.24（`by itself, classing is not sufficient to ensure safety.`）'),
    'c717': dict(kind='図解',
               plan='台本の画：図 再現 NTSB 脚注17 の要点（「新しい技術を確かめる道はある」「旅客や貨物を運ぶ船に『実験的』の区分は無い」）',
               src='NTSB p.23（`Classification societies have a path for owners to prove seaworthiness of new technology.`）・p.23（`have no “experimental” design endorsement for vessels carrying passengers or cargo.`）'),
    'c718': dict(kind='図解',
               plan='🔧 注：🔧 人の言葉＝輪郭＋吹き出し（§0-3）｜新しい画（映像方針）：図 再現 人の輪郭（CEO＝顔は描かない）＋吹き出し2つ（2021年のテレビの取材の英字）・訳は字幕｜台本の画（🔧映像方針で替えた＝元の予定）：図 再現 2021年のテレビの取材の一節（USCG p.301 が引く英字＋訳は字幕）',
               src="USCG p.301〈293〉（`“I’d like to be remembered as an innovator.`）・p.301〈293〉（`And I've broken some rules to make this.”`）"),
    'c719': dict(kind='図解',
               plan='台本の画：図 再現 社員の懸念の一節（NTSB p.47 が引く英字＋訳は字幕）',
               src='NTSB p.47（`who had previous experience as an engineer/machinery technician in the US Coast Guard`）・p.47（`the company accepting paying clients as “mission specialists.”`）・p.47（`you can’t just change the title of a person when you’re receiving compensation.”`）・p.47（`The technician resigned following this conversation`）'),
}

SPEC = {}
