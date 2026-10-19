# -*- coding: utf-8 -*-
"""17本目 映像方針：素材を取る・確かめる（了承② のあと）。23本目の fetch23.py を写して17本目の形にした（2026-10-19）。

  python ref/ep17/eizou_build/fetch17.py commons [記号,…]   # get=commons:orig（原本・sha1 照合）／commons:3840・commons:1920（標準の縮小版）を API で引いて取る（10秒あける）
  python ref/ep17/eizou_build/fetch17.py stock [記号,…]     # get=stock（Pexels・Pixabay の直リンク）：HEAD → GET 1回 → 長さ → 先頭の印（MP4＝ftyp・JPEG）
  python ref/ep17/eizou_build/fetch17.py v1 <yt-dlp の python -m の前に置く PYTHONPATH>   # 記録映像 V1（YouTube の原本・形式は下の V1_FMT）
  python ref/ep17/eizou_build/fetch17.py credits            # Commons の作者欄・クレジット欄・権利を API から src/credits_private.tsv へ（名前は git の外だけ）
  python ref/ep17/eizou_build/fetch17.py check              # 全素材の大きさ・寸法・md5（取った時の md5 と照らす＝2回目）→ fetch17.tsv（手で直さない）

置き場（sources17.psv の file）は git の外（`ref/` は .gitignore の対象・commit は名指しの道具と記録だけ）。すでに置き場にあって長さが合えば取らない。
落としかけ（.part）は測らない。道具の名乗り（User-Agent）にメールや「@」を入れない。報告書・FAA・判決の PDF は ②で手元にある（取らない）。
🔴 撮影者・投稿者の名前は src/credits_private.tsv（git の外）にだけ書く。
"""
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
UA = 'zukai-engine-research/1.0 (github torotorotolo)'
API = 'https://commons.wikimedia.org/w/api.php'
OUT = os.path.join(HERE, 'fetch17.tsv')
LOG = os.path.join(HERE, 'fetch17_log.tsv')     # 取った時の md5（check が2回目と照らす）
PRIVATE = os.path.join(EP, 'src', 'credits_private.tsv')
MAX_STOCK = 50 * 1000 * 1000    # 1本 50MB まで（了承②）
MAX_STOCK_TOTAL = 800 * 1000 * 1000
V1_URL = 'https://www.youtube.com/watch?v=WQTZQU1VOC4'
V1_FMT = os.environ.get('V1_FMT', '137/399/bv*[height<=1080]')   # 1080p（H.264 を先に・無ければ AV1）
V1_SECTION = os.environ.get('V1_SECTION', '')   # 既定は丸ごと（秒を原本のまま使う＝assign17 の「757〜764秒」）。区間だけにするなら '*12:30-13:15'（秒がずれる）


def read_psv(name):
    rows = [ln.rstrip('\n') for ln in open(os.path.join(HERE, name), encoding='utf-8') if not ln.startswith('#') and ln.strip()]
    head = rows[0].split('|')
    return [dict(zip(head, r.split('|'))) for r in rows[1:]]


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def sha1(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def want(codes):
    return set(codes.split(',')) if codes else None


def log_md5(code, path):
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join([code, os.path.relpath(path, REPO).replace('\\', '/'), str(os.path.getsize(path)), md5(path), time.strftime('%Y-%m-%d %H:%M:%S')]) + '\n')


def polite(fn, *a):
    for k in range(3):
        try:
            return fn(*a)
        except urllib.error.HTTPError as e:
            if e.code != 429 or k == 2:
                raise
            print('  429＝90秒待つ（%d回目）' % (k + 1), flush=True)
            time.sleep(90)


def _head(url):
    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, r.headers.get('Content-Type', ''), int(r.headers.get('Content-Length') or -1)


def _get_to(url, dst):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    n = 0
    with urllib.request.urlopen(req, timeout=300) as r, open(dst, 'wb') as f:
        for chunk in iter(lambda: r.read(1 << 20), b''):
            f.write(chunk)
            n += len(chunk)
    return n


def magic_ok(path, kind):
    with open(path, 'rb') as f:
        h = f.read(12)
    return h[4:8] == b'ftyp' if kind == 'video' else h[:3] == b'\xff\xd8\xff' or h[:8] == b'\x89PNG\r\n\x1a\n'


