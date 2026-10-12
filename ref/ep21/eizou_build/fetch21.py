# -*- coding: utf-8 -*-
"""21本目 映像方針：素材を取る・確かめる（出力＝eizou_build/fetch21.tsv）。20本目の fetch20.py を写して、映像の直の URL と YouTube を足した。

  python -I ref/ep21/eizou_build/fetch21.py films [記号,記号]   # sources21.tsv の film（media が直の URL）を HEAD → GET（丸ごと1回）
  python -I ref/ep21/eizou_build/fetch21.py yt 記号 <yt-dlp の道>  # media が YouTube の film を yt-dlp で（720p 以下の mp4）
  python -I ref/ep21/eizou_build/fetch21.py photos [記号,記号]  # photo を原本で（Commons は API → HEAD → GET → sha1 照合／ほかは HEAD → GET）
  python -I ref/ep21/eizou_build/fetch21.py check               # 置き場の全素材の md5 を2回・大きさ・EXIF の日付・映像の長さを測って fetch21.tsv を書く
  python -I ref/ep21/eizou_build/fetch21.py head-media          # 焼くときに引く media の URL を全部 HEAD で確かめる（取れない映像は黙って静止画に落ちる＝先に確かめる）

すでに置き場にあって大きさが合えば取らない。落としかけ（.part）は測らない。道具の名乗りにメールや @ を入れない。
Commons は原本の GET が続くと 429＝90秒待って最大2回だけやり直す・区間読みはしない（20本目の実測）。
🆕 21本目（2026-10-12）：原本を数点取ると 429 が10分続き、返事に「標準の大きさの縮小版を使え」（https://w.wiki/GHai）＝
  FETCH_THUMB=1 で 3840／1920px の縮小版（それより小さい原本だけ原本）・FETCH_GAP＝1点ごとの間隔の秒（既定30）。
  例：FETCH_THUMB=1 FETCH_GAP=10 python -I ref/ep21/eizou_build/fetch21.py photos
"""
import csv
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
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
UA = 'zukai-engine-research/1.0 (personal non-commercial research; github torotorotolo)'
API = 'https://commons.wikimedia.org/w/api.php'
OUT = os.path.join(HERE, 'fetch21.tsv')


def read_sources():
    with open(os.path.join(HERE, 'sources21.tsv'), encoding='utf-8') as f:
        lines = [ln for ln in f if not ln.startswith('#') and ln.strip()]
    return list(csv.DictReader(lines, delimiter='\t'))


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def polite(fn, *a):
    """429（回数制限）なら90秒待って最大2回だけやり直す。"""
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


def _get_to(url, dst):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    n = 0
    with urllib.request.urlopen(req, timeout=300) as r, open(dst, 'wb') as f:
        for chunk in iter(lambda: r.read(1 << 20), b''):
            f.write(chunk)
            n += len(chunk)
    return n


def title_of(page):
    return urllib.parse.unquote(page.rsplit('/wiki/', 1)[1]).replace('_', ' ')


META = os.path.join(os.path.dirname(HERE), 'src', 'fetch21_meta.tsv')  # git の外（撮影者の名前が名前の網に当たる＝公開のリポに置かない）


