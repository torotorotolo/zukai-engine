# -*- coding: utf-8 -*-
"""★焼き上がった本編 mp4 を、仕様と突き合わせる（⑥ の通し検品）。

■ なぜ作ったか
  焼くところまでは門番が揃っているのに、**焼けた mp4 そのものを機械で見る道具が無かった。**
  過去の事故：
    - `--dry` が尺ファイルを上書きして**音ズレのまま焼けた**
      （[[feedback-dry-run-overwrites-timings]]＝焼く前にコマ数と秒数を突合せよ）
    - パイプでつなぐと失敗が exit 0 に化ける
      （[[feedback-pipes-mask-exit-codes]]＝exit 0 でも成果物の実体を見よ）

■ 見るもの（どれも「在るか」でなく「合っているか」）
  1. 総尺が設計と一致するか（`scene_jiko` の組み立て＝LEAD/TAIL/TAIL_EXTRA 込み）
  2. コマ数が 総尺 × 30fps と一致するか
  3. 音声が入っているか。**映像と音声の尺の差**（音ズレの目安）
  4. 解像度・fps・コーデック
  5. 無音で終わっていないか（末尾 5秒の実効音量）
  6. 🔴 **章名が前作のまま残っていないか**（2026-09-07 追加・設計ノート §9-6）

■ 🔴 6 の章名（3本目スレッシャー号で実際に落ちた穴）
  `scene_jiko.CHAPTERS` は**画面の隅に出る章名**、台本の章見出しは `narration.py` の
  `# ── 第N章　…` のコメント。**別々に書くので、片方だけ差し替えると食い違う。**
  3本目は本編を焼き上げたあとで、隅が「3/6 毎秒10メートルの風」＝**2本目（123便）の
  章名のまま**だったことに気づいた。机上検査5種は1つも落ちない（文字として正しく出るため）。
  → 焼けた mp4 を見るこの道具で、**章の数・番号・名前を1件ずつ突き合わせる**。
  ⚠️ 台本側の見出しは `# ── 第N章　<名前>（…` の形だけを読む。本文中の「第4章」は読まない。

使い方:
    python tools/check_final.py out/jiko/titan_audio-ss.mp4
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

FPS = 30
TOL_SEC = 1.0          # 総尺のずれの許容（秒）
TOL_AV = 0.30          # 映像と音声の尺の差の許容（秒）
TAIL_DB = -50.0        # 末尾5秒がこれより静かなら「無音で終わっている」


def ffprobe(path, args):
    """⚠️ 読めなければ 0 で埋めずに落ちる（fail closed）。"""
    r = subprocess.run(["ffprobe", "-v", "error", *args, str(path)],
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"🔴 ffprobe が読めなかった: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


def expected():
    """設計の総尺。**narration.json だけで積むと LEAD/TAIL のぶんずれる。**"""
    import scene_jiko as S
    dur = json.load(open(Path(__file__).parent.parent / "audio" / "narration.json",
                         encoding="utf-8"))["durations"]
    return sum(round(dur[c] + S.LEAD + S.TAIL + S._tail_extra(c), 2) for c in dur), len(dur)


CH_RE = re.compile(r"^\s*#\s*─+\s*第(\d+)章[　\s]+(.+?)(?:（|\(|\s*─|$)")


def script_chapters():
    """台本（`narration.py` の `# ── 第N章　…`）側の章見出し {番号: 名前}。

    🔴 fail closed：1件も読めなければ 0件を返さずに落とす（形が変わったのに
       「合っている」と言わせない。[[feedback-parsers-fail-closed]]）。
    """
    src = Path(__file__).parent / "narration.py"
    out = {}
    for ln in src.read_text(encoding="utf-8").splitlines():
        m = CH_RE.match(ln)
        if m:
            n = int(m.group(1))
            name = m.group(2).strip().rstrip("─ 　")
            if n in out and out[n] != name:
                raise SystemExit(f"🔴 台本に第{n}章の見出しが2通りある: "
                                 f"{out[n]!r} と {name!r}")
            out[n] = name
    if not out:
        raise SystemExit("🔴 台本から章見出しを1件も読めなかった "
                         "（`# ── 第N章　…` の形が変わった？ 0件で通さない）")
    return out


def check_chapters():
    """🔴 画面に出る章名（`scene_jiko.CHAPTERS`）と台本の章見出しを1件ずつ突き合わせる。"""
    import scene_jiko as S
    screen = {n: nm for _, (n, nm) in S.CHAPTERS.items()}
    book = script_chapters()
    ng = []
    print(f"   章 画面 {len(screen)} ／ 台本 {len(book)}")
    for n in sorted(set(screen) | set(book)):
        a, b = screen.get(n), book.get(n)
        if a == b:
            print(f"     ✓ {n}/{len(screen)} {a}")
        else:
            print(f"     🔴 第{n}章  画面「{a}」 ≠ 台本「{b}」")
            ng.append(f"第{n}章の章名が食い違う（画面「{a}」／台本「{b}」）"
                      f"＝前作のまま残っている恐れ")
    if len(screen) != getattr(S, "NCH", len(screen)):
        ng.append(f"CHAPTERS が {len(screen)}件 なのに NCH が {S.NCH}"
                  f"（隅の「n/{S.NCH}」が合わない）")
    return ng


def selftest():
    """🔴 章名の門番の陽性対照。**本番の `check_chapters()` そのもの**を通す。

    陽性対照は作り物ではなく、**実際に起きた事故の状態**を git から取って復元する
    （3本目スレッシャー号を焼いたとき、隅が2本目 123便の章名のままだった）。
    """
    import scene_jiko as S
    ok = True

    def say(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '🔴'} {msg}")

    book = script_chapters()
    say(len(book) >= 1, f"台本から章見出しを {len(book)}件 読めた: "
                        + "／".join(f"{n} {book[n]}" for n in sorted(book)))
    ng = check_chapters()
    say(not ng, f"いまの CHAPTERS と台本は合っている（粗 {len(ng)}件）")

    # 🔴 事故の復元＝**前作の章名のまま**（git から取る。2本目 8b5d129／3本目 ad6882a）
    keep = S.CHAPTERS, getattr(S, "NCH", len(S.CHAPTERS))
    for commit, label in (("8b5d129", "2本目 123便"), ("ad6882a", "3本目 スレッシャー号")):
        r = subprocess.run(["git", "show", f"{commit}:tools/scene_jiko.py"],
                           cwd=Path(__file__).parent.parent,
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        m = re.search(r"^CHAPTERS = \{(.*?)^\}", r.stdout, re.S | re.M)
        if r.returncode != 0 or not m:
            say(False, f"git から {label} の CHAPTERS を取り出せない（陽性対照が作れない）")
            continue
        old = {}
        for k, n, nm in re.findall(r'"(c\d)":\s*\((\d+),\s*"([^"]+)"\)', m.group(1)):
            old[k] = (int(n), nm)
        try:
            S.CHAPTERS, S.NCH = old, len(old)
            got = check_chapters()
        finally:
            S.CHAPTERS, S.NCH = keep
        say(len(got) >= len(old),
            f"{label} の章名のままだと {len(got)}件 鳴る（{len(old)}章とも食い違う）")
    say(check_chapters() == [], "戻すと黙る")

    # 🔴 読めない形は 0件で通さない（fail closed）
    keep_re = globals()["CH_RE"]
    try:
        globals()["CH_RE"] = re.compile(r"^\s*#\s*ZZZ第(\d+)章[　\s]+(.+?)$")
        script_chapters()
        say(False, "章見出しを1件も読めないのに落ちなかった")
    except SystemExit:
        say(True, "章見出しを1件も読めなければ落ちる（0件で通さない）")
    finally:
        globals()["CH_RE"] = keep_re

    # ⚠️ 本文中の「第4章」を拾っていないか（narration.py の c525・c625 に実在する）
    body = script_chapters()
    say(all(len(v) < 30 for v in body.values()),
        "本文中の「第4章…」は拾っていない（見出しだけ）")
    print("  " + ("✓ 陽性対照 7/7" if ok else "🔴 陽性対照に落ちた"))
    return ok


def main():
    if len(sys.argv) < 2:
        raise SystemExit("使い方: python tools/check_final.py <mp4>　／　--selftest")
    p = Path(sys.argv[1])
    if not p.exists():
        raise SystemExit(f"🔴 mp4 が無い: {p}")

    want, n_cuts = expected()
    ng = []

    j = json.loads(ffprobe(p, ["-show_streams", "-show_format", "-of", "json"]))
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    if v is None:
        raise SystemExit("🔴 映像トラックが無い")

    total = float(j["format"]["duration"])
    size_mb = int(j["format"]["size"]) / 1e6
    print(f"■ {p.name}　{size_mb:.1f} MB")
    print(f"   カット {n_cuts} ／ 設計の総尺 {want:.1f}秒 = {int(want//60)}分{want%60:04.1f}秒")
    print(f"   実際の総尺 {total:.1f}秒 = {int(total//60)}分{total%60:04.1f}秒"
          f"　差 {total - want:+.2f}秒")
    if abs(total - want) > TOL_SEC:
        ng.append(f"総尺が設計と {total - want:+.2f}秒 ずれている（許容 ±{TOL_SEC}秒）")

    # コマ数（**数え直す**。nb_frames はコンテナの申告で当てにならないことがある）
    cnt = ffprobe(p, ["-select_streams", "v:0", "-count_frames",
                      "-show_entries", "stream=nb_read_frames",
                      "-of", "default=nw=1:nk=1"])
    frames = int(cnt)
    want_frames = int(round(want * FPS))
    print(f"   コマ数 {frames} ／ 設計 {want_frames}　差 {frames - want_frames:+d}")
    if abs(frames - want_frames) > FPS * TOL_SEC:
        ng.append(f"コマ数が設計と {frames - want_frames:+d} ずれている")

    fps = eval(v["r_frame_rate"])  # 例 "30/1"
    print(f"   {v['width']}x{v['height']} / {fps:g}fps / {v['codec_name']}")
    if (v["width"], v["height"]) != (1920, 1080):
        ng.append(f"解像度が {v['width']}x{v['height']}（1920x1080 でない）")
    if abs(fps - FPS) > 0.01:
        ng.append(f"fps が {fps}（{FPS} でない）")

    if a is None:
        ng.append("🔴 音声トラックが無い")
    else:
        adur = float(a.get("duration") or j["format"]["duration"])
        print(f"   音声 {a['codec_name']} {a['sample_rate']}Hz {a['channels']}ch"
              f" / 尺 {adur:.2f}秒　映像との差 {adur - total:+.2f}秒")
        if abs(adur - total) > TOL_AV:
            ng.append(f"映像と音声の尺が {adur - total:+.2f}秒 違う（音ズレの恐れ）")

        # 末尾5秒が無音でないか
        r = subprocess.run(
            # ⚠️ `-v error` にすると volumedetect の出力ごと消える（info で出るため）。
            #    静かにしたくて loglevel を下げると、**測れないのに測れたつもりになる。**
            ["ffmpeg", "-hide_banner", "-nostats", "-v", "info",
             "-sseof", "-5", "-i", str(p),
             "-af", "volumedetect", "-f", "null", "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace")
        mean = [ln for ln in r.stderr.splitlines() if "mean_volume" in ln]
        if mean:
            db = float(mean[0].split(":")[1].strip().split()[0])
            print(f"   末尾5秒の平均音量 {db:.1f} dB")
            if db < TAIL_DB:
                ng.append(f"末尾5秒がほぼ無音（{db:.1f} dB）")
        else:
            ng.append("末尾5秒の音量が測れなかった（volumedetect が読めない）")

    ng += check_chapters()

    print()
    if ng:
        for x in ng:
            print("🔴", x)
        print(f"🔴 通し検品に粗 {len(ng)}件")
        return 1
    print("✓ 通し検品は通った（尺・コマ数・解像度・音声・音ズレ・末尾・章名）")
    print("⚠️ これは試写の代わりではない。**カズヤくんが本番動画を見るまで公開しない。**")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    sys.exit(main())
