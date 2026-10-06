# -*- coding: utf-8 -*-
"""第1章　海辺の12階建て c201–c213（13カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c2.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep19/make_plan19.py` で
  映像方針の一覧 `ref/ep19/eizou_build/list19.tsv`（承認ずみ・決め①〜⑩）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」と「フリー素材」を数える）。
  ⚠️ plan の「⑤b-1」は1秒1コマの走査で区間を選ぶ所・秒（÷365 の見込み）は書き写さない＝narration.json の実測で組む。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P
from illu import A2_REC as A2R  # noqa: E402  🆕 ⑤b-3：A2 の部品の出典（描く側と同じ文）

PLAN = {
    'c201': dict(kind='フリー素材',     # ⑤b-7b：⑤b-1 で S#46（フリー素材）に替えた＝list19 の種類「フリー」と合わせた
               plan='B2@⑤b-1（海岸の建物の並び・空撮）｜差し込み（tail）：3 P1  3.9秒 P1（崩れる前の建物＝⑤b-1 で写っていれば）｜副題：海岸と現場（崩落の後・2021年）／崩れる前（2012年）｜権利：A推定／CC BY 3.0（顔だけモザイクなら「改変」）｜注：決め④＝P1 に建物が写るかを⑤b-1 で原寸で見る・写らなければ P3（2013年）・どちらも無ければ差し込まない。副題は写り方を見てから。決め③＝C11（BY-SA）は使わない',
               src='TR0053・TR0005'),
    'c202': dict(kind='パネル',
               plan='この動画の資料（台本のまま）｜差し込み（head）：1 B1 約9秒 3.3秒 B1@約9秒（建物の銘板 CHAMPLAIN TOWERS 8777 SOUTH）｜副題：建物の銘板（2021年6〜7月）｜権利：A推定｜注：横顔の作業員は切り方で外すか顔だけモザイク（PD＝§B2-2b）',
               src='A03・A01・A15・A08・A11・A14・A17'),
    'c203': dict(kind='図解',
               plan='図 流れ図 この動画の資料の並び（2018 調査の報告・議事録 → 2021-12 大陪審の報告 → 2026-06 NIST の結果の動画 → 2026-08 文字起こし → 2026-09 諮問委員会の資料）｜権利：自作',
               src='A15・A16・A01'),
    'c204': dict(kind='パネル',
               plan='panel 数と時刻の言い方（長さはメートル・センチ／原文のフィート・インチは括弧／時刻は現地の時刻）｜権利：自作',
               src='—'),
    'c205': dict(kind='図・写真の頁',
               plan='図 p3 TF のスライド3（建物の3Dの画像・西／真ん中／東の部分・プールデッキ）',
               src='TR0004・TR0056・TR0057・TF p3'),
    'c206': dict(kind='図・写真の頁',
               plan='図 p3 TF のスライド3（寸法の札の画像の切り出し＝`12 stories 110\'-10" (33.8 m)`）',
               src='TF p3'),
    'c207': dict(kind='図解',
               plan='図 模式図【横から】フラットプレート（床のコンクリートの板が柱の上に直に載る・柱の上の継ぎ目に色）｜権利：自作',
               src='TR0054・TR0055'),
    'c208': dict(kind='図解',
               plan='図 模式図【上から】塔とプールデッキ・地上の駐車場（塔の南にプールデッキ・下は地下の駐車場の柱の並び）｜権利：自作',
               src='TR0058・TR0005'),
    'c209': dict(kind='再現イラスト',
               plan='図 再現イラスト A2 の地【横から】プールデッキ・地上の駐車場・地下の駐車場・塔の南の面（形＝TF p48 の3D・人は描かない）｜権利：自作',
               src='TR0005・TR0059・TF p48'),
    'c210': dict(kind='図解',
               plan='図 年表 建物の歩み（1979〜81年 設計と建設／1981年 完成／1996〜97年 補修／2018年 調査／2021年 40年の点検の期限）｜権利：自作',
               src='AC p.23・GJ p.2・TR0005'),
    'c211': dict(kind='決め所',
               plan='quote（決め所・大陪審の報告 p.2 の段＝40年の再認証の起こり）｜権利：自作',
               src='GJ p.2（`requirement for a 40-year building recertification followed another tragic event in Miami-Dade County`・`August 5, 1974, crushing to death 7 DEA employees and injuring 15 others`）'),
    'c212': dict(kind='図解',
               plan='図 書類の再現図 議事録の1行（2018-11-15・`The 40 year certification for the building will be due in 2021.`・名前は出さない）｜権利：自作',
               src='MIN18 p.7・GJ p.18'),
    'c213': dict(kind='写真',
               plan='B2@⑤b-1（95.8〜98.8 のデッキの面の引きとその前後）｜副題：プールデッキの跡（崩落の後・2021年）｜権利：A推定｜注：3秒の区間を2.6倍に伸ばさない＝走査で続きの秒・無ければ 97秒のコマを静止画で受ける',
               src='—（橋）'),
}

TR_SRC = "NIST の技術的知見の動画（2026年6月）"

SPEC = {
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）──
    # c207（9.33秒＝0〜2.07／2.56〜5.98／6.47〜9.33）＝フラットプレート（TR0054・0055）。柱と階の数は模式
    "c207": dict(
        t="梁の無い床", s="鉄筋コンクリートの造り",       # ⑤b-4 の echo：「フラットプレート」は語りそのまま＝見出しにしない
        fig=("m19", dict(view="flat",
                         steps=[dict(tag=dict(t="床の板と柱", at="name")),
                                dict(state=dict(plate="on"), delay=0.3, tag=dict(t="床の板が柱に直に載る", at="plate", to="slab")),
                                dict(state=dict(joint="on"), delay=0.3, tag=dict(t="床と柱の継ぎ目", at="joint", to="joint"))],
                         note="柱と階の数・寸法は模式", src=TR_SRC + "の語り")),
    ),
    # c208（9.56秒＝0〜1.62／2.11〜6.24／6.74〜9.56）＝塔の南のデッキ・地上の駐車場・地下の柱（TR0058・TR0005）。並びは A2 の top と同じ
    "c208": dict(
        t="敷地の並び", s="塔の南の床",          # ⑤b-4 の dup：札「プールデッキ」と同じ語を見出しにしない
        fig=("m19", dict(view="site",
                         steps=[dict(tag=dict(t="塔（12階建て）", at="tower", to="tower")),
                                dict(state=dict(zone="on", cols="on"), delay=0.3,
                                     tag=[dict(t="プールデッキ", at="deck", to="deck"), dict(t="地上の駐車場", at="park", to="park"),
                                          dict(t="下は地下の駐車場（柱）", at="cols", to="cols")]),
                                dict(state=dict(pool="on"), delay=0.3, tag=dict(t="プールとジャグジー", at="pool", to="pool"))],
                         rel=[dict(t="12階", src="TR p1004（12 stories tall plus a penthouse）")],
                         note="位置と大きさは模式（並びは NIST の模型の図）", src=TR_SRC + "の語りとスライド")),
    ),
    # ── 🆕 ⑤b-3（2026-10-06）：案C の置き場 A2（`tools/illu.py` の「19本目 ⑤b-3」の節）──
    # c209＝南西の上から（TF p48 の3D の向き）。1行目（0〜3.07）：地上の駐車場（西）とプールデッキ（東）／
    #   2行目（3.56〜7.59）：デッキの北の端と塔の真ん中・東の部分のつなぎ目（9.1 の線＝TR0059）。直前の c208 は上から見た模式図
    "c209": dict(
        fig=("illu", dict(
            place="A2", start=dict(view="oblique"), rec="TR p1005（地上の階のプールデッキと駐車場の床・地下の上の柱）",
            steps=[dict(state=dict(a2zone="both"), delay=0.4, rec=A2R["park"],
                        tag=[dict(t="地上の駐車場", at="park", off=(-150, 80), anchor="end"),
                             dict(t="プールデッキ", at="deck", off=(150, 60))]),
                   dict(state=dict(a2join="on"), delay=0.4, rec=A2R["join"],
                        # ⑤b-3 の下見：右の端（余白の線 1848）に寄りすぎた＝デッキの右の下（砂浜の上）へ
                        tag=dict(t="デッキと塔のつなぎ目", at="join", off=(230, 150)))])),
    ),
    # ── 🆕 ⑤b-5（2026-10-06）：年表（`tools/axis.py`・門番 check_axis＝記録の表 REC_AXIS）──
    # c210（11.22秒＝0〜5.80／6.29〜11.22）＝1行目「設計と建設は1979年から81年」で設計と建設の帯と完成／2行目「建って40年の建物は…
    #   その後も10年ごとに」で40年の括弧と点検の期限（議事録 p.7「due in 2021」）。予定の一覧の「1996〜97年 補修／2018年 調査」も2行目で並べる
    "c210": dict(
        t="建物の歩み", s="40年目の点検の決まり",
        fig=("axis", dict(ss.AX_LIFE, steps=[
            dict(add=[ss.ax("build"), ss.ax("done")], cur="1981"),
            dict(add=[ss.ax("y40"), ss.ax("fix"), ss.ax("survey"), ss.ax("due")], cur="2021")],
            # ⚠️ 門番 layout：断り＋6つの資料の出典は右の端（1848）を越えた＝断りを外し、出典は年の元（AC・議事録・TR）に絞る
            note="", src=ss.src(["AC p2023", "TR p1005・p1441", "MIN18 p4107"]))),
    ),
    # ── 🆕 ⑤b-6（2026-10-06）：箱の型（流れ図・書類の再現図＝`tools/boxes.py`・門番 check_boxes）──
    # c203（7.59秒＝0〜4.55／5.04〜7.59）＝この動画の資料（c202 の語り＝沈めた色）に、1行目で大陪審の報告を足す。
    #   🔴 PLAN の「→」（資料の並び）は矢印にしない＝資料どうしに因果は無い（群で分けるだけ）
    "c203": dict(
        t="もう1つの手がかり", s="市民が調べる仕組み",
        fig=("boxes", dict(view="flow", layout=ss.FL_DOCS,
                           past=[dict(k="grp", t="国の研究所 NIST", x=130, y=360), ss.fl("d_vid"), ss.fl("d_tr"), ss.fl("d_ac"),
                                 dict(k="grp", t="郡と町", x=1100, y=360), ss.fl("d_town")],
                           steps=[dict(add=ss.fl("d_gj")), dict()],
                           src=ss.src(["GJ p3004", "A16 p5801"]))),
    ),
    # c212（9.26秒＝0〜4.76／5.25〜9.26）＝紙2枚（別の書類を1枚に混ぜない）：議事録 p.7（期限）と大陪審の報告 p.18（何年も前に技術者を雇った）。
    #   1行目で議事録・2行目で大陪審の報告
    "c212": dict(
        t="期限の前の準備", s="2つの記録",
        fig=("boxes", dict(view="form", form=[ss.FORM_MIN40, ss.FORM_GJ18], steps=[
            dict(add=[dict(k="paper", i=0), dict(k="fill", i=0, f="40年の点検")]),
            dict(add=[dict(k="paper", i=1), dict(k="fill", i=1, f="管理組合"), dict(k="fill", i=1, f="始めた時期")])],
            note="欄の字は原文のまま・様式は再現", src=ss.src(["MIN18 p4107", "GJ p3021"]))),
    ),
    # ── 🆕 ⑤b-7a（2026-10-06）：写真・映像（list19 の区間と副題＝写っているもの・見出しは語りの写しにしない）──
    # ── 🆕 ⑤b-7b：カットまるごとのフリー素材（左上に「イメージ」・見出しなし＝`ss.vid` が stock の欄で t・s を空に）──
    #   c201＝マイアミビーチの浜と海沿いの建物の空撮（🟡 ホテルの看板＝⑤b-7 の試し焼きで原寸）
    "c201": ss.vid("c201"),
    "c213": ss.vid("c213", t="調査で見えた傷み", s="プールデッキの跡（崩落の後・2021年）"),
    # ── 🆕 ⑤b-7b（2026-10-06）：NIST のスライドの切り抜き（旧版の束から写した・色は変えない＝頁と同じ）──
    #   副題は中身（「スライドN」は出典の行が書く＝門番 dup）。c205 は上の端で切れた寸法の札を切り口の外へ
    "c205": dict(t="建物の形", s="西・真ん中・東の部分とプールデッキの図",
                 photo=P("tf_p003_model"), trim=(0.0, 0.055, 1.0, 1.0), panel=True, color=1.0),
    #   c206＝高さの札（12 stories 110'-10" (33.8 m)）と東の部分・屋上の階・地下の札
    "c206": dict(t="塔の高さ", s="高さの札と東の部分の図",
                 photo=P("tf_p003_model"), trim=(0.52, 0.06, 0.90, 0.62), panel=True, color=1.0),
}
