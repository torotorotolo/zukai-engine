# -*- coding: utf-8 -*-
r"""el_build.py — ElevenLabs で全カットを合成し、AivisSpeech 版の build と**同じ形**の audio/narration.json を出す。

  python tools/el_build.py                     … 全カット（キャッシュが効く＝直した行だけ API を叩く）
  python tools/el_build.py --cuts pr01,pr02    … 一部だけ合成して narration.json を部分更新（他のカットは前回のまま）
  python tools/el_build.py --dry               … API を叩かない。キャッシュにある行だけで wav と json を組む（無い行は止まる）
  python tools/el_build.py --selftest          … 組み立ての検算（API 不使用）

出力（scene_jiko / audio_mix / audio_pack が読む形はそのまま）:
  audio/<cid>.wav      … 24kHz mono 16bit。行と行の間は GAP 秒の無音。audio_mix.read_wav が 44.1kHz に補間する
  audio/narration.json … durations（発話＋行間の合計秒）／subtitles（行ごとの t・d・text）／signatures
                          ＋ engine/voice/model/settings（何で焼いたかの記録。scene_jiko は読まない）

⚠️ 行と行の間（GAP）:
  AivisSpeech の wav は頭と尻に無音を含んでいたので GAP=0.18 で足りた。ElevenLabs は el_tts._trim で
  30ms まで切っているので、句点の間として GAP を厚く取る。⑤a の1章ぶんの実測で決める（尺にも効く）。
⚠️ 台本から消えたカットの wav は消す（AivisSpeech 版と同じ。3本目の241本がここで消える）。
"""
import hashlib
import json
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
import el_tts                       # noqa: E402
import el_artifacts as ART          # noqa: E402
import el_script as ES              # noqa: E402
import narration                    # noqa: E402  SCRIPT の正本

GAP = 0.40          # 行と行のあいだに置く無音（秒）。ElevenLabs は前後を切ってあるぶん AivisSpeech の 0.18 より厚い
SR = el_tts.SR
AUDIO = ROOT / "audio"


def _sig(lines):
    """カットの指紋＝**実際にエンジンへ渡る文字列**と声・モデル・設定・GAP から取る（narration._sig と同じ思想）。"""
    spoken = "".join(ES.el_text(x) for x in lines)
    return hashlib.sha1(f"{spoken}|{el_tts.VOICE}|{el_tts.MODEL}|{json.dumps(ES.SETTINGS, sort_keys=True)}|{GAP}"
                        .encode("utf-8")).hexdigest()[:12]


def write_wav(path, pcm):
    with wave.open(str(path), "w") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm)


def build_cut(cid, lines, synth):
    """1カットぶん。行ごとに合成→5msフェード→GAP で連結。(wavのpcm, 秒, 字幕rows) を返す。"""
    chunks, rows, t = [], [], 0.0
    gap = b"\x00\x00" * int(GAP * SR)
    for i, line in enumerate(lines, 1):
        sent = ES.el_text(line)
        pcm = synth(sent, f"{cid}-{i}")
        pcm = ART.edge_fade(pcm, 5)          # デジタル無音へ直結するクリック止め（長さ不変）
        sec = len(pcm) / 2 / SR
        rows.append({"t": round(t, 3), "d": round(sec, 3), "text": line})
        chunks.append(pcm)
        chunks.append(gap)
        t += sec + GAP
    total = t - GAP
    return b"".join(chunks[:-1]), total, rows


