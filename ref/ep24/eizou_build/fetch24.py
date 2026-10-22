# -*- coding: utf-8 -*-
"""24本目 映像方針：素材を取る・確かめる（了承② 2026-10-22 のあと）。23本目の fetch23.py の形を24本目の素材に合わせた。

  python ref/ep24/eizou_build/fetch24.py commons [記号,…]   # Commons＝原本（sha1 照合）か標準の縮小版（1920・3840）。10秒あける
  python ref/ep24/eizou_build/fetch24.py pages               # 報告書の頁＝手元の PDF から描く（200dpi・USGS の図12は埋め込みの原寸）
  python ref/ep24/eizou_build/fetch24.py stock [id,…]        # Pexels＝動画の頁から 1920×1080 の版の直リンクを探して取る（取れなければ未取得と書く）
  python ref/ep24/eizou_build/fetch24.py check               # 全素材の md5 を2回・大きさ・寸法 → fetch24.tsv（手で直さない）

置き場＝ref/ep24/src/eizou/（git の外）。すでにあって大きさが合えば取らない。落としかけは .part で受けて、大きさを照合してから名前を替える。
先頭の印（JPEG・PNG・MP4）で型を見る（型の札は嘘をつくことがある）。名乗りにメールや @ を入れない。
"""
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
UA = 'zukai-engine/1.0 (ep24 visual plan research)'
OUT = os.path.join(HERE, 'fetch24.tsv')
API_CACHE = os.path.join(HERE, 'api24.json')
GAP = float(os.environ.get('FETCH_GAP', '10'))


def read_sources():
    rows = [ln.rstrip('\n') for ln in open(os.path.join(HERE, 'sources24.psv'), encoding='utf-8') if not ln.startswith('#') and ln.strip()]
    head = rows[0].split('|')
    return [dict(zip(head, r.split('|'))) for r in rows[1:]]


def used_codes():
    import csv
    return {r['code'] for r in csv.DictReader(open(os.path.join(HERE, 'list24.tsv'), encoding='utf-8'), delimiter='\t') if r['code']}


def hash_of(path, algo='md5'):
    h = hashlib.new(algo)
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def magic(path):
    b = open(path, 'rb').read(12)
    if b[:3] == b'\xff\xd8\xff':
        return 'jpeg'
    if b[:4] == b'\x89PNG':
        return 'png'
    if b[4:8] == b'ftyp':
        return 'mp4'
    if b[:4] == b'%PDF':
        return 'pdf'
    return repr(b[:8])


def get(url, out, want_size=None, tries=4):
    part = out + '.part'
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=300) as r:
                total = r.headers.get('Content-Length')
                with open(part, 'wb') as f:
                    while True:
                        b = r.read(1 << 20)
                        if not b:
                            break
                        f.write(b)
            got = os.path.getsize(part)
            if total and int(total) != got:
                raise IOError('大きさが合わない %s≠%s' % (got, total))
            if want_size and int(want_size) != got:
                raise IOError('原本の大きさと合わない %s≠%s' % (got, want_size))
            os.replace(part, out)
            return got
        except urllib.error.HTTPError as e:
            print('  HTTP', e.code, 'retry', i, flush=True)
            time.sleep(60 if e.code == 429 else 10 * (i + 1))
        except Exception as e:
            print('  retry', i, e, flush=True)
            time.sleep(10 * (i + 1))
    raise SystemExit('取れない: %s' % url)


def cmd_commons(only):
    api = json.load(open(API_CACHE, encoding='utf-8'))
    use = used_codes()
    for s in read_sources():
        if s['type'] != 'commons' or s['code'] not in use or (only and s['code'] not in only):
            continue
        out = os.path.join(REPO, s['file'])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        a = api['File:' + s['title']]
        if s['get'].startswith('commons:orig'):
            url, want = a['url'], a['size']
        else:
            # 10-22：幅が3840未満の画像では API の thumburl が原本（thumbnail_unscaled）を指す＝そのまま取ると原本を取って 429 に当たった
            # → 標準の幅の縮小版の URL を原本の URL から組む（…/commons/<a>/<ab>/<名> → …/commons/thumb/<a>/<ab>/<名>/<幅>px-<名>）
            w = s['get'].split(':')[1]
            m = re.match(r'(https://upload\.wikimedia\.org/wikipedia/commons/)([0-9a-f]/[0-9a-f]{2}/)([^?]+)', a['url'])
            url = '%sthumb/%s%s/%spx-%s' % (m.group(1), m.group(2), m.group(3), w, m.group(3)) if m and int(w) < a['w'] else a['url']
            want = None if int(w) < a['w'] else a['size']
        if os.path.exists(out) and (want is None or os.path.getsize(out) == int(want)):
            print('ある', s['code'], os.path.getsize(out), flush=True)
            continue
        n = get(url, out, want)
        kind = magic(out)
        ok = ''
        if want:
            ok = 'sha1 ' + ('一致' if hash_of(out, 'sha1') == a['sha1'] else '🔴不一致')
        print('取った', s['code'], n, kind, ok, flush=True)
        time.sleep(GAP)


def render(pdf, page, out, dpi=200):
    import fitz
    doc = fitz.open(os.path.join(REPO, pdf))
    pg = doc[page - 1]
    imgs = pg.get_images(full=True)
    pix = pg.get_pixmap(dpi=dpi)
    pix.save(out)
    return pix.width, pix.height, len(imgs)


