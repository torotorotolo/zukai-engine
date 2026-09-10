# -*- coding: utf-8 -*-
"""事故検証チャンネルのレイヤー書き出し。**いまは本番3本目「スレッシャー号」**。

  1本目 潜水艇タイタン号 229カット・35分02.9秒（公開ずみ。`57e6c16` が最終）
  2本目 日本航空123便   248カット・約38分（制作中）


■ 何がどこにあるか
  台本の文言   … `tools/narration.py` の SCRIPT（**正本はあちら**。ここには写さない）
  カットの尺   … `audio/narration.json`（合成後の実測秒）
  カットの「画」… `tools/cuts/*.py`（章ごと。この場所だけを直せば図が変わる）
  図の部品     … `tools/titan_fig.py`（型。226カットをこの部品で組む）

■ レイヤーの命名（build_jiko がこの名前で拾う）
  {cid}_base … 地＋見出し＋章マーカー。カット頭から出ている（動かない）
  {cid}_lab  … 図の骨格。**カット前半で左→右に描かれる**
  {cid}_aN   … 図の N 段目。**その段の持ち時間いっぱいをかけて左→右に描かれる**
  {cid}_hot  … 脈打つ強調（省略可）
  実写カットは {cid}_bg（地・写真に覆われる）と {cid}_lab（写真の上）＋{cid}_aN

■ 🔴 3秒以上の静止を禁止（映像ルール4）を**構造で満たす**
  段の持ち時間 ＝ その段が出てから次の段が出るまで（最後の段はカット終わりまで）。
  段はその持ち時間いっぱいをかけて描かれるので、**カットの頭から終わりまで常に何かが動く**。
  テスト映像のようにカットごとに MOTION を手で書く必要が無くなった
  （手書きだと図を動かすたびに直し忘れる。実際 c3 のワイプ範囲で1度やっている）。

■ 🔴 写真より上に出すものは `_lab` に置く
  build_jiko は bg の上に写真を貼るので、`_bg` に置いた文字は全画面写真に丸ごと覆われる
  （21巡目に見出しが完全に消えた）。
"""
import base64
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import jiko_style as J
import titan_fig as F
import fontmetrics as fm
import render

W, H = 1920, 1080
HERE = Path(__file__).parent.parent
FONTS = Path(os.environ.get("ZUKAI_FONTS", HERE / "fonts"))
OUT = HERE / "out" / "jiko"
CSS = ""

# ── 章（章マーカーに出す名前） ────────────────────────────
# 🔴🔴 2026-08-10：**3本目「スレッシャー号」へ差し替え。**
#    ⚠️⚠️ **ここは題材を替えたら必ず書き換える。忘れると全カットの隅に
#         前作の章名が出たまま38分ぶん焼ける。** 実際に一度そうなった：
#         スレッシャー号を焼き上げたあとで、隅が「3/6 毎秒10メートルの風」
#         「4/6 15時間半」「5/6 4,500時間」「6/6 噂はどこから来たのか」＝
#         **2本目（123便）の章名のまま**だったことに気づいた（本編レンダ後）。
#    机上検査5種は**1つも落ちない**。重なりも複写も無く、文字として正しく出るため。
#    → `--report` が章名を必ず出すようにした。回すたびに目に入る（下の print）。
#    1本目（潜水艇タイタン号）の章名は git の `57e6c16`、2本目は `8b5d129` にある。
# 🔴 2026-09-05：**4本目「サーフサイド」へ差し替え**（台本第3版 §3 の章名。7章＋プロローグ＋エピローグ）。
#    3本目（スレッシャー号）の章名は git の `ad6882a` にある。
# 🔴 2026-09-07：**5本目「SL-1 原子炉暴走事故」へ差し替え**（台本第2版 §3 の章名。9章）。
#    4本目（サーフサイド）の章名は git の `3c9ff2d` にある。
# 🔴🔴 2026-09-09（⑤c）：**6本目「フランシス・スコット・キー橋 崩落」へ差し替え**
#    （台本第2版 §3 の章名。**10章**＋冒頭の引き＋締め）。
#    5本目（SL-1）の章名は git の `11d2bea` にある。
#    ⚠️⚠️ **⑤c の検品で c110 を焼くまで、隅が「1/9 北極でも動く炉」のままだった。**
#      ⑤b の門番 11本（`qa_all`）は1本も鳴っていない。門番そのものは
#      `check_final.py` に**在った**のに、`qa_all` に載っておらず**誰も回さなかった**
#      （[[feedback-gates-blind-spot-is-the-scan-direction]]＝単発で回す門番は qa_all へ）。
#      → 同じ日に `qa_all` の GATES へ `chapters` を足した。
#    ⚠️ 6本目は**10章**。`ca`（第10章）を入れ忘れると、その12カットだけ
#      章マーカーが消える（`chapter_of` が None を返す）。NCH も 9→10。
CHAPTERS = {
    "c1": (1, "キー橋という橋"),
    "c2": (2, "その夜の8人"),
    "c3": (3, "ダリという船"),
    "c4": (4, "4分9秒"),
    "c5": (5, "1分16秒"),
    "c6": (6, "橋が落ちた理由"),
    "c7": (7, "一本の線"),
    "c8": (8, "防げたのか"),
    "c9": (9, "撤去と再開"),
    "ca": (10, "何が変わったか"),
}
NCH = 10


def chapter_of(cid):
    """プロローグ（pr*）とエピローグ（ep*）は章マーカー無し。"""
    return CHAPTERS.get(cid[:2])


# ── 出典表記（ref/CREDITS.md の台帳と1対1） ───────────────
CR_NTSB = "出典：NTSB（米国運輸安全委員会）／パブリックドメイン"
CR_USCG_ROV = "出典：アメリカ沿岸警備隊／ROV撮影／パブリックドメイン"
CR_USCG_L = "出典：アメリカ沿岸警備隊／撮影 M. Leake／パブリックドメイン"
CR_NOAA = "出典：NOAA／海洋探査研究所／ロードアイランド大学／パブリックドメイン"

PHOTO_CREDIT = {
    "titan_hull_edge.jpg": CR_NTSB,
    "titan_hull_pair.jpg": CR_NTSB,
    "titan_ntsb14_endface.jpg": CR_NTSB,
    "titan_ntsb15_endpiece.jpg": CR_NTSB,
    "titan_ntsb16_wrinkle.jpg": CR_NTSB,
    "titan_ntsb16_grind.jpg": CR_NTSB,
    "titan_ntsb17_layers.jpg": CR_NTSB,
    "titan_ntsb17_voids.jpg": CR_NTSB,
    "titan_hull_inner.jpg": CR_NTSB,
    "titan_delam_ruler.jpg": CR_NTSB,
    "titan_rov_aft.jpg": CR_USCG_ROV,
    "titan_rov_tailcone.jpg": CR_USCG_ROV,
    "titan_cf_evidence.jpg": CR_USCG_L,
    "titan_titanic_bow.jpg": CR_NOAA,
    # ── 2026-08-02 追加。**PD限定をやめた**ので報告書の図を戻した ─────────
    #    方針変更は 2026-08-01（[[引き継ぎ-事故検証-タイタン号-r13試写指摘-20260801]] §5）。
    #    ⚠️ ところが**解禁したまま、捨てた素材を戻していなかった**ので、
    #      実写の比率は 12.0% → 12.7% までしか動いていなかった。
    #    ⚠️ うち図18は**出所の記載が無い＝NTSB作成＝PD**で、従来の縛りでも
    #      使えたはずの取りこぼし（図13〜18をPDと判定したとき18だけ拾い忘れた）。
    "titan_f18_delam.png": CR_NTSB,
    "titan_f01_descend.jpg": "出典：NTSB 報告書 図1（撮影：オーシャンゲート）",
    "titan_f04_lars.png": "出典：NTSB 報告書 図4（撮影：G. Comber）",
    "titan_f08_launch.png": "出典：NTSB 報告書 図8（撮影：G. Comber）",
    "titan_f09_parking.png": "出典：NTSB 報告書 図9（撮影：A. Harvey）",
    "titan_f10_mishap.png": "出典：NTSB 報告書 図10（撮影：S. Taragel）",
    "titan_f11_wreck.png":
        "出典：NTSB 報告書 図11（ROV撮影：Pelagic Research Services）",
    "titan_f12_wreck.png":
        "出典：NTSB 報告書 図12（ROV撮影：Pelagic Research Services）",
}
# 2026-07-31：titan_hull_pair.jpg は **NTSB 図13**（外面と内面の2枚組）と確認できたので
# 解禁した。報告書の画素サイズ（1609×1490）と完全一致し、図13〜18は出所表記が無い
# ＝NTSB自身の研究室撮影＝PD。使えない写真はいまは無い。
BANNED_PHOTOS = set()

# ── 本番2本目：日本航空123便（2026-08-04）──────────────────
# 🔴 1本目（NTSB）とは**権利の性質が違う**。あちらはパブリックドメインだったが、
#    運輸安全委員会は **公共データ利用規約 PDL1.0（CC BY 4.0 互換）** で、
#    「出典の明示」と「**加工した旨**」が**条件**になっている。
#    → 出典表記を画面から外した時点で条件違反になるので、
#      **168枚ぶんを1件ずつ書かず、名前から機械的に必ず作る**（書き忘れを起こさない）。
#    台帳は `ref/ja123/INDEX.md`、取り出しは `tools/extract_photos.py`。
CR_JTSB = "出典：運輸安全委員会 航空事故調査報告書 62-2（JA8119）"
JA123 = re.compile(r"^(?:a(\d))?([pf])(\d{3})\.jpg$")

# ── 解説書（`jtsb_kaisetsu.pdf`）から切り出した図と表（2026-08-04）─────────
# 🔴 報告書とは**別の文書**なので、出典表記も分ける。混ぜると
#    「報告書に書いてある」と「解説書に書いてある」の取り違えを画面が起こす
#    （台本 §2 で2件やらかしている型）。
#    名前は `tools/extract_kaisetsu.py` の CROP と対応：`kz009`→図9／`kh001`→表1。
CR_KAI = "出典：運輸安全委員会 事故調査報告書についての解説（62-2 JA8119）"
KAISETSU = re.compile(r"^k([zh])(\d{3})\.png$")
# 番号を持たない切り出しだけ、ここに1件ずつ書く。**書き忘れると KeyError で落ちる。**
KAI_EXTRA = {
    "k_keiki.png": "図11・図12",
    "k_camera.png": "10.(3) えい航式深海カメラ",
}


