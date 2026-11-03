# -*- coding: utf-8 -*-
"""29本目 映像方針（2026-11-03・チャット5）：Commons（と Pexels）の写真を取る（了承の範囲だけ）。28本目の fetch28.py を写した。

  python -P ref/ep29/eizou_build/fetch29.py look CM004 P0010 ...           → Commons の標準の縮小版（幅960）を src/look_eizou/ へ（見本帳用）
  python -P ref/ep29/eizou_build/fetch29.py look1920 CM004                 → 同じく幅1920（地の暗さの見本用）
  python -P ref/ep29/eizou_build/fetch29.py final CM004 ...                → 本番＝幅1920（画像が1920以下なら原本）を src/eizou/ へ（了承②のあと）
  python -P ref/ep29/eizou_build/fetch29.py stock [記号…]                  → Pexels の映像（get＝stock:<直リンク>）を src/eizou/<記号>.mp4 へ（⑤b）

作法（記憶 reference-commons-standard-thumbnail-sizes）：Commons は原本をまとめて取ると 429 → 標準の大きさ（960・1280・1920・3840）の縮小版だけ・5秒あけ・429 は120秒以上待つ。
縮小版の URL は原本の URL から組む（API の thumburl は画像が小さいと原本に化ける）。落としかけを測らない＝md5 を2回（取った直後と読み直し）。
記録＝eizou_build/fetch29.tsv（取った日・記号・大きさ・md5・出どころ）。🔴 撮影者の名前は書かない（src/commons/geo29.json＝git の外）。User-Agent に @ を入れない。
"""
import datetime
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
GEO = os.path.join(EP, 'src', 'commons', 'geo29.json')
LOG = os.path.join(HERE, 'fetch29.tsv')
UA = {'User-Agent': 'zukai-engine-research/1.0 (GitHub torotorotolo)'}
GAP = float(os.environ.get('FETCH_GAP', '5'))
BIG = {'CM119'}          # 本番を幅3840で取る点（c215＝上半分に切る＝幅1920だと足りない）


def md5(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def thumb_url(orig, width):
    """https://upload.wikimedia.org/wikipedia/commons/a/ab/Name.jpg → …/commons/thumb/a/ab/Name.jpg/<幅>px-Name.jpg"""
    head, tail = orig.split('/wikipedia/commons/', 1)
    a, ab, name = tail.split('/', 2)
    ext = '' if name.lower().endswith(('.jpg', '.jpeg', '.png')) else '.jpg'
    return '%s/wikipedia/commons/thumb/%s/%s/%s/%dpx-%s%s' % (head, a, ab, name, width, name, ext)


def get(url, path):
    for i in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
            with open(path, 'wb') as f:
                f.write(data)
            return len(data)
        except Exception as e:      # 429 などは待って取り直す（回避はしない）
            print('  ERR', os.path.basename(path), e, file=sys.stderr)
            time.sleep(120 * (i + 1))
    return None


def log(row):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        if new:
            f.write('取った日\t記号\t種類\tbytes\tmd5\tmd5（読み直し）\tファイル\t出どころ\n')
        f.write('\t'.join(str(x) for x in row) + '\n')


def stock(only=None):
    """⑤b：Pexels の映像（sources29 の get＝stock:<置き場の直リンク>・了承②）＝幅1920の版を src/eizou/<記号>.mp4 へ。
    HEAD で大きさ → 流しながら GET（丸ごとメモリに載せない）→ 長さの照合 → md5 を2回 → fetch29.tsv の 出どころ＝`stock:<直リンク>`
    ⚠️ 記号は素材を替えても同じ＝記録の直リンクと違えば取り直す（記録は足すだけ・最後の行が効く）"""
    rows = [ln.rstrip('\n') for ln in open(os.path.join(HERE, 'sources29.psv'), encoding='utf-8') if ln.strip() and not ln.startswith('#')]
    head = rows[0].split('|')
    done = {}
    with open(LOG, encoding='utf-8') as f:
        for ln in f:
            c = ln.rstrip('\n').split('\t')
            if len(c) >= 8 and c[2] == 'stock':
                done[c[1]] = c[7]
    bad = 0
    for r in rows[1:]:
        d = dict(zip(head, r.split('|')))
        if d['type'] != 'stock' or not d['get'].startswith('stock:http') or done.get(d['code']) == d['get'] or (only and d['code'] not in only):
            continue
        url = d['get'][6:]
        path = os.path.join(EP, d['file'])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            with urllib.request.urlopen(urllib.request.Request(url, method='HEAD', headers=UA), timeout=60) as h:
                want, ct = int(h.headers.get('Content-Length') or 0), h.headers.get('Content-Type') or ''
            if not ct.startswith('video/') or not want:
                raise RuntimeError('HEAD が映像でない（%s・%d B）' % (ct, want))
            n = 0
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=300) as g, open(path, 'wb') as f:
                for b in iter(lambda: g.read(1 << 20), b''):
                    f.write(b)
                    n += len(b)
            if n != want or os.path.getsize(path) != want:
                raise RuntimeError('大きさが HEAD と違う（%d / %d）' % (os.path.getsize(path), want))
            m1, m2 = md5(path), md5(path)
            log([datetime.date.today().isoformat(), d['code'], 'stock', n, m1, m2, d['file'], 'stock:' + url])
            print('%s %.1fMB md5 %s %s' % (d['code'], n / 1e6, m1[:8], 'md5x2一致' if m1 == m2 else '🔴md5不一致'), flush=True)
            bad += m1 != m2
        except Exception as e:      # noqa: BLE001
            bad += 1
            print('%s ✗ %s' % (d['code'], e), flush=True)
        time.sleep(3)
    print('おわり＝失敗 %d' % bad)
    return 1 if bad else 0


