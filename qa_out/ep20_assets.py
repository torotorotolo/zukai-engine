# -*- coding: utf-8 -*-
"""ep20_assets.py — 20本目（日本航空123便のリメイク）の写真・頁・映像の束（⑤b-2・2026-10-08）。19本目 `ep19_assets.py` の形。

取得はすんでいる（映像方針＝了承②・`ref/ep20/eizou_build/fetch20.py`・記録 `fetch20.tsv`）。ここは**束を作る道**だけを持つ。
  python qa_out/ep20_assets.py build            # 写真の束 ref/ep20/<名>.jpg ＋ 権利の台帳 ref/ep20/assets.json
  python qa_out/ep20_assets.py panel            # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python qa_out/ep20_assets.py credits [--write] # 画面の出典 ref/ep20/credits.json と ref/CREDITS.md の20本目の節
  python qa_out/ep20_assets.py shots            # ref/ep20/shots.json（防衛庁記録のショット＝bv_shots20.tsv から）
  python qa_out/ep20_assets.py clips            # ref/ep20/clips.json（防衛庁記録の台帳）
  python qa_out/ep20_assets.py use              # tools/footage.py の EP20_USE の欄（手で書かない）
  python qa_out/ep20_assets.py fb [c103 …]      # 映像のひかえの静止画 ref/ep20/fb_<cid>.jpg（手元の YouTube 版の1コマ・黒帯を外した中身）

入力＝映像方針の一覧 `ref/ep20/eizou_build/list20.tsv`（生成物・秒は narration.json の実測）・出どころ `sources20.tsv`・取得の記録 `fetch20.tsv`・
報告書の写真と付図＝旧版の取り出し `ref/ja123/`（PDL1.0・長辺1200・1ビットのスキャンを縮小＋ぼかし0.7＝`ref/ja123/INDEX.md`）。
🔴 報告書の写真は**束へ写すだけ**（切らない・色を変えない＝白黒のまま）。額装になるのは幅が 1280 未満だから（`ss.kind`）。
🔴 額装だけの点＝BY-SA の2点（J2・J3）と、引用の写真-124（地上の第三者の撮影＝c408 だけ）＝`frame=True`（`ss.frame_only`）。
⚠️ 文字の頁（PG＝c211・c813・c907・ca04・ca18・cc06）の切り口（pages.json）はここではまだ作らない＝⑤b-7（頁のチャット）。
"""
import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
EPD = HERE / "ref" / "ep20"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list20.tsv"
SOURCES = BUILD / "sources20.tsv"
FETCH = BUILD / "fetch20.tsv"
BV_SHOTS = BUILD / "bv_shots20.tsv"
JA = HERE / "ref" / "ja123"
DB = EPD / "assets.json"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
FOOTAGE = HERE / "tools" / "footage.py"
BV_LOCAL = EPD / "src" / "bouei60" / "bouei60_full_399.mp4"
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## 日本航空123便のリメイク（1985-08-12・20本目）"
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（12本目の教訓＝footage.py の注）

# 報告書の素材の記号 → 旧版の取り出しの名（make_list20.resolve と同じ当て方）
_JA_PATS = [(r"P(\d+)$", "p%03d", "写真-%d"), (r"A1P(\d+)$", "a1p%03d", "別添1 写真-%d"),
            (r"F(\d+)$", "f%03d", "付図-%d"), (r"A1F(\d+)$", "a1f%03d", "別添1 付図-%d")]
CR_JTSB = "出典：運輸安全委員会 航空事故調査報告書 62-2（JA8119）"
CR_KAI = "出典：運輸安全委員会 事故調査報告書についての解説（62-2 JA8119）"
# 🔴 引用（第三者の写真）＝額装・無加工・この1カットだけ（映像方針 §1 と list20 の c408 の注）
QUOTE = {"P124": "地上の第三者の撮影（報告書に名前の表記なし）＝引用（額装・無加工・c408 だけ・冒頭とサムネに使わない）"}

# Commons の写真（取得ずみ）の画面の出典。🔴 CC BY（継承なし）は額・寄り・流しで端を切ることがある＝「改変：切出」を書く
#   （`scene_jiko.credit_of` は「改変」の無い CC BY に「色調変更・切出」を足す＝20本目は原色なので、こちらで正しく書いておく）。
#   BY-SA は額装・無加工・色そのまま＝「改変なし」。撮影者は sources20.tsv の credit の頭
SCREEN = {
    "J1": "出典：Dennis HKG（Flickr）／CC BY 2.0／改変：切出",
    "J2": "出典：Stuart Jessup（Flickr）／CC BY-SA 2.0／改変なし",
    "J3": "出典：Harcmac60（Wikimedia Commons）／CC BY-SA 3.0／改変なし",
    **{f"O{i}": "出典：daipresents（Panoramio）／CC BY 3.0／改変：切出" for i in range(1, 7)},
}
WHO = {"J1": "Dennis HKG（Flickr）", "J2": "Stuart Jessup（Flickr）", "J3": "Harcmac60（Wikimedia Commons）",
       **{f"O{i}": "daipresents（Panoramio）" for i in range(1, 7)}}
LIC = {"J1": "CC BY 2.0", "J2": "CC BY-SA 2.0", "J3": "CC BY-SA 3.0", **{f"O{i}": "CC BY 3.0" for i in range(1, 7)}}


# 🆕 ⑤b-7（2026-10-11）：顔だけモザイク（ルール §B2-2b・2026-09-30 カズヤくん「顔面のみのモザイク加工」＝PD・CC BY・報告書の PDL1.0
#   は手直しを許す）。範囲＝束の画素 (x0, y0, x1, y1, 誰)＝⑤b-7 に4倍の拡大と10px の目盛りで読んだ（scratchpad `p014_face.jpg`）。
#   写真-14（c310）＝回収した APU のダクトのそばの白いシャツの男性（制服が無く、公的な任務の人か写真から決められない）。左右の人は頭が
#   枠の外＝かけない。元画像そのものを直す＝`cuts/ss.py` の NEEDS_MASK・`ref/ep20/masked.json`（check_photo_mask --record）
MOSAIC_PX = {"p014": 10}        # 升の大きさ（束の画素）。顔の幅 約65px＝6〜7升＝見分けられない
MASK = {
    "p014": [(778, 45, 852, 145, "白いシャツの男性")],
}


