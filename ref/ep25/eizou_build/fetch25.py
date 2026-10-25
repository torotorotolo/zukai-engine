# -*- coding: utf-8 -*-
"""25本目 映像方針：素材を取る・取り出す（2026-10-25・チャット5）。入力＝eizou_build/sources25.psv の get の欄。

  python ref/ep25/eizou_build/fetch25.py public      公的な機関の素材（報告書の PDF から原画・頁・切り出し／国交省の写真）＝許可不要（10-25）
  python ref/ep25/eizou_build/fetch25.py commons     Commons（了承②のあと）＝標準の縮小版（1920）か原本（幅1920以下）・間をあける
  python ref/ep25/eizou_build/fetch25.py check       取った物の md5 を取り直して記録と比べる（落としかけを測らない＝2回目）
  python ref/ep25/eizou_build/fetch25.py --selftest

get の書き方：raw:<PDF名>:<PDF頁>:<番号>（figcap25.tsv の頁の上の並びの番号の原画＝PDF の上の注記は入らない）／raw:mlit2005/<名>.pdf:<頁>:<大きさの順>
             crop:<PDF名>:<PDF頁>:<番号>（頁を描いて写真の矩形で切る＝注記こみ）／clip:<PDF名>:<PDF頁>:<x0,y0,x1,y1 pt＝見たままの向き>
             page:<PDF名>:<PDF頁>（頁を 200dpi で）／file:<src からの道>（手元の物を写す）／http:<URL>（HEAD→GET→大きさ→md5×2）
             commons:1920｜commons:orig（了承②のあと）／tiles:・google:・stock:＝ここでは取らない（手元にある・⑤b-1・⑤b）
出力＝ref/ep25/src/eizou/（写真）・src/eizou/pages/（頁）＝git の外。記録＝eizou_build/fetch25.tsv（code・how・file・px・bytes・md5・source）。
原画の向き＝頁を描いた絵と4つの向きで比べて差の小さい向き（頁が90度回った付図・国交省の PDF）。名乗り（User-Agent）にメールや @ を入れない。
"""
import hashlib
import io
import os
import shutil
import subprocess
import sys
import time
import urllib.parse

import fitz
from PIL import Image, ImageChops

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
SRC = os.path.join(EP, 'src')
OUT = os.path.join(SRC, 'eizou')
PAGES = os.path.join(OUT, 'pages')
LOG = os.path.join(HERE, 'fetch25.tsv')
FIGCAP = os.path.join(HERE, 'figcap25.tsv')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) research-fetch'
DIRS = {'RA': 'jtsb', 'fu': 'jtsb', 'ik': 'jtsb', 'ke': 'jtsb', 'ha': 'courts'}
PDFS = {'RA2007-3-1_cover': 'jtsb/RA2007-3-1_cover.pdf', 'fu04-finalreport': 'jtsb/fu04-finalreport.pdf',
        'fu04-finalreport-annex-2-2': 'jtsb/fu04-finalreport-annex-2-2.pdf', 'iken20070201-an01-honbun': 'jtsb/iken20070201-an01-honbun.pdf',
        'kengi_170906k': 'jtsb/kengi_170906k.pdf', 'hanrei-pdf-82178': 'courts/hanrei-pdf-82178.pdf', 'hanrei-pdf-86834': 'courts/hanrei-pdf-86834.pdf'}
DPI = 200


def pdf_path(name):
    if name in PDFS:
        return os.path.join(SRC, PDFS[name])
    if name.startswith('mlit2005/'):
        return os.path.join(SRC, name)
    return os.path.join(SRC, 'jtsb', name + '.pdf')


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def read_sources():
    rows = [ln.rstrip('\n') for ln in open(os.path.join(HERE, 'sources25.psv'), encoding='utf-8') if ln.strip() and not ln.startswith('#')]
    head = rows[0].split('|')
    return [dict(zip(head, r.split('|'))) for r in rows[1:]]


def figcap_xref(name, page, no):
    for ln in open(FIGCAP, encoding='utf-8'):
        f = ln.rstrip('\n').split('\t')
        if f[0] == name and f[1] == 'PDF%d' % page and f[2] == str(no):
            return int(f[3]), [float(v) for v in f[5].split(',')]
    raise SystemExit('figcap25.tsv に %s PDF%d #%d が無い' % (name, page, no))


