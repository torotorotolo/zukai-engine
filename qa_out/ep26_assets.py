# -*- coding: utf-8 -*-
"""ep26_assets.py — 26本目（タイタニック号沈没事故）の写真・頁の束と NOAA 2004 の映像の台帳（⑤b-2・2026-10-27）。25本目 `ep25_assets.py` の形を、
26本目の台帳（`sources26.psv` の13列〈見出しの行で読む〉・`fetch26.tsv`〈md5 を2回〉・git の外の作者の表 `credits_private.tsv`
〈列 source・no・title・license・author・url＝行の鍵は (sources26, 記号)〉）に合わせた。

取得はすんでいる（映像方針＝了承②・`ref/ep26/eizou_build/fetch26.py`・記録 `fetch26.tsv`）。ここは**束を作る道**だけを持つ。
  python qa_out/ep26_assets.py build             # 写真・頁の束 ref/ep26/<名>.jpg ＋ 権利の台帳 ref/ep26/assets.json
  python qa_out/ep26_assets.py look S1-002 …     # 束の写真を並べた見本（out/ep26_look/・1枚 960 幅）＝選ぶとき・確かめるとき（記号か束の名）
  python qa_out/ep26_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python qa_out/ep26_assets.py edges             # 束の四辺の暗い帯（スライドの台紙の縁）＝門番 check_photo_edge の名簿を決める
  python qa_out/ep26_assets.py credits [--write] # 画面の出典 ref/ep26/credits.json と ref/CREDITS.md の26本目の節
  python qa_out/ep26_assets.py lines P-G2-03     # 🆕 頁の字の層の行（y の割合つき・名前の語は伏せる）＝PAGE_CROP の head・tail を選ぶ
  python qa_out/ep26_assets.py pbox P-G1-054 "There appears" "Californian"   # 頁の字の層の行から切り口（束の割合）を測る
  python qa_out/ep26_assets.py names [<画像かフォルダ> …]   # 名前の門番＝絵の OCR × git の外の名前の表（既定＝束の頁の全部）
  python qa_out/ep26_assets.py names --selftest  # 陽性対照＝名前の載る頁をまるごと描いて網が名前を拾うか
  python qa_out/ep26_assets.py clips｜shots｜frames N04｜use [c… ]｜fb [c… ]   # 映像＝NOAA 2004（⑤b-2）・フリー素材（Pexels＝⑤b-3）

入力＝映像方針の一覧 `ref/ep26/eizou_build/list26.tsv`（生成物・秒は narration.json の実測＝⑤b-1）・出どころ `sources26.psv`（区切り「|」）・
取得の記録 `fetch26.tsv`。元は `ref/ep26/src/`（git の外）。
🔴 束の写真は長辺を縮めるだけ（色はそのまま＝原色・了承②）＝幅 2400 か高さ 1350 の大きい方まで（小さい写真は縮まない＝原画のまま）。
🔴 頁は PDF から長辺 3600px で描き直す（S. Doc. 933・MAIB 1992・37 Stat. 199＝どれも走査の画像＋字の層）。
🔴 **人は名前＋役職か役職だけ・乗客は名前なし（①・承認①）**＝出さない名前（会社の人・カリフォルニアン号の機関部の乗組員・私人＝git の外の
   `src/names_private.txt`）が束の絵に入れば止める。頁は字の層の網（`render_page`）・写真の紙面（新聞・電報の用紙・ネガの字）は**束の段で切り出す**
   （表 PHOTO_CROP＝原寸で見て決めた）。🔴 英字の名前は**語の境**で当てる（短い姓が別の語の切れ目をまたいだ字並び〈「being ill」の「g ill」の形〉に当たらないように＝namecheck26 と同じ考え）。
🔴 **NOAA 2003 の写真2点（S11-716・S11-910）の出典の行は NOAA の頁の courtesy の表記**（撮影者の個人名つき）＝名前は公開リポに書かない
   ＝credits.json の行は印 `{作者}` だけ・焼くときに `scene_jiko._ep26_author` が git の外の表の (sources26, 記号) の行から足す（17・23〜25本目の型）。
"""
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import unicodedata
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
EPD = HERE / "ref" / "ep26"
SRC = EPD / "src"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list26.tsv"
SOURCES = BUILD / "sources26.psv"
FETCH = BUILD / "fetch26.tsv"
PRIVATE = SRC / "credits_private.tsv"      # 🔴 git の外（作者欄）＝ここから名前を公開の物へ写さない
NAMES = SRC / "names_private.txt"          # 🔴 git の外（出さない名前）
DB = EPD / "assets.json"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
FOOTAGE = HERE / "tools" / "footage.py"
SCRATCH = HERE / "out" / "ep26_look"           # look・frames・names の陽性対照の出力（out/ は git の外）
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## タイタニック号沈没事故（1912-04-15・26本目）"
AUTHOR = "{作者}"            # 個人名義の点の画面の出典の行の印（焼くときに git の外の表から足す＝scene_jiko.ep26_credit）
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（footage.py の注）
EVENT_YEAR = 1912            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）
UA = "zukai-engine/1.0 (accident-documentary research; https://github.com/torotorotolo/zukai-engine)"

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
PAGE_LONG = 3600                       # 頁は長辺 3600 で描く（寄りで字を読める大きさを残す＝17・24・25本目と同じ）
JPEG_Q = 92
MOSAIC_PX = 14                         # 升目の大きさ（束の画素）
PHOTO_TYPES = ("commons-photo",)
PAGE_TYPES = ("report-page", "maib-page", "law-page")
OTHER_TYPES = ("satellite", "stock", "noaa-video")      # 束に入れない（衛星写真＝ss.SAT・映像＝clips.json）
# PDF の名（get の page:<名>:<頁>）→ src からの道
PDFS = {"SERIALSET-06179_00_00-019-0933-0000": "gov/SERIALSET-06179_00_00-019-0933-0000.pdf",
        "maib1992": "gov/maib1992.pdf", "stat37_199": "gov/stat37_199.pdf"}
# 頁の資料の年（副題の年と照らす）＝PDF の名で（sources.md の資料の表）
DOC_YEAR = {"SERIALSET-06179_00_00-019-0933-0000": (1912, "英国の審問の報告（1912年7月30日）を米国上院が刷り直した S. Doc. 933（1912年）"),
            "maib1992": (1992, "英国運輸省 海難調査局の再評価の報告（1992年）"),
            "stat37_199": (1912, "米国の法 37 Stat. 199（1912年7月23日）")}
# 🔴 頁が台帳の頁と同じかを字の層の句で照らす（PDF の頁と刷りの頁番号の取り違えを止める＝sources26 の題の語・小文字と空白を揃えて比べる）
PAGE_EXPECT = {
    "P-G1-005": "1,490", "P-G1-041": "grievous mistake", "P-G1-054": "there appears to be no doubt",
    "P-G1-056": "this position is not accurate", "P-G1-058": "rockets at sea for nothing",
    "P-G1-059": "considerable discrepancy", "P-G1-060": "many if not all", "P-G1-076": "unsinkable", "P-G1-085": "24.",
    "P-G2-01": "reappraisal of evidence", "P-G2-03": "fully agree", "P-G2-18": "entirely agree", "P-G2-21": "sympathise",
    "P-G2-22": "distance apart", "P-G2-23": "villains", "P-G4-2": "two or more persons",
}

