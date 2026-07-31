# -*- coding: utf-8 -*-
"""合成済みの wav から「そのモーラが本当に鳴っているか」を**測る**道具。

■ なぜ作ったか
  カズヤくんが冒頭の「10時47分」を「じゅうじ よんじゅうなな」と聞いた。
  ところが `audio/kana_log.txt` にはちゃんと `ヨンジュウナナフン` と出ている。
  **エンジンの読みデータは正しいのに耳では消えている**という状態がありうる
  （日本語の「フ」は無声両唇摩擦音で、母音が無声化すると音量がほぼ無い）。

  ここで辞書を触ると、素で正しく読める語を壊す（「18本→じゅうはちほん」の前科）。
  だから**まず測る**。

■ 何を測るか（耳の代わり）
  10ms ごとに 3 つの量を出す。モーラは音の種類で帯域が違うので見分けられる。
    lo  … 80〜400Hz    … 鼻音「ン」「ナ」「マ」の murmur が出る帯
    hi  … 2000〜9000Hz … 無声摩擦「フ」「シ」「ス」が出る帯
    rms … 全帯域の音量（dBFS）
  「フン」が鳴っていれば、最後の母音のあとに
    ① hi が立つ短い区間（フ）→ ② lo だけが残る区間（ン）→ ③ 無音
  という 3 段が必ず出る。①②が無ければ本当に消えている。

■ 使い方
    python tools/check_mora.py audio/pr01.wav --to=5.4
    python tools/check_mora.py audio/pr01.wav --from=3.6 --to=5.2 --plot
    python tools/check_mora.py audio/c117.wav --tail          … 文の最後だけ見る
    python tools/check_mora.py --compare pr01 c117 c114 c116  … 語尾を並べて比べる

⚠️ 数値は**同じ話者・同じ話速の別カットと比べて**読む。絶対値には意味が無い。
"""
import sys
import wave
from pathlib import Path

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent.parent
AUD = HERE / "audio"

WIN = 0.025          # 窓 25ms
HOP = 0.010          # 10ms ごと
LO = (80, 400)       # 鼻音の murmur
HI = (2000, 9000)    # 無声摩擦
SIL = -46.0          # これ以下は無音とみなす（dBFS）


def load(path):
    with wave.open(str(path), "rb") as w:
        sr, n, sw, ch = w.getframerate(), w.getnframes(), w.getsampwidth(), w.getnchannels()
        raw = w.readframes(n)
    if sw != 2:
        raise SystemExit(f"{path}: 16bit の wav だけ読めます（sampwidth={sw}）")
    x = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
    if ch > 1:
        x = x.reshape(-1, ch).mean(axis=1)
    return x, sr


def frames(x, sr):
    """(時刻, rms_dB, lo, hi) を 10ms ごとに返す。lo/hi は全帯域に対する割合。"""
    nw, nh = int(WIN * sr), int(HOP * sr)
    if len(x) < nw:
        return np.zeros((0, 4))
    win = np.hanning(nw).astype(np.float32)
    idx = np.arange(0, len(x) - nw, nh)
    seg = np.stack([x[i:i + nw] * win for i in idx])
    sp = np.abs(np.fft.rfft(seg, axis=1)) ** 2
    fr = np.fft.rfftfreq(nw, 1 / sr)
    tot = sp.sum(axis=1) + 1e-12
    lo = sp[:, (fr >= LO[0]) & (fr < LO[1])].sum(axis=1) / tot
    hi = sp[:, (fr >= HI[0]) & (fr < HI[1])].sum(axis=1) / tot
    rms = 20 * np.log10(np.sqrt((seg ** 2).mean(axis=1)) + 1e-12)
    return np.stack([idx / sr, rms, lo, hi], axis=1)


def bar(v, w=18, hi=1.0):
    k = int(max(0.0, min(1.0, v / hi)) * w)
    return "█" * k + "·" * (w - k)


def tail_window(f, pad=1.6):
    """最後に音が鳴っている場所から pad 秒ぶん手前を返す。"""
    voiced = f[f[:, 1] > SIL]
    if not len(voiced):
        return f[0, 0], f[-1, 0]
    end = voiced[-1, 0]
    return max(f[0, 0], end - pad), min(f[-1, 0], end + 0.30)


