# -*- coding: utf-8 -*-
"""25本目②：落とす前に大きさを確かめる（HEAD だけ・本体は取らない）。
①の scratchpad に残っている写しは、サーバの申告（Content-Length・Last-Modified）と大きさ・PDF の終わりの印（%%EOF）を並べる。
使い方: python head25.py <出力tsv>"""
import os, sys, time, urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) zukai-engine research"
OLD = r"C:\Users\konar\AppData\Local\Temp\claude\C--Users-konar-Documents-Obsidian-Vault\2bbd946c-93e3-4634-945f-c342938f4c8c\scratchpad"
J = "https://jtsb.mlit.go.jp"
W = "https://www.westjr.co.jp"

# 記号, URL, ①の写し（OLD からの相対・無ければ ""）
ITEMS = [
    ("R0", f"{J}/railway/rep-acci/RA2007-3-1.pdf", r"ep25A\dl\RA2007-3-1\RA2007-3-1.pdf"),
    *[(f"R{i}", f"{J}/railway/fukuchiyama/RA07-3-1-{i}.pdf", rf"ep25A\dl\RA07-3-1-{i}\RA07-3-1-{i}.pdf") for i in range(1, 8)],
    ("K05", f"{J}/railway/kyukengi/170906k.pdf", r"ep25A\dl\170906k\170906k.pdf"),
    ("K07", f"{J}/railway/kyukengi/190628k.pdf", r"ep25A\dl\190628k\190628k.pdf"),
    ("P1", f"{J}/railway/rep-acci/keika2.pdf", r"ep25A\dl\keika2\keika2.pdf"),
    ("S1", f"{J}/fukuchiyama/kensyou/fu04-finalreport.pdf", r"ep25B\dl\kensyou_final\fu04-finalreport.pdf"),
    ("S1k", f"{J}/fukuchiyama/kensyou/fu04-finalreport-annex-2-2.pdf", ""),
    ("T1", f"{J}/bunseki-kankoubutu/jtsbannualreport/annualreport_2010/annualreport2010_pdf/annual2010-fukuchiyama.pdf", r"ep25B\dl\jtsb_annual2010_fuku\annual2010-fukuchiyama.pdf"),
    ("KS", f"{J}/kaisetsu/fukuchiyamaline.html", ""),
    *[(f"I{n:02d}", f"{J}/ikenrail/shiryou/20070201-{s}.pdf", "") for n, s in enumerate(
        ["an01-honbun", "an02-huzu1", "an03-huzu2", "an04-huzu3", "an05-yougosyu", "giji01-gaiyou",
         "giji02-gaiyousetumei-koujyutu1-3", "giji03-koujyutu4", "giji04-koujyutu5-7", "giji05-koujyutu8-10",
         "giji06-koujyutu11-13"], 1)],
    ("S2", "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-86834.pdf", r"ep25B\dl\courts_pdf_86834\hanrei-pdf-86834.pdf"),
    ("S3", "https://www.courts.go.jp/assets/hanrei/hanrei-pdf-82178.pdf", r"ep25B\dl\courts_pdf_82178\hanrei-pdf-82178.pdf"),
    ("M1", "https://www.mlit.go.jp/kisha/kisha06/08/080324_.html", r"ep25B\dl\mlit_kisha_060324\080324_.html"),
    ("M1p", "https://www.mlit.go.jp/pubcom/06/kekka/pubcomk5_.html", r"ep25B\dl\mlit_pubcom_kekka\pubcomk5_.html"),
    ("M1q", "https://www.mlit.go.jp/pubcom/06/pubcom5/01.pdf", r"ep25B\dl\mlit_pubcom5_01\01.pdf"),
    ("M2", "https://www.mlit.go.jp/fukuchiyama/index.html", r"ep25B\dl\mlit_fukuchiyama\index.html"),
    ("F1", "https://www.fdma.go.jp/disaster/info/assets/post364.pdf", r"ep25B\dl\fdma_post364\post364.pdf"),
    ("C1", "https://www.bousai.go.jp/updates/pdf/fukuchiyama_07.pdf", r"ep25B\dl\bousai_fuku07\fukuchiyama_07.pdf"),
    ("J1", f"{W}/fukuchiyama/outline/", r"ep25B\dl\jrw_outline\index.html"),
    ("J2", f"{W}/fukuchiyama/inorinomori/", r"ep25B\dl\jrw_inori\index.html"),
    ("J2p", f"{W}/fukuchiyama/inorinomori/pdf/j_inorinomori.pdf", r"ep25B\dl\jrw_inori_pdf\j_inorinomori.pdf"),
    ("J3", f"{W}/safety/fukuchiyama/plan_improvement/pdf/keikaku_00.pdf", r"ep25B\dl\jrw_keikaku00\keikaku_00.pdf"),
    ("J4", f"{W}/fukuchiyama/support/pdf/houkoku.pdf", r"ep25B\dl\jrw_houkoku_pdf\houkoku.pdf"),
    ("J5", f"{W}/safety/fukuchiyama/pdf/shourainiwataru.pdf", r"ep25B\dl\jrw_shourai\shourainiwataru.pdf"),
    ("HY", "https://web.pref.hyogo.lg.jp/kk37/pa18_000000002.html", ""),
]


def head(url):
    for method, extra in (("HEAD", {}), ("GET", {"Range": "bytes=0-0"})):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, **extra})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                h = r.headers
                n = h.get("Content-Length", "")
                if method == "GET":  # Content-Range: bytes 0-0/12345
                    cr = h.get("Content-Range", "")
                    n = cr.rsplit("/", 1)[-1] if "/" in cr else "?"
                return str(r.status), method, n, h.get("Last-Modified", ""), h.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue
            return str(e.code), method, "", "", ""
        except Exception as e:
            return type(e).__name__, method, "", "", ""
    return "ERR", "", "", "", ""


def local(rel):
    if not rel:
        return "", ""
    p = os.path.join(OLD, rel)
    if not os.path.exists(p):
        return "missing", ""
    n = os.path.getsize(p)
    eof = ""
    if p.lower().endswith(".pdf"):
        with open(p, "rb") as f:
            f.seek(max(0, n - 2048))
            eof = "EOF" if b"%%EOF" in f.read() else "noEOF"
    return str(n), eof


def main():
    out = sys.argv[1]
    rows = ["key\thttp\tmethod\tserver_bytes\tlast_modified\tctype\tlocal_bytes\tlocal_eof\tsame\turl"]
    for key, url, rel in ITEMS:
        st, m, n, lm, ct = head(url)
        lb, eof = local(rel)
        same = "" if not lb else ("=" if lb == n else "DIFF")
        rows.append("\t".join([key, st, m, n, lm, ct, lb, eof, same, url]))
        print(key, st, n, lb, same, flush=True)
        time.sleep(1.5)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")
    print("done", len(ITEMS))


if __name__ == "__main__":
    main()
