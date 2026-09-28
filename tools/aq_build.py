# -*- coding: utf-8 -*-
r"""aq_build.py — ゆっくり（AquesTalk）で全カットを合成し、el_build と**同じ形**の audio/<cid>.wav・audio/narration.json を出す。

  python tools/aq_build.py                   … 全カット（キャッシュが効く＝変わった行だけアプリを呼ぶ）
  python tools/aq_build.py --cuts c101,c102  … 一部だけ（ほかは指紋が合えば前回の記録を持ち越す）
  python tools/aq_build.py --dry             … アプリを呼ばない（キャッシュだけで組む・無い行は止まる）
  python tools/aq_build.py --rate            … audio/narration.json から尺・冒頭・「句読点なしの字数÷尺」（字/分）と話速の当たり
  python tools/aq_build.py --listen c1 --cand A --out X.mp3 [--kanji]
                                             … 章の試聴（カットの頭尻・決め所の余白・章の扉を入れた並び）。audio/ は触らない
  python tools/aq_build.py --selftest        … 組み立ての検算（アプリを呼ばない）

出力（scene_jiko / audio_mix / audio_pack / check_subwrap / check_listener / check_script が読む形は el_build と同じ）:
  audio/<cid>.wav      … 24kHz mono 16bit。行と行の間は GAP 秒の無音
  audio/narration.json … durations（発話＋行間）／subtitles（行ごとの t・d・text＋聞き役だけ "who":"q"）／signatures
                          ＋ engine "aquestalk"・presets（音に効く欄）・exe の md5・ini の音に効く項目・gap
  字幕の text は印 `Q: ` を外した文（speaker.split）。読みは aq_kana の音声記号列（override・利用者辞書こみ・E 0 が前提）

⚠️ 台本に無いカットの wav は消す（el_build と同じ）＝本線で回すと前の回の音が消える。回ごとの作業ツリーで（ルール 5a-23）
⚠️ 話速は合成の後で変えない（atempo を通さない）＝アプリの話速（プリセット）で決める。ルール 5a-28＝380字/分・下限27分
"""
import hashlib
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import aq_tts as T                  # noqa: E402
import el_artifacts as ART          # noqa: E402
import el_script as ES              # noqa: E402
import narration                    # noqa: E402  SCRIPT の正本
import speaker                      # noqa: E402  聞き役の印 `Q: `

GAP = 0.40          # 行と行のあいだ（秒）の既定。回ごとの値は VOICES の "gap"（narration.json に記録＝check_script が読む）
FADE_MS = 5         # 行の頭と尻のクリック止め（長さ不変）
SR = T.SR
AUDIO = ROOT / "audio"
PUNCT = re.compile(r"[、。？！「」（）・]")   # 「句読点なし」の字数（ルール 5a-28＝競合分析 §5 と同じ数え方）
TARGET_CPM = 380    # 字/分（競合「ゆっくり事故検証」5本の中央値）
FLOOR_SEC = 27 * 60  # 尺の下限。割るなら話速を1段ずつ下げる（373字/分まで）
FLOOR_CPM = 373      # 話速を下げてよい下限（字/分）
MEMO = "事故検証ch aq_build が書く（手で直さない）"

# 声（回ごと）。キー None＝語り・"q"＝聞き役（speaker.split の who）。プリセットはアプリの CSV に ensure_presets が書く
_BASE = dict(エンジン="AquesTalk1", 音量=100, 高さ=100, アクセント=100, 声質=100, 音程=100)
VOICES = {
    # 🔴 14本目（2026-09-28 ⑤a-2）：話速は段々でしか動かない（実測：154〜157＝26分52〜55秒・150〜153＝27分39〜42秒）。
    #    27分を割らず 373字/分を保つ話速は無い → 話速 154・行間 0.43（＋30ms）で 27分02秒台・373字/分に合わせた
    "ep14": {"speed": 154, "gap": 0.43, "cand": "A"},     # cand＝声の候補（カズヤくんが選ぶ）
}


