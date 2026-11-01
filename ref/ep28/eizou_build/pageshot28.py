# -*- coding: utf-8 -*-
"""28本目：会社の頁と公的な機関の頁の画面を、画面なしの Chrome を DevTools の口（CDP）で外から操作して撮る（⑤b-2・2026-11-01）。標準ライブラリだけ。
作りは `ref/ep26/eizou_build/helpers/gshot26.py`（websocket の手書き）と同じ。Google の地図と違い WebGL が要らない＝画面なし（--headless=new）で写る。

  python -I pageshot28.py text <URL> <出力ファイル>   # 頁の本文の字（規約を読む・撮る前に中身を読む）
  python -I pageshot28.py lines <記号>                # 頁の塊の字と y（CSS px）＝切り口 head・tail を選ぶ。字は出力ファイルへ（名前が混ざりうる）
  python -I pageshot28.py shot <記号>…                # 表 PAGES の head〜tail だけを撮る → ref/ep28/src/pages/<記号>.png＋撮った日時と md5 を src/pages/log.tsv へ

🔴 撮るのは切り口の中だけ（頁の頭＝社名のロゴ・見出しの帯を写さない・「clip」で撮るので外は絵にならない）。
🔴 出力は git の外（`ref/ep28/src/`）＝公開リポに置くかは束の道具 `qa_out/ep28_assets.py` の台帳が決める。
"""
import base64
import json
import os
import socket
import struct
import subprocess
import sys
import time
import hashlib
import urllib.request
from datetime import datetime, timezone, timedelta

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
OUT = os.path.join(EP, 'src', 'pages')
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PORT = 9334
VIEW_W, VIEW_H = 1100, 1400
SCALE = 2                # 撮る倍率（CSS 1px＝2画素）。額の中で字が読めるように
PROFILE = os.environ.get('PAGESHOT_PROFILE') or os.path.join(os.environ['TEMP'], 'pageshot28_profile')
WAIT = 2.5               # load のあと待つ秒（遅れて出る部品）

