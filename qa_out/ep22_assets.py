# -*- coding: utf-8 -*-
"""ep22_assets.py — 22本目（タイタン号のリメイク）の写真・映像の束（⑤b-2・2026-10-14）。21本目 `ep21_assets.py` の形。

取得はすんでいる（映像方針＝了承②・`ref/ep22/eizou_build/fetch22.py`・記録 `fetch22.tsv`＝md5 2回）。ここは**束を作る道**だけを持つ。
  python qa_out/ep22_assets.py build             # 写真の束 ref/ep22/<名>.jpg ＋ 権利の台帳 ref/ep22/assets.json
  python qa_out/ep22_assets.py panel             # 束の縦横比の並びと、16:9 より縦長の側のいちばん大きな切れ目（ss.PANEL_AR）
  python qa_out/ep22_assets.py edges             # 束の四辺の暗い帯（スライドの台紙の縁）＝門番 check_photo_edge の名簿 SLIDE_MOUNT を決める
  python qa_out/ep22_assets.py credits [--write] # 画面の出典 ref/ep22/credits.json と ref/CREDITS.md の22本目の節
  python qa_out/ep22_assets.py shots             # ref/ep22/shots.json（映像9本のショット＝shots22.tsv から）
  python qa_out/ep22_assets.py clips             # ref/ep22/clips.json（映像9本の台帳・媒体の長さは ffprobe で URL の頭だけ読む）
  python qa_out/ep22_assets.py nogo              # tools/footage.py の EP22_NOGO（使わない窓＝その秒を含むショットまるごと）
  python qa_out/ep22_assets.py fb [c101 …]       # 映像のひかえの静止画 ref/ep22/fb_<cid>.jpg（手元の元ファイルの1コマ・焼くときと同じ切り口）
  python qa_out/ep22_assets.py use               # tools/footage.py の EP22_USE（🔴 章ファイルに `ss.vid` を書いたカットだけ＝門番 slots は両側を見る）

入力＝映像方針の一覧 `ref/ep22/eizou_build/list22.tsv`（生成物・秒は narration.json の実測＝⑤b-1）・出どころ `sources22.tsv`・
取得の記録 `fetch22.tsv`・ショット `shots22.tsv`。写真と報告書の図の元は `ref/ep22/photo/`（git の外）。
🔴 束の写真は長辺を縮めるだけ（色・切り口はそのまま）＝幅 2400 か高さ 1350 の大きい方まで。それ以下は縮めない。
   ・報告書の図（PDF の埋め込みの PNG）は JPEG（品質 92）に直すだけ（`ss.P` は .jpg を引く）
   ・🔴 **EXIF の向きの札を絵に当てる**（D367＝1つ目の船体は札 6＝生の絵は横倒し・2026-10-14 に縮小で見た）＝束は向きの札なし
   ・🔴 **色の札（ICC）が sRGB でない点は sRGB に直す**（D342・D367＝Display P3）＝見た目の色はそのまま（相対の色の写像）・束は sRGB
     （合成の道が札を読まずに数を sRGB と読んでも色がずれない）
🔴 組み写真の片側だけを使う図（NTSB 図16 上下・図17 下・図18 左右）は**束の段階で割る**（ルール 0b-43①＝カットごとの trim でなく束で）＝
   名は `<元の名>_l`・`_r`・`_t`・`_b`。割り目は絵の白か黒の帯（行・列の全部の画素が白か黒）を機械で探す（無ければ止める）。
🔴 地図の衛星写真（G01〜G06＝Google の画像）は**束に入れない**（公開リポに置かない＝映像方針）＝焼き方は ⑤b-3 で決める。
🔴 撮影者の名前が要る3点（C218＝BY-SA・N08／N10＝第三者の個人）は名前を**リポに書かない**（映像方針の sources22 の注）＝
   画面の出典の行は印 `{撮影者:<記号>}` で書き、名前は git の外の `ref/ep22/src/credits_private.tsv` にだけある（差し込み方は ⑤b-3 で決める）。
⚠️ 研究所の報告 24-011 の頁の画像（L15・L21・L48＝1224×1584 の頁まるごと）は「紙面の引用」＝図と説明の行まで切るのは ⑤b-4（c6）。
   それまで束は頁まるごと（`QUOTE_PAGE`）＝PANEL_AR の並びには数えない（切ると縦横比が変わる）。
"""
import csv
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parents[1]
EPD = HERE / "ref" / "ep22"
BUILD = EPD / "eizou_build"
LIST = BUILD / "list22.tsv"
SOURCES = BUILD / "sources22.tsv"
FETCH = BUILD / "fetch22.tsv"
SHOTS_TSV = BUILD / "shots22.tsv"
DB = EPD / "assets.json"
CLIPS = EPD / "clips.json"
SHOTS = EPD / "shots.json"
CREDITS_JSON = EPD / "credits.json"
CREDITS_MD = HERE / "ref" / "CREDITS.md"
FOOTAGE = HERE / "tools" / "footage.py"
# 🔴 見出しは `check_credits.SECTION` と1字も違わない行（門番は**この回の節の中だけ**で表を探す＝§5b-82②・0b-34④）
CREDITS_HEAD = "## タイタン号のリメイク（2023-06-18・22本目）"
STILL_BELOW = 0.6            # rate がこれを下回る欄は動画にせず止め絵（12本目の教訓＝footage.py の注）
EVENT_YEAR = 2023            # 副題の「当日」＝この年（check_credits の EVENT_YEAR と同じ）