def kaisetsu_credit(name):
    """解説書から切り出した図・表の出典。当てはまらなければ None。"""
    n = Path(name).name
    if n in KAI_EXTRA:
        return f"{CR_KAI}{KAI_EXTRA[n]}／切出"
    m = KAISETSU.match(n)
    if not m:
        return None
    kind, num = m.groups()
    return f"{CR_KAI}{'図' if kind == 'z' else '表'}{int(num)}／切出"


def ja123_credit(name):
    """`ref/ja123/` の名前から出典表記を作る。当てはまらなければ None。

      ja123/p043.jpg   → 出典：運輸安全委員会 …（JA8119）写真-43／縮小・切出
      ja123/f012.jpg   → 同上 付図-12
      ja123/a1f003.jpg → 同上 別添1 付図-3
    """
    m = JA123.match(Path(name).name)
    if not m:
        return None
    annex, kind, num = m.groups()
    head = f"別添{annex} " if annex else ""
    return (f"{CR_JTSB}{head}{'写真' if kind == 'p' else '付図'}-{int(num)}"
            f"／縮小・切出")


# ══ 3本目（スレッシャー号）の出典 ══════════════════════════
# 🔴 **出典は撮影者・機関まで画面に出す**（ルール統合版 §3）。台帳＝`ref/CREDITS.md`。
#    ja123 と同じく、名前の規則から作る。**書き忘れると KeyError で落ちる**ので、
#    ref/thresher/ に足したファイルは必ずどれかの規則に当たるようにする。
CR_NARA_T = "出典：米国国立公文書館 NARA 289-T"          # 捜索写真アルバム41点
CR_INQ = "出典：スレッシャー号査問会記録 第9・10次公開"   # 報告書から取り出した図
CR_USN_PD = "出典：米海軍（パブリックドメイン）"

THR_ALBUM = re.compile(r"^thr_t(\d{1,2})\.jpg$")
# 🔴 2026-08-09 追加：アルバムの**ページ全体**（写真部分だけを切り出す前のもの）。
#    第6章 c630 は「ページの左上と右下に、機密指定の印を手で消した跡が残っている」
#    という話なので、**切り出した写真では跡が落ちていて出せない**。
THR_PAGE = re.compile(r"^thr_page(\d{1,2})\.jpg$")
THR_FIG = re.compile(r"^thr_fig_(.+)\.jpg$")
# 報告書の図は、どのページから切ったかまで出す（あとで照合できるように）
THR_FIG_PAGE = {
    "chart_exhibit50": ("131", "EXHIBIT 50 捜索海図"),
    "chart_redact_a": ("132", "捜索海図"),
    "chart_redact_b": ("135", "捜索海図"),
    # 🔴 2026-08-09 追加：原本（3988x2799）から書き込みの一角だけを切り出したもの。
    #    2600px 版から寄ると 8倍に伸びるが、原本から切れば 1.2〜1.8倍で足りる。
    "chart_redact_b2": ("135", "捜索海図　書き込みの一角"),
    "chart_c": ("133", "捜索海図"),
    "table_thresher": ("490", "TABLE I 緊急浮上試験"),
    "table_permit": ("491", "TABLE 2 緊急浮上試験（PERMIT）"),
    "log_cover": ("119", "SKYLARK 報告 表紙"),
    "log_p1": ("120", "経過記録"),
    "log_p2": ("121", "経過記録"),
    "log_p3": ("122", "経過記録"),
}
# Commons の 330-PSA は撮影番号が名前に入っているので、そこまで出す
THR_PSA = re.compile(r"^cm_(330-PSA-[\w-]+?)__")
THR_CM = {
    "cm_SSN593_service_entering.jpg": f"{CR_USN_PD}　USS THRESHER (SSN-593)",
    "cm_USN_1048964_USS_Thresher__SSN-593_.jpg":
        f"{CR_USN_PD}　USN 1048964（造船所）",
    "cm_USS_Thresher__SSN-593_.jpg": f"{CR_USN_PD}　USS THRESHER (SSN-593)",
    "cm_USS_Thresher__SSN-593__bow.jpg": f"{CR_USN_PD}　艦首",
    "cm_USS_Thresher__SSN-593__bow__cropped_.jpg": f"{CR_USN_PD}　艦首／切出",
    "cm_anp_thresher_1963.jpg": f"{CR_USN_PD}　1963年",
    "nara_428-N-1057645.jpg": "出典：米国国立公文書館 NARA 428-N-1057645（米海軍撮影）",
}


def thresher_credit(name):
    """`ref/thresher/` の名前から出典表記を作る。当てはまらなければ None。

      thr_t24.jpg              → 出典：NARA 289-T-24（米海軍／NRL・MIZAR 撮影）
      thr_fig_chart_redact_b   → 出典：査問会記録 第9・10次公開 135ページ 捜索海図
      cm_330-PSA-309-64a__…    → 出典：米海軍 330-PSA-309-64a（パブリックドメイン）
    """
    n = Path(name).name
    if n in THR_CM:
        return THR_CM[n]
    m = THR_ALBUM.match(n)
    if m:
        return (f"{CR_NARA_T}-{int(m.group(1))}"
                f"（米海軍／NRL・MIZAR ほか撮影・1964年編纂）")
    m = THR_PAGE.match(n)
    if m:
        return (f"{CR_NARA_T}-{int(m.group(1))}"
                f"（アルバムのページ全体・米海軍／NRL・MIZAR ほか撮影・1964年編纂）")
    m = THR_FIG.match(n)
    if m:
        key = m.group(1)
        if key not in THR_FIG_PAGE:
            return None                  # 🔴 黙って通さない。KeyError で気づかせる
        page_no, what = THR_FIG_PAGE[key]
        return f"{CR_INQ} {page_no}ページ　{what}／切出"
    m = THR_PSA.match(n)
    if m:
        return f"{CR_USN_PD}　{m.group(1)}"
    return None


# ══ 4本目（サーフサイド）の出典 ══════════════════════════
# 🔴 素材は3種。すべて NIST（米国立標準技術研究所）の職務著作＝パブリックドメイン。台帳＝`ref/CREDITS.md`。
#   tf_pNNN_*.jpg … 技術的知見（2026-06-22 公表・77分の4K動画）のスライドを1コマ抜いて切り出したもの
#   fb_<cid>.jpg  … 記録映像（B-Roll）の**ひかえの静止画**。動画のコマが取れたときは動画の出典が勝つ
#   ss_*.jpg      … 記録映像から**わざと**1コマ抜いた静止画（空撮など、動画のままでは短すぎる場面）
# ⚠️ ここに当たらない名前は None を返し、最後の PHOTO_CREDIT で KeyError にして気づかせる。
CR_TF = "出典：NIST 技術的知見（2026年6月22日公表）"
TF_SLIDE = re.compile(r"^surfside/tf_p(\d{3})_.+\.jpg$")
SS_FALLBACK = re.compile(r"^surfside/fb_([a-z]{1,2}\d{2,3})\.jpg$")   # c106 / pr01 / ep16
SS_STILL = {
    "surfside/ss_b2_87park.jpg":
        "出典：NIST 記録映像 B-Roll #2（空撮）の1コマ／パブリックドメイン",
    "surfside/ss_b1_sign.jpg":
        "出典：NIST 記録映像 B-Roll #1（建物の銘板）の1コマ／パブリックドメイン",
}


def surfside_credit(name):
    """`ref/surfside/` の名前から出典表記を作る。当てはまらなければ None。"""
    if name in SS_STILL:
        return SS_STILL[name]
    m = TF_SLIDE.match(name)
    if m:
        return f"{CR_TF} スライド{int(m.group(1))}ページ／パブリックドメイン／切出"
    m = SS_FALLBACK.match(name)
    if m:
        try:
            import footage as FO
            c = FO.credit_of(m.group(1))
        except Exception:                                # noqa: BLE001
            c = None
        return (c + "（静止画）") if c else None
    return None


# ══ 5本目（SL-1 原子炉暴走事故）の出典 ════════════════════
# 🔴 素材は4種。すべてパブリックドメイン。台帳＝`ref/CREDITS.md`。取り出しは `tools/sl1_assets.py`。
#   ido_pNNN_*.png / i11_* / anl_* / aec_* / fr_*  … 報告書・官報のページを PNG に焼いたもの
#   haer_NN.jpg   … HAER No. ID-33-D の記録写真（米議会図書館）
#   fb_<cid>.jpg  … 記録映画の**ひかえの静止画**。動画のコマが取れたときは動画の出典が勝つ
# 🔴 **画面に出すのは印字ページ**（PDF ページではない）。IDO-19302 は PDF ＝ 印字 ＋ 11 なので、
#    ファイル名の数字（印字）をそのまま出す。混ぜると出典が1ページずれる。
# ⚠️ ここに当たらない名前は None を返し、最後の PHOTO_CREDIT で KeyError にして気づかせる。
CR_IDO02 = "出典：IDO-19302（米原子力委員会アイダホ支所・1962）"
CR_IDO11 = "出典：IDO-19311（米原子力委員会／ゼネラル・エレクトリック・1962）"
CR_ANL = "出典：ANL-6692（アルゴンヌ国立研究所・1962）"
CR_AEC_BD = "出典：米原子力委員会 SL-1 事故 調査委員会報告（1961年6月）"
CR_FR = "出典：連邦官報 36 FR 3258（1971年2月20日）／10 CFR 50 付録A"
CR_HAER = "出典：米議会図書館 HAER ID-33-D"

