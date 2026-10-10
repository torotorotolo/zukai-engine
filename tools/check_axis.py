# -*- coding: utf-8 -*-
"""check_axis.py — 軸の型（年表・時間の帯・交信の帯＝`tools/axis.py`）の**値・画素・割れる時刻・交信の文字**を照合する
（2026-09-29 新設・14本目 ⑤b-5）。

■ なぜ要るか
  年表と時間の帯は「位置」が情報そのもの。点が1か月・1分ずれても字幕と画面が食い違う。
  🔴 §5b-88：門番が型の定数を正解として読むと、型を壊しても通る＝**記録の値はこの門番の側に持つ**（`REC_AXIS`）。
     値の読み方（年月日→年・時刻→分）も型（axis.val）を使わず、ここで別に書く。

■ 測るもの（本番の関数 `axis.axis()` が置いた部品の画素＝`f.mech` から）
  ① 値が記録の表 `REC_AXIS` にあり、部品の rec（頁）の1つが表の頁と合う（目盛りは記録でなく物差し＝照らさない）
  ② 画素：目盛りの画素の x と目盛りの文字（ここで読む）から一次式を当て、部品の x を値へ戻す＝書いた細かさの幅に入る
     （分＝±0.3分・日＝±0.6日・月＝その月の中・年＝その年の中）。目盛りの文字が目盛りの値の書き方と合うかも見る
  ③ 割れる時刻：split は1カットに2つ以上・値が2つ以上・形が同じ（色・大きさを変えない＝どれが正しいと描かない）。
     `cuts/ss.ILLU_SPLIT_TIMES` の時刻の点（pt）は出典の名を添える（by=True）
  ④ 交信の帯：link に文字が無い・段の名は `LANES_OK` だけ（私人の言葉を帯に書かない）
  ⑤ カーソルは記録の値（その段までに描いた部品の x）か軸の左端にだけ止まる
  ⑥ 🆕 19本目 ⑤b-5：秒まである時刻（±0.5秒）・基準からの「約○分前」（基準 ref も記録の表で照らす・札は「約7分前」）・
     並び order（値が時間の順＝門番の読み方 ORDER_UNIT で基準からの秒へ／点が同じ間隔／途切れの印が点のあいだに1つずつ／
     note に「間隔は時間に比例しない」）

■ 使い方
    python tools/check_axis.py              # 全カット
    python tools/check_axis.py --selftest   # 物差しの検算（陽性対照＝型の定数を壊す・記録と違う頁・一つだけの割れ）
"""
from __future__ import annotations

import datetime
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

# ══════════════════════════════════════════════════════════
#  🔴 §0b（題材を替えるとき空にする場所）：記録の値と頁（この回）。
#     🔴 2026-09-30（15本目 リノ ⑤b-1）：**空にした**。14本目（セウォル号）の表は selftest の見本 `tools/fixture_ep14.py`
#        （GATES["check_axis"]・値は1つも変えていない）。15本目の年表・時間の帯を書くチャットで、値と頁を
#        ref/ep15/src/ep15_pages.txt で当てて入れる（空のあいだ、軸のカットは「記録に無い値」で止まる＝fail closed）
#     🔴 2026-10-01（16本目 バイオントダム災害 ⑤b-1）：15本目の表（秒の帯・年表・時刻の帯・横転の前の秒）も**空にした**。
#        selftest の見本 `tools/fixture_ep15.py`（GATES["check_axis"]・値は1つも変えていない＝git の `c646174`）。
#        16本目の値は、軸の型を初めて使う ⑤b のチャットで、値と頁を ref/ep16/src/ep16_pages.txt で当てて入れる
#        （空のあいだ、軸のカットは「記録に無い値」で止まる＝fail closed）
#     🔴 2026-10-04（18本目 スレッシャー号 ⑤b-1）：16本目の表（10月9日の時刻の帯・年表＝第1〜11章）も**空にした**。
#        selftest の見本 `tools/fixture_ep16.py`（GATES["check_axis"]・値は1つも変えていない＝git の `b044b56`）。
#        18本目の値は、軸の型を初めて使う ⑤b のチャットで、値と頁を ref/ep18/src/ep18_pages.txt で当てて入れる
#        （空のあいだ、軸のカットは「記録に無い値」で止まる＝fail closed）
# ══════════════════════════════════════════════════════════
#     ✅ 2026-10-04（18本目 スレッシャー号 ⑤b-5）：18本目の値を入れた（2026-10-06 に下の4つは見本へ移した）。原文＝ref/ep18/src/ep18_pages.txt（頁の番号は
#        cuts/ss.REC_DOCS の通し番号＝R08 p4185＝第8回公開の PDF 185頁ほか）。公開の23回だけは原文が表＝海軍の台帳 xlsx（第1〜17回）と
#        公開の棚の更新日（第18〜23回＝2026-10-04 に棚の一覧で確かめた）＝rec は "台帳"・"棚"（頁なし）
#        ✅ 2026-10-06（19本目 ⑤b-1・§0b）：REC_AXIS・LANES_OK・REC_APPROX・REC_LANE を見本 `tools/fixture_ep18.py` へ移して空にした
#        （selftest_ep18 は見本を差して回す形に直した＝fixture_ep16 と同じ）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-06（19本目 スレッシャー号→サーフサイド ⑤b-1・§0b）：18本目の表（REC_AXIS・LANES_OK・REC_APPROX・REC_LANE と、2段の帯の段の名 _V・_M）も
#    **空にした**。selftest の見本 `tools/fixture_ep18.py`（GATES["check_axis"]・値は1つも変えていない＝git の `2d627a2`）。19本目の値は、軸の型を
#    初めて使う ⑤b のチャットで、値と頁を ref/ep19/src/ep19_pages.txt で当てて入れる（空のあいだ、軸のカットは「記録に無い値」で止まる＝fail closed）。
#    型の側（LANE_COL・tier_pierce・分の小数・「ごろ」・日の目盛り）は残す
# 🔴 2026-10-08（20本目 日本航空123便のリメイク ⑤b-1・§0b）：19本目の表（REC_AXIS＝建物の歩み・報告のあと・最後の3週間の並び・崩れる前の数分・捜索と調査・
#    決まり・裁判所／並び order の基準 ORDER_REF_MIN）も**空にした**。selftest の見本 `tools/fixture_ep19.py`（GATES["check_axis"]・値は1つも
#    変えていない＝git の `70c7e51`）。20本目の値は、軸の型を初めて使う ⑤b のチャットで、値と頁を ref/ep20/src/ep20_pages.txt で当てて入れる
#    （空のあいだ、軸のカットは「記録に無い値」で止まる＝fail closed）。型の側（LANE_COL・tier_pierce・分の小数・「ごろ」・日の目盛り・
#    秒まである時刻・基準 ref からの「約○分前」・並び order の物差し `ORDER_UNIT`・`ORDER_NOTE`・`_order_checks`）は残す。
#    頁の番号の書き方（TR p1NNN＝語りの行 NNN ほか）と引いた原文は移した注の側にある＝fixture_ep19 の REC_AXIS の上
# 🆕 2026-10-10（20本目 ⑤b-5）：時間の帯4カット（c210・c212・c214・c519）の値と頁（ref/ep20/src/ep20_pages.txt で当てた）。
#    報告書＝印刷の頁（別添6 は p310〜343）・解説＝1000＋印刷の頁
#    p6「18時24分35秒…「ドーン」というような音」・p88「18時24分37秒から約1秒間鳴り、26秒間中断した後18時25分04秒に再び鳴りだし」
#    （18:24:38＝37＋約1秒＝その終わり・38＋26＝18:25:04 と合う）・p91「18時24分12秒ごろから18時56分28秒ごろまで」・
#    p311（別添6）18:24:42「(CAP)スコーク77」・18:24:47「(COP)スコーク77」・解説 p19 表3「日没；12日18:40 日出；13日04:55」・
#    p23「墜落地点における日没は、18時40分ごろ」・p8「18時56分ごろ」（割れる＝付図-1「18:56'30」）・p26「8月13日04時39分日航機の残骸を発見し、
#    墜落現場を確認」・p28「8月13日10時45分ごろ…生存者が発見された」
REC_AXIS = {"18:24:35": {"報告書 p6"}, "18:24:37": {"報告書 p88"}, "18:24:38": {"報告書 p88"}, "18:25:04": {"報告書 p88"},
            "18:24:12": {"報告書 p91"}, "18:56:28": {"報告書 p91"}, "18:24:42": {"報告書 p311"}, "18:24:47": {"報告書 p311"},
            "18:40": {"解説 p1019", "報告書 p23"}, "18:56": {"報告書 p8"}, "翌4:39": {"報告書 p26"}, "翌4:55": {"解説 p1019"},
            "翌10:45": {"報告書 p28"}}