def gap_of(slug=None):
    return float(VOICES.get(slug or ES.SLUG, {}).get("gap", GAP))
# 声の候補（⑤a-2 でカズヤくんに選んでもらう）。(声種, 棒読み)。話速は VOICES の speed を使う
CANDIDATES = {
    "A": {None: ("f2", "true"), "q": ("f1", "true")},     # まりさ（説明）・れいむ（聞き役）＝棒読み（ゆっくりの定番の音）
    "B": {None: ("f2", "false"), "q": ("f1", "false")},   # 同じ2つの声でアクセントあり（こちらの記号列のアクセント）
}


def voice_defs(slug=None, cand=None, speed=None):
    """{who: (プリセット名, 欄)}。名前は回・候補・話者で固定（アプリの一覧を散らかさない）。話速はその行を書き換える
    ＝キャッシュの鍵と指紋は名前でなく欄の中身から取るので、書き換えても前の音と混ざらない。"""
    slug = slug or ES.SLUG
    v = VOICES.get(slug)
    if v is None:
        raise SystemExit(f"🔴 aq_build.VOICES に {slug} が無い（声と話速を回ごとに決める）")
    cand = cand or v["cand"]
    speed = int(speed or v["speed"])
    out = {}
    for who, (voice, flat) in CANDIDATES[cand].items():
        name = f"jiko-{slug}-{cand}-{'q' if who else 'n'}"
        out[who] = (name, dict(_BASE, 声種=voice, 棒読み=flat, 話速=speed))
    return out


def setup(defs):
    """アプリの版を確かめ、プリセットを置く。{who: プリセット名}。"""
    T.check_app()
    T.ensure_presets({n: d for n, d in defs.values()}, MEMO)
    return {who: n for who, (n, _) in defs.items()}


def yomi_table():
    """{行ID: 音声記号列}。aq_kana の全行の読み（override・利用者辞書こみ）。E があれば止まる。"""
    import aq_kana
    rows, _, stale = aq_kana.sheet(write=False)
    bad = [(r[0], e) for r in rows for e in r[6]]
    if bad or stale:
        raise SystemExit(f"🔴 読みに E {len(bad)}件・使われない override {stale}＝先に aq_kana --sheet を E 0 に: {bad[:5]}")
    return {r[0]: r[3] for r in rows}


def _sig(cid, lines, yomi, presets):
    """カットの指紋＝**アプリへ送る文字列**・声（音に効く欄）・ini・exe の版・GAP・SR・フェード。
    🔴 合成のあとに音を変える定数は全部ここに入れる（入れ忘れると値を変えても wav が作り直されない）。"""
    sent = [T.sent_text(yomi[f"{cid}-{i}"]) for i in range(1, len(lines) + 1)]
    who = [speaker.split(x)[0] for x in lines]
    rows = {str(w): T.preset_row(presets[w]) for w in set(who)}
    blob = json.dumps([sent, who, rows, T.sound_settings(), T.EXE_MD5, gap_of(), SR, FADE_MS],
                      ensure_ascii=False, sort_keys=True)
    return hashlib.sha1(blob.encode("utf-8")).hexdigest()[:12]


def write_wav(path, pcm, sr=SR):
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm)


def build_cut(cid, lines, synth, gap_sec=None):
    """1カットぶん。行ごとに合成→フェード→行間で連結。(pcm, 秒, 字幕rows)。synth(行ID, who, 文) → pcm。"""
    chunks, rows, t = [], [], 0.0
    gap = b"\x00\x00" * int(round((gap_of() if gap_sec is None else gap_sec) * SR))
    for i, line in enumerate(lines, 1):
        who, body = speaker.split(line)
        pcm = ART.edge_fade(synth(f"{cid}-{i}", who, body), FADE_MS)
        sec = len(pcm) / 2 / SR
        row = {"t": round(t, 3), "d": round(sec, 3), "text": body}
        if who:
            row["who"] = who                          # 語りの行には付けない（check_subwrap は None と比べる）
        rows.append(row)
        chunks += [pcm, gap]
        t += sec + len(gap) / 2 / SR
    return b"".join(chunks[:-1]), t - len(gap) / 2 / SR, rows