def main():
    mode, items = sys.argv[1], sys.argv[2:]
    if mode == 'stock':
        return stock(set(items) or None)
    geo = json.load(open(GEO, encoding='utf-8')) if os.path.exists(GEO) else {}
    outdir = os.path.join(EP, 'src', 'eizou' if mode.startswith('final') else 'look_eizou')
    os.makedirs(outdir, exist_ok=True)
    ok = ng = 0
    for it in items:
        if mode in ('look', 'look1920', 'final'):
            g = geo[it]
            w = {'look': 960, 'look1920': 1920, 'final': 1920}[mode]
            if mode == 'final' and it in BIG:
                w = 3840                             # 全景を流す・寄る余地（了承② 10-29）
            orig = g['url'].split('?')[0]            # 🔴 10-29 から API の URL の後ろに ?utm_… が付く＝外してから組む
            api = (g.get('thumb960') or '').split('?')[0]
            if g['w'] <= w:
                url = orig                           # 画像が幅以下＝原本（標準の縮小版は作れない）
            elif '/960px-' in api:
                url = api.replace('/960px-', '/%dpx-' % w)   # API が返した縮小版の置き場（10-29 は thumb.wikimedia.org）
            else:
                url = thumb_url(orig, w)
            path = os.path.join(outdir, '%s%s.jpg' % (it, '' if mode != 'look1920' else '_1920'))
            src = 'commons:' + g['page']
        else:
            pid, fname = it.split(':', 1)
            w = 640 if mode == 'lookpx' else 1920
            url = 'https://images.pexels.com/photos/%s/%s?auto=compress&cs=tinysrgb&w=%d' % (pid, fname, w)
            path = os.path.join(outdir, 'PX%s%s.jpg' % (pid, '' if mode == 'lookpx' else '_1920'))
            src = 'https://www.pexels.com/photo/%s/' % pid
        if os.path.exists(path):
            print('skip', os.path.basename(path))
            continue
        n = get(url, path)
        if not n:
            ng += 1
            print('NG', it)
            continue
        m1 = md5(path)
        m2 = md5(path)
        log([datetime.date.today().isoformat(), it, mode, n, m1, m2, os.path.relpath(path, EP).replace('\\', '/'), src])
        print('ok %s %d bytes md5=%s %s' % (it, n, m1[:10], 'md5一致' if m1 == m2 else '🔴md5不一致'))
        ok += 1
        time.sleep(GAP if mode in ('look', 'look1920', 'final') else 1.5)
    print('done ok=%d ng=%d' % (ok, ng))
    return 1 if ng else 0


if __name__ == '__main__':
    sys.exit(main())
