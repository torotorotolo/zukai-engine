# -*- coding: utf-8 -*-
"""SL-1 の一次資料 PDF を「原文照合できる形」で扱う道具（抜き出し・検索・切り出し）。

🔴 なぜ要るか（2026-09-07・④台本で判明）
   引き継ぎには「189/208ページに文字層があるので**原文照合にそのまま使える**」と書いてあったが、
   **そのままは使えない。** 文字層は1962年の走査を OCR したもので、次の3つが起きる。
     ① 文字間に空白が入る（`S t a t i o n`）
     ② 字が化ける（AEC→`AM:` / Sr90→`SrgO` / 1/8 inch→`118 inch` / 10^10→`1O1O`）
     ③ 語そのものが壊れる（`Decontarnination`）。⚠️ **目次がいちばんひどく、本文は良い**
   ＝ **素の grep は「在るのに0件」を返す。**
   → [[feedback-absence-of-a-word-is-not-absence]] / [[feedback-verify-your-own-instrument]]

⚠️ **この道具は「当たりを付ける」ためのもので、照合そのものではない。**
   画面に出す語は **crop で原寸を切り出して目で見る**まで確定させないこと。
   台本第1版では、決め所17件のうち **5件が、原寸で見なければ語を決められなかった**。

使い方（Windows。`PYTHONUTF8=1` を付ける）
    python tools/ido_text.py extract                     # 全部の PDF から文字を抜く
    python tools/ido_text.py extract --11
    python tools/ido_text.py find "control rod"          # ① 空白と記号を無視した連続一致
    python tools/ido_text.py find --fuzzy "Sr90"         # ② 紛らわしい字も畳む（数字が壊れるので語専用）
    python tools/ido_text.py find --near "rod withdrawn" # ③ 語がページ内に全部あるか（1語壊れても当たる）
    python tools/ido_text.py find --11 "positive proof"
    python tools/ido_text.py page --02 32                # そのPDFページの素の文字
    python tools/ido_text.py crop --11 19 "positive proof is lacking" --pad 170
    python tools/ido_text.py crop --02 112 --whole
    python tools/ido_text.py --selftest                  # 🔴 使う前にこれを通す

資料の記号: --02=IDO-19302 / --11=IDO-19311 / --13=IDO-19313 / --anl=ANL-6692 / --haer=HAER ID-33-D
🔴 **PDF はリポに入っていない**（合計92MB・`.gitignore`）。取り直しは `ref/CREDITS.md` ⑥ の表。
   全文テキスト（`ref/sl1/*_all.txt`）はリポに在るので、PDF が無くても find は動く。

終了コード: 0=正常／ヒット有り  1=0件／selftest 失敗  2=道具の異常
"""
import io
import re
import sys
from pathlib import Path

REF = Path(__file__).resolve().parent.parent / "ref" / "sl1"
CROPS = REF / "_crops"

# 記号 → (PDF名, 全文テキスト名, ページ単位フォルダ名)
DOCS = {
    "02":   ("IDO-19302", "ido_all.txt",        "ido_text"),
    "11":   ("IDO-19311", "IDO-19311_all.txt",  "ido19311_text"),
    "13":   ("IDO-19313", "IDO-19313_all.txt",  "ido19313_text"),
    "anl":  ("ANL-6692",  "ANL-6692_all.txt",   "anl6692_text"),
    "haer": ("HAER_ID-33-D", "HAER_ID-33-D_all.txt", "haer_text"),
}
PAGE_RE = re.compile(r"^===== PDF PAGE (\d+) =====$", re.M)

# ⚠️ 畳むのは **--fuzzy のときだけ**。数字が字に化けるので、数の照合には使えない。
FOLD = str.maketrans({"0": "o", "1": "l", "5": "s", "8": "b", "9": "g",
                      "I": "l", "|": "l", "!": "l", "£": "l", "3": "e"})


def norm(s, fuzzy=False):
    """空白・記号を落として小文字化する。fuzzy なら紛らわしい字も畳む。"""
    if fuzzy:
        s = s.translate(FOLD)      # 🔴 lower() より **先**（大文字 I を畳むため）
    return re.sub(r"[^a-z0-9]", "", s.lower())


# ─────────────────────────── 抜き出し ───────────────────────────

def extract(keys):
    import fitz
    for k in keys:
        name, allname, _ = DOCS[k]
        pdf = REF / (name + ".pdf")
        if not pdf.exists():
            print("⚠️ %s が無い（ref/CREDITS.md ⑥ の curl で取り直す）" % pdf.name)
            continue
        doc = fitz.open(pdf)
        buf = ["\n\n===== PDF PAGE %d =====\n%s" % (i + 1, p.get_text("text"))
               for i, p in enumerate(doc)]
        (REF / allname).write_text("".join(buf), encoding="utf-8")
        thin = sum(1 for b in buf if len(b.strip()) < 90)
        print("%s: %dページ / %d字 → %s（文字の薄いページ %d）"
              % (name, doc.page_count, sum(len(b) for b in buf), allname, thin))