# 🔴 名前の載る頁＝束の段で名前の外を切り出す {記号: dict(head, tail, why)}。head〜tail＝字の層の行（その行を含む）。⑤b-2（10-27）に `lines` で決めた
PAGE_CROP = {
    # c806（a very grievous mistake）＝頁の頭の2行（y 0.09〜0.12）に会社の人の名前＝その下の段落「The evidence shows…」〜「…case in the future.」
    "P-G1-041": dict(head="The evidence shows that he was not trying", tail="case in the future",
                     why="頁の頭の2行（会社の人の名前）を外し、船長の判断の段落だけ"),
    # c628（A ship is not going to fire rockets at sea for nothing）＝y 0.51 の行に機関部の乗組員の名前＝次の段落「Both Mr. Stone and the apprentice…」から頁の終わりまで
    "P-G1-058": dict(head="Both Mr. Stone and the apprentice", tail="altogether we had seen eight",
                     why="機関部の乗組員の名前の行を外し、二等航海士と見習いの段落から頁の終わりまで"),
    # c906（同意の行）＝宛先の大臣と前の大臣の名前（y 0.27〜0.38）と首席の署名の行（y 0.84〜0.88）を外す＝「Clearly, the case…」〜「I full endorse…」
    "P-G2-03": dict(head="Clearly, the case was somewhat outside", tail="I full endorse",
                    why="宛先と前の大臣の名前・首席の署名の行を外し、調査官を外から呼んだ段落と同意の行だけ"),
    # cb02（結び＝no villains）＝結びの段落だけ（その下の星の行と頁の末の署名の場所を外す＝字の層に署名は無いが、絵の側に残っても入らない）
    #   outside＝切り口の外にあるべき目印の行（字の層に名前が無い頁の陽性対照＝星の行より下に署名の場所）
    "P-G2-23": dict(head="A final word seems called for", tail="just human beings", outside=["* * * *"],
                    why="結びの段落だけ（頁の末の署名の場所を外す）"),
    # 🆕 ⑤b-7（2026-10-28）：引用の頁は額装で切れない（ss.check_frame_only が trim を止める）＝語りの段落だけを束の段で切り出す
    #   （映像方針の一覧 c930・c937・c941「静止の切り出し」。頁まるごとの額は字が約8px で読めない）
    # c904（表紙）＝白い紙の真ん中の題の4行だけ（頁まるごとは額の高さ 648px で題の字が約15px・インク率 1.2%＝門番 blank の下限 4.0% の下）
    "P-G2-01": dict(head='RMS "TITANIC"', tail='SS "CALIFORNIAN"',
                    why="表紙の題の4行だけ（下の局の名・所・刷りの行は外す）"),
    # c930（I entirely agree with him）＝節の題「WERE TITANIC'S ROCKETS SEEN?」から「…seen by TITANIC, than lights.」の行まで
    "P-G2-18": dict(head="ROCKETS SEEN", tail="seen by TITANIC, than lights",
                    why="節の題と、信号弾は見えていたとする段落の頭だけ"),
    # c937（I sympathise with Mr Stone）＝「Of course, … should have gone down himself」の文から「seriously at fault.」まで
    "P-G2-21": dict(head="own eyes and senses", tail="seriously at fault",
                    why="二等航海士の落ち度を書いた文だけ"),
    # c941（if I am right as to the distance apart）＝「It therefore seems clear…」から「…should have been made.」まで
    "P-G2-22": dict(head="arrive well after the sinking", tail="should have been made",
                    why="距離の見方が正しければ結果は変わらない、とする文だけ"),
}
# 送り状は宛先・署名の役職の行も目印にする（名前の表に無い名前が字の層で崩れていても、その行ごと外に出ていることを測る）
#   ⚠️ 署名の下の役職の行「Chief Inspector of Marine Accidents」は本文の「Deputy Chief Inspector of Marine Accidents」にも含まれる＝目印にしない（1回目に当てて止まった）
PAGE_CROP["P-G2-03"]["outside"] = ["of State for Transport", "Your obedient servant"]
# 🔴 名前の載る写真の紙面（新聞・電報の用紙・ネガの字）＝束の段で名前の外を切り出す {記号: ((x0, y0, x1, y1)＝元の絵の割合, 理由)}。
#    ⑤b-2（10-27）に原寸で見て決めた（scratchpad `b2/cA.jpg`＝束の画素の切り出し・割合は元の絵でも同じ）
PHOTO_CROP = {
    # c214（見出し）＝本文の1行目（束 y 288〜）に会社の人の名前と肩書＝見出しの3行（「THE VESSEL UNSINKABLE.」〜「NEW YORK, MONDAY.」・y 〜268）と
    #   名前の行のすき間（y 278）で切る。左右は記事の白い欄（Commons の版の橙の枠と縦の題字の帯を外す）
    "S4-264": ((0.2045, 0.032, 0.9654, 0.1986), "本文の1行目（会社の人の名前）から下と橙の枠を外し、見出しの3行だけ"),
    # c309（本文）＝用紙の頭の枠（会社の名と社長の名前の刷り・束 y 〜479＝1920×1484 の版）を外す＝枠の下の線から 11px 下（y 490）〜用紙の下の線の下まで・
    #   左右は用紙の縦の線の外まで。⚠️ 1回目は並べの中の位置を引き忘れて y 779 から切り、本文の5行を落とした（v4 の原寸で見つけた）。
    #   2回目の y 490 は用紙の番号の行（印刷の字）の上半分を切った（v5）＝枠の線の下（y 485）から
    "S4-N06": ((0.105, 0.3268, 0.895, 0.842), "用紙の頭の枠（電信会社の社長の名前の刷り）を外し、受信の本文・受付印・手書きの書き込みだけ"),
    # c819（全体）＝ネガの上の字（議員の名と番号・束 y 120〜195）を外す＝y 0.125（223px）から下
    "S3-698": ((0.0, 0.125, 1.0, 1.0), "ネガの上の字（議員の名）を外す"),
}
# 撮影年の手当て {記号: (年 か None, 出どころ)}＝決まりの読み（題・根拠の欄の「NNNN年」）で決まらない点
YEAR_FIX = {
    "S11-716": (2003, "NOAA の頁＝RMS Titanic Expedition 2003（Commons の撮影日の札「2004-06」は誤り＝映像方針 sources26 の注）"),
    "S11-910": (2003, "NOAA の頁＝RMS Titanic Expedition 2003（detached rusticles の頁）"),
    # ⑤b-2：冒頭 c103・c106 の副題の年の出どころ（Commons の目録 pick26.tsv の date と materials.md §5・§9）
    "S5-359": (1912, "NARA 278334 の目録の日付 1912-12-14・題「A Photograph of an Iceberg Floating Near the Site of the TITANIC Sinking.」"
                     "（撮影の月は書いていない＝副題は年だけ）"),
    "S8-E03": (1912, "Commons の日付の欄 15/04/1912・説明「…photographed by passenger aboard R.M.S. Carpathia, April 15th 1912」"
                     "（出どころ Reddit＝弱い＝副題は日付ごと「とされる」）"),
}
# MAIB の頁の画面の出典の行（sources26 の出典の欄は長い＝字幅 61.1）＝了承② 決め4「…より引用」の形のまま、著者（英国の海難調査局）・題号（表紙の題そのまま）・年・頁
#   の4つを1行に（字幅 56.5 まで＝「英国運輸省」と「出典：」を外した・題号は削らない）。頁＝刷りの頁番号（送り状と表紙は番号が無い）
MAIB_TITLE = '英国海難調査局『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』1992年'
MAIB_PAGE = {"P-G2-01": "表紙", "P-G2-03": "送り状", "P-G2-18": "p.14 ", "P-G2-21": "p.17 ", "P-G2-22": "p.18 ", "P-G2-23": "p.19 "}
# 顔だけ升目 {記号: [(x0, y0, x1, y1, 誰)]}（束の画素）。⑤b-2（10-27）に原寸で見て決めた（scratchpad `b2/cB〜cF.jpg`）
#   了承② 決め3＝乗客は顔が分かれば顔だけモザイク（PD）／16本目 ⑤b の前例＝私人か写真で決められない顔も升目
#   ✕ 升目にしない（原寸で見た）：S2-045・S1-084・S7-594・S6-480（冒頭 c104）・S1-057 の上半分＝顔が数画素のぼけ／S6-379＝ボートの乗員／
#      S1-013＝制服の係（職務中）と後ろ向きの人（顔の見えない横顔）・遠くの人の列
MASK = {
    # c323・c820＝米国上院の公聴会の部屋（議員・証人・記者・傍聴の人が分けられない＝顔の分かる全員）
    "S9-648": [(925, 165, 990, 240, "上の立つ人"), (1040, 190, 1115, 270, "右上の口ひげの人"), (420, 270, 480, 350, "左の白いひげの人"),
               (525, 248, 590, 300, "奥の人"), (615, 238, 670, 292, "奥の人"), (515, 290, 590, 368, "襟の人"), (600, 272, 668, 348, "奥の人"),
               (655, 318, 720, 392, "若い人"), (735, 288, 815, 372, "大柄な人"), (845, 298, 918, 380, "真ん中の人"),
               (1045, 328, 1125, 412, "右の口ひげの人"), (1135, 345, 1200, 425, "右の人"), (1435, 345, 1515, 425, "右の端の人"),
               (1465, 405, 1528, 475, "右の端の下の人"), (305, 422, 380, 505, "左のネクタイの人"), (378, 405, 455, 495, "横顔の人"),
               (530, 410, 595, 495, "奥に半分の人"), (710, 500, 775, 575, "真ん中の座る人"), (970, 485, 1045, 565, "座る人"),
               (1050, 495, 1125, 580, "下を向く人"), (1140, 535, 1220, 625, "口ひげの座る人"), (1355, 550, 1445, 645, "右の座る人"),
               (590, 595, 690, 705, "手前の口ひげの人"), (500, 775, 610, 890, "手前の若い人"), (90, 445, 170, 515, "左の奥の人"),
               (125, 490, 220, 575, "左の下を向く人"), (10, 480, 85, 575, "左の端の横顔"), (1340, 680, 1430, 770, "右の横顔"),
               (1430, 820, 1536, 910, "右の端の人")],
    # c208・c509＝ボート甲板を歩く乗客（女の子・帽子の女の人・帽子の男の人・奥の男の人）。右の女の人は後ろ姿＝升目にしない
    "S2-054": [(688, 763, 730, 808, "女の子"), (758, 745, 808, 800, "帽子の女の人"), (852, 720, 902, 778, "帽子の男の人"),
               (956, 698, 990, 740, "奥の男の人")],
    # c219＝タイタニック号の甲板の人たち（下半分＝顔の分かる人）。上半分の遠くの人とタグボートの人は数画素＝升目にしない
    "S1-057": [(545, 955, 592, 1010, "真ん中を歩く人"), (598, 1350, 662, 1425, "手前の帽子の人"), (815, 1340, 882, 1412, "手前の右の帽子の人"),
               (373, 710, 418, 752, "座る人"), (125, 775, 168, 818, "左の人"), (198, 745, 242, 790, "左の人"), (253, 752, 292, 795, "左の人"),
               (160, 848, 205, 895, "左のうつむく人"), (880, 995, 945, 1045, "右の手すりの人"), (735, 1112, 785, 1165, "手すりの帽子の人")],
    # c707＝カルパチア号の横のボートの生存者（上から・縦長）。こちらを向く顔
    "S6-383": [(1447, 1924, 1513, 2004, "右上の女の人"), (1100, 1951, 1164, 2020, "左の女の人"), (1283, 1996, 1356, 2076, "白い服の人"),
               (1116, 2160, 1169, 2227, "真ん中の左の人"), (1236, 2207, 1289, 2273, "真ん中の人"), (1317, 2191, 1371, 2257, "真ん中の右の人"),
               (1351, 2140, 1404, 2200, "奥の人"), (1257, 2320, 1316, 2391, "白い帽子の人"), (1484, 2400, 1556, 2473, "右下の女の人"),
               (957, 2520, 1011, 2583, "左下の人"), (1033, 2193, 1087, 2253, "左の人")],
    # c714＝カルパチア号の甲板の生存者（ほとんど後ろ姿）。前を向く・横を向く顔だけ
    "S6-427": [(1045, 750, 1108, 812, "真ん中のベールの人"), (1270, 762, 1322, 820, "真ん中の右の人"), (830, 735, 882, 795, "帽子の人"),
               (418, 788, 475, 848, "左の暗がりの人"), (518, 810, 568, 860, "左の人")],
}
MASKED_BEFORE = {}


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _list():
    return list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))


def _sources():
    rows = [ln for ln in SOURCES.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.startswith("#")]
    head = rows[0].split("|")
    if head != ["code", "type", "title", "page", "get", "dims", "rights", "basis", "credit", "era", "people", "file", "note"]:
        raise SystemExit(f"🔴 sources26.psv の見出しの行が変わった：{rows[0][:120]}")
    out = {}
    for ln in rows[1:]:
        f = ln.split("|")
        if len(f) != 13:
            raise SystemExit(f"🔴 sources26.psv の行の欄が13でない：{ln[:80]}")
        out[f[0]] = dict(zip(head, f))
    return out


