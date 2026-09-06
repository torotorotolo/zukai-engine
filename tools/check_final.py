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

⚠️ これは**カズヤくんが本番動画を見る「試写」の代わりにはならない**
   （[[feedback-confirm-before-video-render]]＝公開ゲートは2段）。

使い方:
    python tools/check_final.py out/jiko/titan_audio-ss.mp4
"""
import json
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


def main():
    if len(sys.argv) < 2:
        raise SystemExit("使い方: python tools/check_final.py <mp4>")
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

    print()
    if ng:
        for x in ng:
            print("🔴", x)
        print(f"🔴 通し検品に粗 {len(ng)}件")
        return 1
    print("✓ 通し検品は通った（尺・コマ数・解像度・音声・音ズレ・末尾）")
    print("⚠️ これは試写の代わりではない。**カズヤくんが本番動画を見るまで公開しない。**")
    return 0


if __name__ == "__main__":
    sys.exit(main())
