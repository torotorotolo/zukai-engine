# -*- coding: utf-8 -*-
"""29本目（GMO不正アクセス問題・2026-10-20 に異変を確認・会社のシステムへの不正アクセス＝事件の回の3本目）の型の値＝**門番の selftest の見本**（本番の表ではない）。

■ 2026-11-05（30本目 地下鉄サリン事件の ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `dc72dd8a` と同じ）
  ・`cuts/ss.py` の29本目の値＝説明カットの地の写真の明るさ（GROUND＝14点）・地図なしの言い分（SAT_NONE）・
    写真の束の定数（顔とナンバーだけ升目にする点 NEEDS_MASK 4・台紙の縁でない暗い帯の名簿 SLIDE_NOT_MOUNT 8）。
    29本目も空のままだった表（REC_DOCS・ILLU_*・AXIS_DOCS・AXI・QG・QB・PEOPLE_*・QDOC・QWHO・SLIDE_MOUNT・OCR_NOT_TEXT・SAT・GEO・SAT_LINES・SAT_LINE_NOTE）も、
    29本目の状態として持つ（17・23〜28本目の見本と同じ考え方）
  ・門番の記録の表（check_mech＝REC_M29〈図解 `mech29.py` の記録の値＝名と色・値と比例・SNS の札の原文・言葉・電話番号・出さない言葉〉・
    check_sat＝REC_SAT_NUM〈29本目は地図なし＝空〉・REC_SAT_PAGES〈抜き書きの道＝git の外〉）。
    check_axis・check_qty・check_boxes・check_illu・check_photo_edge・check_photo_mask は29本目で足した表が無い（check_photo_edge の名簿は ss の SLIDE_*＝上）＝この見本に入れない。
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を29本目の実物でも確かめている（check_mech の m29）＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は30本目の空の器にした
  （fixture_ep14〜ep28・ep17 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep29
      fixture_ep29.apply(sys.modules[__name__])   # その処理の中だけ ss・この門番の記録の表が29本目になる
      try: …（検算）
      finally: fixture_ep29.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14〜28本目・17本目の見本と重ねるとき（check_mech）は
      fixture_ep29.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss は触らない
  🔴 本番の門番・絵の組み立てからは呼ばない（呼ぶと30本目の画に29本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。⚠️ ほかの回の見本（fixture_ep28 ほか）の積み荷とは別＝それぞれの restore で戻す。
■ 注意:
  ⚠️ 29本目の selftest のうち、**章ファイルの SPEC を読むもの**は check_mech の `_selftest_m29`（m29 のカット＝図解）。`apply(gate)`＋`apply_cuts()`（29本目の章ファイルを
     git の `CUTS_SHA`＝`dc72dd8a` から取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ29本目に入れ替える・git が無い所では止める＝fail closed）を使う（
     28本目の `_selftest_m28` と同じ）。
  ⚠️ 29本目の章ファイルは git の版の `tools/cuts/ss.py`（EP＝`ep29/`・29本目の値）ごと取り出して読む＝写真の名 `P("…")` は `ep29/…` のまま（本番の ss は `ep30/`）。
     ただし `ss.vid`・`ss.head`・`ss.tailv` は本番の **`footage.CLIPS`・`footage.USE`**（と `footage.PILLAR`）を引く（フリー素材 17カット＝台帳 `ref/ep29/clips.json`）＝
     本番の footage は30本目の表なので、`cuts_ep29()` は章ファイルを読む間だけ footage の3つを29本目の表（台帳 `ref/ep29/clips.json`・使う区間 `USE` と黒帯の
     git の `dc72dd8a` の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}` の2文を取り出して評価）に差し、読み終えたら戻す
     （`_footage29`＝17本目の `_footage17`・24〜28本目の `_footage24`〜`_footage28` と同じ）。29本目の footage の値は**ここに写していない**（git の `dc72dd8a` が正本）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep29/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は29本目の道を持つ。
  ⚠️ `NEEDS_MASK`・`SLIDE_MOUNT`・`SLIDE_NOT_MOUNT`・`OCR_NOT_TEXT` の鍵は **`ep29/` の名を文字で書いた**（本番の ss は `P(…)`・`f"{EP}…"` で組んでいた＝
     EP が ep30 になると `ep30/…`〈無い名〉に化ける。fixture_ep17・ep22〜ep28 と同じ扱い）。説明の文は1字も変えていない（値＝git の `dc72dd8a` の ss を評価した値）。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝29本目は 1.15）は見本に入れない（16〜28本目・17本目の見本も入れていない）＝本番の ss は今の値のまま。
  ⚠️ 写真の束の定数のうち `TRIM`（`pages.json` から読む＝REF が替われば追う）・`PRIVATE_OUT`・`NG_PHOTOS` は見本に入れない。
  ⚠️ `check_blank.ON_PURPOSE` は29本目も空だった＝見本に入れない。`build_jiko.LAB_HOLD_EP` は回の名で引く＝見本に入れない。
  ⚠️ 型として本番に残した＝ss の関数（`sat`・`ax`・`qb`・`P`・`page`・`vid`・`head`・`tailv`・`mv`・`mvz`・`tcam`・`gr`・`is_private`・`check_frame_only`・`check_card_…`）・
     `SAT_CREDIT`・`GROUND_LIC`・`PRIVATE_DIR`・`SNS_NOTE`・`SNS_NOTE_BOX`・`SNS_NOTE_INK`・`PAGE_BLUR`（回をまたいで同じ）・
     check_mech の `judge_m29`（表が空なら理由を出して止める入口）・check_sat の `_rec_page`・描く側の型 `tools/mech29.py`・`titan_fig.m29`（どれも cuts を読まない）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep29"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から（git の `dc72dd8a` の ss.py の代入文をそのまま写した・`P("…")` だけ `"ep29/….jpg"`・`f"{EP}…"` だけ `"ep29/…"` の文字に）
# ══════════════════════════════════════════════════════
SAT_CREDIT = "地図：Google マップの衛星写真（帰属は地図の右下）"   # 型の定数（本番の ss に残した・SAT を組むための名＝SS_NAMES に入れない）

NEEDS_MASK: dict[str, str] = {
    "ep29/cm096.jpg": "渋谷フクラス1階の通路（c303）＝奥から歩いてくる人の顔5つとバスのナンバー（CC BY 4.0）",
    "ep29/cm103.jpg": "渋谷駅西口の道路（c312）＝タクシーのナンバーとドアの車番・バス2台のナンバー（CC BY 2.0）",
    "ep29/t229.jpg": "夜の首都高と国道246号（c206・c608・地8カット）＝車のナンバー9台（CC0）",
    "ep29/cm105.jpg": "渋谷駅の工事（c418）＝額の下の人の顔1つ（CC0）",
}
SLIDE_MOUNT: dict[str, str] = {}
SLIDE_NOT_MOUNT: dict[str, str] = {
    "ep29/cm021.jpg": "昼のセルリアンタワー＝下の帯は建物の暗い足もと（額装）",
    "ep29/cm049.jpg": "夜のセルリアンタワーの上の階＝左・上・下の帯は夜の空（c106・c520 は全面）",
    "ep29/cm102.jpg": "夜の渋谷フクラス＝上の帯は夜の空（額装）",
    "ep29/p0010.jpg": "お濠と警視庁＝右の帯は手前の木の陰（c411 は全面）",
    "ep29/p0047.jpg": "警視庁の本部＝左の帯は手前の木の陰（地だけ）",
    "ep29/police/d1028.jpg": "開示の表の2頁＝左右の帯は表の罫線の外の余白（額装・引用）",
    "ep29/t229.jpg": "夜の首都高＝上の帯は夜の空（c206・c608 は全面）",
    "ep29/t232.jpg": "夜の首都高と GMO の看板＝左の帯は暗いビル（c201・c605 は全面）",
}
OCR_NOT_TEXT: dict[str, list] = {}
SAT = {}
GEO = {}
SAT_LINES = {}
SAT_LINE_NOTE = ""
SAT_NONE = "29本目は地図のカットが無い（映像方針の一覧・了承② 11-03＝会社のシステムへの不正アクセスの回で、場所を見せる話が無い）"
REC_PAGES = REF / "src" / "ep29_pages.txt"      # 部品の出典（`rec=`）を当てる原文（git の外＝手元だけ）
REC_DOCS = {}                               # 出典の書き方「資料名 p頁」の資料名 → 頁の範囲・画面の名・頁の出し方
ILLU_SPLIT_TIMES = ()                       # 割れる時刻（2つの資料で時刻が割れる所＝札は秒で見る）
ILLU_CROWD_UNTIL = None                     # 群れを描いてよい場面の時刻の上限（None＝群れを描かない）
ILLU_ROLES = dict(sprite=(), crowd=())      # 置いてよい役割（門番 check_illu ②）＝空の組なら、どの役割も置けない（fail closed）
ILLU_SEC_OK = {}                            # 札に出してよい秒＝{秒: 出典}（門番 check_illu ⑤）
ILLU_CLOCK_OK = ()                          # 札に出してよい時計の時刻（「時:分」まで）＝空なら時計の札を出せない
ILLU_COUNTS = {}                            # 描いてよい数＝{部品の obj の名: (数, 出典)}（門番 check_illu ③）
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
GROUND = {"cm003": 0.28, "cm004": 0.28, "cm027": 0.29, "cm030": 0.31, "cm032": 0.28, "cm055": 0.30, "cm056": 0.28, "cm057": 0.28,
          "cm059": 0.28, "cm107": 0.28, "p0047": 0.28, "t229": 0.28, "t230": 0.28, "t232": 0.28}      # 🆕 29本目 ⑤b-4（2026-11-04）：`--suggest` の写し＝14点（⑤c直しで CM049 を外した＝端の輝度 3〜4）

SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "QG", "QB",
            "PEOPLE_ORDER", "PEOPLE_SETS", "PEOPLE_REC", "PEOPLE_CUTS", "QDOC", "QWHO", "SAT", "GEO", "SAT_LINES", "SAT_LINE_NOTE", "SAT_NONE",
            "NEEDS_MASK", "SLIDE_MOUNT", "SLIDE_NOT_MOUNT", "OCR_NOT_TEXT", "GROUND")


# ══════════════════════════════════════════════════════════
#  門番 check_sat から（git の `dc72dd8a` の check_sat.py の代入文をそのまま写した）
# ══════════════════════════════════════════════════════════
REC_SAT_NUM = {}
REC_SAT_PAGES = Path(__file__).resolve().parent.parent / "ref" / "ep29" / "src" / "news_frag_v2.txt"


# ══════════════════════════════════════════════════════════
#  門番 check_mech から（git の `dc72dd8a` の check_mech.py の代入文をそのまま写した）
# ══════════════════════════════════════════════════════════
_D_GAP = ("2026-08-05", "2026-10-20", "2026-09-01", "2026-10-01")
_D_TIPS = ("2026-10-28", "2026-10-29", "2026-10-30", "2026-11-02")
_D_ORDER = ("2026-08-05", "2026-08-17", "2026-09-20", "2026-10-14", "2026-10-20")
_D_HIST = ("2022-02-01", "2024-04-24", "2024-04-26", "2024-05-20", "2025-02-01")
REC_M29 = dict(
    src=dict(company=("会社", "uscg"), attacker=("攻撃した者", "company"), police=("警察", "tsb"), user=("利用者", "bldg_a"), press=("記者", "ship"),
             sec=("セキュリティの会社", "ntsb"), sns=("SNS の声", "SUB")),
    views=dict(
        gap76=dict(val=("2026-08-05", "2026-10-20", 76), d0="2026-08-05", pd=_D_GAP),
        cal3=dict(val=(("2026-10-19", "月", ("問い合わせを受ける", "調査の開始")), ("2026-10-20", "火", ("不正なプログラムを", "確認")),
                       ("2026-10-21", "水", ("午前4時", "全プランを順に停止", "第1報")))),
        num26739=dict(val=("26,739件", "対象となり得るサーバー数", "「不正アクセスまたは情報取得が確認された件数ではありません」")),
        two_reports=dict(val=("「個人情報の漏えいや、…悪用された事実は確認されておりません」", "「外部に持ち出された事実を確認」")),
        clock_noon=dict(val=(("10月27日", 9, 58), ("10月27日", 12, 0)), hands=((299.0, 348.0), (0.0, 0.0))),
        bounty=dict(val=("100万米ドル", "10月28日 12:00 から受付")),
        tips=dict(val=(("2026-10-28", 113), ("2026-10-29", 321), ("2026-10-30", 428), ("2026-11-02", 735)), pv=(113, 321, 428, 735), d0="2026-10-28", pd=_D_TIPS),
        order4=dict(val=_D_ORDER, d0="2026-08-05", pd=_D_ORDER),
        gap2=dict(val=(76, 64), d0="2026-08-05", pd=("2026-08-05", "2026-08-17", "2026-10-20")),
        qa_why=dict(val=("「なぜ10月20日まで気づけなかったのか」", "「その回答は今持ってございません」")),
        two_says=dict(val=("「可能性」", "「確認」")),
        know=dict(val=(("順番と日付", "76日"), ("どう入ったのか", "なぜ気づけなかったのか", "攻撃した者が誰か"))),
        qa_route=dict(val=("「今回攻撃された箇所は、2年前に指摘された箇所なのか」", "「侵入の経路はまだ正確に把握できていない」")),
        hist=dict(val=(_D_HIST, "「ネットのセキュリティもGMO」"), d0="2022-02-01", pd=_D_HIST),
        cal24=dict(val=("2024-04-24", (3, 3), ("「診断結果の報告会」", "「エンジニア同士の詳細説明会」"))),
        deep_fast=dict(val=("「深さと速さの両面で不足しておりました」",)),
        sort5=dict(val=("セキュリティの修正の影響", "グループ全体の脆弱性の対応", "機能の開発", "性能の向上", "使いやすさ")),
        two_ans=dict(val=("基準はある", "どんな脆弱性なら取締役に上げるかの基準は当時は無かった")),
        scope=dict(val=(("不正と認めた取引", "実現損失（取引の差損と手数料など）"), ("市場の変動による損失", "得られたはずの利益", "間接的な損害"))),
        sum3=dict(val=(("基本的な情報", "10,000円"), ("金融・認証の情報", "15,000円"), ("プライバシー性の高い情報", "25,000円"))),
        paycut=dict(val=(30.0, 100.0), pv=(30.0, 100.0)),
        ai_say=dict(val=("「基本的に、AIが使われた証拠は無い」",)),
        contact=dict(val=("03-5456-2560", "help.onamae.com/contact/")),
        tipline=dict(val=("cybercrimebounty.gmo", "info@cybercrimebounty.gmo", "「ご自身での犯人の特定や接触、確証のない情報の投稿はお控えいただき」",
                          "出典：GMOインターネットグループ『【重要】「お名前.com デスクトップクラウド」への不正アクセスに関する現在の対応について（第16報）』2026-10-29 20:50時点 group.gmo/info/alert/2026102902/")),
    ),
    # SNS の札の原文（検索の控えの字＝ref/ep29/src/sns/〈git の外〉・アカウント名は持たない）
    sns=dict(k307=("GMOの正午になる前にPCの電源切ってとかいう呼びかけ今知った。こんなん気づかなかった人が殆どなのでは……。", "X の投稿（2026年10月27日）"),
             k618=("9月末で解約した人間だけど、GMOから今日まで1度もメールで案内ないんだけど。", "X の投稿（2026年11月3日）"),
             k616=("AIと事件の問題の本質は直接的に関係ないような。AIの脅威に問題点をすり替えているように聞こえた。", "X の投稿（2026年11月3日）"),
             k617=("…今年の8月に侵入されていたのに10月まで気づかなかった理由だ。", "X の投稿（2026年11月2日）"),
             k619=("…侵入に2カ月半気づけなかった会社の責任も重い。それでも、叩く順番はまず犯人じゃない？", "X の投稿（2026年11月3日）")),
    ng=("犯人", "加害者", "流出", "容疑者"),
    note="※SNS の投稿。事実かは確かめられていません",      # 了承②の文言＝描く側の cuts.ss.SNS_NOTE と別に持つ
    rel_src=r"^(第(1|3|4|8|12|16)報|開示 2026-(10-24|11-02)|説明会 2026-11-02|質疑 2026-11-02|ANN 2026-10-29|X 2026-1[01]-\d{2}|計算|時点 2026-11-03)$",
)


GATES = {
    "check_mech": dict(REC_M29=REC_M29),
    "check_sat": dict(REC_SAT_NUM=REC_SAT_NUM, REC_SAT_PAGES=REC_SAT_PAGES),
}

_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・（gate を渡せば）その門番の記録の表を29本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss は触らない）＝14〜28本目・17本目の見本と重ねるとき。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が29本目の表で
       30本目の画を測る）。apply の前に**無かった名**も覚えて、restore で**消す**＝selftest のあとに29本目の名が本番へ残らない
       （fixture_ep15〜ep28・ep17 と同じ作り）。⚠️ `titan_fig.GEO` は触らない（29本目の地点は無い）"""
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