BUNDLE_W, BUNDLE_H = 2400, 1350        # 束の写真の大きさの上限（どちらかに届くまで縮める）
JPEG_Q = 92
PART = {"左": "l", "右": "r", "上": "t", "下": "b"}      # list22 の part の欄 → 束の名の尻
WHITE = 235                  # 組み写真の割り目＝この明るさ以上の画素だけの列（行）
BLACK = 20                   # または、この明るさ以下の画素だけの列（行）＝黒い帯の割り目（NTSB 図17）
QUOTE_PAGE = {"L15", "L21", "L48"}     # 頁まるごとの画像（紙面の引用）＝⑤b-4 で図と説明の行まで切る
PRIVATE_TOKEN = "{撮影者:%s}"          # 画面の出典の行の名前の印（名前は git の外）
FRAME_RIGHTS = ("第三者", "共同", "BY-SA")   # 額装だけ（了承② 決め3＝第三者・共同・BY-SA は額装・改変なし）

# 撮影年（副題の年の主張と照らす＝check_credits）。出どころ：DVIDS の EXIF・報告書の図の説明（USCG の MBI＝`src/uscg_mbi_pages.txt`）・
#   sources22 の注・Commons の頁。分からない点は None（表は「不明」・副題に年を書かない）
YEAR = {
    "D444": (2023, "EXIF 2023-06-22・DVIDS の捜索の写真（6月21日）"),
    "D448": (2023, "sources22 の注 2023-06-21（機内から見た海）"),
    "D471": (2023, "EXIF 2023-06-22"),
    "D342": (2023, "EXIF 2023-09-30（回収船の甲板）"),
    "D367": (2023, "sources22 の注：撮影 2023-08-02（MBI 図132 と同じ場面）・DVIDS の撮影日の欄 05.29.2019 は亀裂の日"),
    "C201": (2004, "Commons の説明：2004年6月の調査（EXIF の 2007-07-25 は加工の日）"),
    "C218": (2022, "Commons の頁の日付 2022-08-21（EXIF なし）"),
    "C1cc": (2024, "DVIDS 8668382＝2024-09-27（Commons の写し）"),
    "M03": (2023, "MBI 図3 の説明 June 25, 2023"), "M05": (2023, "MBI 図5 の説明 June 25, 2023"),
    "M18": (None, "MBI 図18＝航海日誌の頁の写真（撮った日の記載なし）"),
    "M21": (2023, "MBI 図21 の説明 Source: USCG, June 25, 2023"),
    "M24": (2023, "sources22 の注 2023-06-23"), "M31": (2023, "sources22 の注 2023-06-25"),
    "M37": (None, "MBI 図37＝post-casualty（日の記載なし）"),
    "M65": (2023, "MBI 図65 の説明 October 26, 2023（フォートメーコンの保管場所）"),
    "M109": (2023, "MBI 図109 の説明 June 25, 2023"), "M112": (2023, "MBI 図112 の説明 June 25, 2023"),
    "M115": (2023, "MBI 図115 の説明 June 25, 2023"),
    "M157": (2023, "MBI 図157 の説明 July 5, 2023（FBI）"), "M159": (2023, "MBI 図159 の説明 July 5, 2023（FBI）"),
    "M255": (None, "MBI 図255＝NTSB の研究所（日の記載なし）"), "M268": (None, "MBI 図268（日の記載なし）"),
    "M270": (None, "MBI 図270＝post-accident（日の記載なし）"),
    "N08": (2022, "NTSB 図8 の説明 in 2022"), "N10": (2023, "NTSB 図10＝2023年の遠征（5月20日と27日・sources22 の注）"),
    "N13": (None, "NTSB の研究所（日の記載なし）"), "N14": (None, "同"), "N15": (None, "同"), "N16": (None, "同"),
    "N17": (None, "同"), "N18": (None, "同（左は1つ目の船体・右は2020年の模型の端材＝写真の日の記載なし）"),
    "L15": (None, "研究所の報告 24-011（写真の日の記載なし）"), "L21": (None, "同"), "L22": (None, "同"), "L28": (None, "同"),
    "L39": (None, "同"), "L43b": (None, "同"), "L45a": (None, "同"), "L47b": (None, "同"), "L48": (None, "同"),
}


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _list():
    return list(csv.DictReader(LIST.open(encoding="utf-8"), delimiter="\t"))


def _rows(path, keys, minf):
    out = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if len(f) >= minf and not ln.startswith("#") and f[0] not in ("code", "film", ""):
            out.append(dict(zip(keys, f)))
    return out


def _sources():
    return {r["code"]: r for r in _rows(SOURCES, ["code", "class", "file", "page", "media", "get", "dims", "bytes", "rights",
                                                  "credit", "note"], 11)}


def _fetched():
    """{記号: [行…]}（U022 は区間4本・N10 は3枚＝1つの記号に行が複数）"""
    out = {}
    for r in _rows(FETCH, ["code", "class", "file", "bytes", "md5", "md5_check", "dims", "dur", "exif", "page"], 9):
        out.setdefault(r["code"], []).append(r)
    return out


def _fetch_row(code, file):
    rows = [r for r in _fetched().get(code, []) if r["file"] == file]
    return rows[0] if len(rows) == 1 else None


def uses():
    """{(記号, 割り): [カット]}（一覧の素材の欄から・写真と報告書の図だけ）。"""
    src = _sources()
    out = {}
    for r in _list():
        c = r["code"]
        if c and src.get(c, {}).get("class") in ("photo", "fig"):
            out.setdefault((c, PART.get(r["part"], "")), []).append(r["cid"])
    return out


def name_of(code, part, src):
    stem = Path(src["file"]).stem
    return f"{stem}_{part}" if part else stem


def frame_of(rights):
    return rights.startswith(FRAME_RIGHTS)