SL1_PAGE = re.compile(r"^sl1/(ido|i11|anl|aec|fr)_p([0-9a-z]+)_[a-z0-9]+\.png$")
SL1_HAER = re.compile(r"^sl1/haer_(\d{2})\.jpg$")
SL1_FB = re.compile(r"^sl1/fb_([a-z]{1,2}\d{2,3})\.jpg$")
# 🔴 ファイル名の数字は**そのファイルの印字ページ**。画面に出す形はここで決める
#    （`i11` は印字が「ii」「I-5」なのでページ番号を作れない＝名指しで持つ）。
SL1_PRINTED = {
    ("ido", "vii"): "p.vii", ("ido", "004"): "p.4", ("ido", "013"): "p.13",
    ("ido", "014"): "p.14", ("ido", "015"): "p.15", ("ido", "016"): "p.16",
    ("ido", "017"): "p.17", ("ido", "018"): "p.18", ("ido", "019"): "p.19",
    ("ido", "020"): "p.20", ("ido", "021"): "p.21", ("ido", "022"): "p.22",
    ("ido", "023"): "p.23", ("ido", "035"): "p.35", ("ido", "036"): "p.36",
    ("ido", "090"): "p.90", ("ido", "091"): "p.91", ("ido", "095"): "p.95",
    ("ido", "096"): "p.96", ("ido", "100"): "p.100",
    ("ido", "101"): "p.101", ("ido", "103"): "p.103",
    ("i11", "004"): "要旨 ii", ("i11", "019"): "I-5",
    ("anl", "001"): "表紙", ("anl", "038"): "p.36",
    ("aec", "001"): "表紙", ("fr", "3258"): "3258ページ",
}
SL1_DOC = {"ido": CR_IDO02, "i11": CR_IDO11, "anl": CR_ANL,
           "aec": CR_AEC_BD, "fr": CR_FR}


def sl1_credit(name):
    """`ref/sl1/` の名前から出典表記を作る。当てはまらなければ None。"""
    m = SL1_PAGE.match(name)
    if m:
        doc, pg = m.group(1), m.group(2)
        pr = SL1_PRINTED.get((doc, pg))
        if pr is None:                       # 🔴 表に無いページは黙って通さない
            return None
        tail = "" if doc == "fr" else f" {pr}"
        return f"{SL1_DOC[doc]}{tail}／パブリックドメイン"
    m = SL1_HAER.match(name)
    if m:
        return f"{CR_HAER}-{int(m.group(1))}／パブリックドメイン"
    m = SL1_FB.match(name)
    if m:
        try:
            import footage as FO
            c = FO.credit_of(m.group(1))
        except Exception:                                # noqa: BLE001
            c = None
        return (c + "（静止画）") if c else None
    return None


# ══ 6本目（フランシス・スコット・キー橋 崩落）の出典 ════════
# 🔴 素材は3種。台帳＝`ref/CREDITS.md` の「⑤b に作った素材」。取り出しは `tools/keybridge_assets.py`。
#   kb_p<印字>_fig<図番>.png … NTSB MIR-25-40 のページを PNG に焼いたもの（PD、17 U.S.C. §105）
#   kb_pre_* / kb_bld_*.jpg  … Commons の写真。**PD と CC BY だけ**（CC BY-SA は採っていない）
#   fb_<cid>.jpg             … 動画の**ひかえの静止画**。動画のコマが取れたときは動画の出典が勝つ
# 🔴 **画面に出すのは印字ページ**（PDF ではない）。ファイル名の数字がそのまま印字ページ。
# ⚠️ CC BY は**表示が条件**なので、撮影者名を落とすと条件を満たさない。ここで名前まで持つ。
# ⚠️ ここに当たらない名前は None を返し、最後の PHOTO_CREDIT で KeyError にして気づかせる。
CR_MIR2540 = "出典：NTSB 事故調査報告 MIR-25-40"

KB_PAGE = re.compile(r"^keybridge/kb_p(\d{3})_fig(\d{2})\.png$")
KB_FB = re.compile(r"^keybridge/fb_([a-z]{1,2}\d{2,3})\.jpg$")
KB_PHOTO = {
    "kb_pre_1976": "The Evening Sun（1976年8月11日）／パブリックドメイン",
    "kb_pre_harbor07": "Frenchcheesemuseum（2007年2月24日）／パブリックドメイン",
    "kb_pre_navy12": "米海軍 Jeremy Johnson 上等兵曹（2012年6月13日）／パブリックドメイン",
    "kb_pre_oakhill14": "米海軍（2014年9月10日）／パブリックドメイン",
    "kb_pre_catlett22": "米陸軍工兵隊 Greg Nash（2022年4月20日）／パブリックドメイン",
    "kb_pre_deck05": "Brent Moore（2005年6月30日）／CC BY 2.0",
    "kb_pre_2019": "Rafael Saldaña（2019年9月16日）／CC BY 2.0",
    "kb_bld_harbor": "米国立公文書館 546833／パブリックドメイン",
    "kb_bld_piers": "米国立公文書館 546837／パブリックドメイン",
    "kb_bld_supports": "米国立公文書館 546929／パブリックドメイン",
    "kb_bld_curtis": "米国立公文書館 546911／パブリックドメイン",
}


def keybridge_credit(name):
    """`ref/keybridge/` の名前から出典表記を作る。当てはまらなければ None。"""
    m = KB_PAGE.match(name)
    if m:
        return f"{CR_MIR2540} p.{int(m.group(1))}（図{int(m.group(2))}）／パブリックドメイン"
    m = KB_FB.match(name)
    if m:
        cid = m.group(1)
        try:
            import footage as FO
            c = FO.credit_of(cid)
        except Exception:                                # noqa: BLE001
            c = None
        if c:
            return c + "（静止画）"
        # 🔴 **黙って通さない。**ひかえの静止画は動画の出典を借りているので、
        #    `footage.USE` に欄が無ければ出せる出典が無い＝出所を偽ることになる。
        raise RuntimeError(
            f"{cid}: 実写のカットだが `footage.USE` に欄が無い。"
            f"⑤b で `ref/keybridge/SHOTS_INDEX.md` からショットの境目を写して足すこと")
    if name.startswith("keybridge/"):
        stem = name.split("/", 1)[1].rsplit(".", 1)[0]
        cr = KB_PHOTO.get(stem)
        if cr:
            return "出典：" + cr
    return None


def credit_of(cid, spec):
    """そのカットに出す出典。**動画を当てたカットは動画の出典を出す。**

    🔴 2026-08-01：動画を差し込むとき、静止画の出典（NTSB／PD）をそのまま
       出してしまうと**出所を偽ることになる**。ROV映像は沿岸警備隊の公開資料だが
       撮影は Pelagic Research Services で、パブリックドメインではない。
       検証番組で出所を偽ると、内容そのものの信用が落ちる。
    """
    try:
        import footage as FO
        c = FO.credit_of(cid)
        if c and FO.have(cid):
            return c
    except Exception:                                    # noqa: BLE001
        pass
    cr = (keybridge_credit(spec["photo"]) or sl1_credit(spec["photo"])
          or surfside_credit(spec["photo"])
          or thresher_credit(spec["photo"]) or kaisetsu_credit(spec["photo"])
          or ja123_credit(spec["photo"]) or PHOTO_CREDIT[spec["photo"]])
    # 🔴 階調を伸ばした写真は、そのことを出典の行に出す（2026-08-09）。
    #    切り抜きに「／切出」と付けているのと同じ扱い。黙って手を入れない。
    if spec.get("levels") or LEVELS_BY_PHOTO.get(spec["photo"]):
        cr += "・濃淡補正"
    # 🔴 2026-09-09（6本目キー橋 ⑤c'・持ち越し §7）：**CC BY は帰属だけでは足りない。**
    #    CC BY 2.0 §4(b) は、改変して使うときに**改変した旨を示すこと**も条件にしている。
    #    この動画は写真を全部デュオトーンにし（`build_jiko.duotone`＝`convert("L")` から
    #    2色に置き換え）、枠に合わせて切り出している＝**CC BY の6カットは全部が改変物**
    #    （`c101` `c106` `c112` `c201` `c213` `ep06`。素材は `kb_pre_2019` と
    #     `kb_pre_deck05` の2点）。それなのに画面には
    #    「出典：Rafael Saldaña（2019年9月16日）／CC BY 2.0」としか出ていなかった。
    #    ⚠️ PD の素材には足さない。同じ断りを付けると、**表示の義務が無いものにも
    #      あるように見える**（PD は 40カット以上ある）。
    #    ⚠️ 「濃淡補正」と同じ扱い＝**黙って手を入れない**。
    if "CC BY" in cr and "改変" not in cr:
        cr += "／改変：色調変更・切出"
    return cr


def face_css(name, filename):
    b = base64.b64encode((FONTS / filename).read_bytes()).decode()
    return (f"@font-face{{font-family:'{name}';src:url(data:font/woff2;base64,{b}) "
            f"format('woff2');font-weight:400;font-display:block;}}")


def page(inner, w=W, h=H):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}">{inner}</svg>')
    return (f'<html><head><meta charset="utf-8"><style>*{{margin:0}}{CSS}'
            f'body{{width:{w}px;height:{h}px;overflow:hidden}}</style></head>'
            f'<body>{svg}</body></html>')


# ── 字幕 ─────────────────────────────────────────────────
# 黒帯の上・38px・NotoSansJP-Bold・全カット統一（映像ルール1）。帯は y=900〜1080。
SUB_Y, SUB_H = 900, 180
SUB_SIZE = 38
SUB_MAXW = 1560          # 字幕1行に許す最大の幅（px）。**実測で折る**
XML = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}


def esc(t):
    return "".join(XML.get(c, c) for c in t)


def wrap2(text):
    """字幕は**2行まで**。折る位置は読点。無ければ幅の中央に近い文字境界。

    🔴 「26字」で折っていたのを**実測幅（px）**に変えた。
       字幕は漢字・かな・数字が混ざるので、字数で折ると1行の長さが 1.6 倍ぶれる
       （「2023年6月18日、午前10時47分。」は16字だが数字が多く、
         「潜水艇は、原型をとどめていなかった。」の18字より狭い）。
    """
    if fm.width(text, SUB_SIZE, "Noto") <= SUB_MAXW:
        return [text]
    half = fm.width(text, SUB_SIZE, "Noto") / 2
    best, acc = None, 0.0
    cands = []
    for i, ch in enumerate(text):
        acc += fm.adv(ch, "Noto") * SUB_SIZE
        if ch in "、。":
            cands.append((abs(acc - half), i + 1))
        if best is None or abs(acc - half) < best[0]:
            best = (abs(acc - half), i + 1)
    cut = min(cands)[1] if cands else best[1]
    return [text[:cut], text[cut:]]


