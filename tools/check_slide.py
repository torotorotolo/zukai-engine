# -*- coding: utf-8 -*-
"""**スライドに焼き込まれた文字**と、**切り方**の門番（4本目・2026-09-06 新設）。

■ なぜ要るか（⑤c 見る C の 🔴 20件のうち 16件がこの2つの穴に落ちた）
  `check_dup.py` は**こちらが描いた文字どうし**しか見ない。
  `check_burned.py` は解説書の**テキスト層**を読むが、4本目のスライドは
  「NIST が公開した動画のコマ」なので**テキスト層が無い**＝どちらも構造上鳴らない。

  G-09 … 注記 d が、画面に写っているスライド自身の英文と**同じ**（見る C で 11件）
  G-10 … 寄りすぎて、英文の行が**左端で語の途中から始まる**（見る C で 5件）
  G-13 … 焼き込みの英文が**字幕帯／見出し帯の中**に入る（pr04 の "Source: NIST…" が実例）

■ 🔴 ケンバーンズ（2026-09-06 に実測して分かったこと）
  `build_jiko.fit()` は z に **(1 + 0.055k)** を掛ける（k = その時刻 / 尺）。
  ＝**切り方はカットの頭と尻で違う**。`cuts/ss.py` の `focus()` は k=0 の値しか返さない。
  検品画像は `qa_shots` の k=0.92 の1枚（`cut_pr04.jpg` でエッジ相関 0.77 対 0.006 で確認）。
  → この門番は **k=0（いちばん広い）と k=1（いちばん狭い）の両端**で見る。
    ⚠️ 動画を当てたカットは寄りをかけない＝k=0 固定（`build_jiko.py` 328-334）。
       そのカットは画面に出るのが**動画のコマ**でスライドではないので、そもそも見ない。

■ OCR
  Windows の OCR（`tools/ocr_win.ps1`）。結果は `ref/surfside/ocr_slides.json` に貯める。
  ⚠️ OCR は誤字が出る（白箱の1字・斜体・小さい字は落ちる）。だから
     **「一致したら鳴らす」**（拾えなかった行は鳴らないだけ）に倒してある＝見逃しは残る。

使い方:
    python tools/check_slide.py --ocr     # OCR を取り直してキャッシュを作る（要 Windows）
    python tools/check_slide.py           # 検査
    python tools/check_slide.py --check   # 陽性対照。**本番の経路で**鳴り・戻して黙るのを見る
    python tools/check_slide.py --all     # ・（記録だけ）も出す
"""
import copy
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
OCR_JSON = HERE / "ref" / "surfside" / "ocr_slides.json"
W, H = 1920, 1080
BAND_TOP = 210          # 見出し帯の下端（jiko_style.BAND_T）
BAND_BOT = 900          # 字幕帯の上端（ルール §6）

# ── しきい値（本番 240カットに当てて、台帳の ⚠️ と ・ の境から決めた）──────
SIM = 0.80              # G-09：注記と焼き込み行の近さ
CONTAIN = 0.90          # G-09：短いほうがどれだけ長いほうに丸ごと入っているか
WINDOW = 3              # G-09：OCR は1文を複数行に割る＝**連続 N 行までつないで**比べる
MINLEN_EN = 12          # G-09：この字数未満の英文は見ない（"NIST" などの名前）
CLIP_CHARS = 8          # G-10：この字数以上の行が端で切れたときだけ言う
CLIP_PX = 12            # G-10：端からこれ以上食い込んで切れていたら言う（1字ぶん未満は無視）
CLIP_SEEN = 0.50        # G-10：**半分以上が見えていて頭が切れる**なら 🔴（それ未満は断片＝参考）
BAND_PX = 10            # G-13：帯にこれ以上入っていたら言う
BAND_TALL = 40          # G-13：帯の中の文字がこの高さ以上なら 🔴（台帳の ・ は 20〜26px）
BAND_WIDE = 800         # G-13：高さが足りなくても、これだけ横に長ければ 🔴（pr04 の Source 行）
OVER_W = 40             # G-14：この幅より狭い重なりは見ない（台帳の「15px 未満は据え置き」）
OVER_H = 12             # G-14：縦の重なりの下限
OVER_W2 = 90            # G-14：これ以上重なったら 🔴（それ未満は参考）


