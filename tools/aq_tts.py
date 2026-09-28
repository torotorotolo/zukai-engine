# -*- coding: utf-8 -*-
r"""aq_tts.py — ゆっくり（AquesTalkPlayer）で音声記号列1行を合成する（事故検証ch 14本目 ⑤a-2 から）。

  python tools/aq_tts.py --probe      … アプリ・プリセット・設定を確かめ、1行だけ合成して WAV の形式を出す
  python tools/aq_tts.py --selftest   … 偽のプレーヤーで検算（本物のアプリは起動しない・本物のプリセットに書かない）

el_tts（ElevenLabs）と同じ位置の道具＝「1行 → pcm」だけを受け持つ。カットの組み立ては aq_build.py。

🔴 許諾（記憶 project-jiko-yukkuri-voice-trial・公式 FAQ）
  ・使用ライセンスは**アプリで使う**ためのもの＝ここは exe をコマンドで呼ぶだけ（DLL を直に呼ぶのは開発ライセンスの領分）
  ・**使う台数分**のライセンス＝合成はカズヤくんの PC 1台だけ（Modal／Actions で合成しない。合成した WAV を混ぜるのは可）
  ・アプリ・DLL・辞書は**再配布禁止**＝リポに入れない。exe はリポの外の絶対パス（環境変数 AQ_PLAYER で差し替え可）
  ・exe の隣の ini にはライセンスキーがある＝**音に効く項目だけを名指しで拾う**（key1・key10 は持たない・出さない）
  ・生成した音声は自由に使える（FAQ「音声データの２次利用の制限はありますか？」＝いいえ）＝opus を公開リポに置いてよい

振る舞い（2026-09-28 の実測・14本目 ⑤a-2 の最初の試し）
  ・出力＝mono 16bit・AquesTalk1 は 8,000Hz（ini の bResample=0＝声の元の周波数）。頭 約0.014秒・尻 約0.032秒の無音を含む
  ・同じ入力なら同じ音（md5 一致）＝キャッシュしてよい。/T と /F（Shift-JIS）は同じ音
  ・棒読み＝true のプリセットは**アクセント記号「'」を無視**（記号の有無で md5 一致）。「？」の上がり調子は棒読みでも効く
  ・句の最後の「っ」（c808「え'っ、」）は通る
  ・エラーは終了コード 2000〜2022（WAV は作られない）。2012＝記号列が正しくない・2021＝プリセットが無い
"""
import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import wave
from math import gcd
from pathlib import Path

import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

EXE = Path(os.environ.get("AQ_PLAYER", r"C:\Users\konar\AquesTalkPlayer\AquesTalkPlayer.exe"))
EXE_MD5 = "4a7a908259ee07d85cae7ea67b63e4de"   # aquestalkplayer_20250606.zip の exe。違えば止める（音が変わりうる）
SR = 24000                                      # 返す pcm＝el_tts.SR と同じ（audio_mix.read_wav が 44.1kHz へ直す）
# 🔴 変換の前に掛ける利得（09-28・14本目⑤a-2）。アプリの出力は波の山が上限に届く（既定の音量100で442行中231行）＝
#    そのまま 8k→24k に直すとフィルタの行き過ぎで上限を越え、196カット中172で計1,068標本が削れた。0.8倍（-1.94dB）で0。
#    本編の聞こえの大きさは audio_mix が -15.0 LUFS に合わせる＝小さくならない。⚠️ 値を変えたら aq_build の指紋が変わる
GAIN = 0.8
CACHE = ROOT / "audio" / "aq_cache"             # <SLUG>/<鍵>.wav＝アプリの出力そのまま（.gitignore 済み）
FIELDS = ["プリセット名", "棒読み", "エンジン", "声種", "話速", "音量", "高さ", "アクセント", "声質", "音程", "メモ"]
NUMS = ("話速", "音量", "高さ", "アクセント", "声質", "音程")
# 音に効く ini の項目（名指し）。🔴 ライセンスキー（key1・key10）はここに入れない＝読まない・鍵にも記録にも入らない
SOUND_KEYS = ("pauseTop", "pauseLast", "bResample", "resample_method", "resample_fs", "bAddPause")
ERRORS = {
    2000: "予期せぬエラー", 2001: "システム辞書が不正", 2002: "ユーザ辞書が不正", 2003: "AqKanji2Koe 初期化エラー",
    2004: "音声記号列が指定されていない", 2005: "DLL のロード失敗", 2006: "不正な DLL", 2007: "PHONT の読み込み失敗",
    2008: "未定義の読み記号", 2009: "タグの指定が正しくない", 2010: "発話文が長すぎる", 2011: "PHONT が不正",
    2012: "音声記号列が正しくない", 2013: "メモリ不足", 2014: "テキストが空", 2015: "AqKanji2Koe 変換エラー",
    2016: "WAV を書けない", 2017: "プリセットファイルが壊れている", 2018: "プリセットファイルが開けない",
    2019: "プリセット名の指定が正しくない", 2020: "プリセットファイルの書き込み失敗", 2021: "プリセット名が見つからない",
    2022: "テキストファイルが開けない",
}
RUN = subprocess.run                            # selftest が偽物に差し替える（本物のアプリを起動しない）
_stats = {"app": 0, "cache": 0}


