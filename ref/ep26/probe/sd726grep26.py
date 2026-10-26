# 26本目 ②：米国上院の公聴会 S. Doc. 726（公式の印刷・1,170頁）で、書き起こしから取った決め所の句を頁ごとに探す
# 句も本文も「英小文字と数字だけ」に揃えて当てる（OCR の句読点・記号の崩れに強くする）。メモリを抑えるため1頁ずつ読む
# 使い方: python -P ref/ep26/probe/sd726grep26.py <pdf> <出力.tsv>
import re, sys

import fitz

PHRASES = [
    ("Lord", "ship's time for 47"), ("Lord", "an hour and fifty minutes time between New York"),
    ("Lord", "south 16 west, sir, was the course"), ("Lord", "Nineteen and one-half to twenty miles"),
    ("Lord", "This is not the Titanic; there is no doubt about it"), ("Lord", "an ordinary cargo steamer"),
    ("Lord", "I think she has fired a rocket"), ("Lord", "went to sleep"),
    ("Lord", "The officer on watch saw some signals, but he said they were not distress signals"),
    ("Lord", "Nineteen and a half miles is a long ways"), ("Lord", "the Virginian as the position where she struck an iceberg"),
    ("Evans", "we are stopped and surrounded by ice"), ("Evans", "Shut up, shut up, I am busy; I am working Cape Race"),
    ("Evans", "I put the phones down and took off my clothes and turned in"), ("Evans", "New York time I called him up"),
    ("Evans", "I was answered by the Frankfurt"), ("Evans", "There is a ship that has been firing rockets in the night"),
    ("Donkeyman", "the lights of a very large steamer about 10 miles away"), ("Donkeyman", "I saw a white rocket about 10 miles away"),
    ("Donkeyman", "It was no tramp"), ("Donkeyman", "At four minutes after 12"), ("Donkeyman", "pale blue, or white"),
    ("Rostron", "that was our apparent time"), ("Rostron", "The New York time at 12"), ("Rostron", "north 52 degrees west true 58 miles"),
    ("Rostron", "I saw a flare, about half a point on the port bow"), ("Rostron", "company's rockets to be fired"),
    ("Rostron", "I got the first boat alongside"), ("Rostron", "the Leyland Line steamer Californian hove up"),
    ("Boxhall", "it was 10.13 Washington time"), ("Boxhall", "I considered she was about 5 miles away"),
    ("Boxhall", "Just white stars, bright"), ("Boxhall", "I do not think we could see them 14 miles"),
    ("Rowe", "five and twenty minutes after"), ("Rowe", "I judged it to be a stern light"),
    ("Bride", "one was keeping New York time and the other was keeping ship's time"),
    ("Cottam", "About 11.20, sir, New York time"), ("Lightoller", "Two points on the port bow"),
]


def norm(s):
    s = s.lower().replace("-\n", "").replace("­", "")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", s)).strip()


def main():
    pdf, out = sys.argv[1], sys.argv[2]
    doc = fitz.open(pdf)
    keys = [(w, p, norm(p)) for w, p in PHRASES]
    hits = {p: [] for _, p, _ in keys}
    prev = ""
    for i in range(doc.page_count):
        t = norm(doc[i].get_text("text"))
        both = prev[-300:] + " " + t  # 頁をまたぐ句も拾う
        for w, p, n in keys:
            if n in both and n not in prev:
                hits[p].append(i + 1)
        prev = t
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("who\tphrase\tpdf_pages\n")
        for w, p, _ in keys:
            f.write(f"{w}\t{p}\t{','.join(map(str, hits[p])) or 'NOT FOUND'}\n")
    print("pages", doc.page_count, "found", sum(1 for v in hits.values() if v), "/", len(hits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