def screen_credit(code, s):
    """画面の出典の行（権利の記号＝sources22 の rights の頭）"""
    r, cr = s["rights"], s["credit"]
    if r.startswith("A"):
        m = re.match(r"(米沿岸警備隊|米空軍州兵 第106救難航空団)（DVIDS (\d+)）$", cr)
        if m:
            return f"出典：{m.group(1)}（DVIDS {m.group(2)}・パブリックドメイン）"
        # 報告書の図＝報告書の名と図の番号・撮った機関がちがう点はかっこに（FBI・NTSB の研究所）
        m = re.match(r"(米沿岸警備隊 海難調査委員会の報告書|米運輸安全委員会の報告書|米運輸安全委員会 研究所の報告 24-011) 図(\d+)"
                     r"(?:（(FBI|米運輸安全委員会)）)?$", cr)
        if m:
            who = {"FBI": "FBI 撮影・", "米運輸安全委員会": "米運輸安全委員会 撮影・"}.get(m.group(3) or "", "")
            return f"出典：{m.group(1)} 図{m.group(2)}（{who}パブリックドメイン）"
        raise SystemExit(f"🔴 {code}: A の出典の行が作れない（credit「{cr}」）")
    if r.startswith("第三者"):
        m = re.search(r"米運輸安全委員会の報告書 図(\d+)$", cr)
        if not m:
            raise SystemExit(f"🔴 {code}: 第三者の出典の行が作れない（credit「{cr}」）")
        return f"出典：米運輸安全委員会の報告書 図{m.group(1)}（撮影：{PRIVATE_TOKEN % code}）"
    if r.startswith("BY-SA"):
        return f"出典：{PRIVATE_TOKEN % code}（Wikimedia Commons）／CC BY-SA 4.0／改変なし"
    if r.startswith("共同"):
        return "出典：NOAA／Institute for Exploration／ロードアイランド大学"
    raise SystemExit(f"🔴 {code}: 権利の記号が読めない（{r}）")


def lic_of(r):
    return ("PD（米連邦の職務・17 U.S.C. §105）" if r.startswith("A") else
            "CC BY-SA 4.0" if r.startswith("BY-SA") else
            "引用（第三者の撮影・報告書の図）" if r.startswith("第三者") else
            "PD（Commons の表示）・共同＝額装" if r.startswith("共同") else None)


# ── 写真の束 ───────────────────────────────────────────────
def _flat(a, axis):
    """列（axis="x"）か行（"y"）ごとに「割り目の色だけか」＝白（WHITE 以上だけ）か黒（BLACK 以下だけ）。
    ⚠️ NTSB 図17 は上下の写真のあいだが**黒い帯**（y 327〜338・平均 0）＝白だけを探すと割り目が無いと出た（⑤b-2 の1回目）"""
    lo = a.min(axis=0) if axis == "x" else a.min(axis=1)
    hi = a.max(axis=0) if axis == "x" else a.max(axis=1)
    return (lo >= WHITE) | (hi <= BLACK)


def _gutter(a, axis, want):
    """組み写真の割り目（白か黒の帯）＝(始め, 終わり)。axis="x"＝縦の列（左右に割る）・"y"＝横の行（上下に割る）。
    want＝割り目のありそうな割合（sources22 の注）。縁に触れない帯のうち want にいちばん近いもの。無ければ None"""
    white = _flat(a, axis)
    n, runs, i = len(white), [], 0
    while i < n:
        if white[i]:
            j = i
            while j < n and white[j]:
                j += 1
            if i > 0 and j < n and j - i >= 3:
                runs.append((i, j))
            i = j
        else:
            i += 1
    if not runs:
        return None
    return min(runs, key=lambda r: abs((r[0] + r[1]) / 2 / n - want))


def _trim_white(im):
    """四辺の白だけの行・列を落とす（割ったあとの片側の紙の余白）。
    ⚠️ 黒は落とさない＝NTSB 図16 の上の写真は右の 1/4 が写真の黒い背景（列の平均 7・左から暗くなって続く）＝黒も落とすと写真の構図を切った
       （⑤b-2 の2回目で 1050→793px になって気づいた）。黒の帯は割り目を探すときだけ使う"""
    import numpy as np
    a = np.asarray(im.convert("L"))
    rows = np.where(a.min(axis=1) < WHITE)[0]
    cols = np.where(a.min(axis=0) < WHITE)[0]
    if not len(rows) or not len(cols):
        raise SystemExit("🔴 割ったあとの片側が白だけ")
    return (int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1)


SPLIT_AT = {"N18": ("x", 0.48), "N16": ("y", 0.5), "N17": ("y", 0.5)}    # 割り目のありそうな所（sources22 の注・左は約48%）


def _to_srgb(im):
    """色の札が sRGB でなければ sRGB に直す（相対の色の写像＝見た目の色はそのまま）。戻り＝(絵, 何をしたか)"""
    from PIL import ImageCms
    icc = im.info.get("icc_profile")
    im = im.convert("RGB")
    if not icc:
        return im, "札なし（sRGB と読む）"
    src = ImageCms.ImageCmsProfile(io.BytesIO(icc))
    desc = ImageCms.getProfileDescription(src).strip()
    if desc.startswith("sRGB") or desc == "c2":               # c2＝Commons の小さな sRGB の札
        return im, f"札 {desc}（sRGB のまま）"
    out = ImageCms.profileToProfile(im, src, ImageCms.createProfile("sRGB"), renderingIntent=1, outputMode="RGB")
    return out, f"札 {desc} → sRGB"