# ⚠️ Windows の OCR がよく取り違える字（**両側に同じ変換を掛ける**ので誤検出は増えない）
#    実例：p185 の "Analyses" が "AnaIyses"（l→大文字 I）／p133 の "of" が "0f"
CONFUSE = str.maketrans({"0": "o", "1": "l", "5": "s", "i": "l"})


def norm_en(s):
    """英文の比べ用。英数字だけ残して小文字にし、OCR の取り違えを畳む。"""
    return re.sub(r"[^a-z0-9]", "", (s or "").lower()).translate(CONFUSE)


def ratio(a, b):
    from difflib import SequenceMatcher
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def contained(a, b):
    """短いほうが長いほうに、どれだけ**丸ごと**入っているか（0〜1）。

    ⚠️ `ratio()` だけだと「注記が原文の一部を写した」場合に長さの差で薄まって落ちる
       （ep07 の d は画面の2行ぶんを1行に書いていたので 0.8 に届かなかった）。
    """
    from difflib import SequenceMatcher
    if not a or not b:
        return 0.0
    m = SequenceMatcher(None, a, b).find_longest_match(0, len(a), 0, len(b))
    return m.size / min(len(a), len(b))


# ── OCR キャッシュ ─────────────────────────────────────────
def run_ocr(files):
    """ocr_win.ps1 を1回呼んで {ファイル名: {"size":[w,h], "lines":[...]}} を作る。"""
    ps = HERE / "tools" / "ocr_win.ps1"
    r = subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(ps),
                        "-Files", ",".join(str(f) for f in files)],
                       capture_output=True, timeout=900)
    # ⚠️ PowerShell の標準出力は **cp932**（utf-8 で読むと黙って空になる。2026-09-06 実測）
    txt = r.stdout.decode("cp932", errors="replace")
    # 🔴 外部の道具の出力が読めなければ 0 で埋めずに止める（fail closed）
    if r.returncode != 0 or not txt.strip():
        raise RuntimeError(f"OCR が動かない: rc={r.returncode} "
                           f"{r.stderr.decode('cp932', 'replace')[-300:]}")
    out, cur = {}, None
    for line in txt.splitlines():
        m = re.match(r"^## (.+?) (\d+)x(\d+)$", line.strip())
        if m:
            cur = Path(m.group(1)).name
            out[cur] = dict(size=[int(m.group(2)), int(m.group(3))], lines=[])
            continue
        m = re.match(r"^\[(\d+),(\d+)-(\d+),(\d+)\] (.*)$", line.rstrip())
        if m and cur:
            x0, y0, x1, y1 = (int(m.group(i)) for i in range(1, 5))
            out[cur]["lines"].append(dict(box=[x0, y0, x1, y1], text=m.group(5)))
    if not out:
        raise RuntimeError("OCR の出力を1件も読めなかった（形式が変わった？）")
    return out


def load_ocr():
    if not OCR_JSON.exists():
        raise SystemExit(f"🔴 {OCR_JSON.name} が無い。先に `python tools/check_slide.py --ocr`")
    return json.loads(OCR_JSON.read_text(encoding="utf-8"))


# ── 切り方の幾何（build_jiko.fit と同じ式。k を外から渡せるようにしただけ）────
def crop_rect(sw, sh, box, k, bias, xbias, zoom):
    _, _, w, h = box
    z = max(w / sw, h / sh) * zoom * (1.0 + 0.055 * k)
    cw, ch = min(sw, w / z), min(sh, h / z)
    left, top = (sw - cw) * xbias, (sh - ch) * bias
    return dict(z=z, cw=cw, ch=ch, left=left, top=top, w=w, h=h, box=box)


def to_screen(bx, r):
    """原画の箱 [x0,y0,x1,y1] を画面座標へ。box の貼り位置ぶんずらす。"""
    ox, oy = r["box"][0], r["box"][1]
    sx = r["w"] / r["cw"]
    sy = r["h"] / r["ch"]
    return [ox + (bx[0] - r["left"]) * sx, oy + (bx[1] - r["top"]) * sy,
            ox + (bx[2] - r["left"]) * sx, oy + (bx[3] - r["top"]) * sy]