def show(path, t0=None, t1=None, tail=False):
    x, sr = load(path)
    f = frames(x, sr)
    if tail:
        t0, t1 = tail_window(f)
    t0 = f[0, 0] if t0 is None else t0
    t1 = f[-1, 0] if t1 is None else t1
    sel = f[(f[:, 0] >= t0) & (f[:, 0] <= t1)]
    print(f"── {Path(path).name}  {t0:.2f}〜{t1:.2f}s "
          f"（全長 {len(x) / sr:.2f}s・{sr}Hz）")
    print("   時刻    dBFS  低域80-400Hz(鼻音)     高域2k-9k(無声摩擦)   判定")
    for t, rms, lo, hi in sel:
        if rms <= SIL:
            kind = "無音"
        elif hi > 0.30 and lo < 0.25:
            kind = "★摩擦(フ/シ/ス)"
        elif lo > 0.55 and rms < -30:
            kind = "★鼻音のみ(ン)"
        elif lo > 0.40:
            kind = "有声(母音/鼻音)"
        else:
            kind = "有声"
        print(f"  {t:6.3f} {rms:7.1f}  {bar(lo)} {lo:4.2f}  "
              f"{bar(hi)} {hi:4.2f}  {kind}")


def segments(f):
    """無音で区切って、鳴っている区間の一覧を返す。"""
    on = f[:, 1] > SIL
    out, s = [], None
    for i, v in enumerate(on):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if f[i - 1, 0] - f[s, 0] > 0.08:
                out.append((f[s, 0], f[i - 1, 0]))
            s = None
    if s is not None:
        out.append((f[s, 0], f[-1, 0]))
    return out


def summarize(path):
    """語尾の3段（有声 → 摩擦 → 鼻音）が揃っているかを1行で出す。"""
    x, sr = load(path)
    f = frames(x, sr)
    segs = segments(f)
    if not segs:
        return None
    a, b = segs[-1]
    sel = f[(f[:, 0] >= a) & (f[:, 0] <= b)]
    # 最後の 0.45 秒を見る（フン ＝ おおむね 0.25〜0.40 秒）
    tailsel = sel[sel[:, 0] >= b - 0.45]
    fric = tailsel[(tailsel[:, 3] > 0.30) & (tailsel[:, 2] < 0.25)]
    nasal = tailsel[(tailsel[:, 2] > 0.55) & (tailsel[:, 1] < -30)]
    return dict(name=Path(path).stem, last=(a, b), dur=b - a,
                fric_ms=len(fric) * HOP * 1000, nasal_ms=len(nasal) * HOP * 1000,
                fric_at=(fric[0, 0] if len(fric) else None),
                nasal_at=(nasal[0, 0] if len(nasal) else None),
                tail_peak_hi=float(tailsel[:, 3].max()) if len(tailsel) else 0.0)


def compare(names):
    print("語尾の 0.45 秒に「無声摩擦（フ）」と「鼻音だけ（ン）」が出ているか")
    print(f"{'カット':<8}{'最後の発話区間':>18}{'摩擦ms':>8}{'鼻音ms':>8}"
          f"{'高域ピーク':>10}  判定")
    for n in names:
        p = AUD / f"{n}.wav"
        if not p.exists():
            print(f"{n:<8}  🔴 {p} が無い")
            continue
        r = summarize(p)
        ok = r["fric_ms"] >= 20 and r["nasal_ms"] >= 20
        mark = "✓ フンが鳴っている" if ok else "🔴 語尾が欠けている疑い"
        if r["fric_ms"] >= 20 and r["nasal_ms"] < 20:
            mark = "△ 摩擦はあるが鼻音が弱い"
        if r["fric_ms"] < 20 and r["nasal_ms"] >= 20:
            mark = "△ 鼻音はあるが摩擦が弱い"
        print(f"{r['name']:<8}{r['last'][0]:7.2f}〜{r['last'][1]:5.2f}s"
              f"{r['fric_ms']:8.0f}{r['nasal_ms']:8.0f}{r['tail_peak_hi']:10.2f}  {mark}")