def cmd_build():
    from PIL import Image, ImageOps
    import numpy as np
    src = _sources()
    db, bad = {}, 0
    for (code, part), cuts in sorted(uses().items()):
        s = src[code]
        f, sp = _fetch_row(code, s["file"]), HERE / s["file"]
        if not f or not sp.exists():
            print(f"🔴 {code}: fetch22.tsv の行か手元のファイルが無い（{s['file']}）")
            bad += 1
            continue
        if md5(sp) != f["md5"]:
            print(f"🔴 {code}: {sp.name} の md5 が取得のときと違う（取り直す）")
            bad += 1
            continue
        name = name_of(code, part, s)
        dst = EPD / f"{name}.jpg"
        notes = []
        with Image.open(sp) as im0:
            ori = im0.getexif().get(274)
            im = ImageOps.exif_transpose(im0)
            if ori and ori != 1:
                notes.append(f"EXIF の向き {ori} を当てた（生の絵 {im0.size[0]}x{im0.size[1]}）")
            im.info["icc_profile"] = im0.info.get("icc_profile")
            im, how_c = _to_srgb(im)
        notes.append(how_c)
        w0, h0 = im.size
        box = [0.0, 0.0, 1.0, 1.0]
        if part:
            axis, want = SPLIT_AT[code]
            a = np.asarray(im.convert("L"))
            g = _gutter(a, axis, want)
            if not g:
                print(f"🔴 {code}: 組み写真の割り目（白いすき間）が見つからない")
                bad += 1
                continue
            # 割り目の側は 1px 内へ（割り目の縁のなじみの1行＝黒い帯と写真の混ざった行を落とす）
            if axis == "x":
                side = (0, 0, g[0] - 1, h0) if part == "l" else (g[1] + 1, 0, w0, h0)
            else:
                side = (0, 0, w0, g[0] - 1) if part == "t" else (0, g[1] + 1, w0, h0)
            sub = im.crop(side)
            t = _trim_white(sub)
            x0, y0 = side[0] + t[0], side[1] + t[1]
            x1, y1 = side[0] + t[2], side[1] + t[3]
            im = im.crop((x0, y0, x1, y1))
            box = [round(x0 / w0, 4), round(y0 / h0, 4), round(x1 / w0, 4), round(y1 / h0, 4)]
            notes.append(f"組み写真の{ {'l': '左', 'r': '右', 't': '上', 'b': '下'}[part]}（割り目 {axis}={g[0]}〜{g[1]}px＝{(g[0] + g[1]) / 2 / (w0 if axis == 'x' else h0):.3f}・"
                         f"切り口 {x0},{y0},{x1},{y1}）")
        w1, h1 = im.size
        k = min(1.0, max(BUNDLE_W / w1, BUNDLE_H / h1))
        if k < 1.0:
            im = im.resize((round(w1 * k), round(h1 * k)), Image.LANCZOS)
            notes.append(f"縮小 {w1}x{h1}→{im.size[0]}x{im.size[1]}")
        im.save(dst, quality=JPEG_Q, optimize=True)
        w, h = im.size
        y, ywhy = YEAR.get(code, (None, "（YEAR に無い）"))
        if code not in YEAR:
            print(f"🔴 {code}: 撮影年の表 YEAR に無い（出どころつきで書く）")
            bad += 1
        r = s["rights"]
        frame = frame_of(r)
        cr = screen_credit(code, s)
        who = (s["credit"] if r.startswith("A") or r.startswith("共同") else
               "（撮影者の名前は git の外＝`ref/ep22/src/credits_private.tsv`・画面の出典の行に出す）")
        db[name] = dict(code=code, part=part, file=s["file"], cut=" ".join(cuts), credit=cr, who=who, note=s["note"][:200],
                        box=box, crop_px=[0, 0, w, h], w=w, h=h, md5=md5(dst), src_md5=f["md5"],
                        lic=lic_of(r), frame=frame, ground=r, url=s["page"] if s["page"] not in ("—", "") else s["get"],
                        blur=[], how="・".join(notes), year=y, year_why=ywhy, stock=False,
                        quote_page=code in QUOTE_PAGE, private_name=PRIVATE_TOKEN % code in cr)
        print(f"✓ {code:5} {name:36} {w}x{h}  {' '.join(cuts):10} {lic_of(r)}{'  額装だけ' if frame else ''}  {'・'.join(notes)}")
    # 🔴 ROV の映像（第三者＝引用）のひかえの静止画も額装だけ（fb_<cid> を `ss.vid` が写真として当てる＝`ss.check_frame_only` が SPEC と
    #    footage.USE の欄〈寄り 1.0・等速・plain〉を見る）＝21本目の fb_c205（BY-SA の映像）と同じ形。出典の行は映像の台帳（CLIP_CREDIT）
    for r in _list():
        if r["code"] not in ROV:
            continue
        fbp = EPD / f"fb_{r['cid']}.jpg"
        if not fbp.exists():
            print(f"・ROV の {r['cid']}: fb_{r['cid']}.jpg がまだ無い（`fb {r['cid']}` のあとに build をもう一度）")
            continue
        with Image.open(fbp) as im:
            w, h = im.size
        s = src[r["code"]]
        db[f"fb_{r['cid']}"] = dict(code=r["code"], part="", file=s["file"], cut=r["cid"], credit=CLIP_CREDIT[r["code"]],
                                    who=s["credit"], note="ROV の映像のひかえの静止画（1コマ・切らない）", box=[0.0, 0.0, 1.0, 1.0],
                                    crop_px=[0, 0, w, h], w=w, h=h, md5=md5(fbp), src_md5=_fetch_row(r["code"], s["file"])["md5"],
                                    lic="引用（第三者の映像）", frame=True, ground=s["rights"], url=s["page"], blur=[],
                                    how="映像の1コマ（`fb`）", year=2023, year_why="ROV の潜航 2023-06-22", stock=False,
                                    quote_page=False, private_name=False)
        print(f"✓ {r['code']:5} fb_{r['cid']:33} {w}x{h}  {r['cid']:10} 引用（第三者の映像）  額装だけ")
    DB.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    tot = sum((EPD / f"{n}.jpg").stat().st_size for n in db)
    print(f"→ ref/ep22/assets.json（{len(db)}点・額装だけ {sum(1 for r in db.values() if r['frame'])}・頁まるごと "
          f"{sum(1 for r in db.values() if r['quote_page'])}・名前の印 {sum(1 for r in db.values() if r['private_name'])}・"
          f"束の大きさ {tot / 1e6:.1f}MB）")
    return 1 if bad else 0


