# -*- coding: utf-8 -*-
"""第4章　20時14分5秒のレバー c401–c420（20カット）。17本目（中華航空140便墜落事故）。

■ 🔴 2026-10-20（⑤b-1）：23本目（三豊百貨店崩壊事故のリメイク）の中身を空にした＝git の `b800dbdb`（`git show b800dbdb:tools/cuts/c4.py`）。
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
    'c401': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C4 断面（寄り）｜注：20:14:05・約330メートル｜このカットの前に章の扉｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.5・p.44'),
    'c402': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：正面｜見た目の型：C3 手｜注：右の席の手がスラスト・レバーに（人は影の手だけ）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.51'),
    'c403': dict(kind='写真',
               plan='R37:全体｜一覧の種類：実写｜見せ方：全面｜副題：事故のあとのスラスト・レバーとゴー・レバー｜動き：寄る｜権利：PDL1.0｜出典の行：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』写真37（加工して作成）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.51・p.59'),
    'c404': dict(kind='図・写真の頁',
               plan='P51:全体｜一覧の種類：頁｜見せ方：額装（頁）｜副題：報告書の写真51（レバーの位置関係）｜動き：下へ｜権利：PDL1.0｜出典の行：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』写真51（加工して作成）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.51・p.163'),
    'c405': dict(kind='写真',
               plan='🔧 R37:ゴー・レバー｜一覧の種類：実写｜見せ方：全面｜副題：ゴー・レバーの寄り｜動き：2点（握り → ゴー・レバー）｜権利：PDL1.0｜出典の行：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』写真37（加工して作成）｜注：🔧 ★｜新しい画（映像方針）：quote → 写真37 の寄り｜★決め所だった行（決め所の画面は作らない＝10-07）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.95'),
    'c406': dict(kind='図・写真の頁',
               plan='L64｜一覧の種類：頁｜見せ方：額装（頁）｜副題：アメリカ連邦航空局の報告の図4（1996年）｜動き：右へ｜権利：PD（米連邦政府）｜出典の行：FAA Human Factors Team (1996) Figure 4｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='L1 PDF p.64・p.60'),
    'c407': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：正面｜見た目の型：C1 FMA（全体）｜注：20:14:06 THR・GO AROUND へ｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.51・p.5・p.135'),
    'c408': dict(kind='写真',
               plan='R35:全体｜一覧の種類：実写｜見せ方：全面｜副題：事故のあとのセンタ・ペデスタル｜動き：左へ｜権利：PDL1.0｜出典の行：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』写真35（加工して作成）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.51'),
    'c409': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C4 断面（寄り）｜注：下り道より上へそれる｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.44'),
    'c410': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：正面｜見た目の型：C3 手｜注：20:14:10 の札だけ・言葉の札は出さない｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.44'),
    'c411': dict(kind='写真',
               plan='🔧 R44:寄り｜一覧の種類：実写｜見せ方：全面｜副題：事故機の音声記録装置（寄り）｜動き：寄る｜権利：PDL1.0｜出典の行：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』写真44（加工して作成）｜注：🔧 c410 と同じ絵を続けない｜新しい画（映像方針）：再現イラスト 場面3 → 写真44 の寄り｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.44'),
    'c412': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C4 断面（寄り）｜注：約320メートル・約15秒・約5.5キロ｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.5'),
    'c413': dict(kind='写真',
               plan='🔧 関連（事故そのものではない実物の写真・20% の数に入れない）｜QB｜一覧の種類：関連｜見せ方：額装（BY-SA）｜副題：同じ系列 A300-600R の操縦室の中央（2003年・別の機体）｜動き：額ごと左へ｜権利：GFDL 1.2｜出典の行：Wikimedia Commons（GFDL 1.2）＝作者は src/credits_private.tsv｜注：🔧 付図4 の頁の4回使いを減らす｜新しい画（映像方針）：付図4 → 同じ型の操縦室の写真｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.44・p.51〜52'),
    'c414': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：正面｜見た目の型：C1 FMA（時刻）｜注：視線の矢印だけ・人は描かない｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.52'),
    'c415': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：横から｜見た目の型：C4 断面（寄り）｜注：下り道の点線へ戻そうと押すが、機体は水平のまま（操縦輪のフリー素材は A320 系や人が主役で合わなかった＝10-19）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.44・p.54・p.57'),
    'c416': dict(kind='図・写真の頁',
               plan='🔧 P51:ボタン｜一覧の種類：頁｜見せ方：全面（頁の切り出し）｜副題：報告書の写真51（ゴー・レバーと自動推力を切るボタン）｜動き：寄る｜権利：PDL1.0｜出典の行：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』写真51（加工して作成）｜注：🔧 ★｜新しい画（映像方針）：quote → 写真51 の頁の切り出し｜★決め所だった行（決め所の画面は作らない＝10-07）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.51'),
    'c417': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：正面｜見た目の型：C3 手｜注：2つの見方の札｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.51'),
    'c418': dict(kind='写真',
               plan='🔧 関連（事故そのものではない実物の写真・20% の数に入れない）｜B192｜一覧の種類：関連｜見せ方：全面｜副題：中華航空の A300 B-192（1998年2月・香港）｜動き：右へ｜権利：CC BY 2.0｜出典の行：Wikimedia Commons「HONG KONG KAI TAK FEB 1998 CHINA AIRLINES AIRBUS A300 B-192 (8673301706).jpg」（CC BY 2.0）＝作者は src/credits_private.tsv｜注：🔧 写真37 の3回使いを減らす｜新しい画（映像方針）：写真37（寄り）→ 中華航空の同じ時代の A300｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.101'),
    'c419': dict(kind='再現イラスト',
               plan='一覧の種類：案C｜見る向き：正面｜見た目の型：C1 FMA（帯）｜注：GO AROUND のまま｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.45・p.53'),
    'c420': dict(kind='図解',
               plan='🔧 一覧の種類：図｜見た目の型：帯（13秒・6秒）｜注：🔧｜新しい画（映像方針）：再現イラスト 場面4 → 時間の帯（20:14:05 → 20:14:12 → 20:14:18）｜台本の画＝台本 §4（撮影者の名前があるので写さない）',
               src='S1 p.5'),
}

SPEC = {}

# ── 🆕 ⑤b-3（2026-10-20）：再現イラスト C1（画面の上の端）・C3（操縦室の手）＝`tools/illu17.py`・門番 check_illu ㉛㉝ ──
from illu17 import C1_REC as R1, C3_REC as R3  # noqa: E402  置き場の部品の出典（描く側と同じ文）

SPEC.update({
    # c402（2行・20:14:05 の直前）＝操縦室の中。副操縦士（右の席）の手がスラスト・レバーに（影の手だけ）→ 2行目でレバー2本に輪
    "c402": dict(fig=("illu", dict(
        place="C3", at="20:14:05", start=dict(switch="on"),
        steps=[dict(state=dict(c3thr="on"), rec=R3["hand_thr"], dur=1.3,
                    tag=dict(t="副操縦士の手", at="hand_thr", off=(170, -150))),
               dict(state=dict(c3ring="lev"), rec=R3["lever"],
                    tag=dict(t="スラスト・レバー", at="lev", off=(-230, -120), anchor="end"))]))),
    # c407（2行・20:14:06）＝画面ぜんたい。14'00" の枠 → 2行目で 14'06"（THR・GO AROUND・ALT〈青〉・FD1）＋ GO AROUND に輪
    "c407": dict(fig=("illu", dict(
        place="C1", at="20:14:06", start=dict(view="all", c1f="1400"), rec=R1["f29"],
        steps=[dict(),
               dict(state=dict(c1f="1406", c1ring="ga"), rec=R1["f29"],
                    tag=dict(t="着陸のやり直し", at="ga", off=(0, -80), anchor="middle"))]))),
    # c410（2行・20:14:10）＝操縦室の中・時刻の札だけ（CVR の言葉は札にしない＝語りと字幕だけ）。2行目でゴー・レバーに輪
    "c410": dict(fig=("illu", dict(
        place="C3", at="20:14:10", start=dict(c3thr="on", switch="on"), rec=R3["hand_thr"],
        steps=[dict(tag=dict(t="20:14:10", xy=(660, 140), anchor="middle")),
               dict(state=dict(c3ring="go"), rec=R3["lever"],
                    tag=dict(t="ゴー・レバー", at="go", off=(-250, -90), anchor="end"))]))),
    # c414（2行・20:14:12）＝上の端と時刻の帯。目の印（見た向き・人は描かない）＝機長は表示を見て言った（p52）
    "c414": dict(fig=("illu", dict(
        place="C1", at="20:14:12", start=dict(view="time", c1f="1412", c1cur="20:14:12", switch="on"), rec=R1["cur"],
        steps=[dict(state=dict(c1eye="on"), rec=R1["eye"]),
               dict(state=dict(c1ring="ga"))]))),
    # c417（3行・20:14:05）＝操縦室の中。2つの見方の札（ボタンの取り違え／スラスト・レバーの操作中）→ 3行目でゴー・レバーに輪
    "c417": dict(fig=("illu", dict(
        place="C3", at="20:14:05", start=dict(c3thr="on", switch="on"), rec=R3["hand_thr"],
        steps=[dict(state=dict(c3ring="at"), rec=R3["at"],
                    tag=dict(t="ボタンの取り違え", at="at", off=(-170, -150), anchor="end", keep=True)),
               dict(state=dict(c3ring="lev"), rec=R3["lever"],
                    tag=dict(t="スラスト・レバーの操作中", at="lev_r", off=(330, -170), anchor="start", keep=True)),
               dict(state=dict(c3ring="go"), rec=R3["lever"])]))),
    # c419（3行・20:14:12 のあと）＝上の端の寄り。GO AROUND のまま（14'12" の枠）
    "c419": dict(fig=("illu", dict(
        place="C1", at="20:14:12", start=dict(view="band", c1f="1412", switch="on"), rec=R1["f29"],
        steps=[dict(),
               dict(state=dict(c1ring="ga"), tag=dict(t="GO AROUND のまま", at="ga", off=(0, -96), anchor="middle")),
               dict()]))),
})

# ── 🆕 ⑤b-4（2026-10-20）：再現イラスト C4 進入の断面図（`tools/illu17.py`・門番 check_illu ㉞）──
from illu17 import C4_REC as R4  # noqa: E402  置き場 C4 の部品の出典（描く側と同じ文）

SPEC.update({
    # c401（2行・20:14:05）＝寄り。ゴー・レバーの点（約330メートル＝1,070フィート・p5）→ 2行目で下り道に沿って手で下りていた
    "c401": dict(fig=("illu", dict(
        place="C4", at="20:14:05", start=dict(view="near", c4t="20:14:05", c4gs="on", c4ring="on"),
        rec="報告書 p5（11時14分05秒、気圧高度約1,070ftを通過中）",
        steps=[dict(tag=dict(t="20:14:05・約330m", at="pt", off=(0, -90), anchor="middle", keep=True)),
               # ⚠️ 試し焼き 39377897273：右へ伸ばすと右下がりの下り道の点線が札をかすめた＝点線の下で左へ（右寄せ）
               dict(tag=dict(t="下り道に沿って", at="gs", off=(-30, 100), anchor="end"))]))),
    # c409（2行・20:14:05→10）＝寄り。推力が増えて、下り道より上へそれ始めた（p44）。前の全面の絵 c407（C1）から置き場が替わる＝切り替えの字
    "c409": dict(fig=("illu", dict(
        place="C4", at="20:14:10", start=dict(view="near", c4t="20:14:05", c4gs="on", switch="on"), rec=R4["mk"],
        steps=[dict(state=dict(c4t="20:14:10"), rec=R4["dev"], dur=2.0,
                    tag=dict(t="下り道より上へ", at="gs", off=(-30, 100), anchor="end")),
               dict()]))),
    # c412（3行）＝寄り。滑走路から約5.5km（p5）→ 2行目で約320メートル・約15秒の水平飛行（p44・p5）。前の全面の絵 c410（C3）から＝切り替えの字
    "c412": dict(fig=("illu", dict(
        place="C4", at="20:14:25", start=dict(view="near", c4t="20:14:05", c4gs="on", switch="on"), rec=R4["mk"],
        steps=[dict(state=dict(c4dist="on"), rec=R4["dist5"],
                    tag=dict(t="滑走路から約5.5km", at="dist", off=(0, -60), anchor="middle")),
               dict(state=dict(c4dist="off", c4t="20:14:25", c4hl="flat"), rec=R4["flat"], dur=2.4,
                    tag=dict(t="約320m・約15秒", at="flat", off=(0, -90), anchor="middle")),
               dict()]))),
    # c415（3行・20:14:10→18）＝寄り。下り道に戻ろうと押す（橙の矢印・p44）→ 2行目で機体は水平のまま。前の全面の絵 c414（C1）から＝切り替えの字
    "c415": dict(fig=("illu", dict(
        place="C4", at="20:14:18", start=dict(view="near", c4t="20:14:10", c4gs="on", switch="on"), rec=R4["mk"],
        steps=[dict(state=dict(c4arrow="push"), rec=R4["push"], tag=dict(t="押す", at="push", off=(60, -10), anchor="start")),
               dict(state=dict(c4t="20:14:18"), rec=R4["push"], dur=1.8,
                    tag=dict(t="水平のまま", at="pt", off=(40, -90), anchor="start")),
               dict()]))),
})

# ── 🆕 ⑤b-5（2026-10-20）：時刻の帯（軸の型＝門番 check_axis の REC_AXIS・REC_ROLE）──
SPEC.update({
    # c420（2行）＝20:14:05 ゴー・レバー → 20:14:12 機長の指示（CVR の言葉は札にしない）→ 20:14:18 自動操縦が入る（括弧2つ＝13秒・6秒は語りと字幕）
    #   → 2行目で「ゴー・アラウンドのまま」の項目の札
    "c420": dict(
        t="自動操縦が入った時刻", s="ゴー・レバーからの秒",
        fig=("axis", dict(ss.AX_S17, steps=[dict(add=[ss.ax("go05"), ss.ax("or12"), ss.ax("ap18"), ss.ax("br13"), ss.ax("br06")], cur="20:14:18"),
                                            dict(add=[dict(k="chips", at="20:14:18", chips=["表示はゴー・アラウンドのまま"], rec="報告書 p44")])],
                          note="時刻は報告書の本文（協定世界時＋9時間）", src=ss.src(["報告書 p44"])))),
})
