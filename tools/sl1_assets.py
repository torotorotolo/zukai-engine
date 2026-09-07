# -*- coding: utf-8 -*-
"""5本目（SL-1）の素材を作る／落とす。**出所と根拠は `ref/CREDITS.md` の台帳と1対1。**

■ なぜ要るか
  ⑤b に入った時点で、SL-1 の画像は**1枚も手元に無かった**（PDF と shots.json だけ）。
  台本 §4 の「図 pNN」45カット・「実写 HAER …」16カットが、そのままでは焼けない。

■ 3つの仕事
  figs   … 報告書 PDF の必要なページだけを PNG に焼く（`ref/sl1/*.png`）
  haer   … HAER ID-33-D の写真を Wikimedia Commons から落とす（`ref/sl1/haer_*.jpg`）
  probe  … 落とした素材の中身を機械で測る（幅・インク率・空白帯）

■ 使い方（Windows は `PYTHONUTF8=1` を付ける）
    python tools/sl1_assets.py --selftest
    python tools/sl1_assets.py figs
    python tools/sl1_assets.py haer
    python tools/sl1_assets.py probe

⚠️ **印字ページと PDF ページを取り違えない。** IDO-19302 は **PDF ＝ 印字 ＋ 11**
   （`ref/CREDITS.md` ⑥ の実測）。ここでは PDF ページを `pdf=` に、画面に出す
   印字ページを `pr=` に**両方**書き、`--selftest` が本文の語で対応を検算する。
⚠️ 報告書の図は**英字が焼き込まれている**。逃がすのは `scene_jiko.TRIM_BY_PHOTO`
   （切る場所はカットでなくファイルに紐づける）。→ [[reference-report-figures-have-burned-in-english]]
"""
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
REF = HERE / "ref" / "sl1"
UA = ("zukai-engine/1.0 (accident-documentary research; "
      "https://github.com/torotorotolo/zukai-engine; konariri8@gmail.com)")

