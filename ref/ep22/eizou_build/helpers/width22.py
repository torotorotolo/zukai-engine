# -*- coding: utf-8 -*-
"""映像の「器の札」と「実効の幅」を測る（22本目 映像方針）。器の札（幅×高・SAR・field）は絵について嘘をつく＝コマで測る。

  python -I width22.py probe <映像のファイルか URL>                 → 器の札（ffprobe：幅・高・SAR・fps・コマ数・field_order・音声）
  python -I width22.py measure <映像> <コマ数> <置き場> [始め 終わり]  → コマごとの黒帯の幅と「1280 を超える中身」の比を印字（等間隔）

実効の幅の2つの物差し（記憶 feedback-container-labels-lie-about-the-picture）：
  ① 黒帯＝列ごとの明るさの平均が 18 を超える列の左右の端（コマごと）→ 幅の中央値と「1280 に届いたコマの数」
  ② 引き伸ばし＝横方向の周波数の強さ。幅 W の絵が 1280 より細かい中身を持つかを、帯 f＞1280/(2W) の強さで見る。
     比 R＝（そのコマの帯の強さ）÷（同じコマを幅 960 に落として戻した対照の帯の強さ）。
     🔴 陽性対照＝同じコマを 1280 に落として戻した絵の R（中身が 1280 までしか無い絵の値）。本物の R がこれと同じなら引き伸ばし。
     陰性の目安＝R が対照の数倍以上なら 1280 を超える中身がある。しきい値は置かず、本物と対照の R を並べて読む。
"""
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')


def probe(src):
    r = run(['ffprobe', '-v', 'error', '-show_entries',
             'stream=index,codec_type,codec_name,width,height,sample_aspect_ratio,display_aspect_ratio,r_frame_rate,avg_frame_rate,nb_frames,field_order:format=duration,size,bit_rate',
             '-of', 'json', src])
    try:
        j = json.loads(r.stdout)
    except ValueError:
        raise SystemExit('🔴 ffprobe が読めない（止める）：%s' % r.stderr[-300:])
    out = {'duration': float(j['format'].get('duration', 0) or 0), 'size': int(j['format'].get('size', 0) or 0),
           'bit_rate': int(j['format'].get('bit_rate', 0) or 0)}
    for s in j.get('streams', []):
        if s.get('codec_type') == 'video' and 'video' not in out:
            out['video'] = {k: s.get(k) for k in ('codec_name', 'width', 'height', 'sample_aspect_ratio', 'display_aspect_ratio',
                                                  'r_frame_rate', 'avg_frame_rate', 'nb_frames', 'field_order')}
        if s.get('codec_type') == 'audio':
            out.setdefault('audio', []).append(s.get('codec_name'))
    return out


def grab(src, t, dst):
    r = run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.3f' % t, '-i', src, '-frames:v', '1', dst])
    return r.returncode == 0 and os.path.exists(dst)


def band_energy(gray, f0):
    a = gray.astype(np.float64)
    a = a - a.mean(axis=1, keepdims=True)
    w = np.hanning(a.shape[1])[None, :]
    F = np.abs(np.fft.rfft(a * w, axis=1)) ** 2
    f = np.fft.rfftfreq(a.shape[1])
    return F[:, f > f0].mean()


def roundtrip(im, w2):
    W, H = im.size
    h2 = max(1, round(H * w2 / W))
    return im.resize((w2, h2), Image.LANCZOS).resize((W, H), Image.BICUBIC)


def measure(src, n, outdir, t0=None, t1=None):
    os.makedirs(outdir, exist_ok=True)
    pr = probe(src)
    dur = pr['duration']
    a = t0 if t0 is not None else dur * 0.02
    b = t1 if t1 is not None else dur * 0.98
    ts = [a + (b - a) * (i + 0.5) / n for i in range(n)]
    rows = []
    for i, t in enumerate(ts):
        p = os.path.join(outdir, 'w%02d.png' % i)
        if not grab(src, t, p):
            print('  🔴 コマが取れない %.1f秒' % t)
            continue
        im = Image.open(p).convert('L')
        W, H = im.size
        g = np.asarray(im)
        colmean = g.mean(axis=0)
        cols = np.where(colmean > 18)[0]
        width = int(cols[-1] - cols[0] + 1) if len(cols) else 0
        f0 = 1280 / (2 * W)
        e = band_energy(g, f0)
        e960 = band_energy(np.asarray(roundtrip(im, 960)), f0)
        e1280 = band_energy(np.asarray(roundtrip(im, 1280)), f0)
        rows.append((t, W, H, width, e / max(e960, 1e-9), e1280 / max(e960, 1e-9)))
    if not rows:
        raise SystemExit('🔴 1コマも取れない（止める）')
    widths = [r[3] for r in rows]
    R = [r[4] for r in rows]
    Rc = [r[5] for r in rows]
    W, H = rows[0][1], rows[0][2]
    print('器 %dx%d・SAR %s・%s・コマ %s・field %s・音声 %s・%.1f秒' % (
        W, H, pr['video'].get('sample_aspect_ratio'), pr['video'].get('avg_frame_rate'), pr['video'].get('nb_frames'),
        pr['video'].get('field_order'), pr.get('audio'), dur))
    print('黒帯を除いた幅：中央値 %d・最小 %d・1280 に届いたコマ %d/%d' % (int(np.median(widths)), min(widths), sum(1 for x in widths if x >= 1280), len(widths)))
    print('1280 を超える中身の比 R（本物）：中央値 %.2f・最小 %.2f／陽性対照（1280 に落として戻した絵）：中央値 %.2f' % (
        float(np.median(R)), min(R), float(np.median(Rc))))
    for r in rows:
        print('  %7.1f秒 幅%4d R=%.2f 対照=%.2f' % (r[0], r[3], r[4], r[5]))


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'probe':
        print(json.dumps(probe(sys.argv[2]), ensure_ascii=False))
    elif cmd == 'measure':
        t0 = float(sys.argv[5]) if len(sys.argv) > 5 else None
        t1 = float(sys.argv[6]) if len(sys.argv) > 6 else None
        measure(sys.argv[2], int(sys.argv[3]), sys.argv[4], t0, t1)