# 🆕 ⑤c'（2026-10-11）：頁から切り直す点。旧版の取り出し（tools/extract_photos.py の clip_text）は、図の右上の題（文字の層）を避けて
#   **右の辺を題の左まで詰めた**＝付図-28 の凡例「山中より回収した残骸」「海上より回収した残骸」と注が「した残」で切れていた
#   （⑤c 原寸・OCR の箱が素材の右端 x=1200 に接する行＝全素材で f028 だけ）。→ 頁を同じ倍率で描き、題の3行（絵のインクの行の帯で
#   求めた箱＝文字の層の座標は使わない）だけを白で消し、インクの外接で切る。縮小・ぼかしは旧版と同じ（長辺1200・0.7・quality 88）
RECUT = {
    "f028": dict(pdf="ref/ep20/src/ja_05.pdf", page=29, zoom=5.05,
                 # 題「付図‐２８」「垂直尾翼損壊図（右側）」「（右側）」の3行・左の頁の番号（164）。2行目の頭「垂直尾」は x 2573 から
                 # （その左 x 2308〜2456 の塊は図の帯の先＝消さない）＝インクの塊（scipy.ndimage.label）で読んだ箱
                 blank=[(2506, 326, 3005, 386), (2566, 416, 3675, 490), (3082, 516, 3367, 572), (360, 1424, 424, 1520)]),
}


def recut(name, dst):
    """RECUT の点を頁から切り直して dst へ（白黒）。返り値＝(w, h, 元の pdf の md5)"""
    import fitz
    import numpy as np
    from PIL import Image, ImageDraw, ImageFilter
    r = RECUT[name]
    pdf = HERE / r["pdf"]
    pg = fitz.open(pdf)[r["page"] - 1]
    pg.set_rotation(0)
    pm = pg.get_pixmap(matrix=fitz.Matrix(r["zoom"], r["zoom"]), colorspace=fitz.csGRAY)
    im = Image.frombytes("L", (pm.width, pm.height), pm.samples)
    dr = ImageDraw.Draw(im)
    for b in r["blank"]:
        dr.rectangle(b, fill=255)
    ys, xs = np.where(np.asarray(im) < 128)
    m = 12
    im = im.crop((max(0, xs.min() - m), max(0, ys.min() - m), min(im.width, xs.max() + m + 1), min(im.height, ys.max() + m + 1)))
    im.thumbnail((1200, 1200), Image.LANCZOS)
    im.filter(ImageFilter.GaussianBlur(0.7)).save(dst, quality=88, optimize=True)
    return im.width, im.height, md5(pdf)


