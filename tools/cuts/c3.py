# -*- coding: utf-8 -*-
"""第2章　25年前から見えていた c301–c319（19カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c3.py`）。
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
    'c301': dict(kind='写真',
               plan='B7@⑤b-1（錆びた鉄筋の標本の別の秒＝42〜46 は c106 の頭）｜副題：証拠の鉄筋の標本（2024年）｜権利：A推定｜注：13.2秒＝走査で錆びた標本の長い区間・無ければ静止画で受ける。代わり＝B3@⑤b-1（倉庫の部材の錆びた鉄筋）',
               src='TR0441'),
    'c302': dict(kind='図解',
               plan='図 年表（1981 完成 → 建てて15年 プールデッキの大改修 → 1996〜97年 構造の補修と防水）｜権利：自作',
               src='TR0236'),
    'c303': dict(kind='図解',
               plan='図 模式図【横から】作り直したプールデッキの重ね（元のコンクリート・防水の膜・砂の層・敷石）｜権利：自作',
               src='TR0237〜0240'),
    'c304': dict(kind='図解',
               plan='図 模式図【上から】プールデッキとプランター（図面に無い大きなプランターを赤い点線＝TR0233 の図の形）｜権利：自作',
               src='TR0232〜0235'),
    'c305': dict(kind='図解',
               plan='図 模式図（同じ・プランターと敷石に重さの印）｜権利：自作',
               src='TR0280'),
    'c306': dict(kind='図解',
               plan='図 数の比べ（余裕の考え方：ふだんかかる重さ ＜ 耐えられる重さ・その差＝余裕・数は出さない）｜権利：自作',
               src='TR0018・TR0470'),
    'c307': dict(kind='図・写真の頁',
               plan='tf_p174_corr（TF スライド174＝鉄筋の腐食・写真つき）｜副題：NIST の技術的知見のスライド174｜権利：A｜注：英語の札は訳を重ねる',
               src='TR0242〜0247・TR0280'),
    'c308': dict(kind='フリー素材',
               plan='S#9（錆びた金属の面の寄り）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：鉄筋そのものではない＝「イメージ」',
               src='TR0442・TR0443・GJ p.18・MC18 p.1'),
    'c309': dict(kind='図解',
               plan='図 書類の再現図 2018年10月8日の調査の報告（9頁・表題「Structural Field Survey Report」・会社と人の名前は出さない）｜権利：自作',
               src='MC18 p.1・p.7・GJ p.17'),
    'c310': dict(kind='文字の頁',
               plan="図 p4007 2018年の報告 p.7（文字の頁・町の写しの切り出し＝④'で画像に当てる）",
               src='MC18 p.7'),
    'c311': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='MC18 p.7（`The failed waterproofing is causing major structural damage to the concrete structural slab below these areas.`）'),
    'c312': dict(kind='写真',
               plan='B5@11–16.3（倉庫の床一面の部材）｜副題：倉庫に並ぶ証拠の部材（2023年）｜権利：A推定｜注：—',
               src='MC18 p.7'),
    'c313': dict(kind='図解',
               plan='図 模式図【横から】平らな床の上の防水（傾きが無く、水が乾くまで残る）｜権利：自作',
               src='MC18 p.7'),
    'c314': dict(kind='図解',
               plan='図 模式図【横から】報告の直し方（敷石から防水まではがす → 床を直す → 傾きのあるコンクリートを足す → 防水を敷き直す）｜権利：自作',
               src='MC18 p.7'),
    'c315': dict(kind='フリー素材',
               plan='S#20（柱の並ぶ屋内駐車場）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：柱の番号・床の表示の字を⑤b-1で',
               src='MC18 p.7'),
    'c316': dict(kind='図解',
               plan='図 数の比べ（2018年の見積もり 合計 約913万ドル＝内わけは出さない）｜権利：自作',
               src='EST18'),
    'c317': dict(kind='写真',
               plan='N#33（プールデッキの床版からコアを抜く）｜副題：プールデッキの床版のコア抜き（2023年9月）｜権利：A｜注：—',
               src='MC18 p.7・legend L02'),
    'c318': dict(kind='図解',
               plan='図 時間の帯（1996〜97年 → 2018年10月 報告 → 2018年11月 → 2021年6月）｜権利：自作',
               src='TR0441・MC18 p.7'),
    'c319': dict(kind='写真',
               plan='B2@⑤b-1（14〜46・49.5〜95.8 の空撮から＝99〜113 は c406・c419）｜副題：現場の空撮（崩落の後・2021年）｜権利：A推定｜注：114秒〜の表題カード・氏名テロップを避ける',
               src='—（橋）'),
}

TR_SRC = "NIST の技術的知見の動画（2026年6月）"
PL_NOTE = "プランターの数と大きさは模式（並びは NIST の空から見た写真の赤い点線）"

SPEC = {
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）──
    # c303（9.40秒＝0〜4.30／4.79〜9.40）＝改修の重ね（TR0237〜0240・TF p9090 のコアの模式）。厚さは図の値の比（門番が照らす）
    "c303": dict(
        t="作り直したプールデッキ", s="膜・砂・敷石を足した",
        fig=("m19", dict(view="core",
                         steps=[dict(state=dict(new="on"), delay=0.3,
                                     tag=[dict(t="敷石と砂（足した）", at="new", to="paver"),
                                          dict(t="防水の膜（足した）", at="memb", to="memb"),
                                          dict(t="元のタイル", d="多くははがした（コアには残る）", at="tile", to="tile")]),
                                dict(state=dict(load="on"), delay=0.3, tag=dict(t="重さを足した", at="load"))],
                         note="重ねの厚さは NIST の図の値の比（下の床の板の厚さは模式）", src=TR_SRC + "のスライド（コアの模式）")),
    ),
    # c304（7.71秒＝0〜3.59／4.08〜7.71）＝図面に無いプランター（TR0233〜0235・TF p9088）
    "c304": dict(
        t="植木の箱", s="図面との違い",
        fig=("m19", dict(view="planter",
                         steps=[dict(state=dict(box="on"), delay=0.3, tag=dict(t="図面に無い箱", at="box", to="planters")),
                                dict(state=dict(palm="gone"), delay=1.6, tag=dict(t="ヤシの木は2017年のあとに抜いた", at="palm", to="palm"))],
                         rel=[dict(t="2017年", src="TR p1235（removed following a hurricane in 2017）")],
                         note=PL_NOTE, src=TR_SRC + "の語りとスライド")),
    ),
    # c305（8.85秒＝0〜1.99／2.48〜6.24／6.73〜8.85）＝余裕を削ったもの（TR0280）
    "c305": dict(
        t="足された重さ", s="プランターと改修の床",
        fig=("m19", dict(view="planter", start=dict(box="on", palm="gone"),
                         steps=[dict(tag=dict(t="図面に無い物", at="q")),
                                dict(state=dict(weight="both"), delay=0.3,
                                     tag=[dict(t="図面より重いプランター", at="wp", to="planters"),
                                          dict(t="改修の砂と敷石", at="wd", to="deck")]),
                                dict(tag=dict(t="「余裕」を削った", at="margin"))],
                         note=PL_NOTE + "・重りの印は模式", src=TR_SRC + "の語り")),
    ),
    # c313（10.59秒＝0〜1.65／2.14〜6.14／6.63〜10.59）＝平らな床の上の防水（MC18 p.7）
    "c313": dict(
        t="防水の問題", s="水がたまる床",
        fig=("m19", dict(view="water",
                         steps=[dict(tag=dict(t="敷石の下に防水の膜", at="q", to="pond")),
                                dict(state=dict(pond="on", level="on"), delay=0.3, tag=dict(t="床が平ら：水が流れない", at="flat", to="pond")),
                                dict(tag=dict(t="図面の誤り（報告）", at="err"))],
                         note="床と重ねの厚さ・水の量は模式", src="モラビトの調査の報告（2018年10月） p.7")),
    ),
    # c314（11.70秒＝0〜4.93／5.42〜8.62／9.11〜11.70）＝報告の直し方（MC18 p.7）
    "c314": dict(
        t="報告の直し方", s="全部はがして作り直す",
        fig=("m19", dict(view="water", start=dict(pond="on"),       # ⑤b-4 の下見：水平器の印は傾けた床の矢印に近い＝c313 だけ
                         steps=[dict(state=dict(strip="on", fix="on"), delay=0.4, tag=dict(t="全部はがして、床を直す", at="strip")),
                                dict(state=dict(slope="on", memb2="on"), delay=0.3,
                                     tag=dict(t="傾斜＋新しい防水", at="slope", to="memb2")),
                                dict(tag=dict(t="高くつき、暮らしも乱す", at="cost"))],
                         note="床と重ねの厚さ・傾きは模式", src="モラビトの調査の報告（2018年10月） p.7")),
    ),
    # ── 🆕 ⑤b-5（2026-10-06）：年表（`tools/axis.py`・門番 check_axis）──
    # c302（7.03秒＝0〜3.63／4.12〜7.03）＝1行目「建てて15年たつころ」で 1981→1996 の括弧／2行目「プールデッキを大きく作り直す」で
    #   1996〜97年の帯（TR0236「15 years after」・TR0441「in 1996 and '97」）
    "c302": dict(
        t="建てて15年", s="ひび・水漏れ・錆",
        fig=("axis", dict(ss.AX_LIFE, past=[ss.ax("build"), ss.ax("done")], start=dict(cur="1981"), steps=[
            dict(add=ss.ax("y15"), cur="1996"),
            dict(add=ss.ax("rehab"), cur="1997")],
            note="年だけの記録はその年の真ん中に置いた", src=ss.src(["TR p1005・p1236・p1441", "AC p2023"]))),
    ),
    # c318（7.02秒＝聞き役 0〜1.94／2.43〜7.02）＝2行目「25年以上前から見えていた錆が、2018年には報告書に」で 1996→崩落の括弧（TR0441
    #   「more than 25 years before the collapse」）と報告の点。⚠️ 予定の一覧の「2018年11月」は報告と1か月差＝この軸では同じ点に重なる＝出さない
    "c318": dict(
        t="錆の年月", s="補修から報告書まで",      # ⚠️ echo：「25年以上前から」は字幕の切り取り
        fig=("axis", dict(ss.AX_RUST, past=[ss.ax("rehab", t="補修と防水")], start=dict(cur="1997"), steps=[
            dict(),
            dict(add=[ss.ax("y25"), ss.ax("fall"), ss.ax("survey", fmt="ym", t="報告")], cur="2018-10-08")],
            note="", src=ss.src(["TR p1441", "MC18 p4001", "A12 p5101"]))),
    ),
    # ── 🆕 ⑤b-6（2026-10-06）：余裕の考え方（模式図 m19 の margin）・書類の再現図（箱の型）──
    # c306（8.97秒＝0〜3.03／3.52〜6.55／7.05〜8.97 聞き役）＝余裕（TR0018・TR0470）。数の比べ → 模式図（数を出さない＝棒の型は値が要る）。
    #   1行目で2本の棒・2行目で余裕の枠
    "c306": dict(
        t="余裕とは", s="2つの重さの差",
        fig=("m19", dict(view="margin",
                         steps=[dict(state=dict(cap="on", load="on"), delay=0.3,
                                     tag=[dict(t="耐えられる重さ", at="cap"), dict(t="ふだんかかる重さ", at="load")]),
                                dict(state=dict(gap="on"), delay=0.3, tag=dict(t="この差が余裕", at="gap", to="gap")),
                                dict()],
                         note="長さは模式（数は出さない）", src=TR_SRC + "の語り")),
    ),
    # c309（9.94秒＝0〜5.34／5.83〜9.94）＝調査の報告 p.1（日付・あて先・表題）と p.7（書いたこと＝2行目）。会社と人の名前は出さない
    "c309": dict(
        t="2018年の調査", s="報告書の表紙と中身",
        fig=("boxes", dict(view="form", form=ss.FORM_MC18, steps=[
            dict(add=dict(k="paper")),
            dict(add=dict(k="fill", f="書いたこと"))],
            note="欄の字は原文のまま・様式は再現・会社と人の名前は出さない", src=ss.src(["MC18 p4001・p4007"]))),
    ),
    # c316（4.61秒＝1行）＝見積もりの合計（EST18）。数の比べ → 書類の再現図（棒が1本しか無い＝18本目 c603 と同じ）・内わけは出さない（映像方針）
    "c316": dict(
        t="報告と一緒に出た額", s="合計だけを見る",      # ⚠️ dup：「2018年10月」は出典の行の写し
        fig=("boxes", dict(view="form", form=ss.FORM_EST18, steps=[
            dict(add=[dict(k="paper"), dict(k="fill", f="合計")])],
            note="欄の字は原文のまま・様式は再現", src=ss.src(["EST18 p4318"]))),
    ),
    # ── 🆕 ⑤b-7a（2026-10-06）：写真・映像（list19 の区間と副題＝写っているもの・見出しは語りの写しにしない）──
    "c301": ss.vid("c301", t="古くからの錆", s="証拠の鉄筋の標本（2024年）"),
    "c312": ss.vid("c312", t="防水と傷みの広がり", s="倉庫に並ぶ証拠の部材（2023年）"),
    # c317＝束で上を切った（ドリルの商標・バケツの字＝⑤b-1 の原寸）
    "c317": dict(t="作り直しの勧め", s="プールデッキの床版のコア抜き（2023年9月）",
                 photo=P("n33_coring"), **ss.kind(P("n33_coring"))),
    # c319＝束で右下を切った（ベストとヘルメットの商標）・調査員は公務
    "c319": dict(t="報告のゆくえ", s="がれきのコンクリート片を調べる調査員（2021年7月1日）",
                 photo=P("n12_concrete"), **ss.kind(P("n12_concrete"))),
    # ── 🆕 ⑤b-7b（2026-10-06）：スライドと資料の頁（色は変えない）──
    # フリー素材（イメージ）：c308＝錆びた金属の面の寄り・c315＝柱の並ぶ屋内駐車場
    "c308": ss.vid("c308"),
    "c315": ss.vid("c315"),
    "c307": dict(t="錆びた鉄筋の標本", s="錆の進んだ鉄筋の標本の写真",
                 photo=P("tf_p174_corr"), panel=True, color=1.0),
    # c310＝2018年の調査の報告 p.7 の1段落目の頭4行（防水が寿命を過ぎ、下の床版に大きな傷み）。🔴 a. の設計者の会社名・
    #   次の決め所 c311 の英文（expand exponentially）は切り口の外（`qa_out/ep19_assets.py` の PAGE_CUTS）
    "c310": dict(t="防水と床版の傷み", s="寿命を過ぎた防水と下の床版の段落",
                 photo=ss.page(4007), trim=ss.ptrim("c310"), bias=ss.pbias("c310"), panel=True, color=1.0),
    # ── 🆕 ⑤b-8（2026-10-07）：決め所 ──
    # c311＝モラビトの報告 Page 7「The failed waterproofing is causing major structural damage to the concrete structural slab below
    #   these areas.」（these areas＝the Pool Deck & Entrance Drive＝前の文）
    "c311": dict(
        t="2018年の調査", s="報告が書いた床の傷み",
        fig=("quote", dict(phrase="報告「防水の不良で床に重大な構造の損傷」",
                           rows=ss.qrows("MC18", "7頁", ("場所", "プールデッキと車道の下")), paper=True)),
    ),
}