# 記号 → 頁の URL と切り口（head＝切り口の頭の塊の字の始まり・tail＝切り口の尻の塊の字の始まり）。⑤b-2 に `lines` で選ぶ
PAGES = json.load(open(os.path.join(HERE, 'pages28.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'pages28.json')) else {}

JS_BLOCKS = r"""
(() => {
  const out = [];
  const seen = new Set();
  for (const el of document.querySelectorAll('h1,h2,h3,h4,h5,p,li,dt,dd,th,td,table,pre,blockquote,section,article,main,div')) {
    const direct = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim());
    const isTable = el.tagName === 'TABLE';
    if (!direct && !isTable && !/^(H[1-5]|P|LI|TH|TD|DT|DD)$/.test(el.tagName)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    const t = (el.innerText || '').replace(/\s+/g, ' ').trim();
    if (!t) continue;
    out.push({tag: el.tagName, x: Math.round(r.left + scrollX), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height), t: t.slice(0, 80)});
  }
  return JSON.stringify({H: document.documentElement.scrollHeight, W: document.documentElement.scrollWidth, title: document.title, blocks: out});
})()
"""


def ws(url):
    hostport, path = url[5:].split('/', 1)
    host, port = hostport.split(':')
    s = socket.create_connection((host, int(port)), timeout=60)
    key = base64.b64encode(os.urandom(16)).decode()
    s.sendall(('GET /%s HTTP/1.1\r\nHost: %s\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: %s\r\n'
               'Sec-WebSocket-Version: 13\r\n\r\n' % (path, hostport, key)).encode())
    buf = b''
    while b'\r\n\r\n' not in buf:
        buf += s.recv(4096)
    if b' 101 ' not in buf.split(b'\r\n')[0]:
        raise SystemExit('🔴 websocket の握手に失敗')
    return s


def send(s, obj):
    data = json.dumps(obj).encode()
    hdr = bytearray([0x81])
    n = len(data)
    hdr += bytes([0x80 | n]) if n < 126 else (bytes([0x80 | 126]) + struct.pack('>H', n) if n < 65536 else bytes([0x80 | 127]) + struct.pack('>Q', n))
    mask = os.urandom(4)
    s.sendall(bytes(hdr) + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))


def recv_exact(s, n):
    out = b''
    while len(out) < n:
        c = s.recv(n - len(out))
        if not c:
            raise SystemExit('🔴 websocket が切れた')
        out += c
    return out


def recv(s):
    msg = b''
    while True:
        b0, b1 = recv_exact(s, 2)
        n = b1 & 0x7f
        n = struct.unpack('>H', recv_exact(s, 2))[0] if n == 126 else (struct.unpack('>Q', recv_exact(s, 8))[0] if n == 127 else n)
        msg += recv_exact(s, n)
        if b0 & 0x80:
            return json.loads(msg.decode('utf-8', 'replace'))


class Tab:
    def __init__(self):
        self.p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--no-default-browser-check',
                                   f'--remote-debugging-port={PORT}', f'--user-data-dir={PROFILE}', f'--window-size={VIEW_W},{VIEW_H}', 'about:blank'],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        url = None
        for _ in range(60):
            time.sleep(0.5)
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json', timeout=3))
                url = next(t['webSocketDebuggerUrl'] for t in tabs if t.get('type') == 'page')
                break
            except Exception:  # noqa: BLE001  立ち上がるのを待つ
                continue
        if not url:
            self.close()
            raise SystemExit('🔴 Chrome の DevTools の口に繋がらない')
        self.s = ws(url)
        self.i = 0
        self.call('Page.enable')
        self.call('Runtime.enable')
        self.call('Emulation.setDeviceMetricsOverride', {'width': VIEW_W, 'height': VIEW_H, 'deviceScaleFactor': 1, 'mobile': False})

    def call(self, method, params=None):
        self.i += 1
        send(self.s, {'id': self.i, 'method': method, 'params': params or {}})
        while True:
            m = recv(self.s)
            if m.get('id') == self.i:
                if 'error' in m:
                    raise SystemExit(f'🔴 {method}: {m["error"]}')
                return m.get('result', {})

    def go(self, url):
        self.i += 1
        send(self.s, {'id': self.i, 'method': 'Page.navigate', 'params': {'url': url}})
        t0 = time.time()
        loaded = False
        err = None
        while time.time() - t0 < 60:
            m = recv(self.s)
            if m.get('id') == self.i and m.get('result', {}).get('errorText'):
                err = m['result']['errorText']
                break
            if m.get('method') == 'Page.loadEventFired':
                loaded = True
                break
        if err or not loaded:
            raise SystemExit(f'🔴 頁が開けない：{url}（{err or "60秒で load が来ない"}）')
        time.sleep(WAIT)

    def js(self, code):
        r = self.call('Runtime.evaluate', {'expression': code, 'returnByValue': True, 'awaitPromise': True})
        if r.get('exceptionDetails'):
            raise SystemExit(f'🔴 JS: {r["exceptionDetails"]}')
        return r['result'].get('value')

    def close(self):
        try:
            self.p.terminate()
            self.p.wait(10)
        except Exception:  # noqa: BLE001
            self.p.kill()


def _blocks(t):
    return json.loads(t.js(JS_BLOCKS))


def _find(blocks, head, start=-1):
    """字の始まりが head に当たる塊のうち、y が start より下で、いちばん内側（小さい）もの"""
    hit = [b for b in blocks if b['t'].startswith(head) and b['y'] > start]
    if not hit:
        raise SystemExit(f'🔴 切り口の字が頁に無い：{head}')
    y0 = min(b['y'] for b in hit)
    same = [b for b in hit if b['y'] == y0]
    return min(same, key=lambda b: b['w'] * b['h'])


def cmd_text(url, out):
    t = Tab()
    try:
        t.go(url)
        txt = t.js('document.body.innerText')
    finally:
        t.close()
    open(out, 'w', encoding='utf-8', newline='\n').write(txt)
    print(f'→ {out}（{len(txt)}字）')


def cmd_lines(code):
    os.makedirs(OUT, exist_ok=True)
    p = PAGES[code]
    t = Tab()
    try:
        t.go(p['url'])
        d = _blocks(t)
    finally:
        t.close()
    out = os.path.join(OUT, f'{code}_lines.txt')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# {d["W"]}x{d["H"]} {d["title"]}\n')
        for b in sorted(d['blocks'], key=lambda b: (b['y'], b['x'])):
            f.write(f'{b["y"]:6} {b["x"]:5} {b["w"]:5}x{b["h"]:<5} {b["tag"]:6} {b["t"]}\n')
    print(f'→ {out}（{len(d["blocks"])}塊・頁 {d["W"]}x{d["H"]}）')


def cmd_shot(codes):
    os.makedirs(OUT, exist_ok=True)
    log = os.path.join(OUT, 'log.tsv')
    new = not os.path.exists(log)
    t = Tab()
    jst = timezone(timedelta(hours=9))
    try:
        with open(log, 'a', encoding='utf-8', newline='\n') as f:
            if new:
                f.write('撮った日時\t記号\tURL\t切り口(CSS px)\t画素\tmd5\n')
            for code in codes:
                p = PAGES[code]
                t.go(p['url'])
                d = _blocks(t)
                a = _find(d['blocks'], p['head'], p.get('after', -1))
                b = _find(d['blocks'], p['tail'], a['y'] - 1)
                pad = p.get('pad', 12)
                x0 = p.get('x0', min(a['x'], b['x']) - pad)
                x1 = p.get('x1', max(a['x'] + a['w'], b['x'] + b['w']) + pad)
                y0 = a['y'] - pad
                y1 = p.get('y1', b['y'] + b['h'] + pad)
                clip = dict(x=max(0, x0), y=max(0, y0), width=x1 - max(0, x0), height=y1 - max(0, y0), scale=SCALE)
                r = t.call('Page.captureScreenshot', {'format': 'png', 'clip': clip, 'captureBeyondViewport': True})
                raw = base64.b64decode(r['data'])
                out = os.path.join(OUT, f'{code}.png')
                open(out, 'wb').write(raw)
                h = hashlib.md5(raw).hexdigest()
                when = datetime.now(jst).strftime('%Y-%m-%d %H:%M:%S%z')
                f.write(f'{when}\t{code}\t{p["url"]}\t{clip["x"]},{clip["y"]},{clip["width"]},{clip["height"]}\t{int(clip["width"] * SCALE)}x{int(clip["height"] * SCALE)}\t{h}\n')
                print(f'✓ {code}: {when}  切り口 {clip["x"]},{clip["y"]} {clip["width"]}x{clip["height"]}（CSS px）→ {out}  md5 {h[:8]}')
    finally:
        t.close()


if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == 'text':
        cmd_text(a[1], a[2])
    elif a and a[0] == 'lines':
        for c in a[1:]:
            cmd_lines(c)
    elif a and a[0] == 'shot':
        cmd_shot(a[1:])
    else:
        print(__doc__)
