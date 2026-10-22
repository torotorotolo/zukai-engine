# -*- coding: utf-8 -*-
"""24本目②：一次資料を ref/ep24/src/ へ取り直す（src/ は git の外）。http・大きさ・md5 を fetch_log.tsv に残す。
①の PDF は別セッションの scratchpad にあり消えている＝照合の相手は無い（md5 は今回の値を正本にする）。
使い方: python fetch_src.py            # 全部（取れているものは飛ばす）
        python fetch_src.py --force    # 取り直す"""
import hashlib, os, sys, time, urllib.request, urllib.error

DST = r"C:\Users\konar\Desktop\zukai-engine\ref\ep24\src"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) zukai-engine research"
IAEA = "https://www.iaea.org/sites/default/files"
UN = "https://www.unscear.org/unscear/uploads/documents"

ITEMS = [
    # 記号, 保存名, URL
    ("S1", "insag7_pub913e.pdf", "https://www-pub.iaea.org/MTCD/Publications/PDF/Pub913e_web.pdf"),
    ("S2", "gc_spl1_3_insag1text.pdf", f"{IAEA}/gc/gc-spl1-3.pdf"),
    ("S3", "ussr_report_part1.pdf", f"{IAEA}/gc/gc29inf-232-corr1_en.pdf"),
    ("L1", "forum_legacy_2006.pdf", f"{IAEA}/chernobyl.pdf"),
    ("L2", "unscear2000_annexJ.pdf", f"{UN}/publications/UNSCEAR_2000_Annex-J.pdf"),
    ("L3", "unscear2008_annexD_corr.pdf", f"{UN}/publications/UNSCEAR_2008_Annex-D-CORR.pdf"),
    ("L4", "unscear_wp2018_thyroid.pdf", f"{UN}/publications/Chernobyl_WP_2017.pdf"),
    ("L5", "unscear1988_report.pdf", f"{UN}/unscear-reports/UNSCEAR_1988_Report.pdf"),
    ("L6", "unscear1988_annexD.pdf", f"{UN}/publications/UNSCEAR_1988_Annex-D.pdf"),
    ("L7", "unscear1988_annexG.pdf", f"{UN}/publications/UNSCEAR_1988_Annex-G.pdf"),
    ("L8", "iarc2006_briefing.pdf", "https://www.iarc.who.int/wp-content/uploads/2018/07/IARCBriefingChernobyl.pdf"),
    ("L9", "who2005_true_scale.html", "https://www.who.int/news/item/05-09-2005-chernobyl-the-true-scale-of-the-accident"),
    ("L10", "ines_manual2008.pdf", "https://www-pub.iaea.org/MTCD/Publications/PDF/INES2013web.pdf"),
    ("L11", "who2006_health_effects.pdf", "https://iris.who.int/bitstream/handle/10665/43447/9241594179_eng.pdf"),
]


def md5(b):
    return hashlib.md5(b).hexdigest()


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read()


def main():
    force = "--force" in sys.argv
    os.makedirs(DST, exist_ok=True)
    log = os.path.join(DST, "fetch_log.tsv")
    rows = []
    for key, name, url in ITEMS:
        path = os.path.join(DST, name)
        if os.path.exists(path) and os.path.getsize(path) > 0 and not force:
            b = open(path, "rb").read()
            rows.append((key, name, "skip", "", str(len(b)), md5(b), url))
            continue
        status, ctype, b = "ERR", "", b""
        for i in range(3):
            try:
                status, ctype, b = get(url)
                break
            except urllib.error.HTTPError as e:
                status = e.code
                break
            except Exception as e:  # 一時的な失敗は間を空けて再試行
                status = type(e).__name__
                time.sleep(8 * (i + 1))
        if b:
            open(path, "wb").write(b)
        rows.append((key, name, str(status), ctype, str(len(b)), md5(b) if b else "", url))
        print(key, name, status, len(b), flush=True)
        time.sleep(2)
    with open(log, "a", encoding="utf-8") as f:
        f.write("# %s\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
        f.write("key\tfile\thttp\tcontent_type\tbytes\tmd5\turl\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    bad = [r for r in rows if r[2] not in ("200", "skip")]
    print("done", len(rows), "bad", len(bad))
    for r in bad:
        print("BAD", r)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
