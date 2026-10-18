# -*- coding: utf-8 -*-
"""23本目 映像方針：素材を取る・確かめる（出力＝eizou_build/fetch23.tsv）。22本目の fetch22.py を写して、写真だけの回の形にした（了承② のあと）。

  python ref/ep23/eizou_build/fetch23.py local [記号,…]     # get=local:960 を手元の Commons 標準の縮小版（ref/ep10/src/commons_640）から写す
  python ref/ep23/eizou_build/fetch23.py commons [記号,…]   # get=commons:orig（原本・sha1 照合）／commons:3840（標準の縮小版）を API で引いて取る（10秒あける）
  python ref/ep23/eizou_build/fetch23.py credits            # Commons の作者欄・クレジット欄を src/credits_private.tsv へ（commons_all.json から・名前は git の外だけ）
  python ref/ep23/eizou_build/fetch23.py check              # 全素材の md5 を2回・大きさ・寸法 → fetch23.tsv（手で直さない）

研究院（sire:1600）と歴史編纂院（hist:form）は頁のフォームの操作＝内蔵ブラウザで取り、置き場（sources23.psv の file）に置いてから check。
すでに置き場にあって大きさが合えば取らない。落としかけ（.part）は測らない。道具の名乗りにメールや @ を入れない。
🔴 撮影者・投稿者の名前は src/credits_private.tsv（git の外）にだけ書く。
"""
import hashlib
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
UA = 'zukai-engine-research/1.0 (personal non-commercial research; github torotorotolo)'
API = 'https://commons.wikimedia.org/w/api.php'
OUT = os.path.join(HERE, 'fetch23.tsv')
PRIVATE = os.path.join(EP, 'src', 'credits_private.tsv')
THUMBS = os.path.join(REPO, 'ref', 'ep10', 'src', 'commons_640')
ALL = os.path.join(REPO, 'ref', 'ep10', 'src', 'commons_all.json')


def read_sources():
    rows = [ln.rstrip('\n') for ln in open(os.path.join(HERE, 'sources23.psv'), encoding='utf-8') if not ln.startswith('#') and ln.strip()]
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


def fetch_direct(code, url, dst, want_size=None, want_sha1=None):
    """HEAD（200・画像・長さ）→ GET を .part へ1回 → 長さ（と sha1）を照合 → 名前を付け替える。"""
    try:
        st, ct, ln = polite(_head, url)
    except Exception as e:
        print('%s 🔴 HEAD できない：%s' % (code, e))
        return False
    print('%s HEAD %d %s %.2fMB' % (code, st, ct, ln / 1e6), flush=True)
    if st != 200 or not ct.startswith('image/') or ln <= 0 or (want_size and ln != want_size):
        print('  🔴 HEAD が合わない（型 %s・長さ %d・期待 %s）＝取らない' % (ct, ln, want_size))
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
    os.replace(part, dst)
    print('  → %s（%d bytes%s）' % (os.path.relpath(dst, REPO), n, '・sha1 一致' if want_sha1 else ''), flush=True)
    return True


def api_info(title, width=None):
    q = {'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url|size|sha1', 'format': 'json', 'formatversion': '2'}
    if width:
        q['iiurlwidth'] = str(width)
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(q), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        p = json.loads(r.read().decode('utf-8'))['query']['pages'][0]
    ii = p['imageinfo'][0]
    if width:
        return ii['thumburl'], None, None, ii['width']
    return ii['url'], ii['size'], ii['sha1'], ii['width']


def title_of(s):
    return 'File:' + urllib.parse.unquote(s['page'].split('/wiki/File:', 1)[1]).replace('_', ' ')


def cmd_local(codes=None):
    sel = want(codes)
    n = 0
    for s in read_sources():
        if s['get'] != 'local:960' or (sel and s['code'] not in sel):
            continue
        no = int(s['code'][1:])
        src = os.path.join(THUMBS, '%03d.jpg' % no)
        dst = os.path.join(REPO, s['file'])
        if os.path.exists(dst) and os.path.getsize(dst) == os.path.getsize(src):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        n += 1
    print('写した %d 点（手元の Commons 標準の縮小版 960px）' % n)
    return 0


def cmd_commons(codes=None):
    sel, bad = want(codes), 0
    for s in read_sources():
        if not s['get'].startswith('commons') or (sel and s['code'] not in sel):
            continue
        dst = os.path.join(REPO, s['file'])
        if os.path.exists(dst):
            print('%s 済み' % s['code'])
            continue
        thumb = int(os.environ.get('FETCH_THUMB') or 0)   # 10-18：原本が 429 のときは標準の縮小版（1280 など）で取る＝置き場の名に _<幅> を足す
        if thumb and s['get'] == 'commons:orig':
            dst = dst.replace('.jpg', '_%d.jpg' % thumb)
            if os.path.exists(dst):
                print('%s 済み（%d）' % (s['code'], thumb))
                continue
        try:
            if s['get'] == 'commons:3840':
                url, size, sh, _ = api_info(title_of(s), 3840)
            elif thumb:
                url, size, sh, _ = api_info(title_of(s), thumb)
            else:
                url, size, sh, _ = api_info(title_of(s))
        except Exception as e:
            print('%s 🔴 API が引けない：%s' % (s['code'], e))
            bad += 1
            continue
        if not fetch_direct(s['code'], url, dst, size, sh):
            bad += 1
        time.sleep(10)
    return 1 if bad else 0


MAX_STOCK = 50 * 1000 * 1000   # 了承②（10-18）＝1本 50MB まで・計 600MB まで


