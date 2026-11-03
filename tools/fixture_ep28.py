# -*- coding: utf-8 -*-
"""28本目（タイムズカー情報漏えい・2026-09-25 検知・会社のシステムへの不正アクセス＝事件の回の2本目）の型の値＝**門番の selftest の見本**（本番の画には使わない）。

■ 2026-11-03（29本目 GMO不正アクセス問題の ⑤b-1・§0b）：本番の置き場から移した（**値は1つも変えていない**＝git の `6fb3d0fc` と同じ）
  ・`cuts/ss.py` の28本目の値＝説明カットの地の写真の明るさ（GROUND＝16点）・地図なしの言い分（SAT_NONE）・
    写真の束の定数（顔とナンバーだけ升目にする点 NEEDS_MASK 12・台紙の縁でない暗い帯の名簿 SLIDE_NOT_MOUNT 4）。
    28本目も空のままだった表（REC_DOCS・ILLU_*・AXIS_DOCS・AXI・QG・QB・PEOPLE_*・QDOC・QWHO・SLIDE_MOUNT・OCR_NOT_TEXT・SAT・GEO・SAT_LINES・SAT_LINE_NOTE）も、
    28本目の状態として持つ（17・23〜27本目の見本と同じ考え方）
  ・門番の記録の表（check_mech＝REC_M28〈図解 `mech28.py` の記録の値＝誰か・何かの名と色・値と比例・SNS の札の原文・言葉・電話番号・出さない言葉〉／
    check_sat＝REC_SAT_NUM〈28本目は地図なし＝空〉・REC_SAT_PAGES〈抜き書きの道＝git の外〉）。
    check_axis・check_qty・check_boxes・check_illu・check_photo_edge・check_photo_mask は28本目で足した表が無い（check_photo_edge の名簿は ss の SLIDE_*＝上）＝この見本の GATES に載せない
■ なぜ：回を替えたら本番の値は空にする（ルール §0b・記憶 project-jiko-rules-index）。けれど門番の selftest は
  「正しい絵が通り・壊した絵が鳴る」を28本目の実物でも確かめている（check_mech の m28）＝見本まで消すと物差しの検算ができない
  （記憶 feedback-verify-your-own-instrument）。→ 見本だけをここに残し、本番の置き場は29本目の空の器にした
  （fixture_ep14〜ep27・ep17 と同じ理由・同じ作り）。
■ 使い方（selftest の中だけ）:
      import fixture_ep28
      fixture_ep28.apply(sys.modules[__name__])   # その処理の中だけ ss・この門番の記録の表が28本目になる
      try: …（検算）
      finally: fixture_ep28.restore()             # 本番の値へ戻す（apply の前に無かった名は消す）
  14〜27本目・17本目の見本と重ねるとき（check_mech）は
      fixture_ep28.apply(sys.modules[__name__], tables_only=True)   # その門番の表（GATES）だけ。ss は触らない
  🔴 本番の門番・合成からは呼ばない（呼ぶと29本目の画に28本目の記録が混ざる＝§0b が防ぎたい事故そのもの）。
  ⚠️ `apply()`／`apply_cuts()` は `restore()` で**積んだ分を全部**（あとに積んだ側から）戻す＝入れ子の外側の apply も戻る。
     入れ子にするなら内側の `restore()` を呼ばず、一番外で1回だけ呼ぶ。⚠️ ほかの回の見本（fixture_ep27 ほか）の積み荷とは別＝それぞれの restore で戻す
■ 注意:
  ⚠️ 28本目の selftest のうち、**章ファイルの SPEC を読むもの**は check_mech の `_selftest_m28`（m28 のカット＝図解）。`apply(gate)`＋`apply_cuts()`（28本目の章ファイルを
     git の `CUTS_SHA`＝`6fb3d0fc` から取り出して `cuts.PLAN`・`cuts.SPEC` をその処理の中だけ28本目に入れ替える・git が無い所では止める＝fail closed）を使う（`restore()` で29本目へ戻る・LIFO）。
  ⚠️ 28本目の章ファイルは git の版の `tools/cuts/ss.py`（EP＝`ep28/`・28本目の値）ごと取り出して読む＝写真の名 `P("…")` は `ep28/…` のまま（本番の ss の EP は ep29）。
     ただし `ss.vid`・`ss.head`・`ss.tailv` は本番の **`footage.CLIPS`・`footage.USE`**（と `footage.PILLAR`）を引く（フリー素材 14カット＝台帳 `ref/ep28/clips.json`）＝
     本番の footage は29本目の表なので、`cuts_ep28()` は章ファイルを読む間だけ footage の3つを28本目の表（台帳 `ref/ep28/clips.json`・使う区間 `USE` と黒帯の割合 `PILLAR` は
     git の `6fb3d0fc` の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}` の2文を取り出して評価）に差し、読み終えたら戻す
     （`_footage28`＝17本目の `_footage17`・24〜27本目の `_footage24`〜`_footage27` と同じ）。28本目の footage の値は**ここに写していない**（git の `6fb3d0fc` が正本）。
  ⚠️ `ILLU_MIX_BUNDLE`（`ref/ep28/credits.json`）は本番では REF から導く道（ss 側は `REF / "credits.json"` を残した）＝この見本は28本目の道を持つ。
  ⚠️ `NEEDS_MASK`・`SLIDE_MOUNT`・`SLIDE_NOT_MOUNT`・`OCR_NOT_TEXT` の鍵は **`ep28/` の名を文字で書いた**（本番の ss は `P(…)`・`f"{EP}…"` で組んでいた＝
     EP が ep29 になると `ep29/…`〈無い名〉に化ける。fixture_ep17・ep22〜ep27 と同じ扱い）。説明の文は1字も変えていない（値＝git の `6fb3d0fc` の ss を評価した結果と同じ）。
  ⚠️ `PANEL_AR`（写真の束ごとに取り直す定数＝28本目は 0.97）は見本に入れない（16〜27本目・17本目の見本も入れていない）＝本番の ss は今の値のまま残し、29本目の束で取り直す。
  ⚠️ 写真の束の定数のうち `TRIM`（`pages.json` から読む＝REF が替われば追う）・`PRIVATE_OUT`・`NG_PHOTOS` は見本に入れない。
  ⚠️ `check_blank.ON_PURPOSE`（28本目 c102 ほか）は門番の selftest が読まない＝見本に入れない（値は git の `6fb3d0fc`）。`build_jiko.LAB_HOLD_EP` は回の名で引く＝本番の表に残した。
  ⚠️ 型として本番に残した＝ss の関数（`sat`・`ax`・`qb`・`P`・`page`・`vid`・`head`・`tailv`・`mv`・`mvz`・`tcam`・`gr`・`is_private`・`check_frame_only`・`check_card_mix`・`src`）・
     `SAT_CREDIT`・`GROUND_LIC`・`PRIVATE_DIR`・`SNS_NOTE`・`SNS_NOTE_BOX`・`SNS_NOTE_INK`（回をまたいで同じ）・
     check_mech の `SNS_VIEWS28`・`judge_m28`（表が空なら理由を出して止める入口）・check_sat の `_rec_page`・描く側の型 `tools/mech28.py`・`titan_fig.m28`（どれも cuts.ss の28本目の値を読まない）。
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "ref" / "ep28"


# ══════════════════════════════════════════════════════
#  cuts/ss.py から（git の `6fb3d0fc` の ss.py の代入文をそのまま写した・`P("…")` だけ `"ep28/….jpg"`・`f"{EP}…"` だけ `"ep28/…"` の文字に）
# ══════════════════════════════════════════════════════
SAT_CREDIT = "地図：Google マップの衛星写真（帰属は地図の右下）"   # 型の定数（本番の ss に残した・SAT を組むための名＝SS_NAMES に入れない）

NEEDS_MASK: dict[str, str] = {
    "ep28/cm001.jpg": "デミオのナンバー（カラーコーンから出た半分）",
    "ep28/cm006.jpg": "手前の青い車・赤いミニ・銀の車・奥の白い車のナンバー",
    "ep28/cm034.jpg": "左の銀の車と札の下の車のナンバー",
    "ep28/cm036.jpg": "左の白い車と右の軽自動車のナンバー",
    "ep28/cm039.jpg": "手前と奥の車6台のナンバー",
    "ep28/cm045.jpg": "札の下の車2台のナンバー",
    "ep28/cm046.jpg": "奥の車3台のナンバー",
    "ep28/cm047.jpg": "白い軽自動車のナンバー",
    "ep28/cm049.jpg": "白い軽ワゴンと銀のワゴンのナンバー",
    "ep28/cm054.jpg": "左の銀の車と赤いプリウスのナンバー",
    "ep28/cm057.jpg": "白い軽自動車と奥の車2台のナンバー",
    "ep28/cm065.jpg": "横断歩道を渡る2人と自転車の人の顔（私人）・白い軽ワゴンと黒い車のナンバー",
}
SLIDE_MOUNT: dict[str, str] = {}
SLIDE_NOT_MOUNT: dict[str, str] = {
    "ep28/cm008.jpg": "車の中の暗がり（上の 5.0%）＝写真の中身",
    "ep28/cm058.jpg": "夕方の看板の左の暗がり（左の 0.2%）＝写真の中身",
    "ep28/cm062.jpg": "夜空と夜の手前（上と下の 5.0%）＝写真の中身",
    "ep28/cm071.jpg": "免許証の裏面の左の縁の影（左の 1.5%）＝写真の中身",
}
OCR_NOT_TEXT: dict[str, list] = {}
SAT = {}
GEO = {}
SAT_LINES = {}
SAT_LINE_NOTE = ""
SAT_NONE = "28本目は地図のカットが無い（映像方針の一覧・了承② 11-01＝会社のシステムへの不正アクセスの回で、場所を見せる話が無い）"
REC_PAGES = REF / "src" / "ep28_pages.txt"      # 部品の出典（`rec=`）を当てる原文（git の外＝手元だけ）
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
GROUND = {"cm001": 0.28, "cm006": 0.28, "cm007": 0.28, "cm008": 0.31, "cm009": 0.28, "cm047": 0.29, "cm051": 0.28, "cm053": 0.28,
          "cm054": 0.29, "cm063": 0.28, "cm064": 0.30, "cm065": 0.28, "cm114": 0.28, "cm115": 0.29, "cm126": 0.28, "cm129": 0.28}

SS_NAMES = ("REC_PAGES", "REC_DOCS", "ILLU_SPLIT_TIMES", "ILLU_CROWD_UNTIL", "ILLU_ROLES", "ILLU_SEC_OK", "ILLU_CLOCK_OK", "ILLU_COUNTS",
            "ILLU_ASSUME", "ILLU_DESTROY_CUTS", "ILLU_TOP_NOSCALE", "ILLU_SUB_UNTIL", "ILLU_SUB_EXC", "ILLU_SUB_STOP",
            "ILLU_BOOM_CUTS", "ILLU_MIX_TODO", "ILLU_MIX_BUNDLE", "AXIS_DOCS", "AXI", "QG", "QB",
            "PEOPLE_ORDER", "PEOPLE_SETS", "PEOPLE_REC", "PEOPLE_CUTS", "QDOC", "QWHO", "SAT", "GEO", "SAT_LINES", "SAT_LINE_NOTE", "SAT_NONE",
            "NEEDS_MASK", "SLIDE_MOUNT", "SLIDE_NOT_MOUNT", "OCR_NOT_TEXT", "GROUND")


# ══════════════════════════════════════════════════════════
#  門番 check_sat から（git の `6fb3d0fc` の check_sat.py の代入文をそのまま写した）
# ══════════════════════════════════════════════════════════
REC_SAT_NUM = {}
REC_SAT_PAGES = Path(__file__).resolve().parent.parent / "ref" / "ep28" / "src" / "news_frag_v2.txt"


# ══════════════════════════════════════════════════════════
#  門番 check_mech から（git の `6fb3d0fc` の check_mech.py の代入文をそのまま写した）
# ══════════════════════════════════════════════════════════
REC_M28 = dict(
    src=dict(company=("会社", "uscg"), attacker=("攻撃した者", "company"), lawyer=("弁護士", "DOC"), kuni=("国", "tsb"), bank=("銀行", "ship"),
             jicc=("信用情報機関", "ntsb"), member=("会員", "bldg_a"), sns=("SNS の声", "SUB")),
    views=dict(
        three=dict(val=("146万4800件", "3000円分", "10万人超")),
        flow8=dict(val=(("不正アクセスを検知", "問い合わせ窓口開設", "調査開始", "対象サーバーを隔離", "不正アクセス経路を遮断",
                         "外部専門機関によるフォレンジック調査を開始", "個人情報保護委員会へ報告", "第1報を公表"), (3, 4, 6))),
        clock2=dict(val=(("9月25日", 9, 7), ("9月26日", 7, 25)), hands=((273.5, 42.0), (222.5, 150.0))),
        reports=dict(val=(("第1報〈9月25日〉", (), "「可能性」"), ("第2報〈9月28日〉", (), "約660万件"),
                          ("第3報〈9月29日〉", ("画像が漏えいしたアカウント",), "約160万件"), ("第5報〈10月23日〉", (), "調査の結果"))),
        cal4w=dict(val=((("第1報", "2026-09-25", "9月25日", (0, 5)), ("第2報", "2026-09-28", "9月28日", (1, 1)), ("第3報", "2026-09-29", "9月29日", (1, 2)),
                         ("第4報", "2026-10-16", "10月16日", (3, 5)), ("第5報", "2026-10-23", "10月23日", (4, 5))), 28)),
        six=dict(val=("氏名", "住所", "生年月日", "電話番号", "メールアドレス", "運転免許情報")),
        bars2=dict(val=(1600000, 1464800, 891602, 2356402), pv=(1600000, 1464800, 2356402)),
        words2=dict(val=("直ちに画像内容が閲覧可能な状態になったことを意味するものではありません", "将来的な復号の可能性を完全に否定できるものではありません")),
        club=dict(val=(("氏名・住所・生年月日・運転免許情報", "5件"), ("タイムズクラブカードの番号", "1万9510件"), ("ほかの会社のサービスとつなぐ番号", "13万5436件"))),
        ccard=dict(val=("一切保持していない", "28件")),
        fixn=dict(val=("計9件", "4件", "0件")),
        unit2=dict(val=(400.0, 662.8007), pv=(400.0, 662.8007)),
        inside=dict(val=(520.0, 120.0)),
        purpose4=dict(val=("会員登録時の本人確認手続き", "不正利用が疑われる事案への対応", "お問い合わせ対応", "各種の本人確認業務")),
        qa7=dict(val=("運転免許情報および画像は、なりすまし対策やお問い合わせ対応のため、7年間保管していました",)),
        law22=dict(val=("利用する必要がなくなったときは、当該個人データを遅滞なく消去するよう努めなければならない。",)),
        rule_oct=dict(val=((("9月25日", "検知"), ("10月16日", "決まりを改める"), ("10月末", "今ある画像を消す〈予定〉")),
                           (("今の会員", "会員の間は保有", "登録確認完了後、即時削除"), ("退会した人", "退会後7年間保有", "保有しない"))),
                      d0="2026-09-25", pd=("2026-09-25", "2026-10-16", "2026-10-31")),
        risk4=dict(val=("フィッシングメールやフィッシングサイトによる詐欺", "なりすましによる各種申込みや問い合わせ", "不正勧誘", "個人情報の悪用")),
        law_kyc=dict(val=("この命令は、令和九年四月一日から施行する。",)),
        fsa_check=dict(val=("「サードパーティリスク管理やインシデントが起きた場合の対応態勢も含めた」",)),
        jicc5=dict(val=(("10月1日", "2日", "3日", "4日", "5日"), ((0.0, 1.0, True), (1.0, 1.72, False), (1.72, 4.0, True), (4.0, 5.0, False)), "「お申込みの集中」")),
        qa12=dict(val=("信用情報機関が悪用の防止効果を保証するものではありません", "預金口座の開設時には利用されません")),
        cutoff=dict(val=("完全に切り捨てられている",)),
        formula=dict(val=(1464800, 3000, 44)),
        profit=dict(val=((440, 385), (44000, 38500, 411000), 12.5), pv=(440, 385)),
        damages=dict(val=((30000, "3万円"), (50000, "5万円"), (3000, "3000円")), pv=(30000, 50000, 3000)),
        quote3000=dict(val=("「3000円という金額を見たとき、非常に低すぎるのではないか」",)),
        two_claims=dict(val=("「勝手にローンを組まれた」", "「売買・公開されたことを示す事実は確認されておりません」")),
        contact=dict(val=("0120-25-8924", "share.timescar.jp/inquiry.html")),
    ),
    # SNS の札の原文（投稿の頁の字＝控え ref/ep28/src/sns/sns_posts_verified_20261031.tsv〈git の外〉・アカウント名は持たない）
    sns=dict(k2=("…退会後どれくらいで必ず削除するというのも追加されればいいのにね。タイムズカーの免許証の画像７年保管してたのも、本当おかしいし。", "X の投稿（2026年10月31日）"),
             k1a=("…ここはしっかり対応してるのでそこは素晴らしい。", "X の投稿（2026年10月29日）"),
             k1b=("個人的には3000円貰ってそれでOK派なんだけど、あえて集団訴訟のサイトにも申し込んでおいた。", "X の投稿（2026年10月29日）"),
             k3a=("タイムズカーじゃなくて、ハッカーたちが犯人だよね？", "X の投稿（2026年10月27日）"),
             k3b=("保管する必要のない画像を保管し続け、脆弱性のあるシステムで流出させたことは非難されても仕方ないですが、その後の犯罪の責任まで負わせる必要はあるのでしょうか？", "X の投稿（2026年10月17日）")),
    ng=("犯人", "加害者", "流出", "ハッカー"),
    note="※SNS の投稿。事実かは確かめられていません",      # 了承②の文言＝描く側の cuts.ss.SNS_NOTE と別に持つ
    rel_src=r"^(第[1-5]報|Q&A|e-Gov|開示 2026-(09-28|10-23)|金融庁 2026-10-09|JICC 2026-10-0[125]|PR 2026-08-17|弁護士ドットコム 2026-10-26|ABEMA 2026-10-26|三井住友銀行 2026-10-23|X 2026-10-\d{2}|計算|時点 2026-10-31)$",
)


GATES = {
    "check_mech": dict(REC_M28=REC_M28),
    "check_sat": dict(REC_SAT_NUM=REC_SAT_NUM, REC_SAT_PAGES=REC_SAT_PAGES),
}

_SAVED = []


def apply(gate=None, tables_only=False):
    """selftest の処理の中だけ、ss・（gate を渡せば）その門番の記録の表を28本目の値にする。
    tables_only=True なら、その門番の表（GATES）だけを差し込む（ss は触らない）＝14〜27本目・17本目の見本と重ねるとき。
    🔴 差し替える前の本番の値を覚える＝selftest のあと `restore()` で戻す（戻さないと、そのあとの本番の照合が28本目の表で
       29本目の画を測る）。apply の前に**無かった名**も覚えて、restore で**消す**＝selftest のあとに28本目の名が本番へ残らない
       （fixture_ep15〜ep27・ep17 と同じ作り）。⚠️ `titan_fig.GEO` は触らない（28本目の地点は無い）"""
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


CUTS_SHA = "6fb3d0fc"      # 28本目の章ファイルが最後に live だった版（章ファイルを29本目の器に替える前＝git の `6fb3d0fc`＝29本目 ⑤b-1 の移し替えの merge）
_CUTS28 = []               # 読んだ (PLAN, SPEC) を1回だけ覚える


def _footage28():
    """28本目の映像の台帳 `CLIPS`（`ref/ep28/clips.json`）と使う区間 `USE`・器の黒帯の割合 `PILLAR`（git の CUTS_SHA の `tools/footage.py` の `USE = {…}`・`PILLAR = {…}`）を返す。
    🔴 28本目の章ファイルは `ss.vid` で `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を引く（フリー素材のカットは台帳の `"stock": true` を見て、ひかえの静止画の名を
    `ep28/stock/fb_<cid>.jpg` に決める）。本番の footage は29本目の表になった＝そのままだと28本目のフリー素材のカットは `ref/ep28/fb_<cid>.jpg`（無い名）の箱を
    決めに行って章ファイルが読み込みで落ちる。→ 章ファイルを読む間だけ、この表を footage に差す（`cuts_ep28` が戻す）。
    footage.py の `USE`・`PILLAR` は値だけの代入＝その2文だけを取り出して評価する（footage.py 全体は import しない）。
    ⚠️ 28本目の PILLAR は空（28本目 ⑤b-1 で空にしたまま・フリー素材に要る欄は無かった）＝空でも止めない形は残す。USE（14カット＝フリー素材）と台帳が読めなければ止める"""
    import ast
    import json
    import subprocess
    p = subprocess.run(["git", "-C", str(ROOT), "show", f"{CUTS_SHA}:tools/footage.py"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 28本目の映像の使う区間を git の {CUTS_SHA} の tools/footage.py から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    ns = {}
    for node in ast.parse(p.stdout.decode("utf-8")).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ("USE", "PILLAR") for t in node.targets):
            exec(compile(ast.Module([node], []), f"footage_{CUTS_SHA}", "exec"), ns)
    use, pillar = ns.get("USE"), ns.get("PILLAR")
    clips_file = REF / "clips.json"
    if not use or pillar is None or not clips_file.exists():
        raise RuntimeError(f"🔴 28本目の映像の表が読めていない（USE {len(use or {})}・PILLAR {'無い' if pillar is None else len(pillar)}・"
                           f"{clips_file} {'ある' if clips_file.exists() else '無い'}）")
    return json.loads(clips_file.read_text(encoding="utf-8")), use, pillar


def cuts_ep28():
    """28本目の章ファイル（git の CUTS_SHA の `tools/cuts/`＝28本目の ss.py ごと）を読み、(PLAN, SPEC) を返す。
    作業場所の外（一時フォルダ）に取り出し、`cuts` の名で一度だけ読んでから、本番の `cuts` の読み込みへ戻す
    （sys.modules と sys.path を元どおりにし、一時フォルダから読んだ module はすべて捨てる）。
    読む間だけ `footage.CLIPS`・`footage.USE`・`footage.PILLAR` を28本目の表にする（`_footage28`＝本番の footage は29本目の表）。読み終えたら戻す。"""
    if _CUTS28:
        return _CUTS28[0]
    import importlib
    import io
    import os
    import shutil
    import subprocess
    import sys
    import tarfile
    import tempfile
    import footage as _FO
    clips24, use24, pillar24 = _footage28()
    p = subprocess.run(["git", "-C", str(ROOT), "archive", CUTS_SHA, "tools/cuts"], capture_output=True)
    if p.returncode != 0 or not p.stdout:
        raise RuntimeError(f"🔴 28本目の章ファイルを git の {CUTS_SHA} から取り出せない（{p.stderr.decode('utf-8', 'replace')[:200]}）")
    tmp = Path(tempfile.mkdtemp(prefix="cuts28_"))
    links = []
    try:
        with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
            tf.extractall(tmp)
        # 章ファイルは自分の場所から根（tools の1つ上）を出して ref/ep28 の写真・頁を読む＝根の下の作業場所の
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
    # 🔴 28本目は 106カット＋ed01＝SPEC 107（git の 6fb3d0fc）。章ファイルが1本でも読めない（BROKEN）と SPEC が欠ける＝黙って一部で検算しない
    if broken or len(got[0]) != 106 or len(got[1]) != 107 or "c101" not in got[1]:
        raise RuntimeError(f"🔴 28本目の章ファイルが読めていない（PLAN {len(got[0])}・SPEC {len(got[1])}・読めない章 {sorted(broken)[:6]}）")
    _CUTS28.append(got)
    return got


def apply_cuts():
    """その処理の中だけ `cuts.PLAN`・`cuts.SPEC` の中身を28本目にする（同じ dict の中身を入れ替える＝`from cuts import PLAN` で
    持っている側にも効く）。`restore()` で29本目へ戻す（LIFO・apply と同じ _SAVED に積む）。"""
    import copy
    import cuts
    plan, spec = cuts_ep28()
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
        if s.get("cuts") is not None:          # apply_cuts() の分＝29本目の PLAN・SPEC へ戻す
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
