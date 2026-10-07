# -*- coding: utf-8 -*-
"""第10章　疑われたもの cb01–cb16（16カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/cb.py`）。
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
    'cb01': dict(kind='写真',
               plan='B2@12–14（ss_b2_87park の秒）｜副題：南どなりの 87パーク と現場（2021年）｜権利：A推定｜注：札「言われていた話」・重機の CAT はもとから在る字。2秒の区間＝9.0秒は伸ばしすぎ＝13秒のコマ（ss_b2_87park）を静止画で受けるか、走査で 87パーク の写る別の秒',
               src='TR0454（`87 Park is an 18-story luxury condominium built just south of CTS and completed in 2019.`）'),
    'cb02': dict(kind='混ざり',       # ⑤b-7c の qa_all（textscreens E）：1行目が映像の差し込み（頭・フリー素材）＋図＝混ざり（c105 と同じ数え方）
               plan='模式図（台本のまま）｜差し込み（head）：1 S#38  5.1秒 S#38（基礎の工事の現場と重機）｜副題：イメージ｜札：イメージ（差し込み）｜権利：Pixabay Content License｜注：杭打ち機の素材は0本＝基礎の工事の重機',
               src='TR0455（`The northern boundary of the soil excavation for the construction of 87 Park was close to the southern boundary of CTS.`）・TR0456（`approximately 9 feet away from the south basement wall of CTS`）'),
    'cb03': dict(kind='図解',
               plan='図 模式図（同じ・揺れの波）｜権利：自作',
               src='TR0457'),
    'cb04': dict(kind='写真',
               plan='N#43（建物の計算機モデルを見る調査団）｜副題：計算機モデルを見る調査団（2023年4月）｜権利：A｜注：—',
               src='TR0460'),
    'cb05': dict(kind='図解',
               plan='図 模式図（揺れの矢印が、地下の壁と鋼の壁で小さくなり、継ぎ目へ届く前にさらに小さく）｜権利：自作',
               src='TR0461'),
    'cb06': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0462（`Vibrations at the critical slab-column connections were too small to have caused structural damage.`）'),
    'cb07': dict(kind='図・写真の頁',
               plan='図 p185 TF のスライド185（札の文＝印字185）',
               src='TF p185（`too small to damage even the distressed connections`）'),
    'cb08': dict(kind='フリー素材',     # ⑤b-7b：⑤b-1 で S#48（フリー素材）に替えた＝list19 の種類「フリー」と合わせた
               plan='B1@⑤b-1（現場の近くの建物の列）｜副題：現場の近くの建物（2021年6〜7月）｜権利：A推定｜注：—',
               src='TR0463・TR0464'),
    'cb09': dict(kind='図解',
               plan='図 一覧（アイコン：基礎・陥没と沈み・ハリケーンと高潮・車の衝突・爆発・クレーンの落下物・屋上の工事＝TF p189 の形）｜権利：自作',
               src='TR0465・TF p189'),
    'cb10': dict(kind='図解',
               plan='図 一覧（同じ・後半を光らせる）｜権利：自作',
               src='TR0465（`accidental loads or overloads caused by the roof repair and roof anchor project ongoing at the time of the collapse`）'),
    'cb11': dict(kind='図解',
               plan='図 模式図【上から】人工衛星で地面の沈みを見る（5年分・沈みの色は無し）｜権利：自作',
               src='A06（`None was seen in the area in the five years before the partial collapse, nor was localized sinking observed near the building in the days leading up to the tragedy.`）'),
    'cb12': dict(kind='図解',
               plan='図 模式図【横から】石灰岩の地面と空洞（水に溶けてできる空洞の説明＝この建物の下には無い）｜権利：自作',
               src='A06（`no evidence of karst in the limestone on which the foundation sits`・`features that actually inhibit the formation of karst`）'),
    'cb13': dict(kind='図解',
               plan="模式図【横から】くいと地下の床（札「くい：強さは足りていた（計算と試験）」）｜副題：—｜権利：自作｜注：🔁 台本は実写（地下の床の写真は在庫に無い）＝§0' の「cb13 のくいを示す図か札」",
               src='A06（`the foundation pile capacity shown on the design drawings was sufficient`・`the basement slab did not show any distress`）'),
    'cb14': dict(kind='図解',
               plan='図 一覧（崩れの起こり＝プールデッキの継ぎ目の余裕の少なさ／大きくは関わっていない＝となりの工事の揺れ・地面・嵐など）｜権利：自作',
               src='TR0476・TR0454・TR0465・TR0474'),
    'cb15': dict(kind='フリー素材',     # ⑤b-7b：⑤b-1 で S#49（フリー素材）に替えた＝list19 の種類「フリー」と合わせた
               plan='N#18 は c702 → N#24（ライダーの撮像を相談する連邦職員）か B2 の別の秒｜副題：—｜権利：A｜注：⑤b-1 で同じ絵を2回使わない',
               src='TR0454（`Things that most probably did not contribute significantly to the collapse include vibrations from the construction of 87 Park.`）'),
    'cb16': dict(kind='写真',
               plan='B1@74–77.8（鉄筋の出た床とコーン）｜副題：崩落の現場の床（2021年6〜7月）｜権利：A推定｜注：—',
               src='—（橋）'),
}

TR_SRC = "NIST の技術的知見の動画（2026年6月）"
EX_NOTE = "掘った所・壁・柱の位置と大きさは模式（揺れの大きさの比も模式）"
A06_SRC = "NIST の発表（2025年6月）"

SPEC = {
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）──
    # cb02（13.46秒＝0〜4.47／4.96〜8.73／9.22〜13.46）＝87パークの掘削と鋼の板（TR0455・0456・TF p9169）。
    #   🔴 頭に差し込み（S#38 基礎の工事の重機・5.1秒・「イメージ」）＝⑤b-7 で差し込みの層。図の1段目は差し込みの下に隠れる
    #   ✅ ⑤b-7c：寄せ（USE の zoom 1.55・xbias 0・bias 0.49＝切り口 x 0〜1652・y 250〜1179）で重機の LIEBHERR の字（x 1877 より右）を外した
    "cb02": dict(
        t="となりの工事", s="鋼の板を打ち込んだ",
        intro=ss.head("cb02"),
        fig=("m19", dict(view="excav",
                         steps=[dict(state=dict(pit="on"), delay=0.3, tag=dict(t="87パークの掘った所", at="pit", to="pit")),
                                dict(state=dict(drive="on"), delay=0.3, tag=dict(t="鋼の板を揺らしながら打ち込む", at="pile", to="pile")),
                                # ⑥ の前（10-07・周2の注意）：「（9フィート）」の下 3px に基図の「この建物（北）」＝3行の札に読めた → 札を 16px 上へ
                                dict(state=dict(dist="on"), delay=0.3, tag=dict(t="約2.7メートル", d="（9フィート）", at=(780.0, 384.0, "start", 640.0), to="dist"))],
                         rel=[dict(t="87パーク", src="TR p1455（87 Park）"), dict(t="約2.7メートル", src="TR p1456（approximately 9 feet）"),
                              dict(t="9フィート", src="TR p1456")],
                         note=EX_NOTE, src=TR_SRC + "の語りとスライド")),
    ),
    # cb03（6.74秒＝0〜4.45／4.94〜6.74）＝揺れは中の人にも感じられた（TR0457）
    "cb03": dict(
        t="揺れへの心配", s="中の人も感じた",
        fig=("m19", dict(view="excav", start=dict(pit="on", drive="on"),
                         steps=[dict(state=dict(wave="on"), delay=0.3, tag=dict(t="揺れは建物の中にも伝わった", at="wave", to="wave"))],
                         note=EX_NOTE, src=TR_SRC + "の語り")),
    ),
    # cb05（8.91秒＝0〜5.12／5.62〜8.92）＝揺れは壁で大きく弱まり、継ぎ目の手前でさらに小さく（TR0461・TF p9173）
    "cb05": dict(
        t="弱まる揺れ", s="揺れの伝わり方",
        fig=("m19", dict(view="excav", start=dict(pit="on", drive="on", wave="on"),
                         steps=[dict(state=dict(damp="on"), delay=0.3, tag=dict(t="壁で弱まる", at="damp")),
                                # ⑤c'（10-07）：札が x 780（壁の波の上）にあり、指す物（継ぎ目の手前の波 x 1300・13.1 の柱の頭の輪 1340,504）から
                                #    500px 以上離れていた＝輪の左上の空へ移し、輪の上の端へ線を引く
                                dict(state=dict(damp="more"), delay=0.3,
                                     tag=dict(t="継ぎ目の手前でさらに小さく", at=(1060.0, 400.0, "start", 640.0), to=(1340.0, 474.0)))],
                         note=EX_NOTE, src=TR_SRC + "の語りとスライド")),
    ),
    # cb11（11.75秒＝0〜2.02／2.51〜7.19／7.68〜11.75）＝人工衛星のデータ＝沈みは無い（A06）
    "cb11": dict(
        t="地面の沈み", s="宇宙からの測定",
        fig=("m19", dict(view="sat",
                         steps=[dict(tag=dict(t="地面の下の空洞？", at="q")),
                                dict(state=dict(sat="on"), delay=0.3, tag=dict(t="5年間：沈みは見られない", at="sat")),
                                dict(state=dict(near="on"), delay=0.3, tag=dict(t="数日前：建物の近くも沈みなし", at="near", to="tower"))],
                         rel=[dict(t="5年間", src="A06（in the five years before the partial collapse）")],
                         note="人工衛星と区画は模式（沈みの色は無し＝どこも同じ色）", src=A06_SRC)),
    ),
    # cb12（9.93秒＝0〜4.44／4.93〜9.93）＝石灰岩と空洞（A06＝no evidence of karst）。例の空洞は建物の下に描かない（門番が照らす）
    "cb12": dict(
        t="石灰岩の地面", s="空洞の跡は無い",
        fig=("m19", dict(view="ground",
                         steps=[dict(state=dict(lime="on", cave="on"), delay=0.3,
                                     tag=[dict(t="石灰岩", at="lime", to="lime"), dict(t="（例）水に溶けてできる空洞", at="cave", to="cave")]),
                                dict(state=dict(none="on"), delay=0.3, tag=dict(t="建物の下：空洞の跡なし", d="むしろ、できにくい性質", at="none", to="none"))],
                         note="地面の重なりとくいの数は模式（右の空洞は説明のための例）", src=A06_SRC)),
    ),
    # cb13（6.40秒＝0〜2.41／2.90〜6.40）＝くいと地下の床（A06）。札「くい：強さは足りていた（計算と試験）」＝台本の注（§0'）
    "cb13": dict(
        t="くいと地下の床", s="土台の確かめ",
        fig=("m19", dict(view="ground", start=dict(lime="on"),
                         steps=[dict(state=dict(pile="on"), delay=0.3, tag=dict(t="くい：強さは足りていた", d="（計算と試験）", at="pile", to="pile")),
                                dict(state=dict(floor="on"), delay=0.3, tag=dict(t="地下の床：ひびや沈みは無い", at="floor", to="floor"))],
                         note="地面の重なりとくいの数は模式", src=A06_SRC)),
    ),
    # ── 🆕 ⑤b-6（2026-10-06）：並べ図・流れ図（箱の型）。一覧 → 並べ図＝同じ形で並べるだけ（アイコンは描かない＝場面にしない）──
    # cb09（6.89秒＝0〜3.34／3.83〜6.89）＝NIST が崩れに大きくは関わっていないとしたもの（TR0465）。2行目で前半の3つ
    "cb09": dict(
        t="関わりの小さいもの", s="NIST の見立て",
        fig=("boxes", dict(view="row", slots=9, per=3, steps=[
            dict(),
            dict(add=[ss.cause("n_found"), ss.cause("n_sink"), ss.cause("n_storm")])],
            src=ss.src(["TR p1465"]))),
    ),
    # cb10（6.52秒＝0〜2.52／3.01〜6.52）＝同じ並びの後半（1行目＝衝突・爆発・クレーン／2行目＝屋上の工事の重さ）
    "cb10": dict(
        t="外からの力と工事", s="これも大きくは関わらない",
        fig=("boxes", dict(view="row", slots=9, per=3,
                           # ⚠️ 門番 check_boxes：沈めた色で残すと箱の色がそろわない（並べ図はどれかを目立たせない）＝keep で同じ色のまま
                           past=[ss.cause("n_found", keep=True), ss.cause("n_sink", keep=True), ss.cause("n_storm", keep=True)], steps=[
            dict(add=[ss.cause("n_car"), ss.cause("n_blast"), ss.cause("n_crane")]),
            dict(add=ss.cause("n_roof"))],
            src=ss.src(["TR p1465"]))),
    ),
    # cb14（8.10秒＝0〜3.23 聞き役／3.72〜8.10）＝1行目で「大きくは関わっていない」の群（となりの工事の揺れ・地面・嵐ほか）・2行目で起こり
    #   （TR0476＝余裕の少なさと傷み）。一覧 → 流れ図（2つの群に分ける）
    "cb14": dict(
        t="崩れの起こり", s="建物の中にあった",
        fig=("boxes", dict(view="flow", layout=ss.FL_EMPTY, steps=[
            dict(add=[dict(k="grp", t="大きくは関わっていない", x=1100, y=370), ss.fl("x_vib"), ss.fl("x_gnd"), ss.fl("x_ext")]),
            dict(add=[dict(k="grp", t="起こり", x=110, y=370), ss.fl("o_mg"), ss.fl("o_deg")])],
            src=ss.src(["TR p1454・p1465・p1476"]))),
    ),
    # ── 🆕 ⑤b-7a（2026-10-06）：写真・映像 ──
    # cb01＝B2 の13.0秒の止め絵（2秒の区間を9秒に伸ばさない）・札「言われていた話」・重機の CAT はもとから在る字
    "cb01": ss.vid("cb01", t="となりの建物の工事", s="南どなりの 87パーク と現場（2021年）"),
    # ⑤c'（10-07）：c806・c807 の「コンピュータの模型」にそろえた（「モデル」は画面でここだけだった）
    "cb04": dict(t="揺れの計算", s="コンピュータの模型を見る調査団（2023年4月）",
                 photo=P("n43_model"), **ss.kind(P("n43_model"))),
    "cb16": ss.vid("cb16", t="その後", s="崩落の現場の床（2021年6〜7月）"),
    # ── 🆕 ⑤b-7b（2026-10-06）：NIST のスライド185（色は変えない）──
    # フリー素材（イメージ）：cb08＝集合住宅を見上げる・cb15＝基礎の穴を掘る重機の筒
    "cb08": ss.vid("cb08"),
    "cb15": ss.vid("cb15"),
    "cb07": dict(t="計算した揺れ", s="87パークの工事の揺れの計算の図",
                 photo=P("tf_p185_87park"), panel=True, color=1.0),
    # ── 🆕 ⑤b-8（2026-10-07）：決め所 ──
    # cb06＝TR0462「Vibrations at the critical slab-column connections were too small to have caused structural damage.」
    "cb06": dict(
        t="揺れの答え", s="大事な継ぎ目での揺れ",
        fig=("quote", dict(phrase="工事の揺れは継ぎ目を傷めるには小さすぎた",
                           rows=ss.qrows("TR", None, ("箇所", "発表の語り")), paper=True)),
    ),
}