def _fetched():
    """{記号: 行}（fetch26.tsv＝code・when・file・bytes・width・md5_1・md5_2・sha1_ok・url_kind）"""
    out = {}
    for r in csv.DictReader(FETCH.open(encoding="utf-8"), delimiter="\t"):
        if r.get("code") and not r["code"].startswith("#"):
            out[r["code"]] = r
    return out


def _private():
    """git の外の表 {(source, no): {列: 値}}。無ければ止める（束を作る手元だけで読む）"""
    if not PRIVATE.exists():
        raise SystemExit(f"🔴 {PRIVATE.relative_to(HERE).as_posix()} が無い（git の外の作者欄の表）")
    rows = [r for r in csv.reader(PRIVATE.open(encoding="utf-8"), delimiter="\t") if r]
    head = rows[0]
    return {(r[0], r[1]): dict(zip(head, r)) for r in rows[1:] if len(r) >= 2}


def _fold(s):
    """当てる側の形＝NFKC・小文字・空白は1つの空白に"""
    return " ".join(unicodedata.normalize("NFKC", s or "").lower().split())


def _mask_word(w):
    return w[0] + "○" * (len(w) - 1)


def _name_re(n):
    """名前1つの当て方。英字＝語の境で（語と語のあいだは空白の有無を問わない）・かなと漢字＝そのまま"""
    n = _fold(n)
    if re.search(r"[a-z]", n):
        return re.compile(r"(?<![a-z])" + r"\s*".join(re.escape(p) for p in n.split()) + r"(?![a-z])")
    return re.compile(re.escape(n.replace(" ", "")))


def _names():
    """git の外の出さない名前 [(伏せた形, 当て方)]（2字以上）。無ければ止める（fail closed）"""
    if not NAMES.exists():
        raise SystemExit(f"🔴 {NAMES.relative_to(HERE).as_posix()} が無い（git の外の名前の表）")
    out = []
    for ln in NAMES.read_text(encoding="utf-8").splitlines():
        n = ln.strip()
        if n and not n.startswith("#") and len(n) >= 2:
            out.append((_mask_word(n.replace(" ", "")), _name_re(n)))
    if not out:
        raise SystemExit("🔴 名前の表が空（fail closed）")
    return out


def _author_res():
    """git の外の作者欄の名前（台帳に漏れていないかを見る網）"""
    out = []
    if PRIVATE.exists():
        for v in _private().values():
            for t in re.findall(r"[A-Za-z][A-Za-z.'-]{2,}", v.get("author") or ""):
                out.append((_mask_word(t), _name_re(t)))
    return out


def hits_in(text, names):
    t = _fold(text)
    return [w for w, rx in names if rx.search(t)]


def uses():
    """{記号: [カット]}（一覧の素材の欄から・束に入る写真と頁だけ）。種類と出どころの型が食い違えば止める"""
    src = _sources()
    out, bad = {}, []
    for r in _list():
        c = r["code"]
        s = src.get(c)
        if not s or s["type"] in OTHER_TYPES:
            continue
        if s["type"] in PAGE_TYPES and r["kind"] != "頁" or s["type"] in PHOTO_TYPES and r["kind"] != "実写":
            bad.append(f"{r['cid']} {c}: 一覧の種類「{r['kind']}」と出どころの型 {s['type']} が食い違う")
        if s["type"] not in PAGE_TYPES + PHOTO_TYPES:
            bad.append(f"{r['cid']} {c}: 出どころの型 {s['type']} を束の道が知らない")
        out.setdefault(c, []).append(r["cid"])
    if bad:
        raise SystemExit("🔴 " + "\n🔴 ".join(bad))
    return out


def bundle_name(code):
    return code.lower().replace("-", "_")


# ── 頁 ─────────────────────────────────────────────────────────
def pdf_path(name):
    if name not in PDFS:
        raise SystemExit(f"🔴 PDF の名 {name} が表 PDFS に無い")
    return SRC / PDFS[name]


def _page_ref(s):
    """出どころの get → (PDF の名, 頁)"""
    g = s["get"]
    m = re.fullmatch(r"page:(.+):(\d+)", g)
    if not m:
        raise SystemExit(f"🔴 {s['code']}: 頁の get が page:<名>:<頁> でない（{g}）")
    return m.group(1), int(m.group(2))


def doc_year(name):
    if name not in DOC_YEAR:
        raise SystemExit(f"🔴 頁の資料の年が表 DOC_YEAR に無い（{name}）")
    return DOC_YEAR[name]


def _lines(pg):
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            t = "".join(s["text"] for s in ln["spans"]).strip()
            if t:
                out.append((t, ln["bbox"]))
    return out


