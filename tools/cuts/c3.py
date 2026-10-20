# -*- coding: utf-8 -*-
"""第3章　2枚の板とモード c301–c323（23カット）。17本目（中華航空140便墜落事故）。

■ 🔴 2026-10-20（⑤b-1）：23本目（三豊百貨店崩壊事故のリメイク）の中身を空にした＝git の `b800dbdb`（`git show b800dbdb:tools/cuts/c3.py`）。
■ PLAN＝この章の全カットの「画面の種類（kind）・画の予定（plan）・出典（src）」＝⑤b-1 に `ref/ep17/make_plan17.py` で
  映像方針の一覧 `ref/ep17/eizou_build/list17.tsv`（了承②ずみ・E 0・秒は narration.json の実測）と台本 第2版 §4 の出典の欄から
  機械で組んだ（手で写していない）。🔴 台本の画の欄は写していない（撮影者の名前がある＝元の画は台本 §4）。
  🔴 SPEC（図の中身）は ⑤b-2 以降で PLAN の予定どおりに書く。**種類を変えるなら PLAN の kind を直す**
     （`cuts/__init__.py` が SPEC に kind を写す＝門番 check_text_screens が「文字だけ・続く長さ」を数える）。
  ⚠️ 秒は書き写さない＝narration.json の実測で組む。🔧＝映像方針で台本の画の欄から替えたカット。
  ⚠️ 「関連」と書いたカットは事故そのものではない実物の写真（種類は写真・20% の数〈この事故の写真〉には入れない）
"""
import jiko_style as J  # noqa: F401
import cuts.ss as ss  # noqa: F401

P = ss.P

