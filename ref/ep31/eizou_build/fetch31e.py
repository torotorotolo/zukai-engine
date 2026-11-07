# -*- coding: utf-8 -*-
"""31本目 映像方針（2026-11-08・チャット5）：了承②の Commons の写真11点を取る（30本目 fetch30e.py の型・API は使わない）。

  PYTHONIOENCODING=utf-8 python -X utf8 -P ref/ep31/eizou_build/fetch31e.py selftest          URL の組み立て・幅の選び方・権利の照合を照らす（ネットに出ない）
  PYTHONIOENCODING=utf-8 python -X utf8 -P ref/ep31/eizou_build/fetch31e.py commons [記号…]   sources31.psv の get＝commons:… を src/eizou/<記号>.jpg へ
  PYTHONIOENCODING=utf-8 python -X utf8 -P ref/ep31/eizou_build/fetch31e.py gsi [記号…]       地理院タイル（A1〜A3・A6・A7）を src/gsi/tiles/ に揃えて記録（無い分だけ取る）
  PYTHONIOENCODING=utf-8 python -X utf8 -P ref/ep31/eizou_build/fetch31e.py reparse [記号…]   残した頁を読み直して権利・撮影者の表・名前の網を作り直す（ネットに出ない）

作法（記憶 reference-commons-standard-thumbnail-sizes）：
- 🔴 Commons の robots.txt は /w/（api.php）と Special: を拒否＝API を使わない（30本目の fetch30e は API だった）。
  /wiki/File: の頁の HTML から原本の URL・縦横・権利・作者を読む（頁は git の外の src/commons/pages/ に残す）
- 縮小版は標準の大きさだけ。原本の URL から組む＝`…/thumb/<a>/<ab>/<名>/<幅>px-<名>`。画像の幅が頼む幅より大きいときだけ縮小版・ほかは原本
- 組んだ原本の URL が頁の「原本」の URL と同じかを照らす（ファイル名の字の打ち違いはここで止まる）
- HEAD で状態・種類・長さ → 流しながら GET → 長さの照合 → md5 を2回（2秒あけて）→ PIL で縦横を照らす
- 1点ごとに 10秒あける・429 と 5xx は待つ（120秒×回数・回避しない）・1点目の失敗と 400・404 はそこで止める（組み立ての誤りで20分待たない）
- 名乗り（User-Agent）にメールと @ を入れない
- 権利は頁の許諾の札（licensetpl_short）で照らす＝頁の下の「構造化データは CC0」の注記を拾わない（11-08 の P2・P4 の読み違いの型）
記録＝eizou_build/fetch31.tsv（公開リポに入る＝撮影者の名前は書かない）。
撮影者＝git の外の src/credits_private.tsv（頭の行なし・列＝code・file・author・license・date・url・WxH・attr＝30本目と同じ並び＋attr）と
src/names_commons.txt（名前の網＝足すだけ）。🔴 名前は画面に出さない＝字数と「足した／すでに網／団体」だけ出す。
"""
import datetime
import hashlib
import html
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
PSV = os.path.join(HERE, 'sources31.psv')
LOG = os.path.join(HERE, 'fetch31.tsv')
CRED = os.path.join(EP, 'src', 'credits_private.tsv')
NAMES = os.path.join(EP, 'src', 'names_commons.txt')
OUTDIR = os.path.join(EP, 'src', 'eizou')
PAGES = os.path.join(EP, 'src', 'commons', 'pages')
UA = {'User-Agent': 'zukai-engine-research/1.0 (GitHub torotorotolo)'}
WIKI = 'https://commons.wikimedia.org/wiki/File:'
UP = 'https://upload.wikimedia.org/wikipedia/commons/'
STD = (20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840)
GAP = 10
ORGS = ('SDASM',)      # 団体の名＝クレジットに出す名・名前の網には入れない
KEYS = ['code', 'type', 'grp', 'title', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note']
HEADER = '取った日\t記号\t種類\tbytes\tmd5\tmd5（読み直し）\t縦横\tファイル\t出どころ\n'


def md5(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def text(s):
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def under(title):
    return title.strip().replace(' ', '_')


def urls(title, width, orig_w):
    """(原本の URL, 使う URL, 種類)＝幅は標準の大きさだけ・画像の幅が頼む幅より大きいときだけ縮小版"""
    name = under(title)
    h = hashlib.md5(name.encode('utf-8')).hexdigest()
    q = urllib.parse.quote(name, safe='')
    orig = '%s%s/%s/%s' % (UP, h[0], h[:2], q)
    if width and width not in STD:
        raise ValueError('標準でない幅 %d' % width)
    if width and not orig_w:
        raise ValueError('原本の幅が分からないまま縮小版を組もうとした')
    if width and orig_w > width:
        return orig, '%sthumb/%s/%s/%s/%dpx-%s' % (UP, h[0], h[:2], q, width, q), 'commons-%d' % width
    return orig, orig, 'commons-原本'


def norm(s):
    return re.sub(r'[\s\-]', '', s).casefold()


def lic_ok(rights, lic, page):
    if rights.startswith('SDASM'):
        return bool(re.search(r'[Nn]o known copyright restrictions|No restrictions', page))
    return any(norm(x) == norm(rights) for x in lic)


US = '(?:_|&#95;)'


def page_info(pg):
    d = {'orig': '', 'w': 0, 'h': 0}
    m = re.search(r'class="fullMedia".*?href="(https://upload\.wikimedia\.org/wikipedia/commons/[^"]+)".*?\(([\d,]+)\s*(?:×|&#215;|&times;)\s*([\d,]+)\s*pixels', pg, re.S)
    if m:
        # 🔴 11-08：頁の原本の URL の尻に ?utm_source=…&utm_content=original が付く（記憶 reference-commons-standard-thumbnail-sizes の API と同じ型）＝外して照らす
        d.update(orig=html.unescape(m.group(1)).split('?')[0], w=int(m.group(2).replace(',', '')), h=int(m.group(3).replace(',', '')))
    # 🔴 11-08：頁の HTML は印の名前の「_」を `&#95;` で書く（id="fileinfotpl&#95;aut"・class="licensetpl&#95;short"）＝両方に当てる
    m = re.search(r'id="fileinfotpl%saut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>' % US, pg, re.S)
    raw = m.group(1) if m else ''
    links = [text(x) for x in re.findall(r'<a\b[^>]*>(.*?)</a>', raw, re.S)]
    links = [x for x in links if x]
    d['author'] = (links[0] if links else text(raw))[:80]
    d['from'] = bool(links) and ' from ' in text(raw)
    d['lic'] = [text(x) for x in re.findall(r'class="licensetpl%sshort"[^>]*>(.*?)</span>' % US, pg, re.S)]
    d['attr'] = ' / '.join(text(x) for x in re.findall(r'class="licensetpl%sattr"[^>]*>(.*?)</span>' % US, pg, re.S))[:160]
    m = re.search(r'id="fileinfotpl%sdate"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>' % US, pg, re.S)
    d['date'] = text(m.group(1))[:40] if m else ''
    d['vrt'] = bool(re.search(r'ticket\.wikimedia\.org|PermissionTicket|permissionTicket|VRT', pg))
    return d


def fetch(url, method='GET', tries=4):
    """(状態, 応答)＝429 と 5xx は待って取り直す（回避しない）"""
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, method=method, headers=UA), timeout=180)
            return r.status, r
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                print('  待つ %s %d（%d秒）' % (method, e.code, 120 * (i + 1)), flush=True)
                time.sleep(120 * (i + 1))
                continue
            return e.code, None
        except Exception as e:      # noqa: BLE001
            print('  ERR %s %s' % (method, e), flush=True)
            time.sleep(30 * (i + 1))
    return 429, None


