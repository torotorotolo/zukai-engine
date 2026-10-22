# -*- coding: utf-8 -*-
"""24本目②：① の主張を「書かれた頁」に当てる（① を引き写さない）。
各行＝(記号, 資料の頭, ①が書いた PDF 頁, 正規表現, メモ)。まず①の頁で探し、無ければ資料全体で探して「頁が違う」と出す。
出力＝1行ごとに 判定（○＝①の頁で当たる／△＝別の頁で当たる／✕＝資料に無い）・PDF頁/印刷頁・前後の文（±CTX字）。
⚠️ 0件は「この綴りでは出ない」であって「無い」ではない＝✕は綴りを変えて当て直す（OCR の崩れ・改行のハイフン）。"""
import os, re, sys

SRC = r"C:\Users\konar\Desktop\zukai-engine\ref\ep24\src"
OFF = {"insag7_pub913e": -10, "ussr_report_part1": -4, "forum_legacy_2006": 2,
       "unscear2000_annexJ": 448, "unscear2008_annexD_corr": 40}
CTX = int(os.environ.get("CTX", "150"))

I7, GC, US, FO, J, D, G88 = ("insag7_pub913e", "gc_spl1_3_insag1text", "ussr_report_part1", "forum_legacy_2006",
                              "unscear2000_annexJ", "unscear2008_annexD_corr", "unscear1988_annexG")