# 🆕 2026-10-10（20本目 ⑤b-6）：年表2つ（c815・c819＝1978年の修理の日付／c824〜c826＝修理のあとの7年）。別添1 本文 p246〜249 は文字の層が
#    無い＝`ref/ep20/src/ja_09_p15-18_ocr200.txt`（OCR）で読んだ：p247「修理作業は、昭和53年6月17日～7月11日の間に行われた」・
#    p248「この作業は6月26日に行われ、6月27日に修理チーム検査員の検査を受けた」・p249「飛行試験は、7月10日及び11日の両日」・
#    「7月11日付けで完了の確認」・「7月12日合格と判定された」／報告書 p18「昭和53年7月12日、同検査に合格した」・「昭和59年11月20日～
#    12月5日に実施されたC整備」・p104「昭和53年7月の修理と同時に行われたC整備（No.5C）」・p1「昭和60年8月12日」
#    🔴 間の C整備（No.6C〜No.10C）の日付は報告書に無い＝表に入れない（年表に点を打たせない）
REC_AXIS.update({"1978-06-17": {"報告書 p247"}, "1978-07-11": {"報告書 p247", "報告書 p249"}, "1978-06-26": {"報告書 p248"},
                 "1978-06-27": {"報告書 p248"}, "1978-07-10": {"報告書 p249"}, "1978-07-12": {"報告書 p249", "報告書 p18"},
                 "1978-07": {"報告書 p104"}, "1984-11-20": {"報告書 p18"}, "1984-12-05": {"報告書 p18"},
                 "1985-08-12": {"報告書 p1", "報告書 p18"}})
# 🆕 2026-10-10（20本目 ⑤b-6b）：ca16・ca17（同じ警報の帯）＝解説 p15「付録8-2 では…その理由を明らかにすることはできなかった」・
#    p16「ダイヤフラム等が…一時的に故障していた可能性も全くないとはいえません」「異常事態発生後、極めて早い時点で急激に客室高度が上昇した、
#    とするのが最も無理がない推論」（18:24:35＝異常事態の発生）。cc11〜cc14 の年表＝sources.md §8（産経新聞 2026-08-12＝ボーイングは2024年9月に
#    自社サイトに説明・2026年8月に削除と謝罪が分かる／国土交通大臣の会見 2026-08-25／2026-10-08 の検索で公表は見つからない）。
#    🔴 月だけの記録（2024年9月・2026年8月）は月の値で置く（日を推測で足さない）
REC_AXIS["18:24:35"] = REC_AXIS["18:24:35"] | {"解説 p1016"}
REC_AXIS["18:24:38"] = REC_AXIS["18:24:38"] | {"解説 p1015", "解説 p1016"}
REC_AXIS["18:25:04"] = REC_AXIS["18:25:04"] | {"解説 p1015", "解説 p1016"}
REC_AXIS.update({"2024-09": {"産経 p1"}, "2026-08": {"産経 p1"}, "2026-08-25": {"会見 p1"}, "2026-10": {"検索 p1"}})
LANES_OK = set()
REC_APPROX = {"18:24:12", "18:56:28", "18:56", "翌10:45"}      # 記録が about の時刻（「ごろ」が要る）
LANE_COL = 20        # 🆕 18本目 ⑤b-5：2段の帯の札が軸の左端より左へ出てよい画素（段の名の列にかけない）
REC_LANE = {}             # 2段の帯の記録ごとの段（値 → 段の名）
CH_PAD = 12          # 🆕 16本目 ⑤b-6b：札と右上の章の札（jiko_style.chapter）のあいだに要る画素
_REF = [None]        # 🆕 19本目 ⑤b-5：「約○分前」の基準（分）＝judge_fig が kw の ref を門番の読み方で読んで置く
# 🆕 19本目 ⑤b-5：並び（order）の値を「基準からの秒」に読む（門番の側の読み方＝型なので残す）
ORDER_UNIT = {"週間": 7 * 86400, "日": 86400, "時間": 3600, "分": 60}
# 🔴 2026-10-08（20本目 ⑤b-1・§0b）：並びの基準の時刻（分）は記録の値（19本目＝町の頁の崩落の時刻 1:22＝82・A12）＝見本 `tools/fixture_ep19.py`
#    （GATES["check_axis"]）へ移して空（None）にした。20本目で時計の時刻を含む並び（"1:16:27" の形）を使うときは、その回の基準の分を入れる。
#    空のあいだ、時計の時刻を含む並びは `_order_checks` が「基準が空」で止める（fail closed）。「約N週間前」「約N分前」だけの並びは基準を使わない
ORDER_REF_MIN = None
ORDER_NOTE = "間隔は時間に比例しない"     # 並びの note に要る断り


def gv(view, s):
    """門番の読み方（型とは別に書く）＝(下限, 上限)。date は年（小数）・clock は分・sec は秒（15本目〜）。"""
    s = str(s).strip()
    if view == "sec":
        # 🆕 15本目 ⑤b-5（c218）：負の秒＝0 の時点より前（"約-8"）
        m = re.fullmatch(r"(?:約)?(-)?(\d+)(?:\.(\d+))?", s)
        v = float(m[2] + ("." + m[3] if m[3] else "")) * (-1 if m[1] else 1)
        tol = 0.5 * 10 ** -len(m[3]) if m[3] else 0.05        # 書いた桁の半分（整数は ±0.05＝目盛りの 0秒）
        return v - tol, v + tol
    if view == "date":
        p = [int(x) for x in s.split("-")]
        if len(p) == 1:
            return float(p[0]), p[0] + 0.999
        if len(p) == 2:
            y, m = p
            a = datetime.date(y, m, 1)
            b = datetime.date(y + (m == 12), m % 12 + 1, 1)
        else:
            a = datetime.date(*p)
            b = a + datetime.timedelta(days=1)
        yl = (datetime.date(a.year + 1, 1, 1) - datetime.date(a.year, 1, 1)).days

        def yr(d):
            return d.year + (d - datetime.date(d.year, 1, 1)).days / yl
        if len(p) == 3:
            v = yr(a)
            return v - 0.6 / yl, v + 0.6 / yl
        return yr(a) - 1e-6, yr(b) + 1e-6
    # 🆕 19本目 ⑤b-5：基準からの「約○分前」（"約-7"・"約-9〜-8"）＝門番の側の基準 _REF（judge_fig が kw の ref を自分で読んで置く）
    r = re.fullmatch(r"約-(\d+)(?:〜-(\d+))?", s)
    if r:
        if _REF[0] is None:
            raise ValueError(f"「{s}」（約○分前）なのに基準 ref が無い")
        lo, hi = sorted([int(r[1]), int(r[2] or r[1])])
        return _REF[0] - hi - 0.3, _REF[0] - lo + 0.3
    nxt = s.startswith("翌")
    parts = s.replace("翌", "").split(":")
    if len(parts) == 3:
        # 🆕 19本目 ⑤b-5：秒まで（"1:16:27"）＝±0.5秒
        h, m, sec = (int(x) for x in parts)
        v = (1440 if nxt else 0) + h * 60 + m + sec / 60
        return v - 0.5 / 60, v + 0.5 / 60
    h, m = parts
    if "." in m:
        # 🆕 18本目 ⑤b-5：分の小数（"9:18.1"）＝書いた桁の半分の幅（±0.05分）。整数の分は今までどおり ±0.3分
        whole, frac = m.split(".")
        v = (1440 if nxt else 0) + int(h) * 60 + int(whole) + int(frac) / 10 ** len(frac)
        tol = 0.5 / 10 ** len(frac)
        return v - tol, v + tol
    v = (1440 if nxt else 0) + int(h) * 60 + int(m)
    return v - 0.3, v + 0.3


