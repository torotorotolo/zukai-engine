# -*- coding: utf-8 -*-
"""20本目 映像方針：了承②（2026-10-08）の素材を取る・確かめる（出力＝eizou_build/fetch20.tsv）。

  python -I ref/ep20/eizou_build/fetch20.py photos        # Commons の写真（sources20.tsv の photo）を原本で取る
  python -I ref/ep20/eizou_build/fetch20.py check         # 置き場の全素材の md5 を2回・大きさ・EXIF の日付を測って fetch20.tsv を書く
  python -I ref/ep20/eizou_build/fetch20.py head-media    # 焼くときの media の URL（Commons の 1080p 版）を HEAD で確かめる
  python -I ref/ep20/eizou_build/fetch20.py thumbs O5,O6  # 原本が 429 で取れないときだけ＝標準の縮小版（幅1280・名前に _w1280）

取り方：API で原本の URL を引く → HEAD（200・画像の Content-Type・Content-Length）→ GET を1回（Content-Length と照合）→ 1.5秒あける。
すでに置き場にあって大きさが合えば取らない。道具の名乗りにメールや @ を入れない。手元の網から Commons の原本を区間読みすると 429（2026-10-08）＝丸ごと1回の GET だけにする。
"""
import csv
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
UA = 'zukai-engine-research/1.0 (personal non-commercial research; github torotorotolo)'
API = 'https://commons.wikimedia.org/w/api.php'
OUT = os.path.join(HERE, 'fetch20.tsv')


def read_sources():
    with open(os.path.join(HERE, 'sources20.tsv'), encoding='utf-8') as f:
        lines = [ln for ln in f if not ln.startswith('#') and ln.strip()]
    return list(csv.DictReader(lines, delimiter='\t'))


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def title_of(page):
    return urllib.parse.unquote(page.rsplit('/wiki/', 1)[1]).replace('_', ' ')


def api_url(title, width=None):
    q = {'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url|size|sha1', 'format': 'json', 'formatversion': '2'}
    if width:
        q['iiurlwidth'] = str(width)
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(q), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        p = json.loads(r.read().decode('utf-8'))['query']['pages'][0]
    ii = p['imageinfo'][0]
    if width:
        return ii['thumburl'], None, None
    return ii['url'], ii['size'], ii['sha1']


def thumbs(codes, width=1280):
    """原本が 429 で取れないときだけ：Commons が勧める標準の縮小版（幅1280）で取る。置き場の名前に _w1280 を付けて原本と分ける。"""
    bad = 0
    for s in read_sources():
        if s['code'] not in codes:
            continue
        base, ext = os.path.splitext(os.path.join(REPO, s['file']))
        dst = '%s_w%d%s' % (base, width, ext)
        url, _, _ = api_url(title_of(s['page']), width)
        try:
            data = polite(_get, url)
        except Exception as e:
            print('%s 🔴 縮小版も取れない：%s' % (s['code'], e))
            bad += 1
            continue
        with open(dst, 'wb') as f:
            f.write(data)
        print('%s 縮小版 → %s（%d bytes）' % (s['code'], os.path.relpath(dst, REPO), len(data)), flush=True)
        time.sleep(5)
    return 1 if bad else 0


def polite(fn, *a):
    """429（回数制限）なら90秒待って最大2回だけやり直す（叩き続けると制限が延びる＝2026-10-08 実測）。"""
    import urllib.error
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


def head(url):
    return polite(_head, url)