def quotes_and_md():
    """決め所（★の行を持つカット）の集合。台本の md から（SCRIPT は ★ を外してある）。カットの並びも突き合わせる。"""
    import check_script as CSC
    md = Path(ES.EXPECT[ES.SLUG]["md"])
    cuts = CSC.parse(md.read_text(encoding="utf-8"))
    ids = [c for c, _, _ in cuts]
    if ids != [c for c, _ in narration.SCRIPT if c in set(ids)]:
        raise SystemExit("🔴 台本の md と narration.SCRIPT でカットの並びが違う")
    return {c for c, _, ls in cuts if any(CSC.STAR_RE.match(l) for l in ls)}


def timeline(durs, script, quotes):
    """カットごとの (始まり, 終わり) と全体の尺。check_script の③・「冒頭:」と同じ並び：
    章の扉（第2章から）→ LEAD → 声（行間こみ）→ TAIL（＋決め所の余白）。"""
    import check_script as CSC
    t, prev, out = 0.0, None, {}
    for cid, _ in script:
        key = cid[:2] if CSC.CHAPTER_CUT_RE.match(cid) else None
        if key is not None:
            if prev is not None and key != prev:
                t += CSC.CARD_SEC
            prev = key
        t0 = t
        t += CSC.LEAD + durs[cid] + CSC.TAIL + (CSC.TAIL_EXTRA_QUOTE if cid in quotes else 0.0)
        out[cid] = (t0, t)
    return out, t


def nopunct_chars(script):
    return sum(len(PUNCT.sub("", speaker.bare(x))) for _, ls in script for x in ls)


def fmt(s):
    return f"{int(s) // 60}分{s - 60 * (int(s) // 60):04.1f}秒"


def rate_report(js=None, quiet=False):
    """narration.json の実測から 尺・冒頭・字/分 と、話速の当たり（380字/分・下限27分）を出す。"""
    js = js or json.loads((AUDIO / "narration.json").read_text(encoding="utf-8"))
    if js.get("engine") != "aquestalk":
        raise SystemExit(f"🔴 narration.json の engine が {js.get('engine')}（aq_build の音でない）")
    durs = js["durations"]
    miss = [c for c, _ in narration.SCRIPT if c not in durs]
    if miss:
        raise SystemExit(f"🔴 narration.json に無いカット {len(miss)}: {miss[:5]}（全カットを作ってから）")
    quotes = quotes_and_md()
    tl, total = timeline(durs, narration.SCRIPT, quotes)
    chars = nopunct_chars(narration.SCRIPT)
    speech = sum(r["d"] for rows in js["subtitles"].values() for r in rows)
    over = total - speech                                 # 構造の尺（行間・頭尻・決め所・扉）＝話速で動かない
    cpm = chars / (total / 60)
    s0 = js["presets"]["n"]["話速"]
    # ⚠️ 話速から尺を式で当てない：AquesTalk1 の話速は段々（14本目の実測＝154→153 で声が 2.7% 跳ぶ・1段では 0.1%）。
    #    話速を替えたら全行を焼き直して、ここの実測で合否を見る（1回 約1分・費用なし）
    ok_floor, ok_cpm = total >= FLOOR_SEC, cpm >= FLOOR_CPM
    if not quiet:
        print(f"話速 {s0}・行間 {js.get('gap')}秒／句読点なし {chars:,}字／声 {fmt(speech)}＋構造 {fmt(over)} ＝ 尺 {fmt(total)}")
        print(f"  字/分（句読点なし÷尺）= {cpm:.1f}（目標 {TARGET_CPM}・下げてよいのは {FLOOR_CPM} まで）"
              f"／声だけの字/分 = {chars / (speech / 60):.1f}")
        print(f"  判定：尺 27分00秒以上 {'✓' if ok_floor else '🔴'}・{FLOOR_CPM}字/分以上 {'✓' if ok_cpm else '🔴'}")
        op = [c for c, _ in narration.SCRIPT][:8]
        print("  冒頭: " + " ".join(f"{c}={tl[c][1]:.1f}s" for c in op))
    return dict(total=total, speech=speech, over=over, cpm=cpm, chars=chars, s0=s0,
                ok=ok_floor and ok_cpm, timeline=tl)


