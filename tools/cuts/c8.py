# -*- coding: utf-8 -*-
"""第7章　プールデッキから c801–c820（20カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c8.py`）。
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
    'c801': dict(kind='図解',
               plan='図 模式図【横から】柱と床の板（床の重さの矢印が下・柱の矢印が上＝TR0062〜0064 の図の型）｜権利：自作',
               src='TR0062〜0064'),
    'c802': dict(kind='写真',     # ⑤b-7c：絵は NIST の動く図（GIF）＝映像として数える（ca12 と同じ）
               plan='GIF（NIST の押し抜きせん断の動く図）｜副題：NIST のアニメーション｜権利：A｜注：🔁 台本は模式図。c801 の模式図の次',
               src='TR0065・TR0066'),
    'c803': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0070（`It is as though the column punches through the slab.`）・TR0021・TR0069・TR0071'),
    'c804': dict(kind='図解',
               plan='図 模式図（はさみで紙を切る絵 → 柱が床をずらして押し抜く絵・柱の頭にフックの形の鉄筋が残る）｜権利：自作',
               src='TR0072・TR0020・TR0021（用語の説明）'),
    'c805': dict(kind='図解',
               plan='図 模式図【上から】最初の2か所（K-13.1・L-13.1 の札・まわりの継ぎ目に色＝TR0095 の図の型）｜権利：自作',
               src='TR0023・TR0075・TR0067・TR0068・TR0015（`We examined two dozen possible scenarios for where and how the failure started.`）'),
    'c806': dict(kind='図解',
               plan='図 流れ図（3つの道具：コンピュータの模型・実物大の試験・ひびの理論）｜権利：自作',
               src='TR0257'),
    'c807': dict(kind='図解',
               plan='図 模式図【上から】コンピュータの模型（継ぎ目ごとの重さとたわみの色＝TR0258 の図の型）｜権利：自作',
               src='TR0258'),
    'c808': dict(kind='写真',
               plan='B8@129〜（ワシントン大学の区間・⑤b-1）｜副題：実物大の試験（ワシントン大学）｜権利：A推定（撮影者の記載なし）｜注：128秒の表題カードの後だけ。2:08 より前はミネソタ大学＝使わない',
               src='TR0260（`build and load-test to failure eight full-scale replicas`）・A06（`slab-column connection test at the University of Washington`）・TR0262（`built as faithfully as possible to replicate the conditions existing in CTS at the time of failure`）'),
    'c809': dict(kind='写真',
               plan='B8@188–198（真上から見た試験体の床・ワシントン大学）｜副題：試験体の床（ワシントン大学）｜権利：A推定｜注：梯子の商標 WERNER／LEANSAFE はもとから在る字',
               src='TR0261（`10 foot, 6 inches square`）・TR0263・§9'),
    'c810': dict(kind='写真',
               plan='B8@⑤b-1（129〜187・199〜207 のうち油圧ジャッキの見える秒＝188〜198 は c809）｜副題：試験体と油圧ジャッキ（ワシントン大学）｜権利：A推定｜注：🔁 台本の型 fb_c327（80〜88秒）はミネソタ大学＝使わない',
               src='TR0263（`loaded by eight hydraulic jacks arranged around the slab perimeter`）'),
    'c811': dict(kind='図・写真の頁',
               plan='tf_p084_salt（TF スライド84＝塩水の槽と電極）｜副題：NIST の技術的知見のスライド84｜権利：A｜注：🔁 台本の型 fb_c328（ミネソタ大学）→ スライド',
               src='TR0266・TR0267'),
    'c812': dict(kind='写真',
               plan='N#70（床の上面のひび・ワシントン大学）｜差し込み（tail）：2 N#66  4.1秒 N#66（床を切った断面の斜めのひび・1430x804＝額装）｜副題：試験のあとの床（ワシントン大学・2025年）｜権利：A｜注：—',
               src='TR0265・A06（`The cut reveals shear cracking and failure at the surface.`）'),
    'c813': dict(kind='写真',
               plan='N#69（わざと錆びさせた鉄筋の標本）｜副題：錆びさせた鉄筋の標本（ワシントン大学・2025年）｜権利：A｜注：—',
               src='TR0268・TR0448（`moderate corrosion can significantly reduce the capacity of connections`）'),
    'c814': dict(kind='図解',
               plan='図 模式図【横から】ひびの幅（柱のまわりの斜めのひび・幅が限界に届くと壊れる＝TR0271 の図の型）｜権利：自作',
               src='TR0269〜0272'),
    'c815': dict(kind='図解',
               plan='図 グラフ（青い線＝継ぎ目にかかる力・赤い線＝耐えられる限界・交わる所に印＝TR0273〜0276 の図の型）｜権利：自作',
               src='TR0272〜0276'),
    'c816': dict(kind='図解',
               plan='図 数の比べ（決まりどおりの継ぎ目＝赤い線が青い線のずっと上・大きな余裕）｜権利：自作',
               src='TR0073'),
    'c817': dict(kind='図解',
               plan='図 数の比べ（プールデッキの継ぎ目＝2本の線が重なる・余裕ゼロ）｜権利：自作',
               src='TR0074（`those margins against failure were zero at the time of failure`）'),
    'c818': dict(kind='写真',
               plan='N#61（床と柱の継ぎ目のせん断破壊）｜副題：実物大の試験で壊れた継ぎ目（ワシントン大学・2025年）｜権利：A｜注：—',
               src='TR0074・TR0474'),
    'c819': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TR0019（`In the case of Champlain Towers South, these margins against failure were too narrow from the start.`）'),
    'c820': dict(kind='写真',
               plan='B2@46–49.5（デッキの床面を歩く作業員・上から）｜副題：プールデッキの跡（崩落の後・2021年）｜権利：A推定｜注：顔は小さい（台帳）',
               src='—（橋）'),
}

TR_SRC = "NIST の技術的知見の動画（2026年6月）"
PU_NOTE = "床の厚さ・柱の太さ・ひびの幅は模式"

SPEC = {
    # ── 🆕 ⑤b-7c（2026-10-07）：NIST の押し抜きせん断の動く図（GIF 0〜6.68秒・167コマ＝字と © なし・白地の断面）──
    #   床が柱のまわりで曲がり、斜めのひびが開いて床が柱から抜ける（語りの「斜めのひび」「継ぎ目は強さを失う」と同じ順）
    "c802": ss.vid("c802", t="抜けていく床", s="床と柱の継ぎ目の断面（NIST のアニメーション）"),
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）──
    #   ⚠️ c802（NIST の押し抜きせん断の動く図＝GIF）は模式図ではない＝⑤b-7c で映像として受けた（上）
    # c801（7.42秒＝0〜2.10／2.60〜7.42）＝床の重さは下・柱は上へ押し返す（TR0062〜0064）
    "c801": dict(
        t="押し抜きせん断", s="柱と床の板の継ぎ目",
        fig=("m19", dict(view="punch",
                         steps=[dict(tag=dict(t="柱", at="q", to="col")),
                                dict(state=dict(load="on", react="on"), delay=0.3,
                                     tag=[dict(t="重さで床は下へ", at="slab", to="slab"), dict(t="柱は上へ押し返す", at="react", to="react")])],
                         note=PU_NOTE, src=TR_SRC + "の語りと図")),
    ),
    # c804（11.03秒＝0〜3.60／4.09〜7.39／7.88〜11.03）＝落ちきるとフックの形の鉄筋（TR0072）・はさみ・押し抜き（TR0020・0021）
    "c804": dict(
        t="落ちきったあと", s="はさみで切るように",
        fig=("m19", dict(view="punch", start=dict(crack="wide"),
                         steps=[dict(state=dict(drop="on", hook="on"), delay=0.3, dur=1.4,
                                     tag=dict(t="柱の頭にフックの形の鉄筋", at="hook", to="hook")),
                                dict(state=dict(scis="on"), delay=0.3, tag=dict(t="はさみ＝ずらして断ち切る", at="scis")),
                                dict(state=dict(shear="on"), delay=0.3, tag=dict(t="柱が床をずらして押し抜く", at="shear"))],
                         note=PU_NOTE, src=TR_SRC + "の語りと図")),
    ),
    # c805（9.02秒＝0〜4.24／4.73〜9.02）＝最初の2か所はまわりが支えた（TR0023・0067・0068・0075）・24通りの筋書き（TR0015）
    "c805": dict(
        t="支え合う継ぎ目", s="比べた筋書き",
        fig=("m19", dict(view="seq", start=dict(first="on", second="on", around="on"),
                         steps=[dict(tag=dict(t="まわりが支えて落ちず", at="around", to="around")),
                                dict(tag=dict(t="筋書き 24通り", at="n24"))],
                         rel=[dict(t="24通り", src="TR p1015（two dozen possible scenarios）")],
                         note="点の位置と灰色の範囲は NIST の図の形・敷地の形は模式", src=TR_SRC + "の語りとスライド")),
    ),
    # c807（3.97秒＝1行）＝コンピュータの模型（TR0258・TF p9096＝駐車場・デッキ・1階のロビーの床の一部）
    "c807": dict(
        t="力の見積もり", s="網の目の模型",
        fig=("m19", dict(view="model",
                         steps=[dict(state=dict(calc="on"), delay=0.3,
                                     tag=[dict(t="継ぎ目の1つずつ", at="calc", to="cols"),
                                          dict(t="模型の範囲", d="駐車場・デッキ・ロビーの床の一部", at="nist")])],
                         rel=[dict(t="1つずつ", src="TR p1258（at each of the connections）")],
                         note="網の目と継ぎ目の印は模式（計算の値の色は描かない）", src=TR_SRC + "の語りとスライド")),
    ),
    # c814（10.49秒＝0〜2.73／3.22〜7.07／7.57〜10.49）＝ひびの幅の理論（TR0269〜0272）
    "c814": dict(
        t="ひびの幅の理論", s="押し抜きを見積もる",
        fig=("m19", dict(view="punch", start=dict(load="on"),
                         steps=[dict(state=dict(crack="on"), delay=0.3, tag=dict(t="柱のまわりの斜めのひび", at="crack", to="crack")),
                                dict(state=dict(crack="wide", gauge="on"), delay=0.3,
                                     tag=dict(t="ひびの幅が限界に届くと壊れる", at="wide", to="crack")),
                                dict(tag=dict(t="欧州の基準の元の理論", at="code"))],
                         note=PU_NOTE, src=TR_SRC + "の語り")),
    ),
    # ── 🆕 ⑤b-6（2026-10-06）：流れ図（箱の型）・2本の線（模式図 m19 の curve＝NIST のグラフの型・数は出さない）──
    # c806（6.79秒＝0〜1.31 聞き役／1.80〜6.79）＝3つの道具（TR0256・TR0257）→ 継ぎ目にかかる力と強さ
    "c806": dict(
        t="確かめ方", s="NIST の3つの道具",
        fig=("boxes", dict(view="flow", layout=ss.FL_EMPTY, steps=[
            dict(),
            dict(add=[ss.fl("t_fem"), ss.fl("t_lab"), ss.fl("t_csct"), ss.fl("t_eval"),
                      ss.ce(["t_fem", "t_lab", "t_csct"], "t_eval")])],
            src=ss.src(["TR p1256・p1257"]))),
    ),
    # c815（13.28秒＝0〜3.94／4.43〜7.93／8.42〜13.29）＝NIST のグラフの型（TR0272〜0276）。グラフ → 模式図（数・目盛りは出さない）。
    #   1行目でひびの幅を決めるもの・2行目で青い線と赤い線・3行目で交わる所（交われば壊れると読む）
    "c815": dict(
        t="壊れるかの読み方", s="2本の線",
        fig=("m19", dict(view="curve",
                         steps=[dict(delay=0.3, tag=dict(t="ひびの幅＝床の厚さと傾きから", at="xaxis")),
                                dict(state=dict(blue="on", red="mid"), delay=0.3,
                                     # ⑤b-6 の下見：交わる赤い線（mid）は右の端が青い線より下＝札の高さを入れ替える（青の札が赤い線の端の隣に来た）
                                     tag=[dict(t="継ぎ目にかかる力", at=(1520.0, 470.0, "start", 300.0), to="blue"),
                                          dict(t="耐えられる限界", at=(1520.0, 640.0, "start", 300.0), to="red")]),
                                dict(state=dict(cross="on"), delay=0.3, tag=dict(t="交わる所で壊れる", at="cross", to="cross"))],
                         note="線の形は模式（NIST のグラフの型・数は出さない）", src=TR_SRC + "の語り")),
    ),
    # c816（6.39秒＝0〜4.27／4.76〜6.39）＝決まりどおりの継ぎ目（TR0073＝大きく離れる）。1行目で2本の線・2行目で余裕の矢印
    "c816": dict(
        t="決まりどおりなら", s="線は離れている",
        fig=("m19", dict(view="curve",
                         steps=[dict(state=dict(blue="on", red="high"), delay=0.3,
                                     tag=[dict(t="かかる力", at="blue", to="blue"), dict(t="耐えられる限界", at="red", to="red")]),
                                dict(state=dict(gap="on"), delay=0.3, tag=dict(t="余裕", at="gap", to="gap"))],
                         note="線の形は模式（NIST のグラフの型・数は出さない）", src=TR_SRC + "の語り")),
    ),
    # c817（6.21秒＝0〜3.32／3.81〜6.21 聞き役）＝プールデッキの継ぎ目（TR0074＝壊れたとき余裕はゼロ）。1行目で2本の線が交わる・輪
    "c817": dict(
        t="実際の継ぎ目", s="壊れたとき",      # ⚠️ echo：「プールデッキの継ぎ目」は字幕の切り取り
        fig=("m19", dict(view="curve",
                         steps=[dict(state=dict(blue="on", red="touch", cross="on"), delay=0.3,
                                     tag=[dict(t="かかる力", at="blue", to="blue"), dict(t="耐えられる限界", at="red", to="red"),
                                          dict(t="余裕ゼロ", at="cross", to="cross")]),
                                dict()],
                         note="線の形は模式（NIST のグラフの型・数は出さない）", src=TR_SRC + "の語り")),
    ),
    # ── 🆕 ⑤b-7a（2026-10-06）：写真・映像（ワシントン大学の試験＝B8 の 128秒より後だけ）──
    "c808": ss.vid("c808", t="8体の試験体", s="実物大の試験（ワシントン大学）"),
    "c809": ss.vid("c809", t="床の板の広さ", s="試験体の床（ワシントン大学）"),
    "c810": ss.vid("c810", t="8本のジャッキ", s="試験体と油圧ジャッキ（ワシントン大学）"),
    # c812＝2行目（床を切った断面）は写真の差し込み（尻＝N#66・1430×804＝額装）
    "c812": dict(t="試験体の壊れ方", s="試験のあとの床（ワシントン大学・2025年）",
                 photo=P("n70_slab_cracks"), **ss.kind(P("n70_slab_cracks")),
                 tail=dict(t="床の断面", s="切った床の断面の斜めのひび（2025年）", photo=P("n66_slab_section"),
                           **ss.kind(P("n66_slab_section")), at=1)),
    "c813": dict(t="錆と継ぎ目の強さ", s="鉄筋をわざと錆びさせた床の標本（ワシントン大学・2025年）",
                 photo=P("n69_corroded_bars"), **ss.kind(P("n69_corroded_bars"))),
    "c818": dict(t="継ぎ目の壊れ", s="実物大の試験で壊れた継ぎ目（ワシントン大学・2025年）",
                 photo=P("n61_shear_uw"), **ss.kind(P("n61_shear_uw"))),
    "c820": ss.vid("c820", t="次は設計と施工", s="プールデッキの跡（崩落の後・2021年）"),
    # ── 🆕 ⑤b-7b（2026-10-06）：NIST のスライド（色は変えない）──
    "c811": dict(t="錆びさせる試験", s="塩水の槽と電極・試験の終わりの鉄筋",
                 photo=P("tf_p084_salt"), panel=True, color=1.0),
    # ── 🆕 ⑤b-8（2026-10-07）：決め所 ──
    # c803＝TR0070「It is as though the column punches through the slab.」（as though＝まるで）
    "c803": dict(
        t="継ぎ目の壊れ方", s="NIST のたとえ",
        fig=("quote", dict(phrase="まるで柱が床を突き抜けたよう",
                           rows=ss.qrows("TR", None, ("箇所", "発表の語り")), paper=True)),
    ),
    # c819＝TR0019「In the case of Champlain Towers South, these margins against failure were too narrow from the start.」
    "c819": dict(
        t="NIST のまとめ", s="建てた時からの弱さ",
        fig=("quote", dict(phrase="壊れないための余裕は、最初から狭すぎた",
                           rows=ss.qrows("TR", None, ("箇所", "発表の語り")), paper=True)),
    ),
}