def spec_strings(spec):
    """そのカットで**こちらが描く**文字（見出し・副題・注記）を (どこ, 文字) で返す。"""
    out = []
    for key in ("t", "s"):
        if spec.get(key):
            out.append((key, spec[key]))
    for i, a in enumerate(spec.get("ann") or []):
        for key in ("t", "v", "d"):
            if a.get(key):
                out.append((f"ann{i + 1}.{key}", a[key]))
    return out


def cut_geom(cid, spec, ocr, photo_of, box_of, skip):
    """そのカットの (原画サイズ, OCR行, k=0 と k=1 の切り方)。見ないカットは None。"""
    if cid in skip:
        return None
    name = photo_of.get(cid)
    if not name:
        return None
    o = ocr.get(Path(name).name)
    if not o:
        return None
    sw, sh = o["size"]
    box = box_of[cid]
    kw = dict(bias=spec.get("bias", 0.5), xbias=spec.get("xbias", 0.5),
              zoom=spec.get("zoom", 1.0))
    return dict(name=Path(name).name, sw=sw, sh=sh, lines=o["lines"],
                rects={k: crop_rect(sw, sh, box, k, **kw) for k in (0.0, 1.0)})


def my_boxes(cid, jobs):
    """そのカットで**こちらが描いた文字**の箱（見出し・副題・注記）。

    `check_layout.boxes()` を借りる＝本番の `build_layers` の SVG から実測した箱。
    """
    import check_layout as CL
    out = []
    for k in (f"{cid}_lab",) + tuple(f"{cid}_a{i}" for i in range(1, 9)):
        if k in jobs:
            out.extend(CL.boxes(jobs[k], k))
    return out


def overlap(a, b):
    """2つの箱の重なり (幅, 高さ)。負なら離れている。"""
    return (min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1]))