def name_boxes(pg, names):
    """頁の字の層で、出さない名前の字の箱（pt）＝[(伏せた名前, (x0, y0, x1, y1)), …]。行をまたぐ名前は字ごとの箱を全部返す"""
    chars = []
    for b in pg.get_text("rawdict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln["spans"]:
                for c in sp["chars"]:
                    t = unicodedata.normalize("NFKC", c["c"]).lower()
                    chars.append((t if t.strip() else " ", c["bbox"]))
            chars.append((" ", None))                 # 行の切れ目＝語の境
    txt = "".join(c for c, _ in chars)
    out = []
    for w, rx in names:
        for m in rx.finditer(txt):
            for i in range(m.start(), m.end()):
                if chars[i][1] is not None and chars[i][0] != " ":
                    out.append((w, tuple(chars[i][1])))
    return out


def _crop_box_pt(pg, spec, code):
    """PAGE_CROP の head〜tail の行の箱（pt）。上下は前後の行とのすき間の真ん中・左右は選んだ行の外接＋8pt"""
    lines = _lines(pg)
    i0 = next((i for i, (t, _) in enumerate(lines) if spec["head"] in t), None)
    if i0 is None:
        raise SystemExit(f"🔴 {code}: 「{spec['head']}」の行が字の層に無い")
    i1 = next((i for i in range(i0, len(lines)) if spec["tail"] in lines[i][0]), None)
    if i1 is None:
        raise SystemExit(f"🔴 {code}: 「{spec['head']}」より後に「{spec['tail']}」の行が無い")
    sel = [b for _, b in lines[i0:i1 + 1]]
    x0, x1 = min(b[0] for b in sel), max(b[2] for b in sel)
    top, bot = min(b[1] for b in sel), max(b[3] for b in sel)
    over = [b for _, b in lines if b[0] < x1 and b[2] > x0 and b not in sel]
    above = [b[3] for b in over if b[3] <= top + 1]
    below = [b[1] for b in over if b[1] >= bot - 1]
    yt = max((max(above) + top) / 2, top - 12) if above else top - 8
    yb = min((min(below) + bot) / 2, bot + 12) if below else bot + 8
    return (max(0, x0 - 8), max(0, yt), min(pg.rect.width, x1 + 8), min(pg.rect.height, yb))


def render_page(code, s, names):
    """頁を描く＝(RGB の PIL 画像, 記録の dict)。名前の字の箱が束の絵に入れば止める"""
    import fitz
    import numpy as np
    from PIL import Image
    name, no = _page_ref(s)
    pdf = pdf_path(name)
    if not pdf.exists():
        raise SystemExit(f"🔴 {code}: PDF {pdf.relative_to(HERE).as_posix()} が無い")
    pg = fitz.open(pdf)[no - 1]
    want = PAGE_EXPECT.get(code)
    if not want or _fold(want) not in _fold(pg.get_text()):
        raise SystemExit(f"🔴 {code}: 字の層に目印の句「{want}」が無い（PDF の頁 {no} が台帳の頁と違う？）")
    nb = name_boxes(pg, names)
    rec0 = dict(pdf=pdf.relative_to(HERE).as_posix(), pdf_page=no, pdf_md5=md5(pdf), expect=want)
    crop = PAGE_CROP.get(code)
    k = PAGE_LONG / max(pg.rect.width, pg.rect.height)
    pix = pg.get_pixmap(matrix=fitz.Matrix(k, k), alpha=False)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    if crop:
        bpt = _crop_box_pt(pg, crop, code)
        box = tuple(int(round(v * k)) for v in bpt)
        how = f"PDF の頁を描いた（長辺 {PAGE_LONG}px）・🔴 名前の外を切り出し（{crop['why']}）＝字の層の行「{crop['head']}」〜「{crop['tail']}」"
    else:
        a = np.asarray(im.convert("L"))
        h, w = a.shape
        m = int(min(h, w) * 0.03)               # 走査の縁の影（端の 3% の暗い帯）は外接に入れない
        ys, xs = np.where(a[m:h - m, m:w - m] < 160)
        box = (max(0, xs.min() + m - 24), max(0, ys.min() + m - 24), min(w, xs.max() + m + 24), min(h, ys.max() + m + 24))
        how = f"PDF の頁を描いた（長辺 {PAGE_LONG}px）・インクの外接"
    region = tuple(v / k for v in box)
    im = im.crop(box)
    rec = dict(rec0, scale=round(k, 5), box_px=[int(v) for v in box], how=how)
    for anc in (crop or {}).get("outside", []):
        hit = [b for t, b in _lines(pg) if anc in t]
        if not hit:
            raise SystemExit(f"🔴 {code}: 目印の行「{anc}」が字の層に無い（外に出したことを測れない）")
        if any(b[0] < region[2] and b[2] > region[0] and b[1] < region[3] and b[3] > region[1] for b in hit):
            raise SystemExit(f"🔴 {code}: 切り口の外にあるべき行「{anc}」が束の絵に入る")
    inside = [(w_, b) for w_, b in nb if b[0] < region[2] and b[2] > region[0] and b[1] < region[3] and b[3] > region[1]]
    if inside:
        raise SystemExit(f"🔴 {code}: 束の絵に出さない名前の字が入る（{sorted({w_ for w_, _ in inside})}）＝PAGE_CROP で外す")
    return im, rec


def cmd_lines(code):
    """頁の字の層の行を y の割合つきで並べる（出さない名前の語は伏せる）＝PAGE_CROP の head・tail を選ぶ"""
    import fitz
    s = _sources()[code]
    names = _names()
    name, no = _page_ref(s)
    pg = fitz.open(pdf_path(name))[no - 1]
    H = pg.rect.height
    for i, (t, b) in enumerate(_lines(pg)):
        hit = hits_in(t, names)
        shown = t
        for w, rx in names:
            shown = rx.sub(w, _fold(shown)) if rx.search(_fold(shown)) else shown
        print(f"{i:3} y {b[1] / H:5.3f}〜{b[3] / H:5.3f} x {b[0]:5.0f}〜{b[2]:5.0f} {'🔴名前 ' if hit else ''}{shown[:110]}")
    return 0


def cmd_pbox(code, head, tail, pad=18):
    """頁の字の層で、head を含む最初の行から tail を含む行までの箱＝束の絵の割合 (x0, y0, x1, y1)。章ファイルの trim に写す値"""
    import fitz
    db = json.loads(DB.read_text(encoding="utf-8"))
    name = next((n for n, r in db.items() if r["code"] == code), None)
    rec = db.get(name) if name else None
    if not rec or "src_rec" not in rec:
        raise SystemExit(f"🔴 {code} は束に頁として無い（build を先に）")
    sr = rec["src_rec"]
    pg = fitz.open(HERE / sr["pdf"])[sr["pdf_page"] - 1]
    lines = _lines(pg)
    i0 = next((i for i, (t, _) in enumerate(lines) if head in t), None)
    if i0 is None:
        raise SystemExit(f"🔴 {code}: 「{head}」の行が無い")
    i1 = next((i for i in range(i0, len(lines)) if tail in lines[i][0]), None)
    if i1 is None:
        raise SystemExit(f"🔴 {code}: 「{head}」より後に「{tail}」の行が無い")
    sel = lines[i0:i1 + 1]
    k, (bx, by, _, _) = sr["scale"], sr["box_px"]
    sx0, sx1 = min(b[0] for _, b in sel), max(b[2] for _, b in sel)
    top, bot = min(b[1] for _, b in sel), max(b[3] for _, b in sel)
    over = [b for _, b in lines if b[0] < sx1 and b[2] > sx0]
    above = [b[3] for b in over if b[3] <= top + 1 and b[1] < top - 1]
    below = [b[1] for b in over if b[1] >= bot - 1 and b[3] > bot + 1]
    yt = (max(above) + top) / 2 if above else top - pad / k
    yb = (min(below) + bot) / 2 if below else bot + pad / k
    x0, x1 = sx0 * k - bx - pad, sx1 * k - bx + pad
    y0, y1 = yt * k - by, yb * k - by
    w, h = rec["w"], rec["h"]
    box = [max(0.0, x0 / w), max(0.0, y0 / h), min(1.0, x1 / w), min(1.0, y1 / h)]
    print(f"{code}: 行 {i0}〜{i1}（{len(sel)}行）")
    print(f"  trim=({box[0]:.3f}, {box[1]:.3f}, {box[2]:.3f}, {box[3]:.3f})  縦横比 {(box[2] - box[0]) * w / ((box[3] - box[1]) * h):.2f}（字の層だけ）")
    return 0


# ── 写真 ───────────────────────────────────────────────────────
def _shrink(im):
    from PIL import Image
    w1, h1 = im.size
    k = min(1.0, max(BUNDLE_W / w1, BUNDLE_H / h1))
    if k < 1.0:
        im = im.resize((round(w1 * k), round(h1 * k)), Image.LANCZOS)
    return im, k


def _to_srgb(im):
    """色の札が sRGB でなければ sRGB の RGB に直す。戻り＝(絵, 何をしたか)"""
    from PIL import ImageCms
    icc = im.info.get("icc_profile")
    if not icc:
        return im.convert("RGB"), "札なし（sRGB と読む）"
    src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
    desc = ImageCms.getProfileDescription(src).strip()
    if im.mode != "CMYK" and (desc.startswith("sRGB") or desc == "c2"):
        return im.convert("RGB"), f"札 {desc}（sRGB のまま）"
    # 🆕 26本目 ⑤b-2（10-27）：灰色の写真（L・I;16）に灰色の札（Gray Gamma ほか）＝lcms は灰色→sRGB の変換を組めない（cannot build transform）
    #    ＝灰色の値をそのまま RGB の3色に（色は変えない＝原色のまま）。灰色の絵に sRGB の札（GIMP built-in sRGB＝S1-013・S1-042）も同じ
    if im.mode in ("L", "LA", "I", "I;16", "1") and (src.profile.xcolor_space.strip() == "GRAY" or "sRGB" in desc):
        return im.convert("L").convert("RGB"), f"{im.mode} 灰色の絵・札 {desc} → 灰色のまま RGB"
    out = ImageCms.profileToProfile(im, src, ImageCms.createProfile("sRGB"), renderingIntent=1, outputMode="RGB")
    return out, f"{im.mode} 札 {desc} → sRGB"


def load_photo(path):
    """元の写真を読む（向きの札を当て・sRGB に）＝(絵, 記録の言葉の並び)"""
    from PIL import Image, ImageOps
    notes = []
    with Image.open(path) as im0:
        ori = im0.getexif().get(274)
        im = ImageOps.exif_transpose(im0)
        if ori and ori != 1:
            notes.append(f"EXIF の向き {ori} を当てた（生の絵 {im0.size[0]}x{im0.size[1]}）")
        im.info["icc_profile"] = im0.info.get("icc_profile")
        im, how_c = _to_srgb(im)
    notes.append(how_c)
    return im, notes


def mosaic(im, boxes, n):
    """顔の範囲だけを升目にする（縮めて NEAREST で戻す）＝16・17・20・23・25本目と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def _src_ok(code, s, fet):
    """手元の元のファイルが取得の記録（md5 を2回＝同じ）と同じか＝md5。違えば止める"""
    p = HERE / s["file"]
    if not p.exists():
        raise SystemExit(f"🔴 {code}: 手元のファイルが無い（{s['file']}）")
    r = fet.get(code)
    if not r:
        raise SystemExit(f"🔴 {code}: 取得の記録が無い（fetch26.tsv）")
    h = md5(p)
    if r["md5_1"] != r["md5_2"] or h != r["md5_1"] or (HERE / r["file"]).resolve() != p.resolve():
        raise SystemExit(f"🔴 {code}: {p.name} の md5 が fetch26.tsv と合わない（取り直す）")
    return h


_YEAR = re.compile(r"((?:18|19|20)\d\d)年(?!代|ごろ|以前|以降|〜)")


def year_of(code, s):
    if code in YEAR_FIX:
        return YEAR_FIX[code]
    if s["type"] in PAGE_TYPES:
        return doc_year(_page_ref(s)[0])
    for col in ("title", "basis"):
        m = _YEAR.search(s[col])
        if m and not re.search(r"\d〜$", s[col][:m.start()]):
            return int(m.group(1)), f"sources26.psv の {col} の欄「{m.group(0)}」（映像方針＝Commons の頁・置き場の説明で読んだ）"
    return None, "撮影の年の出どころが無い（sources26.psv の題と根拠の欄に年が無い）"


def screen_credit(code, s, face_mask):
    """画面の出典の行（了承② 決め4）＝sources26 の出典の欄のまま（機関の名・Wikimedia Commons（パブリックドメイン）・頁は資料名と頁・
    MAIB は「…より引用」）。NOAA 2003 は原文の courtesy の表記（撮影者は印 {作者}）。顔だけ升目は「・改変：顔にモザイク」"""
    cr = s["credit"]
    if s["type"] == "maib-page":
        if code not in MAIB_PAGE:
            raise SystemExit(f"🔴 {code}: MAIB の頁の頁番号が表 MAIB_PAGE に無い")
        cr = f"{MAIB_TITLE} {MAIB_PAGE[code]}より引用"
    if "［撮影者］" in cr:
        cr = re.sub(r"（撮影者の名は[^）]*）$", "", cr).replace("［撮影者］", AUTHOR)
    if "［" in cr or "（⑤b" in cr:
        raise SystemExit(f"🔴 {code}: 出典の欄に書きかけの印が残る（{cr[:60]}）")
    if face_mask:
        if s["type"] not in PHOTO_TYPES or not s["rights"].startswith("PD"):
            raise SystemExit(f"🔴 {code}: 顔の升目は PD の写真だけ（{s['rights']}）")
        cr += "・改変：顔にモザイク"
    return cr


def who_table(code, s):
    """CREDITS.md の撮影者の欄（名前は書かない）"""
    t = s["type"]
    if AUTHOR in screen_credit(code, s, False):
        return "NOAA の頁の courtesy の撮影者（名前は git の外 `ref/ep26/src/credits_private.tsv` の (sources26, 記号) の行）"
    if t == "commons-photo":
        m = re.match(r"出典：(.+)$", s["credit"])
        return f"{m.group(1)}（Commons の版）" if m else "Commons の表記（撮影者の死後70年超・1912年以前の刊行など＝sources26 の根拠の欄）"
    if t == "report-page":
        return "英国の審問（Wreck Commissioner）の報告を米国上院が刷り直した公文書"
    if t == "maib-page":
        return "英国運輸省 海難調査局（MAIB）"
    if t == "law-page":
        return "米国議会（法）"
    return s["credit"]


# ── 束を作る ─────────────────────────────────────────────────
def cmd_build():
    src, fet, names = _sources(), _fetched(), _names()
    db, bad = {}, 0
    us = uses()
    for code in list(PAGE_CROP) + list(PHOTO_CROP) + list(MASK):
        if code not in us:
            print(f"🔴 PAGE_CROP・PHOTO_CROP・MASK の {code} は一覧で使っていない")
            bad += 1
    for code, cuts in sorted(us.items()):
        s = src[code]
        name = bundle_name(code)
        dst = EPD / f"{name}.jpg"
        page = s["type"] in PAGE_TYPES
        rec = {}
        if page:
            im, rec = render_page(code, s, names)
            notes = [rec["how"]]
            smd5 = rec["pdf_md5"]
        else:
            smd5 = _src_ok(code, s, fet)
            im, notes = load_photo(HERE / s["file"])
            pc = PHOTO_CROP.get(code)
            if pc:
                (fx0, fy0, fx1, fy1), why = pc
                W0, H0 = im.size
                cb = (round(fx0 * W0), round(fy0 * H0), round(fx1 * W0), round(fy1 * H0))
                im = im.crop(cb)
                rec = dict(crop_src_px=list(cb), crop_src_size=[W0, H0])
                notes.append(f"🔴 名前の外を切り出し（{why}）＝元の絵の {cb}")
            im, k = _shrink(im)
            if k < 1.0:
                notes.append(f"縮小 ×{k:.3f}")
            notes.append("fetch26.tsv の md5 と同じ（2回とも）")
        box_m = MASK.get(code, [])
        if box_m:
            im = mosaic(im, box_m, MOSAIC_PX)
            notes.append(f"顔だけ升目 {len(box_m)}か所（升 {MOSAIC_PX}px）")
        im.save(dst, quality=JPEG_Q, optimize=True)
        w, h = im.size
        r_ = s["rights"]
        if not (r_ == "PD" or r_.startswith("courtesy") or r_.startswith("引用")):
            print(f"🔴 {code}: 権利の記号が読めない（{r_}）")
            bad += 1
            continue
        frame = r_.startswith("引用")          # MAIB の頁＝引用の型＝無加工・額装（了承② 決め3）
        y, ywhy = year_of(code, s)
        cr = screen_credit(code, s, bool(box_m))
        db[name] = dict(code=code, part="", file=s["file"], cut=" ".join(cuts), credit=cr, who=who_table(code, s),
                        note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                        md5=md5(dst), src_md5=smd5, lic=r_, frame=frame, ground=s["basis"][:120], url=s["page"] or s["file"],
                        blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=False, page=page, related=False,
                        quote_page=page, named=AUTHOR in cr, mosaic=[list(b[:4]) for b in box_m] or None, name_mosaic=None,
                        masked_before=MASKED_BEFORE.get(code), era=s["era"], people=s["people"], **({"src_rec": rec} if rec else {}))
        print(f"✓ {code:10} {name:10} {w}x{h:<5} {' '.join(cuts):16} {r_[:12]}{'  額装だけ' if frame else ''}"
              f"{'  頁' if page else ''}  {'・'.join(notes)[:90]}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    print(f"→ ref/ep26/assets.json（{len(db)}点・写真 {sum(1 for r in db.values() if not r['page'])}・頁 {sum(1 for r in db.values() if r['page'])}"
          f"・額装だけ {sum(1 for r in db.values() if r['frame'])}・作者の印 {sum(1 for r in db.values() if r['named'])}"
          f"・顔の升目 {sum(1 for r in db.values() if r['mosaic'])}・名前の外の切り出し {len(PHOTO_CROP) + len(PAGE_CROP)}"
          f"・束の大きさ {tot / 1e6:.1f}MB）")
    return 1 if bad else 0


def cmd_look(codes, out_name="look.jpg", width=960):
    """束の写真を並べた見本（2列）＝リポの外（SCRATCH）。記号（S1-002）か束の名（s1_002）を渡す"""
    from PIL import Image, ImageDraw
    db = json.loads(DB.read_text(encoding="utf-8"))
    ims = []
    for c in codes:
        ns = [n for n, r in db.items() if n == c or r["code"] == c]
        if not ns:
            raise SystemExit(f"🔴 {c} は束に無い（build を先に）")
        for n in ns:
            im = Image.open(EPD / f"{n}.jpg").convert("RGB")
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            ImageDraw.Draw(im).rectangle((0, 0, 170, 40), fill=(0, 0, 0))
            ImageDraw.Draw(im).text((8, 8), n, fill=(255, 255, 0))
            ims.append(im)
    cols = 2 if len(ims) > 1 else 1
    rows = [ims[i:i + cols] for i in range(0, len(ims), cols)]
    H = sum(max(x.height for x in r) for r in rows) + 8 * (len(rows) - 1)
    sheet = Image.new("RGB", (width * cols + 8 * (cols - 1), H), (40, 40, 40))
    y = 0
    for r in rows:
        for i, x in enumerate(r):
            sheet.paste(x, (i * (width + 8), y))
        y += max(x.height for x in r) + 8
    SCRATCH.mkdir(parents=True, exist_ok=True)
    p = SCRATCH / out_name
    sheet.save(p, quality=90)
    print(f"→ {p}（{sheet.size[0]}x{sheet.size[1]}）")
    return 0


def cmd_panel():
    """ルール 0b-34②：PANEL_AR＝束の縦横比の並びで、16:9 より縦長の側のいちばん大きな切れ目の中点。"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    ars = sorted((r["w"] / r["h"], n, r["w"], r["page"]) for n, r in db.items() if not Path(n).name.startswith("fb_"))
    for a, n, w, pg in ars:
        print(f"  {a:6.3f}  {n:30} 幅 {w}{'  頁' if pg else ''}{'  （1280 未満＝kind() は額装）' if w < 1280 else ''}")
    side = [x for x in ars if x[0] < 16 / 9]
    gaps = sorted(((side[i + 1][0] - side[i][0], side[i], side[i + 1]) for i in range(len(side) - 1)), reverse=True)
    for g, a, b in gaps[:4]:
        print(f"切れ目 {g * 100:5.1f}ポイント：{a[0]:.3f}（{a[1]}）→ {b[0]:.3f}（{b[1]}）＝中点 {(a[0] + b[0]) / 2:.4f}")
    return 0


def cmd_edges():
    """束の全点の四辺の暗い帯（門番 check_photo_edge.margins と同じ物差し）＝スライドの台紙の縁がある写真の名簿を決める"""
    sys.path.insert(0, str(HERE / "tools"))
    import check_photo_edge as PE
    db = json.loads(DB.read_text(encoding="utf-8"))
    hits = []
    for n in sorted(db):
        m = PE.margins(f"ep26/{n}.jpg")
        mx = max(m.values())
        flag = "🔴" if mx >= PE.MIN_EDGE else ("・" if mx > 0 else " ")
        if mx > 0:
            hits.append((n, m))
        print(f"{flag} {n:30} 左 {m['l'] * 100:4.1f}% 上 {m['t'] * 100:4.1f}% 右 {m['r'] * 100:4.1f}% 下 {m['b'] * 100:4.1f}%{'  頁' if db[n]['page'] else ''}")
    big = [n for n, m in hits if max(m.values()) >= PE.MIN_EDGE]
    print(f"→ 暗い帯のある点 {len(hits)}（うち {PE.MIN_EDGE * 100:.1f}% 以上 {len(big)}＝{' '.join(big) or 'なし'}）")
    return 0


# ── 名前の門番（絵の OCR × git の外の名前の表）──────────────────────
def _ocr(files):
    sys.path.insert(0, str(HERE / "tools"))
    import check_slide as CS
    out = {}
    for i in range(0, len(files), 12):              # ocr_win.ps1 は1回の引数が長すぎると落ちる＝12枚ずつ
        out.update(CS.run_ocr(files[i:i + 12]))
    return out


def scan_names(files, names):
    """{ファイル名: ([伏せた名前…], 行の数)}＝OCR の行ごとと、ファイル全体をつないだ字（行をまたぐ名前）の両方で探す"""
    o = _ocr([str(f) for f in files])
    hits = {}
    for f in files:
        v = o.get(Path(f).name)
        if v is None:
            raise SystemExit(f"🔴 {Path(f).name} の OCR が返らない（fail closed）")
        found = []
        for ln in v["lines"]:
            found += hits_in(ln["text"], names)
        found += [w for w in hits_in(" ".join(ln["text"] for ln in v["lines"]), names) if w not in found]
        hits[Path(f).name] = (found, len(v["lines"]))
    return hits


def cmd_names(args):
    names = _names() + _author_res()
    if args and args[0] == "--selftest":
        return names_selftest(names)
    files = []
    for a in args:
        p = Path(a)
        files += sorted(p.glob("*.png")) + sorted(p.glob("*.jpg")) if p.is_dir() else [p]
    if not args:
        db = json.loads(DB.read_text(encoding="utf-8"))
        files = [EPD / f"{n}.jpg" for n, r in sorted(db.items()) if r["page"] or r["code"] in PHOTO_CROP]
    if not files:
        print("🔴 絵が0枚（fail closed）")
        return 2
    res = scan_names(files, names)
    bad = 0
    for fn, (found, nl) in res.items():
        if found:
            bad += 1
            print(f"🔴 {fn}: 名前 {len(found)}件（{sorted(set(found))}）")
        elif nl == 0:
            print(f"⚠️ {fn}: OCR の行 0（字の無い絵か読めない絵＝名前も無い）")
    print(f"→ 名前の門番：絵 {len(res)}枚・名前の表 {len(names)}語・当たり {bad}枚" + ("" if bad else "＝✓"))
    return 1 if bad else 0


# 🔴 この PC の OCR は日本語の読み手だけ（英語の認識の言語が入っていない）＝英字は崩れて読まれる（映像方針 §8）。
#    名前の網は2つ重ねる：① 字の層の網（`render_page`＝名前の字の箱が束の絵に入れば束を作らずに止める・PDF の頁だけ）
#    ② 絵の OCR の網（この `names`＝焼いた絵・字の層の無い写真の紙面も見られる）。② が英字を拾えるかは selftest の陽性対照で毎回測る
def names_selftest(names):
    """陽性対照＝名前の載る頁をまるごと（切らずに）描いた絵で、OCR が名前を拾うか（拾わなければ門番は何も測っていない）。
    陰性対照＝束の名前の外を切り出した絵で 0件。＋字の層の網の陽性対照＝名前の載る頁のまるごとに名前の字の箱がある"""
    import fitz
    from PIL import Image
    src = _sources()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    pos = []
    for code in PAGE_CROP:
        name, no = _page_ref(src[code])
        pg = fitz.open(pdf_path(name))[no - 1]
        k = PAGE_LONG / max(pg.rect.width, pg.rect.height)
        pix = pg.get_pixmap(matrix=fitz.Matrix(k, k), alpha=False)
        p = SCRATCH / f"names_pos_{bundle_name(code)}.jpg"
        Image.frombytes("RGB", (pix.width, pix.height), pix.samples).save(p, quality=JPEG_Q)
        pos.append((code, p))
    for code, ((fx0, fy0, fx1, fy1), _why) in PHOTO_CROP.items():
        im, _ = load_photo(HERE / src[code]["file"])
        p = SCRATCH / f"names_pos_{bundle_name(code)}.jpg"
        im.save(p, quality=JPEG_Q)
        pos.append((code, p))
    neg = [EPD / f"{bundle_name(c)}.jpg" for c in list(PAGE_CROP) + list(PHOTO_CROP)]
    if not pos:
        print("🔴 陽性対照が0（名前の外を切り出した点が無い＝この selftest は何も測らない）")
        return 1
    res = scan_names([p for _, p in pos] + neg, names)
    ok = True
    blind = 0
    # 🔴 ⑤b-2（10-27）の実測＝この PC の OCR は英字の名前を7件中6件拾わない（日本語の読み手だけ＝英字が崩れる）＝OCR の見落としは
    #    selftest の不合格にしない（⚠️ で数を出す）。英字の名前は ① 字の層の網（頁）② 束の段の切り出しを原寸で見る（写真の紙面）が受け持つ
    for code, p in pos:
        found, nl = res[p.name]
        print(f"  {'OK' if found else '⚠️ 見落とし'} 陽性対照 {p.name}（切らずに）：名前 {len(found)}件・OCR の行 {nl}")
        blind += not found
    for p in neg:
        found, _ = res[p.name]
        print(f"  {'OK' if not found else '🔴 NG'} 陰性対照 {p.name}（束）：名前 {len(found)}件")
        ok &= not found
    for code, spec in PAGE_CROP.items():
        name, no = _page_ref(src[code])
        pg = fitz.open(pdf_path(name))[no - 1]
        nb = name_boxes(pg, names)
        anc = [a for a in spec.get("outside", []) if any(a in t for t, _ in _lines(pg))]
        if nb:
            print(f"  OK 字の層の網の陽性対照 {code}（頁まるごと）：名前の字 {len(nb)}字")
        elif anc and len(anc) == len(spec.get("outside", [])):
            print(f"  OK 字の層の目印の陽性対照 {code}（頁まるごと）：名前は字の層に無い（署名は絵だけ）＝目印の行 {len(anc)}つが頁にあり、"
                  "束を作るときに切り口の外かを測る")
        else:
            print(f"  🔴 NG 字の層の網の陽性対照 {code}（頁まるごと）：名前の字 0字・目印の行 {len(anc)}")
            ok = False
    if blind:
        print(f"  ⚠️ OCR の網は陽性対照 {blind}/{len(pos)} を拾わない＝英字の名前は OCR だけに任せられない（字の層の網と原寸の目で受け持つ）")
    print("→ selftest " + ("合格" if ok else "🔴 不合格"))
    return 0 if ok else 1


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
# 出典の行の字幅の上限の目安（全角＝1・半角＝0.55）＝23本目の写真の出典の行で門番 layout を通って公開された最長 56.5。本当の物差しは門番 layout
CREDIT_W_MAX = 56.5


def _width(s):
    return sum(1.0 if unicodedata.east_asian_width(c) in "WF" else 0.55 for c in s)


def cmd_credits(write=False):
    """撮影年＝year_of（出どころつき）。当てたカットの副題が名乗る年（「NNNN年」・「当日」＝1912）と食い違えば止める（写真も頁も＝check_credits と同じ）。
    作者の名乗り（scene_jiko._ep26_author）を当てて出典の行の字幅を測る（名前は出さない＝字数だけ）"""
    sys.path.insert(0, str(HERE / "tools"))
    import scene_jiko as SJ
    db = json.loads(DB.read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    names = _names() + _author_res()
    cj, rows, bad = {}, [], 0
    for n, r in sorted(db.items()):
        cuts = r["cut"].split()
        claims = set()
        for c in cuts:
            claims |= {int(y) for y in re.findall(r"(1[89]\d\d|20\d\d)年(?!代|ごろ|以前)", subs.get(c, ""))}
            if "当日" in subs.get(c, ""):
                claims.add(EVENT_YEAR)
        y = r["year"]
        if claims and (y is None or claims != {y}):
            print(f"🔴 {n}: 副題の年 {sorted(claims)} と撮影年 {y} が食い違う（{' '.join(cuts)}・{subs.get(cuts[0], '')}）＝{r['year_why'][:60]}")
            bad += 1
        leak = hits_in(json.dumps(r, ensure_ascii=False), names)
        if leak:
            print(f"🔴 {n}: 台帳の行に出さない名前が入っている（{len(leak)}語）")
            bad += 1
        line = r["credit"]
        if AUTHOR in line:
            try:
                line = line.replace(AUTHOR, SJ._ep26_author(f"ep26/{n}.jpg"))
            except Exception as e:                         # noqa: BLE001  焼く前に止める
                print(f"🔴 {n}: 作者の名乗りが作れない（{e}）")
                bad += 1
        wd = _width(line)
        if wd > CREDIT_W_MAX:
            print(f"🔴 {n}: 出典の行の字幅 {wd:.1f}（{CREDIT_W_MAX} まで＝画面の左下からはみ出すおそれ）")
            bad += 1
        cj[f"ep26/{n}.jpg"] = r["credit"]
        kind = "頁" if r["page"] else "この事故"
        mod = "・顔に升目" if r.get("mosaic") else ("・名前の外を切り出し" if r["code"] in PHOTO_CROP or r["code"] in PAGE_CROP else "")
        rows.append(f"| `{n}` | {' '.join(cuts)} | {y if y else '不明'} | {r['lic']}（{kind}{mod}） | {r['who']} | {r['url']} |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真・頁 {len(cj)}点{'' if not bad else f'・🔴 {bad}'}")
    if bad:
        return 1
    if not write:
        return 0
    CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    film_rows = []
    if CLIPS.exists():
        cl = json.loads(CLIPS.read_text(encoding="utf-8"))
        lst = _list()
        for k, v in cl.items():
            film_rows.append(f"| `{k}` | {' '.join(r['cid'] for r in lst if r['code'] == k)} | {v['credit']} | {v['license']} | {v['url']} |")
    md = CREDITS_MD.read_text(encoding="utf-8")
    block = "\n".join([
        CREDITS_HEAD, "",
        "※2026-10-27（⑤b-2）。`qa_out/ep26_assets.py credits --write` が書く（手で直さない）。写真と頁は映像方針の一覧 `ref/ep26/eizou_list26.md`（了承② 2026-10-27）。",
        "",
        "### 0. 映像（音はすべて使わない＝`-an`）",
        "- **NOAA 2004 の残骸の映像**（N04＝米国海洋大気庁の Ocean Explorer の頁・5分53秒・640×426）＝頁の表記「Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE.」"
        "（copyright・© の語なし＝NOAA の使い方の方針で courtesy は表記つきで使える）。画面の出典の行はこの表記のまま。13区間（扉を除くカットの秒＝narration.json の実測・"
        "`ref/ep26/eizou_build/list26.tsv`）・字の焼き込みも人も無い（映像方針で16コマを原寸）。【映像あり】に数えない（了承②）。映像そのものは git に入れない"
        "（焼くときに頁の直リンクから丸ごと取る＝`footage.local_media`・md5 は `ref/ep26/clips.json`）",
        "- フリー素材（Pexels・生成AI は使わない）＝画面の左上に「イメージ」・出典の行は「イメージ（Pexels）」だけ（クレジットは任意＝投稿者の名前は書かない・"
        "概要欄にも書かない）。20% に数えない。🔴 映像そのものもひかえの静止画も git に入れない（19本目 決め⑨）＝26本目は8カット（⑤b-3 で取る）",
        "",
        "| 記号 | 使うカット | 画面の出典 | ライセンス | 頁 |",
        "|---|---|---|---|---|", *film_rows, "",
        "### 1. 写真・頁（Commons の PD・NOAA 2003・英国の審問の報告・MAIB 1992・米国の法）",
        "- Commons の PD＝出どころの機関の名（NARA・LOC・BnF・オランダ国立公文書館・北アイルランド国立博物館）か「Wikimedia Commons（パブリックドメイン）」（了承② 決め4）。"
        "色は原本のまま・小さい写真も全面（ぼけは差し替えの理由にしない）",
        "- NOAA 2003 の写真2点＝NOAA の頁の courtesy の表記（撮影者の個人名つき）。🔴 名前はこのリポに書かない＝`ref/ep26/credits.json` は印 `{作者}` だけ・"
        "焼くときに git の外の表から足す（`tools/scene_jiko.ep26_credit`）",
        "- 英国の審問の報告（米国上院の刷り直し S. Doc. 933）・米国の法＝米国の公文書（PD）＝出典の行は資料名と頁。MAIB 1992＝引用の型（出典・主従・必要最小限・"
        "**無加工の額装**＝`frame`）",
        "- 🔴 **人は名前＋役職か役職だけ・乗客は名前なし（①・承認①）**＝会社の人・議員の名（ネガの字）・MAIB の署名・電信会社の社長の名・カリフォルニアン号の"
        "機関部の乗組員の名前は束の段で切り出しの外（`qa_out/ep26_assets.py` の PHOTO_CROP・PAGE_CROP）。乗客の顔が分かる所は顔だけ升目（PD・MASK）",
        "- 撮影年＝Commons の頁と置き場の説明の年（sources26 の題・根拠の欄）・NOAA の頁（2003）・頁は資料の年。年の分からない点は「不明」（副題に年を書かない）",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, "",
        "### 2. 地図の衛星写真（Google マップ）",
        "- c218・c306・c909・c917＝Google マップの衛星写真＋描き足し（束の外＝`cuts/ss.SAT`・⑤b-3 で撮る）。出典は画面の地図の右下の帰属の行（Google の地図の利用）。"
        "🔴 PNG は公開リポに置かない（git の外・md5 と出どころは `cuts/ss.SAT`・`GEO`）",
        ""])
    if CREDITS_HEAD in md:
        pre, rest = md.split(CREDITS_HEAD, 1)
        nxt = rest.find("\n## ")
        md = pre + block + (rest[nxt:] if nxt >= 0 else "")
    else:
        md = md.rstrip("\n") + "\n\n" + block
    CREDITS_MD.write_text(md, encoding="utf-8", newline="\n")
    print(f"→ {CREDITS_JSON.relative_to(HERE).as_posix()} ／ {CREDITS_MD.relative_to(HERE).as_posix()}")
    return 0


# ── 映像：NOAA 2004（⑤b-2）・フリー素材（⑤b-3）＝台帳・ショット・見取り図・USE・ひかえ ──────────────
def _film_codes(kinds=("stock", "noaa-video")):
    """映像の記号 → 使うカット（一覧の順）"""
    src = _sources()
    out = {}
    for r in _list():
        s = src.get(r["code"], {})
        if s.get("type") in kinds:
            out.setdefault(r["code"], []).append(r["cid"])
    return out


def _probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,sample_aspect_ratio:format=duration", "-of", "json", str(p)],
                       capture_output=True, text=True, timeout=120)
    if r.returncode:
        raise SystemExit(f"🔴 ffprobe が読めない：{p}（{r.stderr[-200:]}）")
    j = json.loads(r.stdout)
    st = j["streams"][0]
    a, b = st["r_frame_rate"].split("/")
    return dict(w=int(st["width"]), h=int(st["height"]), fps=round(int(a) / int(b), 3),
                sar=st.get("sample_aspect_ratio") or "1:1", sec=float(j["format"]["duration"]))


def _head(u):
    req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, int(r.headers.get("Content-Length") or 0), r.headers.get("Content-Type") or ""


# NOAA 2004 の映像の取得（映像方針 10-27）＝大きさと md5 の頭（sources26 の注「33,946,045 bytes＝HEAD と一致・md5 d1375766 を2回」）
NOAA_SIZE, NOAA_MD5_HEAD = 33946045, "d1375766"


def _media_url(code, size, rec):
    """🆕 ⑤b-3（10-27）：Pexels の直リンク＝取得の記録（fetch26.tsv の url_kind＝`stock:<直リンク>`）の URL を HEAD で照らし、
    大きさが手元と同じなら返す（違えば止める）。25本目 `_media_url` の記録の枝だけ（新しい素材の名の形は番号から組めない）"""
    try:
        st, n, ct = _head(rec)
    except Exception as e:                                   # noqa: BLE001
        raise SystemExit(f"🔴 {code}: 記録の直リンクを引けない（{rec}・{e}）")
    if st != 200 or n != size or not ct.startswith("video/"):
        raise SystemExit(f"🔴 {code}: 記録の直リンクが手元と違う（http {st}・{n} B／手元 {size} B・{ct}）")
    return rec


def cmd_clips():
    """clips.json＝NOAA 2004（公的な機関の頁の直リンク＝焼くときに丸ごと取る）・フリー素材（Pexels＝取得の記録の直リンク＝🆕 ⑤b-3）"""
    src, fet = _sources(), _fetched()
    out = json.loads(CLIPS.read_text(encoding="utf-8")) if CLIPS.exists() else {}
    for code, cuts in _film_codes(("stock",)).items():
        s = src[code]
        p = HERE / s["file"]
        r = fet.get(code) or {}
        if not p.exists() or not r or md5(p) != r["md5_1"] or not r["url_kind"].startswith("stock:http"):
            raise SystemExit(f"🔴 {code}: 手元の映像が無いか md5 が取得のときと違う（{s['file']}）＝fetch26.py stock で取る")
        size = p.stat().st_size
        media = _media_url(code, size, r["url_kind"][6:])
        loc = _probe(p)
        out[code] = dict(url=s["page"], media=media, stock=True, file=s["file"].removeprefix("ref/"), credit="イメージ（Pexels）", src="stock",
                         at=0.0, what=s["title"][:60], w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"], sec=round(loc["sec"], 3),
                         size=size, md5=r["md5_1"], dispw=loc["w"], decoded=[loc["w"], loc["h"]], license="Pexels License",
                         license_url="https://www.pexels.com/license/", site="Pexels")
        print(f"  {code:13} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:7.2f}秒 {size / 1e6:.1f}MB  {' '.join(cuts)}  {media.rsplit('/', 1)[-1]}")
    for code, cuts in _film_codes(("noaa-video",)).items():
        s = src[code]
        p = HERE / s["file"]
        if not p.exists():
            raise SystemExit(f"🔴 {code}: 手元の映像が無い（{s['file']}）")
        h, size = md5(p), p.stat().st_size
        if size != NOAA_SIZE or not h.startswith(NOAA_MD5_HEAD):
            raise SystemExit(f"🔴 {code}: 手元の映像が取得のときと違う（{size} B・md5 {h[:8]}／記録 {NOAA_SIZE} B・{NOAA_MD5_HEAD}）")
        media = s["get"].removeprefix("http:")
        st, n, ct = _head(media)
        if st != 200 or n != size or not ct.startswith("video/"):
            raise SystemExit(f"🔴 {code}: 頁の直リンクが手元と違う（http {st}・{n} B／手元 {size} B・{ct}）")
        loc = _probe(p)
        out[code] = dict(url=s["page"], media=media, stock=False, file=s["file"].removeprefix("ref/"), credit=s["credit"], src="noaa",
                         at=0.0, date="2004", what=s["title"][:80], w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"],
                         sec=round(loc["sec"], 3), size=size, md5=h, dispw=loc["w"], decoded=[loc["w"], loc["h"]],
                         license="courtesy（NOAA の使い方の方針・copyright の語なし）", rights=s["basis"], scan=s["file"], md5_scan=h,
                         note="音は使わない（-an）。0〜9.5秒と346秒〜は黒。字の焼き込みも人も無い（映像方針で16コマを原寸）")
        print(f"  {code:6} {loc['w']}x{loc['h']} {loc['fps']}fps {loc['sec']:7.2f}秒 {size / 1e6:.1f}MB  {' '.join(cuts)}  HEAD {st} {ct}")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep26/clips.json（{len(out)}本）")
    return 0


# 🔴 NOAA 2004 の映像は**溶け合う転換**（ffmpeg の scene では切れ目が1〜3か所しか出ない＝映像方針 §8）＝ショットの表は
#    2コマ/秒・64×36 の灰色の絵の「隣のコマとの差」が、**前後6秒（真ん中の±1秒を除く）の差の中央値の NOAA_RATIO 倍**を超えて跳ねる所で割る。
#    ⚠️ 1回目（10-27）は「映像全体の中央値の3倍」と「場面の頭のコマとの差 28」で割った＝ROV のカメラが動き続ける所（105〜137秒＝隣の差が 10〜27 の
#       まま続く）を0.5秒ずつに刻んだ（61場面）。動き続ける映像は高い差がずっと続く＝前後と比べた跳ねだけを切り替わりと読む（147秒の
#       4.9→17.8→1.7 は前後の約3倍＝帳簿の「浴槽（147〜161秒）」の頭と合う）。shots.shots_of（1秒1コマ）も ROV の映像では境目を出しすぎる＝使わない
# 🆕 ⑤b-3：フリー素材で、動きの速い素材の隣の1秒の差がしきい値を超えて出た「境目」を、根拠つきで1ショットに直す（25本目 SHOT_ONE の型）
#   根拠＝境目の前後の全コマの隣の差に、1コマに集まる跳ねが無い（切り替わりなら1コマに集まる）。⚠️ 記号は素材を替えても同じ＝替えたら測り直す
SHOT_ONE = {}
NOAA_STEP = 0.5          # 秒（2コマ/秒）
NOAA_RATIO = 2.5         # 隣のコマとの差が、前後6秒の中央値の何倍を超えたら切り替わり
NOAA_FLOOR = 7.0         # かつ、この差（灰色 0〜255 の平均の差＝映像全体の上位 25% の境）以上


def _noaa_frames(p, step=NOAA_STEP):
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"fps=1/{step},scale=64:36", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True, timeout=900)
    a = np.frombuffer(r.stdout, dtype=np.uint8)
    n = len(a) // (64 * 36)
    return a[:n * 64 * 36].reshape(n, 36, 64).astype(float)


