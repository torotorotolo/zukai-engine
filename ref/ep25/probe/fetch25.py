# -*- coding: utf-8 -*-
"""25本目②：一次資料を ref/ep25/src/ にそろえる（src/ は git の外）。
- 「写す」＝①（10-24）の scratchpad に残っていた写し。10-25 の HEAD でサーバの大きさと全件一致（probe/head25.py）＝落とし直さない（10-25 カズヤくん了承「推奨どおり」）
- 「取る」＝①で未読だった5件（同じ了承）
大きさ・md5・出どころを src/fetch_log.tsv に残す。
使い方: python fetch25.py            # 全部（取れているものは飛ばす）
        python fetch25.py --force    # 取り直す"""
import hashlib, os, shutil, sys, time, urllib.request, urllib.error

DST = r"C:\Users\konar\Desktop\zukai-engine\ref\ep25\src"
OLD = r"C:\Users\konar\AppData\Local\Temp\claude\C--Users-konar-Documents-Obsidian-Vault\2bbd946c-93e3-4634-945f-c342938f4c8c\scratchpad"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) zukai-engine research"
J = "https://jtsb.mlit.go.jp"
W = "https://www.westjr.co.jp"
A = r"ep25A\dl"
B = r"ep25B\dl"

# 記号, 保存先（DST からの相対）, URL, ①の写し（OLD からの相対・"" なら取る）
ITEMS = [
    # 事故調（航空・鉄道事故調査委員会／運輸安全委員会）
    ("R0", r"jtsb\RA2007-3-1_cover.pdf", f"{J}/railway/rep-acci/RA2007-3-1.pdf", rf"{A}\RA2007-3-1\RA2007-3-1.pdf"),
    *[(f"R{i}", rf"jtsb\RA07-3-1-{i}.pdf", f"{J}/railway/fukuchiyama/RA07-3-1-{i}.pdf", rf"{A}\RA07-3-1-{i}\RA07-3-1-{i}.pdf") for i in range(1, 8)],
    ("K05", r"jtsb\kengi_170906k.pdf", f"{J}/railway/kyukengi/170906k.pdf", rf"{A}\170906k\170906k.pdf"),
    ("K07", r"jtsb\kengi_190628k.pdf", f"{J}/railway/kyukengi/190628k.pdf", rf"{A}\190628k\190628k.pdf"),
    ("P1", r"jtsb\keika2.pdf", f"{J}/railway/rep-acci/keika2.pdf", rf"{A}\keika2\keika2.pdf"),
    ("S1", r"jtsb\fu04-finalreport.pdf", f"{J}/fukuchiyama/kensyou/fu04-finalreport.pdf", rf"{B}\kensyou_final\fu04-finalreport.pdf"),
    ("S1k", r"jtsb\fu04-finalreport-annex-2-2.pdf", f"{J}/fukuchiyama/kensyou/fu04-finalreport-annex-2-2.pdf", ""),
    ("S1kh", r"jtsb\kaisetsu_fukuchiyamaline.html", f"{J}/kaisetsu/fukuchiyamaline.html", ""),
    ("T1", r"jtsb\annual2010-fukuchiyama.pdf", f"{J}/bunseki-kankoubutu/jtsbannualreport/annualreport_2010/annualreport2010_pdf/annual2010-fukuchiyama.pdf", rf"{B}\jtsb_annual2010_fuku\annual2010-fukuchiyama.pdf"),
    ("I01", r"jtsb\iken20070201-an01-honbun.pdf", f"{J}/ikenrail/shiryou/20070201-an01-honbun.pdf", ""),
    ("I06", r"jtsb\iken20070201-giji01-gaiyou.pdf", f"{J}/ikenrail/shiryou/20070201-giji01-gaiyou.pdf", ""),
    ("RT1", r"rights\jtsb_cyo.html", f"{J}/cyo.html", r"ep25A\work\cyo.html"),
    ("RT2", r"rights\pdl1.0.html", "https://www.digital.go.jp/resources/open_data/public_data_license_v1.0", r"ep25A\work\pdl.html"),
    # 裁判所
    ("S2", r"courts\hanrei-pdf-86834.pdf", "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-86834.pdf", rf"{B}\courts_pdf_86834\hanrei-pdf-86834.pdf"),
    ("S2h", r"courts\hanrei_86834_detail2.html", "https://www.courts.go.jp/hanrei/86834/detail2/index.html", rf"{B}\courts_86834\index.html"),
    ("S3", r"courts\hanrei-pdf-82178.pdf", "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-82178.pdf", rf"{B}\courts_pdf_82178\hanrei-pdf-82178.pdf"),
    ("S3h", r"courts\hanrei_82178_detail4.html", "https://www.courts.go.jp/hanrei/82178/detail4/index.html", rf"{B}\courts_82178\index.html"),
    # 国・自治体
    ("M1", r"gov\mlit_kisha_080324_.html", "https://www.mlit.go.jp/kisha/kisha06/08/080324_.html", rf"{B}\mlit_kisha_060324\080324_.html"),
    ("M1p", r"gov\mlit_pubcomk5_.html", "https://www.mlit.go.jp/pubcom/06/kekka/pubcomk5_.html", rf"{B}\mlit_pubcom_kekka\pubcomk5_.html"),
    ("M1q", r"gov\mlit_pubcom5_01.pdf", "https://www.mlit.go.jp/pubcom/06/pubcom5/01.pdf", rf"{B}\mlit_pubcom5_01\01.pdf"),
    ("M2", r"gov\mlit_fukuchiyama_index.html", "https://www.mlit.go.jp/fukuchiyama/index.html", rf"{B}\mlit_fukuchiyama\index.html"),
    ("M3", r"gov\mlit_hakusho_h18_H1012210.html", "https://www.mlit.go.jp/hakusyo/mlit/h17/hakusho/h18/html/H1012210.html", rf"{B}\mlit_hakusho_h18\H1012210.html"),
    ("M4", r"gov\cao_koutu_h29_h1b2s2_1.html", "https://www8.cao.go.jp/koutu/taisaku/h29kou_haku/zenbun/genkyo/h1/h1b2s2_1.html", rf"{B}\cao_hakusho_h29\h1b2s2_1.html"),
    ("F1", r"gov\fdma_post364.pdf", "https://www.fdma.go.jp/disaster/info/assets/post364.pdf", rf"{B}\fdma_post364\post364.pdf"),
    ("F2", r"gov\fdma_170523_1.pdf", "https://www.fdma.go.jp/singi_kento/singi/items/170523_pdf/1.pdf", rf"{B}\fdma_170523\1.pdf"),
    ("C1", r"gov\bousai_fukuchiyama_07.pdf", "https://www.bousai.go.jp/updates/pdf/fukuchiyama_07.pdf", rf"{B}\bousai_fuku07\fukuchiyama_07.pdf"),
    ("C2", r"gov\bousai_hakusho_h17_hm120503.htm", "https://www.bousai.go.jp/kaigirep/hakusho/h17/bousai2005/html/honmon/hm120503.htm", rf"{B}\bousai_hakusho_h17\hm120503.htm"),
    ("C3", r"gov\bousai_hakusho_h18_hm01020503.htm", "https://www.bousai.go.jp/kaigirep/hakusho/h18/bousai2006/html/honmon/hm01020503.htm", rf"{B}\bousai_hakusho_h18\hm01020503.htm"),
    ("HY1", r"gov\hyogo_kensho_000007823.pdf", "https://web.pref.hyogo.lg.jp/kk37/documents/000007823.pdf", ""),
    ("HY2", r"gov\hyogo_kensho_gaiyou_000007665.pdf", "https://web.pref.hyogo.lg.jp/kk37/documents/000007665.pdf", ""),
    # JR西日本
    ("J0", r"jrw\fukuchiyama_top.html", f"{W}/fukuchiyama/", rf"{B}\jrw_fukutop\index.html"),
    ("J1", r"jrw\outline.html", f"{W}/fukuchiyama/outline/", rf"{B}\jrw_outline\index.html"),
    ("J2", r"jrw\inorinomori.html", f"{W}/fukuchiyama/inorinomori/", rf"{B}\jrw_inori\index.html"),
    ("J2p", r"jrw\j_inorinomori.pdf", f"{W}/fukuchiyama/inorinomori/pdf/j_inorinomori.pdf", rf"{B}\jrw_inori_pdf\j_inorinomori.pdf"),
    ("J3", r"jrw\keikaku_00.pdf", f"{W}/safety/fukuchiyama/plan_improvement/pdf/keikaku_00.pdf", rf"{B}\jrw_keikaku00\keikaku_00.pdf"),
    ("J3h", r"jrw\plan_improvement.html", f"{W}/safety/fukuchiyama/plan_improvement/", rf"{B}\jrw_plan_impr\index.html"),
    ("J4", r"jrw\support_houkoku.pdf", f"{W}/fukuchiyama/support/pdf/houkoku.pdf", rf"{B}\jrw_houkoku_pdf\houkoku.pdf"),
    ("J4a", r"jrw\support_01.html", f"{W}/fukuchiyama/support/01.html", rf"{B}\jrw_support01\01.html"),
    ("J4b", r"jrw\support_02.html", f"{W}/fukuchiyama/support/02.html", rf"{B}\jrw_support02\02.html"),
    ("J4c", r"jrw\action.html", f"{W}/fukuchiyama/action/", rf"{B}\jrw_action\index.html"),
    ("J5", r"jrw\shourainiwataru.pdf", f"{W}/safety/fukuchiyama/pdf/shourainiwataru.pdf", rf"{B}\jrw_shourai\shourainiwataru.pdf"),
    ("J6", r"jrw\report_railroad.html", f"{W}/safety/report_railroad/", rf"{B}\jrw_report_rr\index.html"),
    ("J6a", r"jrw\report_railroad_houkoku_01.pdf", f"{W}/safety/report_railroad/pdf/houkoku_01.pdf", rf"{B}\jrw_rr_houkoku01\houkoku_01.pdf"),
    ("J6b", r"jrw\report_railroad_houkoku_02.pdf", f"{W}/safety/report_railroad/pdf/houkoku_02.pdf", rf"{B}\jrw_rr_houkoku02\houkoku_02.pdf"),
    ("J7", r"jrw\safety_top.html", f"{W}/safety/", rf"{B}\jrw_safety\index.html"),
]
# 国会会議録の JSON（①の B が kokkai.ndl.go.jp/api/speech で引いたもの・条件は scripts/kokkai.py）
for q in ["all_after", "ats", "early", "nikkin", "amagasaki", "leak", "leak2", "leak3", "court", "soken"]:
    d = os.path.join(OLD, B, f"kokkai_{q}")
    if os.path.isdir(d):
        for fn in sorted(os.listdir(d)):
            ITEMS.append((f"K_{q}_{fn[:-5]}", rf"kokkai\kokkai_{q}_{fn}", "https://kokkai.ndl.go.jp/api/speech（条件は src/_ep25_1_scripts/B/kokkai.py）", rf"{B}\kokkai_{q}\{fn}"))


