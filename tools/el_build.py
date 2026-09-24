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
import subprocess
import sys
import time
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

# 🔴🔴 TEMPO＝合成後の話速（2026-09-08・6本目キー橋の⑤a で新設）。
#    なぜ要るか: カズヤくん指示「話速は6本目から少し速く」（正本 §5）は **API では実現できない**。
#    `eleven_v3` は `voice_settings.speed` を見ない（`el_speed_probe.py` の実測＝速度比 0.98／
#    引き直しのばらつき 3.04% に埋もれる）。＝「1.05」は API 側では実現できないまま撤回されていた。
#    ここで ffmpeg の `atempo`（WSOLA・**音の高さは変えず長さだけ変える**）を合成後に当てて実現する。
#    ⚠️ 掛ける場所は **行の pcm 1本ずつ・GAP を足す前**。まとめて掛けると GAP まで縮んで
#       「間」の設計が崩れる。行ごとに掛ければ narration.json の t/d は自動で正しくなる。
#    ⚠️ TEMPO は指紋（_sig）に入れる。入れないと、値を変えても部分更新が「持ち越し可」と誤判定する
#       （feedback-gates-go-stale-when-upstream-changes）。合成キャッシュの鍵には**入らない**
#       ＝TEMPO を変えても API はもう叩かない（`--dry` で 0 クレジットで焼き直せる）。
#    ⚠️ 1.0 のときは ffmpeg を通さない（素通り）。5本目までの音は 1 バイトも変わらない。
#
# 🔴🔴 2026-09-13（7本目・声を Koichi-Deep Calm Japanese Narrator に替えた）: **1.05 → 0.91**。
#    Koichi は Hiro より **14.9% 速い**（同じ24文・speed1.0 で 6.388 対 5.562。
#    差14.9% > 物差しの誤差5.63% ＝測れている。`analytics/el_speed_probe_koichi.json`）。
#    ⚠️ **速い声をそのまま入れると、字数をいくら減らしても密度は下がらない。**
#       行間 GAP と カット頭尻 LEAD/TAIL の合計 256.5秒 は**構造で決まっていて字数では動かない**ので、
#       声が速くなると尺だけが縮み、**同じ字数でも 字/分 が上がる**（10,400字で 297→351字/分）。
#       ＝ 密度を戻す手は TEMPO しかない。
#    🔴 **1.0 に決定（2026-09-13・カズヤくん指示）。**私は 0.91（＝6本目と同じ 296字/分に戻す値）を
#       提案したが、カズヤくんが 1.0 を選んだ。**1.0 は atempo を一度も通さない**ので、
#       声に加工が1つもかからない（上の「1.0 のときは素通り」）。
#    その結果:実効 **6.171文字/秒**・35分の台本は **11,369字（325字/分）**。
#    ⚠️ 6本目は 297字/分 だったので、**9.3% 密になる**。④の台本は
#       [[feedback-jiko-plain-language]] を意識して**1文を短く**書く（字数は増えても、
#       1文あたりの情報は増やさない）。
#    ✅ TEMPO は**合成キャッシュの鍵に入っていない**＝あとで変えても **0クレジット**で焼き直せる。
#       ⑤a で密度が気になれば、ここだけ下げれば尺と密度が同時に直る。
# 🔴 2026-09-21（10本目⑥・試写）カズヤくん「**ナレーションをもう少し早く**」。
#    ⚠️ Otani は Sho より **8.3% ゆっくり**（37分28秒 → 40分36秒）。1.06 で Sho の速さにほぼ戻る。
#       見込み＝発話 2242.7秒 ÷ 1.06 ＝ 2115.7秒 ＋ 余白 193.75秒 ＝ **約 38分29秒**（40分の内側にも戻る）。
#    ⚠️ 1.0 でなくなるので **atempo を1段通る**（高さは変わらない）。
#       尺の規定を外してもらった理由（無加工）は失われるが、**耳の指摘のほうが上位**。
#    ✅ キャッシュの鍵に入っていないので **0クレジット**で焼き直せる（合わなければ何度でも変えてよい）。
# 🔴🔴 2026-09-24（12本目⑥・試写）カズヤくん「**ナレーションの話速を1.3に**。今の速さに対して1.3倍ではなく、
#    TEMPO 1 に対しての 1.3」。見込み（12本目）＝行の合計 2,060.2秒 × 1.06/1.30 → 完成尺 **約32分57秒**（1.06 は 39分17秒）。
#    ⚠️ 35〜40分の勝ち帯（記憶 feedback-duration-band-only-35-40-wins）の外に出る＝指摘したうえで指示を採った（新しい指示が優先）。
TEMPO = 1.30


