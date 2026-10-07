# -*- coding: utf-8 -*-
"""第4章　最後の3週間 c501–c526（26カット）。19本目（サーフサイドのマンション崩壊のリメイク）。

■ 🔴 2026-10-06（⑤b-1）：18本目（スレッシャー号）の中身を空にした＝git の `b11797a`（`git show b11797a:tools/cuts/c5.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep19/make_plan19.py` で
  映像方針の一覧 `ref/ep19/eizou_build/list19.tsv`（承認ずみ・決め①〜⑩）と台本 第2版 §4 の出典から機械で組んだ（手で写していない）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」と「フリー素材」を数える）。
  ⚠️ plan の「⑤b-1」は1秒1コマの走査で区間を選ぶ所・秒（÷365 の見込み）は書き写さない＝narration.json の実測で組む。
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P
from illu import A2_REC as A2R, A3_REC as A3R  # noqa: E402  🆕 ⑤b-3：A2・A3 の部品の出典（描く側と同じ文）

PLAN = {
    'c501': dict(kind='再現イラスト',
               plan='図 再現イラスト A3【横から】夜の地下の駐車場（柱と天井・門＝TF p50〜58 の3Dの形・人は描かない）｜権利：自作',
               src='TR0107・TR0108・TR0111・TR0112'),
    'c502': dict(kind='図・写真の頁',
               plan='図 p50 TF のスライド50（3週間前の3Dの画像・プランターと門の位置の青い点・右上の ©2021 の写真は切る）',
               src='TR0113・TR0114'),
    'c503': dict(kind='再現イラスト',
               plan='図 再現イラスト A3【横から】門（プールデッキと地上の駐車場のあいだ）｜権利：自作',
               src='TR0116'),
    'c504': dict(kind='図・写真の頁',
               plan='図 p50 TF のスライド50（門の描き起こしの画像・1か月前／3週間前の2段・札「目撃談にもとづく NIST の絵」）',
               src='TR0120・TR0121・TF p50'),
    'c505': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TF p50・p52（`Gate door is stuck and cannot be opened.`）'),
    'c506': dict(kind='図解',
               plan='図 模式図【上から】壊れ始めの候補6か所（プールデッキの黄色の6点・最初の2か所に赤い枠＝TR0105 の図の形）｜権利：自作',
               src='TR0105・TR0106・TR0115'),
    'c507': dict(kind='図解',
               plan='図 模式図【横から】柱の上の床のひびと、わずかに下がる床（K-13.1 の札）｜権利：自作',
               src='TR0123・TR0124・TR0106・TR0452'),
    'c508': dict(kind='図解',
               plan='図 模式図（同じ・まわりの床が重さを隣の柱へ渡す矢印）｜権利：自作',
               src='TR0138〜0141・TR0075・TR0076'),
    'c509': dict(kind='図・写真の頁',
               plan='図 p52 TF のスライド52（1週間前の3Dの画像・門の描き起こしの3段＝1か月前・3週間前・1週間前）',
               src='TR0126〜0129・TF p52（`Approx. 1" vertical shift after repairs.`）'),
    'c510': dict(kind='フリー素材',
               plan='S#12（古いコンクリートの縁を流れ落ちる水）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：—',
               src='TR0131'),
    'c511': dict(kind='再現イラスト',
               plan='図 再現イラスト A3【横から】柱を伝う水（水の筋だけ・人は描かない・札「目撃した人の話にもとづく」）｜権利：自作',
               src='TR0132〜0134'),
    'c512': dict(kind='再現イラスト',
               plan='図 再現イラスト A3（同じ柱・変色の筋）｜権利：自作',
               src='TR0135'),
    'c513': dict(kind='図解',
               plan='図 模式図【上から】2か所目の継ぎ目（L-13.1）と1か所目（K-13.1）の位置｜権利：自作',
               src='TR0136・TR0452・TR0095'),
    'c514': dict(kind='図解',
               plan='図 模式図【上から】まわりの継ぎ目（危うくなった柱に色）｜権利：自作',
               src='TR0142'),
    'c515': dict(kind='図・写真の頁',
               plan='図 p57 TF のスライド57（17時間前の3Dの画像・右上の CTS Receiver の写真は切る）',
               src='TR0143・TR0145・TR0158'),
    'c516': dict(kind='図・写真の頁',
               plan='図 p57 TF のスライド57（聞き取りの図と手書きの注記の画像・札「目撃した人の聞き取りの注記（縮尺は合っていない）」）',
               src='TR0147・TF p57・AC p.29'),
    'c517': dict(kind='決め所',
               plan='quote（決め所）｜権利：自作',
               src='TF p57・AC p.29（`Morning June 23 noticed in the floor area, a space or gap of 4inches`）'),
    'c518': dict(kind='再現イラスト',
               plan='図 再現イラスト A2 の地【上から】プランターと床の隙間の位置｜権利：自作',
               src='TR0145・TR0146・TR0158'),
    'c519': dict(kind='フリー素材',
               plan='S#11（錆の染みの配管に水がしたたる）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：屋内の配管＝駐車場の天井ではない',
               src='TR0148・TR0149'),
    'c520': dict(kind='図・写真の頁',
               plan='tf_p058_note（付箋）｜副題：NIST のスライド58（付箋は聞き取りの注記・下地は管財人の原図）｜権利：A＋第三者（原図）｜注：紙面の引用（頁ごと・額装・無加工・出典に CTS Receiver）か付箋だけに切り直す',
               src='TR0153・TR0154・TF p58（付箋＝p9813）・AC p.30'),
    'c521': dict(kind='図解',
               plan='図 模式図【横から】しずく → 蛇口（時間の帯：9時間前 → 3時間前）｜権利：自作',
               src='TR0155・TR0160・AC p.31'),
    'c522': dict(kind='図解',
               plan='図 模式図【上から】傷みの地図（3週間前・1週間前・17時間前・11時間前・9時間前・3時間前の点）｜権利：自作',
               src='TR0152・TR0156〜0160'),
    'c523': dict(kind='図解',
               plan='図 時間の帯（3週間前 門・プランター → 1週間前 柱の水 → 17時間前 隙間 → 9時間前 天井の漏れ → 3時間前）｜権利：自作',
               src='TR0156〜0160'),
    'c524': dict(kind='写真',
               plan='N#13（仮置き場で札を付け撮影・潰れた車と瓦礫）｜副題：がれきから運び出した部材（2021年7月）｜権利：A｜注：—',
               src='TR0474・TR0472'),
    'c525': dict(kind='再現イラスト',
               plan='図 再現イラスト A3【横から】夜の駐車場（止まった車・人は描かない）｜権利：自作',
               src='TR0162・TR0165'),
    'c526': dict(kind='フリー素材',
               plan='S#6（夜の暗い海と波）｜副題：イメージ｜札：イメージ｜権利：Pexels License｜注：🔁 台本は実写（夜明けの海岸線の記録は無い）→ フリー素材に',
               src='—（橋）'),
}

TR_SRC = "NIST の技術的知見の動画（2026年6月）"

SPEC = {
    # ── 🆕 ⑤b-3（2026-10-06）：案C の置き場 A3（地下の駐車場・西を向いて見た断面）と A2（上から）──
    #   A3 の左上にはいつも位置の小さな地図（切り口＝L の線・目の印＝西を向く）＝見る向きの合図（門番 ㉑）。人は描かない
    # c501（10.49秒）＝1行目は聞き役の問い／2行目（2.04〜）：デッキの上のプランターの壁／3行目（6.81〜）：横に長いひびと角のずれ（TR0111・0112）
    "c501": dict(
        fig=("illu", dict(
            place="A3", rec="TR p1107（崩れる約3週間前からの傷みの流れ）",
            # ⑤b-3 の下見：プランターが画面の中で小さく、札が左上の小さな地図の下に隠れた＝2行目で寄る（札は寄る前の絵に置く＝一緒に寄る）
            steps=[dict(),
                   dict(state=dict(a3plant="on", cam=1.6), delay=2.6, dur=1.6, rec=A3R["planter"],
                        tag=dict(t="プランターの壁", at="planter", off=(-60, -110), anchor="end")),
                   dict(state=dict(a3crack="on"), delay=0.3, rec=A3R["crack"],
                        tag=dict(t="ひびと角のずれ", at="crack", off=(40, 110)))],
            camc=(760.0, 330.0))),
    ),
    # c503（7.43秒）＝目撃した人の話（TR0116）。1行目：デッキと地上の駐車場のあいだの門／2行目：門へ寄る
    "c503": dict(
        fig=("illu", dict(
            place="A3", rec="TR p1116（目撃した人が NIST に話した）", assume="目撃した人の話にもとづく",
            steps=[dict(state=dict(a3gate="on"), delay=0.8, rec=A3R["gate"],
                        tag=dict(t="デッキと駐車場の門", at="gate", off=(100, -60))),
                   dict(state=dict(cam=1.5), delay=0.2, dur=3.2)],
            camc=(965.0, 320.0))),
    ),
    # c511（10.47秒）＝目撃した人の話（TR0132〜0134）。1行目：柱 L-13.1 を伝う水／2行目：柱のまわりの天井の高さの変化／
    #   3行目：デッキの水がこの1本へ集まるよう（向きの矢印だけ）
    "c511": dict(
        fig=("illu", dict(
            place="A3", rec="TR p1132（柱 L-13.1）", assume="目撃した人の話にもとづく",
            steps=[dict(state=dict(a3water="on"), delay=0.3, rec=A3R["water"],
                        tag=dict(t="柱を伝う水", at="col", off=(120, 40))),
                   dict(state=dict(a3ceil="on"), delay=1.8, rec=A3R["ceil"],
                        tag=dict(t="天井の高さの変化", at="ceil", off=(140, 90))),
                   dict(state=dict(a3funnel="on"), delay=0.6, rec=A3R["water"],
                        # ⑤c'（10-07・原寸）：札の左上（x 432）が左上の「目撃した人の話にもとづく」の箱（〜449・〜182）の角に重なった＝右へ40
                        tag=dict(t="デッキの水", at="deck", off=(-20, -110), anchor="end"))])),
    ),
    # c512（7.13秒）＝同じ柱の 2020年11月の写真（TR0135）。水の筋（2021年6月）は出さない＝時が違う
    "c512": dict(
        fig=("illu", dict(
            place="A3", rec="TR p1135（2020年11月の写真）",
            steps=[dict(state=dict(a3stain="on"), delay=1.6, rec=A3R["stain"],
                        tag=dict(t="変色と塗料の筋", at="stain", off=(140, -40))),
                   dict(state=dict(cam=1.2), delay=0.2, dur=2.0)],
            camc=(850.0, 560.0))),
    ),
    # c518（7.36秒）＝上から（A3 の横から → 上から＝切り替えの字）。目撃した人の話（TR0145・0146・0158）。
    #   隙間の幅は札に出さない（「約10センチ」は c517 の決め所）
    "c518": dict(
        fig=("illu", dict(
            place="A2", start=dict(switch="on"), rec="TR p1146（約11時間前の目撃が最後）", assume="目撃した人の話にもとづく",
            steps=[dict(state=dict(a2plant="gap"), delay=1.2, rec=A2R["planter"],
                        tag=dict(t="プランターと床の隙間", at="planter", off=(130, -130))),
                   dict(state=dict(cam=1.2), delay=0.2, dur=2.6)],
            camc=(975.0, 560.0))),
    ),
    # c525（8.99秒）＝6月23日の夜に止まっていた車（数と形は模式＝TR0162「何台か」）
    "c525": dict(
        fig=("illu", dict(
            place="A3", rec="TR p1165（落ちた床があれば目に入ったはず）",
            steps=[dict(state=dict(a3cars="on"), delay=1.2, rec=A3R["cars"],
                        tag=dict(t="止まっていた車", at="cars", off=(80, -110))),
                   dict(state=dict(cam=1.06), delay=0.2, dur=3.6)])),
    ),
    # ── 🆕 ⑤b-4（2026-10-06）：模式図（`tools/mech19.py`・門番 check_mech の judge_m19）。上から見た図は A2 の top と同じ並び ──
    # c506（9.48秒＝0〜4.20／4.69〜9.48）＝壊れ始めの候補6か所（TR0105・TF p9039）・赤い枠＝最初の2か所（TR0106）・K-13.1 の余裕（TR0115）
    "c506": dict(
        t="壊れ始めの候補", s="プールデッキの継ぎ目",
        fig=("m19", dict(view="cand",
                         steps=[dict(state=dict(cand="on"), delay=0.3, tag=dict(t="候補（6か所）", at="cand")),
                                dict(state=dict(red="on"), delay=0.3,
                                     tag=dict(t="門とプランターのそば", d="余裕は最小の部類（計算）", at="k131", to="k131"))],
                         rel=[dict(t="6か所", src="TR p1105（six locations in the pool deck）")],
                         note="点の位置は NIST の図（赤い枠＝NIST が最初に壊れたとみる2か所）・敷地の形は模式",
                         src=TR_SRC + "の語りとスライド")),
    ),
    # c507（8.42秒＝0〜4.91／5.40〜8.42）＝K-13.1 の継ぎ目（TR0123・0124・0452）。下がりは大きく描く（実際は数センチ）
    "c507": dict(
        t="最初の継ぎ目", s="最初に壊れた所",
        fig=("m19", dict(view="gspan",
                         steps=[dict(state=dict(crack="on", sag="on"), delay=0.4, tag=dict(t="K-13.1", d="6月の初め", at="k131", to="k131")),
                                dict(tag=dict(t="押し抜きせん断（第7章）", at="punch"))],
                         rel=[dict(t="K-13.1", src="TR p1123"), dict(t="6月の初め", src="TR p1452（early June）"),
                              dict(t="第7章", src="台本 第2版の章立て")],
                         note="下がりは大きく描いた模式（実際は数センチ）", src=TR_SRC + "の語り")),
    ),
    # c508（10.58秒＝0〜2.17／2.66〜6.60／7.09〜10.58）＝まわりの床が重さを隣の柱へ（TR0138〜0141）・1か2インチ（TR0139）
    "c508": dict(
        t="残った床", s="重さを隣の柱へ",
        fig=("m19", dict(view="gspan", start=dict(crack="on", sag="on"),
                         steps=[dict(tag=dict(t="床は落ちずに残った", at="ok")),
                                dict(state=dict(share="on"), delay=0.3, tag=dict(t="隣の柱へ重さを渡す", at="share", to="adj")),
                                # ⑤c'（10-07）：「〜」は幅に読める＝語り・欄外と同じ「か」（1 or 2 inches）。
                                #    原寸：札（x 1000〜1351）の字が 11.1 の柱（1183〜1217）をまたいだ＝柱と柱のあいだは 306px しかない
                                #    ＝主の字を数だけにし、「下がり」は小さい字へ・13.1 の柱（〜877）の右に置く
                                dict(state=dict(dim="on"), delay=0.3,
                                     tag=dict(t="約2.5か5センチ", d="下がり（NIST の見立て）", at=(905.0, 560.0, "start", 266.0), to="sag"))],
                         rel=[dict(t="2.5か5センチ", src="TR p1139（likely 1 or 2 inches）")],
                         note="下がりは大きく描いた模式（実際は約2.5か5センチ）", src=TR_SRC + "の語り")),
    ),
    # c513（8.18秒＝0〜3.12／3.61〜8.18）＝L-13.1（TR0136）・1か所目と2か所目（TR0452）
    "c513": dict(
        t="2か所目の継ぎ目", s="東どなりの柱",
        fig=("m19", dict(view="seq", start=dict(first="on"),
                         steps=[dict(state=dict(second="on"), delay=0.3, tag=dict(t="L-13.1", at="l131", to="l131")),
                                dict(tag=[dict(t="1か所目：6月の初め", at="k131", to="k131"),
                                          dict(t="2か所目：6月の中ごろ", at="l2", to="l131")])],
                         rel=[dict(t="L-13.1", src="TR p1136"), dict(t="1か所目・2か所目", src="TR p1023"),
                              dict(t="6月の初め・中ごろ", src="TR p1452（early June・mid-June）")],
                         note="点の位置は NIST の図・敷地の形は模式", src=TR_SRC + "の語りとスライド")),
    ),
    # c514（9.51秒＝0〜2.25／2.74〜6.19／6.68〜9.51）＝まわりの継ぎ目（TR0140・0142・TF p9052 の灰色の範囲と丸い印の柱）
    "c514": dict(
        t="まわりの継ぎ目", s="どれも危うくなった",
        fig=("m19", dict(view="seq", start=dict(first="on", second="on"),
                         steps=[dict(state=dict(around="on"), delay=0.3, tag=dict(t="まわりの柱へ重さが回る", at="around", to="around")),
                                dict(tag=dict(t="どれも前より危うい", at="next")),
                                dict(tag=dict(t="次はどこでも（NIST）", at="two"))],
                         note="灰色の範囲と丸い印の柱は NIST の図の形・敷地の形は模式", src=TR_SRC + "の語りとスライド")),
    ),
    # c521（6.89秒＝0〜3.18／3.67〜6.89）＝しずく → 蛇口（TR0155・0159・0160）
    "c521": dict(
        t="しずくから蛇口へ", s="ひびからの水",
        fig=("m19", dict(view="drip",
                         steps=[dict(state=dict(band="on"), delay=0.3, tag=dict(t="約9時間前", d="しずく", at="h9", to="drip")),
                                dict(state=dict(flow="tap"), delay=0.3, tag=dict(t="約3時間前", d="蛇口のように", at="h3", to="drip"))],
                         rel=[dict(t="約9時間前", src="TR p1159（nine hours before）"), dict(t="約3時間前", src="TR p1160（three hours before）")],
                         note="ひびと水の量・柱の位置は模式", src=TR_SRC + "の語り")),
    ),
    # c522（5.42秒＝0〜3.41／3.90〜5.42）＝傷みの地図（TR0152・0156〜0160・TF p9057 の楕円・p9059 の点）
    "c522": dict(
        t="傷みの地図", s="何年も前からの漏れ",
        fig=("m19", dict(view="dmg",
                         steps=[dict(state=dict(leak="on"), delay=0.3, tag=dict(t="何年も漏れては直してきた所", at="leak", to="leak")),
                                dict(state=dict(pts="on"), delay=0.1,
                                     tag=[dict(t="3週間前・1週間前", d="門", at="gate", to="gate"),
                                          dict(t="3週間前", d="プランター（17・11時間前に隙間）", at="planter", to="planter"),
                                          dict(t="1週間前", d="柱を伝う水", at="water", to="water"),
                                          dict(t="9時間前・3時間前", d="天井の漏れ", at="leak2", to="leak")])],
                         rel=[dict(t="3週間前", src="TR p1156"), dict(t="1週間前", src="TR p1157（Two weeks later）"),
                              dict(t="17・11時間前", src="TR p1158"), dict(t="9時間前", src="TR p1159"), dict(t="3時間前", src="TR p1160")],
                         note="点の位置は NIST の図（漏れの楕円の大きさは模式）", src=TR_SRC + "の語りとスライド")),
    ),
    # ── 🆕 ⑤b-5（2026-10-06）：時間の並び（`tools/axis.py` の order・門番 check_axis）──
    # c523（6.83秒＝0〜4.11／4.60〜6.83）＝1行目「門、プランター、柱を伝う水、床の隙間、天井の漏れ」で5つの合図を NIST のスライドと同じ
    #   並び（約3週間前〜約3時間前・間隔は時間に比例しない）／2行目はそのまま
    "c523": dict(
        t="合図の並び", s="門から天井まで",      # ⚠️ dup：「最後の3週間」は右上の章の札と同じ
        fig=("axis", dict(view="order", stops=ss.SIGNS, end="塔が崩れる", steps=[
            dict(add=[ss.ax("s3w"), ss.ax("s1w"), ss.ax("s17h"), ss.ax("s9h"), ss.ax("s3h")], cur="約3時間前"),
            dict()],
            note=ss.ORDER_NOTE, src=ss.src(["TR p1156・p1157・p1158・p1159・p1160", "TF p9061"]))),
    ),
    # ── 🆕 ⑤b-7a（2026-10-06）：写真（調査員はスマホで撮る・顔はマスクで半分＝photo_check19）──
    "c524": dict(t="削られた余裕", s="がれきと潰れた車を調べる NIST の調査員（2021年7月）",
                 photo=P("n13_laydown"), **ss.kind(P("n13_laydown"))),
    # ── 🆕 ⑤b-7b（2026-10-06）：NIST のスライド（色は変えない）。🔴 c516・c520 は下地が管財人の原図＝紙面の引用＝額装・無加工
    #   （`assets.json` の frame＝`ss.check_frame_only` が切り出し・寄り・色を止める）
    # フリー素材（イメージ）：c510＝古いコンクリートの縁を流れ落ちる水・c519＝錆の染みの配管に水がしたたる・c526＝夜の暗い海と波
    "c510": ss.vid("c510"),
    "c519": ss.vid("c519"),
    "c526": ss.vid("c526"),
    "c502": dict(t="傷みが見つかった場所", s="プランターと門の位置の図（約3週間前）",
                 photo=P("tf_p050_3d"), panel=True, color=1.0),
    "c504": dict(t="門の描き起こし", s="目撃談にもとづく NIST の門の絵",
                 photo=P("tf_p050_gate"), panel=True, color=1.0),
    "c509": dict(t="3段の門の絵", s="目撃談にもとづく NIST の門の絵（3段）",
                 photo=P("tf_p052_gate"), panel=True, color=1.0),
    "c515": dict(t="最後の日の合図", s="プランターの位置の図（約17時間前）",
                 photo=P("tf_p057_3d"), panel=True, color=1.0),
    "c516": dict(t="目撃した人の話", s="聞き取りの注記（縮尺は合っていない）",
                 photo=P("tf_p057_memo"), panel=True, color=1.0),
    # ⑤c'（10-07）：上と左の端の写真の帯はスライド58 そのものの一部。下地の原図は引用＝額装（丸ごと・無加工）でしか使えない
    #   （trim を足したら cuts/__init__ の額装の門番が止めた）＝据え置き
    "c520": dict(t="地下で見えた漏れ", s="付箋の注記と管財人の原図",
                 photo=P("tf_p058_note"), panel=True, color=1.0),
    # ── 🆕 ⑤b-8（2026-10-07）：決め所 ──
    # c505＝スライド50 の絵の札「3 WEEKS BEFORE COLLAPSE」「Gate door is stuck and cannot be opened.」（目撃談にもとづく NIST の絵）
    "c505": dict(
        t="門の異変", s="目撃談にもとづく NIST の絵",
        fig=("quote", dict(phrase="崩れる3週間前、門が引っかかり開かない",
                           rows=ss.qrows("TR", "スライド50", ("箇所", "絵に添えた札")), paper=True)),
    ),
    # c517＝スライド57 の手書きの注記「Morning June 23 noticed in the floor area, a space or gap of 4inches」（4インチ＝10.16センチ）
    "c517": dict(
        t="床の隙間", s="目撃した人の話の図",      # dup：「…手書きの注記」は札の箇所と同じ言葉
        fig=("quote", dict(phrase="6月23日の朝、床に約10センチの隙間",
                           rows=ss.qrows("TR", "スライド57", ("箇所", "手書きの注記")), paper=True)),
    ),
}
