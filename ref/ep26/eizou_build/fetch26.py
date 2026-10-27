# -*- coding: utf-8 -*-
"""26本目 映像方針：一覧（list26.tsv）が使う Commons の写真を取る（2026-10-27・チャット5）。

  python -P ref/ep26/eizou_build/fetch26.py plan    → 取る点・ファイル名・大きさ（原本の bytes）・取る幅の一覧（取らない）
  python -P ref/ep26/eizou_build/fetch26.py fetch   → 取る（了承②のあと）。間をあけ、429 は長く待つ。md5 を2回取り、fetch26.tsv に残す

決まり（記憶 reference-commons-standard-thumbnail-sizes）：原本の幅が3840超→3840px／1920超→1920px の標準の縮小版・それ以下は原本（sha1 で照合）。
縮小版は sha1 が無い＝長さ（Content-Length）の照合と md5 を2回。名乗り（User-Agent）にメールや「@」を入れない。
ファイル名は src/commons/pick26.tsv（git の外）か sources26.psv の commons-new:（このチャットで足した点）から引く。
"""
import csv
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
UA = {'User-Agent': 'zukai-engine-research/1.0 (ep26 eizou)'}
API = 'https://commons.wikimedia.org/w/api.php'
LOG = os.path.join(HERE, 'fetch26.tsv')
GAP = float(os.environ.get('FETCH_GAP', '10'))


def get_json(params):
    url = API + '?' + urllib.parse.urlencode(dict(params, format='json', formatversion=2))
    for n in range(6):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(30 * (n + 1))
                continue
            raise
    raise RuntimeError('API が 429/503 を返し続けた')


def targets():
    """list26.tsv が使う commons-photo の記号 → (ファイル名, 置き場)"""
    src = {}
    with open(os.path.join(HERE, 'sources26.psv'), encoding='utf-8') as f:
        rows = [ln.rstrip('\n') for ln in f if not ln.startswith('#') and ln.strip()]
    head = rows[0].split('|')
    for r in rows[1:]:
        d = dict(zip(head, r.split('|')))
        src[d['code']] = d
    used = []
    with open(os.path.join(HERE, 'list26.tsv'), encoding='utf-8') as f:
        for d in csv.DictReader(f, delimiter='\t'):
            if d['code'] and src.get(d['code'], {}).get('type') == 'commons-photo' and d['code'] not in used:
                used.append(d['code'])
    pick = {}
    with open(os.path.join(EP, 'src', 'commons', 'pick26.tsv'), encoding='utf-8') as f:
        for d in csv.DictReader(f, delimiter='\t'):
            pick[d['key']] = d['title']
    out = []
    for code in used:
        g = src[code]['get']
        title = g.split(':', 1)[1] if g.startswith('commons-new:') else pick.get(code)
        if not title:
            raise SystemExit('ファイル名が引けない：%s（%s）' % (code, g))
        out.append((code, 'File:' + title, src[code]['file']))
    return out


def info(titles):
    res = {}
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        d = get_json(dict(action='query', titles='|'.join(chunk), prop='imageinfo', iiprop='size|sha1|url|mime'))
        norm = {n['to']: n['from'] for n in (d['query'].get('normalized') or [])}
        for p in d['query']['pages']:
            ii = (p.get('imageinfo') or [{}])[0]
            res[norm.get(p['title'], p['title'])] = ii
        time.sleep(2)
    return res


def width_for(w):
    return 3840 if w > 3840 else (1920 if w > 1920 else None)


def thumb_url(title, width):
    d = get_json(dict(action='query', titles=title, prop='imageinfo', iiprop='url', iiurlwidth=width))
    ii = d['query']['pages'][0]['imageinfo'][0]
    u = ii.get('thumburl', '')
    if '/thumb/' not in u:
        raise RuntimeError('縮小版の URL でない（原本が返った）：%s' % title)
    return u


def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def sha1(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def download(url, path):
    for n in range(5):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                want = int(r.headers.get('Content-Length') or 0)
                data = r.read()
            if want and len(data) != want:
                raise RuntimeError('長さが合わない %d / %d' % (len(data), want))
            tmp = path + '.part'
            with open(tmp, 'wb') as f:
                f.write(data)
            os.replace(tmp, path)
            return want or len(data)
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 120 * (n + 1)
                print('  429 → %d秒待つ' % wait, flush=True)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError('429 が続いた：%s' % url)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'plan'
    tg = targets()
    meta = info([t for _, t, _ in tg])
    total = 0
    rows = []
    for code, title, file in tg:
        ii = meta.get(title) or {}
        w, h, size = ii.get('width', 0), ii.get('height', 0), ii.get('size', 0)
        tw = width_for(w)
        total += size
        rows.append((code, title, file, w, h, size, tw, ii))
    if mode == 'plan':
        for code, title, file, w, h, size, tw, ii in rows:
            print('%s\t%dx%d\t%.2fMB（原本）\t%s\t%s' % (code, w, h, size / 1e6, ('%dpx の縮小版' % tw) if tw else '原本（sha1 で照合）', title[5:] if not code.startswith('S1-057') else '（撮影者の名が入る名前＝pick26.tsv）'))
        print('点数 %d・原本の合計 %.1fMB（縮小版はこれより小さい）' % (len(rows), total / 1e6))
        return 0
    done = set()
    if os.path.exists(LOG):
        with open(LOG, encoding='utf-8') as f:
            done = {ln.split('\t')[0] for ln in f if ln.strip() and not ln.startswith('code\t')}
    else:
        with open(LOG, 'w', encoding='utf-8', newline='\n') as f:
            f.write('code\twhen\tfile\tbytes\twidth\tmd5_1\tmd5_2\tsha1_ok\turl_kind\n')
    bad = 0
    for code, title, file, w, h, size, tw, ii in rows:
        if code in done:
            continue
        path = os.path.join(REPO, file)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            if tw:
                url = thumb_url(title, tw)
                time.sleep(2)
            else:
                url = ii['url']
            n = download(url, path)
            m1, m2 = md5(path), md5(path)
            ok = ''
            if not tw:
                ok = 'yes' if sha1(path) == ii.get('sha1') else 'NO'
                if ok == 'NO':
                    bad += 1
            with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
                f.write('%s\t%s\t%s\t%d\t%s\t%s\t%s\t%s\t%s\n' % (code, time.strftime('%Y-%m-%d %H:%M'), file, n, tw or w, m1, m2, ok, 'thumb' if tw else 'original'))
            print('%s %d bytes md5 %s %s %s' % (code, n, m1[:8], 'md5x2一致' if m1 == m2 else '✗md5x2', ('sha1 ' + ok) if ok else ''), flush=True)
        except Exception as e:
            bad += 1
            print('%s ✗ %s' % (code, e), flush=True)
        time.sleep(GAP)
    print('おわり＝失敗 %d' % bad)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