def mosaic(im, boxes, n):
    """顔の範囲だけを升目にする（縮めて NEAREST で戻す）＝16本目 `qa_out/ep16_assets.py` と同じ式"""
    from PIL import Image
    for x0, y0, x1, y1, _ in boxes:
        reg = im.crop((x0, y0, x1, y1))
        small = reg.resize((max(1, reg.width // n), max(1, reg.height // n)), Image.BOX)
        im.paste(small.resize(reg.size, Image.NEAREST), (x0, y0))
    return im


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _list():
    return list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))


def _sources():
    out = {}
    for ln in SOURCES.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if len(f) >= 10 and not ln.startswith("#") and f[0] not in ("code", ""):
            out[f[0]] = dict(zip(["code", "class", "file", "page", "media", "dims", "dur", "mb", "rights", "credit", "note"], f))
    return out


def _fetched():
    out = {}
    for ln in FETCH.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if len(f) >= 9 and not ln.startswith("#") and f[0] != "code":
            out[f[0]] = dict(zip(["code", "class", "file", "bytes", "md5", "md5_check", "dims", "exif", "page"], f))
    return out


def codes_of(main):
    """一覧の素材の欄（「P15」「BV@1439.0-1446.7+BV@…」「K-kz018」）→ 記号の並び。"""
    return [p.strip().split("@")[0] for p in (main or "").split("+") if p.strip()]


def ja_of(code):
    """報告書の記号 → (束の名, 旧版のファイル, 画面の出典)。当たらなければ None。"""
    for pat, fn, cap in _JA_PATS:
        m = re.match(pat, code)
        if m:
            n = int(m.group(1))
            name = fn % n
            cr = f"{CR_JTSB}{cap % n}／縮小・切出"
            if code in QUOTE:
                cr = f"{CR_JTSB}{cap % n}／縮小（引用）"
            return name, JA / f"{name}.jpg", cr
    m = re.match(r"K-k([zh])(\d{3})$", code)
    if m:
        name = f"k{m.group(1)}{m.group(2)}"
        return name, JA / f"{name}.png", f"{CR_KAI}{'図' if m.group(1) == 'z' else '表'}{int(m.group(2))}／切出"
    return None


def uses():
    """{記号: [カット]}（一覧の素材の欄から・PG と模式・再現は除く）。"""
    out = {}
    for r in _list():
        for c in codes_of(r["main"]):
            if c in ("PG", "模式") or re.fullmatch(r"S\d", c):
                continue
            out.setdefault(c, []).append(r["cid"])
    return out


# ── 写真の束 ───────────────────────────────────────────────
def cmd_build():
    from PIL import Image
    src, fe = _sources(), _fetched()
    db = {}
    bad = 0
    for code, cuts in sorted(uses().items()):
        if code == "BV":
            continue
        if code in src:                      # Commons の写真（J・O）
            s, f = src[code], fe.get(code)
            sp = HERE / s["file"]
            if not f or not sp.exists():
                print(f"🔴 {code}: fetch20.tsv の行か手元のファイルが無い")
                bad += 1
                continue
            if md5(sp) != f["md5"]:
                print(f"🔴 {code}: {sp.name} の md5 が取得のときと違う（取り直す）")
                bad += 1
                continue
            name = sp.stem
            dst = EPD / f"{name}.jpg"
            shutil.copyfile(sp, dst)
            with Image.open(dst) as im:
                w, h = im.size
            lic = LIC[code]
            gm = re.search(r"（(.*)）$", s["rights"])          # 権利の欄の括弧の中＝根拠（「Flickr の審査ずみ」など）
            db[name] = dict(code=code, file=s["file"], cut=" ".join(cuts), credit=SCREEN[code], who=WHO[code],
                            note=s["note"][:200], box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h,
                            md5=md5(dst), src_md5=f["md5"], lic=lic, frame=False,
                            ground=gm.group(1) if gm else "Wikimedia Commons", url=s["page"], blur=[])
            print(f"✓ {code:7} {name:30} {w}x{h}  {' '.join(cuts)}  {lic}")
            continue
        ja = ja_of(code)
        if not ja:
            print(f"🔴 {code}: 出どころが決まらない（sources20.tsv にも報告書の記号にも当たらない）")
            bad += 1
            continue
        name, sp, cr = ja
        if name in RECUT:                    # 頁から切り直す（上の RECUT）
            dst = EPD / f"{name}.jpg"
            w, h, pmd5 = recut(name, dst)
            r = RECUT[name]
            db[name] = dict(code=code, file=f"{r['pdf']}#p{r['page']}", cut=" ".join(cuts), credit=cr,
                            who="運輸安全委員会（報告書 62-2・昭和62年）",
                            note="頁から切り直し（旧版の取り出しは凡例が右の辺で切れていた・題を外した・縮小・ぼかし0.7）",
                            box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h, md5=md5(dst), src_md5=pmd5,
                            lic="PDL1.0", frame=False, ground="運輸安全委員会 公共データ利用規約",
                            url="https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html", blur=[])
            print(f"✓ {code:7} {name:30} {w}x{h}  {' '.join(cuts)}  PDL1.0  頁から切り直し")
            continue
        if not sp.exists():
            print(f"🔴 {code}: {sp.relative_to(HERE).as_posix()} が無い")
            bad += 1
            continue
        dst = EPD / f"{name}.jpg"
        with Image.open(sp) as im0:
            im = im0.convert("L")            # 白黒のまま（1ビットのスキャンの縮小＝灰色）。png の解説の図も jpg の束へ
            w, h = im.size
            if name in MASK:
                mosaic(im, MASK[name], MOSAIC_PX[name]).save(dst, quality=94)     # 顔だけモザイク（上の MASK）
                cr = cr.replace("／縮小・切出", "／縮小・切出・顔にモザイク")
            elif sp.suffix == ".jpg":
                shutil.copyfile(sp, dst)     # 写すだけ（再圧縮しない）
            else:
                im.save(dst, quality=94)
        frame = code in QUOTE
        db[name] = dict(code=code, file=sp.relative_to(HERE).as_posix(), cut=" ".join(cuts), credit=cr,
                        who="第三者（地上の撮影者・報告書に名前の表記なし）" if frame else "運輸安全委員会（報告書 62-2・昭和62年）",
                        note=QUOTE.get(code, "旧版の取り出し（縮小・ぼかし0.7・頁から切出＝ref/ja123/INDEX.md）"),
                        box=[0.0, 0.0, 1.0, 1.0], crop_px=[0, 0, w, h], w=w, h=h, md5=md5(dst), src_md5=md5(sp),
                        lic="引用（報告書の写真-124）" if frame else "PDL1.0", frame=frame,
                        ground="著作権法32条・第三者の写真" if frame else "運輸安全委員会 公共データ利用規約",
                        url="https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html", blur=[])
        if name in MASK:
            db[name]["mosaic"] = [list(b) for b in MASK[name]]
        print(f"✓ {code:7} {name:30} {w}x{h}  {' '.join(cuts)}  {db[name]['lic']}{'  額装だけ（引用）' if frame else ''}"
              f"{f'  顔のモザイク {len(MASK[name])}か所' if name in MASK else ''}")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep20/assets.json（{len(db)}点・額装だけ {sum(1 for r in db.values() if r['frame'] or 'SA' in r['lic'])}）")
    return 1 if bad else 0


def cmd_panel():
    """ルール 0b-34②：PANEL_AR＝束の縦横比の並びで、16:9 より縦長の側のいちばん大きな切れ目の中点。"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    ars = sorted((r["w"] / r["h"], n, r["w"]) for n, r in db.items())
    for a, n, w in ars:
        print(f"  {a:6.3f}  {n:30} 幅 {w}")
    side = [x for x in ars if x[0] < 16 / 9]
    gaps = sorted(((side[i + 1][0] - side[i][0], side[i], side[i + 1]) for i in range(len(side) - 1)), reverse=True)
    for g, a, b in gaps[:4]:
        print(f"切れ目 {g * 100:5.1f}ポイント：{a[0]:.3f}（{a[1]}）→ {b[0]:.3f}（{b[1]}）＝中点 {(a[0] + b[0]) / 2:.4f}")
    return 0


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
def cmd_credits(write=False):
    """撮影年＝その写真を当てたカットの list20 の副題の年（16〜19本目と同じ決め方）。副題に年の無い写真は「不明」（副題も年を名乗らない）"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    cj, rows = {}, []
    for n, r in sorted(db.items()):
        cuts = r["cut"].split()
        ys = sorted({m.group(1) for c in cuts for m in re.finditer(r"(1[89]\d\d|20\d\d)年", subs.get(c, ""))})
        if len(ys) > 1:
            raise SystemExit(f"🔴 {n}: 当てたカットの副題で年が割れる（{ys}）")
        cj[f"ep20/{n}.jpg"] = r["credit"]
        rows.append(f"| `{n}` | {' '.join(cuts)} | {ys[0] if ys else '不明'} | {r['lic']}（{r['ground']}） | {r['who']} | {r['url']} |")
    # 🆕 ⑤b-7：文字の頁（pages.json）＝出典の行は資料の名と頁（`illu.rec_line`＝図のカットの出典と同じ書き方・`ss.REC_DOCS`）
    sys.path.insert(0, str(HERE / "tools"))
    import illu
    pages = json.loads(PAGES_JSON.read_text(encoding="utf-8")) if PAGES_JSON.exists() else {}
    PAGE_YEAR = {"報告書": 1987, "勧告": 1987, "解説はじめに": 2011}
    for k, p in sorted(pages.items()):
        line = illu.rec_line([p["rec"]])
        if not line:
            raise SystemExit(f"🔴 {k} の出典の行が作れない（`cuts/ss.REC_DOCS` に資料が無い）")
        cj[f"ep20/{k}.png"] = line + "／切出"
        doc = p["rec"].split()[0]
        rows.append(f"| `{k}` | {' '.join(sorted(p.get('cuts', {})))} | {PAGE_YEAR[doc]} | PDL1.0（運輸安全委員会 公共データ利用規約） | "
                    f"運輸安全委員会 | {p['pdf']} PDF {p['pdf_page']}頁 |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真 {len(db)}点")
    if not write:
        return 0
    CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    md = CREDITS_MD.read_text(encoding="utf-8")
    block = "\n".join([
        CREDITS_HEAD, "",
        "※2026-10-08（⑤b-2）。`qa_out/ep20_assets.py credits --write` が書く（手で直さない）。旧版の節は上の"
        "「日本航空123便（1985-08-12・JA8119）　※本番2本目」＝直さない（旧版は 10-05 に非公開）。",
        "",
        "### 0. 防衛庁記録（動く映像）",
        "- 防衛省・自衛隊『昭和60年防衛庁記録』（公式 YouTube modchannel・https://www.youtube.com/watch?v=LKrLJc4R0X8）＝"
        "頁の表示「クリエイティブ・コモンズ 著作権表示必須ライセンス」＝**CC BY 3.0**。焼くときの媒体は Wikimedia Commons の同じ映画"
        "（File:昭和６０年防衛庁記録.webm の 1080p 版）・手元の走査は YouTube の 1080p。",
        "- 使う区間＝c103（上空から見た墜落現場）・c104（ヘリの遠景）・c107（まつゆきのボートの前半）・c503（指揮所＋F-4〈昼の離陸〉）・"
        "c601（海の尾翼＋ボートの後半）＝`ref/ep20/eizou_build/bv_shots20.tsv`。改変＝切り出し（4:3 の中身だけ）・額装・再生速度・音なし",
        "- 🔴 使わない区間（`tools/footage.py` の NOGO）：新聞の切り抜き（第三者の著作物）・生存者の救出の寄り・担架と捜索・報道陣の顔",
        "",
        "### 1. 写真（報告書 62-2＝PDL1.0／JA8119 の3点＝CC BY 2.0・CC BY-SA 2.0・3.0／御巣鷹の尾根と慰霊の6点＝CC BY 3.0）",
        "- 報告書の写真・付図＝`ref/ja123/`（旧版の取り出し・縮小・ぼかし0.7・頁から切出）を束へ写した＝白黒のまま。PDL1.0 の条件＝出典と加工した旨"
        "（画面の出典「／縮小・切出」）",
        "- 🔴 **CC BY-SA の2点（J2・J3）は額装・無加工・色そのまま・上に重ねない・1点1カット**（`cuts/ss.check_frame_only`）。動きは額ごと（絵は切らない）",
        "- 🔴 **写真-124（c408）は地上の第三者の撮影＝引用**（額装・無加工・この1カットだけ・冒頭とサムネに使わない）",
        "- 🆕 写真-14（c310）の白いシャツの男性（制服が無く公的な任務の人か写真から決められない）は**顔だけモザイク**（2026-09-30 カズヤくん"
        "「顔面のみのモザイク加工」＝PDL1.0 は手直しを許す・元画像を直す＝`cuts/ss.py` の NEEDS_MASK・`ref/ep20/masked.json`）＝画面の出典に「顔にモザイク」",
        "- CC BY（J1・O1〜O6）は額・寄り・流しで端を切ることがある＝画面の出典に「改変：切出」。20本目は写真を原色で出す（色は変えない）",
        "- 撮影年＝映像方針で書いた副題の年（JA8119＝写真の題・daipresents の6点＝EXIF 2009-08-14 の朝）。副題に年の無い写真は「不明」",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, ""])
    if CREDITS_HEAD in md:
        pre, rest = md.split(CREDITS_HEAD, 1)
        nxt = rest.find("\n## ")
        md = pre + block + (rest[nxt:] if nxt >= 0 else "")
    else:
        md = md.rstrip("\n") + "\n\n" + block
    CREDITS_MD.write_text(md, encoding="utf-8")
    print(f"→ {CREDITS_JSON.relative_to(HERE).as_posix()} ／ {CREDITS_MD.relative_to(HERE).as_posix()}")
    return 0


# ── 文字の頁（⑤b-7・2026-10-11）──────────────────────────────
#   頁の画像 ref/ep20/pg<N>.png（灰色・200dpi）と切り口・寄りの縦の寄せ・頁の上の印 ref/ep20/pages.json（`ss.page`・`ss.ptrim`・
#   `ss.pbias`・`ss.phl`）。切り口の上下と bias は 18本目の `_fit_cut`（寄りの縮みを上下のすき間で受ける）をそのまま使う。
#   🔴 報告書の頁は「スキャンの絵＋OCR の文字の層」（ArialMT・見えない字）＝文字の層の座標は絵とずれることがある
#      （記憶 feedback-ocr-text-layer-is-not-the-picture）＝**目印の行は文字の層で探し、縦の位置は頁の絵の字の帯（インク）に当てる**
#      （行の中心から 0.012 以内に帯が無ければ止める）。印の横の位置は、行の文字の層の左右の端を、その帯のインクの左右の端へ
#      線形に写す（ずれを行ごとに打ち消す）。解説（2011年）は本物の字（文字の層＝絵）
#   頁の番号（`ss.page(N)` の N）＝報告書は印刷の頁・解説の「はじめに」p.i は 2001・勧告第1号（ja_01 の PDF 4頁）は 3004
#   （どれも `cuts.ss.REC_DOCS` の書き方「資料 p頁」＝出典の行）
PAGES_JSON = EPD / "pages.json"
PAGE_DPI = 200
PANEL_AR_T = 1120 / 648        # 額の最大の箱（`scene_jiko.PANEL_MAXW × PANEL_MAXH`）の縦横比＝18本目と同じ目標
COLS = (0.08, 0.95)            # 字を探す横の範囲（頁の幅の割合）。報告書の頁の字は x 0.11〜0.90
PAGE_SRC = {    # 頁 → (PDF, PDF の頁, 出典の書き方, 回す角度＝PIL の rotate の度・反時計回り)
    102: ("ja_04.pdf", 2, "報告書 p102", 0),
    125: ("ja_04.pdf", 25, "報告書 p125", 0),
    126: ("ja_04.pdf", 26, "報告書 p126", 0),
    311: ("ja_11.pdf", 45, "報告書 p311", None),     # 別添6 CVR 記録の最初の頁＝横倒しの表（文字の層なし）。向きは PAGE_ROT311
    2001: ("jtsb_kaisetsu.pdf", 1, "解説はじめに p1", 0),
    3004: ("ja_01.pdf", 4, "勧告 p4", 0),
}
PAGE_ROT311 = 270              # 🔴 頁の絵で決めた向き（⑤b-7 の確かめのシート：90 では字が逆さま＝270＝時計回りに90度）
# カット → (頁, 始めの目印, 終わりの目印)。目印＝文字の層の行の字を空白を除いてつないだ並びへの部分一致（1か所だけ・行をまたいでよい）。
#   None＝頁の字のある所まるごと（c211＝CVR の表・言葉の行には寄らない＝額ごと寄る）
PAGE_CUTS = {
    "c211": (311, None, None),
    # p102＝3.2.2(1)(オ)「実際の修正作業では…なお、このような作業が行われたという記録はない。」（台本 c813 の引用）
    "c813": (102, "（オ）実際の修正作業では", "このような作業が行われたという記録はない。"),
    # p125＝4.1.5.4 の後半「しかしながら…点検方法に十分とはいえない点があったためと考えられる。」（c907 の引用）
    "c907": (125, "しかしながら、今回の場合のように", "えない点があったためと考えられる。"),
    # p126＝4.1.7.2「…運航乗務員は最後まで酸素マスクを着用しなかったものと推定されるが、その理由を明らかにすることはできなかった。」
    #   ⚠️ 「その理由を明らかにすることはできなかった。」は 4.1.7.3 にもある＝終わりの目印は「推定されるが、」から
    "ca18": (126, "4.1.7.2", "推定されるが、その理由を明らかにすることはできなかった。"),
    # 解説 p.i＝題と「はじめに」の頭〜おわびの文（ca04＝2011年の解説を名指し・おわびのうえで）
    "ca04": (2001, "日本航空123便の御巣鷹山墜落事故に係る", "率直にお詫び申し上げます。"),
    # 勧告第1号（PDF 4頁）＝1．と 2．（cc06 の語り＝1つ目・2つ目）。3．は語りに無い＝入れない
    "cc06": (3004, "1．航空事故による損傷", "継続監視するよう、指導の徹底を図ること。"),
}
# 頁の上の印（蛍光ペン＝語りと同時に塗る）：カット → [(頁の上の句, 字幕の行, 字幕の中の句)]。句はどちらも原文の字のまま
#   （頁の句＝文字の層の並び・空白を除く／字幕の句＝narration.json の字幕の行）。塗る秒＝字幕の句の位置の割合（`scene_jiko.hl_times`）
PAGE_HL = {
    "c813": [("このような作業が行われたという記録はない", 1, "このような作業が行われたという記録はない")],
    "c907": [("点検方法に十分とはいえない点があったため", 1, "点検方法に十分とはいえない点があったため")],
    #   「《」より前＝当てるための手がかり（塗らない）。「明らかにすることはできなかった」は 4.1.7.3 にもある
    "ca18": [("運航乗務員は最後まで酸素マスクを着用しなかったものと推定される", 1, "乗員は最後まで酸素マスクを着けなかったと推定している"),
             ("推定されるが、その理由を《明らかにすることはできなかった", 2, "明らかにすることはできなかった")],
    "ca04": [("ご遺族の皆さまに対して、必ずしも十分な説明がなされていなかった", 1, "遺族への説明が足りなかった"),
             ("率直にお詫び申し上げます", 1, "おわびした")],
    "cc06": [("修理作業の計画及び作業管理を、状況に応じ特に慎重に", 0, "計画と管理を状況に応じ特に慎重に"),
             ("その部位について特別の点検項目を設け継続監視するよう", 1, "特別な点検の項目を設けて、見守り続ける")],
}


def _norm_ja(s):
    return re.sub(r"[\s　•]", "", s)


def _rows_ja(page):
    """文字の層の行＝[dict(t＝空白を除いた字, y0, y1, x0, x1, ch＝[(字, x0, x1)])]（頁の割合・上から）。同じ高さの行はまとめる"""
    H, W = page.rect.height, page.rect.width
    segs = []
    for b in page.get_text("rawdict")["blocks"]:
        if b.get("type") != 0:
            continue
        for ln in b["lines"]:
            ch = [(c["c"], c["bbox"][0] / W, c["bbox"][2] / W) for s in ln["spans"] for c in s["chars"] if _norm_ja(c["c"])]
            if ch:
                x0, y0, x1, y1 = ln["bbox"]
                segs.append(dict(y0=y0 / H, y1=y1 / H, ch=ch))
    segs.sort(key=lambda s: (s["y0"] + s["y1"]) / 2)
    rows = []
    for s in segs:
        c = (s["y0"] + s["y1"]) / 2
        if rows and abs(c - (rows[-1]["y0"] + rows[-1]["y1"]) / 2) < 0.45 * (s["y1"] - s["y0"]):
            r = rows[-1]
            r["ch"] += s["ch"]
            r["y0"], r["y1"] = min(r["y0"], s["y0"]), max(r["y1"], s["y1"])
        else:
            rows.append(dict(y0=s["y0"], y1=s["y1"], ch=list(s["ch"])))
    for r in rows:
        r["ch"].sort(key=lambda c: c[1])
        r["t"] = "".join(c[0] for c in r["ch"])
        r["x0"], r["x1"] = r["ch"][0][1], r["ch"][-1][2]
    return rows


def _find_ja(rows, anchor, pr):
    """句の最初と最後の字の (行, 行の中の字の番号)。1か所でなければ止める（黙って別の所を切らない）"""
    joined, owner = "", []
    for i, r in enumerate(rows):
        joined += r["t"]
        owner += [(i, k) for k in range(len(r["t"]))]
    a = _norm_ja(anchor)
    ks = [m.start() for m in re.finditer(re.escape(a), joined)]
    if len(ks) != 1:
        raise SystemExit(f"🔴 p{pr}：句「{anchor}」が {len(ks)} か所＝1か所でないと切らない")
    return owner[ks[0]], owner[ks[0] + len(a) - 1]


def _band_of(bands, r, pr):
    c = (r["y0"] + r["y1"]) / 2
    k = min(range(len(bands)), key=lambda i: abs((bands[i][0] + bands[i][1]) / 2 - c))
    if not bands[k][0] - 0.012 <= c <= bands[k][1] + 0.012:
        raise SystemExit(f"🔴 p{pr}：文字の層の行（y {c:.4f}）に近い字の帯が無い（文字の層が絵とずれている？）")
    return k


def _page_img(pr):
    """頁を灰色 200dpi に焼いて (np 配列, 頁の幅 pt) を返す（p311 は正立させる）"""
    import fitz
    import numpy as np
    from PIL import Image
    fn, pno, _, rot = PAGE_SRC[pr]
    with fitz.open(EPD / "src" / fn) as d:
        pg = d[pno - 1]
        pix = pg.get_pixmap(dpi=PAGE_DPI, colorspace=fitz.csGRAY)
        im = Image.frombytes("L", (pix.width, pix.height), pix.samples)
        wpt, hpt = pg.rect.width, pg.rect.height
    if rot is None:
        im = im.rotate(PAGE_ROT311, expand=True)
        wpt = hpt
    return im, np.asarray(im), wpt


def cmd_pages(only=None):
    """`pages` は全頁。`pages 102` のように頁を書けばその頁だけ焼き直す。印（hl）は字幕（narration.json）の句の位置から"""
    import fitz
    sys.path.insert(0, str(HERE / "qa_out"))
    import ep18_assets as E18
    subs = json.loads((HERE / "audio" / "narration.json").read_text(encoding="utf-8"))["subtitles"]
    pj = json.loads(PAGES_JSON.read_text(encoding="utf-8")) if PAGES_JSON.exists() else {}
    for pr, (fn, pno, rec, rot) in PAGE_SRC.items():
        if only and pr not in only:
            continue
        out = EPD / f"pg{pr}.png"
        im, a, wpt = _page_img(pr)
        im.save(out)
        Hp, Wp = a.shape
        cuts, biases, hls = {}, {}, {}
        for cid, (p2, a_from, a_to) in PAGE_CUTS.items():
            if p2 != pr:
                continue
            if a_from is None:
                # 頁の字のある所まるごと（表）＝インクの外枠＋12pt。寄らない（額ごと寄る）ので bias は 0.5
                bands = E18._bands(a, 0.03, 0.97)
                top, bot = bands[0][0] - E18.END_PAD, bands[-1][1] + E18.END_PAD
                x0, x1 = E18._ink_x(a, top, bot, 0.03, 0.97)
                pad = 12 / wpt
                box = [round(float(v), 4) for v in (max(0.0, x0 - pad), max(0.0, top), min(1.0, x1 + pad), min(1.0, bot))]
                cuts[cid], biases[cid] = box, 0.5
                print(f"✓ pg{pr} {cid}  trim={box}  頁まるごと（帯 {len(bands)}）")
                continue
            with fitz.open(EPD / "src" / fn) as d:
                rows = _rows_ja(d[pno - 1])
                scan = bool(d[pno - 1].get_images())    # スキャンの絵がある頁＝文字の層は OCR（見えない字）
            # 字のある範囲＝インクの帯＋文字の層の行の芯（上下 7% ずつ縮めた箱＝18本目の OCR の行と同じ扱い）。
            #   ⚠️ インクの帯だけだと、字の少ない短い行（p102「録はない。」＝5字）は帯が細く取れた（y 0.4882〜0.4925＝9画素・
            #   横の投影がしきい値に届かない）＝印の箱も薄くなった（⑤b-7 の1回目）。
            #   芯を足す前に、文字の層の行の中心と、いちばん近いインクの帯の中心の差を測って出す（0.006＝行間の約1/4 を超えたら止める）。
            #   測るのは15字以上の行だけ（短い行はインクの帯そのものが取れず、となりの行の帯と比べてしまう＝p102 で 0.0235＝1行ぶん）
            ink = E18._bands(a, *COLS)
            core = [(r["y0"] + 0.07 * (r["y1"] - r["y0"]), r["y1"] - 0.07 * (r["y1"] - r["y0"])) for r in rows
                    if COLS[0] <= (r["x0"] + r["x1"]) / 2 < COLS[1]]
            offs = [min(abs((b[0] + b[1]) / 2 - (r["y0"] + r["y1"]) / 2) for b in ink) for r in rows
                    if len(r["t"]) >= 15 and COLS[0] <= (r["x0"] + r["x1"]) / 2 < COLS[1]]
            print(f"  pg{pr} {cid}：文字の層の行 {len(core)}・インクの帯の中心との差 最大 {max(offs):.4f}・中央 {sorted(offs)[len(offs) // 2]:.4f}")
            if max(offs) > 0.006:
                raise SystemExit(f"🔴 p{pr}：文字の層の行が頁の絵の字の帯とずれている（最大 {max(offs):.4f}）＝芯を足さない")
            bands = E18._occupied(ink, core)
            (r0, _), _ = _find_ja(rows, a_from, pr)
            _, (r1, _) = _find_ja(rows, a_to, pr)
            j0, j1 = _band_of(bands, rows[r0], pr), _band_of(bands, rows[r1], pr)
            x0, x1 = E18._ink_x(a, bands[max(0, j0 - 4)][0], bands[min(len(bands) - 1, j1 + 4)][1], *COLS)
            x0, x1 = max(0.0, x0 - 10 / wpt), min(1.0, x1 + 10 / wpt)
            want = (x1 - x0) * Wp / PANEL_AR_T / Hp
            j0, j1, top, bot, bias = E18._fit_cut(bands, j0, j1, 0, len(bands) - 1, 1 / Hp, want)
            x0, x1 = E18._ink_x(a, top, bot, *COLS)
            x0, x1 = max(0.0, x0 - 10 / wpt), min(1.0, x1 + 10 / wpt)
            box = [round(float(v), 4) for v in (x0, max(0.0, top), x1, min(1.0, bot))]
            cuts[cid], biases[cid] = box, bias
            print(f"✓ pg{pr} {cid}  trim={box}  帯 {j0}〜{j1}  bias={bias}  縦横比 {round((box[2] - box[0]) * Wp / ((box[3] - box[1]) * Hp), 2)}")
            # 頁の上の印＝句の行ごとの箱（縦＝その行のインクの帯・横＝文字の層の字の位置を帯のインクの左右の端へ写す）
            out_hl = []
            for ph, k, sp in PAGE_HL.get(cid, []):
                (ra, ka), (rb, kb) = _find_ja(rows, ph.replace("《", ""), pr)
                if "《" in ph:              # 手がかりの字のぶんだけ、塗り始めを後ろへ送る
                    for _ in range(len(_norm_ja(ph.split("《")[0]))):
                        ka += 1
                        if ka >= len(rows[ra]["t"]):
                            ra, ka = ra + 1, 0
                line = subs[cid][k]["text"]
                m = line.find(sp)
                if m < 0:
                    raise SystemExit(f"🔴 {cid}：字幕の {k} 行目に句「{sp}」が無い（{line}）")
                f0, f1 = m / len(line), (m + len(sp)) / len(line)
                segs = [(r, ka if r == ra else 0, kb if r == rb else len(rows[r]["t"]) - 1) for r in range(ra, rb + 1)]
                n_all = sum(e - s + 1 for _, s, e in segs)
                acc = 0
                for r, s, e in segs:
                    b = bands[_band_of(bands, rows[r], pr)]
                    ix0, ix1 = E18._ink_x(a, b[0], b[1], *COLS)
                    tx0, tx1 = rows[r]["x0"], rows[r]["x1"]
                    if not scan:
                        # 本物の字の頁（解説）＝文字の層が絵そのもの＝写さない（写すと「申し上げます」の「す」が半分外れた＝⑤b-7）
                        ix0, ix1 = tx0, tx1
                    sx = (ix1 - ix0) / max(1e-6, tx1 - tx0)
                    cx0 = ix0 + (rows[r]["ch"][s][1] - tx0) * sx
                    cx1 = ix0 + (rows[r]["ch"][e][2] - tx0) * sx
                    g0 = f0 + (f1 - f0) * acc / n_all
                    acc += e - s + 1
                    g1 = f0 + (f1 - f0) * acc / n_all
                    if not (box[1] <= b[0] and b[1] <= box[3]):
                        raise SystemExit(f"🔴 {cid}：印の行（y {b[0]:.4f}〜{b[1]:.4f}）が切り口の外")
                    out_hl.append([k, round(g0, 3), round(g1, 3), [round(float(cx0), 4), round(float(b[0]), 4),
                                                                   round(float(cx1), 4), round(float(b[1]), 4)]])
            if out_hl:
                hls[cid] = out_hl
                for h in out_hl:
                    print(f"    印 {h}")
        pj[f"pg{pr}"] = dict(rec=rec, pdf=fn, pdf_page=pno, rot=(PAGE_ROT311 if rot is None else rot), w=Wp, h=Hp, dpi=PAGE_DPI,
                             md5=md5(out), cuts=cuts, bias=biases, hl=hls)
        print(f"  pg{pr}  {fn} PDF {pno}頁  {Wp}x{Hp}")
    PAGES_JSON.write_text(json.dumps(pj, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {PAGES_JSON.relative_to(HERE).as_posix()}（{len(pj)}頁）")
    return 0


# ── 防衛庁記録（ショット・台帳・USE・ひかえ） ───────────────────
def _bv_rows():
    out = []
    for ln in BV_SHOTS.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if ln.startswith("#") or len(f) < 7 or f[0] == "shot":
            continue
        out.append(dict(shot=f[0], start=float(f[1]), until=float(f[2]), what=f[3], use=f[5], why=f[6]))
    return out


def cmd_shots():
    """shots.json＝映像方針で1秒1コマ＋scene で決めた境目（bv_shots20.tsv）。footage の門番（outside_shot・unknown_clip）が読む。
    ⚠️ 表は 23:51.9〜25:46.7 だけ（使う区間の前後）＝この外の秒を USE に書けば outside_shot が止める（fail closed）"""
    rows = _bv_rows()
    sd = {"BV": dict(src="昭和60年防衛庁記録（YouTube LKrLJc4R0X8 の 1080p・Commons の 1080p 版と秒は同じ＝差0.021秒）",
                     scan=BV_LOCAL.relative_to(HERE).as_posix(), dur=1801.8,
                     how="映像方針（10-08）：ffmpeg の scene＋1秒1コマの見本帳で目視＝bv_shots20.tsv",
                     shots=[dict(start=r["start"], until=r["until"], motion=0.0, shot=r["shot"], use=r["use"], what=r["what"])
                            for r in rows])}
    SHOTS.write_text(json.dumps(sd, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep20/shots.json（BV {len(rows)}ショット）")
    return 0


def cmd_clips():
    s = _sources()["BV"]
    w, h = 1920, 1080
    out = {"BV": dict(url=s["page"], media=s["media"], credit="出典：防衛省・自衛隊『昭和60年防衛庁記録』／CC BY 3.0／改変：切出・再生速度",
                      src="mod", at=0.0, date=None, what="昭和60年防衛庁記録（日航機の災害派遣の部分）", w=w, h=h, fps=29.97, sar="1:1",
                      sec=1801.8, size=730300000, dispw=w, decoded=[w, h], rights=s["rights"], scan=BV_LOCAL.relative_to(HERE).as_posix(),
                      # 🆕 ⑤b-7：実効の幅（映像方針 §2＝周波数の崖で21コマ・中央値 544px）＝`scene_jiko.foot_box` が差し込み（頭・尻）を
                      #   額装にする（器 1920 のままだと全画面＝試し焼き 38099274247 の c503 の尻が全画面で焼けた）
                      effw=544,
                      note="器 1920x1080・中身は 4:3（x 258〜1657・⑤b-2 で使う区間のコマを測った）＝USE の zoom 1.02 で黒帯を画面の外へ")}
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("→ ref/ep20/clips.json（BV）")
    return 0


def _rng(main):
    return [(float(a), float(b)) for a, b in re.findall(r"BV@([\d.]+)-([\d.]+)", main or "")]


# 黒帯を外す寄り（4:3 の中身 x 258〜1657 を 1.02 倍で＝箱の切り口 x 272〜1648・y 11〜1069）。fb の切り口も同じ幾何
BV_ZOOM = 1.02
FB_BOX = (272, 11, 1648, 1069)
FB_W = 1024


# 🆕 ⑤b-7（2026-10-11）：区間が2つのカット＝尻の映像の差し込み（`ss.tailv`・鍵 `<cid>~t`）に分ける。
#   カット → (差し込む行 at, 頭の区間, 尻の区間)。頭＝at 行目を読み始める少し前＋入れ替えの秒まで・尻＝そこから尺の終わりまで
#   （`scene_jiko.ins_sec`・`INTRO_X`＝footage.secs_of と同じ式）。
#   c503＝A（指揮所・4.3秒）→ B（F-4EJ の昼の離陸・2.0秒しかない＝尻の要る秒 約4.4秒に 0.4倍＝止め絵になる＝STILL_BELOW）。
#   c601＝🔴 一覧の順（E→F の後半）を**入れ替えた**：E（浮かぶ板 2.5秒）を頭にすると要る約4.6秒に 0.54倍＝止め絵。F の後半（ボートが
#   板を押さえる 5.6秒）を頭（1〜2行目＝「引き揚げられた」）・E を尻（3行目＝垂直尾翼の前の縁の上半分）にすると両方とも動く（0.75・0.85倍）。
#   副題は写っているものだけ（映画の板が「最初の破片」かは分からない＝言わない＝映像方針）
SPLIT = {
    "c503": (1, (1431.95, 1436.35), (1436.45, 1438.35)),
    "c601": (2, (1501.40, 1507.10), (1492.15, 1494.60)),
}


def cmd_use():
    """footage.USE の20本目の欄。rate＝使える秒÷要る秒（切り捨て・1.0まで）・0.6未満は止め絵。要る秒＝footage.secs_of（尺−扉）。
    区間が2つのカット（c503・c601）は上の SPLIT で頭と尻（`<cid>~t`）の2欄に分ける"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    import scene_jiko as S
    secs = FO.secs_of()
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))["BV"]["shots"]
    lines, skip = [], []
    for r in _list():
        rg = _rng(r["main"])
        if not rg:
            continue
        if len(rg) > 1:
            if r["cid"] not in SPLIT:
                skip.append(r["cid"])
                continue
            at, ha, ta = SPLIT[r["cid"]]
            head_need = S.ins_sec(r["cid"], at) + S.INTRO_X
            dur = dict(S.CUTS)[r["cid"]] - S.card_of(r["cid"])
            for key, (a, b), need, tail in ((r["cid"], ha, head_need, False), (r["cid"] + S.TAIL_KEY, ta, dur - S.ins_sec(r["cid"], at), True)):
                avail = b - a
                rate = min(1.0, int(avail / need * 100) / 100)
                sh = [s for s in sd if s["start"] <= a < s["until"]]
                where = f"ショット {sh[0]['shot']}（{sh[0]['start']:.2f}〜{sh[0]['until']:.2f}秒）" if sh else "ショット表の外"
                s0 = round((a + b) / 2, 2) if rate < STILL_BELOW else a
                opt = (f", still=True, until={min(b, s0 + 1.0):.2f}" if rate < STILL_BELOW else f", until={b:.2f}, rate={rate}")
                lines.append(f'    "{key}": dict(clip="BV", start={s0:.2f}{opt}, zoom={BV_ZOOM}{", tail=True" if tail else ""}),   '
                             f'# {where}・使える {avail:.2f}秒（{a:g}〜{b:g}）／要る {need:.2f}秒（{"尻" if tail else "頭"}・{at}行目で入れ替え）')
            continue
        a, b = rg[0]
        need = float(secs[r["cid"]])
        avail = b - a
        rate = min(1.0, int(avail / need * 100) / 100)
        sh = [s for s in sd if s["start"] <= a < s["until"]]
        where = f"ショット {sh[0]['shot']}（{sh[0]['start']:.2f}〜{sh[0]['until']:.2f}秒）" if sh else "ショット表の外"
        s0 = round((a + b) / 2, 2) if rate < STILL_BELOW else a
        opt = (f", still=True, until={min(b, s0 + 1.0):.2f}" if rate < STILL_BELOW else f", until={b:.2f}, rate={rate}")
        lines.append(f'    "{r["cid"]}": dict(clip="BV", start={s0:.2f}{opt}, zoom={BV_ZOOM}),   '
                     f'# {where}・使える {avail:.2f}秒（{a:g}〜{b:g}）／要る {need:.2f}秒')
    txt = FOOTAGE.read_text(encoding="utf-8")
    m = re.search(r"(    # EP20_USE>>> ここから[^\n]*\n)(.*?)(    # EP20_USE>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit("🔴 footage.py に EP20_USE の目印が無い")
    FOOTAGE.write_text(txt[:m.start(2)] + "".join(x + "\n" for x in lines) + txt[m.end(2):], encoding="utf-8")
    print(f"→ tools/footage.py USE {len(lines)}欄（止め絵 {sum('still=True' in x for x in lines)}）")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"⚠️ 区間が2つで書いていない（⑤b-7 で尻の差し込みに）：{' '.join(skip)}")
    return 0


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵＝`ss.vid` の photo）＝USE の start の1コマ（手元の YouTube 版＝秒は Commons 版と
    同じ）を、焼くときと同じ幾何（黒帯を外す寄り 1.02）で切った中身。箱の縦横比（`ss.kind`）もこの絵から決まる。
    🔴 幅は FB_W（1280 未満）に縮める＝実効の幅 約544px（映像方針 §2）の映像を全画面にしない（`ss.kind` が額装を返す＝PANEL_AR 0.99 の
    束では 4:3 の 1376px は全画面になる）。箱は 843×648 前後＝控えの 1024px はそれより大きい"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    bad = 0
    for cid, u in FO.USE.items():
        if only and cid not in only:
            continue
        dst = EPD / f"fb_{cid}.jpg"
        x0, y0, x1, y1 = FB_BOX
        r = subprocess.run(["ffmpeg", "-y", "-nostdin", "-v", "error", "-ss", f"{float(u['start']):.2f}", "-i", str(BV_LOCAL),
                            "-frames:v", "1", "-vf", f"crop={x1 - x0}:{y1 - y0}:{x0}:{y0},scale={FB_W}:-2", "-q:v", "2", str(dst)],
                           capture_output=True, text=True)
        if r.returncode or not dst.exists():
            print(f"🔴 {cid}: ひかえの静止画が作れない（{r.stderr[-160:]}）")
            bad += 1
            continue
        print(f"✓ {cid:5} BV {float(u['start']):7.2f}秒 → {dst.relative_to(HERE).as_posix()}（{x1 - x0}x{y1 - y0} → 幅 {FB_W}）")
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"build": cmd_build, "panel": cmd_panel, "shots": cmd_shots, "clips": cmd_clips, "use": cmd_use}
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] == "pages":
        sys.exit(cmd_pages({int(x) for x in a[1:]} or None))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