def preset_path():
    return EXE.parent / "AquesTalkPlayer.preset"


def ini_path():
    return EXE.parent / "AquesTalkPlayer.ini"


def md5_file(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()


def check_app():
    """exe があり、決めた版か。違えば止める（fail closed）。"""
    if not EXE.exists():
        raise SystemExit(f"🔴 AquesTalkPlayer が無い: {EXE}（リポの外に置く・環境変数 AQ_PLAYER で差し替え可）")
    m = md5_file(EXE)
    if m != EXE_MD5:
        raise SystemExit(f"🔴 exe の md5 が {m}（決めた版 {EXE_MD5}）＝アプリが替わった。"
                         f"音が変わりうるので、1行の試し（--probe）からやり直して EXE_MD5 を直す")
    return m


def sound_settings():
    """ini のうち音に効く項目だけ（名指しで拾う）。ini が無ければ空。"""
    p = ini_path()
    out = {}
    if not p.exists():
        return out
    for line in p.read_bytes().decode("cp932", "replace").splitlines():
        k, sep, v = line.partition("=")
        if sep and k.strip() in SOUND_KEYS:
            out[k.strip()] = v.strip()
    return out


def _norm(d):
    """プリセットの欄を比べられる形に（数は int・棒読みは小文字・メモは音に効かないので外す）。"""
    out = {"棒読み": str(d["棒読み"]).strip().lower(), "エンジン": str(d["エンジン"]).strip(),
           "声種": str(d["声種"]).strip()}
    for k in NUMS:
        out[k] = int(d[k])
    return out


def read_presets():
    """{名前: {欄: 値}}。Shift-JIS の CSV（1行目は見出し）。"""
    text = preset_path().read_bytes().decode("cp932")
    rows = [r for r in csv.reader(io.StringIO(text)) if r]
    if not rows or rows[0] != FIELDS:
        raise SystemExit(f"🔴 プリセットの見出しが想定と違う: {rows[0] if rows else '（空）'}")
    return {r[0]: dict(zip(FIELDS[1:], r[1:])) for r in rows[1:]}


def preset_row(name):
    """音に効く欄だけ（キャッシュの鍵と narration.json の記録に入れる形）。無ければ止まる。"""
    ps = read_presets()
    if name not in ps:
        raise SystemExit(f"🔴 プリセット「{name}」が {preset_path().name} に無い（aq_build が ensure_presets で書く）")
    return _norm(ps[name])


def _fmt_row(name, d):
    q = lambda s: '"' + str(s).replace('"', '""') + '"'
    return ",".join([q(name), q(str(d["棒読み"]).lower()), q(d["エンジン"]), q(d["声種"]),
                     *[str(int(d[k])) for k in NUMS], q(d.get("メモ", ""))])


def ensure_presets(defs, memo=""):
    """defs={名前: {欄: 値}} をプリセットの CSV に置く（無ければ足す・音に効く欄が違えば直す）。
    同じなら1バイトも書かない（False）。書くときは先に写し（.bak-日付＝その日の最初の書き込みの前の状態・1日1つ）を取り、
    ほかの行は1バイトも変えない。初期の中身は .preset.org にもある（アプリに付いてくる）。"""
    cur = read_presets()
    want = {n: _norm(d) for n, d in defs.items()}
    todo = {n for n, w in want.items() if n not in cur or _norm(cur[n]) != w}
    if not todo:
        return False
    p = preset_path()
    bak = p.with_name(p.name + time.strftime(".bak-%Y%m%d"))
    if not bak.exists():
        shutil.copy2(p, bak)
    raw = p.read_bytes().decode("cp932")
    nl = "\r\n" if "\r\n" in raw else "\n"
    lines = raw.split(nl)
    tail = []
    while lines and lines[-1] == "":
        tail.append(lines.pop())
    out, seen = [], set()
    for i, line in enumerate(lines):
        name = next(csv.reader([line]))[0] if (i and line) else None
        if name in want:
            seen.add(name)
            line = _fmt_row(name, {**defs[name], "メモ": memo}) if name in todo else line
        out.append(line)
    out += [_fmt_row(n, {**defs[n], "メモ": memo}) for n in defs if n not in seen]
    p.write_bytes(nl.join(out + tail).encode("cp932"))
    return True


def sent_text(aq, kanji=False):
    """アプリへ実際に送る文字列。既定は音声記号列（先頭に #>）。kanji=True は漢字かな文のまま（アプリ自身の変換＝聞き比べ用）。"""
    return aq if kanji else "#>" + aq


def cache_key(sent, row, settings=None):
    """鍵＝exe の版・プリセットの音に効く欄・ini の音に効く項目・**送る文字列**（プリセットの名前とメモは入れない）。"""
    s = sound_settings() if settings is None else settings
    blob = json.dumps([EXE_MD5, row, s, sent], ensure_ascii=False, sort_keys=True)
    return hashlib.md5(blob.encode("utf-8")).hexdigest()


def read_wav(p):
    """(int16 の配列, 標本化周波数)。mono 16bit 以外は止まる。"""
    with wave.open(str(p)) as w:
        ch, sw, fs, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        raw = w.readframes(n)
    if ch != 1 or sw != 2:
        raise SystemExit(f"🔴 {p.name}: {ch}ch {sw * 8}bit（mono 16bit のはず）")
    return np.frombuffer(raw, dtype="<i2"), fs


def to_sr(x, fs, sr=None):
    """fs → sr（既定 SR）。先に GAIN を掛け、整数比の多相フィルタ（scipy resample_poly）で直す＝決定的。8k→24k はちょうど3倍。"""
    sr = SR if sr is None else sr
    y = x.astype(np.float64) * GAIN
    if fs != sr:
        from scipy.signal import resample_poly
        g = gcd(sr, fs)
        y = resample_poly(y, sr // g, fs // g)
    return np.clip(np.round(y), -32768, 32767).astype("<i2").tobytes()


def _slug():
    import el_script
    return el_script.SLUG


def synth(aq, preset, lid="", slug=None, kanji=False):
    """音声記号列（先頭の #> は付けない）→ pcm（s16le mono SR）。キャッシュに無ければアプリを呼ぶ。
    kanji=True は aq に漢字かな文を渡す（アプリ自身の変換＝聞き比べ用。本番では使わない）。"""
    row = preset_row(preset)
    sent = sent_text(aq, kanji)
    key = cache_key(sent, row)
    d = CACHE / (slug or _slug())
    d.mkdir(parents=True, exist_ok=True)
    wp = d / f"{key}.wav"
    if wp.exists():
        _stats["cache"] += 1
    else:
        call_app(sent, preset, wp, lid)
        (d / f"{key}.json").write_text(json.dumps(
            {"lid": lid, "preset": preset, "row": row, "settings": sound_settings(), "exe_md5": EXE_MD5,
             "sent": sent}, ensure_ascii=False), encoding="utf-8")
        _stats["app"] += 1
    x, fs = read_wav(wp)
    return to_sr(x, fs)


def call_app(sent, preset, out, lid=""):
    """アプリを1回呼んで out に WAV を置く。/F（Shift-JIS・CRLF）で渡す＝/T と同じ音（実測）。
    sent＝送る文字列そのもの（音声記号列なら先頭に #>）。"""
    tmp = Path(out).parent / "_tmp"
    tmp.mkdir(exist_ok=True)
    txt, part = tmp / f"{Path(out).stem}.txt", tmp / f"{Path(out).stem}.wav"
    aq = sent
    try:
        body = (sent + "\r\n").encode("cp932")
    except UnicodeEncodeError as e:
        raise SystemExit(f"🔴 {lid}: Shift-JIS に無い字 {sent[e.start:e.end]!r}（「{sent}」）")
    txt.write_bytes(body)
    if part.exists():
        part.unlink()
    rc = RUN([str(EXE), "/F", str(txt), "/P", preset, "/W", str(part)]).returncode
    if rc != 0 or not part.exists():
        raise SystemExit(f"🔴 AquesTalkPlayer が止まった（{lid}）: 終了コード {rc}＝{ERRORS.get(rc, '不明')}"
                         f"／プリセット「{preset}」／記号列「{aq}」")
    read_wav(part)                                  # 形式の門番（mono 16bit）
    part.replace(out)
    txt.unlink()


def stats():
    return dict(_stats)


# ── 確かめる ─────────────────────────────────────────────────────────
def probe(preset="まりさ", aq="か'んこくの/なんせーの/う'みで、りょかくせん/せうぉる'ごーが/かたむ'いた。"):
    m = check_app()
    ps = read_presets()
    print(f"exe {EXE}（md5 {m}・決めた版と一致）")
    print(f"プリセット {len(ps)}個: {'・'.join(ps)}")
    print(f"ini の音に効く項目: {sound_settings()}")
    with tempfile.TemporaryDirectory() as td:
        wp = Path(td) / "probe.wav"
        call_app(sent_text(aq), preset, wp, "probe")
        x, fs = read_wav(wp)
        print(f"「{preset}」→ mono 16bit {fs}Hz {len(x) / fs:.3f}秒 md5 {hashlib.md5(x.tobytes()).hexdigest()[:10]}")
    return 0


def selftest():
    """偽のプレーヤーで検算する。本物の exe・プリセット・ini・キャッシュには触らない。"""
    global EXE, CACHE, RUN, EXE_MD5
    keep = (EXE, CACHE, RUN, EXE_MD5)
    fails = []
    ok = lambda c, name: None if c else fails.append(name)
    calls = []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        try:
            EXE, CACHE = td / "AquesTalkPlayer.exe", td / "cache"
            EXE.write_bytes(b"fake player")
            EXE_MD5 = md5_file(EXE)
            head = ",".join(FIELDS)
            rows = ['"デフォルト","false","AquesTalk10","F1E",100,100,100,100,100,100,"女声"',
                    '"まりさ","true","AquesTalk1","f2",100,100,100,100,100,100,"ゆっくり魔理沙"']
            preset_path().write_bytes(("\n".join([head] + rows) + "\n").encode("cp932"))
            ini_path().write_bytes("[View]\nkey1=SECRETKEY01\nkey10=SECRETKEY10\npauseTop=0\nbResample=0\n".encode("cp932"))

            def fake_run(args):
                calls.append(args)
                a = dict(zip(args[1::2], args[2::2]))
                text = Path(a["/F"]).read_bytes().decode("cp932")
                ps = read_presets()
                if a["/P"] not in ps:
                    return subprocess.CompletedProcess(args, 2021)
                if "ぢ" in text:
                    return subprocess.CompletedProcess(args, 2012)
                n = 800 * len(text) * 100 // int(ps[a["/P"]]["話速"])          # 話速で長さが変わる偽の声
                with wave.open(a["/W"], "w") as w:
                    w.setnchannels(1), w.setsampwidth(2), w.setframerate(8000)
                    w.writeframes((np.sin(np.arange(n) * 0.3) * 8000).astype("<i2").tobytes())
                return subprocess.CompletedProcess(args, 0)
            RUN = fake_run

            ok(check_app() == EXE_MD5, "決めた版の exe は通る")
            s = sound_settings()
            ok(s == {"pauseTop": "0", "bResample": "0"}, f"ini は音に効く項目だけ拾う（{s}）")
            ok("SECRET" not in json.dumps(s), "ライセンスキーを拾わない")

            before = preset_path().read_bytes()
            v = {"jiko-n": dict(棒読み="true", エンジン="AquesTalk1", 声種="f2", 話速=180, 音量=100, 高さ=100,
                                アクセント=100, 声質=100, 音程=100)}
            ok(ensure_presets(v, "試し") is True, "無いプリセットを足す")
            after = preset_path().read_bytes()
            ok(after.startswith(before.rstrip(b"\n")), "ほかの行は1バイトも変えない")
            ok(len(list(td.glob("AquesTalkPlayer.preset.bak-*"))) == 1, "書く前に写しを取る")
            ok(ensure_presets(v, "試し") is False and preset_path().read_bytes() == after, "同じなら書かない")
            ok(preset_row("jiko-n")["話速"] == 180, "足したプリセットを読める")

            pcm = synth("あ'いう。", "jiko-n", "t-1", slug="t")
            n_app = len(calls)
            ok(len(pcm) == 3 * (800 * len("#>あ'いう。\r\n") * 100 // 180) * 2, "8k→24k はちょうど3倍の長さ")
            ok(synth("あ'いう。", "jiko-n", "t-1", slug="t") == pcm and len(calls) == n_app, "2回目はキャッシュ（アプリを呼ばない）")
            meta = "".join(p.read_text(encoding="utf-8") for p in (CACHE / "t").glob("*.json"))
            ok("SECRET" not in meta, "キャッシュの記録にキーが入らない")

            ok(ensure_presets({"jiko-n": {**v["jiko-n"], "話速": 150}}) is True, "話速が違えば行を直す")
            ok(preset_path().read_bytes().count(b"jiko-n") == 1, "直しても行は増えない（名前は1つ）")
            pcm2 = synth("あ'いう。", "jiko-n", "t-1", slug="t")
            ok(len(calls) == n_app + 1 and len(pcm2) > len(pcm), "プリセットの話速を変えると鍵が変わり、作り直す")
            baks = list(td.glob("AquesTalkPlayer.preset.bak-*"))
            ok(len(baks) == 1 and baks[0].read_bytes() == before, "写しは1日1つ＝その日の最初の書き込みの前の中身")

            for bad, code in (("ぢ'ぢ。", "2012"), ):
                try:
                    synth(bad, "jiko-n", "t-2", slug="t")
                    fails.append("エラーで止まらない")
                except SystemExit as e:
                    ok(code in str(e), f"終了コード {code} を出して止まる")
            try:
                synth("あ。", "無いプリセット", "t-3", slug="t")
                fails.append("無いプリセットで止まらない")
            except SystemExit as e:
                ok("無いプリセット" in str(e), "無いプリセットは合成の前に止まる")
            EXE.write_bytes(b"other version")
            try:
                check_app()
                fails.append("別の版の exe が通った")
            except SystemExit:
                pass
            x = np.array([0, 1000, -1000, 0], dtype="<i2")
            ok(to_sr(x, 24000) == np.round(x * GAIN).astype("<i2").tobytes(), "同じ周波数は GAIN を掛けるだけ（長さ不変）")
            # 山が上限で削れた波（アプリの出力と同じ形＝500Hz の正弦波を1.3倍して削った）を 24kHz に直しても削れない。
            # 利得1.0 なら行き過ぎで削れる（陽性対照）。⚠️ 8kHz の 2kHz 矩形波は行き過ぎ約1.41倍＝声（実測 約1.11倍）より極端で見本に向かない
            t = np.arange(1600)
            sq = (np.clip(1.3 * np.sin(2 * np.pi * 500 * t / 8000), -1, 1) * 32767).astype("<i2")
            clipped = lambda b: int((np.abs(np.frombuffer(b, dtype="<i2").astype(np.int32)) >= 32767).sum())
            ok(clipped(to_sr(sq, 8000)) == 0, f"GAIN {GAIN} で上限に届く標本が0")
            keep_gain = GAIN
            try:
                globals()["GAIN"] = 1.0
                ok(clipped(to_sr(sq, 8000)) > 0, "陽性対照：利得1.0 なら行き過ぎで削れる")
            finally:
                globals()["GAIN"] = keep_gain
        finally:
            EXE, CACHE, RUN, EXE_MD5 = keep
    if fails:
        print(f"selftest: 落ちた {len(fails)}: {fails}")
        return 1
    print("selftest: 全部合格（本物のアプリ・プリセット・ini・キャッシュには触っていない）")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--probe" in sys.argv:
        sys.exit(probe())
    print(__doc__)
