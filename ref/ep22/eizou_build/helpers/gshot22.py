# -*- coding: utf-8 -*-
"""22本目：地図のカットの「Google マップの衛星写真」を撮る（了承② 2026-10-14＝撮るのは ⑤b-1）。標準ライブラリだけ。

  python -I gshot22.py shot [記号,…]        # sources22.tsv の class=gmap（media＝gmap:緯度,経度,ズーム）を撮る → file の PNG（1920×1080）
  python -I gshot22.py px <記号> <緯度> <経度>  # その画の上の画素の位置（描き足す点・線の座標）を印字

🔴 画面なしの Chrome（--headless --screenshot）では地図が読み込まれず灰色のまま（19本目・22本目で確かめた）＝画面ありの Chrome を
   DevTools の口（CDP）で外から操作して撮る。デスクトップに Chrome の窓が十数秒出る。プロフィールは src/_gshot_profile（git の外）。
🔴 倍率1.5（CSS の 1280×720 → 1920×1080）で撮る＝右下の帰属の行の字を1.5倍に（Google の決まり＝行は動かせない・読める大きさ）。
   描き足し（点・線・札）は絵に焼かず、本番の描き手で重ねる（Google の決まり＝描き足しは可・色を変えない・地図そのものを大きく変えない）。
   左上の「マップで開く」・右下の全画面の印は Google の操作の部品＝⑤b で題や札の帯で隠してよいか確かめる（帰属の行は隠さない）。
"""
import base64
import csv
import json
import math
import os
import socket
import struct
import subprocess
import sys
import time
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
PORT = 9333
CW, CH, DPR = 1280, 720, 1.5


def gmaps():
    with open(os.path.join(HERE, 'sources22.tsv'), encoding='utf-8') as f:
        lines = [ln for ln in f if not ln.startswith('#') and ln.strip()]
    return {r['code']: r for r in csv.DictReader(lines, delimiter='\t') if r['class'] == 'gmap'}


def view(r):
    lat, lon, z = r['media'].split(':', 1)[1].split(',')
    return float(lat), float(lon), int(z)


def px(lat, lon, lat0, lon0, z):
    """Web メルカトル（256 の瓦）で、中心 (lat0, lon0)・ズーム z の画（CSS 1280×720・倍率1.5）の上の画素（1920×1080 の座標）。"""
    def wx(lo):
        return (lo + 180) / 360 * 256 * 2 ** z

    def wy(la):
        p = math.radians(la)
        return (1 - math.log(math.tan(p) + 1 / math.cos(p)) / math.pi) / 2 * 256 * 2 ** z
    return ((CW / 2 + wx(lon) - wx(lon0)) * DPR, (CH / 2 + wy(lat) - wy(lat0)) * DPR)


def ws(url):
    hostport, path = url[5:].split('/', 1)
    host, port = hostport.split(':')
    s = socket.create_connection((host, int(port)), timeout=30)
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


def call(s, i, method, params=None):
    send(s, {'id': i, 'method': method, 'params': params or {}})
    while True:
        m = recv(s)
        if m.get('id') == i:
            return m


def shot(codes=None):
    sel = set(codes.split(',')) if codes else None
    prof = os.path.join(EP, 'src', '_gshot_profile')
    tmp = os.path.join(EP, 'src', '_gshot_html')
    os.makedirs(tmp, exist_ok=True)
    bad = 0
    for code, r in gmaps().items():
        if sel and code not in sel:
            continue
        lat0, lon0, z = view(r)
        html = os.path.join(tmp, '%s.html' % code)
        open(html, 'w', encoding='utf-8').write(
            '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;width:%dpx;height:%dpx;overflow:hidden}'
            'iframe{border:0;width:%dpx;height:%dpx}</style></head><body><iframe src="https://maps.google.com/maps?ll=%s,%s&z=%d&t=k&hl=ja&output=embed">'
            '</iframe></body></html>' % (CW, CH, CW, CH, lat0, lon0, z))
        p = subprocess.Popen([CHROME, '--remote-debugging-port=%d' % PORT, '--user-data-dir=%s' % prof, '--no-first-run', '--no-default-browser-check',
                              '--window-size=1400,900', '--new-window', 'file:///' + html.replace('\\', '/')])
        try:
            page = None
            for _ in range(40):
                try:
                    ts = json.loads(urllib.request.urlopen('http://127.0.0.1:%d/json' % PORT, timeout=2).read())
                    page = next((t for t in ts if t.get('type') == 'page' and t.get('url', '').startswith('file:')), None)
                    if page:
                        break
                except Exception:
                    pass
                time.sleep(0.5)
            s = ws(page['webSocketDebuggerUrl'])
            call(s, 1, 'Emulation.setDeviceMetricsOverride', {'width': CW, 'height': CH, 'deviceScaleFactor': DPR, 'mobile': False})
            call(s, 2, 'Page.reload')
            time.sleep(15)
            m = call(s, 3, 'Page.captureScreenshot', {'format': 'png'})
            dst = os.path.join(REPO, r['file'])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            open(dst, 'wb').write(base64.b64decode(m['result']['data']))
            print('%s → %s（%d bytes）＝絵を原寸で見て、地図が読み込まれたか・帰属の行があるかを確かめる' % (code, r['file'], os.path.getsize(dst)))
        except Exception as e:
            print('%s 🔴 撮れない：%s' % (code, e))
            bad += 1
        finally:
            p.terminate()
            try:
                p.wait(timeout=10)
            except Exception:
                p.kill()
        time.sleep(3)
    return 1 if bad else 0


if __name__ == '__main__':
    if sys.argv[1] == 'shot':
        sys.exit(shot(sys.argv[2] if len(sys.argv) > 2 else None))
    elif sys.argv[1] == 'px':
        r = gmaps()[sys.argv[2]]
        print('%.1f %.1f' % px(float(sys.argv[3]), float(sys.argv[4]), *view(r)))