def render(pg, zoom):
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    return Image.open(io.BytesIO(pix.tobytes('png'))).convert('RGB')


def orient(raw, ref):
    """原画を4つの向きで頁を描いた絵（ref）と比べ、差の小さい向きにする"""
    best = None
    for rot in (0, 90, 180, 270):
        r = raw.rotate(rot, expand=True)
        a = r.convert('L').resize((96, max(1, int(96 * r.height / r.width))))
        b = ref.convert('L').resize(a.size)
        d = sum(i * n for i, n in enumerate(ImageChops.difference(a, b).histogram())) / (a.size[0] * a.size[1])
        if best is None or d < best[0]:
            best = (d, rot, r)
    return best[2], best[1]


def do_raw(spec, out):
    parts = spec.split(':')
    name, page, no = parts[1], int(parts[2]), int(parts[3])
    doc = fitz.open(pdf_path(name))
    pg = doc[page - 1]
    if name.startswith('mlit2005/'):
        cands = []
        for im in pg.get_images(full=True):
            info = doc.extract_image(im[0])
            for r in pg.get_image_rects(im[0]):
                cands.append((info['width'] * info['height'], im[0], r * pg.rotation_matrix))
        cands.sort(reverse=True)
        _, xref, rect = cands[no - 1]
    else:
        xref, rect = figcap_xref(name, page, no)
        rect = fitz.Rect(*rect)
    raw = Image.open(io.BytesIO(doc.extract_image(xref)['image']))
    if raw.mode not in ('RGB', 'L'):
        raw = raw.convert('RGB')
    z = 3.0
    ref = render(pg, z).crop((int(rect.x0 * z), int(rect.y0 * z), int(rect.x1 * z), int(rect.y1 * z)))
    img, rot = orient(raw.convert('RGB'), ref)
    img.save(out)
    return 'raw xref%d rot%d' % (xref, rot)


def do_crop(spec, out):
    _, name, page, no = spec.split(':')
    doc = fitz.open(pdf_path(name))
    pg = doc[int(page) - 1]
    xref, rect = figcap_xref(name, int(page), int(no))
    info = doc.extract_image(xref)
    w_pt = rect[2] - rect[0]
    nat_w = max(info['width'], info['height']) if abs((rect[3] - rect[1]) - w_pt) < 1 else info['width']
    z = max(2.0, nat_w / w_pt)
    img = render(pg, z).crop((int(rect[0] * z), int(rect[1] * z), int(rect[2] * z), int(rect[3] * z)))
    img.save(out)
    return 'crop z%.2f' % z


def do_clip(spec, out):
    _, name, page, box = spec.split(':')
    doc = fitz.open(pdf_path(name))
    pg = doc[int(page) - 1]
    x0, y0, x1, y1 = [float(v) for v in box.split(',')]
    z = DPI / 72
    render(pg, z).crop((int(x0 * z), int(y0 * z), int(x1 * z), int(y1 * z))).save(out)
    return 'clip %ddpi' % DPI


def do_page(spec, out):
    parts = spec.split(':')
    name, page = ':'.join(parts[1:-1]), int(parts[-1])
    doc = fitz.open(pdf_path(name))
    render(doc[page - 1], DPI / 72).save(out)
    return 'page %ddpi' % DPI


def do_http(url, out):
    cl = ''
    h = subprocess.run(['curl', '-sI', '-L', '-A', UA, url], capture_output=True, text=True)
    for ln in h.stdout.splitlines():
        if ln.lower().startswith('content-length:'):
            cl = ln.split(':', 1)[1].strip()
    r = subprocess.run(['curl', '-s', '-L', '-A', UA, '-o', out, '-w', '%{http_code}', url], capture_output=True, text=True)
    size = os.path.getsize(out) if os.path.exists(out) else 0
    if r.stdout.strip() != '200' or (cl and int(cl) != size):
        raise SystemExit('取り損ない %s（http %s・HEAD %s・%d バイト）' % (url, r.stdout.strip(), cl, size))
    return 'http %s HEAD=%s' % (r.stdout.strip(), cl or '—')