def api_info(title, width=None):
    """原本（url・長さ・sha1）か、width を渡せば幅 width の JPEG（thumburl・長さと sha1 は無し）。頁の作者と許諾を META に写す。"""
    q = {'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url|size|sha1|extmetadata',
         'iiextmetadatafilter': 'Artist|LicenseShortName|Credit|DateTimeOriginal|UsageTerms', 'format': 'json', 'formatversion': '2'}
    if width:
        q['iiurlwidth'] = str(width)
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(q), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        p = json.loads(r.read().decode('utf-8'))['query']['pages'][0]
    ii = p['imageinfo'][0]
    em = ii.get('extmetadata', {})
    import re as _re
    g = lambda k: _re.sub(r'\s+', ' ', _re.sub(r'<[^>]+>', '', em.get(k, {}).get('value') or '')).strip()[:200]
    new = not os.path.exists(META)
    with open(META, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        if new:
            f.write('# 21本目 映像方針：Commons の頁の作者・許諾・撮影日（fetch21.py photos が取るたびに足す＝手で直さない）\n')
            w.writerow(['title', 'width', 'height', 'artist', 'license', 'usage', 'date', 'credit'])
        w.writerow([p['title'], ii.get('width'), ii.get('height'), g('Artist'), g('LicenseShortName'), g('UsageTerms'), g('DateTimeOriginal'), g('Credit')])
    if width:
        return ii['thumburl'], None, None
    return ii['url'], ii['size'], ii['sha1']


def api_width(title):
    q = {'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'size', 'format': 'json', 'formatversion': '2'}
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(q), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return int(json.loads(r.read().decode('utf-8'))['query']['pages'][0]['imageinfo'][0]['width'])


def fetch_direct(code, url, dst, kinds, want_size=None, want_sha1=None):
    """HEAD（200・型・長さ）→ GET を .part へ1回 → 長さ（と sha1）を照合 → 名前を付け替える。"""
    try:
        st, ct, ln = head(url)
    except Exception as e:
        print('%s 🔴 HEAD できない：%s' % (code, e))
        return False
    print('%s HEAD %d %s %.1fMB' % (code, st, ct, ln / 1e6), flush=True)
    if st != 200 or not any(ct.startswith(k) for k in kinds) or ln <= 0 or (want_size and ln != want_size):
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
    if want_sha1:
        h = hashlib.sha1()
        with open(part, 'rb') as f:
            for chunk in iter(lambda: f.read(1 << 20), b''):
                h.update(chunk)
        if h.hexdigest() != want_sha1:
            print('  🔴 sha1 が Commons の値と違う（.part のまま残す）')
            return False
    os.replace(part, dst)
    print('  → %s（%d bytes%s）' % (os.path.relpath(dst, REPO), n, '・sha1 一致' if want_sha1 else ''), flush=True)
    return True


def want(codes):
    return set(codes.split(',')) if codes else None


def films(codes=None):
    bad = 0
    sel = want(codes)
    for s in read_sources():
        if s['class'] != 'film' or (sel and s['code'] not in sel) or 'youtube.com' in s['media']:
            continue
        dst = os.path.join(REPO, s['file'])
        if os.path.exists(dst):
            print('%s 済み（置き場にある・取らない）' % s['code'])
            continue
        ok = fetch_direct(s['code'], s['media'], dst, ('video/', 'application/ogg', 'application/octet-stream', 'binary/octet-stream'))
        bad += 0 if ok else 1
        time.sleep(5)
    return 1 if bad else 0


def yt(code, ytdlp):
    s = {r['code']: r for r in read_sources()}[code]
    dst = os.path.join(REPO, s['file'])
    if os.path.exists(dst):
        print('%s 済み' % code)
        return 0
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    args = [sys.executable, ytdlp] if ytdlp.endswith('.py') else [ytdlp]
    r = subprocess.run(args + ['--no-playlist', '--user-agent', UA, '-f', 'bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]',
                               '--merge-output-format', 'mp4', '-o', dst, s['media']], capture_output=True, text=True, encoding='utf-8', errors='replace')
    print(r.stdout[-1500:])
    if r.returncode != 0 or not os.path.exists(dst):
        print('🔴 yt-dlp 失敗：', r.stderr[-1500:])
        return 1
    return 0


def photos(codes=None):
    bad = 0
    sel = want(codes)
    for s in read_sources():
        if s['class'] != 'photo' or (sel and s['code'] not in sel):
            continue
        dst = os.path.join(REPO, s['file'])
        if 'commons.wikimedia.org/wiki/' in s['page']:
            width = int(s['media'].split(':', 1)[1]) if s['media'].startswith('thumb:') else None
            # 🆕 21本目：原本の GET は数点で 429＝Wikimedia の返事「標準の大きさの縮小版を使え」（https://w.wiki/GHai＝
            #   20・40・60・120・250・330・500・960・1280・1920・3840px。ほかの幅をじかに取ると断られる）。
            #   FETCH_THUMB=1 なら：原本の幅が3840超→3840／1920超→1920／それ以下→原本（sha1 照合）
            if not width and os.environ.get('FETCH_THUMB') and not os.path.exists(dst):
                try:
                    w0 = api_width(title_of(s['page']))
                except Exception as e:
                    print('%s 🔴 API が引けない：%s' % (s['code'], e))
                    bad += 1
                    continue
                width = 3840 if w0 > 3840 else (1920 if w0 > 1920 else None)
            if width and os.path.exists(dst):
                print('%s 済み（幅%d の JPEG・取らない）' % (s['code'], width))
                continue
            try:
                url, size, sha1 = api_info(title_of(s['page']), width)
            except Exception as e:
                print('%s 🔴 API が引けない：%s' % (s['code'], e))
                bad += 1
                continue
            if size and os.path.exists(dst) and os.path.getsize(dst) == size:
                print('%s 済み（大きさ一致・取らない）' % s['code'])
                continue
            ok = fetch_direct(s['code'], url, dst, ('image/',), size, sha1)
        else:
            if os.path.exists(dst):
                print('%s 済み' % s['code'])
                continue
            ok = fetch_direct(s['code'], s['media'], dst, ('image/',))
        bad += 0 if ok else 1
        # 🆕 21本目：Commons の原本は5秒あけでもほぼ毎回 429（90秒待ち）＝間隔を FETCH_GAP 秒（既定30）に広げる
        time.sleep(float(os.environ.get('FETCH_GAP', '30')))
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


def probe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration',
                        '-of', 'json', path], capture_output=True, text=True, encoding='utf-8', errors='replace')
    try:
        j = json.loads(r.stdout)
        st = j['streams'][0]
        return '%dx%d' % (st['width'], st['height']), '%.1f' % float(j['format']['duration'])
    except Exception:
        return '?', '?'