def build(cuts=None, dry=False, cand=None, speed=None):
    AUDIO.mkdir(exist_ok=True)
    jp = AUDIO / "narration.json"
    prev = json.loads(jp.read_text(encoding="utf-8")) if jp.exists() else {}
    known = [c for c, _ in narration.SCRIPT]
    if cuts is not None:
        bad = [c for c in cuts if c not in known]
        if bad:
            raise SystemExit(f"🔴 台本に無いカット: {bad}")
    targets = set(known if cuts is None else cuts)
    defs = voice_defs(cand=cand, speed=speed)
    presets = setup(defs) if not dry else {w: n for w, (n, _) in defs.items()}
    yomi = yomi_table()

    if dry:
        def synth(lid, who, body):
            row = T.preset_row(presets[who])
            p = T.CACHE / ES.SLUG / f"{T.cache_key(T.sent_text(yomi[lid]), row)}.wav"
            if not p.exists():
                raise SystemExit(f"🔴 --dry: キャッシュが無い行 {lid}: {body[:30]}")
            return T.to_sr(*T.read_wav(p))
    else:
        def synth(lid, who, body):
            return T.synth(yomi[lid], presets[who], lid)

    durs, subs, sigs = {}, {}, {}
    kept = built = 0
    skipped = []
    for cid, lines in narration.SCRIPT:
        sig = _sig(cid, lines, yomi, presets)
        if cid not in targets:
            # 部分更新：前回の記録を持ち越す。🔴 指紋が今の台本・声・設定と一致するものだけ（カットIDは題材をまたいでぶつかる）
            if (prev.get("engine") == "aquestalk" and prev.get("signatures", {}).get(cid) == sig
                    and (AUDIO / f"{cid}.wav").exists()):
                durs[cid], subs[cid], sigs[cid] = prev["durations"][cid], prev["subtitles"][cid], sig
                kept += 1
            else:
                skipped.append(cid)
            continue
        pcm, total, rows = build_cut(cid, lines, synth)
        write_wav(AUDIO / f"{cid}.wav", pcm)
        durs[cid], subs[cid], sigs[cid] = round(total, 3), rows, sig
        built += 1

    rows_by = {str(w): {"name": n, **T.preset_row(n)} for w, n in presets.items()}
    js = {
        "engine": "aquestalk", "player_md5": T.EXE_MD5, "settings": T.sound_settings(),
        "presets": {("q" if w == "q" else "n"): r for w, r in rows_by.items()},
        "speaker": "aquestalk:" + "+".join(sorted(presets.values())),
        # speed＝アプリの話速（プリセットの値＝実効値。合成の後で縮めない）
        "speed": defs[None][1]["話速"], "tempo": 1.0, "credit": "",
        "gap": gap_of(), "sr": SR, "durations": durs, "subtitles": subs, "signatures": sigs,
    }
    jp.write_text(json.dumps(js, ensure_ascii=False, indent=2), encoding="utf-8")

    gone = 0
    for f in AUDIO.glob("*.wav"):                        # 記録に無いカットの wav は消す＝wav と json を1対1に
        if f.stem not in durs:
            f.unlink()
            gone += 1
    st = T.stats()
    print(f"合成 {built} カット／持ち越し {kept}／未作成 {len(skipped)}／記録 {len(durs)}／台本 {len(known)}"
          f"（アプリ {st['app']}行・キャッシュ {st['cache']}行{f'・記録に無い wav を {gone} 本削除' if gone else ''}）")
    if skipped:
        print(f"⚠️ まだ作っていないカット {len(skipped)}: {','.join(skipped[:8])}{'…' if len(skipped) > 8 else ''}")
    longest = max(((r["d"], r["text"]) for rs in subs.values() for r in rs), default=(0, ""))
    print(f"最長の1行 = {longest[0]:.2f}秒「{longest[1]}」")
    if len(durs) == len(known):
        rate_report(js)
        return 0
    return 1


