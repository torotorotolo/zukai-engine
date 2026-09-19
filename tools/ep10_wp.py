# -*- coding: utf-8 -*-
"""ep10_wp.py — ソウル市『삼풍백화점 붕괴사고 백서』（1996・761頁）を国家記録院のビューアで読む道具（2026-09-20）。

■ 何をするか
    ビューアが画面に出しているのと同じ頁画像（`archWebViewerStream.do`・1648x2338 の JPEG）を
    **必要な頁だけ**取って、読む形にする。⚠️ コピー防止の回避はしない（このビューアは
    「JPG」「전체인쇄／부분인쇄」を自分で出している＝公開資料）。⚠️ 全761頁は取らない。

■ サブコマンド
    get  <頁の並び>            頁を ref/ep10/src/wp/pNNN.jpg へ（例 1-8,24）
    sheet <頁の並び> <名>       2列×3行・1コマ幅640px のシート（どの頁が目次かを当てる用）
    crop <頁> <左,上,右,下の割合> <名>   頁の一部を原寸で切り出す（本文を読む用）
    half <頁> <上|下>          頁の上半分／下半分を原寸で（本文を読む用）

■ 使い方
    PYTHONIOENCODING=utf-8 PYTHONUTF8=1 python tools/ep10_wp.py get 1-8
"""
import os, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'ref', 'ep10', 'src', 'wp')
VIEW = 'https://theme.archives.go.kr/viewer/common/archWebViewer.do?bsid=200041009845&gubun=search'
BASE = ('https://theme.archives.go.kr/viewer/common/archWebViewerStream.do?filePath='
        'N:/ARCHIVE_FILE/05/M/C11M02772/200041009845/000000000001/000000/')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'


def pages(spec):
    out = []
    for part in str(spec).split(','):
        a, _, b = part.partition('-')
        out += list(range(int(a), int(b) + 1)) if b else [int(a)]
    return out


def path(p):
    return os.path.join(OUT, f'p{p:03d}.jpg')


def get(ps):
    os.makedirs(OUT, exist_ok=True)
    for p in ps:
        fn = path(p)
        if os.path.exists(fn) and os.path.getsize(fn) > 5000:
            continue
        url = f'{BASE}{p:05d}.tif&pageInfo=1'
        for i in range(4):
            try:
                req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': VIEW})
                data = urllib.request.urlopen(req, timeout=120).read()
                if not data.startswith(b'\xff\xd8'):
                    sys.exit(f'{p}頁が JPEG でない（{data[:40]!r}）')  # fail closed
                open(fn, 'wb').write(data)
                break
            except SystemExit:
                raise
            except Exception as e:
                if i == 3:
                    sys.exit(f'{p}頁が取れない: {e}')
                time.sleep(3 * (i + 1))
        time.sleep(0.4)
    from PIL import Image
    for p in ps:
        print(p, Image.open(path(p)).size, os.path.getsize(path(p)))


def sheet(ps, tag):
    from PIL import Image, ImageDraw, ImageFont
    get(ps)
    d = os.path.join(ROOT, 'out', 'ep10_wp')
    os.makedirs(d, exist_ok=True)
    CW, CH, LH = 640, 900, 30
    font = ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 20)
    outs = []
    for s in range(0, len(ps), 6):
        chunk = ps[s:s + 6]
        im0 = Image.new('RGB', (CW * 2 + 12, (CH + LH) * 3 + 8), (30, 30, 30))
        dr = ImageDraw.Draw(im0)
        for k, p in enumerate(chunk):
            im = Image.open(path(p)).convert('RGB')
            sc = min(CW / im.width, CH / im.height)
            im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
            x0, y0 = (k % 2) * (CW + 12), (k // 2) * (CH + LH) + 4
            im0.paste(im, (x0 + (CW - im.width) // 2, y0))
            dr.text((x0 + 6, y0 + CH + 2), f'p{p}', fill=(255, 255, 0), font=font)
        fn = os.path.join(d, f'{tag}_{s // 6 + 1:02d}.jpg')
        im0.save(fn, quality=92)
        outs.append(fn)
    print('\n'.join(outs))


def crop(p, box, tag):
    from PIL import Image
    get([p])
    im = Image.open(path(p)).convert('RGB')
    l, t, r, b = [float(x) for x in box.split(',')]
    im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
    d = os.path.join(ROOT, 'out', 'ep10_wp')
    os.makedirs(d, exist_ok=True)
    fn = os.path.join(d, f'{tag}.jpg')
    im.save(fn, quality=95)
    print(fn, im.size)


if __name__ == '__main__':
    c = sys.argv[1] if len(sys.argv) > 1 else ''
    if c == 'get':
        get(pages(sys.argv[2]))
    elif c == 'sheet':
        sheet(pages(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else 'wp')
    elif c == 'crop':
        crop(int(sys.argv[2]), sys.argv[3], sys.argv[4])
    elif c == 'half':
        crop(int(sys.argv[2]), '0,0,1,0.55' if sys.argv[3] == '上' else '0,0.45,1,1',
             f'p{int(sys.argv[2]):03d}_{sys.argv[3]}')
    else:
        sys.exit(__doc__)
