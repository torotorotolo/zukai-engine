# -*- coding: utf-8 -*-
r"""el_tts.py — ElevenLabs で1行ずつ合成する。tools/el_build.py から呼ばれる。

  python tools/el_tts.py --selftest      … 物差しの検算（API 不使用・クレジット0）
  python tools/el_tts.py --voice         … VOICE の id が VOICE_NAME に完全一致するか（API 読み取りのみ）
  python tools/el_tts.py "文"            … 1行だけ合成して out/el_smoke.wav（声・鍵・quota の確認用）

2026-09-05 カズヤくん決定（事故検証ch 4本目サーフサイドから。心理ch ep005 の道具を移植）:
    声   = Hiro - Ultra Deep Japanese Voice（マイコレクション）。⚠️ 心理chの Koichi／「HIRO - Cool」とは別の声
    モデル = eleven_v3（画面の「PVC の一貫性には Multilingual v2 を」は読んだうえで v3 に決定）
    ⚠️ この声の verified_languages に eleven_v3 は入っていない（2026-09-05 API で実測）＝長尺で崩れないかは自分で確かめる。
    voice_settings は el_script.SETTINGS で一元管理（キャッシュの鍵に入る。途中で変えると全行が別物になる）。

なぜ1行ずつか:
    行ごとの実測秒数が、場面の尺と字幕のタイミングを決めているため（gen_audio.main）。
    まとめて合成すると行の境目が取れない。

⭐ 行ごとにキャッシュする。これが効く理由:
    - 直したい行だけ投げ直せる。**他の行は1クレジットも使わず、音も1サンプルも変わらない**
    - ⚠️ AivisSpeech は非決定的で、全編を合成し直すと検品ずみの行まで変わる事故があった
      （reference-aivisspeech-nondeterministic）。キャッシュはその事故を構造的に防ぐ。
    - 鍵は (voice, model, settings, 本文) のハッシュ。**本文を1文字でも直せば別の鍵**になる。

⚠️ 出力形式について（2026-08-26 実測）:
    pcm_44100 は「Pro 以上」と 403 で断られる。Creator では **pcm_24000 が最上**。
    これは既存パイプラインの SR=24000 と一致するので、変換なしでそのまま使える。

⚠️ 前後の無音は切る:
    ElevenLabs は行の頭と尻に無音を付けてくる。これを残すと gen_audio の GAP(0.55秒) に
    上乗せされて間延びする。ここで切って、間の設計は GAP 側に一本化する。
    ⚠️ 2026-09-05 実測：eleven_v3 は**行の6割で先頭に無音を付けない**（声が 0ms から始まる。261行中161行）。
       それ自体は頭欠けの証拠ではない（0ms 始まりの7テイクが全部正しく聞き取れた）。ただしテイクによって
       文頭の子音が弱くなり「隙間→暇」「門→王」と聞こえることがある。切る前と切った後を同じテイクで
       文字起こしして一致したので _trim は無関係。直し方＝tools/el_retake.py（文字起こしで確かめながら振り直す）。
       文頭に「、」「…」を足しても先頭の無音は作れなかった（6テイク中1回だけ 90ms）。
"""
import hashlib
import json
import os
import struct
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent            # zukai-engine/
sys.path.insert(0, str(Path(__file__).resolve().parent))  # tools/
# 🔴 鍵は config/（public リポ＝gitignore ずみ。`git check-ignore config/elevenlabs_key.txt` で実測ずみ）
KEY_FILE = ROOT / "config" / "elevenlabs_key.txt"

import el_artifacts as ART  # noqa: E402  純粋な関数だけ（el_tts / el_script を import しない）

# 🔴 2026-09-02 異音の門番（カズヤくん指摘「文末や文間にしゃっくりのような細切れの音」）:
#    eleven_v3 は台本に無い 100〜200ms の音を混ぜる（reference-elevenlabs-tts）。振り直せば消える。
#    検出道具 el_find_artifacts.py はあったが「疑いを挙げるだけ」で、ep008 は回した記録が無かった
#    ＝回し忘れても何も止まらない（feedback-rules-need-gates）。そこで合成の中に組み込む:
#      1行合成 → ART.inspect_struct → 余計な音があれば同じ本文で最大 MAX_TAKES 回振り直す
#      → 無いテイクが出たら採用 → 全部同じ形なら本物の語として採用（ep007 s110 の型）
#      → 形が毎回違うなら一番少ないテイクを採用して「要耳」に記録（el_earcheck で聴く）
#    費用: 振り直し1回＝その行の文字数×0.55クレジット。1本で数十行でも上限131,000の1%未満。
MAX_TAKES = 3