def check():
    rows, bad = [], 0
    for s in read_sources():
        if s['class'] not in ('film', 'photo'):
            continue
        p = os.path.join(REPO, s['file'])
        if not os.path.exists(p):
            print('— 無い（まだ取っていない）：%s %s' % (s['code'], s['file']))
            continue
        a = md5(p)
        time.sleep(1.0)
        b = md5(p)
        ok = a == b
        bad += 0 if ok else 1
        if s['class'] == 'photo':
            size, date = exif_date(p)
            dims, dur = ('%dx%d' % size if size else s['dims']), '—'
        else:
            dims, dur = probe(p)
            date = '—'
        rows.append([s['code'], s['class'], s['file'], os.path.getsize(p), a, 'md5 2回一致' if ok else '🔴 md5 が2回で違う', dims, dur, date, s['page']])
        print('%s %s %d bytes md5=%s %s %s %s %s' % (s['code'], s['file'], os.path.getsize(p), a, '一致' if ok else '🔴不一致', dims, dur, date))
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 21本目 映像方針：取った素材（fetch21.py check の出力＝手で直さない）。置き場は git の外（ref/* は .gitignore）\n')
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['code', 'class', 'file', 'bytes', 'md5', 'md5_check', 'dims', 'dur', 'exif_date', 'page'])
        w.writerows(rows)
    print('→', OUT, '（%d 点）' % len(rows))
    return 1 if bad else 0


def head_media():
    bad = 0
    for s in read_sources():
        if s['class'] not in ('film', 'photo') or not s['media'].startswith('http') or 'youtube.com' in s['media']:
            continue
        try:
            st, ct, ln = head(s['media'])
        except Exception as e:
            print('%s 🔴 HEAD できない：%s' % (s['code'], e))
            bad += 1
            continue
        print('%s media HEAD %d %s %.1fMB' % (s['code'], st, ct, ln / 1e6))
        if st != 200 or ln < 10_000:
            bad += 1
        time.sleep(1)
    return 1 if bad else 0


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    arg = sys.argv[2] if len(sys.argv) > 2 else None
    if cmd == 'yt':
        sys.exit(yt(arg, sys.argv[3]))
    sys.exit({'films': lambda: films(arg), 'photos': lambda: photos(arg), 'check': check, 'head-media': head_media}[cmd]())