PLAN = {
    'c301': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C2 尾翼｜注：動く所が2つ｜このカットの前に章の扉｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.78・p.55'),
    'c302': dict(kind='フリー素材',
               plan='🔧 Xf1:全体｜一覧の種類：イメージ｜見せ方：全面（イメージ）｜副題：イメージ（旅客機の操縦輪）｜動き：寄る｜権利：Pexels License｜出典の行：フリー素材（Pexels）｜注：🔧｜新しい画（映像方針）：再現イラスト 場面2 → フリー素材（操縦輪を押す手）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.55・p.44'),
    'c303': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C2 尾翼｜注：水平安定板に色｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.84・p.55'),
    'c304': dict(kind='図解',
               plan='🔧 一覧の種類：図｜見た目の型：比べ（面積のマス目）｜注：🔧｜新しい画（映像方針）：再現イラスト 場面2（面積の比べ）→ 図：面積のマス目（昇降舵1：昇降舵を含めた水平安定板 約3）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.55'),
    'c305': dict(kind='写真',
               plan='R10｜一覧の種類：実写｜見せ方：全面｜副題：事故のあとの右の昇降舵｜動き：左へ｜権利：PDL1.0｜出典の行：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』写真10（加工して作成）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.142'),
    'c306': dict(kind='写真',
               plan='🔧 関連（事故そのものではない実物の写真・20% の数に入れない）｜QA｜一覧の種類：関連｜見せ方：額装（BY-SA）｜副題：同じ型 A300B4-622R の操縦室（2004年・別の機体）｜動き：額ごと寄る｜権利：GFDL 1.2｜出典の行：Wikimedia Commons（GFDL 1.2）＝作者は src/credits_private.tsv｜注：🔧｜新しい画（映像方針）：模式図 → 同じ型の操縦室の写真｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.40'),
    'c307': dict(kind='図解',
               plan='一覧の種類：図｜見た目の型：箱（3つの仕組み）｜注：自動操縦・自動推力・飛行の指示｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.44・p.51'),
    'c308': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：正面｜見た目の型：C1 FMA（全体）｜注：欄の区切りに札（推力・飛び方・指示と自動操縦）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.54・p.135'),
    'c309': dict(kind='図・写真の頁',
               plan='F29:欄｜一覧の種類：頁｜見せ方：全面（頁の切り出し）｜副題：報告書の付図29（欄の切り出し）｜動き：右へ（欄を順に）｜権利：PDL1.0｜出典の行：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』付図29（加工して作成）｜注：c106・c113 と別の切り出し｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.54・p.135'),
    'c310': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C2 尾翼｜注：押す・昇降舵だけが手の側へ｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.40・p.82'),
    'c311': dict(kind='写真',
               plan='🔧 関連（事故そのものではない実物の写真・20% の数に入れない）｜AB1｜一覧の種類：関連｜見せ方：全面｜副題：現在のエアバス社の本社（トゥールーズ）｜動き：右へ｜権利：CC0｜出典の行：Wikimedia Commons（CC0）｜注：🔧｜新しい画（映像方針）：再現イラスト 場面2 → エアバス社の写真｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.82〜83'),
    'c312': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C2 尾翼｜注：水平安定板は自動操縦の側で動き続ける｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.40・p.82'),
    'c313': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C5 相反｜注：押せば押すほど板は逆へ｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.40・p.83'),
    'c314': dict(kind='図解',
               plan='🔧 一覧の種類：図｜見た目の型：年表（前例と改修の承認）｜注：🔧 1985年と1988年3月だけ（⑤b-4：年表に「再現イラスト」の札は合わない＝軸の型・門番 check_axis）｜新しい画（映像方針）：再現イラスト 場面9 → 年表（軸の型）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.78'),
    'c315': dict(kind='写真',
               plan='E3｜一覧の種類：実写｜見せ方：額装（BY-SA）｜副題：事故機 B-1816（1991年9月・香港）｜動き：額ごと左へ｜権利：GFDL 1.2｜出典の行：Wikimedia Commons「China Airlines B-1816 Airbus A300 at HK Airport.jpg」（GFDL 1.2）＝作者は src/credits_private.tsv｜注：GFDL｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.78・p.79・p.40'),
    'c316': dict(kind='再現イラスト',
               plan='🔧 一覧の種類：案C｜見る向き：正面｜見た目の型：C1 FMA（帯）｜注：🔧 ★｜新しい画（映像方針）：quote → 再現イラスト 場面1（GO AROUND に「改修の対象外」の印）｜★決め所だった行（決め所の画面は作らない＝10-07）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.78'),
    'c317': dict(kind='図解',
               plan='🔧 一覧の種類：図｜見る向き：横から｜見た目の型：模式（高さの帯）｜注：🔧｜新しい画（映像方針）：再現イラスト 場面1 → 模式図：横から見た高さの帯（約120メートル以下のランドと、やり直しの上昇に「対象外」）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.78'),
    'c318': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C5 相反｜注：「2つの異なる意図」の札｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.78'),
    'c319': dict(kind='写真',
               plan='R09｜一覧の種類：実写｜見せ方：全面｜副題：事故のあとの左の昇降舵と調べる人｜動き：寄る｜権利：PDL1.0｜出典の行：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』写真9（加工して作成）｜注：調べる人は公的な任務（顔は小さい）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.78'),
    'c320': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：正面｜見た目の型：C1 FMA（帯）｜注：ランドのボタンでは消えない｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.54'),
    'c321': dict(kind='図解',
               plan='🔧 一覧の種類：図｜見た目の型：流れ（抜け方）｜注：🔧｜新しい画（映像方針）：再現イラスト 場面1 → 流れ図（縦だけ選び直す → 文字は消える・働きは残る／縦と横 → 抜ける）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.54・p.81'),
    'c322': dict(kind='図解',
               plan='一覧の種類：図｜見た目の型：書類（手引き書）｜注：「あたかも」｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.81・p.82・p.103'),
    'c323': dict(kind='フリー素材',
               plan='🔧 Xb4｜映像の素材 8.34秒・倍率 1.12（素材の秒÷扉を除いた中身の秒＝narration.json の実測・1.0 以上は等速で区間を選ぶ）｜一覧の種類：イメージ｜見せ方：全面（イメージ）｜副題：イメージ（夜、進入する旅客機）｜動き：映像｜権利：Pexels License｜出典の行：フリー素材（Pexels）｜注：🔧 c215 と別の映像｜新しい画（映像方針）：再現イラスト 場面1 → フリー素材｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.81'),
}