def listen(prefix, out, cand, kanji=False, speed=None):
    """試聴 mp3（audio/ を触らない）。prefix＝章（"c1"）か "all"（全編＝⑤a' の音声だけの試聴）。
    並びは本編と同じ（章の扉 2秒は2つ目の章から・LEAD・声・TAIL・決め所の余白）。
    横に <out>.tsv＝行ごとの開始時刻（試聴の「何分何秒」から行へ戻る表）。"""
    import check_script as CSC
    import numpy as np
    defs = voice_defs(cand=cand, speed=speed)
    presets = setup(defs)
    yomi = None if kanji else yomi_table()
    quotes = quotes_and_md()
    cuts = [(c, ls) for c, ls in narration.SCRIPT if prefix == "all" or c.startswith(prefix)]
    if not cuts:
        raise SystemExit(f"🔴 {prefix} で始まるカットが無い")

    def synth(lid, who, body):
        return T.synth(body if kanji else yomi[lid], presets[who], lid, kanji=kanji)
    sil = lambda s: np.zeros(int(round(s * SR)), dtype="<i2").tobytes()
    parts, secs, prev, marks = [], 0.0, None, []
    for cid, lines in cuts:
        key = cid[:2] if CSC.CHAPTER_CUT_RE.match(cid) else None
        if key is not None:
            if prev is not None and key != prev:
                parts.append(sil(CSC.CARD_SEC))
                secs += CSC.CARD_SEC
            prev = key
        pcm, total, rows = build_cut(cid, lines, synth)
        for i, r in enumerate(rows, 1):
            marks.append((secs + CSC.LEAD + r["t"], f"{cid}-{i}", r.get("who", ""), r["text"]))
        tail = CSC.TAIL + (CSC.TAIL_EXTRA_QUOTE if cid in quotes else 0.0)
        parts += [sil(CSC.LEAD), pcm, sil(tail)]
        secs += CSC.LEAD + total + tail
    with open(Path(out).with_suffix(".tsv"), "w", encoding="utf-8", newline="") as f:
        f.write("時刻\t秒\t行ID\t話者\t文\n")
        for t, lid, who, text in marks:
            f.write(f"{int(t // 60)}:{t % 60:04.1f}\t{t:.2f}\t{lid}\t{who}\t{text}\n")
    wav = Path(out).with_suffix(".wav")
    write_wav(wav, b"".join(parts))
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-b:a", "96k", str(out)])
    if r.returncode != 0:
        raise SystemExit(f"🔴 ffmpeg が失敗（{r.returncode}）")
    wav.unlink()
    chars = nopunct_chars(cuts)
    print(f"{out}: {len(cuts)}カット {fmt(secs)}／句読点なし {chars}字 → {chars / (secs / 60):.1f}字/分"
          f"（声 {cand}・{'アプリ自身の変換' if kanji else 'こちらの記号列'}・{presets}）")
    return 0