def commons_url(page_url, how):
    name = urllib.parse.unquote(page_url.split('File:', 1)[1])
    fn = name.replace(' ', '_')
    h = hashlib.md5(fn.encode('utf-8')).hexdigest()
    q = urllib.parse.quote(fn)
    if how == 'commons:orig':
        return 'https://upload.wikimedia.org/wikipedia/commons/%s/%s/%s' % (h[0], h[:2], q)
    return 'https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/1920px-%s' % (h[0], h[:2], q, q)


def target(s):
    ext = '.jpg' if s['get'].startswith(('http:', 'commons:')) or s['file'].endswith('.jpg') else '.png'
    base = os.path.join(PAGES if '/pages/' in s['file'] else OUT, s['code'] + ext)
    return base


def log(rows):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        if new:
            f.write('time\tcode\thow\tfile\tpx\tbytes\tmd5\tsource\n')
        for r in rows:
            f.write('\t'.join(r) + '\n')


def run(kind):
    os.makedirs(PAGES, exist_ok=True)
    rows, ng, want = [], 0, 0
    for s in read_sources():
        g = s['get']
        if kind == 'public' and not g.startswith(('raw:', 'crop:', 'clip:', 'page:', 'file:', 'http:')):
            continue
        if kind == 'commons' and not g.startswith('commons:'):
            continue
        want += 1
        out = target(s)
        try:
            if g.startswith('raw:'):
                how = do_raw(g, out)
            elif g.startswith('crop:'):
                how = do_crop(g, out)
            elif g.startswith('clip:'):
                how = do_clip(g, out)
            elif g.startswith('page:'):
                how = do_page(g, out)
            elif g.startswith('file:'):
                shutil.copyfile(os.path.join(SRC, g[5:]), out)
                how = 'file'
            elif g.startswith('http:'):
                how = do_http(g[5:], out)
                time.sleep(2)
            else:
                url = commons_url(s['page'], g)
                how = do_http(url, out)
                time.sleep(int(os.environ.get('FETCH_GAP', '20')))
        except SystemExit as e:
            print('NG', s['code'], e)
            ng += 1
            continue
        im = Image.open(out)
        m1 = md5(out)
        rows.append([time.strftime('%Y-%m-%d %H:%M:%S'), s['code'], how, os.path.relpath(out, EP).replace('\\', '/'), '%dx%d' % im.size,
                     str(os.path.getsize(out)), m1, g])
        print('OK', s['code'], how, '%dx%d' % im.size)
    log(rows)
    print('取る物 %d・取れた %d・NG %d' % (want, len(rows), ng))
    return 1 if ng or len(rows) != want else 0


def check():
    rows = [ln.rstrip('\n').split('\t') for ln in open(LOG, encoding='utf-8') if not ln.startswith('time\t')]
    now = {s['code'] for s in read_sources()}
    last = {}
    for r in rows:
        if r[1] in now:            # 出どころの表から外した点（使わないと決めた点）は見ない
            last[r[1]] = r
    ok = bad = 0
    for code, r in sorted(last.items()):
        p = os.path.join(EP, r[3])
        m2 = md5(p) if os.path.exists(p) else '（無い）'
        if m2 == r[6]:
            ok += 1
        else:
            bad += 1
            print('✗', code, r[6], m2)
    print('md5 2回目 一致 %d・不一致 %d' % (ok, bad))
    return 1 if bad else 0


def selftest():
    """付図26 の1コマ目の原画（注記なし・455x303）と、2コマ目の切り出し（注記こみ）が取れるか・向きが0か"""
    import tempfile
    t = tempfile.mkdtemp()
    a = os.path.join(t, 'a.png')
    b = os.path.join(t, 'b.png')
    how_a = do_raw('raw:RA07-3-1-5:28:1', a)
    how_b = do_crop('crop:RA07-3-1-5:28:5', b)
    ok = Image.open(a).size == (455, 303) and how_a.endswith('rot0') and Image.open(b).size[0] >= 423
    print('原画', Image.open(a).size, how_a, '／切り出し', Image.open(b).size, how_b, '→', 'selftest OK' if ok else 'selftest ✗')
    return 0 if ok else 1


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        sys.exit(2)
    if a[0] == '--selftest':
        sys.exit(selftest())
    if a[0] == 'check':
        sys.exit(check())
    sys.exit(run(a[0]))
