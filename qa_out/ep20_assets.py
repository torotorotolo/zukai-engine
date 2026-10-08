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
        if not sp.exists():
            print(f"🔴 {code}: {sp.relative_to(HERE).as_posix()} が無い")
            bad += 1
            continue
        dst = EPD / f"{name}.jpg"
        with Image.open(sp) as im0:
            im = im0.convert("L")            # 白黒のまま（1ビットのスキャンの縮小＝灰色）。png の解説の図も jpg の束へ
            w, h = im.size
            if sp.suffix == ".jpg":
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
        print(f"✓ {code:7} {name:30} {w}x{h}  {' '.join(cuts)}  {db[name]['lic']}{'  額装だけ（引用）' if frame else ''}")
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


def cmd_use():
    """footage.USE の20本目の欄。rate＝使える秒÷要る秒（切り捨て・1.0まで）・0.6未満は止め絵。要る秒＝footage.secs_of（尺−扉）。
    ⚠️ 区間が2つのカット（c503＝A＋B・c601＝E＋F の後半）は1欄に書けない＝⑤b-7 で尻の映像の差し込み（`<cid>~t`）に分ける＝ここでは書かない"""
    sys.path.insert(0, str(HERE / "tools"))
    import footage as FO
    secs = FO.secs_of()
    sd = json.loads(SHOTS.read_text(encoding="utf-8"))["BV"]["shots"]
    lines, skip = [], []
    for r in _list():
        rg = _rng(r["main"])
        if not rg:
            continue
        if len(rg) > 1:
            skip.append(r["cid"])
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
    if a and a[0] in cmds:
        sys.exit(cmds[a[0]]())
    print(__doc__)
