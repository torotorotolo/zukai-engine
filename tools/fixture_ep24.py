# -*- coding: utf-8 -*-
"""24本目（チェルノブイリ原発事故・1986-04-26・ソ連〈いまのウクライナ〉チェルノブイリ原子力発電所4号炉・INSAG-7〈IAEA 1992年〉ほかの報告の動画）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-10-25（25本目 JR福知山線脱線事故の ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `7ae693a1` と同じ）
  ・`cuts/ss.py` の24本目の値＝案C の出典の表（REC_DOCS＝S1 INSAG-7・S2 INSAG-1・S3 ソ連の報告・L2 UNSCEAR 2000 付属書J・L1 チェルノブイリ・フォーラムの5資料）・
    原文の道（REC_PAGES＝`ref/ep24/src/ep24_pages.txt`＝手元にある〈git の外〉）・割れる時刻（ILLU_SPLIT_TIMES＝1:00・1:03）・群れを描いてよい時刻の上限（ILLU_CROWD_UNTIL＝17:00）・
    置いてよい役割（ILLU_ROLES＝住民 residents の顔の無い群れだけ）・札に出してよい時計の時刻（ILLU_CLOCK_OK 8）・
    「この回は衛星写真の地図なし」の言い分（SAT_NONE＝地図2つ〈c203・c713〉は Natural Earth の国の形で描いた）・
    写真の束の定数（台紙の縁でない暗い帯の名簿 SLIDE_NOT_MOUNT＝10点）。
    24本目も空のままだった表（ILLU_SEC_OK・ILLU_COUNTS・ILLU_ASSUME・ILLU_DESTROY_CUTS・ILLU_TOP_NOSCALE・ILLU_SUB_*・ILLU_BOOM_CUTS・ILLU_MIX_TODO・
    AXIS_DOCS・AXI・QG・QB・PEOPLE_*・QDOC・QWHO・SAT・GEO・NEEDS_MASK・SLIDE_MOUNT・OCR_NOT_TEXT）も、24本目の状態として持つ（17本目・23本目の見本と同じ考え方）
  ・門番の記録の表（check_mech＝REC_M24〈図解 `mech24.py` の記録の値＝第1〜11章の図解119のうち m24 のカット〉／
    check_illu＝REC_N1〜REC_N4〈置き場 N1 炉の断面・N2 止める棒・N3 出力の時刻表・N4 避難のバス＝`illu24.py` の記録の値・㊳〜㊶〉）。
    check_axis・check_qty・check_boxes・check_sat・check_photo_edge・check_photo_mask は24本目で足した表が無い（24本目は年表の型・棒・箱の型を使わなかった＝
    REC_AXIS ほかは空のまま。check_sat の言い分は ss の SAT_NONE、check_photo_edge の名簿は ss の SLIDE_*＝上）＝この見本の GATES に載せない
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を24本目の実物でも確かめている（check_illu の ㊳〜㊶・check_mech の m24）＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は25本目の空の器にした
  （fixture_ep14〜ep23・ep17 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep24
      fixture_ep24.apply(sys.modules[__name__])   # その処理の中だけ ss・この門番の記録の表が24本目になる
      try: …（検算）
      finally: fixture_ep24.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14〜23本目・17本目の見本と重ねるとき（check_mech）は
      fixture_ep24.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと25本目の画に24本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。⚠️ ほかの回の見本（fixture_ep17 ほか）の積み荷とは別＝それぞれの restore で戻す
■ 注意:
  ⚠️ 見本の原文 `ref/ep24/src/ep24_pages.txt`（check_illu の `_pages()`・cuts/ss.REC_DOCS の通し頁）と `ref/ep24/src/*.pages.tsv`（check_mech の `_m24_page`）は
     **手元にだけある**（git の外）。Actions には無い＝check_illu の `_pages()` は None を返し、check_mech の `_m24_page` は句の照合を飛ばす。
  ⚠️ 24本目の selftest のうち、**章ファイルの SPEC を読むもの**は 2 つ：check_illu の `selftest_ep24`（置き場 N1〜N4 の正しい場面 c208・c303・c403・c615・c707・c905）・
     check_mech の `_selftest_m24`（m24 のカット＝図解）。どちらも `apply(gate)`（check_mech だけ `apply(gate, tables_only=True)`）＋`apply_cuts()`（24本目の章ファイルを
     git の `CUTS_SHA`＝`7ae693a1` から取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ24本目に入れ替える・git が無い所では止める＝fail closed）を使う（`restore()` で25本目へ戻る・LIFO）。
  ⚠️ 24本目の章ファイルは git の版の `tools/cuts/ss.py`（EP＝`ep24/`・24本目の値）ごと取り出して読む＝写真の名 `P("…")` は `ep24/…` のまま（本番の ss の EP は ep25）。
     ただし `ss.vid`・`ss.head`・`ss.tailv` は本番の **`footage.CLIPS`・`footage.USE`**（と `footage.PILLAR`）を引く（フリー素材8カット c101・c107・c621・c927・ca15・cb22・cb23・cc20＝
     台帳の `"stock": true` を見て、ひかえの静止画の名を `ep24/stock/fb_<cid>.jpg` に決める）＝本番の footage は25本目の表（`USE`・`PILLAR` は空・`CLIPS` は `ref/ep25/clips.json`＝無ければ空）
     なので、`cuts_ep24()` は章ファイルを読む間だけ footage の3つを24本目の表（台帳 `ref/ep24/clips.json`・使う区間 `USE` と黒帯の割合 `PILLAR` は git の `7ae693a1` の `tools/footage.py` の
     `USE = {…}`・`PILLAR = {…}` の2文を取り出して評価＝24本目の PILLAR は空〈Pexels は器も中身も 1920×1080〉）に差し、読み終えたら戻す（`_footage24`＝17本目の `_footage17` と同じ）。
     24本目の footage の値は**ここに写していない**（git の `7ae693a1` が正本）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep24/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は24本目の道を持つ。
  ⚠️ `SLIDE_NOT_MOUNT` の鍵は **`ep24/` の名を文字で書いた**（本番の ss は `P(…)` で組んでいた＝EP が ep25 になると `ep25/…`〈無い名〉に化ける。
     fixture_ep17・ep22・ep23 と同じ扱い）。説明の文は1字も変えていない（値＝git の `7ae693a1` の ss を評価した結果と同じ）。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝24本目は 1.08）は見本に入れない（16〜23本目・17本目の見本も入れていない）＝本番の ss は今の値のまま残し、25本目の束で取り直す。
  ⚠️ 写真の束の定数のうち `TRIM`（`pages.json` から読む＝REF が替われば追う）・`PRIVATE_OUT` は24本目も空のまま＝見本に入れない。
  ⚠️ 型として本番に残した＝ss の関数（`sat`・`ax`・`qb`・`P`・`page`・`vid`・`head`・`tailv`・`mv`・`mvz`・`tcam`・`check_frame_only`・`check_card_mix`・`src`）・`SAT_CREDIT`・
     check_mech の `_M24_TSV`・`_M24_PAGES`・`_m24_page`・`judge_m24`（⚠️ `_m24_page` は原文の道〈`ref/ep24/src/…`〉を直書きしている＝17本目の `_m17_page` と同じ例外）・
     check_illu の `N24_PLACES`・`N24_MARK`・`N24_BAD_IDS`・`N3_STEM_MIN`・`NUMTOK24`・`_col24`・`_min24`・`_toks24`・`judge_n24`（表が空なら理由を出して止める入口を足した）・
     描く側の型 `tools/illu24.py`・`tools/mech24.py`・`ref/ep24/make_map24.py`（どれも cuts.ss の24本目の値を読まない）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep24"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から（git の `7ae693a1` の ss.py の代入文をそのまま写した・`P("…")` だけ `"ep24/….jpg"` の文字に）
# ══════════════════════════════════════════════════════
SAT_CREDIT = "地図：Google マップの衛星写真（帰属は地図の右下）"   # 型の定数（本番の ss に残した・SAT を組むための名＝SS_NAMES に入れない）

NEEDS_MASK: dict[str, str] = {}
SLIDE_MOUNT: dict[str, str] = {}
SLIDE_NOT_MOUNT: dict[str, str] = {
    "ep24/cr3b.jpg": "右 2.2%＝3号機の制御室の右の暗がりと椅子（写真の中身・BY-SA＝額装）",
    "ep24/i18.jpg": "下 1.4%＝ヘリの乗員の黒い服と草の陰（写真の中身・BY-SA＝額装）",
    "ep24/i24.jpg": "下 3.1%＝壊れた4号機の手前の壁の下の陰（写真の中身・BY-SA＝額装）",
    "ep24/i25.jpg": "右 4.8%＝標識の右の森の暗がり（写真の中身・BY-SA＝額装）",
    "ep24/i36.jpg": "下 4.9%＝発電所の手前の森（写真の中身・BY-SA＝額装）",
    "ep24/i40.jpg": "右・下 5.0%＝溶接の暗い作業場（写真の中身・BY-SA＝額装）",
    "ep24/i45.jpg": "下 5.0%＝視察の一行の黒い背広（写真の中身・BY-SA＝額装）",
    "ep24/i56.jpg": "上 5.0%＝記者会見の会場の暗い天井（写真の中身・BY-SA＝額装）",
    "ep24/igb.jpg": "下 5.0%＝夕暮れのイグナリナ原発の前の暗い舗装（写真の中身・CC0）",
    # 🆕 ⑤b-7（10-23）：頁＝c619 の切り口（y 0.743〜0.912）の外の帯＝画面に出ない（引用＝額装）
    "ep24/s1p65.jpg": "上 4.3%＝INSAG-7 p.65 の頁の上の端の暗い帯（c619 の切り口 y 0.743〜0.912 の外・額装）",
}
OCR_NOT_TEXT: dict[str, list] = {}
SAT = {}
GEO = {}
SAT_NONE = "24本目：地図2つ（c203・c713）は Natural Earth の国の形で描く（mech24 の ussr・japan）＝衛星写真の地図は使わない"
REC_PAGES = REF / "src" / "ep24_pages.txt"      # 部品の出典（`rec=`）を当てる原文（git の外＝手元だけ）
REC_DOCS = {                                # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
    "S1": dict(range=(1, 148), name="INSAG-7（IAEA・1992年）", page="print", base=10),
    "S2": dict(range=(1001, 1147), name="INSAG-1（IAEA・1986年）", page="pdf", base=1000),
    "S3": dict(range=(2001, 2060), name="ソ連の報告（1986年8月）", page="print", base=2004),
    "L2": dict(range=(3001, 3117), name="UNSCEAR 2000年報告 付属書J", page="print", base=2552),
    "L1": dict(range=(4001, 4055), name="チェルノブイリ・フォーラム（2006年）", page="print", base=3998),
}
ILLU_SPLIT_TIMES = ("1:00", "1:03")
ILLU_CROWD_UNTIL = "17:00"                  # 群れ（プリピャチの住民）を描いてよい場面の時刻の上限＝L2 p.24「the evacuation began at 14:00 and finished at 17:00」
ILLU_ROLES = dict(sprite=(), crowd=("residents",))   # 置いてよい役割（門番 check_illu ②）＝24本目は住民の顔の無い群れだけ（案C4＝台本 §1-4）・型紙の影0
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）＝24本目の案C は秒の札を出さない
ILLU_CLOCK_OK = ("1:06", "3:47", "7:10", "14:00", "23:10", "0:05", "0:28", "17:00")
ILLU_COUNTS = {}                            # 描いてよい数＝{部品の obj の名: (数, 出典)}（門番 check_illu ③）＝24本目は数を名乗る物を描かない（管・棒・バスは数えられない形か模式）
ILLU_ASSUME = {}                            # 想定の札を出すカット＝{カットID: 札の言葉}（門番 check_illu ④）
ILLU_DESTROY_CUTS = ()                      # 壊れる物の部品を描いてよいカット（門番 check_illu ⑫＝空なら全部止める）
ILLU_TOP_NOSCALE = {}                       # 縮尺を持たない模式の上から見た絵の置き場＝{置き場: 理由}（門番 check_illu ⑧ は縮尺の代わりに「人が0・模式の断り」を測る）
ILLU_SUB_UNTIL = None                      # 潜水艦の時刻の上限（門番 ⑮＝無ければ潜水艦を描いたカットは止まる）
ILLU_SUB_EXC = {}                           # 上の上限の例外＝{カットID: 時刻}
ILLU_SUB_STOP = None                        # 艦の絵を止めたカット（これより後に潜水艦を置かない）
ILLU_BOOM_CUTS = ()                         # 音の輪（9時18.1分の型）を置いてよいカット（門番 ⑰）
ILLU_MIX_TODO = {}                          # 混ざりの本物の側のつなぎ待ち＝{カットID: 理由}（門番 ⑦）
ILLU_MIX_BUNDLE = REF / "credits.json"      # 束ができたか（混ざりのつなぎ待ちの終わり）を見るファイル
AXIS_DOCS = {}
AXI = {}
QG = {}
QB = {}
PEOPLE_ORDER = ()
PEOPLE_SETS = {}
PEOPLE_REC = {}
PEOPLE_CUTS = ()     # 🔴 門番 check_qty がこの外の人の形を止める（亡くなった方の数に使わない）
QDOC = {}
QWHO = {}

SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "QG", "QB",
            "PEOPLE_ORDER", "PEOPLE_SETS", "PEOPLE_REC", "PEOPLE_CUTS", "QDOC", "QWHO", "SAT", "GEO", "SAT_NONE", "NEEDS_MASK", "SLIDE_MOUNT",
            "SLIDE_NOT_MOUNT", "OCR_NOT_TEXT")


# ══════════════════════════════════════════════════════════
#  門番の記録の表（24本目）── 門番の側に別に持つ記録（ルール §5b-88）
# ══════════════════════════════════════════════════════════
# 以下の表は、門番2本の本番の置き場にあった24本目の値を1文字も変えずに写したもの（GATES が門番ごとにまとめる）

# ── check_illu ──（🆕 24本目 ⑤b-3＝㊳ N1 炉の断面・㊴ N2 止める棒・㊵ N3 出力の時刻表・㊶ N4 避難のバス）
# 🔴 記録の値は門番の側に持つ（§5b-88＝illu24 の定数を読まない）。幾何は描く側の部品
#    頁は cuts.ss.REC_DOCS の通し番号（S1＝INSAG-7 の PDF の頁・S3＝2000＋・L2＝3000＋）
REC_N1 = dict(count=("1,660", "S1 p113（There were 1660 fuel channels）"), hd=(7.0, 11.8, "S1 p16（height 7 m, diameter 11.8 m）"))
REC_N2 = dict(core=(700.0, "S1 p16（height 7 m）"), water=(125.0, "S1 p14（1.25 m of water at either end）・S1 p15（図1 (a)＝125）"),
              disp=(450.0, "S1 p15（図1 (a)＝450）"), gap=(20.0, "S1 p15（図1 (a)＝20）"),
              speed=(40.0, "S1 p113（at a speed of 0.4 m/s）"), sec=(3.0, "S1 p65（01:23:40 → 01:23:43）"))   # 速さは cm／秒
REC_N3 = dict(am={"1:06": {"31本"}, "3:47": {"1,600MW"}, "7:10": {"13.2本"}, "14:00": set(), "23:10": {"26本"}},   # 表I-I p63
              night={"0:05": {"720MW"}, "0:28": {"500MW", "30MW"}},                                          # 表I-I p63・S3 p2020
              split={"1:00": "ソ連の報告", "1:03": "INSAG-7"},          # 200MW で止まった時刻＝S3 p2020「1:00」⇔ 表I-I p64「01.03」
              split_val="200MW", rule={"26", "30", "15"}, below=15.0,    # 付属書I p89「not less than 26-30 rods」「falls to 15 rods」
              plan={"700", "1,000", "20", "1"})                         # S3 p2020「700-1000 MW(th)」・台本 §9（30÷700）
REC_N4 = dict(bus="約1,200台", times=("14:00", "17:00"))                  # L2 p3024「nearly 1,200 buses」「began at 14:00 and finished at 17:00」

# ── check_mech ──（🆕 24本目 ⑤b-4〜⑤b-6＝図解 m24〈`tools/mech24.py`〉の記録の値）
#   ①報告の名と色（帰属の呼び分け＝台本 §1-5）②形・表・画素（f.mech["geo"]）を記録で ③基図と段の層の全部の字の数を rel で・時刻は記録の時刻だけ
#   ④句を原文の頁で（`ref/ep24/src/ep24_pages.txt`・`ref/ep24/src/*.pages.tsv`＝git の外・通し頁＝見本の REC_DOCS。Actions では句の照合だけ飛ばす）
REC_M24 = dict(
    reps=dict(r86=("1986年の報告", "bldg_a"), s86=("1986年のソ連の報告", "company"), c91=("1991年の委員会", "city"), r92=("1992年の報告", "state")),
    # 画面に出してよい時計の時刻＝台本 §1-5（1:06・1:00〈1986年の報告と帰属〉・7:10・13:05・14:00・23:10＝25日／0:05・0:28＝26日）
    #   🆕 ⑤b-5：1:19（1986年の報告のドラムの保護）・0:36（1991年の委員会の表）・1:23（1:23:04 試験の始まり・1:23:40 ボタン・1:23:43 信号＝秒は記録の欄で照らす）・
    #   22:00（避難を決めた時刻＝L2 p3024）。🔴 0:43 は「0時43分ごろ」の字で出す（秒は出さない＝台本 §1-5）。1:23:44 は言わない（計算の行）
    times={"1:06", "1:00", "7:10", "13:05", "14:00", "23:10", "0:05", "0:28", "1:19", "0:36", "1:23", "22:00"},
    # 🆕 ⑤b-5：どの見え方でも画面に出さない字（台本 §0-4・§1-5「言えない」）
    ng=("1:23:44", "1時23分44秒", "核爆弾", "無実", "嘘", "半分以下", "事故のあとの計算"),
    viol=("試験の計画", "非常用の冷却", "0時28分の急落", "700メガワット", "蒸気ドラムの保護", "タービンの保護", "残した制御棒の数"),
    years=dict(items=(("s86", "1986年8月", (1986, 8), False), ("r86", "1986年9月", (1986, 9), True), ("c91", "1991年", (1991, 0), True),
                      ("r92", "1992年", (1992, 0), True)),
               quote=(("S3 p2003", "DRAFT August 1986"), ("S2 p1001", "24 September 1986"), ("S1 p39", "(Moscow, 1991)"), ("S1 p1", "VIENNA, 1992"),
                      ("S1 p34", "does not retract INSAG-1, nor does it alter the conclusions of that report"))),
    cards7=dict(quote=(("S2 p1027", "This series of wilful violations of procedure, extraordinary as they were"),)),
    neutron=dict(heat="3,200", elec="1,000", quote=(("S2 p1008", "with an operating power of 1000 MW(e), 3200 MW(th)"),)),
    void=dict(nodes=("水が沸いて泡が増える", "中性子を吸う水が減る", "反応が強まる", "熱が増える"),
              quote=(("S1 p13", "the void and power coefficients of reactivity were both positive"),)),
    power20=dict(low=20, quote=(("S2 p1009", "becomes positive below approximately 20% of full power"),)),
    flow4=dict(boxes=(("ext", "外から来る電気"), ("tb", "止まりかけのタービン"), ("el", "電気"), ("pump", "ポンプ")),
               quote=(("S3 p2019", "to test the possibility of utilizing the mechanical energy of the rotor"),
                      ("S2 p1009", "until the standby diesel generators could supply emergency power"))),
    decay=dict(quote=(("S1 p121", "to verify whether cooldown of the core by forced cir-culation could be maintained"),)),
    cal=dict(years=(1982, 1983, 1984, 1985, 1986),
             marks={1982: ("ok", "3号機で試験"), 1984: ("ok", "改良した装置で試験"), 1985: ("ok", "同じく試験"),
                    1983: ("start", "12月　4号機の運転の始まり"), 1986: ("night", "4月　4号機で試験")},
             quote=(("S1 p61", "In 1982, the corresponding tests were carried out at Chernobyl Unit 3"),
                    ("S1 p61", "Additional tests with a modernized rundown unit were performed in 1984 and 1985."),
                    ("S1 p61", "Chernobyl Unit 4 was com-missioned in December 1983 without having been tested under these conditions"))),
    plan=dict(quote=(("S1 p62", "not entirely satisfactory, primarily in terms of its safety measures"),
                     ("S3 p2019", "the section on safety measures was drafted in a purely formal way"))),
    blame=dict(chips=("承認なし", "その場で", "わざと"),
               quote=(("S1 p34", "unapproved changes in the test procedure were deliberately made on the spot"),)),
    cut=dict(quote=(("S3 p2019", "it called for shutting off the reactor's emergency core cooling system"),
                    ("S3 p2019", "the safety of the reactor would be substantially reduced"))),
    site=dict(n=4, mark=4, quote=(("S2 p1008", "Four have been operating at Chernobyl"),)),
    dial=dict(t="1:06", t86="1:00", quote=(("S1 p63", "01:06 Start of reactor power reduction"), ("S2 p1028", "At 01:00 on 25 April"),
                                          ("S3 p2020", "at exactly 1:00 hours"))),
    ruler=dict(ticks=(30, 26, 15), quote=(("S1 p89", "not less than 26-30 rods"),
                                          ("S1 p89", "When the ORM falls to 15 rods, the reactor should be shut down immediately"))),
    orm=dict(pts=(("1:06", 31.0), ("7:10", 13.2)), line=15.0,
             quote=(("S1 p63", "ORM equals 31 manual control rods"), ("S1 p63", "07:10 ORM equals 13.2 manual control rods"),
                    ("S1 p21", "claim that this minimum ORM was also violated for several hours on 25 April"))),
    turbine=dict(t="13:05", stop=7, keep=8, quote=(("S1 p63", "13:05 Disconnection of turbogenerator No. 7 from the system"),)),
    eccs=dict(t="14:00", n=2, quote=(("S1 p63", "14:00 Disconnection of the ECCS"),)),
    stamp=dict(quote=(("S1 p20", "blocking of the ECCS was in fact permissible at Chernobyl if authorized by the Chief Engineer"),
                      ("S1 p20", "was even an approved step in the test procedure"))),
    off11=dict(t0="14:00", h=11, quote=(("S1 p20", "for the period of approximately 11 hours leading up to the accident"),
                                        ("S1 p20", "are indicative of an absence of safety culture"))),
    grid3=dict(cols=("r86", "c91", "r92"), row1=("安全の原則に反する", "運転の規則に反する", "承認で許されていた"),
               row2="どれも、事故の進み方には効いていない",
               quote=(("S2 p1035", "Safety principle violation"), ("S1 p82", "taking the ECCS out of operation is a violation of Section 2.10.5"),
                      ("S1 p88", "the switching off of the ECCS did not affect the initiation and scale"),
                      ("S1 p20", "INSAG believes that this point did not affect the initiation and development of the accident"))),
    trigger=dict(t="14:00", quote=(("S1 p88", "did not affect the initiation and scale of the accident"),
                                   ("S1 p63", "14:00 Postponement of testing programme"))),
    kiev=dict(quote=(("S1 p63", "Postponement of testing programme requested by Kiev power grid controller"),)),
    ring=dict(a="14:00", b="23:10", h=9, quote=(("S1 p63", "23:10 Power reduction continued"),
                                                ("S2 p1028", "not resumed until approximately 9 h later"))),
    day=dict(quote=(("S1 p63", "25 April 1986"), ("S1 p63", "26 April 1986"))),
    meter=dict(t="0:05", v=720.0, vmax=3200.0, plan=(700.0, 1000.0),
               quote=(("S1 p63", "00:05 Reactor thermal power was 720 MW"), ("S3 p2020", "was to be carried out at a reactor power of 700-1000 MW(th)"),
                      ("S2 p1008", "3200 MW(th)"))),
    clock=dict(t="0:28", quote=(("S1 p63", "00:28 At reactor thermal power of about 500 MW transfer made"),
                                ("S1 p63", "from the local to global main range automatic power control"))),
    hold=dict(n=3, quote=(("S2 p1036", "Operator error with transfer"), ("S2 p1028", "a 'hold power' request was not entered"))),
    swap=dict(quote=(("S1 p21", "Recent reports suggest that there was no operator error as such"),)),
    two91=dict(quote=(("S1 p21", "refers to an unknown cause and inability to control the power"),)),
    letter=dict(quote=(("S1 p21", "former Deputy Chief Engineer for Operations at the Chernobyl plant"),
                       ("S1 p21", "in a private communication refers to the system not working properly"))),
    docline=dict(quote=(("S1 p73", "failed to eliminate fast enough the imbalance"),)),
    say3=dict(cards=(("r86", "運転員の誤り"), ("letter", "仕組みが働かず"), ("c91", "素早く直せず")), v=200, t="1時ごろ",
              quote=(("S3 p2020", "Only at 1:00 on 26 April"), ("S1 p64", "Reactor thermal power increased to 200 MW and stabilized"))),
    bars=dict(rows=(("最大の出力", 3200, "LINE"), ("25日 4時前", 1600, "ship"), ("試験の予定の下の端", 700, "OK"), ("その夜 1時ごろ", 200, "AMBER"),
                    ("0時28分", 30, "ALERT")), n=4,
              quote=(("S2 p1025", "continuous operation below 700 MW(th) is forbidden by normal safety procedures"),
                     ("S1 p63", "03:47 Reactor thermal power is 1600 MW"), ("S1 p63", "reduction in thermal power to 30 MW"))),
    page86=dict(quote=(("S1 p21", "The emphasis placed on this statement in INSAG-1 was not warranted."),
                       ("S1 p20", "was based on oral statements made by Soviet experts"))),
    limit=dict(v=700.0, quote=(("S1 p28", "There should have been such a proscription, but there was none at the time."),
                               ("S1 p38", "sets a lower limit of 700 MW(th) for steady operation"))),
    pillars=dict(items=("設計", "規制", "運転の指示書"), empty="どれにも、禁止の項目なし",
                 quote=(("S1 p87", "there were no safe operating limits in terms of minimum permissible thermal reactor power"),
                        ("S1 p21", "was not proscribed, either in design, in regula-tory limitations or in operating instructions"))),
    inst=dict(quote=(("S1 p15", "they were all located at the mid-plane of the core"),
                     ("S1 p15", "a reactor operator had to rely mainly on experience and intuition"))),
    thermo=dict(quote=(("S1 p18", "The use of all eight pumps increased the coolant flow rate above that under nominal"),
                       ("S1 p74", "eight instead of the usual six MCPs were in operation"))),
    balance=dict(left=("一部のポンプ", "流れすぎ＝違反"), right=("8台のポンプ", "暴走を妨げたかも"),
                 quote=(("S1 p88", "if anything hindered the reactor runaway"), ("S1 p87", "the flow rates of certain MCPs actually exceeded the limit"))),
    # 🆕 ⑤b-5（2026-10-23）：第4〜7章の38カット。句は台本 §4 の出典の欄と同じ頁（pg で引き直した）
    guard=dict(n=(5, 6), quote=(("S2 p1027", "This series of wilful violations of procedure"),)),
    drum=dict(per=2, quote=(("S1 p17", "two parallel horizontal drum type separators in each loop"),)),
    drumtrip=dict(t="1:19", n=5, gauges=("水位", "圧力"),
                  quote=(("S2 p1025", "disabled the reactor trip on separation drum level and steam pressure"),
                         ("S2 p1025", "again a serious violation of normal station procedure"), ("S1 p22", "not at 01:19:00 as stated in INSAG-1"))),
    stage2=dict(t="0:36", quote=(("S1 p64", "00:36:24"), ("S1 p64", "The EPS trip point in response to a pressure drop in the steam separator drums was changed"),
                                 ("S1 p22", "two levels of protection"),
                                 ("S1 p22", "protection at the lower steam drum level remained effective throughout the event"))),
    marks5=dict(n=5, quote=(("S1 p28", "Disabling of the trip on steam drum water level would have been allowable; however, it did not occur"),
                            ("S1 p88", "were not the causes of the accident and did not affect its scale"))),
    tg2=dict(t="1:23:04", n=6, quote=(("S2 p1039", "two TGs-trip signal"),
                                      ("S3 p2027", "Blocking of reactor protection system relying on shutdown signal from two turbogenerators"),
                                      ("S1 p21", "rather than at 01:23:04 as stated in INSAG-1"))),
    retry=dict(n=2, quote=(("S3 p2027", "Intention, if necessary, of repeating the experiment with turbogenerators switched off"),)),
    shift=dict(t86=(1, 23, 4), t92=(0, 43, 27), lab92="0時43分ごろ",
               quote=(("S1 p21", "The event occurred at 00:43:27 rather than at 01:23:04 as stated in INSAG-1"),
                      ("S1 p21", "This trip was blocked in accordance with operational procedures and test procedures"))),
    shadow=dict(quote=(("S2 p1039", "This trip would have saved the reactor."), ("S1 p21", "seems not to be valid"))),
    seesaw=dict(left=("この保護の件は", "運転員を責めない"), right=("ただし", "運転員にも甘くない"),
                quote=(("S1 p21", "does not sup-port the apportionment of any blame to operating personnel"),
                       ("S1 p28", "the occurrence of this trip might well have caused the destruction of the reactor"))),
    light=dict(quote=(("S1 p28", "disabling of reactor protection seems to have been regarded rather lightly"),)),
    test200=dict(plan=700.0, act=200.0, quote=(("S1 p29", "When the reactor power could not be restored to the intended level of 700 MW(th)"),
                                               ("S1 p29", "on the spot they modified the test conditions"),
                                               ("S1 p29", "the test was initiated at a power level (200 MW(th))"))),
    printout=dict(quote=(("S3 p2021", "the available excess reactivity had reached a level requiring immediate shutdown of the reactor"),
                         ("S3 p2021", "Nevertheless, the staff were not stopped by this and began with the experiments."))),
    rods15=dict(rule=15, lo=6, hi=8, n=7, quote=(("S3 p2023", "At 1:22:30 the excess reactivity was only 6-8 rods"),
                                                 ("S1 p89", "When the ORM falls to 15 rods, the reactor should be shut down immediately"))),
    weight=dict(n=7, quote=(("S1 p22", "the ORM is much greater than was indicated in the INSAG-1 report"),)),
    skala=dict(min=(10, 15), quote=(("S1 p16", "This data system required about 10-15 min"),
                                    ("S1 p21", "the computer SKALA, which was used to calculate the ORM, became unreliable"),
                                    ("S1 p21", "it is likely that the operator did not know the value of the ORM"),
                                    ("S1 p21", "Probably he was aware that continued operation"))),
    twosay=dict(quote=(("S3 p2021", "the operator saw from a printout of the fast reactivity evaluation program"),
                       ("S1 p74", "did not know the calculated parameters, including the ORM, at this time"))),
    meaning=dict(quote=(("S1 p21", "regarding the lower limit on ORM as necessary for control of the reactor's spatial power distribution"),
                        ("S1 p21", "were not aware that it had safety significance"))),
    go=dict(t="1:23:04", quote=(("S3 p2021", "At 1:23:04, the emergency regulating valves of turbogenerator No. 8 shut."),)),
    valve8=dict(n=8, quote=(("S3 p2021", "At 1:23:04, the emergency regulating valves of turbogenerator No. 8 shut."),)),
    flow35=dict(sec=35, drop=(10, 15), quote=(("S1 p75", "During the rundown of turbogenerator No. 8 there was no increase in reactor power."),
                                              ("S1 p75", "The total coolant flow rate began to fall."),
                                              ("S1 p75", "Thirty-five seconds after the start of the transient it had fallen by 10-15% of the initial value"))),
    digital=dict(t="1:23:40", quote=(("S1 p76", "The Commission was unable to establish why the button was pressed."),
                                     ("S1 p65", "01:23:40 EPS-S button was pressed"))),
    spike=dict(t="1:23:43", v=530, quote=(("S1 p65", "01:23:43 Power excursion rate emergency protection system signals on"),
                                          ("S1 p65", "power exceeded 530 MW(th)"))),
    rodstop=dict(quote=(("S1 p65", "the RCPS rods stopped moving before they reached the lower limit stop switches"),
                        ("S3 p2021", "He then cut off the current to the sleeves of the servo drives so that the rods would fall into the core under their own weight"))),
    why8=dict(ch=8),
    roof=dict(quote=(("S3 p2021", "fell onto the roof of the machine room and started a fire"),)),
    dayband=dict(t="22:00", quote=(("S2 p1082", "On the morning of 26 April, people were instructed to remain indoors with windows and doors shut."),
                                   ("L2 p3024", "the decision to evacuate the residents of the town was taken at 22:00"))),
    notice=dict(date=(5, 4), quote=(("K1 19860507", "五月四日早朝、放射能対策本部会合を開催し"),
                                    ("K1 19860507", "直接雨水を摂取する場合はできるだけ木炭等でこして使用することが望ましい"),
                                    ("K1 19860507", "水道水、井戸水及び牛乳については心配ない"))),
    table6=dict(rows=6, cols=("違反", "動機", "結果"), mark=(2, 2),
                quote=(("S3 p2026", "Operator error in switching off local automatic control"),
                       ("S3 p2026", "Power dip well below the level provided for by the test programme"))),
    pile=dict(n=6, quote=(("S3 p2027", "the prime cause of the accident was an extremely improbable combination of violations"),)),
    carry=dict(quote=(("S3 p2027", "the rector was taken by the staff into a non-regulation state"),
                      ("S3 p2027", "the positive void coefficient of reactivity was able substantially to enhance the power excursion"))),
    sizes=dict(quote=(("S2 p1112", "is to be found in the so-called 'human element'"),
                      ("S2 p1018", "in combination with specific reactor features which compounded and amplified the effects of the errors"))),
    door=dict(quote=(("S2 p1047", "no attempt has been made to find alternative explanations"),)),
    venn3=dict(items=("決まり", "人", "組織"), quote=(("S2 p1018", "supplemented by the creation and maintenance of a \"nuclear safety culture\""),)),
    shield=dict(quote=(("S2 p1050", "Nuclear plant designs must be as far as possible invulnerable to operator error"),)),
    table86=dict(quote=(("S1 p27", "Certainly the account in INSAG-1 would have been different had the features of the control"),)),
    rod12=dict(m=1.2, h=7.0, quote=(("S3 p2028", "all the rods are inserted in the core to a depth of 1.2 m"),
                                    ("S3 p2028", "a continuing increase in the multiplying characteristics of the core in its lower part"),
                                    ("S1 p16", "height 7 m"))),
    rodq=dict(ch=8),
    # 🆕 ⑤b-6（2026-10-23）：地図2と第8〜11章の40。句は台本 §4 の出典の欄と同じ頁（scratchpad の pg で引き直した）。
    #   🆕 国会会議録の 1986-05-15（K1 19860515＝検索の JSON の発言）・UNSCEAR 白書 2018（L4 pdfN）・IARC 2006（L8 pdfN）・INES の手引き（L10 pdfN）は
    #   `_m24_page` が git の外の pages.tsv から引く。WEB（事業者の年表・防災白書）は保存なし＝句を持たない（値だけ）
    ussr=dict(staff=176, night=268,
              pts=dict(plant=(51.3892, 30.0992), pripyat=(51.4045, 30.0542), town=(51.2763, 30.2219), kiev=(50.4501, 30.5234)),   # 一般の座標（地図の値）
              quote=(("S3 p2016", "On the night of 25-26 April 1986 there were 176 duty operational staff"),
                     ("S3 p2016", "there were 268 builders and assemblers working on the night shift on the site of the third construction stage"))),
    japan=dict(d1=(5, 3), d2=(5, 14), n=29, places=("東京", "千葉", "神奈川"),
               quote=(("K1 19860507", "五月三日に至り、東京都、千葉県、神奈川県におきまして"), ("K1 19860507", "沃素131が検出されました"),
                      ("K1 19860515", "五月三日以降十四日時点で、二十九都道府県にわたり"))),
    rodparts=dict(quote=(("S1 p14", "A graphite rod termed a 'displaced is attached to each end of the length of absorber"),)),
    len7=dict(h=7.0, d=4.5, w=1.25, quote=(("S1 p14", "with 1.25 m of water at either end"), ("S1 p16", "height 7 m"))),
    lowred=dict(quote=(("S1 p53", "local introduction of positive reactivity in the lower part of the core occurs"),
                       ("S1 p14", "depended on the spatial distribution of the power density and the operating regime"))),
    sand=dict(t=(18, 12), quote=(("S1 p14", "when starting from the upper limit stop switches, was 18 s"), ("S1 p37", "reduced from 18 s to 12 s"))),
    lines3=dict(rods=(30, 15, 7), sec=8, quote=(("S1 p49", "When the ORM is about 30 effective manual control rods"), ("S1 p49", "When the ORM is about 15 control rods"),
                                                  ("S1 p49", "In the case of a non-regulation ORM of 7 control rods, during the first eight seconds"),
                                                  ("S1 p49", "the chain reaction is being accelerated rather than terminated"))),
    months=dict(found=((1983, 11), (1983, 12)), acc=(1986, 4), n=30,
                quote=(("S1 p53", "discovered experimentally in November/December 1983 during the physical startup of Ignalina Unit 1"),)),
    names2=dict(rows=("イグナリナ（リトアニア）", "チェルノブイリ4号機"), mark=dict(r92=(True, False), c91=(True, True)),
                quote=(("S1 p23", "first been identified at the Ignalina RBMK plant in the Lithuanian Republic in 1983"),
                       ("S1 p53", "physical startup of Ignalina Unit 1 and that of Chernobyl Unit 4"))),
    ideas=dict(cards=("棒の形を変える", "抜き切る棒の数を限る"), quote=(("S1 p54", "but none of them were implemented before the accident"),
                                                              ("S1 p54", "limitations on the withdrawal of the manual control rods"))),
    longarrow=dict(a=(1983, 11), b=(1986, 4), quote=(("S1 p26", "It is reprehensible that such a deficiency had been known of for so long"),)),
    lecterns=dict(y87=1987, y86=(1986, 8),
                  quote=(("S1 p23", "first acknowledged by Soviet experts at the Conference on Nuclear Power Performance and Safety in Vienna in 1987"),)),
    fog=dict(quote=(("S1 p33", "It is not known for certain what started the power excursion"),)),
    rulers2=dict(r86=100, sec=4, lo=3.5, hi=80, quote=(("S2 p1010", "the first power peak reached 100 times the nominal power within four seconds"),
                                                       ("S1 p131", "ranging from 3.5 times the initial value in Model 2 to approximately 80 times"))),
    memo=dict(date=(1983, 12), quote=(("S1 p54", "Triggering of the EPS in this case may lead to the introduction of positive reactivity."),
                                      ("S1 p54", "When the reactor power decreases to 50%"), ("S1 p100", "Letter No. 33-08/67 of 23 December 1983"),
                                      ("S1 p100", "KURCHATOV INSTITUTE OF ATOMIC ENERGY, Moscow, Letter No. 33-08/67"))),
    four=dict(items=("低い出力", "少ない残りの棒", "炉の性質", "棒の欠陥"), quote=(("S1 p33", "the concurrence of the following major factors"),)),
    volkov=dict(date=(5, 1), pick="design", quote=(("S1 p70", "Somewhat earlier, on 1 May 1986"),
                                                   ("S1 p70", "not to the actions of the operating personnel, but to the design of the reactor"))),
    funnel=dict(out="職員の誤り", n=2, m=6, quote=(("S1 p70", "all the causes of the accident were reduced exclusively to personnel errors"),
                                                 ("S1 p70", "(2 June 1986 and 17 June 1986)"))),
    road=dict(quote=(("S1 p70", "paved the way for the one-sided presentation of information"),)),
    notstop=dict(rods=15, day=25, quote=(("S1 p81", "The Commis-sion assumes that the personnel deliberately violated this requirement."),
                                         ("S1 p81", "this violation was not die cause of the accident"), ("S1 p81", "on 25 April"))),
    cheese=dict(items=("炉の物理の性質", "止める棒の設計", "定めのない状態へ"),
                quote=(("S1 p33", "specific physical characteristics of the reactor"), ("S1 p33", "specific design features of the reactor control elements"),
                       ("S1 p33", "not specified by procedures or investigated by an independent safety body"))),
    precursor=dict(y1=1975, y2=1986, quote=(("S1 p33", "is even considered by some to have been a precursor to the Chernobyl accident"),
                                            ("S1 p33", "were not aware of the nature and causes of the accident at Leningrad Unit 1"))),
    puzzle=dict(quote=(("S1 p34", "critical actions of the operators were most ill judged"),
                       ("S1 p34", "the human factor has still to be considered as a major element"))),
    bins4=dict(ev=("違反", "違反ではない", "誤りとは言えないようだ", "違反ではない", "形の上の違反", "違反ではない", "違反"),
               quote=(("S1 p20", "blocking of the ECCS was in fact permissible at Chernobyl if authorized by the Chief Engineer"),
                      ("S1 p21", "Recent reports suggest that there was no operator error as such"),
                      ("S1 p28", "There should have been such a proscription, but there was none at the time."),
                      ("S1 p21", "This trip was blocked in accordance with operational procedures and test procedures"),
                      ("S1 p22", "the ORM is much greater than was indicated in the INSAG-1 report"),
                      ("S1 p34", "unapproved changes in the test procedure were deliberately made on the spot"))),
    twox=dict(cards=("運転員の責めは消えた", "1986年の報告は取り消し"),
              quote=(("S1 p34", "operating rules were violated"), ("S1 p34", "does not retract INSAG-1"))),
    merge2=dict(year=1989, quote=(("S1 p120", "In October and November 1989"),
                                  ("S1 p120", "reactor instability caused both by design faults and the operating regime"))),
    stairs=dict(n=9, m=5, quote=(("K1 19860515", "合計九名が死亡していると聞いております"),)),
    num31=dict(n=31, of=300, quote=(("S2 p1118", "300 power plant and fire-fighting personnel admitted to hospitals, of whom 31 have so far died"),)),
    blocks30=dict(t=30, rad=28, quote=(("L2 p3005", "30 power plant employees and firemen (including 28 deaths that were due to radiation exposure)"),)),
    two31=dict(forum=((28, "放射線"), (2, "けが"), (1, "心臓")), n=31,
               quote=(("S2 p1118", "of whom 31 have so far died"), ("L1 p4012", "Among these workers, 28 persons died in 1986 due to ARS"),
                      ("L1 p4012", "Two more persons had died at Unit 4 from injuries unrelated to radiation"),
                      ("L1 p4012", "one additional death was thought to have been due to a coronary thrombosis"))),
    circles=dict(n=(237, 134), quote=(("L2 p3040", "a total of 237 were initially examined for signs and symptoms of acute radiation sickness"),
                                      ("L2 p3040", "This diagnosis was later confirmed in 134 patients"))),
    area60=dict(pop=600000, base=100000, add=4000, quote=(("L1 p4013", "among the 600 000 persons receiving more"),
                                                          ("L1 p4014", "This might eventually represent up to four thousand fatal cancers"),
                                                          ("L1 p4014", "in addition to the approximately 100 000 fatal cancers"),
                                                          ("L1 p4014", "to be expected due to all other causes"))),
    scope2=dict(iarc=(16000, 40, 2065), quote=(("L8 pdf5", "about 16,000 deaths"), ("L8 pdf2", "The present analysis focused on 40 European"),
                                               ("L8 pdf2", "(up to 2065)"))),
    machine=dict(quote=(("L1 p4013", "These predictions were based on the experience of other populations exposed to radiation"),
                        ("L1 p4013", "such as the survivors of the atomic bombing in Hiroshima and Nagasaki"))),
    waffle=dict(n=20000, cells=100, q=25, lo=7, hi=50,
                quote=(("L4 pdf7", "registered in the period 1991−2015 in males and females, who were under 18 in 1986"),
                       ("L4 pdf7", "approached 20,000"), ("L4 pdf7", "is of the order of 0.25"),
                       ("L4 pdf7", "The uncertainty range of the estimated attributable fraction extends at least from 0.07 to 0.5"))),
    tags3=dict(tags=("誰が", "いつ", "何を数えたか")),
    gantt=dict(starts=((1, (1986, 10)), (2, (1986, 11)), (3, (1987, 12)))),        # WEB（事業者の年表）＝句は照らせない（台本の決定記録 decisions.md §3 の19）
    ines=dict(lv=8, year=1990, quote=(("L10 pdf12", "The scale was developed in 1990 by international experts convened by the IAEA"),
                                      ("L10 pdf13", "accident at the Chernobyl nuclear power plant is rated at Level 7 on INES."))),
    lvl7=dict(year=2011, date=(4, 12)),                                               # WEB（防災白書 平成23年版）＝句は照らせない
    tiers=dict(quote=(("S1 p35", "A general lack of safety culture in nuclear matters, at the national level as well as locally"),
                      ("S1 p33", "throughout the Soviet design, operating and regula"))),
    flip=dict(t=("0:28", "1:23:40"), quote=(("S1 p63", "00:28"), ("S1 p65", "01:23:40"))),
    tray=dict(quote=(("S1 p34", "Most reprehensibly, unapproved changes in the test procedure were deliberately made"),
                     ("S1 p26", "It is reprehensible that such a deficiency had been known of for so long"))),
)


GATES = {
    "check_mech": dict(REC_M24=REC_M24),
    "check_illu": dict(REC_N1=REC_N1, REC_N2=REC_N2, REC_N3=REC_N3, REC_N4=REC_N4),
}


_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・（gate を渡せば）その門番の記録の表を24本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss は触らない）＝14〜23本目・17本目の見本と重ねるとき。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が24本目の表で
       25本目の画を測る）。apply の前に**無かった名**も覚えて、restore で**消す**＝selftest のあとに24本目の名が本番へ残らない
       （fixture_ep15〜ep23・ep17 と同じ作り）。⚠️ `titan_fig.GEO` は触らない（24本目の地点は無い）"""
    saved = dict(full=not tables_only, ss={}, ss_new=[], gate=gate, tables={}, tables_new=[])
    if not tables_only:
        from cuts import ss
        saved["ss"] = {n: getattr(ss, n) for n in SS_NAMES if hasattr(ss, n)}
        saved["ss_new"] = [n for n in SS_NAMES if not hasattr(ss, n)]
    tabs = {}
    if gate is not None:
        name = Path(getattr(gate, "__file__", "") or "").stem
        tabs = GATES.get(name, {})
        for k in tabs:
            if hasattr(gate, k):
                saved["tables"][k] = getattr(gate, k)
            else:
                saved["tables_new"].append(k)
    _SAVED.append(saved)         # 覚えてから差し込む＝途中で落ちても restore() が戻せる
    if not tables_only:
        g = globals()
        for n in SS_NAMES:
            setattr(ss, n, g[n])
    for k, v in tabs.items():
        setattr(gate, k, v)