def read_cand():
    rows = [ln.rstrip('\n') for ln in open(os.path.join(HERE, 'stock23_cand.psv'), encoding='utf-8') if not ln.startswith('#') and ln.strip()]
    head = rows[0].split('|')
    return [dict(zip(head, r.split('|'))) for r in rows[1:]]


def cmd_stock(codes=None):
    """フリー素材の候補を取る：HEAD（200・型・長さ ≤ 50MB）→ GET 1回 → 長さを照合（置き場＝ref/ep23/src/stock/<cand>.mp4|jpg）。"""
    sel, bad, total = want(codes), 0, 0
    for c in read_cand():
        if sel and c['cand'] not in sel:
            continue
        ext = '.mp4' if c['kind'] == 'video' else '.jpg'
        dst = os.path.join(EP, 'src', 'stock', c['cand'] + ext)
        if os.path.exists(dst):
            total += os.path.getsize(dst)
            print('%s 済み' % c['cand'])
            continue
        try:
            st, ct, ln = polite(_head, c['media'])
        except Exception as e:
            print('%s 🔴 HEAD できない：%s' % (c['cand'], e))
            bad += 1
            continue
        want_ct = 'video/' if c['kind'] == 'video' else 'image/'
        octet = ct.startswith(('binary/octet-stream', 'application/octet-stream'))   # 10-18：Pixabay は動画を octet-stream で返す＝取ったあと先頭の印で見る
        if st != 200 or not (ct.startswith(want_ct) or octet) or ln <= 0 or ln > MAX_STOCK:
            print('%s 🔴 HEAD が合わない（%d・%s・%d bytes）＝取らない' % (c['cand'], st, ct, ln))
            bad += 1
            continue
        if total + ln > 12 * MAX_STOCK:
            print('%s 🔴 計 600MB を超える＝取らない' % c['cand'])
            bad += 1
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        part = dst + '.part'
        try:
            n = polite(_get_to, c['media'], part)
        except Exception as e:
            print('%s 🔴 取れない：%s' % (c['cand'], e))
            bad += 1
            continue
        if n != ln:
            print('%s 🔴 長さ %d ≠ %d＝落としかけ（.part のまま）' % (c['cand'], n, ln))
            bad += 1
            continue
        with open(part, 'rb') as f:
            head12 = f.read(12)
        ok_magic = head12[4:8] == b'ftyp' if c['kind'] == 'video' else head12[:3] == b'\xff\xd8\xff'
        if not ok_magic:
            print('%s 🔴 先頭の印が %s でない（%r）＝置かない' % (c['cand'], 'MP4' if c['kind'] == 'video' else 'JPEG', head12))
            bad += 1
            continue
        os.replace(part, dst)
        total += n
        print('%s → %s（%.1fMB）' % (c['cand'], os.path.relpath(dst, REPO), n / 1e6), flush=True)
        time.sleep(1.5)
    print('フリー素材の候補 計 %.1fMB' % (total / 1e6))
    return 1 if bad else 0


def cmd_credits():
    d = json.load(open(ALL, encoding='utf-8'))
    by_title = {r['title']: r for r in d['files']}
    os.makedirs(os.path.dirname(PRIVATE), exist_ok=True)
    rows = []
    for s in read_sources():
        if not s['code'].startswith('C'):
            continue
        t = title_of(s)[5:]
        r = by_title.get(t)
        if r:
            rows.append('\t'.join([s['code'], t, r['artist'], r['credit'], r['lic'], s['page']]))
    with open(PRIVATE, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 23本目 映像方針：Commons の作者欄・クレジット欄（git の外＝公開のリポに置かない）。fetch23.py credits が書く\n')
        f.write('code\ttitle\tartist\tcredit\tlicense\tpage\n')
        f.write('\n'.join(rows) + '\n')
    print('credits_private.tsv %d 行（git の外）' % len(rows))
    return 0


def cmd_check():
    from PIL import Image
    rows, miss = [], []
    for s in read_sources():
        if not s['file']:
            continue
        p = os.path.join(REPO, s['file'])
        if not os.path.exists(p):
            miss.append(s['code'])
            continue
        a, b = md5(p), md5(p)
        try:
            im = Image.open(p)
            dims = '%dx%d %s' % (im.size[0], im.size[1], im.mode)
        except Exception:
            dims = '（画像でない）'
        rows.append([s['code'], s['file'], str(os.path.getsize(p)), a, 'md5 2回一致' if a == b else '🔴 md5 が2回で違う', dims, s['get']])
    for c in read_cand():
        ext = '.mp4' if c['kind'] == 'video' else '.jpg'
        rel = 'ref/ep23/src/stock/%s%s' % (c['cand'], ext)
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            miss.append(c['cand'])
            continue
        a, b = md5(p), md5(p)
        if ext == '.jpg':
            from PIL import Image
            im = Image.open(p)
            dims = '%dx%d %s' % (im.size[0], im.size[1], im.mode)
        else:
            dims = '映像'
        rows.append([c['cand'], rel, str(os.path.getsize(p)), a, 'md5 2回一致' if a == b else '🔴 md5 が2回で違う', dims, 'stock（候補）'])
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 23本目 映像方針：手元の素材（fetch23.py check の出力＝手で直さない）。置き場は git の外\n')
        f.write('code\tfile\tbytes\tmd5\tmd5_check\tdims\tget\n')
        for r in rows:
            f.write('\t'.join(r) + '\n')
    print('ある %d・まだ無い %d（%s）→ %s' % (len(rows), len(miss), '・'.join(miss), OUT))
    return 0


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    f = {'local': cmd_local, 'commons': cmd_commons, 'stock': cmd_stock, 'credits': cmd_credits, 'check': cmd_check}[a[0]]
    sys.exit(f(*a[1:]))
