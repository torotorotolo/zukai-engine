# -*- coding: utf-8 -*-
"""キー橋（6本目）355ショットの**中身**を機械で当たり付けし、目で見るシートを作る。

■ なぜ要るか
  ②素材は**秒しか測っていない**（`SHOTS_INDEX.md` の冒頭にそう書いてある）。
  ⑤b-4 は「どのショットに何が写っているか」を決める工程だが、
  ⚠️ **355ショットを1枚ずつ原寸で見ることはできない**（画像は枚数の2乗で効く）。
  → 目で見る前に、機械で取れるものを全部取る。
     → [[feedback-gates-dont-see-text-burned-into-the-picture]]（目視の前に OCR＋幾何）

■ 5本目の `tools/sl1_shots.py` と何が違うか（**写しではない**）
  1. **素材の台帳が `ref/keybridge/`**（5本目のパスを向いたままだと全欄が素通りする
     → [[feedback-gates-blind-to-the-new-material]]）
  2. 🔴 **顔の検出を足した**。5本目（記録映画）に無く6本目（B-Roll）に在る危険が
     「**会見・式典の顔**」＝ カズヤくんの指示「人の顔が写る会見・式典の場面を落とす」。
     ⚠️ 顔検出は**当たり付け**であって採否ではない（横顔・小さい顔は落ちる）。
  3. 🔴 **手元に mp4 を落とさない**。C: の空きが 12.6GB しか無く、28本で約3GB。
     ＝ **1本につき ffmpeg 1回の通し読み**で必要なコマだけ抜く（範囲取得の連打をしない）。
     ⚠️ Commons は要求を連打すると **429** を返す（②素材の実測・記憶にもある）。

■ 🔴 コマとショットの対応をずらさないための書き方
  `select='eq(n,..)+eq(n,..)'` ＝ **コマ番号**で選ぶ（秒で選ぶと 1コマ内に2つ入る・0個になる）。
  出てきた枚数が、渡したコマ番号の数と**合っているかを必ず数える**。
  合わなければ順番の対応が崩れているので、その本は「取れていない」として落とす。
  ＝ 例外で止まる門番と同じ扱い（[[feedback-a-gate-that-throws-measures-nothing]]）。

■ 使い方
    python tools/keybridge_shotscan.py frames         # 355ショット×3コマ（頭・中・尻）
    python tools/keybridge_shotscan.py frames <clip>  # 1本だけ
    python tools/keybridge_shotscan.py ocr            # 焼き込み文字（Windows OCR）
    python tools/keybridge_shotscan.py faces          # 顔の検出
    python tools/keybridge_shotscan.py stat           # 表（shotstat.json ＋ 画面に一覧）
    python tools/keybridge_shotscan.py sheet <clip> <頁>  # 目で見るシート
    python tools/keybridge_shotscan.py --selftest     # 陽性対照

⚠️ **この道具は「当たりを付ける」もので、採否そのものではない。**
   採ると決めたショットは `footage.USE` に (start, until) を書き、`fetch --check` に通す。
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
REF = HERE / "ref" / "keybridge"
WORK = HERE / "out" / "jiko" / "kbscan"
SHOTS_JSON = REF / "shots.json"
CLIPS_JSON = REF / "clips.json"
CELL = (960, 540)          # 顔の検出に使うので 5本目（640x360）より大きく取る
# 🔴 顔検出の模型。opencv-python-headless 5.0 は Haar カスケードを同梱しない。
#    無ければ `faces()` は**止まる**（0で埋めない＝[[feedback-parsers-fail-closed]]）。
YUNET = HERE / "ref" / "models" / "face_detection_yunet_2023mar.onnx"
UA = ("zukai-engine/1.0 (accident-documentary research; konariri8@gmail.com)")

SHOTS = json.loads(SHOTS_JSON.read_text(encoding="utf-8"))
CLIPS = json.loads(CLIPS_JSON.read_text(encoding="utf-8"))


def _positions(a, b):
    """そのショットから抜く秒。(接尾辞, 秒) の3つ。

    🔴 ②の境目は**1秒刻みの実測**なので、境目そのものは最大1秒ぶれる。
       ＝ 頭と尻は**1秒ぶん内側**に寄せる（前後のショットの絵を代表にしない）。
    """
    d = max(b - a, 0.0)
    m = min(1.0, d * 0.15)
    return [("_h", a + m), ("", a + d * 0.5), ("_t", b - m)]


def targets(clip):
    """[(ファイル名, 秒, コマ番号)] を返す。**コマ番号で選ぶ**（秒では選ばない）。"""
    fps = CLIPS[clip]["fps"]
    out = []
    for i, s in enumerate(SHOTS[clip]["shots"]):
        for suf, sec in _positions(s["start"], s["until"]):
            out.append((f"{i:04d}{suf}", round(sec, 3), int(round(sec * fps))))
    return out


def frames(clip=None):
    """1本につき ffmpeg 1回の通し読みで、ショットごとに頭・中・尻の3コマを抜く。"""
    names = [clip] if clip else list(SHOTS)
    total, bad = 0, []
    for name in names:
        out = WORK / name
        out.mkdir(parents=True, exist_ok=True)
        tg = targets(name)
        if all((out / f"{t[0]}.jpg").exists() for t in tg):
            print(f"  {name}: すでに {len(tg)} 枚（飛ばす）", flush=True)
            total += len(tg)
            continue
        # コマ番号は重なりうる（極端に短いショット）。**番号は落とし、対応表は残す**
        order, seen = [], {}
        for fn, sec, n in tg:
            if n not in seen:
                seen[n] = len(order)
                order.append(n)
        tmp = out / "_raw"
        tmp.mkdir(exist_ok=True)
        for f in tmp.glob("*.jpg"):
            f.unlink()
        expr = "+".join(f"eq(n\\,{n})" for n in order)
        cmd = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
               "-user_agent", UA, "-i", CLIPS[name]["url"],
               "-vf", f"select='{expr}',scale={CELL[0]}:{CELL[1]}",
               "-vsync", "0", "-q:v", "3", str(tmp / "%04d.jpg")]
        print(f"  {name}: {len(order)} コマを1回の通し読みで抜く…", flush=True)
        r = subprocess.run(cmd, capture_output=True, timeout=5400)
        got = sorted(tmp.glob("*.jpg"))
        if len(got) != len(order):
            # 🔴 数が合わない＝順番の対応が崩れている。**黙って使わない**
            bad.append(f"{name}（渡した {len(order)} / 出た {len(got)}）")
            print(f"    🔴 枚数が合わない: {len(got)}/{len(order)}"
                  f"  {(r.stderr or b'')[-200:].decode('utf-8', 'replace')}", flush=True)
            continue
        for fn, sec, n in tg:
            (out / f"{fn}.jpg").write_bytes(got[seen[n]].read_bytes())
        for f in got:
            f.unlink()
        tmp.rmdir()
        total += len(tg)
        print(f"    ✓ {len(tg)} 枚", flush=True)
    print(f"■ 合計 {total} 枚 → {WORK}")
    if bad:
        print("🔴 取れなかった本（順番が崩れるので使わない）: " + " / ".join(bad))
    return total, bad


def ocr(clip=None):
    """焼き込みの文字を全コマぶん取る（Windows の OCR）。**30枚ずつ渡す**。"""
    dest = WORK / "ocr.json"
    res = json.loads(dest.read_text(encoding="utf-8")) if dest.exists() else {}
    for name in ([clip] if clip else list(SHOTS)):
        files = [f for f in sorted((WORK / name).glob("*.jpg"))
                 if f"{name}/{f.stem}" not in res]
        if not files:
            continue
        for i in range(0, len(files), 30):
            chunk = files[i:i + 30]
            r = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                 "-File", str(HERE / "tools" / "ocr_win.ps1"),
                 "-Files", ",".join(str(f) for f in chunk)],
                capture_output=True, timeout=900)
            # ⚠️ text=True で受けると cp932 で落ちて**残りが黙って0件**になる（5本目の実測）
            raw = r.stdout or b""
            txt = None
            for enc in ("utf-8", "cp932"):
                try:
                    txt = raw.decode(enc)
                    break
                except UnicodeDecodeError:
                    txt = None
            if txt is None:
                txt = raw.decode("cp932", errors="replace")
            cur = None
            for ln in txt.splitlines():
                if ln.startswith("## "):
                    cur = Path(ln.split()[1]).stem
                    res.setdefault(f"{name}/{cur}", [])
                elif cur is not None and ln.strip():
                    res[f"{name}/{cur}"].append(ln.strip())
        print(f"  {name}: {len(files)} 枚", flush=True)
        dest.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    withtext = sum(1 for v in res.values() if v)
    print(f"■ OCR {len(res)} 枚（文字が出た {withtext} 枚）→ {dest}")
    return res


# 🔴 出してはいけない絵の目印。**スレート・クレジット・局のロゴ・氏名テロップ**
#   ⚠️ 5本目（記録映画）の語とは別。DVIDS / NTSB の B-Roll に出る語で作り直した。
BAD_WORDS = re.compile(
    r"(?i)\b(b-?roll|dvids|courtesy|photo by|video by|footage|"
    r"public affairs|press|briefing|news|conference|"
    r"copyright|all rights|getty|reuters|associated press|"
    r"wjz|wbal|wmar|fox\s*\d|abc|nbc|cbs|cnn|"
    # 🔴 2026-09-08 ⑤b-4：**NTSB の3本は頭と尻に「濃紺の題字カード」が入る。**
    #    真っ暗ではない（lum≈30）ので暗さの網に掛からず、`windows` が
    #    「12〜451秒ぜんぶ使える」という**間違った合格**を出していた。
    r"ntsb|national transportation|safety board)\b")


def is_card(r):
    """🔴 中票・題字カードの見分け。**暗さだけでは足りない**（NTSB のカードは濃紺）。

    ＝ ①真っ暗 ②NG語が読める ③**字が読めて、しかも前の秒からほとんど動いていない**
    ⚠️ ③に「字が読めた」を必須にしてあるのは、凪の水面のような
       「動かないが絵である」ショットを巻き込まないため。
    """
    if r.get("lum", 99) < 20:
        return True
    if BAD_WORDS.search(r.get("text") or ""):
        return True
    d = r.get("d")
    return bool(r.get("text")) and d is not None and d < 1.5


def faces(clip=None):
    """🔴 顔の検出。**会見・式典の寄り**をコマの側から止める網。

    ⚠️ これは当たり付け。**横顔・小さい顔・帽子で隠れた顔は落ちる**ので、
       「顔0件」を「人が写っていない」と読み替えてはいけない
       → [[feedback-absence-of-a-word-is-not-absence]]
    """
    import cv2
    if not YUNET.exists():
        raise SystemExit(
            f"🔴 顔検出の模型が無い（{YUNET}）。**0で埋めない**＝測れていない。\n"
            "   opencv-python-headless 5.0 は Haar カスケードを同梱しなくなったので、"
            "YuNet（ONNX）が要る。")
    det = cv2.FaceDetectorYN.create(str(YUNET), "", (CELL[0], CELL[1]),
                                    score_threshold=0.6)
    dest = WORK / "faces.json"
    res = json.loads(dest.read_text(encoding="utf-8")) if dest.exists() else {}
    for name in ([clip] if clip else list(SHOTS)):
        files = [f for f in sorted((WORK / name).glob("*.jpg"))
                 if f"{name}/{f.stem}" not in res]
        for f in files:
            im = cv2.imread(str(f))
            if im is None:
                res[f"{name}/{f.stem}"] = None      # 読めない＝fail closed（0で埋めない）
                continue
            h, w = im.shape[:2]
            det.setInputSize((w, h))
            _, box = det.detect(im)
            box = [] if box is None else list(box)
            res[f"{name}/{f.stem}"] = dict(
                n=len(box),
                big=round(max([float(b[3]) / h for b in box], default=0.0), 3))
        if files:
            print(f"  {name}: {len(files)} 枚", flush=True)
            dest.write_text(json.dumps(res, ensure_ascii=False, indent=1),
                            encoding="utf-8")
    hit = sum(1 for v in res.values() if v and v["n"])
    print(f"■ 顔 {len(res)} 枚中 {hit} 枚で検出 → {dest}")
    return res


def stat():
    """明るさ・彩度・動き・文字・顔を1本の表にまとめる（`shotstat.json`）。"""
    import cv2
    import numpy as np
    ocrd = json.loads((WORK / "ocr.json").read_text(encoding="utf-8")) \
        if (WORK / "ocr.json").exists() else {}
    fac = json.loads((WORK / "faces.json").read_text(encoding="utf-8")) \
        if (WORK / "faces.json").exists() else {}
    rows = []
    for name in SHOTS:
        for i, s in enumerate(SHOTS[name]["shots"]):
            r = dict(clip=name, i=i, start=s["start"], until=s["until"],
                     sec=round(s["until"] - s["start"], 2), motion=s["motion"])
            texts, nface, big, lum, sat = [], 0, 0.0, [], []
            for suf in ("_h", "", "_t"):
                key = f"{name}/{i:04d}{suf}"
                texts += ocrd.get(key) or []
                f = fac.get(key)
                if f:
                    nface = max(nface, f["n"])
                    big = max(big, f["big"])
                p = WORK / name / f"{i:04d}{suf}.jpg"
                im = cv2.imread(str(p)) if p.exists() else None
                if im is not None:
                    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
                    lum.append(float(np.median(hsv[:, :, 2])))
                    sat.append(float(np.median(hsv[:, :, 1])))
            r["lum"] = round(min(lum), 1) if lum else None
            r["sat"] = round(min(sat), 1) if sat else None
            r["face"] = nface
            r["facebig"] = big
            r["text"] = " / ".join(texts)[:160]
            r["bad"] = bool(BAD_WORDS.search(r["text"]))
            r["frames"] = len(lum)
            rows.append(r)
    dest = WORK / "shotstat.json"
    dest.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    miss = [r for r in rows if r["frames"] < 3]
    print(f"■ {len(rows)} ショット → {dest}")
    print(f"   文字が読めた {sum(1 for r in rows if r['text'])} 本"
          f"／うち NG 語 {sum(1 for r in rows if r['bad'])} 本")
    print(f"   顔が出た {sum(1 for r in rows if r['face'])} 本"
          f"／顔が画面の1/4より大きい {sum(1 for r in rows if r['facebig'] >= 0.25)} 本")
    if miss:
        print(f"   🔴 コマが3枚そろっていない {len(miss)} 本 "
              f"（測れていない＝合格にしない）: "
              + ", ".join(f"{r['clip']}#{r['i']}" for r in miss[:12]))
    return rows


def sheet(clip, page, grid=(4, 3), minsec=0.0):
    """目で見るシート（1枚 grid 枚ぶん）。**採否そのものではない・当たり付け**。"""
    from PIL import Image, ImageDraw
    sh = SHOTS[clip]["shots"]
    idx = [i for i, s in enumerate(sh) if s["until"] - s["start"] >= minsec]
    per = grid[0] * grid[1]
    part = idx[page * per:(page + 1) * per]
    if not part:
        print("そのページは空")
        return None
    cw, ch = 480, 270
    im = Image.new("RGB", (cw * grid[0], (ch + 22) * grid[1]), (16, 16, 18))
    d = ImageDraw.Draw(im)
    for k, i in enumerate(part):
        x, y = (k % grid[0]) * cw, (k // grid[0]) * (ch + 22)
        p = WORK / clip / f"{i:04d}.jpg"
        if p.exists():
            im.paste(Image.open(p).resize((cw, ch)), (x, y))
        s = sh[i]
        d.text((x + 6, y + ch + 4),
               f"#{i}  {s['start']:.0f}-{s['until']:.0f}s "
               f"({s['until'] - s['start']:.0f}s) m={s['motion']:.0f}",
               fill=(235, 235, 235))
    dest = WORK / f"sheet_{clip}_{page:02d}.jpg"
    im.save(dest, quality=88)
    print(f"■ {dest}  ショット {part[0]}〜{part[-1]}（{len(part)}枚）")
    return dest


SCAN = HERE / "out" / "jiko" / "kb1s"


def scan1s(clip=None):
    """🔴🔴 **1秒に1コマ、クリップの頭から尻まで**取る（1本につき通し読み1回）。

    ■ なぜショット単位の3コマでは足りないか（2026-09-08 に実測して分かった）
      ②の `shots.json` は 1秒刻みの標本から境目を出し、**`MIN_SHOT` より短い区間は
      前のショットに畳んでいる**。＝ **2秒だけのスレートがショットの中に埋まる。**
      実例：`240401-G-TL908-2303` の「#14 64〜76秒」の中の **67〜68秒が真っ黒の
      スレート**（OCR で `MEDIUM / BOW … DALI` が読める）。台帳には現れない。
      ⚠️ `footage.outside_shot()` は台帳を読むので、この穴に**構造上鳴らない**
      → [[feedback-gates-blind-spot-is-the-scan-direction]] と同じ形の穴。
    """
    names = [clip] if clip else list(SHOTS)
    for name in names:
        out = SCAN / name
        out.mkdir(parents=True, exist_ok=True)
        fps, dur = CLIPS[name]["fps"], CLIPS[name]["sec"]
        secs = list(range(int(dur)))
        if all((out / f"{s:04d}.jpg").exists() for s in secs):
            print(f"  {name}: すでに {len(secs)} 枚（飛ばす）", flush=True)
            continue
        tmp = out / "_raw"
        tmp.mkdir(exist_ok=True)
        for f in tmp.glob("*.jpg"):
            f.unlink()
        # 🔴 `select='eq(n,..)+…'` を秒数ぶん並べると **ffmpeg が
        #    「Cannot allocate memory」で落ちる**（451項で実測。105項でも落ちた）。
        #    ＝ `fps=1` を使う。**②の `shots.py` とまったく同じ標本の取り方**なので、
        #      出てくる i 枚目が台帳の i 秒とそろう。
        print(f"  {name}: {len(secs)} 秒ぶんを通し読み（fps=1）…", flush=True)
        r = subprocess.run(
            ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
             "-user_agent", UA, "-i", CLIPS[name]["url"],
             "-vf", f"fps=1,scale={CELL[0]}:{CELL[1]}",
             "-q:v", "3", str(tmp / "%04d.jpg")],
            capture_output=True, timeout=7200)
        got = sorted(tmp.glob("*.jpg"))
        secs = list(range(len(got)))
        if len(got) < int(dur) - 1:
            print(f"    🔴 {len(got)}/{len(secs)} ＝**測れていない**"
                  f"  {(r.stderr or b'')[-160:].decode('utf-8', 'replace')}", flush=True)
            continue
        for s, f in zip(secs, got):
            (out / f"{s:04d}.jpg").write_bytes(f.read_bytes())
            f.unlink()
        tmp.rmdir()
        print(f"    ✓ {len(secs)} 枚", flush=True)


def map1s(clip=None):
    """1秒ごとの「真っ暗・文字・顔・絵の変わり目」を測って `kb1s/map.json` に置く。"""
    import cv2
    import numpy as np
    dest = SCAN / "map.json"
    res = json.loads(dest.read_text(encoding="utf-8")) if dest.exists() else {}
    det = cv2.FaceDetectorYN.create(str(YUNET), "", (CELL[0], CELL[1]),
                                    score_threshold=0.6)
    for name in ([clip] if clip else list(SHOTS)):
        files = sorted((SCAN / name).glob("[0-9]*.jpg"))
        if not files or name in res:
            continue
        rows, prev = [], None
        for f in files:
            im = cv2.imread(str(f))
            h, w = im.shape[:2]
            det.setInputSize((w, h))
            _, bx = det.detect(im)
            g = cv2.cvtColor(cv2.resize(im, (64, 36)), cv2.COLOR_BGR2GRAY).astype(int)
            rows.append(dict(
                s=int(f.stem), lum=round(float(im.mean()), 1),
                face=0 if bx is None else len(bx),
                big=0.0 if bx is None or not len(bx)
                else round(max(float(x[3]) / h for x in bx), 2),
                d=None if prev is None else round(float(np.abs(g - prev).mean()), 1)))
            prev = g
        # 焼き込み文字（30枚ずつ PowerShell へ）
        txt = {}
        for i in range(0, len(files), 30):
            chunk = files[i:i + 30]
            r = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                 "-File", str(HERE / "tools" / "ocr_win.ps1"),
                 "-Files", ",".join(str(x) for x in chunk)],
                capture_output=True, timeout=900)
            raw = r.stdout or b""
            try:
                s = raw.decode("utf-8")
            except UnicodeDecodeError:
                s = raw.decode("cp932", errors="replace")
            cur = None
            for ln in s.splitlines():
                if ln.startswith("## "):
                    cur = int(Path(ln.split()[1]).stem)
                    txt.setdefault(cur, [])
                elif cur is not None and ln.strip():
                    txt[cur].append(ln.strip())
        for r0 in rows:
            r0["text"] = " / ".join(txt.get(r0["s"], []))[:120]
        res[name] = rows
        dest.write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
        dark = [r0["s"] for r0 in rows if r0["lum"] < 12]
        print(f"  {name}: {len(rows)} 秒／真っ暗 {len(dark)} 秒 {dark[:20]}", flush=True)
    return res


def sheet1s(clip, page=0, minsec=5.0, grid=(4, 4)):
    """1秒の地図から作るシート。**台帳のショットごとに、その真ん中の秒**を1枚ずつ並べる。

    ⚠️ 当たり付け専用（縮小してある）。採ると決めた区間は `verify` に通し、
       決め所のカットは原寸で1枚見る。
    """
    from PIL import Image, ImageDraw
    m = json.loads((SCAN / "map.json").read_text(encoding="utf-8"))[clip]
    by = {r["s"]: r for r in m}
    cand = []
    for i, s in enumerate(SHOTS[clip]["shots"]):
        if s["until"] - s["start"] < minsec:
            continue
        mid = int((s["start"] + s["until"]) / 2)
        r = by.get(mid)
        if r is None or is_card(r) or r["big"] >= 0.25:
            continue
        cand.append((i, mid, s))
    per = grid[0] * grid[1]
    part = cand[page * per:(page + 1) * per]
    if not part:
        print(f"そのページは空（候補 {len(cand)} 本）")
        return None
    cw, ch = 480, 270
    im = Image.new("RGB", (cw * grid[0], (ch + 20) * grid[1]), (14, 14, 16))
    d = ImageDraw.Draw(im)
    for k, (i, mid, s) in enumerate(part):
        x, y = (k % grid[0]) * cw, (k // grid[0]) * (ch + 20)
        p = SCAN / clip / f"{mid:04d}.jpg"
        if p.exists():
            im.paste(Image.open(p).resize((cw, ch)), (x, y))
        d.text((x + 5, y + ch + 4),
               f"#{i}  {s['start']:.0f}-{s['until']:.0f}s"
               f" ({s['until'] - s['start']:.0f}s) m={s['motion']:.0f}  [{mid}s]",
               fill=(240, 240, 240))
    dest = SCAN / f"sheet_{clip[:22]}_{page:02d}.jpg"
    im.save(dest, quality=88)
    print(f"■ {dest}  候補 {len(cand)} 本中 {page * per + 1}〜{page * per + len(part)}"
          f"（全 {-(-len(cand) // per)} 頁）")
    return dest


def windows(clip=None, minsec=6.0):
    """🔴 1秒の地図から「**続けて使える秒の帯**」を出す。`footage.USE` の (start, until) はここから採る。

    使えない秒 ＝ ①真っ暗（スレート・中票・溶暗） ②NG語が読める ③顔が画面の1/4より大きい
    ⚠️ ここを通った帯が「使ってよい」ではない。**中身は目で見る**。
    """
    m = json.loads((SCAN / "map.json").read_text(encoding="utf-8"))
    out = {}
    for name in ([clip] if clip else list(SHOTS)):
        rows = m.get(name)
        if not rows:
            print(f"  🔴 {name}: 1秒の地図が無い＝**測れていない**")
            continue
        ok = [not (is_card(r) or r["big"] >= 0.25) for r in rows]
        runs, a = [], None
        for i, v in enumerate(ok + [False]):
            if v and a is None:
                a = i
            elif not v and a is not None:
                if i - a >= minsec:
                    runs.append((a, i))
                a = None
        out[name] = runs
        print(f"  {name}: " + " ".join(f"{a}-{b}({b - a})" for a, b in runs))
    return out


# 🔴 目で見る前に機械で落とす条件。**「落とした」ではなく「落とせた理由」を残す**
#   ⚠️ これは当たり付け。ここを通ったショットが「使ってよい」という意味ではない。
def why_drop(r, minsec=5.0):
    if r["frames"] < 3:
        return "測れていない"                    # fail closed（0で埋めない）
    if r["sec"] < minsec:
        return "短い"
    if r["lum"] is not None and r["lum"] <= 5 and r["text"]:
        return "スレート/中票"                    # 黒地に文字＝B-Roll のスレート・説明札
    if r["facebig"] >= 0.25:
        return "顔の寄り"                        # 画面の高さの1/4より大きい顔
    if r["bad"]:
        return "NG語"
    return None


def pool(clips=None, minsec=5.0):
    """機械の網を通ったショットだけを (clip, i) で返す。"""
    rows = json.loads((WORK / "shotstat.json").read_text(encoding="utf-8"))
    ks = clips.split(",") if isinstance(clips, str) else clips
    return [(r["clip"], r["i"]) for r in rows
            if (ks is None or r["clip"] in ks) and not why_drop(r, minsec)]


def poolsheet(clips=None, page=0, minsec=5.0, grid=(4, 4)):
    """機械の網を通ったショットだけを並べたシート（**本ごとではなく、まとめて**）。"""
    from PIL import Image, ImageDraw
    cand = pool(clips, minsec)
    per = grid[0] * grid[1]
    part = cand[page * per:(page + 1) * per]
    if not part:
        print(f"そのページは空（候補 {len(cand)} 本）")
        return None
    cw, ch = 480, 270
    im = Image.new("RGB", (cw * grid[0], (ch + 20) * grid[1]), (14, 14, 16))
    d = ImageDraw.Draw(im)
    for k, (clip, i) in enumerate(part):
        x, y = (k % grid[0]) * cw, (k // grid[0]) * (ch + 20)
        p = WORK / clip / f"{i:04d}.jpg"
        if p.exists():
            im.paste(Image.open(p).resize((cw, ch)), (x, y))
        s = SHOTS[clip]["shots"][i]
        d.text((x + 5, y + ch + 4),
               f"{clip[:26]} #{i}  {s['start']:.0f}-{s['until']:.0f}s"
               f" ({s['until'] - s['start']:.0f}s) m={s['motion']:.0f}",
               fill=(240, 240, 240))
    dest = WORK / f"pool_{page:02d}.jpg"
    im.save(dest, quality=88)
    print(f"■ {dest}  候補 {len(cand)} 本中 {page * per + 1}〜{page * per + len(part)}"
          f"（全 {-(-len(cand) // per)} 頁）")
    return dest


def verify(clip, a, b, step=0.5):
    """🔴 採ると決めた区間を**全域**（step 秒刻み）で機械にかける。

    ⚠️ 3コマ（頭・中・尻）を見ただけでは、区間の途中に出る字や顔は見えない。
       5本目 pr01 の『THE END』はこの穴だった（[[feedback-absence-of-a-word-is-not-absence]]）。

    🔴🔴 **`-ss` を使ってはいけない。** `select` の `n` は**復号を始めてからの通し番号**なので、
       `-ss` で飛ばすと `n` が 0 から数え直しになり、**まったく別の秒を測ったまま
       「23コマ取れた」と合格を出す**（2026-09-08 に実際に踏んだ。54〜65秒を測ったつもりで
       107〜118秒を測っていた）。→ [[feedback-verify-your-own-instrument]]
       ＝ 頭から通しで読む。そのぶん遅いので、1本のクリップの範囲はまとめて渡すこと。
    """
    import cv2
    tmp = WORK / "_verify"
    if tmp.exists():
        for f in tmp.glob("*.jpg"):
            f.unlink()
    tmp.mkdir(parents=True, exist_ok=True)
    fps = CLIPS[clip]["fps"]
    ns = sorted({int(round(t * fps)) for t in
                 [a + i * step for i in range(int((b - a) / step) + 1)]})
    expr = "+".join(f"eq(n\\,{n})" for n in ns)
    subprocess.run(
        ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
         "-user_agent", UA, "-i", CLIPS[clip]["url"],
         "-vf", f"select='{expr}',scale={CELL[0]}:{CELL[1]}",
         "-vsync", "0", "-q:v", "3", str(tmp / "%04d.jpg")],
        capture_output=True, timeout=3600)
    got = sorted(tmp.glob("*.jpg"))
    if len(got) != len(ns):
        print(f"🔴 {clip} {a}-{b}: 渡した {len(ns)} / 出た {len(got)}"
              f" ＝**測れていない**")
        return None
    det = cv2.FaceDetectorYN.create(str(YUNET), "", (CELL[0], CELL[1]),
                                    score_threshold=0.6)
    faces, dark, jump, prev = [], [], [], None
    for k, f in enumerate(got):
        im = cv2.imread(str(f))
        h, w = im.shape[:2]
        det.setInputSize((w, h))
        _, bx = det.detect(im)
        if bx is not None and len(bx):
            faces.append((round(a + k * step, 1),
                          len(bx), round(max(float(x[3]) / h for x in bx), 2)))
        if im.mean() < 12:
            dark.append(round(a + k * step, 1))
        # 🔴 **範囲の中で絵が別物になっていないか**を step 秒刻みで見る。
        #    ②の境目は1秒刻みなので、`until` の直前1秒は**もう次のショット**でありうる
        #    （`shots.boundaries` は境目を「後ろ側の秒」に置く）。ここがその穴を塞ぐ。
        g = cv2.cvtColor(cv2.resize(im, (64, 36)), cv2.COLOR_BGR2GRAY).astype(int)
        if prev is not None:
            jump.append((round(a + k * step, 1), round(abs(g - prev).mean(), 1)))
        prev = g
    r = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
         "-File", str(HERE / "tools" / "ocr_win.ps1"),
         "-Files", ",".join(str(f) for f in got)], capture_output=True, timeout=900)
    raw = r.stdout or b""
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        txt = raw.decode("cp932", errors="replace")
    words, cur = [], None
    for ln in txt.splitlines():
        if ln.startswith("## "):
            cur = round(a + got.index(Path(ln.split()[1])) * step, 1) \
                if Path(ln.split()[1]) in got else None
        elif ln.strip():
            words.append(ln.strip())
    print(f"  {clip} {a}-{b}（{len(got)}コマ・{step}秒刻み）")
    print(f"    顔 {len(faces)} コマ" + (f" {faces[:8]}" if faces else ""))
    print(f"    真っ暗 {len(dark)} コマ" + (f" {dark[:8]}" if dark else ""))
    print(f"    文字 {len(words)} 行" + (f" {words[:6]}" if words else ""))
    # 🔴 絵の変わり方は**絶対値でなく、その区間の中での飛び抜け方**で見る。
    #    空撮の流し撮りは 0.5秒でも常に動くので、固定のしきい値では鳴らない／鳴りすぎる。
    med = sorted(x[1] for x in jump)[len(jump) // 2] if jump else 0.0
    top = sorted(jump, key=lambda x: -x[1])[:4]
    hot = [x for x in jump if x[1] > max(3.0 * med, 12.0)]
    print(f"    絵の動き 中央値 {med:.1f}／大きい順 {top}")
    print(f"    {'🔴' if hot else '✓'} 別の絵に切り替わった疑い {len(hot)} か所"
          + (f" {hot}" if hot else ""))
    return dict(faces=faces, dark=dark, words=words, jump=jump, hot=hot, n=len(got))


def selftest():
    """陽性対照。**本番の中身が空でも回ることを見る**（0件を調べて合格にしない）。"""
    ok = True
    # 1. 台帳が 6本目を向いているか
    if SHOTS_JSON.parent.name != "keybridge":
        print("🔴 台帳が keybridge を向いていない"); ok = False
    n = sum(len(v["shots"]) for v in SHOTS.values())
    print(f"  台帳 {len(SHOTS)} 本 / {n} ショット")
    if n != 355:
        print(f"🔴 ショット数が 355 でない（{n}）"); ok = False
    # 2. コマ番号が重ならず、順に増えるか
    for name in SHOTS:
        tg = targets(name)
        ns = [t[2] for t in tg]
        if ns != sorted(ns):
            print(f"🔴 {name}: コマ番号が順に並んでいない"); ok = False
        for fn, sec, k in tg:
            i = int(fn[:4])
            s = SHOTS[name]["shots"][i]
            if not (s["start"] - 1e-6 <= sec <= s["until"] + 1e-6):
                print(f"🔴 {name}#{i}{fn[4:]}: 秒がショットの外 {sec}"); ok = False
    # 3. NG 語の網が**当たるべき文に当たる**（陽性対照）
    for s in ("NTSB B-Roll", "Photo by Petty Officer", "WJZ 13 News",
              "Courtesy of the U.S. Coast Guard"):
        if not BAD_WORDS.search(s):
            print(f"🔴 NG 語の網が「{s}」に当たらない"); ok = False
    for s in ("the bridge collapsed", "Baltimore"):
        if BAD_WORDS.search(s):
            print(f"🔴 NG 語の網が「{s}」に当たってしまう"); ok = False
    # 4. 顔の検出が**読み込める**か。⚠️ 模型が無いなら「測れていない」＝落とす
    try:
        import cv2
        if not YUNET.exists():
            print(f"🔴 顔検出の模型が無い（{YUNET}）＝顔は測れていない"); ok = False
        else:
            cv2.FaceDetectorYN.create(str(YUNET), "", (CELL[0], CELL[1]))
            print("  顔検出器: 読めた")
    except Exception as e:                          # noqa: BLE001
        print(f"🔴 顔検出が動かない: {e}"); ok = False
    print("✓ selftest 通過" if ok else "🔴 selftest 失敗")
    return ok


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "--selftest":
        selftest()
    elif a[0] == "frames":
        frames(a[1] if len(a) > 1 else None)
    elif a[0] == "ocr":
        ocr(a[1] if len(a) > 1 else None)
    elif a[0] == "faces":
        faces(a[1] if len(a) > 1 else None)
    elif a[0] == "stat":
        stat()
    elif a[0] == "sheet":
        sheet(a[1], int(a[2]) if len(a) > 2 else 0)
    elif a[0] == "pool":
        poolsheet(a[1] if len(a) > 1 and a[1] != "-" else None,
                  int(a[2]) if len(a) > 2 else 0,
                  float(a[3]) if len(a) > 3 else 5.0)
    elif a[0] == "verify":
        verify(a[1], float(a[2]), float(a[3]))
    elif a[0] == "scan1s":
        scan1s(a[1] if len(a) > 1 else None)
    elif a[0] == "sheet1s":
        sheet1s(a[1], int(a[2]) if len(a) > 2 else 0)
    elif a[0] == "windows":
        windows(a[1] if len(a) > 1 and a[1] != "-" else None,
                float(a[2]) if len(a) > 2 else 6.0)
    elif a[0] == "map1s":
        map1s(a[1] if len(a) > 1 else None)
    else:
        raise SystemExit(__doc__)