def sub_band(w=W, h=SUB_H):
    """★字幕の黒帯だけ。**文字とは別の1枚**にして、常時貼りっぱなしにする。

    🔴 2026-07-31（試写の指摘③）：それまで帯と文字を1枚のPNGに焼いていたので、
       字幕が変わるたびに**帯までいっしょにフェードして画面がちらついた**。
       帯を分けて常時表示にすれば、消えるのは文字だけになる。
    ⚠️ 帯は**全カット共通**なので焼くのは1枚（`_subband`）。226枚焼かない。
    ⚠️ 図の本体は y=210〜892（jiko_style の BAND_T / BAND_B）に収まっていて、
       帯は y=900 から下。**常時出しても図に一切かからない**（確認済み）。
    """
    return (f'<linearGradient id="subbg" x1="0" y1="1" x2="0" y2="0">'
            f'<stop offset="0" stop-color="#000" stop-opacity="0.78"/>'
            f'<stop offset="0.62" stop-color="#000" stop-opacity="0.70"/>'
            f'<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="url(#subbg)"/>')


def sub_row(text, w=W, h=SUB_H):
    """字幕1枚ぶんの**文字だけ**。1行なら下寄せ、2行なら上下に振り分ける。

    ⚠️ 帯はここに含めない（`sub_band()` が別に持つ）。太いフチは残す
       ── 帯があっても、明るい写真の上では文字がフチで持っている。
    """
    lines = wrap2(text)
    ys = [h * 0.64] if len(lines) == 1 else [h * 0.42, h * 0.78]
    g = []
    for t, y in zip(lines, ys):
        g.append(f'<text x="{w / 2:.0f}" y="{y:.0f}" font-family="Noto" '
                 f'font-size="{SUB_SIZE}" fill="{J.INK_W}" text-anchor="middle" '
                 f'stroke="#000" stroke-width="7" stroke-linejoin="round" '
                 f'paint-order="stroke fill">{esc(t)}</text>')
    return "".join(g)


def sub_strip(lines):
    return "".join(f'<g transform="translate(0,{i * SUB_H})">{sub_row(t)}</g>'
                   for i, t in enumerate(lines))


# ── 実写カットの型：全画面 ────────────────────────────────
PHOTO_FULL = (0, 0, W, H)
SCRIM_TOP = 300
CRED_Y = 872
CRED_BACK_Y = 196       # 写真を地に敷くカットの出典（右上・本体枠の上）
# 🔴 quote の札（x 92〜562）の右・決め所の左端。ここから出典を書くと
#    札の中の原文とも、閉じ括弧（x 1682〜1802）とも当たらない（`check_layout` で確認）
CRED_BACK_X = 632
CRED_BACK_W = 1682 - CRED_BACK_X        # 閉じ括弧「」」の左端（1682）までの幅
BAND_CY = 560           # 帯写真の縦中心


# ── ★額装パネル（2026-08-04・本番2本目のために追加）───────────
# 🔴 **報告書のスキャンは 1ビット（2値・JBIG2）で、全画面に置けない。**
#    中間調が1階調も無く、濃淡はすべて誤差拡散ディザ（網点）。1920px へ伸ばすと
#    砂目がそのまま出て、写真として読めない（2026-08-03 に実写して確認）。
#    → **長辺1200px以下の枠に収めて出す**と、ディザが階調に戻って写真になる。
#    ⚠️ 1本目の「実写カットは全画面／写真を箱に入れる作りは廃止」は、
#      **この題材では成立しない。** 素材の性質が違う（PDF スキャン vs デジタル写真）。
#    ⚠️ 縮小は取り出しの時点で済ませてある（`tools/extract_photos.py --cap 1200`）。
#      ここでやるのは**置き場所**だけ。
# 🔴 高さは本体枠から **出典1行ぶん（34px）を引いて**おく。
#    引かないと額装が y=892 まで届き、出典を右上（副題と同じ帯）へ逃がすことになって
#    **長い副題と重なる**（123便で7件検出）。出典は額の真下に置くのが正しい。
PANEL_MAXW, PANEL_MAXH = 1120, J.BAND_B - J.BAND_T - 34   # 1120 × 648
PANEL_GAP = 56                                       # 写真と注記のあいだ
# 🔴 注記の段と段のあいだ（字面どうし）。台帳 §Y-5 の `c908` で
#    **段内 16px 対 段間 22.6px** ＝ 6px しか違わず、3段が1つのかたまりに見えていた。
#    ⚠️ 狭いところだけ広げる（広い段はそのまま。詰めると下の空きが増える）。
BLOCK_GAP = 34
# 🔴 注記の「ラベルの墨の下」と「答えの墨の上」のすき間（台帳 §Y-2 の実測から）。
#    `vs=88` の段は 10〜15px あって読めていて、`vs=96` の 6px は「縁取りが食い込む」。
#    ⚠️ ここは**墨どうし**の値。縁取り（BG 色）はこの外へさらに 6〜9px ずつ広がる。
V_GAP = 12
PANEL_CRED_Y = J.BAND_B - 4                          # 額の下に出す出典の位置