def _mid(view, s):
    a, b = gv(view, s)
    if view == "date" and len(str(s).split("-")) < 3:
        return a          # 年・月の目盛りはその頭に立つ
    return (a + b) / 2


def _texts(view, s):
    """値 s を画面に出してよい文字（門番の書き方）。date は日まで・年月まで・年だけのどれか（語りの細かさに合わせてよい）。"""
    if view == "date":
        p = [int(x) for x in s.split("-")]
        forms = [f"{p[0]}年"]
        if len(p) > 1:
            forms.append(f"{p[0]}年{p[1]}月")
        if len(p) > 2:
            forms.append(f"{p[0]}年{p[1]}月{p[2]}日")
            forms.append(f"{p[1]}月{p[2]}日")      # 🆕 20本目 ⑤b-6：月日だけ（axis の fmt="md"）
        return set(forms)
    if view == "sec":
        return {_sec_word(s)}
    if view == "order":
        return {s}            # 🆕 19本目：並びの値は書いたまま
    r = re.fullmatch(r"約-(\d+)(?:〜-(\d+))?", s)
    if r:                     # 🆕 19本目：「約7分前」・範囲は小さい方から「約8〜9分前」
        lo, hi = sorted([int(r[1]), int(r[2] or r[1])])
        return {f"約{lo}分前" if lo == hi else f"約{lo}〜{hi}分前"}
    t = s.replace("翌", "")
    if "." in t:
        # 🆕 18本目 ⑤b-5：分の小数は「9時18.1分」（「9:18.1」は9時18分1秒に読める）。分の頭の0は書かない（9:09.8→9時9.8分）
        h, m = t.split(":")
        return {f"{int(h)}時{m.lstrip('0') if not m.startswith('0.') else m}分"}
    return {t}


def _want_texts(view, s):
    """札に出してよい文字（「ごろ」込み）。🆕 18本目 ⑤b-5：REC_APPROX の時刻は「ごろ」が要る・ほかは付けない。"""
    base = _texts(view, s)
    return {b + "ごろ" for b in base} if s in REC_APPROX else base


def _sec_word(s):
    """門番の秒の書き方（型とは別に書く）：負は「N秒前」。"""
    if s.startswith(("-", "約-")):
        return s.replace("-", "", 1) + "秒前"
    return s + "秒"


def _tick_text(view, s):
    if view == "date":
        p = s.split("-")
        if len(p) == 3:       # 🆕 18本目 ⑤b-5：日まである目盛りは「12日」（前の型は「4月」と出した＝日の軸で読めない）
            return f"{int(p[2])}日"
        return f"{int(p[1])}月" if len(p) > 1 else p[0]
    if view == "sec":
        return _sec_word(s)
    return s.replace("翌", "")


def head_touch(labs, head):
    """🆕 2026-10-02（16本目 ⑤c'）：札（`lx`・`ly`＝型が描いた広がり）が左上の見出し（字・下線・副題＝`jiko_style.title`）に
    触れない（間 CH_PAD）。軸の3段目（ROW_UP 398）は字が3行だと y≈110 まで上がり、見出しの帯に入る作り＝見出しが長いと重なる。
    直す前の c518＝見出し「のばさなかった模型」の下線（x72〜670・y134）に「1962年4月」の札（x630〜985・y110〜248）が重なった
    （⑤c の 640px で疑い→幾何で確かめた）。layout は字の箱どうししか見ず、下線は見ていない。head＝(見出し t, 副題 s)"""
    import fontmetrics as fm
    import jiko_style as J
    t, s = head
    hb = []
    if t:
        hb.append(("見出しの字", J.MG - 5, J.MG + fm.width(t, 62, "Dela") + 5, 104 - 0.88 * 62 - 5, 104 + 0.12 * 62 + 5))
        hb.append(("見出しの下線", J.MG, J.MG + min(J.RIGHT - J.MG, 40 + len(t) * 62), 134 - 2.5, 134 + 2.5))
    if s:
        hb.append(("副題", J.MG - 3, J.MG + fm.width(s, 32, "Noto") + 3, 182 - 0.88 * 32 - 3, 182 + 0.12 * 32 + 3))
    bad = []
    for a in labs:
        if not a.get("ly"):
            continue
        for nm, x0, x1, y0, y1 in hb:
            if a["lx"][1] > x0 - CH_PAD and a["lx"][0] < x1 + CH_PAD and a["ly"][0] < y1 + CH_PAD and a["ly"][1] > y0 - CH_PAD:
                bad.append(f"{_nm(a)} の札（段{a.get('row', 0)}・x {a['lx'][0]:.0f}〜{a['lx'][1]:.0f}・上の端 y={a['ly'][0]:.0f}）が"
                           f"{nm}に触れる（間 {CH_PAD} 画素未満）＝見出しを短く／段を減らす")
    return bad


def _nm(p):
    """部品の呼び名（点＝値・帯＝始め〜終わり）。🆕 18本目 ⑤b-5：2段の帯の帯 span も札を持つ"""
    return p["at"] if "at" in p else f"{p.get('a')}〜{p.get('b')}"


def tier_pierce(parts):
    """🆕 18本目 ⑤b-5：2段の帯（tiers）の縦の線（点から札へ・型が描いた vl）が、**同じ段**のほかの札（lx・ly）を貫かない。
    段ごとに札の段 row が別に数えられる＝14本目の「段の番号で比べる」測り方は段をまたいで誤って鳴る → 幾何で測る"""
    bad, n = [], 0
    for b in parts:
        if not b.get("vl"):
            continue
        x, y0, y1 = b["vl"]
        for a in parts:
            if a is b or not (a.get("lx") and a.get("ly")) or a.get("lane") != b.get("lane"):
                continue
            n += 1
            if a["lx"][0] + 2 < x < a["lx"][1] - 2 and y0 < a["ly"][1] and y1 > a["ly"][0]:
                bad.append(f"{_nm(b)} の縦の線（段「{b.get('lane')}」）が {_nm(a)} の札を貫く")
    return bad, n


