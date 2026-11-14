# -*- coding: utf-8 -*-
"""33本目 映像方針：了承②（2026-11-15 カズヤくん「推奨どおり」）の Commons の写真36点と #15 の映像を取る。32本目 fetch32e.py の作法を短く写した。

  python -P -X utf8 ref/ep33/eizou_build/fetch33e.py --selftest         道具の対照（網に触れない）
  python -P -X utf8 ref/ep33/eizou_build/fetch33e.py --dry              取る URL を組んで見せるだけ（網に触れない）
  python -P -X utf8 ref/ep33/eizou_build/fetch33e.py photos [C7 C12 …]  Commons の写真（一覧で使う点＋控え・取ったものは飛ばす）
  python -P -X utf8 ref/ep33/eizou_build/fetch33e.py video240           #15 の 240p の全体（区間を決めるため）
  python -P -X utf8 ref/ep33/eizou_build/fetch33e.py video1080 170-235 …  #15 の 1080p の区間だけ（ffmpeg -ss -t -c copy＝要の絵から始まる＝頼んだ秒より長い）

入力：eizou_build/sources33.psv（commons-photo の行＝取る幅は「取り方」の欄）・eizou_build/list33.tsv（一覧で使う記号）・git の外の src/commons/cand33.json（原本の URL・縦横・作者）
出力：git の外の src/commons/c33/<記号>.jpg・V15_*.webm・src/credits_private.tsv（作者＝撮影者の名はここだけ）
      リポの eizou_build/fetch33.tsv（取った日・記号・bytes・md5 を2回・縦横・ファイル名）＝🔴 撮影者の名を書かない
作法（記憶 reference-commons-standard-thumbnail-sizes・feedback-download-size-is-not-completion・feedback-no-email-in-tool-headers）：
- 縮小版は標準の幅だけ。原本の URL から組む＝`…/thumb/<a>/<ab>/<名>/<幅>px-<名>`（画像の幅が頼む幅より大きいときだけ）・原本の URL の尻の `?…` は外す
- HEAD で型と大きさを確かめてから GET。大きさが HEAD と違えば止める。md5 は2回（2秒あけ）・縦横は画像を開いて照らす
- 10秒あけ・429 と 5xx は Retry-After に従って待つ（回避しない）・6回で止める・名乗りにメールと @ を入れない
"""
import datetime
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
PSV = os.path.join(HERE, 'sources33.psv')
LIST = os.path.join(HERE, 'list33.tsv')
LOG = os.path.join(HERE, 'fetch33.tsv')
CAND = os.path.join(EP, 'src', 'commons', 'cand33.json')
CRED = os.path.join(EP, 'src', 'credits_private.tsv')
OUTDIR = os.path.join(EP, 'src', 'commons', 'c33')
UA = {'User-Agent': 'zukai-engine-research/1.0 (personal video research)'}
STD = (20, 40, 60, 120, 250, 330, 500, 960, 1280, 1920, 3840)
GAP = 10
TRIES = 6
V15 = 'https://upload.wikimedia.org/wikipedia/commons/transcoded/1/14/GRENFELL.webm/GRENFELL.webm.%s.vp9.webm'


def want_width(get):
    m = re.search(r'縮小版 (\d+)', get or '')
    return int(m.group(1)) if m else None


def build_url(orig, w_req, w_img):
    o = orig.split('?')[0]
    if not o.startswith('https://upload.wikimedia.org/wikipedia/commons/'):
        raise ValueError('原本の URL の形が違う: %s' % o)
    if w_req is None or w_req >= w_img:
        return o, w_img
    if w_req not in STD:
        raise ValueError('標準でない幅 %d（%s）' % (w_req, STD))
    name = o.rsplit('/', 1)[1]
    return o.replace('/wikipedia/commons/', '/wikipedia/commons/thumb/', 1) + '/%dpx-%s' % (w_req, name), w_req


def req(url, method='GET'):
    for k in range(TRIES):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA, method=method), timeout=120)
            return r
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504):
                wait = int(e.headers.get('Retry-After') or 10)
                print('   %s %d → %d秒まつ（%d/%d）' % (method, e.code, wait, k + 1, TRIES))
                time.sleep(min(max(wait, 5), 300))
                continue
            raise
    raise RuntimeError('取り直しが %d 回とも通らない＝止める: %s' % (TRIES, url))