CHECKS = [
    # --- 時刻 ---
    ("T01a", US, [19, 20], r"23[.:]?10|2310", "出力低下の再開 23:10（ソ連）"),
    ("T01b", I7, [61, 62, 63], r"23[.:]10", "23:10（付属書I 表I-I）"),
    ("T01c", GC, [9, 10, 26, 27, 28, 29, 30], r"23[.:]?00|23[.:]?10", "INSAG-1 本文は 23:00？"),
    ("T02a", US, [20, 21], r"0?0[.:]28|0028", "00:28 の出力の急落（ソ連）"),
    ("T02b", I7, [19, 20, 21], r"0?0[.:]28", "00:28（INSAG-7 本文）"),
    ("T03a", US, [20, 21], r"0?1[.:]00\b|200 MW", "01:00 に 200MW で安定（ソ連）"),
    ("T03b", I7, [117, 118, 119, 120, 121, 122, 123, 124], r"0?1[.:]03", "01:03（付属書II の運転日誌）"),
    ("T04", I7, [64, 65], r"0?1[.:]23[.:]0?4\b", "試験開始 01:23:04（付属書I）"),
    ("T05a", I7, [64, 65], r"0?1[.:]23[.:]40", "AZ-5 01:23:40（付属書I）"),
    ("T05b", I7, [64, 65, 66], r"0?1[.:]23[.:]39", "テレタイプ 01:23:39（付属書I）"),
    ("T06", I7, [64, 65], r"0?1[.:]23[.:]43", "01:23:43 出力の非常信号"),
    ("T07a", US, [24, 25, 26], r"0?1[.:]24|two explosions|explosions", "1:24ごろ 2回（ソ連・外の目撃）"),
    ("T07b", GC, [10, 30, 31, 32, 33], r"0?1[.:]24|two explosions", "1:24ごろ（INSAG-1）"),
    ("T08", GC, [40, 41, 42, 43, 44, 45], r"0?1[.:]23[.:]44", "01:23:44＝表I の計算上の100倍の行"),
    ("T09a", I7, [19, 20, 21, 22], r"0?0[.:]43[.:]27|0?0[.:]43", "タービン停止の信号の遮断 00:43:27（INSAG-7）"),
    ("T09b", I7, [62, 63, 64], r"0?0[.:]43[.:]37", "00:43:37（付属書I 表I-I？）"),
    ("T09c", GC, [9, 10, 26, 27, 28, 29, 30], r"turbine|trip", "INSAG-1 は 01:23:04 に遮断・「炉を救ったはず」"),
    ("T10", I7, [62, 63], r"14[.:]00", "14:00 ECCS 切り離し・キエフの給電指令"),
    ("T11", I7, [62, 63], r"0?1[.:]06", "25日 01:06 出力低下の開始（付属書I）"),
    # --- ORM ---
    ("O01", I7, [89, 90], r"15 (?:manual )?(?:control )?rods|fifteen", "ORM 15本で即時停止（付属書I 1-4.8）"),
    ("O02", I7, [89, 90], r"26|30 (?:rods|RR)", "定常 26〜30本（付属書I 1-4.8）"),
    ("O03", US, [23, 24], r"6[-–]8|six to eight", "事故の時 6〜8本（ソ連）"),
    ("O04", I7, [64], r"\b8 (?:rods|manual)|eight", "8本（付属書I 表I-I）"),
    ("O05", I7, [123], r"1\.9", "1.9本（付属書II）"),
    ("O06", US, [21, 22], r"print", "印字で知った（ソ連）"),
    ("O07", I7, [21], r"did not know", "運転員は値を知らなかった可能性（INSAG-7 3(5)）"),
    # --- ECCS ---
    ("E01", I7, [20], r"emergency core cooling|ECCS|chief engineer", "技師長の承認で許容（INSAG-7）"),
    ("E02", I7, [82, 83], r"2\.10\.5", "運転手順書2.10.5節の違反（付属書I）"),
    # --- 00:28 の評価 ---
    ("Z01", I7, [20, 21], r"0?0[.:]28.{0,400}", "00:28 は運転員の誤りといえない（INSAG-7）"),
    ("Z02", I7, [70, 71, 72, 73, 74, 75, 76, 77], r"could not (?:be )?(?:control|maintain)|failed to", "付属書I＝制御できなかった"),
    # --- 夜の2人・31人・30人 ---
    ("D01", US, [43], r"died|not found|burns", "1人は 6時にやけど・1人は見つからない（ソ連）"),
    ("D02", GC, [6, 118], r"\b31\b", "31人（INSAG-1）"),
    ("D03", GC, list(range(100, 125)), r"\b29\b", "急性放射線症29人（INSAG-1）"),
    ("D04", FO, [12], r"coronary|thrombosis|\b28\b", "28＋2＋1（フォーラム）"),
    ("D05", J, [5], r"\b30\b|thirty", "30人（UNSCEAR 2000 第2段落）"),
    ("D06", D, [7, 18], r"\b28\b|two|\b30\b", "2＋28（UNSCEAR 2008 第2・49段落）"),
    ("D07", J, [40], r"134|\b28\b", "ARS 134人・28人（UNSCEAR 2000 第186・191段落）"),
    ("D08", G88, list(range(70, 90)), r"burns|was not found|never found|missing", "直後の2人（UNSCEAR 1988 Annex G 付録）"),
    # --- 避難 ---
    ("V01", J, [24], r"49[, ]?360|1[, ]?200 buses|Yanov|254", "プリピャチ 4万9,360人・バス約1,200台・ヤノフ254"),
    ("V02", J, [5, 67], r"116[, ]?000|115[, ]?000", "1986年 約11万6,000人"),
    ("V03", J, [25, 26], r"28 April", "第105段落だけ 28 April"),
    ("V04", FO, [9, 10, 11], r"116[, ]?000|115[, ]?000|350[, ]?000|220[, ]?000", "フォーラムの避難の数"),
    # --- ポジティブ・スクラム ---
    ("P01", I7, [53, 54, 55], r"1983", "1983年11〜12月 イグナリナ1号機とチェルノブイリ4号機の物理起動（付属書I 1-3.8）"),
    ("P02", I7, [25], r"forgotten", "apparently the matter was forgotten（INSAG-7 4.2）"),
    ("P03", I7, [23], r"1987|Vienna", "ソ連が公に認めたのは1987年のウィーン（INSAG-7 4.1）"),
    ("P04", I7, [14, 15], r"1\.25|displacer|graphite", "棒の先の黒鉛・1.25m の水（INSAG-7 2.2）"),
    # --- INSAG-7 の結論 ---
    ("C01", I7, [33], r"shift the emphasis", "6(2)"),
    ("C02", I7, [34], r"in fact not violations", "6(6)"),
    ("C03", I7, [34], r"ill judged|on the spot", "なお運転員の判断の誤り"),
    ("C04", I7, [34, 35], r"retract", "6(7) INSAG-1 を撤回しない"),
    ("C05", I7, [33], r"decisive contributory|not known for certain", "6(4)"),
    ("C06", I7, [24, 25, 26, 27], r"decisive contributory|most likely", "4.1・5.1"),
    # --- INSAG-1 ---
    ("I01", GC, [112], r"human element", "根本原因は人的要素（結論）"),
    ("I02", GC, [18], r"remarkable range", "要約"),
    ("I03", GC, [9, 10], r"deliberately", "故意に棒を抜いた"),
    ("I04", GC, [10], r"100 times", "4秒で定格の100倍"),
    ("I05", GC, list(range(1, 148)), r"700 ?MW", "700MW 未満の運転（禁止と書いたか）"),
    ("I06", GC, list(range(1, 148)), r"nuclear explosion", "核爆発の語（0件のはず）"),
    ("I07", GC, [110], r"plausible", "ソ連の説明は「まったくもっともらしい」"),
    # --- ソ連報告 ---
    ("U01", US, [27], r"improbable combination", "主因＝ありそうにない違反の組合せ"),
    ("U02", US, [26, 27], r"violation", "第4章 違反の表"),
    ("U03", US, [19], r"requisite approval|approv", "試験計画に必要な承認が無い"),
    # --- 付属書I ---
    ("A01", I7, [41], r"not included in the papers", "IAEA に出した資料に入っていなかった"),
    ("A02", I7, [70], r"reduced exclusively|exclusively to personnel", "6月の会議で職員の誤りだけに"),
    ("A03", I7, [70], r"Volkov|1 May", "5月1日 クルチャトフ研のヴォルコフ"),
    ("A04", I7, [61, 62], r"nothing wrong with the programme", "試験計画そのものは悪くない"),
    ("A05", I7, [93, 76], r"EPS-5|trigger", "引き金は EPS-5"),
    ("A06", I7, [77], r"tens of times|several tens", "初期の数十倍"),
    ("A07", I7, [41], r"better or worse|no worse", "ほかの発電所より良くも悪くもない"),
    ("A08", I7, [63], r"Kiev|grid|dispatcher|controller", "延期はキエフの給電指令"),
    # --- 核爆発の語（INSAG-7・ソ連・UNSCEAR 2000）---
    ("N01", I7, list(range(1, 149)), r"nuclear explosion", "0件のはず"),
    ("N02", US, list(range(1, 61)), r"nuclear explosion", "0件のはず"),
    ("N03", I7, list(range(1, 149)), r"700 ?MW", "INSAG-7 の 700MW（禁止は無かった）"),
]