def judge_fig(kw, split_times=(), head=None):
    """(食い違いの list, 照合した件数)。head＝(見出し, 副題)＝渡せば札が見出しに触れないかも見る（head_touch）。"""
    import axis as A
    f = A.axis(**kw)
    m = f.mech
    view = m["view"]
    vk = view if view in ("date", "sec", "order") else "clock"
    bad, n = [], 0
    # 🆕 19本目 ⑤b-5：「約○分前」の基準＝kw の ref を門番の読み方で読み、記録の表で照らす
    _REF[0] = None
    if kw.get("ref"):
        n += 1
        a_, b_ = gv("clock", kw["ref"])
        _REF[0] = (a_ + b_) / 2
        if kw["ref"] not in REC_AXIS or kw.get("ref_rec") not in REC_AXIS[kw["ref"]]:
            bad.append(f"基準 {kw['ref']}（{kw.get('ref_rec')}）が記録の表 REC_AXIS と合わない")
    if view == "order":
        ob, on = _order_checks(m)
        bad += ob
        n += on
        return _judge_parts(kw, m, view, vk, bad, n, None, split_times, head)
    tk = m["ticks"]
    if len(tk) < 2:
        return [f"目盛りが {len(tk)} 本（2本以上ないと画素から値へ戻せない）"], 1
    for t in tk:
        n += 1
        if t["lab"] != _tick_text(vk, t["at"]):
            bad.append(f"目盛り {t['at']} の文字が「{t['lab']}」")
    # 一次式（最小二乗）
    xs = [t["x"] for t in tk]
    vs = [_mid(vk, t["at"]) for t in tk]
    k = len(xs)
    mx, mv = sum(xs) / k, sum(vs) / k
    sxx = sum((v - mv) ** 2 for v in vs)
    p = sum((v - mv) * (x - mx) for v, x in zip(vs, xs)) / sxx
    q = mx - p * mv
    for t in tk:
        if abs(p * _mid(vk, t["at"]) + q - t["x"]) > 1.0:
            bad.append(f"目盛り {t['at']} が一直線に並ばない（{t['x']}）")

    def back(x):
        return (x - q) / p

    return _judge_parts(kw, m, view, vk, bad, n, (back, p), split_times, head)


def _order_checks(m):
    """🆕 19本目 ⑤b-5：並び（order）の物差し＝①値が時間の順（門番の読み方で基準からの秒へ）②同じ間隔（点の x の差が等しく・
    端は半分の間隔）③途切れの印が点のあいだに1つずつ ④note に「間隔は時間に比例しない」。"""
    bad, n = [], 0
    st, sx = m["stops"], m["stop_x"]
    secs = []
    for s in st:
        n += 1
        r = re.fullmatch(r"約(\d+)(週間|日|時間|分)前", s)
        c = re.fullmatch(r"(\d{1,2}):(\d{2})(?::(\d{2}))?", s)
        if r:
            secs.append(-int(r[1]) * ORDER_UNIT[r[2]])
        elif c:
            if ORDER_REF_MIN is None:      # 🆕 20本目 ⑤b-1：基準の表が空のあいだは止める（None を引き算して落ちない）
                bad.append(f"並びの値「{s}」（時計の時刻）なのに基準の時刻 ORDER_REF_MIN が空（記録の表が空）")
                return bad, n
            secs.append((int(c[1]) * 60 + int(c[2]) - ORDER_REF_MIN) * 60 + int(c[3] or 0))
        else:
            bad.append(f"並びの値「{s}」が読めない（約N週間前／約N時間前／約N分前／1:16:27）")
            return bad, n
    n += 1
    if any(b <= a for a, b in zip(secs, secs[1:])):
        bad.append(f"並びが時間の順でない（{st}）")
    n += 1
    gaps = [b - a for a, b in zip(sx, sx[1:])]
    if len(sx) < 2 or max(gaps) - min(gaps) > 0.6 or abs((sx[0] - m["x0"]) - gaps[0] / 2) > 0.6 \
            or abs((m["x1"] - sx[-1]) - gaps[0] / 2) > 0.6:
        bad.append(f"並びの点が同じ間隔でない（{sx}）")
    n += 1
    br = m.get("breaks") or []
    if len(br) != len(st) - 1 or any(not (a < b < c) for a, b, c in zip(sx, br, sx[1:])):
        bad.append(f"途切れの印が点のあいだに1つずつでない（印 {len(br)}・点 {len(st)}）＝間隔が時間に比例しない印")
    n += 1
    if ORDER_NOTE not in (m.get("note") or ""):
        bad.append(f"並びの note に「{ORDER_NOTE}」が無い")
    return bad, n


