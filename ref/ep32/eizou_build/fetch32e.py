# -*- coding: utf-8 -*-
"""32本目 映像方針：了承②（2026-11-10 カズヤくん「推奨どおり」）の Commons の写真と管制の録音を取る。31本目 fetch31e.py の型（頁の HTML から読む＝API を使わない）。

  python -P ref/ep32/eizou_build/fetch32e.py --selftest      道具の対照（網に触れない）
  python -P ref/ep32/eizou_build/fetch32e.py --dry           取る URL を組んで見せるだけ（網に触れない）
  python -P ref/ep32/eizou_build/fetch32e.py [記号 ...]      取る（記号を並べればそれだけ・取ったものは飛ばす）

入力：eizou_build/sources32.psv（type＝commons-photo・commons-audio の行）・git の外の src/look/commons_index.tsv（[n]＝idx → Commons の題）
出力：git の外の src/commons/c32/<記号>.<拡張子>・src/commons/pages32/<記号>.html（頁の控え）・src/credits_private.tsv（作者＝撮影者の名はここだけ）
      リポの eizou_build/fetch32.tsv（取った日・記号・種類・bytes・md5 を2回・縦横・ファイル・出どころ）＝🔴 撮影者の名を書かない
作法（記憶 reference-commons-standard-thumbnail-sizes・feedback-download-size-is-not-completion）：
- 縮小版は標準の幅だけ（3840・1920）。原本の URL から組む＝`…/thumb/<a>/<ab>/<名>/<幅>px-<名>`。画像の幅が頼む幅より大きいときだけ縮小版
- 頁（/wiki/File:＝robots.txt で許可）から原本の URL・縦横・作者・許諾の札（licensetpl_short）・EXIF の撮影日時を読む。原本の URL の尻の `?utm_…` は外して照らす・印の「_」は `&#95;` もある
- HEAD で型と大きさを確かめてから GET。大きさが HEAD と違えば止める。md5 は2回（2秒あけ）・縦横は画像を開いて照らす
- 10秒あけ・429 と 5xx は待って取り直す（回避しない）・名乗り（User-Agent）にメールと @ を入れない
"""
import datetime
import hashlib
import html
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
PSV = os.path.join(HERE, 'sources32.psv')
LOG = os.path.join(HERE, 'fetch32.tsv')
IDX = os.path.join(EP, 'src', 'look', 'commons_index.tsv')
CRED = os.path.join(EP, 'src', 'credits_private.tsv')
NAMES = os.path.join(EP, 'src', 'names_commons.txt')
OUTDIR = os.path.join(EP, 'src', 'commons', 'c32')
PAGES = os.path.join(EP, 'src', 'commons', 'pages32')
UA = {'User-Agent': 'zukai-engine-research/1.0 (GitHub torotorotolo)'}
WIKI = 'https://commons.wikimedia.org/wiki/File:'
UP = 'https://upload.wikimedia.org/wikipedia/commons/'
STD = (20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840)
GAP = 10
AUDIO = {'A1': 'Flight 1549 FAA New York TRACON audio extract.ogg'}
ORG_WORDS = ('Army', 'Corps of Engineers', 'Coast Guard', 'NTSB', 'National Transportation', 'FAA', 'Federal Aviation', 'District', 'Navy', 'Department', 'Police')
KEYS = ['code', 'type', 'grp', 'title', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note']
HEADER = '取った日\t記号\t種類\tbytes\tmd5\tmd5（読み直し）\t縦横\tファイル\t出どころ\tEXIF の撮影日時\n'
US = '(?:_|&#95;)'


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


def lic_ok(rights, lic):
    """sources32 の権利の欄と頁の許諾の札（licensetpl_short）を照らす。PD は「Public domain」の札"""
    if rights.startswith('PD'):
        return any('publicdomain' in norm(x) for x in lic)
    want = rights.split('（')[0].strip()
    return any(norm(x) == norm(want) for x in lic)


def page_info(pg):
    d = {'orig': '', 'w': 0, 'h': 0}
    m = re.search(r'class="fullMedia".*?href="(https://upload\.wikimedia\.org/wikipedia/commons/[^"]+)".*?\(([\d,]+)\s*(?:×|&#215;|&times;)\s*([\d,]+)\s*pixels', pg, re.S)
    if m:
        d.update(orig=html.unescape(m.group(1)).split('?')[0], w=int(m.group(2).replace(',', '')), h=int(m.group(3).replace(',', '')))
    else:
        m = re.search(r'class="fullMedia".*?href="(https://upload\.wikimedia\.org/wikipedia/commons/[^"]+)"', pg, re.S)
        if m:
            d['orig'] = html.unescape(m.group(1)).split('?')[0]
    m = re.search(r'id="fileinfotpl%saut"[^>]*>.*?</td>\s*<td[^>]*>(.*?)</td>' % US, pg, re.S)
    raw = m.group(1) if m else ''
    links = [x for x in (text(y) for y in re.findall(r'<a\b[^>]*>(.*?)</a>', raw, re.S)) if x]
    d['author'] = (links[0] if links else text(raw))[:80]
    d['lic'] = [text(x) for x in re.findall(r'class="licensetpl%sshort"[^>]*>(.*?)</span>' % US, pg, re.S)]
    d['attr'] = ' / '.join(text(x) for x in re.findall(r'class="licensetpl%sattr"[^>]*>(.*?)</span>' % US, pg, re.S))[:160]
    m = re.search(r'class="exif-datetimeoriginal"[^>]*>\s*<th[^>]*>.*?</th>\s*<td[^>]*>(.*?)</td>', pg, re.S)
    d['exif'] = text(m.group(1))[:40] if m else ''
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


def titles():
    out = {}
    if not os.path.exists(IDX):
        return out
    for ln in open(IDX, encoding='utf-8').read().splitlines()[1:]:
        p = ln.split('\t')
        if len(p) >= 2:
            out['C' + p[0]] = p[1].replace('File:', '').strip()
    return out


def rows():
    T = titles()
    out = []
    for ln in open(PSV, encoding='utf-8'):
        if not ln.strip() or ln.startswith('#'):
            continue
        d = dict(zip(KEYS, ln.rstrip('\n').split('|')))
        if d.get('type') == 'commons-photo':
            d['t'] = T.get(d['code'], '')
        elif d.get('type') == 'commons-audio':
            d['t'] = AUDIO.get(d['code'], '')
        else:
            continue
        m = re.match(r'(\d+) の縮小版', d.get('get', ''))
        d['width'] = int(m.group(1)) if m else 0
        out.append(d)
    return out


def log(row):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        if new:
            f.write(HEADER)
        f.write('\t'.join(str(x) for x in row) + '\n')


def is_org(author):
    return any(w.casefold() in author.casefold() for w in ORG_WORDS)


def add_name(author, names):
    """撮影者を名前の網に足す（画面に名前を出さない＝状態の語だけ返す）"""
    if not author:
        return '🔴 作者の欄が読めない'
    if is_org(author):
        return '団体（網に入れない）'
    if any(author.casefold() == x.casefold() for x in names):
        return 'すでに網'
    with open(NAMES, 'a', encoding='utf-8', newline='\n') as f:
        f.write(author + '\n')
    names.append(author)
    return '網に足した'


def load_cred():
    cred = {}
    if os.path.exists(CRED):
        for ln in open(CRED, encoding='utf-8'):
            c = ln.rstrip('\n').split('\t')
            if c and c[0]:
                cred[c[0]] = c
    return cred


def write_cred(cred):
    with open(CRED, 'w', encoding='utf-8', newline='\n') as f:
        for c in cred.values():
            f.write('\t'.join(str(x).replace('\t', ' ').replace('\n', ' ') for x in c) + '\n')


def ext_of(title):
    return os.path.splitext(under(title))[1].lower() or '.bin'


def dry():
    bad = 0
    for d in rows():
        if not d['t']:
            print('🔴 %s 題が引けない（commons_index.tsv）' % d['code'])
            bad += 1
            continue
        wd = re.search(r'([\d,]+)×([\d,]+)', d['dims'] or '')
        ow = int(wd.group(1).replace(',', '')) if wd else 0
        try:
            orig, url, kind = urls(d['t'], d['width'], ow or 1)
        except ValueError as e:
            print('🔴 %s %s' % (d['code'], e))
            bad += 1
            continue
        print('%s %s %s' % (d['code'], kind, url[:150]))
    print('dry おわり＝%d 点・失敗 %d' % (len(rows()), bad))
    return 1 if bad else 0


def run(only):
    from PIL import Image
    cred = load_cred()
    names = [ln.strip() for ln in open(NAMES, encoding='utf-8') if ln.strip() and not ln.startswith('#')] if os.path.exists(NAMES) else []
    os.makedirs(OUTDIR, exist_ok=True)
    os.makedirs(PAGES, exist_ok=True)
    bad, first = 0, True
    for d in rows():
        code, title = d['code'], d['t']
        if only and code not in only:
            continue
        if not title:
            print('🔴 %s 題が引けない' % code, flush=True)
            bad += 1
            continue
        path = os.path.join(OUTDIR, code + ext_of(title))
        if os.path.exists(path) and code in cred:
            print('skip', code, flush=True)
            continue
        purl = WIKI + urllib.parse.quote(under(title), safe='')
        st, r = fetch(purl)
        if st != 200:
            print('🔴 %s 頁が取れない（%s）' % (code, st), flush=True)
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
            print('🔴 %s 頁に原本の URL が無い' % code, flush=True)
            bad += 1
            break
        audio = d['type'] == 'commons-audio'
        orig, url, kind = urls(title, 0 if audio else d['width'], info['w'])
        if urllib.parse.unquote(orig) != urllib.parse.unquote(info['orig']):
            print('🔴 %s 組んだ原本の URL が頁と違う\n  組んだ %s\n  頁　　 %s' % (code, orig, info['orig']), flush=True)
            bad += 1
            break
        okl = lic_ok(d['rights'], info['lic'])
        time.sleep(3)
        st, r = fetch(url, 'HEAD')
        ct, want = '', 0
        if r is not None:
            ct, want = r.headers.get('Content-Type') or '', int(r.headers.get('Content-Length') or 0)
            r.close()
        okct = ct.startswith(('audio/', 'application/ogg', 'video/ogg')) if audio else ct.startswith('image/')
        if st != 200 or not okct:
            print('🔴 %s HEAD %s %s %d' % (code, st, ct, want), flush=True)
            bad += 1
            if first or st in (400, 404):
                break
            continue
        time.sleep(2)
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
        if audio:
            pr = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True)
            try:
                dur = float(pr.stdout.strip())
            except ValueError:
                dur = 0.0
            okd = 185.0 <= dur <= 195.0
            size = '%.1f秒' % dur
        else:
            with Image.open(path) as im:
                W, H = im.size
            if kind == 'commons-原本':
                okd = (W, H) == (info['w'], info['h'])
            else:
                okd = W == d['width'] and abs(H - round(info['h'] * d['width'] / info['w'])) <= 1
            size = '%dx%d' % (W, H)
        log([datetime.date.today().isoformat(), code, kind, n, m1, m2, size, os.path.relpath(path, EP).replace('\\', '/'), 'commons:' + title, info['exif']])
        author = info['author']
        nstat = add_name(author, names)
        cred[code] = [code, title, author, d['rights'], info['exif'], purl, '%dx%d' % (info['w'], info['h']), info['attr'], '・'.join(info['lic'])]
        write_cred(cred)
        okm = m1 == m2
        bad += (not okm) + (not okd) + (not okl)
        print('%s %s %.2fMB %s（原本 %dx%d）%s md5x2%s 権利%s（頁の札:%s） 作者=%d字・%s・EXIF=%s' % (
            code, kind, n / 1e6, size, info['w'], info['h'], '✓' if okd else '🔴縦横か長さ', '✓' if okm else '🔴', '✓' if okl else '🔴',
            '・'.join(info['lic']) or '無し', len(author), nstat, info['exif'] or 'なし'), flush=True)
        first = False
        time.sleep(GAP)
    print('おわり＝失敗 %d' % bad, flush=True)
    return 1 if bad else 0