def rows():
    out = []
    for ln in open(PSV, encoding='utf-8'):
        if not ln.strip() or ln.startswith('#'):
            continue
        d = dict(zip(KEYS, ln.rstrip('\n').split('|')))
        if d.get('type') == 'commons-photo' and d.get('get', '').startswith('commons:'):
            d['t'] = d['get'][8:].split('（')[0].strip()
            m = re.search(r'幅(\d+)の縮小版', d['get'])
            d['width'] = int(m.group(1)) if m else 0
            out.append(d)
    return out


def log(row):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        if new:
            f.write(HEADER)
        f.write('\t'.join(str(x) for x in row) + '\n')


def commons(only):
    from PIL import Image
    cred = {}
    if os.path.exists(CRED):
        for ln in open(CRED, encoding='utf-8'):
            c = ln.rstrip('\n').split('\t')
            if c and c[0]:
                cred[c[0]] = c
    names = [ln.strip() for ln in open(NAMES, encoding='utf-8') if ln.strip() and not ln.startswith('#')]
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(PAGES, exist_ok=True)
    bad, first = 0, True
    for d in rows():
        code, title = d['code'], d['t']
        if only and code not in only:
            continue
        path = os.path.join(OUTDIR, code + '.jpg')
        if os.path.exists(path) and code in cred:
            print('skip', code, flush=True)
            continue
        purl = WIKI + urllib.parse.quote(under(title), safe='')
        st, r = fetch(purl)
        if st != 200:
            print('🔴 %s 頁が取れない（%s）%s' % (code, st, purl), flush=True)
            bad += 1
            if first or st in (400, 404):
                break
            continue
        pg = r.read().decode('utf-8', 'replace')
        r.close()
        with open(os.path.join(PAGES, code + '.html'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(pg)
        info = page_info(pg)
        if not info['orig']:
            print('🔴 %s 頁に原本の URL と縦横が無い' % code, flush=True)
            bad += 1
            break
        orig, url, kind = urls(title, d['width'], info['w'])
        if urllib.parse.unquote(orig) != urllib.parse.unquote(info['orig']):
            print('🔴 %s 組んだ原本の URL が頁と違う\n  組んだ %s\n  頁　　 %s' % (code, orig, info['orig']), flush=True)
            bad += 1
            break
        okl = lic_ok(d['rights'], info['lic'], pg)
        time.sleep(3)
        st, r = fetch(url, 'HEAD')
        ct, want = '', 0
        if r is not None:
            ct, want = r.headers.get('Content-Type') or '', int(r.headers.get('Content-Length') or 0)
            r.close()
        if st != 200 or not ct.startswith('image/'):
            print('🔴 %s HEAD %s %s %d\n  %s' % (code, st, ct, want, url), flush=True)
            bad += 1
            if first or st in (400, 404):
                break
            continue
        st, r = fetch(url)
        if st != 200:
            print('🔴 %s GET %s' % (code, st), flush=True)
            bad += 1
            continue
        n = 0
        with r, open(path + '.part', 'wb') as f:
            for b in iter(lambda: r.read(1 << 20), b''):
                f.write(b)
                n += len(b)
        if want and n != want:
            print('🔴 %s 大きさが HEAD と違う %d / %d' % (code, n, want), flush=True)
            bad += 1
            continue
        os.replace(path + '.part', path)
        m1 = md5(path)
        time.sleep(2)
        m2 = md5(path)
        with Image.open(path) as im:
            W, H = im.size
        if kind == 'commons-原本':
            okd = (W, H) == (info['w'], info['h'])
        else:
            okd = W == d['width'] and abs(H - round(info['h'] * d['width'] / info['w'])) <= 1
        log([datetime.date.today().isoformat(), code, kind, n, m1, m2, '%dx%d' % (W, H), 'src/eizou/%s.jpg' % code, 'commons:' + title])
        author = info['author']
        nstat = add_name(author, names)
        cred[code] = [code, title, author, d['rights'], info['date'], purl, '%dx%d' % (info['w'], info['h']), info['attr']]
        write_cred(cred)
        okm = m1 == m2
        bad += (not okm) + (not okd) + (not okl)
        print('%s %s %.2fMB 縦横%dx%d（原本%dx%d）%s md5x2%s 権利%s（頁の札:%s） 作者=%d字・%s%s・attr=%s・VRT=%s 日=%s' % (
            code, kind, n / 1e6, W, H, info['w'], info['h'], '縦横✓' if okd else '🔴縦横',
            '✓' if okm else '🔴', '✓' if okl else '🔴', '・'.join(info['lic']) or '無し',
            len(author), nstat, '（from を外した）' if info['from'] else '', 'あり' if info['attr'] else 'なし',
            'あり' if info['vrt'] else 'なし', info['date'][:20]), flush=True)
        first = False
        time.sleep(GAP)
    print('おわり＝失敗 %d' % bad, flush=True)
    return 1 if bad else 0


def add_name(author, names):
    """撮影者を名前の網に足す（画面に名前を出さない＝状態の語だけ返す）"""
    if not author:
        return '🔴 作者の欄が読めない'
    if any(o in author for o in ORGS):
        return '団体（網に入れない）'
    if any(author.casefold() == x.casefold() for x in names):
        return 'すでに網'
    with open(NAMES, 'a', encoding='utf-8', newline='\n') as f:
        f.write(author + '\n')
    names.append(author)
    return '網に足した'


def write_cred(cred):
    with open(CRED, 'w', encoding='utf-8', newline='\n') as f:
        for c in cred.values():
            f.write('\t'.join(str(x).replace('\t', ' ').replace('\n', ' ') for x in c) + '\n')


def reparse(only):
    """取ったあとに頁の読み方を直したとき（11-08＝`&#95;`）：src/commons/pages/<記号>.html を読み直し、権利の照合・credits_private.tsv・names_commons.txt を作り直す（ネットに出ない・写真は取り直さない）"""
    cred = {}
    if os.path.exists(CRED):
        for ln in open(CRED, encoding='utf-8'):
            c = ln.rstrip('\n').split('\t')
            if c and c[0]:
                cred[c[0]] = c
    names = [ln.strip() for ln in open(NAMES, encoding='utf-8') if ln.strip() and not ln.startswith('#')]
    bad = 0
    for d in rows():
        code, title = d['code'], d['t']
        if only and code not in only:
            continue
        p = os.path.join(PAGES, code + '.html')
        if not os.path.exists(p) or not os.path.exists(os.path.join(OUTDIR, code + '.jpg')):
            print('🔴 %s 頁か写真が無い' % code)
            bad += 1
            continue
        pg = open(p, encoding='utf-8').read()
        info = page_info(pg)
        okl = lic_ok(d['rights'], info['lic'], pg)
        author = info['author']
        nstat = add_name(author, names)
        purl = WIKI + urllib.parse.quote(under(title), safe='')
        cred[code] = [code, title, author, d['rights'], info['date'], purl, '%dx%d' % (info['w'], info['h']), info['attr']]
        long_ = len(author) > 40
        bad += (not okl) + (not author) + long_
        print('%s 権利%s（台帳:%s／頁の札:%s） 作者=%d字・%s%s%s・attr=%s・VRT=%s 日=%s' % (
            code, '✓' if okl else '🔴', d['rights'], '・'.join(info['lic']) or '無し', len(author), nstat,
            '（from を外した）' if info['from'] else '', '・🔴 長い＝⑤b で見直す' if long_ else '',
            'あり' if info['attr'] else 'なし', 'あり' if info['vrt'] else 'なし', info['date'][:24]), flush=True)
    write_cred(cred)
    print('おわり＝失敗 %d・網 %d 語' % (bad, len(names)), flush=True)
    return 1 if bad else 0


GSI_TILE = 'https://cyberjapandata.gsi.go.jp/xyz/%s/%d/%d/%d.jpg'
GSI_DIR = os.path.join(EP, 'src', 'gsi', 'tiles')
# 記号＝(層, z, 左の x, 上の y, 辺の枚数)＝sources31.psv の A 行。gazo1＝空中写真 1974〜1978年・seamlessphoto＝最新。
# A1〜A3 は ② で取った分（src/gsi/tiles にある＝取り直さない）・A6・A7 は 11-08 に見た分（無ければ取る・1秒あける）。公的な機関（国土地理院・PDL1.0）＝許可不要
GSI = {'A1': ('gazo1', 14, 14617, 6295, 3), 'A2': ('gazo1', 16, 58435, 24890, 3), 'A3': ('seamlessphoto', 16, 58435, 24890, 3),
       'A6': ('gazo1', 15, 29230, 12439, 3), 'A7': ('gazo1', 15, 29214, 12440, 3)}


def gsi(only):
    """タイルを src/gsi/tiles/<層>/<z>/<x>_<y>.jpg に揃え、記号ごとに1行を fetch31.tsv へ（枚数・欠け・合わせた md5 を2回）。組むのは ⑤b-1（印なし）"""
    from PIL import Image
    bad = 0
    for code, (layer, z, x0, y0, side) in GSI.items():
        if only and code not in only:
            continue
        d = os.path.join(GSI_DIR, layer, str(z))
        os.makedirs(d, exist_ok=True)
        cells = [(x, y) for x in range(x0, x0 + side) for y in range(y0, y0 + side)]
        miss, fetched = [], 0
        for x, y in cells:
            p = os.path.join(d, '%d_%d.jpg' % (x, y))
            if os.path.exists(p):
                continue
            st, r = fetch(GSI_TILE % (layer, z, x, y), tries=2)
            time.sleep(1)
            if st != 200:
                miss.append('%d_%d（%s）' % (x, y, st))
                continue
            data = r.read()
            r.close()
            with open(p + '.part', 'wb') as f:
                f.write(data)
            os.replace(p + '.part', p)
            fetched += 1
        have = [(x, y) for x, y in cells if os.path.exists(os.path.join(d, '%d_%d.jpg' % (x, y)))]

        def digest():
            h, n = hashlib.md5(), 0
            for x, y in have:
                with open(os.path.join(d, '%d_%d.jpg' % (x, y)), 'rb') as f:
                    b = f.read()
                h.update(b)
                n += len(b)
            return h.hexdigest(), n
        m1, total = digest()
        time.sleep(2)
        m2, _ = digest()
        odd = 0
        for x, y in have:
            with Image.open(os.path.join(d, '%d_%d.jpg' % (x, y))) as im:
                odd += im.size != (256, 256)
        where = 'src/gsi/tiles/%s/%d/%d〜%d_%d〜%d.jpg（%d枚%s）' % (layer, z, x0, x0 + side - 1, y0, y0 + side - 1, len(have), '・欠け ' + '・'.join(miss) if miss else '')
        log([datetime.date.today().isoformat(), code, 'gsi-%s-z%d-%dx%d' % (layer, z, side, side), total, m1, m2, '%dx%d' % (256 * side, 256 * side),
             where, 'gsi:https://cyberjapandata.gsi.go.jp/xyz/%s/%d/{x}/{y}.jpg' % (layer, z)])
        bad += (m1 != m2) + odd
        print('%s %s z%d %d枚（今回取った %d・欠け %d）%.2fMB md5x2%s 256でない%d' % (code, layer, z, len(have), fetched, len(miss), total / 1e6, '✓' if m1 == m2 else '🔴', odd), flush=True)
    print('おわり＝失敗 %d' % bad, flush=True)
    return 1 if bad else 0


def selftest():
    ok = []
    R = {d['code']: d for d in rows()}
    ok.append(('commons の行が11', sorted(R) == sorted(['P1', 'P3', 'P5', 'P6', 'P7', 'P10', 'L1', 'L1b', 'L2', 'L3', 'L4'])))
    # 名前の md5 の頭（11-08 にブラウザで 960px を開けた URL の <a>/<ab>）＝台帳のファイル名の字の打ち違いを止める
    exp = {'P10': '1/1a', 'P5': '1/13', 'P6': '5/5d', 'P7': '2/20', 'P3': '7/78', 'L1': '0/0c', 'L2': 'd/db', 'L3': 'e/e9', 'L4': '2/20'}
    for code, ab in exp.items():
        u = urls(R[code]['t'], 960, 99999)[1]
        ok.append(('%s の名前の md5 の頭 %s' % (code, ab), u.startswith(UP + 'thumb/' + ab + '/')))
    seen = {
        'P5': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/F-86F-40_of_JSDF.jpg/960px-F-86F-40_of_JSDF.jpg',
        'P7': 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/JASDF_F-86F%2862-7702%29_right_front_view_at_the_Mitsubishi_Heavy_Industries_Komaki_Minami_factory_May_14%2C_2021.jpg/960px-JASDF_F-86F%2862-7702%29_right_front_view_at_the_Mitsubishi_Heavy_Industries_Komaki_Minami_factory_May_14%2C_2021.jpg',
        'P10': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/North_American_F-86F-40-238_-_F-86F-40-MIT_Sabre_-_Kyokk%C5%8D_%E2%80%98865_-_82-7865%E2%80%99_%2820810093720%29.jpg/960px-North_American_F-86F-40-238_-_F-86F-40-MIT_Sabre_-_Kyokk%C5%8D_%E2%80%98865_-_82-7865%E2%80%99_%2820810093720%29.jpg',
        'P6': 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/North_American_F-86F-40-238_-_F-86F-40-MIT_Sabre_-_Kyokk%C5%8D_%E2%80%98865_-_82-7865%E2%80%99_%2820810093715%29.jpg/960px-North_American_F-86F-40-238_-_F-86F-40-MIT_Sabre_-_Kyokk%C5%8D_%E2%80%98865_-_82-7865%E2%80%99_%2820810093715%29.jpg',
    }
    for code, u0 in seen.items():
        ok.append(('%s の URL が 11-08 に開けた URL と字まで同じ' % code, urls(R[code]['t'], 960, 99999)[1] == u0))
    ok.append(('幅の欄＝P1 1920・P6 3840・P3 原本・L1 1920', (R['P1']['width'], R['P6']['width'], R['P3']['width'], R['L1']['width']) == (1920, 3840, 0, 1920)))
    # 陰の対照
    try:
        urls('x.jpg', 1000, 5000)
        ok.append(('標準でない幅は止まる', False))
    except ValueError:
        ok.append(('標準でない幅は止まる', True))
    ok.append(('画像が小さければ原本', urls('x.jpg', 1920, 1280)[2] == 'commons-原本'))
    ok.append(('同じ幅なら原本', urls('x.jpg', 1920, 1920)[2] == 'commons-原本'))
    ok.append(('大きければ縮小版', urls('x.jpg', 1920, 3828)[2] == 'commons-1920'))
    ok.append(('権利：三つのうち CC BY 2.5 を選べる', lic_ok('CC BY 2.5', ['GFDL', 'CC BY-SA 3.0', 'CC BY 2.5'], '')))
    ok.append(('権利：BY-SA 2.5 を BY 2.5 と取り違えない', not lic_ok('CC BY 2.5', ['CC BY-SA 2.5'], '')))
    ok.append(('権利：頁の下の構造化データの CC0 を拾わない', not lic_ok('CC0', ['GFDL'], 'Structured data on this site is available under the Creative Commons CC0 License')))
    ok.append(('権利：SDASM は「制限は知られていない」の札で', lic_ok('SDASM（著作権の制限は知られていない）', [], 'No known copyright restrictions')))
    pg = ('<div class="fullMedia"><bdi><a href="https://upload.wikimedia.org/wikipedia/commons/1/13/F-86F-40_of_JSDF.jpg?utm_source=commons.wikimedia.org&amp;utm_campaign=index&amp;utm_content=original" class="internal">Original file</a></bdi> '
          '<span class="fileInfo">(1,000 × 780 pixels, file size: 1 KB)</span></div><td id="fileinfotpl_aut" class="x">Author</td>\n<td><a href="https://x">Someone</a> from Somewhere</td>')
    i = page_info(pg)
    ok.append(('頁の読み：原本の URL（? から後ろを外す）・縦横・作者のリンクの字・from', (i['orig'].endswith('/1/13/F-86F-40_of_JSDF.jpg'), i['w'], i['h'], i['author'], i['from']) == (True, 1000, 780, 'Someone', True)))
    ok.append(('組んだ原本の URL が、尻に ? の付いた頁の URL と照らせる', urls(R['P5']['t'], 0, 1000)[0] == i['orig']))
    pg2 = ('<td id="fileinfotpl&#95;aut" class="fileinfo-paramfield" lang="en">Author</td>\n<td><a href="/wiki/User:Q">Q</a></td>'
           '<span class="licensetpl&#95;short" style="display: none">CC BY 3.0</span><span class="licensetpl&#95;attr&#95;req licensetpl&#95;link&#95;req">true</span>'
           '<td id="fileinfotpl&#95;date" class="x">Date</td>\n<td>2014-10-01</td>')
    j = page_info(pg2)
    ok.append(('頁の読み：印の「_」が &#95; でも作者・札・日付が読める（attr_req は attr と取らない）', (j['author'], j['lic'], j['date'], j['attr']) == ('Q', ['CC BY 3.0'], '2014-10-01', '')))
    ok.append(('地理院：A1〜A3・A6・A7 の5つ・3×3', sorted(GSI) == ['A1', 'A2', 'A3', 'A6', 'A7'] and all(v[4] == 3 for v in GSI.values())))
    for name, good in ok:
        print('%s %s' % ('OK' if good else 'NG', name))
    print('selftest %d/%d' % (sum(g for _, g in ok), len(ok)))
    return 0 if all(g for _, g in ok) else 1


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'selftest':
        return selftest()
    if mode == 'commons':
        return commons(set(sys.argv[2:]) or None)
    if mode == 'gsi':
        return gsi(set(sys.argv[2:]) or None)
    if mode == 'reparse':
        return reparse(set(sys.argv[2:]) or None)
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main())