def noaa_shots(p):
    """[(start, until, motion)]＝暗い所（0〜9.5秒・346秒〜）は場面にしない"""
    import numpy as np
    f = _noaa_frames(p)
    n = len(f)
    lum = f.mean(axis=(1, 2))
    d = np.r_[0, np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))]
    med = float(np.median(d[1:]))
    w, gap = int(6 / NOAA_STEP), int(1 / NOAA_STEP)

    def cut(i):
        around = np.r_[d[max(1, i - w):max(1, i - gap)], d[i + gap + 1:i + w + 1]]
        base = float(np.median(around)) if len(around) else med
        peak = d[i] >= d[max(1, i - 2):i + 3].max()
        return peak and d[i] >= NOAA_FLOOR and d[i] >= NOAA_RATIO * base
    shots, s0 = [], None
    for i in range(n):
        t = i * NOAA_STEP
        dark = lum[i] < 12
        if dark:
            if s0 is not None:
                shots.append((s0, t))
                s0 = None
            continue
        if s0 is None:
            s0 = t
            continue
        if cut(i):
            shots.append((s0, t))
            s0 = t
    if s0 is not None:
        shots.append((s0, n * NOAA_STEP))
    out = []
    for a, b in shots:
        i0, i1 = int(a / NOAA_STEP), int(b / NOAA_STEP)
        out.append(dict(start=round(a, 2), until=round(b, 2), motion=round(float(d[i0 + 1:i1].mean()) if i1 > i0 + 1 else 0.0, 2)))
    return out, n * NOAA_STEP, med