def scan(spec_map, ocr, photo_of, box_of, skip, jobs=None):
    """🔴 本番も陽性対照もこの1本を通る（判定を2か所に書かない）。"""
    hits, softs = [], []
    for cid in sorted(spec_map):
        spec = spec_map[cid]
        g = cut_geom(cid, spec, ocr, photo_of, box_of, skip)
        if not g:
            continue
        mine = spec_strings(spec)
        vis_lines = []                       # 画面に少しでも入る行（上から順）
        for ln in g["lines"]:
            scr = {k: to_screen(ln["box"], g["rects"][k]) for k in (0.0, 1.0)}
            if not any(s[2] > 0 and s[0] < W and s[3] > 0 and s[1] < H
                       for s in scr.values()):
                continue
            vis_lines.append(dict(txt=ln["text"].strip(), box=ln["box"], scr=scr,
                                  vis={k: (s[2] > 0 and s[0] < W and s[3] > 0
                                           and s[1] < H) for k, s in scr.items()}))
        vis_lines.sort(key=lambda d: (d["box"][1], d["box"][0]))

        # ── G-09 注記が焼き込みの英文の写し ────────────────────
        # ⚠️ OCR は1文を複数行に割る。**連続 WINDOW 行までつないだ窓**と比べる
        windows = []
        for i in range(len(vis_lines)):
            for n in range(1, WINDOW + 1):
                if i + n > len(vis_lines):
                    break
                chunk = vis_lines[i:i + n]
                windows.append((" ".join(c["txt"] for c in chunk),
                                norm_en("".join(c["txt"] for c in chunk))))
        for where, mytxt in mine:
            for part in re.split(r"[／/｜|]", mytxt):
                p = norm_en(part)
                if len(p) < MINLEN_EN:
                    continue
                best = None
                for shown, en in windows:
                    if len(en) < MINLEN_EN:
                        continue
                    r, c = ratio(p, en), contained(p, en)
                    if (r >= SIM or c >= CONTAIN) and (best is None or r > best[0]):
                        best = (r, c, shown)
                if best:
                    hits.append((cid, "G-09 焼き込みの写し", part.strip(), where,
                                 f"画面の「{best[2]}」と 一致 {best[0]:.0%}／"
                                 f"取り込み {best[1]:.0%}"))
                    break

        # ── G-10 端で語の途中から／G-13 焼き込みが帯の中 ─────────
        for v in vis_lines:
            txt = v["txt"]
            if len(txt) < CLIP_CHARS:
                continue
            for k in (1.0, 0.0):
                if not v["vis"][k]:
                    continue
                x0, _, x1, _ = v["scr"][k]
                seen = (min(x1, W) - max(x0, 0)) / max(x1 - x0, 1)
                if x0 < -CLIP_PX and x1 > CLIP_PX:
                    row = (cid, "G-10 行頭が切れる", txt, f"k={k:.0f}",
                           f"左端で {abs(x0):.0f}px 欠ける・見えているのは "
                           f"{seen:.0%}（{g['name']}）")
                    (hits if seen >= CLIP_SEEN else softs).append(row)
                    break
                if x1 > W + CLIP_PX and x0 < W - CLIP_PX:
                    softs.append((cid, "G-10 行尻が切れる", txt, f"k={k:.0f}",
                                  f"右端で {x1 - W:.0f}px 欠ける（{g['name']}）"))
                    break
            for k in (0.0, 1.0):
                if not v["vis"][k]:
                    continue
                x0, y0, x1, y1 = v["scr"][k]
                if y1 > BAND_BOT + BAND_PX and y0 < H:
                    tall, wide = y1 - y0, min(x1, W) - max(x0, 0)
                    row = (cid, "G-13 字幕帯の中", txt, f"k={k:.0f}",
                           f"y {y0:.0f}〜{y1:.0f}・高さ {tall:.0f}px・幅 {wide:.0f}px")
                    (hits if (tall >= BAND_TALL or wide >= BAND_WIDE)
                     else softs).append(row)
                    break
                if y0 < BAND_TOP - BAND_PX and y1 > 0:
                    softs.append((cid, "G-13 見出し帯の裏", txt, f"k={k:.0f}",
                                  f"y {y0:.0f}〜{y1:.0f}（帯 〜{BAND_TOP}）"))
                    break

        # ── G-14 こちらの文字が、焼き込みの文字の上に載る ─────────
        # 台帳の ⚠️ でいちばん多い型（見る B・C で 16件）。check_dup は絵の中の文字を見ない
        if jobs is not None:
            for mb in my_boxes(cid, jobs):
                if len(mb[4].strip()) < 2:
                    continue
                for v in vis_lines:
                    if len(v["txt"]) < 3:
                        continue
                    for k in (0.0, 1.0):
                        if not v["vis"][k]:
                            continue
                        ow, oh = overlap(mb, v["scr"][k])
                        if ow >= OVER_W and oh >= OVER_H:
                            row = (cid, "G-14 焼き込みの上に載る", mb[4], mb[5],
                                   f"画面の「{v['txt']}」と {ow:.0f}×{oh:.0f}px 重なる"
                                   f"（k={k:.0f}）")
                            hard = ow >= OVER_W2 and not mb[5].endswith("_lab")
                            (hits if hard else softs).append(row)
                            break
                    else:
                        continue
                    break
    return hits, softs


# ── 本番の入力（scene_jiko から作る）────────────────────────
def production_inputs():
    import scene_jiko as S
    import footage as F
    spec_map = dict(S.SPEC)
    photo_of = {c: v[1] for c, v in S.PHOTO_CUTS.items()}
    box_of = {c: v[0] for c, v in S.PHOTO_CUTS.items()}
    # 動画のコマが出るカットはスライドが映らない＝見ない（still=True は写真が出るので見る）
    skip = {c for c, u in F.USE.items() if not u.get("still")}
    return spec_map, photo_of, box_of, skip


def jobs_for(spec_map):
    """🔴 **本番の経路** `S.SPEC → build_layers` でレイヤーの SVG を作る。

    陽性対照はここに細工した SPEC を通す＝判定も描画も本番と同じ道を通る。
    """
    import scene_jiko as S
    keep = S.SPEC
    try:
        S.SPEC = spec_map
        jobs, _ = S.build_layers(allow_missing=True)
    finally:
        S.SPEC = keep
    return jobs