# ─────────────────────────── 検索 ───────────────────────────

_CACHE = {}


def pages(key):
    """[(pdf_page, raw)] を全文テキストから復元する。PDF が無くても動く。"""
    if key in _CACHE:
        return _CACHE[key]
    name, allname, _ = DOCS[key]
    p = REF / allname
    if not p.exists():
        print("🔴 %s が無い。先に `python tools/ido_text.py extract --%s` を回す" % (allname, key))
        sys.exit(2)
    txt = p.read_text(encoding="utf-8")
    marks = [(m.start(), m.end(), int(m.group(1))) for m in PAGE_RE.finditer(txt)]
    out = []
    for i, (s, e, pg) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(txt)
        out.append((pg, txt[e:end]))
    _CACHE[key] = out
    return out


def _index(raw, fuzzy):
    s = (raw.translate(FOLD) if fuzzy else raw).lower()
    buf, idx = [], []
    for i, ch in enumerate(s):
        if ch.isascii() and (ch.isalpha() or ch.isdigit()):
            buf.append(ch)
            idx.append(i)
    return "".join(buf), idx


def find(key, needle, ctx=300, fuzzy=False):
    n = norm(needle, fuzzy)
    if not n:
        return []
    hits = []
    for pg, raw in pages(key):
        flat, idx = _index(raw, fuzzy)
        for m in re.finditer(re.escape(n), flat):
            a, b = idx[m.start()], idx[m.end() - 1] + 1
            hits.append((pg, raw[max(0, a - ctx):b + ctx].strip()))
    return hits


