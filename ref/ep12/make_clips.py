# -*- coding: utf-8 -*-
"""12本目の動く映像2本の台帳（`ref/ep12/clips.json`）と、映像から抜く静止画を作る（2026-09-23 ⑤b-2）。

`ref/ep11/make_clips.py` の形に合わせた。12本目は**帯に切らず1本まるごと**＝`at` は 0。
  doe      Commons「Castle Bravo Detonation USDE.ogv」1280x720・60fps・59.7秒（米エネルギー省・§105）
  bravo4k  Commons「Castle Bravo 15 megaton detonation, 1954.webm」3840x2160・25fps・56.9秒
           🔴 全コマの左下に透かし（y 0.78〜0.82）＝静止画は**抜く時点で下を切る**（`TOP4K`）。
              動画のほうは `footage.USE` の `zoom=1.33, bias=0` で画面の外へ出す
  （手元のファイル＝`ref/ep12/vid/`・git 管理外。Modal と Actions は `media` の直リンクから読む）

抜くもの
  fb_<カットID>.jpg … `footage.USE` の欄ごとの**ひかえの静止画**（取れなかったとき黙ってこれに落ちる
                     ＝⑥で `✓ 切り出し完了 N/N` を数える → feedback-fetch-failure-falls-back-to-a-still）
  <名>.jpg          … 止め絵（`rate` が 0.4 を下回る欄は動画にせず、止め絵とカメラの型で置く）

    python ref/ep12/make_clips.py            # clips.json・静止画・assets.json／credits.json へ登録
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools"))
VID = HERE / "vid"
TOP4K = 0.78          # 4K の透かしは y 0.78〜0.82（②の `measure_watermark_box.py` の実測 y=1687..1779／2160）

CLIPS = {
    "doe": dict(
        file="ep12/vid/doe.ogv",
        url="https://commons.wikimedia.org/wiki/File:Castle_Bravo_Detonation_USDE.ogv",
        media="https://upload.wikimedia.org/wikipedia/commons/8/82/Castle_Bravo_Detonation_USDE.ogv",
        credit="出典：米エネルギー省（1954年）（記録映像より）",
        src="doe", at=0.0, date="1954-03-01",
        what="射点の小屋・火球・ヤシの影・きのこ雲（0〜56秒。57秒からは英字の題字＝NOGO）"),
    "bravo4k": dict(
        file="ep12/vid/bravo4k.webm",
        url="https://commons.wikimedia.org/wiki/File:Castle_Bravo_15_megaton_detonation,_1954.webm",
        media="https://upload.wikimedia.org/wikipedia/commons/4/40/Castle_Bravo_15_megaton_detonation%2C_1954.webm",
        credit="出典：Wikimedia Commons「Castle Bravo 15 megaton detonation, 1954」（記録映像より）",
        src="commons", at=0.0, date="1954-03-01",
        what="艦から見た水平線の火球（1ショット・左下に透かし＝下を切る。実効はおよそ1280px相当）"),
}

# ひかえの静止画を抜く秒（**真っ白のコマを避けて**、そのカットの中身が分かる秒）
FB_T = {"c101": 9.0, "c501": 15.0, "c607": 31.0, "c506": 44.0, "c608": 50.0,
        "c324": 4.0, "c502": 12.0, "c606": 20.0, "c110": 30.0, "c102": 42.0, "c522": 52.0}

# 止め絵（名前 → (帯, 秒, 何が写るか)）
STILLS = {
    "doe_shotcab_near": ("doe", 1.0, "射点の小屋（近い・色）"),
    "doe_shotcab_far": ("doe", 3.6, "射点の小屋と土手道（遠い・色）"),
    "doe_cloud_cap": ("doe", 54.0, "きのこ雲の頂"),
}


def probe(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height,r_frame_rate,sample_aspect_ratio",
                        "-show_entries", "format=duration", "-of", "json", str(p)],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    s = j["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return dict(w=s["width"], h=s["height"], fps=round(int(num) / int(den), 3),
                sar=s.get("sample_aspect_ratio", "1:1"), sec=round(float(j["format"]["duration"]), 3))


def grab(clip, t, out):
    vf = ["crop=iw:ih*%.2f:0:0" % TOP4K] if clip == "bravo4k" else []
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", str(VID / Path(CLIPS[clip]["file"]).name),
           "-frames:v", "1", "-q:v", "2"] + (["-vf", ",".join(vf)] if vf else []) + [str(out)]
    subprocess.run(cmd, check=True)


def main():
    import footage as FO
    clips = {}
    for k, c in CLIPS.items():
        m = probe(VID / Path(c["file"]).name)
        clips[k] = dict(c, **m, dar="16:9", square_w=m["w"], dispw=m["w"])
        print(f"✓ {k}: {m}")
    (HERE / "clips.json").write_text(json.dumps(clips, ensure_ascii=False, indent=1), encoding="utf-8")

    db_p, cr_p = HERE / "assets.json", HERE / "credits.json"
    db = json.loads(db_p.read_text(encoding="utf-8"))
    cr = json.loads(cr_p.read_text(encoding="utf-8"))
    miss = sorted(set(FO.USE) - set(FB_T))
    if miss:
        raise SystemExit(f"🔴 FB_T に秒が無い欄: {miss}（ひかえの静止画を作れない）")
    todo = [(f"fb_{cid}", FO.USE[cid]["clip"], FB_T[cid], f"{cid} のひかえ") for cid in FO.USE]
    todo += [(n, c, t, w) for n, (c, t, w) in STILLS.items()]
    for name, clip, t, what in todo:
        out = HERE / f"{name}.jpg"
        grab(clip, t, out)
        from PIL import Image
        with Image.open(out) as im:
            w, h = im.size
        db[name] = dict(src="clip", clip=clip, t=t, slot="video", note=what, box=[0, 0, 1, 1],
                        w=w, h=h, md5=hashlib.md5(out.read_bytes()).hexdigest(),
                        lic="Public domain（米国の職務著作）" if clip == "doe" else "Public domain（US not renewed）",
                        author="米エネルギー省" if clip == "doe" else "Wikimedia Commons",
                        year=1954, title=CLIPS[clip]["url"].rsplit(":", 1)[-1],
                        hold=CLIPS[clip]["url"])
        cr[f"ep12/{name}.jpg"] = CLIPS[clip]["credit"] + ("（静止画）" if name.startswith("fb_") else "")
        print(f"✓ {name}.jpg  {w}x{h}  ← {clip} {t}秒")
    db_p.write_text(json.dumps(db, ensure_ascii=False, indent=1), encoding="utf-8")
    cr_p.write_text(json.dumps(cr, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