def fetch_direct(code, url, dst, kind, want_size=None, want_sha1=None, max_len=None):
    """HEAD（200・型・長さ）→ GET を .part へ1回 → 長さ（と sha1）と先頭の印を照合 → 名前を付け替える。"""
    try:
        st, ct, ln = polite(_head, url)
    except Exception as e:
        print('%s 🔴 HEAD できない：%s' % (code, e))
        return False
    print('%s HEAD %d %s %.2fMB' % (code, st, ct, ln / 1e6), flush=True)
    want_ct = 'video/' if kind == 'video' else 'image/'
    octet = ct.startswith(('binary/octet-stream', 'application/octet-stream'))   # Pixabay は動画を octet-stream で返す＝取ったあと先頭の印で見る
    if st != 200 or not (ct.startswith(want_ct) or octet) or ln <= 0 or (want_size and ln != want_size) or (max_len and ln > max_len):
        print('  🔴 HEAD が合わない（型 %s・長さ %d・期待 %s・上限 %s）＝取らない' % (ct, ln, want_size, max_len))
        return False
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    part = dst + '.part'
    time.sleep(2)
    try:
        n = polite(_get_to, url, part)
    except Exception as e:
        print('  🔴 取れない：%s' % e)
        return False
    if n != ln:
        print('  🔴 長さ %d ≠ %d＝落としかけ（.part のまま残す・測らない）' % (n, ln))
        return False
    if want_sha1 and sha1(part) != want_sha1:
        print('  🔴 sha1 が Commons の値と違う（.part のまま残す）')
        return False
    if not magic_ok(part, kind):
        print('  🔴 先頭の印が %s でない＝置かない（.part のまま）' % ('MP4' if kind == 'video' else 'JPEG/PNG'))
        return False
    os.replace(part, dst)
    log_md5(code, dst)
    print('  → %s（%d bytes%s）' % (os.path.relpath(dst, REPO), n, '・sha1 一致' if want_sha1 else ''), flush=True)
    return True


def api_info(title, width=None):
    q = {'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url|size|sha1|extmetadata', 'format': 'json', 'formatversion': '2'}
    if width:
        q['iiurlwidth'] = str(width)
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(q), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        p = json.loads(r.read().decode('utf-8'))['query']['pages'][0]
    return p['imageinfo'][0]


def title_of(s):
    return 'File:' + urllib.parse.unquote(s['page'].split('/wiki/File:', 1)[1]).replace('_', ' ')


def cmd_commons(codes=None):
    sel, bad = want(codes), 0
    for s in read_psv('sources17.psv'):
        if not s['get'].startswith('commons') or (sel and s['code'] not in sel):
            continue
        dst = os.path.join(REPO, s['file'])
        if os.path.exists(dst):
            print('%s 済み' % s['code'])
            continue
        width = int(s['get'].split(':')[1]) if s['get'] in ('commons:3840', 'commons:1920', 'commons:1280', 'commons:960') else 0
        thumb = int(os.environ.get('FETCH_THUMB') or 0)   # 10-19：原本が 429 のときは標準の縮小版で取る（記憶 reference-commons-standard-thumbnail-sizes）
        if thumb and not width:
            w0 = int((s['dims'].split('x') + ['0'])[0]) if s['dims'][:1].isdigit() else 0
            width = max(x for x in (960, 1280, 1920, 3840) if x <= max(w0, 960)) if w0 else thumb
            if w0 and width >= w0:   # 原本より大きい縮小版は無い（API は原本を返す）＝1段下げる
                width = max([x for x in (960, 1280, 1920) if x < w0] or [960])
            print('%s 原本 %s → 標準の縮小版 %d' % (s['code'], s['dims'], width), flush=True)
        try:
            ii = api_info(title_of(s), width or None)
        except Exception as e:
            print('%s 🔴 API が引けない：%s' % (s['code'], e))
            bad += 1
            continue
        if width:
            ok = fetch_direct(s['code'], ii['thumburl'], dst, 'image')
        else:
            ok = fetch_direct(s['code'], ii['url'], dst, 'image', ii['size'], ii['sha1'])
        bad += 0 if ok else 1
        time.sleep(10)
    return 1 if bad else 0