def find_near(key, words, window=400, ctx=300):
    """語がすべて同じページの window 文字以内に在るか。1語 OCR で壊れていても残りで当たる。"""
    ws = [norm(w) for w in words if norm(w)]
    hits = []
    for pg, raw in pages(key):
        flat, idx = _index(raw, False)
        pos = {w: [m.start() for m in re.finditer(re.escape(w), flat)] for w in ws}
        if not all(pos.values()):
            continue
        anchor = min(pos, key=lambda w: len(pos[w]))
        for a in pos[anchor]:
            if all(any(abs(q - a) <= window for q in pos[w]) for w in ws):
                lo = idx[max(0, a - 60)]
                hits.append((pg, raw[max(0, lo - ctx // 2):lo + ctx].strip()))
                break
    return hits


# ─────────────────────────── 切り出し ───────────────────────────

def crop(key, pg, words, pad=140, zoom=2.6, out=None, whole=False):
    """語で当たりを付けて、そのページの**一部だけ**を PNG にする（原寸を丸ごと読まない）。
    ⚠️ OCR で空白が割れるので `search_for` は当たらない。語の箱を並べて正規化した上で探す。"""
    import fitz
    name = DOCS[key][0]
    pdf = REF / (name + ".pdf")
    if not pdf.exists():
        print("🔴 %s が無い（切り出しには PDF が要る）。ref/CREDITS.md ⑥ の curl で取る" % pdf.name)
        sys.exit(2)
    CROPS.mkdir(parents=True, exist_ok=True)
    page = fitz.open(pdf)[pg - 1]
    r = page.rect
    if whole or not words:
        clip = r
    else:
        flat, spans = [], []
        for w in page.get_text("words"):        # (x0,y0,x1,y1,word,block,line,no)
            s = re.sub(r"[^a-z0-9]", "", w[4].lower())
            if not s:
                continue
            spans.append((len(flat), len(flat) + len(s), w))
            flat.extend(s)
        m = re.search(re.escape(norm(" ".join(words))), "".join(flat))
        if not m:
            print("🔴 その語はこのページの文字層に無い。--whole で全面を切るか、語を短くする")
            sys.exit(1)
        hs = [w for a, b, w in spans if a < m.end() and b > m.start()]
        clip = fitz.Rect(max(r.x0, min(h[0] for h in hs) - pad),
                         max(r.y0, min(h[1] for h in hs) - pad),
                         min(r.x1, max(h[2] for h in hs) + pad),
                         min(r.y1, max(h[3] for h in hs) + pad))
    dest = CROPS / (out or ("%s_p%03d.png" % (name, pg)))
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    pix.save(dest)
    print("%s  %dx%d  clip=%s" % (dest, pix.width, pix.height, [round(v) for v in clip]))


# ─────────────────────────── 検算 ───────────────────────────

def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %s %-34s 期待 %-8s 実際 %s" % ("OK " if good else "🔴NG", name, want, got))

    # ① 正規化そのもの
    chk("空白入りを畳む", norm("S t a t i o n"), "station")
    chk("素は数字を残す", norm("Sr90"), "sr90")
    chk("fuzzy は 9→g", norm("Sr90", True), "srgo")
    chk("fuzzy で SrgO と一致", norm("SrgO", True), norm("Sr90", True))
    chk("大文字 I を先に畳む", norm("I131", True), "llel")
    chk("I131 と Il3I が同じ形", norm("I131", True), norm("Il3I", True))

    # ② 実物に当てる（全文テキストが在るものだけ）
    have = [k for k in DOCS if (REF / DOCS[k][1]).exists()]
    if "02" not in have:
        print("  ⚠️ ido_all.txt が無いので実物の検算を飛ばす（extract を先に回す）")
        print("selftest:", "PASS" if ok else "🔴FAIL")
        return ok
    ps = pages("02")
    chk("IDO-19302 のページ数", len(ps), 208)
    chk("空白入り語を拾う", len(find("02", "National Reactor Testing Station")) >= 1, True)
    chk("数を素で拾う", len(find("02", "January 3, 1961")) >= 1, True)
    # 🔴 陰性対照＝在るはずのない語で0件（何にでも当たる道具でないこと）
    chk("陰性対照 exact", len(find("02", "zqxjkvbwm")), 0)
    chk("陰性対照 fuzzy", len(find("02", "zqxjkvbwm", fuzzy=True)), 0)
    chk("陰性対照 near", len(find_near("02", ["zqxjkvbwm", "reactor"])), 0)
    # 🔴 素の grep が落とすことの陽性対照
    plain = sum(1 for _, raw in ps if "Testing Station" in raw)
    got = len(set(pg for pg, _ in find("02", "Testing Station")))
    chk("素の grep より多く拾う", got > plain, True)
    print("     （素の grep %d ページ → 畳んだ検索 %d ページ）" % (plain, got))
    # 🔴 OCR の質はページで違う（目次が最悪・本文は良い）＝最初の思い込みがここだった
    chk("目次は語が壊れている", sum(1 for _, r in ps if "Decontarnination" in r), 1)
    chk("本文の同じ語は無事", sum(1 for _, r in ps if "Decontamination" in r) >= 5, True)
    # 🔴 印字ページ = PDF - 11（134ページで拾えて125ページがこの差。④で実測）
    chk("前書きは PDF p11", len(find("02", "What began as a routine fire-alarm")), 1)
    chk("削除されたページは PDF p112",
        [pg for pg, _ in find("02", "has been deleted from this report")], [112])
    if "11" in have:
        chk("IDO-19311 の決め所", len(find("11", "Though positive proof is lacking")), 1)
        # 🔴 2026-09-07：調査係の申し送り「原文は "20 inch"（単数）で "20 inches" では0件」は**誤り**だった。
        #    実測＝単数3件（うち1件は `20-inch`。この道具は記号を落とすので拾える）／複数1件
        #    （PDF p252 `16. 7 inches to 20 inches withdrawal`）。
        #    → **渡された「確認ずみ」も自分で当てる**。単複を決め打ちにしない。
        chk("20 inch は単数も複数もある", (len(find("11", "20 inch withdrawal")),
                                        len(find("11", "20 inches withdrawal"))), (3, 1))

    print("selftest:", "PASS" if ok else "🔴FAIL")
    return ok


# ─────────────────────────── 入口 ───────────────────────────

def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(0 if selftest() else 1)
    keys = [k for k in DOCS if "--" + k in a]
    for k in keys:
        a.remove("--" + k)
    fuzzy = "--fuzzy" in a and not a.remove("--fuzzy")
    near = "--near" in a and not a.remove("--near")
    whole = "--whole" in a and not a.remove("--whole")
    opt = {}
    for flag, cast in (("--ctx", int), ("--pad", int), ("--zoom", float), ("--out", str)):
        if flag in a:
            i = a.index(flag)
            opt[flag[2:]] = cast(a[i + 1])
            del a[i:i + 2]
    if not a:
        print(__doc__)
        sys.exit(2)
    cmd, rest = a[0], a[1:]

    if cmd == "extract":
        extract(keys or list(DOCS))
        sys.exit(0)
    key = keys[0] if keys else "02"
    if cmd == "page":
        for pg, raw in pages(key):
            if pg == int(rest[0]):
                print(raw)
        sys.exit(0)
    if cmd == "crop":
        crop(key, int(rest[0]), rest[1:], pad=opt.get("pad", 140),
             zoom=opt.get("zoom", 2.6), out=opt.get("out"), whole=whole)
        sys.exit(0)
    if cmd == "find":
        q = " ".join(rest)
        ctx = opt.get("ctx", 300)
        hits = find_near(key, q.split(), ctx=ctx) if near else find(key, q, ctx, fuzzy)
        tag = "  (near)" if near else "  (fuzzy)" if fuzzy else ""
        print("### %s / %d件 : %s%s" % (DOCS[key][0], len(hits), q, tag))
        for pg, t in hits:
            print("\n--- PDF p%d ---\n%s" % (pg, t))
        sys.exit(0 if hits else 1)
    print("知らない命令: %s" % cmd)
    sys.exit(2)


if __name__ == "__main__":
    main()
