# -*- coding: utf-8 -*-
"""第8章　見えなかったもの c901–c923（23カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c9.py`）。
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
    'c901': dict(kind='写真',
               plan='B3@40–46（倉庫で部材の鉄筋を測る）｜副題：倉庫で証拠を測る（2022年）｜権利：A推定｜注：調査員の顔＝公務',
               src='TR0213'),
    'c902': dict(kind='図解',
               plan='図 模式図 2つの物差し（建てた当時の決まり／今の決まり）｜権利：自作',
               src='TR0213・TR0214'),
    'c903': dict(kind='図解',
               plan='図 模式図【上から】強さが足りない所（黄＝中くらい・赤＝ひどい＝TR0215〜0216 の図の型）｜権利：自作',
               src='TR0215・TR0216'),
    'c904': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0219（`In some locations, the design provided less than half of the code-required strength.`）'),
    'c905': dict(kind='図解',
               plan='図 模式図 2つの物差し（同じ・当時の決まりの物差しにも欠けた所＝決まりの限界）｜権利：自作',
               src="TR0279（`design understrength caused by severe and widespread deviations in the building's original structural design from the codes and standards of the day, but also some limitations in those codes and standards`）"),
    'c906': dict(kind='図・写真の頁',
               plan='tf_p075_cover（TF スライド75＝かぶり・床の断面の写真）｜副題：NIST の技術的知見のスライド75｜権利：A｜注：🔁 台本は実写（NIST の写真）→ 同じ中身のスライドに',
               src='TR0220'),
    'c907': dict(kind='図解',
               plan='図 模式図【横から】鉄筋の上のコンクリートの厚さ（図面＝約1.9センチ〈4分の3インチ〉／実際＝約5センチ〈2インチ〉・上の鉄筋が下がる）｜権利：自作',
               src='TR0221（`the cover was generally about 2 inches rather than 3/4 of an inch shown on the drawings`）'),
    'c908': dict(kind='図解',
               plan='図 模式図（同じ・ずれの分だけ強さが下がる矢印）｜権利：自作',
               src='TR0222（`This deviation, while seemingly minor, significantly diminishes the strength`）'),
    'c909': dict(kind='図・写真の頁',
               plan='tf_p076_bars（印字は77）｜副題：NIST のスライド77（図面＝サーフサイド町）｜権利：A＋町の図面｜注：紙面の引用（頁ごと・額装・無加工・色を変えない・出典に「図面：Town of Surfside」）',
               src='TR0223・TR0226・TR0227・TF p77'),
    'c910': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0228（`only two bars in each direction passed over the columns, half the number required`）・TF p77（`only 2 rather than 4 top bars were centered over the column in each direction`）'),
    'c911': dict(kind='図解',
               plan='図 模式図【上から】鉄筋の間隔（図面の間隔 → 実際は約20から40%広い・柱のまわりの本数が減る）｜権利：自作',
               src='TR0224・TR0229（`about 20% to 40% wider than required by the structural design drawings`）・TR0230'),
    'c912': dict(kind='写真',
               plan='B5@102–109（倉庫の部材のあいだを歩く）｜副題：倉庫に並ぶ証拠（2023年）｜権利：A推定｜注：NIST のヘルメットに寄らない',
               src='TR0231（`Records of whether these changes were approved by the design engineer or observed by inspectors in the field are not available.`）'),
    'c913': dict(kind='図解',
               plan='図 数の比べ（原因の5つ：設計の強さの不足〈いちばん大きい・広い〉・図面とのずれ〈広い〉・重いプランター・足した砂と敷石・年月の傷み＝AC p.54 の形）｜権利：自作',
               src='AC p.54（`Design understrength (largest, pervasive)`）・TR0277〜0280'),
    'c914': dict(kind='図解',
               plan='図 数の比べ（同じ・5つを順に光らせる）｜権利：自作',
               src='AC p.54・TR0280'),
    'c915': dict(kind='写真',
               plan='N#42（吸水の試験）｜副題：コンクリートの吸水の試験（2024年8月）｜権利：A｜注：—',
               src='TR0280（`the most significant factor for which was likely corrosion of the reinforcement, exacerbated by porous concrete, concrete cracks that leaked, and ineffective waterproofing`）'),
    'c916': dict(kind='写真',
               plan='N#3（携帯の分析器で塩化物を測る）｜副題：塩化物を測る（2022年1月）｜権利：A｜注：縦横ほぼ同じ＝額装',
               src='TR0042（`The final factor that brought the critically low margins of safety to the point of failure was most likely long-term degradation from corrosion.`）・TR0280・MC18 p.7'),
    'c917': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='AC p.61（`Degradation was a comparatively small contributor to the strength and deformation capacity deficiencies responsible for the CTS failure.`）'),
    'c918': dict(kind='図解',
               plan='図 年表（1979〜81年 設計と建設＝赤い印「住む前から」 → 1981年 完成 → 2021年 崩落）｜権利：自作',
               src='TR0281（`caused the bulk of the critically low margins against failure from the time construction was complete`）'),
    'c919': dict(kind='図解',
               plan='図 年表（同じ）｜権利：自作',
               src='TR0278（`baked in before the building was even occupied`）'),
    'c920': dict(kind='写真',
               plan='B6@47–51.75（圧縮試験機の中のコア）｜副題：コンクリートのコアの試験（2024年）｜権利：A推定｜注：51.75 から顔の寄り＝until',
               src='TR0441・TR0281'),
    'c921': dict(kind='図解',
               plan='図 流れ図（40年の再認証＝傷みを見る → 建てたときの設計と工事は確かめない＝AC p.61 の1c）｜権利：自作',
               src='AC p.61（`The requirements for recertification of structures in Florida are laudable, but they contain no requirements for establishing confidence in the original design and construction.`）'),
    'c922': dict(kind='写真',
               plan='B5@39–46.5（コア抜きの刃と水）｜副題：コア抜き（2023年）｜権利：A推定｜注：絵が柔らかい（実効 約512px）＝別の秒も⑤b-1で',
               src='TR0472（`Problems in its pool deck structure stemming from the time of original design and construction`）'),
    'c923': dict(kind='写真',
               plan='C13（跡地と抜けた鉄筋）｜副題：崩落の跡地（2021年10月4日）｜権利：CC BY 2.0（Steve Jurvetson）｜注：色や切り出しを変えたら「改変」の表示',
               src='—（橋）'),
}

TR_SRC = "NIST の技術的知見の動画（2026年6月）"
RU_NOTE = "物差しの長さと足りない量は模式（2つの物差しの厳しさは比べていない）"
CV_NOTE = "厚さは記録の値の比で描いた（床の厚さと鉄筋の太さは模式）"

SPEC = {
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）──
    # c902（11.50秒＝0〜3.14／3.63〜6.66／7.15〜11.50）＝2つの物差し（TR0213・0214）
    "c902": dict(
        t="設計の確かめ", s="基準は2つ",
        fig=("m19", dict(view="ruler",
                         steps=[dict(state=dict(rul="on"), delay=0.3,
                                     tag=[dict(t="建てた当時の決まり", at="old", to="old"), dict(t="今の決まり", at="new", to="new")]),
                                dict(tag=dict(t="デッキと駐車場の一部", at="have")),
                                dict(state=dict(short="on"), delay=0.3, tag=dict(t="どちらにも足りない", at="short"))],
                         note=RU_NOTE, src=TR_SRC + "の語り")),
    ),
    # c903（7.43秒＝0〜3.59／4.08〜7.43）＝強さが足りない所（TR0215・0216・TF p9082＝建てた当時の決まりで見た図）
    "c903": dict(
        t="強さが足りない所", s="建てた当時の決まりで見ると",
        fig=("m19", dict(view="code",
                         steps=[dict(state=dict(dots="on", flex="on"), delay=0.3,
                                     tag=[dict(t="赤＝ひどい不足", at="red", to="red"), dict(t="黄＝中くらいの不足", at="yel", to="yel")]),
                                dict(tag=dict(t="設計の時点で弱かった", at="orig"))],
                         note="印の位置は NIST の図の形（継ぎ目は列と行の交点に寄せた模式）", src=TR_SRC + "のスライド（設計の確かめ）")),
    ),
    # c905（7.69秒＝0〜4.22／4.71〜7.69）＝決まりからの外れ・決まりの限界（TR0279）
    "c905": dict(
        t="弱さの理由", s="設計と基準",
        fig=("m19", dict(view="ruler", start=dict(rul="on", short="on"),
                         steps=[dict(state=dict(gap="on"), delay=0.3, tag=dict(t="設計の大きな外れ", at="gap", to="gap")),
                                dict(state=dict(limit="on"), delay=0.3, tag=dict(t="決まりの限界", at="limit", to="limit"))],
                         note=RU_NOTE, src=TR_SRC + "の語り")),
    ),
    # c907（8.49秒＝0〜4.34／4.83〜8.49）＝鉄筋の上のコンクリートの厚さ（TR0221＝図面 3/4 インチ・実際 約2インチ）
    "c907": dict(
        t="鉄筋の上の厚さ", s="図面と現場で違った",
        fig=("m19", dict(view="cover",
                         steps=[dict(state=dict(dwg="on"), delay=0.3, tag=dict(t="図面：約1.9センチ", d="（4分の3インチ）", at="dwg", to="dwg")),
                                dict(state=dict(real="on"), delay=0.3, tag=dict(t="実際：約5センチ", d="（2インチ）", at="real", to="real"))],
                         rel=[dict(t="1.9センチ", src="TR p1221（3/4 of an inch shown on the drawings）"),
                              dict(t="4分の3", src="TR p1221（3/4 of an inch）"),
                              dict(t="約5センチ（2インチ）", src="TR p1221（generally about 2 inches）")],
                         note=CV_NOTE, src=TR_SRC + "の語り")),
    ),
    # c908（6.09秒＝0〜1.19／1.68〜6.09）＝ずれが強さを下げる（TR0222）
    "c908": dict(
        t="小さなずれ", s="床と継ぎ目への影響",
        fig=("m19", dict(view="cover", start=dict(dwg="on", real="on"),
                         steps=[dict(tag=dict(t="数センチの違い", at="diff")),
                                dict(state=dict(weak="on"), delay=0.3, tag=dict(t="床と継ぎ目の強さが下がる", at="weak", to="weak"))],
                         note=CV_NOTE + "・黄色の幅＝鉄筋から床の下の面まで", src=TR_SRC + "の語り")),
    ),
    # c911（13.70秒＝0〜5.20／5.69〜10.37／10.86〜13.70）＝柱の真上の本数（TF p9085＝4本でなく2本）・間隔 20〜40%（TR0229）・強さ（TR0230）
    "c911": dict(
        t="柱の真上の鉄筋", s="本数も間隔も図面と違った",
        fig=("m19", dict(view="rebar",
                         steps=[dict(state=dict(real="on", over="on"), delay=0.3,
                                     tag=[dict(t="図面：真上に4本", at="dwg", to="dwg"), dict(t="実際の例：真上に2本", at="real", to="real")]),
                                dict(state=dict(space="on"), delay=0.3, tag=dict(t="間隔：約20〜40%広い", at="space")),
                                dict(state=dict(weak="on"), delay=0.3, tag=dict(t="強さ↓（床・継ぎ目）", at="weak", to="weak"))],
                         rel=[dict(t="4本・2本", src="TF p9085（only 2 rather than 4 top bars）"),
                              dict(t="20から40%", src="TR p1229（about 20% to 40% wider）")],
                         note="鉄筋の本数（片側の向き）と間隔の比は記録の値・柱の大きさは模式", src=TR_SRC + "の語りとスライド")),
    ),
    # ── 🆕 ⑤b-5（2026-10-06）：年表（`tools/axis.py`・門番 check_axis）──
    # c918（8.77秒＝0〜2.01／2.50〜6.18／6.67〜8.77）＝1行目「錆が、いちばんの原因だと思っていた」で崩落の点／2行目「設計の不足と、図面との
    #   ずれ」で設計と建設の帯を赤に（TR0281「design understrength and deviations in the as-built construction」）／3行目「完成したときから」で完成
    "c918": dict(
        t="弱さの始まり", s="設計と建設のとき",      # ⚠️ echo：「余裕が足りなかった理由」は字幕の切り取り
        fig=("axis", dict(ss.AX_LIFE, steps=[
            dict(add=ss.ax("fall"), cur="2021-06-24"),
            dict(add=ss.ax("build", t="設計の不足・図面とのずれ", c="ALERT", rec=["AC p2023", "TR p1281"]), cur="1979"),
            dict(add=ss.ax("done", rec=["TR p1005", "TR p1281"]), cur="1981")],
            note="年だけの記録はその年の真ん中に置いた", src=ss.src(["TR p1005・p1281", "AC p2023", "A12 p5101"]))),
    ),
    # c919（3.63秒＝1行）＝「人が住む前から組み込まれていた」（TR0278「baked in before the building was even occupied」）の札を完成の下に
    "c919": dict(
        t="弱さの始まり", s="NIST の言い方",
        fig=("axis", dict(ss.AX_LIFE, past=[ss.ax("fall", keep=True),
                                             ss.ax("build", t="設計の不足・図面とのずれ", c="ALERT", rec=["AC p2023", "TR p1281"], keep=True),
                                             ss.ax("done", rec=["TR p1005", "TR p1281"], keep=True)], start=dict(cur="1981"), steps=[
            # ⚠️ 下見：1段目（軸の下 +118）は赤い帯の札「設計の不足・図面とのずれ」と同じ高さで重なった＝2段目へ（i0=1）
            dict(add=dict(k="chips", at="1981", chips=["人が住む前から"], rec="TR p1278", i0=1))],
            note="年だけの記録はその年の真ん中に置いた", src=ss.src(["TR p1005・p1278・p1281", "AC p2023", "A12 p5101"]))),
    ),
    # ── 🆕 ⑤b-6（2026-10-06）：流れ図（箱の型）──
    # c913（7.92秒＝0〜2.97 聞き役／3.46〜7.92）＝AC p.54 の形（原因と後押しの5つ → プールデッキの継ぎ目の壊れ）。2行目で5つを並べる。
    #   数の比べ → 流れ図（大きさの数は記録に無い＝AC p.54 は「largest・pervasive」の言葉だけ）
    "c913": dict(
        t="5つの原因と後押し", s="NIST のまとめ",
        fig=("boxes", dict(view="flow", layout=ss.FL_AC54, steps=[
            dict(),
            dict(add=[ss.fl("a_des"), ss.fl("a_dev"), ss.fl("a_pl"), ss.fl("a_fill"), ss.fl("a_deg"),
                      ss.ce(["a_des", "a_dev", "a_pl", "a_fill", "a_deg"], "h_ac")])],
            src=ss.src(["AC p2054", "TR p1277・p1279・p1280"]))),
    ),
    # c914（10.61秒＝0〜3.36／3.85〜6.84／7.33〜10.60）＝同じ形を語りの順に（1行目＝設計・図面・プランター／2行目＝砂と敷石・年月の傷み／
    #   3行目＝いちばん大きいのは設計の強さの不足＝AC p.54「largest, pervasive」の札）。前のカットの箱に重ねて灯さない（字が二重になる）
    "c914": dict(
        t="5つの中身", s="いちばん大きいもの",
        fig=("boxes", dict(view="flow", layout=ss.FL_AC54, steps=[
            dict(add=[ss.fl("a_des"), ss.fl("a_dev"), ss.fl("a_pl")]),
            dict(add=[ss.fl("a_fill"), ss.fl("a_deg"), ss.ce(["a_des", "a_dev", "a_pl", "a_fill", "a_deg"], "h_ac")]),
            dict(add=dict(k="chip", at="a_des", t="最も大きく、広い範囲", rec="AC p2054", dy=32))],
            src=ss.src(["AC p2054", "TR p1279・p1280"]))),
    ),
    # c921（11.69秒＝0〜3.32／3.81〜7.71／8.20〜11.70）＝AC p.61 の 1c。1行目で40年の点検とほめる札・2行目で建てたときの設計と工事（点線＋
    #   「確かめる決まりが無い」の札）・3行目で傷みを見る（矢印）
    "c921": dict(
        t="点検の決まりの外", s="建てたときは見ない",      # ⚠️ dup：「NIST の指摘」は札と出典の行の写し
        fig=("boxes", dict(view="flow", layout=ss.FL_EMPTY, steps=[
            dict(add=[ss.fl("r_cert"), dict(k="chip", at="r_cert", t="ほめるべき仕組み（NIST）", rec="AC p2061", dy=60)]),
            dict(add=[ss.fl("r_orig"), ss.ce("r_cert", "r_orig", style="leader"),
                      dict(k="chip", at="r_orig", t="確かめる決まりが無い", rec="AC p2061", dy=60)]),
            dict(add=[ss.fl("r_dmg"), ss.ce("r_cert", "r_dmg", lab="見る")])],
            src=ss.src(["AC p2061", "MC18 p4001"]))),
    ),
    # ── 🆕 ⑤b-7a（2026-10-06）：写真・映像（倉庫と試験の調査員は公務）──
    "c901": ss.vid("c901", t="設計の確かめ直し", s="倉庫で証拠を測る（2022年）"),
    # c912 🟡 ⑤c で原寸：バケツの店名の字（背景）
    "c912": ss.vid("c912", t="分からない承認", s="倉庫に並ぶ証拠（2023年）"),     # echo：「残っていない記録」＝字幕と 86%
    "c915": dict(t="錆を進めたもの", s="コンクリートの吸水の試験（2024年8月）",
                 photo=P("n42_absorption"), **ss.kind(P("n42_absorption"))),
    "c916": dict(t="塩化物と錆", s="塩化物を測る（2022年1月）",
                 photo=P("n03_chloride"), **ss.kind(P("n03_chloride"))),
    "c920": ss.vid("c920", t="見えない弱さ", s="コンクリートのコアの試験（2024年）"),
    "c922": ss.vid("c922", t="2つの原因", s="コア抜き（2023年）"),
    # c923＝CC BY 2.0（章の色のデュオトーン＝色の改変＝出典の行に「改変」・credits.json）
    "c923": dict(t="崩れの広がり", s="崩落の跡地（2021年10月4日）",
                 photo=P("c13_jurvetson"), **ss.kind(P("c13_jurvetson"))),
    # ── 🆕 ⑤b-7b（2026-10-06）：NIST のスライド（色は変えない）。🔴 c909 は町の図面を含む＝紙面の引用＝額装・無加工 ──
    "c906": dict(t="上の鉄筋の位置", s="図面の深さと実際の深さの床版の写真",
                 photo=P("tf_p075_cover"), panel=True, color=1.0),
    "c909": dict(t="図面の指定と実際", s="町の図面と NIST の写真",
                 photo=P("tf_p076_bars"), panel=True, color=1.0),
    # ── 🆕 ⑤b-8（2026-10-07）：決め所 ──
    # c904＝TR0219「In some locations, the design provided less than half of the code-required strength.」（所があった＝In some locations）
    "c904": dict(
        t="設計の強さ", s="決まりの求める強さと比べて",
        fig=("quote", dict(phrase="決まりの求める強さの半分も無い所があった",
                           rows=ss.qrows("TR", None, ("箇所", "発表の語り")), paper=True)),
    ),
    # c910＝TR0228「only two bars in each direction passed over the columns, half the number required」（NIST が示した例の柱）
    "c910": dict(
        t="柱の真上の鉄筋", s="NIST が示した例の柱",
        fig=("quote", dict(phrase="ある柱の真上の鉄筋は、4本でなく2本",
                           rows=ss.qrows("TR", None, ("箇所", "発表の語り")), paper=True)),
    ),
    # c917＝諮問委員会の資料 p.61「Degradation was a comparatively small contributor to the strength and deformation capacity
    #   deficiencies responsible for the CTS failure.」（原因の全部ではない＝最後のひと押しは c916）
    "c917": dict(
        t="傷みの分", s="傷みはどれだけ効いたか",      # echo：「強さの不足の内訳」は語りと同文
        fig=("quote", dict(phrase="強さの不足のうち、傷みの分は比較的小さい",
                           rows=ss.qrows("AC", "61頁"), paper=True)),
    ),
}
