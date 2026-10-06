# -*- coding: utf-8 -*-
r"""check_aq_audio.py — ゆっくり（AquesTalk）で合成した音を**機械で**確かめる門番（14本目 ⑤a-2・2026-09-28 新設）。

  python tools/check_aq_audio.py            … audio/narration.json・audio/<cid>.wav・合成キャッシュを全行で当たる
  python tools/check_aq_audio.py --stats    … 行ごとの数（声の高さ・音量・無音・速さ）の分布と外れた行
  python tools/check_aq_audio.py --selftest … 陽性・陰性対照（アプリも audio/ も使わない）

■ なぜ要るか
  事故検証chは14本目から**音声だけの試聴（⑤a'）をしない**＝音は本編の試写で映像と一緒に確かめる（2026-09-28 カズヤくん）。
  試聴で拾っていた粗のうち、機械で拾えるものを本編より前にここで止める。読みそのものは aq_kana・check_aq_yomi が見る
  （棒読みなのでアクセントは効かない）。ここが見るのは「決めた読み・声・行間どおりの音が、壊れずにできているか」。

■ 違反（1件でも E なら exit 1）
  E1 組み立て：audio/<cid>.wav が、いまの読み（aq_kana）・声（aq_build.VOICES）・行間・利得から組んだ音と1バイトでも違う／
     キャッシュの記録（送った文字列・行ID）が合わない／narration.json の声・行間・字幕の行・秒が組み直した値と違う
  E2 話者：語り（まりさ）と聞き役（れいむ）の声の高さ（基本周波数の中央値）の差が SPEAKER_MIN_GAP Hz 未満（同じ声で焼いた疑い）／
     行の声の高さが、台本の話者でない側の中心から SPEAKER_MARGIN Hz 以内（取り違えの疑い）／声の高さが取れない行
  E3 音割れ：audio/<cid>.wav（24kHz・利得のあと）に上限に届く標本がある
  E4 途切れ：1モーラあたりの秒が、その声の中央値の TRUNC 倍未満（途中で切れた疑い）・行の中の無音が PAUSE_MAX 秒超
  W1 語りと聞き役の音量（声の出ている所の RMS の中央値）の差が LOUD_DIFF dB 超
  W2 1モーラあたりの秒が、その声の中央値の SLOW 倍超（間が挟まった疑い）
  （参考）アプリの出力（8kHz）の中で上限に届く標本＝アプリの既定の音に元からある（音量100で231行・456標本・連続は最長2標本）
  ゆっくりでない回（el_script.VOICE_ENGINE が aquestalk でない）は見ない（exit 0 と明示）

■ しきい値の根拠（14本目 442行の実測・09-28）
  声の高さ：語り 210〜258Hz（中央値235）・聞き役 267〜333Hz（中央値308）＝差73Hz。行の外れは0
  行の中の無音：最長0.34秒（「。」の間）／1モーラあたりの秒：その声の中央値の0.83〜1.43倍／音量の差 0.9dB
"""
import hashlib
import json
import sys
import wave
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

FRAME = 0.010            # 無音を見る枠（秒）
SIL_DB = -46.0           # これより静かな枠は無音（dBFS）
EDGE = 0.01              # 頭と尻を切る振幅（上限に対する割合）
SPEAKER_MIN_GAP = 40.0   # 2つの声の高さの中心の差（Hz）の下限
SPEAKER_MARGIN = 15.0    # 行の声の高さが「相手の声の中心」からこれ以内なら取り違えの疑い（Hz）
TRUNC = 0.5              # 1モーラあたりの秒がその声の中央値のこの倍より小さい＝途切れの疑い
SLOW = 1.6               # 同じくこの倍より大きい＝間が挟まった疑い（W）
PAUSE_MAX = 0.6          # 行の中の無音の上限（秒）
LOUD_DIFF = 3.0          # 語りと聞き役の音量の差（dB）の上限（W）
FULL = 32767


def db(v):
    return 20 * np.log10(max(float(v), 1e-9) / 32768.0)