def selfcheck():
    """陽性対照＝**本番の SPEC と本番の scan()** に違反を1件だけ入れて鳴らす。

    ⚠️ `check_dup.selfcheck()` は判定の核を別実装で持っており、`scan()` を直しても
       検算は緑のまま通る（2026-09-06 に確認）。ここは **scan() そのもの**を呼ぶ。
    ⚠️ 「件数が増えたか」では見ない。本番のカットは**もともと鳴っている**ので、
       寄せ方を変えた拍子に別の行が枠外へ出て件数が減り、規則が働いていても
       落ちて見える（c405 で実際に起きた）。
       → **狙った行が鳴るか**を行の文字で名指しし、かつ**素のままでは黙る**ことを見る。
    ⚠️ 試験台は規則ごとに探す。1枚のカットで4規則すべてを試せるとは限らない
       （c405 は本体枠の中に焼き込みの行が1本も無く G-14 を試せなかった）。
    """
    ocr = load_ocr()
    spec_map, photo_of, box_of, skip = production_inputs()

    def fired(sm, cid, kind, txt):
        """そのカットで、その規則が、**その行／その文字**で鳴ったか。"""
        h, sf = scan(sm, ocr, photo_of, box_of, skip, jobs_for(sm))
        # ⚠️ norm_en は非英字を落とす＝日本語の行では空文字になる。生の文字でも見る
        for x in h + sf:
            if x[0] != cid or not x[1].startswith(kind):
                continue
            if txt.strip() and (txt.strip() == x[2].strip() or txt.strip() in x[4]):
                return True
            a, b = norm_en(txt), norm_en(x[2])
            if a and b and (a in b or b in a):
                return True
        return False

    def candidates():
        """全画面で、焼き込みの行が画面に入っているカット（行の多い順）。"""
        out = []
        for c in sorted(spec_map):
            g = cut_geom(c, spec_map[c], ocr, photo_of, box_of, skip)
            if not g:
                continue
            bx = box_of[c]
            if bx[0] or bx[1] or bx[2] != W or bx[3] != H:
                continue
            vis = [l for l in g["lines"]
                   if (lambda sc: sc[2] > 0 and sc[0] < W and sc[3] > 0 and sc[1] < H)(
                       to_screen(l["box"], g["rects"][0.0]))]
            if vis:
                out.append((len(vis), c, g, vis))
        return [(c, g, v) for _, c, g, v in sorted(out, reverse=True)]

    def probe(kind, build):
        """`build(cid, g, vis)` が (細工した1カットぶんの SPEC, 狙う行の文字, 説明) を
        返すまでカットを渡り歩き、**入れると鳴る／戻すと黙る**を確かめる。"""
        for cid, g, vis in candidates():
            made = build(cid, g, vis)
            if not made:
                continue
            one, txt, note = made
            base = {cid: copy.deepcopy(spec_map[cid])}
            if fired(base, cid, kind, txt):      # 素で鳴る行は試験にならない
                continue
            if fired({cid: one}, cid, kind, txt):
                print(f"  ✓ {kind}（{cid}：{note}）… 入れると鳴り、戻すと黙る")
                return True
            print(f"  🔴 {kind}（{cid}：{note}）… 入れても鳴らない")
            return False
        print(f"  🔴 {kind} … 試せるカットが1枚も無い")
        return False

    def b09(cid, g, vis):
        en = [l for l in vis if len(norm_en(l["text"])) >= MINLEN_EN]
        if not en:
            return None
        one = copy.deepcopy(spec_map[cid])
        one["ann"] = [dict(t="原文", d=en[0]["text"])]
        return one, en[0]["text"], f"注記に「{en[0]['text'][:24]}」をそのまま書く"

    def b10(cid, g, vis):
        box = box_of[cid]
        sw, w = g["sw"], box[2]
        bz = max(box[2] / g["sw"], box[3] / g["sh"])
        longs = [l for l in g["lines"] if len(l["text"]) >= CLIP_CHARS
                 and l["box"][2] - l["box"][0] > 200]
        for L in sorted(longs, key=lambda l: l["box"][2] - l["box"][0], reverse=True):
            mid = (L["box"][0] + L["box"][2]) / 2
            if sw - mid < 60:
                continue
            one = copy.deepcopy(spec_map[cid])
            one["zoom"] = max(w / (sw - mid) / bz * 1.05, 1.0)
            cw = min(sw, w / (bz * one["zoom"]))
            one["xbias"] = min(1.0, max(0.0, mid / max(sw - cw, 1)))
            # ⚠️ 横だけ合わせても**縦で枠外**に出れば鳴らない（2026-09-06 に空振り）。
            #    狙う行が画面のまん中あたりに来る bias を逆算する
            ch = min(g["sh"], box[3] / (bz * one["zoom"]))
            top = (L["box"][1] + L["box"][3]) / 2 - ch / 2
            one["bias"] = min(1.0, max(0.0, top / max(g["sh"] - ch, 1)))
            gg = cut_geom(cid, one, ocr, photo_of, box_of, skip)
            sc = to_screen(L["box"], gg["rects"][1.0])
            if not (sc[3] > 0 and sc[1] < H):      # 縦に入っていなければ次の行へ
                continue
            return one, L["text"], (f"行の真ん中に左端（zoom {one['zoom']:.2f}・"
                                    f"bias {one['bias']:.2f}）")
        return None

    def b13(cid, g, vis):
        box = box_of[cid]
        sh, h = g["sh"], box[3]
        bz = max(box[2] / g["sw"], box[3] / g["sh"])
        ch = min(sh, h / bz)
        # ⚠️ bias は 0〜1 の按分＝top を負にできない。下端へ持って来られる行だけ
        cand = [l for l in g["lines"] if len(l["text"]) >= CLIP_CHARS
                and l["box"][1] >= 950 * ch / h and sh - ch > 1]
        for T in sorted(cand, key=lambda l: l["box"][3] - l["box"][1], reverse=True):
            one = copy.deepcopy(spec_map[cid])
            one["zoom"] = 1.0
            one["xbias"] = 0.5
            one["bias"] = min(1.0, max(0.0, (T["box"][1] - 950 * ch / h) / (sh - ch)))
            return one, T["text"], f"帯の中へ（bias {one['bias']:.2f}）"
        return None

    def b14(cid, g, vis):
        r0 = g["rects"][0.0]
        body = []
        for l in vis:
            sc = to_screen(l["box"], r0)
            if (sc[0] > 0 and sc[2] < W and sc[1] > BAND_TOP + 60
                    and sc[3] < BAND_BOT - 60 and len(l["text"]) >= CLIP_CHARS):
                body.append((l, sc))
        if not body:
            return None
        M, sc = max(body, key=lambda p: p[1][2] - p[1][0])
        one = copy.deepcopy(spec_map[cid])
        one["ann"] = [dict(t="かさなり試験の行です", ts=46)]
        one["side"] = "left" if sc[0] < W / 2 else "right"
        one["ann_y"] = round((sc[1] + sc[3]) / 2 + 14)
        return one, "かさなり試験の行です", f"注記を y={one['ann_y']} に置く"

    ok = probe("G-09", b09)
    ok &= probe("G-10", b10)
    ok &= probe("G-13", b13)
    ok &= probe("G-14", b14)

    a = crop_rect(3200, 1570, (0, 0, W, H), 0.0, 0.5, 0.5, 2.0)
    b = crop_rect(3200, 1570, (0, 0, W, H), 1.0, 0.5, 0.5, 2.0)
    narrower = b["cw"] < a["cw"] and abs(b["z"] / a["z"] - 1.055) < 1e-9
    ok &= narrower
    print(f"  {'✓' if narrower else '🔴'} 幾何：k=1 は k=0 の 1.055倍に寄る")
    print("  " + ("✓ 陽性対照 5/5" if ok else "🔴 陽性対照に落ちた"))
    return ok


