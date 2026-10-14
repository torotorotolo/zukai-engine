# -*- coding: utf-8 -*-
"""映像を1秒1コマに切り、ショットの境目を機械で取る（22本目 映像方針）。21本目の shots21.py を写し、URL（mp4・HLS）から1回の読みで済む形にした。
見る前の当たり付け（鉄則2）＝決めるのは絵を見てから。

  python -I shots22.py cut <映像のファイルか URL> <出力フォルダ> [scene の閾値=0.30] [コマの最大幅=960]
      → <出力>/t0000.jpg …（1秒ごと・幅は最大960）・shots.tsv（ショット・始め・終わり・長さ・真ん中の秒）・persec.tsv（秒ごとの数）
  python -I shots22.py pick <出力フォルダ> <最短の秒>      → ショットごとの真ん中の秒を「a,b,c」で印字（見本帳の frames に渡す）
  python -I shots22.py export <出力の tsv> 記号=出力フォルダ …  → shots22.tsv（make_list22.py の門番が読む）

🆕 22本目：ffmpeg の split で「1秒1コマ」と「scene の点数」を1回の読みで取る（URL を2回読まない＝HLS の低い画質でも網を2回引かない）。
persec.tsv の列＝秒・明るさ（0〜255）・彩度（0〜1）・肌色の割合（YCbCr の肌の範囲＝人の寄りの当たり）・灰色の割合・赤橙の割合・前の秒との差（動き）。
"""
import csv
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')


def duration(src):
    r = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', src])
    try:
        return float(r.stdout.strip().split('\n')[0])
    except ValueError:
        raise SystemExit('🔴 ffprobe が長さを読めない（読めないなら止める）：%s %s' % (src, r.stderr[-300:]))


def cut(src, out, thr=0.30, maxw=960):
    os.makedirs(out, exist_ok=True)
    dur = duration(src)
    # eq(n,0)＝頭の1コマは必ず通す（境目が1つも無い映像だと null の出力が空で ffmpeg が落ちる＝22本目 ROV・888022 で踏んだ）。0秒は下で捨てる
    fc = ("[0:v]split=2[a][b];[a]fps=1,scale='min(%d,iw)':-2[f];[b]select='eq(n,0)+gt(scene,%.2f)',showinfo[s]" % (maxw, thr))
    r = run(['ffmpeg', '-v', 'info', '-y', '-i', src, '-filter_complex', fc,
             '-map', '[f]', '-q:v', '3', os.path.join(out, 't%04d.jpg'), '-map', '[s]', '-f', 'null', '-'])
    if r.returncode != 0:
        raise SystemExit('🔴 ffmpeg：' + r.stderr[-800:])
    files = sorted(f for f in os.listdir(out) if re.match(r't\d{4}\.jpg$', f))
    for f in files:  # ffmpeg の番号は1から＝秒に合わせて0からに付け直す
        os.replace(os.path.join(out, f), os.path.join(out, 'x%04d.jpg' % (int(f[1:5]) - 1)))
    for f in sorted(os.listdir(out)):
        if re.match(r'x\d{4}\.jpg$', f):
            os.replace(os.path.join(out, f), os.path.join(out, 't' + f[1:]))
    nfr = len([f for f in os.listdir(out) if re.match(r't\d{4}\.jpg$', f)])
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
    print('%s：長さ %.1f秒・コマ %d・ショット %d（閾値 %.2f）' % (src.rsplit('/', 1)[-1][:60], dur, nfr, len(shots), thr))
    if shots:
        print('  4秒以上のショット %d・最長 %.1f秒' % (sum(1 for s in shots if s[3] >= 4), max(s[3] for s in shots)))


def persec(out, n):
    from PIL import Image, ImageChops, ImageStat
    rows, prev = [], None
    for t in range(n):
        im = Image.open(os.path.join(out, 't%04d.jpg' % t)).convert('RGB').resize((160, 90))
        flat = lambda x: list(x.get_flattened_data() if hasattr(x, 'get_flattened_data') else x.getdata())
        hs = flat(im.convert('HSV'))
        yc = flat(im.convert('YCbCr'))
        N = len(hs)
        skin = sum(1 for (y, cb, cr) in yc if 77 <= cb <= 127 and 133 <= cr <= 173 and y > 60) / N
        gray = sum(1 for (h, s, v) in hs if s < 30 and 90 < v < 230) / N
        fire = sum(1 for (h, s, v) in hs if (h < 25 or h > 245) and s > 120 and v > 120) / N
        luma = ImageStat.Stat(im.convert('L')).mean[0]
        sat = sum(s for (_, s, _) in hs) / N / 255
        diff = sum(ImageStat.Stat(ImageChops.difference(im, prev)).mean) / 3 if prev is not None else 0.0
        prev = im
        rows.append([t, '%.0f' % luma, '%.2f' % sat, '%.3f' % skin, '%.3f' % gray, '%.3f' % fire, '%.1f' % diff])
    with open(os.path.join(out, 'persec.tsv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['t', 'luma', 'sat', 'skin', 'gray', 'fire', 'diff'])
        w.writerows(rows)


def sample(src, out, step, maxw=960, t0=0.0, t1=None):
    """長い記者会見など：step 秒おきに1コマだけ取る（-ss の飛び読み＝丸ごとは読まない）。名前は t<秒>.jpg（切り捨て）。"""
    os.makedirs(out, exist_ok=True)
    dur = duration(src)
    t1 = dur - 0.5 if t1 is None else t1
    t, n = t0 + step / 2, 0
    while t < t1:
        dst = os.path.join(out, 't%04d.jpg' % int(t))
        r = run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.2f' % t, '-i', src, '-frames:v', '1',
                 '-vf', "scale='min(%d,iw)':-2" % maxw, '-q:v', '3', dst])
        if r.returncode != 0:
            print('  🔴 %.1f秒のコマが取れない：%s' % (t, r.stderr[-200:]))
        else:
            n += 1
        t += step
    print('%s：長さ %.1f秒・%g秒おきに %d コマ' % (src.rsplit('/', 1)[-1][:60], dur, step, n))


def pick(out, mn):
    with open(os.path.join(out, 'shots.tsv'), encoding='utf-8') as f:
        rows = list(csv.DictReader(f, delimiter='\t'))
    mids = [r['mid'] for r in rows if float(r['dur']) >= mn]
    print(','.join(mids))
    print('（%d ショット）' % len(mids), file=sys.stderr)


def export(dst, pairs):
    with open(dst, 'w', encoding='utf-8', newline='') as f:
        f.write('# 22本目 映像のショットの境目（helpers/shots22.py cut＝ffmpeg の scene の機械の当たり・export で作る＝手で直さない）\n')
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
        cut(sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else 0.30, int(sys.argv[5]) if len(sys.argv) > 5 else 960)
    elif cmd == 'sample':
        sample(sys.argv[2], sys.argv[3], float(sys.argv[4]), int(sys.argv[5]) if len(sys.argv) > 5 else 960,
               float(sys.argv[6]) if len(sys.argv) > 6 else 0.0, float(sys.argv[7]) if len(sys.argv) > 7 else None)
    elif cmd == 'pick':
        pick(sys.argv[2], float(sys.argv[3]))
    elif cmd == 'export':
        export(sys.argv[2], sys.argv[3:])