SPEC = {}

# ── 🆕 ⑤b-3（2026-10-20）：再現イラスト C1（画面の上の端）・C2（尾翼）＝`tools/illu17.py`・門番 check_illu ㉛㉜ ──
from illu17 import C1_REC as R1, C2_REC as R2  # noqa: E402  置き場の部品の出典（描く側と同じ文）

SPEC.update({
    # c301（2行・章の頭）＝尾翼を横から（しくみの説明＝角度は模式）。2行目で2つの動く所に輪（1＝昇降舵〈c302 で名を言う〉・2＝水平安定板〈c303〉）
    "c301": dict(fig=("illu", dict(
        place="C2", start=dict(c2kind="model", switch="on"), rec=R2["body"],
        steps=[dict(tag=dict(t="尾翼の水平の翼", at="elev", off=(-260, -300), anchor="middle")),
               dict(state=dict(c2hl="both"),
                    tag=[dict(t="動く所 1", at="elev", off=(150, -170), anchor="middle"),
                         dict(t="動く所 2", at="ths", off=(-430, -230), anchor="middle")])]))),
    # c303（2行）＝水平安定板に色（輪）・少しずつ角度を変える（模式の 0度→−4度）→ 2行目「トリム」
    "c303": dict(fig=("illu", dict(
        place="C2", start=dict(c2kind="model"), rec=R2["body"],
        steps=[dict(state=dict(c2hl="ths", c2ths=-4.0), rec=R2["ths"], dur=3.2,
                    tag=[dict(t="水平安定板", at="ths", off=(-430, -230), anchor="middle", keep=True),
                         dict(t="昇降舵", at="elev", off=(150, -170), anchor="middle", keep=True)]),
               dict(tag=dict(t="トリム＝釣り合い", at="le", off=(-260, 170), anchor="middle"))]))),
    # c308（2行）＝画面ぜんたい（しくみの説明＝付図29 の 14'00" の枠を例に）。2行目で上の端の欄の区切りに3つの札
    "c308": dict(fig=("illu", dict(
        place="C1", start=dict(view="all", c1f="1400"), rec=R1["f29"],
        steps=[dict(),
               dict(tag=[dict(t="推力", at="col_thr", off=(0, -78), anchor="middle", keep=True),
                         dict(t="飛び方", at="col_fly", off=(0, -78), anchor="middle", keep=True),
                         dict(t="指示と自動操縦", at="col_fd", off=(-130, -78), anchor="middle", keep=True)])]))),
    # c310（3行）＝しくみの説明（模式）：自動操縦が入っていても、昇降舵は手の力で（橙）・水平安定板は自動操縦（水色）。
    #   前の全面の絵 c308（C1 画面）から置き場が替わる＝切り替えの字
    "c310": dict(fig=("illu", dict(
        place="C2", start=dict(c2kind="model", switch="on"), rec=R2["body"],
        steps=[dict(),
               dict(state=dict(c2ap="on", c2hand="on", c2arrow="hand", c2elev=7.0), rec=R2["hand"], dur=1.4,
                    tag=[dict(t="手の力（押す）", at="te", off=(-40, 210), anchor="middle", keep=True),
                         dict(t="自動操縦", at="ths", off=(-430, -230), anchor="middle", keep=True)]),
               dict(state=dict(c2hl="elev"), tag=dict(t="オーバーライド", at="elev", off=(150, -170), anchor="middle"))]))),
    # c312（2行）＝しくみの説明（模式）：効くのは昇降舵だけ → 水平安定板は自動操縦のとおりに動き続ける（0度→−6度・ゆっくり）
    "c312": dict(fig=("illu", dict(
        place="C2", start=dict(c2kind="model", c2ap="on", c2hand="on", c2elev=7.0), rec=R2["ap"],
        steps=[dict(state=dict(c2hl="elev"), tag=dict(t="手で動くのは昇降舵", at="elev", off=(40, -190), anchor="middle")),
               dict(state=dict(c2hl="ths", c2ths=-6.0), rec=R2["ap"], dur=3.4,
                    tag=dict(t="自動操縦のとおり", at="ths", off=(-430, -230), anchor="middle"))]))),
    # c316（2行・★だった行）＝上の端の寄り（付図29 の 14'06" の枠を例に）。GO AROUND に「改修の対象外」（報告書 p78＝MOD.7187）
    "c316": dict(fig=("illu", dict(
        place="C1", start=dict(view="band", c1f="1406", switch="on"), rec=R1["f29"],
        steps=[dict(),
               dict(state=dict(c1ring="ga"), rec="報告書 p78（LANDTrack及びGOAROUNDモード以外のモードでは…APがディスエンゲージされる）",
                    tag=dict(t="改修の対象外", at="ga", off=(0, -96), anchor="middle"))]))),
    # c320（3行）＝上の端の寄り＋LAND のボタン。2行目で押す → GO AROUND は消えない（×）
    "c320": dict(fig=("illu", dict(
        place="C1", start=dict(view="band", c1f="1406", switch="on"), rec=R1["f29"],
        steps=[dict(state=dict(c1land="on"), rec=R1["land"], tag=dict(t="LAND のボタン", at="land", off=(70, 6))),
               dict(state=dict(c1land="press", c1ring="ga"), rec=R1["land"]),
               dict()]))),
})

