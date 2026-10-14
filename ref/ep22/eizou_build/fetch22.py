# -*- coding: utf-8 -*-
"""22本目 映像方針：素材を取る・確かめる（出力＝eizou_build/fetch22.tsv）。21本目の fetch21.py を写し、手元の PDF から図を抜く figs と、
大きい映像の「使う区間だけ」を取る clips を足した（C: の空きが少ないため・了承② 2026-10-14）。

  python -I ref/ep22/eizou_build/fetch22.py figs                 # class=fig を手元の PDF から抜く（埋め込み画像をそのまま PNG に）
  python -I ref/ep22/eizou_build/fetch22.py photos [記号,…]      # class=photo（DVIDS の原本＝HEAD → GET → 長さ照合／Commons＝API → 原本は sha1・幅1920超は標準の縮小版）
  python -I ref/ep22/eizou_build/fetch22.py films [記号,…]       # get=full の映像を丸ごと（HEAD → GET → 長さ照合）
  python -I ref/ep22/eizou_build/fetch22.py clips [記号,…]       # get=clips の映像を、list22.tsv の区間ごとに「前後10秒」まで切り出す（キーフレームから・再エンコードなし）
  python -I ref/ep22/eizou_build/fetch22.py check                # 全素材の md5 を2回・大きさ・EXIF の日付・映像の長さ → fetch22.tsv
  python -I ref/ep22/eizou_build/fetch22.py head-media           # 焼くときに引く media の URL を全部 HEAD（取れない映像は黙って静止画に落ちる＝先に確かめる）

すでに置き場にあって大きさが合えば取らない。落としかけ（.part）は測らない。道具の名乗りにメールや @ を入れない。
🔴 撮影者・投稿者の名前は src/credits_private.tsv（git の外）にだけ書く（公開のリポに私人の名前を置かない）。
"""
import csv
import hashlib
import json
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
REPO = os.path.dirname(os.path.dirname(EP))
UA = 'zukai-engine-research/1.0 (personal non-commercial research; github torotorotolo)'
API = 'https://commons.wikimedia.org/w/api.php'
OUT = os.path.join(HERE, 'fetch22.tsv')
LIST = os.path.join(HERE, 'list22.tsv')
PRIVATE = os.path.join(EP, 'src', 'credits_private.tsv')
MARGIN = 10.0


def read_sources():
    with open(os.path.join(HERE, 'sources22.tsv'), encoding='utf-8') as f:
        lines = [ln for ln in f if not ln.startswith('#') and ln.strip()]
    return list(csv.DictReader(lines, delimiter='\t'))


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', errors='replace')


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