def main(show_all=False):
    ocr = load_ocr()
    spec_map, photo_of, box_of, skip = production_inputs()
    hits, softs = scan(spec_map, ocr, photo_of, box_of, skip, jobs_for(spec_map))
    seen = sum(1 for c in spec_map
               if cut_geom(c, spec_map[c], ocr, photo_of, box_of, skip))
    print(f"■ スライドが映るカット {seen} 件を、k=0 と k=1 の両端で見た")
    # 🔴 **カットごと**にまとめる（行ごとに出すと1カットで8行になり、直す単位と合わない）
    by = {}
    for cid, kind, txt, where, why in hits:
        by.setdefault((cid, kind), []).append((txt, where, why))
    for (cid, kind) in sorted(by):
        rows = by[(cid, kind)]
        print(f"  🔴 {cid} {kind}（{len(rows)}件）")
        for txt, where, why in rows[:2] if not show_all else rows:
            print(f"      「{txt}」 {why}  [{where}]")
        if not show_all and len(rows) > 2:
            print(f"      … ほか {len(rows) - 2}件（--all で全部）")
    if show_all:
        for cid, kind, txt, where, why in softs:
            print(f"  ・ {cid} {kind}「{txt}」  {why}  [{where}]")
    kinds, cuts = {}, {}
    for h in hits:
        g = h[1].split()[0]
        kinds[g] = kinds.get(g, 0) + 1
        cuts.setdefault(g, set()).add(h[0])
    tail = "／".join(f"{k} {v}件（{len(cuts[k])}カット）" for k, v in sorted(kinds.items()))
    if hits:
        print(f"🔴 焼き込みの文字と切り方に粗（{tail or '0件'}／参考 {len(softs)}件）")
    else:
        print(f"✓ 焼き込みの文字と切り方は通った（参考 {len(softs)}件）")
    lab_summary(softs)
    return 1 if hits else 0