def f0_median(x, fs, fmin=70.0, fmax=500.0, frame=0.04, hop=0.01):
    """声の出ている枠の基本周波数（自己相関）の中央値。取れなければ 0。"""
    L, H = int(frame * fs), int(hop * fs)
    lo, hi = int(fs / fmax), int(fs / fmin)
    vals = []
    for s in range(0, len(x) - L, H):
        seg = x[s:s + L].astype(np.float64)
        seg = seg - seg.mean()
        e = float((seg ** 2).sum())
        if e <= 0 or db(np.sqrt(e / L)) < SIL_DB + 10:
            continue
        ac = np.correlate(seg, seg, "full")[L - 1:]
        k = lo + int(np.argmax(ac[lo:min(hi, L - 1)]))
        if ac[k] > 0.3 * ac[0]:
            vals.append(fs / k)
    return float(np.median(vals)) if vals else 0.0


def metrics(x, fs):
    """1行の音 → 数。x は int16 の配列（アプリの出力そのまま）。"""
    x = np.asarray(x)
    a = np.abs(x.astype(np.int32))
    idx = np.flatnonzero(a > 32768 * EDGE)
    clip = int((a >= FULL).sum())
    if len(idx) == 0:
        return dict(clip=clip, speech=0.0, max_pause=0.0, rms_db=-99.0, f0=0.0)
    y = x[idx[0]:idx[-1] + 1].astype(np.float64)
    n = int(FRAME * fs)
    frames = [y[i:i + n] for i in range(0, len(y) - n + 1, n)]
    rms = np.array([np.sqrt((f ** 2).mean()) for f in frames]) if frames else np.array([0.0])
    silent = np.array([db(r) < SIL_DB for r in rms])
    run = best = 0
    for s in silent:
        run = run + 1 if s else 0
        best = max(best, run)
    voiced = rms[~silent]
    return dict(clip=clip, speech=len(y) / fs, max_pause=best * FRAME,
                rms_db=db(np.sqrt((voiced ** 2).mean())) if len(voiced) else -99.0,
                f0=f0_median(y, fs))


def n_moras(aq):
    """音声記号列のモーラ数（' / 、。？ は数えない）。"""
    import aq_kana
    return len(aq_kana.moras(aq_kana.plain(aq).translate(str.maketrans("", "", "、。？"))))


def read_wav(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype="<i2"), w.getframerate(), w.getnchannels()


def cache_meta_ok(meta, sent, lid, same):
    """合成キャッシュの記録（json）が、いまの行の音として正しいか。same＝いまの台本で「送る文字列と声」が同じ行IDの集合。
    🔴 19本目（2026-10-06）：同じ文・同じ声の行は合成キャッシュを1つ共有する（冒頭の問い c107-2・c107-3 を終わりの
    cc26-1・cc28-1 で一字一句くり返す）＝記録の行IDは先に焼いた行になり、行IDの食い違いで E1 2件が鳴った（音は正しい）。
    送った文字列が同じで、記録の行が same の中なら通す。文字列が違う・記録の行が same の外（前の版の残り）は今までどおり E1"""
    return meta.get("sent") == sent and (meta.get("lid") == lid or meta.get("lid") in same)


