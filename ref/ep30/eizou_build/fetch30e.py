# -*- coding: utf-8 -*-
"""30本目 映像方針（2026-11-05・チャット5）：了承②の範囲の素材を取る・照らす（29本目 fetch29.py の型）。

  python -I -X utf8 ref/ep30/eizou_build/fetch30e.py check <meta.json>   資料館の写真（ブラウザの同じオリジンで取って dec30.py で戻した分）＝大きさと SHA-256 を照らして記録
  python -I -X utf8 ref/ep30/eizou_build/fetch30e.py commons              sources30.psv の get＝commons:… を幅1920（画像が小さければ原本）で src/eizou/ へ
  python -I -X utf8 ref/ep30/eizou_build/fetch30e.py m6                   『平成6年防衛庁記録』の変換版 1080p から 17:20〜18:26 だけ（音なし）を src/footage/M6.webm へ

作法（記憶 reference-commons-standard-thumbnail-sizes）：標準の縮小版だけ・間をあける・429 は待つ（回避しない）・縮小版の URL は API の thumburl から（画像が小さいと原本に化ける＝幅で分ける）。
落としかけを測らない＝md5 を2回。記録＝eizou_build/fetch30.tsv（公開リポに入る＝撮影者の名前は書かない）。撮影者＝git の外の src/credits_private.tsv。
"""
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
LOG = os.path.join(HERE, 'fetch30.tsv')
CRED = os.path.join(EP, 'src', 'credits_private.tsv')
OUTDIR = os.path.join(EP, 'src', 'eizou')
UA = {'User-Agent': 'zukai-engine-research/1.0 (GitHub torotorotolo)'}
API = 'https://commons.wikimedia.org/w/api.php'
WIDTH = 1920
GAP = 8


def md5(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def sha256(path):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def log(row):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        if new:
            f.write('取った日\t記号\t種類\tbytes\tmd5\tmd5（読み直し）\tファイル\t出どころ\n')
        f.write('\t'.join(str(x) for x in row) + '\n')


def check(meta_path):
    txt = open(meta_path, encoding='utf-8', errors='replace').read()      # javascript_tool の大きな戻り値（tool-results の JSON）
    if txt.lstrip().startswith('['):
        txt = ''.join(x.get('text', '') for x in json.loads(txt))
    s, _ = json.JSONDecoder().raw_decode(txt[txt.index('"'):])
    meta = json.loads(s.split('|PAD|')[0])
    bad = 0
    for name, (n, sha, status) in sorted(meta.items()):
        p = os.path.join(OUTDIR, name)
        if not os.path.exists(p):
            print('🔴 無い', name)
            bad += 1
            continue
        size, s2 = os.path.getsize(p), sha256(p)
        m1, m2 = md5(p), md5(p)
        ok = status == 200 and size == n and s2 == sha and m1 == m2
        if not ok:
            print('🔴 合わない', name, size, n, status)
            bad += 1
            continue
        log([datetime.date.today().isoformat(), name.split('.')[0], 'moj', n, m1, m2, 'src/eizou/' + name, 'moj.go.jp/psia/aumarchive/museum/（同じオリジンの fetch・SHA-256 一致）'])
    print('資料館 %d 点・合わない %d' % (len(meta), bad))
    return 1 if bad else 0


def ask(title):
    kw = dict(action='query', titles='File:' + title, prop='imageinfo', iiprop='url|size|sha1|extmetadata', iiurlwidth=WIDTH,
              iiextmetadatafilter='LicenseShortName|Artist|DateTimeOriginal|Credit', format='json', formatversion=2)
    url = API + '?' + urllib.parse.urlencode(kw)
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60))
        except Exception as e:      # 429 など＝待って取り直す（回避はしない）
            print('  ERR', e, file=sys.stderr)
            time.sleep(60 * (i + 1))
    return None


def get(url, path):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r, open(path + '.part', 'wb') as f:
                n = 0
                for b in iter(lambda: r.read(1 << 20), b''):
                    f.write(b)
                    n += len(b)
                want = int(r.headers.get('Content-Length') or n)
            if n != want:
                raise RuntimeError('大きさが違う %d / %d' % (n, want))
            os.replace(path + '.part', path)
            return n
        except Exception as e:      # noqa: BLE001
            print('  ERR', os.path.basename(path), e, file=sys.stderr)
            time.sleep(120 * (i + 1))
    return None