# ── 🆕 ⑤b-4（2026-10-20）：再現イラスト C5 相反の図（`tools/illu17.py`・門番 check_illu ㉟）・年表 c314（軸の型＝門番 check_axis）──
from illu17 import C5_REC as R5  # noqa: E402  置き場 C5 の部品の出典（描く側と同じ文）

SPEC.update({
    # c313（2行・しくみ＝模式）＝自動操縦は水平安定板で釣り合いを取り直す（水色）→ 2行目で人が押し続ける（橙）と、板は機首上げへ動いていく。
    #   前の全面の絵 c312（C2 尾翼）から置き場が替わる＝切り替えの字
    "c313": dict(fig=("illu", dict(
        place="C5", start=dict(c5kind="model", c5ths=-3.0, c5elev=0.0, c5ap="on", switch="on"), rec=R5["ap"],
        steps=[dict(tag=dict(t="自動操縦：板で釣り合いを取る", at="ths", off=(-60, -190), anchor="middle")),
               dict(state=dict(c5hand="on", c5ths=-9.0, c5elev=7.0), rec=R5["hand"], dur=2.4,
                    tag=[dict(t="押す（機首下げ）", at="hand_dn", off=(110, 40), anchor="start"),
                         dict(t="板は逆へ（機首上げ）", at="le", off=(-30, 160), anchor="middle")])]))),
    # c318（3行・しくみ）＝報告書の言葉「2つの異なる意図が同時に入力されるシステム」（p78）→ 2行目で知らせる警報の装置が無い（×）
    "c318": dict(fig=("illu", dict(
        place="C5", start=dict(c5kind="model", c5ths=-9.0, c5elev=7.0, c5ap="on", c5hand="on", switch="on"), rec=R5["ap"],
        # ⚠️ 門番 echo：札「2つの異なる意図が同時に」は語りの複写＝中身を言い換えた（人は機首下げ・機械は機首上げ）
        steps=[dict(rec="報告書 p78（APがTHSを、操縦士がエレベータをそれぞれ制御できようになっており、2つの異なる意図が同時に入力される）",
                    tag=dict(t="人は機首下げ・機械は機首上げ", xy=(960, 680), anchor="middle", keep=True)),
               dict(state=dict(c5warn="on"), rec=R5["warn"], tag=dict(t="知らせる警報は無かった", at="spk", off=(-40, 70), anchor="end")),
               dict()]))),
    # c314（2行）＝年表（軸の型）。1行目「1985年に起きた出来事のあと」→ 2行目「1988年3月、フランスの航空の当局が…改修を承認」（p78）
    "c314": dict(
        t="前にも現れていた危険", s="1985年の出来事と1988年の承認",
        fig=("axis", dict(ss.AX_Y17, steps=[dict(add=[ss.ax("i85")], cur="1985-03-01"),
                                            dict(add=[ss.ax("mod88")], cur="1988-03")],
                          note="年月は報告書の本文（1988年3月18日＝承認の日・月まで）", src=ss.src(["報告書 p78"])))),
})