def selftest():
    ok = []
    o, u, k = urls('Plane and ferry in the Hudson 1.jpg', 3840, 4288)
    ok.append(('縮小版の URL の形', u.startswith(UP + 'thumb/') and '/3840px-Plane_and_ferry_in_the_Hudson_1.jpg' in u and k == 'commons-3840'))
    ok.append(('画像が小さければ原本', urls('x.jpg', 1920, 1289)[2] == 'commons-原本'))
    ok.append(('同じ幅なら原本', urls('x.jpg', 1920, 1920)[2] == 'commons-原本'))
    try:
        urls('x.jpg', 1689, 3000)
        ok.append(('標準でない幅は止める', False))
    except ValueError:
        ok.append(('標準でない幅は止める', True))
    h = hashlib.md5('Flight1549CrashAndRescue.ogv'.encode('utf-8')).hexdigest()
    ok.append(('原本の URL の頭＝名前の md5（VTS の記録 /6/67/ と同じ）', h[:2] == '67'))
    ok.append(('権利 PD ↔ Public domain', lic_ok('PD（PD-USACE）', ['Public domain']) and not lic_ok('PD（PD-USACE）', ['CC BY 2.0'])))
    ok.append(('権利 CC BY 2.0 ↔ 札', lic_ok('CC BY 2.0', ['CC BY 2.0']) and not lic_ok('CC BY 2.0', ['CC BY-SA 2.0'])))
    ok.append(('権利 BY-SA 3.0（GFDL もある）', lic_ok('CC BY-SA 3.0', ['GFDL', 'CC BY-SA 3.0'])))
    ok.append(('権利 CC0', lic_ok('CC0', ['CC0'])))
    pg = ('<div class="fullMedia"><bdi><a href="https://upload.wikimedia.org/wikipedia/commons/a/ab/X.jpg?utm_source=commons.wikimedia.org&amp;utm_content=original" class="internal">'
          'Original file</a></bdi> <span class="fileInfo">(4,288 × 2,848 pixels, file size: 5.44 MB)</span></div>'
          '<td id="fileinfotpl&#95;aut" class="fileinfo-paramfield" lang="en">Author</td>\n<td><a href="/wiki/User:Q">Q</a> from x</td>'
          '<span class="licensetpl&#95;short" style="display: none">CC BY 2.0</span>'
          '<tr class="exif-datetimeoriginal"><th>Date and time of data generation</th><td>13:57, 16 January 2009</td></tr>')
    j = page_info(pg)
    ok.append(('頁の読み：原本の URL（?utm を外す）・縦横・作者・札・EXIF', (j['orig'], j['w'], j['h'], j['author'], j['lic'], j['exif']) ==
               ('https://upload.wikimedia.org/wikipedia/commons/a/ab/X.jpg', 4288, 2848, 'Q', ['CC BY 2.0'], '13:57, 16 January 2009')))
    ok.append(('団体の作者は網に入れない', is_org('U.S. Army Corps of Engineers New York District') and is_org('U.S. Coast Guard') and not is_org('Q')))
    ok.append(('幅の欄の読み（3840・1920・原本）', [int(m.group(1)) if m else 0 for m in (re.match(r'(\d+) の縮小版', g) for g in ('3840 の縮小版（原本 4288）', '1920 の縮小版（原本 2144）', '原本'))] == [3840, 1920, 0]))
    W = {d['code']: d['width'] for d in rows()} if os.path.exists(PSV) else {}
    if W:
        ok.append(('sources32 の幅＝原本 3840 超は 3840・1920 超は 1920（C15・C21・C18・C26・C69）', (W.get('C15'), W.get('C21'), W.get('C18'), W.get('C26'), W.get('C69')) == (3840, 3840, 1920, 0, 1920)))
    bad = 0
    for label, v in ok:
        print(('OK  ' if v else 'NG  ') + label)
        bad += 0 if v else 1
    print('selftest %s' % ('ok' if not bad else 'NG %d' % bad))
    return 1 if bad else 0


def main():
    if '--selftest' in sys.argv:
        return selftest()
    if '--dry' in sys.argv:
        return dry()
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    return run(only)


if __name__ == '__main__':
    sys.exit(main())