def md5_of(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def get_file(url, path, kinds=('image/',)):
    r = req(url, 'HEAD')
    ctype, clen = r.headers.get('Content-Type', ''), int(r.headers.get('Content-Length') or -1)
    if not ctype.startswith(kinds):
        raise RuntimeError('型が違う（%s）: %s' % (ctype, url))
    time.sleep(1)
    r = req(url, 'GET')
    part = path + '.part'
    with open(part, 'wb') as f:
        for b in iter(lambda: r.read(1 << 20), b''):
            f.write(b)
    size = os.path.getsize(part)
    if clen >= 0 and size != clen:
        raise RuntimeError('大きさが HEAD と違う（%d／%d）＝落としかけ: %s' % (size, clen, url))
    os.replace(part, path)
    m1 = md5_of(path)
    time.sleep(2)
    m2 = md5_of(path)
    if m1 != m2:
        raise RuntimeError('md5 が2回で違う: %s' % path)
    return size, m1, m2, ctype


def load_psv():
    rows = {}
    for ln in open(PSV, encoding='utf-8'):
        if ln.startswith('#') or not ln.strip() or ln.startswith('code|'):
            continue
        p = [x.strip() for x in ln.rstrip('\n').split('|')]
        rows[p[0]] = dict(zip(['code', 'type', 'grp', 'title', 'get', 'dims', 'rights', 'basis', 'credit', 'era', 'people', 'file', 'note'], p))
    return rows


def used_codes(S):
    use = set()
    for ln in open(LIST, encoding='utf-8').readlines()[1:]:
        p = ln.rstrip('\n').split('\t')
        for c in (p[5], p[6]):
            c = c.split('=')[0].strip()
            if re.fullmatch(r'C\d+', c):
                use.add(c)
    use |= {c for c, s in S.items() if s['type'] == 'commons-photo' and '控え' in s['note']}
    return sorted(use, key=lambda c: int(c[1:]))


def logged():
    done = {}
    if os.path.exists(LOG):
        for ln in open(LOG, encoding='utf-8').readlines()[1:]:
            p = ln.rstrip('\n').split('\t')
            if len(p) > 5:
                done[p[1]] = p
    return done


def write_log(row):
    new = not os.path.exists(LOG)
    with open(LOG, 'a', encoding='utf-8', newline='\n') as f:
        if new:
            f.write('date\tcode\tkind\tbytes\tmd5_1\tmd5_2\twxh\tfile\tsource\n')
        f.write('\t'.join(str(x) for x in row) + '\n')


def photos(only):
    from PIL import Image
    S = load_psv()
    files = json.load(open(CAND, encoding='utf-8'))['files']
    pathlib.Path(OUTDIR).mkdir(parents=True, exist_ok=True)
    codes = [c for c in used_codes(S) if not only or c in only]
    done = logged()
    cred = {}
    if os.path.exists(CRED):
        for ln in open(CRED, encoding='utf-8'):
            p = ln.rstrip('\n').split('\t')
            cred[p[0]] = ln.rstrip('\n')
    bad = 0
    for k, code in enumerate(codes):
        e = files[int(code[1:]) - 1]
        s = S.get(code)
        if not s:
            print('🔴 %s が sources33.psv に無い＝止める' % code)
            return 1
        url, w2 = build_url(e['orig'], want_width(s['get']), int(e['w']))
        path = os.path.join(OUTDIR, code + '.jpg')
        if code in done and os.path.exists(path) and md5_of(path) == done[code][4]:
            print('%s 取りずみ（md5 一致）' % code)
            continue
        try:
            size, m1, m2, ctype = get_file(url, path)
            im = Image.open(path)
            h2 = round(int(e['h']) * w2 / int(e['w']))
            if im.width != w2 or abs(im.height - h2) > 2:
                raise RuntimeError('縦横が違う（%d×%d・%d×%d のはず）' % (im.width, im.height, w2, h2))
        except Exception as ex:
            bad += 1
            print('🔴 %s 失敗: %s' % (code, ex))
            if bad >= 2:
                print('🔴 2点失敗＝止める（組み立ての誤りなら待っても無駄）')
                return 1
            continue
        write_log([datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), code, 'photo', size, m1, m2, '%d×%d' % (im.width, im.height),
                   'src/commons/c33/%s.jpg' % code, url.rsplit('/', 1)[1]])
        cred[code] = '\t'.join([code, re.sub(r'\s+', ' ', str(e.get('author') or '')).strip(), (e.get('lic') or ['?'])[0],
                                'https://commons.wikimedia.org/wiki/' + e['title'].replace(' ', '_')])
        with open(CRED, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(cred[c] for c in sorted(cred, key=lambda c: (c[0], int(re.sub(r'\D', '', c) or 0)))) + '\n')
        print('%s ✓ %d bytes・%d×%d・md5 %s（2回一致）[%d/%d]' % (code, size, im.width, im.height, m1[:8], k + 1, len(codes)))
        time.sleep(GAP)
    print('photos 終わり＝失敗 %d' % bad)
    return 1 if bad else 0


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration,start_time', '-of', 'default=nw=1', path],
                         capture_output=True, text=True).stdout
    return ' '.join(out.split())