# ── 🆕 ⑤b-5（2026-10-20）：図解（`tools/mech17.py`・門番 check_mech の judge_m17＝記録 REC_M17）──
SPEC.update({
    # c304（3行）＝面積のマス目（p55＝昇降舵を含めた水平安定板は昇降舵の約3倍）→ 2行目で同じ角度の板と効きの矢印（模式）→ 3行目は保つ
    "c304": dict(
        t="板の広さ", s="報告書の値でマス目に",
        fig=("m17", dict(view="area", steps=[dict(state=dict(elev="on", ths="on")), dict(state=dict(same="on")), dict()],
                         rel=[dict(t="約3倍", src="報告書 p55")],
                         note="マス目の数の比＝面積の比・板の形と傾きと効きの矢印は模式", src=ss.src(["報告書 p55"])))),
    # c307（2行）＝自動飛行システムの3つの箱。1行目で見出し・自動操縦・自動推力 → 2行目で飛行の指示
    "c307": dict(
        t="3つの仕組み", s="自動で飛ぶための装置の中身",
        fig=("m17", dict(view="afs", steps=[dict(state=dict(head="on", ap="on", at="on")), dict(state=dict(fd="on"))],
                         note="箱の中の絵は模式", src=ss.src(["報告書 p51", "報告書 p95"])))),
    # c317（2行）＝横から見た進入の道（傾きは誇張）。1行目で対地 約120m（400ft）以下のランド＝対象外 → 2行目でゴー・アラウンド＝対象外（p78 MOD.7187）
    "c317": dict(
        t="押しても切れない場面", s="改修の対象から外れた2つ",
        fig=("m17", dict(view="band", steps=[dict(state=dict(land="on")), dict(state=dict(ga="on"))],
                         rel=[dict(t="約120m（400ft）", src="報告書 p78")],
                         note="傾きと高さは模式（約120mの線だけ記録の値）", src=ss.src(["報告書 p78"])))),
    # c321（3行）＝ゴー・アラウンドの抜け方（p54・p81）。1行目で縦と横の両方＝抜ける → 2行目で縦だけ＝表示の字は消える → 3行目で働きは残る
    "c321": dict(
        t="抜けるための手順", s="報告書の説明",
        fig=("m17", dict(view="modes", steps=[dict(state=dict(a="on")), dict(state=dict(b="on")), dict(state=dict(b2="on"))],
                         note="手順の流れ（模式）", src=ss.src(["報告書 p54", "報告書 p81"])))),
    # c322（3行）＝表示（FMA＝V/S と HDG）と手引き書（FCOM）。1行目で表示と「あたかも」→ 2行目で書かれていない所 → 3行目で勧告（p103 の 2c）
    "c322": dict(
        t="手引き書に無かったこと", s="表示と中の働きのずれ",
        fig=("m17", dict(view="fcom", steps=[dict(state=dict(fma="on")), dict(state=dict(gap="on")), dict(state=dict(rec="on"))],
                         note="手引き書の欄の言葉は報告書の要約・頁の形は模式", src=ss.src(["報告書 p81", "報告書 p82", "報告書 p103"])))),
})
