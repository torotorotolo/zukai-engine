# -*- coding: utf-8 -*-
"""記録映画 410ショットの**中身**を機械で当たり付けし、目で確かめるシートを作る。

■ なぜ要るか（台本 §5-1 の1・§10 の1）
  ④台本の時点で「どのショットに何が写っているかは⑤bの仕事」と持ち越されている。
  ⚠️ **410ショットを1枚ずつ原寸で見ることはできない**（画像は枚数の2乗で効く）。
  → 先に**機械で見えるもの**を全部取り、目で見るのは残りだけにする。
     → [[feedback-gates-dont-see-text-burned-into-the-picture]]（目視の前に OCR＋幾何）

■ 機械で取れるもの
  1. **焼き込みの文字**（表題カード・クレジット・局のロゴ）＝ OCR。
     台本 §5-1 の1「局のロゴ・報道映像の混入を必ず見る」と、
     4本目 c703/c726 の「検品画像が表題カードそのもの」を**同じ網**で止める
  2. **明るさ**（夜の屋外か・屋内か・雪の屋外か）＝ 中央値と暗部の割合
  3. **動きの量**＝ `shots.json` の motion（1秒刻みの実測。この道具では取り直さない）
  4. **色味**＝ 彩度の中央値（記録映画は白黒に近いはずで、色が出るなら別素材の混入を疑う）

■ 使い方
    python tools/sl1_shots.py frames          # ショットごとに1コマ抜く（640x360）
    python tools/sl1_shots.py ocr             # 焼き込み文字を全ショットぶん取る
    python tools/sl1_shots.py stat            # 明るさ・彩度・動きの表
    python tools/sl1_shots.py sheet ph12 0    # 目で見るシート（1枚20コマ）
    python tools/sl1_shots.py --selftest

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
CLIP = HERE / "out" / "jiko" / "clip"
WORK = HERE / "out" / "jiko" / "shotscan"
SHOTS_JSON = HERE / "ref" / "sl1" / "shots.json"
CELL = (640, 360)
try:
    from footage import UA as _UA
except Exception:                                       # noqa: BLE001
    _UA = "Mozilla/5.0"
GRID = (5, 4)              # 1枚 20コマ＝3200x1440。**識別のための当たり付け**


def shots(clip):
    d = json.loads(SHOTS_JSON.read_text(encoding="utf-8"))
    return [(s["start"], s["until"], s["motion"]) for s in d[clip]["shots"]]


def _at(a, b):
    """そのショットの代表の秒。**頭は切り替わりの残りが写る**ので 30% の位置を採る。"""
    return a + (b - a) * 0.30


# 🔴🔴 2026-09-07（5本目 SL-1 ⑤c'・L-03/L-06）：**1ショット1コマでは足りない。**
#    pr01 に使った #137（1478〜1491秒）は、30% の位置（t=1482）では OCR が0件。
#    ところが **t=1490（終端の1秒前）では「THE END」「THE U.S. ATOMIC ENERGY
#    COMMISSION」が読める**。記録映画の終幕タイトルは **ディゾルブ**で1つ前の
#    ショットに重なって浮き上がるので、**ショットの尻でしか見えない**。
#    ＝「文字なし」と判定した #135 #136 #137 は、**尻を見ていなかっただけ**。
#    → 頭・中・尻の3コマを抜く。ファイル名は
#      `NNNN.jpg`（中＝これまでどおり。stat とシートはこれを使う）／
#      `NNNN_h.jpg`（頭）／`NNNN_t.jpg`（尻）。**番号とショットの対応は崩さない。**
def _positions(a, b):
    """そのショットから抜く秒。(接尾辞, 秒) の3つ。短いショットでも順序が崩れない。"""
    d = max(b - a, 0.0)
    head = a + min(0.5, d * 0.10)          # 切り替わりの残りを避けて頭
    mid = _at(a, b)                        # 30%（これまでの代表コマ）
    tail = b - min(1.0, d * 0.10)          # 🔴 尻の1秒前（SL-1 の THE END はここ）
    tail = max(tail, mid + 0.01)
    return [("_h", head), ("", mid), ("_t", tail)]


def frames(clip=None):
    """ショットごとに1コマ抜く。**1ショット1回の seek**（手元のファイルなので速い）。

    ⚠️ 最初は `select=between(t,…)+…` を1本の ffmpeg に渡したが、410項の式は
       **コマンドの長さの上限で落ちた**（exit 4294967284）。式を短くするのではなく、
       **番号とショットが1対1で対応する**書き方（`%04d` を自分で決める）に変えてある。
       ＝取りこぼしが起きても番号がずれない。
    """
    n = 0
    for name in ([clip] if clip else ["sl1_ph12", "sl1_ph3"]):
        src = CLIP / f"{name}.mp4"
        if not src.exists():
            # 🔴 2026-09-07（⑤c'）：手元に mp4 が無くても**URL から直に抜ける**
            #    （`footage._cut_stream` と同じやり方＝範囲取得。落とさない）。
            #    それまでは「無い」で黙って0枚になり、道具が回らなかった。
            import footage as _F
            c = _F.CLIPS.get(name)
            if not c:
                print(f"  🔴 {name} は footage.CLIPS に無い")
                continue
            src = c["url"]
            print(f"  ⚠️ {name}.mp4 が手元に無いので URL から抜く（{src[:56]}…）")
        src = str(src)
        out = WORK / name
        out.mkdir(parents=True, exist_ok=True)
        sh = shots(name)
        miss = []
        for i, (a, b, _mo) in enumerate(sh):
            for suf, sec in _positions(a, b):
                dest = out / f"{i:04d}{suf}.jpg"
                if dest.exists():
                    continue
                cmd = ["ffmpeg", "-y", "-nostdin", "-hide_banner", "-loglevel", "error",
                       "-user_agent", _UA, "-ss", f"{sec:.2f}", "-i", src,
                       "-frames:v", "1",
                       "-vf", f"scale={CELL[0]}:{CELL[1]}", "-q:v", "4", str(dest)]
                subprocess.run(cmd, capture_output=True, timeout=300)
                if not dest.exists():
                    miss.append(f"{i}{suf}")
            if (i + 1) % 40 == 0:
                print(f"    {name}: {i + 1}/{len(sh)}", flush=True)
        got = sorted(out.glob("*.jpg"))
        print(f"  {name}: ショット {len(sh)} 本 → コマ {len(got)} 枚"
              f"（1ショット3コマ＝頭・中・尻）"
              + (f"  🔴 取れなかった {miss}" if miss else ""))
        n += len(got)
    print(f"■ 合計 {n} 枚 → {WORK}")
    return n


def ocr(clip=None):
    """焼き込みの文字を全ショットぶん取る（Windows の OCR）。**30枚ずつ渡す**。"""
    res = {}
    for name in ([clip] if clip else ["sl1_ph12", "sl1_ph3"]):
        files = sorted((WORK / name).glob("*.jpg"))
        if not files:
            print(f"  🔴 {name}: コマがまだ無い（先に frames）")
            continue
        for i in range(0, len(files), 30):
            chunk = files[i:i + 30]
            r = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
                 "-File", str(HERE / "tools" / "ocr_win.ps1"),
                 "-Files", ",".join(str(f) for f in chunk)],
                capture_output=True, timeout=900)
            # 🔴 `text=True` で受けると **cp932 で落ちる**（2026-09-07 実測：
            #    211/410 枚で UnicodeDecodeError。しかも**残りが黙って0件**になる）。
            #    PowerShell の出力は端末の符号化なので、こちらで受け直す。
            #    → [[feedback-verify-your-own-instrument]]（selftest が通っても本番の経路は別）
            raw = r.stdout or b""
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
            print(f"  {name}: {i + len(chunk)}/{len(files)}", flush=True)
    dest = WORK / "ocr.json"
    dest.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    withtext = sum(1 for v in res.values() if v)
    print(f"■ OCR {len(res)} 枚（文字が出た {withtext} 枚）→ {dest}")
    return res


# 🔴 出してはいけない絵の目印。**表題カード・クレジット・局のロゴ**
#   4本目 c703/c726 の「検品画像が表題カードそのもの」を、コマの側から止める網。
BAD_WORDS = re.compile(
    r"(?i)\b(the end|end of|produced|directed|photograph|narrat|courtesy|"
    r"copyright|presented|newsreel|movietone|paramount|universal|"
    r"phase\s+[i1]|classified|confidential|restricted|official use)\b")


def stat():
    """明るさ・彩度・動き・焼き込み文字の表を作る（`shotstat.json`）。"""
    from PIL import Image, ImageStat
    ocr_d = {}
    p = WORK / "ocr.json"
    if p.exists():
        ocr_d = json.loads(p.read_text(encoding="utf-8"))
    rows = []
    for name in ("sl1_ph12", "sl1_ph3"):
        sh = shots(name)
        # 明るさ等は**中のコマ**（`NNNN.jpg`）で測る（これまでと同じ値になる）
        files = sorted(f for f in (WORK / name).glob("*.jpg") if "_" not in f.stem)
        if len(files) != len(sh):
            print(f"  ⚠️ {name}: コマ {len(files)} ≠ ショット {len(sh)}。"
                  f"番号の対応が崩れるので stat は出さない")
            continue
        for i, (f, (a, b, mo)) in enumerate(zip(files, sh)):
            im = Image.open(f).convert("RGB")
            g = im.convert("L")
            st = ImageStat.Stat(g)
            hsv = im.convert("HSV").split()[1]
            # 🔴 文字は**頭・中・尻の3コマぶんを合わせて**見る（L-03：終幕タイトルは
            #    ディゾルブで尻にしか出ない。中の1コマだけだと「文字なし」になる）
            lines = []
            for _suf in ("_h", "", "_t"):
                lines += ocr_d.get(f"{name}/{f.stem}{_suf}", [])
            # OCR の行は「x0,y0,x1,y1<TAB>文字」の形。文字だけ取る
            words = " ".join(ln.split("\t")[-1] for ln in lines)
            rows.append(dict(clip=name, idx=i, start=round(a, 1), until=round(b, 1),
                             sec=round(b - a, 1), motion=round(mo, 2),
                             lum=round(st.mean[0], 1),
                             dark=round(sum(g.histogram()[:48]) / (g.width * g.height), 3),
                             sat=round(ImageStat.Stat(hsv).mean[0], 1),
                             text=words[:120],
                             bad=bool(BAD_WORDS.search(words))))
    dest = WORK / "shotstat.json"
    dest.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    nb = sum(1 for r in rows if r["bad"])
    nt = sum(1 for r in rows if r["text"])
    print(f"■ {len(rows)} ショット（文字あり {nt}／🔴 表題カード等の疑い {nb}）→ {dest}")
    return rows


# 🔴 使ってはいけないショット（OCR で機械が名指しした・目で見る前に外す）
#    表題カード／NARA の収蔵カード／出所カード／制作クレジット／End of Recording。
#    4本目 c703・c726 の「検品画像が表題カードそのもの」を、**選ぶ側**で止める。
#    ⚠️ #269（`SECOND PART TO FOLLOW`）は OCR が `SECO 關 PA ー` としか読めず
#       BAD_WORDS に当たらなかった。**目で見て足した**（機械の網は目視を置き換えない）。
BANNED = {
    "sl1_ph12": {0, 1, 138},
    "sl1_ph3": {0, 1, 2, 3, 269, 270},
}

# シートは長辺 1568px まで（それを超えると受け手が縮めるので、1コマの実効画素が減る）
SHEET_LONG = 1568


def candidates(clip, minsec=10.0, maxsec=1e9):
    """使える見込みのあるショット番号。**禁止札と短すぎるものを機械で外す**。"""
    return [i for i, (a, b, _m) in enumerate(shots(clip))
            if minsec <= b - a < maxsec and i not in BANNED[clip]]


def sheet(clip, page, grid=(4, 3), minsec=10.0, maxsec=1e9):
    """目で見るシート。**当たりを付けるためのもので、検品ではない。**

    ⚠️ 1コマ 392px は「何が写っているか」を決めるには足りるが、
       **粗を見つけるには足りない**。採ったショットは ⑤c で焼いた絵を原寸で見る。
    """
    from PIL import Image, ImageDraw
    sh = shots(clip)
    idxs = candidates(clip, minsec, maxsec)
    per = grid[0] * grid[1]
    sel = idxs[page * per:(page + 1) * per]
    if not sel:
        print(f"  🔴 そのページは無い（候補 {len(idxs)} 本／{-(-len(idxs) // per)} 枚）")
        return None
    cw = SHEET_LONG // grid[0]
    ch = round(cw * CELL[1] / CELL[0])
    W, H = cw * grid[0], (ch + 22) * grid[1]
    out = Image.new("RGB", (W, H), (16, 16, 18))
    d = ImageDraw.Draw(out)
    for k, i in enumerate(sel):
        a, b, mo = sh[i]
        x, y = (k % grid[0]) * cw, (k // grid[0]) * (ch + 22)
        im = Image.open(WORK / clip / f"{i:04d}.jpg").resize((cw, ch), Image.LANCZOS)
        out.paste(im, (x, y + 22))
        d.text((x + 5, y + 5), f"#{i:03d} {a:.0f}-{b:.0f}s({b - a:.0f}s)",
               fill=(240, 240, 240))
    tag = f"{int(minsec)}s" if maxsec > 1e8 else f"{int(minsec)}-{int(maxsec)}s"
    dest = WORK / f"sheet_{clip}_{tag}_{page:02d}.jpg"
    out.save(dest, quality=90)
    print(f"  {dest}  {W}x{H}  {len(sel)}コマ  "
          f"（候補 {len(idxs)} 本中 {page * per + 1}〜{page * per + len(sel)}）")
    return dest


def selftest():
    """陽性対照。**判定に使う関数そのもの**を、作り物の入力で鳴らす。"""
    ok = []

    def chk(name, got, want=True):
        ok.append(bool(got) == bool(want))
        print(f"  {'✓' if ok[-1] else '🔴'} {name}")

    chk("表題カードの語を拾う（THE END）", BAD_WORDS.search("THE END"))
    chk("局のクレジットを拾う（Movietone News）", BAD_WORDS.search("Movietone News"))
    chk("区分の印を拾う（OFFICIAL USE ONLY）", BAD_WORDS.search("official use only"))
    chk("ふつうの現場の看板では鳴らない（AREA II）",
        BAD_WORDS.search("ARA II AREA"), False)
    chk("語の途中では鳴らない（bend ≠ the end）", BAD_WORDS.search("bending"), False)
    # 代表の秒＝ショットの 30% の位置（頭の切り替わりを避ける）
    chk("代表の秒は頭から 30%（10〜20秒 → 13.0秒）", abs(_at(10, 20) - 13.0) < 1e-6)
    chk("1秒のショットでも中に入る（5〜6秒 → 5.3秒）",
        5.0 < _at(5, 6) < 6.0)
    # 🔴 頭・中・尻の3コマ（L-03：SL-1 の終幕タイトルは #137 の t=1490 でしか読めない）
    ph = dict(_positions(1478.0, 1491.0))
    chk("尻のコマは終端の1秒前（#137 → 1490.0秒）", abs(ph["_t"] - 1490.0) < 1e-6)
    chk("中のコマはこれまでどおり 30%（#137 → 1481.9秒）",
        abs(ph[""] - 1481.9) < 1e-6)
    chk("3コマの秒は 頭 < 中 < 尻 の順", ph["_h"] < ph[""] < ph["_t"])
    sh0 = _positions(100.0, 100.2)      # 0.2秒しかないショットでも順序が崩れない
    chk("短いショットでも 頭 < 中 < 尻（0.2秒）",
        sh0[0][1] < sh0[1][1] < sh0[2][1])
    chk("3コマとも枠の中（0.2秒）",
        100.0 <= sh0[0][1] and sh0[2][1] <= 100.2 + 1e-9)
    chk("接尾辞は 中だけ空（stat とシートは NNNN.jpg を使う）",
        [x for x, _ in _positions(0, 10)] == ["_h", "", "_t"])
    if SHOTS_JSON.exists():
        chk("ショット表が読める（ph12 は 139本）", len(shots("sl1_ph12")) == 139)
        chk("ショット表が読める（ph3 は 271本）", len(shots("sl1_ph3")) == 271)
    # 🔴 OCR そのものの陽性対照。**「文字が0枚」は「文字が無い」ではない**。
    #    2026-09-07 実測：`text=True` で受けていたので cp932 で落ち、410枚のうち
    #    211枚で止まり、**残りが黙って0件**になっていた（文字ありは 2 → 直して 25）。
    ctrl = HERE / "ref" / "sl1" / "anl_p001_cover.png"
    if ctrl.exists():
        r = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-File", str(HERE / "tools" / "ocr_win.ps1"), "-Files", str(ctrl)],
            capture_output=True, timeout=300)
        txt = (r.stdout or b"").decode("cp932", errors="replace")
        chk("OCR が英字を読む（表紙に ARGONNE がある）", "ARGONNE" in txt)
        chk("OCR の出力を cp932 で受けても落ちない", len(txt) > 200)
    good = all(ok)
    print("  " + (f"✓ 陽性対照 {len(ok)}/{len(ok)}" if good
                  else f"🔴 陽性対照 {sum(ok)}/{len(ok)} で落ちた"))
    return good


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(0 if selftest() else 1)
    cmd = a[0] if a else ""
    if cmd == "frames":
        frames(a[1] if len(a) > 1 else None)
    elif cmd == "ocr":
        ocr(a[1] if len(a) > 1 else None)
    elif cmd == "stat":
        stat()
    elif cmd == "sheet":
        ms = float(a[3]) if len(a) > 3 else 10.0
        xs = float(a[4]) if len(a) > 4 else 1e9
        if a[2] == "all":
            n = len(candidates("sl1_" + a[1], ms, xs))
            for p in range(-(-n // 12)):
                sheet("sl1_" + a[1], p, minsec=ms, maxsec=xs)
        else:
            sheet("sl1_" + a[1], int(a[2]), minsec=ms, maxsec=xs)
    else:
        print(__doc__)