def _judge_parts(kw, m, view, vk, bad, n, lin, split_times, head):
    """部品ごとの照合と、札の位置の照合（judge_fig の後半）。lin＝(画素→値, 傾き)・order は None（点は並びの位置で照らす）。"""
    placed = [m["x0"]]
    splits = []
    for part in m["parts"]:
        recs = part["rec"] if isinstance(part["rec"], (list, tuple)) else [part["rec"]]
        if part["k"] == "lane":           # 🆕 18本目 ⑤b-5：段の明かり（値を持たない）＝段の名だけ照らす
            n += 1
            if part.get("lane") not in LANES_OK:
                bad.append(f"段の明かりの名「{part.get('lane')}」が決まった名でない")
            continue
        vals = [(part["at"], part["x"])] if "at" in part else [(part["a"], part["xa"]), (part["b"], part["xb"])]
        for s, x in vals:
            n += 2
            if s not in REC_AXIS:
                bad.append(f"{s} は記録の表 REC_AXIS に無い（{part['k']}「{part.get('t', '')}」）")
            elif not any(r in REC_AXIS[s] for r in recs):
                bad.append(f"{s} の rec {recs} が記録の頁 {sorted(REC_AXIS[s])} と合わない")
            if lin is None:
                # 🆕 19本目：並び＝値は stops の1つ・x はその点の位置（同じ間隔は _order_checks が見る）
                if s not in m["stops"]:
                    bad.append(f"{s} は並びの値 stops に無い")
                elif abs(x - m["stop_x"][m["stops"].index(s)]) > 0.6:
                    bad.append(f"{s} の画素 x={x} が並びの位置 {m['stop_x'][m['stops'].index(s)]} と違う")
                placed.append(x)
                continue
            back, p = lin
            lo, hi = gv(vk, s)
            v = back(x)
            eps = 0.5 / abs(p)            # 画素は小数2桁に丸めて記録する＝0.5画素ぶんは丸めの誤差として許す
            if not lo - eps <= v <= hi + eps:
                bad.append(f"{s} の画素 x={x} は値 {v:.4f} に当たる（{lo:.4f}〜{hi:.4f} の外）")
            placed.append(x)
            # 🆕 18本目 ⑤b-5：2段の帯は、値を拾った記録の段に置く（REC_LANE＝門番の側の表。表に無い値は止める）
            if view == "tiers" and part["k"] != "br":
                n += 1
                if REC_LANE.get(s) != part.get("lane"):
                    bad.append(f"{s} を段「{part.get('lane')}」に置いた（記録の段は「{REC_LANE.get(s, '表に無い')}」）")
        if part.get("top"):
            n += 1
            if part["top"] not in _want_texts(vk, part["at"]):
                bad.append(f"{part['at']} の画面の文字が「{part['top']}」（値と合わない"
                           + ("・記録は about＝「ごろ」が要る" if part["at"] in REC_APPROX else "") + "）")
        if part["k"] == "split":
            splits.append(part)
            n += 1
            if not part.get("d"):
                bad.append(f"割れる時刻 {part['at']} に出典の名が無い")
        if part["k"] == "pt" and vk == "clock" and part["at"].replace("翌", "") in split_times:
            n += 1
            if not (part.get("by") and part.get("d")):
                bad.append(f"割れる時刻 {part['at']} の点に出典の名が無い（by=True にする＝ss.ILLU_SPLIT_TIMES）")
        if part["k"] == "link":
            n += 2
            if part.get("t") or part.get("chips"):
                bad.append(f"交信 {part['at']} に文字（私人の言葉を帯に書かない）")
            if not {part["fr"], part["to"]} <= LANES_OK:
                bad.append(f"交信 {part['at']} の段の名 {part['fr']}／{part['to']} が決まった名（{sorted(LANES_OK)}）でない")
    # 🆕 ⑤b-5：上の段へ伸びる縦の線が、それより下の段の札を貫かない（前のカットの点どうし＝同じ層でも）。
    #   門番 layout は層どうしの横切りしか見ない＝c408 の「1946年」の線が「1944年」の札を貫いたのを素通りした（試し焼きで見つけた）
    labs = [p for p in m["parts"] if p.get("lx") and ("at" in p or view == "tiers")]
    if view == "tiers":
        tb, tn = tier_pierce(m["parts"])
        bad += tb
        n += tn
    for b in ([] if view == "tiers" else m["parts"]):
        if "at" not in b or b["k"] in ("chips", "link"):
            continue
        for a in labs:
            if a is b:
                continue
            n += 1
            if b.get("row", 0) > a.get("row", 0) and a["lx"][0] + 2 < b["x"] < a["lx"][1] - 2:
                bad.append(f"{b['at']} の縦の線（段{b.get('row', 0)}）が {a['at']} の札（段{a.get('row', 0)}）を貫く")
    # 🆕 2026-10-01（16本目 ⑤b-6b）：上の段へ積んだ札が、右上の章の札（`jiko_style.chapter`＝x RIGHT−470〜RIGHT・y 56〜158）に
    #   触れない（間 CH_PAD 画素）。試し焼き 36880658544 の cb16＝3段目の「1963年10月9日」が「11 / 11・今も立つダム」の真下に接し、
    #   1つの塊に読めた（原寸の切り出しで見つけた）。門番 layout は層どうしの横切りしか見ない＝札が図の枠の上へ出ても鳴らなかった。
    #   札の縦の広がりは型が描いたとおりに記録する（`ly`＝lx と同じ作り）
    import jiko_style as J
    cbox = (J.RIGHT - 470 - CH_PAD, J.RIGHT + CH_PAD, 56 - CH_PAD, 158 + CH_PAD)
    for a in labs:
        if not a.get("ly"):
            continue
        n += 1
        if a["lx"][1] > cbox[0] and a["lx"][0] < cbox[1] and a["ly"][0] < cbox[3] and a["ly"][1] > cbox[2]:
            bad.append(f"{_nm(a)} の札（段{a.get('row', 0)}・上の端 y={a['ly'][0]:.0f}）が右上の章の札に触れる"
                       f"（間 {CH_PAD} 画素未満）＝段を減らす（軸の右に余白・札を年月まで）")
    if head:
        hb = head_touch(labs, head)
        n += len([a for a in labs if a.get("ly")])
        bad += hb
    if view in ("lanes", "tiers"):
        for nm in m["lanes"]:
            n += 1
            if nm not in LANES_OK:
                bad.append(f"段の名「{nm}」が決まった名でない")
    if view == "tiers":
        # 🆕 18本目 ⑤b-5：段は書いた順（上の段→下の段）に上から並ぶ（型の TIER_Y を逆にすると鳴る＝陽性対照）
        ys = [m["lanes"].get(nm) for nm in (kw.get("lanes") or ())]
        n += 1
        if len(ys) != 2 or None in ys or ys[0] >= ys[1]:
            bad.append(f"2段の帯の段が書いた順（上の段→下の段）に上から並んでいない（{ys}）")
        # 🆕 18本目 ⑤b-5（下見）：札が段の名の列（軸の左端より左）にかかると、段の名の真上に来て1つの言葉に読めた
        #   （c413「タンクを吹いた音でありうる」の上に「監視の記録」）＝札の左の端は軸の左端から LANE_COL 画素まで
        for a in labs:
            n += 1
            if a["lx"][0] < m["x0"] - LANE_COL:
                bad.append(f"{_nm(a)} の札（左の端 x={a['lx'][0]:.0f}）が段の名の列にかかる（軸の左端 {m['x0']:.0f}）"
                           "＝札を短く／右へ振る")
    if splits:
        n += 1
        if len(splits) < 2 or len({s["at"] for s in splits}) < 2:
            bad.append("割れる時刻の印が1つだけ（2つ以上を並べる）")
        if len({(s["c"], s["big"]) for s in splits}) > 1:
            bad.append("割れる時刻の印の形が揃っていない（どれが正しいと描かない）")
    if m["cur_on"]:
        for i, x in enumerate(m["cur"]):
            n += 1
            if not any(abs(x - y) < 0.6 for y in placed):
                bad.append(f"カーソル（段{i}）x={x} が記録の値に止まっていない")
    return bad, n


def _split_times():
    try:
        from cuts import ss
        return tuple(getattr(ss, "ILLU_SPLIT_TIMES", ()))
    except Exception:  # noqa: BLE001
        return ()


def selftest_ep15():
    """15本目（⑤b-2・⑤b-5）の秒の帯（sec）・年表・負の秒の検算＝**見本 `fixture_ep15`（15本目の表）を差し込んで**回す。
    🔴 2026-10-01（16本目 ⑤b-1）：本番の表（この門番の REC_AXIS）は16本目の空の器にした＝15本目の値は
       `fixture_ep15.GATES["check_axis"]`（14本目と同じ作り）。ss の側（AXIS_DOCS・AXI ほか）と GEO も15本目の見本になる
       ＝落ちても終わっても `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep15`"""
    import fixture_ep15
    fixture_ep15.apply(sys.modules[__name__])
    try:
        return _selftest_ep15()
    finally:
        fixture_ep15.restore()


def selftest_ep18():
    """🆕 2026-10-04（18本目 ⑤b-5）：2段の帯（tiers）・分の小数・「ごろ」・日の目盛りの検算＝**見本 `fixture_ep18`（18本目の表）を差し込んで**回す。
    ✅ 2026-10-06（19本目 ⑤b-1・§0b）：本番の表（この門番の REC_AXIS・LANES_OK・REC_APPROX・REC_LANE）は19本目の空の器にした＝18本目の値は
       `fixture_ep18.GATES["check_axis"]`（15・16本目と同じ作り）。ss の側（AXI・TV／TM ほか）と GEO も18本目の見本になる＝落ちても終わっても
       `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep18`。
       （18本目の「ごろ」と段の表を前の回の見本の検算のあいだだけ空にする `_quiet18`・`_loud18` は、本番の表が空になったので要らなくなった＝外した）"""
    import fixture_ep18
    fixture_ep18.apply(sys.modules[__name__])
    try:
        return _selftest_ep18()
    finally:
        fixture_ep18.restore()