def video240():
    pathlib.Path(OUTDIR).mkdir(parents=True, exist_ok=True)
    path = os.path.join(OUTDIR, 'V15_240p.webm')
    size, m1, m2, ctype = get_file(V15 % '240p', path, kinds=('video/',))
    write_log([datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'V15_240p', 'video', size, m1, m2, '426×240', 'src/commons/c33/V15_240p.webm', 'GRENFELL.webm.240p.vp9.webm'])
    print('V15_240p ✓ %d bytes・md5 %s（2回一致）・%s' % (size, m1[:8], probe(path)))
    return 0


def video1080(spans):
    pathlib.Path(OUTDIR).mkdir(parents=True, exist_ok=True)
    for sp in spans:
        a, b = [float(x) for x in sp.split('-')]
        path = os.path.join(OUTDIR, 'V15_1080p_%04d_%04d.webm' % (a, b))
        cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-user_agent', UA['User-Agent'], '-reconnect', '1', '-reconnect_on_http_error', '429,5xx',
               '-reconnect_delay_max', '60', '-multiple_requests', '1', '-ss', '%.2f' % a, '-i', V15 % '1080p', '-t', '%.2f' % (b - a), '-c', 'copy', path]
        r = subprocess.run(cmd, capture_output=True, text=True)
        size = os.path.getsize(path) if os.path.exists(path) else 0
        if r.returncode != 0 or size < 1000000:
            print('🔴 %s 失敗（rc %d・%d bytes）: %s' % (sp, r.returncode, size, r.stderr[-300:]))
            return 1
        m1 = md5_of(path)
        time.sleep(2)
        m2 = md5_of(path)
        if m1 != m2:
            print('🔴 md5 が2回で違う: %s' % path)
            return 1
        write_log([datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), 'V15_1080p_%s' % sp, 'video', size, m1, m2, '1920×1080', 'src/commons/c33/' + os.path.split(path)[1], 'GRENFELL.webm.1080p.vp9.webm（-ss %s -t %s -c copy）' % (a, b - a)])
        print('%s ✓ %d bytes・md5 %s（2回一致）・%s' % (sp, size, m1[:8], probe(path)))
        time.sleep(GAP)
    return 0


def selftest():
    bad = 0
    o = 'https://upload.wikimedia.org/wikipedia/commons/e/e0/Grenfell_Tower_fire_%28wider_view%29.jpg?utm_source=commons.wikimedia.org'
    T = [((o, 1920, 2048), ('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Grenfell_Tower_fire_%28wider_view%29.jpg/1920px-Grenfell_Tower_fire_%28wider_view%29.jpg', 1920)),
         ((o, None, 2048), ('https://upload.wikimedia.org/wikipedia/commons/e/e0/Grenfell_Tower_fire_%28wider_view%29.jpg', 2048)),
         ((o, 1920, 1920), ('https://upload.wikimedia.org/wikipedia/commons/e/e0/Grenfell_Tower_fire_%28wider_view%29.jpg', 1920))]
    for args, want in T:
        got = build_url(*args)
        ok = got == want
        print(('OK  ' if ok else 'NG  ') + '組み立て %s' % str(args[1:]) + ('' if ok else ' → %s' % (got,)))
        bad += 0 if ok else 1
    for args, label in (((o, 1689, 2048), '標準でない幅'), (('https://example.org/x.jpg', 1920, 4000), '原本の URL の形')):
        try:
            build_url(*args)
            print('NG  %s を止めない' % label)
            bad += 1
        except ValueError:
            print('OK  %s を止める' % label)
    for g, want in (('縮小版 1920（原本 2048）', 1920), ('原本', None), ('縮小版 3840（原本 6000）', 3840)):
        ok = want_width(g) == want
        print(('OK  ' if ok else 'NG  ') + '取る幅の読み %s' % g)
        bad += 0 if ok else 1
    print('selftest %s' % ('ok' if not bad else 'NG %d' % bad))
    return 1 if bad else 0


def main(argv):
    if '--selftest' in argv:
        return selftest()
    if '--dry' in argv:
        S = load_psv()
        files = json.load(open(CAND, encoding='utf-8'))['files']
        for code in used_codes(S):
            e = files[int(code[1:]) - 1]
            print(code, build_url(e['orig'], want_width(S[code]['get']), int(e['w']))[0].rsplit('/', 2)[-1])
        print('点数', len(used_codes(S)))
        return 0
    if len(argv) > 1 and argv[1] == 'photos':
        return photos(set(argv[2:]))
    if len(argv) > 1 and argv[1] == 'video240':
        return video240()
    if len(argv) > 2 and argv[1] == 'video1080':
        return video1080(argv[2:])
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