# 🔴 2026-09-21（10本目⑥・試写）カズヤくん「**句点の後の間にバラつきがある**…決め所のあとの間や、
#    章の区切りの間は長めにとって良いが、その他はなるべく間を統一。間が長すぎる箇所がある」。
#    実測（`qa_out/ep10_pauses.txt`・0.25秒以上の無音 617か所）:
#      0.25〜0.50秒 **485か所（79%）**＝行間 GAP そのもの。ここはもう揃っている
#      0.80秒超 **78か所**／1.20秒超 41か所／2.00秒超 11か所・**最大 2.87秒**
#    ＝ばらついているのは **1行の中**で ElevenLabs が句点に作る間。**そこだけ上限を掛ける。**
#    ⚠️ 触らないもの＝①行と行の GAP（0.40秒・構造で一定）②決め所のうしろ（TAIL_EXTRA 2.0秒）
#       ③カットとカットの境（章の区切り）。この関数は**1行の pcm の内側**しか見ない。
#    ⚠️ 声を切らないよう、無音の判定は振幅 `PAUSE_TH` 以下が `PAUSE_MAX` を**超えた分だけ**を、
#       区間の**真ん中から**取り除く（両端は残すのでフェードもクリックも起きない）。
PAUSE_MAX = 0.60         # 行の中に許す無音の上限（秒）。中央値 0.40 の少し上＝自然な息継ぎは残る
PAUSE_TH = 300           # これ以下の振幅を無音とみなす（16bit。`qa_out/ep10_pauses.txt` と同じ値）