CUTS_SHA = "7ae693a1"      # 24本目の章ファイルが最後に live だった版（章ファイルを25本目の器に替える前＝git の `7ae693a1`＝25本目 ⑤b-1 の移し替えの merge）
_CUTS24 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def _footage24():
    """24本目の映像の台帳 `CLIPS`（`ref/ep24/clips.json`）と使う区間 `USE`・器の黒帯の割合 `PILLAR`（git の CUTS_SHA の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}`）を返す。
    🔴 24本目の章ファイルは `ss.vid` で `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を引く（フリー素材のカットは台帳の `"stock": true` を見て、ひかえの静止画の名を
    `ep24/stock/fb_<cid>.jpg` に決める）。本番の footage は25本目の表になった＝そのままだと24本目のフリー素材のカットは `ref/ep24/fb_<cid>.jpg`（無い名）の箱を
    決めに行って章ファイルが読み込みで落ちる。→ 章ファイルを読む間だけ、この表を footage に差す（`cuts_ep24` が戻す）。
    footage.py の `USE`・`PILLAR` は値だけの代入＝その2文だけを取り出して評価する（footage.py 全体は import しない）。
    ⚠️ 24本目の PILLAR は空（17本目の V1 のような黒帯の器は無い）＝空でも止めない。USE（8カット）と台帳が読めなければ止める"""
    import ast
    import json
    import subprocess
    p = subprocess.run(["git", "-C", str(ROOT), "show", f"{CUTS_SHA}:tools/footage.py"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 24本目の映像の使う区間を git の {CUTS_SHA} の tools/footage.py から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    ns = {}
    for node in ast.parse(p.stdout.decode("utf-8")).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("USE", "PILLAR") for t in node.targets):
            exec(compile(ast.Module([node], []), f"footage_{CUTS_SHA}", "exec"), ns)
    use, pillar = ns.get("USE"), ns.get("PILLAR")
    clips_file = REF / "clips.json"
    if not use or pillar is None or not clips_file.exists():
        raise RuntimeError(f"🔴 24本目の映像の表が読めていない（USE {len(use or {})}・PILLAR {'無い' if pillar is None else len(pillar)}・"
                           f"{clips_file} {'ある' if clips_file.exists() else '無い'}）")
    return json.loads(clips_file.read_text(encoding="utf-8")), use, pillar


def cuts_ep24():
    """24本目の章ファイル（git の CUTS_SHA の `tools/cuts/`＝24本目の ss.py ごと）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。
    読む間だけ `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を24本目の表にする（`_footage24`＝本番の footage は25本目の表）。読み終えたら戻す。"""
    if _CUTS24:
        return _CUTS24[0]
    import importlib
    import io
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import tempfile
    import footage as _FO
    clips24, use24, pillar24 = _footage24()
    p = subprocess.run(["git", "-C", str(ROOT), "archive", CUTS_SHA, "tools/cuts"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 24本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts24_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep24 の写真・頁を読む＝根の下の作業場所の
        # フォルダ（ref・out ほか）へ一時フォルダから junction（Windows のフォルダへの道しるべ）を張る。消すときは先に道しるべだけ外す
        import _winapi
        for d in ROOT.iterdir():
            if d.is_dir() and d.name not in ("tools", ".git"):
                _winapi.CreateJunction(str(d), str(tmp / d.name))
                links.append(tmp / d.name)
        live = {k: v for k, v in sys.modules.items() if k == "cuts" or k.startswith("cuts.")}
        before = set(sys.modules)
        for k in live:
            del sys.modules[k]
        sys.path.insert(0, str(tmp / "tools"))
        keep_fo = (_FO.CLIPS, _FO.USE, _FO.PILLAR)
        _FO.CLIPS, _FO.USE, _FO.PILLAR = clips24, use24, pillar24          # 章ファイルを読む間だけ（finally で戻す）
        try:
            old = importlib.import_module("cuts")
            got = (dict(old.PLAN), dict(old.SPEC))
            broken = dict(getattr(old, "BROKEN", {}) or {})
        finally:
            _FO.CLIPS, _FO.USE, _FO.PILLAR = keep_fo
            sys.path.remove(str(tmp / "tools"))
            for k in set(sys.modules) - before:
                del sys.modules[k]
            for k in [k for k in sys.modules if k == "cuts" or k.startswith("cuts.")]:
                del sys.modules[k]
            sys.modules.update(live)
    finally:
        for ln in links:
            os.rmdir(ln)          # 道しるべだけを外す（中身＝本線のフォルダには触らない）
        if any(x.exists() for x in links):
            raise RuntimeError(f"🔴 一時フォルダの道しるべを外せない＝{tmp} を消さずに止める（本線のフォルダを消さないため）")
        shutil.rmtree(tmp, ignore_errors=True)
    # 🔴 24本目は 242カット＋ed01＝SPEC 243（git の 7ae693a1）。章ファイルが1本でも読めない（BROKEN）と SPEC が欠ける＝黙って一部で検算しない
    if broken or len(got[0]) != 242 or len(got[1]) != 243 or "c101" not in got[1]:
        raise RuntimeError(f"🔴 24本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}・読めない章 {sorted(broken)[:6]}）")
    _CUTS24.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を24本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で25本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep24()
    _SAVED.append(dict(cuts=(dict(cuts.PLAN), dict(cuts.SPEC))))
    cuts.PLAN.clear()
    cuts.PLAN.update(copy.deepcopy(plan))
    cuts.SPEC.clear()
    cuts.SPEC.update(copy.deepcopy(spec))


def restore():
    """apply() の前の本番の値に戻す（selftest のあと・本番の照合の前に呼ぶ）。apply を呼んでいなければ何もしない。
    ss と門番の表は、apply の前に無かった名を消す。
    tables_only で差し込んだ分は ss を覚えていない＝戻さない（先に差し込んだ別の見本を壊さない）。LIFO（あとに apply した順）"""
    while _SAVED:
        s = _SAVED.pop()
        if s.get("cuts") is not None:          # apply_cuts() の分＝25本目の PLAN・SPEC へ戻す
            import cuts
            plan, spec = s["cuts"]
            cuts.PLAN.clear()
            cuts.PLAN.update(plan)
            cuts.SPEC.clear()
            cuts.SPEC.update(spec)
            continue
        if s["full"]:
            from cuts import ss
            for n, v in s["ss"].items():
                setattr(ss, n, v)
            for n in s["ss_new"]:
                if hasattr(ss, n):
                    delattr(ss, n)
        gate = s["gate"]
        for k, v in s["tables"].items():
            setattr(gate, k, v)
        for k in s["tables_new"]:
            if hasattr(gate, k):
                delattr(gate, k)