def build(cuts=None, dry=False):
    AUDIO.mkdir(exist_ok=True)
    jp = AUDIO / "narration.json"
    prev = json.loads(jp.read_text(encoding="utf-8")) if jp.exists() else {}
    if cuts is None:
        targets = [c for c, _ in narration.SCRIPT]
    else:
        known = {c for c, _ in narration.SCRIPT}
        bad = [c for c in cuts if c not in known]
        if bad:
            raise SystemExit(f"🔴 台本に無いカット: {bad}")
        targets = cuts

    if dry:
        def synth(sent, lid):
            p = ES.cache_path(sent)
            if not p.exists():
                raise SystemExit(f"🔴 --dry: キャッシュが無い行 {lid}: {sent[:30]}")
            return p.read_bytes()
    else:
        v = el_tts.check_voice()          # 門番：別の Hiro を掴んでいないか
        c0, lim = el_tts.credits_used()
        print(f"ElevenLabs: 声={v['name']}（{el_tts.VOICE}） モデル={el_tts.MODEL} settings={ES.SETTINGS} "
              f"／クレジット {c0:,} / {lim:,}／GAP {GAP}s", flush=True)

        def synth(sent, lid):
            return el_tts.synth(sent, lid, slug=ES.SLUG, settings=ES.SETTINGS)

    durs, subs, sigs = {}, {}, {}
    kept = built = 0
    skipped = []
    longest = (0.0, "")
    for cid, lines in narration.SCRIPT:
        if cid not in targets:
            # 部分更新：前回の記録を持ち越す。🔴 ただし**指紋が今の台本・声・設定と一致するものだけ**。
            #    カットIDは題材をまたいでぶつかる（c101… は3本目にも在る）ので、ID が同じだけで持ち越すと
            #    3本目の秒数と字幕が黙って混ざる（2026-09-05 に実際に 171 カット混ざった）。
            if (prev.get("engine") == "elevenlabs"
                    and prev.get("signatures", {}).get(cid) == _sig(lines)
                    and (AUDIO / f"{cid}.wav").exists()):
                durs[cid] = prev["durations"][cid]
                subs[cid] = prev["subtitles"][cid]
                sigs[cid] = prev["signatures"][cid]
                kept += 1
            else:
                skipped.append(cid)
            continue
        pcm, total, rows = build_cut(cid, lines, synth)
        write_wav(AUDIO / f"{cid}.wav", pcm)
        durs[cid], subs[cid], sigs[cid] = round(total, 2), rows, _sig(lines)
        for r in rows:
            if r["d"] > longest[0]:
                longest = (r["d"], r["text"])
        built += 1
        print(f"{cid}: {total:6.2f}s  ({len(lines)}行)", flush=True)

    jp.write_text(json.dumps({
        "engine": "elevenlabs", "voice": el_tts.VOICE, "voice_name": el_tts.VOICE_NAME,
        "model": el_tts.MODEL, "settings": ES.SETTINGS,
        "speaker": f"elevenlabs:{el_tts.VOICE}", "speed": 1.0, "credit": "",
        "gap": GAP, "durations": durs, "subtitles": subs, "signatures": sigs,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # 記録に無いカットの wav（3本目の残り・今回まだ作っていないカット）は消す＝wav と json を常に1対1にする
    gone = 0
    for f in AUDIO.glob("*.wav"):
        if f.stem not in durs:
            f.unlink()
            gone += 1
    if gone:
        print(f"（記録に無いカットの wav を {gone} 本削除）")

    n = len(narration.SCRIPT)
    done = {c: ls for c, ls in narration.SCRIPT if c in durs}
    chars = sum(len(l) for ls in done.values() for l in ls)
    chars_all = sum(len(l) for _, ls in narration.SCRIPT for l in ls)
    speech = sum(durs.values())
    rate = chars / max(speech, 1e-9)                 # 字/秒（行間込み）＝AivisSpeech の 5.52 と同じ物差し
    # 本編の見込み尺＝発話＋行間（durations に含む）＋カットごとの LEAD 0.35＋TAIL 0.50＋quote の TAIL_EXTRA 2.0×12
    est = chars_all / rate + n * 0.85 + 12 * 2.0
    print(f"\n合成 {built} カット／持ち越し {kept} カット／未作成 {len(skipped)}／記録 {len(durs)}／台本 {n}")
    if skipped:
        print(f"⚠️ まだ作っていないカット {len(skipped)}: {','.join(skipped[:8])}{'…' if len(skipped) > 8 else ''}")
    print(f"作ったぶん: {len(durs)}カット {chars}字 → 発話＋行間 {speech:.1f}秒（{rate:.2f}字/秒・行間込み。AivisSpeech は 5.52）")
    # 🔴 許容範囲は **`check_script` の定数から取る**（2026-09-07）。
    #    ⚠️ ここは長らく「設計 36分43秒・許容 35〜38分」と**文字で書いてあった**＝
    #       下限を 35分→30分 に変えても、書き手には古い範囲が表示され続ける形だった。
    #       「設計 36分43秒」もサーフサイド固有なので落とした（次の題材では嘘になる）。
    import check_script as CSC
    lo, hi = CSC.DUR_MIN / 60, CSC.DUR_MAX / 60
    print(f"本編の見込み {est/60:.1f}分（全 {chars_all}字をこの速さで＋LEAD/TAIL 0.85×{n}＋quote 2.0×12。"
          f"許容 {lo:.0f}〜{hi:.0f}分{'' if CSC.dur_ok(est) else ' ← 🔴 外'}）")
    print(f"最長の1行 = {longest[0]:.2f}秒「{longest[1]}」")
    if not dry:
        st = el_tts.stats()
        c1, _ = el_tts.credits_used()
        print(f"API {st['api']}行（{st['chars']:,}字）／キャッシュ {st['cache']}行／振り直し {st['retakes']}回"
              f"／本物と判定 {st['real']}／要耳 {st['unsure']}（記録＝audio/el_qa/{ES.SLUG}_el_retakes.tsv）")
        print(f"クレジット {c0:,} → {c1:,}（消費 {c1-c0:,}）⚠️ 反映が遅れることがある")
    return 0 if len(durs) == n else 1


def selftest() -> int:
    """API を叩かずに組み立てを検算する。"""
    import struct
    fails = []
    ok = lambda c, name: (None if c else fails.append(name))
    fake = {}

    def synth(sent, lid):
        n = int(SR * (0.5 + 0.1 * len(sent) / 10))
        fake[lid] = n
        return struct.pack(f"<{n}h", *([1000] * n))

    pcm, total, rows = build_cut("t1", ["あいうえお。", "かきくけこさしすせそ。"], synth)
    ok(len(rows) == 2 and rows[0]["t"] == 0.0, "字幕 rows の形")
    ok(abs(rows[1]["t"] - (rows[0]["d"] + GAP)) < 1e-6, "2行目の t ＝ 1行目の d ＋ GAP")
    ok(abs(total - (rows[0]["d"] + GAP + rows[1]["d"])) < 1e-6, "total ＝ 発話＋GAP")
    ok(len(pcm) == (fake["t1-1"] + int(GAP * SR) + fake["t1-2"]) * 2, "pcm の長さ")
    ok(struct.unpack("<h", pcm[:2])[0] == 0, "先頭が 5ms フェードで 0")
    s1 = _sig(["あ", "い"])
    s2 = _sig(["あ", "う"])
    ok(s1 != s2 and s1 == _sig(["あ", "い"]), "指紋は本文で変わる・同じ本文で同じ")
    if fails:
        print(f"selftest: 落ちた: {fails}")
        return 1
    print("selftest: 6/6 合格（API は叩いていない）")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    cuts = None
    if "--cuts" in sys.argv:
        cuts = [c.strip() for c in sys.argv[sys.argv.index("--cuts") + 1].split(",") if c.strip()]
    sys.exit(build(cuts, dry="--dry" in sys.argv))