def _get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def photos():
    bad = 0
    for s in read_sources():
        if s['class'] != 'photo':
            continue
        dst = os.path.join(REPO, s['file'])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        url, size, sha1 = api_url(title_of(s['page']))
        if os.path.exists(dst) and os.path.getsize(dst) == size:
            print('%s 済み（大きさ一致・取らない）' % s['code'])
            continue
        try:
            st, ct, ln = head(url)
        except Exception as e:
            print('%s 🔴 HEAD できない：%s＝あとで回し直す' % (s['code'], e))
            bad += 1
            continue
        print('%s HEAD %d %s %d（API %d）' % (s['code'], st, ct, ln, size), flush=True)
        if st != 200 or not ct.startswith('image/') or ln != size:
            print('  🔴 HEAD が合わない＝取らない')
            bad += 1
            continue
        time.sleep(2)
        try:
            data = polite(_get, url)
        except Exception as e:
            print('  🔴 取れない：%s＝あとで回し直す' % e)
            bad += 1
            continue
        if len(data) != size:
            print('  🔴 長さ %d ≠ %d＝落としかけ' % (len(data), size))
            bad += 1
            continue
        if hashlib.sha1(data).hexdigest() != sha1:
            print('  🔴 sha1 が Commons の値と違う')
            bad += 1
            continue
        with open(dst, 'wb') as f:
            f.write(data)
        print('  → %s（%d bytes・sha1 一致）' % (s['file'], len(data)), flush=True)
        time.sleep(5)
    return 1 if bad else 0


def exif_date(path):
    try:
        from PIL import Image
        im = Image.open(path)
        ex = im.getexif()
        dt = ex.get(36867) or ex.get(306)
        if not dt:
            sub = ex.get_ifd(0x8769)
            dt = sub.get(36867) or sub.get(36868)
        return im.size, (dt or '（EXIF に日付なし）')
    except Exception as e:
        return None, '（読めない：%s）' % e


def check():
    rows = []
    bad = 0
    for s in read_sources():
        p = os.path.join(REPO, s['file'])
        if not os.path.exists(p):
            base, ext = os.path.splitext(p)
            alt = base + '_w1280' + ext
            if os.path.exists(alt):
                print('⚠️ %s は原本が無く縮小版（幅1280）だけ：%s' % (s['code'], os.path.relpath(alt, REPO)))
                p = alt
                s = dict(s, file=os.path.relpath(alt, REPO).replace(os.sep, '/'), page=s['page'] + '（⚠️ 縮小版 幅1280＝原本は手元から 429・⑤b-7 で原本を取り直す）')
            else:
                print('🔴 無い：%s' % s['file'])
                bad += 1
                continue
        a = md5(p)
        time.sleep(1.0)
        b = md5(p)
        ok = a == b
        if not ok:
            bad += 1
        size, date = (None, '—')
        if s['class'] == 'photo':
            size, date = exif_date(p)
        dims = '%dx%d' % size if size else s['dims']
        rows.append([s['code'], s['class'], s['file'], os.path.getsize(p), a, 'md5 2回一致' if ok else '🔴 md5 が2回で違う', dims, date, s['page']])
        print('%s %s %d bytes md5=%s %s %s %s' % (s['code'], s['file'], os.path.getsize(p), a, '一致' if ok else '🔴不一致', dims, date))
    extra = [os.path.join('ref', 'ep20', 'src', 'bouei60', 'bouei60_full_140.m4a')]
    for e in extra:
        p = os.path.join(REPO, e)
        if os.path.exists(p):
            a, b = md5(p), md5(p)
            rows.append(['BV-audio', 'audio', e.replace(os.sep, '/'), os.path.getsize(p), a, 'md5 2回一致' if a == b else '🔴', '—', '—', '語の確かめ用（動画の音は使わない）'])
            print('BV-audio %s %d md5=%s' % (e, os.path.getsize(p), a))
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 20本目 映像方針：了承②（2026-10-08）で取った素材（fetch20.py check の出力＝手で直さない）。置き場は git の外（ref/* は .gitignore）\n')
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['code', 'class', 'file', 'bytes', 'md5', 'md5_check', 'dims', 'exif_date', 'page_or_note'])
        w.writerows(rows)
    print('→', OUT)
    return 1 if bad else 0


def head_media():
    bad = 0
    for s in read_sources():
        if s['class'] != 'film':
            continue
        st, ct, ln = head(s['media'])
        print('%s media HEAD %d %s %.1f MB' % (s['code'], st, ct, ln / 1e6))
        if st != 200 or not ct.startswith('video/') or ln < 1_000_000:
            bad += 1
    return 1 if bad else 0


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'thumbs':
        sys.exit(thumbs(sys.argv[2].split(',')))
    sys.exit({'photos': photos, 'check': check, 'head-media': head_media}[cmd]())
