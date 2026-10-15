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

# ══════════════════════════════════════════════════════════
#  🆕 ⑤b-4（2026-10-15）：図解 第6章（19カット）＝模式図 `tools/mech22.py`・時間の帯（axis）・棒（qty）
# ══════════════════════════════════════════════════════════
#   🔴 章の札「炭素繊維の筒」と4字以上同じ並びを見出し・副題に入れない（門番 dup）。人の言葉は輪郭（顔は描かない）＋吹き出しの英字（訳は字幕）。
#      CEO の名前は画面に出さない（語りだけ）。色＝役の色（会社＝橙・米沿岸警備隊＝青・米運輸安全委員会＝緑・カナダ＝紫）
#   🔧 c706・c709・c713：映像方針の「棒」→ **深さの物差し（ruler・縦・縮尺どおり）**＝目標の深さ・壊れる深さの計算・運航の目標は「線」で、
#      タイタニック（約3,800m）と同じ縦の尺で比べる。c706 の安全率の目標 2.25 は札（棒は c708）。c713 の模型の深さは3冊で割れる＝描かない（札だけ）
_N_SAY = "人の形は模式（顔は描かない）"
SPEC.update({
    # c701（2行）＝聞き役の問い→横から見たタイタン（炭素繊維の筒・チタンのドーム）＋「強い・軽い・形を作りやすい」
    "c701": dict(
        t="強くて軽い材料", s="広く使われる材料",          # ⚠️ 門番 dup：「炭素繊維の…」は章の札の写し
        fig=("m22", dict(view="side", steps=[dict(state=dict(mat="on")), dict(tag=dict(t="強い・軽い・形を作りやすい", at="low"))],
                         note="形は NTSB 図3 の比（模式）", src=ss.src(["TSB §1.13"]))),
    ),
    # c702（3行）＝引っ張り（旅客機の胴体＝中から外へ）→押しつぶし（深い海の殻＝外から中へ）・確かな実績が無い→米沿岸警備隊の見方（青）
    "c702": dict(
        t="押される殻", s="空の上と海の底",          # ⚠️ 門番 dup：「力の向き」は図の左上の札の写し
        fig=("m22", dict(view="tc", steps=[dict(state=dict(air="on")), dict(state=dict(sea="on"), tag=dict(t="確かな実績が無い", at="r1")),
                                           dict(tag=dict(t="一般に弱いとされる", d="米沿岸警備隊の見方", at="r2", col=J.USCG))],
                         note="矢印は力の向きの模式", src=ss.src(["USCG p274"]))),
    ),
    # c703（2行）＝ふつうの深海の潜水艇（鋼かチタンの球）→タイタン（炭素繊維の筒）・ほかに例が無い（カナダ）
    "c703": dict(
        t="殻の形", s="球と筒",
        fig=("m22", dict(view="shell", steps=[dict(state=dict(left="on")),
                                              dict(state=dict(right="on"), tag=dict(t="ほかに例が無い", d="カナダの調べ", at="r2", col=J.INST))],
                         note="形と大きさは模式", src=ss.src(["TSB §1.13", "TSB §脚注53"]))),
    ),
    # c704（3行）＝同じ並べ図。聞き役の問い→軽い（運ぶ・降ろす仕組みが安い）・筒の形（中が広い）→会社の主な理由（カナダ）
    "c704": dict(
        t="選んだわけ", s="軽さと広さ",
        fig=("m22", dict(view="shell", start=dict(left="on", right="on"),
                         steps=[dict(), dict(tag=[dict(t="軽い＝運ぶ・降ろす仕組みが安い", at="r1"), dict(t="筒の形＝中が広い", at="r2")]),
                                dict(tag=dict(t="会社の主な理由", d="カナダの調べの見方", at="r3", col=J.INST))],
                         note="形と大きさは模式", src=ss.src(["TSB §1.13"]))),
    ),
    # c705（2行）＝🔧 人の言葉（元運航部長の話＝CEO の考え）の吹き出し「better in compression than tension」→米沿岸警備隊の見方と逆（青）
    "c705": dict(
        t="逆の向き", s="元部長が伝えた考え",          # ⚠️ 門番 dup：「報告書が引く言葉」は note の写し
        fig=("m22", dict(view="say", start=dict(set="comp"),
                         steps=[dict(state=dict(n="1")), dict(tag=dict(t="米沿岸警備隊の見方と逆", at="r", col=J.USCG))],
                         note=_N_SAY + "・英字は米運輸安全委員会の報告書が引く言葉", src=ss.src(["NTSB p1025", "USCG p274"]))),
    ),
    # c706（2行）＝🔧 深さの物差し（0〜7,000m）。外部の会社の設計書→会社の望み 6,000m（橙の線）・安全率の目標 2.25（札）
    "c706": dict(
        t="設計の目標", s="2015年6月の書類",
        fig=("m22", dict(view="ruler", start=dict(z="near"),
                         steps=[dict(tag=dict(t="外部の会社の設計書", at="doc", col=J.INK_W)),
                                dict(state=dict(goal="on"), tag=dict(t="安全率の目標 2.25", at="sf"))],
                         rel=[dict(t="2.25", src="TSB §1.12.1")],
                         note="深さは縮尺どおり（タイタニックは約3,800メートル）", src=ss.src(["TSB §1.12.1", "TSB §1.3"]))),
    ),
    # c707（3行）＝安全率のしくみ（潜ってよい深さと壊れる深さの棒・長さは模式）。聞き役の問い→何倍か→1より大きいほど余裕
    "c707": dict(
        t="安全率", s="余裕の大きさ",
        fig=("m22", dict(view="sf", steps=[dict(), dict(state=dict(bars="on", ratio="on"), tag=dict(t="何倍か", at="r1")),
                                           dict(state=dict(spare="on"), tag=dict(t="余裕", at="r2"))],
                         note="棒の長さは模式（値ではない）", src=ss.src(["NTSB p1024"]))),
    ),
    # c708（2行）＝棒（安全率）。設計書の2つの計算（2.19・2.21）と会社の目標（2.25）→規格の最低（1.5）
    "c708": dict(
        t="設計書の安全率", s="2015年の計算",
        fig=("qty", dict(view="bar", groups=[ss.QG["sf"]],
                         steps=[dict(add=[ss.qb("sf_ti"), ss.qb("sf_cf"), ss.qb("sf_goal")]), dict(add=[ss.qb("sf_min")])],
                         note="規格＝米国の機械学会の規格", src=ss.src(["TSB §1.12.1", "TSB §脚注45"]))),
    ),
    # c709（2行）＝🔧 深さの物差し（0〜14,000m）。壊れる深さの計算 約1万3,200m（橙）→タイタニックの深さの箱3つ＝3倍あまり
    "c709": dict(
        t="計算の上の深さ", s="深さを並べると",          # ⚠️ 門番 dup：「縮尺どおり」は図の左上の札と note の写し
        fig=("m22", dict(view="ruler", start=dict(z="far", goal="on"),
                         steps=[dict(state=dict(fail="on")), dict(state=dict(ratio="on"), tag=dict(t="3倍あまり", at="dl"))],
                         rel=[dict(t="3倍あまり", src="NTSB p1025（13,200メートル）・TSB §1.3（3800 m）")],
                         note="深さは縮尺どおり（点線の箱1つ＝タイタニックの深さ）", src=ss.src(["NTSB p1025", "TSB §1.3"]))),
    ),
    # c710（2行）＝米運輸安全委員会の一節（理論の模型・完全な形と繊維の向き）→実物で確かめるべきだった
    "c710": dict(
        t="理屈の上の値", s="実物で確かめる前",
        fig=("m22", dict(view="paper", start=dict(doc="model"), steps=[dict(state=dict(hl1="on", hl2="on")), dict(state=dict(hl3="on"))],
                         note="一節は米運輸安全委員会の報告書（英字のまま・模式）", src=ss.src(["NTSB p1063"]))),
    ),
    # c711（2行）＝3分の1の模型（炭素繊維の筒とドーム）に外から圧→ドームの1つが約3,000メートル相当の圧で壊れた
    "c711": dict(
        t="模型の試験", s="2015年12月",
        fig=("m22", dict(view="model", steps=[dict(state=dict(press="on"), tag=dict(t="外から圧をかける", at="r1")),
                                              dict(state=dict(fail="on"), tag=dict(t="ドームの1つが壊れた", d="約3,000メートル", at="r2", col=J.ALERT))],   # ⚠️ 門番 echo：「…相当の圧」まで書くと語りの写し＝数と単位だけ
                         rel=[dict(t="1つ", src="TSB §1.12.1"), dict(t="約3,000メートル", src="TSB §1.12.1")],
                         note="どちらのドームかは描き分けていない（模式）", src=ss.src(["TSB §1.12.1"]))),
    ),
    # c712（2行）＝🔧 人の言葉（CEO の手紙）。2行目で吹き出し（筒には傷が無い・筒の形はよく分かっている）
    "c712": dict(
        t="CEO の手紙", s="筒への自信",
        fig=("m22", dict(view="say", start=dict(set="letter"), steps=[dict(), dict(state=dict(n="1"))],
                         note=_N_SAY + "・英字は米沿岸警備隊の報告書が引く手紙", src=ss.src(["USCG p111"]))),
    ),
    # c713（2行）＝🔧 深さの物差し（0〜7,000m）。運航の目標 4,500m（橙の線）・模型の試験は届かず→模型の筒にも剥離（CEO の話）
    "c713": dict(
        t="届かない模型", s="目指した深さ",
        fig=("m22", dict(view="ruler", start=dict(z="near"),
                         steps=[dict(state=dict(op="on"), tag=dict(t="模型の試験は届かず", at="low2")),
                                dict(tag=dict(t="模型の筒にも剥離", d="CEO の話（米運輸安全委員会の報告書）", at="low", col=J.ALERT))],
                         note="模型の回ごとの深さは報告書で割れる＝描いていない（模式）", src=ss.src(["USCG p114", "NTSB p1025"]))),
    ),
    # c714（3行）＝船級のしくみ。聞き役の問い→船級協会（民間の団体）が設計・工事を確かめる→試験に立ち会い、証明書
    "c714": dict(
        t="船級", s="外から確かめる人",
        fig=("m22", dict(view="klass", steps=[dict(tag=dict(t="確かめるのは？", at="q")), dict(state=dict(soc="on", design="on")),
                                              dict(state=dict(test="on", cert="on"))],
                         note="流れは要点（模式）", src=ss.src(["NTSB p1022"]))),
    ),
    # c715（2行）＝年表（2016年 船級を取るつもり→2018年 あきらめる）
    "c715": dict(
        t="あきらめた船級", s="CEO の判断",
        fig=("axis", dict(ss.AX_CLASS, steps=[dict(add=[ss.ax("cls16")], cur="2016"), dict(add=[ss.ax("cls18")], cur="2018")],
                          note="年は米運輸安全委員会の報告書（元社員の話）", src=ss.src(["NTSB p1022", "NTSB p1023"]))),
    ),
    # c716（3行）＝会社のブログの題「Why Isn’t Titan Classed?」→一節（船級だけでは安全に足りない）→聞き役
    "c716": dict(
        t="ブログの題", s="会社の言い分",
        fig=("m22", dict(view="paper", start=dict(doc="blog"), steps=[dict(state=dict(hl1="on")), dict(state=dict(hl2="on")), dict()],
                         note="題と一節は会社のブログ（英字のまま・カナダと米運輸安全委員会の報告書が引く・模式）",
                         src=ss.src(["TSB §1.26.3.1", "NTSB p1024"]))),
    ),
    # c717（3行）＝米運輸安全委員会の注17（新しい技術を確かめる道→旅客の船に「実験的」の区分は無い）→米運輸安全委員会（緑）
    "c717": dict(
        t="新しい技術の道", s="旅客の船の決まり",
        fig=("m22", dict(view="paper", start=dict(doc="fn17"),
                         steps=[dict(state=dict(hl1="on")), dict(state=dict(hl2="on", hl3="on")),
                                dict(tag=dict(t="米運輸安全委員会の注", at="r3", col=J.OK))],
                         note="一節は米運輸安全委員会の報告書の脚注17（英字のまま・模式）", src=ss.src(["NTSB p1023"]))),
    ),
    # c718（3行）＝🔧 人の言葉（CEO・テレビの取材）。2行目で1つ目の吹き出し・3行目で2つ目
    "c718": dict(
        t="規則を破った", s="2021年の取材",
        fig=("m22", dict(view="say", start=dict(set="tv"), steps=[dict(), dict(state=dict(n="1")), dict(state=dict(n="2"))],
                         note=_N_SAY + "・英字は米沿岸警備隊の報告書が引くテレビの取材", src=ss.src(["USCG p301"]))),
    ),
    # c719（3行）＝社員の言葉（料金を払う客を「ミッション・スペシャリスト」と呼ぶ→呼び名を変えるだけでは済まない）→辞職
    "c719": dict(
        t="社内の声", s="呼び名への懸念",
        fig=("m22", dict(view="paper", start=dict(doc="emp"),
                         #   🔧 試し焼き：3行目（0.69秒）の札「話のあと辞職」は出てすぐ次のカット＝読めない＝外した（辞めたことは語り）
                         steps=[dict(state=dict(hl1="on")), dict(state=dict(hl2="on", hl3="on")), dict()],
                         note="言葉は米運輸安全委員会の報告書が引く社員の言葉（英字のまま・模式）", src=ss.src(["NTSB p1047"]))),
    ),
})