def lab_summary(softs):
    """🔴 2026-09-06（⑥）：**見出し・副題・出典が焼き込みの文字に載る件数を必ず表に出す。**

    なぜ：G-14 の判定は 297行で
        hard = ow >= OVER_W2 and not mb[5].endswith("_lab")
    としており、**`_lab`（見出し・副題・出典）の重なりは、どれだけ大きくても 🔴 にしない。**
    その結果 240件を超える「参考」の中に埋もれ、**誰も読まない**。
    c409 で「私の見出しが焼き込みの "As-Built Conditions" と重なって読めない」のに
    門番が 🔴0 と言った真因がこれだった（焼いた絵を見るまで分からなかった）。

    ⚠️ 判定そのものは変えていない（🔴 に格上げすると本番の 🔴 が 20件増えて意味が変わる）。
       **黙らせないことだけを直した。** 分類の見直しは次の題材の ⑤ でやる。
    """
    import re as _re
    lab = [r for r in softs if "G-14" in r[1] and r[3].endswith("_lab")]
    if not lab:
        return
    def w(msg):
        m = _re.search(r"と (\d+)×", msg)
        return int(m.group(1)) if m else 0
    big = [r for r in lab if w(r[4]) >= 200]
    print(f"⚠️ 見出し・副題・出典が焼き込みの文字に載る "
          f"{len(lab)}件（{len({r[0] for r in lab})}カット）"
          f"／うち重なり 200px 以上 {len(big)}件"
          f"　🔴 には数えない決まりなので、ここで別に出している（--lab で全件）")
    if "--lab" in sys.argv:
        for r in sorted(lab, key=lambda r: -w(r[4])):
            print(f"   {r[0]:<6} {w(r[4]):5}px 「{r[2][:26]}」 {r[4][:58]}")


if __name__ == "__main__":
    if "--ocr" in sys.argv:
        files = sorted((HERE / "ref" / "surfside").glob("tf_*.jpg")) + \
                sorted((HERE / "ref" / "surfside").glob("ss_*.jpg")) + \
                sorted((HERE / "ref" / "surfside").glob("fb_*.jpg"))
        data = run_ocr(files)
        OCR_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=1),
                            encoding="utf-8")
        n = sum(len(v["lines"]) for v in data.values())
        print(f"✓ OCR {len(data)} ファイル・{n} 行 → {OCR_JSON.relative_to(HERE)}")
        sys.exit(0)
    if "--check" in sys.argv:
        sys.exit(0 if selfcheck() else 1)
    sys.exit(main(show_all="--all" in sys.argv))