def cmd_shots():
    """shots.json＝NOAA は noaa_shots（2コマ/秒・溶け合う転換も拾う）・フリー素材は tools/shots.shots_of（1秒1コマ）"""
    sys.path.insert(0, str(HERE / "tools"))
    src = _sources()
    out = json.loads(SHOTS.read_text(encoding="utf-8")) if SHOTS.exists() else {}
    for code in _film_codes():
        s = src[code]
        p = HERE / s["file"]
        if s["type"] == "noaa-video":
            sh, dur, med = noaa_shots(p)
            how = (f"⑤b-2（10-27）：2コマ/秒・64×36 の灰色＝隣のコマとの差が前後6秒（±1秒を除く）の中央値の {NOAA_RATIO} 倍以上・{NOAA_FLOOR} 以上で"
                   f"前後2コマの山（映像全体の中央値 {med:.2f}）＝別の場面。暗い所（平均の明るさ 12 未満）は場面にしない")
        else:
            if not p.exists():
                print(f"  ⚠️ {code}: 手元に無い（⑤b-3 で取る）")
                continue
            import shots as SH
            sh, dur = SH.shots_of(p)
            how = "1秒1コマで tools/shots.shots_of（26本目・フリー素材）"
            if code in SHOT_ONE:
                sh = [dict(start=0.0, until=float(sh[-1]["until"]), motion=max(x["motion"] for x in sh))]
                how += f"・🔧 1ショットに直した（{SHOT_ONE[code]}）"
        out[code] = dict(src=s["page"], scan=s["file"], dur=round(dur, 1), how=how, shots=sh)
        print(f"  {code:12} {dur:6.1f}秒  ショット {len(sh)}：" + " ".join(f"{x['start']:g}〜{x['until']:g}" for x in sh))
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep26/shots.json（{len(out)}本）")
    return 0


