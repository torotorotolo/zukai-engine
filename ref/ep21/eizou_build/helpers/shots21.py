# -*- coding: utf-8 -*-
"""映像を1秒1コマに切り、ショットの境目を機械で取る（21本目 映像方針）。見る前の当たり付け（鉄則2）。

  python -I shots21.py cut <映像> <出力フォルダ> [scene の閾値=0.30]
      → <出力>/t0000.jpg …（1秒ごと・元の大きさ）・shots.tsv（ショット・始め・終わり・長さ・真ん中の秒）・persec.tsv（秒ごとの数）
  python -I shots21.py pick <出力フォルダ> <最短の秒> → ショットごとの真ん中の秒を「a,b,c」で印字（見本帳の frames に渡す）

persec.tsv の列＝秒・明るさ（0〜255）・彩度（0〜1）・肌色の割合（YCbCr の肌の範囲＝人の寄りの当たり）・灰色の割合（煙の当たり）・
赤橙の割合（火の当たり）・前の秒との差（画素の平均の差＝動き）。どれも当たり付けだけ＝決めるのは絵を見てから。
"""
import csv
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')


def duration(path):
    r = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', path])
    return float(r.stdout.strip())


def cut(video, out, thr=0.30):
    os.makedirs(out, exist_ok=True)
    dur = duration(video)
    # 1秒1コマ（JPEG・元の大きさ）
    r = run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-vf', 'fps=1', '-q:v', '2', os.path.join(out, 't%04d.jpg')])
    if r.returncode != 0:
        raise SystemExit('🔴 ffmpeg（コマ）：' + r.stderr[-500:])
    # ffmpeg の番号は 1 から＝秒に合わせて 0 からに付け直す
    files = sorted(f for f in os.listdir(out) if re.match(r't\d{4}\.jpg$', f))
    for f in files:
        n = int(f[1:5]) - 1
        os.replace(os.path.join(out, f), os.path.join(out, 'x%04d.jpg' % n))
    for f in sorted(os.listdir(out)):
        if re.match(r'x\d{4}\.jpg$', f):
            os.replace(os.path.join(out, f), os.path.join(out, 't' + f[1:]))
    nfr = len([f for f in os.listdir(out) if re.match(r't\d{4}\.jpg$', f)])
    # ショットの境目（scene の点数）
    r = run(['ffmpeg', '-v', 'info', '-i', video, '-vf', "select='gt(scene,%.2f)',showinfo" % thr, '-an', '-f', 'null', '-'])
    cuts = [float(m) for m in re.findall(r'pts_time:([\d.]+)', r.stderr)]
    bounds = [0.0] + [c for c in cuts if 0.5 < c < dur - 0.5] + [dur]
    shots = []
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        if b - a < 0.3:
            continue
        shots.append((len(shots) + 1, a, b, b - a, int((a + b) / 2)))
    with open(os.path.join(out, 'shots.tsv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['shot', 'start', 'end', 'dur', 'mid'])
        for s in shots:
            w.writerow([s[0], '%.2f' % s[1], '%.2f' % s[2], '%.2f' % s[3], s[4]])
    persec(out, nfr)
    print('%s：長さ %.1f秒・コマ %d・ショット %d（閾値 %.2f）' % (os.path.basename(video), dur, nfr, len(shots), thr))
    longs = [s for s in shots if s[3] >= 4]
    print('  4秒以上のショット %d・最長 %.1f秒' % (len(longs), max(s[3] for s in shots)))


def persec(out, n):
    from PIL import Image, ImageChops, ImageStat
    rows, prev = [], None
    for t in range(n):
        p = os.path.join(out, 't%04d.jpg' % t)
        im = Image.open(p).convert('RGB').resize((160, 120))
        hsv = im.convert('HSV')
        ycc = im.convert('YCbCr')
        px = list(im.getdata())
        hs = list(hsv.getdata())
        yc = list(ycc.getdata())
        N = len(px)
        skin = sum(1 for (y, cb, cr) in yc if 77 <= cb <= 127 and 133 <= cr <= 173 and y > 60) / N
        gray = sum(1 for (h, s, v) in hs if s < 30 and 90 < v < 230) / N
        fire = sum(1 for (h, s, v) in hs if (h < 25 or h > 245) and s > 120 and v > 120) / N
        st = ImageStat.Stat(im.convert('L'))
        sat = sum(s for (_, s, _) in hs) / N / 255
        diff = 0.0
        if prev is not None:
            diff = sum(ImageStat.Stat(ImageChops.difference(im, prev)).mean) / 3
        prev = im
        rows.append([t, '%.0f' % st.mean[0], '%.2f' % sat, '%.3f' % skin, '%.3f' % gray, '%.3f' % fire, '%.1f' % diff])
    with open(os.path.join(out, 'persec.tsv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['t', 'luma', 'sat', 'skin', 'gray', 'fire', 'diff'])
        w.writerows(rows)


def pick(out, mn):
    with open(os.path.join(out, 'shots.tsv'), encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    mids = [r['mid'] for r in rows if float(r['dur']) >= mn]
    print(','.join(mids))
    print('（%d ショット）' % len(mids), file=sys.stderr)


def export(dst, pairs):
    """記号=出力フォルダ … の shots.tsv を1つの表（make_list21.py の門番が読む）にまとめる。"""
    with open(dst, 'w', encoding='utf-8', newline='') as f:
        f.write('# 21本目 映像のショットの境目（shots21.py cut＝ffmpeg の scene 0.30 の機械の当たり・export で作る＝手で直さない）\n')
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['film', 'shot', 'start', 'end', 'dur'])
        for pair in pairs:
            code, folder = pair.split('=', 1)
            with open(os.path.join(folder, 'shots.tsv'), encoding='utf-8') as g:
                for r in csv.DictReader(g, delimiter='\t'):
                    w.writerow([code, r['shot'], r['start'], r['end'], r['dur']])
    print('→', dst)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'cut':
        cut(sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 0.30)
    elif cmd == 'pick':
        pick(sys.argv[2], float(sys.argv[3]))
    elif cmd == 'export':
        export(sys.argv[2], sys.argv[3:])