def private_row(row):
    new = not os.path.exists(PRIVATE)
    with open(PRIVATE, 'a', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        if new:
            f.write('# 22本目 映像方針：出典の行に要る撮影者・投稿者の名前（git の外＝公開のリポに置かない）。fetch22.py が足す・人が足す\n')
            w.writerow(['code', 'title', 'width', 'height', 'artist', 'license', 'date', 'credit'])
        w.writerow(row)


# ── figs：手元の PDF から抜く ─────────────────────────────
def figs(codes=None):
    import fitz
    from PIL import Image
    sel, bad = want(codes), 0
    for s in read_sources():
        if s['class'] != 'fig' or (sel and s['code'] not in sel):
            continue
        dst = os.path.join(REPO, s['file'])
        if os.path.exists(dst):
            print('%s 済み' % s['code'])
            continue
        _, pdf, page, idx = s['get'].split(':', 3)
        doc = fitz.open(os.path.join(REPO, pdf))
        imgs = doc[int(page) - 1].get_images(full=True)
        parts = []
        for k in idx.split('+'):
            pix = fitz.Pixmap(doc, imgs[int(k)][0])
            if pix.n > 4 or (pix.colorspace and pix.colorspace.n not in (1, 3)):
                pix = fitz.Pixmap(fitz.csRGB, pix)
            parts.append(Image.frombytes('RGB' if pix.n >= 3 else 'L', (pix.width, pix.height), pix.samples).convert('RGB'))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if len(parts) == 1:
            parts[0].save(dst)
        else:   # 左から右へ（get の順）＝報告書の図と同じ並び。1枚ずつには手を入れない（間に16pxの黒）
            Wd = sum(p.width for p in parts) + 16 * (len(parts) - 1)
            Hd = max(p.height for p in parts)
            sheet = Image.new('RGB', (Wd, Hd), (0, 0, 0))
            x = 0
            for i, p in enumerate(parts):
                sheet.paste(p, (x, (Hd - p.height) // 2))
                p.save(dst.replace('.png', '_%d.png' % (i + 1)))
                x += p.width + 16
            sheet.save(dst)
        dims = 'x'.join(str(v) for v in (parts[0].size if len(parts) == 1 else (sum(p.width for p in parts), max(p.height for p in parts))))
        exp = s['dims'].split('×')[0]
        if len(parts) == 1 and exp != dims:
            print('%s 🔴 大きさが台帳と違う（台帳 %s・抜いた絵 %s）' % (s['code'], s['dims'], dims))
            bad += 1
        print('%s → %s（%s）' % (s['code'], s['file'], dims))
    return 1 if bad else 0


# ── photos：DVIDS の原本と Commons ─────────────────────────
def api_info(code, title, width=None):
    q = {'action': 'query', 'titles': title, 'prop': 'imageinfo', 'iiprop': 'url|size|sha1|extmetadata',
         'iiextmetadatafilter': 'Artist|LicenseShortName|Credit|DateTimeOriginal', 'format': 'json', 'formatversion': '2'}
    if width:
        q['iiurlwidth'] = str(width)
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(q), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        p = json.loads(r.read().decode('utf-8'))['query']['pages'][0]
    ii = p['imageinfo'][0]
    em = ii.get('extmetadata', {})
    g = lambda k: re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', em.get(k, {}).get('value') or '')).strip()[:200]
    private_row([code, p['title'], ii.get('width'), ii.get('height'), g('Artist'), g('LicenseShortName'), g('DateTimeOriginal'), g('Credit')])
    if width:
        return ii['thumburl'], None, None, ii['width']
    return ii['url'], ii['size'], ii['sha1'], ii['width']


def photos(codes=None):
    sel, bad = want(codes), 0
    for s in read_sources():
        if s['class'] != 'photo' or (sel and s['code'] not in sel):
            continue
        dst = os.path.join(REPO, s['file'])
        if os.path.exists(dst):
            print('%s 済み' % s['code'])
            continue
        if s['get'].startswith('commons'):
            title = 'File:' + s['media'].split(':', 1)[1]
            try:
                url, size, sha1, w0 = api_info(s['code'], title)
                if w0 > 1920:   # 21本目：原本の GET は数点で 429＝標準の縮小版（3840／1920）
                    url, size, sha1, _ = api_info(s['code'] + '（縮小版）', title, 3840 if w0 > 3840 else 1920)
            except Exception as e:
                print('%s 🔴 API が引けない：%s' % (s['code'], e))
                bad += 1
                continue
            ok = fetch_direct(s['code'], url, dst, ('image/',), size, sha1)
            time.sleep(10)
        else:
            ok = fetch_direct(s['code'], s['media'], dst, ('image/', 'binary/octet-stream', 'application/octet-stream'),
                              int(s['bytes']) if s['bytes'].isdigit() else None)
            time.sleep(3)
        bad += 0 if ok else 1
    return 1 if bad else 0


# ── films：丸ごと ───────────────────────────────────────
def films(codes=None):
    sel, bad = want(codes), 0
    for s in read_sources():
        if s['class'] != 'film' or s['get'] != 'full' or (sel and s['code'] not in sel):
            continue
        dst = os.path.join(REPO, s['file'])
        if os.path.exists(dst) and os.path.getsize(dst) == int(s['bytes']):
            print('%s 済み（大きさ一致）' % s['code'])
            continue
        ok = fetch_direct(s['code'], s['media'], dst, ('video/', 'application/octet-stream', 'binary/octet-stream'), int(s['bytes']))
        bad += 0 if ok else 1
        time.sleep(5)
    return 1 if bad else 0


# ── clips：使う区間だけ（前後10秒・キーフレームから・再エンコードなし） ───────
def windows():
    out = {}
    with open(LIST, encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['window']:
                a, b = [float(v) for v in r['window'].split('〜')]
                out.setdefault(r['code'], []).append((a, b, r['cid']))
    return out


def keyframe_before(url, t):
    lo = max(0.0, t - 40)
    r = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-skip_frame', 'nokey', '-show_entries', 'frame=pts_time',
             '-of', 'csv=p=0', '-read_intervals', '%.2f%%%.2f' % (lo, t + 0.5), url])
    ks = sorted(float(x) for x in r.stdout.split() if re.match(r'^[\d.]+$', x))
    ks = [k for k in ks if k <= t + 1e-3]
    if not ks:
        raise RuntimeError('キーフレームが見つからない（%s %.1f秒）：%s' % (url[-40:], t, r.stderr[-200:]))
    return ks[-1]


def clips(codes=None):
    sel, bad = want(codes), 0
    wins = windows()
    for s in read_sources():
        if s['class'] != 'film' or s['get'] != 'clips' or (sel and s['code'] not in sel):
            continue
        folder = os.path.join(REPO, s['file'])
        os.makedirs(folder, exist_ok=True)
        try:
            st, ct, ln = head(s['media'])
        except Exception as e:
            print('%s 🔴 HEAD できない：%s' % (s['code'], e))
            bad += 1
            continue
        print('%s media HEAD %d %s %.1fMB' % (s['code'], st, ct, ln / 1e6), flush=True)
        for a, b, cid in sorted(wins.get(s['code'], [])):
            have = [f for f in os.listdir(folder) if f.endswith('.mp4')]
            hit = [f for f in have if (lambda m: m and float(m.group(1)) <= a and b <= float(m.group(2)))(re.match(r't([\d.]+)_([\d.]+)\.mp4$', f))]
            if hit:
                print('  %s %.1f〜%.1f 済み（%s）' % (cid, a, b, hit[0]))
                continue
            k = keyframe_before(s['media'], max(0.0, a - MARGIN))
            e = b + MARGIN
            dst = os.path.join(folder, 't%08.3f_%08.3f.mp4' % (k, e))
            part = dst + '.part.mp4'
            r = run(['ffmpeg', '-v', 'error', '-y', '-user_agent', UA, '-ss', '%.3f' % k, '-i', s['media'], '-t', '%.3f' % (e - k),
                     '-map', '0:v:0', '-map', '0:a?', '-c', 'copy', '-avoid_negative_ts', 'make_zero', part])
            if r.returncode != 0 or not os.path.exists(part):
                print('  🔴 %s 切り出せない：%s' % (cid, r.stderr[-300:]))
                bad += 1
                continue
            pr = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=nw=1:nk=1', part])
            d = float(pr.stdout.strip() or 0)
            if d < (e - k) - 1.5:
                print('  🔴 %s 長さが足りない（%.1f秒・欲しい %.1f秒）＝.part のまま' % (cid, d, e - k))
                bad += 1
                continue
            os.replace(part, dst)
            print('  %s %.1f〜%.1f → %s（キーフレーム %.3f 秒から %.1f 秒・%d bytes）' % (cid, a, b, os.path.relpath(dst, REPO), k, d, os.path.getsize(dst)), flush=True)
            time.sleep(3)
    return 1 if bad else 0


# ── check：md5 を2回 ───────────────────────────────────
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
    r = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration', '-of', 'json', path])
    try:
        j = json.loads(r.stdout)
        st = j['streams'][0]
        return '%dx%d' % (st['width'], st['height']), '%.2f' % float(j['format']['duration'])
    except Exception:
        return '?', '?'


def files_of(s):
    p = os.path.join(REPO, s['file'])
    if s['file'].endswith('/'):
        return [os.path.join(p, f) for f in sorted(os.listdir(p)) if f.endswith('.mp4')] if os.path.isdir(p) else []
    out = [p] if os.path.exists(p) else []
    base = p[:-4]
    k = 1
    while os.path.exists('%s_%d.png' % (base, k)):
        out.append('%s_%d.png' % (base, k))
        k += 1
    return out


def check():
    rows, bad, missing = [], 0, 0
    for s in read_sources():
        fs = files_of(s)
        if not fs:
            print('— 無い（まだ取っていない）：%s %s' % (s['code'], s['file']))
            missing += 1
            continue
        for p in fs:
            a = md5(p)
            time.sleep(0.5)
            b = md5(p)
            ok = a == b
            bad += 0 if ok else 1
            if s['class'] == 'film':
                dims, dur = probe(p)
                date = '—'
            else:
                size, date = exif_date(p)
                dims, dur = ('%dx%d' % size if size else '?'), '—'
            rel = os.path.relpath(p, REPO).replace('\\', '/')
            rows.append([s['code'], s['class'], rel, os.path.getsize(p), a, 'md5 2回一致' if ok else '🔴 md5 が2回で違う', dims, dur, date, s['page']])
            print('%s %s %d bytes md5=%s %s %s %s %s' % (s['code'], rel, os.path.getsize(p), a, '一致' if ok else '🔴不一致', dims, dur, date))
    with open(OUT, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 22本目 映像方針：取った素材（fetch22.py check の出力＝手で直さない）。置き場は git の外（ref/* は .gitignore）。clips/ は使う区間＋前後10秒＝名前の t<始め>_<終わり> が元の映像の秒\n')
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['code', 'class', 'file', 'bytes', 'md5', 'md5_check', 'dims', 'dur', 'exif_date', 'page'])
        w.writerows(rows)
    print('→', OUT, '（%d ファイル・無い記号 %d）' % (len(rows), missing))
    return 1 if bad else 0


def head_media():
    bad = 0
    for s in read_sources():
        if s['class'] not in ('film', 'photo') or not s['media'].startswith('http'):
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
    sys.exit({'figs': lambda: figs(arg), 'photos': lambda: photos(arg), 'films': lambda: films(arg), 'clips': lambda: clips(arg),
              'check': check, 'head-media': head_media}[cmd]())
