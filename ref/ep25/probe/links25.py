# -*- coding: utf-8 -*-
"""25本目②：頁を読んで（保存しない）PDF の行き先と大きさ（HEAD）を一覧にする。落とす前の了承の一覧づくり用。
使い方: python links25.py <URL> [<URL> ...]"""
import html, re, sys, time, urllib.parse, urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) zukai-engine research"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        b = r.read()
        cs = r.headers.get_content_charset() or "utf-8"
    for enc in (cs, "utf-8", "cp932", "euc-jp"):
        try:
            return b.decode(enc)
        except Exception:
            continue
    return b.decode("utf-8", "replace")


def size(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.headers.get("Content-Length", "?")
    except urllib.error.HTTPError as e:
        return f"http{e.code}"
    except Exception as e:
        return type(e).__name__


def main():
    for page in sys.argv[1:]:
        print("=== PAGE", page)
        t = fetch(page)
        title = re.search(r"<title>(.*?)</title>", t, re.S | re.I)
        print("title:", html.unescape(title.group(1)).strip() if title else "")
        for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', t, re.S | re.I):
            href, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
            txt = re.sub(r"\s+", " ", html.unescape(txt)).strip()
            if href.lower().endswith(".pdf"):
                u = urllib.parse.urljoin(page, href)
                print(f"PDF\t{size(u)}\t{txt[:80]}\t{u}", flush=True)
                time.sleep(1.0)


if __name__ == "__main__":
    main()