def load(base):
    rows = {}
    for line in open(os.path.join(SRC, base + ".pages.tsv"), encoding="utf-8"):
        p, _n, t = line.rstrip("\n").split("\t", 2)
        rows[int(p)] = t
    return rows


def pr(base, p, text):
    if base in OFF:
        return str(p + OFF[base])
    m = re.match(r"\s*-\s*([0-9IlO.·\s]{1,8}?)\s*-", text)  # スキャンの頁頭「- 105 -」
    return "~" + re.sub(r"\s", "", m.group(1)) if m else "?"


def snip(text, m):
    a, b = max(0, m.start() - CTX), min(len(text), m.end() + CTX)
    return text[a:b]


def main():
    only = set(sys.argv[1:])
    cache = {}
    for cid, base, pages, pat, memo in CHECKS:
        if only and cid not in only:
            continue
        rows = cache.setdefault(base, load(base))
        rx = re.compile(pat, re.I | re.S)
        hits = [(p, m) for p in pages if p in rows for m in [rx.search(rows[p])] if m]
        mark = "○"
        if not hits:
            hits = [(p, m) for p in sorted(rows) for m in [rx.search(rows[p])] if m]
            mark = "△" if hits else "✕"
        n_all = sum(len(rx.findall(rows[p])) for p in rows)
        print(f"\n[{cid}] {mark} {memo} ／ {base} ／ ①の頁 {pages[:6]}{'…' if len(pages) > 6 else ''} ／ 資料全体で {n_all}件")
        for p, m in hits[:3]:
            print(f"   p.{p}/{pr(base, p, rows[p])}: …{snip(rows[p], m)}…")


if __name__ == "__main__":
    main()