def commons():
    rows = [ln.rstrip('\n') for ln in open(os.path.join(HERE, 'sources30.psv'), encoding='utf-8') if ln.strip() and not ln.startswith('#')]
    head = rows[0].split('|')
    os.makedirs(OUTDIR, exist_ok=True)
    cred = {}
    if os.path.exists(CRED):
        for ln in open(CRED, encoding='utf-8'):
            c = ln.rstrip('\n').split('\t')
            if c and c[0]:
                cred[c[0]] = c
    bad = 0
    for r in rows[1:]:
        d = dict(zip(head, r.split('|')))
        if not d['get'].startswith('commons:'):
            continue
        code, title = d['code'], d['get'][8:].split('（')[0].strip()
        path = os.path.join(OUTDIR, code + '.jpg')
        if os.path.exists(path) and code in cred:
            print('skip', code, flush=True)
            continue
        js = ask(title)
        pg = (js or {}).get('query', {}).get('pages', [{}])[0]
        ii = (pg.get('imageinfo') or [{}])[0]
        if not ii:
            print('🔴 頁が無い', code, flush=True)
            bad += 1
            continue
        w, h = ii.get('width'), ii.get('height')
        url = ii['url'].split('?')[0] if w <= WIDTH else ii['thumburl'].split('?')[0]
        n = get(url, path)
        if not n:
            print('🔴 取れない', code, flush=True)
            bad += 1
            continue
        m1, m2 = md5(path), md5(path)
        em = {k: re.sub(r'<[^>]+>', '', v.get('value') or '').strip() for k, v in (ii.get('extmetadata') or {}).items()}
        lic = em.get('LicenseShortName', '')
        log([datetime.date.today().isoformat(), code, 'commons-%d' % min(w, WIDTH), n, m1, m2, 'src/eizou/%s.jpg' % code, 'commons:' + title])
        cred[code] = [code, title, em.get('Artist', '')[:120], lic, em.get('DateTimeOriginal', '')[:30], ii.get('descriptionurl', ''), '%dx%d' % (w, h)]
        with open(CRED, 'w', encoding='utf-8', newline='\n') as f:
            for c in cred.values():
                f.write('\t'.join(str(x).replace('\t', ' ').replace('\n', ' ') for x in c) + '\n')
        print('%s %.2fMB 原本%dx%d %s 日=%s %s' % (code, n / 1e6, w, h, lic, em.get('DateTimeOriginal', '')[:20], 'md5一致' if m1 == m2 else '🔴md5不一致'), flush=True)
        bad += m1 != m2
        time.sleep(GAP)
    print('おわり＝失敗 %d' % bad)
    return 1 if bad else 0


def m6():
    name = '平成６年防衛庁記録.webm'
    q = urllib.parse.quote(name)
    url = 'https://upload.wikimedia.org/wikipedia/commons/transcoded/9/9d/%s/%s.1080p.vp9.webm' % (q, q)
    os.makedirs(os.path.join(EP, 'src', 'footage'), exist_ok=True)
    out = os.path.join(EP, 'src', 'footage', 'M6.webm')
    cmd = ['ffmpeg', '-y', '-v', 'error', '-user_agent', UA['User-Agent'], '-seekable', '1', '-multiple_requests', '1', '-reconnect', '1', '-reconnect_on_network_error', '1',
           '-ss', '1040', '-i', url, '-t', '66', '-an', '-c:v', 'copy', out]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('ffmpeg rc=%d %s' % (r.returncode, r.stderr[-300:]))
    if r.returncode or not os.path.exists(out):
        return 1
    n = os.path.getsize(out)
    m1, m2 = md5(out), md5(out)
    dur = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=width,height', '-of', 'csv=p=0', out], capture_output=True, text=True).stdout.split()
    # 🔴 ffmpeg は rc=0 のまま 471 バイトで終わることがある（11-05）＝大きさと長さで照らす（記憶 feedback-fetch-failure-falls-back-to-a-still）
    secs = [float(x) for x in dur if re.fullmatch(r'[\d.]+', x)]
    if n < 1000000 or not secs or not 60 <= secs[-1] <= 72:
        print('🔴 区間が取れていない %d B %s' % (n, dur))
        return 1
    log([datetime.date.today().isoformat(), 'M6', 'commons-1080p 17:20〜18:26', n, m1, m2, 'src/footage/M6.webm', 'commons:' + name])
    print('M6 %.1fMB %s %s' % (n / 1e6, dur, 'md5一致' if m1 == m2 else '🔴md5不一致'))
    return 0 if m1 == m2 else 1


def main():
    mode = sys.argv[1]
    if mode == 'check':
        return check(sys.argv[2])
    if mode == 'commons':
        return commons()
    if mode == 'm6':
        return m6()
    return 2


if __name__ == '__main__':
    sys.exit(main())