def cap_pauses(pcm: bytes, max_sec: float = None, th: int = PAUSE_TH) -> bytes:
    """行の中の無音が `max_sec` を超えたら、超えたぶんを真ん中から取り除く。"""
    import numpy as _np
    lim = PAUSE_MAX if max_sec is None else max_sec
    if lim <= 0:
        return pcm
    a = _np.frombuffer(pcm, dtype=_np.int16)
    q = _np.abs(a) <= th
    keep = _np.ones(len(a), dtype=bool)
    n = int(lim * SR)
    i, N = 0, len(a)
    while i < N:
        if q[i]:
            j = i
            while j < N and q[j]:
                j += 1
            # ⚠️ 行の頭と尻の無音は触らない（_trim と edge_fade の領分）
            if i > 0 and j < N and (j - i) > n:
                cut = (j - i) - n
                mid = (i + j) // 2
                keep[mid - cut // 2: mid - cut // 2 + cut] = False
            i = j
        else:
            i += 1
    return a[keep].tobytes()


# 🔴 2026-09-24（12本目⑥・試写）カズヤくん「**文と文の間が統一されていない**（決め語のあとの長めの間はOK）」。
#    実測（12本目・句点が行の中にある15行）：行の中の句点の間は 0.19〜0.60秒（中央 0.60＝上の上限に張り付き）で、
#    行と行の間 GAP 0.40 とそろっていない。→ **行の中の句点の数 k だけ、長い無音から k 個を GAP ちょうどにする。**
#    ⚠️ 読点の間は触らない（句点より短いのが自然）。行の頭と尻の無音も触らない（cap_pauses と同じ）。
#    ⚠️ 無音が k 個見つからない行（句点で間を置かなかった）は動かさない＝場所が分からないのに足さない。
#    ⚠️ カットとカットの間（LEAD 0.35＋TAIL 0.50＝0.85秒）はここの外＝絵の切り替えと尺に効くので、
#       再発防止策の別チャットで数字を見て決める（12本目⑥の引き継ぎ）。
STOP_MIN = 0.12          # これより短い無音は句点の間と見なさない（秒・TEMPO 後）


def n_stops(line: str) -> int:
    """行の**中**にある文の切れ目（。？！）の数。行末の句点は GAP が受け持つので数えない。"""
    body = line.rstrip("。？！ 　")
    return sum(body.count(c) for c in "。？！")


def even_stops(pcm: bytes, k: int, target: float = None, th: int = PAUSE_TH) -> bytes:
    """行の中の長い無音から k 個を target 秒（既定 GAP）ちょうどにそろえる。k=0・見つからなければ素通り。"""
    import numpy as _np
    if k <= 0:
        return pcm
    tgt = int(round((GAP if target is None else target) * SR))
    a = _np.frombuffer(pcm, dtype=_np.int16)
    q = _np.abs(a) <= th
    runs, i, N, m = [], 0, len(a), int(STOP_MIN * SR)
    while i < N:
        if q[i]:
            j = i
            while j < N and q[j]:
                j += 1
            if i > 0 and j < N and (j - i) >= m:
                runs.append((i, j))
            i = j
        else:
            i += 1
    if len(runs) < k:
        return pcm
    pick = sorted(sorted(runs, key=lambda r: r[1] - r[0], reverse=True)[:k])
    segs, prev = [], 0
    for i, j in pick:
        L = j - i
        segs.append(a[prev:i])
        if L >= tgt:                          # 長い＝真ん中を抜く（両端の無音は残す）
            h = tgt // 2
            segs.append(a[i:i + h])
            segs.append(a[j - (tgt - h):j])
        else:                                 # 短い＝真ん中にデジタル無音を足す（行と行の GAP と同じ無音）
            mid = (i + j) // 2
            left, right = a[i:mid].astype(_np.float32), a[mid:j].astype(_np.float32)
            f = min(48, len(left), len(right))          # 2ms の小さなフェード（無音の中の段差でクリックを出さない）
            if f:
                left[-f:] *= _np.linspace(1.0, 0.0, f)
                right[:f] *= _np.linspace(0.0, 1.0, f)
            segs += [left.astype(_np.int16), _np.zeros(tgt - L, dtype=_np.int16), right.astype(_np.int16)]
        prev = j
    segs.append(a[prev:])
    return _np.concatenate(segs).astype(_np.int16).tobytes()


def retempo(pcm: bytes, tempo: float = None) -> bytes:
    """話速だけを変える（音の高さは変えない）。raw s16le mono SR を ffmpeg atempo に通す。"""
    t = TEMPO if tempo is None else tempo
    if abs(t - 1.0) < 1e-9:
        return pcm
    if not (0.5 <= t <= 2.0):        # atempo の1段の有効範囲。外は黙って歪むので止める
        raise SystemExit(f"🔴 TEMPO が atempo の範囲外: {t}")
    # 🔴🔴 2026-09-21（11本目⑤a）: **atempo の結果を置いておく。**
    #    この関数は**行ごとに ffmpeg を1本起動する**（473行＝473回）。TEMPO は合成キャッシュの鍵に
    #    わざと入れていない（あとで変えても 0クレジットで焼き直せるようにするため）ので、
    #    **焼き直すたびに 473回の起動をやり直していた**。コミット上限が近いこの環境では、
    #    そのどこか1回が `WinError 1455` で落ちて全部やり直しになる（実際に 369行目と 419行目で落ちた）。
    #    ⭐ ここに置いておけば、**2回目からは ffmpeg をほとんど起動しない**＝落ちる隙が無くなる。
    #    ⚠️ これは**合成キャッシュとは別の棚**（`_tempo/`）。鍵は「元の pcm の中身 ＋ tempo」なので、
    #       TEMPO を変えれば別の鍵になり、**「TEMPO は鍵に入っていない」という約束は壊れない**
    #       （合成＝el_tts のキャッシュは今までどおり TEMPO を見ない＝0クレジットで焼き直せる）。
    #    ⚠️ 容量＝合成キャッシュとほぼ同じ（11本目で約240MB）。C: が細いときは `_tempo/` を消してよい
    #       （消えても ffmpeg を回し直すだけで、クレジットは1も要らない）。
    tdir = ES.cache_path("x").parent.parent / f"{ES.SLUG}_tempo"
    key = hashlib.sha1(pcm).hexdigest() + f"_{t:.4f}"
    tp = tdir / f"{key}.pcm"
    if tp.exists():
        return tp.read_bytes()
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error",
           "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0",
           "-filter:a", f"atempo={t}", "-f", "s16le", "-ac", "1", "-ar", str(SR), "pipe:1"]
    # 🔴🔴 2026-09-21（11本目⑤a）: **ffmpeg を起動できずに全編が落ちた。**
    #    `OSError: [WinError 1455] ページング ファイルが小さすぎるため…`＝Windows の**コミット上限**。
    #    実測＝上限 19.9GB（物理 11.9＋ページング 8）に対し**空き 0.2GB**・claude が **27プロセスで 12.7GB**。
    #    この関数は**行ごとに ffmpeg を1本起動する**（473行＝473回）ので、
    #    一瞬でも空きが無い瞬間に当たると、そこまでの合成を道連れにして止まる（369/473行で停止）。
    #    ⚠️ **クレジットは失わない**（合成キャッシュは内容で引くので、焼き直しは当たった行を叩かない）が、
    #       時間と、落ちるまでの往復は失う。＝**待って振り直せば直る型**なので、ここで数回粘る。
    #    ⚠️ 直らないときはメモリを空ける（claude の窓を閉じる）。**ページングファイルの設定は触らない**
    #       ＝システム設定なのでカズヤくんの仕事（[[reference-tts-fails-on-commit-limit]] と同じ環境）。
    last = None
    for wait in (0, 2, 5, 10, 20):
        if wait:
            time.sleep(wait)
        try:
            r = subprocess.run(cmd, input=pcm, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # ⚠️ **MemoryError も捕まえる**（2026-09-21・3回目の落ち方）。
        #    `OSError` は「**ffmpeg を起動できない**」（WinError 1455）。
        #    `MemoryError` は起動はできたが「**出力を読む python 側がメモリを取れない**」
        #    （`subprocess` の `_readerthread` の `fh.read()` で出た）。
        #    どちらも**待てば直る同じ原因**（コミット上限）なので、同じ棚で振り直す。
        #    最初 OSError だけを捕まえたら、3回目は MemoryError ですり抜けて止まった。
        except (OSError, MemoryError) as e:
            last = e
            print(f"    ⚠️ ffmpeg に失敗（{e.__class__.__name__}: {e}）→ {wait or 0}秒待って振り直す", flush=True)
            continue
        if r.returncode != 0 or not r.stdout:
            raise SystemExit(f"🔴 atempo に失敗: {r.stderr.decode('utf-8', 'replace')[:300]}")
        tdir.mkdir(parents=True, exist_ok=True)
        tmp = tp.with_suffix(".tmp")        # 途中で落ちた半端なファイルを本物の名前で残さない
        tmp.write_bytes(r.stdout)
        tmp.replace(tp)
        return r.stdout
    raise SystemExit(f"🔴 ffmpeg が5回とも失敗（{last.__class__.__name__}: {last}）。"
                     f"メモリの空きを確認する: Get-CimInstance Win32_OperatingSystem の FreeVirtualMemory"
                     f"（見るのは FreeVirtualMemory＝コミットの空き。FreePhysicalMemory では分からない）")


def _sig(lines):
    """カットの指紋＝**実際にエンジンへ渡る文字列**と声・モデル・設定・GAP・TEMPO から取る（narration._sig と同じ思想）。"""
    spoken = "".join(ES.el_text(x) for x in lines)
    return hashlib.sha1(f"{spoken}|{el_tts.VOICE}|{el_tts.MODEL}|{json.dumps(ES.SETTINGS, sort_keys=True)}"
                        f"|{GAP}|{TEMPO}|{PAUSE_MAX}|stops{STOP_MIN}"   # 🔴 合成のあとに音を変える定数は全部ここに入れる
                        #    （入れ忘れると「値を変えたのに wav が作り直されない」＝黙って前の音のまま）
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
        pcm = retempo(pcm)                   # 🔴 話速（GAP を足す前・行ごとに掛ける）
        pcm = cap_pauses(pcm)                # 🔴 行の中の長すぎる間だけ詰める（GAP は触らない）
        pcm = even_stops(pcm, n_stops(line))  # 🔴 行の中の句点の間を GAP にそろえる（2026-09-24）
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
        # 🔴 speed＝**実効の話速**。API の speed は eleven_v3 に効かないので、合成後の atempo（TEMPO）が実効値。
        #    「何で焼いたか」の記録なので、効かない 1.0 を書き残すと後から嘘になる。
        "speaker": f"elevenlabs:{el_tts.VOICE}", "speed": TEMPO, "tempo": TEMPO, "credit": "",
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
    # 本編の見込み尺＝発話＋行間（durations に含む）＋カットごとの LEAD 0.35＋TAIL 0.50＋quote の TAIL_EXTRA 2.0×決め所
    # 🔴 2026-09-07: 決め所の数を **12 と直に書いてあった**（サーフサイド固有）。回が替わると黙って外れるので
    #    el_script.EXPECT[SLUG]["quotes"] から取る（SL-1 は 17）。clean() が ★ を外すので SCRIPT からは数えられない。
    nq = ES.EXPECT[ES.SLUG]["quotes"]
    est = chars_all / rate + n * 0.85 + nq * 2.0
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
    print(f"本編の見込み {est/60:.1f}分（全 {chars_all}字をこの速さで＋LEAD/TAIL 0.85×{n}＋quote 2.0×{nq}。"
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

    # ── ① TEMPO=1.0（素通り）＝組み立てそのものの検算。ここは 1 サンプルも動いてはいけない ──
    global TEMPO
    keep = TEMPO
    try:
        TEMPO = 1.0
        pcm, total, rows = build_cut("t1", ["あいうえお。", "かきくけこさしすせそ。"], synth)
        ok(len(rows) == 2 and rows[0]["t"] == 0.0, "字幕 rows の形")
        ok(abs(rows[1]["t"] - (rows[0]["d"] + GAP)) < 1e-6, "2行目の t ＝ 1行目の d ＋ GAP")
        ok(abs(total - (rows[0]["d"] + GAP + rows[1]["d"])) < 1e-6, "total ＝ 発話＋GAP")
        ok(len(pcm) == (fake["t1-1"] + int(GAP * SR) + fake["t1-2"]) * 2, "pcm の長さ")
        ok(struct.unpack("<h", pcm[:2])[0] == 0, "先頭が 5ms フェードで 0")
        ok(retempo(b"\x00\x00" * 100, 1.0) == b"\x00\x00" * 100, "TEMPO 1.0 は 1バイトも変えない")

        # ── ② TEMPO=1.05 の陽性対照（2026-09-08 新設）──────────────────────
        # 🔴 見るのは3つ:「発話だけが縮む」「GAP は縮まない」「t/d が縮んだ音と合う」。
        #    ⚠️ atempo は WSOLA のフレーム単位なので比はぴったり 1.05 にならない（実測 1.048）。
        #    ここを「== 1.05」で書くと**正しく動いていても落ちる**ので、幅で見る。
        TEMPO = 1.05
        fake.clear()
        pcm2, total2, rows2 = build_cut("t1", ["あいうえお。", "かきくけこさしすせそ。"], synth)
        speech1 = (fake["t1-1"] + fake["t1-2"]) / SR          # 素の発話（GAP を含まない）
        speech2 = rows2[0]["d"] + rows2[1]["d"]
        ok(1.03 <= speech1 / speech2 <= 1.07, f"発話が約5%縮む（実測 {speech1 / speech2:.4f}）")
        ok(abs(rows2[1]["t"] - (rows2[0]["d"] + GAP)) < 2e-3, "縮めても 2行目の t ＝ 1行目の d ＋ GAP")
        ok(abs(total2 - (speech2 + GAP)) < 2e-3, "total ＝ 縮んだ発話＋GAP（GAP は縮まない）")
        ok(abs(len(pcm2) / 2 / SR - total2) < 2e-3, "pcm の長さ ＝ total")
        ok(total2 < total, "TEMPO を上げると尺が短くなる")
        # 指紋は TEMPO で変わる（変わらないと、値を変えても部分更新が「持ち越し可」と誤判定する）
        sig_fast = _sig(["あ", "い"])
        TEMPO = 1.0
        ok(_sig(["あ", "い"]) != sig_fast, "指紋は TEMPO で変わる")
    finally:
        TEMPO = keep

    s1 = _sig(["あ", "い"])
    s2 = _sig(["あ", "う"])
    ok(s1 != s2 and s1 == _sig(["あ", "い"]), "指紋は本文で変わる・同じ本文で同じ")

    # ── ③ 句点の間をそろえる（2026-09-24 新設）──────────────────────────────
    #    陽性対照：短い間（0.20秒）は伸び、長い間（0.80秒）は縮んで、どちらも GAP ちょうど。
    #    陰性対照：句点の無い行（k=0）と、間が見つからない行は 1バイトも変えない。
    tone = struct.pack(f"<{SR // 2}h", *([2000] * (SR // 2)))       # 0.5秒の「声」
    want = (2 * (SR // 2) + int(round(GAP * SR))) * 2                 # 声＋GAP＋声（バイト）
    for sec in (0.20, 0.80):
        out = even_stops(tone + b"\x00\x00" * int(sec * SR) + tone, 1)
        ok(abs(len(out) - want) <= 4, f"間 {sec:.2f}秒 → GAP（実測 {(len(out) - 2 * len(tone)) / 2 / SR:.3f}秒）")
    short = tone + b"\x00\x00" * int(0.20 * SR) + tone
    ok(even_stops(short, 0) == short, "句点の無い行（k=0）は1バイトも変えない")
    ok(even_stops(tone + tone, 1) == tone + tone, "間が見つからない行は動かさない")
    ok(n_stops("1954年3月1日、午前6時45分。太平洋のまん中の、ビキニ環礁。") == 1 and n_stops("あいう。") == 0,
       "文の切れ目は行の中だけ数える（行末の句点は数えない）")
    if fails:
        print(f"selftest: 落ちた: {fails}")
        return 1
    print("selftest: 18/18 合格（API は叩いていない）")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    cuts = None
    if "--cuts" in sys.argv:
        cuts = [c.strip() for c in sys.argv[sys.argv.index("--cuts") + 1].split(",") if c.strip()]
    sys.exit(build(cuts, dry="--dry" in sys.argv))
