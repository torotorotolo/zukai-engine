# -*- coding: utf-8 -*-
"""check_boxes.py — 箱の型（流れ図・書類の再現図・並べ図＝`tools/boxes.py`）の**言葉・つながり・形**を記録と照らす
（2026-09-29 新設・14本目 ⑤b-6）。

■ なぜ要るか
  流れ図は「誰が・どの罪で・どうなったか」を箱のつながりで言う＝**つなぎ違い1本で事実が変わる**（1等航海士に7年の箱を
  つなぐ・無罪の箱を2審でなく1審に置く）。第11章は名前を出さない・人の形を使わない・赤を使わない（責める形にしない）。
  🔴 §5b-88・§5b-93：記録の値（役職・罪名・結果・刑・席の数・欄の名・原因の項目）は**この門番の側に持つ**（`REC_*`）。
  🔴 焼く直前の SVG を読む（画面の文字は `<text>` を全部・席は `data-q="seat"` の四角を数える）。

■ 測るもの
  流れ図 ① 画面の文字が全部、記録の表の言葉（`allowed()`）＝名前・記録に無い言葉が紛れ込まない
         ② 役職→罪名→結果（列＝裁判所）のつながり＝`REC_VERDICT`・役職→刑（点線・大法院の列）＝`REC_SENT`
         ③ 席の数＝裁判官の数（`REC_SEATS`）・灯した席は 0 か全部（全員一致）④ 甲板部・機関部の役職の数と並び＝`REC_CREW`
         ⑤ 赤（ALERT）を使わない・円（人の頭に読める形）を使わない ⑥ 部品の rec の頁
         ⑨ 🆕（15本目 ⑤c'）矢印の線分が箱の内側を通らない（c918＝問い→答えの横線が字の真ん中を通り打ち消し線に見えた）
  書類   ⑦ 表題・欄の名・行き来の箱＝`REC_FORM`（報告書の文にあるものだけ）・欄に値を書かない（記録が「未記入」）・「再現」の札
         ⑩ 🆕（18本目 ⑤b-6a）紙を2〜3枚並べる書類は紙ごとに ⑦ を照らし、紙どうしの間（24画素以上）と本体の左右（72〜1848）を測る
  並べ図 ⑧ 項目＝`REC_CAUSE`・2つ以上・全部同じ大きさと色（どれかを目立たせない）・項目のほかに絵を置かない（場面にしない）

■ 使い方
    python tools/check_boxes.py              # 全カット
    python tools/check_boxes.py --selftest   # 物差しの検算（陽性対照＝名前・つなぎ違い・席の数・赤・欄・形を壊す）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

from check_qty import ATTR, EL, _els, _recs, _unesc  # noqa: E402

# ══════════════════════════════════════════════════════════
#  🔴 §0b（題材を替えるとき空にする場所）：記録の言葉・値と頁（この回）
#     🔴 2026-09-30（15本目 リノ ⑤b-1）：**空にした**。14本目（セウォル号）の表は selftest の見本 `tools/fixture_ep14.py`
#        （GATES["check_boxes"]・値は1つも変えていない）。15本目の書類の再現図（記録簿・参加書類・検査の用紙）を書くチャットで、
#        欄の名と頁を ref/ep15/src/ep15_pages.txt で当てて入れる（空のあいだ、箱のカットは「記録に無い言葉」で止まる）
#     🔴 2026-10-01（16本目 バイオントダム災害 ⑤b-1）：15本目の表（REC_OTHER_ROLE・REC_MECH・REC_CHIP・REC_FORM＝報告書の鎖・
#        実況の担当・3つの問いの答え・書類の再現図）も**空にした**。selftest の見本 `tools/fixture_ep15.py`
#        （GATES["check_boxes"]・値は1つも変えていない＝git の `c646174`）。16本目の箱を書くチャットで、言葉と頁を
#        ref/ep16/src/ep16_pages.txt で当てて入れる（空のあいだ、箱のカットは「記録に無い言葉」で止まる）
#     🔴 2026-10-04（18本目 スレッシャー号 ⑤b-1）：16本目の表（REC_OTHER_ROLE・REC_MECH・REC_CHIP・REC_FORM・REC_CAUSE＝流れ図・
#        書類の再現図〈欄の値は原文のイタリア語〉・並べ図）も**空にした**。selftest の見本 `tools/fixture_ep16.py`
#        （GATES["check_boxes"]・値は1つも変えていない＝git の `b044b56`）。18本目の箱を書くチャットで、言葉と頁を
#        ref/ep18/src/ep18_pages.txt で当てて入れる（空のあいだ、箱のカットは「記録に無い言葉」で止まる）
# ══════════════════════════════════════════════════════════
#     🆕 2026-10-04（18本目 ⑤b-6a）：第1〜6章の箱（流れ図6・書類の再現図19・並べ図1）の言葉と頁を入れた（原文
#        ref/ep18/src/ep18_pages.txt で当てた・文字の層が崩れた5か所は頁の画像を切り出して読んだ）。🔴 19本目の ⑤b-1 でこの表を空にし、
#        値は見本 `tools/fixture_ep18.py` へ（selftest_ep18 も見本を差す形に＝check_axis の selftest_ep18 と同じ）
REC_CREW = {}
REC_ROLE_PAGES = set()
REC_OTHER_ROLE = {    # 流れ図の「role」の箱＝役職でない言葉（報告書の文の言葉）→ 頁の集合
    # c107「3枚の紙」：前の艦長の評価書＝証拠111（X p.531）・認定91（R08 p.195）／検査の数字＝認定102（p.197「145 old joints … rejection
    #   rate of 13.8 per cent」）／検査の書類＝認定104〜106（p.197＝品質保証の部署の報告・12月4日の決定・その写し）／どこまで届いたか＝
    #   認定108（p.197「neither the results … nor the decision … was made known to the Bureau of Ships」）・J p.18（報告書は4月11日より後）
    "前の艦長の評価書": {"X p1531", "R08 p4195"}, "検査の数字": {"R08 p4197"}, "検査の書類": {"R08 p4197"},
    "どこまで届いたか": {"R08 p4197", "J p8018"},
    # c110：査問会の記録（R08 p.181〜＝認定）・議会の公聴会の記録（J p.1「Joint Committee on Atomic Energy」1963年6月26日）
    "査問会の記録": {"R08 p4181"}, "議会の公聴会の記録": {"J p8001"},
    # c218：R08 p.107「we had to have him as Prospective Commanding Officer of the JOHN C. CALHOUN SSB(N) 630」・p.109「I felt that Harvey
    #   was one of the best qualified people we could find.」
    "前の艦長": {"R08 p4107"}, "艦長の予定者（ポラリス）": {"R08 p4107"}, "新しい艦長": {"R08 p4109"},
    # c421：認定16・17（水中電話の声）・認定18（監視の記録の音）＝R08 p.185／意見45（p.212「assumptions and computer solutions」
    #   「a reasonable rationalization of probable events」・p.214「the most probable approximation of the sequence of events」）
    "水中電話の声": {"R08 p4185"}, "監視の記録": {"R08 p4185"}, "仮定と計算": {"R08 p4212"},
    "最もありうる筋書き": {"R08 p4212", "R08 p4214"},
    # c616：認定105（p.197「known to the management personnel of the Shipyard, including the Production Officer and the Commander」）・
    #   認定106（「a copy of this decision was furnished the Commanding Officer of THRESHER」）
    "造船所の生産の責任者": {"R08 p4197"}, "造船所の司令官": {"R08 p4197"}, "スレッシャーの艦長（当時）": {"R08 p4197"},
    # c618：認定102・105・108（p.197）・J p.14「no decision or no recommendation was sent to the Bureau of Ships」
    "検査の結果の数字": {"R08 p4197"}, "外さないという決定": {"R08 p4197"}, "艦船局": {"R08 p4197", "J p8014"},
}
REC_CRIME = {}
REC_VERDICT = {}   # (役職, 罪名, 列) → (結果, 頁)
REC_SENT = {}      # 役職 → (確定した刑, 頁)
REC_SEATS = 0
REC_UNANIMOUS = set()
HEADS = set()
REC_MECH = {          # 流れ図に出してよい言葉のうち、役職・罪名でないもの（仕組み・鎖・問いの箱と矢印の札）
    "スレッシャーの艦長",      # c218 の左上の札（R08 p.107＝艦長と副長の交代の問い）
    "外さないという決定",      # c616 の見出しの箱（認定105＝R08 p.197「decision was made on 4 December 1962 not to unlag」）
    "上がっていない", "造船所の中",   # c618 の矢印の札・群の名（認定108・J p.14「the decision was made locally in the yard」）
}
REC_CHIP = {          # 札（chip）の言葉 → 頁の集合
    "両院原子力合同委員会・1963年と1964年": {"J p8001", "J p8091"},   # c110（J p.1＝1963年6月26日・p.91＝1964年7月1日）
    "最も資格のある1人（人事局長）": {"R08 p4109"},                    # c218（one of the best qualified people we could find）
    "決定の写し": {"R08 p4197"},                                        # c616（認定106 a copy of this decision）
}
# 書類の再現図（表題 → dict(fields・ends・values＝記録の文にある値だけ・rec＝頁の集合)）。🆕 18本目は欄の値に**原文の英語**をそのまま
#   書く（日本語は字幕だけ＝ルール 0b-33）。🔴 査問会の「0913R」の形は画面に出さない（台本 §1-7）＝時刻は欄の名へ。
#   ⚠️ 文字の層の崩れを頁の画像で直した所：認定111「SCULPIN8 ETHAN' ALLEN」→ SCULPIN, ETHAN ALLEN・認定24「COMMIUNICATE」→
#   COMMUNICATE・V1 p.140「No, sirs I don 9 t thifilk so.」→ No, sir, I don't think so.・X p.122「trv be interrupted」→ may be
#   interrupted・X p.124「May bear very weak voice」→ May hear very weak voice（2026-10-04 に原寸の切り出しで読んだ）
REC_FORM = {
    # c112：R08 p.181「FINDINGS OF FACT」・p.204「OPINIONS」・p.217「RECOMMENDATIONS」（紙3枚）
    "認定": dict(fields={"見出し"}, ends=set(), rec={"R08 p4181"}, values={"見出し": "FINDINGS OF FACT"}),
    "意見": dict(fields={"見出し"}, ends=set(), rec={"R08 p4204"}, values={"見出し": "OPINIONS"}),
    "勧告": dict(fields={"見出し"}, ends=set(), rec={"R08 p4217"}, values={"見出し": "RECOMMENDATIONS"}),
    # c209：認定96（R08 p.196）・認定86（p.195）
    "衝撃試験の損傷（認定96・86）": dict(
        fields={"調べた人", "調べ方", "直す予定"}, ends=set(), rec={"R08 p4196", "R08 p4195"},
        values={"調べた人": "ship's force, Bureau of Ships, and Shipyard personnel", "調べ方": "intensively investigated",
                "直す予定": "scheduled for repair during the post shakedown availability"}),
    # c213：認定69（R08 p.193）
    "取扱説明書（認定69）": dict(
        fields={"作った所", "手本", "写し方", "違い"}, ends=set(), rec={"R08 p4193"},
        values={"作った所": "an outside firm under subcontract", "手本": "an SS(N) 588 Class Ship Information Book as a guide",
                "写し方": "virtually copied large portions of it", "違い": "many systems on THRESHER were quite different"}),
    # c217：R08 p.107（1963年5月21日・非公開の場＝THIRTY-THIRD DAY・Tuesday, 21 May 1963）
    "人事局長の証言（1963年5月21日）": dict(
        fields={"理由", "何の圧力"}, ends=set(), rec={"R08 p4107"},
        values={"理由": "The basic consideration was the pressure",
                "何の圧力": "to furnish experienced commanding officers for the POLARIS submarines"}),
    # c219：R08 p.77
    "部隊の司令の証言（査問会）": dict(
        fields={"助言", "答え", "挙げた例", "ほかに"}, ends=set(), rec={"R08 p4077"},
        values={"助言": "he must resist that pressure", "答え": "he would resist it",
                "挙げた例": "some hot words exchanged between the boat officer and the Ship Superintendent",
                "ほかに": "That was the only incident I know of."}),
    # c305：認定8（R08 p.184）
    "2隻の命令（認定8）": dict(
        fields={"スレッシャー", "スカイラーク", "予定表"}, ends=set(), rec={"R08 p4184"},
        values={"スレッシャー": "THRESHER's movement orders were CONFIDENTIAL", "スカイラーク": "SKYLARK's were unclassified",
                "予定表": "were not held by SKYLARK"}),
    # c416：V1 p.118（記録の45頁・航海士）
    "航海士の証言（査問会の記録）": dict(
        fields={"前に聞いた音", "どんな船", "似ていた音"}, ends=set(), rec={"V1 p118"},
        values={"前に聞いた音": "a lot of ships breaking up during World War II", "どんな船": "after having been torpedoed at depths",
                "似ていた音": "a compartment collapsing"}),
    # c418：V1 p.132（甲板の当直の下士官＝p.127 で証言台に）・p.140（記録簿の係の無線員＝p.136）
    "スカイラークの乗員の証言": dict(
        fields={"当直の下士官", "問い", "記録簿の係"}, ends=set(), rec={"V1 p132", "V1 p140"},
        values={"当直の下士官": "air rushing into his tanks for about four to five seconds",
                "問い": "like air being blown into a tank", "記録簿の係": "No, sir, I don't think so."}),
    # c509：認定24（R08 p.186＝頁の画像で読んだ）
    "スカイラークの電文（認定24）": dict(
        fields={"9:17 から", "最後の交信", "示したこと", "いま"}, ends=set(), rec={"R08 p4186"},
        values={"9:17 から": "UNABLE TO COMMUNICATE WITH THRESHER", "最後の交信": "LAST TRANSMISSION RECD WAS GARBLED",
                "示したこと": "INDICATED THRESHER WAS APPROACHING TEST DEPTH", "いま": "CONDUCTING EXPANDING SEARCH"}),
    # c510：認定25（R08 p.186〜187）
    "査問会の認定25": dict(
        fields={"9:13 の声", "勧めた人", "艦長", "その後"}, ends=set(), rec={"R08 p4186", "R08 p4187"},
        values={"9:13 の声": "Experiencing minor difficulty", "勧めた人": "suggested by the Operations Officer",
                "艦長": "the Commanding Officer decided not to include such information",
                "その後": "did not include such additional information in any subsequent reports"}),
    # c517：証拠49（X p.122＝11日 12時19分・p.124＝14時33分）
    "シーウルフの報告（証拠49）": dict(
        fields={"合図", "声"}, ends=set(), rec={"X p1122", "X p1124"},
        values={"合図": "what may be interrupted keying", "声": "May hear very weak voice"}),
    # c522：意見48（R08 p.214）
    "査問会の意見48": dict(
        fields={"伝えなかったこと", "どのくらい", "関わり"}, ends=set(), rec={"R08 p4214"},
        values={"伝えなかったこと": "failed fully to inform higher authority", "どのくらい": "for an unreasonable length of time",
                "関わり": "could not conceivably have contributed in any way to the loss of THRESHER"}),
    # c603：認定112（R08 p.198）
    "査問会の認定112": dict(
        fields={"どの艦", "系統", "大きさ", "数"}, ends=set(), rec={"R08 p4198"},
        values={"どの艦": "an S5W reactor equipped ship", "系統": "in hazardous systems", "大きさ": "of 2-inch size and above",
                "数": "over 3000"}),
    # c604・c605（紙1枚目）：認定111（R08 p.198＝頁の画像で艦名を読んだ）。c604＝本文の一文／c605＝スケートの括弧（深さは語りに無い＝書かない）
    "査問会の認定111": dict(
        fields={"いつ", "どの艦", "何が", "スケート", "場所"}, ends=set(), rec={"R08 p4198"},
        values={"いつ": "prior to THRESHER's post shakedown availability",
                "どの艦": "BARBEL, SKATE, SNOOK, SCULPIN, ETHAN ALLEN and THRESHER",
                "何が": "reports of serious failures of sil-braze joints",
                "スケート": "a 3-inch sil-braze joint parted", "場所": "under the ice"}),
    # c605（紙2枚目）：大西洋艦隊の司令官の意見書（IR18 p.123「The failure of the sil-braze joint in SKATE did not occur under the ice but in
    #   open water」）
    "艦隊司令官の意見書": dict(
        fields={"訂正", "場所"}, ends=set(), rec={"IR18 p2123"},
        values={"訂正": "did not occur under the ice", "場所": "in open water"}),
    # c609：認定98（R08 p.196＝艦船局の手紙 1962年8月28日を引く）
    "艦船局の手紙（1962年8月28日）": dict(
        fields={"何を", "いつまで", "どれだけ"}, ends=set(), rec={"R08 p4196"},
        values={"何を": "employ a minimum of at least one ultrasonic test team",
                "いつまで": "throughout the entire assigned post shakedown availability",
                "どれだけ": "the maximum number of sil-braze joints"}),
    # c610：認定99（R08 p.196）
    "作業の指示書（認定99）": dict(
        fields={"班", "先に", "時間があれば"}, ends=set(), rec={"R08 p4196"},
        values={"班": "use of one ultrasonic test team", "先に": "to test first those joints not lagged",
                "時間があれば": "lagging would be removed to permit tests of additional joints"}),
    # c622：意見21（R08 p.207）
    "査問会の意見21": dict(
        fields={"誰が", "何を", "判断"}, ends=set(), rec={"R08 p4207"},
        values={"誰が": "the management of the Portsmouth Naval Shipyard", "何を": "determining not to unlag pipes",
                "判断": "did not exercise good judgment"}),
    # c624：J p.67（「the testimony I gave in closed session to the court of inquiry on April 29, 1963」）・p.68
    "原子炉の責任者の証言（1963年4月29日）": dict(
        fields={"調べた分", "その結果"}, ends=set(), rec={"J p8067", "J p8068"},
        values={"調べた分": "about 5 percent of her silver-brazed joints were ultrasonically inspected",
                "その結果": "about 10 percent of those checked required repair or replacement"}),
}
REC_CAUSE = {         # 並べ図の項目 → 頁
    # c115：この動画の3つの問い（c114 の語り）＝その問いに答える記録の頁（意見1・認定108／25・1964年の要旨）
    "浮き上がれなかった理由": {"R08 p4204"}, "伝わらなかった検査と声": {"R08 p4197", "R08 p4186"},
    "海の底に残った物": {"R17書 p9802"},
}
MARKS = {"？"}
EXTRA = {"模式図"}


def allowed():
    """流れ図の画面に出してよい言葉＝**いまの**記録の表から組む（2026-09-30 15本目 ⑤b-1）。
    ⚠️ 以前は読み込みの瞬間に組んだ定数（ALLOWED）だった＝表を selftest の見本に差し替えても空のまま残る形だった。"""
    return ({t for v in REC_CREW.values() for t in v} | set(REC_OTHER_ROLE) | set(REC_CRIME) | {"有罪", "無罪"}
            | {s for s, _ in REC_SENT.values()} | HEADS | REC_MECH | set(REC_CHIP) | MARKS | EXTRA)
ALERTS = None     # jiko_style の赤（読み込んでから埋める）
TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')


def _texts(svg):
    """画面の文字（注と出典の行を除く）。"""
    out = []
    for m in TEXT.finditer(svg):
        q = dict(ATTR.findall(m[1])).get("data-q", "")
        if q != "note":
            out.append((q, _unesc(m[2])))
    return out


def _alert_bad(svg):
    import jiko_style as J
    return [f"赤（{c}）を使っている＝責める形にしない" for c in (J.ALERT, J.ALERT_DIM) if c.lower() in svg.lower()]


# ══════════════════════════════════════════════════════════
#  流れ図
# ══════════════════════════════════════════════════════════
def judge_flow(f):
    svg = f.lab + "".join(f.stages)
    bad, n = [], 0
    ok_words = allowed()
    for q, t in _texts(svg):
        n += 1
        if t not in ok_words:
            bad.append(f"画面の文字「{t}」（{q or '印なし'}）が記録の表の言葉に無い＝名前・記録に無い言葉を書かない")
    bad += _alert_bad(svg)
    if "<circle" in svg:
        bad.append("円を使っている（人の頭に読める形＝人の形を使わない）")
    els = _els(svg)
    seats = sum(1 for e in els if e["q"] == "seat")
    on = sum(1 for e in els if e["q"] == "seat_on")
    n += 2
    if seats not in (0, REC_SEATS):
        bad.append(f"席が {seats} 個（裁判官は {REC_SEATS} 人＝判決 p79〜81）")
    if on not in (0, seats):
        bad.append(f"灯した席が {on}／{seats}（全員一致なら全部・そうでなければ灯さない）")
    parts = [p for p in f.mech["parts"]]
    nodes = {p["id"]: p for p in parts if p["k"] in ("role", "crime", "res")}
    edges = [p for p in parts if p["k"] == "edge"]
    ins = {}
    for e in edges:
        for t in (e["to"] if isinstance(e["to"], list) else [e["to"]]):
            ins.setdefault(t, []).append(e)
    # ⑥ 部品の頁
    for p in nodes.values():
        n += 1
        if p["k"] == "role":
            ok = (p["t"] in REC_OTHER_ROLE and _recs(p["rec"]) & REC_OTHER_ROLE[p["t"]]) or \
                 (p["t"] not in REC_OTHER_ROLE and _recs(p["rec"]) & REC_ROLE_PAGES)
        elif p["k"] == "crime":
            ok = _recs(p["rec"]) & REC_CRIME.get(p["t"], set())
        else:
            ok = True     # 結果の頁は ② で組ごとに見る
        if not ok:
            bad.append(f"箱「{p['t']}」の rec {p['rec']} が記録の頁と合わない")

    def up(nid, seen=()):
        """nid から矢印を逆にたどった（役職の list, いちばん近い罪名, 点線か）。"""
        roles, crime, lead = [], None, False
        for e in ins.get(nid, []):
            lead |= e.get("style") == "leader"
            for fr in (e["fr"] if isinstance(e["fr"], list) else [e["fr"]]):
                if fr in seen:
                    continue
                p = nodes.get(fr)
                if not p:
                    continue
                if p["k"] == "role":
                    roles.append(p["t"])
                else:
                    r2, c2, _ = up(fr, seen + (nid,))
                    roles += r2
                    crime = crime or (p["t"] if p["k"] == "crime" else c2)
        return roles, crime, lead

    unanimous = False
    for p in nodes.values():
        if p["k"] != "res":
            continue
        roles, crime, lead = up(p["id"])
        n += 1
        if not roles:
            bad.append(f"結果の箱「{p['t']}」（{p['col']}）に役職がつながっていない")
            continue
        for r in roles:
            n += 1
            if crime:
                want = REC_VERDICT.get((r, crime, p["col"]))
                if not want:
                    bad.append(f"「{r}→{crime}→{p['t']}（{p['col']}）」は記録の表に無い組")
                elif want[0] != p["t"] or not (_recs(p["rec"]) & want[1]):
                    bad.append(f"「{r}→{crime}」の{p['col']}の結果が「{p['t']}」（記録は「{want[0]}」{sorted(want[1])}）")
                unanimous |= (r, crime) in REC_UNANIMOUS and p["col"] == "c3"
            else:
                want = REC_SENT.get(r)
                if not want or want[0] != p["t"] or p["col"] != "c3" or not (_recs(p["rec"]) & want[1]):
                    bad.append(f"「{r}」の刑の箱が「{p['t']}」（{p['col']}）（記録は {want and want[0]}・大法院の列）")
                if not lead:
                    bad.append(f"「{r}」の刑は点線でつなぐ（罪名の矢印と読み分ける）")
    if on and not unanimous:
        bad.append("席が灯っているのに、全員一致の記録（REC_UNANIMOUS）の結果が無い")
    # ④ 甲板部・機関部の役職（cb02）
    grp = {}
    for p in parts:
        if p["k"] == "role" and p.get("grp"):
            grp.setdefault(p["grp"], []).append(p["t"])
    for g, ts in grp.items():
        n += 1
        if sorted(ts) != sorted(REC_CREW.get(g, [])):
            bad.append(f"{g}の役職 {len(ts)}人 {ts} が記録（判決 p2〜3）の {len(REC_CREW.get(g, []))}人と違う")
    for p in parts:
        if p["k"] == "chip":
            n += 1
            if not (_recs(p["rec"]) & REC_CHIP.get(p["t"], set())):
                bad.append(f"札「{p['t']}」の rec {p['rec']} が記録の頁と合わない")
    # ⑨ 🆕 2026-09-30（15本目 ⑤c'）：矢印の線が箱の中を通らない。c918 の問い（上）→答え（真下）は横の線が両方の字の
    #    真ん中を通り、打ち消し線に見えた（原寸）＝型は「左→右」しか描けなかった。字は箱の中にある＝箱の内側（辺から3画素）
    #    に線分が入ったら止める。線分は型が描いたものそのもの（`segs`＝boxes._edge）
    rects = [(p["id"], p["x0"], p["x1"], p["cy"] - p["h"] / 2, p["cy"] + p["h"] / 2)
             for p in list(nodes.values()) + list(f.mech.get("heads") or [])]
    hit = set()
    for e in edges:
        ek = (str(e["fr"]), str(e["to"]))       # fr・to はリストのこともある（寄せる・分ける矢印）＝文字にして鍵に
        for x1, y1, x2, y2 in e.get("segs") or []:
            n += 1
            for bid, bx0, bx1, by0, by1 in rects:
                if ek + (bid,) not in hit and _seg_enters(x1, y1, x2, y2, bx0 + 3, bx1 - 3, by0 + 3, by1 - 3):
                    hit.add(ek + (bid,))
                    bad.append(f"矢印 {e['fr']}→{e['to']} の線が箱「{bid}」の中を通る（字に打ち消し線が引かれて見える）")
    return bad, n


def _seg_enters(x1, y1, x2, y2, bx0, bx1, by0, by1):
    """線分が箱の内側に入るか（2画素ごとに当てる）。"""
    k = max(1, int(max(abs(x2 - x1), abs(y2 - y1)) / 2))
    return any(bx0 < x1 + (x2 - x1) * i / k < bx1 and by0 < y1 + (y2 - y1) * i / k < by1 for i in range(k + 1))


# ══════════════════════════════════════════════════════════
#  書類の再現図
# ══════════════════════════════════════════════════════════
PAPER_SPAN = (72, 1848)     # 🆕 18本目 ⑤b-6a：紙を並べる範囲＝図の本体の左右（titan_fig.BX0・BX1＝型の定数を読まない）
PAPER_GAP_MIN = 24          # 並べた紙どうしの間（これより狭いと1枚の紙に見える）


def _judge_paper(els, parts, head=""):
    """紙1枚ぶん（els＝その紙の印の要素・印の `@番号` は外してある／parts＝その紙の段の部品）。"""
    bad, n = [], 3
    title = next((_unesc(e["text"]) for e in els if e["q"] == "ftitle"), "")
    r = REC_FORM.get(title)
    if not r:
        return [f"{head}書類の表題「{title}」が記録の表に無い"], n
    fields = {_unesc(e["text"]) for e in els if e["q"].startswith("field|")}
    ends = {_unesc(e["text"]) for e in els if e["q"].startswith("ntext|role|")}
    if not fields <= r["fields"]:
        bad.append(f"{head}欄 {sorted(fields - r['fields'])} は報告書の文に無い（無い欄を描かない）")
    if not ends <= r["ends"]:
        bad.append(f"{head}行き来の箱 {sorted(ends - r['ends'])} が記録に無い")
    for e in els:
        if e["q"].startswith("fval|"):
            n += 1
            nm = e["q"].split("|", 1)[1]
            if r["values"].get(nm) != _unesc(e["text"]):
                bad.append(f"{head}欄「{nm}」に値「{_unesc(e['text'])}」（記録は {r['values'].get(nm) or '未記入'}）")
    tag = next((_unesc(e["text"]) for e in els if e["q"] == "reprot"), "")
    if tag != "再現":
        bad.append(f"{head}「再現」の札が無い（「{tag}」）＝自作の用紙だと画面で言う")
    for p in parts:
        n += 1
        rs = _recs(p["rec"])
        if not (rs & r["rec"]):
            bad.append(f"{head}{p['k']} の rec {p['rec']} が記録の頁 {sorted(r['rec'])} と合わない")
        for fd in p.get("fields") or []:
            n += 1
            if not (_recs(fd["rec"]) & r["rec"]):
                bad.append(f"{head}欄「{fd['t']}」の rec {fd['rec']} が記録の頁と合わない")
    return bad, n


def judge_form(f):
    svg = f.lab + "".join(f.stages)
    els = _els(svg)
    # 🆕 2026-10-04（18本目 ⑤b-6a）：紙を2〜3枚並べる書類（印に `@番号`）は紙ごとに照らす（c605＝査問会の認定と艦隊司令官の意見書）
    idx = sorted({int(m[1]) for e in els for m in [re.match(r"ftitle@(\d+)$", e["q"])] if m})
    if not idx:
        bad, n = _judge_paper(els, f.mech["parts"])
        return bad + _alert_bad(svg), n
    bad, n = [], 0
    for i in idx:
        sub = []
        for e in els:
            m = re.match(rf"^([a-z]+)@{i}(\|.*)?$", e["q"])
            if m:
                sub.append(dict(e, q=m[1] + (m[2] or "")))
        b, k = _judge_paper(sub, [p for p in f.mech["parts"] if p.get("i", 0) == i], f"紙{i + 1}：")
        bad += b
        n += k
    # ⑩ 紙どうしが重ならない・本体の左右の外へ出ない（焼く直前の SVG の四角を読む）
    rects = sorted((float(e["a"]["x"]), float(e["a"]["x"]) + float(e["a"]["width"]), e["q"])
                   for e in els if re.fullmatch(r"paper@\d+", e["q"]))
    for a0, a1, q in rects:
        n += 1
        if a0 < PAPER_SPAN[0] or a1 > PAPER_SPAN[1]:
            bad.append(f"紙 {q}（x {a0:.0f}〜{a1:.0f}）が図の本体 {PAPER_SPAN} の外へ出る")
    for (a0, a1, qa), (b0, b1, qb) in zip(rects, rects[1:]):
        n += 1
        if b0 - a1 < PAPER_GAP_MIN:
            bad.append(f"紙 {qa} と {qb} の間が {b0 - a1:.0f} 画素（{PAPER_GAP_MIN} 未満＝重なるか1枚に見える）")
    return bad + _alert_bad(svg), n


# ══════════════════════════════════════════════════════════
#  並べ図
# ══════════════════════════════════════════════════════════
def judge_row(f):
    svg = f.lab + "".join(f.stages)
    els = _els(svg)
    bad, n = [], 2
    items = [e for e in els if e["q"].startswith("item|")]
    if len(items) < 2:
        bad.append(f"並べる項目が {len(items)} つ（2つ以上を同じ形で並べる）")
    forms = {(e["a"].get("width"), e["a"].get("height"), e["a"].get("stroke")) for e in items}
    if len(forms) > 1:
        bad.append(f"項目の箱の形か色が揃っていない {sorted(forms)}＝どれかを目立たせない")
    for q, t in _texts(svg):
        n += 1
        if not (q.startswith("itext|") and t in REC_CAUSE):
            bad.append(f"画面の文字「{t}」（{q or '印なし'}）が原因の項目の表に無い＝並べ図に項目のほかを書かない")
    for e in els:
        if e["q"] not in ("note",) and not e["q"].startswith(("item|", "itext|")):
            bad.append(f"並べ図に項目のほかの部品（{e['q']}）＝場面にしない")
    if re.search(r"<(circle|path|polygon)\b", svg):
        bad.append("並べ図に線や絵（path・circle）がある＝場面にしない")
    for p in f.mech["parts"]:
        n += 1
        if not (_recs(p["rec"]) & REC_CAUSE.get(p["t"], set())):
            bad.append(f"項目「{p['t']}」の rec {p['rec']} が記録の頁と合わない")
    bad += _alert_bad(svg)
    return bad, n


def judge(kw):
    import boxes as B
    f = B.boxes(**kw)
    return {"flow": judge_flow, "form": judge_form, "row": judge_row}[kw["view"]](f)


# ══════════════════════════════════════════════════════════
#  物差しの検算
# ══════════════════════════════════════════════════════════
def selftest_ep15():
    """15本目（⑤b-5）の書類の再現図・鎖・答えの図・実況の担当の検算＝**見本 `fixture_ep15`（15本目の表）を差し込んで**回す。
    🔴 2026-10-01（16本目 ⑤b-1）：本番の表（この門番の REC_*）は16本目の空の器にした＝15本目の値は
       `fixture_ep15.GATES["check_boxes"]`（14本目と同じ作り）。型の側の表（ss.FORM_ENTRY09・CHAIN2・ANS・MC ほか）と GEO も
       15本目の見本になる＝落ちても終わっても `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep15`"""
    import fixture_ep15
    fixture_ep15.apply(sys.modules[__name__])
    try:
        return _selftest_ep15()
    finally:
        fixture_ep15.restore()


def _selftest_ep15():
    """15本目の検算の本体（`fixture_ep15` を差し込んだ中で呼ぶ）。"""
    from cuts import ss
    entry = dict(view="form", form=ss.FORM_ENTRY09, note="n", src="s",
                 steps=[dict(add=dict(k="paper")), dict(add=dict(k="fill", f="大きな改造をしたか"))])
    bad_v = dict(ss.FORM_ENTRY09, fields=[dict(ss.FORM_ENTRY09["fields"][0], v="いいえ")])
    bad_f = dict(ss.FORM_ENTRY09, fields=[dict(t="飛んだ時間", rec="AAB p37")])     # 型は通す＝門番が止めるか
    chain = dict(view="flow", layout=ss.CHAIN2, steps=[dict(add=ss.chain_links())], note="n", src="s")
    bad_w = dict(chain, layout=dict(heads=ss.CHAIN2["heads"][:5] + [dict(ss.CHAIN2["heads"][5], t="墜落の原因")]))
    # 🆕 ⑤c'（2026-09-30）：答えと手がかり（c918）＝問い（上）→答え（真下）の矢印
    ans = dict(view="flow", layout=ss.ANS, steps=[dict(add=[ss.ANSP["a1"], ss.ANSP["a2"], ss.ANSP["a3"]] + ss.ans_links())],
               note="n", src="s")
    cases = [("15本目 正しい参加の書類（後から「はい」）", entry, True),
             ("🔴 15本目 陽性対照：書き込む値が記録と違う（いいえ）", dict(entry, form=bad_v), False),
             ("🔴 15本目 陽性対照：報告書の文に無い欄", dict(entry, form=bad_f, steps=[dict(add=dict(k="paper"))]), False),
             ("15本目 正しい報告書の鎖", chain, True),
             ("🔴 15本目 陽性対照：鎖に記録の表に無い言葉", bad_w, False),
             ("15本目 正しい答えの図（問い→真下の答えは縦の矢印）", ans, True),
             # ⚠️ ⑤c'：⑨ を足した最初の版は、fr・to がリストの矢印（分ける・寄せる）で門番ごと落ちた（本番の c806 で）
             #    ＝見本が1対1の矢印だけだった → 分ける矢印の見本を置く
             ("15本目 正しい実況の担当（1つから2つへ分ける矢印）",
              dict(view="flow", layout=ss.MC, note="n", src="s",
                   steps=[dict(add=[ss.MCP["a_help"], ss.MCP["a_med"], dict(k="edge", fr="mc", to=["a_help", "a_med"])])]),
              True)]
    ok = True
    for name, kw, want in cases:
        try:
            bad, _ = judge(kw)
        except ValueError as e:
            bad = [f"型が止まった：{e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照（型を壊す）：縦の矢印を切る（VERT=False）＝⑤c の c918 と同じ絵（横の線が問いと答えの字を通る）→ ⑨ が鳴ること
    import boxes as B
    keep = B.VERT
    B.VERT = False
    try:
        bad, _ = judge(ans)
    finally:
        B.VERT = keep
    hit7 = any("の中を通る" in b for b in bad)
    ok &= hit7
    print(f"  {'OK' if hit7 else '🔴 NG'} 🔴 15本目 陽性対照（型を壊す）：縦の矢印を切る（VERT=False）: "
          f"{'不合格' if bad else '合格'}（⑨で不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    return ok


def selftest_ep18():
    """🆕 2026-10-04（18本目 ⑤b-6a）：紙を並べる書類（c605・c112）・電文の時刻の形・流れ図（c618）・並べ図（c115）の検算。
    本番の表（この門番の REC_*＝18本目）と ss の18本目の値で回す（🔴 19本目の ⑤b-1 で見本 fixture_ep18 を差す形に直す）。
    陽性対照＝筋を壊す（値・語・枚数）＋型の定数を壊す（FORM_GAP を負に＝紙が重なる・FORM_SPAN を画面いっぱいに＝本体の外）"""
    import boxes as B
    from cuts import ss
    ok = True
    pair = dict(view="form", form=[ss.FORM_F111S, ss.FORM_CINC], note="n", src="s",
                steps=[dict(add=[dict(k="paper", i=0), dict(k="fill", i=0, f="スケート")]),
                       dict(add=dict(k="fill", i=0, f="場所")), dict(add=dict(k="paper", i=1))])
    three = dict(view="form", form=ss.FORM_COURT3, note="n", src="s",
                 steps=[dict(add=[dict(k="paper", i=0), dict(k="paper", i=1)]), dict(add=dict(k="paper", i=2))])
    msg = dict(view="form", form=ss.FORM_MSG, note="n", src="s",
               steps=[dict(add=dict(k="paper")), dict(add=[dict(k="fill", f="示したこと"), dict(k="fill", f="いま")])])
    up = dict(view="flow", layout=ss.FL_UP, src="s",
              steps=[dict(add=[dict(k="grp", t="造船所の中", x=130, y=360), ss.fl("u_res"), ss.fl("u_dec"), ss.fl("u_bu")]),
                     dict(add=ss.ce(["u_res", "u_dec"], "u_bu", style="leader", lab="上がっていない"))])
    row = dict(view="row", slots=3, src="s", steps=[dict(add=[ss.cause("q_float"), ss.cause("q_pass"), ss.cause("q_sea")])])
    bad_cinc = dict(ss.FORM_CINC, fields=[dict(ss.FORM_CINC["fields"][0], v="under the ice"), ss.FORM_CINC["fields"][1]])
    bad_msg = dict(ss.FORM_MSG, fields=[dict(ss.FORM_MSG["fields"][0], v="UNABLE TO COMMUNICATE WITH THRESHER SINCE 0917R")]
                   + list(ss.FORM_MSG["fields"][1:]))

    def run(name, kw, want):
        nonlocal ok
        try:
            bad, _ = judge(kw)
        except (ValueError, KeyError) as e:
            bad = [f"型が止まった：{type(e).__name__} {e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} 18本目 {name}: {'合格' if got else '不合格'}（{'合格' if want else '不合格'}のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    run("正しい紙2枚（c605＝査問会の認定111・艦隊司令官の意見書）", pair, True)
    run("正しい紙3枚（c112＝認定・意見・勧告）", three, True)
    run("正しい電文（c509＝時刻は欄の名へ）", msg, True)
    run("正しい流れ図（c618＝造船所の中 → 艦船局へ上がっていない）", up, True)
    run("正しい並べ図（c115＝3つの問い）", row, True)
    run("🔴 陽性対照：紙2枚目の値が記録と違う（under the ice）", dict(pair, form=[ss.FORM_F111S, bad_cinc]), False)
    run("🔴 陽性対照：電文の値に「0917R」の形（記録の表は時刻を欄の名へ移した）", dict(msg, form=bad_msg), False)
    run("🔴 陽性対照：紙を4枚並べる", dict(three, form=ss.FORM_COURT3 + [ss.FORM_CINC]), False)
    run("🔴 陽性対照：紙2枚目の欄を紙1枚目に書き込む（fill i=0 の「訂正」）",
        dict(pair, steps=pair["steps"] + [dict(add=dict(k="fill", i=0, f="訂正"))]), False)
    run("🔴 陽性対照：次のカット（c619）の語りの箱を足す（艦に命令を出す側）",
        dict(up, steps=[dict(add=up["steps"][0]["add"] + [dict(k="role", id="u_op", t="艦に命令を出す側", y=700,
                                                               pos=(1280, 1760), rec="R08 p4197")])] + up["steps"][1:]), False)
    run("🔴 陽性対照：並べ図に記録の表に無い項目（なぜ沈んだか）",
        dict(row, steps=[dict(add=[ss.cause("q_float"), dict(k="item", t="なぜ沈んだか", rec="R08 p4204")])]), False)

    def broken(name, attr, val, kw):
        nonlocal ok
        keep = getattr(B, attr)
        setattr(B, attr, val)
        try:
            bad, _ = judge(kw)
        except (ValueError, KeyError) as e:
            bad = [f"型が止まった：{e}"]
        finally:
            setattr(B, attr, keep)
        ok &= bool(bad)
        print(f"  {'OK' if bad else '🔴 NG'} 🔴 18本目 陽性対照（型を壊す）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    broken("紙の間を負にする（FORM_GAP＝−100＝紙が重なる）", "FORM_GAP", -100, pair)
    broken("紙の範囲を画面いっぱいに（FORM_SPAN＝0〜1920）", "FORM_SPAN", (0, 1920), three)
    broken("紙の間を狭める（FORM_GAP＝10＝1枚の紙に見える）", "FORM_GAP", 10, three)
    return ok


def selftest():
    # 🆕 2026-10-04（18本目 ⑤b-6a）：本番の表（18本目）で先に検算する（あとの見本の差し込みより前）
    ok18 = selftest_ep18()
    # 🔴 2026-09-30（15本目 ⑤b-5）：先に15本目の書類と鎖を検算してから、14本目の見本に差し替える
    #    （2026-10-01〜：15本目も見本 fixture_ep15 の表＝selftest_ep15 が差し込んで・終わったら戻す）
    ok15 = selftest_ep15()
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（本番の表は回ごとに空にする＝§0b）＝この処理の中だけ14本目にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    import boxes as B
    from cuts import ss
    ok = True
    cap = [ss.ct("r_captain"), ss.ct("x_cap"), ss.ce("r_captain", "x_cap"), ss.ct("o_cap"), ss.ce("x_cap", "o_cap"),
           dict(k="seats_on", n=13, rec="判決 p39")]
    sent = [ss.ct("r_mate1"), ss.ct("s_mate1"), ss.ce("r_mate1", "s_mate1", style="leader")]
    flow = dict(view="flow", layout=ss.CT, steps=[dict(add=cap), dict(add=sent)], src="s")
    crew = dict(view="flow", layout=ss.CT, steps=[dict(add=ss.CREW15)], src="s")
    form = dict(view="form", form=ss.FORM_PRE, steps=[dict(add=[dict(k="end", id="ship"), dict(k="paper"),
                                                                dict(k="edge", fr="ship", to="paper")])], src="s")
    row = dict(view="row", slots=3, steps=[dict(add=[ss.cause("rudder"), ss.cause("fault")])], src="s")

    def run(name, kw, want):
        nonlocal ok
        try:
            bad, _ = judge(kw)
        except (ValueError, KeyError) as e:
            bad = [f"型が止まった：{type(e).__name__} {e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}（{'合格' if want else '不合格'}のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    run("正しい流れ図（船長→殺人・殺人未遂→有罪・13席・1等航海士→懲役12年）", flow, True)
    run("正しい船員15人（甲板部8・機関部7）", crew, True)
    run("正しい書類の再現図（乗船人員・貨物量・空欄）", form, True)
    run("正しい並べ図（舵の使い方？・装置の故障？）", row, True)
    run("🔴 陽性対照：役職の箱に名前（山田船長）", dict(flow, steps=[dict(add=[ss.ct("r_captain", t="山田船長")] + cap[1:])]), False)
    run("🔴 陽性対照：刑のつなぎ違い（1等航海士→懲役7年）",
        dict(flow, steps=[dict(add=cap), dict(add=[ss.ct("r_mate1"), ss.ct("s_mate2", row="1等航海士"),
                                                   ss.ce("r_mate1", "s_mate2", style="leader")])]), False)
    run("🔴 陽性対照：無罪の箱を1審の列に（舵の過失）",
        dict(flow, steps=[dict(add=[ss.ct("r_mate3"), ss.ct("x_rudder"), ss.ce("r_mate3", "x_rudder"),
                                    ss.ct("o_rud2", col="c1"), ss.ce("x_rudder", "o_rud2")])]), False)
    run("🔴 陽性対照：席が12", dict(flow, layout=dict(ss.CT, seats=dict(ss.CT["seats"], n=12))), False)
    run("🔴 陽性対照：甲板部の役職が1人欠ける", dict(crew, steps=[dict(add=ss.CREW15[:2] + ss.CREW15[3:])]), False)
    run("🔴 陽性対照：書類に報告書に無い欄（船長の署名）",
        dict(form, form=dict(ss.FORM_PRE, fields=list(ss.FORM_PRE["fields"]) + [dict(t="船長の署名", rec="海審 p1037")])),
        False)
    run("🔴 陽性対照：書類の欄に値（乗船人員 476）",
        dict(form, form=dict(ss.FORM_PRE, fields=[dict(t="乗船人員", rec="海審 p1037", v="476人")])), False)
    run("🔴 陽性対照：並べ図に記録に無い項目（爆発？）",
        dict(row, steps=[dict(add=[ss.cause("rudder"), dict(k="item", t="爆発？", rec="特調委 p3013")])]), False)
    run("🔴 陽性対照：並べ図の項目が1つ", dict(row, steps=[dict(add=[ss.cause("rudder")])]), False)

    def broken(name, obj, attr, val, kw):
        nonlocal ok
        keep = getattr(obj, attr)
        setattr(obj, attr, val)
        try:
            bad, _ = judge(kw)
        except (ValueError, KeyError) as e:
            bad = [f"型が止まった：{e}"]
        finally:
            setattr(obj, attr, keep)
        ok &= bool(bad)
        print(f"  {'OK' if bad else '🔴 NG'} 🔴 陽性対照（型を壊す）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    broken("結果の箱を赤で描く（KSTY）", B, "KSTY", dict(B.KSTY, res=("ALERT", 28, 40)), flow)
    broken("「再現」の札を書かない（REPRO）", B, "REPRO", "", form)
    import titan_fig as F
    rect0 = F.rect
    cnt = [0]

    def uneven(x, y, w, h, *a, **k):
        cnt[0] += 1
        return rect0(x, y, w + (40 if cnt[0] == 1 else 0), h, *a, **k)
    broken("並べ図の最初の箱だけ広く描く（F.rect）", F, "rect", uneven, row)
    ok = ok and ok15 and ok18
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
    targets = {c: s["fig"][1] for c, s in sorted(cuts.SPEC.items()) if s.get("fig") and s["fig"][0] == "boxes"}
    if not targets:
        print("⚠️ boxes のカットが0件（この回に流れ図・書類・並べ図が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
        return 0
    bad_all, n_all = 0, 0
    for cid, kw in targets.items():
        bad, n = judge(kw)
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {cid}（boxes・{kw['view']}）: {b}")
        else:
            print(f"✓ {cid}（boxes・{kw['view']}）: 言葉・つながり・形 {n}件が記録と合う")
    print(f"\n{'✓' if not bad_all else '🔴'} 箱の型 {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