def judge(rows):
    """rows＝[(行ID, 話者, モーラ数, 数)] → (E, W, 参考)。話者は None＝語り・"q"＝聞き役。"""
    E, W = [], []
    groups = {w: [r for r in rows if r[1] == w] for w in (None, "q")}
    center = {w: float(np.median([r[3]["f0"] for r in g if r[3]["f0"] > 0])) if any(r[3]["f0"] > 0 for r in g) else 0.0
              for w, g in groups.items()}
    both = all(groups[w] for w in (None, "q"))
    if both and center["q"] - center[None] < SPEAKER_MIN_GAP:
        E.append(f"E2 聞き役（中心 {center['q']:.0f}Hz）と語り（{center[None]:.0f}Hz）の声の高さの差が {SPEAKER_MIN_GAP:.0f}Hz 未満"
                 f"＝同じ声で焼いた疑い（aq_build.VOICES・CANDIDATES を見る）")
    spm_med = {}
    for w, g in groups.items():
        v = [r[3]["speech"] / max(r[2], 1) for r in g if r[3]["speech"] > 0]
        spm_med[w] = float(np.median(v)) if v else 0.0
    for lid, w, nm, m in rows:
        name = "聞き役" if w else "語り"
        if m["f0"] <= 0:
            E.append(f"E2 {lid}（{name}）声の高さが取れない（無音か壊れた音）")
        elif both:
            other = center[None] if w else center["q"]
            if (w and m["f0"] <= other + SPEAKER_MARGIN) or (not w and m["f0"] >= other - SPEAKER_MARGIN):
                E.append(f"E2 {lid}（{name}）声の高さ {m['f0']:.0f}Hz が相手の声（中心 {other:.0f}Hz）に近い＝話者の取り違えの疑い")
        spm = m["speech"] / max(nm, 1)
        med = spm_med[w]
        if med > 0 and spm < TRUNC * med:
            E.append(f"E4 {lid} 1モーラ {spm:.3f}秒＝{name}の中央値の {spm / med:.2f}倍（途中で切れた疑い）")
        elif med > 0 and spm > SLOW * med:
            W.append(f"W2 {lid} 1モーラ {spm:.3f}秒＝{name}の中央値の {spm / med:.2f}倍（間が挟まった疑い）")
        if m["max_pause"] > PAUSE_MAX:
            E.append(f"E4 {lid} 行の中に {m['max_pause']:.2f}秒の無音（上限 {PAUSE_MAX}秒）")
    loud = {w: float(np.median([r[3]["rms_db"] for r in g])) for w, g in groups.items() if g}
    if both and abs(loud[None] - loud["q"]) > LOUD_DIFF:
        W.append(f"W1 音量の差 {abs(loud[None] - loud['q']):.1f}dB（語り {loud[None]:.1f}・聞き役 {loud['q']:.1f} dBFS）")
    info = dict(center=center, loud=loud, spm_med=spm_med,
                src_clip=sum(r[3]["clip"] for r in rows), src_clip_lines=sum(r[3]["clip"] > 0 for r in rows))
    return E, W, info