CUTS_SHA = "dc72dd8a"      # 29本目の章ファイルが最後に live だった版（章ファイルを30本目の器に替える前＝git の `dc72dd8a`＝30本目 ⑤b-1 の移し替えの merge）
_CUTS29 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def _footage29():
    """29本目の映像の台帳 `CLIPS`（`ref/ep29/clips.json`）と使う区間 `USE`・器の黒帯の割合 `PILLAR`（git の CUTS_SHA の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}`）を返す。
    🔴 29本目の章ファイルは `ss.vid` で `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を引く（フリー素材のカットは台帳の `"stock": true` を見て、ひかえの静止画の名を
    `ep29/stock/fb_<cid>.jpg` に決める）。本番の footage は30本目の表になった＝そのままだと29本目のフリー素材のカットは `ref/ep29/fb_<cid>.jpg`（無い名）の箱を
    決めに行って章ファイルが読み込みで落ちる。→ 章ファイルを読む間だけ、この表を footage に差す（`cuts_ep29` が戻す）。
    footage.py の `USE`・`PILLAR` は値だけの代入＝その2文だけを取り出して評価する（footage.py 全体は import しない）。
    ⚠️ 29本目の PILLAR は空（29本目 ⑤b-1 で空にしたまま・フリー素材に要る欄は無かった）＝空でも止めない形は残す。USE（17カット＝フリー素材）と台帳が読めなければ止める"""
    import ast
    import json
    import subprocess
    p = subprocess.run(["git", "-C", str(ROOT), "show", f"{CUTS_SHA}:tools/footage.py"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 29本目の映像の使う区間を git の {CUTS_SHA} の tools/footage.py から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    ns = {}
    for node in ast.parse(p.stdout.decode("utf-8")).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("USE", "PILLAR") for t in node.targets):
            exec(compile(ast.Module([node], []), f"footage_{CUTS_SHA}", "exec"), ns)
    use, pillar = ns.get("USE"), ns.get("PILLAR")
    clips_file = REF / "clips.json"
    if not use or pillar is None or not clips_file.exists():
        raise RuntimeError(f"🔴 29本目の映像の表が読めていない（USE {len(use or {})}・PILLAR {'無い' if pillar is None else len(pillar)}・"
                           f"{clips_file} {'ある' if clips_file.exists() else '無い'}）")
    return json.loads(clips_file.read_text(encoding="utf-8")), use, pillar


def cuts_ep29():
    """29本目の章ファイル（git の CUTS_SHA の `tools/cuts/`＝29本目の ss.py ごと）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。
    読む間だけ `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を29本目の表にする（`_footage29`＝本番の footage は30本目の表）。読み終えたら戻す。"""
    if _CUTS29:
        return _CUTS29[0]
    import importlib
    import io
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import tempfile
    import footage as _FO
    clips24, use24, pillar24 = _footage29()
    p = subprocess.run(["git", "-C", str(ROOT), "archive", CUTS_SHA, "tools/cuts"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 29本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts29_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep29 の写真・頁を読む＝根の下の作業場所の
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
    # 🔴 29本目は 113カット＋ed01＝SPEC 114（git の dc72dd8a）。章ファイルが1本でも読めない（BROKEN）と SPEC が欠ける＝黙って一部で検算しない
    if broken or len(got[0]) != 113 or len(got[1]) != 114 or "c101" not in got[1]:
        raise RuntimeError(f"🔴 29本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}・読めない章 {sorted(broken)[:6]}）")
    _CUTS29.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を29本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で30本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep29()
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
        if s.get("cuts") is not None:          # apply_cuts() の分＝30本目の PLAN・SPEC へ戻す
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