# ── 報告書のページ ────────────────────────────────────────
# (出力名, PDF名, PDFページ, 画面に出す印字ページ, 中身, 検算に使う語)
# 🔴 `pr` は**画面と出典に出す番号**。`pdf` は**この道具が開く番号**。混ぜない。
PAGES = [
    # ── IDO-19302（PDF ＝ 印字 ＋ 11）──
    ("ido_pvii_foreword", "IDO-19302", 11, "vii", "前書き（原因は扱わないと断る段落）",
     "does not attempt to determine the cause"),
    ("ido_p004_night", "IDO-19302", 15, "4", "夜間指示書の9項目",
     "December 23, 1960"),
    ("ido_p013_fig11", "IDO-19302", 24, "13", "Fig 1.1 試験場の全体図", None),
    ("ido_p014_fig12", "IDO-19302", 25, "14", "Fig 1.2 SL-1 区域の配置図",
     "PLOT PLAN OF SL-I AREA"),
    ("ido_p015_fig13", "IDO-19302", 26, "15", "Fig 1.3 炉建屋の断面", None),
    ("ido_p016_fig14", "IDO-19302", 27, "16", "Fig 1.4 炉の縦断面",
     "LAYIUATED TOP SHIELD"),
    ("ido_p017_fig15", "IDO-19302", 28, "17", "Fig 1.5 位置の番号と炉心の配置",
     "LOCATION OF POSITIONS AND CORE LOADING PATTERN"),
    ("ido_p018_fig16", "IDO-19302", 29, "18", "Fig 1.6 十字型の制御棒",
     "CADMIUM"),
    ("ido_p019_fig17", "IDO-19302", 30, "19", "Fig 1.7 燃料要素", None),
    ("ido_p020_fig18", "IDO-19302", 31, "20", "Fig 1.8 制御棒の駆動",
     "CONTROL ROD DRIVE"),
    ("ido_p021_log", "IDO-19302", 32, "21", "運転日誌と時系列の最初のページ",
     "SEQUENCE OF EVENTS"),
    # 🔴 2026-09-07（⑤b）追加。**記録映画に無い主題の欄**を、そのカットの出典が指す
    #    報告書のページそのものに落とすために切り出した（代用ではなく根拠を出す）。
    #    → `ref/sl1/SHOTS_INDEX.md` §0／§3
    # ⚠️ 検算の語を `fire station` にしたら落ちた。**ページが違うのではなく語が無かった**
    #    （原文は `Fire Engine No. 3 arrived at the SL-1 Area, approximately eight miles from CFA`）。
    #    → [[feedback-absence-of-a-word-is-not-absence]]。落ちたら先にページの中身を読む
    ("ido_p022_fire", "IDO-19302", 33, "22", "消防の到着・空気呼吸器の受け渡し（時系列）",
     "Fire Engine No. 3"),
    ("ido_p023_ctrl", "IDO-19302", 34, "23", "制御室で見たもの・階段の線量（時系列）",
     "lunch pails"),
    ("ido_p090_found", "IDO-19302", 101, "90", "2人を見つけた記述・3人目の記述",
     "movement of the first victim"),
    ("ido_p091_rescue", "IDO-19302", 102, "91", "救助の8分・救急車と落ち合う",
     "resuscitator"),
    ("ido_p096_ship", "IDO-19302", 107, "96", "棺の札と輸送の記述", "casket"),
    ("ido_p035_fig21", "IDO-19302", 46, "35", "Fig 2.1 事故後の運転室", None),
    ("ido_p036_fig22", "IDO-19302", 47, "36", "Fig 2.2 事故後の運転室", None),
    ("ido_p095_lead", "IDO-19302", 106, "95", "鉛で包み金属の帯で締めた記述",
     "lead sheeting"),
    ("ido_p100_kingston", "IDO-19302", 111, "100", "キングストンでの記述",
     "shipping container"),
    ("ido_p101_deleted", "IDO-19302", 112, "101", "本文が2行だけの白紙ページ",
     "has been deleted from this report"),
    ("ido_p103_fig51", "IDO-19302", 114, "103", "Fig 5.1 運転階の床", None),
    # ── IDO-19311（PDF ページで指定。印字は ii / I-5）──
    ("i11_p004_abstract", "IDO-19311", 4, "ii", "要旨（20インチ引き抜き）",
     "ABSTRACT"),
    ("i11_p019_sec41", "IDO-19311", 19, "I-5", "§4.1 はっきりした証明は無い",
     "Inspection of the core revealed"),
    # ── ANL-6692（印字 36 ＝ PDF 38）──
    ("anl_p001_cover", "ANL-6692", 1, "1", "表紙", "ANL-6692"),
    ("anl_p038_vf", "ANL-6692", 38, "36", "§VIII-F 断定的にこう述べたい",
     "tempting to state categorically"),
    # ── 🔴 2026-09-07（⑤b）に足した2冊。④台本の時点では「未保存（全文検索のみ）」だった ──
    # AEC 調査委員会報告（台本 c903・c904）。Internet Archive `SL1PressRelease1961`。
    # ⚠️ 収蔵品の題は「Press Release」だが、**中身は43ページの報告書本体**（1ページ目で確認）。
    #    題で決めない → [[feedback-measure-the-source-before-choosing-the-crop]]
    ("aec_p001_cover", "AEC-board-1961", 1, "1", "AEC 調査委員会報告の表紙（43ページ）",
     "THE GENERAL MANAGER'S BOARD OF INVESTIGATION"),
    # 官報（台本 c916）。36 FR 3256〜。**印字 3258 ＝ PDF 12**（本文の語で確認）。
    ("fr_p3258_gdc", "FR-1971-02-20", 12, "3258", "一般設計基準の25番と26番",
     "Criterion 25"),
]