def photo_box(spec):
    """写真の置き場所。**額装パネル**か、帯か、全画面か。

    🔴 NTSB の標本写真は 1431×325 のように細長いものが多い。
       全画面（1920×1080）に覆わせると **3.3倍に引き伸ばして左右を切り落とす**ことになり、
       ぼやけたうえに写真の意味（層が並んでいる様子）が消える。
       帯なら原寸に近い倍率で、横方向の情報を全部見せられる。
    """
    if spec.get("panel"):
        from PIL import Image
        with Image.open(HERE / "ref" / spec["photo"]) as im:
            sw, sh = im.size
        # 🔴 2026-08-06（r11 の拡大目視）：**切り出しを勘定に入れていなかった。**
        #    額の箱を「切る**前**の縦横比」で作り、そこへ切ったあとの画像を
        #    `build_jiko.fit()` が**覆い**（cover）ではめる。だから
        #    画素で測って切った端が、もう一度切り落とされていた。
        #    実測（8カット）：ep05 30.8%・ep06 24.2%・c233/c330 19.1%・
        #    c230/c333 17.0%・c222 14.1%・c136 38.1% を失っていた。
        #    c136 では**尾部が枠の外に出て、生存者の斜線が4席のうち3席しか映らなかった**
        #    （見出しは「4人」なので、図が数を裏切る）。
        #    → 箱は**切ったあとの縦横比**で作る。そうすれば覆いは等倍になり何も落ちない。
        t = spec.get("trim") or TRIM_BY_PHOTO.get(spec["photo"])
        if t:
            sw = max(1, int(sw * (t[2] - t[0])))
            sh = max(1, int(sh * (t[3] - t[1])))
        mw = spec.get("pw", PANEL_MAXW)
        z = min(mw / sw, PANEL_MAXH / sh)
        w, h = int(sw * z), int(sh * z)
        # 注記は写真の**反対側**に置く（side は注記を出す側）
        if spec.get("side", "right") == "right":
            x = J.MG
        else:
            x = J.RIGHT - w
        if not spec.get("ann"):
            x = (W - w) // 2                 # 注記が無いカットは真ん中
        return (x, J.BAND_T + (PANEL_MAXH - h) // 2, w, h)
    if not spec.get("band"):
        return PHOTO_FULL
    from PIL import Image
    with Image.open(HERE / "ref" / spec["photo"]) as im:
        sw, sh = im.size
    h = min(int(W * sh / sw), 720)
    return (0, int(BAND_CY - h / 2), W, h)


def full_bg():
    """全画面写真カットの地。**ここには何も置けない**（写真が全面で乗る）。"""
    return J.frame(W, H)


def full_top(cid, spec):
    """写真の上に載せる一式（暗幕・見出し・章マーカー・出典）。`_lab` に入れる。"""
    side = spec.get("side", "right")
    if spec.get("band") or spec.get("panel"):
        # 帯・額装のときは見出しも注記も**写真の外**に置けるので、暗幕は要らない
        g = []
    else:
        g = [J.scrim(0, 0, W, SCRIM_TOP, "top", 0.80)]
        if side == "right":
            g.append(J.scrim(1150, 0, W - 1150, H, "right", 0.62))
        else:
            g.append(J.scrim(0, 0, 770, H, "left", 0.62))
    if spec.get("panel"):
        # ★額装の縁。**写真の外周1本だけ**。図解の罫と同じ色にして、
        #   「資料を1枚貼ってある」と読めるようにする（枠が無いと地に溶ける）。
        x, y, w, h = photo_box(spec)
        g.append(f'<rect x="{x - 3}" y="{y - 3}" width="{w + 6}" height="{h + 6}" '
                 f'fill="none" stroke="{J.LINE}" stroke-width="3"/>')
    g.append(J.title(spec["t"], spec.get("s", "")))
    ch = chapter_of(cid)
    if ch:
        g.append(J.chapter(ch[0], NCH, ch[1]))
    # 🔴 出典の置き場所。全画面写真は写真の上（y=872）でよいが、
    #    額装は写真の外に地が見えているので、**図解カットと同じ右上**へ置く。
    #    写真の上に重ねると、額の中に文字が入って「資料に書き込んだ」ように見える。
    if spec.get("panel"):
        # 額の**真下**の空き帯に、画面の右余白でそろえて出す。
        # ⚠️ 額の右端に合わせると、額が左寄せのカットで**文字が画面の外へ出る**
        #    （出典は約1,000px あるので、額の右端が 972px だと左端が -28 になる）。
        g.append(J.outlined(J.RIGHT, PANEL_CRED_Y, credit_of(cid, spec),
                            J.LINE, 24, anchor="end", sw=5))
    else:
        g.append(J.outlined(J.MG, CRED_Y, credit_of(cid, spec), J.LINE, 24, sw=5))
    return "".join(g)


def photo_ann(spec):
    """実写カットの注記。**4〜6ブロックまで**（全画面では多いと邪魔になる）。

    ann … [dict(t="巡航高度", v="7,300 m", c=J.AMBER)] を上から積む。
    """
    side = spec.get("side", "right")
    x = J.RIGHT if side == "right" else J.MG
    anchor = "end" if side == "right" else "start"
    maxw = 700
    if spec.get("band"):
        # 帯写真の注記は写真の下に横並びで置く（写真の上に載せない）
        x = J.MG if side != "right" else J.RIGHT
        maxw = 1500
    y = spec.get("ann_y", 340)
    if spec.get("panel"):
        # ★額装のときは、注記は**写真の外**の残った幅に収める。
        #   写真の上に載せると、報告書の資料に書き込んだように見える。
        px, _py, pw, _ph = photo_box(spec)
        if side == "right":
            maxw = J.RIGHT - (px + pw + PANEL_GAP)
        else:
            maxw = (px - PANEL_GAP) - J.MG
        y = spec.get("ann_y", J.BAND_T + 34)
    out = []
    last_bot = None                  # 直前に描いた字面の下端（段と段のあいだを測るため）
    for a in spec.get("ann", []):
        # 🔴 2026-09-06（⑤c' 直す #2）：**段ごとに縦へずらせるようにした**。
        #   なぜ：スライドの箇条を指して「1つめ／2つめ／3つめ」と言うカット
        #   （c714 c716 c718 c719・ep02〜ep05）で、**どれが N つめか画面に印が無い**。
        #   型に「箇条の1行だけ明るくする」手段は無く（写真カットは J.outlined＝
        #   <text> しか描かない）、`ann_y` は**注記のかたまり全体**しか動かせなかった。
        #   → 注記を、指している行と**同じ高さ**に置けるようにするのがいちばん安い。
        #   ⚠️ ずらしすぎると枠外に出る＝`check_layout` が落とす（門番は既にある）。
        y += a.get("dy", 0)
        s = []
        ts = 0.0
        dsize = 0.0
        # 🔴 2026-09-09（6本目キー橋 ⑤c'・型⑩「ラベルより中身が小さい」）：
        #    **`v` が無い段では `d` が答えそのもの**なのに、ラベル（`ts` 46）より
        #    小さい（`ds` 26〜34）ので、**問いのほうが大きく明るい**画になっていた。
        #    実測 61組・47カット（`c101`「渡していたもの」46px 対
        #    「パタプスコ川とボルチモア港の出口」32px を原寸で確認）。
        #    ⚠️ `v` がある段の `d` は本当の補足なので触らない（17組はそのまま）。
        #    ⚠️ 引き継ぎは「型⑩は `titan_fig.panel()` の cap 140/76 で直る」と
        #      書いていたが、測ると別の場所だった。`panel` 側で値が小さいのは
        #      `c808` の1件だけ（46 対 44）。
        # 🔴 2026-09-10（⑤c' 2巡目・§S-2）：**上の直しは「同じ大きさ」で止まっていた。**
        #    `fit` は幅で縮めるので、長い答えはラベル 46 まで上がりきらず
        #    **6組が今もラベルより小さい**（`c904` 35対46・`pr01` 38・`c101` `c110`
        #    `c409` `c516` が 43）。答えを上げられないなら**ラベルを下げる**。
        #    → 答えの級数を先に出し、ラベルの上限にする（`min`）。
        d_is_answer = bool(a.get("d")) and not a.get("v")
        if a.get("t"):
            ts = fm.fit(a["t"], maxw, "Noto", cap=a.get("ts", 46), floor=24)
        if d_is_answer:
            dsize = fm.fit(a["d"], maxw, "Noto",
                           cap=max(a.get("ds", 34), ts), floor=22)
            if ts:
                ts = min(ts, dsize)
        lab_bot = None
        if a.get("t"):
            # 🔴 2026-09-10（⑤c' 4巡目・台帳 §Y-5 `c908`）：**段の切れ目が読めなかった。**
            #    実測（`c908`）＝ **段内 16px 対 段間 22.6px**。6px しか違わないので、
            #    3つの段が9行の1つのかたまりに見える。
            #    ⚠️ 段間は本番でも **22.6〜90.5px** とばらばら（`d` の有無と級数で決まる）。
            #    → **狭いところだけ広げる**。広い段はそのまま（詰めると下の空きが増える）。
            #    ⚠️ V_GAP と同じで `max` の片側だけ動かす。全部そろえる直しは採らない。
            if last_bot is not None:
                want = last_bot + BLOCK_GAP + fm.ink(str(a["t"]), ts, "Noto")[0]
                y = max(y, want)
            s.append(J.outlined(x, y, a["t"], a.get("c", J.INK_W), ts, anchor,
                                sw=max(6, ts * 0.17)))
            lab_bot = last_bot = y + fm.ink(str(a["t"]), ts, "Noto")[1]
            y += ts + 18
        d_top = None
        if a.get("v"):
            size = fm.fit(a["v"], maxw, "Dela", cap=a.get("vs", 96), floor=30)
            vbase = y + size * 0.20
            # 🔴🔴 2026-09-10（⑤c' 4巡目・台帳 §Y-1-3／§Y-2）：
            #    **ラベルの墨と答えの墨が重なっていた。** `pr08`（`vs=112`）で実測 **-3px**。
            #    真因はこの `vbase = y + size * 0.20`。答えの字面の上端は
            #    `vbase - ink()[0]` ＝ **y より 0.5〜0.6級数ぶん上**に来るので、
            #    **級数を上げるほど答えが上のラベルへ食い込む**（送り `y` は級数に依らない）。
            #    実測（墨どうし・色で分けて測った台帳 §Y-2 と一致）：
            #      120px `pr01` -4.7 ／ 112px `pr08` -4.3 ／ 104px 0〜2 ／ 96px 6 ／ 88px 10〜15
            #    ＝ **26カット29組**が該当。1枚ずつ触らず、ここで1回で直す。
            #    → 字面で置く：**ラベルの字面の下から V_GAP 下に、答えの字面の上**が来る。
            #    ⚠️ 下へずらしたぶんは `y` にも足す（次の段との間隔を変えないため）。
            #    ⚠️ 上へは動かさない（`max(0, …)`）。空きが広い段はそのまま。
            if lab_bot is not None:
                want = lab_bot + V_GAP + fm.ink(str(a["v"]), size, "Dela")[0]
                drop = max(0.0, want - vbase)
                vbase += drop
                y += drop
            s.append(J.outlined(x, vbase, a["v"], a.get("vc", J.AMBER),
                                size, anchor, sw=max(7, size * 0.15), family="Dela"))
            last_bot = vbase + fm.ink(str(a["v"]), size, "Dela")[1]
            if a.get("d"):
                # 🔴 2026-09-10（⑤c' 2巡目・§R-14）：**補足が、自分の答えより
                #    「下の見出し」に近い**（実測 11カット。上 59〜86px 対 下 24〜28px）。
                #    真因は `y += size + 26` が**級数ぶん**送ること。Dela の数字は
                #    字面が級数よりずっと低いので、級数の大きい段ほど下が空く。
                #    ⚠️ `fm.ink()` で**字面の下端**を実測して送る（比の決め打ちはしない）。
                #    ⚠️ ここで送る `y` は「次の**字面の上**」なので、`d` 側で
                #      字面の上端ぶん足してベースラインへ直す。
                #    ⚠️ 26 だと「下の見出しまで 24〜26px」と**並んで**しまい、
                #      どちらの組か決められない（1回それで直したつもりになった）。
                #      補足は自分の答えのほうへ寄せる ＝ **下より狭い 16**。
                d_top = vbase + fm.ink(str(a["v"]), size, "Dela")[1] + 16
            y += size + 26
        if a.get("d"):
            size = dsize or fm.fit(a["d"], maxw, "Noto",
                                   cap=a.get("ds", 34), floor=22)
            if d_top is not None:
                y = d_top + fm.ink(str(a["d"]), size, "Noto")[0]
            s.append(J.outlined(x, y, a["d"], a.get("dc", J.LINE), size, anchor,
                                sw=max(5, size * 0.17)))
            last_bot = y + fm.ink(str(a["d"]), size, "Noto")[1]
            y += size + 16
        y += 22
        out.append("".join(s))
    return out


# ── 図解カットの地 ────────────────────────────────────────
# ★写真を地に敷くときの暗幕の濃さ（2026-07-31 試写の指摘④）。
#   ⚠️ **推定で置かない。** `tools/check_veil.py` が、写真ごとに
#      「図のいちばん細い色と地とのコントラスト比」を測って必要な濃さを出す。
#      ここは既定値で、カットごとに `veil=` で上書きできる。
# 2026-08-01 カズヤくんが見比べ画像の**5段目**を指定 → **0.76**。
# 実測では 0.76 で「図の読みやすさ 0.37／写真の見え L*20」。
# ⚠️ 机上の基準（0.50）は下回るが、**実物を見たうえでの判断**なのでこちらを採る。
#    机上の基準は「焼く前に候補を絞る」ための道具であって、目より上位ではない。
VEIL = float(os.environ.get("ZUKAI_VEIL", 0.76))


def fig_base(cid, spec, ground=True):
    """図解カットの地。

    ground=False … 写真を地に敷くカット。**不透明な地を置かない**（写真が隠れる）。
                   代わりに方眼だけ薄く残し、出典表記を必ず出す。
    """
    if ground:
        g = [J.frame(W, H)]
    else:
        # 🔴🔴 2026-09-07（5本目 SL-1 ⑤c'・L-30/L-37）：**出典を下（y=872）へ戻した。**
        #    それまでは右上 y=196 に置いていたが、原寸で見ると
        #    **見出し帯の中に出て、ほかのカットの y≒862 と揃っていない**（10カットで確認）。
        #    ⚠️ 旧コメントの「y=872 に置いたら図の文字と重なった（c115a c628）」は
        #      **2本目の型の話**で、いまここを通るのは `quote` だけ（実測 14/14）。
        #      quote の札は card_y 240＋card_h 612 ＝ 底 852、決め所は縦中央で
        #      いちばん下でも y≒726。**y=872 は空いている**（`check_layout` で確認）。
        #    ⚠️ 型が増えて quote 以外がここを通るようになったら、右上へ戻す必要がある。
        #      それを人の記憶に頼らないよう、**型を見て分ける**（下の cred_y）。
        #    ⚠️ 左端（x=72）に置くと**札の下の原文（ctx）と重なる**（c121 319×15px・
        #      c915 94×19px を `check_layout` が検出）。札は x 92〜562 なので、
        #      **札の右**（決め所の左端と同じ x=632）から書く。右端に寄せると
        #      閉じ括弧「」（x 1682〜1802・y 772〜892）に当たる。
        #    ⚠️ 長い出典（IDO-19311 の行は 24px で 1,120px）はそのままだと括弧に届く。
        #      **入る大きさに落として書く**（式で決める。目で詰めない）。
        _fig = (spec.get("fig") or ("", None))[0]
        if _fig == "quote":
            _c = credit_of(cid, spec)
            _sz = fm.fit(_c, CRED_BACK_W, "Noto", cap=24, floor=17)
            g = [J.grid_only(W, H),
                 J.outlined(CRED_BACK_X, CRED_Y, _c, J.LINE, _sz, sw=5)]
        else:
            g = [J.grid_only(W, H),
                 J.outlined(J.RIGHT, CRED_BACK_Y, credit_of(cid, spec),
                            J.LINE, 24, anchor="end", sw=5)]
    g.append(J.title(spec["t"], spec.get("s", "")))
    ch = chapter_of(cid)
    if ch:
        g.append(J.chapter(ch[0], NCH, ch[1]))
    return "".join(g)


# ── カット表を読み込む ────────────────────────────────────
def _load_spec():
    """`tools/cuts/*.py` の SPEC を1つに束ねる。章ごとにファイルを分けてある。"""
    import cuts
    return cuts.SPEC


SPEC = _load_spec()

# ── 尺と字幕（audio/narration.json の実測） ───────────────
LEAD, TAIL = 0.35, 0.50


# 🔴 2026-08-01：カットごとに**末尾の間**を足せるようにした（カズヤくん判断）。
#    r13 の試写で quote に「決め所は前振りを読み終えてから出す」と指摘が出たが、
#    実測すると**どの quote カットも末尾は きっかり 0.50 秒（TAIL）しか無い**。
#    読み終えてから決め所を出す余地が、構造的に無かった。
#    ⚠️ ナレーションの文言も話速も変えていない。**読み終わったあとに間を足すだけ。**
#    16カット × 2.0 秒 ＝ 全体で +32 秒。
TAIL_EXTRA = {"quote": 2.0}


def _tail_extra(cid):
    fig = (SPEC.get(cid) or {}).get("fig")
    return TAIL_EXTRA.get(fig[0], 0.0) if fig else 0.0


def _narration():
    p = HERE / "audio" / "narration.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    dur = d["durations"]
    cuts = [(c, round(dur[c] + LEAD + TAIL + _tail_extra(c), 2)) for c in dur]
    return cuts, d.get("subtitles", {})


CUTS, SUBS = _narration()
ORDER = [c for c, _ in CUTS]

INSETS = {}

# ★写真を地に敷くときの切り方 (横方向の寄せ, 拡大率)。
# 🔴 USCG の ROV 画像には **左端と下端に焼き込み**がある
#    （"OceanGate / Dive: 01 / Depth (m): 3774.9" と日付・HDG・Alt）。
#    実写カットではこれは**出所の証拠**なので残す。だが地に敷くと話が変わる。
#    c115a は「水深3,346メートル」を図で出しているカットで、
#    その真上に **3774.9 という別の数字**が焼き込みで出てしまった（実際に焼いて発見）。
#    → 地に敷くときだけ、焼き込みが画面外に出るところまで寄せて切る。
PHOTO_CROP = {cid: (s.get("xbias", 0.5), s.get("zoom", 1.0))
              for cid, s in SPEC.items() if s.get("photo")}

# ★写真そのものを先に切り落とす (x0, y0, x1, y1)。**元画像に対する割合**で書く。
# 🔴 2026-08-02（r25 の目視・カズヤくん判断「切って英字を逃がす」）：
#    NTSB の標本写真には、**報告書の英字ラベルがビットマップに焼き込まれている**。
#    `extract_figs.py` に「英字はベクタなので付いてこない」と書いたが、実物は違った。
#      "Delamination" "Circumferential" "INCH" "Voids" "Layer 1／2" "Adhesive"
#      "Void in adhesive" "Grinding of composite plies at wrinkles" "0.200in"
#    日本語の注記のすぐ横に英語が並ぶうえ、c429 では**出典が英字の白箱に重なって
#    両方読めなく**なっていた。
#    → 英字が入らない帯を1枚ずつ実測して切る。**寸法は目分量で置かない。**
#    ⚠️ `zoom`/`xbias` では逃がせない（あれは切ったあとの寄せで、
#      英字が上下左右に散っている写真は寄せても必ずどれかが残る）。
#    ⚠️ 切る場所は**その写真の性質**なので、カットではなくファイルに紐づける
#      （`titan_delam_ruler` は c307 と c627 の2カットで使う。同じ英字が同じ場所にある）。
#      値は1枚ずつ画素で測って、切った結果を目で見て確かめたもの。
#
# 🔴 2026-08-04：**1本目（タイタン号）の7件を落とした。**2本目では1件も当たらない。
#    中身は git の `57e6c16` にある。上の設計理由4点は題材が変わっても効くので残す。
# ⚠️ 123便では、**キャプション文字は取り出しの時点で外してある**
#    （`tools/extract_photos.py` の `clip_text`）。それでも写真の中に
#    「上方」「前方」「第2ストラップ」等が**焼き込まれている**ものがあるので、
#    使う1枚ごとに等倍で目視して、必要ならここに足す。
TRIM_BY_PHOTO = {
    # 🔴 2026-08-04（r01 の拡大目視）：**地に敷いた写真の焼き込み札**が、
    #    暗幕0.84 を通しても白く残って、こちらの文字と競っていた。
    #    ルール §3「定規が白飛びして字幕や出典が乗る写真も切る」の、札の版。
    #
    # ep08：写真-107。「No.34リベット孔（起点側）」と「疲労亀裂終端」の**白い札**が
    #   y0.21〜0.38 にあり、**見出しの真裏**に来ていた（見出しの赤い罫が札を横切る）。
    #   下には「0.5mm」の物差しの札（y0.82〜0.92）。
    #   → 疲労破面の帯（y0.39〜0.80）だけを残す。実測で切った。
    "ja123/p107.jpg": (0.0, 0.39, 1.0, 0.80),
    # c214：写真-44。右端に「上方↑／→後方」の方位札（x0.82〜1.00）があり、
    #   画面の右端で「後方」が切れて出ていた。**こちらの図の方位指示に見える。**
    #   → 右の 19% を落とす。構造そのものは x0〜0.81 に収まっている。
    "ja123/p044.jpg": (0.0, 0.0, 0.81, 1.0),
    # c231：写真-43。同じく右端に「上方↑／→前」の方位札（x0.84〜0.98）。
    #   r02 で見ると、こちらの「断熱材の面」の札よりも**大きくて明るい**ので、
    #   積層図の方位指示に見えてしまう（写真の方位であって図の方位ではない）。
    "ja123/p043.jpg": (0.0, 0.0, 0.83, 1.0),
    # 🔴 2026-08-05（r10 の拡大目視）：写真-97。右端に「下方↑／→右舷」の方位札
    #   （x0.82 から先が白帯 248〜255）。r05 でこれを **c233 の spec に `trim=` で**
    #   書いてしまったので、**同じ写真を使う c330 には効かず**、
    #   白い帯がそのまま出て「右舷」が枠の端で切れていた。
    #   上の設計理由どおり、切る場所はファイルに紐づける。
    "ja123/p097.jpg": (0.0, 0.0, 0.81, 1.0),
}
# ── 🔴 6本目（キー橋）：報告書のページは**図の矩形で切る**（式で出す。手で書かない）──
#    紙いちめんを出すと、柱（誌名・MIR-25-40）と本文と図の題まで画面に載る。
#    出したいのは**図そのもの**なので、`tools/keybridge_assets.py bands` が
#    PDF の埋め込み画像の矩形（`page.get_image_bbox()`）から測った箱をそのまま使う。
#    ⚠️ 画素で探していない＝**本文の段落を図と読み違える余地が無い**。
#    ⚠️ 1ページに図が2つ在る印字 p62 は、**題のすぐ上の画像**を採ってある。
#    ⚠️ 台帳が無ければ**黙って全面を出さない**。ここが空のまま焼けたら ⑤c で必ず出る。
_KB_BANDS = HERE / "ref" / "keybridge" / "textbands.json"
KB_BANDS = (json.loads(_KB_BANDS.read_text(encoding="utf-8"))
            if _KB_BANDS.exists() else {})
for _n, _b in KB_BANDS.items():
    _x0, _y0, _x1, _y1 = _b["fig_box"]
    TRIM_BY_PHOTO[f"keybridge/{_n}.png"] = (_x0, _y0, _x1, _y1)

# ── 🔴 図の矩形の中に、さらに焼き込みの札が残るもの（⑤c の目視と画素の実測で足す）──
#    ⚠️ `textbands.json` の `fig_box` は「紙の中で図が占める矩形」なので、
#      **図の内側に報告書が載せた札**（"Pier 14" などの白い箱）は当然そのまま残る。
#      ここはファイル単位の上書き（同じ写真を別のカットが使っても効く。上の §TRIM の作法）。
#
# kb_p063_fig26（c110・3種類の径間）：図の下端に "Pier 14／15／16" の**白い札**が3つ並び、
#   全画面にすると y1008〜1049 ＝ **字幕帯の中**に入る（`check_slide` G-13）。
#   帯は不透明ではなく上端0→下端0.78 のグラデーション（`sub_band`）なので、
#   白い札は透けて残り、白い字幕とぶつかる。
#   → 札の**白い箱の上端を画素で測って**切った（2026-09-09）：
#        x 596〜683 の列で「行の90%以上が輝度235以上」になるのは y1484 から。
#        y1480 の白率 0.00% → y1500 で 13.82%。＝ 境目は 1484。
#      2px の余裕をみて **y=1478**（1478/2376 = 0.62205）で切る。
#   ⚠️ 切ると縦横比が 1404/729 ＝ 1.93（`ss.WIDE_AR` 2.04 未満）＝**全画面のまま**。
#   ⚠️ 横は 108px 切られる。既定の xbias=0.5 だと左の "Shorter/shallower" が
#      15px 欠ける（G-10）ので、c110 側で `xbias=0.0`（図の左端に合わせる）にしてある。
TRIM_BY_PHOTO["keybridge/kb_p063_fig26.png"] = (0.1176, 0.3154, 0.8823, 0.62205)

PHOTO_TRIM = {cid: s.get("trim") or TRIM_BY_PHOTO.get(s["photo"])
              for cid, s in SPEC.items() if s.get("photo")}
PHOTO_TRIM = {c: t for c, t in PHOTO_TRIM.items() if t}

# ── 階調を伸ばす写真（切り抜きと同じく**ファイル単位**で持つ）──────────
# 🔴 2026-08-09（カズヤくん承認）：捜索海図は**線と紙の明るさの差が
#    255階調中12〜16しかない**（実測）。素のまま出すと鉛筆の航跡も船名も見えない。
#      thr_fig_chart_redact_a  min 38 / p1 141 / median 182 / p99 198 / max 255
#      thr_fig_chart_redact_b  min 43 / p1 159 / median 185 / p99 199 / max 255
#      thr_fig_chart_c         min 40 / p1 156 / median 185 / max 212
#    → (118, 196) で伸ばすと、紙が 210〜255・鉛筆が 75〜135 になって読める
#      （切った結果を目で見て決めた。数値だけで決めていない）。
# ⚠️ **中身は足さない・消さない。** 出典の行に「濃淡補正」と出す（`credit_of`）。
# ⚠️ 白い塗り潰し（ちょうど255）は伸ばしても255のまま。**塗り潰しの実測値は
#    伸ばす前の原本で測ってある**（内側 254.95〜254.99・標準偏差 0.09〜0.22）。
LEVELS_BY_PHOTO = {
    "thresher/thr_fig_chart_redact_a.jpg": (118, 196),
    "thresher/thr_fig_chart_redact_b.jpg": (118, 196),
    "thresher/thr_fig_chart_redact_b2.jpg": (118, 196),
    "thresher/thr_fig_chart_c.jpg": (118, 196),
}
PHOTO_LEVELS = {cid: s.get("levels") or LEVELS_BY_PHOTO.get(s["photo"])
                for cid, s in SPEC.items() if s.get("photo")}
PHOTO_LEVELS = {c: v for c, v in PHOTO_LEVELS.items() if v}

# 全画面の実写カット。(枠, ファイル名, 縦方向の寄せ)
# ⚠️ `photo_box` が `TRIM_BY_PHOTO` を見るので、**この行は必ず上の定義より後**に置く
#    （2026-08-06 に額の箱を切り出し後の比で作るよう直したときの制約）。
PHOTO_CUTS = {cid: (photo_box(s), s["photo"], s.get("bias", 0.5))
              for cid, s in SPEC.items() if s.get("photo")}


# ── 段の持ち時間 ─────────────────────────────────────────
# 段が描き終わるのに最低限これだけは残す（秒）。
# 🔴 2026-08-01：r13 の試写で「右端の枠が描き終わる前にカットが切り替わる」（process 17枚）。
#    実測すると、**行より段が多いカット**では余った段を「いちばん広い隙間の真ん中」に
#    挟んでいたので、最後の段の開始が尺の終わりぎりぎりに寄っていた
#    （c414：尺4.86秒に対し最後の段が 4.30秒から。描画0.60秒で 4.90秒＝尺を超える）。
#    → **最後の段は必ず尺の RESERVE 秒前までに出はじめる**ように押し戻す。
RESERVE = 1.0

# build_layers が段の時間割（holds / labk）を書き出す場所。layer_index が直後に読む。
STAGE_META = {}


def stage_times(cid, nstage, holds=None):
    """段 i が「出はじめる秒」と「描き終える秒」を返す。

    段はナレーションの行に合わせて出す。行より段が多ければ余った段を等間隔で挟む。
    **描き終える秒 ＝ 次の段が出る秒**（最後の段はカット終わりまで）。
    こうすると、カットのどの瞬間にも必ず「描いている途中の段」が1つある。

    holds … 段ごとの指定（`titan_fig.Fig.holds`）。
      **"with_last"** … 🔴 **最後の行を読み"始める"のと同時**に出はじめ、
            その行を読み終えるころに出そろう（引用の決め所。2026-08-03 カズヤくん指示）。
      **"after_last"** … 最後の行を**読み終えてから**出す。⚠️ **2026-08-03 に撤回。**
            「読み終えてから出す」と、視聴者はもう答えを聞いてしまっているので
            **画面に出ても何の意外性もない**。新規に使わないこと。
    """
    sec = dict(CUTS)[cid]
    rows = SUBS.get(cid, [])
    starts = [r["t"] + LEAD for r in rows]
    if not starts:
        starts = [0.25]
    if nstage <= len(starts):
        st = starts[:nstage]
    else:
        # 行の切れ目を優先しつつ、足りないぶんは行の間に等間隔で挟む
        st = list(starts)
        bounds = starts + [sec]
        while len(st) < nstage:
            widest = max(range(len(bounds) - 1), key=lambda i: bounds[i + 1] - bounds[i])
            mid = (bounds[widest] + bounds[widest + 1]) / 2
            st.append(mid)
            bounds = sorted(bounds + [mid])
        st = sorted(st)[:nstage]
    # 🔴 最後の段が尺の終わりに寄りすぎていたら押し戻す（上の RESERVE を参照）
    if st and st[-1] > sec - RESERVE:
        st[-1] = max(st[0], sec - RESERVE)
        st = sorted(st)
    ends = st[1:] + [sec]
    if holds:
        last_beg = (rows[-1]["t"] + LEAD) if rows else 0.25
        last_end = (rows[-1]["t"] + rows[-1]["d"] + LEAD) if rows else 0.25
        for i, h in enumerate(holds[:len(st)]):
            if h == "with_last":
                # ★決め所は「最後の行を読み始めるのと同時」に出はじめ、
                #   **その行を読み終えるころに出そろう**。
                #   終わりを sec でなく行末に合わせるのが肝。sec まで引き延ばすと、
                #   声が終わったあともだらだら描き続けることになる。
                st[i] = min(last_beg, max(0.25, sec - RESERVE))
                ends[i] = max(last_end, st[i] + 1.1)
            elif h == "after_last":
                # ⚠️ 2026-08-03 撤回。既存カットの再現用にだけ残す
                st[i] = min(max(last_end + 0.25, st[i]), max(0.25, sec - RESERVE))
                ends[i] = sec
    # 描き終わりが早すぎると止まって見える。最低でも 1.1 秒はかける
    return [(a, max(b, a + 1.1)) for a, b in zip(st, ends)]


# 🔴 決め所と**同じ行**の字幕は出さない（画面に出した言葉は字幕に出さない）。
#    "after_last" のときは「読み終えてから出す」ので字幕は自然に消えていたが、
#    "with_last" は**声と同時**なので、消さないと二重表示になる。
#    {cid: {消す行番号, ...}}。build_layers が埋める。
SUB_MUTE = {}


# ── レイヤーの組み立て ────────────────────────────────────
def build_layers(allow_missing=False):
    """cid → {レイヤー名: SVG} と、ワイプの x 範囲を返す。

    allow_missing … 章を1つずつ作っている途中は True で回す（未定義カットを飛ばす）。
    """
    jobs, spans, holds, labks = {}, {}, {}, {}
    for cid in ORDER:
        spec = SPEC.get(cid)
        if spec is None:
            if allow_missing:
                continue
            raise SystemExit(f"カット {cid} の画が定義されていません（tools/cuts/）")
        if spec.get("photo") and spec["photo"] in BANNED_PHOTOS:
            raise SystemExit(f"{cid}: {spec['photo']} は出所が無いので使えません")
        if spec.get("photo") and not spec.get("fig"):
            # 実写カット（写真だけ。注記は暗幕とフチで写真の上に載せる）
            jobs[f"{cid}_bg"] = full_bg()
            jobs[f"{cid}_lab"] = full_top(cid, spec)
            for i, a in enumerate(photo_ann(spec)):
                jobs[f"{cid}_a{i + 1}"] = a
            spans[cid] = (0, W)
            continue
        # ★写真を地に敷いたうえに図を重ねるカット（photo と fig を両方持つ）
        back = bool(spec.get("photo"))
        kind, kw = spec["fig"]
        fig = getattr(F, kind)(**kw)
        jobs[f"{cid}_base"] = fig_base(cid, spec, ground=not back)
        lab, stages = fig.lab, list(fig.stages)
        holds[cid], labks[cid] = list(fig.holds), fig.labk
        if not stages:
            # 段が無いと「描いている途中」が作れず、カットが丸ごと静止する。
            # 骨格を段に格上げして、カット全体をかけて描かせる。
            lab, stages = "", [lab]
            holds[cid] = [None]
        if lab:
            jobs[f"{cid}_lab"] = lab
        for i, s in enumerate(stages):
            jobs[f"{cid}_a{i + 1}"] = s
        if fig.hot:
            jobs[f"{cid}_hot"] = fig.hot
        # 🔴 ワイプ範囲は**必ず本体枠を含める**。
        #    型が返す span は「図の実体」しか指していないことがあり
        #    （例：icons は絵の並びだけで 640〜1280）、そのままだと枠の左右に置いた
        #    見出し・注記・出典が**ワイプの外に出て永久に現れない**。
        spans[cid] = (min(fig.span[0], F.BX0), max(fig.span[1], F.BX1))
    # ⚠️ 戻り値は (jobs, spans) のまま。`jobs, _ = build_layers()` と受けている
    #    呼び出しが4か所（check_layout / check_box / peek / layer_index）あるので、
    #    段の時間割はここに置いて layer_index が直後に読む。
    STAGE_META.clear()
    STAGE_META.update({c: {"holds": holds.get(c) or [], "labk": labks.get(c)}
                       for c in spans})
    # 🔴 決め所と同じ行の字幕を消す（"with_last" のときだけ）。
    SUB_MUTE.clear()
    for c, hs in holds.items():
        if "with_last" in (hs or []):
            n = len(SUBS.get(c) or [])
            if n:
                SUB_MUTE[c] = {n - 1}
    return jobs, spans


def layer_index(allow_missing=False):
    """build_jiko が読む索引。{cid: dict(photo, layers, span, stages)}"""
    jobs, spans = build_layers(allow_missing=allow_missing)
    idx = {}
    for cid in [c for c in ORDER if c in spans]:
        s = SPEC[cid]
        names = [k for k in jobs if k.startswith(cid + "_")]
        ns = len([k for k in names if re.fullmatch(rf"{cid}_a\d+", k)])
        # photo … 写真を読む必要があるか（実写カットと、地に敷くカットの両方で True）
        # back  … **地に敷く**カットか（写真だけの実写カットと区別する）
        m = STAGE_META.get(cid, {})
        idx[cid] = {"photo": bool(s.get("photo")), "back": bool(s.get("photo") and s.get("fig")),
                    "veil": float(s.get("veil", VEIL)), "span": spans[cid],
                    # 🔴 実写カット（fig の無いカット）にかける暗幕。**書いたカットだけ**
                    "pveil": (float(s["veil"]) if s.get("veil") and not s.get("fig") else None),
                    "stages": ns, "layers": sorted(names),
                    "holds": m.get("holds") or [], "labk": m.get("labk")}
    return idx, jobs


def render_all(force=False, only=None, jobs_workers=4):
    """SVG → PNG。**Chrome を1レイヤーにつき1回起動する**ので並列で回す。

    226カット × 平均5レイヤー ＋ 字幕226枚 ＝ 約1,350回。直列だと20分近い。
    """
    from concurrent.futures import ThreadPoolExecutor
    OUT.mkdir(parents=True, exist_ok=True)
    ensure_css()
    jobs, _ = build_layers(allow_missing=True)
    jobs["_empty"] = J.frame(W, H)        # 余白測定の基準（check_space.py が使う）
    todo = []
    for k, svg in jobs.items():
        if only and not k.startswith(only):
            continue
        p = OUT / f"{k}.png"
        if p.exists() and not force:
            continue
        todo.append((k, svg, p, W, H))
    # ★字幕の黒帯。全カット共通の1枚。**常時貼るので必ず焼く**
    if not (only and not "_subband".startswith(only)):
        p = OUT / "_subband.png"
        if force or not p.exists():
            todo.append(("_subband", sub_band(), p, W, SUB_H))
    for cid, rows in SUBS.items():
        if only and not cid.startswith(only):
            continue
        p = OUT / f"sub_{cid}.png"
        if p.exists() and not force:
            continue
        h = SUB_H * len(rows)
        todo.append((f"sub_{cid}", sub_strip([r["text"] for r in rows]), p, W, h))
    print(f"書き出すレイヤー {len(todo)} 枚（並列 {jobs_workers}）", flush=True)
    done = [0]

    def one(t):
        k, svg, p, w, h = t
        render.png(page(svg, w, h), p, w, h)
        done[0] += 1
        if done[0] % 50 == 0:
            print(f"  {done[0]}/{len(todo)}", flush=True)

    with ThreadPoolExecutor(max_workers=jobs_workers) as ex:
        list(ex.map(one, todo))
    print(f"done {len(todo)}", flush=True)


def ensure_css():
    """フォントの base64 は4MB超。合成側では要らないので遅延で読む。"""
    global CSS
    if not CSS:
        CSS = (face_css("Dela", "DelaGothicOne.woff2")
               + face_css("Noto", "NotoSansJP-Bold.woff2")
               + face_css("NotoM", "NotoSansJP-Medium.woff2"))


def report():
    """焼く前に机上で見る要約。カット数・尺・図の種類の分布。"""
    from collections import Counter
    total = sum(s for _, s in CUTS)

    def kind_of(c):
        s = SPEC[c]
        if s.get("photo") and not s.get("fig"):
            return "photo"
        # ★写真を地に敷いた図解カットは、型の名前に「+写真」を付けて数える
        return s["fig"][0] + ("+写真" if s.get("photo") else "")

    kinds = Counter(kind_of(c) for c in ORDER if c in SPEC)
    nback = sum(1 for c in ORDER if c in SPEC
                and SPEC[c].get("photo") and SPEC[c].get("fig"))
    print(f"カット {len(ORDER)} ／ 完成尺 {total:.1f}秒 = "
          f"{int(total // 60)}分{total % 60:04.1f}秒")
    print(f"字幕 {sum(len(v) for v in SUBS.values())} 枚")
    print(f"実写 {kinds.get('photo', 0)} ／ ★写真を地に敷いた図解 {nback}")
    print("図の種類:")
    for k, v in kinds.most_common():
        print(f"   {k:<12} {v:>3}")

    # 🔴 2026-08-05（r08）：`ep16` の中身を章ファイルの `fig` 側で直したのに、
    #    `cuts/__init__.py` の PHOTO_OVERRIDE が勝っていて**古い ann のまま焼かれた**。
    #    章ファイルだけ見ていると気づけないので、上書きされているカットを毎回出す。
    import cuts as _C
    ov = sorted(_C.PHOTO_OVERRIDE)
    print(f"\n⚠️ cuts/__init__.py が**中身ごと上書き**しているカット（{len(ov)}件）:")
    print("   " + " ".join(ov))
    print("   章ファイルの fig / ann を直すときは、ここに載っていないか必ず見ること。")
    dead = [c for c in ov if c in SPEC and _C.PHOTO_OVERRIDE[c].get("photo")
            and "fig" in SPEC[c]]
    if dead:
        print(f"   🔴 図が捨てられているのに fig が残っているカット: {' '.join(dead)}")
    # 🔴 2026-08-10：**章名を毎回この目に入れる。**
    #    3本目で、隅の章名が2本目のままで38分ぶん焼けた。机上検査は1つも落ちない
    #    （文字として正しく出るので、重なりも複写も無い）。**人が見るしかない。**
    print(f"\n🔴 章の名前（題材を替えたら必ず書き換える／{NCH}章）:")
    for k in sorted(CHAPTERS):
        n, nm = CHAPTERS[k]
        print(f"   {n}/{NCH}  {nm}")
    print("   ↑ これは**いま作っている動画の章名**か？ 前作のままなら止めて直す。")
    miss = [c for c in ORDER if c not in SPEC]
    if miss:
        print(f"🔴 画が未定義: {miss}")
    extra = [c for c in SPEC if c not in ORDER]
    if extra:
        print(f"🔴 台本に無いカット: {extra}")

    # 🔴 2026-08-02：**写真が git に入っていなくて r24 が失敗した。**
    #    `.gitignore` が `ref/*` を除外して許可制（`!ref/…` を1行ずつ）にしているので、
    #    新しい写真を置いても `git add -A` が**黙って落とす**。
    #    ローカルにはファイルがあるから机上検査は全部通り、写真を実際に開くのは
    #    クラウドの `build_jiko` だけなので、**40分焼いた最後に FileNotFoundError**
    #    になる。押す前にここで気づけるようにする。
    #
    # ⚠️ **この検査は最初に作ったとき間違っていた**（2026-08-02・作り直し）。
    #    `git ls-files` は**索引（add した状態）**を答えるので、
    #    `git add` して**commit していない**ファイルを「入っている」と言う。
    #    r24 が落ちたときのリポジトリがまさにその状態で、
    #    **この検査は 0件と答えていた**。クラウドが checkout するのは索引ではなく
    #    **push 済みのコミット**なので、そこを見なければ意味が無い。
    #    → HEAD のツリー（`ls-tree`）を見る。さらに push 済みかも見る。
    used = sorted({v[1] for v in PHOTO_CUTS.values()})
    nofile = [n for n in used if not (HERE / "ref" / n).exists()]
    if nofile:
        print(f"🔴 ref に実体が無い写真: {nofile}")

    def _git(*a):
        import subprocess
        r = subprocess.run(["git", *a], cwd=HERE, capture_output=True,
                           text=True, timeout=20)
        return r.stdout if r.returncode == 0 else None

    uncommitted = []
    head = _git("ls-tree", "-r", "--name-only", "HEAD", "ref/")
    if head is None:                            # git が無い環境（クラウド）では黙る
        print("   （git を確認できないので追跡の検査は飛ばす）")
    else:
        intree = set(head.split())
        uncommitted = [n for n in used if f"ref/{n}" not in intree]
        if uncommitted:
            print(f"🔴 **コミットされていない写真** {len(uncommitted)}件: {uncommitted}")
            print("   → `.gitignore` の許可制リストに `!ref/<名前>` を1行ずつ足して"
                  "**commit する**。add しただけではクラウドに届かない。")
        # コミット済みでも push していなければクラウドは古い版を焼く
        ahead = _git("rev-list", "--count", "@{u}..HEAD")
        if ahead is None:
            print("   （上流が無いので push の検査は飛ばす）")
        elif int(ahead.strip() or 0):
            # 押せば直る（写真そのものは在る）ので、戻り値は落とさず警告だけ出す
            print(f"🔴 **push していないコミットが {ahead.strip()} 個ある。**"
                  "クラウドは古い版を焼く → `git push` してから回すこと")
    return not (miss or extra or nofile or uncommitted)


if __name__ == "__main__":
    if "--report" in sys.argv:
        sys.exit(0 if report() else 1)
    render_all(force="--force" in sys.argv,
               only=next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")),
                         None))
