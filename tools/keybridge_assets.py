# -*- coding: utf-8 -*-
"""6本目（キー橋）の素材を作る／落とす。**出所と根拠は `ref/CREDITS.md` の台帳と1対1。**

■ なぜ要るか
  ⑤b に入った時点で、キー橋の画像は**1枚も手元に無かった**（`ref/keybridge/` は PDF と
  shots.json だけ）。台本 §4 の「図 pNN」36カット・「実写 …」71カットが、そのままでは焼けない。

■ 4つの仕事
  figs   … 報告書 PDF の必要なページだけを PNG に焼く（`ref/keybridge/*.png`）
  desc   … Commons の候補の**説明文とカテゴリ**を機械で引く（題名だけでは中身が分からないため）
  photos … 選んだ写真を Commons から落とす（`ref/keybridge/kb_*.jpg`）
  probe  … 落とした素材の中身を機械で測る（幅・インク率・空白帯）

■ 使い方（Windows は `PYTHONUTF8=1` を付ける）
    python tools/keybridge_assets.py --selftest
    python tools/keybridge_assets.py figs
    python tools/keybridge_assets.py desc <題名の一部> ...
    python tools/keybridge_assets.py photos
    python tools/keybridge_assets.py probe

⚠️ **印字ページと PDF ページを取り違えない。** MIR-25-40 は **PDF ＝ 印字 ＋ 2**
   （前付が i〜xxii。`ref/keybridge/FACTS.md` §0 の実測）。ここでは印字ページを `pr=` に書き、
   PDF ページは `pr + PDF_OFFSET` で**計算する**（手で二重に書くと片方だけ直る）。
   `--selftest` が本文の語で対応を検算する。
⚠️ 報告書の図は**英字が焼き込まれている**。逃がすのは `scene_jiko.TRIM_BY_PHOTO`
   （切る場所はカットでなくファイルに紐づける）。→ [[reference-report-figures-have-burned-in-english]]

🔴 2026-09-08（⑤b）に見つけた台本の書き間違い3件（**出典欄が正しく、画の欄が誤り**）:
   c712「不足電圧引外し装置の制御回路」＝ Figure 50 ＝ **印字 p114**（台本の画の欄は p112）
   c715「端子台381の位置」        ＝ Figure 51 ＝ **印字 p115**（台本の画の欄は p113）
   ca02「端子台381と Wire 1」      ＝ Figure 53 ＝ **印字 p118**（台本の画の欄は p113）
   ＝ 画の欄だけ「印字 ＝ PDF − 2」を逆向きに当てたための2ページずれ。ここは正しい側で焼く。
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
REF = HERE / "ref" / "keybridge"
UA = ("zukai-engine/1.0 (accident-documentary research; "
      "https://github.com/torotorotolo/zukai-engine; konariri8@gmail.com)")

# 🔴 MIR-25-40：**PDF ＝ 印字 ＋ 2**。ここ1か所だけに持たせる
PDF_OFFSET = 2
DOC = "ntsb_MIR2540"

# ── 報告書のページ（印字ページ・図番・中身・検算に使う原文の語）────────────
# 出力名は `kb_p<印字3桁>_fig<図番>.png`。**画面と出典に出るのは印字ページ**。
#
# 🔴 2026-09-08（⑤b-5）に数え直したこと ── **この報告書の図版は 71 枚ある**（焼いてあったのは32枚）。
#    ⑤b-2〜b-4 の「機関室・高圧配電盤・非常用発電機は1コマも無い」は**動画28本についての実測**で、
#    報告書の図版まで数えたものではなかった。要る側（空いた29欄）から在庫を数え直すと、
#    Fig12（0126:10 の配電）・Fig23（南北の橋台）・Fig41（ダリ側面図）・Fig42（高圧/低圧の配電盤）・
#    Fig43（主機関室）・Fig44（PMS の警報画面）・Fig71（赤い警告灯）・Fig2（2004年のキー橋）が
#    **そのまま主題**だった。→ [[feedback-gates-blind-to-the-new-material]]
#    数え方の正本＝`python tools/keybridge_assets.py list`（PDF の全図版と、焼いてあるかを出す）。
# ⚠️ 1ページに図が2つ在るページ（24＝Fig1/2、62＝Fig24/25）は、`bands()` が
#    「題のすぐ上の画像」を採るので取り違えない。ただし `ss.page(印字)` は**印字ページで引く**ので、
#    **同じページの2枚を両方焼いてはいけない**（先に見つかったほうが返る）。`list` が見張る。
PAGES = [
    (24, 2, "事故前のキー橋（2004年）", "The Francis Scott Key Bridge in 2004"),
    (31, 5, "出港時の配電の系統", "Configuration of Dali plant at time the Dali left the dock"),
    (33, 6, "ボルチモア港の海図", "Navigation chart showing Baltimore Harbor"),
    (36, 8, "0125:00 最初の停電時の配電", "the time of the initial loss of power"),
    (37, 9, "出港から接触までの軌跡", "Trackline of the Dali after it departed"),
    (38, 10, "0125:08 主機関の停止", "after the main engine shut down"),
    (40, 11, "0125:58 低圧の復旧", "when LV power was restored"),
    (41, 12, "0126:10 非常用配電盤に電気が来た",
     "when the emergency switchboard was powered by the EDG"),
    (43, 13, "0127:04 二度目の停電", "when the vessel lost power"),
    (46, 15, "0127:36 低圧の復旧", "Configuration of Dali plant at 0127:36"),
    (50, 17, "中央径間の立面図と平面図", "Elevation view and plan view of the main spans"),
    (58, 20, "第18・第19径間と第18〜22橋脚の損傷", "Damage to Spans 18 and 19"),
    (59, 21, "第16〜18径間と17番橋脚の損傷", "Damage to Spans 16"),
    (61, 23, "南の橋台と北の橋台", "South abutment (looking south), and north abutment"),
    (62, 24, "剛節橋脚と2本柱の橋脚", "Rigid-frame reinforced concrete pier"),
    (63, 26, "キー橋の3種類の径間", "The three types of spans at the Key Bridge"),
    (64, 27, "防衝工とドルフィン1", "physical protection systems"),
    (68, 31, "17番橋脚の防衝工・北から", "Pier 17, looking north, showing the fender system"),
    (69, 32, "17番橋脚の防衝工・内側", "showing the interior side of the fender system"),
    (70, 33, "サンシャイン・スカイウェイ橋の防護", "Aerial view of the Sunshine Skyway Bridge"),
    (73, 36, "ブルー・ナゴヤとダリの大きさ", "comparative sizes of the Blue Nagoya"),
    (74, 37, "架け替えの完成予想", "Rendering of the cable-stayed replacement"),
    (75, 38, "崩落したスカイウェイ橋の西径間", "collapsed western span of the Sunshine Skyway"),
    (79, 41, "ダリの側面図（船倉と、船首楼・船尾楼の甲板）",
     "Profile view of the Dali, showing cargo holds and bays"),
    (81, 42, "ダリの高圧の配電盤と低圧の配電盤",
     "The Dali’s HV switchboard (which housed the HV bus)"),
    (85, 43, "ダリの主機関室と、下層を調べる調査員",
     "The Dali’s main engine room (looking aft)"),
    (89, 44, "PMS の画面（警報を出していたもの）", "ACONIS mimic of the vessel’s PMS"),
    (111, 47, "取り外された遮断器 HR1", "HR1 disconnected and removed from HV switchboard"),
    (112, 48, "低圧の配電盤に付けた解析器", "Power analyzers installed on LV switchboard"),
    (114, 50, "HR1 の不足電圧引外し装置の制御回路", "HR1 UVR control circuit"),
    (115, 51, "端子台381の位置", "Terminal Block 381 shown amongst a stack"),
    (118, 53, "端子台381の Wire 1 と Wire 3", "identified in Terminal Block 381"),
    (121, 56, "端子台の見本・組んだものと分解したもの", "An exemplar terminal block, assembled and disassembled"),
    (124, 59, "Wire 1 と Wire 3 の圧着端子", "Close up of the Wire 1 and Wire 3 ferrules"),
    (125, 60, "端子台に差し込まれた線の深さ", "inserted inside the corresponding"),
    (127, 62, "放電で焼けた跡", "Electrical arcing damage on the spring-clamp gate face"),
    (146, 64, "口の面に載っているだけの状態", "How arcing could occur within the gap"),
    (147, 65, "正しい取り付けとの比較", "Correctly installed wire-label banding compared to"),
    (149, 66, "赤外線の熱画像による点検", "Exemplar infrared thermal imaging camera"),
    (173, 71, "点滅する赤い警告灯（クイーン・イサベラ橋）",
     "Red flashing motorist warning lights"),
]


def page_name(pr, fig):
    return f"kb_p{pr:03d}_fig{fig:02d}"


# ── Commons の写真 ───────────────────────────────────────
# (出力名, Commons のファイル名, 中身, ライセンスの区分)
# 🔴 **PD を先に、次に CC BY（表示のみ）、CC BY-SA は最後**。
#    CC BY-SA は「継承」が動画全体に及ぶという論点があるので、代わりが在るなら採らない。
# 🔴 出典は `ref/CREDITS.md` に1点ずつ記録する（撮影者名まで画面に出す）。
#
# 🔴🔴 2026-09-08（⑤b）に機械で確かめたこと ── **「事故前の写真は在庫に1点も無い」は誤り**。
#    ②の台帳が数えたのは `Category:Francis Scott Key Bridge collapse`（1,017点＝崩落後）と
#    郡 Flickr の `FSK-Collapse-NNN`（170点＝崩落後）だけだった。
#    **`Category:Francis Scott Key Bridge (Baltimore)` に 252点あり、うち事故前が 99点**
#    （幅1280以上・連続階調が 92点）。PD 19点・CC BY 12点・残りは CC BY-SA。
#    → `analytics/materials/kb_pre.json`／`kb_const.json`。引き継ぎ §5-5 はここで解消。
#
# ⚠️ **CC BY-SA は採らない**（「継承」が動画全体に及ぶという論点を抱えない）。
#    下は **PD と CC BY（表示のみ）だけ**。説明文は `desc` で1点ずつ読んで中身を確かめた。
PHOTOS = [
    # ── 事故前のキー橋 ──────────────────────────────
    ("kb_pre_1976", "Francis Scott Key bridge 1976.jpg",
     "1976年8月11日・開通前の橋（The Evening Sun）", "PD"),
    ("kb_pre_harbor07", "Francis scott key bridge.jpg",
     "2007年・内港から見た全景", "PD"),
    ("kb_pre_navy12", "Baltimore Navy Week 2012 120613-N-FV870-996.jpg",
     "2012年・橋の下をくぐる艦（航路の上）", "PD"),
    ("kb_pre_oakhill14", "Francis Scott Key Bridge at Baltimore in September 2014.JPG",
     "2014年・橋に近づく艦", "PD"),
    ("kb_pre_catlett22", "USACE boat Catlett passes under Baltimore's Francis Scott "
     "Key Bridge - 220420-A-OX377-2001.jpeg",
     "2022年・橋の下を通る工兵隊の測量艇", "PD"),
    ("kb_pre_deck05", "Driving the Francis Scott Key bridge.jpg",
     "2005年・橋の路面（走行中の車内から。4車線）", "CC BY 2.0"),
    ("kb_pre_2019", "Francis scott key bridge (2019).jpg",
     "2019年・全景（5416x3610）", "CC BY 2.0"),
    # ── 建設中（第1章）──────────────────────────────
    ("kb_bld_harbor", "CONSTRUCTION OF A BRIDGE ACROSS THE BALTIMORE HARBOR. "
     "THE BRIDGE WILL COMPLETE THE BALTIMORE BELTWAY - NARA - 546833.jpg",
     "建設中の橋（NARA 546833）", "PD"),
    ("kb_bld_piers", "AT WORK ON PIERS FOR NEW BRIDGE THAT WILL CROSS THE BALTIMORE "
     "HARBOR AT HAWKINS POINT. THIS BRIDGE WILL COMPLETE THE... - NARA - 546837.jpg",
     "橋脚の工事（NARA 546837）", "PD"),
    ("kb_bld_supports", "AT WORK ON THE SUPPORTS OF A NEW BRIDGE. THIS BRIDGE WILL "
     "COMPLETE THE BALTIMORE BELTWAY. NEAR HAWKINS POINT - NARA - 546929.jpg",
     "橋脚の支持部の工事（NARA 546929）", "PD"),
    ("kb_bld_curtis", "CONSTRUCTION, A BELTWAY BRIDGE ACROSS CURTIS BAY - NARA - 546911.jpg",
     "カーティス湾を渡る取付部の建設（NARA 546911）", "PD"),
]

CM_API = "https://commons.wikimedia.org/w/api.php"


def _get(url, timeout=90):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


# ─────────────────────────── 図 ───────────────────────────

def figs(only=None, zoom=3.0):
    """報告書の必要なページだけを PNG に焼く。"""
    import fitz
    from PIL import Image
    REF.mkdir(parents=True, exist_ok=True)
    src = REF / (DOC + ".pdf")
    if not src.exists():
        print(f"  🔴 {src.name} が無い")
        return 0
    doc = fitz.open(src)
    n = 0
    for pr, fig, note, _w in PAGES:
        name = page_name(pr, fig)
        if only and name not in only and str(pr) not in only:
            continue
        page = doc[pr + PDF_OFFSET - 1]
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        dest = REF / (name + ".png")
        pix.save(dest)
        # グレースケールで保存し直す（このリポジトリは public。本編は低彩度なので絵は変わらない）
        Image.open(dest).convert("L").save(dest, optimize=True)
        kb = dest.stat().st_size // 1024
        print(f"  ✓ {dest.name:<22} {pix.width}x{pix.height} {kb:>5}KB  "
              f"PDF{pr + PDF_OFFSET}／印字 p.{pr}  Figure {fig}  {note}")
        n += 1
    print(f"■ 図 {n} 枚")
    return n


# ─────────────────────────── Commons ───────────────────────────

def _api(**kw):
    kw.setdefault("format", "json")
    url = CM_API + "?" + urllib.parse.urlencode(kw)
    return json.loads(_get(url))


def desc(*words):
    """題名に語を含む Commons のファイルの**説明文とカテゴリ**を出す。

    🔴 題名では中身が分からない（`FSK-Collapse-100.jpg` が何の写真かは題名に無い）。
       **絵を見る前に、書かれている説明を機械で読む。**
       → [[feedback-measure-the-source-before-choosing-the-crop]]
    """
    for w in words:
        d = _api(action="query", prop="imageinfo|categories",
                 iiprop="url|size|extmetadata", cllimit=30,
                 titles=w if w.startswith("File:") else f"File:{w}")
        for p in d.get("query", {}).get("pages", {}).values():
            if "missing" in p:
                print(f"  🔴 {p['title']} は無い")
                continue
            ii = (p.get("imageinfo") or [{}])[0]
            em = ii.get("extmetadata", {})
            def g(k):
                return re.sub(r"<[^>]+>", "", em.get(k, {}).get("value", "")).strip()
            print(f"■ {p['title']}  {ii.get('width')}x{ii.get('height')}")
            print(f"   ライセンス: {g('LicenseShortName')}／撮影者: {g('Artist')[:60]}")
            print(f"   日付: {g('DateTimeOriginal')[:40]}")
            print(f"   説明: {re.sub(chr(10), ' ', g('ImageDescription'))[:400]}")
            cats = [c["title"][9:] for c in p.get("categories", [])]
            print(f"   カテゴリ: {'／'.join(cats[:10])}")
        time.sleep(0.4)


def _commons_url(title, width=2600):
    d = _api(action="query", prop="imageinfo", iiprop="url|size",
             iiurlwidth=width, titles=title)
    for p in d["query"]["pages"].values():
        ii = (p.get("imageinfo") or [{}])[0]
        if ii:
            return ii.get("thumburl") or ii.get("url"), ii.get("width"), ii.get("height")
    return None, None, None


def photos(only=None):
    """`PHOTOS` の写真を落とす。**名前→ファイル名の対応を必ず表に出す**（取り違えの検算）。"""
    REF.mkdir(parents=True, exist_ok=True)
    got, miss = 0, []
    for name, title, note, lic in PHOTOS:
        if only and name not in only:
            continue
        dest = REF / f"{name}.jpg"
        if dest.exists():
            print(f"  ・ {dest.name} は既にある（{dest.stat().st_size // 1024}KB）")
            got += 1
            continue
        try:
            url, w, h = _commons_url(title if title.startswith("File:") else f"File:{title}")
        except Exception as e:                              # noqa: BLE001
            print(f"  🔴 {name}: {e}")
            miss.append(name)
            continue
        if not url:
            print(f"  🔴 {name}: URL が取れない（{title}）")
            miss.append(name)
            continue
        dest.write_bytes(_get(url))
        print(f"  ✓ {dest.name:<26} 原本 {w}x{h}  {lic:<10} {note}")
        got += 1
        time.sleep(0.8)
    print(f"■ 写真 {got} 枚（取れなかった {miss}）")
    return got, miss


# ─────────────────────────── 検算 ───────────────────────────

def selftest():
    """🔴 印字ページと PDF ページの対応を、**本文の語**で検算する。

    ⚠️ 「+2 で足りる」は前付を数えた見立てであって実測ではない。ページを1枚ずつ開いて、
       台本が引く図の題がそこに在ることを確かめる。→ [[feedback-verify-your-own-instrument]]
    """
    import fitz
    ok = []

    def chk(name, got):
        ok.append(bool(got))
        print(f"  {'✓' if ok[-1] else '🔴'} {name}")

    src = REF / (DOC + ".pdf")
    if not src.exists():
        print(f"  🔴 {src.name} が無いので検算できない")
        return False
    doc = fitz.open(src)

    # 陽性対照：**中身が空でも回る検査になっていないか**を先に見る
    # → [[feedback-gates-blind-to-the-new-material]]
    chk("陽性対照：PAGES が空でない", len(PAGES) >= 30)

    for pr, fig, note, word in PAGES:
        pdf = pr + PDF_OFFSET
        t = re.sub(r"[^a-z0-9]", "", doc[pdf - 1].get_text().lower())
        chk(f"印字 p{pr}（PDF{pdf}）Figure {fig}：『{word[:44]}』がある",
            re.sub(r"[^a-z0-9]", "", word.lower()) in t)
        # 🔴 図番も同じページに在ること（ページはずれていないが図が違う、を止める）
        chk(f"印字 p{pr}：そのページに『Figure {fig}.』が在る",
            re.sub(r"[^a-z0-9]", "", f"Figure {fig}.".lower()) in t)

    # 出力名がぶつからないこと（同じ印字ページを2度焼かない）
    names = [page_name(p, f) for p, f, _n, _w in PAGES]
    chk(f"出力名が重複していない（{len(names)}枚）", len(names) == len(set(names)))

    good = all(ok)
    print("  " + (f"✓ 検算 {len(ok)}/{len(ok)}" if good
                  else f"🔴 検算 {sum(ok)}/{len(ok)} で落ちた"))
    return good


def figlist():
    """🔴 PDF に**在る図版を全部**出し、焼いてあるかを並べる（要る側から数えるための道具）。

    ⚠️ なぜ要るか ── `PAGES` を読む検査は「自分が書いた分」しか数えない。
       2026-09-08 に「機関室は1コマも無い」と書いた根拠は**動画28本の実測**で、
       報告書の図版は数えていなかった（実際は Fig43 が主機関室そのもの）。
       → [[feedback-gates-blind-to-the-new-material]]
    ⚠️ 前付（i〜xxii）の「図一覧」は点線とページ番号で終わるので、それで落とす。
    """
    import fitz
    doc = fitz.open(REF / (DOC + ".pdf"))
    have = {f: p for p, f, _n, _w in PAGES}
    seen = {}
    for i in range(doc.page_count):
        pr = i + 1 - PDF_OFFSET
        if pr < 1:
            continue
        for m in re.finditer(r"^Figure (\d+)\.\s*(.{0,160})", doc[i].get_text(), re.M | re.S):
            n, cap = int(m.group(1)), re.sub(r"\s+", " ", m.group(2)).strip()
            if "...." in cap or n in seen:      # 図一覧の行は採らない
                continue
            seen[n] = (pr, cap)
    bad = []
    for n in sorted(seen):
        pr, cap = seen[n]
        if n in have:
            if have[n] != pr:
                bad.append(f"Fig{n}: PAGES は印字 p{have[n]} だが本文は p{pr}")
            print(f"  焼済 Fig{n:>2}  p{pr:>3}  {cap[:110]}")
        else:
            print(f"    ・ Fig{n:>2}  p{pr:>3}  {cap[:110]}")
    # 🔴 同じ印字ページの図を2枚焼くと `ss.page(印字)` がどちらを返すか決まらない
    bypage = {}
    for p, f, _n, _w in PAGES:
        bypage.setdefault(p, []).append(f)
    for p, fs in sorted(bypage.items()):
        if len(fs) > 1:
            bad.append(f"印字 p{p} に図を{len(fs)}枚焼いている（Fig{fs}）＝ ss.page({p}) が決まらない")
    print(f"■ 図版 {len(seen)} 枚（焼いてある {len(have)} 枚）")
    for m in bad:
        print(f"  🔴 {m}")
    return 1 if bad else 0


def where(name, *words):
    """そのページの中で、原文の語がどこにあるかを **0〜1 の位置**で返す（`ss.focus` へ渡す値）。"""
    import fitz
    row = next((p for p in PAGES if page_name(p[0], p[1]) == name or str(p[0]) == name), None)
    if row is None:
        print(f"🔴 {name} は PAGES に無い")
        return None
    pr, fig = row[0], row[1]
    page = fitz.open(REF / (DOC + ".pdf"))[pr + PDF_OFFSET - 1]
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
        print(f"🔴 『{' '.join(words)}』はこのページの文字層に無い")
        return None
    hs = [w for a, b, w in spans if a < m.end() and b > m.start()]
    x0, y0 = min(h[0] for h in hs), min(h[1] for h in hs)
    x1, y1 = max(h[2] for h in hs), max(h[3] for h in hs)
    fx = ((x0 + x1) / 2 - r.x0) / r.width
    fy = ((y0 + y1) / 2 - r.y0) / r.height
    print(f"  {page_name(pr, fig)}: 『{' '.join(words)[:44]}』")
    print(f"    箱 x {(x0 - r.x0) / r.width:.3f}〜{(x1 - r.x0) / r.width:.3f}"
          f"／y {(y0 - r.y0) / r.height:.3f}〜{(y1 - r.y0) / r.height:.3f}")
    print(f"    → **ss.focus(ss.XXX, {fx:.3f}, {fy:.3f}, zoom)**")
    return fx, fy


def fb():
    """`footage.USE` の各欄から**ひかえの静止画** `ref/keybridge/fb_<cid>.jpg` を焼く。"""
    import subprocess
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


# ─────────────────── 図の位置を式で出す（bands）───────────────────

def bands(out=None):
    """32枚それぞれについて **図の箱・題の箱・本文の帯**を測って JSON に書く。

    🔴 なぜ要るか
      `図 pN` のカットで画面に出したいのは**図そのもの**であって、紙いちめんではない。
      どこを切るかを目分量で置くと、5本目で 177件出た「行頭が語の途中から始まる」と
      同じことが図でも起きる。→ [[feedback-measure-before-fixing-layout]]

    🔴 図の箱は**画素で探さない**。この報告書はボーンデジタルで、図は埋め込みの画像なので
      `page.get_image_bbox()` が**正確な矩形**を返す（`ref/keybridge/FACTS.md` §0）。
      ⚠️ 1ページに図が2つ在ることがある（印字 p62 は Figure 24 と 25）。
         **題（`Figure N.`）のすぐ上に在る画像**を、その図番の箱として採る。

    出すもの（すべて **0〜1 の割合**。PNG は PDF を等倍で焼いたので同じ座標）
      `fig_box`  … 図そのものの矩形 (x0,y0,x1,y1)
      `cap_y0/y1`… 図の題の上端・下端（**題は画面に出さない**＝切り出しに入れない）
      `head_y1`  … 柱（誌名と MIR-25-40）の下端
      `text_x0/x1` … 本文の文字が入っている横の帯（本文ページに寄るとき用）
    """
    import fitz
    src = REF / (DOC + ".pdf")
    doc = fitz.open(src)
    res, bad = {}, []
    for pr, fig, note, _w in PAGES:
        name = page_name(pr, fig)
        page = doc[pr + PDF_OFFSET - 1]
        r = page.rect

        def fy(v):
            return (v - r.y0) / r.height

        def fx(v):
            return (v - r.x0) / r.width

        # 題の行＝`Figure <fig>.` で始まる行
        cap = None
        for blk in page.get_text("dict")["blocks"]:
            if blk.get("type") != 0:
                continue
            for ln in blk["lines"]:
                txt = "".join(sp["text"] for sp in ln["spans"]).strip()
                if txt.startswith(f"Figure {fig}."):
                    cap = ln["bbox"]
        if cap is None:
            bad.append(f"{name}: 題『Figure {fig}.』が見つからない")
            continue
        # 🔴 その題のすぐ上に在る画像を採る（同じページの別の図を取り違えない）
        boxes = [page.get_image_bbox(i) for i in page.get_images(full=True)]
        above = [bb for bb in boxes if bb.y1 <= cap[1] + 2]
        if not above:
            bad.append(f"{name}: 題の上に画像が無い（画像 {len(boxes)}個）")
            continue
        bb = max(above, key=lambda x: x.y1)
        # 柱と本文の帯
        words = page.get_text("words")
        head = [w for w in words if fy(w[3]) < 0.12]
        head_y1 = max(fy(w[3]) for w in head) if head else 0.0
        body = [w for w in words if fy(w[1]) > head_y1 + 0.005 and fy(w[3]) < 0.93]
        res[name] = dict(
            printed=pr, figure=fig, note=note,
            fig_box=[round(fx(bb.x0), 4), round(fy(bb.y0), 4),
                     round(fx(bb.x1), 4), round(fy(bb.y1), 4)],
            cap_y0=round(fy(cap[1]), 4), cap_y1=round(fy(cap[3]), 4),
            head_y1=round(head_y1, 4),
            text_x0=round(min(fx(w[0]) for w in body), 4) if body else 0.118,
            text_x1=round(max(fx(w[2]) for w in body), 4) if body else 0.879,
        )
        f = res[name]["fig_box"]
        print(f"  {name:<20} 図 x {f[0]:.3f}-{f[2]:.3f} y {f[1]:.3f}-{f[3]:.3f}"
              f"  縦横比 {(f[2] - f[0]) * 1836 / max(1e-6, (f[3] - f[1]) * 2376):.2f}"
              f"／題 {res[name]['cap_y0']:.3f}  {note}")
    for m in bad:
        print(f"  🔴 {m}")
    if bad:
        raise SystemExit(2)
    dest = Path(out) if out else (REF / "textbands.json")
    dest.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"■ {len(res)} 枚 → {dest}")
    return res


def probe():
    """落とした素材の中身を機械で測る（全画面に耐えるか＝`src_probe.py` と同じ物差し）。"""
    import src_probe as SP
    files = sorted(REF.glob("kb_*.png")) + sorted(REF.glob("kb_*.jpg"))
    if not files:
        print("🔴 まだ1枚も落ちていない")
        return 1
    sys.argv = [sys.argv[0], "--files"] + [str(f) for f in files]
    SP.main()
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(0 if selftest() else 1)
    cmd = a[0] if a else ""
    if cmd == "figs":
        figs(only=set(a[1:]) or None)
    elif cmd == "desc":
        desc(*a[1:])
    elif cmd == "photos":
        photos(only=set(a[1:]) or None)
    elif cmd == "list":
        sys.exit(figlist())
    elif cmd == "where":
        where(a[1], *a[2:])
    elif cmd == "fb":
        fb()
    elif cmd == "bands":
        bands()
    elif cmd == "probe":
        sys.exit(probe())
    else:
        print(__doc__)
