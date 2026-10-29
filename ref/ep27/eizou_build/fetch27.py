# -*- coding: utf-8 -*-
"""27本目 映像方針（2026-10-29・チャット5）：Commons と Pexels の写真を取る（了承の範囲だけ）。26本目の fetch26.py と同じ作法。

  python -P ref/ep27/eizou_build/fetch27.py look CM044 CM045 ...           → Commons の標準の縮小版（幅960）を src/look_eizou/ へ（見本帳用）
  python -P ref/ep27/eizou_build/fetch27.py look1920 CM045 CM254           → 同じく幅1920（地の暗さの見本用）
  python -P ref/ep27/eizou_build/fetch27.py lookpx 30037331:pexels-photo-30037331.jpeg ...   → Pexels の幅640（見本帳用）
  python -P ref/ep27/eizou_build/fetch27.py final CM044 ...                → 本番＝幅1920（画像が1920以下なら原本）を src/eizou/ へ（了承②のあと）
  python -P ref/ep27/eizou_build/fetch27.py finalpx 30037331:pexels-photo-30037331.jpeg ... → Pexels 幅1920 を src/eizou/ へ（了承②のあと）

作法（記憶 reference-commons-standard-thumbnail-sizes）：Commons は原本をまとめて取ると 429 → 標準の大きさ（960・1280・1920・3840）の縮小版だけ・5秒あけ・429 は120秒以上待つ。
縮小版の URL は原本の URL から組む（API の thumburl は画像が小さいと原本に化ける）。落としかけを測らない＝md5 を2回（取った直後と読み直し）。
記録＝eizou_build/fetch27.tsv（取った日・記号・大きさ・md5・出どころ）。🔴 撮影者の名前は書かない（src/commons/geo27.json＝git の外）。User-Agent に @ を入れない。
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
GEO = os.path.join(EP, 'src', 'commons', 'geo27.json')
LOG = os.path.join(HERE, 'fetch27.tsv')
UA = {'User-Agent': 'zukai-engine-research/1.0 (GitHub torotorotolo)'}
GAP = float(os.environ.get('FETCH_GAP', '5'))
BIG = {'CM054'}          # 本番を幅3840で取る点（鶴見岳からの全景＝c107・c706 で流す・引く）


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


def main():
    mode, items = sys.argv[1], sys.argv[2:]
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
