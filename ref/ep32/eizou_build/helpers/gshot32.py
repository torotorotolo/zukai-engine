# -*- coding: utf-8 -*-
"""32本目 ⑤b-3b：地図のカット（衛星 15カット＝一覧 `ref/ep32/eizou_list32.md` の kind「衛星」）の「Google マップの衛星写真」を撮る。
標準ライブラリ＋PIL だけ。31本目の `ref/ep31/eizou_build/helpers/gshot31.py` を写した（表 GMAP と置き場だけ替えた）。

  python -I gshot32.py shot [記号,…] [--out <フォルダ>]   # 下の表 GMAP を撮る → ref/ep32/photo/<file>（1920×1080）。--out は2回撮って比べる用
  python -I gshot32.py px <記号> <緯度> <経度>            # その画の上の画素の位置（描き足す点・札の座標）を印字

作りは22本目の `ref/ep22/eizou_build/helpers/gshot22.py` と同じ（画面ありの Chrome を DevTools の口〈CDP〉で外から操作・倍率2で撮って 0.75 倍＝
瓦の境目の細い線を避ける・15秒待つ）。🔴 撮るたびに読み込みの途中の継ぎ目が出ることがある＝**2回撮って `gseam32.py <A> <B>` で比べ、線の無い方を採る**。
🔴 撮った PNG は公開リポに置かない（`ref/` は git の外）＝Modal の保管庫 `jiko-assets` の `ref/ep32/photo/…` へ入れ、取り戻して md5 を照らす。

■ 表（中心・ズームの決め。点の座標は `tools/cuts/ss.GEO`＝出どころつき・線は `lines32.py` → `ref/ep32/sat_lines32.json`）
  🔴 この回の線＝札は空港・滑走路・川・公の場所だけ（私人の家・乗客の名を付けない）。ズームは住宅が特定できない高さ（いちばん寄って 14＝横 約9キロ）
  映像方針の一覧の「SAT:…」は11の名（撮り方11の見込み）＝同じ広さ・同じズームになる名は1画にまとめた（8画で15カット）：
    G01 ニューヨーク（c109・c501・c521）＝ラガーディア・テターボロ・鳥とぶつかった所・着水した所・飛んだ道の全部が入る引き（ズーム12）
    G02 ラガーディア空港（c201）＝空港とマンハッタンの東（「ニューヨーク市の中にある」）
    G03 ラガーディア空港の滑走路（c212・c406）＝4・22・13・31 の端が入る寄り（ズーム14）
    G04 鳥とぶつかった所（c303・c509）＝空港（下）と鳥とぶつかった所（上）が入る（ズーム13）
    G05 いちばん高い所と左へ曲がった道（c317・c401）
    G06 テターボロ空港（c409・c415）＝滑走路1・19・24 と、15時28分46秒〜29分22秒の機体の位置が入る
    G07 ハドソン川（c421・c512）＝川の上で南へ向かう道と着水した所
    G08 着水した所とフェリー乗り場（c902）＝ウィーホーケンの Port Imperial（ズーム14）
"""
import base64
import io
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
CAP_DPR = 2
GMAP = {
    'G01': dict(ll=(40.815, -73.955), z=12, file='ref/ep32/photo/gmap_g01_newyork.png'),          # c109・c501・c521（横 約37キロ）
    'G02': dict(ll=(40.785, -73.915), z=13, file='ref/ep32/photo/gmap_g02_lga_city.png'),         # c201（横 約18.5キロ・空港は右寄り）
    'G03': dict(ll=(40.7775, -73.8725), z=14, file='ref/ep32/photo/gmap_g03_lga_runways.png'),    # c212・c406（横 約9.3キロ）
    'G04': dict(ll=(40.8125, -73.882), z=13, file='ref/ep32/photo/gmap_g04_birdstrike.png'),      # c303・c509
    'G05': dict(ll=(40.862, -73.915), z=13, file='ref/ep32/photo/gmap_g05_top_turn.png'),         # c317・c401
    'G06': dict(ll=(40.835, -73.995), z=13, file='ref/ep32/photo/gmap_g06_teterboro.png'),        # c409・c415
    'G07': dict(ll=(40.805, -73.985), z=13, file='ref/ep32/photo/gmap_g07_hudson.png'),           # c421・c512
    'G08': dict(ll=(40.7745, -74.006), z=14, file='ref/ep32/photo/gmap_g08_ditch_ferry.png'),     # c902（横 約9.3キロ）
}


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


def shot(codes=None, out=None):
    from PIL import Image
    sel = set(codes.split(',')) if codes else None
    prof = os.path.join(EP, 'src', '_gshot_profile')
    tmp = os.path.join(EP, 'src', '_gshot_html')
    os.makedirs(tmp, exist_ok=True)
    bad = 0
    for code, r in GMAP.items():
        if sel and code not in sel:
            continue
        (lat0, lon0), z = r['ll'], r['z']
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
            call(s, 1, 'Emulation.setDeviceMetricsOverride', {'width': CW, 'height': CH, 'deviceScaleFactor': CAP_DPR, 'mobile': False})
            call(s, 2, 'Page.reload')
            time.sleep(15)
            m = call(s, 3, 'Page.captureScreenshot', {'format': 'png'})
            dst = os.path.join(out, os.path.basename(r['file'])) if out else os.path.join(REPO, r['file'])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            im = Image.open(io.BytesIO(base64.b64decode(m['result']['data']))).convert('RGB')
            if im.size != (CW * CAP_DPR, CH * CAP_DPR):
                raise RuntimeError('撮れた絵の大きさ %s が %dx%d でない' % (im.size, CW * CAP_DPR, CH * CAP_DPR))
            im.resize((round(CW * DPR), round(CH * DPR)), Image.LANCZOS).save(dst)
            print('%s → %s（%d bytes）' % (code, dst, os.path.getsize(dst)))
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
        args = [a for a in sys.argv[2:] if not a.startswith('--')]
        o = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
        args = [a for a in args if a != o]
        sys.exit(shot(args[0] if args else None, o))
    elif sys.argv[1] == 'px':
        r = GMAP[sys.argv[2]]
        print('%.1f %.1f' % px(float(sys.argv[3]), float(sys.argv[4]), *r['ll'], r['z']))