def cmd_panel():
    """ルール 0b-34②：PANEL_AR＝束の縦横比の並びで、16:9 より縦長の側のいちばん大きな切れ目の中点。
    頁まるごとの画像（QUOTE_PAGE＝⑤b-4 で切る）は並びに数えない（紙面の引用は額装で出す・切ると縦横比が変わる）"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    ars = sorted((r["w"] / r["h"], n, r["w"]) for n, r in db.items() if not n.startswith("fb_") and not r.get("quote_page"))
    for a, n, w in ars:
        print(f"  {a:6.3f}  {n:40} 幅 {w}{'  （1280 未満＝kind() は額装）' if w < 1280 else ''}")
    side = [x for x in ars if x[0] < 16 / 9]
    gaps = sorted(((side[i + 1][0] - side[i][0], side[i], side[i + 1]) for i in range(len(side) - 1)), reverse=True)
    for g, a, b in gaps[:4]:
        print(f"切れ目 {g * 100:5.1f}ポイント：{a[0]:.3f}（{a[1]}）→ {b[0]:.3f}（{b[1]}）＝中点 {(a[0] + b[0]) / 2:.4f}")
    return 0


def cmd_edges():
    """束の全点の四辺の暗い帯（門番 check_photo_edge.margins と同じ物差し）＝スライドの台紙の縁がある写真の名簿を決める"""
    sys.path.insert(0, str(HERE / "tools"))
    import check_photo_edge as PE
    db = json.loads(DB.read_text(encoding="utf-8"))
    hits = []
    for n in sorted(db):
        if n.startswith("fb_"):
            continue                    # 映像のひかえ＝門番 check_photo_edge は映像を見ない
        m = PE.margins(f"ep22/{n}.jpg")
        mx = max(m.values())
        flag = "🔴" if mx >= PE.MIN_EDGE else ("・" if mx > 0 else " ")
        if mx > 0:
            hits.append((n, m))
        print(f"{flag} {n:40} 左 {m['l'] * 100:4.1f}% 上 {m['t'] * 100:4.1f}% 右 {m['r'] * 100:4.1f}% 下 {m['b'] * 100:4.1f}%")
    big = [n for n, m in hits if max(m.values()) >= PE.MIN_EDGE]
    print(f"→ 暗い帯のある点 {len(hits)}（うち {PE.MIN_EDGE * 100:.1f}% 以上 {len(big)}＝{' '.join(big) or 'なし'}）")
    return 0


# ── 画面の出典と CREDITS.md の節 ─────────────────────────────
CLIP_CREDIT = {
    "R04": "出典：Pelagic Research Services の ROV 映像（米沿岸警備隊・米運輸安全委員会が公開）",
    "R07": "出典：Pelagic Research Services の ROV 映像（米沿岸警備隊・米運輸安全委員会が公開）",
    "U022": "出典：米沿岸警備隊（DVIDS 888022・パブリックドメイン）",
    "U734": "出典：米沿岸警備隊（DVIDS 887734・パブリックドメイン）",
    "U597": "出典：米沿岸警備隊（DVIDS 887597・パブリックドメイン）",
    "U852": "出典：米沿岸警備隊（DVIDS 887852・パブリックドメイン）",
    "U248": "出典：米沿岸警備隊（DVIDS 888248・パブリックドメイン）",
    "U012": "出典：米空軍州兵 第106救難航空団（DVIDS 888012・パブリックドメイン）",
    "U011": "出典：米空軍州兵 第106救難航空団（DVIDS 888011・パブリックドメイン）",
}


def cmd_credits(write=False):
    """撮影年＝YEAR（出どころつき）。当てたカットの副題が名乗る年（「NNNN年」・「当日」＝2023）と食い違えば止める"""
    db = json.loads(DB.read_text(encoding="utf-8"))
    subs = {r["cid"]: r["sub"] for r in _list()}
    cj, rows, bad = {}, [], 0
    for n, r in sorted(db.items()):
        if n.startswith("fb_"):
            continue
        cuts = r["cut"].split()
        claims = set()
        for c in cuts:
            claims |= {int(y) for y in re.findall(r"(1[89]\d\d|20\d\d)年", subs.get(c, ""))}
            if "当日" in subs.get(c, ""):
                claims.add(EVENT_YEAR)
        y = r["year"]
        if claims and (y is None or claims != {y}):
            print(f"🔴 {n}: 副題の年 {sorted(claims)} と撮影年 {y} が食い違う（{' '.join(cuts)}）")
            bad += 1
        cj[f"ep22/{n}.jpg"] = r["credit"]
        gk = re.match(r"A|第三者|BY-SA|共同", r["ground"]).group(0)
        rows.append(f"| `{n}` | {' '.join(cuts)} | {y if y else '不明'} | {r['lic']}（{gk}） | {r['who']} | {r['url']} |")
    for k, v in cj.items():
        print(k, "|", v)
    print(f"… 写真 {len(cj)}点{'' if not bad else f'・🔴 食い違い {bad}'}")
    if bad:
        return 1
    if not write:
        return 0
    CREDITS_JSON.write_text(json.dumps(cj, ensure_ascii=False, indent=1), encoding="utf-8")
    src = _sources()
    film_rows = [f"| `{c}` | {' '.join(sorted({r['cid'] for r in _list() if r['code'] == c}))} | {CLIP_CREDIT[c]} | "
                 f"{src[c]['rights']} | {src[c]['page']} |" for c in CLIP_CREDIT]
    md = CREDITS_MD.read_text(encoding="utf-8")
    block = "\n".join([
        CREDITS_HEAD, "",
        "※2026-10-14（⑤b-2）。`qa_out/ep22_assets.py credits --write` が書く（手で直さない）。旧版の節は上の"
        "「タイタン号（本番1本目）」＝直さない（旧版は 10-13 に非公開を確かめた・ROV の映像を PD と書いていた誤りは旧版の節に残る）。",
        "🔴 撮影者の名前（私人）はこの表に書かない（映像方針＝公開のリポに置かない）＝名前が要る3点（C218＝CC BY-SA・N08／N10＝第三者の個人）は"
        "画面の出典の行に `{撮影者:<記号>}` の印で書き、名前は git の外（`ref/ep22/src/credits_private.tsv`）。",
        "",
        "### 0. 動く映像（9本・音はすべて使わない＝`-an`）",
        "- 🔴 **ROV の映像2本（R04＝尾部・R07＝前と後ろのドーム）は第三者（Pelagic Research Services の ROV「Odysseus」・2023-06-22）**＝"
        "米沿岸警備隊と米運輸安全委員会が NTSB のドケットで公開した物の引用。**額装・等速（rate 1.0）・寄り 1.0・無加工・地は無地（`plain=True`）"
        "・焼き込み（深さ・日付）は残す・サムネに使わない**（了承② 決め3）。旧版はパブリックドメインと誤って書いていた",
        "- DVIDS 888022／887734／887597／887852／888248＝米沿岸警備隊の職員の職務＝PD。888012／888011＝米空軍州兵 第106救難航空団の職務（連邦の任務の"
        "扱いが弱い所＝DVIDS の表示に従う）。記者会見は使う区間＋前後10秒だけを手元に置き（`ref/ep22/src/film/<記号>/clips/`・git の外）、焼くときは"
        "媒体の URL から区間だけ読む（`range`）",
        "- 使わない窓（`tools/footage.py` の NOGO）：887734 の机の上の顔写真入りの身分証（その秒を含むショットまるごと）",
        "",
        "| 記号 | 使うカット | 画面の出典 | 権利 | 出どころ |",
        "|---|---|---|---|---|", *film_rows, "",
        "### 1. 写真と報告書の図（米連邦の職務〈A〉・第三者〈引用〉・CC BY-SA・共同）",
        "- 束＝`ref/ep22/photo/`（git の外）の長辺を幅 2400／高さ 1350 まで縮めただけ（色・切り口はそのまま）。報告書の図（PDF の埋め込みの PNG）は"
        " JPEG に直しただけ。🔴 EXIF の向きの札は絵に当てた（D367＝1つ目の船体は縦長）・色の札が Display P3 の2点（D342・D367）は sRGB に写した"
        "（見た目の色はそのまま）。組み写真の片側だけを使う NTSB 図16・17・18 は白いすき間で割った（`_l`・`_r`・`_t`・`_b`＝割り目は機械で探した）",
        "- 🔴 **額装だけ（了承② 決め3）**＝第三者（NTSB 図8・図10＝個人の撮影）・共同（タイタニックの船首＝NOAA と連邦の外の機関）・CC BY-SA 4.0"
        "（ホライゾン・アークティック）＝無加工・色そのまま・上に重ねない・寄り0・1点1カット（`cuts/ss.check_frame_only`）・サムネに使わない",
        "- 報告書の図の撮った機関＝米沿岸警備隊の海難調査委員会（MBI）・FBI（図157・159・270）・米運輸安全委員会の研究所（図255・NTSB の図13〜18・24-011）",
        "- 研究所の報告 24-011 の頁まるごとの画像（図15・21・48）は紙面の引用＝図と説明の行まで切るのは ⑤b-4",
        "- 撮影年＝報告書の図の説明・EXIF・Commons の頁（`qa_out/ep22_assets.py` の YEAR＝出どころつき）。分からない点は「不明」＝副題に年を書かない",
        "",
        "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころと許諾 |",
        "|---|---|---|---|---|---|", *rows, "",
        "### 2. 地図の衛星写真（Google マップ・束に入れない）",
        "- G01〜G06＝Google マップの衛星写真（⑤b-1 に撮った・`ref/ep22/photo/gmap_g0*.png`＝git の外）。Google の地理の指針（教育の動画は許可不要・"
        "収益化も可）に従い、**絵の下の帰属の行（地図データ ©2026 Google・画像 ©提供元）とロゴを映す間ずっと残す**・色を変えない・動かさない・"
        "点と線と札は描き足してよい。🔴 公開のリポに画像を置かない＝焼き方は ⑤b-3（地図の型）で決める",
        ""])
    if CREDITS_HEAD in md:
        pre, rest = md.split(CREDITS_HEAD, 1)
        nxt = rest.find("\n## ")
        md = pre + block + (rest[nxt:] if nxt >= 0 else "")
    else:
        md = md.rstrip("\n") + "\n\n" + block
    CREDITS_MD.write_text(md, encoding="utf-8")
    print(f"→ {CREDITS_JSON.relative_to(HERE).as_posix()} ／ {CREDITS_MD.relative_to(HERE).as_posix()}")
    return 0


# ── 映像（ショット・台帳・使わない窓・ひかえ・USE） ─────────────
FILM = {   # 記号 → (何か, 出どころの種類, 撮影の日, 区間読み＝URL のまま区間だけ読むか)
    "R04": ("ROV「Odysseus」の映像 04（尾部・NTSB ドケット 6- SURVIVAL FACTORS – PELAGIC VIDEO 1 OF 2）", "ntsb", "2023-06-22", False),
    "R07": ("ROV「Odysseus」の映像 07（前と後ろのドーム・PELAGIC VIDEO 2 OF 2）", "ntsb", "2023-06-22", False),
    "U022": ("ボストンの記者会見（残骸の発見）", "dvids", "2023-06-22", True),
    "U734": ("ボストン第1管区の指令センターの B-roll", "dvids", "2023-06-20", True),
    "U012": ("ウェストハンプトンビーチの基地・HC-130J の B-roll", "dvids", "2023-06-21", True),
    "U011": ("同じ基地・隊員が機体へ向かう B-roll", "dvids", "2023-06-21", True),
    "U597": ("ボストンの記者会見（捜索の経過）", "dvids", "2023-06-19", True),
    "U852": ("ボストンの記者会見（捜索の経過）", "dvids", "2023-06-21", True),
    "U248": ("ボストンの記者会見（海難調査委員会を開く）", "dvids", "2023-06-25", True),
}
ROV = {"R04", "R07"}          # 🔴 等速（了承② 決め3）＝rate は 1.0 だけ・区間がカットの秒に足りなければ止める
# 中身の切り口。ROV＝額装・寄り 1.0・無加工・地は無地（第三者＝改変しない）。DVIDS＝16:9 の全画面（黒い縁の測りは ⑤b-2 の scratchpad `box22.py`）
GEOM = {"R04": dict(full=False, zoom=1.0, plain=True), "R07": dict(full=False, zoom=1.0, plain=True)}
GEOM.update({k: dict(full=True, zoom=1.0) for k in FILM if k not in ROV})
GEOM_CUT = {}
FB_W = 1024                     # 額装の映像のひかえの幅（1280 未満＝`ss.kind` が額装を返す）
# 使わない窓（mm:ss）＝その秒を含むショットまるごと（sources22 の注：887734 の 31秒前後のショットは机に顔写真入りの身分証）
NOGO_AT = {"U734": [("0:31", "机の上の顔写真入りの身分証")]}


def _shots():
    out = {}
    for ln in SHOTS_TSV.read_text(encoding="utf-8").splitlines():
        f = ln.split("\t")
        if ln.startswith("#") or len(f) < 5 or f[0] == "film":
            continue
        out.setdefault(f[0], []).append(dict(shot=int(f[1]), start=float(f[2]), until=float(f[3])))
    return out


def _probe(p, url=False):
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    net = ["-user_agent", FO.UA] if url else []
    r = subprocess.run(["ffprobe", "-v", "error", *net, "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,sample_aspect_ratio:format=duration", "-of", "json", str(p)],
                       capture_output=True, text=True, timeout=120)
    if r.returncode:
        raise SystemExit(f"🔴 ffprobe が読めない：{p}（{r.stderr[-200:]}）")
    j = json.loads(r.stdout)
    st = j["streams"][0]
    a, b = st["r_frame_rate"].split("/")
    return dict(w=int(st["width"]), h=int(st["height"]), fps=round(int(a) / int(b), 3),
                sar=st.get("sample_aspect_ratio") or "1:1", sec=float(j["format"]["duration"]))


def _local_of(code, t):
    """手元の元ファイルと、その頭が元の何秒か（clips/ は t<始め>_<終わり>.mp4）"""
    s = _sources()[code]
    p = HERE / s["file"]
    if p.is_file():
        return p, 0.0
    for f in sorted(p.glob("t*_*.mp4")):
        a, b = (float(x) for x in re.match(r"t([\d.]+)_([\d.]+)\.mp4", f.name).groups())
        if a <= t < b:
            return f, a
    raise SystemExit(f"🔴 {code}: {t}秒を含む手元の区間が無い（{s['file']}）")


def cmd_shots():
    """shots.json＝映像方針のショットの境目（shots22.tsv）。footage の門番（outside_shot・unknown_clip）が読む"""
    sh = _shots()
    src = _sources()
    out = {}
    for code, rows in sh.items():
        out[code] = dict(src=src[code]["page"], scan=src[code]["file"],
                         how="映像方針（10-14）：ffmpeg の scene の境目（helpers/shots22.py）・使う区間は1秒1コマで見た（shots22.tsv）",
                         shots=[dict(start=r["start"], until=r["until"], motion=0.0, shot=r["shot"]) for r in rows])
    SHOTS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep22/shots.json（{' '.join(f'{k} {len(v)}' for k, v in sh.items())}）")
    return 0


def cmd_clips():
    """台帳。w・h・コマ/秒・SAR は手元のファイルから・媒体の長さは URL の頭だけ ffprobe で（落とさない）"""
    src = _sources()
    out = {}
    for code, (what, kind, date, rng) in FILM.items():
        s = src[code]
        lp, _ = _local_of(code, float(min(float(r["window"].split("〜")[0]) for r in _list() if r["code"] == code)))
        loc = _probe(lp)
        sec = loc["sec"] if lp == HERE / s["file"] else _probe(s["media"], url=True)["sec"]
        e = dict(url=s["page"], media=s["media"], credit=CLIP_CREDIT[code], src=kind, at=0.0, date=date, what=what,
                 w=loc["w"], h=loc["h"], fps=loc["fps"], sar=loc["sar"], sec=round(sec, 3), size=int(s["bytes"]),
                 dispw=loc["w"], decoded=[loc["w"], loc["h"]], rights=s["rights"], scan=s["file"], effw=loc["w"],
                 note=f"中身の切り口＝{GEOM[code]}（qa_out/ep22_assets.py の GEOM）")
        if rng:
            e["range"] = True          # 🔴 丸ごと落とさず URL のまま区間だけ読む（DVIDS の1本 121〜978MB）
        out[code] = e
        print(f"  {code:5} {loc['w']}x{loc['h']} {loc['fps']}fps sar {loc['sar']} {sec:8.2f}秒  range={rng}  {s['media'][:70]}")
    CLIPS.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ ref/ep22/clips.json（{len(out)}本）")
    return 0


def _mmss(t):
    m, s = t.split(":")
    return int(m) * 60 + int(s)


def _write_block(tag, lines):
    txt = FOOTAGE.read_text(encoding="utf-8")
    m = re.search(rf"(    # {tag}>>> ここから[^\n]*\n)(.*?)(    # {tag}>>> ここまで)", txt, re.S)
    if not m:
        raise SystemExit(f"🔴 footage.py に {tag} の目印が無い")
    FOOTAGE.write_text(txt[:m.start(2)] + "".join(x + "\n" for x in lines) + txt[m.end(2):], encoding="utf-8")


def cmd_nogo():
    sh = _shots()
    lines = []
    for code, ats in NOGO_AT.items():
        items = []
        for at, why in ats:
            t = _mmss(at)
            s = [r for r in sh[code] if r["start"] <= t < r["until"]]
            if len(s) != 1:
                raise SystemExit(f"🔴 {code} {at}：ショットが {len(s)} 本")
            s = s[0]
            items.append(f'({s["start"]:.2f}, {s["until"]:.2f}, "sources22 の注の {at}＝{why}（ショット {s["shot"]}）")')
        lines.append(f'    "{code}": [' + ", ".join(items) + "],")
    _write_block("EP22_NOGO", lines)
    print("→ tools/footage.py NOGO")
    for x in lines:
        print(x.strip())
    return 0


def _geom(cid, code):
    g = dict(GEOM[code])
    g.update(GEOM_CUT.get(cid, {}))
    return g


def _crop_box(sw, sh, g):
    """焼くときの切り口（`build_jiko._fit_geom` と同じ式）＝(左, 上, 幅, 高さ)。額装は箱の縦横比＝中身の縦横比（真ん中から寄り）"""
    zoom, xb, yb = g.get("zoom", 1.0), g.get("xbias", 0.5), g.get("bias", 0.5)
    if g["full"]:
        z = max(1920 / sw, 1080 / sh) * zoom
        cw, ch = min(sw, 1920 / z), min(sh, 1080 / z)
    else:
        cw, ch = sw / zoom, sh / zoom
    return (sw - cw) * xb, (sh - ch) * yb, cw, ch


def cmd_fb(only=None):
    """ひかえの静止画（映像のコマが切り出せなかったときだけ出る絵＝`ss.vid` の photo）＝一覧の区間の頭の1コマ（手元の元ファイル）を、
    焼くときと同じ幾何（`_crop_box`）で切った中身。箱（`ss.kind`）もこの絵から決まる＝額装（ROV）は幅 FB_W（1280 未満）・全画面は 1920×1080"""
    from PIL import Image
    bad = 0
    for r in _list():
        if not r["window"]:
            continue
        cid = r["cid"]
        if only and cid not in only:
            continue
        code = r["code"]
        a = float(r["window"].split("〜")[0])
        lp, off = _local_of(code, a)
        b = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a - off:.3f}", "-i", str(lp), "-frames:v", "1",
                            "-vf", "scale=iw*sar:ih,setsar=1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        if not b:
            print(f"🔴 {cid}: コマが取れない")
            bad += 1
            continue
        im = Image.open(io.BytesIO(b)).convert("RGB")
        sw, sh = im.size
        g = _geom(cid, code)
        l, t, cw, ch = _crop_box(sw, sh, g)
        im = im.crop((round(l), round(t), round(l + cw), round(t + ch)))
        im = im.resize((1920, 1080) if g["full"] else (FB_W, round(FB_W * im.height / im.width)), Image.LANCZOS)
        dst = EPD / f"fb_{cid}.jpg"
        im.save(dst, quality=92)
        print(f"✓ {cid:5} {code:5} {a:7.2f}秒（{lp.name} の {a - off:.2f}秒） {sw}x{sh} → {im.width}x{im.height}  {dst.name}")
    return 1 if bad else 0


def cmd_use():
    """footage.USE の22本目の欄（🔴 章ファイルに `ss.vid` を書いたカットだけ＝門番 slots）。rate＝使える秒÷要る秒（切り捨て・1.0まで）・
    0.6未満は止め絵。🔴 ROV は等速（rate 1.0 だけ）＝要る秒が使える秒より TOL を超えて長ければ止める。寄りと寄せは GEOM"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    import check_footage_slots as SL
    secs = FO.secs_of()
    want = set(SL.slots())
    sh = _shots()
    lines, skip, bad = [], [], 0
    for r in _list():
        if not r["window"]:
            continue
        cid = r["cid"]
        if cid not in want:
            skip.append(cid)
            continue
        code = r["code"]
        a, b = (float(x) for x in r["window"].split("〜"))
        need = float(secs[cid])
        avail = b - a
        if code in ROV:
            rate = 1.0
            if need > avail + FO.TOL:
                print(f"🔴 {cid}: ROV は等速＝要る {need:.2f}秒が使える {avail:.2f}秒より長い（区間を assign22.tsv で延ばす）")
                bad += 1
        else:
            rate = min(1.0, int(avail / need * 100) / 100)
        s = [x for x in sh[code] if x["start"] <= a < x["until"]]
        where = f"ショット {s[0]['shot']}（{s[0]['start']:.2f}〜{s[0]['until']:.2f}秒）" if s else "ショット表の外"
        g = _geom(cid, code)
        geo = f", zoom={g['zoom']}" + (f", xbias={g['xbias']}" if "xbias" in g else "") + (", plain=True" if g.get("plain") else "")
        if rate < STILL_BELOW:
            s0 = round((a + b) / 2, 2)
            opt = f", still=True, until={min(b, s0 + 1.0):.2f}"
        else:
            s0 = a
            opt = f", until={b:.2f}, rate={rate}"
        lines.append(f'    "{cid}": dict(clip="{code}", start={s0:.2f}{opt}{geo}),   # {where}・使える {avail:.2f}秒（{a:g}〜{b:g}）／要る {need:.2f}秒')
    if bad:
        return 1
    _write_block("EP22_USE", lines)
    print(f"→ tools/footage.py USE {len(lines)}欄（止め絵 {sum('still=True' in x for x in lines)}）")
    for x in lines:
        print(x.strip())
    if skip:
        print(f"・章ファイルに ss.vid がまだ無い（⑤b-3〜⑤b-7）：{' '.join(skip)}")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    cmds = {"build": cmd_build, "panel": cmd_panel, "edges": cmd_edges, "shots": cmd_shots, "clips": cmd_clips,
            "nogo": cmd_nogo, "use": cmd_use}
    if a and a[0] == "credits":
        sys.exit(cmd_credits("--write" in a))
    if a and a[0] == "fb":
        sys.exit(cmd_fb(set(a[1:]) or None))
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