def _selftest_ep18():
    """18本目の検算の本体（`fixture_ep18` を差し込んだ中で呼ぶ）。
    陽性対照＝筋（段・ごろ・表に無い値・貫き）と、型の定数を壊す形（分の小数を落とす・札の書き方・日の目盛り・段の上下）"""
    import axis as A
    import fixture_ep18
    import jiko_style as J  # noqa: F401
    V, M = fixture_ep18._V, fixture_ep18._M
    five = dict(view="tiers", span=("9:08", "9:20"), ticks=("9:08", "9:10", "9:12", "9:14", "9:16", "9:18", "9:20"), lanes=(V, M),
                past=[dict(k="span", lane=M, a="9:09.8", b="9:11.3", t="吹いた音？", rec="R08 p4185"),
                      dict(k="pt", lane=V, at="9:13", t="声", rec="R08 p4185"),
                      dict(k="pt", lane=V, at="9:16", t="崩れた声", rec="R08 p4185", approx=True)],
                steps=[dict(add=dict(k="pt", lane=M, at="9:18.1", t="音", rec="R08 p4185", big=True, c="ALERT"), cur="9:18.1")],
                note="n", src="s")
    day = dict(view="date", span=("1963-04-09", "1963-04-14"),
               ticks=("1963-04-10", "1963-04-11", "1963-04-12", "1963-04-13"),
               steps=[dict(add=dict(k="pt", at="1963-04-12", t="記録を見る", rec="R08 p4187"), cur="1963-04-12")], note="n", src="s")

    def swap(kw, i, **ch):
        p = list(kw["past"])
        p[i] = dict(p[i], **ch)
        return dict(kw, past=p)
    cases = [("18本目 正しい2段の帯（9:09.8〜9:11.3・9:13・9:16ごろ・9時18.1分）", five, True),
             ("18本目 正しい日の年表（12日）", day, True),
             ("🔴 18本目 陽性対照：9:13 の声を監視の記録の段に置く", swap(five, 1, lane=M), False),
             ("🔴 18本目 陽性対照：9:16（about）の札に「ごろ」が無い", swap(five, 2, approx=False), False),
             ("🔴 18本目 陽性対照：9:13（at）の札に「ごろ」を付ける", swap(five, 1, approx=True), False),
             ("🔴 18本目 陽性対照：段の記録に無い値（9:09 試験深度）を2段の帯に置く",
              dict(five, steps=[dict(add=dict(k="pt", lane=V, at="9:09", t="試験深度", rec="R08 p4212"))]), False),
             ("🔴 18本目 陽性対照：下の段の帯の札が段の名の列にかかる（下見の c413＝左へ振った長い札）",
              swap(five, 0, t="タンクを吹いた音でありうる", anchor="end"), False),
             ("🔴 18本目 陽性対照：点の縦の線が同じ段の帯の札を貫く（9:11 の札を長くして2段目へ）",
              dict(five, past=[dict(five["past"][0], t="タンクを吹いた音でありうる"),
                               dict(k="pt", lane=M, at="9:11", t="主冷却材ポンプが速い回し方をやめる", rec="R08 p4185")]), False)]
    ok = True
    for name, kw, want in cases:
        try:
            bad, _ = judge_fig(kw, ())
        except ValueError as e:
            bad = [f"型が止まった：{e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 型の定数・関数を壊す（§5b-88）
    keep_val, keep_lab, keep_tick, keep_y = A.val, A.label, A._tick_lab, A.TIER_Y
    breaks = (
        ("分の小数を落として描く型（9:18.1 を 9:18 に）", "val",
         lambda view, s: ((float(int(keep_val(view, s)[0])), keep_val(view, s)[1]) if view in ("clock", "tiers") else keep_val(view, s)),
         five),
        ("分の小数の札を「9:18.1」と書く型", "label", lambda view, s, fmt="": str(s).replace("翌", "") if view in ("clock", "tiers")
         else keep_lab(view, s, fmt), five),
        ("日の目盛りを「4月」と書く型（前の型）", "_tick_lab",
         lambda view, s: ((f"{int(s.split('-')[1])}月", s.split("-")[0] + "年") if view == "date" and s.count("-") == 2 else keep_tick(view, s)),
         day),
        ("上の段と下の段を逆に描く型（TIER_Y を逆に）", "TIER_Y", tuple(reversed(keep_y)), five))
    for name, attr, val, kw in breaks:
        setattr(A, attr, val)
        try:
            bad, _ = judge_fig(kw, ())
        except ValueError as e:
            bad = [f"型が止まった：{e}"]
        finally:
            A.val, A.label, A._tick_lab, A.TIER_Y = keep_val, keep_lab, keep_tick, keep_y
        ok &= bool(bad)
        print(f"  {'OK' if bad else '🔴 NG'} 🔴 18本目 陽性対照（型）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    return ok


def _selftest_ep15():
    """15本目の検算の本体（`fixture_ep15` を差し込んだ中で呼ぶ）。"""
    import axis as A
    sec = dict(view="sec", span=("0", "5"), ticks=("0", "1", "2", "3", "4", "5"),
               steps=[dict(add=[dict(k="pt", at="1.3", t="最大G", rec="AAB p28"),
                                dict(k="pt", at="4.6", t="一片が離れる", rec="AAB p28")], cur="4.6"),
                      dict(add=dict(k="pt", at="0.56", t="リンクが折れている", rec="AAB p24"), cur="0.56")],
               note="n", src="s")
    cases = [("15本目 正しい秒の帯（1.3→4.6→0.56）", sec, True),
             ("🔴 15本目 陽性対照：表に無い秒（#42 の 5.3）",
              dict(sec, span=("0", "6"), ticks=("0", "2", "4", "6"),
                   steps=[dict(add=dict(k="pt", at="5.3", t="一片", rec="AAB p28"))]), False),
             ("🔴 15本目 陽性対照：1.3秒の頁が違う（AAB p29）",
              dict(sec, steps=[dict(add=dict(k="pt", at="1.3", t="最大G", rec="AAB p29"))]), False)]
    # 🆕 ⑤b-5（c218）：負の秒（横転の約8秒前）＝札「約8秒前」・目盛り「10秒前」
    upset = dict(view="sec", span=("-10", "1"), ticks=("-10", "-8", "-6", "-4", "-2", "0"),
                 steps=[dict(add=dict(k="pt", at="0", t="横転の始まり", rec="AAB p28"), cur="0"),
                        dict(add=dict(k="pt", at="約-8", t="圧力と回転が下がる", rec="AAB p29"), cur="約-8")],
                 note="n", src="s")
    cases += [("15本目 正しい負の秒（約8秒前）", upset, True),
              ("🔴 15本目 陽性対照：約8秒前の頁が違う（AAB p28）",
               dict(upset, steps=[dict(add=dict(k="pt", at="約-8", t="圧力", rec="AAB p28"))]), False),
              ("🔴 15本目 陽性対照：記録に無い負の秒（約-7）",
               dict(upset, steps=[dict(add=dict(k="pt", at="約-7", t="圧力", rec="AAB p29"))]), False)]
    # 🆕 ⑤b-5：縦の線が別の札を貫く（試し焼きの c408＝前のカットの 1944年と1946年の点が31画素しか離れていない）
    hist = dict(view="date", span=("1942", "2013"), ticks=("1950", "1960", "1970", "1980", "1990", "2000", "2010"),
                steps=[dict(add=dict(k="pt", at="1983-07", t="パイロットが取得", rec="AAB p12", anchor="end"), cur="1983-07")],
                note="n", src="s")
    p44 = dict(k="pt", at="1944-12-23", t="軍へ引き渡し", rec="AAB p12", fmt="y")
    p46 = dict(k="pt", at="1946-07", t="売却", rec="AAB p12", fmt="y")
    cases += [("🔴 15本目 陽性対照：1946年の縦の線が1944年の札を貫く（直す前の c408）", dict(hist, past=[p44, p46]), False),
              ("15本目 正しい：1946年の札を消して沈める（直した c408）", dict(hist, past=[p44, dict(p46, lab=False, t="")]), True)]
    # 🆕 16本目 ⑤b-6b：上の段へ積んだ札が右上の章の札に触れる（直す前の cb16＝軸の右の端に近い3点の札が3段に積まれた）。
    #   日付は15本目の見本の表にある値（CAROL p5008）＝3段目の札だけが章の札の箱に入り、縦の線の貫きは起きない並べ方
    late = dict(view="date", span=("2016-01", "2021-12"), ticks=("2016", "2018", "2020"), note="n", src="s",
                steps=[dict(add=[dict(k="pt", at=d, t="事故", rec="CAROL p5008", anchor="end")
                                 for d in ("2020-07-22", "2020-11-03", "2021-07-13")])])
    cases += [("🔴 16本目 陽性対照：3段目の札が右上の章の札に触れる（直す前の cb16）", late, False),
              ("16本目 正しい：同じ右の端でも2段に収める", dict(late, steps=[dict(add=[
                  dict(k="pt", at=d, t="事故", rec="CAROL p5008", anchor="end") for d in ("2020-07-22", "2020-11-03")])]), True)]
    ok = True
    # 🆕 16本目 ⑤c'：札が見出しに触れる（直す前の c518 の札の広がりと見出し）／見出しを7字にすれば黙る（直した c518）。
    #   札の座標は型が描いた値（⑤c' で axis.axis を呼んで取った）＝回の表に左右されない
    lab518 = [dict(at="1962-04-30", row=2, lx=(630.0, 985.0), ly=(110.5, 248.0)),
              dict(at="1961", row=1, lx=(453.0, 709.0), ly=(300.5, 402.0))]
    for name, hd, want in (("🔴 16本目 陽性対照：3段目の札が見出しの下線に触れる（直す前の c518）", ("のばさなかった模型", "模型の歩み"), False),
                           ("16本目 正しい：見出しを7字に（直した c518）", ("模型はのばさず", "模型の歩み"), True)):
        got = not head_touch(lab518, hd)
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}")
    for name, kw, want in cases:
        bad, _ = judge_fig(kw, ())
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 型を壊す陽性対照（負の秒）：① 約付きの負の秒だけ半分の所に描く（画素）② 札の「前」を落とす（文字）
    keep_val, keep_txt = A.val, A._sec_text
    A.val = lambda view, s: ((keep_val(view, s)[0] / 2 if view == "sec" and str(s).startswith("約-") else keep_val(view, s)[0]),
                             keep_val(view, s)[1])
    try:
        bad, _ = judge_fig(upset, ())
    except ValueError as e:
        bad = [f"型が止まった：{e}"]
    finally:
        A.val = keep_val
    ok &= bool(bad)
    print(f"  {'OK' if bad else '🔴 NG'} 🔴 15本目 陽性対照（画素）：約8秒前を半分の所に描く型: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    A._sec_text = lambda s: s.replace("-", "") + "秒"
    try:
        bad, _ = judge_fig(upset, ())
    finally:
        A._sec_text = keep_txt
    ok &= bool(bad)
    print(f"  {'OK' if bad else '🔴 NG'} 🔴 15本目 陽性対照（文字）：「前」を落とす型（約8秒）: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    keep = A.val
    # 小数の秒だけ 0.3秒ずらして描く型（目盛り＝整数は正しい＝一様な伸び縮みは目盛りの物差しに吸われるので、部品だけずらす）
    A.val = lambda view, s: ((keep(view, s)[0] + (0.3 if "." in str(s) else 0.0), keep(view, s)[1]) if view == "sec"
                             else keep(view, s))
    try:
        bad, _ = judge_fig(sec, ())
    except ValueError as e:
        bad = [f"型が止まった：{e}"]
    finally:
        A.val = keep
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 15本目 陽性対照（画素）：小数の秒を 0.3秒ずらして描く型: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    return ok


def selftest_ep19():
    """🆕 2026-10-06（19本目 ⑤b-5）：秒まである時刻・基準からの「約○分前」・並び（order）の検算＝**見本 `fixture_ep19`（19本目の表）を差し込んで**回す。
    ✅ 2026-10-08（20本目 ⑤b-1・§0b）：本番の表（この門番の REC_AXIS・ORDER_REF_MIN）は20本目の空の器にした＝19本目の値は
       `fixture_ep19.GATES["check_axis"]`（15・16・18本目と同じ作り）。ss の側（REC_DOCS・AXI ほか）と GEO も19本目の見本になる＝落ちても終わっても
       `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep19`。"""
    import fixture_ep19
    fixture_ep19.apply(sys.modules[__name__])
    try:
        return _selftest_ep19()
    finally:
        fixture_ep19.restore()


def _selftest_ep19():
    """19本目の検算の本体（`fixture_ep19` を差し込んだ中で呼ぶ）。
    正しい形が通り、記録・順・断り・型の幾何（約○分前の向き・秒・間隔・途切れの印・札の文字）を壊すと鳴ること。"""
    import axis as A
    ok = True
    night = dict(view="clock", span=("1:11", "1:23"), ticks=("1:12", "1:14", "1:16", "1:18", "1:20", "1:22"),
                 ref="1:22", ref_rec="A12 p5101",
                 steps=[dict(add=dict(k="pt", at="約-7", t="信号", rec="TR p1169"), cur="約-7"),
                        dict(add=dict(k="pt", at="1:16:27", t="電話", rec="TR p1177", anchor="start"), cur="1:16:27")],
                 note="n", src="s")
    signs = ("約3週間前", "約1週間前", "約17時間前", "約9時間前", "約3時間前")
    order = dict(view="order", stops=signs, end="崩れる", note="間隔は時間に比例しない", src="s",
                 steps=[dict(add=[dict(k="pt", at=s, t="合図", rec=r) for s, r in
                                  zip(signs, ("TR p1156", "TR p1157", "TR p1158", "TR p1159", "TR p1160"))], cur="約3時間前")])

    def mod(d, **kw):
        return dict(d, **kw)
    cases = [
        ("正しい時刻の帯（約7分前・1:16:27・基準 1:22）", night, True),
        ("正しい並び（約3週間前〜約3時間前）", order, True),
        ("🔴 陽性対照：基準の頁が違う（TR p1001）", mod(night, ref_rec="TR p1001"), False),
        ("🔴 陽性対照：約7分前の頁が違う（TR p1170）",
         mod(night, steps=[dict(add=dict(k="pt", at="約-7", t="信号", rec="TR p1170"))]), False),
        ("🔴 陽性対照：並びの順が逆（約17時間前を約1週間前の前に）",
         mod(order, stops=("約3週間前", "約17時間前", "約1週間前", "約9時間前", "約3時間前")), False),
        ("🔴 陽性対照：並びの断り「間隔は時間に比例しない」が無い", mod(order, note="NIST のスライドの並べ方"), False),
    ]
    for name, kw, want in cases:
        bad, _ = judge_fig(kw)
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 型を壊す（§5b-88）：門番は値の読み方と並びの物差しを自分で持つ＝型だけが間違えても鳴ること
    keep_x, keep_base, keep_label = A._Ax.x, A._base, A.label

    def x_rel_shift(self, s, item=False):          # 「約○分前」を半分ずらして描く型
        return keep_x(self, s, item) + (66 if A.REL.fullmatch(str(s)) and self.view == "clock" else 0)

    def x_drop_sec(self, s, item=False):           # 秒を捨てて描く型（1:16:27 → 1:16）
        return keep_x(self, s.rsplit(":", 1)[0] if self.view == "clock" and str(s).count(":") == 2 else s, item)

    def x_uneven(self, s, item=False):             # 並びの1点だけ間隔をずらす型
        v = keep_x(self, s, item)
        return v + 40 if self.view == "order" and s == self.stops[1] else v

    def base_no_break(Ax, *a):                     # 途切れの印を1つ描き忘れる型
        r = keep_base(Ax, *a)
        Ax.breaks = Ax.breaks[:-1]
        return r
    breaks = (("「約○分前」を半分ずらす型", "x", x_rel_shift, night), ("秒を捨てる型", "x", x_drop_sec, night),
              ("並びの間隔をずらす型", "x", x_uneven, order), ("途切れの印を1つ描き忘れる型", "base", base_no_break, order),
              ("「約7分前」を「約7分」と書く型", "label", lambda v, s, fmt="": keep_label(v, s, fmt).replace("分前", "分"), night))
    for name, what, fn, kw in breaks:
        if what == "x":
            A._Ax.x = fn
        elif what == "base":
            A._base = fn
        else:
            A.label = fn
        try:
            bad, _ = judge_fig(kw)
        except ValueError as e:
            bad = [f"型が止まった：{e}"]
        finally:
            A._Ax.x, A._base, A.label = keep_x, keep_base, keep_label
        good = bool(bad)
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照（型）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    for name, kw in (("基準 ref の無い「約○分前」", mod(night, ref=None, ref_rec=None)),
                     ("並びに帯 span を置く", mod(order, steps=[dict(add=dict(k="span", a="約3週間前", b="約1週間前", rec="TR p1156"))]))):
        try:
            A.axis(**kw)
            good = False
        except ValueError:
            good = True
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照：{name}で型が止まる: {'止まった' if good else '通った'}（止まるはず）")
    return ok


def selftest():
    # 🆕 2026-10-06（19本目 ⑤b-5）：先に19本目を検算する＝前の回の見本を差す前に
    #    （2026-10-08〜：19本目も見本 fixture_ep19 の表＝selftest_ep19 が差し込んで・終わったら戻す）
    ok = selftest_ep19()
    # 🆕 2026-10-04（18本目 ⑤b-5）：先に18本目を検算する＝前の回の見本を差す前に
    #    （2026-10-06〜：18本目も見本 fixture_ep18 の表＝selftest_ep18 が差し込んで・終わったら戻す）
    ok &= selftest_ep18()
    # 🔴 2026-09-30（15本目 ⑤b-2）：先に15本目の秒の帯を検算してから、14本目の見本に差し替える
    #    （2026-10-01〜：15本目も見本 fixture_ep15 の表＝selftest_ep15 が差し込んで・終わったら戻す）
    ok &= selftest_ep15()
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（本番の表は回ごとに空にする＝§0b）＝この処理の中だけ14本目にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    import axis as A
    ST =("8:52", "8:58", "9:46", "9:48")
    night = dict(view="clock", span=("18:00", "翌10:00"), ticks=("18:00", "22:00", "翌2:00", "翌6:00", "翌10:00"),
                 steps=[dict(add=[dict(k="pt", at="18:30", t="出港", rec="海審 p1026"),
                                  dict(k="pt", at="翌9:10", t="着く", rec="海審 p1026")], cur="18:30"),
                        dict(add=dict(k="span", a="18:30", b="21:05", t="遅れ", rec=["海審 p1026", "海審 p1038"]),
                             cur="21:05")], note="n", src="s")
    years = dict(view="date", span=("2012-09", "2013-04"),
                 ticks=("2012-09", "2012-10", "2012-11", "2012-12", "2013-01", "2013-02", "2013-03", "2013-04"),
                 steps=[dict(add=[dict(k="pt", at="2012-10-08", t="導入", rec="海審 p1016"),
                                  dict(k="span", a="2012-10-12", b="2013-02-12", t="改造", rec="海審 p1016")],
                             cur="2013-02-12")], note="n", src="s")
    split = dict(view="clock", span=("9:40", "9:55"), ticks=("9:40", "9:45", "9:50", "9:55"),
                 steps=[dict(add=[dict(k="split", at="9:46", rec="判決 p18"), dict(k="split", at="9:48", rec="海審 p1055")])],
                 note="n", src="s")
    lanes = dict(view="lanes", span=("9:05", "9:40"), ticks=("9:10", "9:20", "9:30", "9:40"), lanes=("管制", "近くの船", "セウォル号"),
                 steps=[dict(add=dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="判決 p13"), cur="9:13")],
                 note="n", src="s")

    def mod(d, **kw):
        return dict(d, **kw)
    cases = [
        ("正しい夜の帯（18:30→翌9:10・21:05）", night, True),
        ("正しい改造の年表（2012-10-08・2012-10-12〜2013-02-12）", years, True),
        ("正しい割れる時刻（9:46 判決／9:48 海審）", split, True),
        ("正しい交信の帯（9:13 近くの船→セウォル号）", lanes, True),
        ("🔴 陽性対照：9:13 の頁が違う（海審 p1059）",
         mod(lanes, steps=[dict(add=dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="海審 p1059"))]), False),
        ("🔴 陽性対照：記録に無い時刻 9:15",
         mod(lanes, steps=[dict(add=dict(k="link", at="9:15", fr="近くの船", to="セウォル号", rec="判決 p13"))]), False),
        ("🔴 陽性対照：割れる時刻の印が1つだけ", mod(split, steps=[dict(add=dict(k="split", at="9:46", rec="判決 p18"))]), False),
        ("🔴 陽性対照：割れる時刻の片方だけ大きい",
         mod(split, steps=[dict(add=[dict(k="split", at="9:46", rec="判決 p18", big=True),
                                     dict(k="split", at="9:48", rec="海審 p1055")])]), False),
        ("🔴 陽性対照：割れる時刻 8:58 の点に出典の名が無い",
         dict(view="clock", span=("8:48", "9:02"), ticks=("8:50", "9:00"),
              steps=[dict(add=dict(k="pt", at="8:58", t="指示", rec="判決 p12"))], note="n", src="s"), False),
        ("🔴 陽性対照：段の名に私人の名",
         mod(lanes, lanes=("管制", "生徒", "セウォル号"),
             steps=[dict(add=dict(k="link", at="9:13", fr="管制", to="セウォル号", rec="判決 p13"))]), False),
        ("🔴 陽性対照：カーソルが記録の無い所（9:20）に止まる",
         mod(lanes, steps=[dict(add=dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="判決 p13"), cur="9:20")]),
         False),
    ]
    for name, kw, want in cases:
        bad, _ = judge_fig(kw, ST)
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 型の定数を壊す（§5b-88）：月の数え始め・翌日の足し分・軸の右端（部品だけずれる型は無いので目盛りの文字で捕まえる）
    for name, attr, val, kw in (("月を1つずらして描く型（MONTH0=0）", "MONTH0", 0, years),
                                ("翌日を12時間で描く型（NEXT_DAY=720）", "NEXT_DAY", 720, night)):
        keep = getattr(A, attr)
        setattr(A, attr, val)
        try:
            bad, _ = judge_fig(kw, ST)
        except ValueError as e:     # 範囲の外で型が止まるのも「捕まえた」
            bad = [f"型が止まった：{e}"]
        finally:
            setattr(A, attr, keep)
        good = bool(bad)
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照（画素）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    keep = A.label
    A.label = lambda view, s, fmt="": keep(view, s, fmt).replace("30", "03")   # 「18:30」を「18:03」と書く型
    try:
        bad, _ = judge_fig(night, ST)
    finally:
        A.label = keep
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照（文字）：18:30 を「18:03」と書く型: {'不合格' if bad else '合格'}（不合格のはず）"
          + (f"  ← {bad[0]}" if bad else ""))
    try:
        A.axis(**mod(lanes, steps=[dict(add=dict(k="link", at="9:13", fr="近くの船", to="セウォル号", rec="判決 p13",
                                                  t="脱出すれば"))]))
        good = False
    except ValueError:
        good = True
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照：交信に言葉を書くと型が止まる: {'止まった' if good else '通った'}（止まるはず）")
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import fixture_ep14
    fixture_ep14.restore()       # 🔴 15本目 ⑤b-2：selftest で差し込んだ14本目の見本を本番の表に戻す（戻さないと14本目の表で本番を測る）
    import cuts
    targets = {c: s["fig"] for c, s in sorted(cuts.SPEC.items()) if s.get("fig") and s["fig"][0] == "axis"}
    heads = {c: (cuts.SPEC[c].get("t", ""), cuts.SPEC[c].get("s", "")) for c in targets}     # 🆕 16本目 ⑤c'（head_touch）
    if not targets:
        print("⚠️ axis のカットが0件（この回に年表・時間の帯が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
        return 0
    st = _split_times()
    bad_all, n_all = 0, 0
    for cid, (_, kw) in targets.items():
        bad, n = judge_fig(kw, st, head=heads[cid])
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {cid}（axis）: {b}")
        else:
            print(f"✓ {cid}（axis・{kw['view']}）: 値・画素・割れる時刻 {n}件が合う")
    print(f"\n{'✓' if not bad_all else '🔴'} 軸の型 {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