def md5(b):
    return hashlib.md5(b).hexdigest()


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        return r.status, r.headers.get("Content-Length", ""), r.read()


def main():
    force = "--force" in sys.argv
    rows = []
    for key, rel, url, old in ITEMS:
        path = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if os.path.exists(path) and os.path.getsize(path) > 0 and not force:
            b = open(path, "rb").read()
            rows.append((key, rel, "skip", "", str(len(b)), md5(b), url))
            continue
        if old:
            src = os.path.join(OLD, old)
            if not os.path.exists(src):
                rows.append((key, rel, "MISSING_OLD", "", "", "", url))
                continue
            shutil.copy2(src, path)
            b = open(path, "rb").read()
            rows.append((key, rel, "copied(①10-24)", "", str(len(b)), md5(b), url))
            continue
        status, clen, b = "ERR", "", b""
        for i in range(3):
            try:
                status, clen, b = get(url)
                break
            except urllib.error.HTTPError as e:
                status = e.code
                break
            except Exception as e:  # 一時的な失敗は間を空けて再試行
                status = type(e).__name__
                time.sleep(8 * (i + 1))
        if b:
            open(path, "wb").write(b)
        ok = (str(status) == "200") and (not clen or clen == str(len(b)))
        rows.append((key, rel, str(status) if ok else f"{status}/len{clen}", clen, str(len(b)), md5(b) if b else "", url))
        print(key, rel, status, len(b), flush=True)
        time.sleep(2)
    # ①の道具（国会の条件などの記録）も写す
    for side in ("A", "B"):
        s = os.path.join(OLD, f"ep25{side}", "scripts")
        d = os.path.join(DST, "_ep25_1_scripts", side)
        if os.path.isdir(s) and not os.path.isdir(d):
            shutil.copytree(s, d)
    log = os.path.join(DST, "fetch_log.tsv")
    with open(log, "a", encoding="utf-8") as f:
        f.write("# %s\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
        f.write("key\tfile\thow\tcontent_length\tbytes\tmd5\turl\n")
        for r in rows:
            f.write("\t".join(r) + "\n")
    bad = [r for r in rows if not (r[2] in ("200", "skip") or r[2].startswith("copied"))]
    print("done", len(rows), "bad", len(bad))
    for r in bad:
        print("BAD", r)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