def collect():
    """全行の (行ID, 話者, モーラ数, 数) と、組み立て（E1）・音割れ（E3）の E。"""
    import aq_build as B
    import aq_tts as T
    import el_script as ES
    import narration
    E = []
    js = json.loads((ROOT / "audio" / "narration.json").read_text(encoding="utf-8"))
    if js.get("engine") != "aquestalk":
        return [], [f"E1 narration.json の engine が {js.get('engine')}（ゆっくりの音でない・先に aq_build）"]
    defs = B.voice_defs()
    presets = {w: n for w, (n, _) in defs.items()}
    for w, key in ((None, "n"), ("q", "q")):
        got = js.get("presets", {}).get(key, {}).get("name")
        if got != presets[w]:
            E.append(f"E1 narration.json の声（{key}）が {got}＝aq_build.VOICES の {presets[w]} と違う（焼き直す）")
    if abs(float(js.get("gap", -1)) - B.gap_of()) > 1e-9:
        E.append(f"E1 narration.json の行間 {js.get('gap')}＝aq_build の {B.gap_of()} と違う（焼き直す）")
    if (js.get("gap_cuts") or {}) != B.gap_cuts():           # カットごとの行間（18本目〜・無い回は両方とも空）
        E.append(f"E1 narration.json のカットごとの行間 {js.get('gap_cuts')}＝aq_build の {B.gap_cuts()} と違う（焼き直す）")
    yomi = B.yomi_table()
    rows_by = {w: T.preset_row(n) for w, n in presets.items()}
    cache = T.CACHE / ES.SLUG
    out = []
    import speaker
    same = {}                          # (送る文字列, 声) → その組の行ID（同じ文・同じ声の行はキャッシュを共有する）
    for cid, lines in narration.SCRIPT:
        for i, t in enumerate(lines, 1):
            lid = f"{cid}-{i}"
            same.setdefault((T.sent_text(yomi[lid]), speaker.split(t)[0]), set()).add(lid)

    def synth(lid, who, body):
        sent = T.sent_text(yomi[lid])
        p = cache / f"{T.cache_key(sent, rows_by[who])}.wav"
        if not p.exists():
            raise KeyError(lid)
        meta = json.loads(p.with_suffix(".json").read_text(encoding="utf-8"))
        if not cache_meta_ok(meta, sent, lid, same.get((sent, who), ())):
            E.append(f"E1 {lid} キャッシュの記録が合わない（送った文字列・行ID）")
        x, fs, ch = read_wav(p)
        out.append((lid, who, n_moras(yomi[lid]), metrics(x, fs)))
        return T.to_sr(x, fs)

    for cid, lines in narration.SCRIPT:
        try:
            pcm, total, rows = B.build_cut(cid, lines, synth, B.gap_of(cid=cid))
        except KeyError as e:
            E.append(f"E1 {e.args[0]} の合成キャッシュが無い（いまの読み・声で焼いていない＝aq_build）")
            continue
        wp = ROOT / "audio" / f"{cid}.wav"
        if not wp.exists():
            E.append(f"E1 {cid}.wav が無い")
            continue
        got, fs, ch = read_wav(wp)
        if fs != B.SR or ch != 1 or got.tobytes() != pcm:
            E.append(f"E1 {cid}.wav がいまの読み・声・行間・利得から組んだ音と違う（{fs}Hz {ch}ch・"
                     f"md5 {hashlib.md5(got.tobytes()).hexdigest()[:8]} ≠ {hashlib.md5(pcm).hexdigest()[:8]}）")
        c = int((np.abs(got.astype(np.int32)) >= FULL).sum())
        if c:
            E.append(f"E3 {cid}.wav に上限に届く標本 {c}個（音割れ・aq_tts.GAIN を見る）")
        if js.get("subtitles", {}).get(cid) != rows:
            E.append(f"E1 {cid} narration.json の字幕の行（t・d・text・who）が組み直した値と違う")
        if abs(js.get("durations", {}).get(cid, -1) - round(total, 3)) > 1e-6:
            E.append(f"E1 {cid} narration.json の秒 {js.get('durations', {}).get(cid)} ≠ {round(total, 3)}")
    if set(js.get("durations", {})) != {c for c, _ in narration.SCRIPT}:
        E.append("E1 narration.json のカットが台本と1対1でない")
    return out, E


def run(stats=False):
    import el_script as ES
    if getattr(ES, "VOICE_ENGINE", "elevenlabs") != "aquestalk":
        print(f"この回（{ES.SLUG}）はゆっくりでない＝見ない")
        return 0
    rows, E = collect()
    E2, W, info = judge(rows) if rows else ([], [], {})
    E += E2
    if info:
        c = info["center"]
        print(f"行 {len(rows)}（語り {sum(r[1] is None for r in rows)}・聞き役 {sum(r[1] == 'q' for r in rows)}）"
              f"／声の高さの中心 語り {c[None]:.0f}Hz・聞き役 {c['q']:.0f}Hz（差 {c['q'] - c[None]:.0f}）"
              f"／音量 語り {info['loud'][None]:.1f}・聞き役 {info['loud']['q']:.1f} dBFS")
        print(f"（参考）アプリの出力の中で上限に届く標本 {info['src_clip']}個・{info['src_clip_lines']}行＝アプリの既定の音に元からある")
    if stats and rows:
        for w, name in ((None, "語り"), ("q", "聞き役")):
            g = [r for r in rows if r[1] == w]
            for k in ("f0", "rms_db", "max_pause"):
                v = np.percentile([r[3][k] for r in g], [0, 5, 50, 95, 100])
                print(f"  {name} {k:9s} " + " ".join(f"{t:.3f}" for t in v))
            v = np.percentile([r[3]["speech"] / max(r[2], 1) for r in g], [0, 5, 50, 95, 100])
            print(f"  {name} 秒/モーラ " + " ".join(f"{t:.4f}" for t in v))
    for x in E[:40]:
        print("🔴 " + x)
    for x in W[:40]:
        print("⚠️ " + x)
    print(f"E {len(E)}件 / W {len(W)}件")
    return 1 if E else 0