# 🔴 voice_id は 2026-09-05 に /v1/voices で「この名前に完全一致」する1件から取った（43声中1件）。
#    ⚠️ 同じコレクションに「HIRO - Cool Japanese Male Voice」（Bj4Malc5SZLoXfPtxRxH）が別に在る。掴み違えないよう
#    check_voice() が id→名前を API で照合する（el_build の頭と --voice で回す）。
VOICE_NAME = "Hiro - Ultra Deep Japanese Voice"
VOICE = "qaCSabKToUUT4sTqBZtz"
MODEL = "eleven_v3"
# ⚠️ 声に保存された既定の settings（/v1/voices/<id>/settings・2026-09-05 実測）＝
#    stability 0.85 / similarity_boost 1.0 / style 0.0 / speed 1.14 / speaker_boost True。
#    voice_settings を渡さないと**この speed 1.14 で読む**。渡すかどうかは el_script.SETTINGS（1行合成で決める）。
FORMAT = "pcm_24000"
SR = 24000

# 前後の無音を切る閾値。16bit フルスケール 32767 に対して約 -40dBFS。
# ⚠️ 上げすぎると子音の立ち上がりを削る。下げすぎると環境ノイズを声と見なす。
TRIM_LEVEL = 320
TRIM_WIN = SR // 100        # 10ms ごとに見る
TRIM_MARGIN = int(SR * 0.03)  # 切ったあと 30ms は残す

# ⚠️ 2026-08-26: 300秒にしていたら、1本の接続が固まったまま4分以上止まった（実際に発生）。
#    1行あたりの合成は実測1〜3秒なので、90秒あれば十分。固まったら早く諦めて投げ直すほうが速い。
#    キャッシュがあるので、投げ直しても済んだ行にクレジットはかかりません。
REQ_TIMEOUT = 90

_key = None
_stats = {"api": 0, "cache": 0, "chars": 0, "retakes": 0, "unsure": 0, "real": 0}


def _retake_log(slug, scene_id, text, takes, decision, chosen):
    """振り直しの記録。audio/el_qa/<slug>_el_retakes.tsv に追記（行 / 判定 / 採用テイク / テイクごとの所見 / 本文）。"""
    d = ROOT / "audio" / "el_qa"
    d.mkdir(exist_ok=True)
    p = d / f"{slug}_el_retakes.tsv"
    if not p.exists():
        p.write_text("scene\tdecision\tchosen\ttakes\tflags\ttext\n", encoding="utf-8")
    flags = " || ".join(
        f"take{i+1}: " + ("; ".join(x["msg"] for x in ART.blips(t[1])) or "clean")
        for i, t in enumerate(takes))
    with p.open("a", encoding="utf-8") as f:
        f.write(f"{scene_id}\t{decision}\t{chosen+1}\t{len(takes)}\t{flags}\t{text}\n")


def key():
    global _key
    if _key is None:
        if not KEY_FILE.exists():
            raise RuntimeError(f"APIキーがありません: {KEY_FILE}")
        _key = KEY_FILE.read_text(encoding="utf-8-sig").strip()
        if not _key:
            raise RuntimeError(f"APIキーが空です: {KEY_FILE}")
    return _key


def stats():
    return dict(_stats)


def credits_used():
    """いま何クレジット使ったか。⚠️ 反映が数十秒遅れることがある。
    ⚠️ これは口座側の上限だけ。APIキー個別の credit limit は返ってこない（401 quota_exceeded で初めて分かる）。"""
    r = urllib.request.Request("https://api.elevenlabs.io/v1/user/subscription",
                               headers={"xi-api-key": key()})
    with urllib.request.urlopen(r, timeout=60) as f:
        u = json.load(f)
    return u["character_count"], u["character_limit"]