# ── HAER ID-33-D の写真（Wikimedia Commons）─────────────────
# 台本 §4 が名指ししている 15点。`materials.json` の `acc` と1対1。
# 🔴 権利＝米議会図書館 HABS/HAER の記録写真＝合衆国政府の職務著作＝パブリックドメイン。
# ⚠️ **番号で取り違えない**。Commons のファイル名は `…(HAER ID-33-D-NN).tif` の形。
HAER_NOS = [14, 15, 52, 53, 56, 64, 65, 67, 69, 70, 73, 74, 76, 78]

CM_API = "https://commons.wikimedia.org/w/api.php"


def _get(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# ─────────────────────────── 図 ───────────────────────────

def figs(only=None, zoom=3.0):
    """報告書の必要なページだけを PNG に焼く。"""
    import fitz
    REF.mkdir(parents=True, exist_ok=True)
    n = 0
    for name, doc, pdf, pr, note, _w in PAGES:
        if only and name not in only:
            continue
        src = REF / (doc + ".pdf")
        if not src.exists():
            print(f"  🔴 {src.name} が無い（`ref/CREDITS.md` ⑥ の curl で取る）")
            continue
        page = fitz.open(src)[pdf - 1]
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        dest = REF / (name + ".png")
        pix.save(dest)
        # 🔴 グレースケールで保存し直す（**このリポジトリは public。RGB のままだと 22.8MB**）。
        #    ⚠️ 本編は低彩度のデュオトーンで焼くので、**紙の色は最終出力に出ない**
        #       （官報だけ色あせた紙の色 RGB 189/171/144 を持っていたが、同じ理由で落とす）。
        #    ⇒ 絵は変わらず 22.8 → 12.5MB。`check_blank` のインク率も 4.2% 以上のまま。
        from PIL import Image
        Image.open(dest).convert("L").save(dest, optimize=True)
        kb = dest.stat().st_size // 1024
        print(f"  ✓ {dest.name:<24} {pix.width}x{pix.height} {kb:>5}KB  "
              f"{doc} PDF{pdf}／印字 p.{pr}  {note}")
        n += 1
    print(f"■ 図 {n} 枚")
    return n


# ─────────────────────────── HAER ───────────────────────────

def _commons_search(no):
    """HAER ID-33-D-NN を含む Commons のファイル名を1件返す。"""
    q = urllib.parse.quote(f'insource:"HAER ID-33-D-{no}" incategory:"SL-1"')
    url = (f"{CM_API}?action=query&list=search&srsearch={q}"
           f"&srnamespace=6&srlimit=5&format=json")
    import json
    d = json.loads(_get(url))
    hits = [h["title"] for h in d.get("query", {}).get("search", [])]
    if hits:
        return hits
    # カテゴリ縛りを外して再試行
    q = urllib.parse.quote(f'insource:"HAER ID-33-D-{no}"')
    url = (f"{CM_API}?action=query&list=search&srsearch={q}"
           f"&srnamespace=6&srlimit=5&format=json")
    d = json.loads(_get(url))
    return [h["title"] for h in d.get("query", {}).get("search", [])]


def _commons_url(title, width=2600):
    import json
    url = (f"{CM_API}?action=query&prop=imageinfo&iiprop=url|size|extmetadata"
           f"&iiurlwidth={width}&titles={urllib.parse.quote(title)}&format=json")
    d = json.loads(_get(url))
    for p in d["query"]["pages"].values():
        ii = (p.get("imageinfo") or [{}])[0]
        if ii:
            return ii.get("thumburl") or ii.get("url"), ii.get("width"), ii.get("height")
    return None, None, None


def haer(nos=None):
    """HAER の写真を落とす。**番号→ファイル名の対応を必ず表に出す**（取り違えの検算）。"""
    REF.mkdir(parents=True, exist_ok=True)
    got, miss = 0, []
    for no in (nos or HAER_NOS):
        dest = REF / f"haer_{no:02d}.jpg"
        if dest.exists():
            print(f"  ・ {dest.name} は既にある（{dest.stat().st_size // 1024}KB）")
            got += 1
            continue
        try:
            titles = _commons_search(no)
        except Exception as e:                              # noqa: BLE001
            print(f"  🔴 {no}: 検索が失敗 {e}")
            miss.append(no)
            continue
        # 番号がぴったり一致するものだけ採る（`-7` が `-76` に当たるのを防ぐ）
        pat = re.compile(rf"HAER ID-33-D-{no}\b")
        hit = next((t for t in titles if pat.search(t)), None)
        if hit is None:
            print(f"  🔴 ID-33-D-{no}: Commons に見つからない（候補 {titles}）")
            miss.append(no)
            continue
        url, w, h = _commons_url(hit)
        if not url:
            print(f"  🔴 ID-33-D-{no}: URL が取れない（{hit}）")
            miss.append(no)
            continue
        dest.write_bytes(_get(url))
        print(f"  ✓ {dest.name}  原本 {w}x{h}  ← {hit}")
        got += 1
        time.sleep(1.0)
    print(f"■ HAER {got} 枚（取れなかった {miss}）")
    return got, miss


# ─────────────────────────── 検算 ───────────────────────────

def selftest():
    """🔴 印字ページと PDF ページの対応を、**本文の語**で検算する。

    ⚠️ 「+11 で足りる」は表の見立てであって実測ではない。ページを1枚ずつ開いて、
       台本が引く語がそこに在ることを確かめる。→ [[feedback-verify-your-own-instrument]]
    """
    import fitz
    ok = []

    def chk(name, got, want=True):
        ok.append(bool(got) == bool(want))
        print(f"  {'✓' if ok[-1] else '🔴'} {name}")

    for name, doc, pdf, pr, _note, word in PAGES:
        src = REF / (doc + ".pdf")
        if not src.exists():
            print(f"  ⚠️ {src.name} が無いので {name} は検算できない")
            continue
        if word is None:                    # 図のページは文字が無い＝語では検算できない
            t = fitz.open(src)[pdf - 1].get_text()
            chk(f"{name}: 図のページ（文字 {len(t.strip())}字＝300字未満）",
                len(t.strip()) < 300)
            continue
        t = re.sub(r"[^a-z0-9]", "", fitz.open(src)[pdf - 1].get_text().lower())
        chk(f"{name}: PDF{pdf} に『{word[:34]}』がある",
            re.sub(r"[^a-z0-9]", "", word.lower()) in t)

    # 番号の取り違え（`-7` が `-76` に当たらないこと）
    pat = re.compile(r"HAER ID-33-D-7\b")
    chk("番号の境で切る（ID-33-D-7 は ID-33-D-76 に当たらない）",
        not pat.search("Foo (HAER ID-33-D-76).tif"))
    chk("番号の境で切る（ID-33-D-7 は ID-33-D-7 に当たる）",
        bool(pat.search("Foo (HAER ID-33-D-7).tif")))

    good = all(ok)
    print("  " + (f"✓ 検算 {len(ok)}/{len(ok)}" if good
                  else f"🔴 検算 {sum(ok)}/{len(ok)} で落ちた"))
    return good


def where(name, *words):
    """そのページの中で、原文の語がどこにあるかを **0〜1 の位置**で返す。

    🔴 報告書の本文に寄るカットは、`focus()` に渡す (fx, fy) を**目分量で置かない**。
       PDF の文字の箱から出す。→ [[feedback-measure-before-fixing-layout]]
    ⚠️ 文字層は OCR で空白が割れているので、`page.search_for` は当たらない。
       語を畳んで（英数字だけにして）連続一致で探す。→ `ido_text.crop` と同じやり方。
    ⚠️ 出た値は**そのページの PNG に対する割合**。PNG は PDF を等倍で焼いたものなので同じ。
    """
    import fitz
    row = next((p for p in PAGES if p[0] == name), None)
    if row is None:
        print(f"🔴 {name} は PAGES に無い")
        return None
    _n, doc, pdf, _pr, _note, _w = row
    page = fitz.open(REF / (doc + ".pdf"))[pdf - 1]
    r = page.rect
    flat, spans = [], []
    for w in page.get_text("words"):
        s = re.sub(r"[^a-z0-9]", "", w[4].lower())
        if not s:
            continue
        spans.append((len(flat), len(flat) + len(s), w))
        flat.extend(s)
    key = re.sub(r"[^a-z0-9]", "", " ".join(words).lower())
    m = re.search(re.escape(key), "".join(flat))
    if not m:
        print(f"🔴 『{' '.join(words)}』はこのページの文字層に無い"
              f"（OCR の崩れかもしれない。語を短くする）")
        return None
    hs = [w for a, b, w in spans if a < m.end() and b > m.start()]
    x0, y0 = min(h[0] for h in hs), min(h[1] for h in hs)
    x1, y1 = max(h[2] for h in hs), max(h[3] for h in hs)
    fx = ((x0 + x1) / 2 - r.x0) / r.width
    fy = ((y0 + y1) / 2 - r.y0) / r.height
    print(f"  {name}: 『{' '.join(words)[:44]}』")
    print(f"    箱 x {(x0 - r.x0) / r.width:.3f}〜{(x1 - r.x0) / r.width:.3f}"
          f"／y {(y0 - r.y0) / r.height:.3f}〜{(y1 - r.y0) / r.height:.3f}")
    print(f"    → **ss.focus(ss.XXX, {fx:.3f}, {fy:.3f}, zoom)**")
    return fx, fy


def fb():
    """`footage.USE` の各欄から**ひかえの静止画** `ref/sl1/fb_<cid>.jpg` を焼く。

    ⚠️ 動画のコマが取れたときは動画が勝つ（`scene_jiko.credit_of`）。これは
       クラウドで切り出しに失敗したときに**画が空にならない**ための保険。
    ⚠️ 秒は USE の `start` そのもの。ショットの頭は切り替わりの残りが写ることがあるので
       **0.4秒だけ内側**から採る（`until` は越えない）。
    """
    import subprocess
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    clip_dir = HERE / "out" / "jiko" / "clip"
    n, miss = 0, []
    for cid, u in sorted(FO.USE.items()):
        src = clip_dir / f"{u['clip']}.mp4"
        if not src.exists():
            miss.append(cid)
            continue
        at = min(float(u["start"]) + 0.4, float(u["until"]) - 0.2)
        dest = REF / f"fb_{cid}.jpg"
        subprocess.run(
            ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
             "-ss", f"{at:.2f}", "-i", str(src), "-frames:v", "1",
             "-vf", "scale=1920:1080", "-q:v", "2", str(dest)],
            capture_output=True, timeout=300)
        if dest.exists():
            n += 1
        else:
            miss.append(cid)
    print(f"■ ひかえの静止画 {n} 枚（作れなかった {miss}）")
    return n


def probe():
    """落とした素材の中身を機械で測る（全画面に耐えるか＝`src_probe.py` と同じ物差し）。"""
    import src_probe as SP
    files = sorted(REF.glob("*.png")) + sorted(REF.glob("*.jpg"))
    if not files:
        print("🔴 まだ1枚も落ちていない")
        return 1
    SP.main(["--files"] + [str(f) for f in files])
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(0 if selftest() else 1)
    cmd = a[0] if a else ""
    if cmd == "figs":
        figs(only=set(a[1:]) or None)
    elif cmd == "haer":
        haer([int(x) for x in a[1:]] or None)
    elif cmd == "where":
        where(a[1], *a[2:])
    elif cmd == "fb":
        fb()
    elif cmd == "probe":
        sys.exit(probe())
    else:
        print(__doc__)