def selftest():
    """合成音の代わりに正弦波で検算する（アプリ・audio/・キャッシュは使わない）。"""
    fails = []
    ok = lambda c, name: None if c else fails.append(name)
    fs = 8000

    def tone(hz, sec, amp=12000):
        t = np.arange(int(sec * fs))
        return (amp * np.sin(2 * np.pi * hz * t / fs)).astype("<i2")
    for hz in (230, 310):
        f = metrics(tone(hz, 1.0), fs)["f0"]
        ok(abs(f - hz) / hz < 0.05, f"声の高さ {hz}Hz を拾う（{f:.1f}）")
    m = metrics(np.concatenate([tone(230, 0.5), np.zeros(int(0.8 * fs), dtype="<i2"), tone(230, 0.5)]), fs)
    ok(abs(m["max_pause"] - 0.8) < 0.03, f"行の中の無音 0.8秒を測る（{m['max_pause']:.2f}）")
    ok(metrics(np.full(100, 32767, dtype="<i2"), fs)["clip"] == 100, "上限に届く標本を数える")

    def row(lid, who, hz, sec=2.0, moras=20, pause=0.0, amp=12000):
        return (lid, who, moras, dict(clip=0, speech=sec, max_pause=pause, rms_db=db(amp / np.sqrt(2)), f0=hz))
    base = [row(f"n{i}", None, 235) for i in range(20)] + [row(f"q{i}", "q", 308) for i in range(5)]
    E, W, _ = judge(base)
    ok(not E and not W, f"陰性対照（正しい並び）が鳴った: {E + W}")
    cases = [("語りの行が聞き役の声", base + [row("x", None, 300)], "E2 x"),
             ("聞き役の行が語りの声", base + [row("x", "q", 240)], "E2 x"),
             ("声が取れない行", base + [row("x", None, 0.0)], "E2 x"),
             ("途中で切れた行", base + [row("x", None, 235, sec=0.5)], "E4 x"),
             ("行の中の長い無音", base + [row("x", None, 235, pause=0.9)], "E4 x")]
    for name, rows, key in cases:
        E, W, _ = judge(rows)
        ok(any(e.startswith(key) for e in E), f"陽性対照が鳴らない: {name}（{E}）")
    E, W, _ = judge([row(f"n{i}", None, 235) for i in range(20)] + [row(f"q{i}", "q", 245) for i in range(5)])
    ok(any("差が" in e for e in E), "陽性対照：2つの声が近い（同じ声で焼いた疑い）が鳴らない")
    E, W, _ = judge(base + [row("x", None, 235, sec=3.5)])
    ok(any(w.startswith("W2 x") for w in W), "陽性対照：間が挟まった行（W2）が鳴らない")
    E, W, _ = judge([row(f"n{i}", None, 235) for i in range(20)] + [row(f"q{i}", "q", 308, amp=4000) for i in range(5)])
    ok(any(w.startswith("W1") for w in W), "陽性対照：音量の差（W1）が鳴らない")
    # 合成キャッシュの記録（19本目：同じ文・同じ声の行はキャッシュを共有する）
    m = {"sent": "#>ふたつめ。", "lid": "c107-2"}
    ok(cache_meta_ok(m, "#>ふたつめ。", "c107-2", {"c107-2", "cc26-1"}), "陰性対照：記録の行そのもの")
    ok(cache_meta_ok(m, "#>ふたつめ。", "cc26-1", {"c107-2", "cc26-1"}), "陰性対照：同じ文・同じ声の別の行（共有）")
    ok(not cache_meta_ok(m, "#>ふたつめ。", "cc26-1", {"cc26-1"}), "陽性対照：記録の行が同じ文の組の外（前の版の残り）")
    ok(not cache_meta_ok(m, "#>みっつめ。", "c107-2", {"c107-2"}), "陽性対照：送った文字列が違う")
    if fails:
        print("🔴 selftest:\n  " + "\n  ".join(fails))
        return 1
    print("selftest: 全部合格（声の高さ・無音・音割れの物差し／陰性1・陽性8／キャッシュの記録 陰性2・陽性2）")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run(stats="--stats" in sys.argv))