def check_voice():
    """門番：VOICE の id が API 上で VOICE_NAME に**完全一致**する声か（別の Hiro を掴まない）。読み取りのみ。"""
    r = urllib.request.Request(f"https://api.elevenlabs.io/v1/voices/{VOICE}",
                               headers={"xi-api-key": key()})
    with urllib.request.urlopen(r, timeout=60) as f:
        v = json.load(f)
    if v.get("name") != VOICE_NAME:
        raise RuntimeError(f"voice_id {VOICE} の名前が「{v.get('name')}」＝期待「{VOICE_NAME}」と違う。止める")
    return v


def _cache_dir(slug):
    d = ROOT / "audio" / "el_cache" / slug
    d.mkdir(parents=True, exist_ok=True)
    return d


def _cache_key(text, settings):
    h = hashlib.sha1()
    h.update(f"{VOICE}|{MODEL}|{json.dumps(settings, sort_keys=True, ensure_ascii=False)}|{text}"
             .encode("utf-8"))
    return h.hexdigest()[:16]


def _post(text, settings):
    body = {"text": text, "model_id": MODEL}
    if settings:
        body["voice_settings"] = settings
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format={FORMAT}"
    last = None
    for attempt in range(5):
        req = urllib.request.Request(url, data=data, method="POST",
                                     headers={"xi-api-key": key(),
                                              "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=REQ_TIMEOUT) as f:
                return f.read()
        except urllib.error.HTTPError as e:
            detail = ""
            try:
                detail = e.read().decode("utf-8", "replace")[:300]
            except Exception:
                pass
            last = f"HTTP {e.code}: {detail}"
            # 429=混雑 / 5xx=サーバ側。ここだけ待って再試行する。
            # ⚠️ 4xx（文が長すぎる・権限が無い等）は再試行しても直らないので即座に諦める。
            if e.code != 429 and e.code < 500:
                break
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        wait = 2 ** attempt
        print(f"    再試行 {attempt+1}/5（{wait}秒待つ）… {last}", flush=True)
        time.sleep(wait)
    raise RuntimeError(f"合成に失敗しました: {last}")


def _trim(pcm: bytes) -> bytes:
    """前後の無音を切る。⚠️ 全部が無音なら切らずに返す（fail closed 側）。"""
    n = len(pcm) // 2
    if n == 0:
        return pcm
    vals = struct.unpack(f"<{n}h", pcm[: n * 2])
    loud = []
    for i in range(0, n, TRIM_WIN):
        w = vals[i: i + TRIM_WIN]
        if w and max(abs(min(w)), abs(max(w))) >= TRIM_LEVEL:
            loud.append(i)
    if not loud:
        return pcm                      # 声が見つからない＝切らない
    a = max(0, loud[0] - TRIM_MARGIN)
    b = min(n, loud[-1] + TRIM_WIN + TRIM_MARGIN)
    return pcm[a * 2: b * 2]


def synth(text: str, scene_id: str = "", slug: str = "ep000",
          settings=None, refresh: bool = False, send_text: str = None) -> bytes:
    """1行を合成して 16bit/24kHz モノラルの生PCMを返す。キャッシュが効く。

    send_text … API に実際に送る文字列を差し替える（キャッシュの鍵は text のまま）。
      2026-09-05: 文頭の子音が切れるテイクを避けるため、el_retake が「　、」を頭に足して振り直すのに使う。
      足した分は無音なので _trim が切る＝音の中身は text と同じ。meta に "sent" として記録する。"""
    text = text.strip()
    if not text:
        raise ValueError(f"空の本文です（{scene_id}）")
    req_text = send_text if send_text else text
    ck = _cache_key(text, settings)
    cache = _cache_dir(slug) / f"{ck}.pcm"
    meta = _cache_dir(slug) / f"{ck}.json"

    if cache.exists() and not refresh:
        _stats["cache"] += 1
        return cache.read_bytes()

    # 🔴 異音の門番: 合成 → 検出 → 余計な音があれば振り直す（最大 MAX_TAKES 回）
    takes = []   # [(pcm, items, raw_sec)]
    for _ in range(MAX_TAKES):
        raw = _post(req_text, settings)
        _stats["api"] += 1
        _stats["chars"] += len(req_text)
        pcm = _trim(raw)
        sec = len(pcm) / 2 / SR
        # fail closed: 文があるのに音がほぼ無いのは異常。0で埋めて先へ進めない。
        if sec < 0.15:
            raise RuntimeError(f"音が短すぎます {sec:.2f}秒（{scene_id}）: {text[:30]}")
        if sec > 60:
            raise RuntimeError(f"音が長すぎます {sec:.1f}秒（{scene_id}）: {text[:30]}")
        items = ART.inspect_struct(pcm)
        takes.append((pcm, items, round(len(raw) / 2 / SR, 3)))
        if not ART.blips(items):
            break
        print(f"    ⚠️ 異音 {scene_id} take{len(takes)}: "
              + "; ".join(x["msg"] for x in ART.blips(items)), flush=True)

    if not ART.blips(takes[-1][1]):
        chosen, decision = len(takes) - 1, "clean"
    else:
        sigs = {ART.signature(t[1]) for t in takes}
        if len(takes) >= MAX_TAKES and len(sigs) == 1:
            # 何度振っても同じ形＝偶発の混入ではなく本物の語（ep007 s110「入っています。」の型）
            chosen, decision = 0, "real"
            _stats["real"] += 1
        else:
            chosen = min(range(len(takes)), key=lambda i: len(ART.blips(takes[i][1])))
            decision = "unsure"
            _stats["unsure"] += 1
    _stats["retakes"] += len(takes) - 1
    if len(takes) > 1 or decision != "clean":
        _retake_log(slug, scene_id, text, takes, decision, chosen)
    pcm, items, raw_sec = takes[chosen]
    sec = len(pcm) / 2 / SR

    cache.write_bytes(pcm)
    meta.write_text(json.dumps({
        "scene_id": scene_id, "text": text, "sent": req_text, "voice": VOICE, "model": MODEL,
        "settings": settings, "sec": round(sec, 3), "chars": len(text),
        "raw_sec": raw_sec, "takes": len(takes), "decision": decision,
        "flags": [x["msg"] for x in ART.blips(items)],
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    return pcm


def _synth_pcm(sec: float, amp: int = 8000, freq: float = 180.0) -> bytes:
    """自己検算用の疑似の声（のこぎり波）。"""
    n = int(SR * sec)
    return struct.pack(f"<{n}h", *(int(amp * (2 * ((i * freq / SR) % 1.0) - 1)) for i in range(n)))


def _silence(sec: float) -> bytes:
    return b"\x00\x00" * int(SR * sec)


def selftest() -> int:
    """物差しの検算（API は叩かない・クレジット0）。落ちたら exit 1。"""
    import shutil
    global _post
    fails = []
    ok = lambda cond, name: (None if cond else fails.append(name))
    ok(ART.SR == SR, "SR 一致")
    speech = _synth_pcm(0.8)
    blip = _synth_pcm(0.14, amp=12000)
    # 1) 末尾のしゃっくり（s020 の形: 100ms 無音 → 140ms・本文より大きい塊）
    bad = speech + _silence(0.10) + blip
    ok(any(x["kind"] == "tail" for x in ART.blips(ART.inspect_struct(bad))), "末尾の異音を検出")
    # 2) 本物の語尾（450ms の塊）は拾わない
    good = speech + _silence(0.10) + _synth_pcm(0.45, amp=8000)
    ok(not ART.blips(ART.inspect_struct(good)), "本物の語尾を拾わない")
    # 3) 途中に浮いた音
    mid = speech + _silence(0.12) + blip + _silence(0.12) + speech
    ok(any(x["kind"] == "mid" for x in ART.blips(ART.inspect_struct(mid))), "途中の異音を検出")
    # 4) 読点の間（300ms の無音だけ）は拾わない
    pause = speech + _silence(0.30) + speech
    ok(not ART.blips(ART.inspect_struct(pause)), "読点の間を拾わない")
    # 5) 小さい減衰の尻尾（本文の 0.3 倍）は拾わない
    tail = speech + _silence(0.10) + _synth_pcm(0.12, amp=2400)
    ok(not ART.blips(ART.inspect_struct(tail)), "小さい尻尾を拾わない")
    # 6) フェード: 長さ不変・端が 0・中身は不変
    f = ART.edge_fade(speech, 5)
    v0 = struct.unpack("<h", f[:2])[0]
    vmid = struct.unpack("<h", f[len(f) // 2: len(f) // 2 + 2])[0]
    omid = struct.unpack("<h", speech[len(speech) // 2: len(speech) // 2 + 2])[0]
    ok(len(f) == len(speech) and v0 == 0 and vmid == omid, "5ms フェード")
    # 7) 振り直しの筋道（API を偽物に差し替える）: 1テイク目に異音 → 2テイク目 clean を採用
    real_post = _post
    slug = "_selftest"
    shutil.rmtree(_cache_dir(slug), ignore_errors=True)
    seq = [bad, speech]
    _post = lambda text, settings: seq.pop(0)
    before = dict(_stats)
    try:
        out = synth("検算の文です。", "t1", slug=slug)
        ok(out == _trim(speech), "振り直して clean を採用")
        ok(_stats["api"] - before["api"] == 2 and _stats["retakes"] - before["retakes"] == 1,
           "振り直し回数の勘定")
        # 8) 3テイクとも同じ形 → 本物として1テイク目を採用
        seq[:] = [bad, bad, bad]
        out = synth("同じ形の文です。", "t2", slug=slug)
        ok(out == _trim(bad) and _stats["real"] - before["real"] == 1, "同じ形は本物と判定")
        # 9) 形が毎回違う → unsure（一番少ないテイク）
        seq[:] = [bad, mid, bad + _silence(0.10) + blip]
        synth("違う形の文です。", "t3", slug=slug)
        ok(_stats["unsure"] - before["unsure"] == 1, "形が違えば要耳")
        log = ROOT / "audio" / "el_qa" / f"{slug}_el_retakes.tsv"
        ok(log.exists() and len(log.read_text(encoding="utf-8").splitlines()) == 4, "振り直しの記録")
    finally:
        _post = real_post
        shutil.rmtree(_cache_dir(slug), ignore_errors=True)
        try:
            (ROOT / "audio" / "el_qa" / f"{slug}_el_retakes.tsv").unlink()
        except FileNotFoundError:
            pass
        for k in before:
            _stats[k] = before[k]
    total = 11
    if fails:
        print(f"selftest: {total-len(fails)}/{total} — 落ちた項目: {fails}")
        return 1
    print(f"selftest: {total}/{total} 合格（API は叩いていない・クレジット0）")
    return 0


def write_wav(pcm: bytes, path: Path, sr: int = SR):
    n = len(pcm)
    hdr = struct.pack("<4sI4s4sIHHIIHH4sI", b"RIFF", 36 + n, b"WAVE", b"fmt ",
                      16, 1, 1, sr, sr * 2, 2, 16, b"data", n)
    Path(path).write_bytes(hdr + pcm)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    v = check_voice()
    print(f"声の照合 ✓ {VOICE} = 「{v['name']}」（{v.get('category')}）／モデル {MODEL}／形式 {FORMAT}")
    if "--voice" in sys.argv:
        sys.exit(0)
    # 1行合成。--settings '{"speed":1.0}' で voice_settings を試せる（キャッシュは smoke 側に隔離）
    import el_script  # noqa: E402  ← 本番と同じ SETTINGS を既定にする
    st = json.loads(sys.argv[sys.argv.index("--settings") + 1]) if "--settings" in sys.argv else el_script.SETTINGS
    args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] != "--settings"]
    t = args[0] if args else "これは接続の確認です。"
    c0, lim = credits_used()
    p = synth(t, "smoke", "smoke", settings=st)
    out = ROOT / "out" / "el_smoke.wav"
    out.parent.mkdir(exist_ok=True)
    write_wav(p, out)
    c1, _ = credits_used()
    print(f"settings={st}")
    print(f"OK {len(p)/2/SR:.2f}秒（{len(t)}字＝{len(t)/(len(p)/2/SR):.2f}字/秒） -> {out}")
    print(f"クレジット {c0:,} → {c1:,}（消費 {c1-c0:,}／口座上限 {lim:,}）⚠️ 反映が遅れることがある")
    print("使用:", stats())