def cmd_stock(codes=None):
    sel, bad = want(codes), 0
    total = sum(os.path.getsize(os.path.join(REPO, s['file'])) for s in read_psv('sources17.psv')
                if s['class'] == 'stock' and s['file'] not in ('', '—') and os.path.exists(os.path.join(REPO, s['file'])))
    for s in read_psv('sources17.psv'):
        if s['class'] != 'stock' or s['get'] != 'stock' or (sel and s['code'] not in sel):
            continue
        dst = os.path.join(REPO, s['file'])
        if os.path.exists(dst):
            print('%s 済み' % s['code'])
            continue
        kind = 'video' if s['file'].endswith('.mp4') else 'image'
        try:
            _, _, ln = polite(_head, s['media'])
        except Exception as e:
            print('%s 🔴 HEAD できない：%s' % (s['code'], e))
            bad += 1
            continue
        if total + max(ln, 0) > MAX_STOCK_TOTAL:
            print('%s 🔴 計 %dMB を超える＝取らない' % (s['code'], MAX_STOCK_TOTAL // 10 ** 6))
            bad += 1
            continue
        if fetch_direct(s['code'], s['media'], dst, kind, max_len=MAX_STOCK):
            total += os.path.getsize(dst)
        else:
            bad += 1
        time.sleep(1.5)
    print('フリー素材 計 %.1fMB' % (total / 1e6))
    return 1 if bad else 0


def cmd_v1(pypath=''):
    """記録映像 V1：yt-dlp で区間だけ（V1_SECTION）を 1080p で落とす。yt-dlp は scratchpad に入れた版を PYTHONPATH で渡す（全体の環境は変えない）。"""
    s = next(x for x in read_psv('sources17.psv') if x['code'] == 'V1')
    dst = os.path.join(REPO, s['file'])
    if os.path.exists(dst):
        print('V1 済み')
        return 0
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    env = dict(os.environ)
    if pypath:
        env['PYTHONPATH'] = pypath
    cmd = [sys.executable, '-m', 'yt_dlp', '--no-playlist', '--js-runtimes', 'node', '-f', V1_FMT, '--user-agent', UA, '-o', dst + '.part.%(ext)s', V1_URL]
    if V1_SECTION:
        cmd[4:4] = ['--download-sections', V1_SECTION, '--force-keyframes-at-cuts']
    print(' '.join(cmd), flush=True)
    r = subprocess.run(cmd, env=env)
    got = [f for f in os.listdir(os.path.dirname(dst)) if f.startswith(os.path.basename(dst) + '.part.') and not f.endswith(('.part', '.ytdl'))]
    if r.returncode != 0 or len(got) != 1:
        print('🔴 V1 が取れない（exit %d・%s）' % (r.returncode, got))
        return 1
    src = os.path.join(os.path.dirname(dst), got[0])
    if not src.endswith('.mp4'):
        print('🔴 V1 の器が mp4 でない（%s）＝置かない' % got[0])
        return 1
    os.replace(src, dst)
    log_md5('V1', dst)
    print('V1 → %s（%d bytes）' % (os.path.relpath(dst, REPO), os.path.getsize(dst)))
    return 0


GSI_BBOX = (35.238, 35.272, 136.905, 136.945)   # 南・北の緯度、西・東の経度＝滑走路34・基地・北門・事故現場（南の端の東北東）を含む
GSI_Z = 17


def _tile_xy(lat, lon, z):
    import math
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
    return x, y


def cmd_gsi():
    """国土地理院の昔の空中写真（地理院タイル gazo4＝1987〜1990年）を z17 で継ぐ → src/gsi/gazo4_nagoya_z17.png と座標の表（.json）。
    404 のタイルは灰で埋めて数を出す。0.3秒あける。出典＝「国土地理院撮影の空中写真（1987〜1990年撮影）」・加工の旨（PDL1.0）。"""
    from PIL import Image
    import io
    s = next(x for x in read_psv('sources17.psv') if x['code'] == 'A87')
    dst = os.path.join(REPO, s['file'])
    if os.path.exists(dst):
        print('A87 済み')
        return 0
    south, north, west, east = GSI_BBOX
    x0, y0 = _tile_xy(north, west, GSI_Z)
    x1, y1 = _tile_xy(south, east, GSI_Z)
    xs, ys = range(int(x0), int(x1) + 1), range(int(y0), int(y1) + 1)
    W, H = len(xs) * 256, len(ys) * 256
    img = Image.new('RGB', (W, H), (128, 128, 128))
    miss = got = 0
    tmpl = s['media']
    for j, ty in enumerate(ys):
        for i, tx in enumerate(xs):
            url = tmpl.replace('{z}', str(GSI_Z)).replace('{x}', str(tx)).replace('{y}', str(ty))
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    data = r.read()
                img.paste(Image.open(io.BytesIO(data)).convert('RGB'), (i * 256, j * 256))
                got += 1
            except urllib.error.HTTPError as e:
                if e.code != 404:
                    print('🔴 %s → %d（止める）' % (url, e.code))
                    return 1
                miss += 1
            time.sleep(0.3)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    img.save(dst + '.part.png')
    os.replace(dst + '.part.png', dst)
    meta = {'layer': 'gazo4', 'years': '1987〜1990', 'z': GSI_Z, 'x_range': [xs[0], xs[-1]], 'y_range': [ys[0], ys[-1]], 'size': [W, H],
            'bbox_req': GSI_BBOX, 'tiles_got': got, 'tiles_404': miss, 'how_to_px': 'px = (タイル座標 − x_range[0]) × 256＝_tile_xy(lat, lon, 17) から引く',
            'credit': s['credit'], 'source_page': s['page']}
    with open(os.path.splitext(dst)[0] + '.json', 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
    log_md5('A87', dst)
    print('A87 → %s（%dx%d・タイル %d 枚・404 %d 枚）' % (os.path.relpath(dst, REPO), W, H, got, miss))
    return 0 if got else 1


def cmd_credits():
    rows = []
    for s in read_psv('sources17.psv'):
        if not s['get'].startswith('commons'):
            continue
        try:
            ii = api_info(title_of(s))
        except Exception as e:
            print('%s 🔴 API：%s' % (s['code'], e))
            continue
        m = ii.get('extmetadata', {})
        g = lambda k: (m.get(k, {}).get('value') or '').replace('\t', ' ').replace('\n', ' ')
        rows.append('\t'.join([s['code'], title_of(s)[5:], g('Artist'), g('Credit'), g('LicenseShortName'), g('DateTimeOriginal'), s['page'], time.strftime('%Y-%m-%d')]))
        time.sleep(2)
    os.makedirs(os.path.dirname(PRIVATE), exist_ok=True)
    with open(PRIVATE, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 17本目 映像方針：Commons の作者欄・クレジット欄（git の外＝公開のリポに置かない）。fetch17.py credits が書く（HTML のまま）\n')
        f.write('code\ttitle\tartist\tcredit\tlicense\tdate\tpage\tchecked\n')
        f.write('\n'.join(rows) + '\n')
    print('credits_private.tsv %d 行（git の外）' % len(rows))
    return 0


def cmd_check():
    from PIL import Image
    first = {}
    if os.path.exists(LOG):
        for ln in open(LOG, encoding='utf-8'):
            v = ln.rstrip('\n').split('\t')
            if len(v) == 5:
                first[v[1]] = v[3]
    rows, miss = [], []
    for s in read_psv('sources17.psv'):
        if s['get'] == 'pending' or s['get'].startswith(('local', 'capture')) or s['file'] in ('', '—'):
            continue
        rel = s['file']
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            miss.append(s['code'])
            continue
        m = md5(p)
        f0 = first.get(rel)
        chk = '🔴 取った時の md5 が無い' if not f0 else ('md5 2回一致' if f0 == m else '🔴 md5 が取った時と違う')
        try:
            im = Image.open(p)
            dims = '%dx%d %s' % (im.size[0], im.size[1], im.mode)
        except Exception:
            out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration', '-of', 'csv=p=0', p],
                                 capture_output=True, text=True).stdout.split()
            dims = '映像 ' + ' '.join(out)
        rows.append([s['code'], rel, str(os.path.getsize(p)), m, chk, dims, s['get']])
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 17本目 映像方針：手元の素材（fetch17.py check の出力＝手で直さない）。置き場は git の外\n')
        f.write('code\tfile\tbytes\tmd5\tmd5_check\tdims\tget\n')
        for r in rows:
            f.write('\t'.join(r) + '\n')
    bad = [r[0] for r in rows if not r[4].startswith('md5 2回一致')]
    print('ある %d・まだ無い %d（%s）・md5 の照合が合わない %d（%s）→ %s' % (len(rows), len(miss), '・'.join(miss), len(bad), '・'.join(bad), OUT))
    return 1 if bad else 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    f = {'commons': cmd_commons, 'stock': cmd_stock, 'v1': cmd_v1, 'gsi': cmd_gsi, 'credits': cmd_credits, 'check': cmd_check}[a[0]]
    sys.exit(f(*a[1:]))