def cmd_pages():
    use = used_codes()
    outdir = os.path.join(REPO, 'ref/ep24/src/eizou/pages')
    os.makedirs(outdir, exist_ok=True)
    for s in read_sources():
        if s['type'] not in ('page', 'local') or s['code'] not in use:
            continue
        path = s['file']
        if path.startswith('http'):
            print('未取得（頁の画像は⑤b で内蔵のブラウザから）', s['code'], path, flush=True)
            continue
        if s['type'] == 'local' and '#' not in path:
            continue  # 手元の USGS の写真＝check で測るだけ
        for k, part in enumerate(path.split('+')):
            pdf, pg = part.split('#')
            suffix = '' if '+' not in path else '_%d' % (k + 1)
            out = os.path.join(outdir, '%s%s.png' % (s['code'], suffix))
            dpi = 300 if s['code'] == 'U4F12' else 200
            w, h, n = render(pdf, int(pg), out, dpi)
            print('描いた', s['code'] + suffix, w, h, '埋め込み画像', n, flush=True)


def cmd_stock(only):
    use = used_codes()
    for s in read_sources():
        if s['type'] != 'stock' or s['code'] not in use:
            continue
        pid = s['code'][1:]
        if only and pid not in only:
            continue
        out = os.path.join(REPO, s['file'])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if os.path.exists(out):
            print('ある', s['code'], os.path.getsize(out), flush=True)
            continue
        pick = []
        try:
            req = urllib.request.Request(s['page'], headers={'User-Agent': UA})
            html = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'replace')
            links = sorted(set(re.findall(r'https://videos\.pexels\.com/video-files/%s/[^"\'\s]+?\.mp4' % pid, html)))
            pick = [u for u in links if '1920_1080' in u] or [u for u in links if 'hd_' in u]
        except Exception as e:
            # 10-22：Pexels の頁は機械の取得に 403＝動画の置き場（CDN）の直リンクの形を HEAD で当てる（1920×1080 の版）
            print('  頁が開けない（%s）＝置き場の直リンクの形を当てる' % e, flush=True)
            for size, fps in [(sz, f) for sz in ('hd_1920_1080', 'uhd_2560_1440', 'uhd_3840_2160') for f in (30, 25, 24, 60, 50)]:
                u = 'https://videos.pexels.com/video-files/%s/%s-%s_%dfps.mp4' % (pid, pid, size, fps)
                try:
                    req = urllib.request.Request(u, method='HEAD', headers={'User-Agent': UA})
                    with urllib.request.urlopen(req, timeout=60) as r:
                        if r.status == 200 and 'video' in r.headers.get('Content-Type', ''):
                            pick = [u]
                            break
                except Exception:
                    pass
                time.sleep(1)
        if not pick:
            print('未取得（1920・2560・3840 の版の直リンクが見つからない）', s['code'], flush=True)
            continue
        n = get(pick[0], out)
        print('取った', s['code'], n, magic(out), pick[0].rsplit('/', 1)[-1], flush=True)
        time.sleep(3)


def cmd_check():
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    use = used_codes()
    rows = []
    for s in read_sources():
        if s['code'] not in use:
            continue
        files = []
        if s['type'] in ('commons', 'stock') or (s['type'] == 'local' and '#' not in s['file']):
            files = [os.path.join(REPO, s['file'])]
        else:
            base = os.path.join(REPO, 'ref/ep24/src/eizou/pages', s['code'])
            files = [base + '.png'] if os.path.exists(base + '.png') else [base + '_1.png', base + '_2.png']
        for f in files:
            if not os.path.exists(f):
                rows.append([s['code'], os.path.relpath(f, REPO).replace('\\', '/'), '', '', '', '', '未取得'])
                continue
            m1, m2 = hash_of(f), hash_of(f)
            dims = ''
            if magic(f) in ('jpeg', 'png'):
                dims = '%dx%d' % Image.open(f).size
            rows.append([s['code'], os.path.relpath(f, REPO).replace('\\', '/'), str(os.path.getsize(f)), dims, magic(f), m1, '一致' if m1 == m2 else '🔴不一致'])
    with open(OUT, 'w', encoding='utf-8', newline='\n') as w:
        w.write('# 生成物（fetch24.py check）＝手で直さない。md5 は2回取って照合\n')
        w.write('\t'.join(['code', 'file', 'bytes', 'dims', 'magic', 'md5', 'twice']) + '\n')
        for r in rows:
            w.write('\t'.join(r) + '\n')
    ok = sum(1 for r in rows if r[6] == '一致')
    miss = [r[0] for r in rows if r[6] == '未取得']
    bad = [r[0] for r in rows if r[6].startswith('🔴')]
    print('md5 2回一致 %d／%d・未取得 %d %s・不一致 %d %s' % (ok, len(rows), len(miss), miss, len(bad), bad))
    return 1 if bad else 0


def main():
    cmd = sys.argv[1]
    only = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None
    if cmd == 'commons':
        cmd_commons(only)
    elif cmd == 'pages':
        cmd_pages()
    elif cmd == 'stock':
        cmd_stock(only)
    elif cmd == 'check':
        return cmd_check()
    return 0


if __name__ == '__main__':
    sys.exit(main())