# ── ★モーラ境界と実音を突き合わせる（いちばん確実な測り方） ──────────
# エンジンの `audio_query` は**モーラ1つずつの長さ**（consonant_length / vowel_length）を
# 返す。そこから「フ」「ン」が鳴るはずの秒を正確に出し、**その区間の音を測る**。
# 区間の切り出しを目分量でやらずに済むので、判定が揺れない。
def align(text, speed=None, speaker=None):
    """text を合成し、モーラごとに (かな, 開始, 終了, dBFS, 低域, 高域) を返す。"""
    import io
    import json
    import urllib.parse
    import urllib.request

    sys.path.insert(0, str(Path(__file__).parent))
    import narration as N

    sp = speaker or N.SPEAKER
    sd = N.SPEED if speed is None else speed
    q = json.loads(N.post("audio_query", None,
                          f"speaker={sp}&text={urllib.parse.quote(text)}").read())
    q["speedScale"] = sd
    wav = N.post("synthesis", q, f"speaker={sp}").read()
    with wave.open(io.BytesIO(wav)) as w:
        sr = w.getframerate()
        x = (np.frombuffer(w.readframes(w.getnframes()), dtype="<i2")
             .astype(np.float32) / 32768.0)
    f = frames(x, sr)

    # モーラの開始秒。speedScale は**全部の長さを割る**（0.95 なら伸びる）
    rows, t = [], q["prePhonemeLength"] / sd
    for ap in q["accent_phrases"]:
        for m in ap["moras"]:
            d = ((m.get("consonant_length") or 0.0) + m["vowel_length"]) / sd
            rows.append([m["text"], t, t + d, m["vowel"], m["pitch"]])
            t += d
        if ap.get("pause_mora"):
            d = ap["pause_mora"]["vowel_length"] / sd
            rows.append(["（間）", t, t + d, "pau", 0.0])
            t += d
        else:
            rows.append(["／", t, t, "", 0.0])          # アクセント句の切れ目
    out = []
    for text_m, a, b, vowel, pitch in rows:
        if b <= a:
            out.append((text_m, a, b, None, None, None, vowel, pitch))
            continue
        sel = f[(f[:, 0] >= a) & (f[:, 0] < b)]
        if not len(sel):
            sel = f[np.argmin(np.abs(f[:, 0] - a))][None, :]
        out.append((text_m, a, b, float(sel[:, 1].max()), float(sel[:, 2].mean()),
                    float(sel[:, 3].max()), vowel, pitch))
    return out, x, sr, wav, t


def show_align(text, speed=None, keep=None):
    rows, x, sr, wav, total = align(text, speed=speed)
    if keep:
        Path(keep).write_bytes(wav)
    print(f"「{text}」  話速 {speed if speed is not None else '既定'}  "
          f"合成長 {len(x) / sr:.2f}s")
    print(f"{'かな':<5}{'開始':>7}{'終了':>7}{'長さms':>8}{'最大dB':>8}"
          f"{'低域':>6}{'高域':>6}  ")
    for k, a, b, db, lo, hi, vowel, pitch in rows:
        if db is None:
            print(f"{k:<5}{a:7.3f}{'':>7}{'':>8}{'':>8}{'':>6}{'':>6}")
            continue
        # 無声母音（A/I/U/E/O が大文字）はエンジン自身が「無声化する」と言っている印
        dev = "  ← 無声化（母音を鳴らさない）" if vowel and vowel.isupper() else ""
        weak = ""
        if db < -34:
            weak = "  🔴 ほぼ聞こえない"
        elif db < -28:
            weak = "  ⚠️ 弱い"
        print(f"{k:<5}{a:7.3f}{b:7.3f}{(b - a) * 1000:8.0f}{db:8.1f}"
              f"{lo:6.2f}{hi:6.2f}{dev}{weak}")
    return rows


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--align" in args:
        i = args.index("--align")
        sp = next((float(a.split("=")[1]) for a in args if a.startswith("--speed=")), None)
        kp = next((a.split("=")[1] for a in args if a.startswith("--keep=")), None)
        show_align(args[i + 1], speed=sp, keep=kp)
        sys.exit(0)
    if "--compare" in args:
        i = args.index("--compare")
        compare(args[i + 1:])
        sys.exit(0)
    src = next((a for a in args if not a.startswith("-")), None)
    if not src:
        raise SystemExit(__doc__)
    kw = {}
    for a in args:
        if a.startswith("--from="):
            kw["t0"] = float(a.split("=")[1])
        elif a.startswith("--to="):
            kw["t1"] = float(a.split("=")[1])
        elif a == "--tail":
            kw["tail"] = True
    show(src, **kw)