def selftest():
    """アプリを呼ばずに組み立てと尺の式を検算する（audio/ も触らない）。"""
    import check_script as CSC
    fails = []
    ok = lambda c, name: None if c else fails.append(name)
    n_of = {}

    def synth(lid, who, body):
        n = int(SR * (0.5 + 0.1 * len(body)))
        n_of[lid] = n
        return (b"\x10\x27" * n)                          # 10000 の直流＝フェードが効いたか見える

    pcm, total, rows = build_cut("t1", ["あいうえお。", "Q: かきくけこ？", "さしす。"], synth, GAP)
    g = int(round(GAP * SR))
    ok(len(rows) == 3 and rows[0]["t"] == 0.0, "字幕 rows の形")
    ok("who" not in rows[0] and rows[1].get("who") == "q" and "who" not in rows[2], "who は聞き役の行だけ")
    ok(rows[1]["text"] == "かきくけこ？", "字幕は印 `Q: ` を外した文")
    ok(abs(rows[1]["t"] - (rows[0]["d"] + GAP)) < 1e-3, "2行目の t ＝ 1行目の d ＋ GAP")
    ok(len(pcm) == (sum(n_of.values()) + 2 * g) * 2, "pcm の長さ ＝ 声＋GAP×(行数−1)")
    ok(abs(total - len(pcm) / 2 / SR) < 1e-6, "total ＝ pcm の長さ")
    ok(pcm[:2] == b"\x00\x00", "先頭はフェードで 0")

    script = [("c101", ["あ。"]), ("c102", ["い。"]), ("c201", ["う。"]), ("ca01", ["え。"]), ("ed01", ["お。"])]
    durs = {c: 10.0 for c, _ in script}
    tl, tot = timeline(durs, script, {"c102"})
    per = CSC.LEAD + 10.0 + CSC.TAIL
    ok(abs(tl["c101"][1] - per) < 1e-9, "1カット目＝LEAD＋声＋TAIL（第1章の頭に扉は無い）")
    ok(abs(tl["c102"][1] - (2 * per + CSC.TAIL_EXTRA_QUOTE)) < 1e-9, "決め所は余白を足す")
    ok(abs(tl["c201"][0] - (tl["c102"][1] + CSC.CARD_SEC)) < 1e-9, "第2章の頭に扉")
    ok(abs(tl["ca01"][0] - (tl["c201"][1] + CSC.CARD_SEC)) < 1e-9, "第10章（ca）の頭にも扉")
    ok(abs(tl["ed01"][0] - tl["ca01"][1]) < 1e-9, "ed01 は章でない＝扉なし")
    ok(abs(tot - (5 * per + CSC.TAIL_EXTRA_QUOTE + 2 * CSC.CARD_SEC)) < 1e-9, "全体の尺")
    ok(abs(tot - CSC.est_sec(0, 5, 5, 1, 1.0, 2) - 50.0) < 1e-9, "check_script の est_sec と同じ構造の尺")
    ok(nopunct_chars([("c1", ["Q: 「あ」、い。（う）・え？！"])]) == 4, "句読点なしの字数（印も数えない）")
    d1 = voice_defs("ep14", "A", 150)
    d2 = voice_defs("ep14", "A", 151)
    ok(d1[None][0] == d2[None][0] and d1[None][1]["話速"] == 150 and d2[None][1]["話速"] == 151,
       "名前は話速で変わらず、欄の話速が変わる")
    ok(d1["q"][1]["声種"] == "f1" and d1[None][1]["声種"] == "f2", "候補A＝説明 f2・聞き役 f1")
    ok(voice_defs("ep14", "B", 150)[None][1]["棒読み"] == "false" and d1[None][1]["棒読み"] == "true",
       "候補A は棒読み・B はアクセントあり")
    if fails:
        print(f"selftest: 落ちた {len(fails)}: {fails}")
        return 1
    print("selftest: 全部合格（アプリ・audio/ には触っていない）")
    return 0


def _arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--rate" in sys.argv:
        rate_report()
        sys.exit(0)
    sp = _arg("--speed")
    if "--listen" in sys.argv:
        sys.exit(listen(_arg("--listen"), _arg("--out"), _arg("--cand", "A"), "--kanji" in sys.argv, sp))
    cuts = [c.strip() for c in _arg("--cuts", "").split(",") if c.strip()] or None
    sys.exit(build(cuts, dry="--dry" in sys.argv, cand=_arg("--cand"), speed=sp))