def cmd_frames(code, step=1.0, width=384, cols=5):
    """映像の step 秒ごとのコマを並べた見取り図（秒の札つき）＝区間を選ぶとき（out/ep26_look/frames_<記号>.jpg）"""
    from PIL import Image, ImageDraw
    s = _sources()[code]
    p = HERE / s["file"]
    loc = _probe(p)
    hh = round(width * loc["h"] / loc["w"])
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", f"fps=1/{step},scale={width}:{hh}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, timeout=600)
    n = len(r.stdout) // (width * hh * 3)
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * width + (cols - 1) * 4, rows * hh + (rows - 1) * 4), (30, 30, 30))
    for i in range(n):
        im = Image.frombytes("RGB", (width, hh), r.stdout[i * width * hh * 3:(i + 1) * width * hh * 3])
        d = ImageDraw.Draw(im)
        d.rectangle((0, 0, 70, 20), fill=(0, 0, 0))
        d.text((4, 4), f"{i * step + step / 2:5.1f}s", fill=(255, 255, 0))
        sheet.paste(im, ((i % cols) * (width + 4), (i // cols) * (hh + 4)))
    SCRATCH.mkdir(parents=True, exist_ok=True)
    out = SCRATCH / f"frames_{code}.jpg"
    sheet.save(out, quality=88)
    print(f"→ {out}（{n}コマ・{sheet.size[0]}x{sheet.size[1]}・{loc['sec']:.2f}秒）")
    return 0


def _write_block(tag, lines):
    txt = FOOTAGE.read_bytes().decode("utf-8")
    nl = "\r\n" if "\r\n" in txt else "\n"              # 🔴 25本目 ⑤b-1 の落とし穴＝改行を見分ける
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_bytes((txt[:m.start(2)] + "".join(x + nl for x in lines) + txt[m.end(2):]).encode("utf-8"))


# NOAA の区間＝映像方針（`assign26.psv`）の区間を ⑤b-1 で実測の秒に合わせた値＝一覧 list26.tsv の動きの欄「映像（a〜b秒）」から読む（手で写さない）
# フリー素材の区間 {cid: (始め, 終わり, 理由)}・寄せ（footage.USE の zoom・bias・xbias）＝⑤b-3 で見取り図と原寸で決める
#   🆕 ⑤b-3（10-27）：明るさと色の推移（0.5秒ごと・明るい画素の彩度と RGB）で当たりを付け、640px のシート（6コマ）と原寸の切り出しで決めた。
#   書いていないカット（c401・c414・c638・cb05）は1ショットのまん中（cmd_use の既定）＝4本とも頭から尻まで同じ眺め（月・人・字なし）
STOCK_WINDOW = {
    "c517": (20.40, 25.50, "白い筋が上がる区間だけ（20.8〜25秒）＝14〜16秒の開花は橙と緑・28〜30秒の開花は桃色と橙＝白一色でない"),
    "c610": (0.30, 7.90, "頭がいちばん遠い（ドローンが船へ近づく映像＝あとほど船が大きい）"),
    "c939": (22.40, 29.70, "27秒の流れ星の筋を入れる（15秒の筋は淡い）"),
    "ca11": (2.90, 10.50, "赤い輪の開花（2.5・10秒）と上がる筋＝15秒からは白と金"),
}
STOCK_GEOM = {
    "ca11": dict(zoom=1.35, bias=0, xbias=1.0),     # 左の灯りの列（x 210〜480）と下の対岸の町の灯り（y 960〜）を画面の外へ（見える x 498〜1920・y 0〜800）
}
STOCK_EDGE = 0.3                # ショットの境目から離す秒（フリー素材＝1秒1コマで測った境目）


def _noaa_window(r):
    m = re.search(r"映像（([\d.]+)〜([\d.]+)秒）", r["motion"])
    if not m:
        raise SystemExit(f"🔴 {r['cid']}: 一覧の動きの欄に NOAA の区間「映像（a〜b秒）」が無い（{r['motion']}）")
    return float(m.group(1)), float(m.group(2))


def cmd_use(only=None, all_=False):
    """footage.USE の26本目の欄（🔴 章ファイルに `ss.vid` を書いたカットだけ・`only` は書く前の鶏と卵を割るため）"""
    sys.path.insert(0, str(HERE / "tools"))
    if only:
        secs, spec = {r["cid"]: float(r["cont"]) for r in _list()}, {}
    else:
        import footage as FO
        import scene_jiko as S
        secs, spec = FO.secs_of(), S.SPEC
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))
    src = _sources()
    lines, skip = [], []
    films = _film_codes()
    for r in _list():
        if r["code"] not in films:
            continue
        cid, code = r["cid"], r["code"]
        sp = spec.get(cid) or {}
        wrote = str(sp.get("photo") or "").endswith(f"fb_{cid}.jpg")
        if not (all_ or wrote or (only and cid in only)):
            skip.append(cid)
            continue
        need = float(secs[cid])
        shs = sd[code]["shots"]
        if src[code]["type"] == "noaa-video":
            a, b = _noaa_window(r)
            hit = [x for x in shs if x["start"] <= a < x["until"]]
            if len(hit) != 1 or b > hit[0]["until"] + 1e-6:
                raise SystemExit(f"🔴 {cid}: NOAA の区間 {a}〜{b} が1つの場面に収まらない（場面 {[(x['start'], x['until']) for x in hit]}）")
            sh = hit[0]
            rate = min(1.0, int((b - a) / need * 100) / 100)
            why = "・映像方針の区間（⑤b-1 で実測の秒に）"
        elif cid in STOCK_WINDOW:
            a, b = STOCK_WINDOW[cid][:2]
            hit = [x for x in shs if x["start"] <= a < x["until"]]
            if len(hit) != 1 or b > hit[0]["until"]:
                raise SystemExit(f"🔴 {cid}: 区間 {a}〜{b} が1つのショットに収まらない")
            sh = hit[0]
            rate = min(1.0, int((b - a) / need * 100) / 100)
            why = f"・{STOCK_WINDOW[cid][2]}"
        else:
            sh = max(shs, key=lambda x: x["until"] - x["start"])
            room = sh["until"] - sh["start"] - 2 * STOCK_EDGE
            if room >= need:
                a = round(sh["start"] + STOCK_EDGE + (room - need) / 2, 2)
                b, rate = round(a + need + 0.05, 2), 1.0
            else:
                a, b = round(sh["start"] + STOCK_EDGE, 2), round(sh["until"] - STOCK_EDGE, 2)
                rate = min(1.0, int(room / need * 100) / 100)
            why = ""
        if rate < STILL_BELOW:
            raise SystemExit(f"🔴 {cid}: 使える {b - a:.2f}秒／要る {need:.2f}秒＝{rate}＜{STILL_BELOW}（止め絵になる）")
        geo = "".join(f", {k}={v}" for k, v in STOCK_GEOM.get(cid, {}).items())
        lines.append(f'    "{cid}": dict(clip="{code}", start={a:.2f}, until={b:.2f}, rate={rate}{geo}),   '
                     f'# 場面 {sh["start"]:g}〜{sh["until"]:g}秒・使える {b - a:.2f}秒／要る {need:.2f}秒{why}')
    _write_block("EP26_USE", lines)
    print(f"→ tools/footage.py USE {len(lines)}欄")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルにまだ映像を書いていない：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵）＝区間の頭のコマを 1920×1080 に（寄せは USE と同じ式）。
    NOAA＝`ref/ep26/fb_<cid>.jpg`（git に入れる＝17・21本目の記録映像と同じ）・フリー素材＝`ref/ep26/stock/fb_<cid>.jpg`（🔴 git に入れない＝決め⑨）"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    from PIL import Image
    bad = 0
    (EPD / "stock").mkdir(exist_ok=True)
    for cid, u in FO.USE.items():
        if only and cid not in only:
            continue
        c = FO.CLIPS.get(u["clip"]) or {}
        if not c:
            continue
        p = HERE / "ref" / c["file"]
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{float(u['start']):.3f}", "-i", str(p), "-frames:v", "1",
                              "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if not raw:
            print(f"🔴 {cid}: コマが取れない")
            bad += 1
            continue
        im = Image.open(io.BytesIO(raw)).convert("RGB")
        sw, sh_ = im.size
        z = max(1920 / sw, 1080 / sh_) * float(u.get("zoom", 1.0))
        cw, ch = min(sw, 1920 / z), min(sh_, 1080 / z)
        lft, top = (sw - cw) * float(u.get("xbias", 0.5)), (sh_ - ch) * float(u.get("bias", 0.5))
        im = im.crop((round(lft), round(top), round(lft + cw), round(top + ch))).resize((1920, 1080), Image.LANCZOS)
        dst = EPD / ("stock" if c.get("stock") else "") / f"fb_{cid}.jpg"
        im.save(dst, quality=92)
        print(f"✓ {cid:5} {u['clip']:12} {float(u['start']):6.2f}秒 {sw}x{sh_} → {dst.relative_to(HERE).as_posix()}")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"build": cmd_build, "panel": cmd_panel, "edges": cmd_edges, "clips": cmd_clips, "shots": cmd_shots}
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] == "use":
        sys.exit(cmd_use(set(x for x in a[1:] if not x.startswith("--")) or None, "--all" in a))
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "look":
        sys.exit(cmd_look(a[1:]))
    if a and a[0] == "frames":
        sys.exit(cmd_frames(a[1], float(a[2]) if len(a) > 2 else 1.0))
    if a and a[0] == "lines":
        sys.exit(cmd_lines(a[1]))
    if a and a[0] == "pbox":
        sys.exit(cmd_pbox(a[1], a[2], a[3]))
    if a and a[0] == "names":
        sys.exit(cmd_names(a[1:]))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
